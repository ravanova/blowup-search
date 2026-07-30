"""P2 Route-D v4 -- THE FULL OPERATOR IN THE DECAY-GRADED PAIR.

Route-D v3 (experiments/p2_route_d_v3_spaces.py, fig21) proved a no-go for the
whole weighted-ell^1 category and identified the replacement: decay-graded spaces

    ||h||_X = sup (1+X^2)^{a/2}|h| ,     ||g||_Y = sup (1+X^2)^{(a+1)/2}|g| ,

in which both Newton-Kantorovich requirements hold at once.  But v3 established
that on the far-field MODEL operator L h = -c h_X - h/X: no Hilbert coupling, no
compact core, no gauge.  Its headline recommendation (a* ~ 1.44, Z2 ~ 13) is
therefore a far-field estimate, and the obvious way for it to be wrong is that the
core contributes something the model cannot see.

This probe carries the same measurements to the FULL gauged operator, in a THIRD
independent discretization (nodal spectral collocation with weighted sup norms --
solver/decay_collocation.py; v1/v2/v3 all worked in cosine coefficients).

NOT a logged Tier-1/2 experiment: deterministic (no GA, no seeds, no predicate
lock).  Run:

    .venv/bin/python experiments/p2_route_d_v4_graded.py
    -> writeup/data/p2_route_d_v4_graded.json ; figure via
       .venv/bin/python writeup/4_p2_lottery/p2_route_d_v4_evidence.py      (fig22)

SIX measurements.

  W1  THE REPRODUCTION.  ||A||_{Y->X} on a J-ladder, ungraded (alpha = 0) vs graded
      (alpha = 3/2).  v2's negative and v3's repair should both reappear in a
      discretization that shares no code path with them: ungraded GROWS with the
      grid, graded SATURATES.  If they do not, one of the three builds is wrong.

  W2  THE RESONANCE ON THE FULL OPERATOR.  ||A|| against alpha across the
      admissible window, vs v3's far-field law 2/|alpha-2|.  Does the pole at
      alpha = 2 survive the Hilbert coupling and the gauge, and what does the core
      add on top of the far-field constant?

  W3  THE QUADRATIC -- AND THE SECOND HALF OF THE SPACE.  ||Q(h)||_Y <= ||h||_X *
      sup (1+X^2)^{1/2}|H(h)|, so the quadratic reduces to a LINEAR question: is H
      bounded from X_alpha to X_1?  It is not -- H is unbounded on L^infinity --
      and the measurement shows the divergence is LOGARITHMIC in the resolved
      bandwidth.  So the decay grading fixes the inverse but NOT the quadratic:
      the space needs a smoothness component too.  The constant on the natural
      SMOOTH family is reported separately; that is what a weighted-Holder norm
      would deliver, and it is the honest input to the budget.

  W4  THE BUDGET AND THE OPTIMUM.  Z2 = 2||A||M in the same convention as v2/v3,
      and the best conceivable certification budget 1/(4 Z2) (i.e. at Z1 = 0 --
      Z1 is NOT bounded by this leg).  Does v3's interior optimum a* ~ 1.44
      survive when the core is included?

  W5  ROBUSTNESS.  Gauge (origin / a0) and the choice of dropped collocation row.
      The v2 D3 check, repeated here: if these move the answer, the gauge is doing
      work it should not be.

  W6  THE Z1-ANALOGUE, QUANTIFIED (not bounded).  Elements of the decay class are
      not band-limited -- f_alpha is only C^alpha at theta = pi -- so the
      collocation truncates them.  Measured as the graded-codomain error of the
      collocated DF against the exact operator, as a function of J.  This is the
      honest open item: it shrinks, but this leg does not bound it.
"""

import json
import math
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.decay_collocation import (  # noqa: E402
    Collocation, grid, sup_op_norm, gauged_jacobian, graded_inverse_norm, C_ANCHOR,
)
from solver.decay_grading import (  # noqa: E402
    cos_power_coeffs, cos_power_mass, eval_sin_series, farfield_inverse_norm_finite,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "p2_route_d_v4_graded.json"

J_LADDER = [125, 250, 500, 1000, 2000]
ALPHA_GRID = [1.05, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.95]
ALPHA_MAIN = 1.5


def power_fit(xs, ys, upper_half=True):
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    m = (xs >= xs[len(xs) // 2]) if upper_half else np.ones(xs.size, bool)
    if m.sum() < 3 or np.any(ys[m] <= 0):
        return float("nan")
    return float(np.polyfit(np.log(xs[m]), np.log(ys[m]), 1)[0])


# ---------------------------------------------------------------------------


def w1_reproduction(cols):
    rows = []
    for J, col in cols.items():
        flat, _, _ = graded_inverse_norm(col, 0.0)
        grad, _, _ = graded_inverse_norm(col, ALPHA_MAIN)
        rows.append({"J": J, "X_max": float(col.X.max()),
                     "A_norm_ungraded": flat, "A_norm_graded": grad})
    Js = [r["J"] for r in rows]
    return {
        "rows": rows,
        "growth_exponent_ungraded": power_fit(Js, [r["A_norm_ungraded"] for r in rows]),
        "growth_exponent_graded": power_fit(Js, [r["A_norm_graded"] for r in rows]),
        "alpha_graded": ALPHA_MAIN,
    }


def w2_resonance(cols):
    rows = []
    for alpha in ALPHA_GRID:
        per_J = [graded_inverse_norm(col, alpha)[0] for col in cols.values()]
        rows.append({
            "alpha": alpha,
            "A_norm_per_J": per_J,
            "A_norm": per_J[-1],
            "growth_exponent_in_J": power_fit(list(cols.keys()), per_J),
            "farfield_model_law": 2.0 / abs(alpha - 2.0),
            "core_excess": per_J[-1] - 2.0 / abs(alpha - 2.0),
        })
    return {"J_ladder": list(cols.keys()), "rows": rows}


def w3_quadratic(col, alphas, degrees=(4, 8, 16, 32, 64, 128, 256, 512),
                 n_samples=300):
    """Is the quadratic bounded in the decay-graded SUP pair?  It is not.

    Measured DIRECTLY, with no proxy: sample h = f_alpha * p with p a random
    trigonometric polynomial of degree m, normalize to ||h||_X = 1, and record
    ||Q(h)||_Y.  If the sup pair controlled the quadratic this would settle as m
    grows.  It does not -- because Q(h) = h H(h) and the Hilbert transform is
    famously UNBOUNDED on L^infinity, so no purely-sup norm can bound it.  The
    growth in m is the numerical face of that classical fact.

    Also reported, separately, is the constant on the natural SMOOTH family
    (f_beta and low-degree modulations).  That is the value a norm carrying a
    smoothness component -- weighted Holder, on which H IS bounded -- would
    deliver up to a constant, and it is what the v3 far-field estimate predicts.
    It is the honest input to the budget; the sup-pair constant is infinite.
    """
    out = []
    wX = lambda a: (1.0 + col.X ** 2) ** (0.5 * a)                    # noqa: E731
    wY = lambda a: (1.0 + col.X ** 2) ** (0.5 * (a + 1.0))            # noqa: E731
    rng = np.random.default_rng(5)
    for alpha in alphas:
        base = (1.0 + col.X ** 2) ** (-0.5 * alpha)
        WX, WY = wX(alpha), wY(alpha)

        def ratio(h):
            nh = float(np.max(WX * np.abs(h)))
            if nh <= 0:
                return 0.0
            return float(np.max(WY * np.abs(col.quadratic(h)))) / nh ** 2

        # (a) the CONJUGATE-EXTREMAL family.  H is unbounded on L^infinity: the
        # conjugate of a bounded function with a jump has a logarithmic
        # singularity.  Take p_m = the degree-m Fourier partial sum of the even
        # square wave sign(cos theta) -- bounded by ~1.18 (Gibbs) with
        # ||H p_m||_inf >= (2/pi) log m, attained at the jump theta = pi/2 (X = 1),
        # where BOTH weights are O(1).  So C_Q must grow like log m.
        per_deg = []
        for m in degrees:
            j = np.arange((m - 1) // 2 + 1)
            coef = np.zeros(int(2 * j[-1] + 2))
            coef[2 * j + 1] = (4.0 / np.pi) * (-1.0) ** j / (2.0 * j + 1.0)
            pm = col.cos_eval[:, :coef.size] @ coef
            per_deg.append(ratio(base * pm))

        # (a') the control: random perturbations of the same degree, which do NOT
        # find the unbounded direction (an honest note -- sampling cannot
        # demonstrate unboundedness, only the construction can)
        per_deg_rand = []
        for m in degrees:
            best_r = 0.0
            for _ in range(n_samples):
                a_m = rng.standard_normal(m + 1) / np.sqrt(1.0 + np.arange(m + 1))
                best_r = max(best_r, ratio(base * (col.cos_eval[:, :m + 1] @ a_m)))
            per_deg_rand.append(best_r)

        # (b) the natural smooth family
        best, arg = 0.0, None
        cands = [(f"f_{b:g}", (1.0 + col.X ** 2) ** (-0.5 * b))
                 for b in (alpha, alpha + 0.25, alpha + 0.5, 2.0, 2.5, 3.0)]
        cands += [(f"f_a cos{k}", base * np.cos(k * col.theta)) for k in (1, 2, 4)]
        for name, h in cands:
            r = ratio(h)
            if r > best:
                best, arg = r, name
        out.append({
            "alpha": alpha, "degrees": list(degrees), "C_Q_per_degree": per_deg,
            "C_Q_per_degree_random": per_deg_rand,
            "C_Q_log_slope": float(np.polyfit(np.log(degrees), per_deg, 1)[0]),
            "C_Q_growth_exponent": power_fit(degrees, per_deg, upper_half=False),
            "C_Q_smooth_family": best, "argmax": arg,
            "v3_farfield_constant": cos_power_mass(alpha) / math.pi,
        })
    return out


def w4_budget(w2rows, w3rows):
    """Z2 = 2 ||A|| C_Q and the best conceivable budget 1/(4 Z2), at Z1 = 0.

    C_Q is the SMOOTH-FAMILY constant of W3 -- i.e. this prices the certificate a
    norm with a smoothness component would give, not the pure sup pair (where W3
    shows the quadratic is unbounded).  Two idealizations, both stated: Z1 = 0 and
    a smoothness component whose constant is not computed here.
    """
    out = []
    by_alpha = {r["alpha"]: r for r in w3rows}
    for r in w2rows:
        a = r["alpha"]
        if a not in by_alpha:
            continue
        CQ = by_alpha[a]["C_Q_smooth_family"]
        Z2 = 2.0 * r["A_norm"] * CQ
        out.append({
            "alpha": a, "A_norm": r["A_norm"], "C_Q": CQ, "Z2": Z2,
            "budget_ceiling": 1.0 / (4.0 * Z2),
            "v3_farfield_only_Z2": 2.0 * (2.0 / abs(a - 2.0))
                                   * (cos_power_mass(a) / math.pi),
        })
    best = max(out, key=lambda r: r["budget_ceiling"])
    argmin_A = min(w2rows, key=lambda r: r["A_norm"])["alpha"]
    return {"rows": out, "argmax_alpha": best["alpha"],
            "argmin_alpha_of_A_norm": argmin_A,
            "best_Z2": best["Z2"], "best_budget_ceiling": best["budget_ceiling"],
            "note": "budget ceiling = 1/(4 Z2), the value at Z1 = 0. Z1 (the "
                    "discretization/tail term) is NOT bounded by this leg and the "
                    "smoothness component of the norm is not priced, so the true "
                    "budget is strictly smaller. Nothing here closes."}


def w5_robustness(J=1000):
    col = Collocation(J)
    out = []
    for gauge in ("origin", "a0"):
        for drop in (0, 1, 2, J // 4, J // 2, J - 1):
            n, _, _ = graded_inverse_norm(col, ALPHA_MAIN, gauge=gauge, drop=drop)
            out.append({"gauge": gauge, "drop_row": drop, "A_norm": n,
                        "X_of_dropped_row": float(col.X[drop])})
    core = [r for r in out if r["X_of_dropped_row"] < 2.0]
    vals = [r["A_norm"] for r in core]
    allv = [r["A_norm"] for r in out]
    return {"rows": out,
            "spread_core_rows_only": float(max(vals) / min(vals)),
            "spread_all": float(max(allv) / min(allv)),
            "finding": "the gauge must replace a CORE collocation equation. "
                       "Dropping a far-field row instead leaves the far field "
                       "unconstrained and the inverse norm explodes -- an "
                       "operational constraint, not a numerical accident."}


def w6_truncation(alphas=(1.2, 1.5, 1.8)):
    K = 200000
    out = []
    for alpha in alphas:
        a = cos_power_coeffs(alpha, K)
        errs = []
        for J in (250, 500, 1000, 2000):
            col = Collocation(J)
            om = col.anchor()
            h = (1.0 + col.X ** 2) ** (-0.5 * alpha)
            got = col.jacobian_matrix(om, C_ANCHOR) @ h
            Hh = eval_sin_series(a, col.theta)
            hX = -alpha * col.X * (1.0 + col.X ** 2) ** (-0.5 * alpha - 1.0)
            want = h * (-col.X / (1.0 + col.X ** 2)) + om * Hh - C_ANCHOR * hX
            sel = (col.X > 3.0) & (col.X < 50.0)
            w = (1.0 + col.X[sel] ** 2) ** (0.5 * (alpha + 1.0))
            errs.append(float(np.max(w * np.abs(got - want)[sel])))
        out.append({"alpha": alpha, "J": [250, 500, 1000, 2000],
                    "graded_truncation_error": errs,
                    "rate_in_J": power_fit([250, 500, 1000, 2000], errs,
                                           upper_half=False)})
    return out


# ---------------------------------------------------------------------------


def main():
    print("building collocation operators ...", flush=True)
    cols = {J: Collocation(J) for J in J_LADDER}

    print("W1 reproduction ...", flush=True)
    w1 = w1_reproduction(cols)
    print("W2 resonance ...", flush=True)
    w2 = w2_resonance(cols)
    print("W3 quadratic bracket ...", flush=True)
    w3 = w3_quadratic(cols[J_LADDER[-1]], ALPHA_GRID)
    w4 = w4_budget(w2["rows"], w3)
    print("W5 robustness ...", flush=True)
    w5 = w5_robustness()
    print("W6 truncation ...", flush=True)
    w6 = w6_truncation()

    data = {
        "meta": {
            "leg": "P2 Route-D v4 (the full gauged operator in the decay-graded pair)",
            "tier": "Level-1 tooling + scoping (NOT a certificate)",
            "anchor": "Omega_2 = -(1+cos theta)/2 (= -1/(1+X^2)), c_tw = 1/2, a = 0",
            "discretization": "nodal spectral collocation on the midpoint theta-grid, "
                              "weighted sup norms (third independent build of this "
                              "operator; v1/v2/v3 were coefficient-space)",
            "gauge": "c fixed at 1/2 + one scalar normalization replacing one "
                     "collocation row (Route-D v1 Q2)",
            "reproduce": "python experiments/p2_route_d_v4_graded.py",
            "arithmetic": "plain float64 -- nothing interval-enclosed, nothing rigorous",
            "open": "Z1 (the collocation truncation of the non-band-limited decay "
                    "class) is QUANTIFIED in W6 but NOT bounded. No closure is "
                    "claimed and none should be read into the budget numbers.",
        },
        "w1_reproduction": w1,
        "w2_resonance": w2,
        "w3_quadratic": w3,
        "w4_budget": w4,
        "w5_robustness": w5,
        "w6_truncation": w6,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))

    # ---- console summary ---------------------------------------------------
    print(f"\nW1 the reproduction (alpha = 0 vs {ALPHA_MAIN}):")
    print(f"{'J':>7} {'X_max':>10} {'||A|| ungraded':>16} {'||A|| graded':>14}")
    for r in w1["rows"]:
        print(f"{r['J']:>7} {r['X_max']:>10.1f} {r['A_norm_ungraded']:>16.4g} "
              f"{r['A_norm_graded']:>14.4f}")
    print(f"   growth in J: ungraded J^{w1['growth_exponent_ungraded']:.2f}  "
          f"graded J^{w1['growth_exponent_graded']:.3f}")

    print("\nW2 the resonance on the FULL operator:")
    print(f"{'alpha':>7} {'||A||':>10} {'2/|a-2|':>10} {'core excess':>13} "
          f"{'J-exponent':>11}")
    for r in w2["rows"]:
        print(f"{r['alpha']:>7.2f} {r['A_norm']:>10.3f} {r['farfield_model_law']:>10.3f} "
              f"{r['core_excess']:>13.3f} {r['growth_exponent_in_J']:>11.3f}")

    print("\nW3 the quadratic in the SUP pair: NOT bounded (H is unbounded on L^inf)")
    print(f"   C_Q on the CONJUGATE-EXTREMAL family vs degree {w3[0]['degrees']}:")
    for r in w3[:1] + w3[5:6] + w3[-1:]:
        print(f"     alpha={r['alpha']:.2f}: "
              + " ".join(f"{v:.3f}" for v in r["C_Q_per_degree"])
              + f"   (+{r['C_Q_log_slope']:.3f} per e-fold => LOGARITHMIC)")
    print("   control -- random perturbations of the same degree do NOT find it:")
    for r in w3[5:6]:
        print(f"     alpha={r['alpha']:.2f}: "
              + " ".join(f"{v:.3f}" for v in r["C_Q_per_degree_random"])
              + "   (falls; sampling cannot demonstrate unboundedness)")
    print("   C_Q on the natural SMOOTH family (what a Holder-type norm would give):")
    for r in w3:
        print(f"     alpha={r['alpha']:.2f}: {r['C_Q_smooth_family']:.3f}   "
              f"(v3 far-field only: {r['v3_farfield_constant']:.3f}, "
              f"argmax {r['argmax']})")

    print("\nW4 the budget ceiling (Z1 = 0, smoothness component unpriced):")
    for r in w4["rows"]:
        print(f"   alpha={r['alpha']:.2f}: ||A||={r['A_norm']:6.3f} C_Q={r['C_Q']:6.3f} "
              f"Z2={r['Z2']:7.2f}  budget <= {r['budget_ceiling']:.3e}   "
              f"(v3 far-field-only Z2 {r['v3_farfield_only_Z2']:6.2f})")
    print(f"   optimum alpha = {w4['argmax_alpha']:.2f} (v3 predicted 1.44); "
          f"||A|| itself is minimized at alpha = {w4['argmin_alpha_of_A_norm']:.2f}")

    print(f"\nW5 robustness: ||A|| spread over 2 gauges x core rows = "
          f"{w5['spread_core_rows_only']:.4f}x  (over ALL rows including far-field "
          f"ones: {w5['spread_all']:.3g}x -- see finding)")
    for r in w5["rows"]:
        print(f"     gauge={r['gauge']:>6} drop row at X={r['X_of_dropped_row']:>9.3f}: "
              f"||A|| = {r['A_norm']:.4g}")
    print("W6 the Z1-analogue (collocation truncation, graded codomain):")
    for r in w6:
        print(f"   alpha={r['alpha']:.2f}: "
              + " -> ".join(f"{e:.2e}" for e in r["graded_truncation_error"])
              + f"   (J^{r['rate_in_J']:.2f}, J=250..2000)")
    print(f"[done] wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
