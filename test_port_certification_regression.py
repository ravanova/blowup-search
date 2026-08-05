"""Leg 79 / Route-PC: the adversarial fabrication-rejection regression for the port kill-switch.

This file BANKS A MEASUREMENT, and the measurement is a NEGATIVE one. Read this before
changing anything it asserts.

`capabilities.py` records, for solver/port_certification.py:

    "radii_polynomial_status returns BLOCKED_AT_STEP_ONE and is gated to carry NO fabricated
     Y_0 or Z_1"

Leg 79 ran a 39-case adversarial battery against that sentence
(experiments/p2_route_pc_v1_regression.py). It splits the sentence in two:

  * THE FIRST HALF HOLDS, and is gated here. Every call that reaches BLOCKED_AT_STEP_ONE
    returns a dict carrying NO "Y0" and NO "Z1" key. The kill-switch does not invent numbers.

  * THE SECOND HALF DOES NOT HOLD IN THE SENSE OF REJECTING FABRICATIONS. The function
    performs NO domain validation on the numbers a caller hands it. 25 of the 39 cases are
    outside the hypotheses of the radii polynomial theorem it implements -- Y_0, Z_1, Z_2 are
    upper bounds on norms (van den Berg-Lessard, AMS Notices 62(9):1057, 2015), hence
    nonnegative and finite by hypothesis -- and **11 of those 25 come back with
    closes=True**, i.e. the function asserts a contraction on data no certificate run could
    have produced.

THE GAP IS LATENT, NOT ACTIVE. Every caller of `radii_polynomial_status` in this repository
(experiments/p2_route_k_v1_port.py:203, experiments/p2_route_l_v1_precond.py:289) passes
(None, None) and lands on the BLOCKED branch. No stored result depends on the missing
validation. That is why leg 79 characterises the gap rather than patching it: the repair
belongs to whoever owns solver/port_certification.py, under a decision leg 79 does not have
the authority to make.

SO THIS FILE IS DELIBERATELY A CHARACTERISATION TEST. It asserts the behaviour as MEASURED on
2026-08-06, not the behaviour as DESIRED. If someone adds the missing nonnegativity/finiteness
guard to radii_polynomial_status, **test_3 and test_4 below will FAIL** -- and that failure is
the intended alarm, not a bug in this file. The correct response to that failure is to flip the
expectations here to the rejecting behaviour and to update capabilities.py's validated line in
the same commit, so the index and the code stop disagreeing.

  (1) THE HONEST PATHS STILL WORK -- the five documented branches, unchanged.
  (2) BLOCKED_AT_STEP_ONE CARRIES NO BOUND -- the half of the claim that holds.
  (3) THE FABRICATION-ACCEPTANCE SURFACE, case by case, by exact label.
  (4) THE HEADLINE MAGNITUDES agree with the committed artifact.
  (5) THE NaN GUARD BYPASS, isolated -- a named floating-point hazard, present here.

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
    pc1_honest_paths, pc2_sign_violations, pc3_nonfinite, pc4_type_confusion, pc5_verdict,
)

DATA = ROOT / "writeup" / "data" / "p2_route_pc_v1_regression.json"

# The 11 inputs that were MEASURED to produce closes=True while lying outside the radii
# polynomial theorem's hypotheses. Exact, and ordered as the battery emits them.
FALSE_CLOSE_LABELS = [
    "Y0_negative_small",
    "Y0_negative_large",
    "Y0_negative_kills_a_real_failure",
    "Z2_negative",
    "Z2_negative_huge_Y0",
    "Z1_negative",
    "Z1_very_negative",
    "Y0_neg_inf",
    "Z2_neg_inf",
    "Z1_neg_inf",
    "Y0_numpy_scalar",
]


def _battery():
    return (pc1_honest_paths() + pc2_sign_violations()
            + pc3_nonfinite() + pc4_type_confusion())


def test_1_honest_paths_are_unchanged():
    """The five documented branches, re-gated so the battery cannot pass by breaking them."""
    assert radii_polynomial_status(None, None)["status"] == "BLOCKED_AT_STEP_ONE"
    assert radii_polynomial_status(1e-3, None)["status"] == "NO_Z1"
    assert radii_polynomial_status(1e-3, 1.2)["status"] == "Z1_EXCEEDS_ONE"
    assert radii_polynomial_status(1e-3, 0.1)["status"] == "NO_Z2"
    ok = radii_polynomial_status(1e-6, 0.1, 1.0)
    assert ok["status"] == "EVALUATED" and ok["closes"] is True, ok
    bad = radii_polynomial_status(1.0, 0.1, 1.0)
    assert bad["status"] == "EVALUATED" and bad["closes"] is False, bad
    print("  five documented branches classify correctly  OK")


def test_2_blocked_carries_no_fabricated_bound():
    """The half of capabilities.py's claim that HOLDS -- gated on every blocking call."""
    blocked = [r for r in _battery() if r["status"] == "BLOCKED_AT_STEP_ONE"]
    assert len(blocked) == 3, blocked
    for r in blocked:
        assert not r["carries_Y0"] and not r["carries_Z1"], r
        assert r["closes"] is False, r
    # and directly, including with poisoned company on the third argument
    for args in ((None, None), (None, None, 1.0), (None, None, -1.0), (None, None, float("nan"))):
        s = radii_polynomial_status(*args)
        assert s["status"] == "BLOCKED_AT_STEP_ONE", (args, s)
        assert "Y0" not in s and "Z1" not in s, (args, s)
        assert "undefined" in s["why"], s
    print("  3/3 blocked calls carry no Y_0 and no Z_1; a poisoned Z_2 does not unblock  OK")


def test_3_the_fabrication_acceptance_surface_is_exactly_these_eleven():
    """CHARACTERISATION OF A KNOWN GAP -- see the module docstring before editing.

    A failure here means someone changed radii_polynomial_status. That is not forbidden; it
    means this file and capabilities.py must be updated in the same commit.
    """
    rows = _battery()
    got = [r["label"] for r in rows if r["verdict"] == "FALSE_CLOSE"]
    assert got == FALSE_CLOSE_LABELS, (
        "the fabrication-acceptance surface MOVED.\n"
        f"  measured 2026-08-06: {FALSE_CLOSE_LABELS}\n"
        f"  now:                 {got}\n"
        "If radii_polynomial_status gained a domain guard, flip these expectations AND "
        "capabilities.py's validated line in the same commit.")

    # the mechanism, stated as three direct calls rather than left implicit in a list
    assert radii_polynomial_status(-1e-12, 0.1, 1.0)["closes"] is True   # negative defect norm
    assert radii_polynomial_status(1.0, 0.1, -1.0)["closes"] is True     # negative Z_2
    assert radii_polynomial_status(1.0, -3.0, 1.0)["closes"] is True     # negative Z_1
    print(f"  {len(got)} fabricated inputs still return closes=True, by exact label  "
          "OK (gap unchanged)")


def test_4_headline_magnitudes_and_artifact_agree():
    """Fresh call vs committed artifact, on the numbers the finding is reported in."""
    v = pc5_verdict(_battery())
    assert v["cases_total"] == 39, v
    assert v["cases_outside_theorem"] == 25, v
    assert v["false_closes"] == 11, v
    assert v["raised_loudly"] == 5, v
    assert v["blocked_at_step_one_calls"] == 3, v
    assert v["blocked_calls_carrying_a_bound"] == 0, v
    assert v["honest_paths_still_correct"] is True, v
    assert v["gate_answer"] == "no", v
    assert 0.43 < v["false_close_rate_over_outside"] < 0.45, v

    if not DATA.exists():
        print("  SKIP artifact comparison -- run experiments/p2_route_pc_v1_regression.py")
        return
    d = json.loads(DATA.read_text())
    for k in ("cases_total", "cases_outside_theorem", "false_closes", "raised_loudly",
              "blocked_at_step_one_calls", "blocked_calls_carrying_a_bound", "gate_answer"):
        assert d["verdict"][k] == v[k], (k, d["verdict"][k], v[k])
    assert d["verdict"]["false_close_labels"] == FALSE_CLOSE_LABELS
    print(f"  11/25 hypothesis-violating inputs accepted "
          f"({100 * v['false_close_rate_over_outside']:.1f}%); artifact agrees  OK")


def test_5_the_nan_guard_bypass_in_isolation():
    """`Z1 >= 1.0` is False for NaN, so the contraction guard does not see a NaN Z_1.

    A named hazard, not a discovery: 'code comments sometimes explicitly assume that a false
    comparison implies the input is valid and within a certain range, a property that does not
    hold when the input is NaN' -- Verifying Floating-Point Programs in Stainless,
    arXiv:2601.14059. Logged in writeup/novelty/leg_79.md Q4.
    """
    nan = float("nan")
    assert not (nan >= 1.0)                       # the bypass, at the language level
    s = radii_polynomial_status(1e-3, nan, 1.0)
    assert s["status"] == "EVALUATED", s          # NOT Z1_EXCEEDS_ONE -- the guard was skipped
    assert s["closes"] is False, s                # saved only by NaN >= 0.0 also being False
    assert math.isnan(s["discriminant"]), s
    # and the NO_Z2 branch reports a NaN as though it were a measured bound
    t = radii_polynomial_status(1e-3, nan)
    assert t["status"] == "NO_Z2" and math.isnan(t["Z1"]), t
    # +inf, by contrast, IS caught
    assert radii_polynomial_status(1.0, float("inf"), 1.0)["status"] == "Z1_EXCEEDS_ONE"
    print("  NaN Z_1 bypasses the `>= 1.0` contraction guard and is reported as a bound on "
          "the NO_Z2 branch; +inf is caught  OK (hazard present)")


def main():
    tests = [test_1_honest_paths_are_unchanged,
             test_2_blocked_carries_no_fabricated_bound,
             test_3_the_fabrication_acceptance_surface_is_exactly_these_eleven,
             test_4_headline_magnitudes_and_artifact_agree,
             test_5_the_nan_guard_bypass_in_isolation]
    for t in tests:
        print(t.__name__)
        t()
    print("\nALL PASS -- and note what test_3 banks: a MEASURED GAP, not a clean bill of "
          "health. See the module docstring.")


if __name__ == "__main__":
    main()
