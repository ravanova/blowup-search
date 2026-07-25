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
