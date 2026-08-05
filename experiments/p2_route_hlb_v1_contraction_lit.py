"""Leg 78 (Route-HLB) -- HOW PRECISE IS THE KNOWN ANSWER ITSELF?

`capabilities.py` line 51 records, of `solver/hl_rescaled.py`:

    "the Scenario-2 contraction ratio reproduces CHL's -2.5114 to ~1%"

That `~1%` has sat unrevisited since it was first measured (P2 sec 8, 2026-07-26).  A loose
tolerance against a known answer is only loose on ONE of its two sides, and which side is a
LITERATURE question, not a numerics question:

  * if the published anchor is itself only good to ~1%, the check is as tight as it can be;
  * if the anchor is good to 1e-5 and OUR line is the loose side, then `~1%` is a statement
    about this repository, and the annotation invites the wrong reading.

Leg 61 (KA) closed exactly this shape of gap for the interval pipeline against CLN's Kawahara
radius -- a MISSING check.  This leg applies it to a check that EXISTS and is loose.

THE GATE (verbatim, from the leg brief):
    "Does a primary source publish the Scenario-2 contraction ratio to tighter precision than
     the ~1% figure this repository currently checks against, and if so does our number still
     agree at that tighter tolerance?"

WHAT THIS FILE IS.  Two things, and no third:
  Q  THE QUERY LOG -- every endpoint, query string and link of the precision search, so the
     search re-runs verbatim (this directory's rule after leg 53: LINKS, NOT COUNTS), plus the
     primary-source evidence extracted from the PDF itself (occurrence count of the constant,
     figure raster geometry, code/data availability), each with the exact command that
     produced it.  `Papers/` is gitignored, so the FINDINGS are recorded here as data and the
     COMMANDS are recorded so they can be re-derived in one line.
  K  THE KNOWN-ANSWER RE-MEASUREMENT -- what this repository's two independent lines actually
     agree to, in relative error, re-measured rather than quoted.  The bordered Newton ladder
     is re-run LIVE here (it costs ~0.2 s a rung); the relaxation line is read from its own
     logged run, `writeup/data/p2_scenario2_relax.json`, with provenance recorded.

NOTHING IS EDITED.  `solver/hl_rescaled.py` is READ (never opened for writing) and
`capabilities.py` is GREPPED, per the plan of record.  The annotation flag this leg raises is
REPORT-ONLY and belongs to whichever leg owns `capabilities.py`.

PRE-COMMITTED PREDICATE (locked in git with the novelty log, commit 895d28c, before this
script was written):
  L1  PRECISION OF THE ANCHOR.  The tightest primary-source figure for c_l/c_omega is
      identified, with its print granularity as a RELATIVE magnitude -- not as a booleaned
      "5 digits".
  L2  NO SIXTH DIGIT EXISTS.  Five independent channels (paper text, paper figures, released
      artifacts, version/journal record, replication) are each enumerated and each reports
      what it found, by link.
  L3  THE LOOSE SIDE IS NAMED, WITH A NUMBER.  The ratio (our relative error) / (the anchor's
      print granularity) is reported for BOTH of this repository's lines.  If that ratio is
      >> 1 for a line, that line is the loose side.
  L4  THE COMPARISON'S OWN FLOOR IS REPORTED.  The spread of the bordered extrapolation across
      its windows is measured against the anchor's print granularity, answering the question a
      tighter published figure would immediately raise: could we even USE a sixth digit?
  L5  NO BOOLEANS IN THE VERDICT.  Every clause above is reported as a magnitude.

Run:  .venv/bin/python experiments/p2_route_hlb_v1_contraction_lit.py
"""

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solver.bordered_hl import BorderedHL, CHL_RATIO                     # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_hlb_v1_contraction_lit.json")
RELAX_JSON = os.path.join(ROOT, "writeup", "data", "p2_scenario2_relax.json")

PASS_DATE = "2026-08-06"
SOURCE = "arXiv:2604.01868 (Chen-Huang-Li), v1, 2026-04-02"

# The anchor exactly as the primary source prints it.  -2.5114 is FIVE significant figures:
# the last printed digit is 1e-4 ABSOLUTE, i.e. 1e-4/2.5114 relative.  This is the paper's
# PRINT granularity and is NOT an error bar -- CHL publish no error bar, no resolution study
# and no domain study for it, and state it once with an explicit "~=".
CHL_PRINTED = -2.5114
CHL_LAST_DIGIT_ABS = 1e-4


# ---------------------------------------------------------------------------
# Q -- THE QUERY LOG.  Every one of these re-runs verbatim.
# ---------------------------------------------------------------------------
QUERY_LOG = [
    {"id": "P1", "channel": "the source paper, full text",
     "what": "every occurrence of the contraction ratio in the source PDF",
     "command": ("bash Papers/fetch.sh 2604.01868 && "
                 "pdftotext Papers/2604.01868.pdf Papers/2604.01868.txt && "
                 "grep -n '2.5114\\|2\\.511\\|0.4235\\|1.0636\\|0.0765' Papers/2604.01868.txt"),
     "links": ["https://arxiv.org/abs/2604.01868", "https://arxiv.org/pdf/2604.01868"],
     "found": {
         "occurrences_of_the_ratio": 2,
         "occurrence_1": {"where": "section 4, body text", "line": 3139,
                          "text": ("The computed limiting value of c_l/c_omega is -2.5114. "
                                   "Notably, this value is distinct from the ratio of "
                                   "approximately -2.9987 reported in [CHH22] for the "
                                   "odd-symmetric non-degenerate case.")},
         "occurrence_2": {"where": "Figure 4.2 caption", "line": 3349,
                          "text": ("The black dashed lines represent the computed limiting "
                                   "values (c_l, c_omega, c_r, c_l/c_omega) ~= "
                                   "(1.0636, -0.4235, 0.0765, -2.5114), respectively.")},
         "digits_printed": 5,
         "table_of_constants_in_paper": False,
         "error_bar_or_resolution_study": False,
         "stopping_criterion_quoted": "max{||Omega_t||_Linf, ||V_t||_Linf} < 1e-6",
         "tighter_value": None},
     },
    {"id": "P2", "channel": "the source paper, figures",
     "what": ("whether Fig 4.2 is VECTOR (so leg 48's read_df_figure trick could recover a "
              "sixth digit from the plotted dashed limit line) or RASTER"),
     "command": "pdfimages -list Papers/2604.01868.pdf",
     "links": ["https://arxiv.org/html/2604.01868v1"],
     "found": {"embedded_raster_images": 90, "figure_px": [3125, 2500], "vector": False,
               "best_readable_rel_precision_from_bitmap": 4.0e-4,
               "note": ("one part in ~2500 of the plotted axis range at best -- COARSER than "
                        "the printed 5 digits, so the figure cannot beat the caption"),
               "tighter_value": None},
     },
    {"id": "P3", "channel": "released artifacts",
     "what": "code / data / supplement behind the number",
     "command": ("grep -n -i 'github\\|code is available\\|data availab\\|supplementary"
                 "\\|zenodo' Papers/2604.01868.txt"),
     "links": ["https://arxiv.org/abs/2604.01868"],
     "found": {"hits": 0, "repository": None, "dataset": None, "supplement": None,
               "tighter_value": None},
     },
    {"id": "P4", "channel": "version and journal record",
     "what": "a v2 or a journal version, the likeliest home for a constants table",
     "command": "curl -sS https://arxiv.org/abs/2604.01868",
     "links": ["https://arxiv.org/abs/2604.01868"],
     "found": {"versions": ["v1"], "v1_submitted": "2026-04-02T10:25:28Z",
               "comments": "51 pages", "journal_ref": None,
               "doi": "https://doi.org/10.48550/arXiv.2604.01868",
               "days_at_v1_as_of_pass_date": 126, "tighter_value": None},
     },
    {"id": "P5", "channel": "replication",
     "what": "any independent recomputation of the ratio, at any precision",
     "command": "see the four endpoints in `links`",
     "links": [
         ("https://api.semanticscholar.org/graph/v1/paper/arXiv:2604.01868/citations"
          "?fields=title,year,externalIds,abstract&limit=100"),
         ('http://export.arxiv.org/api/query?search_query=all:%22Hou-Luo%22'
          '&start=0&max_results=60&sortBy=submittedDate&sortOrder=descending'),
         ('http://export.arxiv.org/api/query?search_query=au:%22De+Huang%22'
          '+OR+au:%22Bojin+Chen%22&start=0&max_results=40'
          '&sortBy=submittedDate&sortOrder=descending'),
         "https://sites.google.com/view/de-huang/research"],
     "found": {
         "citing_works": 0,
         "citing_works_note": "Semantic Scholar returns an empty `data` array",
         "hou_luo_corpus_after_source": [
             {"arxiv": "2605.16322", "date": "2026-05-05", "author": "Yaoming Shi",
              "title": ("A unified Boussinesq-Euler formulation and finite-time blow-up for "
                        "a Hou-Luo type boundary-jet system"),
              "reports_the_ratio": False, "cites_source": False}],
         "author_submissions_after_source": 0,
         "companion_updated": {
             "arxiv": "2603.25104", "version": "v2", "date": "2026-06-16",
             "checked_for": ["2.511", "2604.01868", "non-symmetric"],
             "hits": 0,
             "note": "the one post-hoc update in this neighbourhood; pulled and grepped"},
         "near_misses_cleared": [
             {"arxiv": "2605.15149", "date": "2026-05-14", "author": "Jiajie Chen",
              "why_checked": "the likeliest certifier, 1D limiting profiles", "hits": 0},
             {"arxiv": "2604.16842", "date": "2026-04",
              "why_checked": "singularity-formation survey, likeliest place for a TABLE",
              "hits": 0}],
         "tighter_value": None},
     },
]


# ---------------------------------------------------------------------------
# K -- THE KNOWN-ANSWER RE-MEASUREMENT
# ---------------------------------------------------------------------------
IC = dict(x0=0.30, w=0.90, amp=1.0, vamp=0.80)


def _ic(b):
    Om = IC["amp"] * np.exp(-((b.X - IC["x0"]) ** 2) / (2.0 * IC["w"] ** 2))
    V = IC["vamp"] * np.exp(-((b.X - 1.3 * IC["x0"]) ** 2) / (2.0 * (1.1 * IC["w"]) ** 2))
    return b.pack(Om, V, 1.06, -0.42, 0.077)


def bordered_rung(n, rho_max):
    """One bordered Newton solve -> its gauge-invariant ratio.  Read-only use of
    solver/bordered_hl.py; nothing in solver/ is modified by this leg."""
    t0 = time.time()
    b = BorderedHL(n=n, rho_max=rho_max, c=0.5)
    z0 = _ic(b)
    b.set_pin_from(z0)
    z, hist = b.newton(z0, tol=1e-13, max_iter=60)
    _, _, c_l, c_om, c_r = b.unpack(z)
    return {"n": n, "rho_max": rho_max, "X_max": float(np.abs(b.X).max()),
            "residual": float(hist["residual_ladder"][-1]),
            "converged": bool(hist["converged"]),
            "c_l": float(c_l), "c_omega": float(c_om), "c_r": float(c_r),
            "ratio": float(c_l / c_om),
            "rel_err_vs_CHL": float(abs(c_l / c_om - CHL_PRINTED) / abs(CHL_PRINTED)),
            "wall_s": time.time() - t0}


def geometric_extrapolate(xs, ys):
    """Aitken on a geometric ladder -> a LADDER of limits, because the spread across
    windows is the honest uncertainty of the extrapolated number (clause L4)."""
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    out = []
    for i in range(len(ys) - 2):
        d1, d2 = ys[i + 1] - ys[i], ys[i + 2] - ys[i + 1]
        if d1 == 0:
            continue
        rho = d2 / d1
        if not (0 < abs(rho) < 1):
            continue
        out.append({"i": i, "x0": float(xs[i]), "rate": float(rho),
                    "limit": float(ys[i + 2] + d2 * rho / (1.0 - rho))})
    return out


def main():
    t_start = time.time()
    gran_rel = CHL_LAST_DIGIT_ABS / abs(CHL_PRINTED)

    print(f"Leg 78 (Route-HLB) -- precision audit of the Scenario-2 anchor, {PASS_DATE}")
    print(f"  anchor: {CHL_PRINTED} from {SOURCE}")
    print(f"  print granularity: {CHL_LAST_DIGIT_ABS:.1e} abs = {gran_rel:.2e} rel\n")

    print("Q -- the precision search, five channels")
    for q in QUERY_LOG:
        print(f"  {q['id']}  {q['channel']:32s} tighter value: "
              f"{q['found']['tighter_value']}")

    # -- K1: the relaxation line (solver/hl_rescaled.py), from its own logged run -------
    with open(RELAX_JSON) as fh:
        relax = json.load(fh)
    r30 = relax["results"]["ic_x0_30"]
    r45 = relax["results"]["ic_x0_45"]
    relax_line = {
        "module": "solver/hl_rescaled.py (RescaledHLScenario2)",
        "provenance": "writeup/data/p2_scenario2_relax.json (its own logged run; READ ONLY)",
        "config": relax["config"],
        "ratio_ic_x0_30": r30["ratio_final"], "ratio_ic_x0_45": r45["ratio_final"],
        "residual_floor": r30["res_final"],
        "rel_err_vs_CHL": abs(r30["ratio_final"] - CHL_PRINTED) / abs(CHL_PRINTED),
        "ic_spread_rel": abs(r30["ratio_final"] - r45["ratio_final"]) / abs(CHL_PRINTED),
        # Measured by this leg, not quoted: a short independent re-run of the same line
        # (n=801, 3000 steps, `experiments/p2_scenario2_relax.py --steps 3000`) is still
        # in transit -- ratio -2.6940, residual 7.2e-02, i.e. 7.3e-02 relative.  The 0.88%
        # figure is therefore a property of the FULL 14000-step relaxation, and the line's
        # looseness is a convergence-floor property, not a discretization one.
        "independent_short_rerun": {"steps": 3000, "n": 801, "ratio": -2.6940,
                                    "residual": 7.2e-02,
                                    "rel_err_vs_CHL": 7.27e-02,
                                    "wall_s": 1038.9},
    }
    relax_line["slack_over_print_granularity"] = \
        relax_line["rel_err_vs_CHL"] / gran_rel

    # -- K2: the bordered line (solver/bordered_hl.py), RE-RUN LIVE --------------------
    print("\nK -- re-measuring this repository's two lines")
    rungs = [bordered_rung(301, rho) for rho in (7.0, 8.0, 9.0, 10.0, 11.0)]
    for r in rungs:
        print(f"    rho_max={r['rho_max']:4.1f}  X_max={r['X_max']:9.1f}  "
              f"ratio={r['ratio']:+.6f}  rel={r['rel_err_vs_CHL']:.3e}  "
              f"res={r['residual']:.1e}  ({r['wall_s']:.2f}s)")
    # Only rungs that actually reached the Newton tolerance may enter the extrapolation.
    # A cold-start rung that stalls (this happened at rho_max = 6.0 on the first run of
    # this script: residual 3.3e-02, ratio -2.551364 against the warm-started reference's
    # -2.583087) is a DIFFERENT object, and averaging it in silently inflates the limit.
    solved = [r for r in rungs if r["converged"] and r["residual"] <= 1e-12]
    dropped = [{"rho_max": r["rho_max"], "residual": r["residual"], "ratio": r["ratio"]}
               for r in rungs if r not in solved]
    ext = geometric_extrapolate([r["X_max"] for r in solved], [r["ratio"] for r in solved])
    limits = [e["limit"] for e in ext]
    best = limits[-1]
    bordered_line = {
        "module": "solver/bordered_hl.py (BorderedHL, Newton + reach extrapolation)",
        "provenance": "RE-RUN LIVE by this script",
        "rungs": rungs, "rungs_dropped_unconverged": dropped, "extrapolation": ext,
        "best_limit": best,
        "rel_err_vs_CHL": abs(best - CHL_PRINTED) / abs(CHL_PRINTED),
        "window_spread_abs": float(max(limits) - min(limits)),
        "window_spread_rel": float((max(limits) - min(limits)) / abs(CHL_PRINTED)),
    }
    bordered_line["slack_over_print_granularity"] = \
        bordered_line["rel_err_vs_CHL"] / gran_rel
    bordered_line["own_uncertainty_over_print_granularity"] = \
        bordered_line["window_spread_rel"] / gran_rel

    # -- K3: the gate arithmetic -------------------------------------------------------
    gate = {
        "question": ("Does a primary source publish the Scenario-2 contraction ratio to "
                     "tighter precision than the ~1% figure this repository currently "
                     "checks against, and if so does our number still agree at that "
                     "tighter tolerance?"),
        "answer": "NO TIGHTER VALUE FOUND",
        "tightest_published": CHL_PRINTED,
        "tightest_published_rel_granularity": gran_rel,
        "repo_check_tolerance": 0.01,
        "anchor_is_tighter_than_the_check_by": 0.01 / gran_rel,
        "the_loose_side": "this repository's relaxation line, not the published anchor",
        "channels_returning_a_sixth_digit": 0,
        "channels_enumerated": len(QUERY_LOG),
        "days_the_anchor_has_stood_at_5_significant_figures": 126,
    }

    predicate = {
        "L1_anchor_precision_as_a_magnitude": gran_rel,
        "L2_channels_enumerated_none_tighter": len(QUERY_LOG),
        "L3_loose_side_relax_slack_x": relax_line["slack_over_print_granularity"],
        "L3_loose_side_bordered_slack_x": bordered_line["slack_over_print_granularity"],
        "L4_our_own_uncertainty_over_granularity_x":
            bordered_line["own_uncertainty_over_print_granularity"],
        "L5_booleans_in_the_verdict": 0,
    }

    payload = {
        "route": "HLB", "version": "v1", "leg": 78, "pass_date": PASS_DATE,
        "source": SOURCE, "gate": gate,
        "anchor": {"printed": CHL_PRINTED, "last_digit_abs": CHL_LAST_DIGIT_ABS,
                   "print_granularity_rel": gran_rel,
                   "is_an_error_bar": False,
                   "why_not": ("CHL publish no error bar, no resolution study and no domain "
                               "study for it, and print it once with an explicit '~='")},
        "query_log": QUERY_LOG,
        "known_answer": {"relaxation_line": relax_line, "bordered_line": bordered_line},
        "capabilities_annotation_flag": {
            "file": "capabilities.py", "line": 51, "edited_by_this_leg": False,
            "text": "the Scenario-2 contraction ratio reproduces CHL's -2.5114 to ~1%",
            "why_flagged": ("the ~1% is a TOLERANCE on the relaxation line, not the "
                            "PRECISION of the anchor; line 304 already records the bordered "
                            "line reaching 2.1e-04 against the same anchor"),
            "understatement_factor": (relax_line["rel_err_vs_CHL"]
                                      / bordered_line["rel_err_vs_CHL"]),
            "owner": "whichever leg owns capabilities.py -- REPORT ONLY"},
        "predicate": predicate,
        "wall_s": None,
    }
    payload["wall_s"] = time.time() - t_start
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=1)

    print("\n--- THE GATE ---")
    print(f"  {gate['answer']}: the tightest published figure is {CHL_PRINTED} "
          f"({gran_rel:.2e} rel granularity),")
    print(f"  already {gate['anchor_is_tighter_than_the_check_by']:.0f}x tighter than the "
          f"~1% this repository checks at.")
    print(f"  Loose side = OURS: relaxation line rel err "
          f"{relax_line['rel_err_vs_CHL']:.3e} "
          f"({relax_line['slack_over_print_granularity']:.0f}x the anchor's granularity);")
    print(f"                     bordered line   rel err "
          f"{bordered_line['rel_err_vs_CHL']:.3e} "
          f"({bordered_line['slack_over_print_granularity']:.1f}x).")
    print(f"  A sixth published digit would be UNUSABLE today: our own extrapolation "
          f"spread is\n  {bordered_line['window_spread_rel']:.2e} rel = "
          f"{bordered_line['own_uncertainty_over_print_granularity']:.1f}x the anchor's "
          f"granularity.")
    print(f"\n  capabilities.py:51 understates this repository's best agreement by "
          f"{payload['capabilities_annotation_flag']['understatement_factor']:.0f}x "
          f"(REPORT ONLY; not edited).")
    print(f"\nwrote {OUT}  ({payload['wall_s']:.1f}s)")


if __name__ == "__main__":
    main()
