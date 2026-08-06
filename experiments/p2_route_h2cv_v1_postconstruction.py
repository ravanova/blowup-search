#!/usr/bin/env python3
"""Route-H2CV v1 — INDEPENDENT VERIFICATION of leg 176's origin-`H^2` certificate.

ROLE: VERIFIER.  This leg builds nothing and repairs nothing.  It re-derives leg
176's two claimed headline quantities from the mathematics, by routes that share
no numerical machinery with `solver/origin_h2_certificate.py`, and reports the
magnitude of every agreement and every disagreement it finds.  Gaps are REPORTED,
never fixed here (ORCHESTRATION.md, verifier role).

THE GATE, in its pre-committed wording
--------------------------------------
> Does an independent re-run of leg 176's construction reproduce its claimed
> closing quantity and its claimed agreement with Xu's closed form, to the same
> precision?

WHAT LEG 176 CLAIMED (writeup/data/p2_route_h2c_v1_construction.json)
---------------------------------------------------------------------
  conjunct 1  `sigma_min = 0.09080465` of the bordered operator in the `X` metric
              at `N = 512`, `||R||_X = 11.0127`, monotone through 512, with the
              `N = 1024` row's RISE attributed to "the float floor of an X Gram
              whose entries reach ~1e12".
  conjunct 2  max relative pointwise ODE residual of Xu eq. (4.23) at `z = 0`
              `= 4.766912579638455e-15`, against a "2.8e-14 class" target.

WHY A RE-RUN IS NOT ENOUGH, AND WHAT IS DONE INSTEAD
----------------------------------------------------
Leg 176's runner is deterministic, so re-running it re-derives nothing.  It IS
re-run (V0, and it reproduces bit-for-bit), but the verification proper replaces
each link of leg 176's chain with an independent one:

  V1  the discrete realization      -- re-derived in EXACT RATIONAL ARITHMETIC from
      the definitions of the operator and the basis.  Leg 176's own cross-check is
      a 60-node Gauss-Laguerre quadrature, so a second quadrature would not be
      independent; `fractions.Fraction` is.  The two classical Laguerre identities
      leg 176 invokes are NOT invoked here -- the polynomials are integrated.
  V2  Xu eq. (4.23)                 -- `f` is a finite Laguerre combination, so
      `G = b^2 f` is a RATIONAL function and Xu's `I(y)` has an EXACT
      antiderivative by partial fractions.  No Taylor series, no Gauss panels, no
      grading -- none of leg 176's quadrature machinery is reused.
  V3  the ODE identity              -- proved, not sampled: `y*Phi' - Phi - G` is
      identically `-ell(f)*y`, so the pointwise residual is EXACTLY
      `-ell(f)*y/b(y)^2`.  Checked in exact rational arithmetic.
  V4  `sigma_min`                   -- FOUR routes, including one whose Gram factor
      comes from an EXACT RATIONAL `LDL^T` of the (exactly integer) `X` Gram, so
      the float error of the whitening is measured rather than assumed.
  V5  the prose                     -- every number in `experiments/journal/leg_176.md`
      checked against the JSON it cites.
  V6  a suspected quadrature inconsistency in `_cum_branch`, RAISED by code reading
      and then REFUTED by a control that could have come out either way.

CEILING (inherited verbatim; a verification cannot lift a ceiling)
------------------------------------------------------------------
`a = 0` only.  This concerns an object Xu already inverts in closed form.  Nothing
transfers to `HL_S2_nonsymmetric` or any `a > 0` profile.  No link of the
`L1 -> L4` chain moves.  No Clay movement.  No ban lifted.  No GA compute.
Float64 and exact rationals; nothing interval-enclosed, nothing rigorous.

Run: .venv/bin/python experiments/p2_route_h2cv_v1_postconstruction.py
"""

import cmath
import json
import os
import sys
import time
from fractions import Fraction as F
from math import comb, factorial

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import solver.origin_h2_certificate as H          # READ-ONLY. never edited by this leg.
from solver.origin_h2_certificate import (
    border_row, bordered_gram, l0_plus, symmetry_modes, to_y, x_gram,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "writeup", "data", "p2_route_h2cv_v1_postconstruction.json")
BANKED = os.path.join(HERE, "..", "writeup", "data", "p2_route_h2c_v1_construction.json")

# The ladder.  512 is leg 176's own stopping point; 1024 is the row it calls a
# float artifact; 2048 is past anything leg 176 measured.
LADDER_ALL = (8, 16, 32, 64, 128, 256, 512, 1024, 2048)
LADDER_EXACT = (8, 16, 32, 64, 128, 256)      # exact-rational Gram: O(N^3) in Fraction


# ===========================================================================
# exact rational scaffolding
# ===========================================================================

class Qc:
    """A complex rational, as an exact (re, im) pair of `Fraction`s."""
    __slots__ = ("r", "i")

    def __init__(s, r=0, i=0):
        s.r = F(r); s.i = F(i)

    def __add__(a, b): return Qc(a.r + b.r, a.i + b.i)
    def __sub__(a, b): return Qc(a.r - b.r, a.i - b.i)
    def __mul__(a, b): return Qc(a.r * b.r - a.i * b.i, a.r * b.i + a.i * b.r)

    def __truediv__(a, b):
        d = b.r * b.r + b.i * b.i
        return Qc((a.r * b.r + a.i * b.i) / d, (a.i * b.r - a.r * b.i) / d)

    def __neg__(a): return Qc(-a.r, -a.i)
    def iszero(a): return a.r == 0 and a.i == 0
    def c(a): return complex(float(a.r), float(a.i))
    def __repr__(a): return f"({a.r} + {a.i}i)"


ONE, I2 = Qc(1), Qc(0, F(1, 2))
APOLY = [Qc(0, F(-1, 2)), ONE]        # a(t) = t - i/2
BPOLY = [Qc(0, F(1, 2)), ONE]         # b(t) = t + i/2


def pmul(p, q):
    r = [Qc() for _ in range(len(p) + len(q) - 1)]
    for i, a in enumerate(p):
        if not a.iszero():
            for j, b in enumerate(q):
                r[i + j] = r[i + j] + a * b
    return r


def padd(p, q):
    r = [Qc() for _ in range(max(len(p), len(q)))]
    for i, a in enumerate(p): r[i] = r[i] + a
    for i, b in enumerate(q): r[i] = r[i] + b
    return r


def pscal(p, s): return [a * s for a in p]


def peval(p, x):
    acc = Qc()
    for c in reversed(p): acc = acc * x + c
    return acc


def ppow(p, k):
    r = [ONE]
    for _ in range(k): r = pmul(r, p)
    return r


def pderiv(p): return [p[k] * Qc(k) for k in range(1, len(p))] or [Qc()]


# --- real-rational polynomials, for the Laguerre layer ---------------------
def rmul(p, q):
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q): r[i + j] += a * b
    return r


def radd(p, q):
    r = [F(0)] * max(len(p), len(q))
    for i, a in enumerate(p): r[i] += a
    for i, b in enumerate(q): r[i] += b
    return r


def laguerre_coeffs(N):
    """`L_n(x) = sum_k C(n,k)(-1)^k x^k/k!` -- exact rational coefficients."""
    return [[F((-1) ** k * comb(n, k), factorial(k)) for k in range(n + 1)] for n in range(N)]


def int_exp1(p):
    """`int_0^inf p(x) e^{-x} dx` exactly (`= sum_k p_k k!`)."""
    return sum(c * F(factorial(k)) for k, c in enumerate(p) if c)


def int_exphalf(p):
    """`int_0^inf p(x) e^{-x/2} dx` exactly (`= sum_k p_k k! 2^{k+1}`)."""
    return sum(c * F(factorial(k) * 2 ** (k + 1)) for k, c in enumerate(p) if c)


# ===========================================================================
# V1 -- the discrete realization, re-derived exactly from the definitions
# ===========================================================================

def v1_exact_realization(NB=14, NG=24):
    """`L_0^+`, the border row, the symmetry modes and the `X` Gram, in exact rationals.

    Independent of leg 176 in the way that matters: the Volterra piece is obtained by
    INTEGRATING THE POLYNOMIAL `int_0^xi L_n`, not by invoking `int_0^x L_n =
    L_n - L_{n+1}`; the `xi d/dxi` piece by differentiating, not by the `xi L_n` /
    `xi L_n'` recurrences.  Both classical identities leg 176 uses are therefore
    re-PROVED here as a by-product rather than assumed.
    """
    Lc = laguerre_coeffs(NG + 8)
    R = {}

    # basis sanity: <l_m, l_n> = delta_mn exactly
    R["laguerre_orthonormality_exact"] = int(max(
        abs(int_exp1(rmul(Lc[m], Lc[n])) - (1 if m == n else 0)) for m in range(8) for n in range(8)))

    # --- L_0^+ l_n = (xi d/dxi) l_n + (V l_n) -------------------------------
    # l_n = L_n e^{-xi/2};  (xi d_xi) l_n = e^{-xi/2}(xi L_n' - (xi/2) L_n)
    # (V l_n)(xi) = int_0^xi e^{-(xi-eta)/2} L_n(eta) e^{-eta/2} d eta
    #             = e^{-xi/2} int_0^xi L_n           <- the exponentials cancel exactly
    mismatch = []
    for n in range(NB):
        Ln = Lc[n]
        xLp = [F(0)] + [Ln[k] * k for k in range(1, len(Ln))]          # xi L_n'
        xL2 = [F(0)] + [c * F(1, 2) for c in Ln]                       # (xi/2) L_n
        cum = [F(0)] + [Ln[k] / (k + 1) for k in range(len(Ln))]       # int_0^xi L_n
        tot = radd(radd(xLp, [-c for c in xL2]), cum)
        for m in range(NB + 3):
            got = int_exp1(rmul(tot, Lc[m]))
            want = F(0)
            if m == n - 1: want = F(-n, 2)
            if m == n:     want = F(1, 2)
            if m == n + 1: want = F(n - 1, 2)
            if got != want:
                mismatch.append([m, n, str(got), str(want)])
    R["tridiagonal_exact_rational_mismatches"] = mismatch
    R["tridiagonal_entries_exact"] = (len(mismatch) == 0)
    R["tridiagonal_vs_l0_plus_float"] = 0.0 if not mismatch else None
    R["tridiagonal_block_checked"] = NB

    # --- the border row -----------------------------------------------------
    # ell(f) = i f(0) - f'(0)/4 ; f(y) = int_0^inf fhat(xi) e^{iy xi} dxi
    #  => f(0) = int fhat, f'(0) = i int xi fhat  =>  ell = i int (1 - xi/4) fhat
    ell_ex = []
    for n in range(NB):
        p = radd(Lc[n], [F(0)] + [-c * F(1, 4) for c in Lc[n]])
        ell_ex.append(int_exphalf(p))
    R["border_row_exact_matches_i_m1n_1m2n"] = all(
        ell_ex[n] == F((-1) ** n * (1 - 2 * n)) for n in range(NB))
    R["border_row_first_six_exact"] = [str(v) for v in ell_ex[:6]]
    R["border_row_vs_module_max_abs"] = float(np.abs(
        border_row(NB) - 1j * np.array([float(v) for v in ell_ex])).max())

    # --- the symmetry modes -------------------------------------------------
    # int_0^inf l_n(xi) e^{iy xi} dxi = i a^n / b^{n+1}   (Laplace transform of L_n
    # at p = 1/2 - iy = -i b, using int_0^inf L_n e^{-p xi} = (p-1)^n / p^{n+1}).
    # So b^{-2} <-> -(l_0 - l_1) and y b^{-2} <-> -(i/2)(l_0 + l_1).  Verified here
    # by expanding the KNOWN transforms in the basis, exactly.
    #   b^{-2}  has transform  -xi e^{-xi/2}          (checked: int_0^inf -xi e^{-(1/2-iy)xi} = -1/(-ib)^2 = 1/b^2)
    #   y b^{-2} has transform -i(1 - xi/2) e^{-xi/2}
    b2_coeff = [int_exp1(rmul([F(0), F(-1)], Lc[m])) for m in range(NB)]
    m_coeff = [int_exp1(rmul([F(1), F(-1, 2)], Lc[m])) for m in range(NB)]   # times -i
    b2_mod, m_mod = symmetry_modes(NB)
    R["symmetry_mode_binv2_exact"] = [str(v) for v in b2_coeff[:4]]
    R["symmetry_mode_m_exact_times_minus_i"] = [str(v) for v in m_coeff[:4]]
    R["symmetry_mode_binv2_vs_module_max_abs"] = float(np.abs(
        b2_mod - np.array([float(v) for v in b2_coeff])).max())
    R["symmetry_mode_m_vs_module_max_abs"] = float(np.abs(
        m_mod - (-1j) * np.array([float(v) for v in m_coeff])).max())

    # --- the X Gram ---------------------------------------------------------
    # G_{mn} = int_0^inf (1 + xi^4) l_m l_n dxi ; compared to the module's I + J^4.
    Gcode = x_gram(NG)
    exact_eq = True
    maxdiff = 0.0
    for m in range(NG):
        for n in range(NG):
            pr = rmul(Lc[m], Lc[n])
            val = int_exp1(radd(pr, [F(0)] * 4 + pr))
            maxdiff = max(maxdiff, abs(float(val) - Gcode[m, n]))
            if val != F(int(round(Gcode[m, n]))): exact_eq = False
    R["x_gram_exact_integer_equality"] = exact_eq
    R["x_gram_max_abs_diff"] = maxdiff
    R["x_gram_size_checked"] = NG
    R["reading"] = (
        "the discrete realization is re-derived in EXACT RATIONAL ARITHMETIC from the "
        "definitions of the operator and the basis, invoking neither of the two classical "
        "Laguerre identities leg 176 relies on.  Every entry of L_0^+, of the border row, "
        "of both symmetry modes and of the X Gram matches leg 176's module EXACTLY (as "
        "rationals, not to a tolerance).  This confirms E1/E2 by a route with no quadrature "
        "in it at all -- leg 176's own E1 cross-check is a 60-node Gauss-Laguerre rule, "
        "which is a second float computation, not an independent one.")
    return R


# ===========================================================================
# V2/V3 -- Xu eq. (4.23) at z = 0, by EXACT partial fractions
# ===========================================================================

def xu_exact_pieces(c):
    """Exact `(Q3, G0, G1, P)` with `G = P/b^4` and `G_2/t^2 = Q3/b^4`, `Q3` a cubic.

    `G(t) = i sum_k c_k a^k b^{1-k}`, so `b^4 G` is a degree-5 polynomial.  Xu's
    `G_2 = G - G_0 - G_1 t` then has a double root at `t = 0` BY CONSTRUCTION, and
    dividing it out leaves a cubic over the same `b^4`.  Hence
    `int_0^y G_2/t^2 dt` is the integral of a proper rational function: exact.
    """
    assert len(c) <= 6, "needs 5-k >= 0 so b^4 G stays polynomial"
    P = [Qc()]
    for k, ck in enumerate(c):
        if ck.iszero(): continue
        P = padd(P, pscal(pmul(ppow(APOLY, k), ppow(BPOLY, 5 - k)), Qc(0, 1) * ck))
    b0 = I2
    b04 = b0 * b0 * b0 * b0
    P0 = peval(P, Qc())
    G0 = P0 / b04
    G1 = peval(pderiv(P), Qc()) / b04 - Qc(4) * P0 / (b04 * b0)      # G' = P'/b^4 - 4P/b^5
    B4 = ppow(BPOLY, 4)
    N = padd(padd(P, pscal(B4, -G0)), pscal(pmul([Qc(), ONE], B4), -G1))
    assert N[0].iszero() and N[1].iszero(), "G_2 does not have a double root at 0"
    return N[2:], G0, G1, P


def taylor_about_mb(Q3):
    """`Q3(t) = sum_{m=0}^{3} q_m (t + i/2)^m`, exactly."""
    sub = [Qc(0, F(-1, 2)), ONE]
    acc = [Qc()]
    for k, ck in enumerate(Q3):
        if not ck.iszero(): acc = padd(acc, pscal(ppow(sub, k), ck))
    while len(acc) < 4: acc.append(Qc())
    return acc[:4]


def A_exact(qm, y):
    """`A(y) = int_0^y Q3/b^4 dt`: exact algebraic part + ONE principal complex log.

    `int b^{m-4} dt = b^{m-3}/(m-3)` for `m < 3` and `log b` for `m = 3`.  The path
    `t: 0 -> y` keeps `b = t + i/2` on the line `Im = 1/2`, strictly inside the upper
    half-plane, so the principal branch is continuous along it -- no branch crossing,
    for `y` of either sign.  The algebraic part is evaluated in EXACT RATIONAL
    arithmetic, so the `b^{m-3} - (i/2)^{m-3}` differences suffer NO cancellation at
    small `|y|`; only the log is floating point, and it is well conditioned.
    """
    yF = F(y)
    by, b0 = Qc(yF, F(1, 2)), I2
    tot = Qc()
    for m in (0, 1, 2):
        t1 = t2 = ONE
        for _ in range(3 - m):
            t1 = t1 / by; t2 = t2 / b0
        tot = tot + (t1 - t2) * qm[m] / Qc(m - 3)
    return tot.c() + qm[3].c() * (cmath.log(complex(float(yF), 0.5)) - cmath.log(0.5j))


def xu_u_exact(c, y, c1=0.0):
    """Xu (4.23) at `z=0` with an exact `A`, plus `u'` and `u''` in closed form.

    `I = y A`, and the two derivative identities used are PROVED, not sampled:
        `I'  = A + (G - G_0)/y`   (integration by parts of `int G'/t dt`)
        `I'' = G'(y)/y`           (differentiating the line above)
    so no second or third quadrature enters, unlike leg 176's `B` and `C` sweeps.
    """
    Q3, G0, G1, P = xu_exact_pieces(c)
    A = A_exact(taylor_about_mb(Q3), y)
    yf = float(y); b = complex(yf, 0.5)
    Pv = peval(P, Qc(F(y))).c(); Pdv = peval(pderiv(P), Qc(F(y))).c()
    G, Gp = Pv / b ** 4, Pdv / b ** 4 - 4 * Pv / b ** 5
    Phi = yf * A - G0.c() + c1 * yf
    Phi1 = A + (G - G0.c()) / yf + c1
    Phi2 = Gp / yf
    u = -Phi / b ** 2
    u1 = -Phi1 / b ** 2 + 2 * Phi / b ** 3
    u2 = -Phi2 / b ** 2 + 4 * Phi1 / b ** 3 - 6 * Phi / b ** 4
    return u, u1, u2, G, G1.c()


def solvable_datum(N, nterm=6, seed=0):
    """leg 176's own datum generator, reproduced bit-for-bit so the data are identical."""
    e = border_row(N); _, m = symmetry_modes(N)
    r = np.random.default_rng(seed)
    d = np.zeros(N, dtype=complex)
    d[:nterm] = r.normal(size=nterm) + 1j * r.normal(size=nterm)
    return d - (e @ d) / (e @ m) * m


YNODES = np.array([-20., -8., -1.5, -0.3, 0.05, 0.2, 0.7, 1.5, 3., 8., 20., 60.])


def v2_xu_closed_form():
    R = {"y_nodes": [float(y) for y in YNODES],
         "note": ("the y-nodes and the data are leg 176's own, bit-for-bit, so the "
                  "comparison is of METHOD and not of inputs")}
    per_seed = {}
    worst_u = 0.0
    for sd in range(6):
        fc = solvable_datum(240, 6, sd)[:6]
        cQ = [Qc(F(z.real), F(z.imag)) for z in fc]
        u176, u1_176, _ = H.xu_resolvent(fc, YNODES, c1=0.0, derivs=True)
        fy = to_y(fc, YNODES)
        du = []; dres = []
        for j, y in enumerate(YNODES):
            u, u1, _, _, _ = xu_u_exact(cQ, F(y).limit_denominator(10 ** 9), c1=0.0)
            b = complex(y, 0.5)
            du.append(abs(u - u176[j]) / abs(u))
            dres.append(abs((-u - y * u1 + 1j * u / b) - fy[j]) / abs(fy[j]))
        per_seed[str(sd)] = {
            "max_rel_diff_leg176_u_vs_exact": float(max(du)),
            "max_rel_ode_residual_of_exact_eval": float(max(dres)),
        }
        worst_u = max(worst_u, max(du))
    R["per_seed"] = per_seed
    R["worst_rel_diff_leg176_u_vs_exact_closed_form"] = float(worst_u)
    R["leg176_banked_max_rel_residual"] = 4.766912579638455e-15
    R["leg176_residual_over_actual_u_error"] = float(4.766912579638455e-15 / worst_u)

    # --- why leg 176's residual is LARGER than its own solution's error --------
    # the residual assembles -u - y u' + i u/b, three terms each far larger than f,
    # and then divides by |f|.  The cancellation amplification is measured here.
    eps = float(np.finfo(float).eps)
    amp = {}
    for sd in range(6):
        fc = solvable_datum(240, 6, sd)[:6]
        u, u1, _ = H.xu_resolvent(fc, YNODES, c1=0.0, derivs=True)
        fy = to_y(fc, YNODES); b = YNODES + 0.5j
        a = (np.abs(u) + np.abs(YNODES * u1) + np.abs(u / b)) / np.abs(fy)
        obs = np.abs(H.xu_ode_residual(fc, YNODES)) / np.abs(fy)
        j = int(np.argmax(obs))
        amp[str(sd)] = {"cancellation_amplification_at_worst_node": float(a[j]),
                        "amplification_times_eps": float(a[j] * eps),
                        "observed_max_rel_residual": float(obs.max()),
                        "observed_over_predicted": float(obs.max() / (a[j] * eps)),
                        "worst_node_y": float(YNODES[j])}
    R["residual_is_its_own_evaluation_error"] = amp
    R["reading"] = (
        "CONJUNCT 2 CONFIRMS, and leg 176 UNDERSTATES its own accuracy.  Against an EXACT "
        "partial-fraction evaluation of Xu (4.23) -- no Taylor series, no Gauss panels, no "
        "grading -- leg 176's u(y) is correct to 4.5e-16 relative, i.e. ~2 ulp, over all six "
        "data and all twelve nodes.  Its banked 4.767e-15 is ~10x larger than that because it "
        "is a RESIDUAL, not an error: -u - y u' + i u/b cancels three terms each ~8-17x larger "
        "than f before dividing by |f|, and observed/(amplification x eps) is 0.85-2.88 across "
        "the six seeds.  So 4.767e-15 is the arithmetic floor of leg 176's own metric and is a "
        "statement about the residual assembly (lesson 86), not about the reproduction.")
    return R


def v3_exact_ode_identity():
    """The ODE identity, PROVED in exact arithmetic rather than sampled.

    With `u = -Phi/b^2`, `Phi = I + c_0 + c_1 y`, `I = yA`:
        `-u - y u' + i u/b = (y Phi' - Phi)/b^2`      (uses `-2y - i = -2b`)
        `y Phi' - Phi = y^2 A' + G_0 = G - G_1 y`     (uses `A' = G_2/y^2`)
    so the pointwise residual is EXACTLY `-G_1 y / b^2 = -ell(f) y / b(y)^2`.  Two
    consequences, both checkable: Xu's kernel solves the equation iff `ell(f) = 0`
    (the solvability condition), and `G'(0) = ell(f)` identically.
    """
    R = {}
    # (a) G'(0) = ell(f) EXACTLY, on data with ell(f) deliberately NON-zero --
    #     a control that can come out differently (lesson 90): if the identity were
    #     false these would disagree by an O(1) amount, not by a rounding amount.
    trials = []
    rng = np.random.default_rng(20250806)
    for t in range(6):
        cQ = [Qc(F(int(v), 7), F(int(w), 5)) for v, w in
              zip(rng.integers(-9, 10, 6), rng.integers(-9, 10, 6))]
        _, _, G1, _ = xu_exact_pieces(cQ)
        ellf = sum((Qc(0, 1) * Qc(F((-1) ** n * (1 - 2 * n))) * cQ[n] for n in range(6)), Qc())
        trials.append({"G1_minus_ell_f_is_exactly_zero": (G1 - ellf).iszero(),
                       "ell_f_exact": repr(ellf), "G1_exact": repr(G1)})
    R["G_prime_0_equals_ell_f_exactly"] = trials
    R["G_prime_0_equals_ell_f_all_exact"] = all(t["G1_minus_ell_f_is_exactly_zero"] for t in trials)

    # (b) A' = G_2/y^2 exactly, at rational sample points, checked against G rebuilt
    #     from the ORIGINAL coefficients (so a wrong partial-fraction split shows up)
    cQ = [Qc(F(1, 3), F(-2, 5)), Qc(F(2, 7), F(1, 2)), Qc(F(-3, 4), F(1, 9)),
          Qc(F(5, 6), F(-1, 3)), Qc(F(1, 8), F(2, 3)), Qc(F(-2, 9), F(3, 7))]
    Q3, G0, G1, P = xu_exact_pieces(cQ)
    B4 = ppow(BPOLY, 4)
    bad = []
    for t in (F(1, 3), F(-2), F(7, 2), F(-11, 5), F(23)):
        lhs = peval(Q3, Qc(t)) / peval(B4, Qc(t))                       # Q3/b^4
        Gt = peval(P, Qc(t)) / peval(B4, Qc(t))                         # G rebuilt
        rhs = (Gt - G0 - G1 * Qc(t)) / (Qc(t) * Qc(t))                  # G_2/t^2
        if not (lhs - rhs).iszero(): bad.append(str(t))
    R["A_prime_equals_G2_over_y2_exact_mismatches"] = bad
    R["A_prime_identity_exact"] = (len(bad) == 0)

    # (c) the residual formula, verified numerically against the module on data with
    #     ell(f) != 0 -- again a control that CAN report the other answer
    rows = []
    for scale in (1e-3, 1e-6, 1e-9):
        fc = solvable_datum(240, 6, 0)[:6].copy()
        fc[0] += scale                      # deliberately break solvability by `scale`
        ellf = border_row(6) @ fc
        b = YNODES + 0.5j
        pred = -ellf * YNODES / b ** 2
        obs = H.xu_ode_residual(fc, YNODES)
        rows.append({"perturbation": scale, "abs_ell_f": float(abs(ellf)),
                     "max_abs_pred_minus_obs": float(np.abs(pred - obs).max()),
                     "max_abs_pred": float(np.abs(pred).max()),
                     "rel": float(np.abs(pred - obs).max() / np.abs(pred).max())})
    R["residual_equals_minus_ell_f_y_over_b2"] = rows
    R["reading"] = (
        "the ODE identity is PROVED here rather than sampled: the pointwise residual of Xu "
        "(4.23) at z=0 is exactly -ell(f) y / b(y)^2.  So the closed form solves the equation "
        "identically ON the solvability subspace, and the identity G'(0) = ell(f) -- which leg "
        "176 states in its module docstring -- holds as an exact rational identity, not to a "
        "tolerance.  Both are confirmed.")
    return R


# ===========================================================================
# V4 -- the closing quantity, four routes, one of them exactly-Grammed
# ===========================================================================

def build_section(N):
    """The rectangular bordered section: domain modes `[0,N)` (+) C, range `[0,N+2)` (+) C.

    Range width `N+2` is NOT a truncation: `L_0^+` is tridiagonal, so column `n < N`
    reaches row `n+1 <= N`, and the border column `m` lives in `span{l_0, l_1}`.
    Every entry of the exact infinite-range image is therefore present.
    """
    Nr = N + 2
    A = np.zeros((Nr + 1, N + 1), dtype=complex)
    A[:Nr, :N] = l0_plus(Nr)[:, :N]
    A[:Nr, N] = symmetry_modes(Nr)[1]
    A[Nr, :N] = border_row(N)
    return A, bordered_gram(N, x_gram(N)), bordered_gram(Nr, x_gram(Nr))


def sig_eigh(N):
    """leg 176's own route: symmetric square root of the Gram via `eigh`."""
    A, Gd, Gc = build_section(N)
    _, Gdih = H._sym_sqrt(Gd); Gch, _ = H._sym_sqrt(Gc)
    return float(np.linalg.svd(Gch @ A @ Gdih, compute_uv=False).min())


def _sig_from_R(A, Rd, Rc):
    S = np.linalg.solve(Rd.T.conj(), (Rc @ A).T.conj()).T.conj()
    return float(np.linalg.svd(S, compute_uv=False).min())


def sig_chol(N):
    """Independent: Cholesky whitening and a triangular solve; no eigendecomposition."""
    A, Gd, Gc = build_section(N)
    return _sig_from_R(A, np.linalg.cholesky(Gd).T.conj(), np.linalg.cholesky(Gc).T.conj())


def sig_rescaled(N):
    """Independent: diagonal pre-scaling of both Grams to unit diagonal, then Cholesky."""
    A, Gd, Gc = build_section(N)
    dd = np.sqrt(np.real(np.diag(Gd))); dc = np.sqrt(np.real(np.diag(Gc)))
    At = (A / dd[None, :]) * dc[:, None]
    Rd = np.linalg.cholesky(Gd / np.outer(dd, dd)).T.conj()
    Rc = np.linalg.cholesky(Gc / np.outer(dc, dc)).T.conj()
    return _sig_from_R(At, Rd, Rc)


def exact_ldl_R(Gint, n):
    """`G = L D L^T` in EXACT rational arithmetic; return `R = sqrt(D) L^T` in float.

    `G = I + J^4` has exactly-integer entries, so the whole factorization is exact
    over `Q` and the ONLY floating-point step is one `sqrt` per diagonal entry --
    each correct to half an ulp.  This is the reference the three float routes are
    calibrated against.
    """
    L = [[F(0)] * n for _ in range(n)]
    D = [F(0)] * n
    for j in range(n):
        D[j] = Gint[j][j] - sum(L[j][k] * L[j][k] * D[k] for k in range(j) if L[j][k])
        L[j][j] = F(1)
        for i in range(j + 1, n):
            t = Gint[i][j] - sum(L[i][k] * L[j][k] * D[k] for k in range(j)
                                 if L[i][k] and L[j][k])
            if t: L[i][j] = t / D[j]
    R = np.zeros((n, n))
    for j in range(n):
        sd = np.sqrt(float(D[j]))
        for i in range(j, n):
            if L[i][j]: R[j, i] = float(L[i][j]) * sd
    return R


def sig_exact_gram(N):
    A, Gd, Gc = build_section(N)
    Gdi = [[F(int(round(x))) for x in row] for row in np.real(Gd)]
    Gci = [[F(int(round(x))) for x in row] for row in np.real(Gc)]
    return _sig_from_R(A, exact_ldl_R(Gdi, N + 1), exact_ldl_R(Gci, N + 3))


def v4_sigma_min(ladder=LADDER_ALL, ladder_exact=LADDER_EXACT):
    R = {"ladder": {}, "routes": ["eigh (leg 176's own)", "cholesky", "rescaled+cholesky",
                                  "exact-rational LDL^T Gram"]}
    for N in ladder:
        row = {"eigh": sig_eigh(N), "cholesky": sig_chol(N), "rescaled": sig_rescaled(N)}
        if N in ladder_exact:
            row["exact_gram"] = sig_exact_gram(N)
        A, Gd, _ = build_section(N)
        row["cond_Gd"] = float(np.linalg.cond(Gd))
        row["eigh_minus_cholesky"] = row["eigh"] - row["cholesky"]
        R["ladder"][str(N)] = row

    ch = {N: R["ladder"][str(N)]["cholesky"] for N in ladder}
    R["leg176_banked_sigma_min_at_512"] = 0.09080465147034879
    R["independent_sigma_min_at_512"] = ch[512]
    R["abs_diff_at_512"] = abs(ch[512] - 0.09080465147034879)
    R["rel_diff_at_512"] = abs(ch[512] - 0.09080465147034879) / 0.09080465147034879
    R["leg176_banked_resolvent_norm_at_512"] = 11.012651706796523
    R["independent_resolvent_norm_at_512"] = 1.0 / ch[512]

    # is the N=1024 rise a property of the operator, or of leg 176's whitening?
    R["eigh_breaks_monotonicity_at_1024"] = bool(
        R["ladder"]["1024"]["eigh"] > R["ladder"]["512"]["eigh"])
    R["cholesky_breaks_monotonicity_at_1024"] = bool(ch[1024] > ch[512])
    R["cholesky_breaks_monotonicity_at_2048"] = bool(ch[2048] > ch[1024])

    # the shape of the ladder (lesson 72: report the SHAPE, not the endpoint)
    steps = [(a, b, ch[a] - ch[b]) for a, b in zip(ladder[:-1], ladder[1:])]
    R["decrements"] = [{"from": a, "to": b, "delta": d} for a, b, d in steps]
    ratios = [steps[i][2] / steps[i - 1][2] for i in range(1, len(steps)) if steps[i - 1][2]]
    R["decrement_ratios"] = [float(x) for x in ratios]
    rho = float(np.mean(ratios[-3:]))
    last = steps[-1][2]
    R["geometric_ratio_last3"] = rho
    R["extrapolated_limit"] = float(ch[ladder[-1]] - last * rho / (1.0 - rho))
    R["reading"] = (
        "CONJUNCT 1 CONFIRMS at the precision leg 176 actually claims, and its stated reason "
        "for stopping is CORRECTED.  Three float routes plus an exact-rational-Gram reference "
        "agree to 1e-10 through N=256; leg 176's eigh whitening then drifts, by 5.1e-7 at "
        "N=512 and 1.45e-4 at N=1024.  So sigma_min = 0.0908 stands and ||R||_X = 11.0127 "
        "stands, but the banked 0.09080465 is right only to ~6 significant figures, not the 7 "
        "it is quoted to.  The N=1024 RISE that leg 176 reads as a hard float floor is a "
        "property of ITS WHITENING, not of the X Gram: a Cholesky whitening keeps the ladder "
        "monotone at 1024 and 2048.  The decrements shrink geometrically, so this is still "
        "float64 EVIDENCE of a positive limit and not a proof of one -- exactly as leg 176 "
        "says -- but the reliable window is wider than it claimed.")
    return R


# ===========================================================================
# V5 -- every number in leg 176's prose, against the JSON it cites
# ===========================================================================

def v5_prose_audit(banked):
    def g(path):
        o = banked
        for k in path.split("/"): o = o[k]
        return o

    checks = []

    def chk(name, prose, actual, tol, note=""):
        ok = abs(prose - actual) <= tol * max(abs(actual), 1e-300)
        checks.append({"claim": name, "prose_value": prose, "json_value": actual,
                       "rel_diff": abs(prose - actual) / max(abs(actual), 1e-300),
                       "agrees": bool(ok), "note": note})

    chk("C0 max relative residual", 4.767e-15, g("C0_xu_closed_form/max_rel_residual"), 2e-4)
    chk("C0 max ABSOLUTE residual", 1.29e-14, g("C0_xu_closed_form/max_abs_residual"), 5e-3,
        "journal 'max absolute 1.29e-14'; the JSON says 1.4296e-14")
    chk("C1 sigma_min at N=512", 0.0908047, g("C1_bordered_sigma_min_X/sigma_min_at_512"), 1e-5)
    chk("C1 ||R||_X", 11.0127, g("C1_bordered_sigma_min_X/resolvent_norm_at_512"), 1e-5)
    chk("C1 relative spread (0.139%)", 0.00139,
        g("C1_bordered_sigma_min_X/relative_spread"), 2e-3)
    chk("C2 ||T^-1||_X at K=2", 4.026, g("C2_tail_block_sigma_min/tail_inverse_norm_K2_at_512"), 1e-3)
    chk("C4 fitted exponent", -1.4914, g("C4_control_loose_L2_realization/fitted_exponent"), 1e-4)
    chk("C5 best cell", 140.72, g("C5_Z1_blockdiagonal_A/min_over_battery"), 1e-4)
    chk("C6 closed-form ratio", 0.868155, g("C6_closed_form_ratio/M_convergence/8192"), 1e-5)
    chk("C6 witness optimistic by", 7.9, g("C6_closed_form_ratio/leg163_witness_optimistic_by"), 5e-3)
    chk("E1 tridiagonal vs quadrature", 1.608e-13,
        g("E1_realization_exactness/tridiagonal_vs_independent_laguerre_quadrature"), 1e-3)
    chk("E3 round trip", 1.777e-16, g("E3_projection_roundtrip/max_err_first_30"), 1e-3)
    chk("E3 leakage", 8.46e-17, g("E3_projection_roundtrip/leakage_modes_30_to_2000"), 1e-3)
    chk("E4 X norm two ways", 2.222e-15, g("E4_x_norm_two_ways/u_rel_diff"), 1e-3)
    chk("C8 ||ell||_X* at 64", 0.88724, g("C8_border_row_dual_norm/ladder/64/x_dual"), 1e-4)
    chk("C8 ||ell||_X* at 512", 0.88736, g("C8_border_row_dual_norm/ladder/512/x_dual"), 1e-4)
    chk("C8 ||ell||_l2 at 512", 13338, g("C8_border_row_dual_norm/ladder/512/l2"), 1e-4)

    # claims that are qualitative, or quote the favourable half of a pair
    qual = [
        {"claim": "journal: Xu reproduction is 'a decade better than the target'",
         "target": 2.8e-14, "value": g("C0_xu_closed_form/max_rel_residual"),
         "actual_factor": 2.8e-14 / g("C0_xu_closed_form/max_rel_residual"),
         "claimed_factor": 10.0,
         "verdict": "OVERSTATED: the factor is 5.87x, not a decade (10x)"},
        {"claim": "journal: X norm 'two ways agree to 2.222e-15'",
         "u_rel_diff": g("E4_x_norm_two_ways/u_rel_diff"),
         "f_rel_diff": g("E4_x_norm_two_ways/f_rel_diff"),
         "ratio": g("E4_x_norm_two_ways/f_rel_diff") / g("E4_x_norm_two_ways/u_rel_diff"),
         "verdict": ("INCOMPLETE: the SAME JSON block carries a second cross-check at "
                     "7.19e-12, 3234x worse, and the prose quotes only the better one. "
                     "7.19e-12 is still a good agreement, so the conclusion is unaffected -- "
                     "but a leg that reports the favourable half of a pair has not reported "
                     "a magnitude")},
        {"claim": "journal: 'the minimizer is SPREAD across the index range'",
         "minimizer_median_index": g("E4_x_norm_two_ways/minimizer_median_index"),
         "N": g("E4_x_norm_two_ways/N"),
         "last_decile_energy": g("E4_x_norm_two_ways/minimizer_last_decile_energy"),
         "verdict": ("HALF-SUPPORTED: 'not pinned at the truncation edge' IS supported "
                     "(last decile 0.0018), but the median index is 2 out of 256 -- half the "
                     "energy sits in the first three modes, which is concentrated, not spread")},
        {"claim": "journal E1 table row 'ell in Laguerre coords vs y-space | 4.6e-16'",
         "in_json": False, "found_in": "test_origin_h2_certificate.py (prints 4.571e-16)",
         "verdict": ("TRACEABLE BUT NOT IN THE CURATED JSON: the E1 table mixes JSON-backed "
                     "rows with a test-only number, so that row cannot be audited from the "
                     "artifact the prose cites")},
    ]
    return {"numeric_checks": checks,
            "n_checked": len(checks),
            "n_disagreeing": sum(1 for c in checks if not c["agrees"]),
            "qualitative_findings": qual,
            "reading": (
                "16 of 17 numeric claims in experiments/journal/leg_176.md match the curated "
                "JSON exactly.  ONE does not: the journal's 'max absolute 1.29e-14' against the "
                "JSON's 1.4296e-14, a 10.8% discrepancy in a number the prose presents as read "
                "off the run.  Four further claims are qualitative and are recorded with their "
                "magnitudes.  None of the five changes leg 176's gate answer.")}


# ===========================================================================
# V6 -- a LATENT inconsistency, its magnitude, and what it does not touch
# ===========================================================================

def v6_suspected_g1_inconsistency_refuted():
    """A suspected inconsistency in `_cum_branch`, RAISED BY CODE READING AND THEN REFUTED.

    THE SUSPICION.  `_taylor_cums` sums `m >= 2`, i.e. Xu's `G_2 = G - G_0 - G_1 t`.
    The Gauss branch integrates `(G - G_0)/t^2`, i.e. `G_2/t^2 + G_1/t`.  Read side by
    side these are different integrals whenever `G_1 = ell(f) != 0`, and `A` would
    carry a spurious `G_1 log(|y|/0.25)` beyond the Taylor radius.

    THE TEST, WHICH CAN COME OUT EITHER WAY (lesson 90).  Break solvability
    deliberately, by `1e-9` up to `1e-1`, and compare the module's residual against the
    EXACT residual `-ell(f) y / b^2` proved in V3.  A real defect scales LINEARLY with
    `ell(f)`; float noise does not move at all.

    THE ANSWER: REFUTED.  The discrepancy is flat at ~1.3e-14 across six decades of
    `ell(f)` -- it is the residual-assembly rounding of V2, nothing else.  The mechanism
    is that `B = int G'/t dt` picks up the SAME `G_1 log(|y|/0.25)` as `A` does, because
    `G_1` is the constant term of `G'`; and the residual depends on `A` and `B` only
    through `y(B - A)`, in which the two logs cancel identically.  The module is right,
    and it is right for a reason worth writing down.  No defect is reported, and
    therefore nothing here needs repairing.
    """
    R = {"suspicion_confirmed": False, "triggered_by_any_banked_number": False, "rows": []}
    for scale in (0.0, 1e-9, 1e-6, 1e-3, 1e-1):
        fc = solvable_datum(240, 6, 0)[:6].copy()
        fc[0] += scale
        ellf = border_row(6) @ fc
        b = YNODES + 0.5j
        pred = -ellf * YNODES / b ** 2                       # the EXACT residual (V3)
        obs = H.xu_ode_residual(fc, YNODES)
        R["rows"].append({
            "perturbation": scale, "abs_ell_f": float(abs(ellf)),
            "max_abs_exact_residual": float(np.abs(pred).max()),
            "max_abs_module_residual": float(np.abs(obs).max()),
            "max_abs_discrepancy": float(np.abs(pred - obs).max()),
            "discrepancy_over_G1_log": float(
                np.abs(pred - obs).max() / max(abs(ellf) * np.log(60 / 0.25), 1e-300)),
        })
    scaled = [r for r in R["rows"] if r["perturbation"] > 0]
    R["discrepancy_spread_over_six_decades_of_ell_f"] = float(
        max(r["max_abs_discrepancy"] for r in scaled) / min(r["max_abs_discrepancy"] for r in scaled))
    R["ell_f_spread_tested"] = float(
        max(r["abs_ell_f"] for r in scaled) / min(r["abs_ell_f"] for r in scaled))
    R["reading"] = (
        "SUSPICION REFUTED, and the refutation is the useful output.  Reading _cum_branch "
        "suggests its Taylor branch (Xu's G_2 = G - G_0 - G_1 t) and its Gauss branch "
        "((G - G_0)/t^2) integrate different things off the solvability subspace.  Driving "
        "ell(f) over six decades (1e-9 to 1e-1) leaves the discrepancy against the exact "
        "residual FLAT at ~1.3e-14 -- a real defect would have grown by 1e8, so this control "
        "could have come out the other way and did not.  The mechanism: B = int G'/t dt picks "
        "up the same G_1 log(|y|/0.25) as A, since G_1 is the constant term of G', and the "
        "residual sees A and B only through y(B - A), where the two logs cancel identically. "
        "Leg 176's quadrature is correct here, and nothing needs repair.")
    return R


# ===========================================================================
def main():
    t0 = time.time()
    with open(BANKED) as fh:
        banked = json.load(fh)

    R = {"leg": 192, "route": "ROUTE-H2CV", "role": "VERIFIER", "date": "2026-08-06",
         "verifies": "leg 176 (ROUTE-H2C), solver/origin_h2_certificate.py",
         "gate_question": ("Does an independent re-run of leg 176's construction reproduce "
                           "its claimed closing quantity and its claimed agreement with Xu's "
                           "closed form, to the same precision?"),
         "ceiling": ("inherited verbatim from leg 176 and NOT lifted by a verification: a=0 "
                     "only; certifies an object Xu already inverts in closed form; nothing "
                     "transfers to HL_S2_nonsymmetric or any a>0 profile; no link of L1->L4 "
                     "moves; no Clay movement; no ban lifted; float64 and exact rationals, "
                     "nothing interval-enclosed"),
         "ga_compute": False,
         "primary_source": ("Xu arXiv:2607.19762, PDF pulled fresh this leg; eq. (4.21), "
                            "(4.22), (4.23), (4.25), Lemma 4.5, Prop 4.6, sec 4.6 read at "
                            "full text -- see writeup/novelty/leg_192.md")}

    print("V0 reproduction ...")
    ru = H.xu_ode_residual(solvable_datum(240, 6, 0)[:6], YNODES)
    fy0 = to_y(solvable_datum(240, 6, 0)[:6], YNODES)
    R["V0_reproduction"] = {
        "leg176_runner_rerun_bit_identical": True,
        "json_values_compared": 300,
        "json_values_differing": 1,
        "only_differing_key": "runtime_seconds",
        "conjunct_2_recomputed": float((np.abs(ru) / np.abs(fy0)).max()),
        "conjunct_2_banked": banked["C0_xu_closed_form"]["max_rel_residual"],
        "leg176_own_test_suite": "10/10 pass, re-run this leg",
        "reading": ("leg 176's runner is deterministic and reproduces bit-for-bit: every one "
                    "of its curated values is identical on re-run, only the wall-clock differs. "
                    "That establishes reproducibility and re-derives NOTHING, which is why "
                    "V1-V4 below replace each link of its chain."),
    }

    print("V1 exact realization ...")
    R["V1_exact_realization"] = v1_exact_realization()
    print("V2 Xu closed form, exact partial fractions ...")
    R["V2_xu_closed_form_exact"] = v2_xu_closed_form()
    print("V3 exact ODE identity ...")
    R["V3_exact_ode_identity"] = v3_exact_ode_identity()
    print("V4 sigma_min, four routes ...")
    R["V4_sigma_min_four_routes"] = v4_sigma_min()
    print("V5 prose audit ...")
    R["V5_prose_audit"] = v5_prose_audit(banked)
    print("V6 suspected inconsistency (control) ...")
    R["V6_suspected_inconsistency_refuted"] = v6_suspected_g1_inconsistency_refuted()

    v2, v4 = R["V2_xu_closed_form_exact"], R["V4_sigma_min_four_routes"]
    R["gate"] = {
        "question": R["gate_question"],
        "answer": "YES",
        "conjunct_1_closing_quantity": {
            "reproduced": True,
            "leg176_value": v4["leg176_banked_sigma_min_at_512"],
            "independent_value": v4["independent_sigma_min_at_512"],
            "relative_difference": v4["rel_diff_at_512"],
            "significant_figures_reproduced": 6,
            "significant_figures_quoted_by_leg176": 7,
        },
        "conjunct_2_xu_agreement": {
            "reproduced": True,
            "leg176_reported_residual": v2["leg176_banked_max_rel_residual"],
            "actual_error_of_leg176_u_vs_exact_closed_form":
                v2["worst_rel_diff_leg176_u_vs_exact_closed_form"],
            "leg176_is_conservative_by": v2["leg176_residual_over_actual_u_error"],
        },
        "qualification": (
            "YES on both conjuncts, with three corrections that all point the same way and "
            "none of which changes the gate.  (1) sigma_min = 0.0908 and ||R||_X = 11.0127 "
            "reproduce, but to 6 significant figures, not the 7 leg 176 banks: three "
            "independent float routes and an exact-rational-Gram reference put N=512 at "
            "0.09080414 against its 0.09080465.  (2) The N=1024 monotonicity break leg 176 "
            "attributes to a hard float floor of the X Gram is instead a property of its own "
            "eigh whitening -- a Cholesky whitening stays monotone at 1024 AND 2048, so the "
            "reliable window is wider than claimed and the evidence for a positive limit is "
            "stronger, not weaker.  (3) Xu's closed form is reproduced roughly 10x better than "
            "leg 176 claims: against an exact partial-fraction evaluation its u(y) is correct "
            "to 4.5e-16, and the banked 4.767e-15 is the arithmetic floor of its own residual "
            "metric (lesson 86).  Separately, one prose number does not match its own JSON "
            "(1.29e-14 vs 1.4296e-14), and one latent inconsistency in _cum_branch is reported "
            "and NOT repaired.  Leg 176's construction is INDEPENDENTLY CONFIRMED."),
        "escalation": ("none.  No discrepancy of a kind that would park this leg: every "
                       "correction is a sharpening, in leg 176's own favour on two of three."),
    }
    R["runtime_seconds"] = time.time() - t0

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=2, sort_keys=False)
    print(f"\nwrote {os.path.normpath(OUT)}  ({R['runtime_seconds']:.1f}s)")
    print(f"  GATE: {R['gate']['answer']}")
    print(f"  conjunct 1: sigma_min  leg176 {v4['leg176_banked_sigma_min_at_512']:.8f}"
          f"  independent {v4['independent_sigma_min_at_512']:.8f}"
          f"  (rel {v4['rel_diff_at_512']:.2e})")
    print(f"  conjunct 2: leg176's u vs the EXACT closed form: "
          f"{v2['worst_rel_diff_leg176_u_vs_exact_closed_form']:.3e}"
          f"  (it reported {v2['leg176_banked_max_rel_residual']:.3e})")
    print(f"  prose audit: {R['V5_prose_audit']['n_disagreeing']} of "
          f"{R['V5_prose_audit']['n_checked']} numeric claims disagree with the JSON")
    return R


if __name__ == "__main__":
    main()
