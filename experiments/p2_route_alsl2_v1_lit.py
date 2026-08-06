#!/usr/bin/env python3
"""Leg 246 (Route-ALSL2) -- literature runner applying this repository's own established
"did the authors' later work close the gap" pattern (legs 175->196->239, 2208.09445->240,
2410.05480->242) to the precedent that sits CLOSEST to this repository's own investigation
line and had never been asked: Ambrose, Lushnikov, Siegel & Silantyev, arXiv:2207.07548 --
gCLM WITH dissipation, filed EXCLUSION in solver/viscous_novelty.py's PRECEDENTS ledger with
the reason "analysis + numerics, no computer-assisted certificate".

    .venv/bin/python experiments/p2_route_alsl2_v1_lit.py

THE QUESTION (pre-committed gate, both branches, DIRECTION.md leg 246):

    Do Ambrose, Lushnikov, Siegel, or Silantyev (or close collaborators) have subsequent
    published work that upgrades arXiv:2207.07548's gCLM-with-dissipation analysis into an
    actual computer-assisted certificate of a profile (of any dissipation exponent sigma,
    not necessarily gamma=2 specifically)?

    YES -> bears directly on the whole gamma=2 dissipative gCLM line (legs 63/125/174/185/
           187/193). Record citation, hypotheses and covered sigma verbatim; ESCALATE; do
           NOT build on it under this leg's authority; push branch only; report as parked.
    NO  -> report the SEARCH precisely (closed candidate sets, primary-source depth reads,
           live-probe controls), same discipline as legs 240/242/245. Bank as confirming
           this precedent's own frontier is still "no certificate" -- useful context for
           anyone evaluating legs 125/187/193's novelty claims. Normal landing.

WHAT THIS IS. A literature leg has no PDE to integrate, so the runner is what keeps the prose
honest (the pattern legs 175/183/189/196/240/242 established): every count and every number
quoted in writeup/novelty/leg_246.md and experiments/journal/leg_246.md is transcribed here
ONCE, from the primary source, with its line locator in a named md5-pinned extraction; the
gate verdict is COMPUTED from that table rather than asserted. Emits
writeup/data/p2_route_alsl2_v1_lit.json.

WHY THE VERDICT IS COMPUTED (lesson 90 -- a control that cannot come out differently is not a
control). The gate's YES branch escalates and parks the leg, so it must be reachable on
evidence that warranted it and not reachable by prose alone. `classify()` takes the evidence
table and returns one of

    CERTIFICATE_FOUND | CERTIFICATE_APPARATUS_BUT_NO_PROFILE
    | SUBSEQUENT_WORK_BUT_NO_APPARATUS | NO_SUBSEQUENT_WORK_ON_OBJECT

and `self_test()` exercises all four on perturbed copies of the evidence.

THE LIVE-PROBE CONTROL, AND IT IS BIDIRECTIONAL (lesson 90 again). This leg's negative rests
on TEN certification-apparatus term counts coming out zero over two full-text extractions. A
census that returns zero because it is not measuring anything is exactly leg 53's failure. So:

  (a) the SAME census, the SAME code, on a THIRD extraction from a DIFFERENT group
      (arXiv:2410.05480, Dahne-Figueras -- the CGL interval-verification paper this repo
      already knows: it closed stage V, and leg 242 audited its author line) must return
      NON-ZERO on the apparatus terms.  It returns 5/5/8/1/5 on
      interval arithmetic / computer-assisted / computer assisted / validated numerics /
      rigorous enclosure.
  (b) and the control must FAIL where the candidates succeed, or "each net finds what the
      other misses" is not established: the control scores dissipation=0, pole=0,
      Constantin-Lax-Majda=0 where the candidates score 19/107/6 and 8/0/26.

Both directions are enforced by `assert_probe_is_live()`, which fails the run if either stops
being true.  Neither set of zeros can then be an artifact of extraction or of the term list.

THE OTHER CONTROL, ON THE SEARCH ITSELF (N10 below). Three initial-form author nets
(au:"Lushnikov_P", au:"Ambrose_D", au:"Siegel_M") return 14/164/156 healthy-looking entries and
NONE of the three contains EITHER the parent OR the follow-up -- verified by direct substring
test on the raw XML. That is leg 240's au:"Buckmaster_T" failure and leg 242's au:"Figueras_J"
failure recurring on THREE author lines at once. It is recorded as data, not discarded, because
a query that silently under-returns is indistinguishable from a clean negative.

PROVENANCE. Three PDFs were pulled from arxiv.org during this leg and extracted with
`pdftotext -layout`; `line` fields locate quotes in those extractions. Papers/ is gitignored.

    arXiv:2411.01891v2  pdf md5 ac9db77e31007f039ccb17fa6010bf33  txt md5 71d45ab68be248efdaa13c64c83fbaf8  2704 lines
    arXiv:2504.14346v1  pdf md5 5cd2555c53bae17c594456434544ff72  txt md5 0df319cb14e1231e5e2a7c295b326edd  1632 lines
    arXiv:2410.05480v2  pdf md5 ce9d5e408491b036c7886b1558f337be  txt md5 d8a3eaf5ad57def4670c259cd60006d2  5114 lines  (CONTROL, different group)

NO NETWORK ACCESS at run time; every network result is transcribed as data below. No solver
module is read, imported or edited -- solver/viscous_novelty.py's PRECEDENTS ledger was read
READ-ONLY and is NOT modified by this leg. No stage is claimed; plan_of_record.py is untouched.

BANS CHECKED BEFORE STARTING (plan_of_record.py output read in full). Two could bind and
neither is tripped:
  - "another gCLM measurement leg" -- NOT TRIPPED. Nothing is measured on gCLM here. No
    solver is run, no profile is computed, no norm is evaluated. This is a bibliographic
    question about an author line, the same shape as legs 174/196/240/242.
  - "re-opening stage V as posed" -- NOT TRIPPED. No certificate is built, no dissipation
    parameter is floated against any margin, nothing is re-derived.
Route-D sharpening: none. GA compute: none. l1-Fourier / collocation machinery: none built.
Leg 51 re-claim: not made. "grep capabilities.py before building": grepped -- nothing built.
"""

import json
import os
from datetime import date

PASS_DATE = "2026-08-06"

PARENT = "arXiv:2207.07548"       # Ambrose, Lushnikov, Siegel, Silantyev -- the precedent
POLE = "arXiv:2411.01891v2"       # Silantyev, Lushnikov, Siegel, Ambrose -- ALL FOUR authors
PARAB = "arXiv:2504.14346v1"      # Ambrose, Lopes Filho, Nussenzveig Lopes -- dissipative CLM
CONTROL = "arXiv:2410.05480v2"    # Dahne & Figueras -- DIFFERENT group, live-probe control

PDF_MD5 = {
    POLE: "ac9db77e31007f039ccb17fa6010bf33",
    PARAB: "5cd2555c53bae17c594456434544ff72",
    CONTROL: "ce9d5e408491b036c7886b1558f337be",
}
TXT_MD5 = {
    POLE: "71d45ab68be248efdaa13c64c83fbaf8",
    PARAB: "0df319cb14e1231e5e2a7c295b326edd",
    CONTROL: "d8a3eaf5ad57def4670c259cd60006d2",
}
EXTRACTION_LINES = {POLE: 2704, PARAB: 1632, CONTROL: 5114}

PARENT_SUBMITTED = date(2022, 7, 15)

# --------------------------------------------------------------------------------------
# 1. HOW THE CANDIDATE SET WAS CLOSED.  Author-LISTING enumerations, not keyword searches:
#    a follow-up with an unexpected title cannot be missed by a listing the way it can by a
#    keyword query.  Two or three mutually independent nets per author, plus an independent
#    CITATION-side net, plus an author-maintained page, plus keyword nets.  The gate's
#    no-branch demands the SEARCH be reported, not the absence.
# --------------------------------------------------------------------------------------

SEARCH_LOG = [
    {"id": "N1", "author": "Lushnikov", "kind": "arxiv-api-author-listing", "n_entries": 77,
     "n_subsequent": 2,
     "query": 'https://export.arxiv.org/api/query?search_query=au:"Lushnikov"'
              '&max_results=300&sortBy=submittedDate&sortOrder=descending',
     "note": "surname net. Exactly 2 entries are Pavel M. Lushnikov and after 2022-07-15: "
             "2411.01891 and 2211.05473. One homonym INSIDE the same listing -- Konstantin "
             "V. Lushnikov, 2511.00013, machine learning for cognitive age -- recorded "
             "because an unexamined listing would have inflated the count (leg 242's Sven "
             "Dahne collision, recurring)."},
    {"id": "N2", "author": "Lushnikov", "kind": "arxiv-api-author-listing-CROSSCHECK",
     "n_entries": 55, "n_subsequent": 2,
     "query": 'https://export.arxiv.org/api/query?search_query=au:"Pavel M Lushnikov"'
              '&max_results=300&sortBy=submittedDate&sortOrder=descending',
     "note": "full-name net, run as an independent cross-check of N1. Same 2 subsequent "
             "papers, 0 missing."},
    {"id": "N3", "author": "Lushnikov", "kind": "arxiv-api-allfield-CROSSCHECK",
     "n_entries": 99, "n_subsequent": 2,
     "query": 'https://export.arxiv.org/api/query?search_query=all:"Lushnikov"'
              '&max_results=300&sortBy=submittedDate&sortOrder=descending',
     "note": "all-field net -- catches the name anywhere in the record, not only the author "
             "list. Same 2 subsequent papers. THREE independent nets, same answer: the "
             "sparseness of this author's recent arXiv output is a property of the author, "
             "not of the query."},
    {"id": "N4", "author": "Lushnikov", "kind": "arxiv-api-coauthor-net",
     "n_entries": 88, "n_subsequent": 1,
     "query": 'https://export.arxiv.org/api/query?search_query=au:"Dyachenko"'
              '&max_results=300&sortBy=submittedDate&sortOrder=descending',
     "note": "coauthor net, a fourth line on the same fact. Exactly 1 entry carries "
             "Lushnikov after the cut-off and it is 2211.05473 again (Stokes waves)."},
    {"id": "N5", "author": "Silantyev", "kind": "arxiv-api-author-listing",
     "n_entries": 27, "n_subsequent": 3,
     "query": 'https://export.arxiv.org/api/query?search_query=au:"Silantyev"'
              '&max_results=300&sortBy=submittedDate&sortOrder=descending',
     "note": "surname net. 3 subsequent Denis A. Silantyev entries (2411.01891, 2211.02875 "
             "almost-extreme waves, 2207.11579 adjoint DSMC for Boltzmann). Homonym excluded: "
             "Alexey Silantyev, 2209.00694, Manin matrices."},
    {"id": "N6", "author": "Silantyev", "kind": "arxiv-api-author-listing-CROSSCHECK",
     "n_entries": 8, "n_subsequent": 2,
     "query": 'https://export.arxiv.org/api/query?search_query=au:"Denis A Silantyev"'
              '&max_results=300&sortBy=submittedDate&sortOrder=descending',
     "note": "full-name net. 0 MISSING against N5 -- it NARROWS rather than widens: N5's "
             "2207.11579 is indexed as 'Denis Silantyev' with no middle initial, so the "
             "full-name form does not return it. This is why neither net form is allowed to "
             "stand alone, and it is the same effect that N9 catches on Ambrose."},
    {"id": "N7", "author": "Siegel", "kind": "arxiv-api-author-listing",
     "n_entries": 91, "n_subsequent": 3,
     "query": 'https://export.arxiv.org/api/query?search_query=au:"Michael Siegel"'
              '&max_results=300&sortBy=submittedDate&sortOrder=descending',
     "note": "full-name net, heavily contaminated by Michael H. Siegel (Swift/UVOT astronomy) "
             "and by an unrelated Michael Siegel in cloud security (2403.01507). The NJIT "
             "Michael Siegel's 3 subsequent works: 2411.01891, 2506.11282 (boundary-integral "
             "two-phase flow with surfactant), 2410.04626 (flapping plates, JFM 1013 A14)."},
    {"id": "N8", "author": "Ambrose", "kind": "arxiv-api-author-listing",
     "n_entries": 38, "n_subsequent": 14,
     "query": 'https://export.arxiv.org/api/query?search_query=au:"David M Ambrose"'
              '&max_results=300&sortBy=submittedDate&sortOrder=descending',
     "note": "full-name net. Ambrose is by far the most active of the four: 14 subsequent "
             "works, spanning KS, mean field games, SQG, vortex sheets, Benjamin-Ono, "
             "hydroelastic waves, 3D Navier-Stokes analyticity."},
    {"id": "N9", "author": "Ambrose", "kind": "arxiv-api-category-CROSSCHECK-THAT-FOUND-ONE",
     "n_entries": 38, "n_subsequent": 15,
     "query": 'https://export.arxiv.org/api/query?search_query=cat:math.AP AND au:"Ambrose"'
              '&max_results=300&sortBy=submittedDate&sortOrder=descending',
     "note": "THE CROSS-CHECK EARNING ITS PLACE. Returns ONE MORE than N8: arXiv:2504.14346, "
             "filed as 'David Ambrose' WITHOUT the middle initial, so the full-name net N8 "
             "does not return it -- and it is the paper CLOSEST to this repository's own "
             "gamma=2 object (dissipative Constantin-Lax-Majda at general sigma>0). Had N8 "
             "been the only Ambrose net, this leg's candidate set would have been short by "
             "exactly the most relevant entry. Leg 242 recorded this lesson from the other "
             "direction (its broad net CONFIRMED the full-name net); here the broad net "
             "CORRECTED it."},
    {"id": "N10", "author": "all", "kind": "arxiv-api-FAILED-FORMS-RECORDED-NOT-DISCARDED",
     "n_entries": 334, "n_subsequent": 0,
     "query": 'au:"Lushnikov_P" (14) | au:"Ambrose_D" (164) | au:"Siegel_M" (156)',
     "note": "ALL THREE return a large, healthy-looking result set and NONE of the three "
             "contains EITHER arXiv:2207.07548 OR arXiv:2411.01891 -- verified by direct "
             "substring test on the raw XML (False/False in all three). au:\"Lushnikov_P\" "
             "newest entry is 2020-03-11; au:\"Ambrose_D\" contains 0 papers by David M. "
             "Ambrose (it is particle-physics D. Ambrose); au:\"Siegel_M\" is dominated by "
             "Daniel M. Siegel (astrophysics). This is leg 240's au:\"Buckmaster_T\" failure "
             "and leg 242's au:\"Figueras_J\" failure recurring on THREE author lines at "
             "once. A query that silently under-returns is indistinguishable from a clean "
             "negative -- had any one of these been the net for its author, this leg would "
             "have reported NO for entirely the wrong reason and looked identical doing it."},
    {"id": "N11", "author": "all", "kind": "citation-side-net-INDEPENDENT-OF-LISTINGS",
     "n_entries": 6, "n_subsequent": 2,
     "query": 'https://api.semanticscholar.org/graph/v1/paper/arXiv:2207.07548/citations'
              '?fields=title,year,authors,externalIds,venue&limit=200',
     "note": "6 citing papers; exactly 2 carry a parent author, and they are the same 2 the "
             "author-listing nets closed on (2411.01891, 2504.14346). The other 4 are the De "
             "Huang-Qin-Wang(-Wei) line (2305.05895, 2401.14615, SIAM J. Math. Anal. version) "
             "and Guo-Jiu 2506.02800 -- none is this author line, and all are already in this "
             "repository's corpus (legs 65, 77, 185). The citation net and the author-listing "
             "net close on the SAME candidate set from OPPOSITE directions."},
    {"id": "N12", "author": "Lushnikov", "kind": "author-maintained-page",
     "n_entries": 2, "n_subsequent": 1,
     "query": "https://math.unm.edu/~plushnik/",
     "note": "carries publication STATUS the arXiv listing does not -- the value leg 240 got "
             "from sites.brown.edu/jgs/papers/ and leg 242 from dahne.eu. Its ENTIRE 2024-2026 "
             "output is the two papers of this line: the follow-up is PUBLISHED (Stud. Appl. "
             "Math. 155, e70115 (2025), doi:10.1111/sapm.70115), and the parent is published "
             "as Nonlinearity 37, 025004 (2024), doi:10.1088/1361-6544/ad140c -- a fact the "
             "PRECEDENTS ledger row does not carry. NOTHING listed for 2026. Neither entry "
             "mentions computer-assisted proof, interval arithmetic or validated numerics."},
    {"id": "N13", "author": "all", "kind": "keyword-net",
     "n_entries": 8, "n_subsequent": 0,
     "query": "Ambrose Lushnikov Siegel Silantyev gCLM dissipation computer-assisted proof "
              "interval arithmetic certificate self-similar profile 2026",
     "note": "surfaces the parent's journal version (IOPscience Nonlinearity 37 025004), the "
             "parent PDF, HQWW 2305.05895 and Xu 2607.19762 (both already read by this repo, "
             "legs 112/189, both INVISCID), and both authors' aggregator profiles. Also "
             "returns 1710.00329 (Kuramoto-Sivashinsky symbolic-dynamics CAP, DIFFERENT "
             "group) -- logged only because it shows the query DOES surface CAPs when they "
             "exist. No follow-up the listings had not already closed."},
    {"id": "N14", "author": "all", "kind": "keyword-net",
     "n_entries": 9, "n_subsequent": 0,
     "query": '"Silantyev" OR "Lushnikov" generalized Constantin-Lax-Majda dissipation '
              "rigorous validated numerics blowup profile preprint 2026",
     "note": "led to N12 (Lushnikov's homepage and CV). Otherwise returns the Huang-line "
             "journal versions and an exact Hou-Luo blow-up paper by a different group. No "
             "new candidate."},
    {"id": "N15", "author": "Silantyev", "kind": "institutional-profile-NUMERICAL-CULTURE",
     "n_entries": 1, "n_subsequent": 0,
     "query": "Denis Silantyev UCCS mathematics publications page 2026 "
              "-> https://math.uccs.edu/denis-silantyev",
     "note": "newest item is the same September-2025 paper. Logged for the one line that "
             "EXPLAINS the negative rather than merely reporting it: his stated computational "
             "interests are 'scientific computing, high-performance computing (HPC), and "
             "multi-precision computations' and spectral methods. This group's numerical "
             "culture is HIGH-PRECISION FLOATING POINT, not VALIDATED NUMERICS -- exactly leg "
             "242's finding on 2607.03498 ('multiprecision following that validation-oriented "
             "philosophy'), now on a second author line."},
]

# --------------------------------------------------------------------------------------
# 2. THE CANDIDATE SET.  Every work by any of the four authors, after 2022-07-15, that is on
#    the OBJECT (gCLM / CLM, with dissipation).  Both were read at full text this leg.
#    The wider author-line output (19 distinct subsequent works) is enumerated below but not
#    tabulated
#    row by row here -- it is enumerated in writeup/novelty/leg_246.md with links.
# --------------------------------------------------------------------------------------

CANDIDATES = [
    {
        "id": POLE,
        "cite": ("Silantyev, Lushnikov, Siegel, Ambrose, 'Exact periodic solutions of the "
                 "generalized Constantin-Lax-Majda equation with dissipation', "
                 "Studies in Applied Mathematics 155, no. 3 (2025): e70115"),
        "submitted": "2024-11-04", "version": "v2", "v2_updated": "2025-11-03",
        "journal_ref": "Studies in Applied Mathematics 155, no. 3 (2025): e70115",
        "doi": "10.1111/sapm.70115",
        "all_four_parent_authors": True,
        "on_the_object": True,
        "read_full_text": True,
        "has_certificate_apparatus": False,
        "certifies_a_profile": False,
        "method": "exact pole dynamics (closed form) + phase-plane analysis",
        "sigma_covered_by_exact_solutions": [0, 1],
        "a_covered_by_exact_solutions": [0.0, 0.5],
        "sigma_2_status": ("NOT covered by any exact solution. Their Table 1 puts every "
                           "sigma in (1,infty) -- which is where sigma=2 lives -- in the "
                           "GEIVP cell: global existence of the initial value problem for "
                           "small data. That is the OPPOSITE side of the question from a "
                           "blow-up profile. And they state at l.2360 that the periodic "
                           "sigma=2 generalization of Schochet's real-line solution DEFEATED "
                           "them."),
        "why_it_fails_the_gate": ("It is an EXACT-SOLUTION paper, not a certification paper. "
                                  "0 of 10 certification-apparatus terms over 2704 lines. Its "
                                  "single 'computer-aided' hit is at l.54 and refers to Chen "
                                  "and Hou's proof, not to anything the authors do."),
    },
    {
        "id": PARAB,
        "cite": ("Ambrose, Lopes Filho, Nussenzveig Lopes, 'Existence and analyticity of "
                 "solutions of nonlinear parabolic model equations with singular data', "
                 "arXiv:2504.14346 (2025-04-19)"),
        "submitted": "2025-04-19", "version": "v1", "v2_updated": None,
        "journal_ref": None,
        "doi": None,
        "all_four_parent_authors": False,
        "on_the_object": True,
        "read_full_text": True,
        "has_certificate_apparatus": False,
        "certifies_a_profile": False,
        "method": "analysis: Banach fixed point in a Wiener-algebra / pseudomeasure scale",
        "sigma_covered_by_exact_solutions": [],
        "a_covered_by_exact_solutions": [],
        "sigma_2_status": ("COVERED, but on the global-existence side: sec 5 is the "
                           "dissipative CLM equation omega_t = omega H(omega) - nu Lambda^"
                           "sigma omega at general sigma > 0 (so sigma=2 is included), sec 6 "
                           "adds the advection term. The result is global existence for small "
                           "rough data (l.693-694) and analyticity for sigma >= 1. No blow-up "
                           "and no profile."),
        "why_it_fails_the_gate": ("0 of 10 certification-apparatus terms over 1632 lines; and "
                                  "there is no profile in the paper to certify -- "
                                  "'self-similar' = 0, 'blowup' = 0, 'blow-up' = 1 in the "
                                  "whole text. Its 2 'contraction mapping' hits are an exact-"
                                  "arithmetic Banach fixed point, enclosing nothing."),
    },
]

# Wider author-line output STRICTLY AFTER the cut-off, by author, from N1-N9 (links in the
# novelty log).  Listed as explicit arXiv ids, not as counts, so the union is COMPUTED and the
# double-counting of the joint paper cannot be got wrong by hand.  (It was, on the first pass:
# the per-author counts had silently included the PARENT itself, which is dated exactly on the
# cut-off, and the union was hand-written as 17.  Enumerating fixes both.)
SUBSEQUENT_BY_AUTHOR = {
    "Lushnikov": ["2411.01891", "2211.05473"],
    "Silantyev": ["2411.01891", "2211.02875", "2207.11579"],
    "Siegel": ["2411.01891", "2506.11282", "2410.04626"],
    "Ambrose": ["2607.19887", "2512.11210", "2508.10254", "2507.20918", "2504.17199",
                "2504.14346", "2412.12457", "2411.01891", "2406.13288", "2403.12829",
                "2402.01038", "2401.06055", "2308.08078", "2209.14481"],
}
SUBSEQUENT_COUNTS_BY_AUTHOR = {k: len(v) for k, v in SUBSEQUENT_BY_AUTHOR.items()}
# 2411.01891 is joint across all four, so the union is strictly smaller than the sum (23).
SUBSEQUENT_UNION = sorted({w for ws in SUBSEQUENT_BY_AUTHOR.values() for w in ws})
N_SUBSEQUENT_UNION = len(SUBSEQUENT_UNION)

# --------------------------------------------------------------------------------------
# 3. TERM CENSUS over the md5-pinned extractions.  Ten CERTIFICATION-APPARATUS terms (which
#    the gate turns on) and six SUBJECT terms (which make the control bidirectional).
# --------------------------------------------------------------------------------------

APPARATUS_TERMS = ["interval arithmetic", "computer-assisted", "computer assisted",
                   "computer-aided", "validated numerics", "Newton-Kantorovich",
                   "radii polynomial", "INTLAB", "rigorous enclosure", "verified enclosure"]
SUBJECT_TERMS = ["self-similar", "blowup", "blow-up", "dissipation", "pole",
                 "Constantin-Lax-Majda"]

CENSUS = {
    POLE: {
        "apparatus": {"interval arithmetic": 0, "computer-assisted": 0, "computer assisted": 0,
                      "computer-aided": 1, "validated numerics": 0, "Newton-Kantorovich": 0,
                      "radii polynomial": 0, "INTLAB": 0, "rigorous enclosure": 0,
                      "verified enclosure": 0},
        "subject": {"self-similar": 28, "blowup": 89, "blow-up": 14, "dissipation": 19,
                    "pole": 107, "Constantin-Lax-Majda": 6},
    },
    PARAB: {
        "apparatus": {"interval arithmetic": 0, "computer-assisted": 0, "computer assisted": 0,
                      "computer-aided": 0, "validated numerics": 0, "Newton-Kantorovich": 0,
                      "radii polynomial": 0, "INTLAB": 0, "rigorous enclosure": 0,
                      "verified enclosure": 0},
        "subject": {"self-similar": 0, "blowup": 0, "blow-up": 1, "dissipation": 8,
                    "pole": 0, "Constantin-Lax-Majda": 26},
    },
    CONTROL: {
        "apparatus": {"interval arithmetic": 5, "computer-assisted": 5, "computer assisted": 8,
                      "computer-aided": 0, "validated numerics": 1, "Newton-Kantorovich": 0,
                      "radii polynomial": 0, "INTLAB": 0, "rigorous enclosure": 5,
                      "verified enclosure": 0},
        "subject": {"self-similar": 50, "blowup": 12, "blow-up": 12, "dissipation": 0,
                    "pole": 0, "Constantin-Lax-Majda": 0},
    },
}

# The ONE apparatus hit anywhere in the candidate set, and what it actually refers to.
LONE_APPARATUS_HIT = {
    "paper": POLE, "term": "computer-aided", "count": 1, "line": 54,
    "quote": ("and Chen and Hou [2], who give a computer-aided proof of finite-time blowup "
              "for C^infty initial data."),
    "reading": ("It is a citation of SOMEBODY ELSE's certificate, in the introduction's "
                "survey of prior work. The authors do not claim, attempt or use computer "
                "assistance anywhere in the paper. Recorded explicitly rather than rounded "
                "to zero -- rounding it away would have made the census look cleaner than "
                "the evidence is."),
}

# --------------------------------------------------------------------------------------
# 4. VERBATIM QUOTES, with line locators into the md5-pinned extractions.
# --------------------------------------------------------------------------------------

KEY_QUOTES = [
    {"paper": POLE, "line": 25, "tag": "method-is-exact-solutions",
     "quote": ("We present exact pole dynamics solutions to the generalized "
               "Constantin-Lax-Majda (gCLM) equation in a periodic geometry with dissipation "
               "-Lambda^sigma, where its spatial Fourier transform is |k|^sigma."),
     "why": "The abstract's first sentence disqualifies the paper under the gate: exact "
            "solutions, not a certificate."},
    {"paper": POLE, "line": 34, "tag": "sigma-and-a-coverage",
     "quote": ("We derive new periodic solutions for a = 0 and 1/2 and sigma = 0 and 1, for "
               "which a closed collection of (periodically repeated) poles evolve in the "
               "complex plane."),
     "why": "The gate's qualifier is 'of ANY dissipation exponent sigma'. The answer is that "
            "the exact solutions exist at sigma in {0,1} and a in {0,1/2} only -- and even "
            "there they are exact solutions, not certificates."},
    {"paper": POLE, "line": 2309, "tag": "where-closed-form-runs-out",
     "quote": ("When sigma = 1 closed form analytical solutions are not available, and we "
               "resort to a phase-plane analysis using special variables to obtain useful "
               "information about singularity formation."),
     "why": "What they reach for when the closed form fails is phase-plane analysis, not "
            "validated numerics. This is the sharpest single line on the group's method."},
    {"paper": POLE, "line": 2358, "tag": "gamma-2-defeated-them",
     "quote": ("When a = 0 and sigma = 2, a pole dynamics solution for the problem on the "
               "real line was found by Schochet [6]. Remarkably, this solution exhibits finite "
               "time blowup in both the L2 and Wiener norms for all initial data. Despite "
               "significant effort, we have been unable to generalize this solution to the "
               "periodic domain."),
     "why": "The most directly relevant sentence in the whole search to this repository's "
            "gamma=2 dissipative line: the authors' own most recent published word on "
            "sigma=2 is that the periodic case defeated them."},
    {"paper": POLE, "line": 2364, "tag": "their-own-stated-next-step",
     "quote": ("In future work, we intend to numerically investigate finite-time singularity "
               "formation in the gCLM equation with dissipation over the full range of a and "
               "for more general values of sigma, both for problems on the real line and "
               "periodic domain."),
     "why": "The gate asks whether they upgraded the analysis into a certificate. Their own "
            "stated next step, in the published follow-up, is NUMERICAL INVESTIGATION. Not "
            "'we have not yet' -- 'we intend to numerically investigate'."},
    {"paper": POLE, "line": 2352, "tag": "table-1-legend",
     "quote": ("Table 1: Summary of our results on global existence versus finite-time "
               "singularity formation in L2 and B0. FTS = finite-time singularity formation "
               "for arbitrarily small data; GEPD = global existence of pole dynamics "
               "solutions for small data; GEIVP = global existence of solutions to initial "
               "value problem for small data; NT = neither pole dynamics solutions nor our "
               "general theory applies."),
     "why": "The legend is what makes the sigma=2 reading checkable: sigma in (1,infty) reads "
            "GEIVP in every column, and every a outside {0,1/2} reads NT."},
    {"paper": POLE, "line": 54, "tag": "the-lone-apparatus-hit",
     "quote": ("and Chen and Hou [2], who give a computer-aided proof of finite-time blowup "
               "for C^infty initial data."),
     "why": "The only certification-apparatus term anywhere in either candidate, and it is "
            "about a different group's result."},
    {"paper": PARAB, "line": 26, "tag": "object-is-dissipative-CLM",
     "quote": ("To illustrate the second approach, we prove existence and analyticity of "
               "solutions of the dissipative Constantin-Lax-Majda equation (which models "
               "vortex stretching), with and without added advection, with two classes of "
               "rough data."),
     "why": "Establishes that this paper IS on the object -- the same dissipative gCLM family "
            "-- so its zero apparatus census is on-target and not a category miss."},
    {"paper": PARAB, "line": 673, "tag": "the-equation-at-general-sigma",
     "quote": "omega_t = omega H(omega) - nu Lambda^sigma omega",
     "why": "Section 5's equation, at general sigma > 0 -- so sigma = 2 IS inside this paper's "
            "scope, which is exactly why it needed a full-text read rather than an abstract "
            "glance."},
    {"paper": PARAB, "line": 693, "tag": "direction-is-global-existence",
     "quote": ("We will show now that for any sigma > 0, sufficiently small periodic data in "
               "Y^{-sigma/2} leads to existence of a global solution."),
     "why": "The direction is global existence for small data -- the opposite side of the "
            "question from a certified blow-up profile."},
]

# --------------------------------------------------------------------------------------
# 5. IN-REPO PRIOR ART.  arXiv:2411.01891 was NOT new to this repository; the gate's
#    QUESTION was.  Six legs held it and every one used it for something else.
# --------------------------------------------------------------------------------------

PRIOR_ART = [
    {"where": "experiments/journal/leg_64.md l.58-70", "depth": "abstract/table",
     "held": "names 2411.01891 as the PERIODIC half of the exhaustive dissipative-gCLM "
             "exact-solution corpus, to establish that sigma=3 is in neither list",
     "asked_the_gate": False},
    {"where": "experiments/p2_route_as2_v1_lit.py l.480, l.541", "depth": "targeted",
     "held": "2411.01891 listed under excluded_sources; checked only for whether it carries "
             "the first integral (FI)",
     "asked_the_gate": False},
    {"where": "writeup/novelty/leg_125.md l.86", "depth": "abstract",
     "held": "keyword-query hit, glossed 'Lushnikov et al., exact periodic gCLM solutions'",
     "asked_the_gate": False},
    {"where": "writeup/novelty/leg_185.md l.49", "depth": "abstract",
     "held": "same gloss, same query family",
     "asked_the_gate": False},
    {"where": "writeup/novelty/leg_77.md l.43", "depth": "listing only",
     "held": "inside a corpus enumeration of the pre-2026 gCLM literature",
     "asked_the_gate": False},
    {"where": "writeup/novelty/leg_65.md l.119", "depth": "listing only",
     "held": "inside a corpus enumeration",
     "asked_the_gate": False},
    {"where": "experiments/p2_route_lga_v1_ledger.py l.155-195", "depth": "full text",
     "held": "five section-locators into the PARENT 2207.07548 (sec 1, 5.1, 5.2 eqs (49)-(50), "
             "5.3 eq (61), 8) -- the parent was read properly; the follow-up never was",
     "asked_the_gate": False},
    {"where": "experiments/p2_route_lss_v1_lit.py, experiments/journal/leg_161.md",
     "depth": "full text",
     "held": "Lushnikov-Silantyev-Siegel arXiv:2010.01201 -- a PRIOR work of the same line, "
             "not a subsequent one",
     "asked_the_gate": False},
]

# --------------------------------------------------------------------------------------
# 6. THE CLASSIFIER.  The verdict is computed from the evidence table, not asserted.
# --------------------------------------------------------------------------------------

CERTIFICATE_FOUND = "CERTIFICATE_FOUND"
APPARATUS_NO_PROFILE = "CERTIFICATE_APPARATUS_BUT_NO_PROFILE"
SUBSEQUENT_NO_APPARATUS = "SUBSEQUENT_WORK_BUT_NO_APPARATUS"
NO_SUBSEQUENT_ON_OBJECT = "NO_SUBSEQUENT_WORK_ON_OBJECT"


def classify(candidates):
    """Return the gate verdict code implied by the candidate table.

    Ordered so that the ESCALATING outcome (CERTIFICATE_FOUND) is reachable on evidence and
    only on evidence: it requires some candidate that is on the object AND carries
    certification apparatus AND certifies a profile.
    """
    on_object = [c for c in candidates if c["on_the_object"]]
    if not on_object:
        return NO_SUBSEQUENT_ON_OBJECT
    if any(c["has_certificate_apparatus"] and c["certifies_a_profile"] for c in on_object):
        return CERTIFICATE_FOUND
    if any(c["has_certificate_apparatus"] for c in on_object):
        return APPARATUS_NO_PROFILE
    return SUBSEQUENT_NO_APPARATUS


VERDICT_TO_GATE_ANSWER = {
    CERTIFICATE_FOUND: "YES",
    APPARATUS_NO_PROFILE: "NO",
    SUBSEQUENT_NO_APPARATUS: "NO",
    NO_SUBSEQUENT_ON_OBJECT: "NO",
}


def self_test():
    """Exercise all four classifier outcomes on perturbed copies of the evidence."""
    import copy
    base = copy.deepcopy(CANDIDATES)

    yes = copy.deepcopy(base)
    yes[0]["has_certificate_apparatus"] = True
    yes[0]["certifies_a_profile"] = True

    apparatus_only = copy.deepcopy(base)
    apparatus_only[0]["has_certificate_apparatus"] = True

    off_object = copy.deepcopy(base)
    for c in off_object:
        c["on_the_object"] = False

    return {
        "actual_evidence_gives_SUBSEQUENT_WORK_BUT_NO_APPARATUS":
            classify(base) == SUBSEQUENT_NO_APPARATUS,
        "flipping_apparatus+profile_gives_CERTIFICATE_FOUND":
            classify(yes) == CERTIFICATE_FOUND,
        "flipping_apparatus_only_gives_APPARATUS_BUT_NO_PROFILE":
            classify(apparatus_only) == APPARATUS_NO_PROFILE,
        "emptying_the_object_column_gives_NO_SUBSEQUENT_WORK_ON_OBJECT":
            classify(off_object) == NO_SUBSEQUENT_ON_OBJECT,
        "empty_candidate_set_gives_NO_SUBSEQUENT_WORK_ON_OBJECT":
            classify([]) == NO_SUBSEQUENT_ON_OBJECT,
        "CERTIFICATE_FOUND_maps_to_gate_YES":
            VERDICT_TO_GATE_ANSWER[CERTIFICATE_FOUND] == "YES",
        "every_other_verdict_maps_to_gate_NO":
            all(v == "NO" for k, v in VERDICT_TO_GATE_ANSWER.items()
                if k != CERTIFICATE_FOUND),
    }


def assert_probe_is_live():
    """Lesson 90, in BOTH directions.

    (a) The apparatus census must be able to fire: the same ten terms, the same counting, on
        a third extraction from a DIFFERENT group must return non-zero.
    (b) The control must FAIL where the candidates fire, or the two nets are not independent
        and 'each finds what the other misses' is unearned.
    """
    cand = [POLE, PARAB]
    app_cand = sum(CENSUS[p]["apparatus"][t] for p in cand for t in APPARATUS_TERMS)
    app_ctrl = sum(CENSUS[CONTROL]["apparatus"][t] for t in APPARATUS_TERMS)

    # Subject terms that are specific to THIS object and absent from the control's object.
    obj_terms = ["dissipation", "pole", "Constantin-Lax-Majda"]
    subj_cand = sum(CENSUS[p]["subject"][t] for p in cand for t in obj_terms)
    subj_ctrl = sum(CENSUS[CONTROL]["subject"][t] for t in obj_terms)

    # The lone apparatus hit in the candidate set is a citation of another group's proof.
    app_cand_self_claimed = app_cand - LONE_APPARATUS_HIT["count"]

    direction_a = app_ctrl > 0
    direction_b = subj_ctrl == 0 and subj_cand > 0
    live = direction_a and direction_b

    if not live:
        raise AssertionError(
            "LIVE-PROBE CONTROL FAILED: apparatus_control=%d (needs >0), "
            "object_control=%d (needs 0), object_candidates=%d (needs >0). The census is "
            "no longer a probe that can come out differently -- see lesson 90."
            % (app_ctrl, subj_ctrl, subj_cand))

    return {
        "apparatus_terms_total_over_2_candidates": app_cand,
        "apparatus_terms_total_self_claimed_by_candidates": app_cand_self_claimed,
        "apparatus_terms_total_over_control": app_ctrl,
        "object_terms_total_over_2_candidates": subj_cand,
        "object_terms_total_over_control": subj_ctrl,
        "direction_a_control_fires_on_apparatus": direction_a,
        "direction_b_control_is_silent_on_the_object": direction_b,
        "probe_is_live": live,
        "reading": ("The apparatus census fires 24 times on a different group's paper and 1 "
                    "time across both candidates -- and that 1 is a citation of Chen-Hou, so "
                    "the SELF-CLAIMED total is 0. Conversely the object census fires 166 "
                    "times across the candidates and 0 times on the control. Each net finds "
                    "what the other misses, so neither set of zeros can be an artifact of "
                    "the extraction or of the term list."),
    }


def build():
    verdict = classify(CANDIDATES)
    gate_answer = VERDICT_TO_GATE_ANSWER[verdict]
    live = assert_probe_is_live()
    st = self_test()
    today = date(*[int(x) for x in PASS_DATE.split("-")])
    days = (today - PARENT_SUBMITTED).days

    n_on_object = sum(1 for c in CANDIDATES if c["on_the_object"])
    n_read = sum(1 for c in CANDIDATES if c["read_full_text"])
    n_apparatus = sum(1 for c in CANDIDATES if c["has_certificate_apparatus"])
    n_profile = sum(1 for c in CANDIDATES if c["certifies_a_profile"])

    return {
        "leg": 246,
        "route": "ALSL2",
        "role": "LIT",
        "date": PASS_DATE,
        "claims_stage": None,
        "parent_paper": PARENT,
        "parent_cite": ("Ambrose, Lushnikov, Siegel, Silantyev, 'Global existence and "
                        "singularity formation for the generalized Constantin-Lax-Majda "
                        "equation with dissipation: The real line vs. periodic domains', "
                        "Nonlinearity 37, 025004 (2024), doi:10.1088/1361-6544/ad140c"),
        "parent_precedents_ledger_verdict": "EXCLUSION",
        "parent_precedents_ledger_reason": "analysis + numerics, no computer-assisted certificate",

        "gate_question": (
            "Do Ambrose, Lushnikov, Siegel, or Silantyev (or close collaborators) have "
            "subsequent published work that upgrades arXiv:2207.07548's gCLM-with-dissipation "
            "analysis into an actual computer-assisted certificate of a profile (of any "
            "dissipation exponent sigma, not necessarily gamma=2 specifically)?"),
        "gate_answer": gate_answer,
        "gate_verdict_code": verdict,
        "escalates": verdict == CERTIFICATE_FOUND,
        "gate_answer_realization": (
            "NO, in the realization: arXiv author-listing enumeration over all four authors, "
            "each closed by two or three MUTUALLY INDEPENDENT nets (au:\"Lushnikov\" 77 / "
            "au:\"Pavel M Lushnikov\" 55 / all:\"Lushnikov\" 99 / coauthor au:\"Dyachenko\" "
            "88; au:\"Silantyev\" 27 / au:\"Denis A Silantyev\" 8; au:\"Michael Siegel\" 91; "
            "au:\"David M Ambrose\" 38 / cat:math.AP AND au:\"Ambrose\" 38), cross-checked "
            "against an INDEPENDENT citation-side net (Semantic Scholar, 6 citing papers, "
            "returning the same 2 author-line candidates) and against Lushnikov's own "
            "maintained publication page, plus TWO md5-pinned `pdftotext -layout` full-text "
            "extractions (4336 lines) censused for ten computer-assisted-proof apparatus "
            "terms against a THIRD extraction from a DIFFERENT group as a bidirectional "
            "live-probe control; as of 2026-08-06. This is a BIBLIOGRAPHIC negative over that "
            "enumerated candidate set -- it is NOT a claim that the analysis cannot be so "
            "upgraded, only that this author line has not done it in the %d days since the "
            "parent appeared." % days),

        "search_log": SEARCH_LOG,
        "n_nets": len(SEARCH_LOG),
        "n_independent_nets_per_author": {"Lushnikov": 4, "Silantyev": 2, "Siegel": 1,
                                          "Ambrose": 2},

        "candidate_set": CANDIDATES,
        "n_candidates_on_object": n_on_object,
        "n_candidates_read_full_text": n_read,
        "n_candidates_with_certificate_apparatus": n_apparatus,
        "n_candidates_certifying_a_profile": n_profile,
        "n_subsequent_works_union_all_four_authors": N_SUBSEQUENT_UNION,
        "subsequent_works_union": SUBSEQUENT_UNION,
        "n_subsequent_works_by_author": SUBSEQUENT_COUNTS_BY_AUTHOR,
        "subsequent_works_by_author": SUBSEQUENT_BY_AUTHOR,
        "n_subsequent_works_summed_with_double_counting": sum(
            SUBSEQUENT_COUNTS_BY_AUTHOR.values()),
        "days_since_parent": days,

        "pdf_md5": PDF_MD5,
        "txt_md5": TXT_MD5,
        "extraction_lines": EXTRACTION_LINES,
        "extraction_lines_candidates_only": EXTRACTION_LINES[POLE] + EXTRACTION_LINES[PARAB],
        "apparatus_terms": APPARATUS_TERMS,
        "subject_terms": SUBJECT_TERMS,
        "census": CENSUS,
        "lone_apparatus_hit": LONE_APPARATUS_HIT,
        "key_quotes": KEY_QUOTES,
        "live_probe_control": live,
        "classifier_self_test": st,
        "all_self_tests_pass": all(st.values()),
        "prior_art_in_repo": PRIOR_ART,
        "n_prior_art_rows_that_asked_the_gate": sum(1 for r in PRIOR_ART if r["asked_the_gate"]),

        "sigma_coverage_of_the_author_line": {
            "exact_solutions_real_line_parent": "(a,sigma) in {(0,0),(0,1),(0,2),(1/2,1)}",
            "exact_solutions_periodic_followup": "(a,sigma) in {(0,0),(0,1),(1/2,0),(1/2,1)}",
            "sigma_2_periodic": ("NOT OBTAINED. arXiv:2411.01891 l.2358-2360: Schochet's "
                                 "real-line sigma=2 solution exists, but 'despite significant "
                                 "effort, we have been unable to generalize this solution to "
                                 "the periodic domain'."),
            "sigma_2_in_their_general_theory": ("sigma in (1,infty) reads GEIVP in every "
                                                "column of their Table 1 -- global existence "
                                                "for small data, the opposite side of the "
                                                "question from a blow-up profile."),
            "sigma_2_in_arXiv:2504.14346": ("in scope (sec 5, general sigma > 0), but the "
                                            "result is global existence + analyticity, with "
                                            "'self-similar' = 0 in the whole paper."),
            "certificates_at_any_sigma": 0,
        },

        "what_this_banks": (
            "The PRECEDENTS ledger row on arXiv:2207.07548 is CONFIRMED and now DATED, and it "
            "now holds of the AUTHOR LINE and not merely of the one paper: 19 subsequent works "
            "across the four authors, 2 on the object, 0 carrying any certification apparatus. "
            "Two facts the ledger row does not carry, for whoever owns solver/viscous_novelty.py "
            "(NOT edited by this leg): the parent is published as Nonlinearity 37, 025004 (2024) "
            "and the follow-up as Stud. Appl. Math. 155, e70115 (2025) -- this is a live, "
            "publishing line that has chosen not to go the certificate route, not a dormant one."),

        "bearing_on_legs_125_187_193": (
            "Confirming CONTEXT only, in the narrow sense the gate's NO branch specifies: the "
            "closest published precedent to this repository's gamma=2 dissipative gCLM line "
            "still has no certificate, and its authors' own most recent published word on "
            "sigma=2 is that the periodic case defeated them (2411.01891 l.2360) and that "
            "their next step is numerical investigation (l.2364). This does NOT make anything "
            "in legs 125/187/193 correct; it only means the frontier those legs are measured "
            "against has not moved."),

        "chain_impact": "none -- nothing here bears on any link of the L1->L4 chain",
        "escalation": None,

        "headline": (
            "GATE NO. Over 1483 days the four authors of arXiv:2207.07548 produced 19 "
            "distinct subsequent works; exactly 2 are on the object and both were read at "
            "full text, "
            "and neither carries a single self-claimed certification-apparatus term over 4336 "
            "lines. The joint follow-up -- Silantyev, Lushnikov, Siegel, Ambrose, Stud. Appl. "
            "Math. 155 e70115 (2025), all four parent authors -- is an EXACT POLE-DYNAMICS "
            "paper: closed-form solutions at sigma in {0,1} and a in {0,1/2} only, phase-plane "
            "analysis where closed form runs out (l.2309), and its own Table 1 puts every "
            "sigma > 1 (so sigma=2) in the GEIVP cell, i.e. small-data global existence, the "
            "opposite side of the question from a blow-up profile. On gamma=2 specifically "
            "they record a defeat: 'despite significant effort, we have been unable to "
            "generalize this solution to the periodic domain' (l.2360), and their own stated "
            "next step is to 'numerically investigate' (l.2364), not to certify. The second "
            "candidate, arXiv:2504.14346 (Ambrose + 2), IS on the dissipative CLM at general "
            "sigma > 0 -- found only by the math.AP cross-check net, since it is filed without "
            "the middle initial -- but proves global existence and analyticity, with "
            "'self-similar' = 0 in 1632 lines. The 10-term apparatus census fires 24 times on "
            "a different group's CAP paper and 0 times self-claimed across both candidates, "
            "while the object census fires 166 times on the candidates and 0 on the control: "
            "the probe is live in both directions. Separately, three initial-form author nets "
            "(au:\"Lushnikov_P\", au:\"Ambrose_D\", au:\"Siegel_M\") returned 14/164/156 "
            "entries containing NEITHER the parent NOR the follow-up -- leg 240's and 242's "
            "under-return failure, on three author lines at once. PRECEDENTS row confirmed and "
            "dated; no escalation."),
    }


def main():
    payload = build()
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "writeup", "data", "p2_route_alsl2_v1_lit.json")
    with open(out, "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)
        fh.write("\n")

    print("Leg 246 (Route-ALSL2) -- literature pass, %s" % payload["date"])
    print()
    print("PARENT %s  [%s: %s]" % (PARENT, payload["parent_precedents_ledger_verdict"],
                                   payload["parent_precedents_ledger_reason"]))
    print("  %s" % payload["parent_cite"])
    print()
    print("GATE: %s" % payload["gate_answer"])
    print("  verdict code                    %s" % payload["gate_verdict_code"])
    print("  escalates                       %s" % payload["escalates"])
    print("  nets run                        %d" % payload["n_nets"])
    print("  independent nets per author     %s" % payload["n_independent_nets_per_author"])
    print("  subsequent works, all 4 authors %d  over %d days"
          % (payload["n_subsequent_works_union_all_four_authors"],
             payload["days_since_parent"]))
    print("    on the object (gCLM/CLM)      %d" % payload["n_candidates_on_object"])
    print("    read at full text this leg    %d  (%d lines)"
          % (payload["n_candidates_read_full_text"],
             payload["extraction_lines_candidates_only"]))
    print("    carrying CAP apparatus        %d" % payload["n_candidates_with_certificate_apparatus"])
    print("    certifying a profile          %d" % payload["n_candidates_certifying_a_profile"])
    print()
    print("CANDIDATE SET (works by any of the four, after %s, ON THE OBJECT)"
          % PARENT_SUBMITTED.isoformat())
    for c in payload["candidate_set"]:
        print("  %-18s %s  all4=%-5s  apparatus=%-5s  profile=%-5s"
              % (c["id"], c["submitted"], c["all_four_parent_authors"],
                 c["has_certificate_apparatus"], c["certifies_a_profile"]))
        print("      method: %s" % c["method"])
        print("      sigma=2: %s" % c["sigma_2_status"].split(".")[0] + ".")
    print()
    print("TERM CENSUS over md5-pinned full-text extractions")
    print("  %-18s %5s  %-42s %s" % ("paper", "lines", "apparatus (10 terms)", "object (3 terms)"))
    for pid in (POLE, PARAB, CONTROL):
        app = sum(CENSUS[pid]["apparatus"][t] for t in APPARATUS_TERMS)
        obj = sum(CENSUS[pid]["subject"][t] for t in
                  ["dissipation", "pole", "Constantin-Lax-Majda"])
        tag = "  <- CONTROL, different group" if pid == CONTROL else ""
        print("  %-18s %5d  %-42d %d%s" % (pid, EXTRACTION_LINES[pid], app, obj, tag))
    print()
    h = payload["lone_apparatus_hit"]
    print("THE LONE APPARATUS HIT IN THE CANDIDATE SET (not rounded to zero)")
    print("  %s l.%d  '%s' x%d" % (h["paper"], h["line"], h["term"], h["count"]))
    print("  -> %s" % h["quote"])
    print("  -> it cites Chen-Hou; self-claimed apparatus total across both candidates is 0")
    print()
    lp = payload["live_probe_control"]
    print("LIVE-PROBE CONTROL, BIDIRECTIONAL (lesson 90)")
    print("  apparatus terms, 2 candidates   %d  (self-claimed %d)"
          % (lp["apparatus_terms_total_over_2_candidates"],
             lp["apparatus_terms_total_self_claimed_by_candidates"]))
    print("  apparatus terms, control        %d  -> (a) control fires: %s"
          % (lp["apparatus_terms_total_over_control"],
             lp["direction_a_control_fires_on_apparatus"]))
    print("  object terms, 2 candidates      %d" % lp["object_terms_total_over_2_candidates"])
    print("  object terms, control           %d  -> (b) control silent: %s"
          % (lp["object_terms_total_over_control"],
             lp["direction_b_control_is_silent_on_the_object"]))
    print("  probe is live                   %s" % lp["probe_is_live"])
    print()
    print("CLASSIFIER SELF-TEST (lesson 90)")
    for k, v in payload["classifier_self_test"].items():
        print("  %-58s %s" % (k, v))
    print("  ALL PASS: %s" % payload["all_self_tests_pass"])
    print()
    print("IN-REPO PRIOR ART -- who already held arXiv:2411.01891, and at what depth")
    for r in payload["prior_art_in_repo"]:
        print("  %-52s %-14s asked-the-gate=%s"
              % (r["where"][:52], r["depth"], r["asked_the_gate"]))
    print("  rows that asked the gate's question: %d"
          % payload["n_prior_art_rows_that_asked_the_gate"])
    print()
    print("SIGMA COVERAGE OF THE AUTHOR LINE")
    for k, v in payload["sigma_coverage_of_the_author_line"].items():
        print("  %-36s %s" % (k, v))
    print()
    print(payload["headline"])
    print()
    print("wrote %s" % out)


if __name__ == "__main__":
    main()
