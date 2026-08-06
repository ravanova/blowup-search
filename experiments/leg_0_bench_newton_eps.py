"""H6, sharpened: is item (6)'s truth value a property of the EQUATION or of roundoff?

The gate asserts `not converged` at a = 0.9, and `converged` degenerates to the
ABSOLUTE test residual_rms < 1e-6 (because hist[0] <= 1).  Both leg 71's run
(3.881e-07, converged=True) and this host's (2.120e-05, converged=False) are
40-ITERATION STALLS -- the iteration cap, not a convergence criterion.

If the stall level is chaotic, a perturbation FAR below any physical meaning --
1e-13 relative in `a`, i.e. 7 orders below the ladder spacing -- must move
residual_rms by orders of magnitude, and across 1e-6.  That is the discriminator:
a gate whose truth value flips under a 1e-13 input change is not measuring the
equation.

Run: .venv/bin/python experiments/leg_0_bench_newton_eps.py
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.profile_newton import continuation  # noqa: E402

THRESH = 1e-6


def main():
    out = {"threshold": THRESH, "note": "converged == residual_rms < 1e-6 (absolute)"}

    # -- epsilon perturbations of the LAST ladder point ---------------------
    eps_rows = []
    for eps in (0.0, 1e-13, 1e-12, 1e-11, 1e-9, 1e-7, 1e-5):
        ladder = [0.0, 0.3, 0.6, 0.9 + eps]
        r = continuation(ladder, n=601)[-1]
        eps_rows.append({"eps": eps, "converged": r["converged"],
                         "residual_rms": r["residual_rms"], "relres": r["relres"],
                         "c": r["c"], "iterations": r["iterations"],
                         "decades_vs_thresh":
                             float(np.log10(r["residual_rms"] / THRESH))})
    out["eps_ladder"] = eps_rows
    rms = [r["residual_rms"] for r in eps_rows]
    out["eps_summary"] = {
        "rms_min": min(rms), "rms_max": max(rms),
        "spread_decades": float(np.log10(max(rms) / min(rms))),
        "straddles_threshold": bool(min(rms) < THRESH < max(rms)),
        "n_converged": int(sum(1 for r in eps_rows if r["converged"])),
        "n_total": len(eps_rows),
        "all_are_iteration_capped": bool(all(r["iterations"] == 40
                                             for r in eps_rows)),
    }

    # -- H8: n sweep at the gate's ladder -----------------------------------
    n_rows = []
    for n in (401, 501, 599, 601, 603, 701, 801):
        r = continuation([0.0, 0.3, 0.6, 0.9], n=n)[-1]
        n_rows.append({"n": n, "converged": r["converged"],
                       "residual_rms": r["residual_rms"], "relres": r["relres"],
                       "c": r["c"], "iterations": r["iterations"],
                       "decades_vs_thresh":
                           float(np.log10(r["residual_rms"] / THRESH))})
    out["h8_n_sweep"] = n_rows
    nrms = [r["residual_rms"] for r in n_rows]
    out["h8_summary"] = {
        "rms_min": min(nrms), "rms_max": max(nrms),
        "spread_decades": float(np.log10(max(nrms) / min(nrms))),
        "straddles_threshold": bool(min(nrms) < THRESH < max(nrms)),
        "n_converged": int(sum(1 for r in n_rows if r["converged"])),
        "n_total": len(n_rows),
    }

    print(json.dumps(out, indent=1, default=float))


if __name__ == "__main__":
    main()
