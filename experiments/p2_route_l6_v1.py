#!/usr/bin/env python3
"""Leg 401, unit `L6` -- BANK A DISCRETE ROUTE-4 PROFILE.

Pre-registered in `experiments/journal/leg_401.md` SS0-SS6, commit `e4598a5`, BEFORE this
file existed.  Nothing here may contradict that pre-registration.

REALIZATION (lesson 91 part 1).  Backward lambda-DSS blow-up profile of 3-D incompressible
Navier-Stokes on R^3, lambda = 1.7, a = -lambda*lambda_t = 0.5, period T_s = 2 log lambda,
unit viscosity, no forcing, non-axisymmetric admitted.  Route 4's profile system, in L5's
own notation:

    R[V] = V_s + a (V + y.grad V) - Lap V + V.grad V + grad P = 0,  div V = 0,
    V(., s + T_s) = V(., s).

Pressure-free (vorticity) form, which is what the load-bearing norm measures:

    W[V] := curl R[V] = w_s + a(2w + y.grad w) - Lap w + (V.grad)w - (w.grad)V,  w = curl V.

TRIAL SPACE (part 2).  Chandrasekhar poloidal-toroidal representation w.r.t. the position
vector,  V = curl curl (f y) + curl (g y),  so div V = 0 IDENTICALLY (no projection, no
Bogovskii corrector).

BASIS (part 3).  Real spherical harmonics Y_lm (1 <= l <= Lmax); radial algebraic map
u = r/(r+Lmap) with Chebyshev T_n(2u-1) carrying end prefactors u^l (poloidal) and
u^l (1-u) (toroidal); real Fourier in s on one DSS period, modes 0..Ks.

NORM (the one route 4's own closure requires; taken from the banked artefact
`p2_route_l5_finite_energy_v1.json` .realization_lesson_91.norms.vorticity_LOAD_BEARING):

    ||curl F||_{L1_t L3/2_x} = int_0^{T_s} ||curl_y R[V](.,s)||_{L3/2(R^3)} ds

CEILING: TIER 2, float64.  A MEASURED residual, not a bound, not a certificate, not a
blow-up.  No link of the L1->L4 chain moves.  BAN C1 stays disengaged: no Y0/Z0/Z1/Z2, no
radii polynomial, no approximate inverse, no contraction constant, no enclosure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import multiprocessing as mp
import os
import sys
import time
from pathlib import Path

# Threads per process.  The 6 starts of a rung are run in 6 worker PROCESSES (the
# optimiser is inherently sequential within a start), so BLAS is capped at 2 threads
# each to fill the 12 available cores without oversubscription.  Must be set BEFORE
# numpy is imported.
_NT = os.environ.setdefault("L6_THREADS", "2")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, _NT)

import numpy as np
from numpy.polynomial import chebyshev as C
from scipy.optimize import minimize
from scipy.special import lpmv

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p2_route_l6_v1_ad import (Var, concat0, einsum, grad_of,  # noqa: E402
                               matvec_last, sqrt as ad_sqrt)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "writeup" / "data" / "p2_route_l6_profile_v1.json"
L5_ART = ROOT / "writeup" / "data" / "p2_route_l5_finite_energy_v1.json"
CLOC_ART = ROOT / "writeup" / "data" / "p2_route_cloc_v1.json"

# --------------------------------------------------------------------------------------
# 0.  The realization's constants -- taken from the banked leg-381 / L5 realization
# --------------------------------------------------------------------------------------
LAMBDA = 1.7
A_SIM = 0.5                       # a = -lambda lambda_t
PERIOD = 2.0 * math.log(LAMBDA)   # 1.0612565021243408
OMEGA_S = 2.0 * math.pi / PERIOD  # = pi / log(lambda)
EPS_FLOOR = 1e-300


# --------------------------------------------------------------------------------------
# 1.  Real spherical harmonics and their angular derivatives
# --------------------------------------------------------------------------------------
def _norm_lm(l, m):
    m = abs(m)
    return math.sqrt((2 * l + 1) / (4 * math.pi) * math.factorial(l - m) / math.factorial(l + m))


def sh_and_derivs(l, m, theta, phi):
    """Real orthonormal Y_lm, d/dtheta Y_lm, (1/sin theta) d/dphi Y_lm on a grid."""
    x = np.cos(theta)
    st = np.sin(theta)
    am = abs(m)
    P = lpmv(am, l, x)
    Pm1 = lpmv(am, l - 1, x) if l - 1 >= 0 else np.zeros_like(x)
    # (x^2-1) dP/dx = l x P_l^m - (l+m) P_{l-1}^m  =>  dP/dtheta = -st dP/dx
    dPdth = (l * x * P - (l + am) * Pm1) / st
    N = _norm_lm(l, m)
    if m == 0:
        f, dfdphi = np.ones_like(phi), np.zeros_like(phi)
    elif m > 0:
        f, dfdphi = math.sqrt(2.0) * np.cos(m * phi), -math.sqrt(2.0) * m * np.sin(m * phi)
    else:
        f, dfdphi = math.sqrt(2.0) * np.sin(am * phi), math.sqrt(2.0) * am * np.cos(am * phi)
    Y = N * P * f
    dY_dth = N * dPdth * f
    dY_dph_over_st = N * P * dfdphi / st
    return Y, dY_dth, dY_dph_over_st


def harmonic_list(lmin, lmax):
    return [(l, m) for l in range(lmin, lmax + 1) for m in range(-l, l + 1)]


# --------------------------------------------------------------------------------------
# 2.  Radial basis: u = r/(r+Lmap), phi = A(u) T_n(2u-1), derivatives in r up to order 4
# --------------------------------------------------------------------------------------
def _cheb_derivs(n, z, kmax):
    """T_n^{(k)}(z), k = 0..kmax."""
    c = np.zeros(n + 1)
    c[n] = 1.0
    out = []
    for k in range(kmax + 1):
        out.append(C.chebval(z, C.chebder(c, k) if k else c))
    return out


def _prefactor_derivs(l, toroidal, u, kmax):
    """A(u) = u^l (times (1-u) if toroidal); derivatives d^k/du^k, k=0..kmax."""
    # represent as monomial polynomial (degree <= l+1, tiny -- exact and well conditioned)
    coef = np.zeros(l + 2)
    coef[l] = 1.0
    if toroidal:
        coef[l] -= 0.0
        c2 = np.zeros(l + 2)
        c2[l] = 1.0
        c2[l + 1] = -1.0
        coef = c2
    out = []
    cc = coef.copy()
    for k in range(kmax + 1):
        out.append(np.polynomial.polynomial.polyval(u, cc))
        cc = np.polynomial.polynomial.polyder(cc) if len(cc) > 1 else np.zeros(1)
    return out


def radial_basis(l, Nr, u, Lmap, toroidal, kmax):
    """Return list of arrays D[k][i, n] = d^k/dr^k phi_n^{(l)}(r_i), k = 0..kmax."""
    z = 2.0 * u - 1.0
    A = _prefactor_derivs(l, toroidal, u, kmax)
    # du/dr and higher: u' = (1-u)^2/Lmap, u'' = -2(1-u)^3/Lmap^2, ...
    om = 1.0 - u
    up1 = om ** 2 / Lmap
    up2 = -2.0 * om ** 3 / Lmap ** 2
    up3 = 6.0 * om ** 4 / Lmap ** 3
    up4 = -24.0 * om ** 5 / Lmap ** 4
    Dr = [np.zeros((u.size, Nr)) for _ in range(kmax + 1)]
    for n in range(Nr):
        T = _cheb_derivs(n, z, kmax)
        # g^{(k)}(u) = sum_j C(k,j) A^{(k-j)}(u) 2^j T^{(j)}(z)
        g = []
        for k in range(kmax + 1):
            acc = np.zeros_like(u)
            for j in range(k + 1):
                acc = acc + math.comb(k, j) * A[k - j] * (2.0 ** j) * T[j]
            g.append(acc)
        # chain rule to r
        Dr[0][:, n] = g[0]
        if kmax >= 1:
            Dr[1][:, n] = g[1] * up1
        if kmax >= 2:
            Dr[2][:, n] = g[2] * up1 ** 2 + g[1] * up2
        if kmax >= 3:
            Dr[3][:, n] = g[3] * up1 ** 3 + 3 * g[2] * up1 * up2 + g[1] * up3
        if kmax >= 4:
            Dr[4][:, n] = (g[4] * up1 ** 4 + 6 * g[3] * up1 ** 2 * up2
                           + g[2] * (4 * up1 * up3 + 3 * up2 ** 2) + g[1] * up4)
    return Dr


# --------------------------------------------------------------------------------------
# 3.  Geometry / operator bundle for one resolution
# --------------------------------------------------------------------------------------
class Geom:
    def __init__(self, Lmax, Nr, Ks, Lmap=2.0, nq_r=None, nth=None, nph=None, ns=None):
        self.Lmax, self.Nr, self.Ks, self.Lmap = Lmax, Nr, Ks, Lmap
        self.nq_r = nq_r if nq_r is not None else 3 * Nr + 12
        self.nth = nth if nth is not None else 2 * Lmax + 8
        self.nph = nph if nph is not None else 4 * Lmax + 12
        self.ns = ns if ns is not None else 4 * Ks + 6
        self.harm = harmonic_list(1, Lmax)
        self.nH = len(self.harm)
        self.nK = 2 * Ks + 1

        # ---- radial quadrature on u in (0,1) -> r in (0, inf) --------------------------
        xu, wu = np.polynomial.legendre.leggauss(self.nq_r)
        u = 0.5 * (xu + 1.0)
        wu = 0.5 * wu
        self.u = u
        self.r = Lmap * u / (1.0 - u)
        drdu = Lmap / (1.0 - u) ** 2
        self.wr = wu * self.r ** 2 * drdu          # includes r^2 dr

        # ---- angular grid -------------------------------------------------------------
        xt, wt = np.polynomial.legendre.leggauss(self.nth)
        th = np.arccos(xt)
        ph = 2.0 * math.pi * np.arange(self.nph) / self.nph
        TH, PH = np.meshgrid(th, ph, indexing="ij")
        self.theta, self.phi = TH.ravel(), PH.ravel()
        self.wa = np.repeat(wt, self.nph) * (2.0 * math.pi / self.nph)
        self.nP = self.theta.size

        st, ct = np.sin(self.theta), np.cos(self.theta)
        sp, cp = np.sin(self.phi), np.cos(self.phi)
        er = np.stack([st * cp, st * sp, ct], axis=-1)
        eth = np.stack([ct * cp, ct * sp, -st], axis=-1)
        eph = np.stack([-sp, cp, np.zeros_like(sp)], axis=-1)
        self.er, self.eth, self.eph = er, eth, eph

        # ---- vector spherical harmonic basis fields, Cartesian components -------------
        E = np.zeros((3, self.nH, self.nP, 3))
        for h, (l, m) in enumerate(self.harm):
            Y, dth, dph = sh_and_derivs(l, m, self.theta, self.phi)
            E[0, h] = Y[:, None] * er                       # Y e_r
            E[1, h] = dth[:, None] * eth + dph[:, None] * eph   # Psi = grad_S Y
            E[2, h] = dth[:, None] * eph - dph[:, None] * eth   # Phi = e_r x Psi
        self.E = E

        # ---- tangential-gradient operator on scalar sphere functions ------------------
        L2 = Lmax + 2
        harm2 = harmonic_list(0, L2)
        Yall = np.zeros((len(harm2), self.nP))
        Psi_all = np.zeros((self.nP, len(harm2), 3))
        for h2, (l, m) in enumerate(harm2):
            if l == 0:
                Yall[h2] = 1.0 / math.sqrt(4.0 * math.pi)
                continue
            Y, dth, dph = sh_and_derivs(l, m, self.theta, self.phi)
            Yall[h2] = Y
            Psi_all[:, h2, :] = dth[:, None] * eth + dph[:, None] * eph
        Ana = Yall * self.wa[None, :]                       # (nH2, nP)
        self.Dop = np.einsum("phj,hq->jpq", Psi_all, Ana, optimize=True)  # (3, nP, nP)
        self.GE = np.einsum("jpq,thqc->thpcj", self.Dop, E, optimize=True)

        # ---- radial basis matrices, per harmonic --------------------------------------
        BF = [np.zeros((self.nH, self.nq_r, Nr)) for _ in range(5)]
        BQ = [np.zeros((self.nH, self.nq_r, Nr)) for _ in range(4)]
        for h, (l, m) in enumerate(self.harm):
            DF = radial_basis(l, Nr, u, Lmap, False, 4)
            DQ = radial_basis(l, Nr, u, Lmap, True, 3)
            for k in range(5):
                BF[k][h] = DF[k]
            for k in range(4):
                BQ[k][h] = DQ[k]
        # column scaling (reparametrisation only -- same trial space, better conditioning)
        gw = np.exp(-self.r ** 2 / 4.0) * self.wr
        sF = np.sqrt(np.einsum("hin,i,hin->hn", BF[0], gw, BF[0], optimize=True))
        sQ = np.sqrt(np.einsum("hin,i,hin->hn", BQ[0], gw, BQ[0], optimize=True))
        sF = np.where(sF > 0, sF, 1.0)
        sQ = np.where(sQ > 0, sQ, 1.0)
        self.scaleF, self.scaleQ = 1.0 / sF, 1.0 / sQ
        self.BF = [b * self.scaleF[:, None, :] for b in BF]
        self.BQ = [b * self.scaleQ[:, None, :] for b in BQ]

        # ---- s basis ------------------------------------------------------------------
        s = PERIOD * np.arange(self.ns) / self.ns
        self.s = s
        self.ws = np.full(self.ns, PERIOD / self.ns)
        S = np.zeros((self.nK, self.ns))
        Sd = np.zeros((self.nK, self.ns))
        S[0] = 1.0
        for j in range(1, Ks + 1):
            S[2 * j - 1] = np.cos(j * OMEGA_S * s)
            Sd[2 * j - 1] = -j * OMEGA_S * np.sin(j * OMEGA_S * s)
            S[2 * j] = np.sin(j * OMEGA_S * s)
            Sd[2 * j] = j * OMEGA_S * np.cos(j * OMEGA_S * s)
        self.S, self.Sd = S, Sd

        # ---- handy broadcast constants ------------------------------------------------
        # stacked synthesis operators: one matmul instead of three plus two adds
        self.Eall = np.ascontiguousarray(np.concatenate(list(self.E), axis=0))
        self.GEall = np.ascontiguousarray(np.concatenate(list(self.GE), axis=0))
        self.Lh = np.array([l * (l + 1) for (l, m) in self.harm], float)[:, None, None]
        self.rinv = (1.0 / self.r)[None, :, None]
        self.rr = self.r[None, :, None]
        self.gauss_w = gw
        self.n_dof = 2 * self.nH * Nr * self.nK
        # F_lm(infinity) functional (u -> 1, T_n(1) = 1)
        self.Finf_vec = self.scaleF                        # (nH, Nr)

    def unpack(self, x):
        n = self.nH * self.Nr * self.nK
        aF = x[:n].reshape(self.nH, self.Nr, self.nK)
        aQ = x[n:].reshape(self.nH, self.Nr, self.nK)
        return aF, aQ


# --------------------------------------------------------------------------------------
# 4.  Forward pass:  coefficients -> W[V] on the quadrature grid  (AD-traced)
# --------------------------------------------------------------------------------------
def _radial_stack(g, aF, aQ, S):
    """s-synthesise then apply radial basis; returns F0..F4, Q0..Q3 as (nH, nq_r, ns)."""
    Fc = einsum("hnk,km->hnm", aF, S)
    Qc = einsum("hnk,km->hnm", aQ, S)
    F = [einsum("hnm,hin->him", Fc, g.BF[k]) for k in range(5)]
    Q = [einsum("hnm,hin->him", Qc, g.BQ[k]) for k in range(4)]
    return F, Q


def _vsh_V(g, F, Q):
    """VSH radial components of V and of d/dr V."""
    L, ri = g.Lh, g.rinv
    Vr = L * ri * F[0]
    Vs = ri * F[0] + F[1]
    Vp = -Q[0]
    dVr = L * (ri * F[1] - ri * ri * F[0])
    dVs = ri * F[1] - ri * ri * F[0] + F[2]
    dVp = -Q[1]
    return (Vr, Vs, Vp), (dVr, dVs, dVp)


def _vsh_w(g, F, Q):
    """VSH radial components of w = curl V and of d/dr w."""
    L, ri = g.Lh, g.rinv
    wr = L * ri * Q[0]
    ws = ri * Q[0] + Q[1]
    wp = F[2] + 2.0 * ri * F[1] - L * ri * ri * F[0]          # = Lap f
    dwr = L * (ri * Q[1] - ri * ri * Q[0])
    dws = ri * Q[1] - ri * ri * Q[0] + Q[2]
    dwp = (F[3] + 2.0 * ri * F[2] - 2.0 * ri * ri * F[1]
           - L * (ri * ri * F[1] - 2.0 * ri ** 3 * F[0]))
    return (wr, ws, wp), (dwr, dws, dwp)


def _vsh_lap_w(g, F, Q):
    """VSH radial components of Lap w."""
    L, ri = g.Lh, g.rinv
    LQ = Q[2] + 2.0 * ri * Q[1] - L * ri * ri * Q[0]
    LQ1 = (Q[3] + 2.0 * ri * Q[2] - 2.0 * ri * ri * Q[1]
           - L * (ri * ri * Q[1] - 2.0 * ri ** 3 * Q[0]))
    Lf = F[2] + 2.0 * ri * F[1] - L * ri * ri * F[0]
    Lf1 = (F[3] + 2.0 * ri * F[2] - 2.0 * ri * ri * F[1]
           - L * (ri * ri * F[1] - 2.0 * ri ** 3 * F[0]))
    Lf2 = (F[4] + 2.0 * ri * F[3] - (4.0 + L) * ri * ri * F[2]
           + (4.0 + 4.0 * L) * ri ** 3 * F[1] - 6.0 * L * ri ** 4 * F[0])
    L2f = Lf2 + 2.0 * ri * Lf1 - L * ri * ri * Lf
    return (L * ri * LQ, ri * LQ + LQ1, L2f)


def _synth(g, comps):
    """VSH radial components -> Cartesian field, layout (nq_r, ns, nP, 3).

    The (r, s, ang, component) ordering is chosen so that every large contraction below
    is already in `matmul` layout and no rank-4/5 array is ever transposed or copied.
    """
    # ONE matmul over the stacked (radial, Psi, Phi) components, not three plus two adds
    return einsum("him,hpc->impc", concat0(comps), g.Eall)


def _synth_grad(g, comps):
    """-> tangential gradient tensor of the Cartesian components: (nq_r, ns, nP, 3, 3)."""
    return einsum("him,hpcj->impcj", concat0(comps), g.GEall)


def weighted_L2_by_mode(g, aF, aQ):
    """N_A = (1/T_s) int int |V|^2 e^{-|y|^2/4} dy ds, split by s-mode -- numpy, no AD.

    Uses VSH orthonormality:  int |V|^2 dOmega = sum_h (V^r)^2 + l(l+1)[(V^Psi)^2+(V^Phi)^2].
    The s-modes are orthogonal on the period, so the total splits exactly by mode.
    """
    gw = g.gauss_w
    tot = np.zeros(g.nK)
    for k in range(g.nK):
        aFk = np.zeros_like(aF)
        aQk = np.zeros_like(aQ)
        aFk[:, :, k] = aF[:, :, k]
        aQk[:, :, k] = aQ[:, :, k]
        F = [np.einsum("hnk,km,hin->him", aFk, g.S, g.BF[j], optimize=True) for j in (0, 1)]
        Q0 = np.einsum("hnk,km,hin->him", aQk, g.S, g.BQ[0], optimize=True)
        Vr = g.Lh * g.rinv * F[0]
        Vs = g.rinv * F[0] + F[1]
        Vp = -Q0
        dens = Vr ** 2 + g.Lh * (Vs ** 2 + Vp ** 2)
        tot[k] = np.einsum("him,i,m->", dens, gw, g.ws, optimize=True) / PERIOD
    return tot


def _norm_A(g, aF, aQ):
    """AD version of N_A."""
    Fc = einsum("hnk,km->hnm", aF, g.S)
    Qc = einsum("hnk,km->hnm", aQ, g.S)
    F0 = einsum("hnm,hin->him", Fc, g.BF[0])
    F1 = einsum("hnm,hin->him", Fc, g.BF[1])
    Q0 = einsum("hnm,hin->him", Qc, g.BQ[0])
    Vr = g.Lh * g.rinv * F0
    Vs = g.rinv * F0 + F1
    Vp = -Q0
    dens = Vr * Vr + g.Lh * (Vs * Vs + Vp * Vp)
    w3 = g.gauss_w[None, :, None] * g.ws[None, None, :]
    return (dens * w3).sum() / PERIOD


def _norm_B(g, aF, aQ):
    """N_B = (1/T_s) int sum_lm F_lm(inf,s)^2 ds  -- the alpha = 1 far-field amplitude."""
    Finf = einsum("hnk,hn->hk", aF, g.Finf_vec)     # (nH, nK)
    Fs = einsum("hk,km->hm", Finf, g.S)
    w = g.ws[None, :]
    return ((Fs * Fs) * w).sum() / PERIOD


def residual_field(g, aF, aQ):
    """W[V] on the grid, shape (nq_r, nP, ns, 3), AD-traced."""
    F, Q = _radial_stack(g, aF, aQ, g.S)
    Fd, Qd = _radial_stack(g, aF, aQ, g.Sd)          # s-derivative

    Vc, dVc = _vsh_V(g, F, Q)
    wc, dwc = _vsh_w(g, F, Q)
    lwc = _vsh_lap_w(g, F, Q)
    wsc, _ = _vsh_w(g, Fd, Qd)                        # w_s

    V = _synth(g, Vc)
    W = _synth(g, wc)
    dV = _synth(g, dVc)
    dW = _synth(g, dwc)
    LW = _synth(g, lwc)
    WS = _synth(g, wsc)
    rdW = _synth(g, tuple(g.rr * c for c in dwc))     # y.grad w = r d/dr w

    SV = _synth_grad(g, Vc)                           # (1/r) x this = tangential grad
    SW = _synth_grad(g, wc)

    # grad A = e_r (x) dA/dr + (1/r) grad_S A, so for any B:
    #   (B.grad) A = (B.e_r) dA/dr + (1/r) sum_j B_j (grad_S A)_{c j}
    # -- the radial piece is contracted analytically, so the rank-5 tensor grad A is
    # never materialised.
    er = g.er[None, None, :, :]                       # (1,1,nP,3)
    ri = (1.0 / g.r)[:, None, None, None]
    sh = V.shape
    Vrad = (V * er).sum(axis=-1).reshape(sh[0], sh[1], sh[2], 1)
    Wrad = (W * er).sum(axis=-1).reshape(sh[0], sh[1], sh[2], 1)
    Ve = V.reshape(sh[0], sh[1], sh[2], 1, 3)
    We = W.reshape(sh[0], sh[1], sh[2], 1, 3)
    NL1 = Vrad * dW + ri * matvec_last(SW, V)         # (V.grad) w
    NL2 = Wrad * dV + ri * matvec_last(SV, W)         # (w.grad) V

    return WS + A_SIM * (2.0 * W + rdW) - LW + NL1 - NL2, V, W


def load_bearing_norm(g, Wfield):
    """int_0^{T_s} ||W(.,s)||_{L3/2(R^3)} ds  (AD-traced when Wfield is a Var).

    This IS the norm route 4's own closure requires -- pressure-free, because W = curl R.
    Layout of Wfield is (nq_r, ns, nP, 3).
    """
    wpr = g.wr[:, None, None] * g.wa[None, None, :]
    if isinstance(Wfield, Var):
        sq = (Wfield * Wfield).sum(axis=-1)            # (nq_r, ns, nP)
        dens = (sq + EPS_FLOOR) ** 0.75
        per_s = (dens * wpr).sum(axis=(0, 2))          # (ns,)
        return ((per_s ** (2.0 / 3.0)) * g.ws).sum()
    sq = (Wfield ** 2).sum(axis=-1)
    dens = (sq + EPS_FLOOR) ** 0.75
    per_s = (dens * wpr).sum(axis=(0, 2))
    return float(np.sum(per_s ** (2.0 / 3.0) * g.ws))


# --------------------------------------------------------------------------------------
# 5.  Objective (branch A / branch B normalisation), value + exact gradient
# --------------------------------------------------------------------------------------
def objective(g, x, branch):
    aF0, aQ0 = g.unpack(x)
    vF, vQ = Var(aF0), Var(aQ0)
    N = _norm_A(g, vF, vQ) if branch == "A" else _norm_B(g, vF, vQ)
    scale = 1.0 / ad_sqrt(N)
    aF, aQ = vF * scale, vQ * scale
    Wf, _, _ = residual_field(g, aF, aQ)
    J = load_bearing_norm(g, Wf)
    gF, gQ = grad_of(J, [vF, vQ])
    return float(J.v), np.concatenate([gF.ravel(), gQ.ravel()])


def normalise(g, x, branch):
    aF, aQ = g.unpack(x)
    N = (float(_norm_A(g, Var(aF), Var(aQ)).v) if branch == "A"
         else float(_norm_B(g, Var(aF), Var(aQ)).v))
    return x / math.sqrt(N)


# --------------------------------------------------------------------------------------
# 6.  Self-tests  (each raises -> caller exits non-zero)
# --------------------------------------------------------------------------------------
def eval_V_cart(g, aF, aQ, pts, s):
    """Evaluate V at arbitrary Cartesian points (numpy, independent of the grid)."""
    x, y, z = pts[:, 0], pts[:, 1], pts[:, 2]
    r = np.sqrt(x * x + y * y + z * z)
    th = np.arccos(np.clip(z / r, -1.0, 1.0))
    ph = np.arctan2(y, x)
    st, ct = np.sin(th), np.cos(th)
    sp, cp = np.sin(ph), np.cos(ph)
    er = np.stack([st * cp, st * sp, ct], -1)
    eth = np.stack([ct * cp, ct * sp, -st], -1)
    eph = np.stack([-sp, cp, np.zeros_like(sp)], -1)
    u = r / (r + g.Lmap)
    sv = np.zeros(g.nK)
    sv[0] = 1.0
    for j in range(1, g.Ks + 1):
        sv[2 * j - 1] = math.cos(j * OMEGA_S * s)
        sv[2 * j] = math.sin(j * OMEGA_S * s)
    out = np.zeros((pts.shape[0], 3))
    for h, (l, m) in enumerate(g.harm):
        DF = radial_basis(l, g.Nr, u, g.Lmap, False, 1)
        DQ = radial_basis(l, g.Nr, u, g.Lmap, True, 0)
        cF = (aF[h] * g.scaleF[h][:, None]) @ sv
        cQ = (aQ[h] * g.scaleQ[h][:, None]) @ sv
        F0, F1 = DF[0] @ cF, DF[1] @ cF
        Q0 = DQ[0] @ cQ
        Y, dth, dph = sh_and_derivs(l, m, th, ph)
        Psi = dth[:, None] * eth + dph[:, None] * eph
        Phi = dth[:, None] * eph - dph[:, None] * eth
        out += (l * (l + 1) * F0 / r)[:, None] * (Y[:, None] * er)
        out += ((F0 / r) + F1)[:, None] * Psi
        out += (-Q0)[:, None] * Phi
    return out


def selftests(verbose=True):
    rng = np.random.default_rng(401)
    g = Geom(Lmax=3, Nr=8, Ks=1, Lmap=2.0)
    aF = rng.standard_normal((g.nH, g.Nr, g.nK)) * 0.3
    aQ = rng.standard_normal((g.nH, g.Nr, g.nK)) * 0.3
    res = {}

    # T-A: div V = 0 (finite differences on the synthesised field)
    pts = np.array([[0.7, -0.4, 1.1], [1.9, 2.2, -0.8], [-3.1, 0.6, 2.4], [0.2, -5.0, 1.3]])
    hstep = 1e-5
    div = []
    for p in pts:
        d = 0.0
        for j in range(3):
            e = np.zeros(3)
            e[j] = hstep
            vp = eval_V_cart(g, aF, aQ, (p + e)[None, :], 0.3)[0, j]
            vm = eval_V_cart(g, aF, aQ, (p - e)[None, :], 0.3)[0, j]
            d += (vp - vm) / (2 * hstep)
        div.append(abs(d))
    scale = np.max(np.abs(eval_V_cart(g, aF, aQ, pts, 0.3)))
    res["T_A_div_V_max_abs_over_scale"] = float(max(div) / scale)
    assert res["T_A_div_V_max_abs_over_scale"] < 1e-6, res

    # T-B: analytic gradient vs central finite differences
    x0 = np.concatenate([aF.ravel(), aQ.ravel()]) * 0.5
    f0, gr = objective(g, x0, "A")
    idx = rng.choice(x0.size, size=12, replace=False)
    errs = []
    for i in idx:
        e = np.zeros_like(x0)
        e[i] = 1e-6
        fp, _ = objective(g, x0 + e, "A")
        fm, _ = objective(g, x0 - e, "A")
        fd = (fp - fm) / 2e-6
        errs.append(abs(fd - gr[i]) / max(1e-12, abs(fd) + abs(gr[i])))
    res["T_B_grad_max_rel_err"] = float(max(errs))
    assert res["T_B_grad_max_rel_err"] < 1e-5, res

    # T-C: curl in the poloidal-toroidal basis vs finite-difference curl
    F, Q = _radial_stack(g, Var(aF), Var(aQ), g.S)
    wc, _ = _vsh_w(g, F, Q)
    wgrid = _synth(g, wc).v
    ptsC = np.stack([g.r[3] * g.er[5], g.r[9] * g.er[11], g.r[15] * g.er[2]])
    im = 2
    sval = g.s[im]
    errs = []
    for p, (ii, pp) in zip(ptsC, [(3, 5), (9, 11), (15, 2)]):
        Jm = np.zeros((3, 3))
        for j in range(3):
            e = np.zeros(3)
            e[j] = 1e-5 * max(1.0, np.linalg.norm(p))
            Jm[:, j] = (eval_V_cart(g, aF, aQ, (p + e)[None, :], sval)[0]
                        - eval_V_cart(g, aF, aQ, (p - e)[None, :], sval)[0]) / (2 * e[j])
        curl = np.array([Jm[2, 1] - Jm[1, 2], Jm[0, 2] - Jm[2, 0], Jm[1, 0] - Jm[0, 1]])
        ref = wgrid[ii, im, pp]
        errs.append(np.max(np.abs(curl - ref)) / max(1e-12, np.max(np.abs(ref))))
    res["T_C_curl_max_rel_err"] = float(max(errs))
    assert res["T_C_curl_max_rel_err"] < 1e-5, res

    # T-D: W[V] from the exact-basis route vs a fully finite-difference curl R[V]
    def Rnp(p, s):
        """R[V] without the pressure gradient, by finite differences."""
        hh = 1e-4 * max(1.0, np.linalg.norm(p))
        V0 = eval_V_cart(g, aF, aQ, p[None, :], s)[0]
        Vs = (eval_V_cart(g, aF, aQ, p[None, :], s + 1e-5)[0]
              - eval_V_cart(g, aF, aQ, p[None, :], s - 1e-5)[0]) / 2e-5
        Jm = np.zeros((3, 3))
        lap = np.zeros(3)
        for j in range(3):
            e = np.zeros(3)
            e[j] = hh
            vp = eval_V_cart(g, aF, aQ, (p + e)[None, :], s)[0]
            vm = eval_V_cart(g, aF, aQ, (p - e)[None, :], s)[0]
            Jm[:, j] = (vp - vm) / (2 * hh)
            lap += (vp - 2 * V0 + vm) / hh ** 2
        ydV = Jm @ p
        VdV = Jm @ V0
        return Vs + A_SIM * (V0 + ydV) - lap + VdV

    Wf, _, _ = residual_field(g, Var(aF), Var(aQ))
    Wg = Wf.v
    errs = []
    for (ii, pp) in [(4, 7), (10, 3), (14, 9)]:
        p = g.r[ii] * g.er[pp]
        sval = g.s[1]
        hh = 3e-4 * max(1.0, np.linalg.norm(p))
        Jm = np.zeros((3, 3))
        for j in range(3):
            e = np.zeros(3)
            e[j] = hh
            Jm[:, j] = (Rnp(p + e, sval) - Rnp(p - e, sval)) / (2 * hh)
        curlR = np.array([Jm[2, 1] - Jm[1, 2], Jm[0, 2] - Jm[2, 0], Jm[1, 0] - Jm[0, 1]])
        ref = Wg[ii, 1, pp]
        errs.append(np.max(np.abs(curlR - ref)) / max(1e-9, np.max(np.abs(ref))))
    res["T_D_W_vs_fd_curlR_max_rel_err"] = float(max(errs))
    assert res["T_D_W_vs_fd_curlR_max_rel_err"] < 2e-3, res

    # T-E: DSS periodicity, exact by construction, checked anyway
    p = np.array([[1.3, -0.7, 2.1]])
    v0 = eval_V_cart(g, aF, aQ, p, 0.2117)[0]
    v1 = eval_V_cart(g, aF, aQ, p, 0.2117 + PERIOD)[0]
    res["T_E_dss_period_max_rel_err"] = float(np.max(np.abs(v1 - v0)) / np.max(np.abs(v0)))
    assert res["T_E_dss_period_max_rel_err"] < 1e-12, res

    # T-F: the R^3 quadrature reproduces a closed-form integral
    #      int_{R^3} e^{-|y|^2} dy = pi^{3/2}
    q = float(np.sum(g.wr * np.exp(-g.r ** 2)) * np.sum(g.wa))
    res["T_F_quadrature_rel_err"] = abs(q - math.pi ** 1.5) / math.pi ** 1.5
    assert res["T_F_quadrature_rel_err"] < 1e-8, res

    if verbose:
        for k, v in res.items():
            print(f"  {k:42s} {v:.3e}")
    return res


# --------------------------------------------------------------------------------------
# 7.  Diagnostics on a converged coefficient vector
# --------------------------------------------------------------------------------------
def diagnostics(g, x, branch):
    x = normalise(g, x, branch)
    aF, aQ = g.unpack(x)
    Wf, V, Wv = residual_field(g, Var(aF), Var(aQ))
    Wg, Vg = Wf.v, V.v

    d = {}
    d["load_bearing_norm"] = load_bearing_norm(g, Wg)

    # velocity-form secondary norm needs R itself (with the pressure term dropped);
    # reported as a diagnostic only, explicitly NOT pressure-free.
    modes = weighted_L2_by_mode(g, aF, aQ)
    tot = float(modes.sum())
    d["weighted_L2_total"] = tot
    d["s_mode_energy_fraction_k0"] = float(modes[0] / tot) if tot > 0 else float("nan")
    d["s_mode_energy_fraction_oscillating"] = float(modes[1:].sum() / tot) if tot > 0 else float("nan")

    # far-field alpha=1 amplitude and its s-dependence
    Finf = np.einsum("hnk,hn->hk", aF, g.Finf_vec)
    Finf_s = Finf @ g.S                                  # (nH, ns)
    amp = np.sqrt((Finf_s ** 2).sum(axis=0))             # (ns,)
    d["far_field_alpha1_amplitude_mean"] = float(amp.mean())
    d["far_field_alpha1_amplitude_rel_std"] = (
        float(amp.std() / amp.mean()) if amp.mean() > 0 else 0.0)
    # angular-shape s-dependence of the far field (reading (c-2))
    if amp.mean() > 0:
        shp = Finf_s / np.where(amp > 0, amp, 1.0)[None, :]
        d["far_field_shape_s_variation"] = float(np.max(np.abs(shp - shp.mean(axis=1, keepdims=True))))
    else:
        d["far_field_shape_s_variation"] = 0.0

    # measured far-field decay exponent of |V|   (layout i, m, p, c)
    prof = np.sqrt(np.einsum("impc,p,m->i", Vg ** 2, g.wa, g.ws, optimize=True)
                   / (4 * math.pi * PERIOD))
    sel = (g.r > 5.0) & (g.r < 200.0) & (prof > 0)
    if sel.sum() >= 3:
        A = np.vstack([np.log(g.r[sel]), np.ones(sel.sum())]).T
        sl = np.linalg.lstsq(A, np.log(prof[sel]), rcond=None)[0]
        d["far_field_decay_exponent_alpha"] = float(-sl[0])
    else:
        d["far_field_decay_exponent_alpha"] = float("nan")

    # radial-tail structure of the load-bearing integrand (leg-381-shaped diagnostic)
    sq = (Wg ** 2).sum(axis=-1)
    dens = sq ** 0.75
    radial_mass = np.einsum("imp,p,m->i", dens, g.wa, g.ws, optimize=True) * g.wr
    cum = np.cumsum(radial_mass) / max(1e-300, radial_mass.sum())
    d["tail_cumfrac"] = {}
    for R in (1.0, 10.0, 100.0, 1000.0, 10000.0):
        j = np.searchsorted(g.r, R)
        d["tail_cumfrac"][f"r_lt_{R:g}"] = float(cum[min(j, cum.size - 1)])

    # quadrature refinement of the SAME field: detects a log-divergent tail
    ref = {}
    for mult in (1, 2, 4):
        g2 = Geom(g.Lmax, g.Nr, g.Ks, g.Lmap, nq_r=mult * g.nq_r, nth=g.nth, nph=g.nph, ns=g.ns)
        W2, _, _ = residual_field(g2, Var(aF), Var(aQ))
        ref[f"nq_r_x{mult}"] = load_bearing_norm(g2, W2.v)
    d["quadrature_refinement_same_field"] = ref
    d["quadrature_refinement_ratio_x4_over_x1"] = ref["nq_r_x4"] / ref["nq_r_x1"]

    # div V, checked not assumed
    pts = np.array([[0.9, -0.5, 1.4], [2.6, 1.1, -1.9], [-0.4, 3.3, 0.7]])
    hstep = 1e-5
    dv = []
    for p in pts:
        acc = 0.0
        for j in range(3):
            e = np.zeros(3)
            e[j] = hstep
            acc += (eval_V_cart(g, aF, aQ, (p + e)[None, :], 0.31)[0, j]
                    - eval_V_cart(g, aF, aQ, (p - e)[None, :], 0.31)[0, j]) / (2 * hstep)
        dv.append(abs(acc))
    d["div_V_max_abs_checked"] = float(max(dv))
    return d


# --------------------------------------------------------------------------------------
# 8.  One rung of the ladder
# --------------------------------------------------------------------------------------
def _gscaled(x, gr, f):
    """Scale-invariant convergence measure ||x||_2 * ||grad||_2 / |J|.

    The objective is INVARIANT under x -> c x (the normalisation is applied inside the
    tape), so grad J is orthogonal to x and its size falls like 1/||x||.  A small
    ||grad||_inf therefore does NOT by itself mean converged -- it can just mean the
    coefficient vector has grown.  This quotient is invariant under x -> c x and is the
    honest stationarity measure for this parametrisation.
    """
    x = np.asarray(x, float)
    gr = np.asarray(gr, float) if gr is not None else None
    if gr is None or not np.isfinite(f) or f == 0.0:
        return float("nan")
    return float(np.linalg.norm(x) * np.linalg.norm(gr) / abs(f))


def _minimise_one(task):
    """One start: L-BFGS-B with RENORMALISING RESTARTS.  Top-level so it is picklable.

    Why restarts.  The objective is invariant under c -> t c, because the normalisation is
    applied inside the tape.  grad J is therefore orthogonal to c and its norm falls like
    1/||c||.  L-BFGS-B's stopping test is on ||proj grad||_inf, so once the iterate has
    drifted outward the test fires while the objective is STILL FALLING -- measured on this
    problem at rung J0: `CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL` at iteration
    1041 with |g|inf = 6.85e-13, at which point J was still dropping 2.7% per 25
    iterations.  That is a false stop, not a minimum.

    The fix keeps the objective and the minimiser untouched: whenever L-BFGS-B stops, the
    iterate is rescaled to the normalisation surface (which changes no function value) and
    the solver is restarted with the remaining iteration budget.  The loop ends when a
    restart buys less than `REL_STALL` relative improvement, or when the budget is spent.

    `Geom` is rebuilt in the worker; it is deterministic in its four arguments.
    """
    Lmax, Nr, Ks, Lmap, branch, name, x0, maxiter = task
    g = Geom(Lmax, Nr, Ks, Lmap)
    ts = time.time()

    traj, state = [], dict(k=0)

    def cb(xk):
        state["k"] += 1
        k = state["k"]
        if k in (1, 2, 5, 10) or k % TRAJ_EVERY == 0:
            f, gr = objective(g, xk, branch)
            traj.append([k, round(time.time() - ts, 2), f, float(np.max(np.abs(gr))),
                         _gscaled(xk, gr, f)])

    x = np.asarray(x0, float)
    total_nit = total_nfev = 0
    prev = float("inf")
    rounds, r = [], None
    while total_nit < maxiter:
        x = normalise(g, x, branch)
        r = minimize(lambda z: objective(g, z, branch), x, jac=True, method="L-BFGS-B",
                     callback=cb,
                     options=dict(maxiter=maxiter - total_nit,
                                  maxfun=2 * (maxiter - total_nit),
                                  ftol=1e-16, gtol=1e-12))
        total_nit += int(r.nit)
        total_nfev += int(r.nfev)
        rounds.append(dict(nit=int(r.nit), fun=float(r.fun), status=int(r.status),
                           coeff_norm=float(np.linalg.norm(r.x))))
        x = np.asarray(r.x, float)
        gain = (prev - float(r.fun)) / abs(prev) if np.isfinite(prev) else 1.0
        prev = float(r.fun)
        if int(r.nit) == 0 or gain < REL_STALL:
            break

    x = normalise(g, x, branch)
    fun, jac = objective(g, x, branch)
    gn = float(np.max(np.abs(jac)))
    gs = _gscaled(x, jac, fun)
    traj.append([int(total_nit), round(time.time() - ts, 2), float(fun), gn, gs])
    rec = dict(start=name, fun=float(fun), nit=int(total_nit), nfev=int(total_nfev),
               restarts=len(rounds), rounds=rounds,
               max_abs_grad=gn, scale_invariant_grad=gs,
               coeff_norm=float(np.linalg.norm(x)),
               status=int(r.status) if r is not None else -1,
               hit_maxiter=bool(total_nit >= maxiter),
               stalled_before_cap=bool(total_nit < maxiter),
               trajectory_k_sec_J_ginf_gscaled=traj,
               seconds=round(time.time() - ts, 2))
    return rec, x.copy()


def run_rung(Lmax, Nr, Ks, branch, seeds, maxiter, warm=None, Lmap=2.0, verbose=True,
             nproc=None):
    t0 = time.time()
    g = Geom(Lmax, Nr, Ks, Lmap)
    rng_starts = []
    for sd in seeds:
        rng = np.random.default_rng(sd)
        x = rng.standard_normal(g.n_dof) * 0.1
        rng_starts.append(("seed%d" % sd, normalise(g, x, branch)))
    if warm is not None:
        xw = prolong(warm[0], g, warm[1])
        try:
            rng_starts.append(("continuation", normalise(g, xw, branch)))
        except (ZeroDivisionError, ValueError):
            pass

    tasks = [(Lmax, Nr, Ks, Lmap, branch, name, x0, maxiter) for name, x0 in rng_starts]
    if nproc is None:
        # measured (experiments/_l6_scaling.py): the residual is memory-bandwidth bound,
        # so at the smallest rung 6 processes are SLOWER in aggregate than 1, while at the
        # larger rungs 6 processes buy ~1.9x.  The threshold is where the two cross.
        wide = int(os.environ.get("L6_NPROC", "6"))
        nproc = min(len(tasks), 1 if g.n_dof < 500 else wide)
    if nproc > 1:
        ctx = mp.get_context("fork")
        with ctx.Pool(nproc) as pool:
            results = pool.map(_minimise_one, tasks, chunksize=1)
    else:
        results = [_minimise_one(t) for t in tasks]

    best = None
    per_start = []
    for rec, xopt in results:
        per_start.append(rec)
        if best is None or rec["fun"] < best[0]:
            best = (rec["fun"], xopt)
        if verbose:
            print(f"    start={rec['start']:12s} J={rec['fun']:.10e} nit={rec['nit']:5d} "
                  f"|g|inf={rec['max_abs_grad']:.2e} {rec['seconds']:.1f}s "
                  f"status={rec['status']}")
    out = dict(Lmax=Lmax, Nr=Nr, Ks=Ks, branch=branch, n_dof=g.n_dof,
               nq_r=g.nq_r, n_theta=g.nth, n_phi=g.nph, n_s=g.ns, Lmap=Lmap,
               residual_load_bearing=best[0], starts=per_start,
               seconds=round(time.time() - t0, 2))
    return out, g, best[1]


def _l5_norm_verbatim():
    """The load-bearing norm string as L5 banked it, read from the banked artefact and
    never retyped -- so the norm this leg measures in cannot have been invented here."""
    try:
        return json.loads(L5_ART.read_text())[
            "realization_lesson_91"]["norms"]["vorticity_LOAD_BEARING"]
    except Exception as exc:                                    # noqa: BLE001
        return f"UNREADABLE: {exc}"


def bank_profile(g, x, branch, tag):
    """Package the actual velocity field so the artefact CARRIES THE PROFILE, not just a
    number about it.  The gate asks for a divergence-free velocity field to be banked."""
    # objective() rescales c -> c/sqrt(N(c)) INSIDE the tape, so the residual it reports is
    # the residual of the NORMALISED field.  Bank that field, not the raw iterate, or the
    # banked coefficients do not reproduce the banked number (caught by evidence check C18).
    x = normalise(g, np.asarray(x, float), branch)
    aF, aQ = g.unpack(x)
    # Sample V on a fixed, named grid so the field is checkable without this code.
    # No direction is the polar axis: theta=0 is a coordinate singularity of the vector
    # spherical harmonics (Psi, Phi involve d_phi Y / sin theta), not of the field.  The
    # quadrature never touches it -- Gauss-Legendre nodes in cos(theta) are interior.
    dirs = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.3, -0.4, 0.9],
                     [1.0, 1.0, 1.0], [1.0, -2.0, 0.5]], float)
    dirs = dirs / np.linalg.norm(dirs, axis=1, keepdims=True)
    radii = [0.25, 1.0, 4.0, 16.0, 64.0]
    pts = np.array([d * rr for rr in radii for d in dirs])
    samples = []
    for s_val in (0.0, 0.25 * PERIOD, 0.5 * PERIOD):
        V = eval_V_cart(g, aF, aQ, pts, s_val)
        if not np.all(np.isfinite(V)):
            raise FloatingPointError("non-finite V in banked field samples")
        samples.append(dict(s=float(s_val),
                            points=[[float(c) for c in q] for q in pts],
                            V=[[float(c) for c in v] for v in V]))
    return dict(
        branch=branch, rung=tag, Lmax=g.Lmax, Nr=g.Nr, Ks=g.Ks, Lmap=g.Lmap,
        n_dof=int(g.n_dof),
        harmonics_l_m=[[int(l), int(m)] for (l, m) in g.harm],
        packing=("x = concat(aF.ravel(), aQ.ravel()); aF, aQ have shape "
                 "(nH, Nr, nK) with nH = Lmax(Lmax+2) harmonics ordered as "
                 "harmonics_l_m, Nr radial Chebyshev modes, nK = 2*Ks+1 real Fourier "
                 "modes in s ordered [1, cos(w s), sin(w s), cos(2 w s), sin(2 w s), ...] "
                 "with w = 2 pi / (2 log lambda)"),
        column_scaling=("coefficients are expressed in the unit-Gaussian-weighted-L2 "
                        "column scaling built by Geom(Lmax,Nr,Ks,Lmap); Geom is "
                        "deterministic in those four arguments, so the scaling is "
                        "reproducible and no scale factors need be stored"),
        reconstruction=("V(y,s) = curl curl (f y) + curl (g y) with "
                        "f = sum_lm F_lm(r) S_k(s) Y_lm, g = sum_lm Q_lm(r) S_k(s) Y_lm; "
                        "F built from aF on the u^l * T_n(2u-1) basis, Q from aQ on the "
                        "u^l (1-u) * T_n(2u-1) basis, u = r/(r+Lmap)"),
        coefficients=[float(c) for c in np.asarray(x, float)],
        field_samples=samples,
    )


def prolong(x_old, g_new, g_old):
    """Zero-prolong a coefficient vector from a coarser space into a finer one."""
    aFo, aQo = g_old.unpack(x_old)
    aFn = np.zeros((g_new.nH, g_new.Nr, g_new.nK))
    aQn = np.zeros((g_new.nH, g_new.Nr, g_new.nK))
    idx_old = {hm: i for i, hm in enumerate(g_old.harm)}
    for i, hm in enumerate(g_new.harm):
        if hm in idx_old:
            j = idx_old[hm]
            nr = min(g_old.Nr, g_new.Nr)
            nk = min(g_old.nK, g_new.nK)
            # undo the old column scaling, apply the new one (same function, new coords)
            aFn[i, :nr, :nk] = (aFo[j, :nr, :nk] * g_old.scaleF[j, :nr, None]
                                / g_new.scaleF[i, :nr, None])
            aQn[i, :nr, :nk] = (aQo[j, :nr, :nk] * g_old.scaleQ[j, :nr, None]
                                / g_new.scaleQ[i, :nr, None])
    return np.concatenate([aFn.ravel(), aQn.ravel()])


def verdict(ns, rs):
    """The pre-registered decision rule (leg_401.md SS5.1), in one place."""
    if len(rs) < 2:
        return "NO", float("nan")
    rels = [(rs[i] - rs[i - 1]) / rs[i - 1] for i in range(1, len(rs))]
    k = slice(max(0, len(rs) - 3), len(rs))
    s3 = slope(ns[k], rs[k])
    strictly_dec = all(rs[i] < rs[i - 1] for i in range(max(1, len(rs) - 2), len(rs)))
    big = all(r < -0.05 for r in rels[-2:]) if len(rels) >= 2 else False
    return ("YES" if (strictly_dec and big and s3 < -0.05) else "NO"), s3


def residual_at_cap(rows, K):
    """Best residual over starts at iteration cap K, from the recorded trajectories.

    Answers the question the iteration cap raises: is the refinement verdict a fact about
    the construction, or about where L-BFGS-B happened to be stopped?
    """
    out = []
    for row in rows:
        best = None
        for st_ in row["starts"]:
            pts = [t for t in st_.get("trajectory_k_sec_J_ginf_gscaled", []) if t[0] <= K]
            if pts:
                v = min(t[2] for t in pts)
                best = v if best is None else min(best, v)
        out.append(best)
    return out


def slope(ns, rs):
    ns, rs = np.asarray(ns, float), np.asarray(rs, float)
    ok = rs > 0
    if ok.sum() < 2:
        return float("nan")
    A = np.vstack([np.log(ns[ok]), np.ones(ok.sum())]).T
    return float(np.linalg.lstsq(A, np.log(rs[ok]), rcond=None)[0][0])


# --------------------------------------------------------------------------------------
# 9.  Driver
# --------------------------------------------------------------------------------------
JOINT_LADDER = [("J0", 2, 8, 1), ("J1", 2, 12, 1), ("J2", 3, 12, 2),
                ("J3", 3, 16, 2), ("J4", 4, 20, 3)]
SEEDS = [401, 402, 403, 404, 405]

# how often the convergence trajectory is sampled (an extra objective+gradient each time,
# so it is kept sparse)
TRAJ_EVERY = 50

# a renormalising restart that buys less than this relative improvement means the
# start has genuinely stalled, not that L-BFGS-B's gradient test misfired
REL_STALL = 1e-10

# Single-axis ladders, leg_401.md SS5, verbatim:
#   radial   N_r   in {8,12,16,20,24} at (L_max,K_s) = (3,2)
#   angular  L_max in {1,2,3,4}       at (N_r,K_s)   = (16,2)
#   temporal K_s   in {0,1,2,3}       at (L_max,N_r) = (3,16);  K_s = 0 is the
#                                     exactly-self-similar control
AXIS_LADDERS = {
    "radial":   [(f"R{n}", 3, n, 2) for n in (8, 12, 16, 20, 24)],
    "angular":  [(f"A{l}", l, 16, 2) for l in (1, 2, 3, 4)],
    "temporal": [(f"K{k}", 3, 16, k) for k in (0, 1, 2, 3)],
}

CKPT = ROOT / "experiments" / "_l6_ckpt"


def _checkpoint(name, obj):
    """Flush partial results to disk.  The container is ephemeral; a ladder that dies at
    the top rung must not take the rungs below it with it."""
    CKPT.mkdir(exist_ok=True)
    (CKPT / f"{name}.json").write_text(json.dumps(obj, indent=1, default=float))


def run_ladder(ladder, branch, seeds, maxiter, ckpt_name, verbose=True):
    """Run a ladder bottom-up with continuation between consecutive rungs."""
    rows, warm, last = [], None, None
    for (tag, Lmax, Nr, Ks) in ladder:
        print(f"  rung {tag}: Lmax={Lmax} Nr={Nr} Ks={Ks}", flush=True)
        row, g, xbest = run_rung(Lmax, Nr, Ks, branch, seeds, maxiter, warm=warm,
                                 verbose=verbose)
        row["tag"] = tag
        rows.append(row)
        warm = (xbest, g)
        last = (row, g, xbest)
        print(f"    -> residual = {row['residual_load_bearing']:.10e}   "
              f"({row['seconds']:.0f}s)", flush=True)
        _checkpoint(ckpt_name, rows)
    return rows, last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--maxiter", type=int, default=4000)
    ap.add_argument("--rungs", type=int, default=5)
    ap.add_argument("--selftest-only", action="store_true")
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--axis-branch", default="B", choices=["A", "B", "none"],
                    help="branch on which the three single-axis ladders are run")
    ap.add_argument("--axis-maxiter", type=int, default=None,
                    help="iteration cap for the secondary single-axis ladders "
                         "(defaults to --maxiter)")
    args = ap.parse_args()

    t_start = time.time()
    print("SELF-TESTS (leg_401.md SS6):")
    st = selftests()
    if args.selftest_only:
        return 0

    seeds = SEEDS[:2] if args.quick else SEEDS
    doc = dict(
        leg=401, unit="L6", lane="L", route="L6-ROUTE4-PROFILE",
        what=("BANK A DISCRETE ROUTE-4 PROFILE: a divergence-free velocity field on a named "
              "realization, in a named trial space and basis, solving route 4's profile system "
              "to a MEASURED residual."),
        preregistration=("experiments/journal/leg_401.md SS0-SS6, commit e4598a5, committed "
                         "BEFORE this file existed"),
        gate_source="writeup/waves/WAVE6_PLAN.md section L6, committed at e202653 before dispatch",
        ceiling=("TIER 2. float64. A MEASURED residual, NOT a bound, NOT a certificate, NOT a "
                 "blow-up. No link of the L1->L4 chain moved. Clay stays ~0.05%."),
        ban_C1=dict(
            engaged=False,
            apparatus="L-BFGS-B nonlinear least-squares residual minimisation",
            citation=("R. H. Byrd, P. Lu, J. Nocedal, C. Zhu, 'A limited memory algorithm for "
                      "bound constrained optimization', SIAM J. Sci. Comput. 16(5) (1995) "
                      "1190-1208; scipy.optimize.minimize(method='L-BFGS-B')"),
            constructs_no_bounded_approximate_inverse_uniform_in_M=True,
            why=("No Y0, Z0, Z1, Z2, no radii polynomial, no operator norm of any A ~ DR[V]^-1, "
                 "no contraction constant, no enclosure, no interval arithmetic. DR[V] is never "
                 "inverted, never approximately inverted and never bounded. The L-BFGS inverse-"
                 "Hessian approximation is an approximation to the Hessian of a SCALAR objective, "
                 "is never bounded or verified, and enters no number in this artefact. C1 is NOT "
                 "cited here as evidence that any apparatus closes for any object class."),
        ),
        realization_lesson_91=dict(
            object=("backward lambda-DSS blow-up profile of 3D incompressible Navier-Stokes on "
                    "R^3, lambda=1.7, a=-lambda*lambda_t=0.5, similarity period 2 log lambda, "
                    "unit viscosity, no forcing, non-axisymmetric admitted (all |m|<=l carried)"),
            lambda_=LAMBDA, a=A_SIM, period=PERIOD, omega_s=OMEGA_S,
            realization_source=("same constants as the banked leg-381 / L5 realization: "
                                "experiments/p2_route_l5_v1.py LAMBDA=1.7, A_MOD=0.5, "
                                "PERIOD=2 log LAMBDA"),
            profile_system=("R[V] = V_s + a(V + y.grad V) - Lap V + V.grad V + grad P = 0, "
                            "div V = 0, V(.,s+2 log lambda) = V(.,s)"),
            pressure_free_form=("W[V] := curl R[V] = w_s + a(2w + y.grad w) - Lap w "
                                "+ (V.grad)w - (w.grad)V,  w = curl V"),
            trial_space=("Chandrasekhar poloidal-toroidal representation w.r.t. the position "
                         "vector: V = curl curl (f y) + curl (g y); div V = 0 IDENTICALLY, no "
                         "projection and no Bogovskii corrector"),
            basis=("real spherical harmonics Y_lm (1<=l<=Lmax) x radial Chebyshev T_n(2u-1) on "
                   "the algebraic map u=r/(r+Lmap), with end prefactors u^l (poloidal) and "
                   "u^l(1-u) (toroidal), x real Fourier in s on one DSS period (modes 0..Ks). "
                   "Far-field alpha=1 IS representable (F(inf) free) and so is alpha>1."),
            basis_conditioning=("coefficients are column-scaled to unit Gaussian-weighted L2 "
                                "norm; a reparametrisation of the SAME trial space, not a "
                                "preconditioner of any operator"),
            quadrature=("radial Gauss-Legendre in u on (0,1) covering all of [0,inf) with no "
                        "outer boundary; Gauss-Legendre in cos(theta); uniform in phi; uniform "
                        "trapezoid in s over one period"),
            norms=dict(
                LOAD_BEARING=("||curl F||_{L1_t L3/2_x} = int_0^{2 log lambda} "
                              "||curl_y R[V](.,s)||_{L3/2(R^3)} ds  (pressure-free)"),
                norm_source=("writeup/data/p2_route_l5_finite_energy_v1.json "
                             ".realization_lesson_91.norms.vorticity_LOAD_BEARING"),
                norm_source_verbatim=_l5_norm_verbatim(),
                same_norm_why=("L5 writes the integrand as curl_y R_loc and L6 as curl_y R[V]: "
                               "the same object, since L6's R[V] IS route 4's profile operator "
                               "and L6's V is global, so no localisation appears. Both are "
                               "||curl F||_{L1_t L3/2_x} over one DSS period."),
            ),
            normalisations=dict(
                branch_A=("free far field: (1/T_s) int int |V|^2 e^{-|y|^2/4} dy ds = 1"),
                branch_B=("pinned far field: (1/T_s) int sum_lm F_lm(inf,s)^2 ds = 1, i.e. the "
                          "alpha=1 far-field amplitude is held at unit size -- the class the "
                          "Chae-Wolf pin says a nontrivial backward lambda-DSS profile must "
                          "lie in"),
                why=("V == 0 solves the system exactly; an unconstrained residual minimisation "
                     "is void. Both normalisations are homogeneous of degree 2 in the "
                     "coefficients and are imposed by exact rescaling, with no multiplier and "
                     "no penalty."),
            ),
        ),
        selftests=st,
        optimiser=dict(method="L-BFGS-B", maxiter=args.maxiter, ftol=1e-16, gtol=1e-12,
                       seeds=seeds, plus_continuation_start=True,
                       reported_residual="minimum over starts"),
        joint_ladder=JOINT_LADDER[:args.rungs],
    )

    results, banked = {}, {}
    for branch in ("A", "B"):
        print(f"\nBRANCH {branch}", flush=True)
        rows, last = run_ladder(JOINT_LADDER[:args.rungs], branch, seeds, args.maxiter,
                                f"joint_{branch}")
        row, g, xbest = last
        row["diagnostics"] = diagnostics(g, xbest, branch)
        _checkpoint(f"joint_{branch}", rows)
        results[branch] = rows
        banked[branch] = bank_profile(g, xbest, branch, row["tag"])
        banked[branch]["residual_load_bearing"] = row["residual_load_bearing"]

    doc["ladder_results"] = results
    doc["banked_profile"] = banked

    # ---- single-axis ladders (leg_401.md SS5) -----------------------------------------
    axis = {}
    axis_maxiter = args.axis_maxiter or args.maxiter
    if args.axis_branch != "none":
        for name, lad in AXIS_LADDERS.items():
            print(f"\nAXIS LADDER {name} (branch {args.axis_branch})", flush=True)
            rows, _ = run_ladder(lad, args.axis_branch, seeds, axis_maxiter,
                                 f"axis_{name}_{args.axis_branch}")
            rs = [r["residual_load_bearing"] for r in rows]
            ns = [r["n_dof"] for r in rows]
            axis[name] = dict(branch=args.axis_branch, rungs=rows,
                              per_rung_residual=dict(zip([r["tag"] for r in rows], rs)),
                              rate_dlogresid_dlogndof=slope(ns, rs))
    doc["axis_ladders"] = dict(
        branch=args.axis_branch,
        maxiter=axis_maxiter,
        why_one_branch=("branch B is the pinned alpha=1 class -- the class the Chae-Wolf pin "
                        "says a nontrivial backward lambda-DSS profile must lie in -- so the "
                        "per-axis rates are measured there. Running both branches on all three "
                        "axis ladders as well as the joint ladder was not affordable; the cost "
                        "is recorded in cost_and_shortfall."),
        ladders=axis,
    )

    # ---- the gate answer ---------------------------------------------------------------
    def _cap_table(rows, ns, mx):
        tab = {}
        for K in [k for k in (50, 100, 200, 400, 800, 1600, 3200) if k <= mx] + [mx]:
            rs_k = residual_at_cap(rows, K)
            if any(v is None for v in rs_k):
                continue
            v, s3 = verdict(ns, rs_k)
            tab[str(K)] = dict(per_rung_residual=rs_k, decreases_under_refinement=v,
                               rate_dlogresid_dlogndof_last3=s3)
        vs = [t["decreases_under_refinement"] for t in tab.values()]
        return dict(by_cap=tab, verdict_is_stable_in_the_cap=bool(len(set(vs)) == 1),
                    why=("if the verdict is the same at every iteration cap, it is a fact "
                         "about the construction and not about where the optimiser stopped"))

    gate = {}
    for branch in ("A", "B"):
        rows = results[branch]
        rs = [r["residual_load_bearing"] for r in rows]
        ns = [r["n_dof"] for r in rows]
        last3 = slice(max(0, len(rs) - 3), len(rs))
        s_all = slope(ns, rs)
        s_last3 = slope(ns[last3], rs[last3])
        rels = [(rs[i] - rs[i - 1]) / rs[i - 1] for i in range(1, len(rs))]
        strictly_dec = all(rs[i] < rs[i - 1] for i in range(max(1, len(rs) - 2), len(rs)))
        big_enough = all(r < -0.05 for r in rels[-2:]) if len(rels) >= 2 else False
        yes = bool(strictly_dec and big_enough and s_last3 < -0.05)
        gate[branch] = dict(
            smallest_residual=min(rs),
            residual_at_best_affordable_resolution=rs[-1],
            best_affordable_resolution=dict(tag=rows[-1]["tag"], Lmax=rows[-1]["Lmax"],
                                            Nr=rows[-1]["Nr"], Ks=rows[-1]["Ks"],
                                            n_dof=rows[-1]["n_dof"]),
            per_rung_residual=dict(zip([r["tag"] for r in rows], rs)),
            per_rung_relative_change=rels,
            decreases_under_refinement="YES" if yes else "NO",
            rate_dlogresid_dlogndof_last3=s_last3,
            rate_dlogresid_dlogndof_all=s_all,
            stability_against_the_iteration_cap=_cap_table(rows, ns, args.maxiter),
        )
    doc["gate"] = gate

    # ---- readings ----------------------------------------------------------------------
    dA = results["A"][-1]["diagnostics"]
    dB = results["B"][-1]["diagnostics"]
    doc["readings"] = dict(
        reading_c1_SS_collapse=dict(
            tolerance=1e-6,
            branch_A_oscillating_fraction=dA["s_mode_energy_fraction_oscillating"],
            branch_B_oscillating_fraction=dB["s_mode_energy_fraction_oscillating"],
            fired_A=bool(dA["s_mode_energy_fraction_oscillating"] < 1e-6),
            fired_B=bool(dB["s_mode_energy_fraction_oscillating"] < 1e-6),
            change_of_variables_if_fired="the DSS->SS reduction V_s == 0",
        ),
        reading_c2_far_field_SS_collapse=dict(
            branch_A_far_field_shape_s_variation=dA["far_field_shape_s_variation"],
            branch_B_far_field_shape_s_variation=dB["far_field_shape_s_variation"],
            branch_A_far_field_amplitude_rel_std=dA["far_field_alpha1_amplitude_rel_std"],
            branch_B_far_field_amplitude_rel_std=dB["far_field_alpha1_amplitude_rel_std"],
        ),
        reading_c3_trivialisation=dict(
            branch_A_weighted_L2=dA["weighted_L2_total"],
            branch_B_weighted_L2=dB["weighted_L2_total"],
        ),
    )
    # ---- reading (d): the cost, stated whether or not the answer is a NO ---------------
    all_starts = []
    for br in results.values():
        for r in br:
            all_starts.extend(r["starts"])
    for lad in axis.values():
        for r in lad["rungs"]:
            all_starts.extend(r["starts"])
    n_capped = sum(1 for r in all_starts if r["hit_maxiter"])
    top = results["B"][-1]
    doc["cost_and_shortfall"] = dict(
        preregistered_maxiter=20000,
        maxiter_actually_used=args.maxiter,
        maxiter_on_the_secondary_axis_ladders=axis_maxiter,
        shortfall_reason=("wall-clock. One objective-plus-exact-gradient evaluation costs "
                          "~0.25 s at rung J0 and ~1.5 s at rung J4 on 12 cores; the "
                          "pre-registered 20000 iterations x 6 starts x 5 joint rungs x 2 "
                          "branches x 13 further axis rungs is ~10^3 core-hours, which this "
                          "container does not have."),
        starts_run=len(all_starts),
        starts_that_hit_the_iteration_cap=n_capped,
        fraction_of_starts_capped=(n_capped / len(all_starts)) if all_starts else None,
        resolution_reached=dict(tag=top["tag"], Lmax=top["Lmax"], Nr=top["Nr"],
                                Ks=top["Ks"], n_dof=top["n_dof"],
                                nq_r=top["nq_r"], n_theta=top["n_theta"],
                                n_phi=top["n_phi"], n_s=top["n_s"]),
        wall_clock_seconds=round(time.time() - t_start, 1),
        wall_clock_hours=round((time.time() - t_start) / 3600.0, 3),
        cores=12,
        UNDER_RESOURCED=bool(n_capped > 0),
    )
    doc["runtime_seconds"] = round(time.time() - t_start, 1)
    doc["chain"] = dict(
        L1_to_L4_link_moved="NONE",
        clay_percent_unchanged=True,
        this_is_not_a_blowup=True,
        this_is_not_a_certificate=True,
    )

    body = json.dumps(doc, sort_keys=True)
    doc["self_hash"] = hashlib.sha256(body.encode()).hexdigest()[:16]
    OUT.write_text(json.dumps(doc, indent=1, sort_keys=True))
    print(f"\nwrote {OUT}  self_hash={doc['self_hash']}  "
          f"({doc['runtime_seconds']:.0f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
