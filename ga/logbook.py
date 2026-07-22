"""Structured experiment logging — the implementation of LOGGING.md.

One experiment = one directory under experiments/run_logs/<experiment_id>/
containing a frozen config.json and an append-only events.jsonl. Every event
is flushed (and fsynced) immediately, so a crash leaves a complete log up to
the last event. A cross-experiment index (experiments/index.jsonl) gets one
row per experiment, updated at start and end, with stale-"running"
reconciliation at every startup (a crashed process cannot mark itself
crashed).

Two ways to use it:

- Single process: `Logbook` directly (start_experiment / append_event /
  write_checkpoint / finish_experiment).
- Parallel evaluation pool (PLAN.md Stage 2): `ExperimentWriter` runs a
  Logbook in a dedicated writer process; workers get a picklable
  `EventSink` and never touch the files — flush-per-event JSONL appends
  from multiple processes would interleave and corrupt lines.

Also here, because they are part of the logging contract rather than GA
logic: `genome_hash` (fitness-cache / reproducibility identity),
`derive_eval_seed` (per-evaluation SeedSequence derivation), and
`append_solver_validation` (the test_solver_clm.py hook writing
experiments/solver_validation.jsonl).
"""

import hashlib
import json
import multiprocessing
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 1

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EXPERIMENTS_ROOT = PROJECT_ROOT / "experiments"


# --- git / environment provenance ---

def _git(args, repo_root):
    return subprocess.run(
        ["git", *args], cwd=repo_root, capture_output=True, text=True, check=True
    ).stdout


def code_version(repo_root=PROJECT_ROOT):
    """Current commit hash — the `code_version` field on every artifact."""
    return _git(["rev-parse", "HEAD"], repo_root).strip()


def working_tree_dirty(repo_root=PROJECT_ROOT):
    """(dirty, diff_hash). Dirty = any tracked-file change, or an untracked
    .py file (untracked code can be imported by a run; untracked non-code
    like editor state cannot pin or unpin reproducibility either way)."""
    status = _git(["status", "--porcelain"], repo_root)
    dirty = False
    for line in status.splitlines():
        if line.startswith("??"):
            if line[3:].strip().endswith(".py"):
                dirty = True
        elif line.strip():
            dirty = True
    if not dirty:
        return False, None
    diff = _git(["diff", "HEAD"], repo_root)
    return True, hashlib.sha256(diff.encode()).hexdigest()


def env_info():
    import numpy

    return {
        "numpy_version": numpy.__version__,
        "python_version": sys.version.split()[0],
        "blas_threads": os.environ.get("OMP_NUM_THREADS"),
        "fft_backend": "numpy.fft (pocketfft)",
    }


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


# --- identities the logging contract depends on ---

def genome_hash(coeffs, envelope_p):
    """Stable identity of (coefficient vector, envelope exponent p) — keys
    the fitness cache and the reproducibility audit (LOGGING.md schema #3)."""
    import numpy as np

    h = hashlib.sha256()
    h.update(np.asarray(coeffs, dtype=np.float64).tobytes())
    h.update(f"p={float(envelope_p)!r}".encode())
    return h.hexdigest()


def derive_eval_seed(root_seed, genome_id):
    """Deterministic per-evaluation seed from (root_seed, genome_id), so any
    single evaluation is re-runnable standalone and results are independent
    of evaluation order (LOGGING.md RNG principle)."""
    import numpy as np

    gid = int.from_bytes(hashlib.sha256(str(genome_id).encode()).digest()[:8], "big")
    return int(np.random.SeedSequence([int(root_seed), gid]).generate_state(1)[0])


# --- the logbook proper ---

class DirtyTreeError(RuntimeError):
    pass


# config keys mirrored into the index row (LOGGING.md schema #8)
_CONFIG_SUMMARY_KEYS = (
    "population_size",
    "genome_length_N",
    "ga_operators",
    "symmetry",
    "gclm_a",
    "fitness_axis",
)


class Logbook:
    def __init__(self, experiments_root=DEFAULT_EXPERIMENTS_ROOT,
                 repo_root=PROJECT_ROOT):
        self.experiments_root = Path(experiments_root)
        self.repo_root = Path(repo_root)
        self.experiment_id = None
        self._events_file = None

    # -- lifecycle --

    def start_experiment(self, config, allow_dirty=False, experiment_id=None,
                         staleness_seconds=3600):
        dirty, diff_hash = working_tree_dirty(self.repo_root)
        if dirty and not allow_dirty:
            raise DirtyTreeError(
                "working tree has uncommitted code changes; commit first, or "
                "pass allow_dirty=True to mark this run as a non-reproducible "
                "throwaway (code_dirty: true is recorded in config and index)"
            )

        self._reconcile_stale_running(staleness_seconds)

        self.experiment_id = experiment_id or (
            time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
        )
        exp_dir = self._experiment_dir()
        for sub in ("checkpoints", "series", "genomes"):
            (exp_dir / sub).mkdir(parents=True, exist_ok=True)

        full_config = {
            "schema_version": SCHEMA_VERSION,
            "experiment_id": self.experiment_id,
            "timestamp_start": _utc_now(),
            "code_version": code_version(self.repo_root),
            "code_dirty": dirty,
            **({"diff_hash": diff_hash} if dirty else {}),
            "env": env_info(),
            **config,
        }
        with open(exp_dir / "config.json", "w") as f:
            json.dump(full_config, f, indent=2, default=_jsonable)

        self._events_file = open(exp_dir / "events.jsonl", "a")

        self._append_index_row({
            "schema_version": SCHEMA_VERSION,
            "experiment_id": self.experiment_id,
            "code_version": full_config["code_version"],
            "code_dirty": dirty,
            "timestamp_start": full_config["timestamp_start"],
            "timestamp_end": None,
            "status": "running",
            "config_summary": {
                key: config.get(key) for key in _CONFIG_SUMMARY_KEYS
            },
            "best_ever_fitness": None,
            "best_genome_id": None,
            "baseline_fitness_mean": None,
            "baseline_fitness_max": None,
            "n_tier2_promotions": 0,
        })
        return self.experiment_id

    def append_event(self, event_type, payload):
        """Append one event row and flush it to disk before returning."""
        if self._events_file is None:
            raise RuntimeError("no experiment started")
        row = {
            "schema_version": SCHEMA_VERSION,
            "experiment_id": self.experiment_id,
            "event": event_type,
            "timestamp": _utc_now(),
            **payload,
        }
        self._events_file.write(json.dumps(row, default=_jsonable) + "\n")
        self._events_file.flush()
        os.fsync(self._events_file.fileno())

    def write_checkpoint(self, generation_index, population, rng_state,
                         archive=None):
        """Full-population snapshot for crash recovery (LOGGING.md checkpoint
        principle). `rng_state` must be the generator's
        `bit_generator.state` dict — resuming without it silently breaks
        reproducibility. `archive` is the MAP-Elites archive, if any."""
        path = (self._experiment_dir() / "checkpoints"
                / f"gen_{generation_index:05d}.json")
        tmp = path.with_suffix(".json.tmp")
        with open(tmp, "w") as f:
            json.dump({
                "schema_version": SCHEMA_VERSION,
                "experiment_id": self.experiment_id,
                "generation_index": generation_index,
                "timestamp": _utc_now(),
                "population": population,
                "rng_state": rng_state,
                "archive": archive,
            }, f, default=_jsonable)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
        return path

    def finish_experiment(self, status="completed", **summary):
        self._update_index_row(self.experiment_id, {
            "status": status,
            "timestamp_end": _utc_now(),
            **summary,
        })
        if self._events_file is not None:
            self._events_file.close()
            self._events_file = None

    # -- index handling --

    @property
    def _index_path(self):
        return self.experiments_root / "index.jsonl"

    def _experiment_dir(self):
        return self.experiments_root / "run_logs" / self.experiment_id

    def _append_index_row(self, row):
        self.experiments_root.mkdir(parents=True, exist_ok=True)
        with open(self._index_path, "a") as f:
            f.write(json.dumps(row, default=_jsonable) + "\n")
            f.flush()
            os.fsync(f.fileno())

    def _read_index(self):
        if not self._index_path.exists():
            return []
        with open(self._index_path) as f:
            return [json.loads(line) for line in f if line.strip()]

    def _rewrite_index(self, rows):
        tmp = self._index_path.with_suffix(".jsonl.tmp")
        with open(tmp, "w") as f:
            for row in rows:
                f.write(json.dumps(row, default=_jsonable) + "\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, self._index_path)

    def _update_index_row(self, experiment_id, updates):
        rows = self._read_index()
        for row in rows:
            if row.get("experiment_id") == experiment_id:
                row.update(updates)
        self._rewrite_index(rows)

    def _reconcile_stale_running(self, staleness_seconds):
        """Rewrite stale "running" index rows as "crashed" (LOGGING.md schema
        #8): a row is stale when its events.jsonl is missing or hasn't been
        touched within the staleness threshold. Runs at every experiment
        start, so the index converges to the truth without relying on dying
        processes to be polite."""
        rows = self._read_index()
        changed = False
        now = time.time()
        for row in rows:
            if row.get("status") != "running":
                continue
            events = (self.experiments_root / "run_logs"
                      / row["experiment_id"] / "events.jsonl")
            stale = (not events.exists()
                     or now - events.stat().st_mtime > staleness_seconds)
            if stale:
                row["status"] = "crashed"
                changed = True
        if changed:
            self._rewrite_index(rows)


def _jsonable(obj):
    """JSON fallback for numpy scalars/arrays in payloads."""
    import numpy as np

    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    raise TypeError(f"not JSON serializable: {type(obj)!r}")


# --- single-writer process for the parallel evaluation pool ---

class EventSink:
    """Picklable worker-side handle: append_event only. Workers never touch
    files under the experiment directory."""

    def __init__(self, queue):
        self._queue = queue

    def append_event(self, event_type, payload):
        self._queue.put(("event", event_type, payload))


def _writer_main(cmd_queue, reply_queue, experiments_root, repo_root, config,
                 allow_dirty, experiment_id, staleness_seconds):
    logbook = Logbook(experiments_root, repo_root)
    try:
        eid = logbook.start_experiment(
            config, allow_dirty=allow_dirty, experiment_id=experiment_id,
            staleness_seconds=staleness_seconds,
        )
    except Exception as exc:
        reply_queue.put(("error", repr(exc)))
        return
    reply_queue.put(("started", eid))
    while True:
        cmd = cmd_queue.get()
        kind = cmd[0]
        if kind == "event":
            logbook.append_event(cmd[1], cmd[2])
        elif kind == "checkpoint":
            logbook.write_checkpoint(*cmd[1:])
        elif kind == "finish":
            logbook.finish_experiment(cmd[1], **cmd[2])
            reply_queue.put(("finished", eid))
            return


class ExperimentWriter:
    """Owns a Logbook in a dedicated process; every file under the experiment
    directory has exactly one writer no matter how many workers evaluate
    fitness (LOGGING.md single-writer principle)."""

    def __init__(self, config, experiments_root=DEFAULT_EXPERIMENTS_ROOT,
                 repo_root=PROJECT_ROOT, allow_dirty=False, experiment_id=None,
                 staleness_seconds=3600):
        ctx = multiprocessing.get_context()
        # Manager queue (not a raw mp.Queue) so the EventSink stays picklable
        # through any worker-pool API, not only fork-inheritance.
        self._manager = ctx.Manager()
        self._cmd_queue = self._manager.Queue()
        self._reply_queue = ctx.Queue()
        self._process = ctx.Process(
            target=_writer_main,
            args=(self._cmd_queue, self._reply_queue, str(experiments_root),
                  str(repo_root), config, allow_dirty, experiment_id,
                  staleness_seconds),
            daemon=True,
        )
        self._process.start()
        kind, value = self._reply_queue.get()
        if kind == "error":
            self._process.join()
            raise RuntimeError(f"experiment failed to start: {value}")
        self.experiment_id = value

    @property
    def sink(self):
        """Picklable EventSink to hand to worker processes."""
        return EventSink(self._cmd_queue)

    def append_event(self, event_type, payload):
        self._cmd_queue.put(("event", event_type, payload))

    def write_checkpoint(self, generation_index, population, rng_state,
                         archive=None):
        self._cmd_queue.put(
            ("checkpoint", generation_index, population, rng_state, archive))

    def finish(self, status="completed", **summary):
        self._cmd_queue.put(("finish", status, summary))
        kind, _ = self._reply_queue.get()
        assert kind == "finished"
        self._process.join()
        self._manager.shutdown()


# --- solver-validation hook (LOGGING.md schema #9) ---

def append_solver_validation(rows, experiments_root=DEFAULT_EXPERIMENTS_ROOT,
                             repo_root=PROJECT_ROOT):
    """Append Stage 1 acceptance-check results to
    experiments/solver_validation.jsonl, tagged with the current commit, so
    solver accuracy is a tracked series across commits rather than a
    one-time gate. Called by test_solver_clm.py on every run."""
    root = Path(experiments_root)
    root.mkdir(parents=True, exist_ok=True)
    version = code_version(repo_root)
    stamp = _utc_now()
    with open(root / "solver_validation.jsonl", "a") as f:
        for row in rows:
            f.write(json.dumps({
                "schema_version": SCHEMA_VERSION,
                "code_version": version,
                "timestamp": stamp,
                **row,
            }, default=_jsonable) + "\n")
        f.flush()
        os.fsync(f.fileno())
