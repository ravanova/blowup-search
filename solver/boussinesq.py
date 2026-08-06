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

INPUT VALIDATION AND NaN DISCIPLINE (repair of leg 89 / Route-BOA's findings).
Leg 89's 90-case adversarial battery found that malformed inputs were dropped
silently rather than propagated or flagged, on 19 of 82 gate-deciding cases. The
four defects and the fix applied here:

1. The `omega0 is identically zero` guard tested `== 0.0` exactly, so a vorticity
   that is zero only to roundoff in the REPRESENTED (post-dealias) subspace --
   e.g. sin(15x)sin(15y) at n=32, whose represented max|w| is 1.797e-16 -- slipped
   past it, and the blow-up trigger `amplification_factor*m0` was then cleared in
   one step by ordinary O(1) buoyancy forcing, returning `blowup_candidate`, the
   most consequential label this module emits, on near-zero noise. The guard is
   now SCALE-AWARE: it rejects when max|w_represented| falls below
   `ZERO_OMEGA_REL_TOL` (1e-13) times the scale of the initial state itself
   (max of the pre-mask |omega0|, the represented |w| and the represented |th|).
   1e-13 is ~1e3 x double eps, i.e. "indistinguishable from zero after the FFT
   round trip", with margin for accumulated roundoff; a genuinely small but
   meaningful vorticity (any fixed fraction of the state scale) is untouched.
2. `nu` and `kappa` were applied behind `if nu > 0.0` / `if kappa > 0.0`, so a
   negative or non-finite value was neither applied nor rejected -- the run that
   executed was the zero-coefficient run, bit for bit, while `params` recorded the
   ignored value. `kappa` is invisible even in principle to the energy identity
   `dE/dt = int(v*th) - nu*int(w^2)`, which does not contain it, so there was no
   tell at all. Both are now validated at entry: the admissible domain is the
   finite non-negative reals (nu, kappa >= 0; the inviscid Euler-analog nu=kappa=0
   is the boundary, and a negative diffusivity is anti-diffusion, not physics).
   Same treatment for every other scalar whose out-of-domain value was silently
   absorbed rather than rejected: `t_max` (>= 0 finite; 0.0 stays legal and
   returns at once), `dt_max`/`c1`/`c2` (> 0 finite -- a non-finite CFL safety
   factor used to REMOVE its `min` limb rather than fail, relaxing dt_min 168x),
   `amplification_factor` (> 0 finite -- a NaN made the threshold comparison
   permanently False, disabling blow-up detection outright and reporting
   `no_blowup` on a 4x amplification), `max_steps` (>= 1 integer), and
   `drift_guard`/`tail_guard` (finite when given; NEGATIVE IS DELIBERATELY LEGAL
   and is how test_boussinesq_dedicated.py forces a guard to fire).
3. `conservation_drift` and the running drift guard used Python's builtin `max`,
   which is order-dependent on NaN (`max(0.3, nan) -> 0.3`), so a 100%-NaN
   `theta_final` reported a drift of 8.077e-18 and `drift_guard=1e-9` never fired.
   Every guard-limb combination now goes through `_guard_max`, which PROPAGATES
   NaN deliberately, and the drift guard treats a non-finite drift as its own
   reportable failure (`outcome="under_resolved"`, `early_exit_reason=
   "nonfinite_drift"`) rather than a comparison that quietly evaluates False.
4. A degenerate grid (n = 1 or 2) leaves the 2/3 dealias mask retaining exactly
   ONE mode -- the (0,0) mean -- so the method has no spatial resolution at all,
   yet ran 30 steps and reported `no_blowup` with drift 0.0. A grid whose mask
   retains no non-zero wavenumber is now rejected.

The rule throughout: an input the module cannot honour is refused loudly at entry
(ValueError) or flagged in `outcome`; it is never absorbed into a run that looks
healthy. Banked by test_boussinesq_adversarial.py.
"""

import time
from dataclasses import dataclass, field

import numpy as np

TWO_PI = 2.0 * np.pi

# Relative tolerance for "the represented vorticity is zero". ~1e3 x double eps:
# large enough to swallow the roundoff of an fft2/ifft2 round trip on an O(1)
# field, small enough that any vorticity carrying a real fraction of the initial
# state's scale is accepted. See the module docstring, defect 1.
ZERO_OMEGA_REL_TOL = 1e-13


def _guard_max(*values):
    """`max` that PROPAGATES NaN, unlike the builtin.

    `max(0.3, float("nan"))` returns 0.3 and `max(float("nan"), 0.3)` returns nan
    -- the builtin's answer depends on argument order, because every comparison
    against NaN is False. Every artifact-guard limb in this module goes through
    this instead, so a poisoned limb can never be hidden behind a healthy one
    (leg 89, defect 3).
    """
    vals = [float(v) for v in values]
    if any(v != v for v in vals):  # v != v is True exactly for NaN
        return float("nan")
    return max(vals)


def _check_scalar(name, value, minimum, strict):
    """Return float(value), or raise ValueError if it is non-finite or below the
    domain floor. `strict` selects `> minimum` over `>= minimum`."""
    v = float(value)
    if not np.isfinite(v):
        raise ValueError(
            f"{name} must be finite, got {value!r}; a non-finite {name} is "
            "dropped rather than applied by the comparisons downstream, which "
            "would silently run a different computation than the one requested"
        )
    if (v <= minimum) if strict else (v < minimum):
        rel = ">" if strict else ">="
        raise ValueError(f"{name} must be {rel} {minimum}, got {v!r}")
    return v


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
    """2/3-rule mask over fft2 modes: keep |kx| < n/3 AND |ky| < n/3, STRICTLY.

    The cut is `(n - 1) // 3`, the largest integer strictly below n/3. This
    line used to read `cut = n / 3.0`, the identical off-by-one leg 120 found
    in `solver/spectral_utils.dealias_mask`: at 3 | n it retained one mode too
    many in EACH direction, so the alias-free guarantee failed on a band of
    (2K+1)^2 - (2K-1)^2 modes rather than on one. See the 1D docstring for the
    published condition (Bowman 2013; arXiv:2603.08892) and the elementary
    argument (a quadratic product reaches 2K, aliases to 2K - n, and re-enters
    the band iff n <= 3K).

    NO-OP where it matters: `(n - 1) // 3 == floor(n/3)` whenever 3 does not
    divide n, so this mask is bit-identical at the n = 32 of every banked
    Boussinesq run and at every power of two. Leg 129 measured that.
    """
    k = np.fft.fftfreq(n, d=1.0 / n)
    KX, KY = np.meshgrid(k, k, indexing="ij")
    cut = (n - 1) // 3
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


# --- Hou-Luo symmetry-wall (PHASE1_PLAN.md, Gate 1b) ---
#
# A no-penetration wall is imposed by parity symmetry rather than a Chebyshev
# boundary: on the doubly-periodic square, restrict to the subspace
#
#     w  odd in x AND odd in y      (w  = sum sin(jx) sin(ky))
#     th even in x AND odd in y     (th = sum cos(jx) sin(ky))
#
# Then Biot-Savart gives u = -psi_y odd-x/even-y and v = psi_x even-x/odd-y, so
# the normal velocity v vanishes on y=0 and y=pi (walls), and u vanishes on x=0
# and x=pi (symmetry axes) -- an effective [0,pi]^2 box with the singular corner
# at the origin, the Luo-Hou geometry. The buoyancy th_x is odd-x/odd-y = w's
# parity, and one checks directly that u.grad w, u.grad th, and the viscous term
# all preserve these parities, so the subspace is invariant: initialising in it
# and evolving keeps the wall exactly (validated to machine precision in
# test_boussinesq_wall.py by measuring the parity-violating residual over time).


def _reflect(f, axis):
    """f evaluated at x -> -x (mod 2pi) along `axis`: index i -> (n-i) % n."""
    r = np.concatenate([f[:1], f[:0:-1]], axis=0)
    return r if axis == 0 else np.concatenate([f[:, :1], f[:, :0:-1]], axis=1)


def project_odd_odd(f):
    """Project a real field onto odd-in-x AND odd-in-y (the w subspace)."""
    return 0.25 * (f - _reflect(f, 0) - _reflect(f, 1) + _reflect(_reflect(f, 0), 1))


def project_even_odd(f):
    """Project a real field onto even-in-x AND odd-in-y (the th subspace)."""
    return 0.25 * (f + _reflect(f, 0) - _reflect(f, 1) - _reflect(_reflect(f, 0), 1))


def parity_residual(f, kind):
    """Relative size of the parity-violating component of f (0 == exactly in the
    subspace). `kind` is "odd_odd" (w) or "even_odd" (th)."""
    proj = project_odd_odd(f) if kind == "odd_odd" else project_even_odd(f)
    scale = float(np.max(np.abs(f)))
    if scale == 0.0:
        return 0.0
    return float(np.max(np.abs(f - proj))) / scale


@dataclass
class BoussinesqResult:
    """Summary of one run — mirrors solver.gclm.SolverResult, plus theta_final."""

    outcome: str  # no_blowup|blowup_candidate|diverged|max_steps_hit|under_resolved
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
    max_tail_fraction: float = 0.0  # peak enstrophy fraction near the dealias cut
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
    symmetry=None,
    drift_guard=None,
    tail_guard=None,
):
    """Integrate 2D Boussinesq from (omega0, theta0) on an n x n grid.

    frozen_u: None, or a constant (cu, cv) divergence-free velocity replacing the
    self-consistent field (the transport-only acceptance check).
    early_decay_exit: as in solve_gclm — {"fraction": f, "window": T}.
    symmetry: None (doubly-periodic, Gate 1a) or "houluo" — project w onto
    odd-x/odd-y and th onto even-x/odd-y each step so the no-flow wall is held
    exactly against roundoff drift (Gate 1b). The dynamics preserve the subspace
    on their own; this only removes float-level leakage on long runs.
    drift_guard: None, or a float — stop with outcome "under_resolved" when the
    running artifact-guard drift (conservation) exceeds it, or when that drift is
    itself non-finite (then `early_exit_reason` is "nonfinite_drift"). A negative
    threshold is legal and fires on the first step; a non-finite one is rejected.
    tail_guard: None, or a float — stop with outcome "under_resolved" when the
    fraction of enstrophy in the top band of retained modes (near the 2/3 dealias
    cut) exceeds it. This is the RIGHT under-resolution signal for a spectral
    method: conservation (drift) can stay tiny while small scales become garbage,
    but a sharpening singularity piles enstrophy at the grid scale, and that shows
    here first. On a uniform grid a genuine 2D-Boussinesq singularity sharpens
    below grid scale before T*; t_final / max_omega then bound the *trustworthy*
    growth window (Phase-1 resolution de-risk). `max_tail_fraction` is always
    reported.
    """
    if symmetry not in (None, "houluo"):
        raise ValueError(f"unknown symmetry {symmetry!r}")

    # --- scalar-parameter domain validation (leg 89 defects 2 and 4) ---------
    # Physical coefficients: the admissible domain is the finite non-negative
    # reals. nu=kappa=0 is the inviscid Euler-analog this module is built for and
    # stays legal; a negative diffusivity is anti-diffusion, and was previously
    # neither applied nor rejected.
    nu = _check_scalar("nu", nu, 0.0, strict=False)
    kappa = _check_scalar("kappa", kappa, 0.0, strict=False)
    # Integration window: 0.0 is a legitimate degenerate request (return at once);
    # negative and NaN made `while t < t_max` False and returned a scientific
    # conclusion from a run that never happened.
    t_max = _check_scalar("t_max", t_max, 0.0, strict=False)
    # Timestep controls: a non-finite one REMOVED its limb from the dt `min`.
    dt_max = _check_scalar("dt_max", dt_max, 0.0, strict=True)
    c1 = _check_scalar("c1", c1, 0.0, strict=True)
    c2 = _check_scalar("c2", c2, 0.0, strict=True)
    # Detection threshold: a non-finite one made `m >= amplification_factor*m0`
    # permanently False, i.e. disabled blow-up detection while still reporting
    # "no_blowup" as though the question had been asked and answered.
    amplification_factor = _check_scalar(
        "amplification_factor", amplification_factor, 0.0, strict=True)
    if int(max_steps) != max_steps or int(max_steps) < 1:
        raise ValueError(f"max_steps must be an integer >= 1, got {max_steps!r}")
    max_steps = int(max_steps)
    # Artifact guards: only finiteness is required. A NEGATIVE threshold is
    # deliberately legal -- it is how test_boussinesq_dedicated.py forces each
    # guard to fire on the first step -- but a NaN one silently never fires.
    if drift_guard is not None:
        drift_guard = _check_scalar("drift_guard", drift_guard, -np.inf, strict=False)
    if tail_guard is not None:
        tail_guard = _check_scalar("tail_guard", tail_guard, -np.inf, strict=False)
    if frozen_u is not None:
        frozen_u = (_check_scalar("frozen_u[0]", frozen_u[0], -np.inf, strict=False),
                    _check_scalar("frozen_u[1]", frozen_u[1], -np.inf, strict=False))

    t_start_wall = time.perf_counter()
    omega0 = np.asarray(omega0, dtype=float)
    theta0 = np.asarray(theta0, dtype=float)
    n = omega0.shape[0]
    if omega0.shape != (n, n) or theta0.shape != (n, n):
        raise ValueError("omega0 and theta0 must be square n x n arrays")
    KX, KY, Ksq, inv_Ksq = wavenumbers2d(n)
    mask = dealias_mask2d(n)
    # Degenerate grid (leg 89 defect 4): at n = 1 and n = 2 the 2/3 rule leaves
    # only the (0,0) mean mode, so the discretization cannot represent ANY
    # dynamics -- and it used to report the most reassuring guard numbers in the
    # battery (drift exactly 0.0) precisely because nothing happened.
    if not np.any(mask & (Ksq > 0.0)):
        raise ValueError(
            f"n={n} leaves the 2/3 dealias mask retaining only the mean mode: "
            "the grid cannot represent any non-constant field, so no dynamics "
            "can be computed on it (n >= 3 required)"
        )
    dx = TWO_PI / n

    if symmetry == "houluo":
        omega0 = project_odd_odd(omega0)
        theta0 = project_even_odd(theta0)
    w_hat = np.fft.fft2(omega0) * mask
    th_hat = np.fft.fft2(theta0) * mask
    w = np.fft.ifft2(w_hat).real
    th = np.fft.ifft2(th_hat).real

    m0 = float(np.max(np.abs(w)))
    if m0 == 0.0:
        raise ValueError("omega0 is identically zero")
    # Scale-aware zero test (leg 89 defect 1). `m0 == 0.0` above only catches a
    # BIT-exact zero. A vorticity annihilated by the dealias mask, or one at a
    # denormal amplitude, leaves m0 at roundoff -- nonzero, so the exact test
    # misses it -- and then `amplification_factor * m0` is a threshold at the
    # roundoff scale that ordinary O(1) buoyancy forcing clears in one step,
    # producing a false "blowup_candidate". Compare against the scale of the
    # initial state itself: the pre-mask input (so a fully dealias-annihilated
    # omega0 is caught even when theta0 is also tiny) and both represented fields.
    state_scale = _guard_max(m0, float(np.max(np.abs(omega0))),
                             float(np.max(np.abs(th))))
    if m0 <= ZERO_OMEGA_REL_TOL * state_scale:
        raise ValueError(
            f"omega0 is numerically zero: the represented (post-dealias) "
            f"max|w| = {m0:.6e} is at or below {ZERO_OMEGA_REL_TOL:g} x the "
            f"initial state scale {state_scale:.6e}, i.e. indistinguishable "
            "from zero at working precision. Amplification relative to it is "
            "meaningless -- growth off such an m0 is forcing response, not "
            "amplification of the data -- so no blow-up verdict can be given"
        )

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

    # Spectral under-resolution signal: enstrophy fraction in the top band of
    # retained modes (radius > 0.75 of the 2/3 dealias cut). Rises sharply when
    # the vorticity sharpens below grid scale.
    k_cut = n / 3.0
    tail_mask = (KX * KX + KY * KY) > (0.75 * k_cut) ** 2

    def tail_fraction(wh):
        p = np.abs(wh) ** 2
        tot = float(p.sum())
        return float(p[tail_mask].sum() / tot) if tot > 0.0 else 0.0

    max_tail_fraction = tail_fraction(w_hat)

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
        if symmetry == "houluo":
            w_hat = np.fft.fft2(project_odd_odd(np.fft.ifft2(w_hat).real)) * mask
            th_hat = np.fft.fft2(project_even_odd(np.fft.ifft2(th_hat).real)) * mask
        w = np.fft.ifft2(w_hat).real
        th = np.fft.ifft2(th_hat).real
        m = float(np.max(np.abs(w)))
        times.append(t)
        max_omega.append(m)

        if not np.isfinite(m):
            outcome = "diverged"
            break

        # Every accumulator uses _guard_max, not the builtin: a NaN entering any
        # limb must reach the reported drift, not be dropped by an order-dependent
        # comparison (leg 89 defect 3).
        max_w_int_dev = _guard_max(max_w_int_dev, abs(_integral(w) - w_int0))
        max_th_int_dev = _guard_max(max_th_int_dev, abs(_integral(th) - th_int0))
        max_l1_w = _guard_max(max_l1_w, _integral(np.abs(w)))
        max_l1_th = _guard_max(max_l1_th, _integral(np.abs(th)))
        e_now, p_now = kinetic_energy_and_prod(w_hat)
        e_accum_err += abs((e_now - e_prev) - 0.5 * dt * (p_now + p_prev))
        e_prev, p_prev = e_now, p_now
        max_e = _guard_max(max_e, abs(e_now))

        tail = tail_fraction(w_hat)
        max_tail_fraction = _guard_max(max_tail_fraction, tail)
        if drift_guard is not None:
            running_drift = _guard_max(
                max_w_int_dev / _guard_max(max_l1_w, 1e-300),
                max_th_int_dev / _guard_max(max_l1_th, 1e-300),
                e_accum_err / _guard_max(max_e, 1e-300),
            )
            # A non-finite drift is its OWN failure, reported as such. It used to
            # evaluate the comparison below to False and let the run continue.
            if not np.isfinite(running_drift):
                outcome = "under_resolved"
                early_exit_reason = "nonfinite_drift"
                break
            if running_drift > drift_guard:
                outcome = "under_resolved"
                break
        if tail_guard is not None and tail > tail_guard:
            outcome = "under_resolved"
            break

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

    mean_drift = _guard_max(max_w_int_dev / _guard_max(max_l1_w, 1e-300),
                            max_th_int_dev / _guard_max(max_l1_th, 1e-300))
    energy_residual = e_accum_err / _guard_max(max_e, 1e-300)
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
        conservation_drift=_guard_max(mean_drift, energy_residual),
        max_tail_fraction=float(max_tail_fraction),
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
