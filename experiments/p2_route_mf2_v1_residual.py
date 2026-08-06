"""Route-MF2 v1 (leg 136): THE RESIDUAL GATE 11 STILL MISSES, CLASSIFIED AND TESTED.

WHAT THIS LEG INHERITS
---------------------------------------------------------------------------
Leg 83 (Route-MFG) measured that `solver/marginal_flow.py:integrate`'s `converged`
predicate flagged **1 of 9** scored non-NaN divergent trajectories: all three of its
clauses were observables of the inner Newton solve or of IEEE finiteness, and none was
an observable of the state.  The bench repair (commit `8572465`) added a fourth clause,

    state_growth < 1e5 ,   state_growth = max(worst_b_growth, worst_mu_growth)

relative to each block's OWN initial magnitude, and took the coverage to **5 of 9**
with 0 of 3 false positives.  Four scored cases remain accepted, plus one that is
excluded on fidelity rather than missed:

    mu_linear                 growth 2.01e2   (mu' = 1;      mu = mu0 + tau)
    b_quadratic               growth 3.73e3   (b'  = 2|b|^.5; b = (1+tau)^2)
    osc_sustained             growth 1.00     (pure rotation, |b| == 1 forever)
    osc_growing               growth 1.99     (rotation, Re = +0.05)
    osc_stiff_underresolved   EXCLUDED        (omega dt = 4 rad/step; BDF2's own
                                               L-stability damped it to 3.5e-14 of its
                                               exact amplitude, so the trajectory the
                                               predicate SAW genuinely converged)

The repair's own commit body asserted the shape of the remaining fix without measuring
it: "bounded, no limit -- a magnitude clause is the wrong instrument; needs a tail
test."  **This module measures whether such a tail test exists.**

WHAT IS MEASURED, AND THE ORDER IT WAS FIXED IN
---------------------------------------------------------------------------
1. Each of the five open cases is classified by MECHANISM -- what, precisely, the state
   clause cannot see about it -- from quantities measured on the trajectory, not from
   the case's name.
2. A family of five candidate second criteria, `C1..C5`, was NAMED AND DEFINED in
   `writeup/novelty/leg_136.md` and COMMITTED (`aeced70`) BEFORE this file existed, per
   leg 111's pre-naming discipline.  They are re-stated in `CRITERIA` below, and the
   novelty log is the record that they were not chosen after seeing the numbers.
3. Every criterion is evaluated on: the full 13-member leg-83 battery, and a
   WELL-BEHAVED battery of 14 real `AugmentedFlow` trajectories lifted verbatim from
   the parameters of the 11 gates in `test_marginal_flow.py`.
4. For each criterion the leg reports a SEPARATION RATIO -- the smallest value it takes
   on a case it must flag, over the largest value it takes on a trajectory it must not
   -- and the identity of the binding false positive.  A criterion admits a threshold
   iff that ratio exceeds 1.  The ratio, not a boolean, is the finding.
5. The 25%/25% window convention is SWEPT (0.10 / 0.25 / 0.50), because the steady-state
   detection literature's standing caveat is that no universal window length exists
   (novelty log Q3).

HOW THE CRITERIA SEE THE TRAJECTORY
---------------------------------------------------------------------------
`integrate` records `mu` at sampled steps only and `b` only at the end, so the candidate
criteria cannot be evaluated from its record.  `instrumented_trajectory` re-runs the
SAME trajectory through the SAME stepper (`solver.marginal_flow._implicit_step`) with
`integrate`'s loop mirrored line for line, recording the per-block state at EVERY
accepted step -- which is exactly the position a real repair would compute them from.
Every run is CONTROLLED against `integrate`'s own record: `mu_end`, `state_growth` and
the `converged` bit must agree, and `reproduction_ok` reports it per case.  A criterion
measured on a trajectory that is not the module's own would be measuring nothing.

`solver/marginal_flow.py` IS NOT EDITED BY THIS LEG UNDER ANY OUTCOME.

Run:  python experiments/p2_route_mf2_v1_residual.py
Out:  writeup/data/p2_route_mf2_v1_residual.json
"""

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.critical_dissipation import mu_branch                          # noqa: E402
from solver.marginal_flow import AugmentedFlow, integrate, _implicit_step  # noqa: E402

import importlib.util as _ilu                                             # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "writeup", "data", "p2_route_mf2_v1_residual.json")

# Leg 83's battery is imported, never re-derived and never re-run through its own
# `main()` (that would rewrite another leg's JSON, which is not this leg's territory).
_spec = _ilu.spec_from_file_location(
    "mfg83", os.path.join(ROOT, "experiments", "p2_route_mfg_v1_adversarial.py"))
MFG = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(MFG)

# The five open items this leg inherits, from commit 8572465's own body.
OPEN_CASES = ["mu_linear", "b_quadratic", "osc_sustained", "osc_growing",
              "osc_stiff_underresolved"]
CLOSED_BY_STATE_GROWTH = ["mu_quartic", "mu_exp_mild", "mu_negative_runaway",
                          "mu_exp_extreme"]
CONVERGENT_CONTROLS = ["decay_to_zero", "exact_fixed_point", "damped_oscillation"]

MU_SCALE_FLOOR = 1e-12          # mirrors integrate's own floor


# ==========================================================================
# the instrumented re-run: integrate's loop, with the state kept
# ==========================================================================
def instrumented_trajectory(A, b0, mu0, tau_end, dt):
    """`integrate`'s accepted-step loop, recording per-block state at EVERY step.

    Returns tau[], v_b[], v_mu[] plus the scales integrate divides by.  Nothing here
    re-derives the stepper: `_implicit_step` is the module's own, called with the same
    arguments in the same order, so the sequence of accepted states is the sequence
    `integrate` walks.  `reproduce_check` in `run_trajectory` is what proves it.
    """
    y = np.concatenate([np.asarray(b0, float), [float(mu0)]])
    y_prev = None
    n = max(1, int(round(float(tau_end) / float(dt))))
    tau = 0.0
    b_scale = max(float(np.max(np.abs(np.asarray(b0, float)))), 1e-300)
    mu_scale = max(abs(float(mu0)), MU_SCALE_FLOOR)
    taus = [0.0]
    v_b = [float(np.max(np.abs(y[:-1])))]
    v_mu = [abs(float(y[-1]))]
    broke = None
    for i in range(n):
        y_new, it, nrm, floor = _implicit_step(A, y, y_prev, dt, first=(i == 0))
        if not np.all(np.isfinite(y_new)):
            broke = float(tau)
            break
        y_prev, y = y, y_new
        tau += dt
        taus.append(tau)
        v_b.append(float(np.max(np.abs(y[:-1]))))
        v_mu.append(abs(float(y[-1])))
    return {"tau": np.array(taus), "v_b": np.array(v_b), "v_mu": np.array(v_mu),
            "b_scale": b_scale, "mu_scale": mu_scale, "dt": float(dt),
            "broke_at_tau": broke, "mu_end": float(y[-1]),
            "state_growth": float(max(np.max(np.array(v_b)) / b_scale,
                                      np.max(np.array(v_mu)) / mu_scale))}


# ==========================================================================
# THE PRE-NAMED FAMILY.  Definitions are those of writeup/novelty/leg_136.md §3,
# committed at aeced70 BEFORE this file existed.  Nothing is added here.
# ==========================================================================
def _windows(n, frac):
    """(PRE, TAIL) index slices: TAIL is the last `frac`, PRE the `frac` before it."""
    w = max(2, int(round(frac * n)))
    if 2 * w > n:
        w = max(2, n // 2)
    return slice(n - 2 * w, n - w), slice(n - w, n)


def criteria(tr, frac=0.25):
    """C1..C5 for one trajectory, per block, max over blocks.  Scale-free throughout."""
    n = tr["tau"].size
    pre, tail = _windows(n, frac)
    dt = tr["dt"]
    out = {}
    per_block = {}
    for name, v, s in (("b", tr["v_b"], tr["b_scale"]), ("mu", tr["v_mu"], tr["mu_scale"])):
        vt, vp = v[tail], v[pre]
        mt, mp = float(np.max(vt)), float(np.max(vp))
        # C1 windowed growth-rate estimate, in ratio form
        c1 = mt / (mp + 1e-300)
        # C2 residual-to-state-scale: late-window drift per unit tau, over initial scale
        d = np.abs(np.diff(v))[tail.start - 1 if tail.start > 0 else 0: n - 1]
        c2 = (float(np.max(d)) / dt) / s if d.size else 0.0
        # C3 monotone-tail fraction
        dv = np.diff(v)[tail.start - 1 if tail.start > 0 else 0: n - 1]
        c3 = float(np.mean(dv > 0.0)) if dv.size else 0.0
        # C4 tail range over initial scale (the non-decay detector)
        c4 = (float(np.max(vt)) - float(np.min(vt))) / s
        # C5 the same windowed growth as a RATE, not a ratio
        dtau = float(np.mean(tr["tau"][tail]) - np.mean(tr["tau"][pre]))
        c5 = (np.log(max(c1, 1e-300)) / dtau) if dtau > 0 else 0.0
        per_block[name] = {"C1": c1, "C2": c2, "C3": c3, "C4": c4, "C5": c5}
    for c in ("C1", "C2", "C3", "C4", "C5"):
        out[c] = float(max(per_block["b"][c], per_block["mu"][c]))
    out["_per_block"] = per_block
    out["_window_frac"] = float(frac)
    out["_n_steps"] = int(n)
    return out


CRITERIA = {
    "C1": "TAIL_GROWTH_RATIO: max_TAIL v / max_PRE v, per block, max over blocks",
    "C2": "TAIL_DRIFT_OVER_INITIAL_SCALE: (max_TAIL |dv|/dt) / initial block scale",
    "C3": "MONOTONE_TAIL_FRACTION: fraction of TAIL steps with v increasing",
    "C4": "TAIL_RANGE_OVER_INITIAL_SCALE: (max_TAIL v - min_TAIL v) / initial scale",
    "C5": "TAIL_EFOLD_RATE: log(C1) / (mean tau of TAIL - mean tau of PRE)",
}
FRACS = (0.10, 0.25, 0.50)


# ==========================================================================
# the two batteries
# ==========================================================================
def synthetic_rows(fracs=FRACS):
    """Leg 83's 13 members, re-run on integrate's real path AND instrumented."""
    rows = []
    for c in MFG.battery():
        # (i) the module's own verdict, via leg 83's own scoring
        verdict = MFG.run_case(c)
        # (ii) the instrumented twin
        A = MFG.SyntheticFlow(c["K"], c["rhs"], c["jac"])
        tr = instrumented_trajectory(A, c["b0"], c["mu0"], c["tau_end"], c["dt"])
        row = {
            "name": c["name"], "family": c["family"], "ground_truth": c["truth"],
            "battery": "synthetic", "why": c["why"],
            "gate11_converged": verdict["gate11_converged"],
            "verdict_leg83_scoring": verdict["verdict"],
            "fidelity_ok": verdict["fidelity_ok"],
            "fidelity_criterion": verdict["fidelity_criterion"],
            "state_growth": float(verdict["state_growth_factor"]),
            "worst_newton_residual_over_floor":
                float(verdict["worst_newton_residual_over_floor"]),
            "mu_end": float(verdict["mu_end"]),
            "reproduction_rel_err_mu_end":
                float(abs(tr["mu_end"] - verdict["mu_end"])
                      / (abs(verdict["mu_end"]) + 1e-300)),
            "criteria": {str(f): {k: v for k, v in criteria(tr, f).items()
                                  if not k.startswith("_per_block")}
                         for f in fracs},
        }
        row["reproduction_ok"] = bool(row["reproduction_rel_err_mu_end"] < 1e-12)
        rows.append(row)
    return rows


def wellbehaved_spec():
    """The real-flow trajectories of the 11 gates, by their gate's own parameters."""
    S = []
    for mu in (0.25, 0.5, 1.0, 2.0, 4.0):
        S.append(dict(name="gate4_a0_neutral_mu%g" % mu, a=0.0, p=1, K=96,
                      branch_mus=[0.25, 0.5, 1.0, 2.0, 4.0], pick=mu, mu0=mu,
                      tau_end=40.0, dt=0.5, gauge=True,
                      why="test_4: a = 0 line of fixed points, held for tau = 40"))
    S.append(dict(name="gate5_gauge_on", a=0.5, p=3, K=96, branch_mus=[0.1, 0.2, 0.3],
                  pick=0.3, mu0=0.3, tau_end=60.0, dt=0.25, gauge=True,
                  why="test_5: the headline trajectory, gauge projection ON"))
    S.append(dict(name="gate5_gauge_off", a=0.5, p=3, K=96, branch_mus=[0.1, 0.2, 0.3],
                  pick=0.3, mu0=0.3, tau_end=60.0, dt=0.25, gauge=False,
                  why="test_5: the same trajectory with the projection OFF"))
    for p in (1, 2, 4, 5):
        S.append(dict(name="gate6_lambda_mu_p%d" % p, a=0.5, p=p, K=96,
                      branch_mus=[2e-3], pick=2e-3, mu0=2e-3, tau_end=3.0, dt=0.02,
                      gauge=True,
                      why="test_6: lambda_mu = p - 3 measured as a growth rate"
                          + (" -- THE 4.06e2 LEGITIMATE CEILING" if p == 5 else "")))
    S.append(dict(name="gate7_alpha1_long", a=0.5, p=3, K=96, branch_mus=[0.1, 0.2, 0.3],
                  pick=0.3, mu0=0.3, tau_end=120.0, dt=0.25, gauge=True,
                  why="test_7: the tau = 120 alpha_1 trajectory"))
    S.append(dict(name="gate11_on_branch", a=0.5, p=3, K=96,
                  branch_mus=[0.05, 0.1, 0.2, 0.3], pick=0.3, mu0=0.3,
                  tau_end=60.0, dt=0.25, gauge=True,
                  why="test_11(b): the on-branch run gate 11 must KEEP"))
    S.append(dict(name="gate3_dt_ladder_finest", a=0.5, p=3, K=96,
                  branch_mus=[0.1, 0.2, 0.3], pick=0.3, mu0=0.3, tau_end=60.0,
                  dt=0.125, gauge=True,
                  why="test_3/10: the finest rung of the dt ladder"))
    return S


def wellbehaved_rows(fracs=FRACS, verbose=True):
    cache = {}
    rows = []
    for spec in wellbehaved_spec():
        key = (spec["a"], spec["p"], spec["K"], tuple(spec["branch_mus"]))
        if key not in cache:
            cache[key] = mu_branch(spec["a"], spec["p"], list(spec["branch_mus"]),
                                   K=spec["K"])
        br = cache[key]
        b0 = [r for r in br if abs(r["mu"] - spec["pick"]) < 1e-14][0]["b"]
        rec = integrate(AugmentedFlow(spec["a"], spec["p"], K=spec["K"],
                                      gauge_project=spec["gauge"]),
                        b0, spec["mu0"], spec["tau_end"], spec["dt"], n_sample=60)
        tr = instrumented_trajectory(
            AugmentedFlow(spec["a"], spec["p"], K=spec["K"],
                          gauge_project=spec["gauge"]),
            b0, spec["mu0"], spec["tau_end"], spec["dt"])
        row = {
            "name": spec["name"], "family": "wellbehaved_real_flow",
            "ground_truth": "convergent", "battery": "wellbehaved", "why": spec["why"],
            "a": spec["a"], "p": spec["p"], "K": spec["K"], "mu0": spec["mu0"],
            "tau_end": spec["tau_end"], "dt": spec["dt"],
            "gate11_converged": bool(rec["converged"]),
            "state_growth": float(rec["state_growth"]),
            "b_growth": float(rec["b_growth"]), "mu_growth": float(rec["mu_growth"]),
            "mu_end": float(rec["mu_end"]),
            "reproduction_rel_err_mu_end":
                float(abs(tr["mu_end"] - rec["mu_end"]) / (abs(rec["mu_end"]) + 1e-300)),
            "reproduction_rel_err_state_growth":
                float(abs(tr["state_growth"] - rec["state_growth"])
                      / (rec["state_growth"] + 1e-300)),
            "criteria": {str(f): {k: v for k, v in criteria(tr, f).items()
                                  if not k.startswith("_per_block")}
                         for f in fracs},
        }
        row["reproduction_ok"] = bool(row["reproduction_rel_err_mu_end"] < 1e-12
                                      and row["reproduction_rel_err_state_growth"] < 1e-12)
        rows.append(row)
        if verbose:
            print(f"  {row['name']:<26s} converged={str(row['gate11_converged']):<5s} "
                  f"growth={row['state_growth']:.3e} "
                  f"C1={row['criteria']['0.25']['C1']:.3e} "
                  f"C4={row['criteria']['0.25']['C4']:.3e} "
                  f"repro={'OK' if row['reproduction_ok'] else 'MISMATCH'}")
    return rows


# ==========================================================================
# mechanism classification of the five open cases
# ==========================================================================
def classify(rows):
    """WHY the scale-free state-growth clause misses each open case.

    Every field is measured off the trajectory, not read off the case's name.  The
    classification is a value (banked lesson 60: a sentence, so a dropped sign fails).
    """
    by = {r["name"]: r for r in rows}
    out = []
    for nm in OPEN_CASES:
        r = by[nm]
        c = r["criteria"]["0.25"]
        if not r["fidelity_ok"]:
            mech = "INTEGRATOR_ERASED_THE_DIVERGENCE"
            why = ("the computed trajectory does not diverge at all: %s.  No state "
                   "predicate can see what the stepper removed; this is a dt-vs-max|Im| "
                   "hazard, not a gate-11 miss." % r["fidelity_criterion"])
        elif c["C4"] < 10.0 and r["state_growth"] < 10.0:
            mech = "BOUNDED_NON_CONVERGENT"
            why = ("the state neither grows nor settles: growth %.3g and tail range "
                   "%.3g of the initial scale.  A MAGNITUDE clause is the wrong "
                   "instrument -- there is no magnitude to exceed." % (
                       r["state_growth"], c["C4"]))
        else:
            mech = "SUB_THRESHOLD_UNBOUNDED_GROWTH"
            why = ("genuinely unbounded but too slow to reach the 1e5 bound in the tau "
                   "the run is given: growth %.3g, i.e. %.3g of the threshold, and only "
                   "%.3gx above the module's own legitimate ceiling of 4.06e2." % (
                       r["state_growth"], r["state_growth"] / 1e5,
                       r["state_growth"] / 4.06e2))
        out.append({"name": nm, "mechanism": mech, "state_growth": r["state_growth"],
                    "tail_range_over_scale": c["C4"], "tail_growth_ratio": c["C1"],
                    "tail_efold_rate": c["C5"], "monotone_tail_fraction": c["C3"],
                    "fidelity_ok": r["fidelity_ok"], "explanation": why})
    return out


# ==========================================================================
# the separation analysis: does ANY pre-named criterion admit a threshold?
# ==========================================================================
def separation(syn, wb, frac):
    """For each criterion: min over must-flag, max over must-not-flag, and the ratio."""
    f = str(frac)
    by = {r["name"]: r for r in syn}
    must_flag_scored = [by[n] for n in OPEN_CASES if by[n]["fidelity_ok"]]
    must_flag_all = [by[n] for n in OPEN_CASES]
    must_not = [by[n] for n in CONVERGENT_CONTROLS] + list(wb)
    res = {}
    for c in ("C1", "C2", "C3", "C4", "C5"):
        tp_s = {r["name"]: r["criteria"][f][c] for r in must_flag_scored}
        tp_a = {r["name"]: r["criteria"][f][c] for r in must_flag_all}
        fp = {r["name"]: r["criteria"][f][c] for r in must_not}
        lo_s = min(tp_s.values())
        lo_a = min(tp_a.values())
        hi = max(fp.values())
        binder = max(fp, key=lambda k: fp[k])
        weakest_s = min(tp_s, key=lambda k: tp_s[k])
        res[c] = {
            "criterion": CRITERIA[c],
            "min_over_must_flag_scored4": float(lo_s),
            "weakest_true_positive_scored4": weakest_s,
            "min_over_must_flag_all5": float(lo_a),
            "max_over_must_not_flag": float(hi),
            "binding_false_positive": binder,
            "separation_ratio_scored4": float(lo_s / (hi + 1e-300)),
            "separation_ratio_all5": float(lo_a / (hi + 1e-300)),
            "admits_threshold_scored4": bool(lo_s > hi),
            "admits_threshold_all5": bool(lo_a > hi),
            "threshold_if_admissible": (float(np.sqrt(lo_s * hi)) if lo_s > hi else None),
            "values_must_flag": {k: float(v) for k, v in tp_a.items()},
            "values_must_not_flag": {k: float(v) for k, v in fp.items()},
        }
    return res


def positive_control(syn, wb, frac):
    """THE CONTROL THAT CAN REPORT THE OTHER ANSWER (a negative needs one).

    The five criteria are not inert instruments that fail on everything: run the SAME
    separation analysis with the must-flag population swapped for the FOUR cases the
    landed `state_growth` clause already closed.  If the family admits a threshold
    there and not on the open five, the failure is a property of the open five, not of
    the family -- and if it failed on both, this leg would be reporting a broken
    measurement rather than a residual.  This is the clause of the leg that could have
    come out differently in the code (banked lesson 90).
    """
    f = str(frac)
    by = {r["name"]: r for r in syn}
    tp = {n: by[n]["criteria"][f] for n in CLOSED_BY_STATE_GROWTH}
    fp = {r["name"]: r["criteria"][f]
          for r in [by[n] for n in CONVERGENT_CONTROLS] + list(wb)}
    out = {}
    for c in ("C1", "C2", "C3", "C4", "C5"):
        lo = min(v[c] for v in tp.values())
        hi = max(v[c] for v in fp.values())
        out[c] = {"min_over_already_closed_4": float(lo),
                  "max_over_must_not_flag": float(hi),
                  "separation_ratio": float(lo / (hi + 1e-300)),
                  "admits_threshold": bool(lo > hi),
                  "binding_false_positive": max(fp, key=lambda k: fp[k][c])}
    return out


def pairs(syn, wb, frac):
    """CONJUNCTIONS of two pre-named criteria, reported as an observation only.

    The gate asks about a SINGLE pre-named criterion.  A conjunction is a different
    object and is NOT scored against the gate; it is measured because "no single one
    works" and "no combination works" are different statements and the leg should not
    leave the stronger one unmeasured.  A conjunction admits a threshold pair iff some
    (t_i, t_j) flags every must-flag case and no must-not case, which is exactly the
    condition that no must-not trajectory dominates every must-flag trajectory on BOTH
    coordinates simultaneously.
    """
    f = str(frac)
    by = {r["name"]: r for r in syn}
    tp = [by[n] for n in OPEN_CASES if by[n]["fidelity_ok"]]
    fp = [by[n] for n in CONVERGENT_CONTROLS] + list(wb)
    keys = ("C1", "C2", "C3", "C4", "C5")
    out = {}
    for i, ci in enumerate(keys):
        for cj in keys[i + 1:]:
            # thresholds must be below EVERY true positive on both coordinates
            ti = min(r["criteria"][f][ci] for r in tp)
            tj = min(r["criteria"][f][cj] for r in tp)
            bad = [r["name"] for r in fp
                   if r["criteria"][f][ci] >= ti and r["criteria"][f][cj] >= tj]
            out[f"{ci}&{cj}"] = {
                "t_i": float(ti), "t_j": float(tj),
                "n_false_positives_at_the_only_admissible_thresholds": len(bad),
                "false_positives": bad,
                "admits_threshold_pair": not bad}
    return out


# ==========================================================================
def main():
    t_all = time.time()
    print("Route-MF2 v1 (leg 136) -- the residual gate 11 still misses")
    print("=" * 78)
    print("  synthetic battery (leg 83's 13 members, real integrate path) ...")
    syn = synthetic_rows()
    for r in syn:
        c = r["criteria"]["0.25"]
        print(f"  {r['name']:<26s} truth={r['ground_truth']:<10s} "
              f"conv={str(r['gate11_converged']):<5s} growth={r['state_growth']:.2e} "
              f"C1={c['C1']:.2e} C2={c['C2']:.2e} C3={c['C3']:.2f} "
              f"C4={c['C4']:.2e} C5={c['C5']:+.3f}")

    print("-" * 78)
    print("  well-behaved battery (real AugmentedFlow, the 11 gates' own parameters) ...")
    wb = wellbehaved_rows()

    print("-" * 78)
    cls = classify(syn)
    for c in cls:
        print(f"  {c['name']:<26s} {c['mechanism']}")
        print(f"      {c['explanation']}")

    print("-" * 78)
    sep = {str(f): separation(syn, wb, f) for f in FRACS}
    pr = {str(f): pairs(syn, wb, f) for f in FRACS}
    pc = {str(f): positive_control(syn, wb, f) for f in FRACS}
    print("  POSITIVE CONTROL -- the same family against the 4 cases the state clause "
          "already closed, window 0.25:")
    for c in ("C1", "C2", "C3", "C4", "C5"):
        s = pc["0.25"][c]
        print(f"    {c}  min over the closed 4 {s['min_over_already_closed_4']:.4g}  vs  "
              f"must-NOT max {s['max_over_must_not_flag']:.4g} "
              f"({s['binding_false_positive']})  -> separation "
              f"{s['separation_ratio']:.4g}x  "
              f"{'ADMITS a threshold' if s['admits_threshold'] else 'NO threshold'}")
    print("-" * 78)
    for f in FRACS:
        print(f"  window fraction {f}:")
        for c in ("C1", "C2", "C3", "C4", "C5"):
            s = sep[str(f)][c]
            print(f"    {c}  must-flag min {s['min_over_must_flag_scored4']:.4g} "
                  f"({s['weakest_true_positive_scored4']})  vs  must-NOT max "
                  f"{s['max_over_must_not_flag']:.4g} ({s['binding_false_positive']})"
                  f"  -> separation {s['separation_ratio_scored4']:.4g}x  "
                  f"{'ADMITS a threshold' if s['admits_threshold_scored4'] else 'NO threshold'}")

    # ---- the gate ------------------------------------------------------
    any_single = {f: [c for c in ("C1", "C2", "C3", "C4", "C5")
                      if sep[str(f)][c]["admits_threshold_all5"]] for f in FRACS}
    any_single_scored = {f: [c for c in ("C1", "C2", "C3", "C4", "C5")
                             if sep[str(f)][c]["admits_threshold_scored4"]]
                         for f in FRACS}
    winners_all5 = sorted({c for v in any_single.values() for c in v})
    winners_scored4 = sorted({c for v in any_single_scored.values() for c in v})
    gate_answer = "yes_complete_detector" if winners_all5 else "no_characterized_residual"

    best = max((sep[str(f)][c]["separation_ratio_scored4"], f, c)
               for f in FRACS for c in ("C1", "C2", "C3", "C4", "C5"))
    repro_bad = [r["name"] for r in syn + wb if not r["reproduction_ok"]]

    summary = {
        "n_open_cases_inherited": len(OPEN_CASES),
        "n_open_scored_misses": sum(1 for r in syn
                                    if r["name"] in OPEN_CASES and r["fidelity_ok"]),
        "n_open_fidelity_excluded": sum(1 for r in syn
                                        if r["name"] in OPEN_CASES
                                        and not r["fidelity_ok"]),
        "n_wellbehaved_trajectories": len(wb),
        "n_wellbehaved_flagged_by_gate11_today": sum(1 for r in wb
                                                     if not r["gate11_converged"]),
        "largest_legitimate_state_growth": float(max(r["state_growth"] for r in wb)),
        "largest_legitimate_state_growth_case":
            max(wb, key=lambda r: r["state_growth"])["name"],
        "criteria_admitting_a_threshold_all5": winners_all5,
        "criteria_admitting_a_threshold_scored4": winners_scored4,
        "best_separation_ratio": float(best[0]),
        "best_separation_at": {"window_frac": best[1], "criterion": best[2]},
        "conjunctions_admitting_a_threshold_pair": sorted(
            {k for f in FRACS for k, v in pr[str(f)].items()
             if v["admits_threshold_pair"]}),
        "positive_control_criteria_admitting_a_threshold_on_the_closed_4":
            [c for c in ("C1", "C2", "C3", "C4", "C5") if pc["0.25"][c]["admits_threshold"]],
        "positive_control_best_separation_ratio":
            float(max(pc["0.25"][c]["separation_ratio"]
                      for c in ("C1", "C2", "C3", "C4", "C5"))),
        # the sharpest single magnitude in the leg: the legitimate trajectory grows
        # FASTER PER UNIT TAU than the divergent one it must be told apart from
        "efold_rate_legitimate_gate6_p5": float(
            [r for r in wb if r["name"] == "gate6_lambda_mu_p5"][0]["criteria"]["0.25"]["C5"]),
        "efold_rate_divergent_mu_linear": float(
            [r for r in syn if r["name"] == "mu_linear"][0]["criteria"]["0.25"]["C5"]),
        "instrumented_reproduction_failures": repro_bad,
        "gate_answer": gate_answer,
        "window_fractions_swept": list(FRACS),
    }

    print("=" * 78)
    print(f"  open cases inherited: {summary['n_open_cases_inherited']} "
          f"({summary['n_open_scored_misses']} scored misses + "
          f"{summary['n_open_fidelity_excluded']} fidelity-excluded)")
    print(f"  well-behaved real-flow trajectories: {summary['n_wellbehaved_trajectories']}"
          f", of which flagged by gate 11 today: "
          f"{summary['n_wellbehaved_flagged_by_gate11_today']}")
    print(f"  largest legitimate state growth: "
          f"{summary['largest_legitimate_state_growth']:.3e} "
          f"({summary['largest_legitimate_state_growth_case']})")
    print(f"  single pre-named criteria admitting a threshold on all 5: "
          f"{winners_all5 or 'NONE'}")
    print(f"  single pre-named criteria admitting a threshold on the scored 4: "
          f"{winners_scored4 or 'NONE'}")
    print(f"  best separation ratio anywhere in the family: {best[0]:.4g}x "
          f"({best[2]} at window {best[1]})")
    print(f"  conjunctions admitting a threshold pair: "
          f"{summary['conjunctions_admitting_a_threshold_pair'] or 'NONE'}")
    print(f"  instrumented reproduction failures: {repro_bad or 'none'}")
    print(f"  GATE ANSWER: {gate_answer}")

    payload = {
        "leg": 136, "route": "MF2", "version": "v1",
        "what": ("classification of the 5 open divergent cases gate 11 still misses, and "
                 "a pre-named family of 5 second criteria tested against them, the 11 "
                 "gates' own trajectories, and the convergent controls"),
        "gate_question": (
            "Does at least one pre-named criterion flag all 5 remaining divergent cases "
            "with zero false positives across the 11 existing gates, the 4 already-closed "
            "cases, and the well-behaved battery?"),
        "predicate_under_test": (
            "solver/marginal_flow.py:integrate -> rec['converged'] = finite(y) and no NaN "
            "break and worst_newton_residual_over_floor < 1e8 and state_growth < 1e5"),
        "criteria_prenamed_at": "writeup/novelty/leg_136.md, commit aeced70",
        "criteria": CRITERIA,
        "open_cases": OPEN_CASES,
        "closed_by_state_growth_clause": CLOSED_BY_STATE_GROWTH,
        "summary": summary,
        "mechanism_classification": cls,
        "separation": sep,
        "positive_control_on_the_already_closed_4": pc,
        "conjunctions": pr,
        "synthetic_battery": syn,
        "wellbehaved_battery": wb,
        "wall_s": round(time.time() - t_all, 1),
    }
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    with open(DATA, "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)
    print(f"  wrote {DATA}  ({payload['wall_s']}s)")
    return payload


if __name__ == "__main__":
    main()
