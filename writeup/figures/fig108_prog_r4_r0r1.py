"""fig108 -- PROG-R4 units R0 + R1 (Lane R, wall W7): the metric re-derived,
and the flatness abort measured.

Four panels, each a magnitude:

  A  CORE-HOURS. The two figures the programme quoted -- 144.69 and 134.45 --
     side by side with what each actually measures. Neither is a typo. The
     gap is pool utilisation, and it is drawn.

  B  THE DISTINCT COUNT. The 14 U3 convergences in the (T, |s|) plane the
     arbiter's rule actually operates in, with the tolerance box drawn to
     scale, so the reader can see that the count is 8 and where the one
     contested pair sits (0.064 apart, 1.29x the tolerance, in T alone).

  C  THE METRIC, three conventions and one reading. The three core-hour
     conventions all put U5 above U3. The cumulative reading -- orbits new to
     the PROGRAMME rather than to the run -- puts U5 below. Both are drawn,
     because reporting only the first is the failure this unit exists to catch.

  D  R1. Residual recovery against safety margin over the 9,760 rules in the
     swept family that kill no banked convergence, with the deployed rule and
     the best admissible rule marked. The headroom is the gap between them,
     and it is 0.45 percentage points.

NO GATE CLAIM AND NO CLAY CLAIM. G1 stays UNDER-RESOURCED. Every projected
quantity in panel C carries the literal label PROJECTED.

Data: writeup/data/p2_prog_r4_r0r1_v1.json (derived, banked by
      experiments/programme_r4/r0_metric.py and r1_flatness.py)
      writeup/data/p2_prog_r4_g1_v1.json (U3, read only, for panel B's points)
"""
import json
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_r0r1_v1.json")
U3P = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_g1_v1.json")
FIG = os.path.join(HERE, "fig108_prog_r4_r0r1.png")

TOL = 0.05
TWO_PI = 2.0 * math.pi
CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" -- " + detail) if detail else ""))
    return bool(ok)


def wrap_abs(s):
    a = abs(float(s)) % TWO_PI
    return min(a, TWO_PI - a)


def main():
    with open(DATA) as fh:
        d = json.load(fh)
    with open(U3P) as fh:
        u3 = json.load(fh)
    r0, r1 = d["r0"], d["r1"]
    ch = r0["core_hours"]

    fig, axes = plt.subplots(2, 2, figsize=(13.6, 9.4))

    # ---------------------------------------------------------------- panel A
    ax = axes[0][0]
    labels = ["U3\npool reservation\n(wall x workers)", "U3\nattempt CPU\n(sum of rows)",
              "U5\npool reservation", "U5\nattempt CPU"]
    vals = [ch["U3"]["pool_reservation_core_hours"], ch["U3"]["attempt_cpu_core_hours"],
            ch["U5"]["pool_reservation_core_hours"], ch["U5"]["attempt_cpu_core_hours"]]
    cols = ["#2c3e50", "#7f8c8d", "#c0392b", "#e59866"]
    ax.bar(range(4), vals, color=cols)
    for i, v in enumerate(vals):
        ax.text(i, v + 2.0, "%.2f" % v, ha="center", fontsize=9, fontweight="bold")
    ax.set_xticks(range(4))
    ax.set_xticklabels(labels, fontsize=7.5)
    ax.set_ylabel("core-hours (strictly: worker-hours)")
    ax.set_ylim(0, max(vals) * 1.22)
    ax.set_title("A. Both quoted figures are real measurements of different things.\n"
                 "Utilisation U3 %.1f%%, U5 %.1f%% -- that gap IS the discrepancy."
                 % (100 * ch["U3"]["pool_utilisation"], 100 * ch["U5"]["pool_utilisation"]),
                 fontsize=9.5)
    ax.annotate("", xy=(1, ch["U3"]["attempt_cpu_core_hours"]),
                xytext=(0, ch["U3"]["pool_reservation_core_hours"]),
                arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.4))
    ax.text(0.5, (vals[0] + vals[1]) / 2 + 8, "10.24 core-h\nstraggler idle",
            ha="center", fontsize=7.5, color="#c0392b")
    ax.grid(alpha=0.3, axis="y")

    # ---------------------------------------------------------------- panel B
    ax = axes[0][1]
    pts = [(a["attempt"], a["T_converged"], wrap_abs(a["s_converged"]))
           for a in u3["attempts"] if a["success"]]
    clusters = r0["distinct"]["U3"]["clusters"]
    palette = ["#2c3e50", "#c0392b", "#27ae60", "#8e44ad",
               "#d68910", "#16a085", "#7f8c8d", "#2980b9"]
    for i, c in enumerate(clusters):
        xs = [p[1] for p in pts if p[0] in c["attempts"]]
        ys = [p[2] for p in pts if p[0] in c["attempts"]]
        ax.scatter(xs, ys, s=52 + 26 * (c["n"] > 1), color=palette[i % len(palette)],
                   zorder=3, edgecolor="white", linewidth=0.6,
                   label="n=%d" % c["n"] if c["n"] > 1 else None)
    nf = r0["distinct"]["U3"]["narrowest_failed_merge"]
    ax.plot(nf["T"], nf["abs_s"], color="#c0392b", lw=1.3, ls="--", zorder=2)
    ax.annotate("the contested pair: attempts %d and %d,\n"
                "%.4f apart in T = %.2fx the tolerance"
                % (nf["pair"][0], nf["pair"][1], nf["dT"], nf["as_multiple_of_tol"]),
                xy=(sum(nf["T"]) / 2, nf["abs_s"][0]), xytext=(17.6, 0.20),
                fontsize=7.5, color="#c0392b",
                arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.0))
    ax.add_patch(Rectangle((20.4, 0.25), 2 * TOL, 2 * TOL, fill=False,
                           edgecolor="#7f8c8d", lw=1.2, ls=":"))
    ax.text(20.4 + TOL, 0.25 + 2 * TOL + 0.006, "TOL box, to scale\n(0.05 each way)",
            ha="center", fontsize=7, color="#7f8c8d")
    ax.set_xlabel("period T at convergence")
    ax.set_ylabel("|s| wrapped to the circle")
    ax.set_title("B. U3: %d convergences -> %d distinct under the arbiter's own rule.\n"
                 "Greedy = single = complete linkage; invariant over 20,000 orderings."
                 % (r0["distinct"]["U3"]["n_convergences"],
                    r0["distinct"]["U3"]["n_distinct_leader_greedy_implemented"]),
                 fontsize=9.5)
    ax.legend(fontsize=7, title="replicated clusters", title_fontsize=7, loc="upper left")
    ax.grid(alpha=0.3)

    # ---------------------------------------------------------------- panel C
    ax = axes[1][0]
    va = r0["metric"]["variants"]
    cu = r0["metric"]["cumulative_reading"]
    names = ["pool\nreservation", "attempt\nCPU", "elapsed\nwall-hours",
             "CUMULATIVE\n(new to programme)"]
    u3v = [va["pool_reservation"]["U3"], va["attempt_cpu"]["U3"],
           va["elapsed_wall_hours"]["U3"], cu["U3"]["per_core_hour"]]
    u5v = [va["pool_reservation"]["U5"], va["attempt_cpu"]["U5"],
           va["elapsed_wall_hours"]["U5"], cu["U5"]["per_core_hour"]]
    # elapsed wall-hours is an order of magnitude larger; plot ratios instead so
    # the four readings are commensurable, and print the raw pair on each bar.
    ratios = [b / a for a, b in zip(u3v, u5v)]
    bcols = ["#2c3e50", "#2c3e50", "#2c3e50", "#c0392b"]
    ax.bar(range(4), ratios, color=bcols)
    ax.axhline(1.0, color="#7f8c8d", lw=1.2, ls="--")
    for i, r in enumerate(ratios):
        ax.text(i, r + 0.04, "%.2fx\nU3 %.4f\nU5 %.4f" % (r, u3v[i], u5v[i]),
                ha="center", fontsize=7.5,
                fontweight="bold" if i == 3 else "normal")
    pj = r1["projection"]
    ax.text(0.02, 0.95,
            "PROJECTED (R1 replay, attempt-CPU convention):\n"
            "U3 at %.4f -> %.4f distinct orbits per core-hour, %.2fx. PROJECTED, not run."
            % (pj["measured_distinct_orbits_per_core_hour_attempt_cpu"],
               pj["PROJECTED_distinct_orbits_per_core_hour_attempt_cpu"],
               pj["PROJECTED_factor"]),
            transform=ax.transAxes, fontsize=7.2, va="top", color="#8e44ad")
    ax.set_xticks(range(4))
    ax.set_xticklabels(names, fontsize=8)
    ax.set_ylabel("U5 / U3, distinct orbits per core-hour")
    ax.set_ylim(0, max(ratios) * 1.55)
    ax.set_title("C. U5 beats U3 under every core-hour convention (1.27x-1.59x)\n"
                 "and LOSES to it, %.2fx, on orbits new to the programme."
                 % (1.0 / cu["U5_over_U3"]), fontsize=9.5)
    ax.grid(alpha=0.3, axis="y")

    # ---------------------------------------------------------------- panel D
    ax = axes[1][1]
    fr = r1["sweep"]["frontier_best_u3_recovery_at_min_margin"]
    xs = [f["margin_factor"] for f in fr]
    ys = [100 * f["u3_fraction_recovered"] for f in fr]
    ax.plot(xs, ys, "o-", color="#2c3e50", lw=1.5, ms=5,
            label="best admissible rule at each safety floor")
    inc = r1["incumbent"]
    ax.scatter([inc["margin_factor_pooled"]],
               [100 * inc["U3"]["fraction_of_epochs_recovered"]],
               s=150, marker="*", color="#c0392b", zorder=5,
               label="deployed rule (K=20, W=10, theta=0.5)")
    hr = r1["headroom"]
    ax.scatter([hr["margin_factor"]], [100 * hr["best_admissible_u3_recovery"]],
               s=110, marker="D", facecolor="none", edgecolor="#27ae60", lw=1.8,
               zorder=5, label="best at no loss of margin (K=21, W=10, theta=0.1)")
    uo = r1["sweep"]["unconstrained_optimum"]
    ax.scatter([uo["margin_factor"]], [100 * uo["u3_fraction_recovered"]],
               s=110, marker="X", color="#8e44ad", zorder=5,
               label="unconstrained optimum -- REJECTED at %.2fx margin" % uo["margin_factor"])
    ax.set_xscale("log")
    ax.set_xlabel("safety margin factor (theta / worst banked convergence window ratio)")
    ax.set_ylabel("% of U3's 4,629 epochs recovered")
    ax.set_title("D. R1: %d of %d deterministic rules kill no banked convergence.\n"
                 "Headroom over the deployed rule: %+.2f pp = %+.2f core-hours."
                 % (r1["sweep"]["n_zero_false_kill"], r1["sweep"]["grid"]["n_rules"],
                    hr["headroom_percentage_points"], hr["headroom_core_hours_u3"]),
                 fontsize=9.5)
    ax.legend(fontsize=7, loc="upper right")
    ax.grid(alpha=0.3, which="both")

    fig.suptitle("fig108  PROG-R4 R0+R1 (Lane R, W7): both headline figures re-derived from the "
                 "banked artefacts. Core-hours AGREE (144.69 / 57.04); the distinct count AGREES "
                 "(8 / 5).\nThe INFERENCE does not: 57 of U5's 100 seeds were already spent by U3 "
                 "and 5 of its 9 convergences are bit-identical re-executions. TIER 2, no gate "
                 "claim, no Clay movement.", fontsize=9.5)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(FIG, dpi=150)
    print("wrote %s" % FIG)

    # ------------------------------------------------------------- the checks
    check("panel A plots the two core-hour conventions banked in the JSON",
          abs(vals[0] - 144.6888) < 5e-4 and abs(vals[1] - 134.4475) < 5e-4,
          "144.6888 pool / 134.4475 attempt CPU")
    check("panel A's utilisation gap equals 144.6888 - 134.4475",
          abs((vals[0] - vals[1]) - 10.2413) < 5e-4)
    check("panel B plots all 14 U3 convergences, no more and no fewer",
          len(pts) == 14 and sum(c["n"] for c in clusters) == 14)
    check("panel B draws exactly 8 clusters",
          len(clusters) == 8
          == r0["distinct"]["U3"]["n_distinct_leader_greedy_implemented"])
    check("panel B's contested pair is separated in T alone, at 1.29x TOL",
          abs(nf["dT"] - nf["chebyshev_distance"]) < 1e-12
          and abs(nf["as_multiple_of_tol"] - 1.2883) < 5e-4)
    check("panel C's three conventions all exceed 1.0",
          all(r > 1.0 for r in ratios[:3]),
          "%.3f, %.3f, %.3f" % tuple(ratios[:3]))
    check("panel C's cumulative reading is below 1.0 and is drawn in red",
          ratios[3] < 1.0 and bcols[3] == "#c0392b",
          "%.4f -- U5 is %.2fx worse on orbits new to the programme"
          % (ratios[3], 1.0 / ratios[3]))
    check("every projected number in panel C carries the literal label PROJECTED",
          "PROJECTED" in ax.get_figure().axes[2].texts[-1].get_text()
          and pj["LABEL"] == "PROJECTED")
    check("panel D's deployed rule sits at 55.0% recovery and a 6.90x margin",
          abs(100 * inc["U3"]["fraction_of_epochs_recovered"] - 55.00) < 5e-2
          and abs(inc["margin_factor_pooled"] - 6.9016) < 5e-4)
    check("panel D's headroom is the +0.45 pp gap it annotates",
          abs(hr["headroom_percentage_points"] - 0.4537) < 5e-4
          and abs(hr["best_admissible_u3_recovery"]
                  - inc["U3"]["fraction_of_epochs_recovered"]
                  - hr["headroom_percentage_points"] / 100.0) < 1e-9)
    check("panel D's rejected optimum is labelled as rejected, at 1.09x margin",
          abs(uo["margin_factor"] - 1.0937) < 5e-4 and "NOT ADOPTED" in uo["why_rejected"])
    check("the figure makes no gate claim and no Clay claim",
          d["clay_movement"].startswith("none"))

    bad = [n for n, ok, _ in CHECKS if not ok]
    print("\n%d/%d checks passed" % (len(CHECKS) - len(bad), len(CHECKS)))
    if bad:
        print("FAILED: " + ", ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
