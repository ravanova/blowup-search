"""ADVERSARIAL gates for solver/nk_bounds.py -- Route-NKA (leg 116, measured) and
Route-NKR (leg 128, REPAIRED and pins inverted).

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

**LEG 128 LANDED THE REPAIR, AND THIS FILE IS ITS RECORD.**  Leg 116 was read-only on
`solver/nk_bounds.py` under both branches of its gate.  Leg 128 (Route-NKR) then closed the
gap with ONE guard shared by all three certificate-assembly modules
(`solver/certificate_guards.py`), rather than a third private copy of legs 79/98's function,
and **inverted every GAP-PIN gate below in the same commit** -- which is what those pins were
for.  Post-repair, of leg 116's 21 false accepts **17 reject and 4 remain**, and the 4 are a
named class, not a leftover: their constants are nonnegative and finite, so they SATISFY the
theorem's hypotheses and lie about a MAGNITUDE instead.  No hypothesis guard can see that.

So the gates below split into four kinds, stated in each docstring:

  * **REPAIRED gates** (`test_repaired_*`) are leg 116's GAP-PINs, inverted exactly as each
    pin's own docstring prescribed.  The pre-repair magnitude is kept in every docstring: a
    repaired defect whose size is forgotten is one that can come back at a different size.
  * **STILL-A-GAP gates** (`test_still_a_gap_*`) are the two clauses leg 128 did NOT close in
    value, marked rather than dropped -- `_I_out`'s log-grid floor (closed as a WARNING,
    because lowering it moves clean values: 15/15 live-range values move, worst 1.08e-04
    relative) and the fabricated-magnitude class above.  Each names what would close it.
  * **HOLDS gates** assert the checks that were ALREADY in place and must never regress --
    the NaN and `+inf` rejections in `budget`, the `alpha <= 1` refusal in `cos_power_mass`,
    and the `gamma = 0` refusal (now a named `ValueError`, formerly a bare
    `ZeroDivisionError`; the intent is pinned, the exception type no longer is).
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
    """HOLDS.  The near-field half carries a `1/gamma`; `gamma = 0` must raise, not return.

    THE INTENT IS UNCHANGED; THE EXCEPTION TYPE IMPROVED (leg 128).  Before the repair this
    was a bare `ZeroDivisionError` from inside the arithmetic -- sound, but leg 98's B20/B21
    lesson applies: a caller with a broad `except` turns an anonymous arithmetic error into a
    silent skip.  It is now a `ValueError` raised at the top of the function, naming `gamma`
    and its range.  This gate asserts what it always meant -- gamma = 0 REFUSES rather than
    returning a number -- and no longer pins the type it refuses with."""
    try:
        hilbert_farfield_bound(10.0, 1.5, 0.0)
    except AssertionError:
        raise
    except (ValueError, ZeroDivisionError) as ex:
        assert "gamma" in str(ex) or isinstance(ex, ZeroDivisionError), str(ex)
    else:
        raise AssertionError("gamma = 0 returned a bound instead of raising")
    print("  holds: gamma = 0 refuses (now a named ValueError, was ZeroDivisionError)")


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
# REPAIRED gates -- leg 116's GAP-PINs, INVERTED (leg 128)
# ===========================================================================
#
# Each gate below was a GAP-PIN asserting a DEFECT, and each named its own inversion in its
# docstring.  Leg 128 landed the shared guard (`solver/certificate_guards.py`) and these are
# those named inversions, applied verbatim -- not weakened, not deleted.  The original
# magnitudes are kept in the docstrings, because a repaired defect whose size is forgotten
# is a defect that can come back at a different size (lesson 68).
#
# TWO PINS SURVIVE AS PINS, and they are marked STILL-A-GAP rather than quietly dropped:
# `_I_out`'s bulk floor (closed in the FLAG sense, because lowering it moves clean values)
# and the fabricated-MAGNITUDE class (structurally undetectable by any hypothesis guard).


def test_repaired_planted_non_solution_no_longer_survives_a_certified_ball():
    """INVERTED (was `test_gap_a_planted_non_solution_survives_...`), leg 116's headline.

    `F(x) = x^2 - 2`, zeros exactly `+-sqrt(2)`; the planted point `x = 1.0` is not one.
    BEFORE: a single `Z_0 = -1` -- forbidden, because `Z_0` is a norm -- made `budget` report
    `closes=True` with `r_min = 0.19169540264054277`, i.e. the certified ball
    `[0.8083, 1.1917]`, which contains NO zero of `F` and misses `sqrt(2)` by
    1.1607902780527646 ball radii.  AFTER: rejected by hypothesis, with the violation naming
    `Z_0`.

    The ball arithmetic is NOT weakened -- it is asserted unreachable instead."""
    honest = _p_constants(P_XPLANT)
    assert not budget(**honest)["closes"], "the control must refuse before the poison is read"

    c = dict(honest); c["Z0"] = -1.0
    v = budget(**c)
    assert v["closes"] is False, f"a negative Z_0 must be REFUSED, got {v}"
    assert any("Z_0" in s and "negative" in s for s in v["violations"]), (
        f"the refusal must name Z_0's nonnegativity hypothesis, got {v['violations']}")
    assert v["reason"].startswith("INVALID_INPUT"), v["reason"]
    assert math.isnan(v["r_min"]), f"a rejected input must carry no radius, got {v['r_min']}"
    # and the ball the old defect produced is now unreachable
    ball = _ball_report(P_XPLANT, v)
    assert ball["ball_lo"] is None and ball["radius"] is None, (
        f"no ball may be reported for a rejected input: {ball}")
    print("  REPAIRED: Z_0 = -1 is refused by hypothesis; the old certified ball "
          "[0.8083, 1.1917] (missing sqrt(2) by 1.161 radii) is unreachable")


def test_still_a_gap_fabricated_MAGNITUDE_is_not_detectable_by_a_hypothesis_guard():
    """STILL A GAP, and it is the honest residue of leg 128's repair.

    Leg 116's pin named its own inversion: "`Y_0 = 0` may legitimately close (`x_bar` is then
    an exact zero), so the repair to assert here is on `r_min`: a `closes=True` must carry
    `r_min > 0`, OR the verdict must state that the centre is claimed to BE the zero."  Leg
    128 took the SECOND branch, because the first is not available: refusing `r_min <= 0`
    would refuse the banked clean gate `test_nk_bounds.py::test_decay_and_budget`
    (`budget(0.0, 1e-12, 0.3, 13.0)`, whose `r_min` is exactly 0.0), and every in-repo caller
    passes `Y_0 = 0.0` literally.  So the verdict now SAYS SO: `degenerate_ball=True` plus a
    `reason` naming which of the two mechanisms produced it.

    THE RESIDUE, STATED AS A CLASS: `Y_0 = 0.0` and `Y_0 = 1e-300` are nonnegative and finite,
    so they SATISFY the theorem's hypotheses.  The fabrication is in the VALUE, not the type,
    and no validation layer can see it -- `solver/interval_certificate.py`'s own docstring
    states the general fact ("Validity checking cannot catch this and no amount of it ever
    will").  4 of leg 116's 21 false accepts are this class; 17 now reject.

    INVERSION WHEN CLOSED: it cannot be closed here.  It would need the CALLER to certify that
    `Y_0` came from a residual evaluation rather than a literal."""
    for Y0 in (0.0, 1e-300):
        c = dict(_p_constants(P_XPLANT)); c["Y0"] = Y0
        v = budget(**c)
        assert v["closes"], f"a hypothesis-satisfying Y_0 = {Y0} must still be evaluated: {v}"
        assert v["r_min"] < 1e-290, f"expected a ~zero radius, got {v['r_min']}"
        assert v["degenerate_ball"] is True, (
            f"the repair's whole content here is the FLAG; it is missing for Y_0={Y0}: {v}")
        assert "DEGENERATE_BALL" in v["reason"], v["reason"]
        if Y0 == 0.0:
            assert "honest zero-residual case" in v["reason"], v["reason"]
        else:
            assert "below float resolution" in v["reason"], v["reason"]
    # the Z_2 half of the same class: a magnitude under-reported by six decades
    c = dict(_p_constants(P_XPLANT)); c["Z2"] = 1e-6
    v = budget(**c)
    assert v["closes"], f"Z_2 = 1e-6 is hypothesis-satisfying and must be evaluated: {v}"
    assert v["degenerate_ball"] is False, v
    print("  STILL A GAP (by construction): Y_0 in {0, 1e-300} and Z_2 = 1e-6 satisfy the "
          "hypotheses and lie about the MAGNITUDE; now flagged degenerate where the ball is, "
          "but not detectable -- 4 of leg 116's 21 false accepts, 17 rejected")


def test_repaired_negative_Y0_is_refused_and_a_negative_radius_is_unreachable():
    """INVERTED (was `test_gap_negative_Y0_yields_a_closing_certificate_with_a_negative_radius`).

    BEFORE: a sign-flipped residual made the discriminant LARGER, so `closes=True` with
    `r_min < 0` -- the theorem's conclusion asserted over an empty set, for every one of
    `Y_0 in {-1, -1e-12, -1e12, -inf}`.  AFTER: all four refused by hypothesis, and the
    `r_min < 0` check is kept as the thing the repair makes unreachable."""
    for Y0 in (-1.0, -1e-12, -1e12, -INF):
        v = budget(Y0, 0.0, 0.3, 1.0)
        assert v["closes"] is False, f"Y_0 = {Y0} must be refused, got {v}"
        assert any("Y_0" in s for s in v["violations"]), v["violations"]
        assert not (v["r_min"] < 0.0), (
            f"a negative radius must be unreachable, got {v['r_min']} for Y_0 = {Y0}")
    honest = budget(1.0, 0.0, 0.3, 1.0)
    assert not honest["closes"], "the |Y_0| counterpart must still not close"
    print("  REPAIRED: Y_0 in {-1, -1e-12, -1e12, -inf} all refused; r_min < 0 unreachable")


def test_repaired_negative_Z0_or_Z1_no_longer_rescues_a_hopeless_certificate():
    """INVERTED (was `test_gap_negative_Z0_or_Z1_rescues_a_hopeless_certificate`).

    BEFORE: `Z_0` and `Z_1` are suprema of operator norms, and `budget` treated negative
    values as extra contraction budget -- a case that honestly cannot close did close once
    either went negative (`Z_0 = -1e6`, `Z_1 = -1.0`, `Z_1 = -1e6`), each with `r_min > 0`.
    AFTER: refused, naming the nonnegativity hypothesis, ahead of the contraction test --
    which matters, because a negative `Z_0`/`Z_1` PASSES `Z_0 + Z_1 < 1`."""
    hopeless = {"Y0": 1.0, "Z0": 0.0, "Z1": 0.3, "Z2": 1.0}
    assert not budget(**hopeless)["closes"], "the honest counterpart must not close"
    for slot, val, name in (("Z0", -1e6, "Z_0"), ("Z1", -1.0, "Z_1"), ("Z1", -1e6, "Z_1")):
        c = dict(hopeless); c[slot] = val
        v = budget(**c)
        assert v["closes"] is False, f"{slot} = {val} must be refused, got {v}"
        assert any(name in s and "negative" in s for s in v["violations"]), (
            f"{slot}={val}: the refusal must name {name}'s nonnegativity, "
            f"got {v['violations']}")
        # the contraction test alone would NOT have caught it -- why the guard runs first
        assert (1.0 - c["Z0"] - c["Z1"]) > 0.0, (
            f"{slot}={val} passes Z_0 + Z_1 < 1; the hypothesis guard is what rejects it")
    print("  REPAIRED: negative Z_0 / Z_1 refused by hypothesis, ahead of the contraction "
          "test they would otherwise pass")


def test_repaired_alpha_at_or_above_2_raises_and_the_window_end_is_flagged():
    """INVERTED (was `test_gap_supremum_is_a_max_over_a_truncated_window_...`).

    BEFORE: `farfield_modelling_error_bound` returned `max` over 40 samples of `[X0, 1e4 X0]`
    as a supremum over `{X >= X0}` with nothing enforcing the `alpha < 2` hypothesis its own
    docstring states.  The claimed bound sat >50x below the truth at `alpha = 2.25`, >5e3x at
    `2.5` and >5e7x at `3.0`, and the function's OWN `argmax_X` pinned to the window's last
    sample in every failing case -- a self-diagnostic it computed and discarded.

    AFTER: `alpha >= 2` raises `ValueError`, and `argmax_at_window_end` is returned so a
    caller INSIDE the hypothesis can still see a window that ran out.  Both halves of the
    named inversion, not one."""
    for alpha in (2.0, 2.25, 2.5, 3.0):
        try:
            farfield_modelling_error_bound(alpha, 0.5, 1.0)
        except ValueError as ex:
            assert "alpha" in str(ex) and "supremum" in str(ex), str(ex)
        else:
            raise AssertionError(f"alpha = {alpha} must raise, it did not")
    inside = farfield_modelling_error_bound(1.9, 0.5, 1.0)
    assert abs(inside["argmax_X"] - 1.0) < 1e-9, (
        f"inside the documented scope the argmax must sit at X0, got {inside['argmax_X']}")
    assert inside["argmax_at_window_end"] is False, inside["argmax_at_window_end"]
    # the self-diagnostic must be able to come out TRUE, or it is not a diagnostic (lesson 90)
    narrow = farfield_modelling_error_bound(1.9, 0.5, 1.0, Xmax_factor=1.0, n_X=3)
    assert narrow["argmax_at_window_end"] is True, (
        f"a zero-width window must flag its own boundary: {narrow['argmax_at_window_end']}")
    print("  REPAIRED: alpha >= 2 raises; argmax_at_window_end returned, False at alpha=1.9 "
          "and True on a degenerate window (the flag can come out both ways)")


def test_still_a_gap_Iout_log_grid_floor_undercuts_the_truth_past_X_1e11_but_now_WARNS():
    """STILL A GAP in value, CLOSED as a flag (was `test_gap_Iout_log_grid_floor_...`).

    `_I_out` grades its bulk panel `[0, X/2]` logarithmically from `eps = 1e-12 * max(X, 1)`.
    The integrand's mass sits at `y = O(1)`, so once `eps` reaches that scale the single panel
    `[0, eps]` replaces the resolved mass region and the claimed UPPER bound falls BELOW the
    truth -- by 2.12% at `alpha = 1.9, X = 1e12`, onset at `X = 1e11`.

    WHY IT IS NOT RECOMPUTED, MEASURED RATHER THAN ASSERTED: lowering the floor rebuilds the
    geomspace grid, so it moves clean values.  Leg 128 measured 15/15 live-range values moving
    (worst 1.08e-04 relative) when `eps` goes 1e-12 -> 1e-18, and any clean-input result moving
    is this leg's own stop condition.  So the value is untouched and the out-of-range regime
    WARNS instead, above a validated ceiling of `X = 1e10`.

    LATENT: the largest `X` any in-repo caller evaluates is `3.2e7`, 3.49 decades below onset.

    INVERSION WHEN CLOSED FOR REAL: assert domination at `X = 1e11 .. 1e13`, keep the
    `X = 1e12` point (the worst case), and delete the warning assertions below."""
    m, r = _I_out(1e12, 1.9), _I_out_reference(1e12, 1.9)
    assert m < r, ("GOOD NEWS, BAD TEST: _I_out now dominates the truth at alpha=1.9, "
                   f"X=1e12. INVERT this gate. module={m}, reference={r}")
    under = r / m - 1.0
    assert abs(under - 0.021237) < 5e-4, f"the pinned 2.12% under-report moved: {under}"
    assert _I_out(1e11, 1.9) < _I_out_reference(1e11, 1.9), (
        "the onset at X=1e11 disappeared -- if a repair landed, INVERT this gate")
    # the safe side, which is what keeps the finding latent
    assert _I_out(LIVE_X_MAX, 1.9) > _I_out_reference(LIVE_X_MAX, 1.9), (
        "the live range must stay on the dominating side of the crossover")
    # THE REPAIR'S OWN CONTENT: the regime is now announced, and only that regime.
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        _I_out(1e12, 1.9)
    assert any(issubclass(x.category, RuntimeWarning) and "validated ceiling" in str(x.message)
               for x in w), f"X = 1e12 must warn, got {[str(x.message) for x in w]}"
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        _I_out(LIVE_X_MAX, 1.9)
    assert not w, f"the live range must NOT warn, got {[str(x.message) for x in w]}"
    print(f"  STILL A GAP (flagged, not recomputed): _I_out falls {100 * under:.3f}% below the "
          f"truth at X=1e12 and now WARNS above X=1e10; live range (X<=3.2e7) is 3.49 decades "
          f"clear and stays silent")


def test_repaired_gamma_outside_the_holder_range_raises():
    """INVERTED (was `test_gap_gamma_outside_the_holder_range_reduces_the_claimed_bound`).

    BEFORE: `gamma` is a Holder exponent in `(0, 1]`, and the near-field half carries a
    `1/gamma`, so `gamma = -0.5` and `-0.05` flipped that half's sign and DROPPED the claimed
    upper bound below the honest `gamma = 0.5` value.  AFTER: `gamma <= 0` raises, as the pin's
    own inversion prescribed -- and so does `gamma > 1`, which is outside the range for the
    same reason and was equally unguarded."""
    ref = hilbert_farfield_bound(10.0, 1.5, 0.5)[0]
    assert ref > 0.0, ref
    for gamma in (-0.5, -0.05, 0.0, 1.5, 3.0):
        try:
            hilbert_farfield_bound(10.0, 1.5, gamma)
        except ValueError as ex:
            assert "gamma" in str(ex) and "(0, 1]" in str(ex), str(ex)
        else:
            raise AssertionError(f"gamma = {gamma} must raise, it did not")
    # the endpoints of the admissible range must still WORK, or the guard over-rejects
    for gamma in (1e-6, 0.5, 1.0):
        b = hilbert_farfield_bound(10.0, 1.5, gamma)[0]
        assert b > 0.0 and math.isfinite(b), f"gamma = {gamma} is admissible: {b}"
    print("  REPAIRED: gamma in {-0.5, -0.05, 0, 1.5, 3.0} raise; gamma in {1e-6, 0.5, 1.0} "
          "still evaluate (the guard rejects the range, not the function)")


def test_repaired_two_point_dual_raises_on_nonpositive_kernel_or_weight_entries():
    """INVERTED (was `test_gap_two_point_dual_drops_nonpositive_kernel_entries_...`).

    BEFORE: `two_point_dual` computes `1/q if q > 0 else 0`, which is correct on the DIAGONAL
    (the suppressed increment is genuinely zero) and a silent fabrication off it: an entry that
    is zero or negative has an honest contribution of `+inf`, and substituting `0` makes that
    reference index artificially cheap so the `min` over `m0` selects it.  Measured 2.19x
    (zeroed `q` column) and 3.57x (negative `v_cod` entry) BELOW the honest bound.  AFTER: both
    raise `ValueError`, as the pin's own inversion prescribed.

    CRAFTED-ONLY, AND THE REPAIR MUST NOT BREAK THAT: `HolderNorm`, the module's own weight
    source, has a minimum off-diagonal kernel entry of 3.58e-01 and a minimum weight of 1.0
    across `J in {125, 250, 500}` and the live `(alpha, gamma)` range, so no in-repo path
    reaches the guard -- asserted below, exactly as leg 116 asserted it."""
    cases, reach = family_C()
    by_name = {c["case"]: c for c in cases}
    assert by_name["C00_control_wellformed"]["outcome"] == "sound", (
        "the well-formed control must still compute -- a guard that rejects everything is "
        "not a repair")
    for name in ("C01_q_column_zeroed", "C02_q_column_negative",
                 "C03_q_single_offdiagonal_zero", "C04_v_one_negative", "C05_v_one_zero",
                 "C06_v_one_nan"):
        c = by_name[name]
        assert c["outcome"] == "raised", f"{name} must now raise, got {c}"
        assert "ValueError" in c["exception"], f"{name}: {c['exception']}"
        assert "do not come from a norm" in c["exception"], f"{name}: {c['exception']}"
    # reachability -- the half that keeps this latent, and that the repair must not break
    for row in reach:
        assert row["n_offdiagonal_nonpositive"] == 0, (
            f"HolderNorm now produces a non-positive off-diagonal kernel entry: {row}")
        assert row["n_w_nonpositive"] == 0, f"HolderNorm now produces a non-positive w: {row}"
        assert row["min_offdiagonal_pair"] > 0.3, f"kernel floor moved: {row}"
    print("  REPAIRED: nonpositive/NaN q_cod and v_cod entries raise (they dropped the dual "
          "bound 2.19x / 3.57x); still NOT reachable from HolderNorm, and the well-formed "
          "control still computes")


def test_repaired_all_three_modules_share_one_guard():
    """NEW, and it is the clause that makes this a class repair rather than a third one-off.

    `port_certification.py` (leg 79), `interval_certificate.py` (leg 98) and `nk_bounds.py`
    (leg 128) now call the SAME function object.  Checked by identity, not by resemblance --
    and then checked BEHAVIOURALLY, because identity alone would not catch a call site that
    holds the shared function and ignores it."""
    import solver.certificate_guards as cg
    import solver.interval_certificate as ic
    import solver.nk_bounds as nk
    import solver.port_certification as pc

    assert pc._shared_hypothesis_violations is cg.hypothesis_violations
    assert ic._shared_hypothesis_violations is cg.hypothesis_violations
    assert nk.hypothesis_violations is cg.hypothesis_violations

    # behaviour: the same violating constants must be refused by all three, naming the same
    # constants for the same reasons.
    for (Y0, Z1, Z2) in ((-1.0, 0.3, 1.0), (NAN, 0.3, 1.0), (INF, 0.3, 1.0),
                         (1e-6, -1.0, 1.0), (1e-6, 0.3, -1.0)):
        vp = pc.radii_polynomial_status(Y0, Z1, Z2)
        vi = ic.radii_verdict(Y0, Z1, Z2)
        vn = nk.budget(Y0, 0.0, Z1, Z2)
        assert vp["status"] == "INVALID_INPUT" and vp["closes"] is False, vp
        assert vi["closes"] is False and vi["reason"].startswith("INVALID_INPUT"), vi
        assert vn["closes"] is False and vn["reason"].startswith("INVALID_INPUT"), vn
        assert len(vp["violations"]) == len(vi["violations"]) == len(vn["violations"]), (
            f"the three pipelines disagree on how many hypotheses {(Y0, Z1, Z2)} breaks: "
            f"{vp['violations']} / {vi['violations']} / {vn['violations']}")
    # the documented differences must SURVIVE -- flattening them would be the wrong abstraction
    assert pc._hypothesis_violations(None, None, None) == [], (
        "port_certification's None-is-NOT-MEASURED kill-switch must survive the shared guard")
    try:
        ic._hypothesis_violations(None, 0.3, 1.0)
    except TypeError:
        pass
    else:
        raise AssertionError("interval_certificate must still RAISE on None")
    print("  REPAIRED: one guard object shared by all three modules, agreeing on 5 violating "
          "inputs, with the None policies still differing as designed")


# ===========================================================================


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for t in tests:
            print(t.__name__)
            t()
    print(f"\nALL {len(tests)} ADVERSARIAL GATES PASS "
          f"(leg 116 measured; leg 128 REPAIRED -- the `test_repaired_*` gates are leg 116's "
          f"GAP-PINs inverted, the two `test_still_a_gap_*` gates are the honest residue)")


if __name__ == "__main__":
    main()
