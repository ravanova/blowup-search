"""Route-EXT6 v1 (leg 123): has ANY new result appeared, by any method, that certifies
an inviscid self-similar blow-up profile OR completes a computer-assisted gCLM a>0
blow-up certificate, since the EXT-family's last window closed?

PURE LITERATURE LEG -- A DATED WATCH.  Nothing here computes anything, no solver
module is imported, no bound is touched.  Unlike legs 74/77/82/90 this leg does not
even READ solver/target_selection.py -- the territory says literature-only and this
leg takes that literally.  This script is the executable record of a search: it
carries the query strings, the endpoints hit, and the verdicts, and it re-emits them
as writeup/data/p2_route_ext6_v1_target_watch6.json.

Distinct in KIND from legs 74/77/82/90/93.  Those five each watched a SPECIFIC named
object (rank 1 HL_S2_nonsymmetric, rank 2 gCLM_degenerate_one_scale, rank 3
Boussinesq_S2_nonsymmetric, rank 4's Conjecture 2.4) or a SPECIFIC claimed paper
(arXiv:2604.09949).  This leg's gate is deliberately WIDER: "by any method" for
gate (a) means the search is not restricted to Chen-Huang-Li's or Huang-Tong-Wang's
own corpora, and covers any inviscid model (Euler, Boussinesq, gCLM, Hou-Luo, gSQG,
...), not just the four ranked ones.

WHAT WAS ASKED (the leg's gate, verbatim, from DIRECTION.md)
    "Has any result been published since the last EXT-family window that either
     (a) certifies an inviscid self-similar blow-up profile by any method, or
     (b) completes a computer-assisted gCLM a>0 blow-up certificate?"

WINDOW BOUNDARY: the EXT family's last window closed with leg 93 (Route-EXT5),
commit 067b7ac, landed 2026-08-06T00:35:44Z.  This leg's channels ran 2026-08-06,
10:49-10:56 UTC, roughly ten hours later.

WHAT CAME BACK: **NO.**  Zero of thirteen arXiv-side channels, and one working
citation-index channel (Semantic Scholar; OpenAlex was budget-exhausted for the day
and is logged as UNAVAILABLE, not as a zero), return any candidate filed, revised, or
newly citing in the window.  The single strongest fact: channel A13 enumerates the
ENTIRE math.AP firehose newest-first, and its newest entry (arXiv:2608.05128,
submitted 2026-08-05T17:51:33Z) predates the window's open (2026-08-06T00:35:44Z) --
i.e. as of the pass time, arXiv's daily announcement batch for 2026-08-06 had not yet
posted AT ALL, so the negative for both gate branches is not a keyword-luck argument,
it is an enumeration of the entire relevant firehose over the window.

WHAT ELSE FELL OUT (recorded, but explicitly NOT a YES on this leg's gate)
    arXiv:2605.19716 (Shao-Wei-Zhang-Zhang, v1 2026-05-19, v2 2026-07-22) is a fully
    analytic (fixed-point, not computer-assisted) certificate of a self-similar
    d-dimensional axisymmetric Euler blow-up profile, C^{1,(1-2/d)-} regularity, with
    a finite-codimensional stability result -- genuinely inside gate (a)'s broad
    wording "by any method", and a genuine miss by legs 74/77/82/90's narrower,
    model-specific queries (none of which were shaped to catch a different equation
    family's own construction).  It does NOT trigger a YES here because it predates
    the window by more than two months even at v2 -- it was not published SINCE the
    last window closed, it was already sitting in the corpus, unrevised, well before
    leg 93 ran.  Recorded as FF1 so a future re-ask (if the window is ever widened
    back past 2026-05-19) does not have to rediscover it from scratch.

METHOD, so the pass is reproducible
    Channels A1-A13 are direct arXiv API enumerations (export.arxiv.org/api/query),
    sortBy=submittedDate&sortOrder=descending where relevant.  Channel B1 is
    Semantic Scholar's citations endpoint (worked).  Channel B2 is OpenAlex full-text
    search (did NOT work today -- daily API budget exhausted, logged honestly as
    UNAVAILABLE rather than folded into a zero).  W1/W2 are open web searches.  The
    exact URLs are in ENDPOINTS below and re-run verbatim.

    Known limitation, recorded rather than hidden: every channel sees only the
    PUBLIC record as of the pass time.  A referee report, a not-yet-submitted
    manuscript, or a paper sitting in arXiv's moderation queue is invisible to all of
    them -- and, given channel A13's finding that the day's whole announcement batch
    had not posted yet, that specific blind spot is wider than usual for this pass.

Full prose is in writeup/novelty/leg_123.md (this leg's novelty log, committed FIRST,
before this script); the journal entry is experiments/journal/leg_123.md.
"""

from __future__ import annotations

import json
import os

PASS_DATE = "2026-08-06"
WINDOW_OPENED = "2026-08-06T00:35:44Z"  # leg 93 (Route-EXT5) landing, commit 067b7ac
WINDOW_CLOSED_PASS_TIME = "2026-08-06T10:56:00Z"
WINDOW_HOURS = 10

GATE = (
    "Has any result been published since the last EXT-family window that either "
    "(a) certifies an inviscid self-similar blow-up profile by any method, or "
    "(b) completes a computer-assisted gCLM a>0 blow-up certificate?"
)

GATE_ANSWER = {
    "answer": "NO",
    "as_of": PASS_DATE,
    "restated": (
        "No result meeting gate (a) or gate (b) has been published in the window "
        "since the EXT family's last watch (leg 93) closed at "
        + WINDOW_OPENED
        + ", as of this pass at "
        + WINDOW_CLOSED_PASS_TIME
        + " -- a gap of roughly "
        + str(WINDOW_HOURS)
        + " hours."
    ),
    "channels_checked": 17,
    "channels_returning_a_candidate_inside_the_window": 0,
    "channels_unavailable": 1,
    "decisive_channel": (
        "A13: the entire math.AP firehose, newest-first. Its newest entry "
        "(arXiv:2608.05128, submitted 2026-08-05T17:51:33Z) predates the window's "
        "open -- arXiv's daily announcement batch for 2026-08-06 had not posted at "
        "all as of the pass time, so the negative is an enumeration of the whole "
        "relevant firehose over the window, not a keyword-luck argument."
    ),
    "false_friend_recorded_not_a_yes": (
        "FF1, arXiv:2605.19716 (Shao-Wei-Zhang-Zhang) -- a genuine analytic "
        "certificate of a self-similar Euler blow-up profile by a method none of "
        "the four ranked objects use, and a real gap in legs 74/77/82/90's narrower "
        "coverage -- but it predates the window by 2+ months even at v2, so it is "
        "OLD news, not NEW news, and does not answer this leg's gate YES."
    ),
    "ledger_action": (
        "NONE. solver/target_selection.py is not opened in this leg at all (neither "
        "read nor written); the territory is literature-only and taken literally."
    ),
}

# ---------------------------------------------------------------------------
# Query log.  Links, not counts (writeup/novelty/README.md's rule, after leg 53).
# ---------------------------------------------------------------------------
QUERIES = [
    {
        "id": "W1",
        "kind": "web_search",
        "query": "computer-assisted proof gCLM a>0 blow-up certificate 2026",
        "relevant_links": [
            "https://arxiv.org/pdf/2103.12390",
            "https://arxiv.org/html/2607.19762",
        ],
        "verdict": (
            "the on-topic return (2607.19762) is already-known false friend F1 from "
            "leg 77 (spectral inclusion for the non-degenerate family, not the a>0 "
            "degenerate branch); the rest is SEO noise for 'certificate management "
            "software' or unrelated PDE blow-up work; nothing new"
        ),
    },
    {
        "id": "W2",
        "kind": "web_search",
        "query": "certified inviscid self-similar blow-up profile 2026 arXiv new proof",
        "relevant_links": [
            "https://arxiv.org/html/2607.19762v1",
            "https://arxiv.org/abs/2605.19716",
            "https://arxiv.org/html/2603.11301",
            "https://link.springer.com/article/10.1007/s00205-026-02195-3",
        ],
        "verdict": (
            "arxiv:2605.19716 is FF1 (see below, predates window); 2603.11301 is a "
            "gSQG 1D-reduction self-similar profile, March 2026, different equation "
            "family, also predates the window; the Springer link is FF1's own "
            "21-months-older sibling (arXiv:2410.21765) now appearing in ARMA -- a "
            "journal typesetting of old content, not new mathematics, also predates "
            "the window. Nothing new."
        ),
    },
    {
        "id": "W3",
        "kind": "web_search",
        "query": "Navier-Stokes Euler blow-up singularity proof announcement August 2026",
        "relevant_links": [
            "https://www.quantamagazine.org/computer-helps-prove-long-sought-fluid-equation-singularity-20221116/",
            "https://arxiv.org/pdf/2604.09949",
        ],
        "verdict": (
            "no announcement newer than the already-known Chen-Hou 2022 result and "
            "the already-known, already-CLAIMED_UNUSABLE arXiv:2604.09949; nothing new"
        ),
    },
    {
        "id": "W4",
        "kind": "web_search",
        "query": "Terry Tao blog self-similar singularity gCLM Hou-Luo 2026",
        "relevant_links": [
            "https://arxiv.org/pdf/2106.05422",
            "https://arxiv.org/pdf/2308.01528",
        ],
        "verdict": (
            "no Tao blog post surfaced; returns are pre-existing Hou-Luo literature "
            "already in the ledger. Nothing new."
        ),
    },
]

# ---------------------------------------------------------------------------
# Structured endpoints -- these re-run verbatim, which is the point.
# ---------------------------------------------------------------------------
ENDPOINTS = [
    {
        "id": "A1a",
        "channel": "source paper version history: rank 1/3's anchor, arXiv:2604.01868",
        "url": "https://export.arxiv.org/api/query?id_list=2604.01868&max_results=1",
        "finding": {"version": "v1", "updated": "2026-04-02T10:25:28Z", "changed_in_window": False},
        "verdict": "unchanged since leg 90's same-day check",
    },
    {
        "id": "A1b",
        "channel": "source paper version history: rank 2's anchor, arXiv:2603.25104",
        "url": "https://export.arxiv.org/api/query?id_list=2603.25104&max_results=1",
        "finding": {"version": "v2", "updated": "2026-06-16T04:42:10Z", "changed_in_window": False},
        "verdict": "unchanged since leg 77's same-day check",
    },
    {
        "id": "A2a",
        "channel": "author enumeration, newest-first: De Huang",
        "url": (
            "https://export.arxiv.org/api/query?search_query=au:%22De_Huang%22"
            "&sortBy=submittedDate&sortOrder=descending&max_results=3"
        ),
        "finding": {"newest": "arXiv:2604.01868v1 (the source itself)", "newer_entry_in_window": False},
        "verdict": "nothing newer",
    },
    {
        "id": "A2b",
        "channel": "author enumeration, newest-first: Bojin Chen",
        "url": (
            "https://export.arxiv.org/api/query?search_query=au:%22Bojin_Chen%22"
            "&sortBy=submittedDate&sortOrder=descending&max_results=3"
        ),
        "finding": {
            "newest": "arXiv:2604.01868v1 (the source itself)",
            "next": "arXiv:2509.20108 (unrelated topic, numerical homogenization)",
            "newer_entry_in_window": False,
        },
        "verdict": "nothing newer",
    },
    {
        "id": "A2c",
        "channel": "author enumeration, newest-first: Xiangyuan Li",
        "url": (
            "https://export.arxiv.org/api/query?search_query=au:%22Xiangyuan_Li%22"
            "&sortBy=submittedDate&sortOrder=descending&max_results=5"
        ),
        "finding": {"newest": "arXiv:2604.01868v1 (the source itself)", "newer_entry_in_window": False},
        "verdict": "nothing newer",
    },
    {
        "id": "A3",
        "channel": "author enumeration, newest-first: Jiajun Tong (rank 2's co-author)",
        "url": (
            "https://export.arxiv.org/api/query?search_query=au:%22Jiajun_Tong%22"
            "&sortBy=submittedDate&sortOrder=descending&max_results=5"
        ),
        "finding": {"newest": "arXiv:2603.25104v2 (the source itself)", "newer_entry_in_window": False},
        "verdict": "nothing newer",
    },
    {
        "id": "A4",
        "channel": "corpus enumeration: all:\"Hou-Luo\"",
        "url": (
            "https://export.arxiv.org/api/query?search_query=all:%22Hou-Luo%22"
            "&sortBy=submittedDate&sortOrder=descending&max_results=10"
        ),
        "finding": {
            "n_entries": 7,
            "newest": "arXiv:2605.16322v1 (2026-05-05)",
            "note": (
                "already known (leg 74's cleared false positive: closed boundary-jet "
                "model, no self-similar profile certified, does not cite the source)"
            ),
            "newer_entry_in_window": False,
        },
        "verdict": "nothing after 2605.16322",
    },
    {
        "id": "A5",
        "channel": "corpus enumeration: abs:\"Constantin-Lax-Majda\"",
        "url": (
            "https://export.arxiv.org/api/query?search_query=abs:%22Constantin-Lax-Majda%22"
            "&sortBy=submittedDate&sortOrder=descending&max_results=10"
        ),
        "finding": {
            "newest": "arXiv:2607.19762v1 (2026-07-22)",
            "note": (
                "already known (leg 77's false friend F1: proves a spectral "
                "inclusion for the LSS non-degenerate family assumed to exist, not "
                "the a>0 degenerate branch)"
            ),
            "newer_entry_in_window": False,
        },
        "verdict": "nothing after 2607.19762",
    },
    {
        "id": "A6",
        "channel": "corpus enumeration: abs:\"gCLM\" (literal string)",
        "url": (
            "https://export.arxiv.org/api/query?search_query=abs:%22gCLM%22"
            "&sortBy=submittedDate&sortOrder=descending&max_results=10"
        ),
        "finding": {
            "newest_relevant": "arXiv:1908.09385 (Chen 2019, the gamma=2 dissipative case)",
            "note": "nothing from 2026 at all under this literal string",
            "newer_entry_in_window": False,
        },
        "verdict": "no gCLM a>0 CAP paper exists under this phrasing",
    },
    {
        "id": "A7",
        "channel": "corpus enumeration: abs:\"self-similar\" AND abs:\"computer-assisted\" (widest net for both gate branches)",
        "url": (
            "https://export.arxiv.org/api/query?search_query=abs:%22self-similar%22+AND+"
            "abs:%22computer-assisted%22&sortBy=submittedDate&sortOrder=descending&max_results=15"
        ),
        "finding": {
            "n_entries": 15,
            "newest": "arXiv:2607.27072v1 (2026-07-29, harmonic map heat flow shrinker -- different equation, not inviscid fluid)",
            "newer_entry_in_window": False,
        },
        "verdict": "nothing after 2607.27072, nothing in the window",
    },
    {
        "id": "A8",
        "channel": "corpus enumeration: cat:math.AP AND abs:\"self-similar\" AND abs:\"blow\"",
        "url": (
            "https://export.arxiv.org/api/query?search_query=cat:math.AP+AND+abs:%22self-similar%22"
            "+AND+abs:%22blow%22&sortBy=submittedDate&sortOrder=descending&max_results=10"
        ),
        "finding": {
            "newest": "arXiv:2608.01580v1 (2026-08-03, Riemann problem for a gas system -- off-topic generic-word hit)",
            "next_on_topic": "FF1, arXiv:2605.19716 (see below)",
            "newer_entry_in_window": False,
        },
        "verdict": "nothing in the window",
    },
    {
        "id": "A9",
        "channel": "corpus enumeration: abs:\"Boussinesq\" AND abs:\"self-similar\"",
        "url": (
            "https://export.arxiv.org/api/query?search_query=abs:%22Boussinesq%22+AND+"
            "abs:%22self-similar%22&sortBy=submittedDate&sortOrder=descending&max_results=10"
        ),
        "finding": {
            "newest": "arXiv:2607.15256v1 (2026-07-16, already known: Chen-Hou methods review, certifies no new profile)",
            "newer_entry_in_window": False,
        },
        "verdict": "nothing after 2607.15256, nothing in the window",
    },
    {
        "id": "A10",
        "channel": "corpus enumeration: abs:\"axisymmetric\" AND abs:\"blow-up\"",
        "url": (
            "https://export.arxiv.org/api/query?search_query=abs:%22axisymmetric%22+AND+"
            "abs:%22blow-up%22&sortBy=submittedDate&sortOrder=descending&max_results=10"
        ),
        "finding": {
            "n_entries": 10,
            "newest": "arXiv:2607.22046v1 (2026-07-24, GR geometry -- off-topic 'axis'/'singularities' hit)",
            "ff1_position": 5,
            "newer_entry_in_window": False,
        },
        "verdict": "nothing after 2607.22046, nothing in the window",
    },
    {
        "id": "A11",
        "channel": "corpus enumeration: abs:\"degenerate\" AND abs:\"one-scale\" (rank 2's exact phrase)",
        "url": (
            "https://export.arxiv.org/api/query?search_query=abs:%22degenerate%22+AND+"
            "abs:%22one-scale%22&max_results=10"
        ),
        "finding": {
            "n_entries": 1,
            "content": "unrelated multi-bubble heat-equation rigidity (arXiv:2601.12517)",
            "newer_entry_in_window": False,
        },
        "verdict": "zero gCLM hits under this phrasing",
    },
    {
        "id": "A12",
        "channel": "corpus enumeration: abs:\"Constantin-Lax-Majda\" AND abs:\"interval\" (a>0 CAP-specific)",
        "url": (
            "https://export.arxiv.org/api/query?search_query=abs:%22Constantin-Lax-Majda%22"
            "+AND+abs:%22interval%22&max_results=5"
        ),
        "finding": {"n_entries": 0},
        "verdict": "no interval-arithmetic CLM/gCLM paper exists in the corpus under this phrasing",
    },
    {
        "id": "A13",
        "channel": "the raw math.AP firehose, newest 40 -- decisive channel",
        "url": (
            "https://export.arxiv.org/api/query?search_query=cat:math.AP"
            "&sortBy=submittedDate&sortOrder=descending&max_results=40"
        ),
        "finding": {
            "newest_entry": "arXiv:2608.05128v1",
            "newest_entry_submitted": "2026-08-05T17:51:33Z",
            "predates_window_open": True,
            "window_open": WINDOW_OPENED,
            "near_miss_opened_and_cleared": {
                "arxiv": "2608.04138",
                "title": "Full-Tail Dynamical Rigidity Forced by Atomic Navier-Stokes Energy Concentration",
                "author": "Hao Huang",
                "submitted": "2026-08-04T18:46:28Z",
                "verdict": (
                    "read in full: VISCOUS 3D NS energy-concentration/rigidity "
                    "statement, no self-similar profile constructed or certified, "
                    "and pre-dates the window regardless"
                ),
            },
            "note": (
                "arXiv's daily announcement batch for 2026-08-06 had not yet posted "
                "as of the pass time (an operational fact about arXiv's once-daily "
                "cadence, not a search-scope limitation) -- so ZERO math.AP papers "
                "of ANY kind have been announced in the window on this channel's "
                "evidence"
            ),
        },
        "evidence_kind": "ENUMERATION OF THE ENTIRE RELEVANT FIREHOSE, not keyword luck",
        "verdict": "no math.AP paper of any kind in the window",
    },
    {
        "id": "B1a",
        "channel": "citation graph: Semantic Scholar, arXiv:2604.01868",
        "url": "https://api.semanticscholar.org/graph/v1/paper/arXiv:2604.01868/citations?fields=title&limit=10",
        "finding": {"citations_payload": '{"offset": 0, "data": []}', "citation_count": 0},
        "evidence_kind": "MEASURED ZERO",
        "verdict": "no citing works",
    },
    {
        "id": "B1b",
        "channel": "citation graph: Semantic Scholar, arXiv:2603.25104",
        "url": "https://api.semanticscholar.org/graph/v1/paper/arXiv:2603.25104/citations?fields=title&limit=10",
        "finding": {"citations_payload": '{"offset": 0, "data": []}', "citation_count": 0},
        "evidence_kind": "MEASURED ZERO",
        "verdict": "no citing works",
    },
    {
        "id": "B1c",
        "channel": "citation graph: Semantic Scholar, arXiv:2604.09949 (rank 6, cross-check with leg 93)",
        "url": "https://api.semanticscholar.org/graph/v1/paper/arXiv:2604.09949/citations?fields=title&limit=10",
        "finding": {"citations_payload": '{"offset": 0, "data": []}', "citation_count": 0},
        "evidence_kind": "MEASURED ZERO, consistent with leg 93's same-day finding",
        "verdict": "no citing works",
    },
    {
        "id": "B2",
        "channel": "citation graph: OpenAlex full-text search -- UNAVAILABLE today",
        "url": "https://api.openalex.org/works?search=2604.01868&per_page=5",
        "url_secondary": "https://api.openalex.org/works?filter=fulltext.search:2603.25104&per_page=5",
        "finding": {
            "http_error": (
                '{"error":"Rate limit exceeded","message":"Insufficient budget...",'
                '"dailyRemainingUsd":0,"retryAfter":46984}'
            ),
            "cause": (
                "OpenAlex's shared daily API budget is spent for 2026-08-06, most "
                "likely by the day's other five EXT-family legs against the same "
                "proxy egress"
            ),
        },
        "evidence_kind": "UNAVAILABLE -- NOT reported as a zero",
        "verdict": (
            "channel could not be run; Semantic Scholar (B1) is the surviving "
            "independent citation channel today"
        ),
    },
]

FF1 = {
    "arxiv": "2605.19716",
    "title": (
        "Self-similar blow-up solutions of d-dimensional incompressible Euler "
        "equations with C^{1,(1-2/d)-} velocity"
    ),
    "authors": ["Feng Shao", "Dongyi Wei", "Ping Zhang", "Zhifei Zhang"],
    "v1_date": "2026-05-19",
    "v2_date": "2026-07-22",
    "abstract_quote": (
        "We investigate self-similar blow-up solutions to the d-dimensional "
        "axisymmetric incompressible Euler equations without swirl for d >= 3. For "
        "any alpha in (0, alpha_d) with alpha_d = 1 - 2/d, we construct a "
        "self-similar blow-up solution whose initial velocity field satisfies "
        "u_0 in C^{1,alpha}_loc(R^d) intersect C^infty(R^d \\ {0}). ... Furthermore, "
        "we establish a finite-codimensional stability result for the self-similar "
        "profiles obtained above."
    ),
    "method": "analytic fixed-point argument on the self-similar profile equations, NOT computer-assisted",
    "is_inside_gate_a_wording": True,
    "why_not_a_yes_for_this_leg": (
        "DISPOSITIVE: predates the window by 2+ months even at v2 (v2 2026-07-22 vs "
        "window open 2026-08-06T00:35:44Z). It was not published SINCE the last "
        "window closed -- it was already sitting in the corpus, unrevised, well "
        "before leg 90 or leg 93 ran today."
    ),
    "genuine_gap_reported": (
        "none of legs 74/77/82/90's narrow, model-specific queries ('Hou-Luo', "
        "'Constantin-Lax-Majda', the rank-2/3 phrasings) were built to catch a "
        "different equation family's own construction -- a real gap in PRIOR "
        "coverage of OLD news, honestly reported, but not this leg's YES-trigger"
    ),
    "older_sibling_also_checked": {
        "arxiv": "2410.21765",
        "title": "Stationary self-similar profiles for the two-dimensional inviscid Boussinesq equations",
        "v1_date": "2024-10-29",
        "recent_appearance": (
            "just appeared in Archive for Rational Mechanics and Analysis "
            "(doi:10.1007/s00205-026-02195-3, a 2026-dated ARMA article-in-press) "
            "-- a JOURNAL TYPESETTING of a 21-month-old preprint, not new "
            "mathematical content, and not inside the window either way"
        ),
    },
    "recorded_for_next_reask": (
        "if the window narrows to 'since 2026-05-19' on a future pass, FF1 is the "
        "first thing to re-open, this time with a full-text read against the exact "
        "profile equation, not the abstract"
    ),
}

LIMITATIONS = [
    (
        "A result finished and typeset in the last few hours but not yet submitted, "
        "or submitted and sitting in arXiv's moderation queue, is invisible to "
        "every channel here -- and channel A13 shows this blind spot is WIDER than "
        "usual for this pass, since the day's whole announcement batch had not "
        "posted as of the pass time."
    ),
    (
        "OpenAlex (B2), leg 90's second independent citation index, was UNAVAILABLE "
        "today (shared daily budget exhausted). This is logged honestly as "
        "unavailable, not folded into a zero; Semantic Scholar (B1) is the only "
        "working citation channel this pass."
    ),
    (
        "The ten-hour window is short enough that 'nothing new' is close to "
        "guaranteed on priors alone. The value of running the channels anyway is "
        "confirming arXiv's own daily cycle had not produced a new batch at all "
        "(A13), and widening the net past the four ranked objects (which is where "
        "FF1 came from)."
    ),
    (
        "FF1 and its older sibling are PRE-EXISTING gaps in the narrower EXT-family "
        "watches' coverage, not new evidence for this leg's own gate. They are "
        "recorded so a future re-ask does not have to rediscover them, but they do "
        "not change this leg's NO."
    ),
]

BANS_RESPECTED = [
    "no gCLM measurement leg -- nothing here computes anything",
    "no Route-D bound sharpening -- no bound is touched",
    "no DSS re-ask -- the DSS lane is not entered",
    (
        "solver/target_selection.py NOT opened at all in this leg (neither read nor "
        "written) -- territory says literature-only, taken literally, unlike legs "
        "74/77/82/90 which at least read it for ledger fields"
    ),
    (
        "the five shared ledgers untouched: PHASE2_P2_NOTES.md, LITERATURE_CHECK.md, "
        "DIRECTION.md, plan_of_record.py, CONTINUATION_PROMPT.md"
    ),
    "no solver/*.py module imported, read, or edited anywhere in this leg",
]


def build() -> dict:
    return {
        "leg": 123,
        "route": "EXT6",
        "kind": "literature watch -- no computation, no solver module touched",
        "pass_date": PASS_DATE,
        "window_opened": WINDOW_OPENED,
        "window_opened_by": "leg 93 (Route-EXT5) landing, commit 067b7ac",
        "window_closed_pass_time": WINDOW_CLOSED_PASS_TIME,
        "window_hours": WINDOW_HOURS,
        "gate": GATE,
        "gate_answer": GATE_ANSWER,
        "queries": QUERIES,
        "endpoints": ENDPOINTS,
        "false_friend_ff1": FF1,
        "limitations": LIMITATIONS,
        "bans_respected": BANS_RESPECTED,
    }


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(
        here, "..", "writeup", "data", "p2_route_ext6_v1_target_watch6.json"
    )
    payload = build()
    with open(os.path.normpath(out), "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)
        fh.write("\n")

    ans = payload["gate_answer"]
    a13 = next(e for e in ENDPOINTS if e["id"] == "A13")["finding"]

    print("Route-EXT6 v1 (leg 123) -- dated literature watch, no computation")
    print("  gate:", GATE)
    print("  ANSWER:", ans["answer"], "as of", ans["as_of"])
    print(
        "  window: %s -> %s (%d hours)"
        % (WINDOW_OPENED, WINDOW_CLOSED_PASS_TIME, WINDOW_HOURS)
    )
    print(
        "  channels: %d checked, %d returned a candidate inside the window, %d unavailable"
        % (
            ans["channels_checked"],
            ans["channels_returning_a_candidate_inside_the_window"],
            ans["channels_unavailable"],
        )
    )
    print(
        "  decisive channel A13: newest math.AP entry submitted %s, predates window "
        "open %s -> arXiv's daily batch for today had not posted yet"
        % (a13["newest_entry_submitted"], WINDOW_OPENED)
    )
    print("  FF1 (recorded, NOT a yes):", FF1["arxiv"], "--", FF1["why_not_a_yes_for_this_leg"])
    print("  ledger action:", ans["ledger_action"])
    print("  queries logged:", len(QUERIES), "| endpoints logged:", len(ENDPOINTS))
    print("  wrote", os.path.normpath(out))


if __name__ == "__main__":
    main()
