"""Dynamic self-similar rescaling of the 1D Hou-Luo (HL) model, on a stretched grid.

Phase-2 P2 (post-Spike-1, the lottery-ticket leg). Target scenario: Chen-Huang-Li
arXiv:2604.01868 -- *singular* self-similar blow-up profiles from *degenerate*
initial data (a not-rigorously-proven frontier; only weak existence of the
explicit profile below is proven, its asymptotic stability is numerical-only).

HL model (their eq 1.1):
    omega_t + u omega_x = theta_x,   theta_t + u theta_x = 0,   u_x = H(omega),
with H the whole-line Hilbert transform, H(f)(x) = (1/pi) p.v. int f(y)/(x-y) dy.

Dynamic-rescaling form (their (2.4)), omega = C_omega^{-1} Omega(X,tau),
theta = C_theta^{-1} Theta(X,tau), X = C_l x, and U the rescaled velocity:
    Omega_tau + (U + c_l X) Omega_X = c_omega Omega + Theta_X,
    Theta_tau + (U + c_l X) Theta_X = (c_l + 2 c_omega) Theta,
    U_X = H(Omega),   U(0) = 0.
Steady states of the frozen system (their (2.5)) are exact self-similar blow-ups
of (1.1) in the form omega(x,t) = (T-t)^lambda Omega(x/(T-t)^gamma), with
gamma = -c_l/c_omega, lambda = -1.

Two genuinely new pieces vs solver/gclm_rescaled.py:
  * the velocity U is the *integral* of H(Omega) pinned at U(0)=0 (CLM's transport
    speed was purely algebraic c_l X); see `velocity`.
  * a second (buoyancy) field Theta couples in via Theta_X.

VALIDATION ANCHOR -- the explicit singular steady state, their Theorem 2.3:
    Omega_bar(X) = (X-1)^{-1/2} 1_{X>1},   Theta_bar(X) = (pi/2) 1_{X>1},
    c_l = 2,   c_omega = -1     (=> c_l + 2 c_omega = 0, so the Theta eqn is trivial).
Derived exact velocity (classical Hilbert pair H(x_+^{-1/2}) = -( -x )_+^{-1/2},
verifiable via the Fourier multiplier -i sgn(xi)):
    H(Omega_bar)(X) = -(1-X)^{-1/2} 1_{X<1},
    U_bar(X)        =  2 sqrt(1-X) - 2   (X<1),   -2   (X>=1),
and one checks (U_bar + 2X) Omega_bar_X + Omega_bar = 0 on X>1 (strong steady form,
Remark 5.4: strong solution for X != singular point, weak at the singularity).
"""

import numpy as np

from solver.line_hilbert import line_hilbert_matrix, natural_spline_slopes
from solver.gclm_rescaled import _drho_upwind as _upwind_deriv

PI = np.pi


# --------------------------------------------------------------------------
# grids
# --------------------------------------------------------------------------
def sinh_grid_at(n, Xc=1.0, delta=None, M=1000.0, offset=True):
    """Whole-line grid clustered near X=Xc: X = Xc + delta*sinh(s), s uniform.

    Resolves an (X-Xc)^{-1/2}-type singularity at Xc. `offset` shifts nodes by
    half a cell so none lands exactly on Xc (where a singular profile is infinite).
    Reach is +-M about Xc. n need not be odd here (the origin X=0 is generally not
    a node; the velocity pin interpolates U at X=0)."""
    if delta is None:
        delta = 4.0 / n
    s_hi = np.arcsinh((M) / delta)
    s_lo = np.arcsinh((-M) / delta)
    s = np.linspace(s_lo, s_hi, n)
    if offset:
        s = s + 0.5 * (s[1] - s[0])
    X = Xc + delta * np.sinh(s)
    return s, X


def sinh_grid_origin(n, c=0.5, rho_max=8.0):
    """Origin-clustered symmetric whole-line grid X = c*sinh(rho) (rho=0 => X=0 a
    node when n is odd). For the odd-symmetric degenerate-data hunt, where the
    singularity forms at the origin."""
    if n % 2 == 0:
        n += 1
    rho = np.linspace(-rho_max, rho_max, n)
    X = c * np.sinh(rho)
    return rho, X


# --------------------------------------------------------------------------
# explicit Theorem 2.3 anchor (closed forms)
# --------------------------------------------------------------------------
def omega_bar(X):
    """Explicit singular steady vorticity Omega_bar = (X-1)^{-1/2} 1_{X>1}."""
    X = np.asarray(X, dtype=float)
    out = np.zeros_like(X)
    m = X > 1.0
    out[m] = (X[m] - 1.0) ** (-0.5)
    return out


def H_omega_bar_exact(X):
    """Exact H(Omega_bar) = -(1-X)^{-1/2} 1_{X<1}, 0 for X>1."""
    X = np.asarray(X, dtype=float)
    out = np.zeros_like(X)
    m = X < 1.0
    out[m] = -((1.0 - X[m]) ** (-0.5))
    return out


def U_bar_exact(X):
    """Exact rescaled velocity U_bar = 2 sqrt(1-X) - 2 (X<1), -2 (X>=1)."""
    X = np.asarray(X, dtype=float)
    return np.where(X < 1.0, 2.0 * np.sqrt(np.maximum(1.0 - X, 0.0)) - 2.0, -2.0)


# --------------------------------------------------------------------------
# velocity operator  U_X = H(Omega),  U(X_ref) = 0
# --------------------------------------------------------------------------
def velocity(X, Homega, X_ref=0.0):
    """Integrate U from U_X = Homega on a (sorted-ascending) non-uniform grid,
    pinned to U(X_ref) = 0. Trapezoidal cumulative integral; U at X_ref is
    removed by linear interpolation so the pin is exact regardless of nodes."""
    X = np.asarray(X, dtype=float)
    Homega = np.asarray(Homega, dtype=float)
    dU = 0.5 * (Homega[1:] + Homega[:-1]) * np.diff(X)
    U = np.concatenate([[0.0], np.cumsum(dU)])
    U_ref = np.interp(X_ref, X, U)
    return U - U_ref


class RescaledHL:
    """Rescaled HL integrator on a fixed stretched grid.

    Fields: Omega (vorticity), Theta (buoyancy). Velocity U = velocity(H Omega).
    The grid X (sorted ascending) and its dense line-Hilbert operator are built
    once. This class currently exposes the velocity operator and the frozen-system
    RHS / steady residual (the validation-anchor surface); time stepping with the
    degenerate-case gauge is added on top once the static anchor is validated.
    """

    def __init__(self, X, X_ref=0.0):
        X = np.asarray(X, dtype=float)
        if np.any(np.diff(X) <= 0):
            raise ValueError("X must be strictly ascending")
        self.X = X
        self.n = X.size
        self.X_ref = X_ref
        self._Hmat = None  # built lazily on first hilbert() call (the O(N^2) op)

    @property
    def Hmat(self):
        """Dense line-Hilbert operator, built once on first use and cached. Runs
        that only ever use the exact/analytic H (validation anchors) never pay it."""
        if self._Hmat is None:
            self._Hmat = line_hilbert_matrix(self.X)
        return self._Hmat

    def hilbert(self, Omega):
        return self.Hmat @ Omega

    def velocity(self, Omega, Homega=None):
        if Homega is None:
            Homega = self.hilbert(Omega)
        return velocity(self.X, Homega, self.X_ref)

    def dX(self, f):
        """d f / dX via the natural cubic spline node slopes (matches line_hilbert)."""
        return natural_spline_slopes(self.X, f)

    def steady_residual(self, Omega, Theta, c_l, c_omega, U=None,
                        Omega_X=None, Theta_X=None):
        """Residual of the frozen steady system (2.5):
            R_Omega = (U + c_l X) Omega_X - c_omega Omega - Theta_X,
            R_Theta = (U + c_l X) Theta_X - (c_l + 2 c_omega) Theta.
        Derivatives default to the spline operator; pass analytic ones to isolate
        the velocity/assembly error from the differentiation error."""
        if U is None:
            U = self.velocity(Omega)
        if Omega_X is None:
            Omega_X = self.dX(Omega)
        if Theta_X is None:
            Theta_X = self.dX(Theta)
        transport = (U + c_l * self.X)
        R_Omega = transport * Omega_X - c_omega * Omega - Theta_X
        R_Theta = transport * Theta_X - (c_l + 2.0 * c_omega) * Theta
        return R_Omega, R_Theta


# --------------------------------------------------------------------------
# smooth degenerate initial data (one-sided; the Conjecture-2.4 basin test)
# --------------------------------------------------------------------------
def degenerate_ic(X, kind="A"):
    """Generic smooth *one-sided degenerate* initial data (Omega0, Theta0).

    "Degenerate" in the Chen-Huang-Li sense: Omega0(0)=Omega0_x(0)=0 and
    Theta0 flat to 2nd order at the origin (Theta0_xx(0)=0). One-sided:
    supp(Omega0), supp(Theta0) ~ [0, +infty). These are NOT CHL's specific data;
    the point of Conjecture 2.4 is that *any* such smooth degenerate datum should
    relax to the same singular profile -- so distinct `kind`s are the basin probe.
    Omega0 is a smooth positive bump vanishing to high order at 0 (degenerate) and
    decaying past the eventual singular region; Theta0 is a smooth 0 -> const step.
    Amplitude is a free gauge (the run renormalises H(Omega)(0) = -1), so only the
    *shapes* matter here."""
    X = np.asarray(X, dtype=float)
    xp = np.maximum(X, 0.0)
    if kind == "A":
        Omega0 = -(xp ** 3) * np.exp(-0.8 * xp)             # ~x^3 degen at 0
        Theta0 = (1.0 - np.exp(-0.5 * xp ** 2)) * np.exp(-0.05 * xp)
    elif kind == "B":
        Omega0 = -(xp ** 2) * np.exp(-0.6 * xp) * (1.0 + 0.5 * xp)
        Theta0 = xp ** 2 / (1.0 + xp ** 2) * np.exp(-0.03 * xp)  # x^2 -> flat step
    elif kind == "C":
        Omega0 = -(xp ** 4) * np.exp(-1.0 * np.sqrt(xp + 1e-12))
        Theta0 = (np.tanh(xp - 0.7) - np.tanh(-0.7)) * np.exp(-0.04 * xp)
    else:
        raise ValueError(f"unknown degenerate IC kind {kind!r}")
    Omega0 = np.where(X > 0.0, Omega0, 0.0)
    Theta0 = np.where(X > 0.0, Theta0, 0.0)
    return Omega0, Theta0


class RescaledHLDynamic(RescaledHL):
    """Dynamic-relaxation integrator for the rescaled HL system (2.4), with the
    Chen-Huang-Li *degenerate-case* normalization gauge (their (3.2)).

    The gauge is the crux for degenerate data. CHH22's non-degenerate gauge pins
    the origin slope Omega_x(0) -- which is *identically zero* for degenerate data,
    hence useless. CHL instead read the NONLOCAL velocity gradient U_X(0)=H(Omega)(0)
    (generically nonzero even when Omega_x(0)=0) for the amplitude, and pin the
    transport stagnation at X=1 for the location:

        c_l      = -U(1)                              (=> stagnation of U+c_l X at X=1)
        c_omega  = H( Theta_X - (U + c_l X) Omega_X )(0)   (holds U_X(0) fixed in tau)

    The amplitude gauge U_X(0) = H(Omega)(0) is fixed to -1 by renormalising the
    initial datum; c_omega then keeps it constant (monitored). At the exact
    Theorem-2.3 anchor this gauge returns (c_l, c_omega) = (2, -1) exactly, since
    Theta_X-(U+c_l X)Omega_X = Omega_bar there and H(Omega_bar)(0) = -1: a
    known-answer test of the gauge (see test_hl_rescaled.py).

    Time stepping: SSPRK3 in rescaled time tau. Advection (U+c_l X)*d/dX is upwinded
    in the *uniform* sinh coordinate s (X = 1 + delta*sinh s), so the dilation speed
    a(s) = (U+c_l X)/(delta cosh s) is bounded and the CFL stays ~ ds, independent of
    the reach M. The Theta_X *source* in the Omega equation uses the (accurate) spline
    slope; the transport derivatives use the upwind stencil for stability.
    """

    def __init__(self, n=2001, delta=0.01, M=500.0, nu=0.0):
        s, X = sinh_grid_at(n, Xc=1.0, delta=delta, M=M, offset=True)
        super().__init__(X, X_ref=0.0)
        self.s = s
        self.ds = s[1] - s[0]
        self.delta = delta
        self.dXds = delta * np.cosh(s)      # dX/ds > 0
        # Subgrid dissipation nu * d^2/ds^2 (in the uniform sinh coordinate). REQUIRED
        # for the singular target: the non-dissipative spline slopes ring at the X=1
        # discontinuity of the profile and the stiff Theta_X delta-source amplifies it,
        # so nu=0 is numerically unstable AT the profile (blows up from step 0). nu>0
        # holds it stably at the cost of an O(nu) profile bias -- a POC stabilizer, not
        # the WENO/adaptive-mesh treatment CHL use. Default 0 keeps the gauge tests
        # (which never time-step) dissipation-free.
        self.nu = nu

    # -- gauge ------------------------------------------------------------
    def gauge(self, Omega, Theta, U=None, Omega_X=None, Theta_X=None):
        """(c_l, c_omega) from CHL (3.2); also returns U and the spline slopes."""
        if U is None:
            U = self.velocity(Omega)
        if Omega_X is None:
            Omega_X = self.dX(Omega)
        if Theta_X is None:
            Theta_X = self.dX(Theta)
        c_l = -float(np.interp(1.0, self.X, U))
        g = Theta_X - (U + c_l * self.X) * Omega_X
        Hg = self.Hmat @ g
        c_omega = float(np.interp(0.0, self.X, Hg))
        return c_l, c_omega, U, Omega_X, Theta_X

    def normalize_amp(self, Omega, target=-1.0):
        """Rescale Omega so the amplitude gauge H(Omega)(0)=U_X(0)=target holds."""
        Homega = self.hilbert(Omega)
        h0 = float(np.interp(0.0, self.X, Homega))
        if abs(h0) < 1e-14:
            raise ValueError("H(Omega)(0) ~ 0; cannot set the amplitude gauge")
        return Omega * (target / h0)

    def amp_gauge(self, Omega):
        """Current value of the amplitude gauge U_X(0)=H(Omega)(0) (target -1)."""
        return float(np.interp(0.0, self.X, self.hilbert(Omega)))

    # -- dynamics ---------------------------------------------------------
    def rhs(self, Omega, Theta):
        """(L_Omega, L_Theta, c_l, c_omega) for the rescaled system (2.4)."""
        U = self.velocity(Omega)
        Omega_X = self.dX(Omega)
        Theta_X = self.dX(Theta)
        c_l, c_omega, U, Omega_X, Theta_X = self.gauge(
            Omega, Theta, U=U, Omega_X=Omega_X, Theta_X=Theta_X)
        speed = U + c_l * self.X
        a_s = speed / self.dXds                       # bounded dilation speed in s
        transport_Om = a_s * _upwind_deriv(Omega, self.ds, a_s)
        transport_Th = a_s * _upwind_deriv(Theta, self.ds, a_s)
        L_Om = c_omega * Omega + Theta_X - transport_Om
        L_Th = (c_l + 2.0 * c_omega) * Theta - transport_Th
        if self.nu != 0.0:
            L_Om = L_Om + self.nu * self._diff_ss(Omega)
            L_Th = L_Th + self.nu * self._diff_ss(Theta)
        return L_Om, L_Th, c_l, c_omega

    def _diff_ss(self, f):
        """Second difference in the uniform s coordinate (subgrid dissipation)."""
        d = np.zeros_like(f)
        d[1:-1] = (f[2:] - 2.0 * f[1:-1] + f[:-2]) / self.ds ** 2
        return d

    def step(self, Omega, Theta, dt):
        """One SSPRK3 (Shu-Osher) step; returns (Om, Th, c_l, c_omega, res)."""
        L0o, L0t, c_l, c_omega = self.rhs(Omega, Theta)
        o1, t1 = Omega + dt * L0o, Theta + dt * L0t
        L1o, L1t, _, _ = self.rhs(o1, t1)
        o2 = 0.75 * Omega + 0.25 * (o1 + dt * L1o)
        t2 = 0.75 * Theta + 0.25 * (t1 + dt * L1t)
        L2o, L2t, _, _ = self.rhs(o2, t2)
        on = (1.0 / 3.0) * Omega + (2.0 / 3.0) * (o2 + dt * L2o)
        tn = (1.0 / 3.0) * Theta + (2.0 / 3.0) * (t2 + dt * L2t)
        res = float(np.abs(L0o).max())
        return on, tn, c_l, c_omega, res

    def max_speed_s(self, Omega):
        """max |a(s)| for the CFL, using c_l from the current gauge."""
        U = self.velocity(Omega)
        c_l = -float(np.interp(1.0, self.X, U))
        return float(np.abs((U + c_l * self.X) / self.dXds).max())

    def run(self, Omega0, Theta0, dt_frac=0.3, tol=1e-6, max_steps=200000,
            renorm_amp=True, verbose=False, record_every=200):
        """Relax (2.4) from (Omega0, Theta0) toward the singular steady state.

        Returns a result dict with the (c_l, c_omega) histories (the gauge-invariant
        observables that Conjecture 2.4 predicts converge to (2, -1)) and the final
        fields. `renorm_amp` re-imposes the amplitude gauge H(Omega)(0)=-1 each step
        to suppress slow gauge drift (the c_omega choice enforces it only to O(dt))."""
        Omega = self.normalize_amp(np.array(Omega0, dtype=float))
        Theta = np.array(Theta0, dtype=float)
        a_max = self.max_speed_s(Omega)
        dt = dt_frac * self.ds / max(a_max, 1e-6)
        tau = 0.0
        cl_h, cw_h, res_h, tau_h, amp_h = [], [], [], [], []
        res, c_l, c_omega = np.inf, np.nan, np.nan
        step = 0
        for step in range(max_steps):
            Omega, Theta, c_l, c_omega, res = self.step(Omega, Theta, dt)
            if renorm_amp:
                Omega = self.normalize_amp(Omega)
            tau += dt
            if step % record_every == 0 or res < tol:
                cl_h.append(c_l); cw_h.append(c_omega); res_h.append(res)
                tau_h.append(tau); amp_h.append(self.amp_gauge(Omega))
                if verbose:
                    print(f"    step {step:6d} tau={tau:8.3f} c_l={c_l:+.5f} "
                          f"c_omega={c_omega:+.5f} res={res:.2e}", flush=True)
            if res < tol:
                break
            if not np.isfinite(res) or res > 1e8:
                break
        return {
            "Omega": Omega, "Theta": Theta, "X": self.X, "s": self.s,
            "c_l": c_l, "c_omega": c_omega, "residual": res, "tau": tau,
            "steps": step + 1, "converged": bool(res < tol),
            "c_l_hist": np.array(cl_h), "c_omega_hist": np.array(cw_h),
            "res_hist": np.array(res_h), "tau_hist": np.array(tau_h),
            "amp_hist": np.array(amp_h),
        }
