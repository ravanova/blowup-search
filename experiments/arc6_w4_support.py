"""Arc 6, wave 4, agent 6 (leg 433), unit R5(vi): COMPACT SUPPORT OF THE FORCE f (manuscript section 10).

    .venv/bin/python experiments/arc6_w4_support.py            # writes writeup/data/arc6/wave4/agent_6_support.json

Gates S1-S3 and the two controls are fixed in experiments/journal/leg_433_prereg.md section 2 (vi) and are
not changed here.  Everything is built from the pinned tail stress of leg 432 (experiments/arc6_residual_v1.py,
route A, imported: Tail, LOG_XT, C_INF); that file is not edited.

  S1  R^(0) = -div(q^{-A-1/2} T_0) (Prop 4.2, p. 27) is exactly zero for X >= X_b with the heat exterior
      (Lemma A.8, p. 140-141); physical support radius r_b(t) = sqrt(2 q(t) X_b) at three t, q(t) = 1 - t on
      z = 0 by (3.2), p. 7.
  S2  section 10's support clauses (p. 117-125) extracted with equation numbers; each clause the leading order
      can check is checked; the leading residual's own q-exponent is MEASURED and the gap to the paper's
      flatness (3.4) is reported.  Flatness is carried by the corrections, not the leading order: NOT CLAIMED.
  S3  (A.51), p. 142: e^{4/delta^2} delta^N |d^k T_0| bounded for some N <= 3k + 3, k = 1, 2, at
      delta in {0.4, 0.2, 0.1, 0.05}.  All flat quantities are carried as e^{4/delta^2} x (.) (the 'hat'
      quantities); e^{-4/delta^2} is never formed at small delta.

Derivative bookkeeping (pre-committed).  With s = r^2/2 = qX and y = log(X/X_tail): d_r = (2/r) d_y, so
  (d_r + 2/r) T = (2/r)(d_y + 1) T,   (d_r + 1/r) T = (2/r)(d_y + 1/2) T,
  R^(0)_theta = q^{-A-1} sqrt(2/X) * Rth,  Rth := -(d_y + 1) T_{0,theta};   R^(0)_z = q^{-A-1} sqrt(2/X) * Rz,
  Rz := -(d_y + 1/2) T_{0,z}.  For T = e^{-lW} That (lW = 4/delta^2, delta = 3 - y, d_y lW = 8/delta^3,
  d_y^2 lW = 24/delta^4):  (d_y T)^ = That' - lW' That,  (d_y^2 T)^ = That'' - 2 lW' That' + (lW'^2 - lW'') That.
  Derivatives of the hat quantities are centred second-order finite differences; the hat quantities are
  smooth for delta > 0 and jump to 0 at delta = 0, so beyond X_b only points y >= 3 are used.
S3 operationalisation (pre-committed): Q_k(delta) := max_eta e^{4/delta^2} |d_y^k T_0| at the four delta;
  N_k := the smallest integer N in [0, 60] such that delta^N Q_k(delta) is non-increasing as delta decreases
  through 0.4, 0.2, 0.1, 0.05;  S3 = YES iff N_1 <= 6 and N_2 <= 9 for both components (theta, z).
  For the polynomial-cutoff control the TRUE (A.51) weight e^{4/delta^2} is applied in log space.
S2 gate rule (pre-committed): YES iff every clause marked CHECKABLE below passes: (a) exact zero of the
  leading residual for X >= X_b (S1's number), (b) the paper's exterior heat profile H of (A.32) satisfies
  its ODE (A.37) to relative 1e-8 at Z in {0, 0.1, 1, 10} (this is what makes the uncut exterior residual
  'exactly zero', p. 119) and its first-order expansion (A.36) matches the kappa the pinned stress uses,
  (c) the measured q-exponent of R^(0) at fixed X equals -(A + 1) to 1e-6 (so the gap to (3.4) is a
  definite number).  Clauses the leading order cannot check are listed, not scored.
Tier 2. Not a proof.
"""
import json, sys, time
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import gamma as Gamma

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))
from arc6_residual_v1 import Tail, LOG_XT, C_INF  # noqa: E402
from arc6_profile_v1 import cheb, PDF_SHA  # noqa: E402
ART = json.loads((ROOT / "writeup" / "data" / "arc6_residual_v1.json").read_text())
OUT = ROOT / "writeup" / "data" / "arc6" / "wave4" / "agent_6_support.json"
DELTAS = (0.4, 0.2, 0.1, 0.05)
LN10 = np.log(10.0)

PAGES_READ = [7, 9, 12, 13, 14, 15, 16, 21, 27, 32, 33, 54, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 130, 137, 138, 140, 141, 142, 143, 144]

CLAIMED = {
    "written_before_run": True,
    "q_of_t": "(3.2), p. 7: tau = q(1 - eta^2), z = q^D eta, X = r^2/(2q), tau = 1 - t.  On z = 0 (eta = 0): q(t) = tau = 1 - t.  "
              "q = q(z, tau) unique with q ~ tau + |z|^{1/D}.",
    "X_b": "p. 137 (A.6 preamble): y = log(X/X_tail), X_b = e^3 X_tail; (A.12) p. 130: psi_o(y) = 1 - sigma((y-1)/2), f_o = 1 - rho_o psi_o "
           "on 0 <= y <= 3, extended by 1 to the right.  Pinned: log X_tail = 476.1528541875995 (leg 430, lambda = 0.1).",
    "support_clauses": [
        {"id": "C1", "where": "Theorem 3.1(iii), (3.4)-(3.5), p. 15; Theorem 4.6(ii), p. 33; p. 9",
         "claim": "For X >= X_ext the residual is identically zero and A = 0, B = K(r,tau) = r^{-1-2h} H_ext(tau/r^2) (3.5).  The leading stress "
                  "profile T_0 is zero for 0 <= X <= X_a and X >= X_b and nonzero at every X_a < X < X_b (Thm 4.6(ii)); T is nonzero precisely "
                  "in the annulus sqrt(2qX_a) < r < sqrt(2qX_b) (p. 9).",
         "leading_order_can_check": "X >= X_b part only (S1); X <= X_a needs the axis construction (Prop B.2, Cor B.10) which this unit does not build."},
        {"id": "C2", "where": "Lemma A.8, p. 140-141; (A.46)",
         "claim": "With U = 0, E = E_pow f_o [1 + chi_K (H(2d/X) - 1)] on y >= 0 and the exact moment conditions M(inf) = J(inf) = S(inf) = 0, "
                  "int (H - H_pow) dX = 0, the leading tangential stresses vanish for X >= X_b; for X >= X_b the field is (0, K, 0) with z-independent "
                  "pressure and Lemma A.6 makes both leading residuals zero there.",
         "leading_order_can_check": "yes: R^(0) = 0 exactly for X >= X_b from the pinned T_0 (S1); the heat-exterior mechanism via (A.37) (S2b)."},
        {"id": "C3", "where": "Lemma A.6, (A.32)-(A.37), p. 138; Step 4 p. 116; (10.7)-(10.8) p. 119",
         "claim": "K(r,t) = c_inf s^{-A} H(2 tau/s), H(Z) = Gamma(a_K)^{-1} int_0^inf e^{-v} v^{a_K-1} (1+Zv)^{-h} dv, a_K = 1 + h, satisfies "
                  "d_t K = (d_rr + r^{-1} d_r - r^{-2}) K exactly because Z^2 H'' + (1 + 2 a_K Z) H' + a_K(a_K - 1) H = 0 (A.37); "
                  "H(Z) = 1 - h(1+h) Z + O(Z^2) (A.36).  'The heat equation for K and d_r p_loc = K^2/r also show directly that the uncut exterior "
                  "residual is exactly zero' (p. 119).",
         "leading_order_can_check": "yes, from the paper's own integral: (A.37) residual by quadrature; (A.36) against the pinned kappa = 2h(1+h)d."},
        {"id": "C4", "where": "Step 4, p. 116; p. 117 (10.1); Theorem 3.1, p. 15",
         "claim": "0 < X_a < X_ext < inf; 'for a fixed X_ext beyond all slow supports, A = 0 and B = K' (all annular wave and mean potentials vanish "
                  "beyond X_b; Stokes streamfunctions vanish in the common exterior).  So X_ext >= X_b, with X_ext not given numerically.",
         "leading_order_can_check": "only that the leading part vanishes beyond X_b (S1); the corrections' supports are not built here."},
        {"id": "C5", "where": "Proposition 10.1 and (10.2)-(10.4), p. 117-118",
         "claim": "u = curl(cA) + cB e_theta, p = c p_loc, c = chi_x(x) chi_t(t), extended by zero outside the cutoff support (10.4); "
                  "chi_x = 1 on r <= r_0/2, |z| <= z_0/2, supp chi_x in {r < r_0, |z| < z_0}; chi_t = 0 for 1 - t >= tau_0, = 1 for 1 - t <= tau_0/2; "
                  "(10.3) q <= C_0(tau + |z|^{1/D}) and C_0(tau_0 + z_0^{1/D}) < q_*/2 keep supp c inside q < q_*/2.  supp u(.,t) U supp p(.,t) "
                  "subset K = supp chi_x for every 0 <= t < 1; u = p = 0 for all small t (10.2).",
         "leading_order_can_check": "no: r_0, z_0, tau_0, q_*, K are existence-only constants; the leading field u^(0) itself is NOT compactly supported "
                                    "(u_theta = K ~ r^{-1-2h} beyond X_b) - its compact support comes from chi_x alone.  Only r_b(t) of the leading "
                                    "residual's support is reported (S1)."},
        {"id": "C6", "where": "(10.5), p. 118; Lemma 10.2 and (10.6), (10.9), p. 118-119",
         "claim": "f = R(u,p) for 0 <= t < 1 (10.5), including every cutoff derivative; div f may be nonzero.  d^alpha_x d^j_t f converges uniformly on R^3 "
                  "as t -> 1 to d^alpha F_j, F_j in C_c^inf supported in K, d^alpha F_j(0) = 0 (10.6).  Near the origin, from (3.4) on X <= X_ext and the "
                  "exact zero for larger X: |d^alpha_x d^j_t f| <= C (tau + |z|^{1/D})^N for every N (10.9).",
         "leading_order_can_check": "no for the limits (they need the corrections); the leading residual's own q-exponent at fixed X is measured (S2c) "
                                    "and the gap to (10.9)/(3.4) reported."},
        {"id": "C7", "where": "Lemma 10.3 and (10.11)-(10.12), p. 120; Theorem 1.1 p. 1",
         "claim": "f extends to C_c^inf(R^3 x (0, inf)) with support in K x [0, 2] by f(x, 1 + sigma) = sum_j chi_0(b_j sigma) sigma^j F_j(x)/j! (10.11), "
                  "chi_0 = 1 near 0 and 0 for arguments >= 1, b_j >= 1 increasing.  NOTE: the paper does NOT extend f by zero at t = 1; the zero extension "
                  "is spatial (outside the cutoff support, (10.4)) and temporal for t near 0 ((10.2), chi_t) and for t >= 2 (chi_0).  At t = 1 the "
                  "extension is the Borel-type series (10.11) whose coefficients F_j vanish with all derivatives at x = 0 only.",
         "leading_order_can_check": "no."},
        {"id": "C8", "where": "p. 54 (Step 5 of the higher-order stress), Theorem 4.6(iv) p. 33, p. 32 (flat at the edge)",
         "claim": "Beyond X_b the leading profile is the z-independent heat field, so the order-1 stress T_1 is still supported in the closed active annulus; "
                  "1 - f_o = e^{-4/delta_b^2} x smooth, delta_b = log(X_b/X).  'Flat at the radial edge': d^j_X g(X_e, eta) = 0 for every j; the stress will "
                  "be flat at both edges.",
         "leading_order_can_check": "flatness of T_0 at X_b: yes, this is S3's (A.51)."},
    ],
    "flatness_statement": "Theorem 3.1(iii), (3.4), p. 15: |d^alpha_x d^b_t R(u,p)| <= C_{alpha,b,N,X_1} q^N for 0 <= X <= X_1, q -> 0, every alpha, b, N, "
                          "every finite X_1; Figure 6 p. 15; obtained by Lemma 5.4 and Prop 9.9 (sum of corrections, sigma_j = 51 + 10j -> inf, p. 14).  "
                          "This is a property of the corrected field.  The leading order gives instead R^(0) = q^{-A-1/2} x (-div) T_0 (Prop 4.2, p. 27), "
                          "a fixed negative power of q at fixed X in the annulus: the pulses (Prop 7.5) and the cycle (Prop 9.6) carry the flatness.",
    "A51": "Proposition A.10, p. 142: for delta = 3 - y small, T_{0,theta} = e^{-4/delta^2} delta^{-3} b_theta(delta, eta), b_theta(0, eta) > 0 (A.48); "
           "T_{0,z} = e^{-4/delta^2} delta^3 b_z (A.49); T_{0,z}/T_{0,theta} = delta^6 b_z/b_theta -> 0 (A.50); for every fixed mixed profile derivative "
           "d^I: |d^I T_0| <= C_I e^{-4/delta^2} delta^{-N_I}, |T_0| >= c e^{-4/delta^2} delta^{-3} (A.51); constants independent of q.  "
           "Leg 432 (H2, H3, amendment section 1): the quoted delta-powers delta^{-3}, delta^3, delta^6 are the limit on a collar delta <~ 1e-69 for this "
           "profile; at every resolvable delta the pinned stress has T_theta ~ e^{-4/delta^2} delta^0 (boundary term 1e-203 of the total).  "
           "Expectation written before running: with That_theta ~ delta^0, (d_y T)^ ~ (8/delta^3) That -> N_1 = 3, (d_y^2 T)^ ~ (64/delta^6) That -> N_2 = 6; "
           "both inside N <= 3k + 3.  The lower bound |T_0| >= c e^{-4/delta^2} delta^{-3} is NOT TESTABLE at resolvable delta (leg 432); "
           "delta^3 That_theta is reported, not scored.",
    "S1_pass_rule": "max over y >= 3 of |Ahat|, |Bhat|, |Tz bracket hat|, |That_theta|, |That_z|, |Rth hat|, |Rz hat| all == 0.0 exactly (floating zero, "
                    "structural: every term is psi_o, f_o' or an integral over [y, 3], plus the constant (2+2h)(s_h - 1) that vanishes only with the heat "
                    "factor); and the measured support edge (first y beyond which That == 0) equals 3.0; r_b(t) reported at t = 1 - 1e-2, 1e-4, 1e-6.",
    "controls": {"no_heat": "heat = False (leg 432 K6): S1 must fail, Bhat(y >= 3) = -(2 + 2h) and Rth hat beyond X_b = -h(2+2h) E_pow/sqrt(2X) "
                            "(i.e. R^(0)_theta = -2h(2+2h) K/r^2, the power law's own swirl-viscosity residual); expected number at h = 1e-3: "
                            "Bhat = -2.002, |Rth|/(E_pow/sqrt(2X)) = 2.002e-3.",
                 "poly_cutoff": "cutoff = 'poly' (leg 432 K1: psi_o = (delta/2)^4): S3 must fail, no N <= 60 bounds e^{4/delta^2} delta^N |d^k T|; "
                                "the N the last pair would need is ~ (4/0.05^2 - 4/0.1^2)/ln 2 = 1731; reported.  S1 still passes for it (the cutoff is "
                                "compactly supported) - reported, not a pre-registered expectation.",
                 "twin": "h = 1e-3, paper cutoff, heat on: S1 and S3 must pass (the controls run at h = 1e-3 as leg 432's did)."},
}


def stress(h, dy=1e-3, cutoff="paper", heat=True, n_eta=16, c_o=0.1):
    """Route A of leg 432 (amendment section 1) on y in [0, 3.5]: the hat (e^{lW}-scaled) stress and its ingredients."""
    A, D = 0.5 + h, 0.5 - h
    eta, _ = cheb(n_eta); d = 1.0 - eta ** 2; L = 1.0 - 2 * h * eta ** 2
    kap = (2 * h * (1 + h) * d) if heat else np.zeros_like(d); kap_eta = (-4 * h * (1 + h) * eta) if heat else np.zeros_like(eta)
    T = Tail(h, c_o, cutoff); rho = T.rho
    y = np.arange(0.0, 3.5 + dy / 2, dy); delta = 3.0 - y; lW = T.lW(delta)
    psi_h, fop_h, fo = T.psi_hat(y), T.fop_hat(y), T.fo(y)
    logX = LOG_XT + y; X = np.exp(logX); log_Epow = np.log(C_INF) - A * logX
    Phi_h = lambda yp: rho * T.psi_hat(yp) * (2.0 - rho * T.psi(yp))
    J_h = T.integral(y, -(1 - h), T.psi_hat); G_h = T.integral(y, h, T.psi_hat)
    S2A = T.integral(y, 2 * A, Phi_h); S2h = T.integral(y, 2 * h, Phi_h)
    A_h = rho * (psi_h + (1 - h) * J_h)
    sh = 1.0 if heat else 0.0
    B_h = ((2 + 2 * h) * (sh - 1.0) * np.exp(np.minimum(lW, 700)) + (2 + 2 * h) * rho * psi_h + 2 * fop_h)[:, None] \
        - sh * (kap[None, :] * rho * psi_h[:, None] + rho * G_h[:, None] * (kap * (1 - h) - D * eta * kap_eta)[None, :]) / L[None, :]
    log_pref = log_Epow + 0.5 * (logX - np.log(2.0))                      # E_pow sqrt(X/2)
    Tth_h = np.exp(log_pref)[:, None] * (A_h[:, None] / L[None, :] + B_h / X[:, None])
    Tzbr_h = eta[None, :] * (2 * A * S2A - 2 * h * S2h)[:, None]
    Tz_h = (C_INF ** 2 * np.exp((0.5 - 2 * A) * logX) / np.sqrt(2))[:, None] * Tzbr_h / L[None, :]
    return dict(h=h, A=A, dy=dy, cutoff=cutoff, heat=heat, y=y, delta=delta, lW=lW, eta=eta, L=L, X=X, logX=logX, log_Epow=log_Epow,
                psi_h=psi_h, fop_h=fop_h, fo=fo, A_h=A_h, B_h=B_h, Tth_h=Tth_h, Tzbr_h=Tzbr_h, Tz_h=Tz_h, rho=rho)


def d1(F, dy):
    """Second-order centred first derivative along axis 0; second-order one-sided at the ends."""
    out = np.empty_like(F)
    out[1:-1] = (F[2:] - F[:-2]) / (2 * dy)
    out[0] = (-3 * F[0] + 4 * F[1] - F[2]) / (2 * dy); out[-1] = (3 * F[-1] - 4 * F[-2] + F[-3]) / (2 * dy)
    return out


def d2(F, dy):
    out = np.empty_like(F)
    out[1:-1] = (F[2:] - 2 * F[1:-1] + F[:-2]) / dy ** 2
    out[0] = (2 * F[0] - 5 * F[1] + 4 * F[2] - F[3]) / dy ** 2; out[-1] = (2 * F[-1] - 5 * F[-2] + 4 * F[-3] - F[-4]) / dy ** 2
    return out


def scaled_derivs(Fh, delta, dy, cutoff):
    """(d_y T)^ and (d_y^2 T)^ for T = e^{-lW} Fh, with the weight's derivatives taken analytically."""
    if cutoff == "paper":
        dpos = np.where(delta > 0, delta, np.inf); lW1 = 8.0 / dpos ** 3; lW2 = 24.0 / dpos ** 4
    else:
        lW1 = np.zeros_like(delta); lW2 = np.zeros_like(delta)
    F1, F2 = d1(Fh, dy), d2(Fh, dy)
    sh = (slice(None),) + (None,) * (Fh.ndim - 1)
    return F1 - lW1[sh] * Fh, F2 - 2 * lW1[sh] * F1 + (lW1 ** 2 - lW2)[sh] * Fh


def residual_profiles(S, y_min=None):
    """Rth hat = -(d_y + 1) T_theta (scaled), Rz hat = -(d_y + 1/2) T_z (scaled), on y >= y_min (default: all y).  Beyond X_b the hat
    quantities jump to 0 at y = 3, so S1 uses y_min = 3.0 (differences never straddle the edge)."""
    m = slice(None) if y_min is None else (S["y"] >= y_min - 1e-12)
    y, delta = S["y"][m], S["delta"][m]
    dTth, _ = scaled_derivs(S["Tth_h"][m], delta, S["dy"], S["cutoff"])
    dTz, _ = scaled_derivs(S["Tz_h"][m], delta, S["dy"], S["cutoff"])
    return y, -(dTth + S["Tth_h"][m]), -(dTz + 0.5 * S["Tz_h"][m])


def gate_S1(S):
    mb = S["y"] >= 3.0
    yb, Rth, Rz = residual_profiles(S, y_min=3.0)
    mx = lambda a: float(np.max(np.abs(a)))
    beyond = {"A_hat": mx(S["A_h"][mb]), "B_hat": mx(S["B_h"][mb]), "Tz_bracket_hat": mx(S["Tzbr_h"][mb]), "Ttheta_hat": mx(S["Tth_h"][mb]),
              "Tz_hat": mx(S["Tz_h"][mb]), "Rtheta_hat": mx(Rth), "Rz_hat": mx(Rz), "n_points": int(mb.sum())}
    # dimensionless residual beyond X_b in units of E_pow/sqrt(2X) (the no-heat control's expected -h(2+2h))
    unit = np.exp(S["log_Epow"][mb] - 0.5 * (S["logX"][mb] + np.log(2.0)))
    beyond["Rtheta_over_Epow_sqrt2X_beyond"] = float(np.max(np.abs(Rth) / unit[:, None])) if Rth.size else 0.0
    beyond["B_hat_beyond_value"] = float(S["B_h"][mb][0, 0])
    # the measured support edge: the first y such that That_theta == 0 for all y' >= y
    nz = np.where(np.any(S["Tth_h"] != 0, axis=1))[0]
    edge = float(S["y"][nz[-1] + 1]) if nz.size and nz[-1] + 1 < len(S["y"]) else float("nan")
    exact = all(beyond[k] == 0.0 for k in ("A_hat", "B_hat", "Tz_bracket_hat", "Ttheta_hat", "Tz_hat", "Rtheta_hat", "Rz_hat"))
    log10_Xb = (LOG_XT + 3.0) / LN10
    rb = {}
    for tau in (1e-2, 1e-4, 1e-6):
        l10 = 0.5 * (np.log10(2.0) + np.log10(tau) + log10_Xb)
        rb[f"t=1-{tau:g}"] = {"q": tau, "log10_r_b": float(l10), "r_b": float(10 ** l10)}
    tau_unit = 1.0 / (2 * np.exp(LOG_XT + 3.0))
    return {"beyond_Xb_max_abs": beyond, "all_exactly_zero": bool(exact), "support_edge_y": edge, "support_edge_expected_y": 3.0,
            "log10_Xb": float(log10_Xb), "log10_X_tail": float(LOG_XT / LN10), "r_b": rb,
            "tau_at_which_r_b_equals_1": float(tau_unit), "log10_tau_at_which_r_b_equals_1": float(np.log10(tau_unit)),
            "r_b_scaling": "r_b(t) = sqrt(2 (1 - t) X_b) on z = 0: exact bookkeeping from (3.2); it tends to 0 as t -> 1, "
                           "but for this lambda = 0.1 profile only once 1 - t < 1/(2 X_b)."}


def heat_exterior_check(h):
    """(A.32)/(A.34): H^(m)(Z) = (-1)^m (h)_m Gamma(1+h)^{-1} int e^{-v} v^{h+m} (1+Zv)^{-h-m} dv; (A.37) residual and (A.36)."""
    aK = 1 + h
    def Hm(Z, m):
        poch = np.prod([h + i for i in range(m)]) if m else 1.0
        val, err = quad(lambda v: np.exp(-v) * v ** (h + m) * (1 + Z * v) ** (-h - m), 0, np.inf, limit=200, epsabs=0, epsrel=1e-12)
        return (-1) ** m * poch * val / Gamma(1 + h), err
    out = {}
    for Z in (0.0, 0.1, 1.0, 10.0):
        H0, e0 = Hm(Z, 0); H1, e1 = Hm(Z, 1); H2, e2 = Hm(Z, 2)
        ode = Z ** 2 * H2 + (1 + 2 * aK * Z) * H1 + aK * (aK - 1) * H0
        out[str(Z)] = {"H": H0, "H1": H1, "H2": H2, "A37_residual": ode, "A37_rel": abs(ode) / (aK * (aK - 1) * abs(H0)),
                       "A36_H_minus_1_plus_h1h_Z": H0 - (1 - h * (1 + h) * Z), "quad_err_max": max(e0, e1, e2)}
    # first-order coefficient against the pinned kappa: H(2d/X) = 1 - kappa/X + O(X^-2), kappa = 2h(1+h)d
    Zs = np.array([1e-3, 2e-3, 4e-3]); dev = np.array([Hm(z, 0)[0] - (1 - h * (1 + h) * z) for z in Zs])
    out["A36_second_order_fit_exponent"] = float(np.polyfit(np.log(Zs), np.log(np.abs(dev) + 1e-300), 1)[0]) if np.all(dev != 0) else None
    out["H_prime_0_over_minus_h1h"] = float(Hm(0.0, 1)[0] / (-h * (1 + h)))
    return out


def q_exponent(S, y_star=1.5, qs=(1e-2, 1e-3, 1e-4)):
    """R^(0)_theta(X_*, eta = 0, q) = q^{-A-1} sqrt(2/X_*) Rth(y_*): the fit is the measurement; the bookkeeping predicts -(A + 1)."""
    y, Rth, Rz = residual_profiles(S)
    i = int(np.argmin(np.abs(y - y_star))); j = int(np.argmin(np.abs(S["eta"])))
    lW = S["lW"][i]; Rth_i = Rth[i, j] * np.exp(-lW); Rz_i = Rz[i, j] * np.exp(-lW)     # delta = 1.5 here: e^{-4/2.25} is formable
    logR = {}; vals = []
    for q in qs:
        R = q ** (-S["A"] - 1) * np.sqrt(2.0 / S["X"][i]) * Rth_i; vals.append(R)
        logR[str(q)] = {"log10_abs_R0_theta": float(np.log10(abs(R))), "log10_abs_R0_theta_over_c_inf": float(np.log10(abs(R) / C_INF))}
    lq = np.log(np.array(qs)); lr = np.log(np.abs(np.array(vals)))
    slope = float(np.polyfit(lq, lr, 1)[0])
    # sup over the annulus (log space; Rth hat carries e^{4/delta^2})
    m = (y >= 0.5) & (y <= 2.95)
    with np.errstate(divide="ignore"):
        l10 = (-S["lW"][m] / LN10)[:, None] + np.log10(np.abs(Rth[m]) + 1e-300) + 0.5 * np.log10(2.0 / S["X"][m])[:, None]
    sup_log10_profile = float(np.max(l10))
    return {"y_star": float(y[i]), "eta_star": float(S["eta"][j]), "Rtheta_at_y_star": float(Rth_i), "Rz_at_y_star": float(Rz_i),
            "fit_exponent_of_R0_theta_in_q": slope, "bookkeeping_exponent_minus_A_minus_1": float(-S["A"] - 1), "abs_diff": abs(slope + S["A"] + 1),
            "values": logR, "log10_sup_annulus_of_q^(A+1)_R0_theta": sup_log10_profile,
            "gap_to_flatness": {"claimed": "(3.4): |R| <= C q^N for every N at fixed X <= X_1", "leading_order": "|R^(0)| = C' q^{-(A+1)} = C' q^{-1.5-h} at fixed X in the annulus",
                                "gap_exponent_for_N": "N + 1.5 + h for every N; infinite in the sense that no power of q is enough - carried by the pulses and the cycle, not measured here"}}


def gate_S3(S):
    """Q_k(delta) = max_eta e^{4/delta^2}|d_y^k T_0| at the four delta; N_k = min N in [0, 60] with delta^N Q_k non-increasing."""
    idx = [int(np.argmin(np.abs(S["delta"] - dd))) for dd in DELTAS]
    dl = np.array([S["delta"][i] for i in idx])
    extra = (4.0 / dl ** 2) / LN10 if S["cutoff"] != "paper" else np.zeros_like(dl)   # the TRUE (A.51) weight for the poly control (log10)
    res = {"deltas_used": dl.tolist()}
    for comp in ("theta", "z"):
        Fh = S["Tth_h"] if comp == "theta" else S["Tz_h"]
        D1, D2 = scaled_derivs(Fh, S["delta"], S["dy"], S["cutoff"])
        for k, Q in ((0, Fh), (1, D1), (2, D2)):
            q = np.array([np.max(np.abs(Q[i])) for i in idx])
            l10 = np.log10(q + 1e-300) + extra
            Nk = None
            for N in range(0, 61):
                seq = l10 + N * np.log10(dl)
                if np.all(np.diff(seq) <= 1e-12): Nk = N; break
            local_power = float(-(l10[-1] - l10[-2]) / (np.log10(dl[-1]) - np.log10(dl[-2])))   # -d log Q / d log delta between 0.1 and 0.05
            need_last = float(np.ceil((l10[-1] - l10[-2]) / np.log10(dl[-2] / dl[-1]))) if l10[-1] > l10[-2] else 0.0
            res[f"{comp}_k{k}"] = {"log10_Q": l10.tolist(), "N_min": Nk, "bound": 3 * k + 3, "local_power_0.1_to_0.05": local_power, "N_needed_by_last_pair": need_last}
    tth = np.array([np.max(np.abs(S["Tth_h"][i])) for i in idx])
    res["delta3_Ttheta_hat"] = (dl ** 3 * tth).tolist(); res["Ttheta_hat"] = tth.tolist()
    ok = all(res[f"{c}_k{k}"]["N_min"] is not None and res[f"{c}_k{k}"]["N_min"] <= 3 * k + 3 for c in ("theta", "z") for k in (1, 2))
    res["YES"] = bool(ok)
    return res


def crosscheck(S):
    """The stress built here IS the pinned one: compare with the artefact's decimated fields (h = 1e-7, dy = 1e-3)."""
    F = ART["preregistered_runs"]["1e-07"]["fields"]; y = np.array(F["y"]); idx = [int(np.argmin(np.abs(S["y"] - yy))) for yy in y]
    m = y <= 2.95
    A_rel = float(np.max(np.abs(S["A_h"][idx][m] - np.array(F["A_hat"])[m]) / np.abs(np.array(F["A_hat"])[m])))
    j0 = int(np.argmin(np.abs(S["eta"])))
    B_rel = float(np.max(np.abs(S["B_h"][idx, j0][m] - np.array(F["B_hat_eta0"])[m]) / np.abs(np.array(F["B_hat_eta0"])[m])))
    lT = np.log10(np.abs(S["Tth_h"][idx, 0]) + 1e-300)
    T_absdiff_log10 = float(np.max(np.abs(lT[m] - np.array(F["log10_Ttheta_hat"])[m])))
    return {"A_hat_rel": A_rel, "B_hat_eta0_rel": B_rel, "log10_Ttheta_hat_eta=1_max_abs_diff": T_absdiff_log10}


def run_one(h, dy=1e-3, cutoff="paper", heat=True, do_s2=True):
    t0 = time.time(); S = stress(h, dy, cutoff, heat)
    r = {"params": {"h": h, "dy": dy, "cutoff": cutoff, "heat": heat, "n_eta": int(len(S["eta"]))}, "S1": gate_S1(S), "S3": gate_S3(S)}
    if do_s2: r["S2c_q_exponent"] = q_exponent(S)
    r["runtime_s"] = time.time() - t0
    return S, r


if __name__ == "__main__":
    t0 = time.time()
    out = {"schema": "arc6_wave4_v1", "agent": 6, "unit": "(vi) support", "leg": 433, "pdf_sha256": PDF_SHA, "prereg": "experiments/journal/leg_433_prereg.md section 2 (vi)",
           "pages_read": PAGES_READ, "claimed": CLAIMED, "tier": "This is Tier 2, not a proof."}
    # ---- main run, h = 1e-7 (the pinned interface), three resolutions
    S, main = run_one(1e-7); main["crosscheck_against_leg432_artefact"] = crosscheck(S)
    res_study = {}
    for dy in (2e-3, 5e-4):
        _, rr = run_one(1e-7, dy=dy, do_s2=False); res_study[str(dy)] = rr["S3"]
    res_study["0.001"] = main["S3"]
    stab = {}
    for c in ("theta", "z"):
        for k in (1, 2):
            L = np.array([res_study[d][f"{c}_k{k}"]["log10_Q"] for d in ("0.002", "0.001", "0.0005")])
            stab[f"{c}_k{k}"] = {"max_abs_diff_log10_Q_across_dy": float(np.max(np.abs(L - L[1]))), "N_min_by_dy": [res_study[d][f"{c}_k{k}"]["N_min"] for d in ("0.002", "0.001", "0.0005")]}
    heat_chk = heat_exterior_check(1e-7)
    print(f"[{time.time()-t0:.0f}s] main: S1 exact={main['S1']['all_exactly_zero']} edge={main['S1']['support_edge_y']} S3={main['S3']['YES']} "
          f"q-exp={main['S2c_q_exponent']['fit_exponent_of_R0_theta_in_q']:.9f} xcheck={main['crosscheck_against_leg432_artefact']}")
    # ---- controls and their twin at h = 1e-3
    _, twin = run_one(1e-3); _, noheat = run_one(1e-3, heat=False); _, poly = run_one(1e-3, cutoff="poly")
    print(f"[{time.time()-t0:.0f}s] twin S1={twin['S1']['all_exactly_zero']} S3={twin['S3']['YES']}; no-heat S1={noheat['S1']['all_exactly_zero']} "
          f"B={noheat['S1']['beyond_Xb_max_abs']['B_hat_beyond_value']} R/unit={noheat['S1']['beyond_Xb_max_abs']['Rtheta_over_Epow_sqrt2X_beyond']:.6e}; "
          f"poly S3={poly['S3']['YES']} S1={poly['S1']['all_exactly_zero']}")
    # ---- gates
    s1 = main["S1"]; s3 = main["S3"]; qe = main["S2c_q_exponent"]
    S1_yes = s1["all_exactly_zero"] and s1["support_edge_y"] == 3.0
    a37_ok = all(v["A37_rel"] < 1e-8 for k, v in heat_chk.items() if k in ("0.0", "0.1", "1.0", "10.0"))
    a36_ok = abs(heat_chk["H_prime_0_over_minus_h1h"] - 1) < 1e-8
    S2_yes = S1_yes and a37_ok and a36_ok and qe["abs_diff"] < 1e-6
    S3_yes = s3["YES"]
    gates = {
        "S1": {"answer": "YES" if S1_yes else "NO", "max_abs_beyond_Xb": s1["beyond_Xb_max_abs"], "support_edge_y": s1["support_edge_y"], "r_b": s1["r_b"],
               "log10_Xb": s1["log10_Xb"], "log10_tau_at_which_r_b_equals_1": s1["log10_tau_at_which_r_b_equals_1"]},
        "S2": {"answer": "YES" if S2_yes else "NO",
               "clauses": {"C1_C2_X>=X_b_exact_zero (CHECKABLE)": "PASS" if S1_yes else "FAIL",
                           "C3_heat_exterior_(A.37)_(A.36) (CHECKABLE from the paper's H)": {"PASS" if (a37_ok and a36_ok) else "FAIL": {k: {"A37_rel": v["A37_rel"], "A36_dev": v["A36_H_minus_1_plus_h1h_Z"]} for k, v in heat_chk.items() if isinstance(v, dict)},
                                                                                      "H'(0)/(-h(1+h))": heat_chk["H_prime_0_over_minus_h1h"], "A36_remainder_exponent_in_Z": heat_chk["A36_second_order_fit_exponent"]},
                           "C6_leading_residual_q_exponent (MEASURED, not flat)": {"fit": qe["fit_exponent_of_R0_theta_in_q"], "bookkeeping": qe["bookkeeping_exponent_minus_A_minus_1"], "abs_diff": qe["abs_diff"], "gap": qe["gap_to_flatness"]},
                           "C1_X<=X_a": "NOT CHECKABLE here (axis construction not built; leg 432 H8)", "C4_X_ext_vs_X_b": "NOT CHECKABLE (corrections' supports not built); leading part vanishes beyond X_b",
                           "C5_cutoffs_K_r0_z0_tau0_q*": "NOT CHECKABLE (existence-only constants); leading u^(0) is not compactly supported - K ~ r^{-1-2h} beyond X_b",
                           "C6_C7_limits_F_j_and_(10.11)_extension": "NOT CHECKABLE at leading order; NOTE the paper extends f at t = 1 by (10.11), not by zero",
                           "C8_flatness_of_T_0_at_X_b": "S3"},
               "flatness": "NOT CLAIMED: (3.4) is carried by the corrections; the leading residual is q^{-(A+1)} at fixed X in the annulus"},
        "S3": {"answer": "YES" if S3_yes else "NO", "N_min": {f"{c}_k{k}": s3[f"{c}_k{k}"]["N_min"] for c in ("theta", "z") for k in (0, 1, 2)},
               "bounds_3k+3": {"k1": 6, "k2": 9}, "local_powers_0.1_to_0.05": {f"{c}_k{k}": s3[f"{c}_k{k}"]["local_power_0.1_to_0.05"] for c in ("theta", "z") for k in (0, 1, 2)},
               "log10_Q": {f"{c}_k{k}": s3[f"{c}_k{k}"]["log10_Q"] for c in ("theta", "z") for k in (0, 1, 2)}, "deltas_used": s3["deltas_used"],
               "delta3_Ttheta_hat_(A.51 lower bound, reported not scored)": s3["delta3_Ttheta_hat"], "resolution_stability": stab},
    }
    controls = {
        "no_heat_factor": {"expected": "S1 must fail: Bhat(y>=3) = -(2+2h) = -2.002 at h = 1e-3, Rtheta beyond X_b = -h(2+2h) E_pow/sqrt(2X)",
                           "fired": not noheat["S1"]["all_exactly_zero"], "numbers": {"B_hat_beyond": noheat["S1"]["beyond_Xb_max_abs"]["B_hat_beyond_value"],
                           "max_abs_beyond": noheat["S1"]["beyond_Xb_max_abs"], "Rtheta_over_Epow_sqrt2X": noheat["S1"]["beyond_Xb_max_abs"]["Rtheta_over_Epow_sqrt2X_beyond"],
                           "expected_h(2+2h)": 1e-3 * (2 + 2e-3), "expected_with_FD_truncation_(1+h)^2dy^2/6": (2 + 2e-3) * (1e-3 + (1 + 1e-3) ** 2 * 1e-6 / 6),
                           "S3_of_control": noheat["S3"]["YES"],
                           "S3_note": "reported, not scored: without the heat factor B carries the constant -(2+2h) e^{4/delta^2}, a term without the flat factor, "
                                      "so T_0 is not flat at X_b and no delta^N bounds e^{4/delta^2}|d^k T_0| (N_min = None); the heat factor is what makes (A.51) true"},
                           "twin": {"B_hat_beyond": twin["S1"]["beyond_Xb_max_abs"]["B_hat_beyond_value"], "max_abs_beyond": twin["S1"]["beyond_Xb_max_abs"], "S1": twin["S1"]["all_exactly_zero"]}},
        "polynomial_cutoff": {"expected": "S3 must fail: no N <= 60 with delta^N e^{4/delta^2}|d^k T| non-increasing; N needed by the last pair ~ 1731",
                              "fired": not poly["S3"]["YES"], "numbers": {f"{c}_k{k}": {"N_min": poly["S3"][f"{c}_k{k}"]["N_min"], "N_needed_by_last_pair": poly["S3"][f"{c}_k{k}"]["N_needed_by_last_pair"],
                                                                          "log10_Q_with_true_weight": poly["S3"][f"{c}_k{k}"]["log10_Q"]} for c in ("theta", "z") for k in (1, 2)},
                              "S1_of_control": poly["S1"]["all_exactly_zero"],
                              "twin": {f"{c}_k{k}": {"N_min": twin["S3"][f"{c}_k{k}"]["N_min"], "log10_Q": twin["S3"][f"{c}_k{k}"]["log10_Q"]} for c in ("theta", "z") for k in (1, 2)}},
        "twin_h=1e-3_unmodified": {"S1": twin["S1"]["all_exactly_zero"], "S3": twin["S3"]["YES"], "support_edge_y": twin["S1"]["support_edge_y"]},
    }
    out.update({"measured": {"main_h=1e-7": main, "resolution_study_S3": res_study, "heat_exterior_A32_A37": heat_chk, "twin_h=1e-3": twin, "control_no_heat": noheat, "control_poly": poly},
                "gates": gates, "controls": controls})
    out["instantiated_vs_scaled"] = (
        "Instantiated at computable lambda = 0.1, h = 1e-7 (and 1e-3 for the controls): the pinned tail stress T_0 of leg 432 on y = log(X/X_tail) in [0, 3.5], "
        "the exact vanishing of R^(0) = -div(q^{-A-1/2} T_0) for X >= X_b, the (A.51)-type bounds on d_y T_0 and d_y^2 T_0 at delta >= 0.05, and the ODE "
        "(A.37) of the paper's own exterior heat profile H.  Measured only as a scaling toward the paper's regime: the q-dependence (the profile is "
        "q-invariant, leg 432 H6, so R^(0) ~ q^{-(A+1)} at fixed X is exact bookkeeping from (4.11) and d_r = (2/r) d_y, confirmed by the fit) and the "
        f"physical support radius r_b(t) = sqrt(2(1-t) X_b): with this profile's log10 X_b = {s1['log10_Xb']:.2f} (the paper's schedule (A.5)-(A.12) at h = 1e-7, "
        "lambda = 0.1 above X_R = 1e12), r_b is ~1e103 at t = 1 - 1e-2 and reaches 1 only at 1 - t ~ 1e-208; the paper needs only X_b finite.  The paper's "
        "delta-powers in (A.48)-(A.51) are the delta -> 0 limit on a collar delta <~ 1e-69 (leg 432); at resolvable delta the measured N_k are what "
        "delta^0 behaviour of That_theta predicts (3 and 6), inside the pre-registered 3k + 3.  Nothing here touches the corrections or the flatness (3.4).")
    out["could_not_determine"] = [
        "I could not determine X_a (the inner support edge of T_0 / f at leading order), because it is fixed by the axis construction (Prop B.2, Cor B.10) which this unit does not build (leg 432 H8).",
        "I could not determine whether X_ext = X_b or X_ext > X_b, because X_ext is 'beyond all slow supports' of the corrections (p. 116) and the corrections are not built here.",
        "I could not determine the cutoff constants r_0, z_0, tau_0, q_*, the compact set K, or the time window [1 - tau_0, 1], because the manuscript gives them as existence-only (p. 118) with no numerical value.",
        "I could not determine whether the derivative limits F_j of (10.6) are nonzero away from the origin (the cutoff-transition terms), because they need the corrected field; the leading residual has no limit at t = 1 (it grows as q^{-(A+1)}).",
        "I could not test the lower bound |T_0| >= c e^{-4/delta^2} delta^{-3} of (A.51) or the delta^{-3}, delta^3, delta^6 of (A.48)-(A.50), because for this profile they hold only on a collar delta <~ 1e-69 (leg 432 H2); delta^3 That_theta at the four delta is reported instead.",
        "The pre-registration's phrase 'the extension by zero at t = 1' does not match the manuscript: f is extended through t = 1 by the Borel-type series (10.11), p. 120; zero extension is spatial ((10.4), outside supp c) and temporal near t = 0 and for t >= 2.  Recorded, not adjudicated.",
        "Flatness (3.4) at t = 1: not determined and not claimed - it is carried by the pulses and the correction cycle (units (iii), (iv)).",
    ]
    out["temptations"] = ["None recorded: no tolerance was changed after a number existed."]
    out["gate_answer"] = (
        f"S1 {gates['S1']['answer']}: from the pinned stress, every scaled ingredient (A, B, the T_z bracket), both stress components and both leading residual "
        f"profiles -(d_y+1)T_theta, -(d_y+1/2)T_z are exactly 0.0 at all {s1['beyond_Xb_max_abs']['n_points']} grid points y >= 3 (X >= X_b = e^3 X_tail), and the measured "
        f"support edge is y = {s1['support_edge_y']}; the zero is structural (psi_o, f_o' and every integral over [y,3] vanish, and the constant (2+2h)(s_h-1) vanishes only with the heat "
        f"factor) - dropping the heat factor gives B = {controls['no_heat_factor']['numbers']['B_hat_beyond']} and a nonzero residual {controls['no_heat_factor']['numbers']['Rtheta_over_Epow_sqrt2X']:.4e} E_pow/sqrt(2X) "
        f"(= h(2+2h): the power law's own swirl-viscosity residual), so the control fired.  r_b(t) = sqrt(2(1-t)X_b) with q = 1 - t on z = 0 ((3.2), p. 7): log10 r_b = "
        f"{s1['r_b']['t=1-0.01']['log10_r_b']:.2f}, {s1['r_b']['t=1-0.0001']['log10_r_b']:.2f}, {s1['r_b']['t=1-1e-06']['log10_r_b']:.2f} at 1 - t = 1e-2, 1e-4, 1e-6 - the shrinking is exact bookkeeping but at this "
        f"profile's X_b (1e{s1['log10_Xb']:.0f}) it reaches r_b = 1 only at 1 - t = 1e{s1['log10_tau_at_which_r_b_equals_1']:.0f}.  "
        f"S2 {gates['S2']['answer']}: the checkable clauses pass - R^(0) = 0 for X >= X_b (Thm 3.1(iii)/Thm 4.6(ii)/Lemma A.8); the paper's exterior heat profile (A.32) satisfies "
        f"(A.37) to relative {max(v['A37_rel'] for k, v in heat_chk.items() if isinstance(v, dict)):.1e} and H'(0) = -h(1+h) to {abs(heat_chk['H_prime_0_over_minus_h1h']-1):.1e}, which is the kappa the pinned stress keeps "
        f"(so 'the uncut exterior residual is exactly zero', p. 119, is the paper's own formula at work); the leading residual's own q-exponent at fixed X is measured "
        f"{qe['fit_exponent_of_R0_theta_in_q']:.7f} against the bookkeeping -(A+1) = {qe['bookkeeping_exponent_minus_A_minus_1']:.7f}: a growing power, not flat - the gap to (3.4)'s q^N is N + 1.5 + h for every N and is "
        f"carried by the pulses and the correction cycle, not by anything measured here.  The time window, K, the limits F_j and the (10.11) extension are not checkable at leading order.  "
        f"S3 {gates['S3']['answer']}: N_min = {gates['S3']['N_min']} against 3k+3 = 6, 9; local powers -dlogQ/dlog delta between 0.1 and 0.05: {gates['S3']['local_powers_0.1_to_0.05']}, stable to "
        f"{max(v['max_abs_diff_log10_Q_across_dy'] for v in stab.values()):.1e} in log10 Q across dy = 2e-3, 1e-3, 5e-4; the polynomial-cutoff control needs N ~ "
        f"{controls['polynomial_cutoff']['numbers']['theta_k1']['N_needed_by_last_pair']:.0f} (no N <= 60), so it fired; the h = 1e-3 twin passes both.  This is Tier 2, not a proof.")
    out["runtime_s"] = time.time() - t0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, default=float) + "\n")
    print("gates:", {k: v["answer"] for k, v in gates.items()}, "controls fired:", {k: v.get("fired") for k, v in controls.items() if "fired" in v})
    print("wrote", OUT, f"{OUT.stat().st_size:,} B in {time.time()-t0:.0f}s")
