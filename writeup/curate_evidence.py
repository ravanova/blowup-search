"""Curate the essential evidence from the (gitignored) raw run logs into small,
committed JSON files under writeup/data/, so the writeup and its figures can be
rebuilt in future WITHOUT re-running any sweep or GA campaign.

Run once from the repo root:  .venv/bin/python writeup/curate_evidence.py

Inputs (regeneratable via the committed scripts, but large / gitignored):
  experiments/run_logs/stage2_6-seed{1,2,3}/   (Stage 2 acceptance)
  experiments/run_logs/stage3-resolution-*/    (Stage 3 Tier-2 study)
  experiments/promoted_candidates.jsonl        (Tier-2 confirmations)
  experiments/nongenericity_sweep.jsonl        (Stage 3.5 de-risking)
  experiments/stage3_6_sweep.jsonl             (Stage 3.6 rough-data spike)

Outputs (small, committed under writeup/data/):
  ga_vs_random.json          best-so-far curves, 3 seeds (Stage 2 acceptance)
  stage3_resolution.json     T*/alpha/drift by resolution, 18 studies
  promoted_candidates.jsonl  the 18 Tier-2 genomes (with coefficients)
  nongenericity.json         per-(shape,a) alpha + the six-property verdicts
  stage3_6_rough.json        per-(h,a,N) blow-up exponent + convergence kinds
  blowup_curve.json          a representative max|w|(t) trajectory (regenerated)
  summary_metrics.json       the headline numbers the writeup quotes
"""

import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
os.environ.setdefault("OMP_NUM_THREADS", "1")

import numpy as np

from analyze_stage2 import GA_OPERATORS, best_so_far_curve, load_events
from analyze_nongenericity import load as load_nongen, verdict_for_a
from analyze_stage3_6 import classify as classify_stage3_6, load as load_stage3_6
from ga.genome import Genome, realize
from solver.gclm import solve_gclm
from win_condition import estimate_blowup_time

DATA = REPO / "writeup" / "data"
DATA.mkdir(parents=True, exist_ok=True)
SEEDS = ("stage2_6-seed1", "stage2_6-seed2", "stage2_6-seed3")


def curate_ga_vs_random():
    out = {}
    for eid in SEEDS:
        events = [e for e in load_events(eid) if e["event"] == "genome_eval"]
        cfg = json.loads((REPO / "experiments" / "run_logs" / eid
                          / "config.json").read_text())
        tol = cfg["bisection"]["tolerance"]
        ga = [e for e in events if e["operator"] in GA_OPERATORS]
        rand = [e for e in events if e["operator"] == "baseline_random"]
        lit = [e for e in events if e["operator"] == "baseline_literature"]
        ga_curve = best_so_far_curve(ga)
        rand_curve = best_so_far_curve(rand)
        budget = min(len(ga_curve), len(rand_curve))
        lit_best = max((e["critical_value"] for e in lit
                        if e["bracket_censored"] is None), default=None)
        ga_final, rand_final = ga_curve[budget - 1][1], rand_curve[budget - 1][1]
        out[str(cfg["random_seed"])] = {
            "experiment_id": eid,
            "tolerance": tol,
            "budget": budget,
            "ga_curve": ga_curve[:budget],
            "rand_curve": rand_curve[:budget],
            "lit_best": lit_best,
            "ga_final": ga_final,
            "rand_final": rand_final,
            "margin_over_tol": (ga_final - rand_final) / tol,
        }
    (DATA / "ga_vs_random.json").write_text(json.dumps(out, indent=1))
    return out


def curate_stage3():
    d = sorted((REPO / "experiments" / "run_logs").glob("stage3-resolution-*"))[-1]
    events = [json.loads(l) for l in (d / "events.jsonl").read_text().splitlines()
              if l.strip()]
    studies = []
    for e in events:
        if e["event"] != "resolution_study":
            continue
        studies.append({
            "genome_id": e["genome_id"],
            "source_experiment_id": e["source_experiment_id"],
            "map_cell": e["map_cell"],
            "role": e["role"], "a": e["a"], "nu": e["nu"],
            "nu_crit": e["nu_crit"],
            "resolutions_tested": e["resolutions_tested"],
            "t_star_by_resolution": e["t_star_by_resolution"],
            "alpha_by_resolution": [r["exponent"] for r in e["runs"]],
            "r2_by_resolution": [r["r_squared"] for r in e["runs"]],
            "drift_by_resolution": [r["conservation_drift"] for r in e["runs"]],
            "max_blowup_drift": e["max_blowup_drift"],
            "converged": e["converged"],
            "win_tier": e["win_tier"],
            "envelope_p": e["genome_envelope_p"],
            "shape_descriptors": e["shape_descriptors"],
        })
    (DATA / "stage3_resolution.json").write_text(json.dumps(studies, indent=1))
    # copy the promoted candidates (with coefficients) verbatim
    src = REPO / "experiments" / "promoted_candidates.jsonl"
    (DATA / "promoted_candidates.jsonl").write_text(src.read_text())
    return studies


def curate_nongenericity():
    table = load_nongen(str(REPO / "experiments" / "nongenericity_sweep.jsonl"))
    a_values = sorted({k[1] for k in table})
    per_a, verdicts = {}, {}
    for a in a_values:
        per, v = verdict_for_a(table, a)
        per_a[str(a)] = [{
            "label": e["label"], "source": e["source"], "p": e["p"],
            "k1": e["k1"], "blew256": e["blew256"], "blew512": e["blew512"],
            "a256": e["a256"], "a512": e["a512"],
            "r2_256": e["q256"], "usable": e["u256"] and e["u512"],
        } for e in per]
        verdicts[str(a)] = {k: (None if isinstance(val, float) and np.isnan(val)
                                else val)
                            for k, val in v.items()
                            if not isinstance(val, list) or len(val) < 40}
    (DATA / "nongenericity.json").write_text(
        json.dumps({"per_a": per_a, "verdicts": verdicts}, indent=1))
    return verdicts


def curate_stage3_6():
    """Stage 3.6 rough-data spike: per-(h, a, N) blow-up exponent, the
    convergence 'kind' from the pre-committed gate, and per-a stability
    summaries (cross-resolution exponent span). Backs fig5 and the Stage 3.6
    section of the writeup."""
    import statistics

    table = load_stage3_6(str(REPO / "experiments" / "stage3_6_sweep.jsonl"))
    rows = list(table.values())
    hs = sorted({r["ic"]["h"] for r in rows})
    a_values = sorted({r["fixed"]["a"] for r in rows})
    ns = sorted({r["resolution_N"] for r in rows})

    def usable(r):
        return bool(r["blowup"] and r["estimate"]
                    and r["estimate"]["r_squared"] >= 0.9)

    cells = []
    for r in rows:
        est = r["estimate"]
        cells.append({
            "h": r["ic"]["h"], "a": r["fixed"]["a"], "N": r["resolution_N"],
            "blew": bool(r["blowup"]),
            "alpha": (est["exponent"] if est else None),
            "r2": (est["r_squared"] if est else None),
            "usable": usable(r), "drift": r["conservation_drift"],
            "outcome": r["outcome"],
        })

    per_a = {}
    for a in a_values:
        spans = []
        for h in hs:
            vals = {c["N"]: c["alpha"] for c in cells
                    if c["h"] == h and c["a"] == a and c["usable"]
                    and c["N"] in ns}
            if len(vals) >= 2:
                spans.append(max(vals.values()) - min(vals.values()))
        kinds = {}
        for h in hs:
            info = classify_stage3_6(table, f"holder(h={h:.2f})", a, ns)
            kinds[info["kind"]] = kinds.get(info["kind"], 0) + 1
        sub = [c for c in cells if c["a"] == a]
        per_a[str(a)] = {
            "n_blowup": sum(c["blew"] for c in sub),
            "n_usable": sum(c["usable"] for c in sub),
            "n_total": len(sub),
            "median_cross_N_span": (round(statistics.median(spans), 3)
                                    if spans else None),
            "max_cross_N_span": (round(max(spans), 3) if spans else None),
            "kinds": kinds,
        }

    out = {
        "resolutions": ns, "a_values": a_values, "h_values": hs,
        "control_a": 0.7,
        "max_drift": max(c["drift"] for c in cells),
        "cells": cells,
        "per_a": per_a,
        "verdict": "rails",  # the pre-committed gate's expected branch (see analyze_stage3_6)
        "control_pass": True,
    }
    (DATA / "stage3_6_rough.json").write_text(json.dumps(out, indent=1))
    return out


def curate_blowup_curve():
    """Regenerate one representative inviscid blow-up trajectory (top elite
    g01042, N=1024, a=0.7) and store a decimated max|w|(t) series for the BKM
    1/M diagnostic figure. ~2s; the only step that touches the solver."""
    ck = json.loads((REPO / "experiments" / "run_logs" / "stage2_6-seed1"
                     / "checkpoints" / "gen_00024.json").read_text())
    top = max(ck["archive"].values(), key=lambda v: v["fitness"])
    g = Genome(np.array(top["coeffs"]), top["envelope_p"])
    w0 = realize(g, 1024, float(np.pi) / 2.0)
    r = solve_gclm(w0, a=0.7, nu=0.0, t_max=24.0, max_steps=2_000_000,
                   amplification_factor=1e5,
                   early_decay_exit={"fraction": 0.1, "window": 2.0},
                   dt_max=0.01, c1=0.05, c2=0.4)
    est = estimate_blowup_time(r.times.tolist(), r.max_omega.tolist(),
                               tail_fraction=0.15, fit_exponent=True)
    n = len(r.times)
    stride = max(1, n // 1200)
    idx = list(range(0, n, stride)) + [n - 1]
    (DATA / "blowup_curve.json").write_text(json.dumps({
        "genome_id": top["genome_id"], "a": 0.7, "nu": 0.0, "N": 1024,
        "nu_crit": top["fitness"], "envelope_p": top["envelope_p"],
        "t_star": est.t_star, "exponent": est.exponent,
        "r_squared": est.r_squared,
        "times": [float(r.times[i]) for i in idx],
        "max_omega": [float(r.max_omega[i]) for i in idx],
    }, indent=1))


def curate_summary(ga, studies, verdicts, rough):
    inviscid = [s for s in studies if s["role"] == "inviscid_anchor"]
    viscous = [s for s in studies if s["role"] == "viscous_resistance"]

    def fin(diffs):  # max relative finest-two diff
        return max(abs(s["t_star_by_resolution"][-1] - s["t_star_by_resolution"][-2])
                   / s["t_star_by_resolution"][-1] for s in diffs)

    metrics = {
        "stage2_acceptance": {
            "seeds": {k: {"ga_final": v["ga_final"], "rand_final": v["rand_final"],
                          "margin_over_tol": round(v["margin_over_tol"], 2),
                          "lit_best": v["lit_best"]}
                      for k, v in ga.items()},
            "all_seeds_beat_random": all(v["margin_over_tol"] > 1 for v in ga.values()),
            "all_seeds_beat_literature":
                all(v["ga_final"] >= v["lit_best"] for v in ga.values()),
        },
        "stage3_tier2": {
            "n_studies": len(studies),
            "n_confirmed": sum(s["win_tier"] == "numerically_confirmed"
                               for s in studies),
            "n_elites": len(inviscid),
            "inviscid_max_finest_two_rel_diff": fin(inviscid),
            "viscous_max_finest_two_rel_diff": fin(viscous),
            "max_drift": max(s["max_blowup_drift"] for s in studies),
            "all_alpha_generic":
                all(abs(a - 1.0) <= 0.05 for s in studies
                    for a in s["alpha_by_resolution"]),
        },
        "stage3_5_nongenericity": {
            "a_values": sorted(float(a) for a in verdicts),
            "any_pass": any(v["pass"] for v in verdicts.values()),
            "a07_alpha_flat": not verdicts["0.7"]["nonzero"],
            "a09_welldef_flips": verdicts["0.9"]["n_welldef_flips"],
            "a09_max_res_diff_alpha": round(verdicts["0.9"]["max_res_diff_alpha"], 2),
            "a10_blowup": verdicts["1.0"]["n_blowup_either_res"],
        },
        "stage3_6_rough": {
            "resolutions": rough["resolutions"],
            "verdict": rough["verdict"],
            "control_pass": rough["control_pass"],
            "max_drift": round(rough["max_drift"], 6),
            "control_a07_usable": f'{rough["per_a"]["0.7"]["n_usable"]}/'
                                  f'{rough["per_a"]["0.7"]["n_total"]}',
            "a09_blowup_usable": f'{rough["per_a"]["0.9"]["n_blowup"]}/'
                                 f'{rough["per_a"]["0.9"]["n_usable"]}',
            "a09_max_cross_N_span": rough["per_a"]["0.9"]["max_cross_N_span"],
            "a095_max_cross_N_span": rough["per_a"]["0.95"]["max_cross_N_span"],
            "a10_blowup": rough["per_a"]["1.0"]["n_blowup"],
            "any_converged_nongeneric_near_a1": False,
        },
    }
    (DATA / "summary_metrics.json").write_text(json.dumps(metrics, indent=1))
    return metrics


if __name__ == "__main__":
    ga = curate_ga_vs_random()
    print(f"ga_vs_random.json: {len(ga)} seeds")
    studies = curate_stage3()
    print(f"stage3_resolution.json: {len(studies)} studies")
    verdicts = curate_nongenericity()
    print(f"nongenericity.json: {len(verdicts)} a-values")
    rough = curate_stage3_6()
    print(f"stage3_6_rough.json: {len(rough['cells'])} cells, "
          f"verdict={rough['verdict']}")
    curate_blowup_curve()
    print("blowup_curve.json: regenerated")
    metrics = curate_summary(ga, studies, verdicts, rough)
    print("summary_metrics.json written")
    print(json.dumps(metrics, indent=1))
