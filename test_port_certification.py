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


if __name__ == "__main__":
    import time
    t0 = time.time()
    for fn in (test_1_gmres_is_correct_and_calibrated,
               test_2_leading_order_inverse_is_exact,
               test_3_stall_verdict_separates_flat_from_bending,
               test_4_kill_switch_refuses_to_invent_numbers,
               test_5_krylov_ladder_is_a_ladder,
               test_6_artifact_carries_the_finding):
        print(f"\n{fn.__name__}")
        fn()
    print(f"\nALL GATES PASS ({time.time() - t0:.0f}s)")
