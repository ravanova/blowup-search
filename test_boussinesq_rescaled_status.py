"""Leg 81 (Route-BRS): the STATUS-REPORTING contract of `RescaledBoussinesq.run`.

`capabilities.py` records, for `solver/boussinesq_rescaled.py`, that "Route-K showed the
relaxation LIMIT-CYCLES and its residual GROWS under refinement, so 'resolution-stable' here
is not 'converged'".  That is a statement about the OBJECT.  These tests are the statement
about the CODE that nothing in the repository previously made: at the refinement levels where
the residual is on record as GROWING, the module must never label the run converged, and its
label must agree with its own exit predicate on every path out of the loop.

Nothing here runs the PDE: rungs are read from `writeup/data/` (Route-G's committed
refinement ladder, Route-K's steps ladder) and the loop is driven by a SCRIPTED residual
sequence via `ScriptedRelaxation`, shared with the audit runner so the test and the banked
result cannot drift apart.  No parameter is swept and no `beta` is measured.

Run:  python test_boussinesq_rescaled_status.py
"""

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments"))

from solver.boussinesq_velocity import PolarGrid                      # noqa: E402
from p2_route_brs_v1_status_audit import (                            # noqa: E402
    ScriptedRelaxation, TOLERANCES, ROUTE_G, ROUTE_K,
)

# The margin the leg measured, kept as a floor rather than an equality so that a genuinely
# better relaxation is free to improve it -- but a rung that gets within 3 decades of ANY
# tolerance in use is a change of regime this test must force someone to look at.
MIN_MARGIN_DECADES = 3.0


def _grid():
    """16x8. The loop never solves on it; it exists so odd_field_x_slope has a grid."""
    return PolarGrid(n_r=16, n_beta=8, r_min=1e-2, r_max=1e2)


def _replay(residuals, tol, max_steps=None, renorm=False):
    g = _grid()
    s = ScriptedRelaxation(g, residuals)
    n = max_steps if max_steps is not None else len(residuals)
    f = np.ones((g.n_r, g.n_beta))
    return s.run(f.copy(), f.copy(), f.copy(), dt_frac=0.3, tol=tol, max_steps=n,
                 renorm=renorm)


def _recorded_rungs():
    """Every residual on record for this object, with the grid it was measured on."""
    g = json.loads(ROUTE_G.read_text())["g2_our_beta"]
    k = json.loads(ROUTE_K.read_text())["K1_K2_no_fixed_point"]
    rows = [("Route-G refine n_r=%d" % r["n_r"], r["n_r"], r["steps"], float(r["residual"]))
            for r in g["resolution_ladder"]]
    rows += [("Route-G steps %d" % r["steps"], 300, r["steps"], float(r["residual"]))
             for r in g["steps_ladder"]]
    rows += [("Route-K steps %d" % r["steps"], k["grid"]["n_r"], r["steps"],
              float(r["residual_sup"])) for r in k["steps_ladder"]]
    return rows


# ---------------------------------------------------------------------------------------
# (1) the premise: the record really does show the residual GROWING under refinement
# ---------------------------------------------------------------------------------------

def test_premise_residual_grows_under_refinement():
    g = json.loads(ROUTE_G.read_text())["g2_our_beta"]
    lad = sorted([r for r in g["resolution_ladder"] if r["r_max"] == 1e5],
                 key=lambda r: r["n_r"])
    assert len(lad) >= 3, "the committed refinement ladder lost rungs"
    res = [float(r["residual"]) for r in lad]
    growth = res[-1] / res[0]
    assert growth > 1.0, f"record no longer shows growth under refinement: {res}"
    print(f"[ok] (1) premise intact: n_r={[r['n_r'] for r in lad]} residual "
          f"{res[0]:.3e} -> {res[-1]:.3e}, GROWING {growth:.1f}x")


# ---------------------------------------------------------------------------------------
# (2) THE GATE: the exit predicate fires at none of the recorded rungs, at any tolerance
# ---------------------------------------------------------------------------------------

def test_predicate_never_fires_at_recorded_rungs():
    rows = _recorded_rungs()
    worst = math.inf
    for label, n_r, steps, res in rows:
        for tol, _site in TOLERANCES:
            margin = math.log10(res / tol)
            assert not (res < tol), (
                f"FALSE-POSITIVE CONVERGENCE: {label} recorded residual {res:.3e} is below "
                f"tol={tol:g} -- the module would report converged at a rung the record "
                f"says limit-cycles")
            worst = min(worst, margin)
    assert worst > MIN_MARGIN_DECADES, (
        f"closest approach to a tolerance in use is {worst:.2f} decades, under the "
        f"{MIN_MARGIN_DECADES} floor -- the regime changed, re-run the leg-81 audit")
    print(f"[ok] (2) {len(rows)} recorded rungs x {len(TOLERANCES)} tolerances in use: "
          f"the predicate fires 0 times, closest approach {worst:.1f} decades")


# ---------------------------------------------------------------------------------------
# (3) the same, through the real run() loop rather than by arithmetic on the record
# ---------------------------------------------------------------------------------------

def test_loop_reports_not_converged_on_recorded_shapes():
    rows = _recorded_rungs()
    seq = [r[3] for r in rows]
    n = 0
    for tol, _site in TOLERANCES:
        r = _replay(seq * 4, tol)
        assert not r["converged"], (
            f"run() reported converged=True replaying the recorded residual sequence at "
            f"tol={tol:g}, residual {r['residual']:.3e}")
        assert r["steps"] == len(seq) * 4, (
            f"loop exited early ({r['steps']} of {len(seq) * 4}) without converging")
        n += 1
    print(f"[ok] (3) the recorded limit-cycle shape replayed through run(): "
          f"converged=False and max_steps exhausted at all {n} tolerances")


# ---------------------------------------------------------------------------------------
# (4) the positive control -- the flag CAN fire, so (2) and (3) are not a dead instrument
# ---------------------------------------------------------------------------------------

def test_positive_control_flag_does_fire():
    for tol, _site in TOLERANCES:
        seq = [10.0 ** (-p) for p in range(0, 20)]
        r = _replay(seq, tol)
        assert r["converged"], f"monotone decade decay failed to converge at tol={tol:g}"
        assert r["residual"] < tol
        assert r["steps"] < len(seq), "converged but did not stop"
    print(f"[ok] (4) positive control: a monotone decade decay is reported converged at all "
          f"{len(TOLERANCES)} tolerances -- the negative above is the module's, not the test's")


# ---------------------------------------------------------------------------------------
# (5) the invariant: the LABEL never disagrees with the module's own exit predicate
# ---------------------------------------------------------------------------------------

def test_label_agrees_with_predicate_on_every_exit_path():
    rng = np.random.default_rng(81)
    checked = 0
    for trial in range(60):
        n = int(rng.integers(2, 12))
        seq = list(10.0 ** rng.uniform(-14.0, 1.0, size=n))
        tol = float(TOLERANCES[int(rng.integers(0, len(TOLERANCES)))][0])
        r = _replay(seq, tol)
        assert bool(r["converged"]) == bool(r["residual"] < tol), (
            f"label/predicate disagree: converged={r['converged']} residual="
            f"{r['residual']:.3e} tol={tol:g} seq={seq}")
        assert len(r["res_hist"]) == r["steps"], "history length != reported steps"
        checked += 1
    print(f"[ok] (5) label == (residual < tol) on {checked} randomized exit paths, "
          f"histories consistent with the reported step count")


# ---------------------------------------------------------------------------------------
# (6) the two abnormal exits must never be labelled converged
# ---------------------------------------------------------------------------------------

def test_blowup_and_nan_are_never_converged():
    r = _replay([1.0, 1e9, 1e-30], tol=1e-6, max_steps=3)
    assert not r["converged"] and r["residual"] > 1e8, "divergence cut mislabelled"
    assert r["steps"] == 2, f"divergence cut fired late ({r['steps']})"

    r = _replay([1.0, np.nan, 1e-30], tol=1e-6, max_steps=3)
    assert not r["converged"], "NaN residual reported as converged"
    assert not np.isfinite(r["residual"]), "NaN residual was silently replaced"
    print("[ok] (6) the 1e8 divergence cut and a NaN residual both exit with "
          "converged=False and hand back the offending number rather than hiding it")


# ---------------------------------------------------------------------------------------
# (7) CHARACTERIZATION: `residual` lags the returned state by exactly one step
# ---------------------------------------------------------------------------------------

def test_reported_residual_lags_returned_state_by_one_step():
    """Not a defect at any reachable rung -- see leg 81 A3 -- but it IS a property callers
    can be surprised by, so it is pinned: if someone repairs it, this test says so."""
    seq = [10.0 ** (-p) for p in range(0, 8)]
    r = _replay(seq, tol=1e-30, max_steps=6)
    applied = float(r["omega"].max() - 1.0)
    assert applied == 6.0, f"the stub applied {applied} updates, expected 6"
    lag = math.log10(r["residual"] / seq[6])
    assert abs(lag - 1.0) < 1e-9, (
        f"the one-step reporting lag changed (measured {lag:.3f} decades on a "
        f"one-decade-per-step sequence) -- update writeup/novelty/leg_81.md A3")
    print(f"[ok] (7) reported residual {r['residual']:.1e} is the PREDECESSOR of the "
          f"returned iterate ({seq[6]:.1e}): a lag of exactly 1 step, {lag:.1f} decade here")


# ---------------------------------------------------------------------------------------
# (8) there is no second, looser status word for a caller to be fooled by
# ---------------------------------------------------------------------------------------

def test_module_exposes_exactly_one_status_predicate():
    src = (ROOT / "solver" / "boussinesq_rescaled.py").read_text()
    low = src.lower()
    for word in ("stable", "plateau", "success", "steady_state_reached"):
        assert low.count(word) == 0, f"a second status word appeared in the module: {word!r}"
    assert src.count("converged=res < tol") == 1, "the status expression moved or multiplied"
    assert src.count("if res < tol:") == 1, "the break predicate moved or multiplied"
    print("[ok] (8) one predicate, `res < tol`, used for both the break and the label; "
          "0 occurrences of 'stable' / 'plateau' / 'success' anywhere in the module")


if __name__ == "__main__":
    test_premise_residual_grows_under_refinement()
    test_predicate_never_fires_at_recorded_rungs()
    test_loop_reports_not_converged_on_recorded_shapes()
    test_positive_control_flag_does_fire()
    test_label_agrees_with_predicate_on_every_exit_path()
    test_blowup_and_nan_are_never_converged()
    test_reported_residual_lags_returned_state_by_one_step()
    test_module_exposes_exactly_one_status_predicate()
    print("\nALL BOUSSINESQ-RESCALED STATUS-REPORTING TESTS PASSED")
