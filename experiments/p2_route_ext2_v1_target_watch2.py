"""Route-EXT2 v1 (leg 77): has anyone certified the RANK-2 target object since March 2026?

PURE LITERATURE LEG.  Nothing here computes a gCLM quantity; the standing ban on further
gCLM measurement legs is respected.  This script is the executable record of a search: it
carries the query strings, the corpus enumerations (arXiv API, not keyword luck), the
primary-source locations, and the verbatim sentences, and re-emits them as
writeup/data/p2_route_ext2_v1_target_watch2.json.

WHAT WAS ASKED (the leg's gate, verbatim)
    "Has a certificate (computer-assisted or analytic) for arXiv:2603.25104's
     gCLM_degenerate_one_scale branch been published since March 2026?"

WHAT CAME BACK: NO -- and the decisive evidence is not an absence.

  The object is Huang-Tong-Wang's a > 0 one-scale self-similar profiles from derivative-
  DEGENERATE data (vanishing order k = 3), solver/target_selection.py's rank-2 candidate.
  The paper was REVISED on 2026-06-16 (v2, 82 days after v1, 51 days before this pass).
  In that revision the authors proved the a <= 0 side -- Theorem 2.4 (a = 0 outer profile
  converges to an explicit singular function), Theorem 2.6 (a < 0 exact singular family),
  Theorem 2.7 (a < 1 inner traveling wave, fixed-point) -- and left the a > 0 side exactly
  where v1 had it: section 4, titled "Numerical results with degenerate initial data for
  a > 0", with the abstract still saying "we observe".  There is no theorem for a > 0 in
  either version, and the paper's only "computer-assisted proof" mentions are in its
  related-work discussion of OTHER models (De Gregorio, axisymmetric Euler).

  Independent corroboration, all at pass date 2026-08-06:
    * Semantic Scholar citations endpoint for arXiv:2603.25104 -> empty data array, 0
      indexed citations, 133 days after v1.
    * arXiv API enumeration abs:"Constantin-Lax-Majda" AND abs:"self-similar" -> 10 entries
      total, 3 from 2026, 0 of which address the degenerate a > 0 branch.
    * arXiv API author enumeration over De Huang / Jiajun Tong / Xiuyuan Wang -> the only
      2026 math.AP entry is 2603.25104v2 itself; the discoverers filed no follow-up.

THE ONE FALSE FRIEND, which would produce a wrong YES from an abstract-only pass:
  Xu arXiv:2607.19762v1 (2026-07-22), the NEWEST gCLM paper in the corpus, contains the
  phrase "For a>0 we prove".  It is not this certificate on three counts:
    F1  wrong branch -- "each admissible smooth focusing profile", the LSS / non-degenerate
        family that target_selection.py's own q1 note already excludes.  The object here is
        the k = 3 DEGENERATE branch at the same a.
    F2  wrong kind of statement -- a "conditional two-line inclusion" localizes spectrum for
        a profile ASSUMED to exist; it certifies no profile even on its own family.
    F3  the words are absent -- "degenerate", "degeneracy", "vanishing order" and
        "Huang-Tong-Wang" all return 0 hits on the Xu page.  Xu does not address the object.

CONSEQUENCE FOR THE LEDGER (reported, never applied -- solver/target_selection.py is leg
63's exclusive territory and is NOT touched by this leg):
    its gCLM_degenerate_one_scale entry, field "certified": "NO", is CURRENT as of
    2026-08-06, not stale.  One precision suggestion only: the entry's "source" field cites
    the paper without a version, and the theorem content grew between v1 and v2.

Full prose, the query log with links, and the watch metadata for the next re-ask are in
writeup/novelty/leg_77.md.
"""

from __future__ import annotations

import json
import os

GATE = (
    "Has a certificate (computer-assisted or analytic) for arXiv:2603.25104's "
    "gCLM_degenerate_one_scale branch been published since March 2026?"
)

PASS_DATE = "2026-08-06"

# ---------------------------------------------------------------------------
# The queries, verbatim, in the order issued.
# ---------------------------------------------------------------------------

QUERIES = [
    {
        "id": "Q1",
        "string": ("arXiv 2603.25104 Huang Tong Wang generalized Constantin-Lax-Majda "
                   "degenerate self-similar"),
        "kind": "web search",
        "relevant_returns": [
            "https://arxiv.org/html/2603.25104",
            "https://sites.google.com/view/de-huang/research",
            "https://arxiv.org/pdf/2401.14615",
            "https://arxiv.org/pdf/2305.05895",
        ],
        "note": ("the first author's page is stale for 2026 math.AP work -- it lists only a "
                 "Bernoulli probability paper for 2026 -- so it is NOT usable as a negative"),
    },
    {
        "id": "Q2",
        "string": "gCLM self-similar profiles degenerate data computer-assisted proof 2026",
        "kind": "web search",
        "relevant_returns": [
            "https://arxiv.org/pdf/2604.01868",
            "https://arxiv.org/pdf/2605.15149",
            "https://arxiv.org/pdf/2605.15130",
            "https://arxiv.org/html/2308.01528",
        ],
        "note": ("2604.01868 is the Hou-Luo / 2D Boussinesq singular-profile paper -- an "
                 "ADJACENT object, itself numerical, and not this branch"),
    },
    {
        "id": "Q3",
        "string": ("\"Constantin-Lax-Majda\" degenerate blowup rigorous proof interval "
                   "arithmetic 2026 arXiv new"),
        "kind": "web search",
        "relevant_returns": [],
        "note": "returns only the pre-2026 gCLM corpus; no new object",
    },
    {
        "id": "Q4",
        "string": ("computer-assisted proof self-similar blowup 2026 arXiv \"degenerate\" "
                   "profile Hou Chen Cadiot Lessard fluid model"),
        "kind": "web search",
        "relevant_returns": [
            "https://arxiv.org/pdf/2310.19781",
            "https://doi.org/10.1137/23M1607507",
        ],
        "note": "the CAP machinery exists; none of it has been pointed at this branch",
    },
    {
        "id": "Q5",
        "string": "\"2603.25104\" cited OR references gCLM degenerate blowup",
        "kind": "web search",
        "relevant_returns": [],
        "note": ("returns the paper itself plus unrelated degenerate-PARABOLIC blowup work; "
                 "the word 'degenerate' reliably drags in porous-medium and semilinear-heat "
                 "results that have nothing to do with the object"),
    },
]

ENUMERATIONS = [
    {
        "id": "E1",
        "url": ("http://export.arxiv.org/api/query?search_query=all:%22Constantin-Lax-Majda%22"
                "&start=0&max_results=60&sortBy=submittedDate&sortOrder=descending"),
        "purpose": "full-corpus sweep, newest first, not keyword luck",
        "entries_2026": ["2607.19762v1", "2604.01244v4", "2603.25104v2", "2603.26715v5"],
    },
    {
        "id": "E2",
        "url": ("http://export.arxiv.org/api/query?search_query=abs:%22Constantin-Lax-Majda%22"
                "+AND+abs:%22self-similar%22&start=0&max_results=60&sortBy=submittedDate"
                "&sortOrder=descending"),
        "purpose": "the self-similar sub-corpus -- where a certificate would have to appear",
        "n_entries_total": 10,
        "entries_2026": ["2607.19762v1", "2603.25104v2", "2603.26715v5"],
        "n_2026_addressing_the_degenerate_a_positive_branch": 0,
    },
    {
        "id": "E3",
        "url": ("http://export.arxiv.org/api/query?search_query=au:%22Jiajun_Tong%22+OR+"
                "au:%22De_Huang%22+OR+au:%22Xiuyuan_Wang%22&start=0&max_results=60"
                "&sortBy=submittedDate&sortOrder=descending"),
        "purpose": "did the DISCOVERERS certify their own branch in a follow-up?",
        "result": "the only 2026 math.AP entry among the three authors is 2603.25104v2 itself",
    },
    {
        "id": "E4",
        "url": ("https://api.semanticscholar.org/graph/v1/paper/arXiv:2603.25104/citations"
                "?fields=title,year,venue,externalIds,abstract&limit=100"),
        "purpose": "who cites the object at all?",
        "n_citations_indexed": 0,
        "result": "empty data array",
    },
]

# ---------------------------------------------------------------------------
# The object, and what its own latest version proves.
# ---------------------------------------------------------------------------

OBJECT = {
    "ledger_id": "gCLM_degenerate_one_scale",
    "ledger_module": "solver/target_selection.py",
    "ledger_rank": 2,
    "arxiv": "2603.25104",
    "title": ("Self-similar finite-time blowups with singular profiles of the generalized "
              "Constantin-Lax-Majda model: theoretical and numerical investigations"),
    "authors": ["De Huang", "Jiajun Tong", "Xiuyuan Wang"],
    "v1_date": "2026-03-26",
    "v2_date": "2026-06-16",
    "branch_in_question": ("a > 0 one-scale self-similar blowups with REGULAR profiles from "
                           "smooth data with derivative degeneracy of vanishing order k = 3"),
}

THEOREM_INVENTORY_V2 = [
    {"label": "Proposition 2.1", "case": "all a",
     "content": "asymptotic self-similarity CONDITIONAL on profile convergence to a steady state",
     "certifies_the_branch": False,
     "why_not": "a conditional implication, not an existence statement"},
    {"label": "Theorem 2.4", "case": "a = 0",
     "content": "outer profile converges to an explicit SINGULAR function (odd-symmetric degenerate)",
     "certifies_the_branch": False, "why_not": "wrong sign of a, and a singular not regular profile"},
    {"label": "Corollary 2.5", "case": "a = 0",
     "content": "same on the half line", "certifies_the_branch": False, "why_not": "wrong sign of a"},
    {"label": "Theorem 2.6", "case": "a < 0",
     "content": "exact singular self-similar solutions, explicit a-parameterized family",
     "certifies_the_branch": False, "why_not": "wrong sign of a"},
    {"label": "Theorem 2.7", "case": "a < 1",
     "content": "existence of the inner TRAVELING WAVE via a fixed-point method",
     "certifies_the_branch": False,
     "why_not": ("the two-scale inner object of the a <= 0 scenario, not the a > 0 one-scale "
                 "profile; the a < 1 range is incidental")},
    {"label": "(none)", "case": "a > 0 regular one-scale, degenerate data",
     "content": "carried entirely by section 4, 'Numerical results with degenerate initial data for a > 0'",
     "certifies_the_branch": False, "why_not": "THERE IS NO THEOREM"},
]

VERBATIM = [
    {"source": "arXiv:2603.25104v2 abstract",
     "text": ("For $a>0$, we observe one-scale self-similar blowups with regular profiles "
              "that have not been found in previous studies."),
     "reading": "'we observe' -- unchanged from v1, in a v2 that upgraded other cases to theorems"},
    {"source": "arXiv:2603.25104v2 body",
     "text": ("In the case $a>0$, our numerical simulation indicates that odd-symmetric "
              "degenerate initial data ... can lead to ordinary self-similar finite-time "
              "blowups but with new regular profiles."),
     "reading": "'our numerical simulation indicates'"},
    {"source": "arXiv:2603.25104v2 related work",
     "text": ("combination of the dynamic rescaling method and the method of computer-"
              "assisted proof"),
     "reading": ("the paper's ONLY computer-assisted-proof mention, and it is about the De "
                 "Gregorio model and axisymmetric Euler -- not about its own a > 0 case")},
    {"source": "arXiv:2607.19762v1 abstract (Xu)",
     "text": ("For $a>0$ we prove a conditional two-line inclusion for each admissible smooth "
              "focusing profile, recompute the branch $c_l(a)$ of Lushnikov, Silantyev, and "
              "Siegel as a cross-check, and record the formal scaling-relevance exponent "
              "$s^*(a) = 1/c_l(a)$"),
     "reading": ("the false friend: right model, right sign of a, the word 'prove', WRONG "
                 "branch -- the smooth focusing / LSS non-degenerate family")},
]

FALSE_FRIENDS = [
    {
        "id": "F1",
        "source": "arXiv:2607.19762v1 (Xu, 2026-07-22)",
        "days_after_object_v1": 118,
        "trap": "contains 'For a>0 we prove' in a gCLM paper posted after the object",
        "why_it_is_not_the_certificate": [
            "wrong branch: 'each admissible smooth focusing profile' is the LSS / NON-degenerate "
            "family, which target_selection.py's q1 note already excludes",
            "wrong kind of statement: a conditional two-line spectral INCLUSION for a profile "
            "assumed to exist certifies no profile",
            "keyword check of the page: 'degenerate' 0 hits, 'degeneracy' 0 hits, 'vanishing "
            "order' 0 hits, 'Huang-Tong-Wang' 0 hits",
        ],
    },
    {
        "id": "F2",
        "source": "arXiv:2604.01868 (2026-04, Hou-Luo / 2D Boussinesq singular profiles)",
        "trap": "a 2026 'novel self-similar blowups with singular profiles' paper, same season",
        "why_it_is_not_the_certificate": [
            "different model (Hou-Luo / Boussinesq, not gCLM)",
            "itself a numerical investigation, so it certifies nothing anywhere",
        ],
    },
    {
        "id": "F3",
        "source": "arXiv:2305.05895 (Huang-Qin-Wang-Wei) and arXiv:2401.14615 (Huang-Qin-Wang)",
        "trap": "same lead author, gCLM, self-similar, and PROVED existence",
        "why_it_is_not_the_certificate": [
            "the NON-degenerate smooth branch and the non-degenerate multi-scale scenario "
            "respectively -- both predate the degenerate setting and neither covers it",
        ],
    },
    {
        "id": "F4",
        "source": "generic web search on 'degenerate ... blowup ... proof'",
        "trap": "degenerate-parabolic / porous-medium / semilinear-heat blowup results dominate",
        "why_it_is_not_the_certificate": ["a different meaning of 'degenerate' entirely"],
    },
]

REPORTED_TO_LEG_63 = [
    {
        "field": "TARGET_LEDGER['gCLM_degenerate_one_scale']['certified']",
        "current_value": "NO",
        "verdict": "STILL CORRECT as of " + PASS_DATE + " -- no stale-entry correction is owed",
        "action_for_this_leg": "none; solver/target_selection.py is leg 63's exclusive territory",
    },
    {
        "field": "TARGET_LEDGER['gCLM_degenerate_one_scale']['source']",
        "current_value": "arXiv:2603.25104 section 4, Table 4.1",
        "suggestion": ("pin the version -- the paper is now at v2 (2026-06-16) and the a <= 0 "
                       "theorem content GREW between v1 and v2 while section 4 did not"),
        "severity": "precision suggestion, not a correctness defect",
    },
    {
        "field": "TARGET_LEDGER['gCLM_degenerate_one_scale']['q1']",
        "current_value": ("Huang-Qin-Wang-Wei's analytic gCLM branch is the NON-degenerate one "
                          "and does not cover these"),
        "verdict": ("survives contact with the newest source -- Xu arXiv:2607.19762 likewise "
                    "works the non-degenerate LSS branch, so the same exclusion now covers two "
                    "papers, not one"),
    },
]

WATCH_METADATA = {
    "object_first_posted": "2026-03-26",
    "object_last_revised": "2026-06-16",
    "searched": PASS_DATE,
    "days_since_v1": 133,
    "days_v1_to_v2": 82,
    "days_since_v2": 51,
    "indexed_citations_at_pass": 0,
    "n_2026_entries_in_self_similar_gclm_enumeration": 3,
    "n_of_those_addressing_the_branch": 0,
    "cheapest_re_ask": ("re-run E4 (Semantic Scholar citations) and E2 (arXiv self-similar "
                        "enumeration); a non-empty citation list or a 4th 2026 entry is the "
                        "only trigger worth a full pass"),
}

INDEPENDENCE_FROM_LEG_74 = {
    "leg_74_object": "HL_S2_nonsymmetric (rank 1)",
    "this_object": "gCLM_degenerate_one_scale (rank 2)",
    "shared_paper": None,
    "shared_authors": None,
    "shared_corpus": ("none -- this leg enumerates the Constantin-Lax-Majda corpus; Hou-Luo "
                      "sources appear here only as listed OFF-TARGET returns"),
    "verdict": "the two legs' findings stand or fall separately",
}


def build() -> dict:
    return {
        "leg": 77,
        "route": "EXT2 v1",
        "pass_date": PASS_DATE,
        "kind": "literature watch -- no computation, no gCLM measurement, no solver touched",
        "gate": GATE,
        "gate_answer": {
            "verdict": "NO",
            "statement": ("no certificate, computer-assisted or analytic, has appeared for the "
                          "a > 0 degenerate one-scale regular branch as of " + PASS_DATE),
            "strongest_evidence": ("not an absence: the AUTHORS revised the paper on 2026-06-16, "
                                   "proved the a <= 0 side in that revision, and left the a > 0 "
                                   "side as section 4 numerics with 'we observe' in the abstract"),
            "ledger_consequence": ("target_selection.py's 'certified': 'NO' for this candidate is "
                                   "CURRENT, not stale -- bank the dated watch entry"),
        },
        "object": OBJECT,
        "queries": QUERIES,
        "enumerations": ENUMERATIONS,
        "theorem_inventory_v2": THEOREM_INVENTORY_V2,
        "verbatim": VERBATIM,
        "false_friends": FALSE_FRIENDS,
        "reported_to_leg_63_not_applied": REPORTED_TO_LEG_63,
        "watch_metadata": WATCH_METADATA,
        "independence_from_leg_74": INDEPENDENCE_FROM_LEG_74,
        "bans_respected": [
            "no gCLM measurement leg -- nothing here computes any gCLM quantity",
            "capabilities.py grepped before writing (row solver/target_selection.py) and NOT edited",
            "solver/target_selection.py read only -- leg 63's exclusive territory",
        ],
    }


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "writeup", "data",
                       "p2_route_ext2_v1_target_watch2.json")
    payload = build()
    with open(os.path.normpath(out), "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)
        fh.write("\n")
    ans = payload["gate_answer"]
    md = payload["watch_metadata"]
    print("Route-EXT2 v1 (leg 77) -- literature watch, no computation")
    print("  gate:", GATE)
    print("  verdict:", ans["verdict"], "--", ans["statement"])
    print("  object: arXiv:%s v1 %s, v2 %s" % (OBJECT["arxiv"], OBJECT["v1_date"],
                                               OBJECT["v2_date"]))
    print("  elapsed: %d days since v1, %d days since v2; %d indexed citations"
          % (md["days_since_v1"], md["days_since_v2"], md["indexed_citations_at_pass"]))
    print("  theorems in v2 covering the a > 0 degenerate branch: %d of %d statements"
          % (sum(1 for t in THEOREM_INVENTORY_V2 if t["certifies_the_branch"]),
             len(THEOREM_INVENTORY_V2)))
    print("  2026 entries in the self-similar gCLM enumeration: %d, addressing the branch: %d"
          % (md["n_2026_entries_in_self_similar_gclm_enumeration"],
             md["n_of_those_addressing_the_branch"]))
    print("  queries logged:", len(QUERIES), "| API enumerations:", len(ENUMERATIONS),
          "| false friends recorded:", len(FALSE_FRIENDS))
    print("  reported to leg 63 (NOT applied here):", len(REPORTED_TO_LEG_63), "items")
    print("  wrote", os.path.normpath(out))


if __name__ == "__main__":
    main()
