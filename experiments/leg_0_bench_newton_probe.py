"""Probe for test_profile_newton.py item (6) -- H6/H7/H8/H9 from the novelty pass.

Item (6) asserts `not converged` at a = 0.9 on the ladder [0.0, 0.3, 0.6, 0.9],
n = 601.  Leg 71 measured converged=True (relres 2.89e-06); this host measures
converged=False (relres 1.6e-04).  `solve()` decides convergence by

    converged = hist[-1] < 1e-6 * max(1.0, hist[0])  or  hist[-1] < 1e-9

and hist[0] <= 1 here, so clause 1 is the ABSOLUTE test residual_rms < 1e-6.

This probe measures, for a = 0.9:
  H6  spread of residual_rms across BLAS thread counts (set by the caller via env)
  H7  ladder refinement at fixed n
  H8  n sweep at fixed ladder
  H9  the two branches of continuation's retry, separately

Run: .venv/bin/python experiments/leg_0_bench_newton_probe.py [mode]
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.profile_newton import TwoScaleNewton, continuation  # noqa: E402

THRESH = 1e-6


def _row(r, a):
    return {"a": a, "converged": r["converged"], "residual_rms": r["residual_rms"],
            "relres": r["relres"], "c": r["c"], "iterations": r["iterations"],
            "hist0": r["history"][0], "margin_decades":
            float(np.log10(r["residual_rms"] / THRESH))}


def h9_branches(ladder, n):
    """Re-run continuation by hand, keeping BOTH branches of the retry."""
    out = []
    om, c = None, 0.5
    for a in ladder:
        nw = TwoScaleNewton(a=float(a), n=n)
        warm = nw.solve(om0=om, c0=c)
        rec = {"a": float(a), "warm": _row(warm, float(a))}
        chosen = warm
        if warm["relres"] > 1e-10:
            cold = nw.solve(om0=None, c0=0.5)
            rec["cold"] = _row(cold, float(a))
            if cold["relres"] < warm["relres"]:
                chosen = cold
            rec["retry_taken"] = bool(cold["relres"] < warm["relres"])
        rec["chosen"] = _row(chosen, float(a))
        out.append(rec)
        if chosen["relres"] < 1e-10:
            om, c = chosen["Omega"], chosen["c"]
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    res = {"mode": mode, "threads": {
        k: os.environ.get(k) for k in
        ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")}}

    if mode in ("all", "h6"):
        # the exact gate configuration, repeated -- determinism within one process
        reps = []
        for _ in range(3):
            rows = continuation([0.0, 0.3, 0.6, 0.9], n=601)
            reps.append({"a09": rows[-1], "a03": rows[1]})
        res["h6_repeats"] = reps

    if mode in ("all", "h9"):
        res["h9"] = h9_branches([0.0, 0.3, 0.6, 0.9], 601)

    if mode in ("all", "h7"):
        ladders = {
            "gate_4pt": [0.0, 0.3, 0.6, 0.9],
            "7pt": [0.0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9],
            "10pt": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
            "banked_17pt": [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4,
                            0.45, 0.5, 0.55, 0.6, 0.7, 0.8, 0.9],
        }
        res["h7"] = {k: continuation(v, n=601)[-1] for k, v in ladders.items()}

    if mode in ("all", "h8"):
        res["h8"] = {str(n): continuation([0.0, 0.3, 0.6, 0.9], n=n)[-1]
                     for n in (401, 501, 599, 601, 603, 701, 801, 1201)}

    print(json.dumps(res, indent=1, default=float))


if __name__ == "__main__":
    main()
