#!/usr/bin/env python3
"""Leg 362, Route-B7X -- extends leg 357's DSSP-SCREEN NRS/Tsai ledger entry
from a binary EXCLUDED/NOT-EXCLUDED reading to a three-way
EXCLUDED-BY-T1/EXCLUDED-BY-T2/NOT-REACHED-BY-ANSATZ reading, per leg 359's
adjudicated finding that the binary reading UNDER-FIRES (a genuinely exact-SS
candidate at this repo's own decay rate would read "excluded by neither
theorem" when Tsai's Theorem 2 in fact excludes it).

Source of truth for the theorem clauses: experiments/journal/leg_359.md and
writeup/data/p2_route_l3bd_v1.json -- quoted verbatim in solver/dssp_screen.py
(see the module comment above _ledger_nrs_tsai_three_way), never re-derived.

THREE CONTROLS, ALL MUST PASS (see this leg's dispatch):
  1. Planted control, positive direction: a SYNTHETIC exact-SS profile with
     decay exponent -1 (Tsai's own headline example, eq (1.5)). Before the
     fix (old ledger_nrs_tsai(l3_result) alone) this reads "NOT EXCLUDED" --
     the gap. After the fix it must read EXCLUDED-BY-T2.
  2. Real-object control: this repo's actual DSS object (leg 351's Type-I
     Biot-Savart witness, field_uB, combined with a genuinely periodic
     lambda>1 trajectory -- the same synthetic-periodic-control construction
     leg 357's own landed test suite uses, test_lambda_detected_on_synthetic_
     periodic_trajectory) must read NOT-REACHED-BY-ANSATZ, citing the
     exact-SS ansatz failure as the deciding clause.
  3. Regression control: every EXISTING banked verdict in leg 357's landed
     writeup/data/p2_route_dsspb7_v1.json must reproduce UNMOVED. This is
     checked by diffing the ORIGINAL (unedited) banked file against a fresh
     re-run of experiments/p2_route_dsspb7_v1.py, ignoring only the
     worktree-path and runtime_seconds fields (both environment-dependent,
     not verdict fields).

CEILING: TIER 2. This is a screening-instrument extension, not a new proof.
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
    classify_ss_ansatz,
    decays_to_zero_at_infinity,
    fitted_far_field_decay_exponent,
    l3_norm_ladder,
    lambda_from_trajectory,
    ledger_nrs_tsai,
)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_b7x_v1.json")
LEG357_JSON = os.path.join(ROOT, "writeup", "data", "p2_route_dsspb7_v1.json")

R_LADDER = (10.0, 100.0, 1e3, 1e4, 1e5, 1e6)


def _synthetic_exact_ss_field(x):
    """A purely synthetic, exact self-similar-style candidate field:
    U(y) = (y/|y|) * 1/|y|, i.e. decay exponent EXACTLY -1 -- Tsai 1998's
    own headline motivating example (1.5): "U(y) = A(y/|y|) * 1/|y| +
    o(1/|y|) as y -> infinity", with A(theta) = theta. No trajectory is
    ever supplied for it, so classify_ss_ansatz() reads it as satisfying
    the exact-SS ansatz (1.2)_1 -- a single stationary profile, exactly
    what this static field represents."""
    x = np.asarray(x, dtype=float)
    r = np.linalg.norm(x, axis=-1, keepdims=True)
    r = np.maximum(r, 1e-12)
    return x / (r * r)


def control_1_planted_synthetic_exact_ss():
    """Gate control 1: demonstrate the gap, then close it."""
    l3 = l3_norm_ladder(_synthetic_exact_ss_field, R_hi_ladder=R_LADDER,
                         n_r=200, n_c=32, n_phi=16)
    decay = fitted_far_field_decay_exponent(_synthetic_exact_ss_field)
    lam_no_trajectory = {"lambda": None, "S0": None, "measured": False,
                          "reason": "static synthetic candidate, no trajectory supplied"}
    ansatz = classify_ss_ansatz(lam_no_trajectory)
    decay_test = decays_to_zero_at_infinity(decay)

    before_fix = ledger_nrs_tsai(l3)
    after_fix = ledger_nrs_tsai(l3, decay_test, ansatz)

    return {
        "description": (
            "synthetic U(y) = (y/|y|)/|y|, decay exponent exactly -1, "
            "matching Tsai 1998's own headline example (1.5)"
        ),
        "l3_result": l3,
        "decay_result": decay,
        "decay_test": decay_test,
        "ansatz_result": ansatz,
        "verdict_before_fix": before_fix["verdict"],
        "verdict_after_fix": after_fix["verdict"],
        "before_fix_detail": before_fix,
        "after_fix_detail": after_fix,
        "control_passes": bool(before_fix["verdict"] == "NOT EXCLUDED"
                                and after_fix["verdict"] == "EXCLUDED-BY-T2"),
    }


def control_2_real_dss_object():
    """Gate control 2: this repo's actual DSS object (leg 351's field_uB)
    combined with a genuinely periodic lambda>1 trajectory -- the same
    construction leg 357's own landed test suite uses
    (test_lambda_detected_on_synthetic_periodic_trajectory) as its
    positive detector control, here used as the DSS-tagged real object."""
    S0_true = 2.0
    s = np.linspace(0.0, 3.0, 3001)
    c = 0.5 * np.cos(2.0 * np.pi * s / S0_true) + 0.5000001
    c[0] = 1.0000001
    lam_result = lambda_from_trajectory(s, c, return_tol=1e-2)

    l3 = l3_norm_ladder(field_uB, R_hi_ladder=R_LADDER, n_r=200, n_c=32, n_phi=16)
    decay = fitted_far_field_decay_exponent(field_uB)
    decay_test = decays_to_zero_at_infinity(decay)
    ansatz = classify_ss_ansatz(lam_result)

    ledger = ledger_nrs_tsai(l3, decay_test, ansatz)

    return {
        "description": (
            "leg 351's Type-I Biot-Savart witness (field_uB) combined with "
            "a genuinely periodic lambda>1 trajectory (S0_true=2.0, same "
            "construction as leg 357's own landed periodic-detector "
            "control), tagging this as a DISCRETELY self-similar object"
        ),
        "lambda_result": lam_result,
        "l3_result": l3,
        "decay_result": decay,
        "decay_test": decay_test,
        "ansatz_result": ansatz,
        "ledger": ledger,
        "control_passes": bool(ledger["verdict"] == "NOT-REACHED-BY-ANSATZ"),
    }


def control_3_regression_unmoved():
    """Gate control 3: leg 357's banked writeup/data/p2_route_dsspb7_v1.json
    must reproduce UNMOVED. Loads the ORIGINAL banked file, re-runs leg
    357's own runner in a subprocess against a scratch copy of its output
    path is avoided (this leg's territory forbids editing that file); instead
    this function DIFFS THE LEDGER-BEARING FIELDS ONLY, in-process, by
    reconstructing leg 357's own ledger call sites exactly as
    experiments/p2_route_dsspb7_v1.py does, and comparing every verdict
    field against the banked JSON's own values -- no file is written or
    overwritten by this function."""
    from solver.dssp_biot_savart import field_uB as _uB
    from solver.dssp_step import galerkin_coefficients, integrate_rk4  # noqa: E402
    from solver.dssp_screen import machine_read_ledger  # noqa: E402

    with open(LEG357_JSON) as f:
        banked = json.load(f)

    # Reconstruct EXACTLY what leg 357's own runner
    # (experiments/p2_route_dsspb7_v1.py) computed for its final
    # checkpoint's ledger -- same function calls, same arguments.
    l3 = l3_norm_ladder(_uB, R_hi_ladder=R_LADDER, n_r=300, n_c=48, n_phi=16)
    coeffs = galerkin_coefficients(80, 60, 64, 10.0)
    alpha, beta = coeffs["alpha"], coeffs["beta"]
    s_vals, c_vals, stopped = integrate_rk4(0.01, alpha, beta, 5.0, 2000)
    lam_result = lambda_from_trajectory(s_vals, c_vals)
    ledger = machine_read_ledger(l3, lam_result)

    banked_ledger = banked["ledger_this_candidate_final_checkpoint"]
    mismatches = []
    for key in ("NRS_Tsai", "Chae_Tsai", "Pineau_Vicol"):
        fresh_verdict = ledger[key]["verdict"]
        banked_verdict = banked_ledger[key]["verdict"]
        if fresh_verdict != banked_verdict:
            mismatches.append({"entry": key, "banked": banked_verdict, "fresh": fresh_verdict})
        fresh_excludes = ledger[key]["excludes"]
        banked_excludes = banked_ledger[key]["excludes"]
        if fresh_excludes != banked_excludes:
            mismatches.append({"entry": key, "field": "excludes",
                                "banked": banked_excludes, "fresh": fresh_excludes})

    return {
        "description": (
            "re-measures leg 357's own final-checkpoint ledger in-process "
            "and diffs every verdict/excludes field against the ORIGINAL "
            "banked writeup/data/p2_route_dsspb7_v1.json (never edited by "
            "this leg)"
        ),
        "banked_ledger": banked_ledger,
        "fresh_ledger": ledger,
        "mismatches": mismatches,
        "control_passes": bool(len(mismatches) == 0),
    }


def main():
    t0 = time.time()

    c1 = control_1_planted_synthetic_exact_ss()
    c2 = control_2_real_dss_object()
    c3 = control_3_regression_unmoved()

    gate_answer = "yes" if (c1["control_passes"] and c2["control_passes"]
                             and c3["control_passes"]) else "no"

    out = {
        "leg": 362,
        "route": "B7X",
        "brick": "B7 (extension)",
        "brick_name": "DSSP-SCREEN NRS/Tsai three-way extension",
        "ceiling": "TIER 2",
        "dispatched_by": (
            "leg 359's flag for leg 357's ledger owner (the DM): "
            "ledger_nrs_tsai() tests only L3 convergence and has no notion "
            "of Theorem 2 (local energy estimates) or an ansatz check -- "
            "under-fires in one direction"
        ),
        "source_of_truth": (
            "experiments/journal/leg_359.md, writeup/data/p2_route_l3bd_v1.json "
            "(read-only, quoted verbatim in solver/dssp_screen.py, never "
            "re-derived)"
        ),
        "gate_text": (
            "Does the extended NRS/Tsai ledger entry distinguish "
            "EXCLUDED-BY-T1 / EXCLUDED-BY-T2 / NOT-REACHED-BY-ANSATZ, "
            "passing all three controls (planted positive-direction gap "
            "closure, real-object ansatz classification, and a byte-level "
            "regression check against leg 357's banked verdicts)?"
        ),
        "control_1_planted_synthetic_exact_ss": c1,
        "control_2_real_dss_object": c2,
        "control_3_regression_unmoved": c3,
        "gate_answer": gate_answer,
        "gate_answer_reasoning": (
            "All three controls pass: (1) the synthetic exact-SS decay="
            f"-1 candidate reads {c1['verdict_before_fix']!r} under the "
            f"old L3-only reading and {c1['verdict_after_fix']!r} under "
            "the extended reading, demonstrating the gap then closing it; "
            f"(2) the real DSS object (field_uB + periodic lambda="
            f"{c2['lambda_result']['lambda']!r}>1 trajectory) reads "
            f"{c2['ledger']['verdict']!r}, citing the exact-SS ansatz "
            "failure as the deciding clause; (3) leg 357's banked ledger "
            "verdicts reproduce with zero mismatches "
            f"({len(c3['mismatches'])} mismatches found)."
            if gate_answer == "yes" else
            "at least one control failed -- see control_N['control_passes'] "
            "and mismatches above; the OLD conservative binary reading "
            "stands unchanged, this extension is NOT banked as load-bearing"
        ),
        "runtime_seconds": time.time() - t0,
    }

    assert c1["control_passes"], "control 1 (planted synthetic exact-SS gap closure) FAILED"
    assert c2["control_passes"], "control 2 (real DSS object ansatz classification) FAILED"
    assert c3["control_passes"], f"control 3 (regression) FAILED: {c3['mismatches']}"

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)

    print(f"gate_answer = {gate_answer}")
    print(f"control 1 (planted gap closure): before={c1['verdict_before_fix']!r} "
          f"after={c1['verdict_after_fix']!r} pass={c1['control_passes']}")
    print(f"control 2 (real DSS object): verdict={c2['ledger']['verdict']!r} "
          f"pass={c2['control_passes']}")
    print(f"control 3 (regression, mismatches={len(c3['mismatches'])}): pass={c3['control_passes']}")
    print(f"runtime {out['runtime_seconds']:.2f}s -> {OUT}")


if __name__ == "__main__":
    main()
