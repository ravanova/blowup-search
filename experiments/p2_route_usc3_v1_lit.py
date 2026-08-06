#!/usr/bin/env python3
"""Leg 239 (Route-USC3) -- literature runner: the SHAPE of the three new obstructions named by
arXiv:2511.22819, "Resolving Sharp Gradients of Unstable Singularities to Machine Precision via
Neural Networks" (Wang, Leger, Lai, Buckmaster; v1, 28 Nov 2025).

WHAT THIS IS. Leg 196 (Route-USC2) read the same 27 pages and answered "is there a certificate?"
-- STILL_SHORT -- and, along the way, NAMED three new obstructions the paper raises (its N1/N2/N3).
Leg 212 verified all three verbatim, 29/29 rows. Neither classified them. This leg applies to each
of the three the EXACT question leg 175 asked of the ORIGINAL paper's obstruction:

    MODEL-specific (naming the alternative model class the paper itself points to)
    or TECHNIQUE-specific (a precision/infrastructure gap independent of model)?

A literature leg has no PDE to integrate, so the runner is the thing that keeps the prose honest
(the pattern leg 175 established and legs 183/189/196/212 reused): every number, count and quote
that writeup/novelty/leg_239.md and experiments/journal/leg_239.md lean on is transcribed here
ONCE, from the primary source, with its line locator; the per-obstruction verdict is then COMPUTED
from that evidence rather than asserted; and the arithmetic the prose quotes is re-derived. It
emits writeup/data/p2_route_usc3_v1_lit.json.

    .venv/bin/python experiments/p2_route_usc3_v1_lit.py

WHY THE VERDICTS ARE COMPUTED (lesson 90: a control that cannot come out differently is not a
control). `classify` below takes an obstruction's evidence and returns one of

    MODEL_SPECIFIC | TECHNIQUE_SPECIFIC | UNDETERMINED

and `self_test()` exercises all three on perturbed copies of the real evidence, plus BOTH answers
of the escalation boundary check -- so neither the classification nor the escalation is reachable
by prose alone, and neither is UNreachable by construction.

THE DISCRIMINATORS, fixed in writeup/novelty/leg_239.md before the evidence was applied:

  D1  Was the technique APPLIED to the resisting object, and did it still resist?
      (leg 175's own D1. Leg 175 measured D1 = No, 0 of 4, and returned TECHNIQUE_SPECIFIC.)
  D2  Does the paper name a DIFFERENT MODEL CLASS in the passage where the obstruction is
      stated, and rank difficulty by model?  (leg 175's own D2.)
  D3  CROSS-MODEL RECURRENCE: in how many DISTINCT model classes does the paper itself exhibit
      the same obstruction?  An obstruction the paper displays in unrelated classes -- including
      non-fluid ones -- cannot be a property of any one model.
  D4  Are all remedies the paper offers APPARATUS-side (loss weighting, network size, training
      stages, memory, hardware) rather than a change of model?

  RULE:  MODEL_SPECIFIC     iff D1 and D2
         TECHNIQUE_SPECIFIC iff D3 >= 2 and D4 and not (D1 and D2)
         otherwise UNDETERMINED

  D1 IS TRUE FOR ALL THREE and therefore discriminates nothing in this leg -- every one of these
  obstructions is by construction what is LEFT AFTER the fix leg 175 identified. That is recorded
  as a finding and then set aside as non-decisive (lesson 90 again: a control whose value is
  identical on every input is not a control). D2 does the work.

PROVENANCE. arXiv:2511.22819v1 was pulled from https://arxiv.org/pdf/2511.22819 during this leg
and extracted with `pdftotext -layout`. PDF md5 8367d9b73bbc615a65da1f99bb3e520e (3 934 832 B);
extraction md5 5e20c57bf6983934fd1f40292618545c, 1593 lines -- BOTH reproducing legs 196 and 212
exactly, so the `line` locator on every quote is unambiguous across all three passes. Papers/ is
gitignored on purpose; `bash Papers/fetch.sh 2511.22819` re-pulls it. NO NETWORK ACCESS AND NO
SOLVER IMPORT at run time -- nothing here reads solver/.
"""

import json
import os
from datetime import date

USC = "arXiv:2509.14185v1"      # Discovery of Unstable Singularities -- leg 175's target
FIX = "arXiv:2511.22819v1"      # Resolving Sharp Gradients ... -- leg 196's / this leg's target

PASS_DATE = "2026-08-06"

PROVENANCE = {
    "pdf_url": "https://arxiv.org/pdf/2511.22819",
    "pdf_md5": "8367d9b73bbc615a65da1f99bb3e520e",
    "pdf_bytes": 3934832,
    "extraction_tool": "pdftotext -layout",
    "extraction_md5": "5e20c57bf6983934fd1f40292618545c",
    "extraction_lines": 1593,
    "pages_read": 27,
    "identical_to_prior_passes": ["leg_196", "leg_212"],
    "note": ("Third independent fetch-and-extract. Both md5s reproduce legs 196 and 212 exactly, "
             "so line locators are directly comparable across all three passes."),
}

# --------------------------------------------------------------------------------------
# 1. Term census over the full extraction (case-insensitive, all 1593 lines).
#    The three ZEROS marked NEW are this leg's addition and carry obstruction C's verdict.
# --------------------------------------------------------------------------------------

CENSUS = {
    "interval arithmetic": 0,
    "enclos": 0,
    "certif": 0,
    "eigen": 0,
    "extended precision": 0,      # NEW this leg -- the paper never contemplates tighter arithmetic
    "quadruple": 0,               # NEW this leg
    "float64": 0,                 # NEW this leg
    "computer-assisted": 4,
    "round-off": 9,
    "double-float": 9,
    "machine precision": 22,
    "budget": 3,
    "memory": 1,
    "spurious": 8,
    "existence": 4,
}

# "GPU" is recorded separately: the raw case-insensitive count is 4, but two of those matches are
# base64 noise inside <latexit> blobs. Reporting the raw count would have overstated the paper's
# hardware discussion by 2x. Reported as the audited count, with the discrepancy kept visible.
GPU_MENTIONS = {"raw_matches": 4, "audited_real": 2, "lines": [774, 775],
                "excluded_reason": "base64 payloads inside <latexit> blobs at l.695, l.739"}

MODEL_NAME_CENSUS = {
    "CCF": 42, "IPM": 46, "vortic": 30, "NLS": 25, "Gross-Pitaevskii": 5,
    "Boussinesq": 2, "Euler": 3,
}

# The paper's model classes, as the paper itself organizes them.
PAPER_MODEL_CLASSES = [
    {"name": "CCF (1D Cordoba-Cordoba-Fontelos)", "section": "2.1", "fluid": True},
    {"name": "IPM (2D incompressible porous media)", "section": "2.2", "fluid": True},
    {"name": "NLS with double-well potential (1D)", "section": "3.1", "fluid": False},
    {"name": "Gross-Pitaevskii vortices (2D elliptic BVP)", "section": "3.2", "fluid": False},
    {"name": "NLS excited states (2D)", "section": "3.3", "fluid": False},
]

# --------------------------------------------------------------------------------------
# 2. The three obstructions, with the evidence each discriminator is read off.
#    Labels N1/N2/N3 are leg 196's, kept so the two reports read side by side.
# --------------------------------------------------------------------------------------

OBSTRUCTIONS = [
    {
        "id": "A",
        "leg_196_label": "N1",
        "short": "the binding quantity is lambda's error bar, not the residual",
        "stated_in": "sec.2.3.3 (l.674-690 -> l.769) + Fig.7(f) table (l.714-738)",
        "quotes": [
            {"line": 678, "section": "2.3.3", "text": (
                "On average, the magnitude of the non-smooth signal Rmax decays exponentially, "
                "reducing by one order of magnitude for each higher-order singularity.")},
            {"line": 683, "section": "2.3.3", "text": (
                "the high-gradient nature of higher-order unstable modes still reduces the "
                "convergence rate of training. For a fixed computational budget (identical "
                "network size, iterations, and two training stages), the achievable background "
                "PDE residual for the smooth solution increases by approximately one order of "
                "magnitude for each successive singularity")},
            {"line": 769, "section": "2.3.3", "text": (
                "decreases the achievable lambda accuracy for a fixed computational budget by "
                "approximately two orders of magnitude per model.")},
        ],
        # D1: gradient normalization AND multistage were both applied; lambda still stops at 1e-7.
        "D1_technique_applied_and_still_resisted": True,
        "D1_evidence": ("sec.2.3.3 reports the ladder AFTER both the gradient-normalized residual "
                        "and the enhanced multistage method (l.666-667: 'Our enhanced multistage "
                        "method successfully resolved all IPM singularities ... to high "
                        "precision'); lambda accuracy still floors at 1e-7 at the 4th unstable."),
        "D2_alternative_model_class_named": False,
        "D2_evidence": ("The whole passage is internal to IPM and attributes the loss to MODE "
                        "ORDER and to a fixed computational budget. No alternative model class is "
                        "named anywhere in it. The string 'per model' at l.769 is, in context, "
                        "'per successive singularity' -- the same quantity is stated at l.686 as "
                        "'for each successive singularity'. Recorded because it is the one string "
                        "here that could be misread as a cross-model claim; it is not one."),
        "D3_recurrence_classes": [
            {"class": "IPM (2D incompressible porous media)", "locator": "sec.2.3.3, Fig.7(f) l.714-738",
             "parameter": "lambda", "fluid": True},
            {"class": "CCF (1D Cordoba-Cordoba-Fontelos)", "locator": "sec.2.3.1 l.466-475",
             "parameter": "lambda", "fluid": True,
             "quote": ("However, it is spurious. ... there is no meaningful variation ... and "
                       "prevents us from finding a more accurate smooth lambda_s")},
            {"class": "Gross-Pitaevskii vortices (2D elliptic BVP)", "locator": "sec.3.2.1 l.941-944",
             "parameter": "core coefficient a_n", "fluid": False,
             "quote": ("this plateau is a spurious artifact caused by the insensitivity of the "
                       "standard loss function to the extremely small value of Un around the "
                       "origin")},
        ],
        "D4_remedies_all_apparatus_side": True,
        "D4_remedies": ["larger networks with more weights (l.770)",
                        "introducing a third stage (l.771)",
                        "Both approaches, however, require more memory (l.772)",
                        "a single A100 GPU (80GB) (l.774)",
                        "more training stages in parallel on multiple GPUs (l.775)"],
        "gap_kind_leg173_vocabulary": "precision",
    },
    {
        "id": "B",
        "leg_196_label": "N2",
        "short": "the discovery frontier stalled: CCF's 3rd unstable searched for and not found",
        "stated_in": "sec.2.1.3 (l.269-281) + Fig.3",
        "quotes": [
            {"line": 271, "section": "2.1.3", "text": (
                "as lambda decreases, the solution's peak amplitude increases dramatically, "
                "reaching nearly 40 for lambda approx 0.455")},
            {"line": 275, "section": "2.1.3", "text": (
                "While our gradient-normalization method effectively reduces the residual in the "
                "peak region, a persistent non-smooth signal at the origin (inset of Fig.3b) "
                "remains for all tested lambda in [0.455, 0.4713]. This indicates that if a third "
                "unstable solution exists, it is located at a lambda value corresponding to an "
                "even higher-gradient profile.")},
            {"line": 278, "section": "2.1.3", "text": (
                "The challenge of exploring the range lambda < 0.455 and resolving such a feature "
                "in the 1D CCF model appears to be even greater than finding highly unstable "
                "solutions in the 2D IPM equation.")},
            {"line": 280, "section": "2.1.3", "text": (
                "A full investigation into the existence and properties of this third unstable "
                "solution is a compelling direction for future research.")},
        ],
        "D1_technique_applied_and_still_resisted": True,
        "D1_evidence": ("l.275: the gradient-normalization method WAS applied and 'effectively "
                        "reduces the residual in the peak region'; the non-smooth origin signal "
                        "survived it across the entire tested window. This is the first D1 = yes "
                        "in the two-paper record (leg 175 measured D1 = 0 of 4)."),
        "D2_alternative_model_class_named": True,
        "D2_named_class": "2D Incompressible Porous Media (IPM) equation",
        "D2_evidence": ("l.278-280 ranks difficulty BETWEEN TWO NAMED MODELS -- the only such "
                        "sentence in 27 pages -- and in the surprising direction: the 1D model is "
                        "rated harder than the 2D one."),
        "paper_own_reasoning": [
            ("profile geometry as a function of the model's own parameter: peak amplitude reaches "
             "nearly 40 at lambda approx 0.455 (l.271-272), so a third solution 'would possess "
             "even more extreme gradients than the second' (l.273-274)"),
            ("the residual fix worked and was not the binding constraint (l.275)"),
            ("existence is conditional -- 'if a third unstable solution exists' (l.277) and 'a "
             "full investigation into the existence ... ' (l.280). No amount of precision decides "
             "an existence question; this is the one strand of the three that is not a numerics "
             "statement at all."),
        ],
        "D3_recurrence_classes": [
            {"class": "CCF (1D Cordoba-Cordoba-Fontelos)", "locator": "sec.2.1.3 l.269-281",
             "parameter": "3rd unstable mode", "fluid": True},
        ],
        "D3_counter_evidence": ("The frontier-stall does NOT recur. On IPM the frontier ADVANCED "
                                "(+1 mode: the 4th unstable newly confirmed, l.105/l.131); on NLS "
                                "excited states the analogous 'cannot reach the target solution' "
                                "problem was SOLVED by targeted inequality constraints (sec.3.3.3 "
                                "l.1187-1212). CCF is the only class where the frontier moved 0 "
                                "modes."),
        "D4_remedies_all_apparatus_side": False,
        "D4_remedies": ["'a compelling direction for future research' (l.281) -- no remedy offered"],
        "gap_kind_leg173_vocabulary": "scope",
    },
    {
        "id": "C",
        "leg_196_label": "N3",
        "short": "the remaining margin is arithmetic- and hardware-bound (double-float round-off)",
        "stated_in": "sec.1 l.50-51 (definition of success) + sec.2.3.3 l.770-775 (remedies)",
        "quotes": [
            {"line": 50, "section": "1", "text": (
                "we refer to machine precision as the highest achievable accuracy, where the "
                "remaining PDE residuals are dominated by the inherent round-off errors of "
                "double-float arithmetic, typically O(10^-13) or lower")},
            {"line": 618, "section": "2.3.1", "text": (
                "although the absolute PDE residual remains higher in the region of high solution "
                "gradient, this is constrained by the round-off error of double-float precision")},
            {"line": 774, "section": "2.3.3", "text": (
                "that can be implemented on a single A100 GPU (80GB). To further improve the "
                "lambda accuracy, one could use larger networks or more training stages in "
                "parallel on multiple GPUs.")},
        ],
        "D1_technique_applied_and_still_resisted": True,
        "D1_evidence": ("The round-off floor is by definition what remains after the full "
                        "apparatus is applied (l.50-51 defines success AS reaching it)."),
        "D2_alternative_model_class_named": False,
        "D2_evidence": "No model class is named in any of the passages that state the floor.",
        "D3_recurrence_classes": [
            {"class": "CCF (1D Cordoba-Cordoba-Fontelos)", "locator": "l.616-620, Fig.5f",
             "floor_as_printed": "O(10^-13)", "fluid": True},
            {"class": "IPM (2D incompressible porous media)", "locator": "l.1423-1424",
             "floor_as_printed": "O(10^-11)-O(10^-13)", "fluid": True},
            {"class": "NLS with double-well potential (1D)", "locator": "l.860-862",
             "floor_as_printed": "loss plateau 10^-29; 'round-off error of the double-float precision'",
             "fluid": False},
            {"class": "Gross-Pitaevskii vortices (2D elliptic BVP)", "locator": "l.948, l.1004-1005",
             "floor_as_printed": "O(10^-15)", "fluid": False},
            {"class": "NLS excited states (2D)", "locator": "l.1159-1161",
             "floor_as_printed": "'reaching round-off errors throughout the domain'", "fluid": False},
        ],
        "D3_note": ("the five rows are five SETTINGS spanning FOUR model classes -- NLS appears "
                    "twice (double-well, sec.3.1; excited states, sec.3.3). Three of the five "
                    "settings are not fluid equations at all. The count used by the rule is the "
                    "number of rows, and it clears the threshold of 2 either way."),
        "D4_remedies_all_apparatus_side": True,
        "D4_remedies": ["larger networks (l.770)", "a third stage (l.771)",
                        "more memory (l.772)", "multiple GPUs (l.775)"],
        "gap_kind_leg173_vocabulary": "infrastructure",
    },
]

# --------------------------------------------------------------------------------------
# 3. The magnitudes the prose quotes.
# --------------------------------------------------------------------------------------

# Fig. 7(f), l.714-738 -- transcribed from the primary source this pass; identical to legs 196/212.
IPM_LAMBDA_TABLE = [
    {"mode": 0, "label": "stable",       "line": 714, "lambda_s": "1.0285722760323", "accuracy": 1e-13},
    {"mode": 1, "label": "1st unstable", "line": 720, "lambda_s": "0.472129736156",  "accuracy": 2e-12},
    {"mode": 2, "label": "2nd unstable", "line": 726, "lambda_s": "0.3149617817",    "accuracy": 3e-10},
    {"mode": 3, "label": "3rd unstable", "line": 732, "lambda_s": "0.24156641",      "accuracy": 1e-8},
    {"mode": 4, "label": "4th unstable", "line": 738, "lambda_s": "0.1987237",       "accuracy": 1e-7},
]
STATED_DECADES_PER_MODE = 2.0          # l.769
RESIDUAL_LOG10_AT_BEST = -13.0         # sec.5 l.1423

CCF_FRONTIER = {
    "searched_lambda_window": [0.455, 0.4713],
    "window_width": 0.0163,
    "peak_amplitude_at_low_end": 40,              # l.272, "reaching nearly 40"
    "modes_in_suite_before": 3,                   # l.157: stable, 1st unstable, 2nd unstable
    "modes_gained_this_paper_ccf": 0,
    "modes_gained_this_paper_ipm": 1,             # 4th unstable newly confirmed, l.105/l.131
    "remaining_search_region": "open half-line lambda < 0.455",
    "finite_gap_quotable": False,                 # lesson 73: no referent -> say so, do not bound
}

# --------------------------------------------------------------------------------------
# 4. The escalation boundary check, measured over this repository's OWN solver modules.
#    Counts are files under solver/ (+ capabilities.py) matching the model-class regex, taken
#    this pass. The Boussinesq and gCLM rows are the POSITIVE CONTROL: the same test fires
#    loudly on the families this repository does touch (lesson 90).
# --------------------------------------------------------------------------------------

REPO_INFRA_COVERAGE = {
    "IPM (2D incompressible porous media)": {
        "solver_files": 1, "touched": False,
        "note": ("the single hit is the citation string in solver/viscous_novelty.py::PRECEDENTS "
                 "line 171, the ledger row for arXiv:2509.14185 -- a bibliography line, not a model")},
    "CCF (Cordoba-Cordoba-Fontelos)": {"solver_files": 0, "touched": False, "note": "no hit anywhere in solver/"},
    "NLS / Gross-Pitaevskii": {"solver_files": 1, "touched": False, "note": "same ledger, same kind of hit"},
    "Boussinesq": {"solver_files": 12, "touched": True, "note": "POSITIVE CONTROL -- touched heavily"},
    "gCLM / CLM / De Gregorio": {"solver_files": 33, "touched": True, "note": "POSITIVE CONTROL -- touched heavily"},
}

REPO_FAMILY_THE_GATE_NAMES = ["gCLM / CLM / De Gregorio", "Boussinesq"]

# --------------------------------------------------------------------------------------
# 5. Classification -- computed, not asserted.
# --------------------------------------------------------------------------------------


def classify(obs):
    """MODEL_SPECIFIC | TECHNIQUE_SPECIFIC | UNDETERMINED, from the four discriminators."""
    d1 = bool(obs["D1_technique_applied_and_still_resisted"])
    d2 = bool(obs["D2_alternative_model_class_named"])
    d3 = len(obs["D3_recurrence_classes"])
    d4 = bool(obs["D4_remedies_all_apparatus_side"])
    if d1 and d2:
        return "MODEL_SPECIFIC"
    if d3 >= 2 and d4:
        return "TECHNIQUE_SPECIFIC"
    return "UNDETERMINED"


def overall(verdicts):
    """ALL_TECHNIQUE_SPECIFIC | ALL_MODEL_SPECIFIC | MIXED | UNDETERMINED_PRESENT."""
    s = set(verdicts)
    if "UNDETERMINED" in s:
        return "UNDETERMINED_PRESENT"
    if s == {"TECHNIQUE_SPECIFIC"}:
        return "ALL_TECHNIQUE_SPECIFIC"
    if s == {"MODEL_SPECIFIC"}:
        return "ALL_MODEL_SPECIFIC"
    return "MIXED"


def escalation_fires(model_specific_classes, coverage, family_names):
    """The gate escalates only if a named alternative class is one this repo's infra touches."""
    hits = []
    for cls in model_specific_classes:
        for key, row in coverage.items():
            if not row["touched"]:
                continue
            if key not in family_names:
                continue
            if _same_class(cls, key):
                hits.append({"named_class": cls, "repo_family": key,
                             "solver_files": row["solver_files"]})
    return (len(hits) > 0), hits


def _same_class(named, repo_key):
    """Loose family match between the paper's wording and the repo's family names."""
    tokens = {"ipm": "ipm", "porous": "ipm", "ccf": "ccf", "cordoba": "ccf",
              "boussinesq": "boussinesq", "gclm": "gclm", "clm": "gclm",
              "gregorio": "gclm", "schrodinger": "nls", "pitaevskii": "nls", "nls": "nls"}
    def fam(s):
        s = s.lower()
        out = set()
        for t, f in tokens.items():
            if t in s:
                out.add(f)
        return out
    return bool(fam(named) & fam(repo_key))


def fit_decades_per_mode(table):
    """Least-squares slope of log10(accuracy) against mode index, over the Fig.7(f) rows."""
    import math
    xs = [r["mode"] for r in table]
    ys = [math.log10(r["accuracy"]) for r in table]
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    return sxy / sxx


# --------------------------------------------------------------------------------------
# 6. Self-tests -- the classifier and the escalation check must both be able to answer
#    differently on evidence that warranted it.
# --------------------------------------------------------------------------------------


def self_test():
    import copy
    results = []

    def check(case, got, want):
        results.append({"case": case, "got": got, "want": want, "pass": got == want})

    real = {o["id"]: classify(o) for o in OBSTRUCTIONS}
    check("real A (N1)", real["A"], "TECHNIQUE_SPECIFIC")
    check("real B (N2)", real["B"], "MODEL_SPECIFIC")
    check("real C (N3)", real["C"], "TECHNIQUE_SPECIFIC")

    # A becomes MODEL_SPECIFIC if the paper HAD named an alternative class in that passage.
    a = copy.deepcopy(OBSTRUCTIONS[0])
    a["D2_alternative_model_class_named"] = True
    check("A + named alternative class -> MODEL", classify(a), "MODEL_SPECIFIC")

    # B becomes TECHNIQUE_SPECIFIC if the paper had shown the same stall in a second class
    # and offered an apparatus remedy.
    b = copy.deepcopy(OBSTRUCTIONS[1])
    b["D2_alternative_model_class_named"] = False
    b["D3_recurrence_classes"] = b["D3_recurrence_classes"] + [
        {"class": "IPM (2D incompressible porous media)", "locator": "counterfactual"}]
    b["D4_remedies_all_apparatus_side"] = True
    check("B - named class + recurrence -> TECHNIQUE", classify(b), "TECHNIQUE_SPECIFIC")

    # UNDETERMINED is reachable: single class, no named alternative, no apparatus remedy.
    u = copy.deepcopy(OBSTRUCTIONS[2])
    u["D2_alternative_model_class_named"] = False
    u["D3_recurrence_classes"] = u["D3_recurrence_classes"][:1]
    u["D4_remedies_all_apparatus_side"] = False
    check("single class, no remedy -> UNDETERMINED", classify(u), "UNDETERMINED")

    # The overall roll-up reaches every branch.
    check("overall real", overall(list(real.values())), "MIXED")
    check("overall all-technique", overall(["TECHNIQUE_SPECIFIC"] * 3), "ALL_TECHNIQUE_SPECIFIC")
    check("overall all-model", overall(["MODEL_SPECIFIC"] * 3), "ALL_MODEL_SPECIFIC")
    check("overall with undetermined",
          overall(["TECHNIQUE_SPECIFIC", "UNDETERMINED", "MODEL_SPECIFIC"]), "UNDETERMINED_PRESENT")

    # The escalation boundary check -- BOTH answers, on the same coverage table.
    fires_real, _ = escalation_fires(["2D Incompressible Porous Media (IPM) equation"],
                                     REPO_INFRA_COVERAGE, REPO_FAMILY_THE_GATE_NAMES)
    check("escalation on IPM (real)", fires_real, False)
    fires_cf, hits_cf = escalation_fires(["the 2D Boussinesq system"],
                                         REPO_INFRA_COVERAGE, REPO_FAMILY_THE_GATE_NAMES)
    check("escalation on Boussinesq (counterfactual)", fires_cf, True)
    check("counterfactual names the right family",
          hits_cf[0]["repo_family"] if hits_cf else None, "Boussinesq")
    fires_gclm, _ = escalation_fires(["the generalized CLM (gCLM) family"],
                                     REPO_INFRA_COVERAGE, REPO_FAMILY_THE_GATE_NAMES)
    check("escalation on gCLM (counterfactual)", fires_gclm, True)

    # The fitted ladder must reproduce legs 196 and 212 to three decimals.
    check("fitted decades/mode reproduces legs 196/212",
          round(fit_decades_per_mode(IPM_LAMBDA_TABLE), 3), 1.570)

    return results, all(r["pass"] for r in results)


# --------------------------------------------------------------------------------------
# 7. Assemble and emit.
# --------------------------------------------------------------------------------------


def main():
    import math

    verdicts = {}
    for o in OBSTRUCTIONS:
        v = classify(o)
        verdicts[o["id"]] = v
        o["verdict"] = v
        o["D3_recurrence_count"] = len(o["D3_recurrence_classes"])
        o["D3_nonfluid_classes"] = sum(1 for c in o["D3_recurrence_classes"]
                                       if c.get("fluid") is False)

    overall_verdict = overall([o["verdict"] for o in OBSTRUCTIONS])

    model_specific = [o for o in OBSTRUCTIONS if o["verdict"] == "MODEL_SPECIFIC"]
    named_classes = [o["D2_named_class"] for o in model_specific]
    fires, hits = escalation_fires(named_classes, REPO_INFRA_COVERAGE, REPO_FAMILY_THE_GATE_NAMES)

    fitted = fit_decades_per_mode(IPM_LAMBDA_TABLE)
    lam_worst = math.log10(IPM_LAMBDA_TABLE[-1]["accuracy"])
    ladder = {
        "fitted_decades_lost_per_mode": round(fitted, 3),
        "paper_stated_decades_per_mode": STATED_DECADES_PER_MODE,
        "ratio_stated_over_fitted": round(STATED_DECADES_PER_MODE / fitted, 3),
        "residual_log10_at_best": RESIDUAL_LOG10_AT_BEST,
        "lambda_log10_accuracy_at_mode4": lam_worst,
        "decades_between_residual_and_lambda_at_mode4": round(lam_worst - RESIDUAL_LOG10_AT_BEST, 1),
        "reproduces_legs_196_and_212": True,
        "note": ("fitted = best achieved across the five Fig.7(f) rows; stated = degradation at a "
                 "FIXED computational budget. Not the same quantity -- they agree in order of "
                 "magnitude, which is what makes this a cross-check rather than a tautology."),
    }

    selftests, selftest_ok = self_test()

    payload = {
        "leg": 239,
        "route": "USC3",
        "role": "LIT",
        "pass_date": PASS_DATE,
        "generated": date.today().isoformat(),
        "target": FIX,
        "predecessor_target": USC,
        "gate": {
            "question": ("For each of the three obstructions arXiv:2511.22819 names, is it "
                         "MODEL-specific (naming the alternative model class the paper itself "
                         "points to) or TECHNIQUE-specific (a precision/infrastructure gap "
                         "independent of model)?"),
            "answer": overall_verdict,
            "per_obstruction": verdicts,
            "escalation_fires": fires,
            "escalation_hits": hits,
            "escalation_reasoning": (
                "Obstruction B is MODEL_SPECIFIC and the paper names its alternative class "
                "explicitly: the 2D Incompressible Porous Media equation (l.278-280). That class "
                "is touched by 1 file under solver/, and that single hit is a citation string in "
                "the PRECEDENTS ledger, not a model. The same test returns 12 files for "
                "Boussinesq and 33 for the gCLM family, so it is a control that can fire. It does "
                "not fire here. No construction is proposed under this leg's authority."),
        },
        "provenance": PROVENANCE,
        "discriminators": {
            "D1": "technique applied to the resisting object and it still resisted (leg 175's D1)",
            "D2": "paper names a different MODEL CLASS in the obstruction's own passage (leg 175's D2)",
            "D3": "cross-model recurrence: distinct model classes in which the paper exhibits it",
            "D4": "all remedies offered are apparatus-side, not a change of model",
            "rule": ("MODEL_SPECIFIC iff D1 and D2; TECHNIQUE_SPECIFIC iff D3>=2 and D4 and not "
                     "(D1 and D2); otherwise UNDETERMINED"),
            "D1_is_non_discriminating_in_this_leg": True,
            "D1_note": ("D1 is TRUE for all three obstructions -- each is by construction what is "
                        "LEFT AFTER the loss-reweighting fix leg 175 identified. A control whose "
                        "value is identical on every input is not a control (lesson 90); recorded "
                        "as a finding, then set aside as non-decisive. D2 does the work."),
        },
        "obstructions": OBSTRUCTIONS,
        "census": CENSUS,
        "gpu_mentions": GPU_MENTIONS,
        "model_name_census": MODEL_NAME_CENSUS,
        "paper_model_classes": PAPER_MODEL_CLASSES,
        "ipm_lambda_table": IPM_LAMBDA_TABLE,
        "lambda_ladder": ladder,
        "ccf_frontier": CCF_FRONTIER,
        "repo_infra_coverage": REPO_INFRA_COVERAGE,
        "repo_family_the_gate_names": REPO_FAMILY_THE_GATE_NAMES,
        "gap_summary_leg173_vocabulary": {
            o["leg_196_label"]: {"kind": o["gap_kind_leg173_vocabulary"], "verdict": o["verdict"]}
            for o in OBSTRUCTIONS
        },
        "prior_art": {
            "leg_175": "located the follow-up; read abstract + p.2 s1 + p.11 s2.3.3; classified the ORIGINAL paper's obstruction",
            "leg_196": "read all 27 pp; answered 'is there a certificate' (STILL_SHORT); NAMED N1/N2/N3; classified none",
            "leg_212": "independent VERIFY of leg 196, 29/29 rows, 3 locator slips; classified none",
            "leg_173": "supplied the precision/scope/infrastructure vocabulary reused here",
            "what_is_new_here": "the classification of each of the three, computed, plus the escalation boundary check",
        },
        "ceiling": ("No link of the L1->L4 chain moved. Clay stays ~0.05%. This leg classifies "
                    "someone else's obstructions and produces no new mathematical content. "
                    "arXiv:2509.14185's EXCLUSION verdict in the precedents ledger is unchanged "
                    "and this leg edits no ledger."),
        "self_tests": selftests,
        "self_tests_pass": selftest_ok,
    }

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "writeup", "data", "p2_route_usc3_v1_lit.json")
    with open(out, "w") as f:
        json.dump(payload, f, indent=2, sort_keys=False)
        f.write("\n")

    print("LEG 239 -- ROUTE-USC3 -- the SHAPE of the three new obstructions in " + FIX)
    print("")
    print("  provenance : pdf md5 %s, extraction md5 %s, %d lines -- identical to legs %s"
          % (PROVENANCE["pdf_md5"][:12] + "...", PROVENANCE["extraction_md5"][:12] + "...",
             PROVENANCE["extraction_lines"], ", ".join(PROVENANCE["identical_to_prior_passes"])))
    print("")
    for o in OBSTRUCTIONS:
        print("  %s (%s) %s" % (o["id"], o["leg_196_label"], o["short"]))
        print("      D1 applied+resisted %-5s   D2 alt class named %-5s   D3 classes %d (%d non-fluid)   D4 apparatus-only %s"
              % (o["D1_technique_applied_and_still_resisted"],
                 o["D2_alternative_model_class_named"],
                 o["D3_recurrence_count"], o["D3_nonfluid_classes"],
                 o["D4_remedies_all_apparatus_side"]))
        print("      gap kind (leg 173 vocabulary): %-14s  VERDICT: %s"
              % (o["gap_kind_leg173_vocabulary"], o["verdict"]))
        if o["verdict"] == "MODEL_SPECIFIC":
            print("      alternative model class the paper itself names: %s" % o["D2_named_class"])
    print("")
    print("  GATE ANSWER : %s   (escalation fires: %s)" % (overall_verdict, fires))
    print("")
    print("  D1 is TRUE on all three -> non-discriminating in this leg (lesson 90). D2 decides.")
    print("")
    print("  lambda ladder  : %.3f decades/mode fitted vs %.1f stated (ratio %.3fx); "
          "residual 1e%.0f vs lambda 1e%.0f at IPM 4th unstable = %.1f decades"
          % (ladder["fitted_decades_lost_per_mode"], ladder["paper_stated_decades_per_mode"],
             ladder["ratio_stated_over_fitted"], ladder["residual_log10_at_best"],
             ladder["lambda_log10_accuracy_at_mode4"],
             ladder["decades_between_residual_and_lambda_at_mode4"]))
    print("  CCF frontier   : window %s (width %.4f), peak ~%d, modes gained CCF %d vs IPM %d; "
          "remaining search = %s"
          % (CCF_FRONTIER["searched_lambda_window"], CCF_FRONTIER["window_width"],
             CCF_FRONTIER["peak_amplitude_at_low_end"],
             CCF_FRONTIER["modes_gained_this_paper_ccf"],
             CCF_FRONTIER["modes_gained_this_paper_ipm"],
             CCF_FRONTIER["remaining_search_region"]))
    print("  arithmetic     : extended precision %d, quadruple %d, float64 %d, interval arithmetic %d, "
          "enclos %d  (memory %d, GPU %d audited)"
          % (CENSUS["extended precision"], CENSUS["quadruple"], CENSUS["float64"],
             CENSUS["interval arithmetic"], CENSUS["enclos"], CENSUS["memory"],
             GPU_MENTIONS["audited_real"]))
    print("")
    print("  escalation boundary check (solver files matching, this repository):")
    for k, v in REPO_INFRA_COVERAGE.items():
        print("      %-40s %2d  touched=%-5s %s"
              % (k, v["solver_files"], v["touched"],
                 "<- named by the paper" if _same_class(k, " ".join(named_classes)) else ""))
    print("")
    for r in selftests:
        print("  self-test %-46s %-22s %s"
              % (r["case"], r["got"], "PASS" if r["pass"] else "FAIL"))
    print("")
    print("  self-tests: %s" % ("ALL PASS" if selftest_ok else "FAILURE"))
    print("  wrote %s" % out)
    return 0 if selftest_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
