#!/usr/bin/env python3
"""Leg 400 / unit L5 -- W4 clause (b): the NATIVELY FINITE-ENERGY ansatz, built and priced.

WHAT THIS IS.  A construction plus a measurement, pre-registered in
`experiments/journal/leg_400.md` SS0-SS3 and committed BEFORE this file existed.

THE ANSATZ (SS2.2 of the journal).  Similarity variables y = x/lambda(t), ds/dt = lambda^-2,
u = lambda^-1 V(y,s), a(s) := -lambda lambda_t.  The profile is poloidal,

    P[f](y;e) = curl curl (f(|y|) e) = (f'' - f'/r)(yhat.e) yhat - (f'' + f'/r) e,
    U(y,s)    = m1(s) P[psi_alpha](y;c) + m2(s) P[psi_alpha](y;d),  psi_alpha = (1+r^2)^{(2-alpha)/2}

which is leg 381's banked synthetic exactly-DSS, exactly-divergence-free realization.  The L5
ansatz CUTS OFF THE POTENTIAL, not the field, so it is divergence-free by construction and needs
NO Bogovskii corrector:

    V(y,s) = m1(s) P[g(.,s)](y;c) + m2(s) P[g(.,s)](y;d),   g(r,s) = chi(r/rho(s)) psi_alpha(r),
    rho(s) = rho0 e^{kappa s}.

kappa = a  <=>  the cutoff radius is FROZEN IN PHYSICAL SPACE (R = lambda rho = const): the
natively finite-energy branch.  kappa = 0 <=> frozen in similarity space, which makes V exactly
2 log lambda-periodic in s, i.e. EXACTLY DSS -- reading (c)'s branch.

WHAT IS MEASURED.  The TOTAL LOCALISATION-PLUS-MODULATION ERROR, i.e. the commutator

    R_loc := R[V] - chi R[U] = T1 + T2 + T3 + T4 + T5      (pressure T6 handled in SS3.1/SS5)

    T1 cutoff drift        = the d_s chi part of V_s - chi U_s          (prop. kappa)
    T2 modulation transport= a[(V + y.grad V) - chi(U + y.grad U)]      (prop. a)
    T3 MODULATION COMMUTATOR = the mdot part of V_s - chi U_s           (prop. mdot; ZERO iff SS)
    T4 viscous commutator  = -[Lap V - chi Lap U]
    T5 nonlinear commutator= V.grad V - chi (U.grad U)

in the two pre-registered scale-invariant norms

    velocity  : ||F||_{L1_t L3_x}      = int ||R_loc(.,s)||_{L3_y} ds
    vorticity : ||curl F||_{L1_t L3/2_x} = int ||curl_y R_loc(.,s)||_{L3/2_y} ds   (PRESSURE-FREE)

CEILING.  Tier 2.  Float64 quadrature on a SYNTHETIC field.  Route 4 has NO banked profile
(leg 382 line 174; leg 397 SS1), so the CONSTANTS below are properties of leg 381's realization and
the EXPONENTS are properties of the ansatz class.  No link of the L1->L4 chain moves.  Clay ~0.05%.

Run:    .venv/bin/python experiments/p2_route_l5_v1.py
Writes: writeup/data/p2_route_l5_finite_energy_v1.json  (checkpointed after every stage)
"""

import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "writeup" / "data" / "p2_route_l5_finite_energy_v1.json"
CLOC = ROOT / "writeup" / "data" / "p2_route_cloc_v1.json"

# ---------------------------------------------------------------------------------------------
# 0.  The banked realization (leg 381, p2_route_cloc_v1.py, verbatim constants)
# ---------------------------------------------------------------------------------------------

C_AXIS = np.array([0.0, 0.0, 1.0])
D_AXIS = np.array([1.0, 0.0, 0.0])
LAMBDA = 1.7
A_MOD = 0.5                      # the (D)SS modulation value a = -lambda lambda_t
PERIOD = 2.0 * math.log(LAMBDA)  # 1.0612565021243408
OMEGA = math.pi / math.log(LAMBDA)


def modulation(s, mode="DSS", amp=1.0):
    """m1, m2 and their s-derivatives.  mode='SS' => constants => exactly self-similar."""
    if mode == "SS":
        return 1.0, 0.6, 0.0, 0.0
    m1 = 1.0 + amp * 0.35 * math.cos(OMEGA * s)
    m2 = 0.6 + amp * 0.25 * math.sin(OMEGA * s + 0.7)
    d1 = -amp * 0.35 * OMEGA * math.sin(OMEGA * s)
    d2 = amp * 0.25 * OMEGA * math.cos(OMEGA * s + 0.7)
    return m1, m2, d1, d2


def psi_derivs(r, alpha, order=4):
    """psi = (1+r^2)^p, p = (2-alpha)/2.  Returns [psi, psi', psi'', psi''', psi''''] (to `order`)."""
    p = (2.0 - alpha) / 2.0
    b = 1.0 + r * r
    # d^k/dr^k of (1+r^2)^p by explicit differentiation
    out = [b ** p]
    if order >= 1:
        out.append(2.0 * p * r * b ** (p - 1.0))
    if order >= 2:
        out.append(2.0 * p * b ** (p - 1.0) + 4.0 * p * (p - 1.0) * r * r * b ** (p - 2.0))
    if order >= 3:
        out.append(12.0 * p * (p - 1.0) * r * b ** (p - 2.0)
                   + 8.0 * p * (p - 1.0) * (p - 2.0) * r ** 3 * b ** (p - 3.0))
    if order >= 4:
        out.append(12.0 * p * (p - 1.0) * b ** (p - 2.0)
                   + 48.0 * p * (p - 1.0) * (p - 2.0) * r ** 2 * b ** (p - 3.0)
                   + 16.0 * p * (p - 1.0) * (p - 2.0) * (p - 3.0) * r ** 4 * b ** (p - 4.0))
    return out


# --- the cutoff basis (lesson 91: the BASIS is part of the measurement) ------------------------

_SMOOTH9 = (126.0, -420.0, 540.0, -315.0, 70.0)     # 126x^5-420x^6+540x^7-315x^8+70x^9  (C^4 join)
_SMOOTH5 = (10.0, -15.0, 6.0)                        # 10x^3-15x^4+6x^5                  (C^2 join)


def _step_derivs(x, kind, order):
    """S(x) and its derivatives on [0,1]; S(0)=0, S(1)=1, derivatives vanish at both ends."""
    coeffs = _SMOOTH9 if kind == "C4" else _SMOOTH5
    p0 = 5 if kind == "C4" else 3
    out = []
    for k in range(order + 1):
        acc = np.zeros_like(x)
        for j, c in enumerate(coeffs):
            n = p0 + j
            if n - k < 0:
                continue
            fac = 1.0
            for i in range(k):
                fac *= (n - i)
            acc = acc + c * fac * x ** (n - k)
        out.append(acc)
    return out


def chi_derivs(r, rho, kind="C4", order=4):
    """chi(r) = X(r/rho): 1 on r<=rho, 0 on r>=2rho.  Returns [chi, chi_r, ..., d^order chi/dr^order]."""
    xi = r / rho
    x = np.clip(xi - 1.0, 0.0, 1.0)
    S = _step_derivs(x, kind, order)
    inside = xi <= 1.0
    outside = xi >= 2.0
    out = []
    for k in range(order + 1):
        if k == 0:
            v = 1.0 - S[0]
            v = np.where(inside, 1.0, np.where(outside, 0.0, v))
        else:
            v = -S[k] / rho ** k
            v = np.where(inside | outside, 0.0, v)
        out.append(v)
    return out


def leibniz(u, v, order):
    """derivatives of the product u*v given derivative lists."""
    out = []
    for n in range(order + 1):
        acc = np.zeros_like(u[0])
        c = 1.0
        for k in range(n + 1):
            acc = acc + math.comb(n, k) * u[k] * v[n - k]
        out.append(acc)
    return out


# ---------------------------------------------------------------------------------------------
# 1.  The poloidal operator P[f](y;e) and everything the profile system needs from it
# ---------------------------------------------------------------------------------------------

def polo_field(h1, h2, r, yhat, e):
    """P[h] = A (yhat.e) yhat + B e,  A = h'' - h'/r,  B = -(h'' + h'/r)."""
    A = h2 - h1 / r
    B = -(h2 + h1 / r)
    proj = yhat @ e
    return A[:, None] * proj[:, None] * yhat + B[:, None] * e[None, :]


def polo_ygrad(h1, h2, h3, r, yhat, e):
    """y.grad P[h] = r A' (yhat.e) yhat + r B' e  (the angular factors are homogeneous of degree 0)."""
    Ap = h3 - h2 / r + h1 / r ** 2
    Bp = -(h3 + h2 / r - h1 / r ** 2)
    proj = yhat @ e
    return (r * Ap)[:, None] * proj[:, None] * yhat + (r * Bp)[:, None] * e[None, :]


def polo_grad(h1, h2, h3, r, yhat, e):
    """Jacobian d_j F_i of F = A (yhat.e) yhat + B e."""
    A = h2 - h1 / r
    B = -(h2 + h1 / r)
    Ap = h3 - h2 / r + h1 / r ** 2
    Bp = -(h3 + h2 / r - h1 / r ** 2)
    proj = (yhat @ e)                                   # (N,)
    N = r.shape[0]
    ident = np.eye(3)[None, :, :]
    # d_j[(yhat.e) yhat_i] = [(e_j - proj yhat_j) yhat_i + proj (delta_ij - yhat_i yhat_j)] / r
    term = ((e[None, None, :] - proj[:, None, None] * yhat[:, None, :]) * yhat[:, :, None]
            + proj[:, None, None] * (ident - yhat[:, :, None] * yhat[:, None, :])) / r[:, None, None]
    out = (Ap[:, None, None] * proj[:, None, None] * yhat[:, :, None] * yhat[:, None, :]
           + A[:, None, None] * term
           + Bp[:, None, None] * e[None, :, None] * yhat[:, None, :])
    return out                                           # index [n, i, j] = d_j F_i


def lap_radial(h1, h2, h3, h4, r):
    """(Lh)' and (Lh)'' where Lh = h'' + 2h'/r, so that Lap P[h] = P[Lh]."""
    L1 = h3 + 2.0 * h2 / r - 2.0 * h1 / r ** 2
    L2 = h4 + 2.0 * h3 / r - 4.0 * h2 / r ** 2 + 4.0 * h1 / r ** 3
    return L1, L2


# ---------------------------------------------------------------------------------------------
# 2.  THE LOCALISATION-PLUS-MODULATION ERROR  R_loc = T1+T2+T3+T4+T5, term by term
# ---------------------------------------------------------------------------------------------

def residual_terms(pts, s, alpha, rho0, kappa, mode="DSS", kind="C4", amp=1.0, a_mod=A_MOD,
                   no_cutoff=False, want=("T1", "T2", "T3", "T4", "T5")):
    """Every extra term the modulation and the cutoff generate, at the points `pts`."""
    r = np.linalg.norm(pts, axis=-1)
    r = np.where(r > 0, r, 1e-300)
    yhat = pts / r[:, None]
    rho = rho0 * math.exp(kappa * s)

    m1, m2, dm1, dm2 = modulation(s, mode, amp)
    ps = psi_derivs(r, alpha, 4)
    if no_cutoff:
        ch = [np.ones_like(r)] + [np.zeros_like(r) for _ in range(4)]
    else:
        ch = chi_derivs(r, rho, kind, 4)
    g = leibniz(ch, ps, 4)
    chi = ch[0]

    # d_s g = -kappa r chi_r psi  (and its r-derivatives, needed to order 2 for P[.])
    q0 = r * ch[1] * ps[0]
    q1 = (ch[1] + r * ch[2]) * ps[0] + r * ch[1] * ps[1]
    q2 = (2.0 * ch[2] + r * ch[3]) * ps[0] + 2.0 * (ch[1] + r * ch[2]) * ps[1] + r * ch[1] * ps[2]
    gs1, gs2 = -kappa * q1, -kappa * q2

    axes = ((m1, dm1, C_AXIS), (m2, dm2, D_AXIS))
    Z = np.zeros_like(pts)
    T = {k: Z.copy() for k in ("T1", "T2", "T3", "T4", "T5")}

    V = Z.copy(); U = Z.copy()
    ygV = Z.copy(); ygU = Z.copy()
    lapV = Z.copy(); lapU = Z.copy()
    gV = np.zeros((pts.shape[0], 3, 3)); gU = np.zeros((pts.shape[0], 3, 3))
    for (m, dm, e) in axes:
        Pg = polo_field(g[1], g[2], r, yhat, e)
        Pp = polo_field(ps[1], ps[2], r, yhat, e)
        V += m * Pg
        U += m * Pp
        if "T1" in want:
            T["T1"] += m * polo_field(gs1, gs2, r, yhat, e)
        if "T3" in want:
            T["T3"] += dm * (Pg - chi[:, None] * Pp)
        if "T2" in want:
            ygV += m * polo_ygrad(g[1], g[2], g[3], r, yhat, e)
            ygU += m * polo_ygrad(ps[1], ps[2], ps[3], r, yhat, e)
        if "T4" in want:
            Lg1, Lg2 = lap_radial(g[1], g[2], g[3], g[4], r)
            Lp1, Lp2 = lap_radial(ps[1], ps[2], ps[3], ps[4], r)
            lapV += m * polo_field(Lg1, Lg2, r, yhat, e)
            lapU += m * polo_field(Lp1, Lp2, r, yhat, e)
        if "T5" in want:
            gV += m * polo_grad(g[1], g[2], g[3], r, yhat, e)
            gU += m * polo_grad(ps[1], ps[2], ps[3], r, yhat, e)

    if "T2" in want:
        T["T2"] = a_mod * ((V + ygV) - chi[:, None] * (U + ygU))
    if "T4" in want:
        T["T4"] = -(lapV - chi[:, None] * lapU)
    if "T5" in want:
        advV = np.einsum("nij,nj->ni", gV, V)
        advU = np.einsum("nij,nj->ni", gU, U)
        T["T5"] = advV - chi[:, None] * advU
    T["V"] = V
    T["Vplus"] = V + ygV
    return T


def R_loc(pts, s, **kw):
    T = residual_terms(pts, s, **kw)
    return T["T1"] + T["T2"] + T["T3"] + T["T4"] + T["T5"]


# ---------------------------------------------------------------------------------------------
# 3.  Quadrature on the annulus (R_loc is supported EXACTLY on rho <= |y| <= 2rho)
# ---------------------------------------------------------------------------------------------

def sphere_nodes(n_theta=24, n_phi=48):
    ct, wct = np.polynomial.legendre.leggauss(n_theta)
    phi = 2.0 * math.pi * np.arange(n_phi) / n_phi
    wphi = np.full(n_phi, 2.0 * math.pi / n_phi)
    st = np.sqrt(1.0 - ct ** 2)
    dirs = np.stack([st[:, None] * np.cos(phi)[None, :],
                     st[:, None] * np.sin(phi)[None, :],
                     np.repeat(ct[:, None], n_phi, axis=1)], axis=-1)
    w = (wct[:, None] * wphi[None, :]).reshape(-1)
    return dirs.reshape(-1, 3), w


def radial_nodes(r_lo, r_hi, n_panel=8, n_gl=16):
    edges = np.linspace(r_lo, r_hi, n_panel + 1)
    xg, wg = np.polynomial.legendre.leggauss(n_gl)
    nodes, wts = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        mid, half = 0.5 * (lo + hi), 0.5 * (hi - lo)
        nodes.append(mid + half * xg)
        wts.append(half * wg)
    return np.concatenate(nodes), np.concatenate(wts)


def annulus_norms(s, alpha, rho0, kappa, mode="DSS", kind="C4", amp=1.0, a_mod=A_MOD,
                  n_theta=24, n_phi=48, n_panel=8, n_gl=16, fd_rel=1e-4, per_term=False):
    """||R_loc||_{L3}, ||curl R_loc||_{L3/2}, and per-term L3 norms, at similarity time s."""
    rho = rho0 * math.exp(kappa * s)
    dirs, wang = sphere_nodes(n_theta, n_phi)
    rad, wrad = radial_nodes(rho, 2.0 * rho, n_panel, n_gl)
    h = fd_rel * rho
    kw = dict(alpha=alpha, rho0=rho0, kappa=kappa, mode=mode, kind=kind, amp=amp, a_mod=a_mod)

    acc3 = 0.0
    acc_curl = 0.0
    acc_terms = {k: 0.0 for k in ("T1", "T2", "T3", "T4", "T5", "T12", "T123")}
    for rr, wr in zip(rad, wrad):
        pts = rr * dirs
        T = residual_terms(pts, s, **kw)
        R = T["T1"] + T["T2"] + T["T3"] + T["T4"] + T["T5"]
        vals = np.linalg.norm(R, axis=-1)
        acc3 += wr * rr * rr * float(np.dot(wang, vals ** 3))
        if per_term:
            for k in ("T1", "T2", "T3", "T4", "T5"):
                acc_terms[k] += wr * rr * rr * float(np.dot(wang, np.linalg.norm(T[k], axis=-1) ** 3))
            for k, comb in (("T12", T["T1"] + T["T2"]), ("T123", T["T1"] + T["T2"] + T["T3"])):
                acc_terms[k] += wr * rr * rr * float(np.dot(wang, np.linalg.norm(comb, axis=-1) ** 3))
        # curl by 4th-order central differences (pressure-free measurement)
        curl = np.zeros_like(pts)
        dR = np.zeros((3, pts.shape[0], 3))              # dR[k][n,i] = dR_i/dy_k
        for k in range(3):
            e = np.zeros(3); e[k] = 1.0
            f = [R_loc(pts + mf * h * e[None, :], s, **kw) for mf in (-2.0, -1.0, 1.0, 2.0)]
            dR[k] = (f[0] - 8.0 * f[1] + 8.0 * f[2] - f[3]) / (12.0 * h)
        curl[:, 0] = dR[1][:, 2] - dR[2][:, 1]
        curl[:, 1] = dR[2][:, 0] - dR[0][:, 2]
        curl[:, 2] = dR[0][:, 1] - dR[1][:, 0]
        cv = np.linalg.norm(curl, axis=-1)
        acc_curl += wr * rr * rr * float(np.dot(wang, cv ** 1.5))

    out = {"rho": rho, "L3": acc3 ** (1.0 / 3.0), "curl_L32": acc_curl ** (2.0 / 3.0)}
    if per_term:
        for k, v in acc_terms.items():
            out[k + "_L3"] = v ** (1.0 / 3.0)
    return out


def period_average(alpha, rho0, kappa, mode="DSS", n_s=8, s0=0.0, per_term=False, **kw):
    """Period-average over ONE whole DSS period in s (the modulation is carried, not dropped)."""
    rows = []
    for j in range(n_s):
        s = s0 + PERIOD * j / n_s
        rows.append(annulus_norms(s, alpha, rho0, kappa, mode=mode, per_term=per_term, **kw))
    avg = {}
    for k in rows[0]:
        avg[k] = float(np.mean([r[k] for r in rows]))
    avg["n_s"] = n_s
    avg["rows_min"] = {k: float(np.min([r[k] for r in rows])) for k in rows[0]}
    avg["rows_max"] = {k: float(np.max([r[k] for r in rows])) for k in rows[0]}
    return avg


def fit_exponent(rhos, vals):
    x = np.log(np.asarray(rhos, dtype=float))
    y = np.log(np.maximum(np.asarray(vals, dtype=float), 1e-300))
    A = np.vstack([x, np.ones_like(x)]).T
    sol, *_ = np.linalg.lstsq(A, y, rcond=None)
    pred = A @ sol
    resid = float(np.max(np.abs(y - pred)))
    return float(sol[0]), float(math.exp(sol[1])), resid


def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def checkpoint(doc, note):
    doc["_checkpoint"] = note
    doc["_checkpoint_time"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    OUT.write_text(json.dumps(doc, indent=1))
    print("  [checkpoint] %s -> %s" % (note, OUT.name), flush=True)
