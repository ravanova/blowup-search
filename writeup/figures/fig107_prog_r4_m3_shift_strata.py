"""fig107 -- PROG-R4 unit U5, milestone M3: the seed budget stratified by SHIFT.

U3 ranked its 100 seeds by a single global score and spent 31 of them inside
the |s| band the eight named Lucas & Kerswell Table IV rows live in. AMENDMENT 4
had already caught the same shape of error one coordinate over, in period. U5
re-mines the anchored reservoir to exhaustion and allocates the same 100-attempt
budget by a pre-committed |s| quota. This figure is the measurement.

It is written to be correct in BOTH pre-committed branches of M3, and in both
readings of the U3 baseline it is measured against:

  H-supply -- U3's miss was a seed-supply artefact. Then panel A shows the band
              starved in U2's library and filled in U5's, and panel C shows the
              in-band yield rising once the band is properly sampled.
  H-hard   -- the band is genuinely harder. Then panel A shows the same repair
              on the supply side and panel C shows the in-band yield staying
              low anyway, which is a measurement, not a failure of the unit.

Every panel plots a magnitude, never a boolean. Panel C carries binomial
intervals precisely because the branch between those two readings turns on
whether a rate difference survives its own error bar -- U3's in-band cell has
n = 31 and one convergence, and a figure that hid that would be arguing rather
than reporting.

THIS FIGURE MAKES NO GATE CLAIM. G1 stays UNDER-RESOURCED as banked in
p2_prog_r4_g1_v1.json. `n_recovered` appears here as a count.

Checks assert the banked JSON supports every claim the panels make, including
that the plotted strata partition the |s| axis, that the counts reconcile with
the attempt rows one at a time, and that the U3 baseline drawn beside U5 is the
one re-derived from U3's own banked attempts rather than typed in. The script
exits non-zero if any check fails.

Data: writeup/data/p2_prog_r4_m3_v1.json (and p2_prog_r4_g1_v1.json, read only
      as the baseline it is compared against)
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_m3_v1.json")
U3 = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_g1_v1.json")
FIG = os.path.join(HERE, "fig107_prog_r4_m3_shift_strata.png")

TOL = 1e-8
TWO_PI = 2.0 * np.pi
BAND = (0.295, 0.707)
ORDER = ["L", "M", "P", "H"]          # left to right in |s|, not quota order
COL = {"L": "#7f8c8d", "M": "#2c3e50", "P": "#c0392b", "H": "#8e44ad"}
MRK = {"L": "o", "M": "s", "P": "o", "H": "^"}
CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail
                                                    else ""))
    return bool(ok)


def wrap_abs(s):
    return np.abs((np.asarray(s, float) + np.pi) % TWO_PI - np.pi)


def wilson(k, n, z=1.96):
    """Wilson interval. Chosen over the normal one because the cell that
    decides the reading has k = 1, n = 31, where the normal interval is
    nonsense and would understate the uncertainty this figure exists to show."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def main():
    with open(DATA) as f:
        d = json.load(f)
    with open(U3) as f:
        u3 = json.load(f)

    att = d["attempts"]
    strat = d["stratification"]
    by = strat["by_stratum"]
    base = strat["u3_baseline"]["by_stratum"]
    abs_s = np.array([a["abs_s_seed"] for a in att], float)
    finals = np.array([a["final_residual"] for a in att], float)
    ok = np.array([a["success"] for a in att], bool)
    rec = np.array([a["recovered_named_orbit"] for a in att], bool)
    u3_abs_s = wrap_abs([a["s_seed"] for a in u3["attempts"]])
    u3_ok = np.array([a["success"] for a in u3["attempts"]], bool)

    # ---- checks --------------------------------------------------------
    check("M3 answer is one of the two pre-committed branches",
          d["milestone"]["answer"] in ("DELIVERED", "NOT DELIVERED"),
          d["milestone"]["answer"])
    check("this unit did not write the G1 record",
          u3["gate"]["answer"] == "UNDER-RESOURCED",
          f"G1 still {u3['gate']['answer']}")
    check("strata partition the |s| axis with no gap and no overlap",
          all(abs(by[a]["abs_s_range"][1] - by[b]["abs_s_range"][0]) < 1e-12
              for a, b in zip(ORDER[:-1], ORDER[1:])),
          " ".join(f"{k}{by[k]['abs_s_range']}" for k in ORDER))
    check("every attempt's stratum label matches its own |s|",
          all(by[a["stratum"]]["abs_s_range"][0] - 1e-12 <= a["abs_s_seed"]
              <= by[a["stratum"]]["abs_s_range"][1] + 1e-12 for a in att))
    check("per-stratum counts reconcile with the attempt rows",
          all(by[k]["n"] == int((np.array([a["stratum"] for a in att]) == k)
                                .sum()) for k in ORDER)
          and sum(by[k]["n"] for k in ORDER) == len(att),
          f"{ {k: by[k]['n'] for k in ORDER} } sum {len(att)}")
    check("per-stratum convergence counts reconcile with the residuals",
          all(by[k]["n_converged"]
              == int(((np.array([a["stratum"] for a in att]) == k)
                      & (finals < TOL)).sum()) for k in ORDER))
    # The baseline is the whole comparison, so it is recomputed here from U3's
    # own attempt rows rather than trusted from U5's record.
    def in_stratum(v, k):
        lo, hi = by[k]["abs_s_range"]
        return (v >= lo) & (v <= hi) if k == "P" else (
            v > lo if k == "H" else (v >= lo) & (v < hi))

    check("the U3 baseline in the record is the one U3's own rows give",
          all(base[k]["n"] == int(in_stratum(u3_abs_s, k).sum())
              and base[k]["n_converged"] == int(
                  (in_stratum(u3_abs_s, k) & u3_ok).sum()) for k in ORDER)
          and sum(base[k]["n"] for k in ORDER) == len(u3["attempts"]),
          f"{ {k: (base[k]['n_converged'], base[k]['n']) for k in ORDER} }")
    check("success is the residual test, not a separate flag",
          bool(np.all(ok == (finals < TOL))))
    check("recovery implies convergence (a recovery is never a bare match)",
          bool(np.all(ok[rec])) if rec.any() else True,
          f"{int(rec.sum())} recovered")
    check("every attempt is anchored to a named Table IV row (Ban 2)",
          all(a["anchor"] in d["seed"]["rows"] for a in att))
    check("caps identical to U3's banked caps -- no iterations bought",
          (d["resourcing"]["max_newton"] == u3["resourcing"]["max_newton"]
           and d["resourcing"]["max_gmres"] == u3["resourcing"]["max_gmres"]
           and d["resourcing"]["tol"] == u3["resourcing"]["tol"]),
          f"max_newton {d['resourcing']['max_newton']}, "
          f"max_gmres {d['resourcing']['max_gmres']}")
    check("the stall exit cut none of U3's convergences",
          d["resourcing"]["stall_exit"]["u3_convergences_lost"] == 0
          and d["resourcing"]["stall_exit"]["admissible"],
          f"margin {d['resourcing']['stall_exit']['margin_factor']:.1f}x")
    check("mining strictly enlarged the anchored reservoir",
          (d["seed"]["mining"]["rule"]["n_taken"]
           > u3["seed"]["seed_supply_funnel"]["n_candidates"]
           and d["seed"]["seed_supply_funnel"]["n_anchored"]
           > u3["seed"]["seed_supply_funnel"]["n_anchored"]),
          f"{d['seed']['mining']['rule']['n_taken']:,} mined vs U2's "
          f"{u3['seed']['seed_supply_funnel']['n_candidates']:,}; admissible "
          f"{d['seed']['seed_supply_funnel']['n_anchored']:,} vs "
          f"{u3['seed']['seed_supply_funnel']['n_anchored']:,}")
    reg = d["seed"]["mining"]["regeneration_checks"]
    check("parallel regeneration reproduced the serial one bit for bit",
          bool(reg["bitwise_check_against_U2_serial_regenerate"]["bit_for_bit"])
          and reg["bitwise_check_against_U2_serial_regenerate"][
              "max_abs_difference"] == 0.0
          and bool(reg["exactness_check_against_U2_banked_library"]["exact"]),
          f"{reg['bitwise_check_against_U2_serial_regenerate']['n_indices_checked']}"
          f" indices, max|diff| "
          f"{reg['bitwise_check_against_U2_serial_regenerate']['max_abs_difference']:.3e}")
    check("controls fired as planted",
          bool(d["controls"]["fired_as_planted"]),
          str(d["controls"]["failures"]))
    check("no L1-L4 link moved", d["clay_movement"].startswith("none"))

    # ---- figure --------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))

    # A. the supply side: where the seeds could have come from, and did.
    ax = axes[0, 0]
    bins = np.linspace(0, np.pi, 40)
    ax.hist(u3_abs_s, bins=bins, color="#95a5a6", alpha=0.85,
            label=f"U3 spent (n={len(u3_abs_s)}, globally ranked)")
    ax.hist(abs_s, bins=bins, histtype="step", lw=2.0, color="#c0392b",
            label=f"U5 spent (n={len(abs_s)}, quota by $|s|$)")
    ax.axvspan(*BAND, color="#c0392b", alpha=0.10)
    # The eight named rows, drawn as ticks rather than lines: they are what the
    # band is defined by, and they crowd together, so the labels are staggered
    # instead of stacked on top of one another.
    pub = sorted({a["anchor"]: a["abs_s_published"] for a in att}.items(),
                 key=lambda kv: kv[1])
    top = ax.get_ylim()[1]
    for j, (n, v) in enumerate(pub):
        ax.plot([v], [0], marker="v", ms=7, color="#2b6cb0", clip_on=False)
        ax.annotate(n, (v, top * (0.97 - 0.075 * (j % 4))), fontsize=6,
                    rotation=90, va="top", ha="center", color="#2b6cb0")
    ax.set_xlabel(r"seed shift $|s|$, wrapped to $(-\pi,\pi]$")
    ax.set_ylabel("attempts")
    ax.set_title("A. where the budget was spent\n"
                 f"in band: U3 {strat['u3_baseline']['in_published_band']['n']}"
                 f"  ->  U5 {d['milestone']['n_seeded_in_published_band']}",
                 fontsize=10)
    ax.legend(fontsize=7, loc="upper right")
    ax.grid(alpha=0.3)

    # B. the reservoir the quota was drawn from, per stratum.
    ax = axes[0, 1]
    f = d["seed"]["seed_supply_funnel"]
    x = np.arange(len(ORDER))
    sup = [f["supply_by_stratum"][k] for k in ORDER]
    quo = [f["quota_by_stratum"][k] for k in ORDER]
    got = [f["realised_by_stratum"][k] for k in ORDER]
    ax.bar(x - 0.27, sup, 0.27, color="#bdc3c7", label="admissible supply")
    ax.bar(x, quo, 0.27, color="#34495e", label="pre-committed quota")
    ax.bar(x + 0.27, got, 0.27, color="#c0392b", label="attempts allocated")
    ax.set_yscale("log")
    for xi, v in zip(x - 0.27, sup):
        ax.annotate(str(v), (xi, v), ha="center", va="bottom", fontsize=7)
    for xi, v in zip(x + 0.27, got):
        ax.annotate(str(v), (xi, v), ha="center", va="bottom", fontsize=7,
                    color="#c0392b")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{k}\n{by[k]['label']}\n"
                        f"[{by[k]['abs_s_range'][0]:.3g},"
                        f"{by[k]['abs_s_range'][1]:.3g}]" for k in ORDER],
                       fontsize=8)
    ax.set_ylabel("candidates (log)")
    ax.set_title("B. supply, quota, spend -- the one manipulated variable\n"
                 f"admissible seeds {f['n_anchored']:,} from a re-mined "
                 f"{f['n_candidates']:,}, against U2's "
                 f"{u3['seed']['seed_supply_funnel']['n_anchored']:,} "
                 f"from {u3['seed']['seed_supply_funnel']['n_candidates']:,}",
                 fontsize=9)
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3, axis="y")

    # C. the measurement M3 exists to make.
    ax = axes[1, 0]
    for i, k in enumerate(ORDER):
        for j, (src, col, lab) in enumerate(
                [(base[k], "#95a5a6", "U3 (global rank)"),
                 (by[k], "#c0392b", "U5 (shift quota)")]):
            n, kk = src["n"], src["n_converged"]
            r = (kk / n) if n else 0.0
            lo, hi = wilson(kk, n)
            xx = i + (j - 0.5) * 0.3
            ax.bar(xx, r, 0.28, color=col,
                   label=lab if i == 0 else None)
            ax.plot([xx, xx], [lo, hi], color="k", lw=1.2)
            ax.annotate(f"{kk}/{n}", (xx, hi), ha="center", va="bottom",
                        fontsize=7)
    ax.set_xticks(np.arange(len(ORDER)))
    ax.set_xticklabels([f"{k}\n{by[k]['label']}" for k in ORDER], fontsize=8)
    ax.set_ylabel("fraction converged to tol")
    ax.set_title("C. per-stratum yield, U3 against U5\n"
                 "bars are Wilson 95% -- the cell that decides the reading "
                 "has n=31, k=1 in U3", fontsize=10)
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3, axis="y")

    # D. magnitudes, so the panel is readable under either branch.
    ax = axes[1, 1]
    for k in ORDER:
        sel = np.array([a["stratum"] == k for a in att], bool)
        if not sel.any():
            continue
        ax.semilogy(abs_s[sel], np.maximum(finals[sel], 1e-12), MRK[k], ms=5,
                    color=COL[k], alpha=0.75, ls="none",
                    label=f"{k} {by[k]['label']} "
                          f"({by[k]['n_converged']}/{by[k]['n']})")
    if rec.any():
        ax.semilogy(abs_s[rec], np.maximum(finals[rec], 1e-12), "*", ms=16,
                    mfc="none", mec="#1e8449", mew=1.6,
                    label=f"matched a named row ({int(rec.sum())})")
    ax.axhline(TOL, color="k", ls="--", lw=1.2)
    ax.annotate(r"tol $=10^{-8}$", (np.pi, TOL), fontsize=8, ha="right",
                va="bottom")
    ax.axvspan(*BAND, color="#c0392b", alpha=0.10)
    ax.set_xlabel(r"seed shift $|s|$")
    ax.set_ylabel(r"final $\|R\|$ reached")
    ax.set_title("D. how far each attempt got, against the shift it was "
                 f"seeded at\n{int(ok.sum())} of {len(att)} reached tol; "
                 f"{int(rec.sum())} matched a named row on both $T$ and $s$",
                 fontsize=10)
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3)

    fig.suptitle(
        "fig107  PROG-R4 U5 / milestone M3: the seed budget stratified by "
        f"SHIFT -- M3 {d['milestone']['answer']}"
        + (f" ({d['milestone']['not_delivered_reason']})"
           if d["milestone"]["not_delivered_reason"] else "")
        + f".  Re={d['resourcing']['Re']}, N={d['resourcing']['N']}, "
        f"T_DNS={float(d['resourcing']['T_dns']):.3g}.  "
        "G1 stays UNDER-RESOURCED; this is not a gate answer.", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(FIG, dpi=150)
    print(f"wrote {FIG}")

    bad = [n for n, ok_, _ in CHECKS if not ok_]
    print(f"\n{len(CHECKS) - len(bad)}/{len(CHECKS)} checks passed")
    if bad:
        print("FAILED: " + ", ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
