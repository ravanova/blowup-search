"""P2 Route-D v6 -- the first genuine UPPER bounds, and the discrete-ball trap.

Five legs built the space; none of them bounded anything.  ||A|| and C_Q were
family-restricted maxima (LOWER bounds), and Z1 was never bounded at all.  A
budget assembled from lower bounds is not a quantity a certificate can use, so
this leg attacks the two gaps the v5 continuation prompt named:

  (i)  bound Z1 using the CLOSED-FORM far-field inverse rather than a
       discretization, and
  (ii) turn the family-restricted operator norms into genuine upper bounds
       analytically -- "the far field has a closed-form inverse and the core is
       finite-dimensional, so an LP is not actually needed".

(ii) turned out to be half right and half a trap, which is the leg's main result.

NOT a logged Tier-1/2 experiment: deterministic (no GA, no seeds, no predicate
lock).  Committed so the writeup rebuilds without re-derivation.  Run:

    .venv/bin/python experiments/p2_route_d_v6_bounds.py
    -> writeup/data/p2_route_d_v6_bounds.json ; figure via
       .venv/bin/python writeup/4_p2_lottery/p2_route_d_v6_evidence.py   (fig24)

SIX measurements:

  B1  THE DISCRETE-BALL TRAP.  Computing an induced norm by duality over the
      DISCRETE unit ball is unsound: a discrete Holder seminorm only inspects
      grid nodes, so the extremizer duality selects is a grid-scale sign pattern
      whose interpolant has an enormous continuum norm.  Measured inflation and
      its J-scaling, against a smooth control.

  B2  WHAT DOES SURVIVE.  The two-point dual bound uses only inequalities the
      CONTINUUM norm implies, so it is valid.  On the domain SUP part it
      saturates in J -- the project's first uniform upper bound on any part of
      ||A||.  On the domain SEMINORM part it is valid but lossy (grows like
      J^gamma); reported with its growth so the slack is visible.

  B3  THE MODELLING IDENTITY.  DF - L = h/(X(1+X^2)) - H(h)/(1+X^2), exact.
      Gated against the collocation operator.

  B4  THE FAR-FIELD Z1 BOUND.  Feeding the Holder-paid |H(h)| bound into B3 and
      taking the sup over X >= X0 gives the first bounded piece of Z1 in six
      legs.  Mapped over (alpha, X0), with the predicted X0^{alpha-2} decay.

  B5  THE NEW ALPHA TENSION.  Z1 wants SMALL alpha (the modelling error decays
      like X0^{alpha-2}); the far-field inverse norm 2/(2-alpha) and the
      quadratic constant want otherwise.  Where the conditional budget peaks once
      Z1 is priced -- the first time Z1 has entered the optimization at all.

  B6  THE LEDGER.  Which of the NK constants are now BOUNDED, which are still
      only MEASURED, and what each open item would take.
"""

import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.decay_collocation import Collocation, C_ANCHOR      # noqa: E402
from solver.decay_grading import farfield_inverse_norm          # noqa: E402
from solver.holder_norms import (                               # noqa: E402
    HolderNorm, family_op_norm, square_wave_partial_sum,
)
from solver.nk_bounds import (                                  # noqa: E402
    two_point_dual, sup_part_upper, seminorm_part_upper, discrete_ball_inflation,
    hilbert_farfield_bound, farfield_modelling_error_bound,
    quadratic_constant_upper, farfield_mass, budget,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "p2_route_d_v6_bounds.json"

ALPHA, GAMMA = 1.5, 0.5
J_LADDER = [125, 250, 500, 1000, 1600]


def gauged_inverse(col, alpha, gamma):
    """A, codomain sup weights, codomain seminorm kernel (gauge in slot 0)."""
    J = col.J
    M = np.empty((J, J))
    M[0, :] = col.to_coef.sum(axis=0)
    M[1:, :] = col.jacobian_matrix(col.anchor(), C_ANCHOR)[1:, :]
    A = np.linalg.inv(M)
    cod = HolderNorm(col.theta, col.X, alpha + 1.0, gamma)
    cod.w[0] = 1.0
    return A, cod.w.copy(), cod.pair.copy(), cod


# ---------------------------------------------------------------------------
# B1 / B2
# ---------------------------------------------------------------------------


def b1_b2_norms():
    rows, infl = [], []
    nf = (lambda th, X: HolderNorm(th, X, ALPHA + 1.0, GAMMA))
    for J in J_LADDER:
        col = Collocation(J)
        A, v, q, cod = gauged_inverse(col, ALPHA, GAMMA)
        dom = HolderNorm(col.theta, col.X, ALPHA, GAMMA)

        sup_ub = sup_part_upper(A, dom.w, v, q)
        semi_ub = (seminorm_part_upper(A, dom.pair, v, q) if J <= 1000
                   else float("nan"))
        fam, _ = family_op_norm(A, dom, cod)
        rows.append({"J": J, "sup_part_upper": sup_ub,
                     "seminorm_part_upper": semi_ub,
                     "family_lower": float(fam)})

        if J <= 500:
            B = A / v[None, :]
            g = np.sign(B[0] - B[1]) / v
            g[0] = 0.0
            smooth = (1.0 + col.X ** 2) ** (-0.5 * (ALPHA + 1.0))
            infl.append({
                "J": J,
                "extremizer": discrete_ball_inflation(col.to_coef, J, g, nf),
                "smooth_control": discrete_ball_inflation(col.to_coef, J, smooth, nf),
            })
    Js = np.array([r["J"] for r in rows], dtype=float)
    sup = np.array([r["sup_part_upper"] for r in rows])
    semi = np.array([r["seminorm_part_upper"] for r in rows])
    ok = np.isfinite(semi)
    return {
        "ladder": rows,
        "sup_part_growth_exponent": float(np.polyfit(np.log(Js), np.log(sup), 1)[0]),
        "seminorm_part_growth_exponent": float(
            np.polyfit(np.log(Js[ok]), np.log(semi[ok]), 1)[0]),
        "inflation": infl,
        "inflation_growth_exponent": float(np.polyfit(
            np.log([d["J"] for d in infl]),
            np.log([d["extremizer"]["inflation"] for d in infl]), 1)[0]),
    }


# ---------------------------------------------------------------------------
# B3 -- the identity
# ---------------------------------------------------------------------------


def b3_identity():
    out = []
    for J in (300, 900):
        col = Collocation(J)
        L = -np.diag(1.0 / col.X) - C_ANCHOR * col.transport
        E = col.jacobian_matrix(col.anchor(), C_ANCHOR) - L
        claim = (np.diag(1.0 / (col.X * (1.0 + col.X ** 2)))
                 - col.H / (1.0 + col.X ** 2)[:, None])
        out.append({"J": J, "scale": float(np.abs(E).max()),
                    "relative_error": float(np.abs(E - claim).max()
                                            / np.abs(E).max())})
    return {"checks": out,
            "identity": "(DF - L) h = h/(X(1+X^2)) - H(h)/(1+X^2)"}


# ---------------------------------------------------------------------------
# B4 -- the far-field Z1 bound
# ---------------------------------------------------------------------------


def b4_far_field(alphas=(1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8),
                 X0s=(50.0, 100.0, 200.0, 400.0, 800.0, 1600.0, 3200.0)):
    grid_map = []
    for a in alphas:
        row = []
        for X0 in X0s:
            d = farfield_modelling_error_bound(a, GAMMA, X0)
            row.append({"X0": X0, "bound": d["bound"],
                        "pointwise_term": d["pointwise_term"],
                        "hilbert_term": d["hilbert_term"]})
        exps = float(np.polyfit(np.log([r["X0"] for r in row]),
                                np.log([r["bound"] for r in row]), 1)[0])
        grid_map.append({"alpha": a, "row": row, "decay_exponent": exps,
                         "predicted_exponent": a - 2.0})

    # validation against the collocation operator on RESOLVED nodes
    col = Collocation(1600)
    res = col.X * (np.pi / col.J) <= 1.0
    dom = HolderNorm(col.theta, col.X, ALPHA, GAMMA)
    rng = np.random.default_rng(6)
    raw = [(1.0 + col.X ** 2) ** (-0.5 * b) for b in (ALPHA, ALPHA + 0.5, ALPHA + 1.5)]
    raw += [square_wave_partial_sum(col.theta, m) for m in (16, 64, 256)]
    for frac in (0.5, 0.8, 0.95):
        i = int(frac * (col.J - 1))
        raw.append(np.sign(col.H[i]) * (1.0 + col.X ** 2) ** (-0.5 * ALPHA))
    for _ in range(6):
        k = int(rng.integers(1, col.J // 4))
        raw.append(np.cos(k * col.theta) * (1.0 + col.X ** 2) ** (-0.5 * ALPHA))
    fam = [h / dom(h) for h in raw if dom(h) > 0]
    L = -np.diag(1.0 / col.X) - C_ANCHOR * col.transport
    E = col.jacobian_matrix(col.anchor(), C_ANCHOR) - L
    w_cod = col.w_codomain(ALPHA)
    checks = []
    for X0 in (20.0, 50.0, 100.0):
        sel = (col.X >= X0) & res
        meas = max(float(np.max(w_cod[sel] * np.abs((E @ h)[sel]))) for h in fam)
        bd = farfield_modelling_error_bound(ALPHA, GAMMA, X0)["bound"]
        checks.append({"X0": X0, "measured": meas, "bound": bd,
                       "headroom": bd / meas, "n_nodes": int(sel.sum())})
    return {"map": grid_map, "validation": checks,
            "validation_J": col.J,
            "resolution_rule": "|X| dtheta <= 1 (project convention)"}


# ---------------------------------------------------------------------------
# B5 -- the alpha tension and the conditional budget
# ---------------------------------------------------------------------------


def b5_tension(alphas=(1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8),
               X0s=(200.0, 800.0, 3200.0)):
    rows = []
    for a in alphas:
        A_far, A_pred = farfield_inverse_norm(a, c=C_ANCHOR, X0=1.0, Xmax=1e12)
        cq = quadratic_constant_upper(a, GAMMA)["C_Q_sup_upper"]
        Z2 = 2.0 * A_far * cq
        entry = {"alpha": a, "A_farfield": A_far, "A_farfield_law": A_pred,
                 "C_Q_sup_upper": cq, "Z2": Z2, "mass": farfield_mass(a),
                 "by_X0": []}
        for X0 in X0s:
            e = farfield_modelling_error_bound(a, GAMMA, X0)["bound"]
            Z1 = A_far * e                       # ||A|| * ||A_dagger - DF||
            b = budget(0.0, 0.0, Z1, Z2)
            entry["by_X0"].append({"X0": X0, "modelling_error": e, "Z1_farfield": Z1,
                                   "one_minus_Z": b["one_minus_Z"],
                                   "Y0_max": b["Y0_max"], "closes": b["closes"]})
        rows.append(entry)
    best = {}
    for X0 in X0s:
        cand = [(r["by_X0"][i]["Y0_max"], r["alpha"])
                for r in rows for i in range(len(X0s))
                if r["by_X0"][i]["X0"] == X0]
        v, a = max(cand)
        best[str(X0)] = {"alpha": a, "Y0_max": v}
    return {"rows": rows, "argmax_alpha_by_X0": best,
            "caveat": "CONDITIONAL: uses the far-field ||A|| (v4 confirmed it "
                      "predicts the full gauged ||A|| to 6% on alpha in [1.4,1.7]) "
                      "and prices only the FAR-FIELD part of Z1; the core "
                      "discretization, the core<->far coupling and the domain "
                      "seminorm part of ||A|| are all still unbounded."}


def main():
    data = {
        "meta": {
            "leg": "P2 Route-D v6 (first genuine upper bounds; the discrete-ball trap)",
            "tier": "Level-1 tooling + partial upper bounds (NOT a certificate)",
            "alpha_gamma_reference": [ALPHA, GAMMA],
            "reproduce": "python experiments/p2_route_d_v6_bounds.py",
            "arithmetic": "plain float64 -- analytic bounds with numerically "
                          "evaluated constants, gated against measurements; "
                          "nothing here is interval-enclosed or rigorous",
        },
        "b1_b2_norms": b1_b2_norms(),
        "b3_identity": b3_identity(),
        "b4_far_field": b4_far_field(),
        "b5_tension": b5_tension(),
        "b6_ledger": [
            {"constant": "Y0 (at the a=0 anchor)", "status": "EXACT",
             "note": "the anchor is an exact zero; Y0 = 0"},
            {"constant": "Z0", "status": "BOUNDED",
             "note": "finite-block rounding only (~1e-11)"},
            {"constant": "Z1 far-field modelling error", "status": "BOUNDED (NEW)",
             "note": "closed form, decays like X0^{alpha-2}; validated to ~3x headroom"},
            {"constant": "Z1 core<->far-field coupling", "status": "OPEN",
             "note": "sharp split has a 1/(X-X0) seam: needs a smooth cutoff + "
                     "a commutator estimate for H"},
            {"constant": "Z1 core discretization", "status": "MEASURED ONLY",
             "note": "v4 W6: J^-2.1..-2.6, never bounded"},
            {"constant": "||A|| domain SUP part", "status": "BOUNDED (NEW)",
             "note": "two-point dual, uniform in J"},
            {"constant": "||A|| domain SEMINORM part", "status": "OPEN",
             "note": "three routes tried; all valid but lossy, growing like "
                     "J^gamma. Continuum argument says it is finite (the inverse "
                     "gains a derivative) but no computation yet shows it"},
            {"constant": "C_Q sup part", "status": "BOUNDED (NEW)",
             "note": "from the same |H(h)| bound; the codomain seminorm of hH(h) "
                     "is not bounded"},
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))

    # ---- console summary -------------------------------------------------
    n = data["b1_b2_norms"]
    print("B1 discrete-ball trap (inflation of the dual extremizer):")
    for d in n["inflation"]:
        print(f"    J={d['J']:5d}  extremizer x{d['extremizer']['inflation']:.3e}"
              f"   smooth control x{d['smooth_control']['inflation']:.4f}")
    print(f"    inflation ~ J^{n['inflation_growth_exponent']:.2f}"
          f"  -> the dual extremizer is NOT in the continuum ball\n")
    print("B2 what survives (two-point dual, valid on the continuum ball):")
    print(f"    {'J':>6} {'sup part (UB)':>15} {'semi part (UB)':>16} {'v5 family (LB)':>16}")
    for r in n["ladder"]:
        semi = ("%.3f" % r["seminorm_part_upper"]
                if np.isfinite(r["seminorm_part_upper"]) else "-")
        print(f"    {r['J']:>6} {r['sup_part_upper']:>15.4f} {semi:>16} "
              f"{r['family_lower']:>16.4f}")
    print(f"    sup part ~ J^{n['sup_part_growth_exponent']:+.3f} (SATURATES); "
          f"seminorm part ~ J^{n['seminorm_part_growth_exponent']:+.3f} (lossy)\n")
    b3 = data["b3_identity"]
    print(f"B3 identity {b3['identity']}: relative error "
          + ", ".join(f"J={c['J']}: {c['relative_error']:.1e}" for c in b3["checks"])
          + "\n")
    b4 = data["b4_far_field"]
    print("B4 far-field Z1 bound, validated on resolved nodes:")
    for c in b4["validation"]:
        print(f"    X0={c['X0']:6.0f}: measured {c['measured']:.3e} <= bound "
              f"{c['bound']:.3e}  (x{c['headroom']:.1f} headroom, "
              f"{c['n_nodes']} nodes)")
    print("    decay exponent vs prediction (alpha-2):")
    for m in b4["map"]:
        print(f"      alpha={m['alpha']:.1f}: {m['decay_exponent']:+.3f} "
              f"(predicted {m['predicted_exponent']:+.3f})")
    print()
    b5 = data["b5_tension"]
    print("B5 the alpha tension (CONDITIONAL budget -- see caveat):")
    print(f"    {'alpha':>6} {'||A||_far':>10} {'C_Q_ub':>8} {'Z2':>8}"
          + "".join(f" {'Z1@'+str(int(x['X0'])):>12}" for x in b5["rows"][0]["by_X0"])
          + "".join(f" {'Y0max@'+str(int(x['X0'])):>14}" for x in b5["rows"][0]["by_X0"]))
    for r in b5["rows"]:
        print(f"    {r['alpha']:>6.1f} {r['A_farfield']:>10.3f} "
              f"{r['C_Q_sup_upper']:>8.3f} {r['Z2']:>8.2f}"
              + "".join(f" {x['Z1_farfield']:>12.4f}" for x in r["by_X0"])
              + "".join(f" {x['Y0_max']:>14.3e}" for x in r["by_X0"]))
    print("    best alpha by X0: "
          + ", ".join(f"X0={k}: alpha={v['alpha']:.1f} (Y0max {v['Y0_max']:.2e})"
                      for k, v in b5["argmax_alpha_by_X0"].items()))
    print("\nB6 ledger:")
    for e in data["b6_ledger"]:
        print(f"    {e['status']:>16}  {e['constant']}")
    print(f"\n[done] wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
