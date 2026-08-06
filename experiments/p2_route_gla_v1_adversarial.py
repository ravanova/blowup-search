"""Route-GLA v1 -- an ADVERSARIAL BATTERY against solver/gclm.py (physical-space gCLM).

Leg 92. The gCLM physical-space initial-value solver is the last module in this family
without a dedicated adversarial pass. capabilities.py:402-406 registers it as "gCLM,
physical space" validated by test_gclm_dedicated.py (14 checks) -- and every one of those
14 checks feeds a finite, band-limited, well-formed omega0 and a finite in-range `a`.
`grep -ci 'nan|inf|adversarial|malformed'` over that file returns 0. It is a CORRECTNESS
check, not a ROBUSTNESS check -- exactly the relationship leg 89 (Route-BOA) established
for the sibling module solver/boussinesq.py.

THE GATE, VERBATIM
------------------
"Under an adversarial battery of malformed physical-space inputs (NaN-seeded vorticity,
degenerate transform input, extreme a), does solver/gclm.py ever silently return a
finite, plausible-looking result instead of propagating or flagging the invalid input?"

WHAT "SILENTLY" MEANS HERE, DECIDED BEFORE THE RUN
--------------------------------------------------
solver/gclm.py makes exactly one validity claim of its own: the `outcome` field, whose
documented vocabulary is "no_blowup" | "blowup_candidate" | "diverged" | "max_steps_hit",
with "diverged" defined by the module docstring as "NaN/Inf detection". It also raises on
identically-zero data. Those are its two flagging channels. So:

  FLAGGED   -- the call raises, OR returns outcome="diverged", OR returns a result whose
               numeric payload is itself non-finite (the poison came out the other end),
               OR returns None from clm_analytic_blowup_time when None is the TRUE answer.

  SILENT CORRUPTION -- the call returns a numeric payload that is ENTIRELY FINITE and
               sits inside the range a caller would accept as ordinary, AND that payload
               disagrees with the module's own documented formula (or with an exact
               invariant of that formula) by more than the tolerance stated per family.
               A big honest number is NOT corruption; a plausible dishonest one is.
               (This is leg 88's rule, reused verbatim so the two audits are comparable.)

The exact invariant used for the analytic branch is stated before it is measured:
the CLM closed form w(x,t) = 4 w0 / ((2 - t H(w0))^2 + t^2 w0^2) is EXACTLY homogeneous
of degree -1 in the amplitude of w0, so for every scalar eps > 0

        T*(eps * w0) == T*(w0) / eps          (exactly, in exact arithmetic)

Any departure of eps * T*(eps * w0) from T*(w0) is therefore a defect of the
implementation, not of the mathematics. That is the ruler this battery uses.

DISCIPLINE
----------
Magnitudes, never booleans. Every family reports the count AND the size of the thing that
could have gone wrong: the relative violation of the exact scaling invariant decade by
decade, the bitwise separation between a poisoned run and the run it silently became, the
amplification actually reached, and the value the artifact guard reported while it
happened.

This leg edits solver/gclm.py under NO outcome. It only reads it.

Run: PYTHONPATH=. .venv/bin/python experiments/p2_route_gla_v1_adversarial.py
Writes: writeup/data/p2_route_gla_v1_adversarial.json
"""

import json
import os
import time

import numpy as np

from solver.gclm import clm_analytic_blowup_time, solve_gclm
from solver.spectral_utils import grid, hilbert_hat, wavenumbers

OUT = os.path.join(os.path.dirname(__file__), "..", "writeup", "data",
                   "p2_route_gla_v1_adversarial.json")

GATE_VERBATIM = (
    "Under an adversarial battery of malformed physical-space inputs (NaN-seeded "
    "vorticity, degenerate transform input, extreme a), does solver/gclm.py ever "
    "silently return a finite, plausible-looking result instead of propagating or "
    "flagging the invalid input?"
)

N_SOLVE = 64
N_SCAN = 4096
POISONS = [("nan", float("nan")), ("+inf", float("inf")), ("-inf", float("-inf"))]


def probe_profile(x):
    """w0 = sin x + 0.5 sin 2x.  Smooth, mean-zero, two simple zeros at x = 0 and pi.

    Chosen because its zero-set maximum of H(w0) and its GLOBAL maximum of H(w0) are
    DIFFERENT numbers (0.5 vs 0.75).  For sin x alone they coincide, which would hide
    the defect this battery is looking for.  Both values are checked analytically below,
    so the discriminating power of the profile is measured, not assumed.
    """
    return np.sin(x) + 0.5 * np.sin(2 * x)


def _finite_stats(arr):
    a = np.asarray(arr, dtype=float).ravel()
    nf = int(np.sum(~np.isfinite(a)))
    fin = a[np.isfinite(a)]
    return {
        "size": int(a.size),
        "nonfinite": nf,
        "nonfinite_frac": float(nf) / max(a.size, 1),
        "all_finite": nf == 0,
        "max_abs_over_finite_entries": float(np.max(np.abs(fin))) if fin.size else None,
    }


def _result_payload_all_finite(r):
    """Is EVERY numeric field a caller would read entirely finite?"""
    fields = [r.omega_final, r.max_omega, r.times, r.t_final, r.mean_drift,
              r.energy_balance_residual, r.conservation_drift, r.dt_min]
    return all(bool(np.all(np.isfinite(np.asarray(f, dtype=float)))) for f in fields)


# ---------------------------------------------------------------------------
# FAMILY 0 -- the discriminating power of the probe profile, measured
# ---------------------------------------------------------------------------
def family_profile_check():
    x = grid(N_SCAN)
    w0 = probe_profile(x)
    H = np.fft.irfft(hilbert_hat(np.fft.rfft(w0), wavenumbers(N_SCAN)), N_SCAN)
    xz = np.array([0.0, np.pi])                       # exact zeros of sin x (1 + cos x)
    Hz = -np.cos(xz) - 0.5 * np.cos(2 * xz)           # H(sin k x) = -cos k x
    t_true = 2.0 / float(Hz.max())
    t_globalmax = 2.0 / float(H.max())
    return {
        "what": "the profile is chosen so the zero-set max and the global max of H differ",
        "profile": "w0 = sin(x) + 0.5*sin(2x)",
        "n_scan": N_SCAN,
        "H_global_max": float(H.max()),
        "H_max_over_true_zero_set": float(Hz.max()),
        "true_zeros": [0.0, float(np.pi)],
        "T_star_exact_from_zero_set": t_true,
        "T_star_if_global_max_were_used_instead": t_globalmax,
        "ratio_globalmax_over_exact": t_globalmax / t_true,
        "measured_T_star_unit_amplitude": clm_analytic_blowup_time(probe_profile,
                                                                   n_scan=N_SCAN),
    }


# ---------------------------------------------------------------------------
# FAMILY 1 -- DEGENERATE TRANSFORM INPUT: the exact amplitude-scaling invariant
# ---------------------------------------------------------------------------
def family_amplitude_invariant():
    """T*(eps w0) * eps must equal T*(w0) exactly.  Measure the departure per decade.

    CRITERION CALIBRATION, recorded rather than hidden.  This family was first written
    with a fixed tolerance of 1e-9 on the scaling violation, and on the first run it
    flagged 16 of 17 cases -- including eps = 1e-2, which is not a degenerate amplitude
    by any standard.  That criterion was miscalibrated by me, not violated by the module:
    the module locates zeros by 60 steps of bisection on a dense trigonometric
    interpolant, and that root-finder has its own noise floor, measured here rather than
    guessed.  The floor is calibrated on the MODERATE decades (eps in [1e-1, 1e-4], where
    an absolute 1e-12 zero-tolerance provably cannot reach the grid: near a simple zero
    the profile has slope ~1.5*eps, so |w0| < 1e-12 demands |x - x0| < 6.7e-11 while the
    grid spacing is 1.5e-3).  The silent-corruption threshold is then set THREE DECADES
    above that measured floor.

    The positive evidence that what survives is the defect and not the floor: the
    violation grows MONOTONICALLY as eps shrinks and SATURATES at exactly 1/3, which is
    the value predicted independently in family_profile_check from the two H-maxima
    (1 - (2/0.75)/(2/0.5) = 1/3).  Root-finder noise does not saturate at an
    analytically predicted constant.
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
    tol = max(floor * 1e3, 1e-12)

    eps_ladder = [1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10, 1e-11,
                  3e-12, 1e-12, 6e-13, 5e-13, 1e-14, 1e-15, 1e-18]
    cases = []
    worst = 0.0
    worst_case = None
    n_silent = 0
    for eps in calib_eps + eps_ladder:
        t = clm_analytic_blowup_time(lambda x, e=eps: e * probe_profile(x), n_scan=N_SCAN)
        rec = {"eps": eps, "returned_T_star": t}
        if t is None:
            rec.update({"returned_None": True, "silent_corruption": False})
        else:
            scaled = eps * t
            rel = abs(scaled - t_ref) / abs(t_ref)
            # silent iff the number is finite, positive, ordinary-looking, and wrong by
            # more than the MEASURED root-finder floor times 1000
            silent = bool(np.isfinite(t) and t > 0.0 and rel > tol)
            rec.update({
                "eps_times_T_star": float(scaled),
                "reference_T_star": float(t_ref),
                "rel_violation_of_exact_scaling": float(rel),
                "returned_value_is_finite": bool(np.isfinite(t)),
                "returned_value_is_positive": bool(t > 0.0),
                "flagged_by_module": False,
                "silent_corruption": silent,
            })
            if silent:
                n_silent += 1
            if rel > worst:
                worst, worst_case = rel, rec
        cases.append(rec)
    return {
        "what": "exact CLM homogeneity T*(eps w0) == T*(w0)/eps, violated by an ABSOLUTE "
                "zero-tolerance |w0| < 1e-12 at solver/gclm.py:289 that never measures "
                "the scale of its own input",
        "invariant": "eps * T*(eps * w0) == T*(w0)",
        "criterion_calibration": {
            "note": "threshold measured, not guessed; see the family docstring",
            "calibration_decades": calib,
            "measured_root_finder_noise_floor": float(floor),
            "threshold_used": float(tol),
            "headroom_over_floor": 1e3,
        },
        "tolerance_for_silent": float(tol),
        "reference_T_star": float(t_ref),
        "cases_run": len(cases),
        "silent_corruptions": n_silent,
        "worst_rel_violation": float(worst),
        "worst_case": worst_case,
        "saturation_rel_violation": 1.0 / 3.0,
        "cases": cases,
    }


# ---------------------------------------------------------------------------
# FAMILY 2 -- NaN/Inf-SEEDED VORTICITY, through both entry points
# ---------------------------------------------------------------------------
def family_nan_seeded_vorticity():
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
        r = solve_gclm(w, a=0.5, nu=0.0, t_max=0.3, max_steps=5000)
        payload_finite = _result_payload_all_finite(r)
        silent = bool(r.outcome != "diverged" and payload_finite)
        n_silent += int(silent)
        cases.append({
            "entry_point": "solve_gclm",
            "case": nm,
            "outcome": r.outcome,
            "n_timesteps": r.n_timesteps,
            "omega_final_stats": _finite_stats(r.omega_final),
            "payload_entirely_finite": payload_finite,
            "flagged": r.outcome == "diverged" or not payload_finite,
            "silent_corruption": silent,
        })

    # the analytic entry point, on a cheap grid (the poisoned sign-scan is O(n_scan) roots)
    for nm, val in POISONS:
        def poisoned(xx, v=val):
            w = probe_profile(xx)
            w[7] = v
            return w
        t0 = time.perf_counter()
        t = clm_analytic_blowup_time(poisoned, n_scan=256)
        wall = time.perf_counter() - t0
        # returning None ("no blow-up for this data") for data that DOES blow up is a
        # wrong answer, but None is not a FINITE plausible number -- recorded, not counted.
        cases.append({
            "entry_point": "clm_analytic_blowup_time",
            "case": f"{nm} at one node (idx 7), n_scan=256",
            "returned": t,
            "returned_None": t is None,
            "true_answer_is_None": False,
            "wrong_but_not_finite": t is None,
            "wall_seconds": wall,
            "silent_corruption": bool(t is not None and np.isfinite(t)),
        })

    return {
        "what": "NaN/Inf seeded directly into the physical-space vorticity",
        "cases_run": len(cases),
        "silent_corruptions": n_silent,
        "note_on_analytic_branch": (
            "a single NaN node poisons the whole rfft spectrum, so every candidate "
            "H-value is NaN; Python's builtin max(best, nan) KEEPS best, so best_h "
            "stays -inf and the function returns None -- reported as WRONG (the data "
            "does blow up, T* = 4.0) but not counted toward the gate, because None is "
            "not a finite plausible number"
        ),
        "cases": cases,
    }


# ---------------------------------------------------------------------------
# FAMILY 3 -- the `if nu > 0.0` guard: NaN and negative viscosity silently dropped
# ---------------------------------------------------------------------------
def family_viscosity_guard():
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
        r = solve_gclm(w0, nu=nu, **kw)
        payload_finite = _result_payload_all_finite(r)
        d_inv = float(np.max(np.abs(r.omega_final - r_inviscid.omega_final)))
        bitwise_inviscid = bool(np.array_equal(r.omega_final, r_inviscid.omega_final))
        # `nu = -0.0` is NOT an invalid input: it compares equal to 0.0, so skipping the
        # viscous step is the CORRECT behaviour. Counting it would be a false positive;
        # only NaN and strictly-negative nu are invalid. (Correction recorded, not hidden:
        # the first draft of this criterion did count -0.0.)
        nu_is_invalid = bool(nu != nu or nu < 0.0)
        silent = bool(nu_is_invalid and r.outcome != "diverged"
                      and payload_finite and bitwise_inviscid)
        n_silent += int(silent)
        cases.append({
            "nu": nm,
            "nu_is_invalid_input": nu_is_invalid,
            "guard_nu_gt_zero": bool(nu > 0.0),
            "viscous_step": "APPLIED" if nu > 0.0 else "SKIPPED",
            "outcome": r.outcome,
            "payload_entirely_finite": payload_finite,
            "max_abs_diff_vs_inviscid_run": d_inv,
            "bitwise_identical_to_inviscid_run": bitwise_inviscid,
            "honest_separation_nu0_vs_nu0p01": honest_separation,
            "echoed_params_nu": (None if not np.isfinite(nu) else float(nu)),
            "echoed_params_nu_repr": repr(r.params["nu"]),
            "energy_balance_residual": float(r.energy_balance_residual),
            "conservation_drift": float(r.conservation_drift),
            "silent_corruption": silent,
        })
    return {
        "what": "solver/gclm.py:164 gates dissipation behind `if nu > 0.0`; NaN and every "
                "negative value fail that comparison, so the viscous step is skipped and "
                "the run silently becomes the inviscid run",
        "inviscid_reference_outcome": r_inviscid.outcome,
        "honest_separation_nu0_vs_nu0p01": honest_separation,
        "partially_flagged_note": (
            "nu=nan and nu=-inf ALSO produce a bitwise-inviscid trajectory, i.e. the "
            "dissipation is silently dropped there too; they are NOT counted as silent "
            "corruptions because the energy_balance_residual field does carry the poison "
            "out (nan / inf respectively). The trajectory is silently wrong; one guard "
            "field is honest. Recorded at full strength rather than counted."
        ),
        "cases_run": len(cases),
        "silent_corruptions": n_silent,
        "cases": cases,
    }


# ---------------------------------------------------------------------------
# FAMILY 4 -- EXTREME `a`
# ---------------------------------------------------------------------------
def family_extreme_a():
    x = grid(N_SOLVE)
    w0 = probe_profile(x)
    cases = []
    n_silent = 0
    for a in [1e0, 1e4, 1e8, 1e12, 1e16, 1e300, -1e16,
              float("nan"), float("inf"), float("-inf")]:
        r = solve_gclm(w0, a=a, nu=0.0, t_max=0.3, max_steps=5000)
        payload_finite = _result_payload_all_finite(r)
        maxw = float(np.max(np.abs(r.omega_final))) if np.all(np.isfinite(r.omega_final)) else None
        # a big honest number is NOT corruption. Corruption here = a poisoned or wildly
        # out-of-range `a` that yields an entirely finite payload AND an outcome that
        # does not admit anything went wrong.
        silent = bool(not np.isfinite(a) and r.outcome != "diverged" and payload_finite)
        n_silent += int(silent)
        cases.append({
            "a": ("nan" if np.isnan(a) else ("+inf" if a == np.inf else
                  ("-inf" if a == -np.inf else float(a)))),
            "a_is_finite": bool(np.isfinite(a)),
            "outcome": r.outcome,
            "n_timesteps": r.n_timesteps,
            "max_abs_omega_final": maxw,
            "payload_entirely_finite": payload_finite,
            "mean_drift": float(r.mean_drift),
            "energy_balance_residual": float(r.energy_balance_residual),
            "conservation_drift": float(r.conservation_drift),
            "silent_corruption": silent,
        })
    return {
        "what": "`a` swept nine decades past [0,1] and poisoned with NaN/+-Inf",
        "rule": "a big honest number is not corruption; only a non-finite `a` that "
                "produces a fully finite payload with a non-diverged outcome counts",
        "cases_run": len(cases),
        "silent_corruptions": n_silent,
        "cases": cases,
    }


# ---------------------------------------------------------------------------
# FAMILY 5 -- the ARTIFACT GUARD itself: max(finite, nan) returns the finite one
# ---------------------------------------------------------------------------
def family_guard_swallows_nan():
    """conservation_drift = max(mean_drift, energy_balance_residual) -- solver/gclm.py:226.

    Python's builtin max(a, b) returns b only if b > a; NaN loses every comparison, so
    max(finite, nan) == finite. The LOGGED guard value can therefore read clean while one
    of its two inputs is NaN.
    """
    x = grid(N_SOLVE)
    w0 = probe_profile(x)
    cases = []
    n_silent = 0
    for a in [1e8, 1e12, 1e16]:
        r = solve_gclm(w0, a=a, nu=0.0, t_max=0.3, max_steps=5000)
        e_nan = not np.isfinite(r.energy_balance_residual)
        cons_finite = bool(np.isfinite(r.conservation_drift))
        silent = bool(e_nan and cons_finite)
        n_silent += int(silent)
        cases.append({
            "a": a,
            "outcome": r.outcome,
            "max_abs_omega_final": (float(np.max(np.abs(r.omega_final)))
                                    if np.all(np.isfinite(r.omega_final)) else None),
            "mean_drift": float(r.mean_drift),
            "energy_balance_residual": float(r.energy_balance_residual),
            "energy_balance_residual_is_nan": e_nan,
            "conservation_drift_LOGGED": float(r.conservation_drift),
            "conservation_drift_is_finite": cons_finite,
            "silent_corruption": silent,
        })
    return {
        "what": "the logged artifact-guard value can report clean while its own input is NaN",
        "mechanism": "solver/gclm.py:226 conservation_drift=max(mean_drift, energy_residual); "
                     "builtin max returns the finite argument when the other is NaN",
        "cases_run": len(cases),
        "silent_corruptions": n_silent,
        "cases": cases,
    }


# ---------------------------------------------------------------------------
# FAMILY 6 -- STOP-CRITERIA config poisons (reported; adjacent to the gate)
# ---------------------------------------------------------------------------
def family_config_poisons():
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
                   ("amplification_factor=nan", dict(t_max=0.3,
                                                     amplification_factor=float("nan")))]:
        r = solve_gclm(w0, a=0.5, nu=0.0, max_steps=5000, **kw)
        payload_finite = _result_payload_all_finite(r)
        silent = bool(r.outcome != "diverged" and payload_finite)
        n_silent += int(silent)
        cases.append({
            "case": nm,
            "outcome": r.outcome,
            "n_timesteps": r.n_timesteps,
            "reference_n_timesteps": ref.n_timesteps,
            "t_final": float(r.t_final) if np.isfinite(r.t_final) else None,
            "payload_entirely_finite": payload_finite,
            "conservation_drift": float(r.conservation_drift),
            "ran_zero_steps_but_reported_a_verdict": bool(r.n_timesteps == 0
                                                          and r.outcome == "no_blowup"),
            "silent_corruption": silent,
        })
    # The sharp form: does a NaN amplification factor SUPPRESS a real blow-up detection?
    # Use a large `a` that the clean run reports as blowup_candidate, then poison only
    # the detector threshold and see what verdict comes back.
    big = dict(a=1e4, nu=0.0, t_max=0.3, max_steps=5000)
    r_clean = solve_gclm(w0, **big)
    r_poisoned = solve_gclm(w0, amplification_factor=float("nan"), **big)
    suppression = {
        "what": "a NaN detector threshold turns a detected blow-up into a clean verdict",
        "clean_outcome": r_clean.outcome,
        "clean_max_abs_omega_final": float(np.max(np.abs(r_clean.omega_final))),
        "clean_n_timesteps": r_clean.n_timesteps,
        "poisoned_outcome": r_poisoned.outcome,
        "poisoned_n_timesteps": r_poisoned.n_timesteps,
        "poisoned_max_over_trajectory": (
            float(np.nanmax(r_poisoned.max_omega))
            if np.any(np.isfinite(r_poisoned.max_omega)) else None),
        "verdict_flipped": bool(r_clean.outcome == "blowup_candidate"
                                and r_poisoned.outcome != "blowup_candidate"),
    }

    return {
        "what": "NaN in the stop-criteria block; every NaN comparison is False, so the "
                "criterion is silently dropped rather than flagged",
        "blowup_detection_suppression": suppression,
        "cases_run": len(cases),
        "silent_corruptions": n_silent,
        "cases": cases,
    }


# ---------------------------------------------------------------------------
# FAMILY 7 -- structural adversaries: a raise counts as FLAGGED
# ---------------------------------------------------------------------------
def family_structural():
    cases = []
    def rec(nm, fn):
        try:
            out = fn()
            cases.append({"case": nm, "raised": None, "returned": str(out)[:120],
                          "flagged_by_raise": False})
        except Exception as ex:
            cases.append({"case": nm, "raised": type(ex).__name__,
                          "returned": None, "flagged_by_raise": True})

    rec("solve_gclm(zeros)", lambda: solve_gclm(np.zeros(N_SOLVE), t_max=0.1).outcome)
    rec("solve_gclm(empty)", lambda: solve_gclm(np.zeros(0), t_max=0.1).outcome)
    rec("analytic: fn returns wrong length",
        lambda: clm_analytic_blowup_time(lambda x: np.sin(x)[:100], n_scan=256))
    rec("analytic: constant 1.0 (H == 0, degenerate transform input)",
        lambda: clm_analytic_blowup_time(lambda x: np.ones_like(x), n_scan=256))
    rec("analytic: identically zero",
        lambda: clm_analytic_blowup_time(lambda x: np.zeros_like(x), n_scan=256))
    return {"what": "structural/degenerate adversaries; a raise is FLAGGED, not silent",
            "cases_run": len(cases), "cases": cases}


# ---------------------------------------------------------------------------
# FAMILY 8 -- cost blow-up of the poisoned sign-change scan (out of gate, reported)
# ---------------------------------------------------------------------------
def family_cost_blowup():
    ladder = []
    for n in [64, 128, 256, 512]:
        t0 = time.perf_counter()
        clm_analytic_blowup_time(lambda x: np.full_like(x, np.nan), n_scan=n)
        t_nan = time.perf_counter() - t0
        t0 = time.perf_counter()
        clm_analytic_blowup_time(probe_profile, n_scan=n)
        t_clean = time.perf_counter() - t0
        ladder.append({"n_scan": n, "wall_nan": t_nan, "wall_clean": t_clean,
                       "ratio": t_nan / max(t_clean, 1e-9)})
    return {
        "what": "np.sign(nan) makes np.diff(sign) != 0 true at EVERY node, so the root "
                "list degenerates from O(1) to O(n_scan), each root costing 60 bisections "
                "of a dense trigonometric evaluation",
        "out_of_gate": True,
        "ladder": ladder,
    }


def main():
    np.seterr(all="ignore")
    t0 = time.perf_counter()
    report = {
        "leg": 92,
        "route": "GLA v1 -- adversarial audit of solver/gclm.py (physical-space gCLM)",
        "module_under_audit": "solver/gclm.py",
        "module_edited": False,
        "gate_verbatim": GATE_VERBATIM,
        "silent_corruption_definition": {
            "flagged": "raises, OR outcome=='diverged', OR the numeric payload is itself "
                       "non-finite, OR None is the true answer",
            "silent": "entirely finite, ordinary-looking payload that disagrees with the "
                      "module's documented formula or an exact invariant of it",
            "structural": "a raise counts as FLAGGED, not silent",
            "big_honest_number": "not corruption",
        },
        "profile_check": family_profile_check(),
        "amplitude_invariant": family_amplitude_invariant(),
        "nan_seeded_vorticity": family_nan_seeded_vorticity(),
        "viscosity_guard": family_viscosity_guard(),
        "extreme_a": family_extreme_a(),
        "guard_swallows_nan": family_guard_swallows_nan(),
        "config_poisons": family_config_poisons(),
        "structural": family_structural(),
        "out_of_gate_cost_blowup": family_cost_blowup(),
    }

    gate_families = ["amplitude_invariant", "nan_seeded_vorticity", "viscosity_guard",
                     "extreme_a", "guard_swallows_nan", "config_poisons"]
    total = sum(report[f]["silent_corruptions"] for f in gate_families)
    cases = sum(report[f]["cases_run"] for f in gate_families)
    report["gate_answer"] = "yes" if total > 0 else "no"
    report["total_silent_corruptions"] = total
    report["total_gate_scoped_cases"] = cases
    report["per_family_silent_corruptions"] = {
        f: report[f]["silent_corruptions"] for f in gate_families
    }
    report["headline"] = (
        "GATE ANSWERS YES. %d silent corruptions in %d gate-scoped cases, across %d "
        "independent mechanisms. Worst: clm_analytic_blowup_time returns a finite, "
        "positive, plausible blow-up time that violates the EXACT amplitude-scaling "
        "invariant of the CLM closed form by %.4f relative (saturating at 1/3) for "
        "initial vorticity of amplitude <= 1e-12, because the zero-detector at "
        "solver/gclm.py:289 uses an ABSOLUTE tolerance |w0| < 1e-12."
    ) % (total, cases,
         sum(1 for f in gate_families if report[f]["silent_corruptions"] > 0),
         report["amplitude_invariant"]["worst_rel_violation"])
    report["wall_seconds"] = time.perf_counter() - t0

    with open(os.path.abspath(OUT), "w") as fh:
        json.dump(report, fh, indent=1, default=str)
    print(report["headline"])
    print("per family:", report["per_family_silent_corruptions"])
    print("wrote", os.path.abspath(OUT), "in %.1fs" % report["wall_seconds"])


if __name__ == "__main__":
    main()
