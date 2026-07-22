"""Stage 1 acceptance checks for the gCLM solver (PLAN.md Stage 1).

Three checks, because CLM alone does not exercise the hard part:

1. clm_analytic      — growth/Hilbert term (a=0, nu=0): the simulated
                       max|w(t)| fed through win_condition.estimate_blowup_time
                       must match CLM's closed-form blow-up time across >=3
                       initial conditions.
2. diffusion_decay   — diffusion term (nu>0, nonlinearity off): pure
                       diffusion against the exact mode-decay solution.
3. advection checks  — the a*u*w_x transport operator, which neither of the
                       above touches: a frozen-u pure-transport run against
                       the exact translated solution, plus conservation of
                       the gCLM invariant (integral of w) on general
                       non-odd De Gregorio (a=1) data.
   (The Okamoto–Sakajo–Wunsch critical-a reproduction — the third variant
   PLAN.md lists — needs the specific published value looked up first; the
   validation-log schema already reserves check="osw_critical_a" for it.)

Every run of this file appends one row per check to
experiments/solver_validation.jsonl tagged with the current commit
(LOGGING.md schema #9), so solver accuracy is a tracked series across
commits, not a one-time gate.
"""

import numpy as np

from ga.logbook import append_solver_validation
from solver.gclm import clm_analytic_blowup_time, solve_gclm
from solver.spectral_utils import grid, wavenumbers
from win_condition import WinTier, classify_candidate, estimate_blowup_time

# --- check 1: CLM against its closed-form blow-up time ---

CLM_INITIAL_CONDITIONS = [
    # (label, w0(x)); analytic T* = 2 / max{H(w0)(x) : w0(x) = 0}
    ("sin(x)", lambda x: np.sin(x)),                        # T* = 2
    ("2sin(x)", lambda x: 2.0 * np.sin(x)),                 # T* = 1 (scale covariance)
    ("sin(x)+0.3sin(2x)", lambda x: np.sin(x) + 0.3 * np.sin(2 * x)),  # T* = 2/0.7
]


def check_clm_analytic(resolution_n=1024, rel_tol=0.01):
    # Window calibration: exactly, 1/M = (T*-t) - (T*-t)^2/4 for CLM, so the
    # reciprocal has genuine quadratic curvature far from the singularity and
    # a linear fit over a deep tail overestimates T* by ~2-3% (verified
    # against the closed-form solution — solver M(t) matches it to 4-5
    # digits). Fit the last 15% of samples of a deep (100x) amplification
    # run, which sits in the asymptotic regime: T* error ~0.1-0.2%,
    # independent of resolution.
    rows = []
    for label, w0_fn in CLM_INITIAL_CONDITIONS:
        t_star_exact = clm_analytic_blowup_time(w0_fn)
        assert t_star_exact is not None, f"{label}: expected analytic blow-up"
        result = solve_gclm(
            w0_fn(grid(resolution_n)), a=0.0, nu=0.0,
            t_max=t_star_exact + 1.0, amplification_factor=100.0,
        )
        rel_err = np.inf
        tier = WinTier.NONE
        if result.outcome == "blowup_candidate":
            est = estimate_blowup_time(
                result.times.tolist(), result.max_omega.tolist(),
                tail_fraction=0.15,
            )
            if est is not None:
                rel_err = abs(est.t_star - t_star_exact) / t_star_exact
                tier = classify_candidate(est)
        rows.append({
            "check": "clm_analytic",
            "initial_condition_label": label,
            "error_metric": float(rel_err),
            "passed": bool(rel_err < rel_tol and tier is WinTier.CANDIDATE
                           and result.conservation_drift < 1e-2),
        })
    return rows


# --- check 2: pure diffusion against exact mode decay ---

def check_diffusion_decay(resolution_n=256, nu=0.1, t_end=1.0):
    x = grid(resolution_n)
    w0 = np.sin(3 * x)
    result = solve_gclm(w0, a=0.0, nu=nu, t_max=t_end, nonlinear=False)
    exact = np.exp(-nu * 9.0 * t_end) * np.sin(3 * x)
    err = float(np.max(np.abs(result.omega_final - exact)))
    return [{
        "check": "diffusion_decay",
        "initial_condition_label": "sin(3x)",
        "error_metric": err,
        "passed": bool(err < 1e-12 and result.outcome == "no_blowup"),
    }]


# --- check 3a: frozen-u pure transport against the exact translate ---

def check_advection_transport(resolution_n=256, a=1.0, u_frozen=1.0, t_end=1.0):
    x = grid(resolution_n)
    w0 = np.sin(x) + 0.3 * np.cos(2 * x) + 0.1 * np.sin(5 * x)
    result = solve_gclm(
        w0, a=a, nu=0.0, t_max=t_end, frozen_u=u_frozen, dt_max=5e-3,
    )
    # w_t + a*c*w_x = 0  =>  w(x, t) = w0(x - a*c*t); exact via phase shift.
    k = wavenumbers(resolution_n)
    exact = np.fft.irfft(
        np.fft.rfft(w0) * np.exp(-1j * k * a * u_frozen * result.t_final),
        resolution_n,
    )
    err = float(np.max(np.abs(result.omega_final - exact)))
    return [{
        "check": "advection_transport",
        "initial_condition_label": "sin(x)+0.3cos(2x)+0.1sin(5x)",
        "error_metric": err,
        "passed": bool(err < 1e-8),
    }]


# --- check 3b: gCLM invariant conservation on general (non-odd) data ---

def check_invariant_conservation(resolution_n=256, t_end=1.0):
    # integral of w is conserved by every term of gCLM (Hilbert-transform
    # antisymmetry), for all a and nu — but it is identically zero for odd
    # data, so this check deliberately uses general non-odd data, where all
    # of (integral w != 0, advection active, stretching active) hold at once.
    # Drift is normalized by ||w||_1, never by the invariant itself.
    x = grid(resolution_n)
    w0 = np.sin(x) + 0.4 * np.cos(2 * x) + 0.2 * np.sin(3 * x)
    result = solve_gclm(w0, a=1.0, nu=0.0, t_max=t_end)
    return [{
        "check": "invariant_conservation",
        "initial_condition_label": "sin(x)+0.4cos(2x)+0.2sin(3x), a=1",
        "error_metric": result.mean_drift,
        "passed": bool(result.mean_drift < 1e-10
                       and result.energy_balance_residual < 1e-3),
    }]


# --- pytest-style wrappers (each also appends its validation rows) ---

def _run_and_record(check_fn):
    rows = check_fn()
    append_solver_validation(rows)
    for row in rows:
        assert row["passed"], (
            f"{row['check']} failed on {row['initial_condition_label']}: "
            f"error_metric={row['error_metric']:.3e}"
        )
    return rows


def test_clm_analytic_blowup_time():
    _run_and_record(check_clm_analytic)


def test_diffusion_decay():
    _run_and_record(check_diffusion_decay)


def test_advection_transport():
    _run_and_record(check_advection_transport)


def test_invariant_conservation():
    _run_and_record(check_invariant_conservation)


if __name__ == "__main__":
    all_rows = []
    for check in (check_clm_analytic, check_diffusion_decay,
                  check_advection_transport, check_invariant_conservation):
        rows = check()
        all_rows.extend(rows)
        for row in rows:
            status = "PASS" if row["passed"] else "FAIL"
            print(f"{status}: {row['check']} [{row['initial_condition_label']}] "
                  f"error={row['error_metric']:.3e}")
    append_solver_validation(all_rows)
    n_passed = sum(r["passed"] for r in all_rows)
    print(f"\n{n_passed}/{len(all_rows)} checks passed "
          f"(logged to experiments/solver_validation.jsonl)")
    if n_passed != len(all_rows):
        raise SystemExit(1)
