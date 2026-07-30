"""Gates for solver/decay_collocation.py -- the Route-D v4 collocation layer.

Every gate is against an independent oracle: an exact closed form, or the
independently-written coefficient-space build in solver/nk_fourier (the third
construction of this operator in the project).  Run:
    .venv/bin/python test_decay_collocation.py

  1  the transforms are exact on even trig polys: DCT round-trip, H(cos k) = sin k,
     and the spectral derivative.
  2  jacobian_matrix == solver.nk_fourier.jacobian on band-limited inputs, and
     residual == solver.nk_fourier.residual.  Two independent builds.
  3  the anchor is an exact zero (nodal residual at rounding) and the two closed-form
     kernel directions are annihilated by [DF | dF/dc].
  4  the far-field law of v3, on the FULL operator: X^{a+1} DF[f_a] -> c a - 1.
  5  the gauged square system is nonsingular and its inverse really inverts.
  6  the graded sup norms behave: ||f_a||_X = 1 exactly for the model profile, the
     ungraded (alpha = 0) inverse norm keeps growing with J (logarithmically here,
     linearly in v2's ell^1 build) and the graded one converges -- v2's negative and
     v3's repair, reproduced in a discretization that shares no code path.
"""

import math

import numpy as np

from solver.decay_collocation import (
    Collocation, grid, sup_op_norm, gauged_jacobian, graded_inverse_norm, C_ANCHOR,
)
from solver import nk_fourier as nkf
from solver.decay_grading import cos_power_coeffs, cos_power_mass, eval_sin_series


def test_transforms():
    J = 64
    col = Collocation(J)
    rng = np.random.default_rng(0)
    a = np.zeros(J)
    a[:8] = rng.standard_normal(8)
    f = col.cos_eval @ a
    err_rt = float(np.max(np.abs(col.to_coef @ f - a)))
    err_H = float(np.max(np.abs(col.H @ f - col.sin_eval @ a)))
    dexact = -(np.arange(J) * a) @ np.sin(np.outer(col.theta, np.arange(J))).T
    err_D = float(np.max(np.abs(col.D @ f - dexact)))
    assert err_rt < 1e-13 and err_H < 1e-13 and err_D < 1e-12, (err_rt, err_H, err_D)
    print(f"[ok] (1) transforms exact on even trig polys "
          f"(round-trip {err_rt:.1e}, H {err_H:.1e}, d/dtheta {err_D:.1e})")


def test_matches_coefficient_build():
    """The collocation operator vs the independent coefficient-space operator."""
    J, c = 96, 0.7
    col = Collocation(J)
    rng = np.random.default_rng(1)
    K = 5
    a = rng.standard_normal(K + 1)
    om = col.cos_eval[:, :K + 1] @ a

    # residual
    b = nkf.residual(a, c)                       # sine coefficients
    want = np.sin(np.outer(col.theta, np.arange(1, b.size + 1))) @ b
    got = col.residual(om, c)
    err_r = float(np.max(np.abs(got - want))) / float(np.abs(b).sum())

    # jacobian, column by column (perturbation = cos(k theta))
    Jm = nkf.jacobian(a, c, M=2 * (K + 1) + 4, n_cols=K + 1)
    DF = col.jacobian_matrix(om, c)
    err_j = 0.0
    for k in range(K + 1):
        ek = col.cos_eval[:, k]
        want_k = np.sin(np.outer(col.theta, np.arange(1, Jm.shape[0] + 1))) @ Jm[:, k]
        err_j = max(err_j, float(np.max(np.abs(DF @ ek - want_k)))
                    / float(np.abs(Jm[:, k]).sum()))

    # dc column
    dcw = nkf.dc_column(a)
    want_c = np.sin(np.outer(col.theta, np.arange(1, dcw.size + 1))) @ dcw
    err_c = float(np.max(np.abs(col.dc_column(om) - want_c))) / float(np.abs(dcw).sum())

    assert err_r < 1e-11 and err_j < 1e-11 and err_c < 1e-11, (err_r, err_j, err_c)
    print(f"[ok] (2) collocation == coefficient-space build "
          f"(residual {err_r:.1e}, jacobian {err_j:.1e}, dc column {err_c:.1e})")


def test_anchor_and_kernel():
    col = Collocation(128)
    om = col.anchor()
    r = float(np.max(np.abs(col.residual(om, C_ANCHOR))))
    assert r < 1e-12, r        # nodal, through two dense matrix products
    DF = col.jacobian_matrix(om, C_ANCHOR)
    dc = col.dc_column(om)
    worst = 0.0
    for v, dcv in nkf.kernel_directions(4):
        h = col.cos_eval[:, :v.size] @ v
        worst = max(worst, float(np.max(np.abs(DF @ h + dcv * dc))))
    assert worst < 1e-11, worst
    print(f"[ok] (3) anchor is an exact zero ({r:.1e}) and both kernel directions "
          f"are annihilated ({worst:.1e})")


def test_far_field_law_full_operator():
    """Does the COLLOCATED operator reproduce the exact far field, and converge?

    f_alpha is not band-limited (it is only C^alpha at theta = pi), so the
    collocation H truncates it.  This gate measures that truncation directly --
    collocated DF[f_a] vs the exact DF[f_a] assembled from the closed-form
    coefficients -- and requires it to SHRINK with J.  It is the analogue of the
    Z1 tail term for this discretization, quantified but not bounded.
    """
    K = 200000
    errs = {}
    for alpha in (1.2, 1.5):
        a = cos_power_coeffs(alpha, K)
        row = []
        for J in (500, 1000, 2000):
            col = Collocation(J)
            om = col.anchor()
            h = (1.0 + col.X ** 2) ** (-0.5 * alpha)
            got = col.jacobian_matrix(om, C_ANCHOR) @ h
            Hh = eval_sin_series(a, col.theta)
            hX = -alpha * col.X * (1.0 + col.X ** 2) ** (-0.5 * alpha - 1.0)
            want = h * (-col.X / (1.0 + col.X ** 2)) + om * Hh - C_ANCHOR * hX
            sel = (col.X > 3.0) & (col.X < 50.0)
            w = (1.0 + col.X[sel] ** 2) ** (0.5 * (alpha + 1.0))   # graded codomain
            row.append(float(np.max(w * np.abs(got - want)[sel])))
        errs[alpha] = row
        assert row[-1] < 0.5 * row[0], (alpha, row)
        # and the exact far-field constant, from the closed-form side
        sel = (col.X > 3e2) & (col.X < 2e3)
        lim = (col.X[sel] ** (alpha + 1.0) * want[sel]
               + (cos_power_mass(alpha) / math.pi) * col.X[sel] ** (alpha - 2.0))
        tgt = C_ANCHOR * alpha - 1.0
        assert float(np.max(np.abs(lim - tgt) / abs(tgt))) < 5e-2, (alpha, lim[[0, -1]], tgt)
    print("[ok] (4) collocated far field converges to the exact operator "
          + ", ".join(f"a={a}: {r[0]:.2e}->{r[-1]:.2e} (J=500->2000)"
                      for a, r in errs.items()))


def test_gauged_system_inverts():
    col = Collocation(200)
    M, rows = gauged_jacobian(col, col.anchor(), C_ANCHOR)
    A = np.linalg.inv(M)
    err = float(np.max(np.abs(A @ M - np.eye(col.J))))
    assert err < 1e-8, err
    assert len(rows) == col.J - 1
    print(f"[ok] (5) the gauged square system inverts (||AM - I||_max = {err:.1e})")


def test_graded_vs_ungraded():
    """alpha = 0 (plain sup) must keep GROWING with J; the graded pair must settle.

    Note the ungraded growth is LOGARITHMIC here (a fixed increment per doubling of
    J), not the linear growth the unweighted ell^1 build of Route-D v2 showed --
    different norm, milder divergence, same verdict: unbounded.  The graded pair
    converges: its increments halve at each doubling.
    """
    Js = [100, 200, 400, 800]
    flat = [graded_inverse_norm(Collocation(J), 0.0)[0] for J in Js]
    grad = [graded_inverse_norm(Collocation(J), 1.5)[0] for J in Js]
    d_flat = np.diff(flat)
    d_grad = np.diff(grad)
    assert np.min(d_flat) > 1.0, flat                 # steady log growth, no sign of stopping
    assert d_grad[-1] < 0.6 * d_grad[0], grad         # increments shrinking
    assert grad[-1] < 1.15 * grad[0], grad
    r_flat, r_grad = flat[-1] / flat[0], grad[-1] / grad[0]

    col = Collocation(400)
    for alpha in (1.2, 1.5, 1.8):
        f = (1.0 + col.X ** 2) ** (-0.5 * alpha)
        assert abs(col.norm_domain(f, alpha) - 1.0) < 1e-12, alpha
    print(f"[ok] (6) graded sup norms: ||f_a||_X = 1 exactly; ungraded ||A|| grows "
          f"+{d_flat.mean():.2f} per doubling of J (log-divergent, {flat[0]:.1f}"
          f"->{flat[-1]:.1f}) while graded converges ({grad[0]:.2f}->{grad[-1]:.2f}, "
          f"increments {d_grad[0]:.3f}->{d_grad[-1]:.3f})")


if __name__ == "__main__":
    test_transforms()
    test_matches_coefficient_build()
    test_anchor_and_kernel()
    test_far_field_law_full_operator()
    test_gauged_system_inverts()
    test_graded_vs_ungraded()
    print("\nALL DECAY-COLLOCATION TESTS PASSED")
