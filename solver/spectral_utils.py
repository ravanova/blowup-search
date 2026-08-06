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


def _require_grid_size(n, who):
    """One consistent refusal for a degenerate grid size (leg 129, D7).

    Before the repair the three grid helpers disagreed about the SAME invalid
    input: `grid(0)` and `grid(-8)` returned empty arrays silently, while
    `wavenumbers(0)` and `dealias_mask(0)` raised `ZeroDivisionError` and
    `wavenumbers(-8)` returned an empty array. Three behaviours, one error.
    `solver/boussinesq.py` (leg 89) made the analogous 2D condition a hard
    `ValueError`; this is the 1D equivalent.
    """
    if int(n) != n or n < 1:
        raise ValueError(f"{who}: n must be a positive integer, got {n!r}")


def _require_k(w_hat, k, who):
    """`k` must be a 1-D array of the same length as `w_hat` (leg 129, D6).

    Before the repair `hilbert_hat` validated nothing and `derivative_hat`
    validated only `len(w_hat)`, so a scalar or length-1 `k` BROADCAST into a
    full-length, plausible, wrong answer: `hilbert_hat(w_hat, -1.0)` returned
    the sign-flipped transform (relative sup error 2.0) and `k = 0.0`
    annihilated it entirely (1.0). `velocity_hat` already refused all five such
    inputs by accident of indexing `k`, which made the module internally
    inconsistent about one caller error. All three now refuse alike, with the
    same exception type.

    These functions sit in the solver's inner loop, so the check reads `.shape` directly
    rather than calling `np.asarray`/`np.shape`: an allocation per call cost ~14% on a full
    gCLM solve when this repair was first written, and the shape-attribute form gives the
    same refusals for ~1% (both measured, leg 129).
    """
    ks = getattr(k, "shape", None)
    ws = getattr(w_hat, "shape", None)
    if ks is None or len(ks) != 1 or ws is None or len(ws) != 1 or ks[0] != ws[0]:
        raise ValueError(
            f"{who}: k must be a 1-D array matching w_hat's length "
            f"{ws[0] if ws is not None and len(ws) == 1 else '?'}, got "
            f"{'a scalar' if ks is None else f'shape {ks}'}"
        )


def grid(n):
    """Uniform periodic grid on [0, 2*pi): n points, spacing 2*pi/n."""
    _require_grid_size(n, "grid")
    return TWO_PI * np.arange(n) / n


def wavenumbers(n):
    """rfft wavenumbers 0..n//2 for a 2*pi-periodic domain."""
    _require_grid_size(n, "wavenumbers")
    return np.fft.rfftfreq(n, d=1.0 / n)


def dealias_mask(n):
    """2/3-rule mask over rfft modes: keep |k| < n/3, STRICTLY.

    The cut is `k <= (n - 1) // 3`, which is the largest integer strictly
    below `n/3` for every n. Before leg 129's repair this read `k <= n/3.0`,
    which retains one mode too many whenever 3 divides n.

    WHY STRICT (Bowman 2013, *How Important is Dealiasing for Turbulence
    Simulations?*, U. Alberta, p.29): "one needs to pad to N >= 3m - 2 to
    prevent mode m - 1 from beating with itself to contaminate the most
    negative (first) mode". With K = m - 1 the largest retained wavenumber
    that is N >= 3K + 1, i.e. K < N/3 strictly. The same condition is
    restated independently in 2026 (arXiv:2603.08892), which zeroes every
    mode with |k| >= (2/3)k_Nyquist = n/3.

    The argument needs no authority, though: a quadratic product of retained
    modes reaches 2K, which aliases to 2K - n; it lands back inside the
    retained band iff |2K - n| <= K, i.e. iff n <= 3K. Alias-freedom is
    exactly n > 3K.

    MEASURED (leg 120, banked in writeup/data/p2_route_sua_v1_adversarial.json):
    under the old cut, placing the field on the top retained mode K and
    squaring it put a spurious coefficient of exactly 2.500e-01 back on mode K
    at all 11 tested grids with 3 | n, against <= 4.83e-16 at all 12 with
    3 | n false. `energy_production` -- documented as the "Exact rate d/dt E"
    and logged as an artifact guard on every run -- inherited that as a
    relative error of 1.6621e-01 at n = 81, versus 2.47e-14 elsewhere.

    NO-OP WHERE IT MATTERS: `(n - 1) // 3 == floor(n/3)` whenever 3 does not
    divide n, so the returned mask is bit-identical at every grid size this
    repository has ever run (all powers of two: 64, 256, 512, 1024, 2048,
    4096, 8192). Leg 129 measured that rather than assuming it.
    """
    _require_grid_size(n, "dealias_mask")
    cut = (n - 1) // 3
    if cut < 1:
        raise ValueError(
            f"dealias_mask: n={n} retains no non-mean mode under the 2/3 rule "
            f"(the strict cut is k <= {cut}); n >= 4 is required. This is the "
            "1D form of the guard solver/boussinesq.py makes in 2D."
        )
    return wavenumbers(n) <= cut


def hilbert_hat(w_hat, k):
    """Hilbert transform in Fourier space: multiply by -i*sign(k)."""
    _require_k(w_hat, k, "hilbert_hat")
    return -1j * np.sign(k) * w_hat


def velocity_hat(w_hat, k):
    """u_hat with u_x = H(w) and zero mean: u_hat[k] = -w_hat[k]/|k|, k != 0.

    The output is always complex128 (leg 129, D5). It used to be
    `np.zeros_like(w_hat)`, which inherited the INPUT dtype, so integer input
    silently truncated the float quotient on assignment -- relative error
    1.0000 at int scale 1 and 3 over 200 draws. `derivative_hat` and
    `hilbert_hat` both promote on the same input; this was the only one of the
    three that did not.

    The mean mode is multiplied by zero rather than left at a fresh zero
    (leg 129, D4). u is chosen zero-mean, so the VALUE is unchanged for every
    finite input -- exactly +0.0, since the trailing `+ 0.0j` normalizes the
    signed zero a multiplication can produce -- but a non-finite w_hat[0], the
    caller's signal that its field is corrupt, now propagates as nan instead of
    being erased into a clean 0.
    """
    _require_k(w_hat, k, "velocity_hat")
    u_hat = np.zeros(w_hat.shape[0], dtype=np.complex128)
    nz = k != 0
    u_hat[nz] = -w_hat[nz] / np.abs(k[nz])
    z = ~nz
    u_hat[z] = w_hat[z] * 0.0 + 0.0j
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

    Leg 129 changed two things and neither moves a finite value. The Nyquist
    entry is now MULTIPLIED by zero rather than assigned zero, which is
    Johnson's Algorithm 1 step 2 verbatim ("multiply Y_k ... by ZERO for
    k = N/2 (if N is even)"). On finite input the two forms are identical --
    the trailing `+ 0.0j` normalizes the signed zero the multiplication can
    produce, so the coefficient is exactly 0+0j as before -- but on non-finite
    input they differ, because 0.0*nan = nan and 0.0*inf = nan. Under the
    assignment form, 12 of 12 poisoned Nyquist coefficients came back as a
    fully finite spectrum with max|w_x| = 1.0000, indistinguishable from clean
    input (leg 120, D3); numpy even raised a RuntimeWarning inside the multiply
    for the six +-inf cases and the assignment discarded exactly the value that
    warning was about. And `k` is now validated, as it already was in
    `velocity_hat` (D6).
    """
    if len(w_hat) != n // 2 + 1:
        raise ValueError(
            f"derivative_hat: {len(w_hat)} rfft coefficients is not the "
            f"{n // 2 + 1} expected for an n={n} grid"
        )
    _require_k(w_hat, k, "derivative_hat")
    d = 1j * k * w_hat
    if n % 2 == 0 and len(w_hat) > 1:
        d[-1] = d[-1] * 0.0 + 0.0j
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
