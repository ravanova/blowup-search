"""P2 Route-D v7 -- the domain seminorm part of ||A||, closed by a derivative gain.

v6 (writeup/4_p2_lottery/TECHNICAL_P2_ROUTED_V6.md) left three named gaps and
called the first of them the sharpest: the domain SEMINORM part of ||A||, where
three separate computations all returned a valid but lossy bound growing like
J^gamma.  Its own recommendation was to attack it by restricting to a
band-limited subspace with a measured faithfulness factor (route a), and to keep
the analytic derivative-gain argument (route b) in reserve.

This leg does route (b), because route (a) turns out to be answering a question
nobody asked: the J^gamma is not a faithfulness defect at all.  V1 localizes it
to the NEAR-DIAGONAL pairs and shows it vanishes the moment they are excluded --
so no amount of care about which ball one optimizes over would have removed it.
What removes it is using the EQUATION, which says neighbouring rows of an inverse
differ by a derivative.

NOT a logged Tier-1/2 experiment: deterministic (no GA, no seeds, no predicate
lock).  Committed so the writeup rebuilds without re-derivation.  Run:

    .venv/bin/python experiments/p2_route_d_v7_seminorm.py
    -> writeup/data/p2_route_d_v7_seminorm.json ; figure via
       .venv/bin/python writeup/4_p2_lottery/p2_route_d_v7_evidence.py   (fig25)

SIX measurements:

  V1  WHERE THE J^gamma LIVES.  v6's dual bound on the seminorm part, computed
      over pairs separated by at least Delta in theta.  All of the growth sits on
      the near diagonal; excluding it leaves a J-flat bound.  Route (a)
      diagnosed, and disqualified as the fix.

  V2  THE SPLIT HILBERT BOUND.  v6 charged |H(h)| entirely to the total norm.
      Separating the part paid by the sup norm from the part paid by the
      seminorm costs nothing and is worth ~30% on the closure.

  V3  THE CLOSURE.  The interpolation inequality plus the solved-for derivative
      gives a J-FREE upper bound on the seminorm part -- the first one -- and
      hence on the whole of ||A||.  Reported next to the measured family lower
      bound, so the bracket is visible.

  V4  THE (alpha, gamma) MAP of the full ||A|| upper bound, and where it is
      smallest.  Both knobs now priced with upper bounds on both parts.

  V5  WHAT THE HONEST ||A|| COSTS.  v6's conditional budget used the far-field
      inverse norm 2/(2-alpha) ~ 2.5 as a proxy for ||A||.  The real bound is
      ~30x larger, and pricing it moves the far-field matching radius to
      X0 ~ 1e5-1e6 -- past what a dense collocation core can reach.  Quantified.

  V6  THE INTERPOLANT DEFECT, and the updated ledger.  A band-limited h is a
      trigonometric polynomial in theta with h(pi) != 0, while the decay weight
      diverges there: the decay-graded norm of the interpolant is INFINITE at
      every J.  Measured, with its J-scaling and the repair it points to.
"""

import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.decay_collocation import Collocation, C_ANCHOR          # noqa: E402
from solver.decay_grading import farfield_inverse_norm              # noqa: E402
from solver.holder_norms import HolderNorm                          # noqa: E402
from solver.nk_bounds import (                                      # noqa: E402
    sup_part_upper, seminorm_part_upper, hilbert_farfield_bound,
    farfield_modelling_error_bound, quadratic_constant_upper, budget,
)
from solver.nk_seminorm import (                                    # noqa: E402
    hilbert_split_bound, hilbert_split_curves, holder_interpolation_bound,
    seminorm_closure, required_X0, interpolant_far_field_defect,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "p2_route_d_v7_seminorm.json"

ALPHA, GAMMA = 1.5, 0.5
J_REF = 800


def gauged_inverse(col):
    """A = inv([gauge row ; DF rows 1..]) -- the same object v5 and v6 measured."""
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


def family_seminorm_lower(A, col, dom, cod, n_rows=14):
    """max over the exact seminorm extremizers: a LOWER bound on the same quantity.

    For a pair (i, j) the vector g = sign(A_i. - A_j.)/v maximizes |(Ag)_i -
    (Ag)_j| over the codomain SUP ball; dividing by the full codomain norm keeps
    it a valid lower bound for the induced norm (it is one admissible direction),
    and it is the sharpest single direction available without an LP.
    """
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
# V1 -- where the J^gamma lives
# ---------------------------------------------------------------------------


def pairwise_dual(A, v_cod, q_cod, n_cand=16, chunk=48):
    """The J x J matrix ||A_j. - A_k.||_{Y*} (v6's two-point dual, all pairs).

    Same content as `nk_bounds.seminorm_part_upper`, but kept as a matrix so the
    domain pair weight can be masked afterwards without redoing the O(J^3) work.
    """
    from solver.nk_bounds import two_point_dual
    J = A.shape[0]
    cand = np.unique(np.linspace(1, A.shape[1] - 1, int(n_cand)).astype(int))
    out = np.empty((J, J))
    for lo in range(0, J, chunk):
        hi = min(lo + chunk, J)
        D = (A[lo:hi, None, :] - A[None, :, :]).reshape(-1, A.shape[1])
        out[lo:hi] = two_point_dual(D, v_cod, q_cod, cand).reshape(hi - lo, J)
    return out


def v1_near_diagonal(Js=(125, 250, 500), seps=(0.0, 0.02, 0.05, 0.1)):
    rows = []
    for J in Js:
        col = Collocation(J)
        A = gauged_inverse(col)
        dom, cod = norms(col, ALPHA, GAMMA)
        dth = np.abs(col.theta[:, None] - col.theta[None, :])
        d = pairwise_dual(A, cod.w, cod.pair)
        entry = {"J": J, "grid_spacing": float(np.pi / J), "by_separation": []}
        for s in seps:
            pair = np.where(dth >= s, dom.pair, 0.0)
            entry["by_separation"].append(
                {"separation": s, "dual_bound": float((d * pair).max())})
        entry["family_lower"] = family_seminorm_lower(A, col, dom, cod)
        rows.append(entry)
    growth = {}
    for i, s in enumerate(seps):
        vals = [r["by_separation"][i]["dual_bound"] for r in rows]
        growth[str(s)] = float(np.polyfit(np.log([r["J"] for r in rows]),
                                          np.log(vals), 1)[0])
    return {"ladder": rows, "growth_exponent_by_separation": growth,
            "gamma": GAMMA,
            "reading": "the J^gamma sits entirely on pairs the grid barely "
                       "separates; a fixed theta-separation makes the same "
                       "bound J-flat, so the growth is a near-diagonal artifact "
                       "of pricing two rows independently, not a faithfulness "
                       "defect of the ball"}


# ---------------------------------------------------------------------------
# V2 -- the split Hilbert bound
# ---------------------------------------------------------------------------


def v2_split():
    Xs = np.geomspace(1e-3, 1e5, 60)
    a_sup, a_semi, total = [], [], []
    for X in Xs:
        s, m = hilbert_split_bound(X, ALPHA, GAMMA)
        a_sup.append(s)
        a_semi.append(m)
        total.append(hilbert_farfield_bound(X, ALPHA, GAMMA)[0])
    a_sup, a_semi, total = map(np.asarray, (a_sup, a_semi, total))
    wk = (1.0 + Xs ** 2) ** (0.5 * (ALPHA - 1.0))
    return {"X": Xs.tolist(), "a_sup": a_sup.tolist(), "a_semi": a_semi.tolist(),
            "v6_total": total.tolist(),
            "identity_max_rel_error": float(
                np.max(np.abs(a_sup + a_semi - total) / total)),
            "weighted_sup_of_a_sup": float(np.max(wk * a_sup)),
            "weighted_sup_of_a_semi": float(np.max(wk * a_semi)),
            "note": "a_sup + a_semi is v6's bound exactly; the split is sharper "
                    "for every element whose norm is not evenly divided between "
                    "the two parts"}


# ---------------------------------------------------------------------------
# V3 -- the closure
# ---------------------------------------------------------------------------


def v3_closure(Js=(125, 250, 500, 800, 1600)):
    curves = hilbert_split_curves(ALPHA, GAMMA)
    ladder = []
    for J in Js:
        col = Collocation(J)
        A = gauged_inverse(col)
        dom, cod = norms(col, ALPHA, GAMMA)
        C_sup = sup_part_upper(A, dom.w, cod.w, cod.pair)
        d = seminorm_closure(ALPHA, GAMMA, C_sup, curves=curves)
        ladder.append({
            "J": J, "C_sup_upper": C_sup, "T_upper": d["T_upper"],
            "P_upper": d["P_upper"], "kappa_star": d["kappa_star"],
            "A_upper": d["A_upper"],
            "dual_seminorm_upper": (seminorm_part_upper(A, dom.pair, cod.w, cod.pair)
                                    if J <= 500 else None),
            "family_seminorm_lower": family_seminorm_lower(A, col, dom, cod),
        })
    Js_a = np.array([r["J"] for r in ladder], dtype=float)
    return {
        "ladder": ladder,
        "A_upper_growth_exponent": float(np.polyfit(
            np.log(Js_a), np.log([r["A_upper"] for r in ladder]), 1)[0]),
        "reference": {"alpha": ALPHA, "gamma": GAMMA},
        "no_J_in_the_bound": "the closure has no J in it at all; the only "
                             "J-dependence in A_upper is inherited from v6's "
                             "C_sup, which saturates",
    }


# ---------------------------------------------------------------------------
# V4 -- the (alpha, gamma) map
# ---------------------------------------------------------------------------


def v4_map(alphas=(1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8),
           gammas=(0.05, 0.1, 0.15, 0.25, 0.35, 0.5, 0.65, 0.8)):
    """||A|| alone, and Z2 = 2 ||A|| C_Q -- the quantity the budget actually sees.

    The gamma grid deliberately runs past where the answer is expected, down to
    0.05: banked lesson (8).  ||A|| alone falls monotonically as gamma -> 0
    (a weaker domain norm is easier to bound), which is exactly why it must not
    be optimized alone -- the quadratic pays for the same weakness.
    """
    col = Collocation(J_REF)
    A = gauged_inverse(col)
    grid_map = []
    for a in alphas:
        row = []
        for g in gammas:
            dom, cod = norms(col, a, g)
            C_sup = sup_part_upper(A, dom.w, cod.w, cod.pair)
            d = seminorm_closure(a, g, C_sup)
            cq = quadratic_constant_upper(a, g, n_X=60)["C_Q_sup_upper"]
            row.append({"gamma": g, "C_sup_upper": C_sup,
                        "T_upper": d["T_upper"], "A_upper": d["A_upper"],
                        "C_Q_sup_upper": cq, "Z2": 2.0 * d["A_upper"] * cq,
                        "kappa_star": d["kappa_star"]})
        grid_map.append({"alpha": a, "row": row})
    best_A = min(((c["A_upper"], r["alpha"], c["gamma"])
                  for r in grid_map for c in r["row"]))
    best_Z = min(((c["Z2"], r["alpha"], c["gamma"])
                  for r in grid_map for c in r["row"]))
    return {"J": J_REF, "map": grid_map,
            "argmin_A": {"A_upper": best_A[0], "alpha": best_A[1],
                         "gamma": best_A[2]},
            "argmin_Z2": {"Z2": best_Z[0], "alpha": best_Z[1], "gamma": best_Z[2]},
            "caveat": "C_sup is v6's two-point dual at a single J (it saturates); "
                      "T_upper is the closure; C_Q is v6's sup-part bound.  All "
                      "three are UPPER bounds, so the map is one too -- the first "
                      "(alpha,gamma) map in this project made of upper bounds "
                      "rather than family-restricted maxima.  It still omits the "
                      "codomain SEMINORM part of C_Q, which is unbounded, and "
                      "that omission is worst exactly where gamma is smallest."}


# ---------------------------------------------------------------------------
# V5 -- what the honest ||A|| costs
# ---------------------------------------------------------------------------


def v5_price(alphas=(1.1, 1.2, 1.3, 1.4, 1.5), gamma=0.35, X0_grid=None):
    if X0_grid is None:
        X0_grid = np.geomspace(1e2, 1e8, 25)
    col = Collocation(J_REF)
    A = gauged_inverse(col)
    rows = []
    for a in alphas:
        dom, cod = norms(col, a, gamma)
        C_sup = sup_part_upper(A, dom.w, cod.w, cod.pair)
        d = seminorm_closure(a, gamma, C_sup)
        A_up = d["A_upper"]
        A_far, _ = farfield_inverse_norm(a, c=C_ANCHOR, X0=1.0, Xmax=1e12)
        cq = quadratic_constant_upper(a, gamma)["C_Q_sup_upper"]

        def err(X0, _a=a):
            return farfield_modelling_error_bound(_a, gamma, X0, n_X=8)["bound"]

        req_honest = required_X0(A_up, err, X0_grid, target=0.5)
        req_v6 = required_X0(A_far, err, X0_grid, target=0.5)
        Z2_honest = 2.0 * A_up * cq
        Z2_v6 = 2.0 * A_far * cq
        rows.append({
            "alpha": a, "A_upper": A_up, "A_farfield_proxy": A_far,
            "inflation": A_up / A_far, "C_Q_sup_upper": cq,
            "Z2_honest": Z2_honest, "Z2_v6_proxy": Z2_v6,
            "Y0_max_honest": budget(0.0, 0.0, 0.5, Z2_honest)["Y0_max"],
            "Y0_max_v6_proxy": budget(0.0, 0.0, 0.5, Z2_v6)["Y0_max"],
            "required_X0_honest": req_honest, "required_X0_v6_proxy": req_v6,
        })
    return {"gamma": gamma, "rows": rows,
            "target_Z1": 0.5,
            "reading": "v6's conditional budget substituted the FAR-FIELD "
                       "inverse norm 2/(2-alpha) for ||A||.  With the honest "
                       "bound the same arithmetic needs the far field to start "
                       "orders of magnitude further out, and a dense collocation "
                       "core cannot reach there (J ~ pi X0 / 4, J^2 entries).  "
                       "Same pattern as v6 B5: replacing a lower bound by an "
                       "upper bound costs the budget an order of magnitude."}


# ---------------------------------------------------------------------------
# V6 -- the interpolant defect
# ---------------------------------------------------------------------------


def v6_interpolant(Js=(200, 400, 800, 1600)):
    out = []
    for J in Js:
        col = Collocation(J)
        A = gauged_inverse(col)
        g = np.zeros(J)
        g[J // 2] = 1.0
        d = interpolant_far_field_defect(col.to_coef, A @ g, ALPHA, col.theta[-1])
        out.append({"J": J, "h_pi": d["h_pi"],
                    "weighted_at_last_node": d["weighted_at_last_node"],
                    "weighted_near_pi": d["weighted"][-1],
                    "theta_last": float(col.theta[-1]),
                    "X_last": float(col.X[-1])})
    Js_a = np.log([r["J"] for r in out])
    return {"ladder": out,
            "h_pi_growth_exponent": float(np.polyfit(
                Js_a, np.log([abs(r["h_pi"]) for r in out]), 1)[0]),
            "statement": "sup_theta w_alpha |h| is INFINITE for the interpolant "
                         "at every J: h(pi) != 0 while w_alpha = sec^alpha(th/2) "
                         "diverges.  Every discrete norm in v1..v7 is finite only "
                         "because the midpoint grid stops half a step short of pi.",
            "repair": "build the decay into the ansatz: h = (1+X^2)^{-alpha/2} "
                      "p(theta) with p a trigonometric polynomial, so the "
                      "weighted sup norm becomes the plain sup norm of p."}


def main():
    data = {
        "meta": {
            "leg": "P2 Route-D v7 (the domain seminorm part, closed by a "
                   "derivative gain)",
            "tier": "Level-1 tooling + upper bounds (NOT a certificate)",
            "alpha_gamma_reference": [ALPHA, GAMMA],
            "reproduce": "python experiments/p2_route_d_v7_seminorm.py",
            "arithmetic": "plain float64 -- analytic bounds with numerically "
                          "evaluated constants, gated against measurements; "
                          "nothing here is interval-enclosed or rigorous",
        },
        "v1_near_diagonal": v1_near_diagonal(),
        "v2_split": v2_split(),
        "v3_closure": v3_closure(),
        "v4_map": v4_map(),
        "v5_price": v5_price(),
        "v6_interpolant": v6_interpolant(),
        "v7_ledger": [
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
            {"constant": "||A|| domain SEMINORM part", "status": "BOUNDED (NEW)",
             "note": "derivative-gain closure; J-free; conditional on the sup "
                     "part bound, and a continuum statement"},
            {"constant": "C_Q sup part", "status": "BOUNDED (v6)",
             "note": "from the same |H(h)| bound"},
            {"constant": "C_Q codomain SEMINORM part", "status": "OPEN",
             "note": "needs weighted Holder boundedness of H with an explicit "
                     "constant; v5 U2 measured it (~1.12) but never bounded it"},
            {"constant": "discrete <-> continuum transfer", "status": "OPEN (NEW)",
             "note": "V6: the interpolant's decay-graded norm is infinite at "
                     "every J.  Not a small correction -- a change of ansatz"},
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))

    # ---- console summary -------------------------------------------------
    v1 = data["v1_near_diagonal"]
    print("V1 where the J^gamma lives (v6's dual bound on the seminorm part):")
    seps = [d["separation"] for d in v1["ladder"][0]["by_separation"]]
    print("    " + "J".rjust(6) + "".join(f"{'sep='+str(s):>14}" for s in seps))
    for r in v1["ladder"]:
        print(f"    {r['J']:>6}"
              + "".join(f"{d['dual_bound']:>14.3f}" for d in r["by_separation"]))
    print("    growth exponent: "
          + ", ".join(f"sep={k}: J^{v:+.3f}"
                      for k, v in v1["growth_exponent_by_separation"].items()))
    print()

    v2 = data["v2_split"]
    print(f"V2 split Hilbert bound: a_sup + a_semi == v6's bound to "
          f"{v2['identity_max_rel_error']:.1e}; weighted sups "
          f"a_sup {v2['weighted_sup_of_a_sup']:.3f}, "
          f"a_semi {v2['weighted_sup_of_a_semi']:.3f}\n")

    v3 = data["v3_closure"]
    print("V3 the closure (alpha=1.5, gamma=0.5):")
    print(f"    {'J':>6} {'C_sup (UB)':>11} {'T (UB, NEW)':>12} {'||A|| (UB)':>11}"
          f" {'v6 dual T':>11} {'family T (LB)':>14}")
    for r in v3["ladder"]:
        du = "-" if r["dual_seminorm_upper"] is None else f"{r['dual_seminorm_upper']:.3f}"
        print(f"    {r['J']:>6} {r['C_sup_upper']:>11.4f} {r['T_upper']:>12.3f} "
              f"{r['A_upper']:>11.3f} {du:>11} {r['family_seminorm_lower']:>14.4f}")
    print(f"    ||A|| upper ~ J^{v3['A_upper_growth_exponent']:+.4f} "
          f"(the closure itself contains no J)\n")

    v4 = data["v4_map"]
    print(f"V4 (alpha,gamma) map of the FULL ||A|| upper bound at J={v4['J']}:")
    gam = [c["gamma"] for c in v4["map"][0]["row"]]
    print("    alpha " + "".join(f"{'g='+str(g):>10}" for g in gam))
    for r in v4["map"]:
        print(f"    {r['alpha']:>5.1f} "
              + "".join(f"{c['A_upper']:>10.2f}" for c in r["row"]))
    print("    Z2 = 2||A||C_Q on the same grid:")
    for r in v4["map"]:
        print(f"    {r['alpha']:>5.1f} "
              + "".join(f"{c['Z2']:>10.1f}" for c in r["row"]))
    aA, aZ = v4["argmin_A"], v4["argmin_Z2"]
    print(f"    smallest ||A|| <= {aA['A_upper']:.2f} at (alpha,gamma) = "
          f"({aA['alpha']}, {aA['gamma']}) -- at the gamma edge, and NOT the "
          f"objective; smallest Z2 = {aZ['Z2']:.1f} at ({aZ['alpha']}, "
          f"{aZ['gamma']})\n")

    v5 = data["v5_price"]
    print(f"V5 what the honest ||A|| costs (gamma={v5['gamma']}, "
          f"target Z1 <= {v5['target_Z1']}):")
    print(f"    {'alpha':>6} {'||A|| UB':>9} {'v6 proxy':>9} {'x':>6} "
          f"{'X0 needed':>11} {'J needed':>10} {'Y0max UB':>10} {'Y0max v6':>10}")
    for r in v5["rows"]:
        rq = r["required_X0_honest"]
        x0 = f"{rq['X0']:.0e}" if rq["found"] else ">1e8"
        jn = f"{rq['J_needed']:.0e}" if rq["found"] else "-"
        print(f"    {r['alpha']:>6.1f} {r['A_upper']:>9.2f} "
              f"{r['A_farfield_proxy']:>9.2f} {r['inflation']:>6.1f} "
              f"{x0:>11} {jn:>10} {r['Y0_max_honest']:>10.2e} "
              f"{r['Y0_max_v6_proxy']:>10.2e}")
    print()

    v6 = data["v6_interpolant"]
    print("V6 the interpolant defect (w_alpha|h| past the last node):")
    for r in v6["ladder"]:
        print(f"    J={r['J']:>5}: h(pi)={r['h_pi']:+.2e}  w|h| at last node "
              f"{r['weighted_at_last_node']:.2e} -> {r['weighted_near_pi']:.2e} "
              f"at theta = pi - 1e-6")
    print(f"    h(pi) ~ J^{v6['h_pi_growth_exponent']:+.2f}; the weighted sup is "
          f"INFINITE at every J\n")

    print("V7 ledger:")
    for e in data["v7_ledger"]:
        print(f"    {e['status']:>18}  {e['constant']}")
    print(f"\n[done] wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
