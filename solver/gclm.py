"""Pseudo-spectral solver for the generalized Constantin–Lax–Majda family.

    w_t + a*u*w_x = w*u_x + nu*w_xx,      u_x = H(w)

on a 2*pi-periodic domain. `a` and `nu` are first-class parameters
(PLAN.md Stage 1): a=0 recovers CLM (closed-form blow-up, used for
validation), a=1 is De Gregorio — one code path, not two.

Method (per PLAN.md):
- rfft pseudo-spectral; Hilbert transform is a Fourier multiplier.
- RK4 on the nonlinear terms; viscosity via an exact integrating-factor
  step exp(-nu*k^2*dt) after each RK4 step (exact when the nonlinearity
  is off, which is what the pure-diffusion validation check exercises).
- 2/3-rule dealiasing on the quadratic products.
- Adaptive dt satisfying BOTH constraints:
      dt = min(dt_max, c1/max|w|, c2*dx/max|u|)
  the second being the advective CFL for the a*u*w_x transport term.

Stop criteria mirror LOGGING.md's `stop_criteria` config block: t_max,
max_steps, an amplification factor that declares "blowup_candidate", an
optional early-decay exit, and NaN/Inf detection ("diverged"). The result
carries the per-run artifact-guard numbers (mean-invariant drift and
energy-balance residual, both normalized by a solution scale).

Test hooks: `nonlinear=False` turns off both nonlinear terms (pure
diffusion); `frozen_u=c` replaces the self-consistent velocity with a
constant, making the equation pure transport w_t + a*c*w_x = 0 — the
frozen-u advection check Stage 1's acceptance criterion requires.
"""

import time
from dataclasses import dataclass, field

import numpy as np

from solver.spectral_utils import (
    TWO_PI,
    dealias_mask,
    derivative_hat,
    energy,
    energy_production,
    hilbert_hat,
    integral,
    l1_norm,
    velocity_hat,
    wavenumbers,
)


@dataclass
class SolverResult:
    """Summary of one (genome, a, nu) run — the fields LOGGING.md's
    `solver_run` event needs, plus the final field for chaining/tests."""

    outcome: str  # "no_blowup" | "blowup_candidate" | "diverged" | "max_steps_hit"
    early_exit_reason: str | None
    times: np.ndarray  # sample times, starting at t=0
    max_omega: np.ndarray  # max|w| at each sample time
    omega_final: np.ndarray
    t_final: float
    n_timesteps: int
    dt_min: float
    wall_clock_seconds: float
    mean_drift: float  # |∫w dx drift| / ||w||_1 scale (never / the invariant)
    energy_balance_residual: float  # viscous-safe under-resolution signal
    conservation_drift: float  # max of the two above; the logged guard value
    # True iff either guard input above was NaN. The logged conservation_drift is
    # then NaN too -- see the G3 note in solve_gclm. A NaN guard is its own failure
    # state, never a small number (leg 92 / Route-GLA).
    guard_nan: bool = False
    params: dict = field(default_factory=dict)


def _nonlinear_rhs_hat(w_hat, k, mask, a, frozen_u):
    """Dealiased spectral RHS of the nonlinear terms: -a*u*w_x + w*u_x."""
    n = 2 * (len(w_hat) - 1)
    w = np.fft.irfft(w_hat, n)
    w_x = np.fft.irfft(derivative_hat(w_hat, k, n), n)
    if frozen_u is not None:
        u = np.full(n, frozen_u)
        u_x = np.zeros(n)
    else:
        u = np.fft.irfft(velocity_hat(w_hat, k), n)
        u_x = np.fft.irfft(hilbert_hat(w_hat, k), n)
    rhs = -a * u * w_x + w * u_x
    return np.fft.rfft(rhs) * mask, u


def _require_finite(name, value, what):
    """Reject a non-finite scalar run parameter, by name, before it is ever compared.

    Leg 92 (Route-GLA) measured the failure this closes: every stop criterion in
    `solve_gclm` is a bare comparison, and EVERY comparison against NaN is False.
    `t_max = nan` makes `while t < t_max` false immediately -- zero timesteps, and a
    returned `outcome="no_blowup"` with a wholly finite payload, a clean verdict from a
    run that never happened. `amplification_factor = nan` disables the blow-up detector
    outright: at a = 1e4 the clean run reports `blowup_candidate` and the poisoned one
    reports `diverged`. A criterion that cannot fire is not a criterion, and silently
    dropping it is worse than refusing it, so it is refused here.
    """
    v = float(value)
    if not np.isfinite(v):
        raise ValueError(
            "%s = %r is not finite. %s Every stop criterion in solve_gclm is a bare "
            "comparison and every comparison against NaN is False, so a non-finite "
            "value here is silently DROPPED rather than applied -- the criterion "
            "stops existing without saying so." % (name, v, what))
    return v


def solve_gclm(
    omega0,
    a=0.0,
    nu=0.0,
    t_max=10.0,
    dt_max=1e-2,
    c1=0.05,
    c2=0.4,
    amplification_factor=1e3,
    max_steps=200_000,
    early_decay_exit=None,
    nonlinear=True,
    frozen_u=None,
):
    """Integrate gCLM from omega0 (values on grid(N), N = len(omega0)).

    early_decay_exit: None, or a dict {"fraction": f, "window": T} — exit
    "no_blowup" early once max|w| has stayed below f * max|w(0)| and been
    non-increasing for a continuous time window of length T (the dominant
    per-run compute saver per PLAN.md's compute plan; audited via
    early_exit_reason).
    """
    # -- run-parameter validation (leg 92 / Route-GLA repairs G2 and G4) --------
    # These run BEFORE any state is built, so an invalid request never produces a
    # partially-integrated result. NaN/negative `omega0` is deliberately NOT validated
    # here: leg 92 measured that poisoned vorticity already reaches outcome="diverged"
    # on step 1 in all 12 cases, and a wild but finite `a` is honestly propagated. Those
    # paths were already correct and are left exactly as they were.
    nu = float(nu)
    if nu < 0.0 or np.isnan(nu):
        raise ValueError(
            "nu = %r is not an admissible viscosity: nu >= 0 is required (nu = 0, the "
            "inviscid case, IS admissible; nu = -0.0 is 0.0 and is fine). A negative nu "
            "is anti-diffusion -- an energy source, an ill-posed backward heat equation "
            "-- and a NaN nu is no viscosity at all. Both used to fail the `if nu > 0.0` "
            "gate below and run BITWISE INVISCID without a word: leg 92 measured "
            "nu = -1.0 returning omega_final identical to the nu = 0 run, outcome "
            "'no_blowup', entire payload finite." % nu)
    t_max = _require_finite(
        "t_max", t_max, "It is the integration horizon in `while t < t_max`.")
    if t_max <= 0.0:
        raise ValueError(
            "t_max = %r is not a positive integration horizon. `while t < t_max` is "
            "false at t = 0, so the run takes ZERO timesteps and still returns "
            "outcome='no_blowup' with conservation_drift = 0.0 -- a clean verdict from "
            "a run that never happened (leg 92 measured exactly this at t_max = -1.0)."
            % t_max)
    amplification_factor = _require_finite(
        "amplification_factor", amplification_factor,
        "It is the blow-up DETECTOR threshold in `m >= amplification_factor * m0`.")
    dt_max = _require_finite("dt_max", dt_max, "It is the timestep ceiling.")
    c1 = _require_finite("c1", c1, "It is the amplitude CFL coefficient.")
    c2 = _require_finite("c2", c2, "It is the advective CFL coefficient.")
    if not (dt_max > 0.0 and c1 > 0.0 and c2 > 0.0):
        raise ValueError(
            "dt_max = %r, c1 = %r, c2 = %r: all three timestep controls must be "
            "strictly positive; a non-positive one makes dt <= 0 and the integration "
            "cannot advance." % (dt_max, c1, c2))
    if not np.isfinite(max_steps):
        raise ValueError(
            "max_steps = %r is not finite; `n_steps >= max_steps` would never fire and "
            "the step budget would silently stop existing." % (max_steps,))

    t_start_wall = time.perf_counter()
    omega0 = np.asarray(omega0, dtype=float)
    n = len(omega0)
    k = wavenumbers(n)
    mask = dealias_mask(n)
    dx = TWO_PI / n
    k_sq = k * k

    w_hat = np.fft.rfft(omega0) * mask
    w = np.fft.irfft(w_hat, n)

    m0 = float(np.max(np.abs(w)))
    if m0 == 0.0:
        raise ValueError("omega0 is identically zero")

    times = [0.0]
    max_omega = [m0]
    # Artifact-guard tracking: mean invariant, L1 scale, energy + production.
    mean0 = integral(w)
    max_abs_mean_dev = 0.0
    max_l1 = l1_norm(w)
    e_prev = energy(w)
    p_prev = energy_production(w, a, nu) if nonlinear else -2.0 * nu * energy_from_gradient(w)
    e_accum_err = 0.0
    max_e = e_prev

    outcome = None
    early_exit_reason = None
    t = 0.0
    n_steps = 0
    dt_min_realized = np.inf
    decay_window_start = None  # time since which the decay-exit condition held
    m_prev = m0

    while t < t_max:
        if n_steps >= max_steps:
            outcome = "max_steps_hit"
            break

        m = float(np.max(np.abs(w)))
        if nonlinear:
            if frozen_u is not None:
                u_max = abs(frozen_u)
            else:
                u_max = float(np.max(np.abs(np.fft.irfft(velocity_hat(w_hat, k), n))))
            dt = min(dt_max, c1 / m, c2 * dx / max(u_max, 1e-12))
        else:
            dt = dt_max
        dt = min(dt, t_max - t)
        dt_min_realized = min(dt_min_realized, dt)

        if nonlinear:
            k1, _ = _nonlinear_rhs_hat(w_hat, k, mask, a, frozen_u)
            k2, _ = _nonlinear_rhs_hat(w_hat + 0.5 * dt * k1, k, mask, a, frozen_u)
            k3, _ = _nonlinear_rhs_hat(w_hat + 0.5 * dt * k2, k, mask, a, frozen_u)
            k4, _ = _nonlinear_rhs_hat(w_hat + dt * k3, k, mask, a, frozen_u)
            w_hat = w_hat + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        if nu > 0.0:
            w_hat = w_hat * np.exp(-nu * k_sq * dt)

        t += dt
        n_steps += 1
        w = np.fft.irfft(w_hat, n)
        m = float(np.max(np.abs(w)))
        times.append(t)
        max_omega.append(m)

        if not np.isfinite(m):
            outcome = "diverged"
            break

        # Artifact guards, accumulated every step (cheap at Stage 1 scale).
        max_abs_mean_dev = max(max_abs_mean_dev, abs(integral(w) - mean0))
        max_l1 = max(max_l1, l1_norm(w))
        e_now = energy(w)
        p_now = (
            energy_production(w, a, nu)
            if nonlinear
            else -2.0 * nu * energy_from_gradient(w)
        )
        e_accum_err += abs((e_now - e_prev) - 0.5 * dt * (p_now + p_prev))
        e_prev, p_prev = e_now, p_now
        max_e = max(max_e, e_now)

        if m >= amplification_factor * m0:
            outcome = "blowup_candidate"
            break

        if early_decay_exit is not None:
            below = m < early_decay_exit["fraction"] * m0
            shrinking = m <= m_prev * (1.0 + 1e-12)
            if below and shrinking:
                if decay_window_start is None:
                    decay_window_start = t
                elif t - decay_window_start >= early_decay_exit["window"]:
                    outcome = "no_blowup"
                    early_exit_reason = "decay_exit"
                    break
            else:
                decay_window_start = None
        m_prev = m

    if outcome is None:
        outcome = "no_blowup"

    mean_drift = max_abs_mean_dev / max(max_l1, 1e-300)
    energy_residual = e_accum_err / max(max_e, 1e-300)
    # G3 (leg 92 / Route-GLA). This used to be `max(mean_drift, energy_residual)`, and
    # Python's builtin max returns `b` only when `b > a` -- NaN loses every comparison,
    # so max(finite, nan) == finite. The ONE number LOGGING.md's `solver_run` event
    # records as the artifact guard was precisely the one that swallowed the NaN: at
    # a = 1e12 the energy residual is NaN while the logged conservation_drift read
    # 4.926e-17, i.e. "clean", on a run that reached max|w| = 9.673e+144.
    # A NaN guard input is now its own reportable failure state: the flag `guard_nan` is
    # set and the logged value is NaN, never a small number. np.nanmax is used for the
    # ordinary path so the intent ("the larger of the two") is explicit rather than
    # resting on builtin max's NaN behaviour either way; +inf still propagates as +inf.
    _guards = np.array([mean_drift, energy_residual], dtype=float)
    guard_nan = bool(np.any(np.isnan(_guards)))
    conservation_drift = float("nan") if guard_nan else float(np.nanmax(_guards))
    return SolverResult(
        outcome=outcome,
        early_exit_reason=early_exit_reason,
        times=np.array(times),
        max_omega=np.array(max_omega),
        omega_final=w,
        t_final=t,
        n_timesteps=n_steps,
        dt_min=float(dt_min_realized) if np.isfinite(dt_min_realized) else 0.0,
        wall_clock_seconds=time.perf_counter() - t_start_wall,
        mean_drift=mean_drift,
        energy_balance_residual=energy_residual,
        conservation_drift=conservation_drift,
        guard_nan=guard_nan,
        params={
            "a": a,
            "nu": nu,
            "resolution_N": n,
            "t_max": t_max,
            "dt_max": dt_max,
            "c1": c1,
            "c2": c2,
            "amplification_factor": amplification_factor,
            "max_steps": max_steps,
        },
    )


def energy_from_gradient(w):
    """(1/2)∫w_x² — dissipation integrand for the linear-only energy balance."""
    n = len(w)
    k = wavenumbers(n)
    w_x = np.fft.irfft(derivative_hat(np.fft.rfft(w), k, n), n)
    return np.pi * float(np.mean(w_x * w_x))


def clm_analytic_blowup_time(omega0_fn, n_scan=4096):
    """Analytic CLM (a=0, nu=0) blow-up time for initial data w0.

    The CLM closed-form solution
        w(x,t) = 4*w0 / ((2 - t*H(w0))^2 + t^2*w0^2)
    blows up iff some x* has w0(x*) = 0 and H(w0)(x*) > 0, at
        T* = 2 / max{ H(w0)(x) : w0(x) = 0 }.
    Zeros are located by sign change on a fine grid, refined by bisection
    of the (band-limited, spectrally interpolated) w0.
    """
    from solver.spectral_utils import grid

    x = grid(n_scan)
    w0 = omega0_fn(x)
    w0_hat = np.fft.rfft(w0)
    k = wavenumbers(n_scan)
    h_hat = hilbert_hat(w0_hat, k)

    def eval_trig(coeffs_hat, xq):
        # Direct evaluation of the trigonometric interpolant at arbitrary xq.
        ks = np.arange(len(coeffs_hat))
        weights = np.where((ks == 0) | (ks == n_scan // 2), 1.0, 2.0)
        return np.real(
            np.sum(weights * coeffs_hat * np.exp(1j * np.outer(xq, ks)), axis=1)
        ) / n_scan

    best_h = -np.inf
    sign_change = np.where(np.diff(np.sign(np.concatenate([w0, w0[:1]]))) != 0)[0]
    for i in sign_change:
        lo, hi = x[i], x[i] + TWO_PI / n_scan
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if eval_trig(w0_hat, np.array([lo]))[0] * eval_trig(w0_hat, np.array([mid]))[0] <= 0:
                hi = mid
            else:
                lo = mid
        x_zero = 0.5 * (lo + hi)
        h_val = eval_trig(h_hat, np.array([x_zero]))[0]
        best_h = max(best_h, h_val)
    # Grid points that are exactly zeros (e.g. x=0, pi for sine data).
    #
    # G1 (leg 92 / Route-GLA). This tolerance used to be the ABSOLUTE constant 1e-12,
    # applied to data whose amplitude was never measured. Below that amplitude EVERY
    # grid point satisfies it, so the "zero set" became the whole grid and best_h
    # became the GLOBAL max of H(w0) instead of its max over the actual zero set --
    # returning a finite, positive, entirely ordinary-looking blow-up time that was up
    # to 1.5x too early, with no flag. The CLM closed form is exactly homogeneous of
    # degree -1 in amplitude, so eps*T*(eps*w0) must not depend on eps; leg 92 measured
    # it running 4.0 -> 2.667 (relative violation saturating at exactly 1/3) as the
    # amplitude shrank below the fixed constant.
    #
    # The tolerance is therefore RELATIVE to the data's own scale, which is what makes
    # it obey the same amplitude homogeneity the closed form does: scaling w0 by eps
    # scales the tolerance by eps and leaves `exact` -- and hence T* -- unchanged.
    # At the O(1) amplitudes every production caller uses, 1e-12 * scale reproduces the
    # old constant to the bit, which is why this repair moves no banked number.
    scale = float(np.max(np.abs(w0))) if w0.size else 0.0
    exact = np.abs(w0) < 1e-12 * scale
    if np.any(exact):
        h_grid = np.fft.irfft(h_hat, n_scan)
        best_h = max(best_h, float(np.max(h_grid[exact])))

    if best_h <= 0:
        return None  # no blow-up for this data
    return 2.0 / best_h
