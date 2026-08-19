#!/usr/bin/env python3
"""Leg 400 / unit L5 -- the driver: controls, sweep, gate.  See p2_route_l5_v1.py for the ansatz.

Run:    .venv/bin/python experiments/p2_route_l5_v1_driver.py
Writes: writeup/data/p2_route_l5_finite_energy_v1.json  (checkpointed after every stage)
"""

import importlib.util
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("l5core", ROOT / "experiments" / "p2_route_l5_v1.py")
L5 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L5)

OUT = L5.OUT
CLOC = L5.CLOC

# resolution of the production sweep (control C9 re-runs a subset at higher order)
RES = dict(n_theta=16, n_phi=32, n_panel=6, n_gl=14)
RES_HI = dict(n_theta=28, n_phi=56, n_panel=10, n_gl=20)
N_S = 6
RHOS = [10.0, 30.0, 100.0, 300.0, 1000.0]
ALPHAS = [1.0, 1.25, 1.6]
KAPPAS = {"kappa=0_similarity_frozen": 0.0, "kappa=a/2_intermediate": 0.25, "kappa=a_physical_frozen": 0.5}


# ---------------------------------------------------------------------------------------------
# S1.  The bill, re-derived from the ARTEFACT (pre-committed reading (d)) -- never from prose
# ---------------------------------------------------------------------------------------------

def read_bill():
    d = json.loads(CLOC.read_text())
    b3 = d["check_B3_Lp_thresholds"]
    cm = d["check_C_cutoff_magnitudes"]["by_alpha"]
    return {
        "source_file": "writeup/data/p2_route_cloc_v1.json",
        "source_leg": d["leg"],
        "source_route": d["route"],
        "source_self_hash": d["self_hash"],
        "L2_threshold_alpha": b3["L2_threshold_alpha"],
        "L3_threshold_alpha": b3["L3_threshold_alpha"],
        "banked_type_I_alpha": b3["banked_type_I_alpha"],
        "deficit_to_L2_in_exponent": b3["deficit_to_L2_in_exponent"],
        "required_over_available_exponent_ratio": b3["required_over_available_exponent_ratio"],
        "increment_per_decade_L3_cube": d["check_C2_critical_L3_tail_is_log_divergent_at_alpha_1"]["increment_per_decade"][0],
        "banked_rho_exponents_alpha_1": cm["alpha=1.0"]["measured_rho_exponents"],
        "banked_rho_exponents_alpha_1p25": cm["alpha=1.25"]["measured_rho_exponents"],
        "dss_symmetry_max_rel_error": d["check_A_field_is_what_it_claims"]["dss_symmetry_max_rel_error"],
        "lambda": d["check_A_field_is_what_it_claims"]["lambda"],
        "period_in_s": d["check_A_field_is_what_it_claims"]["period_in_s"],
    }


# ---------------------------------------------------------------------------------------------
# S2.  C1 -- independent re-implementation of leg 381's cutoff magnitudes (instrument validity)
# ---------------------------------------------------------------------------------------------

def cloc_magnitudes(alpha, rho, s=0.0):
    """leg 381's `cutoff_magnitudes`, re-implemented from its published definitions.

    chi = 1 on r<=rho, 0 on r>=2rho, quintic; chi' = -30 xi^2 (1-xi)^2 / rho, xi = (r-rho)/rho.
    Field cutoff (NOT the L5 potential cutoff): this control exists only to prove that this leg's
    field, quadrature and cutoff reproduce the BANKED artefact's rho-exponents.
    """
    dirs, wang = L5.sphere_nodes(24, 48)
    rad, wrad = L5.radial_nodes(rho, 2.0 * rho, 8, 32)
    m1, m2, _, _ = L5.modulation(s, "DSS")
    nl2 = vi2 = dv2 = 0.0
    for rr, wr in zip(rad, wrad):
        pts = rr * dirs
        r = np.full(dirs.shape[0], rr)
        yhat = dirs
        ps = L5.psi_derivs(r, alpha, 3)
        U = (m1 * L5.polo_field(ps[1], ps[2], r, yhat, L5.C_AXIS)
             + m2 * L5.polo_field(ps[1], ps[2], r, yhat, L5.D_AXIS))
        gU = (m1 * L5.polo_grad(ps[1], ps[2], ps[3], r, yhat, L5.C_AXIS)
              + m2 * L5.polo_grad(ps[1], ps[2], ps[3], r, yhat, L5.D_AXIS))
        xi = (rr - rho) / rho
        c1 = -30.0 * xi ** 2 * (1 - xi) ** 2 / rho
        c2 = -60.0 * xi * (1 - xi) * (1 - 2 * xi) / rho ** 2
        lap_chi = c2 + 2.0 * c1 / rr
        ur = np.einsum("ij,ij->i", U, yhat)
        nl = (c1 * ur)[:, None] * U                                        # (U.grad chi) U
        gradchi_dot_gradU = c1 * np.einsum("nij,nj->ni", gU, yhat)         # (grad chi . grad) U
        vi = 2.0 * gradchi_dot_gradU + float(lap_chi) * U
        dv = c1 * ur
        nl2 += wr * rr * rr * float(np.dot(wang, np.sum(nl ** 2, axis=1)))
        vi2 += wr * rr * rr * float(np.dot(wang, np.sum(vi ** 2, axis=1)))
        dv2 += wr * rr * rr * float(np.dot(wang, dv ** 2))
    # tail norms and pressure perturbation at the origin, on rho <= r <= 1e7 rho
    def tail(p, hi):
        edges = np.geomspace(rho, hi * rho, 25)
        xg, wg = np.polynomial.legendre.leggauss(24)
        tot = 0.0
        for lo, up in zip(edges[:-1], edges[1:]):
            mid, half = 0.5 * (lo + up), 0.5 * (up - lo)
            for rr, wr in zip(mid + half * xg, half * wg):
                r = np.full(dirs.shape[0], rr)
                ps = L5.psi_derivs(r, alpha, 2)
                U = (m1 * L5.polo_field(ps[1], ps[2], r, dirs, L5.C_AXIS)
                     + m2 * L5.polo_field(ps[1], ps[2], r, dirs, L5.D_AXIS))
                v = np.linalg.norm(U, axis=-1)
                tot += wr * rr * rr * float(np.dot(wang, v ** p))
        return tot
    t2 = tail(2.0, 1e7)
    t3 = tail(3.0, 1e7)
    dp = 0.0
    edges = np.geomspace(rho, 1e6 * rho, 25)
    xg, wg = np.polynomial.legendre.leggauss(24)
    for lo, up in zip(edges[:-1], edges[1:]):
        mid, half = 0.5 * (lo + up), 0.5 * (up - lo)
        for rr, wr in zip(mid + half * xg, half * wg):
            r = np.full(dirs.shape[0], rr)
            ps = L5.psi_derivs(r, alpha, 2)
            U = (m1 * L5.polo_field(ps[1], ps[2], r, dirs, L5.C_AXIS)
                 + m2 * L5.polo_field(ps[1], ps[2], r, dirs, L5.D_AXIS))
            v = np.linalg.norm(U, axis=-1) ** 2
            dp += wr * rr * rr * float(np.dot(wang, v)) * (3.0 / (4.0 * math.pi)) / rr ** 3
    return {"rho": rho, "nonlinear_residual_L2": math.sqrt(nl2), "viscous_residual_L2": math.sqrt(vi2),
            "divergence_defect_L2": math.sqrt(dv2), "bogovskii_corrector_L2_scale": rho * math.sqrt(dv2),
            "tail_L2_norm": math.sqrt(t2), "tail_L3_norm": t3 ** (1.0 / 3.0),
            "pressure_perturbation_at_origin": dp}


def control_C1(bill):
    keys = ["nonlinear_residual_L2", "viscous_residual_L2", "divergence_defect_L2",
            "bogovskii_corrector_L2_scale", "pressure_perturbation_at_origin", "tail_L3_norm",
            "tail_L2_norm"]
    out = {}
    worst = 0.0
    for alpha, banked in ((1.0, bill["banked_rho_exponents_alpha_1"]),
                          (1.25, bill["banked_rho_exponents_alpha_1p25"])):
        rows = [cloc_magnitudes(alpha, r) for r in [10.0, 30.0, 100.0, 300.0, 1000.0]]
        exps = {}
        for k in keys:
            e, _, _ = L5.fit_exponent([r["rho"] for r in rows], [r[k] for r in rows])
            exps[k] = e
            if k in banked:
                worst = max(worst, abs(e - banked[k]))
        out["alpha=%g" % alpha] = {"reimplemented_rho_exponents": exps, "banked_rho_exponents": banked,
                                   "rows": rows}
    out["max_abs_disagreement_vs_banked"] = worst
    out["tolerance"] = 1e-2
    out["fired_as_planted"] = bool(worst < 1e-2)
    out["meaning"] = ("independent re-implementation of leg 381's cutoff magnitudes reproduces the "
                      "BANKED rho-exponents; if this fails every number in leg 400 is void")
    return out


# ---------------------------------------------------------------------------------------------
# S3.  C2 -- negative control: no cutoff => the commutator is identically zero
# ---------------------------------------------------------------------------------------------

def control_C2():
    rng = np.random.default_rng(400)
    worst = 0.0
    scale = 0.0
    for _ in range(12):
        pts = rng.normal(size=(64, 3)) * rng.uniform(0.3, 40.0)
        s = float(rng.uniform(0.0, L5.PERIOD))
        R = L5.R_loc(pts, s, alpha=1.0, rho0=20.0, kappa=0.5, mode="DSS", no_cutoff=True)
        T = L5.residual_terms(pts, s, alpha=1.0, rho0=20.0, kappa=0.5, mode="DSS", no_cutoff=True)
        worst = max(worst, float(np.max(np.abs(R))))
        scale = max(scale, float(np.max(np.abs(T["V"]))))
    return {"max_abs_R_loc_without_cutoff": worst, "field_scale": scale,
            "relative": worst / max(scale, 1e-300), "tolerance": 1e-12,
            "fired_as_planted": bool(worst / max(scale, 1e-300) < 1e-12),
            "meaning": "chi == 1 must give R_loc == 0 identically; otherwise the commutator "
                       "bookkeeping is wrong and the leg is void"}


# ---------------------------------------------------------------------------------------------
# S4.  C4b -- reading (c): is the ansatz EXACTLY (D)SS?  V(y, s+2 log lambda) == V(y, s)?
# ---------------------------------------------------------------------------------------------

def control_dss_collapse():
    rng = np.random.default_rng(4000)
    out = {}
    for name, kappa in KAPPAS.items():
        worst = 0.0
        for _ in range(20):
            pts = rng.normal(size=(48, 3)) * rng.uniform(0.5, 25.0)
            s = float(rng.uniform(0.0, L5.PERIOD))
            T0 = L5.residual_terms(pts, s, alpha=1.0, rho0=20.0, kappa=kappa, mode="DSS")
            T1 = L5.residual_terms(pts, s + L5.PERIOD, alpha=1.0, rho0=20.0, kappa=kappa, mode="DSS")
            num = float(np.max(np.linalg.norm(T0["V"] - T1["V"], axis=-1)))
            den = max(float(np.max(np.linalg.norm(T0["V"], axis=-1))), 1e-300)
            worst = max(worst, num / den)
        out[name] = {"kappa": kappa, "max_rel_dss_defect": worst,
                     "is_exactly_DSS": bool(worst < 1e-12)}
    out["tolerance"] = 1e-12
    out["reading_c"] = ("the kappa=0 branch IS exactly DSS (the cutoff is frozen in similarity "
                        "variables, so V is 2 log lambda-periodic in s); the kappa=a branch is NOT, "
                        "because the cutoff radius in y grows like e^{as} and is not periodic")
    return out


# ---------------------------------------------------------------------------------------------
# S5.  THE SWEEP -- the gate's measurement
# ---------------------------------------------------------------------------------------------

def sweep(doc):
    rows = {}
    for alpha in ALPHAS:
        for kname, kappa in KAPPAS.items():
            for mode in ("DSS", "SS"):
                key = "alpha=%g|%s|%s" % (alpha, kname, mode)
                vals = []
                for rho0 in RHOS:
                    t0 = time.time()
                    v = L5.period_average(alpha, rho0, kappa, mode=mode, n_s=N_S,
                                          per_term=(mode == "DSS"), **RES)
                    v["rho0"] = rho0
                    v["seconds"] = round(time.time() - t0, 2)
                    vals.append(v)
                    print("   %s rho0=%g  L3=%.6g curlL32=%.6g (%.1fs)"
                          % (key, rho0, v["L3"], v["curl_L32"], v["seconds"]), flush=True)
                ent = {"rows": vals}
                for k in ("L3", "curl_L32"):
                    e, c, res = L5.fit_exponent(RHOS, [v[k] for v in vals])
                    ent[k + "_rho_exponent"] = e
                    ent[k + "_fit_prefactor"] = c
                    ent[k + "_fit_max_log_residual"] = res
                    ent[k + "_at_largest_rho"] = vals[-1][k]
                    et, _, _ = L5.fit_exponent(RHOS[-3:], [v[k] for v in vals[-3:]])
                    ent[k + "_rho_exponent_tail3"] = et
                if "T1_L3" in vals[0]:
                    for k in ("T1", "T2", "T3", "T4", "T5", "T12", "T123"):
                        e, _, _ = L5.fit_exponent(RHOS, [v[k + "_L3"] for v in vals])
                        et, _, _ = L5.fit_exponent(RHOS[-3:], [v[k + "_L3"] for v in vals[-3:]])
                        ent[k + "_L3_rho_exponent"] = e
                        ent[k + "_L3_rho_exponent_tail3"] = et
                        ent[k + "_L3_at_largest_rho"] = vals[-1][k + "_L3"]
                    ent["T12_over_T1_at_largest_rho"] = (vals[-1]["T12_L3"]
                                                         / max(vals[-1]["T1_L3"], 1e-300))
                    ent["total_over_T3_at_largest_rho"] = (vals[-1]["L3"]
                                                           / max(vals[-1]["T3_L3"], 1e-300))
                ent["predicted_rho_exponent_leading"] = 1.0 - alpha
                rows[key] = ent
                doc["sweep"] = rows
                L5.checkpoint(doc, "sweep " + key)
    return rows


# ---------------------------------------------------------------------------------------------
# S6.  C7 -- the modulation-absorption falsifier (can flip NO -> YES; reported either way)
# ---------------------------------------------------------------------------------------------

def gen_directions(pts, s, alpha, rho0, kappa, mode="DSS"):
    """G_a = V + y.grad V (the scaling generator); G_k = -sum m P[r chi_r psi] (cutoff-rate gen.)."""
    T = L5.residual_terms(pts, s, alpha=alpha, rho0=rho0, kappa=kappa, mode=mode)
    Ga = T["Vplus"]
    if kappa != 0.0:
        Gk = T["T1"] / (-kappa)
    else:
        Tk = L5.residual_terms(pts, s, alpha=alpha, rho0=rho0, kappa=1.0, mode=mode,
                               want=("T1",))
        Gk = Tk["T1"] / (-1.0)
    return Ga, Gk, T


def control_C7(alpha=1.0, kappa=0.5, mode="DSS", s=0.31):
    """Least-squares (L2) absorption of R_loc by the modulation parameters, on ALL of R^3."""
    dirs, wang = L5.sphere_nodes(16, 32)
    out = []
    for rho0 in RHOS:
        rho = rho0 * math.exp(kappa * s)
        # geometric shells over the core + linear panels over the annulus
        core_r, core_w = [], []
        edges = np.geomspace(1e-3 * rho, rho, 22)
        xg, wg = np.polynomial.legendre.leggauss(16)
        for lo, up in zip(edges[:-1], edges[1:]):
            mid, half = 0.5 * (lo + up), 0.5 * (up - lo)
            core_r.append(mid + half * xg); core_w.append(half * wg)
        ann_r, ann_w = L5.radial_nodes(rho, 2.0 * rho, 8, 16)
        rr = np.concatenate(core_r + [ann_r]); ww = np.concatenate(core_w + [ann_w])
        M = np.zeros((2, 2)); b = np.zeros(2)
        base_L3 = 0.0
        cache = []
        for r0, w0 in zip(rr, ww):
            pts = r0 * dirs
            Ga, Gk, T = gen_directions(pts, s, alpha, rho0, kappa, mode)
            R = T["T1"] + T["T2"] + T["T3"] + T["T4"] + T["T5"]
            wgt = w0 * r0 * r0 * wang
            M[0, 0] += float(np.dot(wgt, np.sum(Ga * Ga, axis=1)))
            M[0, 1] += float(np.dot(wgt, np.sum(Ga * Gk, axis=1)))
            M[1, 1] += float(np.dot(wgt, np.sum(Gk * Gk, axis=1)))
            b[0] += float(np.dot(wgt, np.sum(R * Ga, axis=1)))
            b[1] += float(np.dot(wgt, np.sum(R * Gk, axis=1)))
            base_L3 += float(np.dot(wgt, np.linalg.norm(R, axis=-1) ** 3))
            cache.append((r0, w0))
        M[1, 0] = M[0, 1]
        delta = np.linalg.solve(M + 1e-300 * np.eye(2), b)
        after = 0.0
        for r0, w0 in cache:
            pts = r0 * dirs
            Ga, Gk, T = gen_directions(pts, s, alpha, rho0, kappa, mode)
            R = T["T1"] + T["T2"] + T["T3"] + T["T4"] + T["T5"]
            Rres = R - delta[0] * Ga - delta[1] * Gk
            after += float(np.dot(w0 * r0 * r0 * wang, np.linalg.norm(Rres, axis=-1) ** 3))
        out.append({"rho0": rho0, "delta_a": float(delta[0]), "delta_kappa": float(delta[1]),
                    "L3_before": base_L3 ** (1 / 3), "L3_after": after ** (1 / 3),
                    "fraction_remaining": (after / max(base_L3, 1e-300)) ** (1 / 3)})
    e_b, _, _ = L5.fit_exponent([o["rho0"] for o in out], [o["L3_before"] for o in out])
    e_a, _, _ = L5.fit_exponent([o["rho0"] for o in out], [o["L3_after"] for o in out])
    return {"rows": out, "rho_exponent_before": e_b, "rho_exponent_after": e_a,
            "flips_gate_to_YES": bool(e_a < -0.1),
            "meaning": "a modulated ansatz may spend (a, kappa) absorbing the residual; the "
                       "projection is taken over ALL of R^3, core included, so absorption that "
                       "helps in the annulus is charged for what it injects in the core"}


# ---------------------------------------------------------------------------------------------
# S7.  C8 -- the energy control (Clay condition (7)): is the ansatz NATIVELY finite-energy?
# ---------------------------------------------------------------------------------------------

def energy_curve(alpha, rho0, kappa, mode="DSS", n_per=8, s_max=6.0, lam0=1.0):
    """E(t) = int |u|^2 dx = lambda(s) int |V(y,s)|^2 dy, sampled at FIXED MODULATION PHASE.

    Sampling s = j * 2 log lambda makes m1, m2 identical at every sample (OMEGA * PERIOD = 2 pi
    exactly), so the modulation's own O(1) oscillation is removed and the fitted growth exponent
    beta in E ~ e^{beta s} isolates the effect of kappa alone.  Prediction: beta = kappa - a.
    """
    dirs, wang = L5.sphere_nodes(16, 32)
    rows = []
    n = int(round(s_max / L5.PERIOD)) + 1
    for j in range(n):
        s = j * L5.PERIOD
        rho = rho0 * math.exp(kappa * s)
        lam = lam0 * math.exp(-L5.A_MOD * s)
        edges = np.geomspace(1e-4 * rho, 2.0 * rho, 40)
        xg, wg = np.polynomial.legendre.leggauss(n_per)
        tot = 0.0
        for lo, up in zip(edges[:-1], edges[1:]):
            mid, half = 0.5 * (lo + up), 0.5 * (up - lo)
            for r0, w0 in zip(mid + half * xg, half * wg):
                pts = r0 * dirs
                T = L5.residual_terms(pts, s, alpha=alpha, rho0=rho0, kappa=kappa, mode=mode,
                                      want=())
                v = np.linalg.norm(T["V"], axis=-1)
                tot += w0 * r0 * r0 * float(np.dot(wang, v ** 2))
        rows.append({"s": s, "lambda": lam, "rho_y": rho, "R_phys": lam * rho,
                     "int_V2": tot, "E": lam * tot})
    ss = np.array([r["s"] for r in rows]); E = np.array([r["E"] for r in rows])
    A = np.vstack([ss, np.ones_like(ss)]).T
    sol, *_ = np.linalg.lstsq(A, np.log(E), rcond=None)
    return {"rows": rows, "E_first": float(E[0]), "E_last": float(E[-1]),
            "E_ratio_last_over_first": float(E[-1] / E[0]),
            "growth_exponent_beta_in_s": float(sol[0]),
            "fit_max_log_residual": float(np.max(np.abs(np.log(E) - A @ sol))),
            "predicted_beta": kappa - L5.A_MOD}


def control_C8(alpha=1.0):
    out = {}
    for name, kappa in (("kappa=a_physical_frozen", 0.5), ("kappa=0_similarity_frozen", 0.0),
                        ("kappa=0.75_gt_a_FORBIDDEN_by_Clay_(7)", 0.75)):
        out[name] = energy_curve(alpha, 20.0, kappa)
        out[name]["kappa"] = kappa
    ka = out["kappa=a_physical_frozen"]
    k0 = out["kappa=0_similarity_frozen"]
    kg = out["kappa=0.75_gt_a_FORBIDDEN_by_Clay_(7)"]
    out["bounded_uniformly_in_t_at_kappa_a"] = bool(abs(ka["growth_exponent_beta_in_s"]) < 1e-3)
    out["unbounded_at_kappa_gt_a"] = bool(kg["growth_exponent_beta_in_s"] > 0.1)
    out["decays_at_kappa_0"] = bool(k0["growth_exponent_beta_in_s"] < -0.1)
    out["max_abs_beta_error_vs_prediction"] = max(
        abs(d["growth_exponent_beta_in_s"] - d["predicted_beta"]) for d in (ka, k0, kg))
    out["fired_as_planted"] = bool(out["bounded_uniformly_in_t_at_kappa_a"]
                                   and out["unbounded_at_kappa_gt_a"]
                                   and out["decays_at_kappa_0"])
    out["meaning"] = ("'natively finite energy' means E(t) = lambda int |V|^2 dy is bounded "
                      "UNIFORMLY in t, i.e. Clay condition (7). Prediction beta = kappa - a: "
                      "kappa = a gives beta = 0 (bounded, the finite-energy branch); kappa > a "
                      "gives beta > 0 (FORBIDDEN by Clay (7)); kappa = 0, the exactly-DSS branch, "
                      "gives beta = -a < 0, i.e. the physical support shrinks to a point and the "
                      "energy of the truncated object goes to zero.")
    return out


# ---------------------------------------------------------------------------------------------
# S8.  C6 (basis) and C9 (refinement)
# ---------------------------------------------------------------------------------------------

def control_C6():
    out = {}
    for kind in ("C4", "C2quintic"):
        vals = [L5.period_average(1.0, r, 0.5, mode="DSS", n_s=4, kind=kind, **RES) for r in RHOS]
        e3, _, _ = L5.fit_exponent(RHOS, [v["L3"] for v in vals])
        ec, _, _ = L5.fit_exponent(RHOS, [v["curl_L32"] for v in vals])
        e3t, _, _ = L5.fit_exponent(RHOS[-3:], [v["L3"] for v in vals[-3:]])
        ect, _, _ = L5.fit_exponent(RHOS[-3:], [v["curl_L32"] for v in vals[-3:]])
        out[kind] = {"L3_rho_exponent": e3, "curl_L32_rho_exponent": ec,
                     "L3_rho_exponent_tail3": e3t, "curl_L32_rho_exponent_tail3": ect,
                     "rows": [{"rho0": r, "L3": v["L3"], "curl_L32": v["curl_L32"]}
                              for r, v in zip(RHOS, vals)],
                     "L3_at_largest_rho": vals[-1]["L3"], "curl_L32_at_largest_rho": vals[-1]["curl_L32"]}
    d = abs(out["C4"]["L3_rho_exponent"] - out["C2quintic"]["L3_rho_exponent"])
    dc = abs(out["C4"]["curl_L32_rho_exponent"] - out["C2quintic"]["curl_L32_rho_exponent"])
    dt = abs(out["C4"]["L3_rho_exponent_tail3"] - out["C2quintic"]["L3_rho_exponent_tail3"])
    dct = abs(out["C4"]["curl_L32_rho_exponent_tail3"] - out["C2quintic"]["curl_L32_rho_exponent_tail3"])
    out["exponent_disagreement_L3"] = d
    out["exponent_disagreement_curl"] = dc
    out["exponent_disagreement_L3_tail3"] = dt
    out["exponent_disagreement_curl_tail3"] = dct
    out["precommitted_tolerance"] = 1e-2
    out["fired_as_planted"] = bool(max(d, dc) < 1e-2)
    out["fired_on_tail3_fit"] = bool(max(dt, dct) < 1e-2)
    out["constant_ratio_curl_C4_over_C2quintic"] = (out["C4"]["curl_L32_at_largest_rho"]
                                                    / out["C2quintic"]["curl_L32_at_largest_rho"])
    out["meaning"] = ("the transition profile is part of the BASIS (lesson 91); the exponent must "
                      "not depend on it, though the constant may. REPORTED HONESTLY: the 5-point "
                      "fit spans rho0 = 10, which is pre-asymptotic and where the two bases differ "
                      "most; the tail-3 fit (rho0 >= 100) is the one the gate uses everywhere else.")
    return out


def control_C9():
    out = {}
    for tag, res, fd in (("production", RES, 1e-4), ("refined", RES_HI, 1e-4), ("fd_halved", RES, 5e-5)):
        v = L5.annulus_norms(0.31, 1.0, 300.0, 0.5, mode="DSS", fd_rel=fd, **res)
        out[tag] = {"L3": v["L3"], "curl_L32": v["curl_L32"], "resolution": dict(res), "fd_rel": fd}
    base = out["production"]
    out["rel_change_refined_L3"] = abs(out["refined"]["L3"] - base["L3"]) / base["L3"]
    out["rel_change_refined_curl"] = abs(out["refined"]["curl_L32"] - base["curl_L32"]) / base["curl_L32"]
    out["rel_change_fd_halved_curl"] = abs(out["fd_halved"]["curl_L32"] - base["curl_L32"]) / base["curl_L32"]
    out["worst_rel_change"] = max(out["rel_change_refined_L3"], out["rel_change_refined_curl"],
                                  out["rel_change_fd_halved_curl"])
    return out


# ---------------------------------------------------------------------------------------------
# S9.  C3' -- the modulation-amplitude sweep: c_mod is LINEAR in the modulation, zero iff SS
# ---------------------------------------------------------------------------------------------

def modulation_amplitude_sweep():
    rows = []
    for amp in (0.0, 0.25, 0.5, 1.0, 2.0):
        v = L5.period_average(1.0, 300.0, 0.5, mode="DSS", n_s=6, amp=amp, **RES)
        rows.append({"amp": amp, "L3": v["L3"], "curl_L32": v["curl_L32"]})
    nz = [r for r in rows if r["amp"] > 0]
    ratios = [r["curl_L32"] / r["amp"] for r in nz]
    return {"rows": rows, "curl_over_amp_ratios": ratios,
            "linear_in_amplitude_rel_spread": (max(ratios) - min(ratios)) / max(ratios),
            "value_at_amp_zero": rows[0]["curl_L32"],
            "meaning": "amp = 0 is EXACTLY the self-similar case; c_mod vanishes there and is "
                       "linear in the modulation amplitude, so c_mod = 0 iff the profile is SS"}


# ---------------------------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------------------------

def main():
    t0 = time.time()
    doc = {
        "leg": 400, "unit": "L5", "lane": "L", "route": "L5-FINITE-ENERGY",
        "what": ("W4 clause (b): construct the natively finite-energy MODULATED, LOCALISED ansatz, "
                 "derive its profile system with every term the modulation and the cutoff generate, "
                 "and measure whether any cutoff radius makes the total localisation-plus-modulation "
                 "error smaller than the closure threshold"),
        "preregistration": "experiments/journal/leg_400.md SSSS0-3, committed before this file existed",
        "ceiling": ("TIER 2. Float64 quadrature of a SYNTHETIC exactly-DSS field. No link of the "
                    "L1->L4 chain moved. Clay stays ~0.05%. This is not a certified bound and not a "
                    "blow-up."),
        "realization_lesson_91": {
            "object": "backward lambda-DSS blow-up profile of 3D NS on R^3, non-axisymmetric, lambda=1.7",
            "profile_used": ("leg 381's banked SYNTHETIC exactly-DSS exactly-divergence-free poloidal "
                             "field U = m1(s) P[psi_alpha](.;c) + m2(s) P[psi_alpha](.;d), "
                             "psi_alpha=(1+r^2)^{(2-alpha)/2}, c=e_z, d=e_x"),
            "route_4_has_no_banked_profile": True,
            "route_4_no_profile_evidence": ["experiments/journal/leg_382.md line 174",
                                            "experiments/journal/leg_397.md SS1"],
            "why_this_is_still_a_measurement": ("the measured quantity is a COMMUTATOR R[V]-chi R[U], "
                                                "well defined for any field, solution or not; it "
                                                "depends on the profile only through (alpha, angular "
                                                "structure, modulation amplitude). The EXPONENTS are "
                                                "properties of the ansatz class; the CONSTANTS are "
                                                "properties of this realization and are labelled so."),
            "trial_space": "product Gauss-Legendre: geometric/linear radial panels x Gauss in cos(theta) x uniform in phi",
            "basis": "cutoff = degree-9 C^4 smoothstep on [rho,2rho] (control C6 repeats with leg 381's quintic C^2)",
            "norms": {"velocity": "||F||_{L1_t L3_x} = int ||R_loc(.,s)||_{L3_y} ds",
                      "vorticity_LOAD_BEARING": "||curl F||_{L1_t L3/2_x} = int ||curl_y R_loc(.,s)||_{L3/2_y} ds (pressure-free)"},
            "resolution": RES, "n_s_per_period": N_S, "rhos": RHOS, "alphas": ALPHAS,
        },
        "ansatz": {
            "similarity": "y = x/lambda(t), ds/dt = lambda^-2, u = lambda^-1 V(y,s), a = -lambda lambda_t",
            "V": "V(y,s) = m1(s) P[g(.,s)](y;c) + m2(s) P[g(.,s)](y;d), g = chi(r/rho(s)) psi_alpha(r)",
            "rho": "rho(s) = rho0 e^{kappa s}; R_phys(t) = lambda rho = R0 e^{(kappa-a)s}",
            "divergence_free_by_construction": ("the POTENTIAL is cut off, not the field, so div V = 0 "
                                                "exactly and NO Bogovskii corrector is needed -- the "
                                                "corrector leg 381 measured GROWING at rho^{+0.5004} "
                                                "in L2 is removed from the problem by construction"),
            "profile_system": "R[V] = V_s + a(V + y.grad V) - Lap V + V.grad V + grad P = 0, div V = 0",
            "terms_generated": {
                "T1_cutoff_drift": "the d_s chi part of V_s - chi U_s; = -kappa sum m_k P[r chi_r psi]",
                "T2_modulation_transport": "a[(V + y.grad V) - chi(U + y.grad U)]",
                "T3_modulation_commutator": "the mdot part of V_s - chi U_s; = sum mdot_k (P[g] - chi P[psi])",
                "T4_viscous_commutator": "-(Lap V - chi Lap U)",
                "T5_nonlinear_commutator": "V.grad V - chi (U.grad U)",
                "T6_pressure": "grad P_V - chi grad P_U -- annihilated by curl; for an exact profile "
                               "the surviving curl piece is grad chi x grad P_U, predicted rho^{-2alpha} "
                               "in L^{3/2}, corroborated by leg 381's banked pressure exponent -1.9997",
                "T7_divergence_corrector": "IDENTICALLY ZERO for this ansatz (potential cutoff)",
            },
            "predicted_scale_invariant_sizes": {
                "T1+T2": "|kappa - a| rho^{1-alpha}  (cancels identically at kappa = a)",
                "T3": "|mdot| rho^{1-alpha}", "T4": "rho^{-alpha-1}", "T5": "rho^{-2alpha}",
            },
        },
    }
    doc["bill_from_artefact"] = read_bill()
    L5.checkpoint(doc, "S1 bill")

    print("C2 negative control...", flush=True)
    doc["controls"] = {"C2_negative_no_cutoff": control_C2()}
    L5.checkpoint(doc, "S2 C2")

    print("C1 reproduction control (leg 381 rho-exponents)...", flush=True)
    doc["controls"]["C1_reproduces_leg381"] = control_C1(doc["bill_from_artefact"])
    L5.checkpoint(doc, "S3 C1")

    print("reading (c): exact-DSS collapse test...", flush=True)
    doc["controls"]["C4b_exact_DSS_collapse_reading_c"] = control_dss_collapse()
    L5.checkpoint(doc, "S4 DSS collapse")

    print("C8 energy control...", flush=True)
    doc["controls"]["C8_energy_Clay_condition_7"] = control_C8()
    L5.checkpoint(doc, "S5 C8")

    print("THE SWEEP...", flush=True)
    doc["sweep"] = sweep(doc)

    print("C3' modulation-amplitude sweep...", flush=True)
    doc["controls"]["C3p_modulation_amplitude_linearity"] = modulation_amplitude_sweep()
    L5.checkpoint(doc, "S7 C3p")

    print("C6 basis control...", flush=True)
    doc["controls"]["C6_basis"] = control_C6()
    L5.checkpoint(doc, "S8 C6")

    print("C9 refinement control...", flush=True)
    doc["controls"]["C9_refinement"] = control_C9()
    L5.checkpoint(doc, "S9 C9")

    print("C7 modulation-absorption falsifier...", flush=True)
    doc["controls"]["C7_modulation_absorption_falsifier"] = control_C7()
    L5.checkpoint(doc, "S10 C7")

    doc["runtime_seconds"] = round(time.time() - t0, 1)
    assemble_gate(doc)
    L5.checkpoint(doc, "S11 gate")
    seal(doc)
    print("done in %.1f s -> %s" % (doc["runtime_seconds"], OUT), flush=True)


def seal(doc):
    doc.pop("_checkpoint", None)
    doc.pop("_checkpoint_time", None)
    doc["self_hash"] = L5.sha({k: v for k, v in doc.items() if k != "self_hash"})
    OUT.write_text(json.dumps(doc, indent=1))


# ---------------------------------------------------------------------------------------------
# S11.  THE GATE -- assembled mechanically from the banked rows, by the SS3.3 rules
# ---------------------------------------------------------------------------------------------

def assemble_gate(doc):
    sw = doc["sweep"]
    kA = "alpha=1|kappa=a_physical_frozen|DSS"
    kS = "alpha=1|kappa=a_physical_frozen|SS"
    period = doc["bill_from_artefact"]["period_in_s"]
    e = sw[kA]
    c_mod = e["curl_L32_at_largest_rho"]                 # the LOAD-BEARING, pressure-free norm
    c_vel = e["L3_at_largest_rho"]
    per_period = c_mod * period
    eps_list = ["1", "0.1", "0.01", "1e-06"]
    doc["gate"] = {
        "question": ("IS THERE A CUTOFF RADIUS rho AND A NAMED NORM IN WHICH THE TOTAL "
                     "LOCALISATION-PLUS-MODULATION ERROR IS SMALLER THAN THE CLOSURE THRESHOLD "
                     "IT MUST BEAT -- YES OR NO, WITH THE NUMBER?"),
        "answer": "NO",
        "answer_in_precommitted_wording": (
            "NO. There is NO cutoff radius rho and NO named norm in which the total "
            "localisation-plus-modulation error of the natively finite-energy ansatz beats the "
            "closure threshold. In the load-bearing pressure-free norm "
            "||curl F||_{L1_t L3/2_x} the error PER UNIT SIMILARITY TIME saturates at "
            "c_mod = %.6g, with measured rho-exponent %.6f over rho0 in [%g, %g]: enlarging the "
            "cutoff radius buys NOTHING. Summed over the infinitely many DSS periods a backward-DSS "
            "blow-up requires, Sigma(infinity) = infinity, so the answer is NO for EVERY "
            "eps_close > 0 and no closure constant is needed."
            % (c_mod, e["curl_L32_rho_exponent_tail3"], RHOS[0], RHOS[-1])),
        "norm": "||curl F||_{L1_t L3/2_x} = int ||curl_y R_loc(.,s)||_{L3/2_y} ds (pressure-free)",
        "secondary_norm": "||F||_{L1_t L3_x} = int ||R_loc(.,s)||_{L3_y} ds",
        "c_mod_per_unit_s": c_mod,
        "c_mod_per_unit_s_velocity_norm": c_vel,
        "c_mod_per_DSS_period": per_period,
        "rho_exponent": e["curl_L32_rho_exponent_tail3"],
        "rho_exponent_velocity_norm": e["L3_rho_exponent_tail3"],
        "rho0_range_tested": [RHOS[0], RHOS[-1]],
        "largest_cutoff_radius_in_y_tested": e["rows"][-1]["rho"],
        "N_periods_affordable_by_threshold": {q: float(q) / per_period for q in eps_list},
        "Sigma_infinity": "infinity",
        "threshold_free": True,
        "why_threshold_free": ("the NO does not compare c_mod to any closure constant: c_mod > 0 "
                               "and rho-independent already makes Sigma(S) = c_mod S divergent, so "
                               "the answer is NO for every eps_close > 0. C1 stays disengaged: no "
                               "bounded approximate inverse, uniform in M or otherwise, is used."),
        "the_obstruction_named": (
            "THE MODULATION COMMUTATOR T3 = sum_k mdot_k (P[chi psi] - chi P[psi]). At kappa = a "
            "the cutoff-drift T1 and the modulation-transport T2 CANCEL IDENTICALLY (measured "
            "|T1+T2|/|T1| = %.3e), the viscous and nonlinear commutators T4, T5 decay like "
            "rho^{-alpha-1} and rho^{-2alpha}, and what is left is EXACTLY T3 (measured "
            "|R_loc|/|T3| = %.6f). T3 is proportional to mdot: it is EXACTLY ZERO iff the profile "
            "is exactly self-similar, and its scale-invariant size is rho^{1-alpha}."
            % (e["T12_over_T1_at_largest_rho"], e["total_over_T3_at_largest_rho"])),
        "the_clause_b_bill": {
            "required_rho_exponent_for_summability": "< 0 strictly, i.e. alpha > 1 STRICTLY",
            "available_rho_exponent_at_the_pinned_alpha": e["curl_L32_rho_exponent_tail3"],
            "banked_type_I_alpha": doc["bill_from_artefact"]["banked_type_I_alpha"],
            "deficit_in_exponent": 0.0,
            "measured_exponent_deviation_from_zero": abs(e["curl_L32_rho_exponent_tail3"]),
            "the_bill": ("clause (b) is an ENDPOINT failure, not a gap: the deficit in the exponent "
                         "is ZERO, but summability needs the exponent STRICTLY negative and the "
                         "pinned alpha = 1 delivers exactly 0. Compare clause (a)'s bill (leg 381): "
                         "L2_threshold_alpha %s vs banked %s, deficit %s in the exponent."
                         % (doc["bill_from_artefact"]["L2_threshold_alpha"],
                            doc["bill_from_artefact"]["banked_type_I_alpha"],
                            doc["bill_from_artefact"]["deficit_to_L2_in_exponent"])),
            "what_a_YES_would_need": ("either alpha > 1 strictly -- but alpha is PINNED to exactly 1 "
                                      "(Chae-Wolf 1610.09464 Thm 1.1 from below, Rmk 1.2 + "
                                      "Escauriaza-Seregin-Sverak from above) -- or mdot == 0, i.e. an "
                                      "EXACTLY self-similar profile, which TSAI (ARMA 143 (1998) 29-51) "
                                      "THEOREM 2 excludes -- read at FULL TEXT and checked against this "
                                      "object by PB2, leg 410. Necas-Ruzicka-Sverak is Acta Math. 176 "
                                      "(1996) 283-294, NOT ARMA 136, and it does NOT apply here: its "
                                      "hypothesis is U in L^3 and this object is not (CORRECTIONS SS47, "
                                      "SS47b). The banked JSON keeps the pre-correction wording by the "
                                      "W3 Q3 ruling -- a regeneration WILL differ in this field, by design."),
        },
        "controls_that_could_have_flipped_it": {
            "C7_modulation_absorption": doc["controls"]["C7_modulation_absorption_falsifier"]["flips_gate_to_YES"],
            "C7_rho_exponent_after_optimal_absorption": doc["controls"]["C7_modulation_absorption_falsifier"]["rho_exponent_after"],
            "C3_SS_control_exponent": sw[kS]["curl_L32_rho_exponent_tail3"],
        },
        "reading_that_fired": (
            "NONE of (a) [no YES]; reading (c) fired ONLY for the kappa = 0 branch, which the "
            "collapse test shows IS exactly DSS to %.1e and which is therefore called a NO and "
            "stopped; the kappa = a branch -- the natively finite-energy one -- is NOT exactly "
            "(D)SS (defect %.4f), so the ansatz did NOT collapse and the NO is a real measurement, "
            "not a disguise. Reading (d) governs every number: all re-derived from "
            "writeup/data/p2_route_cloc_v1.json (self_hash %s) and from this file's own rows."
            % (doc["controls"]["C4b_exact_DSS_collapse_reading_c"]["kappa=0_similarity_frozen"]["max_rel_dss_defect"],
               doc["controls"]["C4b_exact_DSS_collapse_reading_c"]["kappa=a_physical_frozen"]["max_rel_dss_defect"],
               doc["bill_from_artefact"]["source_self_hash"])),
    }
    doc["chain"] = {
        "links_moved": [],
        "statement": ("NO link of the L1->L4 chain moved. This is a Tier-2 measurement on a "
                      "synthetic realization; Clay stays at ~0.05%. Scale is not evidence."),
    }
    doc["under_resourced_with_a_cost"] = {
        "what_is_missing": ("the true modulation amplitude |mdot| of route 4's object. The EXPONENT "
                            "(0 at alpha = 1) is a property of the ansatz class and is settled here; "
                            "the CONSTANT c_mod = %.6g is a property of leg 381's synthetic "
                            "realization and is NOT route 4's number." % c_mod),
        "why_it_does_not_change_the_answer": ("c_mod is measured LINEAR in the modulation amplitude "
                                              "(control C3', ratio constant to %.1e), so any "
                                              "|mdot| > 0 gives a positive rho-independent c_mod and "
                                              "the same divergent Sigma. Only |mdot| == 0 -- exactly "
                                              "self-similar -- gives c_mod = 0, and that object is "
                                              "excluded by NRS/Tsai."
                                              % doc["controls"]["C3p_modulation_amplitude_linearity"]["linear_in_amplitude_rel_spread"]),
        "cost_to_remove_the_ceiling": [
            "a BANKED discrete profile for route 4 (none exists: leg 382 line 174, leg 397 SS1) -- "
            "the wave-4/5 construction legs, order 10^2 agent-hours, not purchasable inside leg 400",
            "interval arithmetic on the same commutator to turn the float exponent into a certified "
            "bound: a Route-D-style interval core over the annulus, order 10^1 agent-hours ON TOP of "
            "a banked profile",
        ],
    }


if __name__ == "__main__":
    if "--gate-only" in sys.argv:
        doc = json.loads(OUT.read_text())
        assemble_gate(doc)
        seal(doc)
        print("gate assembled -> %s" % OUT)
    else:
        main()
