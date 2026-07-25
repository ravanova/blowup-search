"""Step-B validation, pieces 2-3 (PHASE2_SPIKE1_NOTES.md sec.3): the field GRADIENT operator
grad_xy (for the velocity-gradient fields u_x, v_x, u_y in the eta/xi reaction terms) and the
odd-field ORIGIN SLOPE read + MODULATION (2.11). Manufactured known answers throughout.

Run:  python test_boussinesq_rescaled.py
"""

import numpy as np

from solver.boussinesq_velocity import PolarGrid
from solver.boussinesq_rescaled import (
    grad_xy, odd_field_x_slope, modulation, transport, RescaledBoussinesq,
)


def _seed_fields(grid, a=1.3, b=0.7, c=0.5):
    """Smooth localized seed respecting the symmetry class: omega, eta odd in x (=0 at the
    axis beta=pi/2 via the x=r cos beta factor), xi even in x. All decay like e^{-r^2}."""
    env = np.exp(-(grid.R ** 2))
    omega = a * grid.X * env
    eta = b * grid.X * env
    xi = c * grid.Y * env
    return omega, eta, xi


def _f_and_derivs(grid):
    """f = e^{-r} sin(2 beta) and analytic f_x, f_y (same as the transport test's field)."""
    r, b = grid.R, grid.B
    e = np.exp(-r)
    f = e * np.sin(2 * b)
    f_r = -e * np.sin(2 * b)
    f_b = e * 2 * np.cos(2 * b)
    f_x = np.cos(b) * f_r - (np.sin(b) / r) * f_b
    f_y = np.sin(b) * f_r + (np.cos(b) / r) * f_b
    return f, f_x, f_y


def _rel_linf(a, b, sl):
    return float(np.max(np.abs(a[sl] - b[sl])) / max(np.max(np.abs(b[sl])), 1e-300))


def _interior():
    return (slice(6, -6), slice(2, -2))


def test_grad_xy_known_answer():
    """grad_xy recovers analytic f_x, f_y on the resolved interior."""
    grid = PolarGrid(n_r=700, n_beta=64, r_min=1e-2, r_max=30.0)
    f, fx_ex, fy_ex = _f_and_derivs(grid)
    fx, fy = grad_xy(f, grid)
    sl = _interior()
    ex = _rel_linf(fx, fx_ex, sl)
    ey = _rel_linf(fy, fy_ex, sl)
    assert ex < 5e-3 and ey < 5e-3, f"grad err fx {ex:.2e} fy {ey:.2e}"
    print(f"[ok] grad_xy known answer: f_x {ex:.2e}, f_y {ey:.2e}")


def test_grad_xy_convergence():
    """grad_xy error decreases under joint refinement (Spike-0 discipline)."""
    errs = []
    for s in (1, 2, 4):
        grid = PolarGrid(n_r=250 * s, n_beta=32 * s, r_min=1e-2, r_max=30.0)
        f, fx_ex, _ = _f_and_derivs(grid)
        fx, _ = grad_xy(f, grid)
        errs.append(_rel_linf(fx, fx_ex, _interior()))
    assert errs[1] < errs[0] and errs[2] < errs[1], f"not monotone: {errs}"
    rate = np.log2(errs[0] / errs[2]) / 2.0
    assert rate > 1.5, f"order {rate:.2f} below ~2nd"
    print(f"[ok] grad_xy convergence: errs {[f'{e:.2e}' for e in errs]}, order ~{rate:.2f}")


def test_odd_field_x_slope():
    """omega = wx0 * x * e^{-r^2} (odd in x) -> odd_field_x_slope recovers wx0. Convergent."""
    wx0_true = -2.1
    vals = []
    for n_r in (400, 800, 1600):
        grid = PolarGrid(n_r=n_r, n_beta=64, r_min=1e-3, r_max=20.0)
        omega = wx0_true * grid.X * np.exp(-(grid.R ** 2))
        vals.append(odd_field_x_slope(omega, grid))
    errs = [abs(v - wx0_true) / abs(wx0_true) for v in vals]
    assert errs[-1] < 3e-2, f"omega_x(0) err {errs[-1]:.2e}"
    assert errs[1] < errs[0] and errs[2] < errs[1], f"not converging: {errs}"
    print(f"[ok] odd_field_x_slope: {vals[-1]:.4f} (true {wx0_true}), errs {[f'{e:.1e}' for e in errs]}")


def test_c_l_ratio_bias_cancels():
    """c_l = 2 eta_x(0)/omega_x(0): the projection quadrature bias cancels in the ratio, so
    c_l is recovered MORE accurately than either slope alone (the design rationale)."""
    grid = PolarGrid(n_r=800, n_beta=64, r_min=1e-3, r_max=20.0)
    wx0, ex0 = -2.1, 3.4
    env = np.exp(-(grid.R ** 2))
    omega = wx0 * grid.X * env
    eta = ex0 * grid.X * env
    w_read = odd_field_x_slope(omega, grid)
    e_read = odd_field_x_slope(eta, grid)
    cl_true = 2 * ex0 / wx0
    cl_read = 2 * e_read / w_read
    err_ratio = abs(cl_read - cl_true) / abs(cl_true)
    err_slope = abs(w_read - wx0) / abs(wx0)
    assert err_ratio < err_slope, f"ratio {err_ratio:.2e} not better than slope {err_slope:.2e}"
    assert err_ratio < 5e-3, f"c_l err {err_ratio:.2e}"
    print(f"[ok] c_l ratio bias-cancels: c_l err {err_ratio:.2e} < slope err {err_slope:.2e}")


def test_modulation_assembly():
    """modulation(omega, eta, phi) assembles (2.11) correctly: manufactured omega, eta with
    known slopes and the Step-A phi* (u_x(0) = -2)."""
    grid = PolarGrid(n_r=800, n_beta=48, r_min=1e-3, r_max=30.0)
    wx0, ex0 = -2.1, 3.4
    env = np.exp(-(grid.R ** 2))
    omega = wx0 * grid.X * env
    eta = ex0 * grid.X * env
    phi = grid.R ** 2 * np.exp(-grid.R) * np.sin(2 * grid.B)  # Step-A phi*, u_x(0) = -2
    c_l, c_omega, c_theta, reads = modulation(omega, eta, phi, grid)
    cl_true = 2 * ex0 / wx0
    assert abs(c_l - cl_true) / abs(cl_true) < 5e-3, f"c_l {c_l:.4f} vs {cl_true:.4f}"
    assert abs(reads["u_x0"] - (-2.0)) < 1e-2, f"u_x(0) {reads['u_x0']:.4f}"
    assert abs(c_omega - (0.5 * c_l + reads["u_x0"])) < 1e-12
    assert abs(c_theta - (c_l + 2 * c_omega)) < 1e-12
    print(f"[ok] modulation: c_l {c_l:.4f} (true {cl_true:.4f}), c_omega {c_omega:.4f}, "
          f"c_theta {c_theta:.4f}, u_x0 {reads['u_x0']:.4f}")


def test_rhs_wiring():
    """The assembled RHS equals a term-by-term re-assembly from the separately-validated
    sub-operators (transport, grad_xy, modulation): locks the (2.10)/(2.28) formula as
    written -- signs, coefficients, and which field enters each reaction term."""
    grid = PolarGrid(n_r=200, n_beta=32, r_min=1e-2, r_max=20.0)
    om, et, xi = _seed_fields(grid)
    solver = RescaledBoussinesq(grid)
    Ro, Re, Rx, info = solver.rhs(om, et, xi)
    u, v, phi, u_x, u_y, v_x = solver.velocity_and_grads(om)
    c_l, c_om, c_th, reads = modulation(om, et, phi, grid)
    Ro2 = -transport(om, u, v, grid, c_l) + et + c_om * om
    Re2 = -transport(et, u, v, grid, c_l) + (2 * c_om - u_x) * et - v_x * xi
    Rx2 = -transport(xi, u, v, grid, c_l) + (2 * c_om + u_x) * xi - u_y * et
    assert np.allclose(Ro, Ro2) and np.allclose(Re, Re2) and np.allclose(Rx, Rx2)
    assert abs(info["c_l"] - c_l) < 1e-12
    print(f"[ok] RHS wiring matches term-by-term re-assembly (c_l={c_l:.4f}, c_om={c_om:.4f})")


def test_integrator_runs_stably():
    """End-to-end smoke test: the assembled machine steps SSPRK3 without blowup and yields
    finite c_l, c_omega and finite fields. NOT the gate -- Step C relaxes to the profile with
    a pre-committed predicate; this only certifies the assembly runs."""
    grid = PolarGrid(n_r=200, n_beta=32, r_min=1e-3, r_max=1e3)
    om0, et0, xi0 = _seed_fields(grid)
    solver = RescaledBoussinesq(grid)
    res = solver.run(om0, et0, xi0, dt_frac=0.25, max_steps=60)
    assert np.isfinite(res["residual"]), "residual went non-finite"
    assert np.isfinite(res["c_l"]) and np.isfinite(res["c_omega"]), "modulation non-finite"
    assert np.all(np.isfinite(res["omega"])) and np.all(np.isfinite(res["eta"]))
    assert np.all(np.isfinite(res["xi"]))
    print(f"[ok] integrator stable {res['steps']} steps: c_l={res['c_l']:+.4f}, "
          f"c_omega={res['c_omega']:+.4f}, res={res['residual']:.2e}")


def test_renorm_pins_gauge():
    """renorm=True discretely enforces (2.12): it holds c_l = 2 eta_x(0)/omega_x(0) near its
    initial value, where without it the near-origin truncation slip makes c_l drift (diagnosed
    in experiments/diagnose_stepC_drift.py). Assert the drift is materially smaller with renorm."""
    grid = PolarGrid(n_r=200, n_beta=40, r_min=1e-3, r_max=1e4)
    om0, et0, xi0 = _seed_fields(grid, a=1.0, b=1.5, c=0.0)  # c_l ~ 2*1.5/1.0 = 3
    solver = RescaledBoussinesq(grid)
    cl0 = odd_field_x_slope(et0, grid) / odd_field_x_slope(om0, grid) * 2.0
    r_off = solver.run(om0, et0, xi0, dt_frac=0.25, max_steps=250, renorm=False)
    r_on = solver.run(om0, et0, xi0, dt_frac=0.25, max_steps=250, renorm=True)
    drift_off = abs(r_off["c_l"] - cl0)
    drift_on = abs(r_on["c_l"] - cl0)
    assert drift_on < 0.5 * drift_off, f"renorm did not curb drift: on {drift_on:.3f} off {drift_off:.3f}"
    assert drift_on < 0.05 * abs(cl0), f"renorm c_l drift too large: {drift_on:.3f}"
    print(f"[ok] renorm pins c_l: drift {drift_on:.4f} (renorm) vs {drift_off:.4f} (off), c_l0={cl0:.3f}")


if __name__ == "__main__":
    test_grad_xy_known_answer()
    test_grad_xy_convergence()
    test_odd_field_x_slope()
    test_c_l_ratio_bias_cancels()
    test_modulation_assembly()
    test_rhs_wiring()
    test_integrator_runs_stably()
    test_renorm_pins_gauge()
    print("\nALL BOUSSINESQ-RESCALED (STEP B, PIECES 2-4 + RENORM) TESTS PASSED")
