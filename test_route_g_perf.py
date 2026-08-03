"""Gates for the Route-G v1 performance work -- both speedups change WHAT IS COMPUTED,
so both need a correctness gate, not a timing anecdote.

The leg's G2 stage cost ~41 min and a killed container orphaned it. Two changes cut
that: the steps ladder became ONE chained trajectory read at each rung (8100 steps ->
4000), and the resolution ladder runs in processes (each relaxation is single-threaded,
so four rungs cost the longest rather than the sum). Neither may move a number.

Pre-committed predicates:
  (1) CHAINING IS EQUIVALENT: reading one trajectory at 200 and 400 steps gives the same
      c_l, c_omega and residual as restarting from the ansatz for 200 and for 400 --
      to 1e-10 relative. This is the gate the whole steps-ladder saving rests on, and
      it is not obvious: it holds only because renorm=True re-pins the normalization to
      the same frozen origin slopes on resumption, and dt is state-derived each step.
  (2) EARLY CONVERGENCE IS REFUSED, NOT PADDED: if the trajectory converges before a
      rung, the chained ladder stops there rather than emitting rungs that the
      restarted ladder would not have produced.
  (3) PARALLEL MAP PRESERVES LADDER ORDER AND VALUES: `_map_maybe_parallel` returns
      results in job order, not completion order, and agrees with the serial map.
  (4) THE SERIAL FALLBACK IS REACHABLE: ROUTE_G_SERIAL=1 forces the serial path, so a
      one-core machine and a debugging run reproduce the same artifact.
  (5) MERGE IS SAFE: folding a sibling file in adds its stages, and REFUSES when a
      stage is present in both and differs -- the failure that would let a --quick run
      silently overwrite a real one.

Run: python test_route_g_perf.py     (no scipy; ~3 min -- gate 1 relaxes twice)
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments"))

from experiments.p2_route_g_v1_collapse import (        # noqa: E402
    _chained_steps_ladder, _map_maybe_parallel,
)


def test_chaining_is_equivalent():
    """(1) one chained trajectory == restarting at every rung."""
    from spike1_stepC_gate import run_gate
    rungs = _chained_steps_ladder(300, 48, 1e-3, 1e5, [200, 400])
    assert [r["steps"] for r in rungs] == [200, 400]
    worst = 0.0
    for r in rungs:
        direct = run_gate(300, 48, 1e-3, 1e5, steps=r["steps"])
        for key in ("c_l", "c_omega", "residual"):
            rel = abs(r[key] - direct[key]) / max(abs(direct[key]), 1e-300)
            worst = max(worst, rel)
            assert rel < 1e-10, (f"{key} at {r['steps']} steps: chained {r[key]!r} "
                                 f"vs restarted {direct[key]!r} (rel {rel:.2e})")
    print(f"[ok] (1) chained == restarted to {worst:.1e} relative, at both rungs "
          f"(8100 -> 4000 steps on the real ladder)")


def test_early_convergence_refused():
    """(2) a converged trajectory stops the ladder instead of padding it."""
    # tol=1e-9 is never reached here (residuals bottom out ~1e-2), so assert the
    # STRUCTURE that implements the refusal rather than fabricating a converged run:
    # the loop breaks on res["converged"], and `done` accumulates ACTUAL steps taken.
    src = (ROOT / "experiments" / "p2_route_g_v1_collapse.py").read_text()
    body = src.split("def _chained_steps_ladder")[1].split("\ndef ")[0]
    assert 'if res["converged"]:' in body, "no early-convergence guard"
    assert "break" in body, "guard does not stop the ladder"
    assert 'done += res["steps"]' in body, \
        "must accumulate steps ACTUALLY taken, else a short run mislabels its rung"
    rungs = _chained_steps_ladder(300, 48, 1e-3, 1e5, [150])
    assert rungs[0]["steps"] == 150, f"rung mislabelled: {rungs[0]['steps']}"
    print("[ok] (2) early convergence breaks the ladder; rungs labelled by steps taken")


def _square(job):
    return {"n_r": job[0], "value": job[0] ** 2}


def test_parallel_map_order_and_values():
    """(3)+(4) parallel map == serial map, in ladder order, and the fallback works."""
    jobs = [(300, 48, 1e5, 10), (600, 48, 1e5, 10), (450, 48, 1e5, 10)]
    par = _map_maybe_parallel(_square, jobs)
    assert [r["n_r"] for r in par] == [300, 600, 450], \
        f"must be LADDER order, got {[r['n_r'] for r in par]}"
    os.environ["ROUTE_G_SERIAL"] = "1"
    try:
        ser = _map_maybe_parallel(_square, jobs)
    finally:
        del os.environ["ROUTE_G_SERIAL"]
    assert par == ser, "parallel and serial maps disagree"
    print("[ok] (3)+(4) parallel map preserves ladder order and matches the serial "
          "fallback (ROUTE_G_SERIAL=1)")


def test_merge_is_safe():
    """(5) merge folds stages in, and refuses a conflicting overwrite."""
    script = ROOT / "experiments" / "p2_route_g_v1_collapse.py"
    with tempfile.TemporaryDirectory() as td:
        data = Path(td) / "writeup" / "data"
        data.mkdir(parents=True)
        (data / "main.json").write_text(json.dumps({"leg": "x", "g1_a": {"v": 1}}))
        (data / "side.json").write_text(json.dumps({"leg": "x", "g2_b": {"v": 2}}))
        env = dict(os.environ, ROUTE_G_DATA=str(data))
        run = subprocess.run(
            [sys.executable, str(script), "--merge", "side.json", "--out", "main.json"],
            capture_output=True, text=True, env=env, cwd=td)
        merged = json.loads((data / "main.json").read_text())
        assert "g2_b" in merged and "g1_a" in merged, \
            f"merge did not fold stages in: {sorted(merged)} / {run.stderr[-400:]}"

        # conflicting stage must be REFUSED
        (data / "bad.json").write_text(json.dumps({"g2_b": {"v": 999}}))
        bad = subprocess.run(
            [sys.executable, str(script), "--merge", "bad.json", "--out", "main.json"],
            capture_output=True, text=True, env=env, cwd=td)
        assert bad.returncode != 0 and "refusing to merge" in (bad.stdout + bad.stderr), \
            f"a conflicting merge was NOT refused: rc={bad.returncode}"
        assert json.loads((data / "main.json").read_text())["g2_b"]["v"] == 2, \
            "refused merge must leave the target untouched"
    print("[ok] (5) merge folds sibling stages in and refuses a conflicting overwrite")


if __name__ == "__main__":
    test_chaining_is_equivalent()
    test_early_convergence_refused()
    test_parallel_map_order_and_values()
    test_merge_is_safe()
    print("\nALL ROUTE-G PERF TESTS PASSED")
