#!/usr/bin/env python3
"""Rebuild fig104 for Route-CLOC (leg 381) from the curated JSON alone.

Reads writeup/data/p2_route_cloc_v1.json and re-runs NOTHING -- no quadrature, no
field evaluation, no fit. Every value plotted is a value leg 381's runner banked.
This script is a DOCS-lane closure of leg 381's missing-figure audit finding; it
makes no new claim and it does not call experiments/p2_route_cloc_v1.py.

    .venv/bin/python experiments/p2_route_cloc_v1_evidence.py

FIGURE NUMBER: **fig104**, allocated to this closure and free at allocation time.
NOT fig99: fig99 was freed by leg 381's omission and has since been re-allocated to
leg 386. Figure-number collisions have cost this repository time eight times, so the
number is stated plainly here and registered in writeup/build_figures.py's
P2_EVIDENCE list.

NOT PLOTTED, because it is not banked: leg 381's check_B banks only summary scalars
for the SS/DSS exponent comparison (the exponents, the naive-fit bias, the G
oscillation amplitude, the residual period). The per-sample energy series E(s) and
the modulating factor G(s) themselves are NOT in the JSON, so panel C shows the
banked scalars and cannot show a modulated-vs-unmodulated fit drawn through data
points. Drawing that overlay would require re-running the runner, which is out of
scope for this script by construction.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "writeup" / "data" / "p2_route_cloc_v1.json"
FIGS = ROOT / "writeup" / "figures"
FIGS.mkdir(parents=True, exist_ok=True)

# House style, matched to writeup/build_figures.py.
plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130, "font.size": 9.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "axes.axisbelow": True,
    "legend.frameon": False,
})
C_BAD, C_OK1, C_OK2, C_OK3, C_OK4, C_REF = (
    "#dc2626", "#2563eb", "#0891b2", "#7c3aed", "#059669", "#6b7280")


def main() -> int:
    d = json.loads(DATA.read_text())
    cA1 = d["check_C_cutoff_magnitudes"]["by_alpha"]["alpha=1.0"]
    rows = cA1["rows"]
    meas = cA1["measured_rho_exponents"]
    c2 = d["check_C2_critical_L3_tail_is_log_divergent_at_alpha_1"]
    cb = d["check_B_energy_exponent_SS_vs_DSS"]

    fig, (axA, axB, axC) = plt.subplots(1, 3, figsize=(16.2, 5.0))

    # ---- PANEL A: the cutoff bill -- everything shrinks except the critical tail ----
    rho = np.array([r["rho"] for r in rows], dtype=float)
    series = [
        ("nonlinear residual  ‖(u·∇χ)u‖_{L²}", "nonlinear_residual_L2", C_OK1, "o"),
        ("viscous residual  ‖ν(2∇χ·∇u+(Δχ)u)‖_{L²}", "viscous_residual_L2", C_OK2, "s"),
        ("divergence defect  ‖∇χ·u‖_{L²}", "divergence_defect_L2", C_OK3, "^"),
        ("pressure perturbation at origin  |δp(0)|", "pressure_perturbation_at_origin",
         C_OK4, "D"),
        ("discarded tail, critical  ‖u‖_{L³(|x|>ρ)}", "tail_L3_norm", C_BAD, "v"),
    ]
    for label, key, col, mk in series:
        y = np.array([r[key] for r in rows], dtype=float)
        axA.loglog(rho, y, marker=mk, ms=5, lw=1.4, color=col,
                   label=f"{label}   ρ^{{{meas[key]:+.4f}}}")
    axA.set_xlabel("cutoff radius  ρ   (similarity-variable units, ν = 1)")
    axA.set_ylabel("magnitude of the term   (norm units as labelled)")
    axA.set_title("A. the cutoff bill at the banked Type-I exponent α = 1\n"
                  "four terms shrink with ρ; the critical L³ tail does not move",
                  fontsize=9.5)
    axA.legend(loc="lower left", fontsize=7.2)
    axA.set_ylim(top=2e2)
    axA.annotate(
        f"L³ tail flat: {rows[0]['tail_L3_norm']:.4f} → {rows[-1]['tail_L3_norm']:.4f}\n"
        f"over ρ = {rho[0]:g} → {rho[-1]:g}  (exponent {meas['tail_L3_norm']:.2e})",
        xy=(0.30, 0.90), xycoords="axes fraction", fontsize=7.6, color=C_BAD)

    # ---- PANEL B: the term that never gets cheap, on its own axes ----
    dec = np.array([r["decades_of_window"] for r in c2["rows"]], dtype=float)
    cube = np.array([r["tail_L3_cubed"] for r in c2["rows"]], dtype=float)
    axB.plot(dec, cube, "o-", color=C_BAD, ms=6, lw=1.6, zorder=3,
             label="banked  ‖u‖³_{L³} of the discarded tail")
    inc = c2["increment_per_decade"]
    slope = float(np.mean(inc))
    axB.plot(dec, cube[0] + slope * (dec - dec[0]), "--", color=C_REF, lw=1.2,
             label=f"straight line, slope {slope:.3f} per decade")
    for x, y in zip(dec, cube):
        axB.annotate(f"{y:.1f}", (x, y), textcoords="offset points",
                     xytext=(0, -13), ha="center", fontsize=7.6)
    axB.set_xlabel("decades of window included beyond the cutoff  (log₁₀ ρ_outer/ρ)")
    axB.set_ylabel("‖u‖³_{L³} of the discarded far field   (dimensionless)")
    axB.set_xticks(dec)
    axB.set_ylim(bottom=float(cube[0]) - 300.0)
    axB.set_title("B. no cutoff radius makes this one go away\n"
                  f"+{slope:.3f} per decade, constant to "
                  f"{c2['increment_per_decade_spread']:.1e} across "
                  f"{len(inc)} increments", fontsize=9.5)
    axB.legend(loc="upper left", fontsize=8)
    axB.annotate("log-divergent at α = 1: linear growth here means\n"
                 "unbounded growth in the window, never small",
                 xy=(0.42, 0.09), xycoords="axes fraction", fontsize=7.8, color=C_REF)

    # ---- PANEL C: the DSS exponent is the SS exponent; dropping G is what costs ----
    pred = cb["predicted_exponent"]
    bars = [
        ("SS\n(pure power law)", cb["SS_exponent"], C_OK1),
        ("DSS, modulation\nHANDLED", cb["DSS_exponent"], C_OK2),
        ("DSS, modulation\nDROPPED (naive)",
         cb["DSS_exponent_naive_fit_modulation_DROPPED"], C_BAD),
    ]
    xs = np.arange(len(bars))
    devs = [abs(v - pred) for _, v, _ in bars]
    # Floor the exactly-zero SS deviation onto the symlog linear region so the bar
    # is visible as a bar; its true value is printed on the figure beside it.
    axC.bar(xs, [max(v, 1e-17) for v in devs], color=[c for _, _, c in bars],
            width=0.55, zorder=3)
    axC.set_yscale("symlog", linthresh=1e-16)
    axC.axhline(0.0, color="black", lw=0.8)
    axC.set_xticks(xs)
    axC.set_xticklabels([b[0] for b in bars], fontsize=8.2)
    axC.set_ylabel("|fitted exponent − 1/2|   (dimensionless, symlog)")
    for x, (lab, val, _), dv in zip(xs, bars, devs):
        axC.annotate(f"{val:.9f}\n|dev| {dv:.2e}", (x, max(dv, 1e-17)),
                     textcoords="offset points", xytext=(0, 7), ha="center",
                     fontsize=7.8)
    axC.set_title("C. the DSS exponent equals the SS exponent; the cost is in\n"
                  "dropping the log-periodic modulation, not in the exponent",
                  fontsize=9.5)
    axC.set_ylim(0, 1.0)
    axC.annotate(
        f"DSS/SS ratio {cb['DSS_over_SS_exponent_ratio']:.10f} — no factor\n"
        f"G(s) swings {cb['DSS_G_oscillation_relative_amplitude']:.2f}× within one period\n"
        f"dropping G → {cb['DSS_exponent_naive_fit_modulation_DROPPED']:.4f}, "
        f"{cb['naive_fit_bias_percent']:.2f}% off\n"
        f"residual period {cb['DSS_residual_best_fit_period_in_s']:.4f} in s vs\n"
        f"   predicted 2 log λ = {cb['predicted_period_2_log_lambda']:.4f} "
        f"({100 * cb['period_relative_error']:.2f}%)\n"
        f"period-locked fit max log residual "
        f"{cb['modulation_handled_fit_max_log_residual']:.2e}  (α = {cb['alpha_used']:g})",
        xy=(0.02, 0.73), xycoords="axes fraction", fontsize=7.0, color=C_REF)

    fig.suptitle(
        "fig104 — Route-CLOC (leg 381): CLAY_OBLIGATIONS.md §4 verified AS A "
        f"SPECIFICATION.   GATE: {d['gate']['answer']}\n"
        "The cutoff bill is cheap on every term except the critical L³ tail, and that "
        "one never gets cheap.   "
        "CEILING: TIER 2 — no L1 → L4 link moved, Clay stays ~0.05%.", fontsize=9.5)
    fig.text(0.012, 0.012,
             "Every number is read from writeup/data/p2_route_cloc_v1.json; nothing is "
             "recomputed. Panel C shows leg 381's banked SCALARS: the per-sample energy series "
             "E(s) and the modulating\nfactor G(s) are not banked, so no fit-through-data "
             "overlay is drawn. Verification of a specification is not a certificate, an "
             "enclosure, or a localisation.",
             fontsize=7.4, color=C_REF)
    # The α = 1 coincidence, said on the figure rather than left to prose. It lives in
    # the caption margin because panel A has no gap wide enough to hold it legibly.
    fig.text(0.64, 0.012,
             "Panel A, the α = 1 coincidence: the nonlinear "
             f"({meas['nonlinear_residual_L2']:.4f}) and viscous "
             f"({meas['viscous_residual_L2']:.4f})\ncutoff residuals scale identically at "
             "exactly the Type-I exponent, both ρ^{−3/2}.",
             fontsize=7.4, color=C_REF)
    fig.tight_layout(rect=(0, 0.065, 1, 0.90))
    out = FIGS / "fig104_route_cloc_v1.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"wrote {out}")

    # Re-state the load-bearing numbers from the JSON, so this script is also a
    # claims check and not only a plotter.
    print(f"  gate answer (from JSON): {d['gate']['answer']}")
    print(f"  ceiling: {d['ceiling']}")
    print(f"  clay movement: {d['gate']['clay_movement']}")
    print("  panel A, measured rho-exponents at alpha=1: "
          f"nonlinear {meas['nonlinear_residual_L2']:.4f}, "
          f"viscous {meas['viscous_residual_L2']:.4f}, "
          f"divergence {meas['divergence_defect_L2']:.4f}, "
          f"pressure at origin {meas['pressure_perturbation_at_origin']:.4f}, "
          f"critical L3 tail {meas['tail_L3_norm']:.3e}")
    print(f"  panel B, L^3-cubed increment per decade {slope:.5f}, "
          f"spread {c2['increment_per_decade_spread']:.3e} over {len(inc)} increments")
    print(f"  panel C, SS {cb['SS_exponent']!r}, DSS {cb['DSS_exponent']!r}, "
          f"ratio {cb['DSS_over_SS_exponent_ratio']!r}; naive "
          f"{cb['DSS_exponent_naive_fit_modulation_DROPPED']:.10f} "
          f"({cb['naive_fit_bias_percent']:.4f}% off), G swing "
          f"{cb['DSS_G_oscillation_relative_amplitude']:.4f}x")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
