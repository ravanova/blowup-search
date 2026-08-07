"""Route-HLR2 v1 (leg 291): has ANY later work certified HL_S2_nonsymmetric since stage B
closed?

PURE LITERATURE LEG -- A DATED WATCH, distinct in FRAMING from the EXT family (74/77/82/90/
93/123) though it reuses their channel methodology. Those legs ask "has anything moved in
the outside world since our last watch." This leg asks a narrower, retrospective-facing
question this repository has never asked of its OWN original target SINCE THE PIVOT: stage
B closed (gate NO, leg 126, 2026-08-06) on HL_S2_nonsymmetric, the Clay pivot followed
(leg 0, commit 4ff544a, landed 2026-08-06T22:37:34+01:00 = 21:37:34Z), and no leg of any
kind has re-asked "has anyone certified it" since that pivot -- the EXT family's most recent
landing (leg 123 / Route-EXT6) closed its window at 2026-08-06T11:01:32Z, roughly ELEVEN
HOURS BEFORE the pivot commit. Silence and a checked-and-still-empty answer are different
things to be able to report about this repository's own multi-cycle chain in any future
retrospective.

WHAT WAS ASKED (the leg's gate, verbatim, from DIRECTION.md #291)
    "Has any paper published since stage B's closure (or since this repository's own leg
    55/57 dating of the object) published a rigorous certificate (interval-arithmetic or
    otherwise) for HL_S2_nonsymmetric or a directly equivalent formulation?"

WINDOW BOUNDARY: this leg reports against TWO nested boundaries because the gate names both.
    (i)  since stage B's closure / legs 55-57's dating: 2026-08-05T00:00:00Z (legs 55/57)
         through the pass time below -- roughly 44 hours, the widest reading of the gate.
    (ii) since the pivot specifically (the framing this leg's own thesis foregrounds, and
         the one no other leg has checked): 2026-08-06T21:37:34Z through the pass time --
         roughly 8 hours.
Both boundaries are reported; the gate answer is NO under either.

Full search log, with links (not counts), is in writeup/novelty/leg_291.md, committed
BEFORE this script existed. This script is the executable record of the channels actually
run and their results, re-emitted as writeup/data/p2_route_hlr2_v1_precedent.json.
"""

from __future__ import annotations

import json
import os

PASS_DATE = "2026-08-07"
PASS_TIME_UTC = "2026-08-07T05:30:00Z"

STAGE_B_CLOSE = "2026-08-06T10:58:00Z"        # leg 126 (BX) landing commit d1af212
LEG55_57_DATE = "2026-08-05T00:00:00Z"        # legs 55/57's own dating of the object
PIVOT_COMMIT_TIME = "2026-08-06T21:37:34Z"    # leg 0, commit 4ff544a (converted from +01:00)
EXT6_CLOSE = "2026-08-06T11:01:32Z"           # leg 123 (Route-EXT6), commit de31eb7

WINDOW_WIDE_HOURS = 44   # since leg 55/57's dating, the widest reading of the gate
WINDOW_PIVOT_HOURS = 8   # since the pivot specifically -- the leg's own foregrounded framing

GATE = (
    "Has any paper published since stage B's closure (leg 126) -- or since this "
    "repository's own leg 55/57 dating of the object -- published a rigorous "
    "certificate (interval-arithmetic or otherwise) for HL_S2_nonsymmetric or a "
    "directly equivalent formulation?"
)

GATE_ANSWER = {
    "answer": "NO",
    "as_of": PASS_TIME_UTC,
    "restated": (
        "No paper meeting the gate has been published in either window checked: "
        "the wide one (since legs 55/57's dating, " + LEG55_57_DATE + ", roughly "
        + str(WINDOW_WIDE_HOURS) + " hours) or the narrow one this leg's own thesis "
        "foregrounds (since the pivot, " + PIVOT_COMMIT_TIME + ", roughly "
        + str(WINDOW_PIVOT_HOURS) + " hours). The object remains open exactly as "
        "legs 54/55/57/126 last measured it: numerical only, no proof of any kind."
    ),
    "distinctness_from_ext_family": (
        "Leg 123 (Route-EXT6) closed its own window at " + EXT6_CLOSE + ", roughly "
        "eleven hours BEFORE the pivot commit (" + PIVOT_COMMIT_TIME + "). No leg of "
        "any kind -- EXT-family or otherwise -- has re-asked this question since the "
        "pivot until this one. This leg's channels below independently re-run the "
        "check rather than citing EXT6's now-superseded window."
    ),
    "channels_checked": 14,
    "channels_returning_a_candidate_inside_either_window": 0,
    "channels_unavailable": 0,
    "decisive_channel": (
        "C7: the entire math.AP firehose, newest-first. Its newest entry as of the "
        "pass time (arXiv:2608.06371, submitted 2026-08-06T17:58:36Z) predates the "
        "PIVOT (2026-08-06T21:37:34Z) by roughly 4h39m -- i.e. zero math.AP papers of "
        "any kind have been announced since the pivot, so the negative for the narrow "
        "window is an enumeration of the entire relevant firehose, not a keyword-luck "
        "argument. (It is inside the wide window, but is unrelated -- see ENDPOINTS.)"
    ),
    "near_miss_recorded_not_a_yes": (
        "OpenAlex full-text search for the literal string '2604.01868' surfaces "
        "exactly one paper, arXiv:2605.15130 (Jiajie Chen, 'Asymptotically "
        "Self-Similar Blowup for 3D Incompressible Euler with C^{1,1/3-} Velocity "
        "II'), which cites the Chen-Huang-Li 1D construction as a companion input. "
        "It is a FIXED-POINT ANALYTIC (not computer-assisted, not interval-"
        "arithmetic) construction of a DIFFERENT object -- a 3D axisymmetric Euler "
        "profile lifted FROM a 1D profile, not a certificate of "
        "HL_S2_nonsymmetric itself -- and it predates both windows: submitted "
        "2026-05-14, more than 11 weeks before stage B closed."
    ),
    "ledger_action": (
        "NONE. solver/*.py and capabilities.py are not opened for writing anywhere "
        "in this leg; territory is literature-only, taken literally, matching the "
        "EXT-family's own convention for this class of leg."
    ),
}

# ---------------------------------------------------------------------------
# Structured endpoints -- these re-run verbatim, which is the point.
# ---------------------------------------------------------------------------
ENDPOINTS = [
    {
        "id": "C1a",
        "channel": "source paper version history: arXiv:2604.01868 (Chen-Huang-Li)",
        "url": "https://export.arxiv.org/api/query?id_list=2604.01868&max_results=1",
        "finding": {"version": "v1", "updated": "2026-04-02T10:25:28Z", "changed_since_pivot": False},
        "verdict": "unchanged -- still v1, no revision adding a rigorous certificate",
    },
    {
        "id": "C1b",
        "channel": "source paper version history: arXiv:2603.25104 (Huang-Tong-Wang, gCLM one-scale, adjacent object)",
        "url": "https://export.arxiv.org/api/query?id_list=2603.25104&max_results=1",
        "finding": {"version": "v2", "updated": "2026-06-16T04:42:10Z", "changed_since_pivot": False},
        "verdict": "unchanged",
    },
    {
        "id": "C2a",
        "channel": "author enumeration, newest-first: De Huang",
        "url": "https://export.arxiv.org/api/query?search_query=au:%22De_Huang%22&sortBy=submittedDate&sortOrder=descending&max_results=3",
        "finding": {"newest": "arXiv:2604.01868v1 (the source itself)", "newer_entry_since_pivot": False},
        "verdict": "nothing newer than the source paper",
    },
    {
        "id": "C2b",
        "channel": "author enumeration, newest-first: Bojin Chen",
        "url": "https://export.arxiv.org/api/query?search_query=au:%22Bojin_Chen%22&sortBy=submittedDate&sortOrder=descending&max_results=3",
        "finding": {"newest": "arXiv:2604.01868v1 (the source itself)", "newer_entry_since_pivot": False},
        "verdict": "nothing newer",
    },
    {
        "id": "C2c",
        "channel": "author enumeration, newest-first: Xiangyuan Li",
        "url": "https://export.arxiv.org/api/query?search_query=au:%22Xiangyuan_Li%22&sortBy=submittedDate&sortOrder=descending&max_results=5",
        "finding": {"newest": "arXiv:2604.01868v1 (the source itself)", "newer_entry_since_pivot": False},
        "verdict": "nothing newer",
    },
    {
        "id": "C2d",
        "channel": "author research page (De Huang, sites.google.com/view/de-huang/research), fetched directly",
        "url": "https://sites.google.com/view/de-huang/research",
        "finding": {
            "hou_luo_papers_listed": [
                "Huang-Qin-Wang-Wei, CMP 406(10):243 (2025)",
                "Chen-Hou-Huang, Annals of PDE 8(2):24 (2022)",
                "Huang-Tong-Wang, arXiv:2603.25104",
                "Chen-Huang-Li, arXiv:2604.01868",
            ],
            "certificate_followup_listed": False,
        },
        "verdict": "no successor paper listed by the author himself as of the pass time",
    },
    {
        "id": "C3",
        "channel": "Semantic Scholar citations of arXiv:2604.01868",
        "url": "https://api.semanticscholar.org/graph/v1/paper/arXiv:2604.01868/citations?fields=title,externalIds,publicationDate&limit=20",
        "finding": {"citation_count": 0},
        "verdict": "zero citing works of any kind",
    },
    {
        "id": "C4a",
        "channel": "OpenAlex citations of arXiv:2604.01868 (OpenAlex work W7148668037)",
        "url": "https://api.openalex.org/works?filter=cites:W7148668037&per_page=10",
        "finding": {"citation_count": 0},
        "verdict": "zero citing works, consistent with C3",
    },
    {
        "id": "C4b",
        "channel": "OpenAlex full-text search for the literal string 2604.01868",
        "url": "https://api.openalex.org/works?filter=fulltext.search:2604.01868&per_page=5",
        "finding": {"hits": 1, "hit": "arXiv:2605.15130 (Jiajie Chen)", "predates_both_windows": True},
        "verdict": "one mention, a DIFFERENT object (3D Euler lift), predates stage B's close by 11+ weeks -- recorded in GATE_ANSWER.near_miss_recorded_not_a_yes, not a YES",
    },
    {
        "id": "C5",
        "channel": "arXiv keyword enumeration: non-symmetric AND self-similar",
        "url": "https://export.arxiv.org/api/query?search_query=abs:%22non-symmetric%22+AND+abs:%22self-similar%22&sortBy=submittedDate&sortOrder=descending&max_results=10",
        "finding": {"newest_on_topic": None, "newest_any": "arXiv:2605.27974 (2026-05-27, unrelated -- Dirichlet forms)"},
        "verdict": "newest entry predates both windows and is off-topic on the generic keyword match",
    },
    {
        "id": "C6",
        "channel": "arXiv keyword enumeration: interval arithmetic AND self-similar",
        "url": "https://export.arxiv.org/api/query?search_query=abs:%22interval+arithmetic%22+AND+abs:%22self-similar%22&sortBy=submittedDate&sortOrder=descending&max_results=10",
        "finding": {"newest": "arXiv:2604.09949 (2026-04-10, already-known, CLAIMED_UNUSABLE per PHASE2_P2_NOTES M-5)"},
        "verdict": "newest hit predates both windows and is the already-audited unusable 3D-NS claim, not on this object",
    },
    {
        "id": "C7",
        "channel": "raw math.AP firehose, newest-first (window-bounding channel, same role as EXT6's A13)",
        "url": "https://export.arxiv.org/api/query?search_query=cat:math.AP&sortBy=submittedDate&sortOrder=descending&max_results=15",
        "finding": {
            "newest_entry": "arXiv:2608.06371",
            "newest_entry_submitted": "2026-08-06T17:58:36Z",
            "predates_pivot_by_hours": 4.65,
            "is_inside_wide_window": True,
            "is_inside_pivot_window": False,
        },
        "verdict": (
            "zero math.AP papers of any kind announced since the pivot as of the pass "
            "time -- the pivot-window negative is a full-firehose enumeration, not "
            "keyword luck"
        ),
    },
]

QUERIES = [
    {
        "id": "W1",
        "kind": "web_search",
        "query": "Chen Huang Li non-symmetric self-similar Hou-Luo profile certificate interval arithmetic 2026",
        "relevant_links": [
            "https://arxiv.org/pdf/2604.01868",
            "https://arxiv.org/pdf/2308.01528",
            "https://arxiv.org/pdf/2106.05422",
        ],
        "verdict": (
            "returns the source paper and the two already-known analytic exclusions "
            "(2308.01528, 2106.05422); no certificate of the non-symmetric branch"
        ),
    },
    {
        "id": "W2",
        "kind": "web_search",
        "query": 'computer-assisted proof "Hou-Luo" non-symmetric blowup profile arXiv 2604.01868',
        "relevant_links": [
            "https://arxiv.org/pdf/2604.01868",
            "https://link.springer.com/article/10.1007/s00220-025-05429-9",
            "https://sites.google.com/view/de-huang/research",
        ],
        "verdict": (
            "the Springer link is the already-known Huang-Qin-Wang-Wei CMP publication "
            "(the SYMMETRIC smooth-profile branch, an exclusion, not this object); "
            "the author's own page (C2d) lists no successor; nothing new"
        ),
    },
]


def run() -> dict:
    n_channels = len(ENDPOINTS)
    n_candidates = 0
    result = {
        "leg": 291,
        "route": "HLR2",
        "pass_date": PASS_DATE,
        "pass_time_utc": PASS_TIME_UTC,
        "object": (
            "HL_S2_nonsymmetric -- the strictly positive, regular, non-symmetric "
            "self-similar profile of the 1D Hou-Luo model, Chen-Huang-Li arXiv:2604.01868 "
            "sec 2.5/sec 4, numerical only at last measurement (legs 54/55/57/126)"
        ),
        "gate": GATE,
        "windows": {
            "wide_since_leg55_57_dating": {"open": LEG55_57_DATE, "close": PASS_TIME_UTC, "approx_hours": WINDOW_WIDE_HOURS},
            "narrow_since_pivot": {"open": PIVOT_COMMIT_TIME, "close": PASS_TIME_UTC, "approx_hours": WINDOW_PIVOT_HOURS},
            "stage_b_close": STAGE_B_CLOSE,
            "ext6_close_for_reference_only": EXT6_CLOSE,
        },
        "endpoints": ENDPOINTS,
        "web_queries": QUERIES,
        "gate_answer": GATE_ANSWER,
        "n_channels_checked": n_channels + len(QUERIES),
        "n_channels_with_a_candidate": n_candidates,
    }
    return result


def main() -> None:
    data = run()
    out_path = os.path.join(
        os.path.dirname(__file__), "..", "writeup", "data", "p2_route_hlr2_v1_precedent.json"
    )
    out_path = os.path.normpath(out_path)
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=False)
        f.write("\n")
    print(f"wrote {out_path}")
    print(f"GATE ANSWER: {data['gate_answer']['answer']}")
    print(f"channels checked: {data['n_channels_checked']}, candidates found: {data['n_channels_with_a_candidate']}")


if __name__ == "__main__":
    main()
