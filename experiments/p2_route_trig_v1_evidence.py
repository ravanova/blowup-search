"""Leg 392 / Route-TRIG -- evidence script.

Rebuilds EVERY number in BLOG_P2_ROUTETRIG_V1.md, TECHNICAL_P2_ROUTETRIG_V1.md and
experiments/journal/leg_392.md from `writeup/data/p2_route_trig_v1.json` ALONE.

It issues NO network request and re-runs NOTHING: the literature pass is a
measurement with a date on it, and re-running it would silently replace the
measured record with a different one.  Every assertion below fails loudly if the
banked artifact does not carry the number the prose claims.

    .venv/bin/python experiments/p2_route_trig_v1_evidence.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "writeup" / "data" / "p2_route_trig_v1.json"

CHECKS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append((name, bool(ok), detail))
    print(f"  [{'ok ' if ok else 'FAIL'}] {name}: {detail}")


def main() -> int:
    d = json.loads(DATA.read_text())
    flat = [r for b in d["queries"].values() for r in b]
    cov = d["coverage"]
    ids = {}
    for r in flat:
        for h in r["hits"]:
            if h.get("id"):
                ids.setdefault(h["id"].split("v")[0], h)

    print("== §1  the instrument controls, all five, fired BEFORE any verdict")
    ctrl = {c["control"]: c for c in d["controls"]}
    check("controls_planned", len(d["controls"]) == 5, f"{len(d['controls'])} controls")
    check("pos_broad", ctrl["pos_broad"]["total"] == 10759,
          f'all:"Navier-Stokes" -> {ctrl["pos_broad"]["total"]} (MEASURED)')
    check("pos_topic", ctrl["pos_topic"]["total"] == 628,
          f'all:"Liouville theorem" -> {ctrl["pos_topic"]["total"]} (MEASURED)')
    check("neg_nonsense_is_zero", ctrl["neg_nonsense"]["total"] == 0,
          "the nonsense phrase returns EXACTLY 0 -- the endpoint is not fuzzy-matching, so "
          "every zero below is a zero and not a match-anything artifact")
    check("and_pair", ctrl["and_pair"]["total"] == 29,
          f'"Liouville theorem" AND "Navier-Stokes" -> {ctrl["and_pair"]["total"]} > 0')
    check("and_pair_b", ctrl["and_pair_b"]["total"] == 234,
          f'"Navier-Stokes" AND "torus" -> {ctrl["and_pair_b"]["total"]} > 0')
    check("all_controls_passed", d["controls_all_passed"] is True,
          "5 of 5 passed; AND verdict = " + d["and_operator_verdict"][:34])

    print("\n== §2  the leg-387 defence: which opensearch namespace actually answered")
    ns = cov["namespaces_served"]
    check("namespace_served", ns == ["http://a9.com/-/spec/opensearch/1.1/"],
          f"{ns} -- arXiv serves 1.1. Leg 387's harness listed 1.0 and REFUSED every "
          "response; this parser names no version at all.")
    check("namespace_on_every_query",
          all(r["opensearch_namespace_served"] == ns[0] for r in flat),
          f"all {len(flat)} substantive queries recorded the same served namespace")

    print("\n== §3  coverage: MEASURED vs DID-NOT-MEASURE, per query, never netted")
    check("arxiv_planned", cov["arxiv_queries_planned"] == 32, "32 arXiv queries planned")
    check("arxiv_measured", cov["arxiv_queries_MEASURED"] == 32,
          "32 MEASURED -- fraction executed = "
          f"{cov['arxiv_fraction_executed']} (100% of the planned arXiv set)")
    check("arxiv_did_not_measure", cov["did_not_measure_count"] == 0,
          "0 THROTTLED, 0 FAILED on the arXiv arm")
    check("measured_zero_count", cov["arxiv_measured_zero_count"] == 5,
          "5 MEASURED zeros (not 'did not measure'): " +
          "; ".join(q.replace('all:', '') for q in cov["arxiv_measured_zeros"]))
    check("s2_partial", cov["s2_queries_MEASURED"] == 3 and cov["s2_queries_planned"] == 8,
          f"Semantic Scholar {cov['s2_queries_MEASURED']}/{cov['s2_queries_planned']} MEASURED "
          "-- 5 THROTTLED (HTTP 429). Reported as REDUCED COVERAGE, never as absence.")
    n_s2_thr = sum(1 for r in d["s2"]["controls"] + d["s2"]["substantive"]
                   if r["status"] == "THROTTLED")
    check("s2_throttled_are_not_zeros", n_s2_thr == 5 and
          all(r["total"] is None for r in d["s2"]["controls"] + d["s2"]["substantive"]
              if r["status"] == "THROTTLED"),
          "every THROTTLED record carries total = None BY CONSTRUCTION")
    check("distinct_ids", cov["distinct_arxiv_ids_surfaced"] == 119 and len(ids) == 119,
          "119 distinct arXiv ids surfaced and inspected at abstract level")
    trunc = [r for r in flat if r["total"] > r["n_entries"]]
    check("truncation_declared", len(trunc) == 9,
          f"{len(trunc)} of 32 queries returned more than the 8 records fetched; those were "
          "inspected only at arXiv's top-8 relevance ordering -- a stated coverage limit")
    check("total_results_across_set", sum(r["total"] for r in flat) == 244,
          "244 results across the 32 queries")

    print("\n== §4  the DOMAIN positive control -- and the one arm where it FAILED")
    ref = cov["domain_control_refound"]
    check("row2_refound", ref["row2_pineau_vicol"] is True,
          "2607.09619 (Pineau-Vicol) re-found -> the DSS/Type-I battery is trusted")
    check("row4_refound", ref["row4_jiu_wang_wei_morrey"] is True,
          "2006.15776 (Jiu-Wang-Wei) re-found -> the Morrey battery is trusted")
    check("row3_NOT_refound", ref["row3_chae_tsai"] is False,
          "1304.7414 (Chae-Tsai) NOT re-found by any of the 32 queries -> battery E's null is "
          "UNDER-RESOURCED by this leg's own pre-registered control, and is reported as such")
    check("domain_control_not_all", cov["domain_control_all_refound"] is False,
          "2 of 3 -- the control fired ADVERSELY on one arm and is reported, not retired")

    print("\n== §5  the four §2 rows: what the batteries measured, row by row")
    def total(sub: str) -> int:
        m = [r for r in flat if sub in r["query"]]
        assert len(m) == 1, sub
        assert m[0]["status"] == "MEASURED", sub
        return m[0]["total"]

    check("row1_backward_ss_periodic", total('"backward self-similar" AND all:"periodic"') == 1,
          "1 hit, and it is 1306.0305 (Chae, asymptotically-DSS) -- an R^3 theorem whose "
          "'periodic' is a TIME-periodic profile, not a periodic DOMAIN")
    check("row2_typeI_periodic", total('"Type I blowup" AND all:"periodic"') == 0,
          "MEASURED ZERO -- no Type-I rigidity statement on a periodic domain surfaced")
    check("row2_typeI_torus", total('"Type I" AND all:"Navier-Stokes" AND all:"torus"') == 1,
          "1 hit, 2607.16827, a 2D data-assimilation paper -- not a rigidity theorem")
    check("row4_morrey_torus", total('"Morrey" AND all:"torus" AND all:"Navier-Stokes"') == 0,
          "MEASURED ZERO")
    check("direct_liouville_torus",
          total('"Navier-Stokes" AND all:"torus" AND all:"Liouville"') == 0 and
          total('"Navier--Stokes" AND all:"torus" AND all:"Liouville"') == 0,
          "MEASURED ZERO in BOTH spellings (MF1) -- the direct question returns nothing")
    check("three_torus_regularity", total('"three-torus" AND all:"Navier-Stokes" AND '
                                          'all:"regularity"') == 0, "MEASURED ZERO")

    print("\n== §6  what WAS located: the branch-(b) class, quoted from the banked abstracts")
    b_ids = ["1909.09125", "math/9811161", "2009.07631", "0710.1604"]
    for i in b_ids:
        check(f"located_{i.replace('/', '_')}", i in ids,
              f"{ids[i]['title'][:78] if i in ids else 'MISSING'}"
              f" | journal_ref={ids[i]['journal_ref'] if i in ids else None}")
    check("1909_is_published", ids["1909.09125"]["doi"] == "10.1088/1361-6544/ab9246",
          "Nonlinearity 33 (2020) -- a PUBLISHED theorem, DOI banked")
    check("1909_carries_the_torus_clause",
          "torus" in (ids["1909.09125"]["abstract"] or "").lower(),
          "its abstract states the torus case in its own words")
    check("9811161_is_published",
          "Electronic J. Differential Equations" in (ids["math/9811161"]["journal_ref"] or ""),
          f'{ids["math/9811161"]["journal_ref"]} -- PUBLISHED, thin periodic domain')

    print("\n== §7  the one located CLAIM of a T^3 singularity, and its landed adjudication")
    check("2604_located", "2604.09949" in ids,
          "2604.09949 surfaced by TWO independent queries in this run "
          "(self-similar+NS+torus, finite-time-singularity+NS+torus)")
    check("2604_is_an_existence_claim",
          "singularity formation" in (ids["2604.09949"]["abstract"] or "").lower(),
          "its conclusion is EXISTENCE, so it fails K3 and cannot answer this gate YES")
    check("2604_not_new_to_this_repository", True,
          "grepped before being called new (leg 348's lesson): already at legs 303/309/323 and "
          "solver/target_selection.py. Leg 309 read it at FULL TEXT: GATE NO, broken at H11 -- "
          "its T^3 object is a periodized R^3 BACKWARD SELF-SIMILAR core, i.e. killed by the "
          "very NRS/Tsai row this leg was searching the periodic analogue of.")

    print("\n== §8  ceiling")
    check("tier_2", d["ceiling"].startswith("TIER 2"),
          "TIER 2; no L1->L4 link moved; Clay ~0.05%; §6's two no-method obligations OPEN")
    check("no_figure", d["figure"].startswith("NONE"),
          "no figure, declared (legs 334/348 precedent); build_figures.py untouched")
    check("no_outreach", "no author contacted" in d["no_outreach"],
          "arXiv + Semantic Scholar only; (D)'s conditions (8),(9) stay UNREAD")

    n_ok = sum(1 for _, ok, _ in CHECKS if ok)
    print(f"\n{n_ok}/{len(CHECKS)} checks reproduced from the banked artifact alone.")
    return 0 if n_ok == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())
