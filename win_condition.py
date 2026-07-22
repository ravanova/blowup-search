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
    iff that ``alpha`` is correct, so we pick the ``alpha`` whose linearized
    fit maximizes ``R^2`` and report it on the estimate. ``slope`` is then the
    slope in that linearized coordinate, not of ``1/M`` directly.

    Returns None if there's no forward-pointing blow-up signal, otherwise a
    BlowupEstimate.
    """
    n = len(times)
    if n < 4:
        raise ValueError("need at least 4 samples to fit a trend")

    tail_start = max(0, int(n * (1 - tail_fraction)))
    xs = times[tail_start:]
    ms = vorticity_max[tail_start:]

    if any(m <= 0 for m in ms):
        # Non-positive vorticity max -> reciprocal is undefined. Treat as "no
        # valid signal" rather than crashing; a real blow-up never gets here.
        return None
    inv = [1.0 / m for m in ms]

    def _fit_for_exponent(alpha):
        zs = [v ** (1.0 / alpha) for v in inv]
        slope, intercept, r_squared = _linear_regression(xs, zs)
        if slope >= 0:
            return None  # linearized reciprocal isn't shrinking -> no blow-up
        t_star = -intercept / slope
        if t_star <= xs[-1]:
            return None  # extrapolated crossing is in the past -> not forward
        return slope, r_squared, t_star

    grid = [1.0] if not fit_exponent else (exponent_grid or _DEFAULT_EXPONENT_GRID)
    best = None  # (r_squared, alpha, slope, t_star)
    for alpha in grid:
        res = _fit_for_exponent(alpha)
        if res is None:
            continue
        slope, r_squared, t_star = res
        if best is None or r_squared > best[0]:
            best = (r_squared, alpha, slope, t_star)

    if best is None:
        return None

    r_squared, alpha, slope, t_star = best
    return BlowupEstimate(
        t_star=t_star,
        r_squared=r_squared,
        slope=slope,
        last_time=xs[-1],
        n_points=len(xs),
        exponent=alpha,
    )


def classify_candidate(estimate, r_squared_threshold=0.98):
    """Tier 1 check: is this a credible single-run blow-up candidate?"""
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
