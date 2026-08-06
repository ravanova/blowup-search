"""Route-OLA v1 BENCH CHECK -- what the op_lower repair changed, measured.

The repair on `bench/fix-op-lower-bound-violation` fixes the two soundness
mechanisms leg 101 measured in `solver/op_lower.py`.  Its novelty pass
(writeup/novelty/leg_101.md sec 8.2) pre-committed a two-clause rule, and BOTH
clauses are load-bearing -- a repair that fixed soundness by returning 0
everywhere would satisfy the first and fail the second:

  > The repair PASSES iff, over all 209 gate-deciding Tier-A cases, the count of
  > soundness violations is 0 -- no L > N_ref beyond 0 ULP of the returned float
  > -- AND the production bracket at J = 200/300/400 moves by no more than 1e-9
  > relative, downward only.  The count of candidates rejected on the production
  > path is reported as a magnitude and must be 0.

This runner measures the second clause and the scope statement, side by side
with the PRE-REPAIR values, which are carried as literals below because the
pre-repair module no longer exists on this branch.  The first clause is measured
by `experiments/p2_route_ola_v1_adversarial.py`, which is the SAME battery leg
101 ran, unchanged in its zoo, its reference and its violation definition.

It also re-verifies the scope bound leg 101 used to argue that no banked Route-D
number was contaminated -- the 307.9-decade production headroom -- because a
repair that changed the operator, the candidate family or the norms would have
moved it, and a headroom number quoted from before the repair would be stale.

Run: .venv/bin/python experiments/p2_route_ola_v1_bench_check.py
"""

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.decay_collocation import Collocation, C_ANCHOR       # noqa: E402
from solver.holder_norms import HolderNorm                       # noqa: E402
from solver.op_lower import (                                    # noqa: E402
    NORM_SLACK, REJECT_REL, best_lower, family_lower, sign_pattern_lower,
    smooth_family,
)

#: The banked pre-repair values, measured on this branch's merge base with the
#: identical call (`family_lower`, n_centre=12, n_step=12) before a line of
#: `solver/op_lower.py` was touched.  Carried as literals so the comparison
#: survives the module being replaced.
PRE = {
    200: {"lower": 2.682095980021302, "sign": 0.9726246167747283,
          "max_image": 2.379792003401471, "decades": 307.87817655904615},
    300: {"lower": 2.805616494722006, "sign": 0.9535185138478504,
          "max_image": 2.3799793357393693, "decades": 307.87814237362215},
    400: {"lower": 2.8844503038532703, "sign": 0.9422584088472276,
          "max_image": 2.3800617383434908, "decades": 307.8781273371988},
}
ARGMAX_PRE = "bump3.12/0.50"
BUDGET = 1e-9


def setup(J, alpha=1.5, gamma=0.5):
    col = Collocation(J)
    M = np.empty((J, J))
    M[0, :] = col.to_coef.sum(axis=0)
    M[1:, :] = col.jacobian_matrix(col.anchor(), C_ANCHOR)[1:, :]
    A = np.linalg.inv(M)
    dom = HolderNorm(col.theta, col.X, alpha, gamma)
    cod = HolderNorm(col.theta, col.X, alpha + 1.0, gamma)
    cod.w[0] = 1.0
    return col, A, dom, cod


def production_rows():
    """The banked Route-D bracket input, before and after, at three J."""
    rows = []
    for J in (200, 300, 400):
        col, A, dom, cod = setup(J)
        f = family_lower(A, dom, cod, col.theta, n_centre=12, n_step=12)
        s = sign_pattern_lower(A, dom, cod)
        pre = PRE[J]
        rel = (pre["lower"] - f["lower"]) / pre["lower"]

        # the scope bound, RE-MEASURED rather than quoted from leg 101
        worst, cancel = 0.0, 0.0
        for name, g in smooth_family(col.theta, cod.w, n_centre=8, n_step=8):
            g = g.copy()
            g[0] = 0.0
            v = A @ g
            mv = float(np.max(np.abs(v)))
            worst = max(worst, mv)
            if mv > 0.0:
                cancel = max(cancel, float(np.max(np.abs(A) @ np.abs(g))) / mv)
        decades = float(np.log10(np.finfo(float).max / worst))

        rows.append({
            "J": J,
            "lower_pre": pre["lower"], "lower_post": float(f["lower"]),
            "rel_move": float(rel), "moved_down": bool(f["lower"] <= pre["lower"]),
            "within_budget": bool(rel <= BUDGET),
            "sign_pre": pre["sign"], "sign_post": float(s["lower"]),
            "argmax_pre": ARGMAX_PRE, "argmax_post": f["argmax"],
            "argmax_unchanged": bool(f["argmax"] == ARGMAX_PRE),
            "rejected": int(f["rejected"]), "saturated": int(f["saturated"]),
            "max_rel_bound": float(f["max_rel_bound"]),
            "pow2_exponent": int(f["pow2_exponent"]),
            "max_image_pre": pre["max_image"], "max_image_post": float(worst),
            "decades_pre": pre["decades"], "decades_post": decades,
            "decades_move": float(decades - pre["decades"]),
            "max_cancellation_ratio": float(cancel),
            "max_absA": float(np.max(np.abs(A))),
        })
    return rows


def ascent_row():
    """`best_lower` end to end, so the ascent path is exercised too."""
    col, A, dom, cod = setup(300)
    r = best_lower(A, dom, cod, col.theta, ascent_iters=400, n_centre=12,
                   n_step=12)
    return {"J": 300, "iters": 400,
            "sign_patterns": float(r["sign_patterns"]),
            "smooth_family": float(r["smooth_family"]),
            "after_ascent": float(r["after_ascent"]),
            "headline": float(r["lower"]),
            "ascent_gain": float(r["ascent_gain"]),
            "rejected": int(r["rejected"]), "saturated": int(r["saturated"]),
            "headline_pre": PRE[300]["lower"],
            "rel_move": float((PRE[300]["lower"] - r["lower"])
                              / PRE[300]["lower"])}


def main():
    t0 = time.time()
    rows = production_rows()
    asc = ascent_row()
    dt = time.time() - t0

    worst_move = max(r["rel_move"] for r in rows)
    all_down = all(r["moved_down"] for r in rows)
    all_budget = all(r["within_budget"] for r in rows)
    tot_rej = sum(r["rejected"] for r in rows) + asc["rejected"]
    tot_sat = sum(r["saturated"] for r in rows) + asc["saturated"]
    argmax_ok = all(r["argmax_unchanged"] for r in rows)
    worst_decade_move = max(abs(r["decades_move"]) for r in rows)

    print("PRODUCTION BRACKET -- the pre-committed second clause")
    print("  %-5s %-22s %-22s %-12s %s" % ("J", "pre-repair", "post-repair",
                                           "rel move", "argmax"))
    for r in rows:
        print("  %-5d %-22.16f %-22.16f %-12.3e %s"
              % (r["J"], r["lower_pre"], r["lower_post"], r["rel_move"],
                 r["argmax_post"] + ("" if r["argmax_unchanged"] else " CHANGED")))
    print("  direction: %s   worst move %.3e (budget %.0e)   argmax unchanged: %s"
          % ("DOWN on all three" if all_down else "NOT ALL DOWN",
             worst_move, BUDGET, argmax_ok))
    print("  candidates rejected on the production path: %d   saturated: %d"
          % (tot_rej, tot_sat))
    print("  certified relative error bound, worst over the three J: %.3e"
          % max(r["max_rel_bound"] for r in rows))
    print("  (norm-functor slack %.0e, reject threshold %.0e, cancellation "
          "ratio <= %.2f)"
          % (NORM_SLACK, REJECT_REL,
             max(r["max_cancellation_ratio"] for r in rows)))

    print("\nASCENT PATH (best_lower, J = 300, 400 iters)")
    print("  sign %.9f  family %.15f  after_ascent %.15f  headline %.15f"
          % (asc["sign_patterns"], asc["smooth_family"], asc["after_ascent"],
             asc["headline"]))
    print("  gain %.3fx   moved down %.3e from the pre-repair headline   "
          "rejected %d" % (asc["ascent_gain"], asc["rel_move"], asc["rejected"]))

    print("\nSCOPE -- the 307.9-decade production headroom, RE-MEASURED")
    for r in rows:
        print("  J = %-4d max family image %.9f (pre %.9f), %.6f decades below "
              "the overflow ceiling (pre %.6f, move %+.2e)"
              % (r["J"], r["max_image_post"], r["max_image_pre"],
                 r["decades_post"], r["decades_pre"], r["decades_move"]))
    # computed as a difference of logs: the ratio itself overflows float64
    above = float(np.log10(rows[-1]["max_absA"]) - np.log10(5e-324))
    print("  the operator's own entries reach %.1f, i.e. %.1f decades ABOVE "
          "the denormal floor -- the second mechanism is as far out of reach as "
          "the first" % (rows[-1]["max_absA"], above))

    verdict = (all_down and all_budget and argmax_ok and tot_rej == 0
               and tot_sat == 0)
    print("\nBENCH CHECK (second clause of the pre-committed rule): %s"
          % ("PASS" if verdict else "FAIL"))
    print("elapsed %.1f s" % dt)

    out = {
        "leg": 101, "route": "OLA", "branch": "bench/fix-op-lower-bound-violation",
        "generated": time.strftime("%Y-%m-%d"),
        "rule": ("the production bracket at J = 200/300/400 moves by no more "
                 "than 1e-9 relative, downward only, with 0 candidates rejected "
                 "on the production path"),
        "budget_rel": BUDGET,
        "norm_slack": NORM_SLACK, "reject_rel": REJECT_REL,
        "verdict": "pass" if verdict else "fail",
        "all_moved_down": all_down, "all_within_budget": all_budget,
        "argmax_unchanged": argmax_ok,
        "worst_rel_move": worst_move,
        "rejected_total": tot_rej, "saturated_total": tot_sat,
        "worst_decade_move": worst_decade_move,
        "headroom_decades": {str(r["J"]): r["decades_post"] for r in rows},
        "decades_above_denormal_floor": above,
        "production": rows,
        "ascent": asc,
        "elapsed_s": round(dt, 2),
    }
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "writeup", "data", "p2_route_ola_v1_bench_check.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("wrote %s" % path)
    return out


if __name__ == "__main__":
    main()
