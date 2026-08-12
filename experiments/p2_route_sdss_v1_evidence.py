#!/usr/bin/env python3
"""Rebuild fig76 for Route-SDSS (leg 313) from the curated JSON alone.

Reads writeup/data/p2_route_sdss_v1.json and re-runs NOTHING -- no quadrature, no
Chebyshev transform, no ban read.  Every value plotted is a value the runner banked.

    .venv/bin/python experiments/p2_route_sdss_v1_evidence.py

FIGURE NUMBER: **fig76**.  Numbers up to and including fig75 were taken or reserved at
dispatch (69 -> leg 302, 70 -> leg 311, 71 -> leg 303, 72 -> leg 320, 73 -> leg 312,
74 -> leg 316, 75 -> leg 301), and this leg was instructed to take fig76 and say so
plainly.  It is registered in writeup/build_figures.py's P2_EVIDENCE list.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "writeup" / "data" / "p2_route_sdss_v1.json"
FIGS = ROOT / "writeup" / "figures"
FIGS.mkdir(parents=True, exist_ok=True)

# House style, matched to writeup/build_figures.py.
plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130, "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "axes.axisbelow": True,
    "legend.frameon": False,
})
C_DIV, C_FIN, C_LIT, C_CTRL = "#dc2626", "#059669", "#6b7280", "#2563eb"


def main() -> int:
    d = json.loads(DATA.read_text())
    s2 = d["s2_function_space"]
    s3 = d["s3_regularity_of_the_far_field_block"]

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.2, 4.5))

    # ---------------- LEFT: the same object, three verdicts ----------------
    rows = s2["weighted_L2_rows"]
    ss = sorted(float(k.split("=")[1]) for k in rows)
    ratios = [rows[f"s={s}"]["shell_ratio"] for s in ss]
    fin = [rows[f"s={s}"]["finite"] for s in ss]

    axL.axhline(1.0, color=C_LIT, lw=1.2, ls="--")
    axL.text(2.55, 1.02, "divergence threshold", color=C_LIT, fontsize=8, ha="right")
    axL.plot(ss, ratios, "-", color=C_LIT, lw=1.0, zorder=1)
    axL.scatter([s for s, f in zip(ss, fin) if not f],
                [r for r, f in zip(ratios, fin) if not f],
                s=46, color=C_DIV, zorder=3, label="norm DIVERGES")
    axL.scatter([s for s, f in zip(ss, fin) if f],
                [r for r, f in zip(ratios, fin) if f],
                s=46, color=C_FIN, zorder=3, label="norm FINITE")

    # The unweighted L^2 point IS the s = 0 row; annotate it as leg 260's obstruction.
    axL.annotate(
        "unweighted $L^2$ (s=0):\n"
        f"ratio {s2['unweighted_L2_shell_ratio']:.4f}\n"
        "leg 260 §3.4 reason 2\n"
        "'infinite energy in the\nsimilarity variable'",
        xy=(0.0, ratios[0]), xytext=(0.16, 1.90), fontsize=8, color=C_DIV, va="top",
        arrowprops=dict(arrowstyle="->", color=C_DIV, lw=1.0))
    axL.annotate(
        "leg 260's OWN answer (a):\nweighted $L^2$, s>1 — finite",
        xy=(1.5, rows["s=1.5"]["shell_ratio"]), xytext=(1.15, 1.30), fontsize=8,
        color=C_FIN, arrowprops=dict(arrowstyle="->", color=C_FIN, lw=1.0))

    axL.set_xlabel("weight exponent $s$   in   $\\rho=(1+|y|)^{-s}$")
    axL.set_ylabel("shell ratio  $\\int_R^{2R}\\,/\\,\\int_{R/2}^{R}$")
    axL.set_title("(a) THE SAME OBJECT, THREE VERDICTS\n"
                  "Type-I profile $|U|\\leq C/(1+|y|)$ on $\\mathbb{R}^3$", fontsize=9.5)
    axL.set_ylim(0.0, 2.15)
    axL.legend(loc="upper right", fontsize=8)
    axL.text(0.0, -0.30,
             "compactified $X=|y|/(1+|y|)$:  the profile is the exact linear zero "
             f"$(1-X)$, with $\\|U\\|_{{L^2(dX)}}=\\sqrt{{1/3}}="
             f"{s2['compactified_L2_dX_norm']:.6f}$  —  FINITE.\n"
             "That is the discretisation the one demonstrated seeded method actually "
             "uses (Hou arXiv:2405.10916).",
             transform=axL.transAxes, fontsize=7.8, color=C_FIN, va="top")

    # ---------------- RIGHT: the defect that survives ----------------
    kr = s3["rows"]
    kk = sorted(float(k.split("=")[1]) for k in kr if float(k.split("=")[1]) > 0)
    n6 = [kr[f"kappa={k}"]["modes_for_rel_trunc_1e-6"] for k in kk]

    axR.loglog(kk, n6, "o-", color=C_DIV, lw=1.6, ms=6,
               label="$(1-X)^{1-i\\kappa}$: ALGEBRAIC, "
                     f"fitted rate $p={kr['kappa=1.0']['fitted_algebraic_rate_p']:.3f}$")
    C = s3["cost_scaling_prefactor_C"]
    q = s3["cost_scaling_exponent_q"]
    axR.loglog(kk, [C * k ** q for k in kk], "--", color=C_LIT, lw=1.0,
               label=f"fit  $n\\approx{C:.0f}\\,\\kappa^{{{q:.3f}}}$")
    ctrl6 = s3["positive_control_smooth_modes_to_1e-6"]
    axR.axhline(ctrl6, color=C_CTRL, lw=1.4, ls=":")
    axR.set_ylim(5.0, 3.0e5)
    axR.text(1.05, ctrl6 * 1.22, f"smooth control:  n={ctrl6}  —  GEOMETRIC",
             color=C_CTRL, fontsize=8)

    axR.set_xlabel("log-periodic frequency  $\\kappa$")
    axR.set_ylabel("Chebyshev modes for $10^{-6}$ relative truncation")
    axR.set_title("(b) THE DEFECT THAT SURVIVES SEEDING\n"
                  "far-field block $r^{-1+i\\kappa}\\;\\mapsto\\;(1-X)^{1-i\\kappa}$"
                  "  =  clause (a)'s $X^{1-iy}$", fontsize=9.5)
    axR.legend(loc="lower right", fontsize=8, bbox_to_anchor=(1.0, 0.12))
    axR.text(0.03, 0.985,
             "the compactification that makes the norm finite\n"
             "carries the far field to the SAME functional form as\n"
             "§26/§4.1's recorded gCLM difficulty — at the other end.\n"
             "Seeding dissolves all four of leg 260 §3.4's reasons.\n"
             "It does not dissolve this: it is not about the seed.",
             transform=axR.transAxes, fontsize=7.6, va="top", color="#111827")

    fig.suptitle("fig76 — Route-SDSS (leg 313): leg 260's substantive obstruction is "
                 "realization-scoped; the regularity defect is not",
                 fontsize=10.5, y=1.005)
    fig.tight_layout()
    out = FIGS / "fig76_route_sdss_v1.png"
    fig.savefig(out, bbox_inches="tight")
    print(f"fig76_route_sdss_v1.png -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
