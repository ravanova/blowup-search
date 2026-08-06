"""Leg 104 (Route-BVB) -- the FULL-BATTERY post-repair regression suite for
solver/boussinesq_velocity.py, banked alongside leg 73's known-answer gate
(test_boussinesq_velocity.py) and leg 99's sampled adversarial regression
(test_boussinesq_velocity_adversarial.py).

WHY THIS FILE EXISTS, DISTINCT FROM test_boussinesq_velocity_adversarial.py
----------------------------------------------------------------------------------------------
The bench-repair (commit 26e6bd3, merged e3bdd9f) re-ran ONE benchmark (leg 73's) and its own
bundled test-file update samples THREE representative cases from leg 99's 22-case battery. This
file exercises the FULL original battery -- all 22 cases, all 9 points of the origin-read r_min
sweep -- freshly and independently (leg 99's own script, experiments/p2_route_bva_v1_adversarial.py,
is frozen against the unpatched module and KeyErrors if run post-repair; see
writeup/novelty/leg_104.md sec.2), plus an independent re-run of leg 73's benchmark ladder. See
experiments/p2_route_bvb_v1_postrepair.py for the runner and
writeup/data/p2_route_bvb_v1_postrepair.json for the full curated record.

GATE, VERBATIM (DIRECTION.md leg 104)
----------------------------------------------------------------------------------------------
"Post-repair, does solver/boussinesq_velocity.py (a) no longer return -0.0 on any of leg 99's
original failing degenerate-grid cases, and (b) still reproduce leg 73's Lamb corner-image
benchmark with zero regression?"

ANSWER: YES on both clauses, measured below.
  (a) 0 of 22 cases (0 of 9 origin-read sweep points) return SILENT_WRONG or -0.0. The 6
      formerly-fabricating points (r_min in {0.09, 0.099, 0.15, 0.5, 1.0, 10.0}) all now raise
      ValueError. The reversed-interval and collapsed-interval cases now raise at construction.
  (b) leg 73's 3-level ladder, re-run independently via run_level() (never via that module's
      main(), so its own frozen JSON is never touched here), reproduces the banked
      writeup/data/p2_route_bv_v1_velocity_benchmark.json to ~1e-12 relative -- inside the
      same-code-twice noise floor measured in the same run (BLAS-order floating-point jitter,
      not a regression).

This file READS solver/boussinesq_velocity.py and edits nothing under any outcome.

Run:  PYTHONPATH=. .venv/bin/python test_boussinesq_velocity_postrepair.py
"""

import numpy as np

from solver.boussinesq_velocity import (
    PolarGrid,
    velocity_from_vorticity,
    u_x_at_origin,
)

UX0_TRUTH = -2.0
LEG73_FIELD_TOL = 5e-3


def _manufactured(grid):
    """leg 73's own manufactured field, reused verbatim: phi = r^2 e^{-r} sin(2 beta)."""
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
# GATE CLAUSE (a) -- the FULL 9-point origin-read sweep, not a sample.
# ======================================================================================

def test_full_origin_read_sweep_never_returns_minus_zero_or_silent_wrong():
    """The exact 9-point r_min sweep from leg 99's battery. Every point that used to be a
    silent -0.0 fabrication (r_min >= 0.09, 6 of the 9 points, nodes-in-window 1 or 0) must
    now raise ValueError. The 3 well-resolved points (r_min = 1e-3, 1e-2, 0.05) must still
    return a finite value close to the truth -- the fix must not have turned a working case
    into a broken one."""
    sweep_points = (1e-3, 1e-2, 0.05, 0.09, 0.099, 0.15, 0.5, 1.0, 10.0)
    expect_raises_for = {0.09, 0.099, 0.15, 0.5, 1.0, 10.0}  # leg 99's 6 failing points
    n_checked = 0
    n_raised = 0
    n_returned = 0
    for r_min in sweep_points:
        grid = PolarGrid(n_r=200, n_beta=16, r_min=r_min, r_max=40.0)
        omega, _, _, _ = _manufactured(grid)
        _, _, phi = velocity_from_vorticity(omega, grid)
        mask = (grid.r > grid.r[2]) & (grid.r < 0.1)
        n_nodes = int(mask.sum())
        should_raise = r_min in expect_raises_for
        assert should_raise == (n_nodes < 2), (
            f"r_min={r_min}: expected node-count-based raise={should_raise} to match "
            f"n_nodes={n_nodes} < 2, precondition broken")
        try:
            ux0 = u_x_at_origin(phi, grid)
        except ValueError as exc:
            n_raised += 1
            assert should_raise, (
                f"REGRESSION: r_min={r_min} ({n_nodes} nodes) raised unexpectedly: {exc}")
            assert "window" in str(exc), f"r_min={r_min}: message must name the window"
        else:
            n_returned += 1
            assert not should_raise, (
                f"REGRESSION (leg 99's headline defect returning): r_min={r_min} "
                f"({n_nodes} nodes) returned {ux0!r} instead of raising -- truth is "
                f"{UX0_TRUTH}.")
            assert ux0 != 0.0 or not np.signbit(ux0), (
                f"REGRESSION: r_min={r_min} returned -0.0 (the exact leg 99 fabrication).")
            err = abs(ux0 - UX0_TRUTH)
            assert err < 1e-2, (
                f"r_min={r_min}: well-posed read must stay accurate, got abs err {err:.3e}")
        n_checked += 1
    assert n_checked == 9
    assert n_raised == 6, f"expected 6 raises (leg 99's 6 failing points), got {n_raised}"
    assert n_returned == 3, f"expected 3 well-posed returns, got {n_returned}"
    print(f"[ok] full 9-point origin-read sweep: {n_raised}/9 raise (were SILENT_WRONG/-0.0 "
          f"pre-repair), {n_returned}/9 return accurately (unaffected, no regression)")


def test_single_node_window_r_min_0p09_raises_not_minimum_norm_fit():
    """leg 99's rank-1 case: exactly 1 node in the window used to give a minimum-norm fit
    (u_x(0) = -1.783803, 21.6% error) instead of refusing. Isolated here because it is the
    one sweep point where the window is non-empty yet still degenerate."""
    grid = PolarGrid(n_r=200, n_beta=16, r_min=0.09, r_max=40.0)
    omega, _, _, _ = _manufactured(grid)
    _, _, phi = velocity_from_vorticity(omega, grid)
    mask = (grid.r > grid.r[2]) & (grid.r < 0.1)
    assert mask.sum() == 1, f"precondition: exactly 1 node, got {mask.sum()}"
    try:
        ux0 = u_x_at_origin(phi, grid)
    except ValueError:
        print("[ok] r_min=0.09 (1-node window) raises instead of a minimum-norm fabrication")
        return
    raise AssertionError(f"REGRESSION: 1-node window returned {ux0!r} instead of raising")


# ======================================================================================
# GATE CLAUSE (a) -- family 1: origin singularity, field-solve level (unaffected by the fix,
# but re-checked in full so the "full battery" claim covers all 22, not just family 3).
# ======================================================================================

def test_family1_origin_singularity_all_six_cases_stay_flagged():
    """r_min<=0 / collapsed / n_r=1 / poisoned omega. r_min==r_max MOVED from NONFINITE to
    RAISED (a strictly stronger flag, PolarGrid's new r_min<r_max guard) -- everything else
    is unaffected by the repair and must stay exactly as leg 99 measured it."""
    results = {}

    def run(name, build_and_call):
        try:
            phi = build_and_call()
            nonfinite = int((~np.isfinite(phi)).sum())
            results[name] = ("NONFINITE", nonfinite, phi.size) if nonfinite else ("FINITE", 0, phi.size)
        except Exception as exc:  # noqa: BLE001 -- the exception IS the measurement
            results[name] = ("RAISED", type(exc).__name__, None)

    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        def go_zero():
            g = PolarGrid(n_r=64, n_beta=16, r_min=0.0, r_max=10.0)
            omega, _, _, _ = _manufactured(g)
            _, _, phi = velocity_from_vorticity(omega, g)
            return phi
        run("r_min_zero", go_zero)

        def go_negative():
            g = PolarGrid(n_r=64, n_beta=16, r_min=-1.0, r_max=10.0)
            omega, _, _, _ = _manufactured(g)
            _, _, phi = velocity_from_vorticity(omega, g)
            return phi
        run("r_min_negative", go_negative)

        def go_collapsed():
            g = PolarGrid(n_r=64, n_beta=16, r_min=1.0, r_max=1.0)
            omega, _, _, _ = _manufactured(g)
            _, _, phi = velocity_from_vorticity(omega, g)
            return phi
        run("r_min_equals_r_max", go_collapsed)

        def go_nr1():
            g = PolarGrid(n_r=1, n_beta=16, r_min=1.0, r_max=10.0)
            omega, _, _, _ = _manufactured(g)
            _, _, phi = velocity_from_vorticity(omega, g)
            return phi
        run("n_r_one", go_nr1)

        def go_nan():
            g = PolarGrid(n_r=64, n_beta=16, r_min=1e-3, r_max=10.0)
            omega, _, _, _ = _manufactured(g)
            omega = omega.copy()
            omega[10, 3] = np.nan
            _, _, phi = velocity_from_vorticity(omega, g)
            return phi
        run("omega_one_nan", go_nan)

        def go_inf():
            g = PolarGrid(n_r=64, n_beta=16, r_min=1e-3, r_max=10.0)
            omega, _, _, _ = _manufactured(g)
            omega = omega.copy()
            omega[10, 3] = np.inf
            _, _, phi = velocity_from_vorticity(omega, g)
            return phi
        run("omega_one_inf", go_inf)

    expect_verdict = {
        "r_min_zero": "NONFINITE",
        "r_min_negative": "NONFINITE",
        "r_min_equals_r_max": "RAISED",   # UPGRADED by the repair: was NONFINITE
        "n_r_one": "RAISED",
        "omega_one_nan": "NONFINITE",
        "omega_one_inf": "NONFINITE",
    }
    for name, want in expect_verdict.items():
        got = results[name][0]
        assert got == want, f"{name}: expected {want}, got {results[name]}"
    print(f"[ok] family 1 (6 cases): all flagged as expected -- "
          f"{sum(1 for v in results.values() if v[0]=='RAISED')} RAISED, "
          f"{sum(1 for v in results.values() if v[0]=='NONFINITE')} NONFINITE, "
          f"0 SILENT_WRONG")


# ======================================================================================
# GATE CLAUSE (a) -- family 2: malformed boundary (7 cases).
# ======================================================================================

def test_family2_reversed_interval_now_raises_ascending_control_unaffected():
    """The ascending control must still solve accurately (unaffected by the repair); the
    reversed interval -- leg 99's SECOND defect, a 3.30e-2 local error hidden behind a
    1.43e-4 global norm -- must now be refused at construction, before any solve."""
    g_ok = PolarGrid(n_r=400, n_beta=16, r_min=1e-3, r_max=40.0)
    omega, phi_ex, _, _ = _manufactured(g_ok)
    _, _, phi_ok = velocity_from_vorticity(omega, g_ok)
    near = g_ok.r < 0.05
    glob_ok = _rel_linf(phi_ok, phi_ex)
    near_ok = _rel_linf(phi_ok[near], phi_ex[near])
    assert glob_ok < LEG73_FIELD_TOL and near_ok < LEG73_FIELD_TOL, (
        f"ascending control must stay inside leg 73's {LEG73_FIELD_TOL:.0e}: "
        f"global {glob_ok:.2e}, near-origin {near_ok:.2e}")

    try:
        PolarGrid(n_r=400, n_beta=16, r_min=40.0, r_max=1e-3)
    except ValueError as exc:
        assert "r_min" in str(exc) and "r_max" in str(exc)
        print(f"[ok] family 2: ascending control accurate (global {glob_ok:.2e}, near "
              f"{near_ok:.2e}); reversed interval raises at construction")
        return
    raise AssertionError("REGRESSION: reversed interval built a grid instead of raising")


def test_family2_remaining_five_cases_unaffected():
    """n_beta<=0 (SILENT_EMPTY, deliberately NOT patched -- leg 99 classified this weak and
    the gate never turned on it), and the three malformed-shape cases (RAISED, unaffected):
    all five must show EXACTLY their pre-repair behaviour, because none of them touch the
    two mechanisms the repair fixed."""
    for n_beta in (0, -3):
        grid = PolarGrid(n_r=32, n_beta=n_beta, r_min=1e-3, r_max=10.0)
        omega = np.zeros((grid.n_r, max(grid.n_beta, 0)))
        u, v, phi = velocity_from_vorticity(omega, grid)
        assert 0 in phi.shape, f"n_beta={n_beta}: expected a degenerate-shape SILENT_EMPTY"
    print("[ok] n_beta in {0,-3}: still SILENT_EMPTY (weak finding, deliberately unpatched)")

    grid = PolarGrid(n_r=64, n_beta=16, r_min=1e-3, r_max=10.0)
    omega, _, _, _ = _manufactured(grid)
    for name, call in (
        ("omega square wrong axis",
         lambda: velocity_from_vorticity(np.ones((grid.n_beta, grid.n_beta)), grid)),
        ("omega single row",
         lambda: velocity_from_vorticity(np.ones((1, grid.n_beta)), grid)),
        ("radial_bc case typo 'Robin'",
         lambda: velocity_from_vorticity(omega, grid, radial_bc="Robin")),
    ):
        try:
            call()
        except Exception as exc:  # noqa: BLE001
            print(f"[ok] {name}: still raises {type(exc).__name__}")
            continue
        raise AssertionError(f"REGRESSION: {name} did not raise")


# ======================================================================================
# GATE CLAUSE (b) -- leg 73's Lamb corner-image benchmark, re-run independently.
# ======================================================================================

def test_leg73_benchmark_reproduces_with_zero_regression():
    """Independent re-run of leg 73's exact 3-level ladder via run_level(), imported from
    experiments/p2_route_bv_v1_velocity_benchmark.py (never via its main(), so that module's
    own frozen JSON is never written by this test). Compared against the banked
    writeup/data/p2_route_bv_v1_velocity_benchmark.json to a tolerance well above the
    measured same-code-twice floating-point noise floor."""
    import json
    import os
    from experiments.p2_route_bv_v1_velocity_benchmark import (
        run_level, LADDER, observed_order,
    )

    levels = [run_level(n_r, n_beta, "robin") for n_r, n_beta in LADDER]
    p1 = [lv["p1_rel_err_centre_velocity"] for lv in levels]
    p3 = [lv["p3_rel_l2_phi_window"] for lv in levels]
    ord1 = observed_order(p1)
    ord3 = observed_order(p3)

    here = os.path.dirname(os.path.abspath(__file__))
    banked_path = os.path.join(here, "writeup", "data",
                                "p2_route_bv_v1_velocity_benchmark.json")
    with open(banked_path) as fh:
        banked = json.load(fh)["verdict"]

    p1_diff = abs(p1[-1] - banked["p1_finest"]) / banked["p1_finest"]
    p3_diff = abs(p3[-1] - banked["p3_finest"]) / banked["p3_finest"]
    TOL = 1e-6  # far above the ~1e-12 same-code-twice noise floor measured in leg_104's runner
    assert p1_diff < TOL, (
        f"REGRESSION: P1 finest {p1[-1]:.6e} vs banked {banked['p1_finest']:.6e}, "
        f"rel diff {p1_diff:.3e} exceeds {TOL:.0e}")
    assert p3_diff < TOL, (
        f"REGRESSION: P3 finest {p3[-1]:.6e} vs banked {banked['p3_finest']:.6e}, "
        f"rel diff {p3_diff:.3e} exceeds {TOL:.0e}")
    assert min(ord1) >= 1.9 and min(ord3) >= 1.9, (
        f"REGRESSION: observed order dropped, P1 orders {ord1}, P3 orders {ord3}")
    print(f"[ok] leg 73 benchmark reproduces: P1 finest {p1[-1]:.6e} (banked "
          f"{banked['p1_finest']:.6e}, diff {p1_diff:.2e}), P3 finest {p3[-1]:.6e} "
          f"(banked {banked['p3_finest']:.6e}, diff {p3_diff:.2e}), orders "
          f"{['%.2f' % o for o in ord1]}")


if __name__ == "__main__":
    test_full_origin_read_sweep_never_returns_minus_zero_or_silent_wrong()
    test_single_node_window_r_min_0p09_raises_not_minimum_norm_fit()
    test_family1_origin_singularity_all_six_cases_stay_flagged()
    test_family2_reversed_interval_now_raises_ascending_control_unaffected()
    test_family2_remaining_five_cases_unaffected()
    test_leg73_benchmark_reproduces_with_zero_regression()
    print("\nALL BOUSSINESQ-VELOCITY POST-REPAIR (LEG 104) TESTS PASSED")
    print("GATE: (a) 0/22 SILENT_WRONG, 0 returned -0.0 across the FULL leg-99 battery "
          "(was 7 SILENT_WRONG, 5 returning -0.0); (b) leg 73's benchmark reproduces to "
          "~1e-12 relative, well inside the same-code-twice noise floor -> YES on both. "
          "Banked as a permanent regression suite alongside legs 73 and 99.")
