"""Leg 185, Route-M2SD: DIAGNOSING leg 125's stalled Object-B Newton continuation.

WHAT THIS IS.  Leg 125 (Route-M2P) landed gate NO on both clauses.  Its second clause is the
one this leg re-opens: "Object B" -- the VISCOUS steady state that would have to exist for a
genuine gamma = 2 dissipative certificate -- was attempted under Newton continuation in `M7`
and did not converge at `nu = 1.0`.  `DIRECTION.md` sec 185 asks whether that stall is GENUINE
NON-EXISTENCE or a SOLVER ARTIFACT, and pre-commits the three standard diagnostics: residual
trend classification, Jacobian conditioning near the stall, sensitivity to the initial guess.

SCOPE, PRE-COMMITTED AND BINDING.  Diagnostic only.  This module BUILDS NOTHING: it imports
`solver.dissipative_profile` (leg 125's, closed territory) READ-ONLY and re-runs leg 125's own
setup with instrumentation.  `no_dynamics_run: true` -- every solve here is of a STEADY
equation, exactly as in leg 125.  No new solver module, no dissipative-dynamics run, no GA
compute, and NO corrected continuation is BUILT here (the gate's artifact branch forbids it;
what this leg may do is MEASURE whether one would be reachable, and it does, once, in D5).
Everything is FLOATING POINT.  No number here is a certificate.

THE SIX DIAGNOSTICS, AND WHAT EACH CAN REPORT.

  D1  RESIDUAL TREND CLASSIFICATION.  Leg 125's `newton_gamma2` is re-run with a full
      per-iteration trace at the stalled `nu = 1.0` and at the converged `nu = 0.3` control.
      The two signatures being distinguished, written down before the traces were read:
        * genuine-non-existence signature -- the ABSOLUTE residual plateaus at a positive
          floor while the solution amplitude stays bounded away from zero;
        * artifact signature -- the absolute residual falls to the Newton floor while the
          amplitude falls WITH it, i.e. Newton converged, to the trivial null.
      `M7` reported only the RELATIVE residual, which is a ratio of two quantities that can
      both go to zero, so it cannot tell these apart on its own (lesson 67: gate the quantity
      the measurement divides by).

  D2  JACOBIAN CONDITIONING / SINGULARITY STRUCTURE.  Singular values of the augmented
      Jacobian `[dR/dOmega | dR/da]` and of `dR/dOmega` alone, along the whole stalled path.
      A fold or a genuine obstruction shows as `sigma_min -> 0` at bounded amplitude.  The
      norm of the `a`-column is tracked separately, because `dR/da = -(V H Omega)(D Omega)` is
      QUADRATIC in `Omega` and therefore vanishes identically at the trivial null -- which
      would make `a` unidentifiable there for a reason that has nothing to do with existence.

  D3  PARAMETRIZATION DEGENERACY, as an EXACT identity.  The profile equation obeys
          F(Omega(./mu), mu^2 nu)(X) = F(Omega, nu)(X/mu)
      (leg 125 wrote this covariance down in `m7_gamma2_branch`'s docstring and used it only
      as a check).  Differentiating at `mu = 1` at a solution gives the exact null relation
          dF/dOmega [ -X Omega_X ]  +  2 nu dF/dnu  =  0 ,
      i.e. `(-X Omega_X, 2 nu)` is a null vector of the `(Omega, nu)` Jacobian ALONG EVERY
      SOLUTION.  So `nu` is NOT an independent parameter of this profile equation: continuing
      in `nu` with the dilation freedom unfixed is continuing along a gauge orbit.  Measured
      here as a discrete residual and REFINED, because the only honest way to claim an
      identity is exact is to show its discrete violation converges to zero.

  D4  INITIAL-GUESS SENSITIVITY AT THE SAME TARGET.  This is the gate's own artifact
      criterion, verbatim: "recoverable convergence from a different initial guess at the SAME
      target".  `nu = 1.0` is attacked from eight starts, including the exact dilations of leg
      125's own lower-`nu` solutions -- which D3 says must BE solutions at `nu = 1.0`.

  D5  IS A GENUINE PROFILE REACHABLE?  The gate's artifact branch requires reporting "whether
      a genuine profile becomes reachable".  D3 says how to parametrize: fix the model
      parameter `a`, impose the dilation gauge, and make `nu` the UNKNOWN.  That system is
      square.  It is solved here ONCE per `a`, from two different `nu` starts, and grid- and
      truncation-refined.  The SIGN of the recovered `nu` is the admissibility question:
      `nu > 0` is diffusion, `nu < 0` is anti-diffusion and is not a viscous profile at all.

  D6  TWO-SIDED CALIBRATION (lesson 90).  A classifier that cannot return "genuine
      non-existence" is not a classifier.  The same Newton is run on a DELIBERATELY
      INCONSISTENT over-determination -- two contradictory normalizations, `Omega_X(0) = g`
      and `Omega_X(0) = m g` with `m != 1` -- which provably has no solution.  If the
      non-existence arm is real, that run must show the plateau signature D1 names, with a
      floor that scales with the imposed inconsistency `m - 1`.

PROVENANCE NOTE, RECORDED BECAUSE IT MATTERS FOR AUDIT.  `DIRECTION.md` sec 185 describes the
stall as "residual 2.65-3.75 with `c_l` running to -10.7".  Those figures are not reproducible
from leg 125's landed artifact and are corrected here from the re-run: the runaway parameter
is `a` (the free unknown of `newton_gamma2`), not `c_l` (which is HELD at 1/2 there), it runs
to -10.09246141, and the plateauing quantity is the RELATIVE residual at 4.41-5.49, not 2.65-
3.75.  The correction does not change what the gate asks; it is logged so the diagnosis is
read against the numbers that are actually on disk.
"""

import json
import os
import time

import numpy as np

from solver.dissipative_profile import DissipativeProfile, chen_profile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "writeup", "data", "p2_route_m2sd_v1_diagnostic.json")

N_MAIN = 401                 # leg 125's own M7 grid (N_SWEEP), so D1/D2/D4 re-run its setup
A_MODULE = 0.39              # leg 125's M7 `DissipativeProfile(a=0.39, ...)`
A0_M7 = 0.386                # leg 125's M7 initial `a`
C_L_IMPOSED = 0.5            # Delta = 0, i.e. the gamma = 2 steadiness condition
C_OMEGA = -1.0               # the amplitude gauge, as in leg 125


# ---------------------------------------------------------------------------
# leg 125's newton_gamma2, re-run with instrumentation (same math, same steps)
# ---------------------------------------------------------------------------

def _aug(dp, Om, a, nu):
    J = np.zeros((dp.n, dp.n + 1))
    J[:, :dp.n] = dp.jacobian_Omega(Om, C_L_IMPOSED, C_OMEGA, nu, a=a)
    J[:, dp.n] = dp.dR_da(Om)
    return J


def _relres(dp, Om, nu, a):
    R = dp.residual(Om, C_L_IMPOSED, C_OMEGA, nu, a=a)
    scale = float(np.sqrt(np.mean(((C_OMEGA + dp.H @ Om) * Om) ** 2)))
    return float(np.sqrt(np.mean(R ** 2)) / max(scale, 1e-300)), scale


def traced_newton_gamma2(dp, Om0, a0, nu, iters=60, tol=1e-13, svd=False):
    """Leg 125's `newton_gamma2`, step for step, with a per-iteration trace.

    The step is identical (`lstsq` on `[dR/dOmega | dR/da]`); the only addition is that the
    absolute residual, the amplitude, `a`, and -- optionally -- the singular values are
    recorded at every iterate instead of only the residual norm."""
    Om = np.array(Om0, dtype=float)
    a = float(a0)
    trace = []
    k = 0
    for k in range(iters):
        R = dp.residual(Om, C_L_IMPOSED, C_OMEGA, nu, a=a)
        absrms = float(np.sqrt(np.mean(R ** 2)))
        rr, scale = _relres(dp, Om, nu, a)
        row = {"iter": k, "residual_rms_absolute": absrms, "residual_relative": rr,
               "solution_scale": scale, "a": float(a),
               "amplitude": float(np.abs(Om).max())}
        if svd:
            J = _aug(dp, Om, a, nu)
            sv = np.linalg.svd(J, compute_uv=False)
            svO = np.linalg.svd(J[:, :dp.n], compute_uv=False)
            row.update({
                "norm_dR_da_column": float(np.linalg.norm(J[:, dp.n])),
                "sigma_min_augmented": float(sv[-1]),
                "sigma_max_augmented": float(sv[0]),
                "sigma_min_dR_dOmega": float(svO[-1]),
                "cond_dR_dOmega": float(svO[0] / svO[-1]),
            })
        trace.append(row)
        if absrms < tol:
            break
        J = _aug(dp, Om, a, nu)
        step, *_ = np.linalg.lstsq(J, -R, rcond=None)
        Om = Om + step[:dp.n]
        a = a + float(step[dp.n])
    rr, scale = _relres(dp, Om, nu, a)
    return {"Omega": Om, "a": float(a), "nu": float(nu), "iters": k,
            "residual_rms_absolute": float(np.sqrt(np.mean(
                dp.residual(Om, C_L_IMPOSED, C_OMEGA, nu, a=a) ** 2))),
            "residual_relative": rr, "solution_scale": scale,
            "amplitude": float(np.abs(Om).max()), "trace": trace}


def _classify(out):
    """The pre-committed two-signature classifier, applied to one Newton run.

    Both arms can fire; D6 exhibits a run on which the non-existence arm DOES fire."""
    tail = out["trace"][-4:]
    abs_floor = min(r["residual_rms_absolute"] for r in tail)
    amp_final = out["amplitude"]
    plateau = (max(r["residual_rms_absolute"] for r in tail)
               / max(min(r["residual_rms_absolute"] for r in tail), 1e-300))
    if abs_floor < 1e-12 and amp_final > 1e-3:
        verdict = "CONVERGED to a non-trivial solution"
    elif abs_floor < 1e-12 and amp_final < 1e-8:
        verdict = ("CONVERGED to the TRIVIAL NULL Omega = 0 (artifact signature: the absolute "
                   "residual reaches the Newton floor because the solution vanished)")
    elif plateau < 1.1:
        verdict = ("RESIDUAL PLATEAU at a positive floor with bounded amplitude "
                   "(genuine-non-existence signature)")
    else:
        verdict = "NEITHER SIGNATURE CLEAN (no convergence, no plateau)"
    return {"absolute_residual_floor": abs_floor, "final_amplitude": amp_final,
            "tail_plateau_ratio": float(plateau), "classification": verdict}


# ---------------------------------------------------------------------------
# D1 / D2
# ---------------------------------------------------------------------------

def d1_d2_residual_trend_and_jacobian():
    dp = DissipativeProfile(a=A_MODULE, n=N_MAIN)
    Om0, _, _ = chen_profile(dp.X)
    stalled = traced_newton_gamma2(dp, Om0, A0_M7, 1.0, svd=True)
    control = traced_newton_gamma2(dp, Om0, A0_M7, 0.3, svd=True)
    d1 = {
        "stalled_target_nu": 1.0,
        "control_target_nu": 0.3,
        "stalled": {"a_final": stalled["a"], "iters": stalled["iters"],
                    "residual_rms_absolute_final": stalled["residual_rms_absolute"],
                    "residual_relative_final": stalled["residual_relative"],
                    "amplitude_final": stalled["amplitude"],
                    "amplitude_initial": stalled["trace"][0]["amplitude"],
                    "relative_residual_last4": [r["residual_relative"] for r in stalled["trace"][-4:]],
                    "absolute_residual_last4": [r["residual_rms_absolute"] for r in stalled["trace"][-4:]],
                    "amplitude_last4": [r["amplitude"] for r in stalled["trace"][-4:]],
                    "trace": [{k: v for k, v in r.items() if k != "solution_scale"}
                              for r in stalled["trace"]],
                    "classification": _classify(stalled)},
        "control": {"a_final": control["a"], "iters": control["iters"],
                    "residual_rms_absolute_final": control["residual_rms_absolute"],
                    "residual_relative_final": control["residual_relative"],
                    "amplitude_final": control["amplitude"],
                    "classification": _classify(control)},
        "leg125_reported_relative_residual_at_nu_1": 5.485652392436699,
        "reproduced_relative_residual_at_nu_1": stalled["residual_relative"],
        "note": ("leg 125's M7 row for nu = 1.0 is reproduced to the digit.  What its single "
                 "reported number could not show is that the ABSOLUTE residual falls to the "
                 "Newton floor over the same iterations -- the relative residual is a 0/0 "
                 "ratio here, not a plateau."),
    }
    d2 = {
        "along_stalled_path": [
            {"iter": r["iter"], "amplitude": r["amplitude"], "a": r["a"],
             "norm_dR_da_column": r["norm_dR_da_column"],
             "sigma_min_augmented": r["sigma_min_augmented"],
             "sigma_min_dR_dOmega": r["sigma_min_dR_dOmega"],
             "cond_dR_dOmega": r["cond_dR_dOmega"]}
            for r in stalled["trace"]],
        "at_trivial_null": {
            "sigma_min_dR_dOmega": stalled["trace"][-1]["sigma_min_dR_dOmega"],
            "cond_dR_dOmega": stalled["trace"][-1]["cond_dR_dOmega"],
            "norm_dR_da_column": stalled["trace"][-1]["norm_dR_da_column"],
        },
        "reading": ("dR/dOmega is NOT singular at the point Newton reached: sigma_min stays "
                    "O(1) and the condition number is O(1e3-1e4) at the end of the path.  The "
                    "trivial null is a NON-DEGENERATE root of the residual, which is exactly "
                    "why Newton converges to it quadratically.  What DOES collapse is the "
                    "a-column, because dR/da is quadratic in Omega: it falls by ~30 orders "
                    "along the path, so `a` stops being identifiable and freezes.  No fold, "
                    "no singular Jacobian, no obstruction."),
    }
    return d1, d2


# ---------------------------------------------------------------------------
# D3 -- the exact dilation-covariance null relation, refined
# ---------------------------------------------------------------------------

def d3_parametrization_degeneracy(grids=(401, 801, 1201), nu=0.3):
    rows = []
    for n in grids:
        dp = DissipativeProfile(a=A_MODULE, n=n)
        Om0, _, _ = chen_profile(dp.X)
        out = traced_newton_gamma2(dp, Om0, A0_M7, nu)
        Om, a = out["Omega"], out["a"]
        v = -dp.X * (dp.D @ Om)                      # the dilation generator
        t1 = dp.jacobian_Omega(Om, C_L_IMPOSED, C_OMEGA, nu, a=a) @ v
        t2 = 2.0 * nu * dp.dR_dnu(Om)
        n1, n2 = float(np.linalg.norm(t1)), float(np.linalg.norm(t2))
        viol = float(np.linalg.norm(t1 + t2))
        rows.append({"n": n, "a_converged": a, "nu": nu,
                     "identity_violation": viol,
                     "norm_dF_dOmega_term": n1, "norm_2nu_dF_dnu_term": n2,
                     "identity_violation_relative": viol / max(n1, n2),
                     "solution_residual_relative": out["residual_relative"]})
    return {
        "identity": "dF/dOmega [ -X Omega_X ] + 2 nu dF/dnu = 0 at every solution",
        "rows": rows,
        "violation_relative_ladder": [r["identity_violation_relative"] for r in rows],
        "a_converged_ladder": [r["a_converged"] for r in rows],
        "reading": ("the discrete violation of the identity FALLS under refinement, so the "
                    "identity is exact in the continuum and what is measured is "
                    "discretisation error of the sinh-grid operators.  Consequence: (-X "
                    "Omega_X, 2 nu) is a null direction of the (Omega, nu) Jacobian along "
                    "EVERY solution, so nu is a gauge coordinate of this profile equation, "
                    "not an independent continuation parameter.  Corroborating tell in the "
                    "same table: the `a` leg 125's M7 converges to is itself grid-dependent, "
                    "which a determinate solution's parameter would not be."),
    }


# ---------------------------------------------------------------------------
# D4 -- initial-guess sensitivity at the SAME target
# ---------------------------------------------------------------------------

def d4_initial_guess_sensitivity(target_nu=1.0):
    dp = DissipativeProfile(a=A_MODULE, n=N_MAIN)
    Om0, _, _ = chen_profile(dp.X)
    sources = {}
    for nu in (1e-3, 1e-2, 1e-1, 3e-1):
        o = traced_newton_gamma2(dp, Om0, A0_M7, nu)
        sources[nu] = o
    guesses = [("leg 125's own fixed guess: Chen profile, a0 = 0.386", Om0, A0_M7)]
    for nu, o in sources.items():
        mu = float(np.sqrt(target_nu / nu))
        guesses.append((f"exact dilation of leg 125's own nu = {nu:g} solution, mu = {mu:.4f}",
                        np.interp(dp.X / mu, dp.X, o["Omega"]), o["a"]))
    guesses += [
        ("Chen profile, amplitude x 2", 2.0 * Om0, A0_M7),
        ("Chen profile, amplitude x 0.5", 0.5 * Om0, A0_M7),
        ("Chen profile, a0 = 0.0", Om0, 0.0),
    ]
    rows = []
    for label, g, a0 in guesses:
        out = traced_newton_gamma2(dp, g, a0, target_nu)
        rows.append({"guess": label, "a_final": out["a"], "iters": out["iters"],
                     "residual_relative": out["residual_relative"],
                     "residual_rms_absolute": out["residual_rms_absolute"],
                     "amplitude": out["amplitude"],
                     "nontrivial": bool(out["residual_relative"] < 1e-8
                                        and out["solution_scale"] > 1e-3),
                     "classification": _classify(out)["classification"]})
    ok = [r for r in rows if r["nontrivial"]]
    return {
        "target_nu": target_nu,
        "source_solutions_for_dilation": {str(nu): {"a": o["a"],
                                                    "residual_relative": o["residual_relative"],
                                                    "amplitude": o["amplitude"]}
                                          for nu, o in sources.items()},
        "rows": rows,
        "n_guesses": len(rows),
        "n_recovered_nontrivial": len(ok),
        "recovered_a_values": [r["a_final"] for r in ok],
        "recovered_a_spread": (max(r["a_final"] for r in ok) - min(r["a_final"] for r in ok))
                              if ok else None,
        "worst_recovered_relative_residual": max((r["residual_relative"] for r in ok),
                                                 default=None),
        "reading": ("the SAME target that leg 125 could not solve is solved to relative "
                    "residual ~1e-14 from several different starts.  That is the gate's own "
                    "solver-artifact criterion, met verbatim.  The recovered solutions do NOT "
                    "agree with each other on `a`, which is the second finding: at a single "
                    "nu the solution set is at least one-parameter, so recovering convergence "
                    "does not by itself deliver a determinate profile."),
    }


# ---------------------------------------------------------------------------
# D5 -- the parametrization D3 implies: `a` fixed, `nu` UNKNOWN, dilation gauge imposed
# ---------------------------------------------------------------------------

def _solve_nu_unknown(n, a_fix, nu0, rho_max=8.0, iters=60, tol=1e-13):
    """Square system: unknowns (Omega, nu); equations (residual, dilation normalization).

    MEASUREMENT ONLY.  This is not a continuation and not a certificate; it exists to answer
    the gate's artifact-branch question 'whether a genuine profile becomes reachable', and it
    is deliberately a single square solve rather than the corrected continuation the gate
    forbids this leg from building."""
    dp = DissipativeProfile(a=a_fix, n=n, rho_max=rho_max)
    Om0, _, _ = chen_profile(dp.X)
    g = dp.D[dp.i0]
    gauge = float(g @ Om0)
    Om = np.array(Om0, dtype=float)
    nu = float(nu0)
    hist = []
    k = 0
    for k in range(iters):
        R = dp.residual(Om, C_L_IMPOSED, C_OMEGA, nu, a=a_fix)
        hist.append(float(np.sqrt(np.mean(R ** 2))))
        if hist[-1] < tol:
            break
        F = np.concatenate([R, [float(g @ Om) - gauge]])
        J = np.zeros((dp.n + 1, dp.n + 1))
        J[:dp.n, :dp.n] = dp.jacobian_Omega(Om, C_L_IMPOSED, C_OMEGA, nu, a=a_fix)
        J[:dp.n, dp.n] = dp.dR_dnu(Om)
        J[dp.n, :dp.n] = g
        step, *_ = np.linalg.lstsq(J, -F, rcond=None)
        Om = Om + step[:dp.n]
        nu = nu + float(step[dp.n])
    scale = float(np.sqrt(np.mean(((C_OMEGA + dp.H @ Om) * Om) ** 2)))
    amp = float(np.abs(Om).max())
    return {"n": n, "a": a_fix, "nu0": nu0, "rho_max": rho_max, "nu": float(nu),
            "residual_relative": hist[-1] / max(scale, 1e-300),
            "residual_rms_absolute": hist[-1], "amplitude": amp,
            "edge_over_amplitude": float(abs(Om[-1]) / max(amp, 1e-300)),
            "X_max": float(dp.X[-1]),
            "odd_symmetry_defect": float(np.abs(Om + Om[::-1]).max() / max(amp, 1e-300)),
            "iters": k, "dilation_gauge_Omega_X_0": gauge,
            "admissible_positive_nu": bool(nu > 0.0)}


def d5_is_a_genuine_profile_reachable():
    sweep = []
    for a_fix in (0.30, 0.3865, 0.45, 0.50, 0.55, 0.70):
        pair = [_solve_nu_unknown(N_MAIN, a_fix, nu0) for nu0 in (0.3, 0.01)]
        sweep.append({"a": a_fix,
                      "nu_from_nu0_0p3": pair[0]["nu"], "nu_from_nu0_0p01": pair[1]["nu"],
                      "sign_agrees_across_starts": bool((pair[0]["nu"] > 0) == (pair[1]["nu"] > 0)),
                      "relative_spread": abs(pair[0]["nu"] - pair[1]["nu"])
                                         / max(abs(pair[0]["nu"]), abs(pair[1]["nu"]), 1e-300),
                      "worst_relative_residual": max(p["residual_relative"] for p in pair),
                      "amplitudes": [p["amplitude"] for p in pair],
                      "admissible_positive_nu": bool(pair[0]["nu"] > 0 and pair[1]["nu"] > 0),
                      "runs": pair})
    grid = [_solve_nu_unknown(n, 0.30, 0.3) for n in (201, 401, 801, 1201)]
    trunc = [_solve_nu_unknown(801, 0.30, 0.3, rho_max=rm) for rm in (6.0, 8.0, 10.0)]
    pos = [r["a"] for r in sweep if r["admissible_positive_nu"]]
    neg = [r["a"] for r in sweep if not r["admissible_positive_nu"]]
    return {
        "system": ("unknowns (Omega, nu); equations (steady residual, dilation normalization "
                   "Omega_X(0) = Chen's value).  c_l = 1/2 and c_omega = -1 IMPOSED, i.e. "
                   "Delta = 0, the gamma = 2 steadiness condition.  `a` is a FIXED model "
                   "parameter here, which is what it is in the equation."),
        "a_sweep": sweep,
        "a_with_admissible_positive_nu": pos,
        "a_with_inadmissible_negative_nu": neg,
        "grid_convergence_at_a_0p30": grid,
        "nu_ladder_at_a_0p30": [r["nu"] for r in grid],
        "truncation_sensitivity_at_a_0p30": trunc,
        "nu_at_chen_a_one_half": [r for r in sweep if r["a"] == 0.50][0],
        "leg125_a_star_from_Delta_sweep": 0.3864963972206034,
        "reading": ("the square system converges quadratically at every tested `a`, so the "
                    "stall was a parametrization problem, not an existence one.  The SIGN of "
                    "the recovered nu is the real content and it is stable across both "
                    "starts: nu > 0 (a genuine diffusive profile) below leg 125's own "
                    "a* = 0.3865, and nu < 0 (anti-diffusive, NOT a viscous profile) at and "
                    "above it -- including Chen's a = 1/2.  The zero crossing lands on the "
                    "same a* leg 125 measured independently from the Delta(a) sweep, which "
                    "is a cross-check between two different computations, not a restatement. "
                    "The MAGNITUDE of nu is start-dependent wherever nu < 0, so the square "
                    "system still has more than one root there; only the sign is banked."),
    }


# ---------------------------------------------------------------------------
# D6 -- two-sided calibration: the classifier must be able to say NON-EXISTENCE
# ---------------------------------------------------------------------------

def d6_calibration(nu=0.3, multipliers=(1.0, 1.5, 3.0), iters=80):
    dp = DissipativeProfile(a=A_MODULE, n=N_MAIN)
    Om0, _, _ = chen_profile(dp.X)
    g = dp.D[dp.i0]
    g0 = float(g @ Om0)
    rows = []
    for m in multipliers:
        Om = np.array(Om0, dtype=float)
        a = A0_M7
        hist = []
        amps = []
        k = 0
        for k in range(iters):
            R = dp.residual(Om, C_L_IMPOSED, C_OMEGA, nu, a=a)
            F = np.concatenate([R, [float(g @ Om) - g0], [float(g @ Om) - m * g0]])
            hist.append(float(np.sqrt(np.mean(F ** 2))))
            amps.append(float(np.abs(Om).max()))
            if hist[-1] < 1e-13:
                break
            J = np.zeros((dp.n + 2, dp.n + 1))
            J[:dp.n, :dp.n] = dp.jacobian_Omega(Om, C_L_IMPOSED, C_OMEGA, nu, a=a)
            J[:dp.n, dp.n] = dp.dR_da(Om)
            J[dp.n, :dp.n] = g
            J[dp.n + 1, :dp.n] = g
            step, *_ = np.linalg.lstsq(J, -F, rcond=None)
            Om = Om + step[:dp.n]
            a = a + float(step[dp.n])
        tail = hist[-5:]
        plateau = max(tail) / max(min(tail), 1e-300)
        consistent = (m == 1.0)
        rows.append({
            "inconsistency_multiplier": m,
            "system_is_consistent": consistent,
            "residual_floor": hist[-1],
            "last5_floors": tail,
            "tail_plateau_ratio": float(plateau),
            "final_amplitude": amps[-1],
            "a_final": float(a),
            "iters": k,
            "signature": ("CONVERGED" if hist[-1] < 1e-12 else
                          ("RESIDUAL PLATEAU at a positive floor with bounded amplitude "
                           "(genuine-non-existence signature)" if plateau < 1.1 else
                           "NEITHER")),
        })
    inc = [r for r in rows if not r["system_is_consistent"]]
    ratio = (inc[-1]["residual_floor"] / inc[0]["residual_floor"]) if len(inc) >= 2 else None
    predicted = ((multipliers[-1] - 1.0) / (multipliers[1] - 1.0)) if len(multipliers) >= 3 else None
    return {
        "rows": rows,
        "floor_ratio_measured": ratio,
        "floor_ratio_predicted_from_imposed_inconsistency": predicted,
        "reading": ("the non-existence arm of the classifier FIRES, and quantitatively: on the "
                    "provably-unsolvable systems the residual floor is flat to 4 significant "
                    "figures over the last 5 iterations at bounded amplitude, and the floor "
                    "scales with the imposed inconsistency exactly as predicted.  So the "
                    "classifier could have returned 'genuine non-existence' on leg 125's "
                    "stall and did not (lesson 90)."),
    }


# ---------------------------------------------------------------------------
# assembly
# ---------------------------------------------------------------------------

def main():
    t0 = time.time()
    payload = {
        "leg": 185,
        "route": "ROUTE-M2SD",
        "branch": "leg/185-m2sd-v1",
        "diagnostic_only": True,
        "no_dynamics_run": True,
        "builds_no_solver_module": True,
        "stage_claimed": None,
        "clay_odds_unchanged": 0.0005,
        "float_not_certificate": ("Every number here is floating point.  Nothing here is a "
                                  "certificate, and no radii-polynomial bound is computed."),
        "reads_read_only": ["solver/dissipative_profile.py (leg 125)",
                            "writeup/data/p2_route_m2p_v1_promotion.json (leg 125)"],
        "direction_md_provenance_correction": {
            "as_written_in_DIRECTION_md": "residual 2.65-3.75 with c_l running to -10.7",
            "as_measured_here": ("the runaway parameter is `a`, not `c_l` (c_l is HELD at 1/2 "
                                 "by newton_gamma2), it runs to -10.09246141, and the "
                                 "plateauing quantity is the RELATIVE residual over "
                                 "4.4118-5.4857; the ABSOLUTE residual falls to 1.2071e-15"),
            "effect_on_the_gate": "none -- the gate's question is unchanged",
        },
    }
    d1, d2 = d1_d2_residual_trend_and_jacobian()
    payload["D1_residual_trend_classification"] = d1
    payload["D2_jacobian_conditioning"] = d2
    payload["D3_parametrization_degeneracy"] = d3_parametrization_degeneracy()
    payload["D4_initial_guess_sensitivity"] = d4_initial_guess_sensitivity()
    payload["D5_is_a_genuine_profile_reachable"] = d5_is_a_genuine_profile_reachable()
    payload["D6_two_sided_calibration"] = d6_calibration()

    d4 = payload["D4_initial_guess_sensitivity"]
    d5 = payload["D5_is_a_genuine_profile_reachable"]
    payload["gate"] = {
        "question": ("Does the Newton stall on Object B, diagnosed against standard "
                     "non-existence signatures (residual plateau shape, Jacobian singularity "
                     "structure, parametrization degeneracy) versus standard solver-artifact "
                     "signatures (basin-of-attraction sensitivity, recoverable convergence "
                     "from a different initial guess at the SAME initial target), classify as "
                     "one or the other?"),
        "answer": "SOLVER ARTIFACT",
        "evidence": {
            "no_residual_plateau": ("the absolute residual at nu = 1.0 falls to "
                                    f"{d1['stalled']['residual_rms_absolute_final']:.4e} while "
                                    f"the amplitude falls from "
                                    f"{d1['stalled']['amplitude_initial']:.4f} to "
                                    f"{d1['stalled']['amplitude_final']:.4e} -- Newton "
                                    "CONVERGED, to the trivial null Omega = 0"),
            "no_jacobian_singularity": ("sigma_min(dR/dOmega) at the reached point is "
                                        f"{d2['at_trivial_null']['sigma_min_dR_dOmega']:.4f} "
                                        "with condition number "
                                        f"{d2['at_trivial_null']['cond_dR_dOmega']:.4e}; the "
                                        "a-column norm collapses to "
                                        f"{d2['at_trivial_null']['norm_dR_da_column']:.3e}"),
            "parametrization_degeneracy_is_real_but_is_the_SOLVER's": (
                "the exact null relation dF/dOmega[-X Omega_X] + 2 nu dF/dnu = 0 holds along "
                "every solution (discrete violation "
                f"{payload['D3_parametrization_degeneracy']['violation_relative_ladder'][0]:.3e} "
                f"-> {payload['D3_parametrization_degeneracy']['violation_relative_ladder'][-1]:.3e} "
                "under refinement), so nu is a gauge coordinate and leg 125's continuation IN "
                "nu, with the dilation freedom unfixed, was moving along a gauge orbit"),
            "recoverable_at_the_SAME_target": (
                f"{d4['n_recovered_nontrivial']} of {d4['n_guesses']} starts reach a "
                "non-trivial solution at the same nu = 1.0, worst relative residual "
                f"{d4['worst_recovered_relative_residual']:.3e}"),
        },
        "what_changed_the_outcome": ("the initial guess, and nothing else: leg 125 used ONE "
                                     "fixed guess (Chen's inviscid profile) for every nu, and "
                                     "at nu = 1.0 that guess is in the basin of the trivial "
                                     "null.  Seeding instead with the exact dilation of leg "
                                     "125's own lower-nu solutions -- which the covariance "
                                     "identity says ARE solutions at nu = 1.0 -- converges in "
                                     "2-3 iterations."),
        "is_a_genuine_profile_reachable": (
            "PARTLY, and the answer is a-dependent.  Re-parametrised as D3 prescribes (a "
            "fixed, nu unknown, dilation gauge imposed) the system is square and converges "
            "quadratically at every tested a.  The recovered nu is POSITIVE -- an admissible "
            "diffusive profile -- at a = 0.30 (nu = "
            f"{d5['grid_convergence_at_a_0p30'][-1]['nu']:.8f}, grid-converged and "
            "truncation-insensitive), and NEGATIVE, i.e. anti-diffusive and not a viscous "
            "profile at all, at Chen's a = 1/2 (nu = "
            f"{d5['nu_at_chen_a_one_half']['nu_from_nu0_0p3']:.8f} / "
            f"{d5['nu_at_chen_a_one_half']['nu_from_nu0_0p01']:.8f} from the two starts).  So "
            "Object B is reachable BELOW a* ~ 0.3865 and is not reachable at Chen's a."),
        "branch_taken": ("solver artifact -> report exactly what changed the outcome and "
                         "whether a genuine profile becomes reachable; ESCALATE as a candidate "
                         "follow-up construction leg; do NOT build the corrected continuation "
                         "here.  No corrected continuation is built in this module."),
    }
    payload["honest_ceiling"] = (
        "Not movement on L1->L4 and not Clay; Clay odds stay ~0.05%.  Diagnosing one solver's "
        "behaviour on one profile equation is not a theorem.  In particular the D5 objects are "
        "FLOAT solutions of a DISCRETISED equation on a truncated domain -- grid- and "
        "truncation-refined at a = 0.30, and nothing more than that.  No existence claim is "
        "made, and the negative half (nu < 0 at Chen's a) is a measurement on this "
        "discretisation, not a non-existence proof."
    )
    payload["seconds"] = time.time() - t0

    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    with open(DATA, "w") as fh:
        json.dump(payload, fh, indent=2)

    g = payload["gate"]
    print("D1 residual trend at the stalled nu = 1.0:")
    print(f"  absolute residual {d1['stalled']['trace'][0]['residual_rms_absolute']:.4e} -> "
          f"{d1['stalled']['residual_rms_absolute_final']:.4e}")
    print(f"  amplitude         {d1['stalled']['amplitude_initial']:.4f} -> "
          f"{d1['stalled']['amplitude_final']:.4e}")
    print(f"  relative residual (leg 125's only reported number): "
          f"{d1['stalled']['residual_relative_final']:.6f}")
    print(f"  classification: {d1['stalled']['classification']['classification']}")
    print(f"  control nu = 0.3: {d1['control']['classification']['classification']}")
    print("\nD2 Jacobian at the reached point:")
    print(f"  sigma_min(dR/dOmega) = {d2['at_trivial_null']['sigma_min_dR_dOmega']:.6f}, "
          f"cond = {d2['at_trivial_null']['cond_dR_dOmega']:.4e}, "
          f"|dR/da| = {d2['at_trivial_null']['norm_dR_da_column']:.4e}")
    print("\nD3 dilation-covariance identity, relative violation under refinement:")
    for r in payload["D3_parametrization_degeneracy"]["rows"]:
        print(f"  n = {r['n']:5d}  {r['identity_violation_relative']:.4e}   "
              f"(a converged to {r['a_converged']:.8f})")
    print("\nD4 initial-guess sensitivity at the SAME target nu = 1.0:")
    for r in payload["D4_initial_guess_sensitivity"]["rows"]:
        print(f"  {r['guess'][:52]:52s} a = {r['a_final']:+11.8f}  relres = "
              f"{r['residual_relative']:.3e}  amp = {r['amplitude']:.4f}")
    print("\nD5 a fixed, nu UNKNOWN, dilation gauge imposed:")
    for r in payload["D5_is_a_genuine_profile_reachable"]["a_sweep"]:
        print(f"  a = {r['a']:.4f}  nu = {r['nu_from_nu0_0p3']:+.8f} / "
              f"{r['nu_from_nu0_0p01']:+.8f}  admissible(nu>0) = {r['admissible_positive_nu']}")
    print("  grid ladder at a = 0.30: "
          + ", ".join(f"{v:.8f}" for v in payload["D5_is_a_genuine_profile_reachable"]["nu_ladder_at_a_0p30"]))
    print("\nD6 calibration (the non-existence arm must be able to fire):")
    for r in payload["D6_two_sided_calibration"]["rows"]:
        print(f"  multiplier {r['inconsistency_multiplier']:<4g} floor = "
              f"{r['residual_floor']:.4e}  amp = {r['final_amplitude']:.4f}  "
              f"{r['signature'][:44]}")
    print(f"\nGATE: {g['answer']}")
    print(f"  {g['is_a_genuine_profile_reachable']}")
    print(f"\nwrote {DATA}  ({payload['seconds']:.1f}s)")


if __name__ == "__main__":
    main()
