"""Stage 2.6 acceptance analysis over experiments/stage2_6_sweep.jsonl.

Gates each candidate on the six-property checklist (PLAN.md Stage 2.5/2.6):

- A' — nu_crit under the v3 amplification-only oracle at a in
  {0.4, 0.7, 1.0}: identical verdict logic to Stage 2.5's analyzer
  (imported), now over v3 data at t_max=24.
- B' — the a=0 re-baseline (control; also gated, mostly as the substrate
  check for C).
- C — nu_crit(v3, a=0) * k_eff^2: post-processed from the B' rows. The
  trivially controllable quantity is spectral concentration itself, so
  property 6 fails if the landscape top is an extreme of k_eff^2 (top-3
  all in the top or bottom 15% of the distribution) or the prior reaches
  the top. Per-shape tolerance scales with k_eff^2 (tol_C = tol * k_eff^2),
  so noise-floor comparisons use per-shape values.
- D — time-to-amplification fitness (t_max - t_amp) at fixed nu in
  {0.01, 0.03}, a=0: no bisection, so the monotonicity property is
  replaced by well-definedness (a shape amplifies at both resolutions or
  neither), and the noise floor is max(median cross-resolution |Δ|, 0.05)
  (0.05 ~ 5*dt_max).

Selection precedence if several pass (PLAN.md Stage 2.6):
A' (largest passing a) > C > D.

Usage: .venv/bin/python analyze_stage2_6.py [path.jsonl]
"""

import json
import sys

import numpy as np

from analyze_stage2_5 import analyze_a, spearman, verdict_for_a

A_PRIME_VALUES = (0.4, 0.7, 1.0)
D_NOISE_FLOOR = 0.05


def load(path="experiments/stage2_6_sweep.jsonl"):
    bisect_table, d_table = {}, {}
    for line in open(path):
        if not line.strip():
            continue
        row = json.loads(line)
        if row["mode"] == "bisect":
            bisect_table[(row["ic"]["label"], row["fixed"]["a"],
                          row["resolution_N"])] = row
        else:
            d_table[(row["ic"]["label"], row["nu_fixed"],
                     row["resolution_N"])] = row
    return bisect_table, d_table


def _extreme_band_check(top3_vals, all_vals, frac=0.15):
    """True (= trivial) when the top-3 all sit in the same extreme band of
    the distribution of a controllable quantity."""
    if len(top3_vals) < 3 or len(all_vals) < 8:
        return False
    lo = float(np.quantile(all_vals, frac))
    hi = float(np.quantile(all_vals, 1.0 - frac))
    return all(v >= hi for v in top3_vals) or all(v <= lo for v in top3_vals)


# --- candidate C -----------------------------------------------------------


def verdict_for_c(bisect_table):
    """Six properties for C = nu_crit(v3, a=0) * k_eff^2."""
    labels = sorted({k[0] for k in bisect_table if k[1] == 0.0})
    per_shape = []
    for label in labels:
        r256 = bisect_table.get((label, 0.0, 256))
        r512 = bisect_table.get((label, 0.0, 512))
        if r256 is None or r512 is None:
            continue
        k2 = r256["ic"]["k_eff_sq"]
        entry = {
            "label": label,
            "source": r256["ic"]["source"],
            "k1_frac": r256["ic"]["spectral"]["energy_k1_frac"],
            "k_eff_sq": k2,
            "censored": r256["bracket_censored"] or r512["bracket_censored"],
            "monotone": (r256["critical_value_monotone"] is not False
                         and r512["critical_value_monotone"] is not False),
            "tol_c": r256["tolerance"] * k2,
            "c256": r256["critical_value"] * k2,
            "c512": r512["critical_value"] * k2,
        }
        per_shape.append(entry)

    unc = [e for e in per_shape if e["censored"] is None]
    cens_high = [e for e in per_shape if e["censored"] == "high"]
    vals = [e["c512"] for e in unc]
    diffs = [abs(e["c512"] - e["c256"]) for e in unc]
    nonmono = [e["label"] for e in unc if not e["monotone"]]
    spread = (max(vals) - min(vals)) if vals else 0.0
    med_diff = sorted(diffs)[len(diffs) // 2] if diffs else 0.0
    max_diff = max(diffs) if diffs else 0.0
    med_tol = (sorted(e["tol_c"] for e in unc)[len(unc) // 2]) if unc else 0.0

    prior = [e for e in unc if e["source"] == "init_prior"]
    struct = [e for e in unc if e["source"] == "stage1_5"]
    best_prior = max((e["c256"] for e in prior), default=None)
    best_struct = max((e["c256"] for e in struct), default=None)
    gap = (best_struct - best_prior
           if None not in (best_prior, best_struct) else None)

    top3 = sorted(unc, key=lambda e: e["c256"])[-3:]
    trivial_extreme = _extreme_band_check(
        [e["k_eff_sq"] for e in top3], [e["k_eff_sq"] for e in unc])
    rho_keff = (spearman(np.array([e["k_eff_sq"] for e in unc]),
                         np.array([e["c256"] for e in unc]))
                if len(unc) >= 3 else float("nan"))
    rho_k1 = (spearman(np.array([e["k1_frac"] for e in unc]),
                       np.array([e["c256"] for e in unc]))
              if len(unc) >= 3 else float("nan"))

    noise = max(med_diff, med_tol)
    v = {
        "n_uncensored": len(unc),
        "n_censored_high": len(cens_high),
        "median_tol_c": med_tol,
        "n_nonzero": sum(x > 2 * e["tol_c"] for x, e in
                         zip((e["c512"] for e in unc), unc)),
        "nonzero": len(unc) >= 3,
        "finite": len(cens_high) == 0,
        "n_nonmonotone": len(nonmono),
        "nonmonotone_labels": nonmono,
        "monotone": len(nonmono) == 0,
        "c_min": min(vals) if vals else None,
        "c_max": max(vals) if vals else None,
        "spread": spread,
        "median_res_diff": med_diff,
        "max_res_diff": max_diff,
        "resolution_stable": bool(unc) and max_diff <= max(0.1 * spread,
                                                           2 * med_tol),
        "wide_band": len(unc) >= 5 and spread >= 10 * noise,
        "best_prior": best_prior,
        "best_struct": best_struct,
        "prior_struct_gap": gap,
        "gap_in_noise_units": None if gap is None or noise == 0 else gap / noise,
        "top3_labels": [e["label"] for e in top3],
        "top3_k_eff_sq": [round(e["k_eff_sq"], 2) for e in top3],
        "spearman_keff_vs_c": rho_keff,
        "spearman_k1_vs_c": rho_k1,
        "nontrivial_gap": gap is not None and gap >= 10 * noise,
        "nontrivial_top_not_trivial_quantity":
            not (trivial_extreme or abs(rho_keff) >= 0.8),
    }
    v["nontrivial_optimum"] = (v["nontrivial_gap"]
                               and v["nontrivial_top_not_trivial_quantity"])
    v["pass"] = all((v["nonzero"], v["finite"], v["monotone"],
                     v["resolution_stable"], v["wide_band"],
                     v["nontrivial_optimum"]))
    return per_shape, v


# --- candidate D -----------------------------------------------------------


def verdict_for_d(d_table, nu):
    labels = sorted({k[0] for k in d_table if k[1] == nu})
    per_shape = []
    for label in labels:
        r256 = d_table.get((label, nu, 256))
        r512 = d_table.get((label, nu, 512))
        if r256 is None or r512 is None:
            continue
        per_shape.append({
            "label": label,
            "source": r256["ic"]["source"],
            "k1_frac": r256["ic"]["spectral"]["energy_k1_frac"],
            "k_eff_sq": r256["ic"]["k_eff_sq"],
            "f256": r256["fitness"],
            "f512": r512["fitness"],
        })

    defined = [e for e in per_shape
               if e["f256"] is not None and e["f512"] is not None]
    flipped = [e["label"] for e in per_shape
               if (e["f256"] is None) != (e["f512"] is None)]
    vals = [e["f512"] for e in defined]
    diffs = [abs(e["f512"] - e["f256"]) for e in defined]
    spread = (max(vals) - min(vals)) if vals else 0.0
    med_diff = sorted(diffs)[len(diffs) // 2] if diffs else 0.0
    max_diff = max(diffs) if diffs else 0.0
    noise = max(med_diff, D_NOISE_FLOOR)

    prior = [e for e in defined if e["source"] == "init_prior"]
    struct = [e for e in defined if e["source"] == "stage1_5"]
    best_prior = max((e["f256"] for e in prior), default=None)
    best_struct = max((e["f256"] for e in struct), default=None)
    gap = (best_struct - best_prior
           if None not in (best_prior, best_struct) else None)

    top3 = sorted(defined, key=lambda e: e["f256"])[-3:]
    trivial = (_extreme_band_check([e["k1_frac"] for e in top3],
                                   [e["k1_frac"] for e in defined])
               or _extreme_band_check([e["k_eff_sq"] for e in top3],
                                      [e["k_eff_sq"] for e in defined]))
    rho_k1 = (spearman(np.array([e["k1_frac"] for e in defined]),
                       np.array([e["f256"] for e in defined]))
              if len(defined) >= 3 else float("nan"))
    rho_keff = (spearman(np.array([e["k_eff_sq"] for e in defined]),
                         np.array([e["f256"] for e in defined]))
                if len(defined) >= 3 else float("nan"))

    v = {
        "n_defined": len(defined),
        "n_censored": len(per_shape) - len(defined) - len(flipped),
        "n_resolution_flips": len(flipped),
        "flip_labels": flipped,
        "nonzero": len(defined) >= 5,
        "finite": True,  # fitness bounded by t_max by construction
        "well_defined": len(flipped) == 0,  # replaces bisection monotonicity
        "f_min": min(vals) if vals else None,
        "f_max": max(vals) if vals else None,
        "spread": spread,
        "median_res_diff": med_diff,
        "max_res_diff": max_diff,
        "resolution_stable": bool(defined) and max_diff <= max(0.1 * spread,
                                                               2 * D_NOISE_FLOOR),
        "wide_band": len(defined) >= 5 and spread >= 10 * noise,
        "best_prior": best_prior,
        "best_struct": best_struct,
        "prior_struct_gap": gap,
        "gap_in_noise_units": None if gap is None else gap / noise,
        "top3_labels": [e["label"] for e in top3],
        "spearman_k1_vs_f": rho_k1,
        "spearman_keff_vs_f": rho_keff,
        "nontrivial_gap": gap is not None and gap >= 10 * noise,
        "nontrivial_top_not_trivial_quantity":
            not (trivial or abs(rho_k1) >= 0.8 or abs(rho_keff) >= 0.8),
    }
    v["nontrivial_optimum"] = (v["nontrivial_gap"]
                               and v["nontrivial_top_not_trivial_quantity"])
    v["pass"] = all((v["nonzero"], v["finite"], v["well_defined"],
                     v["resolution_stable"], v["wide_band"],
                     v["nontrivial_optimum"]))
    return per_shape, v


# --- report ----------------------------------------------------------------


def _print_verdict(name, v):
    print(f"\n verdict[{name}]:")
    for key, val in v.items():
        print(f"   {key}: {val}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "experiments/stage2_6_sweep.jsonl"
    bisect_table, d_table = load(path)
    results = {}

    for a in sorted({k[1] for k in bisect_table}):
        name = f"A'(a={a})" if a > 0 else "B'(a=0)"
        per_shape = analyze_a(bisect_table, a)
        print(f"\n=== nu_crit(v3, t_max=24) at a = {a} ===")
        print(f"{'shape':24s} {'src':>10s} {'k1frac':>7s} {'N=256':>9s} "
              f"{'N=512':>9s} {'|diff|':>8s} {'cens':>5s} {'mono':>5s}")
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
                  f"{cens:>5s} {mono:>5s}")
        v = verdict_for_a(per_shape, None)
        results[name] = v
        _print_verdict(name, v)

    if any(k[1] == 0.0 for k in bisect_table):
        per_shape_c, v_c = verdict_for_c(bisect_table)
        print("\n=== candidate C = nu_crit(v3, a=0) * k_eff^2 ===")
        for e in sorted(per_shape_c, key=lambda e: -(e["c256"] or 0)):
            if e["censored"] is None:
                print(f"{e['label']:24s} {e['source']:>10s} "
                      f"k_eff2={e['k_eff_sq']:7.2f} "
                      f"C256={e['c256']:8.4f} C512={e['c512']:8.4f}")
        results["C"] = v_c
        _print_verdict("C", v_c)

    for nu in sorted({k[1] for k in d_table}):
        name = f"D(nu={nu:g})"
        per_shape_d, v_d = verdict_for_d(d_table, nu)
        print(f"\n=== candidate {name}: t_max - t_amp at fixed nu ===")
        for e in sorted(per_shape_d,
                        key=lambda e: -(e["f256"] if e["f256"] is not None
                                        else -1)):
            f2, f5 = e["f256"], e["f512"]
            print(f"{e['label']:24s} {e['source']:>10s} "
                  f"{'cens' if f2 is None else format(f2, '8.3f')} "
                  f"{'cens' if f5 is None else format(f5, '8.3f')}")
        results[name] = v_d
        _print_verdict(name, v_d)

    print("\n=== STAGE 2.6 ACCEPTANCE ===")
    for name, v in results.items():
        keys = ("nonzero", "finite",
                "monotone" if "monotone" in v else "well_defined",
                "resolution_stable", "wide_band", "nontrivial_optimum")
        fails = [k for k in keys if not v[k]]
        print(f" {name}: {'PASS' if v['pass'] else 'FAIL (' + ', '.join(fails) + ')'}")

    a_passing = [float(n.split('a=')[1].rstrip(')')) for n, v in results.items()
                 if n.startswith("A'") and v["pass"]]
    if a_passing:
        print(f" -> chosen axis: A' at a = {max(a_passing)} "
              "(largest passing a; precedence A' > C > D)")
    elif results.get("C", {}).get("pass"):
        print(" -> chosen axis: C = nu_crit(v3, a=0) * k_eff^2")
    else:
        d_passing = [n for n, v in results.items()
                     if n.startswith("D(") and v["pass"]]
        if d_passing:
            print(f" -> chosen axis: {d_passing[0]} (only D passes)")
        else:
            print(" -> NO candidate passes: path 3 activates "
                  "(accept the negative result; see PLAN.md Stage 2.6)")


if __name__ == "__main__":
    main()
