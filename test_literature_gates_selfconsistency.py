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
  (6) THE FIX IS PINNED TO THE MODULE'S CURRENT TEXT -- INVERTED FROM LEG 145's ORIGINAL
      GATE.  Leg 145 found three rows drifted and wrote a pin asserting the drift was
      STILL THERE (deliberately: its gate answered NO and the finding was escalated, not
      patched, so its audit record would fail loudly the moment anyone touched the
      module).  "Leg 0: BENCH -- fix-literature-gates-citation-drift" is that repair, and
      this gate is now the mirror image: it asserts each of the three drifts is ABSENT
      and the corrected text is PRESENT, quoting the exact strings.  It fails loudly if
      the fix is ever reverted or the same drift is reintroduced under different wording.
      All 12 verdicts are additionally pinned unchanged (0 of 12 changed by this repair).

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
    ARXIV_METADATA, FORMER_DRIFT, QUOTES, check_no_phantom_citations, check_repair_status,
    check_source_resolution, check_transcribed_numbers, control_results,
)

DATA = ROOT / "writeup" / "data" / "p2_route_lga_v1_ledger.json"
LG_SRC = (ROOT / "solver" / "literature_gates.py").read_text()

# The two rows that legitimately do not resolve, named so a NEW one cannot hide.  Row 12's
# source string changed with the provenance fix (leg 45's read is now correctly recorded)
# but it still does not resolve to a PRIMARY_SOURCES entry -- 2302.12877 is Tier 2 and
# PRIMARY_SOURCES only describes Tier 1 -- so it stays in this set under its NEW text.
KNOWN_UNRESOLVED = {
    "not found in Tier 1": "NAMES_NO_SOURCE",
    "2302.12877 (Tier 2, fetched, read closely at leg 45)": "ID_NOT_IN_PRIMARY_SOURCES",
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
    assert len(QUOTES) == 14, len(QUOTES)
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


def test_6_drift_is_repaired_and_pinned_against_recurrence():
    """INVERTED from leg 145's original pin (which asserted the drift was STILL there).

    "Leg 0: BENCH -- fix-literature-gates-citation-drift" repaired all three rows and
    changed 0 of 12 verdicts.  This gate is the regression test that would have caught
    the original drift, run in reverse: it asserts the corrected text is PRESENT and the
    original wrong text is ABSENT, so a future edit that reintroduces the same drift (by
    reverting the fix, or by copy-pasting the old wording back in) fails loudly here.
    """
    assert len(FORMER_DRIFT) == 3, len(FORMER_DRIFT)
    assert sum(1 for d in FORMER_DRIFT if d["verdict_changes"]) == 0, "no verdict changes"
    assert all(d.get("repaired") for d in FORMER_DRIFT), "FORMER_DRIFT record out of date"

    by_kind = {d["kind"]: d for d in FORMER_DRIFT}
    assert set(by_kind) == {"LOCATOR_UNDER-SUPPORTS_NOTE", "FALSE_NEGATIVE_ABOUT_A_SOURCE",
                            "STALE_PROVENANCE"}, set(by_kind)

    # (i) the Theorem 2 / Theorem 3 misattribution -- must now be REPAIRED
    spec = [c for c in CLAIM_LEDGER if "isolated eigenvalues" in c["claim"]]
    assert len(spec) == 1, spec
    spec = spec[0]
    assert "Theorem 2" in spec["source"] and "Theorem 3" in spec["source"], spec["source"]
    assert spec["source"] != "2607.19762 Theorem 2", (
        "the old under-attributed source string is back -- drift regressed")
    assert "no embedded eigenvalues" in spec["note"], spec["note"]
    assert "Theorem 2:" in spec["note"] and "Theorem 3" in spec["note"], (
        "the note no longer attributes each fact to the theorem that states it")
    assert spec["verdict"] == "CONFIRMED_AND_PRE-EMPTED", spec["verdict"]

    # the same site in the module docstring must carry the corrected attribution
    assert "Theorem 2: the full point spectrum" not in LG_SRC, (
        "docstring drift regressed -- Theorem 2 is once again over-attributed")
    assert "Theorem 3 extends this to the FULL point" in LG_SRC, (
        "docstring no longer attributes the full point spectrum to Theorem 3")

    # (ii) the false negative about XU -- must now say XU DOES have the sigma=3 result,
    #      corroborated by this same module's OWN transcription of XU Table 1 (a=0.5 row)
    marg = [c for c in CLAIM_LEDGER if "0.133683" in c["claim"]]
    assert len(marg) == 1, marg
    assert "not in ALS and not in XU" not in marg[0]["note"], (
        "the false-negative wording about XU is back -- drift regressed")
    assert "XU DOES record" in marg[0]["note"] or "XU DOES record the" in marg[0]["note"], (
        marg[0]["note"])
    assert marg[0]["verdict"] == "UNSEARCHED_AT_PRIMARY_SOURCE", marg[0]["verdict"]
    a_half = [r for r in XU_TABLE1 if abs(r[0] - 0.5) < 1e-9]
    assert len(a_half) == 1 and abs(a_half[0][2] - 3.0) < 1e-3, a_half
    assert abs(a_half[0][1] - 1.0 / 3.0) < 1e-3, a_half

    # (iii) the stale provenance parenthetical -- must now match MANIFEST.md/LITERATURE_CHECK.md
    trap = [c for c in CLAIM_LEDGER if "discrete-ball trap" in c["claim"]]
    assert len(trap) == 1, trap
    assert trap[0]["source"] == "2302.12877 (Tier 2, fetched, read closely at leg 45)", trap[0]
    assert "NOT read closely" not in trap[0]["source"], "stale provenance regressed"
    assert trap[0]["verdict"] == "UNSEARCHED_AT_PRIMARY_SOURCE", trap[0]["verdict"]
    manifest = (ROOT / "Papers" / "MANIFEST.md").read_text()
    assert "2302.12877" in manifest and "leg 45" in manifest.lower(), (
        "MANIFEST.md no longer corroborates the leg-45 read -- re-check provenance")

    # blast radius: every named site must still exist; the module's own sites must no
    # longer carry the drift, and the live dynamic check must agree
    for d in FORMER_DRIFT:
        assert d["blast_radius"], d["kind"]
        for site in d["blast_radius"]:
            f = site["site"].split(":")[0].split(" ")[0]
            assert (ROOT / f).exists(), f
            if f == "solver/literature_gates.py":
                assert not site["carries_drift"], (
                    f"{site['site']} still marked as carrying drift after the bench fix")
    rep = check_repair_status(CLAIM_LEDGER, LG_SRC)
    assert rep["all_repaired"], rep
    remaining_carriers = sum(1 for d in FORMER_DRIFT for s in d["blast_radius"]
                             if s["carries_drift"])
    assert remaining_carriers == 4, remaining_carriers  # sites outside solver/literature_gates.py
    print(f"  3/3 drift rows repaired in solver/literature_gates.py, 0 verdicts changed, "
          f"live repair check all_repaired={rep['all_repaired']}; {remaining_carriers} "
          f"carrier sites remain outside this bench fix's declared territory  OK")


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
    assert d["L6_former_drift"]["n_former_drift_rows"] == 3
    assert d["L6_former_drift"]["n_verdicts_changed"] == 0
    assert d["L6_former_drift"]["repair_status"]["all_repaired"] is True
    assert d["L7_gate"]["answer"].startswith("YES"), d["L7_gate"]["answer"]
    print(f"  committed JSON agrees with a fresh call: 10/12 resolved, 0 phantom, "
          f"{q['n_found_verbatim']}/{q['n_recheckable_this_run']} quotes relocated, 3 former "
          f"drift rows all repaired  OK")


if __name__ == "__main__":
    import time
    t0 = time.time()
    fails = 0
    for fn in (test_1_source_resolution,
               test_2_no_phantom_citations,
               test_3_transcribed_numbers,
               test_4_quote_record_is_well_formed,
               test_5_negative_controls_fire,
               test_6_drift_is_repaired_and_pinned_against_recurrence,
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
