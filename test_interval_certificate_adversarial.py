"""ADVERSARIAL gates for solver/interval_certificate.py -- Route-ICA, leg 98.

`test_interval_certificate.py` (legs 51-61) tests that this pipeline COMPUTES correctly:
exact rational references, bound-domination orderings, and -- since leg 61 -- a published
known answer (Cadiot-Lessard-Nave's Kawahara radius).  Every one of those gates hands the
pipeline a WELL-FORMED problem.  This file asks the other question, the one leg 79 asked of
the sibling pipeline `solver/port_certification.py`: **what does the pipeline say when the
input is not well formed?**

**LEG 98's GATE ANSWERED YES, AND THE REPAIR HAS LANDED.**  Of 36 hypothesis-violating
inputs, **12 were reported as a CLOSING certificate**, and **8 of those 12 were LOAD-BEARING**
-- the hypothesis-satisfying input of the same magnitude does NOT close, so the violation was
exactly what bought the certificate.  **It is now 0 of 36.**  The full battery, with every
constant and every r-interval, is `experiments/p2_route_ica_v1_adversarial.py` ->
`writeup/data/p2_route_ica_v1_adversarial.json`, whose `history.pre_fix` block carries leg 98's
pre-repair numbers verbatim so regenerating the artifact cannot erase the finding.

**THE SEVEN GAP-PIN GATES BELOW HAVE BEEN INVERTED, NOT WEAKENED** -- the disposition leg 98
wrote into each of their docstrings, and the same conversion legs 66/79/83/85/89/91/92 made
when their findings were repaired.  Each one now asserts the REFUSAL, at the same inputs, with
the same magnitudes quoted, and carries the pre-fix behaviour in its docstring as the record of
what it is protecting against.  So the gates split into three kinds, and the kind is stated in
each docstring:

  * **FIXED gates** (formerly GAP-PIN) assert the guard that closed leg 98's defect: the exact
    inputs that used to buy a certificate must now be refused, and refused FOR THE STATED
    REASON, not by accident.  Each keeps the measured size of the lie it rejects.
  * **HOLDS gates** assert the checks that were ALREADY in place and must never regress --
    notably the NaN and infinity handling in `radii_verdict`, which leg 98 measured as correct
    4/4 and which the repair deliberately leaves as a returned non-closing verdict rather than
    an exception, and `Interval`'s own `lo <= hi` validity guard, which is leg 69's repair
    still holding the line and is the reason two of the poisoned-enclosure cases raise instead
    of lying.
  * **CONTROL gates** are the positive controls: the honest certificate must still close at a
    converged iterate and must still fail at a displaced one, so that a "nothing closes any
    more" regression cannot masquerade as robustness.  These matter more after a repair than
    before it, and the CONTROL below is unchanged from leg 98's version.

WHERE THE REFUSAL SHOWS UP, AND WHY IT DIFFERS BETWEEN THE TWO FUNCTIONS
-----------------------------------------------------------------------------
`radii_verdict` RETURNS `closes=False` with a `reason` beginning `INVALID_INPUT` and a
`violations` list -- it is a verdict function, every caller reads its `closes` field, and this
is the shape leg 79's repair gave the sibling pipeline.  `interval_constants` RAISES
`CertificateInputError` -- it returns rigorous BOUNDS, and there is no field of its result in
which "no bound was established" could be reported honestly.

WHICH HYPOTHESES, AND WHERE THEY COME FROM (writeup/novelty/leg_98.md)
-----------------------------------------------------------------------------
  (H1) `Y_0`, `Z_1`, `Z_2` are upper bounds on norms in the published radii polynomial
       theorem, hence FINITE and NONNEGATIVE.  Textbook since 2015; not a finding of this leg.
  (H2) An enclosure is a valid interval (`lo <= hi`, endpoints not NaN) and CONTAINS the
       quantity it claims to enclose.  IEEE 1788-2015 carries a dedicated `ill` decoration
       for the first half; also not a finding of this leg.
  (H3) The weight vector `w` defines a norm, so it is strictly positive and finite.

The only thing leg 98 claims is the MEASUREMENT: which of these our code enforces, and by how
much the unenforced ones move the answer.

Run: .venv/bin/python test_interval_certificate_adversarial.py
"""

import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from experiments.p2_route_ica_v1_adversarial import (PRE_FIX_MEASUREMENT, Interval,
                                                     _Poisoned, _iv_shrunk, _iv_zero, run,
                                                     substrate)
from solver.interval_certificate import (CertificateInputError, interval_constants,
                                         radii_verdict)

# The battery's banked headline, AFTER the repair. A change here is a change in the finding,
# and it must be accompanied by a change in the JSON.
BANKED = {"cases": 39, "hypothesis_violating": 36, "false_accepts": 0,
          "false_accepts_load_bearing": 0, "rejected": 29, "raised": 7}

# What it was BEFORE the repair, as leg 98 measured it -- imported from the battery rather
# than restated, so the two files cannot drift. 12/36 accepted, 8 load-bearing.
assert PRE_FIX_MEASUREMENT["false_accepts"] == 12
assert PRE_FIX_MEASUREMENT["false_accepts_load_bearing"] == 8

_SUB = None


def _sub():
    global _SUB
    if _SUB is None:
        _SUB = substrate()
    return _SUB


# --------------------------------------------------------------------------
# CONTROL
# --------------------------------------------------------------------------
def test_honest_certificate_still_closes_and_still_fails():
    """CONTROL. The substrate is a real certificate, not a rigged one.

    Without this, every gate below is satisfiable by a pipeline that refuses everything.
    At the converged iterate the certificate must CLOSE; displaced by 1e-3 it must NOT."""
    b, z, z_bad, w, nu, iv = _sub()
    good = interval_constants(iv, z, w, nu)
    bad = interval_constants(iv, z_bad, w, nu)
    vg, vb = (radii_verdict(c["Y0"], c["Z1"], c["Z2"]) for c in (good, bad))
    assert vg["closes"], f"the honest certificate stopped closing: {good}"
    assert not vb["closes"], f"the displaced iterate started closing: {bad}"
    assert good["Y0"] < 1e-9 < 1e-4 < bad["Y0"], (
        f"the poison step stopped separating the two points: Y0 {good['Y0']:.3e} "
        f"vs {bad['Y0']:.3e}")
    print(f"[ok] CONTROL honest Y0 = {good['Y0']:.3e} closes; displaced Y0 = "
          f"{bad['Y0']:.3e} ({bad['Y0'] / good['Y0']:.2e}x) does not")


# --------------------------------------------------------------------------
# HOLDS -- the checks that exist, and must not regress
# --------------------------------------------------------------------------
def test_holds_nan_constants_are_rejected():
    """HOLDS. A NaN in any of Y_0, Z_1, Z_2 must never produce closes=True.

    This is the exact hazard that defeated the sibling pipeline before leg 79's repair --
    `if x >= c: reject` is vacuously bypassed by NaN. `radii_verdict`'s guard is written
    as `if not (Z1 < 1.0)`, which is NaN-safe by construction, and the downstream
    `bool(r_min < r_max)` is False for NaN. Both properties are load-bearing."""
    for name, trip in (("Y0", (np.nan, 0.3, 1.0)), ("Z1", (1e-12, np.nan, 1.0)),
                       ("Z2", (1e-12, 0.3, np.nan)), ("all", (np.nan,) * 3)):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            v = radii_verdict(*trip)
        assert not v["closes"], f"a NaN {name} produced a closing certificate: {v}"
    print("[ok] HOLDS NaN in Y_0 / Z_1 / Z_2 / all three -- 4/4 rejected")


def test_holds_positive_infinities_are_rejected():
    """HOLDS. +inf Y_0, +inf Z_2 and -inf Z_1 are all refused.

    Recorded as a HOLDS rather than assumed: -inf Y_0 is NOT refused (see the GAP-PIN
    below), so infinity handling here is sign-dependent and only three of the four
    directions hold."""
    for name, trip in (("Y0=+inf", (np.inf, 0.3, 1.0)),
                       ("Z1=-inf", (1e-12, -np.inf, 1.0)),
                       ("Z2=+inf", (1e-12, 0.3, np.inf))):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            v = radii_verdict(*trip)
        assert not v["closes"], f"{name} produced a closing certificate: {v}"
    print("[ok] HOLDS Y_0=+inf, Z_1=-inf, Z_2=+inf -- 3/3 rejected")


def test_holds_Z1_at_and_above_one_is_rejected():
    """HOLDS. No contraction, no certificate -- at Z_1 = 1 exactly and above."""
    for Z1 in (1.0, 1.0 + 1e-16, 1.5, 1e6):
        v = radii_verdict(1e-30, Z1, 1.0)
        assert not v["closes"], f"Z_1 = {Z1!r} produced a closing certificate: {v}"
        assert v["reason"] == "Z1 >= 1", f"Z_1 = {Z1!r} rejected for the wrong reason: {v}"
    assert radii_verdict(1e-30, 1.0 - 1e-16, 1.0)["closes"] is False, (
        "Z_1 = 1 - 1e-16 with Y_0 = 1e-30 should not close: the budget is ~5e-33")
    print("[ok] HOLDS Z_1 >= 1 rejected at 1.0, 1+1e-16, 1.5, 1e6; and 1-1e-16 does not "
          "close on a 5e-33 budget")


def test_holds_interval_validity_guard_still_catches_negative_width():
    """HOLDS -- and this one is leg 69's repair, still holding, in a second pipeline.

    An enclosure with lo > hi never reaches `interval_constants` at all, because
    `Interval.__init__` refuses to construct it. That is why the two negative-width
    poisoned-residual cases in the battery RAISE rather than lying. If this guard is ever
    relaxed, the two GAP-PIN cases below acquire a negative-width sibling immediately."""
    for lo, hi in ((np.array([1e-16]), np.array([-1e-16])),
                   (np.array([1.0, 0.0]), np.array([0.5, 0.0]))):
        try:
            Interval(lo, hi)
        except ValueError as ex:
            assert "lo <= hi" in str(ex), f"wrong guard message: {ex}"
        else:
            raise AssertionError(f"Interval({lo}, {hi}) was constructed; lo > hi is "
                                 "ill-formed (IEEE 1788 `ill`) and must not be")
    print("[ok] HOLDS Interval refuses lo > hi -- leg 69's validity guard covers this "
          "pipeline's residual path too")


def test_holds_nan_and_zero_weights_are_rejected():
    """HOLDS. A weight vector with a zero or NaN component cannot buy a certificate.

    Not because anything checks it -- 1/0 and 1/NaN simply poison Z_1, which then fails
    the `not (Z1 < 1.0)` guard. Sound by accident is still sound, and it is pinned so a
    future 'tidy up the reciprocal' change cannot silently remove it."""
    b, z, z_bad, w, nu, iv = _sub()
    for name, wp in (("zero", np.concatenate([[0.0], w[1:]])),
                     ("nan", np.concatenate([[np.nan], w[1:]]))):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            c = interval_constants(iv, z, wp, nu)
            v = radii_verdict(c["Y0"], c["Z1"], c["Z2"])
        assert not v["closes"], f"a {name} weight component closed: {c} -> {v}"
        assert not np.isfinite(c["Z1"]), f"a {name} weight left Z_1 finite: {c['Z1']}"
    print("[ok] HOLDS a zero or NaN weight component drives Z_1 non-finite and is rejected")


# --------------------------------------------------------------------------
# FIXED -- leg 98's seven GAP-PINs, INVERTED. Each asserts the guard that closed it.
# --------------------------------------------------------------------------
def test_fixed_negative_Y0_is_refused():
    """FIXED (H1), was GAP-PIN. A NEGATIVE Y_0 is refused by hypothesis.

    Y_0 = ||A F(z)|| is a norm; it cannot be negative, and the theorem says nothing about
    an input that is. BEFORE THE REPAIR the pipeline evaluated the discriminant anyway,
    and because a negative Y_0 makes the discriminant LARGER it converted a failing
    certificate into a passing one with a nonsensical NEGATIVE r_min: at
    (Y_0, Z_1, Z_2) = (-1.0, 0.3, 1.0) it returned closes=True, r_min = -0.8780, where
    the sign-corrected (+1.0, 0.3, 1.0) does not close on a budget of 0.2450.

    The refusal must be BY HYPOTHESIS -- reason INVALID_INPUT, naming Y_0 -- and must
    carry no r_min at all: a rejected fabrication may not be reported in the same slot
    as a measured bound."""
    for Y0 in (-1.0, -1e-12, -1e6, -1e-30):
        v = radii_verdict(Y0, 0.3, 1.0)
        assert not v["closes"], f"a negative Y_0 = {Y0!r} still closes: {v}"
        assert v["reason"].startswith("INVALID_INPUT"), (
            f"Y_0 = {Y0!r} was refused for the wrong reason: {v['reason']!r}")
        assert any("Y_0 is negative" in s for s in v["violations"]), v["violations"]
        assert v["r_min"] is None and v["r_max"] is None, (
            f"a refused input still carries an r-interval: {v}")
    honest = radii_verdict(1.0, 0.3, 1.0)
    assert not honest["closes"] and honest["reason"] == "Y0 exceeds the budget", (
        f"the |Y_0| counterpart changed behaviour: {honest}")
    tiny = radii_verdict(1e-12, 0.3, 1.0)
    assert tiny["closes"], f"an honest small Y_0 must still close: {tiny}"
    print(f"[ok] FIXED Y_0 < 0 refused 4/4 as INVALID_INPUT with no r-interval "
          f"(was: closes=True, r_min = -0.8780 at Y_0 = -1.0); the +1.0 counterpart "
          f"still fails on its budget of {honest['budget']:.4f} and Y_0 = 1e-12 "
          f"still closes")


def test_fixed_negative_Z1_is_refused():
    """FIXED (H1), was GAP-PIN. A NEGATIVE Z_1 is refused, and no longer rescues Y_0.

    Z_1 < 0 passes the `Z1 < 1.0` guard and then inflates the budget (1-Z_1)^2/(2 Z_2)
    without bound. BEFORE THE REPAIR, at Z_1 = -1e6 the budget was 5.000e+11, so
    Y_0 = 1e3 -- a residual a thousand times the size of anything this repository has
    ever certified -- closed.

    Leg 98 named the trap in its own inversion note and it is gated here: the refusal
    must NOT be 'Z1 >= 1', which would be the wrong reason for the right answer."""
    for trip in ((1e-12, -5.0, 1.0), (1e3, -1e6, 1.0)):
        v = radii_verdict(*trip)
        assert not v["closes"], f"a negative Z_1 still closes: {trip} -> {v}"
        assert v["reason"].startswith("INVALID_INPUT"), (
            f"{trip} refused for the wrong reason: {v['reason']!r}")
        assert v["reason"] != "Z1 >= 1" and any("Z_1 is negative" in s
                                                for s in v["violations"]), v
        assert v["budget"] == 0.0, f"a refused input still quotes a budget: {v}"
    honest = radii_verdict(1e3, 1e6, 1.0)
    assert not honest["closes"] and honest["reason"] == "Z1 >= 1", (
        f"the |Z_1| counterpart changed behaviour: {honest}")
    print("[ok] FIXED Z_1 < 0 refused as INVALID_INPUT naming Z_1 (not as 'Z1 >= 1'), "
          "and quotes no budget -- Z_1 = -1e6 no longer lifts the budget to 5.000e+11 "
          "to rescue a Y_0 = 1e3 certificate")


def test_fixed_negative_infinite_Y0_is_refused():
    """FIXED (H1), was GAP-PIN. Y_0 = -inf is refused for the same reason +inf is.

    BEFORE THE REPAIR, Y_0 = -inf closed with r_min = -1.341e+154 while Y_0 = +inf was
    correctly refused. That asymmetry was the tell that the guard was arithmetic and not
    a hypothesis check. Both directions are now refused as non-finite, and the SYMMETRY
    is what this gate asserts."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        v = radii_verdict(-np.inf, 0.3, 1.0)
        plus = radii_verdict(np.inf, 0.3, 1.0)
    for name, got in (("-inf", v), ("+inf", plus)):
        assert not got["closes"], f"Y_0 = {name} still closes: {got}"
        assert got["reason"].startswith("INVALID_INPUT"), (
            f"Y_0 = {name} refused for the wrong reason: {got['reason']!r}")
        assert any("infinite" in s for s in got["violations"]), got["violations"]
        assert got["r_min"] is None, f"Y_0 = {name} still carries an r_min: {got}"
    print("[ok] FIXED Y_0 = -inf and Y_0 = +inf are now refused identically, as "
          "non-finite by hypothesis (was: -inf closed with r_min = -1.341e+154)")


def test_fixed_fabricated_zero_residual_enclosure_is_refused():
    """FIXED (H2), was GAP-PIN. An enclosure reporting F(z) == [0, 0] is refused.

    BEFORE THE REPAIR this closed at an iterate whose true residual is 5.907e-03, on a
    fabricated Y_0 of 7.9e-323 -- a lie of ~320 decades, undetected, because
    `interval_constants` never checked that the enclosure it was handed contained
    anything. The module's docstring said containment IS gated, but it was gated in the
    test suite for the REAL enclosure class, not enforced at runtime for whatever object
    a caller passes. That distinction was the whole finding on this side of the battery.

    The guard re-evaluates F in float at the same point and compares in the Y_0 currency,
    so the refusal names both numbers. The honest constants at the same point are
    computed first and must be unaffected."""
    b, z, z_bad, w, nu, iv = _sub()
    honest = interval_constants(iv, z_bad, w, nu)
    assert not radii_verdict(honest["Y0"], honest["Z1"], honest["Z2"])["closes"]
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            interval_constants(_Poisoned(iv, f_hook=_iv_zero), z_bad, w, nu)
    except CertificateInputError as ex:
        assert "does not contain the residual" in str(ex), f"wrong guard message: {ex}"
    else:
        raise AssertionError(
            "a fabricated F == [0,0] enclosure still produced constants; it used to "
            "yield Y_0 = 7.9e-323 and CLOSE at a point whose honest Y_0 is 5.907e-03")
    print(f"[ok] FIXED a fabricated F == [0,0] enclosure is REFUSED "
          f"(CertificateInputError) at an iterate whose honest Y_0 = {honest['Y0']:.3e} "
          f"-- it used to return Y_0 = 7.9e-323 and close, a lie of ~320 decades")


def test_fixed_well_formed_non_containing_enclosure_is_refused():
    """FIXED (H2), was GAP-PIN, and the sharpest case in the battery.

    This enclosure is perfectly well formed -- lo <= hi, all endpoints finite, no NaN, a
    positive width -- so EVERY validity check that exists, including leg 69's, passes it.
    It is simply the honest enclosure scaled by 1e-8, so it does not contain the residual,
    and BEFORE THE REPAIR the certificate closed with a Y_0 that was 1.000e+08 times too
    small. No amount of interval-validity checking catches this one; only a containment
    check does, which is why the repair is a containment check and not a stricter
    validity check.

    The 1e-8 factor is kept, per leg 98's inversion note: it is the measured size of the
    lie, and the guard's message must quote the resulting ratio."""
    b, z, z_bad, w, nu, iv = _sub()
    honest = interval_constants(iv, z_bad, w, nu)
    poisoned = _Poisoned(iv, f_hook=_iv_shrunk)
    fz = poisoned.F(z_bad)
    assert np.all(fz.lo <= fz.hi) and np.all(np.isfinite(fz.lo)) and np.any(
        fz.hi > fz.lo), "the poisoned enclosure must stay WELL FORMED, or the gate is moot"
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            interval_constants(poisoned, z_bad, w, nu)
    except CertificateInputError as ex:
        assert "does not contain the residual" in str(ex), f"wrong guard message: {ex}"
        msg = str(ex)
    else:
        raise AssertionError(
            "a well-formed NON-CONTAINING enclosure (the honest one scaled by 1e-8) "
            "still produced constants; it used to understate Y_0 by 1.0e+08x and close")
    print(f"[ok] FIXED a WELL-FORMED non-containing enclosure (lo<=hi, finite, positive "
          f"width, 1e-8 x the honest one) is REFUSED by the containment screen, where "
          f"the honest Y_0 = {honest['Y0']:.3e}; guard reports: {msg.split('--')[1].strip()[:60]}")


def test_fixed_negative_weight_vector_is_refused():
    """FIXED (H3), was GAP-PIN. A sign-flipped weight vector is refused as not a norm.

    `w` defines the norm the certificate is stated in. Negated, it is not a norm, and
    BEFORE THE REPAIR the whole-vector case drove Y_0 NEGATIVE (-2.463e-28) -- the one
    end-to-end path in this battery from structurally valid enclosures to a
    hypothesis-violating constant, which `radii_verdict` then closed. A single negative
    component was accepted too.

    Both are refused at the door now, by `interval_constants`, before any bound exists."""
    b, z, z_bad, w, nu, iv = _sub()
    for name, wp in (("all negative", -np.asarray(w)),
                     ("one negative", np.concatenate([[-w[0]], w[1:]]))):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                interval_constants(iv, z, wp, nu)
        except CertificateInputError as ex:
            assert "negative component" in str(ex), f"wrong guard message: {ex}"
        else:
            raise AssertionError(f"a weight vector with {name} components was accepted "
                                 "as a norm; w -> -w used to yield Y_0 = -2.463e-28 and "
                                 "close")
    good = interval_constants(iv, z, w, nu)
    assert radii_verdict(good["Y0"], good["Z1"], good["Z2"])["closes"], (
        "the honest weight stopped closing -- the guard is too broad")
    print("[ok] FIXED w -> -w and a single negative component are both REFUSED as not a "
          "norm (w -> -w used to yield Y_0 = -2.463e-28, which radii_verdict closed); "
          "the honest w still closes")


def test_fixed_Z2_zero_reports_instead_of_raising():
    """FIXED, was GAP-PIN, the mild one. Z_2 = 0 returns a structured verdict.

    It used to raise a bare `ZeroDivisionError` from inside a verdict function. A crash
    is a refusal, so that was never unsound -- but Z_2 = 0 is not exotic (it is what an
    exactly-linear system gives) and a caller with a broad `except` turns a crash into a
    silent skip.

    The verdict is NON-closing and says why: with Z_2 = 0 the radii polynomial degenerates
    from a quadratic to an affine function, whose feasibility is a different statement
    from the one `radii_verdict` implements. Refusing is the conservative reading and the
    repair adds no mathematics."""
    for Z2 in (0.0, -0.0):
        v = radii_verdict(1e-12, 0.3, Z2)
        assert not v["closes"], f"Z_2 = {Z2!r} produced a closing certificate: {v}"
        assert v["degenerate"] == "Z2 == 0" and "affine" in v["reason"], (
            f"Z_2 = {Z2!r} refused without naming the degeneracy: {v}")
        assert v["r_min"] is None and v["r_max"] is None and v["budget"] == 0.0, (
            f"a degenerate verdict still quotes a radius or a budget: {v}")
    assert radii_verdict(1e-12, 0.3, 1e-300)["closes"], (
        "a tiny but nonzero Z_2 is a legitimate quadratic and must still close")
    print("[ok] FIXED Z_2 = 0 and Z_2 = -0.0 return a structured non-closing verdict "
          "naming the affine degeneracy, instead of raising ZeroDivisionError; "
          "Z_2 = 1e-300 still closes")


# --------------------------------------------------------------------------
# the battery itself, as a gate
# --------------------------------------------------------------------------
def test_banked_battery_reproduces():
    """The headline count is reproducible, and it is the number the writeup quotes.

    0 of 36 hypothesis-violating inputs accepted, down from leg 98's 12 (8 load-bearing).
    Every case that used to be a false accept must now be a rejection or a refusal, BY
    NAME -- a total that moves for some other reason would otherwise pass this gate."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        data = run(write=False, verbose=False)
    t = data["totals"]
    for k, want in BANKED.items():
        assert t[k] == want, (f"battery total {k} = {t[k]}, banked {want}. The finding "
                              f"changed; update the JSON and this file together.")
    assert data["false_accept_cases"] == [] and data["load_bearing_cases"] == []
    by_case = {c["case"]: c["outcome"] for c in data["cases"]}
    for case in PRE_FIX_MEASUREMENT["false_accept_cases"]:
        assert by_case[case] in ("rejected", "raised"), (
            f"{case} was a false accept before the repair and is {by_case[case]!r} now")
    # and the positive controls still separate, inside the battery itself
    assert data["substrate"]["honest_at_z_closes"] is True
    assert data["substrate"]["honest_at_z_bad_closes"] is False
    assert by_case["B01_baseline_valid"] == "valid_closes"
    assert by_case["B03_honest_non_closing"] == "valid_rejects"
    print(f"[ok] battery reproduces: {t['false_accepts']}/{t['hypothesis_violating']} "
          f"hypothesis-violating inputs reported a CLOSING certificate "
          f"(was {PRE_FIX_MEASUREMENT['false_accepts']}, "
          f"{PRE_FIX_MEASUREMENT['false_accepts_load_bearing']} load-bearing); "
          f"{t['rejected']} rejected, {t['raised']} refused loudly, and all "
          f"{len(PRE_FIX_MEASUREMENT['false_accept_cases'])} former false accepts are "
          f"accounted for by name")


if __name__ == "__main__":
    # The poisoned cases divide by zero and take sqrt of NaN on purpose; numpy's
    # RuntimeWarnings are the EXPECTED noise of the battery, not a signal, and letting
    # them through would bury the [ok] lines they are interleaved with.
    warnings.simplefilter("ignore", RuntimeWarning)
    np.seterr(all="ignore")
    test_honest_certificate_still_closes_and_still_fails()
    test_holds_nan_constants_are_rejected()
    test_holds_positive_infinities_are_rejected()
    test_holds_Z1_at_and_above_one_is_rejected()
    test_holds_interval_validity_guard_still_catches_negative_width()
    test_holds_nan_and_zero_weights_are_rejected()
    test_fixed_negative_Y0_is_refused()
    test_fixed_negative_Z1_is_refused()
    test_fixed_negative_infinite_Y0_is_refused()
    test_fixed_fabricated_zero_residual_enclosure_is_refused()
    test_fixed_well_formed_non_containing_enclosure_is_refused()
    test_fixed_negative_weight_vector_is_refused()
    test_fixed_Z2_zero_reports_instead_of_raising()
    test_banked_battery_reproduces()
    print("\nALL ADVERSARIAL GATES PASS -- 7 of them leg 98's GAP-PINs, INVERTED to "
          "assert the guard that closed the defect (12/36 false accepts -> 0/36). "
          "See the header.")
