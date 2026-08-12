"""Tests solver/dssp_biot_savart.py -- Route-DSSP brick B3 (DSSP-BS).

Run: .venv/bin/python test_dssp_biot_savart.py
"""
import math

import numpy as np

from solver.dssp_biot_savart import (
    G4,
    S,
    a_of_r,
    a_prime,
    a_second,
    field_omegaB,
    field_uB,
    grad_omegaB,
    grad_uB,
    vorticity_nonlinearity,
)


def _fd_jac(fn, x, h):
    J = np.zeros(x.shape[:-1] + (3, 3))
    for j in range(3):
        e = np.zeros(3)
        e[j] = h
        J[..., :, j] = (fn(x + e) - fn(x - e)) / (2 * h)
    return J


def test_G4_small_and_big_branches_agree_at_the_seam():
    """The two closed forms (Taylor series below r=0.6, direct algebra
    above) must agree to double precision right at the switch, or the
    branch split is hiding a real discontinuity."""
    r = np.array([0.598, 0.599, 0.600, 0.601, 0.602])
    from solver.dssp_biot_savart import _G4_big, _G4_small
    small = _G4_small(r)
    big = _G4_big(r)
    assert np.max(np.abs(small - big)) < 5e-10, \
        f"G4 branches disagree at the seam: {np.max(np.abs(small - big)):.3e}"
    print("[ok] G4 small/big branches agree to <5e-10 across r=0.598..0.602")


def test_a_of_0_is_minus_two_thirds():
    """a(0) = -2/3 exactly, from the closed-form antiderivative F(0) =
    -(2/3)/sqrt(1) (the G4(r)/r^3 term vanishes as r->0)."""
    a0 = float(a_of_r(np.array([0.0]))[0])
    assert abs(a0 - (-2.0 / 3.0)) < 1e-12, f"a(0) = {a0}, expected -2/3"
    print("[ok] a(0) = -2/3 exactly")


def test_a_of_r_times_r_tends_to_minus_1():
    """Type-I decay check: a(r) ~ -1/r as r -> infinity, so u_B ~ 1/r, the
    envelope this brick's gate names -- arrived at by solving the vector
    Poisson equation, not assumed."""
    for r in (1e4, 1e6, 1e8, 1e10):
        val = float(a_of_r(np.array([r]))[0]) * r
        assert abs(val - (-1.0)) < 1e-4, f"a(r)*r at r={r}: {val}, expected -1"
    print("[ok] a(r)*r -> -1 as r -> infinity (Type-I decay)")


def test_divergence_and_curl_identities_machine_precision():
    """div u_B = 0 and curl u_B = Omega_B, checked ANALYTICALLY (grad_uB
    depends only on the closed-form a, a', a'' -- no finite differences, no
    quadrature) -- this was resolved as the honest way to check these
    identities after an earlier finite-difference cross-check looked like
    it disagreed at the ~2e-3 level, which turned out to be the FD
    estimate's own cancellation error from a(r) once being quadrature-based,
    not a real bug (see the module docstring)."""
    rng = np.random.default_rng(20260811)
    x = rng.normal(scale=0.8, size=(500, 3))
    J = grad_uB(x)
    div = np.trace(J, axis1=-2, axis2=-1)
    curl = np.stack(
        [J[..., 2, 1] - J[..., 1, 2], J[..., 0, 2] - J[..., 2, 0], J[..., 1, 0] - J[..., 0, 1]],
        axis=-1,
    )
    om = field_omegaB(x)
    assert np.max(np.abs(div)) < 1e-10, f"div u_B max = {np.max(np.abs(div)):.3e}"
    assert np.max(np.abs(curl - om)) < 1e-10, \
        f"curl u_B - Omega_B max = {np.max(np.abs(curl - om)):.3e}"
    print("[ok] div u_B = 0 and curl u_B = Omega_B to <1e-10, 500 random points")


def test_falsification_control_wrong_vorticity_fails_the_curl_check():
    """Lesson-90 style control that could come out otherwise: a deliberately
    WRONG vorticity (Omega_B scaled by 1.01) must FAIL curl(u_B) == omega,
    or the identity check above is vacuous."""
    rng = np.random.default_rng(1)
    x = rng.normal(scale=0.8, size=(50, 3))
    J = grad_uB(x)
    curl = np.stack(
        [J[..., 2, 1] - J[..., 1, 2], J[..., 0, 2] - J[..., 2, 0], J[..., 1, 0] - J[..., 0, 1]],
        axis=-1,
    )
    wrong = 1.01 * field_omegaB(x)
    resid = float(np.max(np.abs(curl - wrong)))
    assert resid > 1e-3, f"planted-wrong-vorticity control did not fail (resid={resid:.3e})"
    print(f"[ok] planted wrong-vorticity control fails as expected (resid={resid:.3e})")


def test_grad_uB_matches_finite_difference():
    """Cross-check the analytic Jacobian against a finite difference of the
    field itself (h chosen away from the a(r)-quadrature-cancellation
    regime that no longer applies now a(r) is closed-form)."""
    rng = np.random.default_rng(2)
    x = rng.normal(scale=0.8, size=(200, 3))
    fd = _fd_jac(field_uB, x, 2e-3)
    an = grad_uB(x)
    diff = float(np.max(np.abs(fd - an)))
    assert diff < 1e-4, f"grad_uB vs FD max diff = {diff:.3e}"
    print(f"[ok] grad_uB matches finite-difference Jacobian (max diff {diff:.3e})")


def test_grad_omegaB_matches_finite_difference():
    rng = np.random.default_rng(3)
    x = rng.normal(scale=0.8, size=(200, 3))
    fd = _fd_jac(field_omegaB, x, 1e-5)
    an = grad_omegaB(x)
    diff = float(np.max(np.abs(fd - an)))
    assert diff < 1e-6, f"grad_omegaB vs FD max diff = {diff:.3e}"
    print(f"[ok] grad_omegaB matches finite-difference Jacobian (max diff {diff:.3e})")


def test_sup_u_equals_4_over_3_at_the_origin():
    """u_B(0) = (0,0,-2a(0)) = (0,0,4/3); this is the field's global sup, a
    fact checked by dedicated grid search in the runner, reproduced here
    directly at the origin as a fast closed-form spot check."""
    u0 = field_uB(np.array([[0.0, 0.0, 0.0]]))[0]
    assert np.allclose(u0, [0.0, 0.0, 4.0 / 3.0], atol=1e-12), f"u_B(0) = {u0}"
    print("[ok] u_B(0) = (0,0,4/3) exactly")


def test_omega_L2_matches_closed_form():
    """Int |Omega_B|^2 dx = 2 pi^2 exactly (Beta-function integral of
    r^4(1+r^2)^-3 times the angular factor 8*pi/3), so ||Omega_B||_L2 =
    pi*sqrt(2) -- an independent closed-form check on the quadrature used
    for the mapping-bound denominator in the runner."""
    r_n = np.geomspace(1e-4, 1e6, 4000)
    t, w = np.polynomial.legendre.leggauss(64)
    c = t
    wc = w
    ph = np.linspace(0, 2 * np.pi, 33)[:-1]
    R, C, PH = np.meshgrid(r_n, c, ph, indexing="ij")
    ST = np.sqrt(np.maximum(0.0, 1.0 - C * C))
    x = np.stack([R * ST * np.cos(PH), R * ST * np.sin(PH), R * C], axis=-1)
    om = field_omegaB(x)
    f2 = np.sum(om * om, axis=-1) * R ** 2
    wph = np.full(len(ph), 2.0 * np.pi / len(ph))
    ang_w = wc[None, :, None] * wph[None, None, :]
    ang = np.sum(f2 * ang_w, axis=(1, 2))
    # trapezoid on the log-spaced radial nodes (coarse spot-check only)
    integral = float(np.trapezoid(ang, r_n))
    closed = 2.0 * math.pi ** 2
    rel = abs(integral - closed) / closed
    assert rel < 1e-3, f"omega_L2^2 vs closed form 2pi^2: rel diff {rel:.3e}"
    print(f"[ok] Int|Omega_B|^2 matches closed form 2*pi^2 (rel diff {rel:.3e})")


def test_S_is_positive_and_decays_algebraically():
    r = np.array([0.0, 1.0, 10.0, 1000.0])
    s = S(r)
    assert np.all(s > 0)
    assert abs(s[-1] * r[-1] ** 3 - 1.0) < 1e-4, "S(r) should behave like r^-3 for large r"
    print("[ok] S(r) positive, S(r) ~ r^-3 tail confirmed")


if __name__ == "__main__":
    test_G4_small_and_big_branches_agree_at_the_seam()
    test_a_of_0_is_minus_two_thirds()
    test_a_of_r_times_r_tends_to_minus_1()
    test_divergence_and_curl_identities_machine_precision()
    test_falsification_control_wrong_vorticity_fails_the_curl_check()
    test_grad_uB_matches_finite_difference()
    test_grad_omegaB_matches_finite_difference()
    test_sup_u_equals_4_over_3_at_the_origin()
    test_omega_L2_matches_closed_form()
    test_S_is_positive_and_decays_algebraically()
    print("\nALL DSSP-BS (B3) TESTS PASSED")
