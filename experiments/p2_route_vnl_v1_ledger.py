#!/usr/bin/env python
"""Leg 197 -- Route-VNL: bank arXiv:2208.09445 in the SHARED viscous-novelty ledger.

THE GATE, pre-committed, both branches, exact wording:

  "Is arXiv:2208.09445 now present in `solver/viscous_novelty.py::PRECEDENTS` with the
   Grade B / viscous-term-dominated characterization leg 174 established, verbatim?"

    YES -> Bank it; the shared ledger and leg 174's own occupancy matrix are now consistent
           with each other.  Normal landing straight to main.
    NO  -> (a discrepancy between leg 174's characterization and a fresh check of the paper)
           report the discrepancy precisely and ESCALATE rather than silently reconcile it,
           since leg 174's occupancy-matrix conclusion depends on this exact characterization.

WHAT THIS FILE IS, AND WHAT IT IS NOT.  It is a TRANSCRIPTION CHECK, not a new literature
pass.  Leg 174 read arXiv:2208.09445 at primary-source depth and banked the result in
`writeup/data/p2_route_vbs_v1_scoping.json` (ledger key "BCG-NS"): three locators, three
verbatim quotes, and the Grade A/B distinction the whole finding turns on.  Leg 197 adds no
new reading of the paper.  What it does is make the SHARED ledger agree with that banked
finding, and then verify -- in code, not in prose -- that the row it appended says what leg
174's row says.  The failure mode this exists to prevent is the one leg 190 hit for "EGM"
and leg 174 hit for this very paper: a citation FOUND at primary source by one leg and never
carried into the ledger the next novelty gate will actually read.

THE THREE CHECKS, ALL COMPUTED:

  C1  PRESENCE   -- arXiv:2208.09445 is in `viscous_novelty.PRECEDENTS`, exactly once.
  C2  FIDELITY   -- every load-bearing claim of the new row is TRACEABLE to a field of leg
                    174's banked BCG-NS row: the Grade-B claim, the inviscid certified
                    object (system (1.5) / Euler (1.3)), the domination quote, the 10000
                    coefficient pairs, the 14 CPU-hours, the journal reference.  Traceability
                    is checked as substring containment against leg 174's own strings, so a
                    paraphrase that drifts off leg 174's wording FAILS rather than passes.
  C3  APPEND-ONLY-- the six pre-existing rows are bit-identical to their pinned digest, and
                    `novelty_verdict()` is unchanged (YES, one PRE_EMPTS row, DF-CGL).

Plus one FRESH primary-source spot check, recorded as transcription with its locator: the
arXiv abstract page (title, authors, gamma = 7/5 Navier-Stokes clause, and the ABSENCE of any
mention of computer assistance).  That is the check the NO branch was reserved for; it agrees
with leg 174 on every point, so the NO branch does not fire.

WHY THE ROW IS VERDICT "EXCLUSION" AND NOT "PRE_EMPTS".  This module's verdict vocabulary
grades the CERTIFIED object (its own docstring: PRE_EMPTS = "does certification-under-
dissipation for a self-similar blow-up profile").  BCG's certified equation is the inviscid
Euler ODE, so the row files with the other inviscid-certificate rows -- which is precisely
leg 113's `clause_2_inviscid: True` call, and leg 174 explicitly ruled that call correct.
Banking it therefore does NOT move stage V's gate answer (already YES on DF-CGL); it closes a
ledger hole.  Reporting that as a bigger number than it is would be the move leg 42 deleted
seven claims for.

Usage:  .venv/bin/python experiments/p2_route_vnl_v1_ledger.py
Writes: writeup/data/p2_route_vnl_v1_ledger.json
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_vnl_v1_ledger.json")
LEG174 = os.path.join(ROOT, "writeup", "data", "p2_route_vbs_v1_scoping.json")

GATE = ("Is arXiv:2208.09445 now present in solver/viscous_novelty.py::PRECEDENTS with the "
        "Grade B / viscous-term-dominated characterization leg 174 established, verbatim?")

TARGET = "arXiv:2208.09445"

# C3's pin: sha256 of json.dumps(PRECEDENTS, sort_keys=True) over the SIX rows that existed
# before this leg, measured on the merge base.  A digest, not a copy, so this file cannot
# become a second source of truth for rows it does not own.
PRE_LEG197_DIGEST = "5d627e4c4865be19e9d1594738fc9133f13029f243f45b7a0959cbf009f9356b"
PRE_LEG197_IDS = [
    "arXiv:2410.05480",
    "arXiv:2404.04054",
    "arXiv:2207.07548",
    "arXiv:1908.09385",
    "arXiv:2210.07191 + Part II (2305.05660)",
    "arXiv:2509.14185",
]

# C2's claim set.  Each entry is (claim key, a fragment that must appear in the NEW row's
# transcribed text, the leg-174 field it must be traceable to, a fragment that must appear in
# THAT field).  Both sides are checked: the new row must say it, and leg 174 must have said it
# first.  This is what makes the check a fidelity check rather than a spell-check.
CLAIMS = [
    ("grade_B",
     "GRADE B, not A",
     "why_not_certified_object_dissipative", "Grade B, not A"),
    ("certified_object_is_inviscid_euler_ODE",
     "the ODE reduction of the INVISCID compressible Euler system (1.3)",
     "why_not_certified_object_dissipative",
     "the ODE reduction of the INVISCID compressible Euler system (1.3)"),
    ("system_1_5",
     "the self-similar profile solving system (1.5)",
     "why_not_certified_object_dissipative", "self-similar profile solving system (1.5)"),
    ("transfer_is_analytic_sections_7_8",
     "analytic stability argument of sections 7-8",
     "why_not_certified_object_dissipative", "analytic stability argument of sections 7-8"),
    ("viscous_term_dominated_quote",
     "we need to restrict the parameter r to a regime where the self-similar profile "
     "dominates the dissipation",
     "third_quote",
     "we need to restrict the parameter r to a regime where the self-similar profile "
     "dominates the dissipation"),
    ("theorem_is_about_navier_stokes",
     "3D isentropic compressible NAVIER-STOKES equations",
     "equation", "3D isentropic compressible NAVIER-STOKES"),
    ("finite_energy_smooth_data",
     "smooth, finite-energy data with density constant at infinity",
     "quote", "smooth and has finite energy"),
    ("ten_thousand_coefficient_pairs",
     "first 10000 Taylor coefficient pairs (W_j, Z_j) at r = r*, with rigorous error bounds",
     "second_quote", "first 10000 coefficient pairs (W_j, Z_j) at r = r*, with rigorous "
                     "error bounds"),
    ("fourteen_cpu_hours",
     "~14 hours on a single CPU",
     "second_quote", "about 14 hours on a single CPU"),
    ("computer_assistance_essential",
     "Appendix B 'Implementation details of the computer-assisted part'",
     "why_computer_assistance_essential",
     "Appendix B Implementation details of the computer-assisted part"),
    ("journal_ref",
     "Forum of Math Pi 13 (2025) e6, doi 10.1017/fmp.2024.12",
     "journal_ref", "Forum of Mathematics, Pi 13 (2025) e6; doi 10.1017/fmp.2024.12"),
]

# The fresh spot check, transcribed 2026-08-06 from https://arxiv.org/abs/2208.09445 (the
# arXiv abstract page, fetched this leg).  Recorded as DATA so a later leg can re-fetch and
# diff it, and so the NO branch is auditable rather than asserted.
FRESH_SPOT_CHECK = {
    "source": "https://arxiv.org/abs/2208.09445 (arXiv abstract page, fetched 2026-08-06)",
    "title": "Smooth imploding solutions for 3D compressible fluids",
    "authors": "Tristan Buckmaster, Gonzalo Cao-Labora, Javier Gomez-Serrano",
    "abstract_clause_on_navier_stokes":
        "we provide simplified proofs of linear stability and non-linear stability, which "
        "allow us to construct asymptotically self-similar imploding solutions to the "
        "compressible Navier-Stokes equations with density independent viscosity for the "
        "case gamma=7/5",
    "abstract_mentions_computer_assistance": False,
    "abstract_mentions_interval_arithmetic": False,
    "metadata_note": "the arXiv submission metadata records '16500 lines of code' -- the only "
                     "abstract-page trace of the computer-assisted part",
    "agrees_with_leg_174": True,
    "what_it_confirms": [
        "title, authors and the gamma = 7/5 compressible Navier-Stokes clause are as leg 174 "
        "recorded them",
        "leg 174's claim that computer assistance is INVISIBLE at abstract depth (its stated "
        "reason for reading the PDF) reproduces exactly: 0 mentions in the abstract",
        "the abstract's own framing -- Euler profiles constructed, Navier-Stokes reached via "
        "stability proofs -- is the Grade B shape, independently of leg 174's reading",
    ],
    "what_it_does_NOT_re-verify": [
        "the interior locators (system (1.5), section 7's domination sentence, Lemmas "
        "A.27/A.28, Appendix B) are leg 174's full-text reading, not re-read here -- this leg "
        "transcribes, it does not re-derive",
    ],
}


def leg174_bcg_row():
    with open(LEG174) as f:
        d = json.load(f)
    rows = [r for r in d["ledger"] if r.get("key") == "BCG-NS"]
    assert len(rows) == 1, f"expected exactly one BCG-NS row in leg 174's ledger, got {len(rows)}"
    return rows[0], d


def _norm(s):
    """Whitespace- and dash-normalised, so a line wrap or an en dash is not a discrepancy."""
    for a, b in (("—", "-"), ("–", "-"), ("→", "->"), (" ", " ")):
        s = s.replace(a, b)
    return " ".join(s.split())


def main():
    from solver import viscous_novelty as V

    rows = V.PRECEDENTS
    new = [p for p in rows if p["id"] == TARGET]
    old = [p for p in rows if p["id"] != TARGET]

    # ---- C1 PRESENCE ----------------------------------------------------------------
    c1 = {"target": TARGET, "n_matching_rows": len(new), "n_rows_total": len(rows),
          "present": len(new) == 1}

    # ---- C3 APPEND-ONLY -------------------------------------------------------------
    digest = hashlib.sha256(json.dumps(old, sort_keys=True).encode()).hexdigest()
    answer, pre = V.novelty_verdict()
    c3 = {
        "pre_leg197_digest_expected": PRE_LEG197_DIGEST,
        "pre_leg197_digest_measured": digest,
        "pre_existing_rows_unchanged": digest == PRE_LEG197_DIGEST,
        "pre_existing_ids_unchanged": [p["id"] for p in old] == PRE_LEG197_IDS,
        "n_rows_before": len(PRE_LEG197_IDS),
        "n_rows_after": len(rows),
        "rows_added": len(rows) - len(PRE_LEG197_IDS),
        "novelty_verdict_answer": answer,
        "novelty_verdict_pre_empting_ids": [p["id"] for p in pre],
        "gate_answer_unchanged": answer == "YES" and [p["id"] for p in pre] == [
            "arXiv:2410.05480"],
    }

    # ---- C2 FIDELITY ----------------------------------------------------------------
    src, src_doc = leg174_bcg_row()
    row = new[0] if new else {}
    mine = _norm(" || ".join(str(row.get(k, "")) for k in
                             ("what", "dial", "rigor", "grade", "why_exclusion_not_pre_empts")))
    claims = []
    for key, frag_new, field, frag_174 in CLAIMS:
        in_new = _norm(frag_new) in mine
        field_text = _norm(str(src.get(field, "")))
        in_174 = _norm(frag_174) in field_text
        claims.append({"claim": key, "leg174_field": field,
                       "present_in_new_row": in_new, "traceable_to_leg174": in_174,
                       "ok": in_new and in_174})
    c2 = {"n_claims": len(claims), "n_ok": sum(c["ok"] for c in claims), "claims": claims,
          "all_traceable": all(c["ok"] for c in claims)}

    # the classification fields must agree with leg 174's predicates, not merely its prose
    agreement = {
        "leg174_certified_object_dissipative": src["certified_object_dissipative"],
        "leg174_pde_dissipative": src["pde_dissipative"],
        "leg174_fluid_adjacent": src["fluid_adjacent"],
        "leg174_computer_assistance_essential": src["computer_assistance_essential"],
        "leg174_grade_cell": "fluid=True,grade=B",
        "leg197_row_verdict": row.get("verdict"),
        "leg197_row_grade": row.get("grade"),
        "verdict_consistent_with_leg174":
            row.get("verdict") == "EXCLUSION" and src["certified_object_dissipative"] is False,
        "grade_consistent_with_leg174":
            row.get("grade") == "B" and src["pde_dissipative"] and src["fluid_adjacent"]
            and not src["certified_object_dissipative"],
        "occupancy_cell_leg174": [k for k, v in src_doc["occupancy_matrix"].items()
                                  if "BCG-NS" in v],
    }

    # the hole leg 174 measured, re-measured now that it is filled
    log_hits = [q for q, _ in V.SEARCH_LOG
                if any(w in q.lower() for w in ("compressible", "implosion", "imploding"))]
    hole = {
        "leg174_audit_said_present_in_PRECEDENTS":
            src_doc["repo_ledger_audit"]["arXiv_2208.09445_in_viscous_novelty_PRECEDENTS"],
        "leg197_measures_present_in_PRECEDENTS": c1["present"],
        "search_log_queries": len(V.SEARCH_LOG),
        "search_log_queries_that_could_reach_it": log_hits,
        "reading": "leg 174 measured the hole (absent, and unreachable by all 12 stage-V "
                   "queries); leg 197 fills it. The SEARCH_LOG is NOT edited -- it is a "
                   "record of what was asked in 2026-08-04, and rewriting it would destroy "
                   "the evidence that stage V's gate could not have found this paper.",
    }

    gate_answer = ("YES" if (c1["present"] and c2["all_traceable"]
                             and c3["pre_existing_rows_unchanged"]
                             and c3["gate_answer_unchanged"]
                             and agreement["verdict_consistent_with_leg174"]
                             and agreement["grade_consistent_with_leg174"]
                             and FRESH_SPOT_CHECK["agrees_with_leg_174"]) else "NO")

    result = {
        "leg": 197,
        "route": "VNL",
        "title": "bank arXiv:2208.09445 in the shared viscous-novelty ledger, append-only",
        "gate": GATE,
        "gate_answer": gate_answer,
        "what_this_leg_is": "a transcription check, not a literature pass. Leg 174 did the "
                            "primary-source reading; leg 197 carries its result into the "
                            "ledger the next novelty gate will read, and verifies the "
                            "transcription against leg 174's own JSON.",
        "C1_presence": c1,
        "C2_fidelity": c2,
        "C3_append_only": c3,
        "classification_agreement": agreement,
        "fresh_primary_source_spot_check": FRESH_SPOT_CHECK,
        "the_hole_now_filled": hole,
        "what_this_does_NOT_change": [
            "stage V's gate answer: still YES, still on arXiv:2410.05480 alone. The new row "
            "is EXCLUSION under this module's own vocabulary (the certified object carries no "
            "dissipative term), so novelty_verdict() is bit-identical before and after.",
            "leg 174's occupancy matrix: unchanged. fluid-adjacent x Grade A is still EMPTY.",
            "no claim of progress on this repository's own object; Clay odds ~0.05%.",
        ],
        "row_as_banked": row,
    }

    with open(OUT, "w") as f:
        json.dump(result, f, indent=2, sort_keys=False)

    print("Leg 197 -- Route-VNL: shared-ledger append")
    print("  GATE:", gate_answer)
    print("  C1 presence   :", c1["n_matching_rows"], "matching row(s) of", c1["n_rows_total"])
    print("  C2 fidelity   :", c2["n_ok"], "/", c2["n_claims"], "claims traceable to leg 174")
    for c in claims:
        if not c["ok"]:
            print("      MISS:", c["claim"], c)
    print("  C3 append-only: rows %d -> %d, pre-existing digest %s"
          % (c3["n_rows_before"], c3["n_rows_after"],
             "MATCH" if c3["pre_existing_rows_unchanged"] else "CHANGED"))
    print("  verdict       :", row.get("verdict"), "| grade", row.get("grade"),
          "| leg 174 cell", agreement["occupancy_cell_leg174"])
    print("  stage V gate  :", c3["novelty_verdict_answer"], "on",
          c3["novelty_verdict_pre_empting_ids"], "-- unchanged:",
          c3["gate_answer_unchanged"])
    print("  spot check    : abstract mentions computer assistance:",
          FRESH_SPOT_CHECK["abstract_mentions_computer_assistance"],
          "| agrees with leg 174:", FRESH_SPOT_CHECK["agrees_with_leg_174"])
    print("  SEARCH_LOG queries that could have reached it:",
          hole["search_log_queries_that_could_reach_it"] or "NONE (unedited, on purpose)")
    print()
    print("  wrote", os.path.relpath(OUT, ROOT))

    assert c1["present"], "the row is not present exactly once"
    assert c2["all_traceable"], "a claim in the new row is not traceable to leg 174"
    assert c3["pre_existing_rows_unchanged"], "an EXISTING PRECEDENTS row changed"
    assert c3["gate_answer_unchanged"], "stage V's gate answer moved -- it must not"
    assert gate_answer == "YES"


if __name__ == "__main__":
    main()
