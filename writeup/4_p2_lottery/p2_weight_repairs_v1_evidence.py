"""Weight-repairs v1 (fig48): the two named repairs from TECHNICAL_P2_ROUTEC_PILOT_V0
S4a/b, re-run on the frozen six-property gate. Still FAIL, 4/6 -- but P2 moves
(0.775 -> 0.875 finite) and P3's raw numbers are now honest about which weights the
probe can even validate (21/40 resolved) instead of assuming one eps grid held for
all forty.

Rebuild fig48 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_weight_repairs_v1_evidence.py
Regenerate the data (deterministic, ~140 s):
    .venv/bin/python -u experiments/p2_weight_repairs_v1.py

Four panels: A the six properties, before (leg 49) vs after (this leg), against their
frozen thresholds; B THE PICTURE -- the lower wall carried into the box, and where the
roster sits relative to it; C P3's resolution: which weights the repaired probe can
validate at all, and how the resolved ones track the known answer; D the ceiling.
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
JSON = DATA / "p2_weight_repairs_v1.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ours": "#7b1fa2"}

PROP_ORDER = ["P1_nonzero", "P2_finite", "P3_monotone",
             "P4_resolution_stable", "P5_wide_band", "P6_nontrivial_optimum"]
PROP_METRIC = {"P1_nonzero": ("spread_decades", "threshold"),
              "P2_finite": ("finite_fraction", "threshold"),
              "P3_monotone": ("max_slope_error", "threshold_slope_error"),
              "P4_resolution_stable": ("spearman", "threshold_spearman"),
              "P5_wide_band": ("band_decades", "threshold"),
              "P6_nontrivial_optimum": ("interior_margin", "threshold_margin")}


def build_figure():
    d = json.loads(JSON.read_text())
    before = d["before"]["properties"]
    after = d["after"]["gate"]["properties"]
    fig, ax = plt.subplots(2, 2, figsize=(13.5, 9.6))

    # ---- A: the six properties, before vs after -----------------------------
    a = ax[0, 0]
    x = np.arange(len(PROP_ORDER))
    b_pass = [before[p]["pass"] for p in PROP_ORDER]
    a_pass = [after[p]["pass"] for p in PROP_ORDER]
    a.bar(x - 0.18, [1.0] * 6, 0.34,
          color=[C["good"] if p else C["bad"] for p in b_pass], alpha=0.55,
          label="leg 49 (before)")
    a.bar(x + 0.18, [1.0] * 6, 0.34,
          color=[C["good"] if p else C["bad"] for p in a_pass],
          label="this leg (after repairs)")
    a.set_xticks(x)
    a.set_xticklabels([p.split("_")[0] for p in PROP_ORDER], fontsize=10)
    a.set_yticks([])
    a.set_ylim(0, 1.25)
    for i, p in enumerate(PROP_ORDER):
        a.text(i - 0.18, 1.05, "P" if b_pass[i] else "F", ha="center", fontsize=10,
              color=C["good"] if b_pass[i] else C["bad"], fontweight="bold")
        a.text(i + 0.18, 1.05, "P" if a_pass[i] else "F", ha="center", fontsize=10,
              color=C["good"] if a_pass[i] else C["bad"], fontweight="bold")
    n_before = sum(b_pass)
    n_after = sum(a_pass)
    a.set_title(f"A. THE GATE, BEFORE / AFTER — {n_before}/6 → {n_after}/6.\n"
               "Repairing P2 and P3's MECHANISM does not force a pass.", fontsize=10.5)
    a.legend(loc="lower right", fontsize=8.5)

    # ---- B: the lower wall carried into the box ------------------------------
    b = ax[0, 1]
    lw = after["P2_finite"]
    thc = np.array(d["after"]["gate"]["theta"])
    vc = np.array(d["after"]["gate"]["fitness_coarse"])
    ffp = thc[:, 0] + thc[:, 2]
    fin = np.isfinite(vc)
    b.scatter(ffp[fin], np.ones(fin.sum()) * 0.6, color=C["good"], s=40, alpha=0.7,
             label="roster: finite")
    b.scatter(ffp[~fin], np.ones((~fin).sum()) * 0.6, color=C["bad"], s=40, alpha=0.7,
             marker="x", label="roster: still censored (Z1>=1)")
    b.axvspan(-6, lw["lower_wall_power_coarse"], color=C["bad"], alpha=0.08)
    b.axvspan(0.95, 6, color=C["bad"], alpha=0.08)
    b.axvline(lw["lower_wall_power_coarse"], color=C["ours"], lw=2,
              label=f"measured lower wall  p₋={lw['lower_wall_power_coarse']:.2f}\n"
                    "(now carried in the box)")
    b.axvline(0.95, color="k", lw=1.6, ls="--", label="analytic upper wall p+q=0.95")
    b.set_xlim(-6, 3)
    b.set_ylim(0, 1.2)
    b.set_yticks([])
    b.set_xlabel("far-field power  p + q")
    b.set_title("B. THE P2 REPAIR — the box now stops short of BOTH walls.\n"
               f"finite fraction {d['delta']['P2_finite_fraction']['before']:.3f} → "
               f"{d['delta']['P2_finite_fraction']['after']:.3f} (need ≥0.90)",
               fontsize=10.5)
    b.legend(loc="upper left", fontsize=7.8)

    # ---- C: P3's resolution -- which weights the repaired probe can validate --
    c = ax[1, 0]
    res = d["after"]["gate"]["defect_ladder"]["resolution"]
    slopes = np.array(d["after"]["gate"]["defect_ladder"]["slopes"])
    resolved = np.array([r["resolved"] for r in res])
    n_win = np.array([r["n_window"] for r in res])
    order = np.argsort(n_win)
    cols = np.where(resolved[order], C["good"], C["grey"])
    c.bar(np.arange(len(order)), n_win[order], color=cols, width=1.0)
    c.axhline(3, color="k", lw=1.2, ls=":", label="DEFECT_MIN_WINDOW = 3")
    c.set_xlabel("roster weight (sorted by window size)")
    c.set_ylabel("# eps points inside this weight's own linear window")
    c.set_title(f"C. THE P3 REPAIR — per-weight windows, not one grid for all.\n"
               f"{resolved.sum()}/{len(resolved)} weights resolved at all "
               f"(green); {int((~resolved & (n_win<3)).sum())} unresolved (grey)",
               fontsize=10.5)
    c.legend(fontsize=8.5, loc="upper left")

    # ---- D: the ceiling / verdict text ---------------------------------------
    e = ax[1, 1]
    e.axis("off")
    p3 = after["P3_monotone"]
    txt = (
        "VERDICT: FAIL, 4/6 -- unchanged in COUNT, moved in SUBSTANCE.\n\n"
        f"P2 (finite): {before['P2_finite']['finite_fraction']:.3f} -> "
        f"{after['P2_finite']['finite_fraction']:.3f} (threshold 0.90). The measured "
        "lower wall now bounds the roster and the search box the way the analytic\n"
        "upper wall already did -- closer, not there: the wall is a 1-D slice "
        "(p, q=0) and the true boundary depends on L, l too.\n\n"
        f"P3 (monotone): worst |slope-1| {before['P3_monotone']['max_slope_error']:.3f}"
        f" -> {p3['max_slope_error']:.3f} among "
        f"{p3['n_resolved']}/{p3['n_resolved']+p3['n_unresolved']} weights the "
        "repaired probe can even validate (per-weight windows sized from ||A||_w,\n"
        f"fixed before this run). {p3['violations']} monotonicity violations remain "
        "inside those windows -- the honest reading is float64 roundoff at the "
        "smallest usable eps for some weights,\nnot a defect this repair claims to "
        "have fixed.\n\n"
        "NEITHER REPAIR WAS TUNED AGAINST THIS RUN'S OWN NUMBERS -- both constants "
        "(WALL_LOWER_DELTA, DEFECT_WINDOW_C) were fixed in solver/weight_search.py\n"
        "before the gate was re-run, per the plan-of-record discipline against "
        "post-hoc threshold chasing.\n\n"
        "CEILING: no link of the L1->L4 chain moved. The GA remains banned -- a "
        "same-day PASS would not have lifted it either; only the next planning\n"
        "pass may act on a gate result. This gate still says FAIL."
    )
    e.text(0.0, 1.0, txt, transform=e.transAxes, va="top", ha="left", fontsize=9.3,
          family="monospace", wrap=True)
    e.set_title("D. WHAT MOVED, WHAT DIDN'T", fontsize=10.5)

    fig.suptitle("Weight-repairs v1: the two named repairs, on the SAME frozen gate "
                "leg 49 failed", fontweight="bold", y=1.0)
    fig.tight_layout()
    fig.savefig(FIGS / "fig48_weight_repairs_v1.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    build_figure()
    print("wrote", FIGS / "fig48_weight_repairs_v1.png")
