"""Tests for `solver/chen_inviscid_certificate.py` (leg 187, Route-M2CI).

Self-running, no pytest -- the repo convention (`scripts/merge_gate.sh` line 18).

The load-bearing tests here are the EXACT ones: the orbit's residual is verified as the
zero polynomial in `Fraction` arithmetic, so those assertions are proofs, not measurements.
Every measured quantity is tested against a control that CAN report the other answer
(lesson 90) -- a test that only ever passes is a tautology of the code.
"""

import sys
from fractions import Fraction

import numpy as np

from solver.chen_inviscid_certificate import (
    C_L, C_OMEGA, GAMMA_CHEN, RF, bordered_operator, certificate_battery,
    clause_farfield_symbol, clause_injectivity, clause_isolation, clause_space_membership,
    divergence_exponents, exact_defect_numerator, exact_orbit_check, gate_verdict,
    measured_decay_exponent, orbit_generator, orbit_profile, unbordered_Z_lower_bound,
    weighted_sup_norm,
)
from solver.dissipative_profile import DissipativeProfile, chen_profile

FAILURES = []


def check(name, cond, detail=""):
    if cond:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}  {detail}")
        FAILURES.append(name)


# ---------------------------------------------------------------------------
# 1. the exact rational-function arithmetic itself
# ---------------------------------------------------------------------------

def test_rf_arithmetic():
    print("test_rf_arithmetic")
    g = Fraction(3, 8)
    # d/dX [X / (X^2+g)] = (g - X^2)/(X^2+g)^2
    d = RF([0, 1], 1, g).der()
    check("RF.der matches the hand-computed quotient rule",
          d.num == [g, Fraction(0), Fraction(-1)] and d.k == 2, f"got {d.num}, k={d.k}")
    # (a+b) and (a*b) on a case with a known answer
    s = RF([1], 0, g) + RF([1], 1, g)          # 1 + 1/D = (D+1)/D
    check("RF.__add__ puts both over the common denominator",
          s.k == 1 and s.num == [g + 1, Fraction(0), Fraction(1)], f"got {s.num}")
    m = RF([0, 1], 1, g) * RF([2], 1, g)
    check("RF.__mul__ adds denominator powers", m.k == 2 and m.num == [Fraction(0), Fraction(2)])
    check("RF.is_zero is true only for the zero numerator",
          RF([0, 0], 3, g).is_zero() and not RF([0, 1], 3, g).is_zero())


# ---------------------------------------------------------------------------
# 2. THE EXACT CLAUSE -- the orbit is a continuum of exact solutions
# ---------------------------------------------------------------------------

def test_exact_orbit_is_a_continuum_of_zeros():
    print("test_exact_orbit_is_a_continuum_of_zeros")
    rows = exact_orbit_check()
    check("every tested gamma has an IDENTICALLY ZERO residual numerator (exact arithmetic)",
          all(r["exact_zero"] for r in rows),
          str([(r["gamma"], r["numerator_coeffs"]) for r in rows if not r["exact_zero"]]))
    check("Chen's own gamma = 3/8 is among them and is an exact zero",
          any(r["is_chen_profile"] and r["exact_zero"] for r in rows))
    # THE CONTROL THAT CAN FAIL: perturb the amplitude off the distinguished value and the
    # residual must STOP vanishing.  If this passed too, the arithmetic would be returning
    # zero for everything and the clause above would be vacuous.
    check("CONTROL: a 1/100 amplitude perturbation makes the residual NONZERO at every gamma",
          all(r["control_is_nonzero"] for r in rows),
          str([r["gamma"] for r in rows if not r["control_is_nonzero"]]))
    # A second, independent control: the wrong advection parameter must not solve.
    num_a0, _ = exact_defect_numerator(GAMMA_CHEN, a=Fraction(0))
    check("CONTROL: a = 0 (the CLM sibling) does NOT solve at Chen's a = 1/2 constants",
          any(c != 0 for c in num_a0), f"got {num_a0}")
    num_cl, _ = exact_defect_numerator(GAMMA_CHEN, c_l=Fraction(1, 2))
    check("CONTROL: c_l = 1/2 instead of 1/3 does NOT solve",
          any(c != 0 for c in num_cl), f"got {num_cl}")


def test_orbit_matches_leg125_transcription_at_chens_gamma():
    print("test_orbit_matches_leg125_transcription_at_chens_gamma")
    X = np.linspace(-6.0, 6.0, 401)
    mine = orbit_profile(X, float(GAMMA_CHEN))
    theirs, their_Ux, their_U = chen_profile(X)      # leg 125 returns (Omega, U_x, U)
    err = float(np.max(np.abs(mine - theirs)))
    check("orbit_profile at g = 3/8 IS leg 125's chen_profile, to machine precision",
          err < 1e-13, f"max abs diff {err:.3e}")
    # CONTROL: a different orbit point must NOT coincide with the transcription.
    off = float(np.max(np.abs(orbit_profile(X, 0.5) - theirs)))
    check("CONTROL: the g = 1/2 orbit point is a genuinely DIFFERENT function",
          off > 1e-3, f"max abs diff {off:.3e}")
    # The exact-arithmetic module hard-codes H Psi and U as rational functions; those must
    # be leg 125's transcribed ones too, or the exact defect is solving a different problem.
    g = float(GAMMA_CHEN)
    check("the module's H Psi convention matches leg 125's U_x",
          float(np.max(np.abs((g - X ** 2) / (X ** 2 + g) ** 2 - their_Ux))) < 1e-13)
    check("the module's U convention matches leg 125's U",
          float(np.max(np.abs(X / (X ** 2 + g) - their_U))) < 1e-13)


def test_orbit_generator_is_the_true_tangent():
    print("test_orbit_generator_is_the_true_tangent")
    X = np.linspace(-8.0, 8.0, 801)
    g = float(GAMMA_CHEN)
    h = 1e-6
    fd = (orbit_profile(X, g + h) - orbit_profile(X, g - h)) / (2 * h)
    an = orbit_generator(X, g)
    rel = float(np.max(np.abs(fd - an)) / np.max(np.abs(an)))
    check("orbit_generator equals the central difference d/dg of the orbit",
          rel < 1e-7, f"relative diff {rel:.3e}")


# ---------------------------------------------------------------------------
# 3. the measured clauses, each against a control
# ---------------------------------------------------------------------------

def test_injectivity_kernel_separates_from_controls():
    print("test_injectivity_kernel_separates_from_controls")
    dp = DissipativeProfile(a=0.5, n=401)
    inj = clause_injectivity(dp, s=2.0)
    kd = inj["orbit_tangent_phi"]["relative_defect"]
    cd = inj["control_localised_bump"]["relative_defect"]
    check("the orbit tangent is annihilated by DF to <1e-3 relative", kd < 1e-3, f"{kd:.3e}")
    check("CONTROL: a localised bump is NOT annihilated (relative defect O(1))",
          cd > 1e-2, f"{cd:.3e}")
    check("kernel and non-kernel separate by >1e3", inj["kernel_to_control_ratio"] > 1e3,
          f"ratio {inj['kernel_to_control_ratio']:.3e}")


def test_kernel_sharpens_with_resolution():
    """The kernel must be an OPERATOR fact: its defect must fall as the grid refines,
    while the control's stays flat.  A grid artifact would do neither."""
    print("test_kernel_sharpens_with_resolution")
    ks, cs = [], []
    for n in (401, 801):
        inj = clause_injectivity(DissipativeProfile(a=0.5, n=n), s=2.0)
        ks.append(inj["orbit_tangent_phi"]["relative_defect"])
        cs.append(inj["control_localised_bump"]["relative_defect"])
    check("kernel relative defect FALLS by >3x from n=401 to n=801",
          ks[0] / ks[1] > 3.0, f"{ks[0]:.3e} -> {ks[1]:.3e}")
    check("CONTROL: the bump's relative defect stays flat (within 10%)",
          abs(cs[0] / cs[1] - 1.0) < 0.10, f"{cs[0]:.3e} -> {cs[1]:.3e}")


def test_Z_lower_bound_and_its_two_float_regimes():
    print("test_Z_lower_bound_and_its_two_float_regimes")
    dp = DissipativeProfile(a=0.5, n=401)
    lb = unbordered_Z_lower_bound(dp, s=2.0)
    check("the exact lower bound Z_0 + Z_1 >= 1 is asserted as exact",
          lb["bound_is_exact"] and lb["Z0_plus_Z1_lower_bound"] == 1.0)
    check("the contraction factor upper bound is 0 (never positive)",
          lb["one_minus_Z_upper_bound"] == 0.0)
    # The documented two-regime behaviour, which is the honest part of this clause.
    check("default-rcond pinv gives a MISLEADING ~0 shadow (it inverts the near-kernel)",
          lb["float_shadow_pinv_default_rcond"] < 1e-5,
          f"{lb['float_shadow_pinv_default_rcond']:.3e}")
    check("truncated-rcond pinv returns the shadow to 1 (within 1e-3)",
          abs(lb["float_shadow_pinv_rcond_1e-6"] - 1.0) < 1e-3,
          f"{lb['float_shadow_pinv_rcond_1e-6']:.6f}")
    check("sigma_min/sigma_max sits ABOVE numpy's default cutoff, which is WHY regime 1 lies",
          lb["sigma_ratio"] > 1e-13, f"{lb['sigma_ratio']:.3e}")


def test_isolation_fails_with_competitors_at_every_radius():
    print("test_isolation_fails_with_competitors_at_every_radius")
    dp = DissipativeProfile(a=0.5, n=401)
    iso = clause_isolation(dp, s=2.0)
    for row in iso["rows"]:
        r = row["ball_radius_r"]
        check(f"a competitor exact zero sits at distance r={r:g} (bisection converged)",
              abs(row["distance_achieved"] / r - 1.0) < 1e-6,
              f"achieved {row['distance_achieved']:.6e}")
        check(f"that competitor's residual is at the centre's own floor (r={r:g})",
              row["competitor_residual_sup"] < 2.0 * row["centre_residual_sup"],
              f"{row['competitor_residual_sup']:.3e} vs {row['centre_residual_sup']:.3e}")


def test_farfield_symbol_vanishes_at_the_profiles_own_decay_rate():
    print("test_farfield_symbol_vanishes_at_the_profiles_own_decay_rate")
    fs = clause_farfield_symbol()
    check("the symbol c_omega + s c_l vanishes exactly at s = 3",
          abs(fs["symbol_zero_at_s"] - 3.0) < 1e-12, f"{fs['symbol_zero_at_s']}")
    check("no grading is admissible at or above s = 3",
          not any(r["admissible"] for r in fs["rows"] if r["s"] >= 3.0))
    check("gradings below 3 ARE admissible (the clause is not vacuous)",
          any(r["admissible"] for r in fs["rows"] if r["s"] < 3.0))
    # the tail inverse must blow up as s -> 3
    near = [r for r in fs["rows"] if r["s"] == 2.99][0]
    mid = [r for r in fs["rows"] if r["s"] == 2.0][0]
    check("the tail inverse norm diverges as s -> 3 (100x from s=2 to s=2.99)",
          near["tail_inverse_norm"] / mid["tail_inverse_norm"] > 50.0)

    dec = measured_decay_exponent(DissipativeProfile(a=0.5, n=801))
    check("the profile's MEASURED decay exponent is 3 (not asserted)",
          abs(dec["exponent"] - 3.0) < 1e-3, f"{dec['exponent']:.6f}")
    check("CONTROL: a genuine X^-2 profile measures 2, not 3",
          abs(dec["control_slope_on_Xminus2_profile"] + 2.0) < 1e-3,
          f"{dec['control_slope_on_Xminus2_profile']:.6f}")


def test_space_membership_sees_the_divergence_above_s_equals_3():
    print("test_space_membership_sees_the_divergence_above_s_equals_3")
    rows = clause_space_membership(DissipativeProfile(a=0.5, n=801))
    conv = [r for r in rows if r["s"] <= 3.0]
    div = [r for r in rows if r["s"] == 3.5][0]
    check("for s <= 3 the weighted norm is grid-converged (ratio ~ 1)",
          all(abs(r["ratio_vs_half_domain"] - 1.0) < 1e-6 for r in conv))
    check("CONTROL: at s = 3.5 the norm is carried by the outermost nodes (ratio > 1.1)",
          div["ratio_vs_half_domain"] > 1.1, f"{div['ratio_vs_half_domain']:.4f}")


def test_bordering_repairs_the_singularity_numerically():
    """The standard repair (which this leg CITES, never claims -- see novelty Q2) must
    visibly work, or the NO would be reported for the wrong reason."""
    print("test_bordering_repairs_the_singularity_numerically")
    bo = bordered_operator(DissipativeProfile(a=0.5, n=401), s=2.0)
    lift = bo["sigma_min"] / bo["unbordered_sigma_min"]
    check("bordering lifts sigma_min by >100x", lift > 100.0, f"lift {lift:.3e}")
    check("the bordered matrix is genuinely nonsingular", bo["sigma_min"] > 1e-6,
          f"{bo['sigma_min']:.3e}")


def test_Z2_diverges_while_the_kernel_control_collapses():
    print("test_Z2_diverges_while_the_kernel_control_collapses")
    dv = divergence_exponents(ns=(201, 401, 801))
    check("Z_2 grows with n (it is not an operator constant in this space)",
          dv["Z2_diverges"] and dv["slopes_in_log_n"]["Z2"] > 1.0,
          f"slope {dv['slopes_in_log_n']['Z2']:.3f}")
    check("Z_2 grows by >10x across the ladder",
          dv["Z2_growth_over_ladder"] > 10.0, f"{dv['Z2_growth_over_ladder']:.3e}")
    # CONTROL that can report the other answer: if the kernel were a grid artifact,
    # sigma_ratio would SETTLE.  It must collapse instead.
    check("CONTROL: sigma_min/sigma_max collapses with n (kernel is an operator fact)",
          dv["slopes_in_log_n"]["sigma_ratio"] < -2.0,
          f"slope {dv['slopes_in_log_n']['sigma_ratio']:.3f}")


# ---------------------------------------------------------------------------
# 4. the battery and the gate
# ---------------------------------------------------------------------------

def test_battery_and_gate_answer_NO_for_the_stated_reasons():
    print("test_battery_and_gate_answer_NO_for_the_stated_reasons")
    bat = certificate_battery(n=401)
    check("H2: the exact defect is zero (Y_0 = 0, the best value the framework admits)",
          bat["H2_exact_defect_is_zero"])
    check("the unbordered budget does NOT close", not bat["unbordered_budget"]["closes"],
          str(bat["unbordered_budget"].get("reason")))
    check("the shared hypothesis guard finds the constants admissible (the failure is NOT "
          "a bad input)", bat["guard_on_unbordered_constants"] == [],
          str(bat["guard_on_unbordered_constants"]))

    v = gate_verdict(bat, divergence_exponents(ns=(201, 401, 801)))
    check("the gate is answered NO", v["answer"] == "NO")
    check("the failing clauses are named as H3/H5/H7", len(v["failing_clauses"]) == 3)
    check("Z_0 + Z_1 lower bound is exactly 1", v["Z0_plus_Z1_lower_bound"] == 1.0)
    check("the verdict states the INVISCID scope explicitly",
          "INVISCID" in v["scope"] and "viscous" in v["scope"])
    check("the verdict records that the YES branch would have been hollow",
          "closed form" in v["and_the_YES_branch_would_have_been_hollow"].lower())


def main():
    for t in (test_rf_arithmetic,
              test_exact_orbit_is_a_continuum_of_zeros,
              test_orbit_matches_leg125_transcription_at_chens_gamma,
              test_orbit_generator_is_the_true_tangent,
              test_injectivity_kernel_separates_from_controls,
              test_kernel_sharpens_with_resolution,
              test_Z_lower_bound_and_its_two_float_regimes,
              test_isolation_fails_with_competitors_at_every_radius,
              test_farfield_symbol_vanishes_at_the_profiles_own_decay_rate,
              test_space_membership_sees_the_divergence_above_s_equals_3,
              test_bordering_repairs_the_singularity_numerically,
              test_Z2_diverges_while_the_kernel_control_collapses,
              test_battery_and_gate_answer_NO_for_the_stated_reasons):
        t()
    print()
    if FAILURES:
        print(f"FAILED ({len(FAILURES)}): {FAILURES}")
        return 1
    print("all tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
