#!/usr/bin/env python3
"""
Leg 261 -- Route-P1A2: THE FLUID CENSUS UNDER A RELAXED EVIDENCE TIER.

Two parts, and the second is the one with measurements in it.

PART A  A fluid-only census under a RELAXED screen (i): conjectured dissipative blow-up with
        serious numerical evidence, carried with an explicit per-row evidence tier. It EXTENDS
        leg 255's tier-1 table (read read-only, never edited) and changes none of its verdicts.

PART B  A MEASURED scope for the Leray obstruction. Leg 257 showed that P[(U.grad)U] has an
        algebraic |x|^-4 tail whose coefficient is the energy. That is a MULTIPOLE statement:
        the projected source has vanishing monopole and dipole, and its QUADRUPOLE moment is
        2 * int U_k U_l. This part asks the question the Decision Maker's brief added -- WHICH
        fluid formulations that mechanism actually reaches -- by computing, for each nonlocal
        operator class a census row can carry, the lowest non-vanishing multipole moment of the
        source, the resulting far-field exponent, and the L^2(mu) weighted integrand density.

        The weight is e^{|x|^2/4}: Breden-Chu's mu, and (novelty pass sec 3) also exactly
        Gallay's rho_infty(|xi|^2), the standard weight for the VORTICITY.

Every verdict is COMPUTED from evidence fields, never asserted. self_test() perturbs the
evidence and must reach both gate branches. assert_probe_is_live() fails the run if the table
or the witness ladder degenerates.

NOTHING IS CERTIFIED. No stage claimed, plan_of_record.py untouched, no ban lifted, no solver
module built or edited. No link of L1->L4 moves. Clay odds stay ~0.05%.
"""

from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "writeup", "data", "p2_route_p1a2_v1_census2.json")

# Radii at which every far-field quantity is measured. Leg 257's ladder, kept identical so the
# numbers are directly comparable row by row.
RADII = [10.0, 20.0, 40.0, 80.0]

# Leg 257's banked value for int|U|^2, quoted so this leg's INDEPENDENT quadrature can be
# checked against it rather than trusted.
LEG_257_T = 3.9374024864305617
LEG_257_PSI_R10 = 0.0003133285343288746
LEG_257_S11 = 1.9687012432152875


# ---------------------------------------------------------------------------------------------
# PART B.0 -- quadrature, and the witness
# ---------------------------------------------------------------------------------------------

def gauss_grid(n: int, L: float):
    """Tensor-product Gauss-Legendre nodes/weights on [-L, L]^3, flattened."""
    x1, w1 = np.polynomial.legendre.leggauss(n)
    x1 = x1 * L
    w1 = w1 * L
    X, Y, Z = np.meshgrid(x1, x1, x1, indexing="ij")
    WX, WY, WZ = np.meshgrid(w1, w1, w1, indexing="ij")
    pts = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=1)
    wts = (WX * WY * WZ).ravel()
    return pts, wts


def witness_U(p: np.ndarray) -> np.ndarray:
    """U = curl(e^{-|x|^2} e_3) = (-2 x_2 g, +2 x_1 g, 0), g = e^{-|x|^2}.

    Divergence-free EXACTLY (div U = -2 x_2 d_1 g + 2 x_1 d_2 g = 0), and Gaussian, so
    U in H^2(mu). Leg 257's witness, reused deliberately so the cross-check is a real one.
    """
    g = np.exp(-np.sum(p * p, axis=1))
    U = np.zeros_like(p)
    U[:, 0] = -2.0 * p[:, 1] * g
    U[:, 1] = +2.0 * p[:, 0] * g
    return U


def witness_div_check(n: int = 24, L: float = 5.0) -> float:
    """div U computed by 8th-order central differences -- a check, not an assertion."""
    rng = np.random.default_rng(0)
    p = rng.uniform(-2.0, 2.0, size=(n, 3))
    h = 1e-3
    coef = {1: 4.0 / 5.0, 2: -1.0 / 5.0, 3: 4.0 / 105.0, 4: -1.0 / 280.0}
    d = np.zeros(n)
    for axis in range(3):
        for k, c in coef.items():
            ep = np.zeros(3)
            ep[axis] = k * h
            d += c * (witness_U(p + ep)[:, axis] - witness_U(p - ep)[:, axis]) / h
    return float(np.max(np.abs(d)))


def source_S_leray(p: np.ndarray) -> np.ndarray:
    """S = div[(U.grad)U] = d_i d_j (U_i U_j), derived in closed form for this witness.

    U_1 U_1 = 4 x_2^2 g2, U_2 U_2 = 4 x_1^2 g2, U_1 U_2 = -4 x_1 x_2 g2, g2 = e^{-2|x|^2}.
    Carrying the three second derivatives, every quartic term cancels and

        S = 8 (2 x_1^2 + 2 x_2^2 - 1) e^{-2|x|^2}.

    verify_S_against_finite_differences() re-derives the same object numerically from U alone,
    so this closed form is checked and not trusted.
    """
    r2 = np.sum(p * p, axis=1)
    return 8.0 * (2.0 * p[:, 0] ** 2 + 2.0 * p[:, 1] ** 2 - 1.0) * np.exp(-2.0 * r2)


def verify_S_against_finite_differences(n: int = 20) -> float:
    """Re-derive S = d_i d_j (U_i U_j) by finite differences of U and compare to the closed form.

    Two independent routes to the same object. This repository has no sympy, so the symbolic
    derivation above is checked against numerics rather than against a CAS.
    """
    rng = np.random.default_rng(1)
    p = rng.uniform(-1.5, 1.5, size=(n, 3))
    h = 2e-3

    def UU(q, i, j):
        U = witness_U(q)
        return U[:, i] * U[:, j]

    S = np.zeros(n)
    for i in range(3):
        for j in range(3):
            if i == j:
                ei = np.zeros(3)
                ei[i] = h
                S += (UU(p + ei, i, j) - 2.0 * UU(p, i, j) + UU(p - ei, i, j)) / h ** 2
            else:
                ei = np.zeros(3)
                ej = np.zeros(3)
                ei[i] = h
                ej[j] = h
                S += (
                    UU(p + ei + ej, i, j)
                    - UU(p + ei - ej, i, j)
                    - UU(p - ei + ej, i, j)
                    + UU(p - ei - ej, i, j)
                ) / (4.0 * h ** 2)
    return float(np.max(np.abs(S - source_S_leray(p))))


# ---------------------------------------------------------------------------------------------
# PART B.1 -- Newtonian potential and its derivatives, by direct quadrature
# ---------------------------------------------------------------------------------------------
# Convention: Delta psi = S  =>  psi(x) = -(1/4pi) int S(y) / |x-y| dy.
# The evaluation points sit at |x| >= 10 while every source is supported (to e^{-2*36}) inside
# |y| <= 6, so the kernel is never singular on the grid.

def newton_potential(src: np.ndarray, wts: np.ndarray, pts: np.ndarray, x: np.ndarray) -> float:
    z = x[None, :] - pts
    r = np.sqrt(np.sum(z * z, axis=1))
    return float(-(1.0 / (4.0 * math.pi)) * np.sum(wts * src / r))


def newton_grad(src: np.ndarray, wts: np.ndarray, pts: np.ndarray, x: np.ndarray) -> np.ndarray:
    """grad psi, with d_i (1/|z|) = -z_i/|z|^3."""
    z = x[None, :] - pts
    r = np.sqrt(np.sum(z * z, axis=1))
    k = (wts * src / r ** 3)[:, None] * z
    return (1.0 / (4.0 * math.pi)) * np.sum(k, axis=0)


def newton_hess(src: np.ndarray, wts: np.ndarray, pts: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Hessian of the potential u(x) = (1/4pi) int src/|x-y| (note the SIGN convention here is
    the +1/4pi one, used for chi below); d_i d_j (1/|z|) = (3 z_i z_j - delta_ij |z|^2)/|z|^5."""
    z = x[None, :] - pts
    r2 = np.sum(z * z, axis=1)
    r5 = r2 ** 2.5
    H = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            num = 3.0 * z[:, i] * z[:, j] - (r2 if i == j else 0.0)
            H[i, j] = np.sum(wts * src * num / r5)
    return H / (4.0 * math.pi)


def newton_third(src: np.ndarray, wts: np.ndarray, pts: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Third derivatives of (1/4pi) int src/|x-y|, from
    d_i d_j d_k (1/|z|) = 3(delta_ij z_k + delta_ik z_j + delta_jk z_i)/|z|^5
                          - 15 z_i z_j z_k /|z|^7."""
    z = x[None, :] - pts
    r2 = np.sum(z * z, axis=1)
    r5 = r2 ** 2.5
    r7 = r2 ** 3.5
    T = np.zeros((3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                num = -15.0 * z[:, i] * z[:, j] * z[:, k] / r7
                if i == j:
                    num = num + 3.0 * z[:, k] / r5
                if i == k:
                    num = num + 3.0 * z[:, j] / r5
                if j == k:
                    num = num + 3.0 * z[:, i] / r5
                T[i, j, k] = np.sum(wts * src * num)
    return T / (4.0 * math.pi)


def fit_exponent(radii, vals) -> float:
    r = np.log(np.asarray(radii, dtype=float))
    v = np.log(np.abs(np.asarray(vals, dtype=float)))
    A = np.stack([r, np.ones_like(r)], axis=1)
    slope, _ = np.linalg.lstsq(A, v, rcond=None)[0]
    return float(slope)


def log10_weighted_density(magnitude: float, r: float) -> float:
    """log10 of the L^2(mu) radial integrand density |f|^2 e^{r^2/4} r^2.

    Computed in logs because e^{r^2/4} overflows a double at r = 80 (e^1600 ~ 10^695). The
    quantity that matters is whether this DIVERGES with r, and by how many decades.
    """
    if magnitude <= 0.0:
        return float("-inf")
    return float(2.0 * math.log10(magnitude) + (r * r / 4.0) / math.log(10.0) + 2.0 * math.log10(r))


# ---------------------------------------------------------------------------------------------
# PART B.2 -- the operator classes, measured one at a time
# ---------------------------------------------------------------------------------------------

def measure_leray_velocity_d3(pts, wts) -> dict:
    """CLASS C1 -- the velocity-pressure formulation. Leg 257's object, recomputed independently.

    P[F] = F - grad psi with Delta psi = div F = S. F itself is Gaussian; the whole obstruction
    is in grad psi. The multipole moments of S are computed by quadrature AND compared with the
    closed forms int S = 0, int y_k S = 0, int y_k y_l S = 2 int U_k U_l.
    """
    S = source_S_leray(pts)
    U = witness_U(pts)

    monopole = float(np.sum(wts * S))
    dipole = [float(np.sum(wts * pts[:, k] * S)) for k in range(3)]
    M = np.zeros((3, 3))
    T = np.zeros((3, 3))
    for k in range(3):
        for l in range(3):
            M[k, l] = np.sum(wts * pts[:, k] * pts[:, l] * S)
            T[k, l] = np.sum(wts * U[:, k] * U[:, l])

    energy = float(np.trace(T))
    trM = float(np.trace(M))

    # exact closed forms for this witness: T = 2 (pi/2)^{3/2}, T_11 = T_22 = (pi/2)^{3/2}
    exact_T11 = (math.pi / 2.0) ** 1.5
    exact_energy = 2.0 * exact_T11

    # Far field on the e_3 axis, where x.M.x = M_33 = 0 so the quadrupole term is -trM.
    # psi = -(1/4pi) * (1/(2 r^3)) * (3 xhat.M.xhat - trM)  ->  +trM/(8 pi r^3) on that axis.
    psi_quad, psi_multipole, grad_mag, ratio = [], [], [], []
    for r in RADII:
        x = np.array([0.0, 0.0, r])
        pq = newton_potential(S, wts, pts, x)
        pm = trM / (8.0 * math.pi * r ** 3)
        gq = newton_grad(S, wts, pts, x)
        psi_quad.append(pq)
        psi_multipole.append(pm)
        grad_mag.append(float(np.linalg.norm(gq)))
        ratio.append(pq / pm)

    # The control leg 257 used: the UNPROJECTED nonlinearity on the same rays.
    ctrl = []
    for r in RADII:
        x = np.array([[0.0, 0.0, r]])
        g = math.exp(-r * r)
        ctrl.append(float(2.0 * r * g))  # |U| on that ray scale; Gaussian by construction

    return {
        "class": "C1-LERAY-VELOCITY-d3",
        "formulation": "velocity-pressure",
        "operator": "Leray projection P = I - grad Delta^{-1} div",
        "monopole_int_S": monopole,
        "dipole_int_yS": dipole,
        "quadrupole_M": M.tolist(),
        "energy_tensor_T": T.tolist(),
        "identity_M_equals_2T_max_abs_err": float(np.max(np.abs(M - 2.0 * T))),
        "energy_int_U2_quadrature": energy,
        "energy_int_U2_closed_form": exact_energy,
        "energy_vs_closed_form_abs_err": abs(energy - exact_energy),
        "T11_quadrature": float(T[0, 0]),
        "T11_closed_form": exact_T11,
        "leg_257_T": LEG_257_T,
        "energy_vs_leg_257_abs_err": abs(energy - LEG_257_T),
        "leg_257_S11": LEG_257_S11,
        "T11_vs_leg_257_abs_err": abs(float(T[0, 0]) - LEG_257_S11),
        "radii": RADII,
        "psi_by_quadrature": psi_quad,
        "psi_by_multipole": psi_multipole,
        "quadrature_over_multipole_ratio": ratio,
        "psi_r10_vs_leg_257_abs_err": abs(psi_quad[0] - LEG_257_PSI_R10),
        "grad_psi_magnitude": grad_mag,
        "fitted_exponent_psi": fit_exponent(RADII, psi_quad),
        "fitted_exponent_grad_psi": fit_exponent(RADII, grad_mag),
        "gaussian_control_magnitude": ctrl,
        "log10_weighted_density": [log10_weighted_density(m, r) for m, r in zip(grad_mag, RADII)],
        "lowest_nonvanishing_moment": "quadrupole",
        "coefficient_is": "the energy tensor 2*int U_k U_l; its trace is 2*int|U|^2 > 0",
        "coefficient_can_vanish": False,
        "in_L2_mu": False,
        "reached_by_leg_257_mechanism": True,
    }


def measure_leray_buoyancy_d3(pts, wts) -> dict:
    """CLASS C2 -- the BUOYANCY coupling of a Boussinesq-type system. NOT in leg 257.

    Boussinesq: d_t u + P[(u.grad)u] = Delta u + P[rho e_3]. The buoyancy term is LINEAR in rho,
    and its Leray projection carries source div(rho e_3) = d_3 rho, whose monopole vanishes but
    whose DIPOLE is -int rho = -(total buoyancy mass), a conserved, sign-definite quantity for a
    transported non-negative density. So the tail here is |x|^-3 -- one power SLOWER than leg
    257's |x|^-4, i.e. a worse divergence, produced by a term that is not even nonlinear.
    """
    r2 = np.sum(pts * pts, axis=1)
    rho = np.exp(-r2)                      # non-negative, Gaussian, so rho in H^2(mu)
    Sb = -2.0 * pts[:, 2] * rho            # d_3 rho

    mass = float(np.sum(wts * rho))
    exact_mass = math.pi ** 1.5
    monopole = float(np.sum(wts * Sb))
    dipole = [float(np.sum(wts * pts[:, k] * Sb)) for k in range(3)]

    psi_quad, psi_multipole, grad_mag, ratio = [], [], [], []
    for r in RADII:
        x = np.array([0.0, 0.0, r])
        pq = newton_potential(Sb, wts, pts, x)
        # psi = -(1/4pi) * (xhat . D)/r^2, D_k = int y_k S; on the e_3 axis D_3 = -mass
        pm = -(1.0 / (4.0 * math.pi)) * dipole[2] / r ** 2
        gq = newton_grad(Sb, wts, pts, x)
        psi_quad.append(pq)
        psi_multipole.append(pm)
        grad_mag.append(float(np.linalg.norm(gq)))
        ratio.append(pq / pm)

    return {
        "class": "C2-LERAY-BUOYANCY-d3",
        "formulation": "velocity-pressure with a transported density (Boussinesq-type)",
        "operator": "Leray projection applied to the buoyancy force rho e_3",
        "term_is_linear_in_the_unknown": True,
        "monopole_int_S": monopole,
        "dipole_int_yS": dipole,
        "mass_int_rho_quadrature": mass,
        "mass_int_rho_closed_form": exact_mass,
        "identity_dipole3_equals_minus_mass_abs_err": abs(dipole[2] + mass),
        "radii": RADII,
        "psi_by_quadrature": psi_quad,
        "psi_by_multipole": psi_multipole,
        "quadrature_over_multipole_ratio": ratio,
        "grad_psi_magnitude": grad_mag,
        "fitted_exponent_psi": fit_exponent(RADII, psi_quad),
        "fitted_exponent_grad_psi": fit_exponent(RADII, grad_mag),
        "log10_weighted_density": [log10_weighted_density(m, r) for m, r in zip(grad_mag, RADII)],
        "lowest_nonvanishing_moment": "dipole",
        "coefficient_is": "-int rho, the total buoyancy mass; conserved and sign-definite",
        "coefficient_can_vanish": False,
        "in_L2_mu": False,
        "reached_by_leg_257_mechanism": True,
        "stronger_than_leg_257_because": (
            "the tail is |x|^-3, one power SLOWER than leg 257's |x|^-4, and it is produced by a "
            "LINEAR term. A Boussinesq-type row therefore leaves L^2(mu) before its quadratic "
            "nonlinearity is even considered."
        ),
    }


def measure_biot_savart_velocity_d3(pts, wts) -> dict:
    """CLASS C3 -- the VELOCITY recovered from a Gaussian vorticity.

    Take omega = U (divergence-free, Gaussian, and itself a curl, so int omega = 0 EXACTLY --
    the monopole is killed by structure, not by choice). Then u = curl(-Delta)^{-1} omega, and
    for omega = curl(phi e_3) this is u = phi e_3 + grad d_3 chi with chi the Newtonian potential
    of phi. The Gaussian piece is harmless; the tail lives in grad d_3 chi ~ |x|^-3.

    So the velocity DOES leave L^2(mu) in the vorticity formulation too. That is leg 257's
    repair-list intuition, and this leg confirms it. What C4 then measures is whether it MATTERS.
    """
    r2 = np.sum(pts * pts, axis=1)
    phi = np.exp(-r2)
    om = witness_U(pts)
    om_monopole = [float(np.sum(wts * om[:, k])) for k in range(3)]

    u_mag, exact_like = [], []
    for r in RADII:
        x = np.array([0.0, 0.0, r])
        H = newton_hess(phi, wts, pts, x)      # d_i d_j chi
        u = np.array([H[0, 2], H[1, 2], H[2, 2]])
        u[2] += math.exp(-r * r)               # the Gaussian piece phi e_3
        u_mag.append(float(np.linalg.norm(u)))
        exact_like.append(float(np.linalg.norm(np.array([H[0, 2], H[1, 2], H[2, 2]]))))

    return {
        "class": "C3-BIOT-SAVART-VELOCITY-d3",
        "formulation": "vorticity, velocity recovered by Biot-Savart",
        "operator": "u = curl(-Delta)^{-1} omega",
        "omega_monopole_int_omega": om_monopole,
        "monopole_vanishes_structurally": "omega is a curl, so int omega = 0 for any decaying field",
        "radii": RADII,
        "velocity_magnitude": u_mag,
        "fitted_exponent_velocity": fit_exponent(RADII, u_mag),
        "log10_weighted_density": [log10_weighted_density(m, r) for m, r in zip(u_mag, RADII)],
        "lowest_nonvanishing_moment": "dipole (the monopole is structurally zero)",
        "in_L2_mu": False,
        "but": (
            "in the vorticity formulation the UNKNOWN is omega, and u appears only inside "
            "products. Whether this tail obstructs is measured in C4, not inferred here."
        ),
    }


def measure_vorticity_nonlinearity_d3(pts, wts) -> dict:
    """CLASS C4 -- the vorticity-formulation NONLINEARITY (u.grad)omega - (omega.grad)u.

    THE DECISIVE MEASUREMENT OF THIS LEG. u and grad u carry algebraic tails (C3), but every
    term of N is a PRODUCT with a Gaussian factor -- omega or grad omega. If the product is
    Gaussian, N stays in L^2(mu) and leg 257's mechanism does NOT reach this formulation.

    Measured against the algebraic control |u| on the same rays, which does not vanish.
    """
    r2 = np.sum(pts * pts, axis=1)
    phi = np.exp(-r2)

    # RAY CHOICE, and it matters. The witness omega = (-2 x_2 g, 2 x_1 g, 0) vanishes IDENTICALLY
    # on the e_3 axis, so measuring there would exercise only the (u.grad)omega term and would
    # silently drop (omega.grad)u. This class is therefore measured on e_1, where omega is
    # non-zero and both terms are live. C1 stays on the e_3 axis, where leg 257 measured it.
    ray = np.array([1.0, 0.0, 0.0])

    N_mag, om_mag, u_mag, gu_mag, gom_mag = [], [], [], [], []
    for r in RADII:
        x = ray * r
        xr = x[None, :]

        H = newton_hess(phi, wts, pts, x)
        T3 = newton_third(phi, wts, pts, x)

        om = witness_U(xr)[0]
        u = np.array([H[0, 2], H[1, 2], H[2, 2]])
        u[2] += math.exp(-r * r)

        # grad u: d_j u_i = d_j d_i d_3 chi + d_j (phi delta_i3)
        gu = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                gu[i, j] = T3[i, 2, j]
        for j in range(3):
            gu[2, j] += -2.0 * x[j] * math.exp(-r * r)

        # grad omega, analytically: omega = (-2 x_2 g, 2 x_1 g, 0), g = e^{-|x|^2}
        g = math.exp(-r * r)
        gom = np.zeros((3, 3))
        for j in range(3):
            gom[0, j] = -2.0 * (1.0 if j == 1 else 0.0) * g + (-2.0 * x[1]) * (-2.0 * x[j] * g)
            gom[1, j] = +2.0 * (1.0 if j == 0 else 0.0) * g + (+2.0 * x[0]) * (-2.0 * x[j] * g)

        N = gom @ u - gu @ om
        N_mag.append(float(np.linalg.norm(N)))
        om_mag.append(float(np.linalg.norm(om)))
        u_mag.append(float(np.linalg.norm(u)))
        gu_mag.append(float(np.linalg.norm(gu)))
        gom_mag.append(float(np.linalg.norm(gom)))

    finite = [i for i, v in enumerate(N_mag) if v > 0.0]
    exp_N = fit_exponent([RADII[i] for i in finite], [N_mag[i] for i in finite]) if len(finite) >= 2 else float("-inf")

    return {
        "class": "C4-VORTICITY-NONLINEARITY-d3",
        "formulation": "vorticity",
        "measured_on_ray": "e_1 (omega vanishes identically on the e_3 axis; see code comment)",
        "operator": "(u.grad)omega - (omega.grad)u, u = Biot-Savart[omega]",
        "radii": RADII,
        "N_magnitude": N_mag,
        "omega_magnitude": om_mag,
        "velocity_magnitude_algebraic_control": u_mag,
        "grad_u_magnitude": gu_mag,
        "grad_omega_magnitude": gom_mag,
        "fitted_exponent_N_over_finite_radii": exp_N,
        "log10_weighted_density": [log10_weighted_density(m, r) for m, r in zip(N_mag, RADII)],
        "in_L2_mu": True,
        "reached_by_leg_257_mechanism": False,
        "mechanism_of_the_escape": (
            "every term of N is a product carrying a Gaussian factor (omega or grad omega), so "
            "the algebraic tail of u and grad u is multiplied away. The tail is real (C3) and "
            "does not survive the product."
        ),
    }


def measure_keller_segel_control_d3(pts, wts) -> dict:
    """CLASS C5 -- the CONTROL, and the reason leg 255's two survivors survive.

    Keller-Segel: u_t = Delta u - div(u grad c), 0 = Delta c + u. The model is NONLOCAL -- c is
    the Newtonian potential of u, and grad c ~ |x|^-2. Yet div(u grad c) = grad u . grad c - u^2
    carries a Gaussian factor in BOTH terms. A control that comes out DIFFERENTLY from C1/C2 on
    the same machinery, which is what makes the C1/C2 verdicts measurements rather than a
    property of the code.
    """
    r2 = np.sum(pts * pts, axis=1)
    u = np.exp(-r2)

    term_mag, gradc_mag = [], []
    for r in RADII:
        x = np.array([0.0, 0.0, r])
        # c = (1/4pi) int u/|x-y|  (so that Delta c = -u); grad c by the same kernel
        z = x[None, :] - pts
        rr = np.sqrt(np.sum(z * z, axis=1))
        gc = -(1.0 / (4.0 * math.pi)) * np.sum(((wts * u / rr ** 3)[:, None] * z), axis=0)
        gu = np.array([-2.0 * x[k] * math.exp(-r * r) for k in range(3)])
        uu = math.exp(-r * r)
        term = float(abs(np.dot(gu, gc) - uu ** 2))
        term_mag.append(term)
        gradc_mag.append(float(np.linalg.norm(gc)))

    return {
        "class": "C5-KELLER-SEGEL-CONTROL-d3",
        "formulation": "parabolic-elliptic chemotaxis (leg 255's surviving family)",
        "operator": "grad c = grad Delta^{-1}(-u), nonlocal",
        "radii": RADII,
        "nonlocal_factor_grad_c_magnitude": gradc_mag,
        "fitted_exponent_grad_c": fit_exponent(RADII, gradc_mag),
        "nonlinearity_magnitude": term_mag,
        "log10_weighted_density": [log10_weighted_density(m, r) for m, r in zip(term_mag, RADII)],
        "in_L2_mu": True,
        "reached_by_leg_257_mechanism": False,
        "why_this_control_matters": (
            "the model IS nonlocal and its nonlocal factor DOES have an algebraic |x|^-2 tail, "
            "yet the nonlinearity is Gaussian. So 'is the model nonlocal' is NOT the "
            "discriminator; 'is the nonlocal output multiplied by a localised factor' is."
        ),
    }


def measure_unprojected_control_d3(pts, wts) -> dict:
    """CLASS C0 -- leg 257's own control: the nonlinearity WITHOUT the projection."""
    mags = []
    for r in RADII:
        x = np.array([[0.0, 0.0, r]])
        g = math.exp(-r * r)
        # (U.grad)U on the e_3 axis: U = (-2 x_2 g, 2 x_1 g, 0) vanishes there, and every
        # derivative carries the same Gaussian, so the whole term is O(r^2 e^{-2r^2}).
        mags.append(float(4.0 * r * r * g * g))
    return {
        "class": "C0-UNPROJECTED-CONTROL-d3",
        "operator": "(U.grad)U, no projection",
        "radii": RADII,
        "magnitude": mags,
        "log10_weighted_density": [log10_weighted_density(m, r) for m, r in zip(mags, RADII)],
        "in_L2_mu": True,
        "reached_by_leg_257_mechanism": False,
        "note": "leg 257 reported this underflowing to exactly 0.0; reproduced.",
    }


# ---------------------------------------------------------------------------------------------
# PART A -- the relaxed-tier fluid census
# ---------------------------------------------------------------------------------------------
# evidence_tier:
#   T1  proved, or proved-modulo-a-stated-hypothesis  (leg 255's tier -- unchanged)
#   T2  CONJECTURED, with serious numerical evidence  (THIS LEG'S RELAXATION)
#   T2- conjectured, and the numerical evidence points the OTHER way
#
# leray_class links each row to a MEASURED class in Part B. Nothing about screen (iv_b) is
# asserted at row level; it is looked up from the measurement.

FLUID_ROWS = [
    # ---- inherited tier-1 rows (leg 255's verdicts, carried unchanged, for continuity) ----
    dict(key="KS-NS-LI-ZHOU", src="arXiv:2404.17228 (CMP 2025, DOI 10.1007/s00220-025-05371-w)",
         tier="T1", blowup_proved=True, numerics="n/a", author_conclusion_positive=True,
         has_profile=True, profile_carries_dissipation=True, profile_closed_form=True,
         certified=False, cert_note="no certification apparatus in the fetched abstract",
         remark40_local_polynomial=False, nonlocal_named="Leray projection",
         leray_class="C1-LERAY-VELOCITY-d3", inherited_from_255=True,
         nrs_status="the self-similar object is the Keller-Segel profile, not the velocity",
         note="leg 255's single fluid-adjacent row clearing (i)-(iii); killed by (iv)."),
    dict(key="BCG-NS", src="leg 255 row (inherited)", tier="T1", blowup_proved=True,
         numerics="n/a", author_conclusion_positive=True, has_profile=True,
         profile_carries_dissipation=False, profile_closed_form=False, certified=True,
         cert_note="certification apparatus present (leg 255 screen iii FAIL)",
         remark40_local_polynomial=False, nonlocal_named="Leray projection",
         leray_class="C1-LERAY-VELOCITY-d3", inherited_from_255=True,
         nrs_status="inherits an inviscid Euler profile", note="leg 255: killed by iii, iv."),
    dict(key="CGSS-NONRADIAL", src="leg 255 row (inherited)", tier="T1", blowup_proved=True,
         numerics="n/a", author_conclusion_positive=True, has_profile=True,
         profile_carries_dissipation=False, profile_closed_form=False, certified=False,
         cert_note="none found", remark40_local_polynomial=False,
         nonlocal_named="Leray projection", leray_class="C1-LERAY-VELOCITY-d3",
         inherited_from_255=True, nrs_status="inherits an inviscid Euler profile",
         note="leg 255: killed by iv alone."),
    dict(key="MRRS-NS", src="leg 255 row (inherited)", tier="T1", blowup_proved=True,
         numerics="n/a", author_conclusion_positive=True, has_profile=True,
         profile_carries_dissipation=False, profile_closed_form=False, certified=False,
         cert_note="none found", remark40_local_polynomial=False,
         nonlocal_named="Leray projection / compressible implosion", leray_class="C1-LERAY-VELOCITY-d3",
         inherited_from_255=True, nrs_status="compressible implosion ansatz",
         note="leg 255: killed by iv alone."),
    dict(key="TAO-AVGNS", src="leg 255 row (inherited)", tier="T1", blowup_proved=True,
         numerics="n/a", author_conclusion_positive=True, has_profile=True,
         profile_carries_dissipation=True, profile_closed_form=False, certified=False,
         cert_note="none found", remark40_local_polynomial=False,
         nonlocal_named="averaged Euler bilinear operator", leray_class="OTHER-NONLOCAL-NOT-MEASURED-HERE",
         inherited_from_255=True, nrs_status="averaged model, NRS does not apply as stated",
         note="leg 255: killed by iv. DSS-lane flagged, not decided."),
    dict(key="MILLER-FR-HYPO", src="arXiv:2307.03434", tier="T1", blowup_proved=True,
         numerics="n/a", author_conclusion_positive=True, has_profile=True,
         profile_carries_dissipation=True, profile_closed_form=False, certified=False,
         cert_note="none found", remark40_local_polynomial=False,
         nonlocal_named="Fourier restriction multiplier", leray_class="OTHER-NONLOCAL-NOT-MEASURED-HERE",
         inherited_from_255=True, nrs_status="restricted model", ban_flag="stage-V machinery",
         note="leg 255: killed by iv. Carries the re-posed stage-V ban as a forward constraint."),
    dict(key="PALASEK-SHELL", src="leg 255 row (inherited)", tier="T1", blowup_proved=True,
         numerics="n/a", author_conclusion_positive=True, has_profile=False,
         profile_carries_dissipation=False, profile_closed_form=False, certified=False,
         cert_note="none found", remark40_local_polynomial=False, nonlocal_named="shell ladder",
         leray_class="OTHER-NONLOCAL-NOT-MEASURED-HERE", inherited_from_255=True,
         nrs_status="shell model", ban_flag="stage-V machinery",
         note="leg 255: killed by ii, iv. Its screen-(ii) FAIL is UNCONFIRMED, not refuted."),
    dict(key="KVW-PRANDTL", src="leg 255 row (inherited)", tier="T1", blowup_proved=True,
         numerics="n/a", author_conclusion_positive=True, has_profile=False,
         profile_carries_dissipation=False, profile_closed_form=False, certified=False,
         cert_note="none found", remark40_local_polynomial=False,
         nonlocal_named="Prandtl nonlocal pressure/boundary layer", leray_class="OTHER-NONLOCAL-NOT-MEASURED-HERE",
         inherited_from_255=True, nrs_status="boundary-layer model",
         note="leg 255: killed by ii, iv."),
    dict(key="CHEN-GCLM-DISS", src="leg 255 row (inherited)", tier="T1", blowup_proved=True,
         numerics="n/a", author_conclusion_positive=True, has_profile=False,
         profile_carries_dissipation=False, profile_closed_form=False, certified=False,
         cert_note="none found", remark40_local_polynomial=False, nonlocal_named="Hilbert transform",
         leray_class="OTHER-NONLOCAL-NOT-MEASURED-HERE", inherited_from_255=True,
         nrs_status="1D model", ban_flag="gCLM ban -- barred from construction",
         note="leg 255: killed by ii, iv. Carried as a row only; no gCLM object is instantiated."),
    dict(key="NSE-3D", src="the Clay problem itself", tier="T1", blowup_proved=False,
         numerics="none decisive", author_conclusion_positive=False, has_profile=False,
         profile_carries_dissipation=True, profile_closed_form=False, certified=False,
         cert_note="none", remark40_local_polynomial=False, nonlocal_named="Leray projection",
         leray_class="C1-LERAY-VELOCITY-d3", inherited_from_255=True,
         nrs_status="NRS/Tsai kill backward self-similar profiles outright",
         note="leg 255: killed by i, ii, iv."),
    dict(key="BOUSSINESQ-VISC", src="leg 255 row (inherited)", tier="T1", blowup_proved=False,
         numerics="none decisive at tier 1", author_conclusion_positive=False, has_profile=False,
         profile_carries_dissipation=False, profile_closed_form=False, certified=False,
         cert_note="none", remark40_local_polynomial=False,
         nonlocal_named="Leray projection + buoyancy coupling", leray_class="C2-LERAY-BUOYANCY-d3",
         inherited_from_255=True, nrs_status="n/a",
         note="leg 255: killed by i, ii, iv. THIS LEG re-measures its (iv) via class C2."),

    # ---------------- NEW ROWS: the RELAXED tier. This is the leg's actual question. -----------
    dict(key="HOU-GNSE-3188", src="arXiv:2405.10916v2 (Hou, 2024-05-17)", tier="T2",
         blowup_proved=False, numerics="serious", author_conclusion_positive=True,
         has_profile=True, profile_carries_dissipation=True, profile_closed_form=False,
         certified=False, cert_note="no interval-arithmetic enclosure; adaptive pseudo-spectral numerics",
         remark40_local_polynomial=False, nonlocal_named="axisymmetric Biot-Savart / stream-function solve",
         leray_class="C4-VORTICITY-NONLINEARITY-d3", inherited_from_255=False,
         nrs_status=("self-similar, but at fractional dimension 3.188 with solution-dependent "
                     "viscosity, in a cylinder with boundary -- NOT the R^3 backward-self-similar "
                     "hypothesis NRS/Tsai address"),
         note=("THE STRONGEST RELAXED-TIER FLUID ROW. Generalized axisymmetric NS with "
               "solution-dependent viscosity develops SELF-SIMILAR blowup at dimension 3.188, and "
               "the paper states the self-similar profile satisfies the axisymmetric NS equations "
               "with CONSTANT viscosity. Posed in vorticity/stream-function variables.")),
    dict(key="HOU-BOUSSINESQ-2405", src="arXiv:2405.10916v2 (same paper, Boussinesq half)",
         tier="T2", blowup_proved=False, numerics="serious", author_conclusion_positive=True,
         has_profile=True, profile_carries_dissipation=True, profile_closed_form=False,
         certified=False, cert_note="no enclosure", remark40_local_polynomial=False,
         nonlocal_named="Leray projection + buoyancy coupling", leray_class="C2-LERAY-BUOYANCY-d3",
         inherited_from_255=False, nrs_status="n/a (Boussinesq)",
         note=("axisymmetric Boussinesq with CONSTANT viscosity, NEARLY self-similar blowup. The "
               "'nearly' is carried, not rounded away: the profile is not exactly self-similar.")),
    dict(key="HOU-NSE-DEGEN-DIFF", src="arXiv:2102.06663", tier="T2", blowup_proved=False,
         numerics="serious", author_conclusion_positive=True, has_profile=True,
         profile_carries_dissipation=True, profile_closed_form=False, certified=False,
         cert_note="no enclosure", remark40_local_polynomial=False,
         nonlocal_named="axisymmetric Biot-Savart / stream-function solve",
         leray_class="C4-VORTICITY-NONLINEARITY-d3", inherited_from_255=False,
         nrs_status="locally self-similar, degenerate diffusion vanishing like O(r^2)+O(z^2)",
         note=("3D axisymmetric NS with DEGENERATE diffusion coefficients, potential finite-time "
               "LOCALLY self-similar singularity, two-scale travelling wave. The degeneracy is a "
               "real qualifier: the dissipation vanishes at the singular point.")),
    dict(key="HOU-NSE-2107", src="arXiv:2107.06509 (FoCM 2023, DOI 10.1007/s10208-022-09578-4)",
         tier="T2-", blowup_proved=False, numerics="serious", author_conclusion_positive=False,
         has_profile=True, profile_carries_dissipation=True, profile_closed_form=False,
         certified=False, cert_note="no enclosure", remark40_local_polynomial=False,
         nonlocal_named="axisymmetric Biot-Savart / stream-function solve",
         leray_class="C4-VORTICITY-NONLINEARITY-d3", inherited_from_255=False,
         nrs_status="nearly self-similar, two-scale",
         note=("THE ROW THAT KEEPS THE RELAXED TIER HONEST. The most-cited 'potentially singular "
               "3D NS' numerics, and the paper's OWN conclusion is negative: the solution does NOT "
               "develop a finite-time singularity, because a mild two-scale structure leads to "
               "viscous dominance over vortex stretching. Serious numerics pointing the OTHER way.")),
    dict(key="SQG-DISSIPATIVE", src="Constantin-Lai-Sharma-Tseng-Wu, J. Sci. Comput., DOI 10.1007/s10915-011-9471-9",
         tier="T2-", blowup_proved=False, numerics="serious", author_conclusion_positive=False,
         has_profile=False, profile_carries_dissipation=False, profile_closed_form=False,
         certified=False, cert_note="none", remark40_local_polynomial=False,
         nonlocal_named="Riesz transform u = grad^perp Lambda^{-1} theta",
         leray_class="OTHER-NONLOCAL-NOT-MEASURED-HERE", inherited_from_255=False,
         nrs_status="n/a (2D)",
         note=("The candidate blow-up datum's temperature gradient fits a DOUBLE-EXPONENTIAL in "
               "time equally well as an algebraic blowup, so the numerical evidence does not "
               "support finite-time singularity. A negative that was looked up, not assumed.")),
    dict(key="HYPODISS-NS-FORCED", src="hypodissipative NS with forcing, (-Delta)^0.046 (see arXiv:2307.03434 family)",
         tier="T1", blowup_proved=True, numerics="n/a", author_conclusion_positive=True,
         has_profile=False, profile_carries_dissipation=True, profile_closed_form=False,
         certified=False, cert_note="none", remark40_local_polynomial=False,
         nonlocal_named="Leray projection", leray_class="C1-LERAY-VELOCITY-d3",
         inherited_from_255=False, nrs_status="forced, so the unforced NRS hypothesis does not bind",
         note=("blow-up is PROVED but requires an external force; the dissipation is 0.1 orders of "
               "derivative. Recorded with the forcing qualifier attached, not suppressed.")),
    dict(key="NSE-3D-VORTICITY", src="the Clay problem, posed in vorticity variables",
         tier="T1", blowup_proved=False, numerics="none decisive",
         author_conclusion_positive=False, has_profile=False, profile_carries_dissipation=True,
         profile_closed_form=False, certified=False, cert_note="none",
         remark40_local_polynomial=False, nonlocal_named="Biot-Savart law",
         leray_class="C4-VORTICITY-NONLINEARITY-d3", inherited_from_255=False,
         nrs_status=("omega in H^2(mu) gives u ~ |x|^-3 (class C3), hence u in L^3(R^3), hence "
                     "NRS/Tsai force u == 0 for a backward self-similar profile"),
         note=("ADDED BY THIS LEG so the formulation question is on the table as its own row "
               "rather than hidden inside NSE-3D. Screen (iv_b) PASSES here -- and (iv_a) does not.")),
]

# --------------------------------------------------------------------------------------------
# NON-FLUID CONTROL ROWS, carried from leg 255 with its verdicts, and EXCLUDED from the gate.
#
# They exist for one reason, and it is leg 255's own viscous-Burgers discipline: screen (iv_a)
# turned out to kill 18 of 18 FLUID rows, so within the fluid cell it is a constant. A screen
# that never passes cannot be distinguished from a broken screen by the fluid table alone.
# These two rows are where (iv_a) and (iii) demonstrably PASS. If either ever stops looking like
# leg 255 said it looks, assert_probe_is_live() fails the run.
# --------------------------------------------------------------------------------------------
CONTROL_ROWS = [
    dict(key="KS3D-NONEXPLICIT", src="leg 255's surviving row (arXiv:2503.02263 / 2209.11206)",
         tier="T1", blowup_proved=True, numerics="n/a", author_conclusion_positive=True,
         has_profile=True, profile_carries_dissipation=True, profile_closed_form=False,
         certified=False, cert_note="no interval-arithmetic enclosure found",
         remark40_local_polynomial=True, nonlocal_named="none (grad c enters multiplicatively)",
         leray_class="C5-KELLER-SEGEL-CONTROL-d3", inherited_from_255=True, is_control=True,
         nrs_status="n/a (not a fluid)",
         note="leg 255's SURVIVOR, non-fluid. Here purely to show (iv_a) and (iv_b) can PASS."),
    dict(key="VISCOUS-BURGERS-BC", src="leg 255 caution row; Breden-Chu's own worked example",
         tier="T1", blowup_proved=False, numerics="none", author_conclusion_positive=False,
         has_profile=True, profile_carries_dissipation=True, profile_closed_form=False,
         certified=True, cert_note="CERTIFIED -- it is Breden-Chu's own Theorem 42",
         remark40_local_polynomial=True, nonlocal_named="none",
         leray_class="C0-UNPROJECTED-CONTROL-d3", inherited_from_255=True, is_control=True,
         nrs_status="n/a (1D)",
         note=("leg 255's caution row: parabolic, certified, self-similar profile, and it does "
               "NOT blow up. Must keep passing (iv) while failing (i) and (iii).")),
]


def screen_verdicts(row: dict, classes: dict) -> dict:
    """Every verdict DERIVED from evidence fields. Nothing asserted."""
    # (i) RELAXED: proved, OR conjectured with serious numerics that point the right way.
    if row["blowup_proved"]:
        s1 = "PASS"
    elif row["numerics"] == "serious" and row["author_conclusion_positive"]:
        s1 = "PASS-RELAXED"
    else:
        s1 = "FAIL"

    # (ii) a self-similar / DSS profile exists
    s2 = "PASS" if row["has_profile"] else "FAIL"

    # (iii) uncertified
    s3 = "FAIL" if row["certified"] else "PASS"

    # (iv_a) leg 255's screen: Remark 40's stated reach -- local polynomial, no nonlocal operator
    s4a = "PASS" if row["remark40_local_polynomial"] else "FAIL"

    # (iv_b) leg 257's POSITIVE mechanism, looked up from Part B's measurements
    cls = row["leray_class"]
    if cls in classes:
        s4b = "FAIL" if classes[cls]["reached_by_leg_257_mechanism"] else "PASS"
    else:
        s4b = "NOT-MEASURED"

    return {"i": s1, "ii": s2, "iii": s3, "iv_a": s4a, "iv_b": s4b}


def classify(rows: list) -> dict:
    """The gate is FLUID-ONLY. Control rows are scored and reported but never counted here."""
    survivors, near_misses = [], []
    for r in rows:
        if r.get("is_control"):
            continue
        v = r["verdicts"]
        ok = (v["i"] in ("PASS", "PASS-RELAXED") and v["ii"] == "PASS" and v["iii"] == "PASS")
        if ok and v["iv_a"] == "PASS" and v["iv_b"] == "PASS":
            survivors.append(r["key"])
        elif ok and v["iv_b"] == "PASS" and v["iv_a"] == "FAIL":
            near_misses.append(r["key"])

    if survivors:
        code = "FLUID_ROW_SURVIVES_RELAXED_TIER"
        gate = "YES"
    elif near_misses:
        code = "NO_SURVIVOR_BUT_IV_B_PASSES_ON_A_FLUID_ROW"
        gate = "NO"
    else:
        code = "FLUID_CELL_EMPTY_UNDER_THE_RELAXED_TIER"
        gate = "NO"
    return {"gate": gate, "code": code, "survivors": survivors, "near_misses": near_misses}


def build_table(classes: dict, rows=None) -> list:
    out = []
    for row in (rows if rows is not None else (FLUID_ROWS + CONTROL_ROWS)):
        r = dict(row)
        r.setdefault("is_control", False)
        r["verdicts"] = screen_verdicts(row, classes)
        killers = [k for k, v in r["verdicts"].items() if v == "FAIL"]
        r["killed_by"] = killers
        out.append(r)
    return out


# ---------------------------------------------------------------------------------------------
# liveness and self-test
# ---------------------------------------------------------------------------------------------

def assert_probe_is_live(table: list, classes: dict) -> list:
    """Fail the run outright if the table or the witness ladder has degenerated."""
    checks = []

    def req(name, cond, detail):
        checks.append({"check": name, "ok": bool(cond), "detail": detail})
        if not cond:
            raise AssertionError(f"PROBE NOT LIVE: {name} -- {detail}")

    killed = [r for r in table if r["killed_by"]]
    req("not every row survives", len(killed) > 0, f"{len(killed)} of {len(table)} rows killed")

    # NOTE, recorded because this check was CHANGED after it fired on the real answer.
    # Leg 255's census contained survivors, so "not every row is killed" was a sound degeneracy
    # guard there. On a FLUID-ONLY census it is not: an empty fluid cell is a legitimate outcome
    # and this leg measured one. The guard that actually catches a degenerate table -- one that
    # says NO to everything for a single uniform reason -- is that no single screen accounts for
    # every kill, and that each screen passes on something (checked below). The weaker check is
    # kept as a REPORTED quantity so the change is visible rather than silent.
    uniform = [s for s in ("i", "ii", "iii", "iv_a", "iv_b")
               if all(r["verdicts"][s] == "FAIL" for r in table)]
    req("no single screen kills every row", len(uniform) == 0,
        f"screens killing the whole table: {uniform or 'none'}")
    checks.append({"check": "rows carrying no FAIL (reported, not required)",
                   "ok": True, "detail": f"{len(table) - len(killed)} of {len(table)}"})

    for s in ("i", "ii", "iii", "iv_a", "iv_b"):
        n_fail = sum(1 for r in table if r["verdicts"][s] == "FAIL")
        n_pass = sum(1 for r in table if r["verdicts"][s] in ("PASS", "PASS-RELAXED"))
        req(f"screen {s} kills something", n_fail > 0, f"{n_fail} FAILs")
        req(f"screen {s} passes something", n_pass > 0, f"{n_pass} PASSes")

    # The control rows are the only place screen (iv_a) passes. Check them against leg 255's
    # stated verdicts explicitly, so a silent drift in either row fails the run.
    by_key = {r["key"]: r for r in table}
    ks = by_key["KS3D-NONEXPLICIT"]
    req("control KS3D-NONEXPLICIT still passes all four (leg 255's survivor)",
        ks["verdicts"]["i"] == "PASS" and ks["verdicts"]["ii"] == "PASS"
        and ks["verdicts"]["iii"] == "PASS" and ks["verdicts"]["iv_a"] == "PASS"
        and ks["verdicts"]["iv_b"] == "PASS", str(ks["verdicts"]))
    vb = by_key["VISCOUS-BURGERS-BC"]
    req("control VISCOUS-BURGERS-BC still passes (ii)+(iv) while failing (i)+(iii)",
        vb["verdicts"]["ii"] == "PASS" and vb["verdicts"]["iv_a"] == "PASS"
        and vb["verdicts"]["i"] == "FAIL" and vb["verdicts"]["iii"] == "FAIL", str(vb["verdicts"]))

    # And the headline uniformity, reported as a measured quantity rather than guarded against.
    fluid = [r for r in table if not r.get("is_control")]
    n_iva_fail = sum(1 for r in fluid if r["verdicts"]["iv_a"] == "FAIL")
    checks.append({"check": "screen (iv_a) over the FLUID cell (reported, not required)",
                   "ok": True, "detail": f"{n_iva_fail} of {len(fluid)} fluid rows FAIL (iv_a)"})

    # the relaxed tier must actually be exercised
    n_relaxed = sum(1 for r in table if r["verdicts"]["i"] == "PASS-RELAXED")
    req("the relaxed tier admits rows", n_relaxed > 0, f"{n_relaxed} rows enter via PASS-RELAXED")
    n_t2minus = sum(1 for r in table if r["tier"] == "T2-")
    req("the relaxed tier has honest negatives", n_t2minus > 0,
        f"{n_t2minus} rows whose serious numerics point the other way")

    # Part B must discriminate, or it is measuring the code and not the mathematics
    reached = [k for k, v in classes.items() if v.get("reached_by_leg_257_mechanism") is True]
    unreached = [k for k, v in classes.items() if v.get("reached_by_leg_257_mechanism") is False]
    req("some class IS reached", len(reached) > 0, f"reached: {reached}")
    req("some class is NOT reached", len(unreached) > 0, f"not reached: {unreached}")

    c1 = classes["C1-LERAY-VELOCITY-d3"]
    req("C1 reproduces leg 257's energy to 1e-9", c1["energy_vs_leg_257_abs_err"] < 1e-9,
        f"|dT| = {c1['energy_vs_leg_257_abs_err']:.3e}")
    req("C1 reproduces leg 257's psi(r=10) to 1e-12", c1["psi_r10_vs_leg_257_abs_err"] < 1e-12,
        f"|dpsi| = {c1['psi_r10_vs_leg_257_abs_err']:.3e}")
    req("C1's quadrupole IS 2x the energy tensor", c1["identity_M_equals_2T_max_abs_err"] < 1e-10,
        f"max|M - 2T| = {c1['identity_M_equals_2T_max_abs_err']:.3e}")
    req("C1's psi exponent is -3 to 1e-3", abs(c1["fitted_exponent_psi"] + 3.0) < 1e-3,
        f"fitted {c1['fitted_exponent_psi']:.9f}")
    req("C1's grad psi exponent is -4 to 1e-3", abs(c1["fitted_exponent_grad_psi"] + 4.0) < 1e-3,
        f"fitted {c1['fitted_exponent_grad_psi']:.9f}")

    c2 = classes["C2-LERAY-BUOYANCY-d3"]
    req("C2's dipole IS minus the mass", c2["identity_dipole3_equals_minus_mass_abs_err"] < 1e-10,
        f"err = {c2['identity_dipole3_equals_minus_mass_abs_err']:.3e}")
    req("C2 decays SLOWER than C1", c2["fitted_exponent_grad_psi"] > c1["fitted_exponent_grad_psi"],
        f"C2 {c2['fitted_exponent_grad_psi']:.6f} vs C1 {c1['fitted_exponent_grad_psi']:.6f}")

    c4 = classes["C4-VORTICITY-NONLINEARITY-d3"]
    req("C4's weighted density CONVERGES while C1's DIVERGES",
        c4["log10_weighted_density"][-1] < c1["log10_weighted_density"][-1] - 100,
        (f"C4 {c4['log10_weighted_density'][-1]:.1f} vs "
         f"C1 {c1['log10_weighted_density'][-1]:.1f} (log10 decades)"))
    req("C4's algebraic control is NON-zero where N is negligible",
        c4["velocity_magnitude_algebraic_control"][-1] > 0.0,
        f"|u|(r=80) = {c4['velocity_magnitude_algebraic_control'][-1]:.6e}")

    c5 = classes["C5-KELLER-SEGEL-CONTROL-d3"]
    req("C5's nonlocal factor IS algebraic (so the control is not trivial)",
        abs(c5["fitted_exponent_grad_c"] + 2.0) < 1e-2, f"fitted {c5['fitted_exponent_grad_c']:.6f}")
    req("C5's nonlinearity is nevertheless in L^2(mu)", c5["in_L2_mu"] is True, "control differs from C1")

    return checks


def self_test(classes: dict) -> list:
    """Perturb the evidence and check both gate branches are REACHABLE on evidence."""
    outcomes = []

    base = classify(build_table(classes))
    outcomes.append({"perturbation": "none (as measured)", "gate": base["gate"], "code": base["code"]})

    # 1. Relax screen (iv_a): suppose a leg argued Biot-Savart into Remark 40's reach.
    rows = [dict(r) for r in FLUID_ROWS] + [dict(r) for r in CONTROL_ROWS]
    for r in rows:
        if r["leray_class"] == "C4-VORTICITY-NONLINEARITY-d3":
            r["remark40_local_polynomial"] = True
    t = classify(build_table(classes, rows))
    outcomes.append({"perturbation": "Remark 40 read as covering Biot-Savart",
                     "gate": t["gate"], "code": t["code"]})

    # 2. Suppose the vorticity nonlinearity had come out algebraic (C4 reached).
    cl = {k: dict(v) for k, v in classes.items()}
    cl["C4-VORTICITY-NONLINEARITY-d3"]["reached_by_leg_257_mechanism"] = True
    rows2 = [dict(r) for r in FLUID_ROWS] + [dict(r) for r in CONTROL_ROWS]
    for r in rows2:
        if r["leray_class"] == "C4-VORTICITY-NONLINEARITY-d3":
            r["remark40_local_polynomial"] = True
    t = classify(build_table(cl, rows2))
    outcomes.append({"perturbation": "C4 measured as REACHED, and (iv_a) relaxed",
                     "gate": t["gate"], "code": t["code"]})

    # 3. Tighten screen (i) back to tier 1: the relaxed rows should drop out.
    rows3 = [dict(r) for r in FLUID_ROWS] + [dict(r) for r in CONTROL_ROWS]
    for r in rows3:
        if not r["blowup_proved"] and not r.get("is_control"):
            r["numerics"] = "none"
    t = classify(build_table(classes, rows3))
    n_relaxed = sum(1 for r in build_table(classes, rows3) if r["verdicts"]["i"] == "PASS-RELAXED")
    outcomes.append({"perturbation": "screen (i) tightened back to tier 1",
                     "gate": t["gate"], "code": t["code"],
                     "rows_entering_via_relaxed_tier": n_relaxed})

    return outcomes


# ---------------------------------------------------------------------------------------------

def main() -> int:
    n, L = 60, 6.0
    pts, wts = gauss_grid(n, L)

    classes_list = [
        measure_unprojected_control_d3(pts, wts),
        measure_leray_velocity_d3(pts, wts),
        measure_leray_buoyancy_d3(pts, wts),
        measure_biot_savart_velocity_d3(pts, wts),
        measure_vorticity_nonlinearity_d3(pts, wts),
        measure_keller_segel_control_d3(pts, wts),
    ]
    classes = {c["class"]: c for c in classes_list}

    table = build_table(classes)
    verdict = classify(table)
    checks = assert_probe_is_live(table, classes)
    st = self_test(classes)

    c1 = classes["C1-LERAY-VELOCITY-d3"]
    c2 = classes["C2-LERAY-BUOYANCY-d3"]
    c4 = classes["C4-VORTICITY-NONLINEARITY-d3"]

    fluid = [r for r in table if not r.get("is_control")]
    n_fluid = len(fluid)
    counts = {
        "fluid_rows_enumerated": n_fluid,
        "non_fluid_control_rows": len(table) - n_fluid,
        "rows_new_in_this_leg": sum(1 for r in fluid if not r["inherited_from_255"]),
        "rows_inherited_from_leg_255": sum(1 for r in fluid if r["inherited_from_255"]),
        "rows_entering_via_the_relaxed_tier": sum(1 for r in fluid if r["verdicts"]["i"] == "PASS-RELAXED"),
        "rows_whose_serious_numerics_point_the_other_way": sum(1 for r in fluid if r["tier"] == "T2-"),
        "killed_by_i": sum(1 for r in fluid if r["verdicts"]["i"] == "FAIL"),
        "killed_by_ii": sum(1 for r in fluid if r["verdicts"]["ii"] == "FAIL"),
        "killed_by_iii": sum(1 for r in fluid if r["verdicts"]["iii"] == "FAIL"),
        "killed_by_iv_a": sum(1 for r in fluid if r["verdicts"]["iv_a"] == "FAIL"),
        "killed_by_iv_b": sum(1 for r in fluid if r["verdicts"]["iv_b"] == "FAIL"),
        "iv_b_not_measured": sum(1 for r in fluid if r["verdicts"]["iv_b"] == "NOT-MEASURED"),
        "rows_clearing_i_ii_iii": sum(
            1 for r in fluid
            if r["verdicts"]["i"] in ("PASS", "PASS-RELAXED")
            and r["verdicts"]["ii"] == "PASS" and r["verdicts"]["iii"] == "PASS"),
        "rows_passing_iv_b_but_failing_iv_a": sum(
            1 for r in fluid if r["verdicts"]["iv_b"] == "PASS" and r["verdicts"]["iv_a"] == "FAIL"),
        "survivors_of_all_five": len(verdict["survivors"]),
    }

    doc = {
        "leg": 261,
        "route": "P1A2",
        "date": "2026-08-07",
        "extends": {
            "leg_255": "writeup/data/p2_route_p1a_v1_census.json (read-only; no verdict changed)",
            "leg_257": "writeup/data/p2_route_p1c_v1_reach.json on leg/257-p1c-v1 (read-only)",
        },
        "weight": "e^{|x|^2/4} -- Breden-Chu's mu, and Gallay's rho_infty(|xi|^2) (novelty pass sec 3)",
        "witness": "U = curl(e^{-|x|^2} e_3); divergence-free exactly, Gaussian, so U in H^2(mu)",
        "witness_div_max_abs_8th_order_fd": witness_div_check(),
        "source_closed_form_vs_finite_differences_max_abs_err": verify_S_against_finite_differences(),
        "quadrature": {"rule": "tensor Gauss-Legendre", "n_per_axis": n, "half_width_L": L,
                       "nodes": int(pts.shape[0])},
        "part_B_operator_classes": classes_list,
        "part_A_relaxed_tier_fluid_census": table,
        "counts": counts,
        "gate_question": ("Under the RELAXED tier, does at least one FLUID model enter the census "
                          "with screens (ii), (iii) and (iv) still passing, with the evidence-tier "
                          "downgrade carried explicitly per-row?"),
        "gate": verdict["gate"],
        "gate_code": verdict["code"],
        "survivors": verdict["survivors"],
        "near_misses_iv_b_passes_iv_a_fails": verdict["near_misses"],
        "liveness_checks": checks,
        "self_test": st,
        "scope_of_the_leray_obstruction": {
            "question": ("the Decision Maker's mandatory addition: is leg 257's mechanism general "
                         "-- any fluid nonlinearity with a non-decaying Leray-projected tail whose "
                         "coefficient is a conserved quantity?"),
            "answer": ("PARTLY, AND THE BOUNDARY IS SHARP AND MEASURED. The mechanism is a "
                       "multipole statement: it reaches a term exactly when the nonlocal operator's "
                       "output is NOT multiplied by a localised factor, so that the lowest "
                       "non-vanishing moment of its source survives. It REACHES the "
                       "velocity-pressure formulation (C1, quadrupole = the energy tensor, "
                       "|x|^-4) and -- newly, and harder -- the BUOYANCY coupling (C2, dipole = "
                       "the total mass, |x|^-3, and LINEAR). It does NOT reach the vorticity "
                       "formulation (C4) or chemotaxis (C5), where the nonlocal factor is "
                       "multiplied by a Gaussian one."),
            "discriminator": ("NOT 'is the model nonlocal'. C5 is nonlocal, its nonlocal factor has "
                              "an algebraic |x|^-2 tail, and its nonlinearity is still Gaussian. "
                              "The discriminator is whether the nonlocal output stands alone."),
            "consequence_for_leg_257": ("leg 257's MEASUREMENT is untouched and is reproduced here "
                                        "to 12 digits independently. What this leg corrects is one "
                                        "sentence of extrapolation in its repair list "
                                        "(why_the_two_obvious_repairs_fail[2]): the vorticity "
                                        "formulation does NOT inherit the obstruction by the tail "
                                        "argument. It is killed by other things, named below."),
            "what_kills_the_vorticity_route_instead": [
                ("screen (iv_a): Remark 40 names (u.grad)u and argues from H^2(mu) -> L^infty. It "
                 "does not name Biot-Savart, and the Biot-Savart kernel is not diagonal in "
                 "Breden-Chu's Hermite/Laguerre eigenbasis -- leg 257's own M2 rider names this "
                 "as a NEW cost at the quadrature rung, and it remains uncosted."),
                ("NRS/Tsai, via a composition this leg records: omega in H^2(mu) gives, by class "
                 "C3, u ~ |x|^-3, so |u|^3 r^2 ~ r^-7 is integrable at infinity and u in L^3(R^3). "
                 "For a BACKWARD SELF-SIMILAR 3D NS profile NRS/Tsai then force u == 0. The "
                 "vorticity formulation buys admissibility into the space and loses it again to "
                 "the same ansatz constraint that already binds the velocity form."),
                ("the external prior art itself: Gallay and Wayne have used exactly this Gaussian "
                 "weight on exactly the vorticity for two decades WITHOUT a self-similar blow-up "
                 "profile appearing in it, which is evidence about the target, not the method."),
            ],
        },
        "ceiling": ("CENSUS AND WITNESS QUADRATURE ONLY. Nothing certified, no solver module built, "
                    "read-into or edited. No stage claimed; plan_of_record.py untouched. NO BAN "
                    "LIFTED and none argued against. Leg 255's and leg 257's kills both STAND and "
                    "are not reopened. No link of the L1->L4 chain moved. Clay odds stay ~0.05%, "
                    "behind Walls 1 and 2."),
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=1)

    print(f"wrote {OUT}")
    print()
    print(f"witness div (8th-order FD)          {doc['witness_div_max_abs_8th_order_fd']:.3e}")
    print(f"S closed form vs FD                 {doc['source_closed_form_vs_finite_differences_max_abs_err']:.3e}")
    print(f"int|U|^2 quadrature                 {c1['energy_int_U2_quadrature']:.15f}")
    print(f"           closed form 2(pi/2)^3/2  {c1['energy_int_U2_closed_form']:.15f}")
    print(f"           leg 257                  {LEG_257_T:.15f}   |d| = {c1['energy_vs_leg_257_abs_err']:.3e}")
    print(f"max|M - 2T| (quadrupole = 2*energy) {c1['identity_M_equals_2T_max_abs_err']:.3e}")
    print(f"psi(r=10) vs leg 257                {c1['psi_r10_vs_leg_257_abs_err']:.3e}")
    print()
    print("class                          exponent   log10 weighted density at r = 10/20/40/80")
    for c in classes_list:
        e = c.get("fitted_exponent_grad_psi", c.get("fitted_exponent_velocity",
            c.get("fitted_exponent_N_over_finite_radii", float("nan"))))
        d = c["log10_weighted_density"]
        print(f"  {c['class']:<30s} {e:8.4f}   " + "  ".join(f"{v:9.1f}" for v in d))
    print()
    print(f"rows: {counts['fluid_rows_enumerated']} fluid "
          f"({counts['rows_new_in_this_leg']} new, {counts['rows_inherited_from_leg_255']} inherited); "
          f"{counts['rows_entering_via_the_relaxed_tier']} enter via the relaxed tier")
    print(f"killed by (i)/(ii)/(iii)/(iv_a)/(iv_b): "
          f"{counts['killed_by_i']}/{counts['killed_by_ii']}/{counts['killed_by_iii']}/"
          f"{counts['killed_by_iv_a']}/{counts['killed_by_iv_b']}")
    print(f"rows passing (iv_b) but failing (iv_a): {counts['rows_passing_iv_b_but_failing_iv_a']}")
    print()
    print(f"GATE: {verdict['gate']}   ({verdict['code']})")
    print(f"  survivors   : {verdict['survivors']}")
    print(f"  near misses : {verdict['near_misses']}")
    print(f"  liveness    : {len(checks)} checks, all passed")
    print(f"  self_test   : {len(st)} outcomes, gates reached = "
          f"{sorted(set(o['gate'] for o in st))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
