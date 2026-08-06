"""Leg 212 / Route-USC2V — independent re-verification of leg 196 (ba5ab91).

Leg 196 landed gate STILL_SHORT on `arXiv:2511.22819`: no certificate, 0 of leg 175's 4 open
items closed, 3 new obstructions named by the authors.  That is a literature claim with
specific, checkable content, and this repository's discipline (leg 60's history) says a single
leg's self-report on such a claim gets re-checked before it is fully trusted.  This file is
that re-check.

GATE, pre-committed, verbatim:

    "Does an independent read of arXiv:2511.22819 at full-text depth confirm: (a) no
     certificate is stated or locatable, (b) 0 of leg 175's 4 open items are closed, and
     (c) the same three obstructions leg 196 named are actually present in the paper's own
     text?"

    YES -> independently confirmed; bank as the permanent verification record.
    NO  -> report the exact discrepancy (a missed certificate, a miscounted open item, a
           mistranscribed obstruction) and escalate as a priority finding.

INDEPENDENCE.  This runner does NOT import, exec, or copy anything from
`experiments/p2_route_usc2_v1_lit.py`.  The primary source was re-fetched by this leg from
`https://arxiv.org/pdf/2511.22819` (PDF md5 8367d9b73bbc615a65da1f99bb3e520e, 3 934 832 bytes)
and re-extracted by this leg with `pdftotext -layout` (extraction md5
5e20c57bf6983934fd1f40292618545c, 1593 lines, 27 pp).  That extraction proved BYTE-IDENTICAL
to leg 196's, which is the strongest available reproducibility check: both passes read
literally the same characters, so every line locator in leg 196's JSON is checkable here with
no version ambiguity.

The observations below (`OBS_*`) are this leg's own, read off that extraction by hand and by
term census, and transcribed here once each with their line locators.  Leg 196's claims are
read from its COMMITTED JSON at run time (read-only) and compared row by row.  Where the two
agree, they agree because the paper says so.

Verifier discipline: this leg REPORTS, and repairs nothing.  It edits no file leg 196 touched,
no shared ledger, and no solver module.

    .venv/bin/python experiments/p2_route_usc2v_v1_verification.py
"""

from __future__ import annotations

import datetime as _dt
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LEG196_JSON = os.path.join(ROOT, "writeup", "data", "p2_route_usc2_v1_lit.json")
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_usc2v_v1_verification.json")

LEG196_COMMIT = "ba5ab91"
TARGET = "arXiv:2511.22819v1"

PDF_MD5 = "8367d9b73bbc615a65da1f99bb3e520e"
PDF_BYTES = 3934832
EXTRACT_MD5 = "5e20c57bf6983934fd1f40292618545c"
EXTRACT_LINES = 1593
PAGES = 27


# ---------------------------------------------------------------------------
# THIS LEG'S OWN OBSERVATIONS OF THE PRIMARY SOURCE
# ---------------------------------------------------------------------------

# (a) apparatus census -- counted by this leg over the whole 1593-line extraction,
#     case-insensitive substring counts.
OBS_CENSUS = {
    "interval arithmetic": 0,
    "enclosure": 0,
    "enclos": 0,
    "validated numeric": 0,
    "certif": 0,
    "eigen": 0,
    "computer-assisted": 4,
    "computer assisted": 0,
    "verification": 0,
    "verified": 0,
    "manuscript in preparation": 0,
    "spectrum": 1,
    "spectral": 2,
    "Boussinesq": 2,
    "Euler": 3,
    "3D Euler": 2,
    "rigorous": 3,
    "machine precision": 22,
    "round-off": 9,
}

# every `computer-assisted` occurrence, classified exhaustively by this leg from the
# surrounding sentence.  ACHIEVED would mean the paper claims a CAP was carried out.
OBS_CAP_MENTIONS = [
    {"line": 41, "section": "Abstract", "kind": "PREREQUISITE",
     "text": "providing an important ingredient for bridging the gap between numerical "
             "discovery and computer-assisted proofs for unstable phenomena in nonlinear PDEs"},
    {"line": 49, "section": "1 Introduction", "kind": "DEFINITION",
     "text": "Their rigorous mathematical validation via computer-assisted proofs (CAP) "
             "generally demands extremely high numerical accuracy [2]."},
    {"line": 907, "section": "3 (Gross-Pitaevskii vortices)", "kind": "ASPIRATION",
     "text": "Obtaining robust numerical approximations is paramount for better simulations "
             "and rigorous computer-assisted proofs."},
    {"line": 1438, "section": "5 Conclusion", "kind": "PREREQUISITE",
     "text": "Beyond numerical discovery, high accuracy is a prerequisite for rigorous "
             "mathematical verification via computer-assisted proofs."},
]

# (b) leg 175's four open items, re-checked by this leg against the paper's own content.
OBS_ITEMS = [
    {"id": "a", "item": "Boussinesq / 3D Euler with boundary",
     "closed": False,
     "evidence": "sec.2 l.128-129 names the two models as CCF and IPM only. 'Boussinesq' "
                 "occurs 2x in 27 pp: abstract l.24 (recap of [1]) and ref [2] title l.1460 "
                 "(Chen-Hou). Never computed. '3D Euler' occurs 2x: l.135 (CCF motivated as "
                 "an analog for it) and the same ref [2] title. Neither model is solved.",
     "locators": [128, 24, 1460, 135]},
    {"id": "b", "item": "the ~2 decade/mode margin ladder",
     "closed": False,
     "evidence": "sec.2.3.3 restates it in the paper's own words and it is now binding in "
                 "lambda rather than in residual: l.684-690 + l.769 'decreases the achievable "
                 "lambda accuracy for a fixed computational budget by approximately two orders "
                 "of magnitude per model'. Residual half re-derived at l.676-679 and l.688-689 "
                 "(1.0 decade/mode).",
     "locators": [684, 690, 769, 676, 688]},
    {"id": "c", "item": "the unstable-spectrum enclosure",
     "closed": False,
     "evidence": "ZERO 'eigen' in 1593 lines. 'spectrum' occurs once (l.36, 'a wide spectrum "
                 "of unstable self-similar singularities' -- colloquial). 'spectral' twice, "
                 "both about neural-network spectral bias (l.1186, ref l.1553). 'operator' "
                 "occurs 0 times. No linearized-operator spectrum anywhere.",
     "locators": [36, 1186, 1553]},
    {"id": "d", "item": "the CAP announced Sep 2025 as 'Manuscript in preparation'",
     "closed": False,
     "evidence": "'preparation' occurs 0 times in the follow-up; the abs page shows v1 only, "
                 "no journal ref, 251 days on; none of the 22 Semantic Scholar citers of "
                 "2509.14185 is such a manuscript (4 plausible titles pulled at abstract "
                 "depth and ruled out).",
     "locators": []},
]

# (c) the three obstructions leg 196 attributed TO THE AUTHORS, each re-located by this leg.
#     `present` is this leg's judgement that the paper's own text says what leg 196 said it
#     says -- both the quote and the characterization.
OBS_OBSTRUCTIONS = [
    {"id": "N1", "present": True,
     "name": "the binding quantity moved from the residual to lambda's error bar",
     "found_at": "Fig.7(f) l.714-738 (the table) + sec.2.3.3 l.690/769 (the stated rate)",
     "verbatim": "fixed computational budget by approximately two orders of magnitude per "
                 "model.",
     "note": "the five-row table is present verbatim and every value matches; see LAMBDA_TABLE"},
    {"id": "N2", "present": True,
     "name": "the discovery frontier stalled: CCF's 3rd unstable searched, not found",
     "found_at": "sec.2.1.3 l.269-281",
     "verbatim": "a persistent non-smooth signal at the origin (inset of Fig.3b) remains for "
                 "all tested lambda in [0.455, 0.4713]. This indicates that if a third "
                 "unstable solution exists, it is located at a lambda value corresponding to "
                 "an even higher-gradient profile.",
     "note": "the harder-than-2D claim is at l.279-280 verbatim; the 'suite of three' is "
             "l.157 verbatim ('Previous work successfully identified three self-similar "
             "solutions (stable [12], 1st unstable [3, 12], and 2nd unstable [1])')"},
    {"id": "N3", "present": True,
     "name": "the remaining margin is hardware- and arithmetic-bound, not conceptual",
     "found_at": "sec.1 l.49-51 (the definition of success) + sec.2.3.3 l.770-775 (the remedies)",
     "verbatim": "that can be implemented on a single A100 GPU (80GB). To further improve the "
                 "lambda accuracy, one could use larger networks or more training stages in "
                 "parallel on multiple GPUs.",
     "note": "double-float round-off is the floor by the paper's own definition, l.50-51; "
             "every remedy offered is budget (l.770-772 larger networks / third stage, "
             "l.775 more GPUs). Nothing on extended precision or interval arithmetic."},
]

# Fig. 7(f), transcribed by this leg from l.714-738 of its own extraction.
LAMBDA_TABLE = [
    {"mode": "stable", "n": 0, "lambda_s": 1.0285722760323, "err": 1e-13, "line": 714},
    {"mode": "1st unstable", "n": 1, "lambda_s": 0.472129736156, "err": 2e-12, "line": 720},
    {"mode": "2nd unstable", "n": 2, "lambda_s": 0.3149617817, "err": 3e-10, "line": 726},
    {"mode": "3rd unstable", "n": 3, "lambda_s": 0.24156641, "err": 1e-8, "line": 732},
    {"mode": "4th unstable", "n": 4, "lambda_s": 0.1987237, "err": 1e-7, "line": 738},
]

RESIDUAL_FLOOR = 1e-13   # abstract l.27, sec.1 l.51: O(10^-13) is 'machine precision' here

# dates, for the elapsed-time claims
D_USC = _dt.date(2025, 9, 17)     # arXiv:2509.14185 posted
D_FIX = _dt.date(2025, 11, 28)    # arXiv:2511.22819v1 posted (abs page, verbatim)
D_PASS = _dt.date(2026, 8, 6)     # this leg / leg 196

# the light-novelty side, re-run by this leg
OBS_SEARCH = {
    "arxiv_abs_versions": ["v1"],
    "arxiv_abs_journal_ref": None,
    "arxiv_api_query": 'abs:"unstable singularities", newest first, 40 slots',
    "arxiv_api_records": 14,
    "arxiv_api_relevant_records": 2,
    "semantic_scholar_citers_of_2509_14185": 22,
    "citers_that_are_certificates": 0,
    "citers_pulled_at_abstract_depth": ["2602.17570", "2607.19700", "2510.20757", "2606.25151"],
}


# ---------------------------------------------------------------------------
# the comparator
# ---------------------------------------------------------------------------

def row(label, leg196, leg212, kind):
    """One verification row.  `agrees` is computed, never asserted."""
    return {
        "label": label,
        "leg_196_claim": leg196,
        "leg_212_observation": leg212,
        "kind": kind,
        "agrees": bool(leg196 == leg212),
    }


def clause_a(j196, census, cap_mentions):
    """(a) no certificate stated or locatable.

    Two independent discriminators, both required to be NEGATIVE for 'no certificate':
      A1 apparatus -- any of interval arithmetic / enclosure / validated numerics / certif
      A2 claim     -- any `computer-assisted` occurrence classified ACHIEVED
    """
    apparatus = {k: census.get(k, 0)
                 for k in ("interval arithmetic", "enclosure", "validated numeric", "certif")}
    apparatus_present = any(v > 0 for v in apparatus.values())
    achieved = [m for m in cap_mentions if m["kind"] == "ACHIEVED"]
    certificate_present = bool(apparatus_present or achieved)

    rows = []
    c196 = j196["term_census_full_text"]
    for k, mine in (("interval arithmetic", census["interval arithmetic"]),
                    ("enclosure", census["enclosure"]),
                    ("validated numerics", census["validated numeric"]),
                    ("certif", census["certif"]),
                    ("computer-assisted", census["computer-assisted"]),
                    ("eigen", census["eigen"]),
                    ("spectrum", census["spectrum"]),
                    ("Boussinesq", census["Boussinesq"]),
                    ("Euler", census["Euler"])):
        rows.append(row("census:%s" % k, c196.get(k), mine, "count"))

    rows.append(row("cap_mentions:n", len(j196["cap_mentions_exhaustive"]),
                    len(cap_mentions), "count"))
    for a, b in zip(sorted(j196["cap_mentions_exhaustive"], key=lambda m: m["line"]),
                    sorted(cap_mentions, key=lambda m: m["line"])):
        rows.append(row("cap_mention@l.%d:line" % b["line"], a["line"], b["line"], "locator"))
        rows.append(row("cap_mention@l.%d:kind" % b["line"], a["kind"], b["kind"],
                        "classification"))

    rows.append(row("certificate_present", j196["gate"]["certificate_found"],
                    certificate_present, "verdict"))

    return {
        "apparatus_census": apparatus,
        "apparatus_present": apparatus_present,
        "achieved_claims": achieved,
        "certificate_present": certificate_present,
        "confirms_no_certificate": not certificate_present,
        "rows": rows,
        "agrees": all(r["agrees"] for r in rows),
    }


def clause_b(j196, items):
    """(b) 0 of leg 175's 4 open items are closed."""
    n_closed = sum(1 for it in items if it["closed"])
    rows = [row("items:total", j196["leg_175_items_total"], len(items), "count"),
            row("items:closed", j196["leg_175_items_closed_by_fix"], n_closed, "count")]
    by_id = {r["id"]: r for r in j196["leg_175_open_items_recheck"]}
    for it in items:
        rows.append(row("item(%s):closed" % it["id"],
                        by_id[it["id"]]["closed_by_fix"], it["closed"], "verdict"))
    return {
        "n_items": len(items), "n_closed": n_closed,
        "confirms_zero_closed": n_closed == 0,
        "items": items,
        "rows": rows,
        "agrees": all(r["agrees"] for r in rows),
    }


def clause_c(j196, obstructions):
    """(c) the same three author-named obstructions are present as characterized."""
    authors_only = [o for o in j196["new_obstructions"] if not o.get("is_third_party")]
    rows = [row("obstructions:authors_named",
                j196["new_obstructions_named_by_the_authors"], len(obstructions), "count")]
    mine = {o["id"]: o for o in obstructions}
    for o in authors_only:
        rows.append(row("obstruction(%s):located" % o["id"], True,
                        mine.get(o["id"], {}).get("present", False), "verdict"))
    n_present = sum(1 for o in obstructions if o["present"])
    return {
        "n_named_by_authors": len(authors_only),
        "n_confirmed_present": n_present,
        "confirms_all_present": n_present == len(authors_only) == 3,
        "obstructions": obstructions,
        "rows": rows,
        "agrees": all(r["agrees"] for r in rows),
    }


def verdict(a, b, c):
    """The gate.  YES only if all three clauses confirm."""
    ok = bool(a["confirms_no_certificate"] and a["agrees"]
              and b["confirms_zero_closed"] and b["agrees"]
              and c["confirms_all_present"] and c["agrees"])
    return "CONFIRMED" if ok else "DISCREPANCY"


# ---------------------------------------------------------------------------
# derived magnitudes
# ---------------------------------------------------------------------------

def derived():
    worst = LAMBDA_TABLE[-1]
    gap = math.log10(worst["err"] / RESIDUAL_FLOOR)
    ns = [r["n"] for r in LAMBDA_TABLE]
    ys = [math.log10(r["err"]) for r in LAMBDA_TABLE]
    nbar = sum(ns) / len(ns)
    ybar = sum(ys) / len(ys)
    slope = (sum((n - nbar) * (y - ybar) for n, y in zip(ns, ys))
             / sum((n - nbar) ** 2 for n in ns))
    return {
        "residual_floor": RESIDUAL_FLOOR,
        "worst_lambda_error_bar": worst["err"],
        "worst_mode": worst["mode"],
        "residual_to_lambda_gap_decades": gap,
        # log10(error bar) RISES with mode order (-13 -> -7), so the least-squares slope is
        # positive and is itself the degradation rate in decades per mode.
        "fitted_lambda_degradation_decades_per_mode": slope,
        "stated_lambda_degradation_decades_per_mode": 2.0,
        "stated_locator": "sec.2.3.3 l.690 + l.769",
        "fit_vs_stated_ratio": 2.0 / slope,
        "residual_ladder_decades_per_mode_rederived": 1.0,
        "residual_ladder_locators": "l.676-679 (|dlambda|~1e-3: 1e-3 -> 1e-7 over 4 modes); "
                                    "l.688-689 (Rmax floor 1e-14 -> 1e-10 over 4 modes)",
        "days_usc_to_fix": (D_FIX - D_USC).days,
        "days_fix_to_pass": (D_PASS - D_FIX).days,
        "days_usc_to_pass": (D_PASS - D_USC).days,
    }


# ---------------------------------------------------------------------------
# self-tests: the comparator must be able to say NO on each of the three branches
# ---------------------------------------------------------------------------

def self_tests(j196):
    t = []

    # control: the real data must return CONFIRMED
    a = clause_a(j196, OBS_CENSUS, OBS_CAP_MENTIONS)
    b = clause_b(j196, OBS_ITEMS)
    c = clause_c(j196, OBS_OBSTRUCTIONS)
    t.append({"case": "control (real observations)", "expect": "CONFIRMED",
              "got": verdict(a, b, c)})

    # NO-branch 1: a missed certificate (apparatus present in the paper)
    cen = dict(OBS_CENSUS); cen["certif"] = 3
    t.append({"case": "injected: 'certif' x3 in the text (missed certificate)",
              "expect": "DISCREPANCY",
              "got": verdict(clause_a(j196, cen, OBS_CAP_MENTIONS), b, c)})

    # NO-branch 1b: a missed certificate (an ACHIEVED claim)
    caps = [dict(m) for m in OBS_CAP_MENTIONS]; caps[3]["kind"] = "ACHIEVED"
    t.append({"case": "injected: conclusion reclassified ACHIEVED (missed CAP claim)",
              "expect": "DISCREPANCY",
              "got": verdict(clause_a(j196, OBS_CENSUS, caps), b, c)})

    # NO-branch 2: a miscounted open item
    items = [dict(i) for i in OBS_ITEMS]; items[0]["closed"] = True
    t.append({"case": "injected: item (a) actually closed (miscounted open item)",
              "expect": "DISCREPANCY",
              "got": verdict(a, clause_b(j196, items), c)})

    # NO-branch 3: a mistranscribed obstruction
    obs = [dict(o) for o in OBS_OBSTRUCTIONS]; obs[1]["present"] = False
    t.append({"case": "injected: N2 not in the text (mistranscribed obstruction)",
              "expect": "DISCREPANCY",
              "got": verdict(a, b, clause_c(j196, obs))})

    for case in t:
        case["pass"] = case["got"] == case["expect"]
    return t


# ---------------------------------------------------------------------------

def main():
    with open(LEG196_JSON) as f:
        j196 = json.load(f)

    print("=" * 92)
    print("Leg 212 / Route-USC2V — independent re-verification of leg 196 (%s)" % LEG196_COMMIT)
    print("=" * 92)
    print("target            %s" % TARGET)
    print("PDF               md5 %s, %d bytes, %d pp  (re-fetched by this leg)"
          % (PDF_MD5, PDF_BYTES, PAGES))
    print("extraction        md5 %s, %d lines  (re-extracted by this leg)"
          % (EXTRACT_MD5, EXTRACT_LINES))
    print("                  BYTE-IDENTICAL to leg 196's extraction -> locators are comparable")

    a = clause_a(j196, OBS_CENSUS, OBS_CAP_MENTIONS)
    b = clause_b(j196, OBS_ITEMS)
    c = clause_c(j196, OBS_OBSTRUCTIONS)
    d = derived()
    v = verdict(a, b, c)

    print("\n--- CLAUSE (a): no certificate stated or locatable " + "-" * 40)
    print("  apparatus census   %s" % a["apparatus_census"])
    print("  ACHIEVED claims    %d of %d `computer-assisted` occurrences"
          % (len(a["achieved_claims"]), OBS_CENSUS["computer-assisted"]))
    for m in OBS_CAP_MENTIONS:
        print("    l.%-5d %-28s %s" % (m["line"], m["kind"], m["section"]))
    print("  -> certificate present: %s   confirms leg 196: %s"
          % (a["certificate_present"], a["confirms_no_certificate"] and a["agrees"]))

    print("\n--- CLAUSE (b): 0 of leg 175's 4 open items closed " + "-" * 40)
    for it in b["items"]:
        print("  (%s) %-45s closed=%s" % (it["id"], it["item"][:45], it["closed"]))
    print("  -> %d of %d closed; confirms leg 196: %s"
          % (b["n_closed"], b["n_items"], b["confirms_zero_closed"] and b["agrees"]))

    print("\n--- CLAUSE (c): the 3 author-named obstructions " + "-" * 43)
    for o in c["obstructions"]:
        print("  %s present=%-5s  %s" % (o["id"], o["present"], o["found_at"]))
    print("  -> %d/%d present as characterized; confirms leg 196: %s"
          % (c["n_confirmed_present"], c["n_named_by_authors"],
             c["confirms_all_present"] and c["agrees"]))

    print("\n--- derived magnitudes " + "-" * 68)
    print("  residual floor %.0e vs worst lambda bar %.0e at the %s mode"
          % (d["residual_floor"], d["worst_lambda_error_bar"], d["worst_mode"]))
    print("  residual->lambda enclosure gap        %.1f decades" % d["residual_to_lambda_gap_decades"])
    print("  fitted lambda degradation             %.3f decades/mode"
          % d["fitted_lambda_degradation_decades_per_mode"])
    print("  stated by the authors                 %.1f decades/mode (%s)"
          % (d["stated_lambda_degradation_decades_per_mode"], d["stated_locator"]))
    print("  ratio stated/fitted                   %.3fx" % d["fit_vs_stated_ratio"])
    print("  elapsed  USC->FIX %d d   FIX->now %d d   USC->now %d d"
          % (d["days_usc_to_fix"], d["days_fix_to_pass"], d["days_usc_to_pass"]))

    disagreements = [r for r in (a["rows"] + b["rows"] + c["rows"]) if not r["agrees"]]
    print("\n--- row-by-row comparison against leg 196's committed JSON " + "-" * 32)
    print("  %d rows compared, %d disagreement(s)"
          % (len(a["rows"]) + len(b["rows"]) + len(c["rows"]), len(disagreements)))
    for r in disagreements:
        print("    MISMATCH %-34s leg196=%r  leg212=%r" % (r["label"], r["leg_196_claim"],
                                                           r["leg_212_observation"]))

    tests = self_tests(j196)
    print("\n--- self-tests (the comparator must be able to answer NO) " + "-" * 33)
    for t in tests:
        print("  [%s] %-58s expect %-12s got %s"
              % ("PASS" if t["pass"] else "FAIL", t["case"], t["expect"], t["got"]))
    tests_ok = all(t["pass"] for t in tests)

    payload = {
        "leg": 212, "route": "ROUTE-USC2V", "role": "VERIFY", "pass_date": str(D_PASS),
        "verifies_leg": 196, "verifies_commit": LEG196_COMMIT,
        "verifies_claim": ("leg 196's gate STILL_SHORT on arXiv:2511.22819: no certificate "
                           "stated or locatable, 0 of leg 175's 4 open items closed, 3 new "
                           "obstructions named by the authors"),
        "gate": {
            "question": ("Does an independent read of arXiv:2511.22819 at full-text depth "
                         "confirm: (a) no certificate is stated or locatable, (b) 0 of leg "
                         "175's 4 open items are closed, and (c) the same three obstructions "
                         "leg 196 named are actually present in the paper's own text?"),
            "verdict": v,
            "answered_branch": ("YES -- independently confirmed" if v == "CONFIRMED"
                                else "NO -- discrepancy, escalate"),
            "escalates": v != "CONFIRMED",
        },
        "independence": {
            "imports_leg_196_code": False,
            "primary_source_refetched_by_this_leg": True,
            "pdf_md5": PDF_MD5, "pdf_bytes": PDF_BYTES, "pages": PAGES,
            "extraction_md5": EXTRACT_MD5, "extraction_lines": EXTRACT_LINES,
            "extraction_byte_identical_to_leg_196": True,
            "note": ("both passes read literally the same characters, so leg 196's line "
                     "locators are checkable here with no pdftotext-version ambiguity"),
        },
        "clause_a_no_certificate": a,
        "clause_b_zero_items_closed": b,
        "clause_c_obstructions_present": c,
        "lambda_table_fig_7f": LAMBDA_TABLE,
        "derived": derived(),
        "search_reverification": OBS_SEARCH,
        "term_census_full_text_leg_212": OBS_CENSUS,
        "cap_mentions_exhaustive_leg_212": OBS_CAP_MENTIONS,
        "rows_compared": len(a["rows"]) + len(b["rows"]) + len(c["rows"]),
        "disagreements": disagreements,
        "self_tests": tests,
        "self_tests_all_pass": tests_ok,
        "locator_notes": [
            {"where": "leg 196 JSON new_obstructions[N1].locator 'sec.2.3.3 l.696'",
             "issue": "l.696 is a blank line in the shared extraction; the sentence it points "
                      "at runs l.690 -> l.769 (a figure block splits it).",
             "quoted_text_verbatim_present": True,
             "moves_the_gate": False,
             "severity": "locator only -- the quoted string is exact and present"},
            {"where": "leg 196 JSON leg_175_open_items_recheck[b].evidence 'l.684-696'",
             "issue": "same sentence; the range end should be l.690 (+ l.769 after the figure "
                      "block), not l.696.",
             "quoted_text_verbatim_present": True,
             "moves_the_gate": False,
             "severity": "locator only"},
            {"where": "leg 196 JSON quotes[2].line = 130",
             "issue": "the quoted sentence ('two canonical models ...') occupies l.128-129; "
                      "l.130 is the line after it.",
             "quoted_text_verbatim_present": True,
             "moves_the_gate": False,
             "severity": "locator only, off by one line"},
        ],
        "ceiling": ("No link of the L1->L4 chain moved. Clay stays ~0.05%. This leg edits no "
                    "ledger, no solver module, and registers no figure (the convention for a "
                    "literature-only pass in this repository: legs 175, 183, 189, 196 "
                    "registered none)."),
    }
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2)
    print("\nwrote %s" % os.path.relpath(OUT, ROOT))

    print("\n" + "=" * 92)
    print("GATE: %s — %s" % (v, payload["gate"]["answered_branch"]))
    print("=" * 92)
    return 0 if (v == "CONFIRMED" and tests_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
