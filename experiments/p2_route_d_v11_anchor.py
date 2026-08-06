"""P2 Route-D v11 -- the OTHER side of the inequality: Newton on the profile.

v10 measured what sharpening the constants can buy and the answer was: not
enough.  A perfect ||A|| bound multiplies the budget by 7.7, C_Q's slack is ~4x,
and the product only just reaches the residual floor of ~1e-2 with nothing spare
for the three open Z1 items.  So this leg attacks the factor nobody has touched
in eleven legs -- Y0, the DEFECT of the candidate profile, which enters the radii
polynomial linearly and which every a != 0 profile in this project has carried at
~1e-2 because it came from a GA over a small genome or from fixed-grid dynamic
relaxation.

NOT a logged Tier-1/2 experiment: deterministic Newton, no GA, no seeds.  Run:

    .venv/bin/python experiments/p2_route_d_v11_anchor.py
    -> writeup/data/p2_route_d_v11_anchor.json ; figure via
       .venv/bin/python writeup/4_p2_lottery/p2_route_d_v11_evidence.py  (fig29)

SIX measurements: V1 the known-answer gate; V2 the a-sweep against the GA floor;
V3 the survival boundary, found again with no genome; V4 grid convergence and the
WEIGHTED defect a certificate would actually use; V5 the budget, rewritten; V6
the ledger.
"""

import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.profile_newton import TwoScaleNewton, continuation      # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "p2_route_d_v11_anchor.json"

N = 801
ALPHA = 1.4                  # the operating point's decay grading (v8/v9/v10)
GA_FLOOR = 1e-2
Y0_MAX = 2.45e-4             # v10's conditional budget at (1.4, 0.15)


def weighted_defect(nw, om, c, alpha=ALPHA):
    """sup (1+X^2)^{(alpha+1)/2} |R2| -- the codomain norm a certificate uses.

    The RMS residual is what the GA optimized and what earlier legs quoted; it is
    NOT the quantity the radii polynomial sees.  Reporting both keeps the
    comparison to the GA honest and the budget statement correct.
    """
    R = nw.residual(om, c)
    w = (1.0 + nw.fam.X ** 2) ** (0.5 * (alpha + 1.0))
    return float(np.max(w * np.abs(R)))


def v1_known_answer():
    nw = TwoScaleNewton(a=0.0, n=N)
    ex = nw.anchor()
    exact = float(np.sqrt(np.mean(nw.residual(ex, 0.5) ** 2)))
    r = nw.solve(om0=ex * 1.3 + 0.05 * np.exp(-nw.fam.X ** 2), c0=0.4)
    return {"n": N, "exact_continuum_rms_on_the_grid": exact,
            "newton_rms": r["residual_rms"], "newton_c": r["c"],
            "iterations": r["iterations"],
            "profile_difference": float(np.max(np.abs(r["Omega"] - ex))),
            "history": r["history"],
            "reading": "Newton finds a zero of the DISCRETE system, which is not "
                       "the continuum solution: the exact anchor scores its own "
                       "discretization error on the same equations.  That is the "
                       "correct behaviour and it is the first thing to check, "
                       "because a solver that reproduced the continuum profile "
                       "exactly would be reporting something impossible."}


def v2_sweep(a_values=None):
    if a_values is None:
        a_values = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
                    0.55, 0.6, 0.7, 0.8, 0.9, 1.0]
    rows = continuation(a_values, n=N)
    for r in rows:
        nw = TwoScaleNewton(a=r["a"], n=N)
        s = nw.solve(om0=None, c0=0.5)
        r["weighted_defect"] = weighted_defect(nw, s["Omega"], s["c"])
    good = [r for r in rows if r["relres"] < 1e-8]
    return {"n": N, "rows": rows, "GA_floor": GA_FLOOR,
            "best_relres": min(r["relres"] for r in rows),
            "a_max_machine": max((r["a"] for r in good), default=0.0),
            "orders_below_GA": float(np.log10(GA_FLOOR
                                              / min(r["relres"] for r in rows))),
            "reading": "the GA floored at relres ~1e-2 for every a, and section 9 "
                       "read that floor as a property of the problem.  It is a "
                       "property of the SEARCH: with no genome at all, Newton "
                       "reaches machine precision on the same discrete equations "
                       "for every a below the survival boundary."}


def v3_boundary(a_values=None):
    if a_values is None:
        a_values = list(np.round(np.arange(0.44, 0.76, 0.02), 3))
    rows = []
    for a in a_values:
        nw = TwoScaleNewton(a=float(a), n=N)
        r = nw.solve(om0=None, c0=0.5)
        rows.append({"a": float(a), "relres": r["relres"],
                     "converged": bool(r["relres"] < 1e-8), "c": r["c"]})
    ok = [r["a"] for r in rows if r["converged"]]
    return {"rows": rows,
            "last_machine_precision_a": max(ok) if ok else None,
            "caveat": "Newton's own convergence is NOT the boundary test -- it "
                      "succeeds at isolated large a where the solution is not "
                      "grid-converged (V4).  Read this row together with V4's "
                      "verdict, which is the one that decides.",
            "GA_boundary": [0.5, 0.55],
            "reading": "the GA put the survival boundary at a* ~ 0.5-0.55 and "
                       "section 9-cont2 earned that with GA-, genome- and "
                       "basis-convergence.  Newton has no genome and no search "
                       "budget, so this is a fourth, independent confirmation -- "
                       "and it sharpens the character of the boundary: below it "
                       "an exact discrete traveling wave EXISTS, above it Newton "
                       "does not converge to one."}


def v4_grids(ns=(401, 801, 1601), a_values=(0.0, 0.2, 0.5, 0.8, 1.0)):
    """The check that decides the leg: is the Newton solution a CONTINUUM object?

    Machine precision on the discrete system says nothing by itself -- a solver
    can null a discrete equation with something that has no continuum limit.  The
    test is whether the solution itself (its speed c and its far-field values)
    stops moving as n grows.  It does for a <~ 0.5 and it does NOT for a >~ 0.8,
    where two of the three grids also fail to converge at all.  So the high-a
    successes are solver artifacts, and the survival boundary stands.
    """
    rows = []
    for n in ns:
        for a in a_values:
            nw = TwoScaleNewton(a=float(a), n=int(n))
            r = nw.solve(om0=None, c0=0.5)
            X = nw.fam.X
            i4 = int(np.argmin(np.abs(X - 4.0)))
            rows.append({"n": int(n), "a": float(a), "relres": r["relres"],
                         "residual_rms": r["residual_rms"], "c": r["c"],
                         "Omega_at_X4": float(r["Omega"][i4]),
                         "weighted_defect": weighted_defect(nw, r["Omega"],
                                                            r["c"])})
    verdict = []
    for a in a_values:
        sub = [r for r in rows if r["a"] == a]
        cs = [r["c"] for r in sub]
        om4 = [r["Omega_at_X4"] for r in sub]
        n_ok = sum(1 for r in sub if r["relres"] < 1e-8)
        verdict.append({"a": float(a), "c_spread": float(max(cs) - min(cs)),
                        "Omega_at_X4_spread": float(max(om4) - min(om4)),
                        "grids_reaching_machine_precision": n_ok,
                        "grid_converged": bool(max(cs) - min(cs) < 1e-3
                                               and n_ok >= 2)})
    return {"rows": rows, "verdict": verdict,
            "grid_converged_a_max": max((v["a"] for v in verdict
                                         if v["grid_converged"]), default=0.0),
            "reading": "the machine-precision residual is a statement about the "
                       "DISCRETE system, so it must not improve with n -- it is "
                       "already at rounding.  What n controls is how far the "
                       "discrete solution sits from the continuum one, which is "
                       "the error a certificate would still have to price (v4 W6 "
                       "measured that separately at J^-2.1..-2.6).  The weighted "
                       "defect is reported because the RMS is not what the radii "
                       "polynomial sees -- and it is 6 orders LARGER than the "
                       "RMS, because the codomain weight amplifies exactly the "
                       "far field where the residual lives."}


def v5_budget(v2, v4):
    a_max = v4["grid_converged_a_max"]
    good = [r for r in v2["rows"]
            if r["relres"] < 1e-8 and r["a"] <= a_max + 1e-12]
    wd = [r["weighted_defect"] for r in good]
    best = min(wd) if wd else float("inf")
    worst = max(wd) if wd else float("inf")
    # The budget condition Y0 <= Y0_max is a UNIVERSAL statement over the a-range
    # this block declares it on ("for a < a*"), so the margin that certifies it is
    # the WORST-CASE one: Y0_max / max(weighted_defect).  Building it from the min
    # certifies nothing -- it reports the most favourable row of a set the claim
    # quantifies over.  The min is kept, clearly named, as the best-row diagnostic.
    over = [{"a": r["a"], "weighted_defect": r["weighted_defect"],
             "violation_x": r["weighted_defect"] / Y0_MAX}
            for r in good if r["weighted_defect"] > Y0_MAX]
    under = [r["weighted_defect"] for r in good
             if r["weighted_defect"] <= Y0_MAX]
    return {"Y0_max_from_v10": Y0_MAX,
            "GA_floor_rms": GA_FLOOR,
            "a_range_used": a_max,
            "n_good_rows": len(good),
            "newton_weighted_defect_min": best,
            "newton_weighted_defect_max": worst,
            "margin": Y0_MAX / worst if worst > 0 else float("inf"),
            "margin_selection": "worst-case: Y0_max / newton_weighted_defect_max",
            "margin_at_best_row": Y0_MAX / best if best > 0 else float("inf"),
            "budget_holds_uniformly": not over,
            "rows_over_budget": over,
            "worst_violation_x": (max(o["violation_x"] for o in over)
                                  if over else None),
            "margin_over_rows_within_budget": (Y0_MAX / max(under)
                                               if under else None),
            "reading": "the budget condition is Y0 <= Y0_max.  Every earlier leg "
                       "compared 1e-2 against 2.45e-4 and concluded the profile "
                       "was ~40x too poor.  With Newton the weighted defect of "
                       "the discrete profile is many orders BELOW the budget on "
                       "most of the range but NOT uniformly (see rows_over_budget "
                       "-- the margin above is worst-case, per leg 247), so the "
                       "profile's defect stops being the binding constraint only "
                       "where the budget actually holds.  What binds instead is "
                       "the three unpriced "
                       "Z1 items, which is a different and more tractable "
                       "problem than 'find a better profile'.  CAREFUL: this is "
                       "the defect of the DISCRETE profile in the ROUTE-A "
                       "discretization; carrying it into the certificate needs "
                       "the same object in the theta-collocation basis plus the "
                       "discretization error, which is exactly the open ledger "
                       "item 'Z1 core discretization'."}


def main():
    data = {"meta": {
        "leg": "P2 Route-D v11 (Newton on the two-scale profile: the other side "
               "of the inequality)",
        "tier": "Level-1 tooling + a structural positive (NOT a certificate)",
        "reproduce": "python experiments/p2_route_d_v11_anchor.py",
        "arithmetic": "plain float64; Newton with an exact analytic Jacobian, "
                      "gated against the closed-form a = 0 traveling wave",
    }}
    data["v1_known_answer"] = v1_known_answer()
    data["v2_sweep"] = v2_sweep()
    data["v3_boundary"] = v3_boundary()
    data["v4_grids"] = v4_grids()
    data["v5_budget"] = v5_budget(data["v2_sweep"], data["v4_grids"])
    data["v6_ledger"] = {
        "changed": "Y0 (the profile defect) moves from ~1e-2 (GA / relaxation) "
                   "to machine precision on the discrete system for a < a*",
        "still_open": ["Z1 core<->far coupling", "Z1 core discretization "
                       "(now the binding item)", "discrete<->continuum transfer"],
        "next": ["carry the Newton profile into the theta-collocation basis the "
                 "bounds live in, and measure Y0 there",
                 "price the core discretization error (v4 W6 measured it, never "
                 "bounded it) -- it is now what limits Y0",
                 "C_sup (elasticity ~1, ~2x available)"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))

    v1, v2, v3 = data["v1_known_answer"], data["v2_sweep"], data["v3_boundary"]
    print("\nP2 ROUTE-D v11 -- Newton on the profile\n" + "=" * 58)
    print("  V1  a=0: Newton %.1e vs the exact continuum anchor's %.1e on the "
          "same discrete system (%d iterations)"
          % (v1["newton_rms"], v1["exact_continuum_rms_on_the_grid"],
             v1["iterations"]))
    print("  V2  best relres %.1e -- %.0f orders below the GA floor; machine "
          "precision up to a = %.2f"
          % (v2["best_relres"], v2["orders_below_GA"], v2["a_max_machine"]))
    print("  V3  Newton converges up to a = %s, but V4's GRID test says the "
          "solution is a continuum object only up to a = %.2f (GA said %s)"
          % (v3["last_machine_precision_a"],
             data["v4_grids"]["grid_converged_a_max"], v3["GA_boundary"]))
    b = data["v5_budget"]
    print("  V5  weighted defect (worst of %d good rows) %.4e vs budget %.2e "
          "-- worst-case margin %.4gx (best row %.4e, margin %.4gx)"
          % (b["n_good_rows"], b["newton_weighted_defect_max"],
             b["Y0_max_from_v10"], b["margin"],
             b["newton_weighted_defect_min"], b["margin_at_best_row"]))
    if b["rows_over_budget"]:
        print("      NOT uniform: %d row(s) over budget -- %s"
              % (len(b["rows_over_budget"]),
                 ", ".join("a=%.2f by %.2fx" % (o["a"], o["violation_x"])
                           for o in b["rows_over_budget"])))
    print("\n[done] wrote %s" % OUT)


if __name__ == "__main__":
    main()
