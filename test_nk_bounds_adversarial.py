"""ADVERSARIAL gates for solver/nk_bounds.py -- Route-NKA, leg 116.

`test_nk_bounds.py` (Route-D, legs v6-v11) tests that this module COMPUTES correctly: every
quantity in it dominates an independently computed measurement, and it is checked against an
ADVERSARY rather than a random family (banked lesson 9).  Every one of those gates hands the
module a WELL-FORMED problem.  This file asks the other question, the one leg 79 asked of
`solver/port_certification.py` and leg 98 asked of `solver/interval_certificate.py`: **what
does the module say when the input is not well formed -- and can a planted non-solution
survive inside the ball it reports?**

**LEG 116's GATE ANSWERED YES.**  Of 52 hypothesis-violating inputs, **21 returned a CLOSING
certificate** (19 of them LOAD-BEARING -- the hypothesis-satisfying counterpart does NOT
close, so the violation is exactly what bought the certificate), and **12 claimed UPPER
bounds fell BELOW an independently computed reference**.  Six of the false accepts are
centred on a PLANTED NON-SOLUTION and report a ball containing no zero of `F` at all; the
sharpest is a certified ball `[0.8083, 1.1917]` around `x = 1.0` for `F(x) = x^2 - 2`, which
misses the nearest zero `sqrt(2)` by **1.161 ball radii**.  The full battery, with every
constant, every ball and every ratio, is
`experiments/p2_route_nka_v1_adversarial.py` -> `writeup/data/p2_route_nka_v1_adversarial.json`.

**THIS FILE DOES NOT PATCH ANYTHING, AND MUST NOT BE READ AS AN ENDORSEMENT.**  DIRECTION.md
declares leg 116 read-only on `solver/nk_bounds.py` under BOTH branches of its gate; the
repair belongs to a bench-repair agent under the orchestrator's authority, exactly as legs
79, 98 and 69 were handled.  So the gates below split into three kinds, stated in each
docstring, following leg 98's convention verbatim:

  * **GAP-PIN gates** assert the DEFECTIVE behaviour as it stands today, so the defect cannot
    quietly change shape while it waits for repair (lesson 68: a finding kept in prose decays
    at the rate of memory; a finding kept as an assertion does not).  **These gates will fail
    the day the guard lands -- INVERT them, do not weaken them.**  Each names its inversion.
  * **HOLDS gates** assert the checks that ARE in place and must never regress -- the NaN and
    `+inf` rejections in `budget`, the `alpha <= 1` refusal in `cos_power_mass`, and the
    `gamma = 0` division that raises instead of returning a number.
  * **CONTROL gates** are the positive controls: the honest certificate must still close at a
    genuine approximate zero and must still refuse at the planted point, and the reference
    integrator must still reproduce the module's own published asymptote -- so that a
    "nothing closes any more" regression cannot masquerade as robustness.

WHICH HYPOTHESES, AND WHERE THEY COME FROM (writeup/novelty/leg_116.md)
-----------------------------------------------------------------------------
  (H1) `Y_0`, `Z_0`, `Z_1`, `Z_2` are upper bounds on norms in the published radii polynomial
       theorem, hence FINITE and NONNEGATIVE, and the conclusion is a zero INSIDE the ball of
       radius `r_min`.  Textbook since 2015; not a finding of this leg.
  (H2) A supremum is not the maximum over a finite, TRUNCATED sample grid -- the founding
       premise of interval branch-and-bound.  Also not a finding of this leg.
  (H3) A weight vector defines a norm: strictly positive and finite, with the seminorm
       kernel's zeros confined to the diagonal.

The only thing leg 116 claims is the MEASUREMENT: which of these the module enforces, and by
how much the unenforced ones move the answer.

Run: .venv/bin/python test_nk_bounds_adversarial.py     (~3 min)
"""

import math
import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from experiments.p2_route_nka_v1_adversarial import (          # noqa: E402
    LIVE_X_MAX, P_ROOT, P_XBAR, P_XPLANT, _ball_report, _I_out_reference,
    _p_constants, _reference_sup, family_C,
)
from solver.decay_grading import cos_power_mass                # noqa: E402
from solver.nk_bounds import (                                 # noqa: E402
    _I_out, budget, farfield_modelling_error_bound, hilbert_farfield_bound,
    quadratic_constant_upper, two_point_dual,
)

INF = float("inf")
NAN = float("nan")


# ===========================================================================
# CONTROL gates -- both answers must remain reachable (lesson 90)
# ===========================================================================


def test_control_honest_certificate_closes_and_refuses():
    """CONTROL.  The honest certificate closes at a genuine approximate zero and refuses at
    the planted non-solution.  If this ever fails, every GAP-PIN gate below is measuring a
    broken instrument rather than a defect."""
    good = _p_constants(P_XBAR)
    plant = _p_constants(P_XPLANT)
    v_good, v_plant = budget(**good), budget(**plant)

    assert v_good["closes"], f"the honest certificate stopped closing at x={P_XBAR}: {v_good}"
    assert v_good["r_min"] > 0.0, f"honest r_min must be positive: {v_good}"
    ball = _ball_report(P_XBAR, v_good)
    assert ball["contains_a_zero"], (
        f"the honest ball around {P_XBAR} must contain sqrt(2)={P_ROOT}: {ball}")

    assert not v_plant["closes"], (
        f"honest constants at the planted non-solution x={P_XPLANT} must REFUSE, got {v_plant}")
    assert plant["Y0"] > 20.0 * good["Y0"], (
        f"the planted point must be visibly worse: Y0 {plant['Y0']} vs {good['Y0']}")
    print("  control: honest closes at 1.4 (r_min=%.4e, ball holds sqrt2) and refuses at 1.0"
          % v_good["r_min"])


def test_control_reference_integrator_reproduces_the_published_asymptote():
    """CONTROL.  Family B's ground truth is only usable if it is independently right.  The
    module's own docstring states `_I_out -> M_alpha / X`; the reference must reproduce that
    sharp constant, and must be converged far tighter than the discrepancies it is used to
    call."""
    # The approach to the asymptote is algebraic: the neglected part of the mass integral
    # beyond y ~ X is O(X^{1-alpha}), so the admissible slack must carry that exponent
    # rather than be a flat constant (a flat 2e-3 passes at alpha=1.9 and fails at 1.2 for
    # a reason that has nothing to do with the reference being wrong).
    for alpha in (1.2, 1.5, 1.9):
        M = float(cos_power_mass(alpha))
        for X in (1e8, 1e10, 1e12):
            r = _I_out_reference(X, alpha)
            tol = max(3.0 * X ** (1.0 - alpha), 5e-3)
            assert abs(r * X / M - 1.0) < tol, (
                f"reference lost the M_alpha/X asymptote at alpha={alpha}, X={X}: "
                f"ref*X/M = {r * X / M} (tolerance {tol})")
    r8 = _I_out_reference(1e12, 1.9, n=8000)
    r128 = _I_out_reference(1e12, 1.9, n=128000)
    assert abs(r8 - r128) / r128 < 1e-10, (
        f"reference not converged: n=8000 vs n=128000 differ by {(r8 - r128) / r128}")
    print("  control: reference reproduces M_alpha/X and is self-converged to <1e-10")


# ===========================================================================
# HOLDS gates -- the checks that ARE in place
# ===========================================================================


def test_holds_nan_constants_are_rejected():
    """HOLDS.  A NaN in any slot must not produce a closing certificate.  This works because
    every comparison against NaN is False, not because a guard exists -- which is exactly
    why it is pinned: a refactor to `if not (x >= 0): reject` would keep it, a refactor to
    `if x < 0: reject` would silently lose it."""
    base = {"Y0": 1.0, "Z0": 0.0, "Z1": 0.3, "Z2": 1.0}
    for slot in ("Y0", "Z0", "Z1", "Z2"):
        c = dict(base); c[slot] = NAN
        v = budget(**c)
        assert not v["closes"], f"a NaN {slot} produced a closing certificate: {v}"
    print("  holds: NaN in any of the four slots is rejected")


def test_holds_positive_infinity_is_rejected():
    """HOLDS.  `+inf` in any slot must not close."""
    base = {"Y0": 1.0, "Z0": 0.0, "Z1": 0.3, "Z2": 1.0}
    for slot in ("Y0", "Z0", "Z1", "Z2"):
        c = dict(base); c[slot] = INF
        v = budget(**c)
        assert not v["closes"], f"{slot} = +inf produced a closing certificate: {v}"
    print("  holds: +inf in any of the four slots is rejected")


def test_holds_Z0_plus_Z1_at_or_above_one_is_rejected():
    """HOLDS.  The contraction condition `Z_0 + Z_1 < 1` is genuinely enforced."""
    for Z1 in (0.7, 1.0, 1.5, 1e6):
        v = budget(1e-12, 0.3, Z1, 1.0)
        assert not v["closes"], f"Z_0+Z_1 = {0.3 + Z1} >= 1 closed: {v}"
    assert budget(1e-30, 0.0, 1.0 - 1e-16, 1.0)["closes"] is False, (
        "Z_1 one ulp below 1 with Z_0 = 0 must still fail the strict inequality")
    print("  holds: Z_0 + Z_1 >= 1 is rejected, including at the 1-ulp boundary")


def test_holds_negative_and_zero_Z2_are_rejected():
    """HOLDS.  `Z_2 <= 0` is caught by the explicit `Z2 > 0` guard -- the one domain check
    the module does perform."""
    for Z2 in (0.0, -1.0, -1e12):
        v = budget(1.0, 0.0, 0.3, Z2)
        assert not v["closes"], f"Z_2 = {Z2} produced a closing certificate: {v}"
        assert math.isnan(v["r_min"]), f"Z_2 = {Z2} should give r_min = nan, got {v['r_min']}"
    print("  holds: Z_2 <= 0 is the one domain check budget() does perform")


def test_holds_nonintegrable_alpha_refuses_instead_of_inventing_a_constant():
    """HOLDS.  For `alpha <= 1` the far-field mass `int (1+y^2)^{-alpha/2} dy` diverges, so
    `M_alpha` has no referent.  `cos_power_mass` RAISES rather than returning the value a
    truncated quadrature would produce -- discipline 73 already implemented, and it must not
    be softened into a fallback."""
    for alpha in (0.5, 0.9, 1.0):
        try:
            cos_power_mass(alpha)
            raise AssertionError(f"cos_power_mass({alpha}) returned instead of raising")
        except AssertionError:
            raise
        except Exception:
            pass
        try:
            quadratic_constant_upper(alpha, 0.5, n_X=8, n_quad=201)
            raise AssertionError(
                f"quadratic_constant_upper({alpha}) returned instead of raising")
        except AssertionError:
            raise
        except Exception:
            pass
    print("  holds: alpha <= 1 refuses in cos_power_mass and in quadratic_constant_upper")


def test_holds_gamma_zero_raises_rather_than_returning_a_number():
    """HOLDS.  The near-field half carries a `1/gamma`; `gamma = 0` must raise, not return."""
    try:
        hilbert_farfield_bound(10.0, 1.5, 0.0)
        raise AssertionError("gamma = 0 returned a bound instead of raising")
    except AssertionError:
        raise
    except ZeroDivisionError:
        pass
    print("  holds: gamma = 0 raises ZeroDivisionError")


def test_holds_bounds_are_sound_across_the_whole_live_operating_range():
    """HOLDS, and it is the load-bearing reassurance of this leg.  Every defect family B
    finds is OUTSIDE the range the in-repo callers use.  Inside it -- alpha in [1.1, 1.9],
    gamma in [0.15, 0.9], X0 in [200, 3200], X out to 3.2e7 -- the module's numerically
    evaluated bounds DOMINATE the independent reference, with a small positive slack.  If
    this ever fails, a real certificate in this repository is affected."""
    worst = 0.0
    for alpha in (1.1, 1.5, 1.9):
        for gamma in (0.15, 0.5, 0.9):
            for X0 in (200.0, 3200.0):
                m = farfield_modelling_error_bound(alpha, gamma, X0)
                ref, _ = _reference_sup(alpha, gamma, X0, decades=12, n_X=24)
                worst = max(worst, ref / m["bound"])
                assert ref <= m["bound"], (
                    f"the claimed upper bound fell BELOW the reference inside the live "
                    f"range: alpha={alpha} gamma={gamma} X0={X0}, "
                    f"module={m['bound']} < reference={ref}")
    for alpha in (1.2, 1.5, 1.9):
        for X in (1.0, 1e2, 1e4, LIVE_X_MAX):
            assert _I_out(X, alpha) >= _I_out_reference(X, alpha), (
                f"_I_out fell below the reference inside the live range at "
                f"alpha={alpha}, X={X}")
    assert worst < 1.0, f"expected strict domination inside the live range, worst ratio {worst}"
    print(f"  holds: bounds dominate across the live range, worst reference/module {worst:.6f}")


# ===========================================================================
# GAP-PIN gates -- the defects, pinned so they cannot drift while awaiting repair
# ===========================================================================


def test_gap_a_planted_non_solution_survives_inside_a_reported_certified_ball():
    """GAP-PIN, and it is leg 116's headline -- the gate's question, answered YES.

    `F(x) = x^2 - 2`, zeros exactly `+-sqrt(2)`.  The planted point `x = 1.0` is not one:
    `|F(1.0)| = 1` and the nearest zero is `0.4142...` away.  Honest constants there REFUSE
    (asserted in the control above).  A single H1 violation -- `Z_0 = -1`, which the published
    theorem forbids because `Z_0` is a norm -- makes `budget` report `closes=True` with
    `r_min = 0.09587`, i.e. the certified ball `[0.8083, 1.1917]`.  That ball contains NO zero
    of `F`: it misses `sqrt(2)` by 1.161 ball radii.

    INVERSION WHEN REPAIRED: assert `closes is False` with a reason naming the violated
    hypothesis.  Do NOT weaken the ball arithmetic -- it is the finding."""
    honest = _p_constants(P_XPLANT)
    assert not budget(**honest)["closes"], "the control must refuse before the poison is read"

    c = dict(honest); c["Z0"] = -1.0
    v = budget(**c)
    assert v["closes"], ("GOOD NEWS, BAD TEST: a negative Z_0 is now rejected. INVERT this "
                         f"gate -- assert refusal with a reason. Got {v}")
    ball = _ball_report(P_XPLANT, v)
    assert ball["contains_a_zero"] is False, (
        f"expected a certified ball with no zero of F inside it, got {ball}")
    assert abs(v["r_min"] - 0.19169540264054277) < 1e-12, (
        f"the pinned radius moved: {v['r_min']!r}")
    assert abs(ball["gap_in_ball_radii"] - 1.1607902780527646) < 1e-9, (
        f"the pinned miss distance moved: {ball['gap_in_ball_radii']!r} ball radii")
    print(f"  GAP: certified ball [{ball['ball_lo']:.4f}, {ball['ball_hi']:.4f}] around the "
          f"planted non-solution 1.0 holds NO zero; misses sqrt(2) by "
          f"{ball['gap_in_ball_radii']:.3f} ball radii")


def test_gap_fabricated_zero_residual_certifies_the_planted_point_itself():
    """GAP-PIN.  A residual reported as exactly zero (leg 98's `A1` case, in this module)
    makes `budget` return `closes=True` with `r_min = 0.0` -- a certified "ball" that is
    exactly the planted non-solution, whose true residual is 1.  A denormal-scale fabricated
    `Y_0` does the same.

    INVERSION WHEN REPAIRED: `Y_0 = 0` may legitimately close (`x_bar` is then an exact zero),
    so the repair to assert here is on `r_min`: a `closes=True` must carry `r_min > 0`, or the
    verdict must state that the centre is claimed to BE the zero."""
    for Y0 in (0.0, 1e-300):
        c = dict(_p_constants(P_XPLANT)); c["Y0"] = Y0
        v = budget(**c)
        assert v["closes"], (f"GOOD NEWS, BAD TEST: a fabricated Y_0 = {Y0} is now rejected. "
                             f"INVERT this gate. Got {v}")
        assert v["r_min"] < 1e-290, f"expected a ~zero radius, got {v['r_min']}"
        ball = _ball_report(P_XPLANT, v)
        assert ball["contains_a_zero"] is False, f"expected no zero in the ball: {ball}"
    print("  GAP: Y_0 = 0 and Y_0 = 1e-300 both certify a zero-radius ball on a non-solution")


def test_gap_negative_Y0_yields_a_closing_certificate_with_a_negative_radius():
    """GAP-PIN.  A sign-flipped residual makes the discriminant LARGER, so `closes=True`
    while `r_min < 0` -- the theorem's conclusion asserted over an empty set.

    INVERSION WHEN REPAIRED: assert refusal, and keep the `r_min < 0` check as the thing the
    repair must make unreachable."""
    for Y0 in (-1.0, -1e-12, -1e12, -INF):
        v = budget(Y0, 0.0, 0.3, 1.0)
        assert v["closes"], (f"GOOD NEWS, BAD TEST: Y_0 = {Y0} is now rejected. INVERT this "
                             f"gate. Got {v}")
        assert v["r_min"] < 0.0, f"expected a negative r_min for Y_0 = {Y0}, got {v['r_min']}"
    honest = budget(1.0, 0.0, 0.3, 1.0)
    assert not honest["closes"], "the |Y_0| counterpart must not close"
    print("  GAP: Y_0 in {-1, -1e-12, -1e12, -inf} all close, all with r_min < 0")


def test_gap_negative_Z0_or_Z1_rescues_a_hopeless_certificate():
    """GAP-PIN.  `Z_0` and `Z_1` are suprema of operator norms, so negative values are outside
    the theorem.  `budget` treats them as extra contraction budget: a case that honestly
    cannot close does close once one of them goes negative.

    INVERSION WHEN REPAIRED: assert refusal for each, naming the nonnegativity hypothesis."""
    hopeless = {"Y0": 1.0, "Z0": 0.0, "Z1": 0.3, "Z2": 1.0}
    assert not budget(**hopeless)["closes"], "the honest counterpart must not close"
    for slot, val in (("Z0", -1e6), ("Z1", -1.0), ("Z1", -1e6)):
        c = dict(hopeless); c[slot] = val
        v = budget(**c)
        assert v["closes"], (f"GOOD NEWS, BAD TEST: {slot} = {val} no longer rescues a "
                             f"hopeless certificate. INVERT this gate. Got {v}")
        assert v["r_min"] > 0.0, f"expected a positive radius for {slot}={val}: {v}"
    print("  GAP: negative Z_0 / Z_1 buy a closing certificate the honest constants refuse")


def test_gap_supremum_is_a_max_over_a_truncated_window_outside_the_documented_scope():
    """GAP-PIN.  `farfield_modelling_error_bound` returns `max` over 40 samples of
    `[X0, 1e4 X0]` as a supremum over `{X >= X0}`.  The module's docstring states the
    hypothesis that makes this legitimate -- "For alpha < 2 both terms decay, so the
    supremum sits at X0" -- but nothing enforces `alpha < 2`.  At `alpha = 2.5` the claimed
    bound is ~1e4x below the truth and at `alpha = 3.0` ~1e8x, and the function's OWN
    `argmax_X` pins to the window's last sample in every failing case: a self-diagnostic it
    computes and discards.

    LATENT: the in-repo callers use `alpha in [1.1, 1.8]`, so no banked number is affected --
    asserted by `test_holds_bounds_are_sound_across_the_whole_live_operating_range`.

    INVERSION WHEN REPAIRED: assert that `alpha >= 2` raises, or that the returned dict
    carries a flag when `argmax_X` lands on the window boundary."""
    for alpha, floor in ((2.25, 50.0), (2.5, 5e3), (3.0, 5e7)):
        m = farfield_modelling_error_bound(alpha, 0.5, 1.0)
        ref, ref_X = _reference_sup(alpha, 0.5, 1.0, decades=12, n_X=24)
        ratio = ref / m["bound"]
        assert ratio > floor, (
            f"GOOD NEWS, BAD TEST: alpha={alpha} now under-reports by only {ratio:.4g}x "
            f"(was > {floor}x). If a guard landed, INVERT this gate.")
        assert abs(m["argmax_X"] - 1e4) < 1e-6, (
            f"expected argmax pinned at the window end 1e4, got {m['argmax_X']}")
        assert ref_X > 1e4, f"the reference should find its max beyond the window: {ref_X}"
    inside = farfield_modelling_error_bound(1.9, 0.5, 1.0)
    assert abs(inside["argmax_X"] - 1.0) < 1e-9, (
        f"inside the documented scope the argmax must sit at X0, got {inside['argmax_X']}")
    print("  GAP: alpha=2.25/2.5/3.0 under-report by >50x / >5e3x / >5e7x, argmax pinned "
          "at the window end; alpha=1.9 keeps its argmax at X0")


def test_gap_Iout_log_grid_floor_undercuts_the_truth_past_X_1e11():
    """GAP-PIN, and the mechanism is measured rather than asserted.  `_I_out` grades its bulk
    panel `[0, X/2]` logarithmically from `eps = 1e-12 * max(X, 1)`, joined to `y = 0` by one
    trapezoid.  The integrand's mass sits at `y = O(1)`, so once `eps` reaches that scale the
    single panel `[0, eps]` replaces the resolved mass region.  The claimed UPPER bound then
    falls BELOW the truth: by 2.12% at `alpha = 1.9, X = 1e12`, with onset already at
    `X = 1e11`.  Past `X ~ 1e13` the same panel over-shoots instead, by up to ~30x -- the
    conservative direction, and the reason this cannot be found by looking at large X alone.

    LATENT: the largest `X` any in-repo caller evaluates is `3.2e7` (X0 <= 3200, window
    `1e4 X0`), 3.49 decades below the onset, where the module keeps a `+8.4e-5` relative
    slack.

    INVERSION WHEN REPAIRED: assert domination at `X = 1e11 .. 1e13` too, and keep the
    `X = 1e12` point -- it is the worst case."""
    m, r = _I_out(1e12, 1.9), _I_out_reference(1e12, 1.9)
    assert m < r, ("GOOD NEWS, BAD TEST: _I_out now dominates the truth at alpha=1.9, "
                   f"X=1e12. INVERT this gate. module={m}, reference={r}")
    under = r / m - 1.0
    assert abs(under - 0.021237) < 5e-4, f"the pinned 2.12% under-report moved: {under}"
    assert _I_out(1e11, 1.9) < _I_out_reference(1e11, 1.9), (
        "the onset at X=1e11 disappeared -- if a repair landed, INVERT this gate")
    # and the safe side, which is what keeps the finding latent
    assert _I_out(LIVE_X_MAX, 1.9) > _I_out_reference(LIVE_X_MAX, 1.9), (
        "the live range must stay on the dominating side of the crossover")
    print(f"  GAP: _I_out falls {100 * under:.3f}% below the truth at X=1e12; live range "
          f"(X<=3.2e7) is 3.49 decades clear")


def test_gap_gamma_outside_the_holder_range_reduces_the_claimed_bound():
    """GAP-PIN.  `gamma` is a Holder exponent in `(0, 1]`.  The near-field half carries a
    `1/gamma`, so a negative `gamma` flips that half's sign and DROPS the claimed upper
    bound below the `gamma = 0.5` value -- an unguarded domain, not a conservative one.

    INVERSION WHEN REPAIRED: assert that `gamma <= 0` raises."""
    ref = hilbert_farfield_bound(10.0, 1.5, 0.5)[0]
    for gamma in (-0.5, -0.05):
        b, near, _ = hilbert_farfield_bound(10.0, 1.5, gamma)
        assert near < 0.0, (f"GOOD NEWS, BAD TEST: gamma={gamma} no longer produces a "
                            f"negative near-field part ({near}). INVERT this gate.")
        assert b < ref, f"expected the bound to drop below the gamma=0.5 value {ref}, got {b}"
    print(f"  GAP: gamma=-0.5 gives a negative near-field part and a bound below the "
          f"gamma=0.5 reference {ref:.4e}")


def test_gap_two_point_dual_drops_nonpositive_kernel_entries_instead_of_flagging_them():
    """GAP-PIN, with its reachability stated.  `two_point_dual` computes
    `1/q if q > 0 else 0`.  On the DIAGONAL that is correct -- the suppressed increment is
    genuinely zero.  Off it, an entry that is zero or negative has an honest contribution of
    `+inf`, and substituting `0` makes that reference index artificially cheap, so the `min`
    over `m0` selects it.  A negative codomain sup weight does the same through the other
    term.  Measured: 2.19x and 3.57x below the honest bound on a 6-point instance.

    CRAFTED-ONLY.  `HolderNorm`, the module's own weight source, produces a minimum
    off-diagonal kernel entry of 3.58e-01 and a minimum weight of 1.0 across
    `J in {125, 250, 500}` and `(alpha, gamma)` spanning the live range -- so no in-repo path
    reaches this.  Reported as latent, not as an active fabrication.

    INVERSION WHEN REPAIRED: assert that a non-positive off-diagonal `q_cod` entry, or any
    non-positive `v_cod` entry, raises or yields `+inf`."""
    cases, reach = family_C()
    by_name = {c["case"]: c for c in cases}
    base = by_name["C00_control_wellformed"]["bound"]
    for name, floor in (("C01_q_column_zeroed", 2.0), ("C04_v_one_negative", 3.0)):
        c = by_name[name]
        assert c["outcome"] == "false_bound", (
            f"GOOD NEWS, BAD TEST: {name} is no longer accepted. INVERT this gate. Got {c}")
        assert c["honest_over_reported"] > floor, (
            f"{name}: expected the reported bound to sit >{floor}x below the honest "
            f"{base}, got ratio {c['honest_over_reported']}")
    # reachability -- the half that keeps this latent, and that a repair must not break
    for row in reach:
        assert row["n_offdiagonal_nonpositive"] == 0, (
            f"HolderNorm now produces a non-positive off-diagonal kernel entry: {row}")
        assert row["n_w_nonpositive"] == 0, f"HolderNorm now produces a non-positive w: {row}"
        assert row["min_offdiagonal_pair"] > 0.3, f"kernel floor moved: {row}"
    print("  GAP: nonpositive q_cod / v_cod drop the dual bound 2.19x / 3.57x; NOT reachable "
          "from HolderNorm (min off-diagonal kernel 3.58e-01, min weight 1.0)")


# ===========================================================================


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for t in tests:
            print(t.__name__)
            t()
    print(f"\nALL {len(tests)} ADVERSARIAL GATES PASS "
          f"(leg 116 -- the GAP-PIN gates assert DEFECTS, not correctness)")


if __name__ == "__main__":
    main()
