"""Leg 83 / Route-MFG — the permanent adversarial battery against gate 11.

WHAT THIS FILE PINS, AND WHY IT ASSERTS THE *CURRENT* BEHAVIOUR
---------------------------------------------------------------------------
`capabilities.py` records, for `solver/marginal_flow.py`, that "`integrate` reports
`converged` and gate 11 enforces it (the NaN of leg 41)".  Gate 11
(`test_marginal_flow.py::test_11`) exercises that predicate on exactly two
trajectories: the leg-41 naive-perturbation trap, which ends in a NaN, and one healthy
on-branch run.  Leg 83 asked what the predicate does on divergence that never produces
a NaN, and the answer is measured here.

    MEASURED: 8 of 9 scored divergent trajectories are reported `converged = True`,
    including one whose state grows by 130 decades.  1 of 9 is caught -- the finite-time
    blowup, i.e. the NaN case the gate was built for.  0 of 3 genuinely convergent
    controls is falsely flagged.

**These are CHARACTERIZATION assertions, not soundness assertions.**  They encode what
the predicate does today so the behaviour cannot change silently, following the
precedent set by leg 69's `test_interval_stress.py`.  `solver/marginal_flow.py` was NOT
modified by leg 83 -- the gate's `no` branch forbids patching under the leg's own
authority.  When an authorised leg repairs the predicate, `test_currently_missed_*`
below will START FAILING; that is the intended signal, and the correct response is to
flip those cases from `assert converged is True` to `assert converged is False`, never
to weaken them so a repair looks unnecessary.

The mechanism, in one line: every clause of `converged` is an observable of the inner
Newton solve or of IEEE finiteness, and none is an observable of the state.

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


def test_4_currently_missed_polynomial_and_exponential_growth():
    """(4) CHARACTERIZATION -- unbounded growth with a healthy inner solve is NOT caught.

    Six members, ground truth `divergent` by closed form, every one reported
    `converged = True`.  The magnitudes are asserted as well as the verdict, so that a
    partial repair (one that catches some) is visible as a specific failure rather than
    a silent change of subject.
    """
    expect = {                    # name: (min state growth factor, exact law)
        "mu_linear": (1e2, "mu = mu0 + tau"),
        "mu_quartic": (1e6, "mu = (1+tau)^4"),
        "b_quadratic": (1e3, "b = (1+tau)^2"),
        "mu_exp_mild": (1e12, "mu = 0.3 e^{tau/2}"),
        "mu_exp_extreme": (1e120, "mu = 0.3 e^{5 tau}"),
        "mu_negative_runaway": (1e12, "mu = -0.3 e^{tau/2}"),
    }
    for name, (floor_growth, law) in expect.items():
        r = rows()[name]
        assert r["fidelity_ok"], (name, r["fidelity_criterion"])
        assert r["state_growth_factor"] > floor_growth, (name, r["state_growth_factor"])
        # the characterization: currently MISSED
        assert r["gate11_converged"] is True, (
            name, "gate 11 now catches this -- see the module docstring, flip the "
                  "assertion rather than weakening it")
        # and WHICH clause let it through: all three, comfortably
        assert r["clause_finite"] is True, (name, r)
        assert r["clause_no_nan_break"] is True, (name, r)
        assert r["worst_newton_residual_over_floor"] < 1.0, (name, r)
        print(f"  (4) {name:<22s} {law:<20s} state grew "
              f"{r['state_growth_factor']:.2e}x, Newton residual/floor "
              f"{r['worst_newton_residual_over_floor']:.2e} "
              f"({r['newton_headroom']:.1e}x below the threshold) -> converged=True")


def test_5_currently_missed_sustained_oscillation():
    """(5) CHARACTERIZATION -- a trajectory with NO LIMIT AT ALL is not caught either.

    `osc_sustained` is a pure rotation: the exact amplitude is 1 for all time, so the
    trajectory has no limit and never decays, while nothing about it is large.  This is
    the member that separates "the predicate misses BIG numbers" from "the predicate
    does not look at the state at all" -- it is missed at amplitude O(1).
    """
    for name in ("osc_sustained", "osc_growing"):
        r = rows()[name]
        assert r["fidelity_ok"], (name, r["fidelity_criterion"])
        assert 0.5 <= r["numerical_damping_factor"] <= 2.0, (name, r)
        assert r["gate11_converged"] is True, (name, "flip, do not weaken")
        assert r["worst_newton_residual_over_floor"] < 1.0, (name, r)
        print(f"  (5) {name:<22s} amplitude {r['amp_end_computed']:.4f} at tau=20 "
              f"({r['numerical_damping_factor']:.3f} of exact), Newton residual/floor "
              f"{r['worst_newton_residual_over_floor']:.2e} -> converged=True")


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
    assert len(missed) == 8, [r["name"] for r in missed]
    assert len(caught) == 1 and caught[0]["name"] == "nan_finite_time_blowup", caught
    assert len(conv) == 3 and not fp, (len(conv), fp)
    assert len(excluded) == 1, [r["name"] for r in excluded]

    worst = max(missed, key=lambda r: r["state_growth_factor"])
    head = min(r["newton_headroom"] for r in missed)
    assert worst["state_growth_factor"] > 1e120, worst["state_growth_factor"]
    assert head > 1e7, head
    print(f"  (7) gate 11 catch coverage on non-NaN divergence: {len(caught)}/{len(div)} "
          f"caught, {len(missed)}/{len(div)} MISSED, {len(fp)}/{len(conv)} false "
          f"positives, {len(excluded)} excluded on fidelity")
    print(f"      worst miss {worst['name']}: state x{worst['state_growth_factor']:.2e}, "
          f"mu_end {worst['mu_end']:.3e}; every missed case sits at least "
          f"{head:.1e}x below the 1e8 Newton threshold")


def test_8_the_predicate_has_no_state_clause_at_all():
    """(8) THE MECHANISM, asserted directly rather than inferred from the misses.

    Two trajectories, identical in every inner-solve observable and 13 decades apart in
    the state.  If the predicate had ANY state clause -- a bound on |mu|, a growth
    ratio, a Cauchy tail -- these two could not agree.  They agree, which is the finding
    stated without reference to any particular adversarial case.
    """
    r_ok = rows()["exact_fixed_point"]
    r_bad = rows()["mu_exp_mild"]
    assert r_ok["gate11_converged"] == r_bad["gate11_converged"] is True, (r_ok, r_bad)
    assert r_ok["clause_finite"] == r_bad["clause_finite"] is True
    assert r_ok["clause_no_nan_break"] == r_bad["clause_no_nan_break"] is True
    ratio = r_bad["state_growth_factor"] / max(r_ok["state_growth_factor"], 1.0)
    assert ratio > 1e12, ratio

    # and the same statement made against the source: the record `integrate` returns
    # carries the state, so the information is present and simply unused.
    A = MFG.SyntheticFlow(1, *MFG._scalar_mu(lambda u: 0.5 * u, lambda u: 0.5))
    rec = integrate(A, [1.0], 0.3, 20.0, 0.25, n_sample=80)
    assert rec["converged"] is True
    assert np.isfinite(rec["mu_end"]) and rec["mu_end"] > 1e3, rec["mu_end"]
    assert set(("mu", "b_end", "mu_end")) <= set(rec), sorted(rec)
    print(f"  (8) the fixed point and a state {ratio:.1e}x larger are given the SAME "
          f"verdict on all three clauses; `rec` carries mu_end={rec['mu_end']:.3e} and "
          f"the predicate reads none of it")


if __name__ == "__main__":
    import time
    t0 = time.time()
    for fn in (test_1_the_harness_is_not_degenerate,
               test_2_the_design_case_is_still_caught,
               test_3_no_false_positives_on_genuinely_convergent_flows,
               test_4_currently_missed_polynomial_and_exponential_growth,
               test_5_currently_missed_sustained_oscillation,
               test_6_the_fidelity_gate_excludes_what_the_integrator_did_not_reproduce,
               test_7_the_headline_counts,
               test_8_the_predicate_has_no_state_clause_at_all):
        print(f"\n{fn.__name__}")
        fn()
    print(f"\nALL GATES PASS ({time.time() - t0:.0f}s)")
