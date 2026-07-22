"""Sanity tests for win_condition.py.

These prove the diagnostics work on cases where we already know the answer,
before we ever plug in a real PDE solver:

1. A known analytic finite-time blow-up (dy/dt = y^2, y(0)=1 -> y(t) =
   1/(1-t), blowing up at t=1) must be detected as a Tier 1 candidate with
   an accurate T* and near-perfect fit.
2. Decaying and steady-state series (no real growth) must NOT be flagged.
3. A resolution study with shrinking, converging T* estimates must pass
   Tier 2; one that doesn't converge must not.
"""

from win_condition import (
    estimate_blowup_time,
    classify_candidate,
    resolution_converged,
    classify,
    InsufficientDataError,
    WinTier,
)


def _rk4_y_prime_equals_y_squared(t0, y0, dt, n_steps):
    """Integrate dy/dt = y^2 with classic RK4, used as a stand-in
    'simulation' with a known analytic blow-up at t = t0 + 1/y0."""
    def f(y):
        return y * y

    times = [t0]
    ys = [y0]
    t, y = t0, y0
    for _ in range(n_steps):
        k1 = f(y)
        k2 = f(y + 0.5 * dt * k1)
        k3 = f(y + 0.5 * dt * k2)
        k4 = f(y + dt * k3)
        y = y + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t = t + dt
        times.append(t)
        ys.append(y)
    return times, ys


def test_detects_known_analytic_blowup():
    # y(t) = 1/(1-t) blows up at t=1. Integrate up to t=0.9, well short of
    # the singularity, using only the "simulated" data up to that point --
    # exactly the situation a real solver would be in.
    times, ys = _rk4_y_prime_equals_y_squared(t0=0.0, y0=1.0, dt=0.01, n_steps=90)

    estimate = estimate_blowup_time(times, ys, tail_fraction=0.5)
    assert estimate is not None, "expected a forward blow-up signal"
    assert abs(estimate.t_star - 1.0) < 0.01, f"expected T* ~= 1.0, got {estimate.t_star}"
    assert estimate.r_squared > 0.999, f"expected near-perfect fit, got {estimate.r_squared}"

    tier = classify_candidate(estimate)
    assert tier is WinTier.CANDIDATE, f"expected CANDIDATE, got {tier}"


def test_detects_nongeneric_blowup_with_exponent_fit():
    # Synthetic non-generic blow-up M ~ (T*-t)^-alpha with alpha=2, T*=1.0.
    # The plain linear fit of 1/M is curved here (1/M ~ (T*-t)^2), so
    # fit_exponent=True must recover alpha ~= 2 and a good held-out fit, while
    # the default linear fit would under-fit it.
    alpha_true, t_star_true = 2.0, 1.0
    times = [0.5 + 0.005 * i for i in range(80)]  # tail approaching T*=1.0
    vorticity = [(t_star_true - t) ** (-alpha_true) for t in times]

    est = estimate_blowup_time(times, vorticity, tail_fraction=1.0, fit_exponent=True)
    assert est is not None, "expected a forward blow-up signal"
    assert abs(est.exponent - alpha_true) < 0.15, f"expected alpha ~= 2, got {est.exponent}"
    assert abs(est.t_star - t_star_true) < 0.02, f"expected T* ~= 1.0, got {est.t_star}"
    assert est.r_squared > 0.98, f"correct exponent should clear the gate, got {est.r_squared}"
    assert classify_candidate(est) is WinTier.CANDIDATE


def test_exponent_fit_requires_enough_tail_to_cross_validate():
    # Too few tail points to honestly hold out a validation window. Must raise
    # the dedicated InsufficientDataError (still a ValueError, so older callers
    # keep working) rather than returning None -- a None here would let a
    # bisection caller misread "run too short to fit" as "no blow-up".
    times = [0.1 * i for i in range(5)]
    vorticity = [1.0 / (1.0 - t) for t in times]
    try:
        estimate_blowup_time(times, vorticity, tail_fraction=1.0, fit_exponent=True)
    except InsufficientDataError:
        pass
    else:
        raise AssertionError("expected InsufficientDataError when the tail is too short to cross-validate")
    assert issubclass(InsufficientDataError, ValueError)


def test_rejects_decaying_series():
    times = [t * 0.1 for t in range(20)]
    vorticity = [2.71828 ** (-t) for t in times]  # exp(-t): decaying, not blowing up

    estimate = estimate_blowup_time(times, vorticity)
    assert estimate is None, "decaying vorticity must not register as a blow-up signal"
    assert classify_candidate(estimate) is WinTier.NONE


def test_rejects_steady_state():
    times = [t * 0.1 for t in range(20)]
    vorticity = [1.0 for _ in times]  # flat: no growth at all

    estimate = estimate_blowup_time(times, vorticity)
    assert estimate is None, "flat vorticity must not register as a blow-up signal"
    assert classify_candidate(estimate) is WinTier.NONE


def test_resolution_converged_accepts_shrinking_convergent_series():
    t_stars = [1.10, 1.02, 1.005, 1.001]
    assert resolution_converged(t_stars, rel_tol=0.01) is True


def test_resolution_converged_rejects_non_convergent_series():
    t_stars = [1.10, 1.30, 0.90, 1.50]  # jumps around, doesn't settle
    assert resolution_converged(t_stars) is False


def test_full_classification_reaches_numerically_confirmed():
    times, ys = _rk4_y_prime_equals_y_squared(t0=0.0, y0=1.0, dt=0.01, n_steps=90)
    estimate = estimate_blowup_time(times, ys)

    converging_resolutions = [1.10, 1.02, 1.005, 1.0009]
    tier = classify(estimate, t_star_by_resolution=converging_resolutions)
    assert tier is WinTier.NUMERICALLY_CONFIRMED, f"expected NUMERICALLY_CONFIRMED, got {tier}"


def test_full_classification_stays_candidate_without_resolution_study():
    times, ys = _rk4_y_prime_equals_y_squared(t0=0.0, y0=1.0, dt=0.01, n_steps=90)
    estimate = estimate_blowup_time(times, ys)

    tier = classify(estimate)  # no resolution study supplied
    assert tier is WinTier.CANDIDATE, f"expected CANDIDATE, got {tier}"


if __name__ == "__main__":
    tests = [obj for name, obj in list(globals().items()) if name.startswith("test_")]
    passed = 0
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
        passed += 1
    print(f"\n{passed}/{len(tests)} tests passed.")
