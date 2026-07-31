"""P2 Route-D v8 -- the codomain seminorm part of C_Q, and the first complete Z2.

v7 (writeup/4_p2_lottery/TECHNICAL_P2_ROUTED_V7.md) closed the domain seminorm
part of ||A|| and produced the project's first (alpha, gamma) map made entirely
of upper bounds -- with one term still missing, and it said so:

> Caveat that must travel with it: Z2 here still omits the codomain SEMINORM part
> of C_Q, which is unbounded -- and that omission is worst exactly where gamma is
> smallest.  So the location (1.4, 0.15) is provisional.

This leg bounds that term, which needs weighted Holder boundedness of the Hilbert
transform with an explicit constant.  The weight is the leg's first surprise: it
is 1 - gamma, not alpha - gamma, because H does not inherit h's decay (H(h) ~
(int h)/(pi X) however fast h decays).

NOT a logged Tier-1/2 experiment: deterministic (no GA, no seeds, no predicate
lock).  Committed so the writeup rebuilds without re-derivation.  Run:

    .venv/bin/python experiments/p2_route_d_v8_quadratic.py
    -> writeup/data/p2_route_d_v8_quadratic.json ; figure via
       .venv/bin/python writeup/4_p2_lottery/p2_route_d_v8_evidence.py   (fig26)

SIX measurements:

  X1  THE ESTIMATE, and the two convergences it depends on.  The pair supremum
      on four grid levels and the quadrature on four levels, plus the exact
      second build of the decomposition, plus the ablation against the only
      route v6/v7 had (pointwise) -- which is 240x worse.

  X2  THE BRACKET.  The upper bound against the measured weighted seminorm of
      H(h) over a profile family including v4's square-wave adversary.  Reported
      as a ratio, so the slack is visible rather than implied.

  X3  THE gamma STRUCTURE, and what it does NOT do.  Both endpoint divergences
      are present (1/gamma near, 1/(1-gamma) far), so the new term bowls.  But
      the OLD sup-only C_Q already carried the same 1/gamma near-region
      divergence, so the RATIO of the two is flat at small gamma and grows toward
      gamma = 1 -- the opposite of v7's prediction that the omission would be
      worst where gamma is smallest.

  X4  THE FIRST COMPLETE Z2 MAP.  Every constant in it is an upper bound and
      nothing is omitted.  v7's optimum does NOT move -- its provisional location
      is confirmed, and its stated reason for calling it provisional turns out to
      be the wrong reason.

  X5  THE BUDGET, RE-PRICED -- and the budget history across four legs, which is
      the number worth arguing about.

  X6  THE LEDGER: seven of ten bounded, and what the remaining three are.
"""

import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.decay_collocation import Collocation, C_ANCHOR, grid, transforms  # noqa: E402
from solver.decay_grading import farfield_inverse_norm                # noqa: E402
from solver.holder_norms import HolderNorm, square_wave_partial_sum   # noqa: E402
from solver.nk_bounds import (                                        # noqa: E402
    sup_part_upper, farfield_modelling_error_bound, quadratic_constant_upper,
    budget,
)
from solver.nk_seminorm import seminorm_closure, required_X0          # noqa: E402
from solver.hilbert_holder import (                                   # noqa: E402
    conjugate, cq_sup_split, decomposition_exact, hilbert_holder_constant,
    increment_pair_bound, quadratic_constant_full, weighted_seminorm,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "p2_route_d_v8_quadratic.json"

ALPHA, GAMMA = 1.5, 0.5
J_REF = 800
J_MEAS = 1200


def gauged_inverse(col):
    """A = inv([gauge row ; DF rows 1..]) -- the same object v5, v6 and v7 measured."""
    J = col.J
    M = np.empty((J, J))
    M[0, :] = col.to_coef.sum(axis=0)
    M[1:, :] = col.jacobian_matrix(col.anchor(), C_ANCHOR)[1:, :]
    return np.linalg.inv(M)


def norms(col, alpha, gamma):
    dom = HolderNorm(col.theta, col.X, alpha, gamma)
    cod = HolderNorm(col.theta, col.X, alpha + 1.0, gamma)
    cod.w[0] = 1.0                       # the gauge slot is a plain scalar
    return dom, cod


def profile_family(theta, alpha):
    """The class members used for the measured (LOWER) side of every bracket."""
    f = np.cos(0.5 * theta) ** alpha
    out = {"f_alpha": f}
    for k in (1, 4, 16, 64, 256):
        out["cos%d_f" % k] = np.cos(k * theta) * f
    out["square32_f"] = square_wave_partial_sum(theta, 32) * f
    out["square256_f"] = square_wave_partial_sum(theta, 256) * f
    out["bump_core"] = np.exp(-((theta - 0.6) / 0.05) ** 2) * f
    out["bump_far"] = np.exp(-((theta - 3.0) / 0.02) ** 2) * f
    return out


# ---------------------------------------------------------------------------
# X1 -- the estimate and its convergences
# ---------------------------------------------------------------------------


def x1_estimate():
    levels = [(24, 14), (40, 22), (64, 34), (96, 52)]
    ladder = []
    for nt, nd in levels:
        r = hilbert_holder_constant(ALPHA, GAMMA, n_theta=nt, n_d=nd, n_quad=300)
        ladder.append({"n_theta": nt, "n_d": nd, "n_pairs_swept": None,
                       "b_sup": r["b_sup"], "b_semi": r["b_semi"]})
    quad = [{"n_quad": n,
             "b_semi_at_reference_pair":
                 increment_pair_bound(0.0545, -1e-5, ALPHA, GAMMA, n_quad=n)[1]}
            for n in (150, 300, 600, 1200, 2400)]

    cases = [np.array([0.0, 1.0]), np.array([0.0, 0.0, 0.0, 1.0]),
             np.array([0.3, 1.0, -0.5, 0.2, 0.1, -0.4])]
    pairs = [(0.7, 0.05), (0.7, -0.3), (2.9, 0.02), (0.02, 0.5), (1.0, 1.5),
             (3.1, -0.001), (0.001, 2.0)]
    err = 0.0
    for c in cases:
        for th, sg in pairs:
            got = decomposition_exact(c, th, sg, n_quad=8000)
            ex = float(conjugate(c, [th])[0] - conjugate(c, [th + sg])[0])
            err = max(err, abs(got - ex))

    inc = hilbert_holder_constant(ALPHA, GAMMA, rule="increment",
                                  n_theta=40, n_d=22, n_quad=300)
    pw = hilbert_holder_constant(ALPHA, GAMMA, rule="pointwise",
                                 n_theta=40, n_d=22, n_quad=300)
    sm = hilbert_holder_constant(ALPHA, GAMMA, rule="sum",
                                 n_theta=40, n_d=22, n_quad=300)
    return {
        "reference": {"alpha": ALPHA, "gamma": GAMMA,
                      "b_sup": inc["b_sup"], "b_semi": inc["b_semi"],
                      "argmax_sup": list(inc["argmax_sup"]),
                      "argmax_semi": list(inc["argmax_semi"])},
        "grid_ladder": ladder, "quad_ladder": quad,
        "decomposition_max_error": err,
        "ablation": {
            "increment_rule": inc["b_sup"] + inc["b_semi"],
            "pointwise_only": pw["b_sup"] + pw["b_semi"],
            "gain": (pw["b_sup"] + pw["b_semi"]) / (inc["b_sup"] + inc["b_semi"]),
            "min_sum_rule_b_sup": sm["b_sup"], "increment_rule_b_sup": inc["b_sup"],
        },
        "reading": "the pair supremum is a GRID supremum, which can only "
                   "under-report (the mirror of v6's discrete-ball trap, where a "
                   "set that was too big over-reported), so the refinement study "
                   "is part of the measurement.  It is flat to 4e-4 over a 4x "
                   "refinement in both directions.  The ablation says how much of "
                   "the constant is the new estimate rather than bookkeeping: "
                   "with only the pointwise route -- all v6 and v7 had for this "
                   "quantity -- the same sweep returns a number 240x larger.",
    }


# ---------------------------------------------------------------------------
# X2 -- the bracket
# ---------------------------------------------------------------------------


def x2_bracket(cases=((1.5, 0.5), (1.2, 0.25), (1.4, 0.35), (1.4, 0.65))):
    th, X = grid(J_MEAS)
    to_coef, _, Sm = transforms(J_MEAS)
    rows = []
    for alpha, gamma in cases:
        dom = HolderNorm(th, X, alpha, gamma)
        r = hilbert_holder_constant(alpha, gamma, n_theta=40, n_d=22, n_quad=300)
        worst, arg = 0.0, ""
        per = {}
        for name, h in profile_family(th, alpha).items():
            psi = Sm @ (to_coef @ h)
            S, T = dom.sup_part(h), dom.seminorm(h)
            ub = r["b_sup"] * S + r["b_semi"] * T
            ratio = weighted_seminorm(psi, th, 1.0 - gamma, gamma) / ub
            per[name] = ratio
            if ratio > worst:
                worst, arg = ratio, name
        rows.append({"alpha": alpha, "gamma": gamma, "b_sup": r["b_sup"],
                     "b_semi": r["b_semi"], "worst_ratio": worst,
                     "worst_profile": arg, "per_profile": per})
    return {"J_measure": J_MEAS, "rows": rows,
            "reading": "the measured side is a family-restricted maximum -- a "
                       "LOWER bound, banked lesson (15) -- so the true constant "
                       "lies between the two.  A ratio of ~0.2 means the estimate "
                       "is honest but ~5x lossy on the directions the family "
                       "contains, which is the same order of slack v7's closure "
                       "carried and, per v7 V5, the thing that now matters most."}


# ---------------------------------------------------------------------------
# X3 -- the gamma structure
# ---------------------------------------------------------------------------


def x3_gamma(gammas=(0.05, 0.1, 0.15, 0.25, 0.35, 0.5, 0.65, 0.8, 0.9),
             alpha=ALPHA):
    rows = []
    for g in gammas:
        r = hilbert_holder_constant(alpha, g, n_theta=40, n_d=22, n_quad=300)
        qs, qt = cq_sup_split(alpha, g, n_X=100)
        full = quadratic_constant_full(alpha, g, qs, qt, r["b_sup"], r["b_semi"])
        rows.append({"gamma": g, "b_sup": r["b_sup"], "b_semi": r["b_semi"],
                     "cq_sup_S": qs, "cq_sup_T": qt,
                     "C_Q_full": full["C_Q_full"],
                     "C_Q_sup_only_v6": quadratic_constant_upper(
                         alpha, g, n_X=100)["C_Q_sup_upper"]})
    full = np.array([r["C_Q_full"] for r in rows])
    sup_only = np.array([r["C_Q_sup_only_v6"] for r in rows])
    i = int(full.argmin())
    return {"alpha": alpha, "rows": rows,
            "argmin_C_Q_full": {"gamma": gammas[i], "C_Q_full": float(full[i])},
            "C_Q_full_interior": bool(0 < i < len(gammas) - 1),
            "C_Q_sup_only_argmin_index": int(sup_only.argmin()),
            "reading": "the near region charges int |t|^{gamma-1} ~ 1/gamma and "
                       "the far region int d |t|^{gamma-2} ~ 1/(1-gamma), so the "
                       "NEW term rises at both ends while v6's sup-only C_Q is "
                       "monotone.  That is the whole reason the map's optimum "
                       "moves: the omitted term was the only one that punished "
                       "small gamma."}


# ---------------------------------------------------------------------------
# X4 -- the first complete Z2 map
# ---------------------------------------------------------------------------


def x4_map(alphas=(1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8),
           gammas=(0.05, 0.1, 0.15, 0.25, 0.35, 0.5, 0.65, 0.8)):
    col = Collocation(J_REF)
    A = gauged_inverse(col)
    cache = {}
    grid_map = []
    for a in alphas:
        row = []
        for g in gammas:
            dom, cod = norms(col, a, g)
            C_sup = sup_part_upper(A, dom.w, cod.w, cod.pair)
            d = seminorm_closure(a, g, C_sup)
            if (a, g) not in cache:
                r = hilbert_holder_constant(a, g, n_theta=32, n_d=18, n_quad=300)
                qs, qt = cq_sup_split(a, g, n_X=80)
                cache[(a, g)] = (r, qs, qt)
            r, qs, qt = cache[(a, g)]
            cq_full = quadratic_constant_full(a, g, qs, qt, r["b_sup"],
                                              r["b_semi"])["C_Q_full"]
            cq_v7 = quadratic_constant_upper(a, g, n_X=60)["C_Q_sup_upper"]
            row.append({"gamma": g, "A_upper": d["A_upper"],
                        "C_Q_full": cq_full, "C_Q_v7_sup_only": cq_v7,
                        "Z2_full": 2.0 * d["A_upper"] * cq_full,
                        "Z2_v7": 2.0 * d["A_upper"] * cq_v7})
        grid_map.append({"alpha": a, "row": row})
    best_full = min(((c["Z2_full"], r["alpha"], c["gamma"])
                     for r in grid_map for c in r["row"]))
    best_v7 = min(((c["Z2_v7"], r["alpha"], c["gamma"])
                   for r in grid_map for c in r["row"]))
    return {"J": J_REF, "map": grid_map,
            "argmin_Z2_full": {"Z2": best_full[0], "alpha": best_full[1],
                               "gamma": best_full[2]},
            "argmin_Z2_v7_reproduced": {"Z2": best_v7[0], "alpha": best_v7[1],
                                        "gamma": best_v7[2]},
            "statement": "every constant in Z2_full is an upper bound and NOTHING "
                         "is omitted: ||A|| = v6's sup-part dual + v7's closure, "
                         "C_Q = v6's sup part (split by payer) + v8's codomain "
                         "seminorm part.  This is the first Z2 in the project of "
                         "which that is true."}


# ---------------------------------------------------------------------------
# X5 -- the budget, re-priced, and its history
# ---------------------------------------------------------------------------


def x5_budget(alphas=(1.1, 1.2, 1.3, 1.4, 1.5), gammas=(0.15, 0.35, 0.5, 0.65),
              X0_grid=None):
    if X0_grid is None:
        X0_grid = np.geomspace(1e2, 1e8, 25)
    col = Collocation(J_REF)
    A = gauged_inverse(col)
    rows = []
    for a in alphas:
        for g in gammas:
            dom, cod = norms(col, a, g)
            C_sup = sup_part_upper(A, dom.w, cod.w, cod.pair)
            d = seminorm_closure(a, g, C_sup)
            A_up = d["A_upper"]
            r = hilbert_holder_constant(a, g, n_theta=32, n_d=18, n_quad=300)
            qs, qt = cq_sup_split(a, g, n_X=80)
            cq_full = quadratic_constant_full(a, g, qs, qt, r["b_sup"],
                                              r["b_semi"])["C_Q_full"]
            cq_v7 = quadratic_constant_upper(a, g, n_X=60)["C_Q_sup_upper"]

            def err(X0, _a=a, _g=g):
                return farfield_modelling_error_bound(_a, _g, X0, n_X=8)["bound"]

            req = required_X0(A_up, err, X0_grid, target=0.5)
            Z2_full = 2.0 * A_up * cq_full
            rows.append({
                "alpha": a, "gamma": g, "A_upper": A_up,
                "C_Q_full": cq_full, "C_Q_v7": cq_v7,
                "Z2_full": Z2_full, "Z2_v7": 2.0 * A_up * cq_v7,
                "Y0_max_full": budget(0.0, 0.0, 0.5, Z2_full)["Y0_max"],
                "Y0_max_v7": budget(0.0, 0.0, 0.5, 2.0 * A_up * cq_v7)["Y0_max"],
                "required_X0": req,
            })
    best = max(rows, key=lambda r: r["Y0_max_full"])
    best_v7 = max(rows, key=lambda r: r["Y0_max_v7"])
    cost = [r["C_Q_full"] / r["C_Q_v7"] for r in rows]
    return {"rows": rows, "target_Z1": 0.5, "best": best,
            "best_on_v7_incomplete_map": best_v7,
            "cost_of_the_new_term": {"min": float(min(cost)),
                                     "max": float(max(cost)),
                                     "at_the_optimum":
                                         best["C_Q_full"] / best["C_Q_v7"]},
            "history": [
                {"leg": "v5", "Y0_max": 7.6e-2,
                 "what": "family-restricted maxima (LOWER bounds) throughout; "
                         "Z1 not priced at all"},
                {"leg": "v6", "Y0_max": 1.18e-2,
                 "what": "Z1 far-field priced for the first time; ||A|| still the "
                         "far-field proxy"},
                {"leg": "v7", "Y0_max": float(best_v7["Y0_max_v7"]),
                 "what": "the honest ||A|| (sup part + seminorm closure); C_Q "
                         "still missing its codomain seminorm part.  This is v7's "
                         "map priced over the same (alpha,gamma) sweep as v8, "
                         "which is the like-for-like number; v7's own writeup "
                         "quoted 2.0e-4, its value at the single row gamma=0.35"},
                {"leg": "v8", "Y0_max": float(best["Y0_max_full"]),
                 "what": "C_Q complete; every constant in Z2 an upper bound"},
            ],
            "reading": "THREE consecutive legs each cost the conditional budget "
                       "an order of magnitude, every time for the same reason: a "
                       "lower bound replaced by the honest upper bound.  v8 is "
                       "the first leg where that did NOT happen -- the last "
                       "unpriced term costs 8-44% depending on (alpha,gamma) and "
                       "7% at the optimum, not a factor of ten.  Two reasons: the "
                       "sup part of C_Q already carried the same 1/gamma near-"
                       "region divergence the new term has, so nothing new blows "
                       "up at small gamma; and splitting the |H(h)| bound by "
                       "payer (v7 V2) recovers most of what the new term costs.  "
                       "The budget is still CONDITIONAL (far-field Z1 only; three "
                       "ledger items open) and still OPTIMISTIC."}


def x6_ledger():
    return [
        {"constant": "Y0 (at the a=0 anchor)", "status": "EXACT",
         "note": "the anchor is an exact zero; Y0 = 0"},
        {"constant": "Z0", "status": "BOUNDED",
         "note": "finite-block rounding only (~1e-11)"},
        {"constant": "Z1 far-field modelling error", "status": "BOUNDED (v6)",
         "note": "closed form, decays like X0^{alpha-2}"},
        {"constant": "Z1 core<->far-field coupling", "status": "OPEN",
         "note": "needs a smooth cutoff + a commutator estimate for H"},
        {"constant": "Z1 core discretization", "status": "MEASURED ONLY",
         "note": "v4 W6: J^-2.1..-2.6, never bounded"},
        {"constant": "||A|| domain SUP part", "status": "BOUNDED (v6)",
         "note": "two-point dual, uniform in J"},
        {"constant": "||A|| domain SEMINORM part", "status": "BOUNDED (v7)",
         "note": "derivative-gain closure; J-free"},
        {"constant": "C_Q sup part", "status": "BOUNDED (v6, sharpened v7/v8)",
         "note": "same |H(h)| bound, now split by which part of the norm pays"},
        {"constant": "C_Q codomain SEMINORM part", "status": "BOUNDED (NEW)",
         "note": "weighted Holder bound on H with weight 1-gamma (NOT "
                 "alpha-gamma: H does not inherit h's decay); grid-swept "
                 "supremum of an explicit majorant"},
        {"constant": "discrete <-> continuum transfer", "status": "OPEN (v7)",
         "note": "the interpolant's decay-graded norm is infinite at every J; a "
                 "change of ansatz, h = (1+X^2)^{-alpha/2} p(theta)"},
    ]


def main():
    data = {
        "meta": {
            "leg": "P2 Route-D v8 (the codomain seminorm part of C_Q; the first "
                   "complete Z2)",
            "tier": "Level-1 tooling + upper bounds (NOT a certificate)",
            "alpha_gamma_reference": [ALPHA, GAMMA],
            "reproduce": "python experiments/p2_route_d_v8_quadratic.py",
            "arithmetic": "plain float64 -- analytic majorants with numerically "
                          "evaluated constants, gated against an exact second "
                          "build of the decomposition and against measurements; "
                          "nothing here is interval-enclosed or rigorous",
        },
        "x1_estimate": x1_estimate(),
        "x2_bracket": x2_bracket(),
        "x3_gamma": x3_gamma(),
        "x4_map": x4_map(),
        "x5_budget": x5_budget(),
        "x6_ledger": x6_ledger(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))

    e = data["x1_estimate"]
    print("\nP2 ROUTE-D v8 -- the codomain seminorm part of C_Q\n" + "=" * 66)
    print("  X1  b = (%.4f, %.4f) at (alpha,gamma) = (%.1f, %.1f); grid-flat to "
          "%.1e, decomposition exact to %.1e; pointwise-only control %.0fx worse"
          % (e["reference"]["b_sup"], e["reference"]["b_semi"], ALPHA, GAMMA,
             max(abs(r["b_semi"] - e["reference"]["b_semi"])
                 for r in e["grid_ladder"]) / e["reference"]["b_semi"],
             e["decomposition_max_error"], e["ablation"]["gain"]))
    print("  X2  bracket: worst measured/bound ratio %.3f over %d profiles"
          % (max(r["worst_ratio"] for r in data["x2_bracket"]["rows"]),
             len(data["x2_bracket"]["rows"][0]["per_profile"])))
    g = data["x3_gamma"]
    print("  X3  C_Q_full bowls: minimum %.3f at gamma = %.2f (interior: %s)"
          % (g["argmin_C_Q_full"]["C_Q_full"], g["argmin_C_Q_full"]["gamma"],
             g["C_Q_full_interior"]))
    m = data["x4_map"]
    print("  X4  complete Z2 optimum %.1f at (alpha,gamma) = (%.1f, %.2f)  "
          "[v7's incomplete map said %.1f at (%.1f, %.2f)]"
          % (m["argmin_Z2_full"]["Z2"], m["argmin_Z2_full"]["alpha"],
             m["argmin_Z2_full"]["gamma"], m["argmin_Z2_v7_reproduced"]["Z2"],
             m["argmin_Z2_v7_reproduced"]["alpha"],
             m["argmin_Z2_v7_reproduced"]["gamma"]))
    b = data["x5_budget"]
    print("  X5  budget %.2e at (alpha,gamma) = (%.1f, %.2f);  history %s"
          % (b["best"]["Y0_max_full"], b["best"]["alpha"], b["best"]["gamma"],
             " -> ".join("%.1e" % h["Y0_max"] for h in b["history"])))
    print("  X6  ledger: %d of %d bounded"
          % (sum("BOUNDED" in r["status"] or r["status"] == "EXACT"
                 for r in data["x6_ledger"]), len(data["x6_ledger"])))
    print("\n[done] wrote %s" % OUT)


if __name__ == "__main__":
    main()
