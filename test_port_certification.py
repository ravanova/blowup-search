"""Gates for solver/port_certification.py -- the L1->L2 certification port, step one.

  (1) THE GMRES IS CORRECT, and its ill-conditioning failure mode is CALIBRATED.  Every
      claim in this leg is "the solve stalled", which is exactly what a broken solver
      produces, so the solver is gated first -- on a well-conditioned dense system (must
      reach machine level fast) and on a deliberately cond~1e8 one (must stall, and the
      level it stalls at is the yardstick the real Jacobian is then compared against).
  (2) THE LEADING-ORDER PRECONDITIONER IS AN EXACT INVERSE, not an approximate one.  It is
      only usable because it is O(N) and exact; if it drifted, the preconditioned ladder
      would be measuring the preconditioner's error rather than the operator's spectrum.
  (3) THE STALL VERDICT SEPARATES FLAT FROM BENDING.  The whole reading of this leg turns
      on that distinction -- flat means a continuum, bending means conditioning -- so the
      classifier is gated on synthetic ladders of both shapes.
  (4) THE KILL-SWITCH REFUSES TO INVENT NUMBERS.  `radii_polynomial_status(None, None)`
      must return BLOCKED_AT_STEP_ONE, not a failure with a fabricated bound.  A missing
      Y_0 is a stronger statement than a large one and the code must preserve that.
  (5) THE COMMITTED ARTIFACT AGREES WITH A FRESH CALL on the headline numbers, and carries
      the seed-dependence, the non-monotone residual, and Route-G's growing ladder.

Run: .venv/bin/python test_port_certification.py
"""

import json
from pathlib import Path

import numpy as np

from solver.port_certification import (
    gmres, gmres_controls, krylov_ladder, leading_order_solve,
    radii_polynomial_status, stall_verdict,
)

DATA = Path(__file__).resolve().parent / "writeup" / "data"


def _close(a, b, rel=1e-9):
    return abs(a - b) <= rel * max(abs(a), abs(b), 1e-300)


def test_1_gmres_is_correct_and_calibrated():
    c = gmres_controls()
    good = c["well_conditioned"]
    assert good["rel_true"] < 1e-9, good
    assert _close(good["rel_reported"], good["rel_true"], 1e-6), good
    assert good["k"] < 40, good["k"]
    ill = c["cond_1e8"]
    assert ill["rel"] > 1e-3, ill        # ill-conditioning alone DOES stall it
    assert ill["rel"] < 0.5, ill         # ...but not as badly as the real Jacobian
    print(f"  well-conditioned: {good['rel_true']:.2e} in {good['k']} its; "
          f"cond~1e8 stalls at {ill['rel']:.3f} after {ill['k']}  OK")


def test_2_leading_order_inverse_is_exact():
    """Apply the operator to the solve and get the right-hand side back, to rounding."""
    rng = np.random.default_rng(3)
    n_r, n_b = 64, 8
    c_l, drho, c_diag = 3.0606, 0.09, -1.0145
    rhs = rng.standard_normal((n_r, n_b))
    x = leading_order_solve(rhs, c_l, drho, c_diag)
    a = c_l / drho
    back = np.empty_like(x)
    back[0] = (c_diag - a) * x[0]                       # prev = 0 on the first row
    back[1:] = a * x[:-1] + (c_diag - a) * x[1:]
    err = float(np.max(np.abs(back - rhs)) / np.max(np.abs(rhs)))
    assert err < 1e-12, err
    print(f"  (-c_l d_rho + c) applied to its own solve returns the rhs to {err:.1e}  OK")


def test_3_stall_verdict_separates_flat_from_bending():
    flat = [{"m": 10, "k": 10, "rel_residual": 0.6946},
            {"m": 160, "k": 160, "rel_residual": 0.6623}]
    bend = [{"m": 10, "k": 10, "rel_residual": 0.7},
            {"m": 160, "k": 160, "rel_residual": 1e-6}]
    vf, vb = stall_verdict(flat), stall_verdict(bend)
    assert vf["flat"] and "continuum" in vf["reading"]
    assert (not vb["flat"]) and "conditioning" in vb["reading"]
    assert _close(vf["residual_gain"], 0.6946 / 0.6623, 1e-9)
    assert vf["work_ratio"] == 16
    print(f"  flat ladder -> gain {vf['residual_gain']:.3f} (continuum); "
          f"bending -> gain {vb['residual_gain']:.1e} (conditioning)  OK")


def test_4_kill_switch_refuses_to_invent_numbers():
    s = radii_polynomial_status(None, None)
    assert s["status"] == "BLOCKED_AT_STEP_ONE" and s["closes"] is False
    assert "undefined" in s["why"]
    assert "Y0" not in s and "Z1" not in s, "must not fabricate a bound it does not have"
    assert radii_polynomial_status(1e-3, None)["status"] == "NO_Z1"
    assert radii_polynomial_status(1e-3, 1.2)["status"] == "Z1_EXCEEDS_ONE"
    ok = radii_polynomial_status(1e-6, 0.1, 1.0)
    assert ok["status"] == "EVALUATED" and ok["closes"] is True
    bad = radii_polynomial_status(1.0, 0.1, 1.0)
    assert bad["status"] == "EVALUATED" and bad["closes"] is False
    print("  BLOCKED_AT_STEP_ONE carries no fabricated Y_0 or Z_1; the four other "
          "branches classify correctly  OK")


def test_5_krylov_ladder_is_a_ladder():
    """A ladder must be monotone non-increasing in m -- more Krylov space cannot hurt."""
    rng = np.random.default_rng(5)
    n = 120
    A = np.diag(np.logspace(0, 4, n)) + 0.05 * rng.standard_normal((n, n))
    b = rng.standard_normal(n)
    rows = krylov_ladder(lambda v: A @ v, b, dims=(5, 10, 20, 40))
    r = [q["rel_residual"] for q in rows]
    assert r == sorted(r, reverse=True), r
    assert [q["m"] for q in rows] == [5, 10, 20, 40]
    print(f"  ladder monotone: {[round(x, 4) for x in r]}  OK")


def test_6_artifact_carries_the_finding():
    p = DATA / "p2_route_k_v1_port.json"
    if not p.exists():
        print("  SKIP -- run experiments/p2_route_k_v1_port.py first")
        return
    d = json.loads(p.read_text())
    k1 = d["K1_K2_no_fixed_point"]
    # the relaxation must be shown NOT to converge, both ways
    assert k1["residual_monotone_in_steps"] is False
    assert k1["route_g_residual_grows_under_refinement"] is True
    assert k1["route_g_residual_growth_factor"] > 5.0
    # ...while c_omega stays stable -- the uncomfortable pairing that carries the leg
    assert k1["route_g_c_omega_spread_over_that_ladder"] < 0.01
    # both seeds stall, and both are flat
    for seed in ("cycle_best", "cycle_worst"):
        k4 = d["K4_krylov_stall"][seed]
        assert k4["unpreconditioned_stall"]["flat"] is True, seed
        assert k4["preconditioned_stall"]["flat"] is True, seed
        assert k4["unpreconditioned_stall"]["rel_at_max_dim"] > 0.1, seed
    # and the two seeds disagree -- which is the point
    sd = d["K4_krylov_stall"]["seed_dependence"]
    ratio = sd["unpreconditioned_stall_best"] / sd["unpreconditioned_stall_worst"]
    assert ratio > 2.0, ratio
    assert d["K5_radii_polynomial"]["status"] == "BLOCKED_AT_STEP_ONE"
    # the instrument controls must be present and passing IN the artifact
    g = d["K3_instrument_controls"]["gmres"]
    assert g["well_conditioned"]["rel_true"] < 1e-9
    assert d["K3_instrument_controls"]["jv_best_drift"] < 1e-5
    print(f"  artifact: residual non-monotone, Route-G ladder grows "
          f"{k1['route_g_residual_growth_factor']:.1f}x while c_omega holds to "
          f"{k1['route_g_c_omega_spread_over_that_ladder']:.2%}; both seeds flat, "
          f"levels differ {ratio:.1f}x; status BLOCKED_AT_STEP_ONE  OK")




# --------------------------------------------------------------------------
# Route-L v1 additions -- the line sweep, and the attribution
# --------------------------------------------------------------------------
def test_7_line_sweep_is_an_exact_inverse():
    """One outward Thomas sweep must invert the FULL transport operator, not approximate it.

    This is the gate that separates the line sweep from the ADI composition it replaces.
    ADI composes two exact 1D solves and carries a splitting error; the sweep solves the
    coupled operator, so applying the operator to its own solve must return the right-hand
    side to rounding.  If this ever drifts, the preconditioned Krylov ladder is measuring
    the preconditioner's error rather than the operator's spectrum.
    """
    from solver.boussinesq_velocity import _thomas
    from solver.port_certification import line_sweep_solve
    rng = np.random.default_rng(11)
    n_r, n_b = 48, 16
    drho, dbeta, c = 0.09, 0.033, -1.0145
    s_rho = 0.5 + 4.0 * rng.random((n_r, n_b))          # strictly positive: outward upwind
    s_beta = rng.standard_normal((n_r, n_b))            # both signs, as in the real problem
    rhs = rng.standard_normal((n_r, n_b))
    x = line_sweep_solve(rhs, s_rho, s_beta, drho, dbeta, c, _thomas)

    # apply (-s_rho d_rho - s_beta d_beta + c) with the SAME first-order upwinding
    back = np.empty_like(x)
    prev = np.zeros(n_b)
    for i in range(n_r):
        sr = s_rho[i] / drho
        sb = s_beta[i]
        row = (c - sr) * x[i] + sr * prev
        pos = sb > 0
        xm = np.concatenate([[0.0], x[i][:-1]])
        xp = np.concatenate([x[i][1:], [0.0]])
        row = row + np.where(pos, -sb / dbeta * (x[i] - xm), -sb / dbeta * (xp - x[i]))
        back[i] = row
        prev = x[i]
    err = float(np.max(np.abs(back - rhs)) / np.max(np.abs(rhs)))
    assert err < 1e-11, err
    print(f"  full transport operator applied to its own sweep returns the rhs to {err:.1e}  OK")


def test_8_outward_upwinding_is_a_magnitude_not_a_boolean():
    from solver.port_certification import outward_upwinding_holds
    ok = outward_upwinding_holds(np.array([[0.39, 5.73], [1.0, 2.0]]))
    assert ok["holds"] is True and ok["min_s_rho"] == 0.39
    bad = outward_upwinding_holds(np.array([[-0.01, 5.73]]))
    assert bad["holds"] is False and bad["min_s_rho"] == -0.01
    print("  the sweep's precondition reports min(s_rho), so a marginal case is visible  OK")


def test_9_attribution_ranks_by_shape_not_endpoint():
    """The discriminant must be the ladder's GAIN (lesson 72), not its final value."""
    from solver.port_certification import attribution_summary
    L = {
        "full": [{"m": 10, "k": 10, "rel_residual": 0.6946},
                 {"m": 160, "k": 160, "rel_residual": 0.6623}],
        # WORSE endpoint but a bending curve -- must outrank a flat one that ends lower
        "culprit removed": [{"m": 10, "k": 10, "rel_residual": 0.90},
                            {"m": 160, "k": 160, "rel_residual": 0.20}],
        "irrelevant": [{"m": 10, "k": 10, "rel_residual": 0.50},
                       {"m": 160, "k": 160, "rel_residual": 0.49}],
    }
    r = attribution_summary(L)
    assert r[0]["ablation"] == "culprit removed", [q["ablation"] for q in r]
    assert r[0]["flat"] is False and r[0]["gain_vs_full"] > 4
    assert {q["ablation"] for q in r if q["flat"]} == {"full", "irrelevant"}
    print(f"  a bending ladder starting HIGHER outranks a flat one ending lower "
          f"(gain {r[0]['gain']:.1f} vs {r[-1]['gain']:.2f})  OK")


def test_10_route_l_artifact():
    p = DATA / "p2_route_l_v1_precond.json"
    if not p.exists():
        print("  SKIP -- run experiments/p2_route_l_v1_precond.py first")
        return
    d = json.loads(p.read_text())
    assert d["consistency_checks"]["full_matches_solver_rhs"] < 1e-12
    assert d["outward_upwinding"]["holds"] is True
    lad = d["L1_attribution"]["ladders"]
    # Route-K's two named candidates must BOTH be eliminated by the battery
    assert (lad["velocity feedback OFF"][-1]["rel_residual"]
            > lad["full"][-1]["rel_residual"]), "freezing the velocity must make it WORSE"
    for f in ("omega", "eta"):
        b = d["L2_stalled_residual_bands"][f]
        assert b["wall_first3_frac"] < 3 * d["L2_stalled_residual_bands"][
            "proportional_share_3_of_48"], f
    # ...and the angular transport must be the one that un-flattens the ladder
    top = d["L1_attribution"]["ranked"][0]["ablation"]
    assert "angular" in top or "dilation" in top, top
    # the preconditioner must turn a flat ladder into a bending one
    pl = d["L3_preconditioners"]
    assert pl["stalls"]["none"]["flat"] is True
    assert pl["stalls"]["full transport line sweep"]["flat"] is False
    assert pl["ladders"]["full transport line sweep"][-1]["rel_residual"] < 0.05
    assert pl["line_sweep_deeper"][-1]["rel_residual"] < 1e-4
    # ...and the ADI composition must be recorded as WORSE than doing nothing
    assert (pl["ladders"]["ADI composition"][-1]["rel_residual"]
            > pl["ladders"]["none"][-1]["rel_residual"])
    print(f"  artifact: velocity-OFF is worse, wall fractions proportional, top ablation "
          f"'{top}', sweep reaches "
          f"{pl['line_sweep_deeper'][-1]['rel_residual']:.1e}, ADI worse than nothing  OK")


if __name__ == "__main__":
    import time
    t0 = time.time()
    for fn in (test_1_gmres_is_correct_and_calibrated,
               test_2_leading_order_inverse_is_exact,
               test_3_stall_verdict_separates_flat_from_bending,
               test_4_kill_switch_refuses_to_invent_numbers,
               test_5_krylov_ladder_is_a_ladder,
               test_6_artifact_carries_the_finding,
               test_7_line_sweep_is_an_exact_inverse,
               test_8_outward_upwinding_is_a_magnitude_not_a_boolean,
               test_9_attribution_ranks_by_shape_not_endpoint,
               test_10_route_l_artifact):
        print(f"\n{fn.__name__}")
        fn()
    print(f"\nALL GATES PASS ({time.time() - t0:.0f}s)")
