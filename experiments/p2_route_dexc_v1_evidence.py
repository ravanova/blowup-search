#!/usr/bin/env python3
"""Rebuild fig100 for Route-DEXC (leg 382) from the curated JSON alone.

Reads writeup/data/p2_route_dexc_v1.json and re-runs NOTHING -- no interval
arithmetic, no Fourier-Motzkin elimination, no bisection.  Every value plotted is a
value the runner banked.

    .venv/bin/python experiments/p2_route_dexc_v1_evidence.py

FIGURE NUMBER: **fig100**.  Leg 382 was instructed to take fig100 and no other number
(fig96 was the highest in use at dispatch; eight figure-number collisions have already
cost this repository time, so the number is stated here plainly and registered in
writeup/build_figures.py's P2_EVIDENCE list).
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "writeup" / "data" / "p2_route_dexc_v1.json"
FIGS = ROOT / "writeup" / "figures"
FIGS.mkdir(parents=True, exist_ok=True)

# House style, matched to writeup/build_figures.py.
plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130, "font.size": 9.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "axes.axisbelow": True,
    "legend.frameon": False,
})
C_KNOWN, C_CTRL, C_FIT, C_REF = "#059669", "#dc2626", "#2563eb", "#6b7280"


def main() -> int:
    d = json.loads(DATA.read_text())
    knowns = d["planted_knowns"]
    controls = d["gate_controls"]
    probe = d["resolving_power_probes"]["probes"][0]
    ext = d["post_hoc_tolerance_extension"]

    fig, (axA, axB, axC) = plt.subplots(1, 3, figsize=(14.4, 4.6))

    # ---- PANEL A: fitted point estimate vs certified verdict ---------------
    rows = []
    for k in knowns:
        rows.append((k["id"], k["truth_exponent"], k["fitted"]["fitted_p"],
                     k["certified_cells"], True))
    for c in controls + [probe]:
        rows.append((c["id"], None, c["fitted"]["fitted_p"],
                     c["certified_cells"], False))

    ys = np.arange(len(rows))[::-1]
    for y, (tag, truth, fit_p, cert, is_known) in zip(ys, rows):
        col = C_KNOWN if is_known else C_CTRL
        axA.plot([fit_p], [y], "D", color=C_FIT, ms=7, zorder=4,
                 label="fitted (dssp_screen, unchanged)" if y == ys[0] else None)
        if cert["verdict"] == "INTERVAL":
            axA.plot([cert["p_lo"], cert["p_hi"]], [y, y], "-", color=col, lw=6,
                     solid_capstyle="butt", zorder=3)
            axA.plot([truth], [y], "|", color="#111111", ms=16, mew=2.0, zorder=5,
                     label="exact planted truth" if y == ys[0] else None)
            axA.annotate(f"certified width {cert['width']:.1e}", (cert["p_hi"], y),
                         textcoords="offset points", xytext=(10, -3), fontsize=8,
                         color=col)
        else:
            axA.annotate(f"certified {cert['verdict']}  (gap {cert['p_lo'] - cert['p_hi']:+.3f})",
                         (fit_p, y), textcoords="offset points", xytext=(10, -3),
                         fontsize=8, color=col, fontweight="bold")
    axA.set_yticks(ys)
    axA.set_yticklabels([r[0] + ("  known" if r[4] else "  MISMATCH") for r in rows])
    axA.set_xlim(0.5, 5.2)
    axA.set_ylim(-1.4, len(rows) - 0.5)
    axA.set_xlabel("decay exponent $p$   (profile $\\sim r^{-p}$)")
    axA.set_title("A. the fitted column always answers.\nthe certified column "
                  "refuses when it must.", loc="left", fontsize=10)
    axA.legend(loc="lower center", fontsize=8, ncol=2)

    # ---- PANEL B: certified width vs stated relative tolerance -------------
    wd = [r for r in ext["width_vs_delta_K2"] if r["delta"] > 0]
    dv = np.array([r["delta"] for r in wd])
    wv = np.array([r["width"] for r in wd])
    axB.loglog(dv, wv, "o-", color=C_KNOWN, lw=1.8, ms=6,
               label="measured, exact $r^{-2}$ profile")
    axB.loglog(dv, 0.8686 * dv, "--", color=C_REF, lw=1.4,
               label=r"$(4/W)\,\delta = 0.8686\,\delta$")
    floor = [r for r in ext["width_vs_delta_K2"] if r["delta"] == 0][0]["width"]
    axB.axhline(floor, color=C_FIT, lw=1.2, ls=":",
                label=f"rounding floor {floor:.1e}")
    axB.set_xlabel(r"stated relative accuracy $\delta$ of the supplied profile")
    axB.set_ylabel("certified exponent interval width")
    axB.set_title("B. what a consumer actually buys:\nhalf-width $\\approx 0.434\\,\\delta$",
                  loc="left", fontsize=10)
    axB.legend(loc="upper left", fontsize=8)

    # ---- PANEL C: critical tolerance -------------------------------------
    crit = ext["critical_tolerances"]
    labels = [c["id"] for c in crit]
    vals = [c["delta_star_lo"] for c in crit]
    cols = [C_CTRL if v > 0 else C_KNOWN for v in vals]
    xs = np.arange(len(labels))
    axC.bar(xs, [max(v, 1e-4) for v in vals], color=cols, width=0.6)
    axC.set_yscale("log")
    axC.set_xticks(xs)
    axC.set_xticklabels(labels)
    for x, c in zip(xs, crit):
        v = c["delta_star_lo"]
        axC.annotate("never excluded\n(exact power law)" if v == 0 else f"{v:.3g}",
                     (x, max(v, 1e-4)), textcoords="offset points", xytext=(0, 4),
                     ha="center", fontsize=8)
    axC.set_ylabel(r"critical tolerance $\delta^*$")
    axC.set_title("C. how clean the profile must be\nfor each mismatch to stay excluded",
                  loc="left", fontsize=10)

    fig.suptitle("fig100 — Route-DEXC (leg 382): a CERTIFIED far-field decay enclosure, "
                 "recorded alongside the fitted column, never replacing it.  "
                 "Window $[10,1000]$, $N=1000$ cells.  Validated on PLANTED knowns only — "
                 "no profile of route 4's object exists.",
                 fontsize=9.2, y=1.005)
    fig.tight_layout()
    dest = FIGS / "fig100_route_dexc_certified_decay.png"
    fig.savefig(dest, bbox_inches="tight")
    print(f"wrote {dest}")

    # ---- re-verify the banked headline numbers from the JSON alone --------
    assert d["gate"]["answer"] == "YES"
    assert all(k["certified_cells"]["contains_truth"] for k in knowns)
    assert all(c["fired"] for c in controls)
    assert d["gate"]["dssp_screen_edited"] is False
    print("gate:", d["gate"]["answer"],
          "| knowns enclosed:", len(knowns),
          "| controls fired:", sum(c["fired"] for c in controls), "/", len(controls))
    for k in knowns:
        print(f"  {k['id']}: truth {k['truth_exponent']}, certified "
              f"[{k['certified_cells']['p_lo']!r}, {k['certified_cells']['p_hi']!r}], "
              f"width {k['certified_cells']['width']:.3e}, fitted_p "
              f"{k['fitted']['fitted_p']:.12f}")
    for c in controls:
        print(f"  {c['id']}: certified {c['certified_cells']['verdict']}, gap "
              f"{c['contradiction_gap_p_lo_minus_p_hi']:.6f}, but fitted_p "
              f"{c['fitted']['fitted_p']:.6f} (a confident number for a profile with "
              "no exponent at all)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
