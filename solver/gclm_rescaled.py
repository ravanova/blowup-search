"""Dynamic self-similar rescaling of the 1D CLM model (a=0), on a stretched grid.

Phase-2 Spike 0, second increment (after the line Hilbert transform crux). This
time-steps the *rescaled* CLM equation whose steady state is the exact CLM
self-similar profile, on a sinh-stretched whole-line grid that keeps the dilation
term's CFL bounded (the cure for the uniform-grid death documented in the notes).

Rescaled CLM (a=0), convention omega(x,t)=C_omega(tau)^{-1} Omega(X,tau),
X=C_l x, dtau/dt = C_omega^{-1}, with the value-based normalization from
Huang-Tong-Wang (arXiv:2603.25104):

    Omega_tau = (c_omega + H Omega) Omega - c_l X Omega_X,
    c_l = 1  (constant),   c_omega = 1 - H Omega(0).

To protect the odd (order-1) vanishing at the origin we evolve f = Omega / X
(k=1, the non-degenerate CLM profile vanishes to order 1). Substituting
Omega = X f and c_l = 1:

    f_tau = -X f_X + (H Omega - H Omega(0)) f,   Omega = X f.

On the computational coordinate rho (uniform, X = c*sinh(rho)) the dilation
becomes the bounded advection  X f_X = tanh(rho) f_rho, so

    f_tau = -tanh(rho) f_rho + (H Omega - H Omega(0)) f.

Exact steady state (verified analytically): Omega_0(X) = -4X/(1+4X^2),
H(Omega_0) = 2/(1+4X^2), H Omega(0) = 2, hence c_omega = -1. The origin value
f(0) = Omega_X(0) = -4 is frozen exactly by the scheme (both the advection speed
tanh(0) and the source H Omega(0)-H Omega(0) vanish at rho=0), which realizes the
slope normalization.

Method: 3rd-order upwind-biased advection in rho (solution is smooth -> the
nonlinear WENO limiter of the paper is unnecessary at POC level), SSPRK3 in
rescaled time. The line Hilbert transform is the fixed-grid dense operator from
solver/line_hilbert.py, built once and reused.
"""

import numpy as np

from solver.line_hilbert import line_hilbert_matrix

PI = np.pi

#: Floor on the gauge multiplier used by :meth:`RescaledCLM.run`'s stopping test.
#:
#: The rescaled CLM fixed point is a one-parameter LINE: Omega_lambda(X) = Omega_0(lambda X)
#: is an exact steady state for every lambda > 0, selected by the origin slope f(0) = -4 lambda,
#: which the scheme freezes exactly and which this module's docstring calls a free gauge.
#: ||f_tau||_inf is degree-1 in lambda, so a FIXED ABSOLUTE stopping test is not scale-invariant
#: along the one direction the module declares free: for lambda below ~tol/2.94 it is satisfied
#: by the initial data and `run()` reports convergence after one step (leg 85, Route-GRA).
#: The cure is to measure the residual against the already-frozen gauge |f(0)|/4 (= lambda),
#: which is exactly 1 at the validated gauge f(0) = -4, so no banked number moves.
#:
#: The floor only guards the degenerate gauge f(0) = 0, where no scale exists. It is deliberately
#: TINY rather than the more obvious 1e-6: the floor can only ever make the tolerance LOOSER than
#: the scale-invariant value (max() picks it when lambda < floor), so any floor above the gauge
#: scales one wants to certify re-admits the very false positive this fixes -- measured, floor
#: 1e-6 leaves the lambda = 1e-8/1e-9/1e-10 false positives in place. 1e-15 is ~10x double
#: precision epsilon, below every gauge member representable above roundoff, and it keeps the
#: tolerance strictly positive so a state exactly at rest (residual identically 0) still reports
#: converged.
GAUGE_TOL_FLOOR = 1e-15


def sinh_grid(n, c=0.5, rho_max=8.0):
    """Symmetric whole-line grid X = c*sinh(rho), rho uniform on [-rho_max, rho_max].

    n must be ODD so that rho=0 (=> X=0) is a grid node. dX ~ X drho makes the
    dilation CFL ~ drho, independent of the reach M = c*sinh(rho_max)."""
    if n % 2 == 0:
        n += 1
    rho = np.linspace(-rho_max, rho_max, n)
    X = c * np.sinh(rho)
    return rho, X


def clm_profile(X):
    """Exact rescaled CLM self-similar profile Omega_0(X) = -4X/(1+4X^2)."""
    return -4.0 * X / (1.0 + 4.0 * X ** 2)


def _drho_upwind(f, drho, speed):
    """3rd-order upwind-biased d f/d rho, selected by sign(speed).

    a>0 :  f'_i = (f_{i-2} - 6 f_{i-1} + 3 f_i + 2 f_{i+1}) / (6 drho)
    a<0 :  f'_i = (-2 f_{i-1} - 3 f_i + 6 f_{i+1} - f_{i+2}) / (6 drho)
    Flow is outward at both domain ends, so the upwind stencil always reaches
    inward; only the single outermost node per side needs a one-sided fallback."""
    n = f.size
    dfp = np.zeros(n)  # a>0 stencil
    dfm = np.zeros(n)  # a<0 stencil
    # interior (vectorized)
    i = np.arange(2, n - 1)
    dfp[i] = (f[i - 2] - 6 * f[i - 1] + 3 * f[i] + 2 * f[i + 1]) / (6 * drho)
    i = np.arange(1, n - 2)
    dfm[i] = (-2 * f[i - 1] - 3 * f[i] + 6 * f[i + 1] - f[i + 2]) / (6 * drho)
    # boundary fallbacks (2nd-order one-sided; used only where they are upwind)
    dfp[1] = (f[2] - f[0]) / (2 * drho)
    dfp[n - 1] = (3 * f[n - 1] - 4 * f[n - 2] + f[n - 3]) / (2 * drho)
    dfp[0] = (f[1] - f[0]) / drho
    dfm[n - 2] = (f[n - 1] - f[n - 3]) / (2 * drho)
    dfm[0] = (-3 * f[0] + 4 * f[1] - f[2]) / (2 * drho)
    dfm[n - 1] = (f[n - 1] - f[n - 2]) / drho
    return np.where(speed >= 0.0, dfp, dfm)


class RescaledCLM:
    """Dynamic-rescaling integrator for CLM (a=0) on a fixed sinh-stretched grid."""

    def __init__(self, n=1201, c=0.5, rho_max=8.0):
        self.rho, self.X = sinh_grid(n, c=c, rho_max=rho_max)
        self.n = self.X.size
        self.i0 = self.n // 2  # rho=0 <=> X=0 node
        self.drho = self.rho[1] - self.rho[0]
        self.tanh = np.tanh(self.rho)
        self.Hmat = line_hilbert_matrix(self.X)  # fixed-grid dense operator

    def hilbert(self, omega):
        return self.Hmat @ omega

    def rhs(self, f):
        """L(f) = -tanh(rho) f_rho + (H Omega - H Omega(0)) f,  Omega = X f."""
        omega = self.X * f
        Homega = self.hilbert(omega)
        c_omega = 1.0 - Homega[self.i0]
        source = (Homega - Homega[self.i0]) * f
        adv = -self.tanh * _drho_upwind(f, self.drho, self.tanh)
        return adv + source, c_omega

    def step(self, f, dt):
        """One SSPRK3 (Shu-Osher) step; returns (f_next, c_omega, residual_inf)."""
        L0, c_omega = self.rhs(f)
        f1 = f + dt * L0
        L1, _ = self.rhs(f1)
        f2 = 0.75 * f + 0.25 * (f1 + dt * L1)
        L2, _ = self.rhs(f2)
        fn = (1.0 / 3.0) * f + (2.0 / 3.0) * (f2 + dt * L2)
        res = np.abs(L0).max()
        return fn, c_omega, res

    def run(self, f_init, dt_frac=0.4, tol=1e-8, max_steps=200000, verbose=False):
        """Evolve until ||f_tau||_inf < tol * gauge (or max_steps). Returns a result dict.

        STOPPING TEST (leg 85 / Route-GRA repair): `tol` is RELATIVE to the scaling gauge
        the scheme has already frozen, `gauge = max(|f(0)|/4, GAUGE_TOL_FLOOR)`, and NOT an
        absolute number. At the validated gauge f(0) = -4 the multiplier is exactly 1, so this
        is bit-identical to the previous absolute test and no banked measurement moves; at any
        other gauge member Omega_lambda(X) = Omega_0(lambda X) it is what makes the test
        scale-invariant along the free direction. See GAUGE_TOL_FLOOR for the floor's rationale.

        NOTE on T*: a whole-line rescaling run resolves the *local* self-similar
        structure; the physical blow-up time T* (=2 for w0=-sin x) is a property of
        the *global periodic* solve (validated separately by test_solver_clm.py)
        and is NOT determined by a whole-line run — the rescaled initial amplitude
        is a free gauge. The correct local analogue is the RATE c_omega -> -1, i.e.
        omega ~ (T-t)^{-1}, which this run recovers."""
        f = np.array(f_init, dtype=float)
        dt = dt_frac * self.drho  # tanh(rho) <= 1 => CFL ~ drho
        # the gauge is frozen by the scheme at rho=0 for all time, so read it once, from the
        # data. |f(0)|/4 = lambda, and equals 1 exactly at the validated gauge f(0) = -4.
        # A non-finite f(0) leaves tol_eff non-finite, so `res < tol_eff` stays False: poisoned
        # data can no more be reported converged than before.
        gauge = max(abs(float(f[self.i0])) / 4.0, GAUGE_TOL_FLOOR)
        tol_eff = tol * gauge
        tau = 0.0
        c_hist, res_hist, tau_hist = [], [], []
        res = np.inf
        step = 0
        c_omega = np.nan
        for step in range(max_steps):
            f, c_omega, res = self.step(f, dt)
            tau += dt
            c_hist.append(c_omega)
            res_hist.append(res)
            tau_hist.append(tau)
            if verbose and step % 2000 == 0:
                print(f"    step {step:6d} tau={tau:7.3f} c_omega={c_omega:+.5f} res={res:.2e}")
            if res < tol_eff:
                break
        omega = self.X * f
        return {
            "f": f,
            "omega": omega,
            "X": self.X,
            "rho": self.rho,
            "c_omega": c_omega,
            "residual": res,
            "tau": tau,
            "steps": step + 1,
            "converged": res < tol_eff,
            "gauge": gauge,
            "tol_effective": tol_eff,
            "c_hist": np.array(c_hist),
            "res_hist": np.array(res_hist),
            "tau_hist": np.array(tau_hist),
        }
