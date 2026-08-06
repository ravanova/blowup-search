"""Leg 99 (Route-BVA) -- the ADVERSARIAL regression battery for
solver/boussinesq_velocity.py, banked alongside leg 73's known-answer gate in
test_boussinesq_velocity.py.

Leg 73 asked: is the answer RIGHT on a well-posed polar-grid problem? (Yes -- the Lamb
corner-image closed form to 1.76e-4 relative at observed order 2.00.)
This file asks the independent question: is a WRONG answer FLAGGED as wrong?

STATUS: PATCHED. These tests now assert the FIX, not the defect.
=================================================================
Leg 99's gate answered YES and ESCALATED without patching: the module DID silently return a
finite, plausible-looking wrong result on two reachable classes of degenerate input. A
bench-repair (Leg 0: ORCH) has since patched solver/boussinesq_velocity.py:

  1. u_x_at_origin now counts the origin fit window and checks the least-squares rank, and
     raises ValueError when the window holds fewer than 2 nodes or the fit is rank-deficient,
     instead of letting np.linalg.lstsq absorb an empty (0,2) design matrix into [0., 0.] and
     returning -0.0 against a truth of -2.0.
  2. PolarGrid.__init__ now requires r_min < r_max, instead of accepting a reversed interval
     that swaps which radial boundary condition applies at which end.

The three tests below, formerly marked CHARACTERIZATION, were flipped in that same commit
from pinning the defect to pinning the refusal. The measured magnitudes leg 99 recorded are
preserved in their docstrings so the finding is not erased by the fix; the assertions now
demand the exception. Do not "repair" a failure here by loosening them back.

Every other test in this file pins behaviour that was already CORRECT and must stay correct:
NaN propagates instead of being swallowed, malformed shapes raise, a degenerate radial
extent does not silently produce a finite field.

Leg 73's headline is UNAFFECTED by the patch: its grids put 258-398 nodes in the origin fit
window and are strictly ascending, and re-running its benchmark after the fix reproduced
writeup/data/p2_route_bv_v1_velocity_benchmark.json byte-for-byte (P1 finest 1.7584e-04 at
observed order 2.00).

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
# THE FIX -- these three were leg 99's CHARACTERIZATION tests, flipped to assert the patch.
# Each docstring keeps the magnitude leg 99 measured on the unpatched module. See the header.
# ======================================================================================

def test_empty_fit_window_raises_instead_of_fabricating_zero():
    """FIXED (leg 99 headline). u_x_at_origin fits c1(r) = phi_1(r)/r^2 over the window
    (grid.r[2], r_window). Leg 99 measured: with r_min above r_window the mask is empty,
    np.linalg.lstsq on a (0,2) design matrix returned [0.,0.] at rank 0 without raising or
    warning, and the function returned -0.0 -- a finite, physically plausible-looking value
    ("the origin strain vanishes") against a truth of -2.0, i.e. 100.0% relative error, 2000x
    leg 73's own 1e-3 origin tolerance, 0 warnings and 0 exceptions.

    The patched module counts the window first and refuses. The whole point is that the
    caller can no longer receive a number here -- there is no tolerance to loosen."""
    grid = PolarGrid(n_r=200, n_beta=16, r_min=0.15, r_max=40.0)  # r_min > r_window=0.1
    omega, _, _, _ = _manufactured(grid)
    _, _, phi = velocity_from_vorticity(omega, grid)

    mask = (grid.r > grid.r[2]) & (grid.r < 0.1)
    assert mask.sum() == 0, "precondition: the fit window must be empty for this case"

    try:
        ux0 = u_x_at_origin(phi, grid)
    except ValueError as exc:
        msg = str(exc)
        assert "0" in msg and "window" in msg, (
            f"the message must name the empty window and its occupancy, got {msg!r}")
        print(f"[fixed] empty fit window raises ValueError instead of returning "
              f"-0.0 (was 100.0% wrong, 2000x leg 73's origin tol): {msg[:88]}...")
        return
    raise AssertionError(
        f"REGRESSION: an empty origin fit window returned {ux0!r} instead of raising. "
        f"This is leg 99's headline defect returning -- truth is {UX0_TRUTH}.")


def test_reversed_radial_interval_is_refused_at_construction():
    """FIXED (leg 99, second). A reversed radial interval r_min > r_max used to build without
    complaint. The interior discretization survives (the Thomas solve sees only drho^2) but
    the two radial Dirichlet ends swap, so the far-field decay tail phi ~ r^{-2n} was imposed
    at the singular corner where the truth is phi ~ r^{+2n}. Leg 99 measured the GLOBAL
    relative error at 1.43e-4 -- only 2.00x the ascending grid and comfortably INSIDE leg 73's
    5e-3 acceptance, hence invisible to every existing test -- while the LOCAL error at r<0.05
    was 3.30e-2: 154x the ascending grid, 6.6x OUTSIDE leg 73's tolerance, with the global
    norm under-reporting the local damage by 77x.

    PolarGrid now refuses the interval, so no solve happens at all."""
    # the ascending control still builds and still solves accurately
    g_ok = PolarGrid(n_r=400, n_beta=16, r_min=1e-3, r_max=40.0)
    omega, phi_ex, _, _ = _manufactured(g_ok)
    _, _, phi_ok = velocity_from_vorticity(omega, g_ok)
    near = g_ok.r < 0.05
    glob_ok = _rel_linf(phi_ok, phi_ex)
    near_ok = _rel_linf(phi_ok[near], phi_ex[near])
    assert g_ok.drho > 0, "the control grid must be ascending"
    assert glob_ok < LEG73_FIELD_TOL and near_ok < LEG73_FIELD_TOL, (
        f"the control must stay inside leg 73's {LEG73_FIELD_TOL:.0e}: "
        f"global {glob_ok:.2e}, near-origin {near_ok:.2e}")

    for name, (r_min, r_max) in (
        ("reversed r_min > r_max", (40.0, 1e-3)),
        ("collapsed r_min == r_max", (1.0, 1.0)),
    ):
        try:
            g_bad = PolarGrid(n_r=400, n_beta=16, r_min=r_min, r_max=r_max)
        except ValueError as exc:
            assert "r_min" in str(exc) and "r_max" in str(exc), (
                f"{name}: the message must name both ends, got {str(exc)!r}")
            print(f"[fixed] {name} raises ValueError at construction "
                  f"(control: global {glob_ok:.2e}, near-origin {near_ok:.2e})")
            continue
        raise AssertionError(
            f"REGRESSION: {name} built a grid with drho={g_bad.drho:+.5f} instead of raising. "
            f"Leg 99 measured 3.30e-2 local error hidden behind a 1.43e-4 global norm.")


def test_single_node_window_is_refused_as_rank_deficient():
    """FIXED (leg 99, third). One node in the window makes the two-parameter fit rank-1; lstsq
    used to silently return the minimum-norm solution instead of refusing. Leg 99 measured
    u_x(0) = -1.783803 against a truth of -2, abs error 2.16e-1 -- 216x leg 73's 1e-3 origin
    tolerance and 25x the well-resolved 84-node read, with no rank warning. Not absurd, which
    is exactly what made it dangerous.

    The patched module refuses on the node count (1 < the 2-parameter minimum); the rank check
    behind it catches degenerate configurations that clear the count."""
    grid = PolarGrid(n_r=200, n_beta=16, r_min=0.09, r_max=40.0)
    omega, _, _, _ = _manufactured(grid)
    _, _, phi = velocity_from_vorticity(omega, grid)

    mask = (grid.r > grid.r[2]) & (grid.r < 0.1)
    assert mask.sum() == 1, f"precondition: exactly one node in the window, got {mask.sum()}"

    try:
        ux0 = u_x_at_origin(phi, grid)
    except ValueError as exc:
        print(f"[fixed] single-node window raises ValueError instead of returning "
              f"-1.783803 (216x leg 73's origin tol): {str(exc)[:88]}...")
        return
    raise AssertionError(
        f"REGRESSION: a rank-1 origin fit returned {ux0!r} instead of raising.")


def test_min_points_lever_lets_a_caller_demand_an_accuracy_margin():
    """The patch's default min_points=2 is the WELL-POSEDNESS floor, not an accuracy
    guarantee: leg 99 measured an 18-node window still landing 4.01e-3 off truth, 4.0x leg
    73's origin tolerance. A caller that needs a margin raises min_points, and a grid that
    cannot supply it is refused rather than quietly fitted."""
    grid = PolarGrid(n_r=200, n_beta=16, r_min=0.05, r_max=40.0)
    omega, _, _, _ = _manufactured(grid)
    _, _, phi = velocity_from_vorticity(omega, grid)
    n = int(((grid.r > grid.r[2]) & (grid.r < 0.1)).sum())
    assert 2 <= n < 50, f"this grid should be thin but well-posed, got {n} nodes"

    ux0 = u_x_at_origin(phi, grid)  # default min_points=2: allowed through
    assert np.isfinite(ux0), "a well-posed thin window must still return a value by default"

    try:
        u_x_at_origin(phi, grid, min_points=n + 1)
    except ValueError:
        print(f"[fixed] min_points lever: {n}-node window fitted by default "
              f"(u_x(0)={ux0:+.6f}, abs err {abs(ux0 - UX0_TRUTH):.2e}) but refused at "
              f"min_points={n + 1}")
        return
    raise AssertionError(f"min_points={n + 1} did not refuse a {n}-node window")


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
    """r_min = 0 and a negative r_min must NOT come back as a finite field. NaN reaching the
    output is an acceptable flag -- what would not be acceptable is a finite, plottable
    answer. Both clear the patched r_min < r_max check (0 < 10 and -1 < 10 are true) and are
    still caught downstream by log(0) = -inf and log(<0) = nan, exactly as leg 99 measured.

    The third case leg 99 grouped here, r_min == r_max, has MOVED: it is now refused at
    construction by the r_min < r_max guard, and is asserted in
    test_reversed_radial_interval_is_refused_at_construction. Raising is a strictly stronger
    flag than a non-finite field, so this is the fix improving on the measured behaviour, not
    a regression."""
    for name, (r_min, r_max) in (
        ("r_min=0 (log 0 = -inf)", (0.0, 10.0)),
        ("r_min<0 (log of a negative)", (-1.0, 10.0)),
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
    test_empty_fit_window_raises_instead_of_fabricating_zero()
    test_reversed_radial_interval_is_refused_at_construction()
    test_single_node_window_is_refused_as_rank_deficient()
    test_min_points_lever_lets_a_caller_demand_an_accuracy_margin()
    test_well_posed_origin_read_is_the_control()
    test_degenerate_radial_grids_go_nonfinite_not_plausible()
    test_n_r_one_raises()
    test_poisoned_vorticity_propagates_globally()
    test_malformed_inputs_raise()
    test_empty_angular_basis_is_accepted_but_shape_degenerate()
    print("\nALL BOUSSINESQ-VELOCITY ADVERSARIAL (LEG 99) TESTS PASSED")
    print("GATE: YES -- u_x_at_origin fabricated -0.0 on an empty fit window "
          "(truth -2.0, 100% error, no warning), and a reversed radial interval hid a "
          "3.30e-2 local error behind a 1.43e-4 global norm.")
    print("STATUS: PATCHED (Leg 0: ORCH). Both are now refused with a ValueError; leg 73's "
          "benchmark reproduces byte-for-byte (P1 1.7584e-04, order 2.00).")
