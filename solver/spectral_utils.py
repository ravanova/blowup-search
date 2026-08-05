"""Spectral helpers for the gCLM solver (PLAN.md Stage 1).

Everything works on a uniform periodic grid on [0, 2*pi) with real fields,
so transforms are rfft/irfft. Conventions:

- Hilbert transform: H(e^{ikx}) = -i*sign(k)*e^{ikx}, so H(sin x) = -cos x.
  This is the convention under which the CLM equation w_t = w*H(w) has the
  closed-form blow-up solution used by test_solver_clm.py.
- Velocity: u_x = H(w) with u chosen zero-mean, i.e.
  u_hat[k] = -w_hat[k]/|k| for k != 0, u_hat[0] = 0.
- Dealiasing: 2/3 rule (both gCLM nonlinear terms are quadratic).

The invariant/energy-balance evaluations at the bottom implement the
artifact-guard design from PLAN.md Stage 1 / LOGGING.md: drift is always
normalized by a solution scale by the caller, never by the invariant's own
(possibly zero) value.
"""

import numpy as np

TWO_PI = 2.0 * np.pi


def grid(n):
    """Uniform periodic grid on [0, 2*pi): n points, spacing 2*pi/n."""
    return TWO_PI * np.arange(n) / n


def wavenumbers(n):
    """rfft wavenumbers 0..n//2 for a 2*pi-periodic domain."""
    return np.fft.rfftfreq(n, d=1.0 / n)


def dealias_mask(n):
    """2/3-rule mask over rfft modes: keep |k| <= n/3."""
    return wavenumbers(n) <= n / 3.0


def hilbert_hat(w_hat, k):
    """Hilbert transform in Fourier space: multiply by -i*sign(k)."""
    return -1j * np.sign(k) * w_hat


def velocity_hat(w_hat, k):
    """u_hat with u_x = H(w) and zero mean: u_hat[k] = -w_hat[k]/|k|, k != 0."""
    u_hat = np.zeros_like(w_hat)
    nz = k != 0
    u_hat[nz] = -w_hat[nz] / np.abs(k[nz])
    return u_hat


def derivative_hat(w_hat, k, n):
    """Spectral d/dx on an n-point real grid: multiply by i*k.

    The last rfft coefficient is zeroed ONLY when n is even, where it is the
    Nyquist mode -- an odd derivative of a real field has no well-defined
    value there, and dropping it is the standard treatment. When n is ODD
    there is no Nyquist mode: rfftfreq runs 0..(n-1)/2 and the last entry is
    an ordinary, fully resolved wavenumber, differentiated like any other.

    `n` is REQUIRED and cannot be inferred: rfft of an n-point real signal
    has n//2 + 1 coefficients, which is the same count for n = 2m and
    n = 2m - 1 (n = 8 and n = 9 both give 5), and `wavenumbers` returns the
    identical integers for both. The parity therefore has to come from the
    caller. Before Leg 0's fix this function took (w_hat, k) and zeroed the
    last coefficient unconditionally, which destroyed the k = (n-1)/2 mode at
    odd n -- relative sup error 1.000 on data supported there (leg 66). The
    defect was latent: every call site passed an even n.
    """
    if len(w_hat) != n // 2 + 1:
        raise ValueError(
            f"derivative_hat: {len(w_hat)} rfft coefficients is not the "
            f"{n // 2 + 1} expected for an n={n} grid"
        )
    d = 1j * k * w_hat
    if n % 2 == 0 and len(w_hat) > 1:
        d[-1] = 0.0
    return d


# --- integral quantities (trapezoid == exact spectral quadrature on a
# --- uniform periodic grid: integral = 2*pi * mean) ---

def integral(f):
    """integral of f over [0, 2*pi)."""
    return TWO_PI * float(np.mean(f))


def l1_norm(w):
    """||w||_1 = integral |w| — the solution scale drift is normalized by."""
    return TWO_PI * float(np.mean(np.abs(w)))


def energy(w):
    """E = (1/2) * integral w^2."""
    return np.pi * float(np.mean(w * w))


def energy_production(w, a, nu):
    """Exact rate d/dt E for gCLM: w_t + a*u*w_x = w*u_x + nu*w_xx.

    d/dt (1/2)∫w² = (a/2 + 1)∫ w²·H(w) − nu·∫ w_x².

    When the solver is resolved, the measured dE/dt matches this; the
    accumulated mismatch is the energy-balance residual logged per run
    (the viscous generalization of invariant drift — see LOGGING.md).
    """
    n = len(w)
    k = wavenumbers(n)
    w_hat = np.fft.rfft(w)
    h_w = np.fft.irfft(hilbert_hat(w_hat, k), n)
    w_x = np.fft.irfft(derivative_hat(w_hat, k, n), n)
    prod = (a / 2.0 + 1.0) * TWO_PI * float(np.mean(w * w * h_w))
    diss = nu * TWO_PI * float(np.mean(w_x * w_x))
    return prod - diss
