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

INPUT VALIDATION (added by the leg-100 bench repair; see `_reject_nonfinite`).
Leg 100 measured this module answering CONFIDENTLY AND WRONGLY on non-finite and
degenerate input, in seven places, all one hazard: **an ordered comparison used as
a filter silently DROPS a NaN candidate instead of propagating it**, because
IEEE-754 makes every NaN compare unordered.  The sharpest measured case was a
2.1053x understated operator-norm lower bound; the most alarming was
`conformal_check` -- the module's OWN self-validation routine -- returning a
bit-identical "clean" 1.517287054473293e-04 on a NaN-poisoned grid, and (0.0, 0.0),
i.e. EXACT conformal agreement, on a grid of pure NaN.  Every public entry point
below now rejects non-finite and degenerate arguments with a `ValueError` before
any such comparison runs.  The rule the repair follows throughout:

    a filter may drop a candidate only for a reason it can STATE; it may never
    drop one merely because a comparison against NaN was False.

The two propagating reductions are deliberately left alone: `HolderNorm.sup_part`
and `.seminorm` reduce the CALLER'S DATA VECTOR `h` through `np.max`, which
propagates NaN honestly, and validating `h` on every call would put an O(J^2)
scan inside `family_op_norm`'s inner loop to replace a correct answer.
"""

import numpy as np


# ---------------------------------------------------------------------------
# input validation -- the guard leg 100 measured the absence of
# ---------------------------------------------------------------------------


def _reject_nonfinite(name, value, what):
    """Reject a non-finite scalar argument, by name, BEFORE it is ever compared.

    Leg 100 (Route-HNA) measured what this closes.  Every filter in this module is a
    bare ordered comparison -- `|mid| * dth <= resolved`, `if ng <= 0`, `if r > best`,
    `if den > 0` -- and IEEE-754 says every NaN compares unordered, so each one
    evaluates False on a poisoned candidate and DISCARDS it.  The discard is total:
    no NaN in the result, no warning, no exception, and no field in the return value
    recording that anything was dropped.  What comes back is the max over the
    survivors, which is a real number computed from a subset the caller never chose --
    a 2.1053x understatement in the measured worst case, and 0.0 (the value that means
    "exact agreement", or "the Hilbert transform annihilates this space") in four
    others.  Refusing the input is the only honest option: a filter that cannot fire
    is not a filter, and a criterion that silently stops existing is worse than one
    that says it cannot be applied.
    """
    v = float(value)
    if not np.isfinite(v):
        raise ValueError(
            "%s = %r is not finite. %s Every filter in solver/holder_norms.py is an "
            "ordered comparison, and IEEE-754 makes every comparison against NaN "
            "False, so a non-finite value here is SILENTLY DROPPED rather than "
            "propagated -- the returned number is then a maximum over an unannounced "
            "subset (leg 100 measured 2.1053x understatement, and 0.0 reported as "
            "exact agreement)." % (name, v, what))
    return v


def _reject_nonfinite_array(name, arr, what):
    """Same, for an array argument: reject if ANY entry is non-finite."""
    a = np.asarray(arr, dtype=float)
    bad = ~np.isfinite(a)
    n_bad = int(bad.sum())
    if n_bad:
        idx = np.flatnonzero(bad.ravel())
        raise ValueError(
            "%s has %d non-finite entr%s (flat index %s%s; first bad value %r) out of "
            "%d. %s A single non-finite entry is enough: leg 100 measured ONE NaN grid "
            "node leaving conformal_check bit-identical to its clean value "
            "(1.517287054473293e-04), and ONE NaN operator entry collapsing "
            "family_op_norm from 661.207572 to exactly 0.0." %
            (name, n_bad, "y" if n_bad == 1 else "ies",
             ", ".join(str(int(i)) for i in idx[:4]),
             ", ..." if n_bad > 4 else "",
             float(a.ravel()[idx[0]]), a.size, what))
    return a


def _reject_nonpositive_gamma(gamma):
    """The Holder exponent must be finite and strictly positive.

    `gamma <= 0` is not a Holder exponent and does not define a seminorm: the kernel
    `|th_j - th_k|^{-gamma}` stops decaying in the separation, so the "seminorm" no
    longer measures smoothness at all.  Leg 100 measured `gamma = -0.3` as one of the
    four degenerate inputs on which `holder_H_constant`'s random arm returns exactly
    0.0 against a clean 0.891421 -- i.e. reports that the Hilbert transform annihilates
    the Holder space.  Every gamma used anywhere in this repository lies in
    [0.05, 0.9]; no upper bound is imposed here, only positivity.
    """
    g = _reject_nonfinite("gamma", gamma, "It is the Holder (smoothness) exponent.")
    if g <= 0.0:
        raise ValueError(
            "gamma = %r is not a Holder exponent: gamma > 0 is required. At gamma <= 0 "
            "the kernel |th_j - th_k|^{-gamma} does not decay in the separation, so the "
            "seminorm measures no smoothness. Leg 100 measured gamma = -0.3 returning "
            "an embedding constant of exactly 0.0 against a clean 0.891421." % g)
    return g


def _reject_repeated_nodes(name, d, size):
    """Reject a grid with a repeated node, given the pair-distance matrix `d`.

    `d` must already carry `np.inf` on its diagonal.  A repeated node is an
    off-diagonal zero, and `0 ** (-gamma)` is `+inf`, so the seminorm kernel acquires
    an infinite entry and the seminorm becomes `inf * 0 = nan` for any two components
    that happen to agree there.  The same repetition in `jacobian_identity_error`
    gives `dth = 0` and a `0/0` finite difference -- measured below.
    """
    if not np.all(d > 0.0):
        n_pairs = int((d <= 0.0).sum()) // 2
        raise ValueError(
            "%s contains a REPEATED node: %d off-diagonal pair%s among %d nodes have "
            "separation exactly 0. The seminorm kernel is |th_j - th_k|^{-gamma}, so a "
            "repeated node makes it +inf and the seminorm inf * 0 = nan. Leg 100's "
            "hazard then applies directly: the builtin `max` discards that nan and "
            "returns the max over the surviving pairs as though nothing happened."
            % (name, n_pairs, "" if n_pairs == 1 else "s", size))


# ---------------------------------------------------------------------------
# the norms
# ---------------------------------------------------------------------------


def decay_weight(X, alpha):
    """w = (1 + X^2)^{alpha/2}: the decay grading, shared by both norm parts.

    `alpha` and every entry of `X` must be finite.  This is not defensive
    boilerplate: leg 100 measured `decay_weight([0, 1, 10], alpha=nan)` returning
    `[1.0, nan, nan]`, because IEEE-754 mandates `pow(1.0, x) == 1.0` even for
    `x = NaN`, so the grid node `X = 0` keeps an exactly-UNIT weight under a wholly
    invalid grading exponent.  That was latent only because the sup over the grid
    still saw the other NaNs; it goes live the moment anything evaluates the weight
    at a single origin node.  It is refused here rather than left to decay at the
    rate of memory.
    """
    a = _reject_nonfinite(
        "alpha", alpha,
        "It is the decay grading exponent of the weight (1 + X^2)^{alpha/2}.")
    Xa = _reject_nonfinite_array(
        "X", X, "It is the compactified grid the weight is evaluated on.")
    return (1.0 + Xa ** 2) ** (0.5 * a)


class HolderNorm:
    """||h|| = sup w|h| + [h]_gamma, with the pair geometry cached per grid."""

    def __init__(self, theta, X, alpha, gamma, semi_alpha=None, sup_only=False):
        """`semi_alpha` overrides the seminorm weight exponent (default alpha-gamma).

        Pass semi_alpha=0 together with alpha=0 for a plain, unweighted Holder
        norm on the circle -- the right thing for pure smoothness questions about
        objects that do not decay at all (the square-wave adversary, for one:
        weighting a non-decaying function by (1+X^2)^{alpha/2} just measures the
        grid's outer radius).

        VALIDATION.  `theta` and `X` must be finite, equal-length and free of
        repeated nodes; `alpha` and `semi_alpha` must be finite; `gamma` must be
        finite and > 0.  Leg 100 measured every one of these poisonings reaching
        the caller as a NaN total norm rather than as an error -- honest, but only
        because the reductions here happen to be `np.max`.  The SAME poisoned grid
        is invisible to `conformal_check`, which filters instead of maximising, so
        the grid is rejected at the door instead of relying on which reduction a
        given consumer happens to use.
        """
        self.theta = _reject_nonfinite_array(
            "theta", theta, "It is the circle grid the seminorm's pair geometry is "
            "built from.")
        self.X = _reject_nonfinite_array(
            "X", X, "It is the compactified grid the decay weight is built from.")
        if self.theta.ndim != 1 or self.X.ndim != 1:
            raise ValueError(
                "theta and X must be 1-D grids; got theta.ndim = %d, X.ndim = %d."
                % (self.theta.ndim, self.X.ndim))
        if self.theta.size != self.X.size:
            raise ValueError(
                "theta and X describe the same grid in two coordinates and must have "
                "equal length; got %d and %d. A mismatch silently pairs the seminorm "
                "kernel (built from theta) with the wrong decay weights (built from X)."
                % (self.theta.size, self.X.size))
        self.alpha = _reject_nonfinite(
            "alpha", alpha, "It is the decay grading exponent of the sup part.")
        self.gamma = _reject_nonpositive_gamma(gamma)
        self.sup_only = bool(sup_only)     # drop the seminorm (for consistency gates)
        self.semi_alpha = (self.alpha - self.gamma) if semi_alpha is None else \
            _reject_nonfinite("semi_alpha", semi_alpha,
                              "It is the seminorm's decay grading exponent, which "
                              "defaults to the FORCED value alpha - gamma.")
        self.w = decay_weight(self.X, self.alpha)                  # sup part
        self.w_semi = decay_weight(self.X, self.semi_alpha)        # seminorm part
        d = np.abs(self.theta[:, None] - self.theta[None, :])
        np.fill_diagonal(d, np.inf)                    # exclude j == k
        _reject_repeated_nodes("theta", d, self.theta.size)
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

    VALIDATION, and why this function needed the most of it (leg 100).  Three of
    the module's measured silent-corruption cases live here, and all three come
    from the pair `ok = |mid| * dth <= resolved` / `worst, xmax = 0.0, 0.0`:

      * a NaN grid node makes `ok` False at the poisoned pairs, so they are DROPPED
        and the returned deviation is bit-identical to the clean grid's
        (5.058518860e-04 on 128 nodes) -- this routine is the module's own
        self-validation, so a broken grid is exactly what its filter discards;
      * an all-NaN grid empties `ok` at every offset, `continue`s past all of them,
        and returns the untouched initialiser `(0.0, 0.0)` -- and 0.0 is the value
        that means EXACT agreement, so a grid on which nothing was checked is
        indistinguishable from one that passed perfectly;
      * `worst = max(worst, ...)` is python's BUILTIN `max`, which returns its first
        argument when the second is NaN. The repair pass measured a seventh case
        leg 100 had not separated out: a single REPEATED node gives `dth = 0` and a
        0/0 finite difference at offset 1, whose contribution is NaN, whose discard
        by `max(0.0, nan)` silently deletes the finest and most informative offset
        from the maximum -- 5.058518860e-04 becomes 8.127828757e-04, a 1.6068x
        change, finite and plausible and carrying no tell.

    So: `theta` must be finite and STRICTLY INCREASING (the finite differences are
    signed, and a descending grid makes `dth < 0`, which passes `|mid| * dth <=
    resolved` unconditionally and thereby switches the resolution restriction off
    altogether -- measured: reported coverage |X| <= 1019.81 against a true 1.9095,
    a 534.1x overstatement of the range actually verified). At least one pair must
    survive the resolution filter, and every offset's contribution must be finite.
    """
    theta = _reject_nonfinite_array(
        "theta", theta, "It is the grid whose Jacobian identity is being checked.")
    if theta.ndim != 1:
        raise ValueError("theta must be a 1-D grid; got ndim = %d." % theta.ndim)
    n_near = int(n_near)
    if n_near < 1:
        raise ValueError(
            "n_near = %d must be >= 1: it is the number of near-neighbour offsets the "
            "finite difference is taken over, and 0 offsets check nothing while "
            "returning the initialiser (0.0, 0.0), which reads as exact agreement."
            % n_near)
    if theta.size <= n_near:
        raise ValueError(
            "theta has %d nodes but n_near = %d: every offset would produce an empty "
            "difference, and the function would return (0.0, 0.0) -- exact agreement -- "
            "having checked nothing." % (theta.size, n_near))
    resolved = _reject_nonfinite(
        "resolved", resolved,
        "It is the cutoff |X| dtheta <= resolved selecting the pairs the grid resolves.")
    if resolved <= 0.0:
        raise ValueError(
            "resolved = %r must be > 0: it is the resolution cutoff |X| dtheta <= "
            "resolved, and a non-positive cutoff admits no pair at all, returning the "
            "initialiser (0.0, 0.0) -- the value that means exact agreement." % resolved)

    dth1 = np.diff(theta)
    if not np.all(dth1 > 0.0):
        n_bad = int((dth1 <= 0.0).sum())
        raise ValueError(
            "theta must be STRICTLY INCREASING; %d of %d consecutive gaps are <= 0 "
            "(minimum gap %r). The finite differences here are signed, so a repeated "
            "node gives dth = 0 and a 0/0 quotient (whose NaN the builtin `max` then "
            "discards, deleting a whole offset from the maximum: leg 100's repair "
            "measured 5.058518860e-04 -> 8.127828757e-04, 1.6068x), and a descending "
            "grid gives dth < 0, which satisfies |mid| * dth <= resolved for EVERY "
            "pair and so switches the resolution restriction off entirely (measured: "
            "reported coverage |X| <= 1019.81 against a true 1.9095, 534.1x)."
            % (n_bad, dth1.size, float(dth1.min())))

    X = np.tan(0.5 * theta)
    _reject_nonfinite_array(
        "X = tan(theta/2)", X,
        "The compactified image of theta is not finite, so theta has a node at an odd "
        "multiple of pi where tan blows up.")

    worst, xmax, n_checked = 0.0, 0.0, 0
    for off in range(1, n_near + 1):
        dth = theta[off:] - theta[:-off]
        mid = 0.5 * (X[off:] + X[:-off])
        ok = np.abs(mid) * dth <= resolved
        if not ok.any():
            continue
        fd = (X[off:] - X[:-off])[ok] / dth[ok]
        dev = float(np.max(np.abs(fd / (0.5 * (1.0 + mid[ok] ** 2)) - 1.0)))
        span = float(np.max(np.abs(mid[ok])))
        # Never let a non-finite contribution be dropped by an ordered comparison:
        # `max(0.0, nan)` is 0.0, which would delete this entire offset in silence.
        if not (np.isfinite(dev) and np.isfinite(span)):
            raise ValueError(
                "offset %d produced a non-finite contribution (deviation %r over %d "
                "resolved pairs, |X| span %r) from finite, strictly increasing input. "
                "Refusing to return: python's builtin `max` would drop it and report "
                "the maximum over the remaining offsets as though this one had been "
                "checked." % (off, dev, int(ok.sum()), span))
        worst = max(worst, dev)
        xmax = max(xmax, span)
        n_checked += int(ok.sum())

    if n_checked == 0:
        raise ValueError(
            "no pair of the %d supplied nodes is resolved at the cutoff |X| dtheta <= "
            "%r, so NOTHING was checked. The pre-repair code returned the initialiser "
            "(0.0, 0.0) here, which is the value that means EXACT agreement with the "
            "conformal identity -- leg 100's worst case: maximally uninformative input, "
            "maximally reassuring output. Refine the grid or raise `resolved`."
            % (theta.size, resolved))
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

    THIS FUNCTION IS THE MODULE'S SELF-VALIDATION GATE -- the docstring at the top
    of the module credits it with catching a wrong seminorm exponent in the first
    draft -- and leg 100 measured that before the repair it could not detect a broken
    grid at all, because a broken grid is exactly what its filter discarded: on 128
    nodes with theta[7], theta[64] or theta[120] set to NaN it returned
    1.517287054473293e-04, bit-identical to the clean grid, deviation exactly 0.0,
    no NaN, no warning, no exception.  `gamma` is validated here and the grid is
    validated in `jacobian_identity_error`, which now raises rather than filtering.
    """
    g = _reject_nonpositive_gamma(gamma)
    err, xmax = jacobian_identity_error(theta, n_near=n_near, resolved=resolved)
    ratio = abs((1.0 + err) ** g - 1.0)
    if not np.isfinite(ratio):
        raise ValueError(
            "the conformal ratio deviation is %r, computed as |(1 + %r)^%r - 1| from a "
            "validated grid. Refusing to return a non-finite self-validation verdict."
            % (ratio, err, g))
    return ratio, xmax


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

    VALIDATION (leg 100).  Both of this function's guards -- `if ng <= 0: continue`
    and `if r > best` -- are ordered comparisons, so before the repair EVERY
    non-finite candidate was rejected by both and control fell through to the
    initialiser `best, arg = 0.0, -1`.  The two measured consequences:

      * one NaN anywhere in a 48x48 operator turned 661.207572 into exactly 0.0, a
        100% collapse returned as a legitimate finite LOWER bound and numerically
        indistinguishable from the answer for the zero operator; the only trace was
        the `arg = -1` sentinel, which no caller in this repository inspects;
      * the sharpest case in the whole battery -- a poisoned TRUE MAXIMIZER was
        dropped and the runner-up reported as the answer: 221.978372 became
        105.435714, a 2.1053x UNDERSTATEMENT of a quantity that is only ever used as
        a lower bound, finite, plausible, with `arg` pointing at a perfectly
        legitimate clean test vector and nothing in the return value recording that
        a test function had been discarded at all.

    `A`, every vector in `extra`, and the codomain sup weights are therefore checked
    up front, and each candidate's norm and ratio are checked before they meet a
    comparison.  `ng <= 0` survives as a filter because it now has a reason it can
    STATE: a test vector of norm zero carries no information about the operator, and
    the all-zero operator legitimately returns `(0.0, -1)`.
    """
    A = _reject_nonfinite_array(
        "A", A, "It is the operator whose family-restricted lower bound is wanted.")
    if A.ndim != 2:
        raise ValueError("A must be a 2-D operator; got ndim = %d." % A.ndim)
    cands = []
    if include_sup_extremizers:
        v = _reject_nonfinite_array(
            "cod_norm.w", cod_norm.w,
            "It is the codomain sup weight the exact sup-part extremizers divide by.")
        if not np.all(v > 0.0):
            raise ValueError(
                "cod_norm.w has %d non-positive entries (minimum %r); the sup-part "
                "extremizers are sign(A_ij) / w_j, so a zero weight makes the test "
                "vector infinite and a negative one flips its sign."
                % (int((v <= 0.0).sum()), float(v.min())))
        S = np.sign(A) / v[None, :]
        cands.extend(S[i] for i in range(A.shape[0]))
    for j, g in enumerate(extra):
        cands.append(_reject_nonfinite_array(
            "extra[%d]" % j, g,
            "It is a caller-supplied test vector. Before this check a poisoned test "
            "vector was silently discarded and the runner-up reported as the answer "
            "(measured: 221.978372 -> 105.435714, 2.1053x understated)."))
    best, arg = 0.0, -1
    for i, g in enumerate(cands):
        ng = cod_norm(g)
        if not np.isfinite(ng):
            raise ValueError(
                "candidate %d of %d has non-finite codomain norm %r from validated "
                "inputs. Refusing to continue: `if ng <= 0` is an ordered comparison "
                "and would DISCARD this candidate, silently shrinking the family the "
                "reported lower bound is a maximum over." % (i, len(cands), ng))
        if ng <= 0:
            continue                       # no information: a zero test vector
        r = dom_norm(A @ g) / ng
        if not np.isfinite(r):
            raise ValueError(
                "candidate %d of %d has non-finite ratio %r (codomain norm %r) from "
                "validated inputs. Refusing to continue: `if r > best` would DISCARD "
                "it and report the maximum over the survivors as the lower bound."
                % (i, len(cands), r, ng))
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
    theta = _reject_nonfinite_array(
        "theta", theta, "It is the grid the partial sum is sampled on.")
    m_f = _reject_nonfinite(
        "m", m, "It is the Fourier truncation degree of the square-wave adversary.")
    if m_f < 1:
        raise ValueError(
            "m = %r must be >= 1: it is the degree of the partial sum, and a "
            "non-positive degree returns the empty sum silently." % m_f)
    j = np.arange((int(m_f) - 1) // 2 + 1)
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

    VALIDATION (leg 100).  This function's two arms DISAGREED about whether their
    shared input was valid, which is what made the silence here a trap rather than
    an obvious bug.  The per-degree arm is a plain list comprehension with no filter,
    so it propagates: it returned all-NaN on each of {NaN grading exponent,
    gamma = -0.3, NaN grid node, Inf grid node}.  The random arm, on the same four
    inputs, returned exactly **0.0** against a clean 0.891421 -- i.e. it reported
    that the Hilbert transform ANNIHILATES the Holder space, the most consequential
    wrong answer this module can give.  Cause: `if den > 0` rejects a NaN denominator,
    and `max(best, x)` is python's BUILTIN max, which returns `best` when `x` is NaN
    (`nan > best` is False), so `best` never left its 0.0 initialiser.  A caller
    reading the first return value was protected; one reading the second was not.

    The random family draws degrees up to 63 and contracts against a (J x J) basis,
    so it needs `theta.size >= 64` -- a precondition that was previously enforced
    only incidentally, by a numpy shape error, and documented nowhere.  It is stated
    and checked here.
    """
    theta = _reject_nonfinite_array(
        "theta", theta, "It is the grid the Holder seminorm kernel is built from.")
    if theta.ndim != 1:
        raise ValueError("theta must be a 1-D grid; got ndim = %d." % theta.ndim)
    gamma = _reject_nonpositive_gamma(gamma)
    degrees = tuple(degrees)
    for k, m in enumerate(degrees):
        m_f = _reject_nonfinite("degrees[%d]" % k, m,
                                "It is an adversarial Fourier truncation degree.")
        if m_f < 1:
            raise ValueError(
                "degrees[%d] = %r must be >= 1: it is a truncation degree, and a "
                "non-positive one contributes an empty sum whose ratio is 0/0."
                % (k, m_f))
    n_random = int(n_random)
    if n_random < 0:
        raise ValueError("n_random = %d must be >= 0." % n_random)
    if n_random > 0 and theta.size < 64:
        raise ValueError(
            "theta has %d nodes but the random family draws Fourier degrees up to 63 "
            "and contracts them against a (%d x %d) basis, so theta.size >= 64 is "
            "required. This precondition was previously enforced only incidentally, by "
            "a numpy shape error, and stated nowhere; pass n_random=0 to use the "
            "per-degree adversarial arm alone on a coarser grid."
            % (theta.size, theta.size, theta.size))
    d = np.abs(theta[:, None] - theta[None, :])
    np.fill_diagonal(d, np.inf)
    _reject_repeated_nodes("theta", d, theta.size)
    ker = d ** (-gamma)

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
        den = sup(p) + semi(p)
        if not np.isfinite(den) or den <= 0.0:
            raise ValueError(
                "the degree-%r adversary has non-positive or non-finite Holder norm %r "
                "on this grid, so its ratio is not defined." % (m, den))
        per_deg.append(semi(Hp) / den)

    rng = np.random.default_rng(seed)
    best = 0.0
    for t in range(n_random):
        m = int(rng.integers(2, 64))
        a = rng.standard_normal(m + 1) / (1.0 + np.arange(m + 1)) ** rng.uniform(0.0, 1.5)
        p, Hp = Cm[:, :m + 1] @ a, Sm[:, :m + 1] @ a
        den = sup(p) + semi(p)
        num = semi(Hp)
        # `if den > 0` and the builtin `max` below are BOTH ordered comparisons: a
        # non-finite den or ratio would be discarded by them and `best` would stay at
        # its 0.0 initialiser, reporting that H annihilates the space (leg 100: 0.0
        # against a clean 0.891421 on all four poisoned inputs).
        if not (np.isfinite(den) and np.isfinite(num)):
            raise ValueError(
                "random trial %d of %d (degree %d) produced a non-finite Holder norm "
                "(denominator %r, numerator %r) from a validated grid and exponent. "
                "Refusing to continue: `if den > 0` and the builtin `max` would both "
                "drop it, and `best` would be reported as the maximum over the "
                "survivors -- or, if every trial is dropped, as exactly 0.0."
                % (t, n_random, m, den, num))
        if den > 0:
            ratio = num / den
            if not np.isfinite(ratio):
                raise ValueError(
                    "random trial %d of %d (degree %d) produced a non-finite ratio %r. "
                    "Refusing to let the builtin `max` discard it." % (t, n_random, m, ratio))
            best = max(best, ratio)
    return per_deg, float(best)
