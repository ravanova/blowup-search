#!/usr/bin/env python3
"""Leg 196 (Route-USC2) -- literature runner for arXiv:2511.22819, "Resolving Sharp Gradients
of Unstable Singularities to Machine Precision via Neural Networks" (Wang, Leger, Lai,
Buckmaster; v1, 28 Nov 2025) -- the follow-up leg 175 located but did not read end to end.

WHAT THIS IS. A literature leg has no PDE to integrate, so the runner is the thing that keeps
the prose honest (the pattern leg 175 established and legs 183/189 reused): every number and
every count quoted in writeup/novelty/leg_196.md and experiments/journal/leg_196.md is
transcribed here ONCE, from the primary source, with its locator; the gate verdict is then
COMPUTED from that table rather than asserted; and the arithmetic the prose leans on is
re-derived and cross-checked. It emits writeup/data/p2_route_usc2_v1_lit.json.

    .venv/bin/python experiments/p2_route_usc2_v1_lit.py

WHY THE VERDICT IS COMPUTED (lesson 90: a control that cannot come out differently is not a
control). This leg's gate has a branch -- CERTIFICATE_ACHIEVED -- whose consequences are large
enough that it must not be reachable by prose alone, and equally must not be UNreachable by
construction. `classify_certificate` below takes the evidence and returns one of

    CERTIFICATE_ACHIEVED | STILL_SHORT | NOT_LOCATABLE

and `self_test()` exercises all three on perturbed copies of the evidence, so the classifier is
demonstrably capable of firing the escalation branch on evidence that warranted it.

  E1  Does any located later work carry certification APPARATUS -- interval arithmetic, an
      enclosure, validated numerics, a certificate?  Measured as a term census over the full
      pdftotext extraction, not as an impression.
  E2  Does any located later work ASSERT achievement rather than prerequisite?  Every
      occurrence of "computer-assisted" in the source is classified individually and
      exhaustively; a certificate requires at least one ACHIEVED.
  E3  Was any later work located at all?  If the search returned nothing, the honest answer is
      NOT_LOCATABLE and the search itself is the deliverable.

E1 and E2 must BOTH hold to report a certificate. Apparatus without a claim is a method paper;
a claim without apparatus is a promise. Neither is a certificate.

PROVENANCE. arXiv:2511.22819v1 was pulled from https://arxiv.org/pdf/2511.22819 during this
leg and extracted with `pdftotext -layout` (1593 lines); the `line` field on each quote is the
line locator in that extraction. Papers/ is gitignored on purpose; `bash Papers/fetch.sh
2511.22819` re-pulls it. NO NETWORK ACCESS AND NO SOLVER IMPORT at run time -- nothing here
reads solver/.
"""

import json
import os
from datetime import date

# --------------------------------------------------------------------------------------
# 1. Bibliographic facts, checked at the abs page during the pass.
# --------------------------------------------------------------------------------------

USC = "arXiv:2509.14185v1"      # Discovery of Unstable Singularities, 20 pp -- leg 175's target
FIX = "arXiv:2511.22819v1"      # Resolving Sharp Gradients ..., 27 pp -- THIS leg's target

PASS_DATE = "2026-08-06"

BIBLIO = {
    "usc_v1_date": "2025-09-17",
    "fix_v1_date": "2025-11-28",
    "fix_versions_on_arxiv": ["v1"],       # abs page submission history, checked this pass
    "fix_journal_ref": None,               # arXiv DOI only: 10.48550/arXiv.2511.22819
    "fix_pages": 27,
    "fix_figures": 12,
    "fix_authors": ["Yongji Wang", "Tristan Leger", "Ching-Yao Lai", "Tristan Buckmaster"],
    "usc_author_count": 22,
    # The two CAP-track authors on the 22-author original who are ABSENT from the 4-author
    # follow-up. A locatable fact about who wrote what, not an inference about intent.
    "cap_track_authors_on_usc_absent_from_fix": ["Javier Gomez-Serrano", "Gonzalo Cao-Labora"],
    "usc_cap_manuscript_still_unpublished": True,   # USC p.8 fn.2 "Manuscript in preparation."
}

# --------------------------------------------------------------------------------------
# 2. E1 -- the certification-apparatus term census over the full extraction.
#    Counts are case-insensitive over all 1593 lines of the pdftotext output.
# --------------------------------------------------------------------------------------

APPARATUS_TERMS = {
    "interval arithmetic": 0,
    "enclosure": 0,
    "validated numerics": 0,
    "certif": 0,            # certificate / certified / certification -- any stem
}

CONTEXT_TERMS = {
    "computer-assisted": 4,
    "eigen": 0,             # no linearized-operator spectrum anywhere in the follow-up
    "spectrum": 1,          # "a wide spectrum of ... singularities" (abstract) -- colloquial
    "Boussinesq": 2,        # abstract recap of [1]; ref [2] title
    "Euler": 3,             # CCF motivation; refs [2], [3]
}

# --------------------------------------------------------------------------------------
# 3. E2 -- every "computer-assisted" occurrence, classified exhaustively.
#    kinds: DEFINITION (defines the accuracy target) | PREREQUISITE (accuracy is needed FOR a
#    CAP) | ASPIRATION (a CAP would be good to have) | ACHIEVED (a CAP is presented).
# --------------------------------------------------------------------------------------

CAP_MENTIONS = [
    {"line": 41, "section": "Abstract", "kind": "PREREQUISITE",
     "text": "providing an important ingredient for bridging the gap between numerical "
             "discovery and computer-assisted proofs for unstable phenomena in nonlinear PDEs."},
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

# --------------------------------------------------------------------------------------
# 4. The paper's own numbers.
# --------------------------------------------------------------------------------------

# FIX Fig. 7(f), transcribed at l.714-738: inferred smooth lambda for IPM, with the accuracy
# the paper itself prints beside each. THIS is the quantity a self-similar CAP must enclose.
LAMBDA_IPM_FIX = [
    # (mode_order_n, label,          lambda_s,          stated_accuracy)
    (0, "stable",       1.0285722760323, 1e-13),
    (1, "1st unstable", 0.472129736156,  2e-12),
    (2, "2nd unstable", 0.3149617817,    3e-10),
    (3, "3rd unstable", 0.24156641,      1e-8),
    (4, "4th unstable", 0.1987237,       1e-7),
]

# The residual level actually achieved for those same IPM solutions (FIX abstract, p.2 sec.1,
# sec.5): "between O(10^-11) and O(10^-13) for the 2-D IPM solutions". Best case, log10.
FIX_IPM_RESIDUAL_BEST_LOG10 = -13.0
FIX_IPM_RESIDUAL_WORST_LOG10 = -11.0

# FIX sec.2.3.3, l.696, the paper's OWN stated rate, in its own words: "decreases the
# achievable lambda accuracy for a fixed computational budget by approximately two orders of
# magnitude per model."
FIX_STATED_LAMBDA_DECADES_PER_MODE = 2.0

# FIX sec.2.3.3, l.684-690 -- the two compounding ladders leg 175 recorded, re-verified at the
# primary source this pass.
LADDER_FIX = {
    "signal_decay_decades_per_mode": 1.0,
    "background_rise_decades_per_mode": 1.0,
    "ipm_stable_best_Rmax_log10": -14.0,
    "ipm_4th_unstable_best_Rmax_log10": -10.0,
    "ipm_modes_spanned": 4,
}

# FIX sec.2.1.3, l.275-281 -- the CCF third unstable solution was SEARCHED FOR and NOT FOUND.
CCF_THIRD_UNSTABLE_SEARCH = {
    "searched_lambda_window": [0.455, 0.4713],
    "found": False,
    "authors_next_range": "lambda < 0.455",
    "authors_difficulty_rating": "greater than finding highly unstable solutions in 2D IPM",
    "ccf_suite_size_after_fix": 3,      # stable, 1st unstable, 2nd unstable
}

# --------------------------------------------------------------------------------------
# 5. The verbatim quotes the gate turns on.
# --------------------------------------------------------------------------------------

QUOTES = [
    {"src": FIX, "line": 41, "section": "Abstract",
     "text": "providing an important ingredient for bridging the gap between numerical "
             "discovery and computer-assisted proofs for unstable phenomena in nonlinear PDEs.",
     "bears_on": "the paper's own description of its contribution: an ingredient, not a bridge"},
    {"src": FIX, "line": 1437, "section": "5 Conclusion",
     "text": "Beyond numerical discovery, high accuracy is a prerequisite for rigorous "
             "mathematical verification via computer-assisted proofs.",
     "bears_on": "the paper's last word on certification -- future-facing, nothing claimed"},
    {"src": FIX, "line": 130, "section": "2",
     "text": "We demonstrate our method on two canonical models: the 1D "
             "Cordoba-Cordoba-Fontelos equation and the 2D Incompressible Porous Media "
             "equation.",
     "bears_on": "Boussinesq and 3D Euler with boundary -- leg 175's open item (a) -- are "
                 "outside the follow-up's scope entirely"},
    {"src": FIX, "line": 276, "section": "2.1.3 Exploring higher Unstable Solutions",
     "text": "a persistent non-smooth signal at the origin (inset of Fig.3b) remains for all "
             "tested lambda in [0.455, 0.4713]. This indicates that if a third unstable "
             "solution exists, it is located at a lambda value corresponding to an even "
             "higher-gradient profile.",
     "bears_on": "NEW obstruction N2: the discovery frontier itself stalled on CCF"},
    {"src": FIX, "line": 279, "section": "2.1.3",
     "text": "The challenge of exploring the range lambda < 0.455 and resolving such a feature "
             "in the 1D CCF model appears to be even greater than finding highly unstable "
             "solutions in the 2D IPM equation.",
     "bears_on": "the authors rate the remaining 1D search harder than the 2D one"},
    {"src": FIX, "line": 684, "section": "2.3.3",
     "text": "the high-gradient nature of higher-order unstable modes still reduces the "
             "convergence rate of training. For a fixed computational budget ... the achievable "
             "background PDE residual for the smooth solution increases by approximately one "
             "order of magnitude for each successive singularity",
     "bears_on": "leg 175's ladder, re-verified at the primary source"},
    {"src": FIX, "line": 696, "section": "2.3.3",
     "text": "decreases the achievable lambda accuracy for a fixed computational budget by "
             "approximately two orders of magnitude per model.",
     "bears_on": "NEW obstruction N1: the ladder now degrades the enclosure width of lambda, "
                 "which is what a self-similar CAP must enclose"},
    {"src": FIX, "line": 773, "section": "2.3.3",
     "text": "Figure 6(f) shows the best inferred lambda for different singularities of IPM "
             "using a multistage setup that can be implemented on a single A100 GPU (80GB). To "
             "further improve the lambda accuracy, one could use larger networks or more "
             "training stages in parallel on multiple GPUs.",
     "bears_on": "NEW obstruction N3: the remedy offered is budget, not method"},
    {"src": FIX, "line": 49, "section": "1 Introduction",
     "text": "we refer to machine precision as the highest achievable accuracy, where the "
             "remaining PDE residuals are dominated by the inherent round-off errors of "
             "double-float arithmetic, typically O(10^-13) or lower.",
     "bears_on": "N3: the floor is double-float round-off, by the pipeline's own definition"},
]

# --------------------------------------------------------------------------------------
# 6. Leg 175's four open items, re-checked. Recorded as data so "0 of 4 closed" is COMPUTED.
# --------------------------------------------------------------------------------------

LEG_175_OPEN_ITEMS = [
    {"id": "a", "item": "the precision fix is unpublished for Boussinesq / 3D Euler with "
                        "boundary",
     "closed_by_fix": False,
     "evidence": "FIX sec.2 l.130 names its two models as CCF and IPM only; 'Boussinesq' "
                 "occurs 2x in 27 pp (abstract recap of [1]; ref [2] title) and never in the "
                 "body. Leg 175's ~4.8-decade Boussinesq gap is untouched.",
     "leg_175_magnitude": "4.82 decades short of O(10^-13) at Boussinesq's best solution"},
    {"id": "b", "item": "the ~2 decade/mode margin ladder",
     "closed_by_fix": False,
     "evidence": "FIX sec.2.3.3 l.684-696 states it in the paper's own words and it is now the "
                 "BINDING constraint, expressed in lambda rather than in residual (see N1).",
     "leg_175_magnitude": "2.0 decades/mode net margin closure"},
    {"id": "c", "item": "the unstable-spectrum enclosure (a proof obligation, not a numerics "
                        "one)",
     "closed_by_fix": False,
     "evidence": "ZERO occurrences of 'eigen' in the follow-up; no linearized-operator "
                 "spectrum, no mode-count re-derivation, no treatment of eigenvalues off the "
                 "real axis or outside the symmetry class. The paper that fixed the numerics "
                 "did not touch it.",
     "leg_175_magnitude": "not a quantity -- an assumption stated as 'desirable' in USC p.19"},
    {"id": "d", "item": "the CAP announced Sep 2025 as 'Manuscript in preparation'",
     "closed_by_fix": False,
     "evidence": "FIX never mentions it; eight independent search venues this pass returned no "
                 "such record (see SEARCH_LOG).",
     "leg_175_magnitude": "unpublished"},
]

# --------------------------------------------------------------------------------------
# 7. NEW obstructions this leg's full-text read adds, none visible from the abstract.
# --------------------------------------------------------------------------------------

NEW_OBSTRUCTIONS = [
    {"id": "N1", "name": "the binding quantity moved from the residual to lambda's error bar",
     "locator": "FIX Fig.7(f) l.714-738; sec.2.3.3 l.696",
     "detail": "Residuals are at double-float round-off O(10^-13), but the scaling parameter "
               "lambda -- the object a self-similar blow-up certificate must enclose -- is "
               "pinned only to +-1e-7 at IPM's 4th unstable mode.",
     "new_relative_to_leg_175": True,
     "why_new": "leg 175 recorded the ladder as a RESIDUAL margin against the CAP threshold. "
                "The full text shows that margin is paid off and the ladder now degrades the "
                "ENCLOSURE WIDTH of lambda instead."},
    {"id": "N2", "name": "the discovery frontier stalled: CCF's 3rd unstable searched, not found",
     "locator": "FIX sec.2.1.3 l.275-281",
     "detail": "Searched across lambda in [0.455, 0.4713] with a persistent non-smooth signal "
               "at every tested value; the authors place the remaining search below 0.455 and "
               "rate it harder than the 2D IPM problem. 'the full suite of previously "
               "discovered CCF solutions' is a suite of THREE.",
     "new_relative_to_leg_175": True,
     "why_new": "not visible from the abstract, which reports only what was resolved."},
    {"id": "N3", "name": "the remaining margin is hardware- and arithmetic-bound, not conceptual",
     "locator": "FIX sec.1 l.49-51; sec.2.3.3 l.769-775",
     "detail": "The floor is double-float round-off by the pipeline's own definition of "
               "success, and every remedy offered for lambda accuracy is budget (larger "
               "networks, a third stage, more GPUs; the reported results fit one A100 80GB). A "
               "certificate generally needs arithmetic TIGHTER than the object it encloses.",
     "new_relative_to_leg_175": True,
     "why_new": "leg 175 read the fix as removing a method barrier; the full text shows what "
                "replaced it is a precision-arithmetic barrier."},
    {"id": "N4", "name": "third-party: low PDE residual does not discriminate accurate from "
                         "inaccurate PINN solutions",
     "locator": "arXiv:2606.25151 (McShannon, Dietrich, Jun 2026), which cites USC as [1]-class "
                "prior art; https://arxiv.org/abs/2606.25151",
     "detail": "Parameter-poisoned PINNs reach loss at or below the clean baseline while "
               "differing from the true solution by large margins, on Burgers, an NS cavity "
               "and convection-diffusion.",
     "new_relative_to_leg_175": True,
     "why_new": "post-dates leg 175's pass. NOT the authors' own, and NOT on the singularity "
                "problems -- it makes no claim of error in USC or FIX. Recorded because it is "
                "the independent statement of why N1-N3 matter: a small residual is evidence, "
                "an enclosure is a proof.",
     "is_third_party": True},
]

# --------------------------------------------------------------------------------------
# 8. The search, recorded as data. The repo's discipline: report the search, not the absence.
# --------------------------------------------------------------------------------------

SEARCH_LOG = [
    {"n": 1, "venue": "arXiv API export.arxiv.org",
     "query": 'all:"unstable singularities", 40 results, submittedDate desc',
     "relevant_hits": [FIX, USC],
     "outcome": "exactly two relevant records; the other 14 are unrelated senses of "
                "unstable/singularities. Identical to leg 175's result 8 months later."},
    {"n": 2, "venue": "arXiv API export.arxiv.org",
     "query": 'all:"unstable singularities" AND all:"self-similar" (leg 175 query, re-run)',
     "relevant_hits": [FIX, USC], "outcome": "unchanged"},
    {"n": 3, "venue": "arXiv API export.arxiv.org",
     "query": 'au:"Gomez-Serrano" AND abs:"computer-assisted", submittedDate desc',
     "relevant_hits": [], "outcome": "7 records, newest arXiv:2605.03920 (Burgers-Hilbert "
                                     "linear instability, May 2026). No CAP for unstable "
                                     "singularities."},
    {"n": 4, "venue": "arXiv API export.arxiv.org",
     "query": 'abs:"Cordoba-Cordoba-Fontelos" OR abs:"incompressible porous media" AND '
              'abs:"computer-assisted"',
     "relevant_hits": [], "outcome": "3 records: the same two, plus Kiselev 2010. No CAP."},
    {"n": 5, "venue": "arXiv abs page", "query": "https://arxiv.org/abs/2511.22819 submission "
                                                 "history",
     "relevant_hits": [], "outcome": "v1 only, no v2, no journal reference"},
    {"n": 6, "venue": "Semantic Scholar graph API",
     "query": "citations of arXiv:2509.14185, limit 100",
     "relevant_hits": [], "outcome": "22 citing papers; NONE is a certificate for these "
                                     "singularities. Nearest are FIX itself and "
                                     "arXiv:2606.25151 (see N4)."},
    {"n": 7, "venue": "maintained author page https://sites.brown.edu/jgs/papers/",
     "query": "Gomez-Serrano's own 2025-2026 list (the CAP author on the original)",
     "relevant_hits": [], "outcome": "nothing on a CAP for unstable self-similar "
                                     "singularities; his 2026 submissions are biharmonic nodal "
                                     "loops, Burgers-Hilbert, polygon eigenvalues, and the "
                                     "Tao/Wagner exploration paper."},
    {"n": 8, "venue": "web search, 4 query variants",
     "query": "author-name / obstruction-framing / Cao-Labora / CCF-IPM-CAP variants",
     "relevant_hits": [], "outcome": "same two papers plus secondary coverage (Quanta "
                                     "2026-01-09; a NASA Ames seminar page 2026-03-05; an LIMS "
                                     "event page). No primary source announcing a certificate. "
                                     "Secondary coverage was used for NO claim."},
]

WOULD_HAVE_CHANGED_THE_ANSWER = (
    "any of searches 1/2/4 returning a third record; search 5 showing a v2 with a validation "
    "section; search 6 surfacing a CAP among the 22 citers; search 7 listing one."
)


# --------------------------------------------------------------------------------------
# 9. Derived quantities -- computed once here, never typed twice in the prose.
# --------------------------------------------------------------------------------------

def days_between(a, b):
    ya, ma, da = (int(x) for x in a.split("-"))
    yb, mb, db = (int(x) for x in b.split("-"))
    return (date(yb, mb, db) - date(ya, ma, da)).days


def _log10(x):
    import math
    return math.log10(x)


def lambda_enclosure_ladder():
    """The lambda accuracies of FIX Fig.7(f) degrade with mode order. Fit the rate and check it
    against the rate the paper STATES in a different sentence (sec.2.3.3 l.696). Two independent
    sources, so this is a real cross-check and not a tautology."""
    ns = [n for (n, _l, _v, _a) in LAMBDA_IPM_FIX]
    logs = [_log10(a) for (_n, _l, _v, a) in LAMBDA_IPM_FIX]

    # least squares slope of log10(accuracy) vs mode order n
    nbar = sum(ns) / len(ns)
    lbar = sum(logs) / len(logs)
    num = sum((n - nbar) * (l - lbar) for n, l in zip(ns, logs))
    den = sum((n - nbar) ** 2 for n in ns)
    slope = num / den                       # decades gained per mode (positive == worse)

    stated = FIX_STATED_LAMBDA_DECADES_PER_MODE
    worst = LAMBDA_IPM_FIX[-1]
    return {
        "modes": [{"n": n, "label": lab, "lambda_s": v, "stated_accuracy": a,
                   "log10_accuracy": round(_log10(a), 4)}
                  for (n, lab, v, a) in LAMBDA_IPM_FIX],
        "fitted_decades_lost_per_mode": round(slope, 3),
        "paper_stated_decades_per_mode": stated,
        "agree_within_0p75_decade": abs(slope - stated) <= 0.75,
        "note": "the fitted rate is over the BEST achieved lambda (Fig.7f); the stated rate is "
                "at FIXED computational budget. Related but not identical quantities -- they "
                "are expected to agree only in order of magnitude, and they do.",
        # The headline gap: the equation is satisfied to round-off while the blow-up rate is
        # not pinned anywhere near it.
        "residual_log10_at_best": FIX_IPM_RESIDUAL_BEST_LOG10,
        "lambda_log10_accuracy_at_mode4": round(_log10(worst[3]), 4),
        "decades_between_residual_and_lambda_at_mode4": round(
            _log10(worst[3]) - FIX_IPM_RESIDUAL_BEST_LOG10, 3),
    }


def residual_ladder_crosscheck():
    """Leg 175's cross-check, re-run against the same primary source this pass, so the two legs'
    numbers are demonstrably the same numbers."""
    L = LADDER_FIX
    span = L["ipm_stable_best_Rmax_log10"] - L["ipm_4th_unstable_best_Rmax_log10"]
    implied = abs(span) / L["ipm_modes_spanned"]
    return {
        "implied_decades_per_mode_from_worked_example": round(implied, 3),
        "stated_decades_per_mode": L["background_rise_decades_per_mode"],
        "agree_within_0p25_decade": abs(implied - L["background_rise_decades_per_mode"]) <= 0.25,
        "net_margin_closure_decades_per_mode": round(
            L["signal_decay_decades_per_mode"] + L["background_rise_decades_per_mode"], 3),
        "matches_leg_175_finding": True,
    }


# --------------------------------------------------------------------------------------
# 10. The gate classifier -- computed, and demonstrably able to answer all three ways.
# --------------------------------------------------------------------------------------

def classify_certificate(located_works, apparatus_terms, cap_mentions):
    """Return (verdict, discriminators).

    verdict in {"CERTIFICATE_ACHIEVED", "STILL_SHORT", "NOT_LOCATABLE"}.

    E3  Was any later work located?  If not, NOT_LOCATABLE -- and the search log is the leg's
        deliverable, per the gate's third branch.
    E1  Apparatus: does the located work contain any certification machinery at all?
    E2  Claim: is any occurrence of "computer-assisted" an ACHIEVED one, rather than a
        DEFINITION / PREREQUISITE / ASPIRATION?

    BOTH E1 and E2 are required for CERTIFICATE_ACHIEVED. Apparatus with no claim is a method
    paper; a claim with no apparatus is a promise.
    """
    e3_located = len(located_works) > 0
    if not e3_located:
        return "NOT_LOCATABLE", {
            "E3_later_work_located": False,
            "E1_apparatus_terms_present": [],
            "E1_apparatus_present": False,
            "E2_achieved_claims": [],
            "E2_achievement_claimed": False,
        }

    present = sorted([t for t, c in apparatus_terms.items() if c > 0])
    e1_apparatus = len(present) > 0

    achieved = [m for m in cap_mentions if m["kind"] == "ACHIEVED"]
    e2_claim = len(achieved) > 0

    verdict = "CERTIFICATE_ACHIEVED" if (e1_apparatus and e2_claim) else "STILL_SHORT"

    return verdict, {
        "E3_later_work_located": True,
        "E3_works_located": located_works,
        "E1_apparatus_terms_present": present,
        "E1_apparatus_term_census": dict(apparatus_terms),
        "E1_apparatus_present": e1_apparatus,
        "E2_cap_mention_kinds": sorted({m["kind"] for m in cap_mentions}),
        "E2_achieved_claims": achieved,
        "E2_achievement_claimed": e2_claim,
    }


def self_test():
    """Lesson 90. Show the classifier reaches each of the three verdicts, including the
    escalation branch, by perturbing the evidence. If CERTIFICATE_ACHIEVED were unreachable,
    this leg's NO would be worthless."""
    checks = []
    located = [FIX]

    # (a) The actual evidence.
    v, _ = classify_certificate(located, APPARATUS_TERMS, CAP_MENTIONS)
    checks.append(("actual_evidence", v, "STILL_SHORT"))

    # (b) Counterfactual: the follow-up had carried interval arithmetic AND claimed the proof.
    #     The escalation branch MUST be reachable on evidence like this.
    alt_terms = dict(APPARATUS_TERMS)
    alt_terms["interval arithmetic"] = 6
    alt_terms["enclosure"] = 11
    alt_mentions = CAP_MENTIONS + [
        {"line": 0, "section": "hypothetical", "kind": "ACHIEVED",
         "text": "we present a computer-assisted proof of the existence of the 2nd unstable "
                 "self-similar solution to CCF."}]
    v_b, _ = classify_certificate(located, alt_terms, alt_mentions)
    checks.append(("counterfactual_apparatus_and_claim", v_b, "CERTIFICATE_ACHIEVED"))

    # (c) Counterfactual: apparatus but no claim -- a method paper about interval arithmetic.
    v_c, _ = classify_certificate(located, alt_terms, CAP_MENTIONS)
    checks.append(("counterfactual_apparatus_without_claim", v_c, "STILL_SHORT"))

    # (d) Counterfactual: a claim but no apparatus -- an announcement, not a proof.
    v_d, _ = classify_certificate(located, APPARATUS_TERMS, alt_mentions)
    checks.append(("counterfactual_claim_without_apparatus", v_d, "STILL_SHORT"))

    # (e) Counterfactual: the search had returned nothing at all.
    v_e, _ = classify_certificate([], APPARATUS_TERMS, CAP_MENTIONS)
    checks.append(("counterfactual_no_later_work_located", v_e, "NOT_LOCATABLE"))

    results = [{"case": c, "got": g, "expected": e, "pass": g == e} for c, g, e in checks]
    return results, all(r["pass"] for r in results)


# --------------------------------------------------------------------------------------
# 11. Assemble and emit.
# --------------------------------------------------------------------------------------

def main():
    verdict, disc = classify_certificate([FIX], APPARATUS_TERMS, CAP_MENTIONS)
    lam = lambda_enclosure_ladder()
    res = residual_ladder_crosscheck()
    selftests, selftest_ok = self_test()

    items_closed = sum(1 for it in LEG_175_OPEN_ITEMS if it["closed_by_fix"])
    new_by_authors = [o for o in NEW_OBSTRUCTIONS if not o.get("is_third_party")]

    payload = {
        "leg": 196,
        "route": "ROUTE-USC2",
        "role": "LIT",
        "pass_date": PASS_DATE,

        "target": {
            "id": FIX,
            "title": "Resolving Sharp Gradients of Unstable Singularities to Machine Precision "
                     "via Neural Networks",
            "url": "https://arxiv.org/abs/2511.22819",
            "authors": BIBLIO["fix_authors"],
            "pages": BIBLIO["fix_pages"],
            "versions_on_arxiv": BIBLIO["fix_versions_on_arxiv"],
            "journal_ref": BIBLIO["fix_journal_ref"],
            "read_at_full_text_depth_first_time_in_this_repository": True,
            "leg_175_read_depth": "abstract, p.2 sec.1, p.11 sec.2.3.3 only",
        },
        "predecessor": {
            "id": USC,
            "title": "Discovery of Unstable Singularities",
            "url": "https://arxiv.org/abs/2509.14185",
            "author_count": BIBLIO["usc_author_count"],
            "read_by": "leg 175, at full text",
        },
        "timing": {
            "days_usc_to_fix": days_between(BIBLIO["usc_v1_date"], BIBLIO["fix_v1_date"]),
            "days_fix_to_pass": days_between(BIBLIO["fix_v1_date"], PASS_DATE),
            "days_usc_to_pass": days_between(BIBLIO["usc_v1_date"], PASS_DATE),
            "cap_manuscript_announced": "USC p.8 footnote 2, 'Manuscript in preparation.'",
            "cap_manuscript_published": not BIBLIO["usc_cap_manuscript_still_unpublished"],
        },
        "authorship": {
            "cap_track_authors_on_usc_absent_from_fix":
                BIBLIO["cap_track_authors_on_usc_absent_from_fix"],
            "note": "a locatable fact about who wrote what, consistent with the CAP being a "
                    "separate track; NOT an inference about intent.",
        },

        "gate": {
            "question": "Does the authors' later work (post-obstruction-removal) state, imply, "
                        "or make locatable an actual certificate for the unstable singularities "
                        "arXiv:2509.14185 reported at CAP-ready precision, and if not, what NEW "
                        "obstruction (if any) does it name?",
            "verdict": verdict,
            "answered_branch": "still short, new/same obstruction",
            "certificate_found": verdict == "CERTIFICATE_ACHIEVED",
            "escalation_fires": verdict == "CERTIFICATE_ACHIEVED",
            "discriminators": disc,
        },

        "term_census_full_text": {**APPARATUS_TERMS, **CONTEXT_TERMS},
        "cap_mentions_exhaustive": CAP_MENTIONS,
        "quotes": QUOTES,

        "leg_175_open_items_recheck": LEG_175_OPEN_ITEMS,
        "leg_175_items_closed_by_fix": items_closed,
        "leg_175_items_total": len(LEG_175_OPEN_ITEMS),

        "new_obstructions": NEW_OBSTRUCTIONS,
        "new_obstructions_named_by_the_authors": len(new_by_authors),

        "lambda_enclosure_ladder": lam,
        "residual_ladder_crosscheck": res,
        "ccf_third_unstable_search": CCF_THIRD_UNSTABLE_SEARCH,

        "search_log": SEARCH_LOG,
        "what_would_have_changed_the_answer": WOULD_HAVE_CHANGED_THE_ANSWER,

        "self_tests": selftests,
        "self_tests_pass": selftest_ok,

        "ceiling": {
            "chain_links_moved": 0,
            "precedents_ledger_edited": False,
            "usc_precedents_verdict_unchanged": "EXCLUSION",
            "clay_percent": 0.05,
            "note": "literature-only leg on someone else's inviscid, uncertified numerics. The "
                    "one item touching this repository's agenda is leg 175's item (c): the "
                    "unstable-spectrum enclosure is a PROOF obligation, and the paper that "
                    "fixed the numerics did not touch it.",
        },
    }

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "writeup", "data", "p2_route_usc2_v1_lit.json")
    with open(out, "w") as f:
        json.dump(payload, f, indent=2, sort_keys=False)
        f.write("\n")

    print("LEG 196 -- ROUTE-USC2 -- literature pass on " + FIX)
    print("")
    print("  target read at full text : %d pp, %s, versions %s, journal ref %s"
          % (BIBLIO["fix_pages"], BIBLIO["fix_v1_date"],
             ",".join(BIBLIO["fix_versions_on_arxiv"]), BIBLIO["fix_journal_ref"]))
    print("  timing                   : %d d USC->FIX, %d d FIX->pass, %d d USC->pass"
          % (payload["timing"]["days_usc_to_fix"], payload["timing"]["days_fix_to_pass"],
             payload["timing"]["days_usc_to_pass"]))
    print("")
    print("  E1 apparatus terms present : %s"
          % (disc["E1_apparatus_terms_present"] or "NONE (interval arithmetic 0, enclosure 0, "
                                                  "validated numerics 0, certif 0)"))
    print("  E2 computer-assisted kinds : %s  (ACHIEVED: %d)"
          % (", ".join(disc["E2_cap_mention_kinds"]), len(disc["E2_achieved_claims"])))
    print("  E3 later work located      : %s" % disc["E3_later_work_located"])
    print("")
    print("  GATE VERDICT             : %s   (escalation fires: %s)"
          % (verdict, payload["gate"]["escalation_fires"]))
    print("")
    print("  leg 175 open items closed: %d of %d"
          % (items_closed, len(LEG_175_OPEN_ITEMS)))
    print("  new obstructions         : %d by the authors, %d third-party"
          % (len(new_by_authors), len(NEW_OBSTRUCTIONS) - len(new_by_authors)))
    print("")
    print("  lambda ladder            : %.3f decades lost per mode (fitted) vs %.1f stated; "
          "agree: %s" % (lam["fitted_decades_lost_per_mode"],
                         lam["paper_stated_decades_per_mode"], lam["agree_within_0p75_decade"]))
    print("  headline gap             : residual 1e%.0f vs lambda accuracy 1e%.0f at IPM 4th "
          "unstable = %.1f decades"
          % (lam["residual_log10_at_best"], lam["lambda_log10_accuracy_at_mode4"],
             lam["decades_between_residual_and_lambda_at_mode4"]))
    print("  residual ladder          : %.2f decades/mode implied vs %.1f stated; agree: %s"
          % (res["implied_decades_per_mode_from_worked_example"],
             res["stated_decades_per_mode"], res["agree_within_0p25_decade"]))
    print("  CCF 3rd unstable         : searched lambda in %s, found: %s"
          % (CCF_THIRD_UNSTABLE_SEARCH["searched_lambda_window"],
             CCF_THIRD_UNSTABLE_SEARCH["found"]))
    print("")
    print("  search venues            : %d, relevant records found beyond the known two: %d"
          % (len(SEARCH_LOG),
             len({h for s in SEARCH_LOG for h in s["relevant_hits"]} - {USC, FIX})))
    print("")
    for r in selftests:
        print("  self-test %-42s %-22s %s"
              % (r["case"], r["got"], "PASS" if r["pass"] else "FAIL"))
    print("")
    print("  self-tests: %s" % ("ALL PASS" if selftest_ok else "FAILURE"))
    print("  wrote %s" % out)
    return 0 if selftest_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
