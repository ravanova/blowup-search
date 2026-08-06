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


# ==========================================================================
# LEG 201 (Route-ICA2) -- THE DEGENERATE BANDS.  APPENDED, NOTHING ABOVE TOUCHED.
# ==========================================================================
# Leg 98's 39 cases above are ALL normal-range floats.  They ask whether this module
# enforces the HYPOTHESES it is imported under.  They do not ask whether the module's own
# ARITHMETIC is a bound.  Leg 201 drives it through the two bands leg 69 (Route-IA) named
# in the primitive underneath, `solver/interval.py`:
#
#   the SUBNORMAL band  -- where a purely RELATIVE error bound underflows to zero while the
#                          true accumulation error stays ABSOLUTE (a few eta).  Leg 69
#                          repaired this IN `interval.py` with Rump's eta term (BIT
#                          52:201-220, 2012): `_ETA_TERMS_PLAIN`, `_ETA_TERMS_DOT2`.
#   the 2^997 band      -- where Dekker's splitting constant overflows and used to return a
#                          silent NaN.  Leg 69 repaired this by raising in `_two_product`.
#
# **LEG 201's GATE ANSWERED YES, AND IS NOT REPAIRED.**  `interval_certificate.
# matmul_point_interval` is a CLONE of `interval.matvec` that never received leg 69's eta
# term, and in the subnormal band it returns an enclosure that DOES NOT CONTAIN the value it
# encloses -- by up to 200 eta, which is 24.63% of the returned magnitude at the shipped
# N = 405.  The defect reaches `interval_constants`, whose returned `Y_0` -- a claimed UPPER
# bound -- comes back 19.66% BELOW the exact quantity it bounds, with no exception and
# `rigorous: True`.
#
# The gates below are therefore **GAP-PIN**s: they assert the DEFECT, at measured
# magnitudes, so that a repair cannot land silently and a regression cannot either.  Each
# names its own inversion.  **Invert them on repair; do not weaken them.**  The repair is
# one line -- the same eta term, in the same place, that `interval.matvec` already carries.
#
# Leg 201 did NOT patch `solver/interval_certificate.py` or `solver/interval.py`, under
# either gate outcome, per the precedent of legs 66, 69, 79 and 98.

from fractions import Fraction as _Fr

from solver.interval import dot2_matvec, matvec as _matvec
from solver.interval_certificate import matmul_point_interval as _mpi

_ETA = 2.0 ** -1074
_SUB_BASE_201 = 2.0 ** -537


def _subnormal_pair(m, k):
    """(M, v) whose m products are all exactly k*eta -- leg 201's deterministic case."""
    return np.full((1, m), _SUB_BASE_201), np.full(m, k * _SUB_BASE_201)


def _exact_row(M_row, v):
    return sum((_Fr(float(a)) * _Fr(float(b)) for a, b in zip(M_row, v)), _Fr(0))


def test_gappin_201_matmul_point_interval_loses_containment_when_subnormal():
    """GAP-PIN (leg 201). `matmul_point_interval` returns a NON-CONTAINING enclosure.

    Deterministic, not searched: every product is exactly k*eta, a forced rounding tie, so
    the m per-product errors accumulate to m/2 eta while the relative guard
    `gamma_m * sum|M_ij v_j|` underflows to EXACTLY ZERO -- leaving one nextafter push,
    worth 1 eta, against it.

    MEASURED at the two accumulation lengths this repository ships (BorderedCLM N=103,
    BorderedHL N=405), both rounding directions:

        m = 103 -> escape  50 eta = 24.04% of the returned magnitude
        m = 405 -> escape 200 eta = 24.63% of the returned magnitude

    ON REPAIR (add `_eta_floor(m, _ETA_TERMS_PLAIN)` to both error terms, exactly as
    `interval.matvec` does): INVERT this gate to assert containment at every m, and keep
    these magnitudes in the docstring as the record of what it protects against."""
    for m, want in ((103, 50.0), (405, 200.0)):
        for k in (1.5, 2.5):
            M, v = _subnormal_pair(m, k)
            lo, hi = _mpi(M, v[:, None], v[:, None])
            exact = _exact_row(M[0], v)
            esc = max(float(_Fr(float(lo[0, 0])) - exact) / _ETA,
                      float(exact - _Fr(float(hi[0, 0]))) / _ETA)
            assert esc == want, (
                f"m={m} k={k}: containment escape {esc} eta, banked {want}. If this is "
                "now <= 0 the defect is REPAIRED -- invert this gate, do not delete it.")
    print("[ok] GAP-PIN 201: matmul_point_interval escapes containment by 50 eta "
          "(m=103) and 200 eta (m=405) -- 24.63% of the returned magnitude")


def test_gappin_201_interval_constants_Y0_is_below_the_quantity_it_bounds():
    """GAP-PIN (leg 201). The defect reaches the certificate's own returned constant.

    `Y_0` is documented as a RIGOROUS UPPER BOUND on `max_i w_i |(A F(z))_i|`.  On a
    synthetic linear system (identity Jacobian -- the most favourable case there is) whose
    `A @ F` products are subnormal, it comes back 19.66% BELOW that quantity at m = 405,
    and 18.99% below at m = 103.  No exception; the result still carries `rigorous: True`.

    Leg 98's `_containment_screen` cannot see this and is not expected to: it compares the
    enclosure against a FLOAT re-evaluation, which makes the SAME underflow error, so the
    screen's ratio is 0.996 -- four decades inside its 1e4 threshold.  That is two
    different defects and they stay separate (discipline 75).

    ON REPAIR: INVERT to assert `Y0 >= exact` at both m."""
    from experiments.p2_route_ica2_v1_adversarial import SubnormalToy
    for m, want_pct in ((103, 18.99), (405, 19.66)):
        iv = SubnormalToy(m, 2.5)
        A = np.full((m, m), _SUB_BASE_201)
        c = interval_constants(iv, np.zeros(m), np.ones(m), np.ones(m), A=A)
        exact = float(m * _Fr(_SUB_BASE_201) * _Fr(2.5 * _SUB_BASE_201))
        pct = 100.0 * (1.0 - c["Y0"] / exact)
        assert c["Y0"] < exact, (
            f"m={m}: Y_0 = {c['Y0']!r} is now >= the exact {exact!r}. The defect is "
            "REPAIRED -- invert this gate, do not delete it.")
        assert abs(pct - want_pct) < 0.01, (
            f"m={m}: Y_0 understated by {pct:.2f}%, banked {want_pct}%")
    print("[ok] GAP-PIN 201: interval_constants returns Y_0 19.66% BELOW the quantity it "
          "claims to bound, with rigorous=True")


def test_holds_201_the_repaired_primitive_is_the_control_and_it_encloses():
    """HOLDS + CONTROL (leg 201, discipline 90). The control CAN come out the other way.

    `interval.matvec` -- leg 69's REPAIRED sibling of the routine under test -- is run on
    BYTE-IDENTICAL input and encloses correctly at every m and both rounding directions.
    That is what attributes the escape to the CLONE rather than to the data: if the input
    were simply too hard for interval arithmetic, this control would fail too.

    This gate also protects leg 69's repair itself from regressing."""
    for m in (103, 405):
        for k in (1.5, 2.5):
            M, v = _subnormal_pair(m, k)
            r = _matvec(M, Interval(v, v))
            exact = _exact_row(M[0], v)
            assert _Fr(float(r.lo[0])) <= exact <= _Fr(float(r.hi[0])), (
                f"m={m} k={k}: leg 69's eta term has REGRESSED in interval.matvec -- the "
                "control for leg 201's finding no longer holds")
    print("[ok] HOLDS 201: interval.matvec (leg 69, repaired) encloses the same "
          "byte-identical subnormal input at m=103 and m=405, both directions")


def test_holds_201_the_same_routine_is_sound_in_the_normal_range():
    """HOLDS (leg 201). The defect is BAND-SPECIFIC, and that is what scopes it.

    The identical routine on O(1) data encloses correctly. Together with the scoping
    measurement in the battery -- the live `BorderedCLM` minimum row mass is 1.63e-28,
    **292.9 decades above** the top of the subnormal band -- this is why leg 201's finding
    is LATENT: no banked number in this repository is shown to be wrong."""
    rng = np.random.default_rng(20201)
    for m in (103, 405):
        M = rng.standard_normal((1, m))
        v = rng.standard_normal(m)
        lo, hi = _mpi(M, v[:, None], v[:, None])
        exact = _exact_row(M[0], v)
        assert _Fr(float(lo[0, 0])) <= exact <= _Fr(float(hi[0, 0])), (
            f"m={m}: matmul_point_interval has lost containment in the NORMAL range. That "
            "is a far more serious defect than leg 201's and is NOT what leg 201 found.")
    print("[ok] HOLDS 201: matmul_point_interval is sound in the normal range -- "
          "the defect is band-specific, 292.9 decades below any live operand")


def test_holds_201_the_2_997_band_still_refuses_loudly():
    """HOLDS (leg 201). Leg 69's defect-2 repair holds ONE LEVEL UP.

    An oversized operand reaching `interval_constants` through the compensated residual
    path -- which is how every shipped enclosure class in this module builds `F` -- raises
    `OverflowError` out of the certificate entry point rather than returning `[nan, nan]`.
    This is the informative confirmation leg 201's NO-branch would have banked, and it
    holds even though the subnormal branch did not."""
    from experiments.p2_route_ica2_v1_adversarial import run as _run201  # noqa: F401
    big = 2.0 ** 997

    class _BigToy:
        n = N = 8

        def F_float(self, z):
            return np.full(8, big)

        def F(self, z):
            return dot2_matvec(np.full((8, 8), big), np.ones(8))

        def jacobian(self, z):
            return np.eye(8), np.eye(8)

        def bilinear_bound(self, w, nu):
            return 1.0

    try:
        interval_constants(_BigToy(), np.zeros(8), np.ones(8), np.ones(8), A=np.eye(8))
    except OverflowError as e:
        assert "2^997" in str(e)
        print("[ok] HOLDS 201: 2^997 raises OverflowError out of interval_constants, "
              "loudly -- leg 69's defect-2 repair holds one level up")
        return
    raise AssertionError(
        "interval_constants returned at 2^997 instead of raising; leg 69's defect-2 "
        "repair has regressed or been bypassed")


def test_banked_201_battery_reproduces():
    """Leg 201's headline counts are reproducible and are the numbers the writeup quotes."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from experiments.p2_route_ica2_v1_adversarial import run as run201
        data = run201(write=False, verbose=False)
    t = data["totals"]
    assert (t["cases"], t["silent_wrong"], t["sound"], t["raised"]) == (41, 11, 28, 2), (
        f"leg 201 battery totals {t}, banked cases=41 silent_wrong=11 sound=28 raised=2")
    assert data["answer"] == "YES"
    h = data["headline"]
    assert h["worst_escape_eta"] == 200.0
    assert abs(h["worst_escape_relative"] - 0.2463) < 1e-4
    assert abs(h["Y0_understated_percent"] - 19.664) < 1e-3
    assert h["reachable_from_live_operator"] is False
    print(f"[ok] leg 201 battery reproduces: {t['silent_wrong']}/{t['cases']} cases "
          f"return a non-bound silently; worst escape {h['worst_escape_eta']:.0f} eta = "
          f"{h['worst_escape_relative'] * 100:.2f}% of the returned magnitude; "
          f"Y_0 understated {h['Y0_understated_percent']:.2f}%; unreachable from any "
          "live operator (292.9 decades)")


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
    # -- leg 201 (Route-ICA2): the degenerate bands ------------------------------------
    test_gappin_201_matmul_point_interval_loses_containment_when_subnormal()
    test_gappin_201_interval_constants_Y0_is_below_the_quantity_it_bounds()
    test_holds_201_the_repaired_primitive_is_the_control_and_it_encloses()
    test_holds_201_the_same_routine_is_sound_in_the_normal_range()
    test_holds_201_the_2_997_band_still_refuses_loudly()
    test_banked_201_battery_reproduces()
    print("\nALL ADVERSARIAL GATES PASS -- 7 of them leg 98's GAP-PINs, INVERTED to "
          "assert the guard that closed the defect (12/36 false accepts -> 0/36); "
          "plus leg 201's 2 GAP-PINs pinning an OPEN defect in the subnormal band "
          "(matmul_point_interval escapes containment by 200 eta = 24.63%; Y_0 comes "
          "back 19.66% below the quantity it bounds) and 3 HOLDS. See the header.")
