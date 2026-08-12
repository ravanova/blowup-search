#!/usr/bin/env python3
"""Leg 128 (Route-NKR v1): evidence/verification script, from curated JSON alone, no re-run.

writeup/INDEX.md's gap-list item 13 named this route as missing a `*_evidence.py`.
`writeup/4_p2_lottery/TECHNICAL_P2_ROUTENKR_V1.md`'s own header states: "No figure: this is
a repair leg with no curve to plot, and the established convention is that such legs
register none" -- so no figure is owed or produced here, matching that stated convention
(the same class item 6 records for Route-D's advection/literature-scope legs, and the same
class this leg's own sibling script records for Route-KA v1). What is owed, and what this
closes, is the `*_evidence.py` itself: a script that reproduces the route's claimed numbers
from `writeup/data/p2_route_nkr_v1_repair.json` alone, with no solver import and no re-run.

What is verified, all read straight from the JSON:

  G1 -- gate (a): the repair moves false-accept cases from 21/105 pre-repair to 4/105
       post-repair (17 rejected), and every post-repair survivor is hypothesis-satisfying.
  G2 -- gate (a), the negative control: the leg-116 pattern reproduces on the pre-repair
       module (i.e. the adversarial battery is testing the right thing).
  G3 -- gate (a) does NOT over-claim: 0 clean-input outcomes moved (the repair changes
       nothing about honest inputs), and it does not claim all 21 false-accepts now reject
       -- only 17 of 21, the remaining 4 a named residual class, not silently dropped.
  G4 -- gate (b): the zero-regression suite is bit-identical on clean inputs across all
       4626 comparisons (worst_ulps = 0, drifted = []), and the sibling test suites all
       still pass.
  G5 -- gate (c): all three certificate-assembly modules route through the one shared
       guard and agree on every probed input.
  G6 -- the overall gate answer reproduces exactly: YES on (b) and (c), NO on (a) (because
       (a)'s clause 'a_all_false_accepts_now_reject' is False -- 4 of 21 remain, by design,
       a named class rather than a leftover).

All six checks are asserted; the script exits nonzero if any fails.

    .venv/bin/python experiments/p2_route_nkr_v1_repair_evidence.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "writeup", "data", "p2_route_nkr_v1_repair.json")


def main():
    with open(DATA) as fh:
        d = json.load(fh)

    ga = d["gate_a_rejection"]
    gb = d["gate_b_zero_regression"]
    gc = d["gate_c_routing"]
    answer = d["gate_answer"]

    checks = []

    checks.append((
        "G1 gate (a): false accepts %d/105 (pre) -> %d/105 (post), %d rejected by the "
        "repair, all post survivors hypothesis-satisfying"
        % (ga["pre_totals"]["false_accepts"], ga["post_totals"]["false_accepts"],
           ga["pre_totals"]["false_accepts"] - ga["post_totals"]["false_accepts"]),
        ga["pre_totals"]["false_accepts"] == 21
        and ga["post_totals"]["false_accepts"] == 4
        and answer["a_survivors_are_all_hypothesis_satisfying"] is True,
    ))

    checks.append((
        "G2 gate (a): negative control reproduces the leg-116 pattern on the pre-repair "
        "module",
        ga["negative_control_reproduces_leg_116"] is True
        and answer["a_negative_control_holds"] is True,
    ))

    checks.append((
        "G3 gate (a) does not over-claim: 0 clean-input outcomes moved, and "
        "a_all_false_accepts_now_reject is honestly False (4 of 21 remain, named not "
        "dropped)",
        len(ga["clean_case_outcomes_that_moved"]) == 0
        and answer["a_all_false_accepts_now_reject"] is False
        and len(ga["post_false_accept_cases"]) == 4,
    ))

    checks.append((
        "G4 gate (b): zero regression, %d/%d comparisons bit-identical, worst_ulps=%d, "
        "sibling suites all pass"
        % (gb["total_identical"], gb["total_comparisons"], gb["worst_ulps"]),
        gb["total_identical"] == gb["total_comparisons"]
        and gb["worst_ulps"] == 0
        and len(gb["drifted"]) == 0
        and gb["clean_inputs_bit_identical"] is True
        and d["gate_b_sibling_suites_all_pass"] is True,
    ))

    checks.append((
        "G5 gate (c): all three certificate-assembly modules route through one shared "
        "guard and agree on every probed input",
        gc["all_agree"] is True and gc["all_three_route_through_one_guard"] is True,
    ))

    checks.append((
        "G6 overall gate answer reproduces: YES on (b) and (c), NO on (a)",
        answer["b_clean_inputs_bit_identical"] is True
        and answer["b_sibling_suites_pass"] is True
        and answer["c_one_shared_guard"] is True
        and answer["a_all_false_accepts_now_reject"] is False
        and answer["YES"] is False,
    ))

    ok = True
    for name, passed in checks:
        mark = "PASS" if passed else "FAIL"
        print(f"  [{mark}] {name}")
        ok = ok and passed

    print()
    print("gate (a) false-accept residual class (4, named not dropped): %s"
          % ga["post_false_accept_cases"])

    if not ok:
        print("\nFAILED -- a banked number did not reproduce from the JSON as expected.")
        sys.exit(1)

    print("\n%d/%d checks pass -- Route-NKR v1's magnitudes reproduce from "
          "writeup/data/p2_route_nkr_v1_repair.json alone, no solver import, no re-run. "
          "No figure produced, matching the route's own declared "
          "'no curve to plot' convention." % (len(checks), len(checks)))


if __name__ == "__main__":
    main()
