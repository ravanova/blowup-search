"""Gate 1a acceptance checks for the 2D Boussinesq solver (PHASE1_PLAN.md).

An exact analytic ladder, each check isolating ONE piece of new machinery so no
two unknowns are ever debugged at once (the Phase-0 discipline):

1. biot_savart      — single-mode w -> u analytic, and div(u)=0 at machine zero.
2. rhs_terms        — full spectral RHS (advection assembly + buoyancy th_x) vs
                      a hand-computed analytic RHS on low modes. Isolates the
                      buoyancy coupling and the advection assembly, exactly.
3. scalar_transport — frozen divergence-free u translates th exactly (the 2D
                      analog of the gCLM frozen-u check).
4. viscous_decay    — single-mode w under pure diffusion -> exp(-nu k^2 t).
5. taylor_green     — w = e^{-2 nu t} sin x sin y, an exact solution of the full
                      advection+viscous (buoyancy off) system: advection
                      self-cancels, so this checks Biot-Savart + transport
                      dynamically, together.
6. conservation     — general nonlinear run with buoyancy on: total vorticity
                      and total theta drift at machine scale; energy-balance
                      residual small.

Every run appends one row per check to experiments/solver_validation.jsonl
tagged with the current commit (same tracked series as test_solver_clm.py).
"""

import numpy as np

from ga.logbook import append_solver_validation
from solver.boussinesq import (
    TWO_PI,
    dealias_mask2d,
    grid2d,
    solve_boussinesq,
    velocity_from_vorticity,
    wavenumbers2d,
    _rhs_hat,
)


# --- check 1: Biot-Savart single mode + divergence-free ---

def check_biot_savart(n=64):
    X, Y = grid2d(n)
    KX, KY, Ksq, inv_Ksq = wavenumbers2d(n)
    # w = sin(x): psi = -sin(x), u = -psi_y = 0, v = psi_x = -cos(x).
    w = np.sin(X)
    u, v = velocity_from_vorticity(np.fft.fft2(w), KX, KY, inv_Ksq)
    err_mode = max(float(np.max(np.abs(u - 0.0))),
                   float(np.max(np.abs(v - (-np.cos(X))))))
    # Divergence of a general random-field velocity must vanish spectrally.
    rng = np.random.default_rng(0)
    w_rand = rng.standard_normal((n, n))
    w_rand -= w_rand.mean()
    w_hat = np.fft.fft2(w_rand)
    u_hat = 1j * KY * w_hat * inv_Ksq
    v_hat = -1j * KX * w_hat * inv_Ksq
    div = np.fft.ifft2(1j * KX * u_hat + 1j * KY * v_hat).real
    err_div = float(np.max(np.abs(div)))
    err = max(err_mode, err_div)
    return [{
        "check": "biot_savart",
        "initial_condition_label": "w=sin(x); div(random)",
        "error_metric": err,
        "passed": bool(err < 1e-12),
    }]


# --- check 2: full RHS terms vs analytic ---

def check_rhs_terms(n=64):
    # w0 = sin(x) + sin(2y), th0 = cos(x). Velocities (from Biot-Savart):
    #   from sin(x):  (0, -cos x);  from sin(2y):  ((1/2)cos 2y, 0)
    #   => u = (1/2)cos(2y),  v = -cos(x).
    # Analytic RHS (buoyancy on):
    #   dw/dt = -(u w_x + v w_y) + th_x = 1.5 cos(x)cos(2y) - sin(x)
    #   dth/dt = -(u th_x + v th_y)     = 0.5 sin(x)cos(2y)
    X, Y = grid2d(n)
    KX, KY, Ksq, inv_Ksq = wavenumbers2d(n)
    mask = dealias_mask2d(n)
    w0 = np.sin(X) + np.sin(2 * Y)
    th0 = np.cos(X)
    w_hat = np.fft.fft2(w0) * mask
    th_hat = np.fft.fft2(th0) * mask
    dw_hat, dth_hat, u, v = _rhs_hat(w_hat, th_hat, KX, KY, inv_Ksq, mask,
                                     nonlinear=True, buoyancy=True, frozen_u=None)
    dw = np.fft.ifft2(dw_hat).real
    dth = np.fft.ifft2(dth_hat).real
    dw_exact = 1.5 * np.cos(X) * np.cos(2 * Y) - np.sin(X)
    dth_exact = 0.5 * np.sin(X) * np.cos(2 * Y)
    err = max(float(np.max(np.abs(dw - dw_exact))),
              float(np.max(np.abs(dth - dth_exact))))
    return [{
        "check": "rhs_terms",
        "initial_condition_label": "w=sin(x)+sin(2y), th=cos(x)",
        "error_metric": err,
        "passed": bool(err < 1e-12),
    }]


# --- check 3: frozen-u pure transport against exact translate ---

def check_scalar_transport(n=64, t_end=1.0):
    X, Y = grid2d(n)
    KX, KY, Ksq, inv_Ksq = wavenumbers2d(n)
    th0 = np.sin(X) + 0.3 * np.cos(2 * X) * np.cos(Y) + 0.1 * np.sin(3 * Y)
    w0 = np.cos(X) * np.sin(Y)  # carried along; not checked
    res = solve_boussinesq(
        w0, th0, nu=0.0, kappa=0.0, t_max=t_end, frozen_u=(1.0, 0.0),
        buoyancy=False, dt_max=5e-3,
    )
    # th_t - th_x = 0 (u=(1,0)) => th(x,y,t) = th0(x - t, y); exact phase shift.
    exact = np.fft.ifft2(np.fft.fft2(th0) * np.exp(-1j * KX * res.t_final)).real
    err = float(np.max(np.abs(res.theta_final - exact)))
    return [{
        "check": "scalar_transport",
        "initial_condition_label": "frozen u=(1,0), th translate",
        "error_metric": err,
        "passed": bool(err < 1e-8),
    }]


# --- check 4: pure viscous decay against exact mode decay ---

def check_viscous_decay(n=64, nu=0.1, kappa=0.05, t_end=1.0):
    X, Y = grid2d(n)
    w0 = np.sin(2 * X) + np.sin(3 * Y)
    th0 = np.cos(X) * np.cos(Y)
    res = solve_boussinesq(w0, th0, nu=nu, kappa=kappa, t_max=t_end,
                           nonlinear=False, buoyancy=False)
    w_exact = (np.exp(-nu * 4.0 * t_end) * np.sin(2 * X)
               + np.exp(-nu * 9.0 * t_end) * np.sin(3 * Y))
    th_exact = np.exp(-kappa * 2.0 * t_end) * np.cos(X) * np.cos(Y)
    err = max(float(np.max(np.abs(res.omega_final - w_exact))),
              float(np.max(np.abs(res.theta_final - th_exact))))
    return [{
        "check": "viscous_decay",
        "initial_condition_label": "w=sin2x+sin3y, th=cosx cosy",
        "error_metric": err,
        "passed": bool(err < 1e-10 and res.outcome == "no_blowup"),
    }]


# --- check 5: Taylor-Green exact solution (advection cancels + viscous decay) ---

def check_taylor_green(n=64, nu=0.05, t_end=1.0):
    X, Y = grid2d(n)
    w0 = np.sin(X) * np.sin(Y)  # k^2 = 2 Laplacian eigenfunction => steady Euler
    th0 = np.zeros((n, n))
    res = solve_boussinesq(w0, th0, nu=nu, kappa=0.0, t_max=t_end,
                           nonlinear=True, buoyancy=False, dt_max=2e-3)
    exact = np.exp(-2.0 * nu * t_end) * np.sin(X) * np.sin(Y)
    err = float(np.max(np.abs(res.omega_final - exact)))
    return [{
        "check": "taylor_green",
        "initial_condition_label": "w=sin(x)sin(y), nu>0",
        "error_metric": err,
        "passed": bool(err < 1e-8 and res.outcome == "no_blowup"),
    }]


# --- check 6: conservation of total vorticity & theta on a general run ---

def check_conservation(n=64, t_end=1.0):
    X, Y = grid2d(n)
    # General, non-symmetric, modest-amplitude data; buoyancy active.
    w0 = 0.5 * (np.sin(X) * np.cos(Y) + 0.4 * np.cos(2 * X)
                + 0.3 * np.sin(X + 2 * Y))
    th0 = 0.5 * (np.cos(X) + 0.3 * np.sin(2 * Y) * np.cos(X))
    res = solve_boussinesq(w0, th0, nu=0.0, kappa=0.0, t_max=t_end,
                           buoyancy=True, dt_max=2e-3)
    return [{
        "check": "conservation",
        "initial_condition_label": "general (w,th), buoyancy on",
        "error_metric": res.mean_drift,
        "passed": bool(res.mean_drift < 1e-10
                       and res.energy_balance_residual < 1e-3
                       and res.outcome == "no_blowup"),
    }]


_CHECKS = (check_biot_savart, check_rhs_terms, check_scalar_transport,
           check_viscous_decay, check_taylor_green, check_conservation)


def _run_and_record(check_fn):
    rows = check_fn()
    append_solver_validation(rows)
    for row in rows:
        assert row["passed"], (
            f"{row['check']} failed on {row['initial_condition_label']}: "
            f"error_metric={row['error_metric']:.3e}"
        )
    return rows


def test_biot_savart():
    _run_and_record(check_biot_savart)


def test_rhs_terms():
    _run_and_record(check_rhs_terms)


def test_scalar_transport():
    _run_and_record(check_scalar_transport)


def test_viscous_decay():
    _run_and_record(check_viscous_decay)


def test_taylor_green():
    _run_and_record(check_taylor_green)


def test_conservation():
    _run_and_record(check_conservation)


if __name__ == "__main__":
    all_rows = []
    for check in _CHECKS:
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
