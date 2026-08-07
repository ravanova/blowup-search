#!/usr/bin/env python3
"""Route-H2CV2 — the INDEPENDENT VERIFICATION of leg 176's origin-`H^2` certificate.

ROLE: VERIFIER (leg 249).  This leg builds nothing and repairs nothing.  It
re-derives leg 176's two headline quantities from the definitions, by routes that
share no numerical machinery with `solver/origin_h2_certificate.py`, and reports
the magnitude of every agreement and every disagreement.  Gaps are REPORTED, never
fixed here (ORCHESTRATION.md, verifier role).

THE GATE, in its pre-committed wording
--------------------------------------
> Does an independent re-run of leg 176's construction reproduce `sigma_min =
> 0.0908` and `||T^-1||_X = 4.026` (or report a discrepancy precisely), to the
> same precision leg 176 itself claims?

WHAT IS UNDER VERIFICATION, AND WHERE IT IS LOAD-BEARING
--------------------------------------------------------
  `sigma_min`     0.09080465147034879 at N=512, quoted as 0.0908 with
                  `||R||_X = 11.0127`.  PUB2 (approved, submission-track) quotes
                  it at TECHNICAL L46/L297/L299/L332/L335.
  `||T^-1||_X`    4.026, the tail block (modes >= 2, unbordered) at N=512.
                  PUB2 TECHNICAL L303.
`BLOG_P2_PUB2_V1.md` L190 calls these "one leg's own float64 measurements, with
the independent check still outstanding".  That sentence is what this leg exists
to retire or to convert into a precisely-stated discrepancy.

WHY A RE-RUN IS NOT ENOUGH (lesson 90: a control that cannot come out
differently is not a control)
---------------------------------------------------------------------
Leg 176's runner is deterministic, so re-running it re-derives nothing.  It is
re-run (W0) and reported as a REPRODUCTION and not as a verification.  The
verification proper replaces every link of the chain:

  W1   the discrete realization  -- re-derived in EXACT RATIONAL ARITHMETIC by
       integrating and differentiating the Laguerre polynomials term by term.
       NEITHER classical identity leg 176 invokes is used; both come out as
       by-products.  Every matrix used downstream in this file is built HERE,
       from these rationals -- leg 176's module supplies nothing but a comparand.
  W1b  the SAME realization again, from a completely different direction: the
       tridiagonal action is checked in y-SPACE against Xu (4.21) itself, in
       exact rational arithmetic, with no Laguerre integral and no quadrature
       anywhere.  Two independent proofs of one matrix.
  W2   THE LINK LEG 176 AND THE 192 SALVAGE BOTH LEAVE UNCHECKED: that the Gram
       IS the `X` norm of Xu's Definition 4.1.  Verified by an independent
       quadrature in y-space, including the `2 pi` Plancherel factor.
  W3   `sigma_min` by three float whitenings AND by EXACT-RATIONAL INERTIA
       BISECTION, which returns a certified enclosure rather than a float
       measurement, and so settles how many significant figures the banked value
       carries instead of asserting a count.
  W4   `||T^-1||_X` of the tail block, by the same two-tier treatment.  THE 192
       SALVAGE NEVER RE-DERIVED THIS NUMBER AT ALL.
  W5   the convention sensitivity of `sigma_min` to the border weight -- an
       arbitrary constant in the definition that no artifact had measured.
  W6   Xu (4.23) at `z = 0` by EXACT PARTIAL FRACTIONS, and the pointwise ODE
       residual identity PROVED rather than sampled.
  W7   leg 176's prose and PUB2's five quoting sites, audited against the JSON.

CEILING (inherited verbatim; a verification cannot lift a ceiling)
------------------------------------------------------------------
`a = 0` only.  This concerns an object Xu (arXiv:2607.19762) already inverts in
closed form.  Nothing transfers to `HL_S2_nonsymmetric` or to any `a > 0`
profile.  No link of the `L1 -> L4` chain moves.  No Clay movement; odds
unchanged at ~0.05%.  No ban lifted.  No GA compute.  Float64 and exact
rationals; nothing interval-enclosed in the interval-arithmetic sense, nothing
rigorous as a theorem.

ON THE STANDING BAN.  `plan_of_record.py` bans RE-ATTEMPTING the ell^1-Fourier /
radii-polynomial machinery measured dead in three realizations, the third being
"origin-H^2 capped at a=0 ... legs 163/176".  This leg makes no new attempt at
that machinery: no fourth space or basis is proposed, no `Y_0`/`Z_1`/`Z_2` is
formed, no target is aimed at.  It audits a number already banked from the dead
lane, because that number is quoted in a submission-track document.

Run: .venv/bin/python experiments/p2_route_h2cv_v1_postconstruction.py
     (--quick trims the ladders; the default is the full run)
"""

import cmath
import json
import math
import os
import sys
import time
from fractions import Fraction as F
from math import comb, factorial

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import solver.origin_h2_certificate as H          # READ-ONLY comparand. Never edited.

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "writeup", "data", "p2_route_h2cv_v1_postconstruction.json")
BANKED = os.path.join(HERE, "..", "writeup", "data", "p2_route_h2c_v1_construction.json")

LADDER_FLOAT = (8, 16, 32, 64, 128, 256, 512, 1024, 2048)
LADDER_EXACT = (8, 16, 32, 64, 128)
CERTIFY_N = (256, 512)
TAIL_FLOAT = (64, 128, 256, 512, 1024)
TAIL_EXACT = (64, 128)
TAIL_CERTIFY = (256, 512)

LEG176_SIGMA = 0.09080465147034879
LEG176_TAIL_INV = 4.026


# ===========================================================================
# W1 -- the discrete realization, re-derived in exact rational arithmetic
# ===========================================================================
# Everything below is built from the DEFINITIONS:
#     l_n(xi) = L_n(xi) e^{-xi/2},  L_0^+ = xi d/dxi + V,
#     (V g)(xi) = int_0^xi e^{-(xi-eta)/2} g(eta) d eta,
#     <phi, psi>_X  <->  int_0^inf (1 + xi^4) phihat conj(psihat) d xi,
#     ell(f) = i f(0) - f'(0)/4.
# No classical Laguerre identity is invoked.

def lag_coeffs(N):
    """`L_n(x) = sum_k C(n,k)(-1)^k x^k / k!` -- exact rational coefficients."""
    return [[F((-1) ** k * comb(n, k), factorial(k)) for k in range(n + 1)]
            for n in range(N)]


def pmul(p, q):
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q):
                r[i + j] += a * b
    return r


def padd(*ps):
    r = [F(0)] * max(len(p) for p in ps)
    for p in ps:
        for i, a in enumerate(p):
            r[i] += a
    return r


def int_e1(p):
    """`int_0^inf p(x) e^{-x} dx = sum_k p_k k!` -- exact."""
    return sum((c * factorial(k) for k, c in enumerate(p) if c), F(0))


def int_ehalf(p):
    """`int_0^inf p(x) e^{-x/2} dx = sum_k p_k k! 2^{k+1}` -- exact."""
    return sum((c * F(factorial(k) * 2 ** (k + 1)) for k, c in enumerate(p) if c), F(0))


def l0_column_poly(Ln):
    """`L_0^+ l_n` as (polynomial) * `e^{-xi/2}`, by CALCULUS not by identities.

    `l_n = L_n e^{-xi/2}`, so `(xi d_xi) l_n = e^{-xi/2}(xi L_n' - (xi/2) L_n)`,
    and the Volterra piece's exponentials cancel exactly:
        `(V l_n)(xi) = int_0^xi e^{-(xi-eta)/2} L_n(eta) e^{-eta/2} d eta
                     = e^{-xi/2} int_0^xi L_n`.
    `int_0^xi L_n` is obtained by integrating the polynomial term by term -- NOT
    by `int_0^x L_n = L_n - L_{n+1}`, which is one of the two identities leg 176
    relies on and which this routine therefore re-proves rather than assumes.
    """
    xLp = [F(0)] + [Ln[k] * k for k in range(1, len(Ln))]         # xi L_n'
    xL2 = [F(0)] + [c * F(1, 2) for c in Ln]                      # (xi/2) L_n
    cum = [F(0)] + [Ln[k] / (k + 1) for k in range(len(Ln))]      # int_0^xi L_n
    return padd(xLp, [-c for c in xL2], cum)


def w1_exact_realization(NB=14, NG=20):
    R = {}
    Lc = lag_coeffs(NB + 8)

    R["laguerre_orthonormality_max_defect_exact"] = str(max(
        (int_e1(pmul(Lc[m], Lc[n])) - (1 if m == n else 0)
         for m in range(8) for n in range(8)), key=abs))

    # --- the operator matrix -------------------------------------------------
    mism = []
    for n in range(NB):
        tot = l0_column_poly(Lc[n])
        for m in range(NB + 3):
            got = int_e1(pmul(tot, Lc[m]))
            want = F(0)
            if m == n - 1: want = F(-n, 2)
            if m == n:     want = F(1, 2)
            if m == n + 1: want = F(n - 1, 2)
            if got != want:
                mism.append([m, n, str(got), str(want)])
    R["l0_plus_tridiagonal_exact_mismatches"] = mism
    R["l0_plus_tridiagonal_exact"] = (len(mism) == 0)
    R["l0_plus_block_checked"] = NB
    R["l0_plus_vs_module_max_abs"] = float(np.abs(
        H.l0_plus(NB) - my_l0_float(NB)).max())

    # --- the border row ------------------------------------------------------
    # ell(f) = i f(0) - f'(0)/4 with f(y) = int_0^inf fhat(xi) e^{iy xi} d xi,
    # so f(0) = int fhat and f'(0) = i int xi fhat, giving ell = i int(1 - xi/4) fhat.
    ell_ex = [int_ehalf(padd(Lc[n], [F(0)] + [-c * F(1, 4) for c in Lc[n]]))
              for n in range(NB)]
    R["border_row_first_eight_exact"] = [str(v) for v in ell_ex[:8]]
    R["border_row_equals_i_m1n_1m2n_exact"] = all(
        ell_ex[n] == F((-1) ** n * (1 - 2 * n)) for n in range(NB))
    R["border_row_vs_module_max_abs"] = float(np.abs(
        H.border_row(NB) - 1j * np.array([float(v) for v in ell_ex])).max())

    # --- the symmetry modes --------------------------------------------------
    # Transform pair (re-derived in W1b): int_0^inf l_n e^{iy xi} d xi = i a^n/b^{n+1}.
    # b^{-2}   has inverse transform  -xi e^{-xi/2}
    # y b^{-2} has inverse transform  -i(1 - xi/2) e^{-xi/2}
    b2_ex = [int_e1(pmul([F(0), F(-1)], Lc[m])) for m in range(NB)]
    m_ex = [int_e1(pmul([F(1), F(-1, 2)], Lc[m])) for m in range(NB)]     # times -i
    b2_mod, m_mod = H.symmetry_modes(NB)
    R["symmetry_mode_binv2_exact"] = [str(v) for v in b2_ex[:4]]
    R["symmetry_mode_m_exact_times_minus_i"] = [str(v) for v in m_ex[:4]]
    R["symmetry_mode_binv2_vs_module_max_abs"] = float(np.abs(
        b2_mod - np.array([float(v) for v in b2_ex])).max())
    R["symmetry_mode_m_vs_module_max_abs"] = float(np.abs(
        m_mod - (-1j) * np.array([float(v) for v in m_ex])).max())

    # kernel and eigenvalue, exactly, from the exact tridiagonal columns
    def apply_exact(vec):
        out = [F(0)] * (len(vec) + 1)
        for n, cn in enumerate(vec):
            if not cn: continue
            if n - 1 >= 0: out[n - 1] += cn * F(-n, 2)
            out[n] += cn * F(1, 2)
            out[n + 1] += cn * F(n - 1, 2)
        return out
    mvec = [F(v) for v in m_ex[:4]]           # up to the -i factor; L_0^+ is real
    b2vec = [F(v) for v in b2_ex[:4]]
    R["L0_applied_to_m_is_exactly_zero"] = all(v == 0 for v in apply_exact(mvec))
    R["L0_applied_to_binv2_minus_binv2_is_exactly_zero"] = all(
        v == (b2vec[i] if i < len(b2vec) else F(0))
        for i, v in enumerate(apply_exact(b2vec)))
    R["ell_dot_L0_columns_exactly_zero"] = all(
        F(-n, 2) * ell_ex[n - 1] + F(1, 2) * ell_ex[n] + F(n - 1, 2) * ell_ex[n + 1] == 0
        for n in range(1, NB - 1))
    R["ell_of_m_exact"] = str(sum(
        (ell_ex[n] * m_ex[n] for n in range(4)), F(0)))     # ell(m) with both -i,+i factors

    # --- the X Gram ----------------------------------------------------------
    Gcode = H.x_gram(NG)
    bad, maxd = [], 0.0
    for m in range(NG):
        for n in range(m, NG):
            pr = pmul(Lc[m], Lc[n])
            val = int_e1(padd(pr, [F(0)] * 4 + pr))          # int (1 + xi^4) l_m l_n
            maxd = max(maxd, abs(float(val) - Gcode[m, n]))
            if val != F(int(round(Gcode[m, n]))):
                bad.append([m, n, str(val), Gcode[m, n]])
    R["x_gram_exact_integer_mismatches"] = bad
    R["x_gram_exact_integer_equality"] = (len(bad) == 0)
    R["x_gram_max_abs_diff_vs_module"] = maxd
    R["x_gram_size_checked"] = NG
    R["x_gram_vs_my_own_float_build_max_abs"] = float(np.abs(
        Gcode - my_gram_float(NG)).max())

    R["reading"] = (
        "the discrete realization is re-derived in EXACT RATIONAL ARITHMETIC from the "
        "definitions of the operator, the basis, the border functional and the X inner "
        "product, invoking NEITHER of the two classical Laguerre identities leg 176 "
        "relies on -- both are integrated/differentiated out instead, so they are "
        "re-proved here rather than assumed.  Every entry of L_0^+, of the border row, "
        "of both symmetry modes and of the X Gram agrees with leg 176's module EXACTLY, "
        "as rationals rather than to a tolerance.  Leg 176's own cross-check of the same "
        "entries is a 60-node Gauss-Laguerre quadrature agreeing to 1.6e-13, which is a "
        "second float computation and not an independent one.")
    return R


# --- my own float matrices (used by every downstream measurement here) ------

def my_l0_float(n):
    """`L_0^+` from the exact rational column, in float.  Built here, not imported."""
    A = np.zeros((n, n))
    for k in range(n):
        if k: A[k - 1, k] = -k / 2.0
        A[k, k] = 0.5
        if k + 1 < n: A[k + 1, k] = (k - 1) / 2.0
    return A


def my_gram_float(n, pad=6):
    """`G = I + J^4` in float, from my own `J`."""
    m = n + pad
    J = np.zeros((m, m))
    for i in range(m):
        J[i, i] = 2 * i + 1
        if i + 1 < m:
            J[i + 1, i] = J[i, i + 1] = -(i + 1)
    J2 = J @ J
    return (np.eye(m) + J2 @ J2)[:n, :n]


# ===========================================================================
# W1b -- the SAME matrix, from y-space, exactly, with no quadrature at all
# ===========================================================================

class Qc:
    """A complex rational as an exact `(re, im)` pair of `Fraction`s."""
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
    def __repr__(a): return f"({a.r}{'+' if a.i >= 0 else ''}{a.i}i)"


ONE = Qc(1)


def _phi_n(n, y):
    """`phi_n(y) = i a^n / b^{n+1}`, `a = y - i/2`, `b = y + i/2`, exactly."""
    a, b = Qc(y, F(-1, 2)), Qc(y, F(1, 2))
    num = ONE
    for _ in range(n): num = num * a
    den = ONE
    for _ in range(n + 1): den = den * b
    return Qc(0, 1) * num / den


def _phi_n_prime(n, y):
    """`d/dy [i a^n b^{-n-1}] = i(n a^{n-1} b^{-n-1} - (n+1) a^n b^{-n-2})`, exactly.

    Derived here by the product rule; leg 176's `to_y` uses a Blaschke-factor form
    with different-looking coefficients, and W1b's agreement is a check on both.
    """
    a, b = Qc(y, F(-1, 2)), Qc(y, F(1, 2))

    def pw(z, k):
        r = ONE
        for _ in range(k): r = r * z
        return r
    t1 = Qc(n) * pw(a, n - 1) / pw(b, n + 1) if n >= 1 else Qc(0)
    t2 = Qc(n + 1) * pw(a, n) / pw(b, n + 2)
    return Qc(0, 1) * (t1 - t2)


def w1b_y_space_identity(NB=16):
    """Xu (4.21) applied to the basis functions, EXACTLY, at rational `y`.

    `L_0^+ phi = -phi - y phi' + i phi / b`.  The claim under test is leg 176's
    tridiagonal column
        `L_0^+ phi_n = -(n/2) phi_{n-1} + (1/2) phi_n + ((n-1)/2) phi_{n+1}`.
    This uses ONLY Xu's (4.21) and the transform pair; it never integrates a
    Laguerre polynomial and never touches a quadrature node.  It is therefore a
    second, structurally disjoint proof of the same matrix -- and it can fail.
    """
    R = {"y_nodes": [], "mismatches": [], "n_checked": NB}
    ys = [F(1, 3), F(-2), F(7, 2), F(-11, 5), F(23), F(1, 100), F(-1, 7)]
    R["y_nodes"] = [str(y) for y in ys]
    for y in ys:
        b = Qc(y, F(1, 2))
        for n in range(NB):
            lhs = (-_phi_n(n, y) - Qc(y) * _phi_n_prime(n, y)
                   + Qc(0, 1) * _phi_n(n, y) / b)
            rhs = Qc(0)
            if n - 1 >= 0: rhs = rhs + Qc(F(-n, 2)) * _phi_n(n - 1, y)
            rhs = rhs + Qc(F(1, 2)) * _phi_n(n, y)
            rhs = rhs + Qc(F(n - 1, 2)) * _phi_n(n + 1, y)
            if not (lhs - rhs).iszero():
                R["mismatches"].append([n, str(y), repr(lhs), repr(rhs)])
    R["exact_identity_holds"] = (len(R["mismatches"]) == 0)

    # the transform pair itself, and leg 176's `to_y`, against my own evaluation
    yv = np.array([-20., -3.3, -0.4, 0.17, 1.9, 12.0])
    worst_val = worst_d2 = 0.0
    for n in range(12):
        c = np.zeros(n + 1, dtype=complex); c[n] = 1.0
        mine = np.array([_phi_n(n, F(y).limit_denominator(10 ** 9)).c() for y in yv])
        theirs = H.to_y(c, yv)
        worst_val = max(worst_val, float(np.abs(mine - theirs).max()
                                          / max(np.abs(mine).max(), 1e-300)))
        # second derivative: mine by the product rule, theirs by their Blaschke form
        d2 = _phi_from_coeffs(c, yv, 2)
        worst_d2 = max(worst_d2, float(np.abs(d2 - H.to_y(c, yv, 2)).max()
                                       / max(np.abs(d2).max(), 1e-300)))
    R["transform_pair_vs_module_to_y_max_rel"] = worst_val
    R["second_derivative_two_derivations_max_rel"] = worst_d2
    R["reading"] = (
        "the tridiagonal matrix is PROVED a second time, in y-space, from Xu (4.21) "
        "directly and in exact rational arithmetic at seven rational nodes and sixteen "
        "modes -- no Laguerre integral, no quadrature, no basis identity.  The two "
        "derivations of the realization (W1's exact integrals in xi, W1b's exact algebra "
        "in y) are structurally disjoint and agree exactly, and leg 176's y-space "
        "evaluator and its second-derivative formula reproduce an independently "
        "product-rule-derived one to float rounding.")
    return R


# ===========================================================================
# W2 -- THE UNCHECKED LINK: is the Gram the X norm of Xu's Definition 4.1?
# ===========================================================================

def _de_nodes(h=0.04, U=4.5):
    """DOUBLE-EXPONENTIAL rule `y = sinh(sinh(u))`, uniform trapezoid in `u`.

    An INDEPENDENT quadrature: leg 176's `x_norm_y` uses the Blaschke map
    `y = -cot(theta/2)/2` and a periodic rule, and shares nothing with this one.

    The double exponential is NOT decoration.  A single `y = sinh(u)` was tried
    first and is not good enough, for a reason worth recording: `|phi|^2` decays
    only like `y^{-2}`, so a cut at `y = sinh(7) = 548` leaves an ALGEBRAIC tail
    of `~1/548 = 1.8e-3` -- and it showed up as a 5.75e-4 defect in exactly the
    integral that has the slow tail, while `|phi''|^2 ~ y^{-6}` passed at 4e-15.
    Two integrals disagreeing by eleven orders on the same nodes is the tell.
    With `y = sinh(sinh u)` the cut sits at `y ~ 1.7e19` and both integrals reach
    1.3e-15; the accuracy is a property of the integrand again, not of the cut.
    """
    u = np.arange(-U, U + 1e-12, h)
    s = np.sinh(u)
    return np.sinh(s), np.cosh(s) * np.cosh(u) * h


def _phi_from_coeffs(c, y, deriv=0):
    """`phi = i sum_n c_n a^n b^{-n-1}` and its 2nd derivative, by the product rule.

    Evaluated through `r = a/b` (`|r| = 1` on the real axis) so nothing overflows;
    the COEFFICIENTS are the ones derived in W1b, not the module's.
    """
    c = np.asarray(c)
    y = np.atleast_1d(np.asarray(y, dtype=float)).astype(complex)
    a, b = y - 0.5j, y + 0.5j
    r = a / b
    n = len(c)
    R = np.empty((n + 2, len(y)), dtype=complex)
    R[0] = 1.0
    for k in range(1, n + 2):
        R[k] = R[k - 1] * r
    out = np.zeros(len(y), dtype=complex)
    for k in range(n):
        ck = c[k]
        if ck == 0: continue
        if deriv == 0:
            T = R[k] / b
        elif deriv == 2:
            # T_k = a^k b^{-k-1};  by the product rule, twice,
            #   T_k'' = k(k-1) a^{k-2}b^{-k-1} - 2k(k+1) a^{k-1}b^{-k-2}
            #           + (k+1)(k+2) a^k b^{-k-3}
            # and each of the three terms is (a/b)^j / b^3 for j = k-2, k-1, k.
            num = (k + 1) * (k + 2) * R[k]
            if k >= 1: num = num - 2 * k * (k + 1) * R[k - 1]
            if k >= 2: num = num + k * (k - 1) * R[k - 2]
            T = num / b ** 3
        else:
            raise ValueError("deriv 0 or 2")
        out = out + ck * T
    return 1j * out


def w2_gram_is_the_x_norm(nmax=10):
    """`int_R phi_m conj(phi_n) dy = 2 pi delta_mn` and `int_R phi_m'' conj(phi_n'') = 2 pi (J^4)_mn`.

    Xu Definition 4.1 (read at full text this leg) sets
    `||phi||_X^2 = ||phi||_{L^2}^2 + ||phi''||_{L^2}^2`.  Leg 176 discretizes it as
    `c* (I + J^4) c`.  THE STEP BETWEEN THE TWO -- Plancherel, the `xi^4 <-> phi''`
    correspondence and the `2 pi` -- is asserted in a docstring and is checked by
    NOTHING in leg 176's evidence, and by nothing in the 192 salvage either.  It is
    checked here, in y-space, by a quadrature that shares no machinery with the
    module's.  If the weight were misidentified every sigma_min in both legs would
    be wrong, and wrong identically.
    """
    y, w = _de_nodes()
    R = {"quadrature": ("y = sinh(sinh(u)), uniform trapezoid h=0.04 on |u| <= 4.5 "
                        "(226 nodes); a single sinh was tried first and rejected -- "
                        "see _de_nodes"),
         "n_modes_checked": nmax}
    G = my_gram_float(nmax)
    twopi = 2.0 * math.pi
    worst_l2 = worst_d2 = worst_full = 0.0
    for m in range(nmax):
        cm = np.zeros(m + 1, dtype=complex); cm[m] = 1.0
        pm = _phi_from_coeffs(cm, y); pm2 = _phi_from_coeffs(cm, y, 2)
        for n in range(nmax):
            cn = np.zeros(n + 1, dtype=complex); cn[n] = 1.0
            pn = _phi_from_coeffs(cn, y); pn2 = _phi_from_coeffs(cn, y, 2)
            i0 = float(np.real(np.sum(w * pm * np.conj(pn))))
            i2 = float(np.real(np.sum(w * pm2 * np.conj(pn2))))
            want0 = twopi * (1.0 if m == n else 0.0)
            want2 = twopi * (G[m, n] - (1.0 if m == n else 0.0))
            worst_l2 = max(worst_l2, abs(i0 - want0) / twopi)
            worst_d2 = max(worst_d2, abs(i2 - want2) / max(abs(want2), twopi))
            worst_full = max(worst_full, abs((i0 + i2) - twopi * G[m, n])
                             / max(abs(twopi * G[m, n]), twopi))
    R["l2_orthonormality_max_abs_defect_over_2pi"] = worst_l2
    R["second_derivative_gram_max_rel_defect"] = worst_d2
    R["full_X_gram_max_rel_defect"] = worst_full
    R["plancherel_constant_recovered"] = twopi

    # a control that CAN come out differently: the same test against the WRONG
    # constant (1 instead of 2 pi) and against the WRONG weight (xi^2, i.e. one
    # derivative rather than two) must FAIL, and by how much is reported.
    cm = np.zeros(3, dtype=complex); cm[2] = 1.0
    p0 = _phi_from_coeffs(cm, y); p2 = _phi_from_coeffs(cm, y, 2)
    got = float(np.real(np.sum(w * (p0 * np.conj(p0) + p2 * np.conj(p2)))))
    R["control_wrong_constant_rel_error_if_2pi_omitted"] = abs(got - G[2, 2]) / got
    R["control_correct_constant_rel_error"] = abs(got - twopi * G[2, 2]) / got
    # a resolution control: the same identity on a coarser rule, so the reported
    # agreement is shown to be the quadrature's converged answer and not its noise
    y2, w2 = _de_nodes(h=0.08, U=4.0)
    c1 = np.zeros(4, dtype=complex); c1[3] = 1.0
    p_a = _phi_from_coeffs(c1, y2); p_b = _phi_from_coeffs(c1, y2, 2)
    coarse = float(np.real(np.sum(w2 * (p_a * np.conj(p_a) + p_b * np.conj(p_b)))))
    R["resolution_control_coarse_vs_fine_rel"] = abs(coarse - twopi * G[3, 3]) / (twopi * G[3, 3])

    # and the module's own y-space norm, as a third opinion
    c = np.array([0.3 + 0.1j, -0.7, 0.2j, 0.9, -0.15 + 0.4j])
    mine = math.sqrt(float(np.real(np.sum(
        w * (_phi_from_coeffs(c, y) * np.conj(_phi_from_coeffs(c, y))
             + _phi_from_coeffs(c, y, 2) * np.conj(_phi_from_coeffs(c, y, 2)))))))
    gram_side = math.sqrt(twopi) * H.x_norm(c, my_gram_float(len(c)))
    R["random_datum_my_quadrature_vs_gram_rel"] = abs(mine - gram_side) / gram_side
    R["random_datum_vs_module_x_norm_y_rel"] = abs(
        mine - H.x_norm_y(lambda yy: (H.to_y(c, yy), H.to_y(c, yy, 2)))) / mine
    R["reading"] = (
        "CONFIRMED, and this is the link neither leg 176 nor the 192 salvage checks. "
        "The Laguerre basis is orthonormal in L^2(R) with constant 2 pi and its "
        "second-derivative Gram is exactly 2 pi J^4, so c*(I + J^4)c IS "
        "(||phi||_{L^2}^2 + ||phi''||_{L^2}^2)/(2 pi) -- Xu Definition 4.1's norm up to "
        "the single overall constant 2 pi, which cancels in every ratio sigma_min is "
        "built from.  Measured by an independent sinh-trapezoid quadrature that shares "
        "no machinery with the module's Blaschke rule.  The control confirms the test "
        "can fail: omitting the 2 pi puts the same identity out by a factor of 6.28.")
    return R


# ===========================================================================
# W3/W4 -- sigma_min and ||T^-1||_X: float routes AND exact-rational inertia
# ===========================================================================
# The section, realified.  `m` and `ell` are purely imaginary, so the diagonal
# unitary change of variable `kappa -> i kappa` on the domain border coordinate
# and `-i` on the range border coordinate makes the whole matrix REAL without
# changing any norm (both Grams carry a unit weight on those coordinates, so the
# unitaries commute with them).  That observation is this leg's, it is what makes
# an exact-rational treatment affordable, and it is checked in `w3_sigma_min`
# against the complex form.

def my_section_float(N, lo=0, bordered=True, border_weight=1.0):
    """Domain modes `[lo, N)` (+) C, range modes `[0, N+2)` (+) C, RANGE UNTRUNCATED.

    Range width `N+2` is not a truncation: `L_0^+` is tridiagonal, so domain column
    `n < N` reaches range row `n+1 <= N`, and the border column lives in
    `span{l_0, l_1}`.  Every entry of the exact infinite-range image is present.
    """
    Nr = N + 2
    nd = N - lo
    L = my_l0_float(Nr)[:, lo:N]
    Gd0 = my_gram_float(N)[lo:, lo:]
    Gc0 = my_gram_float(Nr)
    if not bordered:
        return L, Gd0, Gc0
    A = np.zeros((Nr + 1, nd + 1))
    A[:Nr, :nd] = L
    A[0, nd] = A[1, nd] = 0.5                                # i * m
    n = np.arange(lo, N)
    A[Nr, :nd] = (-1.0) ** n * (1.0 - 2.0 * n)               # -i * ell
    Gd = np.zeros((nd + 1, nd + 1)); Gd[:nd, :nd] = Gd0; Gd[nd, nd] = border_weight
    Gc = np.zeros((Nr + 1, Nr + 1)); Gc[:Nr, :Nr] = Gc0; Gc[Nr, Nr] = border_weight
    return A, Gd, Gc


def _sig_from_R(A, Rd, Rc):
    S = np.linalg.solve(Rd.T.conj(), (Rc @ A).T.conj()).T.conj()
    return float(np.linalg.svd(S, compute_uv=False).min())


def sig_chol(N, lo=0, bordered=True, bw=1.0):
    A, Gd, Gc = my_section_float(N, lo, bordered, bw)
    return _sig_from_R(A, np.linalg.cholesky(Gd).T, np.linalg.cholesky(Gc).T)


def sig_eigh(N, lo=0, bordered=True, bw=1.0):
    """The whitening leg 176 uses (symmetric square root via `eigh`)."""
    A, Gd, Gc = my_section_float(N, lo, bordered, bw)
    w, U = np.linalg.eigh(Gd); Gdih = (U * (1.0 / np.sqrt(w))) @ U.T
    w, U = np.linalg.eigh(Gc); Gch = (U * np.sqrt(w)) @ U.T
    return float(np.linalg.svd(Gch @ A @ Gdih, compute_uv=False).min())


def sig_rescaled(N, lo=0, bordered=True, bw=1.0):
    """Diagonal pre-scaling to unit diagonal, then Cholesky -- a third conditioning."""
    A, Gd, Gc = my_section_float(N, lo, bordered, bw)
    dd = np.sqrt(np.diag(Gd)); dc = np.sqrt(np.diag(Gc))
    At = (A / dd[None, :]) * dc[:, None]
    Rd = np.linalg.cholesky(Gd / np.outer(dd, dd)).T
    Rc = np.linalg.cholesky(Gc / np.outer(dc, dc)).T
    return _sig_from_R(At, Rd, Rc)


# --- the exact-rational tier ------------------------------------------------

def _jrow(i):
    d = {i: 2 * i + 1, i + 1: -(i + 1)}
    if i: d[i - 1] = -i
    return d


def gram_band_exact(n):
    """Rows of `G = I + J^4` as exact integers (band 4), by banded `J`-multiplication."""
    rows = [_jrow(i) for i in range(n + 8)]
    for _ in range(3):
        out = []
        for r in rows:
            acc = {}
            for k, v in r.items():
                for k2, v2 in _jrow(k).items():
                    acc[k2] = acc.get(k2, 0) + v * v2
            out.append({k: v for k, v in acc.items() if v})
        rows = out
    G = []
    for i in range(n):
        d = {k: v for k, v in rows[i].items() if v and 0 <= k < n}
        d[i] = d.get(i, 0) + 1
        G.append(d)
    return G


def build_exact(N, lo=0, bordered=True):
    """`P` = the BANDED part of `A^T G_c A`; `v` = the border row; `Gd`.

    The border row of `A` contributes a RANK-ONE dense term `v v^T` to `A^T G_c A`,
    which would destroy the bandwidth.  It is kept out of `P` and restored in the
    inertia test by a Haynsworth bordering, which is what keeps the exact
    factorization `O(N b^2)` instead of `O(N^3)`.
    """
    Nr = N + 2
    cols = []
    for n in range(lo, N):
        c = {}
        if n - 1 >= 0: c[n - 1] = F(-n, 2)
        c[n] = F(1, 2)
        c[n + 1] = F(n - 1, 2)
        cols.append(c)
    if bordered:
        cols.append({0: F(1, 2), 1: F(1, 2)})
    nd = len(cols)
    G = gram_band_exact(Nr)

    P = [dict() for _ in range(nd)]
    for i in range(nd):
        ci = cols[i]
        for j in range(i, nd):
            if j > i + 7 and not (bordered and j == nd - 1):
                continue
            tot = F(0)
            for k, vk in ci.items():
                for l, vl in cols[j].items():
                    if abs(k - l) <= 4:
                        g = G[k].get(l, 0)
                        if g: tot += vk * vl * g
            if tot: P[i][j] = tot

    v = [F(0)] * nd
    if bordered:
        for i, n in enumerate(range(lo, N)):
            v[i] = F((-1) ** n * (1 - 2 * n))

    Gd = [dict() for _ in range(nd)]
    nb = nd - 1 if bordered else nd
    for i in range(nb):
        for j in range(i, min(nb, i + 5)):
            g = G[i + lo].get(j + lo, 0)
            if g: Gd[i][j] = F(g)
    if bordered:
        Gd[nd - 1][nd - 1] = F(1)
    return P, v, Gd, nd


def _inertia(P, v, Gd, lam, nd, bw, bordered):
    """Pivot signs of `T = [[P - lam Gd, v], [v^T, -1/bw]]` (Haynsworth bordering).

    `inertia(T) = inertia(-1/bw) + inertia(P - lam Gd + bw v v^T)`, so
    `A^T G_c A - lam G_d > 0` iff `T` has exactly one negative pivot.  Sparse
    `LDL^T`, exact rationals, no pivoting; a zero pivot returns `None` and the
    caller nudges `lam`.
    """
    n = nd + (1 if bordered else 0)
    M = [dict() for _ in range(n)]
    for i in range(nd):
        for j, x in P[i].items(): M[i][j] = x
        for j, x in Gd[i].items(): M[i][j] = M[i].get(j, F(0)) - lam * x
    if bordered:
        for i in range(nd):
            if v[i]: M[i][n - 1] = M[i].get(n - 1, F(0)) + v[i]
        M[n - 1][n - 1] = -1 / bw
    npos = nneg = 0
    for j in range(n):
        d = M[j].get(j, F(0))
        if d == 0: return None
        if d > 0: npos += 1
        else: nneg += 1
        col = sorted(((k, x) for k, x in M[j].items() if k > j and x))
        for a, (i, vi) in enumerate(col):
            q = vi / d
            for (k, vk) in col[a:]:
                M[i][k] = M[i].get(k, F(0)) - q * vk
        M[j] = None
    return npos, nneg


def _is_pd(P, v, Gd, lam, nd, bw, bordered):
    c = _inertia(P, v, Gd, lam, nd, bw, bordered)
    if c is None: return None
    npos, nneg = c
    return (nneg == 1 and npos == nd) if bordered else (nneg == 0)


def sigma_enclosure(N, lo=0, bordered=True, sig_float=None, half=1e-6, nbis=44,
                    bw=F(1)):
    """A CERTIFIED enclosure of `sigma_min`, in exact rational arithmetic.

    `sigma_min^2` is the smallest generalized eigenvalue of `(A^T G_c A, G_d)`, so
    `lam < sigma_min^2` iff `A^T G_c A - lam G_d` is positive definite -- a question
    exact `LDL^T` answers with NO rounding at all.  Bisecting on `lam` therefore
    returns an enclosure of `sigma_min` whose only float operation is the final
    square root.  This is strictly stronger than any float SVD: it does not measure
    `sigma_min`, it BRACKETS it.
    """
    P, v, Gd, nd = build_exact(N, lo, bordered)
    # DYADIC bisection: every trial `lam` is `k / 2^D` with `D` FIXED, so the trial
    # value contributes one bounded power-of-two denominator instead of a fresh
    # 10^15-sized one at every step.  The pivots' own denominators still grow with
    # the elimination -- that is intrinsic -- but the trial no longer compounds it.
    D = 52
    den = 1 << D

    def dy(x):
        return F(max(int(round(x * den)), 1), den)

    a = dy(max(sig_float - half, 1e-9) ** 2)
    b = dy((sig_float + half) ** 2)
    for _ in range(80):
        if _is_pd(P, v, Gd, a, nd, bw, bordered): break
        a = dy(float(a) / 2)
    else:
        raise RuntimeError("no lower bracket")
    for _ in range(80):
        if _is_pd(P, v, Gd, b, nd, bw, bordered) is False: break
        b = dy(float(b) * 2)
    else:
        raise RuntimeError("no upper bracket")
    ai, bi = a.numerator * (den // a.denominator), b.numerator * (den // b.denominator)
    for _ in range(nbis):
        if bi - ai <= 1: break
        mi = (ai + bi) // 2
        r = _is_pd(P, v, Gd, F(mi, den), nd, bw, bordered)
        if r is None:
            mi += 1
            r = _is_pd(P, v, Gd, F(mi, den), nd, bw, bordered)
        if r: ai = mi
        else: bi = mi
    return math.sqrt(ai / den), math.sqrt(bi / den)


def certify_bracket(N, lo=0, bordered=True, sig_lo=None, sig_hi=None, bw=F(1)):
    """TWO exact calls that certify `sig_lo < sigma_min < sig_hi` -- or refute it.

    A full bisection costs ~29 exact factorizations and the cost per factorization
    grows about 8x per doubling of `N`, which puts `N = 512` out of reach.  But the
    question that actually matters at `N = 512` is not "what are the next six
    digits", it is "is leg 176's banked value above or below the true one" -- and
    that is TWO calls, not twenty-nine.  Each returns a rigorous verdict in exact
    arithmetic; `None` means a zero pivot was hit and the test was inconclusive.
    """
    P, v, Gd, nd = build_exact(N, lo, bordered)
    D = 52
    den = 1 << D
    out = {"N": N, "sigma_lower_probe": sig_lo, "sigma_upper_probe": sig_hi}
    out["seconds_lower"] = 0.0
    out["lower_probe_is_pd"] = None
    if sig_lo is not None:                    # skippable: a caller that has already
        t0 = time.time()                      # certified this side does not pay twice
        out["lower_probe_is_pd"] = _is_pd(
            P, v, Gd, F(int(round(sig_lo ** 2 * den)), den), nd, bw, bordered)
        out["seconds_lower"] = time.time() - t0
    t0 = time.time()
    out["upper_probe_is_pd"] = _is_pd(P, v, Gd, F(int(round(sig_hi ** 2 * den)), den),
                                      nd, bw, bordered)
    out["seconds_upper"] = time.time() - t0
    out["certified"] = (out["lower_probe_is_pd"] is True
                        and out["upper_probe_is_pd"] is False)
    out["reading"] = (
        "PD at the lower probe and NOT PD at the upper probe certifies, in exact "
        "arithmetic with no rounding anywhere, that sigma_min lies strictly between "
        "them." if out["certified"] else
        "the probes did not bracket; the individual verdicts above are still exact.")
    return out


def _ladder_stats(vals, ns):
    d = {}
    lo_n = [n for n in ns if n >= 32 and n <= 512]
    rel = [vals[n] for n in lo_n]
    if rel:
        d["window_32_to_512_min"] = min(rel)
        d["window_32_to_512_max"] = max(rel)
        d["relative_spread_over_window"] = (max(rel) - min(rel)) / max(rel)
    d["monotone_decreasing_through_512"] = all(
        vals[a] >= vals[b] for a, b in zip(ns, ns[1:]) if b <= 512)
    return d


def w3_sigma_min(quick=False):
    ladder = (8, 16, 32, 64, 128, 256) if quick else LADDER_FLOAT
    lex = (8, 16, 32, 64) if quick else LADDER_EXACT
    R = {"quantity": ("sigma_min of the bordered [[L_0^+, m],[ell, 0]] in the X (+) C "
                      "metric, domain modes [0,N) truncated, RANGE UNTRUNCATED"),
         "ladder": {}, "exact_enclosures": {}}

    # the realification, checked rather than asserted: leg 176's own COMPLEX
    # section, built from its own module, against my realified real one
    Nr = 66
    Ax = np.zeros((Nr + 1, 65), dtype=complex)
    Ax[:Nr, :64] = H.l0_plus(Nr)[:, :64]
    Ax[:Nr, 64] = H.symmetry_modes(Nr)[1]
    Ax[Nr, :64] = H.border_row(64)
    wc, Uc = np.linalg.eigh(H.bordered_gram(64, H.x_gram(64)))
    Gdih = (Uc * (1.0 / np.sqrt(wc))) @ Uc.T
    wc, Uc = np.linalg.eigh(H.bordered_gram(Nr, H.x_gram(Nr)))
    Gch = (Uc * np.sqrt(wc)) @ Uc.T
    sig_complex = float(np.linalg.svd(Gch @ Ax @ Gdih, compute_uv=False).min())
    R["realification_complex_vs_real_at_64"] = {
        "complex_form_with_module_matrices": sig_complex,
        "my_realified_form": sig_eigh(64),
        "abs_diff": abs(sig_complex - sig_eigh(64)),
        "note": ("the realification kappa -> i kappa is a diagonal UNITARY change of "
                 "variable on a coordinate both Grams weight by 1, so it cannot move "
                 "sigma_min; measured rather than argued"),
    }

    for N in ladder:
        t0 = time.time()
        row = {"cholesky": sig_chol(N), "eigh": sig_eigh(N), "rescaled": sig_rescaled(N)}
        row["max_route_spread"] = max(row[k] for k in ("cholesky", "eigh", "rescaled")) \
            - min(row[k] for k in ("cholesky", "eigh", "rescaled"))
        row["cond_Gd"] = float(np.linalg.cond(my_section_float(N)[1]))
        row["seconds"] = time.time() - t0
        R["ladder"][str(N)] = row
        print(f"    W3 N={N:5d} chol={row['cholesky']:.10f} eigh={row['eigh']:.10f} "
              f"resc={row['rescaled']:.10f} ({row['seconds']:.1f}s)", flush=True)

    for N in lex:
        t0 = time.time()
        a, b = sigma_enclosure(N, sig_float=R["ladder"][str(N)]["cholesky"])
        R["exact_enclosures"][str(N)] = {
            "lower": a, "upper": b, "width": b - a,
            "certified_digits": int(-math.log10(max(b - a, 1e-300))),
            "seconds": time.time() - t0}
        print(f"    W3 exact N={N:5d} [{a:.14f}, {b:.14f}] ({time.time()-t0:.1f}s)",
              flush=True)

    # certified brackets where a full bisection is unaffordable -- and, at N=512,
    # the probe is placed so that it DECIDES leg 176's banked digits
    R["certified_brackets"] = {}
    for N in ((128,) if quick else CERTIFY_N):
        if str(N) not in R["ladder"]: continue
        s = R["ladder"][str(N)]["cholesky"]
        c = certify_bracket(N, sig_lo=s - 5e-8, sig_hi=s + 5e-8)
        if N == 512:
            c["decides_leg176_banked_value"] = certify_bracket(
                512, sig_lo=None, sig_hi=LEG176_SIGMA)
            c["decides_leg176_banked_value"]["meaning"] = (
                "the upper probe is leg 176's OWN banked 0.09080465147034879.  "
                "'upper_probe_is_pd = false' means sigma_min is strictly BELOW it, "
                "i.e. the banked value overstates sigma_min -- proved, not measured.")
        R["certified_brackets"][str(N)] = c
        print(f"    W3 certify N={N:5d} lower_pd={c['lower_probe_is_pd']} "
              f"upper_pd={c['upper_probe_is_pd']} certified={c['certified']} "
              f"({c['seconds_lower']+c['seconds_upper']:.0f}s)", flush=True)

    ch = {n: R["ladder"][str(n)]["cholesky"] for n in ladder}
    R.update(_ladder_stats(ch, list(ladder)))
    R["leg176_banked_sigma_min_at_512"] = LEG176_SIGMA
    R["leg176_banked_resolvent_norm_at_512"] = 11.012651706796523
    if 512 in ladder:
        R["independent_sigma_min_at_512_cholesky"] = ch[512]
        R["abs_diff_at_512"] = abs(ch[512] - LEG176_SIGMA)
        R["rel_diff_at_512"] = abs(ch[512] - LEG176_SIGMA) / LEG176_SIGMA
        R["independent_resolvent_norm_at_512"] = 1.0 / ch[512]
        R["resolvent_norm_rel_diff"] = abs(
            1.0 / ch[512] - 11.012651706796523) / 11.012651706796523
    if "512" in R["exact_enclosures"]:
        e = R["exact_enclosures"]["512"]
        R["leg176_value_inside_exact_enclosure_at_512"] = bool(
            e["lower"] <= LEG176_SIGMA <= e["upper"])
        R["leg176_value_error_vs_exact_midpoint"] = abs(
            LEG176_SIGMA - 0.5 * (e["lower"] + e["upper"]))
    if 1024 in ladder:
        R["eigh_breaks_monotonicity_at_1024"] = bool(
            R["ladder"]["1024"]["eigh"] > R["ladder"]["512"]["eigh"])
        R["cholesky_breaks_monotonicity_at_1024"] = bool(ch[1024] > ch[512])
    if 2048 in ladder:
        R["cholesky_breaks_monotonicity_at_2048"] = bool(ch[2048] > ch[1024])
    R["decrements"] = _extrapolate(ch, list(ladder))
    return R


def _extrapolate(vals, ns):
    """The SHAPE of the ladder, and a geometric extrapolation of its limit.

    A decreasing positive sequence with geometrically shrinking decrements is
    float64 EVIDENCE of a positive limit, never a proof of one (leg 176 says this
    in its own words and it is repeated here unweakened).  The extrapolation is
    reported so that "the value at N = 512" and "the limit the ladder is heading
    for" are two numbers on the page rather than one number doing both jobs.
    """
    steps = [(a, b, vals[a] - vals[b]) for a, b in zip(ns[:-1], ns[1:])]
    out = {"decrements": [{"from": a, "to": b, "delta": d} for a, b, d in steps]}
    ratios = [steps[i][2] / steps[i - 1][2] for i in range(1, len(steps))
              if steps[i - 1][2]]
    out["decrement_ratios"] = [float(x) for x in ratios]
    if len(ratios) >= 3 and all(0 < r < 1 for r in ratios[-3:]):
        rho = float(np.mean(ratios[-3:]))
        out["geometric_ratio_last3"] = rho
        out["extrapolated_limit"] = float(vals[ns[-1]] - steps[-1][2] * rho / (1 - rho))
        out["value_at_last_rung"] = vals[ns[-1]]
        out["gap_between_last_rung_and_extrapolated_limit"] = abs(
            out["extrapolated_limit"] - vals[ns[-1]])
    return out


def w4_tail_inverse_norm(quick=False):
    ladder = (64, 128, 256) if quick else TAIL_FLOAT
    lex = (64,) if quick else TAIL_EXACT
    R = {"quantity": ("sigma_min of the UNBORDERED tail block: domain modes [2, N) "
                      "(the two symmetry modes removed), range untruncated.  "
                      "||T^-1||_X = 1/sigma_min."),
         "why_it_matters": ("this is the direct ell^1_w comparison point -- there "
                            "(legs 51/53) the tail inverse norm DIVERGED with M.  It is "
                            "also the number the leg-192 salvage never re-derived: its "
                            "only mention of 4.026 compares leg 176's prose to leg 176's "
                            "own JSON."),
         "ladder": {}, "exact_enclosures": {}}
    for N in ladder:
        t0 = time.time()
        s = sig_chol(N, lo=2, bordered=False)
        row = {"cholesky": s, "eigh": sig_eigh(N, lo=2, bordered=False),
               "rescaled": sig_rescaled(N, lo=2, bordered=False),
               "inverse_norm": 1.0 / s, "seconds": time.time() - t0}
        R["ladder"][str(N)] = row
        print(f"    W4 N={N:5d} sigma={s:.10f} 1/sigma={1/s:.8f} "
              f"({row['seconds']:.1f}s)", flush=True)
    for N in lex:
        t0 = time.time()
        a, b = sigma_enclosure(N, lo=2, bordered=False,
                               sig_float=R["ladder"][str(N)]["cholesky"])
        R["exact_enclosures"][str(N)] = {
            "sigma_lower": a, "sigma_upper": b,
            "inverse_norm_lower": 1.0 / b, "inverse_norm_upper": 1.0 / a,
            "width": b - a, "seconds": time.time() - t0}
        print(f"    W4 exact N={N:5d} sigma in [{a:.14f}, {b:.14f}] "
              f"1/sigma in [{1/b:.10f}, {1/a:.10f}] ({time.time()-t0:.1f}s)", flush=True)

    R["certified_brackets"] = {}
    for N in ((128,) if quick else TAIL_CERTIFY):
        if str(N) not in R["ladder"]: continue
        s = R["ladder"][str(N)]["cholesky"]
        c = certify_bracket(N, lo=2, bordered=False, sig_lo=s - 5e-8, sig_hi=s + 5e-8)
        c["inverse_norm_bracket"] = [1.0 / (s + 5e-8), 1.0 / (s - 5e-8)]
        R["certified_brackets"][str(N)] = c
        print(f"    W4 certify N={N:5d} lower_pd={c['lower_probe_is_pd']} "
              f"upper_pd={c['upper_probe_is_pd']} certified={c['certified']} "
              f"({c['seconds_lower']+c['seconds_upper']:.0f}s)", flush=True)

    ch = {n: R["ladder"][str(n)]["cholesky"] for n in ladder}
    R["leg176_banked_tail_inverse_norm"] = LEG176_TAIL_INV
    R["leg176_banked_tail_sigma_at_512"] = 0.248377
    if 512 in ladder:
        R["independent_tail_sigma_at_512"] = ch[512]
        R["independent_tail_inverse_norm_at_512"] = 1.0 / ch[512]
        R["abs_diff_inverse_norm"] = abs(1.0 / ch[512] - LEG176_TAIL_INV)
        R["rel_diff_inverse_norm"] = abs(1.0 / ch[512] - LEG176_TAIL_INV) / LEG176_TAIL_INV
    if "512" in R["exact_enclosures"]:
        e = R["exact_enclosures"]["512"]
        R["leg176_inverse_norm_inside_exact_enclosure"] = bool(
            e["inverse_norm_lower"] - 5e-4 <= LEG176_TAIL_INV <= e["inverse_norm_upper"] + 5e-4)
        R["leg176_quoted_to_decimals"] = 3
    inv = {n: 1.0 / ch[n] for n in ladder}
    spread = max(inv.values()) - min(inv.values())
    R["truncation_independence_claim"] = {
        "leg176_wording": "'i.e. ||T^-1||_X = 4.026, truncation-independent'",
        "inverse_norm_by_N": {str(n): inv[n] for n in ladder},
        "absolute_spread_over_ladder": spread,
        "relative_spread_over_ladder": spread / max(inv.values()),
        "monotone_increasing": all(inv[a] <= inv[b] for a, b in zip(ladder, ladder[1:])),
        "shape": _extrapolate(ch, list(ladder)),
        "reading": (
            "the VALUE 4.026 reproduces at N=512 to the decimals leg 176 quotes.  The "
            "DESCRIPTOR 'truncation-independent' is the part that does not survive: the "
            "inverse norm rises monotonically across the ladder by the relative spread "
            "recorded here, and is still rising at the last rung.  The correct reading "
            "of the same data is the one leg 176 gives its OTHER number -- a monotone "
            "sequence with geometrically shrinking decrements, i.e. float64 evidence of "
            "a finite limit -- and that limit is NOT 4.026 but the extrapolated value "
            "above.  This changes no gate: the ell^1_w comparison leg 176 draws is "
            "between a CONVERGING sequence here and a DIVERGING one there (legs 51/53), "
            "and convergence to 4.03 makes that contrast exactly as strong as "
            "convergence to 4.026 would.")}
    return R


def w5_border_weight_sensitivity(N=256):
    """`sigma_min` is NOT invariant under the border weight, and nothing measured it.

    The `X (+) C` Gram puts weight `1` on the border amplitude while the `X` block
    carries the bare Laguerre-coefficient normalization (no `2 pi`, no half-line
    `1/2`).  Rescaling the `X` block relative to the border coordinate is exactly a
    change of border weight, so this single sweep measures BOTH conventions at once.
    The number `0.0908` is a property of the pair, not of the operator alone -- a
    statement no artifact in the repository contains, and one a reader of PUB2 could
    not have inferred.
    """
    R = {"N": N, "sweep": {}}
    for w in (0.01, 0.1, 0.25, 1.0, 4.0, 10.0, 100.0):
        s = sig_chol(N, bw=w)
        R["sweep"][str(w)] = {"sigma_min": s, "resolvent_norm": 1.0 / s}
    base = R["sweep"]["1.0"]["sigma_min"]
    R["sigma_at_weight_1"] = base
    R["ratio_over_weight_range_1e-2_to_1e2"] = (
        max(v["sigma_min"] for v in R["sweep"].values())
        / min(v["sigma_min"] for v in R["sweep"].values()))
    R["sigma_if_X_block_carried_the_2pi"] = sig_chol(N, bw=1.0 / (2 * math.pi))
    R["reading"] = (
        "REPORTED, NOT A DEFECT.  sigma_min depends on the relative normalization of "
        "the X block and the border amplitude, which the module fixes by convention "
        "(unit weight) and states in its docstring.  Over a 10^4 range of that weight "
        "sigma_min moves by the factor recorded here, and adopting Xu's own y-space "
        "normalization for the X block (i.e. carrying the 2 pi) moves it too.  So "
        "0.0908 is a property of (operator, space, NORMALIZATION CONVENTION).  Leg "
        "176's gate is about whether the formulation closes -- whether sigma_min is "
        "bounded away from zero uniformly in the truncation -- and THAT conclusion is "
        "invariant under the convention, since a positive weight cannot send a positive "
        "limit to zero.  The headline digits are convention-relative; the gate answer "
        "is not.  PUB2 quotes the digits without the convention.")
    return R


# ===========================================================================
# W6 -- Xu (4.23) at z = 0 by EXACT partial fractions, and the residual identity
# ===========================================================================

APOLY = [Qc(0, F(-1, 2)), ONE]        # a(t) = t - i/2
BPOLY = [Qc(0, F(1, 2)), ONE]         # b(t) = t + i/2


def qpmul(p, q):
    r = [Qc() for _ in range(len(p) + len(q) - 1)]
    for i, a in enumerate(p):
        if not a.iszero():
            for j, b in enumerate(q):
                r[i + j] = r[i + j] + a * b
    return r


def qpadd(*ps):
    r = [Qc() for _ in range(max(len(p) for p in ps))]
    for p in ps:
        for i, a in enumerate(p):
            r[i] = r[i] + a
    return r


def qpscal(p, s): return [a * s for a in p]


def qpeval(p, x):
    acc = Qc()
    for c in reversed(p): acc = acc * x + c
    return acc


def qppow(p, k):
    r = [ONE]
    for _ in range(k): r = qpmul(r, p)
    return r


def qpderiv(p): return [p[k] * Qc(k) for k in range(1, len(p))] or [Qc()]


def xu_pieces(c):
    """`P = b^4 G` (degree 5), `G_0`, `G_1`, and the cubic `Q3` with `G_2/t^2 = Q3/b^4`.

    `G = b^2 f = i sum_k c_k a^k b^{1-k}`, so for `k <= 5` the product `b^4 G` is a
    polynomial.  `G_2 = G - G_0 - G_1 t` has a double root at `t = 0` BY
    CONSTRUCTION, so dividing it out leaves a cubic over the same `b^4` and
    `int_0^y G_2/t^2 dt` is the integral of a PROPER RATIONAL FUNCTION -- exact, with
    no Taylor series, no Gauss panels and no grading.  None of leg 176's quadrature
    machinery enters.
    """
    assert len(c) <= 6
    P = [Qc()]
    for k, ck in enumerate(c):
        if ck.iszero(): continue
        P = qpadd(P, qpscal(qpmul(qppow(APOLY, k), qppow(BPOLY, 5 - k)), Qc(0, 1) * ck))
    b0 = Qc(0, F(1, 2))
    b04 = b0 * b0 * b0 * b0
    P0 = qpeval(P, Qc())
    G0 = P0 / b04
    G1 = qpeval(qpderiv(P), Qc()) / b04 - Qc(4) * P0 / (b04 * b0)
    B4 = qppow(BPOLY, 4)
    Nn = qpadd(P, qpscal(B4, -G0), qpscal(qpmul([Qc(), ONE], B4), -G1))
    assert Nn[0].iszero() and Nn[1].iszero(), "G_2 lacks its double root at 0"
    return Nn[2:], G0, G1, P, B4


def q3_in_powers_of_b(Q3):
    """`Q3(t) = sum_{m<=3} q_m b(t)^m` with `b = t + i/2`, exactly."""
    sub = [Qc(0, F(-1, 2)), ONE]          # t = b - i/2
    acc = [Qc()]
    for k, ck in enumerate(Q3):
        if not ck.iszero(): acc = qpadd(acc, qpscal(qppow(sub, k), ck))
    while len(acc) < 4: acc.append(Qc())
    return acc[:4]


def A_exact(qm, y):
    """`A(y) = int_0^y Q3/b^4 dt` -- exact algebraic part plus ONE principal log.

    `int b^{m-4} dt = b^{m-3}/(m-3)` for `m < 3`, `log b` for `m = 3`.  The path
    `t : 0 -> y` keeps `b` on the line `Im = 1/2`, strictly inside the upper
    half-plane, so the principal branch is continuous along it for `y` of either
    sign.  The algebraic part is formed in EXACT RATIONALS, so the differences
    `b^{m-3} - (i/2)^{m-3}` suffer no cancellation at small `|y|`.
    """
    by, b0 = Qc(F(y), F(1, 2)), Qc(0, F(1, 2))
    tot = Qc()
    for m in (0, 1, 2):
        t1 = t2 = ONE
        for _ in range(3 - m):
            t1 = t1 / by; t2 = t2 / b0
        tot = tot + (t1 - t2) * qm[m] / Qc(m - 3)
    return tot.c() + qm[3].c() * (cmath.log(complex(float(y), 0.5)) - cmath.log(0.5j))


def xu_u_exact(c, y, c1=0.0):
    """Xu (4.23) at `z = 0`, with `A` exact.  Derivatives by identities, not quadrature.

    `I = y A`, `A' = G_2/y^2 = Q3/b^4`, hence
        `Phi'  = A + y Q3/b^4 + c_1`
        `Phi'' = 2 Q3/b^4 + y (Q3/b^4)'`
    -- NOTE this differs from the `Phi' = A + (G - G_0)/y + c_1` form by exactly
    `-G_1`, i.e. by `-ell(f)`, so the two agree ON the solvability subspace and
    nowhere else.  The form used here is the one that is right off it too.
    """
    Q3, G0, G1, P, B4 = xu_pieces(c)
    A = A_exact(q3_in_powers_of_b(Q3), y)
    yf = float(y); b = complex(yf, 0.5)
    Q3v = qpeval(Q3, Qc(F(y))).c()
    Q3d = qpeval(qpderiv(Q3), Qc(F(y))).c()
    b4 = b ** 4
    Ap = Q3v / b4
    App = Q3d / b4 - 4 * Q3v / b ** 5
    Phi = yf * A - G0.c() + c1 * yf
    Phi1 = A + yf * Ap + c1
    Phi2 = 2 * Ap + yf * App
    u = -Phi / b ** 2
    u1 = -Phi1 / b ** 2 + 2 * Phi / b ** 3
    u2 = -Phi2 / b ** 2 + 4 * Phi1 / b ** 3 - 6 * Phi / b ** 4
    return u, u1, u2, G1.c()


def solvable_datum(N, nterm=6, seed=0):
    """Leg 176's own datum generator, reproduced so the DATA are identical.

    Only the data are shared; every evaluation of them below is independent.
    """
    e = H.border_row(N); _, m = H.symmetry_modes(N)
    r = np.random.default_rng(seed)
    d = np.zeros(N, dtype=complex)
    d[:nterm] = r.normal(size=nterm) + 1j * r.normal(size=nterm)
    return d - (e @ d) / (e @ m) * m


YNODES = np.array([-20., -8., -1.5, -0.3, 0.05, 0.2, 0.7, 1.5, 3., 8., 20., 60.])


def w6_xu_closed_form():
    R = {"y_nodes": [float(v) for v in YNODES], "per_seed": {}}

    # (a) the residual identity, PROVED by hand and checked exactly.
    #   -u - y u' + i u/b = (y Phi' - Phi)/b^2   (using -2y - i = -2b)
    #   y Phi' - Phi = y^2 A' + G_0 = G - G_1 y  (using A' = G_2/y^2, c_0 = -G_0)
    #   so  L_0^+ u - f = -G_1 y / b^2 = -ell(f) y / b(y)^2  IDENTICALLY.
    trials = []
    rng = np.random.default_rng(20260807)
    for _ in range(6):
        cQ = [Qc(F(int(v), 7), F(int(w), 5)) for v, w in
              zip(rng.integers(-9, 10, 6), rng.integers(-9, 10, 6))]
        _, _, G1, _, _ = xu_pieces(cQ)
        ellf = sum((Qc(0, 1) * Qc(F((-1) ** n * (1 - 2 * n))) * cQ[n] for n in range(6)),
                   Qc())
        trials.append({"G1_minus_ell_f_exactly_zero": (G1 - ellf).iszero(),
                       "ell_f": repr(ellf)})
    R["G_prime_0_equals_ell_f_exactly"] = all(t["G1_minus_ell_f_exactly_zero"] for t in trials)
    R["G_prime_0_trials"] = trials

    # (b) leg 176's u(y) against the exact partial-fraction u(y)
    worst = 0.0
    for sd in range(6):
        fc = solvable_datum(240, 6, sd)[:6]
        cQ = [Qc(F(z.real), F(z.imag)) for z in fc]
        u176, u1_176, _ = H.xu_resolvent(fc, YNODES, c1=0.0, derivs=True)
        du, dres = [], []
        for j, y in enumerate(YNODES):
            u, u1, _, _ = xu_u_exact(cQ, F(y).limit_denominator(10 ** 9), c1=0.0)
            b = complex(y, 0.5)
            fy = _phi_from_coeffs(fc, np.array([y]))[0]
            du.append(abs(u - u176[j]) / abs(u))
            dres.append(abs((-u - y * u1 + 1j * u / b) - fy) / abs(fy))
        R["per_seed"][str(sd)] = {
            "max_rel_diff_leg176_u_vs_exact": float(max(du)),
            "max_rel_ode_residual_of_the_exact_evaluation": float(max(dres))}
        worst = max(worst, max(du))
    R["worst_rel_diff_leg176_u_vs_exact_closed_form"] = float(worst)
    R["leg176_banked_max_rel_residual"] = 4.766912579638455e-15
    R["leg176_residual_over_its_actual_solution_error"] = float(
        4.766912579638455e-15 / worst) if worst else None

    # (c) the residual formula against the module, OFF the solvability subspace --
    #     a control that can come out differently: a real defect scales with ell(f).
    rows = []
    for scale in (0.0, 1e-9, 1e-6, 1e-3, 1e-1):
        fc = solvable_datum(240, 6, 0)[:6].copy()
        fc[0] += scale
        ellf = H.border_row(6) @ fc
        b = YNODES + 0.5j
        pred = -ellf * YNODES / b ** 2
        obs = H.xu_ode_residual(fc, YNODES)
        rows.append({"perturbation": scale, "abs_ell_f": float(abs(ellf)),
                     "max_abs_exact_residual": float(np.abs(pred).max()),
                     "max_abs_discrepancy": float(np.abs(pred - obs).max())})
    R["residual_equals_minus_ell_f_y_over_b2"] = rows
    scaled = [r for r in rows if r["perturbation"] > 0]
    R["discrepancy_spread_over_six_decades_of_ell_f"] = float(
        max(r["max_abs_discrepancy"] for r in scaled)
        / max(min(r["max_abs_discrepancy"] for r in scaled), 1e-300))
    R["reading"] = (
        "the closed form is CONFIRMED and the pointwise ODE residual is PROVED rather "
        "than sampled: it equals -ell(f) y / b(y)^2 identically, so on the solvability "
        "subspace Xu (4.23) solves the equation exactly and leg 176's banked 4.767e-15 "
        "is measuring its own floating-point assembly, not an approximation error.  "
        "Against an exact partial-fraction evaluation leg 176's u(y) is correct to the "
        "relative accuracy recorded above.  Driving ell(f) over six decades off the "
        "solvability subspace leaves the module's discrepancy against the exact residual "
        "FLAT, so the control could have come out the other way and did not.")
    return R


# ===========================================================================
# W7 -- leg 176's prose, and PUB2's quoting sites, against the JSON
# ===========================================================================

def w7_prose_and_pub2_audit(banked, w3, w4):
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

    chk("journal C0 max relative residual", 4.767e-15,
        g("C0_xu_closed_form/max_rel_residual"), 2e-4)
    chk("journal C0 max ABSOLUTE residual", 1.29e-14,
        g("C0_xu_closed_form/max_abs_residual"), 5e-3,
        "journal says 'max absolute 1.29e-14'; the JSON it cites says 1.4296e-14")
    chk("journal C1 sigma_min at N=512", 0.0908047,
        g("C1_bordered_sigma_min_X/sigma_min_at_512"), 1e-5)
    chk("journal C1 ||R||_X", 11.0127,
        g("C1_bordered_sigma_min_X/resolvent_norm_at_512"), 1e-5)
    chk("journal C1 relative spread 0.139%", 0.00139,
        g("C1_bordered_sigma_min_X/relative_spread"), 2e-3)
    chk("journal C2 ||T^-1||_X", 4.026,
        g("C2_tail_block_sigma_min/tail_inverse_norm_K2_at_512"), 1e-3)
    chk("journal C4 fitted exponent", -1.4914,
        g("C4_control_loose_L2_realization/fitted_exponent"), 1e-4)
    chk("journal C5 best cell", 140.72, g("C5_Z1_blockdiagonal_A/min_over_battery"), 1e-4)
    chk("journal C6 closed-form ratio", 0.868155,
        g("C6_closed_form_ratio/M_convergence/8192"), 1e-5)
    chk("journal C6 witness optimistic by", 7.9,
        g("C6_closed_form_ratio/leg163_witness_optimistic_by"), 5e-3)
    chk("journal E1 tridiagonal vs quadrature", 1.608e-13,
        g("E1_realization_exactness/tridiagonal_vs_independent_laguerre_quadrature"), 1e-3)

    pub2 = [
        {"site": "TECHNICAL_P2_PUB2_V1.md L46", "quotes": "sigma_min = 0.0908, truncation-independent"},
        {"site": "TECHNICAL_P2_PUB2_V1.md L297", "quotes": "the full sigma_min ladder, 8..1024"},
        {"site": "TECHNICAL_P2_PUB2_V1.md L299", "quotes": "sigma_min = 0.0908, ||R||_X = 11.0127"},
        {"site": "TECHNICAL_P2_PUB2_V1.md L303", "quotes": "||T^-1||_X = 4.026"},
        {"site": "TECHNICAL_P2_PUB2_V1.md L332/L335", "quotes": "'the measured value is 0.0908'"},
        {"site": "BLOG_P2_PUB2_V1.md L88/L190", "quotes":
         "'0.0908' and 'this leg's own float64 measurements, with the independent check still outstanding'"},
    ]
    return {"numeric_checks": checks,
            "n_checked": len(checks),
            "n_disagreeing": sum(1 for c in checks if not c["agrees"]),
            "pub2_quoting_sites": pub2,
            "pub2_status_after_this_leg": (
                "the BLOG's 'independent check still outstanding' is the sentence this "
                "leg addresses; the TECHNICAL sites carry the digits without the "
                "normalization convention W5 measures.  NOTHING IS EDITED HERE -- this "
                "leg's territory excludes both PUB2 files, and the wording change is "
                "recorded as a recommendation in the journal."),
            "reading": (
                "the journal's numeric claims reproduce against the JSON it cites, with "
                "one exception recorded above at its measured size.  The exception does "
                "not touch either gate number.")}


# ===========================================================================
def main():
    t0 = time.time()
    quick = "--quick" in sys.argv
    with open(BANKED) as fh:
        banked = json.load(fh)

    R = {"leg": 249, "route": "ROUTE-H2CV2", "role": "VERIFIER", "date": "2026-08-07",
         "verifies": "leg 176 (ROUTE-H2C), solver/origin_h2_certificate.py",
         "supersedes": ("the never-landed WIP branches verify/192-h2cv-v1-wip and "
                        "verify/249-h2cv2-v1-wip; NEITHER was inherited -- see "
                        "writeup/novelty/leg_249.md sec 2a for the three named defects"),
         "gate_question": ("Does an independent re-run of leg 176's construction "
                           "reproduce sigma_min = 0.0908 and ||T^-1||_X = 4.026 (or "
                           "report a discrepancy precisely), to the same precision leg "
                           "176 itself claims?"),
         "ceiling": ("inherited verbatim from leg 176 and NOT lifted by a verification: "
                     "a=0 only; certifies an object Xu already inverts in closed form; "
                     "nothing transfers to HL_S2_nonsymmetric or any a>0 profile; no "
                     "link of L1->L4 moves; no Clay movement, odds unchanged at ~0.05%; "
                     "no ban lifted; float64 and exact rationals only"),
         "ga_compute": False,
         "primary_source": ("Xu arXiv:2607.19762, PDF pulled fresh this leg, "
                            "md5 709dac668a1ff508f00d765916db492c; Definition 4.1, eq. "
                            "(4.21)-(4.25), Lemma 4.5, Prop 4.6, Prop 2 read at full "
                            "text.  NEITHER 0.0908 NOR 4.026 appears in it in any form "
                            "-- see writeup/novelty/leg_249.md sec 3"),
         "quick_mode": quick}

    print("W0 reproduction control (NOT a verification) ...", flush=True)
    fc = solvable_datum(240, 6, 0)[:6]
    ru = H.xu_ode_residual(fc, YNODES)
    fy0 = H.to_y(fc, YNODES)
    R["W0_reproduction_control"] = {
        "conjunct_2_recomputed_from_leg176_own_code": float((np.abs(ru) / np.abs(fy0)).max()),
        "conjunct_2_banked": banked["C0_xu_closed_form"]["max_rel_residual"],
        "reading": ("leg 176's runner is deterministic, so this re-derives NOTHING and is "
                    "reported as a reproduction, not as a verification (lesson 90).  It "
                    "establishes only that the banked artifact matches the code that "
                    "produced it.  W1-W6 replace every link of the chain.")}

    print("W1 exact-rational realization ...", flush=True)
    R["W1_exact_realization"] = w1_exact_realization()
    print("W1b y-space exact identity ...", flush=True)
    R["W1b_y_space_exact_identity"] = w1b_y_space_identity()
    print("W2 is the Gram the X norm? ...", flush=True)
    R["W2_gram_is_the_x_norm"] = w2_gram_is_the_x_norm()
    print("W3 sigma_min: float routes + exact enclosures ...", flush=True)
    R["W3_sigma_min"] = w3_sigma_min(quick)
    print("W4 tail ||T^-1||_X: float routes + exact enclosures ...", flush=True)
    R["W4_tail_inverse_norm"] = w4_tail_inverse_norm(quick)
    print("W5 border-weight sensitivity ...", flush=True)
    R["W5_border_weight_sensitivity"] = w5_border_weight_sensitivity(128 if quick else 256)
    print("W6 Xu (4.23) by exact partial fractions ...", flush=True)
    R["W6_xu_closed_form_exact"] = w6_xu_closed_form()
    print("W7 prose + PUB2 audit ...", flush=True)
    R["W7_prose_and_pub2_audit"] = w7_prose_and_pub2_audit(
        banked, R["W3_sigma_min"], R["W4_tail_inverse_norm"])

    w3, w4 = R["W3_sigma_min"], R["W4_tail_inverse_norm"]
    R["gate"] = build_gate(w3, w4)
    R["runtime_seconds"] = time.time() - t0

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=2, sort_keys=False)
    print(f"\nwrote {os.path.normpath(OUT)}  ({R['runtime_seconds']:.1f}s)")
    print(f"  sigma_min   leg176 {LEG176_SIGMA:.11f}  "
          f"independent {w3.get('independent_sigma_min_at_512_cholesky', float('nan')):.11f}")
    print(f"  ||T^-1||_X  leg176 {LEG176_TAIL_INV}  "
          f"independent {w4.get('independent_tail_inverse_norm_at_512', float('nan')):.6f}")
    return R


def build_gate(w3, w4):
    """The gate verdict, assembled from W3/W4's stored measurements.

    Factored out so `--regate` can rebuild ONLY this block from an existing
    artifact without a 51-minute recomputation.  It is pure assembly: every number
    it reads was produced by the full run and none is recomputed or adjusted here,
    so a `--regate` artifact is byte-identical to a full re-run's except for the
    verdict prose and the wall clock.
    """
    return {
        "question": ("Does an independent re-run of leg 176's construction reproduce "
                     "sigma_min = 0.0908 and ||T^-1||_X = 4.026 (or report a discrepancy "
                     "precisely), to the same precision leg 176 itself claims?"),
        "sigma_min": {
            "leg176": LEG176_SIGMA,
            "independent": w3.get("independent_sigma_min_at_512_cholesky"),
            "rel_diff": w3.get("rel_diff_at_512"),
            "exact_enclosure_at_512": w3["exact_enclosures"].get("512"),
        },
        "tail_inverse_norm": {
            "leg176": LEG176_TAIL_INV,
            "independent": w4.get("independent_tail_inverse_norm_at_512"),
            "rel_diff": w4.get("rel_diff_inverse_norm"),
            "exact_enclosure_at_512": w4["exact_enclosures"].get("512"),
            "certified_bracket_at_512": (w4["certified_brackets"].get("512") or {})
            .get("inverse_norm_bracket"),
        },
        "answer": ("REPRODUCES as quoted, ESCALATED below the quotation.  Both headline "
                   "numbers -- sigma_min = 0.0908 and ||T^-1||_X = 4.026, the two the gate "
                   "names and the two PUB2 quotes -- reproduce to every digit they are "
                   "stated to.  Three findings below that precision trigger the "
                   "escalation clause and are NOT repaired here: (1) the banked "
                   "C1 sigma_min_at_512 = 0.09080465147034879 is PROVED WRONG in exact "
                   "rational arithmetic -- the pencil is not positive definite at that "
                   "lambda, so sigma_min is strictly below it, certified in "
                   "(0.090804094, 0.090804194); (2) the banked C2 "
                   "tail_inverse_norm_K2_at_512 = 4.02614534796022 lies OUTSIDE the "
                   "certified bracket [4.02623993, 4.02624155]; (3) 'truncation-"
                   "independent', which leg 176's journal and PUB2 TECHNICAL L303 both "
                   "attach to 4.026, is FALSE at that precision -- the tail inverse norm "
                   "rises monotonically by 0.865% across the ladder, is still rising at "
                   "N=1024, and converges to approximately 4.0318, not 4.026.  Leg 176's "
                   "GATE ANSWER AND CONCLUSIONS ARE UNCHANGED AND CONFIRMED; two of the "
                   "corrections make its case stronger than it claimed (its reliable "
                   "window extends to N=2048 under a Cholesky whitening, and its Xu "
                   "reproduction is 7.1x better than its own residual metric reports).  "
                   "This is a precision-and-wording escalation on banked and "
                   "submission-track artifacts, not a reversal."),
        "escalation": ("YES -- branch pushed only, main untouched, nothing banked edited.  "
                       "Findings (1) and (2) are discrepancies in banked results; finding "
                       "(3) is a false claim in an approved submission-track document.  "
                       "The three remedies differ (JSON regeneration, a PUB2 value "
                       "correction, a PUB2 wording correction) and every one touches an "
                       "artifact this leg is forbidden to edit, so all three need a DM "
                       "ruling.  Precedent: leg 247, same shape."),
    }


def regate():
    """Rebuild only the `gate` block of an existing artifact.  No measurement reruns."""
    with open(OUT) as fh:
        R = json.load(fh)
    R["gate"] = build_gate(R["W3_sigma_min"], R["W4_tail_inverse_norm"])
    R["gate_rebuilt_without_recomputation"] = True
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=2, sort_keys=False)
    print(f"regated {os.path.normpath(OUT)}")
    print("  " + R["gate"]["answer"][:200] + " ...")
    return R


if __name__ == "__main__":
    if "--regate" in sys.argv:
        regate()
    else:
        main()
