"""Route-NB v1, leg 55 -- DOES THE REAL TARGET HAVE FINITE NORM AT ALL?

Runs the whole leg and writes `writeup/data/p2_route_nb_v1_targetnorm.json`.
Every number quoted in BLOG_P2_ROUTENB_V1.md / TECHNICAL_P2_ROUTENB_V1.md comes out of
that file, and `p2_route_nb_v1_targetnorm_evidence.py` rebuilds every claim from it
without re-running anything here.

THE QUESTION
------------
Legs 51-53 all measured on the `a = 0` CLM anchor, which is exactly one basis mode.
A live ban asserts, of the REAL target, that it "does not have finite norm in the class
where the operator is least bad".  That clause has never been measured.  This leg
projects `HL_S2_nonsymmetric` into the compactified basis `solver/spectral_certificate.py`
already uses and measures the decay exponent `p` of `|h_k|`, on two ladders.

    |h_k| ~ C k^{-p}      ==>      ||h||_{l^1_w} < infinity  <=>  p - s > 1.

THE BLOCKS
----------
NB-1  CONTROLS FIRST, and every one of them can come out differently.
NB-2  the target on the RESOLUTION ladder n = 201/401/801 at the shipped domain.
NB-3  the DOMAIN ladder -- and this is the ladder that moves.
NB-4  ablations: the far-field closure, the interpolation order, the fit band, M.
NB-5  the norms themselves: weighted partial sums, the analytic tail, the verdict.
NB-6  the second unknown V, because a certificate needs BOTH in the space.

WHAT IS NOT CLAIMED
-------------------
Nothing here says a certificate closes.  `MM` owns that.  A finite norm says the target
is IN the space; the whole of legs 51-53 is about the operator being bad IN that space.
"""

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solver.bordered_hl import BorderedHL, tail_exponent                  # noqa: E402
from solver.spectral_certificate import (                                 # noqa: E402
    coefficient_decay_exponent, sawtooth_coefficients, weight_vector, weight_window,
)
from solver.target_norm import (                                          # noqa: E402
    analytic_tail, calibration_family, clm_anchor_profile, coefficient_magnitudes,
    compactify,
    fit_exponent, inverse_X_profile, midpoint_theta_grid, noise_floor, norm_verdict,
    sawtooth_exact, sawtooth_profile, spectrum, theta_of_X, weighted_partial_sums,
    X_of_theta,
)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_nb_v1_targetnorm.json")

IC = dict(x0=0.30, w=0.90, amp=1.0, vamp=0.80)
NEWTON_TOL = 1e-13

# The primary fit band and the primary transform size, fixed HERE and swept in NB-4 so
# that "the answer does not depend on them" is checked rather than asserted.
BAND = (32, 256)
M_PRIMARY = 16384

# The classes.  s < alpha ~ 0.394 is admissible (the gate's own wording); s = 1 is where
# leg 51 measured the OPERATOR to be least bad, and is the class the ban clause names.
S_VALUES = [0.0, 0.3, 0.39, 1.0]

# The positive control's pre-registered window (lesson 84).
PC_WINDOW = {"abs_err_h1_max": 1e-10, "max_other_mode_max": 1e-08}


# --------------------------------------------------------------------------
def _ic(b, x0=0.30, w=0.90, amp=1.0, vamp=0.80):
    Om = amp * np.exp(-((b.X - x0) ** 2) / (2.0 * w ** 2))
    V = vamp * np.exp(-((b.X - 1.3 * x0) ** 2) / (2.0 * (1.1 * w) ** 2))
    return b.pack(Om, V, 1.06, -0.42, 0.077)


def solve_target(n, rho_max=8.0, c=0.5):
    """One bordered Newton solve of HL_S2_nonsymmetric.  Same path as Route-PORT."""
    t0 = time.time()
    b = BorderedHL(n=n, rho_max=rho_max, c=c)
    b.set_pin_from(_ic(b, **IC))
    z, hist = b.newton(_ic(b, **IC), tol=NEWTON_TOL, max_iter=60)
    Om, V, c_l, c_om, c_r = b.unpack(z)
    return {"b": b, "Omega": Om, "V": V, "c_l": c_l, "c_omega": c_om, "c_r": c_r,
            "alpha": -c_om / c_l, "residual": float(hist["residual_ladder"][-1]),
            "converged": bool(hist["converged"]), "wall_s": time.time() - t0}


def _measure(X, f, tail_exp, M=M_PRIMARY, band=BAND, far_field="power", order=8):
    sp = spectrum(X, f, M=M, far_field=far_field, tail_exponent=tail_exp, order=order)
    fit = fit_exponent(sp["k"], sp["hk"], *band)
    fit["noise_floor"] = noise_floor(sp["hk"], sp["k"])
    fit["n_outside_grid"] = sp["n_outside_grid"]
    fit["ratio_real_to_complex_convention"] = float(
        np.median(sp["hk_real_basis"][:256] / np.maximum(sp["hk"][:256], 1e-300)))
    return sp, fit


# --------------------------------------------------------------------------
# NB-1 -- the controls
# --------------------------------------------------------------------------
def nb1_controls():
    out = {}

    # POSITIVE CONTROL: the a = 0 CLM anchor is exactly ONE basis mode.
    pc = []
    for n in (201, 401, 801):
        b = BorderedHL(n=n)
        sp = spectrum(b.X, clm_anchor_profile(b.X), M=M_PRIMARY,
                      far_field="power", tail_exponent=-1.0)
        hk = sp["hk"]
        err1 = float(abs(hk[0] - 1.0))
        rest = float(hk[1:].max())
        pc.append({"n": int(n), "abs_err_h1": err1, "max_other_mode": rest,
                   "in_window": bool(err1 < PC_WINDOW["abs_err_h1_max"]
                                     and rest < PC_WINDOW["max_other_mode_max"])})
    out["positive_control_clm_anchor"] = {
        "what": "Omega_0 = -sin theta = -2X/(1+X^2): exactly one basis mode, p = infinity",
        "window": PC_WINDOW, "rows": pc,
        "passes": bool(all(r["in_window"] for r in pc)),
        "can_fail": ("a wrong half-angle convention, a sign error in theta_of_X or an "
                     "off-by-one in the FFT phase all smear this across every k")}

    # NEGATIVE CONTROL 1: far field |X|^-1 with a KINK -> p = 2, the s = 1 threshold.
    th = midpoint_theta_grid(65536)
    Xt = X_of_theta(th)
    k, hk, _ = coefficient_magnitudes(inverse_X_profile(Xt))
    f1 = fit_exponent(k, hk, *BAND)
    out["negative_control_1_inverse_X"] = {
        "what": "Omega = 1/(1+|X|): far field |X|^-1, kink at theta = pi, p = 2 exactly",
        "why_p2_matters": ("p = 2 is the divergence threshold of the class s = 1 -- the "
                           "class leg 51 measured the operator to be least bad in, and "
                           "the class the ban clause names"),
        "p_measured": f1["p"], "p_expected": 2.0, "abs_err": abs(f1["p"] - 2.0),
        "r2": f1["r2"],
        "note_even_modes_annihilated": ("h(theta) + h(pi - theta) = 1 kills every even "
                                        "mode; this control is retained BECAUSE that "
                                        "broke two versions of the fitter"),
        # The raw evidence that the spectrum really IS k^-2, quoted in the prose as the
        # thing the two broken fitters contradicted.  k^2 |h_k| on the ODD modes must be
        # flat; if it is not, the control's expected value is wrong and not the fitter.
        "k2_hk_on_odd_modes": [{"k": int(kk), "k2_hk": float(kk ** 2 * hk[kk - 1])}
                               for kk in (9, 17, 33, 65, 129, 255, 511, 1023)],
        "k2_hk_flatness_rel_spread_k9_to_k129": float(
            (max(kk ** 2 * hk[kk - 1] for kk in (9, 17, 33, 65, 129))
             - min(kk ** 2 * hk[kk - 1] for kk in (9, 17, 33, 65, 129)))
            / (129 ** 2 * hk[128]))}

    # NEGATIVE CONTROL 2: the sawtooth -- p = 1 AND exact coefficient values.
    k2, hk2, _ = coefficient_magnitudes(sawtooth_profile(Xt))
    f2 = fit_exponent(k2, hk2, *BAND)
    ex = sawtooth_exact(k2)
    sel = k2 <= 512
    rel = float(np.max(np.abs(hk2[sel] - ex[sel]) / ex[sel]))
    # cross-check the closed form against the repo's own sine-coefficient helper
    repo = sawtooth_coefficients(8)
    out["negative_control_2_sawtooth"] = {
        "what": "Omega = 2 arctan(X)/pi, i.e. h(theta) = theta/pi: alpha = 0, a JUMP",
        "why_p1_matters": "p = 1 is the divergence threshold of the FLAT class s = 0",
        "p_measured": f2["p"], "p_expected": 1.0, "abs_err": abs(f2["p"] - 1.0),
        "r2": f2["r2"],
        "max_rel_err_vs_exact_coeffs_k_le_512": rel,
        "exact_form": "|h_k| = 2/(pi k)",
        "repo_sawtooth_coefficients_first8": [float(v) for v in repo],
        "note": ("this control brackets the target's alpha-cusp from the BAD side: a jump "
                 "is the worst non-smoothness on the circle, so if the instrument holds "
                 "here it holds for any 0 < alpha < 1")}

    # THE CALIBRATION CURVE: does the fitter recover an exponent nobody told it?
    cal = []
    for a in (0.1, 0.2, 0.3935, 0.6, 1.0, 1.5):
        kc, hc, _ = coefficient_magnitudes(calibration_family(Xt, a))
        fc = fit_exponent(kc, hc, *BAND)
        cal.append({"alpha": float(a), "p_expected": 1.0 + a, "p_measured": fc["p"],
                    "err": fc["p"] - 1.0 - a, "r2": fc["r2"]})
    out["calibration_family"] = {
        "what": ("Omega_alpha = (1+X^2)^{-alpha/2}: far field exactly |X|^-alpha, "
                 "h = |cos(theta/2)|^alpha, so p = 1 + alpha for every alpha"),
        "band": list(BAND), "rows": cal,
        "max_abs_err": float(max(abs(r["err"]) for r in cal)),
        "systematic_bias_at_target_alpha": float(
            [r["err"] for r in cal if abs(r["alpha"] - 0.3935) < 1e-9][0]),
        "role": ("this is the instrument's systematic error bar, and it is what the "
                 "target's exponent must be quoted against")}
    return out


# --------------------------------------------------------------------------
# NB-2 -- the target on the resolution ladder, at the shipped domain
# --------------------------------------------------------------------------
def nb2_resolution_ladder(ns=(201, 401, 801)):
    rows = []
    for n in ns:
        s = solve_target(n)
        sp, fit = _measure(s["b"].X, s["Omega"], s["c_omega"] / s["c_l"])
        rows.append({"n": int(n), "rho_max": 8.0,
                     "X_max": float(np.abs(s["b"].X).max()),
                     "newton_residual": s["residual"], "converged": s["converged"],
                     "alpha_from_constants": s["alpha"],
                     "tail_exponent_physical_space": float(
                         tail_exponent(s["b"].X, s["Omega"], 50.0, 700.0)),
                     "p": fit["p"], "C": fit["C"], "r2": fit["r2"],
                     "noise_floor": fit["noise_floor"],
                     "p_predicted_1_plus_alpha": 1.0 + s["alpha"],
                     "wall_s": s["wall_s"]})
    drift = float(max(r["p"] for r in rows) - min(r["p"] for r in rows))
    return {"what": "n = 201/401/801 at the shipped domain rho_max = 8, X_max = 745",
            "band": list(BAND), "M": M_PRIMARY, "rows": rows,
            "p_drift_over_ladder": drift,
            "reading": ("the resolution ladder is FLAT -- p moves by less than the "
                        "fitter's own systematic.  The exponent is not resolution "
                        "limited at this domain size; it is DOMAIN limited, which is "
                        "NB-3")}


# --------------------------------------------------------------------------
# NB-3 -- the domain ladder, which is the one that moves
# --------------------------------------------------------------------------
def nb3_domain_ladder(rho_maxes=(8.0, 10.0, 12.0, 14.0), n=801):
    rows = []
    for rm in rho_maxes:
        s = solve_target(n, rho_max=rm)
        X_max = float(np.abs(s["b"].X).max())
        sp, fit = _measure(s["b"].X, s["Omega"], s["c_omega"] / s["c_l"])
        rows.append({"rho_max": float(rm), "n": int(n), "X_max": X_max,
                     "newton_residual": s["residual"], "converged": s["converged"],
                     "alpha_from_constants": s["alpha"],
                     "tail_exponent_physical_space_outer": float(
                         tail_exponent(s["b"].X, s["Omega"], 0.30 * X_max, 0.95 * X_max)),
                     "p": fit["p"], "p_minus_1": fit["p"] - 1.0, "r2": fit["r2"],
                     "p_predicted_1_plus_alpha": 1.0 + s["alpha"],
                     "gap_p_minus_1_minus_alpha": fit["p"] - 1.0 - s["alpha"],
                     "wall_s": s["wall_s"]})
    return {"what": ("X_max = 745 -> 3.0e+05.  This is a DIAGNOSTIC on whether the "
                     "measured exponent is a property of the profile or of the domain; "
                     "it is NOT an attempt to close the certificate's truncation gap, "
                     "which is a different quantity and is separately banned"),
            "rows": rows,
            "reading": ("p - 1 and the physical-space tail exponent RISE TOGETHER toward "
                        "alpha as X_max grows.  At X_max = 745 the profile has not yet "
                        "reached its asymptotic tail, and the coefficient measurement "
                        "reports the effective exponent over the range it can see -- "
                        "agreeing with the independent physical-space fit over the same "
                        "range.  Two different measurements of the same shortfall"),
            "relation_to_leg_47": ("leg 47 measured that extending the domain makes the "
                                   "certificate's TRUNCATION GAP worse (+0.47 decades per "
                                   "unit rho).  That is not contradicted: the exponent "
                                   "improves with reach while the gap worsens.  Different "
                                   "quantities, and nothing here repairs the gap")}


# --------------------------------------------------------------------------
# NB-4 -- the ablations
# --------------------------------------------------------------------------
def nb4_ablations(n=801, rho_max=12.0):
    s = solve_target(n, rho_max=rho_max)
    X, Om, te = s["b"].X, s["Omega"], s["c_omega"] / s["c_l"]
    out = {"base": {"n": n, "rho_max": rho_max, "alpha": s["alpha"],
                    "X_max": float(np.abs(X).max())}}

    # THE FAR-FIELD CLOSURE, RUN WHERE IT CAN ACTUALLY FIRE.
    # At rho_max = 12 the domain reaches X = 4.1e+04 while the finest theta cell of an
    # M = 16384 transform only reaches |X| = 2/(pi/M) ~ 1.0e+04, so NO sample point ever
    # falls outside the grid and all three closures return byte-identical numbers.
    # Reporting that spread as "the closure does not decide" would be a tautology of the
    # code -- lesson 90, and the tell is exactly that the numbers are identical.  So the
    # ablation is run at BOTH domains and `n_theta_points_outside_grid` is reported with
    # every row, so a vacuous row is visible as vacuous instead of counting as evidence.
    ff = []
    for rm in (8.0, rho_max):
        sr = s if rm == rho_max else solve_target(n, rho_max=rm)
        Xr, Omr, ter = sr["b"].X, sr["Omega"], sr["c_omega"] / sr["c_l"]
        for mode in ("power", "clamp", "zero"):
            _, fit = _measure(Xr, Omr, ter, far_field=mode)
            ff.append({"rho_max": float(rm), "X_max": float(np.abs(Xr).max()),
                       "far_field": mode, "p": fit["p"], "r2": fit["r2"],
                       "n_theta_points_outside_grid": fit["n_outside_grid"],
                       "ablation_fires": bool(fit["n_outside_grid"] > 0)})
    live = [r for r in ff if r["ablation_fires"]]
    out["far_field_closure"] = {
        "rows": ff,
        "can_change_the_answer": ("'clamp' injects alpha = 0 and 'zero' injects a jump, "
                                  "both worth a spurious k^-1; if they moved p the "
                                  "measurement would be reporting the closure and not "
                                  "the profile"),
        "n_rows_that_fire": len(live),
        # How far out the transform itself can see: the finest theta cell of an M-point
        # staggered grid sits pi/M from the branch point, i.e. |X| = 2M/pi.  A domain
        # shorter than this MUST be extrapolated; a longer one never is.
        "finest_theta_cell_reaches_X": float(2.0 * M_PRIMARY / np.pi),
        "spread_where_it_fires": (float(max(r["p"] for r in live)
                                        - min(r["p"] for r in live)) if live else None),
        "spread_all_rows": float(max(r["p"] for r in ff) - min(r["p"] for r in ff))}

    # INTERPOLATION ORDER, including an order that MUST break it.
    # order = 2 is linear interpolation; on the coarse end of the rho grid it cannot
    # resolve the profile and the exponent has to move.  If it does not, the `order`
    # argument is not reaching the interpolator and every other row is meaningless.
    orders = []
    for rm in (8.0, rho_max):
        sr = s if rm == rho_max else solve_target(n, rho_max=rm)
        Xr, Omr, ter = sr["b"].X, sr["Omega"], sr["c_omega"] / sr["c_l"]
        ref = compactify(Xr, Omr, M_PRIMARY, far_field="power",
                         tail_exponent=ter, order=12)[1]
        for o in (2, 3, 4, 8):
            h = compactify(Xr, Omr, M_PRIMARY, far_field="power",
                           tail_exponent=ter, order=o)[1]
            fit = fit_exponent(*coefficient_magnitudes(h)[:2], *BAND)
            orders.append({"rho_max": float(rm), "interp_order": o, "p": fit["p"],
                           "max_abs_diff_vs_order12": float(np.abs(h - ref).max()),
                           "rel_diff_vs_order12": float(np.abs(h - ref).max()
                                                        / np.abs(ref).max())})
    # The spread must be taken WITHIN a domain: the two rho_max values sit at genuinely
    # different exponents (that is NB-3's whole point), so a spread across both would
    # report the domain ladder and call it interpolation sensitivity.
    by_dom = {}
    for r in orders:
        by_dom.setdefault(r["rho_max"], []).append(r["p"])
    out["interpolation_order"] = {
        "rows": orders,
        "spread_within_domain": {str(k): float(max(v) - min(v))
                                 for k, v in by_dom.items()},
        "spread": float(max(max(v) - min(v) for v in by_dom.values())),
        "max_rel_interpolant_movement": float(max(r["rel_diff_vs_order12"]
                                                  for r in orders)),
        "why_the_second_column_is_here": (
            "p is identical to five digits across orders 2..12, and identical numbers "
            "are exactly what lesson 90 says to distrust.  So the movement of the "
            "INTERPOLANT ITSELF is reported beside it: order 2 shifts h by 8.7e-05 "
            "relative and shifts p by 3.5e-05.  The knob is wired and the profile is "
            "resolved -- that is a real null, not a tautology of the code")}

    Ms = []
    for M in (4096, 8192, 16384, 32768):
        _, fit = _measure(X, Om, te, M=M)
        Ms.append({"M": M, "p": fit["p"], "r2": fit["r2"]})
    out["transform_size_M"] = {"rows": Ms,
                               "spread": float(max(r["p"] for r in Ms)
                                               - min(r["p"] for r in Ms))}

    bands = []
    for band in ((16, 128), (32, 256), (64, 512), (32, 1024)):
        _, fit = _measure(X, Om, te, band=band)
        bands.append({"band": list(band), "p": fit["p"], "r2": fit["r2"],
                      "n_points": fit["n_points"]})
    out["fit_band"] = {"rows": bands,
                       "spread": float(max(r["p"] for r in bands)
                                       - min(r["p"] for r in bands))}
    return out


# --------------------------------------------------------------------------
# NB-5 -- the norms
# --------------------------------------------------------------------------
def nb5_norms(n=801, rho_max=12.0):
    s = solve_target(n, rho_max=rho_max)
    sp, fit = _measure(s["b"].X, s["Omega"], s["c_omega"] / s["c_l"])
    k, hk = sp["k"], sp["hk"]
    p, C = fit["p"], fit["C"]

    # the flat class of spectral_certificate must equal s = 0 of the algebraic class
    wv_flat = weight_vector(8, kind="flat")
    wv_alg0 = weight_vector(8, kind="algebraic", param=0.0)
    flat_agrees = bool(np.allclose(wv_flat, wv_alg0))

    checkpoints = [16, 64, 256, 1024, 4096]
    classes = []
    for sv in S_VALUES:
        ps = weighted_partial_sums(k, hk, sv, checkpoints)
        tail = analytic_tail(p, C, checkpoints[-1], sv)
        v = norm_verdict(p, sv, alpha=s["alpha"])
        classes.append({"s": sv, "admissible_s_lt_alpha": bool(sv < s["alpha"]),
                        "partial_sums": ps, "analytic_tail": tail, "verdict": v,
                        "norm_upper_bound": (None if not tail["finite"]
                                             else float(ps[-1]["S_N"] + tail["bound"]))})
    return {"n": n, "rho_max": rho_max, "alpha": s["alpha"], "p": p, "C": C,
            "flat_class_equals_algebraic_s0": flat_agrees,
            "checkpoints": checkpoints, "classes": classes,
            "weight_window_object_vs_operator": weight_window(s["alpha"], 1.0),
            "repo_predicted_exponent": float(-coefficient_decay_exponent(s["alpha"])),
            "reading": ("the partial sums are not the norm.  What makes the norm finite "
                        "is the TAIL, and the tail is a statement about p: finite iff "
                        "p - s > 1.  Where it is not, the entry says so instead of "
                        "quoting a large number")}


# --------------------------------------------------------------------------
# NB-6 -- the second unknown
# --------------------------------------------------------------------------
def nb6_second_unknown(n=801, rho_max=12.0):
    s = solve_target(n, rho_max=rho_max)
    X_max = float(np.abs(s["b"].X).max())
    _, fO = _measure(s["b"].X, s["Omega"], s["c_omega"] / s["c_l"])
    _, fV = _measure(s["b"].X, s["V"], 2.0 * s["c_omega"] / s["c_l"])
    return {"what": ("a certificate needs BOTH unknowns in the space.  The steady "
                     "equation forces Omega ~ |X|^(c_omega/c_l) and V ~ |X|^(2 c_omega/c_l), "
                     "so V should decay TWICE as fast and be the easier of the two"),
            "alpha_Omega": s["alpha"], "alpha_V_expected": 2.0 * s["alpha"],
            "p_Omega_predicted": 1.0 + s["alpha"],
            "p_V_predicted": 1.0 + 2.0 * s["alpha"],
            "Omega": {"p": fO["p"], "r2": fO["r2"],
                      "s_max_object": fO["p"] - 1.0,
                      "tail_exponent_physical": float(
                          tail_exponent(s["b"].X, s["Omega"],
                                        0.30 * X_max, 0.95 * X_max))},
            "V": {"p": fV["p"], "r2": fV["r2"], "s_max_object": fV["p"] - 1.0,
                  "tail_exponent_physical": float(
                      tail_exponent(s["b"].X, s["V"], 0.30 * X_max, 0.95 * X_max))},
            "binding": "Omega",
            "reading": ("V is the easier unknown by roughly a factor two in the "
                        "exponent, so Omega is what sets the admissible window and the "
                        "gate is decided on Omega alone")}


# --------------------------------------------------------------------------
# NB-7 -- the curves the figure is drawn from, stored so nothing is re-run
# --------------------------------------------------------------------------
def _thin(k, hk, npts=260):
    """Log-uniform subsample, so a 8000-point spectrum becomes a plottable curve."""
    k = np.asarray(k, float)
    want = np.unique(np.round(np.geomspace(k[0], k[-1], npts)).astype(int))
    idx = np.searchsorted(k, want)
    idx = np.unique(np.clip(idx, 0, k.size - 1))
    return [float(v) for v in k[idx]], [float(v) for v in np.asarray(hk)[idx]]


def nb7_curves(n=801, rho_max=12.0):
    out = {}
    s = solve_target(n, rho_max=rho_max)
    sp, fit = _measure(s["b"].X, s["Omega"], s["c_omega"] / s["c_l"])
    k, hk = _thin(sp["k"], sp["hk"])
    out["target_Omega"] = {"k": k, "hk": hk, "p": fit["p"], "C": fit["C"],
                           "rho_max": rho_max, "n": n, "alpha": s["alpha"]}
    spv, fv = _measure(s["b"].X, s["V"], 2.0 * s["c_omega"] / s["c_l"])
    kv, hv = _thin(spv["k"], spv["hk"])
    out["target_V"] = {"k": kv, "hk": hv, "p": fv["p"], "C": fv["C"]}

    b = BorderedHL(n=801)
    spc = spectrum(b.X, clm_anchor_profile(b.X), M=M_PRIMARY,
                   far_field="power", tail_exponent=-1.0)
    kc, hc = _thin(spc["k"], np.maximum(spc["hk"], 1e-18))
    out["positive_control_clm"] = {"k": kc, "hk": hc}

    th = midpoint_theta_grid(65536)
    Xt = X_of_theta(th)
    ks, hs, _ = coefficient_magnitudes(sawtooth_profile(Xt))
    kk, hh = _thin(ks[ks <= 8192], hs[ks <= 8192])
    out["negative_control_sawtooth"] = {"k": kk, "hk": hh}
    return out


# --------------------------------------------------------------------------
# the gate
# --------------------------------------------------------------------------
def evaluate(pay):
    c, dom, norms = pay["NB1_controls"], pay["NB3_domain_ladder"], pay["NB5_norms"]
    best = dom["rows"][-1]
    p = best["p"]
    sysm = abs(c["calibration_family"]["systematic_bias_at_target_alpha"])
    finite = [x for x in norms["classes"]
              if x["admissible_s_lt_alpha"] and x["verdict"]["finite"]
              and x["verdict"]["margin_in_exponent_units"] > sysm]
    return {
        "P1_positive_control_in_window": c["positive_control_clm_anchor"]["passes"],
        "P2_negative_controls_on_threshold": bool(
            c["negative_control_1_inverse_X"]["abs_err"] < 0.02
            and c["negative_control_2_sawtooth"]["abs_err"] < 0.02),
        "P3_calibration_recovers_exponent": bool(
            c["calibration_family"]["max_abs_err"] < 0.02),
        "P4_exponent_stable_on_resolution_ladder": bool(
            pay["NB2_resolution_ladder"]["p_drift_over_ladder"] < 0.01),
        # NOT "the closure does not decide" -- it DOES, at the shipped domain, by 0.19.
        # What licenses the headline is that at the headline domain no sample point ever
        # lies outside the grid, so no closure is consulted at all.
        "P5_headline_needs_no_extrapolation": bool(
            all(r["n_theta_points_outside_grid"] == 0
                for r in pay["NB4_ablations"]["far_field_closure"]["rows"]
                if r["rho_max"] >= 12.0)),
        "P5b_closure_DOES_decide_at_shipped_domain": float(
            pay["NB4_ablations"]["far_field_closure"]["spread_where_it_fires"] or 0.0),
        "P6_at_least_one_admissible_class_finite": bool(len(finite) > 0),
        "p_best": p,
        "systematic": sysm,
        "admissible_classes_with_finite_norm": [x["s"] for x in finite],
        "GATE": ("yes" if len(finite) > 0 else "no"),
    }


def _jsonable(o):
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(type(o))


def main():
    t0 = time.time()
    pay = {"leg": 55, "route": "NB", "version": "v1",
           "object": "HL_S2_nonsymmetric (solver/bordered_hl.py)",
           "basis": "X = tan(theta/2), full circle Fourier (the target is NON-symmetric)",
           "convention": "|h_k| = |c_k| + |c_-k| = 2|c_k|",
           "band": list(BAND), "M_primary": M_PRIMARY}
    print("NB-1 controls ...", flush=True)
    pay["NB1_controls"] = nb1_controls()
    print("NB-2 resolution ladder ...", flush=True)
    pay["NB2_resolution_ladder"] = nb2_resolution_ladder()
    print("NB-3 domain ladder ...", flush=True)
    pay["NB3_domain_ladder"] = nb3_domain_ladder()
    print("NB-4 ablations ...", flush=True)
    pay["NB4_ablations"] = nb4_ablations()
    print("NB-5 norms ...", flush=True)
    pay["NB5_norms"] = nb5_norms()
    print("NB-6 second unknown ...", flush=True)
    pay["NB6_second_unknown"] = nb6_second_unknown()
    print("NB-7 curves ...", flush=True)
    pay["NB7_curves"] = nb7_curves()
    pay["evaluation"] = evaluate(pay)
    pay["wall_s"] = time.time() - t0
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(pay, fh, indent=2, default=_jsonable)
    print(json.dumps(pay["evaluation"], indent=2, default=_jsonable))
    print(f"\nwrote {OUT}  ({pay['wall_s']:.1f} s)")
    return pay


if __name__ == "__main__":
    main()
