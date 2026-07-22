"""Tests for ga/logbook.py — the LOGGING.md logging contract.

Each test builds a throwaway git repo + experiments root in a temp dir, so
nothing here reads or writes the real repository's state or the real
experiments/ directory.
"""

import json
import multiprocessing
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np

from ga.logbook import (
    DirtyTreeError,
    EventSink,
    ExperimentWriter,
    Logbook,
    derive_eval_seed,
    genome_hash,
)


class _TempRepo:
    """Context manager: a fresh git repo with one commit, plus an
    experiments root, both deleted on exit."""

    def __enter__(self):
        self.dir = Path(tempfile.mkdtemp(prefix="logbook_test_"))
        self.repo = self.dir / "repo"
        self.experiments = self.dir / "experiments"
        self.repo.mkdir()
        run = lambda *args: subprocess.run(
            ["git", *args], cwd=self.repo, check=True, capture_output=True)
        run("init", "-q")
        run("config", "user.email", "test@test")
        run("config", "user.name", "test")
        (self.repo / "code.py").write_text("x = 1\n")
        run("add", "code.py")
        run("commit", "-qm", "init")
        return self

    def __exit__(self, *exc):
        shutil.rmtree(self.dir, ignore_errors=True)

    def logbook(self):
        return Logbook(experiments_root=self.experiments, repo_root=self.repo)


def test_dirty_tree_guard():
    with _TempRepo() as tr:
        # Clean tree: starts fine, code_dirty is false.
        eid = tr.logbook().start_experiment({"population_size": 10})
        config = json.loads(
            (tr.experiments / "run_logs" / eid / "config.json").read_text())
        assert config["code_dirty"] is False
        assert "diff_hash" not in config

        # Modified tracked file: refused by default.
        (tr.repo / "code.py").write_text("x = 2\n")
        try:
            tr.logbook().start_experiment({})
        except DirtyTreeError:
            pass
        else:
            raise AssertionError("dirty tree must refuse to launch")

        # Explicit override: allowed, but marked non-reproducible.
        eid2 = tr.logbook().start_experiment({}, allow_dirty=True)
        config2 = json.loads(
            (tr.experiments / "run_logs" / eid2 / "config.json").read_text())
        assert config2["code_dirty"] is True
        assert len(config2["diff_hash"]) == 64
        index_rows = [json.loads(l) for l in
                      (tr.experiments / "index.jsonl").read_text().splitlines()]
        assert [r["code_dirty"] for r in index_rows] == [False, True]


def test_untracked_python_counts_as_dirty():
    with _TempRepo() as tr:
        (tr.repo / "notes.txt").write_text("not code\n")
        tr.logbook().start_experiment({})  # untracked non-code: still clean
        (tr.repo / "sneaky.py").write_text("y = 2\n")
        try:
            tr.logbook().start_experiment({})
        except DirtyTreeError:
            pass
        else:
            raise AssertionError("untracked .py must count as dirty")


def test_events_are_flushed_and_self_describing():
    with _TempRepo() as tr:
        lb = tr.logbook()
        eid = lb.start_experiment({"population_size": 5})
        lb.append_event("genome_eval", {"genome_id": "g0", "critical_value": 0.5})
        lb.append_event("generation", {"generation_index": 0})
        # Read back WITHOUT finishing: flush-per-event means a crash here
        # would still leave both complete lines on disk.
        lines = (tr.experiments / "run_logs" / eid / "events.jsonl").read_text().splitlines()
        assert len(lines) == 2
        rows = [json.loads(l) for l in lines]
        for row in rows:
            assert row["experiment_id"] == eid
            assert row["schema_version"] == 1
            assert "timestamp" in row
        assert rows[0]["event"] == "genome_eval"
        assert rows[1]["event"] == "generation"


def test_index_lifecycle_and_stale_reconciliation():
    with _TempRepo() as tr:
        # Experiment A "crashes": started, never finished.
        lb_a = tr.logbook()
        lb_a.start_experiment({"population_size": 1})

        # Later startup reconciles A's stale "running" row to "crashed"
        # (staleness 0 => any not-just-written events file counts as stale).
        lb_b = tr.logbook()
        eid_b = lb_b.start_experiment({"population_size": 2},
                                      staleness_seconds=-1)
        lb_b.finish_experiment(status="completed", best_ever_fitness=1.5)

        rows = {r["experiment_id"]: r for r in (
            json.loads(l) for l in
            (tr.experiments / "index.jsonl").read_text().splitlines())}
        statuses = sorted(r["status"] for r in rows.values())
        assert statuses == ["completed", "crashed"], statuses
        assert rows[eid_b]["best_ever_fitness"] == 1.5
        assert rows[eid_b]["timestamp_end"] is not None


def test_checkpoint_rng_state_roundtrip():
    with _TempRepo() as tr:
        lb = tr.logbook()
        eid = lb.start_experiment({})
        rng = np.random.default_rng(42)
        rng.standard_normal(100)  # advance past the seed state
        population = [{"genome_id": "g1", "coeffs": list(np.arange(4.0)),
                       "envelope_p": 1.5}]
        path = lb.write_checkpoint(7, population, rng.bit_generator.state)
        expected = rng.standard_normal(5)

        saved = json.loads(Path(path).read_text())
        assert saved["generation_index"] == 7
        assert saved["population"] == population
        restored = np.random.default_rng()
        restored.bit_generator.state = saved["rng_state"]
        # The restored generator must continue the exact stream — resuming
        # without this diverges from an uninterrupted run (LOGGING.md).
        assert np.array_equal(restored.standard_normal(5), expected)


def test_genome_hash_and_eval_seed_are_stable():
    coeffs = np.array([0.1, -0.2, 0.3])
    assert genome_hash(coeffs, 1.5) == genome_hash(list(coeffs), 1.5)
    assert genome_hash(coeffs, 1.5) != genome_hash(coeffs, 1.6)
    assert genome_hash(coeffs, 1.5) != genome_hash(coeffs * 1.0000001, 1.5)

    s1 = derive_eval_seed(123, "gen3-genome7")
    assert s1 == derive_eval_seed(123, "gen3-genome7")  # deterministic
    assert s1 != derive_eval_seed(124, "gen3-genome7")  # root seed matters
    assert s1 != derive_eval_seed(123, "gen3-genome8")  # genome id matters


def _worker_send_events(args):
    sink, worker_id, count = args
    for i in range(count):
        sink.append_event("genome_eval",
                          {"genome_id": f"w{worker_id}-{i}", "worker": worker_id})
    return worker_id


def test_single_writer_with_parallel_workers():
    with _TempRepo() as tr:
        writer = ExperimentWriter({"population_size": 4},
                                  experiments_root=tr.experiments,
                                  repo_root=tr.repo)
        eid = writer.experiment_id
        sink = writer.sink
        with multiprocessing.Pool(4) as pool:
            pool.map(_worker_send_events, [(sink, w, 25) for w in range(4)])
        writer.append_event("generation", {"generation_index": 0})
        writer.finish(status="completed", best_ever_fitness=2.0)

        lines = (tr.experiments / "run_logs" / eid / "events.jsonl").read_text().splitlines()
        rows = [json.loads(l) for l in lines]  # every line parses: no interleaving
        assert len(rows) == 101
        evals = [r for r in rows if r["event"] == "genome_eval"]
        assert len(evals) == 100
        assert len({r["genome_id"] for r in evals}) == 100  # nothing lost
        index_row = json.loads((tr.experiments / "index.jsonl").read_text())
        assert index_row["status"] == "completed"
        assert index_row["best_ever_fitness"] == 2.0


if __name__ == "__main__":
    tests = [obj for name, obj in list(globals().items())
             if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print(f"\n{len(tests)}/{len(tests)} tests passed.")
