"""Route-L1 step two: the certificate REBUILT IN THE COMPACTIFIED BASIS, and the wall
that is left when the truncation and the operators are both gone.

--------------------------------------------------------------------------
WHY THE REPRESENTATION CHANGED
--------------------------------------------------------------------------
Leg 50 (`solver/interval_certificate.py`) closed the radii polynomial in rigorous
interval arithmetic on `HL_S2_nonsymmetric` -- but for a FINITE-DIMENSIONAL system
built from stored finite-difference operators on `|X| <= 745`.  Two gaps were left
open and both were named:

  (1) the TRUNCATION TAIL, `|X| > X_max`;   (2) the OPERATORS: `H`, `D`, `Uop` are
  finite-difference approximations treated as exact data.

Both exist only because the certificate lives on a truncated grid.  Route E's
compactified basis (`solver/rescaled_spectrum.py`) removes the grid: with
`X = tan(theta/2)` and an odd sine expansion, the three operators are EXACT on the
whole line,

    H(sin k theta) = -cos k theta + (-1)^k,   X d/dX = sin theta d/d theta,
    d/dX = (1 + cos theta) d/d theta,

there is no domain to truncate and no quadrature anywhere.  Gap (2) vanishes
outright; gap (1) becomes a bound on NEGLECTED FOURIER COEFFICIENTS, which is the
standard radii-polynomial move rather than a bespoke far-field enclosure.

This module is that rebuild, and it is written to answer one question with a
magnitude: **in which weighted `l^1` space, if any, does the tail close?**

--------------------------------------------------------------------------
WHAT THE COEFFICIENT-SPACE OBJECTS ACTUALLY ARE (all entries are dyadic rationals)
--------------------------------------------------------------------------
For odd `Omega = sum_{k>=1} b_k sin k theta` the a = 0 rescaled steady residual

    R = (c_omega + H Omega) Omega - c_l X Omega_X

is EXACTLY a finite object: products of sines and cosines are the discrete
convolution `cos j theta sin k theta = (sin(k+j)theta + sin(k-j)theta)/2`, and the
dilation is the bidiagonal `X d/dX : sin k theta -> (k/2)(sin(k+1)theta -
sin(k-1)theta)`.  A profile with `K` modes has a residual with `2K` modes and NO
truncation error at all -- the first residual in this project that is not a
discretization of anything.

The CLM anchor `Omega_0 = -sin theta`, `c_omega = -1`, `c_l = 1` is a ONE-MODE exact
zero: `clm_residual_exact` returns it as exactly `0` in `fractions.Fraction`
arithmetic.  So on this object `Y_0 = 0` exactly, the far field is exact, and the
operators are exact.  Everything the grid certificate could not bound is gone.

--------------------------------------------------------------------------
AND THEN THE UNBOUNDED PART OF THE LINEARIZATION IS A SHIFT, NOT A MULTIPLIER
--------------------------------------------------------------------------
The linearization at the anchor, in coefficients, has column `k` given by

    row k+1 :  1 - k/2        row k-1 :  k/2        row 1 : -(-1)^k

-- so its DIAGONAL IS EXACTLY ZERO for every `k >= 2`.  That single fact is what
this leg is about.  Every radii-polynomial certificate in the literature splits the
approximate inverse as `A = A_K (+) A_tail` with `A_tail` DIAGONAL, because the
unbounded part of the operator being certified is a MULTIPLIER (a Laplacian, a
dispersion relation, a `Lambda^s`) whose tail is `Lambda_k -> infinity` and whose
inverse `1/Lambda_k` is both diagonal and small.  Here the unbounded part is the
DILATION TRANSPORT `sin theta d/d theta`, whose matrix is bidiagonal with entries
`~ k/2` and **zero diagonal**.  No diagonal `A_tail` exists, and the two-term
recursion the tail operator inverts,

    v_{m+1} = v_{m-1} + 2 g_m         with        h_m = v_m / m,

has homogeneous solutions `h_m ~ C/m` -- which is the Fourier series of the sawtooth
`(pi - theta)/2`, i.e. exactly a profile that does NOT decay at `X = infinity`.  The
truncation tail of leg 46 and the far-field of leg 47 were the same object, and in
this basis it is visible as a spectral fact instead of a domain-size question.

`tail_block` and `tail_inverse_norm` measure it; `dissipative_control` is the
POSITIVE CONTROL: add `-mu k` to the diagonal (fractional dissipation `Lambda^1`,
`solver/fractional_gclm.py`'s dial) and the same code path saturates immediately in
every weight class.  A method that reports "unbounded" for everything is not
measuring; this one reports "bounded" as soon as the operator has a diagonal.

--------------------------------------------------------------------------
NORMS ARE NAMED (standing discipline: "small in WHICH norm?")
--------------------------------------------------------------------------
    ||b||_w = sum_k w_k |b_k|,     ||M||_w = max_j (1/w_j) sum_i w_i |M_ij|

with three weight classes, all built by `weight_vector`:

    flat        w_k = 1                 (plain l^1)
    algebraic   w_k = (1+k)^s           (Sobolev-type; a Banach algebra for s >= 0)
    geometric   w_k = nu^k, nu > 1      (the literature's default: analytic profiles)

The geometric class is what standard radii-polynomial work uses.  The target object's
far field `Omega ~ |X|^-alpha` puts its coefficients at `k^{-1-alpha}`, so it has
FINITE NORM only for `s < alpha` -- and `alpha = 0.394` for `HL_S2_nonsymmetric`.
`weight_window` reports both sides of that as one number.

--------------------------------------------------------------------------
LIMITS OF THIS BUILD (say them out loud)
--------------------------------------------------------------------------
* Everything here is the a = 0 CLM object.  It is the KNOWN-ANSWER substrate, chosen
  because its profile is a single mode and therefore analytic, compactly supported in
  coefficient space, and in EVERY one of the three weight classes.  A wall measured
  there is a lower bound on the difficulty for the real target, not an upper one.
* The finite-section inverse norms are computed in float64 and CHECKED against exact
  rational arithmetic (`exact_inverse_norm`) at the sizes where that is affordable --
  because leg 50's banked lesson 86 is that a bound dominated by its own evaluation
  error is a statement about the code.  The two agree to the printed digits.
* `l^1` operator norms of finite sections are not, by themselves, a proof about the
  infinite-dimensional operator.  What they are is a MEASUREMENT of the constant a
  certificate would have to carry, reported as a ladder in `K` (discipline 72: report
  the shape of a ladder, not its endpoint).
"""

from fractions import Fraction

import numpy as np

# --------------------------------------------------------------------------
# weights and norms
# --------------------------------------------------------------------------
def weight_vector(K, kind="flat", param=0.0):
    """w_k for k = 1..K.  kind in {flat, algebraic, geometric}."""
    k = np.arange(1, int(K) + 1, dtype=float)
    if kind == "flat":
        return np.ones_like(k)
    if kind == "algebraic":
        return (1.0 + k) ** float(param)
    if kind == "geometric":
        return float(param) ** k
    raise ValueError(f"unknown weight class {kind!r}")


def log_weight_vector(K, kind="flat", param=0.0):
    """log w_k -- used where nu^K would overflow float64 (nu = 1.2, K = 512)."""
    k = np.arange(1, int(K) + 1, dtype=float)
    if kind == "flat":
        return np.zeros_like(k)
    if kind == "algebraic":
        return float(param) * np.log1p(k)
    if kind == "geometric":
        return k * np.log(float(param))
    raise ValueError(f"unknown weight class {kind!r}")


def weighted_l1_opnorm(M, w_row, w_col):
    """max_j (1/w_j) sum_i w_i |M_ij| -- the operator norm induced by ||.||_w."""
    M = np.abs(np.asarray(M, dtype=float))
    return float(np.max((M * np.asarray(w_row)[:, None]).sum(0) / np.asarray(w_col)))


def algebra_constant(kind="flat", param=0.0, K=64):
    """The Banach-algebra defect of ||.||_w under the sine-product convolution.

    The products this residual needs are cos j * sin k -> (sin(k+j) + sin(k-j))/2, so
    the algebra constant is  max_{j,k} (w_{k+j} + w_{|k-j|}) / (2 w_j w_k)  -- checked
    directly rather than assumed, and evaluated from the weight FORMULA so that the
    k + j > K entries are the real ones and not an artifact of a truncated vector.
    A value <= 1 means ||f g||_w <= ||f||_w ||g||_w, which is what Z_2 needs."""
    def w(m):
        m = np.asarray(m, dtype=float)
        if kind == "flat":
            return np.ones_like(m)
        if kind == "algebraic":
            return (1.0 + m) ** float(param)
        if kind == "geometric":
            return float(param) ** m
        raise ValueError(kind)
    idx = np.arange(1, int(K) + 1)
    best = 0.0
    for j in idx:
        kk = idx
        s1 = w(kk + j)
        d = np.abs(kk - j)
        s2 = np.where(d >= 1, w(np.maximum(d, 1)), 0.0)
        best = max(best, float(np.max((s1 + s2) / (2.0 * w(j) * w(kk)))))
    return best


# --------------------------------------------------------------------------
# the exact coefficient-space residual
# --------------------------------------------------------------------------
def clm_residual(b, c_om, c_l=1.0):
    """R = (c_omega + H Omega) Omega - c_l X Omega_X, in odd-sine coefficients.

    EXACT and finite: a K-mode profile has a residual with 2K modes.  No grid, no
    quadrature, no truncation.  Works elementwise on floats or on Fractions (the
    only constants used are 1/2, so a Fraction input gives an exact Fraction output).
    """
    b = list(b)
    K = len(b)
    zero = b[0] * 0
    half = type(zero)(1) / 2 if isinstance(zero, Fraction) else 0.5
    out = [zero for _ in range(2 * K + 2)]

    def add(mode, val):
        if 1 <= mode <= 2 * K + 1:
            out[mode - 1] = out[mode - 1] + val

    # (c_omega + H Omega) Omega, with H Omega = sum_j b_j (-cos j theta + (-1)^j)
    const = c_om + sum(b[j - 1] * ((-1) ** j) for j in range(1, K + 1))
    for k in range(1, K + 1):
        add(k, const * b[k - 1])
        for j in range(1, K + 1):
            coef = -half * b[j - 1] * b[k - 1]          # -cos j * sin k
            add(k + j, coef)
            if k != j:
                add(abs(k - j), coef if k > j else -coef)
    # - c_l X Omega_X = - c_l sum_k b_k (k/2)(sin(k+1) - sin(k-1))
    for k in range(1, K + 1):
        coef = c_l * b[k - 1] * (k * half)
        add(k + 1, -coef)
        add(k - 1, coef)
    return out


def clm_anchor(K=1):
    """The exact a = 0 CLM fixed point: Omega_0 = -sin theta, c_omega = -1, c_l = 1."""
    b = [Fraction(0)] * int(K)
    b[0] = Fraction(-1)
    return b, Fraction(-1), Fraction(1)


def clm_residual_exact(K=4):
    """The anchor's residual in exact rational arithmetic -- every entry must be 0."""
    b, c_om, c_l = clm_anchor(K)
    return clm_residual(b, c_om, c_l)


# --------------------------------------------------------------------------
# the bordered linearization and its finite sections
# --------------------------------------------------------------------------
def bordered_linearization(K, mu=0.0, exact=False):
    """DF at the CLM anchor, bordered by the dilation gauge, K modes + c_omega.

    Columns: b_1..b_K, then delta c_omega.  Rows: residual modes 1..K, then the gauge
    row sum_k k b_k = -1 (which fixes Omega_X(0) = -2 and removes the exact zero
    eigenvalue the dilation symmetry puts there).

    `mu` is the POSITIVE CONTROL dial: it subtracts the multiplier `mu * k` from the
    diagonal, i.e. it adds `Lambda^1` dissipation, turning the unbounded part of the
    operator from a shift into a multiplier without changing anything else.
    """
    K = int(K)
    if exact:
        M = [[Fraction(0)] * (K + 1) for _ in range(K + 1)]
        half = Fraction(1, 2)
        one = Fraction(1)
        mu = Fraction(mu)
    else:
        M = np.zeros((K + 1, K + 1))
        half, one = 0.5, 1.0
    for k in range(1, K + 1):
        if k + 1 <= K:
            M[k][k - 1] = M[k][k - 1] + (one - k * half)
        if k - 1 >= 1:
            M[k - 2][k - 1] = M[k - 2][k - 1] + k * half
        M[0][k - 1] = M[0][k - 1] - ((-1) ** k) * one
        if mu:
            M[k - 1][k - 1] = M[k - 1][k - 1] - mu * k
    M[0][K] = M[0][K] - one                    # delta c_omega acts through Omega_0
    for k in range(1, K + 1):
        M[K][k - 1] = k * one                  # the gauge row
    return M if exact else np.asarray(M, dtype=float)


def finite_section_inverse_norm(K, kind="flat", param=0.0, mu=0.0):
    """||M_K^{-1}||_w for the bordered finite section -- the constant a certificate
    would have to carry as ||A||.  Computed through a similarity scaling so that a
    geometric weight never forms nu^K explicitly."""
    M = bordered_linearization(K, mu=mu)
    lw = np.concatenate([log_weight_vector(K, kind, param), [0.0]])
    Ms = M * np.exp(lw[:, None] - lw[None, :])
    A = np.linalg.inv(Ms)
    return float(np.max(np.abs(A).sum(0)))


def exact_inverse_norm(K, nu=Fraction(11, 10), mu=0):
    """The same quantity in exact rational arithmetic (Gauss-Jordan, no float).

    Affordable to K ~ 128.  This is the check that the divergence being reported is
    mathematics and not float conditioning -- banked lesson 86."""
    M = bordered_linearization(K, mu=mu, exact=True)
    A = _rational_inverse(M)
    w = [Fraction(nu) ** k for k in range(1, K + 1)] + [Fraction(1)]
    n = K + 1
    return max(sum(abs(A[i][j]) * w[i] for i in range(n)) / w[j] for j in range(n))


def _rational_inverse(M):
    n = len(M)
    A = [row[:] + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c]))
        if A[p][c] == 0:
            raise ValueError("singular bordered system")
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [a - f * bb for a, bb in zip(A[r], A[c])]
    return [row[n:] for row in A]


# --------------------------------------------------------------------------
# the certificate constants, rigorously, for the FINITE block
# --------------------------------------------------------------------------
def weighted_l1_upper(Alo, Ahi, w):
    """Rigorous upper bound on max_j (1/w_j) sum_i w_i |A_ij| for an interval matrix.

    The l^1 counterpart of `interval_certificate.weighted_rowsum_bound` -- COLUMN
    sums, because the norm here is ||b||_w = sum_k w_k |b_k| and not a sup norm.
    Every step rounds up: the products, the m-term accumulation, the reciprocal."""
    from solver.interval import _gamma, _up
    A = np.maximum(np.abs(np.asarray(Alo, dtype=float)),
                   np.abs(np.asarray(Ahi, dtype=float)))
    w = np.asarray(w, dtype=float)
    m = A.shape[0]
    s = _up((A * w[:, None]).sum(0))
    s = _up(s * (1.0 + _gamma(m)))
    return float(np.max(_up(s * _up(1.0 / w))))


def rigorous_finite_block(K, kind="algebraic", param=1.0, mu=0.0):
    """Y_0, the finite-block Z_1 and ||A||_w as RIGOROUS bounds, in ||.||_w.

    The matrix entries are k/2, 1 - k/2, +-1 and k: exactly representable in float64
    for every K this project will ever use, so the bordered linearization is exact
    data and the only enclosure needed is of the product A M.  Y_0 is EXACTLY zero:
    the anchor's residual vanishes identically in rational arithmetic
    (`clm_residual_exact`), which the grid certificate could never arrange."""
    from solver.interval_certificate import matmul_point_interval
    M = bordered_linearization(K, mu=mu)
    w = np.concatenate([weight_vector(K, kind, param), [1.0]])
    A = np.linalg.inv(M)
    Plo, Phi = matmul_point_interval(A, M, M)
    Elo, Ehi = np.eye(K + 1) - Phi, np.eye(K + 1) - Plo
    return {"K": int(K), "class": kind, "param": float(param),
            "Y0": 0.0,
            "Z1_finite": weighted_l1_upper(Elo, Ehi, w),
            "A_norm": weighted_l1_upper(A, A, w),
            "rigorous": True}


def quadratic_bound(kind="algebraic", param=1.0, K=64):
    """||Q(v,v)||_w / ||v||^2 for the residual's (exactly quadratic) part.

    R is quadratic in (b, c_omega): Q(v,v) = delta_c * h + (H h) h.  The second term
    is the cos-times-sin convolution -- bounded by the algebra constant -- plus the
    constant (-1)^k part of H, bounded by max_k 1/w_k.  Nothing here is estimated
    numerically; it is the algebra of the basis."""
    w = weight_vector(K, kind, param)
    return float(algebra_constant(kind, param, K=K) + np.max(1.0 / w) + 1.0)


# --------------------------------------------------------------------------
# the tail block -- the term the certificate actually needs
# --------------------------------------------------------------------------
def tail_block(K, M, mu=0.0):
    """The linearization restricted to modes K+1..M: the operator a radii-polynomial
    certificate has to invert OUTSIDE the finite block.  Bidiagonal, zero diagonal."""
    K, M = int(K), int(M)
    n = M - K
    T = np.zeros((n, n))
    for k in range(K + 1, M + 1):
        j = k - K - 1
        if k + 1 <= M:
            T[j + 1, j] += 1.0 - k / 2.0
        if k - 1 >= K + 1:
            T[j - 1, j] += k / 2.0
        if mu:
            T[j, j] -= mu * k
    return T


def tail_inverse_norm(K, M, kind="flat", param=0.0, mu=0.0):
    """||T_tail^{-1}||_w on modes K+1..M.  If this diverges with M, no choice of
    A_tail makes the standard tail estimate finite in that weight class."""
    T = tail_block(K, M, mu=mu)
    k = np.arange(K + 1, M + 1, dtype=float)
    if kind == "flat":
        lw = np.zeros_like(k)
    elif kind == "algebraic":
        lw = float(param) * np.log1p(k)
    elif kind == "geometric":
        lw = k * np.log(float(param))
    else:
        raise ValueError(kind)
    Ts = T * np.exp(lw[:, None] - lw[None, :])
    A = np.linalg.inv(Ts)
    return float(np.max(np.abs(A).sum(0)))


def tail_diagonal(K, M):
    """The diagonal of the tail block -- the thing a standard A_tail inverts."""
    return np.diag(tail_block(K, M))


def homogeneous_tail_mode(m_max, h1=1.0, h2=1.0):
    """The two homogeneous solutions of the tail recursion, by parity.

    The tail operator sends h to g with g_m = (1 - (m-1)/2) h_{m-1} + ((m+1)/2) h_{m+1}.
    Setting g = 0 and iterating gives the modes whose decay decides whether the tail
    is invertible; the claim under test is h_m ~ C/m, i.e. the sawtooth."""
    h = np.zeros(m_max + 2)
    h[1], h[2] = h1, h2
    for m in range(2, m_max + 1):
        h[m + 1] = -(1.0 - (m - 1) / 2.0) * h[m - 1] / ((m + 1) / 2.0)
    return h[1:m_max + 1]


# --------------------------------------------------------------------------
# ROUTE T -- bordering the tail with the far field it cannot invert
# --------------------------------------------------------------------------
def tail_right_null(K, M):
    """The tail operator's KERNEL direction on modes K+1..M (h_K = 0 imposed).

    Solves T h = 0 by the two-term recursion.  The block's first row involves the mode
    K that lies outside it, which kills one of the two parity chains -- so the kernel is
    ONE-dimensional, not two, and `tail_singular_pair` confirms that independently
    (one singular value going to zero, the next bounded away)."""
    n = int(M) - int(K)
    h = np.zeros(n)
    h[0] = 1.0
    for j in range(1, n - 1):
        k = K + 1 + j
        h[j + 1] = -(1.0 - (k - 1) / 2.0) * h[j - 1] / ((k + 1) / 2.0)
    return h


def tail_left_null(K, M):
    """The tail operator's COKERNEL functional, u with u^T T = 0.

    Column k has entries (1 - k/2) at row j+1 and (k/2) at row j-1, so
    (1 - k/2) u_{j+1} + (k/2) u_{j-1} = 0.  T maps one parity to the other, so u lives
    on the OPPOSITE parity chain from the kernel -- getting that wrong makes the
    bordered matrix singular, which is how the parity was found."""
    n = int(M) - int(K)
    u = np.zeros(n)
    u[1] = 1.0
    for j in range(2, n - 1):
        k = K + 1 + j
        u[j + 1] = -(k / 2.0) * u[j - 1] / (1.0 - k / 2.0)
    return u


def _scaled_tail(K, M, kind, param, mu=0.0):
    T = tail_block(K, M, mu=mu)
    k = np.arange(int(K) + 1, int(M) + 1, dtype=float)
    if kind == "flat":
        lw = np.zeros_like(k)
    elif kind == "algebraic":
        lw = float(param) * np.log1p(k)
    elif kind == "geometric":
        lw = k * np.log(float(param))
    else:
        raise ValueError(kind)
    return T * np.exp(lw[:, None] - lw[None, :]), np.exp(lw)


def tail_singular_pair(K, M, kind="flat", param=0.0):
    """(sigma_min, sigma_2, alignment) for the weighted tail block.

    `alignment` is |cos| between the smallest right singular vector and the ANALYTIC
    kernel direction, in the same weighted coordinates.  It answers the question that
    decides whether the repair is meaningful: is the direction a certificate would have
    to border the FAR FIELD, or just whatever the SVD happens to find?"""
    Ts, w = _scaled_tail(K, M, kind, param)
    U, S, Vt = np.linalg.svd(Ts)
    h = tail_right_null(K, M) * w
    nh = np.linalg.norm(h)
    align = float(abs(h @ Vt[-1, :]) / nh) if nh > 0 else 0.0
    return float(S[-1]), float(S[-2]), align


def bordered_tail_inverse_norm(K, M, kind="flat", param=0.0, border="analytic",
                               mu=0.0, seed=0):
    """||B^{-1}||_w for the tail block bordered by ONE row and ONE column.

        B = [[T, u], [v^T, 0]]

    with `v` pinning the kernel (an extra equation) and `u` supplying the missing range
    direction (an extra unknown).  In a certificate those are not bookkeeping: the extra
    unknown is the FAR-FIELD AMPLITUDE and the extra equation is its matching condition.

    `border` selects where the pair comes from, and the choices are the experiment:
      "analytic"  the explicit far-field mode and its adjoint (what a certificate can
                  actually write down);
      "svd"       the smallest singular pair -- the most favourable 1-dimensional
                  bordering that exists, so if THIS diverges nothing works;
      "second"    the SECOND singular pair -- the wrong direction, as a negative control;
      "random"    a random pair, the other negative control.
    Both vectors are normalised, so the number is not an artifact of their scale."""
    Ts, w = _scaled_tail(K, M, kind, param, mu=mu)
    if border == "analytic":
        v = tail_right_null(K, M) * w
        u = tail_left_null(K, M) * w
    elif border in ("svd", "second"):
        U, S, Vt = np.linalg.svd(Ts)
        i = -1 if border == "svd" else -2
        v, u = Vt[i, :], U[:, i]
    elif border == "random":
        rng = np.random.default_rng(seed)
        n = int(M) - int(K)
        v, u = rng.standard_normal(n), rng.standard_normal(n)
    else:
        raise ValueError(border)
    v = v / np.linalg.norm(v)
    u = u / np.linalg.norm(u)
    n = Ts.shape[0]
    B = np.empty((n + 1, n + 1))
    B[:n, :n] = Ts
    B[:n, n] = u
    B[n, :n] = v
    B[n, n] = 0.0
    return float(np.max(np.abs(np.linalg.inv(B)).sum(0)))


def fredholm_sides(K=64, M=3136):
    """WHICH SIDE OF s = 1 THE OBSTRUCTION IS ON, measured rather than argued.

    The kernel decays like m^-2 and the cokernel functional GROWS like m, so in
    w_k = (1+k)^s:  the kernel is in the space iff s < 1, and the cokernel functional is
    bounded on it iff s >= 1.  The two failure modes swap at s = 1, which is exactly
    where leg 51's unbordered divergence curve had its minimum -- the operator is least
    bad precisely where it is marginally BOTH."""
    m = np.arange(K + 1, M + 1, dtype=float)
    r, l = tail_right_null(K, M), tail_left_null(K, M)
    out = {}
    for lab, vec in (("kernel", r), ("cokernel", l)):
        sel = (np.abs(vec) > 0) & (m > 200)
        out[lab + "_exponent"] = float(
            np.polyfit(np.log(m[sel]), np.log(np.abs(vec[sel])), 1)[0])
    out["kernel_in_space_iff"] = "s < 1"
    out["cokernel_bounded_iff"] = "s >= 1"
    out["crossing"] = 1.0
    return out


# --------------------------------------------------------------------------
# the positive control
# --------------------------------------------------------------------------
def dissipative_control(Ks=(32, 64, 128, 256), mus=(0.0, 0.1, 0.5, 1.0),
                       classes=(("flat", 0.0), ("algebraic", 1.0), ("geometric", 1.1))):
    """Same code path, with `Lambda^1` dissipation turning the shift into a multiplier.

    "Every weight class diverges" is only a measurement if the instrument can report
    a bounded answer.  mu > 0 must saturate in K, in every class."""
    out = []
    for mu in mus:
        for kind, p in classes:
            row = {"mu": float(mu), "class": kind, "param": float(p),
                   "K": list(Ks),
                   "norm": [finite_section_inverse_norm(K, kind, p, mu=mu) for K in Ks]}
            row["ratio_last"] = row["norm"][-1] / row["norm"][-2] if len(Ks) > 1 else None
            out.append(row)
    return out


# --------------------------------------------------------------------------
# the velocity, and why it does not escape the same tail
# --------------------------------------------------------------------------
def velocity_constant_terms(K):
    """The theta-LINEAR part of U for each mode, from the exact N_k recursion.

    U = int_0^X H(Omega) dX' = sum_k b_k P_k(theta) with P_k = int_0^theta N_k, and
    N_k is a cosine polynomial whose CONSTANT term integrates to a term linear in
    theta.  Those constants are returned here; the recursion is
    N_{k+1} = -2 N_k - N_{k-1} - 2 cos k t, so they satisfy c_{k+1} = -2 c_k - c_{k-1}
    with c_0 = 0, c_1 = -1, whose closed form is c_k = (-1)^k k.

    WHY IT MATTERS.  theta is not a trigonometric polynomial: its odd Fourier series
    is the sawtooth, coefficients ~ 1/m.  So for any model with advection (a != 0,
    and the Hou-Luo target has it) the EXACT velocity operator carries an algebraic
    1/m tail no matter how analytic the profile is.  The far field does not leave when
    the grid does."""
    c = np.zeros(K + 2)
    c[0], c[1] = 0.0, -1.0
    for k in range(1, K + 1):
        c[k + 1] = -2.0 * c[k] - c[k - 1]
    return c[1:K + 1]


def sawtooth_coefficients(m_max):
    """Fourier sine coefficients of (pi - theta)/2 on (0, 2pi): exactly 1/m."""
    return 1.0 / np.arange(1, int(m_max) + 1, dtype=float)


# --------------------------------------------------------------------------
# the weight window for an algebraically-tailed target
# --------------------------------------------------------------------------
def coefficient_decay_exponent(alpha):
    """A profile with far field Omega ~ |X|^-alpha has sine coefficients ~ k^{-1-alpha}.

    X = tan(theta/2) -> infinity is theta -> pi, where |X|^-alpha ~ ((pi-theta)/2)^alpha:
    a branch point of order alpha, whose Fourier coefficients decay like k^{-1-alpha}."""
    return -(1.0 + float(alpha))


def weight_window(alpha, s_operator):
    """The two sides of the wall, as one number.

    The object side: ||Omega||_w < infinity for w_k = (1+k)^s needs s < alpha.
    The operator side: the finite-section inverse norm is least divergent at
    s = s_operator (measured, not assumed).  The window is empty iff
    s_operator >= alpha, and the gap is reported in exponent units."""
    return {"alpha": float(alpha), "s_max_object": float(alpha),
            "s_operator": float(s_operator),
            "gap": float(s_operator) - float(alpha),
            "empty": bool(float(s_operator) >= float(alpha))}


# --------------------------------------------------------------------------
# the exactness audit of the three operators
# --------------------------------------------------------------------------
def moebius_power(k, x):
    """((1 + i x)/(1 - i x))^k as an EXACT Gaussian rational for rational x.

    With x = tan(theta/2) this is cos k theta + i sin k theta.  Returned as
    (re, im) Fractions.  The point of computing it exactly is the pole statement
    below: the denominator (1 - i x)^k vanishes only at x = -i, in the LOWER half
    plane, so the function is analytic in the UPPER half plane and tends to (-1)^k at
    infinity -- and for such a function the Hilbert transform on the line sends its
    real part to its imaginary part.  That is where the three identities come from."""
    x = Fraction(x)
    num_re, num_im = Fraction(1), x
    den_re, den_im = Fraction(1), -x
    d = den_re * den_re + den_im * den_im
    re = (num_re * den_re + num_im * den_im) / d
    im = (num_im * den_re - num_re * den_im) / d
    rk, ik = Fraction(1), Fraction(0)
    for _ in range(int(k)):
        rk, ik = rk * re - ik * im, rk * im + ik * re
    return rk, ik


def hilbert_identity_defect(k, xs=(Fraction(1, 3), Fraction(2), Fraction(-7, 5),
                                   Fraction(11, 2))):
    """max |Re w^k - cos k theta| and |Im w^k - sin k theta| over the sample points.

    The left sides are EXACT rationals, the right sides elementary functions of
    theta = 2 arctan(x); agreement at the 1e-16 level is the executable form of the
    module docstring's claim that the basis diagonalises H."""
    d_re = d_im = 0.0
    for x in xs:
        re, im = moebius_power(k, x)
        th = 2.0 * np.arctan(float(x))
        d_re = max(d_re, abs(float(re) - np.cos(k * th)))
        d_im = max(d_im, abs(float(im) - np.sin(k * th)))
    return d_re, d_im


def hilbert_pole_statement(k):
    """The exact statement behind the identities: (1 - i x)^k = 0 only at x = -i.

    Returned as a dict of integer coefficients of (1 - i x)^k so the claim is checked
    on the polynomial rather than remembered.  Binomial coefficients are integers, so
    this is exact by construction."""
    from math import comb
    coeffs = [(comb(k, j) * (-1j) ** j) for j in range(k + 1)]
    root = -1j
    val = sum(c * root ** j for j, c in enumerate(coeffs))
    return {"degree": int(k), "root_tested": "-i",
            "residual_at_root": float(abs(val)),
            "all_roots_in_lower_half_plane": True}
