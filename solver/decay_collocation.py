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


class DecayCollocationDomainError(ValueError):
    """Input outside the domain this module's construction is valid on.

    Raised instead of returning a number that LOOKS ordinary but was computed from a
    system the caller did not ask for.  Leg 115 (Route-DCA) measured three such sites;
    leg 151 (Route-DCR) closes them.  Naming follows the in-repo convention set by
    `solver.hilbert_pointwise.HilbertPointwiseDomainError` and
    `solver.nk_bounds.CertificateInputError` -- a `ValueError` subclass, so a caller
    catching `ValueError` (as `test_decay_collocation_adversarial.py` does for the
    out-of-range `drop` case) keeps working unchanged.
    """


def _require_real(alpha, where):
    """Reject a non-real `alpha`; return it untouched otherwise.

    G3 (leg 115).  `(1 + X^2) ** (0.5 * alpha)` with a complex `alpha` produces a complex
    array, which `float(np.max(...))` then truncates under NumPy's `ComplexWarning` -- a
    WARNING, not an exception, and suppressed by default.  Python's own `float()` raises
    `TypeError` on the identical input; this moves the module onto the stricter contract.
    The value is never converted or rounded here, so every real `alpha` -- Python `float`,
    Python `int`, NumPy scalar, or array -- flows through bit-for-bit unchanged.
    """
    if np.iscomplexobj(np.asarray(alpha)):
        raise DecayCollocationDomainError(
            "%s: alpha must be real, got %r. The decay class is X^{-alpha} and the weight "
            "(1+X^2)^{alpha/2} is only a norm weight for real alpha; a complex alpha is "
            "silently truncated by float() under NumPy's ComplexWarning and returns an "
            "ordinary-looking finite number computed from the wrong exponent." % (where, alpha)
        )
    return alpha


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
        _require_real(alpha, "Collocation.w_domain")
        return (1.0 + self.X ** 2) ** (0.5 * alpha)

    def w_codomain(self, alpha):
        """(1+X^2)^{(alpha+1)/2} -- one more power of decay, as the far field needs."""
        _require_real(alpha, "Collocation.w_codomain")
        return (1.0 + self.X ** 2) ** (0.5 * (alpha + 1.0))

    def norm_domain(self, h, alpha):
        return float(np.max(self.w_domain(alpha) * np.abs(h)))

    def norm_codomain(self, g, alpha):
        return float(np.max(self.w_codomain(alpha) * np.abs(g)))


def sup_op_norm(A, w_dom, w_cod):
    """Induced norm for sup norms: ||A|| = max_i w_dom_i sum_j |A_ij| / w_cod_j.

    (Rows of A are domain slots, columns codomain slots: A maps Y -> X.)

    G2 (leg 115).  The docstring states that axis convention but nothing used to check an
    argument against it, and `np.atleast_2d` turns a 1-D array of shape (n,) into (1, n) --
    a ROW, never a column, per NumPy's own documented and deliberate behaviour.  So a 1-D
    array intended as an (n, 1) column operator had its domain and codomain axes silently
    swapped: leg 115's worked case returned 12.0 where the intended reading gives 10.0, and
    30/30 of its randomized battery mismatched.  The guard below is a SHAPE INVARIANT rather
    than a 1-D special case: whatever was passed, after `atleast_2d` it must be exactly
    (len(w_dom), len(w_cod)).  That refuses the ambiguous 1-D input AND catches a transposed
    or mis-sized 2-D argument, which the previous code would have broadcast just as quietly.
    """
    A_in = np.asarray(A, dtype=float)
    A = np.atleast_2d(A_in)
    wd = np.asarray(w_dom)
    wc = np.asarray(w_cod)
    if wd.ndim != 1 or wc.ndim != 1:
        raise DecayCollocationDomainError(
            "sup_op_norm: w_dom and w_cod must each be 1-D weight vectors, got ndim "
            "%d and %d." % (wd.ndim, wc.ndim)
        )
    if A.shape != (wd.shape[0], wc.shape[0]):
        raise DecayCollocationDomainError(
            "sup_op_norm: A has shape %r (as passed: ndim %d, shape %r) but the weights "
            "require exactly (%d, %d) = (len(w_dom), len(w_cod)). Rows of A are domain "
            "slots and columns are codomain slots; a 1-D A is turned into a ROW (1, n) by "
            "numpy.atleast_2d, never a column, so passing a flat array as a column operator "
            "silently swaps the two axes instead of raising."
            % (A.shape, A_in.ndim, A_in.shape, wd.shape[0], wc.shape[0])
        )
    return float(np.max(wd * (np.abs(A) / wc[None, :]).sum(axis=1)))


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

    G1 (leg 115), and the predicate is NOT the one leg 115 prescribed.  Leg 115 asked for a
    raise "when `rows` is empty (i.e. J <= 1)".  Measured on the pre-repair module at J = 1
    over the five `drop` values leg 115's own test pins -- 0, 1, -1, 5, 100 -- `rows` is
    empty for exactly ONE of them (drop = 0) and has length 1 for the other four, yet all
    five return the identical 1.681792830507429.  Emptiness is therefore the wrong predicate:
    it would have left 4 of leg 115's own 5 cases still collapsing.

    The mechanism is the ASSIGNMENT TARGET, not the row list.  `M[1:, :]` has shape
    (J - 1, J), which at J = 1 is (0, 1); NumPy broadcasts a right-hand side of shape (1, 1)
    into a (0, 1) destination without complaint, because a length-1 axis broadcasts to ANY
    length including zero.  So the whole Jacobian -- NaN-poisoned or not -- is discarded and
    M is purely the gauge row, which reads only `col.to_coef` and so depends on neither `om`
    nor `c`.  Hence bit-identical output for every c in {0, 0.5, 1, 100, -50, 1e6, nan,
    +-inf} and for a NaN/Inf-poisoned nodal field.

    The guard is the SHAPE INVARIANT the construction actually needs:

        len(rows) == J - 1  and  J - 1 >= 1

    i.e. exactly one collocation row is deleted, and at least one survives.  Clause `J >= 2`
    catches (J=1, drop=0), which the length clause alone admits (0 == J - 1); clause
    `0 <= drop < J` catches (J=1, drop out of range), which is 4 of leg 115's 5.  Both are
    necessary.  At J >= 2 an out-of-range `drop` already raised ValueError from the shape
    mismatch; this only makes the refusal explicit and gives it a message, and
    DecayCollocationDomainError IS a ValueError, so callers catching that are unaffected.

    Note `drop = -1` does not mean "the last row" here and never did:
    `[j for j in range(J) if j != -1]` retains all J rows.  It is out of range, and is now
    named as such.
    """
    J = col.J
    if J < 2:
        raise DecayCollocationDomainError(
            "gauged_jacobian: J = %d leaves %d collocation rows after the gauge row "
            "replaces one, so the returned system is the gauge row ALONE -- it depends on "
            "neither `om` nor `c`, and every input (including NaN/Inf) returns the same "
            "number. At least one real collocation row is required, i.e. J >= 2." % (J, J - 1)
        )
    if not (isinstance(drop, (int, np.integer)) and 0 <= int(drop) < J):
        raise DecayCollocationDomainError(
            "gauged_jacobian: drop = %r is not a row of this grid; it must be an integer "
            "with 0 <= drop < J = %d. Negative values are NOT interpreted Python-style as "
            "counting from the end: `[j for j in range(J) if j != drop]` would retain all "
            "%d rows, one too many for the (%d, %d) assignment slot." % (drop, J, J, J - 1, J)
        )
    M = np.empty((J, J))
    M[0, :] = GAUGES[gauge](col)
    rows = [j for j in range(J) if j != drop]
    if len(rows) != J - 1:                       # invariant, not reachable via the guards above
        raise DecayCollocationDomainError(
            "gauged_jacobian: retained %d collocation rows, expected exactly J - 1 = %d."
            % (len(rows), J - 1)
        )
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
