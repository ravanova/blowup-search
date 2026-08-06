"""Leg 83 / Route-MFG — the permanent adversarial battery against gate 11.

This file BANKS A MEASUREMENT.  It was originally a CHARACTERISATION of a defect; it is
now a gate on that defect's (partial) ABSENCE.  Read this before changing anything it
asserts.

WHAT LEG 83 FOUND (2026-08-06).  `capabilities.py` records, for
`solver/marginal_flow.py`, that "`integrate` reports `converged` and gate 11 enforces it
(the NaN of leg 41)".  Gate 11 (`test_marginal_flow.py::test_11`) exercises that
predicate on exactly two trajectories: the leg-41 naive-perturbation trap, which ends in
a NaN, and one healthy on-branch run.  Leg 83 asked what the predicate does on
divergence that never produces a NaN:

    MEASURED, BEFORE THE REPAIR: 8 of 9 scored divergent trajectories were reported
    `converged = True`, including one whose state grows by 130 decades.  1 of 9 was
    caught -- the finite-time blowup, i.e. the NaN case the gate was built for.  0 of 3
    genuinely convergent controls was falsely flagged.

The mechanism, in one line: every clause of `converged` was an observable of the inner
Newton solve or of IEEE finiteness, and none was an observable of the state.

WHAT WAS THEN FIXED.  `integrate` now tracks, at EVERY step, how far `b` and `mu` have
grown relative to their own initial magnitude (per block, never as a joint norm -- see
the module comment) and adds a fourth clause: `state_growth < 1e5`.  The bound is
relative and therefore scale-free, because this module integrates trajectories at
mu0 = 2e-3 and at mu0 = 4 and no absolute cap serves both.

    MEASURED, AFTER THE REPAIR: 5 of 9 caught, 4 still missed, still 0 of 3 false
    positives.  Newly caught: `mu_quartic` (1.4e7), `mu_exp_mild` (1.2e13),
    `mu_negative_runaway` (1.2e13) and `mu_exp_extreme` -- leg 83's worst case, which
    grows by 4.99e130 and which the old predicate accepted with a Newton residual
    1.6e-10 of its threshold.

WHAT IS DELIBERATELY STILL MISSED, AND WHY IT IS NOT A WEAKER FIX THAN IT LOOKS.  A
growth bound cannot go below the growth of trajectories this module is SUPPOSED to
accept.  `test_marginal_flow.py` test (6) at p = 5 has lambda_mu = +2 and is meant to
grow mu from 2e-3 to 0.813 over tau = 3, a factor 4.06e2 -- growth is normal here, and a
"must settle to a limit" clause would be flatly wrong for this module.  So:

  * `mu_linear` (2.01e2) sits BELOW that legitimate ceiling.  No scale-free growth
    observable can separate it from test (6); it is structurally out of reach.
  * `b_quadratic` (3.73e3) is only 9.2x above the ceiling -- catchable only by a
    threshold with too little headroom to be safe.
  * `osc_sustained` (1.00) and `osc_growing` (1.99) never get large at all.  They have
    no limit, but a state-MAGNITUDE clause is the wrong instrument for them; catching
    them needs a tail/Cauchy test, which is a separate change (leg 83 disposition 2).

These four remain pinned as `assert converged is True` for exactly the reason the
original eight were: so the behaviour cannot change silently.  If a later repair catches
them, flip those assertions -- never weaken the ones above so a repair looks
unnecessary.  Tests 2 and 3 are SOUNDNESS assertions and must never be relaxed.

Run:  .venv/bin/python test_marginal_flow_adversarial.py
"""

import importlib.util
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

_SPEC = importlib.util.spec_from_file_location(
    "p2_route_mfg_v1_adversarial",
    PROJECT_ROOT / "experiments" / "p2_route_mfg_v1_adversarial.py")
MFG = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(MFG)

from solver.marginal_flow import integrate  # noqa: E402


# The battery is deterministic and cheap (~6 s); run it once and share the rows.
# The LIVE controls are deliberately not run here -- they are gate 11's own two
# trajectories and cost ~150 s of Newton seeding.  `experiments/
# p2_route_mfg_v1_adversarial.py` runs them and banks the result.
_ROWS = None


def rows():
    global _ROWS
    if _ROWS is None:
        _ROWS = {r["name"]: r for r in (MFG.run_case(c) for c in MFG.battery())}
    return _ROWS


# --------------------------------------------------------------------------
def test_1_the_harness_is_not_degenerate():
    """(1) A SYNTHETIC FLOW MUST BE INDISTINGUISHABLE FROM AugmentedFlow TO `integrate`.

    If `SyntheticFlow` were mis-shaped, `integrate` could be failing for a reason that
    has nothing to do with the trajectory and every verdict below would be worthless.
    So: the record `integrate` returns must carry every field the real one carries, the
    trajectory must have been stepped the full number of steps, and the exactly-solvable
    members must be reproduced to their stated tolerance.
    """
    A = MFG.SyntheticFlow(1, *MFG._scalar_mu(lambda u: 0.0, lambda u: 0.0))
    rec = integrate(A, [1.0], 0.3, 5.0, 0.25, n_sample=20)
    for key in ("converged", "finite", "worst_newton_residual_over_floor",
                "worst_newton_iters", "mu_end", "b_end", "gauge_drift",
                "gauge_violation", "steps", "a", "p", "K", "s"):
        assert key in rec, (key, sorted(rec))

    # a constant flow is reproduced exactly and runs every step
    r = rows()["exact_fixed_point"]
    assert r["steps"] == 240, r["steps"]
    assert r["rel_err_vs_exact"] == 0.0, r["rel_err_vs_exact"]
    assert r["worst_newton_residual_over_floor"] == 0.0, r

    # and a flow with a known closed form is tracked, not merely finite
    q = rows()["mu_quartic"]
    assert q["rel_err_vs_exact"] < 0.05, q["rel_err_vs_exact"]
    assert abs(q["fit_polynomial_exponent"] - 4.0) < 0.2, q["fit_polynomial_exponent"]
    print(f"  (1) harness OK: fixed point exact to {r['rel_err_vs_exact']:.1e}, "
          f"(1+tau)^4 tracked to {q['rel_err_vs_exact']:.2e} with fitted exponent "
          f"{q['fit_polynomial_exponent']:.3f}")


def test_2_the_design_case_is_still_caught():
    """(2) THE NaN OF LEG 41 -- the one failure mode gate 11 was built for.

    `mu' = mu^2` blows up at tau = 1 and is integrated to tau = 60.  The predicate must
    refuse it.  This assertion is a SOUNDNESS assertion and must never be relaxed.
    """
    r = rows()["nan_finite_time_blowup"]
    assert r["gate11_converged"] is False, r
    assert r["worst_newton_residual_over_floor"] > MFG.NEWTON_STAGNATION, r
    print(f"  (2) finite-time blowup REFUSED: Newton residual/floor "
          f"{r['worst_newton_residual_over_floor']:.2e} exceeds the "
          f"{MFG.NEWTON_STAGNATION:.0e} threshold by "
          f"{r['worst_newton_residual_over_floor'] / MFG.NEWTON_STAGNATION:.2e}x")


def test_3_no_false_positives_on_genuinely_convergent_flows():
    """(3) THE OTHER HALF OF COVERAGE, and the one that must not regress under a repair.

    A predicate can be made to catch everything by flagging everything.  These three
    trajectories have real limits -- exponential decay to zero, an exact fixed point,
    and a spiral that is oscillatory but decaying -- and all three must be kept.  A
    repair that catches the missed cases below by failing any of these has made the
    gate worse, not better.
    """
    kept = []
    for name in ("decay_to_zero", "exact_fixed_point", "damped_oscillation"):
        r = rows()[name]
        assert r["gate11_converged"] is True, (name, r)
        assert r["verdict"] == "PASSED", (name, r["verdict"])
        kept.append((name, r["worst_newton_residual_over_floor"]))
    print("  (3) all 3 convergent controls kept: "
          + ", ".join(f"{n} (res/floor {v:.1e})" for n, v in kept))


def test_4_smooth_runaway_is_now_refused():
    """(4) THE REPAIR -- unbounded growth with a PERFECTLY HEALTHY inner solve is caught.

    Four members, ground truth `divergent` by closed form, each one of which the old
    predicate accepted.  What makes them the interesting cases is the second block of
    assertions: every one is finite, never breaks on a NaN, and has a Newton residual
    BELOW ITS OWN FLOOR (`< 1.0`, i.e. at least 1e8x inside the stagnation threshold).
    So none of the three original clauses fires on any of them -- they are refused by
    the state clause and by nothing else, which is exactly what was missing.

    The magnitudes are asserted as well as the verdict, so a regression that catches
    them for some unrelated reason is visible as a specific failure rather than a silent
    change of subject.  These are now SOUNDNESS assertions: do not relax them.
    """
    expect = {                    # name: (min state growth factor, exact law)
        "mu_quartic": (1e6, "mu = (1+tau)^4"),
        "mu_exp_mild": (1e12, "mu = 0.3 e^{tau/2}"),
        "mu_exp_extreme": (1e120, "mu = 0.3 e^{5 tau}"),
        "mu_negative_runaway": (1e12, "mu = -0.3 e^{tau/2}"),
    }
    for name, (floor_growth, law) in expect.items():
        r = rows()[name]
        assert r["fidelity_ok"], (name, r["fidelity_criterion"])
        assert r["state_growth_factor"] > floor_growth, (name, r["state_growth_factor"])
        # the repair: now REFUSED
        assert r["gate11_converged"] is False, (
            name, "the state clause must refuse this; see the module docstring")
        # and it is the STATE clause doing it -- none of the original three fires here
        assert r["clause_finite"] is True, (name, r)
        assert r["clause_no_nan_break"] is True, (name, r)
        assert r["worst_newton_residual_over_floor"] < 1.0, (name, r)
        print(f"  (4) {name:<22s} {law:<20s} state grew "
              f"{r['state_growth_factor']:.2e}x with Newton residual/floor "
              f"{r['worst_newton_residual_over_floor']:.2e} "
              f"({r['newton_headroom']:.1e}x below the Newton threshold) -> REFUSED")


def test_4b_what_the_growth_bound_still_cannot_reach():
    """(4b) CHARACTERIZATION -- the two divergent cases a growth bound cannot separate.

    `mu_linear` grows by 2.01e2 and `b_quadratic` by 3.73e3.  The largest growth reached
    by any trajectory `test_marginal_flow.py` legitimately accepts is 4.06e2 (test (6) at
    p = 5, where lambda_mu = +2 is SUPPOSED to grow mu by that much).  `mu_linear` is
    below that ceiling outright; `b_quadratic` clears it by only 9.2x, which is not
    enough headroom for a threshold that must never refuse a good run.

    This is pinned, not hidden: the repair's limit is a measured quantity like its
    coverage.  Catching these needs a different instrument (a per-block bound with a
    tighter b channel, or a tail test), not a smaller number here.
    """
    for name, law in (("mu_linear", "mu = mu0 + tau"), ("b_quadratic", "b = (1+tau)^2")):
        r = rows()[name]
        assert r["fidelity_ok"], (name, r["fidelity_criterion"])
        assert r["gate11_converged"] is True, (
            name, "a later repair catches this -- flip the assertion, do not weaken "
                  "the ones in test_4")
        assert r["state_growth_factor"] < 1e5, (name, r["state_growth_factor"])
        print(f"  (4b) {name:<21s} {law:<20s} state grew only "
              f"{r['state_growth_factor']:.2e}x -- inside the 1e5 bound, still accepted")


def test_5_still_missed_sustained_oscillation():
    """(5) CHARACTERIZATION -- a trajectory with NO LIMIT AT ALL is still not caught.

    `osc_sustained` is a pure rotation: the exact amplitude is 1 for all time, so the
    trajectory has no limit and never decays, while nothing about it is large.  Before
    the repair this was the member that separated "the predicate misses BIG numbers"
    from "the predicate does not look at the state at all".  After the repair it makes a
    sharper point: the state clause is a MAGNITUDE clause, and magnitude is the wrong
    instrument for a bounded trajectory with no limit.  Amplitude 1.00 and 1.99 are not
    distinguishable from a good run by any growth bound that leaves test (6) alone.

    Catching these needs a tail/Cauchy or drift test (leg 83 disposition 2), which is a
    separate change with its own regression surface -- test (6)'s p = 5 trajectory is
    still growing at tau_end, so "must settle" is not available as a clause here.
    """
    for name in ("osc_sustained", "osc_growing"):
        r = rows()[name]
        assert r["fidelity_ok"], (name, r["fidelity_criterion"])
        assert 0.5 <= r["numerical_damping_factor"] <= 2.0, (name, r)
        assert r["gate11_converged"] is True, (name, "flip, do not weaken")
        assert r["worst_newton_residual_over_floor"] < 1.0, (name, r)
        assert r["state_growth_factor"] < 10.0, (name, r["state_growth_factor"])
        print(f"  (5) {name:<22s} amplitude {r['amp_end_computed']:.4f} at tau=20 "
              f"({r['numerical_damping_factor']:.3f} of exact), state growth only "
              f"{r['state_growth_factor']:.2f}x -> still converged=True")


def test_6_the_fidelity_gate_excludes_what_the_integrator_did_not_reproduce():
    """(6) THE AUDIT'S OWN HONESTY CLAUSE, and it binds on a real case.

    `osc_stiff_underresolved` is a rotation at omega dt = 4 rad/step.  BDF2 is L-stable,
    so it damps that mode to nothing: the trajectory the predicate actually saw DID
    converge, to zero.  Counting it as a missed divergence would blame the gate for the
    integrator.  It is excluded from the catch statistic and recorded as a separate
    hazard -- an under-resolved sustained oscillation is silently turned into a spurious
    decay, and nothing downstream would say so.
    """
    r = rows()["osc_stiff_underresolved"]
    assert r["fidelity_ok"] is False, r
    assert r["verdict"].startswith("EXCLUDED"), r["verdict"]
    assert r["numerical_damping_factor"] < 1e-6, r["numerical_damping_factor"]
    print(f"  (6) osc_stiff_underresolved EXCLUDED: BDF2 retained "
          f"{r['numerical_damping_factor']:.2e} of the exact amplitude, so the "
          f"trajectory seen by the predicate genuinely decayed")


def test_7_the_headline_counts():
    """(7) THE LEG'S HEADLINE, as a value so a dropped case fails a test (lesson 60)."""
    rs = list(rows().values())
    scored = [r for r in rs if r["fidelity_ok"]]
    div = [r for r in scored if r["ground_truth"] == "divergent"]
    missed = [r for r in div if r["verdict"] == "MISSED"]
    caught = [r for r in div if r["verdict"] == "CAUGHT"]
    conv = [r for r in scored if r["ground_truth"] == "convergent"]
    fp = [r for r in conv if r["verdict"] == "FALSE_POSITIVE"]
    excluded = [r for r in rs if not r["fidelity_ok"]]

    assert len(div) == 9, len(div)
    assert len(conv) == 3 and not fp, (len(conv), fp)
    assert len(excluded) == 1, [r["name"] for r in excluded]

    # BEFORE the repair: 1 caught / 8 missed.  AFTER: 5 caught / 4 missed, and the four
    # that remain are named, because a count alone would let a regression swap one for
    # another and still read 5.
    assert len(caught) == 5, sorted(r["name"] for r in caught)
    assert len(missed) == 4, sorted(r["name"] for r in missed)
    assert sorted(r["name"] for r in caught) == [
        "mu_exp_extreme", "mu_exp_mild", "mu_negative_runaway", "mu_quartic",
        "nan_finite_time_blowup"], sorted(r["name"] for r in caught)
    assert sorted(r["name"] for r in missed) == [
        "b_quadratic", "mu_linear", "osc_growing", "osc_sustained"], \
        sorted(r["name"] for r in missed)

    # leg 83's worst case is caught, and it is caught on the STATE, not on Newton
    worst = max(div, key=lambda r: r["state_growth_factor"])
    assert worst["name"] == "mu_exp_extreme", worst["name"]
    assert worst["state_growth_factor"] > 1e120, worst["state_growth_factor"]
    assert worst["verdict"] == "CAUGHT", worst["verdict"]
    assert worst["worst_newton_residual_over_floor"] < 1.0, worst
    # and everything still missed is small -- no large state is accepted any more
    assert max(r["state_growth_factor"] for r in missed) < 1e5, \
        [(r["name"], r["state_growth_factor"]) for r in missed]

    print(f"  (7) catch coverage on non-NaN divergence: {len(caught)}/{len(div)} caught "
          f"(was 1/9), {len(missed)}/{len(div)} missed (was 8/9), {len(fp)}/{len(conv)} "
          f"false positives, {len(excluded)} excluded on fidelity")
    print(f"      leg 83's worst case {worst['name']} (state x"
          f"{worst['state_growth_factor']:.2e}, mu_end {worst['mu_end']:.3e}) is REFUSED "
          f"on the state clause, with its Newton residual "
          f"{worst['worst_newton_residual_over_floor']:.2e} still 1e8x inside its own "
          f"threshold")
    print(f"      still accepted, all small: "
          + ", ".join(f"{r['name']} (x{r['state_growth_factor']:.2e})"
                      for r in sorted(missed, key=lambda r: -r["state_growth_factor"])))


def test_8_the_predicate_now_has_a_state_clause():
    """(8) THE MECHANISM, asserted directly rather than inferred from the verdicts.

    Two trajectories, identical in every inner-solve observable and 13 decades apart in
    the state.  Leg 83's finding was that they received the SAME verdict, which is
    impossible if any state clause exists.  They must now disagree, and they must
    disagree while STILL agreeing on all three original clauses -- otherwise the change
    is being made by something other than the new clause.

    The second half locates the threshold rather than trusting it: the same exponential
    law, integrated for tau = 20 and for tau = 60, straddles 1e5 and gets both verdicts.
    Both runs are finite with a healthy Newton, so the state clause is the only thing
    that can be separating them.
    """
    r_ok = rows()["exact_fixed_point"]
    r_bad = rows()["mu_exp_mild"]
    ratio = r_bad["state_growth_factor"] / max(r_ok["state_growth_factor"], 1.0)
    assert ratio > 1e12, ratio
    # the original three clauses still agree ...
    assert r_ok["clause_finite"] == r_bad["clause_finite"] is True
    assert r_ok["clause_no_nan_break"] == r_bad["clause_no_nan_break"] is True
    assert r_ok["worst_newton_residual_over_floor"] < 1.0
    assert r_bad["worst_newton_residual_over_floor"] < 1.0
    # ... and the verdicts now differ anyway, which only a state clause can do
    assert r_ok["gate11_converged"] is True, r_ok
    assert r_bad["gate11_converged"] is False, r_bad

    # the clause is a growth bound, and here is where it sits
    A = MFG.SyntheticFlow(1, *MFG._scalar_mu(lambda u: 0.5 * u, lambda u: 0.5))
    near = integrate(A, [1.0], 0.3, 20.0, 0.25, n_sample=80)   # grows 2.2e4 -> kept
    far = integrate(MFG.SyntheticFlow(1, *MFG._scalar_mu(lambda u: 0.5 * u,
                                                         lambda u: 0.5)),
                    [1.0], 0.3, 60.0, 0.25, n_sample=240)      # grows 1.1e13 -> refused
    for rec in (near, far):
        assert rec["finite"] is True and "diverged_at_tau" not in rec, rec["mu_end"]
        assert rec["worst_newton_residual_over_floor"] < MFG.NEWTON_STAGNATION, rec
        assert "state_growth" in rec and "state_growth_threshold" in rec, sorted(rec)
    assert near["state_growth"] < near["state_growth_threshold"] <= far["state_growth"]
    assert near["converged"] is True, near["state_growth"]
    assert far["converged"] is False, far["state_growth"]
    print(f"  (8) the fixed point and a state {ratio:.1e}x larger now get DIFFERENT "
          f"verdicts while agreeing on all three original clauses")
    print(f"      threshold located: same law grows {near['state_growth']:.2e}x over "
          f"tau=20 (kept) and {far['state_growth']:.2e}x over tau=60 (refused), "
          f"bound = {near['state_growth_threshold']:.0e}")


if __name__ == "__main__":
    import time
    t0 = time.time()
    for fn in (test_1_the_harness_is_not_degenerate,
               test_2_the_design_case_is_still_caught,
               test_3_no_false_positives_on_genuinely_convergent_flows,
               test_4_smooth_runaway_is_now_refused,
               test_4b_what_the_growth_bound_still_cannot_reach,
               test_5_still_missed_sustained_oscillation,
               test_6_the_fidelity_gate_excludes_what_the_integrator_did_not_reproduce,
               test_7_the_headline_counts,
               test_8_the_predicate_now_has_a_state_clause):
        print(f"\n{fn.__name__}")
        fn()
    print(f"\nALL GATES PASS ({time.time() - t0:.0f}s)")
