"""Gate the non-genericity fitness axis over experiments/nongenericity_sweep.jsonl.

The candidate axis is fitness = |alpha - 1| (distance of the fitted blow-up
exponent from the generic CLM value), measured inviscid at fixed a. It is
gated per a in {0.7, 0.9, 1.0} on the six-property checklist (PLAN.md Stage
2.5/2.6), with candidate-D's single-run adaptations:

  1. nonzero    -> >=3 shapes with |alpha-1| > 2*noise (genuine non-genericity
                   exists; if every blow-up is alpha~1 the axis is dead-flat).
  2. finite     -> alpha not railing at the fit-grid edge for the top shapes
                   (a rail is a fit failure, not a measurement).
  3. monotone   -> replaced by WELL-DEFINEDNESS: a shape is usable at both
                   resolutions or neither (no blow-up flip, no fit-reliability
                   flip). This is where the marginal high-a rough regime breaks.
  4. resolution-stable -> max |alpha_512 - alpha_256| small vs the shape spread.
  5. wide band  -> spread of |alpha-1| resolvable above noise.
  6. non-trivial optimum -> best init-prior vs best structured gap >= 10*noise
                   AND the top not trivially controlled by k=1 dominance or,
                   for prior draws, the envelope p (the regularity lever).

An alpha is "usable" only if the run blew up, a held-out fit exists, and its
R^2 >= R2_FLOOR (an unreliable fit is not a measurement of the exponent).

Folds in the "x p-regimes" question: reports, among the init-prior draws
(which carry envelope_p), how blow-up occurrence and |alpha-1| correlate with
regularity p -- i.e. whether roughness is the lever that unlocks non-generic
blow-up, and at which a.

Usage: .venv/bin/python analyze_nongenericity.py [path.jsonl]
"""

import json
import sys

import numpy as np

from analyze_stage2_5 import spearman

R2_FLOOR = 0.9          # a fit below this does not define alpha
ALPHA_GRID = (0.30, 3.00)   # win_condition exponent grid edges
ALPHA_NOISE_FLOOR = 0.05    # exponent grid step; floor on cross-res |Delta|


def load(path="experiments/nongenericity_sweep.jsonl"):
    table = {}
    for line in open(path):
        if not line.strip():
            continue
        row = json.loads(line)
        table[(row["ic"]["label"], row["fixed"]["a"],
               row["resolution_N"])] = row  # newest wins
    return table


def _usable(row):
    """(blew_up, alpha, r2, usable) for one run row."""
    if row is None:
        return False, None, None, False
    if not row["blowup"] or row["estimate"] is None:
        return bool(row["blowup"] if row else False), None, None, False
    a = row["estimate"]["exponent"]
    r2 = row["estimate"]["r_squared"]
    return True, a, r2, (r2 >= R2_FLOOR)


def _p_of(row):
    """Envelope p for init-prior draws (carry it in spec); None otherwise."""
    spec = row["ic"]["spec"]
    return spec.get("envelope_p") if isinstance(spec, dict) else None


def verdict_for_a(table, a):
    labels = sorted({k[0] for k in table if k[1] == a})
    per = []
    for label in labels:
        r256, r512 = table.get((label, a, 256)), table.get((label, a, 512))
        if r256 is None or r512 is None:
            continue
        b256, a256, q256, u256 = _usable(r256)
        b512, a512, q512, u512 = _usable(r512)
        per.append({
            "label": label, "source": r256["ic"]["source"],
            "k1": r256["ic"]["spectral"]["energy_k1_frac"],
            "p": _p_of(r256),
            "blew256": b256, "blew512": b512,
            "a256": a256, "a512": a512, "q256": q256, "q512": q512,
            "u256": u256, "u512": u512,
            "absdev256": None if a256 is None else abs(a256 - 1.0),
            "absdev512": None if a512 is None else abs(a512 - 1.0),
        })

    n_blowup = sum(e["blew256"] or e["blew512"] for e in per)
    both = [e for e in per if e["u256"] and e["u512"]]
    flips = [e["label"] for e in per if e["u256"] != e["u512"]]

    absdev = [e["absdev256"] for e in both]
    diffs = [abs(e["a512"] - e["a256"]) for e in both]
    spread = (max(absdev) - min(absdev)) if absdev else 0.0
    med_diff = sorted(diffs)[len(diffs) // 2] if diffs else 0.0
    max_diff = max(diffs) if diffs else 0.0
    noise = max(med_diff, ALPHA_NOISE_FLOOR)

    prior = [e for e in both if e["source"] == "init_prior"]
    struct = [e for e in both if e["source"] == "stage1_5"]
    best_prior = max((e["absdev256"] for e in prior), default=None)
    best_struct = max((e["absdev256"] for e in struct), default=None)
    gap = (best_struct - best_prior
           if None not in (best_prior, best_struct) else None)

    top3 = sorted(both, key=lambda e: e["absdev256"])[-3:]
    top3_railing = [e for e in top3
                    if min(abs(e["a256"] - ALPHA_GRID[0]),
                           abs(e["a256"] - ALPHA_GRID[1])) < 1e-6]
    top3_k1 = [e["k1"] for e in top3]
    top_not_trivial_k1 = not (len(top3_k1) == 3 and all(f >= 0.95 for f in top3_k1))
    top3_p = [e["p"] for e in top3 if e["p"] is not None]
    top_not_trivial_p = not (len(top3_p) == 3 and all(p <= 0.3 for p in top3_p))

    # p-regime fold-in (init-prior draws carry envelope_p)
    prior_all = [e for e in per if e["source"] == "init_prior" and e["p"] is not None]
    rho_absdev_p = (spearman(np.array([e["p"] for e in prior]),
                             np.array([e["absdev256"] for e in prior]))
                    if len(prior) >= 3 else float("nan"))
    rho_blow_p = (spearman(np.array([e["p"] for e in prior_all]),
                           np.array([float(e["blew256"] or e["blew512"])
                                     for e in prior_all]))
                  if len(prior_all) >= 3 else float("nan"))

    v = {
        "n_shapes": len(per),
        "n_blowup_either_res": n_blowup,
        "n_usable_both": len(both),
        "n_welldef_flips": len(flips),
        "flip_labels": flips,
        "absdev_min": min(absdev) if absdev else None,
        "absdev_max": max(absdev) if absdev else None,
        "spread": spread,
        "median_res_diff_alpha": med_diff,
        "max_res_diff_alpha": max_diff,
        "n_nongeneric": sum(d > 2 * noise for d in absdev),
        "nonzero": sum(d > 2 * noise for d in absdev) >= 3,
        "finite": len(top3_railing) == 0,
        "well_defined": len(flips) == 0,
        "resolution_stable": bool(both) and max_diff <= max(0.1 * spread,
                                                            2 * ALPHA_NOISE_FLOOR),
        "wide_band": len(both) >= 5 and spread >= 10 * noise,
        "best_prior_absdev": best_prior,
        "best_struct_absdev": best_struct,
        "prior_struct_gap": gap,
        "gap_in_noise_units": None if gap is None or noise == 0 else gap / noise,
        "top3_labels": [e["label"] for e in top3],
        "spearman_absdev_vs_p_prior": rho_absdev_p,
        "spearman_blowup_vs_p_prior": rho_blow_p,
        "nontrivial_gap": gap is not None and gap >= 10 * noise,
        "nontrivial_top_not_trivial_quantity":
            top_not_trivial_k1 and top_not_trivial_p,
    }
    v["nontrivial_optimum"] = (v["nontrivial_gap"]
                               and v["nontrivial_top_not_trivial_quantity"])
    v["pass"] = all((v["nonzero"], v["finite"], v["well_defined"],
                     v["resolution_stable"], v["wide_band"],
                     v["nontrivial_optimum"]))
    return per, v


def main():
    path = (sys.argv[1] if len(sys.argv) > 1
            else "experiments/nongenericity_sweep.jsonl")
    table = load(path)
    a_values = sorted({k[1] for k in table})
    verdicts = {}

    for a in a_values:
        per, v = verdict_for_a(table, a)
        print(f"\n=== non-genericity |alpha-1| at a = {a} (inviscid) ===")
        print(f"{'shape':24s} {'src':>10s} {'p':>5s} {'blew':>9s} "
              f"{'a256':>6s} {'a512':>6s} {'R2_256':>7s} {'usable':>7s}")
        for e in sorted(per, key=lambda e: -(e["absdev256"] or -1)):
            blew = f"{e['blew256']:d}/{e['blew512']:d}"
            a256 = "-" if e["a256"] is None else f"{e['a256']:.2f}"
            a512 = "-" if e["a512"] is None else f"{e['a512']:.2f}"
            r2 = "-" if e["q256"] is None else f"{e['q256']:.3f}"
            pp = "-" if e["p"] is None else f"{e['p']:.2f}"
            use = f"{e['u256']:d}/{e['u512']:d}"
            print(f"{e['label']:24s} {e['source']:>10s} {pp:>5s} {blew:>9s} "
                  f"{a256:>6s} {a512:>6s} {r2:>7s} {use:>7s}")
        verdicts[a] = v
        print(f"\n verdict[a={a}]:")
        for key, val in v.items():
            print(f"   {key}: {val}")

    print("\n=== NON-GENERICITY AXIS VERDICT ===")
    for a, v in verdicts.items():
        keys = ("nonzero", "finite", "well_defined", "resolution_stable",
                "wide_band", "nontrivial_optimum")
        fails = [k for k in keys if not v[k]]
        print(f" a={a}: {'PASS' if v['pass'] else 'FAIL (' + ', '.join(fails) + ')'} "
              f"| blow-up {v['n_blowup_either_res']}/{v['n_shapes']}, "
              f"usable {v['n_usable_both']}, non-generic {v['n_nongeneric']}, "
              f"flips {v['n_welldef_flips']}")
    passing = [a for a, v in verdicts.items() if v["pass"]]
    print()
    if passing:
        print(f" -> non-genericity axis VIABLE at a = {max(passing)}: the GA "
              "edge and the novel target overlap. Proceed to a six-property "
              "acceptance rerun on this axis.")
    else:
        # Where does non-genericity even appear, and is it stable?
        appears = [a for a, v in verdicts.items() if v["n_nongeneric"] >= 3]
        stable = [a for a in appears if verdicts[a]["resolution_stable"]
                  and verdicts[a]["well_defined"]]
        print(" -> NO a admits a viable non-genericity axis.")
        if not appears:
            print("    Non-genericity (|alpha-1| > noise) does not appear at "
                  "any swept a: blow-up here is generically CLM-type (alpha~1). "
                  "The GA-edge regime and the novel (alpha!=1) target are "
                  "DISJOINT within reachable gCLM.")
        elif not stable:
            print(f"    Non-genericity appears (a in {appears}) but only "
                  "resolution-UNSTABLE / ill-defined (the Stage 1.5 a_crit "
                  "instability, now on the exponent). It is not searchable at "
                  "N in {256,512}. Edge (a=0.7, generic) and novel target "
                  "(high-a rough, unstable) are effectively disjoint.")
        print("    Implication: a De Gregorio-type Tier-3 target is not "
              "reachable on this axis at these resolutions. Options for review "
              "in the results write-up (rougher data + finer N; a different "
              "model e.g. 2D Boussinesq; or bank the validated 1D pipeline).")


if __name__ == "__main__":
    main()
