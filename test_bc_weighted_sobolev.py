"""Executable gates for solver/bc_weighted_sobolev.py (leg 256, Route-P1B).

Banked lesson 68 -- a check that is not executable decays at the rate of memory --
applied to a module whose whole value is that it agrees with somebody else's published
numbers.  Every gate here is a KNOWN ANSWER: an exact rational, an exact orthogonality,
an analytically-known eigenvalue, or a constant printed in arXiv:2404.04054v2.

The gate that matters most is (2).  Breden-Chu's operator has TWO plausible eigenvalue
conventions in play -- their eq. (11) indexes Hermite functions in Cartesian coordinates
by |beta| and their Corollary 9 indexes the radial Laguerre basis by n, and for the even
half-Hermite family used in section 6 those differ by a factor of two in the index.  A
slip there would make every constant downstream a correct bound on the wrong problem.
Test (2) settles it against the operator itself, by finite differences, and is the exact
analogue of leg 61's sign-convention gate.

Run: .venv/bin/python test_bc_weighted_sobolev.py
"""

import math
import sys

import numpy as np

from solver import bc_weighted_sobolev as bc


def test_gauss_laguerre_small_cases_are_exact():
    """N = 2, alpha = 0: nodes 2 -+ sqrt(2), weights (2 -+ sqrt(2))/4."""
    s, lw = bc.gauss_laguerre(2, 0.0)
    w = np.exp(lw)
    assert np.allclose(s, [2 - math.sqrt(2), 2 + math.sqrt(2)], rtol=1e-13), s
    assert np.allclose(w, [(2 + math.sqrt(2)) / 4, (2 - math.sqrt(2)) / 4],
                       rtol=1e-12), w
    # Sturm bisection cannot deliver a repeated or out-of-order node
    for N, alpha in ((40, 0.0), (40, 0.5), (40, -0.5), (200, 0.5)):
        s, lw = bc.gauss_laguerre(N, alpha)
        assert len(s) == N
        assert np.all(np.diff(s) > 0), (N, alpha)
        rel = abs(float(np.sum(np.exp(lw))) / math.gamma(alpha + 1.0) - 1.0)
        assert rel < 1e-11, (N, alpha, rel)
    print("    N=2 nodes/weights exact; nodes strictly increasing; sum w = Gamma(a+1)")
    print("[ok] Gauss-Laguerre without scipy is right")


def test_the_eigenvalue_convention_is_lambda_m_equals_half_plus_m():
    """L psi_m = (1/2 + m) psi_m for L = -d_xx - (x/2)d_x -- checked, not assumed.

    This is the gate that would catch the 1/2 + m vs 1/2 + 2m confusion between the
    paper's eq. (11) (Cartesian, indexed by |beta|) and its Corollary 9 (radial,
    indexed by the Laguerre degree).  Finite-differenced on a grid, away from the
    endpoints.
    """
    n = 8
    h = 1e-4
    x = np.linspace(0.2, 6.0, 401)
    P, _ = bc.psi_values(n, x)
    Pp, _ = bc.psi_values(n, x + h)
    Pm, _ = bc.psi_values(n, x - h)
    d2 = (Pp - 2.0 * P + Pm) / h ** 2
    d1 = (Pp - Pm) / (2.0 * h)
    Lpsi = -d2 - (x[:, None] / 2.0) * d1
    lam = bc.eigenvalues(n)
    for m in range(n + 1):
        num = float(np.max(np.abs(Lpsi[:, m] - lam[m] * P[:, m])))
        scale = float(np.max(np.abs(P[:, m]))) * lam[m]
        assert num / scale < 2e-6, (m, num / scale)
    # and the operator is NOT consistent with the other convention
    bad = float(np.max(np.abs(Lpsi[:, 2] - (0.5 + 4) * P[:, 2])))
    assert bad / (float(np.max(np.abs(P[:, 2]))) * 4.5) > 1e-2
    print(f"    L psi_m = (1/2+m) psi_m for m=0..{n}, rel residual < 2e-6")
    print("    the 1/2+2m convention is refuted by the same measurement")
    print("[ok] the eigenvalue convention is the one section 6 uses")


def test_psi_at_zero_and_sup_bounds_agree_with_direct_evaluation():
    n = 30
    P, D = bc.psi_values(n, np.array([0.0]))
    assert np.allclose(P[0], bc.psi_at_zero(n), rtol=1e-12)
    assert np.allclose(D[0], 0.0, atol=1e-12), "Neumann: d_x psi_m(0) = 0"
    sup, dsup = bc.sharp_sup_psi(n, n_x=4001, x_max=40.0)
    bnd, dbnd = bc.sup_psi_bounds(n)
    assert np.all(bnd >= sup * (1 - 1e-9)), "their analytic sup bound must dominate"
    assert np.all(dbnd >= dsup * (1 - 1e-9)), "their analytic dsup bound must dominate"
    # Remark 41: the true sup obeys ||psi_m||_inf <= pi^{-1/4}
    assert np.max(sup) <= math.pi ** -0.25 * (1 + 1e-9), np.max(sup)
    print(f"    psi_m(0) matches the closed form; d_xpsi_m(0) = 0 (Neumann)")
    print(f"    measured max_m ||psi_m||_inf = {np.max(sup):.6f} "
          f"<= pi^-1/4 = {math.pi ** -0.25:.6f}  (Remark 41)")
    print("[ok] basis values, Neumann condition and the sup bounds are consistent")


def test_breden_chu_own_exact_rational_quadrature_identities():
    """The two identities their quadrature.jl checks, and all-mode orthonormality."""
    rules = bc.make_rules(30)
    ident = bc.check_quadrature_identities(rules)
    assert ident["six_product_rel_err"] < 1e-11, ident
    assert ident["four_product_rel_err"] < 1e-11, ident
    ortho = bc.check_orthonormality(rules)
    assert ortho["max_abs_offdiag_and_diag_defect"] < 1e-12, ortho
    print(f"    sqrt(5) pi Int psi_1^4 psi_1'^2 = 669/31250 to "
          f"{ident['six_product_rel_err']:.2e}")
    print(f"    pi Int psi_1^3 psi_1'         = -29/324   to "
          f"{ident['four_product_rel_err']:.2e}")
    print(f"    <psi_a,psi_b> = delta_ab to "
          f"{ortho['max_abs_offdiag_and_diag_defect']:.2e} over all a,b <= 30")
    print("[ok] the product quadrature reproduces exact rationals")


def test_radii_polynomial_reproduces_breden_chus_published_delta_bar():
    """Corollary 21, fed their published Z's, must return their published delta_bar.

    Pure algebra -- it does not touch the heavy machinery -- but it is the check that
    our radii polynomial IS their radii polynomial, without which no comparison of
    constants means anything.
    """
    P = bc.BC_THEOREM_42
    v = bc.radii_verdict(P["Y_published"], P["Z1_published"],
                         P["Z2_published"], P["Z3_published"])
    rel = abs(v["delta_bar"] / P["deltabar_published"] - 1.0)
    assert rel < 1e-8, (v["delta_bar"], rel)
    assert v["closes"]
    # Theorem 42's claimed enclosure must be a certified radius of their own polynomial
    assert v["delta_min"] < P["enclosure_published"] < v["delta_bar"]
    assert bc.radii_polynomial(P["Y_published"], P["Z1_published"], P["Z2_published"],
                               P["Z3_published"], P["enclosure_published"]) < 0
    print(f"    their delta_bar reproduced to {rel:.2e} relative")
    print(f"    their enclosure 1e-3 lies in [{v['delta_min']:.6e}, "
          f"{v['delta_bar']:.6e}] -- Theorem 42 is carried by its printed constants")
    print("[ok] the radii polynomial is Corollary 21")


def test_the_ode_branch_is_the_one_breden_chu_solved():
    """u(0) brackets the admissible amplitude, and their ubar(0) is inside it.

    Their stored coefficients give ubar(0) = 1.165375102578254 (recorded in
    writeup/novelty/leg_256.md).  Shooting the ODE, u(9) changes sign across it: below,
    the profile stays positive, above, it crosses.  Cheap, and it pins the branch
    without running the full bisection.
    """
    lo, hi = 1.10, 1.25
    _, u_lo = bc.shoot_profile(lo, x_max=9.0, h=4e-4)
    _, u_hi = bc.shoot_profile(hi, x_max=9.0, h=4e-4)
    assert u_lo[-1] > 0 > u_hi[-1], (u_lo[-1], u_hi[-1])
    _, u_at = bc.shoot_profile(1.165375102578254, x_max=9.0, h=4e-4)
    assert abs(u_at[-1]) < 1e-4 * abs(u_lo[-1]), u_at[-1]
    assert lo < 1.165375102578254 < hi
    print(f"    u(9): {u_lo[-1]:+.3e} at a=1.10, {u_hi[-1]:+.3e} at a=1.25, "
          f"{u_at[-1]:+.3e} at their ubar(0)")
    print("[ok] the shooting branch is Breden-Chu's Theorem 42 profile")


def test_newton_solves_equation_54_and_the_bounds_are_finite():
    """End to end at a small n: Newton converges, and every bound is a real number."""
    n = 60
    rules = bc.make_rules(n)
    pr = bc.BurgersSelfSimilar(n, rules)
    xs, us = bc.shoot_profile(1.1653751, x_max=12.0, h=4e-4)
    a, hist = pr.newton(bc.project_profile(xs, us, n))
    assert hist[-1] < 1e-12, hist
    assert len(hist) < 12, hist
    b = bc.bounds(pr, a)
    for k in ("Y", "Z1", "Z2", "Z3", "Zbar11", "Zbar12", "Zbar21", "Zbar22"):
        assert np.isfinite(b[k]) and b[k] >= 0, (k, b[k])
    # the solution Newton lands on is the one that was shot for
    assert abs(b["ubar_at_zero"] - 1.1653751) < 5e-3, b["ubar_at_zero"]
    # Zbar11 measures how well An inverts P_n DF(ubar) P_n: it must be tiny
    assert b["Zbar11"] < 1e-8, b["Zbar11"]
    print(f"    n={n}: Newton {hist[0]:.2e} -> {hist[-1]:.2e} in {len(hist)} steps")
    print(f"    ubar(0) = {b['ubar_at_zero']:.7f}, Zbar11 = {b['Zbar11']:.2e}")
    print("[ok] eq. (54) is solved and every section-6 bound evaluates")


def test_a_displaced_ubar_is_noticed():
    """An over-optimistic certificate is one that does not notice a displacement.

    The quantity that tracks the ITERATE is Y's finite part ||L A_n P_n F(ubar)||;
    Y's other half is the discarded tail ||(I-P_n)(ubar^2 d_x ubar)||, which is set by
    the TRUNCATION and is nearly blind to a small displacement.  At a small n the tail
    dominates the total outright, so asserting on the total would be asserting on the
    resolution.  Both are reported; the assertion is on the one with the meaning.
    """
    n = 40
    rules = bc.make_rules(n)
    pr = bc.BurgersSelfSimilar(n, rules)
    xs, us = bc.shoot_profile(1.1653751, x_max=12.0, h=4e-4)
    a, _ = pr.newton(bc.project_profile(xs, us, n))
    base = bc.bounds(pr, a)
    rng = np.random.default_rng(256)
    bad = a.copy()
    bad[:10] += 1e-4 * rng.standard_normal(10)
    worse = bc.bounds(pr, bad)
    assert worse["Y_finite_part"] > 1e5 * base["Y_finite_part"], (
        base["Y_finite_part"], worse["Y_finite_part"])
    assert worse["Y"] > base["Y"]
    print(f"    Y finite part {base['Y_finite_part']:.3e} -> "
          f"{worse['Y_finite_part']:.3e}  ({worse['Y_finite_part'] / base['Y_finite_part']:.2e}x)")
    print(f"    Y total       {base['Y']:.3e} -> {worse['Y']:.3e}  "
          f"(tail-dominated at n={n}: tail is {base['Y_tail_part'] / base['Y']:.4f} of it)")
    print("[ok] the defect bound tracks the iterate")


if __name__ == "__main__":
    test_gauss_laguerre_small_cases_are_exact()
    test_the_eigenvalue_convention_is_lambda_m_equals_half_plus_m()
    test_psi_at_zero_and_sup_bounds_agree_with_direct_evaluation()
    test_breden_chu_own_exact_rational_quadrature_identities()
    test_radii_polynomial_reproduces_breden_chus_published_delta_bar()
    test_the_ode_branch_is_the_one_breden_chu_solved()
    test_newton_solves_equation_54_and_the_bounds_are_finite()
    test_a_displaced_ubar_is_noticed()
    print("\nALL BC-WEIGHTED-SOBOLEV TESTS PASSED")
    sys.exit(0)
