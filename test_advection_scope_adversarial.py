"""Leg 122 / Route-ASA -- the adversarial regression battery for solver/advection_scope.py.

THE GATE (DIRECTION.md:2782-2785, verbatim)
-------------------------------------------
Under an adversarial battery of degenerate or poisoned inputs, does
solver/advection_scope.py ever silently return a wrong result instead of flagging the
input?
  yes -> Silent-corruption gap; report the exact failing case; escalate, do not patch.
  no  -> Confirmed robust; bank the battery as a permanent regression test.

IT ANSWERED YES.  `solver/advection_scope.py` is byte-identical to this leg's merge base:
the leg had no patch authority under its own gate.  Six gates below therefore PIN OPEN
DEFECTS -- they assert the WRONG behaviour, on purpose, so that the day someone repairs
the module these tests FAIL and say so.  Each is marked `PINS AN OPEN DEFECT`.  **A
failure of one of those six is the intended signal of a repair, and must be answered by
deleting the pin and re-stating the gate -- never by loosening a tolerance.**

The other seven gates are ordinary soundness gates: they assert behaviour the module
gets RIGHT, and must keep passing.

WHAT "TRUE" MEANS FOR THE FAR-FIELD PROBES
------------------------------------------
The module labels the keys of `transport_at` / `stretch_at` as the weighted piece at
`X = 1e1, 1e2, 1e3, 1e4` (lines 184-187).  On the DEFAULT construction path the family is
the sinh grid `X = 0.5 sinh(rho)`, `rho_max = 8` (solver/gclm_family.py:102-110), whose
last node is `~745.24` -- so two of those four keys have no referent, and `np.interp`
clamps instead of saying so (lesson 73).

Numbers are pinned at RELATIVE tolerance, not bitwise: the Newton solve is not
bit-reproducible across BLAS thread counts (`c` moves in the 11th significant figure
between 1 and 4 threads).  The CLAMPING identities are pinned EXACTLY, because they are
properties of `np.interp` and the grid, not of the solve.

Run: python test_advection_scope_adversarial.py    (no scipy, no pytest; ~23 s)

(LAPACK prints a few "DLASCL parameter number 4 had an illegal value" lines to stderr from
gate 12's deliberate `lo = -5` probe -- that is the least-squares fit refusing `log` of a
negative abscissa, which is the behaviour the gate asserts.)
"""

import warnings

import numpy as np

from solver.advection_scope import (advection_split, grading_comparison,
                                    profile_mass, stagnation_point, velocity,
                                    velocity_log_rate)
from solver.profile_newton import TwoScaleNewton, derivative_matrix

ALPHA = 1.4          # the operating point of v8-v10, and of test_advection_scope.py
N = 801
RTOL = 1e-6          # BLAS-thread-count slack on every solve-derived number

_CACHE = {}


def _solved(a, rho_max):
    key = (a, rho_max)
    if key not in _CACHE:
        nw = TwoScaleNewton(a=a, n=N, rho_max=rho_max)
        r = nw.solve()
        assert r["converged"], f"substrate failed to converge at a={a}"
        assert r["relres"] < 1e-10, f"substrate relres {r['relres']:.3e} at a={a}"
        _CACHE[key] = (nw.fam, r["Omega"], float(r["c"]), derivative_matrix(nw.fam))
    return _CACHE[key]


def _close(got, want, rtol=RTOL):
    return abs(got - want) <= rtol * max(abs(want), 1e-300)


# ===========================================================================
# (1) PINS AN OPEN DEFECT -- np.interp clamps past the last node, silently
# ===========================================================================
def test_far_field_probe_fabricates_values_past_the_grid():
    fam, om, c, D = _solved(0.3, 8.0)
    X_max = float(fam.X.max())
    assert _close(X_max, 745.2394128947751, 1e-12), X_max

    sp = advection_split(fam, om, 0.3, ALPHA, D)
    t, s = sp["transport_at"], sp["stretch_at"]

    beyond = [q for q in (1e1, 1e2, 1e3, 1e4) if q > X_max]
    assert beyond == [1e3, 1e4], beyond

    # PINNED DEFECT: both out-of-grid keys are EXACTLY the last node's value, and
    # so exactly equal to each other -- four fabricated numbers per call.
    last_t, last_s = float(sp["transport"][-1]), float(sp["stretch"][-1])
    assert t[1e3] == t[1e4] == last_t, (t[1e3], t[1e4], last_t)
    assert s[1e3] == s[1e4] == last_s, (s[1e3], s[1e4], last_s)
    assert t[1e4] - t[1e3] == 0.0
    assert s[1e4] - s[1e3] == 0.0

    # the magnitude, on the converged a=0.3 profile
    assert _close(t[1e4], 2.2906076249428438), t[1e4]
    assert _close(s[1e4], 0.00384032871440196), s[1e4]

    # and it is silent: no warning of any category is raised
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        advection_split(fam, om, 0.3, ALPHA, D)
    assert [x.category.__name__ for x in w] == [], [x.category.__name__ for x in w]
    print("(1) PINNED DEFECT: 4 of 8 far-field values fabricated per call "
          f"(X_max={X_max:.2f}; keys 1e3,1e4 both = {last_t:.10f})")


# ===========================================================================
# (2) THE CONTROL FOR (1), AND IT CAN COME OUT EITHER WAY
# ===========================================================================
def test_control_grid_that_contains_the_keys_disagrees_out_of_grid_only():
    fam8, om8, c8, D8 = _solved(0.3, 8.0)
    fam12, om12, c12, D12 = _solved(0.3, 12.0)
    assert float(fam12.X.max()) > 1e4, fam12.X.max()

    t8 = advection_split(fam8, om8, 0.3, ALPHA, D8)["transport_at"]
    t12 = advection_split(fam12, om12, 0.3, ALPHA, D12)["transport_at"]

    rel = {q: (t8[q] - t12[q]) / t12[q] for q in (1e2, 1e3, 1e4)}
    # IN-grid key: the two grids agree -- so (1) is not flagging arithmetic
    assert abs(rel[1e2]) < 0.02, rel[1e2]
    assert _close(rel[1e2], 0.005899392815269795, 1e-3), rel[1e2]
    # OUT-of-grid key: a quarter of the value is missing, and it is missing
    # DOWNWARD -- the module under-states the very divergence it exists to show
    assert rel[1e4] < -0.2, rel[1e4]
    assert _close(rel[1e4], -0.25941186719122694, 1e-3), rel[1e4]
    assert _close(t12[1e4], 3.0929575069687223, 1e-4), t12[1e4]
    sep = abs(rel[1e4]) / abs(rel[1e2])
    assert sep > 20.0, sep
    print(f"(2) CONTROL: in-grid 1e2 error {rel[1e2]*100:+.2f}% vs out-of-grid 1e4 "
          f"error {rel[1e4]*100:+.2f}% -- separation {sep:.0f}x")


# ===========================================================================
# (3) PINS AN OPEN DEFECT -- the REQUESTED fit window is reported, not the realized one
# ===========================================================================
def test_reported_window_is_the_requested_one():
    fam, om, c, D = _solved(0.3, 8.0)
    X = np.asarray(fam.X, float)
    d = velocity_log_rate(fam, om)                     # defaults lo=10, hi=1e3

    assert list(d["window"]) == [10.0, 1e3], d["window"]       # PINNED: requested
    realized_hi = float(X[(X > 10.0) & (X < 1e3)].max())
    assert _close(realized_hi, 745.2394128947751, 1e-12), realized_hi
    assert _close(1e3 / realized_hi, 1.341850662615446, 1e-9)

    # advection_split fits to hi=1e4 by default and reports NO window at all
    sp = advection_split(fam, om, 0.3, ALPHA, D)
    assert "window" not in sp, sorted(sp)
    assert _close(1e4 / realized_hi, 13.41850662615446, 1e-9)

    # PINNED DEFECT: the module's own two-predictor discrepancy check is INERT on
    # its default path -- the windowed and full-domain masses are bit-identical,
    # because |X| <= 1e3 already contains the whole grid (lesson 90).
    assert d["predicted"] - d["predicted_full_domain"] == 0.0
    assert d["mass_window"] - d["mass"] == 0.0
    print("(3) PINNED DEFECT: window reported [10, 1000], realized [10.1, 745.24]; "
          "advection_split requests 13.42x past the grid and reports no window")


# ===========================================================================
# (4) SOUND -- NaN and Inf propagate through every entry point, nothing absorbs
# ===========================================================================
def test_nonfinite_poison_propagates_everywhere():
    fam, om0, c, D = _solved(0.3, 8.0)
    X = np.asarray(fam.X, float)
    for tag, bad in (("nan", np.nan), ("posinf", np.inf), ("neginf", -np.inf)):
        om = np.asarray(om0, float).copy()
        om[om.size // 2 + 40] = bad
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            outs = {
                "mass": profile_mass(om, X),
                "velocity_first": float(velocity(fam, om)[0]),
                "vlr": velocity_log_rate(fam, om)["measured"],
                "split_rate": advection_split(fam, om, 0.3, ALPHA, D)[
                    "transport_log_rate"],
                "split_at_1e2": advection_split(fam, om, 0.3, ALPHA, D)[
                    "transport_at"][1e2],
                "one_scale": grading_comparison(fam, om, 0.3, ALPHA, D)["one_scale"][
                    "transport_log_rate"],
                "stagnation": stagnation_point(fam, om, c, 0.3),
            }
        for k, v in outs.items():
            assert v is None or not np.isfinite(v), f"{tag}/{k} absorbed the poison: {v}"
        # the whole velocity field is contaminated, not one node
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            U = velocity(fam, om)
        assert int((~np.isfinite(U)).sum()) == U.size, (tag, (~np.isfinite(U)).sum())
    print("(4) SOUND: 0 of 21 poisoned calls returned a finite number; "
          "the dense Hmat/Vmat products contaminate 801/801 velocity nodes")


# ===========================================================================
# (5) SOUND -- stagnation_point does not fabricate a root from a NaN bracket
# ===========================================================================
def test_stagnation_nan_bracket_does_not_fabricate_a_root():
    fam, om0, c, D = _solved(0.3, 8.0)
    X = np.asarray(fam.X, float)
    true_star = stagnation_point(fam, om0, c, 0.3)
    assert _close(true_star, 7.12838418502464, 1e-6), true_star
    # np.sign(nan) is nan and (nan != 0) is True, so a NaN CAN enter the bracket
    assert bool(np.sign(np.nan) != 0)
    for where in (0.25, 4.0):
        om = np.asarray(om0, float).copy()
        om[int(np.searchsorted(X, true_star * where))] = np.nan
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            got = stagnation_point(fam, om, c, 0.3)
        assert got is not None and np.isnan(got), got     # flagged, not fabricated
    print(f"(5) SOUND: true X* = {true_star:.6f}; a NaN bracket returns nan, "
          "never a plausible finite root")


# ===========================================================================
# (6) PINS AN OPEN DEFECT -- one None for physically opposite states
# ===========================================================================
def test_none_means_two_opposite_things():
    fam, om, c, D = _solved(0.3, 8.0)
    U = velocity(fam, om)[fam.X > 0]

    documented = stagnation_point(fam, om, c, 0.0)          # c_eff == c > 0
    reversed_everywhere = stagnation_point(fam, om, -c, 0.3)
    eff = -c + 0.3 * U
    assert documented is None
    assert reversed_everywhere is None                       # PINNED: same answer
    assert float(eff.max()) < 0.0, eff.max()                 # yet never positive
    assert _close(float(eff.min()), -2.218815594569719, 1e-5), eff.min()
    assert _close(float(eff.max()), -0.5822647074273348, 1e-5), eff.max()
    assert float(np.mean(eff < 0)) == 1.0

    # the contrast: a genuine crossing is found and is well inside the grid
    assert _close(stagnation_point(fam, om, c, 0.3), 7.12838418502464, 1e-6)
    print("(6) PINNED DEFECT: None returned for c_eff == +0.5822 everywhere AND for "
          "c_eff in [-2.2188, -0.5823] -- a span of 2.80 covering both signs")


# ===========================================================================
# (7) PINS AN OPEN DEFECT -- a hard-coded 0.0 published as a "predicted rate"
# ===========================================================================
def test_one_scale_predicted_rate_is_a_constant():
    fam, om, c, D = _solved(0.3, 8.0)
    gc = grading_comparison(fam, om, 0.3, ALPHA, D)
    one, two = gc["one_scale"], gc["two_scale"]

    # PINNED: the key is exactly 0.0 no matter what is fed to it (lesson 90 --
    # a number that cannot come out differently is not a prediction)
    for a, al in ((0.0, 1.4), (0.3, 1.4), (0.5, 0.5), (0.9, 2.0), (2.0, 1.9)):
        v = advection_split(fam, om, a, al, D, grading="one_scale")[
            "transport_predicted_rate"]
        assert v == 0.0, (a, al, v)
    assert _close(one["transport_log_rate"], -0.01832528938761544, 1e-3)

    # the positive control: under two_scale the SAME key is a real prediction
    rel = abs(two["transport_log_rate"] - two["transport_predicted_rate"]) / abs(
        two["transport_predicted_rate"])
    assert rel < 0.01, rel
    assert _close(rel, 0.0026550307688162898, 1e-2), rel
    print("(7) PINNED DEFECT: one_scale predicted rate is 0.0 for 5/5 inputs while the "
          "fit reads -0.01833; the two_scale sibling predicts its fit to 0.27%")


# ===========================================================================
# (8) PINS AN OPEN DEFECT -- the predictor's SIGN is wrong outside the working range
# ===========================================================================
def test_predicted_rate_sign_is_wrong_for_negative_alpha():
    fam, om, c, D = _solved(0.3, 8.0)
    rows = {al: advection_split(fam, om, 0.3, al, D) for al in (1.4, 2.0, 2.5, -1.0)}

    # inside the stated working range the predictor tracks the fit
    for al in (1.4, 2.0, 2.5):
        p, m = rows[al]["transport_predicted_rate"], rows[al]["transport_log_rate"]
        assert abs(p - m) / abs(m) < 0.01, (al, p, m)

    # PINNED: at alpha < 0 the reported prediction has the OPPOSITE sign to the fit,
    # with no warning -- a |x| in the measured quantity that the formula does not carry
    p, m = rows[-1.0]["transport_predicted_rate"], rows[-1.0]["transport_log_rate"]
    assert p < 0.0 < m, (p, m)
    assert _close(p, -0.22614575196271194, 1e-4), p
    assert _close(m, 0.22674693723070877, 1e-4), m

    # and the header's "decays for alpha < 2, which is the whole working range" is
    # left with no flag: the stretch rate grows by 567x from alpha=1.4 to alpha=2.5
    growth = rows[2.5]["stretch_log_rate"] / rows[1.4]["stretch_log_rate"]
    assert growth > 100.0, growth
    assert _close(growth, 567.3542, 1e-2), growth
    print(f"(8) PINNED DEFECT: at alpha=-1 predicted {p:+.5f} vs fitted {m:+.5f} "
          f"(opposite signs); stretch rate grows {growth:.0f}x past alpha=2, unflagged")


# ===========================================================================
# (9) PINS AN OPEN DEFECT -- `predicted` survives a window the fit refused
# ===========================================================================
def test_predicted_survives_a_window_the_fit_refused():
    fam, om, c, D = _solved(0.3, 8.0)

    inverted = velocity_log_rate(fam, om, lo=1e3, hi=10.0)
    empty = velocity_log_rate(fam, om, lo=1e6, hi=1e7)
    for d in (inverted, empty):
        assert np.isnan(d["measured"])                   # the fit is honest
        # PINNED: a finite, plausible `predicted` is returned beside the nan,
        # because the mass window is |X| <= hi -- a different set from the fit window
        assert np.isfinite(d["predicted"]), d["predicted"]
    assert _close(inverted["predicted"], -0.7537916060318983, 1e-5)
    assert _close(empty["predicted"], -0.7538191732090398, 1e-5)
    assert list(inverted["window"]) == [1e3, 10.0]        # reported inverted, unflagged
    print("(9) PINNED DEFECT: inverted window [1000, 10] -> measured nan but "
          f"predicted {inverted['predicted']:.6f}; empty window [1e6, 1e7] -> "
          f"predicted {empty['predicted']:.6f}")


# ===========================================================================
# (10) PINS AN OPEN DEFECT -- transport_predicted_rate ignores h entirely
# ===========================================================================
def test_predicted_rate_ignores_a_poisoned_h():
    fam, om, c, D = _solved(0.3, 8.0)
    h = np.ones(int(fam.X.size))
    h[h.size // 2] = np.nan
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sp = advection_split(fam, om, 0.3, ALPHA, D, h=h)
    assert np.isnan(sp["transport_log_rate"])            # the fit is honest
    # PINNED: the sibling key in the SAME dict returns the unpoisoned number,
    # because the formula reads only M and alpha
    assert np.isfinite(sp["transport_predicted_rate"])
    clean = advection_split(fam, om, 0.3, ALPHA, D)["transport_predicted_rate"]
    assert sp["transport_predicted_rate"] == clean
    assert _close(clean, 0.3166040527477967, 1e-5), clean
    print("(10) PINNED DEFECT: with h NaN-poisoned, transport_log_rate is nan while "
          f"transport_predicted_rate returns the clean {clean:.10f} in the same dict")


# ===========================================================================
# (11) SOUND -- the <8-node refusal fires exactly where it says it does
# ===========================================================================
def test_short_window_refusal_boundary():
    fam, om, c, D = _solved(0.3, 8.0)
    X = np.asarray(fam.X, float)
    Xs = np.sort(X[X > 0])
    hi = float(Xs[-1]) * 1.001
    seven, eight = float(Xs[-8]), float(Xs[-9])
    assert int(((X > seven) & (X < hi)).sum()) == 7
    assert int(((X > eight) & (X < hi)).sum()) == 8
    assert np.isnan(velocity_log_rate(fam, om, lo=seven, hi=hi)["measured"])
    got = velocity_log_rate(fam, om, lo=eight, hi=hi)["measured"]
    assert np.isfinite(got) and _close(got, -0.7538664492045556, 1e-5), got
    print("(11) SOUND: 7 nodes -> nan, 8 nodes -> a fit; the guard is exactly at 8")


# ===========================================================================
# (12) SOUND -- the loud failures, and the a=0 control that must NOT flag
# ===========================================================================
def test_loud_failures_and_the_a_zero_control():
    fam, om, c, D = _solved(0.3, 8.0)
    fam0, om0, c0, D0 = _solved(0.0, 8.0)

    raised = {}
    for tag, fn in (
        ("grading_typo", lambda: advection_split(fam, om, 0.3, ALPHA, D,
                                                 grading="two-scale")),
        ("grading_empty", lambda: advection_split(fam, om, 0.3, ALPHA, D, grading="")),
        ("h_wrong_length", lambda: advection_split(fam, om, 0.3, ALPHA, D,
                                                   h=np.ones(7))),
        ("lo_negative", lambda: velocity_log_rate(fam, om, lo=-5.0, hi=1e3)),
    ):
        try:
            with warnings.catch_warnings():   # the lo<0 probe logs log(x<=0) on purpose
                warnings.simplefilter("ignore")
                fn()
        except Exception as exc:                            # noqa: BLE001
            raised[tag] = type(exc).__name__
    assert raised == {"grading_typo": "KeyError", "grading_empty": "KeyError",
                      "h_wrong_length": "ValueError",
                      "lo_negative": "LinAlgError"}, raised

    # C1: at a = 0 every advection quantity is IDENTICALLY zero -- if the battery
    # flagged these it would be flagging arithmetic, not corruption
    sp0 = advection_split(fam0, om0, 0.0, ALPHA, D0)
    assert float(np.max(np.abs(sp0["transport"]))) == 0.0
    assert float(np.max(np.abs(sp0["stretch"]))) == 0.0
    assert all(v == 0.0 for v in sp0["transport_at"].values())
    assert sp0["transport_predicted_rate"] == 0.0
    assert stagnation_point(fam0, om0, c0, 0.0) is None
    print(f"(12) SOUND: 4 loud failures {sorted(raised.values())}; a=0 control exactly "
          "zero on every advection quantity")


# ===========================================================================
if __name__ == "__main__":
    import time
    t0 = time.time()
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    order = [test_far_field_probe_fabricates_values_past_the_grid,
             test_control_grid_that_contains_the_keys_disagrees_out_of_grid_only,
             test_reported_window_is_the_requested_one,
             test_nonfinite_poison_propagates_everywhere,
             test_stagnation_nan_bracket_does_not_fabricate_a_root,
             test_none_means_two_opposite_things,
             test_one_scale_predicted_rate_is_a_constant,
             test_predicted_rate_sign_is_wrong_for_negative_alpha,
             test_predicted_survives_a_window_the_fit_refused,
             test_predicted_rate_ignores_a_poisoned_h,
             test_short_window_refusal_boundary,
             test_loud_failures_and_the_a_zero_control]
    assert len(order) == len(tests), (len(order), len(tests))
    for fn in order:
        fn()
    print(f"\nall {len(order)} gates passed in {time.time() - t0:.1f} s "
          "(6 of them PIN OPEN DEFECTS -- see the module docstring)")
