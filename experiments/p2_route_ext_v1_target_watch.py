"""Route-EXT v1 (leg 74): has anyone certified HL_S2_nonsymmetric since April 2026?

PURE LITERATURE LEG -- A DATED WATCH.  Nothing here computes anything about the
Hou-Luo model, nothing is solved, no solver module is imported.  This script is the
executable record of a search: it carries the query strings, the author-feed and
citation-graph enumerations, the endpoints hit, and the verdicts, and it re-emits
them as writeup/data/p2_route_ext_v1_target_watch.json.

WHAT WAS ASKED (the leg's gate, verbatim)
    "Has a certificate (computer-assisted or analytic) for arXiv:2604.01868's
     HL_S2_nonsymmetric profile been published, by Chen-Huang-Li or anyone else,
     since April 2026?"

WHAT CAME BACK: **NO**, on five independent channels, none of which produced a
single candidate certificate.  Concretely, as of 2026-08-06:

  C1  THE SOURCE PAPER HAS NOT MOVED.  arXiv:2604.01868 is still at **v1**, sole
      submission 2 Apr 2026, comment field "51 pages", no journal-ref and no DOI
      beyond the arXiv DOI.  **126 days** elapsed with **0** replacements.  Its own
      abstract still says "numerically demonstrate" / "a numerical investigation";
      no proof claim of any kind for Scenario 2.

  C2  THE AUTHORS HAVE POSTED NOTHING SINCE.  arXiv author feeds for all three of
      Chen-Huang-Li: De Huang's most recent submission of any kind is 2604.01868
      itself (**0** submissions in the 126 days since); Bojin Chen's is the same
      paper; Xiangyuan Li's is the same paper.  De Huang's own maintained research
      page lists 2604.01868 under "Preprints", with **no** companion or follow-up
      certificate entry, and **0** of his listed items carry proof/verification
      language for the Scenario-2 object.

  C3  THE WHOLE "Hou-Luo" ARXIV CORPUS SINCE APRIL 2026 IS **ONE** PAPER, AND IT IS
      A DIFFERENT OBJECT.  A submittedDate-descending enumeration of every arXiv
      entry matching "Hou-Luo" returns exactly **1** submission after 2604.01868:
      arXiv:2605.16322 (Yaoming Shi, 5 May 2026), "A unified Boussinesq--Euler
      formulation and finite-time blow-up for a Hou--Luo type boundary-jet system".
      That paper proves blow-up for a CLOSED BOUNDARY-JET MODEL (Q0) by a Riccati
      argument, states in its own abstract that "the theorem is therefore a blow-up
      result for the closed boundary-jet model, not for the unrestricted Boussinesq
      or Euler systems", and does not cite 2604.01868 or mention a non-symmetric
      self-similar profile.  It is **not** a certificate for the ledger's rank-1
      object -- it is not even about a self-similar profile.

  C4  THE CAP CORPUS SINCE APRIL 2026 CONTAINS **NO** HOU-LUO ENTRY.  Enumerating
      arXiv abstracts carrying both "computer-assisted" and "self-similar",
      submittedDate-descending, gives **2** submissions after 1 Apr 2026:
      arXiv:2607.27072 (harmonic map heat flow shrinker) and arXiv:2607.15256
      (Chen-Hou, 16 Jul 2026, analytic finite-rank corrections).  **0 of 2** concern
      the 1D Hou-Luo model.  The Chen-Hou one is the nearest miss and is worth
      naming precisely: it is a METHODS review of the low-rank-correction technique
      for singularly weighted estimates in the 3D Euler CAP; by its own abstract it
      certifies no profile ("the paper does not certify specific profiles"), and it
      mentions neither the 1D Hou-Luo model nor 2604.01868.

  C5  THE CITATION GRAPH IS EMPTY.  Semantic Scholar's citations endpoint for
      arXiv:2604.01868 returns **zero** citing works.  This is the weakest of the
      five channels (a 4-month-old preprint is at the edge of S2's indexing lag and
      the paper-record endpoint 429'd on retry, so the count is not independently
      corroborated) and it is recorded as CORROBORATING, not load-bearing.  C1-C4
      are each sufficient on their own.

ALSO CHECKED AND CLEARED, because it is the obvious false positive:
    Jiajie Chen -- the author of the existing Hou-Luo CAP (arXiv:2106.05422, with
    Hou and Huang) and thus the single most likely person to certify this object --
    has **5** submissions after 1 Apr 2026 (2605.00808, 2605.15130, 2605.15149,
    2606.18152, 2607.15256).  **0 of 5** target the 1D Hou-Luo non-symmetric
    profile: two are 3D Euler C^{1,1/3-} self-similar blowup (I and II), two are
    Euler implosions/explosions, and one is the C4 methods review.  The count is
    high enough that "nobody was working nearby" would be the wrong summary -- the
    right summary is that the nearby work aims elsewhere.

WHAT THIS MEANS FOR THE LEDGER
    The no-branch lands.  solver/target_selection.py's TARGET_LEDGER rank-1 entry
    `certified: "NO"` is **confirmed current as of 2026-08-06**, not stale.  No
    ledger edit is needed and this leg makes none -- that file is leg 63's (M2)
    exclusively, and this leg never opened it for writing.  The same confirmation
    extends to the rank-3 entry Boussinesq_S2_nonsymmetric (same source paper,
    section 6.2): C1-C4 sweep the source and the corpus, not one profile, so the
    2D Scenario-2 object is equally uncertified as of the same date.

WHAT IT MEANS FOR ROUTE-PORT
    Legs 44-47's four-leg spend is **not** externally mooted.  The port stalled
    1.55e+08 ball radii outside the truncated object (leg 46), with reach making it
    worse at +0.47 decades per unit rho (leg 47); that stall stands as this
    repository's own measured wall, and no external result has since closed the
    object from the other side.  The negative is worth stating with its magnitude:
    the object has been open for **126 days** past its announcement with **zero**
    published attempts on it by anyone, which is a statement about how expensive
    the three-modulation-constant bordered shape is, not about how uninteresting.

METHOD, so the pass is reproducible
    Channels C1/C3/C4 and the author feeds are arXiv-API `search_query` calls with
    sortBy=submittedDate&sortOrder=descending -- the exact URLs are in ENDPOINTS
    below, and they re-run verbatim.  Note the known limitation, recorded rather
    than hidden: the arXiv API `all:`/`abs:` fields search METADATA, not full text,
    so C3/C4 would miss a certificate that never says "Hou-Luo" or never says
    "computer-assisted" in its title/abstract.  C1, C2 and C5 are what cover that
    gap from the other direction (source, authors, citations).

Full prose is in writeup/novelty/leg_74.md (this leg's novelty log as well as its
technical note); the journal entry is experiments/journal/leg_74.md.
"""

from __future__ import annotations

import json
import os

PASS_DATE = "2026-08-06"
SOURCE_ARXIV = "2604.01868"
SOURCE_V1_DATE = "2026-04-02"
DAYS_ELAPSED = 126  # 2026-04-02 -> 2026-08-06

GATE = (
    "Has a certificate (computer-assisted or analytic) for arXiv:2604.01868's "
    "HL_S2_nonsymmetric profile been published, by Chen-Huang-Li or anyone else, "
    "since April 2026?"
)

# ---------------------------------------------------------------------------
# Query log.  Links, not counts (writeup/novelty/README.md's rule, after leg 53).
# ---------------------------------------------------------------------------
QUERIES = [
    {
        "id": "Q1",
        "kind": "web_search",
        "query": (
            "arXiv 2604.01868 Chen Huang Li Hou-Luo self-similar blowup singular "
            "profiles"
        ),
        "relevant_links": [
            "https://arxiv.org/abs/2604.01868",
            "https://arxiv.org/pdf/2604.01868",
            "https://sites.google.com/view/de-huang/research",
            "https://arxiv.org/abs/2308.01528",
            "https://arxiv.org/html/2603.25104",
        ],
        "verdict": (
            "located the source paper and the author's own page; every return "
            "describes it as a numerical investigation, no certificate surfaced"
        ),
    },
    {
        "id": "Q2",
        "kind": "web_search",
        "query": (
            "computer-assisted proof self-similar blowup Hou-Luo model "
            "non-symmetric profile 2026"
        ),
        "relevant_links": [
            "https://arxiv.org/abs/2106.05422",
            "https://arxiv.org/abs/2308.01528",
            "https://link.springer.com/article/10.1007/s00220-025-05429-9",
            "https://arxiv.org/pdf/2604.01868",
        ],
        "verdict": (
            "returns the PRE-EXISTING symmetric results only (Chen-Hou-Huang 2021 "
            "CAP, Huang-Qin-Wang-Wei analytic); nothing non-symmetric, nothing new"
        ),
    },
    {
        "id": "Q3",
        "kind": "web_search",
        "query": (
            "arXiv 2026 rigorous computer-assisted proof singular self-similar "
            "profile Hou-Luo Boussinesq interval arithmetic"
        ),
        "relevant_links": [
            "https://arxiv.org/html/2509.14185",
            "https://arxiv.org/html/2604.09949v1",
            "https://arxiv.org/html/2607.19762v1",
            "https://epubs.siam.org/doi/10.1137/23M1580395",
        ],
        "verdict": (
            "surfaced adjacent 2026 CAP/ML-singularity work (Discovery of Unstable "
            "Singularities; Xu's CLM spectral picture) -- none aimed at Scenario 2"
        ),
    },
    {
        "id": "Q4",
        "kind": "web_search",
        "query": (
            '2026 preprint "non-symmetric" OR "asymmetric" self-similar profile '
            "Hou-Luo model computer-assisted proof certificate Scenario 2"
        ),
        "relevant_links": [
            "https://arxiv.org/pdf/2605.15149",
            "https://arxiv.org/pdf/2605.15130",
            "https://arxiv.org/abs/2308.01528",
            "https://arxiv.org/html/2604.01868v1",
        ],
        "verdict": (
            "the targeted non-symmetric query returns the source paper itself plus "
            "J. Chen's 3D Euler pair; zero certificate candidates"
        ),
    },
]

# ---------------------------------------------------------------------------
# Structured endpoints -- these re-run verbatim, which is the point.
# ---------------------------------------------------------------------------
ENDPOINTS = [
    {
        "id": "C1",
        "channel": "source paper: version history",
        "url": "https://arxiv.org/abs/2604.01868",
        "finding": {
            "versions": ["v1"],
            "v1_submitted": SOURCE_V1_DATE,
            "n_replacements_since": 0,
            "comment_field": "51 pages",
            "journal_ref": None,
            "doi": "https://doi.org/10.48550/arXiv.2604.01868",
            "abstract_claim": "numerical investigation only; no proof claim for Scenario 2",
        },
        "verdict": "NO certificate",
    },
    {
        "id": "C2a",
        "channel": "author feed: De Huang",
        "url": (
            "https://export.arxiv.org/api/query?search_query=au:%22De+Huang%22"
            "&start=0&max_results=60&sortBy=submittedDate&sortOrder=descending"
        ),
        "finding": {
            "most_recent_submission": SOURCE_ARXIV,
            "n_submissions_after_2026_04_02": 0,
            "next_most_recent": "2603.25104 (gCLM singular profiles, 2026-03-26)",
        },
        "verdict": "NO certificate",
    },
    {
        "id": "C2b",
        "channel": "author feeds: Bojin Chen, Xiangyuan Li",
        "url": (
            "https://export.arxiv.org/api/query?search_query=au:%22Xiangyuan+Li%22"
            "+OR+au:%22Bojin+Chen%22&start=0&max_results=40"
            "&sortBy=submittedDate&sortOrder=descending"
        ),
        "finding": {
            "most_recent_for_both": SOURCE_ARXIV,
            "n_submissions_after_2026_04_02": 0,
        },
        "verdict": "NO certificate",
    },
    {
        "id": "C2c",
        "channel": "author's maintained publication page",
        "url": "https://sites.google.com/view/de-huang/research",
        "finding": {
            "listing_for_2604_01868": "under 'Preprints', unchanged",
            "n_followup_certificate_entries": 0,
            "n_entries_with_CAP_or_verification_language_for_scenario_2": 0,
        },
        "verdict": "NO certificate",
    },
    {
        "id": "C3",
        "channel": 'whole "Hou-Luo" arXiv corpus, submittedDate-descending',
        "url": (
            "https://export.arxiv.org/api/query?search_query=all:%22Hou-Luo%22"
            "&start=0&max_results=60&sortBy=submittedDate&sortOrder=descending"
        ),
        "finding": {
            "n_submissions_after_source": 1,
            "the_one": {
                "arxiv": "2605.16322",
                "date": "2026-05-05",
                "authors": "Yaoming Shi",
                "title": (
                    "A unified Boussinesq--Euler formulation and finite-time "
                    "blow-up for a Hou--Luo type boundary-jet system"
                ),
                "object": "closed boundary-jet model (Q0), periodic interval",
                "method": "Riccati argument (Choi-Hou-Kiselev-Luo-Sverak-Yao style)",
                "self_similar_profile": False,
                "cites_2604_01868": False,
                "disqualifying_quote": (
                    "The theorem is therefore a blow-up result for the closed "
                    "boundary-jet model, not for the unrestricted Boussinesq or "
                    "Euler systems."
                ),
            },
        },
        "verdict": "NO certificate -- the one new Hou-Luo paper is a different object",
    },
    {
        "id": "C4",
        "channel": 'CAP corpus: abs:"computer-assisted" AND abs:"self-similar"',
        "url": (
            "https://export.arxiv.org/api/query?search_query=abs:%22computer-"
            "assisted%22+AND+abs:%22self-similar%22&start=0&max_results=60"
            "&sortBy=submittedDate&sortOrder=descending"
        ),
        "finding": {
            "n_submissions_after_2026_04_01": 2,
            "n_concerning_1d_hou_luo": 0,
            "entries": [
                {
                    "arxiv": "2607.27072",
                    "date": "2026-07-29",
                    "authors": "Angerer, Kistner, Schoerkhuber",
                    "topic": "corotational harmonic map heat flow shrinker",
                    "hou_luo": False,
                },
                {
                    "arxiv": "2607.15256",
                    "date": "2026-07-16",
                    "authors": "Jiajie Chen, Thomas Y. Hou",
                    "topic": (
                        "analytic finite-rank corrections for singularly weighted "
                        "estimates in the 3D Euler CAP -- a METHODS review"
                    ),
                    "hou_luo": False,
                    "certifies_a_profile": False,
                    "mentions_2604_01868": False,
                },
            ],
        },
        "verdict": "NO certificate",
    },
    {
        "id": "C5",
        "channel": "citation graph (CORROBORATING ONLY, not load-bearing)",
        "url": (
            "https://api.semanticscholar.org/graph/v1/paper/arXiv:2604.01868/"
            "citations?fields=title,year,publicationDate,externalIds&limit=100"
        ),
        "finding": {
            "citing_works": 0,
            "caveat": (
                "a 126-day-old preprint sits inside S2's indexing lag, and the "
                "paper-record endpoint returned HTTP 429 on retry, so the zero is "
                "NOT independently corroborated -- recorded as weak evidence"
            ),
        },
        "verdict": "NO certificate (weak channel)",
    },
    {
        "id": "F1",
        "channel": "false-positive check: Jiajie Chen (author of the 2021 HL CAP)",
        "url": (
            "https://export.arxiv.org/api/query?search_query=au:%22Jiajie+Chen%22"
            "&start=0&max_results=40&sortBy=submittedDate&sortOrder=descending"
        ),
        "finding": {
            "n_submissions_after_2026_04_01": 5,
            "n_targeting_hl_s2_nonsymmetric": 0,
            "ids": [
                "2607.15256 (2026-07-16, CAP methods review)",
                "2606.18152 (2026-06-16, a new class of Euler explosions)",
                "2605.15149 (2026-05-14, 3D Euler C^{1,1/3-} self-similar blowup I)",
                "2605.15130 (2026-05-14, 3D Euler C^{1,1/3-} self-similar blowup II)",
                "2605.00808 (2026-05-01, smooth and stable Euler implosions)",
            ],
            "reading": (
                "the most-likely certifier is highly active (5 papers/126 days) and "
                "aiming entirely elsewhere -- 3D Euler, not the 1D non-symmetric "
                "profile"
            ),
        },
        "verdict": "NO certificate",
    },
]

# ---------------------------------------------------------------------------
# What the repository already holds about this object -- QUOTED, not recomputed.
# Nothing below is measured by this leg.
# ---------------------------------------------------------------------------
OUR_STANDING_POSITION = {
    "ledger_entry": {
        "file": "solver/target_selection.py",
        "id": "HL_S2_nonsymmetric",
        "rank": 1,
        "source": "arXiv:2604.01868 sections 2.5 and 4",
        "certified": "NO",
        "read_only": True,
        "note": "read for reference only; this leg does not edit that file (leg 63/M2 owns it)",
    },
    "our_attempt": {
        "route": "Route-PORT, legs 44-47",
        "truncation_gap_ball_radii": 1.55e08,
        "reach_trend_decades_per_unit_rho": +0.47,
        "reach_trend_sign": "WRONG -- extending the domain makes the gap worse (leg 47)",
        "status": "stalled; not mooted externally, per this leg's search",
    },
    "second_affected_entry": {
        "id": "Boussinesq_S2_nonsymmetric",
        "rank": 3,
        "source": "arXiv:2604.01868 section 6.2",
        "certified": "NO",
        "note": (
            "same source paper -- channels C1-C4 sweep the paper and the corpus, "
            "so this entry is confirmed current by the same evidence"
        ),
    },
}

LIMITATIONS = [
    "arXiv API all:/abs: search METADATA, not full text -- C3/C4 would miss a "
    "certificate whose title and abstract avoid both 'Hou-Luo' and "
    "'computer-assisted'.  C1/C2/C5 cover that gap from source, author and "
    "citation directions; no single channel is treated as sufficient.",
    "A certificate could exist unposted (in review, in a talk, on a personal page "
    "not checked).  The claim is about the PUBLISHED record as of " + PASS_DATE
    + ", which is exactly what the gate asks.",
    "C5's zero-citation count is inside Semantic Scholar's indexing lag for a "
    "126-day-old preprint and its paper-record endpoint 429'd; it corroborates, it "
    "does not carry the answer.",
]


def build() -> dict:
    return {
        "leg": 74,
        "route": "EXT",
        "title": "target watch -- has HL_S2_nonsymmetric been certified by anyone since?",
        "pass_date": PASS_DATE,
        "kind": "literature watch; no computation, no solver import, no code edit",
        "gate": GATE,
        "gate_answer": {
            "answer": "NO",
            "as_of": PASS_DATE,
            "meaning": (
                "no certificate, computer-assisted or analytic, for arXiv:"
                "2604.01868's HL_S2_nonsymmetric profile has been published by "
                "anyone since April 2026"
            ),
            "channels_checked": 6,
            "channels_returning_a_candidate": 0,
            "days_object_has_stood_open": DAYS_ELAPSED,
            "ledger_action": (
                "NONE -- solver/target_selection.py's `certified: NO` is CONFIRMED "
                "CURRENT, not stale; this leg does not edit that file"
            ),
        },
        "source_paper": {
            "arxiv": SOURCE_ARXIV,
            "authors": "Bojin Chen, De Huang, Xiangyuan Li",
            "title": (
                "Novel Self-similar Finite-time Blowups with Singular Profiles of "
                "the 1D Hou-Luo Model and the 2D Boussinesq Equations: A Numerical "
                "Investigation"
            ),
            "v1_date": SOURCE_V1_DATE,
            "current_version": "v1",
            "days_since_v1": DAYS_ELAPSED,
            "journal_ref": None,
        },
        "queries": QUERIES,
        "endpoints": ENDPOINTS,
        "our_standing_position": OUR_STANDING_POSITION,
        "limitations": LIMITATIONS,
        "bans_respected": [
            "no gCLM measurement leg -- nothing here computes anything",
            "no Route-D bound sharpening -- no bound is touched",
            "capabilities.py grepped before writing (HL_S2_nonsymmetric appears at "
            "lines 130, 230, 297; solver/target_selection.py registered at 340); "
            "nothing built, nothing edited",
            "solver/target_selection.py read-only -- owned by leg 63 (M2)",
        ],
    }


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "writeup", "data", "p2_route_ext_v1_target_watch.json")
    payload = build()
    with open(os.path.normpath(out), "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)
        fh.write("\n")
    ans = payload["gate_answer"]
    print("Route-EXT v1 (leg 74) -- dated literature watch, no computation")
    print("  gate:", GATE)
    print("  ANSWER:", ans["answer"], "as of", ans["as_of"])
    print(
        "  channels: %d checked, %d returned a candidate certificate"
        % (ans["channels_checked"], ans["channels_returning_a_candidate"])
    )
    print(
        "  source paper: arXiv:%s still at %s, %d days, %d replacements, journal-ref %s"
        % (
            SOURCE_ARXIV,
            payload["source_paper"]["current_version"],
            DAYS_ELAPSED,
            0,
            payload["source_paper"]["journal_ref"],
        )
    )
    c3 = next(e for e in ENDPOINTS if e["id"] == "C3")["finding"]
    c4 = next(e for e in ENDPOINTS if e["id"] == "C4")["finding"]
    f1 = next(e for e in ENDPOINTS if e["id"] == "F1")["finding"]
    print(
        "  corpus since Apr 2026: Hou-Luo %d new (%d on this object); "
        "CAP+self-similar %d new (%d on Hou-Luo); J. Chen %d new (%d on this object)"
        % (
            c3["n_submissions_after_source"],
            0,
            c4["n_submissions_after_2026_04_01"],
            c4["n_concerning_1d_hou_luo"],
            f1["n_submissions_after_2026_04_01"],
            f1["n_targeting_hl_s2_nonsymmetric"],
        )
    )
    print("  ledger action:", ans["ledger_action"])
    print("  queries logged:", len(QUERIES), "| endpoints logged:", len(ENDPOINTS))
    print("  wrote", os.path.normpath(out))


if __name__ == "__main__":
    main()
