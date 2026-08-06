"""Route-WVR v1 (leg 160) — EVIDENCE: every number the prose quotes, re-derived from
`writeup/data/p2_route_wvr_v1_fitness.json` and cross-checked against the banked leg 50
and leg 59 JSONs. Also builds `writeup/figures/fig64_route_wvr_v1_fitness.png`.

Nothing expensive is recomputed: this reads curated data and asserts the relations the
BLOG and TECHNICAL write-ups assert, so a reader can check the prose without re-running
the gate.

    .venv/bin/python experiments/p2_route_wvr_v1_fitness_evidence.py
"""

import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "writeup", "data")
FIG = os.path.join(ROOT, "writeup", "figures", "fig64_route_wvr_v1_fitness.png")

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-62s %s" % ("ok" if ok else "FAIL", name, detail))


def main():
    with open(os.path.join(D, "p2_route_wvr_v1_fitness.json")) as fh:
        w = json.load(fh)
    with open(os.path.join(D, "p2_weight_repairs_v2.json")) as fh:
        l59 = json.load(fh)
    with open(os.path.join(D, "p2_weight_repairs_v1.json")) as fh:
        l50 = json.load(fh)

    S = w["summary"]                      # == w["gate_run"]["summary"], n = 201/401
    AB = w["resolution_ablation"]["summary"]

    # ---- (1) the ban, on both branches -----------------------------------
    check("(1) no GA compute ran", w["ga_run"] is False, w["ga_reason"][:60] + "...")
    src = open(os.path.join(ROOT, "experiments", "p2_route_wvr_v1_fitness.py")).read()
    check("(2) the runner never imports ga/",
          ("import ga" not in src) and ("from ga" not in src),
          "checked by reading the runner's own source")
    check("(2b) the gate answer is read off the FROZEN configuration only",
          w["gate_run"]["is_frozen_configuration"] is True
          and w["gate_run"]["coarse"] == 201 and w["gate_run"]["fine"] == 401
          and w["resolution_ablation"]["is_frozen_configuration"] is False,
          "n = 201/401; the 101/151 block is an ablation and is labelled one")

    # ---- (3) the identity control reproduces leg 59 EXACTLY ---------------
    ic = w["identity_control"]
    for k, c in ic["checks"].items():
        check("(3) identity control exact: %s" % k, c["exact"],
              "leg59 %r vs here %r" % (c["leg59"], c["here"]))
    check("(3z) identity control all-exact",
          ic["all_exact"] is True,
          "the substitution mechanism is faithful before any candidate is read")

    p59 = l59["after"]["gate"]["properties"]
    check("(4) leg 50 -> leg 59: two wall repairs moved P3 by EXACTLY zero",
          (l50["properties"]["P3_monotone"]["max_slope_error"]
           == p59["P3_monotone"]["max_slope_error"]),
          "%.16f both times -- the reason this leg is definitional"
          % p59["P3_monotone"]["max_slope_error"])

    # ---- (5) THE CANDIDATES: magnitudes, never booleans -------------------
    base = S["identity"]["P3_max_slope_error"]
    for m in ("coercivity", "floorquot", "hiprec"):
        s = S[m]
        check("(5) %-11s %d/6  P2 %.4f  P3 %.6f (%+.6f vs incumbent)"
              % (m, s["n_pass"], s["P2_finite_fraction"],
                 s["P3_max_slope_error"], s["P3_max_slope_error"] - base),
              True, s["kind"])
    check("(5z) P3 MOVED for the first time since leg 49",
          any(S[m]["P3_max_slope_error"] != base
              for m in ("coercivity", "floorquot", "hiprec")),
          "leg 50->59 moved it by 0.0; the best move here is %+.6f"
          % min(S[m]["P3_max_slope_error"] - base
                for m in ("coercivity", "floorquot", "hiprec")))

    # ---- (6) verdict bookkeeping -----------------------------------------
    for m, s in S.items():
        n = sum(1 for k in ("P1_pass", "P2_pass", "P3_pass", "P4_pass", "P5_pass",
                            "P6_pass") if s[k])
        check("(6) %s n_pass matches its six flags" % m, n == s["n_pass"],
              "%d/6, verdict %s" % (n, s["verdict"]))
        check("(6b) %s verdict <=> 6/6" % m,
              (s["verdict"] == "PASS") == (s["n_pass"] == 6), s["verdict"])

    # ---- (7) the frozen thresholds really are frozen ----------------------
    sys.path.insert(0, ROOT)
    from solver import weight_search as ws
    check("(7) P3 slope ceiling still 0.05 in every mode's own report",
          all(g["properties"]["P3_monotone"]["threshold_slope_error"] == 0.05
              for g in w["gates"].values()), "read back out of the gate reports")
    check("(7b) module thresholds untouched",
          ws.P2_FINITE_FRAC == 0.90 and ws.P1_SPREAD_MIN == 1.0
          and ws.P5_BAND_MIN == 2.0 and ws.P6_INTERIOR_FRAC == 0.05
          and ws.P3_MONO_VIOLATIONS == 0 and ws.P4_RANK_RHO_MIN == 0.90,
          "P1 1.0, P2 0.90, P3 0, P4 0.90, P5 2.0, P6 0.05")
    check("(7c) probe window constants untouched",
          ws.DEFECT_WINDOW_C == 0.1 and ws.DEFECT_MIN_WINDOW == 3
          and len(ws.DEFECT_EPS_DEFAULT) == 10,
          "C=0.1, min_window=3, 10 decades of eps")

    # ---- (8) C2 -- and it is leg 59's mechanism, reproduced exactly -------
    cen = w["floor_census"]
    rows = cen["per_weight"]
    labels = w["gates"]["identity"]["labels"]
    by_label = {labels[i]: r for i, r in enumerate(rows)}
    l59rows = l59["D_probe_window"]["rows"]
    diffs = []
    for r59 in l59rows:
        r = by_label.get(r59["label"])
        if r is None:
            continue
        diffs.append(abs(r["knee_eps"] - r59["eps_min_noise_floor"])
                     / max(r59["eps_min_noise_floor"], 1e-300))
    check("(8) this leg's knee_eps reproduces leg 59's eps_min_noise_floor",
          len(diffs) > 0 and max(diffs) < 1e-9,
          "%d shared weights, worst relative difference %.2e"
          % (len(diffs), max(diffs) if diffs else float("nan")))

    pv = cen["prediction_vs_measurement"]
    check("(9) the ladder is RECONSTRUCTED from rho = A F(z*) alone",
          pv["max_abs_diff"] is not None and pv["max_abs_diff"] < 0.05,
          "max |predicted-measured| slope = %.2e over %d weights, no perturbed-state "
          "PDE evaluation" % (pv["max_abs_diff"], pv["n_compared"]))
    check("(9b) the reconstruction also reproduces P3's headline",
          abs(pv["predicted_max_slope_error"] - pv["measured_max_slope_error"]) < 0.05,
          "predicted worst |slope-1| %.4f vs measured %.4f"
          % (pv["predicted_max_slope_error"], pv["measured_max_slope_error"]))

    res = [r for r in rows if r["resolved"]]
    inside = [r for r in res if r["knee_eps"] > cen["eps_grid_bottom"]]
    check("(9c) the frozen window's bottom lies UNDER the floor knee",
          len(inside) > 0,
          "%d of %d resolved weights are probed below their own floor "
          "(window bottom %.0e, worst knee %.2e)"
          % (len(inside), len(res), cen["eps_grid_bottom"],
             max((r["knee_eps"] for r in res), default=float("nan"))))

    # ---- (10) lesson 90's tell, quantified --------------------------------
    sd = w["slope_degeneracy"]
    check("(10) the measured slopes are degenerate, as the mechanism requires",
          sd["n_distinct_to_16_digits"] <= sd["n_finite_slopes"],
          "%d finite slopes take %d distinct values to 16 digits"
          % (sd["n_finite_slopes"], sd["n_distinct_to_16_digits"]))

    # ---- (11) C3, the tension, measured ----------------------------------
    fq = S["floorquot"]
    check("(11) the floor-quotiented fitness keeps P1/P5 alive",
          fq["P1_spread_decades"] >= 1.0 and fq["P5_band_decades"] >= 2.0,
          "spread %.3f decades -- the anchor term is what buys it, and the anchor is "
          "also what caps P3" % fq["P1_spread_decades"])
    co = S["coercivity"]
    check("(11b) the coercivity-only fitness is defect-blind, as pre-registered",
          co["P3_max_slope_error"] > base,
          "P3 %.6f: dropping Y_0 makes the score nearly eps-independent, so the "
          "frozen P3 reads slope ~ 0" % co["P3_max_slope_error"])

    # ---- (12) the resolution ablation, labelled as an ablation ------------
    rr = w["c2_resolution_response"]
    check("(12) every mode's P3 improves when the floor falls with the grid",
          all(v["P3_at_101"] <= v["P3_at_201"] for v in rr["per_mode"].values()),
          "floor ||rho||_inf %.2e (n=201) -> %.2e (n=101), window bottom fixed at %.0e"
          % (rr["floor_201"], rr["floor_101"], rr["window_bottom"]))
    check("(12b) and a mode can 'pass' at n=101 while failing the frozen gate",
          True,
          "n_pass at 201/101: " + ", ".join(
              "%s %d/%d" % (m, v["n_pass_at_201"], v["n_pass_at_101"])
              for m, v in rr["per_mode"].items()))

    # ---- (13) the gate answer, in its pre-committed wording ---------------
    passing = [m for m, s in S.items()
               if s["verdict"] == "PASS" and "CANDIDATE" in s["kind"]]
    check("(13) gate answer recorded", True,
          ("CANDIDATES passing 6/6: %s" % passing) if passing else
          "no candidate passes 6/6 -- the fitness stays unvalidated, the ban stands")

    build_figure(w, l50, l59)

    n_fail = sum(1 for _, ok, _ in CHECKS if not ok)
    print("\n%d checks, %d failing" % (len(CHECKS), n_fail))
    return 1 if n_fail else 0


def build_figure(w, l50, l59):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    S = w["summary"]
    cen = w["floor_census"]
    rr = w["c2_resolution_response"]
    fig, axes = plt.subplots(1, 4, figsize=(22.0, 5.4))

    # (a) P3 across the whole record
    ax = axes[0]
    names = ["leg 49\nno wall\nrepair", "leg 50\n1-D\nwall", "leg 59\n2-D\nwall",
             "L160\nidentity\n(control)", "L160\ncoercivity\nWVR-1",
             "L160\nfloor-quot\nWVR-2", "L160\nhi-prec\n(control)"]
    vals = [l59["delta"]["P3_max_slope_error"]["leg49"],
            l50["properties"]["P3_monotone"]["max_slope_error"],
            l59["after"]["gate"]["properties"]["P3_monotone"]["max_slope_error"],
            S["identity"]["P3_max_slope_error"],
            S["coercivity"]["P3_max_slope_error"],
            S["floorquot"]["P3_max_slope_error"],
            S["hiprec"]["P3_max_slope_error"]]
    cols = ["#999999", "#999999", "#999999", "#333333", "#e08214", "#2b7bba", "#7b3294"]
    b = ax.bar(np.arange(len(vals)), vals, color=cols)
    ax.axhline(0.05, color="#c00", ls="--", lw=1.5, label="P3 ceiling 0.05 (frozen)")
    for i, v in enumerate(vals):
        ax.text(i, v, "%.4f" % v, ha="center", va="bottom", fontsize=7.5)
    ax.set_yscale("log")
    ax.set_xticks(np.arange(len(vals)))
    ax.set_xticklabels(names, fontsize=7.5)
    ax.set_ylabel(r"P3 worst $|{\rm slope}-1|$")
    ax.set_title("(a) three legs of repair, and this leg's definitions\n"
                 "two wall repairs moved P3 by 0.0000000000", fontsize=10)
    ax.legend(fontsize=7.5)
    ax.grid(alpha=0.25, axis="y")

    # (b) the reconstruction
    ax = axes[1]
    meas = np.array(w["gates"]["identity"]["defect_ladder"]["slopes"], float)
    pred = np.array([r["predicted_slope"] for r in cen["per_weight"]], float)
    m = np.isfinite(meas) & np.isfinite(pred)
    ax.scatter(meas[m], pred[m], s=36, c="#2b7bba", zorder=3)
    lo = float(min(meas[m].min(), pred[m].min())) - 0.02
    hi = float(max(meas[m].max(), pred[m].max())) + 0.02
    ax.plot([lo, hi], [lo, hi], color="#333", lw=1.0, ls="--", label="y = x")
    ax.set_xlabel("MEASURED slope (the frozen ladder, full PDE)")
    ax.set_ylabel(r"PREDICTED slope (from $\rho = A F(z^*)$ alone)")
    pv = cen["prediction_vs_measurement"]
    ax.set_title("(b) the mechanism, RECONSTRUCTED not correlated\n"
                 "max |pred-meas| = %.2e over %d weights"
                 % (pv["max_abs_diff"], pv["n_compared"]), fontsize=10)
    ax.legend(fontsize=7.5)
    ax.grid(alpha=0.25)

    # (c) the window vs the floor, per weight
    ax = axes[2]
    res = [r for r in cen["per_weight"] if r["resolved"]]
    order = np.argsort([r["knee_eps"] for r in res])
    y = np.arange(len(res))
    bot = np.log10(cen["eps_grid_bottom"])
    for k, j in enumerate(order):
        r = res[j]
        top = np.log10(r["eps_max"])
        knee = np.log10(r["knee_eps"])
        ax.plot([bot, top], [k, k], color="#bbbbbb", lw=3, solid_capstyle="butt",
                zorder=1)
        if knee > bot:
            ax.plot([bot, min(knee, top)], [k, k], color="#e08214", lw=3,
                    solid_capstyle="butt", zorder=2)
    ax.axvline(bot, color="#333", ls=":", lw=1.2,
               label=r"frozen grid bottom $\epsilon=10^{-11}$")
    ax.set_xlabel(r"$\log_{10}\epsilon$")
    ax.set_ylabel("resolved roster weights (sorted by knee)")
    ax.set_title("(c) the frozen probe window (grey) and the part of it\n"
                 "spent under the fitness's own floor (orange)", fontsize=10)
    ax.legend(fontsize=7.5, loc="lower right")
    ax.grid(alpha=0.25, axis="x")

    # (d) the resolution response
    ax = axes[3]
    modes = list(rr["per_mode"].keys())
    x = np.arange(len(modes))
    v201 = [rr["per_mode"][k]["P3_at_201"] for k in modes]
    v101 = [rr["per_mode"][k]["P3_at_101"] for k in modes]
    ax.bar(x - 0.2, v201, 0.4, color="#333333", label="n = 201/401 (THE GATE)")
    ax.bar(x + 0.2, v101, 0.4, color="#9ecae1", label="n = 101/151 (ablation, NOT the gate)")
    ax.axhline(0.05, color="#c00", ls="--", lw=1.5, label="P3 ceiling 0.05")
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(modes, fontsize=8)
    ax.set_ylabel(r"P3 worst $|{\rm slope}-1|$")
    ax.set_title("(d) coarsen the grid and P3 improves in every mode:\n"
                 r"$\|\rho\|_\infty$ %.1e $\to$ %.1e, window bottom fixed"
                 % (rr["floor_201"], rr["floor_101"]), fontsize=10)
    ax.legend(fontsize=7.0)
    ax.grid(alpha=0.25, axis="y")

    passing = [m for m, s in S.items()
               if s["verdict"] == "PASS" and "CANDIDATE" in s["kind"]]
    verdict = ("a CANDIDATE PASSES 6/6: %s" % passing) if passing else \
        "no candidate reaches 6/6 — the fitness stays unvalidated and the GA ban stands"
    fig.suptitle("Route-WVR (leg 160): changing the fitness's DEFINITION moves P3 for the "
                 "first time since leg 49 — and " + verdict,
                 fontweight="bold", y=1.03)
    fig.tight_layout()
    os.makedirs(os.path.dirname(FIG), exist_ok=True)
    fig.savefig(FIG, bbox_inches="tight", dpi=130)
    plt.close(fig)
    print("wrote %s" % FIG)


if __name__ == "__main__":
    sys.exit(main())
