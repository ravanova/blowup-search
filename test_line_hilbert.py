"""Unit tests for the whole-line spline-analytic Hilbert transform.

THE CRUX of Phase-2 Spike 0. The decisive check is the exact CLM pair

    f(X) = -4X/(1+4X^2)   -->   H(f)(X) = 2/(1+4X^2)

on a non-uniform (sinh-stretched) whole-line grid. Run:  python test_line_hilbert.py
"""

import numpy as np

from solver.line_hilbert import (
    natural_spline_slopes,
    line_hilbert,
    line_hilbert_matrix,
    _A,
    _B,
)

PI = np.pi


def _sinh_grid(n, c=0.5, rho_max=8.0):
    """Symmetric whole-line grid X = c*sinh(rho), rho uniform on [-rho_max, rho_max].

    Clusters points near X=0 (resolving the profile peak) and reaches
    |X|_max = c*sinh(rho_max); dX ~ X drho gives the CFL-friendly stretch."""
    rho = np.linspace(-rho_max, rho_max, n)
    return c * np.sinh(rho)


def test_spline_slopes_nonuniform():
    """Natural cubic spline slopes recover d/dx sin on a non-uniform grid."""
    x = np.sort(np.concatenate([
        np.linspace(-3, 3, 60),
        np.random.RandomState(0).uniform(-3, 3, 40),
    ]))
    f = np.sin(x)
    fp = natural_spline_slopes(x, f)
    # exclude the two end nodes (natural BC f''=0 biases the boundary slope)
    err = np.abs(fp[2:-2] - np.cos(x[2:-2])).max()
    assert err < 1e-3, f"spline slope error {err:.2e}"
    print(f"[ok] natural spline slopes on non-uniform grid: max err {err:.2e}")


def test_AB_special_values():
    """A, B match their known limits and are continuous across the |s|=0.5 branch."""
    # s -> 1 finite limits
    assert abs(_A(np.array([1.0]))[0] - (-5.0 / (6 * PI))) < 1e-12
    assert abs(_B(np.array([1.0]))[0] - (-1.0 / (6 * PI))) < 1e-12
    # s -> 0 limits are 0
    assert abs(_A(np.array([1e-9]))[0]) < 1e-8
    assert abs(_B(np.array([1e-9]))[0]) < 1e-8
    # branch continuity at |s|=0.5: small-branch and direct-branch agree
    for s0 in (0.5, -0.5):
        eps = 1e-9
        a_lo = _A(np.array([s0 - eps]))[0]   # |s|<0.5 side (if s0=0.5)
        a_hi = _A(np.array([s0 + eps]))[0]
        b_lo = _B(np.array([s0 - eps]))[0]
        b_hi = _B(np.array([s0 + eps]))[0]
        assert abs(a_lo - a_hi) < 1e-9, f"A discontinuous at s={s0}: {a_lo} vs {a_hi}"
        assert abs(b_lo - b_hi) < 1e-9, f"B discontinuous at s={s0}: {b_lo} vs {b_hi}"
    print("[ok] A,B special values and branch continuity")


def test_AB_against_direct_definition():
    """A(s), B(s) match the raw (unstabilized) closed forms at moderate |s|."""
    s = np.array([0.6, 0.7, -0.6, -0.8, 0.9])
    s3 = s ** 3
    log = np.log(np.abs(1.0 - s))
    a_raw = (-5 * s3 - 12 * s ** 2 + 12 * s + 6 * (s3 - 3 * s + 2) * log) / (6 * PI * s3)
    b_raw = (2 * s3 - 9 * s ** 2 + 6 * s + 6 * (s - 1) ** 2 * log) / (6 * PI * s3)
    assert np.abs(_A(s) - a_raw).max() < 1e-12
    assert np.abs(_B(s) - b_raw).max() < 1e-12
    print("[ok] A,B match direct closed form at moderate |s|")


def test_clm_pair_known_answer():
    """THE CRUX: H(-4X/(1+4X^2)) = 2/(1+4X^2) on a stretched whole-line grid."""
    best = None
    for n, c, rho_max in [(1200, 0.5, 8.0), (2400, 0.5, 9.0)]:
        X = _sinh_grid(n, c=c, rho_max=rho_max)
        f = -4.0 * X / (1.0 + 4.0 * X ** 2)
        exact = 2.0 / (1.0 + 4.0 * X ** 2)
        Hf = line_hilbert(X, f)
        # measure error on the resolved core (|X| < 5), excluding boundary nodes
        core = np.abs(X) < 5.0
        core[:3] = core[-3:] = False
        err = np.abs(Hf[core] - exact[core]).max()
        rel = err / np.abs(exact[core]).max()
        print(f"    n={n:5d} c={c} rho_max={rho_max}: max abs err {err:.3e}  rel {rel:.3e}")
        best = rel
    assert best < 1e-2, f"CLM Hilbert pair rel error {best:.3e} exceeds 1% POC target"
    print(f"[ok] CLM known-answer pair recovered to rel {best:.3e} (< 1% POC target)")


def test_resolution_improves():
    """Error decreases under whole-line refinement (both core resolution AND the
    tail-truncation reach M grow together). NOTE: at fixed M the error hits a
    ~1/M truncation floor from the profile's 1/X tail, so both knobs must move —
    that floor, not core resolution, is the dominant term for this profile."""
    errs = []
    for n, rho_max in ((600, 7.0), (1200, 8.5), (2400, 10.0)):
        X = _sinh_grid(n, c=0.5, rho_max=rho_max)
        f = -4.0 * X / (1.0 + 4.0 * X ** 2)
        exact = 2.0 / (1.0 + 4.0 * X ** 2)
        Hf = line_hilbert(X, f)
        core = np.abs(X) < 5.0
        core[:3] = core[-3:] = False
        errs.append(np.abs(Hf[core] - exact[core]).max())
    print(f"    refinement errors: {[f'{e:.2e}' for e in errs]}")
    assert errs[1] < errs[0] and errs[2] < errs[1], f"not converging: {errs}"
    print("[ok] error decreases under whole-line refinement (resolution + reach M)")


def test_matrix_reuse_matches():
    """Prebuilt matrix reproduces the on-the-fly transform exactly."""
    X = _sinh_grid(400, c=0.5, rho_max=7.0)
    f = -4.0 * X / (1.0 + 4.0 * X ** 2)
    M = line_hilbert_matrix(X)
    assert np.abs(line_hilbert(X, f, matrix=M) - line_hilbert(X, f)).max() < 1e-14
    print("[ok] precomputed matrix matches on-the-fly transform")


def test_slope_matrix_matches_sweeps():
    """The cached dense slope OPERATOR reproduces the Thomas sweeps it replaces.

    Route-M swapped `natural_spline_slopes(X, f)` for `slope_matrix(X) @ f` inside the
    relaxation integrators, because profiling put 81% of a Scenario-2 step inside the
    Python sweep loop.  That is a change of association, not of formula, and this is the
    gate that says so -- reported as a MAGNITUDE relative to the slope's own scale, and
    checked on the non-uniform sinh grid the integrators actually use (a uniform grid
    would hide a spacing bug).  Also checks the cache returns the SAME object, since a
    silently rebuilt matrix would cost the speedup without failing anything.
    """
    from solver.line_hilbert import slope_matrix
    worst = 0.0
    for n, c in ((201, 0.35), (401, 0.5), (801, 0.35)):
        X = _sinh_grid(n, c=c, rho_max=7.0)
        S = slope_matrix(X)
        assert slope_matrix(X) is S, "slope_matrix rebuilt instead of hitting the cache"
        for f in (-4.0 * X / (1.0 + 4.0 * X ** 2),
                  np.exp(-0.5 * X ** 2),
                  1.0 / (1.0 + X ** 2) ** 0.75):
            ref = natural_spline_slopes(X, f)
            rel = np.abs(S @ f - ref).max() / max(np.abs(ref).max(), 1e-300)
            worst = max(worst, rel)
    print(f"    worst |S f - sweeps| / |slopes|_inf over 3 grids x 3 fields = {worst:.2e}")
    assert worst < 1e-12, f"slope operator disagrees with the sweeps: {worst:.2e}"
    print("[ok] cached slope operator == the Thomas sweeps it replaces, at rounding")


if __name__ == "__main__":
    test_spline_slopes_nonuniform()
    test_slope_matrix_matches_sweeps()
    test_AB_special_values()
    test_AB_against_direct_definition()
    test_matrix_reuse_matches()
    test_resolution_improves()
    test_clm_pair_known_answer()
    print("\nALL LINE-HILBERT TESTS PASSED")
