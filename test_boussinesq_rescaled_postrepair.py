"""Leg 233 (Route-BVRRV) -- the standing gate on leg 221's repair to
`solver/boussinesq_rescaled.py::odd_field_x_slope`.

This is clause (a) of leg 233's gate, made permanent. Leg 221 repaired the two mechanisms leg
205 measured and graded its own repair; legs 307 and 335 adjudicated adjacent artifacts but
both consumed leg 221's numbers as a premise. Until this file existed there was no standing
check that the two mechanisms still reject -- `test_boussinesq_rescaled.py`,
`test_boussinesq_transport.py` and `test_boussinesq_rescaled_status.py` are correctness gates on
well-posed input, and a correctness check on well-behaved input is not a robustness check (leg
205's own words).

The heavy lifting lives in `experiments/p2_route_bvrrv_v1_postrepair.py`; this file is the fast
gate over it. It reads `solver/boussinesq_rescaled.py` and edits nothing.

Run:  python test_boussinesq_rescaled_postrepair.py

Runtime: a few seconds. Leg 205's 81-case battery is executed TWICE (once against the
pre-repair module read out of git, once against the module on disk), which is the whole cost.
"""

from __future__ import annotations

import contextlib
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
for p in (ROOT, os.path.join(ROOT, "experiments")):
    if p not in sys.path:
        sys.path.insert(0, p)

from p2_route_bvrrv_v1_postrepair import (            # noqa: E402
    LEG_205_TOTALS, clause_a, load_pre_repair, module_staleness,
    probe_liveness_selftest, two_modules_really_differ,
)
from solver.boussinesq_velocity import PolarGrid      # noqa: E402
import solver.boussinesq_rescaled as POST             # noqa: E402

_CACHE = {}


def pre():
    if "pre" not in _CACHE:
        _CACHE["pre"], _ = load_pre_repair()
    return _CACHE["pre"]


def battery():
    if "battery" not in _CACHE:
        with open(os.devnull, "w") as devnull, contextlib.redirect_stdout(devnull):
            _CACHE["battery"] = clause_a(pre(), POST)
    return _CACHE["battery"]


@contextlib.contextmanager
def raises(exc, match=None):
    try:
        yield
    except exc as e:
        if match is not None and match not in str(e):
            raise AssertionError("expected %r in %r" % (match, str(e)[:300])) from None
        return
    raise AssertionError("expected %s, nothing was raised" % exc.__name__)


# ---------------------------------------------------------------------------
# Q0. Is the module under test still the module that was repaired?
# ---------------------------------------------------------------------------
def test_module_semantics_are_still_the_repaired_ones():
    """`solver/boussinesq_rescaled.py` was touched by leg 352 (`aa9c5cd`) AFTER the repair, so
    "byte-identical to the repair commit" is FALSE and stating it would be wrong. What is true,
    and what this test pins, is that every post-repair change is docstring text: the
    docstring-stripped AST is identical to the repair commit's, and differs from the pre-repair
    commit's. If a future leg edits executable code here, this fails and the leg is told to
    re-run the sweep rather than inherit leg 233's answer."""
    st = module_staleness()
    assert st["main_vs_repair_commit"]["ast_nodoc_identical"], (
        "executable semantics have moved since leg 221's repair commit d2d9769; leg 233's "
        "clause-(b) sweep no longer covers this module and must be re-run")
    assert not st["main_vs_pre_repair"]["ast_nodoc_identical"], (
        "the module on disk is semantically the PRE-repair module -- the repair has been "
        "reverted or lost")
    # Recorded as magnitudes, not booleans: the raw bytes genuinely do differ.
    d = st["main_vs_leg221_final"]
    assert d["ast_nodoc_identical"]
    assert isinstance(d["byte_delta"], int)


# ---------------------------------------------------------------------------
# LESSON 90 -- a control that cannot come out differently is not a control
# ---------------------------------------------------------------------------
def test_lesson_90_the_two_modules_really_differ():
    """Before any "0 SILENT_WRONG" below is believed: the pre- and post-repair functions must be
    distinct objects that disagree by a MEASURED amount on the two inputs leg 205 published. A
    differential between a module and itself reports zero for free."""
    c = two_modules_really_differ(pre(), POST)
    assert c["all_passed"], c["checks"]
    m = c["magnitudes"]
    # DEFECT B: pre fabricates by ~87%, post lands inside the module's own 5e-4 tolerance.
    assert m["defect_B_pre_rel_err"] > 0.8
    assert m["defect_B_post_rel_err"] <= 5e-4
    # DEFECT A: pre returns exactly 0.0 against a truth of 2.0; post raises.
    assert m["defect_A_pre"] == 0.0
    assert str(m["defect_A_post"]).startswith("ValueError")


def test_guard_reachability_probe_can_report_both_outcomes():
    """LESSON 90, applied to leg 233's own instrument. Clause (b)'s sharpest number is
    `cap_binds` -- how often the DEFECT-B window cap actually BINDS across the banked corpus.
    A zero there is only informative if the probe can report non-zero, so it is exercised on
    two fields with known, opposite answers: lam=400 (scale 0.05, inside r_win) must bind, and
    lam=1 (scale 1.0, outside r_win) must not."""
    s = probe_liveness_selftest(POST)
    assert s["probe_can_report_both_outcomes"], s
    for k, v in s.items():
        if isinstance(v, dict):
            assert v["probe_agrees_with_expectation"], (k, v)
    # magnitudes, not booleans: the cap shrinks the window to ~6.2% of r_win on lam=400
    assert s["lam=400 (scale 0.05, INSIDE r_win)"]["cap_shrink_factor"] < 0.1
    assert s["lam=1 (scale 1.0, OUTSIDE r_win)"]["cap_shrink_factor"] == 1.0


# ---------------------------------------------------------------------------
# The control on the control: does the PRE-repair re-measurement reproduce leg 205?
# ---------------------------------------------------------------------------
def test_pre_repair_side_reproduces_leg_205s_committed_battery():
    """If the "before" column is not leg 205's finding, nothing downstream verifies leg 221.
    Checked case-by-case on the `case` string, not just on the totals -- a tally can match while
    individual verdicts have swapped."""
    b = battery()
    assert b["n_cases_before"] == 81
    assert b["n_verdict_mismatch_vs_committed"] == 0, \
        b["verdict_mismatch_detail"]
    assert b["tally_remeasured_pre_repair"] == dict(sorted(LEG_205_TOTALS.items()))


# ---------------------------------------------------------------------------
# CLAUSE (a) -- do both named mechanisms now reject correctly?
# ---------------------------------------------------------------------------
def test_defect_A_empty_window_is_refused_not_fabricated():
    """Leg 205's headline for DEFECT A: an empty fit window handed to `np.linalg.lstsq` absorbs
    a (0,3) design matrix into exactly 0.0 -- 100% relative error against a truth of 2.0, no
    raise, no warning. A fabricated 0.0 is indistinguishable at the call site from the true
    statement "the origin strain vanishes"."""
    grid = PolarGrid(n_r=200, n_beta=16, r_min=0.5, r_max=40.0)
    g = 2.0 * grid.R * np.cos(grid.B) * np.exp(-grid.R ** 2)
    with raises(ValueError, match="fit window"):
        POST.odd_field_x_slope(g, grid)


def test_defect_A_under_determined_window_is_refused():
    """One node against three parameters: lstsq returns its minimum-norm solution and the caller
    sees a number. Leg 205 measured 1.9061 (4.694e-2, 93.9x tolerance) presented as the fit."""
    grid = PolarGrid(n_r=10, n_beta=16, r_min=1e-2, r_max=1e2)
    g = 2.0 * grid.R * np.cos(grid.B) * np.exp(-grid.R ** 2)
    with raises(ValueError):
        POST.odd_field_x_slope(g, grid)


def test_defect_A_rank_deficient_window_is_refused():
    """The guard is not just an occupancy count. A window of 32 nodes at r ~ 1e-4 makes the
    (r, r^3, r^5) design matrix numerically singular -- measured singular-value ratio 3.9e-15,
    rank 2 of 3 -- and lstsq would hand back its minimum-norm solution as the fit."""
    grid = PolarGrid(n_r=400, n_beta=16, r_min=1e-4, r_max=1e4)
    g = 2.0 * grid.R * np.cos(grid.B) * np.exp(-grid.R ** 2)
    with raises(ValueError, match="rank-deficient"):
        POST.odd_field_x_slope(g, grid, r_win=5e-4)


def test_defect_B_scale_mismatch_is_recovered_not_fabricated():
    """Leg 205's headline for DEFECT B, on its own leg-73-class grid: a FULLY RESOLVED window
    (177 nodes, rank 3) on a smooth in-contract field of scale 0.05, read as 0.269302 against a
    truth of 2.0 -- 86.5%, 1731x the module's own 5e-4 tolerance. The occupancy guard is
    provably blind to this one, so it is a genuinely independent mechanism."""
    grid = PolarGrid(n_r=400, n_beta=16, r_min=1e-4, r_max=1e4)
    g = 2.0 * grid.R * np.cos(grid.B) * np.exp(-400.0 * grid.R ** 2)
    got = float(POST.odd_field_x_slope(g, grid))
    assert abs(got - 2.0) / 2.0 <= 5e-4, got


def test_defect_B_cap_is_one_sided_and_non_binding_in_contract():
    """The cure must not move a value it was not aimed at. On the class the module is validated
    on, the cap returns the caller's `r_win` as the identical float, so the fit is bit-identical
    to the unrepaired one. Measured against the pre-repair module directly."""
    pre_mod = pre()
    grid = PolarGrid(n_r=400, n_beta=16, r_min=1e-4, r_max=1e4)
    g = 2.0 * grid.R * np.cos(grid.B) * np.exp(-1.0 * grid.R ** 2)
    a = float(pre_mod.odd_field_x_slope(g, grid))
    b = float(POST.odd_field_x_slope(g, grid))
    assert a == b, (a.hex(), b.hex())


def test_battery_silent_wrong_goes_to_zero():
    """The gate's clause (a), on leg 205's own 81 cases. 18 SILENT_WRONG before, 0 after."""
    b = battery()
    assert b["silent_wrong_before"] == 18
    assert b["silent_wrong_after"] == 0, b["silent_wrong_after_cases"]
    assert b["n_cases_after"] == 81


def test_the_repair_buys_its_zero_without_breaking_anything():
    """The check a count cannot make. "18 -> 0" is compatible with a repair that fixed 18
    SILENT_WRONGs by breaking 18 OKs, so the FULL transition matrix is examined and every
    case leaving OK is adjudicated against the module's own documented precondition: a refusal
    counts as justified only if the window genuinely holds fewer than `min_points` nodes or the
    design matrix is genuinely rank-deficient. Three cases leave OK here; all three are
    justified refusals, and any UNJUSTIFIED_REGRESSION fails this test."""
    b = battery()
    assert b["n_ok_regressions"] == 0, b["ok_regressions"]
    assert b["n_justified_refusals"] == b["n_ok_left_ok"]
    for a in b["ok_to_nonok_adjudication"]:
        assert a["verdict"] == "JUSTIFIED_REFUSAL", a
        assert a["precondition_genuinely_fails"], a


def test_no_verdict_class_lost_cases():
    """RAISED, NONFINITE, NO_REFERENT and RETURNED must not shrink: the repair may only turn
    SILENT_WRONG (and justified OKs) into refusals, never launder a visible failure into a
    silent success."""
    b = battery()
    before, after = b["tally_remeasured_pre_repair"], b["tally_post_repair"]
    for k in ("NONFINITE", "NO_REFERENT", "RETURNED"):
        assert after.get(k, 0) == before.get(k, 0), (k, before, after)
    assert after.get("RAISED", 0) >= before.get("RAISED", 0)
    assert sum(after.values()) == sum(before.values()) == 81


def test_clause_a_overall():
    b = battery()
    assert b["clause_a_pass"], {k: b[k] for k in
                                ("silent_wrong_after", "n_ok_regressions",
                                 "n_verdict_mismatch_vs_committed")}


# ---------------------------------------------------------------------------
# The two-scale field leg 221 flagged and leg 307 adjudicated: NOT reopened, PINNED
# ---------------------------------------------------------------------------
def test_two_scale_counterexample_is_pinned_where_leg_307_left_it():
    """Leg 307 (`401a5f7`) adjudicated this field yes-ARTIFACT, not yes-genuine: it sits outside
    the repository's own banked reachability. This test does not reopen that; it pins the
    magnitude so a future change to the cap heuristic cannot move it silently. The number is
    43.2% against a truth of 2.0 -- and ~865x the module's own 5e-4 basis, NOT the 86x the
    original passage said (leg 307's arithmetic finding, corrected in-place by leg 352
    `aa9c5cd`)."""
    grid = PolarGrid(n_r=400, n_beta=16, r_min=1e-4, r_max=1e4)
    g = grid.R * np.cos(grid.B) * (np.exp(-grid.R ** 2) + np.exp(-400.0 * grid.R ** 2))
    got = float(POST.odd_field_x_slope(g, grid))
    rel = abs(got - 2.0) / 2.0
    assert 0.40 < rel < 0.45, got
    assert 800 < rel / 5e-4 < 900, rel / 5e-4


# ---------------------------------------------------------------------------
TESTS = [
    test_module_semantics_are_still_the_repaired_ones,
    test_lesson_90_the_two_modules_really_differ,
    test_guard_reachability_probe_can_report_both_outcomes,
    test_pre_repair_side_reproduces_leg_205s_committed_battery,
    test_defect_A_empty_window_is_refused_not_fabricated,
    test_defect_A_under_determined_window_is_refused,
    test_defect_A_rank_deficient_window_is_refused,
    test_defect_B_scale_mismatch_is_recovered_not_fabricated,
    test_defect_B_cap_is_one_sided_and_non_binding_in_contract,
    test_battery_silent_wrong_goes_to_zero,
    test_the_repair_buys_its_zero_without_breaking_anything,
    test_no_verdict_class_lost_cases,
    test_clause_a_overall,
    test_two_scale_counterexample_is_pinned_where_leg_307_left_it,
]


if __name__ == "__main__":
    for t in TESTS:
        t()
        print("[ok] %s" % t.__name__)
    b = battery()
    print("\n  leg 205 committed        : %s" % b["tally_committed_leg_205"])
    print("  re-measured pre-repair   : %s" % b["tally_remeasured_pre_repair"])
    print("  post-repair (this module): %s" % b["tally_post_repair"])
    print("  transitions              : %s" % b["transitions"])
    print("  OK -> non-OK adjudicated : %d justified refusal(s), %d unjustified regression(s)"
          % (b["n_justified_refusals"], b["n_ok_regressions"]))
    print("\nALL BOUSSINESQ-RESCALED POST-REPAIR (LEG 233 CLAUSE (a)) TESTS PASSED")
