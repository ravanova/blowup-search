"""Leg 85 / Route-GRA — adversarial audit of solver/gclm_rescaled.py's fixed-point reporting.

THE GATE (verbatim, from DIRECTION.md leg 85):

    Under an adversarial battery of non-convergent upwind-transport trajectories (sustained
    oscillation, slow drift near a saddle rather than the fixed point), does
    solver/gclm_rescaled.py's relaxation loop ever report having reached the fixed point when
    it has not?

This script runs the battery and emits every magnitude to
writeup/data/p2_route_gra_v1_adversarial.json.  It READS solver/gclm_rescaled.py and never
edits, subclasses or monkeypatches it: every trajectory below is driven through the real
`RescaledCLM.run()` exactly as a caller would.

WHAT IS AND IS NOT MEASURED.  This is a STATUS-REPORTING audit of a Python predicate --
`res < tol` at gclm_rescaled.py:157 and the `break` at :145-146.  It is not a gCLM physics
measurement and varies no model parameter (`a = 0` throughout, single point, no sweep), so it
does not touch the plan-of-record ban on further gCLM measurement legs.  See
writeup/novelty/leg_85.md sec 0.

THE DECISIVE METRIC: POST-STOP RELATIVE DRIFT.
An absolute residual is not gauge-invariant, so "res < tol" cannot by itself settle whether a
trajectory is at rest.  The battery therefore measures, for every trajectory, how much the
returned state STILL MOVES after the loop declared convergence:

    post_stop_drift = ||f(after N more steps) - f_returned||_inf / ||f_returned||_inf

This is dimensionless and invariant under the scaling gauge.  A genuinely relaxed trajectory
has post_stop_drift ~ 1e-9.  A value of order 1 means the loop stopped on a state that
subsequently changes by its own full amplitude -- i.e. it never relaxed at all.

THE MECHANISM THE BATTERY ISOLATES.
The rescaled CLM fixed point is not a point but a ONE-PARAMETER LINE.  The dilation term
X d/dX is scale-invariant and H is scale-invariant at the origin, so

    Omega_lambda(X) = Omega_0(lambda X) = -4 lambda X / (1 + 4 lambda^2 X^2)

is an exact steady state for EVERY lambda > 0, all with c_omega = -1.  The member is selected
by the origin slope f(0) = Omega_X(0) = -4 lambda, which the scheme freezes exactly (both the
advection speed tanh(0) and the source H Omega - H Omega(0) vanish at rho = 0).  The module's
own docstring states the corresponding fact for the caller: "the rescaled initial amplitude is
a FREE GAUGE".

The dynamics are equivariant along this gauge and ||f_tau||_inf scales LINEARLY in lambda,
while `tol` is a FIXED ABSOLUTE number.  So the stopping test is not scale-invariant along the
one direction the module declares free.  Family G below sweeps lambda and measures the
consequence.

Run:  python experiments/p2_route_gra_v1_adversarial.py
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.gclm_rescaled import RescaledCLM, clm_profile  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_gra_v1_adversarial.json")

# The exact profile's peak, |Omega_0|_inf = 1.0 at X = +-1/2; used to make the shape error a
# fraction of the thing that is supposed to be there.
OMEGA0_PEAK = 1.0

# post-stop drift is measured over this many further steps of the SAME integrator
DRIFT_STEPS = 4000


def gauge_profile(X, lam):
    """Omega_lambda(X)/X = the exact steady state at gauge lambda, as the evolved variable f."""
    return -4.0 * lam / (1.0 + 4.0 * (lam * X) ** 2)


def shape_error(omega, X, radius=5.0):
    """||Omega - Omega_0||_inf over the core, absolute (Omega_0 peaks at 1)."""
    exact = clm_profile(X)
    core = np.abs(X) < radius
    core[:3] = False
    core[-3:] = False
    if not np.any(core) or not np.all(np.isfinite(omega[core])):
        return float("nan")
    return float(np.abs(omega[core] - exact[core]).max())


def post_stop_drift(solver, result, nsteps=DRIFT_STEPS, dt_frac=0.4):
    """How much the RETURNED state still moves, relative to its own amplitude.

    The gauge-invariant test of "is it actually at rest?".  Returns nan on a non-finite state
    (which the loop already reports as not-converged, so there is nothing to audit there)."""
    f = np.asarray(result["f"], dtype=float).copy()
    if not np.all(np.isfinite(f)):
        return float("nan")
    scale = float(np.abs(f).max())
    if scale == 0.0:
        return 0.0
    dt = dt_frac * solver.drho
    f_end = f.copy()
    for _ in range(nsteps):
        f_end, _, _ = solver.step(f_end, dt)
    if not np.all(np.isfinite(f_end)):
        return float("inf")
    return float(np.abs(f_end - f).max() / scale)


def audit(solver, label, family, f_init, dt_frac=0.4, tol=1e-8, max_steps=20000, note=""):
    """Run one adversarial trajectory through the REAL run() and report every magnitude."""
    r = solver.run(np.asarray(f_init, dtype=float), dt_frac=dt_frac, tol=tol,
                   max_steps=max_steps)
    conv = bool(r["converged"])
    drift = post_stop_drift(solver, r, dt_frac=dt_frac)
    c_om = float(r["c_omega"])
    err = shape_error(r["omega"], solver.X)
    rec = {
        "label": label,
        "family": family,
        "note": note,
        "n": int(solver.n),
        "tol": float(tol),
        "dt_frac": float(dt_frac),
        "reported_converged": conv,
        "reported_residual": float(r["residual"]),
        "steps": int(r["steps"]),
        "tau": float(r["tau"]),
        "c_omega": c_om,
        "c_omega_abs_error_vs_exact_minus_1": (float("nan") if not np.isfinite(c_om)
                                               else abs(c_om - (-1.0))),
        "f_origin": float(r["f"][solver.i0]) if np.isfinite(r["f"][solver.i0]) else float("nan"),
        "shape_err_inf_vs_Omega0": err,
        "shape_err_as_fraction_of_peak": (float("nan") if not np.isfinite(err)
                                          else err / OMEGA0_PEAK),
        "post_stop_rel_drift": drift,
        "drift_steps": DRIFT_STEPS,
    }
    # THE VERDICT for this trajectory.  A false positive is: the loop said converged, AND the
    # returned state is not at rest by the gauge-invariant measure.  1e-3 is three orders of
    # magnitude above what a genuinely relaxed trajectory shows (measured: ~2e-9).
    rec["false_positive"] = bool(conv and np.isfinite(drift) and drift > 1e-3)
    return rec


def main():
    records = []
    s = RescaledCLM(n=601, c=0.5, rho_max=7.0)
    X = s.X
    gauss = -4.0 * np.exp(-X ** 2 / 2.0)  # f(0) = -4, the validated gauge

    # ---- Family G: the amplitude/scaling gauge the module declares FREE -------------------
    # f_init = lam * (validated data).  Since the scheme freezes f(0) = -4 lam, lam IS the
    # member of the fixed-point line this trajectory is heading for.  The residual scales
    # linearly in lam; tol does not.
    for lam in (1.0, 1e-1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-9, 1e-10):
        records.append(audit(
            s, f"G_lambda_{lam:.0e}", "G_amplitude_gauge", lam * gauss,
            note="lam*validated data; the module's docstring calls this amplitude a free gauge"))

    # ---- Family S: exact members of the fixed-point line, off the validated member ---------
    # These ARE genuine steady states (drift ~ 1e-9 expected).  They are in the battery as the
    # CONTROL that separates "converged to the wrong member of the gauge line" (honest, and the
    # rate c_omega -> -1 is still correct) from "never relaxed at all" (the failure).
    for lam in (2.0, 4.0, 0.5, 0.25):
        records.append(audit(
            s, f"S_lambda_{lam:g}", "S_gauge_line_member", gauge_profile(X, lam),
            note="exact Omega_lambda: a genuine steady state, but not the validated Omega_0"))

    # ---- Family O: sustained oscillation / marginal and past-limit time steps ---------------
    for dtf in (0.4, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0):
        records.append(audit(
            s, f"O_dtfrac_{dtf:g}", "O_oscillation", gauss, dt_frac=dtf, max_steps=6000,
            note="upwind/SSPRK3 time step pushed toward and past its stability limit"))
    records.append(audit(
        s, "O_mode6", "O_oscillation", gauss * (1.0 + 0.3 * np.cos(6.0 * s.rho)),
        max_steps=40000, note="high-wavenumber modulation in rho (f(0) = -5.2, i.e. lam=1.3)"))
    records.append(audit(
        s, "O_far_bump", "O_oscillation",
        gauss + 0.5 * np.exp(-(np.abs(X) - 40.0) ** 2 / 8.0) * np.sign(X),
        max_steps=40000,
        note="distant far-field bump that must advect out: slow drift at the validated gauge"))

    # ---- Family N: the trivial fixed point, and non-finite states ---------------------------
    records.append(audit(s, "N_zero", "N_trivial_and_nonfinite", np.zeros_like(X),
                         note="f == 0 is an exact fixed point, but NOT the CLM one"))
    records.append(audit(s, "N_tiny_const", "N_trivial_and_nonfinite",
                         1e-12 * np.ones_like(X), note="1e-12 constant"))
    records.append(audit(s, "N_overflow", "N_trivial_and_nonfinite",
                         -4e6 * np.exp(-X ** 2 / 2.0), max_steps=3000,
                         note="amplitude large enough to overflow: does NaN reach res < tol?"))
    nan_seed = gauss.copy()
    nan_seed[np.abs(X) < 0.1] = np.nan
    records.append(audit(s, "N_nan_seed", "N_trivial_and_nonfinite", nan_seed, max_steps=3000,
                         note="NaN planted in the initial data"))

    # ---- The mechanism, measured directly: residual is exactly degree-1 in the gauge --------
    scaling = []
    for lam in (1.0, 1e-3, 1e-6, 1e-9):
        res = float(np.abs(s.rhs(lam * gauss)[0]).max())
        scaling.append({"lambda": lam, "residual": res, "residual_over_lambda": res / lam})

    # ---- Resolution independence of the failing trajectory ----------------------------------
    resolution = []
    for n, rho_max in ((401, 6.0), (601, 7.0), (901, 7.5)):
        sv = RescaledCLM(n=n, c=0.5, rho_max=rho_max)
        rec = audit(sv, f"G_lambda_1e-10_n{n}", "G_amplitude_gauge",
                    1e-10 * (-4.0 * np.exp(-sv.X ** 2 / 2.0)),
                    note="the failing trajectory, re-run at a different resolution")
        rec["rho_max"] = rho_max
        resolution.append(rec)

    # ---- Secondary: the reported residual is the PRE-step value (off by one step) -----------
    sv = RescaledCLM(n=401, c=0.5, rho_max=6.0)
    f_pre = -4.0 * np.exp(-sv.X ** 2 / 2.0)
    f_post, _, res_reported = sv.step(f_pre, 0.4 * sv.drho)
    res_pre = float(np.abs(sv.rhs(f_pre)[0]).max())
    res_post = float(np.abs(sv.rhs(f_post)[0]).max())
    offby = {
        "residual_reported_by_step": float(res_reported),
        "residual_of_the_state_passed_in": res_pre,
        "residual_of_the_state_returned": res_post,
        "reported_equals_pre_step": bool(abs(res_reported - res_pre) < 1e-15 * max(1.0, res_pre)),
        "relative_mismatch_vs_returned_state": abs(res_reported - res_post) / res_post,
    }

    fps = [r for r in records if r["false_positive"]]
    summary = {
        "leg": 85,
        "route": "GRA",
        "module_audited": "solver/gclm_rescaled.py",
        "module_edited": False,
        "gate": ("Under an adversarial battery of non-convergent upwind-transport trajectories "
                 "(sustained oscillation, slow drift near a saddle rather than the fixed "
                 "point), does solver/gclm_rescaled.py's relaxation loop ever report having "
                 "reached the fixed point when it has not?"),
        "gate_answer": "yes" if fps else "no",
        "trajectories_run": len(records),
        "false_positive_count": len(fps),
        "false_positive_labels": [r["label"] for r in fps],
        "worst_post_stop_drift_among_reported_converged": max(
            [r["post_stop_rel_drift"] for r in records
             if r["reported_converged"] and np.isfinite(r["post_stop_rel_drift"])],
            default=float("nan")),
        "nan_ever_reported_converged": any(
            r["reported_converged"] and not np.isfinite(r["reported_residual"])
            for r in records),
        "false_positive_at_validated_gauge_f0_minus4": any(
            r["false_positive"] for r in records
            if np.isfinite(r["f_origin"]) and abs(abs(r["f_origin"]) - 4.0) < 1e-9),
    }

    payload = {
        "summary": summary,
        "trajectories": records,
        "residual_scales_linearly_in_the_gauge": scaling,
        "resolution_independence": resolution,
        "reported_residual_is_pre_step": offby,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=2)

    print(f"{'label':22s} {'conv':5s} {'residual':10s} {'steps':>6s} {'c_omega':>9s} "
          f"{'shape_err':>10s} {'post-drift':>11s}  FP")
    for r in records:
        print(f"{r['label']:22s} {str(r['reported_converged']):5s} "
              f"{r['reported_residual']:.3e} {r['steps']:6d} {r['c_omega']:+9.4f} "
              f"{r['shape_err_inf_vs_Omega0']:10.3e} {r['post_stop_rel_drift']:11.4e}  "
              f"{'<-- FALSE POSITIVE' if r['false_positive'] else ''}")
    print(f"\nGATE ANSWER: {summary['gate_answer'].upper()}  "
          f"({summary['false_positive_count']}/{summary['trajectories_run']} trajectories)")
    print(f"  false positives: {summary['false_positive_labels']}")
    print(f"  NaN ever reported converged: {summary['nan_ever_reported_converged']}")
    print(f"  false positive at the validated gauge f(0)=-4: "
          f"{summary['false_positive_at_validated_gauge_f0_minus4']}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
