#!/usr/bin/env python3
"""Rebuild fig102 for Route-ST2G (leg 383) from the curated JSON alone.

Reads writeup/data/p2_route_st2g_v1.json and re-runs NOTHING -- no quadrature, no
screen call, no field evaluation. Every value plotted is a value the runner banked.

    .venv/bin/python experiments/p2_route_st2g_v1_evidence.py

FIGURE NUMBER: **fig102**. Leg 383 was instructed to take fig102 and no other number
(fig100 and fig101 were already allocated this cycle to legs 382 and 233). Figure-number
collisions have cost this repository time before, so the number is stated plainly here
and registered in writeup/build_figures.py's P2_EVIDENCE list.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "writeup" / "data" / "p2_route_st2g_v1.json"
FIGS = ROOT / "writeup" / "figures"
FIGS.mkdir(parents=True, exist_ok=True)

# House style, matched to writeup/build_figures.py.
plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130, "font.size": 9.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "axes.axisbelow": True,
    "legend.frameon": False,
})
C_FIRE, C_SILENT, C_BEFORE, C_REF = "#dc2626", "#2563eb", "#9ca3af", "#6b7280"


def main() -> int:
    d = json.loads(DATA.read_text())
    rows = d["controls"]
    ci = d["gate_clause_i_tsai_headline"]

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(13.0, 4.8))

    # ---- PANEL A: what the report path said BEFORE vs AFTER the rewiring ----
    ys = np.arange(len(rows))[::-1]
    # "EXCLUDED" is leg 357's original BINARY vocabulary, which the before-column
    # still speaks: the old reading could say only EXCLUDED / NOT EXCLUDED, with no
    # clause attached. It gets its own tick rather than being silently folded into
    # EXCLUDED-BY-T1.
    verdict_order = ["NOT EXCLUDED", "NOT-REACHED-BY-ANSATZ",
                     "EXCLUDED-BY-T2", "EXCLUDED-BY-T1", "EXCLUDED"]
    xpos = {v: i for i, v in enumerate(verdict_order)}
    for y, r in zip(ys, rows):
        col = C_FIRE if r["required_direction"] == "FIRE" else C_SILENT
        xb, xa = xpos[r["verdict_before_rewiring"]], xpos[r["verdict_after_rewiring"]]
        if xb != xa:
            axA.annotate("", xy=(xa, y), xytext=(xb, y),
                         arrowprops=dict(arrowstyle="->", color=col, lw=1.4))
        axA.plot([xb], [y], "o", ms=6, mfc="none", mec=C_BEFORE, zorder=3)
        axA.plot([xa], [y], "o", ms=7, color=col, zorder=4)
    axA.set_yticks(ys)
    axA.set_yticklabels([f"{r['id']}  [{r['required_direction']}]" for r in rows])
    axA.set_xticks(range(len(verdict_order)))
    axA.set_xticklabels(["NOT\nEXCLUDED", "NOT-REACHED\nBY-ANSATZ",
                          "EXCLUDED\nBY-T2", "EXCLUDED\nBY-T1",
                          "EXCLUDED\n(357 binary)"], fontsize=8.5)
    axA.set_xlim(-0.5, len(verdict_order) - 0.5)
    axA.set_title("A. screen_candidate()'s NRS/Tsai verdict\n"
                   "hollow = before rewiring (main @ 104f5b3), filled = after",
                   fontsize=9.5)
    axA.plot([], [], "o", color=C_FIRE, label="control required to FIRE")
    axA.plot([], [], "o", color=C_SILENT, label="control required to stay SILENT")
    axA.plot([], [], "o", mfc="none", mec=C_BEFORE, label="verdict before rewiring")
    axA.legend(loc="lower right", fontsize=8)

    # ---- PANEL B: the decay exponents the classification turns on ----------
    ids = [r["id"] for r in rows]
    exps = [r["fitted_decay_exponent"] for r in rows]
    cols = [C_FIRE if r["required_direction"] == "FIRE" else C_SILENT for r in rows]
    xs = np.arange(len(rows))
    axB.bar(xs, exps, color=cols, width=0.6, zorder=3)
    axB.axhline(ci["tsai_source_exponent_eq_1_5"], color=C_REF, ls="--", lw=1.2,
                 label=f"Tsai 1998 eq (1.5): exactly {ci['tsai_source_exponent_eq_1_5']:g}")
    axB.axhline(0.0, color="black", lw=0.8)
    axB.set_xticks(xs)
    axB.set_xticklabels(ids)
    axB.set_ylabel("fitted far-field decay exponent")
    for x, r in zip(xs, rows):
        e = r["fitted_decay_exponent"]
        axB.annotate(f"{e:.4f}", (x, e), textcoords="offset points",
                     xytext=(0, 6 if e >= 0 else -14), ha="center", fontsize=8)
    axB.set_title("B. the exponent each classification turns on\n"
                   f"repo's own measured {ci['repo_measured_exponent_on_field_uB']:.6f} "
                   f"vs source -1: |diff| {ci['abs_difference_repo_vs_source']:.2e}",
                   fontsize=9.5)
    axB.legend(loc="upper left", fontsize=8)

    fig.suptitle("fig102 -- Route-ST2G (leg 383): the DSSP screen's report path learns "
                  "Tsai Thm 2 and the SS/DSS ansatz check. "
                  f"GATE: {d['gate_answer']}. CEILING: TIER 2 (surviving a screen is not "
                  "evidence for existence).", fontsize=10)
    # C5 is a SILENT-direction control whose VERDICT nevertheless moves: its
    # required silence is on the ANSATZ column (the ansatz clause must not fire on a
    # static, non-periodic candidate), not on the verdict. Said plainly on the figure
    # so panel A cannot be misread.
    fig.text(0.012, 0.015,
             "C5's required silence is on the ANSATZ column (EXACT-SS, satisfies=True), "
             "not on the verdict -- it is the C1 field, so its verdict legitimately moves "
             "to EXCLUDED-BY-T2.",
             fontsize=8, color=C_REF)
    fig.tight_layout(rect=(0, 0.045, 1, 0.93))
    out = FIGS / "fig102_route_st2g_v1.png"
    fig.savefig(out)
    print(f"wrote {out}")

    # Re-state the load-bearing numbers from the JSON, so this script is also a
    # claims check and not only a plotter.
    print(f"  gate answer (from JSON): {d['gate_answer']}")
    print(f"  clause (i): planted C1 exponent {ci['planted_field_fitted_exponent']!r}, "
          f"|diff| vs source {ci['abs_difference_planted_vs_source']:.3e}; "
          f"{ci['verdict_before_rewiring']} -> {ci['verdict_after_rewiring']}")
    cii = d["gate_clause_ii_dss_object"]
    print(f"  clause (ii): lambda {cii['measured_lambda']!r} -> "
          f"{cii['verdict_after_rewiring']}, exact-SS-ansatz deciding clause: "
          f"{cii['deciding_clause_is_exact_ss_ansatz']}")
    print(f"  all controls pass: {d['all_controls_pass']}; two-directional: "
          f"{d['gate_qualifier_both_directions']['battery_is_two_directional']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
