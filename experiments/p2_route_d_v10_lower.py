"""P2 Route-D v10 -- a LOWER bound on ||A|| worth reading, and what it decides.

v9 ended with the sharpest statement this project has made about its own state:
every bracket quoted so far has a lower end that is a maximum over sign patterns,
which is nearly meaningless, and until that is fixed "the bound is 50x too big"
and "the operator really is that large" cannot be told apart -- while implying
opposite decisions about the whole Route-D lane.  v9 also paid for the confusion,
converting the uninterpretable bracket into a "19x available gain" that was pure
artifact.

So this leg builds the adversary (banked lesson 9, applied to the operator rather
than to the quadratic) and then reads the answer.

NOT a logged Tier-1/2 experiment: deterministic (no GA, no seeds, no predicate
lock).  Run:

    .venv/bin/python experiments/p2_route_d_v10_lower.py
    -> writeup/data/p2_route_d_v10_lower.json ; figure via
       .venv/bin/python writeup/4_p2_lottery/p2_route_d_v10_evidence.py   (fig28)

SIX measurements:

  W1  THE LOWER BOUND against the sign-pattern baseline, over J.
  W2  THE SAME AT THE OPERATING POINT (1.4, 0.15) -- the bracket that the budget
      is actually evaluated in, which is not the reference point.
  W3  WHAT THE EXTREMIZER IS.  A wide far-field shape, not an oscillation.
  W4  THE BRACKET ACROSS THE MAP.
  W5  THE VERDICT: how much of the budget could a perfect upper bound recover,
      and what stays ambiguous.
  W6  THE LEDGER, and the next brick this implies.
"""

import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.decay_collocation import Collocation, C_ANCHOR             # noqa: E402
from solver.holder_norms import HolderNorm                             # noqa: E402
from solver.nk_bounds import sup_part_upper, budget                    # noqa: E402
from solver.nk_seminorm import seminorm_closure                        # noqa: E402
from solver.hilbert_holder import (hilbert_holder_constant,            # noqa: E402
                                   quadratic_constant_full)
from solver.hilbert_pointwise import pointwise_curves, weighted_sups   # noqa: E402
from solver.op_lower import (best_lower, family_lower,                 # noqa: E402
                             sign_pattern_lower, smooth_family)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "p2_route_d_v10_lower.json"

REF = (1.5, 0.5)
OP = (1.4, 0.15)
RHO = 6.0


def setup(J, alpha, gamma):
    col = Collocation(J)
    M = np.empty((J, J))
    M[0, :] = col.to_coef.sum(axis=0)
    M[1:, :] = col.jacobian_matrix(col.anchor(), C_ANCHOR)[1:, :]
    A = np.linalg.inv(M)
    dom = HolderNorm(col.theta, col.X, alpha, gamma)
    cod = HolderNorm(col.theta, col.X, alpha + 1.0, gamma)
    cod.w[0] = 1.0
    return col, A, dom, cod


def upper(A, dom, cod, alpha, gamma, rho=RHO):
    C_sup = sup_part_upper(A, dom.w, cod.w, cod.pair)
    cv = pointwise_curves(alpha, gamma, rho=rho, n_theta=90, n_quad=300)
    d = seminorm_closure(alpha, gamma, C_sup, curves=cv)
    return d["A_upper"], C_sup


def w1_ladder(Js=(200, 400, 800, 1600)):
    rows = []
    for J in Js:
        col, A, dom, cod = setup(J, *REF)
        base = sign_pattern_lower(A, dom, cod)["lower"]
        fam = family_lower(A, dom, cod, col.theta, n_centre=30, n_step=40)
        up, C_sup = upper(A, dom, cod, *REF)
        rows.append({"J": J, "sign_patterns": base, "lower": fam["lower"],
                     "argmax": fam["argmax"], "upper": up, "C_sup": C_sup,
                     "bracket": up / fam["lower"],
                     "bracket_old": up / base})
    return {"alpha": REF[0], "gamma": REF[1], "ladder": rows,
            "reading": "the sign-pattern baseline DEGRADES with J -- it is not "
                       "converging to anything about the operator, it is "
                       "measuring how badly a grid-scale sign pattern is punished "
                       "by a Holder seminorm.  The smooth family is stable."}


def w2_operating(Js=(200, 400, 800)):
    rows = []
    for J in Js:
        col, A, dom, cod = setup(J, *OP)
        base = sign_pattern_lower(A, dom, cod)["lower"]
        fam = family_lower(A, dom, cod, col.theta, n_centre=30, n_step=40)
        up, C_sup = upper(A, dom, cod, *OP)
        rows.append({"J": J, "sign_patterns": base, "lower": fam["lower"],
                     "argmax": fam["argmax"], "upper": up, "C_sup": C_sup,
                     "bracket": up / fam["lower"]})
    return {"alpha": OP[0], "gamma": OP[1], "ladder": rows,
            "reading": "this is where the budget is actually evaluated, and has "
                       "been for three legs.  A bracket quoted at the reference "
                       "point is not the bracket that matters."}


def w3_shape(J=400):
    col, A, dom, cod = setup(J, *REF)
    scored = []
    for name, g in smooth_family(col.theta, cod.w, n_centre=30, n_step=40):
        g = g.copy()
        g[0] = 0.0
        n = cod(g)
        if n > 0:
            scored.append((dom(A @ g) / n, name))
    scored.sort(reverse=True)
    best_name = scored[0][1]
    gbest = None
    for name, g in smooth_family(col.theta, cod.w, n_centre=30, n_step=40):
        if name == best_name:
            gbest = g.copy()
            gbest[0] = 0.0
            break
    h = A @ gbest
    idx = np.unique(np.linspace(0, J - 1, 120).astype(int))
    return {"J": J, "top": [{"name": n, "ratio": v} for v, n in scored[:8]],
            "theta": col.theta[idx].tolist(), "X": col.X[idx].tolist(),
            "g": (gbest[idx] * cod.w[idx]).tolist(),
            "image": (h[idx] * dom.w[idx]).tolist(),
            "reading": "the extremizer is a WIDE, FAR-FIELD-supported, "
                       "slowly-varying shape -- the opposite of the grid-scale "
                       "sign patterns earlier legs used, and consistent with "
                       "every other thing this project has learned about where "
                       "the difficulty lives (v2's far-field degeneracy, v3's "
                       "resonance, v6's X0 matching radius)."}


def w4_map(points=((1.2, 0.15), (1.4, 0.15), (1.4, 0.35), (1.5, 0.5),
                   (1.6, 0.25), (1.8, 0.15)), J=400):
    rows = []
    for a, g in points:
        col, A, dom, cod = setup(J, a, g)
        fam = family_lower(A, dom, cod, col.theta, n_centre=24, n_step=30)
        up, C_sup = upper(A, dom, cod, a, g)
        rows.append({"alpha": a, "gamma": g, "lower": fam["lower"], "upper": up,
                     "bracket": up / fam["lower"], "C_sup": C_sup,
                     "sign_patterns": sign_pattern_lower(A, dom, cod)["lower"]})
    return {"J": J, "rows": rows}


def w5_verdict(w2, w4):
    op = w2["ladder"][-1]
    a, g = OP
    col, A, dom, cod = setup(400, a, g)
    hh = hilbert_holder_constant(a, g, n_theta=32, n_d=18, n_quad=300)
    w = weighted_sups(pointwise_curves(a, g, rho=1.0, n_theta=90, n_quad=300), a)
    cq = quadratic_constant_full(a, g, w["cq_sup"], w["cq_semi"],
                                 hh["b_sup"], hh["b_semi"])["C_Q_full"]
    Z2_now = 2.0 * op["upper"] * cq
    Z2_best = 2.0 * op["lower"] * cq
    return {"operating_point": list(OP),
            "A_upper": op["upper"], "A_lower": op["lower"],
            "bracket": op["bracket"], "C_Q_full": cq,
            "Y0_now": budget(0.0, 0.0, 0.5, Z2_now)["Y0_max"],
            "Y0_if_A_were_sharp": budget(0.0, 0.0, 0.5, Z2_best)["Y0_max"],
            "GA_residual_floor": 1e-2,
            "verdict": "A PERFECT upper bound on ||A|| -- one that reached the "
                       "adversary exactly -- would multiply the conditional "
                       "budget by the bracket and no more.  That is now a "
                       "MEASURED ceiling on what any amount of further "
                       "sharpening of ||A|| can buy, which is exactly the number "
                       "no earlier leg could quote.  It is still an over-estimate "
                       "of the achievable gain, because the true norm is "
                       "somewhere inside the bracket rather than at its bottom, "
                       "and C_Q's own slack is not included."}


def w6_ledger():
    return {
        "bounded": 7, "total": 10,
        "note": "coverage unchanged by this leg; what changed is that the "
                "bracket on the dominant constant is now interpretable",
        "next": [
            "C_sup (the two-point dual): elasticity ~1 (v9 Y5), untouched since "
            "v6, and now with a measured ceiling on what sharpening it can buy",
            "the core<->far cutoff commutator [H, phi] (the last structural "
            "piece of Z1)",
            "the change of ansatz h = (1+X^2)^{-alpha/2} p(theta) (v7 V6)",
            "the core discretization error (v4 W6)",
        ],
    }


def main():
    data = {"meta": {
        "leg": "P2 Route-D v10 (a lower bound on ||A|| worth reading)",
        "tier": "Level-1 tooling + bounds (NOT a certificate)",
        "reference_point": list(REF), "operating_point": list(OP),
        "reproduce": "python experiments/p2_route_d_v10_lower.py",
        "arithmetic": "plain float64; every lower bound is the exact ratio "
                      "||A g||_X / ||g||_Y for an explicit g, so it is valid by "
                      "construction -- the question is only how good the g is",
    }}
    data["w1_ladder"] = w1_ladder()
    data["w2_operating"] = w2_operating()
    data["w3_shape"] = w3_shape()
    data["w4_map"] = w4_map()
    data["w5_verdict"] = w5_verdict(data["w2_operating"], data["w4_map"])
    data["w6_ledger"] = w6_ledger()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))

    r = data["w1_ladder"]["ladder"][1]
    o = data["w2_operating"]["ladder"][-1]
    v = data["w5_verdict"]
    print("\nP2 ROUTE-D v10 -- a lower bound worth reading\n" + "=" * 60)
    print("  W1  reference (1.5,0.5) J=400: sign patterns %.3f -> family %.3f "
          "(%s); bracket %.0fx -> %.0fx"
          % (r["sign_patterns"], r["lower"], r["argmax"], r["bracket_old"],
             r["bracket"]))
    print("  W2  OPERATING (1.4,0.15) J=%d: %.3f <= ||A|| <= %.2f  (bracket %.1fx)"
          % (o["J"], o["lower"], o["upper"], o["bracket"]))
    print("  W3  extremizer: %s" % data["w3_shape"]["top"][0]["name"])
    print("  W4  brackets across the map: %s"
          % ", ".join("(%.1f,%.2f) %.1fx" % (q["alpha"], q["gamma"], q["bracket"])
                      for q in data["w4_map"]["rows"]))
    print("  W5  budget now %.2e; ceiling if ||A|| were SHARP %.2e (GA floor %.0e)"
          % (v["Y0_now"], v["Y0_if_A_were_sharp"], v["GA_residual_floor"]))
    print("\n[done] wrote %s" % OUT)


if __name__ == "__main__":
    main()
