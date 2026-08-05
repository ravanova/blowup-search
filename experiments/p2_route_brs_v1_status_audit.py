"""Route-BRS v1: does `solver/boussinesq_rescaled.py` ever CALL a limit-cycling run converged?

Leg 81.  A STATUS-REPORTING audit, not a physics leg.  It changes no parameter, runs no
sweep, computes no beta (leg 43's ban is on a physics number obtained by relaxing the 2D
object; the quantity here is a boolean field in a returned dict and the arithmetic that
sets it).  It touches `solver/boussinesq_rescaled.py` only by importing it.

THE GATE, verbatim:

  "At the grid refinement levels where Route-K already measured the residual GROWING
   (limit-cycling), does solver/boussinesq_rescaled.py's own relaxation loop ever report a
   converged/stable status?"

The audit has four parts, and only A1+A2 answer the gate.

  A1  THE PREDICATE AGAINST THE LADDER ON RECORD.  The refinement rungs are read out of
      writeup/data/ (Route-G's committed resolution ladder, Route-K's steps ladder) and are
      NOT re-run.  The module's own exit predicate `res < tol` is evaluated at every rung,
      at every tolerance any caller in this repository actually passes, and the margin is
      reported in DECADES.  A recorded FINAL residual is decisive for the whole run, not
      just its endpoint: `run()` breaks the instant `res < tol` and returns that same `res`,
      so a final residual of 1.7e-02 at tol=1e-09 proves no intermediate step of that run
      was below tolerance either.

  A2  THE LOOP ITSELF, REPLAYED.  A subclass of RescaledBoussinesq whose `rhs`/`step` are
      overridden to emit a SCRIPTED residual sequence: no PDE, no velocity solve, no
      modulation constant -- just the real `run()` control flow, driven over the shapes on
      record (the recorded limit cycle) and over adversarial shapes that are not.

  A3  THE REPORTING LAG, measured.  `step()` computes `res` from the state it was GIVEN,
      then returns the state one SSPRK3 stage later; with renorm=True the returned fields
      are rescaled after that.  So `residual` in the result dict is not the residual of
      `omega/eta/xi` in the same dict.  Magnitude reported, on the replay where the true
      sequence is known exactly.

  A4  EDGE CASES of the exit paths: non-finite residual, the 1e8 divergence cut, max_steps=0.

Deterministic, seconds, no PDE solve.  Writes writeup/data/p2_route_brs_v1_status_audit.json.

Run: .venv/bin/python -u experiments/p2_route_brs_v1_status_audit.py
"""

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.boussinesq_rescaled import RescaledBoussinesq   # noqa: E402
from solver.boussinesq_velocity import PolarGrid            # noqa: E402

OUT = ROOT / "writeup" / "data" / "p2_route_brs_v1_status_audit.json"
ROUTE_G = ROOT / "writeup" / "data" / "p2_route_g_v1_g2.json"
ROUTE_K = ROOT / "writeup" / "data" / "p2_route_k_v1_port.json"

GATE = ("At the grid refinement levels where Route-K already measured the residual GROWING "
        "(limit-cycling), does solver/boussinesq_rescaled.py's own relaxation loop ever "
        "report a converged/stable status?")

# Every tolerance any caller in this repository passes to RescaledBoussinesq.run, with the
# call site, grepped rather than assumed.  The signature default is the loosest of them.
TOLERANCES = [
    (1e-6,  "solver/boussinesq_rescaled.py:239 (signature default)"),
    (1e-7,  "writeup/3_spikes/spike0_rescaling_evidence.py:66"),
    (1e-9,  "experiments/p2_route_g_v1_collapse.py:136 and "
            "experiments/spike1_stepC_gate.py:102 (the ladder ON RECORD)"),
    (1e-12, "experiments/p2_route_k_v1_port.py:63 and "
            "experiments/p2_route_l_v1_precond.py:56"),
]


# ---------------------------------------------------------------------------------------
# A1 -- the exit predicate, against the refinement ladder already on record
# ---------------------------------------------------------------------------------------

def a1_predicate_vs_recorded_ladder():
    g = json.loads(ROUTE_G.read_text())["g2_our_beta"]
    k = json.loads(ROUTE_K.read_text())["K1_K2_no_fixed_point"]

    rungs = []
    for r in g["resolution_ladder"]:
        rungs.append({"source": "Route-G g2 resolution_ladder (writeup/data/p2_route_g_v1_g2.json)",
                      "kind": "grid refinement", "n_r": r["n_r"], "n_beta": r["n_beta"],
                      "r_max": r["r_max"], "steps": r["steps"],
                      "tol_used_by_that_run": 1e-9, "residual": float(r["residual"])})
    for r in g["steps_ladder"]:
        rungs.append({"source": "Route-G g2 steps_ladder (writeup/data/p2_route_g_v1_g2.json)",
                      "kind": "steps at n_r=300", "n_r": 300, "n_beta": 48, "r_max": 1e5,
                      "steps": r["steps"], "tol_used_by_that_run": 1e-9,
                      "residual": float(r["residual"])})
    kg = k["grid"]
    for r in k["steps_ladder"]:
        rungs.append({"source": "Route-K K1 steps_ladder (writeup/data/p2_route_k_v1_port.json)",
                      "kind": "steps at n_r=200", "n_r": kg["n_r"], "n_beta": kg["n_beta"],
                      "r_max": kg["r_max"], "steps": r["steps"],
                      "tol_used_by_that_run": 1e-12,
                      "residual": float(r["residual_sup"])})

    for row in rungs:
        row["margin_decades"] = {}
        row["predicate_fires"] = {}
        for tol, _site in TOLERANCES:
            row["margin_decades"][f"{tol:g}"] = float(math.log10(row["residual"] / tol))
            row["predicate_fires"][f"{tol:g}"] = bool(row["residual"] < tol)

    # The growth Route-K measured, restated from the record so the gate's premise is visible.
    res_ref = [r for r in rungs if r["kind"] == "grid refinement"]
    by_nr = sorted([r for r in res_ref if r["r_max"] == 1e5], key=lambda r: r["n_r"])
    growth = {"n_r": [r["n_r"] for r in by_nr],
              "residual": [r["residual"] for r in by_nr],
              "growth_factor_coarsest_to_finest": by_nr[-1]["residual"] / by_nr[0]["residual"]}
    k_steps = [r for r in rungs if r["kind"] == "steps at n_r=200"]
    r_k = [r["residual"] for r in k_steps]
    growth["route_k_limit_cycle_fall_then_climb"] = {
        "steps": [r["steps"] for r in k_steps], "residual": r_k,
        "fall_factor": r_k[0] / min(r_k), "climb_factor_after_minimum": r_k[-1] / min(r_k)}

    worst = min(rungs, key=lambda r: r["residual"])
    summary = {
        "n_rungs": len(rungs),
        "n_rungs_where_predicate_fires": {
            f"{tol:g}": sum(r["predicate_fires"][f"{tol:g}"] for r in rungs)
            for tol, _ in TOLERANCES},
        "smallest_residual_ever_recorded": worst["residual"],
        "closest_approach_decades": {
            f"{tol:g}": float(math.log10(worst["residual"] / tol)) for tol, _ in TOLERANCES},
        "closest_rung": {kk: worst[kk] for kk in ("source", "n_r", "steps", "residual")},
        # A run that exits via `res < tol` RETURNS that res.  Every recorded final residual
        # is >> its own run's tol, so no intermediate step of any recorded run fired either.
        # DISTINCT steps only: the two steps ladders are CUMULATIVE checkpoints of one run
        # each (400->4000, 500->5000), so they count once at their deepest rung, not summed.
        "step_evaluations_covered_by_that_argument": int(
            sum(r["steps"] for r in rungs if r["kind"] == "grid refinement")
            + max(r["steps"] for r in rungs if r["kind"] == "steps at n_r=300")
            + max(r["steps"] for r in rungs if r["kind"] == "steps at n_r=200")),
        "step_count_note": ("distinct step evaluations, not a sum over overlapping "
                            "checkpoints: 4 refinement rungs x 2500, plus the deepest "
                            "checkpoint of each of the two cumulative steps ladders"),
    }
    return {"tolerances_in_use": [{"tol": t, "call_site": s} for t, s in TOLERANCES],
            "rungs": rungs, "premise_restated_from_record": growth, "summary": summary}


# ---------------------------------------------------------------------------------------
# A2 -- the loop's own control flow, driven by a scripted residual sequence
# ---------------------------------------------------------------------------------------

class ScriptedRelaxation(RescaledBoussinesq):
    """The REAL `run()` loop, with the physics removed.

    `rhs` and `step` are the only two places `run()` touches the PDE.  Overriding them with
    a scripted residual sequence exercises the loop's dt logic, its histories, its two break
    branches and its result-dict assembly, with no velocity solve and no modulation constant
    anywhere.  Fields are advanced by a harmless marker (+1 per step) so the returned state
    can be identified.
    """

    def __init__(self, grid, residuals):
        super().__init__(grid)
        self.script = [float(x) for x in residuals]
        self.calls = 0

    def _res_at(self, i):
        return self.script[min(i, len(self.script) - 1)]

    def rhs(self, omega, eta, xi):
        z = np.zeros_like(omega)
        info = dict(c_l=1.0, c_omega=-1.0, c_theta=0.0, cfl_speed=1.0,
                    omega_x0=1.0, eta_x0=1.0, u_x0=-1.0)
        return z, z, z, info

    def step(self, omega, eta, xi, dt):
        res = self._res_at(self.calls)
        self.calls += 1
        _, _, _, info = self.rhs(omega, eta, xi)
        one = np.ones_like(omega)
        return omega + one, eta + one, xi + one, info, res


def _tiny_grid():
    # 16x8 -- the loop never solves on it; it exists so odd_field_x_slope has a grid.
    return PolarGrid(n_r=16, n_beta=8, r_min=1e-2, r_max=1e2)


def _replay(grid, residuals, tol, max_steps=None, renorm=False):
    s = ScriptedRelaxation(grid, residuals)
    n = max_steps if max_steps is not None else len(residuals)
    f = np.ones((grid.n_r, grid.n_beta))
    r = s.run(f.copy(), f.copy(), f.copy(), dt_frac=0.3, tol=tol, max_steps=n, renorm=renorm)
    return s, r


def a2_loop_replay(a1):
    grid = _tiny_grid()
    rec = a1["rungs"]
    cases = []

    # (a) the recorded limit cycle itself: Route-K's four checkpoints, as a residual
    #     sequence, at each tolerance any caller uses.
    kcyc = [r["residual"] for r in rec if r["kind"] == "steps at n_r=200"]
    # (b) the recorded refinement ladder's residuals, in refinement order (they GROW).
    gref = [r["residual"] for r in rec if r["kind"] == "grid refinement"]
    # (c) the recorded steps ladder at n_r=300.
    gstp = [r["residual"] for r in rec if r["kind"] == "steps at n_r=300"]

    for label, seq in (("route_k_limit_cycle_checkpoints", kcyc),
                       ("route_g_refinement_residuals", gref),
                       ("route_g_steps_residuals", gstp)):
        for tol, _site in TOLERANCES:
            s, r = _replay(grid, seq * 8, tol)          # 8 laps of the cycle
            cases.append({"case": label, "tol": tol, "sequence_len": len(seq) * 8,
                          "steps_taken": int(r["steps"]), "exhausted_max_steps":
                          bool(r["steps"] == len(seq) * 8),
                          "reported_residual": float(r["residual"]),
                          "reported_converged": bool(r["converged"]),
                          "min_residual_in_sequence": float(min(seq)),
                          "margin_decades_at_minimum": float(math.log10(min(seq) / tol))})

    # (d) THE ADVERSARIAL CONTROL, deliberately outside anything on record: a limit cycle
    #     that dips one single step below tolerance and climbs straight back out.  This is
    #     the shape that WOULD fool the predicate; the audit measures how far it is from
    #     the shapes actually observed.
    adv = []
    for tol, _site in TOLERANCES:
        dip = 0.1 * tol
        seq = [2.5e-1, 2.6e-2, dip, 2.3e-1, 1.9e-1]
        s, r = _replay(grid, seq, tol, max_steps=len(seq))
        true_next = seq[min(int(r["steps"]), len(seq) - 1)]
        adv.append({"case": "single_step_dip_below_tol", "tol": tol, "dip": dip,
                    "steps_taken": int(r["steps"]),
                    "reported_converged": bool(r["converged"]),
                    "reported_residual": float(r["residual"]),
                    "residual_of_the_state_actually_returned": float(true_next),
                    "lag_mismatch_decades": float(math.log10(true_next / r["residual"])),
                    "decades_below_smallest_recorded_residual":
                        float(math.log10(a1["summary"]["smallest_residual_ever_recorded"] / dip))})

    # (e) a genuinely convergent sequence -- the control that shows the flag CAN fire, so
    #     the `no` answer is not a broken instrument.
    conv = []
    for tol, _site in TOLERANCES:
        seq = [1.0 * 10.0 ** (-p) for p in range(0, 20)]
        s, r = _replay(grid, seq, tol, max_steps=len(seq))
        conv.append({"case": "monotone_decade_decay", "tol": tol,
                     "steps_taken": int(r["steps"]),
                     "reported_converged": bool(r["converged"]),
                     "reported_residual": float(r["residual"]),
                     "predicate_consistent": bool(r["converged"] == (r["residual"] < tol))})

    return {"recorded_shapes": cases, "adversarial_dip": adv, "positive_control": conv}


# ---------------------------------------------------------------------------------------
# A3 -- the reporting lag between `residual` and the state returned beside it
# ---------------------------------------------------------------------------------------

def a3_reporting_lag():
    grid = _tiny_grid()
    seq = [10.0 ** (-p) for p in range(0, 8)]           # one decade per step
    s, r = _replay(grid, seq, tol=1e-30, max_steps=6)   # tol unreachable: full 6 steps
    reported = float(r["residual"])
    true_of_returned = seq[6]
    marker = float(r["omega"].max() - 1.0)              # steps actually applied to the state

    # renorm=True additionally rescales the returned fields AFTER res was measured.
    s2, r2 = _replay(grid, seq, tol=1e-30, max_steps=6, renorm=True)
    return {
        "what": ("step() computes res from the state it was GIVEN and returns the state one "
                 "SSPRK3 update later; run() stores that res beside the LATER state."),
        "scripted_sequence": seq,
        "steps_requested": 6,
        "field_marker_steps_applied": marker,
        "reported_residual": reported,
        "residual_of_the_state_returned_beside_it": true_of_returned,
        "lag_decades_on_a_one_decade_per_step_sequence": float(
            math.log10(reported / true_of_returned)),
        "lag_steps": 1,
        "renorm_true_also_rescales_after_measurement": True,
        "renorm_reported_residual": float(r2["residual"]),
        "history_lengths_equal_steps": bool(len(r["res_hist"]) == int(r["steps"])),
        "consequence": ("`converged=True` certifies the residual of the PREDECESSOR of the "
                        "returned iterate, not of the returned iterate.  It is a labelling "
                        "lag of exactly one step, it never manufactures a sub-tolerance "
                        "number, and at the recorded rungs it is unreachable -- see A1."),
    }


# ---------------------------------------------------------------------------------------
# A4 -- the other exit paths
# ---------------------------------------------------------------------------------------

def a4_edge_cases():
    grid = _tiny_grid()
    out = []

    s, r = _replay(grid, [1.0, np.nan, 1e-30], tol=1e-6, max_steps=3)
    out.append({"case": "non_finite_residual", "steps_taken": int(r["steps"]),
                "reported_converged": bool(r["converged"]),
                "reported_residual_is_finite": bool(np.isfinite(r["residual"])),
                "note": "NaN < tol is False in IEEE, and the 1e8 branch breaks first"})

    s, r = _replay(grid, [1.0, 1e9, 1e-30], tol=1e-6, max_steps=3)
    out.append({"case": "divergence_cut_1e8", "steps_taken": int(r["steps"]),
                "reported_converged": bool(r["converged"]),
                "reported_residual": float(r["residual"])})

    err = None
    try:
        _replay(grid, [1.0], tol=1e-6, max_steps=0)
    except Exception as exc:                                  # noqa: BLE001
        err = f"{type(exc).__name__}: {exc}"
    out.append({"case": "max_steps_zero", "raises": err,
                "note": ("`step` is the loop variable; with max_steps=0 the loop body never "
                         "runs and `step + 1` is unbound.  A robustness wart on a path no "
                         "caller in this repository takes -- reported, not patched.")})

    # The predicate is *by construction* the same expression as the break, so it cannot
    # disagree with itself; recorded explicitly because that is the property being audited.
    src = (ROOT / "solver" / "boussinesq_rescaled.py").read_text().splitlines()
    out.append({"case": "predicate_identity",
                "break_line": next(l.strip() for l in src if l.strip() == "if res < tol:"),
                "report_line": next(l.strip() for l in src if "converged=res < tol" in l),
                "note": ("one expression, `res < tol`, used for both the break and the "
                         "label -- there is no second, looser 'stable' predicate anywhere "
                         "in the module: the strings 'stable', 'resolution-stable' and "
                         "'plateau' do not occur in it."),
                "status_words_in_module": {
                    w: sum(l.lower().count(w) for l in src)
                    for w in ("converged", "stable", "plateau", "success")}})
    return out


def main():
    t0 = time.time()
    a1 = a1_predicate_vs_recorded_ladder()
    a2 = a2_loop_replay(a1)
    a3 = a3_reporting_lag()
    a4 = a4_edge_cases()

    fires_anywhere = any(v for v in a1["summary"]["n_rungs_where_predicate_fires"].values())
    replay_fires = any(c["reported_converged"] for c in a2["recorded_shapes"])
    answer = "YES" if (fires_anywhere or replay_fires) else "NO"

    closest = a1["summary"]["closest_approach_decades"]
    verdict = (
        "NO. Across the {n} rungs on record -- Route-G's grid-refinement ladder "
        "(n_r=300/450/600, residual GROWING {gf:.1f}x) and Route-G's and Route-K's steps "
        "ladders (the limit cycle: falls {ff:.0f}x, climbs {cf:.1f}x back) -- the module's "
        "exit predicate `res < tol` fires at ZERO rungs at every tolerance any caller "
        "passes. The closest approach is {rmin:.3e}, which is {d9:.1f} decades above the "
        "tol=1e-9 those runs used and {d6:.1f} decades above the signature default 1e-6. "
        "Because run() returns the residual it broke on, that covers every one of the "
        "{ne} step evaluations in those runs, not just their endpoints. Replaying the "
        "recorded residual shapes through the real run() loop reports converged=False on "
        "{nc}/{nc} cases, while a monotone decade-decay control fires correctly -- so the "
        "negative is the module's, not the instrument's."
    ).format(n=a1["summary"]["n_rungs"],
             gf=a1["premise_restated_from_record"]["growth_factor_coarsest_to_finest"],
             ff=a1["premise_restated_from_record"]["route_k_limit_cycle_fall_then_climb"]["fall_factor"],
             cf=a1["premise_restated_from_record"]["route_k_limit_cycle_fall_then_climb"]["climb_factor_after_minimum"],
             rmin=a1["summary"]["smallest_residual_ever_recorded"],
             d9=closest["1e-09"], d6=closest["1e-06"],
             ne=a1["summary"]["step_evaluations_covered_by_that_argument"],
             nc=len(a2["recorded_shapes"]))

    doc = {
        "leg": "Leg 81 -- Route-BRS v1",
        "title": "Status-reporting audit of solver/boussinesq_rescaled.py against the "
                 "refinement ladder already on record",
        "generated": time.strftime("%Y-%m-%d"),
        "gate_verbatim": GATE,
        "gate_answer": answer,
        "verdict": verdict,
        "physics_run_by_this_leg": "none -- rungs are read from writeup/data/, the loop is "
                                   "driven by a scripted residual sequence",
        "module_edited": False,
        "A1_predicate_vs_recorded_ladder": a1,
        "A2_loop_replay": a2,
        "A3_reporting_lag": a3,
        "A4_edge_cases": a4,
        "secondary_observations": [
            "A3: `residual` in the result dict lags the returned state by exactly one step "
            "(and, with renorm=True, is measured before the rescaling). Not reachable at any "
            "recorded rung; reported, not patched.",
            "A4: run(max_steps=0) raises UnboundLocalError on `step + 1`. No caller in this "
            "repository passes 0.",
            "A2(d): a single-step dip below tol WOULD be reported converged -- but the "
            "residual would have to fall {loose:.1f} decades below anything ever recorded on "
            "this object at the LOOSEST tolerance in use (1e-6), and {rec:.1f} decades below "
            "it at the 1e-9 the recorded runs actually used, for that path to be "
            "reachable.".format(
                loose=min(a["decades_below_smallest_recorded_residual"]
                          for a in a2["adversarial_dip"]),
                rec=next(a["decades_below_smallest_recorded_residual"]
                         for a in a2["adversarial_dip"] if a["tol"] == 1e-9)),
        ],
        "wall_clock_seconds": time.time() - t0,
    }
    OUT.write_text(json.dumps(doc, indent=1))
    print(verdict)
    print(f"\nwrote {OUT.relative_to(ROOT)}  ({doc['wall_clock_seconds']:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
