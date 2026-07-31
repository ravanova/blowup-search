"""The turning point at X_c: what actually makes the inverse diverge.

v12 found that the a > 0 two-scale profile ends at a finite radius X_c, where the
effective transport coefficient E(X) = c + a U(X) crosses zero, with an algebraic
zero of order 1/a; and it measured that the gauged inverse's graded norm DIVERGES
with J at that profile (J^+2.86 at a = 0.2) while it is flat at the a = 0 anchor
(J^-0.003).  It then attributed the divergence to a homogeneous mode

    h ~ (X_c - X)^{-1/a}                                          [WRONG]

and that attribution is wrong -- a sign dropped in converting d/dX to d/ds.  This
module carries the corrected analysis and the instrument that checks it.

--------------------------------------------------------------------------
THE CORRECTED LOCAL PICTURE
--------------------------------------------------------------------------
Beyond and around X_c the profile vanishes, so the linearization is

    L h = H(Omega) h - E h_X ,       E(X) ~ a h_c (X - X_c) ,  h_c = H(Omega)(X_c)

(both H(Omega) and E are FIXED functions of the profile; only h is unknown).  With
s = X_c - X, so h_X = -h_s and E = -a h_c s, the homogeneous equation reads

    h_c h - a h_c s h_s = 0    =>    h_s / h = 1/(a s)    =>    h ~ s^{1/a} ,

a mode that VANISHES at X_c rather than blowing up.  The inhomogeneous solve is
bounded there too: with the integrating factor s^{-1/a},

    h = s^{1/a} [ C - (1/(a h_c)) INT g sigma^{-1/a - 1} dsigma ]  ->  g(X_c)/(h_c)
        as s -> 0,

so nothing is singular AT the turning point.  v12's number is real; its stated
reason was not.

--------------------------------------------------------------------------
WHERE THE OBSTRUCTION ACTUALLY IS: THE FAR FIELD, NOT THE TURNING POINT
--------------------------------------------------------------------------
Outside X_c the same homogeneous equation has the same exponent, and now it is a
GROWING mode.  For X >> X_c,

    H(Omega) ~ m/(pi X)  (m = INT Omega < 0),
    E = c + a U ~ (a m / pi) log(X / X_c)          (E(X_c) = 0 by definition)
    =>  h_X / h = H(Omega)/E ~ 1 / (a X log(X/X_c))
    =>  h ~ ( log(X / X_c) )^{1/a} ,

which grows without bound.  The domain space of the whole Route-D programme is
the decay class |h| <~ X^{-alpha}.  A growing mode is not in it, and the constant
in front of it is fixed by matching to the inner solve rather than free, so
generically the image of the inverse LEAVES the space: one scalar compatibility
condition, i.e. a codimension-1 range obstruction of the continuum operator.  The
discrete inverse sees exactly that as a norm that grows as the grid's outer radius
(~ 4J/pi) grows.

So 1/a appears three times in one problem, in three different roles: the order of
the profile's zero at X_c, the exponent of the vanishing inner mode, and the power
of the logarithm by which the outer mode grows.

--------------------------------------------------------------------------
WHY THE CHEAP REPAIR DOES NOT WORK (state it before trying it)
--------------------------------------------------------------------------
The obvious move is to border the system with an extra unknown whose column
supplies the missing range direction, and the obvious candidate is the speed c,
which v12 froze.  It cannot work, and the reason is already in the project's
notes: dilation `Omega(X) -> Omega(X/mu)`, `c -> mu c` is a SYMMETRY of the zero
set at every a, so restoring c adds a KERNEL direction, not a range direction --
which is exactly why Route-D v1 Q2 and v11 V0 both found the one-gauge system
singular.  A symmetry cannot discharge a solvability condition.  `bordered_norm`
measures it anyway, because a prediction that is not measured is an opinion.

Plain float64.  Nothing here is interval-enclosed and nothing is rigorous.
"""

import numpy as np

from solver.collocation_newton import ACollocation, critical_radius, effective_speed, eval_matrices


def profile_far_field(col, om, c, X):
    """(H(Omega), E) of a collocation profile, evaluated at arbitrary X.

    Exact from the interpolant -- no quadrature, no differencing -- which is what
    makes this an instrument independent of the matrix inverse it is checking.
    """
    A = col.to_coef @ np.asarray(om, float)
    X = np.atleast_1d(np.asarray(X, float))
    th = 2.0 * np.arctan(X)
    _, Sm, Im = eval_matrices(th, col.J)
    return Sm @ A, effective_speed(X, Im @ A, c, col.a)


def homogeneous_far_field(col, om, c, X0=None, X_max=1e8, n=4001):
    """Integrate h_X = (H(Omega)/E) h outward from X0 > X_c; returns (X, h).

    The ODE is the linearization RESTRICTED to the region where the profile
    vanishes, so it is exactly the far-field mode the domain space has to contain.
    Integrated in log X (the coefficient is smooth there) with the trapezoid rule
    on the exponentiated quadrature -- the quantity of interest is a log-log slope,
    and gate 3 checks it against grid refinement rather than trusting the rule.
    """
    Xc = critical_radius(col.X, effective_speed(col.X, col.V @ om, c, col.a))
    if not np.isfinite(Xc):
        raise ValueError("no turning point: E does not change sign (a = 0?)")
    X0 = 1.5 * Xc if X0 is None else float(X0)
    X = np.exp(np.linspace(np.log(X0), np.log(X_max), int(n)))
    Hp, E = profile_far_field(col, om, c, X)
    f = Hp / E
    logh = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(X))])
    return X, np.exp(logh), Xc


def log_growth_exponent(X, h, Xc, tail=0.1):
    """d log h / d log log(X/X_c) over the outer `tail` fraction: predicted 1/a."""
    L = np.log(np.log(np.asarray(X, float) / Xc))
    y = np.log(np.asarray(h, float))
    k = int((1.0 - tail) * L.size)
    return float(np.polyfit(L[k:], y[k:], 1)[0])


def inner_mode_exponent(col, om, c, frac=(0.02, 0.2), n=2001):
    """Fitted p in h ~ (X_c - X)^p for the INNER homogeneous mode: predicted 1/a.

    Integrated inward from X_c(1 - frac[1]) toward X_c, which is the stable
    direction for this mode (it vanishes at X_c, so marching toward the turning
    point is contracting and the fit is insensitive to the starting amplitude).
    """
    Xc = critical_radius(col.X, effective_speed(col.X, col.V @ om, c, col.a))
    s = np.linspace(frac[1] * Xc, frac[0] * Xc, int(n))        # decreasing s
    X = Xc - s
    Hp, E = profile_far_field(col, om, c, X)
    f = Hp / E                                                  # = d log h / dX
    logh = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(X))])
    return float(np.polyfit(np.log(s), logh, 1)[0]), Xc


# ---------------------------------------------------------------------------
# the operator norms, and where they come from
# ---------------------------------------------------------------------------


def gauged_matrix(col, om, c, drop=0):
    J = col.J
    g0 = col.to_coef.sum(axis=0)
    keep = [j for j in range(J) if j != drop]
    M = np.empty((J, J))
    M[0, :] = g0
    M[1:, :] = col.jacobian_a(om, c)[keep, :]
    return M, keep


def graded_norm_by_radius(col, om, c, alpha, cutoffs=(20.0, 50.0, 200.0, np.inf)):
    """||A|| with the DOMAIN sup restricted to X <= cutoff, for each cutoff.

    The point of the restriction: the grid's own outer radius is ~ 4J/pi, so it
    grows with J.  If the divergence is the far-field mode leaving the space, the
    unrestricted norm grows fast and the restricted ones grow much more slowly.
    Attributing a divergence to a mechanism means separating those.
    """
    M, keep = gauged_matrix(col, om, c)
    A = np.linalg.inv(M)
    w_dom = (1.0 + col.X ** 2) ** (0.5 * alpha)
    w_cod = np.empty(col.J)
    w_cod[0] = 1.0
    w_cod[1:] = ((1.0 + col.X ** 2) ** (0.5 * (alpha + 1.0)))[keep]
    rows = w_dom * (np.abs(A) / w_cod[None, :]).sum(axis=1)
    out = {}
    for X0 in cutoffs:
        m = col.X <= X0
        out["%g" % X0] = float(rows[m].max()) if m.any() else float("nan")
    sv = np.linalg.svd(M, compute_uv=False)
    return {"by_cutoff": out,
            "argmax_X": float(col.X[int(np.argmax(rows))]),
            "unweighted_row_sum": float(np.abs(A).sum(axis=1).max()),
            "cond": float(sv[0] / sv[-1]), "smin": float(sv[-1])}


def source_of_the_row(col, om, c, alpha):
    """Fraction of the extremal row's mass coming from codomain slots near X_c."""
    M, keep = gauged_matrix(col, om, c)
    A = np.linalg.inv(M)
    w_dom = (1.0 + col.X ** 2) ** (0.5 * alpha)
    w_cod = np.empty(col.J)
    w_cod[0] = 1.0
    w_cod[1:] = ((1.0 + col.X ** 2) ** (0.5 * (alpha + 1.0)))[keep]
    i = int(np.argmax(w_dom * (np.abs(A) / w_cod[None, :]).sum(axis=1)))
    contrib = w_dom[i] * np.abs(A[i]) / w_cod
    Xj = np.concatenate([[np.nan], col.X[keep]])
    Xc = critical_radius(col.X, effective_speed(col.X, col.V @ om, c, col.a))
    near = np.isfinite(Xj) & (np.abs(Xj - Xc) <= 0.1 * Xc)
    return {"row_X": float(col.X[i]), "Xc": float(Xc),
            "near_Xc_fraction": float(contrib[near].sum() / contrib.sum())}


def bordered_norm(col, om, c, alpha):
    """||A|| for the system with the speed RESTORED as an unknown.

    Predicted (see the module docstring) not to help, because dilation is a
    symmetry: restoring c adds kernel, not range.  Unknowns (Omega, c); equations
    two gauge rows plus all J residual rows; the pseudo-inverse stands in for A
    because the system is overdetermined by one.
    """
    J = col.J
    g0 = col.to_coef.sum(axis=0)
    i1 = int(np.argmin(np.abs(col.X - 1.0)))
    M = np.zeros((J + 2, J + 1))
    M[0, :J] = g0
    M[1, i1] = 1.0
    M[2:, :J] = col.jacobian_a(om, c)
    M[2:, J] = col.dc_column_a(om)
    A = np.linalg.pinv(M)
    wc = (1.0 + col.X ** 2) ** (0.5 * (alpha + 1.0))
    w_cod = np.concatenate([[1.0, 1.0], wc])
    w_dom = np.concatenate([(1.0 + col.X ** 2) ** (0.5 * alpha), [1.0]])
    return float(np.max(w_dom * (np.abs(A) / w_cod[None, :]).sum(axis=1)))


def square_bordered_smin(col, om, c):
    """Smallest singular value of the SQUARE bordered system [gauge ; DF | dF/dc].

    At a = 0 this must be (numerically) singular -- dilation is an exact symmetry
    of the zero set and one gauge cannot pin two directions.  That is v11 V0's
    finding read forward, and it is the cheapest demonstration that the speed is
    the wrong thing to border with.
    """
    J = col.J
    g0 = col.to_coef.sum(axis=0)
    M = np.zeros((J + 1, J + 1))
    M[0, :J] = g0
    M[1:, :J] = col.jacobian_a(om, c)
    M[1:, J] = col.dc_column_a(om)
    sv = np.linalg.svd(M, compute_uv=False)
    return float(sv[-1]), float(sv[0] / sv[-1])


def solved_profile(J, a, c=0.5):
    """Convenience: the Newton profile in the certificate's gauged system."""
    col = ACollocation(J, a=a)
    return col, col.newton_gauged(c=c)["Omega"], c
