"""H6, sharpened: is item (6)'s truth value a property of the EQUATION or of roundoff?

The gate asserts on the a = 0.9 row of `continuation([0.0, 0.3, 0.6, 0.9], n=601)`.
`converged` degenerates to the ABSOLUTE test residual_rms < 1e-6 (because the measured
hist[0] = 0.0465 makes `max(1.0, hist[0])` exactly 1.0).  Both leg 71's run
(3.881e-07, converged=True) and this host's (2.120e-05, converged=False) are
40-ITERATION STALLS -- the iteration cap, not a convergence criterion.

Two discriminators, printed ONE ROW AT A TIME (each row is expensive, and a probe
that only prints at the end loses everything if it is interrupted):

  eps  perturb the last ladder point by 1e-13 .. 1e-5.  A perturbation 7+ orders
       below the ladder spacing that moves residual_rms by orders of magnitude, and
       across 1e-6, proves the gate's truth value is not a property of the equation.
  n    sweep the grid at the gate's ladder, to check the SEPARATION the repaired
       gate actually asserts (a=0.3 below 1e-9, a=0.9 above 1e-8) holds off n=601.

Run: .venv/bin/python experiments/leg_0_bench_newton_eps.py [eps|n|all]
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.profile_newton import continuation  # noqa: E402

THRESH = 1e-6


def emit(tag, extra, rows):
    """One ladder run -> one printed line, flushed immediately."""
    last, mid = rows[-1], rows[1]
    rec = {"probe": tag, **extra,
           "a09_converged": last["converged"],
           "a09_residual_rms": last["residual_rms"], "a09_relres": last["relres"],
           "a09_iterations": last["iterations"], "a09_c": last["c"],
           "a09_decades_vs_1e-6": float(np.log10(last["residual_rms"] / THRESH)),
           "a03_relres": mid["relres"], "a03_converged": mid["converged"],
           # the two thresholds the repaired gate asserts
           "gate_a03_below_1e-9": bool(mid["relres"] < 1e-9),
           "gate_a09_above_1e-8": bool(last["relres"] > 1e-8)}
    print(json.dumps(rec, default=float), flush=True)
    return rec


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("all", "eps"):
        for eps in (0.0, 1e-13, 1e-11, 1e-9, 1e-7, 1e-5):
            emit("eps", {"eps": eps},
                 continuation([0.0, 0.3, 0.6, 0.9 + eps], n=601))

    if mode in ("all", "n"):
        for n in (401, 501, 599, 601, 603, 701):
            emit("n", {"n": n}, continuation([0.0, 0.3, 0.6, 0.9], n=n))


if __name__ == "__main__":
    main()
