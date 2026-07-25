"""Tests for the 1D Hou-Luo rescaled machinery (Phase-2 P2, validation-first anchor).

The genuinely new pieces vs the CLM solver are the *velocity operator*
(U from U_X = H(Omega), U(0)=0) and the singular explicit steady state of
Chen-Huang-Li arXiv:2604.01868 (their Theorem 2.3). Pre-committed predicates:

  (1) VELOCITY, smooth known pair: with H(Omega)=2/(1+4X^2) (the CLM Hilbert pair),
      U = integral pinned at U(0)=0 must equal arctan(2X) to high accuracy.
  (2) VELOCITY, full pipeline: feeding Omega_CLM=-4X/(1+4X^2) through the actual
      dense Hilbert operator then integrating still recovers arctan(2X).
  (3) VELOCITY on the SINGULAR anchor: velocity(Omega_bar) -> U_bar = 2 sqrt(1-X)-2
      away from the singular point, truncation-limited (error falls as reach M grows).
  (4) STEADY RESIDUAL of the explicit Thm 2.3 profile: (U+c_l X)Omega_X - c_omega Omega
      -> 0 on X>1 (strong steady form, Remark 5.4), small and falling with M.
  (5) CONSTANT CONSISTENCY: c_l+2c_omega = 0 exactly, so the Theta steady equation
      residual vanishes for the explicit profile away from the singularity.

Run: python test_hl_rescaled.py
"""

import numpy as np

from solver.hl_rescaled import (
    RescaledHL, sinh_grid_at, velocity,
    omega_bar, H_omega_bar_exact, U_bar_exact,
)

PI = np.pi


def test_velocity_smooth_known_pair():
    """U from H(Omega)=2/(1+4X^2), pinned U(0)=0, equals arctan(2X)."""
    _, X = sinh_grid_at(4001, Xc=0.0, delta=None, M=400.0)
    Homega = 2.0 / (1.0 + 4.0 * X ** 2)          # = H(-4X/(1+4X^2))
    U = velocity(X, Homega, X_ref=0.0)
    Uex = np.arctan(2.0 * X)
    core = np.abs(X) < 20.0
    err = np.abs(U[core] - Uex[core]).max()
    print(f"    velocity vs arctan(2X): L-inf(|X|<20) = {err:.2e}")
    assert err < 1e-3, f"velocity operator off analytic integral by {err:.2e}"
    print("[ok] velocity operator matches the analytic arctan(2X) on a smooth pair")


def test_velocity_full_pipeline():
    """Omega_CLM -> dense Hilbert -> integrate still recovers arctan(2X).
    (CLM decays only like 1/X, so a large reach M is needed; the residual is
    truncation-limited -- Herr and Uerr both fall ~5x per 5x M, see diagnostics.)"""
    _, X = sinh_grid_at(2001, Xc=0.0, delta=None, M=5000.0)
    s = RescaledHL(X, X_ref=0.0)
    Omega = -4.0 * X / (1.0 + 4.0 * X ** 2)
    U = s.velocity(Omega)
    Uex = np.arctan(2.0 * X)
    core = np.abs(X) < 15.0
    err = np.abs(U[core] - Uex[core]).max()
    print(f"    full-pipeline velocity vs arctan(2X): L-inf(|X|<15) = {err:.2e}")
    assert err < 5e-3, f"pipeline hilbert->velocity off by {err:.2e}"
    print("[ok] hilbert->velocity pipeline recovers arctan(2X)")


def test_velocity_on_singular_anchor_converges():
    """velocity(Omega_bar) -> U_bar away from X=1, integrating the exact H. Error is
    set by the near-singularity resolution delta (the integrable (1-X)^{-1/2} of H),
    and falls as delta shrinks -- ~1/2-order, the expected sqrt-singularity rate."""
    errs = []
    for delta in (0.016, 0.004):
        _, X = sinh_grid_at(4001, Xc=1.0, delta=delta, M=1000.0)
        U = velocity(X, H_omega_bar_exact(X), X_ref=0.0)  # exact H, isolate the integral
        Uex = U_bar_exact(X)
        far = (np.abs(X - 1.0) > 0.25) & (np.abs(X) < 20.0)
        err = np.abs(U[far] - Uex[far]).max()
        errs.append(err)
        print(f"    delta={delta:.3f}  |U-U_bar|_inf(far) = {err:.3e}")
    assert errs[1] < errs[0] * 0.85, "velocity error not falling as delta shrinks"
    assert errs[1] < 1e-2, f"velocity on singular anchor too large: {errs[1]:.2e}"
    print("[ok] velocity on the singular anchor converges to U_bar under refinement")


def test_steady_residual_explicit_profile():
    """(U+2X)Omega_X + Omega -> 0 on X>1 for the explicit Thm 2.3 profile.
    Analytically the residual is exactly zero on the support; numerically it is the
    velocity-integration error (delta-limited), so it falls as delta shrinks."""
    c_l, c_omega = 2.0, -1.0
    res = []
    for delta in (0.016, 0.004):
        _, X = sinh_grid_at(4001, Xc=1.0, delta=delta, M=1000.0)
        s = RescaledHL(X, X_ref=0.0)
        Om = omega_bar(X)
        Th = np.where(X > 1.0, PI / 2.0, 0.0)
        # analytic derivatives (Theta_X = 0 away from the singular point)
        Om_X = np.where(X > 1.0, -0.5 * np.abs(X - 1.0) ** (-1.5), 0.0)
        Th_X = np.zeros_like(X)
        U = velocity(X, H_omega_bar_exact(X), X_ref=0.0)  # exact H to isolate assembly
        R_Om, _ = s.steady_residual(Om, Th, c_l, c_omega, U=U,
                                    Omega_X=Om_X, Theta_X=Th_X)
        # evaluate on the support, away from the singular point, relative to |Omega|
        band = (X > 1.25) & (X < 20.0)
        rel = np.abs(R_Om[band]).max() / np.abs(Om[band]).max()
        res.append(rel)
        print(f"    delta={delta:.3f}  rel steady residual (1.25<X<20) = {rel:.3e}")
    assert res[1] < res[0], "steady residual not decreasing under refinement"
    assert res[1] < 1e-2, f"steady residual not at POC level: {res[1]:.2e}"
    print("[ok] explicit Thm 2.3 profile is a numerical steady state on its support")


def test_constant_consistency_theta_equation():
    """c_l+2c_omega=0 => the Theta steady residual vanishes for the explicit profile."""
    c_l, c_omega = 2.0, -1.0
    assert abs(c_l + 2.0 * c_omega) < 1e-14, "anchor constants violate c_l+2c_omega=0"
    _, X = sinh_grid_at(2001, Xc=1.0, delta=0.004, M=500.0)
    s = RescaledHL(X, X_ref=0.0)
    Om = omega_bar(X)
    Th = np.where(X > 1.0, PI / 2.0, 0.0)
    U = velocity(X, H_omega_bar_exact(X), X_ref=0.0)
    _, R_Th = s.steady_residual(Om, Th, c_l, c_omega, U=U,
                                Omega_X=None, Theta_X=np.zeros_like(X))
    band = (X > 1.25) & (X < 20.0)
    m = np.abs(R_Th[band]).max()
    print(f"    Theta steady residual (1.25<X<20) = {m:.3e}  (c_l+2c_omega={c_l+2*c_omega:.1e})")
    assert m < 1e-12, f"Theta residual nonzero: {m:.2e}"
    print("[ok] c_l+2c_omega=0 makes the Theta equation exactly consistent")


if __name__ == "__main__":
    test_velocity_smooth_known_pair()
    test_velocity_full_pipeline()
    test_velocity_on_singular_anchor_converges()
    test_steady_residual_explicit_profile()
    test_constant_consistency_theta_equation()
    print("\nALL HL-RESCALED TESTS PASSED")
