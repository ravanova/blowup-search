"""Tests solver/dssp_screen.py -- Route-DSSP brick B7 (DSSP-SCREEN).

Run: .venv/bin/python test_dssp_screen.py
"""
import numpy as np

from solver.dssp_biot_savart import field_uB
from solver.dssp_screen import (
    _ledger_nrs_tsai_three_way,
    axisymmetry_residual,
    classify_ss_ansatz,
    decays_to_zero_at_infinity,
    fitted_far_field_decay_exponent,
    l3_norm_ladder,
    ledger_chae_tsai,
    ledger_morrey,
    ledger_nrs_tsai,
    ledger_pineau_vicol,
    lambda_from_trajectory,
    machine_read_ledger,
    morrey_ball_average_sweep,
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


def _synthetic_exact_ss_field(x):
    """Leg 362's planted control field: U(y) = (y/|y|)/|y|, decay exponent
    exactly -1, matching Tsai 1998's own headline example (1.5)."""
    x = np.asarray(x, dtype=float)
    r = np.linalg.norm(x, axis=-1, keepdims=True)
    r = np.maximum(r, 1e-12)
    return x / (r * r)


def test_ledger_nrs_tsai_backward_compatible_single_arg():
    """Leg 362 must not change ledger_nrs_tsai(l3_result)'s output when
    called the ORIGINAL (leg 357) way -- this is the regression guarantee
    that makes writeup/data/p2_route_dsspb7_v1.json reproduce unmoved."""
    l3 = l3_norm_ladder(field_uB, R_hi_ladder=(10.0, 100.0, 1e3, 1e4, 1e5, 1e6),
                         n_r=200, n_c=32, n_phi=16)
    result = ledger_nrs_tsai(l3)
    assert set(result.keys()) == {"excludes", "verdict", "reason"}
    assert result["verdict"] == "NOT EXCLUDED"
    assert result["excludes"] is False
    print("[ok] ledger_nrs_tsai(l3_result) alone still returns leg 357's original two-key shape")


def test_decays_to_zero_at_infinity_detects_type_i_witness():
    """leg 351's witness decays like C/|x|, so decays_to_zero_at_infinity()
    must report True -- Theorem 2's finishing-step hypothesis is met."""
    decay = fitted_far_field_decay_exponent(field_uB)
    result = decays_to_zero_at_infinity(decay)
    assert result["decays_to_zero"] is True
    print(f"[ok] decays_to_zero_at_infinity: {result['reason'][:60]}...")


def test_decays_to_zero_at_infinity_rejects_growing_field():
    """FALSIFICATION CONTROL: a field that GROWS with r must NOT be read
    as decaying to zero."""
    def growing(x):
        x = np.asarray(x, dtype=float)
        r = np.linalg.norm(x, axis=-1, keepdims=True)
        return x * r  # magnitude ~ r^2, grows
    decay = fitted_far_field_decay_exponent(growing)
    result = decays_to_zero_at_infinity(decay)
    assert result["decays_to_zero"] is False
    print(f"[ok] growing-field control correctly rejected: exponent={result['fitted_exponent']:.3f}")


def test_classify_ss_ansatz_static_candidate_is_exact_ss():
    """A candidate with no trajectory ever measured (lambda_from_trajectory
    not called, or reporting measured=False because no s_vals/c_vals were
    given) is read as satisfying the exact-SS ansatz -- it IS a single
    stationary profile U(y), exactly Tsai's (1.2)_1 form."""
    lam = {"lambda": None, "S0": None, "measured": False,
           "reason": "static candidate, no trajectory supplied"}
    result = classify_ss_ansatz(lam)
    assert result["ansatz"] == "EXACT-SS"
    assert result["satisfies_theorem_ansatz"] is True
    print("[ok] static candidate classified EXACT-SS (ansatz satisfied)")


def test_classify_ss_ansatz_periodic_lambda_gt_1_is_dss():
    """FALSIFICATION CONTROL / positive detector: a genuinely periodic
    trajectory at lambda > 1 must be classified DSS, failing the ansatz --
    this is leg 357's own landed periodic-detector construction, reused
    here to confirm the classifier can actually detect DSS, not just
    always report EXACT-SS."""
    S0_true = 2.0
    s = np.linspace(0.0, 3.0, 3001)
    c = 0.5 * np.cos(2.0 * np.pi * s / S0_true) + 0.5000001
    c[0] = 1.0000001
    lam_result = lambda_from_trajectory(s, c, return_tol=1e-2)
    result = classify_ss_ansatz(lam_result)
    assert result["ansatz"] == "DSS"
    assert result["satisfies_theorem_ansatz"] is False
    assert result["measured_lambda"] > 1.0
    print(f"[ok] periodic lambda={result['measured_lambda']:.4f}>1 trajectory classified DSS "
          "(ansatz fails)")


def test_gate_control_1_planted_synthetic_exact_ss_gap_then_closure():
    """Leg 362's gate control 1: before the fix, a synthetic exact-SS
    decay-exponent -1 candidate (Tsai's own headline example) reads
    'excluded by neither theorem'; after the fix it must read
    EXCLUDED-BY-T2."""
    l3 = l3_norm_ladder(_synthetic_exact_ss_field,
                         R_hi_ladder=(10.0, 100.0, 1e3, 1e4, 1e5, 1e6),
                         n_r=200, n_c=32, n_phi=16)
    decay = fitted_far_field_decay_exponent(_synthetic_exact_ss_field)
    lam = {"lambda": None, "S0": None, "measured": False,
           "reason": "static synthetic candidate, no trajectory supplied"}
    ansatz = classify_ss_ansatz(lam)
    decay_test = decays_to_zero_at_infinity(decay)

    before = ledger_nrs_tsai(l3)
    after = ledger_nrs_tsai(l3, decay_test, ansatz)

    assert before["verdict"] == "NOT EXCLUDED", "gap-demonstration control did not reproduce the gap"
    assert after["verdict"] == "EXCLUDED-BY-T2", "extended ledger did not close the gap"
    print(f"[ok] control 1: before={before['verdict']!r} -> after={after['verdict']!r}")


def test_gate_control_2_real_dss_object_not_reached_by_ansatz():
    """Leg 362's gate control 2: this repo's actual DSS object (field_uB
    plus a genuinely periodic lambda>1 trajectory) must read
    NOT-REACHED-BY-ANSATZ, citing the exact-SS ansatz failure."""
    S0_true = 2.0
    s = np.linspace(0.0, 3.0, 3001)
    c = 0.5 * np.cos(2.0 * np.pi * s / S0_true) + 0.5000001
    c[0] = 1.0000001
    lam_result = lambda_from_trajectory(s, c, return_tol=1e-2)
    ansatz = classify_ss_ansatz(lam_result)

    l3 = l3_norm_ladder(field_uB, R_hi_ladder=(10.0, 100.0, 1e3, 1e4, 1e5, 1e6),
                         n_r=200, n_c=32, n_phi=16)
    decay = fitted_far_field_decay_exponent(field_uB)
    decay_test = decays_to_zero_at_infinity(decay)

    ledger = ledger_nrs_tsai(l3, decay_test, ansatz)
    assert ledger["verdict"] == "NOT-REACHED-BY-ANSATZ"
    assert "ansatz" in ledger["deciding_clause"].lower() or "(1.2)" in ledger["deciding_clause"]
    print(f"[ok] control 2: real DSS object verdict={ledger['verdict']!r}, "
          f"deciding_clause cites the ansatz")


def test_machine_read_ledger_optional_args_default_to_original_behaviour():
    """machine_read_ledger() with only its original two positional args
    must still return leg 357's original NRS_Tsai shape."""
    l3 = l3_norm_ladder(field_uB, R_hi_ladder=(10.0, 100.0, 1e3, 1e4),
                         n_r=150, n_c=24, n_phi=12)
    lam = {"lambda": None, "S0": None, "measured": False, "reason": "no trajectory"}
    ledger = machine_read_ledger(l3, lam)
    assert set(ledger["NRS_Tsai"].keys()) == {"excludes", "verdict", "reason"}
    print("[ok] machine_read_ledger() with two args reproduces leg 357's original shape")


_RAY_DIRECTION = np.array([0.4, 0.5, np.sqrt(1.0 - 0.4 ** 2 - 0.5 ** 2)])
_RAY_DIRECTION = _RAY_DIRECTION / np.linalg.norm(_RAY_DIRECTION)


def _nonmonotone_morrey_field(x):
    """Leg 370's planted control field: a synthetic exact-SS profile with
    base decay U(y) ~ (y/|y|)/|y| plus a narrow angular*radial bump
    concentrated on the SAME sampled ray fitted_far_field_decay_exponent()
    uses, at r~1000 -- pushes the LAST sampled magnitude above the FIRST
    (evading T2's monotonic-decrease-between-first-and-last proxy) while
    staying angularly narrow enough that the full-solid-angle L^3 shell
    integral is still genuinely log-divergent (evading T1). See
    experiments/p2_route_b7m_v1.py's own fuller docstring for the same
    construction (this is the identical field, duplicated here so this
    test file does not import a runner script)."""
    x = np.asarray(x, dtype=float)
    r = np.linalg.norm(x, axis=-1, keepdims=True)
    r = np.maximum(r, 1e-9)
    base = 1.0 / r
    direction = x / r
    cosang = np.clip(np.sum(direction * _RAY_DIRECTION, axis=-1, keepdims=True), -1.0, 1.0)
    ang = np.arccos(cosang)
    angular_bump = np.exp(-(ang ** 2) / 0.01)
    radial_bump = np.exp(-((np.log10(r) - 3.0) ** 2) / 0.0005)
    bump = 300.0 * angular_bump * radial_bump
    amp = base * (1.0 + bump)
    return direction * amp


def test_morrey_ball_average_sweep_finds_membership_for_type_i_decay():
    """A plain 1/|x| exact-SS profile's ball-averaged L^1 mass grows like
    R^2 (Int_{B_R} |V| dy ~ Int r^2 dr / r ~ R^2), which IS bounded at the
    M-dot_{q,1} scaling rate for q near 3 (inside the open (3/2,6) range) --
    the sweep must find a witnessing q and report in_morrey_class True."""
    def field_type_i(x):
        x = np.asarray(x, dtype=float)
        r = np.linalg.norm(x, axis=-1, keepdims=True)
        r = np.maximum(r, 1e-9)
        return x / (r * r)
    m = morrey_ball_average_sweep(field_type_i, n_r=100, n_c=16, n_phi=8)
    assert m["in_morrey_class"] is True
    assert 1.5 < m["witnessing_q"] < 6.0
    print(f"[ok] Type-I 1/|x| profile: in_morrey_class=True, witnessing_q={m['witnessing_q']:.3f}")


def test_ledger_morrey_not_reached_by_ansatz_on_dss():
    """A candidate classified DSS (via a genuinely periodic lambda>1
    trajectory) must read NOT-REACHED-BY-ANSATZ under the Morrey entry,
    exactly as T1/T2 already do -- the ansatz gate applies to Theorem 1.2
    too, per leg 368's confirmed reading (no DSS content anywhere in the
    primary text)."""
    S0_true = 2.0
    s = np.linspace(0.0, 3.0, 3001)
    c = 0.5 * np.cos(2.0 * np.pi * s / S0_true) + 0.5000001
    c[0] = 1.0000001
    lam_result = lambda_from_trajectory(s, c, return_tol=1e-2)
    ansatz = classify_ss_ansatz(lam_result)
    assert ansatz["ansatz"] == "DSS"

    morrey = morrey_ball_average_sweep(field_uB, n_r=100, n_c=16, n_phi=8)
    verdict = ledger_morrey(morrey, ansatz)
    assert verdict["verdict"] == "NOT-REACHED-BY-ANSATZ"
    assert "(1.2)" in verdict["deciding_clause"] or "ansatz" in verdict["deciding_clause"].lower()
    print(f"[ok] Morrey entry on DSS object: {verdict['verdict']!r}, ansatz-gated exactly like T1/T2")


def test_gate_control_a_planted_widen_then_close():
    """Leg 370's gate control (a): the planted non-monotone-decay control
    must evade BOTH T1 (L^3 does not converge) and T2 (does not read
    decays-to-zero) while the new Morrey entry catches it as
    EXCLUDED-BY-MORREY -- demonstrating leg 368's WIDENS finding
    concretely, then closing it."""
    field = _nonmonotone_morrey_field
    l3 = l3_norm_ladder(field, R_hi_ladder=(10.0, 100.0, 1e3, 1e4, 1e5, 1e6),
                         n_r=200, n_c=32, n_phi=16)
    decay = fitted_far_field_decay_exponent(field)
    decay_test = decays_to_zero_at_infinity(decay)
    lam_none = {"lambda": None, "S0": None, "measured": False,
                "reason": "static synthetic candidate, no trajectory supplied"}
    ansatz = classify_ss_ansatz(lam_none)

    t1_t2 = _ledger_nrs_tsai_three_way(l3, decay_test, ansatz)
    assert t1_t2["verdict"] == "NOT EXCLUDED", \
        f"planted control should evade T1/T2, got {t1_t2['verdict']!r}"

    morrey = morrey_ball_average_sweep(field, n_r=100, n_c=16, n_phi=8)
    morrey_verdict = ledger_morrey(morrey, ansatz)
    assert morrey_verdict["verdict"] == "EXCLUDED-BY-MORREY", \
        f"planted control should be caught by Morrey, got {morrey_verdict['verdict']!r}"
    print(f"[ok] control (a): T1/T2={t1_t2['verdict']!r} -> Morrey={morrey_verdict['verdict']!r}")


def test_machine_read_ledger_morrey_key_is_opt_in():
    """machine_read_ledger()'s new morrey_result parameter must be
    backward compatible: omitting it (every pre-existing call site) must
    NOT add a 'Morrey' key, so set(ledger.keys()) is UNCHANGED for every
    caller that predates this leg -- this is what makes leg 357's and leg
    362's banked JSON reproduce unmoved."""
    l3 = l3_norm_ladder(field_uB, R_hi_ladder=(10.0, 100.0, 1e3, 1e4),
                         n_r=150, n_c=24, n_phi=12)
    lam = {"lambda": None, "S0": None, "measured": False, "reason": "no trajectory"}

    ledger_default = machine_read_ledger(l3, lam)
    assert set(ledger_default.keys()) == {"NRS_Tsai", "Chae_Tsai", "Pineau_Vicol", "reportable"}, \
        "machine_read_ledger()'s default key set changed -- breaks backward compatibility"

    decay = fitted_far_field_decay_exponent(field_uB)
    decay_test = decays_to_zero_at_infinity(decay)
    ansatz = classify_ss_ansatz(lam)
    morrey = morrey_ball_average_sweep(field_uB, n_r=80, n_c=12, n_phi=8,
                                        R_hi_ladder=(10.0, 100.0, 1e3, 1e4))
    ledger_with_morrey = machine_read_ledger(l3, lam, decay_test, ansatz, morrey)
    assert set(ledger_with_morrey.keys()) == {"NRS_Tsai", "Chae_Tsai", "Pineau_Vicol",
                                               "Morrey", "reportable"}
    print("[ok] machine_read_ledger()'s Morrey key is opt-in (backward compatible by default)")


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
    test_ledger_nrs_tsai_backward_compatible_single_arg()
    test_decays_to_zero_at_infinity_detects_type_i_witness()
    test_decays_to_zero_at_infinity_rejects_growing_field()
    test_classify_ss_ansatz_static_candidate_is_exact_ss()
    test_classify_ss_ansatz_periodic_lambda_gt_1_is_dss()
    test_gate_control_1_planted_synthetic_exact_ss_gap_then_closure()
    test_gate_control_2_real_dss_object_not_reached_by_ansatz()
    test_machine_read_ledger_optional_args_default_to_original_behaviour()
    test_morrey_ball_average_sweep_finds_membership_for_type_i_decay()
    test_ledger_morrey_not_reached_by_ansatz_on_dss()
    test_gate_control_a_planted_widen_then_close()
    test_machine_read_ledger_morrey_key_is_opt_in()
    print("\nALL DSSP-SCREEN TESTS PASSED")
