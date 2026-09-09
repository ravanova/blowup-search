"""Arc-5 evidence: rebuild every number quoted in BLOG_OUTPACED.md / TECHNICAL_OUTPACED.md.

This arc runs no experiment. Its primaries are (a) this repository's own landed
files and (b) an external public record read on 2026-09-09. Both are banked in
    writeup/data/arc5_outpaced_v1.json
and this script recomputes the derived arithmetic from them:

    .venv/bin/python writeup/5_outpaced/outpaced_evidence.py

It prints a claim table and CHECKS each derived number against the value written
in the prose. Exit 0 = every prose number is reproduced from the JSON. Exit 1 =
a prose number drifted from its source, which is a documentation-contract
failure, not a rounding opinion.

No figure is produced. See TECHNICAL_OUTPACED.md section 6: this arc has no
measurement of its own to plot, and that gap is recorded rather than hidden.

Deliberately NOT done here: any claim about whether the external result is
correct. This script checks arithmetic and provenance. The external record's
status is UNVERIFIED and this script does not move it.
"""

import json
import sys
from datetime import date
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
JSON = DATA / "arc5_outpaced_v1.json"

# Values as written in the prose. If a prose edit drifts from the JSON, this
# table is what catches it.
PROSE = {
    "span_days": 28,
    "legs_per_day": 14.86,
    "cp95_upper": 0.007175,
    "legs_per_link_at_bound": 139.4,
    "days_per_link_measured_cadence": 9.4,
    "parity_years_total": 11.98,
    "parity_years_proof_only": 10.04,
    "odds_years": {2.5: 61.3, 2.0: 76.7, 1.75: 87.6, 1.5: 102.2},
}

TOL = 5e-3  # relative; the prose quotes 3-4 significant figures throughout


def _close(got, want, tol=TOL):
    if want == 0:
        return abs(got) < tol
    return abs(got - want) / abs(want) <= tol


def main():
    d = json.loads(JSON.read_text())
    prog = d["this_programme"]
    ext = d["external_record"]["openai_navier_stokes"]
    fails = []

    def check(label, got, want, unit="", note=""):
        ok = _close(got, want)
        mark = "ok  " if ok else "FAIL"
        print(f"  [{mark}] {label:<52} {got:>12.4f} {unit:<10} (prose: {want})"
              + (f"  -- {note}" if note else ""))
        if not ok:
            fails.append(label)

    print(f"\nARC 5 — OUTPACED · evidence rebuild from {JSON.name}")
    print(f"artefact: {d['artefact']}   date: {d['date']}")

    # ---- provenance banner -------------------------------------------------
    print("\n== PROVENANCE ==")
    print("  external_record : UNVERIFIED here — not audited at full text, not")
    print("                    reproduced, no Lean file compiled in this repo.")
    print("  this_programme  : PRIMARY — every field cites its repository file.")
    print("  derived         : recomputed below, never restated from prose.")

    # ---- 1. measured throughput -------------------------------------------
    print("\n== 1. MEASURED THROUGHPUT (primary) ==")
    d0 = date.fromisoformat(prog["span_start"]["value"])
    d1 = date.fromisoformat(prog["span_end"]["value"])
    span = (d1 - d0).days
    legs = prog["legs_run"]["value"]
    check("span 2026-07-22 -> 2026-08-19", span, PROSE["span_days"], "days")
    check("cadence legs/day", legs / span, PROSE["legs_per_day"], "legs/day")
    print(f"  [ -- ] {'live leg slots actually run':<52} "
          f"{prog['concurrency_actually_run']['live_leg_slots']:>12} "
          f"{'Opus 5':<10} (+1 Fable 5 DM, 20-worker ceiling)")
    print(f"  [ -- ] {'L1 -> L4 links moved':<52} "
          f"{prog['l1_l4_links_moved']['value']:>12}  in {legs} legs")

    # ---- 2. price C: what the record measures ------------------------------
    print("\n== 2. PRICE C — the Clopper-Pearson bound on 0 successes in "
          f"{legs} legs ==")
    cp = 1 - 0.05 ** (1 / legs)
    check("one-sided 95% upper bound, per leg", cp, PROSE["cp95_upper"])
    check("legs per link AT THE BOUND", 1 / cp,
          PROSE["legs_per_link_at_bound"], "legs")
    check("days per link at measured cadence", (1 / cp) / (legs / span),
          PROSE["days_per_link_measured_cadence"], "days")
    print("         DIRECTION: this bounds the RATE ABOVE, so it bounds the")
    print("         TIME BELOW. It is a FLOOR with no ceiling. Quoting it as a")
    print("         forecast inverts it.")

    # ---- 3. price A: agent-hour parity -------------------------------------
    print("\n== 3. PRICE A — agent-hour parity at 10 concurrent agents ==")
    comp = ext["compute_as_reported"]
    ours = d["derived"]["agent_hour_parity"]["our_agent_count"]
    for hours, key, label in (
        (comp["hours_total"], "parity_years_total", "proof + Lean (105 h)"),
        (comp["hours_proof_only"] if "hours_proof_only" in comp
         else comp["hours_to_proof"], "parity_years_proof_only",
         "proof only (88 h)"),
    ):
        ah = comp["concurrent_agents"] * hours
        check(f"{label}", ah / ours / 24 / 365.25, PROSE[key], "years",
              note=f"{ah:,} agent-h / {ours}")
    print("         ASSUMPTION (false): that our 10 agents run their method, on")
    print("         their model, at their efficiency. This is the price of")
    print("         BURNING THE FUEL, not of arriving.")

    # ---- 4. price B: the programme's own odds ------------------------------
    print("\n== 4. PRICE B — the programme's own self-assessed odds ==")
    odds = prog["self_assessed_clay_odds"]["value"]
    n = 1 / odds
    print(f"  [ -- ] {'programme-equivalents at ~0.05%':<52} {n:>12,.0f}")
    for s in d["derived"]["odds_parity"]["speedups_considered"]:
        check(f"at {s}x slot speedup ({span / s:.1f} d/programme)",
              n * (span / s) / 365.25, PROSE["odds_years"][s], "years")
    print("         ASSUMPTION: that programmes are independent repeats. The")
    print("         record says the odds were 'unmoved' across 416 legs, i.e.")
    print("         NOT a per-trial rate that accumulates.")

    # ---- 5. the structural answer ------------------------------------------
    print("\n== 5. THE STRUCTURAL ANSWER (why the prices are beside the point) ==")
    for i, r in enumerate(d["the_finding"]["structural_reasons_the_plan_could_not_have_arrived"], 1):
        head = r.split(".", 1)[0]
        print(f"  {i}. {head}")
    print(f"\n  ceiling: {prog['ceiling']['value']}"
          f"   |   obligations with no known method: "
          f"{prog['obligations_with_no_known_method']['count']}"
          f"   |   cheapest unit that could move a link: "
          f"{prog['cheapest_unit_that_could_move_one']['value']}")
    print(f"  genome is initial data only (no force gene): "
          f"{prog['genome_is_initial_data']['value']}"
          f"   |   external construction starts from: "
          f"{ext['initial_data_as_reported']}")

    # ---- 6. what is NOT established ----------------------------------------
    print("\n== 6. WHAT THIS DOES NOT ESTABLISH ==")
    for s in d["the_finding"]["what_this_does_NOT_establish"]:
        print(f"  - {s}")

    # ---- 7. movement -------------------------------------------------------
    print("\n== 7. MOVEMENT ==")
    print(f"  walls moved: none   |   L1->L4 links moved: 0   |   Clay odds: "
          f"{prog['self_assessed_clay_odds']['as_written']}, unchanged")
    print("  Tier 2 is never a proof. This arc produces no tier.")

    print()
    if fails:
        print(f"EVIDENCE REBUILD: FAIL ({len(fails)} prose number(s) drifted "
              f"from {JSON.name})")
        for f in fails:
            print(f"  - {f}")
        return 1
    print("EVIDENCE REBUILD: PASS — every prose number reproduced from the JSON.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
