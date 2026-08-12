#!/usr/bin/env python3
"""Rebuild fig105 for Route-COBV (leg 384) from the curated JSON alone.

Reads writeup/data/p2_route_cobv_v1.json and re-runs NOTHING -- no document parse, no
ledger execution, no network fetch of the Clay prize rules.  Every value drawn and
every claim asserted below is a value the runner banked.

    .venv/bin/python experiments/p2_route_cobv_v1_evidence.py

FIGURE NUMBER: **fig105**.  Leg 384 was allocated fig105 at dispatch and no other
number (fig97/98 -> PROG-R4, fig99 -> leg 386, fig100 -> leg 382, fig101 -> leg 233,
fig102 -> leg 383, fig103 -> leg 385, fig104 -> a DOCS unit).  Eight figure-number
collisions have already cost this repository time, so the number is stated here
plainly and registered in writeup/build_figures.py's P2_EVIDENCE list.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "writeup" / "data" / "p2_route_cobv_v1.json"
FIGS = ROOT / "writeup" / "figures"
FIGS.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130, "font.size": 9.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "axes.axisbelow": True,
    "legend.frameon": False,
})
C_MATCH, C_MISMATCH, C_UNVER, C_REF = "#059669", "#dc2626", "#d97706", "#6b7280"
C_DOC, C_REC = "#2563eb", "#111827"


def main() -> int:
    d = json.loads(DATA.read_text(encoding="utf-8"))
    checks = d["checks"]
    counts = d["counts"]
    ctrl = d["instrument_control"]

    # ---------------------------------------------------------------- assertions
    # Rebuilt from the JSON, not recomputed from sources: the prose in
    # BLOG_/TECHNICAL_P2_ROUTECOBV_V1.md quotes exactly these numbers.
    assert d["leg"] == 384 and d["route"] == "COBV"
    assert d["checks_run"] == len(checks) == 23, len(checks)
    recount = {"MATCH": 0, "MISMATCH": 0, "UNVERIFIED": 0}
    for c in checks:
        recount[c["verdict"]] += 1
    assert recount == counts, (recount, counts)
    assert counts == {"MATCH": 17, "MISMATCH": 6, "UNVERIFIED": 0}, counts
    assert ctrl["controls_run"] == 23 and ctrl["controls_fired"] == 23
    assert ctrl["controls_failed"] == []
    assert len(ctrl["corrupt_plants"]) + len(ctrl["repair_plants"]) == 23
    assert d["gate"]["answer"] == "YES"
    assert d["gate"]["unverifiable_clauses"] == []
    assert d["clay_rules_fetch"]["reachable"] is True
    assert d["clay_rules_fetch"]["http_status"] == 200
    assert d["ceiling"].startswith("TIER 2")
    assert "~0.05%" in d["gate"]["clay_movement"]

    by_id = {c["id"]: c for c in checks}
    mismatches = [c["id"] for c in checks if c["verdict"] == "MISMATCH"]
    assert mismatches == ["I8", "I10", "I15", "III1", "III3", "III4"], mismatches

    i8 = by_id["I8"]
    assert i8["doc_literal"] == "2.6e-5"
    assert abs(i8["record_max_abs_error"] - 0.0256893924479335) < 1e-15
    assert abs(i8["ratio_max_over_doc"] - 988.05355568975) < 1e-6
    assert abs(i8["record_row_at_alpha_1"]["abs_error"] - 0.000264923221459137) < 1e-15

    i10 = by_id["I10"]
    cubed = i10["record_tail_L3_cubed"]
    norms = i10["record_tail_L3_norm"]
    inc = i10["record_increment_per_decade"]
    assert len(cubed) == len(norms) == 5 and len(inc) == 4
    assert abs(inc[0] - 326.87521405120924) < 1e-9
    assert abs(norms[0] - 8.678998071314405) < 1e-12
    assert abs(norms[-1] - 14.840907203374448) < 1e-12

    ii2 = by_id["II2"]
    assert abs(ii2["record_value_lambda_ceiling"] - 1.6487212707001282) < 1e-15
    assert abs(ii2["record_value_lambda_ceiling"] - ii2["exp_half"]) < 1e-15
    assert ii2["executed_verdict"].startswith("OUTSIDE")
    assert by_id["II1"]["executed_ledger_verdict"] == "NOT-REACHED-BY-ANSATZ"
    assert by_id["II3"]["record_theorem_count"] == 4
    assert by_id["II4"]["record_classification"] == "WIDENS"
    assert by_id["II4"]["executed_verdict"] == "NOT-REACHED-BY-ANSATZ"
    assert by_id["I3"]["doc_counts"] == {"confirmed": 4, "corrected": 1, "refuted": 1}
    assert by_id["I3"]["recomputed_from_ledger_rows"] == by_id["I3"]["doc_counts"]
    assert by_id["I1"]["doc_occurrences"] == 0

    # ---------------------------------------------------------------- the figure
    fig = plt.figure(figsize=(15.0, 5.4))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.35, 1.0, 1.0], wspace=0.34)
    axA = fig.add_subplot(gs[0, 0])
    axB = fig.add_subplot(gs[0, 1])
    axC = fig.add_subplot(gs[0, 2])

    # PANEL A -- the 23-row board, with the planted control alongside each verdict.
    ys = np.arange(len(checks))[::-1]
    for y, c in zip(ys, checks):
        col = {"MATCH": C_MATCH, "MISMATCH": C_MISMATCH,
               "UNVERIFIED": C_UNVER}[c["verdict"]]
        axA.barh(y, 1.0, height=0.62, color=col, alpha=0.85)
        k = c["control"]["plant_kind"]
        axA.plot(1.28, y, marker=("v" if k == "corrupt" else "^"), ms=6,
                 color=(C_MISMATCH if k == "corrupt" else C_MATCH), mec="white", mew=0.6)
    axA.set_yticks(ys)
    axA.set_yticklabels(["%-4s %s" % (c["id"], c["item"]) for c in checks], fontsize=7.6,
                        family="monospace")
    axA.set_xlim(0, 1.55)
    axA.set_xticks([])
    axA.set_ylim(-1.6, len(checks) - 0.3)
    axA.set_title("A. 23 clauses checked mechanically\n"
                  "%d MATCH / %d MISMATCH / %d UNVERIFIED"
                  % (counts["MATCH"], counts["MISMATCH"], counts["UNVERIFIED"]),
                  fontsize=10)
    axA.grid(False)
    axA.text(0.0, -1.25,
             "green MATCH   red MISMATCH        planted control:  "
             "$\\bf{v}$ corrupt   $\\bf{\\wedge}$ repair  —  23/23 fired",
             ha="left", va="center", fontsize=7.4, color=C_REF)

    # PANEL B -- finding I8: the quoted tolerance against the four banked rows.
    rows = i8["rows"]
    alphas = [r["alpha"] for r in rows]
    errs = [r["abs_error"] for r in rows]
    axB.semilogy(alphas, errs, "o-", color=C_REC, ms=7, label="banked abs_error per row")
    axB.axhline(i8["doc_literal_value"], color=C_DOC, ls="--",
                label="document: 'verified to 2.6e-5'")
    axB.axhline(i8["record_max_abs_error"], color=C_MISMATCH, ls=":",
                label="JSON max_abs_error = 2.569e-2")
    axB.set_xlim(0.74, 1.60)
    axB.set_ylim(1.2e-5, 2.5e-1)
    axB.annotate("", xy=(1.50, i8["record_max_abs_error"]), xytext=(1.50, i8["doc_literal_value"]),
                 arrowprops=dict(arrowstyle="<->", color=C_MISMATCH, lw=1.3))
    axB.text(1.47, 6e-4, "988x", color=C_MISMATCH, fontsize=10.5, ha="right", weight="bold")
    axB.axvline(1.0, color=C_REF, lw=0.9, alpha=0.7)
    axB.text(1.02, 1.7e-5, r"$\alpha=1$: the case §4 is about", fontsize=7.4, color=C_REF)
    axB.set_xlabel(r"$\alpha$ (far-field decay exponent)")
    axB.set_ylabel("|measured - predicted| fixed-ball exponent")
    axB.set_title("B. I8 MISMATCH: the quoted tolerance is\nthe best row, not the "
                  "verification tolerance", fontsize=10)
    axB.legend(fontsize=7.4, loc="upper left")

    # PANEL C -- finding I10: 326.875 is the increment of the CUBE, not of the norm.
    dec = [2, 4, 6, 8, 10]
    axC.plot(dec, cubed, "s-", color=C_MISMATCH, ms=6,
             label=r"$\|\cdot\|_{L^3}^3$ tail (JSON tail_L3_cubed)")
    axC.set_xlabel("decades of window")
    axC.set_ylabel(r"cube of the critical tail", color=C_MISMATCH)
    axC.tick_params(axis="y", labelcolor=C_MISMATCH)
    axC.set_title("C. I10 MISMATCH: 326.875/decade is the\nincrement of the CUBE, "
                  "not of the norm", fontsize=10)
    ax2 = axC.twinx()
    ax2.plot(dec, norms, "o--", color=C_DOC, ms=6,
             label=r"$\|\cdot\|_{L^3}$ tail (JSON tail_L3_norm)")
    ax2.set_ylabel(r"the $L^3$ norm itself", color=C_DOC)
    ax2.tick_params(axis="y", labelcolor=C_DOC)
    ax2.grid(False)
    ax2.spines["top"].set_visible(False)
    axC.set_ylim(300, 4100)
    axC.text(6.3, 1050,
             "the document's number:\n%.3f per decade\n(spread 7.4e-10)" % inc[0],
             fontsize=7.6, color=C_MISMATCH)
    ax2.text(2.15, 11.6, "the norm itself:\n%.3f $\\rightarrow$ %.3f"
             % (norms[0], norms[-1]), fontsize=7.6, color=C_DOC)
    h1, l1 = axC.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    axC.legend(h1 + h2, l1 + l2, fontsize=7.4, loc="upper left",
               bbox_to_anchor=(0.0, 0.88))

    fig.suptitle("fig105 — leg 384 Route-COBV: CLAY_OBLIGATIONS.md checked against "
                 "leg 381's banked verdicts, §2's landed records, and the Clay "
                 "Institute's own prize rules (HTTP 200). CEILING TIER 2; Clay "
                 "stays ~0.05%.", fontsize=9.2, y=1.005)

    dest = FIGS / "fig105_route_cobv_v1.png"
    fig.savefig(dest, bbox_inches="tight")
    plt.close(fig)

    print("leg 384 Route-COBV evidence (rebuilt from JSON, nothing re-run)")
    print("  checks               %d" % d["checks_run"])
    print("  MATCH/MISMATCH/UNVER %(MATCH)d / %(MISMATCH)d / %(UNVERIFIED)d" % counts)
    print("  controls             %d run, %d fired, failed: %s"
          % (ctrl["controls_run"], ctrl["controls_fired"], ctrl["controls_failed"]))
    print("  clay rules           HTTP %s, reachable=%s"
          % (d["clay_rules_fetch"]["http_status"], d["clay_rules_fetch"]["reachable"]))
    print("  mismatches           %s" % ", ".join(mismatches))
    print("  GATE ANSWERS         %s" % d["gate"]["answer"])
    print("  wrote %s" % dest.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
