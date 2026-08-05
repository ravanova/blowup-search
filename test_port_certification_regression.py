"""Leg 79 / Route-PC: the adversarial fabrication-rejection regression for the port kill-switch.

This file BANKS A MEASUREMENT. It was originally a CHARACTERISATION of a defect; it is now a
gate on that defect's ABSENCE. Read this before changing anything it asserts.

WHAT LEG 79 FOUND (2026-08-06). `capabilities.py` recorded, for solver/port_certification.py:

    "radii_polynomial_status returns BLOCKED_AT_STEP_ONE and is gated to carry NO fabricated
     Y_0 or Z_1"

A 39-case adversarial battery (experiments/p2_route_pc_v1_regression.py) split that sentence:

  * THE FIRST HALF HELD, and is gated here in test_2. Every call reaching BLOCKED_AT_STEP_ONE
    returns a dict carrying NO "Y0" and NO "Z1" key. The kill-switch does not invent numbers.

  * THE SECOND HALF DID NOT. The function performed NO domain validation on the numbers a
    caller handed it. 25 of the 39 cases are outside the hypotheses of the radii polynomial
    theorem it implements -- Y_0, Z_1, Z_2 are upper bounds on norms (van den Berg-Lessard,
    AMS Notices 62(9):1057, 2015), hence nonnegative and finite by hypothesis -- and
    **11 of those 25 (44.0%) came back with closes=True**, including the bare sign flip
    radii_polynomial_status(-1.0, 0.9, 1e4) -> closes=True against the honest
    (+1.0, 0.9, 1e4) -> closes=False.

WHAT WAS THEN FIXED. `radii_polynomial_status` now checks every supplied constant against the
theorem's own hypotheses (`_hypothesis_violations`) BEFORE the discriminant, and returns
status "INVALID_INPUT" with closes=False for a negative or non-finite Y_0, Z_1 or Z_2. The
NaN bypass of the `Z1 >= 1.0` guard goes with it: a NaN Z_1 is now rejected outright rather
than reaching EVALUATED, and it is no longer echoed back as a measured bound on the NO_Z2
branch. **All 11 false closes are now REJECTED: 0/25.** The blocked branch is tested first
and is untouched, so (None, None, <poison>) still reports BLOCKED_AT_STEP_ONE.

SO THE EXPECTATIONS BELOW NOW PIN THE CORRECTED BEHAVIOUR, not the measured defect. The 11
labels are kept, by name, as the exact set that must go on being rejected -- the historical
false-close surface is the strongest available regression target, and if any label on it ever
returns closes=True again, test_3 fails.

  (1) THE HONEST PATHS STILL WORK -- the five documented branches, unchanged by the guard.
  (2) BLOCKED_AT_STEP_ONE CARRIES NO BOUND -- the half of the claim that always held.
  (3) THE 11 HISTORICAL FALSE CLOSES ARE ALL REJECTED, by exact label, and the surface is
      empty: no case anywhere in the battery closes on a hypothesis-violating input.
  (4) THE HEADLINE MAGNITUDES agree with the committed artifact, before and after.
  (5) THE NaN GUARD BYPASS IS CLOSED -- a named floating-point hazard, no longer present.

Run: .venv/bin/python test_port_certification_regression.py
"""

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments"))

from solver.port_certification import radii_polynomial_status      # noqa: E402
from p2_route_pc_v1_regression import (                            # noqa: E402
    PRE_FIX_MEASUREMENT, pc1_honest_paths, pc2_sign_violations, pc3_nonfinite,
    pc4_type_confusion, pc5_verdict,
)

DATA = ROOT / "writeup" / "data" / "p2_route_pc_v1_regression.json"

# The 11 inputs that were MEASURED on 2026-08-06 to produce closes=True while lying outside
# the radii polynomial theorem's hypotheses. Exact, ordered as the battery emits them. Every
# one of them must now be REJECTED -- this list is the fix's regression target, and it is
# imported from the battery so the two files cannot drift.
FORMERLY_FALSE_CLOSING_LABELS = PRE_FIX_MEASUREMENT["false_close_labels"]


def _battery():
    return (pc1_honest_paths() + pc2_sign_violations()
            + pc3_nonfinite() + pc4_type_confusion())


def test_1_honest_paths_are_unchanged():
    """The five documented branches, re-gated so the guard cannot pass by breaking them."""
    assert radii_polynomial_status(None, None)["status"] == "BLOCKED_AT_STEP_ONE"
    assert radii_polynomial_status(1e-3, None)["status"] == "NO_Z1"
    assert radii_polynomial_status(1e-3, 1.2)["status"] == "Z1_EXCEEDS_ONE"
    assert radii_polynomial_status(1e-3, 0.1)["status"] == "NO_Z2"
    ok = radii_polynomial_status(1e-6, 0.1, 1.0)
    assert ok["status"] == "EVALUATED" and ok["closes"] is True, ok
    bad = radii_polynomial_status(1.0, 0.1, 1.0)
    assert bad["status"] == "EVALUATED" and bad["closes"] is False, bad
    # the boundary of the new guard: 0.0 is a legitimate bound, and so is -0.0
    edge = radii_polynomial_status(0.0, 0.0, 0.0)
    assert edge["status"] == "EVALUATED" and edge["closes"] is True, edge
    assert radii_polynomial_status(-0.0, 0.1, 1.0)["status"] == "EVALUATED"
    print("  five documented branches classify correctly; zero and -0.0 are admitted  OK")


def test_2_blocked_carries_no_fabricated_bound():
    """The half of capabilities.py's claim that ALWAYS HELD -- gated on every blocking call.

    Also gates the ORDER of the new validation: the blocked branch is tested before the
    hypothesis check, so a poisoned Z_2 alongside two missing bounds must still report
    BLOCKED_AT_STEP_ONE ("no bounds at all") rather than INVALID_INPUT ("bad bounds").
    """
    blocked = [r for r in _battery() if r["status"] == "BLOCKED_AT_STEP_ONE"]
    assert len(blocked) == 3, blocked
    for r in blocked:
        assert not r["carries_Y0"] and not r["carries_Z1"], r
        assert r["closes"] is False, r
    for args in ((None, None), (None, None, 1.0), (None, None, -1.0), (None, None, float("nan"))):
        s = radii_polynomial_status(*args)
        assert s["status"] == "BLOCKED_AT_STEP_ONE", (args, s)
        assert "Y0" not in s and "Z1" not in s, (args, s)
        assert "undefined" in s["why"], s
    print("  3/3 blocked calls carry no Y_0 and no Z_1; a poisoned Z_2 does not unblock "
          "and does not re-label  OK")


def test_3_the_fabrication_acceptance_surface_is_empty():
    """THE FIX, GATED. Every historical false close is rejected, and no new one exists.

    A failure here means radii_polynomial_status stopped enforcing the theorem's hypotheses
    on the constants a caller supplies. That is a soundness regression, not a style change:
    it converts a fabricated input into an asserted contraction.
    """
    rows = _battery()
    still_closing = [r["label"] for r in rows if r["verdict"] == "FALSE_CLOSE"]
    assert still_closing == [], (
        "the fabrication-acceptance surface is NOT EMPTY -- a hypothesis-violating input "
        f"returned closes=True: {still_closing}.\n"
        "  leg 79 measured 11 such cases on 2026-08-06 and they were all fixed; "
        "this is a soundness regression in solver/port_certification.py.")

    # every one of the 11 historically-accepted fabrications, by exact label, individually
    by_label = {r["label"]: r for r in rows}
    for label in FORMERLY_FALSE_CLOSING_LABELS:
        r = by_label[label]
        assert r["status"] == "INVALID_INPUT", (label, r)
        assert r["closes"] is False, (label, r)
        assert r["verdict"] == "REJECTED", (label, r)
        # a rejection must not report the fabrication back in a bound's slot
        assert not r["carries_Y0"] and not r["carries_Z1"], (label, r)

    # the mechanism, stated as direct calls rather than left implicit in a list
    assert radii_polynomial_status(-1e-12, 0.1, 1.0)["closes"] is False   # negative defect norm
    assert radii_polynomial_status(1.0, 0.1, -1.0)["closes"] is False     # negative Z_2
    assert radii_polynomial_status(1.0, -3.0, 1.0)["closes"] is False     # negative Z_1
    # THE SHARPEST WITNESS: the sign flip no longer overturns a genuine non-closure
    flipped = radii_polynomial_status(-1.0, 0.9, 1e4)
    honest = radii_polynomial_status(1.0, 0.9, 1e4)
    assert flipped["status"] == "INVALID_INPUT" and flipped["closes"] is False, flipped
    assert honest["status"] == "EVALUATED" and honest["closes"] is False, honest
    assert any("negative" in v for v in flipped["violations"]), flipped
    print(f"  0 fabricated inputs close; all {len(FORMERLY_FALSE_CLOSING_LABELS)} historical "
          "false closes return INVALID_INPUT, the sign flip included  OK")


def test_4_headline_magnitudes_and_artifact_agree():
    """Fresh call vs committed artifact, on the numbers the fix is reported in."""
    v = pc5_verdict(_battery())
    assert v["cases_total"] == 39, v
    assert v["cases_outside_theorem"] == 25, v
    assert v["false_closes"] == 0, v
    assert v["false_close_labels"] == [], v
    assert v["raised_loudly"] == 5, v                 # unchanged: bad TYPES still raise
    assert v["blocked_at_step_one_calls"] == 3, v
    assert v["blocked_calls_carrying_a_bound"] == 0, v
    assert v["honest_paths_still_correct"] is True, v
    assert v["gate_answer"] == "yes", v

    # the before, kept as recorded history rather than as a live expectation
    assert PRE_FIX_MEASUREMENT["false_closes"] == 11, PRE_FIX_MEASUREMENT
    assert PRE_FIX_MEASUREMENT["cases_outside_theorem"] == 25, PRE_FIX_MEASUREMENT
    assert len(FORMERLY_FALSE_CLOSING_LABELS) == 11, FORMERLY_FALSE_CLOSING_LABELS

    if not DATA.exists():
        print("  SKIP artifact comparison -- run experiments/p2_route_pc_v1_regression.py")
        return
    d = json.loads(DATA.read_text())
    for k in ("cases_total", "cases_outside_theorem", "false_closes", "raised_loudly",
              "blocked_at_step_one_calls", "blocked_calls_carrying_a_bound", "gate_answer"):
        assert d["verdict"][k] == v[k], (k, d["verdict"][k], v[k])
    assert d["verdict"]["false_close_labels"] == []
    assert d["history"]["false_close_labels"] == FORMERLY_FALSE_CLOSING_LABELS
    print("  0/25 hypothesis-violating inputs accepted, down from 11/25 (44.0%); "
          "artifact agrees and carries the before  OK")


def test_5_the_nan_guard_bypass_is_closed():
    """`Z1 >= 1.0` is False for NaN, so a NaN Z_1 used to skip the contraction guard.

    A named hazard, not a discovery: 'code comments sometimes explicitly assume that a false
    comparison implies the input is valid and within a certain range, a property that does not
    hold when the input is NaN' -- Verifying Floating-Point Programs in Stainless,
    arXiv:2601.14059. Logged in writeup/novelty/leg_79.md Q4. The guard no longer relies on
    that comparison: NaN is rejected by hypothesis, ahead of it.
    """
    nan = float("nan")
    assert not (nan >= 1.0)                       # the bypass, still there at the language level
    s = radii_polynomial_status(1e-3, nan, 1.0)
    assert s["status"] == "INVALID_INPUT", s      # ...but no longer reachable through the guard
    assert s["closes"] is False, s
    assert "discriminant" not in s, s             # nothing was evaluated on a NaN
    assert any("NaN" in v for v in s["violations"]), s
    # the NO_Z2 branch no longer reports a NaN as though it were a measured bound
    t = radii_polynomial_status(1e-3, nan)
    assert t["status"] == "INVALID_INPUT" and "Z1" not in t, t
    # both infinities are now rejected as such -- +inf used to be caught by the >= 1.0 guard,
    # which was correct by accident and only for Z_1
    for args in ((1.0, float("inf"), 1.0), (float("inf"), 0.1, 1.0), (1e-3, 0.1, float("inf")),
                 (1.0, float("-inf"), 1.0), (float("-inf"), 0.1, 1.0)):
        r = radii_polynomial_status(*args)
        assert r["status"] == "INVALID_INPUT" and r["closes"] is False, (args, r)
        assert any("infinite" in q for q in r["violations"]), (args, r)
    # and a non-real type still raises loudly rather than being classified
    for args in (("1e-6", 0.1, 1.0), (1e-6, "0.1", 1.0), (complex(1e-6, 1.0), 0.1, 1.0)):
        try:
            radii_polynomial_status(*args)
        except TypeError:
            pass
        else:
            raise AssertionError(f"a non-real constant was accepted: {args}")
    print("  NaN and both infinities are rejected by hypothesis ahead of the `>= 1.0` guard; "
          "non-real types still raise  OK (hazard closed)")


def main():
    tests = [test_1_honest_paths_are_unchanged,
             test_2_blocked_carries_no_fabricated_bound,
             test_3_the_fabrication_acceptance_surface_is_empty,
             test_4_headline_magnitudes_and_artifact_agree,
             test_5_the_nan_guard_bypass_is_closed]
    for t in tests:
        print(t.__name__)
        t()
    print("\nALL PASS -- and note what test_3 now banks: the ABSENCE of the gap leg 79 "
          "measured (11/25 -> 0/25). See the module docstring.")


if __name__ == "__main__":
    main()
