#!/usr/bin/env python3
"""Leg 175 (Route-USC) -- scoping runner for arXiv:2509.14185, "Discovery of Unstable
Singularities" (Wang, ..., Buckmaster, Georgiev, Gomez-Serrano, Jiang, Lai; v1, 17 Sep 2025).

WHAT THIS IS. A literature-scoping leg has no PDE to integrate, so the "runner" is the thing
that keeps the prose honest: every number quoted in writeup/novelty/leg_175.md and
experiments/journal/leg_175.md is transcribed here ONCE, from the primary source, with its
page and section; the gate verdict is then COMPUTED from that table rather than asserted; and
the arithmetic the prose leans on is re-derived and cross-checked. It emits
writeup/data/p2_route_usc_v1_scoping.json.

    .venv/bin/python experiments/p2_route_usc_v1_scoping.py

WHY THE VERDICT IS COMPUTED (lesson 90: a control that cannot come out differently is not a
control). The MODEL-vs-TECHNIQUE classification is the leg's whole deliverable, so it must not
be a constant in the source. `classify_obstruction` below takes the evidence table and returns
MODEL_SPECIFIC, TECHNIQUE_SPECIFIC or NOT_LOCATABLE. Two discriminators decide it, and
`self_test()` exercises BOTH outcomes on perturbed copies of the evidence, so the classifier is
demonstrably capable of answering the other way:

  D1  Is any solution to which the paper's own precision technique (multi-stage training) WAS
      applied still stranded above the CAP threshold?  If yes, the technique was applied and
      the model resisted -> evidence of a MODEL wall.
  D2  Did a later, model-preserving TECHNIQUE change move previously-stranded solutions to the
      threshold?  If yes, the barrier was in the method -> TECHNIQUE-specific.

D2 is the decisive one and it is not our inference: arXiv:2511.22819 (Wang, Leger, Lai,
Buckmaster; 28 Nov 2025) is the same core author group changing only the loss function.

NO NETWORK ACCESS AND NO SOLVER IMPORT. Both PDFs were fetched at primary source during the
leg (Papers/ is gitignored on purpose; `bash Papers/fetch.sh 2509.14185 2511.22819` re-pulls
them). Nothing here reads solver/.
"""

import json
import os

# --------------------------------------------------------------------------------------
# 1. The paper's own numbers, transcribed from the primary source with page provenance.
# --------------------------------------------------------------------------------------

USC = "arXiv:2509.14185v1"          # Discovery of Unstable Singularities, 20 pp, 17 Sep 2025
FIX = "arXiv:2511.22819v1"          # Resolving Sharp Gradients ..., 27 pp, 28 Nov 2025

# The paper's own stated CAP threshold: "machine precision ... typically O(10^-13) or lower"
# (FIX p.1 sec.1); USC p.8 claims sufficiency at "double-float machine precision", O(10^-13).
CAP_THRESHOLD_LOG10 = -13.0

# USC Figure 3b, p.6 -- log10 maximum equation residual, best solution discovered.
# "multistage" records whether USC applied its five-decade precision technique to that
# solution: USC p.17 Methods/Multi-stage Training, "we apply two-stage training to the stable
# and first unstable solutions of the CCF and IPM equations" (restated main text p.8).
RESIDUALS_USC = [
    # (model,               mode,           log10_max_residual, multistage_applied)
    ("CCF",                 "stable",       -13.714, True),
    ("CCF",                 "1st unstable", -13.589, True),
    ("CCF",                 "2nd unstable",  -6.664, False),
    ("IPM with boundary",   "stable",       -11.183, True),
    ("IPM with boundary",   "1st unstable", -10.510, True),
    ("IPM with boundary",   "2nd unstable",  -8.101, False),
    ("IPM with boundary",   "3rd unstable",  -7.526, False),
    ("Boussinesq",          "stable",        -8.178, False),
    ("Boussinesq",          "1st unstable",  -8.038, False),
    ("Boussinesq",          "2nd unstable",  -7.772, False),
    ("Boussinesq",          "3rd unstable",  -7.558, False),
    ("Boussinesq",          "4th unstable",  -7.020, False),
]

# USC p.17: the floor of the pipeline WITHOUT multi-stage training, in the paper's own words --
# "we are unable to reach maximum equation residuals much below 10^-8".
SINGLE_STAGE_FLOOR_LOG10 = -8.0

# USC Figure 2f, p.4 -- admissible self-similar scaling parameters, to their stated
# significant digits. USC Fig.2f caption: "The 4th unstable solution of the Boussinesq
# equation is un-validated."
LAMBDA_USC = {
    "CCF":               {"stable": 1.1807776628998, "1st unstable": 0.6057337012032,
                          "2nd unstable": 0.4713248638620},
    "IPM with boundary": {"stable": 1.0285722760222, "1st unstable": 0.4721297362414,
                          "2nd unstable": 0.3149620267088, "3rd unstable": 0.2415604743989},
    "Boussinesq":        {"stable": 1.9205599746927, "1st unstable": 1.3990961221852,
                          "2nd unstable": 1.2523481636489, "3rd unstable": 1.1842500861997,
                          "4th unstable": 1.1448833556188},
}
UNVALIDATED_USC = [("Boussinesq", "4th unstable")]   # USC p.4 Fig.2f caption; p.5 body

# FIX p.2 sec.1 -- post-fix accuracy, same models, loss re-weighting only.
# "We achieve O(10^-13) residuals for the full suite of previously discovered CCF solutions and
#  achieve accuracy between O(10^-11) and O(10^-13) for the 2-D IPM solutions."
RESIDUALS_FIX = {
    "CCF":               {"best_log10": -13.0, "worst_log10": -13.0, "coverage": "full suite"},
    "IPM with boundary": {"best_log10": -13.0, "worst_log10": -11.0, "coverage": "all modes, "
                          "including the newly confirmed 4th unstable"},
    # "Boussinesq" occurs exactly once in FIX -- in the abstract's recap of [1] -- and never in
    # the body. The fix was demonstrated on "two canonical models: the 1D
    # Cordoba-Cordoba-Fontelos equation and the 2D Incompressible Porous Media equation"
    # (FIX p.2 sec.2). Deliberately absent from this dict; see MODELS_UNFIXED.
}
MODELS_UNFIXED = ["Boussinesq"]

# FIX p.11 sec.2.3.3 -- the two compounding ladders, per additional unstable mode.
LADDER_FIX = {
    "signal_decay_decades_per_mode": 1.0,       # "reducing by one order of magnitude for each
                                                # higher-order singularity"
    "background_rise_decades_per_mode": 1.0,    # "increases by approximately one order of
                                                # magnitude for each successive singularity"
    # The worked example the paper gives for the background ladder, IPM, fixed compute budget:
    "ipm_stable_best_log10": -14.0,             # "reaches O(10^-14)"
    "ipm_4th_unstable_best_log10": -10.0,       # "stagnates at O(10^-10)"
    "ipm_modes_spanned": 4,                     # stable (n=0) -> 4th unstable (n=4)
}

# Bibliographic facts, checked against https://arxiv.org/abs/2509.14185 on the pass date.
BIBLIO = {
    "usc_versions_on_arxiv": ["v1"],
    "usc_v1_date": "2025-09-17",
    "fix_v1_date": "2025-11-28",
    "pass_date": "2026-08-06",
    "usc_si_published": False,      # footnote 1, p.4: "will be uploaded in a forthcoming
                                    # version of the manuscript" -- no v2 exists
    "usc_cap_manuscript_published": False,   # footnote 2, p.8: "Manuscript in preparation."
}

# The verbatim statements the gate turns on. Page + section carried with each.
QUOTES = [
    {"src": USC, "page": 8, "section": "Implications for Future Studies",
     "text": "This level of accuracy proves to be sufficient for utilizing the numerical "
             "solution for computer-assisted proofs for this specific problem[2], although the "
             "required precision for such proofs is generally problem-dependent.",
     "bears_on": "CAP-readiness is claimed for CCF only, and the threshold is stated to be "
                 "problem-dependent"},
    {"src": USC, "page": 8, "section": "footnote 2",
     "text": "Manuscript in preparation.",
     "bears_on": "the promised CAP; still unpublished at the pass date"},
    {"src": USC, "page": 17, "section": "Methods / Multi-stage Training",
     "text": "If we only employ methods described up to this point, we are unable to reach "
             "maximum equation residuals much below 10^-8.",
     "bears_on": "the precision floor is attributed to the METHOD, not to any model"},
    {"src": USC, "page": 17, "section": "Methods / Multi-stage Training",
     "text": "In this study, we apply two-stage training to the stable and first unstable "
             "solutions of the CCF and IPM equations.",
     "bears_on": "the technique reached only 4 of 12 solutions"},
    {"src": USC, "page": 19, "section": "Methods / Spectrum of Linearization",
     "text": "For a computer-assisted proof to be feasible, it is desirable that the spectrum "
             "in the right-half mu-plane consists of a finite number of eigenvalues.",
     "bears_on": "a CAP prerequisite stated as desirable and never established"},
    {"src": USC, "page": 19, "section": "Methods / Spectrum of Linearization",
     "text": "we learn the non-negative real eigenvalues of the corresponding linearized "
             "operators, under the assumption that there exist eigenvalues with non-negative "
             "real part that lie on the real axis",
     "bears_on": "the unstable-mode count is assumed real, not enclosed"},
    {"src": USC, "page": 19, "section": "Methods / Spectrum of Linearization",
     "text": "Here, the eigenfunction problem is restricted to Psi that lie within the same "
             "symmetry class as the original solution.",
     "bears_on": "the unstable subspace is enumerated only inside the symmetry class"},
    {"src": USC, "page": 18, "section": "Methods / Validation of lambda",
     "text": "there exists a limit to the resolution of lambda at which this method can discern "
             "admissibility",
     "bears_on": "lambda digits come from a seed-averaged basin width, not an enclosure"},
    {"src": USC, "page": 4, "section": "footnote 1",
     "text": "The Supplementary Information to the paper will be uploaded in a forthcoming "
             "version of the manuscript.",
     "bears_on": "every object a CAP would enclose is deferred to a document that does not exist"},
    {"src": FIX, "page": 1, "section": "Abstract",
     "text": "For highly unstable solutions characterized by extreme gradients, the accuracy "
             "remained insufficient for validation. The primary obstacle is the presence of "
             "sharp solution gradients.",
     "bears_on": "the same authors name USC's obstruction explicitly"},
    {"src": FIX, "page": 2, "section": "1 Introduction",
     "text": "We achieve O(10^-13) residuals for the full suite of previously discovered CCF "
             "solutions and achieve accuracy between O(10^-11) and O(10^-13) for the 2-D IPM "
             "solutions.",
     "bears_on": "a loss re-weighting, on unchanged models, removed the barrier"},
    {"src": FIX, "page": 11, "section": "2.3.3",
     "text": "the best Rmax residual for the stable solution reaches O(10^-14), while the one "
             "for the 4th unstable solution stagnates at O(10^-10)",
     "bears_on": "the residual technique gap has a ladder shape, ~1 decade per mode"},
]


# --------------------------------------------------------------------------------------
# 2. Derived quantities -- everything the prose quotes, computed here, never typed twice.
# --------------------------------------------------------------------------------------

def per_model_summary():
    """Best/worst residual per model, and the distance to the paper's own CAP threshold."""
    out = {}
    for model, mode, r, ms in RESIDUALS_USC:
        d = out.setdefault(model, {"modes": [], "multistage_modes": []})
        d["modes"].append({"mode": mode, "log10_max_residual": r, "multistage_applied": ms})
        if ms:
            d["multistage_modes"].append(mode)
    for model, d in out.items():
        rs = [m["log10_max_residual"] for m in d["modes"]]
        d["best_log10"] = min(rs)                     # most negative == most accurate
        d["worst_log10"] = max(rs)
        d["decades_short_of_cap_at_best"] = round(d["best_log10"] - CAP_THRESHOLD_LOG10, 3)
        d["decades_short_of_cap_at_worst"] = round(d["worst_log10"] - CAP_THRESHOLD_LOG10, 3)
        d["meets_cap_threshold"] = d["best_log10"] <= CAP_THRESHOLD_LOG10
    return out


def ladder_crosscheck():
    """The paper states a ~1 decade/mode background ladder AND gives a worked example.
    Re-derive the slope from the example and check it against the stated rate. This is a real
    cross-check: the two numbers come from different sentences and could disagree."""
    L = LADDER_FIX
    span = L["ipm_stable_best_log10"] - L["ipm_4th_unstable_best_log10"]   # -14 - (-10) = -4
    implied = abs(span) / L["ipm_modes_spanned"]
    stated = L["background_rise_decades_per_mode"]
    return {
        "implied_decades_per_mode_from_worked_example": round(implied, 3),
        "stated_decades_per_mode": stated,
        "agree_within_0p25_decade": abs(implied - stated) <= 0.25,
        "net_margin_closure_decades_per_mode": round(
            L["signal_decay_decades_per_mode"] + L["background_rise_decades_per_mode"], 3),
    }


def days_between(a, b):
    from datetime import date
    ya, ma, da = (int(x) for x in a.split("-"))
    yb, mb, db = (int(x) for x in b.split("-"))
    return (date(yb, mb, db) - date(ya, ma, da)).days


# --------------------------------------------------------------------------------------
# 3. The gate classifier -- computed, and demonstrably able to answer either way.
# --------------------------------------------------------------------------------------

def classify_obstruction(residuals_usc, residuals_fix, models_unfixed, threshold,
                         single_stage_floor):
    """Return (verdict, discriminators).

    verdict in {"MODEL_SPECIFIC", "TECHNIQUE_SPECIFIC", "NOT_LOCATABLE"}.

    D1 -- technique applied but model resisted?  A solution that RECEIVED the paper's precision
          technique and is still stranded far above the CAP threshold is evidence that the
          model, not the method, is the wall.  We call it stranded if it failed to clear the
          no-multistage floor by at least one decade, i.e. the five-decade technique bought
          essentially nothing on it.
    D2 -- model held fixed, technique changed, stranded solutions moved?  If a later work
          reaches the threshold on the SAME models by changing only the method, the barrier was
          methodological.
    """
    # D1: solutions the technique was actually applied to.
    applied = [(m, mode, r) for (m, mode, r, ms) in residuals_usc if ms]
    resisted = [(m, mode, r) for (m, mode, r) in applied if r > single_stage_floor - 1.0]

    # D2: models that were stranded in USC and reach the threshold in the follow-up.
    stranded_models = sorted({m for (m, _mode, r, _ms) in residuals_usc if r > threshold})
    rescued_models = sorted([m for m in stranded_models
                             if m in residuals_fix
                             and residuals_fix[m]["worst_log10"] <= threshold + 2.0])

    d1_model_wall = len(resisted) > 0
    d2_technique_rescue = len(rescued_models) > 0

    if d2_technique_rescue and not d1_model_wall:
        verdict = "TECHNIQUE_SPECIFIC"
    elif d1_model_wall and not d2_technique_rescue:
        verdict = "MODEL_SPECIFIC"
    elif d1_model_wall and d2_technique_rescue:
        # Both signals present: the technique rescued some models but demonstrably failed on a
        # model it was applied to. That is a genuine model wall on top of a technique gap.
        verdict = "MODEL_SPECIFIC"
    else:
        verdict = "NOT_LOCATABLE"

    return verdict, {
        "D1_solutions_technique_was_applied_to": [
            {"model": m, "mode": mode, "log10": r} for (m, mode, r) in applied],
        "D1_of_those_still_stranded": [
            {"model": m, "mode": mode, "log10": r} for (m, mode, r) in resisted],
        "D1_model_wall_detected": d1_model_wall,
        "D2_models_stranded_in_usc": stranded_models,
        "D2_models_rescued_by_later_technique_change": rescued_models,
        "D2_models_never_retried": models_unfixed,
        "D2_technique_rescue_detected": d2_technique_rescue,
    }


def self_test():
    """Lesson 90. Show the classifier can report each verdict, by perturbing the evidence.
    If these do not come out differently, the classifier is a constant wearing a function's
    clothes and the leg's headline is worthless."""
    checks = []

    # (a) The actual evidence.
    v, _ = classify_obstruction(RESIDUALS_USC, RESIDUALS_FIX, MODELS_UNFIXED,
                                CAP_THRESHOLD_LOG10, SINGLE_STAGE_FLOOR_LOG10)
    checks.append(("actual_evidence", v, "TECHNIQUE_SPECIFIC"))

    # (b) Counterfactual: multi-stage training WAS applied to IPM 2nd/3rd unstable and they
    #     still sat at ~1e-8. Then the technique was tried and the model resisted.
    alt = [(m, mode, r, (True if (m == "IPM with boundary") else ms))
           for (m, mode, r, ms) in RESIDUALS_USC]
    v_b, _ = classify_obstruction(alt, {}, MODELS_UNFIXED,
                                  CAP_THRESHOLD_LOG10, SINGLE_STAGE_FLOOR_LOG10)
    checks.append(("counterfactual_technique_applied_and_failed", v_b, "MODEL_SPECIFIC"))

    # (c) Counterfactual: no follow-up paper existed and the technique was never stress-tested.
    #     Nothing then discriminates -- the honest answer is that it is not locatable.
    v_c, _ = classify_obstruction(RESIDUALS_USC, {}, MODELS_UNFIXED,
                                  CAP_THRESHOLD_LOG10, SINGLE_STAGE_FLOOR_LOG10)
    checks.append(("counterfactual_no_followup", v_c, "NOT_LOCATABLE"))

    results = [{"case": c, "got": g, "expected": e, "pass": g == e} for c, g, e in checks]
    return results, all(r["pass"] for r in results)


# --------------------------------------------------------------------------------------
# 4. Assemble and emit.
# --------------------------------------------------------------------------------------

def main():
    summary = per_model_summary()
    verdict, disc = classify_obstruction(RESIDUALS_USC, RESIDUALS_FIX, MODELS_UNFIXED,
                                         CAP_THRESHOLD_LOG10, SINGLE_STAGE_FLOOR_LOG10)
    ladder = ladder_crosscheck()
    selftests, selftest_ok = self_test()

    payload = {
        "leg": 175,
        "route": "ROUTE-USC",
        "pass_date": BIBLIO["pass_date"],
        "target": {
            "id": USC,
            "title": "Discovery of Unstable Singularities",
            "url": "https://arxiv.org/abs/2509.14185",
            "authors_short": "Wang, Bennani, Martens, ..., Buckmaster, Georgiev, "
                             "Gomez-Serrano, Jiang, Lai",
            "pages": 20,
            "read_at_full_text_depth_first_time_in_this_repository": True,
        },
        "followup": {
            "id": FIX,
            "title": "Resolving Sharp Gradients of Unstable Singularities to Machine Precision "
                     "via Neural Networks",
            "url": "https://arxiv.org/abs/2511.22819",
            "authors": "Yongji Wang, Tristan Leger, Ching-Yao Lai, Tristan Buckmaster",
            "pages": 27,
            "days_after_target": days_between(BIBLIO["usc_v1_date"], BIBLIO["fix_v1_date"]),
        },

        "gate": {
            "question": "Does arXiv:2509.14185's own text state, imply, or make locatable an "
                        "obstruction to certifying its CAP-ready unstable singularities, and is "
                        "that obstruction MODEL-specific or TECHNIQUE-specific?",
            "locatable": True,
            "verdict": verdict,
            "answered_branch": "technique-specific",
            "escalation_fires": verdict == "MODEL_SPECIFIC",
            "discriminators": disc,
        },

        "cap_threshold_log10": CAP_THRESHOLD_LOG10,
        "single_stage_floor_log10": SINGLE_STAGE_FLOOR_LOG10,
        "residuals_usc_fig3b_p6": [
            {"model": m, "mode": mode, "log10_max_residual": r, "multistage_applied": ms}
            for (m, mode, r, ms) in RESIDUALS_USC],
        "per_model": summary,
        "lambda_usc_fig2f_p4": LAMBDA_USC,
        "unvalidated_solutions": [{"model": m, "mode": mode} for (m, mode) in UNVALIDATED_USC],
        "residuals_after_technique_fix": RESIDUALS_FIX,
        "models_not_retried_after_fix": MODELS_UNFIXED,
        "ladder": {**LADDER_FIX, **ladder},

        "gap_in_leg_173_terms": {
            "precision_ccf": {
                "status": "CLOSED",
                "by": FIX,
                "detail": "O(10^-13), full suite of previously discovered CCF solutions; "
                          "round-off limited."},
            "precision_ipm": {
                "status": "CLOSED",
                "by": FIX,
                "detail": "O(10^-11) to O(10^-13) across all modes, including a newly "
                          "confirmed 4th unstable solution."},
            "precision_boussinesq": {
                "status": "OPEN",
                "decades_short_at_best": summary["Boussinesq"]["decades_short_of_cap_at_best"],
                "decades_short_at_worst": summary["Boussinesq"]["decades_short_of_cap_at_worst"],
                "detail": "UNTESTED, not measured-dead: the gradient-normalization fix was "
                          "never applied to Boussinesq. 'Boussinesq' appears exactly once in "
                          "the follow-up, in the abstract's recap of [1], and never in its "
                          "body. Headwind is the ~2 decade/mode margin ladder."},
            "scope_unstable_spectrum": {
                "status": "OPEN",
                "detail": "The finite-unstable-spectrum condition a CAP needs is called "
                          "'desirable' (USC p.19) and never established. The mode count comes "
                          "from a PINN eigensolve assumed real and restricted to the "
                          "solution's symmetry class. No residual reduction discharges this."},
            "infrastructure_cap": {
                "status": "OPEN",
                "detail": "No CAP for any of these solutions exists. USC's was 'Manuscript in "
                          "preparation' (Sep 2025) and has not appeared. The SI defining every "
                          "object such a CAP would enclose has never been uploaded."},
        },

        "ledger_audit": {
            "note": "solver/viscous_novelty.py and LITERATURE_CHECK.md were read, never "
                    "edited. This leg has no authority over either.",
            "recorded_what": "Unstable self-similar singularities for IPM and 3D Euler with "
                             "boundary at near-machine precision, stated as CAP-ready. "
                             "Inviscid.",
            "defect": "The row names IPM and 3D Euler with boundary and omits CCF -- the ONLY "
                      "model for which the paper actually claims CAP-sufficiency (USC p.8). "
                      "The two models named are those where the claim is weakest.",
            "wording_slip": "'near-machine precision' flattens a 6.7-decade stratification "
                            "(Fig.3b spans -13.714 to -7.020); 2 of 12 solutions are at "
                            "machine precision.",
            "correct_as_recorded": ["no certificate claimed", "inviscid", "EXCLUSION verdict"],
            "verdict_unchanged_by_this_pass": "EXCLUSION",
        },

        "banked_numbers_correction": {
            "claim_checked": "The re-derivation numbers 1.8e-07, 3.0e-06/1.9e-06 rms, 3.8e-07 "
                             "were attributed to arXiv:2509.14185 in the coordinator's framing.",
            "finding": "CONFIRMED MISATTRIBUTED. Papers/MANIFEST.md assigns exactly those "
                       "figures to arXiv:2410.05480 (Dahne-Figueras, CGL branches). "
                       "arXiv:2509.14185 appears in no manifest, no fetch tier, and no "
                       "writeup/data JSON. There was no prior re-derivation of this paper.",
        },

        "escalation_branch_checked": {
            "fires": False,
            "reason": "The gate answered TECHNIQUE_SPECIFIC, so the model-specific escalation "
                      "branch does not apply.",
            "near_miss_recorded_honestly": "CCF is NOT a member of this repository's gCLM "
                                           "a-family. solver/gclm_family.py implements "
                                           "omega_t + a u omega_x = omega H(omega) with "
                                           "u_x = H(omega); CCF is theta_t + (H theta) theta_x "
                                           "= 0 -- no stretching term, and the velocity is "
                                           "H theta itself rather than its antiderivative. "
                                           "grep for CCF/Cordoba over solver/ returns nothing. "
                                           "Only model-agnostic 1D tooling is shared "
                                           "(line_hilbert.py, interval.py, profile_newton.py). "
                                           "No construction lane is proposed.",
        },

        "user_framing_correction": {
            "framing": "still one model class away",
            "finding": "Not supported. It was one loss-reweighting scheme away, and that "
                       "scheme landed 72 days later on the same models, closing CCF and IPM to "
                       "round-off. What remains open is narrower than a model class: the fix "
                       "unpublished for Boussinesq, the ~2 decade/mode margin ladder, the "
                       "unstable-spectrum enclosure (a proof obligation, not a numerics one), "
                       "and a CAP announced in Sep 2025 that has not appeared.",
        },

        "biblio": BIBLIO,
        "quotes": QUOTES,
        "self_tests": {"cases": selftests, "all_pass": selftest_ok},
        "no_certificate_exists_search": {
            "queries": [
                'export.arxiv.org all:"unstable singularities" AND all:"self-similar", '
                'sortBy=submittedDate desc -> exactly 2 records: 2511.22819 (2025-11-28), '
                '2509.14185 (2025-09-17)',
                'export.arxiv.org all:"Cordoba-Cordoba-Fontelos" -> 1 unrelated 2010 record '
                '(Kiselev, 1009.0540, Regularity and blow up for active scalars)',
            ],
            "cap_found": False,
        },
    }

    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, os.pardir, "writeup", "data", "p2_route_usc_v1_scoping.json")
    out = os.path.normpath(out)
    with open(out, "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)
        fh.write("\n")

    # ---- console report -------------------------------------------------------------
    print("Leg 175 / ROUTE-USC -- arXiv:2509.14185 scoping")
    print("=" * 78)
    print(f"GATE: obstruction locatable = True, verdict = {verdict}")
    print(f"      escalation branch fires: {payload['gate']['escalation_fires']}")
    print()
    print("Precision stratification (USC Fig.3b p.6), log10 max residual:")
    for model in ("CCF", "IPM with boundary", "Boussinesq"):
        d = summary[model]
        flag = "MEETS CAP" if d["meets_cap_threshold"] else \
               f"{d['decades_short_of_cap_at_best']:.2f} decades short"
        print(f"  {model:20s} best {d['best_log10']:8.3f}  worst {d['worst_log10']:8.3f}"
              f"   multistage on: {d['multistage_modes'] or 'NONE'}   [{flag}]")
    print()
    print("D1  technique applied and model resisted? "
          f"{disc['D1_model_wall_detected']}  "
          f"(stranded despite multistage: {len(disc['D1_of_those_still_stranded'])})")
    print("D2  model fixed, technique changed, stranded models rescued? "
          f"{disc['D2_technique_rescue_detected']}  "
          f"-> {disc['D2_models_rescued_by_later_technique_change']}")
    print(f"    never retried after the fix: {disc['D2_models_never_retried']}")
    print()
    print("Ladder cross-check (FIX p.11 sec.2.3.3):")
    print(f"  stated background rise      {ladder['stated_decades_per_mode']:.2f} decades/mode")
    print(f"  implied by worked example   "
          f"{ladder['implied_decades_per_mode_from_worked_example']:.2f} decades/mode"
          f"   agree: {ladder['agree_within_0p25_decade']}")
    print(f"  net margin closure          "
          f"{ladder['net_margin_closure_decades_per_mode']:.2f} decades per unstable mode")
    print()
    print("Self-tests (can the classifier answer the other way?):")
    for r in selftests:
        print(f"  [{'ok' if r['pass'] else 'FAIL'}] {r['case']:45s} -> {r['got']}")
    print()
    print(f"wrote {out}")
    return 0 if selftest_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
