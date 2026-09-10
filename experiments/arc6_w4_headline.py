"""Arc 6, wave 4, agent 5 (leg 433), unit R5(v): THE TWO HEADLINE QUANTITIES.

    .venv/bin/python experiments/arc6_w4_headline.py [--cache DIR] [--quick]

For the leading-order field u^(0)(x, t) built from the pinned lambda = 0.1 profile
(writeup/data/arc6_profile_v1.json, rebuilt here by experiments/arc6_profile_v1.build,
which is imported and not edited) through (4.3), (4.7)-(4.8) of the OpenAI manuscript
"Finite Time Blowup for Navier-Stokes" and the paper's q(z, t) of (3.2)/(4.1):

  * ||u^(0)(t)||_{L^2} and ||u^(0)(t)||_{L^inf} on t in [1 - 1e-1, 1 - 1e-6], at three radial
    resolutions dy in {4e-3, 2e-3, 1e-3}, with fitted exponents against the exact bookkeeping
    exponents derived (in CLAIMED below, before any number existed) from the change of variables;
  * the force the leading order alone would need, f^(0) := NS(u^(0)), from the operators of
    Lemma 4.1 (p. 25), its sup-norm exponent in q (gate V2), and two internal checks of the
    operator algebra against the paper's (4.14) and the S_n identity of Proposition 4.2, plus an
    independent physical-space finite-difference route at a few points;
  * gate V3: T* = 1 is prescribed; only the refinement stability of the norm fits and the
    quadrature/conservation drifts are reported;
  * two controls (A -> 3/4 + 0.1; U -> 0 in (4.7)) and the unmodified twin.

Everything is carried in logarithms where the profile spans ~450 e-folds of X.
Pre-registration: experiments/journal/leg_433_prereg.md section 2 (v), fixed before this
file existed. Tier 2. Not a proof; verifies nothing about the theorem.
"""
import argparse
import inspect
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))
import arc6_profile_v1 as P  # noqa: E402  (imported, never edited)

OUT = ROOT / "writeup" / "data" / "arc6" / "wave4" / "agent_5_headline.json"
PROFILE = ROOT / "writeup" / "data" / "arc6_profile_v1.json"

LAM, H, N_ETA = 0.1, 1e-7, 16
A, D = 0.5 + H, 0.5 - H
DYS = (4e-3, 2e-3, 1e-3)
TAUS = np.logspace(-1, -6, 26)          # t = 1 - tau on [1 - 1e-1, 1 - 1e-6]
ETA_CORE = 0.5                          # the paper's core C_tau = {X <= X_c, |eta| <= eta_c} (p. 8); X_c = inf here
Q_STARS = (0.1, 1.0)                    # the paper's domain Omega* = {q < q*} (Theorem 3.1, p. 15), q* not determined by the paper

# ----------------------------------------------------------------------------------------------
# CLAIMED — written before the run (committed as such), quoting the paper.
# ----------------------------------------------------------------------------------------------
CLAIMED = {
    "q_of_t": {
        "statement": "tau = 1 - t; the concentration scale q = q(z, t) is defined by tau = q(1 - eta^2), z = q^D eta, "
                     "X = r^2/(2q), i.e. q - z^2 q^{2h} = tau with d_q(q - z^2 q^{2h}) = 1 - 2h eta^2 > 0, so q is unique and "
                     "q ~ tau + |z|^{1/D}. On the axis z = 0 (eta = 0): q(0, t) = tau = 1 - t. Lemma 4.1: q_t = -1/L, "
                     "eta_t = D eta/(qL), X_t = X/(qL), q_z = 2 eta q^{1-D}/L, eta_z = d/(q^D L), X_z = -2 eta X/(q^D L).",
        "pages": {"(3.2) and q - z^2 q^{2h} = tau": 7, "(4.1)": 24, "Lemma 4.1": 25},
        "T_star": "T* = 1 is PRESCRIBED by tau = 1 - t (no dynamics fixes it).",
    },
    "field": {
        "statement": "(4.3) p. 25: u_theta = q^{-A} E(X, eta), u_z = q^{-A} U(X, eta), r u_r = V_0(X, eta), p = q^{-2A} Pi(X, eta); "
                     "(4.7) p. 26: V_0 = (X/L)(2 eta U - 2 D eta A_X(U) - d d_eta A_X(U)) = (X/L)(2 eta U + W - 1), Pi_X = E^2/(2X); "
                     "(4.8) p. 26: H = sqrt(2X) E, F = E/sqrt(2X), l = D_X log H, W = 1 - 2 D eta A_X(U) - d d_eta A_X(U), H_c = D eta + d U; "
                     "(4.25) p. 33: Pi = -int_X^inf E^2/(2x) dx. A = 1/2 + h, D = 1/2 - h, h = 1e-7 (pinned), lambda = 0.1 (pinned).",
        "inner_branch": "For X < X_R the pinned artefact carries only Lemma 4.8(i)'s temporary inner branch U = 4 eta, "
                        "E = P_* f x^{1/10} (p. 35), which 'need not be regular at the physical axis'; the paper's field for "
                        "X <= X_h = X_R e^{-5} (p. 36, p. 40) is the Appendix B axis profile, NOT instantiated (leg 430 section 4). "
                        "The field is built here on X >= X_h with the reference branch on [X_h, X_R] (where the paper's field equals it, "
                        "Prop 4.10(iii)); the reference branch continued to X = 0 is used only for the L^2 integrals (its share reported).",
    },
    "L_inf": {
        "derivation": "At fixed t, q = tau/d(eta). u_theta = tau^{-A} d^A E, u_z = tau^{-A} d^A U, u_r = V_0/r = tau^{-1/2} d^{1/2} sqrt(X/2) v_0 "
                      "with v_0 = V_0/X. Hence ||u_theta||_inf = tau^{-A} sup_{X,eta} d^A E: EXACT exponent -A = -(1/2 + h) = -0.5000001; "
                      "||u_r||_inf: EXACT exponent -1/2 (the paper: ||u_r||_{L^inf(C_tau)} = O(tau^{-1/2}), ratio O(tau^h), p. 8); "
                      "||u_z||_inf: -A. The full |u| mixes -1/2 and -A: measured exponent in [-A, -1/2]. With h = 1e-7 the gate's 1e-4 "
                      "cannot separate -A from -1/2: said in advance, not a widening.",
        "paper": "(3.6) p. 16: u_theta(sqrt(2 X_in tau), 0, 0, 1 - tau) = tau^{-A}(e_0 + O(tau^{2h})); p. 8: ||u_theta||_{L^inf(C_tau)} ~ tau^{-1/2-h}.",
        "exponent_L_inf_u_theta": -A, "exponent_L_inf_u_r": -0.5, "exponent_L_inf_u_z": -A,
    },
    "L_2": {
        "derivation": "dx dy dz = 2 pi r dr dz = 2 pi ds dz with s = qX, ds = q dX (X-integration at fixed eta), and at fixed t "
                      "z = tau^D eta d^{-D}, dz = q^D (L/d) d_eta = tau^D L d^{-1-D} d_eta (Lemma 4.1: eta_z = d/(q^D L)). "
                      "So dV = 2 pi q^{1+D} (L/d) dX d_eta = 2 pi tau^{1+D} L d^{-2-D} dX d_eta — the prereg's 'q dX q^D d_eta' times L/d. "
                      "Tangential part: ||(u_theta, u_z)||_2^2 = 2 pi tau^{1+D-2A} int int (E^2 + U^2) L d^{2A-2-D} dX d_eta, "
                      "1 + D - 2A = 1/2 - 3h, 2A - 2 - D = -3/2 + 3h (the paper's own E_core ~ tau^{1/2-3h}, p. 16). "
                      "Radial part: ||u_r||_2^2 = 2 pi tau^{D} int int (X v_0^2/2) L d^{-1-D} dX d_eta, D = 1/2 - h.",
        "exact_exponents_of_the_NORM_on_a_fixed_eta_core": {"tangential": 0.25 - 1.5 * H, "radial": 0.25 - 0.5 * H,
                                                             "combined": "between 0.25 - 1.5h and 0.25 - 0.5h, i.e. 0.25 to within 1.5e-7"},
        "R3_prediction": "The eta-weights d^{-3/2+3h} (tangential) and d^{-3/2+h} (radial) are NOT integrable at eta = +-1 (the far axial "
                         "field, q ~ |z|^{1/D} -> inf, where the leading field is ~ |z|^{-1-4h} on a tube of radius ~ |z|: energy per unit z "
                         "~ |z|^{-4h}). Prediction: ||u^(0)(t)||_{L^2(R^3)} = +inf for every t < 1; on |eta| <= eta_c the truncated norm^2 "
                         "diverges like d_c^{-1/2+3h}, d_c = 1 - eta_c^2. The paper never claims L^2(R^3) for the leading field: Theorem 3.1 "
                         "lives on Omega* = {q < q*} (p. 15) and the whole-space u is cut off by chi_x with compact support K (p. 16); "
                         "its energy statement is for the core C_tau (p. 16).",
        "q_star_prediction": "On the paper's domain {q < q*} (d >= tau/q*): ||u||_2^2 = C_0(q*) + C_1 tau^{1/2-3h} + ..., the leading term "
                             "CONSTANT (the near-eta = +-1 piece (tau/q*)^{-1/2+3h} times tau^{1/2-3h}): bounded, non-vanishing, exponent -> 0.",
        "gate_reading": "V1's L^2 sub-gate is applied to the core norm (|eta| <= 0.5, the only place the bookkeeping exponent exists), "
                        "against 0.25 - 1.5h (tangential-or-radial dominated: 0.25 within 1.5e-7 either way). The R^3 and {q < q*} "
                        "behaviours are reported as findings, decided before the run.",
    },
    "force": {
        "derivation": "f^(0) = NS(u^(0)) = d_t u + (u . grad) u - Lap u + grad p in cylindrical components, with Lemma 4.1's operators: "
                      "d_t(q^b g) = q^{b-1} T_b g, T_b g = (-b g + D eta g_eta + D_X g)/L; d_z(q^b g) = q^{b-D} Z_b g, "
                      "Z_b g = (2 b eta g + d g_eta - 2 eta D_X g)/L; d_r(q^b g) = q^{b-1/2} R g, R g = sqrt(2/X) D_X g; 1/r = q^{-1/2}/sqrt(2X). "
                      "With G := sqrt(X/2) v_0 (u_r = q^{-1/2} G): "
                      "R_r = q^{-3/2}[T_{-1/2}G + G RG + U Z_{-1/2}G - R(RG) - RG/sqrt(2X) + G/(2X)] - q^{-3/2+2h} Z_{-1/2-D}Z_{-1/2}G "
                      "(the centrifugal balance d_r p = u_theta^2/r is exact by (4.7), its q^{-2A-1/2} terms cancel identically); "
                      "R_theta = q^{-A-1}[T_{-A}E + G RE + U Z_{-A}E + GE/sqrt(2X) - R(RE) - RE/sqrt(2X) + E/(2X)] - q^{-A-2D} Z_{-A-D}Z_{-A}E; "
                      "R_z = q^{-A-1}[T_{-A}U + G RU + U Z_{-A}U - R(RU) - RU/sqrt(2X) + Z_{-2A}Pi] - q^{-A-2D} Z_{-A-D}Z_{-A}U. "
                      "Powers: -A - 1 = -3/2 - h (tangential, the paper's q^{-A-1/2} T_0 divided once more by r), -3/2 (radial), "
                      "-3/2 + h and -3/2 + 2h (axial viscosity, the paper's relative q^{2h}).",
        "predicted_exponent_L_inf_f": "-3/2 - h = -1.5000001 if a tangential term dominates, -3/2 if the radial does; the gate's +-0.01 "
                                      "cannot separate them: -1.5 either way.",
        "paper": "Theorem 3.1(iii) p. 15: |d^alpha_x d^b_t R(u, p)| <= C q^N for every N (flat), R = 0 for X >= X_ext; the corrected f is "
                 "bounded and flat at t = 1. Proposition 4.2 p. 27: the LEADING tangential residual is -div(q^{-A-1/2} T_0), a power, not flat.",
        "gap": "the corrections must remove 3/2 + h powers of q for boundedness and every power for flatness.",
        "where": "Expected sup on the inner reference region X ~ X_R (E ~ P_* ~ 7e5, sqrt(X) v_0 ~ 3e6) and, for R_z, the unbalanced axial "
                 "pressure gradient Z_{-2A}Pi ~ P_*^2 ~ 4e11 — exactly the term the paper's Appendix B axis profile is built to balance "
                 "(Z_* on p. 37); the pinned outer profile has no axis profile, so the magnitude is not the paper's; the exponent is.",
        "checks": "K1: sqrt(2X)[inviscid R_theta bracket] = {W D_X H + H_c H_eta + h(1 - 2 eta U) H}/L, (4.14) p. 27; "
                  "K2: inviscid R_z bracket = -S_n/L, (4.9) p. 26; K0: incompressibility (V_0)_X = (2 A eta U - d U_eta + 2 eta X U_X)/L, p. 26; "
                  "K3: physical-space central differences on u(r, z, t) at sample points vs the similarity-variable formula.",
    },
    "controls": {
        "C_A": "A -> 3/4 + 0.1 = 0.85 in the velocity powers only (coordinates D, L, d unchanged): core L^2 exponent (1 + D - 2A)/2 = "
               "(1.5 - h - 1.7)/2 = -0.1 - h/2 < 0 (diverges, sign flips), L^inf(u_theta) exponent -0.85. MUST fire.",
        "C_U": "U -> 0 in (4.7): A_X(U) = 0, W = 1, V_0 = 0 identically, u_r = 0; the L^inf location moves from the u_r-dominated point "
               "(X ~ X_R, where sqrt(X_R/2)|v_0| ~ 2.8e6 > P_* ~ 6.7e5) to the u_theta peak; exponent becomes exactly -A. Reported.",
        "twin": "the unmodified run must pass V1.",
    },
    "resolution": "dy in {4e-3, 2e-3, 1e-3}, n_eta = 16 (17 Chebyshev points, as pinned); the sup over X is refined parabolically about the "
                  "discrete argmax (stated now); eta-integrals use the Chebyshev interpolant (the profiles are smooth in eta).",
}


# ----------------------------------------------------------------------------------------------
# build the pinned profile and capture its internal arrays (the builder returns only a summary)
# ----------------------------------------------------------------------------------------------
def build_with_locals(**kw):
    src = inspect.getsource(P.build)
    assert src.count("\n    return res\n") == 1
    src = src.replace("\n    return res\n", "\n    return res, dict(locals())\n")
    ns = dict(vars(P))
    exec(src, ns)
    return ns["build"](**kw)


def profile_fields(dy, cache=None, drop_U=False):
    """The leading profiles on the coarse grid y (step dy), extended to y in [-5, 0) by the closed-form
    reference branch (Lemma 4.8(i)). Returns a dict of arrays (ny, 17) and the grid."""
    tag = f"dy{dy:g}"
    if cache is not None and (Path(cache) / f"{tag}.npz").exists():
        z = np.load(Path(cache) / f"{tag}.npz")
        F = {k: z[k] for k in z.files}
    else:
        res, loc = build_with_locals(lam=LAM, dy=dy, n_eta=N_ETA, verbose=False)
        keep = ["yca", "lxc", "logEc", "Uc", "lc", "rhoM", "rI", "rhoJ", "sS", "gE", "eta", "Deta", "W", "Qs", "NsE", "Pi0"]
        F = {k: np.asarray(loc[k], dtype=float) for k in keep}
        F["y_tail0"] = np.array(loc["y_tail0"]); F["c_inf"] = np.array(loc["c_inf"]); F["P_star"] = np.array(loc["P_star"])
        F["stage_starts"] = np.array([loc["b"][k] for k in ["axl", "axU", "int1", "int", "pulse", "interp", "hold", "ext1", "hold1", "ext2", "holdh"]])
        F["gates"] = np.array(json.dumps({k: v[0] for k, v in P.gates(res).items()}))
        if cache is not None:
            Path(cache).mkdir(parents=True, exist_ok=True)
            np.savez(Path(cache) / f"{tag}.npz", **F)
    eta, Deta = F["eta"], F["Deta"]
    f = 1.0 / (1.0 + eta ** 2); d = 1.0 - eta ** 2; L = 1.0 - 2 * H * eta ** 2
    P_star = float(F["P_star"])
    # --- numerical part, y >= 0
    y1, lx1, logE1, U1, W1 = F["yca"], F["lxc"], F["logEc"], F["Uc"], F["W"]
    E1 = np.exp(logE1)
    Pi1 = -0.5 * F["gE"] * E1 ** 2
    if drop_U:
        U1 = np.zeros_like(U1); W1 = np.ones_like(W1)
    v01 = (2 * eta[None, :] * U1 + W1 - 1.0) / L[None, :]
    # --- closed-form reference branch on [-5, 0): U = 4 eta, E = P_* f x^{1/10}, A_X(U) = 4 eta, Pi = Pi_0 + (5/2) P_*^2 f^2 x^{1/5}
    n0 = int(round(5.0 / dy))
    y0 = -5.0 + dy * np.arange(n0)                       # excludes 0 (the numerical grid starts there)
    lx0 = np.log(1e12) + y0
    logE0 = (np.log(P_star * f))[None, :] + 0.1 * y0[:, None]
    U0 = np.tile(4.0 * eta[None, :], (n0, 1))
    W0 = np.tile((1.0 - 8 * D * eta ** 2 - 4 * d)[None, :], (n0, 1))
    if drop_U:
        U0 = np.zeros_like(U0); W0 = np.ones_like(W0)
    v00 = (2 * eta[None, :] * U0 + W0 - 1.0) / L[None, :]
    Pi_0 = F["Pi0"]                                       # Pi(0, eta) (the axis datum, (4.31))
    Pi0_arr = Pi_0[None, :] + 2.5 * (P_star * f)[None, :] ** 2 * np.exp(0.2 * y0)[:, None]
    y = np.concatenate([y0, y1]); lx = np.concatenate([lx0, lx1])
    G = {"y": y, "lx": lx, "logE": np.vstack([logE0, logE1]), "U": np.vstack([U0, U1]), "v0": np.vstack([v00, v01]),
         "Pi": np.vstack([Pi0_arr, Pi1]), "W": np.vstack([W0, W1]), "eta": eta, "Deta": Deta, "f": f, "d": d, "L": L,
         "P_star": P_star, "y_tail0": float(F["y_tail0"]), "c_inf": float(F["c_inf"]), "stage_starts": F["stage_starts"],
         "gates": json.loads(str(F["gates"])), "n_inner": n0}
    G["E"] = np.exp(G["logE"])
    return G


# ----------------------------------------------------------------------------------------------
# Chebyshev barycentric interpolation in eta (the profiles are smooth in eta)
# ----------------------------------------------------------------------------------------------
def bary_weights(x):
    n = len(x)
    w = np.ones(n)
    for j in range(n):
        w[j] = 1.0 / np.prod([x[j] - x[k] for k in range(n) if k != j])
    return w


def bary_eval(x, w, vals, xq):
    """vals: (..., n) at nodes x; returns (..., len(xq))."""
    xq = np.asarray(xq, dtype=float)
    out = np.zeros(vals.shape[:-1] + (len(xq),))
    for i, xx in enumerate(xq):
        hit = np.where(np.abs(xx - x) < 1e-14)[0]
        if len(hit):
            out[..., i] = vals[..., hit[0]]
        else:
            c = w / (xx - x)
            out[..., i] = (vals * c).sum(axis=-1) / c.sum()
    return out


# ----------------------------------------------------------------------------------------------
# the two norms
# ----------------------------------------------------------------------------------------------
def radial_integrals(G):
    """e2(eta) = int_0^inf (E^2 + U^2) dX, g2(eta) = int_0^inf (X v_0^2/2) dX, split into the closed-form axis piece
    X < X_h = X_R e^{-5} and the gridded piece; dX = X dy. Also the pieces on X < X_R (the reference branch)."""
    y, lx, E, U, v0, eta, f, d, L = G["y"], G["lx"], G["E"], G["U"], G["v0"], G["eta"], G["f"], G["d"], G["L"]
    X = np.exp(lx)[:, None]
    P_star = G["P_star"]
    Xh = 1e12 * np.exp(-5.0)
    # X < X_h (closed form): int E^2 dX = P_*^2 f^2 X_R (5/6) x_h^{6/5}; int U^2 = 16 eta^2 X_h; int X v_0^2/2 = v_0^2 X_h^2/4
    xh = np.exp(-5.0)
    e2_axis = (P_star * f) ** 2 * 1e12 * (5.0 / 6.0) * xh ** 1.2 + 16 * eta ** 2 * Xh
    v0_ref = (8 * eta ** 2 - 8 * D * eta ** 2 - 4 * d) / L if not np.allclose(U[0], 0) else np.zeros_like(eta)
    g2_axis = v0_ref ** 2 * Xh ** 2 / 4.0
    e2_grid = np.trapezoid((E ** 2 + U ** 2) * X, y, axis=0)
    g2_grid = np.trapezoid(0.5 * X ** 2 * v0 ** 2, y, axis=0)
    # tail beyond the grid: E = c X^{-A} f_o (U = v_0 = 0): int_{X_end}^inf E^2 dX = E_end^2 X_end/(2A)
    e2_tail = E[-1] ** 2 * np.exp(lx[-1]) / (2 * A)
    m_in = y < 0
    e2_in = e2_axis + np.trapezoid(((E ** 2 + U ** 2) * X)[m_in], y[m_in], axis=0)
    return {"e2": e2_axis + e2_grid + e2_tail, "g2": g2_axis + g2_grid, "e2_axis": e2_axis, "g2_axis": g2_axis,
            "e2_tail": e2_tail, "e2_inner_XR": e2_in}


def eta_quadrature(eta, w, vals, weight_exp, eta_max, n1=4001, n2=6000):
    """int_{-eta_max}^{eta_max} L d^{weight_exp} vals(eta) d_eta with vals on the Chebyshev nodes; split at |eta| = 0.5
    (uniform in eta) and [0.5, eta_max] (uniform in log d, d = 1 - eta^2), both sides."""
    def piece(e):
        v = bary_eval(eta, w, vals, e)
        dd = 1.0 - e ** 2; LL = 1.0 - 2 * H * e ** 2
        return LL * dd ** weight_exp * v
    e_a = np.linspace(-0.5, 0.5, n1)
    tot = np.trapezoid(piece(e_a), e_a)
    if eta_max > 0.5:
        d_hi, d_lo = 0.75, 1.0 - eta_max ** 2
        ld = np.linspace(np.log(d_hi), np.log(d_lo), n2)
        dd = np.exp(ld); e = np.sqrt(1.0 - dd)
        # d_eta = -dd/(2 eta) = -(d/(2 eta)) d(log d); integrate from d_hi down to d_lo -> positive
        integrand = piece(e) * dd / (2 * e)
        side = -np.trapezoid(integrand, ld)
        tot += 2 * side
    return tot


def norms(G, taus, A_vel=A):
    """L^2 (core, {q < q*}, truncated-eta divergence study) and L^inf at each tau. A_vel is the velocity power
    (the control C_A replaces A by 0.85 in the velocity powers only)."""
    eta, d, L = G["eta"], G["d"], G["L"]
    w = bary_weights(eta)
    RI = radial_integrals(G)
    e2, g2 = RI["e2"], RI["g2"]
    p_t = 1.0 + D - 2 * A_vel           # tangential tau-power of the norm^2
    p_r = D                              # radial
    w_t = 2 * A_vel - 2 - D
    w_r = -1.0 - D
    I_t_core = eta_quadrature(eta, w, e2, w_t, ETA_CORE)
    I_r_core = eta_quadrature(eta, w, g2, w_r, ETA_CORE)
    out = {"tau": taus.tolist(), "core_eta_c": ETA_CORE}
    L2_core = np.sqrt(2 * np.pi * (taus ** p_t * I_t_core + taus ** p_r * I_r_core))
    L2_core_t = np.sqrt(2 * np.pi * taus ** p_t * I_t_core)
    L2_core_r = np.sqrt(2 * np.pi * taus ** p_r * I_r_core)
    out["L2_core"] = L2_core.tolist(); out["L2_core_tangential"] = L2_core_t.tolist(); out["L2_core_radial"] = L2_core_r.tolist()
    # direct per-tau quadrature (q = tau/d at every point, no factorisation) as a quadrature-drift check at 3 taus
    drift = []
    for tau in (taus[0], taus[len(taus) // 2], taus[-1]):
        def integrand_e(e):
            v_e = bary_eval(eta, w, e2, e); v_g = bary_eval(eta, w, g2, e)
            dd = 1 - e ** 2; LL = 1 - 2 * H * e ** 2; q = tau / dd
            return 2 * np.pi * q ** (1 + D) * (LL / dd) * (q ** (-2 * A_vel) * v_e + q ** (-1) * v_g)
        e_a = np.linspace(-ETA_CORE, ETA_CORE, 8001)
        direct = np.sqrt(np.trapezoid(integrand_e(e_a), e_a))
        fact = np.sqrt(2 * np.pi * (tau ** p_t * I_t_core + tau ** p_r * I_r_core))
        drift.append({"tau": float(tau), "direct": float(direct), "factorised": float(fact), "rel_diff": float(abs(direct - fact) / fact)})
    out["L2_core_direct_vs_factorised"] = drift
    # {q < q*}: d >= tau/q*
    for qs in Q_STARS:
        vals = []
        for tau in taus:
            eta_max = np.sqrt(max(1.0 - tau / qs, 0.0))
            if eta_max <= 0.5:
                vals.append(float("nan")); continue
            It = eta_quadrature(eta, w, e2, w_t, eta_max); Ir = eta_quadrature(eta, w, g2, w_r, eta_max)
            vals.append(float(np.sqrt(2 * np.pi * (tau ** p_t * It + tau ** p_r * Ir))))
        out[f"L2_q_lt_{qs:g}"] = vals
    # R^3: truncated-eta divergence at one tau
    tau0 = 1e-3
    trunc = []
    for eta_c in (0.9, 0.99, 0.999, 0.9999, 0.99999, 0.999999):
        It = eta_quadrature(eta, w, e2, w_t, eta_c); Ir = eta_quadrature(eta, w, g2, w_r, eta_c)
        trunc.append({"eta_c": eta_c, "d_c": 1 - eta_c ** 2, "L2_sq": float(2 * np.pi * (tau0 ** p_t * It + tau0 ** p_r * Ir))})
    dc = np.array([t["d_c"] for t in trunc]); ns2 = np.array([t["L2_sq"] for t in trunc])
    slope = np.polyfit(np.log(dc[-4:]), np.log(ns2[-4:]), 1)[0]
    out["R3_truncated_eta_at_tau_1e-3"] = {"points": trunc, "fitted_dlog(L2^2)/dlog(d_c)_last4": float(slope),
                                           "predicted": -0.5 + 3 * H, "diverges": bool(slope < -0.4)}
    # L^inf: |u|^2 = tau^{-1} d G^2 + tau^{-2A} d^{2A} (E^2 + U^2) on the grid, parabolic refinement in y
    y, lx, E, U, v0 = G["y"], G["lx"], G["E"], G["U"], G["v0"]
    Gr = np.exp(0.5 * (lx - np.log(2.0)))[:, None] * v0          # sqrt(X/2) v_0
    dA = d ** A_vel
    def sup_refined(F2):
        i, j = np.unravel_index(np.argmax(F2), F2.shape)
        if 0 < i < len(y) - 1:
            a, b, c = F2[i - 1, j], F2[i, j], F2[i + 1, j]
            den = a - 2 * b + c
            val = b - 0.125 * (c - a) ** 2 / den if den < 0 else b
            yy = y[i] + 0.5 * (a - c) / den * (y[i + 1] - y[i]) if den < 0 else y[i]
        else:
            val, yy = F2[i, j], y[i]
        return float(np.sqrt(max(val, 0.0))), float(yy), float(eta[j])
    Linf, Linf_th, Linf_r, Linf_z, locs = [], [], [], [], []
    for tau in taus:
        th2 = (tau ** (-2 * A_vel)) * (dA[None, :] ** 2) * E ** 2
        z2 = (tau ** (-2 * A_vel)) * (dA[None, :] ** 2) * U ** 2
        r2 = (tau ** -1) * d[None, :] * Gr ** 2
        s_all = sup_refined(th2 + z2 + r2); s_th = sup_refined(th2); s_r = sup_refined(r2); s_z = sup_refined(z2)
        Linf.append(s_all[0]); Linf_th.append(s_th[0]); Linf_r.append(s_r[0]); Linf_z.append(s_z[0])
        locs.append({"all": s_all[1:], "theta": s_th[1:], "r": s_r[1:], "z": s_z[1:]})
    out["Linf"] = Linf; out["Linf_theta"] = Linf_th; out["Linf_r"] = Linf_r; out["Linf_z"] = Linf_z
    out["Linf_location_y_eta"] = {"first_tau": locs[0], "last_tau": locs[-1]}
    out["radial_integrals"] = {"e2_at_eta0": float(e2[len(eta) // 2]), "g2_at_eta0": float(g2[len(eta) // 2]),
                               "e2_axis_share_eta0": float(RI["e2_axis"][len(eta) // 2] / e2[len(eta) // 2]),
                               "e2_inner_XR_share_eta0": float(RI["e2_inner_XR"][len(eta) // 2] / e2[len(eta) // 2]),
                               "e2_tail_share_eta0": float(RI["e2_tail"][len(eta) // 2] / e2[len(eta) // 2]),
                               "I_t_core": float(I_t_core), "I_r_core": float(I_r_core)}
    return out


def fit_exponent(taus, vals):
    m = np.isfinite(vals) & (np.asarray(vals) > 0)
    lt, lv = np.log(taus[m]), np.log(np.asarray(vals)[m])
    slope, icpt = np.polyfit(lt, lv, 1)
    resid = lv - (slope * lt + icpt)
    local = np.diff(lv) / np.diff(lt)
    return {"slope": float(slope), "max_abs_log_residual": float(np.max(np.abs(resid))), "local_slope_first": float(local[0]),
            "local_slope_last": float(local[-1]), "endpoint_slope": float((lv[-1] - lv[0]) / (lt[-1] - lt[0]))}


# ----------------------------------------------------------------------------------------------
# the force f^(0) = NS(u^(0)) in similarity variables
# ----------------------------------------------------------------------------------------------
def force_profiles(G, A_vel=A):
    y, lx, E, U, v0, Pi, eta, Deta, d, L = G["y"], G["lx"], G["E"], G["U"], G["v0"], G["Pi"], G["eta"], G["Deta"], G["d"], G["L"]
    ny = len(y)
    dX = lambda g: np.gradient(g, y, axis=0, edge_order=2)          # D_X = d/dy
    de = lambda g: g @ Deta.T
    T = lambda b, g: (-b * g + D * eta[None, :] * de(g) + dX(g)) / L[None, :]
    Z = lambda b, g: (2 * b * eta[None, :] * g + d[None, :] * de(g) - 2 * eta[None, :] * dX(g)) / L[None, :]
    s2X = np.exp(0.5 * (np.log(2.0) + lx))[:, None]                # sqrt(2X)
    R = lambda g: np.sqrt(2.0) * np.exp(-0.5 * lx)[:, None] * dX(g)   # sqrt(2/X) D_X g = sqrt(2X) g_X
    inv_s2X = 1.0 / s2X; inv_2X = np.exp(-np.log(2.0) - lx)[:, None]
    Gr = np.exp(0.5 * (lx - np.log(2.0)))[:, None] * v0            # G = sqrt(X/2) v_0
    Av = A_vel
    R_r = T(-0.5, Gr) + Gr * R(Gr) + U * Z(-0.5, Gr) - R(R(Gr)) - R(Gr) * inv_s2X + Gr * inv_2X
    R_r_ax = -Z(-0.5 - D, Z(-0.5, Gr))
    inv_th = T(-Av, E) + Gr * R(E) + U * Z(-Av, E) + Gr * E * inv_s2X
    R_th = inv_th - R(R(E)) - R(E) * inv_s2X + E * inv_2X
    R_th_ax = -Z(-Av - D, Z(-Av, E))
    inv_z = T(-Av, U) + Gr * R(U) + U * Z(-Av, U) + Z(-2 * Av, Pi)
    R_z = inv_z - R(R(U)) - R(U) * inv_s2X
    R_z_ax = -Z(-Av - D, Z(-Av, U))
    # checks K0-K2 (paper's identities, with the paper's A)
    Hh = s2X * E; W = G["W"]; Hc = D * eta[None, :] + d[None, :] * U
    l = dX(np.log(Hh))
    K1_rhs = (W * dX(Hh) + Hc * de(Hh) + H * (1 - 2 * eta[None, :] * U) * Hh) / L[None, :]
    K1_lhs = s2X * inv_th
    Sn = -W * dX(U) - A * (1 - 2 * eta[None, :] * U) * U - Hc * de(U) - d[None, :] * de(Pi) + 4 * A * eta[None, :] * Pi + 2 * eta[None, :] * dX(Pi)
    K2_lhs, K2_rhs = inv_z, -Sn / L[None, :]
    K0_lhs = v0 + dX(v0)                                          # D_X(X v_0)/X
    K0_rhs = (2 * A * eta[None, :] * U - d[None, :] * de(U) + 2 * eta[None, :] * dX(U)) / L[None, :]
    def relerr(a, b, m):
        sc = np.max(np.abs(b[m])) if np.max(np.abs(b[m])) > 0 else 1.0
        return float(np.max(np.abs(a[m] - b[m])) / sc)
    interior = np.ones(ny, bool); interior[:3] = False; interior[-3:] = False
    m = np.zeros_like(E, bool); m[interior, 1:-1] = True
    checks = {"K1_rel_max_(4.14)": relerr(K1_lhs, K1_rhs, m), "K2_rel_max_Sn": relerr(K2_lhs, K2_rhs, m),
              "K0_rel_max_incompressibility": relerr(K0_lhs, K0_rhs, m), "l_minus_lc_note": "l recomputed from H"}
    return {"R_r": R_r, "R_r_ax": R_r_ax, "R_th": R_th, "R_th_ax": R_th_ax, "R_z": R_z, "R_z_ax": R_z_ax, "checks": checks,
            "s2X": s2X}


def force_sup(G, FP, taus, A_vel=A, regions=None):
    y, d, eta = G["y"], G["d"], G["eta"]
    Av = A_vel
    dd = d[None, :]
    if regions is None:
        ss = G["stage_starts"]
        regions = {"all_X_ge_Xh": (y >= -5.0), "inner_reference_y<0": (y < 0), "y_in_[0,pulse)": (y >= 0) & (y < ss[4]),
                   "pulse_to_tail": (y >= ss[4]) & (y < G["y_tail0"]), "tail": y >= G["y_tail0"]}
    out = {}
    for name, m in regions.items():
        mm = m[:, None] & (np.abs(eta) < 1)[None, :]
        vals, comp, locs = [], [], []
        for tau in taus:
            q = tau / dd
            fr = q ** -1.5 * FP["R_r"] + q ** (-1.5 + 2 * H) * FP["R_r_ax"]
            fth = q ** (-Av - 1) * FP["R_th"] + q ** (-Av - 2 * D) * FP["R_th_ax"]
            fz = q ** (-Av - 1) * FP["R_z"] + q ** (-Av - 2 * D) * FP["R_z_ax"]
            mag = np.sqrt(fr ** 2 + fth ** 2 + fz ** 2)
            mag = np.where(mm, mag, 0.0)
            i, j = np.unravel_index(np.argmax(mag), mag.shape)
            vals.append(float(mag[i, j]))
            comp.append([float(abs(fr[i, j])), float(abs(fth[i, j])), float(abs(fz[i, j]))])
            locs.append([float(y[i]), float(eta[j])])
        out[name] = {"sup": vals, "components_r_th_z_at_sup_first_last": [comp[0], comp[-1]], "loc_y_eta_first_last": [locs[0], locs[-1]],
                     "fit": fit_exponent(taus, np.array(vals))}
    return out


# ----------------------------------------------------------------------------------------------
# K3: physical-space finite differences at sample points (independent route)
# ----------------------------------------------------------------------------------------------
def physical_check(G, FP, tau, points):
    from scipy.interpolate import CubicSpline
    y, lx, eta = G["y"], G["lx"], G["eta"]
    w = bary_weights(eta)
    m = y <= 60.0                                  # the sample points live in the inner region; keep the spline small
    sp = {k: CubicSpline(y[m], G[k][m], axis=0) for k in ("logE", "U", "v0", "Pi")}
    def prof(yy, ee):
        return {k: float(bary_eval(eta, w, sp[k](yy), [ee])[0]) for k in sp}
    def q_of(z, tau_):
        q = tau_ + abs(z) ** (1 / D)
        for _ in range(60):
            g = q - z * z * q ** (2 * H) - tau_
            q -= g / (1 - 2 * H * z * z * q ** (2 * H - 1))
        return q
    def field(r, z, t):
        tau_ = 1 - t; q = q_of(z, tau_); X = r * r / (2 * q); yy = np.log(X / 1e12); ee = z / q ** D
        p = prof(yy, ee)
        E = np.exp(p["logE"])
        ur = q ** -0.5 * np.sqrt(X / 2) * p["v0"]; uth = q ** -A * E; uz = q ** -A * p["U"]; pr = q ** (-2 * A) * p["Pi"]
        return np.array([ur, uth, uz, pr])
    def d1(fun, x, hstep):
        return (-fun(x + 2 * hstep) + 8 * fun(x + hstep) - 8 * fun(x - hstep) + fun(x - 2 * hstep)) / (12 * hstep)
    def d2(fun, x, hstep):
        return (-fun(x + 2 * hstep) + 16 * fun(x + hstep) - 30 * fun(x) + 16 * fun(x - hstep) - fun(x - 2 * hstep)) / (12 * hstep ** 2)
    res = []
    for (yy, ee) in points:
        q = tau / (1 - ee ** 2); X = 1e12 * np.exp(yy); r = np.sqrt(2 * q * X); z = q ** D * ee; t = 1 - tau
        hr, hz, ht = 2e-4 * r, 2e-4 * max(abs(z), q ** D), 2e-4 * tau
        u = field(r, z, t)
        ur_, uth_, uz_ = u[:3]
        Fr = lambda rr: field(rr, z, t); Fz = lambda zz: field(r, zz, t); Ft = lambda tt: field(r, z, tt)
        ut = d1(Ft, t, ht); u_r = d1(Fr, r, hr); u_z = d1(Fz, z, hz); u_rr = d2(Fr, r, hr); u_zz = d2(Fz, z, hz)
        lap = lambda k: u_rr[k] + u_r[k] / r + u_zz[k]
        NS_r = ut[0] + ur_ * u_r[0] + uz_ * u_z[0] - uth_ ** 2 / r - (lap(0) - ur_ / r ** 2) + u_r[3]
        NS_th = ut[1] + ur_ * u_r[1] + uz_ * u_z[1] + ur_ * uth_ / r - (lap(1) - uth_ / r ** 2)
        NS_z = ut[2] + ur_ * u_r[2] + uz_ * u_z[2] - lap(2) + u_z[3]
        # similarity-variable route at the same (y, eta), interpolated on the grid
        i = int(np.argmin(np.abs(y - yy)))
        def simv(name):
            return float(bary_eval(eta, w, FP[name][i], [ee])[0])
        qq = q
        S_r = qq ** -1.5 * simv("R_r") + qq ** (-1.5 + 2 * H) * simv("R_r_ax")
        S_th = qq ** (-A - 1) * simv("R_th") + qq ** (-A - 2 * D) * simv("R_th_ax")
        S_z = qq ** (-A - 1) * simv("R_z") + qq ** (-A - 2 * D) * simv("R_z_ax")
        sim = np.array([S_r, S_th, S_z]); fd = np.array([NS_r, NS_th, NS_z])
        res.append({"y": yy, "eta": ee, "y_grid": float(y[i]), "fd": fd.tolist(), "similarity": sim.tolist(),
                    "rel_diff": float(np.linalg.norm(fd - sim) / np.linalg.norm(sim)),
                    "u_r_theta_z": [float(ur_), float(uth_), float(uz_)]})
    return res


# ----------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=None)
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    t0 = time.time()
    dys = (4e-3,) if args.quick else DYS
    taus = TAUS
    measured = {"dy": list(dys), "taus": taus.tolist(), "per_dy": {}}
    profiles = {}
    for dy in dys:
        G = profile_fields(dy, cache=args.cache)
        profiles[dy] = G
        N = norms(G, taus)
        FP = force_profiles(G)
        FS = force_sup(G, FP, taus)
        fits = {k: fit_exponent(taus, np.array(N[k])) for k in ("L2_core", "L2_core_tangential", "L2_core_radial", "Linf", "Linf_theta", "Linf_r", "Linf_z")}
        for qs in Q_STARS:
            fits[f"L2_q_lt_{qs:g}"] = fit_exponent(taus, np.array(N[f"L2_q_lt_{qs:g}"]))
        measured["per_dy"][f"{dy:g}"] = {"norms": N, "fits": fits, "force": FS, "force_checks": FP["checks"],
                                         "profile_gates_G1_G8": G["gates"], "y_tail0": G["y_tail0"], "c_inf": G["c_inf"], "n_y": int(len(G["y"]))}
        print(f"[{time.time()-t0:.0f}s] dy={dy}: L2core slope {fits['L2_core']['slope']:.9f} Linf_theta slope {fits['Linf_theta']['slope']:.9f} "
              f"Linf slope {fits['Linf']['slope']:.9f} |f| slope {FS['all_X_ge_Xh']['fit']['slope']:.6f} checks {FP['checks']}")
        if dy == dys[-1]:
            pts = [(-2.0, 0.0), (-2.0, 0.5), (0.5, 0.3), (2.0, -0.4), (5.0, 0.6), (20.0, 0.2), (40.0, 0.0)]
            measured["K3_physical_space_fd_at_tau_1e-3"] = physical_check(G, FP, 1e-3, pts)
            print(f"[{time.time()-t0:.0f}s] K3:", [round(r["rel_diff"], 6) for r in measured["K3_physical_space_fd_at_tau_1e-3"]])
    # --- refinement stability across dy (relative, in the norm, at every tau)
    keys = ("L2_core", "Linf", "Linf_theta", "L2_q_lt_0.1")
    fine = measured["per_dy"][f"{dys[-1]:g}"]["norms"]
    stab = {}
    for k in keys:
        stab[k] = {}
        for dy in dys[:-1]:
            a = np.array(measured["per_dy"][f"{dy:g}"]["norms"][k]); b = np.array(fine[k])
            mm = np.isfinite(a) & np.isfinite(b)
            stab[k][f"dy{dy:g}_vs_dy{dys[-1]:g}_max_rel"] = float(np.max(np.abs(a[mm] - b[mm]) / np.abs(b[mm])))
        stab[k]["slopes_by_dy"] = {f"{dy:g}": measured["per_dy"][f"{dy:g}"]["fits"][k]["slope"] for dy in dys}
    measured["refinement_stability"] = stab
    fsup = {f"{dy:g}": measured["per_dy"][f"{dy:g}"]["force"]["all_X_ge_Xh"]["fit"]["slope"] for dy in dys}
    measured["force_slope_by_dy"] = fsup
    # --- controls at the coarsest dy (their twin: the unmodified run at the same dy)
    dyc = dys[0]
    Gc = profiles[dyc]
    twin = measured["per_dy"][f"{dyc:g}"]
    NA = norms(Gc, taus, A_vel=0.85)
    fitA = {k: fit_exponent(taus, np.array(NA[k])) for k in ("L2_core", "Linf_theta", "Linf")}
    GU = profile_fields(dyc, cache=args.cache, drop_U=True)
    NU = norms(GU, taus)
    fitU = {k: fit_exponent(taus, np.array(NU[k])) for k in ("L2_core", "Linf_theta", "Linf", "Linf_r")}
    controls = {
        "C_A_0.85": {"expected": "core L^2 exponent = (1 + D - 2*0.85)/2 = -0.1 - h/2 < 0: the norm DIVERGES (sign flips); L^inf(u_theta) exponent -0.85",
                     "measured": {"L2_core_slope": fitA["L2_core"]["slope"], "L2_core_first_last": [NA["L2_core"][0], NA["L2_core"][-1]],
                                  "Linf_theta_slope": fitA["Linf_theta"]["slope"], "Linf_slope": fitA["Linf"]["slope"]},
                     "twin": {"L2_core_slope": twin["fits"]["L2_core"]["slope"], "Linf_theta_slope": twin["fits"]["Linf_theta"]["slope"]},
                     "fired": bool(fitA["L2_core"]["slope"] < 0 and abs(fitA["L2_core"]["slope"] - (-0.1 - 0.5 * H)) < 1e-4)},
        "C_U_zero": {"expected": "V_0 = 0 (W = 1, A_X(U) = 0), u_r = 0: the L^inf location moves from the u_r point to the u_theta peak; exponent exactly -A",
                     "measured": {"Linf_slope": fitU["Linf"]["slope"], "Linf_r_max": float(np.nanmax(NU["Linf_r"])),
                                  "Linf_location_first_tau": NU["Linf_location_y_eta"]["first_tau"], "L2_core_slope": fitU["L2_core"]["slope"],
                                  "L2_core_radial_first": NU["L2_core_radial"][0]},
                     "twin": {"Linf_slope": twin["fits"]["Linf"]["slope"], "Linf_location_first_tau": twin["norms"]["Linf_location_y_eta"]["first_tau"]},
                     "fired": bool(NU["Linf_location_y_eta"]["first_tau"]["all"] != twin["norms"]["Linf_location_y_eta"]["first_tau"]["all"]
                                   and abs(fitU["Linf"]["slope"] + A) < 1e-6)},
        "twin_passes_V1": None,
    }
    # --- gates
    fine_fits = measured["per_dy"][f"{dys[-1]:g}"]["fits"]
    v1_linf = abs(fine_fits["Linf_theta"]["slope"] + A) < 1e-4
    v1_l2 = abs(fine_fits["L2_core"]["slope"] - (0.25 - 1.5 * H)) < 1e-4
    v1_stab = all(stab[k][f"dy{dy:g}_vs_dy{dys[-1]:g}_max_rel"] < 1e-6 for k in ("L2_core", "Linf_theta") for dy in dys[:-1]) if len(dys) > 1 else False
    v1_all_slopes_ok = all(abs(measured["per_dy"][f"{dy:g}"]["fits"]["Linf_theta"]["slope"] + A) < 1e-4 and
                           abs(measured["per_dy"][f"{dy:g}"]["fits"]["L2_core"]["slope"] - (0.25 - 1.5 * H)) < 1e-4 for dy in dys)
    V1 = "YES" if (v1_linf and v1_l2 and v1_stab and v1_all_slopes_ok) else "NO"
    fslopes = list(fsup.values())
    V2 = "YES" if all(abs(s - (-1.5 - H)) < 0.01 for s in fslopes) else "NO"
    V3 = "YES" if v1_stab else "NO"
    controls["twin_passes_V1"] = bool(abs(twin["fits"]["Linf_theta"]["slope"] + A) < 1e-4 and abs(twin["fits"]["L2_core"]["slope"] - (0.25 - 1.5 * H)) < 1e-4)
    gates = {
        "V1": {"answer": V1, "Linf_theta_slope_finest": fine_fits["Linf_theta"]["slope"], "target": -A, "tol": 1e-4,
               "Linf_full_slope_finest": fine_fits["Linf"]["slope"], "Linf_r_slope_finest": fine_fits["Linf_r"]["slope"],
               "L2_core_slope_finest": fine_fits["L2_core"]["slope"], "L2_target_from_bookkeeping": 0.25 - 1.5 * H,
               "refinement_max_rel": {k: {kk: vv for kk, vv in stab[k].items() if kk != "slopes_by_dy"} for k in ("L2_core", "Linf_theta")},
               "note": "the -A vs -1/2 (h = 1e-7) and 1/4-3h/2 vs 1/4-h/2 distinctions are below the gate's 1e-4 (said in CLAIMED)."},
        "V2": {"answer": V2, "force_slope_by_dy": fsup, "target": -1.5 - H, "tol": 0.01,
               "sup_f_first_last_finest": [measured["per_dy"][f"{dys[-1]:g}"]["force"]["all_X_ge_Xh"]["sup"][0],
                                            measured["per_dy"][f"{dys[-1]:g}"]["force"]["all_X_ge_Xh"]["sup"][-1]],
               "gap": "the leading order's force grows like q^{-3/2-h}: NOT bounded at t = 1; the paper's corrected f is bounded and flat "
                      "(Theorem 3.1(iii)): the corrections must close 3/2 + h powers for boundedness and every power for flatness."},
        "V3": {"answer": V3, "statement": "T* = 1 is prescribed (tau = 1 - t); WIN_CONDITION's 'T* stable under refinement' cannot be tested on a "
                                          "prescribed field; reported instead: the norms' fits are refinement-stable (numbers in V1) and the "
                                          "quadrature/conservation drifts below.",
               "quadrature_drift_direct_vs_factorised": measured["per_dy"][f"{dys[-1]:g}"]["norms"]["L2_core_direct_vs_factorised"],
               "incompressibility_K0_by_dy": {f"{dy:g}": measured["per_dy"][f"{dy:g}"]["force_checks"]["K0_rel_max_incompressibility"] for dy in dys},
               "centrifugal_balance": "exact by construction (Pi_X = E^2/(2X) is the definition of Pi; the q^{-2A-1/2} terms cancel identically)"},
    }
    out = {"schema": "arc6_wave4_v1", "agent": 5, "unit": "(v) headline", "leg": 433,
           "pages_read": [7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44],
           "prereg": "experiments/journal/leg_433_prereg.md section 2 (v)", "profile": str(PROFILE.relative_to(ROOT)),
           "claimed": CLAIMED, "measured": measured, "gates": gates, "controls": controls,
           "instantiated_vs_scaled": (
               "What is instantiated is the pinned lambda = 0.1 outer profile (closure G3 and cone G7 fail there, leg 430) with Lemma 4.8(i)'s "
               "temporary inner branch in place of the paper's Appendix B axis profile; the paper's regime is lambda <~ 3e-4 and h = 1e-7 is "
               "pinned. The two headline norms are EXACT SCALINGS of this prescribed field under q -> 0: u_theta = q^{-A} E and the volume "
               "element q^{1+D} L/d dX d_eta make ||u_theta||_inf ~ tau^{-A} and the core energy ~ tau^{1/2-3h} identities, not measurements of "
               "any dynamics; the resolutions test only the quadrature of tau-independent profile integrals. This signal is therefore not by "
               "itself evidence of Navier-Stokes blowup: any prescribed u solves the forced equation with f := NS(u), and the leading order's "
               "own f grows like q^{-3/2-h}. Whether the corrected f is bounded and flat (Theorem 3.1(iii)) is what the arc's other units and the "
               "proof carry; nothing here tests it."),
           "could_not_determine": [
               "I could not determine ||u^(0)(t)||_{L^2(R^3)} as a finite number, because it is infinite: the eta-weight d^{-3/2+3h} of the "
               "change of variables is not integrable at eta = +-1 (measured: the truncated norm^2 diverges with the predicted exponent). The "
               "bounded-energy headline is a statement about the cut-off field (chi_x, p. 16) or the core, not about the leading field on R^3.",
               "I could not determine the paper's q* (Theorem 3.1, 'sufficiently small'), because the paper does not give it; the {q < q*} norms "
               "are reported for q* in {0.1, 1} and their limits scale as q*^{1/4-3h/2}.",
               "I could not determine the paper's magnitude of ||f^(0)||_inf (only its exponent), because the pinned profile has no Appendix B "
               "axis profile: on X <= X_h the paper's leading field balances the axial pressure gradient Z_{-2A} Pi ~ P_*^2 that dominates the "
               "sup here, and on X < X_h the reference branch u_theta ~ r^{1/5} has a non-integrable Laplacian at the axis (sup = +inf there); "
               "the sup is therefore taken on X >= X_h.",
               "I could not separate the exponent -A from -1/2 (nor 1/4 - 3h/2 from 1/4 - h/2) by measurement, because h = 1e-7 is three "
               "orders below the pre-registered tolerance 1e-4; the component-wise norms carry the exact exponents by construction.",
           ],
           "gate_answer": None, "tier": "This is Tier 2, not a proof.", "runtime_s": time.time() - t0}
    fs = measured["per_dy"][f"{dys[-1]:g}"]
    out["gate_answer"] = (
        f"V1 {V1}: on the finest grid ||u_theta||_inf ~ tau^{fine_fits['Linf_theta']['slope']:.9f} (target -A = {-A}), full |u| ~ "
        f"tau^{fine_fits['Linf']['slope']:.9f}, u_r ~ tau^{fine_fits['Linf_r']['slope']:.9f}; the core L^2 norm ~ tau^{fine_fits['L2_core']['slope']:.9f} "
        f"(bookkeeping 1/4 - 3h/2 = {0.25 - 1.5*H}); refinement: max relative change of the norms between dy = 4e-3, 2e-3 and 1e-3 is "
        f"{max(v for k in ('L2_core','Linf_theta') for kk, v in stab[k].items() if kk != 'slopes_by_dy'):.2e}. The L^2(R^3) norm of the "
        f"un-cut-off leading field is infinite (truncated-eta divergence exponent {fs['norms']['R3_truncated_eta_at_tau_1e-3']['fitted_dlog(L2^2)/dlog(d_c)_last4']:.4f}, "
        f"predicted {-0.5 + 3*H}); on the paper's domain q < 0.1 the norm is bounded and tends to a constant (local slope at tau = 1e-6: "
        f"{fs['fits']['L2_q_lt_0.1']['local_slope_last']:.4f}). V2 {V2}: ||f^(0)||_inf ~ q^{fs['force']['all_X_ge_Xh']['fit']['slope']:.6f} "
        f"(target -3/2 - h), from {fs['force']['all_X_ge_Xh']['sup'][0]:.3e} at tau = 1e-1 to {fs['force']['all_X_ge_Xh']['sup'][-1]:.3e} at tau = 1e-6: "
        f"the leading order's force is not bounded at t = 1, the paper's corrected force is claimed bounded and flat; the gap is 3/2 + h powers "
        f"of q (and every power for flatness). V3 {V3}: T* = 1 is prescribed and 'T* stable under refinement' cannot be tested on a prescribed "
        f"field; the norm fits are refinement-stable as stated and the quadrature drift (direct vs factorised) is "
        f"{max(dd['rel_diff'] for dd in fs['norms']['L2_core_direct_vs_factorised']):.2e}, incompressibility residual "
        f"{fs['force_checks']['K0_rel_max_incompressibility']:.2e}. Controls: C_A fired = {controls['C_A_0.85']['fired']}, C_U fired = "
        f"{controls['C_U_zero']['fired']}, twin passes V1 = {controls['twin_passes_V1']}. This is Tier 2, not a proof.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, default=float) + "\n")
    print(out["gate_answer"])
    print("wrote", OUT, f"{OUT.stat().st_size:,} B in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
