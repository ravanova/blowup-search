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
"""

import numpy as np

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

    `far_field` says what happens for |X_j| > max|X| -- and it is a real choice, not a
    detail, because those points are exactly the branch point the exponent comes from:

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
    X_max = float(np.abs(X).max())
    rho = np.arcsinh(X / float(c))
    rho_lo, rho_hi = float(rho[0]), float(rho[-1])
    h_rho = (rho_hi - rho_lo) / (rho.size - 1)

    th = midpoint_theta_grid(M)
    Xt = X_of_theta(th)
    inside = np.abs(Xt) <= X_max
    out = np.full(th.size, np.nan)

    t = (np.arcsinh(Xt[inside] / float(c)) - rho_lo) / h_rho
    out[inside] = lagrange_interp_uniform(f, t, order=order)

    if (~inside).any():
        f_hi = float(f[-1])                      # value at X = +X_max
        f_lo = float(f[0])                       # value at X = -X_max
        edge = np.where(Xt[~inside] > 0, f_hi, f_lo)
        if far_field == "power":
            if tail_exponent is None:
                raise ValueError("far_field='power' needs tail_exponent")
            ratio = np.abs(Xt[~inside]) / X_max
            out[~inside] = edge * ratio ** float(tail_exponent)
        elif far_field == "clamp":
            out[~inside] = edge
        elif far_field == "zero":
            out[~inside] = 0.0
        elif far_field == "none":
            pass
        else:
            raise ValueError(f"unknown far_field {far_field!r}")
    return th, out, int((~inside).sum())


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


def fit_exponent(k, hk, k_lo, k_hi):
    """Least-squares slope of log|h_k| against log k over [k_lo, k_hi].

    Returns p > 0 for |h_k| ~ C k^{-p}, the prefactor C, the R^2 of the fit and the
    band actually used.

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
    m = (k >= k_lo) & (k <= k_hi)
    if m.sum() < 8:
        return {"p": float("nan"), "C": float("nan"), "r2": float("nan"),
                "k_lo": float(k_lo), "k_hi": float(k_hi), "n_points": int(m.sum())}
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
    #     k^2 |h_k| is flat to three digits over eight octaves.
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
                "k_lo": float(k_lo), "k_hi": float(k_hi), "n_points": int(m.sum())}
    slope, icpt = np.polyfit(bx, by, 1)
    pred = slope * bx + icpt
    ss_res = float(((by - pred) ** 2).sum())
    ss_tot = float(((by - by.mean()) ** 2).sum())
    return {"p": float(-slope), "C": float(np.exp(icpt)),
            "r2": float(1.0 - ss_res / ss_tot) if ss_tot > 0 else float("nan"),
            "k_lo": float(k_lo), "k_hi": float(k_hi),
            "n_points": int(m.sum()), "n_bins": int(bx.size),
            "frac_zero_modes": float((hh <= 0.0).mean())}


# --------------------------------------------------------------------------
# the norms themselves
# --------------------------------------------------------------------------
def weighted_partial_sums(k, hk, s, checkpoints):
    """S_N = sum_{k <= N} (1+k)^s |h_k| at each N in `checkpoints`.

    This is the partial sum of the actual norm, in the algebraic class
    `spectral_certificate.weight_vector(kind="algebraic", param=s)`; `s = 0` is that
    module's flat class exactly, and the runner checks the two agree entry for entry.
    A partial sum is not a norm -- what makes the norm finite is the TAIL, which is
    `analytic_tail` below and is a statement about the exponent, not about the data.
    """
    k = np.asarray(k, dtype=float)
    w = (1.0 + k) ** float(s)
    cum = np.cumsum(w * np.asarray(hk, dtype=float))
    out = []
    for N in checkpoints:
        j = np.searchsorted(k, float(N), side="right") - 1
        out.append({"N": int(N), "S_N": float(cum[j]) if j >= 0 else 0.0})
    return out


def analytic_tail(p, C, N, s):
    """The tail sum_{k > N} (1+k)^s C k^{-p}, or the honest statement that it is not one.

    Returns a dict with `finite` and, when finite, the integral bound
    `C N^{1 + s - p} / (p - s - 1)` (using (1+k)^s <= (2k)^s for k >= 1, folded into
    the constant).  When `p - s <= 1` the quantity HAS NO VALUE -- the sum diverges --
    and the dict says so instead of returning a large number (lesson 73).
    """
    p, C, N, s = float(p), float(C), float(N), float(s)
    margin = p - s - 1.0
    if not np.isfinite(margin) or margin <= 0.0:
        return {"finite": False, "margin": float(margin), "bound": None,
                "reason": "p - s <= 1: the weighted sum diverges; the tail has no value"}
    return {"finite": True, "margin": float(margin),
            "bound": float((2.0 ** s) * C * N ** (-margin) / margin), "reason": None}


def norm_verdict(p, s, alpha=None):
    """Is ||.||_{l^1_w} finite at exponent `s`, and by how much -- as a MAGNITUDE."""
    margin = float(p) - float(s) - 1.0
    d = {"s": float(s), "p": float(p), "margin_in_exponent_units": margin,
         "finite": bool(margin > 0.0)}
    if alpha is not None:
        d["margin_predicted"] = float(alpha) - float(s)
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
    return {"k": k, "hk": hk, "hk_real_basis": hk_real, "M": int(M),
            "n_outside_grid": int(n_out), "far_field": far_field}
