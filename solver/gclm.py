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
    params: dict = field(default_factory=dict)


def _nonlinear_rhs_hat(w_hat, k, mask, a, frozen_u):
    """Dealiased spectral RHS of the nonlinear terms: -a*u*w_x + w*u_x."""
    n = 2 * (len(w_hat) - 1)
    w = np.fft.irfft(w_hat, n)
    w_x = np.fft.irfft(derivative_hat(w_hat, k), n)
    if frozen_u is not None:
        u = np.full(n, frozen_u)
        u_x = np.zeros(n)
    else:
        u = np.fft.irfft(velocity_hat(w_hat, k), n)
        u_x = np.fft.irfft(hilbert_hat(w_hat, k), n)
    rhs = -a * u * w_x + w * u_x
    return np.fft.rfft(rhs) * mask, u


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
        conservation_drift=max(mean_drift, energy_residual),
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
    w_x = np.fft.irfft(derivative_hat(np.fft.rfft(w), k), n)
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
    exact = np.abs(w0) < 1e-12
    if np.any(exact):
        h_grid = np.fft.irfft(h_hat, n_scan)
        best_h = max(best_h, float(np.max(h_grid[exact])))

    if best_h <= 0:
        return None  # no blow-up for this data
    return 2.0 / best_h
