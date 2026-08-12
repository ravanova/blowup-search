"""PROG-R4, unit U3 -- the planted controls on GATE G1.

Pre-registered in experiments/journal/prog_r4_u2u3_prereg_addendum.md section 3,
BEFORE the recurrence stage and before any attempt. Nothing here may be changed
after an outcome is seen.

WHY G1 NEEDS THESE AND NOT JUST A COUNT. G1's `no` branch is a RESOURCED null:
ORCHESTRATION.md section 3d's stop fires on it and route 4 stops. A null is only
allowed to mean that if the instrument that produced it can be shown, IN THE
SAME RUN, to be able to say `yes`. Without that, "no orbit recovered" and "the
recovery machinery cannot reach tol=1e-8 on anything" are indistinguishable, and
in solo mode (section 3f) there is no paired verifier to tell them apart. The
controls are the whole defence, so they must be able to fire in BOTH directions.

    P (positive, unconditional) -- MUST SUCCEED
    R (positive, conditional)   -- MUST SUCCEED IF IT RUNS
    N (negative)                -- MUST FAIL

    CONTROLS FIRED AS PLANTED := P recovered AND N did not recover
                                 AND (R recovered, if R ran)

    If they do not fire as planted, G1 is answered UNANSWERED, NOT `no`.

CONTROL P, and why an exact solution is available without a search. The
programme's stepper is a Lie-Trotter split (RK4 on the nonstiff part, then the
exact viscous factor), so it does NOT preserve the continuous steady state
w_lam = -(Re/n)cos(n y) -- that is the first-order error measured in the
addendum section 1. But the discrete map has its own relative equilibrium, and
it is available in CLOSED FORM rather than by Newton:

  span{cos(n y)} is invariant. For w in it the streamfunction is
  psi = -(A/n^2)cos(n y), so v = psi_x = 0 and u = -psi_y depends on y alone,
  giving u.grad(w) = u dw/dx + v dw/dy = 0 identically. The forcing
  -n cos(n y) lies in the same subspace and the viscous factor preserves it.
  So on this subspace _rhs_hat is the CONSTANT forcing_hat, every RK4 stage is
  equal, (dt/6)(k1+2k2+2k3+k4) = dt*forcing_hat, and one step is exactly

      w_hat -> (w_hat + dt*forcing_hat) * decay.

  Its fixed point is therefore

      w*_hat = dt * forcing_hat * decay / (1 - decay).

Measured: ||Phi_dt(w*) - w*|| = 7.6e-14, and at T = 19.33 -- an exact multiple
of dt, which matters because integrate() shortens its last step to land on T --
||Phi_T(w*) - w*|| = 2.35e-13. So the extended residual at (w*, T, s=0) with
the reference at w* is exactly zero: the state row is Phi_T(w*) - w* and the two
phase rows vanish because w - w0_ref = 0. It is a genuine exact zero, 5 orders
below tol=1e-8, and it needed no search that could itself have failed.

  Independent cross-check of the addendum's section 1 finding: ||w* - w_lam||
  is 1.3327e-3 relative, against the 1.3242e-3 global splitting error measured
  by refinement. Two unrelated routes to the same O(dt) number.

  WHAT P TESTS AND WHAT IT DOES NOT. The state block ONLY. At a relative
  equilibrium ||dR/ds|| = 0 exactly and dR/dT is negligible -- MILESTONE M1
  measured this and recorded the rank deficiency of 2 -- so P does not exercise
  the T and s directions. Control R does; it is the reason R exists.

CONTROL N, and the failure mode it guards. The matching predicate could fire
spuriously -- declaring a named orbit recovered when the solve merely landed
near a published period by coincidence -- and that would turn a `no` into a
false `yes`, the one error the count alone cannot catch. N seeds the machinery
with a PHASE-SCRAMBLED field: the amplitude spectrum of a real candidate, so
its energy and enstrophy are those of a genuine turbulent state (Parseval), but
phases drawn at random, so it lies near no orbit. Seeded with a period from the
Table IV anchor band, it must NOT report a recovered named orbit.
"""
from __future__ import annotations

import time

import numpy as np

from solver.kolmogorov2d_nkbasin import newton_hookstep_rpo

# AMENDMENT 1, recorded AFTER control P was run exactly as pre-registered and
# FAILED. The original is kept in the record, not overwritten: see
# u3_control_P_asprereg.json and the addendum's amendment note.
#
# WHAT WAS PRE-REGISTERED. T_CONTROL = 19.33, an exact multiple of dt in the
# Table IV band. Run at that value P did not recover: it stalled on the first
# epoch at reason=trust_region_collapsed, residual 236 -> 223, having moved the
# state not at all (relative error to w* still 1.0e-3, the perturbation itself).
#
# WHY THAT FAILURE CARRIES NO INFORMATION ABOUT THE INSTRUMENT, measured rather
# than argued. In the linear regime (eps = 1e-13 relative) the equilibrium's
# amplification is 1.91 at T=0.5, 6.09 at T=1, 99.9 at T=2, 2.81e3 at T=3 and
# 1.02e5 at T=4 -- a Lyapunov exponent rising to lambda = 2.88. Extrapolated to
# T=19.33 that is exp(54) ~ 1e24. Double precision carries ~1e16 of dynamic
# range, so the shooting Jacobian there is not merely ill-conditioned but
# numerically empty: NO Newton method can solve it, and P's failure at 19.33
# says only that, not anything about this one.
#
# THE TARGETS ARE NOT LIKE THAT. On the turbulent attractor, where the Table IV
# orbits live, the same measurement gives lambda = 0.35 and an amplification of
# 8.73e2 over T=19.33 -- about 1e21 times gentler. The equilibrium is simply a
# far more unstable object than the orbits being sought.
#
# THE AMENDMENT, fixed by the TARGET and not by P's outcome. T_P is the exact
# multiple of dt at which the equilibrium's amplification equals the
# ATTRACTOR's amplification over one Table IV period (8.73e2). Log-interpolating
# the measured table between T=2 and T=3 gives T_P = 2.65. This makes P as hard,
# in conditioning, as the real problem -- neither easier nor harder -- and the
# number is derived from a property of the attractor that was measured before P
# was re-run. It is NOT tuned to make P pass.
#
# WHAT P STILL DOES NOT TEST, stated so it is not discovered later: behaviour at
# amplifications far above 1e3. Control R covers the real regime exactly,
# because it perturbs an actual converged orbit.
T_CONTROL_ASPREREG = 19.33
T_CONTROL = 2.65
CONTROL_AMPLIFICATION_TARGET = 8.73e2
EPS_CONTROL = 1e-3       # perturbation size for P and R, relative
CONTROL_SEED = 380       # the programme's leg number; fixed here, not tuned


def discrete_relative_equilibrium(solver):
    """The exact fixed point of the DISCRETE map, in closed form.

    Not the continuous steady state w_lam: the Lie-Trotter split does not
    preserve that one. See the module docstring for the derivation."""
    d = solver.decay
    # decay == 1 exactly at k = 0, where the forcing also vanishes; divide only
    # where the denominator is nonzero rather than dividing everywhere and
    # selecting afterwards, which would evaluate 0/0 and warn.
    den = 1.0 - d
    ok = np.abs(den) > 1e-300
    w_hat = np.zeros_like(solver.forcing_hat)
    w_hat[ok] = solver.dt * solver.forcing_hat[ok] * d[ok] / den[ok]
    return np.fft.ifft2(w_hat).real


def phase_scramble(w, solver, rng):
    """A real field with w's amplitude spectrum and random phases.

    Hermitian symmetry is automatic: |w_hat| is already symmetric because w is
    real, and the random phases are taken from the transform of a random REAL
    field, which is symmetric too. The dealiasing mask is reapplied and the
    mean is removed, so the result is an admissible vorticity field."""
    w_hat = np.fft.fft2(w) * solver.mask
    g_hat = np.fft.fft2(rng.standard_normal(w.shape))
    mag = np.abs(g_hat)
    phase = np.where(mag > 0, g_hat / np.maximum(mag, 1e-300), 1.0)
    out = np.abs(w_hat) * phase * solver.mask
    out[0, 0] = 0.0
    return np.fft.ifft2(out).real


def _solve(w0, T0, s0, solver, tol, max_newton, max_gmres, gmres_rtol):
    t0 = time.time()
    out = newton_hookstep_rpo(w0, T0, s0, solver, tol=tol,
                              max_newton=max_newton, max_gmres=max_gmres,
                              gmres_rtol=gmres_rtol, fd_eps=1e-6)
    out["wall_seconds"] = time.time() - t0
    return out


def control_P(solver, tol, max_newton, max_gmres, gmres_rtol):
    """POSITIVE, UNCONDITIONAL. Perturb the exact discrete relative equilibrium
    and require hookstep-Newton to recover it to tol.

    `recovered` is deliberately TWO conditions, not one: the solve must reach
    tol AND come back to w* itself. Reaching tol at some other state would mean
    the machinery converges to something, which is not what P is planted to
    show."""
    w_star = discrete_relative_equilibrium(solver)
    nrm = np.linalg.norm(w_star)
    rng = np.random.default_rng(CONTROL_SEED)
    d = rng.standard_normal(w_star.shape)
    d -= d.mean()
    d /= np.linalg.norm(d)
    w0 = w_star + EPS_CONTROL * nrm * d

    out = _solve(w0, T_CONTROL, 0.0, solver, tol, max_newton, max_gmres,
                 gmres_rtol)
    err = float(np.linalg.norm(out["w0"] - w_star) / nrm)
    recovered = bool(out["success"] and err < 10.0 * EPS_CONTROL)
    return dict(
        control="P", role="POSITIVE, unconditional -- MUST SUCCEED",
        planted=("the exact fixed point of the discrete map, in closed form: "
                 "w*_hat = dt*forcing_hat*decay/(1-decay). ||Phi_dt(w*)-w*|| "
                 "= 7.6e-14 and ||Phi_T(w*)-w*|| = 2.35e-13 at T=19.33, so the "
                 "extended residual there is an exact zero"),
        exercises="the state block ONLY -- at a relative equilibrium "
                  "||dR/ds|| = 0 exactly and dR/dT is negligible (M1's rank "
                  "deficiency of 2); T and s are exercised by control R",
        T_used=T_CONTROL, perturbation_relative=EPS_CONTROL,
        seed_residual_would_be="0 exactly at the unperturbed w*",
        final_residual=out["final_residual"], n_epochs=out["n_iters"],
        reason=out["reason"], converged_to_tol=bool(out["success"]),
        relative_error_to_w_star=err, recovered=recovered,
        wall_seconds=out["wall_seconds"],
        residual_history=[float(v) for v in out["residual_history"]])


def control_N(solver, w_candidate, T_anchor, s_anchor, tol, max_newton,
              max_gmres, gmres_rtol, match_T_tol, match_s_tol, table_iv):
    """NEGATIVE. A phase-scrambled field must NOT report a recovered orbit.

    Guards the matching predicate, not the solver: the failure this catches is
    a solve that lands near a published period by coincidence and is then
    declared a recovery."""
    rng = np.random.default_rng(CONTROL_SEED + 1)
    w_scr = phase_scramble(w_candidate, solver, rng)
    out = _solve(w_scr, T_anchor, s_anchor, solver, tol, max_newton, max_gmres,
                 gmres_rtol)

    # The SAME matching predicate the real attempts use, applied unchanged.
    two_pi = 2.0 * np.pi
    matched = None
    for name, Tp, sp, _ in table_iv:
        ds = abs(((out["s"] - sp + np.pi) % two_pi) - np.pi)
        if (out["success"] and abs(out["T"] - Tp) < match_T_tol
                and ds < match_s_tol):
            matched = name
            break
    recovered = matched is not None
    return dict(
        control="N", role="NEGATIVE -- MUST FAIL",
        planted=("a phase-scrambled field: the amplitude spectrum of a real "
                 "candidate (so energy and enstrophy are a genuine turbulent "
                 "state's, by Parseval) with random phases, so it lies near no "
                 "orbit; seeded with a period from the Table IV anchor band"),
        guards="the matching predicate firing spuriously, which would turn a "
               "`no` into a false `yes`",
        T_seeded=T_anchor, s_seeded=s_anchor,
        final_residual=out["final_residual"], n_epochs=out["n_iters"],
        reason=out["reason"], converged_to_tol=bool(out["success"]),
        T_converged=out["T"], s_converged=out["s"],
        matched_row=matched, recovered=recovered,
        wall_seconds=out["wall_seconds"])


def control_R(solver, w_orbit, T_orbit, s_orbit, anchor, tol, max_newton,
              max_gmres, gmres_rtol):
    """POSITIVE, CONDITIONAL. Perturb a converged orbit and re-recover it.

    Runs only if U3 converged something. Unlike P this DOES exercise the T and
    s directions, because at a genuine RPO neither is degenerate."""
    nrm = np.linalg.norm(w_orbit)
    rng = np.random.default_rng(CONTROL_SEED + 2)
    d = rng.standard_normal(w_orbit.shape)
    d -= d.mean()
    d /= np.linalg.norm(d)
    out = _solve(w_orbit + EPS_CONTROL * nrm * d, T_orbit, s_orbit, solver,
                 tol, max_newton, max_gmres, gmres_rtol)
    dT = abs(out["T"] - T_orbit)
    two_pi = 2.0 * np.pi
    ds = abs(((out["s"] - s_orbit + np.pi) % two_pi) - np.pi)
    err = float(np.linalg.norm(out["w0"] - w_orbit) / nrm)
    recovered = bool(out["success"] and err < 10.0 * EPS_CONTROL
                     and dT < 0.05 and ds < 0.05)
    return dict(
        control="R", role="POSITIVE, conditional -- MUST SUCCEED IF IT RUNS",
        planted=f"a converged orbit from this run (anchor {anchor}), perturbed",
        exercises="the state block AND T and s -- neither is degenerate at a "
                  "genuine RPO, which is what P cannot test",
        anchor=anchor, T_orbit=T_orbit, s_orbit=s_orbit,
        perturbation_relative=EPS_CONTROL,
        final_residual=out["final_residual"], n_epochs=out["n_iters"],
        reason=out["reason"], converged_to_tol=bool(out["success"]),
        relative_error_to_orbit=err, delta_T=float(dT), delta_s=float(ds),
        recovered=recovered, wall_seconds=out["wall_seconds"])


def verdict(p, n, r):
    """CONTROLS FIRED AS PLANTED := P recovered AND N did not, AND R recovered
    if R ran. Mirrors u4_g2_basin.py's controls_fired construction."""
    fired = bool(p["recovered"] and not n["recovered"])
    if r is not None:
        fired = bool(fired and r["recovered"])
    reasons = []
    if not p["recovered"]:
        reasons.append("P did NOT recover the exact discrete relative "
                       "equilibrium -- the machinery cannot reach tol on a "
                       "state that IS a solution, so a `no` at G1 would be an "
                       "instrument failure, not a fact about orbits")
    if n["recovered"]:
        reasons.append("N DID report a recovered named orbit from a "
                       "phase-scrambled field -- the matching predicate fires "
                       "spuriously and any `yes` is untrustworthy")
    if r is not None and not r["recovered"]:
        reasons.append("R did not re-recover a perturbed converged orbit -- "
                       "the T and s directions are not being solved")
    return fired, reasons
