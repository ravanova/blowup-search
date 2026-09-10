"""Arc 6, unit R5(i) (leg 430): the leading-order profile, built from the paper's schedule.

    .venv/bin/python experiments/arc6_profile_v1.py             # full run, writes the artefact
    .venv/bin/python experiments/arc6_profile_v1.py --quick     # one lambda, coarser grid, no artefact

PRE-REGISTRATION: experiments/journal/leg_430_prereg.md, committed at e01a64d
BEFORE this file existed. Nine gates G1-G9 with the paper's numbers, five
planted controls, parameters in the order (A.6).

WHAT IS BUILT. Lemma 4.8's outer reference profile (Appendix A.2 of the OpenAI
manuscript, sha256 0e779481..., pinned leg 417), in the paper's own variables:
on the logarithmic radius y = log(X/X_R) and the axial parameter eta, the
logarithmic slope l = X d_X log H is prescribed stage by stage; E follows from
log E = int (l - 1/2) dy; U is prescribed (4 eta, the axial cutoff, the pulse
E R_b, then zero); the five cumulative integrals (4.15) are carried as the
normalised ratios M/X, I/(XH), J/(XH), S/(X E^2); Pi is normalised to vanish at
infinity (4.25); Q_s, N_s come from the explicit formulas (4.16) with spectral
eta-derivatives; a, b_s, p_s from (4.11); the cone tests from (4.20)-(4.22) and
the sufficient test (A.24). The moments are closed as in A.3: c_1, c_2 from
M = J = 0 at pulse end, Amp(eta) from S(inf) = 0 on the bracket [.9, 1.2], the
two (A.11) bumps from I = XH/(1-lambda) and zero pressure increment, the
exterior -h hold from Q_s reaching Q_p.

CEILING: float64, a fixed grid, one instance. Tier 2. Not a proof; verifies
nothing about the theorem; moves no wall.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "arc6_profile_v1.json"
PDF_SHA = "0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f"


# ------------------------------------------------------------------ the smooth step (A.5)
def sigma(y):
    y = np.asarray(y, dtype=float)
    out = np.zeros_like(y)
    inside = (y > 0) & (y < 1)
    yi = y[inside]
    a = np.exp(-1.0 / yi ** 2)
    b = np.exp(-1.0 / (1.0 - yi) ** 2)
    out[inside] = a / (a + b)
    out[y >= 1] = 1.0
    return out


def dsigma(y, h=1e-5):
    return (sigma(y + h) - sigma(y - h)) / (2 * h)


SIGMA_PRIME_MAX = float(np.max(dsigma(np.linspace(0.01, 0.99, 9801))))


def bump(y, center, width):
    """A positive bump: a rescaled copy of sigma' on [center - width/2, center + width/2]."""
    return dsigma((y - center) / width + 0.5) / width


# ------------------------------------------------------------------ Chebyshev in eta
def cheb(n):
    """Chebyshev-Gauss-Lobatto points on [-1, 1] and the differentiation matrix (Trefethen)."""
    k = np.arange(n + 1)
    x = np.cos(np.pi * k / n)
    c = np.ones(n + 1); c[0] = c[-1] = 2.0; c *= (-1.0) ** k
    X = np.tile(x, (n + 1, 1)).T
    dX = X - X.T
    D = np.outer(c, 1.0 / c) / (dX + np.eye(n + 1))
    D -= np.diag(D.sum(axis=1))
    return x[::-1], D[::-1, ::-1]  # ascending eta (reordering does not change the sign of d/deta)


# ------------------------------------------------------------------ the schedule
class Schedule:
    """Stage boundaries in y (y = 0 at x = X/X_R = 1) and the prescribed l, U, log E."""

    def __init__(self, Md, lam, h, T_f, c_o, flip_lambda=False, R0_cut=10.0):
        self.Md, self.lam, self.h, self.T_f, self.c_o = Md, lam, h, T_f, c_o
        self.T_d = np.exp(Md) + 10.0
        self.P_star = 2.0 * np.exp(self.T_d)
        self.T_w = 60.0 * np.log(1.0 / lam)
        self.lam_int = -lam if flip_lambda else lam   # C1 control flips the sign
        self.R0_cut = R0_cut                            # C6 control truncates R_0 at 5
        # order of choices (A.6): lambda after Md, T_d, P_*; h after lambda and e^{-T_d}
        assert self.P_star > np.exp(self.T_d), "(A.6): P_* > e^{T_d}"
        assert 0 < h < min(1.0 / 100, lam, np.exp(-self.T_d)), "(A.6)/Lemma 4.8: h < min{1/100, lambda, e^{-T_d}}"
        self.rho_o = c_o * h
        b = {}
        b["axl"] = 0.0
        b["axU"] = 1.0
        b["int1"] = b["axU"] + self.T_d
        b["int"] = b["int1"] + 1.0
        b["pulse"] = b["int"] + self.T_w
        b["interp"] = b["pulse"] + 13.0 / lam
        b["hold"] = b["interp"] + T_f
        b["ext1"] = b["hold"] + 30.0 * np.log(1.0 / lam)
        b["hold1"] = b["ext1"] + 1.0
        b["ext2"] = b["hold1"] + 4.0 * np.log(1.0 / h)
        b["holdh"] = b["ext2"] + 1.0
        self.b = b  # holdh length and tail start are fixed later from Q_p
        self.patches = [(b["int"] + self.T_w - 25, b["int"] + self.T_w - 20), (b["int"] + self.T_w - 20, b["int"] + self.T_w - 15),
                        (b["int"] + self.T_w - 14, b["int"] + self.T_w - 9), (b["int"] + self.T_w - 8, b["int"] + self.T_w - 3)]

    # ---- pieces
    def k_axial(self, yp):
        return 4.0 * (1.0 - sigma(np.log(1.0 + yp) / self.Md))

    def R0(self, xi):
        """R_0(xi) = phi_b(xi) [1 - sigma(xi - cut)], phi_b = int_0^xi sigma(v/.02) dv."""
        xi = np.asarray(xi, dtype=float)
        # phi_b: for xi >= .02 it equals xi - int_0^.02 (1 - sigma(v/.02)) dv = xi - .02 (1 - int_0^1 sigma) = xi - .01 by symmetry
        v = np.linspace(0, 1, 2001)
        m = np.trapezoid(sigma(v), v)  # = 1/2 by the step's symmetry
        phi = np.where(xi >= 0.02, xi - 0.02 * (1 - m), 0.0)
        small = (xi > 0) & (xi < 0.02)
        if small.any():
            xs = xi[small]
            phi[small] = np.array([np.trapezoid(sigma(np.linspace(0, x, 201) / 0.02), np.linspace(0, x, 201)) for x in xs])
        return phi * (1.0 - sigma(xi - self.R0_cut))

    def f_o(self, yt):
        psi = 1.0 - sigma((yt - 1.0) / 2.0)
        return 1.0 - self.rho_o * psi

    def l_and_U(self, y, eta, Amp=None, c12=None, cb=None, with_pulse_bumps=True):
        """Prescribed l(y) (eta-independent except in the interpolation) and U(y, eta) for y before the tail.
        Amp, c12 = (c1, c2) per eta, cb = (c1', c2') the (A.11) relative E bumps. Returns l (ny, neta), U (ny, neta),
        and logE (ny, neta) computed by integration where l is prescribed and directly where log E is."""
        b, lam = self.b, self.lam_int
        ny, ne = len(y), len(eta)
        l = np.zeros((ny, ne)); U = np.zeros((ny, ne))
        f = 1.0 / (1.0 + eta ** 2); J0 = np.log(1.0 + eta ** 2)
        st = self.stage_of(y)
        # axl
        m = st == "axl"; l[m] = (0.6 * (1 - sigma(y[m])))[:, None]; U[m] = 4.0 * eta[None, :]
        # axU
        m = st == "axU"; l[m] = 0.0; U[m] = (self.k_axial(y[m] - b["axU"]))[:, None] * eta[None, :]
        # int1, int
        m = st == "int1"; l[m] = (-lam * sigma(y[m] - b["int1"]))[:, None]
        m = st == "int"; l[m] = -lam
        # pulse (U needs E; filled after logE below)
        m = st == "pulse"; l[m] = -lam
        # interp: log E prescribed; l = 1/2 + d/dy log E
        # hold, ext1, hold1, ext2, holdh
        m = st == "hold"; l[m] = -lam
        m = st == "ext1"; l[m] = (-lam - (1 - lam) * sigma(y[m] - b["ext1"]))[:, None]
        m = st == "hold1"; l[m] = -1.0
        m = st == "ext2"; l[m] = (-1.0 + (1 - self.h) * sigma(y[m] - b["ext2"]))[:, None]
        m = st == "holdh"; l[m] = -self.h
        # log E by cumulative integration of (l - 1/2) from y = 0 (E(0) = P_* f)
        dy = y[1] - y[0]
        logE = np.zeros((ny, ne))
        logE[0] = np.log(self.P_star * f)
        # interpolation stage: prescribed
        mi = st == "interp"
        # integrate up to interp start
        # do a proper Simpson-consistent cumulative trapezoid on the FINE grid (dy is the fine step)
        incr = 0.5 * ((l[1:] - 0.5) + (l[:-1] - 0.5)) * np.diff(y)[:, None]   # variable step
        cum = np.vstack([np.zeros((1, ne)), np.cumsum(incr, axis=0)])
        logE = logE[0][None, :] + cum
        # interp: log E = log e_end - (1/2 + lam) y' - theta J0 - (1 - theta) log 2, with e_end = E/f at interp start
        if mi.any():
            i0 = np.argmax(mi)
            e_end = logE[i0] - np.log(f)           # log(e_end) per eta, equal across eta up to f
            yp = y[mi] - b["interp"]
            theta = 1.0 - sigma(yp / self.T_f)
            logE[mi] = (e_end[None, :] - (0.5 + lam) * yp[:, None] - theta[:, None] * J0[None, :]
                        - (1 - theta)[:, None] * np.log(2.0))
            # continue the integration after interp from its last value
            i1 = np.where(mi)[0][-1]
            if i1 + 1 < ny:
                logE[i1 + 1:] = logE[i1][None, :] + (cum[i1 + 1:] - cum[i1][None, :])
            # l on interp from the derivative of the prescribed log E (4th-order central)
            dlog = np.gradient(logE[:, :], y, axis=0, edge_order=2)
            l[mi] = 0.5 + dlog[mi]
        # (A.11) bumps on the hold: relative E bumps, width .3, centred 3 and 1 units before hold end
        if cb is not None:
            yh = y
            B1 = bump(yh, b["ext1"] - 3.0, 0.3); B2 = bump(yh, b["ext1"] - 1.0, 0.3)
            fac = 1.0 + cb[0][None, :] * B1[:, None] + cb[1][None, :] * B2[:, None]
            logE = logE + np.log(fac)
            dlog = np.gradient(np.log(fac), y, axis=0, edge_order=2)
            l = l + dlog
        # pulse U = E R_b
        mp = st == "pulse"
        if mp.any() and Amp is not None:
            yp = y[mp] - b["pulse"]
            xi = lam * yp if not np.isscalar(lam) else self.lam * yp
            R = Amp[None, :] * self.R0(xi)[:, None]
            if with_pulse_bumps and c12 is not None:
                B1 = bump(yp, 13.0 / self.lam - 3.0, 0.3); B2 = bump(yp, 13.0 / self.lam - 1.0, 0.3)
                R = R + c12[0][None, :] * B1[:, None] + c12[1][None, :] * B2[:, None]
            U[mp] = np.exp(logE[mp]) * R
        return l, U, logE

    def stage_of(self, y):
        b = self.b
        names = ["axl", "axU", "int1", "int", "pulse", "interp", "hold", "ext1", "hold1", "ext2", "holdh"]
        starts = [b[n] for n in names]
        idx = np.searchsorted(starts, y, side="right") - 1
        idx = np.clip(idx, 0, len(names) - 1)
        return np.array(names)[idx]


# ------------------------------------------------------------------ the build
def make_grid(segments):
    """Fine grid from (start, end, coarse_step) segments; every segment gets an even number of fine
    intervals so coarse points (even indices) land on segment boundaries and midpoints are exact."""
    pieces = []
    for k, (a, b, step) in enumerate(segments):
        n = max(2, int(np.ceil((b - a) / (step / 2.0))))
        if n % 2:
            n += 1
        seg = np.linspace(a, b, n + 1)
        pieces.append(seg if k == 0 else seg[1:])
    return np.concatenate(pieces)


def rk4_linear(y, g, c, r0):
    """Solve r' = g(y) - c(y) r on the coarse grid y[::2], variable step, given g, c on the fine grid."""
    n = (len(y) - 1) // 2
    r = np.zeros((n + 1,) + np.shape(r0))
    r[0] = r0
    for i in range(n):
        a, m, bb = 2 * i, 2 * i + 1, 2 * i + 2
        H = y[bb] - y[a]
        k1 = g[a] - c[a] * r[i]
        k2 = g[m] - c[m] * (r[i] + 0.5 * H * k1)
        k3 = g[m] - c[m] * (r[i] + 0.5 * H * k2)
        k4 = g[bb] - c[bb] * (r[i] + H * k3)
        r[i + 1] = r[i] + (H / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    return r


def rk4_linear_backward(y, gfun, c, r_end):
    """Solve r' = gfun(y) - c(y) r BACKWARD from y[-1] with r(y[-1]) = r_end; coarse-grid output."""
    n = (len(y) - 1) // 2
    r = np.zeros((n + 1,) + np.shape(r_end))
    r[n] = r_end
    for i in range(n, 0, -1):
        a, m, bb = 2 * i, 2 * i - 1, 2 * i - 2
        H = y[a] - y[bb]
        k1 = -(gfun[a] - c[a] * r[i])
        k2 = -(gfun[m] - c[m] * (r[i] + 0.5 * H * k1))
        k3 = -(gfun[m] - c[m] * (r[i] + 0.5 * H * k2))
        k4 = -(gfun[bb] - c[bb] * (r[i] + H * k3))
        r[i - 1] = r[i] + (H / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    return r


def simpson_cum(y, g):
    """Cumulative Simpson integral of g on the fine grid (variable step), returned on the coarse grid."""
    H = (y[2::2] - y[0:-2:2])
    inc = (H / 6.0).reshape((-1,) + (1,) * (g.ndim - 1)) * (g[0:-2:2] + 4 * g[1:-1:2] + g[2::2])
    return np.concatenate([np.zeros((1,) + g.shape[1:]), np.cumsum(inc, axis=0)], axis=0)


def simp_range(y, g, i0, i1):
    """Simpson integral of g over fine indices [i0, i1] (both even)."""
    yy, gg = y[i0:i1 + 1], g[i0:i1 + 1]
    H = (yy[2::2] - yy[0:-2:2]).reshape((-1,) + (1,) * (g.ndim - 1))
    return ((H / 6.0) * (gg[0:-2:2] + 4 * gg[1:-1:2] + gg[2::2])).sum(axis=0)


def build(Md=1.0, lam=0.1, h=1e-7, T_f=10.0, c_o=0.1, X_R=1e12, dy=2e-3, n_eta=24, pulse_step=None, P_star=None,
          flip_lambda=False, force_Amp=None, drop_c12=False, drop_A11=False, R0_cut=10.0, verbose=True):
    sch = Schedule(Md, lam, h, T_f, c_o, flip_lambda=flip_lambda, R0_cut=R0_cut)
    if P_star is not None:          # post-hoc exploration only: violates Lemma 4.8's P_* > e^{T_d}
        sch.P_star = P_star
    b, T_d, P_star = sch.b, sch.T_d, sch.P_star
    if pulse_step is None:
        pulse_step = max(dy, min(1.0, 0.002 / lam))   # the pulse ramp sigma(v/.02) has width .02/lambda in y
    A, D = 0.5 + h, 0.5 - h
    eta, Deta = cheb(n_eta)
    f = 1.0 / (1.0 + eta ** 2); d = 1.0 - eta ** 2; L = 1.0 - 2 * h * eta ** 2
    # --- the interpolation must keep -lam - .1 <= l <= -lam: T_f >= SIGMA'max log2 / .1
    T_f_min = SIGMA_PRIME_MAX * np.log(2.0) / 0.1
    # --- fine grid up to the end of ext2 (segmented: the pulse body is smooth on the scale 1/lambda and
    #     gets the coarser step `pulse_step`; the two end bumps of width .3 get the fine step); the -h hold
    #     length is decided from Q_p below
    y_end_pre = b["holdh"]
    cb1, cb2 = b["pulse"] + 13.0 / lam - 3.0, b["pulse"] + 13.0 / lam - 1.0
    segments = [(0.0, b["pulse"], dy), (b["pulse"], cb1 - 0.6, pulse_step), (cb1 - 0.6, cb2 + 0.6, dy), (cb2 + 0.6, b["interp"], dy),
                (b["interp"], y_end_pre, dy)]
    yf = make_grid(segments)
    yc = yf[::2]
    # --- first pass without pulse bumps / Amp: the eta-independent pieces of E
    #     Everything below is carried in LOG-SCALED form: X = X_R e^y overflows float64 beyond ~680 e-folds,
    #     and the paper's own schedule spans thousands at small lambda. lx = log X; every integral with an
    #     X-weight is taken relative to its own stage's scale (the paper normalises the same way, p. 131).
    lxR = np.log(X_R)
    l0, _, logE0 = sch.l_and_U(yf, eta, Amp=np.ones_like(eta), c12=None, with_pulse_bumps=False)
    E0 = np.exp(logE0)
    lx = lxR + yf                                   # log X on the fine grid
    lH0 = 0.5 * np.log(2.0) + 0.5 * lx[:, None] + logE0   # log H = log sqrt(2X) E
    # --- pulse closure: M = J = 0 at pulse end (affine in Amp, c1, c2), then S(inf) = 0 on [.9, 1.2]
    mp = sch.stage_of(yf) == "pulse"
    ip0, ip1 = np.where(mp)[0][0], np.where(mp)[0][-1]
    yp = yf[mp] - b["pulse"]
    R0 = sch.R0(lam * yp)
    B1 = bump(yp, 13.0 / lam - 3.0, 0.3); B2 = bump(yp, 13.0 / lam - 1.0, 0.3)
    # inner closed forms at y = 0 (x <= 1: U = 4 eta, E = P_* f x^{1/10})
    rM0 = 4.0 * eta                       # M/X
    rI0 = np.full_like(eta, 1.0 / 1.6)    # I/(XH)
    rJ0 = 4.0 * eta / 1.6                 # J/(XH)
    sS0 = 16 * eta ** 2 / (P_star * f) ** 2 - 1.0 / 2.4   # S/(X E^2)
    _, Upre, _ = sch.l_and_U(yf, eta, Amp=np.zeros_like(eta), c12=None, with_pulse_bumps=False)
    st_f = sch.stage_of(yf)
    axial = (st_f == "axl") | (st_f == "axU")
    UoE_pre = np.where(axial[:, None], Upre * np.exp(-np.where(axial[:, None], logE0, 0.0)), 0.0)   # U/E, log-safe (E is large on the axial stages)
    # moments normalised by E as well: rho_M = M/(XE) solves rho' = U/E - (l + 1/2) rho; rho_J = J/(XHE): rho' = U/E - (2l + 1/2) rho
    rhoM0 = rM0 / (P_star * f); rhoJ0 = rJ0 / (P_star * f)
    rhoM = rk4_linear(yf, UoE_pre, l0 + 0.5, rhoM0)
    rI = rk4_linear(yf, np.ones((len(yf), 1)), 1.0 + l0, rI0)
    rhoJ = rk4_linear(yf, UoE_pre, 2.0 * l0 + 0.5, rhoJ0)
    sS = rk4_linear(yf, UoE_pre ** 2 - 0.5, 2.0 * l0, sS0)
    ic0 = ip0 // 2
    ip1e = ip1 if ip1 % 2 == 0 else ip1 - 1
    # reference scales: the first bump centre for M, J (the paper's normalisation, p. 131); pulse start for S
    y_c1 = b["pulse"] + 13.0 / lam - 3.0
    lx_c1 = lxR + y_c1
    ic1 = int(np.searchsorted(yf, y_c1)); ic1 -= ic1 % 2
    lxp0 = lx[ip0]
    e_b = E0[ip0] / f                                     # E/f at pulse start (eta-independent)
    # the paper's normalisation (p. 131): each moment row in units of its integrand at the first bump centre,
    # M: E_c1 X_c1 (= X_p e_b f e^{s_1 (13/lam - 3)}),  J: E_c1 X_c1 H_c1
    lE_c1 = logE0[ic1]; lH_c1 = lH0[ic1]
    M_start_n = rhoM[ic0] * np.exp(logE0[ip0] + lxp0 - lx_c1 - lE_c1)
    J_start_n = rhoJ[ic0] * np.exp(logE0[ip0] + lH0[ip0] + lxp0 - lx_c1 - lE_c1 - lH_c1)
    S_start_n = sS[ic0] * E0[ip0] ** 2 / (e_b * f) ** 2 * lam
    def simp(g):  # Simpson over the pulse rows (fine, variable step)
        return simp_range(yf[ip0:ip1e + 1], g[:ip1e + 1 - ip0], 0, ip1e - ip0)
    wM = np.exp(logE0[mp] - lE_c1[None, :] + (lx[mp] - lx_c1)[:, None])
    wJ = wM * np.exp(lH0[mp] - lH_c1[None, :])
    mA, m1, m2 = simp(wM * R0[:, None]), simp(wM * B1[:, None]), simp(wM * B2[:, None])
    jA, j1, j2 = simp(wJ * R0[:, None]), simp(wJ * B1[:, None]), simp(wJ * B2[:, None])
    c0 = np.zeros((2, n_eta + 1)); cA = np.zeros((2, n_eta + 1))
    for k in range(n_eta + 1):
        Ak = np.array([[m1[k], m2[k]], [j1[k], j2[k]]])
        c0[:, k] = np.linalg.solve(Ak, -np.array([M_start_n[k], J_start_n[k]]))
        cA[:, k] = np.linalg.solve(Ak, -np.array([mA[k], jA[k]]))
    if drop_c12:
        c0[:] = 0.0; cA[:] = 0.0
    logebf = np.log(e_b * f)
    wS = lam * np.exp(2 * (logE0[mp] - logebf[None, :]) + (lx[mp] - lxp0)[:, None])      # = lam e^{-2 lam y'} on the pulse
    ia = ip1e
    iend_all = len(yf) - 1 if (len(yf) - 1) % 2 == 0 else len(yf) - 2
    S_after_n = -0.5 * lam * simp_range(yf, np.exp(2 * (logE0 - logebf[None, :]) + (lx - lxp0)[:, None]), ia, iend_all)
    def S_inf_n(Amp):
        R = Amp[None, :] * R0[:, None] + (c0[0] + Amp * cA[0])[None, :] * B1[:, None] + (c0[1] + Amp * cA[1])[None, :] * B2[:, None]
        return S_start_n + simp(wS * (R ** 2 - 0.5)) + S_after_n
    K_b = float(np.trapezoid(np.exp(-2 * lam * yp) * R0 ** 2, lam * yp))
    Pfun = lambda a: a ** 2 * K_b - (1 + np.exp(-26.0)) / 4.0
    if force_Amp is not None:
        Amp = np.full_like(eta, force_Amp)
    else:
        from scipy.optimize import brentq
        Amp = np.zeros_like(eta)
        for k in range(n_eta + 1):
            g = lambda a, k=k: S_inf_n(np.where(np.arange(n_eta + 1) == k, a, 1.0))[k]
            try:
                Amp[k] = brentq(g, 0.9, 1.2, xtol=1e-14, rtol=1e-14, maxiter=200)
            except ValueError:
                Amp[k] = np.nan
    Amp_eff = np.nan_to_num(Amp, nan=1.0)
    c12 = (c0[0] + Amp_eff * cA[0], c0[1] + Amp_eff * cA[1])
    if drop_c12:
        c12 = (np.zeros_like(eta), np.zeros_like(eta))
    S_res = S_inf_n(Amp_eff)
    S_pieces = {"S_start/norm": float(np.mean(S_start_n)), "S_pulse/norm_at_Amp1": float(np.mean(S_inf_n(np.ones_like(eta)) - S_start_n - S_after_n)), "S_after/norm": float(np.mean(S_after_n))}
    # --- second pass: fields with the pulse and (A.11) bumps
    l1, U1, logE1 = sch.l_and_U(yf, eta, Amp=Amp_eff, c12=c12, cb=None)
    lH1 = 0.5 * np.log(2.0) + 0.5 * lx[:, None] + logE1
    rI1 = rk4_linear(yf, np.ones((len(yf), 1)), 1.0 + l1, rI0)
    ih = int(np.searchsorted(yf[::2], b["ext1"]))
    if drop_A11:
        cb = (np.zeros_like(eta), np.zeros_like(eta))
    else:
        yh = yf; Bh1 = bump(yh, b["ext1"] - 3.0, 0.3); Bh2 = bump(yh, b["ext1"] - 1.0, 0.3)
        # the two bumps live in the last 3.5 units of the hold: integrate on that window only (the weights
        # e^{...} are O(1) there and overflow far away, where the bumps vanish anyway)
        iw0 = int(np.searchsorted(yf, b["ext1"] - 4.0)); iw0 -= iw0 % 2
        iw1 = 2 * ih
        full = lambda g: simp_range(yf, g, iw0, iw1)
        lxe, lHe = lx[2 * ih], lH1[2 * ih]
        wI = np.exp(lH1 - lHe[None, :] + (lx - lxe)[:, None])
        dI1 = full(wI * Bh1[:, None]); dI2 = full(wI * Bh2[:, None])
        target_I = 1.0 / (1 - lam) - rI1[ih]
        E2n = np.exp(2 * (logE1 - logE1[2 * ih][None, :]))
        p1 = full(E2n * Bh1[:, None]); p2 = full(E2n * Bh2[:, None])
        p11 = full(E2n * (Bh1 ** 2)[:, None]); p22 = full(E2n * (Bh2 ** 2)[:, None]); p12 = full(E2n * (Bh1 * Bh2)[:, None])
        cb = np.zeros((2, n_eta + 1))
        for it in range(30):
            c1, c2 = cb
            F1 = dI1 * c1 + dI2 * c2 - target_I
            F2 = p1 * c1 + p2 * c2 + 0.5 * (p11 * c1 ** 2 + p22 * c2 ** 2 + 2 * p12 * c1 * c2)
            J11, J12 = dI1, dI2
            J21, J22 = p1 + p11 * c1 + p12 * c2, p2 + p22 * c2 + p12 * c1
            det = J11 * J22 - J12 * J21
            d1 = (F1 * J22 - F2 * J12) / det; d2 = (J11 * F2 - J21 * F1) / det
            cb = np.array([c1 - d1, c2 - d2])
            if max(np.max(np.abs(d1)), np.max(np.abs(d2))) < 1e-16:
                break
        cb = (cb[0], cb[1])
    l2, U2, logE2 = sch.l_and_U(yf, eta, Amp=Amp_eff, c12=c12, cb=cb)
    rI = rk4_linear(yf, np.ones((len(yf), 1)), 1.0 + l2, rI0)
    Q_ext_start = -1.0 + (1 - h) * rI[int(np.searchsorted(yf[::2], b["ext1"]))]
    yt = np.linspace(0, 3, 30001)
    fo = sch.f_o(yt); fop = np.gradient(fo, yt, edge_order=2)
    Q_p = float(np.trapezoid(np.exp((1 - h) * yt) * fop / fo[0], yt))
    Q_hold_start = -1.0 + (1 - h) * rI[-1]
    Q_hold_start_e = float(np.mean(Q_hold_start))
    if Q_hold_start_e > Q_p > 0:
        T_hold = np.log(Q_hold_start_e / Q_p) / (1 - h)
    else:
        T_hold = 0.0
    y_tail0 = b["holdh"] + T_hold
    yf_ext = make_grid([(y_end_pre, y_tail0, dy), (y_tail0, y_tail0 + 4.0, dy)])[1:]
    yfa = np.concatenate([yf, yf_ext])
    lxa = lxR + yfa
    st_tail = yfa >= y_tail0
    ytt = np.clip(yfa - y_tail0, 0, None)
    fo_a = np.where(st_tail, sch.f_o(ytt), 1.0 - sch.rho_o)
    l_ext = np.full(len(yf_ext), -h)
    fo_e = fo_a[len(yf):]
    dfo = np.gradient(fo_e, yfa[len(yf):], edge_order=2)
    l_ext = l_ext + np.where(st_tail[len(yf):], dfo / fo_e, 0.0)
    l_all = np.vstack([l2, np.tile(l_ext[:, None], (1, n_eta + 1))])
    logE_ext = logE2[-1][None, :] - (0.5 + h) * (yf_ext - y_end_pre)[:, None] + np.log(fo_e / fo_a[len(yf) - 1])[:, None]
    logE_all = np.vstack([logE2, logE_ext])
    lH_all = 0.5 * np.log(2.0) + 0.5 * lxa[:, None] + logE_all
    U_all = np.vstack([U2, np.zeros((len(yf_ext), n_eta + 1))])
    # U/E, log-safe: R on the pulse, U e^{-log E} on the axial stages (E large there), 0 elsewhere
    st_a = np.concatenate([st_f, np.array(["ext"] * len(yf_ext))])
    axial_a = (st_a == "axl") | (st_a == "axU")
    mp_a = st_a == "pulse"
    R_final = Amp_eff[None, :] * R0[:, None] + c12[0][None, :] * B1[:, None] + c12[1][None, :] * B2[:, None]
    UoE = np.zeros_like(logE_all)
    UoE[axial_a] = U_all[axial_a] * np.exp(-logE_all[axial_a])
    UoE[mp_a] = R_final[:mp_a.sum()]
    rhoM = rk4_linear(yfa, UoE, l_all + 0.5, rhoM0)
    rI = rk4_linear(yfa, np.ones((len(yfa), 1)), 1.0 + l_all, rI0)
    rhoJ = rk4_linear(yfa, UoE, 2.0 * l_all + 0.5, rhoJ0)
    sS = rk4_linear(yfa, UoE ** 2 - 0.5, 2.0 * l_all, sS0)
    # g = (int_y^inf E^2 dy') / E^2  solves g' = -1 - (2l - 1) g backward from g(inf) = 1/(2A)  (E = E_pow beyond the grid)
    gE = rk4_linear_backward(yfa, -np.ones((len(yfa), 1)), (2.0 * l_all - 1.0), np.full(n_eta + 1, 1.0 / (2 * A)))
    yca = yfa[::2]; lxc = lxa[::2]; logEc = logE_all[::2]; lHc = lH_all[::2]; Uc = U_all[::2]; lc = l_all[::2]; UoEc = UoE[::2]
    Ec = np.exp(logEc)                                   # underflows to 0 far out; only ever multiplied, never divided by
    rM = rhoM * Ec; rJ = rhoJ * Ec                       # M/X and J/(XH), used only where multiplied
    Pi0 = -0.5 * gE[0] * np.exp(2 * logEc[0]) - 0.5 * 5.0 * (P_star * f) ** 2
    dEta = lambda g: g @ Deta.T
    dlogH = dEta(lHc); dlogE = dEta(logEc)
    W = 1.0 - 2 * D * eta[None, :] * rM - d[None, :] * (dEta(rhoM) + rhoM * dlogE) * Ec
    Qs = -W + ((1 - h) * rI - D * eta[None, :] * (dEta(rI) + rI * dlogH) - d[None, :] * (dEta(rhoJ) + rhoJ * (dlogE + dlogH)) * Ec
               + 2 * (h - D) * eta[None, :] * rJ)
    # N_s / E, log-safe:  -W U/E + D(rho_M - eta(rho_M,eta + rho_M logE_eta)) + E[4h eta s - d(s_eta + 2 s logE_eta)] + E[-2A eta g + (d/2)(g_eta + 2 g logE_eta)]
    rMeoE = rhoM - eta[None, :] * (dEta(rhoM) + rhoM * dlogE)
    NsE = (-W * UoEc + D * rMeoE
           + Ec * (4 * h * eta[None, :] * sS - d[None, :] * (dEta(sS) + 2 * sS * dlogE))
           + Ec * (-2 * A * eta[None, :] * gE + 0.5 * d[None, :] * (dEta(gE) + 2 * gE * dlogE)))
    a = 2.0 - 2.0 * lc
    # b_s = 2 D_X U / E = 2[(l - 1/2) U/E + d(U/E)/dy]
    dUoE = np.gradient(UoE, yfa, axis=0, edge_order=2)[::2]
    bs = 2.0 * ((lc - 0.5) * UoEc + dUoE)
    w = NsE / Qs
    test1 = a - bs * w
    test2 = 2 * bs * w + bs ** 2 / a + (a - 2) * w ** 2
    ts = -bs / a; vs = a * (1 + ts ** 2)
    invX = np.exp(-lxc)[:, None]
    PcX = (Qs + ts * NsE) / L[None, :]; JcX = (NsE - ts * Qs) / L[None, :]
    exact1 = PcX - vs * invX
    exact2 = 2 * (PcX - vs * invX) ** 2 - (vs - 2) * JcX ** 2
    stc = np.array([("holdh" if yy < y_tail0 else "tail") if yy >= b["holdh"] else sch.stage_of(np.array([yy]))[0] for yy in yca])
    c_inf = float(np.mean(np.exp(logEc[-1] + A * lxc[-1])))
    i_tailend = np.searchsorted(yca, y_tail0 + 3.0)
    rI_tailend = rI[i_tailend]
    E_all = None
    lxt, lHt = lxc[i_tailend], lHc[i_tailend]
    lHpow_a = 0.5 * np.log(2.0) + 0.5 * lxa + np.log(c_inf) - A * lxa
    inner_I_n = (np.sqrt(2) * P_star * f / 1.6) * np.exp(1.5 * lxR - lxt - lHt) - (np.sqrt(2) * c_inf / (1.5 - A)) * np.exp((1.5 - A) * lxR - lxt - lHt)
    diffw = (np.exp(lH_all - lHt[None, :] + (lxa - lxt)[:, None]) - np.exp(lHpow_a[:, None] - lHt[None, :] + (lxa - lxt)[:, None]))
    ang = inner_I_n + simpson_cum(yfa, diffw)[i_tailend]
    ang_abs = np.abs(inner_I_n) + simpson_cum(yfa, np.abs(diffw))[i_tailend]
    I_simp = simpson_cum(yfa, np.exp(lH_all - lHt[None, :] + (lxa - lxt)[:, None])) + (rI0 * np.exp(lxR + lHc[0] - lxt - lHt))[None, :]
    I_rk4 = rI * np.exp(lxc[:, None] + lHc - lxt - lHt)
    i_p = np.searchsorted(yca, b["pulse"]); i_e = np.searchsorted(yca, b["ext1"])
    G5_debug = {"ang": float(np.mean(ang)), "ang_abs": float(np.mean(ang_abs)), "one_over_ang_abs": float(np.mean(1.0 / ang_abs)),
                "I_rel_diff_at_pulse_start": float(np.max(np.abs(I_simp[i_p] - I_rk4[i_p]) / np.abs(I_rk4[i_p]))),
                "I_rel_diff_at_hold_end": float(np.max(np.abs(I_simp[i_e] - I_rk4[i_e]) / np.abs(I_rk4[i_e]))),
                "I_rel_diff_at_tail_end": float(np.max(np.abs(I_simp[i_tailend] - I_rk4[i_tailend]) / np.abs(I_rk4[i_tailend])))}
    i_int = np.searchsorted(yca, b['interp'])
    M_end_bc = np.abs(rhoM[i_int]) * np.exp(logEc[i_int] + lxc[i_int] - lx_c1 - lE_c1)                      # |M(pulse end)| / (E_c1 X_c1)
    J_end_bc = np.abs(rhoJ[i_int]) * np.exp(logEc[i_int] + lxc[i_int] + lHc[i_int] - lx_c1 - lE_c1 - lH_c1)   # |J(pulse end)| / (E_c1 X_c1 H_c1)
    M_closure_residual = float(np.max(np.abs(M_start_n + Amp_eff * mA + c12[0] * m1 + c12[1] * m2)))
    J_closure_residual = float(np.max(np.abs(J_start_n + Amp_eff * jA + c12[0] * j1 + c12[1] * j2)))
    s1, s2 = 0.5 - lam, 0.5 - 2 * lam
    # the pre-registered normalisation X_p e_b f is smaller by e^{s_1 (13/lam - 3)}; reported as log10 (it overflows at small lambda)
    log10_M_pre = float(np.max(np.log10(np.maximum(M_end_bc, 1e-300)) + s1 * (13 / lam - 3) / np.log(10)))
    log10_J_pre = float(np.max(np.log10(np.maximum(J_end_bc, 1e-300)) + s2 * (13 / lam - 3) / np.log(10)))
    res = {
        "params": {"Md": Md, "T_d": T_d, "P_star": P_star, "lambda": lam, "h": h, "T_f": T_f, "T_f_min_for_l_bound": T_f_min,
                   "c_o": c_o, "rho_o": sch.rho_o, "X_R": X_R, "dy": dy, "pulse_step": pulse_step, "n_eta": n_eta + 1, "sigma_prime_max": SIGMA_PRIME_MAX,
                   "T_w": sch.T_w, "pulse_length": 13 / lam, "T_hold_minus_h": T_hold, "Q_p": Q_p, "Q_ext_start_mean": float(np.mean(Q_ext_start)),
                   "Q_ext_start_expected": (lam - h) / (1 - lam), "stage_starts": {k: float(v) for k, v in b.items()}, "tail_start": y_tail0, "y_end": float(yfa[-1]), "n_fine": int(len(yfa))},
        "G1": {"K_b": K_b},
        "G2": {"P(.9)": Pfun(0.9), "P(1.2)": Pfun(1.2), "Pprime_min_on_bracket": 2 * 0.9 * K_b},
        "G3": {"S_pieces": S_pieces, "Amp": Amp.tolist(), "Amp_min": float(np.nanmin(Amp)) if np.isfinite(Amp).any() else None, "Amp_max": float(np.nanmax(Amp)) if np.isfinite(Amp).any() else None, "n_nan": int(np.isnan(Amp).sum()),
               "normalised_residual_max": float(np.max(np.abs(S_res))), "remainder_E_max": float(np.max(np.abs(Pfun(Amp_eff)))),
               "dAmp_deta_max": float(np.max(np.abs(dEta(Amp_eff[None, :])))), "e_b": float(np.mean(e_b)), "P_1_over_P_star": float(np.exp(logE0[np.searchsorted(yf, b['axU'])][0]) / (P_star * f[0]))},
        "G4": {"M_pulse_end_rel": 10.0 ** log10_M_pre if log10_M_pre < 300 else float("inf"), "J_pulse_end_rel": 10.0 ** log10_J_pre if log10_J_pre < 300 else float("inf"),
               "log10_M_pulse_end_over_prereg_scale": log10_M_pre, "log10_J_pulse_end_over_prereg_scale": log10_J_pre,
               "M_pulse_end_over_bump_centre_scale": float(np.max(M_end_bc)), "J_pulse_end_over_bump_centre_scale": float(np.max(J_end_bc)),
               "M_closure_residual": M_closure_residual, "J_closure_residual": J_closure_residual,
               "M_cancellation_rel": float(np.max(M_end_bc) / max(float(np.max(np.abs(c12[0] * m1))), 1e-300)),
               "rM_after_pulse_max": float(np.max(np.abs(rM[i_int + 10:]))), "rJ_after_pulse_max": float(np.max(np.abs(rJ[i_int + 10:]))),
               "rI_hold_end_minus_target": float(np.max(np.abs(rI[np.searchsorted(yca, b['ext1'])] - 1 / (1 - lam)))),
               "cb": [float(np.max(np.abs(cb[0]))), float(np.max(np.abs(cb[1])))], "c12_max": [float(np.max(np.abs(c12[0]))), float(np.max(np.abs(c12[1])))]},
        "G5_debug": G5_debug,
        "G5": {"rI_tail_end": float(np.mean(rI_tailend)), "target_1_over_1_minus_h": 1 / (1 - h), "rI_tail_end_rel_err": float(np.max(np.abs(rI_tailend - 1 / (1 - h))) * (1 - h)),
               "angular_moment_integral_over_abs": float(np.max(np.abs(ang / ang_abs))), "c_inf": c_inf, "Q_s_at_tail_end_max": float(np.max(np.abs(Qs[i_tailend])))},
        "G6": {}, "G7": {}, "G8": {"Pi0_over_Pstar2f2_max": float(np.max(Pi0 / (P_star * f) ** 2)), "Pi0_even_rel_err": float(np.max(np.abs(Pi0 - Pi0[::-1])) / np.max(np.abs(Pi0))),
                                   "eta_Pi0prime_min_offaxis": float(np.min((eta * dEta(Pi0[None, :])[0])[np.abs(eta) > 0.05]))},
        "G9": {}, "fields": {}
    }
    # G6 exponents
    patch_slopes = []
    for (p0, p1) in sch.patches:
        m = (yca > p0 + 0.05) & (yca < p1 - 0.05)
        patch_slopes.append({"patch": [p0, p1], "dlogE_dy_minus_expected_max": float(np.max(np.abs((lc[m] - 0.5) - (-0.5 - lam)))), "U_max": float(np.max(np.abs(Uc[m])))})
    m_tail = yca > y_tail0 + 3.0 + 0.1
    res["G6"] = {"patches": patch_slopes, "tail_dlogE_dy_minus_minusA_max": float(np.max(np.abs((lc[m_tail] - 0.5) + A))) if m_tail.any() else None, "e_b_over_P1": float(np.mean(e_b)) / float(np.exp(logE0[np.searchsorted(yf, b['axU'])][0]) / f[0])}
    # G7 cone tests per stage
    def stage_min(names, tail_max=None):
        m = np.isin(stc, names)
        if tail_max is not None:
            m &= (yca <= y_tail0 + tail_max)
        return {"n": int(m.sum()), "min_test1": float(np.min(test1[m])), "max_test2": float(np.max(test2[m])), "min_vs_minus_2": float(np.min(vs[m] - 2)),
                "min_Qs": float(np.min(Qs[m])), "max_abs_w": float(np.max(np.abs(w[m]))), "min_exact_Pc_minus_vs": float(np.min(exact1[m])), "min_exact_quadratic": float(np.min(exact2[m]))}
    mint = (stc == "int") & (yca > b["int"] + 1.0)
    ok_int = (test1 > 0) & (test2 < 2) & (vs > 2)
    ok_ex = (exact1 > 0) & (exact2 > 0) & (vs > 2)
    frac_int_ok = float(np.mean(np.all(ok_int[mint], axis=1))) if mint.any() else None
    frac_int_exact_ok = float(np.mean(np.all(ok_ex[mint], axis=1))) if mint.any() else None
    # first y on the intermediate interval from which the sufficient test holds for all eta (the paper: whole interval)
    ok_rows = np.all(ok_int, axis=1) & mint
    y_int_ok_from = float(yca[ok_rows][0] - b["int"]) if ok_rows.any() else None
    mpu = stc == "pulse"
    frac_pulse_ok = float(np.mean(np.all(ok_int[mpu], axis=1))) if mpu.any() else None
    G7 = {"int": stage_min(["int"]), "pulse": stage_min(["pulse"]), "interp": stage_min(["interp"]), "hold": stage_min(["hold"]),
          "exterior_to_tail_half": stage_min(["ext1", "hold1", "ext2", "holdh", "tail"], tail_max=0.5),
          "pulse_sup_bsw": float(np.max((bs * w)[stc == "pulse"])), "pulse_sup_test2": float(np.max(test2[stc == "pulse"])),
          "int_sup_sqrtlam_abs_w": float(np.sqrt(lam) * np.max(np.abs(w[mint]))),
          "int_fraction_sufficient_test_ok": frac_int_ok, "int_fraction_exact_admissible_ok": frac_int_exact_ok, "int_ok_from_y": y_int_ok_from,
          "int_length": float(sch.T_w), "pulse_fraction_ok": frac_pulse_ok,
          "sqrtlam_Pstar": float(np.sqrt(lam) * P_star), "lam_120_log": float(120 * lam * np.log(1 / lam))}
    res["G7"] = G7
    # G9: X_R needed for P_c > 2 on x in [e^-5, 1] with the relaxed test: P_c = X Q_s / L (1 - b_s w / a) ... report min Qs there and the required X_R
    # (the inner reference interval is y <= 0, closed form: Q_s from (A.25); report from the first grid point instead)
    res["G9"] = {"Qs_at_y0_min": float(np.min(Qs[0])), "X_R_needed_for_Pc_gt_2_at_x_e_minus_5": float(2 * np.max(L) / (np.exp(-5) * max(np.min(Qs[0]), 1e-300)))}
    res["fields"] = {"y": yca[::50].tolist(), "stage": stc[::50].tolist(), "logE_eta0": logE_all[::100, n_eta // 2].tolist(),
                     "U_eta_0p5": Uc[::50, int(np.argmin(np.abs(eta - 0.5)))].tolist(), "test1_min_over_eta": np.min(test1, axis=1)[::50].tolist(),
                     "test2_max_over_eta": np.max(test2, axis=1)[::50].tolist(), "vs_min_over_eta": np.min(vs, axis=1)[::50].tolist(),
                     "Qs_min_over_eta": np.min(Qs, axis=1)[::50].tolist(), "eta": eta.tolist()}
    if verbose:
        print(f"lambda={lam} P_*={P_star:.3e} h={h} T_d={T_d:.3f} T_w={sch.T_w:.1f} pulse={13/lam:.0f} T_hold={T_hold:.2f} Q_p={Q_p:.3e} y_end={yfa[-1]:.1f} grid {len(yfa)}x{n_eta+1}")
        print(f"  G1 K_b={K_b:.5f}   G2 P(.9)={Pfun(0.9):.4f} P(1.2)={Pfun(1.2):.4f} P'min={2*0.9*K_b:.3f}")
        print(f"  G3 pieces {S_pieces}")
        print(f"  G3 Amp in [{res['G3']['Amp_min']}, {res['G3']['Amp_max']}] nan={res['G3']['n_nan']}  resid={res['G3']['normalised_residual_max']:.2e}  |E|max={res['G3']['remainder_E_max']:.3e}  |dAmp/deta|max={res['G3']['dAmp_deta_max']:.3e}  e_b/P1={res['G6']['e_b_over_P1']:.3e}")
        print(f"  G4 M_end/(X_p e_b f)={res['G4']['M_pulse_end_rel']:.2e} J={res['G4']['J_pulse_end_rel']:.2e} | bump-centre scale: M={res['G4']['M_pulse_end_over_bump_centre_scale']:.2e} J={res['G4']['J_pulse_end_over_bump_centre_scale']:.2e} | cancellation {res['G4']['M_cancellation_rel']:.1e} | rM,rJ after pulse {res['G4']['rM_after_pulse_max']:.1e},{res['G4']['rJ_after_pulse_max']:.1e} rI-target={res['G4']['rI_hold_end_minus_target']:.2e} cb={res['G4']['cb']} c12={res['G4']['c12_max']}")
        print(f"  G5dbg {G5_debug}")
        print(f"  G5 rI(tail end)={res['G5']['rI_tail_end']:.9f} vs {1/(1-h):.9f} rel {res['G5']['rI_tail_end_rel_err']:.2e}; ang/abs={res['G5']['angular_moment_integral_over_abs']:.2e}; Qs(tail end)={res['G5']['Q_s_at_tail_end_max']:.2e}; Q_ext_start {res['params']['Q_ext_start_mean']:.6f} vs {(lam-h)/(1-lam):.6f}")
        print(f"  G6 patches: {[ (round(p['dlogE_dy_minus_expected_max'],12), p['U_max']) for p in patch_slopes]} tail: {res['G6']['tail_dlogE_dy_minus_minusA_max']}")
        for k, v in G7.items():
            print(f"  G7 {k}: {v}")
        print(f"  G8 Pi0/(P*^2 f^2) max={res['G8']['Pi0_over_Pstar2f2_max']:.6f} even_rel={res['G8']['Pi0_even_rel_err']:.2e} eta*Pi0' min={res['G8']['eta_Pi0prime_min_offaxis']:.3e}")
        print(f"  G9 {res['G9']}")
    return res


def gates(r):
    """The pre-registered gate answers for one run, YES/NO with the number."""
    g = {}
    g["G1"] = ("YES" if 0.20 < r["G1"]["K_b"] <= 0.25 else "NO", r["G1"]["K_b"])
    g["G2"] = ("YES" if (r["G2"]["P(.9)"] < -0.047 and r["G2"]["P(1.2)"] > 0.038 and r["G2"]["Pprime_min_on_bracket"] >= 0.36) else "NO",
               [r["G2"]["P(.9)"], r["G2"]["P(1.2)"], r["G2"]["Pprime_min_on_bracket"]])
    g["G3"] = ("YES" if (r["G3"]["n_nan"] == 0 and r["G3"]["normalised_residual_max"] < 1e-9) else "NO",
               {"n_no_root": r["G3"]["n_nan"], "residual": r["G3"]["normalised_residual_max"], "remainder_E_at_Amp1": r["G3"]["S_pieces"]["S_start/norm"] + r["G3"]["S_pieces"]["S_after/norm"]})
    g["G4_as_preregistered"] = ("YES" if (r["G4"]["M_pulse_end_rel"] < 1e-10 and r["G4"]["J_pulse_end_rel"] < 1e-10 and r["G4"]["rI_hold_end_minus_target"] < 1e-8) else "NO",
                                [r["G4"]["M_pulse_end_rel"], r["G4"]["J_pulse_end_rel"], r["G4"]["rI_hold_end_minus_target"]])
    g["G4_paper_normalisation"] = ("YES" if (r["G4"]["M_pulse_end_over_bump_centre_scale"] < 1e-8 and r["G4"]["J_pulse_end_over_bump_centre_scale"] < 1e-8 and r["G4"]["rI_hold_end_minus_target"] < 1e-8) else "NO",
                                   [r["G4"]["M_pulse_end_over_bump_centre_scale"], r["G4"]["J_pulse_end_over_bump_centre_scale"]])
    g["G5"] = ("YES" if r["G5"]["angular_moment_integral_over_abs"] < 1e-6 else "NO", r["G5"]["angular_moment_integral_over_abs"])
    g["G6"] = ("YES" if (all(p["dlogE_dy_minus_expected_max"] < 1e-9 and p["U_max"] == 0.0 for p in r["G6"]["patches"]) and r["G6"]["tail_dlogE_dy_minus_minusA_max"] < 1e-9) else "NO",
               [max(p["dlogE_dy_minus_expected_max"] for p in r["G6"]["patches"]), r["G6"]["tail_dlogE_dy_minus_minusA_max"]])
    G7 = r["G7"]
    ok = all(G7[k]["min_test1"] > 0 and G7[k]["max_test2"] < 2 and G7[k]["min_vs_minus_2"] > 0 for k in ("int", "pulse", "interp", "hold", "exterior_to_tail_half"))
    g["G7"] = ("YES" if (ok and G7["pulse_sup_bsw"] < 0.74 and G7["pulse_sup_test2"] < 1.68 and G7["int_sup_sqrtlam_abs_w"] < 0.25) else "NO",
               {k: [G7[k]["min_test1"], G7[k]["max_test2"], G7[k]["min_vs_minus_2"]] for k in ("int", "pulse", "interp", "hold", "exterior_to_tail_half")} | {"pulse_sup_bsw": G7["pulse_sup_bsw"], "pulse_sup_test2": G7["pulse_sup_test2"], "int_sup_sqrtlam_w": G7["int_sup_sqrtlam_abs_w"], "int_fraction_ok": G7["int_fraction_sufficient_test_ok"]})
    g["G8"] = ("YES" if (r["G8"]["Pi0_over_Pstar2f2_max"] <= -2.5 and r["G8"]["Pi0_even_rel_err"] < 1e-12 and r["G8"]["eta_Pi0prime_min_offaxis"] > 0) else "NO",
               [r["G8"]["Pi0_over_Pstar2f2_max"], r["G8"]["Pi0_even_rel_err"], r["G8"]["eta_Pi0prime_min_offaxis"]])
    return g


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--full", action="store_true")
    args = ap.parse_args()
    if args.quick:
        r = build(lam=0.1, dy=4e-3, n_eta=12)
        print(json.dumps(gates(r), indent=1, default=str))
        sys.exit(0)
    import time
    out = {"schema": "arc6_profile_v1", "leg": 430, "pdf_sha256": PDF_SHA, "prereg_commit": "e01a64d",
           "preregistered_runs": {}, "controls": {}, "post_hoc": {"label": "decided after the pre-registered runs were seen; numbers not pre-committed"}}
    t0 = time.time()
    # --- the pre-registered runs
    for lam in (0.1, 0.05, 0.025):
        r = build(lam=lam, dy=2e-3, n_eta=16, verbose=True)
        r["gates"] = gates(r)
        out["preregistered_runs"][str(lam)] = r
        print(f"[{time.time()-t0:.0f}s] lambda={lam} gates:", {k: v[0] for k, v in r["gates"].items()})
    # --- controls at lambda = 0.1 (each with its unmodified twin = the run above)
    ctrl = {}
    ctrl["C1_flip_lambda"] = gates(build(lam=0.1, dy=2e-3, n_eta=16, flip_lambda=True, verbose=False))
    ctrl["C3_drop_c12"] = gates(build(lam=0.1, dy=2e-3, n_eta=16, drop_c12=True, verbose=False))
    ctrl["C5_drop_A11_bumps"] = gates(build(lam=0.1, dy=2e-3, n_eta=16, drop_A11=True, verbose=False))
    ctrl["C6_R0_cut_5"] = gates(build(lam=0.1, dy=2e-3, n_eta=16, R0_cut=5.0, verbose=False))
    out["controls"] = ctrl
    print(f"[{time.time()-t0:.0f}s] controls:", {k: {kk: vv[0] for kk, vv in v.items()} for k, v in ctrl.items()})
    if args.sweep or args.full:
        # --- post hoc 1: the lambda sweep, to locate the paper's "sufficiently small lambda"
        sweep = {}
        for lam in (0.1, 0.03, 0.01, 0.003, 0.001, 3e-4, 1e-4, 5e-5):
            r = build(lam=lam, dy=4e-3, n_eta=12, verbose=False)
            sweep[str(lam)] = {"remainder_E_at_Amp1": r["G3"]["S_pieces"]["S_start/norm"] + r["G3"]["S_pieces"]["S_after/norm"],
                               "asymptote_(lam^-120lam - 1)/2": (lam ** (-120 * lam) - 1) / 2, "asymptote_60_lam_log": 60 * lam * np.log(1 / lam),
                               "root_in_bracket": r["G3"]["n_nan"] == 0, "Amp_range": [r["G3"]["Amp_min"], r["G3"]["Amp_max"]],
                               "int_fraction_ok": r["G7"]["int_fraction_sufficient_test_ok"], "int_ok_from_y": r["G7"]["int_ok_from_y"], "int_length": r["G7"]["int_length"],
                               "pulse_sup_bsw": r["G7"]["pulse_sup_bsw"], "pulse_sup_test2": r["G7"]["pulse_sup_test2"], "pulse_fraction_ok": r["G7"]["pulse_fraction_ok"],
                               "sqrtlam_Pstar": r["G7"]["sqrtlam_Pstar"], "gates": {k: v[0] for k, v in gates(r).items()}, "e_b_over_P1": r["G6"]["e_b_over_P1"], "y_end": r["params"]["y_end"]}
            print(f"[{time.time()-t0:.0f}s] sweep lambda={lam}: {sweep[str(lam)]}")
        out["post_hoc"]["lambda_sweep"] = sweep
        # --- post hoc 2: the role of P_*: the intermediate-interval cone needs sqrt(lambda) P_* << 1
        pst = {}
        for Ps in (None, 100.0, 1.0):
            r = build(lam=0.01, dy=4e-3, n_eta=12, P_star=Ps, verbose=False)
            pst[str(Ps or "paper")] = {"P_star": r["params"]["P_star"], "sqrtlam_Pstar": r["G7"]["sqrtlam_Pstar"], "int_fraction_ok": r["G7"]["int_fraction_sufficient_test_ok"],
                                       "int_ok_from_y": r["G7"]["int_ok_from_y"], "int_sup_sqrtlam_w": r["G7"]["int_sup_sqrtlam_abs_w"], "G7": gates(r)["G7"][0], "G8": gates(r)["G8"][0]}
            print(f"[{time.time()-t0:.0f}s] P_* = {Ps}: {pst[str(Ps or 'paper')]}")
        out["post_hoc"]["P_star_role_at_lambda_0.01"] = pst
    out["runtime_s"] = time.time() - t0
    OUT.write_text(json.dumps(out, indent=1, default=float) + "\n")
    print("wrote", OUT, f"{OUT.stat().st_size:,} B in {time.time()-t0:.0f}s")
