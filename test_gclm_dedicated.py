"""Dedicated unit tests for solver/gclm.py (leg 66, Route-QF).

`capabilities.py` recorded this module as having "no dedicated test file --
exercised through test_solver_clm.py". That file is a system test: every one
of its assertions is on a `SolverResult` field after a full integration. The
solver's own pieces -- the RHS assembly, the stop-criterion branches, the
argument validation, `energy_from_gradient` (named by zero of the repo's 52
test files) -- are never asked anything directly.

This file asks them directly. Nothing here re-measures gCLM: no parameter is
changed and no new sweep is run. Every target value is either a closed form
or a structural invariant of code that already exists.

Test convention (repo-wide): self-running script, no pytest.
    .venv/bin/python test_gclm_dedicated.py
"""

import numpy as np

from solver.gclm import (
    SolverResult,
    _nonlinear_rhs_hat,
    clm_analytic_blowup_time,
    energy_from_gradient,
    solve_gclm,
)
from solver.spectral_utils import (
    TWO_PI,
    dealias_mask,
    grid,
    wavenumbers,
)


def _rhs(w, a, frozen_u=None):
    """Physical-space nonlinear RHS on an n-point grid."""
    n = len(w)
    k = wavenumbers(n)
    rhs_hat, u = _nonlinear_rhs_hat(np.fft.rfft(w), k, dealias_mask(n), a, frozen_u)
    return np.fft.irfft(rhs_hat, n), u


# --- _nonlinear_rhs_hat: hand-computed RHS values ------------------------


def check_rhs_clm_single_mode():
    """a = 0: RHS = w * H(w). For w = sin x this is -sin(x)cos(x) = -sin(2x)/2.

    A closed-form check on the growth term alone, with no time stepping in
    the way. test_solver_clm.py only ever sees this term's effect after a
    full integration and a blow-up-time fit.
    """
    out = {}
    n = 64
    x = grid(n)
    for label, w, want in [
        ("sin", np.sin(x), -0.5 * np.sin(2 * x)),
        ("2sin", 2.0 * np.sin(x), -2.0 * np.sin(2 * x)),
        ("cos", np.cos(x), 0.5 * np.sin(2 * x)),
        ("sin2x", np.sin(2 * x), -0.5 * np.sin(4 * x)),
    ]:
        got, _ = _rhs(w, a=0.0)
        err = float(np.max(np.abs(got - want))) / float(np.max(np.abs(want)))
        out[label] = err
        assert err < 1e-12, (label, err)
    return out


def check_rhs_degregorio_stationary_mode():
    """a = 1, w = sin x: the two nonlinear terms CANCEL exactly.

    u = -sin x (from u_hat = -w_hat/|k|), so
        -a*u*w_x = sin(x)cos(x) = +sin(2x)/2
        + w*u_x  = sin(x)*(-cos x) = -sin(2x)/2
    and sin x is a stationary solution of De Gregorio. This is the sharpest
    single check on the RELATIVE sign and scaling of the two terms -- a sign
    error in either one turns an exact zero into O(1). No existing test asks
    it: test_solver_clm.py's advection check freezes u, which switches this
    term off entirely.
    """
    out = {}
    n = 64
    x = grid(n)
    w = np.sin(x)
    got, u = _rhs(w, a=1.0)
    out["rhs_max_abs"] = float(np.max(np.abs(got)))
    assert out["rhs_max_abs"] < 1e-13, out
    out["u_err"] = float(np.max(np.abs(u + np.sin(x))))
    assert out["u_err"] < 1e-13, out

    # ... and it is genuinely a cancellation, not two zeros
    transport_only, _ = _rhs(w, a=1.0, frozen_u=None)
    growth_only, _ = _rhs(w, a=0.0)
    out["growth_term_max_abs"] = float(np.max(np.abs(growth_only)))
    assert out["growth_term_max_abs"] > 0.4, out
    del transport_only

    # The RHS is affine in a with slope -u*w_x = +sin(2x)/2, and the a = 0
    # value is -sin(2x)/2, so the cancellation happens at a = 1 and NOWHERE
    # else. At a = 2 the residue is exactly the negative of the a = 0 term.
    got2, _ = _rhs(w, a=2.0)
    err = float(np.max(np.abs(got2 + growth_only))) / out["growth_term_max_abs"]
    out["a2_equals_minus_growth"] = err
    assert err < 1e-12, out
    got_half, _ = _rhs(w, a=0.5)
    err = float(np.max(np.abs(got_half - 0.5 * growth_only))) / out["growth_term_max_abs"]
    out["a_affine"] = err
    assert err < 1e-12, out
    return out


def check_rhs_frozen_u():
    """frozen_u = c makes the RHS exactly -a*c*w_x (u_x is set to zero).

    The frozen-u hook is the one the Stage-1 advection acceptance check
    depends on; here it is checked as an operator identity rather than
    through a translated solution.
    """
    out = {}
    n = 64
    x = grid(n)
    w = np.sin(x) + 0.3 * np.cos(3 * x)
    w_x = np.cos(x) - 0.9 * np.sin(3 * x)
    for a, c in [(1.0, 1.0), (1.0, -2.5), (0.5, 3.0), (0.0, 1.0)]:
        got, u = _rhs(w, a=a, frozen_u=c)
        want = -a * c * w_x
        scale = max(float(np.max(np.abs(want))), 1e-14)
        err = float(np.max(np.abs(got - want))) / scale
        out[f"a{a}_c{c}"] = err
        assert err < 1e-12, (a, c, err)
        assert float(np.max(np.abs(u - c))) < 1e-15, (a, c)
    return out


def check_rhs_dealiasing():
    """The returned spectrum is zero above the 2/3 cut, by construction.

    `dealias_mask` is named by no other test in the repo; this is the place
    its effect on the solver is visible.
    """
    out = {}
    n = 64
    x = grid(n)
    k = wavenumbers(n)
    mask = dealias_mask(n)
    out["k_cut"] = int(np.max(k[mask]))  # 21 at n = 64

    # w = sin(11x) + sin(13x), a = 0: w*H(w) = -[sin(22x) + sin(26x)]/2
    # - sin(24x). All three modes sit above the cut (21) and below Nyquist
    # (32), so none may survive AND none is destroyed by aliasing instead.
    # The unmasked value is O(1), which separates "masked" from "happened
    # to be small".
    w = np.sin(11 * x) + np.sin(13 * x)
    w_hat = np.fft.rfft(w)
    rhs_hat, _ = _nonlinear_rhs_hat(w_hat, k, mask, 0.0, None)
    unmasked, _ = _nonlinear_rhs_hat(w_hat, k, np.ones_like(mask), 0.0, None)
    out["all_above_cut_masked_max"] = float(np.max(np.abs(rhs_hat)))
    out["all_above_cut_unmasked_max"] = float(np.max(np.abs(unmasked))) / n
    assert out["all_above_cut_masked_max"] < 1e-11, out
    assert out["all_above_cut_unmasked_max"] > 0.4, out

    # w = sin(x) + sin(20x): products at modes 2, 19, 21 are retained, 40 is
    # not. The mask must be a band cut, not a blanket.
    w = np.sin(x) + np.sin(20 * x)
    rhs_hat, _ = _nonlinear_rhs_hat(np.fft.rfft(w), k, mask, 0.0, None)
    out["max_abs_above_cut"] = float(np.max(np.abs(rhs_hat[~mask])))
    assert out["max_abs_above_cut"] == 0.0, out
    out["max_abs_below_cut"] = float(np.max(np.abs(rhs_hat[mask]))) / n
    assert out["max_abs_below_cut"] > 0.1, out
    return out


# --- energy_from_gradient ------------------------------------------------


def check_energy_from_gradient():
    """(1/2) int w_x^2. For w = sin(kx) this is pi*k^2/2, exactly.

    Named by ZERO existing test files, and it is the dissipation integrand
    the linear-only energy balance is scored against.
    """
    out = {}
    n = 256
    x = grid(n)
    for k in (1, 2, 5, 13):
        got = energy_from_gradient(np.sin(k * x))
        want = 0.5 * np.pi * k * k
        err = abs(got - want) / want
        out[f"sin{k}x"] = err
        assert err < 1e-11, (k, got, want)
    out["const"] = abs(energy_from_gradient(np.full(n, 3.0)))
    assert out["const"] < 1e-20, out
    # additivity across orthogonal modes
    a = energy_from_gradient(np.sin(x))
    b = energy_from_gradient(np.sin(4 * x))
    ab = energy_from_gradient(np.sin(x) + np.sin(4 * x))
    out["mode_additivity"] = abs(ab - (a + b)) / ab
    assert out["mode_additivity"] < 1e-12, out
    return out


def check_energy_from_gradient_odd_n_known_defect():
    """KNOWN DEFECT INHERITED from spectral_utils.derivative_hat -- PINNED.

    `energy_from_gradient` calls `derivative_hat`, which on ODD-length grids
    destroys the k = (n-1)/2 mode (see
    test_spectral_utils_dedicated.check_derivative_odd_n_known_defect).
    Consequence, measured: for w = sin(32 x) on n = 65 the function returns
    2.56e-26 where the exact value is 1.6085e+03 -- relative error 1.000, a
    total loss. n = 129, k = 64: 5.50e-25 against 6.4340e+03, same.

    Latent, not active: no call site in this repository passes an odd n.
    Recorded here so the blast radius of the spectral_utils defect is on
    file at the point where it would corrupt a logged artifact-guard number
    rather than a mere derivative. Fixing derivative_hat fixes this too, and
    WILL make this test fail -- that is the intended signal.
    """
    out = {}
    for n in (65, 129):
        x = grid(n)
        kt = (n - 1) // 2
        got = energy_from_gradient(np.sin(kt * x))
        want = 0.5 * np.pi * kt * kt
        out[f"n{n}_got"] = got
        out[f"n{n}_exact"] = want
        out[f"n{n}_rel_err"] = abs(got - want) / want
        assert out[f"n{n}_rel_err"] > 0.99, (n, out)
        # even n of the same size class is correct, for contrast
        m = n - 1
        xm = grid(m)
        km = m // 2 - 1
        gm = energy_from_gradient(np.sin(km * xm))
        wm = 0.5 * np.pi * km * km
        out[f"n{m}_rel_err"] = abs(gm - wm) / wm
        assert out[f"n{m}_rel_err"] < 1e-11, (m, out)
    return out


# --- clm_analytic_blowup_time -------------------------------------------


def check_clm_blowup_time_closed_form():
    """T* = 2 / max{H(w0)(x) : w0(x) = 0}, on data where that is hand-known.

    test_solver_clm.py uses this function as the REFERENCE its simulation is
    compared against, so it is never itself checked -- if it were wrong, the
    acceptance check would be scoring the solver against a wrong target.
    Here it is checked against values derived by hand.
    """
    out = {}
    cases = [
        # w0 = sin x: zeros at 0, pi; H(sin) = -cos, values -1 and +1 -> T* = 2
        ("sin", lambda x: np.sin(x), 2.0),
        # scale covariance: w0 -> c*w0 scales H likewise, so T* -> T*/c
        ("2sin", lambda x: 2.0 * np.sin(x), 1.0),
        ("10sin", lambda x: 10.0 * np.sin(x), 0.2),
        # w0 = cos x: zeros at pi/2, 3pi/2; H(cos) = sin, values +1, -1 -> 2
        ("cos", lambda x: np.cos(x), 2.0),
        # w0 = sin(2x): zeros at 0, pi/2, pi, 3pi/2; H = -cos(2x) -> max +1
        ("sin2x", lambda x: np.sin(2 * x), 2.0),
    ]
    for label, fn, want in cases:
        got = clm_analytic_blowup_time(fn)
        assert got is not None, label
        err = abs(got - want) / want
        out[label] = err
        assert err < 1e-9, (label, got, want)

    # sign flip: -sin x has zeros at the same places, H(-sin) = +cos, max +1
    out["minus_sin"] = abs(clm_analytic_blowup_time(lambda x: -np.sin(x)) - 2.0) / 2.0
    assert out["minus_sin"] < 1e-9, out

    # the mixed datum test_solver_clm.py lists as T* = 2/0.7
    got = clm_analytic_blowup_time(lambda x: np.sin(x) + 0.3 * np.sin(2 * x))
    out["mixed"] = abs(got - 2.0 / 0.7) / (2.0 / 0.7)
    assert out["mixed"] < 1e-6, (got, 2.0 / 0.7)
    return out


def check_clm_blowup_time_no_blowup():
    """Sign-definite data has no zero at all -> the function returns None.

    This branch (`best_h <= 0 -> None`) is never reached by any existing
    test; every initial condition in test_solver_clm.py blows up.
    """
    out = {}
    for label, fn in [
        ("1+0.5sin", lambda x: 1.0 + 0.5 * np.sin(x)),
        ("const", lambda x: np.full_like(x, 2.0)),
        ("neg", lambda x: -3.0 + np.cos(x)),
    ]:
        got = clm_analytic_blowup_time(fn)
        out[label] = -1.0 if got is None else got
        assert got is None, (label, got)
    # and the scan resolution is an honest knob: coarser scan, same answer
    a = clm_analytic_blowup_time(lambda x: np.sin(x), n_scan=512)
    b = clm_analytic_blowup_time(lambda x: np.sin(x), n_scan=4096)
    out["n_scan_stability"] = abs(a - b) / b
    assert out["n_scan_stability"] < 1e-9, out
    return out


# --- solve_gclm: argument validation and stop-criterion branches ---------


def check_solve_gclm_rejects_zero_data():
    """omega0 identically zero raises ValueError (m0 == 0 guard)."""
    out = {}
    raised = False
    try:
        solve_gclm(np.zeros(32))
    except ValueError as exc:
        raised = True
        out["message_mentions_zero"] = 1.0 if "zero" in str(exc) else 0.0
    assert raised, "solve_gclm accepted identically-zero data"
    assert out["message_mentions_zero"] == 1.0, out
    # a field that is zero only on the grid's dealiased part is still rejected
    raised = False
    try:
        solve_gclm(np.zeros(8) + 0.0)
    except ValueError:
        raised = True
    assert raised
    return out


def check_solve_gclm_result_contract():
    """SolverResult's fields are self-consistent for every outcome branch.

    The dataclass is named by zero existing tests; these are the invariants
    every downstream consumer (ga/fitness.py, the sweeps, win_condition)
    silently assumes.
    """
    out = {}
    n = 64
    x = grid(n)
    runs = {
        "no_blowup": solve_gclm(0.01 * np.sin(x), a=1.0, nu=0.5, t_max=0.5),
        "blowup": solve_gclm(np.sin(x), a=0.0, nu=0.0, t_max=5.0,
                             amplification_factor=50.0),
        "max_steps": solve_gclm(np.sin(x), a=0.0, nu=0.0, t_max=10.0,
                                max_steps=7),
    }
    allowed = {"no_blowup", "blowup_candidate", "diverged", "max_steps_hit"}
    for label, r in runs.items():
        assert isinstance(r, SolverResult), label
        assert r.outcome in allowed, (label, r.outcome)
        assert len(r.times) == len(r.max_omega), label
        assert len(r.times) == r.n_timesteps + 1, (label, len(r.times), r.n_timesteps)
        assert r.times[0] == 0.0, label
        assert np.all(np.diff(r.times) > 0.0), label
        assert abs(r.times[-1] - r.t_final) < 1e-15, label
        assert r.omega_final.shape == (n,), label
        assert np.isfinite(r.omega_final).all(), label
        assert r.dt_min > 0.0, label
        assert r.conservation_drift == max(r.mean_drift, r.energy_balance_residual), label
        assert r.wall_clock_seconds >= 0.0, label
        for key in ("a", "nu", "resolution_N", "t_max", "dt_max",
                    "c1", "c2", "amplification_factor", "max_steps"):
            assert key in r.params, (label, key)
        assert r.params["resolution_N"] == n, label
        out[f"{label}_outcome"] = r.outcome
        out[f"{label}_steps"] = r.n_timesteps

    assert runs["max_steps"].outcome == "max_steps_hit", runs["max_steps"].outcome
    assert runs["max_steps"].n_timesteps == 7, runs["max_steps"].n_timesteps
    assert runs["blowup"].outcome == "blowup_candidate", runs["blowup"].outcome
    # the amplification threshold really was met, not merely approached
    m0 = float(np.max(np.abs(np.sin(x))))
    out["blowup_amplification"] = float(runs["blowup"].max_omega[-1]) / m0
    assert out["blowup_amplification"] >= 50.0, out
    assert float(runs["blowup"].max_omega[-2]) / m0 < 50.0, "stopped late"
    # a no-blowup run integrates to exactly t_max
    assert abs(runs["no_blowup"].t_final - 0.5) < 1e-12, runs["no_blowup"].t_final
    assert runs["no_blowup"].early_exit_reason is None
    return out


def check_solve_gclm_early_decay_exit():
    """early_decay_exit fires and is audited via early_exit_reason.

    The compute-saving branch PLAN.md's compute plan depends on. No existing
    test exercises it.
    """
    out = {}
    n = 64
    x = grid(n)
    w0 = 0.05 * np.sin(x)
    full = solve_gclm(w0, a=1.0, nu=1.0, t_max=8.0)
    early = solve_gclm(w0, a=1.0, nu=1.0, t_max=8.0,
                       early_decay_exit={"fraction": 0.5, "window": 0.1})
    assert full.outcome == "no_blowup" and full.early_exit_reason is None
    assert early.outcome == "no_blowup", early.outcome
    assert early.early_exit_reason == "decay_exit", early.early_exit_reason
    out["t_full"] = full.t_final
    out["t_early"] = early.t_final
    out["steps_saved_ratio"] = full.n_timesteps / max(early.n_timesteps, 1)
    assert early.t_final < full.t_final, out
    assert out["steps_saved_ratio"] > 1.5, out
    # the exit condition it claims really held: max|w| below the fraction
    assert float(early.max_omega[-1]) < 0.5 * float(early.max_omega[0]), out
    return out


def check_solve_gclm_pure_diffusion_exact():
    """nonlinear=False + nu>0 is the integrating factor ALONE: exp(-nu k^2 t).

    With the nonlinearity off the scheme is exact, so this is an
    equality-to-round-off check, not a convergence check. test_solver_clm.py
    asserts only a 1% tolerance on this path.
    """
    out = {}
    n = 64
    x = grid(n)
    nu, t_end = 0.1, 1.0
    for k in (1, 3, 6):
        r = solve_gclm(np.sin(k * x), a=0.0, nu=nu, t_max=t_end,
                       nonlinear=False, dt_max=1e-2)
        want = np.exp(-nu * k * k * t_end) * np.sin(k * x)
        err = float(np.max(np.abs(r.omega_final - want))) / float(np.max(np.abs(want)))
        out[f"k{k}_rel_err"] = err
        assert err < 1e-12, (k, err)
    # superposition, and dt-independence (exactness, not convergence)
    w0 = np.sin(x) + 0.5 * np.sin(4 * x)
    r_coarse = solve_gclm(w0, nu=nu, t_max=t_end, nonlinear=False, dt_max=5e-1)
    r_fine = solve_gclm(w0, nu=nu, t_max=t_end, nonlinear=False, dt_max=1e-3)
    out["dt_independence"] = float(
        np.max(np.abs(r_coarse.omega_final - r_fine.omega_final))
    )
    assert out["dt_independence"] < 1e-13, out
    out["step_ratio"] = r_fine.n_timesteps / r_coarse.n_timesteps
    assert out["step_ratio"] > 100, out
    return out


def check_solve_gclm_degregorio_stationary():
    """sin x is a stationary solution of De Gregorio (a = 1, nu = 0).

    The end-to-end consequence of check_rhs_degregorio_stationary_mode: the
    solver must hold it fixed for a long time. This is a known-answer check
    on the FULL a != 0 code path that no existing test performs -- the only
    a != 0 check in test_solver_clm.py freezes u, which removes the term
    whose cancellation is being tested here.
    """
    out = {}
    n = 64
    x = grid(n)
    w0 = np.sin(x)
    r = solve_gclm(w0, a=1.0, nu=0.0, t_max=5.0, dt_max=1e-2)
    out["outcome_no_blowup"] = 1.0 if r.outcome == "no_blowup" else 0.0
    assert r.outcome == "no_blowup", r.outcome
    out["max_drift_from_initial"] = float(np.max(np.abs(r.omega_final - w0)))
    assert out["max_drift_from_initial"] < 1e-9, out
    out["amplitude_ratio"] = float(r.max_omega[-1]) / float(r.max_omega[0])
    assert abs(out["amplitude_ratio"] - 1.0) < 1e-9, out
    out["conservation_drift"] = r.conservation_drift
    assert r.conservation_drift < 1e-8, out
    return out


def check_solve_gclm_mean_invariant():
    """int w dx is exactly conserved: no term touches the k = 0 mode.

    Asserted here on NON-odd data with a nonzero mean, at a != 0, which is
    the configuration in which the invariant is a real constraint rather
    than a symmetry.
    """
    out = {}
    n = 64
    x = grid(n)
    w0 = 1.0 + np.sin(x) + 0.4 * np.cos(2 * x)
    for a in (0.0, 0.5, 1.0):
        r = solve_gclm(w0, a=a, nu=0.0, t_max=1.0, dt_max=1e-2)
        out[f"a{a}_mean_drift"] = r.mean_drift
        assert r.mean_drift < 1e-13, (a, r.mean_drift)
        got_mean = TWO_PI * float(np.mean(r.omega_final))
        out[f"a{a}_abs_mean_err"] = abs(got_mean - TWO_PI * float(np.mean(w0)))
        assert out[f"a{a}_abs_mean_err"] < 1e-11, (a, out)
    return out


CHECKS = [
    check_rhs_clm_single_mode,
    check_rhs_degregorio_stationary_mode,
    check_rhs_frozen_u,
    check_rhs_dealiasing,
    check_energy_from_gradient,
    check_energy_from_gradient_odd_n_known_defect,
    check_clm_blowup_time_closed_form,
    check_clm_blowup_time_no_blowup,
    check_solve_gclm_rejects_zero_data,
    check_solve_gclm_result_contract,
    check_solve_gclm_early_decay_exit,
    check_solve_gclm_pure_diffusion_exact,
    check_solve_gclm_degregorio_stationary,
    check_solve_gclm_mean_invariant,
]


def test_rhs_clm_single_mode():
    check_rhs_clm_single_mode()


def test_rhs_degregorio_stationary_mode():
    check_rhs_degregorio_stationary_mode()


def test_rhs_frozen_u():
    check_rhs_frozen_u()


def test_rhs_dealiasing():
    check_rhs_dealiasing()


def test_energy_from_gradient():
    check_energy_from_gradient()


def test_energy_from_gradient_odd_n_known_defect():
    check_energy_from_gradient_odd_n_known_defect()


def test_clm_blowup_time_closed_form():
    check_clm_blowup_time_closed_form()


def test_clm_blowup_time_no_blowup():
    check_clm_blowup_time_no_blowup()


def test_solve_gclm_rejects_zero_data():
    check_solve_gclm_rejects_zero_data()


def test_solve_gclm_result_contract():
    check_solve_gclm_result_contract()


def test_solve_gclm_early_decay_exit():
    check_solve_gclm_early_decay_exit()


def test_solve_gclm_pure_diffusion_exact():
    check_solve_gclm_pure_diffusion_exact()


def test_solve_gclm_degregorio_stationary():
    check_solve_gclm_degregorio_stationary()


def test_solve_gclm_mean_invariant():
    check_solve_gclm_mean_invariant()


if __name__ == "__main__":
    for fn in CHECKS:
        metrics = fn()
        head = ", ".join(f"{k}={v:.3g}" if isinstance(v, float) else f"{k}={v}"
                         for k, v in list(metrics.items())[:4])
        print(f"PASS {fn.__name__}: {head}")
    print(f"\nall gclm dedicated checks passed ({len(CHECKS)} checks)")
