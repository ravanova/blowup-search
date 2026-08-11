"""Tests for solver/dssp_basis.py -- Route-DSSP brick B2 (DSSP-BASIS).

Run: .venv/bin/python test_dssp_basis.py
"""
import numpy as np

from solver.dssp_basis import (
    DEFAULT_L,
    boundary_block,
    boundary_block_v,
    cheb_coeffs,
    modes_for_rel_tol,
    smooth_control_v,
    smooth_control_X,
    tail_truncation_error,
    v_of_X,
    X_of_v,
)


def test_kappa0_is_a_polynomial_on_X_and_terminates():
    """(1-X)^{1-i*0} = (1-X)^1 is degree-1; the plain-X Chebyshev coefficients
    past n=2 must vanish (leg 313's own kappa=0 control, reproduced)."""
    a = cheb_coeffs(lambda X: boundary_block(X, 0.0), 1 << 12)
    assert np.max(a[3:]) < 1e-10, f"kappa=0 did not terminate: {np.max(a[3:]):.3e}"
    print("[ok] kappa=0 control terminates on the plain-X basis")


def test_baseline_reproduces_leg313_smooth_control_separation():
    """FIRST, before anything else: reproduce leg 313's own 82.3x smooth-control
    separation on the plain-X instrument, exactly (same function, same N, same
    1e-6 relative-tail criterion) -- the sanity check that this leg is working
    against the SAME baseline leg 313/343 measured, not a re-derivation."""
    N = 1 << 20
    n_smooth = modes_for_rel_tol(smooth_control_X, N, 1e-6)
    n_k1 = modes_for_rel_tol(lambda X: boundary_block(X, 1.0), N, 1e-6)
    assert n_smooth == 10, f"smooth control modes drifted: {n_smooth} (expected 10)"
    assert n_k1 == 823, f"kappa=1 baseline modes drifted: {n_k1} (expected 823)"
    sep = n_k1 / n_smooth
    assert abs(sep - 82.3) < 0.1, f"separation drifted: {sep:.1f}x (expected 82.3x)"
    print(f"[ok] baseline reproduced: smooth={n_smooth}, kappa=1={n_k1}, "
          f"separation={sep:.1f}x")


def test_baseline_matches_leg313_full_table():
    """The plain-X baseline at every measured kappa row, to the exact mode
    count leg 313 banked."""
    N = 1 << 20
    expected = {1.0: 823, 2.0: 1482, 5.0: 3564, 10.0: 7086, 20.0: 14149}
    for kap, want in expected.items():
        got = modes_for_rel_tol(lambda X, kap=kap: boundary_block(X, kap), N, 1e-6)
        assert got == want, f"kappa={kap}: got {got}, leg 313 banked {want}"
    print(f"[ok] full baseline table matches leg 313's banked numbers exactly: "
          f"{expected}")


def test_enriched_basis_resolves_at_lower_mode_count():
    """The whole gate: does the enriched (log + algebraic) compactified basis
    resolve the boundary block at a LOWER mode count than the plain-X
    baseline, at the SAME 1e-6 truncation, on a SINGLE fixed map scale L
    (no per-kappa tuning)?"""
    N = 1 << 16
    baseline = {1.0: 823, 2.0: 1482, 5.0: 3564, 10.0: 7086, 20.0: 14149}
    for kap, base_n in baseline.items():
        n = modes_for_rel_tol(lambda v, kap=kap: boundary_block_v(v, kap), N, 1e-6)
        assert 0 < n < base_n, (
            f"kappa={kap}: enriched basis did not beat the baseline "
            f"({n} vs {base_n})")
        factor = base_n / n
        assert factor > 5.0, f"kappa={kap}: enrichment factor too small ({factor:.1f}x)"
    print("[ok] enriched basis beats the plain-X baseline at every measured kappa, "
          "single fixed L")


def test_enrichment_is_stable_under_resolution_refinement():
    """The enriched-basis mode counts must not be an artefact of the array
    size (leg 313's own S3.7 lesson, carried here as a control on the new
    instrument)."""
    for N in (1 << 14, 1 << 15, 1 << 16, 1 << 17):
        n = modes_for_rel_tol(lambda v: boundary_block_v(v, 20.0), N, 1e-6)
        assert n == 496, f"N={N}: kappa=20 enriched mode count drifted to {n} (expected 496)"
    print("[ok] enriched kappa=20 mode count (496) stable across a 8x resolution range")


def test_falsification_control_smooth_function_gets_worse_under_the_map():
    """A control that CAN come out either way (lesson 90): a function with NO
    boundary singularity has nothing for the enrichment to buy. If the
    enriched basis silently helped EVERYTHING, the comparison above would be
    meaningless. It must instead cost MORE modes under the v-map than the
    plain-X basis needs directly, because the map compresses an unbounded
    u-domain into the same finite interval for no reason."""
    N = 1 << 16
    n_direct = modes_for_rel_tol(smooth_control_X, N, 1e-6)
    n_mapped = modes_for_rel_tol(lambda v: smooth_control_v(v), N, 1e-6)
    assert n_direct == 10
    assert n_mapped > n_direct, (
        f"falsification control did not fail as required: mapped ({n_mapped}) "
        f"<= direct ({n_direct})")
    print(f"[ok] falsification control: smooth function costs MORE under the map "
          f"({n_mapped} vs {n_direct} direct) -- the enrichment is not a free lunch")


def test_forward_and_inverse_maps_are_consistent():
    """v_of_X and X_of_v must be inverses of one another away from the
    endpoint singularity itself."""
    X = np.linspace(0.01, 0.95, 37)
    v = v_of_X(X, DEFAULT_L)
    X2 = X_of_v(v, DEFAULT_L)
    assert np.max(np.abs(X2 - X)) < 1e-9, \
        f"map round-trip failed, max err {np.max(np.abs(X2 - X)):.3e}"
    print("[ok] X -> v -> X round-trips to <1e-9")


def test_tail_truncation_error_is_monotone_nonincreasing():
    a = cheb_coeffs(lambda X: boundary_block(X, 5.0), 1 << 10)
    t = tail_truncation_error(a)
    assert np.all(np.diff(t) <= 1e-15), "tail sum must be non-increasing in n"
    print("[ok] tail truncation sum is monotone non-increasing")


if __name__ == "__main__":
    test_kappa0_is_a_polynomial_on_X_and_terminates()
    test_baseline_reproduces_leg313_smooth_control_separation()
    test_baseline_matches_leg313_full_table()
    test_enriched_basis_resolves_at_lower_mode_count()
    test_enrichment_is_stable_under_resolution_refinement()
    test_falsification_control_smooth_function_gets_worse_under_the_map()
    test_forward_and_inverse_maps_are_consistent()
    test_tail_truncation_error_is_monotone_nonincreasing()
    print("\nALL DSSP-BASIS (B2) TESTS PASSED")
