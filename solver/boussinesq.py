"""Pseudo-spectral solver for the 2D Boussinesq system (PHASE1_PLAN.md, Gate 1a).

    w_t + u.grad w = th_x + nu*Lap w        (vorticity; buoyancy forcing th_x)
    th_t + u.grad th = kappa*Lap th         (temperature/density transport)
    u = grad^perp psi = (-psi_y, psi_x),  Lap psi = w      (Biot-Savart)

on the 2*pi-periodic square [0,2*pi)^2. This is the "poor man's 3D Euler": the
buoyancy force f=(0,th) has curl th_x, which is the entire singular mechanism.
`nu` (viscosity) and `kappa` (thermal diffusivity) are first-class; the inviscid
Euler-analog is nu=kappa=0.

Gate 1a is the DOUBLY-PERIODIC core (no wall yet); the Hou-Luo symmetry-wall is
layered on in Gate 1b. The method mirrors solver/gclm.py exactly so the harness
transfers:
- full fft2 pseudo-spectral (complex spectra, real fields); Biot-Savart is a
  Fourier multiplier w_hat -> u_hat.
- RK4 on the advection + buoyancy terms; viscosity/diffusion via an exact
  integrating-factor step exp(-nu*k^2*dt) (resp. kappa) after each RK4 step.
- 2/3-rule dealiasing on the quadratic advection products.
- Adaptive dt from the advective CFL: dt = min(dt_max, c2*dx/max|u|, c1/max|w|).

Artifact guards, first-class from the start (analogs of the gCLM guards):
- total vorticity ∫w dx and total ∫th dx are exactly conserved (the (0,0) mode
  is untouched by every term) -> mean_drift, normalized by an L1 scale.
- kinetic-energy balance d/dt(1/2∫|u|^2) = ∫ v*th dx - nu*∫w^2 dx (the periodic
  incompressible identity ∫|grad u|^2 = ∫w^2 gives the clean dissipation form)
  -> energy_balance_residual, the viscous-safe under-resolution signal.

Test hooks mirror gclm.py: `nonlinear=False` turns off advection (pure
diffusion); `buoyancy=False` turns off th_x (pure 2D Euler/NS on w); `frozen_u`
= (cu, cv) replaces the self-consistent velocity with a constant divergence-free
field, making the transport pure translation for the frozen-u acceptance check.
"""

import time
from dataclasses import dataclass, field

import numpy as np

TWO_PI = 2.0 * np.pi


def grid2d(n):
    """Uniform periodic grid on [0,2*pi)^2; returns (X, Y) with shape (n, n),
    indexing='ij' so axis 0 is x and axis 1 is y."""
    x = TWO_PI * np.arange(n) / n
    return np.meshgrid(x, x, indexing="ij")


def wavenumbers2d(n):
    """Integer wavenumber meshes (KX, KY) for fft2 on the 2*pi square, plus
    Ksq = KX^2+KY^2 and inv_Ksq (0 at the mean mode)."""
    k = np.fft.fftfreq(n, d=1.0 / n)  # 0,1,..,n/2-1,-n/2,..,-1 (integers)
    KX, KY = np.meshgrid(k, k, indexing="ij")
    Ksq = KX * KX + KY * KY
    inv_Ksq = np.zeros_like(Ksq)
    nz = Ksq > 0
    inv_Ksq[nz] = 1.0 / Ksq[nz]
    return KX, KY, Ksq, inv_Ksq


def dealias_mask2d(n):
    """2/3-rule mask over fft2 modes: keep |kx|<=n/3 AND |ky|<=n/3."""
    k = np.fft.fftfreq(n, d=1.0 / n)
    KX, KY = np.meshgrid(k, k, indexing="ij")
    cut = n / 3.0
    return (np.abs(KX) <= cut) & (np.abs(KY) <= cut)


def velocity_from_vorticity(w_hat, KX, KY, inv_Ksq):
    """u=(-psi_y, psi_x), Lap psi = w -> u_hat = i*KY*w_hat/k^2,
    v_hat = -i*KX*w_hat/k^2. Returns physical (u, v)."""
    n = w_hat.shape[0]
    u_hat = 1j * KY * w_hat * inv_Ksq
    v_hat = -1j * KX * w_hat * inv_Ksq
    u = np.fft.ifft2(u_hat).real
    v = np.fft.ifft2(v_hat).real
    return u, v


@dataclass
class BoussinesqResult:
    """Summary of one run — mirrors solver.gclm.SolverResult, plus theta_final."""

    outcome: str  # "no_blowup" | "blowup_candidate" | "diverged" | "max_steps_hit"
    early_exit_reason: str | None
    times: np.ndarray
    max_omega: np.ndarray  # max|w| at each sample time
    omega_final: np.ndarray
    theta_final: np.ndarray
    t_final: float
    n_timesteps: int
    dt_min: float
    wall_clock_seconds: float
    mean_drift: float  # max(|∫w drift|, |∫th drift|) / L1 scale
    energy_balance_residual: float
    conservation_drift: float  # max of the two above; the logged guard value
    params: dict = field(default_factory=dict)


def _rhs_hat(w_hat, th_hat, KX, KY, inv_Ksq, mask, nonlinear, buoyancy, frozen_u):
    """Spectral RHS of the non-stiff terms: -(u.grad w) + th_x, and -(u.grad th).
    Returns (dw_hat, dth_hat, u, v); u,v are the physical velocities (for CFL)."""
    n = w_hat.shape[0]
    if frozen_u is not None:
        u = np.full((n, n), float(frozen_u[0]))
        v = np.full((n, n), float(frozen_u[1]))
    else:
        u, v = velocity_from_vorticity(w_hat, KX, KY, inv_Ksq)

    dw_hat = np.zeros_like(w_hat)
    dth_hat = np.zeros_like(th_hat)
    if nonlinear:
        wx = np.fft.ifft2(1j * KX * w_hat).real
        wy = np.fft.ifft2(1j * KY * w_hat).real
        thx = np.fft.ifft2(1j * KX * th_hat).real
        thy = np.fft.ifft2(1j * KY * th_hat).real
        dw_hat += -np.fft.fft2(u * wx + v * wy) * mask
        dth_hat += -np.fft.fft2(u * thx + v * thy) * mask
    if buoyancy:
        dw_hat += 1j * KX * th_hat  # th_x
    return dw_hat, dth_hat, u, v


def _integral(f):
    """∫f over [0,2*pi)^2 = (2*pi)^2 * mean(f)."""
    return TWO_PI * TWO_PI * float(np.mean(f))


def solve_boussinesq(
    omega0,
    theta0,
    nu=0.0,
    kappa=0.0,
    t_max=10.0,
    dt_max=1e-2,
    c1=0.05,
    c2=0.4,
    amplification_factor=1e3,
    max_steps=200_000,
    early_decay_exit=None,
    nonlinear=True,
    buoyancy=True,
    frozen_u=None,
):
    """Integrate 2D Boussinesq from (omega0, theta0) on an n x n grid.

    frozen_u: None, or a constant (cu, cv) divergence-free velocity replacing the
    self-consistent field (the transport-only acceptance check).
    early_decay_exit: as in solve_gclm — {"fraction": f, "window": T}.
    """
    t_start_wall = time.perf_counter()
    omega0 = np.asarray(omega0, dtype=float)
    theta0 = np.asarray(theta0, dtype=float)
    n = omega0.shape[0]
    if omega0.shape != (n, n) or theta0.shape != (n, n):
        raise ValueError("omega0 and theta0 must be square n x n arrays")
    KX, KY, Ksq, inv_Ksq = wavenumbers2d(n)
    mask = dealias_mask2d(n)
    dx = TWO_PI / n

    w_hat = np.fft.fft2(omega0) * mask
    th_hat = np.fft.fft2(theta0) * mask
    w = np.fft.ifft2(w_hat).real
    th = np.fft.ifft2(th_hat).real

    m0 = float(np.max(np.abs(w)))
    if m0 == 0.0:
        raise ValueError("omega0 is identically zero")

    times = [0.0]
    max_omega = [m0]
    # Artifact-guard tracking.
    w_int0, th_int0 = _integral(w), _integral(th)
    max_w_int_dev = 0.0
    max_th_int_dev = 0.0
    max_l1_w = _integral(np.abs(w))
    max_l1_th = max(_integral(np.abs(th)), 1e-300)

    def kinetic_energy_and_prod(w_hat_):
        u_, v_ = velocity_from_vorticity(w_hat_, KX, KY, inv_Ksq)
        w_ = np.fft.ifft2(w_hat_).real
        th_ = np.fft.ifft2(th_hat).real
        e_ = 0.5 * TWO_PI * TWO_PI * float(np.mean(u_ * u_ + v_ * v_))
        # d/dt E_k = ∫ v*th dx - nu*∫ w^2 dx  (periodic incompressible identity).
        p_ = TWO_PI * TWO_PI * float(np.mean(v_ * th_)) - nu * TWO_PI * TWO_PI * float(
            np.mean(w_ * w_)
        )
        return e_, p_

    e_prev, p_prev = kinetic_energy_and_prod(w_hat)
    e_accum_err = 0.0
    max_e = max(abs(e_prev), 1e-300)

    outcome = None
    early_exit_reason = None
    t = 0.0
    n_steps = 0
    dt_min_realized = np.inf
    decay_window_start = None
    m_prev = m0

    visc_w = None
    while t < t_max:
        if n_steps >= max_steps:
            outcome = "max_steps_hit"
            break

        m = float(np.max(np.abs(w)))
        if nonlinear or buoyancy:
            if frozen_u is not None:
                speed = np.hypot(frozen_u[0], frozen_u[1])
            else:
                u_, v_ = velocity_from_vorticity(w_hat, KX, KY, inv_Ksq)
                speed = float(np.max(np.hypot(u_, v_)))
            dt = min(dt_max, c2 * dx / max(speed, 1e-12), c1 / max(m, 1e-12))
        else:
            dt = dt_max
        dt = min(dt, t_max - t)
        dt_min_realized = min(dt_min_realized, dt)

        if nonlinear or buoyancy:
            k1w, k1t, _, _ = _rhs_hat(w_hat, th_hat, KX, KY, inv_Ksq, mask,
                                      nonlinear, buoyancy, frozen_u)
            k2w, k2t, _, _ = _rhs_hat(w_hat + 0.5 * dt * k1w, th_hat + 0.5 * dt * k1t,
                                      KX, KY, inv_Ksq, mask, nonlinear, buoyancy, frozen_u)
            k3w, k3t, _, _ = _rhs_hat(w_hat + 0.5 * dt * k2w, th_hat + 0.5 * dt * k2t,
                                      KX, KY, inv_Ksq, mask, nonlinear, buoyancy, frozen_u)
            k4w, k4t, _, _ = _rhs_hat(w_hat + dt * k3w, th_hat + dt * k3t,
                                      KX, KY, inv_Ksq, mask, nonlinear, buoyancy, frozen_u)
            w_hat = w_hat + (dt / 6.0) * (k1w + 2 * k2w + 2 * k3w + k4w)
            th_hat = th_hat + (dt / 6.0) * (k1t + 2 * k2t + 2 * k3t + k4t)
        if nu > 0.0:
            w_hat = w_hat * np.exp(-nu * Ksq * dt)
        if kappa > 0.0:
            th_hat = th_hat * np.exp(-kappa * Ksq * dt)

        t += dt
        n_steps += 1
        w = np.fft.ifft2(w_hat).real
        th = np.fft.ifft2(th_hat).real
        m = float(np.max(np.abs(w)))
        times.append(t)
        max_omega.append(m)

        if not np.isfinite(m):
            outcome = "diverged"
            break

        max_w_int_dev = max(max_w_int_dev, abs(_integral(w) - w_int0))
        max_th_int_dev = max(max_th_int_dev, abs(_integral(th) - th_int0))
        max_l1_w = max(max_l1_w, _integral(np.abs(w)))
        max_l1_th = max(max_l1_th, _integral(np.abs(th)))
        e_now, p_now = kinetic_energy_and_prod(w_hat)
        e_accum_err += abs((e_now - e_prev) - 0.5 * dt * (p_now + p_prev))
        e_prev, p_prev = e_now, p_now
        max_e = max(max_e, abs(e_now))

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

    mean_drift = max(max_w_int_dev / max(max_l1_w, 1e-300),
                     max_th_int_dev / max(max_l1_th, 1e-300))
    energy_residual = e_accum_err / max(max_e, 1e-300)
    return BoussinesqResult(
        outcome=outcome,
        early_exit_reason=early_exit_reason,
        times=np.array(times),
        max_omega=np.array(max_omega),
        omega_final=w,
        theta_final=th,
        t_final=t,
        n_timesteps=n_steps,
        dt_min=float(dt_min_realized) if np.isfinite(dt_min_realized) else 0.0,
        wall_clock_seconds=time.perf_counter() - t_start_wall,
        mean_drift=mean_drift,
        energy_balance_residual=energy_residual,
        conservation_drift=max(mean_drift, energy_residual),
        params={
            "nu": nu,
            "kappa": kappa,
            "resolution_N": n,
            "t_max": t_max,
            "dt_max": dt_max,
            "c1": c1,
            "c2": c2,
            "amplification_factor": amplification_factor,
            "max_steps": max_steps,
            "buoyancy": buoyancy,
            "nonlinear": nonlinear,
        },
    )
