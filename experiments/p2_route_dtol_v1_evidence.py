#!/usr/bin/env python3
"""Rebuild fig99 for Route-DTOL (leg 386) from the curated JSON alone.

Reads writeup/data/p2_route_dtol_v1.json and re-runs NOTHING -- no interval arithmetic,
no Fourier-Motzkin elimination, no bisection.  Every value plotted is a value the runner
banked.

    .venv/bin/python experiments/p2_route_dtol_v1_evidence.py

FIGURE NUMBER: **fig99**.  Leg 386 was allocated fig99 at dispatch and takes that number
and no other; it was reserved for leg 381, which drew no figure and left it unused.
Registered in writeup/build_figures.py's P2_EVIDENCE list.

WHAT THE TWO PANELS SAY, so the figure is not over-read:

  (a) the width law is a property of the WINDOW.  The closed form
      width = 4 log(1+delta)/log(R1/R0) tracks the measurement to +0.51% over nine decades
      of delta, and the coefficient DOUBLES when the window is shortened from [10,1000] to
      [10,100] -- so leg 382's 0.8686 is 4/log(100), not an instrument constant.

  (b) the composed delta window of CLAY_OBLIGATIONS §4 exists ONLY to the right of the
      threshold.  Each bar is a measured [delta_min, delta_max]; there is no bar at or
      below alpha_centre = 1, which is the alpha the banked Type-I object carries.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "writeup" / "data" / "p2_route_dtol_v1.json"
FIGS = ROOT / "writeup" / "figures"
FIGS.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130, "font.size": 9.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "axes.axisbelow": True,
    "legend.frameon": False,
})
C_PRIM, C_SEC, C_REF, C_EMPTY = "#2563eb", "#059669", "#6b7280", "#dc2626"
SHAPE_C = {"two_power": "#2563eb", "rational_cutoff": "#059669", "log_corrected": "#b45309"}
SHAPE_L = {"two_power": "two-power", "rational_cutoff": "rational cutoff",
           "log_corrected": "log-corrected"}


def main() -> int:
    d = json.loads(DATA.read_text())
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11.2, 4.3))

    # ---- panel (a): the width law, measured against the closed form ----------
    wl = d["clause1_a_width_law"]
    for tag, colour, label in (("primary_10_1000", C_PRIM, "window [10, 1000]"),
                               ("secondary_10_100", C_SEC, "window [10, 100]")):
        rows = [r for r in wl["rows"] if r["window"] == tag]
        x = np.array([r["delta"] for r in rows])
        y = np.array([r["width_measured"] for r in rows])
        yp = np.array([r["width_predicted_closed_form"] for r in rows])
        order = np.argsort(x)
        ax0.plot(x[order], yp[order], "-", color=colour, lw=1.2, alpha=0.55,
                 label=f"closed form, {label}")
        ax0.plot(x[order], y[order], "o", color=colour, ms=5, label=f"measured, {label}")
    ax0.set_xscale("log"); ax0.set_yscale("log")
    ax0.set_xlabel(r"tolerance  $\delta$")
    ax0.set_ylabel("certified width of the exponent enclosure")
    cp = wl["measured_small_delta_coefficient_primary"]
    cs = wl["measured_small_delta_coefficient_secondary"]
    ax0.set_title("(a) the width law is a property of the WINDOW\n"
                  rf"measured $/$ closed form $= {wl['ratio_min']:.6f}$–${wl['ratio_max']:.6f}$",
                  fontsize=10)
    ax0.legend(loc="upper left", fontsize=8)
    ax0.text(0.97, 0.06,
             f"coefficient  {cp:.5f}  vs  {cs:.5f}\n"
             f"ratio {wl['secondary_over_primary_measured']:.6f}  (predicted exactly 2)\n"
             r"$4/\log 100 = 0.868589$;  leg 382's lead $0.8686$",
             transform=ax0.transAxes, ha="right", va="bottom", fontsize=8, color=C_REF)

    # ---- panel (b): the composed delta window vs the REALISED alpha_centre ---
    rows = [r for r in d["clause2_delta_windows"]["rows"]
            if r["alpha_threshold"] == 1.0]
    ax1.axvspan(0.0, 1.0, color=C_EMPTY, alpha=0.07, zorder=0)
    ax1.axvline(1.0, color=C_EMPTY, lw=1.3, ls="--", zorder=1)
    seen = set()
    for r in rows:
        ac, dmin, dmax = r["alpha_centre"], r["delta_min"], r["delta_max"]
        c = SHAPE_C[r["shape"]]
        lab = SHAPE_L[r["shape"]] if r["shape"] not in seen else None
        seen.add(r["shape"])
        if not r["admissible"]:
            ax1.plot([ac], [0.04], "x", color=c, ms=7, mew=1.6, label=lab)
            continue
        capped = bool(r.get("capped"))
        ax1.plot([ac, ac], [dmin, dmax], "-", color=c, lw=3.0, alpha=0.85, label=lab)
        ax1.plot([ac], [dmin], "o", color=c, ms=4.5)
        ax1.plot([ac], [dmax], ("^" if capped else "o"), color=c, ms=5,
                 mfc=("none" if capped else c))
    a = np.linspace(1.0, 4.3, 200)
    ax1.plot(a, (a - 1.0) / 0.43429448190325176, "-", color=C_REF, lw=1.1,
             label=r"leg 381's law  $\delta<(\alpha_c-1)/0.434$")
    ax1.set_yscale("log")
    ax1.set_ylim(0.03, 60)
    ax1.set_xlim(0.35, 4.3)
    ax1.set_xlabel(r"realised certified centre  $\alpha_{\rm centre}$")
    ax1.set_ylabel(r"admissible tolerance  $\delta$")
    ax1.set_title(r"(b) §4's composed $\delta$ window: EMPTY at $\alpha_{\rm centre}\leq 1$"
                  "\n" r"$\times$ = no window at all;  $\triangle$ = capped at the search "
                  r"ceiling $\delta=10$", fontsize=10)
    ax1.legend(loc="lower right", fontsize=8)
    ax1.text(0.985, 0.985,
             "banked Type-I object carries " r"$\alpha=1$" ":  window EMPTY\n"
             "30/30 rows obey  admissible " r"$\Leftrightarrow$ " r"$\alpha_{\rm centre}>$ "
             "threshold  (0 exceptions)",
             transform=ax1.transAxes, ha="right", va="top", fontsize=8, color=C_EMPTY)

    fig.suptitle("Route-DTOL (leg 386): the pre-registered tolerance mode, and the tolerance "
                 "§4 can actually afford — CEILING TIER 2, Clay ~0.05%", fontsize=10.5)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    dest = FIGS / "fig99_route_dtol_v1_delta_window.png"
    fig.savefig(dest)
    print(f"wrote {dest.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
