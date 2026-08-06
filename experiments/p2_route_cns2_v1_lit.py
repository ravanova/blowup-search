#!/usr/bin/env python3
"""Leg 240 (Route-CNS2) -- literature runner for the follow-on question legs 174/197 did not
ask: does the author group of arXiv:2208.09445 (Buckmaster, Cao-Labora, Gomez-Serrano) have
SUBSEQUENT work that upgrades the viscous-term treatment from DOMINATED to ENCLOSED?

    .venv/bin/python experiments/p2_route_cns2_v1_lit.py

WHAT THIS IS. A literature leg has no PDE to integrate, so the runner is what keeps the prose
honest (the pattern legs 175/183/189/196 established): every number and every count quoted in
writeup/novelty/leg_240.md and experiments/journal/leg_240.md is transcribed here ONCE, from
the primary source, with its line locator in a named extraction; the gate verdict is COMPUTED
from that table rather than asserted; and the arithmetic the prose leans on is re-derived.
It emits writeup/data/p2_route_cns2_v1_lit.json.

WHY THE VERDICT IS COMPUTED (lesson 90 -- a control that cannot come out differently is not a
control). The gate's YES branch escalates and parks the leg, so it must not be reachable by
prose alone and must not be UNreachable by construction. `classify()` below takes the evidence
table and returns one of

    UPGRADED_TO_ENCLOSED | NOT_UPGRADED_STILL_DOMINATED | NO_SUBSEQUENT_WORK

and `self_test()` exercises all three on perturbed copies of the evidence, so the classifier is
demonstrably able to fire the escalation branch on evidence that warranted it.

  E1  Does any located subsequent same-group work on the same (or a directly comparable)
      object carry certification APPARATUS of its own -- interval arithmetic, an enclosure,
      validated numerics, a certificate?  Measured as a term census over the full pdftotext
      extraction, not as an impression.
  E2  Is the viscous term ENCLOSED (inside the certified object) or DOMINATED (an error term
      whose smallness comes from a scaling inequality)?  Read from the authors' own words.
  E3  Was any subsequent same-group work on a comparable object located at all?

E1 and E2 must BOTH come out the right way for an upgrade. Apparatus alone is a method paper;
a viscous theorem alone is what 2208.09445 already had (leg 174's Grade B).

THE ARITHMETIC CROSS-CHECK, AND WHY IT CAN FAIL. The load-bearing claim of this leg is that
the follow-up carries the PARENT's viscous condition forward UNCHANGED. That is checked, not
asserted: BCG's (1.20), CGSS's (1.8) and the third (different-group) paper's delta_dis are
transcribed from three separate extractions in the three papers' own notation and required to
agree numerically over a gamma x r grid. A transcription slip in any one of them fails the
check. Two further published identities are re-derived from the transcription -- BCG's (1.21)
`delta_dis > 0 <=> r > 2 gamma / (gamma + 1)` and its ceiling `gamma < 1 + 2/sqrt(3)` as the
root of `r_star(gamma) = 2 gamma / (gamma + 1)` -- and either could have come out wrong.

PROVENANCE. Three PDFs were pulled from arxiv.org during this leg and extracted with
`pdftotext -layout`; `line` fields locate quotes in those extractions.  Papers/ is gitignored
on purpose.

    arXiv:2310.05325v2  md5 83b98f3ddc0ec1590c9012c7735147c1   6642 lines
    arXiv:2208.09445v2  md5 98c5b7dd6f535cdb0146c64fece771e4  10108 lines
    arXiv:2501.15701v2  md5 9ee1ea9f2de0543b84be2a2c244a5dee   4146 lines
    arXiv:2503.16813v1  md5 a811a5e630ab38cd85a0079243d42a9e    657 lines

NO NETWORK ACCESS AND NO SOLVER IMPORT at run time. solver/viscous_novelty.py is leg 197's and
is NOT read, imported or edited here.
"""

import json
import math
import os
from datetime import date

PASS_DATE = "2026-08-06"

PARENT = "arXiv:2208.09445v2"   # Buckmaster, Cao-Labora, Gomez-Serrano -- leg 174's Grade B row
FOLLOW = "arXiv:2310.05325v2"   # Cao-Labora, Gomez-Serrano, Shi, Staffilani -- THIS leg's target
NLSHYD = "arXiv:2503.16813v1"   # same group, "Euler with a certain dissipation" -- 2nd candidate
OTHERG = "arXiv:2501.15701v2"   # Shao, Wei, Wang, Zhang -- DIFFERENT group, same object: control

PDF_MD5 = {
    FOLLOW: "83b98f3ddc0ec1590c9012c7735147c1",
    PARENT: "98c5b7dd6f535cdb0146c64fece771e4",
    NLSHYD: "a811a5e630ab38cd85a0079243d42a9e",
    OTHERG: "9ee1ea9f2de0543b84be2a2c244a5dee",
}
EXTRACTION_LINES = {FOLLOW: 6642, PARENT: 10108, NLSHYD: 657, OTHERG: 4146}

# --------------------------------------------------------------------------------------
# 1. HOW THE CANDIDATE SET WAS CLOSED.  Two independent enumerations, so the set is closed by
#    construction rather than by whichever keyword query happened to fire.
# --------------------------------------------------------------------------------------

SEARCH_LOG = [
    {"kind": "arxiv-api-author-listing", "n_entries": 11, "newest": "2608.05114 (2026-08-05)",
     "query": 'http://export.arxiv.org/api/query?search_query=au:"Cao-Labora"'
              '&max_results=40&sortBy=submittedDate&sortOrder=descending',
     "note": "complete career listing, read entry by entry -- a follow-up with an unexpected "
             "title cannot be missed by a listing the way it can by a keyword search"},
    {"kind": "arxiv-api-author-listing", "n_entries": 46, "newest": "2605.18699 (2026-05-18)",
     "query": 'http://export.arxiv.org/api/query?search_query=au:"Gomez-Serrano"'
              '&max_results=60&sortBy=submittedDate&sortOrder=descending',
     "note": "one name collision noted and NOT counted: 2108.11284 is Vicente Gomez-Serrano, "
             "battery chemistry"},
    {"kind": "arxiv-api-author-listing", "n_entries": 11, "newest": "2511.22819 (2025-11-28)",
     "query": 'http://export.arxiv.org/api/query?search_query=au:"Buckmaster"'
              '&max_results=60&sortBy=submittedDate&sortOrder=descending',
     "note": "listing polluted by unrelated Buckmasters (agriculture, gaze-contingent AI). The "
             "NARROWER form au:\"Buckmaster_T\" was tried first and DISCARDED: it returned only "
             "2 entries, newest 2016, and would have hidden every paper this leg is about. "
             "Recorded because a query that silently under-returns is the failure mode."},
    {"kind": "author-maintained-page", "n_entries": 20, "newest": "2026 submissions",
     "query": "https://sites.brown.edu/jgs/papers/",
     "note": "carries journal status the arXiv listing does not (this is where "
             "2310.05325 = Cambridge J. Math. 13(4) 753-885 is confirmed as PUBLISHED); "
             "cross-checked against the arXiv listings, no entry in one and not the other"},
    {"kind": "web-search", "n_entries": 8, "newest": None,
     "query": "Buckmaster Cao-Labora Gomez-Serrano imploding Navier-Stokes viscous term "
              "interval arithmetic 2026", "note": "no same-group hit not already in the listings"},
    {"kind": "web-search", "n_entries": 9, "newest": None,
     "query": "computer-assisted proof enclosing viscous term compressible Navier-Stokes "
              "implosion follow-up", "note": "surfaced 2501.15701 -- DIFFERENT group, read anyway"},
    {"kind": "web-search", "n_entries": 10, "newest": None,
     "query": 'arXiv 2208.09445 cited by Navier-Stokes implosion viscosity "interval arithmetic" '
              "2026 new computer-assisted", "note": "no same-group hit"},
    {"kind": "web-search", "n_entries": 8, "newest": None,
     "query": "Cao-Labora Gomez-Serrano 2026 compressible Navier-Stokes self-similar profile "
              "computer assisted proof viscosity enclosed", "note": "no same-group hit"},
]

# Every subsequent same-group work, and the depth each was read at.  `same_object` is the gate's
# own scope test: the 3D compressible Navier-Stokes imploding object, or a directly comparable one.
CANDIDATES = [
    {"id": "arXiv:2310.05325", "date": "2023-10-09", "latest_version": "v2 2025-04-21",
     "authors": ["Gonzalo Cao-Labora", "Javier Gomez-Serrano", "Jia Shi", "Gigliola Staffilani"],
     "title": "Non-radial implosion for compressible Euler and Navier-Stokes in T^3 and R^3",
     "journal": "Cambridge Journal of Mathematics 13(4), 753-885",
     "group_overlap": 2, "same_object": True, "depth": "FULL_TEXT"},
    {"id": "arXiv:2301.10101", "date": "2023-01-24", "latest_version": "v1",
     "authors": ["Tristan Buckmaster", "Gonzalo Cao-Labora", "Javier Gomez-Serrano"],
     "title": "Smooth self-similar imploding profiles to 3D compressible Euler",
     "journal": "Quarterly of Applied Mathematics 81, 517-532",
     "group_overlap": 3, "same_object": False, "depth": "ABSTRACT",
     "why_not": "review/announcement OF the parent; its own object is Euler, nu = 0"},
    {"id": "arXiv:2410.04532", "date": "2024-10-06", "latest_version": "v1",
     "authors": ["Gonzalo Cao-Labora", "Javier Gomez-Serrano", "Jia Shi", "Gigliola Staffilani"],
     "title": "Non-radial implosion for the defocusing NLS in T^d and R^d",
     "journal": None, "group_overlap": 2, "same_object": False, "depth": "ABSTRACT",
     "why_not": "dispersive, no viscous term at all"},
    {"id": "arXiv:2503.16813", "date": "2025-03-21", "latest_version": "v1",
     "authors": ["Gonzalo Cao-Labora", "Javier Gomez-Serrano", "Jia Shi", "Gigliola Staffilani"],
     "title": "A note on the existence of self-similar profiles of the hydrodynamic "
              "formulation of the focusing NLS",
     "journal": "La Matematica 5(4)", "group_overlap": 2, "same_object": True,
     "depth": "FULL_TEXT",
     "why_not": "its abstract says 'compressible Euler equations with a certain dissipation', "
                "so it is IN scope on the gate's wording and was read at full text; it carries "
                "no certification apparatus of its own (see APPARATUS_CENSUS)"},
    {"id": "arXiv:2509.14185", "date": "2025-09-17", "latest_version": "v1",
     "authors": ["Yongji Wang", "et al. (22 authors incl. all three)"],
     "title": "Discovery of Unstable Singularities", "journal": None,
     "group_overlap": 3, "same_object": False, "depth": "FULL_TEXT_AT_LEGS_175_196_212",
     "why_not": "inviscid objects (3D Euler / IPM / Boussinesq); leg 196 classified all four of "
                "its 'computer-assisted' mentions and ACHIEVED = 0; the CAP manuscript is 'in "
                "preparation' (USC p.8 fn.2) and still unpublished at leg 212"},
    {"id": "arXiv:2511.22819", "date": "2025-11-28", "latest_version": "v1",
     "authors": ["Yongji Wang", "Tristan Leger", "Ching-Yao Lai", "Tristan Buckmaster"],
     "title": "Resolving Sharp Gradients of Unstable Singularities to Machine Precision",
     "journal": None, "group_overlap": 1, "same_object": False,
     "depth": "FULL_TEXT_AT_LEGS_196_212",
     "why_not": "inviscid; 0/0/0/0 apparatus terms over 27 pp (leg 196, re-verified leg 212)"},
]

# --------------------------------------------------------------------------------------
# 2. E1 -- the certification-apparatus term census, case-insensitive, over the FULL extraction.
# --------------------------------------------------------------------------------------

APPARATUS_CENSUS = {
    FOLLOW: {"interval arithmetic": 0, "computer-assisted": 0, "enclosure": 0,
             "validated numerics": 0, "certif": 0, "rigorous": 0},
    NLSHYD: {"interval arithmetic": 0, "computer-assisted": 1, "enclosure": 0,
             "validated numerics": 0, "certif": 0, "rigorous": 0},
    OTHERG: {"interval arithmetic": 0, "computer-assisted": 1, "enclosure": 0,
             "validated numerics": 0, "certif": 0, "rigorous": 0},
    # The parent, for contrast -- this is what apparatus looks like when it IS there.
    PARENT: {"interval arithmetic": 2, "computer-assisted": 34, "enclosure": None,
             "validated numerics": None, "certif": None, "rigorous": None},
}

# The two nonzero "computer-assisted" hits outside the parent, classified individually so the
# census cannot be over-read.  Neither is an apparatus the paper itself operates.
NONZERO_HITS_CLASSIFIED = [
    {"paper": NLSHYD, "line": 84, "class": "CITATION_TO_OTHERS",
     "quote": "via a computer assisted proof in the case d = p = 3 in [8] and [7]"},
    {"paper": OTHERG, "line": None, "class": "CITATION_TO_OTHERS",
     "quote": "cites 2208.09445 as [6]; establishes its own gamma = 5/3 profiles ANALYTICALLY, "
              "with 0 occurrences of 'interval arithmetic' over 4146 lines"},
]

# --------------------------------------------------------------------------------------
# 3. E2 -- the viscous-term treatment, in the authors' own words, from three papers.
#
#    This is the heart of the leg.  DOMINATED means: the viscous term is carried as an ERROR /
#    FORCING term whose smallness comes from an inequality on the self-similar scaling exponent,
#    and the CERTIFIED object is the nu = 0 system.  ENCLOSED would mean: the interval
#    arithmetic encloses a solution of an equation that itself carries the viscous term.
# --------------------------------------------------------------------------------------

VISCOUS_QUOTES = [
    {"paper": PARENT, "line": 636, "label": "BCG-error-term",
     "quote": "The last term can be treated as an error so long as",
     "reads_on": "the viscous term, introduced one line above with prefactor "
                 "e^{(2 - r + (1-r)/alpha) s}"},
    {"paper": PARENT, "line": 637, "label": "BCG-(1.20)",
     "quote": "-delta_dis = 2 - r + (1/alpha)(1 - r) < 0 ,   (1.20)"},
    {"paper": PARENT, "line": 639, "label": "BCG-(1.21)",
     "quote": "or equivalently   r > 2 gamma / (gamma + 1) ,   (1.21)"},
    {"paper": PARENT, "line": 643, "label": "BCG-gamma-ceiling",
     "quote": "Given that we intend to restrict r < r_star, by the definition of r_star given in "
              "(1.16), we conclude that we require gamma < 1 + 2/sqrt(3)"},
    {"paper": FOLLOW, "line": 220, "label": "CGSS-(1.5)",
     "quote": "d_s U = -(r-1)U - (y+U).grad U - alpha S grad S + nu C_dis e^{-delta_dis s} "
              "Delta U / S^{1/alpha}",
     "reads_on": "the viscous term is the ONLY nu-dependent term and it carries an explicit "
                 "exponentially decaying prefactor in self-similar time"},
    {"paper": FOLLOW, "line": 227, "label": "CGSS-C_dis-delta_dis",
     "quote": "C_dis = r^{1+1/alpha} / alpha^{1/alpha} ,   delta_dis = (r-1)/alpha + r - 2"},
    {"paper": FOLLOW, "line": 249, "label": "CGSS-(1.8)",
     "quote": "In the case of Navier-Stokes (nu = 1), we need to impose an extra condition on our "
              "range of parameters, namely: delta_dis = (r-1)/alpha + r - 2 > 0.   (1.8)"},
    {"paper": FOLLOW, "line": 251, "label": "CGSS-profiles-are-nu-0",
     "quote": "From [8, 51], we know that there exist radially symmetric profiles (U, S) that "
              "solve (1.5) for nu = 0, with r in the range (1.6).",
     "reads_on": "THE CERTIFIED OBJECT IS IMPORTED AND IT IS THE nu = 0 SYSTEM. [8] is the "
                 "parent 2208.09445; [51] is MRRS."},
    {"paper": FOLLOW, "line": 343, "label": "CGSS-Remark-1.5",
     "quote": "condition (1.8) guarantees that delta_dis > 0, hence the term "
              "nu C_dis e^{-delta_dis s} Delta U / S^{1/alpha} in (1.5) has an exponential decay, "
              "which is crucial in the proof of stability. If nu = 0, this term vanishes and thus "
              "the condition is not needed. The proof is analogous to the Navier-Stokes one, "
              "except that one does not need to bound the dissipation term when doing energy "
              "estimates.",
     "reads_on": "the authors' own statement of the mechanism, and of the fact that the Euler "
                 "and Navier-Stokes proofs differ ONLY by bounding this one decaying term"},
    {"paper": FOLLOW, "line": 2363, "label": "CGSS-bootstrap-cost",
     "quote": "delta_g << delta_dis is used in Lemmas 3.11 and 3.12 in order to control the term "
              "F_dis (1.15). Because F_dis has decay not faster than e^{-delta_dis s}, our "
              "bootstrap estimate can only have a lower decay.",
     "reads_on": "the viscous term is an entry in the FORCING vector F of the perturbation "
                 "equation (1.15) -- the textbook shape of DOMINATED"},
    {"paper": OTHERG, "line": 246, "label": "SWWZ-same-form",
     "quote": "d_s U = -(r-1)U - (z+U).grad U - (1/l) S grad S + nu C_dis e^{-delta_dis s} Delta U"},
    {"paper": OTHERG, "line": 252, "label": "SWWZ-delta_dis",
     "quote": "C_dis := r^{1+l} l^l ,   delta_dis := l(r-1) + r - 2,   with l = 2/(gamma-1)"},
    {"paper": OTHERG, "line": 269, "label": "SWWZ-(1.4)",
     "quote": "delta_dis = l(r-1) + r - 2 > 0   (1.4)"},
]

# The one definition everything else is measured against, quoted rather than inferred.
ALPHA_DEF = {"paper": FOLLOW, "line": 169,
             "quote": "First of all, let us define alpha = (gamma-1)/2 and the rescaled sound "
                      "speed sigma = (1/alpha) rho^alpha"}

# --------------------------------------------------------------------------------------
# 4. THE ARITHMETIC.  Re-derived from the transcription above; every one of these can fail.
# --------------------------------------------------------------------------------------


def alpha_of(gamma):
    """alpha = (gamma - 1)/2, quoted at ALPHA_DEF."""
    return (gamma - 1.0) / 2.0


def delta_dis_bcg(gamma, r):
    """BCG (1.20), read as delta_dis = -(2 - r + (1-r)/alpha)."""
    a = alpha_of(gamma)
    return -(2.0 - r + (1.0 - r) / a)


def delta_dis_cgss(gamma, r):
    """CGSS (1.8) / line 227, in CGSS's own notation."""
    a = alpha_of(gamma)
    return (r - 1.0) / a + r - 2.0


def delta_dis_swwz(gamma, r):
    """SWWZ, in THEIR notation: delta_dis = l(r-1) + r - 2 with l = 2/(gamma-1)."""
    ell = 2.0 / (gamma - 1.0)
    return ell * (r - 1.0) + r - 2.0


def r_star(gamma):
    """The upper end of the admissible self-similar exponent, BCG (1.16) = CGSS (1.6)."""
    if gamma < 5.0 / 3.0:
        return 1.0 + 2.0 / (1.0 + math.sqrt(2.0 / (gamma - 1.0))) ** 2
    return (3.0 * gamma - 1.0) / (2.0 + math.sqrt(3.0) * (gamma - 1.0))


def r_dis_threshold(gamma):
    """BCG (1.21): delta_dis > 0 <=> r > 2 gamma / (gamma + 1)."""
    return 2.0 * gamma / (gamma + 1.0)


def viscous_window(gamma):
    """The r-interval on which a VISCOUS theorem is available at all: (threshold, r_star)."""
    lo, hi = r_dis_threshold(gamma), r_star(gamma)
    return {"lo": lo, "hi": hi, "width": max(0.0, hi - lo), "nonempty": hi > lo,
            "delta_dis_max": max(0.0, delta_dis_cgss(gamma, hi))}


def check_arithmetic():
    """Everything the prose leans on, re-derived.  Returns a dict of named checks."""
    out = {}

    # (a) The three papers' delta_dis, in three different notations, are the SAME function.
    #     A transcription slip in any one of them fails this.
    worst = 0.0
    for i in range(1, 40):
        gamma = 1.05 + i * 0.05
        for j in range(1, 20):
            r = 1.0 + j * 0.05
            v = (delta_dis_bcg(gamma, r), delta_dis_cgss(gamma, r), delta_dis_swwz(gamma, r))
            worst = max(worst, max(v) - min(v))
    out["delta_dis_agreement_max_abs_dev"] = worst
    out["delta_dis_identical_across_three_papers"] = worst < 1e-12

    # (b) BCG (1.21): delta_dis > 0 <=> r > 2 gamma/(gamma+1).  Checked at the threshold and
    #     on both sides of it.
    ok, dev = True, 0.0
    for i in range(1, 40):
        gamma = 1.05 + i * 0.05
        rt = r_dis_threshold(gamma)
        dev = max(dev, abs(delta_dis_cgss(gamma, rt)))
        ok &= delta_dis_cgss(gamma, rt * 1.01) > 0.0 > delta_dis_cgss(gamma, rt * 0.99)
    out["threshold_is_a_root_max_abs_residual"] = dev
    out["sign_change_at_threshold_everywhere"] = bool(ok and dev < 1e-12)

    # (c) The two branches of r_star agree at gamma = 5/3, which is what CGSS asserts in words
    #     ("Note that both expressions agree for gamma = 5/3") -- so this check is a direct test
    #     of whether the formula was transcribed correctly off a mangled PDF extraction.
    g = 5.0 / 3.0
    lo_branch = 1.0 + 2.0 / (1.0 + math.sqrt(2.0 / (g - 1.0))) ** 2
    hi_branch = (3.0 * g - 1.0) / (2.0 + math.sqrt(3.0) * (g - 1.0))
    out["r_star_branches_at_gamma_5_3"] = {"low_branch": lo_branch, "high_branch": hi_branch,
                                           "abs_dev": abs(lo_branch - hi_branch)}
    out["r_star_branches_agree"] = abs(lo_branch - hi_branch) < 1e-12

    # (d) CGSS (1.7): r < sqrt(3) for all gamma, as the gamma -> infinity limit of r_star.
    out["r_star_limit_large_gamma"] = r_star(1e7)
    out["r_star_limit_is_sqrt3"] = abs(r_star(1e7) - math.sqrt(3.0)) < 1e-5

    # (e) BCG's ceiling gamma < 1 + 2/sqrt(3) as the root of r_star(gamma) = 2 gamma/(gamma+1),
    #     found by bisection rather than quoted.
    f = lambda x: r_star(x) - r_dis_threshold(x)
    a, b = 1.7, 3.0
    for _ in range(200):
        m = 0.5 * (a + b)
        if f(a) * f(m) <= 0.0:
            b = m
        else:
            a = m
    root = 0.5 * (a + b)
    out["gamma_ceiling_bisected"] = root
    out["gamma_ceiling_published"] = 1.0 + 2.0 / math.sqrt(3.0)
    out["gamma_ceiling_matches"] = abs(root - (1.0 + 2.0 / math.sqrt(3.0))) < 1e-9

    # (f) The magnitudes the report quotes: how much room the DOMINATION inequality actually has
    #     on the parent's own case gamma = 7/5, and on the degenerate monatomic case gamma = 5/3.
    out["window_gamma_7_5"] = viscous_window(1.4)
    out["window_gamma_5_3"] = viscous_window(5.0 / 3.0)
    # For gamma = 7/5, delta_dis collapses to a line: (r-1)/0.2 + r - 2 = 6r - 7.
    out["delta_dis_gamma_7_5_is_6r_minus_7"] = all(
        abs(delta_dis_cgss(1.4, 1.0 + k * 0.01) - (6.0 * (1.0 + k * 0.01) - 7.0)) < 1e-12
        for k in range(0, 30))
    return out


# --------------------------------------------------------------------------------------
# 5. THE CLASSIFIER.  Computed, and demonstrably able to fire the escalation branch.
# --------------------------------------------------------------------------------------

UPGRADED = "UPGRADED_TO_ENCLOSED"
NOT_UPGRADED = "NOT_UPGRADED_STILL_DOMINATED"
NONE_FOUND = "NO_SUBSEQUENT_WORK"


def classify(evidence):
    """evidence: {'candidates_on_object': int, 'apparatus_terms': int,
                  'viscous_treatment': 'DOMINATED'|'ENCLOSED',
                  'certified_object_carries_viscosity': bool}

    An UPGRADE requires all three: subsequent work on the object, certification apparatus of
    its own, and a certified object that actually carries the viscous term.
    """
    if evidence["candidates_on_object"] == 0:
        return NONE_FOUND
    if (evidence["apparatus_terms"] > 0
            and evidence["viscous_treatment"] == "ENCLOSED"
            and evidence["certified_object_carries_viscosity"]):
        return UPGRADED
    return NOT_UPGRADED


def apparatus_operated_by(paper_id):
    """Total apparatus-term occurrences MINUS the ones classified as citations to others.

    An apparatus term the paper spends on someone else's proof is not apparatus the paper
    operates, and counting it would manufacture a hit out of a bibliography.
    """
    total = sum(v for v in APPARATUS_CENSUS[paper_id].values() if v is not None)
    cited = sum(1 for h in NONZERO_HITS_CLASSIFIED
                if h["paper"] == paper_id and h["class"] == "CITATION_TO_OTHERS")
    return total - cited


EVIDENCE = {
    "candidates_on_object": sum(1 for c in CANDIDATES if c["same_object"]),
    # summed over the candidates that are ON the object -- the two read at full text this leg
    "apparatus_terms": apparatus_operated_by(FOLLOW) + apparatus_operated_by(NLSHYD),
    "viscous_treatment": "DOMINATED",
    "certified_object_carries_viscosity": False,
}


def self_test():
    """Lesson 90: show the classifier can return each of its three values."""
    up = dict(EVIDENCE, apparatus_terms=7, viscous_treatment="ENCLOSED",
              certified_object_carries_viscosity=True)
    none = dict(EVIDENCE, candidates_on_object=0)
    results = {"as_measured": classify(EVIDENCE),
               "if_apparatus_and_enclosed": classify(up),
               "if_nothing_located": classify(none),
               "if_apparatus_but_still_dominated": classify(dict(EVIDENCE, apparatus_terms=7))}
    assert results["as_measured"] == NOT_UPGRADED
    assert results["if_apparatus_and_enclosed"] == UPGRADED
    assert results["if_nothing_located"] == NONE_FOUND
    assert results["if_apparatus_but_still_dominated"] == NOT_UPGRADED
    assert len(set(results.values())) == 3
    return results


# --------------------------------------------------------------------------------------
# 6. THE GATE, in its pre-committed wording.
# --------------------------------------------------------------------------------------

GATE_QUESTION = (
    "Does arXiv:2208.09445's author group have subsequent published work that upgrades the "
    "viscous-term treatment from DOMINATED to ENCLOSED for this same 3D compressible "
    "Navier-Stokes object (or a directly comparable one), achieving a genuine Grade-A/"
    "fluid=True certificate?")

# Lesson 91: the negative must name the realization it holds in.
REALIZATION = (
    "The negative holds in the following named realization, and nowhere wider: the enumerated "
    "publication record of the three authors of arXiv:2208.09445 (Buckmaster, Cao-Labora, "
    "Gomez-Serrano) as listed by the arXiv API author queries and the author-maintained page "
    "https://sites.brown.edu/jgs/papers/ as of " + PASS_DATE + "; the two entries of that record "
    "whose object is a compressible-fluid system carrying a dissipative term (arXiv:2310.05325 "
    "and arXiv:2503.16813) read at full text in the pdftotext -layout extractions pinned in "
    "PDF_MD5; and the term census run case-insensitively over those complete extractions. It is "
    "NOT a statement about the wider literature, about unpublished work, or about the group's "
    "in-preparation CAP manuscript for the unstable-singularities thread (which is inviscid).")


def build():
    checks = check_arithmetic()
    verdict = classify(EVIDENCE)
    return {
        "leg": 240, "route": "CNS2", "role": "LIT", "date": PASS_DATE,
        "gate_question": GATE_QUESTION,
        "gate_answer": "NO",
        "gate_verdict_code": verdict,
        "realization_the_negative_holds_in": REALIZATION,
        "parent_paper": {
            "id": PARENT, "authors": ["Tristan Buckmaster", "Gonzalo Cao-Labora",
                                      "Javier Gomez-Serrano"],
            "journal": "Forum of Mathematics Pi 13 (2025) e6",
            "leg_174_grade": "B", "leg_174_fluid": True,
            "leg_174_reason": "the theorem is about compressible Navier-Stokes and computer "
                              "assistance is essential, but the ENCLOSED object is the inviscid "
                              "Euler ODE; the viscous term is DOMINATED, not enclosed"},
        "search_log": SEARCH_LOG,
        "candidates": CANDIDATES,
        "n_candidates_same_group": len(CANDIDATES),
        "n_candidates_on_object": EVIDENCE["candidates_on_object"],
        "n_read_full_text_this_leg": sum(1 for c in CANDIDATES if c["depth"] == "FULL_TEXT"),
        "different_group_control": {
            "id": OTHERG, "authors": ["Feng Shao", "Dongyi Wei", "Shumao Wang", "Zhifei Zhang"],
            "title": "Blow-up of the 3-D compressible Navier-Stokes equations for monatomic gases",
            "why_it_is_here": "out of the gate's scope (different group) but it is the sharpest "
                              "available control on the MECHANISM: an independent group, on the "
                              "same object, at the degenerate gamma = 5/3, reaches the viscous "
                              "theorem by the IDENTICAL delta_dis domination inequality -- and "
                              "with 0 interval arithmetic, having replaced the computer-assisted "
                              "profile step by an analytic one. The domination is therefore not "
                              "an artifact of the parent's computer assistance; it is how this "
                              "literature transfers an Euler profile to Navier-Stokes."},
        "apparatus_census": APPARATUS_CENSUS,
        "nonzero_apparatus_hits_classified": NONZERO_HITS_CLASSIFIED,
        "extraction_lines": EXTRACTION_LINES,
        "pdf_md5": PDF_MD5,
        "alpha_definition": ALPHA_DEF,
        "viscous_quotes": VISCOUS_QUOTES,
        "arithmetic_checks": checks,
        "reading_note_gamma_5_3": (
            "A misreading this leg caught in itself and is recording so nobody re-makes it: "
            "gamma = 5/3 is NOT excluded because the viscous window is empty. The runner "
            "computes that window as NONEMPTY -- r in (1.2500000, 1.2679492), width 1.79e-02. "
            "CGSS exclude gamma = 5/3 for a different reason: the PROFILES they import are "
            "MRRS's 'almost every gamma' result, from which gamma = 5/3 (the degenerate case) "
            "is excluded, while the parent's computer-assisted profile covers gamma = 7/5. "
            "Which is why the different-group control matters: Shao-Wei-Wang-Zhang supply the "
            "missing gamma = 5/3 profiles ANALYTICALLY, closing that hole without any "
            "certificate at all."),
        "classifier_self_test": self_test(),
        "headline": (
            "NOT UPGRADED. The one subsequent same-group work on the 3D compressible "
            "Navier-Stokes object itself -- Cao-Labora, Gomez-Serrano, Shi, Staffilani, "
            "arXiv:2310.05325, Cambridge J. Math. 13(4) 753-885 -- carries ZERO certification "
            "apparatus of its own (0/0/0/0/0/0 over a 6642-line full-text extraction), IMPORTS "
            "its certified profile from the parent and from MRRS as the nu = 0 system (1.9), and "
            "treats the viscous term exactly as the parent did: as a forcing term with prefactor "
            "e^{-delta_dis s}, admissible only under the SAME scalar inequality "
            "delta_dis = (r-1)/alpha + r - 2 > 0 the parent wrote as (1.20)/(1.21) 14 months "
            "earlier -- the two transcriptions agree to 1.78e-15 max absolute deviation over a "
            "39 x 19 (gamma, r) grid. On the parent's own gamma = 7/5 the entire domination "
            "margin is delta_dis <= 0.1458980 on an r-window of width 2.43e-02. The "
            "Grade-A/fluid=True cell leg 174 found empty is still empty."),
    }


def main():
    payload = build()
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "writeup", "data", "p2_route_cns2_v1_lit.json")
    with open(out, "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)
        fh.write("\n")

    c = payload["arithmetic_checks"]
    print("Leg 240 (Route-CNS2) -- literature pass, %s" % payload["date"])
    print()
    print("GATE: %s" % payload["gate_answer"])
    print("  verdict code            %s" % payload["gate_verdict_code"])
    print("  same-group works found  %d (on the object: %d; full-text this leg: %d)"
          % (payload["n_candidates_same_group"], payload["n_candidates_on_object"],
             payload["n_read_full_text_this_leg"]))
    print()
    print("APPARATUS CENSUS (case-insensitive, full extraction)")
    for pid in (FOLLOW, NLSHYD, OTHERG, PARENT):
        row = APPARATUS_CENSUS[pid]
        print("  %-18s %s lines   %s" % (pid, EXTRACTION_LINES[pid],
              ", ".join("%s=%s" % (k, v) for k, v in row.items())))
    print()
    print("ARITHMETIC")
    print("  delta_dis identical across 3 papers   %s  (max abs dev %.3e over 39x19 grid)"
          % (c["delta_dis_identical_across_three_papers"], c["delta_dis_agreement_max_abs_dev"]))
    print("  (1.21) threshold is a root of it      %s  (max abs residual %.3e)"
          % (c["sign_change_at_threshold_everywhere"], c["threshold_is_a_root_max_abs_residual"]))
    print("  r_star branches agree at gamma=5/3    %s  (%.10f vs %.10f)"
          % (c["r_star_branches_agree"], c["r_star_branches_at_gamma_5_3"]["low_branch"],
             c["r_star_branches_at_gamma_5_3"]["high_branch"]))
    print("  r_star -> sqrt(3) as gamma -> inf     %s  (%.8f)"
          % (c["r_star_limit_is_sqrt3"], c["r_star_limit_large_gamma"]))
    print("  gamma ceiling 1+2/sqrt(3) bisected    %s  (%.12f vs published %.12f)"
          % (c["gamma_ceiling_matches"], c["gamma_ceiling_bisected"],
             c["gamma_ceiling_published"]))
    w = c["window_gamma_7_5"]
    print("  viscous window gamma=7/5              r in (%.7f, %.7f), width %.7e"
          % (w["lo"], w["hi"], w["width"]))
    print("      max delta_dis over that window    %.7f   <- the ENTIRE domination margin"
          % w["delta_dis_max"])
    w2 = c["window_gamma_5_3"]
    print("  viscous window gamma=5/3              r in (%.7f, %.7f), width %.7e"
          % (w2["lo"], w2["hi"], w2["width"]))
    print()
    print("CLASSIFIER SELF-TEST (lesson 90)")
    for k, v in payload["classifier_self_test"].items():
        print("  %-34s %s" % (k, v))
    print()
    print(payload["headline"])
    print()
    print("wrote %s" % out)


if __name__ == "__main__":
    main()
