"""Stage 1.5 acceptance analysis over experiments/stage1_5_sweep.jsonl.

Evaluates, for each candidate fitness axis (nu_crit at a=0, a_crit at nu=0),
the five acceptance properties from PLAN.md Stage 1.5:

1. nonzero   — uncensored critical values > 0 for some shapes.
2. finite    — not censored "high" (blow-up does not survive the whole range).
3. monotone  — post-bisection probes on the regular side found no blow-up.
4. resolution-stable — |crit(512) - crit(256)| small relative to both the
   bisection tolerance and the shape-to-shape spread.
5. wide band — the spread of critical values across shapes is resolvable
   above the resolution/bisection noise floor.

Prints per-shape tables and the per-axis verdict. Pure stdlib.
"""

import json
import sys
from collections import defaultdict

RESOLUTIONS = (256, 512)


def load(path="experiments/stage1_5_sweep.jsonl"):
    rows = [json.loads(line) for line in open(path) if line.strip()]
    # Keyed on (label, axis, N); keep the newest row if re-run.
    table = {}
    for row in rows:
        table[(row["ic"]["label"], row["axis"], row["resolution_N"])] = row
    return table


def analyze(table):
    labels = sorted({k[0] for k in table}, key=lambda s: s)
    report = {}
    for axis in ("nu", "a"):
        per_shape = []
        for label in labels:
            entry = {"label": label}
            for n in RESOLUTIONS:
                row = table.get((label, axis, n))
                if row is None:
                    continue
                entry[n] = {
                    "critical": row["critical_value"],
                    "censored": row["bracket_censored"],
                    "monotone": row["critical_value_monotone"],
                    "tol": (row["range"][1] - row["range"][0])
                            / 2 ** row["n_bisect_iters"],
                    "n_fit_below_floor": row.get("n_fit_below_floor", 0),
                    "max_drift": row.get("max_conservation_drift_blowup_runs"),
                }
            per_shape.append(entry)
        report[axis] = per_shape
    return labels, report


def verdict_for_axis(per_shape):
    """Apply the five acceptance properties; returns (verdict_dict, lines)."""
    both = [e for e in per_shape if 256 in e and 512 in e]
    uncensored = [e for e in both
                  if e[256]["censored"] is None and e[512]["censored"] is None]
    censored_high = [e for e in both
                     if "high" in (e[256]["censored"], e[512]["censored"])]
    censored_low = [e for e in both
                    if "low" in (e[256]["censored"], e[512]["censored"])]

    tol = both[0][256]["tol"] if both else 0.0
    crits = [e[512]["critical"] for e in uncensored]
    diffs = [abs(e[512]["critical"] - e[256]["critical"]) for e in uncensored]
    nonmono = [e["label"] for e in uncensored
               if e[256]["monotone"] is False or e[512]["monotone"] is False]

    n = len(uncensored)
    spread = (max(crits) - min(crits)) if crits else 0.0
    max_diff = max(diffs) if diffs else 0.0
    med_diff = sorted(diffs)[len(diffs) // 2] if diffs else 0.0

    v = {
        "n_shapes_both_res": len(both),
        "n_uncensored": n,
        "n_censored_low": len(censored_low),
        "n_censored_high": len(censored_high),
        "bisection_tol": tol,
        # PLAN.md: "nonzero for some shapes" — a dead-flat landscape is the
        # failure mode being tested for, not one shape with a small value.
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
        # stability: resolution shift is small vs the shape spread (and we
        # also report it against the bisection tolerance for context)
        "resolution_stable": n > 0 and max_diff <= max(0.1 * spread, 2 * tol),
        "wide_band": n >= 5 and spread >= 10 * max(med_diff, tol),
    }
    v["pass"] = all((v["nonzero"], v["finite"], v["monotone"],
                     v["resolution_stable"], v["wide_band"]))
    return v


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "experiments/stage1_5_sweep.jsonl"
    table = load(path)
    labels, report = analyze(table)

    for axis in ("nu", "a"):
        name = "nu_crit (a=0)" if axis == "nu" else "a_crit (nu=0)"
        print(f"\n=== {name} ===")
        print(f"{'shape':28s} {'N=256':>10s} {'N=512':>10s} {'|diff|':>8s} "
              f"{'cens':>5s} {'mono':>5s} {'drift512':>9s}")
        for e in report[axis]:
            if 256 not in e or 512 not in e:
                continue
            c256, c512 = e[256], e[512]
            cens = c256["censored"] or c512["censored"] or "-"
            mono = str(c512["monotone"] if c512["monotone"] is not None
                       else c256["monotone"])
            drift = c512["max_drift"]
            print(f"{e['label']:28s} {c256['critical']:10.4f} "
                  f"{c512['critical']:10.4f} "
                  f"{abs(c512['critical'] - c256['critical']):8.4f} "
                  f"{cens:>5s} {mono:>5s} "
                  f"{drift if drift is None else format(drift, '9.1e')}")
        v = verdict_for_axis(report[axis])
        print(f"\n verdict[{axis}]:")
        for key, val in v.items():
            print(f"   {key}: {val}")

    va = verdict_for_axis(report["a"])
    vn = verdict_for_axis(report["nu"])
    print("\n=== STAGE 1.5 ACCEPTANCE ===")
    print(f" nu_crit passes: {vn['pass']}")
    print(f" a_crit  passes: {va['pass']}")
    if va["pass"]:
        print(" -> Stage 2 fitness axis: a_crit (preferred when both pass)")
    elif vn["pass"]:
        print(" -> Stage 2 fitness axis: nu_crit")
    else:
        print(" -> NEITHER axis passes: stop and redesign fitness "
              "(PLAN.md Stage 1.5 fallbacks)")


if __name__ == "__main__":
    main()
