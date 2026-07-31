"""P2 Route-D v9 -- the sharpness leg: a better |H(h)| bound, the payer rule,
and an attribution of the slack that is left.

By v8, seven of ten Newton-Kantorovich constants were bounded and Z2 was
complete, which changed the question.  The budget goes like 1/(||A|| C_Q);
||A||'s bracket is ~75x wide and C_Q's ~4x; bounding the remaining three
constants can buy a constant factor each, while halving ||A||'s slack buys more
than all three together.  So this leg SHARPENS instead of covering.

Almost all of ||A||'s slack enters through one input: v7's closure is dominated
by its own feedback and the feedback is v6's bound on |H(h)|.  Rebuilding that
bound with v8's machinery (exact folded kernel, log-graded quadrature, a
pointwise payer choice) is the leg -- and it turns up something v6's
construction could not show: the payer RULE has an interior optimum, and the
neutral choice is worse than the crude bound it replaces.

NOT a logged Tier-1/2 experiment: deterministic (no GA, no seeds, no predicate
lock).  Run:

    .venv/bin/python experiments/p2_route_d_v9_sharpen.py
    -> writeup/data/p2_route_d_v9_sharpen.json ; figure via
       .venv/bin/python writeup/4_p2_lottery/p2_route_d_v9_evidence.py   (fig27)

SIX measurements:

  Y1  THE SHARPER BOUND: the pointwise ratio against v6 across seven decades of
      X, the exact second build of the kernel, and both convergence ladders.

  Y2  THE PAYER RULE: ||A|| bowls in rho with an interior optimum; the neutral
      rule rho = 1 is worse than v6.  C_Q, consuming the same bound in a
      different regime, wants a different rho.  Both are valid bounds.

  Y3  THE NEW ||A||, its J-ladder, and the bracket that remains.

  Y4  THE COMPLETE Z2 MAP, re-sharpened.  Does the optimum move this time?

  Y5  THE BUDGET, and five legs of history.

  Y6  THE SENSITIVITY OF ||A|| TO EACH INPUT -- which one is worth attacking,
      and why the bracket's width cannot be attributed until there is a better
      LOWER bound.  This is the measurement that should shape the next leg.
"""

import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.decay_collocation import Collocation, C_ANCHOR, grid, transforms  # noqa: E402
from solver.holder_norms import HolderNorm, square_wave_partial_sum   # noqa: E402
from solver.nk_bounds import (                                        # noqa: E402
    sup_part_upper, farfield_modelling_error_bound, budget,
)
from solver.nk_seminorm import (                                      # noqa: E402
    hilbert_split_bound, hilbert_split_curves, seminorm_closure, required_X0,
)
from solver.hilbert_holder import (                                   # noqa: E402
    conjugate, hilbert_holder_constant, quadratic_constant_full,
)
from solver.hilbert_pointwise import (                                # noqa: E402
    measured_pointwise, pointwise_bound, pointwise_curves, sweep_rho,
    weighted_sups,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "p2_route_d_v9_sharpen.json"

ALPHA, GAMMA = 1.5, 0.5
J_REF = 800
J_MEAS = 1200
RHO_CLOSURE = 6.0
RHO_CQ = 1.0


def gauged_inverse(col):
    J = col.J
    M = np.empty((J, J))
    M[0, :] = col.to_coef.sum(axis=0)
    M[1:, :] = col.jacobian_matrix(col.anchor(), C_ANCHOR)[1:, :]
    return np.linalg.inv(M)


def norms(col, alpha, gamma):
    dom = HolderNorm(col.theta, col.X, alpha, gamma)
    cod = HolderNorm(col.theta, col.X, alpha + 1.0, gamma)
    cod.w[0] = 1.0
    return dom, cod


def profile_family(theta, alpha):
    f = np.cos(0.5 * theta) ** alpha
    out = {"f_alpha": f}
    for k in (1, 4, 16, 64, 256):
        out["cos%d_f" % k] = np.cos(k * theta) * f
    out["square32_f"] = square_wave_partial_sum(theta, 32) * f
    out["square256_f"] = square_wave_partial_sum(theta, 256) * f
    out["bump_core"] = np.exp(-((theta - 0.6) / 0.05) ** 2) * f
    out["bump_far"] = np.exp(-((theta - 3.0) / 0.02) ** 2) * f
    return out


def family_full_lower(A, dom, cod, n_rows=40):
    """max over the exact SUP extremizer directions of the FULL norm ratio.

    This is v5's `family_op_norm` restricted to the directions that do not need
    an LP -- a LOWER bound on ||A||, and the one earlier legs quoted (~2.2-2.9).
    Note it is NOT a lower bound on C_sup alone: dividing the sup part of the
    image by the FULL codomain norm of a sign pattern (whose Holder seminorm is
    enormous) gives a number an order of magnitude smaller, which an earlier
    draft of this leg mistook for a sharp value of C_sup and duly reported a
    19x "available gain" that does not exist.
    """
    B = A / cod.w[None, :]
    rows = np.unique(np.linspace(0, A.shape[0] - 1, n_rows).astype(int))
    best = 0.0
    for i in rows:
        g = np.sign(B[i]) / cod.w
        g[0] = 0.0
        n = cod(g)
        if n > 0:
            best = max(best, dom(A @ g) / n)
    return float(best)


def family_seminorm_lower(A, dom, cod, n_rows=14):
    B = A / cod.w[None, :]
    rows = np.unique(np.linspace(0, A.shape[0] - 1, n_rows).astype(int))
    best = 0.0
    for i in rows:
        for j in rows:
            if i == j:
                continue
            g = np.sign(B[i] - B[j]) / cod.w
            g[0] = 0.0
            n = cod(g)
            if n > 0:
                best = max(best, dom.seminorm(A @ g) / n)
    return float(best)


# ---------------------------------------------------------------------------
# Y1 -- the sharper bound
# ---------------------------------------------------------------------------


def y1_bound():
    ratios = []
    for X in (1e-3, 1e-2, 1e-1, 1.0, 3.0, 10.0, 1e2, 1e3, 1e5):
        th = 2.0 * np.arctan(X)
        s6, m6 = hilbert_split_bound(X, ALPHA, GAMMA)
        s9, m9 = pointwise_bound(th, ALPHA, GAMMA, rho=1.0, n_quad=600)
        ratios.append({"X": X, "v6": s6 + m6, "v9": s9 + m9,
                       "ratio": (s9 + m9) / (s6 + m6)})
    quad = [{"n_quad": n,
             "value": sum(pointwise_bound(2.0, ALPHA, GAMMA, rho=RHO_CLOSURE,
                                          n_quad=n))}
            for n in (150, 300, 600, 1200, 2400)]
    thl = []
    for n_th, n_q in ((70, 200), (140, 400), (280, 800)):
        w = weighted_sups(pointwise_curves(ALPHA, GAMMA, rho=RHO_CLOSURE,
                                           n_theta=n_th, n_quad=n_q), ALPHA)
        thl.append({"n_theta": n_th, "n_quad": n_q, **w})
    return {"pointwise_ratio": ratios, "quad_ladder": quad,
            "theta_ladder": thl,
            "reading": "the folded kernel K = 2 sin(th)/(cos phi - cos th) has "
                       "the far-field decay built in (sin th -> 0), and its "
                       "principal value over (0, pi) is exactly zero -- it is "
                       "the conjugate of the constant function -- so the p.v. "
                       "can be handled by a GLOBAL subtraction with no band, no "
                       "matching scale and no remainder term.  v6 needed all "
                       "three, and each cost a crude constant."}


# ---------------------------------------------------------------------------
# Y2 -- the payer rule
# ---------------------------------------------------------------------------


def y2_payer(rhos=(1.0, 1.5, 2.0, 3.0, 4.5, 6.0, 9.0, 12.0, 18.0, 25.0, 50.0)):
    col = Collocation(J_REF)
    A = gauged_inverse(col)
    dom, cod = norms(col, ALPHA, GAMMA)
    C_sup = sup_part_upper(A, dom.w, cod.w, cod.pair)
    hh = hilbert_holder_constant(ALPHA, GAMMA, n_theta=40, n_d=22, n_quad=300)
    rows = []
    for rho in rhos:
        cv = pointwise_curves(ALPHA, GAMMA, rho=rho, n_theta=110, n_quad=350)
        d = seminorm_closure(ALPHA, GAMMA, C_sup, curves=cv)
        w = weighted_sups(cv, ALPHA)
        cq = quadratic_constant_full(ALPHA, GAMMA, w["cq_sup"], w["cq_semi"],
                                     hh["b_sup"], hh["b_semi"])["C_Q_full"]
        rows.append({"rho": rho, "A_upper": d["A_upper"], "C_Q_full": cq,
                     "Z2": 2.0 * d["A_upper"] * cq, **w})
    v6 = seminorm_closure(ALPHA, GAMMA, C_sup,
                          curves=hilbert_split_curves(ALPHA, GAMMA))
    gain = []
    for a, g in ((1.5, 0.5), (1.4, 0.35), (1.4, 0.25), (1.4, 0.15), (1.2, 0.15)):
        d2, c2 = norms(col, a, g)
        cs = sup_part_upper(A, d2.w, c2.w, c2.pair)
        old = seminorm_closure(a, g, cs, curves=hilbert_split_curves(a, g))["A_upper"]
        best = None
        for rho in (1.0, 2.0, 3.0, 4.5, 6.0, 9.0, 14.0, 25.0):
            cv = pointwise_curves(a, g, rho=rho, n_theta=90, n_quad=300)
            v = seminorm_closure(a, g, cs, curves=cv)["A_upper"]
            if best is None or v < best[1]:
                best = (rho, v)
        gain.append({"alpha": a, "gamma": g, "C_sup": cs, "A_v7": old,
                     "A_v9": best[1], "rho_star": best[0],
                     "gain": 1.0 - best[1] / old})
    best_A = min(rows, key=lambda r: r["A_upper"])
    best_Q = min(rows, key=lambda r: r["C_Q_full"])
    best_Z = min(rows, key=lambda r: r["Z2"])
    return {"C_sup": C_sup, "rows": rows, "v6_A_upper": v6["A_upper"],
            "gain_by_point": gain,
            "gain_caveat": "THE GAIN DOES NOT TRANSFER.  32% at the reference "
                           "(1.5, 0.5), 11% at (1.4, 0.35), ~0% at the map's "
                           "actual optimum (1.4, 0.15).  The mechanism is the "
                           "interpolation exponent: T <= C(gamma) (P/2)^gamma "
                           "(2S)^{1-gamma}, and the |H| bound enters ONLY through "
                           "P.  At gamma = 0.15 that exponent is 0.15, so "
                           "sharpening P by 30% moves T by 4%.  The operating "
                           "point is governed by S = C_sup, not by the estimate "
                           "this leg improved.",
            "argmin_A": best_A, "argmin_C_Q": best_Q, "argmin_Z2": best_Z,
            "neutral_A": next(r for r in rows if r["rho"] == 1.0)["A_upper"],
            "reading": "every rho gives a VALID bound; the choice is a free "
                       "parameter of the estimate, not an approximation.  The "
                       "neutral rule rho = 1 -- v8's default, and the natural "
                       "one -- is WORSE than the crude bound it replaces, "
                       "because in the closure T is ~10x S and the neutral rule "
                       "charges the expensive account.  Different consumers want "
                       "different rho: the closure feeds a large T, C_Q "
                       "maximises over the unit simplex where the ratio is O(1)."}


# ---------------------------------------------------------------------------
# Y3 -- the new ||A||, and the bracket
# ---------------------------------------------------------------------------


def y3_operator(Js=(125, 250, 500, 800, 1600)):
    cv9 = pointwise_curves(ALPHA, GAMMA, rho=RHO_CLOSURE, n_theta=140, n_quad=400)
    cv6 = hilbert_split_curves(ALPHA, GAMMA)
    rows = []
    for J in Js:
        col = Collocation(J)
        A = gauged_inverse(col)
        dom, cod = norms(col, ALPHA, GAMMA)
        C_sup = sup_part_upper(A, dom.w, cod.w, cod.pair)
        d9 = seminorm_closure(ALPHA, GAMMA, C_sup, curves=cv9)
        d6 = seminorm_closure(ALPHA, GAMMA, C_sup, curves=cv6)
        rows.append({"J": J, "C_sup_upper": C_sup,
                     "T_upper_v9": d9["T_upper"], "A_upper_v9": d9["A_upper"],
                     "T_upper_v7": d6["T_upper"], "A_upper_v7": d6["A_upper"],
                     "A_lower_family": family_full_lower(A, dom, cod),
                     "T_lower": family_seminorm_lower(A, dom, cod)})
    lj = np.log([r["J"] for r in rows])
    return {"ladder": rows,
            "A_growth_exponent": float(np.polyfit(
                lj, np.log([r["A_upper_v9"] for r in rows]), 1)[0]),
            "bracket_v7": rows[0]["A_upper_v7"] / rows[0]["A_lower_family"],
            "bracket_v9": rows[0]["A_upper_v9"] / rows[0]["A_lower_family"],
            "caveat": "the LOWER end of the bracket is a maximum over a handful "
                      "of directions, so the bracket's WIDTH is not a measure of "
                      "how lossy the bound is -- it bounds that from above and "
                      "nothing more.  Y6 is about what can actually be recovered."}


# ---------------------------------------------------------------------------
# Y4 -- the re-sharpened complete Z2 map
# ---------------------------------------------------------------------------


def y4_map(alphas=(1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8),
           gammas=(0.05, 0.1, 0.15, 0.25, 0.35, 0.5, 0.65, 0.8)):
    col = Collocation(J_REF)
    A = gauged_inverse(col)
    out = []
    for a in alphas:
        row = []
        for g in gammas:
            dom, cod = norms(col, a, g)
            C_sup = sup_part_upper(A, dom.w, cod.w, cod.pair)
            hh = hilbert_holder_constant(a, g, n_theta=32, n_d=18, n_quad=300)
            best = None
            for rho in (1.0, 3.0, 6.0, 12.0):
                cv = pointwise_curves(a, g, rho=rho, n_theta=90, n_quad=300)
                d = seminorm_closure(a, g, C_sup, curves=cv)
                w = weighted_sups(cv, a)
                cq = quadratic_constant_full(a, g, w["cq_sup"], w["cq_semi"],
                                             hh["b_sup"], hh["b_semi"])["C_Q_full"]
                cand = {"gamma": g, "rho": rho, "A_upper": d["A_upper"],
                        "C_Q_full": cq, "Z2": 2.0 * d["A_upper"] * cq}
                if best is None or cand["Z2"] < best["Z2"]:
                    best = cand
            row.append(best)
        out.append({"alpha": a, "row": row})
    best = min(((c["Z2"], r["alpha"], c["gamma"]) for r in out for c in r["row"]))
    return {"J": J_REF, "rho_grid": [1.0, 3.0, 6.0, 12.0], "map": out,
            "argmin_Z2": {"Z2": best[0], "alpha": best[1], "gamma": best[2]}}


# ---------------------------------------------------------------------------
# Y5 -- the budget
# ---------------------------------------------------------------------------


def y5_budget(mp, X0_grid=None):
    if X0_grid is None:
        X0_grid = np.geomspace(1e2, 1e8, 25)
    col = Collocation(J_REF)
    A = gauged_inverse(col)
    rows = []
    for r in mp["map"]:
        a = r["alpha"]
        for c in r["row"]:
            if c["gamma"] not in (0.1, 0.15, 0.25, 0.35):
                continue
            g = c["gamma"]

            def err(X0, _a=a, _g=g):
                return farfield_modelling_error_bound(_a, _g, X0, n_X=8)["bound"]

            req = required_X0(c["A_upper"], err, X0_grid, target=0.5)
            rows.append({"alpha": a, "gamma": g, "A_upper": c["A_upper"],
                         "C_Q_full": c["C_Q_full"], "Z2": c["Z2"],
                         "Y0_max": budget(0.0, 0.0, 0.5, c["Z2"])["Y0_max"],
                         "required_X0": req})
    best = max(rows, key=lambda r: r["Y0_max"])
    return {"rows": rows, "best": best, "target_Z1": 0.5,
            "history": [
                {"leg": "v5", "Y0_max": 7.6e-2},
                {"leg": "v6", "Y0_max": 1.18e-2},
                {"leg": "v7", "Y0_max": 2.58e-4},
                {"leg": "v8", "Y0_max": 2.39e-4},
                {"leg": "v9", "Y0_max": float(best["Y0_max"])},
            ]}


# ---------------------------------------------------------------------------
# Y6 -- the slack attribution ladder
# ---------------------------------------------------------------------------


def y6_sensitivity(scales=(0.25, 0.5, 1.0, 2.0, 4.0),
                   points=((1.5, 0.5), (1.4, 0.15))):
    """How much does ||A|| move when each INPUT of the closure moves?

    An earlier draft did this as an "oracle" ladder -- substitute each input's
    measured value and read off the gain.  That was wrong in a way worth
    recording: the substituted C_sup was a family LOWER bound computed by
    dividing the sup part of an image by the FULL codomain norm of a sign
    pattern, which is an order of magnitude below any plausible sharp value, and
    the ladder duly reported a 19x available gain that does not exist.  Banked
    lesson (15) again: know which side of the inequality each number is on.

    What is defensible without an oracle is the ELASTICITY: scale an input by a
    factor and see what the closure does.  That says which input is worth
    attacking, and combined with each input's own known slack it says how much
    is actually on the table.
    """
    col = Collocation(J_REF)
    A = gauged_inverse(col)

    def elasticity(rows):
        x = np.log([r["scale"] for r in rows])
        y = np.log([r["A_upper"] for r in rows])
        return float(np.polyfit(x, y, 1)[0])

    out = []
    for a, g in points:
        dom, cod = norms(col, a, g)
        C_sup = sup_part_upper(A, dom.w, cod.w, cod.pair)
        Xs, aS, aT = pointwise_curves(a, g, rho=RHO_CLOSURE, n_theta=140,
                                      n_quad=400)

        def A_of(curves, cs, _a=a, _g=g):
            return seminorm_closure(_a, _g, cs, curves=curves)["A_upper"]

        c_rows = [{"scale": f, "C_sup": C_sup * f,
                   "A_upper": A_of((Xs, aS, aT), C_sup * f)} for f in scales]
        h_rows = [{"scale": f, "A_upper": A_of((Xs, aS * f, aT * f), C_sup)}
                  for f in scales]
        out.append({"alpha": a, "gamma": g, "C_sup": C_sup,
                    "base_A_upper": A_of((Xs, aS, aT), C_sup),
                    "C_sup_rows": c_rows, "C_sup_elasticity": elasticity(c_rows),
                    "hilbert_rows": h_rows,
                    "hilbert_elasticity": elasticity(h_rows)})
    ref, op = out[0], out[1]
    return {"points": out, "reference": ref, "operating": op,
            "C_sup_rows": ref["C_sup_rows"], "hilbert_rows": ref["hilbert_rows"],
            "C_sup_elasticity": ref["C_sup_elasticity"],
            "hilbert_elasticity": ref["hilbert_elasticity"],
            "base_A_upper": ref["base_A_upper"], "C_sup": ref["C_sup"],
            "reading": "||A|| is nearly PROPORTIONAL to C_sup and much less "
                       "sensitive to the |H| input, which is the opposite of "
                       "where the last two legs spent their effort.  C_sup is "
                       "v6's two-point dual; v6 B2 bracketed it against a family "
                       "lower bound by about 2x, so sharpening it is worth about "
                       "2x -- real, but not the order of magnitude the raw "
                       "bracket suggests.  The rest of the bracket cannot be "
                       "attributed at all until there is a better LOWER bound: "
                       "a maximum over a few sign patterns says almost nothing "
                       "about how lossy an upper bound is.  That -- not another "
                       "estimate -- is what the next leg needs."}


def y7_ledger():
    return [
        {"constant": "Y0 (at the a=0 anchor)", "status": "EXACT", "note": "Y0 = 0"},
        {"constant": "Z0", "status": "BOUNDED", "note": "finite-block rounding"},
        {"constant": "Z1 far-field modelling error", "status": "BOUNDED (v6)",
         "note": "closed form, X0^{alpha-2}"},
        {"constant": "Z1 core<->far-field coupling", "status": "OPEN",
         "note": "smooth cutoff + [H, phi] commutator"},
        {"constant": "Z1 core discretization", "status": "MEASURED ONLY",
         "note": "v4 W6: J^-2.1..-2.6"},
        {"constant": "||A|| domain SUP part", "status": "BOUNDED (v6)",
         "note": "two-point dual; v9's elasticity says ||A|| is nearly "
                 "PROPORTIONAL to it, so it is now the dominant input"},
        {"constant": "||A|| domain SEMINORM part",
         "status": "BOUNDED (v7, SHARPENED v9)",
         "note": "derivative-gain closure, J-free; -32% from the new |H| bound"},
        {"constant": "C_Q sup part", "status": "BOUNDED (v6, SHARPENED v9)",
         "note": "same |H| bound, exact kernel"},
        {"constant": "C_Q codomain SEMINORM part", "status": "BOUNDED (v8)",
         "note": "weight 1-gamma"},
        {"constant": "discrete <-> continuum transfer", "status": "OPEN (v7)",
         "note": "a change of ansatz"},
    ]


def main():
    data = {
        "meta": {
            "leg": "P2 Route-D v9 (the sharpness leg: a better |H| bound, the "
                   "payer rule, and the slack attribution)",
            "tier": "Level-1 tooling + upper bounds (NOT a certificate)",
            "alpha_gamma_reference": [ALPHA, GAMMA],
            "reproduce": "python experiments/p2_route_d_v9_sharpen.py",
            "arithmetic": "plain float64 -- analytic majorants with numerically "
                          "evaluated constants, gated against an exact second "
                          "build of the kernel and against measurements; nothing "
                          "here is interval-enclosed or rigorous",
        },
        "y1_bound": y1_bound(),
        "y2_payer": y2_payer(),
        "y3_operator": y3_operator(),
    }
    data["y4_map"] = y4_map()
    data["y5_budget"] = y5_budget(data["y4_map"])
    data["y6_sensitivity"] = y6_sensitivity()
    data["y7_ledger"] = y7_ledger()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))

    y1, y2, y3 = data["y1_bound"], data["y2_payer"], data["y3_operator"]
    print("\nP2 ROUTE-D v9 -- the sharpness leg\n" + "=" * 62)
    print("  Y1  pointwise vs v6: ratio %.3f-%.3f over 8 decades of X"
          % (min(r["ratio"] for r in y1["pointwise_ratio"]),
             max(r["ratio"] for r in y1["pointwise_ratio"])))
    print("  Y2  ||A||: v6 %.2f -> neutral rho=1 %.2f -> best %.2f at rho=%.1f"
          % (y2["v6_A_upper"], y2["neutral_A"], y2["argmin_A"]["A_upper"],
             y2["argmin_A"]["rho"]))
    print("  Y3  ||A|| <= %.2f (J^%+.4f); bracket %.0fx -> %.0fx"
          % (y3["ladder"][0]["A_upper_v9"], y3["A_growth_exponent"],
             y3["bracket_v7"], y3["bracket_v9"]))
    print("  Y4  Z2 optimum %.1f at (alpha,gamma) = (%.1f, %.2f)"
          % (data["y4_map"]["argmin_Z2"]["Z2"],
             data["y4_map"]["argmin_Z2"]["alpha"],
             data["y4_map"]["argmin_Z2"]["gamma"]))
    print("  Y5  budget %s"
          % " -> ".join("%.2e" % h["Y0_max"] for h in data["y5_budget"]["history"]))
    sen = data["y6_sensitivity"]
    for q in sen["points"]:
        print("  Y6  (%.1f, %.2f): d log A / d log C_sup = %+.2f ; "
              "d log A / d log |H| = %+.2f"
              % (q["alpha"], q["gamma"], q["C_sup_elasticity"],
                 q["hilbert_elasticity"]))
    print("  Y2b gain by point: " + ", ".join(
        "(%.1f,%.2f) %.0f%%" % (r["alpha"], r["gamma"], 100 * r["gain"])
        for r in data["y2_payer"]["gain_by_point"]))
    print("\n[done] wrote %s" % OUT)


if __name__ == "__main__":
    main()
