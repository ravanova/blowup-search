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

Since leg 98's audit, two of those are also enforced AT RUNTIME rather than only in
the test suite, on whatever object and whatever constants a caller supplies -- see the
next section, and test_interval_certificate_adversarial.py for the battery that
motivated it.
"""

import numpy as np

from solver.certificate_guards import (
    NAN_HINT_LT_ONE, hypothesis_violations as _shared_hypothesis_violations)
from solver.interval import Interval, _down, _gamma, _up, dot2_matvec


# --------------------------------------------------------------------------
# THE HYPOTHESES OF THE IMPORTED THEOREM, ENFORCED (leg 98's finding, repaired)
# --------------------------------------------------------------------------
# Leg 98 (Route-ICA) pointed a 39-case fabrication battery at this module and found that
# 12 of 36 hypothesis-violating inputs came back as CLOSING certificates -- 8 of them
# load-bearing, i.e. the same input with the hypothesis restored does NOT close.  The two
# mechanisms are independent and both are guarded below.
#
#   (1) `radii_verdict` evaluated the discriminant on constants the theorem excludes.
#       `Y_0`, `Z_1`, `Z_2` are UPPER BOUNDS ON NORMS in the radii polynomial theorem
#       (van den Berg-Lessard, AMS Notices 62(9):1057, 2015; Hungria-Lessard-Mireles
#       James, Math. Comp.), hence FINITE and NONNEGATIVE by hypothesis.  A negative
#       `Y_0` makes the discriminant LARGER and buys a certificate with a NEGATIVE
#       r_min; a negative `Z_1` slips past the `Z1 < 1.0` contraction guard and inflates
#       the budget (1-Z_1)^2/(2 Z_2) without bound, rescuing an arbitrarily large
#       residual.  Neither is a conservative input -- it is an input the imported result
#       says nothing about.  `_hypothesis_violations` is the same check, with the same
#       citation, that leg 79's repair put into the sibling pipeline
#       (`solver/port_certification._hypothesis_violations`), and like the sibling it
#       returns a structured non-closing verdict rather than raising: `radii_verdict`'s
#       contract is to RETURN A VERDICT, and every caller in this repository reads its
#       `closes` field.  Raising here would also silently convert the NaN and infinity
#       paths -- which leg 98 measured as already CORRECT, 4/4 -- from a sound refusal
#       into an exception, and those are pinned as HOLDS gates precisely so they cannot
#       change shape.
#
#   (2) `interval_constants` never checked the enclosure it was handed for CONTAINMENT.
#       Validity checking cannot catch this and no amount of it ever will: leg 98's
#       sharpest case is the honest enclosure scaled by 1e-8, which is perfectly well
#       formed (lo <= hi, finite endpoints, positive width, passes leg 69's guard) and
#       simply does not contain the residual it claims to enclose.  It understates Y_0
#       by 1.000e+08x and closes.  The only check that sees this is a re-evaluation of
#       the quantity itself -- `_containment_screen` below, per leg 98's own
#       recommendation (its journal, "Recommended repair", item 4).
#
# SEVERITY WAS AND REMAINS LATENT.  Every in-repo caller of `radii_verdict` takes its
# constants from `interval_constants`, where `Y_0 = max(w * mag(A F))` and `Z_1`, `Z_2`
# are weighted row-sum bounds over MAGNITUDES -- nonnegative whenever `w > 0`, and every
# shipped weight is strictly positive by construction (`exp(clip(.))` in
# `weight_search.weight_vector`, the symbol `l_n > 0` in `KawaharaProblem.weight`).  No
# banked number in this repository moves.  What the guards restore is the GUARANTEE.

class CertificateInputError(ValueError):
    """Data handed to `interval_constants` that lies outside the certificate's hypotheses.

    Raised, not returned, and the distinction is deliberate: `interval_constants`'
    contract is to return RIGOROUS BOUNDS, so there is no field in its result in which a
    refusal could honestly be reported.  A bound that was never established must not be
    handed back in the same slot as one that was.  `radii_verdict`, whose contract IS to
    return a verdict, reports its own hypothesis violations as `closes=False` instead."""


def _hypothesis_violations(Y0, Z1, Z2):
    """Which hypothesis of the radii polynomial theorem each supplied constant breaks.

    Mirrored `solver.port_certification._hypothesis_violations` (leg 79's repair) so the
    two pipelines could not drift apart on what "outside the theorem" means.  SINCE LEG 128
    IT NO LONGER MIRRORS IT -- both call the SAME function,
    `solver.certificate_guards.hypothesis_violations`, so drift is now impossible rather
    than merely intended against.  The predicate, the message strings and this module's
    raise-on-`None` policy are unchanged byte-for-byte; `nk_bounds.budget` is the third
    caller and the reason the copy became an abstraction (the Rule of Three).

    Returns a list of strings naming the offending constant and the hypothesis it breaks;
    empty means every constant is admissible.  `0.0` and `-0.0` are legitimate bounds and
    are NOT violations -- a zero `Z_2` is a degeneracy of the polynomial, handled
    separately and named as such, not a hypothesis failure."""
    return _shared_hypothesis_violations(
        (("Y_0", Y0), ("Z_1", Z1), ("Z_2", Z2)),
        allow_none=False, nan_hint=NAN_HINT_LT_ONE)


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

    def F_float(self, z):
        """The SAME residual, evaluated in plain float64 -- the containment reference.

        Not part of any bound: `interval_constants` uses it only to check that the
        enclosure returned by `F` is an enclosure OF SOMETHING, and of this problem's
        residual in particular (see `_containment_screen`)."""
        return np.asarray(self.pr.F(np.asarray(z, dtype=float)), dtype=float)

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

    def F_float(self, z):
        """The float64 residual -- the containment reference, not a bound."""
        return np.asarray(self.pr.F(np.asarray(z, dtype=float)), dtype=float)

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
# How far the float re-evaluation of the residual may exceed the enclosure's own Y_0
# before the enclosure is refused.  THIS NUMBER IS MEASURED, NOT CHOSEN BY TASTE, and it
# has to be a slack rather than an exact containment test for a reason banked as lesson
# 86: the float evaluation of F is itself noisy (`BorderedCLM.residual_floor` measures
# that noise, and it GROWS with n), so at a converged iterate the plain-float residual
# routinely falls a few ulp OUTSIDE a correct, tight enclosure.  Componentwise exact
# containment therefore fails on honest data -- measured, 40/103 components at
# BorderedCLM n=101 -- and would break every legitimate certificate in the repository.
#
# What IS stable is the ratio in the certificate's own currency.  Measured on honest
# data with this module's own enclosure classes:
#
#     max_i w_i |A F_float(z)|_i  /  Y_0          (the screen's ratio)
#     BorderedCLM  n=101   z converged   0.081
#     BorderedCLM  n=101   z displaced   1.000
#     BorderedCLM  n=201 / n=401         0.179 / 0.151
#     Kawahara     N=250   CLN iterate   0.038
#     Kawahara     N=250   trace-projected 0.057
#
# (the BorderedHL path is not tabulated here but is covered: gates (3), (5), (6) and (7)
# of test_interval_certificate.py drive `interval_constants` through it at n = 201, 401
# and 801, on both the compensated and the naive enclosure class, and all four pass the
# screen with their printed numbers unchanged to the last digit.)
#
# i.e. never above 1.0, as it should be -- Y_0 is a rigorous upper bound and the float
# reading is the thing it bounds.  Leg 98's sharpest fabrication (the honest enclosure
# scaled by 1e-8) sits at 1.0e+08 on the same ratio.  The threshold is placed at the
# geometric midpoint of those two, 1e4: four decades of headroom above anything honest
# ever measured, four decades of margin below the smallest lie in the battery.
#
# WHAT THIS DOES AND DOES NOT PROMISE.  It is a SCREEN, and it is stated as one: it
# catches order-of-magnitude fabrication of the residual enclosure, not a subtle
# understatement below 1e4x.  The rigour of the certificate still rests on the enclosure
# class being correct -- that is what the exact-rational gates in
# test_interval_certificate.py are for.  What the screen removes is the ability of an
# ARBITRARY caller-supplied object to hand this function a residual enclosure with no
# relation to the problem and get a closing certificate out.
_CONTAINMENT_SLACK = 1.0e4


def _containment_screen(iv, z, w, A, Fz, Y0):
    """Refuse a residual enclosure that does not enclose this problem's residual.

    Leg 98's recommended repair, item 4, and the only check that catches its case A6:
    re-evaluate F in float at the same point and compare in the Y_0 currency.  See
    `_CONTAINMENT_SLACK` for why the comparison carries a slack and what it promises.

    Non-finite readings on either side are NOT refused here: they are left to travel to
    `radii_verdict`, which rejects a non-finite Y_0 by hypothesis.  That keeps the
    zero/NaN-weight path -- sound today, and pinned as a HOLDS gate -- unchanged."""
    f_float = getattr(iv, "F_float", None)
    if f_float is None:
        raise CertificateInputError(
            f"{type(iv).__name__} exposes no `F_float`, so the residual enclosure it "
            "returns cannot be checked for CONTAINMENT (leg 98 case A6: a well-formed "
            "enclosure that simply does not contain the residual understates Y_0 by "
            "1e8x and closes). An enclosure class must be able to re-evaluate its own "
            "residual in float.")
    fz = np.asarray(f_float(z), dtype=float).reshape(-1)
    if fz.shape[0] != np.asarray(Fz.lo).reshape(-1).shape[0]:
        raise CertificateInputError(
            f"`F_float` returned {fz.shape[0]} components and `F` enclosed "
            f"{np.asarray(Fz.lo).reshape(-1).shape[0]}; they are not the same residual.")
    Y0_float = float(np.max(np.abs(np.asarray(w, dtype=float) * (np.asarray(A) @ fz))))
    if np.isfinite(Y0_float) and np.isfinite(Y0) and Y0_float > _CONTAINMENT_SLACK * Y0:
        raise CertificateInputError(
            f"the residual enclosure does not contain the residual: it gives "
            f"Y_0 = {Y0:.6e}, while F re-evaluated in float at the same point gives "
            f"{Y0_float:.6e} in the same norm -- a factor {Y0_float / Y0:.3e}, past the "
            f"{_CONTAINMENT_SLACK:.0e} screen. An enclosure of F(z) that excludes F(z) "
            "is not a bound and no certificate may be read off it.")
    return Y0_float


def interval_constants(iv, z, w, nu, A=None):
    """Rigorous (Y_0, Z_1, Z_2) upper bounds in the weighted sup norm given by w.

    A is the approximate inverse: an exact float matrix, and a CHOICE. Default is the
    float inverse of the midpoint Jacobian, which is what makes Z_1 small; nothing
    about the result depends on A being accurate.

    TWO PIECES OF CALLER DATA ARE CHECKED BEFORE ANY BOUND IS RETURNED (leg 98):

      * `w`, which DEFINES the norm the certificate is stated in.  A negative component
        is not a norm, and leg 98 measured it end to end: `w -> -w` is accepted, drives
        `Y_0` NEGATIVE (-2.5e-28), and the negative `Y_0` then closes.  Refused here.
        A zero or NaN component is deliberately NOT refused: it drives `Z_1` non-finite
        through `1/w`, the certificate is already rejected downstream for that reason,
        and that behaviour is pinned as a HOLDS gate in
        test_interval_certificate_adversarial.py.  A weight can also underflow to zero
        legitimately during a sweep over `theta`, and turning that into an exception
        would break the sweep rather than the certificate.
      * the residual enclosure, for CONTAINMENT -- see `_containment_screen`.

    Both refusals are `CertificateInputError`, never a returned constant."""
    w_arr = np.asarray(w, dtype=float)
    if np.any(w_arr < 0.0):
        k = int(np.argmin(w_arr))
        raise CertificateInputError(
            f"the weight vector has {int(np.sum(w_arr < 0.0))} negative component(s) "
            f"(w[{k}] = {w_arr[k]!r}); ||z||_w = max_i w_i |z_i| is a norm only for a "
            "strictly positive w, and a negative one produces a negative Y_0 -- outside "
            "the radii polynomial theorem's hypotheses entirely.")
    Jlo, Jhi = iv.jacobian(z)
    if A is None:
        A = np.linalg.inv(0.5 * (Jlo + Jhi))
    Fz = iv.F(z)
    AFlo, AFhi = matmul_point_interval(A, Fz.lo[:, None], Fz.hi[:, None])
    Y0 = float(np.max(_up(np.asarray(w) * mag(AFlo, AFhi)[:, 0])))
    _containment_screen(iv, z, w, A, Fz, Y0)
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
    conservative way: the budget DOWN, the ratio UP.

    THE CONSTANTS ARE CHECKED AGAINST THE THEOREM'S OWN HYPOTHESES FIRST (leg 98, the
    same repair leg 79 landed in the sibling pipeline).  A negative or non-finite
    `Y_0`/`Z_1`/`Z_2` returns `closes=False` with `reason` beginning `INVALID_INPUT` and
    a `violations` list, and NO discriminant is evaluated -- ahead of the contraction
    guard, because `Z_1 < 0` passes `Z_1 < 1.0` and would otherwise inflate the budget
    `(1-Z_1)^2/(2 Z_2)` without bound.  The offending values are deliberately not echoed
    into `budget`/`r_min`/`r_max`: a rejected fabrication must not be reported in the
    same slots as a measured bound."""
    violations = _hypothesis_violations(Y0, Z1, Z2)
    if violations:
        return {"closes": False,
                "reason": ("INVALID_INPUT: outside the hypotheses of the radii "
                           "polynomial theorem (Y_0, Z_1, Z_2 are upper bounds on norms, "
                           "hence finite and nonnegative): " + "; ".join(violations)
                           + ". No discriminant is evaluated."),
                "violations": violations, "Y0_over_budget": np.inf,
                "budget": 0.0, "r_min": None, "r_max": None}
    if not (Z1 < 1.0):
        return {"closes": False, "reason": "Z1 >= 1", "Y0_over_budget": np.inf,
                "budget": 0.0, "r_min": None, "r_max": None}
    if Z2 == 0.0:
        # Z_2 = 0 is what an exactly LINEAR system gives, and it used to raise a bare
        # ZeroDivisionError from inside this function -- sound (a crash is a refusal) but
        # a caller with a broad `except` turns it into a silent skip (leg 98, B20/B21).
        # It is reported instead.  The verdict stays NON-closing: with Z_2 = 0 the radii
        # polynomial degenerates from a quadratic to the affine Y_0 - (1-Z_1) r, whose
        # feasibility is a DIFFERENT statement from the one this function implements and
        # is not certified here.  Refusing is the conservative reading, and this repair
        # adds no mathematics.
        return {"closes": False,
                "reason": ("Z2 == 0 (degenerate: the radii polynomial is affine, not "
                           "quadratic; this function certifies the quadratic case and "
                           "makes no claim about the affine one)"),
                "degenerate": "Z2 == 0",
                # reported exactly as the other refusal branch reports itself: NO budget
                # was established.  (The affine problem's own budget is unbounded, which
                # is precisely why quoting it here would read as a pass.)
                "Y0_over_budget": np.inf, "budget": 0.0,
                "r_min": None, "r_max": None}
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


# --------------------------------------------------------------------------
# ROUTE-TN (leg 56): the (H, D) CONSISTENCY DEFECT, enclosed
# --------------------------------------------------------------------------
# THE GAP THIS ADDRESSES, AND THE ONE IT DOES NOT.
# This module's own docstring names two things that keep the interval certificate
# at "step one of L1" rather than L1: the far-field tail beyond X_max, and the
# CONSISTENCY of (H, D) with the operators they discretise.  What follows measures
# the second one, at FIXED reach.  It is not, and must not be read as, an attack on
# the first: X_max is held fixed throughout and the truncation term is computed
# separately and reported separately, precisely so the two defects are not confused
# with each other (standing discipline 75).
#
# THE QUANTITY HAS NO OPERATOR NORM, AND THAT IS THE FIRST FINDING (discipline 73).
# There is no such thing as ||H_disc - H|| here.  H_disc maps R^n -> R^n; H maps
# functions to functions.  The difference is only defined once a CLASS OF FUNCTIONS
# is named, and its size depends on that class -- a function with features finer
# than the local mesh has an enormous defect and a well-resolved one has a tiny
# defect, on the same grid, with the same operator.  So the defect is reported ON A
# NAMED CLASS, as a curve in the class's scale parameter, and never as a single
# number pretending to be an operator norm.
#
# THE MECHANISM.  ***CORRECTED after VER-C's review -- see the section at the bottom
# of this file.  The two operators do NOT share an interpolant.***
#
# `line_hilbert_matrix` is NOT a quadrature rule.  It represents the data by a C^1
# cubic spline and applies the EXACT Hilbert transform of that spline (Huang-Tong-
# Wang App. C.1).  BUT it assembles source columns for INTERIOR nodes only, dropping
# the two endpoint basis functions, so the spline it transforms is Pi^0_n f -- pinned
# to zero value and zero slope at +-M -- and NOT the natural-spline interpolant Pi_n f
# that `slope_matrix` differentiates.  Exactly:
#
#     H_disc f  =  H(Pi^0_n f) restricted to [-M, M]      (M = max |X|)
#     D_disc f  =  (Pi_n f)'  at the nodes                 <-- a DIFFERENT interpolant
#
# so the gated defect carries two terms of different character:
#
#     D_disc f - f'      =  (Pi_n f - f)'                 order 4, the spline order
#     H_disc f - H_M f   =  [H(Pi^0_n f) - H(Pi_n f)]     endpoint zeroing, DOES NOT converge
#                         + [H(Pi_n f)   - H_M f]         true interpolation, order ~1.95
#     H_M f    - H f     =  the far-field tail            <-- THE OTHER GAP, reported not gated
#
# where H_M is the Hilbert transform truncated to [-M, M].  `SplineConsistency.
# decomposition` measures the split; the GATED quantity is the total, i.e. the defect
# of the operator as implemented.  H's part cannot be bounded from ||e||_sup in any
# case: H is unbounded on L^infinity.  It has to be evaluated, and that is what the
# closed form below is for.
#
# THE TEST CLASS.  f_{a,b}(X) = -(X - b) / ((X - b)^2 + a^2), whose whole-line
# Hilbert transform, truncated Hilbert transform and derivative are ALL closed form:
#
#     H f_{a,b}(x) = a / ((x - b)^2 + a^2)
#     f'_{a,b}(x)  = ((x - b)^2 - a^2) / ((x - b)^2 + a^2)^2
#
# (`a = 1/2, b = 0` is exactly the CLM pair `line_hilbert.py` already gates against).
# The truncated transform follows from partial fractions of -u/((u^2+a^2)(X-u)):
# with X = x - b, A = C = -X/(X^2+a^2), B = a^2/(X^2+a^2),
#
#     pi H_M f = (A/2) ln((u2^2+a^2)/(u1^2+a^2))
#              + (B/a)(arctan(u2/a) - arctan(u1/a))
#              - C ln|(x - M)/(x + M)|,     u1 = -M-b,  u2 = M-b,
#
# which tends to pi B/a = pi H f as M -> infinity, as it must.  The TRUNCATION is
# formed directly, cancellation-free, rather than as a difference of two nearly
# equal numbers.
#
# THE ENDPOINT NODES ARE EXCLUDED, AND WHY.  At x = +-M the truncated transform is
# logarithmically divergent (the cut end of the integral sits on the evaluation
# point).  H_disc's own boundary basis is one-sided and finite there, and the two
# divergences cancel in the difference -- but not in floating point.  The defect is
# therefore reported on the INTERIOR nodes, and the count of excluded nodes is
# reported with it.  Those two nodes are where the far-field gap lives anyway.

class SplineConsistency:
    """Rigorous enclosures of the (H, D) consistency defect on the rational class.

    `problem` is a `BorderedHL` (or anything exposing `X`, `H`, `D`).  All defects
    are returned as enclosures together with their WIDTHS, because a rigorous bound
    whose width is comparable to its value is a statement about the code and not
    about the operator (standing discipline 86)."""

    def __init__(self, problem):
        self.pr = problem
        self.X = np.asarray(problem.X, dtype=float)
        self.M = float(np.abs(self.X).max())
        self.interior = np.abs(self.X) < self.M          # drop the two endpoint nodes

    # -- the class, enclosed -------------------------------------------------
    # TWO families, and the second one exists to FALSIFY the first one's mechanism
    # (standing discipline 85/90 -- ablate the mechanism, and only quote a control
    # that could have come out the other way):
    #
    #   "odd"   f = -u/(u^2+a^2),  H f = a/(u^2+a^2),  f(+-M) ~ 1/M    DECAYS LIKE 1/X
    #   "even"  g =  a/(u^2+a^2),  H g = u/(u^2+a^2),  g(+-M) ~ a/M^2  DECAYS LIKE 1/X^2
    #
    # (`H` is a rotation: H^2 = -1, so the second pair is the first one transformed,
    # and both are exact.)  They have the SAME smoothness and the SAME interior
    # resolution demands and differ by two orders of magnitude in their VALUE AT THE
    # CUT.  If the H defect is set by interior interpolation, the two families give
    # the same number; if it is set by what the discrete operator does at +-M, the
    # "even" family's defect collapses.  Nothing in the code knows which is which.
    def _coeffs(self, a, b, family):
        """(A, B) of the partial-fraction decomposition; C == A in both families."""
        iX = Interval.point(self.X)
        u = iX - Interval.point(float(b))
        ia = Interval.point(float(a))
        ia2 = Interval.point(float(a) ** 2)
        den = u * u + ia2
        if family == "odd":
            return u, den, (-u / den), (ia2 / den)
        if family == "even":
            return u, den, (ia / den), (ia * u / den)
        raise ValueError(f"unknown family {family!r}")

    def f(self, a, b=0.0, family="odd"):
        """Enclosure of the test function at every node."""
        u, den, _A, _B = self._coeffs(a, b, family)
        if family == "odd":
            return -u / den
        return Interval.point(float(a)) / den

    def f_prime(self, a, b=0.0, family="odd"):
        """Enclosure of the test function's derivative at every node."""
        u, den, _A, _B = self._coeffs(a, b, family)
        ia2 = Interval.point(float(a) ** 2)
        if family == "odd":
            return (u * u - ia2) / (den * den)
        return -(Interval.point(2.0 * float(a)) * u) / (den * den)

    def H_exact(self, a, b=0.0, family="odd"):
        """Enclosure of the WHOLE-LINE Hilbert transform at every node (= B/a)."""
        _u, _den, _A, B = self._coeffs(a, b, family)
        return B / Interval.point(float(a))

    def H_truncation(self, a, b=0.0, family="odd"):
        """Enclosure of (H f - H_M f): the FAR-FIELD gap, formed cancellation-free.

        This is the OTHER named gap.  It is computed here only so that it can be
        SUBTRACTED OFF and reported separately -- it is not what leg 56 gates."""
        from solver.interval import IPI, iatan_small, ilog
        M = self.M
        _u, _den, A, B = self._coeffs(a, b, family)
        Bov_a = B / Interval.point(float(a))              # B/a
        u2 = float(M - b)
        u1 = float(-M - b)
        # arctan tail, both arguments small: pi - (atan(u2/a) - atan(u1/a))
        t2 = iatan_small(np.full(self.X.shape, float(a) / u2))
        t1 = iatan_small(np.full(self.X.shape, float(a) / (-u1)))
        atan_part = Bov_a * (t2 + t1)
        # log of the symmetric-cut ratio (a pure constant across nodes)
        r = float((u2 * u2 + float(a) ** 2) / (u1 * u1 + float(a) ** 2))
        log1 = A * Interval.point(0.5) * ilog(np.full(self.X.shape, r))
        # -C ln|(x-M)/(x+M)| with C = A; safe only on the interior
        Xi = np.where(self.interior, self.X, 0.0)
        lg = ilog(np.maximum(M - Xi, 1e-300)) - ilog(np.maximum(M + Xi, 1e-300))
        log2 = -A * lg
        num = atan_part - log1 - log2
        return num / IPI

    # -- the discrete operators applied, rigorously --------------------------
    def _apply(self, Mat, iv_vec):
        """Rigorous enclosure of Mat @ v for an exact float Mat and enclosed input v.

        The compensated path is used on the MIDPOINT (that is the evaluation whose
        cancellation matters, leg 50), and the input's own radius is carried through
        by the exact non-negative bound |Mat| @ rad.  Both pieces are rounded out."""
        Mat = np.asarray(Mat, dtype=float)
        mid = np.asarray(iv_vec.mid, dtype=float)
        rad = np.asarray(iv_vec.rad, dtype=float)
        core = dot2_matvec(Mat, mid)
        m = Mat.shape[1]
        spread = _up(np.abs(Mat) @ rad)
        spread = _up(spread * (1.0 + _gamma(m)))
        return Interval(_down(core.lo - spread), _up(core.hi + spread))

    def decomposition(self, a, b=0.0, nu=None, family="odd"):
        """Split the Hilbert defect into endpoint-zeroing and true interpolation.

        Enclosed by the same path as `defects` -- the full-interpolant matrix is exact
        float data by exactly the convention the certificate already applies to `H`
        itself. The endpoint nodes are excluded as everywhere else."""
        nu = np.ones_like(self.X) if nu is None else np.asarray(nu, dtype=float)
        msk = self.interior
        fv = self.f(a, b, family)
        H_M = self.H_exact(a, b, family) - self.H_truncation(a, b, family)
        Hfull = full_interpolant_hilbert_matrix(self.X)
        d_total = self._apply(self.pr.H, fv) - H_M          # the GATED quantity
        d_interp = self._apply(Hfull, fv) - H_M             # true interpolation error
        d_endpt = self._apply(self.pr.H, fv) - self._apply(Hfull, fv)   # the artifact

        def wsup(iv):
            m = np.maximum(np.abs(np.asarray(iv.lo))[msk], np.abs(np.asarray(iv.hi))[msk])
            return float(np.max(_up(nu[msk] * m)))

        return {"a": float(a), "family": family, "n": int(self.X.size),
                "defect_H_total": wsup(d_total),
                "defect_H_interpolation": wsup(d_interp),
                "defect_H_endpoint_zeroing": wsup(d_endpt)}

    # -- the defects ---------------------------------------------------------
    def defects(self, a, b=0.0, nu=None, family="odd"):
        """Enclosures of the D and H consistency defects in the weighted sup norm.

        Returns absolute defects, the relative ones (divided by the same weighted
        norm of the test function itself), the enclosure widths, and the far-field
        truncation term kept strictly separate."""
        nu = np.ones_like(self.X) if nu is None else np.asarray(nu, dtype=float)
        msk = self.interior
        fv = self.f(a, b, family)
        # --- D: (Pi_n f)' - f' at the nodes
        Dd = self._apply(self.pr.D, fv)
        dD = Dd - self.f_prime(a, b, family)
        # --- H: H(Pi_n f) - H_M f on [-M, M]
        Hd = self._apply(self.pr.H, fv)
        trunc = self.H_truncation(a, b, family)
        H_M = self.H_exact(a, b, family) - trunc
        dH = Hd - H_M

        def wsup(iv):
            """Rigorous weighted sup of |iv| over the interior nodes, and its lower mate."""
            lo = np.asarray(iv.lo)[msk]
            hi = np.asarray(iv.hi)[msk]
            m = np.maximum(np.abs(lo), np.abs(hi))
            lowmag = np.minimum(np.abs(lo), np.abs(hi))
            straddle = (lo <= 0) & (hi >= 0)
            lowmag = np.where(straddle, 0.0, lowmag)
            wu = _up(nu[msk] * m)
            wl = _down(nu[msk] * lowmag)
            return float(np.max(wu)), float(np.max(wl))

        f_norm_hi, f_norm_lo = wsup(fv)
        dD_hi, dD_lo = wsup(dD)
        dH_hi, dH_lo = wsup(dH)
        tr_hi, tr_lo = wsup(trunc)
        return {
            "a": float(a), "b": float(b),
            "n": int(self.X.size), "interior_nodes": int(msk.sum()),
            "excluded_nodes": int((~msk).sum()), "X_max": self.M,
            "f_norm_w": f_norm_hi,
            "defect_D_abs": dD_hi, "defect_D_abs_lower": dD_lo,
            "defect_H_abs": dH_hi, "defect_H_abs_lower": dH_lo,
            "truncation_H_abs": tr_hi, "truncation_H_abs_lower": tr_lo,
            "defect_D_rel": float(_up(dD_hi / f_norm_lo)) if f_norm_lo > 0 else float("inf"),
            "defect_H_rel": float(_up(dH_hi / f_norm_lo)) if f_norm_lo > 0 else float("inf"),
            # lesson 86: how much of the bound is the bound, and how much is the code
            "width_frac_D": float((dD_hi - dD_lo) / dD_hi) if dD_hi > 0 else float("nan"),
            "width_frac_H": float((dH_hi - dH_lo) / dH_hi) if dH_hi > 0 else float("nan"),
        }


# --------------------------------------------------------------------------
# THE CORRECTION (leg 56, after VER-C's review): H AND D DO NOT SHARE AN INTERPOLANT
# --------------------------------------------------------------------------
# The first version of this module claimed that `H_disc` and `D_disc` are the exact
# Hilbert transform and the exact derivative OF THE SAME natural-spline interpolant,
# so that both consistency defects were one interpolation error seen through two
# operators.  THAT CLAIM IS FALSE, and the ablation two sections up already contained
# the evidence against it without naming it.
#
# `slope_matrix` really is the full natural-spline slope operator at every node.  But
# `line_hilbert_matrix` assembles source columns for INTERIOR nodes only --
# `Hp_full[:, 1:-1] = HP`, and likewise for `Hq_full` -- so the two endpoint basis
# functions are dropped.  The function it actually transforms is therefore
#
#     Pi^0_n f  =  the C^1 piecewise cubic that matches f and the natural-spline
#                  slopes at the INTERIOR nodes, and is ZERO with ZERO SLOPE at +-M
#
# and not `Pi_n f`.  Measured at n = 201, node 1 (X = -687.94), with `a = 1/2`:
#
#     H_disc f                      = -1.858472e-03
#     H(Pi^0_n f), by PV quadrature = -1.858472e-03   <- agrees to 2.6e-15
#     H(Pi_n f),  by PV quadrature  = -1.488064e-03   <- differs by 3.7e-04
#     H_M f (the reference)         = -1.488558e-03
#
# So the operator's defect splits into two terms of completely different character:
#
#     H_disc f - H_M f  =  [H(Pi^0_n f) - H(Pi_n f)]  +  [H(Pi_n f) - H_M f]
#                           ^ ENDPOINT ZEROING          ^ TRUE INTERPOLATION
#                             O(f(+-M)), does not         converges, order ~2
#                             converge at fixed reach
#
# The gated quantity is unchanged -- it is the defect of the operator AS IMPLEMENTED,
# and that is the left-hand side.  What changes is the ATTRIBUTION, and it matters for
# anyone reading this code next: the Hilbert side is not a slightly worse version of
# the derivative side, it is a structurally different discretisation.

def full_interpolant_hilbert_matrix(x):
    """`line_hilbert_matrix` WITH the two endpoint basis functions restored.

    Diagnostic only -- this is not what the certificate runs on.  It exists so the
    endpoint-zeroing term can be separated from the genuine interpolation term.

    The endpoint hats are ONE-SIDED: P_0 and Q_0 are supported on [x_0, x_1] alone, so
    their transforms are the r-part of the interior formula by itself; P_{n-1}, Q_{n-1}
    are supported on [x_{n-2}, x_{n-1}] and give the l-part alone.  Row 0 and row n-1
    are left as NaN on purpose: at x = +-M a one-sided value hat has a genuinely
    divergent transform, and every caller here already excludes those two nodes.
    Verified against direct principal-value quadrature to seven digits."""
    from solver.line_hilbert import _A, _B, _L_series, _slope_matrix
    x = np.asarray(x, dtype=float)
    n = x.size
    Xj = x[:, None]
    HP = np.zeros((n, n))
    HQ = np.zeros((n, n))

    xi, xm, xp = x[1:-1], x[:-2], x[2:]
    dm, dp = xm - xi, xp - xi
    with np.errstate(divide="ignore", invalid="ignore"):
        l = dm[None, :] / (Xj - xi[None, :])
        r = dp[None, :] / (Xj - xi[None, :])
        Ll, Lr = _L_series(l), _L_series(r)
        HP[:, 1:-1] = _A(l, Ll) - _A(r, Lr)
        HQ[:, 1:-1] = dm[None, :] * _B(l, Ll) - dp[None, :] * _B(r, Lr)
        jd = np.arange(1, n - 1)
        HP[jd, jd] = (1.0 / np.pi) * np.log(np.abs(dm / dp))
        HQ[jd, jd] = (xm - xp) / (3.0 * np.pi)

        d0 = x[1] - x[0]
        r0 = d0 / (x - x[0])
        L0 = _L_series(r0)
        HP[:, 0] = -_A(r0, L0)
        HQ[:, 0] = -d0 * _B(r0, L0)

        dn = x[-2] - x[-1]
        ln = dn / (x - x[-1])
        Ln = _L_series(ln)
        HP[:, -1] = _A(ln, Ln)
        HQ[:, -1] = dn * _B(ln, Ln)

    HP[0, :] = np.nan
    HP[-1, :] = np.nan
    return HP + HQ @ _slope_matrix(x)


# --------------------------------------------------------------------------
# ROUTE-KA (leg 61): THE FIRST PUBLISHED KNOWN-ANSWER PROBLEM THIS PIPELINE HAS RUN
# --------------------------------------------------------------------------
# WHY THIS IS HERE.  Read the `validated` column of capabilities.py for the
# certificate stack: every entry is validated INTERNALLY.  Enclosures contain exact
# rationals; rigorous bounds dominate their float readings; a poisoned iterate is
# rejected.  All of that is self-consistency.  What the stack had never done, before
# this section, is point `interval_constants` + `radii_verdict` at a problem whose
# certified radius is IN PRINT and see where it lands.
#
# THE PROBLEM.  Cadiot-Lessard-Nave, arXiv:2302.12877 (SIADS 10.1137/23M1607507),
# section 6: the Kawahara soliton.  With Bond number T and wave speed c,
#
#     u_t + u u_y + (3/2) u_y + a(T) u_yyy + b(T) u_yyyyy = 0,
#     a(T) = (1 - 3T)/6,   b(T) = (19 - 30T - 45T^2)/360,
#
# and the travelling-wave reduction x = y - ct, integrated once, becomes the zero
# finding problem CLN call (75).  In the sign convention of their released code
# (github.com/matthieucadiot/ProofKawahara.jl) it is
#
#     F(u) = L u + lam3 u^2 = 0,     L = I + lam1 d_xx + lam2 d_xxxx,
#     lam1 = (1 - 3T)/(6(1 - c)),  lam2 = (19 - 30T - 45T^2)/(360(1 - c)),
#     lam3 = 3/(4(1 - c)).
#
# THEIR PARAMETERS ARE NOT ALL IN THE PAPER.  The paper prints T = 0.35, c = 0.9 and
# the constants (||DF_e(u0)^{-1}||_{2,l} <= 4.4, Y_0 <= 2.26e-14, r_0 = 2.27e-14,
# uniqueness in B_0.015) but NOT the truncation.  `ProofKawahara.jl` lines 357-360
# print it: N = 250 cosine modes (0..N) and half-domain d = 50.  The window this
# section is gated against is pre-committed AT THAT TRUNCATION (writeup/novelty/
# leg_61.md), which is only possible because CLN released their code.
#
# THE REPRESENTATION, AND WHY IT IS THE EXPONENTIAL ONE.  CLN write cosine series in
# the L^2-orthonormal normalisation u = U_0 + sqrt(2) sum_{n>=1} U_n cos(n pi x / d).
# Convolution is clumsy in that normalisation and trivial in the exponential one, so
# this class carries the EVEN EXPONENTIAL coefficients
#
#     a_n = (1/|Omega_0|) int_{Omega_0} u(x) e^{-i n pi x / d} dx,   a_{-n} = a_n,
#
# i.e. u = sum_{n in Z} a_n e^{i n pi x / d}, with U_0 = a_0 and U_n = sqrt(2) a_n.
# The two normalisations give the SAME l^2 norm on the whole-line index set, so
# ||U||_{X^l} = ||a||_{l^2_l(Z)} exactly -- which is what makes the comparison to
# CLN's radius a conversion between norms and not between conventions.
#
# The folded product.  With a, b even and supported on |n| <= N,
#
#     (a*b)_n = sum_{m in Z} a_m b_{n-m} = M(a) b,
#     M(a)_{n,0} = a_n,   M(a)_{n,m} = a_{|n-m|} + a_{n+m}  (m >= 1),
#
# where a_k := 0 for k > N.  So the GALERKIN system this pipeline certifies is
#
#     F_n(a) = l_n a_n + lam3 (a*a)_n,  n = 0..N,   l_n = 1 - lam1 k_n^2 + lam2 k_n^4,
#
# with k_n = n pi / d.  It is a genuine polynomial map R^{N+1} -> R^{N+1}.
#
# WHAT THIS DOES *NOT* CERTIFY, SAID BEFORE THE NUMBER IS QUOTED (discipline 75).
# The Galerkin system is the truncation of the PERIODIC problem on Omega_0.  CLN
# certify strictly more: the Fourier tail n > N, and the passage from the periodic
# problem to the one on R.  Their Theorem 6.6 states BOTH conclusions, and the
# periodic one -- a solution in B_{r_0/sqrt(|Omega_0|)}(U_0) of X^l_e -- is the one
# this section is comparable to.  Because we bound FEWER error terms than they do,
# a converted radius BELOW theirs is evidence of over-optimism, not of sharpness.
#
# THE NORM IS NOT THEIRS, AND THE CONVERSION IS PART OF THE RESULT.  This pipeline
# works in the weighted sup norm ||a||_w = max_n w_n |a_n|; CLN work in l^2_l.  For
# a vector supported on |n| <= N (2N+1 whole-line entries),
#
#     ||a||_{l^2_l} <= sqrt(2N+1) * max_n (l_n / w_n) * ||a||_w,
#
# and `kawahara_norm_conversion` returns that factor with every step rounded up.

_KAWAHARA_CLN = {
    "source": "Cadiot-Lessard-Nave arXiv:2302.12877 Thm 6.6 / ProofKawahara.jl",
    "T": 0.35, "c": 0.9, "N": 250, "d": 50.0,
    "r0_published": 2.27e-14,          # H^l(R) existence radius
    "r_uniqueness_published": 0.015,   # H^l(R) uniqueness ball
    "Y0_published": 2.26e-14,          # ||A F(u0)||_l
    "DFinv_published": 4.4,            # ||DF_e(u0)^{-1}||_{2,l}
}


class KawaharaProblem:
    """The finite Kawahara Galerkin system at CLN's published truncation.

    Float layer only: parameters, the symbol l, the folded multiplication matrix, the
    residual and its Jacobian, and a Newton solve seeded by the KdV soliton.  The
    enclosures live in `KawaharaIntervals`; this class is what that class treats as
    exact data.

    The seed is not arbitrary and it is a check in its own right.  Dropping the fourth
    derivative leaves u + lam1 u'' + lam3 u^2 = 0, whose sech^2 solution is

        u(x) = alpha sech^2(beta x),  beta^2 = -1/(4 lam1),  alpha = 6 lam1 beta^2/lam3,

    which at T = 0.35, c = 0.9 gives alpha = -0.2, beta = sqrt(3).  CLN's Figure 1
    shows u_0 with a minimum near -0.18: the seed lands on their picture before any
    Newton step, which is how the sign convention above was confirmed rather than
    guessed."""

    def __init__(self, N=250, d=50.0, T=0.35, c=0.9):
        self.N, self.d, self.T, self.c = int(N), float(d), float(T), float(c)
        self.n = self.N + 1
        self.lam1 = (1.0 - 3.0 * T) / (6.0 * (1.0 - c))
        self.lam2 = (19.0 - 30.0 * T - 45.0 * T ** 2) / (360.0 * (1.0 - c))
        self.lam3 = 3.0 / (4.0 * (1.0 - c))
        self.k = np.arange(self.n, dtype=float) * np.pi / self.d
        self.l = 1.0 - self.lam1 * self.k ** 2 + self.lam2 * self.k ** 4

    # -- the folded product ---------------------------------------------------
    def mult_matrix(self, a):
        """M(a): the matrix with (a*b) = M(a) b on even sequences truncated at N."""
        a = np.asarray(a, dtype=float)
        n = self.n
        ext = np.zeros(2 * n)
        ext[:n] = a                          # a_k = 0 for k > N
        idx = np.arange(n)
        diff = np.abs(idx[:, None] - idx[None, :])
        summ = idx[:, None] + idx[None, :]
        M = ext[diff] + ext[summ]
        M[:, 0] = a                          # the m = 0 column is not doubled
        return M

    def residual(self, a):
        a = np.asarray(a, dtype=float)
        return self.l * a + self.lam3 * (self.mult_matrix(a) @ a)

    def jacobian(self, a):
        return np.diag(self.l) + 2.0 * self.lam3 * self.mult_matrix(a)

    # -- the seed and the Newton solve ---------------------------------------
    def kdv_seed(self, n_quad=8192):
        """Even exponential coefficients of the KdV sech^2 soliton on Omega_0."""
        beta = np.sqrt(-1.0 / (4.0 * self.lam1))
        alpha = 6.0 * self.lam1 * beta ** 2 / self.lam3
        x = (np.arange(n_quad) / n_quad - 0.5) * (2.0 * self.d)
        u = alpha / np.cosh(beta * x) ** 2
        # a_n = (1/|Omega_0|) int u e^{-i n pi x/d}; the grid is uniform and u is even
        coef = np.fft.rfft(np.fft.ifftshift(u)) / n_quad
        return np.real(coef[: self.n])

    def newton(self, a0=None, tol=1e-15, maxit=60):
        a = self.kdv_seed() if a0 is None else np.array(a0, dtype=float)
        hist = []
        for _ in range(maxit):
            R = self.residual(a)
            hist.append(float(np.max(np.abs(R))))
            step = np.linalg.solve(self.jacobian(a), R)
            a = a - step
            if np.max(np.abs(step)) < tol * max(1.0, np.max(np.abs(a))):
                break
        hist.append(float(np.max(np.abs(self.residual(a)))))
        return a, hist

    def weight(self):
        """The norm's weight vector: exact float data, close to but not equal to l.

        Any positive vector defines a norm, so w carries no enclosure of its own --
        but the conversion to CLN's l^2_l norm then needs sup_n l_n / w_n, which
        `kawahara_norm_conversion` bounds rigorously rather than assuming it is 1."""
        return self.l.copy()


class KawaharaIntervals:
    """Interval enclosures of F and DF for `KawaharaProblem`.

    The coefficient vector a is exact float data.  The SYMBOL is not: lam1, lam2, lam3
    and pi are all inexact, so l_n is enclosed rather than read.  That is the only
    place widening enters the linear part, and it is why this class exists instead of
    a call to the float layer."""

    def __init__(self, problem):
        self.pr = problem
        self.n = self.N = problem.n

    def F_float(self, z):
        """The float64 residual l a + lam3 (a*a) -- the containment reference."""
        return np.asarray(self.pr.residual(np.asarray(z, dtype=float)), dtype=float)

    # -- the enclosed symbol --------------------------------------------------
    def _lam(self):
        from solver.interval import Interval as I
        T, c = I.point(self.pr.T), I.point(self.pr.c)
        one = I.point(1.0)
        lam1 = (one - I.point(3.0) * T) / (I.point(6.0) * (one - c))
        lam2 = ((I.point(19.0) - I.point(30.0) * T - I.point(45.0) * (T * T))
                / (I.point(360.0) * (one - c)))
        lam3 = I.point(3.0) / (I.point(4.0) * (one - c))
        return lam1, lam2, lam3

    def symbol(self):
        """Enclosure of l_n = 1 - lam1 k_n^2 + lam2 k_n^4, k_n = n pi / d."""
        from solver.interval import IPI, Interval as I
        lam1, lam2, _ = self._lam()
        idx = np.arange(self.pr.n, dtype=float)
        k = (IPI * I.point(idx)) / I.point(self.pr.d)
        k2 = k * k
        return I.point(np.ones(self.pr.n)) - lam1 * k2 + lam2 * (k2 * k2)

    # -- the pipeline's three hooks ------------------------------------------
    def F(self, z):
        """Enclosure of F(a). The quadratic term goes through the COMPENSATED matvec:
        at a Newton-converged iterate l_n a_n and lam3 (a*a)_n cancel to ~1e-16 of
        their own size, which is exactly the regime `matvec` loses and `dot2_matvec`
        does not (leg 50's lesson, re-used rather than re-learned)."""
        from solver.interval import Interval as I
        a = np.asarray(z, dtype=float)
        _, _, lam3 = self._lam()
        lin = self.symbol() * I.point(a)
        quad = dot2_matvec(self.pr.mult_matrix(a), a)
        return lin + lam3 * quad

    def jacobian(self, z):
        """(Jlo, Jhi) enclosing DF(a) = diag(l) + 2 lam3 M(a)."""
        from solver.interval import Interval as I
        a = np.asarray(z, dtype=float)
        _, _, lam3 = self._lam()
        M = self.pr.mult_matrix(a)
        two_lam3 = I.point(2.0) * lam3
        lo = np.minimum(two_lam3.lo * M, two_lam3.hi * M)
        hi = np.maximum(two_lam3.lo * M, two_lam3.hi * M)
        lo, hi = _down(lo), _up(hi)
        l = self.symbol()
        idx = np.arange(self.pr.n)
        lo[idx, idx] = _down(lo[idx, idx] + l.lo)
        hi[idx, idx] = _up(hi[idx, idx] + l.hi)
        return lo, hi

    def bilinear_bound(self, w, nu=None):
        """Rigorous bound on sup{ ||lam3 u*v||_w : ||u||_w, ||v||_w <= 1 }.

        ||u||_w <= 1 means |u_m| <= 1/w_m for every m in Z (w is even-extended), so

            |(u*v)_n| <= sum_{|m| <= N, |n-m| <= N} 1 / (w_{|m|} w_{|n-m|})

        and the bound is w_n times that, maximised over n.  Every step rounds up.
        `nu` is accepted for signature compatibility with the bordered classes and is
        not used: this problem has one field and one weight."""
        _, _, lam3 = self._lam()
        w = np.asarray(w, dtype=float)
        n = self.pr.n
        inv = _up(1.0 / w)
        ext = np.zeros(2 * n)                       # 1/w_k, zero for k > N
        ext[:n] = inv
        idx = np.arange(n)
        m = np.arange(-n + 1, n)
        d1 = ext[np.abs(m)]                         # 1/w_{|m|}
        diff = np.abs(idx[:, None] - m[None, :])
        d2 = np.where(diff < n, ext[np.minimum(diff, 2 * n - 1)], 0.0)
        s = _up(d2 @ d1)
        s = _up(s * (1.0 + _gamma(2 * n)))
        total = float(np.max(_up(w * s)))
        return float(_up(float(lam3.hi) * total))


def kawahara_norm_conversion(pr):
    """Rigorous factors taking a radius in ||.||_w to CLN's two published norms.

    Returns the multiplier `to_l2_l` such that ||a||_{l^2_l} <= to_l2_l * ||a||_w for
    a supported on |n| <= N -- that is sqrt(2N+1) * sup_n (l_n / w_n) -- and
    `to_Hl`, which multiplies by sqrt(|Omega_0|) to reach the function-space norm
    CLN quote r_0 in (their Thm 6.6 states the coefficient statement with the same
    sqrt(|Omega_0|) between them)."""
    iv = KawaharaIntervals(pr)
    l = iv.symbol()
    w = pr.weight()
    ratio = float(np.max(_up(np.asarray(l.hi) / w)))
    modes = 2 * pr.N + 1
    sq = _up(np.sqrt(float(modes)) * (1.0 + 2.0 ** -52))
    to_l2_l = float(_up(sq * ratio))
    to_Hl = float(_up(to_l2_l * _up(np.sqrt(2.0 * pr.d) * (1.0 + 2.0 ** -52))))
    return {"modes_whole_line": int(modes), "sup_l_over_w": ratio,
            "to_l2_l": to_l2_l, "to_Hl": to_Hl,
            "sqrt_Omega0": float(_up(np.sqrt(2.0 * pr.d) * (1.0 + 2.0 ** -52)))}


def kawahara_trace_rows(pr):
    """CLN's finite trace operator T^N_{4,e}, in this module's folded coefficients.

    CLN do not certify the Newton iterate.  They PROJECT it onto ker T^N_{4,e} first,
    so that its function representation lies in H^4_0(Omega_0) and can be extended by
    zero to the whole line -- the step that makes the periodic computation say
    anything about R at all.  For an even function the first and third derivatives
    already vanish at x = d, so two constraints remain: the value and the second
    derivative.  With mu_0 = 1, mu_n = 2 (the folding multiplicity),

        u(d)   = sum_n mu_n (-1)^n a_n,     u''(d) = -sum_n mu_n k_n^2 (-1)^n a_n.

    Returned as the 2 x (N+1) matrix of those two rows."""
    n = pr.n
    mu = np.full(n, 2.0)
    mu[0] = 1.0
    sgn = mu * (-1.0) ** np.arange(n)
    return np.vstack([sgn, sgn * pr.k ** 2])


def kawahara_trace_projection(pr, a):
    """The l^2_l-nearest point of ker T^N_{4,e} to a -- CLN's projection, replicated.

    Minimises sum_n mu_n l_n^2 (Delta_n)^2 subject to C(a + Delta) = 0, which is the
    change of smallest X^l norm.  Float only: this is an ABLATION on the iterate, and
    the iterate is exact data for the certificate whatever it is, so no enclosure of
    the projection itself is needed."""
    C = kawahara_trace_rows(pr)
    mu = np.full(pr.n, 2.0)
    mu[0] = 1.0
    ginv = 1.0 / (mu * pr.l ** 2)
    M = C @ (ginv[:, None] * C.T)
    lam = np.linalg.solve(M, -(C @ a))
    return a + ginv * (C.T @ lam)


def kawahara_certificate(N=250, d=50.0, T=0.35, c=0.9, A=None, trace_project=False):
    """Run the pipeline end to end on the Kawahara problem and convert to CLN's norms.

    No new certificate algebra: `interval_constants` and `radii_verdict` are the same
    functions that produced every other interval result in this repository.  The only
    new code is the enclosure class above, which is what the gate is about.

    `trace_project` replaces the Newton iterate by its projection onto ker T^N_{4,e},
    which is the iterate CLN actually certify.  It is an ablation and it can only make
    the certificate worse; it is here because it is the cheapest way to find out
    whether the gap to their radius is OUR arithmetic or THEIR extra step."""
    pr = KawaharaProblem(N=N, d=d, T=T, c=c)
    a, hist = pr.newton()
    if trace_project:
        a = kawahara_trace_projection(pr, a)
        hist = hist + [float(np.max(np.abs(pr.residual(a))))]
    iv = KawaharaIntervals(pr)
    w = pr.weight()
    consts = interval_constants(iv, a, w, w, A=A)
    verdict = radii_verdict(consts["Y0"], consts["Z1"], consts["Z2"])
    conv = kawahara_norm_conversion(pr)
    out = {"params": {"N": pr.N, "d": pr.d, "T": pr.T, "c": pr.c,
                      "lam1": pr.lam1, "lam2": pr.lam2, "lam3": pr.lam3},
           "float_residual_sup": hist[-1], "newton_history": hist,
           "constants": consts, "verdict": verdict, "conversion": conv,
           "trace_projected": bool(trace_project),
           "published": dict(_KAWAHARA_CLN), "coefficients": a}
    out["Y0_Hl"] = float(_up(consts["Y0"] * conv["to_Hl"]))
    if verdict["closes"]:
        out["r_min_w"] = verdict["r_min"]
        out["r_min_l2_l"] = float(_up(verdict["r_min"] * conv["to_l2_l"]))
        out["r_min_Hl"] = float(_up(verdict["r_min"] * conv["to_Hl"]))
        out["r_max_Hl"] = float(_down(verdict["r_max"] * conv["to_Hl"]))
    return out
