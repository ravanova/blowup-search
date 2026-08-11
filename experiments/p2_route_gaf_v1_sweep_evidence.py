"""Route-GAF v1 (leg 303) — EVIDENCE: every number the BLOG and TECHNICAL write-ups quote,
re-derived from `writeup/data/p2_route_gaf_v1_sweep.json`. Also builds
`writeup/figures/fig68_route_gaf_v1_cell.png`.

Nothing is re-queried: this reads the curated JSON and asserts the relations the prose
asserts, so a reader can check the prose without going back to arXiv.

    .venv/bin/python experiments/p2_route_gaf_v1_sweep_evidence.py
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "writeup", "data")
FIG = os.path.join(ROOT, "writeup", "figures", "fig68_route_gaf_v1_cell.png")

THE_HIT = "2604.09949"

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-66s %s" % ("ok" if ok else "FAIL", name, detail))


def main():
    with open(os.path.join(D, "p2_route_gaf_v1_sweep.json")) as fh:
        s = json.load(fh)

    cov, cell, c1 = s["coverage"], s["cell_state"], s["c1_replication"]

    # ---- (1) the pre-registration is intact --------------------------------
    check("(1) the four-clause hit rule was committed before the first query",
          s["hit_rule"]["committed_in"].startswith("writeup/novelty/leg_303.md")
          and s["hit_rule"]["all_four_required"] is True,
          s["hit_rule"]["committed_in"])

    # ---- (2) coverage: the sweep is a strict superset of leg 174's net -----
    check("(2) 35 queries over 5 channels, all reached, none reported as a zero",
          cov["n_queries_total"] == 35 and cov["n_queries_ok"] == 35
          and cov["n_queries_unavailable"] == 0 and cov["n_channels"] == 5,
          "%d queries, %d OK, %d UNAVAILABLE, %d channels"
          % (cov["n_queries_total"], cov["n_queries_ok"],
             cov["n_queries_unavailable"], cov["n_channels"]))
    check("(2b) 23 queries are new relative to leg 174's 12",
          cov["n_queries_new_vs_leg174"] == 23 and cov["superset_of_leg174_net"],
          "%d new" % cov["n_queries_new_vs_leg174"])
    check("(2c) 68 distinct papers returned, every one with its link recorded",
          cov["n_distinct_papers_returned"] == 68
          and all(len(q["links"]) == q["n"] for q in s["query_log"]),
          "%d distinct" % cov["n_distinct_papers_returned"])

    # ---- (3) leg 174's own net replicates exactly --------------------------
    check("(3) all 12 of leg 174's queries return the counts leg 174 banked",
          c1["n_grown"] == 0 and c1["all_counts_identical_to_leg174"] is True
          and len(c1["rows"]) == 12,
          "0/12 grew; deltas %s" % sorted({r["delta"] for r in c1["rows"]}))
    check("(3b) 10 links behind those counts were never recorded by leg 174",
          c1["leg174_links_never_recorded"] == 10,
          "%d unattributable" % c1["leg174_links_never_recorded"])

    # ---- (4) the gate, in its pre-committed wording ------------------------
    check("(4) gate answers YES", s["gate_answer"] == "YES", s["gate_answer"])
    new_hits = [h for h in s["hits"] if not h["already_in_PRECEDENTS"]]
    check("(4b) exactly one hit is new to solver/viscous_novelty.py::PRECEDENTS",
          len(new_hits) == 1 and new_hits[0]["arxiv_id"] == THE_HIT,
          new_hits[0]["link"] if new_hits else "-")
    check("(4c) the other hit was already banked (2509.14185), so it is not news",
          any(h["already_in_PRECEDENTS"] and h["arxiv_id"] == "2509.14185"
              for h in s["hits"]))

    # ---- (5) the cell is CLAIMED, not FILLED -------------------------------
    check("(5) the cell is recorded as claimed, with zero ESTABLISHED occupants",
          cell["grade_A_fluid_occupants_before"] == 0
          and cell["grade_A_fluid_occupants_claimed_after"] == 1
          and cell["grade_A_fluid_occupants_ESTABLISHED_after"] == 0,
          "before 0 -> claimed 1, established 0")
    check("(5b) the full-text read is routed to leg 309, not done here",
          "309" in cell["why_claimed_not_established"]
          and "309" in new_hits[0]["what_this_leg_does_with_it"])
    check("(5c) four credibility flags are recorded at abstract level",
          len(new_hits[0]["credibility_flags_visible_at_abstract_level"]) == 4,
          "%d flags" % len(new_hits[0]["credibility_flags_visible_at_abstract_level"]))

    # ---- (6) the near misses carry a named failing clause ------------------
    adjudicated = [n for n in s["near_misses"] if n.get("adjudication")]
    check("(6) 34 near misses recorded; every adjudicated one names its failing clause",
          cell["n_near_misses_recorded"] == 34
          and all(n.get("failing_clause") for n in adjudicated),
          "%d near, %d adjudicated by hand" % (cell["n_near_misses_recorded"],
                                               len(adjudicated)))
    check("(6b) 4 mechanical verdicts were overridden by hand, all visible as overrides",
          cell["n_mechanical_verdicts_overridden"] == 4,
          "%d overrides" % cell["n_mechanical_verdicts_overridden"])
    by_clause = {}
    for n in adjudicated:
        by_clause[n["failing_clause"]] = by_clause.get(n["failing_clause"], 0) + 1
    check("(6c) the two failure modes are 'no certificate' and 'inviscid object'",
          set(by_clause) == {"a_certificate", "c_dissipative"},
          " ".join("%s=%d" % kv for kv in sorted(by_clause.items())))

    # ---- (7) the NRS/Tsai screen -------------------------------------------
    sb = s["screen_boundary_NRS_Tsai"]
    check("(7) the screen boundary is unmoved; 5 boundary-adjacent works recorded",
          sb["verdict"].startswith("UNMOVED") and len(sb["movers_found"]) == 5,
          "%d movers, %d strengthening"
          % (len(sb["movers_found"]),
             sum(1 for m in sb["movers_found"] if m["moves_boundary"])))

    # ---- (8) the walls -----------------------------------------------------
    check("(8) Clay odds unchanged at ~0.05%",
          "0.05%" in s["clay_odds_note"] and "unchanged" in s["clay_odds_note"])
    check("(8b) this leg lands normally: no sec-8 escalation is triggered",
          "ESCALATION-CANDIDATE" in s["escalation"]
          and "not an escalation as landed" in s["escalation"])

    make_figure(s)

    bad = [c for c in CHECKS if not c[1]]
    print("\n%d/%d checks pass" % (len(CHECKS) - len(bad), len(CHECKS)))
    return 1 if bad else 0


def make_figure(s):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.2, 5.4),
                                   gridspec_kw={"width_ratios": [1.05, 1.0]})

    # ---------------- left: the 2x2 occupancy matrix ----------------
    axL.set_title("The occupancy matrix after leg 303's sweep\n"
                  "(rows: where the dissipation sits; columns: is it a fluid transport model)",
                  fontsize=10, pad=26)
    axL.set_xlim(0, 2); axL.set_ylim(0, 2.16); axL.set_xticks([]); axL.set_yticks([])
    axL.set_frame_on(False)
    for x in (0, 1, 2):
        axL.plot([x, x], [0, 2], color="0.55", lw=1)
    for y in (0, 1, 2):
        axL.plot([0, 2], [y, y], color="0.55", lw=1)
    axL.text(0.5, 2.06, "non-fluid", ha="center", fontsize=10, fontweight="bold")
    axL.text(1.5, 2.06, "fluid", ha="center", fontsize=10, fontweight="bold")
    axL.text(-0.03, 1.5, "Grade A\ndissipation INSIDE\nthe certified object",
             ha="right", va="center", fontsize=9, fontweight="bold")
    axL.text(-0.03, 0.5, "Grade B / none\ninviscid object,\nviscosity dominated",
             ha="right", va="center", fontsize=9, fontweight="bold")

    cells = {
        (0, 1): ("2410.05480  CGL (PRE_EMPTS)\n2404.04054  visc. Burgers (ADJACENT)",
                 "#dbeafe"),
        (1, 1): ("EMPTY before this sweep\n\nnow: 1 CLAIMANT, 0 established\narXiv:2604.09949  "
                 "(3D NS, NK + interval)\nfull-text read -> leg 309", "#fde68a"),
        (0, 0): ("2410.05480 has no fluid twin\n(nothing lands here)", "#f3f4f6"),
        (1, 0): ("2208.09445 BCG (Grade B)\n2210.07191 + 2305.05660 Chen-Hou\n"
                 "2509.14185, 2207.07548, 1908.09385\nnew this sweep: 2501.15701, 2509.12435",
                 "#e5e7eb"),
    }
    for (col, row), (txt, colour) in cells.items():
        axL.add_patch(plt.Rectangle((col, row), 1, 1, facecolor=colour, edgecolor="none",
                                    zorder=0))
        axL.text(col + 0.5, row + 0.5, txt, ha="center", va="center", fontsize=7.4,
                 zorder=1)
    axL.add_patch(plt.Rectangle((1, 1), 1, 1, facecolor="none", edgecolor="#b45309",
                                lw=2.4, zorder=2))

    # ---------------- right: why the 34 near misses miss ----------------
    near = [n for n in s["near_misses"] if n.get("adjudication")]
    a_fail = sum(1 for n in near if n["failing_clause"] == "a_certificate")
    c_fail = sum(1 for n in near if n["failing_clause"] == "c_dissipative")
    unadj = s["cell_state"]["n_near_misses_recorded"] - len(near)
    labels = ["no certificate\n(clause a)", "inviscid object\n(clause c)",
              "screened out\nmechanically"]
    vals = [a_fail, c_fail, unadj]
    bars = axR.barh(labels, vals, color=["#93c5fd", "#fca5a5", "#d1d5db"])
    axR.bar_label(bars, padding=3, fontsize=9)
    axR.set_xlim(0, max(vals) * 1.35)
    axR.set_xlabel("papers, out of the %d the sweep returned"
                   % s["coverage"]["n_distinct_papers_returned"], fontsize=9)
    axR.set_title("Why every other candidate misses the cell\n"
                  "35/35 queries reached, 0 reported as a zero", fontsize=10)
    axR.spines[["top", "right"]].set_visible(False)
    axR.text(0.98, 0.06,
             "leg 174's 12 queries replicate exactly: 0/12 counts grew\n"
             "but 10 of its links were never recorded, so which papers\n"
             "it read and rejected is unrecoverable",
             transform=axR.transAxes, ha="right", va="bottom", fontsize=7.6,
             bbox=dict(boxstyle="round", fc="#fffbeb", ec="#d1d5db"))

    fig.suptitle("Route-GAF v1 (leg 303) — Grade-A/fluid cell freshness sweep, 2026-08-11",
                 fontsize=11.5, fontweight="bold")
    fig.tight_layout(rect=[0.10, 0, 1, 0.94])
    fig.savefig(FIG, dpi=150)
    plt.close(fig)
    print("wrote %s" % os.path.relpath(FIG, ROOT))


if __name__ == "__main__":
    sys.exit(main())
