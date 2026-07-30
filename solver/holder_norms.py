"""Weighted-Holder norms: the TWO-GRADING space Route-D v3 + v4 jointly demanded.

The two previous legs each found half of the requirement.

  v3 (writeup/4_p2_lottery/TECHNICAL_P2_ROUTED_SPACES.md): a diagonal weight on
     Fourier coefficients measures SMOOTHNESS, and the far-field transport needs
     DECAY.  No weighted-ell^1 pair can carry the certificate.
  v4 (TECHNICAL_P2_ROUTED_V4.md): a weighted SUP norm measures decay, and it fixes
     the inverse -- but the Hilbert transform is unbounded on L^infinity, so the
     quadratic term is not controlled.  Smoothness is needed as well.

So the space must carry both gradings at once: a decay weight AND a smoothness
scale.  The classical setting where H IS bounded is Holder, so the candidate is

    ||h||_{alpha,gamma} = sup_j w^{(alpha)}_j |h_j|
                        + sup_{j != k} min(w^{(alpha-gamma)}_j, w^{(alpha-gamma)}_k)
                          |h_j - h_k| / |th_j - th_k|^gamma ,
    w^{(beta)} = (1 + X^2)^{beta/2} .

Note the seminorm carries the WEAKER weight alpha - gamma, not alpha.  That is
forced, not chosen (see below), and getting it wrong is not cosmetic: with weight
alpha the model profile f_alpha itself has infinite seminorm, so the space would
not even contain the objects the certificate is about.  The numerical conformal
check below is what caught that.

WHY THETA AND NOT X (the simplification that makes this cheap).  The natural
far-field Holder seminorm on the LINE is the conformal one, measured at the local
scale |X - Y| <~ (1+|X|):

    [h] = sup (1+X^2)^{(alpha+gamma)/2} |h(X) - h(Y)| / |X - Y|^gamma .

Under X = tan(theta/2), nearby points satisfy |X - Y| = |th - th'| (1+X^2)/2 +
O(...), so

    (1+X^2)^{(alpha+gamma)/2} |dh| / |dX|^gamma
        = 2^gamma (1+X^2)^{(alpha-gamma)/2} |dh| / |dth|^gamma ,

i.e. THE CONFORMALLY-WEIGHTED HOLDER SEMINORM IN X IS (up to 2^gamma) THE PLAIN
theta-HOLDER SEMINORM WITH WEIGHT alpha - gamma.  The compactified variable does
the far-field bookkeeping for free -- no local windows, no scale-dependent pair
selection, and the whole seminorm is one O(J^2) broadcast.  Sanity: for h = f_alpha
the expression is (alpha/2)(X dtheta)^{1-gamma}, bounded exactly where the grid
resolves the far field.  (`conformal_check` verifies the identity numerically; it
is what caught the wrong exponent in the first draft.)

WHAT IS EXACT HERE AND WHAT IS NOT.  The norms themselves are exact (a finite max
over grid pairs).  Induced OPERATOR norms between them are not: both norms are
polyhedral, so the induced norm is a linear program, and this project has no LP.
`family_op_norm` therefore reports a FAMILY-RESTRICTED norm -- a genuine LOWER
bound that includes the exact extremizers of the sup part -- and every caller must
say so.  Nothing in this module is an upper bound and nothing here is rigorous.
"""

import numpy as np


# ---------------------------------------------------------------------------
# the norms
# ---------------------------------------------------------------------------


def decay_weight(X, alpha):
    """w = (1 + X^2)^{alpha/2}: the decay grading, shared by both norm parts."""
    return (1.0 + np.asarray(X, dtype=float) ** 2) ** (0.5 * alpha)


class HolderNorm:
    """||h|| = sup w|h| + [h]_gamma, with the pair geometry cached per grid."""

    def __init__(self, theta, X, alpha, gamma, semi_alpha=None, sup_only=False):
        """`semi_alpha` overrides the seminorm weight exponent (default alpha-gamma).

        Pass semi_alpha=0 together with alpha=0 for a plain, unweighted Holder
        norm on the circle -- the right thing for pure smoothness questions about
        objects that do not decay at all (the square-wave adversary, for one:
        weighting a non-decaying function by (1+X^2)^{alpha/2} just measures the
        grid's outer radius).
        """
        self.theta = np.asarray(theta, dtype=float)
        self.X = np.asarray(X, dtype=float)
        self.alpha, self.gamma = float(alpha), float(gamma)
        self.sup_only = bool(sup_only)     # drop the seminorm (for consistency gates)
        self.semi_alpha = (alpha - gamma) if semi_alpha is None else float(semi_alpha)
        self.w = decay_weight(self.X, alpha)                       # sup part
        self.w_semi = decay_weight(self.X, self.semi_alpha)        # seminorm part
        d = np.abs(self.theta[:, None] - self.theta[None, :])
        np.fill_diagonal(d, np.inf)                    # exclude j == k
        self.inv_dist = d ** (-self.gamma)
        self.wmin = np.minimum(self.w_semi[:, None], self.w_semi[None, :])
        self.pair = self.wmin * self.inv_dist          # the seminorm kernel

    def sup_part(self, h):
        return float(np.max(self.w * np.abs(h)))

    def seminorm(self, h):
        if self.sup_only:
            return 0.0
        h = np.asarray(h, dtype=float)
        return float(np.max(self.pair * np.abs(h[:, None] - h[None, :])))

    def __call__(self, h):
        return self.sup_part(h) + self.seminorm(h)


def jacobian_identity_error(theta, n_near=3, resolved=0.1):
    """max relative deviation of dX/dtheta from its exact value (1 + X^2)/2.

    EXACT in the continuum: X = tan(theta/2) => dX/dtheta = (1/2) sec^2(theta/2)
    = (1 + X^2)/2.  On a grid the finite difference is only faithful where the
    grid RESOLVES the X-scale, i.e. where |X| dtheta <~ 1; at the outermost nodes
    consecutive points differ in X by a factor of order 2, so the difference
    quotient there is meaningless.  `resolved` sets the cutoff |X| dtheta <=
    resolved, and the returned pair is (worst deviation, largest resolved |X|).

    This is not a defect of the theta-seminorm -- which is a perfectly good
    discretization of the continuum theta-seminorm -- but a reminder that a
    compactified grid does not resolve the far field uniformly in X, the same
    limitation every other far-field measurement in this project carries.
    """
    theta = np.asarray(theta, dtype=float)
    X = np.tan(0.5 * theta)
    worst, xmax = 0.0, 0.0
    for off in range(1, int(n_near) + 1):
        dth = theta[off:] - theta[:-off]
        mid = 0.5 * (X[off:] + X[:-off])
        ok = np.abs(mid) * dth <= resolved
        if not ok.any():
            continue
        fd = (X[off:] - X[:-off])[ok] / dth[ok]
        worst = max(worst, float(np.max(np.abs(fd / (0.5 * (1.0 + mid[ok] ** 2)) - 1.0))))
        xmax = max(xmax, float(np.max(np.abs(mid[ok]))))
    return worst, xmax


def conformal_check(theta, gamma, n_near=3, resolved=0.1):
    """max deviation from 1 of the POINTWISE conformal ratio, over resolved pairs.

    The two seminorm integrands differ by a factor that is INDEPENDENT of h:

        [(1+X^2)^{(a+g)/2}|dh|/|dX|^g] / [2^g (1+X^2)^{(a-g)/2}|dh|/|dth|^g]
            = ( (1+X^2) dth / (2 dX) )^g ,

    i.e. the Jacobian identity raised to gamma, with alpha cancelling entirely.
    So the honest test is pointwise, not a ratio of maxima -- the two seminorms'
    maxima are attained at different pairs, and comparing them measures which pair
    wins rather than whether the identity holds.  Restricted to pairs the grid
    resolves (|X| dtheta <= `resolved`); see `jacobian_identity_error`.
    """
    err, xmax = jacobian_identity_error(theta, n_near=n_near, resolved=resolved)
    return abs((1.0 + err) ** float(gamma) - 1.0), xmax


# ---------------------------------------------------------------------------
# operator norms (family-restricted -- LOWER bounds, never upper)
# ---------------------------------------------------------------------------


def family_op_norm(A, dom_norm, cod_norm, extra=(), include_sup_extremizers=True):
    """max over a test family of ||A g||_dom / ||g||_cod.

    A LOWER bound on the induced norm, and only that.  The family contains the
    exact extremizers of the SUP part of the domain norm (for each domain index i
    the codomain vector g_j = sign(A_ij)/v_j, whose image maximizes w_i |(Ag)_i|),
    plus whatever `extra` supplies.

    It is NOT bounded below by the sup-to-sup induced norm, and expecting that was
    a mistake worth recording: those sign-pattern extremizers are wild, so their
    HOLDER norm is far larger than their sup norm, and dividing by it gives a much
    smaller ratio.  A stronger codomain norm makes the operator norm smaller; there
    is no ordering between the two induced norms.  With `sup_only` norms on both
    sides this function reproduces the exact sup-to-sup norm (test gate 6).
    """
    A = np.asarray(A, dtype=float)
    cands = []
    if include_sup_extremizers:
        v = cod_norm.w
        S = np.sign(A) / v[None, :]
        cands.extend(S[i] for i in range(A.shape[0]))
    cands.extend(np.asarray(g, dtype=float) for g in extra)
    best, arg = 0.0, -1
    for i, g in enumerate(cands):
        ng = cod_norm(g)
        if ng <= 0:
            continue
        r = dom_norm(A @ g) / ng
        if r > best:
            best, arg = r, i
    return best, arg


def square_wave_partial_sum(theta, m):
    """Degree-m Fourier partial sum of sign(cos theta): the L^infinity adversary.

    Bounded by ~1.18 (Gibbs) with a conjugate that grows like (2/pi) log m at the
    jump theta = pi/2 -- the construction that broke the pure sup pair in
    Route-D v4 W3.  Its Holder seminorm grows like m^gamma, which is exactly the
    point: in a Holder norm the adversary pays for its own oscillation.
    """
    theta = np.asarray(theta, dtype=float)
    j = np.arange((int(m) - 1) // 2 + 1)
    k = 2 * j + 1
    coef = (4.0 / np.pi) * (-1.0) ** j / k
    return np.cos(np.outer(theta, k)) @ coef


def holder_H_constant(theta, gamma, degrees=(4, 8, 16, 32, 64, 128, 256, 512),
                      n_random=200, seed=3):
    """[H p]_gamma / (||p||_inf + [p]_gamma) over the adversary + random families.

    On C^{0,gamma} the Hilbert transform IS bounded (unlike on L^infinity), with a
    constant that blows up as gamma -> 0 and gamma -> 1 -- so gamma has an interior
    optimum of its own, just as alpha does.  Returns (per_degree, random_best):
    the adversarial ratios by degree, and the best over random trig polynomials.
    """
    theta = np.asarray(theta, dtype=float)
    d = np.abs(theta[:, None] - theta[None, :])
    np.fill_diagonal(d, np.inf)
    ker = d ** (-float(gamma))

    def semi(f):
        return float(np.max(ker * np.abs(f[:, None] - f[None, :])))

    def sup(f):
        return float(np.max(np.abs(f)))

    k_all = np.arange(theta.size)
    Cm = np.cos(np.outer(theta, k_all))
    Sm = np.sin(np.outer(theta, k_all))

    per_deg = []
    for m in degrees:
        j = np.arange((int(m) - 1) // 2 + 1)
        kk = 2 * j + 1
        coef = (4.0 / np.pi) * (-1.0) ** j / kk
        p = np.cos(np.outer(theta, kk)) @ coef
        Hp = np.sin(np.outer(theta, kk)) @ coef
        per_deg.append(semi(Hp) / (sup(p) + semi(p)))

    rng = np.random.default_rng(seed)
    best = 0.0
    for _ in range(n_random):
        m = int(rng.integers(2, 64))
        a = rng.standard_normal(m + 1) / (1.0 + np.arange(m + 1)) ** rng.uniform(0.0, 1.5)
        p, Hp = Cm[:, :m + 1] @ a, Sm[:, :m + 1] @ a
        den = sup(p) + semi(p)
        if den > 0:
            best = max(best, semi(Hp) / den)
    return per_deg, float(best)
