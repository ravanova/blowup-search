"""Leg 205 (Route-BVR) -- the adversarial battery for solver/boussinesq_rescaled.py, banked.

READ THIS BEFORE CHANGING ANYTHING HERE.

This file is a CHARACTERIZATION test. It is written to pass against the module AS IT IS at leg
205's merge base -- including its two defects. It does NOT bless them. Every case that pins a
defect is named `..._is_currently_silent...` and carries the magnitude it fabricates, so no
reader can mistake a green run for a clean module.

WHEN THE MODULE IS PATCHED, THESE EXPECTATIONS MUST FLIP IN THE SAME COMMIT AS THE FIX:
  * test_defectA_empty_window_is_currently_silent          -> expect ValueError
  * test_defectA_single_node_window_is_currently_silent    -> expect ValueError
  * test_defectB_scale_blind_window_is_currently_silent    -> expect ValueError (or a
                                                              residual-gated refusal)
  * test_defectB_reaches_modulation_on_a_resolved_grid     -> expect ValueError
This instruction is the same one leg 99 attached to test_boussinesq_velocity_adversarial.py,
and leg 104 is the precedent for how the flip is done.

THE GATE THIS BATTERY ANSWERED (DIRECTION.md leg 205, verbatim):
"Under adversarial and degenerate inputs, does boussinesq_rescaled.py ever silently return a
wrong value rather than reject or visibly propagate the defect?"   ANSWER: YES, two mechanisms.

DEFECT A -- the second occurrence of leg 99's class, in the module leg 99 flagged.
  odd_field_x_slope (solver/boussinesq_rescaled.py:159-162) masks a fit window and hands the
  result to `coef, *_ = np.linalg.lstsq(A, d1[m], rcond=None)` with no occupancy and no rank
  check. An empty window yields a (0,3) design matrix, which lstsq absorbs into a zero
  coefficient without raising or warning: the function returns exactly 0.0 against a truth of
  2.0 -- 100% relative error, 2000x the module's own acceptance tolerance. This is verbatim the
  mechanism leg 99 measured in the sibling u_x_at_origin (-0.0 vs -2.0) and leg 104 confirmed
  repaired THERE ONLY; writeup/novelty/leg_99.md sec.4 note 2 flagged this exact line by number.

DEFECT B -- NEW, and NOT a variant of A.
  The fit window r_win=0.4 is a hard-coded ABSOLUTE length that never references the field's own
  radial scale, and the least-squares residual that would expose the resulting misfit is thrown
  away by the `*_` in the same line. So for a perfectly smooth, in-contract, odd-in-x field
  whose decay scale is well inside 0.4, the three-term basis (r, r^3, r^5) cannot represent d1
  over the window and the function returns a finite, plausible, wrong number ON A FULLY
  RESOLVED GRID -- 177 nodes in the window, no exception, no warning.
  Leg 99's guard provably cannot catch this: across the failing sweep the lstsq rank is 3 in
  every row and the condition number is CONSTANT at 5.537e2, while the discarded relative
  residual tracks the slope error across four orders of magnitude. Occupancy and rank are blind
  to B; only the residual sees it.
  B reaches the coupled entry point modulation() and corrupts c_l = 2 eta_x(0)/omega_x(0),
  because the module docstring's claimed cancellation ("the projection's quadrature bias
  CANCELS in the ratio (same basis both reads)") holds only when omega and eta share a radial
  scale -- which the Chen-Hou profile they target does not require.

WHAT THE BATTERY DID **NOT** FIND, banked so a later leg does not re-derive it:
  * The rank-deficient-but-nonempty window is NOT a live defect at modulation(): the sibling
    guard's window (r<0.1, 2 params) is a strict subset of this one (r<0.4, 3 params), so an
    empty window here always trips u_x_at_origin first, and the surviving rank-deficient gap is
    bounded at 1.90e-6 relative on c_l -- 0.0038x the module's own tolerance, over 80 scored
    pairs each of which passed its own resolved control.
  * NaN/Inf placed anywhere in omega, eta or xi propagate VISIBLY into the returned RHS arrays.
    Nothing is swallowed.
  * There is no dealiasing mask and no spectral truncation anywhere in this module, so the
    legs 129/188 mask class has no site here. The angular DST-I is an exact bijection on grid
    fields (round-trip relative error ~1e-16).

Full battery + every case: experiments/p2_route_bvr_v1_adversarial.py ->
writeup/data/p2_route_bvr_v1_adversarial.json.

solver/boussinesq_rescaled.py is READ ONLY to leg 205 and is byte-identical to its merge-base
state. This leg did not patch either defect; both are escalated and parked.
"""

import numpy as np

from solver.boussinesq_velocity import PolarGrid, velocity_from_vorticity
from solver.boussinesq_rescaled import (
    odd_field_x_slope, modulation, transport, grad_xy, advection_speeds,
    RescaledBoussinesq,
)

# The module's own acceptance tolerance for the origin read, read off its only correctness gate
# (test_boussinesq_rescaled.py::test_odd_field_x_slope). Anything inside this would not be
# caught by the module's existing tests.
ACCEPT_REL = 5.0e-4


def approx(got, want, rel):
    """assert-friendly relative comparison (no pytest in this repo's test convention)."""
    return abs(got - want) <= rel * abs(want)


def raises(exc, fn, *a, **kw):
    """Return the exception repr if fn raises `exc`, else raise AssertionError."""
    try:
        fn(*a, **kw)
    except exc as e:
        return f"{type(e).__name__}: {e}"
    except Exception as e:                                        # noqa: BLE001
        raise AssertionError(f"expected {exc.__name__}, got {type(e).__name__}: {e}")
    raise AssertionError(f"expected {exc.__name__}, nothing was raised")


def odd_field(grid, a=1.0, lam=1.0):
    """a * x * exp(-lam r^2). Odd in x; g_x(0) = a EXACTLY (the envelope is flat at r=0)."""
    return a * grid.R * np.cos(grid.B) * np.exp(-lam * grid.R ** 2)


def window_nodes(grid, r_win=0.4, i_lo=3):
    return int(((np.arange(grid.n_r) >= i_lo) & (grid.r < r_win)).sum())


# =======================================================================================
# Positive controls first. If these ever fail, the battery below is measuring nothing.
# =======================================================================================

def test_control_well_posed_read_is_accurate_and_moves_with_the_truth():
    """Lesson 90: a control that cannot come out differently is not a control. This one tracks
    four different truths, so it can report the other answer."""
    grid = PolarGrid(n_r=400, n_beta=16, r_min=1e-4, r_max=1e4)
    assert window_nodes(grid) == 177
    for a in (0.5, 1.0, 2.0, -3.0):
        got = odd_field_x_slope(odd_field(grid, a=a, lam=1.0), grid)
        rel = abs(got - a) / abs(a)
        assert rel < ACCEPT_REL, f"well-posed read broke: a={a} got={got} rel={rel:.3e}"


def test_control_odd_field_x_slope_converges_on_well_posed_input():
    grid_c = PolarGrid(n_r=100, n_beta=32, r_min=1e-4, r_max=1e4)
    grid_f = PolarGrid(n_r=800, n_beta=32, r_min=1e-4, r_max=1e4)
    e_c = abs(odd_field_x_slope(odd_field(grid_c, a=2.0), grid_c) - 2.0)
    e_f = abs(odd_field_x_slope(odd_field(grid_f, a=2.0), grid_f) - 2.0)
    assert e_c < 1e-2 and e_f < 1e-2, (e_c, e_f)


# =======================================================================================
# DEFECT A -- window occupancy. Leg 99's class, second occurrence.
# =======================================================================================

def test_defectA_empty_window_is_currently_silent():
    """FLIP TO `raises(ValueError, ...)` WHEN THE MODULE IS PATCHED.

    Empty fit window -> lstsq on a (0,3) design matrix -> exactly 0.0, no raise, no warning.
    Truth 2.0. 100% relative error = 2000x the module's own acceptance tolerance."""
    for n_r, r_min, r_max in [(8, 1e-2, 1e2), (200, 0.5, 40.0), (200, 1.0, 1e3)]:
        grid = PolarGrid(n_r=n_r, n_beta=16, r_min=r_min, r_max=r_max)
        assert window_nodes(grid) == 0, "grid no longer degenerate; battery would be vacuous"
        field = odd_field(grid, a=2.0, lam=1.0)   # built outside errstate: the far-field
        # Gaussian tail underflows harmlessly at r_max, which is not the defect under test.
        with np.errstate(divide="raise", invalid="raise", over="raise"):
            got = odd_field_x_slope(field, grid)
        assert got == 0.0, f"fabrication changed: got {got!r} (expected exactly 0.0)"
        assert approx(abs(got - 2.0) / 2.0, 1.0, 1e-12), "no longer 100% wrong"
        assert np.isfinite(got), "a NaN here would at least be visible; 0.0 is not"


def test_defectA_empty_window_is_reachable_through_the_public_r_win_argument():
    """Same fabrication on the leg-73-class 400-node grid, via the r_win knob alone."""
    grid = PolarGrid(n_r=400, n_beta=16, r_min=1e-4, r_max=1e4)
    got = odd_field_x_slope(odd_field(grid, a=2.0, lam=1.0), grid, r_win=1e-4)
    assert window_nodes(grid, r_win=1e-4) == 0
    assert got == 0.0, f"expected the fabricated 0.0, got {got!r}"


def test_defectA_single_node_window_is_currently_silent():
    """FLIP WHEN PATCHED. One node against three parameters -> lstsq minimum-norm solution,
    returned as if it were the fit. 1.906 vs truth 2.0: 4.69e-2 relative, 93.9x tolerance."""
    grid = PolarGrid(n_r=10, n_beta=16, r_min=1e-2, r_max=1e2)
    assert window_nodes(grid) == 1
    got = odd_field_x_slope(odd_field(grid, a=2.0, lam=1.0), grid)
    rel = abs(got - 2.0) / 2.0
    assert np.isfinite(got) and got != 0.0
    assert approx(rel, 4.693582843e-2, 1e-6), f"magnitude moved: {rel:.6e}"
    assert rel / ACCEPT_REL > 90.0


def test_defectA_empty_window_always_trips_the_sibling_guard_at_modulation():
    """The BANKED NEGATIVE: an empty window here is never reachable through modulation(),
    because u_x_at_origin's window (r<0.1) is a strict subset of this one (r<0.4) and leg 99's
    guard fires first. This is why defect A is a public-API defect, not a c_l defect."""
    grid = PolarGrid(n_r=8, n_beta=16, r_min=1e-2, r_max=1e2)
    om, et = odd_field(grid, a=1.0, lam=1.0), odd_field(grid, a=0.7, lam=4.0)
    _, _, phi = velocity_from_vorticity(om, grid)
    msg = raises(ValueError, modulation, om, et, phi, grid)
    assert "u_x_at_origin" in msg, msg


def test_defectA_surviving_rank_deficient_gap_is_bounded():
    """The other banked negative, with its magnitude. Where the sibling guard passes but this
    module's 3-parameter fit is still rank-deficient (2 nodes), both nodes necessarily lie at
    r < 0.1, and the c_l error stays at 1.90e-6 -- 0.0038x the module's own tolerance."""
    grid = PolarGrid(n_r=8, n_beta=32, r_min=0.00016000000000000102,
                     r_max=12.499999999999893)
    assert window_nodes(grid) == 2
    om, et = odd_field(grid, a=1.0, lam=1.0), odd_field(grid, a=0.7, lam=0.25)
    _, _, phi = velocity_from_vorticity(om, grid)
    c_l = modulation(om, et, phi, grid)[0]
    rel = abs(c_l - 1.4) / 1.4
    assert rel < 10 * ACCEPT_REL, f"the bounded gap grew: {rel:.3e}"


# =======================================================================================
# DEFECT B -- the scale-blind window and the discarded residual. NEW at leg 205.
# =======================================================================================

DEFECT_B_SCALES = [
    # (lam, expected relative error) on the n_beta=16 leg-73-class grid. lam=1 is the ONLY
    # scale the module's own correctness gate ever tests, and it is inside tolerance.
    (0.25, 4.9923e-4),
    (1.0, 4.6977e-4),
    (4.0, 1.0766e-3),
    (25.0, 1.16125e-1),
    (100.0, 5.5661e-1),
    (400.0, 8.65349e-1),
]


def test_defectB_scale_blind_window_is_currently_silent():
    """FLIP WHEN PATCHED (for every row but lam=1).

    A FULLY RESOLVED grid -- 177 nodes in the fit window in every row -- and a perfectly smooth,
    in-contract, odd-in-x field. The only thing that changes is the field's radial scale
    1/sqrt(lam) relative to the hard-coded r_win=0.4. The read degrades to 0.269 against a truth
    of 2.0 without raising or warning."""
    grid = PolarGrid(n_r=400, n_beta=16, r_min=1e-4, r_max=1e4)
    assert window_nodes(grid) == 177, "window is full; occupancy cannot explain this"
    for lam, expected_rel in DEFECT_B_SCALES:
        got = odd_field_x_slope(odd_field(grid, a=2.0, lam=lam), grid)
        rel = abs(got - 2.0) / 2.0
        assert np.isfinite(got), "the defect is that it is finite and plausible"
        assert approx(rel, expected_rel, 1e-3), f"lam={lam}: magnitude moved: {rel:.6e}"
        tag = "[silent]" if rel > ACCEPT_REL else "[ok]    "
        print(f"{tag} lam={lam:6g} scale={1/np.sqrt(lam):.3g} returned={got:+.6f} "
              f"truth=2.0 rel_err={rel:.4e} = {rel/ACCEPT_REL:.1f}x the module's tolerance")


def test_defectB_rank_and_conditioning_are_blind_to_it():
    """The reason defect B is NOT defect A: leg 99's occupancy+rank guard cannot see it.
    Across the whole failing sweep the lstsq rank is 3 and the condition number is CONSTANT,
    while the discarded relative residual tracks the slope error over four decades."""
    grid = PolarGrid(n_r=400, n_beta=16, r_min=1e-4, r_max=1e4)
    beta = grid.beta
    dbeta = beta[1] - beta[0]
    cb = np.cos(beta)
    m = (np.arange(grid.n_r) >= 3) & (grid.r < 0.4)
    rr = grid.r[m]
    A = np.vstack([rr, rr ** 3, rr ** 5]).T
    ranks, conds, resids, errs = [], [], [], []
    for lam in (1.0, 4.0, 25.0, 100.0, 400.0):
        g = odd_field(grid, a=2.0, lam=lam)
        integrand = g * cb[None, :]
        g_wall = 2 * g[:, 0] - g[:, 1]
        d1 = (4.0 / np.pi) * (np.trapezoid(integrand, beta, axis=1)
                              + 0.5 * dbeta * (g_wall + integrand[:, 0])
                              + 0.5 * dbeta * integrand[:, -1])
        coef, res, rank, sv = np.linalg.lstsq(A, d1[m], rcond=None)
        ranks.append(int(rank))
        conds.append(float(sv[0] / sv[-1]))
        resids.append(float(np.sqrt(res[0])) / float(np.linalg.norm(d1[m])))
        errs.append(abs(float(coef[0]) - 2.0) / 2.0)
    assert ranks == [3, 3, 3, 3, 3], f"rank is not blind after all: {ranks}"
    assert max(conds) - min(conds) < 1e-6 * max(conds), f"cond varied: {conds}"
    assert approx(conds[0], 5.537e2, 1e-3), conds[0]
    # the discarded signal, in contrast, spans four decades alongside the error
    assert resids[0] < 1e-3 and resids[-1] > 0.5, resids
    assert errs[0] < 1e-3 and errs[-1] > 0.8, errs
    assert resids[-1] / resids[0] > 1e3 and errs[-1] / errs[0] > 1e3, (resids, errs)
    assert all(resids[i] < resids[i + 1] for i in range(len(resids) - 1)), resids


DEFECT_B_MODULATION = [
    (4.0, 1.5457e-3),
    (25.0, 1.1654e-1),
    (100.0, 5.5682e-1),
    (400.0, 8.6541e-1),
]


def test_defectB_reaches_modulation_on_a_resolved_grid():
    """FLIP WHEN PATCHED. Defect B is not confined to the standalone reduction: it corrupts
    c_l = 2 eta_x(0)/omega_x(0) at the coupled entry point, on a fully resolved grid, with no
    exception and no warning. The module docstring claims the quadrature bias cancels in this
    ratio; it does so only when omega and eta share a radial scale, and here they do not."""
    grid = PolarGrid(n_r=400, n_beta=32, r_min=1e-4, r_max=1e4)
    om = odd_field(grid, a=1.0, lam=1.0)
    _, _, phi = velocity_from_vorticity(om, grid)
    for lam_eta, expected_rel in DEFECT_B_MODULATION:
        et = odd_field(grid, a=0.7, lam=lam_eta)
        c_l = modulation(om, et, phi, grid)[0]
        rel = abs(c_l - 1.4) / 1.4
        assert np.isfinite(c_l)
        assert approx(rel, expected_rel, 1e-3), f"lam={lam_eta}: moved: {rel:.6e}"
        print(f"[silent] eta scale {1/np.sqrt(lam_eta):.3g} vs r_win 0.4: c_l={c_l:+.6f} "
              f"truth=1.4 rel_err={rel:.4e} = {rel/ACCEPT_REL:.1f}x tolerance")


def test_defectB_recovers_completely_when_the_window_matches_the_field():
    """The sharpest form of defect B, and its fix direction stated as a measurement.

    Same field, same grid, same code -- ONLY r_win varies. The read climbs from 0.269 (86.5%
    wrong) to 2.0009 (inside the module's own tolerance) as the window comes down to the
    field's own scale 0.05. So odd_field_x_slope is fully CAPABLE of the right answer here;
    what it lacks is any means of noticing that its hard-coded default window is the wrong
    size for the field, and any means of telling the caller. Lesson 90: this control can come
    out the other way, and does."""
    grid = PolarGrid(n_r=400, n_beta=16, r_min=1e-4, r_max=1e4)
    field = odd_field(grid, a=2.0, lam=400.0)        # field radial scale 1/sqrt(400) = 0.05
    got = {rw: odd_field_x_slope(field, grid, r_win=rw)
           for rw in (0.4, 0.1, 0.02, 0.005)}
    assert approx(got[0.4], 0.269302, 1e-4), got[0.4]
    assert approx(got[0.1], 1.766702, 1e-4), got[0.1]
    assert abs(got[0.02] - 2.0) / 2.0 < ACCEPT_REL, got[0.02]
    assert abs(got[0.005] - 2.0) / 2.0 < ACCEPT_REL, got[0.005]
    # monotone recovery, and the window count stays healthy throughout -- so occupancy is not
    # what is changing. 112 and 82 nodes respectively at the two windows that read correctly.
    assert window_nodes(grid, r_win=0.02) == 112
    assert window_nodes(grid, r_win=0.005) == 82
    print(f"[recovery] r_win 0.4 -> {got[0.4]:.6f} (86.5% wrong); r_win 0.02 -> "
          f"{got[0.02]:.6f} (inside tolerance). Same field, same grid, same code.")


def test_defectB_the_modules_own_gate_sits_exactly_at_the_one_safe_scale():
    """Why this survived to leg 205: test_boussinesq_rescaled.py::test_odd_field_x_slope uses
    exp(-r^2), i.e. lam=1 -- the single scale at which the read is accurate -- with a 3e-2
    tolerance. At lam=1 the error is 3.9e-5; one factor of 20 in scale takes it past 0.86."""
    grid = PolarGrid(n_r=400, n_beta=16, r_min=1e-4, r_max=1e4)
    e1 = abs(odd_field_x_slope(odd_field(grid, a=2.0, lam=1.0), grid) - 2.0) / 2.0
    e2 = abs(odd_field_x_slope(odd_field(grid, a=2.0, lam=400.0), grid) - 2.0) / 2.0
    assert e1 < 3e-2, "the module's own gate would have caught lam=1"
    assert e2 > 3e-2, "the module's own gate WOULD have caught lam=400 -- it never runs it"
    assert e2 / e1 > 1e3, f"e1={e1:.4e} e2={e2:.4e} ratio={e2/e1:.1f}"
    print(f"[silent] the module's own gate scale lam=1 reads {e1:.4e}; lam=400 reads "
          f"{e2:.4e} -- {e2/e1:.0f}x worse, and never tested")


# =======================================================================================
# NEGATIVE FAMILIES -- banked so a later leg does not re-derive them.
# =======================================================================================

NONFINITE_PLANTS = [
    ("omega", 0.05, np.nan), ("omega", 10.0, np.nan), ("omega", 10.0, np.inf),
    ("eta", 0.05, np.nan), ("eta", 10.0, np.nan), ("xi", 10.0, np.nan),
]


def test_nonfinite_inputs_propagate_visibly():
    """Nothing is swallowed: a planted NaN/Inf always reaches the returned RHS arrays."""
    grid = PolarGrid(n_r=200, n_beta=16, r_min=1e-3, r_max=1e3)
    for field, idx_r, bad in NONFINITE_PLANTS:
        idx = int(np.argmax(grid.r > idx_r))
        om = odd_field(grid, a=1.0, lam=1.0)
        et = odd_field(grid, a=0.7, lam=4.0)
        xi = 0.3 * odd_field(grid, a=1.0, lam=4.0)
        {"omega": om, "eta": et, "xi": xi}[field][idx, 0] = bad
        R_om, R_et, R_xi, _info = RescaledBoussinesq(grid).rhs(om, et, xi)
        n_bad = sum(int(np.count_nonzero(~np.isfinite(A))) for A in (R_om, R_et, R_xi))
        assert n_bad > 0, f"{bad!r} in {field} at r={idx_r} VANISHED -- a silent defect"


def test_no_dealiasing_mask_exists_in_this_module():
    """The legs 129/188 mask class has no site here. This control CAN report the other answer:
    a truncating mask would show up as a finite round-trip loss."""
    grid = PolarGrid(n_r=64, n_beta=16, r_min=1e-3, r_max=1e3)
    rng = np.random.default_rng(0)
    f = rng.standard_normal((grid.n_r, grid.n_beta))
    rel = np.max(np.abs(grid.from_modes(grid.to_modes(f)) - f)) / np.max(np.abs(f))
    assert rel < 1e-12, f"angular transform is lossy: {rel:.3e}"
    n_top = grid.n_modes[-1]
    f_top = np.sin(2.0 * n_top * grid.B) * np.exp(-grid.R ** 2)
    rel_top = np.max(np.abs(grid.from_modes(grid.to_modes(f_top)) - f_top)) / np.max(np.abs(f_top))
    assert rel_top < 1e-12, "the highest representable mode is annihilated"


def test_zero_and_degenerate_fields_are_rejected_or_correct():
    grid = PolarGrid(n_r=200, n_beta=16, r_min=1e-3, r_max=1e3)
    z = np.zeros((grid.n_r, grid.n_beta))
    _, _, phi = velocity_from_vorticity(odd_field(grid, a=1.0), grid)
    assert odd_field_x_slope(z, grid) == 0.0        # correct: the zero field has zero slope
    raises(ZeroDivisionError, modulation, z, z, phi, grid)   # c_l = 0/0 raises, not fabricates
    raises(ZeroDivisionError, modulation, z, odd_field(grid, a=0.7), phi, grid)


def test_known_answer_controls_on_the_untouched_kernels():
    """grad_xy and advection_speeds are not implicated; pinned so the escalation stays scoped."""
    grid = PolarGrid(n_r=400, n_beta=32, r_min=1e-3, r_max=1e2)
    f_x, f_y = grad_xy(grid.X, grid)                 # f = x  ->  f_x = 1, f_y = 0
    m = (grid.R > 1e-2) & (grid.R < 10.0)
    # 2nd-order central FD on a stretched grid: 7.52e-4 / 2.58e-4 over the interior band.
    assert np.max(np.abs(f_x[m] - 1.0)) < 1e-3, np.max(np.abs(f_x[m] - 1.0))
    assert np.max(np.abs(f_y[m])) < 1e-3, np.max(np.abs(f_y[m]))
    z = np.zeros_like(grid.R)
    s_rho, s_beta = advection_speeds(z, z, grid, 3.0)
    assert np.max(np.abs(s_rho - 3.0)) == 0.0 and np.max(np.abs(s_beta)) == 0.0


def test_transport_on_a_collapsed_angular_axis_is_visibly_empty_not_wrong():
    grid = PolarGrid(n_r=200, n_beta=0, r_min=1e-3, r_max=1e3)
    f = np.zeros((grid.n_r, 0))
    raises(IndexError, transport, f, f, f, grid, 3.0)   # beta[1] does not exist -- visible


if __name__ == "__main__":
    test_control_well_posed_read_is_accurate_and_moves_with_the_truth()
    test_control_odd_field_x_slope_converges_on_well_posed_input()
    test_defectA_empty_window_is_currently_silent()
    test_defectA_empty_window_is_reachable_through_the_public_r_win_argument()
    test_defectA_single_node_window_is_currently_silent()
    test_defectA_empty_window_always_trips_the_sibling_guard_at_modulation()
    test_defectA_surviving_rank_deficient_gap_is_bounded()
    test_defectB_scale_blind_window_is_currently_silent()
    test_defectB_rank_and_conditioning_are_blind_to_it()
    test_defectB_reaches_modulation_on_a_resolved_grid()
    test_defectB_recovers_completely_when_the_window_matches_the_field()
    test_defectB_the_modules_own_gate_sits_exactly_at_the_one_safe_scale()
    test_nonfinite_inputs_propagate_visibly()
    test_no_dealiasing_mask_exists_in_this_module()
    test_zero_and_degenerate_fields_are_rejected_or_correct()
    test_known_answer_controls_on_the_untouched_kernels()
    test_transport_on_a_collapsed_angular_axis_is_visibly_empty_not_wrong()
    print("\nALL BOUSSINESQ-RESCALED ADVERSARIAL (LEG 205) TESTS PASSED")
    print("GATE: YES -- two silent mechanisms in odd_field_x_slope, neither patched here.")
    print("  A (leg 99's class, 2nd occurrence): empty fit window -> exactly 0.0 vs truth 2.0, "
          "100% error, 2000x the module's own tolerance; 1 node -> 4.69e-2, 93.9x.")
    print("  B (NEW): scale-blind r_win=0.4 + discarded lstsq residual -> 0.269 vs truth 2.0 "
          "(86.5% error, 1731x tolerance) on a FULLY RESOLVED grid, and c_l off by the same "
          "86.5% through modulation(). rank=3 and cond=5.537e2 throughout, so leg 99's "
          "occupancy+rank guard is provably blind to B.")
    print("STATUS: PARKED, both escalated. solver/boussinesq_rescaled.py byte-unchanged.")
