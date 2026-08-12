"""Tests solver/dssp_screen.py -- Route-DSSP brick B7 (DSSP-SCREEN).

Run: .venv/bin/python test_dssp_screen.py
"""
import numpy as np

from solver.dssp_biot_savart import field_uB
from solver.dssp_screen import (
    axisymmetry_residual,
    fitted_far_field_decay_exponent,
    l3_norm_ladder,
    ledger_chae_tsai,
    ledger_nrs_tsai,
    ledger_pineau_vicol,
    lambda_from_trajectory,
    machine_read_ledger,
    screen_candidate,
)


def test_l3_norm_diverges_on_type_i_witness():
    """leg 351's witness decays like C/|x| (Type-I), so |V|^3 ~ 1/|x|^3 and
    the R^3-volume integral ~ Int (1/r) dr diverges logarithmically. The
    ladder must NOT report convergence, and successive shells must NOT
    shrink toward zero (a genuine log-divergence signature, not just slow
    convergence)."""
    l3 = l3_norm_ladder(field_uB, R_hi_ladder=(10.0, 100.0, 1e3, 1e4, 1e5, 1e6),
                         n_r=200, n_c=32, n_phi=16)
    assert not l3["converged"], "Type-I witness's L3 ladder unexpectedly converged"
    shells = [row["shell_integral_cube"] for row in l3["ladder"][-3:]]
    # a convergent integrand's shell contributions shrink toward 0; a
    # logarithmic divergence's shell contributions stay roughly CONSTANT
    # per decade -- check they do NOT shrink by more than a factor of 2
    assert min(shells) / max(shells) > 0.5, f"shells shrinking, not log-divergent: {shells}"
    print(f"[ok] L3 ladder diverges (rel_change_last_step={l3['rel_change_last_step']:.3e}, "
          f"shells stay ~constant: {shells})")


def test_fitted_decay_exponent_matches_type_i_envelope():
    """u_B ~ C/|x| by construction (solver/dssp_biot_savart.py's own
    docstring: a(r)*r -> -1 as r -> infinity), so the fitted exponent
    should land near -1, not near leg 332's -3 (a different, Gaussian-
    vorticity witness)."""
    d = fitted_far_field_decay_exponent(field_uB)
    assert abs(d["fitted_exponent"] - (-1.0)) < 0.05, \
        f"expected decay exponent near -1, got {d['fitted_exponent']!r}"
    print(f"[ok] fitted decay exponent = {d['fitted_exponent']:.6f} (Type-I, ~-1)")


def test_axisymmetry_residual_near_zero_on_swirl_witness():
    """leg 351's u_B is built from a pure swirl ansatz A=a(r)(x2,-x1,0); its
    cylindrical components must be phi-independent to near machine
    precision."""
    ax = axisymmetry_residual(field_uB)
    assert ax["max_rel_residual_over_phi"] < 1e-10, \
        f"axisymmetric witness has non-trivial residual: {ax['max_rel_residual_over_phi']!r}"
    print(f"[ok] axisymmetry residual = {ax['max_rel_residual_over_phi']:.3e} "
          "(machine-zero, as required for a swirl-ansatz witness)")


def test_axisymmetry_diagnostic_is_not_vacuous():
    """FALSIFICATION CONTROL (lesson 90): a deliberately non-axisymmetric
    perturbation of u_B must be DETECTED, not silently pass."""
    def broken(x):
        V = field_uB(x)
        out = V.copy()
        out[..., 0] = out[..., 0] + 0.1 * x[..., 0]
        return out
    ax = axisymmetry_residual(broken)
    assert ax["max_rel_residual_over_phi"] > 1e-3, \
        "planted non-axisymmetric control was not detected -- diagnostic is vacuous"
    print(f"[ok] planted control detected: residual = {ax['max_rel_residual_over_phi']:.3e}")


def test_normalisation_fix_matters_on_identically_zero_component():
    """Regression test for the bug this module's own construction caught:
    normalising each cylindrical component's spread by ITS OWN max (rather
    than the ring's overall field magnitude) divides roundoff by roundoff
    for u_B's identically-zero V_phi component, producing an O(1) false
    positive. This test pins the CURRENT (fixed) behaviour."""
    ax = axisymmetry_residual(field_uB)
    v_phi_spreads = [row["V_phi_rel_spread_over_phi"] for row in ax["rows"]]
    assert max(v_phi_spreads) < 1e-8, \
        f"V_phi's own near-zero component should not dominate the residual: {max(v_phi_spreads)!r}"
    print(f"[ok] V_phi rel spreads all < 1e-8 (max {max(v_phi_spreads):.3e}), "
          "confirming the ring-magnitude normalisation")


def test_lambda_undefined_on_decaying_trajectory():
    """A trajectory that relaxes monotonically toward c=0 (leg 354's own
    landed B4 finding) has no non-trivial period, so lambda must be
    reported as undefined, not silently zero or silently excluded."""
    s = np.linspace(0.0, 5.0, 2001)
    c = 0.01 * np.exp(-1.1875 * s)  # leg 354's own alpha = -19/16
    result = lambda_from_trajectory(s, c)
    assert result["lambda"] is None
    assert result["measured"] is False
    assert result["relaxes_monotonically_to_trivial"] is True
    print(f"[ok] lambda correctly undefined on a decaying trajectory: {result['reason'][:60]}...")


def test_lambda_detected_on_synthetic_periodic_trajectory():
    """FALSIFICATION CONTROL: a synthetic trajectory that DOES return to
    its initial amplitude must be detected as periodic, with lambda =
    exp(S0/2) computed correctly -- the detector must be able to succeed,
    not just always report 'undefined'."""
    S0_true = 2.0
    s = np.linspace(0.0, 3.0, 3001)
    c = 0.5 * np.cos(2.0 * np.pi * s / S0_true) + 0.5000001  # returns near c0 at s=S0
    c[0] = 1.0000001  # c0
    result = lambda_from_trajectory(s, c, return_tol=1e-2)
    assert result["measured"] is True
    expected_lambda = np.exp(S0_true / 2.0)
    assert abs(result["lambda"] - expected_lambda) / expected_lambda < 0.05, \
        f"lambda={result['lambda']!r}, expected near {expected_lambda!r}"
    print(f"[ok] periodic control detected: lambda={result['lambda']:.4f} "
          f"(expected near {expected_lambda:.4f})")


def test_chae_tsai_machine_read_matches_leg_326_landed_verdict():
    """ledger_chae_tsai() must parse leg 326's landed JSON and reproduce
    its own landed verdict programmatically -- not by re-stating it."""
    result = ledger_chae_tsai()
    assert result["excludes"] is False
    assert "SILENT" in result["verdict"]
    assert result["clause_alpha_equation_verdict"] == "FAILS_HYPOTHESIS"
    assert result["consumed_leg"] == 326
    print(f"[ok] Chae-Tsai machine-read: {result['verdict']}")


def test_pineau_vicol_machine_read_matches_leg_330_landed_verdict():
    """ledger_pineau_vicol() must parse leg 330's landed JSON's H5 clause
    and WLOG lambda ceiling programmatically."""
    outside = ledger_pineau_vicol({"lambda": 5.0})
    assert outside["excludes"] is False
    assert "OUTSIDE" in outside["verdict"]
    assert outside["consumed_leg"] == 330
    assert abs(outside["lambda_ceiling_from_source"] - 1.6487212707001282) < 1e-9

    inside = ledger_pineau_vicol({"lambda": 1.2})
    assert inside["excludes"] is None
    assert "INSIDE" in inside["verdict"]

    not_applicable = ledger_pineau_vicol({"lambda": None, "reason": "no period found"})
    assert not_applicable["verdict"] == "NOT APPLICABLE"
    print(f"[ok] Pineau-Vicol machine-read: lambda ceiling = "
          f"{outside['lambda_ceiling_from_source']:.6f}, outside/inside/N-A all route correctly")


def test_nrs_tsai_excludes_leg332_landed_witness_but_not_this_family():
    """The concrete demonstration of the gate's own no-branch warning:
    leg 332's landed L3=0.7307683991070311 (a DIFFERENT, well-behaved
    witness) must read as EXCLUDED, while leg 351/354's Type-I witness's
    own (divergent) L3 measurement must read as NOT EXCLUDED."""
    leg332_l3 = {"converged": True, "L3_norm": 0.7307683991070311,
                 "rel_change_last_step": 0.0, "rel_tol": 1e-4}
    excluded = ledger_nrs_tsai(leg332_l3)
    assert excluded["excludes"] is True

    this_l3 = l3_norm_ladder(field_uB, R_hi_ladder=(10.0, 100.0, 1e3, 1e4, 1e5, 1e6),
                              n_r=200, n_c=32, n_phi=16)
    not_excluded = ledger_nrs_tsai(this_l3)
    assert not_excluded["excludes"] is False
    print(f"[ok] NRS/Tsai: leg 332's witness EXCLUDED, this family's witness NOT EXCLUDED "
          "-- landing in L3 is the default, this family's decay rate is the exception")


def test_screen_candidate_end_to_end_is_reportable():
    """The top-level orchestration function must run all four screen
    quantities and machine-read all three ledger entries for one static
    candidate, and report it as reportable (the B7 yes-branch consequence)."""
    result = screen_candidate(field_uB, R_hi_ladder=(10.0, 100.0, 1e3, 1e4),
                               n_r=150, n_c=24, n_phi=12)
    for key in ("l3_norm", "far_field_decay", "axisymmetry", "lambda", "ledger"):
        assert key in result
    assert result["ledger"]["reportable"] is True
    assert set(result["ledger"].keys()) == {"NRS_Tsai", "Chae_Tsai", "Pineau_Vicol", "reportable"}
    print("[ok] screen_candidate() runs end-to-end and reports the full ledger")


if __name__ == "__main__":
    test_l3_norm_diverges_on_type_i_witness()
    test_fitted_decay_exponent_matches_type_i_envelope()
    test_axisymmetry_residual_near_zero_on_swirl_witness()
    test_axisymmetry_diagnostic_is_not_vacuous()
    test_normalisation_fix_matters_on_identically_zero_component()
    test_lambda_undefined_on_decaying_trajectory()
    test_lambda_detected_on_synthetic_periodic_trajectory()
    test_chae_tsai_machine_read_matches_leg_326_landed_verdict()
    test_pineau_vicol_machine_read_matches_leg_330_landed_verdict()
    test_nrs_tsai_excludes_leg332_landed_witness_but_not_this_family()
    test_screen_candidate_end_to_end_is_reportable()
    print("\nALL DSSP-SCREEN TESTS PASSED")
