"""Leg 145 / ROUTE-LGA: the LEDGER SELF-CONSISTENCY gates for solver/literature_gates.py.

This is the companion to `test_literature_gates.py`, not a replacement.  That file gates
the module's NUMBERS -- it re-derives Schochet's constant, Route-H's (E), alpha(1/2) = 3 and
the supercritical balance from the published equations.  This file gates the module's PROSE:
the twelve `CLAIM_LEDGER` rows that say what each published paper did to a standing novelty
claim.  A wrong row corrupts no computation and moves no number; it misreports a citation,
and every leg that quotes the row inherits the misreport silently.

  (1) SOURCE RESOLUTION.  Every row's `source` must name a paper this project has actually
      indexed -- by arXiv id or by the tag PRIMARY_SOURCES itself defines.  The two rows
      that do not are named here EXPLICITLY, so a thirteenth unresolved row fails this gate
      instead of joining an anonymous count.  `test_literature_gates.py` cannot see this:
      its `test_8_ledger_does_not_rot` asserts `source` is a non-empty string and stops.
  (2) NO PHANTOM CITATIONS.  Every arXiv id the ledger cites has real metadata, and for the
      four papers PRIMARY_SOURCES also DESCRIBES, the stored authors and title match what
      arxiv.org returns.  Read live 2026-08-06 and frozen into the runner, because a check
      that needs egress decays at the rate of the network (banked lesson 68).
  (3) THE TRANSCRIBED NUMBERS.  `XU_TABLE1`, `XU_S2_BOUNDARY`, the a_c pair and the
      Chen-Hou pair are TRANSCRIPTIONS, which the module says plainly.  Transcription is
      where errors hide, so each is checked against the others and against XU's own table.
  (4) THE QUOTE RECORD IS WELL-FORMED.  Thirteen verbatim sentences, each with an arXiv id
      and a locator, and each `find` anchor must be a substring of its own `quote` -- so the
      anchor the runner searches for is provably the sentence the human reads.
  (5) THE NEGATIVE CONTROLS FIRE.  A fabricated arXiv id and a source naming no paper must
      both be CAUGHT.  Without this the resolution gate would be an ornament that cannot
      come out differently (banked lesson 90).
  (6) THE DRIFT CENSUS IS PINNED TO THE MODULE'S CURRENT TEXT.  Two rows drift.  This gate
      asserts the drift is STILL THERE, quoting the exact strings that carry it.  That is
      deliberate: leg 145's gate answered NO and the finding is ESCALATED, not patched, so
      the audit record must fail loudly the moment someone repairs the module -- which is
      the signal to re-run the audit rather than to inherit a stale clean bill.

Run: .venv/bin/python test_literature_gates_selfconsistency.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "experiments"))

from solver.literature_gates import (  # noqa: E402
    CHEN_HOU_BETA, CHEN_HOU_CL_OVER_COMEGA, CLAIM_LEDGER, LSS_A_C, PRIMARY_SOURCES,
    XU_A_C_RECOMPUTED, XU_S2_BOUNDARY, XU_TABLE1,
)
from p2_route_lga_v1_ledger import (  # noqa: E402
    ARXIV_METADATA, DRIFT, QUOTES, check_no_phantom_citations, check_source_resolution,
    check_transcribed_numbers, control_results,
)

DATA = ROOT / "writeup" / "data" / "p2_route_lga_v1_ledger.json"

# The two rows that legitimately do not resolve, named so a NEW one cannot hide.
KNOWN_UNRESOLVED = {
    "not found in Tier 1": "NAMES_NO_SOURCE",
    "2302.12877 (Tier 2, fetched, NOT read closely)": "ID_NOT_IN_PRIMARY_SOURCES",
}


def test_1_source_resolution():
    rows = check_source_resolution(CLAIM_LEDGER, PRIMARY_SOURCES)
    assert len(rows) == len(CLAIM_LEDGER) == 12, len(rows)
    unresolved = {r["source"]: r["status"] for r in rows if r["status"] != "RESOLVED"}
    assert unresolved == KNOWN_UNRESOLVED, unresolved
    resolved = [r for r in rows if r["status"] == "RESOLVED"]
    by_id = sum(1 for r in resolved if r["resolved_via"] == "arxiv_id")
    by_tag = sum(1 for r in resolved if r["resolved_via"] == "tag")
    assert by_id + by_tag == 10, (by_id, by_tag)
    print(f"  {len(resolved)}/12 rows resolve ({by_id} by arXiv id, {by_tag} by tag); the 2 "
          f"that do not are the two known ones, named  OK")


def test_2_no_phantom_citations():
    rows = check_no_phantom_citations(CLAIM_LEDGER, PRIMARY_SOURCES)
    assert rows, "the ledger cites no arXiv id at all -- that is itself a failure"
    phantom = [r["arxiv"] for r in rows if not r["has_arxiv_metadata"]]
    assert not phantom, phantom
    described = [r for r in rows if r["declared_in_primary_sources"]]
    assert len(described) == 4, len(described)
    for r in described:
        assert r["authors_match"], (r["arxiv"], r["stored_authors"], r["real_authors"])
        assert r["title_match"], r["arxiv"]
    # every declared primary source must also be REACHED by the ledger
    assert set(PRIMARY_SOURCES) <= set(ARXIV_METADATA), "a declared source has no metadata"
    print(f"  {len(rows)} distinct ids cited, 0 phantom; {len(described)}/4 described sources "
          f"match arXiv title AND author list exactly  OK")


def test_3_transcribed_numbers():
    n = check_transcribed_numbers()
    # XU Table 1's own internal identity s* = 1/c_l, at XU's stated accuracy (~3 s.f.)
    assert n["worst_rel_s_star_vs_inv_cl"] < 2e-3, n["worst_rel_s_star_vs_inv_cl"]
    assert len(n["table_rows"]) == len(XU_TABLE1) == 8
    # c_l must decrease monotonically along the branch
    cls = [r[1] for r in XU_TABLE1]
    assert cls == sorted(cls, reverse=True), cls
    # the s = 2 boundary: stored 0.39 is XU's headline, and inverting XU's OWN table
    # linearly must land on XU's own parenthetical 0.386
    assert abs(n["s2_boundary_from_table_linear"] - 0.386) < 5e-3, n
    assert abs(n["s2_boundary_stored"] - n["s2_boundary_from_table_linear"]) < 1e-2, n
    # the a_c pair: XU's recompute must be the more accurate of the two, ~0.04%
    assert 3e-4 < n["xu_a_c_rel_err_vs_lss"] < 5e-4, n["xu_a_c_rel_err_vs_lss"]
    assert LSS_A_C > XU_A_C_RECOMPUTED
    # the Chen-Hou pair is one number stored twice with opposite sign
    assert n["chen_hou_pair_consistent"], (CHEN_HOU_BETA, CHEN_HOU_CL_OVER_COMEGA)
    print(f"  XU Table 1 s* = 1/c_l to {n['worst_rel_s_star_vs_inv_cl']:.1e} over 8 rows; "
          f"s=2 boundary inverts to {n['s2_boundary_from_table_linear']:.4f} vs XU's own "
          f"0.386; a_c recompute {n['xu_a_c_rel_err_vs_lss']:.2%}  OK")


def test_4_quote_record_is_well_formed():
    assert len(QUOTES) == 13, len(QUOTES)
    for q in QUOTES:
        assert q["arxiv"] in ARXIV_METADATA, q["arxiv"]
        assert q["locator"] and q["quote"] and q["find"] and q["supports"]
        # the anchor must be verbatim inside the quote a human can read
        assert q["find"] in q["quote"], (q["row_claim_key"], q["find"])
        assert len(q["quote"]) > 30, q["row_claim_key"]
    papers = {q["arxiv"] for q in QUOTES}
    assert papers == set(PRIMARY_SOURCES), papers
    print(f"  {len(QUOTES)} located quotes spanning all {len(papers)} Tier-1 sources; every "
          f"search anchor is a substring of its own quote  OK")


def test_5_negative_controls_fire():
    rows = control_results()
    named = {r["control"]: r["caught"] for r in rows}
    assert named["phantom_arxiv_id"] is True, named
    assert named["source_with_no_identifier"] is True, named
    # the quote control needs the PDF; when absent it is None and must NOT read as passed
    assert named["mutated_quote_anchor"] in (True, None), named
    if named["mutated_quote_anchor"] is None:
        print("  2/2 offline controls fire; quote control NOT RUN (PDF absent, not a pass) OK")
    else:
        print("  3/3 controls fire: a fabricated id, a sourceless row and a one-word quote "
              "mutation are all CAUGHT  OK")


def test_6_drift_census_is_pinned_to_the_module_text():
    """The audit answered NO and was escalated, not patched.  Pin the exact drift.

    If someone repairs `literature_gates.py`, these assertions fail -- on purpose.  That
    failure means "leg 145's audit record is now stale, re-run it", not "the module broke".
    """
    assert len(DRIFT) == 2, len(DRIFT)
    assert sum(1 for d in DRIFT if d["verdict_changes"]) == 0, "no verdict changes"

    by_kind = {d["kind"]: d for d in DRIFT}
    assert set(by_kind) == {"LOCATOR_UNDER-SUPPORTS_NOTE", "STALE_PROVENANCE"}, set(by_kind)

    # (i) the Theorem 2 / Theorem 3 misattribution, still present
    spec = [c for c in CLAIM_LEDGER if "isolated eigenvalues" in c["claim"]]
    assert len(spec) == 1, spec
    spec = spec[0]
    assert spec["source"] == "2607.19762 Theorem 2", spec["source"]
    assert "Point spectrum exactly {0,1}" in spec["note"], spec["note"]
    assert "no embedded eigenvalues" in spec["note"], spec["note"]
    assert "Theorem 3" not in spec["source"] and "Theorem 3" not in spec["note"], (
        "the module now cites Theorem 3 -- the drift may be repaired; re-run the audit")
    assert spec["verdict"] == "CONFIRMED_AND_PRE-EMPTED", spec["verdict"]

    # the same drift in the module docstring
    src = (ROOT / "solver" / "literature_gates.py").read_text()
    assert "Theorem 2: the full point spectrum" in src, (
        "docstring drift repaired -- re-run the audit")

    # (ii) the stale provenance parenthetical, still present
    trap = [c for c in CLAIM_LEDGER if "discrete-ball trap" in c["claim"]]
    assert len(trap) == 1, trap
    assert trap[0]["source"] == "2302.12877 (Tier 2, fetched, NOT read closely)", trap[0]
    assert trap[0]["verdict"] == "UNSEARCHED_AT_PRIMARY_SOURCE", trap[0]["verdict"]

    # blast radius: every named site must still exist
    for d in DRIFT:
        assert d["blast_radius"], d["kind"]
        for site in d["blast_radius"]:
            f = site["site"].split(":")[0].split(" ")[0]
            assert (ROOT / f).exists(), f
    carriers = sum(1 for d in DRIFT for s in d["blast_radius"] if s["carries_drift"])
    assert carriers == 7, carriers
    print(f"  2 drift rows still present verbatim, 0 verdicts changed, {carriers} quote sites "
          f"carry them; LITERATURE_CHECK.md's own Thm-2 row is correct and excluded  OK")


def test_7_artifact_matches_a_fresh_call():
    if not DATA.exists():
        print("  SKIP -- run experiments/p2_route_lga_v1_ledger.py first")
        return
    d = json.loads(DATA.read_text())
    assert d["leg"] == 145 and d["route"] == "ROUTE-LGA"
    assert d["edits_to_the_audited_module"] == 0
    assert d["L1_source_resolution"]["n_rows"] == len(CLAIM_LEDGER)
    assert d["L1_source_resolution"]["n_rows_resolving_to_primary_sources"] == 10
    assert d["L2b_phantom_citation_check"]["n_phantom"] == 0
    assert d["L2b_phantom_citation_check"]["n_distinct_ids_cited"] == 5
    assert d["L4_quote_relocation"]["n_quotes"] == len(QUOTES)
    # every quote that was recheckable on the recorded run was found
    q = d["L4_quote_relocation"]
    assert q["n_found_verbatim"] == q["n_recheckable_this_run"], q
    assert d["L6_drift"]["n_drift_rows"] == 2
    assert d["L6_drift"]["n_verdicts_changed"] == 0
    assert d["L7_gate"]["answer"] == "NO"
    print(f"  committed JSON agrees with a fresh call: 10/12 resolved, 0 phantom, "
          f"{q['n_found_verbatim']}/{q['n_recheckable_this_run']} quotes relocated, 2 drift "
          f"rows  OK")


if __name__ == "__main__":
    import time
    t0 = time.time()
    fails = 0
    for fn in (test_1_source_resolution,
               test_2_no_phantom_citations,
               test_3_transcribed_numbers,
               test_4_quote_record_is_well_formed,
               test_5_negative_controls_fire,
               test_6_drift_census_is_pinned_to_the_module_text,
               test_7_artifact_matches_a_fresh_call):
        print(f"\n{fn.__name__}")
        try:
            fn()
        except AssertionError as exc:
            fails += 1
            print(f"  FAIL: {exc}")
    if fails:
        print(f"\n{fails} GATE(S) FAILED ({time.time() - t0:.0f}s)")
        sys.exit(1)
    print(f"\nALL GATES PASS ({time.time() - t0:.0f}s)")
