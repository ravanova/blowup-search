"""Win-condition diagnostics for the Navier-Stokes blow-up search project.

Implements the Tier 1 / Tier 2 checks described in WIN_CONDITION.md. These
are numerical proxies for the Beale-Kato-Majda criterion: a smooth solution
fails to extend past T iff the time-integral of ||vorticity||_inf diverges
as t -> T. Tier 3 (a rigorous computer-assisted proof) is out of scope for
this module by design -- no amount of floating-point simulation can
substitute for it.
"""

from dataclasses import dataclass
from enum import Enum


class WinTier(Enum):
    NONE = "none"
    CANDIDATE = "candidate"
    NUMERICALLY_CONFIRMED = "numerically_confirmed"


class InsufficientDataError(ValueError):
    """The max|omega(t)| series is too short to fit (or cross-validate).

    This is a *data* outcome, not a programmer error: near the critical
    parameter, a solver run can legitimately terminate early -- e.g. by
    hitting the omega-amplification stop threshold moments after it starts --
    leaving too few samples for a trend fit. Callers in the bisection/fitness
    path must catch this and classify from the run's termination reason
    instead: a run stopped by the amplification threshold IS a blow-up even
    though the fit couldn't run, and a run cut short for any other reason is
    an error event, not evidence either way. Treating this exception as "no
    blow-up" would flip the bisection in exactly the wrong direction for the
    fastest-blowing-up genomes. Subclasses ValueError so pre-existing callers
    that caught ValueError keep working.
    """


@dataclass
class BlowupEstimate:
    t_star: float
    r_squared: float
    slope: float
    last_time: float
    n_points: int
    exponent: float = 1.0  # fitted blow-up exponent alpha (1.0 = CLM-like linear)


def _linear_regression(xs, ys):
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    sxx = sum((x - mean_x) ** 2 for x in xs)
    sxy = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    slope = sxy / sxx
    intercept = mean_y - slope * mean_x
    ss_tot = sum((y - mean_y) ** 2 for y in ys)
    ss_res = sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys))
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return slope, intercept, r_squared


_DEFAULT_EXPONENT_GRID = [round(0.3 + 0.05 * i, 2) for i in range(55)]  # 0.30 .. 3.00


def estimate_blowup_time(times, vorticity_max, tail_fraction=0.5,
                         fit_exponent=False, exponent_grid=None):
    """Fit the reciprocal vorticity over the tail of the run and extrapolate
    its zero crossing (the Hou/Luo reciprocal-vorticity diagnostic for
    BKM-consistent blow-up).

    With ``fit_exponent=False`` (default) this is the plain CLM-style fit:
    ``1/||omega||_inf(t)`` is fit as a straight line, which is exact only for
    generic self-similar blow-up ``M ~ (T*-t)^-1`` (e.g. Constantin-Lax-Majda).
    For a non-generic exponent ``M ~ (T*-t)^-alpha`` with ``alpha != 1`` that
    reciprocal is *curved*, so a straight-line fit both mis-estimates ``T*``
    and depresses ``R^2`` -- which would make the Tier 1 gate reject exactly
    the non-generic (e.g. De Gregorio) blow-ups we are hunting for.

    With ``fit_exponent=True`` we search ``alpha``: for each candidate,
    ``(1/M)^(1/alpha)`` is linear in ``t`` (with the same zero crossing ``T*``)
    iff that ``alpha`` is correct. Naively picking the ``alpha`` that maximizes
    ``R^2`` over the whole grid is an overfitting trap: on a short monotone
    tail, taking the argmax over ~55 candidate exponents inflates ``R^2`` by
    pure garden-of-forking-paths selection, which would manufacture false Tier 1
    candidates -- the exact self-fooling WIN_CONDITION.md exists to prevent. So
    instead we select ``alpha`` **out of sample**: fit the linearized line on
    the first half of the tail and score its ``R^2`` on the held-out second
    half, choosing the ``alpha`` with the best held-out fit. A wrong ``alpha``
    leaves the linearized reciprocal curved, so the first-half line extrapolates
    badly onto the second half and its held-out ``R^2`` collapses; only an
    ``alpha`` that is genuinely linear across the *whole* tail scores well.
    The reported ``r_squared`` is that honest held-out value (so the Tier 1
    gate judges out-of-sample fit, not in-sample), while ``t_star`` and
    ``slope`` come from a final fit over the full tail. ``slope`` is in the
    linearized coordinate, not of ``1/M`` directly.

    Returns None if there's no forward-pointing blow-up signal, otherwise a
    BlowupEstimate. Raises InsufficientDataError (a ValueError subclass) when
    the series is too short to fit at all -- see that class's docstring for
    why bisection callers must NOT treat that case as "no blow-up".
    """
    n = len(times)
    if n < 4:
        raise InsufficientDataError("need at least 4 samples to fit a trend")

    tail_start = max(0, int(n * (1 - tail_fraction)))
    xs = times[tail_start:]
    ms = vorticity_max[tail_start:]

    if any(m <= 0 for m in ms):
        # Non-positive vorticity max -> reciprocal is undefined. Treat as "no
        # valid signal" rather than crashing; a real blow-up never gets here.
        return None
    inv = [1.0 / m for m in ms]

    if not fit_exponent:
        # CLM-style generic blow-up: 1/M is fit directly as a straight line
        # (alpha == 1). No exponent search, so no overfitting to guard against.
        slope, intercept, r_squared = _linear_regression(xs, inv)
        if slope >= 0:
            return None  # reciprocal isn't shrinking -> no blow-up
        t_star = -intercept / slope
        if t_star <= xs[-1]:
            return None  # extrapolated crossing is in the past -> not forward
        return BlowupEstimate(
            t_star=t_star,
            r_squared=r_squared,
            slope=slope,
            last_time=xs[-1],
            n_points=len(xs),
            exponent=1.0,
        )

    # fit_exponent=True: choose alpha by held-out (out-of-sample) validation.
    m = len(xs)
    if m < 8:
        raise InsufficientDataError(
            "need at least 8 tail samples to cross-validate the blow-up "
            "exponent; increase tail_fraction or run the solver longer"
        )
    mid = m // 2
    grid = exponent_grid or _DEFAULT_EXPONENT_GRID

    best = None  # (r2_holdout, alpha, slope_full, t_star_full)
    for alpha in grid:
        zs = [v ** (1.0 / alpha) for v in inv]
        # Train on the first half, score on the held-out second half.
        s_tr, b_tr, _ = _linear_regression(xs[:mid], zs[:mid])
        if s_tr >= 0:
            continue  # linearized reciprocal not shrinking on the train window
        r2_holdout = _r_squared_out_of_sample(xs[mid:], zs[mid:], s_tr, b_tr)
        if r2_holdout is None:
            continue  # held-out window is degenerate (no variance to explain)
        # Final estimate uses a fit over the full tail (all the data), but the
        # reported R^2 stays the honest held-out one that the gate judges.
        s_full, b_full, _ = _linear_regression(xs, zs)
        if s_full >= 0:
            continue
        t_star = -b_full / s_full
        if t_star <= xs[-1]:
            continue
        if best is None or r2_holdout > best[0]:
            best = (r2_holdout, alpha, s_full, t_star)

    if best is None:
        return None

    r2_holdout, alpha, slope, t_star = best
    return BlowupEstimate(
        t_star=t_star,
        r_squared=r2_holdout,
        slope=slope,
        last_time=xs[-1],
        n_points=len(xs),
        exponent=alpha,
    )


def _r_squared_out_of_sample(xs, ys, slope, intercept):
    """R^2 of a line (fit elsewhere) evaluated on a held-out window.

    Unlike the in-sample R^2 from _linear_regression, this can go negative when
    the line -- fit on other data -- predicts this window worse than its own
    mean would. That is the point: a wrong blow-up exponent produces a curved
    linearization whose train-window line extrapolates badly here, and this
    number is what exposes it. Returns None if the window has no variance to
    explain (R^2 undefined).
    """
    k = len(ys)
    mean_y = sum(ys) / k
    ss_tot = sum((y - mean_y) ** 2 for y in ys)
    if ss_tot <= 0:
        return None
    ss_res = sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys))
    return 1 - ss_res / ss_tot


def classify_candidate(estimate, r_squared_threshold=0.98):
    """Tier 1 check: is this a credible single-run blow-up candidate?

    Threshold caveat: the meaning of ``estimate.r_squared`` depends on how the
    estimate was produced. The plain linear path reports an *in-sample* R^2;
    the ``fit_exponent=True`` path reports a *held-out* R^2, which runs
    systematically lower on the same data. One number (0.98) currently gates
    both, which is conservative for the exponent path. Once real solver data
    exists, calibrate the two thresholds separately (e.g. on the Stage 1
    validation runs) rather than assuming one value fits both distributions.
    """
    if estimate is None:
        return WinTier.NONE
    if estimate.r_squared >= r_squared_threshold:
        return WinTier.CANDIDATE
    return WinTier.NONE


def resolution_converged(t_star_by_resolution, rel_tol=0.02,
                         monotonicity_slack=1.5):
    """Tier 2 check: does the estimated blow-up time stabilize as
    resolution increases?

    `t_star_by_resolution` is a list of T* estimates ordered from coarsest
    to finest resolution (at least 3 needed). We require the finest two
    estimates to agree within `rel_tol` AND the successive differences to be
    *overall* contracting -- i.e. Cauchy-convergent, not just close.

    "Overall contracting" is deliberately looser than strict monotone
    shrinking: a genuinely converging refinement sequence often has a mild
    non-monotone wobble (e.g. diffs 0.10, 0.008, 0.009) from differing
    truncation errors at each level, and a strict `diffs[i] <= diffs[i-1]`
    rule would wrongly reject those and suppress the Tier 2 promotion rate.
    Instead we require the last diff to be no larger than the first, and no
    single diff to exceed its predecessor by more than `monotonicity_slack`x.
    """
    if len(t_star_by_resolution) < 3:
        raise ValueError("need at least 3 resolutions to assess convergence")

    diffs = [
        abs(t_star_by_resolution[i] - t_star_by_resolution[i - 1])
        for i in range(1, len(t_star_by_resolution))
    ]
    overall_contracting = diffs[-1] <= diffs[0]
    no_large_reversal = all(
        diffs[i] <= monotonicity_slack * diffs[i - 1]
        for i in range(1, len(diffs))
    )
    converged = diffs[-1] / abs(t_star_by_resolution[-1]) <= rel_tol
    return overall_contracting and no_large_reversal and converged


def classify(single_run_estimate, t_star_by_resolution=None,
             r_squared_threshold=0.98, rel_tol=0.02):
    """Overall win-tier classification, capped at NUMERICALLY_CONFIRMED.

    Tier 3 (a rigorous computer-assisted proof) is never returned here --
    it requires a dedicated validated-numerics pipeline built around a
    specific Tier-2 candidate, not something this diagnostic can automate.
    """
    tier = classify_candidate(single_run_estimate, r_squared_threshold)
    if tier is WinTier.NONE:
        return tier
    if t_star_by_resolution and resolution_converged(t_star_by_resolution, rel_tol):
        return WinTier.NUMERICALLY_CONFIRMED
    return tier
