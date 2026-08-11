#!/usr/bin/env python3
"""fig82 -- Leg 305 (Route-DWM): per-constant width ledger of BCG's r-dominance argument.

Every number plotted is READ FROM writeup/data/p2_route_dwm_v1.json.  Nothing is hardcoded and
nothing is retyped -- leg 315 found that float64 had silently truncated leg 300's exact
(7+3sqrt5)/2 in prose, and the cheapest defence against that class of error is to never let a
number exist in two places.  The JSON is the single source; this script only draws it.

    .venv/bin/python experiments/p2_route_dwm_v1_evidence.py
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "writeup" / "data" / "p2_route_dwm_v1.json"
OUT = HERE.parent / "writeup" / "figures" / "fig82_route_dwm_v1_ledger.png"


def main():
    d = json.loads(DATA.read_text())
    rows = d["ledger"]
    win = d["checks"]
    lo = float(win["lower_endpoint"])
    hi = float(win["upper_endpoint"])
    ratio = float(win["width_ratio"])
    costliest = d["costliest_constant"]["constant"]

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(13.4, 5.6))

    # ---- Panel A: how far each constant must move to close the deficit -------------------
    names = [r["constant"] for r in rows]
    finite, inf_idx = [], []
    for i, r in enumerate(rows):
        if r["M3_move_to_close"] == "unreachable":
            finite.append(0.0)
            inf_idx.append(i)
        else:
            finite.append(abs(float(r["M3_move_to_close"])) * 100.0)

    y = list(range(len(names)))[::-1]
    colors = ["#b2182b" if n == costliest else
              ("#cccccc" if i in inf_idx else "#4393c3")
              for i, n in enumerate(names)]
    axA.barh(y, finite, color=colors, edgecolor="black", linewidth=0.6)
    axA.set_yticks(y)
    axA.set_yticklabels(names, fontsize=9)
    axA.set_xscale("symlog", linthresh=1.0)
    axA.set_xlabel("|relative move needed to close the deficit|  (%)  -- log scale")
    axA.set_title("A.  Per-constant width ledger: what it would take to reach width 1/6",
                  fontsize=10.5)
    for i, n in enumerate(names):
        yy = y[i]
        if i in inf_idx:
            axA.text(1.1, yy, "unreachable: $r^\\ast$ is at a stationary MAXIMUM "
                              "of this family", va="center", fontsize=7.6, color="#555555")
        else:
            axA.text(finite[i] * 1.15, yy, "%.2f%%" % finite[i], va="center", fontsize=8)
    axA.axvline(0, color="black", linewidth=0.8)
    axA.set_xlim(0, 3000)

    # ---- Panel B: the two windows on the r-axis, and the counterfactual ------------------
    axB.axhline(1.0, color="black", linewidth=0.8)
    axB.plot([1.0, lo], [1.0, 1.0], linewidth=11, color="#f4a582",
             solid_capstyle="butt", label="target window $(1,\\,7/6]$: $F_{dis}$ NOT dominated")
    axB.plot([lo, hi], [1.0, 1.0], linewidth=11, color="#2166ac",
             solid_capstyle="butt", label="dominance window $(7/6,\\,r^\\ast)$: certified")
    for x, lab in ((1.0, "$r=1$"), (lo, "$2\\gamma/(\\gamma+1)$"), (hi, "$r^\\ast$")):
        axB.axvline(x, color="black", linewidth=0.6, linestyle=":")
        axB.text(x, 1.055, lab, ha="center", fontsize=9)

    cf = d.get("counterfactual", {})
    if cf:
        lo_cf = float(cf["lower_endpoint_after"])
        axB.plot([lo_cf, hi], [0.80, 0.80], linewidth=11, color="#66bd63",
                 solid_capstyle="butt",
                 label="counterfactual: $c_{lap}\\to%.6f$, i.e. $\\nu(-\\Delta)^{s}$, $s=%.7f$"
                       % (float(cf["c_lap_after"]), float(cf["fractional_order_s"])))
        axB.axvline(lo_cf, color="#1a9850", linewidth=0.8, linestyle="--")
        axB.text(lo_cf, 0.735, "$c_{lap}^{\\ast}$", ha="center", fontsize=9, color="#1a9850")
        axB.text((lo_cf + hi) / 2, 0.855, "width $=1/6$: deficit closed, but this is a\n"
                 "DIFFERENT PDE (hypodissipation), not a sharper proof",
                 ha="center", fontsize=7.8, color="#1a9850")

    axB.set_ylim(0.62, 1.16)
    axB.set_yticks([])
    axB.set_xlabel("self-similar exponent $r$   ($\\gamma = 7/5$)")
    axB.set_title("B.  The %.4f$\\times$ deficit, and the only move that closes it" % ratio,
                  fontsize=10.5)
    axB.legend(loc="lower left", fontsize=7.8, framealpha=0.95)

    fig.suptitle("fig82 -- Leg 305 (Route-DWM): the %.4f$\\times$ dominance-window deficit is "
                 "SHARP for BCG's argument as stated.\nAll eleven constants are exact "
                 "identities; the costliest is %s.  3D COMPRESSIBLE Navier-Stokes "
                 "(BCG, arXiv:2208.09445) -- NOT Clay's incompressible system."
                 % (ratio, costliest), fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=160)
    print(OUT.name)


if __name__ == "__main__":
    main()
