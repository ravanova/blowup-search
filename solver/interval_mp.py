"""Arbitrary-precision arithmetic for two named re-measurements (Route-APIA, leg 312).

SCOPE, STATED ONCE SO IT CANNOT DRIFT. This module is NOT a general-purpose
arbitrary-precision interval library. It is the minimum arithmetic two
pre-registered re-measurements need:

  (1) leg 178's `T2_egm | E_egm` weighted-energy coercivity gap at grading
      depth `n_grade = 96`, where the runner's own `contamination` diagnostic
      reads `3.1e+03` -- the innermost quadrature panel sits at `theta ~ 3e-31`
      and the order-`theta^3` cancellation that DEFINES the constrained trial
      space is below float64's ability to represent it
      (`solver/energy_coercivity.py::wes_form_matrices_constrained`).
  (2) leg 176's `sigma_min` ladder for the bordered origin-`H^2` certificate,
      whose `N = 1024` row RISES instead of continuing to fall, attributed to
      "the float floor of an X Gram whose entries reach ~1e12"
      (`solver/origin_h2_certificate.py::x_gram`, condition number ~ N^4).

Two different arithmetic shapes are needed because the two defects are
different in kind (lesson 75): (1) is catastrophic CANCELLATION in forming a
constrained basis pointwise -- fixed by evaluating the same closed-form
trigonometric expressions with more correct digits, which is exactly what
INTERVAL arithmetic is for, so Section 1 below is genuine rigorous
directed-rounded interval arithmetic, backed by `decimal.Decimal` in place of
float64 (the precedent named in the brief is `fractions.Fraction`, used
already by `solver/spectral_certificate.py`; `Decimal` is used here instead
because the quadrature nodes are transcendental (sin/cos/tan of irrational
angles) and have no exact rational value for `Fraction` to hold -- `Decimal`
is the other arbitrary-precision numeric type in the standard library, and
nothing here changes `requirements.txt`).

(2) is loss of RELATIVE accuracy in a densely ill-conditioned generalized
eigenvalue problem (condition number of the X Gram grows like `N^4`, reaching
~1.8e13 at `N = 1024` -- 13 of float64's 16 digits). No enclosure is built for
this: verified eigenvalue bounds (Rohn/Kashiwagi-style) are a research area of
their own (see `writeup/novelty/leg_312.md` Section 3) and are explicitly out
of scope. Section 2 below is HIGH-PRECISION, NOT RIGOROUS -- it recomputes the
SAME linear algebra with `decimal.Decimal` at 30+ working digits instead of
float64's 16, replacing the one demonstrably ill-conditioned step (computing a
Gram matrix's symmetric square root by dense eigendecomposition) with an
EXACT-STRUCTURE banded Cholesky factorization that never forms that square
root at all. This is flagged, not smoothed over: "high working precision" is
not "verified enclosure" (lesson 86 applied to this leg's own output).

Both sections exploit exact structure this repository's own modules already
establish: the quantities feeding both re-measurements (`x_gram`'s I + J^4,
`l0_plus`'s half-integer tridiagonal, `border_row`'s integer-valued row) are
EXACT in float64 up to the sizes used here (verified below, `_assert_exact`),
so converting them to `Decimal` loses nothing -- the arbitrary precision is
spent entirely on the arithmetic that follows, not on re-deriving the inputs.
"""

from __future__ import annotations

from decimal import Decimal, Context, ROUND_FLOOR, ROUND_CEILING, localcontext
import math

__all__ = [
    "MPInterval",
    "mp_add", "mp_sub", "mp_mul", "mp_div",
    "mp_isum", "mp_dot",
    "dsin", "dcos", "dtan_ratio",
    "mp_pi",
    "banded_cholesky",
    "banded_triangular_inverse",
    "banded_matmul",
    "assert_exact_as_decimal",
]


# ===========================================================================
# SECTION 0 -- shared precision plumbing
# ===========================================================================

def _floor_ctx(prec):
    return Context(prec=int(prec), rounding=ROUND_FLOOR)


def _ceil_ctx(prec):
    return Context(prec=int(prec), rounding=ROUND_CEILING)


def assert_exact_as_decimal(x):
    """Verify a float64 value is EXACTLY represented by `Decimal(x)`.

    Used at every point this module ingests a float from another solver
    module (`x_gram`, `l0_plus`, `border_row`, quadrature nodes): those
    modules' own docstrings claim exactness (integer or half-integer Gram
    entries; float64 quadrature nodes taken AS the discretization, not
    re-derived), and this converts the CLAIM into a check that runs every
    time, rather than trusting the docstring. Raises on failure.
    """
    d = Decimal(float(x))
    if float(d) != float(x):
        raise ValueError(f"Decimal({x!r}) round-trips to {float(d)!r}: not exact")
    return d


# ===========================================================================
# SECTION 1 -- rigorous arbitrary-precision INTERVAL arithmetic (leg 178)
# ===========================================================================
#
# Same construction as solver/interval.py, generalized from float64 (one-ulp
# outward push via np.nextafter, because IEEE-754/numpy exposes no directed
# rounding mode) to Decimal at any working precision (Decimal DOES expose
# directed rounding natively -- a Context with rounding=ROUND_FLOOR or
# ROUND_CEILING makes every operation performed under it correctly rounded
# toward that direction). `MPInterval.lo`/`.hi` are Decimal; every arithmetic
# op takes the working `prec` as an explicit argument (no global state), so
# two computations at different precisions cannot silently interact.

class MPInterval:
    """Rigorous [lo, hi] enclosure, Decimal-backed, arbitrary precision.

    Invariant: lo <= hi. Unlike `solver.interval.Interval` this is SCALAR
    (leg 178's re-measurement needs enclosures of individual quadrature-node
    trig values and small dot products, not whole-array broadcasting -- see
    the module docstring for why an array-shaped generalization is out of
    scope)."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi):
        lo = Decimal(lo)
        hi = Decimal(hi)
        if lo > hi:
            raise ValueError(f"MPInterval requires lo <= hi, got [{lo}, {hi}]")
        self.lo = lo
        self.hi = hi

    @classmethod
    def point(cls, x):
        d = Decimal(x)
        return cls(d, d)

    @classmethod
    def from_mid_rad(cls, mid, rad, prec):
        mid, rad = Decimal(mid), abs(Decimal(rad))
        lo = _floor_ctx(prec).subtract(mid, rad)
        hi = _ceil_ctx(prec).add(mid, rad)
        return cls(lo, hi)

    @property
    def mid(self):
        return (self.lo + self.hi) / 2

    @property
    def width(self):
        return self.hi - self.lo

    def contains(self, x):
        x = Decimal(x)
        return self.lo <= x <= self.hi

    def __repr__(self):
        return f"MPInterval([{self.lo}, {self.hi}], width={self.width:.3e})"

    @staticmethod
    def _coerce(x):
        return x if isinstance(x, MPInterval) else MPInterval.point(x)


def mp_add(a, b, prec):
    a, b = MPInterval._coerce(a), MPInterval._coerce(b)
    lo = _floor_ctx(prec).add(a.lo, b.lo)
    hi = _ceil_ctx(prec).add(a.hi, b.hi)
    return MPInterval(lo, hi)


def mp_sub(a, b, prec):
    a, b = MPInterval._coerce(a), MPInterval._coerce(b)
    lo = _floor_ctx(prec).subtract(a.lo, b.hi)
    hi = _ceil_ctx(prec).subtract(a.hi, b.lo)
    return MPInterval(lo, hi)


def mp_mul(a, b, prec):
    a, b = MPInterval._coerce(a), MPInterval._coerce(b)
    fc, cc = _floor_ctx(prec), _ceil_ctx(prec)
    lo_candidates = (fc.multiply(a.lo, b.lo), fc.multiply(a.lo, b.hi),
                      fc.multiply(a.hi, b.lo), fc.multiply(a.hi, b.hi))
    hi_candidates = (cc.multiply(a.lo, b.lo), cc.multiply(a.lo, b.hi),
                      cc.multiply(a.hi, b.lo), cc.multiply(a.hi, b.hi))
    return MPInterval(min(lo_candidates), max(hi_candidates))


def mp_reciprocal(a, prec):
    a = MPInterval._coerce(a)
    if a.lo <= 0 <= a.hi:
        raise ZeroDivisionError("mp_reciprocal: interval contains 0")
    fc, cc = _floor_ctx(prec), _ceil_ctx(prec)
    return MPInterval(fc.divide(Decimal(1), a.hi), cc.divide(Decimal(1), a.lo))


def mp_div(a, b, prec):
    return mp_mul(a, mp_reciprocal(b, prec), prec)


def mp_neg(a):
    a = MPInterval._coerce(a)
    return MPInterval(-a.hi, -a.lo)


def mp_isum(ivs, prec):
    """Rigorous sum of a list of MPInterval, outward-rounded at each step.

    Pairwise accumulation (not a closed-form gamma_m bound as in
    `solver.interval.isum`): the term counts this module runs (tens to a
    few hundred) make an O(m) Python loop cheap, and a step-by-step directed
    rounding is simpler to get right than re-deriving Decimal's own
    per-operation rounding guarantee into a closed-form bound."""
    acc = MPInterval.point(0)
    for x in ivs:
        acc = mp_add(acc, x, prec)
    return acc


def mp_dot(a_list, b_list, prec):
    return mp_isum([mp_mul(a, b, prec) for a, b in zip(a_list, b_list)], prec)


# ---------------------------------------------------------------------------
# rigorous transcendentals: sin, cos (no range reduction needed)
# ---------------------------------------------------------------------------
# theta lives in (0, pi) throughout this leg's application (graded_quadrature
# domain), and the alternating Taylor series for sin/cos around 0 already
# converges comfortably over the WHOLE of [0, pi] without range reduction:
# the ratio of successive terms is theta/((2k)(2k+1)) <= pi/6 < 1 once k >= 1,
# so the series is alternating with strictly decreasing terms from the start,
# and the classic alternating-series remainder bound (|error| <= first
# omitted term) applies directly. `nterms` is fixed generously (not adaptive)
# because the cost of a few unnecessary terms is negligible next to the
# complexity an adaptive stopping rule would add; `_TERMS_MARGIN` sizes it
# from the requested precision so a caller asking for more digits gets more
# terms automatically.

def _series_terms_for(prec):
    """How many Taylor terms make the alternating remainder < 10^-prec for
    |theta| <= pi. Solved once, generously: term_n ~ pi^n / n!, and Stirling
    puts n! comfortably ahead of pi^n by n ~ 3*prec + 20 for any prec used in
    this module (checked up to prec=200 by `test_interval_mp.py`)."""
    return 3 * int(prec) + 30


def dsin(theta, prec):
    """Rigorous MPInterval enclosure of sin(theta) for a Decimal point theta,
    |theta| <= pi, via the alternating Taylor series with a proved remainder."""
    return _sin_cos_series(theta, prec, want_sin=True)


def dcos(theta, prec):
    """Rigorous MPInterval enclosure of cos(theta) for a Decimal point theta,
    |theta| <= pi, via the alternating Taylor series with a proved remainder."""
    return _sin_cos_series(theta, prec, want_sin=False)


def _sin_cos_series(theta, prec, want_sin):
    theta = Decimal(theta)
    if abs(theta) > Decimal("3.15"):
        raise ValueError("dsin/dcos: |theta| > pi + slack, outside the proved range")
    work = prec + 20   # guard digits for the internal accumulation
    n = _series_terms_for(prec)
    fc, cc = _floor_ctx(work), _ceil_ctx(work)
    theta2 = fc.multiply(theta, theta)  # sign doesn't matter, theta^2 >= 0 either way
    # term_k for sin: (-1)^k theta^(2k+1)/(2k+1)!  starting k=0 => theta
    # term_k for cos: (-1)^k theta^(2k)/(2k)!      starting k=0 => 1
    acc = MPInterval.point(1) if not want_sin else MPInterval.point(theta)
    term = MPInterval.point(1) if not want_sin else MPInterval.point(theta)
    start = 0 if want_sin else 1
    for k in range(1, n + 1):
        # term_k = term_{k-1} * (-theta^2) / ((2k)(2k-1))  [cos]  or
        #          term_{k-1} * (-theta^2) / ((2k)(2k+1))  [sin]
        denom = (2 * k) * (2 * k - 1) if not want_sin else (2 * k) * (2 * k + 1)
        num = mp_mul(term, MPInterval.point(-theta2), work)
        term = mp_div(num, MPInterval.point(Decimal(denom)), work)
        acc = mp_add(acc, term, work)
    # remainder: alternating, decreasing (true once k >= 1 for |theta|<=pi),
    # so |error| <= |first omitted term|'s magnitude. Bound term's own width-
    # inflated magnitude from above and widen both endpoints by it.
    rem = max(abs(term.lo), abs(term.hi))
    rem = cc.add(rem, Decimal(0))  # re-round into the guard context, defensive
    lo = fc.subtract(acc.lo, rem)
    hi = cc.add(acc.hi, rem)
    # round down to the CALLER's requested precision at the very end (widen
    # by one more ulp at that coarser precision so the guard-digit rounding
    # above cannot have been silently truncated inward)
    out_fc, out_cc = _floor_ctx(prec), _ceil_ctx(prec)
    lo2 = out_fc.plus(lo)
    hi2 = out_cc.plus(hi)
    return MPInterval(lo2, hi2)


def dtan_ratio(theta, prec):
    """MPInterval enclosure of tan(theta) = sin(theta)/cos(theta).

    Raises if the enclosure of cos(theta) straddles 0 (leg 178's `E_egm`
    weight is deliberately singular at theta -> pi via X = tan(theta/2), and
    the graded quadrature never places a node AT the endpoint, so this should
    not fire on live data; it is a guard, not expected to trip)."""
    s = dsin(theta, prec)
    c = dcos(theta, prec)
    return mp_div(s, c, prec)


def mp_pi(prec):
    """Rigorous MPInterval enclosure of pi via Machin's formula
    pi = 16 atan(1/5) - 4 atan(1/239), each atan by its alternating Taylor
    series (|x| < 1/5, converges fast, proved remainder = first omitted
    term -- same pattern as solver/interval.py's `_atanh_series`)."""
    work = prec + 20
    a5 = _atan_small(Decimal(1) / Decimal(5), work)
    a239 = _atan_small(Decimal(1) / Decimal(239), work)
    sixteen_a5 = mp_mul(MPInterval.point(16), a5, work)
    four_a239 = mp_mul(MPInterval.point(4), a239, work)
    pi_iv = mp_sub(sixteen_a5, four_a239, work)
    out_fc, out_cc = _floor_ctx(prec), _ceil_ctx(prec)
    return MPInterval(out_fc.plus(pi_iv.lo), out_cc.plus(pi_iv.hi))


def _atan_small(x, prec):
    """atan(x) = sum_{k>=0} (-1)^k x^(2k+1)/(2k+1), |x| < 1, alternating."""
    x = Decimal(x)
    fc, cc = _floor_ctx(prec), _ceil_ctx(prec)
    x2 = fc.multiply(x, x)
    n = _series_terms_for(prec) + 40  # x is small but be generous regardless
    acc = MPInterval.point(x)
    term = MPInterval.point(x)
    for k in range(1, n + 1):
        num = mp_mul(term, MPInterval.point(-x2), prec)
        term = mp_div(num, MPInterval.point(Decimal(2 * k + 1)), prec)
        acc = mp_add(acc, term, prec)
    rem = max(abs(term.lo), abs(term.hi))
    return MPInterval(fc.subtract(acc.lo, rem), cc.add(acc.hi, rem))


# ===========================================================================
# SECTION 2 -- high-precision (NOT interval-enclosed) banded linear algebra
#              for leg 176's ill-conditioned Gram square root
# ===========================================================================
#
# NOT RIGOROUS. Ordinary Decimal arithmetic at a fixed working precision
# `prec` (30+ guard digits above float64's 16), no directed rounding, no
# proved remainder. What makes this trustworthy for its one job is not
# interval enclosure but STRUCTURE: `x_gram`'s Gram matrix G = I + J^4 is
# EXACT (an integer matrix, `assert_exact_as_decimal` checked) and BANDED
# (bandwidth 4, since J is tridiagonal and matrix powers of a bandwidth-b
# matrix have bandwidth k*b). `solver/origin_h2_certificate.py`'s own
# `_sym_sqrt` instead runs a DENSE eigendecomposition of this banded matrix
# to build G^{1/2} and G^{-1/2} -- the eigenvectors of an ill-conditioned
# matrix (condition number ~ N^4, ~1.8e13 at N=1024) are themselves computed
# to only float64's 16 digits minus that condition number's exponent, i.e.
# ~3 correct digits, and BOTH square-root factors inherit that loss.
#
# A banded Cholesky factorization G = R^T R (R upper triangular, ALSO banded)
# needs no eigendecomposition and no square root of anything but individual
# POSITIVE diagonal pivots -- an intrinsically well-conditioned scalar
# operation regardless of the matrix's overall condition number. Doing that
# factorization (and the one dense-but-structured product it feeds) at 30+
# working digits instead of float64's 16 is the entire fix; nothing else in
# leg 176's pipeline needs to move off float64 (the FINAL svd, on the
# resulting matrix, is done in ordinary numpy once this module hands back a
# well-conditioned float64 array -- see experiments/p2_route_apia_v1.py).

def banded_cholesky(G, n, bw, prec):
    """Upper-triangular Cholesky factor R (R^T R = G) of a banded SPD matrix.

    `G` is a dense (n, n) sequence of Decimal (or float/int, coerced), only
    entries with |i-j| <= bw are read. Returns R as a dense (n, n) list of
    Decimal (zero outside the band). Standard "up-looking" banded Cholesky,
    O(n * bw^2)."""
    with localcontext(Context(prec=int(prec))):
        R = [[Decimal(0)] * n for _ in range(n)]
        for j in range(n):
            s = Decimal(G[j][j])
            lo = max(0, j - bw)
            for k in range(lo, j):
                s -= R[k][j] * R[k][j]
            if s <= 0:
                raise ValueError(f"banded_cholesky: pivot {j} is <= 0 ({s}); "
                                  "matrix is not positive definite at this precision")
            R[j][j] = s.sqrt()
            hi = min(n, j + bw + 1)
            for i in range(j + 1, hi):
                s2 = Decimal(G[j][i])
                for k in range(lo, j):
                    s2 -= R[k][j] * R[k][i]
                R[j][i] = s2 / R[j][j]
        return R


def banded_triangular_inverse(R, n, bw, prec):
    """Dense inverse of an upper-triangular banded matrix R (R @ Rinv = I).

    Column j of the inverse is obtained by back-substitution against e_j; for
    an upper-triangular R, that column is zero below the diagonal at row j+1..
    and possibly dense above it (rows 0..j), so this costs O(j * bw) for
    column j -- O(n^2 * bw) total, not O(n^3)."""
    with localcontext(Context(prec=int(prec))):
        Rinv = [[Decimal(0)] * n for _ in range(n)]
        for j in range(n):
            x = [Decimal(0)] * (j + 1)
            x[j] = Decimal(1) / R[j][j]
            for i in range(j - 1, -1, -1):
                hi = min(n, i + bw + 1)
                s = Decimal(0)
                for k in range(i + 1, min(hi, j + 1)):
                    s += R[i][k] * x[k]
                x[i] = -s / R[i][i]
            for i in range(j + 1):
                Rinv[i][j] = x[i]
        return Rinv


def banded_matmul(B, bw_lo, bw_hi, X, prec):
    """B @ X, exploiting that B is banded (nonzero only for j in
    [i - bw_lo, i + bw_hi]); X is a dense (n, m) list of Decimal.

    `B` is (n_out, n_in); returns dense (n_out, m). O(n_out * (bw_lo+bw_hi+1) * m)."""
    with localcontext(Context(prec=int(prec))):
        n_out = len(B)
        n_in = len(B[0]) if n_out else 0
        m = len(X[0]) if X else 0
        out = [[Decimal(0)] * m for _ in range(n_out)]
        for i in range(n_out):
            lo = max(0, i - bw_lo)
            hi = min(n_in, i + bw_hi + 1)
            row_out = out[i]
            for k in range(lo, hi):
                b_ik = B[i][k]
                if b_ik == 0:
                    continue
                xk = X[k]
                for j in range(m):
                    row_out[j] += b_ik * xk[j]
        return out
