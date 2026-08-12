#!/usr/bin/env python3
"""Rebuild fig106 for Route-DTOR (leg 390) from the curated JSON alone.

Reads writeup/data/p2_route_dtor_v1.json and re-runs NOTHING -- no lattice sums,
no field evaluation, no fit, no bisection. Every value plotted is a value leg
390's runner banked. This script does not import or call
experiments/p2_route_dtor_v1.py.

    .venv/bin/python experiments/p2_route_dtor_v1_evidence.py

FIGURE NUMBER: **fig106**, allocated to this leg at dispatch and free at
allocation time (fig97/98 -> PROG-R4, fig99 -> leg 386, fig100 -> leg 382,
fig101/104 -> DOCS units, fig102 -> leg 383, fig103 -> leg 385, fig105 -> leg
384). Eight figure-number collisions have cost this repository time, so the
number is stated plainly here and registered in writeup/build_figures.py.

THE FIGURE MAKES NO RECOMMENDATION. It shows two bills in one currency and a
screen tally. THE RETARGET DECISION IS THE USER'S AND LEG 390 MAKES NONE.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "writeup" / "data" / "p2_route_dtor_v1.json"
FIGS = ROOT / "writeup" / "figures"
FIGS.mkdir(parents=True, exist_ok=True)

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
    C = d["check_C_periodization_bill"]
    D = d["check_D_cut_then_periodize"]
    E = d["check_E_section_2_four_rows"]
    bill = C["THE_BILL"]

    fig, (axA, axB, axC) = plt.subplots(1, 3, figsize=(16.4, 5.1))

    # ---- panel A: the image-sum exponent, and where the threshold sits -----
    a = np.array([r["alpha"] for r in C["rows"]])
    meas = np.array([r["measured_increment_exponent_in_R"] for r in C["rows"]])
    pred = np.array([r["predicted_increment_exponent_3_minus_alpha"] for r in C["rows"]])
    axA.plot(a, pred, "-", color=C_REF, lw=1.4, label="predicted  3 − α")
    axA.plot(a, meas, "o", color=C_OK1, ms=6,
             label="measured shell-increment exponent")
    axA.axhline(0.0, color="k", lw=0.8)
    acrit = bill["alpha_required_for_periodization_to_converge"]
    axA.axvline(acrit, color=C_BAD, lw=1.6, ls="--",
                label=f"periodization threshold α = {acrit:.4f}")
    axA.axvline(bill["alpha_required_by_section_4_bounded_energy_L2"], color=C_OK4,
                lw=1.4, ls=":", label="§4 bounded-energy threshold α = 1.5")
    axA.axvline(bill["alpha_available_a_priori_Type_I_Chae_Wolf"], color=C_OK3,
                lw=1.4, ls="-.", label="available a priori (Type-I) α = 1.0")
    axA.set_xlabel("profile far-field decay exponent α")
    axA.set_ylabel("growth exponent of the image sum in R")
    axA.set_title("A. Wrapping the uncut profile: $\\sum_k |Lk|^{-\\alpha}$\n"
                  "converges only above α ≈ 3", fontsize=10)
    axA.legend(fontsize=7.6, loc="lower left")
    worst = max(r["abs_error"] for r in C["rows"])
    axA.text(0.40, 0.94, f"worst |measured − predicted| = {worst:.5f}",
             transform=axA.transAxes, fontsize=7.6, color=C_REF)

    # ---- panel B: the two bills side by side, same currency ---------------
    labels = ["§4\nbounded energy\n(leg 381)", "periodization\n(this leg)"]
    deficits = [bill["deficit_section_4"], bill["deficit_periodization"]]
    bars = axB.bar(labels, deficits, color=[C_OK4, C_BAD], width=0.55)
    for b, v in zip(bars, deficits):
        axB.text(b.get_x() + b.get_width() / 2, v + 0.05, f"{v:.4f}",
                 ha="center", fontsize=10)
    axB.set_ylabel("deficit in the decay exponent α  (required − available)")
    axB.set_ylim(0, max(deficits) * 1.9)
    axB.set_title("B. Both bills in one currency:\n"
                  f"repurchase factor {bill['REPURCHASE_FACTOR_IN_DEFICIT']:.4f}× in deficit",
                  fontsize=10)
    axB.text(0.03, 0.86,
             f"required: {bill['alpha_required_by_section_4_bounded_energy_L2']} vs "
             f"{bill['alpha_required_for_periodization_to_converge']:.4f}\n"
             f"available (both): {bill['alpha_available_a_priori_Type_I_Chae_Wolf']}\n"
             f"ratio: {bill['ratio_section_4_required_over_available']:.4f} vs "
             f"{bill['ratio_periodization_required_over_available']:.4f}",
             transform=axB.transAxes, ha="left", fontsize=8.4, color=C_REF)
    incr = C["alpha_3_is_the_logarithmic_boundary"]["increment_per_doubling_of_R"]
    axB.text(0.03, 0.66, "at α = 3 exactly: log-divergent,\n"
                        f"increment per doubling {incr[-1]:.4f}, spread "
                        f"{C['alpha_3_is_the_logarithmic_boundary']['increment_spread']:.4f}",
             transform=axB.transAxes, ha="left", fontsize=8.0, color=C_REF)

    # ---- panel C: §2's screen tally, and what the cut route inherits ------
    axC.axis("off")
    rows = E["rows"]
    y = 0.95
    axC.text(0.0, y, "C. §2's four screen rows, machine-read", fontsize=10.5,
             weight="bold", transform=axC.transAxes)
    y -= 0.09
    for r in rows:
        col = C_BAD if r["combined_verdict"] == "R3-ONLY" else C_OK4
        axC.text(0.0, y, "• " + r["row"], fontsize=8.6, transform=axC.transAxes)
        axC.text(0.0, y - 0.042, f"    {r['combined_verdict']}   "
                 f"(marker {r['marker_verdict']}, ansatz {r['ansatz_class_verdict']})",
                 fontsize=7.9, color=col, transform=axC.transAxes)
        axC.text(0.0, y - 0.079, f"    record: {r['landed_record'].split(' (')[0]}",
                 fontsize=7.0, color=C_REF, transform=axC.transAxes)
        y -= 0.130
    t = E["tally"]
    axC.text(0.0, y, f"tally: {t['R3_ONLY']} of {t['rows_total']} R³-only, "
                     f"{t['CARRIES_TO_T3']} clearances carry to T³",
             fontsize=9.4, weight="bold", color=C_BAD, transform=axC.transAxes)
    y -= 0.075
    inh = D["inherited_cutoff_bill_from_leg_381"]
    axC.text(0.0, y, "cut-then-wrap inherits leg 381's bill unchanged:",
             fontsize=8.6, transform=axC.transAxes)
    axC.text(0.0, y - 0.042,
             f"    critical L³ tail {inh['critical_L3_tail_increment_per_decade']:.3f} per decade "
             f"(spread {inh['critical_L3_tail_increment_spread']:.1e})",
             fontsize=7.9, color=C_REF, transform=axC.transAxes)
    mp = D["image_pressure_interaction_leading_multipole"]
    axC.text(0.0, y - 0.084,
             f"    image pressure: signed sum cancels to "
             f"{mp['cumulative_signed_tensor_max_abs_at_N_32']:.2e} (cubic lattice)",
             fontsize=7.9, color=C_OK4, transform=axC.transAxes)
    axC.text(0.0, y - 0.126,
             f"    direct image contamination at L > 2ρ: "
             f"{D['image_overlap_of_the_cut_field']['rows'][0]['sup_image_velocity_contamination_in_the_cell']:.1f}",
             fontsize=7.9, color=C_OK4, transform=axC.transAxes)
    axC.text(0.0, y - 0.245, "THE RETARGET DECISION IS THE USER'S.\nLeg 390 makes none.",
             fontsize=8.6, weight="bold", color="k", transform=axC.transAxes)

    fig.suptitle("Leg 390 Route-DTOR — Fefferman statement (D) on the torus: what it deletes, "
                 "and what periodization charges back. CEILING TIER 2; Clay ~0.05%.",
                 fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    out = FIGS / "fig106_route_dtor_v1.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
