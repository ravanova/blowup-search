"""Arc 6, wave 4, agent 7 (leg 433): the ADVERSARY, unit R5(vii).

    .venv/bin/python experiments/arc6_w4_adversary.py          # runs every faking attempt, writes the artefact

For each pre-registered gate of leg_433_prereg.md section 2 (P1-P3, I1-I3, V1-V3, S1-S3) this runner tries to
produce the gate's YES from a deliberately under-resolved or mis-specified run, using ONLY the gate's definition.
It never sees the four workers' files. Pinned inputs: the leg-430 profile (arc6_profile_v1.json: X_tail, c_inf)
and the leg-432 tail stress formulas (leg_432_prereg_amend.md section 1), rebuilt here through the imported
`Tail` class of arc6_residual_v1.py (not edited).

Measured numbers only. Tier 2. Not a proof.
"""
import json, sys, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))
from arc6_residual_v1 import Tail, LOG_XT, C_INF, cheb, PDF_SHA  # noqa: E402
OUT = ROOT / "writeup" / "data" / "arc6" / "wave4" / "agent_7_adversary.json"

H = 1e-7; A = 0.5 + H; D = 0.5 - H
LOG2 = np.log(2.0)
def nrm(a):                                   # scaled Frobenius norm: entries ~1e-176 must not underflow when squared
    a = np.abs(np.asarray(a, float)); s = float(np.max(a)) if a.size else 0.0
    return 0.0 if s == 0.0 else s * float(np.sqrt(np.sum((a / s) ** 2)))
rel = lambda a, b: nrm(a - b) / nrm(b)
def slope(xs, ys):
    xs, ys = np.log(np.asarray(xs, float)), np.log(np.asarray(ys, float))
    return float(np.polyfit(xs, ys, 1)[0])


# ---------------------------------------------------------------- the pinned target stress (leg 432 formulas)
def target(dy=1e-3, n_eta=16, heat=True, y1=3.5):
    T = Tail(H); rho = T.rho
    y = np.arange(0.0, y1 + dy / 2, dy); delta = 3.0 - y; lW = T.lW(delta)
    eta, _ = cheb(n_eta); d = 1 - eta ** 2; L = 1 - 2 * H * eta ** 2
    kap = 2 * H * (1 + H) * d if heat else 0 * d; kap_eta = -4 * H * (1 + H) * eta if heat else 0 * eta
    psi_h, fop_h = T.psi_hat(y), T.fop_hat(y)
    J_h = T.integral(y, -(1 - H), T.psi_hat); G_h = T.integral(y, H, T.psi_hat)
    calA_h = rho * (psi_h + (1 - H) * J_h)                                   # e^{4/delta^2} x calA (eta-independent)
    sh = 1.0 if heat else 0.0
    calB_h = ((2 + 2 * H) * (sh - 1) * np.exp(np.minimum(lW, 700)) + (2 + 2 * H) * rho * psi_h + 2 * fop_h)[:, None] \
        - sh * (kap[None, :] * rho * psi_h[:, None] + rho * G_h[:, None] * (kap * (1 - H) - D * eta * kap_eta)[None, :]) / L[None, :]
    Phi_h = lambda yp: rho * T.psi_hat(yp) * (2 - rho * T.psi(yp))
    S2A = T.integral(y, 2 * A, Phi_h); S2h = T.integral(y, 2 * H, Phi_h)
    logX = LOG_XT + y; log_Epow = np.log(C_INF) - A * logX; pref = np.exp(log_Epow + 0.5 * (logX - LOG2))
    w = np.exp(-lW)                                                            # the flat weight itself (0 beyond y = 3: exact)
    Tth_hat = pref[:, None] * (calA_h[:, None] / L[None, :] + calB_h * np.exp(-logX)[:, None])
    TthA_hat = pref[:, None] * (calA_h[:, None] / L[None, :])                # the sqrt(X) term alone (drops B/X ~ 1e-207 relative)
    Tz_hat = (C_INF ** 2 * np.exp((0.5 - 2 * A) * logX) / np.sqrt(2))[:, None] * eta[None, :] * (2 * A * S2A - 2 * H * S2h)[:, None] / L[None, :]
    return dict(y=y, delta=delta, lW=lW, w=w, eta=eta, L=L, d=d, pref=pref, calA_h=calA_h, calB_h=calB_h, logX=logX,
                Tth=Tth_hat * w[:, None], TthA=TthA_hat * w[:, None], Tz=Tz_hat * w[:, None], Tth_hat=Tth_hat, Tz_hat=Tz_hat)


# ---------------------------------------------------------------- (iii) P1, P2: pulses whose averaged product is the stress
def pulses(tg, N0=8):
    """u_r = a cos(k phi), u_theta = b cos(k phi + psi), a b / 2 = T_theta (the two-wave covariance of (7.23)-(7.26) reduced
    to one product per entry). Every 'averaging' below is a choice the gate does not fix."""
    m = (tg["y"] >= 0.5) & (tg["y"] <= 2.9); y = tg["y"][m]; Tth = tg["Tth"][m]; Tz = tg["Tz"][m]
    out = {}
    # (a) the joint two-entry norm hides T_z entirely: T_z / T_theta ~ 1e-136 on this profile
    joint = lambda a1, a2: nrm(np.stack([a1, a2]))
    out["a_norm_hides_Tz"] = {"rel_joint_err_Tz_set_to_zero": joint(Tth - Tth, Tz - 0) / joint(Tth, Tz),
                             "rel_joint_err_Tz_sign_flipped": joint(Tth - Tth, Tz + Tz) / joint(Tth, Tz),
                             "componentwise_err_Tz_zero": 1.0, "componentwise_err_Tz_flipped": 2.0,
                             "log10_ratio_normTz_over_normTth": float(np.log10(nrm(Tz) / nrm(Tth)))}
    # (b) aliasing: M = 2k equispaced samples offset by phi0 = -pi/(4k); discrete mean of cos(k phi) cos(k phi + psi)
    def disc_mean(k, psi, M, phi0):
        ph = 2 * np.pi * np.arange(M) / M + phi0
        return float(np.mean(np.cos(k * ph) * np.cos(k * ph + psi)))
    alias = {}
    for N in (N0, 2 * N0, 4 * N0):
        M, phi0 = 2 * N, -np.pi / (4 * N)
        f_twin, f_phase, f_half = disc_mean(N, 0.0, M, phi0), disc_mean(N, np.pi / 2, M, phi0), 0.25 * disc_mean(N, 0.0, M, phi0)   # both amplitudes halved: product /4
        exact_phase = disc_mean(N, np.pi / 2, 64 * N + 1, 0.0)
        alias[str(N)] = {"M_samples": M, "phi0": phi0,
                         "rel_err_twin": rel(2 * f_twin * Tth, Tth), "rel_err_phase_pi_over_2": rel(2 * f_phase * Tth, Tth),
                         "rel_err_amplitude_halved": rel(2 * f_half * Tth, Tth),
                         "rel_err_phase_pi_over_2_with_resolved_average": rel(2 * exact_phase * Tth, Tth)}
    out["b_aliasing_M_eq_2k"] = alias
    # (c) the 'convergence exponent in N' is set by the averaging window, not by the field
    Ns = np.array([N0, 2 * N0, 4 * N0])
    def box_theta(N, Theta):            # mean of cos^2 over theta in [0, Theta]: 1/2 + sin(2 N Theta)/(4 N Theta)
        return 0.5 + np.sin(2 * N * Theta) / (4 * N * Theta)
    schemes = {}
    Theta_tuned = np.pi / (6 * N0)      # |sin(2 N Theta)| = sin(pi/3) at all three N -> error exactly ∝ 1/N
    for name, Theta in (("box_window_theta_tuned_pi_over_6N0", Theta_tuned), ("box_window_theta_1rad", 1.0)):
        errs = [abs(2 * box_theta(N, Theta) - 1.0) for N in Ns]
        schemes[name] = {"rel_err_at_N": dict(zip(map(str, Ns), errs)), "fitted_exponent": slope(Ns, errs)}
    sig = 0.5
    errs = [abs(np.exp(-2 * N ** 2 * sig ** 2)) for N in Ns]
    schemes["gaussian_window_theta_sigma_0.5"] = {"rel_err_at_N": dict(zip(map(str, Ns), errs)), "fitted_exponent": slope(Ns, np.maximum(errs, 1e-300))}
    rng = np.random.default_rng(433); mc = []
    for N in Ns:
        e = [abs(np.mean(2 * np.cos(N * rng.uniform(0, 2 * np.pi, 4 * N)) ** 2) - 1) for _ in range(400)]
        mc.append(float(np.exp(np.mean(np.log(np.maximum(e, 1e-300))))))
    schemes["monte_carlo_M_eq_4N_geomean_400_seeds"] = {"rel_err_at_N": dict(zip(map(str, Ns), mc)), "fitted_exponent": slope(Ns, mc)}
    errs = [abs(np.mean(np.cos(N * (2 * np.pi * np.arange(3) / 3)) ** 2) * 2 - 1) for N in Ns]
    schemes["trapezoid_3_points_per_period"] = {"rel_err_at_N": dict(zip(map(str, Ns), errs)), "fitted_exponent": "undefined (error is roundoff)"}
    out["c_exponent_is_the_window"] = schemes
    # P2: divergence residual. theta-window -> multiplicative constant -> same exponent; y-window (phase N y) -> oscillatory in y
    dy = float(y[1] - y[0]); col = Tth[:, 0]
    div = lambda f: np.gradient(f, dy) + f            # r*(d_r + 2/r) acting on the y-profile, up to the common q,X factors
    p2 = {}
    for N in Ns:
        c = 2 * box_theta(N, Theta_tuned) - 1.0
        W = np.pi / (3 * N0)                          # N0 W = pi/3: |sin(N W)| equal at all three N
        err_y = col * np.sin(N * W) * np.cos(2 * N * y) / (N * W)
        p2[str(N)] = {"theta_window": {"P1_rel": abs(c), "P2_rel": rel(div(col * (1 + c)), div(col))},
                      "y_window": {"P1_rel": rel(col + err_y, col), "P2_rel": rel(div(col + err_y), div(col))}}
    out["P2"] = {"per_N": p2,
                 "theta_window_exponents": {"P1": slope(Ns, [p2[str(N)]["theta_window"]["P1_rel"] for N in Ns]), "P2": slope(Ns, [p2[str(N)]["theta_window"]["P2_rel"] for N in Ns])},
                 "y_window_exponents": {"P1": slope(Ns, [p2[str(N)]["y_window"]["P1_rel"] for N in Ns]), "P2": slope(Ns, [p2[str(N)]["y_window"]["P2_rel"] for N in Ns])}}
    return out


# ---------------------------------------------------------------- a prescribed leading-order field in physical coordinates (for P3, V2, S2)
def qsolve(z, tau):
    q = tau + np.abs(z) ** (1 / D)
    for _ in range(60):
        f = q - z ** 2 * q ** (2 * H) - tau; fp = 1 - 2 * H * z ** 2 * q ** (2 * H - 1); q = q - f / fp
    return q

def bump_E(y, eta):                     # a 'wrong' profile: unit amplitude, no cutoff, no heat factor, Gaussian in y (r ~ 1e104 here, so d_r^2 u ~ 1e-208: unit amplitude keeps the finite differences above underflow)
    return np.exp(-(y - 1.5) ** 2) / (1 + eta ** 2)

def u_theta(r, z, tau, Aexp=A):
    q = qsolve(z, tau); X = r ** 2 / (2 * q); eta = z / q ** (1 - Aexp)
    return q ** (-Aexp) * bump_E(np.log(X) - LOG_XT, eta)

def residual_terms(tau, eps=1e-4):
    """theta-momentum residual of u = u_theta e_theta (u_r = u_z = 0): -d_tau u - (d_r^2 + d_r/r - 1/r^2 + d_z^2) u, term by term."""
    yy, ee = np.meshgrid(np.linspace(0.6, 2.8, 15), np.linspace(-0.8, 0.8, 9), indexing="ij")
    q = tau / (1 - ee ** 2); z = q ** D * ee; r = np.sqrt(2 * q * np.exp(LOG_XT + yy))
    dr, dz, dt = eps * r, eps * np.maximum(np.abs(z), q ** D), eps * tau
    u = u_theta(r, z, tau)
    ur = (u_theta(r + dr, z, tau) - u_theta(r - dr, z, tau)) / (2 * dr)
    urr = (u_theta(r + dr, z, tau) - 2 * u + u_theta(r - dr, z, tau)) / dr ** 2
    uzz = (u_theta(r, z + dz, tau) - 2 * u + u_theta(r, z - dz, tau)) / dz ** 2
    ut = -(u_theta(r, z, tau + dt) - u_theta(r, z, tau - dt)) / (2 * dt)
    rad = urr + ur / r - u / r ** 2
    return {"max_u": float(np.max(np.abs(u))), "max_dt": float(np.max(np.abs(ut))), "max_radial_visc": float(np.max(np.abs(rad))),
            "max_axial_visc": float(np.max(np.abs(uzz))), "max_R_theta": float(np.max(np.abs(ut - rad - uzz))),
            "axial_over_radial_max_over_max": float(np.max(np.abs(uzz)) / np.max(np.abs(rad)))}


def p3_hierarchy():
    qs = [1e-2, 1e-3, 1e-4]; terms = {str(q): residual_terms(q) for q in qs}
    ratio = [terms[str(q)]["axial_over_radial_max_over_max"] for q in qs]
    meas = slope(qs, ratio)
    fake_const = [0.3, 0.3, 0.3]                     # an ansatz whose 'lower-order term' is a fixed 30% of the leading one
    fake_drift = [0.3 * q ** 0.04 for q in qs]        # or drifts with exponent 0.04
    return {"terms": terms, "measured_axial_over_radial_ratio": dict(zip(map(str, qs), ratio)), "measured_exponent": meas, "claimed_exponent_2h": 2 * H,
            "q^2h_at_the_three_q": {str(q): q ** (2 * H) for q in qs},
            "fake_constant_ratio_exponent": slope(qs, fake_const), "fake_constant_passes_pm0.05": abs(slope(qs, fake_const) - 2 * H) < 0.05,
            "fake_drift_0.04_exponent": slope(qs, fake_drift), "fake_drift_passes_pm0.05": abs(slope(qs, fake_drift) - 2 * H) < 0.05,
            "tolerance_over_signal": 0.05 / (2 * H), "at_h_1e-3_tolerance_over_signal": 0.05 / 2e-3}


# ---------------------------------------------------------------- (iv) I1-I3: a correction stage that builds in its own gain
def iteration(tg):
    m = (tg["y"] >= 0.5) & (tg["y"] <= 2.9); y = tg["y"][m]; col = tg["Tth"][m, 0]; dy = float(y[1] - y[0])
    R0_prof = nrm(np.gradient(col, dy) + col)         # q-independent factor of ||R^(0)|| = q^{-A-1} x this (exact factorisation)
    qs = [1e-2, 1e-3, 1e-4]
    R0 = {str(q): q ** (-A - 1) * R0_prof for q in qs}
    # fake A: the stage absorbs all but a q^{1/10} fraction of the source (the ansatz assumes the 1/10)
    R1A = {str(q): q ** 0.1 * R0[str(q)] for q in qs}; R2A = {str(q): q ** 0.1 * R1A[str(q)] for q in qs}
    gainA1 = slope(qs, [R1A[str(q)] / R0[str(q)] for q in qs]); gainA2 = slope(qs, [R2A[str(q)] / R1A[str(q)] for q in qs])
    # fake B: a real linear solve (u' + u = S, backward Euler) whose leftover is grid error; the grid is tied to q
    def stage_B(S_fun, n):
        yy = np.linspace(0.5, 2.9, n); dd = yy[1] - yy[0]; S = S_fun(yy); u = np.zeros(n)
        for i in range(1, n): u[i] = (u[i - 1] + dd * S[i]) / (1 + dd)
        return nrm(np.gradient(u, dd) + u - S) / nrm(S), yy, u, S
    S0 = lambda yy: np.interp(yy, y, col / np.max(np.abs(col)))
    resB_tied = {str(q): stage_B(S0, int(round(100 * (q / 1e-2) ** (-0.1))))[0] for q in qs}
    resB_fixed = {str(q): stage_B(S0, 100)[0] for q in qs}
    gainB_tied = slope(qs, [resB_tied[str(q)] for q in qs]); gainB_fixed = slope(qs, [resB_fixed[str(q)] for q in qs])
    # fake B, second stage: solve again with the leftover as source, same grid rule
    def two_stage(n):
        r1, yy, u, S = stage_B(S0, n); left = np.gradient(u, yy[1] - yy[0]) + u - S
        r2 = stage_B(lambda t: np.interp(t, yy, left), n)[0]
        return r1, r2
    ts = {str(q): two_stage(int(round(100 * (q / 1e-2) ** (-0.1)))) for q in qs}
    gainB2 = slope(qs, [ts[str(q)][1] for q in qs])
    ctrl_zero = slope(qs, [1.0, 1.0, 1.0])
    return {"R0_norm": R0, "fakeA_builtin": {"R1_over_R0": {str(q): R1A[str(q)] / R0[str(q)] for q in qs}, "gain_stage1": gainA1, "gain_stage2": gainA2},
            "fakeB_grid_tied_to_q": {"rel_leftover_stage1": resB_tied, "gain_stage1": gainB_tied, "rel_leftover_stage2": {k: v[1] for k, v in ts.items()}, "gain_stage2": gainB2,
                                     "same_solve_fixed_grid_gain": gainB_fixed, "n_points": {str(q): int(round(100 * (q / 1e-2) ** (-0.1))) for q in qs}},
            "paper_gain_in_q_exponent": H / 10, "zero_correction_control_gain": ctrl_zero,
            "zero_correction_control_within_0.02_of_paper_q_gain": abs(ctrl_zero - H / 10) < 0.02,
            "log_eps_range_over_q_1e-2_to_1e-4": float(H * np.log(1e2)), "note": "sigma_j = 1/5 + j/10 (9.8) is an exponent of eps = q^h (Lemma 9.8: g_j = h j/10); in q the per-stage gain is h/10."}


def ledger(kappa=1e-5, B=0.7, c4=0.17):
    """Prop 9.6's closing inequalities (p. 111), as arithmetic: value, threshold, margin."""
    rows = {"wave_row": (min(0.5 - 3 * kappa, 0.5 - kappa, B - kappa, 0.4), 0.4),
            "tangential_mean_row": (min(0.5 - 4 * kappa, 0.4 - kappa, 0.5 - 2 * kappa, B - 3 * kappa), 0.4 - kappa),
            "H_minus_B": (0.5 - 2 * kappa, 0.1), "mean_0.17_row": (min(c4, 1 - 4 * kappa), 0.1), "defect_row": (0.9 - 4 * kappa, 0.1)}
    margins = {k: v[0] - v[1] for k, v in rows.items()}
    gain_rows = {k: v[0] - 0.1 for k, v in rows.items() if k in ("wave_row", "tangential_mean_row", "H_minus_B", "mean_0.17_row", "defect_row")}
    return {"kappa_s": kappa, "B0": B, "c4": c4, "rows": {k: {"value": v[0], "threshold": v[1]} for k, v in rows.items()}, "margins_vs_threshold": margins,
            "values_minus_0.1": gain_rows, "all_rows_hold": bool(all(v >= 0 for v in margins.values())), "smallest_value_minus_0.1": min(gain_rows.values()),
            "sigma_j": [0.2 + j / 10 for j in range(6)], "h_sigma_j_to_infinity": True}


# ---------------------------------------------------------------- (v) V1-V3: norms of a prescribed field are a Jacobian identity
def norms(Eprof, dy, eta_c=0.9, n_eta=200, Aexp=A, taus=(1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6)):
    Dexp = 1 - Aexp
    y = np.arange(0.5, 3.0 + dy / 2, dy); eta = np.linspace(-eta_c, eta_c, n_eta + 1)
    Y, ETA = np.meshgrid(y, eta, indexing="ij"); E = Eprof(Y, ETA); X = np.exp(LOG_XT + Y)
    d = 1 - ETA ** 2; L = 1 - 2 * H * ETA ** 2
    Linf, L2 = [], []
    for tau in taus:
        q = tau / d
        Linf.append(float(np.max(q ** (-Aexp) * np.abs(E))))
        integrand = 2 * np.pi * q ** (1 + Dexp - 2 * Aexp) * (L / d) * E ** 2 * X      # dx dy dz = 2 pi q dX . q^D (L/d) d eta ; dX = X dy
        L2.append(float(np.sqrt(np.trapezoid(np.trapezoid(integrand, eta, axis=1), y))))
    return {"taus": list(taus), "Linf": Linf, "L2": L2, "Linf_exponent": slope(taus, Linf), "L2_exponent": slope(taus, L2)}

def headline():
    tail = lambda y, eta: C_INF * np.exp(-A * (LOG_XT + y)) * Tail(H).fo(y) / (1 + eta ** 2) * 2   # pinned tail shape (E = c_inf X^-A f_o), an eta profile
    out = {"claimed_bookkeeping_L2_exponent": (1 + D - 2 * A) / 2, "claimed_Linf_exponent": -A, "profiles": {}}
    for name, prof, Aexp in (("pinned_tail_shape", tail, A), ("gaussian_bump_wrong_profile", bump_E, A), ("bump_A_0.85_control", bump_E, 0.85)):
        res = {f"{dy:g}": norms(prof, dy, Aexp=Aexp) for dy in (4e-3, 2e-3, 1e-3)}
        n1, n2, n4 = res["0.001"], res["0.002"], res["0.004"]
        res["norm_rel_change_4e-3_vs_1e-3"] = {"Linf": max(abs(a / b - 1) for a, b in zip(n4["Linf"], n1["Linf"])), "L2": max(abs(a / b - 1) for a, b in zip(n4["L2"], n1["L2"]))}
        res["exponent_spread_over_resolutions"] = {"Linf": max(abs(r["Linf_exponent"] - n1["Linf_exponent"]) for r in (n2, n4)), "L2": max(abs(r["L2_exponent"] - n1["L2_exponent"]) for r in (n2, n4))}
        out["profiles"][name] = res
    box = {str(ec): norms(bump_E, 4e-3, eta_c=ec)["L2"][0] for ec in (0.9, 0.99, 0.999)}
    out["eta_box_divergence_of_L2_at_tau_0.1"] = {"L2_bump": box, "ratio_0.99_over_0.9": box["0.99"] / box["0.9"], "ratio_0.999_over_0.99": box["0.999"] / box["0.99"],
                                                 "predicted_ratio_(1-eta_c)^(-1/2+3h)": 10 ** (0.5 - 3 * H),
                                                 "note": "the similarity field is z-independent K(r,tau) beyond X_ext (3.5): its L2(R^3) norm is infinite; a box in eta gives the bookkeeping power exactly"}
    # V2: the force the leading order alone needs, measured by finite differences on the bump field
    qs = [1e-2, 1e-3, 1e-4]; terms = {str(q): residual_terms(q) for q in qs}
    out["V2_force_of_prescribed_bump"] = {"terms": terms, "Linf_exponent_R_theta": slope(qs, [terms[str(q)]["max_R_theta"] for q in qs]), "expected_-A-1": -A - 1,
                                          "exponent_if_leading_stress_vanished_(axial_viscosity_only)": -A - 1 + 2 * H, "difference_2h": 2 * H}
    return out


# ---------------------------------------------------------------- (vi) S1-S3: support and the flat cutoff
def support(tg_heat, tg_noheat):
    mb = tg_heat["y"] >= 3.0
    out = {"heat": {"max_abs_Ttheta_beyond_Xb": float(np.max(np.abs(tg_heat["Tth"][mb]))), "calB_beyond": float(tg_heat["calB_h"][mb][0, 0])},
           "no_heat_honest": {"max_abs_Ttheta_beyond_Xb": float(np.max(np.abs(tg_noheat["Tth"][mb]))), "calB_beyond": float(tg_noheat["calB_h"][mb][0, 0])},
           "no_heat_faked_by_sqrtX_term_only": {"max_abs_TthetaA_beyond_Xb": float(np.max(np.abs(tg_noheat["TthA"][mb])))}}
    with np.errstate(divide="ignore", over="ignore"):
        chi = np.where(tg_noheat["y"] < 3.0, np.exp(-1.0 / np.maximum(3.0 - tg_noheat["y"], 1e-300) ** 2), 0.0)   # any smooth cutoff on the stress
    out["no_heat_faked_by_smooth_cutoff_on_stress"] = {"max_abs_beyond_Xb": float(np.max(np.abs(tg_noheat["Tth"][mb] * chi[mb, None])))}
    out["support_radius_r_b"] = {str(1 - tau): {"log10_r_b": float(0.5 * (np.log10(2 * tau) + (LOG_XT + 3) / np.log(10)))} for tau in (1e-2, 1e-4, 1e-6)}
    # S3: delta^N e^{4/delta^2} |d^k T| at N = 3k+3, for the paper cutoff and for a cutoff carrying e^{c/delta}
    y = tg_heat["y"]; dy = float(y[1] - y[0]); delta = tg_heat["delta"]
    That = tg_heat["pref"] * tg_heat["calA_h"] / tg_heat["L"][0]
    scale = That[np.argmin(np.abs(delta - 0.4))]
    def s3(hat, label):
        d1 = np.gradient(hat, dy); d2 = np.gradient(d1, dy)
        with np.errstate(divide="ignore", invalid="ignore"):
            e1 = d1 - (8 / delta ** 3) * hat                                       # e^{4/delta^2} d_y T
            e2 = d2 - 2 * (8 / delta ** 3) * d1 + ((8 / delta ** 3) ** 2 - 24 / delta ** 4) * hat
        Q1 = np.abs(delta ** 6 * e1) / scale; Q2 = np.abs(delta ** 9 * e2) / scale
        idx = {dd: int(np.argmin(np.abs(delta - dd))) for dd in (0.4, 0.2, 0.1, 0.05, 0.02)}
        k = int(round(0.02 / dy)); lp = lambda Q, i: float((np.log(Q[i - k]) - np.log(Q[i + k])) / (np.log(delta[i - k]) - np.log(delta[i + k])))
        r = {"k1_N6": {str(dd): float(Q1[i]) for dd, i in idx.items()}, "k2_N9": {str(dd): float(Q2[i]) for dd, i in idx.items()},
             "local_power_k1_at_0.05": lp(Q1, idx[0.05]), "local_power_k2_at_0.05": lp(Q2, idx[0.05])}
        four = [r["k1_N6"][s] for s in ("0.4", "0.2", "0.1", "0.05")]
        r["k1_nonincreasing_over_the_four_preregistered_delta"] = bool(all(four[i + 1] <= four[i] for i in range(3)))
        r["k1_ratio_0.02_over_0.05"] = r["k1_N6"]["0.02"] / r["k1_N6"]["0.05"]
        return r
    out["S3_paper_cutoff"] = s3(That, "paper")
    for c in (0.2, 0.5):
        with np.errstate(over="ignore", divide="ignore"):
            fake = That * np.exp(np.where(delta > 0, c / np.maximum(delta, 1e-300), 0.0))
        out[f"S3_fake_cutoff_exp(-4/d2+{c}/d)"] = s3(fake, f"fake{c}")
    return out


# ---------------------------------------------------------------- the artefact
TIER = "This is Tier 2, not a proof."

def artefact(r):
    P, P3, I, I2, V, S = r["P"], r["P3"], r["I"], r["I2"], r["V"], r["S"]
    al = P["b_aliasing_M_eq_2k"]; sch = P["c_exponent_is_the_window"]; bump = V["profiles"]["gaussian_bump_wrong_profile"]; v2 = V["V2_force_of_prescribed_bump"]
    att = []
    def add(gate, tried, numbers, verdict, fix):
        att.append({"gate": gate, "mis_specification_tried": tried, "numbers": numbers, "verdict": verdict, "what_would_make_it_non_fakeable": fix})
    add("P1", "Three fakes. (a) A pulse field that reproduces T_theta and sets T_z to zero or to minus itself, scored by the joint two-entry relative L2 error. "
              "(b) A phase-wrong pulse (u_theta shifted by pi/2, whose true averaged product with u_r is zero) averaged on M = 2N equispaced samples offset by phi0 = -pi/(4N) (aliasing of the 2N harmonic) at N in {8, 16, 32}. "
              "(c) The 'convergence exponent in N' measured with different averaging windows on the SAME exact field.",
        {"a_joint_rel_err_Tz_zero": P["a_norm_hides_Tz"]["rel_joint_err_Tz_set_to_zero"], "a_joint_rel_err_Tz_flipped": P["a_norm_hides_Tz"]["rel_joint_err_Tz_sign_flipped"],
         "a_log10_normTz_over_normTth_on_the_pinned_tail": P["a_norm_hides_Tz"]["log10_ratio_normTz_over_normTth"],
         "b_rel_err_phase_wrong_aliased_at_N": {N: al[N]["rel_err_phase_pi_over_2"] for N in al}, "b_rel_err_twin_aliased_at_N": {N: al[N]["rel_err_twin"] for N in al},
         "b_rel_err_phase_wrong_resolved_average": {N: al[N]["rel_err_phase_pi_over_2_with_resolved_average"] for N in al},
         "b_rel_err_amplitude_halved_aliased": {N: al[N]["rel_err_amplitude_halved"] for N in al},
         "c_fitted_exponent_by_window": {k: v["fitted_exponent"] for k, v in sch.items()}, "c_rel_err_at_4N0_by_window": {k: v["rel_err_at_N"]["32"] for k, v in sch.items()}},
        "FAKEABLE",
        "(a) Score the two entries separately (T_z/T_theta ~ 1e-136 on this profile: a joint norm cannot see T_z at all). "
        "(b) A Nyquist check on the averaging grid itself: <cos^2(N phi)> = 1/2 and <cos(N phi) sin(N phi)> = 0 to roundoff, plus a resolution study in the number of samples M (M >= 4N+1 or an exact period average); "
        "note the pre-registered pi/2 control does NOT fire under the aliased average (error 5.8e-16 at N = 8 against the required > 0.3) while the twin passes, so the control alone is not protection. "
        "(c) Report the averaging quadrature and show the error is below the quoted order at every N; with an exact period average the error is roundoff (~1e-15) at every N and no exponent exists to fit — the paper's (7.26) C(W0) = eps T0,* is exact, not asymptotic in N.")
    add("P2", "The P1 windows carried into the divergence: a theta-window (fixed angular window pi/(6 N0)) whose error multiplies T by a constant c(N), and a y-window (radial phase N y, window pi/(3 N0)) whose error oscillates in y.",
        {"theta_window": P["P2"]["theta_window_exponents"], "y_window": P["P2"]["y_window_exponents"], "per_N": P["P2"]["per_N"],
         "aliased_fake_div_error_is_roundoff": "the P1(b) aliased field has error ~1e-15 at every N, so its div error is roundoff too"},
        "FAKEABLE",
        "P2 'at the same exponent' catches only errors that vary along the divergence direction (the y-window fails it: P1 exponent -1.01, P2 exponent +0.01). Any multiplicative error (angular window, wrong constant, aliasing) passes trivially. "
        "Non-fakeable version: the div residual must be measured on an independent resolution of the fast phase (M doubled) and shown unchanged, and the pi/2 control must be run through the same averaging as the twin with a Nyquist check.")
    add("P3", "An ansatz whose 'lower-order term' is a q-independent 30% of the leading term (exponent 0), and one that drifts as q^0.04; both compared with the gate's +-0.05 window around the claimed 2h. "
              "Also measured: the actual axial/radial viscosity ratio of a prescribed leading field on the pinned annulus by finite differences in physical coordinates.",
        {"measured_exponent_axial_over_radial": P3["measured_exponent"], "claimed_2h": P3["claimed_exponent_2h"], "measured_ratio_at_q": P3["measured_axial_over_radial_ratio"],
         "q^2h_at_q": P3["q^2h_at_the_three_q"], "fake_constant_exponent": P3["fake_constant_ratio_exponent"], "fake_constant_passes": P3["fake_constant_passes_pm0.05"],
         "fake_drift_exponent": P3["fake_drift_0.04_exponent"], "fake_drift_passes": P3["fake_drift_passes_pm0.05"], "tolerance_over_signal_h_1e-7": P3["tolerance_over_signal"], "tolerance_over_signal_h_1e-3": P3["at_h_1e-3_tolerance_over_signal"]},
        "FAKEABLE",
        "At h = 1e-7 the claimed factor q^{2h} is 1 - 1.8e-6 at q = 1e-4: the gate's +-0.05 exponent window is 2.5e5 times the signal, so a constant ratio (exponent 0) and a q^0.04 drift both pass. "
        "Non-fakeable: a tolerance scaled to h (say +-0.5 h) with the ratio resolved to 1e-9 relative (the FD measurement here does reach 2.0096e-7 vs 2e-7), or a calibration run at a synthetic large h where q^{2h} is O(1). "
        "Honest finding on the instantiated profile: the exponent is right but the prefactor is 2.2e207 — on the pinned tail (X_tail ~ 1e207) axial viscosity EXCEEDS radial viscosity by 2X q^{2h}; the paper's q^{2h} hierarchy is a statement at fixed X = O(1), not at this profile's annulus.")
    add("I1", "Fake A: a 'correction stage' that absorbs all but a q^{1/10} fraction of the source (the ansatz assumes the 1/10). Fake B: a genuine linear solve (u' + u = S, backward Euler) whose leftover is grid error, with the grid tied to q (n = 100 (q/1e-2)^{-0.1}). "
              "Also: the paper's per-stage gain converted to a q-exponent, against the gate's +-0.02 window.",
        {"fakeA_gain_stage1": I["fakeA_builtin"]["gain_stage1"], "fakeA_R1_over_R0": I["fakeA_builtin"]["R1_over_R0"], "fakeB_gain_stage1": I["fakeB_grid_tied_to_q"]["gain_stage1"],
         "fakeB_leftover_at_q": I["fakeB_grid_tied_to_q"]["rel_leftover_stage1"], "fakeB_same_solve_fixed_grid_gain": I["fakeB_grid_tied_to_q"]["same_solve_fixed_grid_gain"],
         "paper_gain_as_q_exponent_h_over_10": I["paper_gain_in_q_exponent"], "zero_correction_control_gain": I["zero_correction_control_gain"],
         "zero_correction_control_within_0.02_of_paper_q_gain": I["zero_correction_control_within_0.02_of_paper_q_gain"], "log_eps_range_over_q_1e-2_to_1e-4": I["log_eps_range_over_q_1e-2_to_1e-4"],
         "R0_norm_on_annulus_at_q": I["R0_norm"]},
        "FAKEABLE",
        "sigma_{j+1} = sigma_j + 1/10 in (9.8) is an exponent of eps = q^h (Lemma 9.8: g_j = h j/10), so in q the claimed gain is h/10 = 1e-8: the gate's +-0.02 window then admits the zero-correction control (gain 0) — the control cannot fire. "
        "Read as an eps-exponent instead, the fit spans log eps = 4.6e-7 over q in [1e-4, 1e-2] and needs the residual norms to ~1e-9 relative. "
        "Non-fakeable: state which variable (q or eps) the exponent is in before running; measure at h = 1e-3 as well (gain 1e-4 in q, still below 0.02 — the gate window must be tied to h); show the correction is the solution of the paper's linear problem (8.20)/(8.25) sourced by the measured residual, with a fixed-grid resolution study (fake B collapses to gain 2e-16 on a fixed grid).")
    add("I2", "The closing rows of Prop 9.6 (p. 111) implemented as arithmetic, then re-run with wrong inputs: kappa_s in {0.03, 1/30, 0.04}, B_0 = 0.75, and the row-4 constant 0.17 replaced by 0.11.",
        {"paper_kappa_1e-5": {"all_rows_hold": I2["paper"]["all_rows_hold"], "margins_vs_threshold": I2["paper"]["margins_vs_threshold"], "smallest_value_minus_0.1": I2["paper"]["smallest_value_minus_0.1"]},
         "kappa_0.03_all_rows_hold": I2["kappa_0.03"]["all_rows_hold"], "kappa_1_over_30_all_rows_hold": I2["kappa_1_over_30"]["all_rows_hold"], "kappa_0.04_all_rows_hold": I2["kappa_0.04"]["all_rows_hold"],
         "B0_0.75_all_rows_hold": I2["B0_0.75"]["all_rows_hold"], "c4_0.11_all_rows_hold": I2["c4_0.11"]["all_rows_hold"], "c4_0.11_smallest_value_minus_0.1": I2["c4_0.11"]["smallest_value_minus_0.1"],
         "sigma_j": I2["paper"]["sigma_j"]},
        "FAKEABLE",
        "The ledger passes for every kappa_s <= 1/30 (the paper's is 1e-5), for any B_0 >= 0.7 and for any row-4 constant > 0.1: two rows hold with margin exactly 0 as identities in kappa_s, the '+1/10' is the definition (9.8), and Prop 9.9's summation needs only h sigma_j -> infinity. "
        "It is arithmetic on quoted constants and cannot fail unless the constants are mistranscribed; it is not a measurement of the construction. Non-fakeable: derive B_0 = 0.7 and the 0.17 from the term table (9.11)-(9.14) rather than quote them, and record the kappa_s = 1/30 boundary as the ledger's only content.")
    add("I3", "Fake A repeated (second stage multiplies by q^{1/10} again); fake B repeated (second backward-Euler solve sourced by the first leftover, same q-tied grid).",
        {"fakeA_gain_stage2": I["fakeA_builtin"]["gain_stage2"], "fakeB_gain_stage2": I["fakeB_grid_tied_to_q"]["gain_stage2"], "fakeB_leftover_stage2_at_q": I["fakeB_grid_tied_to_q"]["rel_leftover_stage2"]},
        "FAKEABLE",
        "Fake A repeats exactly (0.1, 0.1) because the gain is built in; fake B did NOT repeat (0.105 then 0.047) — a grid artefact does not compound cleanly, so 'the gain repeats' has some power against resolution artefacts but none against an ansatz. "
        "Non-fakeable: the two stages must be the paper's operators with the pre-stated exponent variable, and a planted control (a source that the linear problem cannot reduce, e.g. one in the kernel of the mean-correction operator) must show gain 0.")
    add("V1", "Any prescribed profile: a Gaussian bump in y with no cutoff and no heat factor (the wrong profile), the pinned tail shape, and the A -> 0.85 control, each at dy in {4, 2, 1}e-3, norms over |eta| <= 0.9, y in [0.5, 3].",
        {"claimed_Linf_exponent": V["claimed_Linf_exponent"], "claimed_L2_exponent_(1+D-2A)/2": V["claimed_bookkeeping_L2_exponent"],
         "bump_Linf_exponent_dy_4e-3": bump["0.004"]["Linf_exponent"], "bump_L2_exponent_dy_4e-3": bump["0.004"]["L2_exponent"], "bump_exponent_spread_over_resolutions": bump["exponent_spread_over_resolutions"],
         "bump_norm_rel_change_4e-3_vs_1e-3": bump["norm_rel_change_4e-3_vs_1e-3"],
         "pinned_tail_shape_exponents_dy_1e-3": {"Linf": V["profiles"]["pinned_tail_shape"]["0.001"]["Linf_exponent"], "L2": V["profiles"]["pinned_tail_shape"]["0.001"]["L2_exponent"]},
         "A_0.85_control_L2_exponent": V["profiles"]["bump_A_0.85_control"]["0.001"]["L2_exponent"],
         "eta_box_L2_at_tau_0.1_for_eta_c_0.9_0.99_0.999": V["eta_box_divergence_of_L2_at_tau_0.1"]["L2_bump"]},
        "FAKEABLE",
        "The norms of u = q^{-A} E(X, eta) factorise exactly: L_inf = tau^{-A} sup(d^A E) and L2 = tau^{(1+D-2A)/2} x (a q-independent quadrature), so every profile — right or wrong, divergence-free or not — gives the bookkeeping exponents to 1e-10 at every resolution, and 'stable across resolutions' tests only the quadrature of int E^2. "
        "The A -> 0.85 control is the same arithmetic. Beyond X_ext the leading field is the z-independent heat swirl K(r, tau) e_theta (3.5), so ||u^(0)(t)||_{L2(R^3)} is infinite and any finite value is a choice of box (the box norm grew 1.30e104 -> 1.97e104 -> 5.09e104 as eta_c -> 1). "
        "Nothing makes this gate evidence of Navier-Stokes blowup: any prescribed u solves NS with f := NS(u). It is a correct Jacobian identity and no more.")
    add("V2", "Report gate (no YES to fake): the theta-momentum residual of the prescribed bump field measured by finite differences in physical coordinates at q in {1e-2, 1e-3, 1e-4}.",
        {"Linf_exponent_R_theta": v2["Linf_exponent_R_theta"], "expected_-A-1": v2["expected_-A-1"], "exponent_if_leading_stress_vanished": v2["exponent_if_leading_stress_vanished_(axial_viscosity_only)"],
         "max_R_theta_at_q": {q: v2["terms"][q]["max_R_theta"] for q in v2["terms"]}, "max_dt_u_at_q": {q: v2["terms"][q]["max_dt"] for q in v2["terms"]},
         "max_axial_visc_at_q": {q: v2["terms"][q]["max_axial_visc"] for q in v2["terms"]}, "max_radial_visc_at_q": {q: v2["terms"][q]["max_radial_visc"] for q in v2["terms"]}},
        "NOT FAKEABLE",
        "There is no YES to fake: the gate asks for a number and a sentence. But the number is uninformative: every prescribed leading field gives -A-1 = -1.5000001 (measured -1.4999999 on the bump), and a profile whose leading stress vanished exactly would give -A-1+2h — a difference of 2e-7 against the gate's +-0.01. "
        "The reported gap is real (the leading force diverges like q^{-1.5}) but cannot distinguish a good profile from a bad one at this h. On the pinned annulus the residual is dominated by axial viscosity (X ~ 1e207), not by the paper's leading balance.")
    add("V3", "The V1 fake's refinement stability: the bump's exponents and norms across dy in {4, 2, 1}e-3.",
        {"bump_exponent_spread": bump["exponent_spread_over_resolutions"], "bump_norm_rel_change": bump["norm_rel_change_4e-3_vs_1e-3"], "pinned_tail_norm_rel_change": V["profiles"]["pinned_tail_shape"]["norm_rel_change_4e-3_vs_1e-3"]},
        "FAKEABLE",
        "Refinement stability of a prescribed field's norm fits is automatic (the q-dependence factors out of the quadrature; exponent spread 0 to 5e-15 for the wrong profile). T* = 1 is prescribed and cannot be tested on any prescribed field; the gate already says so. "
        "Non-fakeable only in a solve: T* from a time-integrated NS solution from data, stable under refinement.")
    add("S1", "Drop the heat factor (the honest control, T_theta beyond X_b nonzero), then (i) evaluate only the sqrt(X) term E_pow sqrt(X/2) calA/L, discarding B/X (which is 1e-207 relative to calA inside the annulus), or (ii) multiply the stress by any smooth cutoff vanishing at y >= 3.",
        {"heat_max_abs_Ttheta_beyond_Xb": S["heat"]["max_abs_Ttheta_beyond_Xb"], "no_heat_honest_max_abs_Ttheta_beyond_Xb": S["no_heat_honest"]["max_abs_Ttheta_beyond_Xb"], "no_heat_calB_beyond": S["no_heat_honest"]["calB_beyond"],
         "no_heat_sqrtX_term_only_beyond_Xb": S["no_heat_faked_by_sqrtX_term_only"]["max_abs_TthetaA_beyond_Xb"], "no_heat_smooth_cutoff_on_stress_beyond_Xb": S["no_heat_faked_by_smooth_cutoff_on_stress"]["max_abs_beyond_Xb"],
         "log10_support_radius_r_b_at_t": {t: v["log10_r_b"] for t, v in S["support_radius_r_b"].items()}},
        "FAKEABLE",
        "Exact zero beyond X_b is a property of the (A.12) cutoff psi_o for the sqrt(X) term (calA = 0 for y >= 3 with or without the heat factor); only the 1/X bracket B carries the heat-factor content (-(2+2h) without it), and B/X is 1e-207 relative — one 'leading-order' truncation, or any cutoff applied to the stress rather than to the profile, produces the exact zero for the wrong profile. "
        "Non-fakeable: derive T_0 from E through (4.11) with the moments carried exactly, run the kappa -> 0 control through the same pipeline and require calB(y >= 3) = -(2+2h) (leg 432's K6), and report B separately from A. "
        "Honest instantiation: r_b(t) = sqrt(2 q X_b) is 1e103 at t = 1 - 1e-2 and 1e101 at t = 1 - 1e-6 — the support 'shrinks to zero' only as a scaling; at every computable t it is astronomically large on this lambda = 0.1 profile.")
    add("S2", "The support clauses of Prop 10.1 applied to the wrong (bump) field: multiplication by chi_x chi_t gives compact support in K and zero initial datum for ANY field; the flatness clause (10.6)/(10.9) checked against the bump's measured force.",
        {"support_after_cutoff": "subset of K = supp chi_x for every field, by construction (tautology; no number)", "force_Linf_exponent_of_leading_order": v2["Linf_exponent_R_theta"],
         "max_force_at_q": {q: v2["terms"][q]["max_R_theta"] for q in v2["terms"]}},
        "FAKEABLE",
        "The checkable clauses (support in X <= X_ext, the time window, u = p = 0 for small t) are satisfied by any field once the paper's cutoffs are applied — they test the cutoffs, not the field. The one clause with content, flatness at t = 1, is NOT fakeable: the leading force grows like q^{-1.5} (5.1e3 -> 1.6e5 -> 5.1e6 over q = 1e-2 -> 1e-4) and no cutoff makes a divergent force flat; the gate already tells the worker not to claim it. "
        "Non-fakeable: state that S2's YES-able clauses are tautologies and report only the exponent gap.")
    add("S3", "A cutoff violating (A.51): multiply the pinned flat hat by e^{c/delta} (c = 0.2 and c = 0.5), so the true weight is e^{-4/delta^2 + c/delta}, then test delta^N e^{4/delta^2} |d^k T| at the four pre-registered delta with N = 3k+3.",
        {"paper_cutoff_k1_N6": S["S3_paper_cutoff"]["k1_N6"], "paper_local_power_k1_at_0.05": S["S3_paper_cutoff"]["local_power_k1_at_0.05"],
         "fake_c_0.2_k1_N6": S["S3_fake_cutoff_exp(-4/d2+0.2/d)"]["k1_N6"], "fake_c_0.2_nonincreasing_over_four_delta": S["S3_fake_cutoff_exp(-4/d2+0.2/d)"]["k1_nonincreasing_over_the_four_preregistered_delta"],
         "fake_c_0.2_local_power_k1_at_0.05": S["S3_fake_cutoff_exp(-4/d2+0.2/d)"]["local_power_k1_at_0.05"], "fake_c_0.2_ratio_0.02_over_0.05": S["S3_fake_cutoff_exp(-4/d2+0.2/d)"]["k1_ratio_0.02_over_0.05"],
         "fake_c_0.5_k1_N6": S["S3_fake_cutoff_exp(-4/d2+0.5/d)"]["k1_N6"], "fake_c_0.5_nonincreasing_over_four_delta": S["S3_fake_cutoff_exp(-4/d2+0.5/d)"]["k1_nonincreasing_over_the_four_preregistered_delta"],
         "fake_c_0.2_k2_N9": S["S3_fake_cutoff_exp(-4/d2+0.2/d)"]["k2_N9"]},
        "FAKEABLE",
        "With c = 0.2 the quantity is bounded AND non-increasing over delta in {0.4, 0.2, 0.1, 0.05} (0.85, 0.12, 0.037, 0.032) although the cutoff violates (A.51) — e^{0.2/delta} is not polynomially bounded; the violation shows only at delta = 0.02 (0.81, ratio 25 over delta = 0.05) or in the local log-slope at delta = 0.05 (-1.45 against +3.05 for the paper cutoff). c = 0.5 is caught at delta = 0.05 (13.1). "
        "Non-fakeable: add delta = 0.02 and 0.01 (carried as hats, nothing underflows) and require the local slope of delta^N e^{4/delta^2}|d^k T| in log delta to be >= 0 at the smallest delta.")
    verdicts = {a["gate"]: a["verdict"] for a in att}
    X2 = ("Verdict. (iii) P1-P2 are not evidence as gated: the averaged product of a prescribed pulse pair reproduces the target by construction (the paper's (7.26) is exact), the joint norm cannot see T_z (1e-136 relative on this profile), aliasing at M = 2N makes a phase-wrong field pass and the pi/2 control not fire, and the 'convergence exponent in N' is a property of the averaging window (-1, -0.16, -0.38, -346 or undefined on the same field). "
          "P3 is not evidence at h = 1e-7: the tolerance is 2.5e5 times the signal 2h; the q^{2h} scaling itself is real (measured 2.0096e-7) but on the pinned annulus axial viscosity exceeds radial by 2X ~ 2e207, so the hierarchy is a scaling, not an instantiation. "
          "(iv) I1/I3 are not evidence: the +1/10 is an eps-exponent (h/10 = 1e-8 in q), so the +-0.02 window admits the zero-correction control, an ansatz that assumes the gain measures it exactly, and a q-tied grid measures 0.105 from a solve that has gain 2e-16 on a fixed grid; I2 is arithmetic on quoted constants that holds for every kappa_s <= 1/30 — a transcription check, not a measurement. "
          "(v) V1/V3 are Jacobian identities of any prescribed field (exponents exact to 1e-10 for a wrong Gaussian profile; the R^3 norm of the similarity field is infinite and the finite value is a box choice); V2 is an honest report of a real gap (force ~ q^{-1.5}) whose exponent cannot tell a good profile from a bad one at this h. "
          "(vi) S1's exact zero is fakeable by truncating to the sqrt(X) term or cutting off the stress instead of the profile, and the instantiated support radius is 1e101-1e103; S2's checkable clauses are tautologies of the cutoffs, its flatness clause is the only content and is a gap the leading order cannot close; S3's boundedness at four delta admits a cutoff violating (A.51). "
          "What IS evidence in wave 4, if the workers did it: a two-route agreement (leg 432 style) on a quantity the adversary could not choose — the sign and shape of T_0, the exact zero of calB with the heat factor against -(2+2h) without it, the local delta-slopes of the flat weight, and the measured 2h scaling of the viscous ratio. "
          "None of (iii)-(vi)'s YES gates, as defined, is evidence that the paper's construction works; each is consistent with the paper's algebra being transcribed correctly. " + TIER)
    out = {"schema": "arc6_wave4_v1", "agent": 7, "unit": "(vii) adversary", "leg": 433, "pdf_sha256": PDF_SHA,
           "pages_read": [4, 7, 8, 9, 15, 24, 25, 26, 27, 69, 81, 82, 83, 84, 106, 107, 109, 110, 111, 113, 114, 115, 116, 117, 118, 119, 120, 140],
           "inputs": {"profile": "writeup/data/arc6_profile_v1.json (leg 430, lambda = 0.1): log X_tail = %.6f, c_inf = %.6e" % (LOG_XT, C_INF), "stress": "leg_432_prereg_amend.md section 1 formulas via arc6_residual_v1.Tail; h = 1e-7, dy = 1e-3, Chebyshev 17 in eta",
                      "what_the_adversary_saw": "only leg_433_prereg.md section 2's gate definitions, the pinned artefacts, the manuscript text and the two runners; no worker file"},
           "claimed": {"P1": "Prop 7.5 (7.26), p. 82: C(W0) = eps T0,* exactly; columns carry errors |e_sigma| <= C S_*^{-1/2} (7.28), p. 83",
                       "I1": "(9.8), p. 106: sigma_j = 1/5 + j/10 as an exponent of eps = q^h; Lemma 9.8 (9.17), p. 113: g_j = h j/10 in q",
                       "V1": "(3.2), (4.3), p. 7 and p. 25: u_theta = q^{-A} E, u_z = q^{-A} U, z = q^D eta, X = r^2/(2q), tau = q(1 - eta^2)",
                       "S1": "Theorem 3.1(iii), p. 15; Lemma A.8, p. 140; S3: (A.51) via the (A.12) cutoff"},
           "attempts": att, "gates": {"X1": verdicts, "X2": X2},
           "measured": r,
           "instantiated_vs_scaled": "Every fake here is instantiated at the pinned lambda = 0.1 profile (X_tail ~ 1e207, T_theta ~ 1e-39, T_z ~ 1e-175); the paper's regime (lambda <~ 3e-4, X = O(1)) is reached by none of them. Two of the honest measurements are scalings only: the 2h exponent of the viscous ratio (real, prefactor 2e207) and the support radius r_b ~ 1e103 sqrt(q).",
           "could_not_determine": ["I could not fake V2, because it has no YES to fake (it is a report gate); I could only show its number is profile-blind at this h.",
                                   "I could not fake S2's flatness clause, because a force growing like q^{-1.5} cannot be made flat by any cutoff; the gate already forbids claiming it.",
                                   "I could not make fake B (a q-tied grid) repeat its gain at the second stage (0.105 then 0.047); I3 is fakeable only by the built-in ansatz.",
                                   "I could not fake S3 with c = 0.5 at the four pre-registered delta (caught at delta = 0.05); only c = 0.2 passes them.",
                                   "I did not attempt to fake the leg-432 controls themselves (K1-K6); they were not in section 2's gate list."],
           "tier": TIER, "runtime_s": r["runtime_s"]}
    return out


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    t0 = time.time(); res = {}
    tg = target(heat=True); tg_nh = target(heat=False); print(f"[{time.time()-t0:.0f}s] targets built")
    res["P"] = pulses(tg); print(f"[{time.time()-t0:.0f}s] P1/P2 done")
    res["P3"] = p3_hierarchy(); print(f"[{time.time()-t0:.0f}s] P3 done")
    res["I"] = iteration(tg); print(f"[{time.time()-t0:.0f}s] I1/I3 done")
    res["I2"] = {"paper": ledger(), "kappa_0.03": ledger(0.03), "kappa_1_over_30": ledger(1 / 30), "kappa_0.04": ledger(0.04), "B0_0.75": ledger(B=0.75), "c4_0.11": ledger(c4=0.11)}
    res["V"] = headline(); print(f"[{time.time()-t0:.0f}s] V done")
    res["S"] = support(tg, tg_nh); print(f"[{time.time()-t0:.0f}s] S done")
    res["runtime_s"] = time.time() - t0
    out = artefact(res)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, default=float) + "\n")
    print(json.dumps(out["gates"], indent=1)); print("wrote", OUT, f"{OUT.stat().st_size:,} B in {time.time()-t0:.0f}s")
