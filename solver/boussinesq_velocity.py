"""Step A of Spike 1 (PHASE2_SPIKE1_NOTES.md): the 2D Boussinesq velocity operator
u = grad^perp (-Lap)^{-1} omega on a stretched grid, standalone + validatable.

This is the 2D analogue of Spike 0's non-FFT line Hilbert transform: on the uniform
periodic grid the Biot-Savart/Poisson solve is a trivial FFT multiplier, but the
self-similar profile lives on the whole quarter-plane with a slow r^{-1/3} tail, so we
need a *stretched* grid, and FFT cannot go there.

GEOMETRY (Chen-Hou 2D Boussinesq, arXiv:2210.07191 (2.3)-(2.5), MMS-Numerics-2025 (2.5)).
Physical: -Lap phi = omega on the upper half-plane {y>=0} with phi=0 on the wall y=0, and
u = -phi_y, v = phi_x. With omega ODD in x and theta EVEN in x, phi is odd in x, so phi=0
on the axis x=0 as well: the effective domain is the first quadrant [0,inf)^2 with the
singular corner at the origin, and phi has DIRICHLET data on both boundaries beta=0 (wall)
and beta=pi/2 (axis).

DISCRETIZATION (POC-fidelity; see PHASE2_SPIKE1_NOTES.md sec.2 for why this replaces the
paper's B-spline FEM). Polar (r, beta), beta in [0, pi/2]. Expand in the Dirichlet angular
sine basis sin(2 n beta), n=1..M-1 (a DST-I with kernel sin(pi j n / M)). On a LOG-radial
grid r = e^rho (uniform rho), the polar Laplacian
    Lap phi = phi_rr + (1/r) phi_r + (1/r^2) phi_bb
decouples per mode into a CONSTANT-COEFFICIENT ODE (a clean cancellation on the log grid):
    -Lap phi = omega   <=>   phi_n''(rho) - (2n)^2 phi_n = -r^2 omega_n(r),   per mode n,
a tridiagonal solve per mode (no scipy sparse). Homogeneous solutions r^{+-2n} carry the
near-origin regularity and the far-field tail analytically (the r^{-1/3} lever, POC-level).

Velocity: u = -phi_y, v = phi_x, with the polar chain rule
    phi_x = cos b phi_r - (sin b / r) phi_b,   phi_y = sin b phi_r + (cos b / r) phi_b,
    phi_r = phi_rho / r  (log grid),            phi_b via the sine-basis angular derivative.
"""

import numpy as np


class PolarGrid:
    """Log-radial x angular-sine grid on the first quadrant (r,beta), beta in (0,pi/2).

    Radial: rho uniform on [log r_min, log r_max], r = exp(rho), n_r points.
    Angular: beta_j = (pi/2) j / M, j=1..M-1 (M = n_beta+1 interior points), matching the
    DST-I sine basis sin(2 n beta_j) = sin(pi j n / M). Fields are stored as arrays of
    shape (n_r, n_beta) indexed [i, j] = (rho_i, beta_j).
    """

    def __init__(self, n_r=400, n_beta=48, r_min=1e-4, r_max=1e4):
        self.n_r = int(n_r)
        self.n_beta = int(n_beta)
        self.M = self.n_beta + 1  # sin(pi j n / M) DST-I size
        self.rho = np.linspace(np.log(r_min), np.log(r_max), self.n_r)
        self.drho = self.rho[1] - self.rho[0]
        self.r = np.exp(self.rho)  # (n_r,)
        j = np.arange(1, self.M)  # 1..M-1
        self.beta = (np.pi / 2.0) * j / self.M  # (n_beta,)
        self.n_modes = np.arange(1, self.M)  # angular mode numbers n = 1..M-1
        # DST-I matrix S[j-1, n-1] = sin(pi j n / M); S @ S = (M/2) I, so S^{-1} = (2/M) S.
        J, N = np.meshgrid(j, self.n_modes, indexing="ij")
        self.S = np.sin(np.pi * J * N / self.M)  # (n_beta, n_beta)
        self.C = np.cos(np.pi * J * N / self.M)  # for angular derivatives
        # 2D physical coordinates for convenience.
        self.R, self.B = np.meshgrid(self.r, self.beta, indexing="ij")
        self.X = self.R * np.cos(self.B)
        self.Y = self.R * np.sin(self.B)

    def to_modes(self, f):
        """Angular forward transform: grid values f[i,j] -> mode coeffs f_n[i,n]."""
        return (2.0 / self.M) * (f @ self.S)

    def from_modes(self, fn):
        """Angular inverse transform: mode coeffs f_n[i,n] -> grid values f[i,j]."""
        return fn @ self.S


def _thomas(a, b, c, d):
    """Solve a tridiagonal system with sub a, diag b, super c, rhs d (all length n).
    a[0] and c[-1] are unused. Returns x. Non-destructive."""
    n = len(b)
    cp = np.empty(n)
    dp = np.empty(n)
    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]
    for i in range(1, n):
        m = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / m
        dp[i] = (d[i] - a[i] * dp[i - 1]) / m
    x = np.empty(n)
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


def poisson_solve(omega, grid, radial_bc="robin", phi_exact=None):
    """Solve -Lap phi = omega on the quarter-plane, phi=0 on beta=0 and beta=pi/2.

    Per angular mode n: phi_n''(rho) - (2n)^2 phi_n = -r^2 omega_n(rho), tridiagonal in rho.

    radial_bc:
      "robin"  -- impose the analytic homogeneous tails: phi_n ~ r^{+2n} at r_min (regular
                  at the origin) and phi_n ~ r^{-2n} at r_max (decay). This is the physical
                  far-field lever (POC-level).
      "dirichlet" -- Dirichlet from phi_exact at both radial ends (used to validate the
                  INTERIOR discretization independent of the far-field BC modeling).
    Returns phi on the grid, shape (n_r, n_beta).
    """
    n_r = grid.n_r
    drho = grid.drho
    inv_dr2 = 1.0 / (drho * drho)
    omega_n = grid.to_modes(omega)  # (n_r, n_beta)
    r2 = grid.r ** 2
    phi_n = np.zeros_like(omega_n)

    if radial_bc == "dirichlet":
        if phi_exact is None:
            raise ValueError("dirichlet radial_bc requires phi_exact")
        phi_exact_n = grid.to_modes(phi_exact)

    for k, n in enumerate(grid.n_modes):
        lam = (2.0 * n) ** 2
        rhs = -r2 * omega_n[:, k]
        a = np.full(n_r, inv_dr2)
        b = np.full(n_r, -2.0 * inv_dr2 - lam)
        c = np.full(n_r, inv_dr2)
        d = rhs.copy()
        if radial_bc == "robin":
            # near-origin: dphi/drho = 2n phi  ->  -(1+2n*drho) phi_0 + phi_1 = 0
            b[0] = -(1.0 + 2.0 * n * drho)
            c[0] = 1.0
            a[0] = 0.0
            d[0] = 0.0
            # far-field: dphi/drho = -2n phi  ->  (1+2n*drho) phi_{-1} - phi_{-2} = 0
            b[-1] = 1.0 + 2.0 * n * drho
            a[-1] = -1.0
            c[-1] = 0.0
            d[-1] = 0.0
        else:  # dirichlet
            b[0] = 1.0
            c[0] = 0.0
            a[0] = 0.0
            d[0] = phi_exact_n[0, k]
            b[-1] = 1.0
            a[-1] = 0.0
            c[-1] = 0.0
            d[-1] = phi_exact_n[-1, k]
        phi_n[:, k] = _thomas(a, b, c, d)

    return grid.from_modes(phi_n)


def _phi_derivatives(phi, grid):
    """Return (phi_r, phi_b) on the grid. phi_r via log-grid central rho-differences
    (phi_r = phi_rho / r); phi_b via the sine-basis angular derivative."""
    # radial: central in rho, one-sided at ends.
    phi_rho = np.empty_like(phi)
    phi_rho[1:-1, :] = (phi[2:, :] - phi[:-2, :]) / (2.0 * grid.drho)
    phi_rho[0, :] = (phi[1, :] - phi[0, :]) / grid.drho
    phi_rho[-1, :] = (phi[-1, :] - phi[-2, :]) / grid.drho
    phi_r = phi_rho / grid.r[:, None]
    # angular: phi = sum phi_n sin(2n b) -> phi_b = sum phi_n (2n) cos(2n b).
    phi_n = grid.to_modes(phi)
    phi_b = (phi_n * (2.0 * grid.n_modes)[None, :]) @ grid.C
    return phi_r, phi_b


def velocity_from_vorticity(omega, grid, radial_bc="robin", phi_exact=None):
    """u = -phi_y, v = phi_x from -Lap phi = omega. Returns (u, v, phi)."""
    phi = poisson_solve(omega, grid, radial_bc=radial_bc, phi_exact=phi_exact)
    phi_r, phi_b = _phi_derivatives(phi, grid)
    cb = np.cos(grid.B)
    sb = np.sin(grid.B)
    phi_x = cb * phi_r - (sb / grid.R) * phi_b
    phi_y = sb * phi_r + (cb / grid.R) * phi_b
    u = -phi_y
    v = phi_x
    return u, v, phi


def u_x_at_origin(phi, grid, r_window=0.1):
    """u_x(0) = -phi_xy(0). Near the origin phi ~ c1 r^2 sin(2 beta) = 2 c1 x y (n=1 mode),
    so phi ~ 2 c1 x y  =>  u = -phi_y ~ -2 c1 x  =>  u_x(0) = -2 c1, with c1 = lim_{r->0}
    phi_1(r)/r^2 (phi_1 the n=1 radial coefficient). A clean, mode-localized origin read
    (contrast the noise-prone raw high-derivative reads of Spike-0 recon).

    We EXTRAPOLATE c1(r) = phi_1(r)/r^2 to r=0 by a linear fit over a small-r window,
    skipping the innermost nodes where the first-order Robin BC contaminates the read."""
    phi_n = grid.to_modes(phi)
    c1 = phi_n[:, 0] / (grid.r ** 2)  # n=1 mode coefficient / r^2 -> c1(r)
    mask = (grid.r > grid.r[2]) & (grid.r < r_window)
    rr = grid.r[mask]
    A = np.vstack([np.ones_like(rr), rr]).T  # fit c1 ~ a + b r, take a = c1(0)
    coef, *_ = np.linalg.lstsq(A, c1[mask], rcond=None)
    return -2.0 * float(coef[0])
