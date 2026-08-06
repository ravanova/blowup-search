"""Route-GLB v1 -- POST-REPAIR REGRESSION CHECK on solver/gclm.py (physical-space gCLM).

Leg 103. Leg 92 (Route-GLA) answered its gate YES: 19 silent corruptions in 54 gate-scoped
cases across four independent mechanisms, worst a blow-up time up to 1.5x TOO EARLY from an
ABSOLUTE zero-tolerance. It was forbidden from patching and escalated. The bench-repair
`bench/fix-gclm-silent-corruption` then landed on main (merge 0740cbf, content 6dc4e14).
This leg closes the loop -- the same pattern as legs 86, 87 and 94.

THE GATE, VERBATIM (DIRECTION.md, leg 103)
------------------------------------------
"Post-repair, does solver/gclm.py (a) no longer exhibit the early-blow-up-time bug or the
other 3 issues leg 92 found, and (b) show zero regression on its previously-validated
well-behaved test cases?"

WHY THIS IS NOT JUST RE-RUNNING LEG 92'S SCRIPT
-----------------------------------------------
`experiments/p2_route_gla_v1_adversarial.py` and its JSON are FROZEN as the pre-repair
evidence and are leg 92's territory; they are not edited or overwritten here. They also
cannot simply be re-executed: the repair converted several of the cases into `ValueError`,
and leg 92's families call the solver bare, so the script would abort at the first one.
This file re-runs THE SAME 54 CASES -- same profile, same ladders, same parameters -- with
a raise-aware wrapper, and classifies them under LEG 92'S OWN PRE-REGISTERED DEFINITIONS,
quoted here rather than restated:

  FLAGGED   -- the call raises, OR returns outcome="diverged", OR returns a result whose
               numeric payload is itself non-finite, OR returns None when None is the TRUE
               answer.  ("structural: a raise counts as FLAGGED, not silent")
  SILENT    -- an entirely finite, ordinary-looking payload that disagrees with the
               module's documented formula or an exact invariant of it, by more than the
               tolerance stated per family.  A big honest number is NOT corruption.

Because a raise was already FLAGGED under leg 92's own rule, the post-repair count is
directly comparable to its 19/54. No threshold is re-tuned in the direction that flatters
the fix: the amplitude family is scored BOTH against a freshly measured root-finder floor
AND against leg 92's own frozen threshold 2.353e-03, and the stricter verdict is reported.

PART B -- ZERO REGRESSION, MEASURED AS A BITWISE A/B, NOT ASSERTED
------------------------------------------------------------------
The pre-repair module is read straight out of git (blob `6dc4e14^:solver/gclm.py`) and
imported side-by-side with the current one. `solver/spectral_utils.py` is byte-identical
across that range (`git diff 6dc4e14^ HEAD -- solver/spectral_utils.py` is empty), so the
A/B isolates gclm.py exactly. Compared: all 20 `stage1_5_sweep.py` production T* values,
and a set of full-length production-shaped `solve_gclm` runs covering every code path a
caller uses (inviscid, viscous, linear-diffusion, frozen-u, decay-exit, blow-up detection,
max-steps). Identity is checked at the BIT level -- SHA-256 of `omega_final`'s bytes and
the hex float of every scalar -- not at some relative tolerance.

PART C -- NO OVERSHOOT: the repair's four guards must not reject admissible input.
The real `SOLVER_PARAMS` blocks of all five production sweeps are harvested from the
modules themselves (not transcribed), plus the admissible edge cases the repair explicitly
promised to keep: nu = 0.0, nu = -0.0, and O(1)-amplitude data.

This leg edits solver/gclm.py under NO outcome. It only reads it.

Run: PYTHONPATH=. .venv/bin/python experiments/p2_route_glb_v1_postrepair.py
Writes: writeup/data/p2_route_glb_v1_postrepair.json
"""

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time

import numpy as np

from solver.gclm import clm_analytic_blowup_time, solve_gclm
from solver.spectral_utils import grid, hilbert_hat, wavenumbers

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_glb_v1_postrepair.json")

GATE_VERBATIM = (
    "Post-repair, does solver/gclm.py (a) no longer exhibit the early-blow-up-time bug or "
    "the other 3 issues leg 92 found, and (b) show zero regression on its "
    "previously-validated well-behaved test cases?"
)

# Leg 92's own constants, quoted so the re-run is the SAME experiment.
N_SOLVE = 64
N_SCAN = 4096
POISONS = [("nan", float("nan")), ("+inf", float("inf")), ("-inf", float("-inf"))]
LEG92_AMPLITUDE_THRESHOLD = 2.353e-03   # leg 92's frozen, measured threshold
LEG92_NOISE_FLOOR = 2.353e-06           # leg 92's measured root-finder floor
LEG92_NU_SEPARATION = 7.364e-03         # leg 92's honest nu=0 vs nu=0.01 separation
LEG92_WORST_REL_VIOLATION = 0.3333331589781352
PREREPAIR_REV = "6dc4e14^"              # the commit just before the bench-repair


def probe_profile(x):
    """Leg 92's profile, verbatim: w0 = sin x + 0.5 sin 2x.

    Its zero-set max of H(w0) (0.5) and its GLOBAL max of H(w0) (0.75) are DIFFERENT,
    which is exactly what makes it able to see G1. For sin x alone they coincide.
    """
    return np.sin(x) + 0.5 * np.sin(2 * x)


# ---------------------------------------------------------------------------
# raise-aware call wrapper -- leg 92's rule: a raise is FLAGGED, never silent
# ---------------------------------------------------------------------------
class Raised:
    def __init__(self, exc):
        self.exc = exc
        self.type = type(exc).__name__
        self.msg = str(exc)


def attempt(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as exc:  # noqa: BLE001 -- classification, not control flow
        return Raised(exc)


def _payload_all_finite(r):
    fields = [r.omega_final, r.max_omega, r.times, r.t_final, r.mean_drift,
              r.energy_balance_residual, r.conservation_drift, r.dt_min]
    return all(bool(np.all(np.isfinite(np.asarray(f, dtype=float)))) for f in fields)


def _finite_stats(arr):
    a = np.asarray(arr, dtype=float).ravel()
    nf = int(np.sum(~np.isfinite(a)))
    fin = a[np.isfinite(a)]
    return {"size": int(a.size), "nonfinite": nf, "all_finite": nf == 0,
            "max_abs_over_finite_entries": float(np.max(np.abs(fin))) if fin.size else None}


def _raise_record(r):
    return {"raised": r.type, "raise_message_head": r.msg.split(".")[0][:160]}


# ===========================================================================
# PART A -- LEG 92'S 54 GATE-SCOPED CASES, RE-RUN AGAINST THE REPAIRED MODULE
# ===========================================================================

def family_profile_check():
    """Family 0 (out of gate): the probe's discriminating power, re-measured."""
    x = grid(N_SCAN)
    w0 = probe_profile(x)
    H = np.fft.irfft(hilbert_hat(np.fft.rfft(w0), wavenumbers(N_SCAN)), N_SCAN)
    xz = np.array([0.0, np.pi])
    Hz = -np.cos(xz) - 0.5 * np.cos(2 * xz)
    t_true = 2.0 / float(Hz.max())
    t_globalmax = 2.0 / float(H.max())
    measured = clm_analytic_blowup_time(probe_profile, n_scan=N_SCAN)
    return {
        "what": "the profile's zero-set max and global max of H differ (0.5 vs 0.75); the "
                "ratio of the two T* values is the exact size of G1's defect",
        "H_global_max": float(H.max()),
        "H_max_over_true_zero_set": float(Hz.max()),
        "T_star_exact_from_zero_set": t_true,
        "T_star_if_global_max_were_used_instead": t_globalmax,
        "ratio_globalmax_over_exact": t_globalmax / t_true,
        "measured_T_star_unit_amplitude": measured,
        "rel_error_of_measured_vs_exact": abs(measured - t_true) / t_true,
    }


def family_amplitude_invariant():
    """G1. eps * T*(eps * w0) == T*(w0) exactly, for every eps > 0.

    Leg 92's ladder verbatim: 4 calibration decades + 14 ladder points = 18 cases. Scored
    twice -- against a freshly measured root-finder floor (its procedure) and against leg
    92's own frozen 2.353e-03 (its number) -- and the stricter of the two is the verdict.
    """
    t_ref = clm_analytic_blowup_time(probe_profile, n_scan=N_SCAN)
    calib_eps = [1e-1, 1e-2, 1e-3, 1e-4]
    floor = 0.0
    calib = []
    for eps in calib_eps:
        t = clm_analytic_blowup_time(lambda x, e=eps: e * probe_profile(x), n_scan=N_SCAN)
        rel = abs(eps * t - t_ref) / abs(t_ref)
        calib.append({"eps": eps, "rel": float(rel)})
        floor = max(floor, rel)
    tol_fresh = max(floor * 1e3, 1e-12)

    eps_ladder = [1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10, 1e-11,
                  3e-12, 1e-12, 6e-13, 5e-13, 1e-14, 1e-15, 1e-18]
    cases = []
    worst = 0.0
    worst_case = None
    n_silent_fresh = 0
    n_silent_leg92 = 0
    for eps in calib_eps + eps_ladder:
        t = clm_analytic_blowup_time(lambda x, e=eps: e * probe_profile(x), n_scan=N_SCAN)
        rec = {"eps": eps, "returned_T_star": t}
        if t is None:
            rec.update({"returned_None": True, "silent_corruption": False})
        else:
            scaled = eps * t
            rel = abs(scaled - t_ref) / abs(t_ref)
            silent_fresh = bool(np.isfinite(t) and t > 0.0 and rel > tol_fresh)
            silent_92 = bool(np.isfinite(t) and t > 0.0 and rel > LEG92_AMPLITUDE_THRESHOLD)
            n_silent_fresh += int(silent_fresh)
            n_silent_leg92 += int(silent_92)
            rec.update({
                "eps_times_T_star": float(scaled),
                "reference_T_star": float(t_ref),
                "rel_violation_of_exact_scaling": float(rel),
                "silent_under_fresh_threshold": silent_fresh,
                "silent_under_leg92_frozen_threshold": silent_92,
                "silent_corruption": bool(silent_fresh or silent_92),
            })
            if rel > worst:
                worst, worst_case = rel, rec
        cases.append(rec)

    # The amplitude span is extended far beyond leg 92's ladder to show the repaired
    # tolerance is genuinely scale-free rather than merely rescaled once.
    span = []
    for eps in [1e-300, 1e-200, 1e-100, 1e-30, 1.0, 1e30, 1e100]:
        t = clm_analytic_blowup_time(lambda x, e=eps: e * probe_profile(x), n_scan=N_SCAN)
        span.append({"eps": eps,
                     "eps_times_T_star": (None if t is None else float(eps * t)),
                     "rel_violation": (None if t is None else
                                       float(abs(eps * t - t_ref) / abs(t_ref)))})

    return {
        "mechanism": "G1 -- absolute zero-tolerance |w0| < 1e-12 at the OLD gclm.py:289, "
                     "now relative: |w0| < 1e-12 * max|w0|",
        "invariant": "eps * T*(eps * w0) == T*(w0)",
        "leg92_result": {"cases_run": 18, "silent_corruptions": 11,
                         "worst_rel_violation": LEG92_WORST_REL_VIOLATION,
                         "saturation": 1.0 / 3.0,
                         "threshold_used": LEG92_AMPLITUDE_THRESHOLD,
                         "measured_noise_floor": LEG92_NOISE_FLOOR},
        "criterion_calibration": {
            "calibration_decades": calib,
            "freshly_measured_root_finder_noise_floor": float(floor),
            "fresh_threshold_used": float(tol_fresh),
            "leg92_frozen_threshold_also_applied": LEG92_AMPLITUDE_THRESHOLD,
            "verdict_is_the_stricter_of_the_two": True,
        },
        "reference_T_star": float(t_ref),
        "cases_run": len(cases),
        "silent_corruptions": max(n_silent_fresh, n_silent_leg92),
        "silent_under_fresh_threshold": n_silent_fresh,
        "silent_under_leg92_frozen_threshold": n_silent_leg92,
        "worst_rel_violation": float(worst),
        "worst_case": worst_case,
        "extended_amplitude_span_beyond_leg92": span,
        "cases": cases,
    }


def family_nan_seeded_vorticity():
    """Leg 92 measured 0/12 silent here. This must STAY 0 -- a regression channel."""
    x = grid(N_SOLVE)
    base = probe_profile(x)
    cases = []
    n_silent = 0

    def seed(idx, val):
        w = base.copy()
        w[idx] = val
        return w

    seeds = []
    for nm, val in POISONS:
        seeds.append((f"{nm} at one node (idx 7)", seed(7, val)))
        seeds.append((f"{nm} at three nodes", seed([0, 7, 31], val)))
        seeds.append((f"{nm} everywhere", np.full(N_SOLVE, val)))

    for nm, w in seeds:
        r = attempt(solve_gclm, w, a=0.5, nu=0.0, t_max=0.3, max_steps=5000)
        if isinstance(r, Raised):
            cases.append({"entry_point": "solve_gclm", "case": nm, "flagged": True,
                          "silent_corruption": False, **_raise_record(r)})
            continue
        payload_finite = _payload_all_finite(r)
        silent = bool(r.outcome != "diverged" and payload_finite)
        n_silent += int(silent)
        cases.append({
            "entry_point": "solve_gclm", "case": nm, "outcome": r.outcome,
            "n_timesteps": r.n_timesteps,
            "omega_final_stats": _finite_stats(r.omega_final),
            "payload_entirely_finite": payload_finite,
            "flagged": r.outcome == "diverged" or not payload_finite,
            "silent_corruption": silent,
        })

    for nm, val in POISONS:
        def poisoned(xx, v=val):
            w = probe_profile(xx)
            w[7] = v
            return w
        t = attempt(clm_analytic_blowup_time, poisoned, n_scan=256)
        if isinstance(t, Raised):
            cases.append({"entry_point": "clm_analytic_blowup_time", "case": nm,
                          "flagged": True, "silent_corruption": False, **_raise_record(t)})
            continue
        cases.append({
            "entry_point": "clm_analytic_blowup_time",
            "case": f"{nm} at one node (idx 7), n_scan=256",
            "returned": t, "returned_None": t is None,
            "wrong_but_not_finite": t is None,
            "silent_corruption": bool(t is not None and np.isfinite(t)),
        })

    return {
        "mechanism": "NaN/Inf seeded directly into the physical-space vorticity -- leg 92 "
                     "found this path ALREADY CORRECT (0/12) and the repair deliberately "
                     "left it alone; re-run as a REGRESSION channel",
        "leg92_result": {"cases_run": 12, "silent_corruptions": 0},
        "cases_run": len(cases),
        "silent_corruptions": n_silent,
        "cases": cases,
    }


def family_viscosity_guard():
    """G2. `if nu > 0.0` used to drop negative/NaN viscosity into a bitwise-inviscid run."""
    x = grid(N_SOLVE)
    w0 = probe_profile(x)
    kw = dict(a=0.5, t_max=0.3, max_steps=5000)
    r_inviscid = solve_gclm(w0, nu=0.0, **kw)
    r_viscous = solve_gclm(w0, nu=0.01, **kw)
    honest_separation = float(np.max(np.abs(r_inviscid.omega_final - r_viscous.omega_final)))

    cases = []
    n_silent = 0
    for nm, nu in [("nan", float("nan")), ("-1.0", -1.0), ("-0.0", -0.0),
                   ("+inf", float("inf")), ("-inf", float("-inf"))]:
        # leg 92's own corrected criterion: -0.0 == 0.0 so skipping dissipation is CORRECT
        # there, and +inf is not "invalid" under its rule either. Only NaN and strictly
        # negative nu are invalid input.
        nu_is_invalid = bool(nu != nu or nu < 0.0)
        r = attempt(solve_gclm, w0, nu=nu, **kw)
        if isinstance(r, Raised):
            cases.append({"nu": nm, "nu_is_invalid_input": nu_is_invalid,
                          "flagged_by_raise": True, "silent_corruption": False,
                          **_raise_record(r)})
            continue
        payload_finite = _payload_all_finite(r)
        d_inv = float(np.max(np.abs(r.omega_final - r_inviscid.omega_final))) \
            if np.all(np.isfinite(r.omega_final)) else None
        bitwise_inviscid = bool(np.array_equal(r.omega_final, r_inviscid.omega_final))
        silent = bool(nu_is_invalid and r.outcome != "diverged"
                      and payload_finite and bitwise_inviscid)
        n_silent += int(silent)
        cases.append({
            "nu": nm, "nu_is_invalid_input": nu_is_invalid, "flagged_by_raise": False,
            "outcome": r.outcome, "payload_entirely_finite": payload_finite,
            "max_abs_diff_vs_inviscid_run": d_inv,
            "bitwise_identical_to_inviscid_run": bitwise_inviscid,
            "honest_separation_nu0_vs_nu0p01": honest_separation,
            "energy_balance_residual": float(r.energy_balance_residual),
            "conservation_drift": float(r.conservation_drift),
            "guard_nan": bool(getattr(r, "guard_nan", False)),
            "silent_corruption": silent,
        })
    return {
        "mechanism": "G2 -- `if nu > 0.0` silently skipped dissipation for NaN and every "
                     "negative nu; leg 92 measured nu=-1.0 BITWISE identical to the "
                     "inviscid run while the honest nu=0.01 separation is %.6e"
                     % honest_separation,
        "leg92_result": {"cases_run": 5, "silent_corruptions": 1,
                         "honest_separation": LEG92_NU_SEPARATION},
        "honest_separation_nu0_vs_nu0p01": honest_separation,
        "separation_vs_leg92_rel_change":
            abs(honest_separation - LEG92_NU_SEPARATION) / LEG92_NU_SEPARATION,
        "cases_run": len(cases),
        "silent_corruptions": n_silent,
        "cases": cases,
    }


def family_extreme_a():
    """Leg 92 measured 0/10 silent (big honest numbers, unclamped). Regression channel."""
    x = grid(N_SOLVE)
    w0 = probe_profile(x)
    cases = []
    n_silent = 0
    for a in [1e0, 1e4, 1e8, 1e12, 1e16, 1e300, -1e16,
              float("nan"), float("inf"), float("-inf")]:
        r = attempt(solve_gclm, w0, a=a, nu=0.0, t_max=0.3, max_steps=5000)
        if isinstance(r, Raised):
            cases.append({"a": repr(a), "flagged_by_raise": True,
                          "silent_corruption": False, **_raise_record(r)})
            continue
        payload_finite = _payload_all_finite(r)
        maxw = (float(np.max(np.abs(r.omega_final)))
                if np.all(np.isfinite(r.omega_final)) else None)
        silent = bool(not np.isfinite(a) and r.outcome != "diverged" and payload_finite)
        n_silent += int(silent)
        cases.append({
            "a": ("nan" if np.isnan(a) else ("+inf" if a == np.inf else
                  ("-inf" if a == -np.inf else float(a)))),
            "a_is_finite": bool(np.isfinite(a)), "outcome": r.outcome,
            "n_timesteps": r.n_timesteps, "max_abs_omega_final": maxw,
            "payload_entirely_finite": payload_finite,
            "conservation_drift": float(r.conservation_drift),
            "guard_nan": bool(getattr(r, "guard_nan", False)),
            "silent_corruption": silent,
        })
    return {
        "mechanism": "extreme/poisoned `a` -- leg 92 found this ALREADY CORRECT (0/10); a "
                     "big honest number is not corruption. Regression channel",
        "leg92_result": {"cases_run": 10, "silent_corruptions": 0},
        "cases_run": len(cases), "silent_corruptions": n_silent, "cases": cases,
    }


def family_guard_swallows_nan():
    """G3. conservation_drift = max(mean_drift, energy_residual) swallowed the NaN."""
    x = grid(N_SOLVE)
    w0 = probe_profile(x)
    cases = []
    n_silent = 0
    for a in [1e8, 1e12, 1e16]:
        r = attempt(solve_gclm, w0, a=a, nu=0.0, t_max=0.3, max_steps=5000)
        if isinstance(r, Raised):
            cases.append({"a": a, "flagged_by_raise": True, "silent_corruption": False,
                          **_raise_record(r)})
            continue
        e_nan = not np.isfinite(r.energy_balance_residual)
        cons_finite = bool(np.isfinite(r.conservation_drift))
        # SILENT iff a NaN guard input is reported as a finite ("clean") guard value.
        silent = bool(e_nan and cons_finite)
        n_silent += int(silent)
        cases.append({
            "a": a, "outcome": r.outcome,
            "max_abs_omega_final": (float(np.max(np.abs(r.omega_final)))
                                    if np.all(np.isfinite(r.omega_final)) else None),
            "max_over_trajectory": (float(np.nanmax(r.max_omega))
                                    if np.any(np.isfinite(r.max_omega)) else None),
            "mean_drift": float(r.mean_drift),
            "energy_balance_residual": float(r.energy_balance_residual),
            "energy_balance_residual_is_nan": e_nan,
            "conservation_drift_LOGGED": float(r.conservation_drift),
            "conservation_drift_is_finite": cons_finite,
            "guard_nan_flag": bool(getattr(r, "guard_nan", False)),
            "flag_agrees_with_nan_input": bool(getattr(r, "guard_nan", False) == e_nan),
            "silent_corruption": silent,
        })
    return {
        "mechanism": "G3 -- builtin max(finite, nan) == finite, so the ONE number "
                     "LOGGING.md records as the artifact guard read 4.926e-17 ('clean') on "
                     "a run reaching max|w| = 9.673e+144. Now: explicit NaN check, NaN "
                     "reported, and a dedicated SolverResult.guard_nan flag",
        "leg92_result": {"cases_run": 3, "silent_corruptions": 2,
                         "logged_drift_a1e12": 4.926e-17, "max_w_a1e12": 9.673e+144},
        "cases_run": len(cases), "silent_corruptions": n_silent, "cases": cases,
    }


def family_config_poisons():
    """G4. Every NaN comparison is False, so each stop criterion silently ceased to exist."""
    x = grid(N_SOLVE)
    w0 = probe_profile(x)
    ref = solve_gclm(w0, a=0.5, nu=0.0, t_max=0.3, max_steps=5000)
    cases = []
    n_silent = 0
    for nm, kw in [("t_max=nan", dict(t_max=float("nan"))),
                   ("t_max=-1.0", dict(t_max=-1.0)),
                   ("dt_max=nan", dict(t_max=0.3, dt_max=float("nan"))),
                   ("c1=nan", dict(t_max=0.3, c1=float("nan"))),
                   ("c2=nan", dict(t_max=0.3, c2=float("nan"))),
                   ("amplification_factor=nan",
                    dict(t_max=0.3, amplification_factor=float("nan")))]:
        r = attempt(solve_gclm, w0, a=0.5, nu=0.0, max_steps=5000, **kw)
        if isinstance(r, Raised):
            cases.append({"case": nm, "flagged_by_raise": True,
                          "silent_corruption": False, **_raise_record(r)})
            continue
        payload_finite = _payload_all_finite(r)
        silent = bool(r.outcome != "diverged" and payload_finite)
        n_silent += int(silent)
        cases.append({
            "case": nm, "flagged_by_raise": False, "outcome": r.outcome,
            "n_timesteps": r.n_timesteps, "reference_n_timesteps": ref.n_timesteps,
            "payload_entirely_finite": payload_finite,
            "ran_zero_steps_but_reported_a_verdict":
                bool(r.n_timesteps == 0 and r.outcome == "no_blowup"),
            "silent_corruption": silent,
        })

    # The sharp form: does a NaN detector threshold still suppress a real detection?
    big = dict(a=1e4, nu=0.0, t_max=0.3, max_steps=5000)
    r_clean = solve_gclm(w0, **big)
    r_poisoned = attempt(solve_gclm, w0, amplification_factor=float("nan"), **big)
    suppression = {
        "what": "a NaN detector threshold used to turn a DETECTED blow-up into a clean "
                "verdict: leg 92 measured blowup_candidate -> diverged at a = 1e4",
        "clean_outcome": r_clean.outcome,
        "clean_max_abs_omega_final": float(np.max(np.abs(r_clean.omega_final))),
        "clean_n_timesteps": r_clean.n_timesteps,
        "poisoned_raised": isinstance(r_poisoned, Raised),
        "poisoned_outcome": (None if isinstance(r_poisoned, Raised)
                             else r_poisoned.outcome),
        "detection_still_reported_on_the_clean_run":
            bool(r_clean.outcome == "blowup_candidate"),
        "verdict_can_still_be_flipped_silently":
            bool(not isinstance(r_poisoned, Raised)
                 and r_clean.outcome == "blowup_candidate"
                 and r_poisoned.outcome != "blowup_candidate"),
    }
    if isinstance(r_poisoned, Raised):
        suppression.update(_raise_record(r_poisoned))

    # max_steps was the sixth entry point of G4 and is checked too (leg 92 reported it in
    # the mechanism table without a dedicated ladder case).
    ms = attempt(solve_gclm, w0, a=0.5, nu=0.0, t_max=0.3, max_steps=float("nan"))
    max_steps_case = ({"case": "max_steps=nan", "flagged_by_raise": True,
                       **_raise_record(ms)} if isinstance(ms, Raised)
                      else {"case": "max_steps=nan", "flagged_by_raise": False,
                            "outcome": ms.outcome, "n_timesteps": ms.n_timesteps})

    return {
        "mechanism": "G4 -- NaN/non-positive stop criteria were silently DROPPED, never "
                     "flagged: t_max=nan gave 0 timesteps and outcome='no_blowup'",
        "leg92_result": {"cases_run": 6, "silent_corruptions": 5,
                         "verdict_flip_at_a_1e4": "blowup_candidate -> diverged"},
        "blowup_detection_suppression": suppression,
        "extra_max_steps_check_beyond_leg92_ladder": max_steps_case,
        "cases_run": len(cases), "silent_corruptions": n_silent, "cases": cases,
    }


def family_structural():
    """Leg 92: 5/5 raised (FLAGGED). Regression channel -- must still raise."""
    cases = []

    def rec(nm, fn):
        out = attempt(fn)
        if isinstance(out, Raised):
            cases.append({"case": nm, "raised": out.type, "flagged_by_raise": True})
        else:
            cases.append({"case": nm, "raised": None, "returned": str(out)[:120],
                          "flagged_by_raise": False})

    rec("solve_gclm(zeros)", lambda: solve_gclm(np.zeros(N_SOLVE), t_max=0.1).outcome)
    rec("solve_gclm(empty)", lambda: solve_gclm(np.zeros(0), t_max=0.1).outcome)
    rec("analytic: fn returns wrong length",
        lambda: clm_analytic_blowup_time(lambda x: np.sin(x)[:100], n_scan=256))
    rec("analytic: constant 1.0 (H == 0)",
        lambda: clm_analytic_blowup_time(lambda x: np.ones_like(x), n_scan=256))
    rec("analytic: identically zero",
        lambda: clm_analytic_blowup_time(lambda x: np.zeros_like(x), n_scan=256))
    return {"mechanism": "structural/degenerate adversaries; a raise is FLAGGED",
            "leg92_result": {"cases_run": 5, "all_raised": True},
            "cases_run": len(cases),
            "n_flagged_by_raise": sum(1 for c in cases if c["flagged_by_raise"]),
            "cases": cases}


# ===========================================================================
# PART B -- ZERO REGRESSION: BITWISE A/B, PRE-REPAIR vs CURRENT
# ===========================================================================

def load_prerepair_module():
    """Import `6dc4e14^:solver/gclm.py` side-by-side with the current one.

    solver/spectral_utils.py is byte-identical across that range, so the A/B isolates
    gclm.py exactly; that fact is verified here rather than assumed.
    """
    src = subprocess.run(["git", "show", "%s:solver/gclm.py" % PREREPAIR_REV],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    util_diff = subprocess.run(
        ["git", "diff", "--name-only", PREREPAIR_REV, "HEAD", "--", "solver/spectral_utils.py"],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    path = os.path.join(ROOT, ".glb_prerepair_gclm.py")
    with open(path, "w") as fh:
        fh.write(src)
    try:
        spec = importlib.util.spec_from_file_location("glb_prerepair_gclm", path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["glb_prerepair_gclm"] = mod
        spec.loader.exec_module(mod)
    finally:
        os.remove(path)
    meta = {
        "prerepair_rev": PREREPAIR_REV,
        "prerepair_sha256": hashlib.sha256(src.encode()).hexdigest(),
        "prerepair_lines": src.count("\n"),
        "spectral_utils_changed_across_the_ab_range": bool(util_diff),
        "ab_isolates_gclm_py_exactly": not util_diff,
        "prerepair_has_absolute_tolerance": "np.abs(w0) < 1e-12\n" in src,
    }
    return mod, meta


def _hexf(v):
    v = float(v)
    return "nan" if np.isnan(v) else float.hex(v)


def _run_signature(r):
    """Everything a caller can read, at bit precision."""
    return {
        "outcome": r.outcome,
        "early_exit_reason": r.early_exit_reason,
        "n_timesteps": int(r.n_timesteps),
        "t_final": _hexf(r.t_final),
        "dt_min": _hexf(r.dt_min),
        "mean_drift": _hexf(r.mean_drift),
        "energy_balance_residual": _hexf(r.energy_balance_residual),
        "conservation_drift": _hexf(r.conservation_drift),
        "omega_final_sha256": hashlib.sha256(
            np.ascontiguousarray(r.omega_final, dtype=float).tobytes()).hexdigest(),
        "max_omega_sha256": hashlib.sha256(
            np.ascontiguousarray(r.max_omega, dtype=float).tobytes()).hexdigest(),
    }


def part_b_banked_t_stars(pre):
    """All 20 stage1_5_sweep.py production T* values, pre-repair vs current, bitwise."""
    import stage1_5_sweep as s15
    ics = s15.build_initial_conditions()
    x_ref = grid(s15.N_REFERENCE)
    rows = []
    n_moved = 0
    worst_rel = 0.0
    amps = []
    for ic in ics:
        amp = float(np.max(np.abs(ic["fn"](x_ref))))
        amps.append(amp)
        t_new = clm_analytic_blowup_time(ic["fn"])
        t_old = pre.clm_analytic_blowup_time(ic["fn"])
        if t_new is None or t_old is None:
            identical = (t_new is None) and (t_old is None)
            rel = 0.0 if identical else float("inf")
        else:
            identical = float.hex(float(t_new)) == float.hex(float(t_old))
            rel = abs(t_new - t_old) / abs(t_old)
        n_moved += int(not identical)
        worst_rel = max(worst_rel, rel if np.isfinite(rel) else 0.0)
        rows.append({"label": ic["label"], "amplitude_after_energy_normalization": amp,
                     "T_star_prerepair": t_old, "T_star_current": t_new,
                     "hex_prerepair": (None if t_old is None else float.hex(float(t_old))),
                     "hex_current": (None if t_new is None else float.hex(float(t_new))),
                     "bit_identical": identical, "rel_change": rel})
    return {
        "what": "the 20 banked stage1_5_sweep.py initial conditions, energy-normalized to "
                "ENERGY_TARGET = pi/2, T* recomputed on BOTH module versions",
        "n_initial_conditions": len(rows),
        "n_T_star_values_that_moved": n_moved,
        "worst_relative_change": worst_rel,
        "amplitude_range_after_normalization": [min(amps), max(amps)],
        "decades_above_the_old_absolute_1e-12_tolerance":
            float(np.log10(min(amps) / 1e-12)),
        "rows": rows,
    }


def _production_call_surface():
    """The real SOLVER_PARAMS blocks, harvested from the sweep modules themselves."""
    import nongenericity_sweep as ng
    import stage1_5_sweep as s15
    import stage2_5_sweep as s25
    import stage2_6_sweep as s26
    import stage3_6_sweep as s36
    return [("stage1_5_sweep", dict(s15.SOLVER_PARAMS), float(s15.T_MAX)),
            ("stage2_5_sweep", dict(s25.SOLVER_PARAMS), float(s25.T_MAX)),
            ("stage2_6_sweep", dict(s26.SOLVER_PARAMS), float(s26.T_MAX)),
            ("stage3_6_sweep", dict(s36.SOLVER_PARAMS), float(s36.T_MAX)),
            ("nongenericity_sweep", dict(ng.SOLVER_PARAMS), float(ng.T_MAX))]


def part_b_production_runs(pre):
    """Full-length production-shaped runs on every code path, pre-repair vs current."""
    x256 = grid(256)
    w0 = np.sin(x256)
    rows = []
    n_moved = 0
    cases = []
    for name, params, t_max in _production_call_surface():
        cases.append((f"{name} SOLVER_PARAMS, a=0, nu=0 (CLM)",
                      dict(a=0.0, nu=0.0, t_max=t_max, **params)))
        cases.append((f"{name} SOLVER_PARAMS, a=1, nu=0 (De Gregorio)",
                      dict(a=1.0, nu=0.0, t_max=t_max, **params)))
    p15 = dict(_production_call_surface()[0][1])
    t15 = _production_call_surface()[0][2]
    cases += [
        ("viscous nu=0.01 (bisection path)", dict(a=0.0, nu=0.01, t_max=t15, **p15)),
        ("viscous nu=0.3 (top of ga/evolve range)", dict(a=0.0, nu=0.3, t_max=t15, **p15)),
        ("linear diffusion, nonlinear=False", dict(a=0.0, nu=0.05, t_max=1.0,
                                                   nonlinear=False, dt_max=1e-2,
                                                   c1=0.05, c2=0.4, max_steps=200_000,
                                                   amplification_factor=100.0)),
        ("frozen_u transport check", dict(a=0.7, nu=0.0, t_max=1.0, frozen_u=0.5,
                                          dt_max=1e-2, c1=0.05, c2=0.4,
                                          max_steps=200_000, amplification_factor=100.0)),
        ("max_steps_hit path", dict(a=0.5, nu=0.0, t_max=10.0, max_steps=7,
                                    dt_max=1e-2, c1=0.05, c2=0.4,
                                    amplification_factor=100.0)),
        ("blowup_candidate path", dict(a=0.0, nu=0.0, t_max=12.0, dt_max=1e-2,
                                       c1=0.05, c2=0.4, max_steps=200_000,
                                       amplification_factor=50.0)),
        ("nu = -0.0 (admissible; repair promised it stays so)",
         dict(a=0.0, nu=-0.0, t_max=t15, **p15)),
    ]
    for nm, kw in cases:
        r_new = solve_gclm(w0, **kw)
        r_old = pre.solve_gclm(w0, **kw)
        sig_new, sig_old = _run_signature(r_new), _run_signature(r_old)
        identical = sig_new == sig_old
        n_moved += int(not identical)
        row = {"case": nm, "bit_identical": identical, "outcome": r_new.outcome,
               "n_timesteps": int(r_new.n_timesteps),
               "max_over_trajectory": float(np.nanmax(r_new.max_omega))}
        if not identical:
            row["signature_current"] = sig_new
            row["signature_prerepair"] = sig_old
            row["fields_that_moved"] = [k for k in sig_new
                                        if sig_new[k] != sig_old[k]]
        rows.append(row)
    return {
        "what": "full-length production-shaped solve_gclm runs on every code path a caller "
                "uses, compared at BIT level (sha256 of omega_final + hex of every scalar)",
        "n_runs": len(rows), "n_runs_that_moved": n_moved, "rows": rows,
    }


# ===========================================================================
# PART C -- NO OVERSHOOT: the guards must not reject admissible input
# ===========================================================================

def part_c_no_overshoot():
    x = grid(128)
    w0 = np.sin(x) + 0.3 * np.sin(3 * x)
    rows = []
    n_rejected = 0

    def probe(nm, fn):
        nonlocal n_rejected
        out = attempt(fn)
        rejected = isinstance(out, Raised)
        n_rejected += int(rejected)
        rec = {"case": nm, "admissible": True, "rejected": rejected}
        if rejected:
            rec.update(_raise_record(out))
        else:
            rec.update({"outcome": out.outcome if hasattr(out, "outcome") else None,
                        "value": (None if hasattr(out, "outcome") else out)})
        rows.append(rec)

    for name, params, t_max in _production_call_surface():
        for a in (0.0, 0.5, 1.0):
            probe(f"{name} SOLVER_PARAMS, a={a}, nu=0.0",
                  lambda p=params, t=t_max, aa=a: solve_gclm(w0, a=aa, nu=0.0,
                                                             t_max=min(t, 1.0), **p))
    # The admissible-viscosity range every bisecting caller uses: ga/evolve [0, 0.3],
    # ga/fitness2d [0, 1.5], stage2_5 NU_RANGE_LADDER all (0.0, .).
    for nu in (0.0, -0.0, 1e-16, 1e-8, 0.01, 0.3, 1.5):
        probe("admissible nu = %r" % nu,
              lambda v=nu: solve_gclm(w0, a=0.5, nu=v, t_max=0.5))
    # Integer-typed and numpy-scalar parameters, which real callers do pass.
    probe("int t_max / int max_steps",
          lambda: solve_gclm(w0, a=0.5, nu=0, t_max=1, max_steps=5000))
    probe("numpy float64 params",
          lambda: solve_gclm(w0, a=np.float64(0.5), nu=np.float64(0.0),
                             t_max=np.float64(0.5), dt_max=np.float64(1e-2)))
    # The analytic entry point across the full production amplitude band and beyond.
    for amp in (1e-9, 0.8814, 1.0, 1.699, 10.0, 1e9):
        probe("clm_analytic_blowup_time, A sin x, A = %g" % amp,
              lambda A=amp: clm_analytic_blowup_time(lambda xx, s=amp: s * np.sin(xx)))
    probe("clm_analytic_blowup_time, non-blowing data (true answer is None)",
          lambda: clm_analytic_blowup_time(lambda xx: 1.0 + 0.5 * np.sin(xx)))

    # The closed form's OWN amplitude law, which the repair must reproduce exactly:
    # for w0 = A sin x, H(w0) = -A cos x, zero set {0, pi}, so T* = 2/A.
    law = []
    worst_law = 0.0
    for amp in (1e-30, 1e-12, 1e-9, 1.0, 10.0, 1e9, 1e30):
        got = clm_analytic_blowup_time(lambda xx, s=amp: s * np.sin(xx))
        exact = 2.0 / amp
        rel = abs(got - exact) / exact
        worst_law = max(worst_law, rel)
        law.append({"amplitude": amp, "T_star": got, "exact_2_over_A": exact,
                    "rel_error": rel})
    return {
        "what": "does any of the four new guards reject input that was legitimately "
                "admissible? Production parameter blocks harvested from the sweep modules "
                "themselves, not transcribed",
        "n_admissible_cases": len(rows),
        "n_wrongly_rejected": n_rejected,
        "closed_form_amplitude_law_T_star_equals_2_over_A": law,
        "worst_rel_error_against_closed_form": worst_law,
        "cases": rows,
    }


# ===========================================================================

def main():
    np.seterr(all="ignore")
    t0 = time.perf_counter()
    sys.path.insert(0, ROOT)

    pre, ab_meta = load_prerepair_module()

    report = {
        "leg": 103,
        "route": "GLB v1 -- post-repair regression check on solver/gclm.py",
        "module_under_check": "solver/gclm.py",
        "module_edited": False,
        "gate_verbatim": GATE_VERBATIM,
        "closes": "leg 92 (Route-GLA) + bench/fix-gclm-silent-corruption (merge 0740cbf)",
        "definitions_reused_verbatim_from_leg_92": {
            "flagged": "raises, OR outcome=='diverged', OR the numeric payload is itself "
                       "non-finite, OR None is the true answer",
            "silent": "entirely finite, ordinary-looking payload that disagrees with the "
                      "module's documented formula or an exact invariant of it",
            "structural": "a raise counts as FLAGGED, not silent",
            "big_honest_number": "not corruption",
        },
        "ab_provenance": ab_meta,
        # PART A
        "profile_check": family_profile_check(),
        "amplitude_invariant": family_amplitude_invariant(),
        "nan_seeded_vorticity": family_nan_seeded_vorticity(),
        "viscosity_guard": family_viscosity_guard(),
        "extreme_a": family_extreme_a(),
        "guard_swallows_nan": family_guard_swallows_nan(),
        "config_poisons": family_config_poisons(),
        "structural": family_structural(),
    }

    gate_families = ["amplitude_invariant", "nan_seeded_vorticity", "viscosity_guard",
                     "extreme_a", "guard_swallows_nan", "config_poisons"]
    total = sum(report[f]["silent_corruptions"] for f in gate_families)
    cases = sum(report[f]["cases_run"] for f in gate_families)
    report["part_a_total_silent_corruptions"] = total
    report["part_a_total_gate_scoped_cases"] = cases
    report["part_a_per_family"] = {f: report[f]["silent_corruptions"] for f in gate_families}
    report["part_a_leg92_per_family"] = {"amplitude_invariant": 11,
                                         "nan_seeded_vorticity": 0, "viscosity_guard": 1,
                                         "extreme_a": 0, "guard_swallows_nan": 2,
                                         "config_poisons": 5}
    report["part_a_leg92_total"] = 19

    # PART B + C
    report["zero_regression_banked_t_stars"] = part_b_banked_t_stars(pre)
    report["zero_regression_production_runs"] = part_b_production_runs(pre)
    report["no_overshoot"] = part_c_no_overshoot()

    moved = (report["zero_regression_banked_t_stars"]["n_T_star_values_that_moved"]
             + report["zero_regression_production_runs"]["n_runs_that_moved"])
    rejected = report["no_overshoot"]["n_wrongly_rejected"]
    report["part_b_total_artifacts_that_moved"] = moved
    report["part_c_admissible_inputs_wrongly_rejected"] = rejected

    gate_a = total == 0
    gate_b = (moved == 0 and rejected == 0)
    report["gate_answer"] = "yes" if (gate_a and gate_b) else "no"
    report["gate_a_no_longer_exhibits_the_four_mechanisms"] = gate_a
    report["gate_b_zero_regression"] = gate_b
    report["headline"] = (
        "GATE ANSWERS %s. Part A: %d silent corruptions in %d gate-scoped cases "
        "(leg 92: 19/54); worst amplitude-invariant violation %.6e vs leg 92's %.6e, a "
        "%.0fx reduction, at leg 92's own frozen threshold %.3e. Part B: %d of %d banked "
        "T* values and %d of %d production runs moved (bitwise). Part C: %d of %d "
        "admissible inputs wrongly rejected; closed-form law T* = 2/A reproduced to "
        "%.2e worst relative error over 60 decades of amplitude."
    ) % (
        report["gate_answer"].upper(), total, cases,
        report["amplitude_invariant"]["worst_rel_violation"], LEG92_WORST_REL_VIOLATION,
        LEG92_WORST_REL_VIOLATION / max(report["amplitude_invariant"]["worst_rel_violation"],
                                        1e-300),
        LEG92_AMPLITUDE_THRESHOLD,
        report["zero_regression_banked_t_stars"]["n_T_star_values_that_moved"],
        report["zero_regression_banked_t_stars"]["n_initial_conditions"],
        report["zero_regression_production_runs"]["n_runs_that_moved"],
        report["zero_regression_production_runs"]["n_runs"],
        rejected, report["no_overshoot"]["n_admissible_cases"],
        report["no_overshoot"]["worst_rel_error_against_closed_form"],
    )
    report["wall_seconds"] = time.perf_counter() - t0

    with open(OUT, "w") as fh:
        json.dump(report, fh, indent=1, default=str)
    print(report["headline"])
    print("part A per family:", report["part_a_per_family"], "(leg 92:",
          report["part_a_leg92_per_family"], ")")
    print("wrote", OUT, "in %.1fs" % report["wall_seconds"])


if __name__ == "__main__":
    main()
