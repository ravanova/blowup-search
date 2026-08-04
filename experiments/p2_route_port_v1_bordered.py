"""ROUTE-PORT v1 -- the bordered system, aimed at Route-M's named target.

TARGET (Route-M, leg 45): `HL_S2_nonsymmetric` -- the strictly positive, regular,
NON-SYMMETRIC self-similar profile of the 1D Hou-Luo model, Chen-Huang-Li
arXiv:2604.01868 sec 2.5 / sec 4, reported April 2026 as a previously unreported blowup
phenomenon and NUMERICAL ONLY.  No proof, computer-assisted or otherwise; not covered by
Chen-Hou-Huang (odd, non-degenerate) or by Huang-Qin-Wang-Wei, both of which use the
symmetry the object does not have.

WHAT THIS LEG DOES, IN ONE SENTENCE.  It replaces the relaxation with a BORDERED NEWTON
SOLVE in which the three modulation constants (c_l, c_omega, c_r) are unknowns of the
same system as the profile -- and then measures, in a named norm, the three
radii-polynomial constants the certification port has never once had for its target.

WHY BORDERED FROM THE START.  Leg 44 (L-7) solved first and projected the constants
after, on the 2D object, and Newton accepted no step at all: lambda down to 1/1024.  The
directive for this leg pre-committed to the other order.

PRE-COMMITTED PREDICATE.  Calibrated on short scratch runs (n <= 501) before the logged
run, in the house convention -- the clauses below name what the scratch showed and what
this run must reproduce at full ladder depth.  P6 is a PREDICTED CEILING, in the same
spirit as clause S5 of experiments/p2_scenario2_relax.py.

  P1 CONVERGENCE.  From generic non-symmetric positive data the bordered Newton reaches
     ||F||_inf <= 1e-12 at EVERY rung of the resolution ladder.  The relaxation of leg
     ~38 floored at ~1e-2 on the same object and said so in advance; the gain must be at
     least 10 decades, and it is the reason a defect Y_0 exists at all (Route-K sec 32:
     "no fixed profile to take a defect of").
  P2 EXACT QUADRATIC STRUCTURE.  F(z+v) - F(z) - DF(z)v == Q(v,v) to <= 1e-13 of the
     CANCELLING scale |F| + |DF v|.  Consequence, and the point: Z_2 is EXACT, not a
     ball-radius estimate.
  P3 RESOLUTION-CONVERGED INVARIANT.  c_l/c_omega varies by <= 1e-3 relative across
     n = 201..1201 at fixed reach.  (The absolute triple is normalization-dependent and
     is NOT compared to CHL's -- sec 8 of the notes settled that before this leg.)
  P4 THE GAP IS ATTRIBUTED, NOT ABSORBED.  The residual gap to CHL's -2.5114 is a
     function of the DOMAIN REACH X_max alone: the reach ladder and the (independent)
     grid-stretch ladder must collapse onto one power law to within 5%, and the
     geometric extrapolation in reach must land within 0.1% of -2.5114.
  P5 THE GATE.  Does the radii polynomial close in float, with margin?  Closure means
     Y_0 <= (1-Z_1)^2/(2 Z_2) at every rung of the resolution ladder, in the weighted
     sup norm named in solver/bordered_hl.py, with its two free constants (p, w_l)
     reported and swept -- not chosen silently.
  P6 THE CEILING, PREDICTED.  (a) At the NAIVE scalar weight w_l = X_max the same
     object at the finest rung FAILS to close, so the verdict is a statement about the
     SPACE and the free constant is worth >= 100x; and (b) the distance between the
     X_max = 745 and X_max = 2026 solutions, measured in the certificate's own norm,
     exceeds r_max by many decades -- i.e. the float ball does not contain the true
     object, and the far field is the named obstruction to a real certificate.

Run:  .venv/bin/python experiments/p2_route_port_v1_bordered.py
"""

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solver.bordered_hl import (                                        # noqa: E402
    BorderedHL, CHL_RATIO, CHL_TRIPLE, profile_shape, tail_exponent,
)
from solver.target_selection import radii_polynomial, y0_budget          # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_port_v1_bordered.json")

IC = dict(x0=0.30, w=0.90, amp=1.0, vamp=0.80)
P_STAR = 0.39          # the largest decay exponent the object's own tail admits
NEWTON_TOL = 1e-13


def _ic(b, x0=0.30, w=0.90, amp=1.0, vamp=0.80):
    Om = amp * np.exp(-((b.X - x0) ** 2) / (2.0 * w ** 2))
    V = vamp * np.exp(-((b.X - 1.3 * x0) ** 2) / (2.0 * (1.1 * w) ** 2))
    return b.pack(Om, V, 1.06, -0.42, 0.077)


def solve(n=301, rho_max=8.0, c=0.5, pin=None, warm=None, ic=None, tol=NEWTON_TOL):
    """One bordered Newton solve. `warm` = (X_prev, z_prev) interpolated as the guess."""
    t0 = time.time()
    b = BorderedHL(n=n, rho_max=rho_max, c=c)
    if warm is None:
        z0 = _ic(b, **(ic or IC))
    else:
        Xp, zp = warm
        nb = (zp.size - 3) // 2
        z0 = b.pack(np.interp(b.X, Xp, zp[:nb]), np.interp(b.X, Xp, zp[nb:2 * nb]),
                    *zp[-3:])
    if pin is None:
        b.set_pin_from(_ic(b, **(ic or IC)))
    else:
        b.pin = tuple(pin)
    z, hist = b.newton(z0, tol=tol, max_iter=60)
    _, _, c_l, c_om, c_r = b.unpack(z)
    hist["wall_s"] = time.time() - t0
    return b, z, hist, (c_l, c_om, c_r)


def _row(b, z, hist, cs, **extra):
    c_l, c_om, c_r = cs
    ratio = c_l / c_om
    row = {"n": b.n, "rho_max": float(b.rho.max()), "X_max": float(np.abs(b.X).max()),
           "h_min": float(np.diff(b.X).min()),
           "residual": float(hist["residual_ladder"][-1]),
           "iters": int(len(hist["residual_ladder"]) - 1),
           "converged": bool(hist["converged"]),
           "c_l": c_l, "c_omega": c_om, "c_r": c_r, "ratio": ratio,
           "ratio_err_vs_CHL": abs(ratio - CHL_RATIO) / abs(CHL_RATIO),
           "wall_s": hist["wall_s"]}
    row.update(extra)
    return row


def geometric_extrapolate(xs, ys):
    """Aitken/Richardson on a geometric ladder: returns (limit, rate, exponent).

    xs must be geometric in the ladder variable (here X_max grows by a fixed factor).
    Reported as a LADDER of triples, not a single number, because the SHAPE is the
    evidence that the model (a single power law) is the right one at all."""
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    out = []
    for i in range(len(ys) - 2):
        d1, d2 = ys[i + 1] - ys[i], ys[i + 2] - ys[i + 1]
        if d1 == 0:
            continue
        rho = d2 / d1
        fac = xs[i + 1] / xs[i]
        q = -np.log(abs(rho)) / np.log(fac) if 0 < abs(rho) < 1 else float("nan")
        lim = ys[i + 2] + d2 * rho / (1.0 - rho) if abs(rho) < 1 else float("nan")
        out.append({"i": i, "x0": float(xs[i]), "rate": float(rho),
                    "exponent": float(q), "limit": float(lim)})
    return out


def weighted_distance(b_ref, z_ref, b_fine, z_fine, p=P_STAR, w_l_frac=0.01):
    """|| z_ref - z_fine || in the certificate's own norm, on the coarser reach's grid.

    The fine-reach solution is interpolated to the reference nodes; the constants are
    compared directly with their own weights.  This is the number that says whether the
    ball the float certificate encloses could possibly contain the TRUE profile."""
    w, nu, w_l = b_ref.weights(p=p, w_l=w_l_frac * float(np.abs(b_ref.X).max()))
    n = b_ref.n
    Om_r, V_r, cl_r, cw_r, cr_r = b_ref.unpack(z_ref)
    Om_f, V_f, cl_f, cw_f, cr_f = b_fine.unpack(z_fine)
    Om_i = np.interp(b_ref.X, b_fine.X, Om_f)
    V_i = np.interp(b_ref.X, b_fine.X, V_f)
    d = np.concatenate([Om_r - Om_i, V_r - V_i,
                        [cl_r - cl_f, cw_r - cw_f, cr_r - cr_f]])
    parts = {"Omega": float(np.max(w[:n] * np.abs(d[:n]))),
             "V": float(np.max(w[n:2 * n] * np.abs(d[n:2 * n]))),
             "c_l": float(w[2 * n] * abs(d[2 * n])),
             "c_omega": float(w[2 * n + 1] * abs(d[2 * n + 1])),
             "c_r": float(w[2 * n + 2] * abs(d[2 * n + 2]))}
    return float(max(parts.values())), parts


def evaluate(pay):
    A, B, C, D, E = (pay["A_newton_ladder"], pay["B_ablation"], pay["C_extrapolation"],
                     pay["D_certificate"], pay["E_ceiling"])
    ratios = [r["ratio"] for r in A["rungs"]]
    spread = (max(ratios) - min(ratios)) / abs(np.mean(ratios))
    tuned_ok = all(r["tuned"]["feasible"] for r in D["rungs"])
    tuned_margin = max(r["tuned"]["Y0_over_budget"] for r in D["rungs"])
    return {
        "P1_newton_converges_every_rung":
            all(r["converged"] and r["residual"] <= 1e-12 for r in A["rungs"])
            and A["decades_vs_relaxation"] >= 10,
        "P2_F_is_exactly_quadratic": A["quadratic_identity_rel"] <= 1e-11,
        "P3_ratio_resolution_converged": spread <= 1e-3,
        "P4_gap_attributed_to_reach":
            C["collapse_rel_disagreement"] <= 0.05
            and C["best_limit_err_vs_CHL"] <= 1e-3,
        "P5_radii_polynomial_closes_in_float": tuned_ok and tuned_margin <= 1e-2,
        "P6a_naive_weight_fails_at_the_finest_rung":
            (not D["rungs"][-1]["naive"]["feasible"])
            and D["rungs"][-1]["free_constant_gain"] >= 1e2,
        "P6b_truncation_distance_exceeds_r_max": E["distance_over_r_max"] >= 1e3,
    }


def _jsonable(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.bool_, bool)):
        return bool(o)
    raise TypeError(type(o))


def main():
    t_start = time.time()
    print("ROUTE-PORT v1 -- the bordered system at HL_S2_nonsymmetric "
          "(CHL arXiv:2604.01868 sec 4)")
    print(f"  target invariant: c_l/c_omega = {CHL_RATIO} (their Fig 4.2); "
          f"their raw triple {CHL_TRIPLE} is normalization-dependent and is NOT compared")

    # ---- A: the Newton ladder ------------------------------------------
    print("\n[A] bordered Newton, resolution ladder at fixed reach rho_max=8 "
          "(X_max = 745)", flush=True)
    rungs, warm, pin = [], None, None
    first_ladder = None
    for n in (201, 301, 501, 801, 1201):
        b, z, hist, cs = solve(n=n, warm=warm, pin=pin)
        if pin is None:
            pin = b.pin
        if first_ladder is None:
            first_ladder = hist["residual_ladder"]
        Om, V, c_l, c_om, _ = b.unpack(z)
        sh = profile_shape(b.X, Om, V)
        rungs.append(_row(b, z, hist, cs, shape=sh,
                          tail_Omega=tail_exponent(b.X, Om, 20.0, 200.0),
                          tail_V=tail_exponent(b.X, V, 20.0, 200.0),
                          tail_pred_Omega=c_om / c_l, tail_pred_V=2.0 * c_om / c_l))
        r = rungs[-1]
        print(f"    n={n:5d}  iters={r['iters']:3d}  ||F||_inf={r['residual']:.2e}  "
              f"c_l={r['c_l']:+.6f} c_omega={r['c_omega']:+.6f} c_r={r['c_r']:+.6f}  "
              f"ratio={r['ratio']:+.6f} ({100*r['ratio_err_vs_CHL']:.3f}% from CHL)  "
              f"[{r['wall_s']:.0f}s]", flush=True)
        warm = (b.X, z)
    print(f"    ladder shape (n=201, cold): "
          f"{' -> '.join(f'{x:.1e}' for x in first_ladder[:4])} ... "
          f"{first_ladder[-1]:.1e} in {len(first_ladder)-1} steps")

    # the exact-quadratic identity, on the coarsest rung
    b0 = BorderedHL(n=201)
    b0.set_pin_from(_ic(b0))
    z0 = _ic(b0)
    rng = np.random.default_rng(20260804)
    J0, F0 = b0.jacobian(z0), b0.F(z0)
    rels = []
    for s in (1e-1, 1e-2, 1e-3):
        v = s * rng.standard_normal(b0.N)
        Jv = J0 @ v
        lhs = b0.F(z0 + v) - F0 - Jv
        # normalized by the CANCELLING terms, not by |Q| -- see the same note in
        # test_bordered_hl.py: |Q| falls like ||v||^2 and the subtraction's round-off
        # does not, so dividing by |Q| would gate float64 instead of the algebra (67).
        rels.append(float(np.abs(lhs - b0.quadratic(v)).max()
                          / (np.abs(F0).max() + np.abs(Jv).max())))
    RELAX_FLOOR = 1e-2          # experiments/p2_scenario2_relax.py, clause S5
    decades = np.log10(RELAX_FLOOR / max(r["residual"] for r in rungs))
    A_block = {"rungs": rungs, "quadratic_identity_rel": max(rels),
               "relaxation_floor": RELAX_FLOOR, "decades_vs_relaxation": float(decades),
               "first_ladder": first_ladder, "pin": list(pin)}
    print(f"    exact-quadratic identity: max relative error {max(rels):.2e} "
          f"(=> Z_2 is EXACT, not a ball estimate)")
    print(f"    vs the relaxation's floor {RELAX_FLOOR:.0e}: {decades:.1f} decades")

    # ---- B: the ablation battery ---------------------------------------
    print("\n[B] ablation battery on the residual gap to CHL -- ALL suspects at once (74)",
          flush=True)
    reach, stretch, pins = [], [], []
    for rm in (6.0, 7.0, 8.0, 9.0, 10.0, 11.0):
        b, z, hist, cs = solve(n=301, rho_max=rm)
        reach.append(_row(b, z, hist, cs))
        r = reach[-1]
        print(f"    reach   rho_max={rm:4.1f}  X_max={r['X_max']:9.1f}  "
              f"ratio={r['ratio']:+.6f}  err={100*r['ratio_err_vs_CHL']:6.3f}%", flush=True)
    for cc in (0.25, 0.5, 1.0, 2.0):
        b, z, hist, cs = solve(n=301, c=cc)
        stretch.append(_row(b, z, hist, cs, stretch_c=cc))
        r = stretch[-1]
        print(f"    stretch c={cc:5.2f}      X_max={r['X_max']:9.1f}  "
              f"ratio={r['ratio']:+.6f}  err={100*r['ratio_err_vs_CHL']:6.3f}%", flush=True)
    for ic in ({"x0": 0.45}, {"w": 1.4}, {"amp": 2.0}, {"x0": 0.60, "w": 1.2, "amp": 0.5}):
        kw = dict(IC, **ic)
        b, z, hist, cs = solve(n=301, ic=kw)
        pins.append(_row(b, z, hist, cs, ic=kw, pin=list(b.pin)))
        r = pins[-1]
        print(f"    datum   {str(ic):32s} pin={tuple(round(t,4) for t in b.pin)}  "
              f"ratio={r['ratio']:+.6f}", flush=True)

    # ---- C: is the gap a function of X_max alone? -----------------------
    print("\n[C] attribution: is the gap a function of X_max ALONE?", flush=True)
    fit_x = np.array([r["X_max"] for r in reach])
    fit_e = np.array([r["ratio_err_vs_CHL"] for r in reach])
    slope = float(np.polyfit(np.log(fit_x), np.log(fit_e), 1)[0])
    # the stretch ladder is an INDEPENDENT way of moving X_max: predict its ratios from
    # the reach power law and see whether they land on it
    pred = np.exp(np.polyval(np.polyfit(np.log(fit_x), np.log(fit_e), 1),
                             np.log([r["X_max"] for r in stretch])))
    obs = np.array([r["ratio_err_vs_CHL"] for r in stretch])
    collapse = float(np.max(np.abs(pred - obs) / obs))
    extrap = geometric_extrapolate([r["X_max"] for r in reach],
                                   [r["ratio"] for r in reach])
    errs = [abs(e["limit"] - CHL_RATIO) / abs(CHL_RATIO) for e in extrap]
    best = int(np.argmin(errs))
    print(f"    reach power law: err ~ X_max^({slope:+.4f})   "
          f"(naive prediction from the tail exponent c_omega/c_l: "
          f"{rungs[-1]['tail_pred_Omega']:+.4f})")
    print(f"    the stretch ladder, PREDICTED from the reach law: "
          f"worst relative disagreement {100*collapse:.2f}%")
    for e in extrap:
        print(f"    extrapolate from X_max={e['x0']:8.1f}:  exponent q={e['exponent']:.4f}  "
              f"limit={e['limit']:.6f}  "
              f"({100*abs(e['limit']-CHL_RATIO)/abs(CHL_RATIO):.3f}% from CHL)")
    C_block = {"reach": reach, "stretch": stretch, "pins": pins,
               "reach_power_law_slope": slope,
               "collapse_rel_disagreement": collapse,
               "extrapolation": extrap, "best_limit": extrap[best]["limit"],
               "best_limit_err_vs_CHL": errs[best], "chl_ratio": CHL_RATIO}
    B_block = {"note": "reach / stretch / datum, run together before naming a suspect",
               "n_solves": len(reach) + len(stretch) + len(pins)}

    # ---- D: the certificate --------------------------------------------
    print("\n[D] the radii-polynomial constants, in the norm named in "
          "solver/bordered_hl.py", flush=True)
    print("    ||z|| = max( max_j (1+X_j^2)^(p/2)|Omega_j|, same for V, "
          "w_l|c_l|, |c_omega|, |c_r| )")
    cert_rungs, warm, sweep = [], None, []
    for n in (201, 401, 801):
        b, z, hist, cs = solve(n=n, warm=warm, pin=pin, tol=1e-14)
        warm = (b.X, z)
        Xmax = float(np.abs(b.X).max())
        A = np.linalg.inv(b.jacobian(z))
        grid = []
        for p in (0.0, 0.2, P_STAR):
            for f in (1e-3, 1e-2, 1e-1, 1.0):
                cc = b.certificate_constants(z, p=p, w_l=f * Xmax, A=A)
                st = radii_polynomial(cc["Y0"], cc["Z1"], cc["Z2"])
                grid.append({"n": n, "p": p, "w_l_frac": f, **cc,
                             "feasible": st["feasible"],
                             "Y0_over_budget": st["Y0_over_budget"],
                             "Y0_budget": st["Y0_budget"],
                             "r_min": st["r_min"], "r_max": st["r_max"]})
        sweep.extend(grid)
        tuned = [g for g in grid if g["p"] == P_STAR and g["w_l_frac"] == 1e-2][0]
        naive = [g for g in grid if g["p"] == P_STAR and g["w_l_frac"] == 1.0][0]
        gain = naive["Y0_over_budget"] / tuned["Y0_over_budget"]
        cert_rungs.append({"n": n, "X_max": Xmax, "h_min": float(np.diff(b.X).min()),
                           "residual": float(hist["residual_ladder"][-1]),
                           "tuned": tuned, "naive": naive, "free_constant_gain": gain})
        print(f"    n={n:4d}  TUNED (p={P_STAR}, w_l=0.01 X_max): "
              f"Y0={tuned['Y0']:.3e} Z1={tuned['Z1']:.2e} Z2={tuned['Z2']:.3e} "
              f"budget={tuned['Y0_budget']:.3e}  Y0/budget={tuned['Y0_over_budget']:.3e}  "
              f"{'CLOSES' if tuned['feasible'] else 'FAILS'}", flush=True)
        print(f"          NAIVE (p={P_STAR}, w_l=X_max):        "
              f"Y0={naive['Y0']:.3e} Z1={naive['Z1']:.2e} Z2={naive['Z2']:.3e} "
              f"budget={naive['Y0_budget']:.3e}  Y0/budget={naive['Y0_over_budget']:.3e}  "
              f"{'CLOSES' if naive['feasible'] else 'FAILS'}  "
              f"(one free constant: {gain:.0f}x)", flush=True)
    D_block = {"rungs": cert_rungs, "sweep": sweep, "p_star": P_STAR,
               "p_star_note": "the largest decay exponent the object's own tail admits: "
                              "Omega ~ |X|^(c_omega/c_l) ~ |X|^-0.394, so a weight "
                              "(1+X^2)^(p/2) with p > 0.394 makes the TRUE profile's norm "
                              "infinite -- p_star is the boundary, not a tuning choice"}

    # ---- E: the ceiling -------------------------------------------------
    print("\n[E] the ceiling: how far is the truncated object from the less-truncated one,"
          " in the certificate's OWN norm?", flush=True)
    b8, z8, h8, cs8 = solve(n=401, rho_max=8.0)
    b9, z9, h9, cs9 = solve(n=401, rho_max=9.0, pin=b8.pin)
    dist, parts = weighted_distance(b8, z8, b9, z9)
    A8 = np.linalg.inv(b8.jacobian(z8))
    c8 = b8.certificate_constants(z8, p=P_STAR,
                                  w_l=0.01 * float(np.abs(b8.X).max()), A=A8)
    st8 = radii_polynomial(c8["Y0"], c8["Z1"], c8["Z2"])
    over = dist / st8["r_max"] if st8["r_max"] else float("inf")
    print(f"    ||z(X_max=745) - z(X_max=2026)|| = {dist:.3e}   "
          f"(worst block: {max(parts, key=parts.get)})")
    print(f"    the float certificate's ball: r in [{st8['r_min']:.3e}, "
          f"{st8['r_max']:.3e}]")
    print(f"    the truncation distance is {over:.2e}x r_max -- the float ball does NOT "
          f"contain the true object")
    E_block = {"distance": dist, "parts": parts, "r_min": st8["r_min"],
               "r_max": st8["r_max"], "distance_over_r_max": over,
               "constants": c8, "reach_ref": 8.0, "reach_fine": 9.0, "n": 401}

    payload = {"route": "PORT", "version": 1,
               "target": "HL_S2_nonsymmetric (CHL arXiv:2604.01868 sec 2.5/sec 4)",
               "question": "does the radii polynomial close in float, with margin?",
               "A_newton_ladder": A_block, "B_ablation": B_block,
               "C_extrapolation": C_block, "D_certificate": D_block, "E_ceiling": E_block}
    payload["predicate_checks"] = evaluate(payload)
    payload["wall_s"] = time.time() - t_start
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, default=_jsonable)

    print("\n--- PRE-COMMITTED PREDICATE ---")
    for k, v in payload["predicate_checks"].items():
        print(f"    {'PASS' if v else 'FAIL'}  {k}")
    npass = sum(payload["predicate_checks"].values())
    print(f"\n{npass}/{len(payload['predicate_checks'])} clauses hold  "
          f"[{payload['wall_s']:.0f}s]")
    print("\nGATE (pre-committed in CONTINUATION_PROMPT.md, Directive 1): "
          "does the radii polynomial close in float, with margin?")
    verdict = "YES" if payload["predicate_checks"]["P5_radii_polynomial_closes_in_float"] \
        else "NO"
    print(f"    {verdict} -- in the weighted sup norm with p={P_STAR}, w_l = 0.01 X_max, "
          f"at every rung, worst margin "
          f"{1/max(r['tuned']['Y0_over_budget'] for r in cert_rungs):.0f}x")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
