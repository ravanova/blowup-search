"""ADVERSARIAL gates for solver/certificate_guards.py -- Route-CGA (leg 199, MEASURED).

`solver/certificate_guards.py` is the ONE shared hypothesis guard -- the accept/reject layer
that decides whether a radii-polynomial verdict function may evaluate a discriminant at all.
It exists because the same defect was measured three times: `port_certification.py` 11/25
(leg 79), `interval_certificate.py` 12/36 (leg 98), `nk_bounds.py` 21/52 (leg 116).  Leg 128
replaced two private copies of legs 79/98's function with it.

**IT HAD NEVER ITSELF BEEN AUDITED.**  `capabilities.py:303-334` says so in its own words --
"NO known-answer gate of its own -- it is exercised through the three modules' suites" -- its
entire history is one commit (`bfe6883`), and the only prior art that touches it
(`test_nk_bounds_adversarial.py:528-554`) drives five PLAIN FLOAT64 triples through the three
CONSUMERS, i.e. exactly the three shapes it was written to catch.

**LEG 199's GATE ANSWERED YES.**  Of 67 cases, **16 are silent ACCEPTS** of inputs the
module's own docstrings say are outside the theorem, across four mechanisms; 43 controls
pass, 0 fail.  The headline is M1:

    `unit_range_violation` is the ONLY one of the five exported guards with no `isinf` test
    -- `hypothesis_violations` and `radius_violation` both call `math.isinf`, and
    `positive_weight_violations` counts infinite entries.  It delegates non-finiteness to two
    comparisons, and `nk_bounds.py:430` asks it for a CLOSED lower endpoint at MINUS
    INFINITY, so the lower test is `-inf < -inf` = False.  **`alpha = -inf` is admissible**,
    and `farfield_modelling_error_bound(-inf, 0.5, 1.0)` then returns `bound = NaN` with
    40 of 40 window samples NaN and DOES NOT RAISE -- against an honest 2.537396530974982 at
    alpha = 1.5, and against `+inf` and `NaN`, which both refuse with a named `ValueError`.
    1 of 3 non-finite alphas is accepted, and it is the only one that MANUFACTURES a NaN in
    an upper-bound slot -- the exact object this module's own `NAN_HINT_*` constants exist to
    warn about ("`NaN >= 1.0` is False, so an unguarded NaN would slip past the contraction
    test").

**THE BLAST RADIUS IS LATENT, AND THAT IS A MEASUREMENT.**  Every in-repo caller of the
affected sites passes alpha in [1.1, 1.8] and float64 constants: `test_nk_bounds.py:192,207`,
`p2_route_d_v6/v7/v8/v9`, `p2_route_nka_v1_adversarial.py:408,425`,
`p2_route_nkr_v1_repair.py:230`, `p2_route_nkb_v1_postrepair.py:150`.  **0 banked numbers are
impeached.**  The guard restores a guarantee, not a margin -- but the guarantee is the whole
reason the module exists.

**THE MODULE IS NOT PATCHED HERE**, by this leg's own gate: the YES branch escalates and
forbids patching under this leg's authority.  The gates below are therefore **GAP-PINs** --
each ASSERTS THE DEFECT and names its own inversion, so that whoever lands the repair has an
executable statement of what must change and at what magnitude (lesson 68: a repaired defect
whose size is forgotten is one that comes back at a different size).

The full battery, every case and every magnitude:
`experiments/p2_route_cga_v1_adversarial.py` -> `writeup/data/p2_route_cga_v1_adversarial.json`.

WHICH HYPOTHESES, AND WHERE THEY COME FROM
-----------------------------------------------------------------------------
Not findings of this leg.  `Y_0`, `Z_0`, `Z_1`, `Z_2` are upper bounds on norms in the
published radii polynomial theorem (van den Berg & Lessard, *Notices AMS* 62(9):1057, 2015),
hence finite and nonnegative; a Holder exponent is a REAL number, so a non-finite one is
outside the hypothesis whatever the interval endpoints say; a weight vector defines a norm.
The only claim here is the MEASUREMENT: which of these the guard enforces, and what the
unenforced ones produce at the real call sites.

GATE KINDS
-----------------------------------------------------------------------------
  * GAP-PIN gates (`test_gap_*`) assert a DEFECT and name their inversion.
  * HOLDS gates (`test_holds_*`) assert what the guard DOES enforce and must never regress
    -- this is the majority of the module, and a battery that reported only the gaps would
    misrepresent it.
  * CONTROL gates (`test_control_*`) are over-rejection controls: a legitimate bound, radius,
    exponent and weight vector must still be ACCEPTED, so that a "nothing passes any more"
    regression cannot masquerade as a repair.
"""

import math
import sys
import traceback
from decimal import Decimal
from fractions import Fraction

import numpy as np

import solver.certificate_guards as cg
import solver.nk_bounds as nk

INF, NAN = float("inf"), float("nan")

# The two REAL call sites, transcribed from `solver/nk_bounds.py` rather than paraphrased.
ALPHA_SITE = dict(lo=-INF, hi=2.0, lo_open=False, hi_open=True)     # nk_bounds.py:430
GAMMA_SITE = dict(lo=0.0, hi=1.0, lo_open=True, hi_open=False)      # nk_bounds.py:392


# ===========================================================================
# GAP-PIN gates -- leg 199's findings, asserted as defects
# ===========================================================================

def test_gap_m1_unit_range_violation_accepts_minus_infinity_at_the_alpha_site():
    """M1, THE HEADLINE.  A non-finite Holder exponent is ADMISSIBLE at `nk_bounds.py:430`.

    `unit_range_violation` has no `isinf` test.  Its two comparisons are

        lo_bad = (f <= lo) if lo_open else (f < lo)
        hi_bad = (f >= hi) if hi_open else (f > hi)

    and the alpha call site passes `lo = -inf, lo_open=False`, so `lo_bad` is `-inf < -inf`,
    which is False.  MEASURED: the guard returns `None` (admissible) and
    `farfield_modelling_error_bound(-inf, 0.5, 1.0)` returns `bound = NaN`, 40/40 window
    samples NaN, WITHOUT RAISING -- while `+inf` and `NaN` both raise a named `ValueError`.

    INVERSION WHEN REPAIRED: `unit_range_violation` grows an explicit `math.isinf(f)` test
    alongside its `math.isnan(f)` one, and this gate becomes
    `assert cg.unit_range_violation("alpha", -INF, **ALPHA_SITE) is not None` plus
    `pytest.raises(ValueError)` on the consumer.  The 2.537396530974982 reference at
    alpha=1.5 must NOT move -- it is a clean-input value and leg 128's stop condition
    (a rejection layer may never change a number a hypothesis-satisfying input produced)
    binds any repair of this module."""
    assert cg.unit_range_violation("alpha", -INF, **ALPHA_SITE) is None, (
        "GAP-PIN: if this now REJECTS, M1 is repaired -- invert this gate per the docstring")

    d = nk.farfield_modelling_error_bound(-INF, 0.5, 1.0)
    assert math.isnan(d["bound"]), f"expected a NaN bound, got {d['bound']}"
    assert sum(1 for v in d["value"] if math.isnan(v)) == 40, "expected 40/40 NaN samples"

    # the two siblings that DO refuse -- this is what makes -inf the odd one out
    for bad in (INF, NAN):
        try:
            nk.farfield_modelling_error_bound(bad, 0.5, 1.0)
        except ValueError:
            pass
        else:
            raise AssertionError(f"alpha={bad} must still be refused")

    honest = nk.farfield_modelling_error_bound(1.5, 0.5, 1.0)["bound"]
    assert honest == 2.537396530974982, (
        f"the clean-input reference moved: {honest!r} != 2.537396530974982")
    print("  GAP M1: alpha=-inf ACCEPTED -> bound=NaN, 40/40 NaN samples, no exception; "
          "+inf and NaN both refuse. Honest alpha=1.5 bound 2.537396530974982 unmoved")


def test_gap_m1_localised_the_gamma_site_with_a_finite_endpoint_is_clean():
    """M1's LOCALISATION, and it is what makes the finding precise rather than vague.

    The SAME function, at the SAME repository, refuses BOTH infinities at the gamma site --
    because there the lower endpoint is finite (`0.0`, open), so `-inf <= 0.0` is True.  The
    defect is therefore not "the guard is careless about infinity" but the INTERACTION of a
    missing `isinf` test with a caller-supplied INFINITE endpoint, and `nk_bounds.py:430` is
    the only such caller in the repository.

    This gate stays as-is after the repair; it is the evidence that the repair's scope is
    one line and not a rewrite."""
    for bad in (INF, -INF, NAN, 0.0, 1.5):
        assert cg.unit_range_violation("gamma", bad, **GAMMA_SITE) is not None, (
            f"gamma={bad} must be refused at the finite-endpoint site")
    for good in (0.5, 1.0):
        assert cg.unit_range_violation("gamma", good, **GAMMA_SITE) is None, (
            f"gamma={good} is a legitimate Holder exponent and must be accepted")
    print("  LOCALISED: the gamma site (finite lower endpoint) refuses +-inf 2/2; only the "
          "alpha site's caller-supplied -inf endpoint is exposed")


def test_gap_m2_three_guards_have_no_type_check_while_their_sibling_raises():
    """M2.  `hypothesis_violations` enforces `isinstance(v, numbers.Real)` and RAISES on a
    non-real value -- "a constant that is not a number is a caller bug, not a fabricated
    bound, and must not be laundered into a `closes=False`".  `radius_violation` and
    `unit_range_violation`, in the SAME FILE, call `float()` with no such check.

    MEASURED: `radius_violation` accepts `'0.5'`, `Decimal('0.5')`, `Fraction(1,2)` and
    `True` as admissible RADII -- 4 of 4 -- while the sibling refuses 3 of those 4 by
    `TypeError` (bool is `numbers.Real` and passes both).  A string `gamma` passes the
    exponent guard too, and the refusal that eventually happens is an unnamed `TypeError`
    from the power operator three lines into `hilbert_farfield_bound` -- leg 98's B20/B21
    shape, in the module that was repaired for it.

    INVERSION WHEN REPAIRED: both guards grow the same `numbers.Real` check, and this gate
    becomes a `TypeError` assertion on all four values."""
    for v in ("0.5", Decimal("0.5"), Fraction(1, 2), True):
        assert cg.radius_violation(v) is None, (
            f"GAP-PIN: radius_violation({v!r}) now rejects -- M2 repaired, invert this gate")
    n_sibling_raises = 0
    for v in ("0.5", Decimal("0.5"), Fraction(1, 2), True):
        try:
            cg.hypothesis_violations((("Y_0", v),))
        except TypeError:
            n_sibling_raises += 1
    assert n_sibling_raises == 2, (
        f"expected the sibling to raise on str and Decimal only, got {n_sibling_raises}")

    assert cg.unit_range_violation("gamma", "0.5", **GAMMA_SITE) is None
    try:
        nk.hilbert_farfield_bound(1.0, 1.5, "0.5")
    except TypeError:
        pass
    else:
        raise AssertionError("a string gamma reached a numeric result")
    print("  GAP M2: radius_violation accepts 4/4 non-float radii and unit_range_violation "
          "accepts a str exponent; hypothesis_violations raises on 2 of the same 4")


def test_gap_m3_bool_is_numbers_real_and_is_silently_reinterpreted():
    """M3, reported at its HONEST weight.

    `isinstance(True, numbers.Real)` is True in Python, so a FLAG passes every guard in the
    module and is evaluated as the number 1.0 (or 0.0).  MEASURED at the consumers:
    `hilbert_farfield_bound(1.0, 1.5, gamma=True)` returns a claimed upper bound of
    1.2209630139367613 against 1.5390840894727127 at the live gamma=0.5 -- **1.2605493138651522x
    SMALLER** -- and `budget(Y_0=False, ...)` returns `closes=True` with a `reason` that
    narrates the boolean into a mathematical claim: "Y_0 is exactly 0.0, which is the honest
    zero-residual case -- the centre itself is a zero".

    WHAT THIS IS NOT, stated because inflating it would be the dishonest move: `True` IS
    arithmetically 1.0 and gamma=1.0 IS a legitimate exponent, so each number is CORRECT FOR
    THE COERCED VALUE.  This is a missing signal, not an arithmetic lie, and it is pinned at
    that weight.  It is listed because the module's whole purpose is to refuse inputs no run
    could have produced, and a Boolean in a norm slot is one.

    INVERSION WHEN REPAIRED: `isinstance(v, bool)` is rejected ahead of the `numbers.Real`
    test in all four guards."""
    assert cg.hypothesis_violations((("Y_0", True), ("Z_0", False))) == [], (
        "GAP-PIN: booleans now rejected -- M3 repaired, invert this gate")

    probe = nk.hilbert_farfield_bound(1.0, 1.5, True)[0]
    ref = nk.hilbert_farfield_bound(1.0, 1.5, 0.5)[0]
    assert probe == 1.2209630139367613 and ref == 1.5390840894727127, (probe, ref)
    assert abs(ref / probe - 1.2605493138651522) < 1e-12, ref / probe

    v = nk.budget(False, 0.0, 0.3, 1.0)
    assert v["closes"] is True and v["r_min"] == 0.0
    assert "Y_0 is exactly 0.0" in v["reason"], v["reason"]
    print("  GAP M3: gamma=True gives a bound 1.2605493138651522x smaller than the live "
          "gamma=0.5; budget(Y_0=False) closes and narrates the flag as a zero residual")


def test_gap_m4_a_negative_rational_below_the_denormal_floor_is_accepted():
    """M4.  `float(v)` underflows a NEGATIVE rational to `-0.0` on the line BEFORE the
    `f < 0.0` test, so a constant the docstring calls "an input the theorem says nothing
    about" is admitted as nonnegative, and `budget` closes on it.

    MAGNITUDE, stated so it cannot later be overstated: the accepted negatives span
    `(-5e-324, 0)`, so the contraction-budget inflation is at most 1 ULP.  The ACCEPT is
    real; the magnitude is nil.  It is also unreachable from float64 by construction -- a
    negative float below the denormal floor already IS `-0.0` -- so it needs an exact type
    (`Fraction`, or an `int` ratio) to express at all.

    The discrimination control is in the same gate: a REPRESENTABLE negative rational is
    correctly refused, so this is a float-conversion boundary and not a Fraction blind spot.

    INVERSION WHEN REPAIRED: sign is tested on the ORIGINAL value (`v < 0`) rather than on
    its float image, and this gate asserts the violation string names `Y_0`."""
    tiny = Fraction(-1, 10 ** 400)
    assert cg.hypothesis_violations((("Y_0", tiny),)) == [], (
        "GAP-PIN: the underflowed negative now rejects -- M4 repaired, invert this gate")
    assert float(tiny) == 0.0 and math.copysign(1.0, float(tiny)) < 0, "expected -0.0"

    # discrimination control (lesson 90): a representable negative rational IS refused
    v = cg.hypothesis_violations((("Y_0", Fraction(-1, 3)),))
    assert len(v) == 1 and "negative" in v[0], v
    assert nk.budget(1e-6, tiny, 0.3, 1.0)["closes"] is True
    print("  GAP M4: Fraction(-1, 10**400) accepted as nonnegative (float image -0.0) and "
          "budget closes; Fraction(-1,3) correctly refused -- a conversion boundary, <=1 ULP")


def test_gap_m5_an_empty_container_is_a_vacuous_pass_in_two_guards():
    """M5.  `hypothesis_violations(())` returns `[]` -- "every constant is admissible", with
    zero constants examined -- and `positive_weight_violations("v_cod", [])` certifies an
    EMPTY weight vector as one "a norm could have produced".  The same empty-window shape
    leg 99 measured in `boussinesq_velocity.py`.

    AT THE CONSUMER the reach is measured, not assumed: `nk_bounds.py:225`'s own numpy
    pre-screen ALSO passes an empty array (`np.all` of an empty array is True), so the guard
    is never even consulted, and the failure surfaces four lines later as numpy's
    `ValueError: zero-size array to reduction operation minimum`.  Sound in the end, silent
    at the layer whose job is to speak.

    INVERSION WHEN REPAIRED: both guards report an emptiness violation, and this gate asserts
    a non-empty return."""
    assert cg.hypothesis_violations(()) == [], (
        "GAP-PIN: an empty constant list now rejects -- M5 repaired, invert this gate")
    for empty in ([], np.array([]), (x for x in [])):
        assert cg.positive_weight_violations("v_cod", empty) == [], (
            "GAP-PIN: an empty weight vector now rejects -- M5 repaired, invert this gate")

    assert bool(np.all(np.isfinite(np.array([])))) and bool(np.all(np.array([]) > 0.0)), (
        "the caller's own pre-screen must be shown to pass the empty array too")
    print("  GAP M5: empty constants and empty weight vectors both certified admissible; "
          "the consumer's numpy pre-screen passes them too, so the guard is never consulted")


def test_gap_m7_invalid_input_reason_builds_an_accusation_with_no_charge():
    """M7, a hygiene note rather than a certificate risk, kept because it is in the same
    sentence-assembly path every artifact quotes.

    `invalid_input_reason([])` returns the full rejection sentence with an empty reason
    clause: `INVALID_INPUT: ... nonnegative): . No discriminant is evaluated.`  Not reachable
    at `nk_bounds.py:533`, which is guarded by `if violations:`.

    INVERSION WHEN REPAIRED: the function raises or returns `None` on an empty list."""
    s = cg.invalid_input_reason([])
    assert s.startswith("INVALID_INPUT") and "): ." in s, s
    print(f"  GAP M7: a {len(s)}-character rejection sentence naming 0 violated hypotheses")


# ===========================================================================
# HOLDS gates -- what the guard DOES enforce, and must never lose
# ===========================================================================

def test_holds_the_three_shapes_the_guard_was_written_for():
    """NaN, +-inf and negative constants are refused, in float64 and in numpy scalars.  This
    is the majority of the module and the reason 17 of leg 116's 21 false-closing
    certificates now reject; a battery reporting only the gaps would misrepresent it."""
    for v in (-1.0, NAN, INF, -INF, np.float64(-1.0), np.float32("nan"), np.float64(INF)):
        out = cg.hypothesis_violations((("Y_0", v),))
        assert len(out) == 1 and out[0].startswith("Y_0"), (v, out)
    for v in ("-1.0", complex(-1, 0), np.array(-1.0), Decimal("-1")):
        try:
            cg.hypothesis_violations((("Y_0", v),))
        except TypeError:
            continue
        raise AssertionError(f"a non-real {type(v).__name__} must raise TypeError")
    print("  HOLDS: 7/7 non-finite or negative constants refused, 4/4 non-real raise")


def test_holds_radius_and_weight_guards_on_the_shapes_they_do_catch():
    for v in (NAN, INF, -INF, 0.0, -0.0, -1.0):
        assert cg.radius_violation(v) is not None, f"r_min={v} must be refused"
    for vals in ([-1.0, -1.0], [1.0, -0.0], [1.0, NAN], [1.0, INF], [1.0, 2.0, -3.0]):
        assert cg.positive_weight_violations("v_cod", vals), f"{vals} must be refused"
    print("  HOLDS: 6/6 inadmissible radii and 5/5 corrupt weight vectors refused")


def test_holds_the_three_pipelines_still_agree():
    """Leg 128's shared-guard claim, RE-DERIVED here rather than quoted -- if this fails, the
    module under audit is not the one the other legs measured."""
    import solver.interval_certificate as ic
    import solver.port_certification as pc
    for (Y0, Z1, Z2) in ((-1.0, 0.3, 1.0), (NAN, 0.3, 1.0), (INF, 0.3, 1.0),
                         (1e-6, -1.0, 1.0), (1e-6, 0.3, -1.0)):
        vp = pc.radii_polynomial_status(Y0, Z1, Z2)
        vi = ic.radii_verdict(Y0, Z1, Z2)
        vn = nk.budget(Y0, 0.0, Z1, Z2)
        assert vp["closes"] is False and vi["closes"] is False and vn["closes"] is False
        assert len(vp["violations"]) == len(vi["violations"]) == len(vn["violations"])
    assert pc._shared_hypothesis_violations is cg.hypothesis_violations
    assert ic._shared_hypothesis_violations is cg.hypothesis_violations
    assert nk.hypothesis_violations is cg.hypothesis_violations
    print("  HOLDS: one guard object, three pipelines, 5/5 violating triples agreed")


# ===========================================================================
# CONTROL gates -- over-rejection
# ===========================================================================

def test_control_legitimate_inputs_are_still_accepted():
    """The "nothing passes any more" control.  A repair of M1-M5 must leave every one of
    these ACCEPTED; if it does not, it moved a clean-input result, which is leg 128's own
    stop condition for this module."""
    for v in (0.0, -0.0, 1e-300, 1.0):
        assert cg.hypothesis_violations((("Y_0", v),)) == [], v
    for v in (0.5, 5e-324):
        assert cg.radius_violation(v) is None, v
    for v in (0.5, 1.0):
        assert cg.unit_range_violation("gamma", v, **GAMMA_SITE) is None, v
    for v in (1.5, -1e300):
        assert cg.unit_range_violation("alpha", v, **ALPHA_SITE) is None, v
    assert cg.positive_weight_violations("v_cod", [1.0, 2.0, 3.0]) == []
    assert cg.positive_weight_violations("q_cod", [1.0, 0.0], allow_zero=True) == [], (
        "allow_zero=True is the rectangular-kernel path and permits zeros BY DESIGN")
    print("  CONTROL: 13/13 legitimate bounds, radii, exponents and weights still accepted")


def test_control_the_live_range_still_produces_finite_bounds():
    """The blast-radius measurement, as an executable gate: every in-repo alpha
    (1.1 .. 1.8, read out of the callers) must still return a finite bound.  This is what
    makes "LATENT / 0 banked numbers impeached" a measurement rather than a reassurance."""
    for a in (1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8):
        b = nk.farfield_modelling_error_bound(a, 0.5, 1.0, n_X=8)["bound"]
        assert np.isfinite(b) and b > 0.0, (a, b)
    print("  CONTROL: 8/8 live alphas in [1.1, 1.8] return finite positive bounds -- the "
          "defect is unreachable from every in-repo caller")


# ===========================================================================


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        print(f"{t.__name__}")
        try:
            t()
        except Exception:                                       # noqa: BLE001
            failed += 1
            traceback.print_exc()
    print(f"\n{len(tests) - failed}/{len(tests)} gates pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
