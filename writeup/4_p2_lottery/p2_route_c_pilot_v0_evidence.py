"""Phase-2 Route-C-PILOT v0 (fig44): the certificate-weight fitness, and the gate it failed.

Stage C-PILOT asked whether the one number that decides a certificate — Y0 divided by
the budget the other two constants leave it — is safe to hand to a genetic algorithm.
The gate says no, on two of six properties, and the reasons are specific enough to
price what would fix them. Along the way the leg reproduced the premise the stage was
built on (leg 46's 5186x between a naive and a hand-tuned weight), located where that
effect actually lives (the border rows, not the weight family), and found that the
float rehearsal's admissible band closes entirely at n ~ 3.2e3.

Rebuild fig44 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_c_pilot_v0_evidence.py
Regenerate the data (deterministic, ~70 s):
    .venv/bin/python -u experiments/p2_route_c_pilot_v0.py

Six panels: A the known-answer ladders that make CLM a substrate; B the premise, and the
gauge ablation that explains it; C the searched weight against the two hand-picked ones;
D the six properties against their frozen thresholds; E THE PICTURE — the two walls and
the band between them, closing under refinement; F the fitness's response to a known
defect, and the window in which its known answer holds.
"""

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DATA = Path(__file__).resolve().parents[1] / "data"
FIGS = Path(__file__).resolve().parents[1] / "figures"
JSON = DATA / "p2_route_c_pilot_v0.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ours": "#7b1fa2"}


def build_figure():
    d = json.loads(JSON.read_text())
    ka, pre = d["C0_2_known_answers"], d["C0_3_premise"]
    gate, search = d["C0_4_gate"], d["C0_5_search"]
    walls, p3 = d["C0_6_walls"], d["C0_4_p3_diagnosis"]
    fig, ax = plt.subplots(2, 3, figsize=(16.8, 9.8))

    # ---- A: the substrate's known answers --------------------------------
    a = ax[0, 0]
    ns = [r["n"] for r in ka["profile_distance"]]
    dist = [r["sup_distance_to_exact"] for r in ka["profile_distance"]]
    xm = [r["X_max"] for r in ka["c_omega_vs_reach"]]
    cerr = [r["error_vs_exact"] for r in ka["c_omega_vs_reach"]]
    a.loglog(ns, dist, "o-", color=C["anchor"], label=r"$\|\Omega-\Omega_0\|_\infty$ vs $n$")
    a.loglog(xm, cerr, "s--", color=C["ours"], label=r"$|c_\omega+1|$ vs $X_{max}$")
    a.loglog(xm, [cerr[0] * (xm[0] / x) for x in xm], ":", color=C["grey"],
             label=r"$1/X_{max}$")
    a.set_xlabel("resolution $n$   /   reach $X_{max}$")
    a.set_ylabel("error")
    a.set_title("A. two knobs, two known answers\n"
                "spacing fixes the profile, reach fixes the constant", fontsize=10)
    a.legend(fontsize=8)
    a.grid(alpha=0.3, which="both")

    # ---- B: the premise and the gauge ablation ---------------------------
    b = ax[0, 1]
    bars = [("leg 46\n(HL object)", pre["leg46_reported_gain_HL"], C["grey"]),
            ("this leg\nimplicit gauge", pre["gain_implicit_gauge"], C["good"]),
            ("this leg\nc_l pinned", pre["gain_stiff_gauge"], C["bad"])]
    b.bar(range(3), [v for _, v, _ in bars], color=[c for _, _, c in bars], alpha=0.85)
    b.set_yscale("log")
    b.set_ylim(0.2, 4e4)
    b.axhline(1.0, color="k", lw=1)
    b.set_xticks(range(3))
    b.set_xticklabels([t for t, _, _ in bars], fontsize=8)
    b.set_ylabel(r"gain: naive $\to$ hand-tuned $w_l$  ($\times$)")
    for i, (_, v, _) in enumerate(bars):
        b.text(i, v * 1.4, f"{v:.3g}x", ha="center", fontsize=9)
    b.set_title("B. the premise reproduces — and dies\nwhen the gauge stops being implicit",
                fontsize=10)
    b.grid(alpha=0.3, axis="y")

    # ---- C: the searched weight vs the hands -----------------------------
    c = ax[0, 2]
    labs = ["naive", "leg 46\nhand-tuned", "searched"]
    vals = [search["fitness_naive"], search["fitness_tuned_leg46"],
            search["fitness_star"]]
    cols = [C["bad"] if v >= 0 else C["good"] for v in vals]
    c.bar(range(3), vals, color=cols, alpha=0.85)
    c.axhline(0.0, color="k", lw=1.2)
    c.text(0.02, 0.06, "below the line the certificate closes", transform=c.transAxes,
           fontsize=8, color=C["good"])
    c.set_xticks(range(3))
    c.set_xticklabels(labs, fontsize=8)
    c.set_ylabel(r"$\log_{10}(Y_0/\mathrm{budget})$")
    c.set_ylim(min(vals) - 1.4, max(vals) + 1.2)
    for i, v in enumerate(vals):
        c.text(i, v + (0.18 if v >= 0 else -0.55), f"{v:+.2f}", ha="center", fontsize=9)
    c.set_title(f"C. the search beats the hand\n{search['gain_over_naive']:.3g}x over naive,"
                f" {search['gain_over_tuned']:.2f}x over leg 46", fontsize=10)
    c.grid(alpha=0.3, axis="y")

    # ---- D: the six properties -------------------------------------------
    dd = ax[1, 0]
    props = gate["properties"]
    keys = list(props)
    # each property as measured / threshold, so 1.0 is the bar to clear
    ratios, names, ok = [], [], []
    spec = {
        "P1_nonzero": ("spread_decades", "threshold", True),
        "P2_finite": ("finite_fraction", "threshold", True),
        "P3_monotone": ("max_slope_error", "threshold_slope_error", False),
        "P4_resolution_stable": ("spearman", "threshold_spearman", True),
        "P5_wide_band": ("band_decades", "threshold", True),
        "P6_nontrivial_optimum": ("interior_margin", "threshold_margin", True),
    }
    for k in keys:
        m, t, higher = spec[k]
        r = props[k][m] / props[k][t]
        ratios.append(r if higher else 1.0 / max(r, 1e-9))
        names.append(k.split("_", 1)[0] + "\n" + k.split("_", 1)[1].replace("_", "\n"))
        ok.append(props[k]["pass"])
    dd.bar(range(6), ratios, color=[C["good"] if o else C["bad"] for o in ok], alpha=0.85)
    dd.axhline(1.0, color="k", lw=1.2)
    dd.set_yscale("log")
    dd.set_xticks(range(6))
    dd.set_xticklabels(names, fontsize=6.5)
    dd.set_ylabel("measured / threshold  (1 = the bar)")
    dd.set_title(f"D. the frozen predicate: {sum(ok)}/6 — VERDICT {gate['verdict']}\n"
                 "the GA stays banned", fontsize=10)
    dd.grid(alpha=0.3, axis="y")

    # ---- E: THE PICTURE — the two walls and the band ----------------------
    e = ax[1, 1]
    ns_w = [r["n"] for r in walls["ladder"]]
    pm = [r["p_minus"] for r in walls["ladder"]]
    up = walls["analytic_upper_wall"]
    e.fill_between(ns_w, pm, [up] * len(ns_w), color=C["good"], alpha=0.18,
                   label="admissible band")
    e.plot(ns_w, pm, "o-", color=C["bad"], label=r"measured lower wall $p_-$  ($Z_1=1$)")
    e.axhline(up, color=C["anchor"], lw=2,
              label=r"analytic wall $p^*=1$  ($\|\Omega_0\|_\nu=\infty$ above)")
    e.set_xscale("log")
    e.set_xlabel("resolution $n$")
    e.set_ylabel("far-field power $p+q$")
    e.set_ylim(-4.5, 3.4)
    closed = [r["n"] for r in walls["ladder"] if r["p_minus"] >= up]
    if closed:
        e.axvline(closed[0], color=C["bad"], ls=":", lw=2)
        e.text(closed[0], -4.2, f" band empty\n at n={closed[0]}", fontsize=8,
               color=C["bad"], va="bottom")
    e.legend(fontsize=7.5, loc="upper left")
    e.set_title("E. two walls, and only one of them is mathematics\n"
                "the float rehearsal's band shuts under refinement", fontsize=10)
    e.grid(alpha=0.3)

    # ---- F: the fitness's response to a known defect ----------------------
    f = ax[1, 2]
    eps = [r["eps"] for r in p3["linearity_check"]]
    dev = [r["rel_dev_from_eps_d"] for r in p3["linearity_check"]]
    f.loglog(eps, dev, "o-", color=C["ours"],
             label=r"$\|A F(z+\epsilon d)-\epsilon d\|/\epsilon$")
    f.axhline(0.01, color=C["grey"], ls=":", label="1% of the linear term")
    a_norm = p3["A_norm_at_tuned"]
    f.axvline(1.0 / a_norm, color=C["anchor"], ls="--",
              label=r"$1/\|A\|$ = %.1e" % (1.0 / a_norm))
    f.set_xlabel(r"perturbation $\epsilon$")
    f.set_ylabel("relative departure from linear")
    f.set_title("F. where the known answer (slope 1) is valid\n"
                f"inside it, median |slope-1| = {p3['median_abs_slope_error']:.4f}, "
                f"worst {p3['max_abs_slope_error']:.3f}", fontsize=10)
    f.legend(fontsize=7.5)
    f.grid(alpha=0.3, which="both")

    fig.suptitle("Route-C-PILOT v0 — searching the certificate's function space on an "
                 "object whose answer is known: the fitness FAILS the viability gate",
                 fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    out = FIGS / "fig44_route_c_pilot_v0.png"
    fig.savefig(out, dpi=150)
    print(f"wrote {out}")


if __name__ == "__main__":
    build_figure()
