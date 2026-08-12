"""Tests for solver/kolmogorov2d_nkbasin.py -- Route-DSSP brick B5
(DSSP-NKBASIN).

Run: .venv/bin/python test_kolmogorov2d_nkbasin.py
"""
import numpy as np

from solver.kolmogorov2d_nkbasin import (
    Kolmogorov2D,
    TWO_PI,
    extended_residual,
    gmres_matrix_free,
    grid2d,
    newton_hookstep_rpo,
    newton_krylov_rpo,
    optimal_shift_residual,
    pack,
    shift_x,
    unpack,
)


def test_laminar_profile_is_an_exact_fixed_point():
    """w_lam = -(Re/n)*cos(n*y) must make the FULL rhs (advection+forcing+
    viscosity) vanish identically -- the paper's own base state, and the
    cheapest possible correctness check on the spectral RHS."""
    solver = Kolmogorov2D(N=24, Re=60.0, n_forcing=4, dt=0.01)
    _, Y = grid2d(24)
    w_lam = -(solver.Re / solver.n_forcing) * np.cos(solver.n_forcing * Y)
    rhs = solver.rhs_physical(w_lam)
    resid = float(np.max(np.abs(rhs)))
    assert resid < 1e-10, f"laminar profile is not a fixed point: max|rhs|={resid:.3e}"
    print(f"[ok] laminar fixed point residual {resid:.3e}")


def test_laminar_profile_is_invariant_under_integration():
    """A direct integration check (not just the instantaneous RHS): w_lam
    integrated forward by a finite T must return w_lam unchanged."""
    solver = Kolmogorov2D(N=24, Re=60.0, n_forcing=4, dt=0.01)
    _, Y = grid2d(24)
    w_lam = -(solver.Re / solver.n_forcing) * np.cos(solver.n_forcing * Y)
    w_final, _ = solver.integrate(w_lam, 2.0)
    drift = float(np.max(np.abs(w_final - w_lam))) / float(np.max(np.abs(w_lam)))
    # fixed-dt RK4 accumulates O(dt^4 * n_steps) numerical drift over 200
    # steps; this bounds that, not machine epsilon (the instantaneous RHS
    # check above already confirms the analytic fixed point exactly).
    assert drift < 1e-3, f"laminar profile drifted under integration: {drift:.3e}"
    print(f"[ok] laminar profile integration drift {drift:.3e}")


def test_energy_balance_identity():
    """dE/dt == I - D (paper eq. 13) checked by finite difference on a
    non-trivial (perturbed) field -- exercises advection, forcing, and
    viscosity together, not just the base state."""
    solver = Kolmogorov2D(N=24, Re=60.0, n_forcing=4, dt=0.005)
    rng = np.random.default_rng(0)
    _, Y = grid2d(24)
    w0 = -(solver.Re / solver.n_forcing) * np.cos(solver.n_forcing * Y)
    w0 = w0 + 2.0 * rng.standard_normal((24, 24))
    w0 = np.fft.ifft2(np.fft.fft2(w0) * solver.mask).real
    dt_probe = 0.02
    w_minus, _ = solver.integrate(w0, 4.0)
    w_plus, _ = solver.integrate(w0, 4.0 + dt_probe)
    E_minus = solver.diagnostics(w_minus)[0]
    E_plus = solver.diagnostics(w_plus)[0]
    dEdt_fd = (E_plus - E_minus) / dt_probe
    E, D, I = solver.diagnostics(w_minus)
    dEdt_identity = I - D
    rel = abs(dEdt_fd - dEdt_identity) / max(abs(dEdt_identity), 1e-8)
    assert rel < 0.15, f"energy balance identity off by {rel:.3f} (fd={dEdt_fd:.5f}, I-D={dEdt_identity:.5f})"
    print(f"[ok] energy balance dE/dt(fd)={dEdt_fd:.5f} vs I-D={dEdt_identity:.5f}, rel={rel:.3f}")


def test_shift_x_is_a_group_action_and_identity_at_zero():
    """shift_x(w,0)=w, and shift_x(shift_x(w,a),b) == shift_x(w,a+b) (mod
    2pi), on a generic field -- the phase-condition machinery leans on this
    being an exact Fourier-phase multiply."""
    # a full-band random field aliases at the Nyquist bin under a fractional
    # phase shift (that mode has no real fractional-shift representation),
    # so this uses a band-limited field, as every real caller in this module
    # does (fields are always dealiased with dealias_mask2d before shift_x
    # is applied to them).
    N = 16
    rng = np.random.default_rng(1)
    w_full = rng.standard_normal((N, N))
    mask = np.abs(np.fft.fftfreq(N, d=1.0 / N))[:, None] < N / 3.0
    w = np.fft.ifft2(np.fft.fft2(w_full) * mask).real
    assert np.allclose(shift_x(w, 0.0, N=N), w, atol=1e-10)
    a, b = 0.7, 1.3
    lhs = shift_x(shift_x(w, a, N=N), b, N=N)
    rhs = shift_x(w, a + b, N=N)
    assert np.max(np.abs(lhs - rhs)) < 1e-9
    print("[ok] shift_x identity + composition")


def test_optimal_shift_residual_is_zero_for_a_shifted_copy():
    """optimal_shift_residual(w, shift_x(w,s)) must find s (mod grid
    resolution) and report ~0 residual -- the recurrence-search instrument's
    own correctness check."""
    N = 24
    rng = np.random.default_rng(2)
    w = rng.standard_normal((N, N))
    w = np.fft.ifft2(np.fft.fft2(w) * (np.abs(np.fft.fftfreq(N, d=1.0 / N))[:, None] <= 8)).real
    s_true = 1.1
    w2 = shift_x(w, -s_true, N=N)  # so shift_x(w2, s_true) == w
    s_found, rel = optimal_shift_residual(w, w2)
    # parabolic sub-grid refinement is not exact for a generic band-limited
    # field, so this bounds it well above machine epsilon; the sign/direction
    # convention (this test's real purpose -- it caught a sign bug pairing
    # optimal_shift_residual against shift_x) is what must be tight.
    assert rel < 1e-2, f"optimal-shift residual not near zero: {rel:.3e}"
    ds = abs(((s_found - s_true + np.pi) % TWO_PI) - np.pi)
    assert ds < 0.05, f"found shift {s_found:.4f} does not match true shift {s_true} (|ds|={ds:.4f})"
    print(f"[ok] optimal_shift_residual found s={s_found:.4f} (true {s_true}), rel={rel:.3e}")


def test_pack_unpack_roundtrip():
    N = 8
    rng = np.random.default_rng(3)
    w0 = rng.standard_normal((N, N))
    x = pack(w0, 3.5, -0.2)
    w0b, T, s = unpack(x, N)
    assert np.allclose(w0, w0b)
    assert T == 3.5 and s == -0.2
    print("[ok] pack/unpack roundtrip")


def test_gmres_solves_a_small_linear_system_exactly():
    """The homemade matrix-free GMRES (no scipy available) must solve a
    small well-conditioned linear system to tight tolerance -- checked
    against a plain small matrix, independent of the RPO machinery."""
    rng = np.random.default_rng(4)
    n = 12
    A = rng.standard_normal((n, n)) + 5.0 * np.eye(n)
    b = rng.standard_normal(n)
    x_exact = np.linalg.solve(A, b)
    x, hist = gmres_matrix_free(lambda v: A @ v, b, maxiter=n, tol=1e-10)
    err = np.linalg.norm(x - x_exact) / np.linalg.norm(x_exact)
    assert err < 1e-6, f"GMRES did not match direct solve: rel err {err:.3e}"
    print(f"[ok] homemade GMRES matches np.linalg.solve, rel err {err:.3e}")


def test_extended_residual_vanishes_at_the_laminar_manifold():
    """At w0=w_lam EXACTLY (any T, any s), both phase conditions vanish
    identically (w_lam is x-independent, so d/dx=0, and it's a fixed point,
    so RHS=0) and the state residual vanishes too (shift_x(w_lam,s)=w_lam
    for all s). This is the degenerate control case the Newton-Krylov
    control run (see experiments/journal/leg_353.md) is built on."""
    solver = Kolmogorov2D(N=16, Re=60.0, n_forcing=4, dt=0.01)
    _, Y = grid2d(16)
    w_lam = -(solver.Re / solver.n_forcing) * np.cos(solver.n_forcing * Y)
    ref_rhs = solver.rhs_physical(w_lam)
    w_hat = np.fft.fft2(w_lam) * solver.mask
    ref_dwdx = np.fft.ifft2(1j * solver.KX * w_hat).real
    x = pack(w_lam, 2.3, 0.7)
    R = extended_residual(x, solver, w_lam, ref_rhs, ref_dwdx)
    # relative to the field's own scale: exact algebraically, but the state
    # rows go through a T=2.3 (230-step) RK4 integration first, so this is a
    # numerical-integration-accuracy bound, not machine epsilon.
    rel = float(np.max(np.abs(R))) / float(np.max(np.abs(w_lam)))
    assert rel < 1e-3, f"residual not ~0 (relative) at exact fixed point: {rel:.3e}"
    print(f"[ok] extended_residual ~0 at w_lam, max|R|={np.max(np.abs(R)):.3e} (rel={rel:.3e})")


def test_newton_krylov_reduces_residual_substantially_near_a_true_solution():
    """CONTROL distinguishing 'seed too far from any solution' (what this
    leg found on the published-RPO candidates, see leg_353.md) from 'the
    solver is broken': started near the EXACT (degenerate) laminar fixed
    point, Newton-Krylov must cut the residual by a large factor, unlike the
    <=27% reduction-then-stall seen on every real recurrence-flow seed."""
    solver = Kolmogorov2D(N=24, Re=60.0, n_forcing=4, dt=0.01)
    _, Y = grid2d(24)
    w_lam = -(solver.Re / solver.n_forcing) * np.cos(solver.n_forcing * Y)
    rng = np.random.default_rng(0)
    d = rng.standard_normal(w_lam.shape)
    d /= np.linalg.norm(d)
    w0_guess = w_lam + 0.01 * np.linalg.norm(w_lam) * d
    out = newton_krylov_rpo(w0_guess, 1.0, 0.1, solver, tol=1e-8,
                             max_newton=8, max_gmres=15, fd_eps=1e-6)
    hist = out["residual_history"]
    reduction = 1.0 - hist[-1] / hist[0]
    assert reduction > 0.9, f"control did not reduce residual enough: {100*reduction:.1f}%"
    monotone = all(hist[i + 1] <= hist[i] + 1e-9 for i in range(len(hist) - 1))
    assert monotone, "control residual history was not monotone decreasing"
    print(f"[ok] laminar-control Newton reduced |R| by {100*reduction:.1f}%, monotone")


def test_hookstep_rpo_reproduces_the_laminar_control_through_the_new_layer():
    """PROG-R4 U1 / MILESTONE M1. The same control as the test above, run
    through the trust-region hookstep layer instead of step-halving, must
    still cut the residual by at least as much as leg 353 recorded
    (99.3426310647174%, monotone). This is the milestone's whole content: it
    shows the new globalisation has not broken the solver on a problem whose
    answer is known analytically. It says NOTHING about whether the hookstep
    helps on real RPOs -- that is gate G1's pre-registered question."""
    solver = Kolmogorov2D(N=24, Re=60.0, n_forcing=4, dt=0.01)
    _, Y = grid2d(24)
    w_lam = -(solver.Re / solver.n_forcing) * np.cos(solver.n_forcing * Y)
    rng = np.random.default_rng(0)
    d = rng.standard_normal(w_lam.shape)
    d /= np.linalg.norm(d)
    w0_guess = w_lam + 0.01 * np.linalg.norm(w_lam) * d
    out = newton_hookstep_rpo(w0_guess, 1.0, 0.1, solver, tol=1e-8,
                              max_newton=8, max_gmres=15, fd_eps=1e-6)
    hist = out["residual_history"]
    reduction = 1.0 - hist[-1] / hist[0]
    leg353 = 0.993426310647174
    assert reduction >= leg353, (
        f"hookstep layer reduced |R| by only {100*reduction:.4f}%, below leg "
        f"353's recorded {100*leg353:.4f}%")
    monotone = all(hist[i + 1] <= hist[i] + 1e-9 for i in range(len(hist) - 1))
    assert monotone, "hookstep control residual history was not monotone"
    assert out["reason"] != "nonpositive_period", (
        "the period left the domain: the trust region is not honouring T > 0")
    print(f"[ok] hookstep layer reduced |R| by {100*reduction:.4f}% "
          f"(leg 353 baseline {100*leg353:.4f}%), monotone, "
          f"reason={out['reason']}")


def test_hookstep_rpo_ledger_carries_the_per_iteration_magnitudes():
    """M1's second deliverable: a per-iteration convergence ledger, persisted.
    The ledger has to carry the trust-region magnitudes (radius, multiplier,
    step norm, ratio) and not merely a residual history, because U4's basin
    measurement reports the FAILURE side and needs the mechanism, not a
    boolean."""
    solver = Kolmogorov2D(N=16, Re=60.0, n_forcing=4, dt=0.02)
    _, Y = grid2d(16)
    w_lam = -(solver.Re / solver.n_forcing) * np.cos(solver.n_forcing * Y)
    rng = np.random.default_rng(1)
    d = rng.standard_normal(w_lam.shape)
    d /= np.linalg.norm(d)
    out = newton_hookstep_rpo(w_lam + 0.01 * np.linalg.norm(w_lam) * d,
                              1.0, 0.1, solver, tol=1e-8, max_newton=3,
                              max_gmres=8, fd_eps=1e-6)
    assert out["ledger"], "hookstep RPO driver produced an empty ledger"
    need = {"iteration", "residual_before", "residual_after", "krylov_dim",
            "n_radius_trials", "accepted", "trials", "delta_after",
            "T_before", "s_before"}
    missing = need - set(out["ledger"][0])
    assert not missing, f"ledger entry missing fields: {sorted(missing)}"
    tneed = {"delta", "mu", "step_norm", "on_boundary", "rho",
             "predicted_reduction", "actual_reduction", "residual_after"}
    tmissing = tneed - set(out["ledger"][0]["trials"][0])
    assert not tmissing, f"trial record missing fields: {sorted(tmissing)}"
    # Every finite-difference probe is a full nonlinear integration over the
    # orbit period, so the counts are the real cost currency of U3 and must be
    # reported rather than inferred.
    assert out["n_jac_evals"] > 0 and out["n_residual_evals"] > 0, (
        "driver did not count its Jacobian actions / residual evaluations")
    print(f"[ok] hookstep RPO ledger complete over {len(out['ledger'])} "
          f"iterations, {out['n_jac_evals']} Jacobian actions, "
          f"{out['n_residual_evals']} residual evaluations")


def test_hookstep_rpo_keeps_the_period_strictly_positive():
    """T <= 0 is meaningless for an orbit and the residual map is not even
    defined there. Started from a deliberately bad period, the driver must
    never RETURN a non-positive period -- the trust region has to reject
    those trials rather than integrate a penalised surrogate."""
    solver = Kolmogorov2D(N=16, Re=60.0, n_forcing=4, dt=0.02)
    _, Y = grid2d(16)
    w_lam = -(solver.Re / solver.n_forcing) * np.cos(solver.n_forcing * Y)
    rng = np.random.default_rng(2)
    d = rng.standard_normal(w_lam.shape)
    d /= np.linalg.norm(d)
    out = newton_hookstep_rpo(w_lam + 0.05 * np.linalg.norm(w_lam) * d,
                              0.05, 0.3, solver, tol=1e-8, max_newton=5,
                              max_gmres=8, fd_eps=1e-6)
    assert out["T"] > 0.0, f"driver returned a non-positive period T={out['T']}"
    for e in out["ledger"]:
        assert e["T_before"] > 0.0, (
            f"iteration {e['iteration']} began at T={e['T_before']}")
    # NOTE, recorded rather than tuned away: T collapses towards the boundary
    # on THIS control because the laminar point is a fixed point, where
    # Phi_T(w) = w for every T and the period is an exact null direction (U1's
    # ledger measures ||dR/dT|| = 0.0212 against 9.775 for a state direction).
    # For a genuine RPO seed the period is a real direction and no such
    # collapse is expected; if one is seen in U3 it is a finding, not a bug.
    print(f"[ok] period stayed positive from a bad start: T={out['T']:.3e} "
          f"over {len(out['ledger'])} iterations, reason={out['reason']}")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"\n{len(tests)}/{len(tests)} tests passed")
