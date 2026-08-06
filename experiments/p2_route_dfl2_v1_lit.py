#!/usr/bin/env python3
"""Leg 242 (Route-DFL2) -- literature runner applying this repository's own established
"check for later work by the same authors" pattern (legs 175->196, 174/197->240) to the ONE
author line it had never been applied to: Dahne & Figueras, arXiv:2410.05480, the CGL
interval-verification paper that closed stage V for non-novelty and that leg 48 independently
re-derived to 1.8e-07.

    .venv/bin/python experiments/p2_route_dfl2_v1_lit.py

THE QUESTION (pre-committed gate, both branches, DIRECTION.md leg 242):

    Does Dahne & Figueras's subsequent published work extend the interval-verification
    technique to a fluid/vortex-dynamics-adjacent model, or complete the CGL work into an
    actual certified blow-up?

    YES (either) -> bears on leg 174's "missing rung" occupancy matrix; record the citation and
                    its hypotheses verbatim, name the cell, ESCALATE, park, push branch only.
    NO           -> report the SEARCH precisely, not just the absence; bank as confirming leg
                    174's catalog is still current on this specific author line.

WHAT THIS IS. A literature leg has no PDE to integrate, so the runner is what keeps the prose
honest (the pattern legs 175/183/189/196/240 established): every count and every number quoted
in writeup/novelty/leg_242.md and experiments/journal/leg_242.md is transcribed here ONCE, from
the primary source, with its line locator in a named md5-pinned extraction; the gate verdict is
COMPUTED from that table rather than asserted. It emits writeup/data/p2_route_dfl2_v1_lit.json.

WHY THE VERDICT IS COMPUTED (lesson 90 -- a control that cannot come out differently is not a
control). The gate's YES branch escalates and parks the leg, so it must be reachable on
evidence that warranted it and not reachable by prose alone. `classify()` takes the evidence
table and returns one of

    EXTENDED_TO_FLUID_ADJACENT | COMPLETED_TO_BLOWUP_CERTIFICATE
    | NO_SUCH_SUBSEQUENT_WORK  | NO_SUBSEQUENT_WORK_AT_ALL

and `self_test()` exercises all four on perturbed copies of the evidence.

THE LIVE-PROBE CONTROL, AND IT IS THE ONE THAT MATTERS (lesson 90 again). This leg's negative
rests on a term census returning ZERO for every fluid and every blow-up term over three
full-text extractions. A census that returns zero because it is not measuring anything is
exactly leg 53's failure. So the SAME census, on the SAME extractions, is required to return
NON-ZERO for the certification-apparatus terms -- and it does: `interval arithmetic` fires 9
times in arXiv:2410.18536 and 6 times in arXiv:2601.16285 while `blow-up`, `blowup`,
`self-similar` and `vorticit` are 0/0/0/0 in all three. The probe is demonstrably live; the
zeros are a property of the papers, not of the code. `assert_probe_is_live()` enforces this and
fails the run if the apparatus terms ever go to zero too.

PROVENANCE. Three PDFs were pulled from arxiv.org during this leg and extracted with
`pdftotext -layout`; `line` fields locate quotes in those extractions. Papers/ is gitignored.

    arXiv:2607.03498v1  md5 85c9536b2536b779e10da4b4602b1599   2357 lines
    arXiv:2410.18536v2  md5 8ed84e59afd281d6b4d3972fb77a05a8   1093 lines
    arXiv:2601.16285v1  md5 fabbb42de4e3746e0a69a81525daf594   3206 lines

NO NETWORK ACCESS at run time; every network result is transcribed as data below. No solver
module is read, imported or edited. No stage is claimed; plan_of_record.py is untouched.

BANS CHECKED BEFORE STARTING (plan_of_record.py output read in full). The one that could bind
is "re-opening stage V as posed" -- NOT TRIPPED: no certificate is built, no dissipation
parameter is floated against any margin, nothing is re-derived. This is a bibliographic
question about an author line, the same shape as legs 174/196/240. gCLM measurement: none.
Route-D sharpening: none. GA compute: none. l1-Fourier / collocation machinery: none built.
Leg 51 re-claim: not made. "grep capabilities.py before building": grepped (2410.05480 appears
there as a novelty-ledger row; not touched).
"""

import json
import os
from datetime import date

PASS_DATE = "2026-08-06"

PARENT = "arXiv:2410.05480v2"   # Dahne & Figueras -- the CGL paper that closed stage V
SNBIF = "arXiv:2607.03498v1"    # Figueras, Gimeno, Parker -- the only fluid-ADJACENT-looking one
MATHIEU = "arXiv:2410.18536v2"  # Figueras & Puig -- subsequent interval-arithmetic CAP
POLYGON = "arXiv:2601.16285v1"  # Dahne, Gomez-Serrano, Pech-Alberich -- Dahne's only subsequent

PDF_MD5 = {
    SNBIF: "85c9536b2536b779e10da4b4602b1599",
    MATHIEU: "8ed84e59afd281d6b4d3972fb77a05a8",
    POLYGON: "fabbb42de4e3746e0a69a81525daf594",
}
EXTRACTION_LINES = {SNBIF: 2357, MATHIEU: 1093, POLYGON: 3206}

# --------------------------------------------------------------------------------------
# 1. HOW THE CANDIDATE SET WAS CLOSED.  Author-LISTING enumerations, not keyword searches:
#    a follow-up with an unexpected title cannot be missed by a listing the way it can by a
#    keyword query.  Two independent nets per author, plus author-maintained pages, plus a
#    third keyword net.  The gate's no-branch demands the search be reported, not the absence.
# --------------------------------------------------------------------------------------

SEARCH_LOG = [
    {"id": "N1", "kind": "arxiv-api-author-listing", "n_entries": 10,
     "query": 'https://export.arxiv.org/api/query?search_query=au:"Dahne"'
              '&max_results=300&sortBy=submittedDate&sortOrder=descending',
     "note": "complete career listing for the surname. 6 of the 10 are Joel Dahne; the other "
             "4 are Sven Dahne (machine-learning, 2016-2018) -- a homonym collision inside the "
             "SAME listing, recorded because an unexamined listing would have inflated the "
             "count. Newest Joel Dahne entry 2601.16285 (2026-01-22)."},
    {"id": "N2", "kind": "arxiv-api-author-listing", "n_entries": 18,
     "query": 'https://export.arxiv.org/api/query?search_query=au:"Jordi-Lluis Figueras"'
              '&max_results=300&sortBy=submittedDate&sortOrder=descending',
     "note": "complete career listing, 2016-01-01 -> 2026-07-03, read entry by entry. This is "
             "the decisive net for Figueras."},
    {"id": "N3", "kind": "arxiv-api-author-listing-FAILED-FORM", "n_entries": 0,
     "query": 'https://export.arxiv.org/api/query?search_query=au:"Figueras_J"',
     "note": "RETURNS ZERO. Recorded, not discarded: this is exactly leg 240's methodological "
             "failure (au:\"Buckmaster_T\" -> 2 entries, newest 2016) recurring on a different "
             "author line. A query that silently under-returns is indistinguishable from a "
             "clean negative, which is this repository's recurring failure mode. Had this been "
             "the only Figueras net, the leg would have reported NO for the wrong reason."},
    {"id": "N4", "kind": "arxiv-api-author-listing-BROAD-CROSSCHECK", "n_entries": 300,
     "query": 'https://export.arxiv.org/api/query?search_query=au:"Figueras"'
              '&max_results=300&sortBy=submittedDate&sortOrder=descending',
     "note": "surname-only net, window 2021-11-04 -> 2026-08-04, swamped by the LHCb "
             "collaboration and by Pau Figueras (gravity). Run as an independent cross-check "
             "of N2: 11 of the 300 carry a genuine Jordi-Lluis Figueras authorship and ALL 11 "
             "are in N2's 18 -- zero missing. A loose first-name filter ('Jordi' anywhere) "
             "additionally catches 16 false positives from 4 colliding authors (C. Jordi, "
             "Carme Jordi, Jordi Armengol-Estape, Jordi Miralda-Escude)."},
    {"id": "N5", "kind": "author-maintained-page", "n_entries": 8,
     "query": "https://dahne.eu/publications/",
     "note": "Joel Dahne's own page. Carries publication STATUS the arXiv listing does not. "
             "2 of the 8 are not in N1 at all (Enclosing all zeros of a system of analytic "
             "functions, AMC 348, 2019; Swapping trajectories with a sufficient sanitizer, "
             "PRL 2020) -- both PRE-date 2410.05480 and neither is fluid or blow-up. "
             "2410.05480 is listed as 'Submitted', not published."},
    {"id": "N6", "kind": "author-maintained-page", "n_entries": 22,
     "query": "https://www2.math.uu.se/~jorfi688/publications.html",
     "note": "Jordi-Lluis Figueras's own page, last update 2025-12-10, split into Submitted / "
             "Accepted / published. 2410.05480 sits under 'Submitted'. 2410.18536 is 'Accepted', "
             "Communications in Nonlinear Science and Numerical Simulation, Volume 152 (2026) "
             "-- journal status the arXiv listing does not carry."},
    {"id": "N7", "kind": "arxiv-api-id-query", "n_entries": 1,
     "query": "https://export.arxiv.org/api/query?id_list=2410.05480",
     "note": "version/journal status of the parent itself: still v2, updated 2024-12-20, "
             "NO journal_ref field. Corroborates N5 and N6."},
    {"id": "N8", "kind": "arxiv-api-author-listing-COAUTHOR", "n_entries": 46,
     "query": 'https://export.arxiv.org/api/query?search_query=au:"Gomez-Serrano"',
     "note": "Dahne's other coauthor, in scope under the gate's '(or a coauthor)'. This exact "
             "listing was already closed by leg 240 (46 entries, newest 2605.18699). Its "
             "fluid/blow-up entries are prior art HERE, not new candidates: 2509.14185 "
             "(unstable singularities) is legs 175/196's object and 2511.22819 its follow-up "
             "(leg 212/196); 2208.09445 / 2310.05325 are legs 174/240's. Not re-litigated."},
    {"id": "N9", "kind": "arxiv-api-author-listing-COAUTHOR", "n_entries": 16,
     "query": 'https://export.arxiv.org/api/query?search_query=au:"Jeremy Parker"',
     "note": "Figueras's newest coauthor, and the reason 2607.03498 was read at full text: "
             "Parker is a fluid dynamicist (Navier-Stokes periodic orbits, Kelvin-Helmholtz, "
             "viscous Holmboe instability). If the technique were going to reach a fluid "
             "model through this author line, this is the coauthor it would go through."},
    {"id": "N10", "kind": "web-keyword-search",
     "query": "Dahne Figueras self-similar singular solutions Ginzburg-Landau interval "
              "arithmetic follow-up 2026 fluid Euler blow-up",
     "note": "third net. Returned the parent, the Princeton seminar copy, dahne.eu, and "
             "unrelated analytic NLS/CGL blow-up literature. No follow-up surfaced."},
    {"id": "N11", "kind": "web-keyword-search",
     "query": '"Figueras" computer-assisted proof 2026 self-similar blow-up Euler '
              'Navier-Stokes interval arithmetic Uppsala',
     "note": "returned the live fluid-blow-up CAP literature (Chen-Hou, Hou-Wang-Yang, "
             "2208.09445) -- none of it by this author line. A useful negative: the query "
             "DOES surface fluid blow-up CAPs when they exist, it just never attaches this "
             "author line to one."},
    {"id": "N12", "kind": "web-keyword-search",
     "query": '"Joel Dahne" OR "Jordi-Lluis Figueras" 2026 preprint computer-assisted vortex '
              'vorticity blow-up certified',
     "note": "returned the parent, the CAPA team page, Figueras's homepage, and unrelated "
             "Gomez-Serrano fluid papers. No new candidate."},
]

# --------------------------------------------------------------------------------------
# 2. THE CANDIDATE SET.  Every work by either author submitted after the parent (2024-10-07),
#    from N1/N2, cross-checked against N4/N5/N6.  This is the whole set, not a selection.
# --------------------------------------------------------------------------------------

SUBSEQUENT = [
    {"id": "arXiv:2410.18536", "date": "2024-10-24", "cat": "math.DS",
     "authors": ["Jordi-Lluis Figueras", "Joaquim Puig"],
     "title": "Computer Validation of Open Gaps for the Almost Mathieu Operator with "
              "Critical Coupling",
     "status": "Accepted, Commun. Nonlinear Sci. Numer. Simul. 152 (2026)  [N6]",
     "object": "quasi-periodic Schrodinger cocycle (almost Mathieu operator), spectral gaps",
     "interval_verified": True, "fluid_adjacent": False, "blow_up": False,
     "read_full_text": True},
    {"id": "arXiv:2410.22384", "date": "2024-10-29", "cat": "math.ST",
     "authors": ["Jordi-Lluis Figueras", "Aron Persson", "Lauri Viitasaari"],
     "title": "On parameter estimation for N(mu, sigma^2 I_3) based on projected data into S^2",
     "status": "Modern Stochastics: Theory and Applications (2025)  [N6]",
     "object": "directional statistics / parameter estimation",
     "interval_verified": False, "fluid_adjacent": False, "blow_up": False,
     "read_full_text": False},
    {"id": "arXiv:2509.24767", "date": "2025-09-29", "cat": "math.ST",
     "authors": ["Jordi-Lluis Figueras", "Aron Persson"],
     "title": "Autoregressive Processes on Stiefel and Grassmann Manifolds",
     "status": "Submitted  [N6]",
     "object": "stochastic processes on matrix manifolds",
     "interval_verified": False, "fluid_adjacent": False, "blow_up": False,
     "read_full_text": False},
    {"id": "arXiv:2511.02680", "date": "2025-11-04", "cat": "math.ST",
     "authors": ["Jordi-Lluis Figueras", "Aron Persson", "Lauri Viitasaari"],
     "title": "On the Convergence of the Extended Kalman Filter on Stiefel Manifolds when "
              "Observing a Constant Signal",
     "status": "Submitted  [N6]",
     "object": "filtering theory on matrix manifolds",
     "interval_verified": False, "fluid_adjacent": False, "blow_up": False,
     "read_full_text": False},
    {"id": "arXiv:2511.02682", "date": "2025-11-04", "cat": "stat.AP",
     "authors": ["Jordi-Lluis Figueras", "Aron Persson", "Lauri Viitasaari"],
     "title": "Extended Kalman Filtering on Stiefel Manifolds",
     "status": "Submitted  [N6]",
     "object": "filtering theory on matrix manifolds",
     "interval_verified": False, "fluid_adjacent": False, "blow_up": False,
     "read_full_text": False},
    {"id": "arXiv:2601.16285", "date": "2026-01-22", "cat": "math.SP",
     "authors": ["Joel Dahne", "Javier Gomez-Serrano", "Joana Pech-Alberich"],
     "title": "Monotonicity of the first Dirichlet eigenvalue of regular polygons",
     "status": "Submitted  [N5]",
     "object": "Dirichlet Laplacian eigenvalues of regular N-gons (Antunes-Freitas conjecture)",
     "interval_verified": True, "fluid_adjacent": False, "blow_up": False,
     "read_full_text": True},
    {"id": "arXiv:2607.03498", "date": "2026-07-03", "cat": "math.DS",
     "authors": ["Jordi-Lluis Figueras", "Joan Gimeno", "Jeremy Parker"],
     "title": "Numerical Computation of Quasiperiodic Reducible Saddle-Node Bifurcations: "
              "a Parameterization Method approach",
     "status": "preprint, 2026-07-03 (post-dates N6's 2025-12-10 page update)",
     "object": "two ODE toy models: a saddle-node toy model and a 3D saddle-node model",
     "interval_verified": False, "fluid_adjacent": False, "blow_up": False,
     "read_full_text": True},
]

# Joint works by the two authors of the parent, over their whole careers (N1 x N2).
JOINT_WORKS_EVER = ["arXiv:2410.05480"]
JOINT_WORKS_SUBSEQUENT = []

# --------------------------------------------------------------------------------------
# 3. THE TERM CENSUS.  Case-insensitive substring counts over the FULL pdftotext -layout
#    extraction of each paper read this leg -- a measurement, not an impression.
# --------------------------------------------------------------------------------------

FLUID_TERMS = ["fluid", "Navier", "Euler", "vorticit", "turbulen", "viscos", "Couette"]
BLOWUP_TERMS = ["blow-up", "blowup", "singularit", "self-similar", "dissipat"]
APPARATUS_TERMS = ["interval arithmetic", "computer-assisted", "validated numerics",
                   "rigorous", "enclosure"]

CENSUS = {
    SNBIF: {"fluid": 3, "Navier": 2, "Euler": 0, "vorticit": 0, "turbulen": 4, "viscos": 0,
            "Couette": 0,
            "blow-up": 0, "blowup": 0, "singularit": 3, "self-similar": 0, "dissipat": 15,
            "interval arithmetic": 0, "computer-assisted": 2, "validated numerics": 1,
            "rigorous": 10, "enclosure": 0},
    MATHIEU: {"fluid": 0, "Navier": 0, "Euler": 0, "vorticit": 0, "turbulen": 0, "viscos": 0,
              "Couette": 0,
              "blow-up": 0, "blowup": 0, "singularit": 0, "self-similar": 0, "dissipat": 0,
              "interval arithmetic": 9, "computer-assisted": 6, "validated numerics": 4,
              "rigorous": 19, "enclosure": 0},
    POLYGON: {"fluid": 0, "Navier": 0, "Euler": 1, "vorticit": 0, "turbulen": 0, "viscos": 0,
              "Couette": 0,
              "blow-up": 0, "blowup": 0, "singularit": 10, "self-similar": 0, "dissipat": 0,
              "interval arithmetic": 6, "computer-assisted": 11, "validated numerics": 1,
              "rigorous": 16, "enclosure": 65},
}

# Every non-zero fluid/blow-up-looking count above, resolved at its line locator so it cannot
# be over-read.  This is where "singularit = 10" stops being alarming.
DISAMBIGUATION = [
    {"paper": SNBIF, "term": "fluid/Navier/turbulen", "count": 3 + 2 + 4, "verdict": "MOTIVATION+BIBLIOGRAPHY",
     "line": 91,
     "quote": "In particular, in fluid dynamics, the breakdown of an invariant torus arising "
              "from a Neimark-Sacker bifurcation has been hypothesized [RT71; NRT78] and has "
              "been observed in experiments and simulations [SG78; MSE89; Van05] to be a "
              "dominant route to turbulence in many configurations of the Navier-Stokes "
              "equations.",
     "note": "The word 'fluid' never attaches to an object this paper computes. The two "
             "numerical experiments are section 4.1 'Toy saddle-node model' and section 4.2 "
             "'3D saddle-node model'. Remaining hits are reference titles (J. Fluid Mech.)."},
    {"paper": SNBIF, "term": "dissipat", "count": 15, "verdict": "DISSIPATIVE-DYNAMICS-JARGON",
     "line": 89,
     "quote": "Numerical evidence suggests that many dissipative systems do indeed exhibit "
              "structurally and dynamically stable invariant tori",
     "note": "'dissipative system' in the dynamical-systems sense (non-volume-preserving "
             "flow), NOT a viscosity/diffusion term. viscos = 0 in this paper."},
    {"paper": SNBIF, "term": "singularit", "count": 3, "verdict": "NOT-BLOWUP", "line": 0,
     "quote": "", "note": "no finite-time singularity anywhere; blow-up = blowup = "
                          "self-similar = 0 over all 2357 lines."},
    {"paper": POLYGON, "term": "singularit", "count": 10, "verdict": "INTEGRAND-SINGULARITY",
     "line": 723,
     "quote": "The integrand has a (integrable) singularity at t = 0, to handle this we split "
              "the integral as",
     "note": "All 10 hits are integrable or REMOVABLE singularities of integrands in the "
             "enclosure computation (lines 723, 739, 1810, 1890, 2031, 2043, 2066, 2081, 2308) "
             "plus one reference title (line 3100, Gopal-Trefethen, 'corner singularities'). "
             "None is a solution blowing up."},
    {"paper": POLYGON, "term": "Euler", "count": 1, "verdict": "EULERS-CONSTANT", "line": 933,
     "quote": "representation of the digamma function, psi_0(z) = ... - gamma_0 for Re(z) > 0 "
              "and where gamma_0 stands for the Euler",
     "note": "Euler-Mascheroni constant. Not the Euler equations."},
]

# The single sentence that decides 2607.03498, in the authors' own words.
KEY_QUOTES = [
    {"paper": SNBIF, "line": 1556, "what": "self-disclaimer: not a computer-assisted proof",
     "quote": "Although this paper does not include a computer-assisted proof, we carried out "
              "all computations in multiprecision following that validation-oriented "
              "philosophy, so that the numerics are compatible with future rigorous "
              "extensions."},
    {"paper": SNBIF, "line": 26, "what": "what the paper actually delivers",
     "quote": "We give explicit algorithms for the methods and demonstrate their "
              "applicability with two numerical examples."},
    {"paper": SNBIF, "line": 87, "what": "the closest the paper comes to a PDE ambition",
     "quote": "Finally, exploring the scalability of the method to high-dimensional partial "
              "differential equations (PDEs) through the use of efficient Fourier-spectral "
              "implementations remains an area of active interest."},
    {"paper": POLYGON, "line": 9, "what": "the object certified instead",
     "quote": "In this paper we prove that the first Dirichlet eigenvalue lambda_1^N of an "
              "N-sided regular polygon of fixed area is a monotonically decreasing function "
              "of N for all N >= 3 ... This settles a conjecture of Antunes-Freitas from "
              "2006 [1, Conjecture 3.2]."},
]

# Leg 174's occupancy matrix, transcribed from writeup/data/p2_route_vbs_v1_scoping.json's
# occupancy_matrix as this leg found it.  This leg changes nothing in it; it reports whether
# anything it found would have.
LEG_174_MATRIX = {
    "fluid_adjacent__gradeA": None,                 # THE EMPTY CELL
    "fluid_adjacent__gradeB": "arXiv:2208.09445",   # compressible Navier-Stokes
    "not_fluid_adjacent__gradeA": "arXiv:2410.05480",   # CGL -- the parent of THIS leg
    "not_fluid_adjacent__gradeB": None,
}


# --------------------------------------------------------------------------------------
# 4. THE CLASSIFIER, AND ITS SELF-TEST.
# --------------------------------------------------------------------------------------

def classify(subsequent, joint_subsequent):
    """Compute the gate verdict from the evidence table. Four reachable outcomes."""
    if not subsequent:
        return "NO_SUBSEQUENT_WORK_AT_ALL"
    for w in subsequent:
        if w["blow_up"] and w["interval_verified"]:
            return "COMPLETED_TO_BLOWUP_CERTIFICATE"
    for w in subsequent:
        if w["fluid_adjacent"] and w["interval_verified"]:
            return "EXTENDED_TO_FLUID_ADJACENT"
    return "NO_SUCH_SUBSEQUENT_WORK"


def self_test():
    """Each branch fired on a perturbed copy of the real evidence (lesson 90)."""
    real = SUBSEQUENT
    out = {}
    out["real_evidence_gives_NO"] = (
        classify(real, JOINT_WORKS_SUBSEQUENT) == "NO_SUCH_SUBSEQUENT_WORK")

    empty = classify([], [])
    out["empty_set_gives_NO_SUBSEQUENT_WORK_AT_ALL"] = (empty == "NO_SUBSEQUENT_WORK_AT_ALL")

    # flip 2607.03498 to interval-verified AND fluid-adjacent -> the escalation branch
    pert = [dict(w) for w in real]
    for w in pert:
        if w["id"] == "arXiv:2607.03498":
            w["interval_verified"] = True
            w["fluid_adjacent"] = True
    out["fluid_plus_interval_gives_ESCALATION"] = (
        classify(pert, []) == "EXTENDED_TO_FLUID_ADJACENT")

    # flip 2410.18536 to a certified blow-up -> the other escalation branch
    pert2 = [dict(w) for w in real]
    for w in pert2:
        if w["id"] == "arXiv:2410.18536":
            w["blow_up"] = True
    out["blowup_plus_interval_gives_ESCALATION"] = (
        classify(pert2, []) == "COMPLETED_TO_BLOWUP_CERTIFICATE")

    # a fluid paper with NO interval arithmetic must NOT escalate -- 2607.03498's actual shape
    pert3 = [dict(w) for w in real]
    for w in pert3:
        if w["id"] == "arXiv:2607.03498":
            w["fluid_adjacent"] = True
    out["fluid_without_interval_does_NOT_escalate"] = (
        classify(pert3, []) == "NO_SUCH_SUBSEQUENT_WORK")
    return out


def assert_probe_is_live():
    """The census must be capable of reporting non-zero, or its zeros mean nothing.

    Returns the evidence that it is: apparatus terms fire where fluid/blow-up terms do not,
    in the SAME extractions under the SAME counting code.
    """
    fluid_blowup_total = 0
    for pid, row in CENSUS.items():
        for t in ("blow-up", "blowup", "self-similar", "vorticit", "viscos", "Couette"):
            fluid_blowup_total += row[t]
    apparatus_total = sum(CENSUS[p]["interval arithmetic"] for p in CENSUS)
    assert apparatus_total > 0, "census probe is dead -- apparatus terms zero too"
    return {
        "hard_fluid_and_blowup_term_total_over_3_papers": fluid_blowup_total,
        "interval_arithmetic_total_over_same_3_papers": apparatus_total,
        "per_paper_interval_arithmetic": {p: CENSUS[p]["interval arithmetic"] for p in CENSUS},
        "probe_is_live": apparatus_total > 0,
        "terms_counted_as_hard": ["blow-up", "blowup", "self-similar", "vorticit", "viscos",
                                  "Couette"],
    }


def build():
    verdict = classify(SUBSEQUENT, JOINT_WORKS_SUBSEQUENT)
    live = assert_probe_is_live()
    st = self_test()

    parent_v1 = date(2024, 10, 7)
    parent_v2 = date(2024, 12, 20)
    today = date(*[int(x) for x in PASS_DATE.split("-")])

    n_interval = sum(1 for w in SUBSEQUENT if w["interval_verified"])
    n_fluid = sum(1 for w in SUBSEQUENT if w["fluid_adjacent"])
    n_blowup = sum(1 for w in SUBSEQUENT if w["blow_up"])
    n_read = sum(1 for w in SUBSEQUENT if w["read_full_text"])

    return {
        "leg": 242,
        "route": "DFL2",
        "role": "LIT",
        "date": PASS_DATE,
        "claims_stage": None,
        "parent_paper": PARENT,
        "gate_question": (
            "Does Dahne & Figueras's subsequent published work extend the interval-"
            "verification technique to a fluid/vortex-dynamics-adjacent model, or complete "
            "the CGL work into an actual certified blow-up?"),
        "gate_answer": "NO",
        "gate_verdict_code": verdict,
        "gate_answer_realization": (
            "NO, in the realization: arXiv author-listing enumeration over the complete "
            "career listings of both authors (au:\"Dahne\" 10 entries, "
            "au:\"Jordi-Lluis Figueras\" 18 entries), cross-checked against a broad "
            "surname net (au:\"Figueras\", 300 entries, 11/11 agreement, 0 missing) and "
            "against both authors' own maintained publication pages, plus three md5-pinned "
            "`pdftotext -layout` full-text extractions (6656 lines total) censused for fluid "
            "and blow-up terms; as of 2026-08-06. This is a bibliographic negative over that "
            "enumerated candidate set -- it is NOT a claim that the technique cannot be so "
            "extended, only that this author line has not done it and has published nothing "
            "in that direction in the 668 days since the parent appeared."),

        "search_log": SEARCH_LOG,
        "n_nets": len(SEARCH_LOG),

        "candidate_set": SUBSEQUENT,
        "n_subsequent_works_on_author_line": len(SUBSEQUENT),
        "n_subsequent_joint_works": len(JOINT_WORKS_SUBSEQUENT),
        "joint_works_ever": JOINT_WORKS_EVER,
        "n_subsequent_interval_verified": n_interval,
        "n_subsequent_fluid_adjacent": n_fluid,
        "n_subsequent_blow_up": n_blowup,
        "n_read_full_text_this_leg": n_read,

        "parent_publication_status": {
            "latest_version": "v2",
            "v1_submitted": parent_v1.isoformat(),
            "v2_updated": parent_v2.isoformat(),
            "journal_ref": None,
            "author_page_status_dahne": "Submitted",
            "author_page_status_figueras": "Submitted",
            "days_since_v1": (today - parent_v1).days,
            "days_since_v2": (today - parent_v2).days,
            "reading": ("The CGL work has not been completed into anything -- it has not even "
                        "reached a journal. Both authors' own pages still file it under "
                        "'Submitted' 668 days after v1. The gate's second clause ('complete "
                        "the CGL work into an actual certified blow-up') has no candidate at "
                        "all, not a weak one."),
        },

        "pdf_md5": PDF_MD5,
        "extraction_lines": EXTRACTION_LINES,
        "extraction_lines_total": sum(EXTRACTION_LINES.values()),
        "census": CENSUS,
        "disambiguation": DISAMBIGUATION,
        "key_quotes": KEY_QUOTES,
        "live_probe_control": live,
        "classifier_self_test": st,
        "all_self_tests_pass": all(st.values()),

        "leg_174_occupancy_matrix_before": LEG_174_MATRIX,
        "leg_174_occupancy_matrix_after": LEG_174_MATRIX,
        "matrix_changed": False,
        "cell_this_leg_would_have_filled": "fluid_adjacent__gradeA",

        "prior_art_not_relitigated": {
            "arXiv:2509.14185": "legs 175 / 196 / 212 (Gomez-Serrano coauthor line)",
            "arXiv:2511.22819": "legs 196 / 212",
            "arXiv:2208.09445": "legs 174 / 197 / 240",
            "arXiv:2310.05325": "leg 240",
            "arXiv:2410.05480": "legs 48 (re-derived to 1.8e-07) / 174 (full text) / 189",
        },

        "headline": (
            "GATE NO on both clauses. Dahne and Figueras have published NOTHING together "
            "since arXiv:2410.05480 -- it remains their only joint paper, still v2 of "
            "2024-12-20 with no journal_ref and filed as 'Submitted' on both authors' own "
            "pages 668 days on. Individually the author line produced 7 subsequent works "
            "(1 Dahne, 6 Figueras), of which 2 are genuine interval-arithmetic computer-"
            "assisted proofs -- but of a quasi-periodic Schrodinger cocycle "
            "(arXiv:2410.18536, Almost Mathieu open gaps, accepted CNSNS 152 (2026)) and of "
            "Dirichlet eigenvalues of regular polygons (arXiv:2601.16285, settling "
            "Antunes-Freitas). 0 of 7 are fluid/vortex-adjacent and 0 of 7 concern blow-up. "
            "The one candidate whose coauthor is a fluid dynamicist (arXiv:2607.03498, "
            "Figueras-Gimeno-Parker) disclaims itself in one sentence at line 1556 -- "
            "'this paper does not include a computer-assisted proof' -- and computes two ODE "
            "toy models, with 'fluid' appearing only in the route-to-turbulence motivation. "
            "Over 6656 lines of full text the terms blow-up/blowup/self-similar/vorticity/"
            "viscosity total 0 while 'interval arithmetic' totals 15, so the census is a live "
            "probe and the zeros are a property of the papers. Leg 174's "
            "(fluid-adjacent, Grade A) cell is untouched and still EMPTY."),
    }


def main():
    payload = build()
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "writeup", "data", "p2_route_dfl2_v1_lit.json")
    with open(out, "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)
        fh.write("\n")

    print("Leg 242 (Route-DFL2) -- literature pass, %s" % payload["date"])
    print()
    print("GATE: %s" % payload["gate_answer"])
    print("  verdict code                 %s" % payload["gate_verdict_code"])
    print("  nets run                     %d" % payload["n_nets"])
    print("  subsequent works on the line %d  (joint Dahne+Figueras: %d)"
          % (payload["n_subsequent_works_on_author_line"],
             payload["n_subsequent_joint_works"]))
    print("    interval-verified          %d" % payload["n_subsequent_interval_verified"])
    print("    fluid/vortex-adjacent      %d" % payload["n_subsequent_fluid_adjacent"])
    print("    blow-up                    %d" % payload["n_subsequent_blow_up"])
    print("    read at full text this leg %d  (%d lines total)"
          % (payload["n_read_full_text_this_leg"], payload["extraction_lines_total"]))
    print()
    p = payload["parent_publication_status"]
    print("PARENT %s: %s, updated %s, journal_ref %s"
          % (PARENT, p["latest_version"], p["v2_updated"], p["journal_ref"]))
    print("  days since v1 %d / since v2 %d;  author pages say '%s' / '%s'"
          % (p["days_since_v1"], p["days_since_v2"],
             p["author_page_status_dahne"], p["author_page_status_figueras"]))
    print()
    print("CANDIDATE SET (every work by either author after 2024-10-07)")
    for w in payload["candidate_set"]:
        print("  %-17s %s %-9s iv=%-5s fluid=%-5s blowup=%-5s %s"
              % (w["id"], w["date"], w["cat"], w["interval_verified"], w["fluid_adjacent"],
                 w["blow_up"], w["title"][:52]))
    print()
    print("TERM CENSUS over md5-pinned full-text extractions")
    for pid in (SNBIF, MATHIEU, POLYGON):
        row = CENSUS[pid]
        print("  %-17s %4d lines  fluid=%d Navier=%d vorticit=%d blow-up=%d self-similar=%d "
              "| interval arithmetic=%d"
              % (pid, EXTRACTION_LINES[pid], row["fluid"], row["Navier"], row["vorticit"],
                 row["blow-up"], row["self-similar"], row["interval arithmetic"]))
    print()
    lp = payload["live_probe_control"]
    print("LIVE-PROBE CONTROL (lesson 90)")
    print("  hard fluid+blow-up terms, 3 papers   %d" %
          lp["hard_fluid_and_blowup_term_total_over_3_papers"])
    print("  'interval arithmetic', same 3 papers %d  -> probe is live: %s"
          % (lp["interval_arithmetic_total_over_same_3_papers"], lp["probe_is_live"]))
    print()
    print("CLASSIFIER SELF-TEST (lesson 90)")
    for k, v in payload["classifier_self_test"].items():
        print("  %-42s %s" % (k, v))
    print("  ALL PASS: %s" % payload["all_self_tests_pass"])
    print()
    print("LEG 174 OCCUPANCY MATRIX")
    for k, v in payload["leg_174_occupancy_matrix_after"].items():
        print("  %-30s %s" % (k, v if v else "-- EMPTY --"))
    print("  changed by this leg: %s" % payload["matrix_changed"])
    print()
    print(payload["headline"])
    print()
    print("wrote %s" % out)


if __name__ == "__main__":
    main()
