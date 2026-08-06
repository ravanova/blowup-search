"""ADVERSARIAL gates for solver/turning_point.py -- Route-TPA, leg 118.

`test_turning_point.py` (6 gates) checks the module's physics on a real, Newton-converged,
non-degenerate profile: the sign and magnitude of the fitted inner/outer exponents against
the predicted `1/a`, quadrature convergence, and the speed-bordering repair's documented
failure.  None of its inputs is degenerate or poisoned.  This file tests the one property
that makes the module's classification safe to trust downstream -- that `critical_radius`
(imported from `solver/collocation_newton.py` into `turning_point.py`'s own namespace, and
the primitive every public function of the module relies on to locate `X_c`) never reports a
turning point that does not exist, and never silently substitutes a spurious one for a real,
further-out crossing.

**Leg 118's gate answered YES.** `critical_radius`'s bracketing test is
`np.sign(E[i+1]) != np.sign(E[i])`, which is weaker than the classical bracketing condition
(the STRICT product inequality `E[i]*E[i+1] < 0`, Bolzano's theorem; `scipy.optimize.brentq`
enforces exactly this and raises `ValueError: f(a) and f(b) must have different signs`
otherwise).  The module's test ALSO fires whenever either endpoint is exactly `0.0` -- a
TANGENCY, where `E` grazes zero without ever actually changing sign.  Since `E` is a
continuous function of `X` evaluated only at grid nodes, a tangency exactly on a node makes
`critical_radius` return a fully finite, plausible `X_c`, and nothing downstream re-validates
it: `homogeneous_far_field` checks only `np.isfinite(Xc)`, which a tangency-produced value
passes trivially, and `inner_mode_exponent`/`log_growth_exponent`/`source_of_the_row` inherit
whatever `X_c` they are handed with no check at all.

**solver/turning_point.py and solver/collocation_newton.py are NOT patched by leg 118** --
the gate's yes-branch escalates, it does not repair.  Gates 4-6 below are GAP-PINS in the
sense of leg 84: they assert the CURRENT unsound classification behaviour so it cannot decay
at the rate of memory, and

    **they must be INVERTED, not weakened, the day a guard lands.**

The repair, when authorised, is a guard on `critical_radius` itself -- require the STRICT
product `E[i]*E[i+1] < 0` (equivalently, treat an exact `0.0` endpoint as its own case rather
than folding it into the sign-difference test) -- not a change to any exponent or constant
the module computes on a genuine crossing, all of which `test_turning_point.py` continues to
own and which this file does not touch.

Gates 1-3 are the CONTROLS that show the module is not universally broken: a real converged
profile's one genuine crossing is found correctly (gate 1); an `E` that truly never crosses
and does not land on a node is correctly reported as no-turning-point (gate 2); NaN/Inf
poisoning is FLAGGED (a `nan` `X_c` or a raised `ValueError`), not silently absorbed into a
finite answer (gate 3).  Gate 7 measures severity: no Newton-converged profile this
repository can currently produce reaches the defect on its own, because the physical
velocity field is monotone on every grid/`a` tested (a monotone function can only cross zero
transversally, never tangentially) -- the defect is latent under every configuration the
repository's own experiments run today, exactly as leg 120 measured for `spectral_utils.py`.

Run: .venv/bin/python test_turning_point_adversarial.py
"""

import json
import os

import numpy as np

import solver.turning_point as tp
from solver.turning_point import (homogeneous_far_field, inner_mode_exponent,
                                  log_growth_exponent, solved_profile, source_of_the_row)
from solver.collocation_newton import critical_radius, effective_speed

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "writeup", "data",
                    "p2_route_tpa_v1_adversarial.json")


def _banked():
    with open(DATA) as f:
        return json.load(f)


# ---------------------------------------------------------------------------


def test_1_CONTROL_real_crossing_is_found():
    """A real, converged profile's one genuine crossing is located correctly."""
    banked = _banked()
    b = banked["g1_positive_control"]
    col, om, c = solved_profile(banked["J_default"], banked["a_default"])
    Xc = critical_radius(col.X, effective_speed(col.X, col.V @ om, c, col.a))
    assert np.isfinite(Xc) and Xc > 0, Xc
    assert abs(Xc - b["Xc_direct"]) < 1e-9, (Xc, b["Xc_direct"])
    p, Xc2 = inner_mode_exponent(col, om, c)
    assert abs(Xc2 - Xc) < 1e-9, (Xc2, Xc)
    assert abs(p - 1.0 / col.a) / (1.0 / col.a) < 0.5, (p, 1.0 / col.a)   # loose: not a physics re-derivation
    print("[ok] (1) CONTROL: a real converged profile's genuine crossing is found at "
          "Xc=%.6f, matching the banked value and this file's own live re-check" % Xc)


def test_2_CONTROL_offgrid_no_crossing_correctly_flagged():
    """E that truly never crosses, and does not land on a node, is correctly Xc=inf."""
    b = _banked()["g2_offgrid_no_crossing_control"]
    assert len(b) >= 5, b
    for row in b:
        assert row["correctly_infinite"], row
        assert row["hff_correctly_raised"], row
    print("[ok] (2) CONTROL: %d/%d off-grid non-crossing constructions correctly report "
          "Xc=inf and homogeneous_far_field correctly raises -- the module is not "
          "universally broken, only at the exact-node tangency" % (len(b), len(b)))


def test_3_CONTROL_nan_inf_are_flagged_not_absorbed():
    """Poisoned E/om produces a flagged nan or a raised ValueError, never a silent finite
    classification."""
    b = _banked()["g3_nan_inf_controls"]
    assert b["nan_at_crossing"]["is_nan"], b["nan_at_crossing"]
    assert b["nan_om_hff"]["correctly_flagged"], b["nan_om_hff"]
    if "distant_inf_does_not_disturb_crossing" in b:
        assert b["distant_inf_does_not_disturb_crossing"]["unchanged"], b
    # live re-check: a fresh NaN at the crossing is caught the same way
    col, om, c = solved_profile(_banked()["J_default"], _banked()["a_default"])
    U = col.V @ om
    E = effective_speed(col.X, U, c, col.a)
    i = int(np.argmin(np.abs(E)))
    E2 = E.copy(); E2[max(i - 1, 0)] = np.nan
    assert np.isnan(critical_radius(col.X, E2))
    print("[ok] (3) CONTROL: NaN at or near the real crossing propagates to a flagged "
          "nan X_c (never a silently-plausible finite one), and homogeneous_far_field "
          "raises on a NaN-poisoned om")


def test_4_GAPPIN_ongrid_tangency_is_a_silent_false_positive():
    """THE DEFECT.  E touches exactly 0.0 at a grid node and never actually changes
    sign; critical_radius reports a finite Xc anyway, and every downstream function
    accepts it with zero warnings and zero exceptions."""
    b = _banked()["g4_ongrid_tangency_defect"]
    assert len(b) >= 8, b
    n_silent = 0
    for row in b:
        assert row["E_exactly_zero_at_touch"], row
        assert row["E_single_signed_elsewhere"], row     # ground truth: NOT a crossing
        if row["silently_finite_not_inf"]:
            n_silent += 1
            assert row["hff_meta"]["raised"] is None, row
            assert row["hff_meta"]["n_warnings"] == 0, row
            assert row["hff_h_all_finite"], row
            assert row["source_of_the_row_meta"]["raised"] is None, row
    assert n_silent == len(b), (n_silent, len(b))    # EVERY tangency case is silently wrong
    print("[ok] (4) GAP-PIN: %d/%d on-grid-node tangencies (E touches 0.0, provably never "
          "changes sign) produce a SILENT FINITE Xc from critical_radius, accepted with "
          "zero warnings by homogeneous_far_field/source_of_the_row.  "
          "INVERT THIS GATE, DO NOT WEAKEN IT, when a strict-sign-change guard lands"
          % (n_silent, len(b)))


def test_5_GAPPIN_spurious_touch_masks_the_real_crossing():
    """THE SHARPEST INSTANCE.  A spurious tangency sits before a real, well-separated
    transversal crossing; critical_radius reports the spurious point and MISSES the real
    turning point entirely."""
    b = _banked()["g5_composite_masks_real_crossing"]
    assert len(b) >= 3, b
    worst_ratio = 0.0
    for row in b:
        assert row["reported_equals_spurious_touch"], row
        assert row["true_over_reported_ratio"] is not None, row
        assert row["true_over_reported_ratio"] > 1.0, row     # reported is EARLIER than true
        worst_ratio = max(worst_ratio, row["true_over_reported_ratio"])
        assert row["hff_meta"]["raised"] is None, row
        assert row["hff_finite"], row
    assert worst_ratio > 5.0, worst_ratio
    print("[ok] (5) GAP-PIN: a spurious tangency placed before a real crossing hijacks "
          "the result in %d/%d constructions; the real turning point is missed by up to "
          "%.1fx, with a fully finite, unflagged output.  INVERT WHEN GUARDED"
          % (len(b), len(b), worst_ratio))


def test_6_GAPPIN_live_reproduction_no_banked_dependency():
    """Reproduces gate 4's mechanism LIVE, independent of the banked JSON, so this gate
    cannot silently go stale if the JSON is ever regenerated differently."""
    col, om, c = solved_profile(60, 0.3)
    idx = len(col.X) // 2
    X0 = float(col.X[idx])
    real_es = tp.effective_speed

    def tangent_on_node(Xarr, U, c_, a_):
        Xarr = np.asarray(Xarr, dtype=float)
        return (Xarr - X0) ** 2

    tp.effective_speed = tangent_on_node
    try:
        E = tangent_on_node(col.X, None, c, col.a)
        assert E[idx] == 0.0 and np.all(E >= 0.0), E
        Xc = critical_radius(col.X, E)
        assert np.isfinite(Xc), Xc                 # THE DEFECT: should be inf
        assert abs(Xc - X0) < 1e-9, (Xc, X0)
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            X, h, Xc2 = homogeneous_far_field(col, om, c, n=201)
        assert len(w) == 0, [str(x.message) for x in w]
        assert np.isfinite(h).all(), h
        p, Xc3 = inner_mode_exponent(col, om, c, n=201)
        assert np.isfinite(p), p
    finally:
        tp.effective_speed = real_es
    print("[ok] (6) GAP-PIN live reproduction (no JSON dependency): a fresh on-node "
          "tangency at X0=%.6f reproduces Xc=%.6f (finite, should be inf), and "
          "homogeneous_far_field returns with ZERO warnings" % (X0, Xc))


def test_7_natural_reachability_is_latent_today():
    """SEVERITY.  No currently-computable, Newton-converged profile's own velocity field
    has an interior local extremum -- the only way a real physics run could organically
    produce the tangency, since a monotone field crosses only transversally.  The defect
    is latent under every configuration the repository's own experiments run."""
    b = _banked()["g6_natural_reachability"]
    assert b["any_real_profile_has_interior_extremum"] is False, b
    for row in b["rows"]:
        assert row["U_monotonic"], row
    print("[ok] (7) SEVERITY: 0/%d (J, a) configurations produce a profile whose own "
          "velocity field has an interior extremum -- the defect is LATENT: it requires "
          "an adversarially-constructed E, not merely an unlucky real solve, to reach "
          "under this repository's current usage" % len(b["rows"]))


def test_8_matrix_functions_crash_loudly_not_silently():
    """The matrix-inversion side of the module (graded_norm_by_radius, bordered_norm,
    square_bordered_smin) is NOT the classification primitive, but the gate covers the
    whole module.  Under NaN poisoning these raise (LinAlgError) rather than returning a
    silently-plausible finite number -- an ugly failure mode, but a FLAGGED one."""
    b = _banked()["g8_matrix_functions_under_poison"]
    nan_row = next(r for r in b if r["case"] == "NaN_om")
    for fname in ("graded_norm_by_radius", "bordered_norm", "square_bordered_smin"):
        assert nan_row[fname]["raised"] is not None, (fname, nan_row[fname])
        assert not nan_row[fname]["silently_finite"], (fname, nan_row[fname])
    clean_row = next(r for r in b if r["case"] == "clean")
    for fname in ("graded_norm_by_radius", "bordered_norm", "square_bordered_smin"):
        assert clean_row[fname]["raised"] is None, (fname, clean_row[fname])
    print("[ok] (8) CONTROL: the matrix-inversion functions raise LinAlgError under NaN "
          "poisoning (loud, not silent) and return normally on the clean profile")


def test_9_the_banked_verdict_is_the_one_this_file_asserts():
    b = _banked()
    assert b["gate"].startswith("Under an adversarial battery"), b["gate"]
    assert len(b["g4_ongrid_tangency_defect"]) >= 8
    assert b["g6_natural_reachability"]["any_real_profile_has_interior_extremum"] is False
    print("[ok] (9) writeup/data/p2_route_tpa_v1_adversarial.json banks the full battery "
          "this file re-checks; gate answer recorded in experiments/journal/leg_118.md "
          "as YES -- ESCALATE, do not patch")


if __name__ == "__main__":
    test_1_CONTROL_real_crossing_is_found()
    test_2_CONTROL_offgrid_no_crossing_correctly_flagged()
    test_3_CONTROL_nan_inf_are_flagged_not_absorbed()
    test_4_GAPPIN_ongrid_tangency_is_a_silent_false_positive()
    test_5_GAPPIN_spurious_touch_masks_the_real_crossing()
    test_6_GAPPIN_live_reproduction_no_banked_dependency()
    test_7_natural_reachability_is_latent_today()
    test_8_matrix_functions_crash_loudly_not_silently()
    test_9_the_banked_verdict_is_the_one_this_file_asserts()
    print("\n9/9 TURNING-POINT ADVERSARIAL GATES PASSED "
          "(gate answer: YES -- escalated, module unpatched)")
