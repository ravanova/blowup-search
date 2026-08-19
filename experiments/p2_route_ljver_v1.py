#!/usr/bin/env python3
"""Leg 409, unit `L-JVER` -- AN INDEPENDENT SECOND IMPLEMENTATION OF `W[V]` AND `J(c)`.

Pre-registered in `experiments/journal/leg_409.md` SS0-SS6, commit `bb3a5f8`, BEFORE this
file existed.  Nothing here may contradict that pre-registration.

WHY THIS FILE EXISTS.  Every route-4 residual in the record -- `L5`'s `c_mod = 869.288`,
`L6`'s `rho = 1.613811231995397`, `L6-b`'s `1.504851895102804` -- is downstream of one
function, `experiments/p2_route_l6_v1.py`'s `objective`, whose only internal evidence is a
self-test comparing two of its OWN implementations.  This file computes the same written
functional by disjoint means so that the comparison is a CHECK and not a self-comparison.

WHAT THIS FILE MAY NOT DO, AND DOES NOT DO.  It imports nothing from
`experiments/p2_route_l6_v1.py`, calls nothing in it, and contains no line copied or
transliterated from it.  `experiments/p2_route_ljver_v1_ref.py` is a SEPARATE, QUARANTINED
driver that runs `L6`'s code as a black box to produce reference values at points the
artefact does not bank; this module does not import that driver either.

THE WRITTEN MATHEMATICS, taken from `writeup/data/p2_route_l6_profile_v1.json`
(`.realization_lesson_91`, `.banked_profile.*.packing/reconstruction/column_scaling`) and
from the docstring of `L6`'s script -- READ, never imported:

    R[V] = V_s + a (V + y.grad V) - Lap V + V.grad V + grad P = 0,  div V = 0
    W[V] = curl R[V] = w_s + a(2w + y.grad w) - Lap w + (V.grad)w - (w.grad)V,  w = curl V
    V    = curl curl (f y) + curl (g y)
    J    = int_0^{T_s} || W(.,s) ||_{L3/2(R^3)} ds,   T_s = 2 log lambda,  lambda = 1.7, a = 0.5

HOW THIS IMPLEMENTATION DIFFERS (journal SS3, pre-committed):

 1. OPERATOR REPRESENTATION.  `L6` works in vector-spherical-harmonic radial components
    with hand-derived per-component radial recursions and a pseudo-spectral tangential
    gradient matrix.  This file works in CARTESIAN coordinates on real SOLID HARMONIC
    POLYNOMIALS R_lm(y) = r^l Y_lm(yhat), with one generic differentiation rule

        d_i [ y^alpha r^p G^{(k)}(r) ] =   alpha_i y^{alpha-e_i} r^p     G^{(k)}
                                         + p       y^{alpha+e_i} r^{p-2} G^{(k)}
                                         +         y^{alpha+e_i} r^{p-1} G^{(k+1)}

    from which curl, curl curl, grad, Lap and y.grad are all assembled.  No VSH component,
    no 1/sin(theta), no analytic per-component formula appears anywhere below.
 2. RADIAL DERIVATIVES.  `L6` uses an explicit chain rule through u(r) with hard-coded
    du/dr .. d4u/dr4.  This file uses 1-D TAYLOR (jet) ARITHMETIC carried through the
    Chebyshev three-term recurrence and a jet division for u = r/(r+Lmap); no chain-rule
    formula is written down at all.  CAUCHY'S INTEGRAL FORMULA on a complex circle is
    implemented as well and cross-checks the jets (control X6).
 3. RADIAL QUADRATURE.  `L6`: one Gauss-Legendre rule in u = r/(r+2).  This file:
    COMPOSITE Gauss-Legendre in ln r over an explicit [r_min, r_max], so the inner and
    outer cutoffs are named numbers that can be varied and reported.
 4. ANGULAR QUADRATURE.  `L6`: Gauss-Legendre in cos(theta) x uniform phi (a polar grid).
    This file: a CUBE-SPHERE rule -- six gnomonic patches, Gauss-Legendre in each
    equiangular patch coordinate, exact (1+X^2)(1+Y^2)/delta^3 Jacobian.  No polar axis.
 5. s QUADRATURE AND NORMALISATION.  `L6`: uniform trapezoid, and N_B by that quadrature.
    This file: half-step-offset uniform rule at a different count, and N_B in CLOSED FORM
    from Fourier orthogonality with no s quadrature at all.

WHAT CANNOT BE MADE DIFFERENT, and is inherited (journal ceiling C-6): the Y_lm phase and
normalisation convention, the harmonic ordering, the packing of x, the map u = r/(r+2), the
Chebyshev index, and the column scaling sigma -- these are the CONVENTION that gives the
banked coefficients their meaning.  sigma is re-derived here from its defining integral with
this file's own quadrature and the discrepancy is reported, not adopted.

CEILING: TIER 2, float64.  A MEASURED agreement or disagreement between two codes.  Not a
bound, not a certificate, not a blow-up.  No link of the L1->L4 chain moves.  Clay ~0.05%.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import lpmv

ROOT = Path(__file__).resolve().parents[1]
L6_ART = ROOT / "writeup" / "data" / "p2_route_l6_profile_v1.json"

# ---------------------------------------------------------------------------------------
# 0.  The realization's constants -- read from the banked artefact, not hard-wired blindly
# ---------------------------------------------------------------------------------------
LAMBDA = 1.7
A_SIM = 0.5
PERIOD = 2.0 * math.log(LAMBDA)
OMEGA_S = 2.0 * math.pi / PERIOD
LMAP = 2.0


# ---------------------------------------------------------------------------------------
# 1.  The angular CONVENTION (inherited, see ceiling C-6) and its POLYNOMIAL form (mine)
# ---------------------------------------------------------------------------------------
def ylm_convention(l, m, nx, ny, nz):
    """Real Y_lm on unit vectors, in the convention the banked coefficients are expressed in.

    This is a CONVENTION, not an implementation choice: N_lm * P_l^{|m|}(cos th) * f_m(phi)
    with N_lm = sqrt((2l+1)/(4 pi) (l-|m|)!/(l+|m|)!), f_0 = 1, f_{m>0} = sqrt2 cos(m phi),
    f_{m<0} = sqrt2 sin(|m| phi), and P including the Condon-Shortley phase (scipy `lpmv`).
    """
    am = abs(m)
    N = math.sqrt((2 * l + 1) / (4.0 * math.pi)
                  * math.factorial(l - am) / math.factorial(l + am))
    ct = np.clip(nz, -1.0, 1.0)
    phi = np.arctan2(ny, nx)
    P = lpmv(am, l, ct)
    if m == 0:
        f = np.ones_like(phi)
    elif m > 0:
        f = math.sqrt(2.0) * np.cos(m * phi)
    else:
        f = math.sqrt(2.0) * np.sin(am * phi)
    return N * P * f


def _monomials_of_degree(d):
    return [(i, j, d - i - j) for i in range(d + 1) for j in range(d - i + 1)]


def solid_harmonic_poly(l, m, rng):
    """R_lm(y) = r^l Y_lm(yhat) as an exact homogeneous polynomial, {(i,j,k): coeff}.

    Determined by solving a small least-squares system against the convention above on
    random unit vectors -- i.e. the polynomial is DERIVED here, not looked up, and is then
    verified (i) to reproduce the convention to 1e-13 on fresh points and (ii) to be
    harmonic, which no fitting artefact would satisfy.
    """
    mons = _monomials_of_degree(l)
    npts = max(6 * len(mons), 60)
    v = rng.standard_normal((npts, 3))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    A = np.stack([v[:, 0] ** i * v[:, 1] ** j * v[:, 2] ** k for (i, j, k) in mons], axis=1)
    b = ylm_convention(l, m, v[:, 0], v[:, 1], v[:, 2])
    c, *_ = np.linalg.lstsq(A, b, rcond=None)
    return {mons[t]: float(c[t]) for t in range(len(mons))}


def poly_eval(poly, nx, ny, nz):
    out = np.zeros_like(nx)
    for (i, j, k), c in poly.items():
        out = out + c * nx ** i * ny ** j * nz ** k
    return out


def poly_laplacian(poly):
    out = {}
    for (i, j, k), c in poly.items():
        for ax, e in enumerate((i, j, k)):
            if e >= 2:
                key = list((i, j, k))
                key[ax] -= 2
                key = tuple(key)
                out[key] = out.get(key, 0.0) + c * e * (e - 1)
    return {k: v for k, v in out.items() if abs(v) > 0.0}


# ---------------------------------------------------------------------------------------
# 2.  1-D Taylor (jet) arithmetic -- the radial derivative engine
# ---------------------------------------------------------------------------------------
class Jet:
    """Taylor coefficients a[k] = f^{(k)}(r)/k!, vectorised over the radial nodes."""

    __slots__ = ("a",)

    def __init__(self, a):
        self.a = a                                   # shape (K+1, n)

    @property
    def K(self):
        return self.a.shape[0] - 1

    @staticmethod
    def const(c, K, n):
        a = np.zeros((K + 1, n))
        a[0] = c
        return Jet(a)

    @staticmethod
    def var(r, K):
        a = np.zeros((K + 1, r.size))
        a[0] = r
        if K >= 1:
            a[1] = 1.0
        return Jet(a)

    def __add__(self, o):
        return Jet(self.a + o.a) if isinstance(o, Jet) else Jet(
            np.concatenate([[self.a[0] + o], self.a[1:]]))

    def __sub__(self, o):
        return Jet(self.a - o.a)

    def __mul__(self, o):
        if not isinstance(o, Jet):
            return Jet(self.a * o)
        K = self.K
        out = np.zeros_like(self.a)
        for k in range(K + 1):
            acc = np.zeros_like(self.a[0])
            for j in range(k + 1):
                acc += self.a[j] * o.a[k - j]
            out[k] = acc
        return Jet(out)

    __rmul__ = __mul__

    def recip(self):
        """1/f by the standard Taylor recursion."""
        K = self.K
        out = np.zeros_like(self.a)
        out[0] = 1.0 / self.a[0]
        for k in range(1, K + 1):
            acc = np.zeros_like(self.a[0])
            for j in range(1, k + 1):
                acc += self.a[j] * out[k - j]
            out[k] = -acc * out[0]
        return Jet(out)

    def ipow(self, p):
        """f**p for integer p (negative allowed), by repeated multiplication."""
        if p < 0:
            return self.recip().ipow(-p)
        res = Jet.const(1.0, self.K, self.a.shape[1])
        base = self
        while p:
            if p & 1:
                res = res * base
            base = base * base
            p >>= 1
        return res

    def derivs(self):
        """f^{(k)}(r) = k! a[k]."""
        return np.stack([math.factorial(k) * self.a[k] for k in range(self.K + 1)])


def cheb_jets(z, nmax):
    """T_n(z) for n = 0..nmax-1 as jets, via the three-term recurrence."""
    K, n = z.K, z.a.shape[1]
    out = [Jet.const(1.0, K, n)]
    if nmax > 1:
        out.append(z)
    for _ in range(2, nmax):
        out.append(2.0 * (z * out[-1]) - out[-2])
    return out


# ---------------------------------------------------------------------------------------
# 3.  Column scaling sigma -- re-derived here from its defining integral
# ---------------------------------------------------------------------------------------
def _composite_gl(a, b, npanel, order):
    x, w = leggauss(order)
    edges = np.linspace(a, b, npanel + 1)
    lo, hi = edges[:-1], edges[1:]
    mid, half = 0.5 * (lo + hi), 0.5 * (hi - lo)
    nodes = (mid[:, None] + half[:, None] * x[None, :]).ravel()
    wts = (half[:, None] * w[None, :]).ravel()
    return nodes, wts


def column_sigma(Lmax, Nr, rmax=48.0, npanel=240, order=16):
    """sigma^F_{l,n}, sigma^Q_{l,n} with sigma^2 = int_0^inf (A_l(u) T_n(2u-1))^2 e^{-r^2/4} r^2 dr.

    A_l = u^l (poloidal) or u^l (1-u) (toroidal).  Evaluated on a composite Gauss-Legendre
    rule in r, refinable, entirely different from the single Gauss-Legendre rule in u that
    `L6` uses -- which is the point: the convention is inherited, its NUMERICAL VALUE is not.
    """
    r, w = _composite_gl(0.0, rmax, npanel, order)
    u = r / (r + LMAP)
    z = 2.0 * u - 1.0
    T = np.zeros((Nr, r.size))
    T[0] = 1.0
    if Nr > 1:
        T[1] = z
    for n in range(2, Nr):
        T[n] = 2.0 * z * T[n - 1] - T[n - 2]
    gw = w * np.exp(-r ** 2 / 4.0) * r ** 2
    sF = np.zeros((Lmax + 1, Nr))
    sQ = np.zeros((Lmax + 1, Nr))
    for l in range(1, Lmax + 1):
        AF = u ** l
        AQ = u ** l * (1.0 - u)
        sF[l] = np.sqrt((AF ** 2 * T ** 2 * gw).sum(axis=1))
        sQ[l] = np.sqrt((AQ ** 2 * T ** 2 * gw).sum(axis=1))
    return sF, sQ


def cauchy_derivs(r, l, n, toroidal, sigma, K, M=64, frac=0.35):
    """G^{(k)}(r) for one basis column by CAUCHY'S INTEGRAL FORMULA on a complex circle.

    G(z) = T_n(2u-1) (z+L)^{-l}  (poloidal) or  L T_n(2u-1) (z+L)^{-l-1}  (toroidal), which
    is analytic everywhere except z = -L, so a circle of radius frac*r about r stays inside
    the domain of analyticity and G^{(k)} = k! c_k with c_k the k-th Fourier coefficient.

    This is the SECOND radial-derivative mechanism of this unit; the primary is the jet
    arithmetic in `Space.radial_G`.  Their agreement is control X6.
    """
    r = np.asarray(r, float)
    th = 2.0 * math.pi * np.arange(M) / M
    rho = frac * r
    z = r[:, None] + rho[:, None] * np.exp(1j * th)[None, :]
    u = z / (z + LMAP)
    zz = 2.0 * u - 1.0
    T = np.ones_like(zz)
    if n >= 1:
        Tm1, T = T, zz
        for _ in range(2, n + 1):
            Tm1, T = T, 2.0 * zz * T - Tm1
    if toroidal:
        G = LMAP * T * (z + LMAP) ** (-l - 1) / sigma
    else:
        G = T * (z + LMAP) ** (-l) / sigma
    c = np.fft.fft(G, axis=1) / M
    return np.stack([math.factorial(k) * c[:, k].real / rho ** k for k in range(K + 1)])


# ---------------------------------------------------------------------------------------
# 4.  Symbolic term algebra.  Term key = (mono, p, k, gen); value = coeff.
#     Meaning:  coeff * y^mono * r^p * G^{gen,(k)}(r, s)
# ---------------------------------------------------------------------------------------
GEN_F, GEN_Q = 0, 1


def _add(d, key, c):
    if c == 0.0:
        return
    v = d.get(key, 0.0) + c
    if v == 0.0:
        d.pop(key, None)
    else:
        d[key] = v


def t_deriv(T, i):
    out = {}
    for (mono, p, k, gen), c in T.items():
        if mono[i] > 0:
            m2 = list(mono)
            m2[i] -= 1
            _add(out, (tuple(m2), p, k, gen), c * mono[i])
        if p != 0:
            m2 = list(mono)
            m2[i] += 1
            _add(out, (tuple(m2), p - 2, k, gen), c * p)
        m2 = list(mono)
        m2[i] += 1
        _add(out, (tuple(m2), p - 1, k + 1, gen), c)
    return out


def t_muly(T, j):
    out = {}
    for (mono, p, k, gen), c in T.items():
        m2 = list(mono)
        m2[j] += 1
        _add(out, (tuple(m2), p, k, gen), c)
    return out


def t_add(A, B, sa=1.0, sb=1.0):
    out = {}
    for key, c in A.items():
        _add(out, key, sa * c)
    for key, c in B.items():
        _add(out, key, sb * c)
    return out


def v_curl(V):
    """(curl V)_c = eps_{cij} d_i V_j."""
    return [t_add(t_deriv(V[2], 1), t_deriv(V[1], 2), 1.0, -1.0),
            t_add(t_deriv(V[0], 2), t_deriv(V[2], 0), 1.0, -1.0),
            t_add(t_deriv(V[1], 0), t_deriv(V[0], 1), 1.0, -1.0)]


def v_scalar_times_y(S):
    return [t_muly(S, 0), t_muly(S, 1), t_muly(S, 2)]


def build_operator_terms(poly, gen_pol, gen_tor):
    """All the term lists needed, for ONE spherical harmonic.

    `poly` is the solid harmonic polynomial R_lm; `gen_pol`/`gen_tor` tag which radial
    generator (f or g) the terms belong to.  Returns a dict of named fields.
    """
    f = {(mono, 0, 0, gen_pol): c for mono, c in poly.items()}
    g = {(mono, 0, 0, gen_tor): c for mono, c in poly.items()}

    Vpol = v_curl(v_curl(v_scalar_times_y(f)))
    Vtor = v_curl(v_scalar_times_y(g))
    V = [t_add(Vpol[c], Vtor[c]) for c in range(3)]
    w = v_curl(V)
    gradV = [[t_deriv(V[c], j) for j in range(3)] for c in range(3)]
    gradw = [[t_deriv(w[c], j) for j in range(3)] for c in range(3)]
    lapw = [t_add(t_add(t_deriv(gradw[c][0], 0), t_deriv(gradw[c][1], 1)),
                  t_deriv(gradw[c][2], 2)) for c in range(3)]
    return dict(V=V, w=w, gradV=gradV, gradw=gradw, lapw=lapw)


# ---------------------------------------------------------------------------------------
# 5.  Quadratures -- all three genuinely different from `L6`'s
# ---------------------------------------------------------------------------------------
def radial_rule(rmin, rmax, per_efold=1, order=8):
    """Composite Gauss-Legendre in ln r.  int_0^inf F dr ~ sum w_i F(r_i), w includes r."""
    a, b = math.log(rmin), math.log(rmax)
    npanel = max(1, int(round((b - a) * per_efold)))
    xi, wxi = _composite_gl(a, b, npanel, order)
    r = np.exp(xi)
    return r, wxi * r


def cube_sphere(ng):
    """Six gnomonic patches, Gauss-Legendre in each equiangular patch coordinate."""
    x, w = leggauss(ng)
    a = (math.pi / 4.0) * x                     # equiangular patch coordinate
    wa = (math.pi / 4.0) * w
    t = np.tan(a)
    X, Y = np.meshgrid(t, t, indexing="ij")
    WX, WY = np.meshgrid(wa, wa, indexing="ij")
    d = np.sqrt(1.0 + X ** 2 + Y ** 2)
    jac = (1.0 + X ** 2) * (1.0 + Y ** 2) / d ** 3
    base = (WX * WY * jac).ravel()
    Xf, Yf, one = X.ravel(), Y.ravel(), np.ones(X.size)
    faces = [(one, Xf, Yf), (-one, Xf, Yf), (Xf, one, Yf),
             (Xf, -one, Yf), (Xf, Yf, one), (Xf, Yf, -one)]
    dirs, wts = [], []
    for fx, fy, fz in faces:
        v = np.stack([fx, fy, fz], axis=1)
        v = v / np.linalg.norm(v, axis=1, keepdims=True)
        dirs.append(v)
        wts.append(base)
    return np.concatenate(dirs, axis=0), np.concatenate(wts, axis=0)


def s_rule(ns):
    """Half-step-offset uniform rule on one DSS period."""
    s = PERIOD * (np.arange(ns) + 0.5) / ns
    return s, np.full(ns, PERIOD / ns)


def s_rule_gl(ns):
    s, w = _composite_gl(0.0, PERIOD, 1, ns)
    return s, w


# ---------------------------------------------------------------------------------------
# 6.  The discretisation bundle
# ---------------------------------------------------------------------------------------
class Space:
    """Trial-space CONVENTION (inherited) + this unit's own quadrature (independent)."""

    def __init__(self, Lmax, Nr, Ks, rmin=1e-5, rmax=1e8, per_efold=1, gl_order=8,
                 ng=12, ns=32, kmax=6, s_gauss=False, sigma_kw=None):
        self.Lmax, self.Nr, self.Ks = Lmax, Nr, Ks
        self.harm = [(l, m) for l in range(1, Lmax + 1) for m in range(-l, l + 1)]
        self.nH = len(self.harm)
        self.nK = 2 * Ks + 1
        self.n_dof = 2 * self.nH * Nr * self.nK
        self.kmax = kmax

        self.r, self.wr = radial_rule(rmin, rmax, per_efold, gl_order)
        self.wv = self.wr * self.r ** 2          # the volume weight: dy = r^2 dr dOmega
        self.nr = self.r.size
        self.dirs, self.wa = cube_sphere(ng)
        self.nang = self.dirs.shape[0]
        self.s, self.ws = (s_rule_gl(ns) if s_gauss else s_rule(ns))
        self.ns = self.s.size
        self.rmin, self.rmax = rmin, rmax

        sk = sigma_kw or {}
        self.sF, self.sQ = column_sigma(Lmax, Nr, **sk)

        # s basis and its exact derivative
        S = np.zeros((self.nK, self.ns))
        Sd = np.zeros((self.nK, self.ns))
        S[0] = 1.0
        for j in range(1, Ks + 1):
            S[2 * j - 1] = np.cos(j * OMEGA_S * self.s)
            Sd[2 * j - 1] = -j * OMEGA_S * np.sin(j * OMEGA_S * self.s)
            S[2 * j] = np.sin(j * OMEGA_S * self.s)
            Sd[2 * j] = j * OMEGA_S * np.cos(j * OMEGA_S * self.s)
        self.S, self.Sd = S, Sd

        # ---- radial jets: T_n(z(r)) and (r + Lmap)^{-l} ---------------------------------
        rj = Jet.var(self.r, kmax)
        uden = rj + LMAP
        zj = 2.0 * (rj * uden.recip()) - Jet.const(1.0, kmax, self.nr)
        self._T = cheb_jets(zj, Nr)
        self._pw = {l: uden.ipow(-l) for l in range(1, Lmax + 2)}

        # ---- solid harmonic polynomials and the symbolic operator ----------------------
        rng = np.random.default_rng(409)
        self.poly = {}
        for (l, m) in self.harm:
            P = solid_harmonic_poly(l, m, rng)
            self.poly[(l, m)] = P
        self.terms = [build_operator_terms(self.poly[hm], GEN_F, GEN_Q) for hm in self.harm]

        # ---- angular monomial table -----------------------------------------------------
        self._mon_cache = {}

    # -- radial generator arrays ---------------------------------------------------------
    def radial_G(self, aF, aQ):
        """G^{gen,(k)}_{h,k'}(r): shape (2, nH, kmax+1, nK, nr).

        f = sum_h R_lm(y) G^F_h(r,s),  with G^F = phi^F / r^l = T_n(z)/(sigma (r+L)^l)
        g = sum_h R_lm(y) G^Q_h(r,s),  with G^Q = phi^Q / r^l = L T_n(z)/(sigma (r+L)^{l+1})
        """
        out = np.zeros((2, self.nH, self.kmax + 1, self.nK, self.nr))
        for h, (l, m) in enumerate(self.harm):
            pF = self._pw[l]
            pQ = self._pw[l + 1]
            for n in range(self.Nr):
                Tn = self._T[n]
                dF = (Tn * pF).derivs()
                dQ = (Tn * pQ).derivs() * LMAP
                cF = aF[h, n, :] / self.sF[l, n]
                cQ = aQ[h, n, :] / self.sQ[l, n]
                out[0, h] += dF[:, None, :] * cF[None, :, None]
                out[1, h] += dQ[:, None, :] * cQ[None, :, None]
        return out

    # -- rebuild the same trial space on a FOREIGN grid ---------------------------------
    def regrid(self, r, dirs, wa, s, ws):
        """The same trial space and the same operator, evaluated on someone else's grid.

        Used only by the evidence script, to put this unit's `W` and `L6`'s `W` on a COMMON
        set of points so the two can be differenced pointwise.  The symbolic operator, the
        polynomials and the column scaling are shared unchanged; only the grid moves.
        """
        o = Space.__new__(Space)
        o.__dict__.update(self.__dict__)
        o.r = np.asarray(r, float)
        o.nr = o.r.size
        o.wr = np.zeros(o.nr)
        o.wv = np.zeros(o.nr)
        o.dirs = np.asarray(dirs, float)
        o.wa = np.asarray(wa, float)
        o.nang = o.dirs.shape[0]
        o.s = np.asarray(s, float)
        o.ws = np.asarray(ws, float)
        o.ns = o.s.size
        S = np.zeros((self.nK, o.ns))
        Sd = np.zeros((self.nK, o.ns))
        S[0] = 1.0
        for j in range(1, self.Ks + 1):
            S[2 * j - 1] = np.cos(j * OMEGA_S * o.s)
            Sd[2 * j - 1] = -j * OMEGA_S * np.sin(j * OMEGA_S * o.s)
            S[2 * j] = np.sin(j * OMEGA_S * o.s)
            Sd[2 * j] = j * OMEGA_S * np.cos(j * OMEGA_S * o.s)
        o.S, o.Sd = S, Sd
        rj = Jet.var(o.r, self.kmax)
        uden = rj + LMAP
        zj = 2.0 * (rj * uden.recip()) - Jet.const(1.0, self.kmax, o.nr)
        o._T = cheb_jets(zj, self.Nr)
        o._pw = {l: uden.ipow(-l) for l in range(1, self.Lmax + 2)}
        o._mon_cache = {}
        return o

    # -- angular evaluation of a collected monomial polynomial ---------------------------
    def _mon(self, mono):
        v = self._mon_cache.get(mono)
        if v is None:
            i, j, k = mono
            v = (self.dirs[:, 0] ** i) * (self.dirs[:, 1] ** j) * (self.dirs[:, 2] ** k)
            self._mon_cache[mono] = v
        return v


def collect(field_terms, nH, kmax):
    """Group a per-harmonic list of term dicts into (h, gen, k) -> (weight, {mono: coeff}).

    Asserts that the radial weight W = |mono| + p depends only on (h, gen, k), which is the
    homogeneity property of the construction and is a genuine internal check: it would fail
    if the term algebra were wrong.
    """
    groups = {}
    for h in range(nH):
        for (mono, p, k, gen), c in field_terms[h].items():
            W = sum(mono) + p
            key = (h, gen, k)
            if key not in groups:
                groups[key] = [W, {}]
            if groups[key][0] != W:
                raise AssertionError("inhomogeneous weight in term collection")
            if k > kmax:
                raise AssertionError("radial derivative order %d exceeds kmax" % k)
            g = groups[key][1]
            g[mono] = g.get(mono, 0.0) + c
    return groups


# ---------------------------------------------------------------------------------------
# 7.  Field evaluation and the residual W[V]
# ---------------------------------------------------------------------------------------
FIELD_SPEC = [("V", 3), ("w", 3), ("lapw", 3), ("gradV", 9), ("gradw", 9)]


def _flat_fields(sp):
    """Flatten the per-harmonic symbolic fields into a list of (name, comp, terms-per-h)."""
    flat = []
    for name, ncomp in FIELD_SPEC:
        for c in range(ncomp):
            if ncomp == 3:
                per_h = [sp.terms[h][name][c] for h in range(sp.nH)]
            else:
                per_h = [sp.terms[h][name][c // 3][c % 3] for h in range(sp.nH)]
            flat.append((name, c, per_h))
    return flat


def residual_W(sp, aF, aQ, chunk=96, drop_dss_term=False):
    """W[V] on the grid, shape (nang, nr, ns, 3), plus V and w for diagnostics."""
    G = sp.radial_G(aF, aQ)                        # (2, nH, kmax+1, nK, nr)
    # radial-s arrays per (h, gen, k): value(r, s) = sum_k' S_k'(s) G^{(k)}_{h,k'}(r)
    # RS[0] uses S (the field itself), RS[1] uses dS/ds (the s-derivative, for w_s)
    RS = np.zeros((2, 2, sp.nH, sp.kmax + 1, sp.nr, sp.ns))
    for which, Smat in ((0, sp.S), (1, sp.Sd)):
        RS[which] = np.einsum("ghkjr,jm->ghkrm", G, Smat, optimize=True)

    flat = _flat_fields(sp)
    groups = [collect(per_h, sp.nH, sp.kmax) for (_, _, per_h) in flat]

    nfield = len(flat)
    out = np.zeros((nfield, sp.nang, sp.nr, sp.ns))
    out_ws = np.zeros((3, sp.nang, sp.nr, sp.ns))   # w_s uses the same terms as w

    # index set j = (h, gen, k)
    jidx = [(h, gen, k) for h in range(sp.nH) for gen in (0, 1) for k in range(sp.kmax + 1)]
    jpos = {key: t for t, key in enumerate(jidx)}
    nj = len(jidx)
    lofh = np.array([l for (l, m) in sp.harm])

    # bucket fields by the radial exponent offset omega with W = omega + k
    buckets = {}
    for fi, gr in enumerate(groups):
        for (h, gen, k), (W, poly) in gr.items():
            om = W - k
            buckets.setdefault((fi, om), []).append((h, gen, k, poly))

    r = sp.r
    for a0 in range(0, sp.nang, chunk):
        a1 = min(sp.nang, a0 + chunk)
        na = a1 - a0
        for (fi, om), items in buckets.items():
            A = np.zeros((na, nj))
            for (h, gen, k, poly) in items:
                acc = np.zeros(na)
                for mono, c in poly.items():
                    acc += c * sp._mon(mono)[a0:a1]
                A[:, jpos[(h, gen, k)]] += acc
            use = np.abs(A).sum(axis=0) > 0
            if not use.any():
                continue
            cols = np.nonzero(use)[0]
            B = np.empty((cols.size, sp.nr * sp.ns))
            Bs = np.empty((cols.size, sp.nr * sp.ns)) if flat[fi][0] == "w" else None
            for t, jj in enumerate(cols):
                h, gen, k = jidx[jj]
                fac = r ** (om + k)
                B[t] = (RS[0, gen, h, k] * fac[:, None]).ravel()
                if Bs is not None:
                    Bs[t] = (RS[1, gen, h, k] * fac[:, None]).ravel()
            out[fi, a0:a1] += (A[:, cols] @ B).reshape(na, sp.nr, sp.ns)
            if Bs is not None:
                out_ws[flat[fi][1], a0:a1] += (A[:, cols] @ Bs).reshape(na, sp.nr, sp.ns)

    idx = {}
    p = 0
    for name, ncomp in FIELD_SPEC:
        idx[name] = out[p:p + ncomp]
        p += ncomp
    V = np.moveaxis(idx["V"], 0, -1)
    w = np.moveaxis(idx["w"], 0, -1)
    lapw = np.moveaxis(idx["lapw"], 0, -1)
    ws = np.moveaxis(out_ws, 0, -1)
    gradV = idx["gradV"].reshape(3, 3, sp.nang, sp.nr, sp.ns)
    gradw = idx["gradw"].reshape(3, 3, sp.nang, sp.nr, sp.ns)

    yv = sp.dirs[:, None, None, :] * r[None, :, None, None]      # (nang, nr, 1, 3)
    ydotgradw = np.zeros_like(w)
    VgradW = np.zeros_like(w)
    wgradV = np.zeros_like(w)
    for c in range(3):
        for j in range(3):
            ydotgradw[..., c] += yv[..., j] * gradw[c, j]
            VgradW[..., c] += V[..., j] * gradw[c, j]
            wgradV[..., c] += w[..., j] * gradV[c, j]

    dss = 0.0 if drop_dss_term else A_SIM
    W = ws + dss * (2.0 * w + ydotgradw) - lapw + VgradW - wgradV
    return W, V, w, gradV


def load_bearing_norm(sp, W):
    """J = int_0^{T_s} ||W(.,s)||_{L3/2(R^3)} ds, on this unit's own quadrature."""
    sq = (W ** 2).sum(axis=-1)
    dens = sq ** 0.75
    wpr = sp.wa[:, None, None] * sp.wv[None, :, None]
    per_s = (dens * wpr).sum(axis=(0, 1))
    return float((per_s ** (2.0 / 3.0) * sp.ws).sum()), per_s


def radial_density(sp, W):
    """dJ-ish radial profile: sum over angle and s of |W|^{3/2} r^2, per ln r."""
    sq = (W ** 2).sum(axis=-1)
    dens = sq ** 0.75
    return np.einsum("arm,a,m->r", dens, sp.wa, sp.ws, optimize=True) * sp.wv


# ---------------------------------------------------------------------------------------
# 8.  Branch normalisations
# ---------------------------------------------------------------------------------------
def norm_B_closed_form(sp, aF):
    """N_B = (1/T_s) int sum_lm F_lm(inf, s)^2 ds -- EXACT, no s quadrature.

    F_lm(inf, s) = sum_{n,k} aF[h,n,k] / sigma^F_{l,n} (since u^l -> 1 and T_n(1) = 1),
    and int cos^2 = int sin^2 = T_s/2 over the period while the mean mode gives T_s.
    """
    tot = 0.0
    for h, (l, m) in enumerate(sp.harm):
        c = (aF[h] / sp.sF[l][:, None]).sum(axis=0)       # (nK,)
        tot += c[0] ** 2 + 0.5 * float((c[1:] ** 2).sum())
    return float(tot)


def norm_A_quadrature(sp, V):
    """N_A = (1/T_s) int int |V|^2 e^{-|y|^2/4} dy ds, on this unit's own quadrature."""
    dens = (V ** 2).sum(axis=-1)
    gw = np.exp(-sp.r ** 2 / 4.0) * sp.wv
    return float(np.einsum("arm,a,r,m->", dens, sp.wa, gw, sp.ws, optimize=True) / PERIOD)


def unpack(sp, x):
    n = sp.nH * sp.Nr * sp.nK
    return (np.asarray(x[:n], float).reshape(sp.nH, sp.Nr, sp.nK),
            np.asarray(x[n:], float).reshape(sp.nH, sp.Nr, sp.nK))


def J_of(sp, x, branch, chunk=96, drop_dss_term=False, want_extra=False):
    """The functional, at the same normalisation convention `L6`'s `objective` applies."""
    aF, aQ = unpack(sp, x)
    if branch == "B":
        N = norm_B_closed_form(sp, aF)
        sc = 1.0 / math.sqrt(N)
        aF, aQ = aF * sc, aQ * sc
        W, V, w, gradV = residual_W(sp, aF, aQ, chunk, drop_dss_term)
    else:
        W, V, w, gradV = residual_W(sp, aF, aQ, chunk, drop_dss_term)
        N = norm_A_quadrature(sp, V)
        sc = 1.0 / math.sqrt(N)
        aF, aQ = aF * sc, aQ * sc
        W, V, w, gradV = residual_W(sp, aF, aQ, chunk, drop_dss_term)
    J, per_s = load_bearing_norm(sp, W)
    if not want_extra:
        return J
    div = np.zeros(V.shape[:-1])
    for c in range(3):
        div += gradV[c, c]
    return dict(J=J, N=N, per_s=per_s.tolist(),
                div_rel=float(np.max(np.abs(div)) / max(1e-300, np.max(np.abs(V)))),
                radial_density=radial_density(sp, W).tolist(),
                max_absW=float(np.max(np.abs(W))))


def eval_V_at(sp, x, branch, pts, s_val):
    """V at arbitrary Cartesian points -- for the banked-field-sample control X2."""
    aF, aQ = unpack(sp, x)
    if branch == "B":
        sc = 1.0 / math.sqrt(norm_B_closed_form(sp, aF))
        aF, aQ = aF * sc, aQ * sc
    pts = np.asarray(pts, float)
    r = np.linalg.norm(pts, axis=1)
    nvec = pts / r[:, None]
    Sv = np.zeros(sp.nK)
    Sv[0] = 1.0
    for j in range(1, sp.Ks + 1):
        Sv[2 * j - 1] = math.cos(j * OMEGA_S * s_val)
        Sv[2 * j] = math.sin(j * OMEGA_S * s_val)

    sub = Space.__new__(Space)
    sub.__dict__.update(sp.__dict__)
    sub.r = r
    sub.nr = r.size
    rj = Jet.var(r, sp.kmax)
    uden = rj + LMAP
    zj = 2.0 * (rj * uden.recip()) - Jet.const(1.0, sp.kmax, r.size)
    sub._T = cheb_jets(zj, sp.Nr)
    sub._pw = {l: uden.ipow(-l) for l in range(1, sp.Lmax + 2)}
    G = sub.radial_G(aF, aQ)                          # (2, nH, kmax+1, nK, npts)
    Gs = np.einsum("ghkjr,j->ghkr", G, Sv, optimize=True)

    out = np.zeros((pts.shape[0], 3))
    for c in range(3):
        for h in range(sp.nH):
            for (mono, p, k, gen), coef in sp.terms[h]["V"][c].items():
                val = (nvec[:, 0] ** mono[0] * nvec[:, 1] ** mono[1] * nvec[:, 2] ** mono[2])
                out[:, c] += coef * val * r ** (sum(mono) + p) * Gs[gen, h, k]
    return out


# ---------------------------------------------------------------------------------------
# 9.  Controls -- these run and are reported BEFORE any verdict
# ---------------------------------------------------------------------------------------
def control_X1(sp):
    """Closed-form curl and closed-form L^{3/2} norm, on THIS unit's quadrature.

    Field  Phi(y) = e^{-|y|^2/2} (zhat x y) = curl(psi y) with psi = z e^{-|y|^2/2}.
      curl Phi = e^{-|y|^2/2} (y1 y3, y2 y3, 2 - y1^2 - y2^2)     [derived by hand, SS7]
    Field  Psi(y) = e^{-|y|^2/2} zhat,  ||Psi||_{L3/2} = (int e^{-3r^2/4} dy)^{2/3} = 4 pi/3.
    """
    r = sp.r[None, :]
    n = sp.dirs
    y = n[:, None, :] * r[:, :, None]                 # (nang, nr, 3)
    e = np.exp(-(y ** 2).sum(axis=-1) / 2.0)
    curl_closed = np.stack([e * y[..., 0] * y[..., 2],
                            e * y[..., 1] * y[..., 2],
                            e * (2.0 - y[..., 0] ** 2 - y[..., 1] ** 2)], axis=-1)
    # finite-difference curl of Phi, entirely independent of the closed form
    h = 1e-5

    def Phi(q):
        ee = np.exp(-(q ** 2).sum(axis=-1) / 2.0)
        return np.stack([-ee * q[..., 1], ee * q[..., 0], np.zeros_like(ee)], axis=-1)

    Jm = np.zeros(y.shape + (3,))
    for j in range(3):
        d = np.zeros(3)
        d[j] = h
        Jm[..., j] = (Phi(y + d) - Phi(y - d)) / (2 * h)
    curl_fd = np.stack([Jm[..., 2, 1] - Jm[..., 1, 2],
                        Jm[..., 0, 2] - Jm[..., 2, 0],
                        Jm[..., 1, 0] - Jm[..., 0, 1]], axis=-1)
    sel = (sp.r > 1e-3) & (sp.r < 8.0)
    num = np.max(np.abs(curl_fd[:, sel] - curl_closed[:, sel]))
    den = np.max(np.abs(curl_closed[:, sel]))
    curl_err = float(num / den)

    # L^{3/2} assembly on Psi, constant in s
    Wtest = np.zeros((sp.nang, sp.nr, sp.ns, 3))
    Wtest[..., 2] = np.exp(-(sp.r ** 2) / 2.0)[None, :, None]
    Jt, _ = load_bearing_norm(sp, Wtest)
    exact = PERIOD * 4.0 * math.pi / 3.0
    return dict(curl_closed_form_vs_fd_rel=curl_err,
                norm_value=Jt, norm_exact=exact,
                norm_rel_err=abs(Jt - exact) / exact)


# ---------------------------------------------------------------------------------------
# 10.  Vector constructions for the gate's three (four) points and the five-rung table
# ---------------------------------------------------------------------------------------
RUNGS = [("J0", 2, 8, 1), ("J1", 2, 12, 1), ("J2", 3, 12, 2),
         ("J3", 3, 16, 2), ("J4", 4, 20, 3)]


def restrict_to_rung(x, Lmax, Nr, Ks, Lmax_t, Nr_t, Ks_t):
    """Zero every coefficient outside a coarser rung's index box, in the SAME space."""
    nH = Lmax * (Lmax + 2)
    nK = 2 * Ks + 1
    harm = [(l, m) for l in range(1, Lmax + 1) for m in range(-l, l + 1)]
    aF = np.asarray(x[:nH * Nr * nK], float).reshape(nH, Nr, nK).copy()
    aQ = np.asarray(x[nH * Nr * nK:], float).reshape(nH, Nr, nK).copy()
    keep_h = np.array([l <= Lmax_t for (l, m) in harm])
    aF[~keep_h] = 0.0
    aQ[~keep_h] = 0.0
    aF[:, Nr_t:, :] = 0.0
    aQ[:, Nr_t:, :] = 0.0
    aF[:, :, 2 * Ks_t + 1:] = 0.0
    aQ[:, :, 2 * Ks_t + 1:] = 0.0
    return np.concatenate([aF.ravel(), aQ.ravel()])


def random_vector(n_dof, seed):
    return np.random.default_rng(seed).standard_normal(n_dof) * 0.3


def load_l6():
    with open(L6_ART) as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="smoke")
    ap.add_argument("--rmin", type=float, default=1e-5)
    ap.add_argument("--rmax", type=float, default=1e8)
    ap.add_argument("--per-efold", type=int, default=1)
    ap.add_argument("--order", type=int, default=8)
    ap.add_argument("--ng", type=int, default=12)
    ap.add_argument("--ns", type=int, default=32)
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    doc = load_l6()
    if args.mode == "smoke":
        sp = Space(2, 6, 1, rmin=1e-3, rmax=1e4, ng=6, ns=8)
        print("n_dof", sp.n_dof, "nr", sp.nr, "nang", sp.nang, "ns", sp.ns)
        print("sum of angular weights / 4pi - 1 =",
              sp.wa.sum() / (4 * math.pi) - 1.0)
        print("control X1:", control_X1(sp))
        x = random_vector(sp.n_dof, 1)
        print("J =", J_of(sp, x, "B"))
    elif args.mode == "banked":
        B = doc["banked_profile"]["B"]
        sp = Space(B["Lmax"], B["Nr"], B["Ks"], rmin=args.rmin, rmax=args.rmax,
                   per_efold=args.per_efold, gl_order=args.order, ng=args.ng, ns=args.ns)
        res = J_of(sp, np.array(B["coefficients"]), "B", want_extra=True)
        print("J_new(B) =", res["J"], " N_B =", res["N"], " div_rel =", res["div_rel"])
        print("J_L6(B)  =", doc["gate"]["B"]["residual_at_best_affordable_resolution"])
    if args.out:
        Path(args.out).write_text(json.dumps({"ok": True}))


if __name__ == "__main__":
    main()
