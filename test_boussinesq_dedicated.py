"""Dedicated unit tests for solver/boussinesq.py (leg 66, Route-QF).

`capabilities.py` recorded this module as having "no dedicated test file --
exercised through test_solver_boussinesq.py". Leg 66's coverage audit
(writeup/novelty/leg_66.md) found ten test files import it, but every
assertion in all of them lands on a `BoussinesqResult` field after a full
integration, or on `parity_residual` of a solver output. The module's own
pieces -- the parity projectors as PROJECTORS, `_reflect` as an involution,
the argument-validation branches, the `under_resolved` guards, the
`BoussinesqResult` contract -- are asked nothing directly.

This file asks them directly, against hand-computed values.

Test convention (repo-wide): self-running script, no pytest.
    .venv/bin/python test_boussinesq_dedicated.py

CONTRAST WITH THE 1D MODULE (leg 66's finding): this module's spectral
derivative is correct on ODD grids as well as even ones -- see
check_derivative_odd_n_is_correct_here. The defect leg 66 found was specific
to solver/spectral_utils.derivative_hat, and has since been fixed (Leg 0,
bench/fix-derivative-hat-odd-n); this contrast check is what localized it to
the 1D helper and is kept as the regression guard for the 2D path.
"""

import numpy as np

from solver.boussinesq import (
    TWO_PI,
    BoussinesqResult,
    _reflect,
    dealias_mask2d,
    grid2d,
    parity_residual,
    project_even_odd,
    project_odd_odd,
    solve_boussinesq,
    velocity_from_vorticity,
    wavenumbers2d,
)

TOL = 1e-12


def _ddx(f):
    n = f.shape[0]
    KX, KY, _, _ = wavenumbers2d(n)
    return np.fft.ifft2(1j * KX * np.fft.fft2(f)).real


def _ddy(f):
    n = f.shape[0]
    KX, KY, _, _ = wavenumbers2d(n)
    return np.fft.ifft2(1j * KY * np.fft.fft2(f)).real


# --- grid2d / wavenumbers2d / dealias_mask2d -----------------------------


def check_grid2d_indexing():
    """indexing='ij': axis 0 is x, axis 1 is y. Getting this backwards would
    transpose every field in Phase 1 silently (the Hou-Luo geometry is NOT
    symmetric in x and y, so it matters)."""
    out = {}
    n = 16
    X, Y = grid2d(n)
    assert X.shape == (n, n) and Y.shape == (n, n)
    # X varies along axis 0 only, Y along axis 1 only
    out["X_const_along_axis1"] = float(np.max(np.abs(np.diff(X, axis=1))))
    out["Y_const_along_axis0"] = float(np.max(np.abs(np.diff(Y, axis=0))))
    assert out["X_const_along_axis1"] == 0.0, out
    assert out["Y_const_along_axis0"] == 0.0, out
    out["X_spacing_err"] = float(np.max(np.abs(np.diff(X, axis=0) - TWO_PI / n)))
    assert out["X_spacing_err"] < TOL, out
    assert X[0, 0] == 0.0 and Y[0, 0] == 0.0
    # ...and the derivative operators agree with that convention
    f = np.sin(X)
    out["ddx_of_sinX"] = float(np.max(np.abs(_ddx(f) - np.cos(X))))
    out["ddy_of_sinX"] = float(np.max(np.abs(_ddy(f))))
    assert out["ddx_of_sinX"] < TOL and out["ddy_of_sinX"] < TOL, out
    return out


def check_wavenumbers2d():
    """KX, KY are integer meshes; Ksq = KX^2+KY^2; inv_Ksq is its pseudo-inverse
    with an exact zero at the mean mode (the Biot-Savart regularization)."""
    out = {}
    for n in (8, 16, 17, 32):
        KX, KY, Ksq, inv = wavenumbers2d(n)
        for M in (KX, KY, Ksq, inv):
            assert M.shape == (n, n), n
        out[f"n{n}_kx_integrality"] = float(np.max(np.abs(KX - np.round(KX))))
        assert out[f"n{n}_kx_integrality"] == 0.0, n
        out[f"n{n}_ksq_err"] = float(np.max(np.abs(Ksq - (KX**2 + KY**2))))
        assert out[f"n{n}_ksq_err"] == 0.0, n
        assert inv[0, 0] == 0.0, n  # the mean mode, explicitly zeroed
        nz = Ksq > 0
        out[f"n{n}_pseudoinv_err"] = float(np.max(np.abs(inv[nz] * Ksq[nz] - 1.0)))
        assert out[f"n{n}_pseudoinv_err"] < 1e-15, n
        assert float(np.min(inv)) >= 0.0, n
        # KX is constant along axis 1, matching grid2d's ij convention
        assert float(np.max(np.abs(np.diff(KX, axis=1)))) == 0.0, n
    return out


def check_dealias_mask2d():
    """Square 2/3 cut: keep |kx| <= n/3 AND |ky| <= n/3, counted exactly."""
    out = {}
    for n in (16, 32, 48, 64, 96):
        mask = dealias_mask2d(n)
        KX, KY, _, _ = wavenumbers2d(n)
        keep1 = int(np.sum(np.abs(np.fft.fftfreq(n, d=1.0 / n)) <= n / 3.0))
        out[f"n{n}_kept"] = int(mask.sum())
        assert int(mask.sum()) == keep1 * keep1, (n, int(mask.sum()), keep1**2)
        assert bool(mask[0, 0]), n  # the mean mode is always kept
        # it is a product mask (square), not a disc
        assert np.array_equal(mask, mask.T), n
        kept_kx = np.abs(KX[mask])
        out[f"n{n}_kx_hi"] = float(np.max(kept_kx))
        assert out[f"n{n}_kx_hi"] <= n / 3.0, n
        assert out[f"n{n}_kx_hi"] + 1 > n / 3.0, n
    # n = 96: the cut 32 is attained and must be RETAINED (<=, not <)
    m = dealias_mask2d(96)
    KX, KY, _, _ = wavenumbers2d(96)
    assert bool(m[(KX == 32) & (KY == 0)][0]), "kx = n/3 must be retained"
    assert not bool(m[(KX == 33) & (KY == 0)][0])
    return out


def check_derivative_odd_n_is_correct_here():
    """The 2D spectral derivative is exact at ODD n too.

    Recorded deliberately: solver/spectral_utils.derivative_hat was NOT (leg
    66's finding -- it unconditionally zeroed the last rfft coefficient,
    which is the Nyquist mode only when n is even; fixed by Leg 0). This
    module builds i*KX from a full fft2 and has no such special case, so it
    was clean throughout. Measured relative sup error at n = 17, 33 on the
    top mode: ~6e-15 and ~7e-15, against 1.000 for the unfixed 1D helper.
    """
    out = {}
    for n in (16, 17, 32, 33):
        X, Y = grid2d(n)
        kt = (n - 1) // 2 if n % 2 else n // 2 - 1
        f = np.sin(kt * X) * np.cos(Y)
        want_x = kt * np.cos(kt * X) * np.cos(Y)
        want_y = -np.sin(kt * X) * np.sin(Y)
        ex = float(np.max(np.abs(_ddx(f) - want_x))) / float(np.max(np.abs(want_x)))
        ey = float(np.max(np.abs(_ddy(f) - want_y))) / float(np.max(np.abs(want_y)))
        out[f"n{n}_ddx"] = ex
        out[f"n{n}_ddy"] = ey
        assert ex < 1e-12, (n, ex)
        assert ey < 1e-12, (n, ey)
    return out


# --- velocity_from_vorticity --------------------------------------------


def check_biot_savart_hand_values():
    """u = (-psi_y, psi_x), Lap psi = w, on modes whose psi is hand-known.

    w = sin(x)sin(y)  ->  psi = -w/2  ->  u = (1/2)sin(x)cos(y),
                                          v = -(1/2)cos(x)sin(y).
    Checked as an operator identity, not through a solver step.
    """
    out = {}
    n = 32
    X, Y = grid2d(n)
    KX, KY, Ksq, inv = wavenumbers2d(n)
    cases = [
        ("sinx_siny", np.sin(X) * np.sin(Y),
         0.5 * np.sin(X) * np.cos(Y), -0.5 * np.cos(X) * np.sin(Y)),
        # w = sin(2x): psi = -w/4, u = 0, v = -(1/2)cos(2x)
        ("sin2x", np.sin(2 * X), np.zeros((n, n)), -0.5 * np.cos(2 * X)),
        # w = cos(3y): psi = -w/9, u = -(1/3)sin(3y), v = 0
        ("cos3y", np.cos(3 * Y), -(1.0 / 3.0) * np.sin(3 * Y), np.zeros((n, n))),
    ]
    for label, w, u_ex, v_ex in cases:
        u, v = velocity_from_vorticity(np.fft.fft2(w), KX, KY, inv)
        scale = max(float(np.max(np.abs(u_ex))), float(np.max(np.abs(v_ex))))
        out[f"{label}_u"] = float(np.max(np.abs(u - u_ex))) / scale
        out[f"{label}_v"] = float(np.max(np.abs(v - v_ex))) / scale
        assert out[f"{label}_u"] < 1e-13, (label, out)
        assert out[f"{label}_v"] < 1e-13, (label, out)
    return out


def check_biot_savart_invariants():
    """The recovered velocity is divergence-free, zero-mean, and inverts the
    curl: v_x - u_y = w for every zero-mean w."""
    out = {}
    n = 32
    KX, KY, Ksq, inv = wavenumbers2d(n)
    rng = np.random.default_rng(66)
    w = rng.standard_normal((n, n))
    w -= w.mean()
    w = np.fft.ifft2(np.fft.fft2(w) * dealias_mask2d(n)).real
    u, v = velocity_from_vorticity(np.fft.fft2(w), KX, KY, inv)
    scale = float(np.max(np.abs(w)))
    out["div_u"] = float(np.max(np.abs(_ddx(u) + _ddy(v)))) / scale
    assert out["div_u"] < 1e-12, out
    out["curl_u_minus_w"] = float(np.max(np.abs((_ddx(v) - _ddy(u)) - w))) / scale
    assert out["curl_u_minus_w"] < 1e-12, out
    out["u_mean"] = abs(float(np.mean(u))) / scale
    out["v_mean"] = abs(float(np.mean(v))) / scale
    assert out["u_mean"] < 1e-14 and out["v_mean"] < 1e-14, out

    # a constant vorticity field carries NO velocity (the inv_Ksq[0,0] = 0
    # branch); it is the one input for which Biot-Savart has no solution.
    u0, v0 = velocity_from_vorticity(np.fft.fft2(np.full((n, n), 3.0)), KX, KY, inv)
    out["const_w_u_max"] = float(np.max(np.abs(u0)))
    out["const_w_v_max"] = float(np.max(np.abs(v0)))
    assert out["const_w_u_max"] == 0.0 and out["const_w_v_max"] == 0.0, out

    # linearity
    w2 = np.fft.ifft2(np.fft.fft2(rng.standard_normal((n, n))) * dealias_mask2d(n)).real
    ua, va = velocity_from_vorticity(np.fft.fft2(w + 2.0 * w2), KX, KY, inv)
    ub, vb = velocity_from_vorticity(np.fft.fft2(w2), KX, KY, inv)
    out["linearity"] = float(np.max(np.abs(ua - (u + 2.0 * ub)))) / scale
    assert out["linearity"] < 1e-12, out
    return out


# --- the parity machinery -----------------------------------------------


def check_reflect_involution():
    """_reflect is the map x -> -x (mod 2pi) along one axis: an involution
    that fixes cos and negates sin. Named by zero existing tests."""
    out = {}
    n = 16
    X, Y = grid2d(n)
    rng = np.random.default_rng(3)
    f = rng.standard_normal((n, n))
    for axis in (0, 1):
        out[f"involution_ax{axis}"] = float(
            np.max(np.abs(_reflect(_reflect(f, axis), axis) - f))
        )
        assert out[f"involution_ax{axis}"] == 0.0, out
    out["fixes_cosx"] = float(np.max(np.abs(_reflect(np.cos(X), 0) - np.cos(X))))
    out["negates_sinx"] = float(np.max(np.abs(_reflect(np.sin(X), 0) + np.sin(X))))
    out["fixes_cosy"] = float(np.max(np.abs(_reflect(np.cos(Y), 1) - np.cos(Y))))
    out["negates_siny"] = float(np.max(np.abs(_reflect(np.sin(Y), 1) + np.sin(Y))))
    for key in ("fixes_cosx", "negates_sinx", "fixes_cosy", "negates_siny"):
        assert out[key] < 1e-14, (key, out)
    # the two reflections commute
    out["commute"] = float(np.max(np.abs(
        _reflect(_reflect(f, 0), 1) - _reflect(_reflect(f, 1), 0)
    )))
    assert out["commute"] == 0.0, out
    # x = 0 is fixed by the axis-0 reflection (index 0 maps to itself)
    assert np.array_equal(_reflect(f, 0)[0], f[0])
    return out


def check_parity_projectors():
    """project_odd_odd / project_even_odd are genuine orthogonal projectors.

    `project_even_odd` is named by ZERO existing test files, and it is what
    holds theta in the Hou-Luo wall subspace on every Gate-1b run.
    """
    out = {}
    n = 32
    rng = np.random.default_rng(1966)
    f = rng.standard_normal((n, n))
    poo, peo = project_odd_odd(f), project_even_odd(f)

    # idempotent
    out["oo_idempotent"] = float(np.max(np.abs(project_odd_odd(poo) - poo)))
    out["eo_idempotent"] = float(np.max(np.abs(project_even_odd(peo) - peo)))
    assert out["oo_idempotent"] < 1e-14 and out["eo_idempotent"] < 1e-14, out
    # mutually annihilating (the two subspaces intersect trivially)
    out["oo_of_eo"] = float(np.max(np.abs(project_odd_odd(peo))))
    out["eo_of_oo"] = float(np.max(np.abs(project_even_odd(poo))))
    assert out["oo_of_eo"] < 1e-14 and out["eo_of_oo"] < 1e-14, out
    # orthogonal in L2
    out["l2_orthogonality"] = abs(float(np.sum(poo * peo))) / float(np.sum(f * f))
    assert out["l2_orthogonality"] < 1e-14, out
    # linear, and norm-reducing
    g = rng.standard_normal((n, n))
    out["linearity"] = float(np.max(np.abs(
        project_odd_odd(f + 2.5 * g) - (poo + 2.5 * project_odd_odd(g))
    )))
    assert out["linearity"] < 1e-13, out
    assert float(np.sum(poo * poo)) <= float(np.sum(f * f)) + 1e-10

    # exactness on basis functions: the projectors must FIX their own basis
    X, Y = grid2d(n)
    for j in (1, 3):
        for k in (1, 2):
            b_oo = np.sin(j * X) * np.sin(k * Y)
            b_eo = np.cos(j * X) * np.sin(k * Y)
            e1 = float(np.max(np.abs(project_odd_odd(b_oo) - b_oo)))
            e2 = float(np.max(np.abs(project_even_odd(b_eo) - b_eo)))
            assert e1 < 1e-14 and e2 < 1e-14, (j, k, e1, e2)
            # ...and annihilate the other one
            assert float(np.max(np.abs(project_odd_odd(b_eo)))) < 1e-14, (j, k)
            assert float(np.max(np.abs(project_even_odd(b_oo)))) < 1e-14, (j, k)
    out["basis_checks"] = 4
    return out


def check_parity_residual():
    """parity_residual is 0 inside the subspace, O(1) outside, 0 on zero data.

    The zero-field branch (`scale == 0 -> return 0.0`) is a real code path
    that no existing test reaches, and it is the one that would otherwise
    divide by zero.
    """
    out = {}
    n = 32
    X, Y = grid2d(n)
    w_ok = np.sin(X) * np.sin(2 * Y) + 0.4 * np.sin(3 * X) * np.sin(Y)
    th_ok = np.cos(X) * np.sin(Y) - 0.2 * np.cos(2 * X) * np.sin(3 * Y)
    out["w_in_subspace"] = parity_residual(w_ok, "odd_odd")
    out["th_in_subspace"] = parity_residual(th_ok, "even_odd")
    assert out["w_in_subspace"] < 1e-14, out
    assert out["th_in_subspace"] < 1e-14, out
    # wrong parity is detected at O(1), not at O(eps)
    out["w_wrong_parity"] = parity_residual(th_ok, "odd_odd")
    out["th_wrong_parity"] = parity_residual(w_ok, "even_odd")
    assert out["w_wrong_parity"] > 0.5, out
    assert out["th_wrong_parity"] > 0.5, out
    # the zero field is (vacuously) in every subspace, without a 0/0
    out["zero_field_oo"] = parity_residual(np.zeros((n, n)), "odd_odd")
    out["zero_field_eo"] = parity_residual(np.zeros((n, n)), "even_odd")
    assert out["zero_field_oo"] == 0.0 and out["zero_field_eo"] == 0.0, out
    # scale-invariance: it is a RELATIVE residual
    rng = np.random.default_rng(9)
    f = rng.standard_normal((n, n))
    out["scale_invariance"] = abs(
        parity_residual(f, "odd_odd") - parity_residual(1e6 * f, "odd_odd")
    )
    assert out["scale_invariance"] < 1e-14, out
    return out


# --- solve_boussinesq: validation and stop-criterion branches ------------


def check_solve_rejects_bad_arguments():
    """Every documented ValueError branch actually raises.

    None of the three is reached by any existing test.
    """
    out = {}
    n = 16
    good = np.sin(grid2d(n)[0]) * np.sin(grid2d(n)[1])
    cases = {
        "unknown_symmetry": lambda: solve_boussinesq(
            good, good, symmetry="not_a_symmetry"),
        "zero_omega0": lambda: solve_boussinesq(np.zeros((n, n)), good),
        "non_square": lambda: solve_boussinesq(good, np.zeros((n, n + 1))),
        "rank1_theta": lambda: solve_boussinesq(good, np.zeros(n)),
    }
    for label, fn in cases.items():
        raised = False
        try:
            fn()
        except ValueError:
            raised = True
        except (IndexError, AttributeError) as exc:  # pragma: no cover
            raise AssertionError(f"{label}: wrong exception type {exc!r}")
        out[label] = 1.0 if raised else 0.0
        assert raised, f"{label} did not raise ValueError"
    return out


def check_result_contract():
    """BoussinesqResult's fields are self-consistent on every branch.

    The dataclass is named by zero existing tests, yet phase1_*.py and
    ga/fitness2d.py read these fields directly.
    """
    out = {}
    n = 32
    X, Y = grid2d(n)
    w0 = np.sin(X) * np.sin(Y)
    th0 = np.cos(X) * np.sin(Y)
    runs = {
        "no_blowup": solve_boussinesq(w0, th0, nu=0.1, kappa=0.1, t_max=0.3),
        "max_steps": solve_boussinesq(w0, th0, t_max=10.0, max_steps=5),
    }
    allowed = {"no_blowup", "blowup_candidate", "diverged",
               "max_steps_hit", "under_resolved"}
    for label, r in runs.items():
        assert isinstance(r, BoussinesqResult), label
        assert r.outcome in allowed, (label, r.outcome)
        assert len(r.times) == len(r.max_omega) == r.n_timesteps + 1, label
        assert r.times[0] == 0.0 and np.all(np.diff(r.times) > 0.0), label
        assert abs(r.times[-1] - r.t_final) < 1e-15, label
        assert r.omega_final.shape == (n, n), label
        assert r.theta_final.shape == (n, n), label
        assert np.isfinite(r.omega_final).all(), label
        assert np.isfinite(r.theta_final).all(), label
        assert r.conservation_drift == max(r.mean_drift, r.energy_balance_residual), label
        assert 0.0 <= r.max_tail_fraction <= 1.0, (label, r.max_tail_fraction)
        for key in ("nu", "kappa", "resolution_N", "t_max", "dt_max", "c1", "c2",
                    "amplification_factor", "max_steps", "buoyancy", "nonlinear"):
            assert key in r.params, (label, key)
        assert r.params["resolution_N"] == n, label
        out[f"{label}_outcome"] = r.outcome
    assert runs["max_steps"].outcome == "max_steps_hit"
    assert runs["max_steps"].n_timesteps == 5
    assert abs(runs["no_blowup"].t_final - 0.3) < 1e-12
    out["no_blowup_drift"] = runs["no_blowup"].conservation_drift
    return out


def check_pure_diffusion_exact():
    """nonlinear=False + buoyancy=False is the integrating factor ALONE.

    Both fields must decay by exactly exp(-nu k^2 t) / exp(-kappa k^2 t),
    independently, and independently of dt. No existing test switches BOTH
    hooks off, so this decoupled path is unexercised.
    """
    out = {}
    n = 32
    X, Y = grid2d(n)
    nu, kappa, t_end = 0.1, 0.03, 1.0
    for j, k in ((1, 1), (2, 3)):
        w0 = np.sin(j * X) * np.sin(k * Y)
        th0 = np.cos(j * X) * np.sin(k * Y)
        r = solve_boussinesq(w0, th0, nu=nu, kappa=kappa, t_max=t_end,
                             nonlinear=False, buoyancy=False, dt_max=1e-2)
        ksq = j * j + k * k
        w_want = np.exp(-nu * ksq * t_end) * w0
        th_want = np.exp(-kappa * ksq * t_end) * th0
        out[f"j{j}k{k}_w"] = float(np.max(np.abs(r.omega_final - w_want)))
        out[f"j{j}k{k}_th"] = float(np.max(np.abs(r.theta_final - th_want)))
        assert out[f"j{j}k{k}_w"] < 1e-13, (j, k, out)
        assert out[f"j{j}k{k}_th"] < 1e-13, (j, k, out)

    # exactness, not convergence: dt must not matter at all
    w0 = np.sin(X) * np.sin(Y)
    th0 = np.cos(X) * np.sin(Y)
    coarse = solve_boussinesq(w0, th0, nu=nu, kappa=kappa, t_max=t_end,
                              nonlinear=False, buoyancy=False, dt_max=5e-1)
    fine = solve_boussinesq(w0, th0, nu=nu, kappa=kappa, t_max=t_end,
                            nonlinear=False, buoyancy=False, dt_max=1e-3)
    out["dt_independence"] = float(
        np.max(np.abs(coarse.omega_final - fine.omega_final))
    )
    assert out["dt_independence"] < 1e-14, out
    out["step_ratio"] = fine.n_timesteps / coarse.n_timesteps
    assert out["step_ratio"] > 100, out
    return out


def check_buoyancy_switch():
    """buoyancy=False really removes th_x, and theta then only advects.

    With nonlinear=False and buoyancy=False and no dissipation, NOTHING may
    move at all -- a null test that catches a term leaking in.
    """
    out = {}
    n = 32
    X, Y = grid2d(n)
    w0 = np.sin(X) * np.sin(Y)
    th0 = np.cos(X) * np.sin(Y)
    frozen = solve_boussinesq(w0, th0, t_max=1.0, nonlinear=False,
                              buoyancy=False, dt_max=1e-2)
    out["frozen_w_change"] = float(np.max(np.abs(frozen.omega_final - w0)))
    out["frozen_th_change"] = float(np.max(np.abs(frozen.theta_final - th0)))
    assert out["frozen_w_change"] < 1e-14, out
    assert out["frozen_th_change"] < 1e-14, out

    # switching buoyancy back on must move w by an O(1) amount
    forced = solve_boussinesq(w0, th0, t_max=1.0, nonlinear=False,
                              buoyancy=True, dt_max=1e-3)
    out["buoyancy_w_change"] = float(np.max(np.abs(forced.omega_final - w0)))
    assert out["buoyancy_w_change"] > 0.1, out
    # ...and theta must be untouched by it (buoyancy enters only the w equation)
    out["buoyancy_th_change"] = float(np.max(np.abs(forced.theta_final - th0)))
    assert out["buoyancy_th_change"] < 1e-14, out

    # short-time check against the exact linear solution w = w0 + t*th_x
    small = solve_boussinesq(w0, th0, t_max=1e-3, nonlinear=False,
                             buoyancy=True, dt_max=1e-5)
    want = w0 + 1e-3 * _ddx(th0)
    out["linear_growth_err"] = float(np.max(np.abs(small.omega_final - want)))
    assert out["linear_growth_err"] < 1e-12, out
    return out


def check_frozen_u_translation():
    """frozen_u = (cu, cv) with buoyancy off makes both fields pure translation.

    Checked on THETA, which test_solver_boussinesq.py's transport check does
    not track to the same tolerance, and at a velocity with both components
    nonzero (a diagonal translation), which no existing test uses.
    """
    out = {}
    n = 64
    X, Y = grid2d(n)
    w0 = np.sin(X) * np.sin(Y) + 0.3 * np.sin(2 * X) * np.cos(Y)
    th0 = np.cos(X) * np.sin(Y)
    cu, cv, t_end = 0.7, -0.4, 1.0
    r = solve_boussinesq(w0, th0, t_max=t_end, buoyancy=False,
                         frozen_u=(cu, cv), dt_max=1e-3)
    Xs, Ys = X - cu * t_end, Y - cv * t_end
    w_want = np.sin(Xs) * np.sin(Ys) + 0.3 * np.sin(2 * Xs) * np.cos(Ys)
    th_want = np.cos(Xs) * np.sin(Ys)
    out["w_rel_err"] = float(np.max(np.abs(r.omega_final - w_want))) / float(
        np.max(np.abs(w_want)))
    out["th_rel_err"] = float(np.max(np.abs(r.theta_final - th_want))) / float(
        np.max(np.abs(th_want)))
    assert out["w_rel_err"] < 1e-8, out
    assert out["th_rel_err"] < 1e-8, out
    # Translation preserves the sup norm. Compared against the sampled exact
    # solution, not against max|w0|: a shift by a non-grid-aligned distance
    # moves the continuous peak off the grid, which is a sampling effect of
    # size 5.2e-05 here and not a solver error.
    out["sup_norm_change"] = abs(
        float(np.max(np.abs(r.omega_final))) - float(np.max(np.abs(w_want)))
    ) / float(np.max(np.abs(w_want)))
    assert out["sup_norm_change"] < 1e-8, out
    out["grid_sampling_effect"] = abs(
        float(np.max(np.abs(w_want))) - float(np.max(np.abs(w0)))
    ) / float(np.max(np.abs(w0)))
    assert out["grid_sampling_effect"] < 1e-3, out
    return out


def check_under_resolved_guards():
    """tail_guard and drift_guard both produce outcome "under_resolved".

    Neither guard's firing path is exercised by any existing test; they are
    the Phase-1 resolution de-risk, so a guard that silently never fires
    would be worse than no guard.
    """
    out = {}
    n = 32
    X, Y = grid2d(n)
    w0 = np.sin(X) * np.sin(Y)
    th0 = np.cos(X) * np.sin(Y)

    # an impossible tail threshold fires immediately; an impossible-to-exceed
    # one never fires. Both directions, so the guard is not a constant.
    hot = solve_boussinesq(w0, th0, t_max=1.0, tail_guard=-1.0)
    cold = solve_boussinesq(w0, th0, t_max=0.2, tail_guard=2.0)
    out["tail_hot_outcome"] = hot.outcome
    out["tail_cold_outcome"] = cold.outcome
    assert hot.outcome == "under_resolved", hot.outcome
    assert hot.n_timesteps == 1, hot.n_timesteps
    assert cold.outcome == "no_blowup", cold.outcome

    hot_d = solve_boussinesq(w0, th0, t_max=1.0, drift_guard=-1.0)
    cold_d = solve_boussinesq(w0, th0, t_max=0.2, drift_guard=1.0)
    out["drift_hot_outcome"] = hot_d.outcome
    out["drift_cold_outcome"] = cold_d.outcome
    assert hot_d.outcome == "under_resolved", hot_d.outcome
    assert cold_d.outcome == "no_blowup", cold_d.outcome

    # max_tail_fraction is always reported, guard or no guard
    out["cold_tail_fraction"] = cold.max_tail_fraction
    assert 0.0 <= cold.max_tail_fraction <= 1.0, out
    # a single well-resolved mode puts essentially nothing near the cut
    assert cold.max_tail_fraction < 1e-3, out
    return out


def check_houluo_symmetry_is_preserved_and_enforced():
    """symmetry="houluo" projects the INITIAL data too, not just the steps.

    Feeding it data with the wrong parity must produce a run whose output is
    exactly in the subspace -- a contract no existing test states (the wall
    test starts from already-symmetric data).
    """
    out = {}
    n = 32
    X, Y = grid2d(n)
    rng = np.random.default_rng(66)
    dirty_w = np.sin(X) * np.sin(Y) + 0.3 * np.cos(X) * np.cos(Y)
    dirty_th = np.cos(X) * np.sin(Y) + 0.3 * np.sin(X) * np.cos(2 * Y)
    out["input_w_residual"] = parity_residual(dirty_w, "odd_odd")
    out["input_th_residual"] = parity_residual(dirty_th, "even_odd")
    assert out["input_w_residual"] > 0.1, out

    r = solve_boussinesq(dirty_w, dirty_th, nu=0.01, kappa=0.01,
                         t_max=0.5, symmetry="houluo", dt_max=1e-2)
    out["output_w_residual"] = parity_residual(r.omega_final, "odd_odd")
    out["output_th_residual"] = parity_residual(r.theta_final, "even_odd")
    assert out["output_w_residual"] < 1e-13, out
    assert out["output_th_residual"] < 1e-13, out

    # and the projection is idempotent as a run: starting from the projected
    # data gives the same trajectory
    clean = solve_boussinesq(project_odd_odd(dirty_w), project_even_odd(dirty_th),
                             nu=0.01, kappa=0.01, t_max=0.5,
                             symmetry="houluo", dt_max=1e-2)
    out["trajectory_agreement"] = float(
        np.max(np.abs(clean.omega_final - r.omega_final))
    ) / float(np.max(np.abs(r.omega_final)))
    assert out["trajectory_agreement"] < 1e-13, out
    return out


def check_mean_invariants():
    """int w and int th are conserved: no term touches the (0,0) mode."""
    out = {}
    n = 32
    X, Y = grid2d(n)
    w0 = 0.5 + np.sin(X) * np.sin(Y)
    th0 = 1.5 + np.cos(X) * np.sin(Y)
    r = solve_boussinesq(w0, th0, t_max=0.5, dt_max=1e-2)
    out["mean_drift"] = r.mean_drift
    assert r.mean_drift < 1e-12, out
    out["w_int_err"] = abs(float(np.mean(r.omega_final)) - float(np.mean(w0)))
    out["th_int_err"] = abs(float(np.mean(r.theta_final)) - float(np.mean(th0)))
    assert out["w_int_err"] < 1e-13, out
    assert out["th_int_err"] < 1e-13, out
    return out


CHECKS = [
    check_grid2d_indexing,
    check_wavenumbers2d,
    check_dealias_mask2d,
    check_derivative_odd_n_is_correct_here,
    check_biot_savart_hand_values,
    check_biot_savart_invariants,
    check_reflect_involution,
    check_parity_projectors,
    check_parity_residual,
    check_solve_rejects_bad_arguments,
    check_result_contract,
    check_pure_diffusion_exact,
    check_buoyancy_switch,
    check_frozen_u_translation,
    check_under_resolved_guards,
    check_houluo_symmetry_is_preserved_and_enforced,
    check_mean_invariants,
]


def test_grid2d_indexing():
    check_grid2d_indexing()


def test_wavenumbers2d():
    check_wavenumbers2d()


def test_dealias_mask2d():
    check_dealias_mask2d()


def test_derivative_odd_n_is_correct_here():
    check_derivative_odd_n_is_correct_here()


def test_biot_savart_hand_values():
    check_biot_savart_hand_values()


def test_biot_savart_invariants():
    check_biot_savart_invariants()


def test_reflect_involution():
    check_reflect_involution()


def test_parity_projectors():
    check_parity_projectors()


def test_parity_residual():
    check_parity_residual()


def test_solve_rejects_bad_arguments():
    check_solve_rejects_bad_arguments()


def test_result_contract():
    check_result_contract()


def test_pure_diffusion_exact():
    check_pure_diffusion_exact()


def test_buoyancy_switch():
    check_buoyancy_switch()


def test_frozen_u_translation():
    check_frozen_u_translation()


def test_under_resolved_guards():
    check_under_resolved_guards()


def test_houluo_symmetry_is_preserved_and_enforced():
    check_houluo_symmetry_is_preserved_and_enforced()


def test_mean_invariants():
    check_mean_invariants()


if __name__ == "__main__":
    for fn in CHECKS:
        metrics = fn()
        head = ", ".join(f"{k}={v:.3g}" if isinstance(v, float) else f"{k}={v}"
                         for k, v in list(metrics.items())[:4])
        print(f"PASS {fn.__name__}: {head}")
    print(f"\nall boussinesq dedicated checks passed ({len(CHECKS)} checks)")
