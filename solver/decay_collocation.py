"""Spectral collocation of the gCLM two-scale operator in DECAY-GRADED sup norms.

Route-D v3 (writeup/4_p2_lottery/TECHNICAL_P2_ROUTED_SPACES.md) closed the whole
weighted-ell^1 category with a conservation law -- the two Newton-Kantorovich
requirements are separated by exactly one grading power and the separation cannot
be removed -- and identified the replacement: **decay-graded** spaces

    ||h||_X = sup_X (1+X^2)^{alpha/2} |h| ,   ||g||_Y = sup_X (1+X^2)^{(alpha+1)/2} |g| ,

in which both requirements hold at once.  v3 established that on the FAR-FIELD
MODEL operator L h = -c h_X - h/X, whose inverse has norm exactly 2/|alpha-2|.
That is a model: it drops the Hilbert-transform coupling, the compact core, and
the gauge.  This module carries the same measurement to the FULL operator.

WHY COLLOCATION AND NOT COEFFICIENTS.  The v2/v3 layer (solver/nk_fourier) works in
cosine coefficients, where the operator is exact and banded.  It cannot carry the
decay grading, and the reason is now understood: a function decaying exactly like
X^{-alpha} with non-integer alpha is only C^alpha at theta = pi (X = infinity), so
its coefficients decay like k^{-alpha-1} and no diagonal weight sees the decay at
all (v3 sec. 4).  A weighted SUP norm sees it directly.  So the natural
discretization for the graded pair is nodal, and that is what this module builds.

THE DISCRETIZATION.  Even functions on the midpoint grid

    theta_j = pi (j + 1/2) / J ,   j = 0..J-1    (avoids both endpoints),
    X_j = tan(theta_j / 2)                        (reaches |X| ~ 4J/pi),

represented exactly by their DCT-II cosine coefficients.  On that space

    H (cos k theta) = sin k theta                 (exact, unconditional)
    d/dtheta                                      (exact, spectral)
    f_X = (1 + cos theta) f_theta                 (exact)

so the linearization DF is assembled as a dense J x J matrix with NO quadrature
and no finite differences: it is the exact operator restricted to the space of
even trigonometric polynomials of degree < J.  `jacobian_matrix` agrees with the
independent coefficient-space build `solver.nk_fourier.jacobian` to rounding on
every band-limited input (test gate 2) -- the third independent construction of
the same operator in this project.

WHAT IS AND IS NOT BOUNDED HERE.  The discrete operator is exact on band-limited
functions; the true elements of the decay class are not band-limited, and the
resulting truncation error is the analogue of the Z1 tail term.  It is NOT bounded
in this module.  Everything here is a float rehearsal of the ONE question v3
leaves open at this stage -- is the full gauged inverse uniformly bounded in the
graded pair, and with what constant -- not a certificate.
"""

import numpy as np

C_ANCHOR = 0.5


# ---------------------------------------------------------------------------
# grid and transforms
# ---------------------------------------------------------------------------


def grid(J):
    """Midpoint theta-grid on (0, pi) and the matching X = tan(theta/2)."""
    th = np.pi * (np.arange(J) + 0.5) / J
    return th, np.tan(0.5 * th)


def transforms(J):
    """(to_coef, cos_eval, sin_eval) for even trig polys of degree < J.

    to_coef @ f  = cosine coefficients a_0..a_{J-1} of the interpolant of the
    nodal values f (DCT-II; exact for degree < J).
    cos_eval @ a = nodal values of sum a_k cos(k theta).
    sin_eval @ a = nodal values of sum a_k sin(k theta)  ( = H of the above ).
    """
    th, _ = grid(J)
    k = np.arange(J)
    Cm = np.cos(np.outer(th, k))
    Sm = np.sin(np.outer(th, k))
    scale = np.full(J, 2.0 / J)
    scale[0] = 1.0 / J
    to_coef = scale[:, None] * Cm.T
    return to_coef, Cm, Sm


class Collocation:
    """Cached operators on a fixed grid (build once, reuse -- the matrices are dense)."""

    def __init__(self, J):
        self.J = J
        self.theta, self.X = grid(J)
        self.to_coef, self.cos_eval, self.sin_eval = transforms(J)
        k = np.arange(J)
        self.H = self.sin_eval @ self.to_coef                 # Hilbert transform
        self.D = -(self.sin_eval * k[None, :]) @ self.to_coef  # d/dtheta
        self.transport = (1.0 + np.cos(self.theta))[:, None] * self.D   # d/dX

    # -- the objects ------------------------------------------------------
    def anchor(self):
        """Omega_2 = -(1+cos theta)/2 = -1/(1+X^2), nodal."""
        return -0.5 * (1.0 + np.cos(self.theta))

    def residual(self, om, c):
        """F(Omega, c) = Omega H(Omega) - c Omega_X, nodal."""
        return om * (self.H @ om) - c * (self.transport @ om)

    def jacobian_matrix(self, om, c):
        """DF = diag(H Omega) + diag(Omega) H - c (1+cos) d/dtheta."""
        return (np.diag(self.H @ om) + om[:, None] * self.H
                - c * self.transport)

    def dc_column(self, om):
        """dF/dc = -Omega_X, nodal."""
        return -(self.transport @ om)

    def quadratic(self, h):
        """The exact second-order remainder Q(h) = h H(h)  (F is quadratic)."""
        return h * (self.H @ h)

    # -- weighted sup norms ------------------------------------------------
    def w_domain(self, alpha):
        """(1+X^2)^{alpha/2} -- the domain weight of the decay class X^{-alpha}."""
        return (1.0 + self.X ** 2) ** (0.5 * alpha)

    def w_codomain(self, alpha):
        """(1+X^2)^{(alpha+1)/2} -- one more power of decay, as the far field needs."""
        return (1.0 + self.X ** 2) ** (0.5 * (alpha + 1.0))

    def norm_domain(self, h, alpha):
        return float(np.max(self.w_domain(alpha) * np.abs(h)))

    def norm_codomain(self, g, alpha):
        return float(np.max(self.w_codomain(alpha) * np.abs(g)))


def sup_op_norm(A, w_dom, w_cod):
    """Induced norm for sup norms: ||A|| = max_i w_dom_i sum_j |A_ij| / w_cod_j.

    (Rows of A are domain slots, columns codomain slots: A maps Y -> X.)
    """
    A = np.atleast_2d(np.asarray(A, dtype=float))
    return float(np.max(np.asarray(w_dom)
                        * (np.abs(A) / np.asarray(w_cod)[None, :]).sum(axis=1)))


# ---------------------------------------------------------------------------
# the gauged square system
# ---------------------------------------------------------------------------

GAUGES = {
    # Omega(X=0) = Omega(theta=0): the origin normalization (evaluated
    # spectrally, since theta = 0 is not a node of the midpoint grid)
    "origin": lambda col: col.to_coef.sum(axis=0),
    # the mean of Omega over theta = the a_0 coefficient
    "a0": lambda col: col.to_coef[0],
}


def gauged_jacobian(col, om, c, gauge="origin", drop=0):
    """[gauge row ; DF with one collocation row dropped] -- a square J x J system.

    Speed c is FIXED (gauge condition 1) and one scalar normalization replaces one
    collocation equation (gauge condition 2) -- the two conditions Route-D v1 Q2
    counted.  `drop` selects which collocation row the normalization replaces; the
    default drops the innermost node, where the residual is least informative
    about the far field.  Returns (M, w_cod_index) with row 0 the gauge row.
    """
    J = col.J
    M = np.empty((J, J))
    M[0, :] = GAUGES[gauge](col)
    rows = [j for j in range(J) if j != drop]
    M[1:, :] = col.jacobian_matrix(om, c)[rows, :]
    return M, rows


def graded_inverse_norm(col, alpha, gauge="origin", drop=0, c=C_ANCHOR):
    """||A||_{Y -> X} for the gauged inverse, in the decay-graded sup norms.

    The codomain slots are [gauge row (weight 1), collocation rows], the domain
    slots are nodal values of the profile correction.  This is the v3 far-field
    prediction 2/|alpha-2| carried to the FULL operator: Hilbert coupling, compact
    core and gauge included.
    """
    om = col.anchor()
    M, rows = gauged_jacobian(col, om, c, gauge=gauge, drop=drop)
    A = np.linalg.inv(M)
    w_dom = col.w_domain(alpha)
    w_cod = np.empty(col.J)
    w_cod[0] = 1.0
    w_cod[1:] = col.w_codomain(alpha)[rows]
    return sup_op_norm(A, w_dom, w_cod), A, M
