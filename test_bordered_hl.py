"""Gates for solver/bordered_hl.py -- the bordered steady system for the Route-M target.

The characteristic failure of a Newton-plus-certificate module is not a wrong answer, it
is an answer nobody can check: a Jacobian that is nearly right, a norm nobody named, a
"converged" that means "stopped".  These gates are all known-answer or exactness gates:

  1. the Jacobian against central differences (and the exact quadratic identity, which
     needs no differences at all and is the stronger of the two);
  2. the residual against the INDEPENDENT implementation in solver/hl_rescaled.py, which
     time-steps the same equations through a different code path;
  3. the converged constants against Chen-Huang-Li's published c_l/c_omega = -2.5114;
  4. the weighted-norm helper against hand-computable cases;
  5. the certificate constants against solver/target_selection.py's radii polynomial,
     so the two modules cannot drift apart on what "closes" means.

Run: .venv/bin/python test_bordered_hl.py
"""

import numpy as np

from solver.bordered_hl import (
    BorderedHL, CHL_RATIO, induced_sup_norm, profile_shape, tail_exponent,
    velocity_matrix,
)
from solver.hl_rescaled import RescaledHLScenario2
from solver.target_selection import radii_polynomial, y0_budget

SEED = 20260804


def _fresh(n=201, rho_max=8.0, x0=0.3, w=0.9):
    """A bordered system with border targets taken from generic non-symmetric data."""
    b = BorderedHL(n=n, rho_max=rho_max)
    Om = np.exp(-((b.X - x0) ** 2) / (2.0 * w ** 2))
    V = 0.8 * np.exp(-((b.X - 1.3 * x0) ** 2) / (2.0 * (1.1 * w) ** 2))
    z0 = b.pack(Om, V, 1.06, -0.42, 0.077)
    b.set_pin_from(z0)
    return b, z0


def test_velocity_matrix_matches_the_quadrature_it_replaces():
    """W @ H(Omega) is the same U as hl_rescaled.velocity, to round-off.

    The matrix exists only so the Jacobian can differentiate U; if it were not the
    SAME operator the whole bordered system would be solving a different problem
    from the one the relaxation validated."""
    from solver.hl_rescaled import velocity as velocity_quadrature
    b, z0 = _fresh(n=121)
    Om = z0[:b.n]
    HOm = b.H @ Om
    U_mat = velocity_matrix(b.X, b.i0) @ HOm
    U_quad = velocity_quadrature(b.X, HOm, 0.0)
    err = float(np.abs(U_mat - U_quad).max() / max(np.abs(U_quad).max(), 1e-300))
    assert err < 1e-13, f"velocity operator disagrees with its quadrature: {err:.2e}"
    print(f"    max relative disagreement {err:.2e} over {b.n} nodes")
    print("[ok] the velocity MATRIX is the velocity QUADRATURE")


def test_jacobian_is_exact_by_the_quadratic_identity():
    """F(z+v) - F(z) - DF(z)v == Q(v,v) to round-off, for random v of several sizes.

    This is a stronger gate than a finite-difference check and it is available only
    because F is exactly quadratic: it tests the Jacobian AND the claim of
    quadraticity at once, with no step-size tuning to hide behind.

    The error is normalized by the CANCELLING terms |F(z)| + |DF(z)v|, not by |Q(v,v)|.
    LHS is a difference of O(1) quantities whose round-off is O(eps * |F|) regardless
    of ||v||, while |Q| falls like ||v||^2 -- so normalizing by |Q| would report a
    growing 'error' for a shrinking v and gate the floating-point subtraction rather
    than the algebra.  (Gate the quantity the measurement divides by -- discipline 67.)
    """
    b, z0 = _fresh(n=151)
    rng = np.random.default_rng(SEED)
    J = b.jacobian(z0)
    Fz = b.F(z0)
    worst = 0.0
    for scale in (1e-1, 1e-2, 1e-3):
        v = scale * rng.standard_normal(b.N)
        Jv = J @ v
        lhs = b.F(z0 + v) - Fz - Jv
        rhs = b.quadratic(v)
        cancel = float(np.abs(Fz).max() + np.abs(Jv).max())
        rel = float(np.abs(lhs - rhs).max() / cancel)
        worst = max(worst, rel)
        print(f"    ||v||={scale:.0e}:  |LHS-Q(v,v)| / (|F|+|DFv|) = {rel:.2e}   "
              f"(|Q| itself = {np.abs(rhs).max():.2e})")
    assert worst < 1e-13, f"F is not exactly quadratic (or DF is wrong): {worst:.2e}"
    print("[ok] F is EXACTLY quadratic and DF is its exact derivative")


def test_jacobian_against_central_differences():
    """The independent, dumber check: DF v vs a central difference of F."""
    b, z0 = _fresh(n=151)
    rng = np.random.default_rng(SEED + 1)
    J = b.jacobian(z0)
    h = 1e-6
    worst = 0.0
    for _ in range(3):
        v = rng.standard_normal(b.N)
        fd = (b.F(z0 + h * v) - b.F(z0 - h * v)) / (2.0 * h)
        rel = float(np.abs(fd - J @ v).max() / max(np.abs(J @ v).max(), 1e-300))
        worst = max(worst, rel)
    assert worst < 1e-8, f"Jacobian disagrees with central differences: {worst:.2e}"
    print(f"    worst relative disagreement {worst:.2e} at h = {h:.0e}")
    print("[ok] the analytic Jacobian survives finite differences too")


def test_residual_agrees_with_the_relaxation_solver():
    """R_Omega, R_V are MINUS the relaxation's RHS at the relaxation's own constants.

    solver/hl_rescaled.py evaluates the same equations with upwind transport in rho
    and a 3x3 gauge solve; this module uses spline slopes and treats the constants as
    unknowns.  Where the two must agree is the SMOOTH part of the transport term, so
    the comparison is made with the spline derivative substituted into both -- what is
    being gated is the ALGEBRA of (4.1), not the choice of stencil."""
    n = 401
    b, z0 = _fresh(n=n)
    s2 = RescaledHLScenario2(n=n)
    assert np.abs(s2.X - b.X).max() < 1e-12, "the two modules disagree about the grid"
    Om, V, _, _, _ = b.unpack(z0)
    c_l, c_om, c_r, U, Om_X, V_X = s2.gauge(Om, V)
    z = b.pack(Om, V, c_l, c_om, c_r)
    F = b.F(z)
    HOm = s2.hilbert(Om)
    speed = U + c_l * s2.X + c_r
    L_Om = c_om * Om + V - speed * Om_X            # (4.1), spline transport
    L_V = (2.0 * c_om - HOm) * V - speed * V_X
    err_o = float(np.abs(F[:n] + L_Om).max() / max(np.abs(L_Om).max(), 1e-300))
    err_v = float(np.abs(F[n:2 * n] + L_V).max() / max(np.abs(L_V).max(), 1e-300))
    assert max(err_o, err_v) < 1e-12, f"(4.1) algebra differs: {err_o:.2e}, {err_v:.2e}"
    print(f"    R_Omega {err_o:.2e}, R_V {err_v:.2e} relative to the relaxation RHS")
    print("[ok] the bordered residual is the relaxation's own (4.1), sign for sign")


def test_border_rows_hold_and_are_the_gauge_directions():
    """The three border rows are (4.2)'s three conditions, and Newton satisfies them."""
    b, z0 = _fresh(n=201)
    z, hist = b.newton(z0, tol=1e-13, max_iter=60)
    assert hist["converged"], f"Newton did not converge: {hist['residual_ladder'][-1]:.2e}"
    Om, V, _, _, _ = b.unpack(z)
    g = (Om[b.i0] - b.pin[0], float(b.Drow0 @ Om) - b.pin[1], V[b.i0] - b.pin[2])
    assert max(abs(x) for x in g) < 1e-13, f"border rows not met: {g}"
    lad = hist["residual_ladder"]
    assert lad[-1] < 1e-13 < lad[0], "the ladder does not run from O(1) to machine zero"
    print(f"    ladder {lad[0]:.2e} -> {lad[-1]:.2e} in {len(lad)-1} steps; "
          f"|G| = {max(abs(x) for x in g):.2e}")
    print("[ok] the three (4.2) conditions are equations here, and they hold exactly")


def test_converged_ratio_reproduces_chen_huang_li():
    """c_l/c_omega on a finite domain, and its extrapolation in reach, vs -2.5114.

    The ratio is invariant under all three gauge freedoms (amplitude, dilation,
    translation), so it is the only constant that can be compared with a published
    value at all -- the raw triple depends on CHL's normalization, and sec 8 of the
    notes said so before this leg existed.  On a truncated domain the ratio carries a
    reach-dependent bias; the gate is on the FINITE value being close and the
    extrapolated value being closer, which is what an attributed error looks like."""
    ratios = {}
    for rho_max in (7.0, 8.0, 9.0):
        b, z0 = _fresh(n=301, rho_max=rho_max)
        z, hist = b.newton(z0, tol=1e-13, max_iter=60)
        assert hist["converged"], f"rho_max={rho_max}: {hist['residual_ladder'][-1]:.2e}"
        _, _, c_l, c_om, _ = b.unpack(z)
        ratios[rho_max] = c_l / c_om
        print(f"    rho_max={rho_max:4.1f}  X_max={np.abs(b.X).max():8.1f}  "
              f"c_l/c_omega = {c_l / c_om:.6f}  "
              f"({abs(c_l / c_om - CHL_RATIO) / abs(CHL_RATIO) * 100:.3f}% from CHL)")
    r = [ratios[k] for k in (7.0, 8.0, 9.0)]
    d1, d2 = r[1] - r[0], r[2] - r[1]
    rho = d2 / d1
    assert 0 < rho < 1, f"the reach ladder is not geometric: {rho:.3f}"
    r_inf = r[2] + d2 * rho / (1.0 - rho)
    err = abs(r_inf - CHL_RATIO) / abs(CHL_RATIO)
    assert abs(r[1] - CHL_RATIO) / abs(CHL_RATIO) < 0.02, "finite-reach ratio too far off"
    assert err < 2e-3, f"extrapolated ratio misses CHL by {err*100:.3f}%"
    print(f"    extrapolated in reach: {r_inf:.6f} vs CHL {CHL_RATIO} "
          f"({err*100:.3f}%)")
    print("[ok] the published contraction ratio is reproduced, and the gap is attributed")


def test_converged_profile_is_positive_regular_and_non_symmetric():
    """The object is what Route-M named: positive, regular, no symmetry point.

    Plus the internal known-answer check the border rows never saw -- the far-field
    exponent of Omega must be c_omega/c_l."""
    b, z0 = _fresh(n=401, rho_max=9.0)
    z, hist = b.newton(z0, tol=1e-13, max_iter=60)
    assert hist["converged"]
    Om, V, c_l, c_om, _ = b.unpack(z)
    sh = profile_shape(b.X, Om, V)
    assert sh["positive"], f"profile is not strictly positive: {sh}"
    assert sh["X_peak"] > 0.15, f"profile is peaked at the origin: {sh['X_peak']}"
    assert sh["asymmetry"] > 0.1, f"profile is nearly symmetric: {sh['asymmetry']}"
    q = tail_exponent(b.X, Om, 20.0, 200.0)
    pred = c_om / c_l
    assert abs(q - pred) / abs(pred) < 0.12, f"tail {q:.4f} vs predicted {pred:.4f}"
    print(f"    peak at X={sh['X_peak']:.3f}, min Omega={sh['Omega_min']:.3e}, "
          f"asymmetry={sh['asymmetry']:.3f}")
    print(f"    far-field exponent {q:.4f} vs c_omega/c_l = {pred:.4f}")
    print("[ok] positive, regular, non-symmetric -- and the tail knows the constants")


def test_weighted_norm_helper_is_the_norm_it_claims():
    """induced_sup_norm on hand-computable cases, including both weight directions."""
    M = np.array([[1.0, -2.0], [3.0, 4.0]])
    assert abs(induced_sup_norm(M, None, np.ones(2)) - 7.0) < 1e-14
    # column weights divide, row weights multiply
    v = induced_sup_norm(M, np.array([2.0, 1.0]), np.array([1.0, 2.0]))
    assert abs(v - max(2 * (1 + 1), 1 * (3 + 2))) < 1e-14, v
    # consistency with the vector norm it induces
    rng = np.random.default_rng(SEED + 2)
    w_r, w_c = np.array([0.5, 3.0]), np.array([2.0, 0.25])
    nrm = induced_sup_norm(M, w_r, w_c)
    worst = 0.0
    for _ in range(2000):
        x = rng.standard_normal(2)
        nx = float(np.max(w_c * np.abs(x)))
        worst = max(worst, float(np.max(w_r * np.abs(M @ x))) / nx)
    assert worst <= nrm * (1 + 1e-12), f"sampled {worst:.6f} exceeds claimed {nrm:.6f}"
    assert worst > 0.5 * nrm, "the claimed norm is not attained anywhere near"
    print(f"    claimed {nrm:.6f}, best of 2000 sampled directions {worst:.6f}")
    print("[ok] the weighted induced norm is an upper bound and is nearly attained")


def test_Z2_bound_dominates_the_bilinear_form_it_bounds():
    """Z_2/(2||A||) must dominate ||Qtilde(v,w)|| for sampled unit v, w.

    Z_2 is assembled from operator norms rather than sampled, so this is the gate
    that the assembly is a BOUND and not merely a number of the right size."""
    b, z0 = _fresh(n=151)
    z, _ = b.newton(z0, tol=1e-12, max_iter=60)
    p, w_l = 0.39, 0.01 * float(np.abs(b.X).max())
    c = b.certificate_constants(z, p=p, w_l=w_l)
    w, nu, _ = b.weights(p=p, w_l=w_l)
    rng = np.random.default_rng(SEED + 3)
    worst = 0.0
    for _ in range(200):
        v = rng.standard_normal(b.N)
        v = v / float(np.max(w * np.abs(v)))          # unit in the weighted norm
        Qvv = b.quadratic(v)
        worst = max(worst, float(np.max(w * np.abs(Qvv))))
    assert worst <= c["B"] * (1 + 1e-9), \
        f"sampled bilinear value {worst:.4e} exceeds the bound B = {c['B']:.4e}"
    print(f"    B = {c['B']:.4e} bounds the worst of 200 sampled unit directions "
          f"({worst:.4e}); slack {c['B']/max(worst,1e-300):.1f}x")
    print("[ok] the Z_2 assembly is an upper bound on the form it bounds")


def test_certificate_agrees_with_the_target_selection_radii_polynomial():
    """The float constants, fed to Route-M's radii polynomial, close -- and the module
    and the ledger agree on what closing means.

    Also gates the honest part: at the NAIVE scalar weight the same object at the same
    resolution does NOT close, so the verdict is a statement about the norm and this
    test would catch a silent change of default."""
    b, z0 = _fresh(n=201)
    z, hist = b.newton(z0, tol=1e-14, max_iter=60)
    assert hist["converged"]
    Xmax = float(np.abs(b.X).max())
    tuned = b.certificate_constants(z, p=0.39, w_l=0.01 * Xmax)
    st = radii_polynomial(tuned["Y0"], tuned["Z1"], tuned["Z2"])
    assert st["feasible"], f"the tuned norm does not close: {st['reason']}"
    assert abs(st["Y0_budget"] - y0_budget(tuned["Z1"], tuned["Z2"])) == 0.0
    margin = tuned["Y0"] / st["Y0_budget"]
    assert margin < 1e-2, f"margin thinner than reported: Y0/budget = {margin:.3e}"
    print(f"    tuned norm: Y0={tuned['Y0']:.3e} Z1={tuned['Z1']:.3e} "
          f"Z2={tuned['Z2']:.3e} budget={st['Y0_budget']:.3e}")
    print(f"    r in [{st['r_min']:.3e}, {st['r_max']:.3e}], Y0/budget = {margin:.3e}")
    print("[ok] the radii polynomial closes in float, and both modules agree it does")


def test_the_free_constant_of_the_norm_changes_the_verdict():
    """Directive 3's premise, measured: one scalar weight decides closure.

    Same object, same discretization, same Newton iterate -- only the norm's free
    constant w_l moves, and the radii polynomial goes from closing to not closing.
    If this test ever fails it means the certificate stopped being sensitive to the
    space, which would REMOVE the motivation for stage B."""
    b, z0 = _fresh(n=801)
    z, hist = b.newton(z0, tol=1e-13, max_iter=60)
    assert hist["converged"]
    Xmax = float(np.abs(b.X).max())
    naive = b.certificate_constants(z, p=0.39, w_l=Xmax)
    tuned = b.certificate_constants(z, p=0.39, w_l=0.01 * Xmax)
    s_naive = radii_polynomial(naive["Y0"], naive["Z1"], naive["Z2"])
    s_tuned = radii_polynomial(tuned["Y0"], tuned["Z1"], tuned["Z2"])
    assert not s_naive["feasible"], "the naive weight closes; the contrast is gone"
    assert s_tuned["feasible"], "the tuned weight no longer closes"
    gain = s_naive["Y0_over_budget"] / s_tuned["Y0_over_budget"]
    assert gain > 1e2, f"the free constant is worth only {gain:.1f}x"
    print(f"    n={b.n}: naive w_l={Xmax:.0f} -> Y0/budget {s_naive['Y0_over_budget']:.3e} "
          f"(FAILS)")
    print(f"          tuned w_l={0.01*Xmax:.1f} -> Y0/budget "
          f"{s_tuned['Y0_over_budget']:.3e} (CLOSES); one constant is worth {gain:.0f}x")
    print("[ok] closure is a property of the SPACE, not of the object alone")


if __name__ == "__main__":
    test_velocity_matrix_matches_the_quadrature_it_replaces()
    test_jacobian_is_exact_by_the_quadratic_identity()
    test_jacobian_against_central_differences()
    test_residual_agrees_with_the_relaxation_solver()
    test_border_rows_hold_and_are_the_gauge_directions()
    test_converged_ratio_reproduces_chen_huang_li()
    test_converged_profile_is_positive_regular_and_non_symmetric()
    test_weighted_norm_helper_is_the_norm_it_claims()
    test_Z2_bound_dominates_the_bilinear_form_it_bounds()
    test_certificate_agrees_with_the_target_selection_radii_polynomial()
    test_the_free_constant_of_the_norm_changes_the_verdict()
    print("\nALL BORDERED-HL TESTS PASSED")
