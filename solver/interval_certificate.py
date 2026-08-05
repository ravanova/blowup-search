"""Route-L1 step one: the certificate constants as RIGOROUS BOUNDS, not float readings.

WHAT THIS CHANGES, AND WHAT IT DOES NOT
-----------------------------------------------------------------------------
`solver/interval.py` has existed since Route-D as an arithmetic layer and had never
been connected to a certificate.  Every `Y_0`, `Z_1`, `Z_2` this project has printed
was computed in float64, which means `Z_1 = ||I - A DF||` was measuring the
CONDITIONING of a float inverse rather than bounding an operator norm.  Leg 49 put a
number on how badly that eventually bites: on a known-answer object the float `Z_1`
grows like `kappa(DF) * eps_mach` until, at `n ~ 3.2e3`, no weight closes anything.

This module computes the three constants as **rigorous upper bounds**.  What it
certifies is stated once, precisely, and not widened afterwards:

    THEOREM SHAPE.  Let H, D be the stored float matrices, and define F by the
    formulas in `bordered_hl.py` / `weight_search.py` with THOSE matrices as exact
    data.  Then F is a polynomial map R^N -> R^N with exactly-representable
    coefficients, and this module returns Y_0, Z_1, Z_2 such that the radii
    polynomial's conclusion holds: there is a TRUE ZERO of that polynomial system
    within r of the stored float iterate, in the weighted sup norm.

    WHAT IT DOES NOT SAY.  Nothing about the continuum profile.  The gap between the
    discrete system and the PDE is two further terms -- the consistency of (H, D) with
    the operators they discretise, and the far-field tail beyond X_max -- and neither
    is bounded here.  They are separate defects and they get separate treatment
    (standing discipline 75).

WHY THE ARITHMETIC IS AFFORDABLE
-----------------------------------------------------------------------------
A naive interval matrix product is O(N^3) interval operations in Python and is out of
reach at N = 405.  It is not needed.  Two standard facts do the whole job:

  * The approximate inverse A is a CHOICE, not a computed quantity that has to be
    right.  Its stored float entries are exact data; the certificate is valid for
    whatever A is handed to it, and a bad A merely makes Z_1 large.
  * A point matrix times an interval matrix splits monotonically: with
    M = M+ + M-, (M B)_lo = M+ B_lo + M- B_hi and (M B)_hi = M+ B_hi + M- B_lo, plus
    the classic gamma_m bound for the m-term float accumulation.  Four BLAS matmuls
    per product, no Python loop.

So the rigorous constants cost about four times the float ones.

NORMS ARE NAMED, AND THE WEIGHT IS EXACT DATA
-----------------------------------------------------------------------------
The norm is the weighted sup norm defined by the STORED float weight vector w:

    ||z||_w = max_i w_i |z_i|

Any positive vector defines a norm, so w needs no enclosure of its own -- but every
ratio w_i / w_j is rounded UP wherever it appears, so the operator norms are bounds
rather than evaluations.

WHAT IS GATED (test_interval_certificate.py)
-----------------------------------------------------------------------------
Containment in both directions is the test that catches a bound that is not one:
the interval constants must DOMINATE the float constants (a bound that is smaller
than the thing it bounds is broken), the enclosure of F must CONTAIN the float
residual, and a deliberately poisoned iterate must be rejected.
"""

import numpy as np

from solver.interval import Interval, _down, _gamma, _up, dot2_matvec

# --------------------------------------------------------------------------
# rigorous products
# --------------------------------------------------------------------------
def matmul_point_interval(M, Blo, Bhi):
    """Rigorous enclosure of M @ B for an exact float M and an interval matrix B.

    Monotone split on M, then the gamma_m accumulation bound, then the outward ulp
    push. Returns (lo, hi)."""
    M = np.asarray(M, dtype=float)
    m = M.shape[1]
    Mp, Mn = np.maximum(M, 0.0), np.minimum(M, 0.0)
    lo = Mp @ Blo + Mn @ Bhi
    hi = Mp @ Bhi + Mn @ Blo
    g = _gamma(m)
    a_lo = Mp @ np.abs(Blo) + (-Mn) @ np.abs(Bhi)
    a_hi = Mp @ np.abs(Bhi) + (-Mn) @ np.abs(Blo)
    return _down(lo - _up(g * a_lo)), _up(hi + _up(g * a_hi))


def mag(lo, hi):
    """Elementwise max(|lo|, |hi|) -- the magnitude of an interval."""
    return np.maximum(np.abs(lo), np.abs(hi))


def weighted_rowsum_bound(Alo, Ahi, w_row, w_col):
    """Rigorous UPPER bound on max_i w_row_i * sum_j |A_ij| / w_col_j.

    Every step rounds up: the reciprocal, the products, and the m-term sum."""
    A = mag(Alo, Ahi)
    inv = _up(1.0 / np.asarray(w_col, dtype=float))
    m = A.shape[1]
    s = _up(A @ inv)
    s = _up(s * (1.0 + _gamma(m)))
    return float(np.max(_up(np.asarray(w_row, dtype=float) * s)))


# --------------------------------------------------------------------------
# the two bordered systems, enclosed
# --------------------------------------------------------------------------
class BorderedHLIntervals:
    """Interval enclosures of F and DF for `solver.bordered_hl.BorderedHL`.

    The stored operators (H, D, Uop, Drow0) are treated as exact float data, which
    is what makes the enclosed object a polynomial system with representable
    coefficients. z is a float vector, also exact data."""

    def __init__(self, problem):
        self.pr = problem
        self.n, self.N = problem.n, problem.N

    def F(self, z):
        pr = self.pr
        Om, V, c_l, c_om, c_r = pr.unpack(np.asarray(z, dtype=float))
        iOm, iV = Interval.point(Om), Interval.point(V)
        HOm = dot2_matvec(pr.H, Om)
        U = dot2_matvec(pr.Uop, Om)
        S = U + Interval.point(c_l * pr.X) + Interval.point(c_r)
        R_Om = S * dot2_matvec(pr.D, Om) - Interval.point(c_om) * iOm - iV
        R_V = S * dot2_matvec(pr.D, V) - (Interval.point(2.0 * c_om) - HOm) * iV
        G = Interval(np.array([Om[pr.i0] - pr.pin[0],
                               float(pr.Drow0 @ Om) - pr.pin[1],
                               V[pr.i0] - pr.pin[2]]),
                     np.array([Om[pr.i0] - pr.pin[0],
                               float(pr.Drow0 @ Om) - pr.pin[1],
                               V[pr.i0] - pr.pin[2]]))
        # the border rows are affine in exact data; enclose the one dot product
        gd = dot2_matvec(pr.Drow0[None, :], Om)
        G = Interval(np.array([Om[pr.i0] - pr.pin[0], gd.lo[0] - pr.pin[1],
                               V[pr.i0] - pr.pin[2]]),
                     np.array([Om[pr.i0] - pr.pin[0], gd.hi[0] - pr.pin[1],
                               V[pr.i0] - pr.pin[2]]))
        return _cat([R_Om, R_V, G])

    def jacobian(self, z):
        """(Jlo, Jhi) enclosing DF(z). Same expressions as the analytic Jacobian,
        evaluated in interval arithmetic on exact data."""
        pr = self.pr
        n = self.n
        Om, V, c_l, c_om, c_r = pr.unpack(np.asarray(z, dtype=float))
        HOm = dot2_matvec(pr.H, Om)
        U = dot2_matvec(pr.Uop, Om)
        S = U + Interval.point(c_l * pr.X) + Interval.point(c_r)
        Om_X = dot2_matvec(pr.D, Om)
        V_X = dot2_matvec(pr.D, V)
        Jlo = np.zeros((self.N, self.N))
        Jhi = np.zeros((self.N, self.N))
        # rows 0..n-1
        blk = _outer_plus_scaled(Om_X, pr.Uop, S, pr.D)
        blk = _add_diag(blk, -Interval.point(c_om * np.ones(n)))
        Jlo[:n, :n], Jhi[:n, :n] = blk
        Jlo[:n, n:2 * n] = Jhi[:n, n:2 * n] = -np.eye(n)
        Jlo[:n, 2 * n], Jhi[:n, 2 * n] = _col(Om_X * pr.X)
        Jlo[:n, 2 * n + 1] = Jhi[:n, 2 * n + 1] = -Om
        Jlo[:n, 2 * n + 2], Jhi[:n, 2 * n + 2] = _col(Om_X)
        # rows n..2n-1
        blk2 = _outer_plus_outer(V_X, pr.Uop, Interval.point(V), pr.H)
        Jlo[n:2 * n, :n], Jhi[n:2 * n, :n] = blk2
        blk3 = _scale_rows(S, pr.D)
        blk3 = _add_diag(blk3, -(Interval.point(2.0 * c_om) - HOm))
        Jlo[n:2 * n, n:2 * n], Jhi[n:2 * n, n:2 * n] = blk3
        Jlo[n:2 * n, 2 * n], Jhi[n:2 * n, 2 * n] = _col(V_X * pr.X)
        Jlo[n:2 * n, 2 * n + 1] = Jhi[n:2 * n, 2 * n + 1] = -2.0 * V
        Jlo[n:2 * n, 2 * n + 2], Jhi[n:2 * n, 2 * n + 2] = _col(V_X)
        # border rows -- exact
        Jlo[2 * n, pr.i0] = Jhi[2 * n, pr.i0] = 1.0
        Jlo[2 * n + 1, :n] = Jhi[2 * n + 1, :n] = pr.Drow0
        Jlo[2 * n + 2, n + pr.i0] = Jhi[2 * n + 2, n + pr.i0] = 1.0
        return Jlo, Jhi

    def bilinear_bound(self, w, nu):
        """Rigorous upper bound on B = sup_{||v||,||w||<=1} ||Qtilde(v,w)||, the same
        decomposition `bordered_hl.certificate_constants` uses, every step rounded up."""
        pr = self.pr
        Xmax = float(np.abs(pr.X).max())
        w_l, w_om, w_r = w[2 * pr.n], w[2 * pr.n + 1], w[2 * pr.n + 2]
        Uop_ni = weighted_rowsum_bound(pr.Uop, pr.Uop, np.ones(pr.n), nu)
        H_ni = weighted_rowsum_bound(pr.H, pr.H, np.ones(pr.n), nu)
        D_nn = weighted_rowsum_bound(pr.D, pr.D, nu, nu)
        S1 = _up(Uop_ni + _up(Xmax / w_l) + _up(1.0 / w_r))
        B1 = _up(_up(S1 * D_nn) + _up(1.0 / w_om))
        B2 = _up(_up(_up(S1 * D_nn) + H_ni) + _up(2.0 / w_om))
        return float(max(B1, B2))


class BorderedCLMIntervals:
    """The same, for `solver.weight_search.BorderedCLM` -- the known-answer object."""

    def __init__(self, problem):
        self.pr = problem
        self.n, self.N = problem.n, problem.N

    def F(self, z):
        pr = self.pr
        z = np.asarray(z, dtype=float)
        Om, c_l, c_om = pr.unpack(z)
        iOm = Interval.point(Om)
        R = ((Interval.point(c_om) + dot2_matvec(pr.H, Om)) * iOm
             - Interval.point(c_l) * dot2_matvec(pr.XD, Om))
        gd = dot2_matvec(pr.Drow0[None, :], Om)
        G = Interval(np.array([gd.lo[0] - pr.slope0, Om[pr.jstar] - pr.v_pin]),
                     np.array([gd.hi[0] - pr.slope0, Om[pr.jstar] - pr.v_pin]))
        return _cat([R, G])

    def jacobian(self, z):
        pr = self.pr
        n = self.n
        Om, c_l, c_om = pr.unpack(np.asarray(z, dtype=float))
        HOm = dot2_matvec(pr.H, Om)
        Om_XD = dot2_matvec(pr.XD, Om)
        Jlo = np.zeros((self.N, self.N))
        Jhi = np.zeros((self.N, self.N))
        blk = _outer_plus_scaled(Interval.point(Om), pr.H,
                                 Interval.point(-c_l * np.ones(n)), pr.XD)
        blk = _add_diag(blk, Interval.point(c_om) + HOm)
        Jlo[:n, :n], Jhi[:n, :n] = blk
        Jlo[:n, n], Jhi[:n, n] = _col(-Om_XD)
        Jlo[:n, n + 1] = Jhi[:n, n + 1] = Om
        Jlo[n, :n] = Jhi[n, :n] = pr.Drow0
        Jlo[n + 1, pr.jstar] = Jhi[n + 1, pr.jstar] = 1.0
        return Jlo, Jhi

    def bilinear_bound(self, w, nu):
        pr = self.pr
        w_l, w_om = w[pr.n], w[pr.n + 1]
        H_ni = weighted_rowsum_bound(pr.H, pr.H, np.ones(pr.n), nu)
        XD_nn = weighted_rowsum_bound(pr.XD, pr.XD, nu, nu)
        return float(_up(_up(H_ni + _up(1.0 / w_om)) + _up(XD_nn / w_l)))


# --------------------------------------------------------------------------
# the constants
# --------------------------------------------------------------------------
def interval_constants(iv, z, w, nu, A=None):
    """Rigorous (Y_0, Z_1, Z_2) upper bounds in the weighted sup norm given by w.

    A is the approximate inverse: an exact float matrix, and a CHOICE. Default is the
    float inverse of the midpoint Jacobian, which is what makes Z_1 small; nothing
    about the result depends on A being accurate."""
    Jlo, Jhi = iv.jacobian(z)
    if A is None:
        A = np.linalg.inv(0.5 * (Jlo + Jhi))
    Fz = iv.F(z)
    AFlo, AFhi = matmul_point_interval(A, Fz.lo[:, None], Fz.hi[:, None])
    Y0 = float(np.max(_up(np.asarray(w) * mag(AFlo, AFhi)[:, 0])))
    AJlo, AJhi = matmul_point_interval(A, Jlo, Jhi)
    Elo, Ehi = np.eye(iv.N) - AJhi, np.eye(iv.N) - AJlo
    Z1 = weighted_rowsum_bound(Elo, Ehi, w, w)
    A_norm = weighted_rowsum_bound(A, A, w, w)
    B = iv.bilinear_bound(w, nu)
    Z2 = float(_up(2.0 * _up(A_norm * B)))
    return {"Y0": Y0, "Z1": Z1, "Z2": Z2, "A_norm": A_norm, "B": B,
            "rigorous": True}


def radii_verdict(Y0, Z1, Z2):
    """Feasibility of (1/2) Z2 r^2 - (1 - Z1) r + Y0 < 0, with every step rounded the
    conservative way: the budget DOWN, the ratio UP."""
    if not (Z1 < 1.0):
        return {"closes": False, "reason": "Z1 >= 1", "Y0_over_budget": np.inf,
                "budget": 0.0, "r_min": None, "r_max": None}
    budget = _down((1.0 - Z1) ** 2 / _up(2.0 * Z2))
    disc = (1.0 - Z1) ** 2 - _up(2.0 * Y0 * Z2)
    if disc <= 0.0:
        return {"closes": False, "reason": "Y0 exceeds the budget",
                "Y0_over_budget": float(_up(Y0 / budget)) if budget > 0 else np.inf,
                "budget": float(budget), "r_min": None, "r_max": None}
    s = np.sqrt(disc)
    r_min = _up(((1.0 - Z1) - s) / Z2)
    r_max = _down(min(((1.0 - Z1) + s) / Z2, (1.0 - Z1) / Z2))
    return {"closes": bool(r_min < r_max), "reason": "ok",
            "Y0_over_budget": float(_up(Y0 / budget)), "budget": float(budget),
            "r_min": float(r_min), "r_max": float(r_max)}


# --------------------------------------------------------------------------
# small interval helpers used by the Jacobian assemblies
# --------------------------------------------------------------------------
def _mv(M, v):
    """Point matrix times interval vector, rigorous (wraps interval.matvec)."""
    from solver.interval import matvec
    M = np.atleast_2d(np.asarray(M, dtype=float))
    return matvec(M, v)


def _cat(parts):
    return Interval(np.concatenate([p.lo for p in parts]),
                    np.concatenate([p.hi for p in parts]))


def _col(iv):
    return iv.lo, iv.hi


def _scale_rows(s, M):
    """(lo, hi) of diag(s) @ M for an interval vector s and exact M."""
    M = np.asarray(M, dtype=float)
    a = s.lo[:, None] * M
    b = s.hi[:, None] * M
    return _down(np.minimum(a, b)), _up(np.maximum(a, b))


def _outer_plus_scaled(u, M1, s, M2):
    """(lo, hi) of diag(u) @ M1 + diag(s) @ M2, u and s interval vectors."""
    l1, h1 = _scale_rows(u, M1)
    l2, h2 = _scale_rows(s, M2)
    return _down(l1 + l2), _up(h1 + h2)


def _outer_plus_outer(u, M1, v, M2):
    return _outer_plus_scaled(u, M1, v, M2)


def _add_diag(blk, d):
    lo, hi = blk
    lo = lo.copy()
    hi = hi.copy()
    idx = np.arange(lo.shape[0])
    lo[idx, idx] = _down(lo[idx, idx] + d.lo)
    hi[idx, idx] = _up(hi[idx, idx] + d.hi)
    return lo, hi
