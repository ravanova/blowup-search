"""Arc 6, R5(ii) (leg 432): the residual stress the outer profile leaves on its terminal tail.

    .venv/bin/python experiments/arc6_residual_v1.py --quick     # h = 1e-3, coarse
    .venv/bin/python experiments/arc6_residual_v1.py --full      # the pre-registered runs, controls, q-test

Pre-registered in experiments/journal/leg_432_prereg.md (96657de) and its amendment
leg_432_prereg_amend.md (fcac005), both committed before this file existed. Two routes to
T_0 = F(p_s - s) on y = log(X/X_tail) in [0, 3]:
  A  (4.11) with Lemma A.8's backward moment representation, heat factor to first order in Z = 2d/X;
  B  the paper's (A.54)/(A.46)/(A.53) at explicit physical scale q.
Every flat quantity is carried as e^{4/delta^2} x (.), delta = 3 - y; nothing underflows.
Tier 2. Not a proof.
"""
import argparse, json, sys, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))
from arc6_profile_v1 import cheb, PDF_SHA  # noqa: E402
OUT = ROOT / "writeup" / "data" / "arc6_residual_v1.json"
PROF = json.loads((ROOT / "writeup" / "data" / "arc6_profile_v1.json").read_text())["preregistered_runs"]["0.1"]
LOG_XT = float(np.log(PROF["params"]["X_R"]) + PROF["params"]["tail_start"])   # log X_tail, leg 430, lambda = 0.1
C_INF = float(PROF["G5"]["c_inf"])
NV, VMAX = 4001, 60.0


class Tail:
    """f_o = 1 - rho_o psi_o on the terminal tail; 'paper' = the (A.12) step, 'poly' = control K1."""
    def __init__(self, h, c_o=0.1, cutoff="paper", flip=False):
        self.h, self.rho, self.cutoff, self.flip = h, c_o * h, cutoff, flip
    def lW(self, delta):            # log of the flat weight e^{4/delta^2} pulled out of every flat quantity
        delta = np.asarray(delta, float)
        return 4.0 / np.where(delta > 0, delta, np.inf) ** 2 if self.cutoff == "paper" else np.zeros_like(delta)
    def _ab(self, y):
        u = np.clip((y - 1.0) / 2.0, 1e-300, 1 - 1e-300)
        return np.exp(-1.0 / u ** 2), u
    def psi_hat(self, y):           # e^{lW} psi_o
        y = np.asarray(y, float); d = 3.0 - y; out = np.zeros_like(y)
        m0 = y <= 1.0; out[m0] = np.exp(self.lW(d[m0]))
        m = (y > 1.0) & (y < 3.0)
        if self.cutoff == "paper":
            a, _ = self._ab(y[m]); out[m] = 1.0 / (a + np.exp(-4.0 / d[m] ** 2))
        else:
            out[m] = (d[m] / 2.0) ** 4
        return out
    def psi(self, y):               # unscaled psi_o (never underflows badly where it is used: f_o)
        y = np.asarray(y, float); d = 3.0 - y
        return np.where(y <= 1.0, 1.0, np.where(y < 3.0, self.psi_hat(y) * np.exp(-self.lW(d)), 0.0))
    def fo(self, y):
        s = -1.0 if self.flip else 1.0
        return 1.0 - s * self.rho * self.psi(y)
    def fop_hat(self, y):           # e^{lW} f_o'
        y = np.asarray(y, float); d = 3.0 - y; out = np.zeros_like(y)
        m = (y > 1.0) & (y < 3.0)
        if self.cutoff == "paper":
            a, u = self._ab(y[m]); b = np.exp(-4.0 / d[m] ** 2)
            out[m] = self.rho * a * (2.0 / u ** 3 + 16.0 / d[m] ** 3) / (2.0 * (a + b) ** 2)
        else:
            out[m] = 2.0 * self.rho * (d[m] / 2.0) ** 3
        return (-1.0 if self.flip else 1.0) * out

    def integral(self, y, beta, Fhat):
        """I(y) = int_y^3 e^{-beta (y'-y)} e^{lW(y) - lW(y')} Fhat(y') dy' for every y in the array.
        Paper cutoff: v = 4/delta'^2 - 4/delta^2 >= 0, delta' = 2/sqrt(v + 4/delta^2), ddelta' = -delta'^3/8 dv,
        Simpson on v in [0, VMAX]; the integrand is smooth in v. Poly cutoff: Simpson in y'."""
        y = np.asarray(y, float); out = np.zeros_like(y)
        v = np.linspace(0.0, VMAX, NV); wS = np.ones(NV); wS[1:-1:2] = 4; wS[2:-1:2] = 2; wS *= (v[1] - v[0]) / 3.0
        for i, yi in enumerate(y):
            d = 3.0 - yi
            if d <= 0: continue
            if self.cutoff == "paper":
                dp = 2.0 / np.sqrt(v + 4.0 / d ** 2); yp = 3.0 - dp
                out[i] = np.sum(wS * np.exp(-beta * (yp - yi) - v) * Fhat(yp) * dp ** 3 / 8.0)
            else:
                yp = np.linspace(yi, 3.0, NV); w2 = np.ones(NV); w2[1:-1:2] = 4; w2[2:-1:2] = 2; w2 *= (yp[1] - yp[0]) / 3.0
                out[i] = np.sum(w2 * np.exp(-beta * (yp - yi)) * Fhat(yp))
        return out


def build(h=1e-7, c_o=0.1, dy=1e-3, n_eta=16, cutoff="paper", flip=False, heat=True, eps_moment=0.0, D_wrong=False, q_list=(1.0, 10.0, 1e3), verbose=False):
    t0 = time.time()
    A, D = 0.5 + h, 0.5 - h
    eta, _ = cheb(n_eta); d = 1.0 - eta ** 2; L = 1.0 - 2 * h * eta ** 2
    kap = (2 * h * (1 + h) * d) if heat else np.zeros_like(d); kap_eta = (-4 * h * (1 + h) * eta) if heat else np.zeros_like(eta)
    T = Tail(h, c_o, cutoff, flip); rho = T.rho
    y = np.arange(0.0, 3.5 + dy / 2, dy); delta = 3.0 - y; lW = T.lW(delta)
    psi_h, fop_h, fo = T.psi_hat(y), T.fop_hat(y), T.fo(y)
    logX = LOG_XT + y; log_Epow = np.log(C_INF) - A * logX
    # ---- route A: the flat integrals of psi and Phi = 1 - f_o^2
    Phi_h = lambda yp: rho * T.psi_hat(yp) * (2.0 - rho * T.psi(yp))
    if flip:  # f_o = 1 + rho psi: Phi = 1 - f_o^2 = -rho psi (2 + rho psi)
        Phi_h = lambda yp: -rho * T.psi_hat(yp) * (2.0 + rho * T.psi(yp))
    J_h = T.integral(y, -(1 - h), T.psi_hat)              # int e^{(1-h)(y'-y)} psi
    G_h = T.integral(y, h, T.psi_hat)                     # int e^{-h(y'-y)} psi
    S2A = T.integral(y, 2 * A, Phi_h); S2h = T.integral(y, 2 * h, Phi_h)
    sgn = -1.0 if flip else 1.0
    calA_h = sgn * rho * (psi_h + (1 - h) * J_h) + eps_moment * np.exp(np.minimum(lW, 700)) * fo   # e^{lW} * A
    calA_beyond = eps_moment                                                                       # unscaled, y >= 3
    # B (eta-dependent): (2+2h)(s_h - 1) e^{lW} + (2+2h) rho psi_h + 2 fop_h - s_h [kap rho psi_h + rho G_h (kap(1-h) - D eta kap_eta)] / L
    sh = 1.0 if heat else 0.0
    calB_h = ((2 + 2 * h) * (sh - 1.0) * np.exp(np.minimum(lW, 700)) + (2 + 2 * h) * sgn * rho * psi_h + 2 * fop_h)[:, None] - sh * (kap[None, :] * sgn * rho * psi_h[:, None] + sgn * rho * G_h[:, None] * (kap * (1 - h) - D * eta * kap_eta)[None, :]) / L[None, :]
    calB_beyond = (2 + 2 * h) * (sh - 1.0)
    Tz_br_A = eta[None, :] * (2 * A * S2A - 2 * h * S2h)[:, None]          # e^{lW} x the T_z bracket; T_z = C^2 X^{1/2-2A} bracket / (sqrt2 L)
    # ---- route B at explicit q, hats throughout
    def routeB(q, Dz):
        Xy = np.exp(logX); r = np.sqrt(2 * q * Xy)
        third0 = T.integral(y, -(1 - h), T.fop_hat)                    # int e^{(1-h)(y'-y)} f'  (kappa-free part, x prefactor)
        Ih = T.integral(y, h, T.fop_hat)                                # int e^{-h(y'-y)} f'
        pref = np.exp(log_Epow + 0.5 * (logX - np.log(2.0)))            # E_pow sqrt(X/2)
        # boundary q^{A+1/2} K f_r = 2 E_pow f' / sqrt(2X) -> e^{lW}: 2 E_pow fop_h / sqrt(2X)  (heat factor 1 - kap/X dropped: O(1/X) of O(1/X))
        bnd = 2 * np.exp(log_Epow - 0.5 * (logX + np.log(2.0))) * fop_h
        # second: q^{A+1/2} r^{-2} int r'(K - r'K_r') f' dy' with r'K_r' = 2 X' dK/dX' = -2A K (1 + O(kap/X)):  (2+2h) E_pow Ih / sqrt(2X)
        # kept literally in q: q^{A+1/2} (2qX)^{-1} int sqrt(2qX') C (qX')^{-A} (1 + 2A) f' dy'
        qpow = q ** (A + 0.5) * (2 * q) ** (-1) * np.sqrt(2 * q) * q ** (-A)
        sec = qpow * (1 + 2 * A) * C_INF * np.exp((-0.5 - A) * logX) * Ih
        # third: q^{A+1/2} (q L r^2)^{-1} int (r'^3/2) K f' dy' = q^{A+1/2} (q L 2 q X)^{-1} int (2qX')^{3/2}/2 C (qX')^{-A} (1 - kap/X') f' dy'
        qpow3 = q ** (A + 0.5) / (q * 2 * q) * (2 * q) ** 1.5 / 2 * q ** (-A)
        thirdA = (qpow3 * C_INF * np.exp((0.5 - A) * logX) * third0)[:, None] / L[None, :]
        third_k = -qpow3 * C_INF * (np.exp((0.5 - A) * logX) * Ih * np.exp(-logX))[:, None] * (kap[None, :] / L[None, :]) if heat else np.zeros_like(thirdA)
        # T_z: q^{A+1/2} (2qX)^{-1/2} q (2 eta / (q^Dz L)) C^2 q^{-2A} int X''^{-2A} (X'' - X)(1 - 2kap/X'') f_o f' dy''
        I_z0 = T.integral(y, 2 * A - 1, lambda yp: T.fo(yp) * T.fop_hat(yp)) - T.integral(y, 2 * A, lambda yp: T.fo(yp) * T.fop_hat(yp))  # int e^{-2As}(e^s - 1) f f'
        qz = q ** (A + 0.5) * (2 * q) ** (-0.5) * q * 2 / q ** Dz * C_INF ** 2 * q ** (-2 * A)
        Tz_hat = qz * np.exp((0.5 - 2 * A) * logX)[:, None] * eta[None, :] / L[None, :] * I_z0[:, None]
        AhatB = thirdA * L[None, :] / pref[:, None]                    # should equal calA (eta-independent)
        BhatB = (bnd[:, None] + sec[:, None] + third_k) * np.exp(logX)[:, None] / pref[:, None]
        return {"A_hat": AhatB, "B_hat": BhatB, "Tz_hat": Tz_hat, "boundary_hat": bnd, "second_hat": sec, "third_A_hat": thirdA, "pref": pref}
    Dz = A if D_wrong else (1 - A)
    RB = {str(q): routeB(q, Dz) for q in q_list}
    B1 = RB[str(q_list[0])]
    # route A totals in the same normalisation: T_theta_hat = pref [A/L + B/X]
    pref = B1["pref"]
    # ---- gates data
    m = (y >= 0.5) & (y <= 2.95); mb = y >= 3.0
    A_A = np.tile(calA_h[:, None], (1, n_eta + 1)); A_B = B1["A_hat"]
    rel = lambda a, b: float(np.max(np.abs(a[m] - b[m]) / np.maximum(np.abs(b[m]), 1e-300)))
    Tz_A = (C_INF ** 2 * np.exp((0.5 - 2 * A) * logX) / np.sqrt(2))[:, None] * Tz_br_A / L[None, :]
    H0 = {"A_rel": rel(A_A, A_B), "B_rel": rel(calB_h, B1["B_hat"]), "Tz_rel": rel(Tz_A, B1["Tz_hat"])}
    H1 = {"min_A": float(np.min(calA_h[m])), "min_B": float(np.min(calB_h[m])), "min_boundary": float(np.min(B1["boundary_hat"][m])), "min_second": float(np.min(B1["second_hat"][m])), "min_third": float(np.min(B1["third_A_hat"][m]))}
    # H2 (i): boundary term x delta^3 against b_theta(0) = 16 rho E_pow(X_b) g(0) / sqrt(2 X_b), ratio = e^{(A+1/2) delta} fop_hat delta^3 / (8 rho e)
    ratio = np.exp((A + 0.5) * delta) * fop_h * delta ** 3 / (8 * abs(rho) * np.e)
    idx = {dd: int(np.argmin(np.abs(delta - dd))) for dd in (0.4, 0.2, 0.1, 0.05)}
    H2 = {"boundary_over_b0": {str(dd): float(ratio[i]) for dd, i in idx.items()}}
    i5 = idx[0.05]; kk = max(1, int(round(0.02 / dy))); sl = lambda f, i, k=kk: float((np.log(f[i - k]) - np.log(f[i + k])) / (np.log(delta[i - k]) - np.log(delta[i + k])))
    Ttheta_hat = pref * calA_h / L[0]                 # eta = -1 column; A is eta-independent
    H2["local_power_Ttheta_hat_at_0.05"] = sl(np.abs(Ttheta_hat), i5) if calA_h[i5] > 0 else float("nan")
    with np.errstate(divide="ignore"):
        frac = np.abs(calB_h[:, 0]) / (np.exp(logX) * np.abs(calA_h) + 1e-300)
    H2["log10_boundary_fraction_at_0.05"] = float(np.log10(frac[i5] + 1e-300)); H2["delta_cross"] = float(delta[i5] * frac[i5] ** (1 / 3))
    H2["not_testable"] = "T_hat delta^3 -> b_theta(0,eta) needs delta < delta_cross"
    rz = np.abs(Tz_A[:, :] / np.maximum(np.abs(pref[:, None] * calA_h[:, None] / L[None, :]), 1e-300))
    ratio_over_Epow = rz / np.exp(log_Epow)[:, None]
    H3 = {"local_power_Tz_over_Ttheta_at_0.05": sl(np.max(rz, axis=1), i5), "C_sup_ratio_over_Epow": float(np.max(ratio_over_Epow[m])), "log10_ratio_at_0.05": float(np.log10(np.max(rz[i5]) + 1e-300))}
    fop_over_fo = fop_h * np.exp(-np.minimum(lW, 700)) / fo         # f_o' unscaled = fop_hat e^{-lW}; underflow to 0 is the truth there
    a_m2 = 2 * h - 2 * fop_over_fo                                    # a - 2 formed directly (a = 2 + O(h) would lose the digits)
    H4 = {"h": h, "a_minus_2_min": float(np.min(a_m2[m])), "a_minus_2_max": float(np.max(a_m2[m])), "a_minus_2_min_over_h": float(np.min(a_m2[m]) / h), "a_minus_2_max_over_h": float(np.max(a_m2[m]) / h), "fop_over_fo_max_over_h": float(np.max(fop_over_fo) / h)}
    H5 = {"log10_sup_a_minus_2_times_ratio2": float(np.log10(np.max(np.abs(a_m2[m, None]) * rz[m] ** 2) + 1e-300)), "Pc_minus_vs_positive": bool(np.min(calA_h[m]) > 0)}
    a = 2 + a_m2
    q0 = RB[str(q_list[0])]
    H6 = {str(q): {"Ttheta_rel": rel(RB[str(q)]["A_hat"], q0["A_hat"]), "Tz_rel": rel(RB[str(q)]["Tz_hat"], q0["Tz_hat"])} for q in q_list[1:]}
    H7 = {"A_beyond_Xb": float(calA_beyond), "B_beyond_Xb": float(calB_beyond), "Tz_bracket_beyond_max": float(np.max(np.abs(Tz_br_A[mb]))) if mb.any() else 0.0,
          "A_hat_beyond_max": float(np.max(np.abs(calA_h[mb]))), "delta3_dlogT_ddelta_at_0.05": float(delta[i5] ** 3 * ((8 / delta[i5] ** 3 if cutoff == "paper" else 0.0) + (np.log(np.abs(Ttheta_hat[i5 - kk])) - np.log(np.abs(Ttheta_hat[i5 + kk]))) / (delta[i5 - kk] - delta[i5 + kk]))) if calA_h[i5] > 0 else float("nan")}
    H8 = {"could_not_determine": "X_a is fixed by the axis construction (Prop B.2, Cor B.10); on the tail A(y) > 0 at every y < 3, so the tail alone does not locate it", "A_hat_at_y0": float(calA_h[0])}
    res = {"params": {"h": h, "c_o": c_o, "rho_o": rho, "dy": dy, "n_eta": n_eta + 1, "cutoff": cutoff, "flip": flip, "heat": heat, "eps_moment": eps_moment, "D_wrong": D_wrong, "q_list": list(q_list),
                      "log_X_tail": LOG_XT, "log10_X_tail": LOG_XT / np.log(10), "c_inf": C_INF, "NV": NV, "VMAX": VMAX, "runtime_s": time.time() - t0},
           "H0": H0, "H1": H1, "H2": H2, "H3": H3, "H4": H4, "H5": H5, "H6": H6, "H7": H7, "H8": H8,
           "fields": {"y": y[::25].tolist(), "delta": delta[::25].tolist(), "log10_Ttheta_hat": np.log10(np.abs(Ttheta_hat[::25]) + 1e-300).tolist(), "A_hat": calA_h[::25].tolist(), "B_hat_eta0": calB_h[::25, n_eta // 2].tolist(),
                      "log10_Tz_over_Ttheta_max": np.log10(np.max(rz, axis=1)[::25] + 1e-300).tolist(), "boundary_over_b0": ratio[::25].tolist(), "a_minus_2_over_h": ((a[::25] - 2) / h).tolist()}}
    if verbose:
        print(f"  [{time.time()-t0:.0f}s] h={h} cutoff={cutoff} heat={heat}: H0 {H0}\n    H1 {H1}\n    H2 {H2}\n    H3 {H3}\n    H4 {H4}\n    H5 {H5}\n    H6 {H6}\n    H7 {H7}")
    return res


def gates(r):
    g = {}
    g["H0"] = ("YES" if max(r["H0"].values()) < 1e-6 else "NO", r["H0"])
    g["H1"] = ("YES" if (r["H1"]["min_A"] > 0 and r["H1"]["min_B"] > 0 and min(r["H1"]["min_boundary"], r["H1"]["min_second"], r["H1"]["min_third"]) >= 0) else "NO", r["H1"])
    bb = r["H2"]["boundary_over_b0"]; errs = [abs(bb[k] - 1) for k in ("0.4", "0.2", "0.1", "0.05")]
    g["H2"] = ("YES" if (errs[-1] < 0.5 and all(errs[i + 1] <= errs[i] for i in range(3)) and abs(r["H2"]["local_power_Ttheta_hat_at_0.05"]) < 0.5) else "NO",
               {"boundary_over_b0": bb, "local_power": r["H2"]["local_power_Ttheta_hat_at_0.05"], "log10_boundary_fraction": r["H2"]["log10_boundary_fraction_at_0.05"], "delta_cross": r["H2"]["delta_cross"]})
    g["H3"] = ("YES" if (2.5 <= r["H3"]["local_power_Tz_over_Ttheta_at_0.05"] <= 3.5 and r["H3"]["C_sup_ratio_over_Epow"] < 10) else "NO", r["H3"])
    h = r["params"]["h"]
    g["H4"] = ("YES" if (r["H4"]["a_minus_2_min"] > r["H4"]["h"] and r["H4"]["a_minus_2_max"] <= 2 * r["H4"]["h"] * (1 + 1e-12)) else "NO", r["H4"])   # literally 2 + h < a <= 2 + 2h
    g["H5"] = ("YES" if (r["H5"]["Pc_minus_vs_positive"] and r["H5"]["log10_sup_a_minus_2_times_ratio2"] < -3) else "NO", r["H5"])
    g["H6"] = ("YES" if all(v["Ttheta_rel"] < 1e-10 and v["Tz_rel"] < 1e-10 for v in r["H6"].values()) else "NO", r["H6"])
    g["H7"] = ("YES" if (r["H7"]["A_beyond_Xb"] == 0 and r["H7"]["B_beyond_Xb"] == 0 and r["H7"]["Tz_bracket_beyond_max"] == 0 and r["H7"]["A_hat_beyond_max"] == 0 and 7 <= r["H7"]["delta3_dlogT_ddelta_at_0.05"] <= 9) else "NO", r["H7"])
    return g


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--quick", action="store_true"); ap.add_argument("--full", action="store_true"); args = ap.parse_args()
    if args.quick:
        r = build(h=1e-3, dy=4e-3, n_eta=8, verbose=True); print(json.dumps({k: v[0] for k, v in gates(r).items()})); sys.exit(0)
    t0 = time.time()
    out = {"schema": "arc6_residual_v1", "leg": 432, "pdf_sha256": PDF_SHA, "prereg_commits": ["96657de", "fcac005"], "preregistered_runs": {}, "controls": {}}
    for h in (1e-7, 1e-3):
        r = build(h=h, verbose=True); r["gates"] = gates(r); out["preregistered_runs"][str(h)] = r
        print(f"[{time.time()-t0:.0f}s] h={h} gates:", {k: v[0] for k, v in r["gates"].items()})
    ctrl = {"K1_poly_cutoff": dict(cutoff="poly"), "K2_D_equals_A": dict(D_wrong=True), "K3_residual_moment": dict(eps_moment=1e-3), "K4_flip_cutoff": dict(flip=True), "K5_minus_h": dict(h=-1e-3), "K6_no_heat": dict(heat=False)}
    for k, kw in ctrl.items():
        r = build(**{"h": 1e-3, **kw}); out["controls"][k] = {"gates": {kk: vv[0] for kk, vv in gates(r).items()}, "H7": r["H7"], "H1": r["H1"], "H6": r["H6"], "H4": r["H4"], "H2": r["H2"]}
        print(f"[{time.time()-t0:.0f}s] {k}: {out['controls'][k]['gates']}")
    out["runtime_s"] = time.time() - t0
    OUT.write_text(json.dumps(out, indent=1, default=float) + "\n"); print("wrote", OUT, f"{OUT.stat().st_size:,} B in {time.time()-t0:.0f}s")
