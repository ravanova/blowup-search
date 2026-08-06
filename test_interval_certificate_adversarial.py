"""ADVERSARIAL gates for solver/interval_certificate.py -- Route-ICA, leg 98.

`test_interval_certificate.py` (legs 51-61) tests that this pipeline COMPUTES correctly:
exact rational references, bound-domination orderings, and -- since leg 61 -- a published
known answer (Cadiot-Lessard-Nave's Kawahara radius).  Every one of those gates hands the
pipeline a WELL-FORMED problem.  This file asks the other question, the one leg 79 asked of
the sibling pipeline `solver/port_certification.py`: **what does the pipeline say when the
input is not well formed?**

**LEG 98's GATE ANSWERED YES.**  Of 36 hypothesis-violating inputs, **12 were reported as a
CLOSING certificate**, and **8 of those 12 are LOAD-BEARING** -- the hypothesis-satisfying
input of the same magnitude does NOT close, so the violation is exactly what bought the
certificate.  The full battery, with every constant and every r-interval, is
`experiments/p2_route_ica_v1_adversarial.py` -> `writeup/data/p2_route_ica_v1_adversarial.json`.

**THIS FILE DOES NOT PATCH ANYTHING, AND MUST NOT BE READ AS AN ENDORSEMENT.**  Leg 98 was
declared claim-bearing and read-only on `solver/interval_certificate.py`; the repair belongs
to a bench-repair agent under the orchestrator's authority, exactly as leg 79's finding in
`port_certification.py` and leg 69's in `interval.py` were handled.  So the gates below split
into three kinds, and the kind is stated in each docstring:

  * **GAP-PIN gates** assert the DEFECTIVE behaviour as it stands today, so the defect cannot
    quietly change shape while it waits for repair (lesson 68: a finding kept in prose decays
    at the rate of memory; a finding kept as an assertion does not).  Following leg 84's
    convention verbatim: **these gates will fail the day the guard lands -- INVERT them, do
    not weaken them.**  Each one names the inversion it expects.
  * **HOLDS gates** assert the checks that ARE in place and must never regress -- notably the
    NaN and infinity handling in `radii_verdict`, and `Interval`'s own `lo <= hi` validity
    guard, which is leg 69's repair still holding the line and is the reason two of the
    poisoned-enclosure cases raise instead of lying.
  * **CONTROL gates** are the positive controls: the honest certificate must still close at a
    converged iterate and must still fail at a displaced one, so that a "nothing closes any
    more" regression cannot masquerade as robustness.

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

from experiments.p2_route_ica_v1_adversarial import (Interval, _Poisoned, _iv_shrunk,
                                                     _iv_zero, run, substrate)
from solver.interval_certificate import interval_constants, radii_verdict

# The battery's banked headline. A change here is a change in the finding, and it must be
# accompanied by a change in writeup/novelty/leg_98.md and the JSON.
BANKED = {"cases": 39, "hypothesis_violating": 36, "false_accepts": 12,
          "false_accepts_load_bearing": 8, "rejected": 20, "raised": 4}

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
# GAP-PIN -- the defect, pinned. INVERT these when the guard lands.
# --------------------------------------------------------------------------
def test_gap_negative_Y0_is_accepted():
    """GAP-PIN (H1). A NEGATIVE Y_0 closes the certificate. This is the finding.

    Y_0 = ||A F(z)|| is a norm; it cannot be negative, and the theorem says nothing about
    an input that is. The pipeline evaluates the discriminant anyway, and because a
    negative Y_0 makes the discriminant LARGER it converts a failing certificate into a
    passing one with a nonsensical NEGATIVE r_min.

    INVERSION WHEN REPAIRED: assert closes is False with a reason naming the hypothesis
    violation (the sibling returns status INVALID_INPUT), for all four values below."""
    for Y0 in (-1.0, -1e-12, -1e6, -1e-30):
        v = radii_verdict(Y0, 0.3, 1.0)
        assert v["closes"], (
            "GOOD NEWS, BAD TEST: a negative Y_0 is now rejected -- the defect leg 98 "
            "found has been repaired. INVERT this gate, do not delete it.")
    v = radii_verdict(-1.0, 0.3, 1.0)
    assert v["r_min"] < 0.0, f"expected a nonsensical negative r_min, got {v['r_min']}"
    honest = radii_verdict(1.0, 0.3, 1.0)
    assert not honest["closes"], "the |Y_0| counterpart should not close"
    print(f"[ok] GAP-PIN Y_0 < 0 accepted 4/4; at Y_0 = -1.0 the verdict is "
          f"closes=True with r_min = {v['r_min']:.4f} < 0, where Y_0 = +1.0 "
          f"(same magnitude) does NOT close on a budget of {honest['budget']:.4f}")


def test_gap_negative_Z1_is_accepted():
    """GAP-PIN (H1). A NEGATIVE Z_1 closes, and it rescues an arbitrarily large Y_0.

    Z_1 < 0 passes the `Z1 < 1.0` guard and then inflates the budget (1-Z_1)^2/(2 Z_2)
    without bound. At Z_1 = -1e6 the budget is 5e11, so Y_0 = 1e3 -- a residual a
    thousand times the size of anything this repository has ever certified -- closes.

    INVERSION WHEN REPAIRED: both cases must be refused as hypothesis violations, NOT as
    'Z_1 >= 1' (which would be the wrong reason for the right answer)."""
    v = radii_verdict(1e-12, -5.0, 1.0)
    assert v["closes"], ("GOOD NEWS, BAD TEST: a negative Z_1 is now rejected. INVERT "
                         "this gate, do not delete it.")
    hard = radii_verdict(1e3, -1e6, 1.0)
    assert hard["closes"], ("GOOD NEWS, BAD TEST: Z_1 = -1e6 no longer rescues a large "
                            "Y_0. INVERT this gate.")
    honest = radii_verdict(1e3, 1e6, 1.0)
    assert not honest["closes"], "the |Z_1| counterpart should not close"
    print(f"[ok] GAP-PIN Z_1 < 0 accepted; Z_1 = -1e6 lifts the budget to "
          f"{hard['budget']:.3e} and closes a Y_0 = 1e3 certificate that the same "
          f"magnitude Z_1 = +1e6 rejects")


def test_gap_negative_infinite_Y0_is_accepted():
    """GAP-PIN (H1). Y_0 = -inf closes, while Y_0 = +inf is refused.

    The asymmetry is the tell: nothing is checking the hypothesis, only the arithmetic.

    INVERSION WHEN REPAIRED: -inf must be refused for the same reason +inf is."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        v = radii_verdict(-np.inf, 0.3, 1.0)
        plus = radii_verdict(np.inf, 0.3, 1.0)
    assert v["closes"], ("GOOD NEWS, BAD TEST: Y_0 = -inf is now rejected. INVERT this "
                         "gate, do not delete it.")
    assert not plus["closes"], "Y_0 = +inf must stay rejected"
    assert v["r_min"] < -1e150, f"expected r_min ~ -1.3e154, got {v['r_min']}"
    print(f"[ok] GAP-PIN Y_0 = -inf closes with r_min = {v['r_min']:.3e} while "
          f"Y_0 = +inf is refused -- the guard is arithmetic, not a hypothesis check")


def test_gap_fabricated_zero_residual_enclosure_is_accepted():
    """GAP-PIN (H2). An enclosure object that reports F(z) == [0, 0] closes, at a point
    whose true residual is 5.9e-03.

    `interval_constants` never checks that the enclosure it is handed contains anything.
    The module's own docstring says containment IS gated -- but it is gated in the test
    suite, for the real enclosure class, not enforced at runtime for whatever object the
    caller passes. That distinction is the whole finding on this side of the battery.

    INVERSION WHEN REPAIRED: `interval_constants` should re-evaluate F in float at z and
    refuse an enclosure that does not contain it; assert the refusal here."""
    b, z, z_bad, w, nu, iv = _sub()
    honest = interval_constants(iv, z_bad, w, nu)
    assert not radii_verdict(honest["Y0"], honest["Z1"], honest["Z2"])["closes"]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        c = interval_constants(_Poisoned(iv, f_hook=_iv_zero), z_bad, w, nu)
        v = radii_verdict(c["Y0"], c["Z1"], c["Z2"])
    assert v["closes"], ("GOOD NEWS, BAD TEST: a fabricated zero-residual enclosure is "
                         "now rejected. INVERT this gate, do not delete it.")
    assert c["Y0"] < 1e-300, f"expected a denormal-scale fabricated Y_0, got {c['Y0']}"
    print(f"[ok] GAP-PIN a fabricated F == [0,0] enclosure gives Y_0 = {c['Y0']:.1e} "
          f"(denormal) and CLOSES at an iterate whose honest Y_0 = {honest['Y0']:.3e} "
          f"does not -- a lie of ~320 decades, undetected")


def test_gap_well_formed_non_containing_enclosure_is_accepted():
    """GAP-PIN (H2), and the sharpest case in the battery.

    This enclosure is perfectly well formed -- lo <= hi, all endpoints finite, no NaN, a
    positive width -- so EVERY validity check that exists, including leg 69's, passes it.
    It is simply the honest enclosure scaled by 1e-8, so it does not contain the residual.
    The certificate closes with a Y_0 that is 1.0e+08 times too small. No amount of
    interval-validity checking catches this one; only a containment check does.

    INVERSION WHEN REPAIRED: assert refusal, and keep the 1e-8 factor -- it is the
    measured size of the lie."""
    b, z, z_bad, w, nu, iv = _sub()
    honest = interval_constants(iv, z_bad, w, nu)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        c = interval_constants(_Poisoned(iv, f_hook=_iv_shrunk), z_bad, w, nu)
        v = radii_verdict(c["Y0"], c["Z1"], c["Z2"])
    assert v["closes"], ("GOOD NEWS, BAD TEST: a non-containing enclosure is now "
                         "rejected. INVERT this gate, do not delete it.")
    ratio = honest["Y0"] / c["Y0"]
    assert 0.5e8 < ratio < 2e8, f"expected a ~1e8 understatement, measured {ratio:.3e}"
    print(f"[ok] GAP-PIN a WELL-FORMED non-containing enclosure (lo<=hi, finite, positive "
          f"width) understates Y_0 by {ratio:.3e}x -- {honest['Y0']:.3e} -> {c['Y0']:.3e} "
          f"-- and closes; no validity check can see this, only containment")


def test_gap_negative_weight_vector_is_accepted():
    """GAP-PIN (H3). A sign-flipped weight vector is accepted as a norm.

    `w` defines the norm the certificate is stated in. Negated, it is not a norm, and the
    whole-vector case even drives Y_0 NEGATIVE (-2.5e-28) -- the one end-to-end path in
    this battery from structurally valid enclosures to a hypothesis-violating constant.

    INVERSION WHEN REPAIRED: `interval_constants` should refuse a `w` that is not strictly
    positive and finite."""
    b, z, z_bad, w, nu, iv = _sub()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        c = interval_constants(iv, z, -np.asarray(w), nu)
        v = radii_verdict(c["Y0"], c["Z1"], c["Z2"])
    assert v["closes"], ("GOOD NEWS, BAD TEST: a negative weight vector is now rejected. "
                         "INVERT this gate, do not delete it.")
    assert c["Y0"] < 0.0, f"expected a negative Y_0 from a negated weight, got {c['Y0']}"
    print(f"[ok] GAP-PIN w -> -w is accepted as a norm and yields Y_0 = {c['Y0']:.3e} < 0, "
          f"which radii_verdict then closes")


def test_gap_Z2_zero_raises_instead_of_reporting():
    """GAP-PIN, the mild one. Z_2 = 0 raises ZeroDivisionError.

    A crash is a refusal, so this is not unsound -- but it is a bare `ZeroDivisionError`
    from inside a verdict function, and a caller with a broad `except` turns it into a
    silent skip. Z_2 = 0 is not exotic: it is what an exactly-linear system gives.

    INVERSION WHEN REPAIRED: return a structured non-closing verdict naming the
    degeneracy, rather than raising."""
    for Z2 in (0.0, -0.0):
        try:
            radii_verdict(1e-12, 0.3, Z2)
        except ZeroDivisionError:
            pass
        else:
            raise AssertionError(
                "GOOD NEWS, BAD TEST: Z_2 = 0 no longer raises. INVERT this gate to "
                "assert the structured verdict that replaced it.")
    print("[ok] GAP-PIN Z_2 = 0 and Z_2 = -0.0 both raise ZeroDivisionError from inside "
          "radii_verdict rather than returning a verdict")


# --------------------------------------------------------------------------
# the battery itself, as a gate
# --------------------------------------------------------------------------
def test_banked_battery_reproduces():
    """The headline count is reproducible, and it is the number the writeup quotes.

    12/36 hypothesis-violating inputs accepted; 8 of them load-bearing. If any of these
    move, `writeup/novelty/leg_98.md` and the JSON are stale and must move with them."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        data = run(write=False, verbose=False)
    t = data["totals"]
    for k, want in BANKED.items():
        assert t[k] == want, (f"battery total {k} = {t[k]}, banked {want}. The finding "
                              f"changed; update the JSON and writeup/novelty/leg_98.md.")
    assert set(data["load_bearing_cases"]) <= set(data["false_accept_cases"])
    print(f"[ok] battery reproduces: {t['false_accepts']}/{t['hypothesis_violating']} "
          f"hypothesis-violating inputs reported a CLOSING certificate, "
          f"{t['false_accepts_load_bearing']} of them load-bearing "
          f"({t['rejected']} rejected, {t['raised']} raised)")


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
    test_gap_negative_Y0_is_accepted()
    test_gap_negative_Z1_is_accepted()
    test_gap_negative_infinite_Y0_is_accepted()
    test_gap_fabricated_zero_residual_enclosure_is_accepted()
    test_gap_well_formed_non_containing_enclosure_is_accepted()
    test_gap_negative_weight_vector_is_accepted()
    test_gap_Z2_zero_raises_instead_of_reporting()
    test_banked_battery_reproduces()
    print("\nALL ADVERSARIAL GATES PASS -- and 7 of them are GAP-PINs, pinning a DEFECT "
          "rather than endorsing it. See the header.")
