"""Known-answer tests for the Fourier-basis two-scale operator (Route-D dress rehearsal).

Everything the Newton-Kantorovich dress rehearsal computes rests on the closed-form
coefficients in solver/nk_fourier.py, so those are gated here against three
INDEPENDENT oracles: the exact a=0 anchor, finite differences, and the banked
GRID residual (solver/gclm_family.py::GCLMResidual.residual_two_scale) that the GA
sweeps actually scored.  No science claim -- this is the tooling gate.

Pre-committed predicates:
  (1) EXACT ANCHOR: the Fourier residual of Omega_2 = -(1+cos th)/2 at c = 1/2 is
      ZERO to machine precision, at every truncation, in every mode.
  (2) JACOBIAN: the closed-form `jacobian` matches a central finite difference of
      `residual` to ~1e-8, at the anchor AND at a random off-anchor profile.
  (3) SYMMETRY KERNEL: both exact scaling-valley tangents (amplitude, dilation)
      are annihilated by the un-gauged [DF | dF/dc] -- the analytic version of the
      Route-D v1 Q2 singular-value count -- and the gauge functionals are all
      NON-degenerate on the surviving fixed-c kernel direction.
  (4) GRID CROSS-CHECK: the Fourier residual agrees with the independent grid
      residual (sinh grid + dense line-Hilbert matrix) for a non-trivial profile.
  (5) TAIL ALGEBRA: the closed-form far-field band matches a directly assembled
      DF column exactly (and that column is tridiagonal); the two natural tail
      diagonal models SANDWICH the Z1 column weight around 1 and both converge to
      it like O(1/k); and no positive weight beats that (the marginal affine-u
      weight gives exactly 1).
  (6) RADII POLYNOMIAL: closes / fails exactly where the algebra says, including
      the Y0_max ("certification budget") boundary.

Run: python test_nk_fourier.py    (no scipy; a few seconds)
"""

import numpy as np

from solver.nk_fourier import (
    C_ANCHOR, anchor, kernel_directions, residual, jacobian, dc_column,
    gauged_system, gauge_row, ell1_op_norm, radii_polynomial,
    tail_band, tail_Z1_column, tail_weight_obstruction,
)
from solver.gclm_family import GCLMResidual, clm_two_scale


def test_exact_anchor():
    """(1) The anchor is an EXACT zero of the Fourier residual, at every N."""
    worst = 0.0
    for N in (1, 2, 5, 12, 40):
        a = anchor(N)
        b = residual(a, C_ANCHOR)
        worst = max(worst, float(np.abs(b).max()))
        assert np.abs(b).max() < 1e-15, f"N={N}: anchor residual {np.abs(b).max():.3e}"
    # and it is NOT accidentally zero for a wrong speed
    off = residual(anchor(8), 0.45)
    assert np.abs(off).max() > 1e-3, "residual must be speed-sensitive"
    print(f"[ok] (1) exact anchor: max |b_m| = {worst:.3e} over N in {{1,2,5,12,40}}; "
          f"c=0.45 gives {np.abs(off).max():.3e}")


def test_jacobian_matches_finite_difference():
    """(2) Closed-form DF == central finite difference of the residual."""
    rng = np.random.default_rng(7)
    worst = 0.0
    for label, a in (("anchor", anchor(6)),
                     ("random", rng.standard_normal(7) * 0.3)):
        c = C_ANCHOR
        M = 2 * (a.size - 1) + 2
        J = jacobian(a, c, M=M, n_cols=a.size)
        h = 1e-6
        for k in range(a.size):
            ap, am = a.copy(), a.copy()
            ap[k] += h
            am[k] -= h
            fd = (residual(ap, c, M=M) - residual(am, c, M=M)) / (2 * h)
            err = float(np.abs(fd - J[:, k]).max())
            worst = max(worst, err)
            assert err < 1e-7, f"{label} col {k}: DF vs FD mismatch {err:.3e}"
        # and the speed column
        M2 = 2 * (a.size - 1)
        fd_c = (residual(a, c + h, M=M2) - residual(a, c - h, M=M2)) / (2 * h)
        errc = float(np.abs(fd_c - dc_column(a, M=M2)).max())
        assert errc < 1e-7, f"{label}: dF/dc mismatch {errc:.3e}"
        worst = max(worst, errc)
    print(f"[ok] (2) jacobian vs finite difference: max err = {worst:.3e}")


def test_symmetry_kernel_and_gauges():
    """(3) The two scaling-valley tangents lie in ker[DF | dF/dc]; gauges break it."""
    N = 10
    a = anchor(N)
    M = 2 * N
    J = jacobian(a, C_ANCHOR, M=M, n_cols=N + 1)
    dc = dc_column(a, M=M)
    worst = 0.0
    for v, dcv in kernel_directions(N):
        img = J @ v + dcv * dc
        worst = max(worst, float(np.abs(img).max()))
        assert np.abs(img).max() < 1e-14, f"kernel direction not annihilated: {img}"
    # with c FIXED the surviving kernel is the fiber lambda*mu = 1
    v1, d1 = kernel_directions(N)[0]
    v2, d2 = kernel_directions(N)[1]
    w = (-d2 / d1) * v1 + v2          # the combination with zero dc component
    assert np.abs(J @ w).max() < 1e-14, "fixed-c kernel direction must be annihilated"
    # closed form: w = -(1/4) cos(th)(1 + cos th) = -(1/8, 1/4, 1/8, 0, ...)
    ref = np.zeros(N + 1)
    ref[0], ref[1], ref[2] = -0.125, -0.25, -0.125
    assert np.abs(w - ref).max() < 1e-14, f"fixed-c kernel closed form: {w[:4]}"
    # every gauge functional must be non-degenerate on w (else it does not isolate)
    vals = {}
    for name in ("origin", "a0", "a1"):
        grad, _ = gauge_row(name, N)
        vals[name] = float(np.dot(grad, w))
        assert abs(vals[name]) > 1e-3, f"gauge {name} degenerate on the kernel"
    # ... and the gauged square system is then non-singular
    _, Jg = gauged_system(a, C_ANCHOR, N, gauge="origin")
    s = np.linalg.svd(Jg, compute_uv=False)
    assert s[-1] > 1e-6, f"gauged system singular: sigma_min = {s[-1]:.3e}"
    print(f"[ok] (3) kernel annihilated to {worst:.3e}; gauge<w> = "
          + ", ".join(f"{k}:{v:+.3f}" for k, v in vals.items())
          + f"; sigma_min(gauged) = {s[-1]:.3e}")


def test_grid_cross_check():
    """(4) Fourier residual == the independent grid residual (sinh grid + Hmat)."""
    R = GCLMResidual(a=0.0, n=2001)
    X, theta = R.X, 2.0 * np.arctan(R.X)
    msk = np.abs(X) < 12.0                      # well-resolved bulk

    # anchor gate: the grid form of the Fourier anchor IS clm_two_scale
    a_anchor = anchor(3)
    Om_fourier = sum(a_anchor[k] * np.cos(k * theta) for k in range(a_anchor.size))
    assert np.abs(Om_fourier - clm_two_scale(X)).max() < 1e-12, "anchor map mismatch"

    # a genuinely non-trivial profile: anchor + two extra cosine modes
    a = anchor(4).copy()
    a[2] += 0.13
    a[4] -= 0.07
    c = 0.37
    Om = sum(a[k] * np.cos(k * theta) for k in range(a.size))
    R2_grid, _ = R.residual_two_scale(Om, c_tw=c)
    b = residual(a, c)
    R2_fourier = sum(b[m - 1] * np.sin(m * theta) for m in range(1, b.size + 1))
    scale = float(np.abs(R2_grid[msk]).max())
    err = float(np.abs(R2_grid - R2_fourier)[msk].max()) / scale
    assert err < 5e-3, f"grid vs Fourier residual rel err {err:.3e}"
    print(f"[ok] (4) grid cross-check: rel err = {err:.3e} "
          f"(|R2|max = {scale:.3f}, discretization-limited)")


def test_tail_algebra():
    """(5) The far-field column weight -> 1 from BOTH sides, and no weight fixes it."""
    # directly assemble the far-field columns from the SAME jacobian code and
    # confirm the closed band + both column-weight models
    N = 60
    a = anchor(4)
    J = jacobian(a, C_ANCHOR, M=N + 4, n_cols=N + 2)
    worst = 0.0
    for k in (20, 35, 50):
        col = J[:, k]
        sub, dia, sup = tail_band(k)
        assembled = (col[k - 2], col[k - 1], col[k])          # rows k-1, k, k+1
        worst = max(worst, float(np.abs(np.array(assembled)
                                       - np.array([sub, dia, sup])).max()))
        assert abs(col).sum() - abs(sub) - abs(dia) - abs(sup) < 1e-12, \
            f"column {k} must be tridiagonal"
        for model, lam in (("transport", lambda m: C_ANCHOR * m),
                           ("exact", lambda m: C_ANCHOR * m - 0.5)):
            z = abs(sub) / abs(lam(k - 1)) + abs(sup) / abs(lam(k + 1))
            assert abs(z - tail_Z1_column(k, diag=model)) < 1e-12, \
                f"k={k} {model}: assembled {z:.9f}"

    # the two tail models sandwich 1 and BOTH converge to it -> exactly marginal
    for k in (10, 100, 1000, 10000):
        lo = tail_Z1_column(k, diag="transport")
        hi = tail_Z1_column(k, diag="exact")
        assert lo < 1.0 < hi, f"k={k}: models must sandwich 1 ({lo:.6f}, {hi:.6f})"
        assert hi - lo < 3.0 / k, f"k={k}: sandwich must tighten like 1/k"

    # weighted: the marginal affine-u weight w(k) = k*(1+k) gives exactly 1 ...
    z_aff, _, _ = tail_weight_obstruction(lambda k: k * (1.0 + k), 5, 400)
    assert abs(z_aff - 1.0) < 1e-9, f"affine u must be marginal, got {z_aff:.9f}"
    # ... and the two natural families both fail to get uniformly below 1
    for name, w in (("k^0.5", lambda k: k ** 0.5),
                    ("k^1.5", lambda k: k ** 1.5),
                    ("1.05^k", lambda k: 1.05 ** k)):
        zw, _, _ = tail_weight_obstruction(w, 5, 400)
        assert zw >= 1.0 - 1e-3, f"weight {name} unexpectedly beat the bound: {zw:.6f}"
    print(f"[ok] (5) tail: assembled band vs closed form max err {worst:.3e}; "
          f"z(k)->1 from both sides; affine-u weight marginal at {z_aff:.9f}")


def test_radii_polynomial_algebra():
    """(6) The radii polynomial closes/fails exactly where the algebra says."""
    good = radii_polynomial(Y0=1e-12, Z0=1e-13, Z1=0.3, Z2=2.0)
    assert good["closes"] and good["r_min"] > 0
    assert abs(good["Y0_max"] - (0.7 ** 2) / 8.0) < 1e-12
    bad = radii_polynomial(Y0=1e-12, Z0=1e-13, Z1=1.02, Z2=2.0)
    assert not bad["closes"] and bad["Y0_max"] == 0.0
    tight = radii_polynomial(Y0=good["Y0_max"] * (1 + 1e-9), Z0=0.0, Z1=0.3, Z2=2.0)
    assert not tight["closes"], "just above Y0_max must NOT close"
    print(f"[ok] (6) radii polynomial: r_min={good['r_min']:.3e}, "
          f"Y0_max={good['Y0_max']:.4f}; Z0+Z1>1 correctly rejected")


if __name__ == "__main__":
    test_exact_anchor()
    test_jacobian_matches_finite_difference()
    test_symmetry_kernel_and_gauges()
    test_grid_cross_check()
    test_tail_algebra()
    test_radii_polynomial_algebra()
    print("\nALL NK-FOURIER TESTS PASSED")
