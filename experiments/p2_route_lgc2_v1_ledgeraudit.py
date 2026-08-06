"""ROUTE-LGC2 v1 (leg 213): the POST-APPEND consistency audit of the two shared ledgers.

Leg 145 (Route-LGA) audited `solver/literature_gates.py::CLAIM_LEDGER` for citation-to-claim
fidelity and found 3 drifted rows.  That audit ran BEFORE this cycle's appends.  Since then:

  * leg 190 (Route-EGML) appended `EGM_PRIMARY_READ` to `solver/literature_gates.py`,
  * leg 197 (Route-VNL)  appended the `arXiv:2208.09445` row to
    `solver/viscous_novelty.py::PRECEDENTS`,
  * leg 189 (Route-XUTRI) correctly appended NOTHING (gate NO, null result),
  * leg 214 (Route-EGMB) corrected the five leg-141/leg-165 PROSE sites that leg 190 flagged,
    and deliberately left `literature_gates.py` untouched.

THE GATE, verbatim and pre-committed:

  "Do the 190 and 197 rows match `literature_gates.py`'s and `viscous_novelty.py`'s own
   existing row format exactly, with no duplicate/conflicting entry and no transcription drift
   from legs 190's/197's own banked reports?"

  YES -> bank as confirming ledger integrity post-append; record the pass in capabilities.py.
  NO  -> name the exact inconsistency precisely and ESCALATE.  Never silently reconcile:
         both ledgers are shared infrastructure that every literature-pass leg reads.

--------------------------------------------------------------------------
WHY "APPEND-ONLY" IS NOT AUTOMATICALLY SAFE, WHICH IS THE WHOLE PREMISE
--------------------------------------------------------------------------
An append cannot corrupt an existing row's BYTES.  It can do three other things, and this
runner is built around exactly those three:

  (1) FORMAT DRIFT.  A new row shaped unlike its neighbours makes every consumer that walks
      the structure either miss it or trip on it.  Neither ledger's tests catch this:
      `test_viscous_novelty.py:50` is `fields <= set(p)`, a SUBSET check, so a row with extra
      or renamed optional keys passes; and `EGM_PRIMARY_READ` sits OUTSIDE `CLAIM_LEDGER`, so
      `test_8_ledger_does_not_rot` never reaches it.

  (2) DUPLICATE / CONFLICT.  Two rows for one paper, disagreeing.  `novelty_verdict()`
      filters on `verdict` and would silently count a duplicate twice.

  (3) TRANSCRIPTION DRIFT.  The row paraphrases the source leg instead of transcribing it.
      This is the defect leg 145 actually found three of, and no test can see it, because
      "says the same thing" is not a property of a string.

  ...and this runner adds a FOURTH, which the gate's wording does not name but which the
  spec's own note about leg 214 points at directly:

  (4) POST-HOC STALENESS.  A row that was TRUE when appended and that a LATER leg falsified
      without touching the row.  An append-only discipline protects the bytes of old rows; it
      offers no protection at all to a NEW row whose truth depends on files outside it.

--------------------------------------------------------------------------
THE EVIDENCE MODEL: EVERYTHING COMPARED IS COMMITTED
--------------------------------------------------------------------------
Leg 145 had to store verbatim quotes because `Papers/` is gitignored and decays (banked
lesson 68).  This leg has the easier problem and takes the stronger position: it reads no PDF
and needs none.  Every object it compares -- the two ledger modules, leg 190's JSON, leg 174's
JSON, leg 214's five corrected prose sites -- is git-tracked, so every finding is reproducible
from the repository alone, forever.  Where a check depends on a file this leg does not own,
the check is stated as a comparison between two committed artifacts, never as a claim about
the world.

--------------------------------------------------------------------------
NEGATIVE CONTROLS (banked lesson 90: a control that cannot come out differently is not one)
--------------------------------------------------------------------------
Every checker runs a second time against a DELIBERATELY CORRUPTED copy of the same structure:
a renamed key, a duplicated row, a paraphrased claim, a site list retro-fitted to look fresh.
A checker that passes its own corruption is reported as an ORNAMENT in the JSON and is NOT
counted toward the gate.

--------------------------------------------------------------------------
WHAT THIS IS NOT
--------------------------------------------------------------------------
* Not a re-reading of EGM or BCG.  Whether EGM's gap is -1/2 and whether BCG is Grade B are
  legs 190's and 174's findings; this leg asks only whether the LEDGER says what they said.
* Not a patch.  `solver/literature_gates.py` and `solver/viscous_novelty.py` are read-only to
  this leg under BOTH branches of the gate.
* Not a physics leg.  It imports no solver numerics, derives nothing, lifts no ban.

Run: .venv/bin/python experiments/p2_route_lgc2_v1_ledgeraudit.py
"""

import json
import re
import sys
import time
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from solver.literature_gates import (  # noqa: E402
    CLAIM_LEDGER, EGM_PRIMARY_READ, LSS_PRIMARY_READ,
)
from solver.viscous_novelty import PRECEDENTS, novelty_verdict  # noqa: E402

OUT = ROOT / "writeup" / "data" / "p2_route_lgc2_v1_ledgeraudit.json"

ARXIV_RE = re.compile(r"\b(\d{4}\.\d{4,5})\b")

# The seven keys `test_viscous_novelty.py` requires, i.e. "the schema the gate reads".
PRECEDENT_SCHEMA = ("id", "who", "what", "dial", "rigor", "verdict", "gate")
VERDICT_VOCAB = {"PRE_EMPTS", "ADJACENT", "EXCLUSION"}

# The leg-number-templated key names, so `provenance_before_leg_161` and
# `provenance_before_leg_190` compare as the SAME slot rather than as two mismatches.
LEG_NUM_RE = re.compile(r"_leg_\d+$")


def _slot(key):
    """Normalise a leg-number-templated key to its template."""
    return LEG_NUM_RE.sub("_leg_N", key)


def _norm(s):
    """Whitespace-insensitive, case-insensitive normalisation for containment tests."""
    return re.sub(r"\s+", " ", str(s)).strip().lower()


# =========================================================================
# A1.  FORMAT -- EGM_PRIMARY_READ against its own declared template, LSS_PRIMARY_READ.
#
# leg 190's novelty note sec 6 names the template explicitly: "Leg 161 hit exactly this and
# solved it ... LSS_PRIMARY_READ ... This leg follows that precedent exactly."  So the format
# question has a definite answer, not a taste: does it follow LSS's slot sequence?
# =========================================================================
def a1_format_literature_gates(egm, lss):
    egm_slots = [_slot(k) for k in egm]
    lss_slots = [_slot(k) for k in lss]

    # The citation header both blocks must share, in order.
    header = ["arxiv", "tag", "authors", "title", "venue", "read", "provenance_before_leg_N"]
    egm_header = egm_slots[:len(header)]
    lss_header = lss_slots[:len(header)]

    # Every header field must be a non-empty string in both.
    bad_types = [k for k in header
                 if not (isinstance(egm.get(k if k in egm else _unslot(egm, k)), str))]

    payload_egm = [k for k in egm if isinstance(egm[k], dict)]
    payload_lss = [k for k in lss if isinstance(lss[k], dict)]

    # arXiv id format: bare "NNNN.NNNNN", as LSS stores it (NOT the "arXiv:" prefix that
    # viscous_novelty uses -- the two ledgers have different, internally consistent conventions
    # and mixing them is exactly the drift this check exists for).
    id_ok = bool(re.fullmatch(r"\d{4}\.\d{4,5}", str(egm.get("arxiv", ""))))
    lss_id_ok = bool(re.fullmatch(r"\d{4}\.\d{4,5}", str(lss.get("arxiv", ""))))

    return {
        "template": "LSS_PRIMARY_READ (leg 161), named as the template by leg 190's own novelty sec 6",
        "header_slots_required": header,
        "egm_header_slots": egm_header,
        "lss_header_slots": lss_header,
        "header_sequence_identical": egm_header == lss_header == header,
        "header_fields_all_nonempty_str": all(
            isinstance(egm[k], str) and egm[k].strip() for k in egm if _slot(k) in header),
        "egm_all_slots": egm_slots,
        "lss_all_slots": lss_slots,
        "egm_payload_subdicts": payload_egm,
        "lss_payload_subdicts": payload_lss,
        "payload_count_egm": len(payload_egm),
        "payload_count_lss": len(payload_lss),
        "arxiv_id_bare_format_egm": id_ok,
        "arxiv_id_bare_format_lss": lss_id_ok,
        "arxiv_convention_matches": id_ok and lss_id_ok,
        "bad_types": bad_types,
        # The sub-dict field-name comparison, reported rather than gated: LSS uses `locators`
        # (plural, several pointers per number), EGM uses `locator` (singular, one inequality).
        # Recorded because it IS a difference; classified below in the verdict prose.
        "subdict_shared_fields": sorted(
            set().union(*[set(egm[k]) for k in payload_egm])
            & set().union(*[set(lss[k]) for k in payload_lss])),
        "subdict_egm_only": sorted(
            set().union(*[set(egm[k]) for k in payload_egm])
            - set().union(*[set(lss[k]) for k in payload_lss])),
        "pass": (egm_header == lss_header == header) and id_ok and lss_id_ok and not bad_types,
    }


def _unslot(d, slot):
    for k in d:
        if _slot(k) == slot:
            return k
    return slot


# =========================================================================
# A2.  FORMAT -- leg 197's PRECEDENTS row against the six rows that preceded it.
#
# The module's own test is `fields <= set(p)`, a SUBSET check, so it passes on a row with any
# number of extra keys and on a row whose `id` uses a different citation convention.  This
# check is the one that would notice.
# =========================================================================
def a2_format_viscous_novelty(precedents, appended_id="arXiv:2208.09445"):
    rows = list(precedents)
    idx = [i for i, p in enumerate(rows) if p.get("id") == appended_id]
    per_row = []
    for i, p in enumerate(rows):
        per_row.append({
            "i": i,
            "id": p.get("id"),
            "has_all_seven": set(PRECEDENT_SCHEMA) <= set(p),
            "missing": sorted(set(PRECEDENT_SCHEMA) - set(p)),
            "extra": sorted(set(p) - set(PRECEDENT_SCHEMA)),
            "id_prefixed": str(p.get("id", "")).startswith("arXiv:"),
            "verdict_in_vocab": p.get("verdict") in VERDICT_VOCAB,
            "gate_is_none_or_str": p.get("gate") is None or isinstance(p.get("gate"), str),
            "what_len": len(str(p.get("what", ""))),
            "what_over_60": len(str(p.get("what", ""))) > 60,
            # `who` is a comma-separated surname list in every pre-existing row.
            "who_surname_list": bool(re.fullmatch(r"[^;]+", str(p.get("who", "")))),
        })
    appended = [r for r in per_row if r["id"] == appended_id]
    priors = [r for r in per_row if r["id"] != appended_id]
    return {
        "n_rows": len(rows),
        "appended_row_index": idx,
        "appended_row_is_last": idx == [len(rows) - 1],
        "schema_gate_reads": list(PRECEDENT_SCHEMA),
        "per_row": per_row,
        "all_rows_have_all_seven": all(r["has_all_seven"] for r in per_row),
        "all_ids_prefixed": all(r["id_prefixed"] for r in per_row),
        "all_verdicts_in_vocab": all(r["verdict_in_vocab"] for r in per_row),
        "all_what_over_60": all(r["what_over_60"] for r in per_row),
        "rows_with_extra_keys": [r["id"] for r in per_row if r["extra"]],
        "appended_extra_keys": appended[0]["extra"] if appended else None,
        "prior_rows_with_extra_keys": [r["id"] for r in priors if r["extra"]],
        "extra_keys_documented_in_source": "the seven fields above are the schema the gate reads"
                                           in (ROOT / "solver" / "viscous_novelty.py").read_text(),
        # The module's own subset test, re-run here so the JSON records what it does and does
        # not certify.
        "module_own_test_would_pass": all(r["has_all_seven"] for r in per_row),
        "pass": (all(r["has_all_seven"] for r in per_row)
                 and all(r["id_prefixed"] for r in per_row)
                 and all(r["verdict_in_vocab"] for r in per_row)
                 and all(r["what_over_60"] for r in per_row)
                 and all(r["gate_is_none_or_str"] for r in per_row)),
    }


# =========================================================================
# A3.  DUPLICATE / CONFLICT, in both ledgers.
# =========================================================================
def a3_duplicates(precedents, egm, lss, claim_ledger):
    ids = [str(p.get("id", "")) for p in precedents]
    bare = [ARXIV_RE.search(i).group(1) if ARXIV_RE.search(i) else i for i in ids]
    dup_ids = sorted({b for b in bare if bare.count(b) > 1})

    # Rows sharing a paper must not disagree on verdict -- the conflict that would actually
    # move `novelty_verdict()`.
    by_paper = {}
    for b, p in zip(bare, precedents):
        by_paper.setdefault(b, set()).add(p.get("verdict"))
    conflicting = {k: sorted(v) for k, v in by_paper.items() if len(v) > 1}

    gates_src = (ROOT / "solver" / "literature_gates.py").read_text()
    # Where 1906.05811 occurs in the module.  Expected: the scope comment explaining why it is
    # NOT in a CLAIM_LEDGER `source`, and the block's own `arxiv` field.  Anywhere else would
    # be the second, conflicting home the scope note says must not exist.
    egm_hits = [(i + 1, ln.strip()) for i, ln in enumerate(gates_src.splitlines())
                if "1906.05811" in ln]
    claim_ledger_mentions_egm = [r for r in claim_ledger
                                 if "1906.05811" in json.dumps(r) or "Elgindi" in json.dumps(r)]

    # And the two standalone blocks must not be two homes for one paper.
    two_blocks_distinct = egm.get("arxiv") != lss.get("arxiv")

    verdict_before = novelty_verdict()[0]

    return {
        "viscous_novelty_ids": ids,
        "viscous_novelty_bare": bare,
        "n_unique": len(set(bare)),
        "duplicate_ids": dup_ids,
        "verdict_conflicts_same_paper": conflicting,
        "literature_gates_1906_05811_sites": egm_hits,
        "n_1906_05811_sites": len(egm_hits),
        "claim_ledger_rows_mentioning_egm": len(claim_ledger_mentions_egm),
        "scope_note_promise_kept": len(claim_ledger_mentions_egm) == 0,
        "egm_and_lss_are_different_papers": two_blocks_distinct,
        "novelty_verdict_now": verdict_before,
        "novelty_verdict_expected": "YES",
        "novelty_verdict_unmoved": verdict_before == "YES",
        "pass": (not dup_ids and not conflicting and two_blocks_distinct
                 and len(claim_ledger_mentions_egm) == 0 and verdict_before == "YES"),
    }


# =========================================================================
# A4.  TRANSCRIPTION -- the EGM ledger block against leg 190's OWN banked JSON.
#
# This is the strongest form the check can take: leg 190's JSON carries a `citation` dict and a
# `verbatim` dict that are supposed to be the same objects the ledger block holds.  So this is
# not a paraphrase-similarity test.  It is BYTE EQUALITY, field by field, and a single changed
# word fails it.
# =========================================================================
def a4_transcription_egm(egm):
    j = json.loads((ROOT / "writeup" / "data" / "p2_route_egml_v1_lit.json").read_text())

    cit = j["citation"]
    header_cmp = []
    for k in ("arxiv", "tag", "authors", "title", "venue", "read"):
        header_cmp.append({"field": k, "identical": egm.get(k) == cit.get(k),
                           "ledger_len": len(str(egm.get(k, ""))),
                           "json_len": len(str(cit.get(k, "")))})

    verb = j["verbatim"]
    gap = egm["spectral_gap"]
    verb_cmp = []
    for k in verb:
        verb_cmp.append({"field": k, "in_ledger": k in gap,
                         "identical": gap.get(k) == verb.get(k),
                         "ledger_len": len(str(gap.get(k, ""))),
                         "json_len": len(str(verb.get(k, "")))})

    prose_cmp = []
    for k in ("scope", "the_relayed_p2_claim"):
        prose_cmp.append({"field": k, "identical": egm.get(k) == j.get(k)})

    # The load-bearing NUMBERS the ledger's `re_derived_at_leg_190` prose quotes, checked
    # against the JSON's own measured values rather than against the prose's neighbours.
    e1, e2, e3 = j["E1_egm_constant"], j["E2_gamma_sweep"], j["E3_hilbert_of_F0"]
    prose = egm["re_derived_at_leg_190"]
    decoys = sorted(round(abs(c["max_dev_from_-0.5"]), 3) for c in e1["negative_controls"])
    g39 = [r for r in e2["rows"] if r["gamma"] == 3.9][0]
    numeric_claims = [
        {"claim": "4.44e-16 (E1 max deviation)", "measured": e1["max_dev_analytic"],
         "in_prose": "4.44e-16" in prose,
         "consistent": abs(e1["max_dev_analytic"] - 4.44e-16) < 1e-17},
        {"claim": "spread 8.88e-16", "measured": e1["spread_analytic"],
         "in_prose": "8.88e-16" in prose,
         "consistent": abs(e1["spread_analytic"] - 8.88e-16) < 1e-17},
        # Word-bounded: a bare `"4000" in prose` is satisfied by "40000" and so cannot detect
        # an inflated node count -- control C9 caught exactly that and the checker was fixed
        # rather than the control retired.
        {"claim": "4000 nodes", "measured": e1["n_nodes"],
         "in_prose": bool(re.search(r"\b4000\b nodes", prose)),
         "consistent": e1["n_nodes"] == 4000},
        {"claim": "decoys miss by 0.500 and 0.343", "measured": decoys,
         "in_prose": "0.500 and 0.343" in prose, "consistent": decoys == [0.343, 0.5]},
        {"claim": "gamma=4 unique, 1 of 10 scanned", "measured": [len(e2["y_independent_at"]),
                                                                  len(e2["rows"])],
         "in_prose": "1 of 10 scanned" in prose,
         "consistent": e2["y_independent_at"] == [4.0] and len(e2["rows"]) == 10},
        {"claim": "spread 0.0500 at gamma = 3.9", "measured": g39["spread_over_y"],
         "in_prose": "0.0500 at gamma = 3.9" in prose,
         "consistent": abs(g39["spread_over_y"] - 0.05) < 5e-6},
        {"claim": "leg 165's D_phi(0) = (3-gamma)/2 reproduced", "measured":
            e2["leg_165_formula_reproduced"],
         "in_prose": "(3-gamma)/2" in prose,
         "consistent": e2["leg_165_formula_reproduced"] is True},
        # The prose quotes ONE value "over four grid extents", so the faithful check is against
        # the four-row set, not against any single row.  (An earlier version of this checker
        # compared to rows[-1] alone and reported a false FAIL -- recorded here because a
        # false positive from an auditor is the same defect class it audits.)
        {"claim": "err * S = 0.639 vs 2/pi = 0.6366, over four grid extents",
         "measured": {"n_extents": len(e3["rows"]),
                      "err_times_S": [round(r["err_times_S"], 4) for r in e3["rows"]],
                      "min": round(min(r["err_times_S"] for r in e3["rows"]), 4),
                      "max": round(max(r["err_times_S"] for r in e3["rows"]), 4)},
         "in_prose": "0.639" in prose and "0.6366" in prose and "four grid extents" in prose,
         "consistent": (len(e3["rows"]) == 4
                        and round(min(r["err_times_S"] for r in e3["rows"]), 3) == 0.639
                        and all(abs(r["err_times_S"] - 0.639) < 5e-3 for r in e3["rows"]))},
        {"claim": "negated target off by 2.0, pinning the sign convention",
         "measured": round(max(r["max_abs_err_vs_NEGATED_EGM"] for r in e3["rows"]), 3),
         "in_prose": "off by 2.0" in prose,
         "consistent": abs(max(r["max_abs_err_vs_NEGATED_EGM"] for r in e3["rows"]) - 2.0) < 1e-2},
    ]

    # And the ONE substantive claim: the bracket, and its slope in |a|.
    bracket_ok = "-(1/2 - C|a|)" in gap["statement_verbatim"]
    slope_ok = "DEGRADES with |a|" in gap["sign_correction_leg_190"]
    latex_ok = j["E4_transcription_audit"]["latex_source_verbatim"].replace("\\\\", "\\") \
        in gap["sign_correction_leg_190"].replace("\\\\", "\\")
    gap_val_ok = gap["gap_at_a_zero"] == -0.5 == j["E1_egm_constant"]["egm_printed_value"]

    return {
        "source": "writeup/data/p2_route_egml_v1_lit.json (leg 190's own banked report)",
        "method": "BYTE EQUALITY per field, not similarity",
        "header_fields": header_cmp,
        "header_all_identical": all(c["identical"] for c in header_cmp),
        "verbatim_fields": verb_cmp,
        "verbatim_all_present": all(c["in_ledger"] for c in verb_cmp),
        "verbatim_all_identical": all(c["identical"] for c in verb_cmp),
        "n_verbatim_fields": len(verb_cmp),
        "prose_fields": prose_cmp,
        "prose_all_identical": all(c["identical"] for c in prose_cmp),
        "numeric_claims": numeric_claims,
        "n_numeric_claims": len(numeric_claims),
        "n_numeric_traceable": sum(1 for c in numeric_claims
                                   if c["in_prose"] and c["consistent"]),
        "bracket_form_correct": bracket_ok,
        "slope_direction_correct": slope_ok,
        "latex_source_quoted_verbatim": latex_ok,
        "gap_at_a_zero_matches": gap_val_ok,
        "pass": (all(c["identical"] for c in header_cmp)
                 and all(c["identical"] for c in verb_cmp)
                 and all(c["identical"] for c in prose_cmp)
                 and all(c["in_prose"] and c["consistent"] for c in numeric_claims)
                 and bracket_ok and slope_ok and latex_ok and gap_val_ok),
    }


# =========================================================================
# A5.  TRANSCRIPTION -- the VNL row against leg 174's OWN banked JSON.
#
# Weaker instrument than A4 and deliberately so: leg 197 did not copy leg 174's fields, it
# WROTE a `what`/`dial`/`rigor` prose characterization from them.  So the check is substring
# containment of leg 174's own wording inside leg 197's row (leg 197's own check `C2`,
# re-run here independently rather than trusted).
# =========================================================================
def a5_transcription_vnl(precedents, appended_id="arXiv:2208.09445"):
    j = json.loads((ROOT / "writeup" / "data" / "p2_route_vbs_v1_scoping.json").read_text())
    src = [e for e in j["ledger"] if e.get("key") == "BCG-NS"]
    row = [p for p in precedents if p.get("id") == appended_id]
    if not src or not row:
        return {"pass": False, "fatal": "BCG-NS or the appended row is missing"}
    src, row = src[0], row[0]
    blob = _norm(json.dumps(row))
    src_blob = _norm(json.dumps(j))

    claims = [
        ("arXiv id matches leg 174's url", "2208.09445" in src["url"],
         "2208.09445" in row["id"]),
        ("authors verbatim", _norm("Buckmaster, Cao-Labora, Gomez-Serrano") in _norm(src["cite"]),
         _norm(row["who"]) == _norm("Buckmaster, Cao-Labora, Gomez-Serrano")),
        ("title verbatim", _norm("Smooth imploding solutions for 3D compressible fluids")
         in _norm(src["cite"]), _norm("Smooth imploding solutions for 3D compressible fluids")
         in blob),
        ("journal ref", "13 (2025) e6" in src["journal_ref"], "13 (2025) e6" in blob),
        ("doi", "10.1017/fmp.2024.12" in src["journal_ref"], "10.1017/fmp.2024.12" in blob),
        ("Theorem 1.3 locator", "Theorem 1.3" in src["locator"], "theorem 1.3" in blob),
        ("Grade B", src["certified_object_dissipative"] is False,
         row.get("grade") == "B" and "grade b" in blob),
        ("system (1.5) is the enclosed object",
         "system (1.5)" in src["why_not_certified_object_dissipative"], "system (1.5)" in blob),
        ("(1.5) is the ODE reduction of the INVISCID Euler system (1.3)",
         _norm("ODE reduction of the INVISCID compressible Euler system (1.3)")
         in _norm(src["why_not_certified_object_dissipative"]),
         _norm("ODE reduction of the INVISCID compressible Euler system (1.3)") in blob),
        ("sections 7-8 analytic stability",
         "sections 7-8" in src["why_not_certified_object_dissipative"], "sections 7-8" in blob),
        ("section 7 domination quote verbatim",
         _norm("we need to restrict the parameter r to a regime where the self-similar profile "
               "dominates the dissipation") in _norm(src["third_quote"]),
         _norm("in the Navier-Stokes case we need to restrict the parameter r to a regime where "
               "the self-similar profile dominates the dissipation") in blob),
        ("10000 coefficient pairs (W_j, Z_j)",
         _norm("10000 coefficient pairs (W_j, Z_j)") in _norm(src["second_quote"]),
         _norm("10000 Taylor coefficient pairs (W_j, Z_j)") in blob),
        ("~14 CPU-hours", "14 hours on a single CPU" in src["second_quote"],
         "14 hours on a single cpu" in blob),
        ("Lemmas A.27/A.28", "A.27/A.28" in src["why_computer_assistance_essential"],
         "a.27/a.28" in blob),
        ("Appendix B implementation details",
         _norm("Appendix B Implementation details of the computer-assisted part")
         in _norm(src["why_computer_assistance_essential"]),
         _norm("Appendix B 'Implementation details of the computer-assisted part'") in blob),
        ("Lame viscosities mu_1 > 0, 2 mu_1 + mu_2 > 0",
         "2 mu_1 + mu_2 > 0" in src["equation"], "2 mu_1 + mu_2 > 0" in blob),
        ("computer assistance essential/non-removable",
         src["computer_assistance_essential"] is True, "non-removable" in blob),
        ("density constant at infinity", "density constant at infinity" in src_blob,
         "density constant at infinity" in blob),
        ("banked_by names leg 174 / BCG-NS", True,
         "174" in str(row.get("banked_by", "")) and "BCG-NS" in str(row.get("banked_by", ""))),
        ("verdict EXCLUSION consistent with certified_object_dissipative=False",
         src["certified_object_dissipative"] is False, row["verdict"] == "EXCLUSION"),
    ]
    rows = [{"claim": c, "present_in_leg174": bool(a), "traceable_in_row": bool(b)}
            for c, a, b in claims]
    n_ok = sum(1 for r in rows if r["present_in_leg174"] and r["traceable_in_row"])
    return {
        "source": "writeup/data/p2_route_vbs_v1_scoping.json, ledger key BCG-NS (leg 174)",
        "method": "substring containment, normalised for whitespace/case",
        "n_claims": len(rows),
        "n_traceable": n_ok,
        "claims": rows,
        "untraceable": [r["claim"] for r in rows
                        if not (r["present_in_leg174"] and r["traceable_in_row"])],
        "pass": n_ok == len(rows),
    }


# =========================================================================
# A6.  POST-HOC STALENESS -- the fourth failure mode, and the one leg 214 creates.
#
# `EGM_PRIMARY_READ["spectral_gap"]["sign_correction_leg_190"]` names five prose sites and says,
# in the PRESENT TENSE, that they "all render the bracket as (-1/2 - C|a|)".  Leg 214 then
# corrected all five.  Nobody edited the ledger row, because an append-only discipline says the
# row's bytes are safe -- and they are.  What is not safe is the row's TRUTH.
#
# This check reads the five named sites out of the live tree and asks what they say NOW.
# =========================================================================
WRONG = "(-1/2 - C|a|)"          # the erroneous bracket, ASCII
RIGHT = "-(1/2 - C|a|)"          # the correct bracket, ASCII


def _canon(line):
    """Map the prose files' unicode math to the ledger's ASCII so the two are comparable."""
    return (line.replace("−", "-").replace("φ", "phi").replace("∫", "int")
                .replace("\\|", "|").replace("²", "2"))


def a6_staleness_after_leg_214(egm):
    field = egm["spectral_gap"]["sign_correction_leg_190"]
    sites = [
        ("experiments/journal/leg_141.md", 30),
        ("experiments/journal/leg_141.md", 117),
        ("writeup/novelty/leg_141.md", 233),
        ("experiments/journal/leg_165.md", 120),
        ("experiments/journal/leg_165.md", 128),
    ]
    rows = []
    for path, lineno in sites:
        p = ROOT / path
        txt = p.read_text().splitlines()
        line = _canon(txt[lineno - 1]) if 0 < lineno <= len(txt) else ""
        has_wrong = WRONG in line
        has_right = RIGHT in line
        rows.append({
            "site": f"{path}:{lineno}", "exists": p.exists(),
            "line": line.strip()[:200],
            "renders_wrong_bracket_parenthesised": has_wrong,
            "renders_right_bracket": has_right,
            # THE PREDICATE, and it is deliberately the ABSENCE of the correct form rather
            # than the presence of the parenthesised wrong one.  Leg 214's diff has TWO
            # shapes -- 3 relocated brackets in the verbatim blockquotes (sites 1, 3, 4) and
            # 2 FRESH pairs inserted on the inline constants (sites 2, 5), which carried no
            # parentheses at all before.  A predicate keyed to the literal "(-1/2 - C|a|)"
            # is blind at sites 2 and 5 in both directions and would measure the bracket
            # SHAPE instead of the claim.  What the ledger asserts is that the gap is
            # rendered as IMPROVING with |a| at all five, i.e. that the corrected form is
            # absent at all five.
            "ledger_claim_holds_at_this_site": not has_right,
        })
    n_still_wrong = sum(1 for r in rows if r["ledger_claim_holds_at_this_site"])
    n_now_right = sum(1 for r in rows if r["renders_right_bracket"])
    # The ledger's own sentence, quoted so the JSON carries what is being falsified.
    sentence = field[field.index("experiments/journal/leg_141.md"):
                     field.index("i.e. a gap IMPROVING")].strip()
    return {
        "ledger_field": "EGM_PRIMARY_READ['spectral_gap']['sign_correction_leg_190']",
        "ledger_sentence_under_test": sentence + "all render the bracket as (-1/2 - C|a|)",
        "tense": "present indicative -- 'all render', not 'rendered at leg 190'",
        "n_sites_named": len(rows),
        "sites": rows,
        "n_sites_still_carrying_the_error": n_still_wrong,
        "n_sites_now_corrected": n_now_right,
        "falsified_by": "leg 214 (Route-EGMB), commit 2c901c4, 5 lines / 5 ins / 5 del",
        "leg_214_declined_to_touch_literature_gates": True,
        # THE FINDING: 0 of 5 -- the sentence is now false at every site it names.
        "ledger_claim_holds_at_n_of_5": n_still_wrong,
        "banked_numbers_moved_by_this": 0,
        "why_it_matters": (
            "the field is the ledger's ONLY record of a three-leg propagated error and its "
            "repair.  Read today it points five readers at five files and tells each of them "
            "the file is wrong when it is right -- the exact inverse of the defect leg 190 "
            "created the field to record.  It is not a wrong NUMBER (0 move) and not a wrong "
            "CITATION; it is a wrong statement about this repository's own current state, in "
            "shared infrastructure, and it can only get staler."),
        "pass": n_still_wrong == len(rows),
    }


# =========================================================================
# A7.  NEGATIVE CONTROLS.  Each checker vs a deliberately corrupted structure.
# =========================================================================
def a7_controls():
    out = []

    # C1: A1 vs a block with a renamed header slot.
    bad = deepcopy(EGM_PRIMARY_READ)
    bad["author"] = bad.pop("authors")
    out.append({"control": "A1 / header slot 'authors' renamed to 'author'",
                "checker": "a1_format_literature_gates",
                "fired": not a1_format_literature_gates(bad, LSS_PRIMARY_READ)["pass"]})

    # C2: A1 vs the viscous_novelty citation convention leaking into literature_gates.
    bad = deepcopy(EGM_PRIMARY_READ)
    bad["arxiv"] = "arXiv:1906.05811"
    out.append({"control": "A1 / arXiv id carries the OTHER ledger's 'arXiv:' prefix",
                "checker": "a1_format_literature_gates",
                "fired": not a1_format_literature_gates(bad, LSS_PRIMARY_READ)["pass"]})

    # C3: A2 vs a row missing one of the seven schema keys.
    bad = deepcopy(list(PRECEDENTS))
    bad[-1] = {k: v for k, v in bad[-1].items() if k != "dial"}
    out.append({"control": "A2 / appended row loses its 'dial' key",
                "checker": "a2_format_viscous_novelty",
                "fired": not a2_format_viscous_novelty(bad)["pass"]})

    # C4: A2 vs an unprefixed id.
    bad = deepcopy(list(PRECEDENTS))
    bad[-1] = dict(bad[-1], id="2208.09445")
    out.append({"control": "A2 / appended row's id drops the 'arXiv:' prefix",
                "checker": "a2_format_viscous_novelty",
                "fired": not a2_format_viscous_novelty(bad, "2208.09445")["pass"]})

    # C5: A3 vs a genuine duplicate row.
    bad = list(deepcopy(list(PRECEDENTS)))
    bad.append(deepcopy(bad[-1]))
    out.append({"control": "A3 / the appended row duplicated verbatim",
                "checker": "a3_duplicates",
                "fired": not a3_duplicates(bad, EGM_PRIMARY_READ, LSS_PRIMARY_READ,
                                           CLAIM_LEDGER)["pass"]})

    # C6: A3 vs a duplicate that DISAGREES -- the one that would move the gate.
    bad = list(deepcopy(list(PRECEDENTS)))
    bad.append(dict(deepcopy(bad[-1]), verdict="PRE_EMPTS"))
    r = a3_duplicates(bad, EGM_PRIMARY_READ, LSS_PRIMARY_READ, CLAIM_LEDGER)
    out.append({"control": "A3 / duplicate row with a CONFLICTING verdict",
                "checker": "a3_duplicates",
                "fired": not r["pass"] and bool(r["verdict_conflicts_same_paper"])})

    # C7: A4 vs a one-word paraphrase of a verbatim field.
    bad = deepcopy(EGM_PRIMARY_READ)
    bad["spectral_gap"] = dict(bad["spectral_gap"])
    bad["spectral_gap"]["weight_verbatim"] = \
        bad["spectral_gap"]["weight_verbatim"].replace("origin exponent", "origin power")
    out.append({"control": "A4 / two words changed inside a *_verbatim field",
                "checker": "a4_transcription_egm",
                "fired": not a4_transcription_egm(bad)["pass"]})

    # C8: A4 vs the SIGN flipped back -- the defect the whole field exists to record.
    bad = deepcopy(EGM_PRIMARY_READ)
    bad["spectral_gap"] = dict(bad["spectral_gap"])
    bad["spectral_gap"]["statement_verbatim"] = \
        bad["spectral_gap"]["statement_verbatim"].replace(RIGHT, WRONG)
    out.append({"control": "A4 / bracket reverted to the erroneous (-1/2 - C|a|)",
                "checker": "a4_transcription_egm",
                "fired": not a4_transcription_egm(bad)["pass"]})

    # C9: A4 vs a numeric claim inflated in the prose.
    bad = deepcopy(EGM_PRIMARY_READ)
    bad["re_derived_at_leg_190"] = bad["re_derived_at_leg_190"].replace("4000 nodes", "40000 nodes")
    out.append({"control": "A4 / node count in the prose inflated 4000 -> 40000",
                "checker": "a4_transcription_egm",
                "fired": not a4_transcription_egm(bad)["pass"]})

    # C10: A5 vs a paraphrased quote -- the drift leg 145 actually found three of.
    bad = deepcopy(list(PRECEDENTS))
    bad[-1] = dict(bad[-1], what=bad[-1]["what"].replace(
        "the self-similar profile dominates the dissipation",
        "the profile is larger than the dissipation"))
    out.append({"control": "A5 / section-7 quote paraphrased rather than transcribed",
                "checker": "a5_transcription_vnl",
                "fired": not a5_transcription_vnl(bad)["pass"]})

    # C11: A5 vs a grade flip contradicting leg 174.
    bad = deepcopy(list(PRECEDENTS))
    bad[-1] = dict(bad[-1], grade="A")
    out.append({"control": "A5 / Grade B upgraded to A against leg 174's finding",
                "checker": "a5_transcription_vnl",
                "fired": not a5_transcription_vnl(bad)["pass"]})

    # C12: A6 -- can the staleness checker come out the OTHER way?  Run it against a ledger
    # field naming five sites that DO still carry the error (a synthetic file this leg writes
    # nowhere -- instead, re-run the same predicate against the pre-leg-214 blobs from git).
    import subprocess
    fired, detail = None, {}
    pre_sites = {"experiments/journal/leg_141.md": [30, 117],
                 "writeup/novelty/leg_141.md": [233],
                 "experiments/journal/leg_165.md": [120, 128]}
    try:
        held = []
        for path, linenos in pre_sites.items():
            pre = subprocess.run(["git", "show", f"2c901c4^:{path}"],
                                 cwd=ROOT, capture_output=True, text=True, timeout=60)
            if pre.returncode != 0:
                raise RuntimeError(f"git show failed for {path}")
            lines = pre.stdout.splitlines()
            for n in linenos:
                ln = _canon(lines[n - 1])
                held.append({"site": f"{path}:{n}",
                             "ledger_claim_held_before_leg_214": RIGHT not in ln})
        detail = {"pre_leg_214_sites": held,
                  "n_held_before": sum(1 for h in held
                                       if h["ledger_claim_held_before_leg_214"])}
        # The control fires iff the SAME predicate returns the OPPOSITE answer before the
        # commit that is alleged to have falsified it: 5/5 held before, 0/5 hold after.
        fired = detail["n_held_before"] == 5
    except Exception as exc:      # pragma: no cover -- reported, never swallowed
        detail = {"error": repr(exc)}
        fired = False
    out.append({"control": "A6 / same predicate against the PRE-leg-214 blobs "
                           "(git show 2c901c4^ at all five sites)",
                "checker": "a6_staleness_after_leg_214",
                "note": "the predicate must report the ledger's claim TRUE before leg 214 and "
                        "FALSE after; if it said FALSE at both times it would be measuring "
                        "nothing about leg 214, and the staleness finding would be an artifact "
                        "of the predicate rather than a fact about the commit",
                "detail": detail, "fired": bool(fired)})

    n_fired = sum(1 for c in out if c["fired"])
    return {"n_controls": len(out), "n_fired": n_fired,
            "ornaments": [c["control"] for c in out if not c["fired"]],
            "controls": out, "pass": n_fired == len(out)}


def main():
    t0 = time.time()
    A1 = a1_format_literature_gates(EGM_PRIMARY_READ, LSS_PRIMARY_READ)
    A2 = a2_format_viscous_novelty(PRECEDENTS)
    A3 = a3_duplicates(PRECEDENTS, EGM_PRIMARY_READ, LSS_PRIMARY_READ, CLAIM_LEDGER)
    A4 = a4_transcription_egm(EGM_PRIMARY_READ)
    A5 = a5_transcription_vnl(PRECEDENTS)
    A6 = a6_staleness_after_leg_214(EGM_PRIMARY_READ)
    A7 = a7_controls()

    # THE GATE.  Its three named clauses are A1+A2 (format), A3 (duplicate/conflict),
    # A4+A5 (transcription drift).  A6 is the fourth mode, outside the gate's wording; it is
    # reported separately and its effect on the branch is stated explicitly rather than
    # folded in silently.
    gate_clauses = {
        "format_literature_gates": A1["pass"],
        "format_viscous_novelty": A2["pass"],
        "no_duplicate_or_conflict": A3["pass"],
        "no_transcription_drift_190": A4["pass"],
        "no_transcription_drift_197": A5["pass"],
    }
    gate_as_worded = all(gate_clauses.values())
    stale = not A6["pass"]

    answer = "YES" if (gate_as_worded and not stale) else "NO"

    out = {
        "route": "LGC2 v1", "leg": 213,
        "gate": ("Do the 190 and 197 rows match literature_gates.py's and viscous_novelty.py's "
                 "own existing row format exactly, with no duplicate/conflicting entry and no "
                 "transcription drift from legs 190's/197's own banked reports?"),
        "A1_format_literature_gates": A1,
        "A2_format_viscous_novelty": A2,
        "A3_duplicates_conflicts": A3,
        "A4_transcription_egm_vs_leg190": A4,
        "A5_transcription_vnl_vs_leg174": A5,
        "A6_post_hoc_staleness_leg214": A6,
        "A7_negative_controls": A7,
        "gate_clauses_as_worded": gate_clauses,
        "gate_as_worded_clean": gate_as_worded,
        "fourth_mode_staleness_found": stale,
        "gate_answer": answer,
        "escalation": None if answer == "YES" else {
            "what": "EGM_PRIMARY_READ['spectral_gap']['sign_correction_leg_190'] is STALE",
            "where": "solver/literature_gates.py, inside the leg-190 block",
            "class": "post-hoc staleness -- NOT format drift, NOT a duplicate, NOT a "
                     "transcription error against leg 190's own report (A1-A5 are all clean)",
            "measured": f"{A6['ledger_claim_holds_at_n_of_5']} of 5 named sites still carry "
                        f"the bracket the field says they all carry; "
                        f"{A6['n_sites_now_corrected']} of 5 now carry the corrected form",
            "cause": "leg 214 (2c901c4) corrected all five prose sites and deliberately left "
                     "literature_gates.py untouched, on the correct ground that leg 190's row "
                     "states the MATHEMATICS correctly. The mathematics is correct. The "
                     "sentence about the repository's own files is not.",
            "banked_numbers_moved": 0,
            "not_reconciled_here": "solver/literature_gates.py is read-only to leg 213 under "
                                   "both branches; the fix is one tense change and it belongs "
                                   "to whoever owns the ledger, not to its auditor.",
            "suggested_repair_not_applied": "re-tense the sentence to '...rendered the bracket "
                                            "as (-1/2 - C|a|) until leg 214 (2c901c4) corrected "
                                            "all five', which leaves every other word intact.",
        },
        "what_did_NOT_move": (
            "no verdict in CLAIM_LEDGER moves; novelty_verdict() returns "
            f"{A3['novelty_verdict_now']} on arXiv:2410.05480 alone, unchanged; 0 banked "
            "numbers move; EGM's -1/2 at a = 0 and BCG's Grade B both stand exactly as legs "
            "190 and 174 banked them.  No ban lifts, no route advances, no figure owed."),
        "elapsed_s": round(time.time() - t0, 3),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n")

    print("ROUTE-LGC2 v1 (leg 213) -- post-append ledger consistency audit")
    print(f"  A1 format literature_gates (EGM vs LSS template) : {'PASS' if A1['pass'] else 'FAIL'}")
    print(f"  A2 format viscous_novelty  (row vs 6 priors)     : {'PASS' if A2['pass'] else 'FAIL'}"
          f"   [{A2['n_rows']} rows, extra keys on {len(A2['rows_with_extra_keys'])}]")
    print(f"  A3 duplicates / conflicts                        : {'PASS' if A3['pass'] else 'FAIL'}"
          f"   [{A3['n_unique']}/{len(A3['viscous_novelty_ids'])} unique ids, "
          f"verdict {A3['novelty_verdict_now']}]")
    print(f"  A4 transcription 190 (byte equality)             : {'PASS' if A4['pass'] else 'FAIL'}"
          f"   [{A4['n_verbatim_fields']}/{A4['n_verbatim_fields']} verbatim fields identical, "
          f"{A4['n_numeric_traceable']}/{A4['n_numeric_claims']} numerics traceable]")
    print(f"  A5 transcription 197 (containment)               : {'PASS' if A5['pass'] else 'FAIL'}"
          f"   [{A5['n_traceable']}/{A5['n_claims']} claims traceable]")
    print(f"  A6 post-hoc staleness after leg 214              : {'PASS' if A6['pass'] else 'FAIL'}"
          f"   [ledger claim holds at {A6['ledger_claim_holds_at_n_of_5']}/5 named sites]")
    print(f"  A7 negative controls fired                       : "
          f"{A7['n_fired']}/{A7['n_controls']}"
          + ("" if A7["pass"] else f"   ORNAMENTS: {A7['ornaments']}"))
    print(f"  gate as worded (A1,A2,A3,A4,A5)                  : "
          f"{'CLEAN' if gate_as_worded else 'NOT CLEAN'}")
    print(f"  GATE ANSWER: {answer}")
    if answer == "NO":
        print(f"  ESCALATE: {out['escalation']['what']}")
        print(f"            {out['escalation']['measured']}")
    print(f"  wrote {OUT.relative_to(ROOT)}  ({out['elapsed_s']}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
