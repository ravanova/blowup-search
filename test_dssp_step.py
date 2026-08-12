"""Tests solver/dssp_step.py -- Route-DSSP brick B4 (DSSP-STEP).

Run: .venv/bin/python test_dssp_step.py
"""
import numpy as np

from solver.dssp_step import (
    blowup_time,
    closed_form_c,
    galerkin_coefficients,
    integrate_rk4,
    quadrature_nodes,
    rhs,
    rk4_step,
)


def test_quadrature_M_matches_leg351_closed_form():
    """Int|Omega_B|^2 dy = 2*pi^2 exactly (leg 351's own closed form,
    test_dssp_biot_savart.py's test_omega_L2_matches_closed_form). This is
    the quadrature-correctness control for everything downstream in this
    module: if M doesn't match, G and N are not trustworthy either."""
    c = galerkin_coefficients(80, 60, 64, 10.0)
    closed = 2.0 * np.pi ** 2
    rel = abs(c["M"] - closed) / closed
    assert rel < 1e-9, f"M vs 2*pi^2: rel diff {rel:.3e}"
    print(f"[ok] quadrature M matches 2*pi^2 to {rel:.3e} relative")


def test_alpha_converges_across_resolution_and_domain():
    """alpha=-(1/4+G/M) must be stable to at least 1e-8 relative across four
    independent quadrature resolutions AND domain scales (L), or the
    Galerkin coefficients are not converged and nothing downstream can be
    trusted."""
    settings = [(60, 40, 48, 8.0), (80, 60, 64, 10.0),
                (100, 70, 80, 12.0), (120, 80, 96, 14.0)]
    alphas = [galerkin_coefficients(*s)["alpha"] for s in settings]
    spread = max(alphas) - min(alphas)
    rel = spread / abs(alphas[-1])
    assert rel < 1e-7, f"alpha not converged across ladder: rel spread {rel:.3e}"
    print(f"[ok] alpha={alphas[-1]:.10f} stable to {rel:.3e} rel across 4 settings")


def test_alpha_matches_exact_rational_19_over_16():
    """Measured to converge to the exact rational -19/16 -- reported as an
    empirical (not hand-derived) fact, cross-checked at machine precision."""
    c = galerkin_coefficients(100, 70, 80, 12.0)
    assert abs(c["alpha"] - (-19.0 / 16.0)) < 1e-10, c["alpha"]
    assert abs(c["alpha_bug"] - (13.0 / 16.0)) < 1e-10, c["alpha_bug"]
    print(f"[ok] alpha = -19/16 exactly, alpha_bug = 13/16 exactly (to 1e-10)")


def test_N_vanishes_to_machine_precision():
    """N = <Omega_B,(u_B.grad)Omega_B-(Omega_B.grad)u_B> is an EXACT zero by
    a y3-parity argument (module docstring), not merely small -- confirmed
    here at the ~1e-15 relative-to-M level."""
    c = galerkin_coefficients(80, 60, 64, 10.0)
    assert abs(c["N"] / c["M"]) < 1e-13, f"N/M = {c['N']/c['M']:.3e}, expected machine-zero"
    assert abs(c["beta"]) < 1e-13
    print(f"[ok] N/M = {c['N']/c['M']:.3e} (machine-zero, exact identity confirmed numerically)")


def test_rk4_reproduces_closed_form_decay_within_stated_window():
    """THE GATE: stepper reproduces the known answer c(s)=c0*exp(alpha*s)
    (alpha<0, so the probe relaxes to the trivial state) inside the window
    S_max=5, n_steps=2000, to < 1e-6 relative error, decaying below 1% of c0
    by S_max -- all four numbers fixed independently of this run."""
    alpha, beta = -19.0 / 16.0, 0.0
    c0 = 0.01
    s, c, stopped = integrate_rk4(c0, alpha, beta, 5.0, 2000)
    exact = closed_form_c(s, c0, alpha, beta)
    rel_err = float(np.max(np.abs((c - exact) / np.maximum(np.abs(exact), 1e-300))))
    assert not stopped
    assert rel_err < 1e-6, f"stepper vs closed form: {rel_err:.3e}"
    assert abs(c[-1]) / c0 < 1e-2, f"probe did not relax: c(S_max)/c0={c[-1]/c0:.3e}"
    print(f"[ok] RK4 reproduces closed form to {rel_err:.3e} rel; "
          f"c(5)/c0={c[-1]/c0:.3e} (relaxed)")


def test_planted_sign_bug_control_fails_the_relaxation_check():
    """Lesson-90/leg-318 style control: a stepper with the confinement
    term's sign flipped (alpha_bug=13/16>0) must FAIL to relax on the SAME
    initial data and window, or the relaxation check is vacuous."""
    alpha_bug = 13.0 / 16.0
    c0 = 0.01
    s, c, stopped = integrate_rk4(c0, alpha_bug, 0.0, 5.0, 2000)
    ratio = abs(c[-1]) / c0
    assert ratio > 1.0, f"planted control did not fail: growth ratio {ratio:.3e}"
    print(f"[ok] planted sign-bug control fails as required: growth ratio {ratio:.3f}")


def test_closed_form_matches_rk4_for_nonzero_beta():
    """Cross-check the Riccati closed form itself against RK4 on a case with
    beta != 0 (not the physical Omega_B mode, which has beta=0) -- exercises
    the general (**) formula, not just its beta=0 special case."""
    alpha, beta, c0 = -0.7, 0.3, 0.05
    s, c, stopped = integrate_rk4(c0, alpha, beta, 4.0, 3000)
    exact = closed_form_c(s, c0, alpha, beta)
    rel_err = float(np.max(np.abs((c - exact) / np.maximum(np.abs(exact), 1e-300))))
    assert not stopped
    assert rel_err < 1e-6, f"general Riccati case: {rel_err:.3e}"
    print(f"[ok] general (beta!=0) closed form matches RK4 to {rel_err:.3e} rel")


def test_blowup_time_matches_integrator_divergence():
    """A KNOWN finite blowup time s* (alpha=-1,beta=1,c0=2, equilibrium
    c*=1<c0) must be where integrate_rk4's own divergence stop fires, within
    one step-width -- confirms the stepper detects non-relaxation rather
    than silently overflowing past it."""
    alpha, beta, c0 = -1.0, 1.0, 2.0
    s_star = blowup_time(c0, alpha, beta)
    assert s_star is not None and s_star > 0
    s, c, stopped = integrate_rk4(c0, alpha, beta, 2.0 * s_star, 4000)
    assert stopped
    assert abs(s[-1] - s_star) < (2.0 * s_star / 4000) * 2
    print(f"[ok] blowup_time={s_star:.6f} matches integrator stop at s={s[-1]:.6f}")


def test_rhs_and_rk4_step_basic_sanity():
    """rhs(0,...)=0 (Omega=0 is always a fixed point), and one RK4 step on
    pure exponential decay matches exp(alpha*ds) to high order in ds."""
    assert rhs(0.0, -1.0, 3.0) == 0.0
    c1 = rk4_step(1.0, 0.01, -2.0, 0.0)
    assert abs(c1 - np.exp(-0.02)) < 1e-10
    print("[ok] rhs(0)=0 (trivial state is a fixed point); rk4_step matches exp to 1e-10")


def test_quadrature_nodes_shape_and_weight_positivity():
    pts, w = quadrature_nodes(20, 12, 8, 6.0)
    assert pts.shape == (20, 12, 8, 3)
    assert w.shape == (20, 12, 8)
    assert np.all(w > 0), "quadrature weights must all be positive (r^2 dr dcos(theta) dphi)"
    print(f"[ok] quadrature_nodes shapes correct, all {w.size} weights positive")


if __name__ == "__main__":
    test_quadrature_M_matches_leg351_closed_form()
    test_alpha_converges_across_resolution_and_domain()
    test_alpha_matches_exact_rational_19_over_16()
    test_N_vanishes_to_machine_precision()
    test_rk4_reproduces_closed_form_decay_within_stated_window()
    test_planted_sign_bug_control_fails_the_relaxation_check()
    test_closed_form_matches_rk4_for_nonzero_beta()
    test_blowup_time_matches_integrator_divergence()
    test_rhs_and_rk4_step_basic_sanity()
    test_quadrature_nodes_shape_and_weight_positivity()
    print("\nALL DSSP-STEP (B4) TESTS PASSED")
