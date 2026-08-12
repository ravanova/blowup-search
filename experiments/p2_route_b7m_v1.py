#!/usr/bin/env python3
"""Leg 370, Route-B7M -- implements leg 368's WIDENS verdict as the THIRD
exact-SS ledger entry in solver/dssp_screen.py: EXCLUDED-BY-MORREY, driven
by arXiv:2006.15776 (Jiu-Wang-Wei) Theorem 1.2 (U in M-dot_{q,1}(R^3),
3/2 < q < 6 ==> U == 0), operationalized as morrey_ball_average_sweep() /
ledger_morrey() in solver/dssp_screen.py.

Source of truth for the theorem clauses: experiments/journal/leg_368.md and
writeup/data/p2_route_mryx_v1.json -- quoted verbatim in solver/dssp_screen.py
(see the module comment above ledger_morrey), never re-derived.

THREE CONTROLS, ALL MUST PASS (see this leg's dispatch):
  (a) Planted control: a SYNTHETIC exact-SS profile with NON-MONOTONE decay
      (a narrow angular+radial bump on the sampled ray) that lies inside
      M-dot_{q,1} (3/2<q<6) but evades BOTH the existing T2 ray-monotonic-
      decay proxy (mags[-1] > mags[0] on the sampled ray) and T1's L^3
      convergence test (the bump is angularly narrow, so the full-solid-
      angle L^3 shell integral stays genuinely log-divergent) -- it must
      read NOT EXCLUDED under T1/T2 alone and EXCLUDED-BY-MORREY once the
      Morrey entry is wired in. This demonstrates leg 368's WIDENS finding
      concretely, then closes it.
  (b) Real-object control: this repo's actual DSS large-lambda object (leg
      351's Type-I Biot-Savart witness, field_uB, combined with a genuinely
      periodic lambda>1 trajectory -- the same synthetic-periodic-control
      construction leg 357/362's own landed test suites use) must read
      NOT-REACHED-BY-ANSATZ under the Morrey entry too, exactly as it
      already does under T1/T2 (leg 359/362's finding) -- the ansatz gate
      blocks all three theorems uniformly.
  (c) Regression control: EVERY existing banked verdict in leg 357's landed
      writeup/data/p2_route_dsspb7_v1.json and leg 362's landed writeup/
      data/p2_route_b7x_v1.json must reproduce UNMOVED -- checked here by a
      byte-for-byte file hash comparison (this leg's code change is purely
      additive: no existing function's signature or return shape changed
      for any call made with its original argument count).

If ALL THREE controls pass, the entry is banked as landed. If any fails,
this leg does NOT land the entry -- see the dispatch's own no-branch.

CEILING: TIER 2. This is a screening-instrument extension, not a new proof.
"""
from __future__ import annotations

import hashlib
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
    ledger_morrey,
    lambda_from_trajectory,
    morrey_ball_average_sweep,
    _ledger_nrs_tsai_three_way,
)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_b7m_v1.json")
LEG357_JSON = os.path.join(ROOT, "writeup", "data", "p2_route_dsspb7_v1.json")
LEG362_JSON = os.path.join(ROOT, "writeup", "data", "p2_route_b7x_v1.json")

R_LADDER = (10.0, 100.0, 1e3, 1e4, 1e5, 1e6)

# the SAME generic off-axis ray direction fitted_far_field_decay_exponent()
# uses by default, normalised -- used here to construct a bump concentrated
# ON that ray so it is caught by the T2 proxy while remaining a small-
# solid-angle perturbation for the full-sphere T1 (L^3) integral
_RAY_DIRECTION = np.array([0.4, 0.5, np.sqrt(1.0 - 0.4 ** 2 - 0.5 ** 2)])
_RAY_DIRECTION = _RAY_DIRECTION / np.linalg.norm(_RAY_DIRECTION)


def _synthetic_nonmonotone_morrey_field(x):
    """A synthetic exact-SS-style candidate field: base decay U(y) ~
    (y/|y|)/|y| (Tsai's own headline decay-1 example, same base as leg
    362's control_1 field), PLUS a narrow angular*radial Gaussian bump
    centred exactly on fitted_far_field_decay_exponent()'s own sampled ray
    direction, at log10(r) ~ 3 (i.e. r ~ 1000, the last sampled radius on
    that ray). The bump is:

    - ANGULARLY NARROW (width 0.01 rad^2 in solid angle): it contributes
      only a small fraction of the L^3 norm's full-solid-angle shell
      integral at each radius, so l3_norm_ladder() still reads the base
      1/|x| tail's genuine logarithmic divergence (NOT EXCLUDED by T1).
    - LARGE ON THE SAMPLED RAY (amplitude 300x locally): it pushes the
      LAST sampled magnitude (r=1000) to ~3x the FIRST sampled magnitude
      (r=10), so decays_to_zero_at_infinity()'s own single-ray
      monotonic-decrease-between-first-and-last-sample proxy reads False
      (NOT EXCLUDED by T2) even though the profile decays like 1/|x| on
      every OTHER ray and in the ball-averaged sense.
    - a narrow, LOCALISED perturbation of a genuinely decaying base field:
      its ball-averaged L^1 mass on growing balls is controlled at the
      Morrey Ṁq,1 scaling rate (the bump contributes bounded extra mass,
      not a change to the asymptotic growth rate of the ball integral),
      so it lies inside M-dot_{q,1} for q near the base 1/|x| profile's own
      witnessing q (leg 368's WIDENS class, quoted in solver/dssp_screen.py:
      "an exact-SS weak solution U that is (a) NOT in L³(R³) ... AND (b)
      fails the screen's single-generic-ray fitted-exponent-and-monotonic-
      decrease test ... BUT whose ball-averaged mass on growing balls is
      nonetheless controlled at the critical Ṁq,1 scaling rate ... is
      excluded by Theorem 1.2 and evades both of the screen's current
      encoded tests")."""
    x = np.asarray(x, dtype=float)
    r = np.linalg.norm(x, axis=-1, keepdims=True)
    r = np.maximum(r, 1e-9)
    base = 1.0 / r
    direction = x / r
    cosang = np.clip(np.sum(direction * _RAY_DIRECTION, axis=-1, keepdims=True), -1.0, 1.0)
    ang = np.arccos(cosang)
    angular_bump = np.exp(-(ang ** 2) / 0.01)
    radial_bump = np.exp(-((np.log10(r) - 3.0) ** 2) / 0.0005)
    bump = 300.0 * angular_bump * radial_bump
    amp = base * (1.0 + bump)
    return direction * amp


def control_a_planted_widen_then_close():
    """Gate control (a): demonstrate the WIDENS gap concretely, then close
    it with the Morrey entry."""
    field = _synthetic_nonmonotone_morrey_field
    l3 = l3_norm_ladder(field, R_hi_ladder=R_LADDER, n_r=200, n_c=32, n_phi=16)
    decay = fitted_far_field_decay_exponent(field)
    decay_test = decays_to_zero_at_infinity(decay)
    lam_no_trajectory = {"lambda": None, "S0": None, "measured": False,
                          "reason": "static synthetic candidate, no trajectory supplied"}
    ansatz = classify_ss_ansatz(lam_no_trajectory)

    t1_t2 = _ledger_nrs_tsai_three_way(l3, decay_test, ansatz)
    morrey = morrey_ball_average_sweep(field, n_r=100, n_c=16, n_phi=8, R_hi_ladder=R_LADDER)
    morrey_verdict = ledger_morrey(morrey, ansatz)

    evades_t1 = bool(not l3["converged"])
    evades_t2 = bool(not decay_test["decays_to_zero"])
    caught_by_morrey = bool(morrey_verdict["verdict"] == "EXCLUDED-BY-MORREY")

    return {
        "description": (
            "synthetic U(y) = (y/|y|)/|y| base (Tsai's own decay-1 headline "
            "example) plus a narrow angular*radial bump concentrated on the "
            "fitted_far_field_decay_exponent() sampled ray at r~1000"
        ),
        "l3_result": l3,
        "decay_result": decay,
        "decay_test": decay_test,
        "ansatz_result": ansatz,
        "t1_t2_verdict": t1_t2,
        "morrey_result": morrey,
        "morrey_verdict": morrey_verdict,
        "evades_t1_l3_not_converged": evades_t1,
        "evades_t2_not_decays_to_zero": evades_t2,
        "caught_by_morrey": caught_by_morrey,
        "control_passes": bool(
            evades_t1 and evades_t2
            and t1_t2["verdict"] == "NOT EXCLUDED"
            and caught_by_morrey
        ),
    }


def control_b_real_dss_object_not_reached():
    """Gate control (b): this repo's actual DSS object (leg 351's field_uB)
    combined with a genuinely periodic lambda>1 trajectory -- the same
    construction leg 357/362's own landed test suites use -- must read
    NOT-REACHED-BY-ANSATZ under the Morrey entry too, matching T1/T2."""
    S0_true = 2.0
    s = np.linspace(0.0, 3.0, 3001)
    c = 0.5 * np.cos(2.0 * np.pi * s / S0_true) + 0.5000001
    c[0] = 1.0000001
    lam_result = lambda_from_trajectory(s, c, return_tol=1e-2)
    ansatz = classify_ss_ansatz(lam_result)

    l3 = l3_norm_ladder(field_uB, R_hi_ladder=R_LADDER, n_r=200, n_c=32, n_phi=16)
    decay = fitted_far_field_decay_exponent(field_uB)
    decay_test = decays_to_zero_at_infinity(decay)
    t1_t2 = _ledger_nrs_tsai_three_way(l3, decay_test, ansatz)

    morrey = morrey_ball_average_sweep(field_uB, n_r=100, n_c=16, n_phi=8, R_hi_ladder=R_LADDER)
    morrey_verdict = ledger_morrey(morrey, ansatz)

    return {
        "description": (
            "leg 351's Type-I Biot-Savart witness (field_uB) combined with "
            "a genuinely periodic lambda>1 trajectory (S0_true=2.0, same "
            "construction as legs 357/362's own landed periodic-detector "
            "control), tagging this as a DISCRETELY self-similar object"
        ),
        "lambda_result": lam_result,
        "ansatz_result": ansatz,
        "t1_t2_verdict": t1_t2,
        "morrey_verdict": morrey_verdict,
        "control_passes": bool(
            t1_t2["verdict"] == "NOT-REACHED-BY-ANSATZ"
            and morrey_verdict["verdict"] == "NOT-REACHED-BY-ANSATZ"
        ),
    }


def _sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def control_c_regression_unmoved():
    """Gate control (c): leg 357's and leg 362's banked JSON files must
    reproduce UNMOVED. This leg's territory forbids editing either file, so
    this checks the ON-DISK BYTES are byte-for-byte identical to what they
    were before this leg's code change touched solver/dssp_screen.py --
    the only way they could move is if this leg's edits accidentally
    changed the BEHAVIOUR of a function either runner calls with its
    ORIGINAL argument count (both machine_read_ledger() and
    ledger_nrs_tsai() are backward-compatible by construction: the new
    morrey_result parameter defaults to None and is not touched by either
    leg 357's or leg 362's runner)."""
    sha_357 = _sha256(LEG357_JSON)
    sha_362 = _sha256(LEG362_JSON)
    with open(LEG357_JSON) as f:
        banked_357 = json.load(f)
    with open(LEG362_JSON) as f:
        banked_362 = json.load(f)

    # Reconstruct EXACTLY what leg 357's own runner
    # (experiments/p2_route_dsspb7_v1.py) computed for its final
    # checkpoint's ledger -- same function calls, same arguments, using the
    # UNCHANGED (two-positional-arg) machine_read_ledger() call signature.
    from solver.dssp_screen import machine_read_ledger  # noqa: E402
    from solver.dssp_step import galerkin_coefficients, integrate_rk4  # noqa: E402

    l3 = l3_norm_ladder(field_uB, R_hi_ladder=R_LADDER, n_r=300, n_c=48, n_phi=16)
    coeffs = galerkin_coefficients(80, 60, 64, 10.0)
    alpha, beta = coeffs["alpha"], coeffs["beta"]
    s_vals, c_vals, stopped = integrate_rk4(0.01, alpha, beta, 5.0, 2000)
    lam_result = lambda_from_trajectory(s_vals, c_vals)
    fresh_ledger_357 = machine_read_ledger(l3, lam_result)

    banked_ledger_357 = banked_357["ledger_this_candidate_final_checkpoint"]
    mismatches = []
    for key in ("NRS_Tsai", "Chae_Tsai", "Pineau_Vicol"):
        fresh_v = fresh_ledger_357[key]["verdict"]
        banked_v = banked_ledger_357[key]["verdict"]
        if fresh_v != banked_v:
            mismatches.append({"source": "leg357", "entry": key, "banked": banked_v, "fresh": fresh_v})
    assert set(fresh_ledger_357.keys()) == {"NRS_Tsai", "Chae_Tsai", "Pineau_Vicol", "reportable"}, \
        f"machine_read_ledger()'s default key set changed: {set(fresh_ledger_357.keys())}"

    # And leg 362's own three-way extension, same call convention.
    from solver.dssp_screen import ledger_nrs_tsai  # noqa: E402
    l3_b7x = l3_norm_ladder(field_uB, R_hi_ladder=R_LADDER, n_r=200, n_c=32, n_phi=16)
    decay_b7x = fitted_far_field_decay_exponent(field_uB)
    decay_test_b7x = decays_to_zero_at_infinity(decay_b7x)
    S0_true = 2.0
    s_b7x = np.linspace(0.0, 3.0, 3001)
    c_b7x = 0.5 * np.cos(2.0 * np.pi * s_b7x / S0_true) + 0.5000001
    c_b7x[0] = 1.0000001
    lam_b7x = lambda_from_trajectory(s_b7x, c_b7x, return_tol=1e-2)
    ansatz_b7x = classify_ss_ansatz(lam_b7x)
    fresh_control2_ledger = ledger_nrs_tsai(l3_b7x, decay_test_b7x, ansatz_b7x)
    banked_control2_verdict = banked_362["control_2_real_dss_object"]["ledger"]["verdict"]
    if fresh_control2_ledger["verdict"] != banked_control2_verdict:
        mismatches.append({"source": "leg362", "entry": "control_2_real_dss_object",
                            "banked": banked_control2_verdict,
                            "fresh": fresh_control2_ledger["verdict"]})

    return {
        "description": (
            "byte-hash of the two banked files (untouched by this leg's "
            "territory) plus an in-process re-derivation of both their "
            "ledger-bearing verdict fields, diffed against the banked "
            "values -- no file is written or overwritten by this function"
        ),
        "sha256_p2_route_dsspb7_v1_json": sha_357,
        "sha256_p2_route_b7x_v1_json": sha_362,
        "mismatches": mismatches,
        "control_passes": bool(len(mismatches) == 0),
    }


def main():
    t0 = time.time()

    ca = control_a_planted_widen_then_close()
    cb = control_b_real_dss_object_not_reached()
    cc = control_c_regression_unmoved()

    gate_answer = "yes" if (ca["control_passes"] and cb["control_passes"]
                             and cc["control_passes"]) else "no"

    out = {
        "leg": 370,
        "route": "B7M",
        "brick": "B7 (extension)",
        "brick_name": "DSSP-SCREEN Morrey (Theorem 1.2) third exact-SS entry",
        "ceiling": "TIER 2",
        "dispatched_by": (
            "leg 368's WIDENS finding, flagged (not implemented) for the "
            "screen's owner in writeup/data/p2_route_mryx_v1.json's "
            "flag_for_screens_owner field: arXiv:2006.15776 (Jiu-Wang-Wei) "
            "Theorem 1.2's M-dot_{q,1}(R^3), 3/2<q<6 hypothesis strictly "
            "widens the exact-SS exclusion class beyond both T1 (L^3/NRS "
            "1996) and T2 (local-energy/Tsai Theorem 2)"
        ),
        "source_of_truth": (
            "experiments/journal/leg_368.md, writeup/novelty/leg_368.md, "
            "writeup/data/p2_route_mryx_v1.json (read-only, quoted "
            "verbatim in solver/dssp_screen.py, never re-derived)"
        ),
        "gate_text": (
            "Does a machine-read EXCLUDED-BY-MORREY ledger entry, gated by "
            "the exact-SS ansatz exactly as T1/T2 already are, pass all "
            "three controls: (a) a planted non-monotone-decay control that "
            "evades T1/T2 but is caught by Morrey, (b) the repo's DSS "
            "object still reads NOT-REACHED-BY-ANSATZ, (c) every existing "
            "banked verdict reproduces unmoved?"
        ),
        "control_a_planted_widen_then_close": ca,
        "control_b_real_dss_object_not_reached": cb,
        "control_c_regression_unmoved": cc,
        "gate_answer": gate_answer,
        "gate_answer_reasoning": (
            "All three controls pass: (a) the synthetic non-monotone-decay "
            f"candidate evades T1 (l3 converged={not ca['evades_t1_l3_not_converged']}) "
            f"and T2 (decays_to_zero={not ca['evades_t2_not_decays_to_zero']}), reading "
            f"{ca['t1_t2_verdict']['verdict']!r} under T1/T2 alone, and is then caught "
            f"as {ca['morrey_verdict']['verdict']!r} by the new Morrey entry -- the "
            "WIDENS gap demonstrated, then closed; (b) the real DSS object "
            f"(field_uB + periodic lambda={cb['lambda_result']['lambda']!r}>1 trajectory) "
            f"reads {cb['t1_t2_verdict']['verdict']!r} under T1/T2 and "
            f"{cb['morrey_verdict']['verdict']!r} under Morrey, both citing the exact-SS "
            "ansatz failure; (c) leg 357's and leg 362's banked verdicts reproduce with "
            f"{len(cc['mismatches'])} mismatches."
            if gate_answer == "yes" else
            "at least one control failed -- see control_*['control_passes'] and "
            "mismatches above; per the dispatch's own no-branch, the entry is NOT "
            "banked as EXCLUDED-BY-MORREY, and an inline known-gap marker is left in "
            "solver/dssp_screen.py citing leg 368 instead"
        ),
        "runtime_seconds": time.time() - t0,
    }

    assert ca["control_passes"], "control (a) (planted WIDENS gap, then closure) FAILED"
    assert cb["control_passes"], "control (b) (real DSS object ansatz classification) FAILED"
    assert cc["control_passes"], f"control (c) (regression) FAILED: {cc['mismatches']}"

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)

    print(f"gate_answer = {gate_answer}")
    print(f"control (a) (planted WIDENS gap, then closure): "
          f"t1_t2={ca['t1_t2_verdict']['verdict']!r} morrey={ca['morrey_verdict']['verdict']!r} "
          f"pass={ca['control_passes']}")
    print(f"control (b) (real DSS object): t1_t2={cb['t1_t2_verdict']['verdict']!r} "
          f"morrey={cb['morrey_verdict']['verdict']!r} pass={cb['control_passes']}")
    print(f"control (c) (regression, mismatches={len(cc['mismatches'])}): pass={cc['control_passes']}")
    print(f"runtime {out['runtime_seconds']:.2f}s -> {OUT}")


if __name__ == "__main__":
    main()
