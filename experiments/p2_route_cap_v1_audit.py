"""Route-CAP v1 (leg 71) -- the self-audit of `capabilities.py` against the test suite.

WHY
---
`capabilities.py` is the repository's single ledger of what each solver module holds and
how it was validated.  `DIRECTION.md`, `PHASE2_P2_NOTES.md` and every leg in the queue
read its `test` and `validated` fields as ground truth, and `plan_of_record.py` carries a
standing ban on "building a solver without grepping capabilities.py for the object first".

The existing drift detector, `test_capabilities.py`, checks that each cited test file
EXISTS.  It does not check that the file RUNS, that it PASSES, or that it has anything to
do with the module whose row cites it.  This script closes that gap.

Banked lesson 68 -- a check that is not executable decays at the rate of memory -- applied
to the index's own `test` field.

INVOCATION CONVENTION
---------------------
The chartered gate says "collected by pytest".  This repository has no pytest (and no
scipy); `scripts/merge_gate.sh` states the real convention:

    every test_*.py is a self-running script (`.venv/bin/python test_x.py`, no pytest).
    A solver/<name>.py change maps to test_<name>.py at the repo root when that file
    exists.

So "is collected" is audited in the only form meaningful here:
  * the file parses (compile()), and
  * it has a runnable entry point (an `if __name__ == "__main__":` block) or at least one
    top-level `test_*` function, and
  * running it under `.venv/bin/python` exits 0.

WHAT IT REPORTS  (categories pre-registered in writeup/novelty/leg_71.md)
------------------------------------------------------------------------
  S1 missing        the cited path is not on disk
  S2 uncollected    exists but does not parse / has no runnable entry point / errors on import
  S3 red            runs and FAILS at HEAD -- priority bug report, never a silent fix
  S4 drift          green, but the cited test does not reference the row's module, or the
                    module is unreachable from `scripts/merge_gate.sh`'s name mapping
                    (a solver/<name>.py edit runs NO test) -- green but ungated

Run:  .venv/bin/python experiments/p2_route_cap_v1_audit.py [--cache PATH]
Out:  writeup/data/p2_route_cap_v1_audit.json

RESUMABILITY.  The full sweep is expensive -- several of these tests are multi-minute
numerics (`test_advection_scope.py` and `test_critical_dissipation.py` are each ~30 min),
and the whole sweep runs to about an hour of wall time.  Each test's result is therefore
appended to a JSONL cache and flushed the moment it finishes, so an interrupted run
resumes instead of starting over.  Delete the cache to force a clean re-run.
"""

import ast
import json
import re
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities import CAPABILITIES  # noqa: E402

PY = ROOT / ".venv" / "bin" / "python"
if not PY.exists():
    PY = Path(sys.executable)

TIMEOUT_S = 3600
SERIAL_TIMEOUT_S = 7200   # budget for the alone/unloaded re-timing of a slow test
WORKERS = 6

# Results are appended here as each test finishes, so an interrupted sweep resumes.
# Kept OUTSIDE the repository: it is scratch, not evidence.
DEFAULT_CACHE = Path(tempfile.gettempdir()) / "cap_audit_cache_leg71.jsonl"
_cache_lock = threading.Lock()

# Modules claimed by a live leg this cycle (DIRECTION.md live-assignments table).  A stale
# row for one of these is REPORTED, not corrected, to avoid colliding with that leg's own
# in-flight test changes.
LIVE_CLAIMED = {
    "solver/spectral_certificate.py": "leg 58 (NG)",
    "solver/certificate_shapes.py": "leg 62 (CP)",
    "solver/literature_gates.py": "leg 62 (CP)",
    "solver/target_selection.py": "leg 63 (M2)",
    "solver/weight_search.py": "leg 59 (WV)",
    "solver/interval_certificate.py": "leg 61 (KA)",
    "solver/interval.py": "leg 69 (IA), read-only",
    "solver/holder_norms.py": "leg 65 (L1G), landed",
}


# ----------------------------------------------------------------------------- collect
def collect(test_path):
    """Static 'collection': does it parse, and in which of this repo's THREE styles?

    An earlier version of this script demanded an `if __name__ == "__main__":` block or a
    top-level `test_*` function, and flagged test_spectral_certificate.py and
    test_target_norm.py as uncollected.  That was a DEFECT IN THIS INSTRUMENT, not a
    finding: both are straight-line module-level gate scripts that do their work at import
    and end in `sys.exit(1 if n_fail else 0)`, and both run for real (28 and 25 lines of
    gate output, 875s and 0.9s).  Recorded here rather than quietly deleted, because a
    self-audit that silently repairs its own false positives is not auditable.

    So static collectability is now just: does it PARSE.  The genuine no-op case -- a file
    that "passes" because it does nothing -- is caught at RUNTIME instead (exit 0 with no
    output at all), which is the only way to tell a real straight-line script from an
    empty one.

    Returns (ok, detail, n_test_funcs, has_main).
    """
    try:
        src = test_path.read_text()
    except OSError as exc:
        return False, f"unreadable: {exc}", 0, False
    try:
        tree = ast.parse(src, filename=str(test_path))
    except SyntaxError as exc:
        return False, f"SyntaxError line {exc.lineno}: {exc.msg}", 0, False

    n_funcs = sum(1 for n in tree.body
                  if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                  and n.name.startswith("test"))
    has_main = any(
        isinstance(n, ast.If)
        and "__name__" in ast.dump(n.test)
        and "__main__" in ast.dump(n.test)
        for n in tree.body
    )
    if has_main:
        style = "`__main__` block"
    elif n_funcs:
        style = f"{n_funcs} top-level test_* function(s)"
    else:
        style = "straight-line module-level gates"
    return True, f"parses; style: {style}", n_funcs, has_main


def references(test_path, module_path):
    """Does the test actually mention the module it is cited for?

    Coverage proxy: the module's basename appearing in an import or anywhere in the
    source.  Deliberately generous -- a hit is NOT proof of coverage, but a MISS is hard
    evidence that the row's test does not exercise the row's module directly.
    """
    stem = Path(module_path).stem
    try:
        src = test_path.read_text()
    except OSError:
        return False, False
    imported = bool(re.search(rf"\b(from|import)\s+solver[.\s].*\b{re.escape(stem)}\b", src)
                    or re.search(rf"from\s+solver\.{re.escape(stem)}\b", src)
                    or re.search(rf"import\s+solver\.{re.escape(stem)}\b", src))
    mentioned = bool(re.search(rf"\b{re.escape(stem)}\b", src))
    return imported, mentioned


def load_cache(cache_path):
    """Previously completed test results, keyed by test name."""
    done = {}
    if cache_path.exists():
        for line in cache_path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue  # a torn final line from a killed run
            done[rec["test"]] = rec
    return done


def append_cache(cache_path, rec):
    """Append one result and flush it immediately -- the point of the cache."""
    with _cache_lock:
        with cache_path.open("a") as fh:
            fh.write(json.dumps(rec) + "\n")
            fh.flush()


def run_test(test_name, timeout_s=TIMEOUT_S):
    """Run one test the way scripts/merge_gate.sh runs it. Returns a record."""
    t0 = time.time()
    try:
        p = subprocess.run([str(PY), test_name], cwd=str(ROOT),
                           capture_output=True, text=True, timeout=timeout_s)
        rc, out, err = p.returncode, p.stdout, p.stderr
        timed_out = False
    except subprocess.TimeoutExpired:
        rc, out, err, timed_out = -1, "", f"TIMEOUT after {timeout_s}s", True
    dt = time.time() - t0
    # These tests report failure on STDOUT as often as on stderr (a printed FAIL line
    # plus sys.exit(1)), so both tails are kept -- a stderr-only record loses the reason.
    return {"test": test_name, "returncode": rc, "seconds": round(dt, 2),
            "timed_out": timed_out, "stdout_lines": len(out.splitlines()),
            "stderr_tail": (err.strip().splitlines() or [""])[-8:],
            "stdout_tail": (out.strip().splitlines() or [""])[-15:]}


# -------------------------------------------------------------------------------- main
def main():
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(ROOT),
                          capture_output=True, text=True).stdout.strip()

    rows = []
    for c in CAPABILITIES:
        mod_p = ROOT / c["module"]
        test_p = ROOT / c["test"]
        ok, detail, n_funcs, has_main = collect(test_p) if test_p.exists() else (
            False, "file does not exist", 0, False)
        imported, mentioned = references(test_p, c["module"]) if test_p.exists() else (False, False)
        conventional = ROOT / f"test_{Path(c['module']).stem}.py"
        rows.append({
            "module": c["module"],
            "module_exists": mod_p.exists(),
            "cited_test": c["test"],
            "test_exists": test_p.exists(),
            "collectable": ok,
            "collect_detail": detail,
            "n_test_functions": n_funcs,
            "has_main_block": has_main,
            "test_imports_module": imported,
            "test_mentions_module": mentioned,
            "merge_gate_name": f"test_{Path(c['module']).stem}.py",
            "merge_gate_name_exists": conventional.exists(),
            "live_claimed_by": LIVE_CLAIMED.get(c["module"]),
        })

    # Run each distinct cited test once, in parallel, resuming from cache.
    cache_path = DEFAULT_CACHE
    if "--cache" in sys.argv:
        cache_path = Path(sys.argv[sys.argv.index("--cache") + 1])
    cached = load_cache(cache_path)

    distinct = sorted({r["cited_test"] for r in rows if r["test_exists"]})
    todo = [t for t in distinct if t not in cached]
    print(f"{len(distinct)} distinct cited tests; {len(cached)} already in cache "
          f"{cache_path}; running {len(todo)} under {PY} "
          f"({WORKERS} workers, {TIMEOUT_S}s timeout each)", flush=True)

    def run_and_cache(test_name):
        rec = run_test(test_name)
        append_cache(cache_path, rec)
        mark = "PASS" if rec["returncode"] == 0 else f"FAIL rc={rec['returncode']}"
        print(f"  {mark:12s} {rec['seconds']:8.2f}s  {test_name}", flush=True)
        return rec

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        fresh = list(ex.map(run_and_cache, todo))

    by_test = dict(cached)
    by_test.update({r["test"]: r for r in fresh})

    # Any test that TIMED OUT is re-run ALONE, one at a time, with a longer budget.  Six
    # multi-minute numerics sharing a box is a contention artifact, not a red test, and
    # calling it red would be exactly the kind of false alarm this leg exists to prevent.
    serial_cache = cache_path.with_suffix(".serial.jsonl")
    serial_done = load_cache(serial_cache)
    slow = sorted(t for t, r in by_test.items() if r.get("timed_out"))
    if slow:
        print(f"\nre-timing {len(slow)} timed-out test(s) ALONE, serially: {slow}",
              flush=True)
    for t in slow:
        if t in serial_done:
            continue
        rec = run_test(t, timeout_s=SERIAL_TIMEOUT_S)
        rec["serial"] = True
        append_cache(serial_cache, rec)
        serial_done[t] = rec
        mark = "PASS" if rec["returncode"] == 0 else f"FAIL rc={rec['returncode']}"
        print(f"  SERIAL {mark:12s} {rec['seconds']:8.2f}s  {t}", flush=True)

    results = [by_test[t] for t in distinct]
    for r in results:
        mark = "PASS" if r["returncode"] == 0 else f"FAIL rc={r['returncode']}"
        print(f"  {mark:12s} {r['seconds']:8.2f}s  {r['test']}")

    # Classify.
    for r in rows:
        run = by_test.get(r["cited_test"])
        r["run"] = run
        srun = serial_done.get(r["cited_test"])
        r["serial_run"] = srun
        r["serial_pass"] = bool(srun and srun["returncode"] == 0)
        # The unloaded serial re-run is authoritative when the parallel sweep timed out.
        if run and run.get("timed_out") and srun:
            r["passes"] = srun["returncode"] == 0
        else:
            r["passes"] = bool(run and run["returncode"] == 0)
        flags = []
        if not r["test_exists"]:
            flags.append("S1_missing")
        elif not r["collectable"]:
            flags.append("S2_uncollected")
        elif run and run.get("timed_out") and not r["serial_pass"]:
            # A timeout is NOT by itself evidence of a red test: this sweep runs 6 tests at
            # once and these are multi-minute numerics. Timeouts are re-timed ALONE and
            # only called red if they still fail or time out unloaded.
            flags.append("S3_red" if (r["serial_run"] and not r["serial_run"]["timed_out"])
                         else "S3_timeout_unresolved")
        elif not r["passes"]:
            flags.append("S3_red")
        # A test that exits 0 having printed nothing at all is a no-op, not a pass.
        if run and run["returncode"] == 0 and run["stdout_lines"] == 0 \
                and not r["has_main_block"] and r["n_test_functions"] == 0:
            flags.append("S2_runtime_noop")
        if r["test_exists"] and r["passes"]:
            if not r["test_mentions_module"]:
                flags.append("S4_no_coverage")
            if not r["merge_gate_name_exists"]:
                flags.append("S4_ungated_by_merge_gate")
        if not r["module_exists"]:
            flags.append("S1_module_missing")
        r["flags"] = flags

    def n(flag):
        return [r["module"] for r in rows if flag in r["flags"]]

    summary = {
        "rows_total": len(rows),
        "distinct_tests_run": len(distinct),
        "rows_clean": sum(1 for r in rows if not r["flags"]),
        "S1_missing_test_file": n("S1_missing"),
        "S1_missing_module_file": n("S1_module_missing"),
        "S2_uncollected": n("S2_uncollected"),
        "S2_runtime_noop": n("S2_runtime_noop"),
        "S3_red_at_head": n("S3_red"),
        "S3_timeout_unresolved": n("S3_timeout_unresolved"),
        "slow_but_green_alone": [r["module"] for r in rows
                                 if r["run"] and r["run"].get("timed_out")
                                 and r["serial_pass"]],
        "S4_no_coverage": n("S4_no_coverage"),
        "S4_ungated_by_merge_gate": n("S4_ungated_by_merge_gate"),
        "total_runtime_s": round(sum(r["seconds"] for r in results), 1),
    }

    gate_yes = not (summary["S1_missing_test_file"] or summary["S1_missing_module_file"]
                    or summary["S2_uncollected"] or summary["S2_runtime_noop"]
                    or summary["S3_red_at_head"] or summary["S3_timeout_unresolved"])

    out = {
        "leg": 71,
        "route": "CAP",
        "head": head,
        "interpreter": str(PY),
        "convention": ("no pytest in this repo; every test_*.py is a self-running script "
                       "run as `.venv/bin/python test_x.py` (scripts/merge_gate.sh)"),
        "gate": ("Does every module row in capabilities.py have a test file that exists, "
                 "is collected by pytest, and passes at current HEAD?"),
        "gate_answer": "yes" if gate_yes else "no",
        "gate_answer_scope": ("'yes'/'no' is decided on S1/S2/S3 only -- existence, "
                              "collectability and greenness. S4 rows are green but "
                              "ungated/uncovered and are reported separately."),
        "summary": summary,
        "serial_reruns": serial_done,
        "rows": rows,
    }
    dest = ROOT / "writeup" / "data" / "p2_route_cap_v1_audit.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=2) + "\n")

    print(f"\nHEAD {head}")
    print(f"  rows                      {summary['rows_total']}")
    print(f"  distinct tests run        {summary['distinct_tests_run']}")
    print(f"  clean rows                {summary['rows_clean']}")
    print(f"  S1 missing test file      {len(summary['S1_missing_test_file'])}")
    print(f"  S1 missing module file    {len(summary['S1_missing_module_file'])}")
    print(f"  S2 uncollected            {len(summary['S2_uncollected'])}")
    print(f"  S2 runtime no-op          {len(summary['S2_runtime_noop'])}")
    print(f"  S3 RED AT HEAD            {len(summary['S3_red_at_head'])}  "
          f"{summary['S3_red_at_head']}")
    print(f"  S3 timeout unresolved     {len(summary['S3_timeout_unresolved'])}  "
          f"{summary['S3_timeout_unresolved']}")
    print(f"  slow, but green alone     {len(summary['slow_but_green_alone'])}  "
          f"{summary['slow_but_green_alone']}")
    print(f"  S4 no coverage            {len(summary['S4_no_coverage'])}  "
          f"{summary['S4_no_coverage']}")
    print(f"  S4 ungated by merge gate  {len(summary['S4_ungated_by_merge_gate'])}  "
          f"{summary['S4_ungated_by_merge_gate']}")
    print(f"  GATE ANSWER               {out['gate_answer'].upper()}")
    print(f"\nwrote {dest}")


if __name__ == "__main__":
    main()
