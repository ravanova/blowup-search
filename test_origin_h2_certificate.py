"""Known-answer gates for solver/origin_h2_certificate.py (leg 176, Route-H2C).

The point of this file is that the discrete realization is EXACT, not approximate:
the tridiagonal entries, the two symmetry modes and the border row are all
re-derived here by routes independent of the module's own algebra, and several of
the gates below are exact zeros rather than tolerances.

Run: .venv/bin/python test_origin_h2_certificate.py
"""

import numpy as np

import solver.origin_h2_certificate as H
from solver.origin_h2_certificate import (
    bordered_gram, bordered_operator, border_row, border_row_dual_norm,
    jacobi_xi, l0_plus, project_to_laguerre, symmetry_modes, to_y, x_gram,
    x_norm, x_norm_y, xu_ode_residual, xu_resolvent,
)


def _rect_sigma(N, bordered=True, gram=True):
    Nr = N + 2
    L = l0_plus(Nr)[:, :N]
    _, m = symmetry_modes(Nr)
    Gx_d = x_gram(N) if gram else np.eye(N)
    Gx_c = x_gram(Nr) if gram else np.eye(Nr)
    if bordered:
        A = np.zeros((Nr + 1, N + 1), dtype=complex)
        A[:Nr, :N] = L
        A[:Nr, N] = m
        A[Nr, :N] = border_row(N)
        Gd, Gc = bordered_gram(N, Gx_d), bordered_gram(Nr, Gx_c)
    else:
        A, Gd, Gc = L, Gx_d, Gx_c
    _, Gdih = H._sym_sqrt(Gd)
    Gch, _ = H._sym_sqrt(Gc)
    return float(np.linalg.svd(Gch @ A @ Gdih, compute_uv=False).min())


def test_l0_is_exactly_tridiagonal():
    """Re-derive `xi d/dxi + V` by Laguerre quadrature -- a route the module never takes."""
    nq, NB = 60, 12
    x, w = np.polynomial.laguerre.laggauss(nq)
    E = np.eye(NB + 3)
    Lm = np.array([np.polynomial.laguerre.lagval(x, E[k]) for k in range(NB + 3)])
    dLm = np.array([np.polynomial.laguerre.lagval(
        x, np.polynomial.laguerre.lagder(E[k])) for k in range(NB + 3)])
    assert np.abs(Lm[:NB] @ (w[:, None] * Lm[:NB].T) - np.eye(NB)).max() < 1e-12
    D = np.zeros((NB, NB))
    for n in range(NB):
        D[:, n] = Lm[:NB] @ (w * (x * (dLm[n] - Lm[n] / 2.0)))
    V = np.zeros((NB, NB))
    for n in range(NB):
        V[n, n] += 1.0
        if n + 1 < NB:
            V[n + 1, n] -= 1.0
    err = np.abs(D + V - l0_plus(NB)).max()
    assert err < 1e-11, err
    print(f"    tridiagonal entries vs independent quadrature: {err:.3e}")
    print("[ok] L_0^+ is exactly tridiagonal (-n/2, 1/2, (n-1)/2)")


def test_symmetry_modes_and_border_are_exact():
    """These are EXACT zeros -- Xu's two modes occupy span{l_0,l_1} exactly."""
    N = 200
    L, e = l0_plus(N), border_row(N)
    b2, m = symmetry_modes(N)
    assert np.abs(L @ b2 - b2).max() == 0.0
    assert np.abs(L @ m).max() == 0.0
    assert np.abs(e @ L[:, :N - 1]).max() == 0.0      # ell is the LEFT null vector
    assert e @ m == 1.0
    assert abs(e @ b2) == 0.0
    print("    L0 b^-2 - b^-2 = 0.0 ; L0 m = 0.0 ; ell.L0 = 0.0 ; ell(m) = 1")
    print("[ok] symmetry modes and border row are exact, not approximate")


def test_border_row_matches_its_y_space_definition():
    """`ell(f) = i f(0) - f'(0)/4` evaluated in y-space must equal the Laguerre row."""
    N = 60
    rng = np.random.default_rng(3)
    c = np.zeros(N, dtype=complex)
    c[:8] = rng.normal(size=8) + 1j * rng.normal(size=8)
    lag = border_row(N) @ c
    ysp = 1j * to_y(c, [0.0])[0] - to_y(c, [0.0], 1)[0] / 4.0
    assert abs(lag - ysp) < 1e-12 * abs(lag), (lag, ysp)
    print(f"    ell: laguerre vs y-space, rel diff {abs(lag - ysp) / abs(lag):.3e}")
    print("[ok] border row agrees with i f(0) - f'(0)/4")


def test_x_gram_is_padding_independent_and_positive():
    d = np.abs(x_gram(64, 4) - x_gram(64, 32)).max()
    assert d == 0.0, d
    G = x_gram(64)
    assert np.abs(G - G.T).max() == 0.0
    assert np.linalg.eigvalsh(G).min() > 0
    J = jacobi_xi(40)
    assert np.abs(J - J.T).max() == 0.0
    print("    pad-4 vs pad-32 identical; G symmetric positive definite")
    print("[ok] the X Gram is the exact infinite-basis block")


def test_projection_round_trip():
    c = np.zeros(30, dtype=complex)
    c[0], c[3], c[7], c[15] = 1.0, -0.4 + 0.2j, 0.25j, 0.1
    cr = project_to_laguerre(lambda y: to_y(c, y), M=4096)
    assert np.abs(cr[:30] - c).max() < 1e-14
    assert np.abs(cr[30:1500]).max() < 1e-14
    print(f"    round trip {np.abs(cr[:30] - c).max():.3e}, "
          f"leakage {np.abs(cr[30:1500]).max():.3e}")
    print("[ok] Blaschke projection inverts the y-space evaluation")


def test_to_y_derivatives():
    c = np.array([1.0, -0.3 + 0.2j, 0.15, 0.05j, -0.02])
    for y0 in (0.0, 0.7, 3.0, 25.0):
        h = 1e-5
        d1 = (to_y(c, [y0 + h])[0] - to_y(c, [y0 - h])[0]) / (2 * h)
        assert abs(d1 - to_y(c, [y0], 1)[0]) < 1e-7
        d2 = (to_y(c, [y0 + h])[0] - 2 * to_y(c, [y0])[0]
              + to_y(c, [y0 - h])[0]) / h ** 2
        assert abs(d2 - to_y(c, [y0], 2)[0]) < 1e-4
    print("[ok] analytic first and second derivatives match finite differences")


def test_xu_closed_form_solves_the_ode():
    """The gate's second conjunct, in miniature: Xu eq (4.23) against Xu's own ODE."""
    N = 120
    e, (_, m) = border_row(N), symmetry_modes(N)
    rng = np.random.default_rng(0)
    d = np.zeros(N, dtype=complex)
    d[:6] = rng.normal(size=6) + 1j * rng.normal(size=6)
    f = (d - (e @ d) / (e @ m) * m)[:6]
    yv = np.array([-8., -0.3, 0.05, 0.7, 3., 20.])
    r = xu_ode_residual(f, yv)
    rel = float((np.abs(r) / np.abs(to_y(f, yv))).max())
    assert rel < 1e-12, rel
    print(f"    max relative pointwise ODE residual {rel:.3e} (leg 163 class: 2.8e-14)")
    print("[ok] Xu eq. (4.23) at z=0 reproduces the closed form")


def test_x_norm_gram_matches_y_space_quadrature():
    """Two completely independent routes to the same norm, including the 2*pi factor."""
    c = np.zeros(60, dtype=complex)
    rng = np.random.default_rng(11)
    c[:12] = rng.normal(size=12) + 1j * rng.normal(size=12)
    a = x_norm(c)
    b = x_norm_y(lambda y: (to_y(c, y), to_y(c, y, 2)), M=16384) / np.sqrt(2 * np.pi)
    assert abs(a - b) / a < 1e-10, (a, b)
    print(f"    gram {a:.10f} vs y-space {b:.10f}, rel {abs(a - b) / a:.3e}")
    print("[ok] the X metric is consistent between coefficient and y space")


def test_the_diagnostic_closes_and_the_controls_do_not():
    """C1 vs C3/C4: the result is only meaningful because the controls can fail."""
    s_b = [_rect_sigma(n) for n in (64, 128, 256)]
    assert min(s_b) > 0.08, s_b
    assert max(s_b) - min(s_b) < 1e-4, s_b
    s_u = _rect_sigma(128, bordered=False)
    assert s_u < 1e-10, s_u                      # m is the kernel
    s_l2a, s_l2b = _rect_sigma(64, gram=False), _rect_sigma(256, gram=False)
    assert s_l2b < 0.2 * s_l2a, (s_l2a, s_l2b)   # loose L^2: no gap, decays
    print(f"    bordered/X {s_b} (bounded away from 0, truncation-independent)")
    print(f"    unbordered {s_u:.3e} ; loose-L2 {s_l2a:.3e} -> {s_l2b:.3e}")
    print("[ok] diagnostic closes in X; both controls collapse, as they must")


def test_border_row_bounded_in_X_star_only():
    xd, l2 = [], []
    for n in (64, 128, 256):
        a, b = border_row_dual_norm(n)
        xd.append(a)
        l2.append(b)
    assert max(xd) - min(xd) < 0.05 * max(xd)
    assert l2[-1] > 5 * l2[0]
    print(f"    ||ell||_X* {xd[0]:.4f}->{xd[-1]:.4f} converges ; ||ell||_l2 diverges")
    print("[ok] ell is bounded on X and unbounded on l^2")


if __name__ == "__main__":
    for fn in [v for k, v in sorted(globals().items()) if k.startswith("test_")]:
        print(f"== {fn.__name__}")
        fn()
    print("\nall origin-H^2 certificate gates pass")
