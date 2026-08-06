"""Route-NB: DOES THE REAL TARGET HAVE FINITE NORM AT ALL?

Leg 55.  This module measures ONE thing, and it is a thing this repository has
asserted for four legs without ever measuring it.

--------------------------------------------------------------------------
THE CLAUSE THIS MODULE IS AIMED AT
--------------------------------------------------------------------------
`plan_of_record.py` carries a live ban whose text ends:

    "... the non-symmetric Hou-Luo profile is not [one basis mode], and does not
     have finite norm in the class where the operator is least bad"

Everything in legs 51, 52 and 53 was measured on the `a = 0` CLM anchor, which is
exactly one basis mode.  The clause above is the *only* statement in the ledger
about the REAL target's membership in the certificate's function space, and as far
as the repository shows it has never been computed.  It is a derivation
(`spectral_certificate.coefficient_decay_exponent` asserts `|h_k| ~ k^{-1-alpha}`
in a docstring) resting on a value of `alpha` that is itself read off a solve.

This module does the measurement.

--------------------------------------------------------------------------
WHAT IS MEASURED, AND IN WHICH BASIS
--------------------------------------------------------------------------
`solver/spectral_certificate.py` compactifies the line with the tangent half-angle
map `X = tan(theta/2)`, in which the three operators of the a = 0 CLM problem are
exact.  Its profiles are ODD, so it uses an odd sine series.  **The target is
NON-symmetric**, so it needs the full circle:

    h(theta) := Omega(tan(theta / 2)),      theta in (-pi, pi),
    h(theta)  = sum_{k in Z} c_k e^{i k theta},       c_{-k} = conj(c_k),

and the coefficient magnitude that a weighted `l^1` norm actually sums is the pair

    |h_k| := |c_k| + |c_{-k}| = 2 |c_k|,      k >= 1.                    (COMPLEX)

The real-basis alternative `|a_k| + |b_k|` (with `a_k = 2 Re c_k`, `b_k = -2 Im c_k`)
satisfies `2|c_k| <= |a_k| + |b_k| <= 2 sqrt(2) |c_k|`, so it is the SAME decay
exponent and at most a factor `sqrt(2)` in the norm.  `coefficient_magnitudes`
returns both and the runner reports the ratio, because "small in WHICH norm" has to
survive a change of convention.

The norms are the ones `spectral_certificate.weight_vector` already defines:

    ||h||_w = sum_{k >= 1} w_k |h_k|,     w_k = (1 + k)^s   (algebraic)  or  1 (flat).

**Finiteness is a statement about an exponent.**  If `|h_k| ~ C k^{-p}` then

    ||h||_w < infinity   <=>   p - s > 1.

So the whole leg is the number `p`, its drift along a resolution ladder, and the
margin `p - 1 - s`.

--------------------------------------------------------------------------
WHY theta -> +-pi IS THE ONLY PLACE THE EXPONENT COMES FROM
--------------------------------------------------------------------------
`X -> +-infinity` is `theta -> +-pi`, one single point of the circle, and near it
`X ~ 2/(pi - theta)`.  A far field `Omega ~ A_+ |X|^{-alpha}` therefore becomes a
BRANCH POINT of order `alpha`,

    h(theta) ~ A_+ ((pi - theta) / 2)^alpha       (and `A_-` from the other side),

whose Fourier coefficients decay like `k^{-1-alpha}`.  Everywhere else on the
circle the profile is smooth, and smooth parts contribute super-algebraically.  So
`p = 1 + alpha` is the prediction, and the object being NON-symmetric only means the
two one-sided amplitudes `A_+ != A_-` differ -- it does not change `p`.

**This is a prediction, not a result.**  It is what the measurement is compared
against; it is not what the measurement reports.

--------------------------------------------------------------------------
THE INSTRUMENT HAS TO BE CALIBRATED, BECAUSE THE PROFILE IS ONLY KNOWN ON A GRID
--------------------------------------------------------------------------
`solver/bordered_hl.py` solves on `X = c sinh(rho)`, uniform in `rho`, `|X| <= 745`.
Two error sources, both of which put a FLOOR under the measurable exponent, and both
of which are measured rather than assumed:

  (1) INTERPOLATION.  `d theta / d rho -> 1` at the origin, so the theta-resolution
      is worst there and is `~ 16 / (n - 1)`.  Local Lagrange interpolation of order
      `L` on the uniform rho grid has error `O(h^L)`; the resulting noise appears as
      a FLOOR in `|h_k|` at large `k`, and where the floor crosses the true
      `C k^{-p}` is where the fit has to stop.
  (2) TRUNCATION.  Beyond `|X| = X_max` there is no data.  `pi - theta = 2 / X_max`
      there, so modes with `k >~ X_max / 2` are determined ENTIRELY by whatever is
      assumed outside the grid.  `far_field="power"` continues the steady equation's
      own forced tail `|X|^{c_omega / c_l}`; `far_field="clamp"` and `"zero"` are
      ABLATIONS THAT CAN CHANGE THE ANSWER (they inject `alpha = 0` and a jump, i.e.
      a spurious `k^{-1}`), and the runner reports all three.

`calibration_family` is the instrument's known-answer curve: `Omega_alpha(X) =
(1 + X^2)^{-alpha/2}` has far field exactly `|X|^{-alpha}`, becomes
`h = |cos(theta/2)|^alpha` exactly, and therefore has `p = 1 + alpha` for EVERY
alpha.  Running the pipeline across a sweep of alpha, including the target's own
alpha, says whether the instrument recovers an exponent it was not told.

--------------------------------------------------------------------------
THE CONTROLS (and each one can come out differently -- lesson 90)
--------------------------------------------------------------------------
POSITIVE, and it can fail: the `a = 0` CLM anchor `Omega_0 = -sin theta =
-2X/(1 + X^2)` is exactly ONE basis mode.  The pipeline must return `|h_1| = 1` and
nothing else -- `p = infinity`, exact truncation.  A wrong half-angle convention, a
sign error in `theta_of_X`, or an off-by-one in the FFT phase all smear this across
every `k`, so the control's numbers are not forced by the code.
**Window (lesson 84): `| |h_1| - 1 | < 1e-10` AND `max_{k >= 2} |h_k| < 1e-08`.**

NEGATIVE 1, and it can fail: `Omega(X) = 1 / (1 + |X|)` has far field exactly
`|X|^{-1}` and an absolute-value KINK at `theta = pi`, so `p = 2` exactly -- which is
precisely the divergence threshold of the class `s = 1`, the class leg 51 measured
the operator to be least bad in.  If the fitter is biased, this reports `p != 2`.

NEGATIVE 2, and it can fail, and it has an EXACT answer: `Omega(X) = 2 arctan(X)/pi`
gives `h(theta) = theta / pi` -- the sawtooth, which does NOT decay at infinity
(`alpha = 0`), whose coefficients are exactly `|h_k| = 2 / (pi k)`, so `p = 1`
exactly: the divergence threshold of the FLAT class.  This is simultaneously the
instrument's hardest calibration (a jump discontinuity is the worst non-smoothness
on the circle, and it brackets the target's `alpha`-cusp from the bad side) and a
control whose coefficient VALUES, not just its exponent, are known in closed form.
Cross-checked against `spectral_certificate.sawtooth_coefficients`.

--------------------------------------------------------------------------
WHAT THIS MODULE DOES NOT DO
--------------------------------------------------------------------------
* It does not certify anything.  A finite norm is a statement that the target is IN
  the space; it is not a statement that any certificate closes.  `MM`'s gate owns
  that question and this module must not be read as touching it.
* It does not re-derive `alpha`.  `alpha = -c_omega / c_l` comes from the solved
  bordered system, and `bordered_hl.tail_exponent` is the independent physical-space
  read of the same number.  The point of this module is the COEFFICIENT side.
* It does not extend the domain to close anything.  `X_max` is varied only as a
  DIAGNOSTIC, to show that `p` does not depend on it.  The live ban against closing
  the truncation gap by extending the domain is about the certificate's gap, and
  nothing here repairs any gap.

--------------------------------------------------------------------------
THE DOMAIN GUARD (added by a bench repair, after leg 84 / Route-TNA)
--------------------------------------------------------------------------
Leg 84 audited this module and answered its gate **YES (silent)**: 8 of 8 adversarial
inputs that pushed theta-samples outside the data returned a finite number with no
exception and no warning, and **0 of 6** exponent- or norm-bearing surfaces carried any
field saying so.  The count `n_outside_grid` existed, was correct, and propagated
nowhere -- so `norm_verdict` could report the target's norm FINITE on the strength of an
exponent fitted where `capabilities.py` calls the measurement untrustworthy, over a
window of width 0.1616 in `s`, with nothing in the returned dict recording it.

The repair is a THRESHOLD plus PROPAGATION.  Both halves are deliberate:

  * **The threshold is `n_outside_grid > 0`, and it is dynamic, not the literal 745.**
    The validated window is not a constant of this module -- it is `max|X|` of whatever
    grid the caller supplied, and 745.2 is merely what `bordered_hl.py` ships at
    `rho_max = 8`.  The trust criterion is leg 55's own, quoted verbatim from the
    `capabilities.py` line: *"the headline is taken where no sample point leaves the
    grid"*.  So one sample outside the data is the violation, at every resolution and
    every domain, and nothing here hardcodes an `X_max`.

  * **Propagation is by an explicit `n_outside_grid=` argument**, threaded from
    `compactify`/`spectrum` into `fit_exponent`, `weighted_partial_sums`,
    `analytic_tail` and `norm_verdict`.  Every one of those returns
    `n_outside_grid` and `domain_valid` in EVERY branch, including the early returns.
    `domain_valid` is `True` (clean), `False` (contaminated) or `None` (the caller did
    not say).  `None` is FALSY on purpose: `if not d["domain_valid"]` treats unknown
    provenance the same as a known violation, which is the conservative direction.

  * **The signal.** `compactify` raises `TargetNormDomainWarning` the moment it has to
    invent data outside the grid, and the downstream functions raise it again when they
    are handed a contaminated count.  It is a warning and not an exception on purpose:
    the far-field ablations (`clamp`, `zero`) exist to be run OUTSIDE the window, that
    is their whole job, and an exception would make the module's own ablation
    unrunnable.  Callers who want it fatal have `warnings.simplefilter("error",
    TargetNormDomainWarning)`; callers running the ablation on purpose have
    `simplefilter("ignore", ...)`.

  * **What is unchanged.**  Every in-window number this module returns is bit-identical
    to what it returned before.  The guard adds fields and a warning; it computes
    nothing new and corrects nothing.  `coefficient_magnitudes` (a tuple) and
    `noise_floor` (a float) have no dict to carry a field and are untouched.

--------------------------------------------------------------------------
THE WINDOW ITSELF (repaired by leg 220 / Route-TNR, after leg 204 / Route-TNA2)
--------------------------------------------------------------------------
Leg 204's fourth audit of this module found a hole in the guard above: the THRESHOLD was
right and the PROPAGATION was right, but the **window** was wrong.  `compactify` tested
`inside = |Xt| <= max|X|`.  For a grid symmetric about zero that IS the data interval; for
any other grid it is strictly larger, and every theta-sample in the gap was handed to
`lagrange_interp_uniform`, whose index clip turns it into polynomial EXTRAPOLATION.
`n_outside_grid` counted only samples beyond `max|X|`, so it reported `0`.  On leg 55's
own headline grid truncated at `X_min = -9.71` -- still 523 real data points over four
decades -- 535 of 16384 samples were extrapolated while the module reported
`n_outside_grid = 0`, `domain_valid = True`, zero warnings, and a fitted exponent of
`-0.0889` against the exact `1.4`: 386x the systematic, with the SIGN wrong.  That defeated
leg 84's audit, the bench repair that answered it, and leg 94's precision pass, all three.

The repair is one word wide: **the window is the data interval `[min X, max X]`**, so
`inside = (Xt >= X_lo) & (Xt <= X_hi)`.  Two arithmetic sites follow it -- which grid edge
a far-field sample continues FROM (`Xt > X_hi`, was `Xt > 0`) and which endpoint magnitude
the `power` closure normalises by (per side, was `max|X|` for both).  On a symmetric grid
all three reduce to the pre-repair expressions bit for bit, which is why leg 55's banked
margins (`+0.394` at `s = 0`, `+0.094` at `s = 0.3`) are reproduced to `0.0` difference.

`spectrum` now also reports `X_lo_data` / `X_hi_data`.  `X_max_data` is unchanged in name
and value, but it is no longer the guard's threshold and must not be read as one.
"""

import warnings

import numpy as np


class TargetNormDomainWarning(UserWarning):
    """Theta-samples fell outside the data, so the far-field CLOSURE decided the answer.

    Leg 84 measured what that costs: at the shipped domain 14 of 16384 samples (0.085%)
    move the fitted exponent from 1.4039 to 1.5654 to 1.1488 across the power/clamp/zero
    closures -- a spread of 0.4166 on an object whose exponent is 1.4 exactly.  The
    warning does not say the answer is wrong; it says the answer is a property of the
    closure as much as of the data, which is exactly what `capabilities.py` means by
    "not trustworthy there".
    """


def domain_fields(n_outside_grid):
    """The two keys EVERY result-bearing dict in this module carries, uniformly.

    `n_outside_grid` is the count from `compactify`/`spectrum`, or `None` when the caller
    did not thread it through.  `domain_valid` is `True` / `False` / `None` for
    clean / contaminated / unknown -- and `None` is falsy, so a caller who writes
    `if not d["domain_valid"]` errs toward distrust rather than toward silence.
    """
    if n_outside_grid is None:
        return {"n_outside_grid": None, "domain_valid": None}
    n = int(n_outside_grid)
    return {"n_outside_grid": n, "domain_valid": bool(n == 0)}


def _warn_if_outside(n_outside_grid, where, extra=""):
    """Raise TargetNormDomainWarning iff a KNOWN count is positive.  Unknown is silent.

    Unknown provenance does not warn, because warning on it would fire on every legacy
    call site and train callers to filter the category away -- which is how a guard
    becomes noise and then becomes nothing.  Unknown is recorded in the dict instead,
    where it is falsy.
    """
    if n_outside_grid is None or int(n_outside_grid) <= 0:
        return
    warnings.warn(
        f"target_norm.{where}: {int(n_outside_grid)} theta-sample(s) lie outside the "
        f"supplied data window, so the far-field closure -- not the data -- determines "
        f"those modes{extra}.  capabilities.py calls the measurement untrustworthy "
        f"there; the headline is taken where no sample point leaves the grid.",
        TargetNormDomainWarning, stacklevel=3)

# --------------------------------------------------------------------------
# the compactification map
# --------------------------------------------------------------------------
def theta_of_X(X):
    """theta = 2 arctan(X) in (-pi, pi).  The inverse of X = tan(theta/2)."""
    return 2.0 * np.arctan(np.asarray(X, dtype=float))


def X_of_theta(theta):
    """X = tan(theta/2).  Infinite at theta = +-pi, which the grids never sample."""
    return np.tan(0.5 * np.asarray(theta, dtype=float))


def midpoint_theta_grid(M):
    """M points, uniform, on (-pi, pi), STAGGERED off the endpoints.

    theta_j = -pi + 2 pi (j + 1/2) / M.  The stagger matters: theta = +-pi is the one
    point where X is infinite and where the profile's branch point sits, so a grid
    that lands on it cannot be evaluated at all.  The half-cell shift is a pure phase
    in the transform and does not touch any |c_k|."""
    M = int(M)
    return -np.pi + 2.0 * np.pi * (np.arange(M) + 0.5) / M


# --------------------------------------------------------------------------
# high-order interpolation on the uniform rho grid (no scipy in this project)
# --------------------------------------------------------------------------
def _barycentric_weights(m):
    """Barycentric weights for m EQUISPACED nodes: w_j = (-1)^j C(m-1, j)."""
    from math import comb
    return np.array([((-1) ** j) * comb(m - 1, j) for j in range(m)], dtype=float)


def lagrange_interp_uniform(y, t, order=8):
    """Local Lagrange interpolation of `y` (samples on the uniform index grid 0..n-1).

    `t` is an array of REAL indices.  A stencil of `order` consecutive nodes centred on
    `t` is used, clipped to the array; on equispaced nodes the barycentric form is
    stable for the small orders used here.  Error is O(h^order) for smooth `y`, which
    is what pushes the interpolation noise floor below the coefficients being measured.

    Values of `t` outside [0, n-1] are NOT extrapolated here -- callers handle the far
    field explicitly, because assuming something outside the data is exactly the choice
    this leg has to expose rather than bury.
    """
    y = np.asarray(y, dtype=float)
    n = y.size
    order = int(min(order, n))
    t = np.asarray(t, dtype=float)
    i0 = np.clip(np.floor(t).astype(int) - (order // 2 - 1), 0, n - order)
    idx = i0[:, None] + np.arange(order)[None, :]          # (T, order)
    w = _barycentric_weights(order)[None, :]
    d = t[:, None] - idx.astype(float)                      # (T, order)
    exact = np.isclose(d, 0.0, atol=0.0)
    d_safe = np.where(exact, 1.0, d)
    q = w / d_safe
    num = (q * y[idx]).sum(1)
    den = q.sum(1)
    out = num / den
    hit = exact.any(1)
    if hit.any():
        j = np.argmax(exact[hit], axis=1)
        out[hit] = y[idx[hit], j]
    return out


# --------------------------------------------------------------------------
# sample a grid-borne profile onto the compactified circle
# --------------------------------------------------------------------------
def compactify(X, f, M, c=0.5, far_field="power", tail_exponent=None, order=8):
    """h(theta_j) on the staggered grid of size M, from samples f on X = c sinh(rho).

    The interpolation is done in `rho = arcsinh(X / c)`, which is the variable the data
    are UNIFORM in; interpolating in X directly would put a 745-to-0.04 spacing ratio
    inside the stencil.

    `far_field` says what happens for X_j outside the DATA interval [min X, max X] -- and
    it is a real choice, not a detail, because those points are exactly the branch point
    the exponent comes from:

        "power" : continue |X|^tail_exponent from the last grid value (the steady
                  equation's own forced tail; tail_exponent = c_omega / c_l).
        "clamp" : hold the last grid value  (injects alpha = 0, i.e. a spurious k^-1).
        "zero"  : set 0                     (injects a JUMP, also k^-1).
        "none"  : leave NaN, so a caller that forgot to choose finds out.

    "clamp" and "zero" are ABLATIONS. They are here so that "the answer does not depend
    on the far-field closure" is something the runner can check instead of assert.
    """
    X = np.asarray(X, dtype=float)
    f = np.asarray(f, dtype=float)
    if X.shape != f.shape:
        raise ValueError("X and f must have the same shape")
    # THE WINDOW IS THE DATA INTERVAL, NOT max|X| (leg 204 finding 1, repaired at leg 220).
    # `X_lo`/`X_hi` are the true endpoints of the supplied grid.  `X_max = max|X|` is kept
    # only because `spectrum` has always reported it under that name; it is NO LONGER the
    # guard's threshold.  On a grid symmetric about zero -- which every live caller in this
    # repository supplies, to |X_lo + X_hi| = 0.0e+00 exactly -- `X_lo = -X_hi = -X_max`
    # and every branch below reduces to the pre-repair arithmetic bit for bit.
    X_lo = float(X.min())
    X_hi = float(X.max())
    X_max = float(np.abs(X).max())
    rho = np.arcsinh(X / float(c))
    rho_lo, rho_hi = float(rho[0]), float(rho[-1])
    h_rho = (rho_hi - rho_lo) / (rho.size - 1)

    th = midpoint_theta_grid(M)
    Xt = X_of_theta(th)
    inside = (Xt >= X_lo) & (Xt <= X_hi)
    out = np.full(th.size, np.nan)

    t = (np.arcsinh(Xt[inside] / float(c)) - rho_lo) / h_rho
    out[inside] = lagrange_interp_uniform(f, t, order=order)

    if (~inside).any():
        f_hi = float(f[-1])                      # value at X = X_hi
        f_lo = float(f[0])                       # value at X = X_lo
        above = Xt[~inside] > X_hi               # was `Xt > 0`: identical iff X_lo = -X_hi
        edge = np.where(above, f_hi, f_lo)
        if far_field == "power":
            if tail_exponent is None:
                raise ValueError("far_field='power' needs tail_exponent")
            # The power continuation is |X|^q measured from the edge it continues FROM, so
            # each side normalises by its OWN endpoint magnitude.  Symmetric grid: both are
            # X_max and this is the pre-repair `|Xt| / X_max`.  A one-sided grid whose data
            # interval touches zero has a zero edge magnitude on that side; the resulting
            # inf/0 is VISIBLE, and those samples are now counted in `n_outside` besides.
            scale = np.where(above, X_hi, -X_lo)
            ratio = np.abs(Xt[~inside]) / scale
            out[~inside] = edge * ratio ** float(tail_exponent)
        elif far_field == "clamp":
            out[~inside] = edge
        elif far_field == "zero":
            out[~inside] = 0.0
        elif far_field == "none":
            pass
        else:
            raise ValueError(f"unknown far_field {far_field!r}")
    n_outside = int((~inside).sum())
    # THE GUARD, at the one place in the module that actually knows.  The threshold is
    # dynamic -- `X_max` above is the caller's own grid, not a hardcoded 745.
    _warn_if_outside(n_outside, "compactify",
                     f" ({n_outside} of {int(M)} samples, "
                     f"{100.0 * n_outside / max(int(M), 1):.3f}%, outside the DATA "
                     f"interval [{X_lo:.6g}, {X_hi:.6g}] with far_field={far_field!r})")
    return th, out, n_outside


# --------------------------------------------------------------------------
# coefficients
# --------------------------------------------------------------------------
def coefficient_magnitudes(h):
    """From h on the staggered grid: k, |h_k| = 2|c_k| (complex), and |a_k| + |b_k|.

    The staggered grid contributes a pure phase e^{-i k (pi/M - pi)} which cancels in
    |c_k|; it is applied anyway so that a_k and b_k are the real Fourier coefficients
    and not rotated ones.  Returned for k = 1 .. M/2 - 1: the k = 0 mean and the
    Nyquist mode are dropped, the latter because it is the one mode aliasing cannot be
    separated from its own image.
    """
    h = np.asarray(h, dtype=float)
    M = h.size
    if not np.all(np.isfinite(h)):
        raise ValueError("h has non-finite entries -- did far_field='none' leave NaN?")
    C = np.fft.fft(h) / M
    kmax = M // 2 - 1
    k = np.arange(1, kmax + 1)
    th0 = -np.pi + np.pi / M
    ck = C[1:kmax + 1] * np.exp(-1j * k * th0)
    a = 2.0 * np.real(ck)
    b = -2.0 * np.imag(ck)
    return k, 2.0 * np.abs(ck), np.abs(a) + np.abs(b)


# --------------------------------------------------------------------------
# the exponent, and the floor that limits it
# --------------------------------------------------------------------------
def noise_floor(hk, k, frac=0.25):
    """Median |h_k| over the top `frac` of the measured band -- the plateau level.

    Where the true coefficients have fallen below the interpolation/aliasing noise the
    spectrum flattens.  This is the level of that plateau, used to CHOOSE the fit band
    rather than to correct anything."""
    n = hk.size
    lo = int(n * (1.0 - float(frac)))
    return float(np.median(hk[lo:]))


def fit_exponent(k, hk, k_lo, k_hi, n_outside_grid=None):
    """Least-squares slope of log|h_k| against log k over [k_lo, k_hi].

    Returns p > 0 for |h_k| ~ C k^{-p}, the prefactor C, the R^2 of the fit and the
    band actually used -- plus, in EVERY branch including the two early returns,
    `n_outside_grid` and `domain_valid` (see `domain_fields`).  Pass
    `n_outside_grid=sp["n_outside_grid"]` from the `spectrum` call the coefficients came
    from; without it the exponent is returned with `domain_valid = None`, meaning "this
    number carries no record of the domain it came from", which is the state leg 84
    measured for every exponent this module has ever returned.

    THE COEFFICIENTS ARE AVERAGED **LINEARLY** WITHIN LOGARITHMIC BINS, AND THAT IS NOT
    A COSMETIC CHOICE.  Individual |h_k| can be exactly zero: a profile with a symmetry
    kills a whole arithmetic sub-sequence of modes (the negative control 1/(1+|X|)
    satisfies h(theta) + h(pi - theta) = 1, which annihilates every even mode), and two
    branch points of different amplitude at the same circle point beat against each
    other and produce near-cancellations.  A log-average then takes logs of roundoff and
    reports nonsense -- the first version of this function did exactly that and returned
    p = -0.06 for an object whose exponent is 2.  A LINEAR bin mean is immune, and it is
    also the physically right object: the norm this leg is about SUMS coefficients, so
    the quantity whose decay decides finiteness is the mass in a bin, not the geometric
    mean of a bin.  For a clean power law the two agree up to a constant, so the
    exponent is unchanged where nothing cancels.
    """
    k = np.asarray(k, dtype=float)
    hk = np.asarray(hk, dtype=float)
    _warn_if_outside(n_outside_grid, "fit_exponent",
                     f" (the exponent over k = {float(k_lo):g}..{float(k_hi):g} is being "
                     "fitted to coefficients the closure helped set)")
    dom = domain_fields(n_outside_grid)
    m = (k >= k_lo) & (k <= k_hi)
    if m.sum() < 8:
        return {"p": float("nan"), "C": float("nan"), "r2": float("nan"),
                "k_lo": float(k_lo), "k_hi": float(k_hi), "n_points": int(m.sum()),
                **dom}
    kk, hh = k[m], hk[m]
    # LOG-SPACED bins, MERGED until every bin holds at least `min_count` modes.
    # Both halves of that are needed, and each was learned from a control coming out
    # wrong:
    #   * log spacing, because every bin then spans the same RATIO of k, so the
    #     convexity offset between a bin's linear mean and its value at the bin's
    #     geometric-mean k is the same in every bin -- it moves the PREFACTOR and
    #     leaves the SLOPE alone.  Equal-COUNT bins have k-widths that grow along the
    #     band, so their offset drifts and the fitted exponent inherits a bias that
    #     grew to +0.06 on the calibration family.
    #   * the merge, because a sparsely populated log bin can catch a single mode of
    #     a symmetry-annihilated sub-sequence (1/(1+|X|) kills every even mode), whose
    #     value is ~1e-18; its log is -41 against a trend of -12 and it captures the
    #     entire least squares.  That returned p = -0.25 for a spectrum whose
    #     k^2 |h_k| is flat to 2.3% over k = 9..129 and to three digits from k = 33 on.
    min_count = 8
    lk = np.log(kk)
    nb0 = min(64, max(4, int(kk.size // min_count)))
    edges = np.linspace(lk.min(), lk.max() + 1e-12, nb0 + 1)
    which = np.clip(np.digitize(lk, edges) - 1, 0, nb0 - 1)
    bx, by, acc = [], [], []
    for j in range(nb0):
        acc.extend(np.flatnonzero(which == j).tolist())
        if len(acc) >= min_count:
            idx = np.array(acc)
            if hh[idx].mean() > 0.0:
                bx.append(float(np.exp(lk[idx].mean())))
                by.append(float(hh[idx].mean()))      # LINEAR mean, see docstring
            acc = []
    if acc and len(bx) and hh[np.array(acc)].mean() > 0.0:
        idx = np.array(acc)
        bx.append(float(np.exp(lk[idx].mean())))
        by.append(float(hh[idx].mean()))
    bx, by = np.log(np.array(bx)), np.log(np.array(by))
    if bx.size < 4:
        return {"p": float("nan"), "C": float("nan"), "r2": float("nan"),
                "k_lo": float(k_lo), "k_hi": float(k_hi), "n_points": int(m.sum()),
                **dom}
    slope, icpt = np.polyfit(bx, by, 1)
    pred = slope * bx + icpt
    ss_res = float(((by - pred) ** 2).sum())
    ss_tot = float(((by - by.mean()) ** 2).sum())
    return {"p": float(-slope), "C": float(np.exp(icpt)),
            "r2": float(1.0 - ss_res / ss_tot) if ss_tot > 0 else float("nan"),
            "k_lo": float(k_lo), "k_hi": float(k_hi),
            "n_points": int(m.sum()), "n_bins": int(bx.size),
            "frac_zero_modes": float((hh <= 0.0).mean()), **dom}


# --------------------------------------------------------------------------
# the norms themselves
# --------------------------------------------------------------------------
def weighted_partial_sums(k, hk, s, checkpoints, n_outside_grid=None):
    """S_N = sum_{k <= N} (1+k)^s |h_k| at each N in `checkpoints`.

    This is the partial sum of the actual norm, in the algebraic class
    `spectral_certificate.weight_vector(kind="algebraic", param=s)`; `s = 0` is that
    module's flat class exactly, and the runner checks the two agree entry for entry.
    A partial sum is not a norm -- what makes the norm finite is the TAIL, which is
    `analytic_tail` below and is a statement about the exponent, not about the data.

    Every checkpoint dict carries `n_outside_grid` and `domain_valid`: a partial sum runs
    over modes `k <~ X_max / 2` and above, and the modes above that bound are exactly the
    ones the closure invented, so a checkpoint at `N = 4096` on a 745 grid is a sum over
    data the grid never held.
    """
    k = np.asarray(k, dtype=float)
    _warn_if_outside(n_outside_grid, "weighted_partial_sums",
                     f" (the partial sums at s = {float(s):g} include those modes)")
    dom = domain_fields(n_outside_grid)
    w = (1.0 + k) ** float(s)
    cum = np.cumsum(w * np.asarray(hk, dtype=float))
    out = []
    for N in checkpoints:
        j = np.searchsorted(k, float(N), side="right") - 1
        out.append({"N": int(N), "S_N": float(cum[j]) if j >= 0 else 0.0, **dom})
    return out


def analytic_tail(p, C, N, s, n_outside_grid=None):
    """The tail sum_{k > N} (1+k)^s C k^{-p}, or the honest statement that it is not one.

    Returns a dict with `finite` and, when finite, the integral bound
    `C N^{1 + s - p} / (p - s - 1)` (using (1+k)^s <= (2k)^s for k >= 1, folded into
    the constant).  When `p - s <= 1` the quantity HAS NO VALUE -- the sum diverges --
    and the dict says so instead of returning a large number (lesson 73).
    """
    p, C, N, s = float(p), float(C), float(N), float(s)
    _warn_if_outside(n_outside_grid, "analytic_tail",
                     f" (the bound at s = {s:g} rests entirely on p = {p:.6g})")
    dom = domain_fields(n_outside_grid)
    margin = p - s - 1.0
    if not np.isfinite(margin) or margin <= 0.0:
        return {"finite": False, "margin": float(margin), "bound": None,
                "reason": "p - s <= 1: the weighted sum diverges; the tail has no value",
                **dom}
    return {"finite": True, "margin": float(margin),
            "bound": float((2.0 ** s) * C * N ** (-margin) / margin), "reason": None,
            **dom}


def norm_verdict(p, s, alpha=None, n_outside_grid=None):
    """Is ||.||_{l^1_w} finite at exponent `s`, and by how much -- as a MAGNITUDE.

    This is the surface leg 84 named as the concrete harm: `finite` is a statement that
    the target IS in the certificate's space, and before the guard the dict recorded
    nothing about which domain `p` came from.  At the shipped domain the untrustworthy
    exponent reports FINITE where the headline exponent reports DIVERGENT over a window
    of width 0.1616 in `s`.  `domain_valid` is now in the same dict as `finite`, so the
    two can no longer be read apart.
    """
    margin = float(p) - float(s) - 1.0
    _warn_if_outside(n_outside_grid, "norm_verdict",
                     f" (the FINITE/DIVERGENT verdict at s = {float(s):g} is being taken "
                     f"from p = {float(p):.6g}, fitted outside the validated window)")
    d = {"s": float(s), "p": float(p), "margin_in_exponent_units": margin,
         "finite": bool(margin > 0.0)}
    if alpha is not None:
        d["margin_predicted"] = float(alpha) - float(s)
    d.update(domain_fields(n_outside_grid))
    return d


# --------------------------------------------------------------------------
# the controls and the calibration family
# --------------------------------------------------------------------------
def clm_anchor_profile(X):
    """POSITIVE CONTROL: Omega_0 = -sin theta = -2X/(1+X^2).  Exactly one mode."""
    X = np.asarray(X, dtype=float)
    return -2.0 * X / (1.0 + X ** 2)


def inverse_X_profile(X):
    """NEGATIVE CONTROL 1: 1/(1+|X|).  Far field |X|^-1, a KINK at theta = pi, p = 2.

    p = 2 is the divergence threshold of the class s = 1 -- the class leg 51 measured
    the operator to be least bad in."""
    X = np.asarray(X, dtype=float)
    return 1.0 / (1.0 + np.abs(X))


def sawtooth_profile(X):
    """NEGATIVE CONTROL 2: 2 arctan(X)/pi, i.e. h(theta) = theta/pi.

    Does NOT decay (alpha = 0); a JUMP at theta = pi; coefficients exactly 2/(pi k),
    so p = 1 -- the divergence threshold of the FLAT class."""
    return theta_of_X(X) / np.pi


def sawtooth_exact(k):
    """|h_k| = 2 / (pi k) exactly, in the complex convention 2|c_k|."""
    return 2.0 / (np.pi * np.asarray(k, dtype=float))


def calibration_family(X, alpha):
    """(1 + X^2)^{-alpha/2} -- far field exactly |X|^-alpha, h = |cos(theta/2)|^alpha.

    A branch point of order alpha at theta = pi and analytic everywhere else, so
    p = 1 + alpha for EVERY alpha.  This is the instrument's calibration curve: run it
    across a sweep of alpha (including the target's own) and see whether the fitter
    returns an exponent nobody told it."""
    X = np.asarray(X, dtype=float)
    return (1.0 + X ** 2) ** (-0.5 * float(alpha))


# --------------------------------------------------------------------------
# the whole pipeline, once
# --------------------------------------------------------------------------
def spectrum(X, f, M=8192, c=0.5, far_field="power", tail_exponent=None, order=8):
    """compactify -> FFT -> magnitudes.  One call, so the controls use the same path."""
    th, h, n_out = compactify(X, f, M, c=c, far_field=far_field,
                              tail_exponent=tail_exponent, order=order)
    k, hk, hk_real = coefficient_magnitudes(h)
    out = {"k": k, "hk": hk, "hk_real_basis": hk_real, "M": int(M),
           "far_field": far_field,
           "X_max_data": float(np.abs(np.asarray(X, dtype=float)).max()),
           # the guard's ACTUAL window since leg 220: the data interval, which equals
           # (-X_max_data, +X_max_data) only on a grid symmetric about zero
           "X_lo_data": float(np.asarray(X, dtype=float).min()),
           "X_hi_data": float(np.asarray(X, dtype=float).max()),
           "frac_outside_grid": float(n_out) / float(max(int(M), 1))}
    # `n_outside_grid` was already here and already correct; what it lacked was a
    # threshold (`domain_valid`) and anywhere to go.  compactify has warned already, so
    # this does not warn twice.
    out.update(domain_fields(n_out))
    return out
