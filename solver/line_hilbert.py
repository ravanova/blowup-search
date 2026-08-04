"""Whole-line Hilbert transform on a NON-uniform grid (spline-analytic).

This is the crux component for Phase-2 Spike 0 (dynamic self-similar rescaling
of the 1D gCLM model). The rescaled CLM profile Omega_0(X) = -4X/(1+4X^2) is a
whole-line, ~1/X-decaying function; its Hilbert transform must be computed on a
stretched (non-uniform) mesh reaching large |X|, so the periodic-FFT multiplier
`H(e^{ikx}) = -i sign(k)` in `spectral_utils.py` does NOT apply here (the tail is
too slow — a periodic H converges to the WRONG profile, see PHASE2_SPIKE0_NOTES).

Convention. The line Hilbert transform is the principal value

    H(f)(x) = (1/pi) p.v. integral  f(y) / (x - y) dy.

Under this convention the ready-made unit test is the pair

    f(X)  = -4X / (1 + 4X^2)   -->   H(f)(X) = 2 / (1 + 4X^2)

(the exact CLM self-similar profile and its transform, arXiv:2603.25104).

Method (Appendix C.1 of Huang-Tong-Wang, arXiv:2603.25104). Represent f on
[-M, M] by a cubic spline in the C^1_0 Hermite basis {P_i, Q_i} whose Hilbert
transforms are BOUNDED and known in closed form:

    P_i : value hat  (P_i(x_j) = delta_ij,  P_i'(x_j) = 0)
    Q_i : slope hat  (Q_i(x_j) = 0,         Q_i'(x_j) = delta_ij)

    H(P_i)(x) = A(l) - A(r)
    H(Q_i)(x) = (x_{i-1}-x_i) B(l) - (x_{i+1}-x_i) B(r)
        l = (x_{i-1}-x_i)/(x-x_i),   r = (x_{i+1}-x_i)/(x-x_i)

    A(s) = [-5s^3 - 12s^2 + 12s + 6(s^3-3s+2) ln|1-s|] / (6 pi s^3)
    B(s) = [ 2s^3 -  9s^2 +  6s + 6(s-1)^2   ln|1-s|] / (6 pi s^3)

with the diagonal (x = x_i) limits

    H(P_i)(x_i) = (1/pi) ln| (x_{i-1}-x_i)/(x_{i+1}-x_i) |
    H(Q_i)(x_i) = (x_{i-1}-x_{i+1}) / (3 pi).

Node slopes f'_i are the standard natural cubic spline (f''=0 at both ends).

Stability. As s -> 0 the numerators of A, B suffer catastrophic cancellation
(the ln term Taylor-cancels the polynomial to O(s^4)). We remove it analytically
using L(s) = ln|1-s| + s + s^2/2 + s^3/3 = -sum_{n>=4} s^n/n:

    A(s) = (s^3-3s+2) L(s)/(pi s^3) - (3s^2+2s^3)/(6 pi)
    B(s) = (s-1)^2   L(s)/(pi s^3) + (s   -2s^2)/(6 pi)

evaluated by a series for L when |s| < 0.5 (never near the s=1 log singularity),
and by the direct formula otherwise (no cancellation there; the s->1 product
(s-1)^2 ln|1-s| -> 0 is guarded). This reproduces the paper's Mathematica
minimax to machine precision without transcribing its 23-term coefficient list.
"""

import numpy as np

PI = np.pi


# --------------------------------------------------------------------------
# natural cubic spline node slopes on a non-uniform grid
# --------------------------------------------------------------------------

def natural_spline_slopes(x, f):
    """First derivatives f'_i of the natural cubic spline through (x_i, f_i).

    Natural BC: second derivative vanishes at both endpoints. Solves the
    standard tridiagonal system for the node second derivatives M_i, then
    reads off the slopes. O(N) Thomas algorithm; x may be non-uniform.

    `f` may be 1-D (shape (n,)) or a stack of independent right-hand sides
    (shape (n, k)); in the latter case every column is solved at once with the
    Thomas sweeps vectorized across columns (so building the slope operator is
    O(N) Python iterations, not O(N^2)). The return matches f's ndim.
    """
    x = np.asarray(x, dtype=float)
    f = np.asarray(f, dtype=float)
    n = x.size
    oned = (f.ndim == 1)
    F = f[:, None] if oned else f          # (n, k)
    h = np.diff(x)                         # h[i] = x[i+1]-x[i], length n-1

    # Tridiagonal system for M_1..M_{n-2} (M_0 = M_{n-1} = 0):
    #   h[i-1] M_{i-1} + 2(h[i-1]+h[i]) M_i + h[i] M_{i+1} = rhs_i
    M = np.zeros_like(F)
    if n <= 2:
        # too few points for interior curvature; slope = secant
        d = np.zeros_like(F)
        if n == 2:
            d[:] = (F[1] - F[0]) / h[0]
        return d[:, 0] if oned else d

    lower = h[:-1]                         # sub-diagonal, length n-2 (indices 1..n-2)
    diag = 2.0 * (h[:-1] + h[1:])          # length n-2
    upper = h[1:]                          # super-diagonal
    hc = h[:, None]                        # column-broadcast spacings
    rhs = 6.0 * ((F[2:] - F[1:-1]) / hc[1:] - (F[1:-1] - F[:-2]) / hc[:-1])  # (m, k)

    # Thomas algorithm on the (n-2)x(n-2) interior system. The sweep coefficients
    # cp depend only on x (1-D); dp/Mi carry all k columns (vectorized rows).
    m = n - 2
    cp = np.empty(m)
    dp = np.empty_like(rhs)               # (m, k)
    cp[0] = upper[0] / diag[0]
    dp[0] = rhs[0] / diag[0]
    for i in range(1, m):
        denom = diag[i] - lower[i] * cp[i - 1]
        cp[i] = upper[i] / denom
        dp[i] = (rhs[i] - lower[i] * dp[i - 1]) / denom
    Mi = np.empty_like(rhs)
    Mi[-1] = dp[-1]
    for i in range(m - 2, -1, -1):
        Mi[i] = dp[i] - cp[i] * Mi[i + 1]
    M[1:-1] = Mi

    # slopes from the piecewise-cubic form
    d = np.zeros_like(F)
    d[:-1] = (F[1:] - F[:-1]) / hc - hc * (2.0 * M[:-1] + M[1:]) / 6.0
    d[-1] = (F[-1] - F[-2]) / h[-1] + h[-1] * (2.0 * M[-1] + M[-2]) / 6.0
    return d[:, 0] if oned else d


_SLOPE_MATRIX_CACHE = {}


def slope_matrix(x):
    """The dense operator S with S @ f == natural_spline_slopes(x, f), cached per grid.

    WHY THIS EXISTS.  `natural_spline_slopes` runs two Thomas sweeps as PYTHON loops of
    length n, and the sweep coefficients depend only on `x` -- yet the relaxation
    integrators call it nine times per time step with a single right-hand side, so the
    same n iterations are re-executed with the same coefficients on every call.
    Profiling the Scenario-2 step at n = 801 put **81% of the wall clock in this one
    function** (3.4 s of 4.2 s over forty steps).

    The operator is linear in `f`, so it can be built ONCE per grid by solving with the
    identity as right-hand side -- which the stacked-RHS path already does in O(n)
    Python iterations rather than O(n^2) -- and applied thereafter as a single gemv.
    That is the same O(n^2) per call as the Hilbert transform this code already does,
    but in BLAS instead of in the interpreter.

    The cache is keyed on the grid's bytes, so two different grids of the same length do
    not collide, and a grid that is rebuilt identically is not rebuilt here.  Memory is
    n^2 doubles (20 MB at n = 1601), which is the price of the third rung of a
    refinement ladder and is worth it.

    EXACTNESS.  This is a change of ASSOCIATION, not of formula: S is assembled from the
    same routine it replaces.  It is not bitwise identical to the direct call, because
    `S @ f` sums the same terms in a different order; `test_line_hilbert.py` gates the
    difference, and it sits at rounding.
    """
    x = np.asarray(x, dtype=float)
    key = (x.shape, x.tobytes())
    S = _SLOPE_MATRIX_CACHE.get(key)
    if S is None:
        S = natural_spline_slopes(x, np.eye(x.size))
        _SLOPE_MATRIX_CACHE[key] = S
    return S


# --------------------------------------------------------------------------
# analytic Hilbert transforms of the C^1_0 Hermite basis elements
# --------------------------------------------------------------------------

_LSERIES_NMAX = 60  # for |s|<0.5, 0.5^60/60 ~ 8e-20 << machine eps of L(s)~O(s^4)


def _L_series(s):
    """L(s) = ln|1-s| + s + s^2/2 + s^3/3 = -sum_{n>=4} s^n/n, for |s| < 0.5.

    Evaluated as -s^4 * P(s), P(s) = sum_{n>=4} s^{n-4}/n, by Horner in-place: one
    fused multiply-add per term, no per-iteration division or temporary allocation
    (the hot path -- this runs over the whole N x N stencil array). Callers that
    need both A and B at the same argument should compute L(s) once and pass it in
    (see `_A`/`_B` `Ls=`), since the series is by far the dominant build cost."""
    s = np.asarray(s, dtype=float)
    with np.errstate(over="ignore", invalid="ignore"):
        p = np.full_like(s, 1.0 / _LSERIES_NMAX)  # innermost Horner coeff
        for n in range(_LSERIES_NMAX - 1, 3, -1):
            p *= s
            p += 1.0 / n
        p *= s ** 4
    return -p


def _A(s, Ls=None):
    """A(s), stable for all |s| <= 1 (s=1 gives the finite limit -5/(6 pi)).
    `Ls` may be a precomputed _L_series(s) (shared with _B at the same argument)."""
    s = np.asarray(s, dtype=float)
    small = np.abs(s) < 0.5

    # small-|s| branch (never near s=1): cancellation removed via L(s)
    with np.errstate(divide="ignore", invalid="ignore"):
        s3 = s ** 3
        if Ls is None:
            Ls = _L_series(s)
        a_small = (s3 - 3.0 * s + 2.0) * Ls / (PI * s3) - (3.0 * s ** 2 + 2.0 * s3) / (6.0 * PI)
        # limit at s=0 is 0
        a_small = np.where(np.abs(s) < 1e-12, 0.0, a_small)

    # direct branch (|s| >= 0.5): guard the s->1 product 0*ln0 -> 0
    with np.errstate(divide="ignore", invalid="ignore"):
        one_ms = 1.0 - s
        logt = np.where(np.abs(one_ms) < 1e-300, 0.0, np.log(np.abs(one_ms)))
        poly_log = (s3 - 3.0 * s + 2.0) * logt
        poly_log = np.where(np.abs(one_ms) < 1e-14, 0.0, poly_log)
        a_direct = (-5.0 * s3 - 12.0 * s ** 2 + 12.0 * s + 6.0 * poly_log) / (6.0 * PI * s3)

    return np.where(small, a_small, a_direct)


def _B(s, Ls=None):
    """B(s), stable for all |s| <= 1 (s=1 gives the finite limit -1/(6 pi)).
    `Ls` may be a precomputed _L_series(s) (shared with _A at the same argument)."""
    s = np.asarray(s, dtype=float)
    small = np.abs(s) < 0.5

    with np.errstate(divide="ignore", invalid="ignore"):
        s3 = s ** 3
        if Ls is None:
            Ls = _L_series(s)
        b_small = (s - 1.0) ** 2 * Ls / (PI * s3) + (s - 2.0 * s ** 2) / (6.0 * PI)
        b_small = np.where(np.abs(s) < 1e-12, 0.0, b_small)

    with np.errstate(divide="ignore", invalid="ignore"):
        one_ms = 1.0 - s
        logt = np.where(np.abs(one_ms) < 1e-300, 0.0, np.log(np.abs(one_ms)))
        poly_log = (s - 1.0) ** 2 * logt
        poly_log = np.where(np.abs(one_ms) < 1e-14, 0.0, poly_log)
        b_direct = (2.0 * s3 - 9.0 * s ** 2 + 6.0 * s + 6.0 * poly_log) / (6.0 * PI * s3)

    return np.where(small, b_small, b_direct)


# --------------------------------------------------------------------------
# assembled line Hilbert transform
# --------------------------------------------------------------------------

def line_hilbert_matrix(x):
    """Dense N x N matrix Hmat with H(f)(x_j) = (Hmat @ f)[j].

    Folds the slope dependence in: since the natural-spline slopes f'_i are a
    linear map of the node values f (f' = S @ f), and H(f) = Hp @ f + Hq @ f',
    the returned matrix is Hp + Hq @ S. The grid is fixed during a rescaling
    run, so this is built once and reused every RHS evaluation.
    """
    x = np.asarray(x, dtype=float)
    n = x.size
    xi = x[1:-1]                     # interior source nodes, i = 1..N-2
    xm = x[:-2]                      # x_{i-1}
    xp = x[2:]                       # x_{i+1}
    dm = xm - xi                     # x_{i-1}-x_i  (<0)
    dp = xp - xi                     # x_{i+1}-x_i  (>0)

    # For every evaluation node x_j (rows) and interior source i (cols):
    Xj = x[:, None]                  # (N, 1)
    denom = Xj - xi[None, :]         # (N, N-2)
    with np.errstate(divide="ignore", invalid="ignore"):
        l = dm[None, :] / denom
        r = dp[None, :] / denom
    # L(s) is the dominant build cost and is reused by both A and B at each of the
    # two arguments -> compute it once per argument and share.
    Ls_l = _L_series(l)
    Ls_r = _L_series(r)
    HP = _A(l, Ls_l) - _A(r, Ls_r)                              # (N, N-2)
    HQ = dm[None, :] * _B(l, Ls_l) - dp[None, :] * _B(r, Ls_r)  # (N, N-2)

    # diagonal (x_j == x_i): overwrite rows where j == i+1 in interior indexing
    # interior source i corresponds to global node index i+1, evaluated at j=i+1
    j_diag = np.arange(1, n - 1)     # global node index of each interior source
    col = np.arange(n - 2)           # interior column index
    HP[j_diag, col] = (1.0 / PI) * np.log(np.abs(dm / dp))
    HQ[j_diag, col] = (xm - xp) / (3.0 * PI)

    # slope map S: f'_i = (S @ f)_i, natural cubic spline
    S = _slope_matrix(x)

    # Hp acts on values at interior nodes; Hq acts on slopes at interior nodes.
    Hp_full = np.zeros((n, n))
    Hp_full[:, 1:-1] = HP
    Hq_full = np.zeros((n, n))
    Hq_full[:, 1:-1] = HQ
    return Hp_full + Hq_full @ S


def _slope_matrix(x):
    """Matrix S with f'_i = (S @ f)_i for the natural cubic spline (columns =
    node values). Built in one shot by applying the (batched) slope solve to the
    identity: column k is the slopes of the unit-value hat at node k."""
    x = np.asarray(x, dtype=float)
    n = x.size
    return natural_spline_slopes(x, np.eye(n))


def line_hilbert(x, f, matrix=None):
    """H(f) sampled at the grid nodes x (non-uniform, whole-line).

    Pass a precomputed `matrix` (from `line_hilbert_matrix`) to reuse it across
    RHS evaluations on a fixed grid; otherwise it is built on the fly.
    """
    f = np.asarray(f, dtype=float)
    if matrix is None:
        matrix = line_hilbert_matrix(x)
    return matrix @ f
