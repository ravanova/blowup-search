"""Step-B validation, piece 1 (PHASE2_SPIKE1_NOTES.md sec.3): the 2D upwind TRANSPORT
operator (c_l x + u).grad f on the log-radial x angular grid, against MANUFACTURED known
answers. This is the highest-risk new numerical kernel of Step B (2D upwind advection on
the curved, stretched grid), de-risked standalone before the coupled solver -- same
discipline as Step A's velocity operator.

Pre-committed predicate:
  1. For an analytic advecting field A and scalar f, transport(f,...) matches the exact
     A.grad f in relative L-inf on the resolved interior, to a stated tol;
  2. the error DECREASES under grid refinement (convergence, not a lucky single grid);
  3. exact structural checks: rigid rotation of a radial field gives zero; pure dilation
     of f reduces to f_rho on the log grid.

Manufactured field: f = e^{-r} sin(2 beta) (smooth, decaying, a single angular mode so the
angular part is clean). For an analytic advecting velocity A = (A_x, A_y),
    A.grad f = A_x f_x + A_y f_y,   f_x = cos b f_r - (sin b/r) f_b,  f_y = sin b f_r + (cos b/r) f_b,
    f_r = -e^{-r} sin 2b,   f_b = 2 e^{-r} cos 2b.
We drive `transport` with (u, v) = A and c_l = 0 so A is exactly the advecting field.

Run:  python test_boussinesq_transport.py
"""

import numpy as np

from solver.boussinesq_velocity import PolarGrid
from solver.boussinesq_rescaled import transport, advection_speeds


def _f_and_derivs(grid):
    """f = e^{-r} sin(2 beta) and its analytic f_x, f_y on the grid."""
    r = grid.R
    b = grid.B
    e = np.exp(-r)
    f = e * np.sin(2 * b)
    f_r = -e * np.sin(2 * b)
    f_b = e * 2 * np.cos(2 * b)
    f_x = np.cos(b) * f_r - (np.sin(b) / r) * f_b
    f_y = np.sin(b) * f_r + (np.cos(b) / r) * f_b
    return f, f_x, f_y


def _rel_linf(a, b, sl):
    num = np.max(np.abs(a[sl] - b[sl]))
    den = max(np.max(np.abs(b[sl])), 1e-300)
    return float(num / den)


def _interior(grid, rmargin=6, bmargin=2):
    """Resolved-interior slice: drop radial rings near the BC/round-off and the two angular
    rows adjacent to the boundaries (the beta grid is interior-only, so the upwind stencil
    there lacks boundary ghosts -- a coupled-solver concern, not a transport-kernel one)."""
    return (slice(rmargin, -rmargin), slice(bmargin, -bmargin))


def test_rigid_rotation_of_radial_field_is_zero():
    """A = (y, -x) (rigid rotation) advecting a purely radial field must give ~0: rotation
    has no radial component and the field has no angular variation."""
    grid = PolarGrid(n_r=400, n_beta=64, r_min=1e-2, r_max=30.0)
    r = grid.R
    frad = np.exp(-r) * (1.0 + 0.5 * r)  # radial only
    u = grid.Y            # A_x = y
    v = -grid.X           # A_y = -x
    t = transport(frad, u, v, grid, c_l=0.0)
    sl = _interior(grid)
    amp = np.max(np.abs(frad[sl]))
    assert np.max(np.abs(t[sl])) / amp < 1e-12, "rotation of radial field not zero"
    print("[ok] rigid rotation of a radial field -> 0")


def test_pure_dilation_reduces_to_f_rho():
    """A = (x, y) (pure dilation, = c_l x with c_l=1, u=v=0): transport = r f_r = f_rho.
    Structural identity of the log grid; check against a central rho-difference of f."""
    grid = PolarGrid(n_r=500, n_beta=48, r_min=1e-2, r_max=30.0)
    f, _, _ = _f_and_derivs(grid)
    t = transport(f, np.zeros_like(f), np.zeros_like(f), grid, c_l=1.0)
    # exact: r f_r = r * (-e^{-r}) sin2b
    exact = grid.R * (-np.exp(-grid.R)) * np.sin(2 * grid.B)
    sl = _interior(grid)
    err = _rel_linf(t, exact, sl)
    assert err < 5e-3, f"dilation transport err {err:.2e}"
    print(f"[ok] pure dilation transport = f_rho: rel err {err:.2e}")


def test_manufactured_advection_known_answer():
    """General analytic A = (x + y, y - x) (dilation + rotation): both s_rho and s_beta are
    nonzero and change sign across the grid, exercising both upwind branches."""
    grid = PolarGrid(n_r=700, n_beta=64, r_min=1e-2, r_max=30.0)
    f, f_x, f_y = _f_and_derivs(grid)
    Ax = grid.X + grid.Y
    Ay = grid.Y - grid.X
    exact = Ax * f_x + Ay * f_y
    t = transport(f, Ax, Ay, grid, c_l=0.0)
    sl = _interior(grid)
    err = _rel_linf(t, exact, sl)
    assert err < 5e-3, f"advection rel L-inf err {err:.2e}"
    print(f"[ok] manufactured advection (dilation+rotation): rel err {err:.2e}")


def test_convergence_under_refinement():
    """Error must DECREASE under joint (radial+angular) refinement (Spike-0 discipline)."""
    errs = []
    for scale in (1, 2, 4):
        grid = PolarGrid(n_r=250 * scale, n_beta=32 * scale, r_min=1e-2, r_max=30.0)
        f, f_x, f_y = _f_and_derivs(grid)
        Ax = grid.X + grid.Y
        Ay = grid.Y - grid.X
        exact = Ax * f_x + Ay * f_y
        t = transport(f, Ax, Ay, grid, c_l=0.0)
        errs.append(_rel_linf(t, exact, _interior(grid)))
    assert errs[1] < errs[0] and errs[2] < errs[1], f"not monotone: {errs}"
    rate = np.log2(errs[0] / errs[2]) / 2.0
    assert rate > 1.5, f"convergence order {rate:.2f} below ~2nd"
    print(f"[ok] transport convergence: errs {[f'{e:.2e}' for e in errs]}, order ~{rate:.2f}")


def test_advection_speeds_cfl_bounded_at_far_field():
    """s_rho -> c_l (bounded) and s_beta -> 0 at large r when u,v decay: the Spike-0 CFL cure
    carries to 2D (dilation speed is c_l in rho, independent of the domain reach)."""
    grid = PolarGrid(n_r=400, n_beta=48, r_min=1e-2, r_max=1e4)
    u = np.exp(-grid.R) * grid.Y  # decaying velocity
    v = -np.exp(-grid.R) * grid.X
    CL = 3.0
    s_rho, s_beta = advection_speeds(u, v, grid, c_l=CL)
    outer = grid.r > 1e2
    assert np.max(np.abs(s_rho[outer] - CL)) < 1e-3, "s_rho does not -> c_l far field"
    assert np.max(np.abs(s_beta[outer])) < 1e-3, "s_beta does not decay far field"
    print(f"[ok] far-field CFL: s_rho -> {CL} (dev {np.max(np.abs(s_rho[outer]-CL)):.1e}), s_beta -> 0")


if __name__ == "__main__":
    test_rigid_rotation_of_radial_field_is_zero()
    test_pure_dilation_reduces_to_f_rho()
    test_manufactured_advection_known_answer()
    test_convergence_under_refinement()
    test_advection_speeds_cfl_bounded_at_far_field()
    print("\nALL BOUSSINESQ-TRANSPORT (STEP B, PIECE 1) TESTS PASSED")
