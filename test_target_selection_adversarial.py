"""GAP-PINS for solver/target_selection.py -- leg 208, Route-TSA.  Gate answered YES.

THIS SUITE PINS A DEFECT.  IT DOES NOT ASSERT CORRECTNESS.
-----------------------------------------------------------------------------
Every assertion below records behaviour that is WRONG, so that a repair makes this file
FAIL LOUDLY rather than pass quietly.  That is the `test_nk_fourier_adversarial.py`
GAP-PIN convention (legs 79 / 98 / 116 / 128), and the reason for it is that the defect
is claim-adjacent: `solver/target_selection.py` may not be edited by this leg, so the
only honest artifact is an executable statement of what it currently does.

**IF YOU ARE HERE BECAUSE THIS FILE FAILED, THAT IS PROBABLY GOOD NEWS.**  Read
`experiments/journal/leg_208.md`, confirm the failure is a repair and not a drift, and
then delete the pin it broke and replace it with the positive assertion.

WHAT IS PINNED, AND WHAT IS EXPLICITLY NOT
-----------------------------------------------------------------------------
Pinned: the ARITHMETIC screen (`y0_budget`, `radii_polynomial`, `unknowns`), which the
landed `test_target_selection.py` exercises on four admissible `(Z1, Z2)` pairs and
nothing else.

NOT pinned: the LEDGER verdicts (`uncertified_targets`, `gate_verdict`).  They are
unguarded internally, but `test_target_selection.py` already catches both plants this
leg tried (see `battery_g` in the runner), and a second copy of a working gate is not a
gate.  `test_pinned_ledger_cover_still_exists` below asserts that cover is still there,
so if the drift suite ever loses it this file says so.

Run: .venv/bin/python test_target_selection_adversarial.py
"""

import math

import numpy as np

from solver.target_selection import (
    gate_verdict, radii_polynomial, unknowns, y0_budget,
)

_PIN = "GAP-PIN (leg 208, Route-TSA) MOVED:"

NAN, INF = float("nan"), float("inf")


# ---------------------------------------------------------------------------
# GAP-PIN A -- y0_budget is blind to the sign of (1 - Z1)
# ---------------------------------------------------------------------------

def test_gap_y0_budget_is_sign_blind_in_one_minus_Z1():
    """`(1 - Z1)^2` is invariant under `Z1 -> 2 - Z1`, and nothing checks `Z1 < 1`.

    `Z1 >= 1` means `A` is not an approximate inverse.  `radii_polynomial` knows this and
    refuses.  `y0_budget` -- which the module's own docstring calls "the number that makes
    'is it within interval-arithmetic reach?' a measurement rather than an opinion" --
    hands back a finite positive budget where the true budget is exactly zero.
    """
    # the mirror identity.  EXACT for dyadic x, where 1 +/- x is representable; for
    # x = 0.1 and 0.9 the two sides differ by <= 1.11e-16, which is the float
    # representation of 0.9/1.1 and NOT a property of the function.  Pinned at the
    # strength the measurement actually supports (banked in the runner's mirror_pairs).
    for x in (0.25, 0.5, 0.75):
        lo, hi = y0_budget(1.0 - x, 1.0), y0_budget(1.0 + x, 1.0)
        assert lo == hi, f"{_PIN} y0_budget no longer mirrors exactly at x={x}: {lo} vs {hi}"
    for x in (0.1, 0.9):
        lo, hi = y0_budget(1.0 - x, 1.0), y0_budget(1.0 + x, 1.0)
        assert abs(lo - hi) <= 1.2e-16 and abs(lo - hi) / max(lo, hi) < 1e-14, \
            f"{_PIN} y0_budget mirror at x={x} moved beyond rounding: {lo} vs {hi}"

    # the sharpest case: maximally-not-an-inverse gets a PERFECT inverse's budget
    assert y0_budget(2.0, 1.0) == y0_budget(0.0, 1.0) == 0.5, \
        f"{_PIN} y0_budget(2.0, 1.0) = {y0_budget(2.0, 1.0)}"

    # Z1 = 1 exactly is the one boundary it gets right, and that is worth pinning too
    assert y0_budget(1.0, 1.0) == 0.0, f"{_PIN} y0_budget(1.0, 1.0) moved off zero"

    positive_outside = [Z1 for Z1 in (1.1, 1.25, 1.5, 2.0, 3.0, 5.0)
                        if y0_budget(Z1, 1.0) > 0.0]
    assert len(positive_outside) == 6, \
        f"{_PIN} expected 6 outside-theorem Z1 with a positive budget, got {positive_outside}"
    print(f"    y0_budget(2.0,1.0) = {y0_budget(2.0,1.0)} = y0_budget(0.0,1.0); "
          f"true budget at Z1=2 is 0")
    print("[ok] GAP-PIN A: y0_budget is sign-blind in (1 - Z1); 6/6 forbidden Z1 "
          "return a positive budget")


# ---------------------------------------------------------------------------
# GAP-PIN B -- radii_polynomial accepts forbidden constants
# ---------------------------------------------------------------------------

FORBIDDEN = {
    "Z2_negative_unit":   (1e-3,  0.5, -1.0),
    "Z2_negative_large":  (1e-3,  0.5, -1e4),
    "Y0_negative_unit":   (-1.0,  0.5,  1.0),
    "Y0_negative_small":  (-1e-6, 0.5,  1.0),
    "Y0_negative_huge":   (-1e6,  0.5,  1.0),
    "Z1_negative_unit":   (1e-3, -1.0,  1.0),
    "Z1_negative_large":  (1e-3, -3.0,  1.0),
    "Y0_and_Z1_negative": (-1.0, -1.0,  1.0),
    "all_three_negative": (-1.0, -1.0, -1.0),
}


def test_gap_radii_polynomial_accepts_forbidden_constants():
    """Y0, Z1, Z2 are NORMS -- the module's own comment above `radii_polynomial` says so.

    It guards `Z1 >= 1`, `disc < 0` and `a <= 0`.  It never guards a SIGN.  Same guard
    class as port_certification (79), interval_certificate (98), nk_bounds (116) and
    nk_fourier (pinned).  This is the SIXTH member, and the one
    `solver/certificate_guards.py`'s census never enumerated.
    """
    out = {k: radii_polynomial(*v) for k, v in FORBIDDEN.items()}
    n_feasible = sum(1 for r in out.values() if r["feasible"])
    assert n_feasible == 9, f"{_PIN} expected 9/9 forbidden triples feasible, got {n_feasible}"

    neg = {k: float(r["r_min"]) for k, r in out.items()
           if r["feasible"] and r["r_min"] is not None
           and not math.isnan(float(r["r_min"])) and float(r["r_min"]) < 0.0}
    assert set(neg) == {"Y0_negative_unit", "Y0_negative_small", "Y0_negative_huge",
                        "Y0_and_Z1_negative", "all_three_negative"}, \
        f"{_PIN} negative-radius set moved: {sorted(neg)}"
    assert neg["Y0_negative_unit"] == -1.0, \
        f"{_PIN} unit negative radius moved: {neg['Y0_negative_unit']}"
    # the sharpest: r_min = -(sqrt(0.25 + 2e6) - 0.5) from the quadratic branch, NOT
    # -Y0 -- the polynomial is still a quadratic here (Z2 = 1), so the radius is the
    # root, not the residual.  Pinned at the measured value.
    assert abs(neg["Y0_negative_huge"] - (-1413.71365076144)) < 1e-9, \
        f"{_PIN} sharpest negative radius moved: {neg['Y0_negative_huge']}"
    assert abs(neg["all_three_negative"] - (-0.5)) < 1e-15, \
        f"{_PIN} all_three_negative radius moved: {neg['all_three_negative']}"

    # the reason string that contradicts its own input
    for k in ("Z2_negative_unit", "Z2_negative_large"):
        assert out[k]["reason"] == "Z2 = 0, affine", \
            f"{_PIN} {k} reason moved: {out[k]['reason']!r}"
    print(f"    9/9 forbidden triples feasible; 5 with a negative certified radius, "
          f"worst r_min = {neg['Y0_negative_huge']:.6g}; two report 'Z2 = 0, affine' "
          f"for Z2 = -1 and -1e4")
    print("[ok] GAP-PIN B: radii_polynomial validates no sign")


def test_nan_and_inf_are_refused_but_for_the_wrong_reason():
    """The BENIGN direction, pinned so it is never inflated into a soundness failure.

    NaN reaches `feasible = r_min < min(r_max, r_cap)`, which is False because every
    ordered comparison with NaN is False -- not because anything checked.  The row still
    says `reason = 'ok'` and carries `r_min = nan`.
    """
    with np.errstate(invalid="ignore"):
        for label, args in (("Y0_nan", (NAN, 0.5, 1.0)),
                            ("Z1_nan", (1e-3, NAN, 1.0)),
                            ("Z2_nan", (1e-3, 0.5, NAN)),
                            ("Y0_inf", (INF, 0.5, 1.0))):
            r = radii_polynomial(*args)
            assert not r["feasible"], f"{_PIN} {label} became feasible"
        r = radii_polynomial(NAN, 0.5, 1.0)
    assert r["reason"] == "ok", f"{_PIN} the mislabelled NaN reason moved: {r['reason']!r}"
    assert math.isnan(float(r["r_min"])), f"{_PIN} NaN r_min moved"
    print("    NaN/inf refused (feasible=False) but with reason='ok' and r_min=nan")
    print("[ok] NaN/inf land in the benign direction, by accident rather than by a guard")


# ---------------------------------------------------------------------------
# GAP-PIN C -- a correct refusal that still ships a favourable magnitude
# ---------------------------------------------------------------------------

def test_gap_correct_Z1_refusal_still_reports_spare_headroom():
    """`out` is assembled BEFORE the `Z1 >= 1` guard, so the budget fields survive it.

    This repository quotes `Y0_over_budget` as its magnitude (`p2_route_l1_v1_interval.py`
    line 115, `p2_route_port_v1_bordered.json`).  Here the boolean is right and the
    number is wrong, which is the harder failure to notice.
    """
    r = radii_polynomial(0.1, 2.0, 1.0)
    assert r["feasible"] is False, f"{_PIN} the Z1 >= 1 refusal itself has moved"
    assert r["reason"].startswith("Z1 >= 1"), f"{_PIN} reason moved: {r['reason']!r}"
    assert r["Y0_budget"] == 0.5, f"{_PIN} leaked budget moved: {r['Y0_budget']}"
    assert abs(r["Y0_over_budget"] - 0.2) < 1e-15, \
        f"{_PIN} leaked Y0_over_budget moved: {r['Y0_over_budget']}"
    n = sum(1 for Z1 in (1.0, 1.1, 1.5, 2.0, 3.0)
            if radii_polynomial(0.1, Z1, 1.0)["Y0_over_budget"] < 1.0)
    assert n == 3, f"{_PIN} expected 3 refusals reporting spare headroom, got {n}"
    print("    at Z1=2.0: feasible=False (correct) alongside Y0_over_budget=0.2 "
          "(reads as 5x headroom)")
    print("[ok] GAP-PIN C: 3/5 correct refusals ship a favourable magnitude")


# ---------------------------------------------------------------------------
# GAP-PIN D -- unknowns truncates a fractional dimension silently
# ---------------------------------------------------------------------------

def test_gap_unknowns_truncates_a_fractional_dimension():
    """"Exact unknown count ... No fudge factors" -- and `int(dim)` throws away 598.5x.

    Q2's entire discriminator is the unknown count, so a dimension that arrives as
    1.9 instead of 2 screens a 2D object as 1D and understates its cost by the full
    factor of `n_per_dim`.
    """
    u19, u2, u1 = (unknowns(1.9, 2, 600, 3), unknowns(2, 2, 600, 3),
                   unknowns(1, 2, 600, 3))
    assert u19 == u1 == 1203, f"{_PIN} truncated count moved: {u19}"
    assert u2 == 720003, f"{_PIN} dim-2 count moved: {u2}"
    assert abs(u2 / u19 - 598.5062344139651) < 1e-9, \
        f"{_PIN} understatement factor moved: {u2 / u19}"

    # a negative dim returns a FLOAT from a function documented as an exact count
    neg = unknowns(-1, 2, 600, 3)
    assert not isinstance(neg, int), f"{_PIN} unknowns(-1,...) now returns an int"
    assert abs(neg - 3.0033333333333334) < 1e-12, f"{_PIN} negative-dim value moved: {neg}"

    # the one loud degenerate case, pinned so a repair does not quietly remove it
    try:
        unknowns(NAN, 2, 600, 3)
        raise AssertionError(f"{_PIN} unknowns(nan, ...) no longer raises")
    except ValueError:
        pass
    print(f"    unknowns(1.9,2,600,3) = {u19} (the dim-1 answer) vs {u2} for dim 2 "
          f"-- {u2 / u19:.1f}x understatement; unknowns(-1,...) = {neg} (a float)")
    print("[ok] GAP-PIN D: a fractional dimension is truncated silently")


# ---------------------------------------------------------------------------
# the cover that DOES exist, asserted so its loss is visible
# ---------------------------------------------------------------------------

def test_pinned_ledger_cover_still_exists():
    """The ledger half is covered by the landed drift suite, and this pins that fact.

    Leg 208 planted two wrong values (a CAP-certified object marked `NO`; the ledger
    reordered out of rank order).  `gate_verdict` absorbed both silently, and
    `test_target_selection.py` caught both.  If that suite ever stops catching them, the
    ledger half becomes as exposed as the arithmetic half, and this assertion says so.
    """
    import copy
    import contextlib
    import io

    import solver.target_selection as ts
    import test_target_selection as T

    orig = copy.deepcopy(ts.TARGET_LEDGER)
    try:
        next(t for t in ts.TARGET_LEDGER
             if t["id"] == "Boussinesq_ChenHou")["certified"] = "NO"
        caught = False
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                T.test_certification_record_is_consistent_with_the_ledger()
        except AssertionError:
            caught = True
        assert caught, (f"{_PIN} test_target_selection.py NO LONGER catches a "
                        f"CAP-certified object marked uncertified -- the ledger half "
                        f"has lost its only cover")

        ts.TARGET_LEDGER[:] = sorted(copy.deepcopy(orig), key=lambda t: -t["rank"])
        caught = False
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                T.test_gate_is_decisive_and_names_a_live_target()
        except AssertionError:
            caught = True
        assert caught, (f"{_PIN} test_target_selection.py NO LONGER catches a reordered "
                        f"ledger -- gate_verdict's unsorted live[0] is now unguarded")
    finally:
        ts.TARGET_LEDGER[:] = copy.deepcopy(orig)

    g = gate_verdict()
    assert g["named_target"] == "HL_S2_nonsymmetric" and g["gate"] == "YES", \
        f"{_PIN} the ledger was not restored cleanly: {g}"
    print("    both plants still caught by test_target_selection.py; ledger restored")
    print("[ok] the ledger half's external cover is intact")


# ---------------------------------------------------------------------------
# the CONTROL, in the suite as well as the runner (lesson 90)
# ---------------------------------------------------------------------------

def test_control_shared_guard_rejects_what_target_selection_accepts():
    """Same tuples, two readers.  If both accepted, the finding would be about the tuples.

    `solver/certificate_guards.py` is leg 128's repaired predicate for exactly this
    theorem.  It rejects 9/9 of the triples `target_selection` accepts 9/9 of -- and it
    passes the admissible ones, so it is not simply a function that says no.
    """
    from solver.certificate_guards import hypothesis_violations

    n_reject = 0
    for Y0, Z1, Z2 in FORBIDDEN.values():
        if hypothesis_violations((("Y_0", Y0), ("Z_1", Z1), ("Z_2", Z2))):
            n_reject += 1
    assert n_reject == 9, f"{_PIN} shared guard rejects {n_reject}/9, not 9/9"

    n_accept = sum(1 for v in FORBIDDEN.values() if radii_polynomial(*v)["feasible"])
    assert n_accept == 9, f"{_PIN} target_selection accepts {n_accept}/9, not 9/9"

    for Y0, Z1, Z2 in ((1e-8, 0.3, 1e3), (1e-12, 0.05, 1.0), (1e-6, 0.9, 1e-2)):
        assert not hypothesis_violations((("Y_0", Y0), ("Z_1", Z1), ("Z_2", Z2))), \
            f"{_PIN} the shared guard rejects an ADMISSIBLE triple ({Y0}, {Z1}, {Z2})"
        assert radii_polynomial(Y0, Z1, Z2)["feasible"], \
            f"{_PIN} target_selection refuses an admissible triple"
    print("    shared guard 9/9 reject, target_selection 9/9 accept, 3/3 admissible "
          "pass both")
    print("[ok] the control is informative: the tuples are forbidden, the guard is the "
          "difference")


if __name__ == "__main__":
    test_gap_y0_budget_is_sign_blind_in_one_minus_Z1()
    test_gap_radii_polynomial_accepts_forbidden_constants()
    test_nan_and_inf_are_refused_but_for_the_wrong_reason()
    test_gap_correct_Z1_refusal_still_reports_spare_headroom()
    test_gap_unknowns_truncates_a_fractional_dimension()
    test_pinned_ledger_cover_still_exists()
    test_control_shared_guard_rejects_what_target_selection_accepts()
    print("\nALL GAP-PINS HOLD -- solver/target_selection.py is UNREPAIRED, as expected "
          "for a leg whose gate answered YES and which may not patch its target.")
