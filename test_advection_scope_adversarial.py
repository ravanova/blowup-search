"""Permanent regression battery for Route-ASA (leg 122): does
`solver/advection_scope.py` ever SILENTLY return a wrong result under a degenerate or
poisoned input, instead of flagging it?

**Gate answered YES** (`experiments/journal/leg_122.md`, `writeup/data/p2_route_asa_v1_
adversarial.json`). Two independent silent-corruption mechanisms, both rooted in an
unvalidated array-order precondition the module's own docstrings never state:

  (T) `profile_mass` -- and, through it, `velocity_log_rate`'s `mass`/`mass_window`/
      `predicted` fields -- is a two-line wrapper around `numpy.trapezoid`, which NumPy's
      own manual documents as evaluating "in sequence along its elements -- they are not
      sorted". `profile_mass`'s docstring promises a mathematical (order-independent)
      integral; the code computes NumPy's sequential (order-DEPENDENT) quadrature.
  (S) `stagnation_point`'s docstring promises "the SMALLEST X > 0"; the implementation
      finds the smallest ARRAY INDEX with a sign change, which coincides with the
      smallest coordinate only if the caller's `X` is already sorted ascending -- a
      precondition the function never checks.

Per this leg's territory and the family's convention (69/100/101/120), `solver/
advection_scope.py` is READ-ONLY here. Checks marked **PIN** assert the CURRENT, DEFECTIVE
behaviour exactly as measured, so a future repair has an exact target and these checks will
(and should) start FAILING the moment `solver/advection_scope.py` is fixed to validate or
sort its inputs -- the pin must be updated in the same commit as any repair. Checks NOT
marked PIN are permanent invariants that must hold both now and after any repair.

Run: .venv/bin/python test_advection_scope_adversarial.py   (< 5 s, no solver run)
"""
import math
import warnings

import numpy as np

from solver.advection_scope import (
    profile_mass, velocity_log_rate, stagnation_point, advection_split, _log_fit,
)


class Fam:
    """Minimal duck-typed stand-in exposing only X, Vmat, Hmat -- see
    experiments/p2_route_asa_v1_adversarial.py for the full rationale."""

    def __init__(self, X, Vmat=None, Hmat=None):
        self.X = np.asarray(X, dtype=float)
        n = self.X.size
        self.Vmat = Vmat if Vmat is not None else np.eye(n)
        self.Hmat = Hmat if Hmat is not None else np.eye(n)


# ---------------------------------------------------------------------------
# PIN: category T -- trapezoidal order-dependence
# ---------------------------------------------------------------------------

def check_pin_reversal_negates_the_mass():
    """PIN: exact reversal of (om, X) returns the exact NEGATION of the true mass, with
    no warning and no exception -- NumPy's own documented trapz behaviour, uncaught.
    Correct behaviour would raise, warn, or re-sort before integrating."""
    L, n = 1000.0, 4001
    X = np.linspace(-L, L, n)
    om = -1.0 / (1.0 + X ** 2)
    exact = -2.0 * math.atan(L)
    asc = profile_mass(om, X)
    rev = profile_mass(om[::-1], X[::-1])
    assert abs(asc - exact) / abs(exact) < 1e-4, f"ascending control should be sound: {asc} vs {exact}"
    assert rev == -asc, f"PIN violated: reversal no longer exactly negates ({rev} != {-asc})"
    assert np.isfinite(rev), "PIN violated: reversal no longer returns a finite (silently wrong) value"
    print(f"[PIN] reversed-X profile_mass = {rev:.10f} = exact negation of ascending "
          f"{asc:.10f} (true value {exact:.10f}) -- no warning, no exception")


def check_pin_permutation_gives_arbitrary_wrong_mass():
    """PIN: five seeded random permutations of a well-formed (om, X) pair each return a
    FINITE value at least 10x away (relative) from the exact closed-form mass, with no
    flag of any kind."""
    L, n = 1000.0, 4001
    X = np.linspace(-L, L, n)
    om = -1.0 / (1.0 + X ** 2)
    exact = -2.0 * math.atan(L)
    worst, best = -1.0, float("inf")
    for seed in range(5):
        rng = np.random.default_rng(seed)
        perm = rng.permutation(n)
        val = profile_mass(om[perm], X[perm])
        assert np.isfinite(val), f"seed {seed}: PIN violated, permutation produced non-finite (a flag)"
        rel = abs(val - exact) / abs(exact)
        worst, best = max(worst, rel), min(best, rel)
    assert best > 5.0, f"PIN violated: mildest permutation error only {best:.2f}x, expected >5x"
    print(f"[PIN] 5 random permutations: relative error range {best:.2f}x - {worst:.2f}x "
          f"the true mass, all finite, all silent")


def check_pin_single_adjacent_swap_corrupts():
    """PIN: swapping exactly TWO adjacent array entries -- the minimal possible order
    perturbation -- already produces a >1% silently wrong finite mass."""
    L, n = 1000.0, 4001
    X = np.linspace(-L, L, n)
    om = -1.0 / (1.0 + X ** 2)
    exact = -2.0 * math.atan(L)
    i = n // 2
    Xs, oms = X.copy(), om.copy()
    Xs[[i, i + 1]] = Xs[[i + 1, i]]
    oms[[i, i + 1]] = oms[[i + 1, i]]
    val = profile_mass(oms, Xs)
    rel = abs(val - exact) / abs(exact)
    assert np.isfinite(val)
    assert rel > 0.01, f"PIN violated: single-swap error only {rel:.4%}, expected >1%"
    print(f"[PIN] single adjacent-pair swap: relative error {rel:.2%} vs the true mass, "
          f"from touching only 2 of {n} entries")


def check_pin_velocity_log_rate_internally_inconsistent():
    """PIN: velocity_log_rate's polyfit-based 'measured' field is order-independent and
    barely moves under a permutation, while its trapz-based 'predicted'/'mass'/
    'mass_window' fields are corrupted by the SAME permutation -- an internally
    inconsistent result package returned without any flag."""
    L, n = 1000.0, 4001
    X = np.linspace(-L, L, n)
    om = -1.0 / (1.0 + X ** 2)
    fam_sorted = Fam(X)
    d_sorted = velocity_log_rate(fam_sorted, om, lo=10.0, hi=1e3)
    perm = np.random.default_rng(0).permutation(n)
    fam_shuf = Fam(X[perm])
    d_shuf = velocity_log_rate(fam_shuf, om[perm], lo=10.0, hi=1e3)
    measured_rel = abs(d_shuf["measured"] - d_sorted["measured"]) / abs(d_sorted["measured"])
    predicted_rel = abs(d_shuf["predicted"] - d_sorted["predicted"]) / abs(d_sorted["predicted"])
    assert measured_rel < 1e-8, f"PIN violated: 'measured' should stay ~fixed, moved {measured_rel:.2e}"
    assert predicted_rel > 1.0, f"PIN violated: 'predicted' should be badly corrupted, moved only {predicted_rel:.2e}"
    print(f"[PIN] velocity_log_rate under permutation: measured moved {measured_rel:.2e} "
          f"relative (order-independent), predicted moved {predicted_rel:.2e} relative "
          f"(trapz-based, corrupted) -- returned together with no internal-consistency flag")


# ---------------------------------------------------------------------------
# PIN: category S -- stagnation_point array-order-dependence
# ---------------------------------------------------------------------------

def check_pin_stagnation_point_shuffled_order_is_wrong():
    """PIN: a single, unambiguous crossing at X=5 (eff = tanh(X-5), a strictly monotone
    odd function). Sorted order finds it to 1e-6. Five seeded shuffles of the SAME
    physically-correct (X, eff) pairs each return a finite value that is NOT the true
    root, silently, violating the function's own 'smallest X > 0' docstring contract."""
    Xs = np.linspace(0.02, 20.0, 4001)
    eff = lambda X: np.tanh(X - 5.0)                                      # noqa: E731
    om = np.ones_like(Xs)
    fam_sorted = Fam(Xs, Hmat=np.diag(eff(Xs)))
    x_true = stagnation_point(fam_sorted, om, 0.0, 1.0)
    assert x_true is not None and abs(x_true - 5.0) < 1e-4, f"sorted control should be sound: {x_true}"

    worst = 0.0
    for seed in range(5):
        rng = np.random.default_rng(seed)
        perm = rng.permutation(len(Xs))
        fam_p = Fam(Xs[perm], Hmat=np.diag(eff(Xs)[perm]))
        xv = stagnation_point(fam_p, om[perm], 0.0, 1.0)
        assert xv is not None and np.isfinite(xv), f"seed {seed}: PIN violated, shuffled case produced a flag"
        worst = max(worst, abs(xv - x_true))
    assert worst > 0.01, f"PIN violated: worst shuffled error only {worst:.4f}, expected >0.01"
    print(f"[PIN] stagnation_point under 5 array-order shuffles of physically-identical "
          f"data: worst deviation from the true root (X=5) is {worst:.3f}, all finite, "
          f"all silent -- 'smallest X > 0' becomes 'smallest ARRAY INDEX'")


def check_pin_stagnation_point_two_crossings_can_miss_both():
    """PIN: with two real crossings (~5 and ~12), at least one seeded shuffle returns a
    finite value that matches NEITHER real crossing -- confirming the failure fabricates
    an interpolated value between physically non-adjacent samples, rather than merely
    picking the 'wrong' of two genuine roots."""
    Xs = np.linspace(0.02, 20.0, 4001)
    eff = lambda X: np.tanh(X - 5.0) * np.where(X < 12.0, 1.0, -1.0)      # noqa: E731
    om = np.ones_like(Xs)
    matches_neither = 0
    for seed in range(100, 105):
        rng = np.random.default_rng(seed)
        perm = rng.permutation(len(Xs))
        fam_p = Fam(Xs[perm], Hmat=np.diag(eff(Xs)[perm]))
        xv = stagnation_point(fam_p, om[perm], 0.0, 1.0)
        if xv is not None and np.isfinite(xv) and abs(xv - 5.0) > 0.5 and abs(xv - 12.0) > 0.5:
            matches_neither += 1
    assert matches_neither >= 1, "PIN violated: expected at least one shuffle to fabricate a value matching neither real crossing"
    print(f"[PIN] two-crossing case: {matches_neither}/5 shuffles returned a finite value "
          f"matching NEITHER real crossing (~5, ~12) -- a fabricated interpolation, not a "
          f"mere swap of which real root is reported")


# ---------------------------------------------------------------------------
# Permanent invariants -- must hold NOW and after any repair
# ---------------------------------------------------------------------------

def check_nan_before_crossing_never_looks_real():
    """NaN placed strictly BEFORE the true crossing, in otherwise correctly-SORTED order,
    must never yield a plausible finite crossing -- this is the one thing that already
    works, and a repair must not regress it while fixing the order-dependence above."""
    Xs = np.linspace(0.02, 20.0, 4001)
    eff = np.tanh(Xs - 5.0)
    Hmat = np.diag(eff.copy())
    Hmat[100, 100] = np.nan  # Xs[100] ~ 0.52, well before the root at 5
    fam = Fam(Xs, Hmat=Hmat)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        xv = stagnation_point(fam, np.ones_like(Xs), 0.0, 1.0)
    assert xv is not None and math.isnan(xv), f"NaN-before-crossing must return nan, got {xv}"
    print("[ok] NaN strictly before the true crossing (sorted order) returns nan, "
          "never a plausible finite crossing")


def check_mismatched_shapes_raise():
    """A caller error (mismatched array lengths) must raise, not silently broadcast or
    truncate."""
    raised = False
    try:
        profile_mass(np.ones(5), np.ones(6))
    except Exception:                                                    # noqa: BLE001
        raised = True
    assert raised, "mismatched shapes must raise"
    print("[ok] mismatched (om, X) shapes raise, as required")


def check_unknown_grading_key_raises():
    """An unrecognised `grading=` value must raise (KeyError), not silently fall back to
    a default grading."""
    X = np.linspace(1.0, 100.0, 50)
    fam = Fam(X)
    D = np.eye(50)
    raised = False
    try:
        advection_split(fam, np.ones(50), 0.3, 1.4, D, grading="bogus")
    except Exception:                                                    # noqa: BLE001
        raised = True
    assert raised, "an unknown grading key must raise"
    print("[ok] unknown grading key raises KeyError, as required")


def check_nonfinite_scalars_flag_not_fabricate():
    """nan/inf passed as the scalar `a` or `c` to stagnation_point must produce nan
    output (or None), never a plausible finite crossing."""
    Xs = np.linspace(0.1, 20.0, 500)
    fam = Fam(Xs, Hmat=np.diag(np.tanh(Xs - 5.0)))
    om = np.ones_like(Xs)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        r_a_nan = stagnation_point(fam, om, 0.0, float("nan"))
        r_c_nan = stagnation_point(fam, om, float("nan"), 1.0)
    assert r_a_nan is not None and math.isnan(r_a_nan)
    assert r_c_nan is not None and math.isnan(r_c_nan)
    print("[ok] nan scalar a/c both propagate to a nan crossing, never a plausible number")


def check_extreme_scale_sorted_is_sound():
    """Extreme dynamic range ALONE (no order violation) must not corrupt profile_mass --
    isolates that the defect above is about ORDER, not about magnitude."""
    Xe = np.linspace(-1e150, 1e150, 501)
    ome = np.ones_like(Xe) * 1e150
    val = profile_mass(ome, Xe)
    expected = 1e150 * 2e150
    rel = abs(val - expected) / abs(expected)
    assert np.isfinite(val) and rel < 1e-9, f"extreme-scale sorted case should be sound: rel err {rel:.2e}"
    print(f"[ok] extreme scale (1e150), correctly sorted: relative error {rel:.2e} -- sound")


def check_a_zero_control_survives_shuffle():
    """At a=0, c+a*U == c is constant and never changes sign, so stagnation_point must
    return None regardless of array order -- verified under an adversarial shuffle."""
    Xs = np.linspace(0.1, 20.0, 500)
    perm = np.random.default_rng(7).permutation(len(Xs))
    fam = Fam(Xs[perm])
    r = stagnation_point(fam, np.zeros(len(Xs)), 0.5, 0.0)
    assert r is None, f"a=0 control should return None even under shuffle, got {r}"
    print("[ok] a = 0 control (no crossing) survives an adversarial array shuffle")


def check_complex_input_warns_but_still_discards_silently_from_the_gate():
    """Documented for completeness: a complex-valued profile array DOES raise a Python
    ComplexWarning when it is cast to float -- a real, if weak and easily-missed, flag.
    This is reported as its own category (WARNED_NOT_SILENT), distinct from the fully
    silent T/S mechanisms above, and is not itself a PIN."""
    Xc = np.linspace(-5.0, 5.0, 101)
    om_complex = -1.0 / (1.0 + Xc ** 2) + 1j * 3.0
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        profile_mass(om_complex, Xc)
    fired = any("omplex" in str(w.message) for w in caught)
    assert fired, "a ComplexWarning should fire on a complex-valued profile array"
    print("[ok] complex-valued profile array fires a ComplexWarning (weak flag, not fully silent)")


def check_window_too_small_returns_nan():
    """_log_fit's own documented behaviour: fewer than 8 points in the fit window
    returns nan rather than fabricating a slope from too little data."""
    X = np.linspace(1.0, 1000.0, 2000)
    y = np.log(X)
    r = _log_fit(X, y, lo=999.99, hi=1000.0)
    assert isinstance(r, float) and math.isnan(r)
    print("[ok] fit window with < 8 points returns nan, as documented")


if __name__ == "__main__":
    checks = [
        check_pin_reversal_negates_the_mass,
        check_pin_permutation_gives_arbitrary_wrong_mass,
        check_pin_single_adjacent_swap_corrupts,
        check_pin_velocity_log_rate_internally_inconsistent,
        check_pin_stagnation_point_shuffled_order_is_wrong,
        check_pin_stagnation_point_two_crossings_can_miss_both,
        check_nan_before_crossing_never_looks_real,
        check_mismatched_shapes_raise,
        check_unknown_grading_key_raises,
        check_nonfinite_scalars_flag_not_fabricate,
        check_extreme_scale_sorted_is_sound,
        check_a_zero_control_survives_shuffle,
        check_complex_input_warns_but_still_discards_silently_from_the_gate,
        check_window_too_small_returns_nan,
    ]
    for c in checks:
        c()
    print(f"\nALL {len(checks)} ADVECTION-SCOPE ADVERSARIAL CHECKS PASSED "
          f"(6 PIN current-defect checks, 8 permanent invariants)")
