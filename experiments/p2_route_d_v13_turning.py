"""P2 Route-D v13 -- the turning point: correcting v12's mechanism, and locating the wall.

v12 measured two things that stand: the a > 0 two-scale profile ENDS at a finite
radius X_c where E = c + aU crosses zero, with an algebraic zero of order 1/a;
and the gauged inverse's graded norm DIVERGES with J at that profile (J^+2.86 at
a = 0.2) while it is flat at the a = 0 anchor (J^-0.003).  It attributed the
second to a homogeneous mode ~ (X_c - X)^{-1/a}, and that attribution is WRONG --
a sign dropped converting d/dX to d/ds.  The mode at X_c vanishes like
(X_c - X)^{+1/a}; nothing is singular there.

The obstruction is in the far field instead, and it is worse than a local
singularity because no amount of resolution touches it: OUTSIDE X_c the same
homogeneous equation gives h ~ (log(X/X_c))^{1/a}, which GROWS, and the domain
space of the whole Route-D programme is a decay class.  This leg pins that down,
attributes v12's divergence to it by measurement rather than by argument, and
disqualifies the cheap repair.

NOT a logged Tier-1/2 experiment: deterministic Newton + deterministic sweeps.  Run:

    .venv/bin/python -u experiments/p2_route_d_v13_turning.py
    -> writeup/data/p2_route_d_v13_turning.json ; figure via
       .venv/bin/python writeup/4_p2_lottery/p2_route_d_v13_evidence.py   (fig31)

SIX measurements: S1 the correction; S2 the growing outer mode; S3 the divergence
attributed by outer radius; S4 where the extremal row is sourced; S5 the cheap
repair disqualified; S6 the ledger and the finite-interval spec.
"""

import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.collocation_newton import ACollocation                          # noqa: E402
from solver.turning_point import (bordered_norm, graded_norm_by_radius,     # noqa: E402
                                  homogeneous_far_field, inner_mode_exponent,
                                  log_growth_exponent, solved_profile,
                                  source_of_the_row, square_bordered_smin)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "p2_route_d_v13_turning.json"

ALPHA = 1.4
A_VALUES = (0.2, 0.25, 0.3, 0.35, 0.4, 0.5)
J_REF = 400


def s1_correction():
    rows = []
    for a in A_VALUES:
        col, om, c = solved_profile(J_REF, a)
        p, Xc = inner_mode_exponent(col, om, c)
        rows.append({"a": a, "Xc": Xc, "inner_exponent": p,
                     "predicted": 1.0 / a, "sign_correct": bool(p > 0)})
    return {"J": J_REF, "rows": rows,
            "v12_claim": "h ~ (X_c - X)^{-1/a} (WRONG: sign dropped in d/dX -> d/ds)",
            "corrected": "h ~ (X_c - X)^{+1/a}; the inhomogeneous solve is bounded "
                         "at X_c as well"}


def s2_outer_mode():
    rows, curves = [], []
    for a in A_VALUES:
        col, om, c = solved_profile(J_REF, a)
        X, h, Xc = homogeneous_far_field(col, om, c)
        q = log_growth_exponent(X, h, Xc)
        rows.append({"a": a, "Xc": Xc, "exponent": q, "predicted": 1.0 / a,
                     "h_at_1e8": float(h[-1])})
        idx = np.unique(np.linspace(0, X.size - 1, 250).astype(int))
        curves.append({"a": a, "Xc": Xc, "X": [float(x) for x in X[idx]],
                       "h": [float(x) for x in h[idx]]})
    # the quadrature gate, carried into the data
    col, om, c = solved_profile(J_REF, 0.3)
    conv = []
    for n in (1001, 4001, 16001):
        X, h, Xc = homogeneous_far_field(col, om, c, n=n)
        conv.append({"n": n, "exponent": log_growth_exponent(X, h, Xc)})
    # THE ROW THAT DOES NOT FIT, CHECKED RATHER THAN DROPPED.  a = 0.5 comes back
    # at 0.05 instead of 2.0 at J_REF -- and v12's own rate table already said the
    # collocation profile stops converging there.  Refining separates "the
    # prediction fails" from "the profile is not resolved".
    grid = []
    for a in (0.4, 0.5):
        for J in (400, 800, 1600):
            col, om, c = solved_profile(J, a)
            X, h, Xc = homogeneous_far_field(col, om, c)
            grid.append({"a": a, "J": J, "exponent": log_growth_exponent(X, h, Xc),
                         "predicted": 1.0 / a, "h_at_1e8": float(h[-1])})
    return {"rows": rows, "curves": curves, "quadrature_convergence": conv,
            "grid_refinement": grid}


def s3_attribution(Js=(200, 400, 800), a_values=(0.0, 0.2, 0.3)):
    out = []
    for a in a_values:
        rows = []
        for J in Js:
            col, om, c = solved_profile(J, a)
            r = graded_norm_by_radius(col, om, c, ALPHA)
            r["J"] = J
            r["X_grid_max"] = float(col.X[-1])
            rows.append(r)
        lj = np.log([r["J"] for r in rows])
        slopes = {}
        for key in rows[0]["by_cutoff"]:
            vals = [r["by_cutoff"][key] for r in rows]
            slopes[key] = float(np.polyfit(lj, np.log(vals), 1)[0])
        out.append({"a": a, "rows": rows, "slopes": slopes})
    return {"alpha": ALPHA, "blocks": out}


def s4_source(a_values=(0.2, 0.3, 0.4), Js=(200, 400, 800)):
    rows = []
    for a in a_values:
        for J in Js:
            col, om, c = solved_profile(J, a)
            s = source_of_the_row(col, om, c, ALPHA)
            s.update({"a": a, "J": J})
            rows.append(s)
    return rows


def s5_repair_disqualified(Js=(200, 400, 800)):
    square, over = [], []
    for a in (0.0, 0.2, 0.3):
        col = ACollocation(200, a=a)
        om = col.newton_gauged(c=0.5)["Omega"]
        smin, cond = square_bordered_smin(col, om, 0.5)
        square.append({"a": a, "J": 200, "smin": smin, "cond": cond})
        rows = []
        for J in Js:
            col, om, c = solved_profile(J, a)
            rows.append({"J": J, "norm": bordered_norm(col, om, c, ALPHA)})
        slope = float(np.polyfit(np.log([r["J"] for r in rows]),
                                 np.log([r["norm"] for r in rows]), 1)[0])
        over.append({"a": a, "rows": rows, "log_slope": slope})
    return {"square_bordered": square, "overdetermined": over,
            "why": "dilation Omega(X)->Omega(X/mu), c->mu c is a SYMMETRY of the "
                   "zero set at every a, so restoring c supplies KERNEL, not the "
                   "missing range direction"}


def main():
    data = {"meta": {"leg": "P2 Route-D v13", "alpha": ALPHA, "J_ref": J_REF,
                     "corrects": "P2 Route-D v12 (fig30) mechanism claim"}}
    print("S1 the correction ...", flush=True)
    data["s1_correction"] = s1_correction()
    print("S2 the outer mode ...", flush=True)
    data["s2_outer_mode"] = s2_outer_mode()
    print("S3 attribution ...", flush=True)
    data["s3_attribution"] = s3_attribution()
    print("S4 source of the row ...", flush=True)
    data["s4_source"] = s4_source()
    print("S5 the cheap repair ...", flush=True)
    data["s5_repair"] = s5_repair_disqualified()
    data["s6_ledger"] = {
        "corrected": "v12's stated mechanism for the ||A|| divergence",
        "unchanged": ["the profile ends at X_c with a zero of order 1/a",
                      "||A|| diverges with J at the a>0 profile, flat at a=0",
                      "Y0 in the graded codomain norm is not under budget"],
        "obstruction": "the far-field homogeneous mode grows like "
                       "(log(X/X_c))^{1/a}; the domain space is a decay class, so "
                       "the image generically leaves it -- a codimension-1 range "
                       "condition, not a local singularity",
        "next": "the finite-interval formulation on [0, X_c] with X_c an unknown: "
                "the far field is not in the domain at all, so the obstruction "
                "cannot arise. Kill switch: ||A|| vs J there.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))

    print("\nP2 ROUTE-D v13 -- the turning point\n" + "=" * 58)
    print("  S1  inner mode exponent (predicted +1/a; v12 said -1/a):")
    for r in data["s1_correction"]["rows"]:
        print("      a=%.2f  X_c=%8.4f  fitted %+.3f  vs %+.3f" %
              (r["a"], r["Xc"], r["inner_exponent"], r["predicted"]))
    print("  S2  outer mode ~ (log(X/X_c))^q, q predicted 1/a:")
    for r in data["s2_outer_mode"]["rows"]:
        print("      a=%.2f  q = %.4f  vs %.4f   (h reaches %.2e by X=1e8)" %
              (r["a"], r["exponent"], r["predicted"], r["h_at_1e8"]))
    print("  S2b the a=0.5 outlier, refined:")
    for r in data["s2_outer_mode"]["grid_refinement"]:
        print("      a=%.2f J=%4d  q = %.4f  vs %.4f" %
              (r["a"], r["J"], r["exponent"], r["predicted"]))
    print("  S3  ||A|| by outer cutoff, and its J-slope:")
    for b in data["s3_attribution"]["blocks"]:
        print("      a=%.1f  " % b["a"] + "  ".join(
            "X<=%s: J^%+.2f" % (k, v) for k, v in b["slopes"].items()))
    print("  S5  the cheap repair (restore c):")
    for r in data["s5_repair"]["square_bordered"]:
        print("      a=%.1f square bordered cond %.2e (smin %.1e)"
              % (r["a"], r["cond"], r["smin"]))
    for r in data["s5_repair"]["overdetermined"]:
        print("      a=%.1f overdetermined bordered norm J^%+.2f"
              % (r["a"], r["log_slope"]))
    print("\n[done] wrote %s" % OUT)


if __name__ == "__main__":
    main()
