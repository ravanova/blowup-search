"""Stage 2.5 acceptance analysis over experiments/stage2_5_sweep.jsonl.

Evaluates, for each candidate a in {0.4, 0.7, 1.0}, the SIX-property
viability checklist (PLAN.md Stage 2.5 = Stage 1.5's five + the property
Stage 2 proved necessary):

1. nonzero    — >=3 uncensored shapes with nu_crit > 2*tol (a censored-low-
                everywhere a-value is a dead axis, the known a~1 risk).
2. finite     — nothing censored high at the top of the range ladder.
3. monotone   — no post-bisection probe found blow-up on the regular side.
4. resolution-stable — max |crit(512) - crit(256)| small vs the shape
                spread (same rule as Stage 1.5: <= max(0.1*spread, 2*tol)).
5. wide band  — spread across shapes resolvable above noise
                (>=5 uncensored shapes, spread >= 10*max(median diff, tol)).
6. non-trivial optimum — BOTH:
   (a) the best init-prior draw sits clearly below the best structured
       (Stage 1.5) shape: gap >= 10*tol at the fitness resolution N=256
       (Stage 2's failure signature was a gap of 0-0.2 tol);
   (b) the top of the landscape is not monotone in k=1 dominance: the top-3
       shapes by nu_crit must not all have energy_k1_frac >= 0.95
       (Stage 2's degenerate optimum was >=99.5% k=1); Spearman rho between
       energy_k1_frac and nu_crit is reported alongside.

Selection rule (PLAN.md): the LARGEST a passing all six.

Usage: .venv/bin/python analyze_stage2_5.py [path.jsonl]
"""

import json
import sys
from collections import defaultdict

import numpy as np

A_VALUES = (0.4, 0.7, 1.0)
RESOLUTIONS = (256, 512)


def load(path="experiments/stage2_5_sweep.jsonl"):
    table = {}
    for line in open(path):
        if not line.strip():
            continue
        row = json.loads(line)
        # newest row wins on re-run
        table[(row["ic"]["label"], row["fixed"]["a"], row["resolution_N"])] = row
    candidates = {r.get("candidate", "A") for r in table.values()}
    caps = {json.dumps(r.get("bandwidth_cap")) for r in table.values()}
    assert len(candidates) == 1 and len(caps) == 1, \
        "mixed candidate sweeps in one file; analyze them separately"
    return table, candidates.pop(), json.loads(caps.pop())


def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    if np.std(rx) == 0 or np.std(ry) == 0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def analyze_a(table, a):
    labels = sorted({k[0] for k in table if k[1] == a})
    per_shape = []
    for label in labels:
        entry = {"label": label}
        for n in RESOLUTIONS:
            row = table.get((label, a, n))
            if row is None:
                continue
            entry["source"] = row["ic"]["source"]
            entry["k1_frac"] = row["ic"]["spectral"]["energy_k1_frac"]
            entry["low2_frac"] = row["ic"]["spectral"].get("energy_low2_frac")
            entry[n] = {
                "critical": row["critical_value"],
                "censored": row["bracket_censored"],
                "monotone": row["critical_value_monotone"],
                "tol": row["tolerance"],
                "n_ext": row["n_range_extensions"],
                "max_drift": row.get("max_conservation_drift_blowup_runs"),
            }
        per_shape.append(entry)
    return per_shape


def verdict_for_a(per_shape, bandwidth_cap=None):
    both = [e for e in per_shape if 256 in e and 512 in e]
    uncensored = [e for e in both
                  if e[256]["censored"] is None and e[512]["censored"] is None]
    censored_high = [e for e in both
                     if "high" in (e[256]["censored"], e[512]["censored"])]
    censored_low = [e for e in both
                    if "low" in (e[256]["censored"], e[512]["censored"])]

    tol = both[0][256]["tol"] if both else 1e-3
    crits = [e[512]["critical"] for e in uncensored]
    diffs = [abs(e[512]["critical"] - e[256]["critical"]) for e in uncensored]
    nonmono = [e["label"] for e in uncensored
               if e[256]["monotone"] is False or e[512]["monotone"] is False]

    n = len(uncensored)
    spread = (max(crits) - min(crits)) if crits else 0.0
    max_diff = max(diffs) if diffs else 0.0
    med_diff = sorted(diffs)[len(diffs) // 2] if diffs else 0.0

    # property 6 at the fitness resolution (N=256)
    prior = [e for e in uncensored if e["source"] == "init_prior"]
    struct = [e for e in uncensored if e["source"] == "stage1_5"]
    best_prior = max((e[256]["critical"] for e in prior), default=None)
    best_struct = max((e[256]["critical"] for e in struct), default=None)
    gap = (best_struct - best_prior
           if best_prior is not None and best_struct is not None else None)

    top3 = sorted(uncensored, key=lambda e: e[256]["critical"])[-3:]
    top3_k1 = [e["k1_frac"] for e in top3]
    rho = (spearman(np.array([e["k1_frac"] for e in uncensored]),
                    np.array([e[256]["critical"] for e in uncensored]))
           if n >= 3 else float("nan"))

    # Candidate B: the trivially controllable quantity is the k<=2 energy
    # fraction, whose reachable maximum is the cap itself — the failure mode
    # is the landscape top PINNED at the constraint boundary (PLAN.md's
    # stated candidate-B risk).
    if bandwidth_cap is not None:
        max_frac = float(bandwidth_cap["max_frac"])
        top3_low2 = [e["low2_frac"] for e in top3]
        top_not_trivial = not (len(top3_low2) == 3 and
                               all(f >= max_frac - 1e-3 for f in top3_low2))
    else:
        top3_low2 = None
        top_not_trivial = not (len(top3_k1) == 3
                               and all(f >= 0.95 for f in top3_k1))

    v = {
        "n_shapes_both_res": len(both),
        "n_uncensored": n,
        "n_censored_low": len(censored_low),
        "censored_low_labels": [e["label"] for e in censored_low],
        "n_censored_high": len(censored_high),
        "bisection_tol": tol,
        "n_nonzero": sum(c > 2 * tol for c in crits),
        "nonzero": sum(c > 2 * tol for c in crits) >= 3,
        "finite": len(censored_high) == 0,
        "n_nonmonotone": len(nonmono),
        "nonmonotone_labels": nonmono,
        "monotone": len(nonmono) == 0,
        "crit_min": min(crits) if crits else None,
        "crit_max": max(crits) if crits else None,
        "spread": spread,
        "median_res_diff": med_diff,
        "max_res_diff": max_diff,
        "resolution_stable": n > 0 and max_diff <= max(0.1 * spread, 2 * tol),
        "wide_band": n >= 5 and spread >= 10 * max(med_diff, tol),
        "n_prior_uncensored": len(prior),
        "n_struct_uncensored": len(struct),
        "best_prior": best_prior,
        "best_struct": best_struct,
        "prior_struct_gap": gap,
        "gap_in_tol_units": None if gap is None else gap / tol,
        "top3_labels": [e["label"] for e in top3],
        "top3_k1_fracs": [round(f, 4) for f in top3_k1],
        "top3_low2_fracs": (None if top3_low2 is None
                            else [round(f, 4) for f in top3_low2]),
        "spearman_k1_vs_crit": rho,
        "nontrivial_gap": gap is not None and gap >= 10 * tol,
        "nontrivial_top_not_trivial_quantity": top_not_trivial,
    }
    v["nontrivial_optimum"] = v["nontrivial_gap"] and top_not_trivial
    v["pass"] = all((v["nonzero"], v["finite"], v["monotone"],
                     v["resolution_stable"], v["wide_band"],
                     v["nontrivial_optimum"]))
    return v


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "experiments/stage2_5_sweep.jsonl"
    table, candidate, cap = load(path)
    a_values = sorted({k[1] for k in table})
    print(f"candidate {candidate}"
          + (f" (bandwidth cap: k<={cap['k_max']} frac<={cap['max_frac']})"
             if cap else ""))
    verdicts = {}

    for a in a_values:
        per_shape = analyze_a(table, a)
        if not per_shape:
            continue
        print(f"\n=== nu_crit at a = {a} ===")
        print(f"{'shape':24s} {'src':>10s} {'k1frac':>7s} {'N=256':>9s} "
              f"{'N=512':>9s} {'|diff|':>8s} {'cens':>5s} {'mono':>5s} "
              f"{'ext':>3s}")
        for e in sorted(per_shape,
                        key=lambda e: -(e.get(256, {}).get("critical") or 0)):
            if 256 not in e or 512 not in e:
                continue
            c256, c512 = e[256], e[512]
            cens = c256["censored"] or c512["censored"] or "-"
            mono = str(c512["monotone"] if c512["monotone"] is not None
                       else c256["monotone"])
            print(f"{e['label']:24s} {e['source']:>10s} {e['k1_frac']:7.3f} "
                  f"{c256['critical']:9.4f} {c512['critical']:9.4f} "
                  f"{abs(c512['critical'] - c256['critical']):8.4f} "
                  f"{cens:>5s} {mono:>5s} {max(c256['n_ext'], c512['n_ext']):3d}")
        v = verdict_for_a(per_shape, cap)
        verdicts[a] = v
        print(f"\n verdict[a={a}]:")
        for key, val in v.items():
            print(f"   {key}: {val}")

    print("\n=== STAGE 2.5 ACCEPTANCE ===")
    passing = [a for a, v in verdicts.items() if v["pass"]]
    for a, v in verdicts.items():
        fails = [k for k in ("nonzero", "finite", "monotone",
                             "resolution_stable", "wide_band",
                             "nontrivial_optimum") if not v[k]]
        print(f" a={a}: {'PASS' if v['pass'] else 'FAIL (' + ', '.join(fails) + ')'}")
    if passing:
        chosen = max(passing)
        if candidate == "B":
            print(f" -> candidate B passes: nu_crit at a=0 under the "
                  f"k<={cap['k_max']} cap ({cap['max_frac']}) is the axis")
        else:
            print(f" -> chosen axis: nu_crit at a = {chosen} "
                  "(largest passing a — closest to De Gregorio)")
    elif candidate == "A":
        print(" -> NO a passes all six: fall back to bandwidth-constrained "
              "nu_crit at a=0 (PLAN.md Stage 2.5 candidate B)")
    else:
        print(" -> candidate B FAILS: stop and write up — do not run the GA "
              "on an unverified axis (PLAN.md Stage 2.5)")


if __name__ == "__main__":
    main()
