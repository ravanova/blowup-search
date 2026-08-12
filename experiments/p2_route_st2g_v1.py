#!/usr/bin/env python3
"""Leg 383, Route-ST2G -- the DSSP screen's report path learns Tsai 1998's
Theorem 2 and the SS/DSS ansatz check.

WHAT THIS RUNNER MEASURES
------------------------------------------------------------------------------
Leg 359 (a048de7) flagged that leg 357's B7 screen (3f614d7) tests only L^3
convergence, missing Tsai Theorem 2's local-energy route and any SS/DSS ansatz
check, so it would misclassify a genuinely self-similar candidate at this
repo's measured decay rate. Legs 362 (ec48622) and 370 (9a3dd41) then landed
both routes as FUNCTIONS -- but as strictly opt-in arguments to
machine_read_ledger(), so the per-candidate REPORT PATH, screen_candidate(),
never called them. This runner measures the report path before and after that
rewiring, on six PRE-REGISTERED planted controls (writeup/novelty/leg_383.md,
committed at 1ca4ce5, before construction).

THE GATE, verbatim and pre-committed (DIRECTION.md cycle-11a):

  "Does the upgraded screen classify (i) Tsai's own headline example as
   REACHED by Theorem 2 (the source's decay exponent matching this repo's
   measured one, per 359), and (ii) this programme's DSS object as NOT
   REACHED with the deciding clause recorded as the exact-SS ansatz
   hypothesis -- with planted controls able to fail in both directions?"

  yes -> The screen stops under-warning; every future candidate report carries
         the two new columns. CEILING: TIER 2 -- surviving a screen is not
         evidence for existence.
  no  -> A planted control fails to fire: stop, report verbatim, never widen
         (the 361 lesson).

The BEFORE column is produced by calling machine_read_ledger() with its
original two positional arguments -- which is literally what screen_candidate()
did on main at 104f5b3 -- so the "before" is a re-measurement, not a
recollection.

    .venv/bin/python experiments/p2_route_st2g_v1.py

CEILING: TIER 2. This is a screening instrument. Surviving it is not evidence
for existence, and CLAY_OBLIGATIONS Sec 6's two no-method obligations stay OPEN
regardless of this gate's answer. Clay odds unchanged, ~0.05%.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from solver.dssp_biot_savart import field_uB  # noqa: E402
from solver.dssp_screen import (  # noqa: E402
    machine_read_ledger,
    screen_candidate,
)
from test_dssp_screen_t2 import (  # noqa: E402
    LADDER,
    NQ,
    _periodic_dss_trajectory,
    field_c1_tsai_headline,
    field_c3_exponent_minus_two,
    field_c4_tends_to_nonzero_constant,
    field_c6_growing,
)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_st2g_v1.json")

# Tsai 1998's headline example (1.5) has decay exponent exactly -1; leg 359
# banked this repo's own measured exponent on leg 351's Type-I Biot-Savart
# witness as -0.9971. Both are re-measured here, not recited.
TSAI_SOURCE_EXPONENT = -1.0

CONTROLS = [
    ("C1", "Tsai 1998's headline example (1.5), U(y) = A(y/|y|)/|y|, exponent -1",
     field_c1_tsai_headline, None, "FIRE", "EXCLUDED-BY-T2"),
    ("C2", "this programme's DSS object: leg 351's field_uB with a genuinely "
           "periodic lambda>1 trajectory under the rescaled flow",
     field_uB, "dss", "FIRE", "NOT-REACHED-BY-ANSATZ"),
    ("C3", "planted exponent -2 field, L^3 genuinely convergent",
     field_c3_exponent_minus_two, None, "FIRE", "EXCLUDED-BY-T1"),
    ("C4", "planted field tending to a NONZERO constant at infinity "
           "(anti-tautology control)",
     field_c4_tends_to_nonzero_constant, None, "SILENT", "NOT EXCLUDED"),
    ("C5", "the C1 field read through the ansatz column alone: the ansatz "
           "clause must not be a catch-all",
     field_c1_tsai_headline, None, "SILENT", "EXCLUDED-BY-T2"),
    ("C6", "planted field GROWING like |y|, reached by no theorem in the ledger",
     field_c6_growing, None, "SILENT", "NOT EXCLUDED"),
]


def _run_one(field_fn, trajectory):
    if trajectory == "dss":
        s, c = _periodic_dss_trajectory()
        res = screen_candidate(field_fn, s_vals=s, c_vals=c, R_hi_ladder=LADDER, **NQ)
    else:
        res = screen_candidate(field_fn, R_hi_ladder=LADDER, **NQ)
    # The BEFORE column: exactly the two-positional-argument call that
    # screen_candidate() made on main at 104f5b3.
    before = machine_read_ledger(res["l3_norm"], res["lambda"])
    return res, before


def main() -> int:
    t0 = time.time()
    rows = []
    all_pass = True

    for tag, desc, field_fn, trajectory, direction, expected in CONTROLS:
        res, before = _run_one(field_fn, trajectory)
        row_after = res["ledger"]["NRS_Tsai"]
        decay = res["far_field_decay"]
        l3 = res["l3_norm"]

        if tag == "C5":
            # C5's assertion is about the ansatz column, not the verdict.
            fired = res["ss_ansatz"]["ansatz"] != "EXACT-SS"
            passed = (res["ss_ansatz"]["ansatz"] == "EXACT-SS"
                       and res["ss_ansatz"]["satisfies_theorem_ansatz"] is True
                       and row_after["verdict"] != "NOT-REACHED-BY-ANSATZ")
        else:
            fired = bool(row_after["excludes"]) or row_after["verdict"] == "NOT-REACHED-BY-ANSATZ"
            passed = row_after["verdict"] == expected

        all_pass = all_pass and passed
        rows.append({
            "id": tag,
            "description": desc,
            "required_direction": direction,
            "expected_verdict": expected,
            "verdict_before_rewiring": before["NRS_Tsai"]["verdict"],
            "verdict_after_rewiring": row_after["verdict"],
            "control_passes": bool(passed),
            "fired": bool(fired),
            "fitted_decay_exponent": decay["fitted_exponent"],
            "first_sampled_magnitude": decay["magnitudes"][0],
            "last_sampled_magnitude": decay["magnitudes"][-1],
            "l3_converged": bool(l3["converged"]),
            "l3_norm": l3["L3_norm"],
            "l3_rel_change_last_step": l3["rel_change_last_step"],
            "l3_rel_tol": l3["rel_tol"],
            "theorem2_decays_to_zero": res["theorem2_decay_to_zero"]["decays_to_zero"],
            "ansatz": res["ss_ansatz"]["ansatz"],
            "satisfies_theorem_ansatz": res["ss_ansatz"]["satisfies_theorem_ansatz"],
            "measured_lambda": res["lambda"]["lambda"],
            "measured_S0": res["lambda"]["S0"],
            "deciding_clause": row_after.get("deciding_clause"),
        })

    by_id = {r["id"]: r for r in rows}

    # --- the gate's clause (i): the source's exponent against this repo's ----
    c1_exp = by_id["C1"]["fitted_decay_exponent"]
    repo_exp = by_id["C2"]["fitted_decay_exponent"]
    clause_i = {
        "control": "C1",
        "tsai_source_exponent_eq_1_5": TSAI_SOURCE_EXPONENT,
        "planted_field_fitted_exponent": c1_exp,
        "abs_difference_planted_vs_source": abs(c1_exp - TSAI_SOURCE_EXPONENT),
        "repo_measured_exponent_on_field_uB": repo_exp,
        "abs_difference_repo_vs_source": abs(repo_exp - TSAI_SOURCE_EXPONENT),
        "leg_359_banked_repo_exponent": -0.9971,
        "verdict_before_rewiring": by_id["C1"]["verdict_before_rewiring"],
        "verdict_after_rewiring": by_id["C1"]["verdict_after_rewiring"],
        "reached_by_theorem_2": by_id["C1"]["verdict_after_rewiring"] == "EXCLUDED-BY-T2",
        "deciding_clause": by_id["C1"]["deciding_clause"],
    }

    # --- the gate's clause (ii): DSS object, deciding clause = ansatz -------
    c2 = by_id["C2"]
    clause_ii = {
        "control": "C2",
        "measured_lambda": c2["measured_lambda"],
        "measured_S0": c2["measured_S0"],
        "ansatz": c2["ansatz"],
        "satisfies_theorem_ansatz": c2["satisfies_theorem_ansatz"],
        "verdict_after_rewiring": c2["verdict_after_rewiring"],
        "not_reached": c2["verdict_after_rewiring"] == "NOT-REACHED-BY-ANSATZ",
        "deciding_clause_is_exact_ss_ansatz": bool(
            c2["deciding_clause"] is not None
            and "(1.2)" in c2["deciding_clause"]
            and "EXACT" in c2["deciding_clause"]),
        "deciding_clause": c2["deciding_clause"],
    }

    # --- the gate's qualifier: both directions available --------------------
    fired_ids = [r["id"] for r in rows if r["required_direction"] == "FIRE"]
    silent_ids = [r["id"] for r in rows if r["required_direction"] == "SILENT"]
    verdicts_reachable = sorted({r["verdict_after_rewiring"] for r in rows})
    both_directions = {
        "controls_required_to_fire": fired_ids,
        "controls_required_to_stay_silent": silent_ids,
        "all_four_verdicts_reachable_through_report_path": verdicts_reachable,
        "battery_is_two_directional": bool(
            len(fired_ids) >= 2 and len(silent_ids) >= 2
            and set(verdicts_reachable) >= {"EXCLUDED-BY-T1", "EXCLUDED-BY-T2",
                                             "NOT-REACHED-BY-ANSATZ", "NOT EXCLUDED"}),
    }

    gate_yes = bool(all_pass
                     and clause_i["reached_by_theorem_2"]
                     and clause_ii["not_reached"]
                     and clause_ii["deciding_clause_is_exact_ss_ansatz"]
                     and both_directions["battery_is_two_directional"])

    payload = {
        "leg": 383,
        "route": "ROUTE-ST2G",
        "title": ("the DSSP screen's REPORT PATH learns Tsai 1998 Theorem 2 "
                   "and the SS/DSS ansatz check"),
        "base_commit": "104f5b3",
        "novelty_pre_registration_commit": "1ca4ce5",
        "ceiling": ("TIER 2. Surviving a screen is not evidence for existence. "
                     "CLAY_OBLIGATIONS Sec 6's two no-method obligations stay OPEN "
                     "regardless of this gate's answer. Clay odds unchanged, ~0.05%."),
        "gate_question": (
            "Does the upgraded screen classify (i) Tsai's own headline example as "
            "REACHED by Theorem 2 (the source's decay exponent matching this repo's "
            "measured one, per 359), and (ii) this programme's DSS object as NOT "
            "REACHED with the deciding clause recorded as the exact-SS ansatz "
            "hypothesis -- with planted controls able to fail in both directions?"),
        "gate_answer": "YES" if gate_yes else "NO",
        "what_was_already_built_and_not_rebuilt": {
            "ec48622": ("leg 362: decays_to_zero_at_infinity(), classify_ss_ansatz(), "
                         "_ledger_nrs_tsai_three_way() -- as OPT-IN arguments"),
            "9a3dd41": ("leg 370: morrey_ball_average_sweep(), ledger_morrey() -- "
                         "also opt-in; left opt-in here, not wired into the report "
                         "path (a separate, far more expensive ball-average pass)"),
            "3bfe677": "leg 366: q=3 row re-attributed to NRS 1996, not Tsai Thm 1",
        },
        "the_gap_this_leg_closed": (
            "screen_candidate() -- the single end-to-end path producing a candidate "
            "report -- computed the far-field decay exponent and then dropped it, "
            "calling machine_read_ledger(l3, lam) with two positional arguments, and "
            "never computed the ansatz classification at all. Measured on main at "
            "104f5b3: a planted exact-SS field at fitted exponent "
            f"{c1_exp!r} with a log-divergent L^3 ladder was reported "
            f"{by_id['C1']['verdict_before_rewiring']!r}, while Tsai 1998 Theorem 2 "
            "excludes it outright. Both columns are now unconditional in the report "
            "path; machine_read_ledger()'s own signature and defaults are untouched."),
        "gate_clause_i_tsai_headline": clause_i,
        "gate_clause_ii_dss_object": clause_ii,
        "gate_qualifier_both_directions": both_directions,
        "controls": rows,
        "all_controls_pass": bool(all_pass),
        "scope_call_leg_382_enclosure": (
            "solver/dssp_decay_enclosure.py (leg 382, 104f5b3) provides a CERTIFIED "
            "interval-arithmetic far-field decay enclosure. It was read and "
            "deliberately NOT wired in: this gate is about whether the screen "
            "CLASSIFIES correctly, not about the rigor of the exponent it classifies "
            "on, and swapping the estimator mid-leg would move the numbers under the "
            "planted controls. The fitted column stays in place, unchanged, per "
            "dispatch. Left as an open clause for a successor: a second, CERTIFIED "
            "T2 column driven by the enclosure."),
        "runtime_seconds": round(time.time() - t0, 3),
    }

    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=2)

    print(f"GATE ANSWER: {payload['gate_answer']}")
    print(f"  clause (i)  C1 exponent {c1_exp!r} vs Tsai's exact "
          f"{TSAI_SOURCE_EXPONENT} (|diff| {clause_i['abs_difference_planted_vs_source']:.3e}); "
          f"repo's own {repo_exp!r} (|diff| {clause_i['abs_difference_repo_vs_source']:.3e}); "
          f"{by_id['C1']['verdict_before_rewiring']} -> {by_id['C1']['verdict_after_rewiring']}")
    print(f"  clause (ii) C2 lambda {c2['measured_lambda']!r} -> "
          f"{c2['verdict_after_rewiring']}, deciding clause is the exact-SS ansatz: "
          f"{clause_ii['deciding_clause_is_exact_ss_ansatz']}")
    for r in rows:
        print(f"  {r['id']} [{r['required_direction']:6s}] "
              f"expected {r['expected_verdict']:22s} got "
              f"{r['verdict_after_rewiring']:22s} pass={r['control_passes']}")
    print(f"  both-directional battery: {both_directions['battery_is_two_directional']}, "
          f"verdicts reachable: {verdicts_reachable}")
    print(f"wrote {OUT}")
    return 0 if gate_yes else 1


if __name__ == "__main__":
    raise SystemExit(main())
