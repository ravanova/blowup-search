#!/usr/bin/env python3
"""Leg 381 / Route-CLOC -- verifying CLAY_OBLIGATIONS.md §4 (the localisation clause).

WHAT THIS IS.  A verification runner, not a construction.  CLAY_OBLIGATIONS.md is a DRAFT
whose own header flags two clauses as most likely wrong, and §4 is built on both:

  (i)  the reviewer's ARITHMETIC   -- "int |u|^2 dx at time t scales as (T*-t)^{1/2} int |U|^2 dy,
       so bounded energy requires U in L^2(R^3), which the specification does not give";
  (ii) the reviewer's READING of the official Clay problem statement -- "smooth, divergence-free,
       decaying faster than any polynomial, with f = 0, such that no smooth solution exists for
       all time with bounded energy".

This runner re-derives (i) INDEPENDENTLY for genuine lambda-DSS (not merely exact self-similar),
with the log-periodic modulation CARRIED rather than dropped, checks it numerically against an
explicitly-constructed exactly-DSS exactly-divergence-free synthetic field, checks (ii) against the
official statement's own text, and puts MAGNITUDES on what an admissible-cutoff analysis consumes.

IT ATTEMPTS NO LOCALISATION.  Cutting off changes the solution; the obligation transfers to §5's
persistence question.  This runner measures the SIZE of what a cutoff would introduce and stops.

CEILING.  Tier 2.  Float64 quadrature of a SYNTHETIC field plus a text check.  No link of the
L1 -> L4 chain moves.  Clay stays ~0.05%.  Verifying an obligation is not movement toward Clay.
This leg does NOT produce a certified decay exponent -- that is leg 382's instrument, in slot C;
every magnitude here is reported as a FUNCTION of the exponent alpha so leg 382's enclosure can be
substituted when it exists.

--------------------------------------------------------------------------------------------
THE DERIVATION (step (i)), stated before it is checked.

Similarity variables for backward blow-up at T*, standard normalisation a = 1/2:

    y = x / sqrt(T*-t),    s = -log(T*-t),    u(x,t) = (T*-t)^{-1/2} U(y, s).

The NS scaling symmetry is u -> lam u(lam x, T* - lam^2 (T*-t)).  A lambda-DSS solution is
invariant under that map at the single value lam = lambda, which in (y,s) coordinates is exactly
the shift s -> s + 2 log lambda.  Hence

    DSS  <=>  U(y, s + 2 log lambda) = U(y, s)                        [leg 260's framing]

and exact self-similarity is the degenerate case U independent of s.  Then

    E(t) = int_{R^3} |u|^2 dx = (T*-t)^{-1} (T*-t)^{3/2} int |U(y,s)|^2 dy = (T*-t)^{1/2} G(s),
    G(s) := int_{R^3} |U(y,s)|^2 dy,     G(s + 2 log lambda) = G(s).

STRUCTURAL POINT, and the reason no exponent can shift: the DSS group lambda^Z is a SUBGROUP of
the same one-parameter scaling group that fixes the SS exponents.  Reducing R_{>0} to lambda^Z
cannot change an exponent; it can only turn the CONSTANT G into a PERIODIC FUNCTION of s.  So the
DSS exponent equals the SS exponent EXACTLY -- ratio 1, no factor -- and the log-periodic
modulation appears as a bounded positive prefactor, oscillating in [min G, max G] over each
period, so that E(t) (T*-t)^{-1/2} does not converge as t -> T* unless G is constant.

THE ONE PLACE THE REVIEWER'S STEP IS NOT VALID AS WRITTEN.  When U(.,s) is not in L^2 both sides
of the identity are +infinity, and an identity between infinities cannot by itself establish the
conditional "bounded energy requires U in L^2".  The load-bearing form must be the TRUNCATED one,
which is finite for every alpha and every rho and reduces to the reviewer's statement when both
sides are finite.  With far-field |U(y,s)| <= C_alpha (1+|y|)^{-alpha} and a FIXED ball of radius
rho in PHYSICAL space,

    E_rho(t) = int_{|x|<=rho} |u|^2 dx = (T*-t)^{1/2} int_{|y| <= rho/sqrt(T*-t)} |U|^2 dy
             ~ [K(s) / (3 - 2 alpha)] * rho^{3-2alpha} * (T*-t)^{alpha-1}      (alpha < 3/2)

so the fixed-ball energy exponent is (alpha - 1), and the L^2(R^3) threshold is alpha > 3/2.
Leg 260's banked Type-I bound (Chae-Wolf arXiv:1610.09464, |U| <= C/(1+|y|), alpha = 1) therefore
sits EXACTLY at the critical value where the fixed-ball energy is time-independent, and is short
of the L^2 threshold by exactly Delta alpha = 1/2, i.e. the certified exponent must be 1.5x the
a-priori Type-I one.
--------------------------------------------------------------------------------------------

THE SYNTHETIC FIELD (the falsifier).  Poloidal fields, exactly divergence-free by construction:

    P[psi](y) = curl curl (psi(r) e) = (psi'' - psi'/r)(yhat.e) yhat - (psi'' + psi'/r) e
    U(y,s) = m1(s) P[psi_alpha](y; e=c) + m2(s) P[psi_alpha](y; e=d),   c.d = 0
    psi_alpha(r) = (1+r^2)^{(2-alpha)/2}   =>   |U| ~ r^{-alpha},  radial component present.

m1, m2 are 2 log lambda-periodic in s, so u(x,t) := (T*-t)^{-1/2} U(y,s) is EXACTLY lambda-DSS.
This field is NOT the route-4 candidate and is not claimed to be.  Its only job is to catch an
algebra error: if the closed-form law and the quadrature disagree, the derivation is wrong.

Run:    .venv/bin/python experiments/p2_route_cloc_v1.py
Writes: writeup/data/p2_route_cloc_v1.json
"""

import hashlib
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "writeup" / "data" / "p2_route_cloc_v1.json"

CLAY_SOURCE = ("Charles L. Fefferman, 'Existence and smoothness of the Navier-Stokes equation', "
               "official Clay Mathematics Institute problem description, "
               "https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf "
               "(TeX creation date 2006-08-04, last modified 2013-02-05); fetched and its text "
               "layer extracted by this leg, 2026-08-12")

# ---------------------------------------------------------------------------------------------
# 0.  The synthetic exactly-DSS, exactly-divergence-free field.
# ---------------------------------------------------------------------------------------------

C_AXIS = np.array([0.0, 0.0, 1.0])
D_AXIS = np.array([1.0, 0.0, 0.0])           # c . d = 0 -> genuinely non-axisymmetric
LAMBDA = 1.7                                  # the DSS ratio; period in s is 2 log lambda
T_STAR = 1.0


def _psi_derivs(r, alpha):
    """psi = (1+r^2)^p with p = (2-alpha)/2; returns psi', psi''.  alpha != 2."""
    p = (2.0 - alpha) / 2.0
    base = 1.0 + r * r
    d1 = 2.0 * p * r * base ** (p - 1.0)
    d2 = 2.0 * p * base ** (p - 1.0) + 4.0 * p * (p - 1.0) * r * r * base ** (p - 2.0)
    return d1, d2


def poloidal(xyz, alpha, axis):
    """curl curl (psi(r) axis): exactly divergence-free, |P| ~ r^-alpha, radial component present."""
    r = np.linalg.norm(xyz, axis=-1)
    r_safe = np.where(r > 0, r, 1.0)
    d1, d2 = _psi_derivs(r_safe, alpha)
    yhat = xyz / r_safe[..., None]
    proj = yhat @ axis
    return (d2 - d1 / r_safe)[..., None] * proj[..., None] * yhat - (d2 + d1 / r_safe)[..., None] * axis


def modulation(s, which):
    """2 log lambda-periodic in s.  omega = pi / log lambda gives period exactly 2 log lambda."""
    omega = math.pi / math.log(LAMBDA)
    if which == "SS":                                    # degenerate case: no s-dependence
        return 1.0, 0.6
    return 1.0 + 0.35 * math.cos(omega * s), 0.6 + 0.25 * math.sin(omega * s + 0.7)


def U_profile(y, s, alpha, mode="DSS"):
    m1, m2 = modulation(s, mode)
    return m1 * poloidal(y, alpha, C_AXIS) + m2 * poloidal(y, alpha, D_AXIS)


def u_physical(x, t, alpha, mode="DSS"):
    dt = T_STAR - t
    y = x / math.sqrt(dt)
    s = -math.log(dt)
    return U_profile(y, s, alpha, mode) / math.sqrt(dt)


# ---------------------------------------------------------------------------------------------
# 1.  Quadrature: composite Gauss-Legendre on geometric radial shells x Gauss(cos theta) x FFT(phi)
# ---------------------------------------------------------------------------------------------

def _sphere_nodes(n_theta=40, n_phi=80):
    ct, wct = np.polynomial.legendre.leggauss(n_theta)
    phi = 2.0 * math.pi * np.arange(n_phi) / n_phi
    wphi = np.full(n_phi, 2.0 * math.pi / n_phi)
    st = np.sqrt(1.0 - ct ** 2)
    dirs = np.stack([(st[:, None] * np.cos(phi)[None, :]),
                     (st[:, None] * np.sin(phi)[None, :]),
                     np.repeat(ct[:, None], n_phi, axis=1)], axis=-1)
    w = wct[:, None] * wphi[None, :]
    return dirs.reshape(-1, 3), w.reshape(-1)


def _radial_nodes(r_lo, r_hi, n_shell=12, n_gl=24):
    """Geometric shells so that algebraic tails are resolved to many decades."""
    if r_lo <= 0:
        edges = [0.0] + list(np.geomspace(max(r_hi * 1e-6, 1e-6), r_hi, n_shell))
    else:
        edges = list(np.geomspace(r_lo, r_hi, n_shell + 1))
    xg, wg = np.polynomial.legendre.leggauss(n_gl)
    nodes, wts = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        mid, half = 0.5 * (a + b), 0.5 * (b - a)
        nodes.append(mid + half * xg)
        wts.append(half * wg)
    return np.concatenate(nodes), np.concatenate(wts)


def shell_integral_Lp(alpha, s, r_lo, r_hi, p=2.0, mode="DSS", n_shell=14):
    """int_{r_lo <= |y| <= r_hi} |U(y,s)|^p dy, by product quadrature."""
    dirs, wang = _sphere_nodes()
    rad, wrad = _radial_nodes(r_lo, r_hi, n_shell=n_shell)
    total = 0.0
    for r, wr in zip(rad, wrad):
        pts = r * dirs
        val = np.linalg.norm(U_profile(pts, s, alpha, mode), axis=-1)
        total += wr * r * r * float(np.dot(wang, val ** p))
    return total


def divergence_max(alpha, s, radii=(0.3, 1.0, 3.0, 10.0)):
    """4th-order central-difference divergence of the analytic field: must be ~0."""
    dirs, _ = _sphere_nodes(n_theta=6, n_phi=8)
    worst_abs, worst_rel = 0.0, 0.0
    for r in radii:
        h = 1e-3 * max(r, 1.0)
        for d in dirs:
            x0 = r * d
            div = 0.0
            for k in range(3):
                e = np.zeros(3)
                e[k] = 1.0
                f = [U_profile(x0 + m * h * e, s, alpha)[k] for m in (-2, -1, 1, 2)]
                div += (f[0] - 8 * f[1] + 8 * f[2] - f[3]) / (12 * h)
            scale = float(np.linalg.norm(U_profile(x0, s, alpha))) / max(r, 1e-12)
            worst_abs = max(worst_abs, abs(div))
            worst_rel = max(worst_rel, abs(div) / max(scale, 1e-300))
    return worst_abs, worst_rel


# ---------------------------------------------------------------------------------------------
# 2.  CHECK A -- the field really is lambda-DSS (else every downstream number is about nothing)
# ---------------------------------------------------------------------------------------------

def check_dss_symmetry(alpha=1.0):
    """u(x,t) == lambda * u(lambda x, T* - lambda^2 (T*-t)) to machine precision."""
    rng = np.random.default_rng(381)
    worst = 0.0
    for _ in range(40):
        x = rng.normal(size=3) * rng.uniform(0.2, 6.0)
        t = T_STAR - rng.uniform(1e-3, 0.5)
        lhs = u_physical(x, t, alpha)
        t2 = T_STAR - LAMBDA ** 2 * (T_STAR - t)
        rhs = LAMBDA * u_physical(LAMBDA * x, t2, alpha)
        worst = max(worst, float(np.linalg.norm(lhs - rhs) / max(np.linalg.norm(lhs), 1e-300)))
    return worst


# ---------------------------------------------------------------------------------------------
# 3.  CHECK B -- the energy exponent, SS vs DSS, with the modulation carried
# ---------------------------------------------------------------------------------------------

def energy_curve(alpha, mode, rho=None, n_t=48, dt_lo=1e-3, dt_hi=0.3, r_max_factor=4e3,
                 n_periods=None):
    """E(t) (or E_rho(t) if rho given) by quadrature in y, over a grid of (T*-t).

    n_periods: if given, the grid spans EXACTLY that many DSS periods in s and is uniform in s.
    That is what 'handling the modulation rather than dropping it' means operationally -- a
    power-law fit over whole periods averages the log-periodic factor out exactly, so any residual
    departure of the fitted exponent from the SS value would be a REAL exponent shift.
    """
    if n_periods is not None:
        s_hi = -math.log(dt_lo if dt_lo else 1e-3)
        s_lo = -math.log(dt_hi)
        s_hi = s_lo + n_periods * 2.0 * math.log(LAMBDA)
        s_grid = np.linspace(s_lo, s_hi, n_t, endpoint=False)
        dts = np.exp(-s_grid)
    else:
        dts = np.geomspace(dt_lo, dt_hi, n_t)
    out = []
    for dt in dts:
        s = -math.log(dt)
        R = (rho / math.sqrt(dt)) if rho is not None else r_max_factor
        g = shell_integral_Lp(alpha, s, 0.0, R, 2.0, mode)
        out.append((dt, s, math.sqrt(dt) * g, g))
    return np.array(out)


def fit_exponent(dts, vals):
    """vals ~ A (T*-t)^p; returns p and the max relative residual of the pure power law."""
    ld, lv = np.log(dts), np.log(vals)
    p, c = np.polyfit(ld, lv, 1)
    resid = lv - (p * ld + c)
    return float(p), float(np.max(np.abs(np.expm1(resid))))


def fit_exponent_modulation_handled(dts, s_vals, vals, n_harmonics=6):
    """Fit log E = p log(T*-t) + [log-periodic series in s of period 2 log lambda].

    THIS is 'handling the modulation rather than dropping it'.  A plain OLS of log E on
    log(T*-t) is BIASED for a genuinely DSS object -- the periodic factor is correlated with the
    regressor on any finite window -- and the size of that bias is itself reported, because it is
    exactly the error a careless reader of the reviewer's arithmetic would make.  With the periodic
    factor in the design matrix the exponent is recovered without bias, and any surviving departure
    from the SS value 1/2 would be a REAL DSS exponent shift.
    """
    omega = 2.0 * math.pi / (2.0 * math.log(LAMBDA))
    cols = [np.log(dts), np.ones_like(dts)]
    for k in range(1, n_harmonics + 1):
        cols.append(np.cos(k * omega * s_vals))
        cols.append(np.sin(k * omega * s_vals))
    A = np.stack(cols, axis=1)
    coef, *_ = np.linalg.lstsq(A, np.log(vals), rcond=None)
    resid = np.log(vals) - A @ coef
    return float(coef[0]), float(np.max(np.abs(resid)))


def periodicity_of_residual(s_vals, resid):
    """Best-fit period of the residual by scanning: must land on 2 log lambda for DSS."""
    periods = np.linspace(0.4 * 2 * math.log(LAMBDA), 2.5 * 2 * math.log(LAMBDA), 4001)
    best, best_p = -np.inf, None
    r = resid - np.mean(resid)
    for P in periods:
        ph = 2 * math.pi * s_vals / P
        score = (np.dot(r, np.cos(ph)) ** 2 + np.dot(r, np.sin(ph)) ** 2)
        if score > best:
            best, best_p = score, P
    return float(best_p)


# ---------------------------------------------------------------------------------------------
# 4.  CHECK C -- what the admissible cutoff consumes, as magnitudes vs rho and alpha
# ---------------------------------------------------------------------------------------------

def cutoff_magnitudes(alpha, rho, s=0.0, nu=1.0):
    """Sizes of the objects a cutoff at radius rho introduces, at t=0 (T*=1, so y=x).

    chi = 1 on r<=rho, 0 on r>=2rho, smooth, with |chi'| <= c1/rho, |chi''| <= c2/rho^2.
    Everything is measured on the annulus rho <= r <= 2rho where the cutoff acts.
    """
    dirs, wang = _sphere_nodes()
    rad, wrad = _radial_nodes(rho, 2.0 * rho, n_shell=8, n_gl=32)
    # smooth transition chi(r) = h((2rho - r)/rho) with h the standard C^inf-ish quintic
    def chi_d1(r):
        xi = (r - rho) / rho
        return -30.0 * xi ** 2 * (1 - xi) ** 2 / rho
    def chi_d2(r):
        xi = (r - rho) / rho
        return -60.0 * xi * (1 - xi) * (1 - 2 * xi) / rho ** 2

    nl2 = 0.0     # || (u . grad chi) u ||_{L2}^2       -- nonlinear cutoff residual
    vi2 = 0.0     # || nu (2 grad chi . grad u + (lap chi) u) ||_{L2}^2  -- viscous residual
    dv2 = 0.0     # || grad chi . u ||_{L2}^2           -- divergence defect (Bogovskii source)
    h = 1e-4 * rho
    for r, wr in zip(rad, wrad):
        pts = r * dirs
        U = U_profile(pts, s, alpha)
        yhat = pts / r
        ur = np.einsum("ij,ij->i", U, yhat)                 # radial component of u
        c1, c2 = chi_d1(r), chi_d2(r)
        lap_chi = c2 + 2.0 * c1 / r
        # radial derivative of u by central difference
        dU = (U_profile((r + h) * dirs, s, alpha) - U_profile((r - h) * dirs, s, alpha)) / (2 * h)
        nl = (c1 * ur)[:, None] * U
        vi = nu * (2.0 * c1 * dU + lap_chi * U)
        w = wr * r * r
        nl2 += w * float(np.dot(wang, np.sum(nl * nl, axis=1)))
        vi2 += w * float(np.dot(wang, np.sum(vi * vi, axis=1)))
        dv2 += w * float(np.dot(wang, (c1 * ur) ** 2))
    tail_l2 = shell_integral_Lp(alpha, s, rho, 1e7 * rho, 2.0)
    tail_l3 = shell_integral_Lp(alpha, s, rho, 1e7 * rho, 3.0)
    sup_tail = float(np.max(np.linalg.norm(U_profile(rho * dirs, s, alpha), axis=-1)))
    # pressure perturbation felt at the origin from deleting the exterior mass (order of magnitude:
    # |delta p(0)| <~ (3/4pi) int_{|x|>rho} |u|^2 / |x|^3 dx, from the Calderon-Zygmund kernel)
    dp = 0.0
    rad2, wrad2 = _radial_nodes(rho, 1e6 * rho, n_shell=24, n_gl=24)
    for r, wr in zip(rad2, wrad2):
        val = np.linalg.norm(U_profile(r * dirs, s, alpha), axis=-1) ** 2
        dp += wr * r * r * float(np.dot(wang, val)) * (3.0 / (4.0 * math.pi)) / r ** 3
    return {
        "rho": rho,
        "tail_energy_L2_sq": tail_l2,
        "tail_L2_norm": math.sqrt(tail_l2),
        "tail_L3_norm": tail_l3 ** (1.0 / 3.0),
        "tail_sup_at_rho": sup_tail,
        "nonlinear_residual_L2": math.sqrt(nl2),
        "viscous_residual_L2": math.sqrt(vi2),
        "divergence_defect_L2": math.sqrt(dv2),
        "bogovskii_corrector_H1_scale": math.sqrt(dv2),
        "bogovskii_corrector_L2_scale": rho * math.sqrt(dv2),
        "pressure_perturbation_at_origin": dp,
    }


def fit_rho_exponent(rows, key):
    rs = np.array([r["rho"] for r in rows])
    vs = np.array([r[key] for r in rows])
    if np.any(vs <= 0) or not np.all(np.isfinite(vs)):
        return None
    p, _ = np.polyfit(np.log(rs), np.log(vs), 1)
    return float(p)


# ---------------------------------------------------------------------------------------------
# 5.  The Clay primary text (step (ii)) -- verbatim, from the official PDF's own text layer
# ---------------------------------------------------------------------------------------------

CLAY_VERBATIM = {
    "(4)": "|∂xα u◦ (x)| ≤ CαK (1 + |x|)−K on Rn , for any α and K",
    "(5)": "|∂xα ∂tm f (x, t)| ≤ CαmK (1 + |x| + t)−K on Rn × [0, ∞), for any α, m, K",
    "(6)": "p, u ∈ C ∞ (Rn × [0, ∞))",
    "(7)": "∫_{Rn} |u(x, t)|2 dx < C for all t ≥ 0 (bounded energy)",
    "(10)": "u(x, t) = u(x + ej , t) on R3 × [0, ∞) for 1 ≤ j ≤ n",
    "(11)": "p, u ∈ C ∞ (Rn × [0, ∞))",
    "(A)": ("Existence and smoothness of Navier-Stokes solutions on R3. Take ν > 0 and n = 3. "
            "Let u◦ (x) be any smooth, divergence-free vector field satisfying (4). Take f (x, t) "
            "to be identically zero. Then there exist smooth functions p(x, t), ui (x, t) on "
            "R3 × [0, ∞) that satisfy (1), (2), (3), (6), (7)."),
    "(C)": ("Breakdown of Navier-Stokes solutions on R3. Take ν > 0 and n = 3. Then there exist "
            "a smooth, divergence-free vector field u◦ (x) on R3 and a smooth f (x, t) on "
            "R3 × [0, ∞), satisfying (4), (5), for which there exist no solutions (p, u) of "
            "(1), (2), (3), (6), (7) on R3 × [0, ∞)."),
    "(D)": ("Breakdown of Navier-Stokes Solutions on R3/Z3. Take ν > 0 and n = 3. Then there "
            "exist a smooth, divergence-free vector field u◦ (x) on R3 and a smooth f (x, t) on "
            "R3 × [0, ∞), satisfying (8), (9), for which there exist no solutions (p, u) of "
            "(1), (2), (3), (10), (11) on R3 × [0, ∞)."),
}

REVIEWER_PARAGRAPH_CLAUSES = [
    {
        "reviewer_clause": "the Clay statement being answered is direction (b) - exhibit a breakdown",
        "verdict": "CORRECTED (labelling)",
        "primary_text": "The breakdown statement on R3 is labelled (C); (D) is the torus breakdown; "
                        "(B) is EXISTENCE on R3/Z3, not a breakdown statement at all.",
        "load_bearing": False,
        "why": "Pure labelling. It matters only because a reader chasing '(b)' in the official text "
               "lands on an existence statement and could mis-transcribe the hypotheses.",
    },
    {
        "reviewer_clause": "initial data u0 on R^3 that is smooth",
        "verdict": "CONFIRMED",
        "primary_text": "(C): 'a smooth, divergence-free vector field u◦ (x) on R3'.",
        "load_bearing": True,
        "why": "Verbatim in (C).",
    },
    {
        "reviewer_clause": "divergence-free",
        "verdict": "CONFIRMED",
        "primary_text": "(C): 'smooth, divergence-free vector field'.",
        "load_bearing": True,
        "why": "Verbatim in (C).",
    },
    {
        "reviewer_clause": "decaying faster than any polynomial",
        "verdict": "CONFIRMED AND STRENGTHENED",
        "primary_text": "(4): '|∂xα u◦(x)| ≤ CαK (1+|x|)^{-K} ... for any α and K'.",
        "load_bearing": True,
        "why": "The official condition binds EVERY DERIVATIVE ∂xα, not the field alone. The "
               "reviewer's phrase understates it: a cutoff construction owes faster-than-polynomial "
               "decay of all derivatives of the DATA, which a compactly-supported cutoff supplies "
               "trivially -- so this clause is confirmed and is NOT the binding difficulty.",
    },
    {
        "reviewer_clause": "with f = 0",
        "verdict": "REFUTED",
        "primary_text": "(C) permits 'a smooth f (x, t) on R3 × [0, ∞), satisfying (4), (5)'. "
                        "'Take f (x, t) to be identically zero' appears in (A) and (B) -- the two "
                        "EXISTENCE statements -- and in neither breakdown statement.",
        "load_bearing": True,
        "why": "The obligation is WEAKER than the document states: a breakdown candidate may carry a "
               "forcing, provided f is smooth and satisfies (5), i.e. decays faster than any "
               "polynomial in (1+|x|+t) with all x- and t-derivatives. This is a real relaxation and "
               "it is the correction most likely to change how a build is scoped. It is NOT a "
               "shortcut -- see 'f_allowance_is_not_a_shortcut' in the payload.",
    },
    {
        "reviewer_clause": "such that no smooth solution exists for all time with bounded energy",
        "verdict": "CONFIRMED",
        "primary_text": "(C): 'for which there exist no solutions (p, u) of (1), (2), (3), (6), (7) "
                        "on R3 × [0, ∞)', with (6) smoothness and (7) '∫|u(x,t)|^2 dx < C "
                        "for all t ≥ 0 (bounded energy)'.",
        "load_bearing": True,
        "why": "The bounded-energy requirement CLAY_OBLIGATIONS §4 rests on is verbatim in the "
               "official text, as numbered condition (7), with a single constant C uniform in t. "
               "§4's premise is verified.",
    },
]


def main():
    ok = True
    payload = {
        "leg": 381,
        "route": "CLOC",
        "what": "verification of CLAY_OBLIGATIONS.md §4 (the localisation clause): the reviewer's "
                "energy arithmetic under DSS modulation, and the reviewer's reading of the official "
                "Clay problem statement",
        "ceiling": "TIER 2. No link of the L1->L4 chain moved. Clay stays ~0.05%. Verifying an "
                   "obligation is not such a link.",
        "does_not": ["attempts no localisation", "builds no certified decay enclosure (leg 382, slot C)",
                     "edits no solver module", "edits no obligations file"],
        "clay_source": CLAY_SOURCE,
    }

    # ---- A. the synthetic field is what it claims to be -------------------------------------
    dss_err = check_dss_symmetry(alpha=1.0)
    div_abs, div_rel = divergence_max(alpha=1.0, s=0.0)
    payload["check_A_field_is_what_it_claims"] = {
        "dss_symmetry_max_rel_error": dss_err,
        "dss_symmetry_tolerance": 1e-12,
        "divergence_max_abs_fd4": div_abs,
        "divergence_max_relative_to_field_over_r": div_rel,
        "divergence_tolerance_relative": 1e-6,
        "lambda": LAMBDA,
        "period_in_s": 2.0 * math.log(LAMBDA),
        "can_fail": "a wrong similarity convention (exponent or the s -> s + 2 log lambda shift) "
                    "breaks the DSS identity immediately; a non-solenoidal field breaks the second.",
    }
    ok &= dss_err < 1e-12 and div_rel < 1e-6

    # ---- B0. step (i): the identity itself, checked in PHYSICAL space (not tautological) -----
    # The similarity-variable calculation and a direct quadrature of int_{|x|<=X} |u(x,t)|^2 dx are
    # different integrals on different grids in different variables. If the change of variables
    # (the (T*-t)^{-1/2} amplitude and the (T*-t)^{3/2} Jacobian) were wrong, they would disagree.
    b0_rows = []
    X_MAX = 5.0
    for dt in (0.25, 0.05, 0.01, 0.002):
        s = -math.log(dt)
        dirs, wang = _sphere_nodes()
        rad, wrad = _radial_nodes(0.0, X_MAX, n_shell=14, n_gl=24)
        phys = 0.0
        for r, wr in zip(rad, wrad):
            pts = r * dirs
            val = np.linalg.norm(u_physical(pts, T_STAR - dt, 1.2), axis=-1)
            phys += wr * r * r * float(np.dot(wang, val ** 2))
        sim = math.sqrt(dt) * shell_integral_Lp(1.2, s, 0.0, X_MAX / math.sqrt(dt), 2.0)
        b0_rows.append({"T_star_minus_t": dt, "physical_space_quadrature": phys,
                        "similarity_variable_prediction": sim,
                        "rel_disagreement": abs(phys - sim) / abs(sim)})
    payload["check_B0_identity_in_physical_space"] = {
        "alpha_used": 1.2, "ball_radius_in_x": X_MAX, "rows": b0_rows,
        "max_rel_disagreement": max(r["rel_disagreement"] for r in b0_rows),
        "statement_checked": "int_{|x|<=X} |u|^2 dx == (T*-t)^{1/2} int_{|y| <= X/sqrt(T*-t)} |U|^2 dy",
        "can_fail": "any error in the (T*-t)^{-1/2} amplitude or the (T*-t)^{3/2} Jacobian shows up "
                    "as a dt-dependent disagreement.",
    }
    ok &= max(r["rel_disagreement"] for r in b0_rows) < 1e-8

    # ---- B. step (i): the energy exponent, SS vs DSS -----------------------------------------
    alpha_fin = 2.5                      # finite-energy case (alpha > 3/2) so both sides are finite
    curves = {}
    for mode in ("SS", "DSS"):
        arr = energy_curve(alpha_fin, mode, n_t=96, dt_hi=0.3, n_periods=6)
        p_naive, resid = fit_exponent(arr[:, 0], arr[:, 2])
        p, fit_resid = fit_exponent_modulation_handled(arr[:, 0], arr[:, 1], arr[:, 2])
        curves[mode] = {"exponent": p, "exponent_naive_modulation_dropped": p_naive,
                        "modulation_handled_fit_max_log_residual": fit_resid,
                        "max_rel_residual_of_pure_power_law": resid,
                        "G_min": float(np.min(arr[:, 3])), "G_max": float(np.max(arr[:, 3]))}
        curves[mode]["_arr"] = arr
    ss, ds = curves["SS"], curves["DSS"]
    lv = np.log(ds["_arr"][:, 2])
    ld = np.log(ds["_arr"][:, 0])
    pp, cc = np.polyfit(ld, lv, 1)
    resid = lv - (pp * ld + cc)
    period_fit = periodicity_of_residual(ds["_arr"][:, 1], resid)
    payload["check_B_energy_exponent_SS_vs_DSS"] = {
        "alpha_used": alpha_fin,
        "DSS_exponent_naive_fit_modulation_DROPPED": ds["exponent_naive_modulation_dropped"],
        "naive_fit_bias_percent": 100.0 * abs(ds["exponent_naive_modulation_dropped"] - 0.5) / 0.5,
        "modulation_handled_fit_max_log_residual": ds["modulation_handled_fit_max_log_residual"],
        "DSS_exponent_note": "the period-locked figure below is the one that answers the gate: a fit "
                             "over a whole number of DSS periods averages the log-periodic factor out "
                             "exactly, so a surviving departure from 1/2 would be a real exponent "
                             "shift. The naive fit's departure is a windowing artifact of the "
                             "modulation, and its size is a measure of how badly one is misled by "
                             "dropping the modulation instead of handling it.",
        "SS_exponent": ss["exponent"],
        "DSS_exponent": ds["exponent"],
        "predicted_exponent": 0.5,
        "DSS_over_SS_exponent_ratio": ds["exponent"] / ss["exponent"],
        "SS_max_rel_residual": ss["max_rel_residual_of_pure_power_law"],
        "DSS_max_rel_residual": ds["max_rel_residual_of_pure_power_law"],
        "DSS_G_oscillation_relative_amplitude": (ds["G_max"] - ds["G_min"]) / ds["G_min"],
        "DSS_residual_best_fit_period_in_s": period_fit,
        "predicted_period_2_log_lambda": 2.0 * math.log(LAMBDA),
        "period_relative_error": abs(period_fit - 2 * math.log(LAMBDA)) / (2 * math.log(LAMBDA)),
        "reading": "The DSS exponent equals the SS exponent EXACTLY: ratio 1 to fit precision, no "
                   "factor. The modulation does not move the exponent -- it converts the constant "
                   "int|U|^2 dy into a log-periodic G(s) of period 2 log lambda, which shows up as a "
                   "residual around the pure power law, not as a different power.",
        "can_fail": "if the DSS exponent differed from 1/2 the ratio would not be 1; if the "
                    "modulation were merely noise the residual period would not land on 2 log lambda.",
    }
    ok &= abs(ss["exponent"] - 0.5) < 1e-6 and abs(ds["exponent"] - 0.5) < 1e-6
    ok &= abs(period_fit - 2 * math.log(LAMBDA)) / (2 * math.log(LAMBDA)) < 0.05
    ok &= ss["max_rel_residual_of_pure_power_law"] < 1e-3          # SS: pure power law
    ok &= ds["max_rel_residual_of_pure_power_law"] > 1e-2          # DSS: genuinely modulated

    # ---- B2. the truncated law, which is valid for every alpha ------------------------------
    rows = []
    for a in (0.8, 1.0, 1.2, 1.4):
        arr = energy_curve(a, "SS", rho=1.0, n_t=24, dt_lo=1e-9, dt_hi=1e-5)
        p, _ = fit_exponent(arr[:, 0], arr[:, 2])
        rows.append({"alpha": a, "fixed_ball_energy_exponent_measured": p,
                     "predicted_alpha_minus_1": a - 1.0,
                     "abs_error": abs(p - (a - 1.0))})
    payload["check_B2_truncated_energy_law"] = {
        "rho": 1.0,
        "rows": rows,
        "max_abs_error": max(r["abs_error"] for r in rows),
        "reading": "E_rho(t) ~ rho^{3-2alpha} (T*-t)^{alpha-1}. At the banked Type-I exponent "
                   "alpha = 1 the fixed-ball energy is TIME-INDEPENDENT -- the critical case -- so "
                   "the divergence of the total energy is a pure far-field statement, not a "
                   "concentration statement.",
        "why_this_matters": "The reviewer's identity is between two infinities when U is not in L^2, "
                            "so as written it cannot carry the conditional. The truncated law is "
                            "finite for every alpha and reduces to the reviewer's statement when both "
                            "sides are finite. Same conclusion, valid derivation.",
    }
    ok &= max(r["abs_error"] for r in rows) < 0.05

    # ---- B3. the L^p thresholds ---------------------------------------------------------------
    thresholds = []
    for p_ in (2.0, 3.0):
        for a in (0.9, 1.0, 1.1, 1.4, 1.5, 1.6, 2.2):
            near = shell_integral_Lp(a, 0.0, 1.0, 1e3, p_)
            far = shell_integral_Lp(a, 0.0, 1e3, 1e6, p_)
            thresholds.append({"p": p_, "alpha": a, "shell_1_to_1e3": near,
                               "shell_1e3_to_1e6": far, "ratio_far_over_near": far / near,
                               "converges_predicted": a > 3.0 / p_})
    payload["check_B3_Lp_thresholds"] = {
        "rows": thresholds,
        "L2_threshold_alpha": 1.5,
        "L3_threshold_alpha": 1.0,
        "banked_type_I_alpha": 1.0,
        "type_I_source": "Chae-Wolf arXiv:1610.09464 Thm 1.1, carried by leg 253's full-text read and "
                         "banked in leg 260: |U(y)| <= C/(1+|y|) for every lambda-DSS solution",
        "deficit_to_L2_in_exponent": 0.5,
        "required_over_available_exponent_ratio": 1.5,
        "reading": "L^2 needs alpha > 3/2; the a-priori Type-I bound gives alpha = 1 exactly. The "
                   "certified exponent would have to be 1.5x the a-priori one. At alpha = 1 the "
                   "critical L^3 tail is log-divergent, so the discarded tail is not small in ANY "
                   "critical norm.",
    }

    # ---- C. step (iii): what the cutoff analysis consumes, as magnitudes ---------------------
    cut = {}
    for a in (1.0, 1.25, 1.6):
        rowset = [cutoff_magnitudes(a, rho) for rho in (10.0, 30.0, 100.0, 300.0, 1000.0)]
        fits = {k: fit_rho_exponent(rowset, k) for k in
                ("tail_L2_norm", "tail_L3_norm", "tail_sup_at_rho", "nonlinear_residual_L2",
                 "viscous_residual_L2", "divergence_defect_L2", "bogovskii_corrector_L2_scale",
                 "pressure_perturbation_at_origin")}
        cut[f"alpha={a}"] = {
            "rows": rowset,
            "measured_rho_exponents": fits,
            "predicted_rho_exponents": {
                "tail_L2_norm": (3 - 2 * a) / 2 if a < 1.5 else None,
                "tail_L3_norm": (3 - 3 * a) / 3 if a < 1.0 else (1 - a),
                "tail_sup_at_rho": -a,
                "nonlinear_residual_L2": 0.5 - 2 * a,
                "viscous_residual_L2": -a - 0.5,
                "divergence_defect_L2": 0.5 - a,
                "bogovskii_corrector_L2_scale": 1.5 - a,
                "pressure_perturbation_at_origin": -2 * a,
            },
        }
    # C2: at alpha = 1 the CRITICAL L^3 tail is log-divergent -- shown, not asserted, by widening
    # the truncation window and watching the cube of the norm grow LINEARLY in the number of decades.
    c2 = []
    for k in (2, 4, 6, 8, 10):
        v = shell_integral_Lp(1.0, 0.0, 100.0, 100.0 * 10.0 ** k, 3.0)
        c2.append({"decades_of_window": k, "tail_L3_cubed": v, "tail_L3_norm": v ** (1.0 / 3.0)})
    diffs = [c2[i + 1]["tail_L3_cubed"] - c2[i]["tail_L3_cubed"] for i in range(len(c2) - 1)]
    per_decade = [d / 2.0 for d in diffs]
    payload["check_C2_critical_L3_tail_is_log_divergent_at_alpha_1"] = {
        "rows": c2,
        "increment_per_decade": per_decade,
        "increment_per_decade_spread": (max(per_decade) - min(per_decade)) / max(per_decade),
        "reading": "the cube of the critical-norm tail grows by a CONSTANT amount per decade of "
                   "window, i.e. logarithmically without bound: at the banked Type-I exponent the "
                   "discarded far field is not small in L^3 no matter how far out the cutoff is put.",
    }
    ok &= (max(per_decade) - min(per_decade)) / max(per_decade) < 1e-3

    payload["check_C_cutoff_magnitudes"] = {
        "by_alpha": cut,
        "what_the_analysis_consumes": {
            "input_1_certified_decay_exponent": {
                "who_builds_it": "leg 382 (slot C), Route-DEXC -- NOT this leg",
                "form_needed": "a two-sided enclosure [alpha_lo, alpha_hi]; every magnitude below "
                               "depends only on alpha_lo",
                "thresholds_that_matter": {"fixed_ball_energy_decays": "alpha_lo > 1",
                                           "critical_L3_tail_finite": "alpha_lo > 1",
                                           "global_L2_finite": "alpha_lo > 1.5"},
                "currently_available": "alpha = 1 a priori (Type-I, Chae-Wolf), fitted per candidate "
                                       "by solver/dssp_screen.py::fitted_far_field_decay_exponent; "
                                       "fitted is not sufficient (CLAY_OBLIGATIONS §8 bullet 2)",
            },
            "input_2_perturbation_size_vs_cutoff_radius": {
                "nonlinear_cutoff_residual_L2": "~ C^2 rho^{1/2 - 2 alpha}",
                "viscous_cutoff_residual_L2": "~ nu C rho^{-alpha - 1/2}",
                "divergence_defect_L2": "~ C rho^{1/2 - alpha} (Bogovskii source; corrector H^1 the "
                                        "same size, corrector L^2 ~ C rho^{3/2 - alpha})",
                "discarded_tail_L2": "~ C rho^{3/2 - alpha}, DIVERGENT for alpha <= 3/2",
                "discarded_tail_L3_critical": "~ C rho^{1 - alpha}, log-divergent at alpha = 1",
                "pressure_perturbation_at_origin": "~ C^2 rho^{-2 alpha}, to be compared with the "
                                                   "profile's own pressure scale (T*-t)^{-1}: ratio "
                                                   "rho^{-2 alpha}(T*-t) -> 0, so the pressure "
                                                   "non-locality is NOT the obstruction",
                "coincidence_at_alpha_1": "at exactly the Type-I exponent the nonlinear and viscous "
                                          "cutoff residuals scale identically, both rho^{-3/2}; for "
                                          "alpha > 1 the nonlinear one is the smaller of the two",
            },
        },
        "the_obligation_is_not_discharged_by_this": "The residuals go to zero with rho, but smallness "
            "of a residual is not persistence of a blow-up. What must be shown is that the localised "
            "solution still loses smoothness at a finite time, over a time interval of length ~T*, "
            "with the cutoff sitting at similarity radius rho/sqrt(T*-t) -> infinity. That is §5, "
            "and this leg does not attempt it.",
    }

    # ---- D. step (ii): the primary text --------------------------------------------------------
    payload["check_D_clay_primary_text"] = {
        "source": CLAY_SOURCE,
        "verbatim_conditions": CLAY_VERBATIM,
        "reviewer_paragraph_clause_ledger": REVIEWER_PARAGRAPH_CLAUSES,
        "counts": {
            "confirmed": sum(1 for c in REVIEWER_PARAGRAPH_CLAUSES if c["verdict"].startswith("CONFIRMED")),
            "corrected": sum(1 for c in REVIEWER_PARAGRAPH_CLAUSES if c["verdict"].startswith("CORRECTED")),
            "refuted": sum(1 for c in REVIEWER_PARAGRAPH_CLAUSES if c["verdict"] == "REFUTED"),
            "total": len(REVIEWER_PARAGRAPH_CLAUSES),
        },
        "bounded_energy_premise_of_section_4": "VERIFIED -- condition (7) verbatim, uniform in t.",
        "f_allowance_is_not_a_shortcut":
            "(C) permitting a forcing does NOT let the cutoff residual be absorbed into f and the "
            "obligation declared discharged. To do that one would DEFINE f as the residual of the "
            "truncated field, but (C) requires f smooth on R3 x [0, infinity) satisfying (5) while "
            "requiring that NO smooth bounded-energy solution exists on [0, infinity) -- so f must be "
            "specified past T*, where the candidate field does not exist, and cutting f off in time "
            "before T* removes exactly the forcing that was making the field a solution. The "
            "relaxation is real and should be recorded; it does not discharge §4 or §5.",
        "alternative_target_noted": "(D), the R3/Z3 breakdown statement, carries NO decay condition "
            "and NO bounded-energy condition -- its acceptance conditions are (10) periodicity and "
            "(11) smoothness only. A torus target would make §4 vacuous by construction. This is "
            "recorded as an OPTION WITH ITS OWN COST, not a recommendation: the route-4 object is a "
            "DSS profile on R3 and is not periodic, and re-targeting would re-open §2's rigidity "
            "screen from scratch. No leg is authorised by this note.",
    }

    # ---- E. the gate -------------------------------------------------------------------------
    arithmetic_survives = (abs(ds["exponent"] - 0.5) < 2e-2
                           and abs(ds["exponent"] / ss["exponent"] - 1.0) < 2e-2)
    bounded_energy_confirmed = True     # condition (7), verbatim
    payload["gate"] = {
        "question": "Does the reviewer's arithmetic survive (i) with the DSS modulation handled, AND "
                    "does (ii) confirm the bounded-energy reading against the primary text?",
        "answer": "YES, WITH ONE REFUTED SIDE-CLAUSE AND ONE REPAIRED DERIVATION STEP",
        "i_arithmetic_survives": arithmetic_survives,
        "i_dss_exponent_vs_ss_exponent": "IDENTICAL, ratio 1 (no factor). The log-periodic modulation "
                                         "enters as a bounded periodic prefactor G(s), period "
                                         "2 log lambda, not as an exponent shift.",
        "i_repair_required": "The reviewer's identity is vacuous exactly in the case of interest "
                             "(both sides +infinity when U is not in L^2). Replace it with the "
                             "truncated law E_rho(t) ~ rho^{3-2alpha}(T*-t)^{alpha-1}. Same "
                             "conclusion, valid in the case that matters.",
        "ii_bounded_energy_confirmed": bounded_energy_confirmed,
        "ii_refuted_clause": "'with f = 0' is NOT in the breakdown statement (C); f may be any smooth "
                             "forcing satisfying (4),(5). f = 0 belongs to the EXISTENCE statements "
                             "(A),(B).",
        "ii_labelling_correction": "the breakdown-on-R3 statement is (C), not '(b)'.",
        "consequence": "CLAY_OBLIGATIONS §4 is VERIFIED AS A SPECIFICATION: the localisation "
                       "problem is confirmed load-bearing and its inputs are named. Routed to "
                       "integration for the DRAFT-UNVERIFIED header (integration's edit, not this "
                       "leg's), together with the two corrections above.",
        "clay_movement": "none. Clay stays ~0.05%.",
    }

    for k in ("SS", "DSS"):
        curves[k].pop("_arr", None)

    text = json.dumps(payload, indent=2, sort_keys=False)
    payload["self_hash"] = hashlib.sha256(text.encode()).hexdigest()[:16]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=False))

    a = payload["check_A_field_is_what_it_claims"]
    b = payload["check_B_energy_exponent_SS_vs_DSS"]
    print("LEG 381 / ROUTE-CLOC -- verifying CLAY_OBLIGATIONS §4")
    print()
    print("A. Is the synthetic object actually lambda-DSS and divergence-free?")
    print(f"   DSS symmetry max rel error : {a['dss_symmetry_max_rel_error']:.3e}  (tol 1e-12)")
    print(f"   div u, max rel (4th-order) : {a['divergence_max_relative_to_field_over_r']:.3e}  (tol 1e-6)")
    print()
    print("B. (i) THE ENERGY EXPONENT -- does (T*-t)^{1/2} survive genuine DSS?")
    print(f"   SS  exponent               : {b['SS_exponent']:.9f}   (predicted 0.5)")
    print(f"   DSS exponent, modulation   : {b['DSS_exponent']:.9f}   (predicted 0.5)")
    print(f"     HANDLED (in the fit)     ")
    print(f"   DSS exponent, modulation   : {b['DSS_exponent_naive_fit_modulation_DROPPED']:.9f}"
          f"   <-- biased by {b['naive_fit_bias_percent']:.2f}%")
    print(f"     DROPPED (naive OLS)      ")
    print(f"   DSS/SS ratio               : {b['DSS_over_SS_exponent_ratio']:.9f}   <-- THE FACTOR")
    print(f"   SS  residual (pure power)  : {b['SS_max_rel_residual']:.3e}")
    print(f"   DSS residual (modulation)  : {b['DSS_max_rel_residual']:.3e}  amplitude "
          f"{b['DSS_G_oscillation_relative_amplitude']:.3f}")
    print(f"   residual period in s       : {b['DSS_residual_best_fit_period_in_s']:.6f}  vs "
          f"2 log lambda = {b['predicted_period_2_log_lambda']:.6f}")
    print()
    print("B2. The truncated law (valid for every alpha, unlike the reviewer's as written)")
    for r in payload["check_B2_truncated_energy_law"]["rows"]:
        print(f"   alpha={r['alpha']:.2f}  fixed-ball exponent {r['fixed_ball_energy_exponent_measured']:+.4f}"
              f"   predicted {r['predicted_alpha_minus_1']:+.4f}   err {r['abs_error']:.1e}")
    print()
    print("B3. Thresholds: L^2 needs alpha > 1.5; banked Type-I gives alpha = 1.0 "
          "(deficit 0.5, ratio 1.5x)")
    print()
    print("C. (iii) What the cutoff analysis consumes -- measured rho-exponents at alpha = 1.0")
    m = cut["alpha=1.0"]["measured_rho_exponents"]
    pr = cut["alpha=1.0"]["predicted_rho_exponents"]
    for k in ("tail_sup_at_rho", "divergence_defect_L2", "nonlinear_residual_L2",
              "viscous_residual_L2", "pressure_perturbation_at_origin"):
        got = m[k]
        pred = pr[k]
        print(f"   {k:<34} measured {got:+.4f}   predicted {pred:+.4f}")
    print()
    print("D. (ii) The official Clay text, clause by clause")
    for c in REVIEWER_PARAGRAPH_CLAUSES:
        print(f"   {c['verdict']:<26} {c['reviewer_clause'][:60]}")
    print()
    print("E. GATE")
    print(f"   {payload['gate']['answer']}")
    print(f"   DSS vs SS exponent: {payload['gate']['i_dss_exponent_vs_ss_exponent'][:60]}...")
    print()
    print(f"wrote {OUT.relative_to(ROOT)}")
    print("SELF-TESTS: " + ("ALL PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
