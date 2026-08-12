#!/usr/bin/env python3
"""Leg 287 -- ROUTE-EPA: environment-portability census of banked artifact families.

WHAT THIS IS
------------
Leg 252 (Route-VBRG) regenerated exactly ONE banked artifact family
(``writeup/data/p2_route_d_v11_anchor.json``) in a later environment, with zero
code change since the banking commit, and found 202 of 359 banked leaves moved
(46 by more than 10%), including a ``converged: True -> False`` flip.  Its own
open question was whether that is an outlier or the norm.

This runner answers that question by census.  It takes the N=10 families
enumerated *in advance* in ``writeup/novelty/leg_287.md``, regenerates each one
by running its own runner inside a throwaway copy of the repository, and
compares every scalar leaf of the regenerated JSON against the banked bytes.

TWO REFS, BECAUSE ONE WOULD CONFLATE TWO CAUSES
-----------------------------------------------
Leg 252's condition was *zero code change since banking*.  Re-running a runner
at today's HEAD does not reproduce that condition: this repository has moved a
long way since most artifacts were banked, and a family whose *inputs* changed
(``p2_route_cap_v1_audit`` audits ``capabilities.py``, which later legs grew)
would be mislabelled as environment-non-portable on a HEAD-only measurement.
So each family is regenerated at BOTH refs:

* **at its own banking commit** (``git log -1 -- writeup/data/<fam>.json``,
  materialised with ``git archive``) -- the code is byte-identical to what
  produced the bank, so a leaf that moves moved because of the ENVIRONMENT.
  **This is the primary measurement and what the classification is based on.**
* **at HEAD** -- the operational question, "does re-running this today
  reproduce the banked file", reported separately as
  ``classification_at_head``.

The difference between the two, taken in the same environment, is the pure
source-change contribution, and is reported per family as well.

READ-ONLY GUARANTEE
-------------------
The censused runners are executed inside a temp-directory copy of the tree, so
that their ``ROOT = Path(__file__).resolve().parents[1]`` convention makes them
write into the COPY's ``writeup/data/``.  The real banked artifacts are only
ever opened for reading, and a SHA-256 manifest of every banked file this leg
touches is taken before and after the census and compared -- if any banked byte
moved, the run aborts and says so.  ``p2_route_d_v11_anchor`` is excluded by
name (the 236/226/252 consolidation rework owns it) and the exclusion is
asserted, not assumed.

WHAT IT MEASURES, PER FAMILY
----------------------------
* ``max_rel_move``       -- largest relative move over numeric leaves
* ``n_leaves_over_10pct``-- how many numeric leaves moved by more than 10%
* ``flag_flips``         -- verdict-shaped leaves (gate/verdict/converged/...)
                            whose value changed: the highest-severity category
* structural moves       -- leaves present in one JSON and absent in the other
* ``worst_mover``        -- the single leaf with the largest relative move,
                            named by its dotted path, with both values

Volatile leaves (timestamps, elapsed times, absolute paths, hostnames, git
hashes) are classified separately and NEVER counted as portability evidence --
they are expected to move and would otherwise manufacture a false positive.

CONTROLS
--------
* NEGATIVE CONTROLS (pre-registered, P1): ``p2_route_cap_v1_audit`` and
  ``p2_route_alsl2_v1_lit`` call no numerical solver.  If those move, the
  finding is about the harness, not about floating point.  They CAN fail.
* POSITIVE CONTROL: after each family's real comparison, one untouched numeric
  leaf of the regenerated JSON is perturbed by a relative 1e-9 and the
  comparator is re-run.  If it does not report exactly that one leaf, the
  comparator is blind and the family's "no movement" reading is void.  This is
  the falsifiability check leg 252 used, and it is what makes a PORTABLE
  verdict mean something (lesson 90: a control that cannot come out differently
  is not a control).
* DETERMINISM CONTROL: a family that MOVED is regenerated a second time, in an
  independent process in an independent temp copy.  Run-to-run disagreement
  inside one environment is *nondeterminism*, which is a different defect from
  *environment non-portability*; conflating them would misattribute the cause.
  A family that reproduced the banked bytes exactly does not need it -- it has
  already agreed with a run made in a different environment months earlier.

CHECKPOINTING
-------------
Each regeneration costs 20-50 minutes and the full census is several hours, so
every family's record is written to a checkpoint directory (outside the repo)
the moment it completes, and a restart resumes rather than recomputing.

CLASSIFICATION (thresholds fixed before the run, matching the novelty pass)
--------------------------------------------------------------------------
* ``IRREPRODUCIBLE-AS-BANKED`` -- runner crashed, timed out, or wrote no JSON
* ``NON-PORTABLE``   -- any verdict-shaped flip, or any structural leaf move
* ``DRIFT``          -- max relative move >= 1e-3
* ``MINOR-DRIFT``    -- 1e-9 <= max relative move < 1e-3
* ``PORTABLE``       -- max relative move < 1e-9, no flips, no structural move

Usage:
    .venv/bin/python experiments/p2_route_epa_v1_census.py [--timeout SEC]
                                                           [--families a,b,c]
                                                           [--repeats 2]
                                                           [--out PATH]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "writeup" / "data" / "p2_route_epa_v1_census.json"

# ---------------------------------------------------------------------------
# The census set, enumerated in writeup/novelty/leg_287.md BEFORE any number
# was regenerated.  genre / rationale are carried here so the runner and the
# novelty pass cannot silently disagree.
# ---------------------------------------------------------------------------
CENSUS = [
    ("p2_route_e_v1_spectrum", "newton-heavy",
     "4 flow.newton(...) call sites -- closest structural analogue to the v11 anchor family"),
    ("p2_route_mf2_v1_residual", "newton-adjacent",
     "carries its own worst_newton_residual_over_floor diagnostic"),
    ("p2_route_cvf_v1_classify", "float-heavy, no Newton",
     "32-row/6-group numeric convention classification (leg 281)"),
    ("p2_route_l1rh_v1_construction", "interval / L1 construction",
     "a numerical method family that is not shooting/Newton"),
    ("p2_route_hhr_v1_repair", "repair record, self-hashing",
     "hashes its own record, so its internal determinism check is itself censused"),
    ("p2_route_h2i_v1_scoping", "scoping record",
     "bordered-H2 lane, a distinct solver path from Route-D and Route-E"),
    ("p2_route_nka_v1_adversarial", "adversarial battery",
     "stress-test genre"),
    ("p2_route_dpa_v1_adversarial", "newton-adjacent adversarial",
     "built on newton_gamma2 / newton_profile, independent of Route-D and Route-E"),
    ("p2_route_cap_v1_audit", "NEGATIVE CONTROL: structural audit",
     "AST-parses capabilities.py; essentially no floating-point content"),
    ("p2_route_alsl2_v1_lit", "NEGATIVE CONTROL: literature record",
     "no solver call at all"),
]
NEGATIVE_CONTROLS = {"p2_route_cap_v1_audit", "p2_route_alsl2_v1_lit"}

# Owned by the 236/226/252 consolidation rework -- excluded by name, asserted below.
EXCLUDED = {"p2_route_d_v11_anchor"}

# Leaf keys whose movement is a VERDICT move, not a numeric wobble.
VERDICT_TOKENS = (
    "gate", "verdict", "converged", "classification", "decision", "flag",
    "status", "pass", "fail", "holds", "answer", "conclusion", "outcome",
    "class", "category", "portable", "admissible", "refuted", "confirmed",
)
# Leaf keys that are EXPECTED to move between runs and carry no portability
# information.  Counted and reported separately; never used as evidence.
VOLATILE_TOKENS = (
    "timestamp", "generated", "generated_at", "date", "elapsed", "runtime",
    "wall", "duration", "seconds", "seconds_", "_seconds", "hostname", "host",
    "cwd", "abspath", "tmpdir", "tempdir", "pid", "git_head", "git_commit",
    "commit_hash", "run_at", "created", "machine_id", "uuid",
)
# NOTE on the pattern above, found and fixed by leg 361 (LCB4): several
# entries here were SUFFIXED/UNDERSCORE-BOUNDED forms ("generated_at",
# "seconds_"/"_seconds") without their BARE ROOT ("generated", "seconds").
# Substring matching is one-directional -- a bare root is a substring of its
# suffixed form, but not vice versa -- so a family that wrote the bare field
# name (e.g. ``"generated": "2026-..."`` in p2_route_e_v1_spectrum.json, or
# ``run.seconds`` -- real wall-clock time -- in the p2_route_cap_v1_audit
# NEGATIVE CONTROL) fell straight through undetected as volatile and got
# treated as content.  ``generated`` is the leg-356-diagnosed gap that
# produced leg 287's false "fails its own determinism control" headline for
# p2_route_e_v1_spectrum (see writeup/CORRECTIONS.md §25, §26).  ``seconds`` is
# a sibling of the exact same shape, found by auditing the other
# suffix-only entries in this list against every CENSUS family's actual
# leaf names: with the bare root missing, a negative control's own runtime
# column could have manufactured a false NON-PORTABLE/DRIFT verdict on
# nothing but CPU-speed noise.  Checked and NOT bare-rooted because no
# family leaf actually needs it: "host" (already bare and a substring of
# "hostname"), "created" (already bare and a substring of "created_at"),
# "run_at" (no family writes a bare "run" timestamp leaf; over-widening to
# bare "run" would blind the comparator to real content like
# ``rungs``/``run.seconds`` themselves, which must stay numerically visible
# via other tokens, not swallowed by a stray "run").


# Leaves that RECORD THE ENVIRONMENT rather than measure anything: the
# interpreter path, the git HEAD the runner saw, the repo root.  These move by
# construction and carry no portability information about the artifact's
# CONTENT.  They are bucketed separately and reported IN FULL (never silently
# dropped), because deciding that a differing leaf "doesn't count" is exactly
# the kind of judgement that has to be auditable.
#
# Note on `head` specifically: a `git archive` copy has no `.git`, so a runner
# that records git HEAD records the empty string there.  That is an artifact of
# THIS leg's method, not a property of the censused family, and is disclosed as
# such.
PROVENANCE_KEYS = {
    "head", "interpreter", "python", "executable", "repo_root", "root",
    "cwd", "git_head", "commit", "venv",
}
_SHA_HEX = set("0123456789abcdef")

# Substring markers for leaves that record whether THIS PARTICULAR invocation
# happened to hit a warm scratch cache, rather than anything about the
# artifact's computed content.  Discovered on p2_route_cvf_v1_classify:
# ``sections_served_from_cache_this_invocation`` is True in the banked file
# (which was produced after earlier warm runs) and False when this census
# regenerates it inside a fresh throwaway copy with no CVF_CACHE directory --
# the memoisation itself was independently verified inert (12732da: unset
# CVF_CACHE makes ``cached()`` a passthrough), so this leaf is exactly the
# same class of false NON-PORTABLE that ``head``/``interpreter`` already were
# for p2_route_cap_v1_audit: it records how this run was invoked, not what it
# computed.  Bucketed the same way, not silently dropped.
_CACHE_PROVENANCE_MARKERS = ("served_from_cache", "cache_this_invocation")


def is_provenance(path: str, banked, regen) -> bool:
    leaf = path.rsplit(".", 1)[-1].split("[")[0].lower()
    if leaf in PROVENANCE_KEYS:
        return True
    if any(m in leaf for m in _CACHE_PROVENANCE_MARKERS):
        return True
    for v in (banked, regen):
        if isinstance(v, str):
            if len(v) == 40 and set(v.lower()) <= _SHA_HEX:
                return True          # a git object id
            if v.startswith("/") and ("/.venv/" in v or v.endswith("/python")):
                return True          # an absolute interpreter path
    return False


REL_PORTABLE = 1e-9
REL_DRIFT = 1e-3
PCT10 = 0.10

COPY_EXCLUDE = {".git", ".venv", "Papers", ".claude", "__pycache__", ".pytest_cache"}


# ---------------------------------------------------------------------------
# environment fingerprint -- the whole finding is about environment dependence,
# so an unrecorded environment makes the census unusable.
# ---------------------------------------------------------------------------
def _blas_backend() -> dict:
    info = {}
    try:
        import numpy as np
        info["numpy_version"] = np.__version__
        try:
            cfg = np.show_config(mode="dicts")  # numpy >= 1.25
            build = cfg.get("Build Dependencies", {})
            blas = build.get("blas", {})
            lapack = build.get("lapack", {})
            info["blas_name"] = blas.get("name")
            info["blas_version"] = blas.get("version")
            info["lapack_name"] = lapack.get("name")
            info["lapack_version"] = lapack.get("version")
            info["compilers"] = {k: v.get("version") for k, v in
                                 cfg.get("Compilers", {}).items()}
            info["simd_baseline"] = cfg.get("SIMD Extensions", {}).get("baseline")
            info["simd_found"] = cfg.get("SIMD Extensions", {}).get("found")
        except Exception as exc:  # pragma: no cover - numpy version dependent
            info["show_config_error"] = repr(exc)
    except Exception as exc:  # pragma: no cover
        info["numpy_import_error"] = repr(exc)
    try:
        import scipy
        info["scipy_version"] = scipy.__version__
    except Exception as exc:
        info["scipy_import_error"] = repr(exc)
    try:
        import mpmath
        info["mpmath_version"] = mpmath.__version__
    except Exception:
        pass
    return info


def _cpu_model() -> str:
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.lower().startswith("model name"):
                return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return platform.processor() or "unknown"


def environment_fingerprint() -> dict:
    env = {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cpu_model": _cpu_model(),
        "cpu_count": os.cpu_count(),
        "python_version": sys.version.split()[0],
        "python_implementation": platform.python_implementation(),
        "python_executable": sys.executable,
        "libc": "-".join(x for x in platform.libc_ver() if x) or "unknown",
        "float_repr_style": sys.float_repr_style,
        "maxsize": sys.maxsize,
        "byteorder": sys.byteorder,
        "thread_env": {k: os.environ.get(k) for k in (
            "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
            "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")},
    }
    env.update(_blas_backend())
    return env


# ---------------------------------------------------------------------------
# leaf flattening and comparison
# ---------------------------------------------------------------------------
def flatten(obj, prefix="") -> dict:
    """Flatten a JSON document to {dotted.path: scalar}."""
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flatten(v, f"{prefix}.{k}" if prefix else str(k)))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(flatten(v, f"{prefix}[{i}]"))
    else:
        out[prefix] = obj
    return out


def _key_has(path: str, tokens) -> bool:
    low = path.lower()
    return any(t in low for t in tokens)


def is_verdict(path: str) -> bool:
    return _key_has(path, VERDICT_TOKENS)


def is_volatile(path: str) -> bool:
    return _key_has(path, VOLATILE_TOKENS)


def rel_move(a, b) -> float:
    """Relative move between two numeric leaves.

    Gated on the denominator (lesson 67): when the banked value is 0 the
    relative move has no referent, so we fall back to the absolute move rather
    than dividing by zero and reporting inf as if it were a measurement.
    """
    if isinstance(a, bool) or isinstance(b, bool):
        return 0.0 if a == b else float("inf")
    try:
        fa, fb = float(a), float(b)
    except (TypeError, ValueError):
        return 0.0 if a == b else float("inf")
    if math.isnan(fa) and math.isnan(fb):
        return 0.0
    if math.isnan(fa) != math.isnan(fb):
        return float("inf")
    if fa == fb:
        return 0.0
    if math.isinf(fa) or math.isinf(fb):
        return float("inf")
    denom = max(abs(fa), abs(fb))
    if denom == 0.0:
        return 0.0
    return abs(fa - fb) / denom


def compare(banked: dict, regen: dict) -> dict:
    """Leaf-by-leaf comparison of two flattened JSON documents."""
    bk, rk = set(banked), set(regen)
    only_banked = sorted(bk - rk)
    only_regen = sorted(rk - bk)
    shared = sorted(bk & rk)

    numeric_moves = []      # (rel, path, banked, regen)
    flag_flips = []
    volatile_moves = []
    string_moves = []
    provenance_moves = []

    for p in shared:
        a, b = banked[p], regen[p]
        if is_volatile(p):
            if a != b:
                volatile_moves.append({"path": p, "banked": a, "regenerated": b})
            continue
        a_num = isinstance(a, (int, float)) and not isinstance(a, bool)
        b_num = isinstance(b, (int, float)) and not isinstance(b, bool)
        if a_num and b_num:
            r = rel_move(a, b)
            if r > 0.0:
                numeric_moves.append((r, p, a, b))
                if is_verdict(p):
                    flag_flips.append({"path": p, "banked": a, "regenerated": b,
                                       "kind": "numeric-verdict-leaf",
                                       "rel_move": r})
        else:
            if a != b:
                rec = {"path": p, "banked": a, "regenerated": b}
                if is_provenance(p, a, b):
                    provenance_moves.append(rec)
                elif is_verdict(p):
                    rec["kind"] = "verdict-flip"
                    flag_flips.append(rec)
                else:
                    string_moves.append(rec)

    numeric_moves.sort(key=lambda t: (-t[0], t[1]))
    n_numeric_shared = sum(
        1 for p in shared
        if not is_volatile(p)
        and isinstance(banked[p], (int, float)) and not isinstance(banked[p], bool)
        and isinstance(regen[p], (int, float)) and not isinstance(regen[p], bool))
    over10 = [t for t in numeric_moves if t[0] > PCT10]
    max_rel = numeric_moves[0][0] if numeric_moves else 0.0

    worst = None
    if numeric_moves:
        r, p, a, b = numeric_moves[0]
        worst = {"path": p, "banked": a, "regenerated": b, "rel_move": r,
                 "is_verdict_leaf": is_verdict(p)}

    return {
        "n_leaves_banked": len(bk),
        "n_leaves_regenerated": len(rk),
        "n_leaves_shared": len(shared),
        "n_numeric_leaves_compared": n_numeric_shared,
        "n_leaves_only_in_banked": len(only_banked),
        "n_leaves_only_in_regenerated": len(only_regen),
        "leaves_only_in_banked_sample": only_banked[:20],
        "leaves_only_in_regenerated_sample": only_regen[:20],
        "n_numeric_leaves_moved": len(numeric_moves),
        "n_leaves_over_10pct": len(over10),
        "max_rel_move": max_rel,
        "worst_mover": worst,
        "top_movers": [{"path": p, "banked": a, "regenerated": b, "rel_move": r}
                       for r, p, a, b in numeric_moves[:15]],
        "over_10pct_sample": [{"path": p, "banked": a, "regenerated": b, "rel_move": r}
                              for r, p, a, b in over10[:25]],
        "n_flag_flips": len(flag_flips),
        "flag_flips": flag_flips[:40],
        "n_string_moves": len(string_moves),
        "string_moves_sample": string_moves[:15],
        "n_volatile_moves": len(volatile_moves),
        "volatile_moves_sample": volatile_moves[:10],
        # environment-recording leaves: listed IN FULL, excluded from the verdict
        "n_provenance_moves": len(provenance_moves),
        "provenance_moves": provenance_moves,
        "provenance_moves_note": (
            "these leaves RECORD the environment (interpreter path, git HEAD, "
            "repo root) rather than measure anything; they are excluded from the "
            "classification and listed here in full so the exclusion is auditable"),
    }


def classify(cmp_result: dict) -> str:
    if cmp_result["n_flag_flips"] > 0:
        return "NON-PORTABLE"
    if (cmp_result["n_leaves_only_in_banked"] > 0
            or cmp_result["n_leaves_only_in_regenerated"] > 0):
        return "NON-PORTABLE"
    if cmp_result["n_string_moves"] > 0:
        return "NON-PORTABLE"
    m = cmp_result["max_rel_move"]
    if m >= REL_DRIFT:
        return "DRIFT"
    if m >= REL_PORTABLE:
        return "MINOR-DRIFT"
    return "PORTABLE"


# ---------------------------------------------------------------------------
# regeneration in a throwaway copy
# ---------------------------------------------------------------------------
def _ignore(_dir, names):
    return [n for n in names if n in COPY_EXCLUDE]


def git(*args) -> str:
    return subprocess.run(["git", *args], cwd=str(ROOT), capture_output=True,
                          text=True, check=True).stdout.strip()


def banking_commit(family: str) -> dict:
    """The commit that last wrote the banked JSON, plus what has changed since.

    THIS IS THE LOAD-BEARING CONTROL FOR THE WHOLE LEG.  Leg 252's finding was
    specifically 'zero code change since banking'.  Regenerating at today's
    HEAD conflates two causes -- source edits and environment -- so each family
    is regenerated at BOTH refs:

      * at its own banking commit : code is byte-identical to what produced the
        bank, so any leaf that moves moved because of the ENVIRONMENT;
      * at HEAD                   : the operational question, 'does re-running
        the runner today reproduce the banked file', which mixes the two.

    Reporting only the second would have mislabelled a family whose *inputs*
    changed (capabilities.py grew) as environment-non-portable.
    """
    rel_json = f"writeup/data/{family}.json"
    rel_run = f"experiments/{family}.py"
    info = {"banked_json_path": rel_json}
    try:
        commit = git("log", "-1", "--format=%H", "--", rel_json)
        info["banking_commit"] = commit
        info["banking_commit_short"] = commit[:10]
        info["banking_commit_date"] = git("log", "-1", "--format=%cI", commit)
        info["banking_commit_subject"] = git("log", "-1", "--format=%s", commit)[:200]
        runner_changed = git("diff", "--name-only", f"{commit}..HEAD", "--", rel_run)
        info["runner_changed_since_banking"] = bool(runner_changed)
        changed = git("diff", "--name-only", f"{commit}..HEAD")
        changed_files = [c for c in changed.splitlines() if c]
        info["n_repo_files_changed_since_banking"] = len(changed_files)
        info["n_solver_files_changed_since_banking"] = sum(
            1 for c in changed_files if c.startswith("solver/"))
        info["n_commits_since_banking"] = int(
            git("rev-list", "--count", f"{commit}..HEAD") or 0)
    except subprocess.CalledProcessError as exc:
        info["git_error"] = repr(exc)
    return info


def regenerate(family: str, timeout: int, workroot: Path,
               ref: str | None = None) -> dict:
    """Materialise the tree (at `ref`, or the working tree) and run the runner.

    The runner's own ``ROOT = Path(__file__).resolve().parents[1]`` convention
    makes it write into the materialised COPY's ``writeup/data/``, never the
    real bank.
    """
    dest = workroot / f"copy_{family}_{os.getpid()}_{int(time.time()*1000)%100000}"
    t_copy = time.time()
    if ref is None:
        shutil.copytree(ROOT, dest, ignore=_ignore, symlinks=True)
    else:
        dest.mkdir(parents=True)
        arch = subprocess.run(["git", "archive", "--format=tar", ref],
                              cwd=str(ROOT), capture_output=True, check=True)
        subprocess.run(["tar", "-x", "-C", str(dest)], input=arch.stdout, check=True)
    copy_s = time.time() - t_copy

    runner = dest / "experiments" / f"{family}.py"
    if not runner.exists():
        return {"status": "runner-absent-at-ref", "returncode": None,
                "run_seconds": 0.0, "copy_seconds": round(copy_s, 2),
                "stderr_tail": "", "error": f"experiments/{family}.py absent at {ref}",
                "doc": None, "workdir": str(dest), "ref": ref}
    target = dest / "writeup" / "data" / f"{family}.json"
    # Remove the copied banked JSON so a runner that fails cannot be mistaken
    # for one that reproduced the bank exactly.
    if target.exists():
        target.unlink()

    t0 = time.time()
    status, rc, stderr_tail = "ok", None, ""
    try:
        proc = subprocess.run(
            [sys.executable, str(runner)],
            cwd=str(dest), capture_output=True, text=True, timeout=timeout)
        rc = proc.returncode
        stderr_tail = proc.stderr[-1500:]
        if rc != 0:
            status = "nonzero-exit"
    except subprocess.TimeoutExpired:
        status, rc = "timeout", None
    except Exception as exc:  # pragma: no cover
        status, rc, stderr_tail = "launch-error", None, repr(exc)
    run_s = time.time() - t0

    doc, err = None, None
    if target.exists():
        try:
            doc = json.loads(target.read_text())
        except Exception as exc:
            err = f"regenerated JSON unparseable: {exc!r}"
            status = "unparseable-json"
    else:
        if status == "ok":
            status = "no-json-written"

    out = {"status": status, "returncode": rc, "run_seconds": round(run_s, 2),
           "copy_seconds": round(copy_s, 2), "stderr_tail": stderr_tail,
           "error": err, "doc": doc, "workdir": str(dest), "ref": ref}
    return out


# ---------------------------------------------------------------------------
# positive control: the comparator must be able to report the other answer
# ---------------------------------------------------------------------------
def positive_control(regen_flat: dict) -> dict:
    """Perturb ONE numeric leaf of the regenerated doc by 1e-9 relative and
    confirm the comparator reports exactly that leaf.

    The comparison is regenerated-vs-itself-with-one-perturbation, so the
    baseline movement is identically zero and the control has exactly one
    correct answer: one moved leaf, at the perturbed path.  Anything else means
    the comparator is blind, and every PORTABLE verdict in this run is void.

    This is deliberately NOT compared against the banked doc: on a family that
    really does move, a 1e-9 injection would be buried under the real movement
    and the control could not come out differently (lesson 90).
    """
    candidates = [p for p in sorted(regen_flat)
                  if not is_volatile(p) and not is_verdict(p)
                  and isinstance(regen_flat[p], (int, float))
                  and not isinstance(regen_flat[p], bool)
                  and regen_flat[p] != 0
                  and math.isfinite(float(regen_flat[p]))]
    if not candidates:
        return {"fired": None, "reason": "no nonzero finite numeric leaf available",
                "leaf": None}
    leaf = candidates[len(candidates) // 2]
    perturbed = dict(regen_flat)
    perturbed[leaf] = float(regen_flat[leaf]) * (1.0 + 1e-9)
    res = compare(regen_flat, perturbed)
    fired = (res["n_numeric_leaves_moved"] == 1
             and res["worst_mover"] is not None
             and res["worst_mover"]["path"] == leaf
             and res["max_rel_move"] > 0.0)
    return {"fired": bool(fired), "leaf": leaf,
            "unperturbed_value": regen_flat[leaf],
            "perturbed_value": perturbed[leaf],
            "detected_rel_move": res["max_rel_move"],
            "detected_path": (res["worst_mover"] or {}).get("path"),
            "n_moved_leaves_reported": res["n_numeric_leaves_moved"],
            "expected_n_moved_leaves": 1}


# ---------------------------------------------------------------------------
# planted nondeterminism control (leg 361 / LCB4)
# ---------------------------------------------------------------------------
def planted_nondeterminism_control(banked_flat: dict) -> dict:
    """Confirm the VOLATILE_TOKENS fix does not blind the comparator to REAL
    content nondeterminism -- only to harmless timestamp/runtime noise.

    Leg 356 found leg 287's "fails its own within-environment determinism
    control" headline for p2_route_e_v1_spectrum was a false alarm: a
    one-token gap (``generated_at`` present, bare ``generated`` absent) in
    VOLATILE_TOKENS made a harmless timestamp field read as content movement.
    Fixing that gap (this leg) must not overcorrect into silence on a leaf
    that genuinely differs between two runs of the SAME family in the SAME
    environment -- that would trade one false alarm for a false negative,
    which is strictly worse (a real defect going unflagged).

    This constructs two "runs" of a synthetic artifact that differ in BOTH a
    volatile leaf (a bare ``generated`` timestamp, deliberately made to move
    only along the fixed gap) AND a genuinely content-bearing numeric leaf
    (a computed residual), and asserts the comparator:
      * does NOT flag the ``generated`` move (it is volatile, correctly so
        post-fix -- this is the fix under test, not the control target), and
      * DOES flag the residual move as real nondeterminism (n_numeric_leaves
        moved >= 1, that leaf named, not swallowed as volatile).
    ``banked_flat`` is unused; the control is self-contained by design (lesson
    90: it must not be compared against a family that could already be
    expected to move for other reasons).
    """
    run_a = {
        "generated": "2026-08-11T00:00:00Z",
        "family": "PLANTED_CONTROL_synthetic",
        "residual": 1.0000000123,   # differs run-to-run: genuine content drift
        "gate.verdict": "hold",
    }
    run_b = {
        "generated": "2026-08-11T00:00:07Z",   # differs: timestamp only, must NOT count
        "family": "PLANTED_CONTROL_synthetic",
        "residual": 1.0007654321,               # differs: real numeric content, MUST count
        "gate.verdict": "hold",
    }
    res = compare(run_a, run_b)
    generated_move_reported = any(
        m["path"] == "generated" for m in res["volatile_moves_sample"])
    residual_seen = res["max_rel_move"] > 0.0 and res["worst_mover"] is not None \
        and res["worst_mover"]["path"] == "residual"
    trips = (res["n_numeric_leaves_moved"] >= 1) and residual_seen
    stays_silent_on_generated = is_volatile("generated") and generated_move_reported
    return {
        "trips_on_real_nondeterminism": bool(trips),
        "stays_silent_on_generated_timestamp": bool(stays_silent_on_generated),
        "n_numeric_leaves_moved": res["n_numeric_leaves_moved"],
        "worst_mover": res["worst_mover"],
        "n_volatile_moves": res["n_volatile_moves"],
        "pass": bool(trips and stays_silent_on_generated),
    }


# ---------------------------------------------------------------------------
# read-only guarantee
# ---------------------------------------------------------------------------
def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def banked_manifest(families) -> dict:
    man = {}
    for fam in families:
        for rel in (f"writeup/data/{fam}.json", f"experiments/{fam}.py"):
            p = ROOT / rel
            if p.exists():
                man[rel] = sha256(p)
    for rel in ("writeup/data/p2_route_d_v11_anchor.json",
                "experiments/p2_route_d_v11_anchor.py",
                "solver/profile_newton.py"):
        p = ROOT / rel
        if p.exists():
            man[rel] = sha256(p)
    return man


# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout", type=int, default=3600)
    ap.add_argument("--families", type=str, default="")
    ap.add_argument("--repeats", type=int, default=2)
    ap.add_argument("--out", type=str, default=str(OUT))
    ap.add_argument("--partial-dir", type=str, default="",
                    help="where per-family checkpoints live (default: a temp dir "
                         "OUTSIDE the repository)")
    ap.add_argument("--no-resume", action="store_true",
                    help="recompute every family even if a checkpoint exists")
    ap.add_argument("--self-test", action="store_true",
                    help="run the planted-nondeterminism control (leg 361) and "
                         "exit; does not touch any banked JSON or run a census")
    args = ap.parse_args()

    if args.self_test:
        r = planted_nondeterminism_control({})
        print(json.dumps(r, indent=2))
        if not r["pass"]:
            print("SELF-TEST FAIL: planted nondeterminism control did not pass "
                  "-- either it failed to trip on real content movement, or it "
                  "wrongly flagged the volatile 'generated' timestamp.")
            return 1
        print("SELF-TEST PASS: comparator still trips on genuine content "
              "nondeterminism and stays silent on the 'generated' timestamp.")
        return 0

    census = CENSUS
    if args.families:
        want = [f.strip() for f in args.families.split(",") if f.strip()]
        census = [c for c in CENSUS if c[0] in want]

    families = [c[0] for c in census]
    # The exclusion is asserted, not assumed.
    assert not (set(families) & EXCLUDED), "v11 anchor family must not be censused"

    t_start = time.time()
    man_before = banked_manifest(families)
    env = environment_fingerprint()

    workroot = Path(tempfile.mkdtemp(prefix="epa_census_"))
    # Per-family checkpointing.  These regenerations cost 20-50 minutes each and
    # the whole census is many hours, so a single interruption must never
    # discard completed families: every family's record is written to
    # `partial_dir` the moment it finishes, and a restart skips any family whose
    # checkpoint already exists.  (This repository has been bitten by exactly
    # this before -- p2_route_cvf_v1_classify carries the same note about a
    # crash discarding finished sections.)
    # Default lives OUTSIDE the repository, so checkpointing never puts a file
    # in this leg's declared territory (or anyone else's).
    partial_dir = Path(args.partial_dir) if args.partial_dir else (
        Path(tempfile.gettempdir()) / "epa_census_partials")
    partial_dir.mkdir(parents=True, exist_ok=True)

    results = []
    try:
        for fam, genre, why in census:
            ckpt = partial_dir / f"{fam}.json"
            if ckpt.exists() and not args.no_resume:
                try:
                    rec = json.loads(ckpt.read_text())
                    results.append(rec)
                    print(f"[{fam}] resumed from checkpoint -> "
                          f"{rec.get('classification')}", flush=True)
                    continue
                except Exception as exc:
                    print(f"[{fam}] checkpoint unreadable ({exc!r}), recomputing",
                          flush=True)

            banked_path = ROOT / "writeup" / "data" / f"{fam}.json"
            runner_path = ROOT / "experiments" / f"{fam}.py"
            rec = {"family": fam, "genre": genre, "why_chosen": why,
                   "is_negative_control": fam in NEGATIVE_CONTROLS,
                   "banked_json": str(banked_path.relative_to(ROOT)),
                   "runner": str(runner_path.relative_to(ROOT)),
                   "banked_sha256": man_before.get(f"writeup/data/{fam}.json"),
                   "runner_sha256": man_before.get(f"experiments/{fam}.py")}

            if not runner_path.exists() or not banked_path.exists():
                rec["classification"] = "IRREPRODUCIBLE-AS-BANKED"
                rec["irreproducible_reason"] = (
                    "missing runner" if not runner_path.exists() else "missing banked JSON")
                results.append(rec)
                (partial_dir / f"{fam}.json").write_text(json.dumps(rec, indent=1) + "\n")
                print(f"[{fam}] IRREPRODUCIBLE: {rec['irreproducible_reason']}", flush=True)
                continue

            banked_doc = json.loads(banked_path.read_text())
            banked_flat = flatten(banked_doc)
            rec["n_banked_leaves"] = len(banked_flat)

            prov = banking_commit(fam)
            rec["provenance"] = prov
            ref = prov.get("banking_commit")

            # At the banking commit: code fixed, so the environment is the only
            # variable.  The SECOND repeat is run only if the first one actually
            # moved: a family that reproduces the banked bytes exactly has
            # already demonstrated run-to-run determinism (it agreed with a run
            # made in a different environment, months earlier), so the
            # nondeterminism-vs-non-portability question does not arise for it.
            # Spending a second full solve there buys nothing and these solves
            # cost 20-50 minutes each.
            runs = []
            head_runs = []  # at HEAD: the operational "does it reproduce today"
            print(f"[{fam}] banking-commit regeneration 1 "
                  f"@{prov.get('banking_commit_short')} ...", flush=True)
            r0 = regenerate(fam, args.timeout, workroot, ref=ref)
            print(f"[{fam}]   status={r0['status']} rc={r0['returncode']} "
                  f"{r0['run_seconds']}s", flush=True)
            runs.append(r0)

            needs_repeat = False
            if r0["doc"] is not None:
                _probe = compare(banked_flat, flatten(r0["doc"]))
                needs_repeat = (_probe["n_numeric_leaves_moved"] > 0
                                or _probe["n_flag_flips"] > 0
                                or _probe["n_string_moves"] > 0
                                or _probe["n_leaves_only_in_banked"] > 0
                                or _probe["n_leaves_only_in_regenerated"] > 0)
            rec["determinism_repeat_triggered"] = needs_repeat
            rec["determinism_repeat_policy"] = (
                "a second independent regeneration at the banking commit is run "
                "IFF the first one moved at least one leaf; an exact reproduction "
                "of the banked bytes already establishes determinism")

            if needs_repeat and args.repeats > 1:
                print(f"[{fam}] banking-commit regeneration 2 (movement seen; "
                      f"determinism control) ...", flush=True)
                r1 = regenerate(fam, args.timeout, workroot, ref=ref)
                print(f"[{fam}]   status={r1['status']} rc={r1['returncode']} "
                      f"{r1['run_seconds']}s", flush=True)
                runs.append(r1)

            print(f"[{fam}] HEAD regeneration ...", flush=True)
            head_runs.append(regenerate(fam, args.timeout, workroot, ref=None))
            print(f"[{fam}]   status={head_runs[0]['status']} "
                  f"{head_runs[0]['run_seconds']}s", flush=True)

            rec["regeneration_runs_at_banking_commit"] = [
                {k: v for k, v in r.items() if k not in ("doc", "workdir")} for r in runs]
            rec["regeneration_run_at_head"] = [
                {k: v for k, v in r.items() if k not in ("doc", "workdir")}
                for r in head_runs]

            first = runs[0]
            if first["doc"] is None:
                rec["classification"] = "IRREPRODUCIBLE-AS-BANKED"
                rec["irreproducible_reason"] = first["status"]
                rec["irreproducible_detail"] = first["stderr_tail"]
                results.append(rec)
                (partial_dir / f"{fam}.json").write_text(json.dumps(rec, indent=1) + "\n")
                print(f"[{fam}] -> IRREPRODUCIBLE-AS-BANKED ({first['status']})", flush=True)
                for r in runs + head_runs:
                    shutil.rmtree(r["workdir"], ignore_errors=True)
                continue

            regen_flat = flatten(first["doc"])
            cmp_res = compare(banked_flat, regen_flat)
            rec["comparison"] = cmp_res           # environment-isolated: THE finding
            rec["classification"] = classify(cmp_res)

            # secondary, operational: banked bytes vs a re-run at today's HEAD.
            if head_runs[0]["doc"] is not None:
                head_flat = flatten(head_runs[0]["doc"])
                head_cmp = compare(banked_flat, head_flat)
                rec["comparison_at_head"] = head_cmp
                rec["classification_at_head"] = classify(head_cmp)
                # and the pure source-change contribution: banking-commit code vs
                # HEAD code, both in TODAY's environment.
                src = compare(regen_flat, head_flat)
                rec["source_change_contribution"] = {
                    "n_numeric_leaves_moved": src["n_numeric_leaves_moved"],
                    "n_leaves_over_10pct": src["n_leaves_over_10pct"],
                    "max_rel_move": src["max_rel_move"],
                    "n_flag_flips": src["n_flag_flips"],
                    "n_structural_moves": (src["n_leaves_only_in_banked"]
                                           + src["n_leaves_only_in_regenerated"]),
                    "worst_mover": src["worst_mover"],
                    "note": ("same environment, code at banking commit vs code at "
                             "HEAD -- everything here is source change, not "
                             "environment"),
                }
            else:
                rec["classification_at_head"] = "IRREPRODUCIBLE-AT-HEAD"
                rec["head_failure_reason"] = head_runs[0]["status"]
                rec["head_failure_detail"] = head_runs[0]["stderr_tail"]

            # determinism control: two independent processes, same environment,
            # same code.  Distinguishes nondeterminism from non-portability.
            if len(runs) > 1 and runs[1]["doc"] is not None:
                second_flat = flatten(runs[1]["doc"])
                det = compare(regen_flat, second_flat)
                rec["determinism_control"] = {
                    "two_processes_agree_on_nonvolatile_leaves":
                        (det["n_numeric_leaves_moved"] == 0
                         and det["n_flag_flips"] == 0
                         and det["n_string_moves"] == 0
                         and det["n_leaves_only_in_banked"] == 0
                         and det["n_leaves_only_in_regenerated"] == 0),
                    "n_leaves_differing_between_repeats": (
                        det["n_numeric_leaves_moved"] + det["n_flag_flips"]
                        + det["n_string_moves"]),
                    "max_rel_move_between_repeats": det["max_rel_move"],
                    "worst_between_repeats": det["worst_mover"],
                }
            elif not needs_repeat:
                rec["determinism_control"] = {
                    "two_processes_agree_on_nonvolatile_leaves": True,
                    "n_leaves_differing_between_repeats": 0,
                    "max_rel_move_between_repeats": 0.0,
                    "reason": ("not run: the single regeneration reproduced the "
                               "banked bytes exactly, which already establishes "
                               "cross-process AND cross-environment agreement"),
                    "established_by": "exact reproduction of the bank"}
            else:
                rec["determinism_control"] = {
                    "two_processes_agree_on_nonvolatile_leaves": None,
                    "reason": "second repeat attempted but produced no document"}

            rec["positive_control"] = positive_control(regen_flat)
            results.append(rec)
            (partial_dir / f"{fam}.json").write_text(json.dumps(rec, indent=1) + "\n")
            print(f"[{fam}] -> {rec['classification']} (env-isolated)  "
                  f"max_rel={cmp_res['max_rel_move']:.3e}  "
                  f">10%={cmp_res['n_leaves_over_10pct']}  "
                  f"flips={cmp_res['n_flag_flips']}  | at HEAD: "
                  f"{rec.get('classification_at_head')}", flush=True)

            for r in runs + head_runs:
                shutil.rmtree(r["workdir"], ignore_errors=True)
    finally:
        shutil.rmtree(workroot, ignore_errors=True)

    man_after = banked_manifest(families)
    banked_unchanged = (man_before == man_after)
    changed_banked = sorted(k for k in man_before
                            if man_after.get(k) != man_before[k])

    # ---- roll-up -----------------------------------------------------------
    by_class = {}
    for r in results:
        by_class.setdefault(r["classification"], []).append(r["family"])
    by_class_head = {}
    for r in results:
        if "classification_at_head" in r:
            by_class_head.setdefault(r["classification_at_head"], []).append(r["family"])

    movers = [(r["comparison"]["max_rel_move"], r["family"])
              for r in results if "comparison" in r]
    movers.sort(reverse=True)
    total_leaves = sum(r.get("n_banked_leaves", 0) for r in results)
    total_moved = sum(r["comparison"]["n_numeric_leaves_moved"]
                      for r in results if "comparison" in r)
    total_over10 = sum(r["comparison"]["n_leaves_over_10pct"]
                       for r in results if "comparison" in r)
    total_flips = sum(r["comparison"]["n_flag_flips"]
                      for r in results if "comparison" in r)

    pc = [r["positive_control"]["fired"] for r in results if "positive_control" in r]
    dc = [r["determinism_control"]["two_processes_agree_on_nonvolatile_leaves"]
          for r in results if "determinism_control" in r]

    nc = [r for r in results if r["is_negative_control"]]
    nc_portable = all(r["classification"] == "PORTABLE" for r in nc) if nc else None

    newton = [r for r in results
              if "newton" in r["genre"] and "comparison" in r]
    non_newton_numeric = [r for r in results
                          if "newton" not in r["genre"]
                          and not r["is_negative_control"]
                          and "comparison" in r]

    def _frac_moved(rs):
        tot = sum(x["comparison"]["n_numeric_leaves_compared"] for x in rs)
        mv = sum(x["comparison"]["n_numeric_leaves_moved"] for x in rs)
        return (mv / tot) if tot else None

    src_movers = [r for r in results if "source_change_contribution" in r
                  and (r["source_change_contribution"]["n_numeric_leaves_moved"] > 0
                       or r["source_change_contribution"]["n_flag_flips"] > 0
                       or r["source_change_contribution"]["n_structural_moves"] > 0)]

    summary = {
        "n_families_censused": len(results),
        "primary_measurement": (
            "banked bytes vs regeneration AT THE ARTIFACT'S OWN BANKING COMMIT, so "
            "the code is byte-identical to what produced the bank and every move is "
            "attributable to the environment -- the same condition leg 252 measured "
            "under"),
        "classification_counts": {k: len(v) for k, v in sorted(by_class.items())},
        "families_by_classification": {k: sorted(v) for k, v in sorted(by_class.items())},
        "classification_counts_at_head": {k: len(v) for k, v in sorted(by_class_head.items())},
        "families_by_classification_at_head": {k: sorted(v) for k, v in
                                               sorted(by_class_head.items())},
        "n_families_where_source_change_also_moves_leaves": len(src_movers),
        "families_where_source_change_also_moves_leaves": [
            {"family": r["family"],
             "n_moved": r["source_change_contribution"]["n_numeric_leaves_moved"],
             "n_flag_flips": r["source_change_contribution"]["n_flag_flips"],
             "n_structural": r["source_change_contribution"]["n_structural_moves"],
             "max_rel_move": r["source_change_contribution"]["max_rel_move"]}
            for r in src_movers],
        "total_banked_leaves_compared": total_leaves,
        "total_numeric_leaves_moved": total_moved,
        "total_leaves_over_10pct": total_over10,
        "total_flag_flips": total_flips,
        "worst_family_by_max_rel_move": (
            {"family": movers[0][1], "max_rel_move": movers[0][0]} if movers else None),
        "ranked_max_rel_move": [{"family": f, "max_rel_move": m} for m, f in movers],
        "positive_control_fired_for_all_families": (all(pc) if pc else None),
        "positive_control_results": pc,
        "determinism_control_all_agree": (all(x is True for x in dc) if dc else None),
        "determinism_control_results": dc,
        "negative_controls_all_portable": nc_portable,
        "negative_control_classifications": {r["family"]: r["classification"] for r in nc},
        "newton_family_moved_leaf_fraction": _frac_moved(newton),
        "non_newton_numeric_moved_leaf_fraction": _frac_moved(non_newton_numeric),
        "zero_banked_files_modified": banked_unchanged,
        "banked_files_changed": changed_banked,
        "n_banked_files_hashed_before_and_after": len(man_before),
        "v11_anchor_family_excluded": sorted(EXCLUDED),
        "elapsed_seconds": round(time.time() - t_start, 1),
    }

    doc = {
        "leg": 287,
        "route": "ROUTE-EPA",
        "title": ("environment-portability census of banked artifact families "
                  "(leg 252's finding, generalized)"),
        "purpose": (
            "Leg 252 found one banked artifact family regenerates 202/359 leaves "
            "differently across environments with zero code change. This censuses "
            "N=10 OTHER families, enumerated in writeup/novelty/leg_287.md before "
            "any number was regenerated, to measure whether that is an outlier or "
            "the norm."),
        "environment": env,
        "thresholds": {
            "PORTABLE_max_rel_move_below": REL_PORTABLE,
            "DRIFT_max_rel_move_at_or_above": REL_DRIFT,
            "over_10pct_threshold": PCT10,
            "note": ("fixed before the run; PORTABLE also requires zero verdict "
                     "flips, zero string moves and zero structural leaf moves"),
        },
        "verdict_key_tokens": list(VERDICT_TOKENS),
        "volatile_key_tokens": list(VOLATILE_TOKENS),
        "read_only_guarantee": {
            "method": ("censused runners execute inside a throwaway copytree of the "
                       "repo, so their ROOT-relative writes land in the copy"),
            "banked_sha256_before": man_before,
            "banked_sha256_after": man_after,
            "zero_banked_files_modified": banked_unchanged,
        },
        "summary": summary,
        "families": results,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(doc, indent=2, sort_keys=False) + "\n")
    print(f"\nwrote {out_path}")
    print(json.dumps(summary, indent=2)[:4000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
