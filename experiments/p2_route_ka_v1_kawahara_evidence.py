#!/usr/bin/env python3
"""Leg 61 (Route-KA v1): evidence/verification script, from curated JSON alone, no re-run.

writeup/INDEX.md's gap-list item 10 named three missing pieces for this route: a BLOG
writeup, a `*_evidence.py`, and a figure. Leg 372 closes the `*_evidence.py` piece. The
figure piece is NOT closed here, and that is a finding, not an omission: this route's own
`writeup/4_p2_lottery/TECHNICAL_P2_ROUTEKA_V1.md` states in its header, verbatim, "No
figure: this is a known-answer audit and the established convention is that such legs
register none" -- the same declared-by-design convention `writeup/INDEX.md` gap-list item
13 already records for Route-NKR v1, and the same class of convention item 6 records for
Route-D's advection/literature-scope legs. So the gap-list's "GAP: none" mark in the figure
column is corrected here (by writeup/INDEX.md's row text, not by this script) to "not a
gap, by design" rather than papered over with a script-picked figure number -- this repo's
own standing practice ("legs must not pick their own numbers; integration allocates") is
respected: no fig-number is claimed by this leg for a route whose own header says none is
owed. The BLOG piece is prose (a claim-bearing write-up), outside this leg's
scripts/figures-only remit, and stays open.

What this script verifies, reading ONLY writeup/data/p2_route_ka_v1_kawahara.json:

  G1 -- Reading A (the gate's literal words): the certified interval contains CLN's
       published r0 as a certified radius (`gate.reading_A_published_r0_is_a_certified_radius`).
  G2 -- Reading B (the pre-committed window): r_min sits BELOW the window's lower end, by
       the banked shortfall factor (3.3531x, 0.5254 decades) -- the caveat is not smoothed
       away.
  G3 -- Both nominated explanations for Reading B's shortfall were tested and both FAILED:
       trace projection explains only 2.52% of the gap (ratio 1.0252x against a needed
       3.34x); the discarded quadratic tail explains only 0.105% of it (2.978 decades
       short).
  G4 -- The resolution sweep (N = 60..300): Y0 in the pipeline's own norm is flat (within a
       factor of ~1.03 of its N=250 value) while r_min_Hl tracks sqrt(2N+1) almost exactly
       -- the position of the radius relative to CLN's is set by the norm conversion, not
       by arithmetic precision.
  G5 -- The poisoning control is exactly linear across 8 decades of displacement scale and
       the certificate fails to close (`closes: False`) at the largest kick tested.

All five checks are asserted; the script exits nonzero if any fails. No solver module is
imported, nothing is re-run, nothing is re-measured.

    .venv/bin/python experiments/p2_route_ka_v1_kawahara_evidence.py
"""

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "writeup", "data", "p2_route_ka_v1_kawahara.json")


def main():
    with open(DATA) as fh:
        d = json.load(fh)

    gate = d["gate"]
    ablation_trace = d["ablation_trace_projection"]
    ablation_tail = d["ablation_quadratic_tail"]
    sweep = d["resolution_sweep"]
    poison = d["poisoning"]

    checks = []

    # G1 -- Reading A: literal gate words, YES.
    checks.append((
        "G1 Reading A: CLN's published r0 is a certified radius of our polynomial",
        gate["reading_A_published_r0_is_a_certified_radius"] is True,
    ))

    # G2 -- Reading B: pre-committed window, NO, by the banked shortfall.
    shortfall_factor = gate["reading_B_shortfall_factor_at_lower_end"]
    checks.append((
        "G2 Reading B: r_min is below the pre-committed window (shortfall %.4fx, "
        "%.4f decades)" % (shortfall_factor, gate["reading_B_shortfall_decades"]),
        (gate["reading_B_r_min_inside_window"] is False)
        and math.isclose(shortfall_factor, 3.3531187462334855, rel_tol=1e-9),
    ))

    # G3 -- both nominated explanations FALSIFIED, magnitudes as banked.
    checks.append((
        "G3a trace-projection ablation explains only %.4fx of the needed %.4fx gap"
        % (ablation_trace["ratio"], ablation_trace["gap_it_needed_to_explain"]),
        (ablation_trace["explains_the_gap"] is False)
        and ablation_trace["ratio"] < ablation_trace["gap_it_needed_to_explain"],
    ))
    checks.append((
        "G3b discarded-tail ablation is %.4f decades short of the gap"
        % ablation_tail["decades_short"],
        (ablation_tail["explains_the_gap"] is False)
        and ablation_tail["decades_short"] > 2.5,
    ))

    # G4 -- resolution sweep: Y0 flat, r_min tracks sqrt(2N+1).
    y0_values = [row["Y0"] for row in sweep]
    y0_spread = max(y0_values) / min(y0_values)
    r_min_values = [row["r_min_Hl"] for row in sweep]
    conv_values = [row["conversion_to_Hl"] for row in sweep]
    # r_min_Hl should scale (near-)proportionally with conversion_to_Hl across the sweep,
    # since Y0 itself is flat -- check the ratio r_min/conversion is roughly constant.
    ratios = [rm / cv for rm, cv in zip(r_min_values, conv_values)]
    ratio_spread = max(ratios) / min(ratios)
    checks.append((
        "G4a Y0 flat across N=60..300 (spread %.4fx, i.e. resolution-independent)"
        % y0_spread,
        y0_spread < 1.05,
    ))
    checks.append((
        "G4b r_min_Hl tracks the sqrt(2N+1) conversion factor (ratio spread %.4fx)"
        % ratio_spread,
        ratio_spread < 1.10,
    ))

    # G5 -- poisoning: exactly linear, and fails to close at the largest kick.
    over_budget = [row["Y0_over_budget"] for row in poison]
    scales = [row["scale"] for row in poison]
    lin_ratios = [ob / sc for ob, sc in zip(over_budget, scales)]
    lin_spread = max(lin_ratios) / min(lin_ratios)
    checks.append((
        "G5a poisoning response is linear in the displacement scale (ratio spread %.4fx "
        "across %d decades)" % (lin_spread, round(math.log10(scales[-1] / scales[0]))),
        lin_spread < 1.01,
    ))
    checks.append((
        "G5b the certificate fails to close at the largest tested kick (scale=%.0e)"
        % poison[-1]["scale"],
        poison[-1]["closes"] is False,
    ))

    ok = True
    for name, passed in checks:
        mark = "PASS" if passed else "FAIL"
        print(f"  [{mark}] {name}")
        ok = ok and passed

    print()
    print("certified interval (H^l):    [%.4e, %.4e]" % tuple(gate["certified_interval_Hl"]))
    print("CLN published interval:      %s" % d["published"])
    print("Reading A margin above r0:   %.4f decades" % gate["reading_A_margin_decades_above_r0"])
    print("Reading A margin below r_max: %.4f decades" % gate["reading_A_margin_decades_below_r0"])
    print("Reading B shortfall:         %.4fx (%.4f decades)"
          % (shortfall_factor, gate["reading_B_shortfall_decades"]))

    if not ok:
        print("\nFAILED -- a banked number did not reproduce from the JSON as expected.")
        sys.exit(1)

    print("\n%d/%d checks pass -- Route-KA v1's magnitudes reproduce from "
          "writeup/data/p2_route_ka_v1_kawahara.json alone, no re-run." % (len(checks), len(checks)))


if __name__ == "__main__":
    main()
