"""Step-A validation for Spike 1 (PHASE2_SPIKE1_NOTES.md sec.3): the 2D Boussinesq
velocity operator u = grad^perp (-Lap)^{-1} omega on the stretched (log-radial x
angular-sine) quarter-plane grid, against a MANUFACTURED KNOWN SOLUTION.

Pre-committed predicate (before trusting anything downstream):
  1. recovered phi, u, v match the analytic answer in relative L-inf to a stated tol;
  2. the error DECREASES under radial refinement (convergence, not a lucky single grid);
  3. u_x(0) -- the origin read the modulation (2.11) depends on -- matches analytics.

Manufactured solution (single angular mode n=1, so the angular part is exact and the
error is a clean radial O(drho^2)):
    phi*  = r^2 e^{-r} sin(2 beta)
    omega* = -Lap phi* = (5r - r^2) e^{-r} sin(2 beta)
    u* = -phi*_y,  v* = phi*_x    (analytic, below)
Near the origin phi* -> r^2 sin(2b) = 2 x y, so u* -> -2x and u_x(0) = -2.

Run:  python test_boussinesq_velocity.py
"""

import numpy as np

from solver.boussinesq_velocity import (
    PolarGrid,
    poisson_solve,
    velocity_from_vorticity,
    u_x_at_origin,
)


def _manufactured(grid, modes=(1,)):
    """Return (omega, phi, u, v) on the grid for phi = sum_n R_n(r) sin(2n beta), with
    R_1 = r^2 e^{-r}, R_2 = r^4 e^{-r} (both ~ r^{2n}: regular at the origin, decaying).
    Per-mode radial Laplacian L[R_n] = R_n'' + R_n'/r - (2n)^2/r^2 R_n verified by hand:
      n=1: L = (r^2 - 5r) e^{-r}   -> omega_1 = (5r - r^2) e^{-r}
      n=2: L = (r^4 - 9r^3) e^{-r} -> omega_2 = (9r^3 - r^4) e^{-r}
    """
    r = grid.R
    b = grid.B
    e = np.exp(-r)
    R = {1: r**2 * e, 2: r**4 * e}
    Rp = {1: (2 * r - r**2) * e, 2: (4 * r**3 - r**4) * e}  # dR/dr
    omega = np.zeros_like(r)
    phi = np.zeros_like(r)
    phi_x = np.zeros_like(r)
    phi_y = np.zeros_like(r)
    om_radial = {
        1: (5 * r - r**2) * e,
        2: (9 * r**3 - r**4) * e,
    }
    for n in modes:
        s = np.sin(2 * n * b)
        cc = np.cos(2 * n * b)
        phi += R[n] * s
        omega += om_radial[n] * s
        # phi_x = cos b phi_r - (sin b / r) phi_b ; phi_b = R * 2n cos(2n b)
        phi_r = Rp[n] * s
        phi_b = R[n] * (2 * n) * cc
        phi_x += np.cos(b) * phi_r - (np.sin(b) / r) * phi_b
        phi_y += np.sin(b) * phi_r + (np.cos(b) / r) * phi_b
    u = -phi_y
    v = phi_x
    return omega, phi, u, v


def _rel_linf(a, b):
    return float(np.max(np.abs(a - b)) / max(np.max(np.abs(b)), 1e-300))


def test_angular_transform_roundtrip():
    """DST-I forward/inverse is an identity, and a known 2-mode field decomposes exactly."""
    grid = PolarGrid(n_r=32, n_beta=40)
    f = np.random.RandomState(1).standard_normal((grid.n_r, grid.n_beta))
    assert _rel_linf(grid.from_modes(grid.to_modes(f)), f) < 1e-12
    # a pure sin(2n beta) field has a single nonzero mode coefficient (per radius)
    field = np.sin(2 * 3 * grid.B)  # n=3
    fn = grid.to_modes(field)
    peak = np.abs(fn).max(axis=0)
    assert peak[2] > 0.9 and np.delete(peak, 2).max() < 1e-10
    print("[ok] angular DST-I round-trips and isolates modes")


def test_poisson_interior_dirichlet():
    """Interior discretization: with exact radial Dirichlet BCs, recover phi to O(drho^2)."""
    grid = PolarGrid(n_r=600, n_beta=48, r_min=1e-3, r_max=40.0)
    omega, phi_ex, _, _ = _manufactured(grid, modes=(1, 2))
    phi = poisson_solve(omega, grid, radial_bc="dirichlet", phi_exact=phi_ex)
    err = _rel_linf(phi, phi_ex)
    assert err < 1e-3, f"phi rel L-inf err {err:.2e}"
    print(f"[ok] Poisson interior (Dirichlet BC), 2-mode: phi rel err {err:.2e}")


def test_velocity_known_answer():
    """The headline crux: recover u, v from omega on the stretched grid, robin far-field."""
    grid = PolarGrid(n_r=800, n_beta=48, r_min=1e-3, r_max=40.0)
    omega, phi_ex, u_ex, v_ex = _manufactured(grid, modes=(1,))
    u, v, phi = velocity_from_vorticity(omega, grid, radial_bc="robin")
    # compare on the resolved bulk (exclude the outermost radial ring near the BC and the
    # innermost where r^2 is at round-off scale)
    sl = slice(5, -5)
    eu = _rel_linf(u[sl], u_ex[sl])
    ev = _rel_linf(v[sl], v_ex[sl])
    ep = _rel_linf(phi[sl], phi_ex[sl])
    assert ep < 5e-3, f"phi err {ep:.2e}"
    assert eu < 5e-3, f"u err {eu:.2e}"
    assert ev < 5e-3, f"v err {ev:.2e}"
    print(f"[ok] velocity from vorticity (robin): phi {ep:.2e}, u {eu:.2e}, v {ev:.2e}")


def test_convergence_under_refinement():
    """Error must DECREASE under radial refinement (Spike-0 discipline: convergence, not a
    lucky single grid). Expect ~2nd order in drho for the single-mode manufactured field."""
    errs = []
    for n_r in (200, 400, 800):
        grid = PolarGrid(n_r=n_r, n_beta=48, r_min=1e-3, r_max=40.0)
        omega, phi_ex, _, _ = _manufactured(grid, modes=(1,))
        phi = poisson_solve(omega, grid, radial_bc="dirichlet", phi_exact=phi_ex)
        errs.append(_rel_linf(phi[3:-3], phi_ex[3:-3]))
    assert errs[1] < errs[0] and errs[2] < errs[1], f"not monotone: {errs}"
    rate = np.log2(errs[0] / errs[2]) / 2.0  # order over the 4x refinement
    assert rate > 1.5, f"convergence order {rate:.2f} below 2nd order"
    print(f"[ok] radial convergence: errs {[f'{e:.2e}' for e in errs]}, order ~{rate:.2f}")


def test_u_x_at_origin():
    """u_x(0) = -2 for the manufactured field -- the modulation (2.11) origin read."""
    grid = PolarGrid(n_r=800, n_beta=48, r_min=1e-3, r_max=40.0)
    omega, phi_ex, _, _ = _manufactured(grid, modes=(1, 2))
    _, _, phi = velocity_from_vorticity(omega, grid, radial_bc="robin")
    ux0 = u_x_at_origin(phi, grid)
    assert abs(ux0 - (-2.0)) < 1e-3, f"u_x(0) = {ux0:.4f}, expected -2"
    print(f"[ok] u_x(0) origin read: {ux0:.4f} (expected -2)")


if __name__ == "__main__":
    test_angular_transform_roundtrip()
    test_poisson_interior_dirichlet()
    test_velocity_known_answer()
    test_convergence_under_refinement()
    test_u_x_at_origin()
    print("\nALL BOUSSINESQ-VELOCITY (STEP A) TESTS PASSED")
