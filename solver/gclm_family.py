"""Rescaled self-similar residual for the generalized CLM (gCLM) `a`-family.

This is the *problem definition* consumed by the global GA search
(solver/ga_search.py) and, later, reusable as the residual a rigorous
interval-Newton (Route D) step would certify. It is deliberately SEPARATE from
the a=0 dynamic-rescaling relaxation (solver/gclm_rescaled.py::RescaledCLM):
that file time-STEPS to a local attractor; this file evaluates the steady
RESIDUAL of an arbitrary candidate profile so a global optimizer can score it.

Model. The gCLM family on the whole line (Okamoto-Sakajo-Wunsch convention)

    omega_t + a u omega_x = omega H(omega),     u_x = H(omega),  u(0)=0,

with a the advection parameter: a=0 is CLM (no advection; exactly solvable,
HQW25 arXiv:2401.14615), a=1 is De Gregorio. Dynamic self-similar rescaling
omega(x,t) = C_omega^{-1} Omega(X), X = C_l x, dtau/dt = C_omega^{-1} carries the
equation to the rescaled profile equation whose steady state is the self-similar
profile. Writing U(X) = int_0^X H(Omega) dX' (the rescaled velocity, U(0)=0),
the rescaled evolution is

    Omega_tau = (c_omega + H Omega) Omega - c_l X Omega_X - a U Omega_X,     (*)

so the steady RESIDUAL scored here is

    R(Omega; c_omega, c_l, a) = (c_omega + H Omega) Omega - c_l X Omega_X - a U Omega_X.

At a=0 this is EXACTLY the residual of RescaledCLM (validated): with the origin
gauge c_omega = 1 - H Omega(0) and c_l = 1, the exact steady state is
Omega_0(X) = -4 X / (1 + 4 X^2) on the c=0.5 sinh grid (H Omega_0 = 2/(1+4X^2),
H Omega_0(0) = 2, c_omega = -1). test_gclm_family.py checks R(Omega_0) -> 0 to
machine precision as the KNOWN-ANSWER GATE, and that the GA recovers Omega_0.

Gauge discipline (banked lesson). c_omega, c_l are a NORMALIZATION gauge, not
results. The physical, gauge-invariant self-similar exponent is the RATIO
c_l / c_omega and the profile SHAPE; report only those. The origin gauge
c_omega = 1 - H Omega(0) is the amplitude convention of the a=0 anchor and is
reused here so a=0 lands exactly on Omega_0.

Grid + Hilbert transform are the fixed-grid whole-line operators from
solver/gclm_rescaled.py (sinh_grid) and solver/line_hilbert.py (dense Hmat),
built once and reused for every residual evaluation (the GA calls this on a
whole population every generation, so the operators must be cached).
"""

import numpy as np

from solver.gclm_rescaled import sinh_grid
from solver.line_hilbert import line_hilbert_matrix


def _drho_centered4(f, drho):
    """4th-order centered d f/d rho on the uniform rho grid; one-sided at ends.

    Profiles are smooth and decay to ~0 near the domain ends, so the reduced
    end-accuracy is harmless (Omega ~ 0 there). Used for the residual's spatial
    derivative Omega_rho; the physical derivative is Omega_X = Omega_rho / X_rho,
    and X Omega_X = tanh(rho) Omega_rho on the sinh coordinate."""
    n = f.size
    d = np.zeros(n)
    i = np.arange(2, n - 2)
    d[i] = (-f[i + 2] + 8 * f[i + 1] - 8 * f[i - 1] + f[i - 2]) / (12 * drho)
    # near-boundary: 2nd-order centered where possible, one-sided at the very ends
    d[1] = (f[2] - f[0]) / (2 * drho)
    d[n - 2] = (f[n - 1] - f[n - 3]) / (2 * drho)
    d[0] = (-3 * f[0] + 4 * f[1] - f[2]) / (2 * drho)
    d[n - 1] = (3 * f[n - 1] - 4 * f[n - 2] + f[n - 3]) / (2 * drho)
    return d


def _velocity_matrix(X, i0):
    """Matrix V with U = V @ g the cumulative trapezoid of g=H(Omega) from X=0.

    U(X) = int_0^X g dX', U(0)=0, built by trapezoid marching OUTWARD from the
    center node i0 in both directions. Grid is fixed, so this is assembled once
    and reused (like the Hilbert matrix). Returns dense (n, n)."""
    n = X.size
    V = np.zeros((n, n))
    dX = np.diff(X)
    # march up:  U[i] = U[i-1] + 0.5*(g[i]+g[i-1])*dX[i-1]
    for i in range(i0 + 1, n):
        w = 0.5 * dX[i - 1]
        V[i] = V[i - 1]
        V[i, i] += w
        V[i, i - 1] += w
    # march down: U[i] = U[i+1] - 0.5*(g[i]+g[i+1])*dX[i]
    for i in range(i0 - 1, -1, -1):
        w = 0.5 * dX[i]
        V[i] = V[i + 1]
        V[i, i] -= w
        V[i, i + 1] -= w
    return V


class GCLMResidual:
    """Steady self-similar residual (*) of the gCLM `a`-family on a fixed grid.

    One instance per (grid, a); the Hilbert and velocity operators are cached so
    a whole GA population is scored by cheap matvecs. `a` is a SWEEP parameter
    (fixed per instance) -- the transition map is built by instantiating across a
    range of a, not by evolving a inside one search."""

    def __init__(self, a=0.0, n=1201, c=0.5, rho_max=8.0):
        self.a = float(a)
        self.c = float(c)
        self.rho, self.X = sinh_grid(n, c=c, rho_max=rho_max)
        self.n = self.X.size
        self.i0 = self.n // 2  # rho=0 <=> X=0 node
        self.drho = self.rho[1] - self.rho[0]
        self.tanh = np.tanh(self.rho)
        self.X_rho = self.c * np.cosh(self.rho)   # dX/drho > 0 everywhere (>= c)
        self.Hmat = line_hilbert_matrix(self.X)
        self.Vmat = _velocity_matrix(self.X, self.i0)

    # -- operators -----------------------------------------------------------
    def hilbert(self, Omega):
        return self.Hmat @ Omega

    def velocity(self, Omega):
        """Rescaled velocity U(X) = int_0^X H(Omega) dX', U(0)=0."""
        return self.Vmat @ (self.Hmat @ Omega)

    def gauge_c_omega(self, Omega):
        """Origin amplitude gauge c_omega = 1 - H(Omega)(0) (a=0 anchor convention)."""
        return 1.0 - (self.Hmat @ Omega)[self.i0]

    # -- residual ------------------------------------------------------------
    def residual(self, Omega, c_omega=None, c_l=1.0):
        """R(Omega) on the grid. If c_omega is None, use the origin gauge.

        R = (c_omega + H Omega) Omega - c_l * X Omega_X - a * U Omega_X,
        with X Omega_X = tanh(rho) Omega_rho and U = int_0^X H Omega."""
        HOmega = self.Hmat @ Omega
        if c_omega is None:
            c_omega = 1.0 - HOmega[self.i0]
        Omega_rho = _drho_centered4(Omega, self.drho)
        Omega_X = Omega_rho / self.X_rho              # Omega_X, no 0/0 (X_rho >= c)
        XOmega_X = self.X * Omega_X                   # = X Omega_X (= tanh(rho) Omega_rho)
        source = (c_omega + HOmega) * Omega
        R = source - c_l * XOmega_X
        if self.a != 0.0:
            U = self.Vmat @ HOmega                    # rescaled velocity, U(0)=0
            R = R - self.a * U * Omega_X              # advection - a U Omega_X
        return R, c_omega, c_l

    def residual_norm(self, Omega, c_omega=None, c_l=1.0, weight=None):
        """Scalar ||R||: RMS over the grid (optionally weighted). The GA fitness."""
        R, _, _ = self.residual(Omega, c_omega=c_omega, c_l=c_l)
        if weight is not None:
            R = R * weight
        return float(np.sqrt(np.mean(R ** 2)))


# --------------------------------------------------------------------------
# low-dimensional parametric profile families (the GA genome -> Omega map)
# --------------------------------------------------------------------------
#
# A GA over hundreds of raw grid values is just slow gradient descent; it earns
# its keep only over a COMPACT parameterization. These families are odd/even by
# construction (matching the one-scale / two-scale symmetry) and are rich enough
# to represent the exact anchors as a special case (the known-answer gate):
#   * odd_rational  with K=1 represents Omega_0 = -4X/(1+4X^2)  (params A=-4,B=4)
#   * even_lorentz  with K=1 represents HQW25's two-scale bump Omega_2 (even).


def odd_rational(X, params):
    """Odd profile  Omega(X) = sum_k A_k * X / (1 + B_k X^2),  B_k > 0.

    genome = [A_1, B_1, A_2, B_2, ...]. One-scale / De-Gregorio-type profiles
    (odd, ~1/X decay). K=1 with (A,B)=(-4,4) is the exact a=0 CLM anchor."""
    p = np.asarray(params, dtype=float)
    K = p.size // 2
    A = p[0::2][:K]
    B = np.abs(p[1::2][:K]) + 1e-9
    out = np.zeros_like(X)
    for k in range(K):
        out = out + A[k] * X / (1.0 + B[k] * X ** 2)
    return out


def even_lorentz(X, params):
    """Even bump  Omega(X) = sum_k A_k / (1 + B_k X^2),  B_k > 0.

    Two-scale-type profiles (even Lorentzian bulk, peaked at X=0), the symmetry
    of HQW25's Omega_2. genome = [A_1, B_1, ...]."""
    p = np.asarray(params, dtype=float)
    K = p.size // 2
    A = p[0::2][:K]
    B = np.abs(p[1::2][:K]) + 1e-9
    out = np.zeros_like(X)
    for k in range(K):
        out = out + A[k] / (1.0 + B[k] * X ** 2)
    return out


# exact anchors (for tests / GA gate targets) -------------------------------

def clm_one_scale(X):
    """Exact a=0 CLM one-scale steady profile on the c=0.5 grid: -4X/(1+4X^2)."""
    return -4.0 * X / (1.0 + 4.0 * X ** 2)
