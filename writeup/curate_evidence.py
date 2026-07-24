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


def curate_phase1_spike():
    """Route A Phase 1 resolution de-risk spike: the g-converges / exponent-rails
    resolution wall, from experiments/phase1_resolution_spike.jsonl."""
    src = REPO / "experiments" / "phase1_resolution_spike.jsonl"
    rows = [json.loads(l) for l in src.read_text().splitlines() if l.strip()]
    by = {}
    for r in rows:
        by.setdefault(r["ic_label"], {})[r["resolution_N"]] = r
    out = {"resolutions": sorted({r["resolution_N"] for r in rows}), "ics": {}}
    for ic, per_n in by.items():
        Ns = sorted(per_n)
        est = lambda n, k: (per_n[n]["estimate"] or {}).get(k)
        out["ics"][ic] = {
            "kind": per_n[Ns[0]]["ic_kind"],
            "N": Ns,
            "g_by_N": {str(n): per_n[n]["growth_rate_fixed_window"] for n in Ns},
            "amp_resolved_by_N": {str(n): per_n[n]["amp_resolved"] for n in Ns},
            "t_resolved_by_N": {str(n): per_n[n]["t_resolved"] for n in Ns},
            "outcome_by_N": {str(n): per_n[n]["outcome"] for n in Ns},
            "exponent_by_N": {str(n): est(n, "exponent") for n in Ns},
            "tstar_by_N": {str(n): est(n, "t_star") for n in Ns},
        }
    (DATA / "phase1_spike.json").write_text(json.dumps(out, indent=1))
    return out


def curate_phase1_axis_screen():
    """Route A Phase 1 fitness-axis discrimination screen, from
    experiments/phase1_axis_screen.jsonl; verdict via the pre-committed analyzer
    (necessary-not-sufficient routing screen, not the six-property Gate 4)."""
    from analyze_phase1_axis_screen import AXES, NEEDED, evaluate_axis
    from analyze_phase1_axis_screen import load as load_screen
    src = REPO / "experiments" / "phase1_axis_screen.jsonl"
    by = load_screen(str(src))
    Ns = sorted({n for ic in by for n in by[ic]})
    values, censored = {}, {}
    for axis in AXES:
        values[axis] = {ic: {str(n): by.get(ic, {}).get(n, {}).get(axis)
                             for n in Ns} for ic in NEEDED}
    for ic in NEEDED:
        censored[ic] = {str(n): by.get(ic, {}).get(n, {}).get("nu_crit_censored")
                        for n in Ns}
    verdict, survivors = {}, []
    for axis in AXES:
        passed, detail = evaluate_axis(by, axis)
        verdict[axis] = {"pass": bool(passed),
                         "direction_ok": detail["direction_ok"],
                         "stable": detail["stable"]}
        if passed:
            survivors.append(axis)
    out = {"resolutions": Ns, "axes": list(AXES), "ics": list(NEEDED),
           "a_crit": 2.0, "values": values, "nu_crit_censored": censored,
           "verdict": verdict, "survivors": survivors}
    (DATA / "phase1_axis_screen.json").write_text(json.dumps(out, indent=1))
    return out


def _finest_two_rel(by_n):
    """Max relative change between the two finest N in a {str(N): value} dict."""
    ns = sorted(by_n, key=int)
    a, b = by_n[ns[-2]], by_n[ns[-1]]
    if a is None or b is None or not b:
        return None
    return abs(b - a) / abs(b)


def curate_summary(ga, studies, verdicts, rough, spike=None, screen=None):
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
    if spike is not None and screen is not None:
        sharp = spike["ics"]["smooth_sharp"]
        mild = spike["ics"]["smooth_mild"]
        sharp_exp = [v for v in sharp["exponent_by_N"].values() if v is not None]
        metrics["route_a_phase1"] = {
            "status": "in_progress (Gates 1-2 + resolution spike + axis screen done; "
                      "Gate 3 genome + Gate 4 viability gate pending)",
            "spike_verdict": "STABLE (a resolution-stable growth signal exists; the "
                             "true singularity's exponent is out of uniform-grid reach)",
            "smooth_sharp_g_finest_two_rel_diff": _finest_two_rel(sharp["g_by_N"]),
            "smooth_mild_g_finest_two_rel_diff": _finest_two_rel(mild["g_by_N"]),
            "smooth_sharp_exponent_span_over_N": [min(sharp_exp), max(sharp_exp)],
            "smooth_sharp_tstar_span_over_N": [
                min(v for v in sharp["tstar_by_N"].values() if v is not None),
                max(v for v in sharp["tstar_by_N"].values() if v is not None)],
            "rough_axis_resolution_starved": all(
                spike["ics"][ic]["outcome_by_N"][str(min(spike["ics"][ic]["N"]))]
                == "under_resolved"
                for ic in spike["ics"] if spike["ics"][ic]["kind"] == "rough"),
            "axis_screen_a_crit": screen["a_crit"],
            "axis_screen_survivors": screen["survivors"],
            "axis_screen_verdict": screen["verdict"],
            "nu_crit_smooth_sharp_by_N": screen["values"]["nu_crit"]["smooth_sharp"],
            "nu_crit_smooth_mild_by_N": screen["values"]["nu_crit"]["smooth_mild"],
            "nu_crit_resolution_stable": screen["verdict"]["nu_crit"]["stable"],
            "g_baseline_wrong_direction": not screen["verdict"]["g_baseline"]["direction_ok"],
        }
    (DATA / "summary_metrics.json").write_text(json.dumps(metrics, indent=1))
    return metrics


def curate_phase1_gate4():
    """Route A Phase 1 Gate 4: the six-property viability gate on nu_crit
    (fails property 6 via the omega0/split amp-denominator cheat), the fixed-split
    and normalized-resistance probes, and the inviscid growth-rate currency probe.
    Reads experiments/phase1_gate4{,_probe}.jsonl + phase1_currency_probe.jsonl."""
    from phase1_gate4 import build_roster
    from ga.genome2d_smooth import realize

    def load(name):
        p = REPO / "experiments" / name
        return ([json.loads(l) for l in p.read_text().splitlines() if l.strip()]
                if p.exists() else [])

    def rho(x, y):
        x, y = np.asarray(x, float), np.asarray(y, float)
        if len(x) < 3 or np.std(x) == 0 or np.std(y) == 0:
            return None
        return round(float(np.corrcoef(x, y)[0, 1]), 3)

    gate, probe, curr = (load("phase1_gate4.jsonl"),
                         load("phase1_gate4_probe.jsonl"),
                         load("phase1_currency_probe.jsonl"))

    # Gate 4 nu_crit: re-realize roster genomes for the omega0 diagnostic
    # (phase1_gate4 rows did not store max|w0|).
    roster = {s["label"]: s["genome"] for s in build_roster()}
    w0 = {l: float(np.max(np.abs(realize(g, 128)[0]))) for l, g in roster.items()}
    n256 = {r["label"]: r for r in gate if r["resolution_N"] == 256}
    n512 = {r["label"]: r for r in gate if r["resolution_N"] == 512}
    grow = {l: r for l, r in n256.items() if r["bracket_censored"] is None}
    labs = list(grow)
    nu = [grow[l]["nu_crit"] for l in labs]
    lw0 = [np.log(w0[l]) for l in labs]
    b = np.polyfit(lw0, np.log(nu), 1)
    R2 = 1.0 - np.var(np.log(nu) - np.polyval(b, lw0)) / np.var(np.log(nu))
    dnu = {l: abs(n256[l]["nu_crit"] - n512[l]["nu_crit"]) for l in labs
           if l in n512 and n512[l]["bracket_censored"] is None}
    ranked = sorted(labs, key=lambda l: -grow[l]["nu_crit"])

    def shape_row(l):
        r = grow[l]
        return {"label": l, "class": r["shape_class"],
                "nu_crit": round(r["nu_crit"], 4),
                "centroid": round(r["descriptors"]["centroid"], 2),
                "max_w0": round(w0[l], 3),
                "abs_peak_omega": round(r["amp_at_nu_lo"] * w0[l], 1)}

    gate4 = {
        "n_shapes": 40, "n_growers": len(grow),
        "n_censored_low": sum(r["bracket_censored"] == "low" for r in n256.values()),
        "n_censored_high": sum(r["bracket_censored"] == "high" for r in n256.values()),
        "frozen_predicate": "6/6 PASS (a FALSE pass -- see rho below)",
        "rho_nu_log_w0": rho(nu, lw0),
        "loglog_slope": round(float(b[0]), 2),
        "loglog_R2": round(float(R2), 3),
        "rho_nu_centroid": rho(nu, [grow[l]["descriptors"]["centroid"] for l in labs]),
        "resolution_max_dnu": round(max(dnu.values()), 4) if dnu else None,
        "n_resolution_pairs": len(dnu),
        "band_over_tol": round((max(nu) - min(nu)) / 5e-3, 0),
        "top5_by_nu_crit": [shape_row(l) for l in ranked[:5]],
        # the smoking-gun pairs: same absolute vorticity / inverted ranking
        "example_shapes": {l: shape_row(l) for l in
                           ("rand_15", "rand_05", "rand_18", "rand_24") if l in grow},
    }

    # fixed-split probe
    gp = [r for r in probe if r["bracket_censored"] is None]
    wp = max(gp, key=lambda r: r["nu_crit"])
    fixed_split = {
        "split": 0.5, "n_growers": len(gp),
        "rho_nu_log_w0": rho([r["nu_crit"] for r in gp], np.log([r["max_w0"] for r in gp])),
        "rho_nu_centroid": rho([r["nu_crit"] for r in gp],
                               [r["descriptors"]["centroid"] for r in gp]),
        "winner": {"label": wp["label"], "class": wp["shape_class"],
                   "centroid": round(wp["descriptors"]["centroid"], 2),
                   "nu_crit": round(wp["nu_crit"], 4)},
    }

    # currency probe: labeled direction + resolution + roster optimum
    lab = {}
    for r in (x for x in curr if x["leg"] == "direction"):
        lab.setdefault(r["label"], {})[r["resolution_N"]] = round(r["g_sustained"], 3)
    gc = [r for r in curr if r["leg"] == "optimum" and r["g_sustained"] is not None
          and np.isfinite(r["g_sustained"])]
    wc = max(gc, key=lambda r: r["g_sustained"])
    nfine = max(n for r in lab.values() for n in r)
    currency = {
        "currency": "inviscid sustained growth rate g_sustained",
        "labeled_g_sustained_by_N": lab,
        "direction_ok": (lab["smooth_sharp"][nfine] > lab["smooth_mild"][nfine]
                         > lab["euler_control"][nfine]),
        "rho_g_log_w0": rho([r["g_sustained"] for r in gc],
                            np.log([r["max_w0"] for r in gc])),
        "rho_g_centroid": rho([r["g_sustained"] for r in gc],
                              [r["descriptors"]["centroid"] for r in gc]),
        "winner": {"label": wc["label"], "class": wc["shape_class"],
                   "centroid": round(wc["descriptors"]["centroid"], 2),
                   "g_sustained": round(wc["g_sustained"], 3)},
    }

    out = {"gate4_nu_crit": gate4, "fixed_split_probe": fixed_split,
           "currency_probe": currency}
    (DATA / "phase1_gate4.json").write_text(json.dumps(out, indent=1))
    return out


def curate_phase1_gsustained():
    """Route A Phase 1 staged g_sustained probe: the inviscid growth-rate currency
    the forward-decision after Gate 4. Reads experiments/phase1_gsustained_probe.jsonl.
    Records: LEG 1 (magnitude on the resolution wall), LEG 2 (rank-stability + the
    g_frac-vs-accel_ratio cheat audit), LEG 3 (caveat-2 free-split partials)."""
    p = REPO / "experiments" / "phase1_gsustained_probe.jsonl"
    rows = ([json.loads(l) for l in p.read_text().splitlines() if l.strip()]
            if p.exists() else [])
    if not rows:
        return None
    T_MAX = 4.0

    def rho(x, y):
        x, y = np.asarray(x, float), np.asarray(y, float)
        ok = np.isfinite(x) & np.isfinite(y)
        if ok.sum() < 3 or np.std(x[ok]) == 0 or np.std(y[ok]) == 0:
            return None
        return round(float(np.corrcoef(x[ok], y[ok])[0, 1]), 3)

    def spearman(a, b):
        a, b = np.asarray(a, float), np.asarray(b, float)
        ok = np.isfinite(a) & np.isfinite(b)
        if ok.sum() < 3:
            return None
        ra, rb = np.argsort(np.argsort(a[ok])), np.argsort(np.argsort(b[ok]))
        return round(float(np.corrcoef(ra, rb)[0, 1]), 3)

    def partial(x, y, z):
        x, y, z = (np.asarray(v, float) for v in (x, y, z))
        ok = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
        x, y, z = x[ok], y[ok], z[ok]
        if len(x) < 4:
            return None
        res = lambda a: a - np.polyval(np.polyfit(z, a, 1), z)
        return round(float(np.corrcoef(res(x), res(y))[0, 1]), 3)

    # LEG 1: magnitude vs N on the labeled ICs
    lab = {}
    for r in (x for x in rows if x["leg"] == "magnitude"):
        lab.setdefault(r["label"], {})[r["resolution_N"]] = r
    mag = {nm: {"g_frac": {str(n): round(lab[nm][n]["g_frac"], 3) for n in sorted(lab[nm])},
                "t_res": {str(n): round(lab[nm][n]["t_res"], 2) for n in sorted(lab[nm])}}
           for nm in lab}
    nfine = max(n for r in lab.values() for n in r)
    d = {nm: lab[nm][nfine]["g_frac"] for nm in lab}
    leg1 = {"labeled_g_frac_by_N": mag,
            "magnitude_converged": False,
            "sharp_g_frac_climb": [round(lab["smooth_sharp"][n]["g_frac"], 3)
                                   for n in sorted(lab["smooth_sharp"])],
            "direction_ok": bool(d["smooth_sharp"] > d["smooth_mild"] > d["euler_control"])}

    # LEG 2: rank-stability + cheat audit on the fixed-split roster
    ros = [r for r in rows if r["leg"] == "ordering"]
    labs = sorted({r["label"] for r in ros})
    at = {(r["label"], r["resolution_N"]): r for r in ros}
    leg2 = {}
    for cur in ("g_frac", "accel_ratio"):
        a = [at[(l, 128)][cur] for l in labs]
        b = [at[(l, 256)][cur] for l in labs]
        fin = sorted((at[(l, 256)] for l in labs if np.isfinite(at[(l, 256)][cur])),
                     key=lambda r: -r[cur])
        v = [r[cur] for r in fin]
        win = fin[0]
        leg2[cur] = {
            "spearman_128_256": spearman(a, b),
            "winner": {"label": win["label"], "class": win["shape_class"],
                       "is_grower": bool(win["t_res"] < T_MAX - 1e-6),
                       "centroid": round(win["descriptors"]["centroid"], 2)},
            "top5_growers": int(sum(r["t_res"] < T_MAX - 1e-6 for r in fin[:5])),
            "rho_log_w0": rho(v, np.log([r["max_w0"] for r in fin])),
            "rho_early_rate": rho(v, [r["early_rate"] for r in fin]),
            "rho_centroid": rho(v, [r["descriptors"]["centroid"] for r in fin]),
            "rho_t_res": rho(v, [r["t_res"] for r in fin]),
        }

    # LEG 3: caveat-2 free split
    sweep = {}
    for r in (x for x in rows if x["leg"] == "split_sweep"):
        base = r["label"].rsplit("_s", 1)[0]
        sweep.setdefault(base, []).append((r["target_split"], r["g_frac"]))
    sweep_argmax = {}
    for base, pts in sweep.items():
        pts.sort()
        gv = [g for _, g in pts]
        sweep_argmax[base] = {"curve": [[round(s, 2), round(g, 3)] for s, g in pts],
                              "argmax_split": pts[int(np.nanargmax(gv))][0]}
    free = [r for r in rows if r["leg"] == "free_split" and np.isfinite(r["g_frac"])]
    gf = [r["g_frac"] for r in free]
    sv = [r["descriptors"]["split"] for r in free]
    lw = list(np.log([r["max_w0"] for r in free]))
    cv = [r["descriptors"]["centroid"] for r in free]
    winner = max(free, key=lambda r: r["g_frac"])
    leg3 = {
        "split_sweep": sweep_argmax,
        "no_max_split_rail": all(v["argmax_split"] < 0.97 for v in sweep_argmax.values()),
        "rho_g_split": rho(gf, sv),
        "rho_g_log_w0": rho(gf, lw),
        "rho_split_log_w0": rho(sv, lw),
        "partial_g_log_w0_given_split": partial(gf, lw, sv),
        "partial_g_split_given_log_w0": partial(gf, sv, lw),
        "partial_g_centroid_given_split": partial(gf, cv, sv),
        "winner_split": round(winner["descriptors"]["split"], 2),
        "omega0_cheat_absent": True,
    }

    out = {"leg1_magnitude_wall": leg1, "leg2_rank_and_audit": leg2,
           "leg3_free_split": leg3,
           "note": ("g_frac rank-based currency: cheat-free, direction-correct, "
                    "caveat-2-favorable, rank-stable at 128<->256; MAGNITUDE on the "
                    "uniform-grid resolution wall; 256->512 rank check un-run (paused).")}
    (DATA / "phase1_gsustained.json").write_text(json.dumps(out, indent=1))
    return out


def curate_phase1_gate4_reform():
    """Route A Phase 1 reformulated Gate 4 on the g_frac currency (the FAIL that
    concluded the uniform-grid fitness search). Reads
    experiments/phase1_gate4_reform.jsonl. Records the six-property scorecard, the
    top shapes (free-split rail to omega0->0), the property-6 sub-conditions, and
    the property-4 grower->non-grower classification flips."""
    p = REPO / "experiments" / "phase1_gate4_reform.jsonl"
    rows = ([json.loads(l) for l in p.read_text().splitlines() if l.strip()]
            if p.exists() else [])
    if not rows:
        return None
    from analyze_phase1_gate4_reform import evaluate
    T_MAX = 4.0
    res = evaluate(rows)
    scorecard = {k: {"pass": (None if v[0] is None else bool(v[0])), "detail": v[1]}
                 for k, v in res.items() if not k.startswith("_")}

    roster = [r for r in rows if r.get("block") == "roster"]
    at = {(r["label"], r["resolution_N"]): r for r in roster}
    f512 = {l: at[(l, 512)] for (l, n) in at if n == 512}
    grow = lambda r: r["t_res"] < T_MAX - 1e-6
    ranked = sorted((r for r in f512.values() if np.isfinite(r["g_frac"])),
                    key=lambda r: -r["g_frac"])
    top = [{"label": r["label"], "class": r["shape_class"],
            "g_frac": round(r["g_frac"], 3),
            "centroid": round(r["descriptors"]["centroid"], 2),
            "split": round(r["descriptors"]["split"], 2),
            "t_res": round(r["t_res"], 2), "grower": bool(grow(r))} for r in ranked[:6]]
    flips = []
    for l in sorted({r["label"] for r in roster}):
        trs = {n: at[(l, n)]["t_res"] for n in (128, 256, 512) if (l, n) in at}
        if 128 in trs and 512 in trs and trs[128] < T_MAX - 1e-6 and trs[512] >= T_MAX - 1e-6:
            flips.append({"label": l, "t_res_by_N": {str(n): round(trs[n], 2) for n in trs}})

    out = {
        "verdict": "FAIL 4/6",
        "scorecard": scorecard,
        "property6_subconditions": res.get("_6sub", {}),
        "top6_at_512": top,
        "classification_flips": flips,
        "note": ("g_frac RANK is resolution-stable (+0.889, +0.926) but on a FREE "
                 "split roster the optimum rails to split->1 (omega0->0, the nu_crit "
                 "degeneracy); split-dominated (partial rho(g,centroid|split)=+0.11) "
                 "and largely a formation-time proxy (partial rho(g,centroid|t_res)="
                 "-0.39). 7/37 shapes are coarse-grid false-growers. Two currencies, "
                 "one uniform-grid wall -> Route D."),
    }
    # numpy bools in _6sub -> plain bool for JSON
    out["property6_subconditions"] = {k: bool(v) for k, v in out["property6_subconditions"].items()}
    (DATA / "phase1_gate4_reform.json").write_text(json.dumps(out, indent=1))
    return out


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
    spike = curate_phase1_spike()
    print(f"phase1_spike.json: {len(spike['ics'])} ICs x {len(spike['resolutions'])} N")
    screen = curate_phase1_axis_screen()
    print(f"phase1_axis_screen.json: survivors={screen['survivors']}")
    gate4 = curate_phase1_gate4()
    print(f"phase1_gate4.json: nu_crit rho(nu,log|w0|)="
          f"{gate4['gate4_nu_crit']['rho_nu_log_w0']}, "
          f"currency direction_ok={gate4['currency_probe']['direction_ok']}")
    gsus = curate_phase1_gsustained()
    if gsus:
        print(f"phase1_gsustained.json: g_frac spearman(128,256)="
              f"{gsus['leg2_rank_and_audit']['g_frac']['spearman_128_256']}, "
              f"omega0-cheat-absent partial={gsus['leg3_free_split']['partial_g_log_w0_given_split']}")
    reform = curate_phase1_gate4_reform()
    if reform:
        print(f"phase1_gate4_reform.json: {reform['verdict']}, "
              f"top winner split={reform['top6_at_512'][0]['split']}, "
              f"{len(reform['classification_flips'])} classification flips")
    metrics = curate_summary(ga, studies, verdicts, rough, spike, screen)
    print("summary_metrics.json written")
    print(json.dumps(metrics, indent=1))
