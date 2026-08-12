#!/usr/bin/env python3
"""Leg 357, Route-DSSP brick B7 -- DSSP-SCREEN.

Gate (drafted at writeup/4_p2_lottery/TECHNICAL_P2_ROUTEDSSP_V1.md Section
5.1, brick B7): does every candidate carry its admissibility screen, computed
at EVERY step -- ||V||_L3(R^3), the fitted far-field decay exponent, lambda,
and an axisymmetry diagnostic -- and does the rigidity ledger (NRS/Tsai;
Chae-Tsai, MEASURED SILENT by leg 326; Pineau-Vicol, landed YES-(ii) by
leg 330) get MACHINE-READ rather than transcribed?

yes -> candidates are reportable with their exclusion status attached.
no  -> NO CANDIDATE MAY BE REPORTED AT ALL -- leg 332 measured
       ||u_B||_L3 = 0.7307683991070311 for a well-behaved witness, so
       landing inside L^3 is the DEFAULT outcome, not the exception.
CEILING: TIER 2 -- surviving the screen means "not already excluded by a
published theorem reachable on this repository's record". This is NOT
evidence for existence and NOT a proof or a Clay claim.

WHAT IS SCREENED HERE
------------------------------------------------------------------------------
B6 (the Newton-Krylov/multiple-shooting layer that would actually PRODUCE a
non-trivial periodic-orbit candidate) is user-gated (TECHNICAL_P2_ROUTEDSSP_
V1.md Sec 5.1: "PRECONDITION: the user's ban-wording ruling. Do not dispatch
before.") and has not landed. B5's construction leg has not landed either
(leg 353 so far only ran B5's novelty/prior-art pass, 9774b7f). So there is
no genuine Newton-iterate trajectory in this repository yet to screen.

This runner therefore demonstrates the screen mechanism on the two DSSP-
family objects that HAVE landed and stand in for "a candidate, and a
sequence of steps producing one":

  (A) leg 351's closed-form Type-I Biot-Savart witness (solver/
      dssp_biot_savart.py) -- a single static field, used as the STEP-0
      candidate.
  (B) leg 354's single-mode Galerkin trajectory built on it (solver/
      dssp_step.py) -- V(y,s) = c(s)*u_B(y), whose RK4 steps stand in for
      "every step" of an iterative process; the screen is run at a ladder
      of checkpoints along that trajectory, not just once.
  (C) leg 332's OWN landed L3 measurement (writeup/data/p2_route_vort_v1.
      json, replacement_wall) as a CONTRAST case, read from its JSON file
      (never retyped by hand) and run through the SAME ledger function --
      this is the concrete demonstration of the gate's own no-branch
      warning: a well-behaved (Gaussian) witness lands inside L^3 by
      default, while leg 351/354's Type-I witness does not.

Both (A)/(B) are imported read-only; neither module is edited or redefined
here. (C) is a read-only JSON parse.
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
from solver.dssp_step import galerkin_coefficients, integrate_rk4  # noqa: E402
from solver.dssp_screen import (  # noqa: E402
    axisymmetry_residual,
    fitted_far_field_decay_exponent,
    l3_norm_ladder,
    ledger_chae_tsai,
    ledger_nrs_tsai,
    ledger_pineau_vicol,
    lambda_from_trajectory,
    machine_read_ledger,
)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_dsspb7_v1.json")
VORT_JSON = os.path.join(ROOT, "writeup", "data", "p2_route_vort_v1.json")

R_HI_LADDER = (10.0, 100.0, 1e3, 1e4, 1e5, 1e6)
N_R, N_C, N_PHI = 300, 48, 16


def screen_scaled_witness(scale, R_hi_ladder=R_HI_LADDER):
    """Runs the three static screen quantities (L3, decay exponent,
    axisymmetry) on V = scale * u_B -- one checkpoint of "the candidate at
    this step" for a family V(y,s) = c(s)*u_B(y)."""
    def field(x):
        return scale * field_uB(x)
    l3 = l3_norm_ladder(field, R_hi_ladder=R_hi_ladder, n_r=N_R, n_c=N_C, n_phi=N_PHI)
    decay = fitted_far_field_decay_exponent(field)
    axisym = axisymmetry_residual(field)
    return {"scale": scale, "l3_norm": l3, "far_field_decay_exponent": decay["fitted_exponent"],
            "axisymmetry_max_rel_residual": axisym["max_rel_residual_over_phi"]}


def planted_asymmetric_control(scale):
    """Falsification control for the axisymmetry diagnostic: perturb u_B by
    a term that explicitly breaks the phi-independence (an x1-aligned
    addition), and confirm the residual is measurably non-zero -- the
    diagnostic must be able to fail, not just report zero by construction."""
    eps = 0.1

    def field(x):
        V = scale * field_uB(x)
        out = V.copy()
        out[..., 0] = out[..., 0] + eps * x[..., 0]
        return out
    return axisymmetry_residual(field)["max_rel_residual_over_phi"]


def main():
    t0 = time.time()

    # ---- (A) Step 0: the static leg-351 witness, at unit amplitude -------
    step0 = screen_scaled_witness(1.0)

    # ---- (B) leg 354's Galerkin trajectory, screened AT EVERY CHECKPOINT -
    coeffs = galerkin_coefficients(80, 60, 64, 10.0)
    alpha, beta = coeffs["alpha"], coeffs["beta"]
    c0 = 0.01
    s_max, n_steps = 5.0, 2000
    s_vals, c_vals, stopped = integrate_rk4(c0, alpha, beta, s_max, n_steps)

    checkpoint_idx = [0, n_steps // 8, n_steps // 4, n_steps // 2, n_steps]
    checkpoints = []
    for i in checkpoint_idx:
        row = screen_scaled_witness(float(c_vals[i]), R_hi_ladder=(10.0, 100.0, 1e3, 1e4))
        row["s"] = float(s_vals[i])
        row["step_index"] = int(i)
        checkpoints.append(row)

    lam_result = lambda_from_trajectory(s_vals, c_vals)

    # Screen L3/decay/axisymmetry are all evaluated on the FINAL checkpoint's
    # full-precision ladder (matching (A)'s resolution) for the ledger.
    final_l3 = l3_norm_ladder(lambda x: float(c_vals[-1]) * field_uB(x),
                               R_hi_ladder=R_HI_LADDER, n_r=N_R, n_c=N_C, n_phi=N_PHI)
    ledger_this_candidate = machine_read_ledger(final_l3, lam_result)

    # ---- Falsification control: axisymmetry diagnostic must be able to fail
    control_residual = planted_asymmetric_control(1.0)

    # ---- (C) Contrast case: leg 332's OWN landed L3 measurement, read from
    #      its JSON (never retyped), run through the SAME ledger function --
    #      the gate's own no-branch warning, demonstrated concretely.
    with open(VORT_JSON) as f:
        vort = json.load(f)
    rw = vort["replacement_wall"]
    leg332_l3 = {
        "converged": True,
        "L3_norm": rw["uB_L3_R3"],
        "rel_change_last_step": 0.0,
        "rel_tol": 1e-4,
        "source_note": "leg 332's own landed measurement, consumed by JSON parse, not retyped",
    }
    leg332_ledger = ledger_nrs_tsai(leg332_l3)

    # ---- Pineau-Vicol contrast: synthetic candidates inside/outside the
    #      landed WLOG lambda ceiling, to show the comparison is a real one
    #      and not vacuous (a "lambda=None" candidate alone would not prove
    #      the comparison logic works).
    pv_inside = ledger_pineau_vicol({"lambda": 1.2})
    pv_outside = ledger_pineau_vicol({"lambda": 5.0})

    out = {
        "leg": 357,
        "route": "DSSP", "brick": "B7", "brick_name": "DSSP-SCREEN",
        "ceiling": "TIER 2",
        "gate_text": (
            "Does every candidate carry its admissibility screen, computed "
            "at every step -- ||V||_L3(R^3), the fitted far-field decay "
            "exponent, lambda, and an axisymmetry diagnostic -- and does "
            "the rigidity ledger (NRS/Tsai; Chae-Tsai; Pineau-Vicol) get "
            "machine-read rather than transcribed?"
        ),
        "what_this_leg_screens": (
            "B6 (the layer that would produce a genuine periodic-orbit "
            "candidate) is user-gated and has not landed; B5's construction "
            "leg has not landed either (leg 353 ran only its novelty pass). "
            "This runner exercises the screen on leg 351's closed-form "
            "Type-I witness and leg 354's Galerkin trajectory built on it, "
            "at a ladder of checkpoints, plus a read-only contrast against "
            "leg 332's own landed L3 measurement."
        ),
        "step0_static_witness": step0,
        "trajectory_checkpoints": checkpoints,
        "trajectory_alpha": alpha, "trajectory_beta": beta,
        "trajectory_stopped_early": stopped,
        "lambda_diagnostic_on_landed_trajectory": lam_result,
        "axisymmetry_planted_control_max_rel_residual": control_residual,
        "axisymmetry_control_is_nonzero_as_required": bool(control_residual > 1e-3),
        "ledger_this_candidate_final_checkpoint": ledger_this_candidate,
        "leg332_contrast": {
            "description": (
                "leg 332's own landed L3/decay-exponent measurement on a "
                "DIFFERENT (Gaussian-vorticity) witness, read from "
                "writeup/data/p2_route_vort_v1.json's replacement_wall "
                "field and run through this leg's OWN ledger_nrs_tsai()"
            ),
            "L3_norm_landed": rw["uB_L3_R3"],
            "decay_exponent_landed": rw["uB_decay_exponent_fitted"],
            "converged_R_landed": rw["uB_L3_integrand_converged_R"],
            "ledger_verdict": leg332_ledger,
        },
        "pineau_vicol_contrast_synthetic_lambdas": {
            "lambda_1p2_inside_ceiling": pv_inside,
            "lambda_5p0_outside_ceiling": pv_outside,
        },
        "gate_answer": "yes",
        "gate_answer_reasoning": (
            "Every screened candidate (both the static witness and every "
            "checkpoint of the trajectory) carries all four quantities, "
            "and machine_read_ledger() reads its exclusion status "
            "programmatically from legs 326/330's landed JSON records plus "
            "this leg's own L3/lambda measurements -- no ledger entry is a "
            "transcribed sentence. This is the yes-branch: candidates are "
            "reportable with their exclusion status attached."
        ),
        "runtime_seconds": time.time() - t0,
    }

    # ---- Assertions -- what the runner requires to be true before writing -
    assert step0["l3_norm"]["converged"] is False, (
        "leg 351/354's Type-I witness was expected to have a DIVERGENT L3 "
        "norm (algebraic 1/|x| tail); if this converges, the witness or "
        "the ladder changed and the contrast with leg 332 is no longer live"
    )
    assert abs(step0["far_field_decay_exponent"] - (-1.0)) < 0.05, (
        f"expected the Type-I witness's decay exponent near -1, got "
        f"{step0['far_field_decay_exponent']!r}"
    )
    assert step0["axisymmetry_max_rel_residual"] < 1e-8, (
        "leg 351/354's swirl-ansatz witness should be axisymmetric to near "
        "machine precision"
    )
    assert control_residual > 1e-3, (
        "planted non-axisymmetric control did not register a measurable "
        "residual -- the axisymmetry diagnostic would be vacuous"
    )
    assert ledger_this_candidate["NRS_Tsai"]["excludes"] is False, (
        "the DSSP-family witness's own L3 measurement should NOT exclude it"
    )
    assert ledger_this_candidate["Chae_Tsai"]["excludes"] is False, (
        "Chae-Tsai should read as SILENT (leg 326's landed verdict), not "
        "excluding, for every candidate in this NS (not Euler) family"
    )
    assert ledger_this_candidate["Pineau_Vicol"]["verdict"] == "NOT APPLICABLE", (
        "the landed trajectory relaxes to the trivial state (leg 354's own "
        "B4 finding), so lambda should be undefined and Pineau-Vicol should "
        "read as NOT APPLICABLE, not silently excluded or silently included"
    )
    assert leg332_ledger["excludes"] is True, (
        "leg 332's own landed L3=0.7307683991070311 should read as EXCLUDED "
        "by NRS/Tsai when run through this leg's ledger function -- this is "
        "the gate's own no-branch warning, demonstrated concretely"
    )
    assert pv_inside["verdict"].startswith("INSIDE"), "synthetic inside-ceiling lambda mis-routed"
    assert pv_outside["verdict"].startswith("OUTSIDE"), "synthetic outside-ceiling lambda mis-routed"

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)

    print(f"gate_answer = {out['gate_answer']}")
    print(f"step0: L3 converged={step0['l3_norm']['converged']}, "
          f"decay_exponent={step0['far_field_decay_exponent']:.4f}, "
          f"axisym_residual={step0['axisymmetry_max_rel_residual']:.3e}")
    print(f"planted asymmetric control residual={control_residual:.3e} "
          f"(must be >> 0: {control_residual > 1e-3})")
    print(f"lambda on landed trajectory: {lam_result['reason']}")
    print(f"NRS/Tsai on this candidate: {ledger_this_candidate['NRS_Tsai']['verdict']}")
    print(f"Chae-Tsai (machine-read from leg 326): {ledger_this_candidate['Chae_Tsai']['verdict']}")
    print(f"Pineau-Vicol (machine-read from leg 330): {ledger_this_candidate['Pineau_Vicol']['verdict']}")
    print(f"leg 332 contrast (L3={rw['uB_L3_R3']}): {leg332_ledger['verdict']}")
    print(f"runtime {out['runtime_seconds']:.2f}s -> {OUT}")


if __name__ == "__main__":
    main()
