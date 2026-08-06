"""Route-EXT5 v1 (leg 93): has the community's verdict on arXiv:2604.09949 moved?

PURE LITERATURE LEG -- A DATED WATCH.  Nothing here computes anything, no solver
module is imported, no bound is touched.  This script is the executable record of a
search: it carries the query strings, the endpoints hit, and the verdicts, and it
re-emits them as writeup/data/p2_route_ext5_v1_target_watch5.json.

Distinct in KIND from legs 74/77/82/90, which ask "does a certificate EXIST".  This
leg asks "has the community's verdict on an EXISTING claim MOVED".

WHAT WAS ASKED (the leg's gate, verbatim)
    "Since arXiv:2604.09949 was posted, has any independent group published a
     confirmation, refutation, retraction, or correction of its 3D NS self-similar
     singularity claim?"

WHAT CAME BACK: **NO** -- no independent verdict of any kind, on four channels,
118 days on.  **BUT the watch turned up something larger than what it asked for:
the AUTHOR has since published SIX papers claiming the LOGICALLY OPPOSITE result,
using the SAME 5D-lifted machinery, none of which cite 2604.09949.**  That is a de
facto self-refutation -- provenance evidence, not proof -- and it is reported here
prominently rather than filed quietly.  Concretely, as of 2026-08-06:

  E1  THE SOURCE PAPER HAS NOT MOVED AND HAS NOT BEEN WITHDRAWN.  arXiv:2604.09949
      is still at **v1**, sole submission 10 Apr 2026, single author Rishad
      Shahmurov, math.AP.  **118 days** elapsed with **0** replacements, **0**
      corrections, no journal-ref, no withdrawal marker on the abs page.  A
      retraction or a published correction BY THE AUTHOR would be visible exactly
      here, and there is none.  This is positive evidence, not absence.

  E2  THE CITATION GRAPH IS EMPTY, ON TWO INDEPENDENT INDEXES.  Semantic Scholar's
      citations endpoint returns `{"offset": 0, "data": []}`, and the paper record
      returns `citationCount: 0, influentialCitationCount: 0` WITH a live
      `CorpusId: 287425079` -- so the paper IS indexed and the zero is a measured
      zero, not an indexing miss.  OpenAlex's **full-text** search for the string
      "2604.09949" returns `count: 0`, which would also catch a paper that
      discussed the claim in its body without formally citing it.  Unlike leg 74's
      C5, this channel is load-bearing here: it is corroborated across two indexes
      and neither endpoint rate-limited on the calls that produced the zeros.

  E3  THE AUTHOR HAS POSTED EIGHT TIMES SINCE, AND SIX CLAIM THE OPPOSITE.  A
      submittedDate-descending author feed returns 8 submissions after 2604.09949.
      Two are 3D Euler blow-up (a DIFFERENT system -- not contradictory, and named
      here so the count is not overstated).  The other **six** claim global
      regularity / global smoothness / unconditional global existence for 3D
      Navier-Stokes.  And one submission SEVEN DAYS BEFORE the singularity paper --
      2604.03519, "Unconditional Axis-Regularity in the 5D Corridor" -- was already
      claiming unconditional regularity in the SAME 5D lift, so the two lines were
      running SIMULTANEOUSLY rather than one superseding the other.

  E4  THE LATER PAPERS USE THE SAME MACHINERY AND NEVER MENTION THE CLAIM.
      2606.07869 Thm 1.1 gives `T* = infinity` for axisymmetric 3D NS with arbitrary
      swirl, and its sec 2.4 defines the five-dimensional lifted measure
      `dmu_5 = r^3 dr dz` and lifted Laplacian `Delta_5 = d_rr + 3 r^-1 d_r + d_zz`
      -- the SAME 5D lift named in 2604.09949's own TITLE.  2605.01873 Thm 2.1 gives
      `T_+ = infinity` for the FULL 3D system, and its bibliography has **23**
      entries, **0** of them self-citations.  Neither paper cites, retracts,
      corrects, or acknowledges 2604.09949.

  E5  THE NEAREST INDEPENDENT CANDIDATE, OPENED AND CLEARED.  arXiv:2606.25341
      (Runlong Yu, "A Structural Audit of Navier-Stokes Obstruction Calculus") is
      the only 2026 paper the searches surfaced whose TITLE suggests an audit of NS
      singularity claims.  It was FETCHED AND READ rather than pattern-matched: it
      is a structural analysis of CKN-badness across scales concluding "no
      unconditional single-scale domination by a signed combined-work detector is
      available", and it mentions neither 2604.09949 nor Shahmurov.  Not a response
      paper.  Cleared.

WHAT THIS MEANS FOR M-5
    The no-branch lands.  PHASE2_P2_NOTES's M-5 verdict `CLAIMED_UNUSABLE` and
    solver/target_selection.py's rank-6 entry "claimed by arXiv:2604.09949" are
    **confirmed current as of 2026-08-06**, not stale.  This leg edits neither file
    and never opened target_selection.py for writing.

    M-5 rested `CLAIMED_UNUSABLE` on two reasons that "stand on their own": (i) no
    verification package released, (ii) its Thm 12.1 reconstructs the exactly
    BACKWARD self-similar solution excluded by Necas-Ruzicka-Sverak and Tsai.  This
    leg adds a THIRD, independent of both and unavailable in April: (iii) the
    author's own subsequent corpus asserts the negation.  Reason (iii) is cheaper to
    state than either -- it needs no reading of the manuscript -- but it is WEAKER AS
    MATHEMATICS, because a self-contradicting corpus says at most that one of the two
    lines is wrong and does not say WHICH.  M-5's reason (ii) remains the one that
    says which, and it stays load-bearing.  **M-5 is strengthened, not overturned**,
    and its arithmetic audit (2*delta*M*K = 8.9e-5; Kantorovich 2*M^2*K*delta =
    4.3e-2 with 23x margin) remains the best available check of the document -- as
    far as this pass can determine, the ONLY independent check that exists.

METHOD, so the pass is reproducible
    E1/E3 are arXiv-API calls with sortBy=submittedDate&sortOrder=descending; E2 is
    Semantic Scholar + OpenAlex; E4/E5 are direct document fetches.  The exact URLs
    are in ENDPOINTS below and re-run verbatim.  Known limitation, recorded rather
    than hidden: all four channels see only the PUBLIC record.  A referee report, a
    private erratum, or a seminar dismissal would be invisible to every one of them,
    and a four-month-old single-author preprint sits near the edge of index lag.
    What is claimed is the public record, and nothing more.

    Second limitation, equally important: the self-contradiction of E3/E4 is
    INFERENCE.  No paper in the corpus says "2604.09949 is withdrawn" or
    "supersedes".  The incompatibility is read off theorem statements.  It is
    recorded as PROVENANCE evidence and must NOT be reported as "the author
    retracted", because he did not.

Full prose is in writeup/novelty/leg_93.md (this leg's novelty log as well as its
technical note); the journal entry is experiments/journal/leg_93.md.
"""

from __future__ import annotations

import json
import os

PASS_DATE = "2026-08-06"
SOURCE_ARXIV = "2604.09949"
SOURCE_V1_DATE = "2026-04-10"
DAYS_ELAPSED = 118  # 2026-04-10 -> 2026-08-06

GATE = (
    "Since arXiv:2604.09949 was posted, has any independent group published a "
    "confirmation, refutation, retraction, or correction of its 3D NS self-similar "
    "singularity claim?"
)

# ---------------------------------------------------------------------------
# Query log.  Links, not counts (writeup/novelty/README.md's rule, after leg 53).
# ---------------------------------------------------------------------------
QUERIES = [
    {
        "id": "W1",
        "kind": "web_search",
        "query": (
            'arXiv 2604.09949 Shahmurov "Stable Finite-Time Singularity" 3D '
            "Navier-Stokes refutation error"
        ),
        "relevant_links": [
            "https://arxiv.org/abs/2604.09949",
            "https://arxiv.org/html/2604.09949v1",
            "https://arxiv.org/pdf/2604.09949",
            "https://arxiv.org/abs/2107.06509",
            "https://arxiv.org/pdf/2112.14917",
            "https://arxiv.org/pdf/math/0504219",
            "https://arxiv.org/abs/1811.03304",
        ],
        "verdict": (
            "every return is the source paper itself or pre-existing unrelated NS "
            "near-singularity work; no critique, no comment, no response paper"
        ),
    },
    {
        "id": "W2",
        "kind": "web_search",
        "query": (
            "Shahmurov Navier-Stokes singularity claim 2026 contradictory global "
            "regularity preprints discussion"
        ),
        "relevant_links": [
            "https://arxiv.org/html/2604.21213",
            "https://arxiv.org/html/2605.01873",
            "https://arxiv.org/html/2605.01875",
            "https://arxiv.org/html/2605.09797v1",
            "https://arxiv.org/pdf/2605.04181",
            "https://arxiv.org/pdf/2605.04526",
            "https://arxiv.org/html/2604.09949",
        ],
        "verdict": (
            "THE QUERY THAT BROKE THE LEG OPEN -- every hit is by the same author; "
            "the 'discussion' asked for does not exist, what exists is the author's "
            "own contradictory corpus"
        ),
    },
    {
        "id": "W3",
        "kind": "web_search",
        "query": (
            'MathOverflow OR blog 2026 "Navier-Stokes" singularity preprint '
            "computer-assisted Newton-Kantorovich claim flawed backward self-similar "
            "Necas Ruzicka Sverak excluded"
        ),
        "relevant_links": [
            "https://arxiv.org/html/2606.07501",
            "https://arxiv.org/pdf/2606.25341",
            "https://arxiv.org/pdf/2606.12756",
            "https://arxiv.org/pdf/2509.25116",
            "https://arxiv.org/pdf/2510.20757",
            "https://arxiv.org/pdf/2101.03727",
            "https://navier-stokes.dev/",
            (
                "https://terrytao.wordpress.com/wp-content/uploads/2024/03/"
                "machine-assisted-proof-notices.pdf"
            ),
        ],
        "verdict": (
            "no MathOverflow thread, no blog post, no commentary of any kind on "
            "2604.09949; the nearest candidate 2606.25341 was opened and cleared (E5)"
        ),
    },
]

# ---------------------------------------------------------------------------
# Structured endpoints -- these re-run verbatim, which is the point.
# ---------------------------------------------------------------------------
ENDPOINTS = [
    {
        "id": "E1",
        "channel": "source paper: version history and withdrawal check",
        "url": "https://export.arxiv.org/api/query?id_list=2604.09949",
        "url_secondary": "https://arxiv.org/abs/2604.09949",
        "finding": {
            "title": (
                "Stable Finite-Time Singularity Formation for 3D Navier--Stokes via "
                "5D-Lifted Axisymmetric Reductions"
            ),
            "author": "Rishad Shahmurov",
            "n_authors": 1,
            "primary_category": "math.AP",
            "versions": ["v1"],
            "v1_submitted": "2026-04-10T23:03:18Z",
            "days_elapsed": DAYS_ELAPSED,
            "n_replacements_since": 0,
            "n_corrections_or_errata": 0,
            "withdrawn": False,
            "journal_ref": None,
            "doi": "https://doi.org/10.48550/arXiv.2604.09949",
        },
        "evidence_kind": "POSITIVE (a retraction or correction would be visible here)",
        "verdict": "NO retraction, NO correction",
    },
    {
        "id": "E2a",
        "channel": "citation graph: Semantic Scholar",
        "url": (
            "https://api.semanticscholar.org/graph/v1/paper/arXiv:2604.09949/"
            "citations?fields=title,year,externalIds,abstract&limit=100"
        ),
        "url_secondary": (
            "https://api.semanticscholar.org/graph/v1/paper/arXiv:2604.09949"
            "?fields=title,year,citationCount,influentialCitationCount,externalIds,venue"
        ),
        "finding": {
            "citations_payload": '{"offset": 0, "data": []}',
            "citation_count": 0,
            "influential_citation_count": 0,
            "venue": "",
            "corpus_id": 287425079,
            "indexed": True,
            "note": (
                "the live CorpusId is what makes this a MEASURED zero rather than an "
                "indexing miss -- the paper is in the index and has no citations"
            ),
        },
        "evidence_kind": "MEASURED ZERO",
        "verdict": "NO independent engagement",
    },
    {
        "id": "E2b",
        "channel": "citation graph: OpenAlex FULL-TEXT search",
        "url": "https://api.openalex.org/works?search=2604.09949&per_page=20",
        "finding": {
            "count": 0,
            "resolved_query": "works where full text has (2604.09949)",
            "note": (
                "full text, not metadata -- would catch a paper discussing the claim "
                "in its body without formally citing it; still zero"
            ),
        },
        "evidence_kind": "MEASURED ZERO (stronger channel than E2a)",
        "verdict": "NO independent engagement",
    },
    {
        "id": "E3",
        "channel": "author feed: Rishad Shahmurov, submittedDate-descending",
        "url": (
            "https://export.arxiv.org/api/query?search_query=au:%22Shahmurov%22"
            "&start=0&max_results=60&sortBy=submittedDate&sortOrder=descending"
        ),
        "finding": {
            "n_submissions_after_source": 8,
            "n_claiming_opposite_for_NS": 6,
            "n_euler_blowup_not_contradictory": 2,
            "n_citing_the_source": 0,
            "submissions_after": [
                {
                    "arxiv": "2604.21213",
                    "date": "2026-04-23",
                    "version": "v1",
                    "title": (
                        "Axisymmetric Navier--Stokes with Swirl: Final Master "
                        "Manuscript for the Unconditional Global Existence Program"
                    ),
                    "direction": "GLOBAL EXISTENCE -- contradicts the source",
                },
                {
                    "arxiv": "2605.01873",
                    "date": "2026-05-03",
                    "version": "v2",
                    "title": (
                        "Large-Data Global Regularity for Three-Dimensional "
                        "Navier--Stokes II: ... Full System"
                    ),
                    "direction": "GLOBAL REGULARITY, FULL SYSTEM -- contradicts",
                },
                {
                    "arxiv": "2605.01875",
                    "date": "2026-05-03",
                    "version": "v3",
                    "title": (
                        "Large-Data Global Regularity for Three-Dimensional "
                        "Navier--Stokes I: ... Axisymmetric Swirl Class"
                    ),
                    "direction": "GLOBAL REGULARITY -- contradicts",
                },
                {
                    "arxiv": "2605.04181",
                    "date": "2026-05-05",
                    "version": "v1",
                    "title": "Euler Singularities I: Boundary Blow-Up ...",
                    "direction": "EULER blow-up -- DIFFERENT SYSTEM, not contradictory",
                },
                {
                    "arxiv": "2605.04526",
                    "date": "2026-05-06",
                    "version": "v1",
                    "title": "Euler Singularities II: Interior Quadrupole Blow-Up ...",
                    "direction": "EULER blow-up -- DIFFERENT SYSTEM, not contradictory",
                },
                {
                    "arxiv": "2605.09797",
                    "date": "2026-05-10",
                    "version": "v2",
                    "title": (
                        "A Classical Two-Part First-Threshold Proof of Global "
                        "Smoothness for Navier--Stokes ..."
                    ),
                    "direction": "GLOBAL SMOOTHNESS -- contradicts",
                },
                {
                    "arxiv": "2606.07869",
                    "date": "2026-06-05",
                    "version": "v1",
                    "title": (
                        "Global Regularity for Axisymmetric Navier--Stokes Flows "
                        "with Swirl"
                    ),
                    "direction": "GLOBAL REGULARITY, SAME 5D LIFT -- contradicts",
                },
                {
                    "arxiv": "2606.07875",
                    "date": "2026-06-05",
                    "version": "v1",
                    "title": (
                        "Hypothetical Singularity of 3D Navier-Stokes in Clay "
                        "Institute set up Reduces to Axisymmetric with Swirl class"
                    ),
                    "direction": (
                        "REDUCTION -- composed with 2606.07869 gives global "
                        "regularity for 3D NS, negating the source"
                    ),
                },
            ],
            "the_one_BEFORE_that_matters": {
                "arxiv": "2604.03519",
                "date": "2026-04-03",
                "version": "v1",
                "title": "Unconditional Axis-Regularity in the 5D Corridor",
                "why_it_matters": (
                    "posted SEVEN DAYS BEFORE the singularity paper, already claiming "
                    "UNCONDITIONAL regularity for 3D axisymmetric NS via the SAME "
                    "dmu_5 = r^3 dr dz five-dimensional radial lift -- so the two "
                    "contradictory lines ran SIMULTANEOUSLY, and the singularity "
                    "paper is not an earlier position later superseded"
                ),
            },
            "revision_asymmetry": (
                "the regularity line is ACTIVELY MAINTAINED (2605.01875 at v3, "
                "2605.01873 and 2605.09797 at v2) while the singularity paper has sat "
                "at v1 for 118 days with 0 revisions -- abandoned by revealed "
                "preference"
            ),
        },
        "evidence_kind": "POSITIVE, about the one person most likely to correct it",
        "verdict": (
            "NO independent verdict, but a DE FACTO SELF-REFUTATION -- reported "
            "prominently, recorded as PROVENANCE evidence and NOT as a retraction"
        ),
    },
    {
        "id": "E4a",
        "channel": "document fetch: the full-system regularity paper",
        "url": "https://arxiv.org/html/2605.01873",
        "finding": {
            "theorem": (
                "Thm 2.1: 'Let u_0 in C_c^infty(R^3) be divergence-free ... Then "
                "T_+ = infinity' -- the solution is global, for the FULL 3D system"
            ),
            "n_bibliography_entries": 23,
            "n_self_citations": 0,
            "cites_2604_09949": False,
            "acknowledges_contradiction": False,
        },
        "verdict": "contradicts the source; does not mention it",
    },
    {
        "id": "E4b",
        "channel": "document fetch: the axisymmetric regularity paper, SAME 5D lift",
        "url": "https://arxiv.org/html/2606.07869",
        "finding": {
            "theorem": (
                "Thm 1.1: 'Let u_0 in C_c^infty(R^3) be divergence-free and "
                "axisymmetric ... Then T* = infinity'"
            ),
            "machinery": (
                "sec 2.4: 'The five-dimensional lifted measure is dmu_5 = r^3 dr dz', "
                "Delta_5 = d_rr + 3 r^-1 d_r + d_zz; Lemma 3.1 'Lifted G-equation' -- "
                "the SAME 5D lift named in 2604.09949's own title"
            ),
            "cites_2604_09949": False,
            "retracts_or_corrects": False,
            "acknowledges_contradiction": False,
        },
        "verdict": "contradicts the source with the source's own machinery; silent on it",
    },
    {
        "id": "E5",
        "channel": "false-positive check: the nearest independent audit candidate",
        "url": "https://arxiv.org/abs/2606.25341",
        "finding": {
            "title": "A Structural Audit of Navier-Stokes Obstruction Calculus",
            "author": "Runlong Yu",
            "topic": (
                "CKN-badness across scales; concludes 'no unconditional single-scale "
                "domination by a signed combined-work detector is available'"
            ),
            "mentions_2604_09949": False,
            "mentions_shahmurov": False,
            "is_a_response_paper": False,
            "method": "FETCHED AND READ, not pattern-matched on the title",
        },
        "verdict": "CLEARED -- not a response to the source",
    },
]

GATE_ANSWER = {
    "answer": "NO",
    "as_of": PASS_DATE,
    "restated": (
        "No independent group has published a confirmation, refutation, retraction, "
        "or correction of arXiv:2604.09949 in the 118 days since it was posted."
    ),
    "channels_checked": 4,
    "channels_returning_an_independent_verdict": 0,
    "qualifying_finding": (
        "THE AUTHOR HIMSELF has published 6 papers claiming the logically opposite "
        "result for 3D Navier-Stokes in the 56 days from 2026-04-23 to 2026-06-05, "
        "using the same 5D-lifted axisymmetric machinery, 0 of which cite "
        "2604.09949 -- a de facto self-refutation, though NOT a retraction"
    ),
    "m5_action": (
        "CONFIRMED CURRENT, not stale. M-5's CLAIMED_UNUSABLE stands and is "
        "STRENGTHENED by a third independent reason (author's own corpus asserts the "
        "negation). M-5's reason (ii) -- the exactly-backward self-similar solution "
        "excluded by Necas-Ruzicka-Sverak and Tsai -- remains the LOAD-BEARING one, "
        "because it says WHICH of the two contradictory lines is wrong, and a "
        "self-contradicting corpus does not."
    ),
    "ledger_action": (
        "NONE. solver/target_selection.py's rank-6 entry 'claimed by "
        "arXiv:2604.09949' is confirmed current; this leg never opened that file for "
        "writing."
    ),
}

OUR_STANDING_POSITION = {
    "m5_arithmetic_audit": {
        "two_delta_M_K": 8.9e-5,
        "kantorovich_two_M2_K_delta": 4.3e-2,
        "kantorovich_margin_factor": 23.0,
        "K_reproduction_relative_error": 2.2e-4,
        "reading": (
            "THE ARITHMETIC IS NOT WHERE IT FAILS, and M-5 said so. This leg does "
            "not revisit the arithmetic and does not need to."
        ),
    },
    "m5_reasons_unusable": [
        "(i) no verification package released (its appendix F/E)",
        (
            "(ii) Thm 12.1 reconstructs the exactly-BACKWARD self-similar solution "
            "excluded by Necas-Ruzicka-Sverak and Tsai -- LOAD-BEARING"
        ),
        (
            "(iii) NEW, this leg: the author's own subsequent corpus asserts the "
            "negation -- cheaper to state, but WEAKER AS MATHEMATICS (provenance, "
            "not proof)"
        ),
    ],
    "status_unchanged": "CLAIMED_UNUSABLE: not certified, not open",
    "only_known_independent_check": (
        "as far as four channels can determine, M-5 is the ONLY independent check of "
        "arXiv:2604.09949 that exists anywhere"
    ),
}

LIMITATIONS = [
    (
        "ALL FOUR CHANNELS SEE ONLY THE PUBLIC RECORD. A referee report, a private "
        "erratum, a seminar dismissal, or a comment on a version of record would be "
        "invisible to every one of them. What is claimed is the public record."
    ),
    (
        "A 118-day-old single-author preprint sits near the edge of index lag. E2a is "
        "mitigated by the live CorpusId and E2b by being full-text, but neither is "
        "immune."
    ),
    (
        "THE SELF-CONTRADICTION IS INFERENCE, NOT A STATEMENT. No paper in the corpus "
        "says '2604.09949 is withdrawn' or 'supersedes'. The incompatibility is read "
        "off theorem statements (T_+ = infinity / T* = infinity versus finite-time "
        "singularity). Strong reading, but a reading -- it must NOT be reported as "
        "'the author retracted', because he did not."
    ),
    (
        "The 2 Euler blow-up papers (2605.04181, 2605.04526) are a DIFFERENT system "
        "and are explicitly NOT counted as contradictory, so the 6 is a floor on "
        "honesty rather than a maximised headline."
    ),
]


def build() -> dict:
    return {
        "leg": 93,
        "route": "EXT5",
        "kind": "literature watch -- no computation",
        "pass_date": PASS_DATE,
        "gate": GATE,
        "gate_answer": GATE_ANSWER,
        "source_paper": {
            "arxiv": SOURCE_ARXIV,
            "v1_date": SOURCE_V1_DATE,
            "current_version": "v1",
            "days_elapsed": DAYS_ELAPSED,
            "n_replacements": 0,
            "withdrawn": False,
            "journal_ref": None,
        },
        "queries": QUERIES,
        "endpoints": ENDPOINTS,
        "our_standing_position": OUR_STANDING_POSITION,
        "limitations": LIMITATIONS,
        "bans_respected": [
            "no gCLM measurement leg -- nothing here computes anything",
            "no Route-D bound sharpening -- no bound is touched",
            "no DSS re-ask -- the DSS lane is not entered",
            (
                "capabilities.py grepped before writing (solver/target_selection.py "
                "registered at line 387, solver/literature_gates.py at 311); nothing "
                "built, nothing edited"
            ),
            "solver/target_selection.py read-only -- never opened for writing",
            (
                "the five shared ledgers untouched: PHASE2_P2_NOTES.md, "
                "LITERATURE_CHECK.md, DIRECTION.md, plan_of_record.py, "
                "CONTINUATION_PROMPT.md"
            ),
        ],
    }


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(
        here, "..", "writeup", "data", "p2_route_ext5_v1_target_watch5.json"
    )
    payload = build()
    with open(os.path.normpath(out), "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)
        fh.write("\n")

    ans = payload["gate_answer"]
    src = payload["source_paper"]
    e3 = next(e for e in ENDPOINTS if e["id"] == "E3")["finding"]

    print("Route-EXT5 v1 (leg 93) -- dated literature watch, no computation")
    print("  gate:", GATE)
    print("  ANSWER:", ans["answer"], "as of", ans["as_of"])
    print(
        "  channels: %d checked, %d returned an independent verdict"
        % (ans["channels_checked"], ans["channels_returning_an_independent_verdict"])
    )
    print(
        "  source: arXiv:%s still at %s after %d days, %d replacements, withdrawn=%s, "
        "journal-ref %s"
        % (
            SOURCE_ARXIV,
            src["current_version"],
            src["days_elapsed"],
            src["n_replacements"],
            src["withdrawn"],
            src["journal_ref"],
        )
    )
    print("  citations: Semantic Scholar %d (CorpusId %d, so indexed), OpenAlex "
          "full-text %d"
          % (
              next(e for e in ENDPOINTS if e["id"] == "E2a")["finding"]["citation_count"],
              next(e for e in ENDPOINTS if e["id"] == "E2a")["finding"]["corpus_id"],
              next(e for e in ENDPOINTS if e["id"] == "E2b")["finding"]["count"],
          ))
    print(
        "  AUTHOR CORPUS: %d submissions since; %d claim the OPPOSITE result for NS, "
        "%d are Euler (different system), %d cite the source"
        % (
            e3["n_submissions_after_source"],
            e3["n_claiming_opposite_for_NS"],
            e3["n_euler_blowup_not_contradictory"],
            e3["n_citing_the_source"],
        )
    )
    print("  ->", ans["qualifying_finding"])
    print("  M-5 action:", ans["m5_action"])
    print("  ledger action:", ans["ledger_action"])
    print("  queries logged:", len(QUERIES), "| endpoints logged:", len(ENDPOINTS))
    print("  wrote", os.path.normpath(out))


if __name__ == "__main__":
    main()
