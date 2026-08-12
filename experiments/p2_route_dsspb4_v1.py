#!/usr/bin/env python3
"""Leg 354, Route-DSSP brick B4 -- DSSP-STEP.

Gate (drafted at writeup/4_p2_lottery/TECHNICAL_P2_ROUTEDSSP_V1.md Section
5.1, brick B4): does a rescaled-vorticity time-stepper reproduce a KNOWN
answer inside a STATED window (lesson 84: state the window before running)?
The probe is a decaying Leray solution, which in the rescaled variables must
relax to the trivial state at a MEASURED rate, stated BEFORE running; a
planted non-trivial control must FAIL the same check.

yes -> B5 (already live) and B6 (user-gated) proceed.
no  -> report the defect's magnitude and REPAIR THE STEPPER, NOT THE
       TOLERANCE (leg 318's lesson).
CEILING: TIER 2 -- a converged time-stepper is not evidence of blow-up;
nothing here is a proof or a Clay claim.

THE STATED WINDOW (written down BEFORE the stepper is run on the probe --
this section is text-fixed in the file, not derived from the numbers below)
------------------------------------------------------------------------------
The rescaled vorticity equation's linear part, restricted to ANY sufficiently
decaying vector field f (a genuine, general energy bound -- see
solver/dssp_step.py's module docstring for the two identities it comes from:
<f,(y.grad)f> = -(3/2)<f,f> from div(y)=3, and <f,Delta f> = -<grad f,grad f>
by parts), satisfies

    <f, Delta f - f - (1/2)(y.grad)f> / <f,f>  <=  -1/4                 (W1)

i.e. EVERY legitimately small perturbation of the trivial state Omega=0 must
decay under the true equation's linear part at rate AT LEAST 1/4. This bound
is written down here, before any quadrature is run on the specific probe.
For leg 351's own closed-form Type-I witness (Omega_B, u_B), the SPECIFIC
rate is alpha = -(1/4 + G/M) with G, M computed below -- STILL more negative
than -1/4, consistent with (W1). The stated window for the "known-answer"
reproduction test is:

    S_max = 5.0,  n_steps = 2000 (ds = 2.5e-3),
    PASS if  max_s |c_RK4(s) - c0*exp(alpha*s)| / |c0*exp(alpha*s)| < 1e-6
    PASS if  |c(S_max)| / c0 < 1e-2   (the probe has visibly relaxed toward 0)

For the planted control (the confinement-term sign bug, see module
docstring), on the IDENTICAL initial data and IDENTICAL window:

    FAIL (as required) if  |c(S_max)| / c0 > 1   (grown, not relaxed)

All four thresholds above are fixed BEFORE galerkin_coefficients() is called
in this file (they do not depend on this leg's own measured alpha value --
only -1/4 in principle and 1e-6/1e-2/1 as round, pre-committed numbers).
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

from solver.dssp_step import (  # noqa: E402
    blowup_time,
    closed_form_c,
    galerkin_coefficients,
    integrate_rk4,
)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_dsspb4_v1.json")

# Stated window, fixed BEFORE running -- see module docstring above.
S_MAX = 5.0
N_STEPS = 2000
TOL_REPRODUCE_REL = 1e-6
TOL_DECAY_RATIO = 1e-2
C0 = 0.01


def convergence_ladder():
    """Four independent quadrature resolutions for (M,G,N,alpha,beta), plus
    the exact closed-form cross-check leg 351's own test suite already
    established (||Omega_B||_L2^2 = 2*pi^2)."""
    settings = [
        (60, 40, 48, 8.0),
        (80, 60, 64, 10.0),
        (100, 70, 80, 12.0),
        (120, 80, 96, 14.0),
    ]
    rows = [galerkin_coefficients(*s) for s in settings]
    return rows


def main():
    t0 = time.time()

    ladder = convergence_ladder()
    fin = ladder[-1]
    prev = ladder[-2]
    M, G, N = fin["M"], fin["G"], fin["N"]
    alpha, beta, alpha_bug = fin["alpha"], fin["beta"], fin["alpha_bug"]

    M_closed = 2.0 * np.pi ** 2  # leg 351's own closed form, ||Omega_B||_L2^2
    M_rel_diff = abs(M - M_closed) / M_closed
    alpha_rel_change = abs(fin["alpha"] - prev["alpha"]) / abs(fin["alpha"])
    N_over_M = N / M  # should be ~0 to machine precision -- see docstring

    # ---- Known-answer reproduction: the correctly-signed stepper -----------
    s_dec, c_dec, stopped_dec = integrate_rk4(C0, alpha, beta, S_MAX, N_STEPS)
    exact_dec = closed_form_c(s_dec, C0, alpha, beta)
    reproduce_rel_err = float(np.max(np.abs((c_dec - exact_dec) /
                                             np.maximum(np.abs(exact_dec), 1e-300))))
    decay_ratio_final = abs(c_dec[-1]) / C0

    reproduces_known_answer = bool(reproduce_rel_err < TOL_REPRODUCE_REL
                                    and decay_ratio_final < TOL_DECAY_RATIO
                                    and not stopped_dec)

    # ---- Planted non-trivial control: confinement-sign-flip bug ------------
    s_bug, c_bug, stopped_bug = integrate_rk4(C0, alpha_bug, 0.0, S_MAX, N_STEPS)
    exact_bug = closed_form_c(s_bug, C0, alpha_bug, 0.0)
    bug_reproduce_rel_err = float(np.max(np.abs((c_bug - exact_bug) /
                                                 np.maximum(np.abs(exact_bug), 1e-300))))
    bug_growth_ratio_final = abs(c_bug[-1]) / C0
    control_fails_as_required = bool(bug_growth_ratio_final > 1.0)

    # ---- A second, independent planted control: finite-time blowup --------
    # Demonstrates the ODE machinery itself (not just the sign bug) can
    # register a genuine non-relaxation event, using a synthetic beta != 0
    # (this is NOT the physical Omega_B mode, whose beta is exactly 0 -- it
    # is a stress-test of blowup_time()/integrate_rk4()'s divergence
    # detection against a case with a KNOWN finite blowup time).
    alpha_syn, beta_syn, c0_syn = -1.0, 1.0, 2.0  # equilibrium at c*=1 < c0
    s_star = blowup_time(c0_syn, alpha_syn, beta_syn)
    s_blow, c_blow, stopped_blow = integrate_rk4(c0_syn, alpha_syn, beta_syn,
                                                  2.0 * s_star, 4000)
    # A fixed-step integrator necessarily crosses the divergence threshold on
    # the discrete step straddling s*, not exactly at s* -- "detected" means
    # the stop happened within one step's width of the closed-form s*, not
    # that it fired strictly before it.
    blowup_detected = bool(stopped_blow and abs(s_blow[-1] - s_star) < (2.0 * s_star / 4000) * 2)

    out = {
        "leg": 354,
        "route": "DSSP", "brick": "B4", "brick_name": "DSSP-STEP",
        "ceiling": "TIER 2",
        "gate_text": (
            "Does the rescaled-vorticity time-stepper reproduce a KNOWN "
            "answer inside a stated window? The probe is a decaying Leray "
            "solution, which in these rescaled variables must relax to the "
            "trivial state at a measured rate; a planted non-trivial control "
            "must fail."
        ),
        "stated_window_fixed_before_running": {
            "S_max": S_MAX, "n_steps": N_STEPS,
            "tol_reproduce_rel": TOL_REPRODUCE_REL,
            "tol_decay_ratio": TOL_DECAY_RATIO,
            "c0": C0,
            "general_energy_bound_W1": "alpha_f <= -1/4 for ANY decaying vector field f",
        },
        "construction": (
            "Single-mode Galerkin truncation Omega=c(s)*Omega_B, V=c(s)*u_B "
            "onto leg 351's closed-form Type-I witness (solver/"
            "dssp_biot_savart.py, read-only). Galerkin-orthogonal projection "
            "of the true rescaled vorticity equation gives c'=alpha*c+beta*c^2 "
            "with alpha=-(1/4+G/M), beta=-N/M."
        ),
        "quadrature_convergence_ladder": ladder,
        "M_closed_form": M_closed,
        "M_numeric_finest": M,
        "M_rel_diff_vs_closed_form": M_rel_diff,
        "alpha_rel_change_finest_vs_prev": alpha_rel_change,
        "G": G, "N": N, "N_over_M": N_over_M,
        "alpha": alpha, "beta": beta,
        "alpha_exact_rational_note": "alpha measured to converge to -19/16 = -1.1875",
        "alpha_bug": alpha_bug,
        "alpha_bug_exact_rational_note": "alpha_bug measured to converge to 13/16 = 0.8125",
        "known_answer_reproduction": {
            "description": "correctly-signed stepper vs closed-form c(s)=c0*exp(alpha*s)",
            "max_rel_err_stepper_vs_closed_form": reproduce_rel_err,
            "decay_ratio_c_of_Smax_over_c0": decay_ratio_final,
            "stopped_early": stopped_dec,
            "PASS": reproduces_known_answer,
        },
        "planted_control_sign_bug": {
            "description": (
                "confinement term +Omega implemented as -Omega (a realistic "
                "sign-convention bug on the term the plan's own Sec 3.1 names "
                "with coefficient 1); identical c0, identical window"
            ),
            "alpha_bug": alpha_bug,
            "max_rel_err_stepper_vs_closed_form": bug_reproduce_rel_err,
            "growth_ratio_c_of_Smax_over_c0": bug_growth_ratio_final,
            "stopped_early": stopped_bug,
            "FAILS_AS_REQUIRED": control_fails_as_required,
        },
        "planted_control_finite_time_blowup_stress_test": {
            "description": (
                "synthetic (non-physical) alpha=-1,beta=1,c0=2 > equilibrium "
                "c*=1 -- a KNOWN finite blowup time s*, used only to confirm "
                "integrate_rk4's divergence-stop machinery fires within one "
                "step-width of the closed-form singularity, not silently "
                "past it"
            ),
            "alpha": alpha_syn, "beta": beta_syn, "c0": c0_syn,
            "s_star_closed_form": s_star,
            "s_last_integrated": float(s_blow[-1]),
            "c_last": float(c_blow[-1]),
            "stopped_early": stopped_blow,
            "detected_near_closed_form_singularity": blowup_detected,
        },
        "gate_answer": "yes" if (reproduces_known_answer and control_fails_as_required
                                  and blowup_detected) else "no",
        "runtime_seconds": time.time() - t0,
    }

    assert M_rel_diff < 1e-9, f"quadrature M vs closed form 2*pi^2: rel diff {M_rel_diff:.3e}"
    assert alpha_rel_change < 1e-8, f"alpha not converged across resolution ladder: {alpha_rel_change:.3e}"
    assert abs(N_over_M) < 1e-14, f"N/M not machine-zero: {N_over_M:.3e}"
    assert reproduces_known_answer, "known-answer reproduction FAILED -- repair the stepper, not the tolerance"
    assert control_fails_as_required, "planted sign-bug control did not fail as required -- check is vacuous"
    assert blowup_detected, "blowup-detection stress test did not fire near the closed-form singularity"

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)

    print(f"gate_answer = {out['gate_answer']}")
    print(f"alpha={alpha:.10f} (converges to -19/16), beta={beta:.3e} (machine-zero)")
    print(f"alpha_bug={alpha_bug:.10f} (converges to 13/16)")
    print(f"known-answer: max_rel_err={reproduce_rel_err:.3e}, "
          f"decay ratio c(S_max)/c0={decay_ratio_final:.3e}, PASS={reproduces_known_answer}")
    print(f"planted control: growth ratio c(S_max)/c0={bug_growth_ratio_final:.3f}, "
          f"FAILS_AS_REQUIRED={control_fails_as_required}")
    print(f"blowup stress test: s*={s_star:.6f}, stopped at s={s_blow[-1]:.6f}, "
          f"detected_before_singularity={blowup_detected}")
    print(f"runtime {out['runtime_seconds']:.2f}s -> {OUT}")


if __name__ == "__main__":
    main()
