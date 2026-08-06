"""Leg 99 (Route-BVA) -- the ADVERSARIAL regression battery for
solver/boussinesq_velocity.py, banked alongside leg 73's known-answer gate in
test_boussinesq_velocity.py.

Leg 73 asked: is the answer RIGHT on a well-posed polar-grid problem? (Yes -- the Lamb
corner-image closed form to 1.76e-4 relative at observed order 2.00.)
This file asks the independent question: is a WRONG answer FLAGGED as wrong?

READ THIS BEFORE "FIXING" A FAILURE HERE
=========================================
Leg 99's gate answered YES: the module DOES silently return a finite, plausible-looking
wrong result on one reachable class of degenerate input. Per the gate's yes-branch that
defect was REPORTED AND ESCALATED, not patched -- solver/boussinesq_velocity.py is
unmodified by leg 99.

So the two tests below marked CHARACTERIZATION pin the DEFECT, not the desired behaviour.
They pass against the current, unpatched module. **When the module is patched, they will
fail, and that failure is the fix working.** Update them in the SAME commit as the patch:
the empty-fit-window case should then raise (or return NaN) rather than return -0.0.
Do not "repair" these tests by loosening them; that would erase the finding.

Every other test in this file pins behaviour that is already CORRECT and must stay correct:
NaN propagates instead of being swallowed, malformed shapes raise, a collapsed radial
extent does not silently produce a finite field.

Reference truth is leg 73's own manufactured field, reused verbatim so no new analytic
claim is introduced:
    phi*  = r^2 e^{-r} sin(2 beta),  w* = (5r - r^2) e^{-r} sin(2 beta),  u_x(0) = -2.

Run:  PYTHONPATH=. python test_boussinesq_velocity_adversarial.py
Full measurement: experiments/p2_route_bva_v1_adversarial.py
Findings:         writeup/novelty/leg_99.md
"""

import warnings

import numpy as np

from solver.boussinesq_velocity import (
    PolarGrid,
    velocity_from_vorticity,
    u_x_at_origin,
)

# leg 73's own acceptance tolerances, used here only as yardsticks
LEG73_FIELD_TOL = 5e-3
LEG73_ORIGIN_TOL = 1e-3
UX0_TRUTH = -2.0


def _manufactured(grid):
    """(omega, phi, u, v) for phi = r^2 e^{-r} sin(2 beta) -- leg 73's single-mode field."""
    r, b = grid.R, grid.B
    e = np.exp(-r)
    s = np.sin(2 * b)
    cc = np.cos(2 * b)
    phi = r ** 2 * e * s
    omega = (5 * r - r ** 2) * e * s
    phi_r = (2 * r - r ** 2) * e * s
    phi_b = r ** 2 * e * 2.0 * cc
    phi_x = np.cos(b) * phi_r - (np.sin(b) / r) * phi_b
    phi_y = np.sin(b) * phi_r + (np.cos(b) / r) * phi_b
    return omega, phi, -phi_y, phi_x


def _rel_linf(a, b):
    return float(np.max(np.abs(a - b)) / max(float(np.max(np.abs(b))), 1e-300))


# ======================================================================================
# CHARACTERIZATION -- these pin the DEFECT leg 99 found. See the header.
# ======================================================================================

def test_characterization_empty_fit_window_fabricates_zero():
    """DEFECT (leg 99 headline). u_x_at_origin fits c1(r) = phi_1(r)/r^2 over the window
    (grid.r[2], r_window). The occupancy of that window is never checked. With r_min above
    r_window the mask is empty, np.linalg.lstsq on a (0,2) design matrix returns [0.,0.] at
    rank 0 without raising or warning, and the function returns -0.0 -- a finite,
    physically plausible-looking value ("the origin strain vanishes") that is 100% wrong.
    """
    grid = PolarGrid(n_r=200, n_beta=16, r_min=0.15, r_max=40.0)  # r_min > r_window=0.1
    omega, _, _, _ = _manufactured(grid)
    _, _, phi = velocity_from_vorticity(omega, grid)

    mask = (grid.r > grid.r[2]) & (grid.r < 0.1)
    assert mask.sum() == 0, "precondition: the fit window must be empty for this case"

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        ux0 = u_x_at_origin(phi, grid)

    assert np.isfinite(ux0), "characterization: the value comes back finite"
    assert ux0 == 0.0, f"characterization: expected a fabricated 0.0, got {ux0!r}"
    assert len(caught) == 0, f"characterization: no warning is emitted, got {len(caught)}"

    abs_err = abs(ux0 - UX0_TRUTH)
    assert abs_err > 1.9, f"the fabricated value must be ~100% wrong, abs err {abs_err:.3f}"
    assert abs_err / LEG73_ORIGIN_TOL > 1e3, "and far outside leg 73's own origin tolerance"
    print(f"[DEFECT] empty fit window: u_x(0) = {ux0:+.1f} (truth {UX0_TRUTH}), "
          f"abs err {abs_err:.4f} = {100 * abs_err / abs(UX0_TRUTH):.1f}% relative, "
          f"{abs_err / LEG73_ORIGIN_TOL:.0f}x leg 73's origin tol, 0 warnings, 0 exceptions")


def test_characterization_reversed_radial_interval_hides_local_damage():
    """DEFECT (leg 99, second). A reversed radial interval r_min > r_max is accepted without
    complaint. The interior discretization survives (the Thomas solve sees only drho^2) but
    the two radial Dirichlet ends swap, so the far-field decay tail phi ~ r^{-2n} is imposed
    at the singular corner where the truth is phi ~ r^{+2n}. The GLOBAL relative error stays
    inside leg 73's 5e-3 acceptance and is therefore invisible to every existing test, while
    the LOCAL error at the origin end blows through it.
    """
    def solve(r_min, r_max):
        grid = PolarGrid(n_r=400, n_beta=16, r_min=r_min, r_max=r_max)
        omega, phi_ex, _, _ = _manufactured(grid)
        _, _, phi = velocity_from_vorticity(omega, grid)
        near = grid.r < 0.05
        return grid, phi, _rel_linf(phi, phi_ex), _rel_linf(phi[near], phi_ex[near])

    g_ok, _, glob_ok, near_ok = solve(1e-3, 40.0)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        g_bad, phi_bad, glob_bad, near_bad = solve(40.0, 1e-3)

    assert g_bad.drho < 0 < g_ok.drho, "the reversed grid must have a negative drho"
    assert np.isfinite(phi_bad).all(), "characterization: the reversed grid returns all-finite"
    assert len(caught) == 0, "characterization: and emits no warning"

    # the global norm looks fine -- this is why no existing test catches it
    assert glob_bad < LEG73_FIELD_TOL, (
        f"characterization: global err {glob_bad:.2e} should sit inside leg 73's "
        f"{LEG73_FIELD_TOL:.0e}")
    assert glob_bad / glob_ok < 10.0, "and be within an order of magnitude of the good grid"

    # the local error at the singular corner does not
    assert near_bad > LEG73_FIELD_TOL, (
        f"the near-origin err {near_bad:.2e} must exceed leg 73's {LEG73_FIELD_TOL:.0e}")
    assert near_bad / near_ok > 50.0, (
        f"and must be a large multiple of the ascending grid's {near_ok:.2e}")

    print(f"[DEFECT] reversed interval: drho {g_bad.drho:+.5f}, global rel err {glob_bad:.3e} "
          f"({glob_bad / glob_ok:.2f}x good, INSIDE leg 73's {LEG73_FIELD_TOL:.0e}) but "
          f"{near_bad:.3e} at r<0.05 ({near_bad / near_ok:.0f}x good, "
          f"{near_bad / LEG73_FIELD_TOL:.1f}x OUTSIDE it) -- the global norm under-reports "
          f"the local damage by {(near_bad / glob_bad) / (near_ok / glob_ok):.0f}x")


def test_characterization_single_node_window_is_underdetermined():
    """DEFECT (leg 99, third). One node in the window makes the two-parameter fit rank-1;
    lstsq silently returns the minimum-norm solution instead of refusing. The value is not
    absurd, which is exactly what makes it dangerous."""
    grid = PolarGrid(n_r=200, n_beta=16, r_min=0.09, r_max=40.0)
    omega, _, _, _ = _manufactured(grid)
    _, _, phi = velocity_from_vorticity(omega, grid)

    mask = (grid.r > grid.r[2]) & (grid.r < 0.1)
    assert mask.sum() == 1, f"precondition: exactly one node in the window, got {mask.sum()}"

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        ux0 = u_x_at_origin(phi, grid)
    assert len(caught) == 0, "characterization: rank deficiency is not warned about"

    err = abs(ux0 - UX0_TRUTH)
    assert 1e-2 < err < 1.0, f"expected a plausible-but-wrong value, got {ux0:.4f}"
    assert err / LEG73_ORIGIN_TOL > 100.0, "well outside leg 73's origin tolerance"
    print(f"[DEFECT] single-node window: u_x(0) = {ux0:+.6f}, abs err {err:.3e}, "
          f"{err / LEG73_ORIGIN_TOL:.0f}x leg 73's origin tol, no rank warning")


# ======================================================================================
# ROBUSTNESS -- these pin behaviour that is already correct and must STAY correct.
# ======================================================================================

def test_well_posed_origin_read_is_the_control():
    """The same call on a grid that DOES resolve the origin: 84 nodes in the window and an
    error three orders of magnitude below the fabricated case. Without this control the
    characterization tests above would not be evidence of anything."""
    grid = PolarGrid(n_r=200, n_beta=16, r_min=1e-3, r_max=40.0)
    omega, _, _, _ = _manufactured(grid)
    _, _, phi = velocity_from_vorticity(omega, grid)
    n = int(((grid.r > grid.r[2]) & (grid.r < 0.1)).sum())
    ux0 = u_x_at_origin(phi, grid)
    err = abs(ux0 - UX0_TRUTH)
    assert n > 50, f"control grid must fill the fit window, got {n} nodes"
    assert err < 2e-2, f"control read must be accurate, abs err {err:.3e}"
    print(f"[ok] control: {n} nodes in window, u_x(0) = {ux0:+.6f}, abs err {err:.3e}")


def test_degenerate_radial_grids_go_nonfinite_not_plausible():
    """r_min = 0, a negative r_min, and a collapsed radial extent must NOT come back as a
    finite field. NaN reaching the output is an acceptable flag -- what would not be
    acceptable is a finite, plottable answer."""
    for name, (r_min, r_max) in (
        ("r_min=0 (log 0 = -inf)", (0.0, 10.0)),
        ("r_min<0 (log of a negative)", (-1.0, 10.0)),
        ("r_min==r_max (drho=0)", (1.0, 1.0)),
    ):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            grid = PolarGrid(n_r=64, n_beta=16, r_min=r_min, r_max=r_max)
            omega = np.ones((grid.n_r, grid.n_beta))
            u, v, phi = velocity_from_vorticity(omega, grid)
        bad = int((~np.isfinite(phi)).sum())
        assert bad == phi.size, (
            f"{name}: expected a fully non-finite field, only {bad}/{phi.size} flagged")
        assert not np.isfinite(u).any(), f"{name}: velocity must not come back finite"
        print(f"[ok] {name}: {bad}/{phi.size} non-finite in phi -- degeneracy visible")


def test_n_r_one_raises():
    """A single radial node has no spacing; the grid constructor must not invent one."""
    try:
        PolarGrid(n_r=1, n_beta=16, r_min=1.0, r_max=10.0)
    except IndexError:
        print("[ok] n_r=1 raises IndexError -- degeneracy flagged")
        return
    raise AssertionError("n_r=1 built a grid without raising")


def test_poisoned_vorticity_propagates_globally():
    """A single NaN or Inf anywhere in omega must contaminate the whole returned field --
    the angular transform and the tridiagonal sweep are both global, and a solver that
    swallowed the poison locally would be the dangerous outcome."""
    for name, value in (("NaN", np.nan), ("Inf", np.inf)):
        grid = PolarGrid(n_r=64, n_beta=16, r_min=1e-3, r_max=10.0)
        omega, _, _, _ = _manufactured(grid)
        omega = omega.copy()
        omega[10, 3] = value
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            u, v, phi = velocity_from_vorticity(omega, grid)
        bad = int((~np.isfinite(phi)).sum())
        assert bad == phi.size, (
            f"one {name} contaminated only {bad}/{phi.size} of phi -- poison was swallowed")
        print(f"[ok] one {name} in omega -> {bad}/{phi.size} non-finite in phi")


def test_malformed_inputs_raise():
    """Wrong-shaped vorticity and a mis-cased radial_bc must raise, not coerce."""
    grid = PolarGrid(n_r=64, n_beta=16, r_min=1e-3, r_max=10.0)
    omega, _, _, _ = _manufactured(grid)

    cases = (
        ("omega square on the wrong axis", lambda: velocity_from_vorticity(
            np.ones((grid.n_beta, grid.n_beta)), grid)),
        ("omega a single broadcastable row", lambda: velocity_from_vorticity(
            np.ones((1, grid.n_beta)), grid)),
        ("radial_bc case typo 'Robin'", lambda: velocity_from_vorticity(
            omega, grid, radial_bc="Robin")),
        ("dirichlet without phi_exact", lambda: velocity_from_vorticity(
            omega, grid, radial_bc="dirichlet")),
    )
    for name, call in cases:
        try:
            call()
        except Exception as exc:  # noqa: BLE001 -- the exception type IS the measurement
            print(f"[ok] {name} raises {type(exc).__name__}")
            continue
        raise AssertionError(f"{name} did not raise")


def test_empty_angular_basis_is_accepted_but_shape_degenerate():
    """n_beta <= 0 is accepted without complaint. That is a missing guard, but the returned
    field has a zero-length axis, so a consumer cannot mistake it for a real field. Pinned as
    the weak finding it is: if a future patch raises here instead, update this test."""
    for n_beta in (0, -3):
        grid = PolarGrid(n_r=32, n_beta=n_beta, r_min=1e-3, r_max=10.0)
        omega = np.zeros((grid.n_r, max(grid.n_beta, 0)))
        u, v, phi = velocity_from_vorticity(omega, grid)
        assert grid.n_modes.size == 0, f"n_beta={n_beta} built {grid.n_modes.size} modes"
        assert 0 in phi.shape, f"n_beta={n_beta} returned a non-degenerate shape {phi.shape}"
        print(f"[weak] n_beta={n_beta}: accepted silently, phi.shape={phi.shape}, "
              f"{grid.n_modes.size} angular modes")


if __name__ == "__main__":
    test_characterization_empty_fit_window_fabricates_zero()
    test_characterization_reversed_radial_interval_hides_local_damage()
    test_characterization_single_node_window_is_underdetermined()
    test_well_posed_origin_read_is_the_control()
    test_degenerate_radial_grids_go_nonfinite_not_plausible()
    test_n_r_one_raises()
    test_poisoned_vorticity_propagates_globally()
    test_malformed_inputs_raise()
    test_empty_angular_basis_is_accepted_but_shape_degenerate()
    print("\nALL BOUSSINESQ-VELOCITY ADVERSARIAL (LEG 99) TESTS PASSED")
    print("GATE: YES -- u_x_at_origin fabricates -0.0 on an empty fit window "
          "(truth -2.0, 100% error, no warning). ESCALATED, NOT PATCHED.")
