"""Route-XUTRI v1: does Xu arXiv:2607.19762's SPECTRAL-PICTURE framework independently
reproduce a_c = 0.6890665 or alpha(1/2) = 3?  The third-source triangulation, measured.

This repository has two independent derivations of alpha(1/2) = 3 (ALS (49)-(50) integrated
cold, 7.7e-5 relative on c_l -- PHASE2_P2_NOTES J-3; and LSS (35)-(36) as the root of
3p^2 - p = 0, exact -- leg 161 L2), the published LSS a_c = 0.6890665337007457..., and its
own instrument's a_c = 0.693493, recorded as "the worst of three sources" (J-8).

Xu has been read six times (legs 127, 163, 171, 173, 181, 183) for the origin-H^2 citation
and the sec 8 no-go, and his 0.6888 / 0.04% is already banked.  What was never asked is the
PROVENANCE question: WHERE INSIDE XU'S OWN PAPER do these numbers come from -- the spectral
machinery of sec 3 (essential spectrum, gap 1/2, point spectrum {0,1}, Hardy-Mellin
resolvent, Evans determinant) or the profile-continuation of sec 2 -- and is either
independent of LSS/ALS, at what precision?  That is this driver's subject.

  X1  THE SPECTRAL COLUMNS OF TABLE 1 ARE ALGEBRAIC IMAGES OF c_l, MEASURED.  Xu's Table 1
      prints, beside c_l(a), the far-field line 1 - c_l/2 (the essential-spectrum quantity
      of sec 3) and s*(a) = 1/c_l (the sec 6 exponent).  If those columns are exactly
      f(c_l) to the printed digits, then the spectral picture CONSUMES the profile branch
      and contributes no independent determination of anything.  Checked row by row.
      NEGATIVE CONTROL THAT CAN FAIL (lesson 90): the same code path is run against two
      DECOY maps (1 - c_l and 2/c_l) which must NOT reproduce the printed columns.

  X2  XU'S ENDPOINT REPRODUCED FROM XU'S OWN PRINTED BRACKET.  sec 2 states a* ~ 0.6888 by
      "linear interpolation between the computed branch values c_l(0.68) = 0.0185 and
      c_l(0.72) = -0.0659", and claims 0.04% against LSS.  Both the endpoint and the
      percentage are recomputed from those two printed numbers.  This is an internal
      consistency check on the third source that can fail.

  X3  THE 0.04% IS BRACKET-SENSITIVE -- A CONTROL THAT REPORTS A DIFFERENT ANSWER.  Run the
      identical interpolation on a different admissible bracket taken from Xu's OWN Table 1
      (the a = 0.65 row, c_l = 0.0775, against the same c_l(0.72) = -0.0659).  Same code,
      different Xu-printed input, different a*.  If the headline 0.04% moves materially,
      it is a property of the chosen bracket and not a resolved measurement.

  X4  XU'S OWN RESOLUTION, PROPAGATED TO a*.  Xu states a two-grid self-consistency
      |c_l(1024) - c_l(2048)| <~ 5e-4, "a self-consistency measure rather than a certified
      continuum error bound".  Propagated through the local slope dc_l/da of his own
      bracket, that is an uncertainty on a*.  Compared against the 0.04% agreement he
      reports: the question is whether his cross-check RESOLVES a_c or merely fails to
      contradict it.

  X5  alpha(1/2) = 3 IN XU IS CITED, NOT COMPUTED -- AND HIS TABLE ROW IS UNDER-RESOLVED.
      Table 1's caption reads "c_l(1/2) = 1/3 is exact ([20]; also [4, Thm. 2])" and sec 6
      repeats it; the a = 0.5 row is (per sec 2) a degree-6 interpolation of the Newton
      branch, printed as 0.3333.  Measure the gap between the printed row and the exact
      1/3, and compare it to Xu's own 5e-4 resolution: if the gap is far BELOW his
      resolution, the row cannot distinguish a computation from a transcription of the
      cited exact value, and carries no independent information.  Then rank the three
      sources on alpha(1/2) by relative precision.

  X6  THE SPECTRAL DIAGNOSTIC'S OWN OUTPUT AND ITS DOMAIN.  Xu's sec 3.2 Evans-determinant
      continuation returns n_disc(a) = 0 for a in [0, 0.65] -- constant, featureless, and
      stopping short of a_c = 0.689.  Recorded as data: the coverage gap, and the fact that
      a constant integer count carries no location information.

  X7  THE PROVENANCE LEDGER AND THE GATE.  Each constant x each of Xu's two machineries,
      with the verbatim sentence that settles it.

Deterministic, no network, sub-second.  Every number the prose quotes is in the JSON.
Writes writeup/data/p2_route_xutri_v1_lit.json.

Run: .venv/bin/python -u experiments/p2_route_xutri_v1_lit.py
"""

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.literature_gates import LSS_A_C  # noqa: E402

OUT = ROOT / "writeup" / "data" / "p2_route_xutri_v1_lit.json"

# ---------------------------------------------------------------------------
# Constants, each with its locator.  These are TRANSCRIPTIONS from primary text;
# the locator is what makes them auditable.
# ---------------------------------------------------------------------------

# LSS arXiv:2010.01201, abstract p. 1; sec 1 Eq. (8) p. 5; sec 12 p. 43.  Read at primary
# source by leg 161.  This is the reference value all three sources are scored against.
LSS_A_C_FULL = 0.6890665337007457

# This repository's own instrument (PHASE2_P2_NOTES J-8; LITERATURE_CHECK 7th pass item 8).
OURS_A_C = 0.693493

# This repository's cold re-derivation of alpha(1/2) = 3 by integrating ALS (49)-(50)
# (experiments/p2_route_j_v1_literature.py::j3_alpha_half_from_als; PHASE2_P2_NOTES J-3):
# relative error on c_l.  Leg 161's LSS route (L2) is exact and is scored separately.
OURS_ALPHA_HALF_C_L_REL = 7.7e-5

# Xu arXiv:2607.19762v1, sec 2: the two printed branch values that bracket the crossing,
# and the Table 1 row at a = 0.65.
XU_BRACKET_LO_A, XU_BRACKET_LO_CL = 0.68, 0.0185
XU_BRACKET_HI_A, XU_BRACKET_HI_CL = 0.72, -0.0659
XU_TABLE_A065_CL = 0.0775

# Xu sec 2: "the two-grid difference is |c_l(N=1024) - c_l(2048)| <~ 5e-4".
XU_TWO_GRID_CL = 5.0e-4
# Xu sec 1 / sec 2: solution accuracy ~3e-4 at the a = 0 floor; c_l(0) recovered as 1.00024.
XU_A0_SOLUTION_ACCURACY = 3.0e-4
XU_CL_AT_ZERO = 1.00024
# Xu abstract / sec 2 / Figure 1 caption: the headline agreement, as a percentage.
XU_CLAIMED_ENDPOINT = 0.6888
XU_CLAIMED_AGREEMENT_PCT = 0.04

# Xu Table 1, transcribed in full: (a, c_l, far-field 1 - c_l/2, s* = 1/c_l).
# Rows at a = 0.1, 0.3, 0.5, 0.65 are degree-6 interpolations of the Delta_a = 0.04 Newton
# branch (sec 2); the rest are Newton solves.
XU_TABLE_1 = [
    {"a": 0.00, "c_l": 1.0000, "far_field_printed": 0.500, "s_star_printed": 1.000,
     "row_kind": "exact CLM anchor"},
    {"a": 0.10, "c_l": 0.8730, "far_field_printed": 0.564, "s_star_printed": 1.145,
     "row_kind": "degree-6 interpolation"},
    {"a": 0.20, "c_l": 0.7474, "far_field_printed": 0.626, "s_star_printed": 1.338,
     "row_kind": "Newton solve"},
    {"a": 0.30, "c_l": 0.6178, "far_field_printed": 0.691, "s_star_printed": 1.619,
     "row_kind": "degree-6 interpolation"},
    {"a": 0.40, "c_l": 0.4809, "far_field_printed": 0.760, "s_star_printed": 2.079,
     "row_kind": "Newton solve"},
    {"a": 0.50, "c_l": 0.3333, "far_field_printed": 0.833, "s_star_printed": 3.000,
     "row_kind": "degree-6 interpolation"},
    {"a": 0.60, "c_l": 0.1691, "far_field_printed": 0.915, "s_star_printed": 5.914,
     "row_kind": "Newton solve"},
    {"a": 0.65, "c_l": 0.0775, "far_field_printed": 0.961, "s_star_printed": 12.90,
     "row_kind": "degree-6 interpolation"},
]

# Xu sec 3.2, the Evans-determinant continuation.
XU_EVANS_NDISC = 0
XU_EVANS_A_RANGE = (0.0, 0.65)


def _rel(x, ref):
    return abs(x - ref) / abs(ref)


# ---------------------------------------------------------------------------
# X1 -- the spectral columns of Table 1 are algebraic images of c_l
# ---------------------------------------------------------------------------
def x1_spectral_columns_are_images_of_cl():
    """Are Xu's far-field and s* columns exactly f(c_l), to the printed digits?

    The far-field line 1 - c_l/2 is the sec 3 essential-spectrum quantity; s* = 1/c_l is
    the sec 6 exponent.  If both reproduce to the printed precision from c_l alone, the
    spectral picture carries NO input the profile branch did not already supply.

    The decoys are the lesson-90 control: two wrong maps run through the identical
    comparison, which MUST fail to reproduce the columns.
    """
    rows, decoy_rows = [], []
    for r in XU_TABLE_1:
        cl = r["c_l"]
        ff_true, ss_true = 1.0 - cl / 2.0, 1.0 / cl
        # printed to 3 decimals (far field) and to the digits shown (s*)
        ff_dev = abs(round(ff_true, 3) - r["far_field_printed"])
        ss_digits = 2 if r["s_star_printed"] >= 10 else 3
        ss_dev = abs(round(ss_true, ss_digits) - r["s_star_printed"])
        rows.append({"a": r["a"], "c_l": cl, "row_kind": r["row_kind"],
                     "far_field_printed": r["far_field_printed"],
                     "far_field_from_cl": ff_true,
                     "far_field_dev_at_printed_precision": ff_dev,
                     "s_star_printed": r["s_star_printed"],
                     "s_star_from_cl": ss_true,
                     "s_star_dev_at_printed_precision": ss_dev})
        # decoys: same comparison, deliberately wrong maps
        decoy_rows.append({"a": r["a"],
                           "decoy_far_field_1_minus_cl": 1.0 - cl,
                           "decoy_far_field_abs_dev": abs((1.0 - cl) - r["far_field_printed"]),
                           "decoy_s_star_2_over_cl": 2.0 / cl,
                           "decoy_s_star_abs_dev": abs((2.0 / cl) - r["s_star_printed"])})

    worst_ff = max(r["far_field_dev_at_printed_precision"] for r in rows)
    worst_ss = max(r["s_star_dev_at_printed_precision"] for r in rows)
    n_exact = sum(1 for r in rows
                  if r["far_field_dev_at_printed_precision"] == 0.0
                  and r["s_star_dev_at_printed_precision"] == 0.0)
    decoy_worst_ff = max(r["decoy_far_field_abs_dev"] for r in decoy_rows)
    decoy_worst_ss = max(r["decoy_s_star_abs_dev"] for r in decoy_rows)
    control_fired = decoy_worst_ff > 10 * max(worst_ff, 1e-12) and decoy_worst_ss > 1.0

    return {
        "rows": rows, "decoy_rows": decoy_rows,
        "n_rows": len(rows), "n_rows_exact_at_printed_precision": n_exact,
        "worst_far_field_dev": worst_ff, "worst_s_star_dev": worst_ss,
        "decoy_worst_far_field_dev": decoy_worst_ff,
        "decoy_worst_s_star_dev": decoy_worst_ss,
        "negative_control_fired": bool(control_fired),
        "quote_far_field": ("Table 1 caption: 'the focusing exponent c_l(a) ..., the "
                            "far-field-line distance 1 - c_l/2, the exponent "
                            "s*(a) = 1/c_l, and the anchor cross-checks'"),
        "verdict": ("Both of Xu's spectral-side columns are exact algebraic images of the "
                    f"single profile quantity c_l: {n_exact}/{len(rows)} rows reproduce to "
                    "the printed digit with zero deviation, worst deviation "
                    f"{max(worst_ff, worst_ss):.1e}, while the two decoy maps miss by "
                    f"{decoy_worst_ff:.3f} and {decoy_worst_ss:.3f}.  The sec 3 spectral "
                    "picture therefore CONSUMES the sec 2 branch and supplies no "
                    "independent determination of c_l, a_c or alpha."),
    }


# ---------------------------------------------------------------------------
# X2 -- Xu's endpoint, recomputed from Xu's own printed bracket
# ---------------------------------------------------------------------------
def x2_endpoint_from_xus_own_bracket():
    """Reproduce a* ~ 0.6888 and the 0.04% from the two branch values Xu prints."""
    a0, c0 = XU_BRACKET_LO_A, XU_BRACKET_LO_CL
    a1, c1 = XU_BRACKET_HI_A, XU_BRACKET_HI_CL
    a_star = a0 + (a1 - a0) * c0 / (c0 - c1)          # linear interpolation to c_l = 0
    rel = _rel(a_star, LSS_A_C_FULL)
    return {
        "bracket": {"a_lo": a0, "c_l_lo": c0, "a_hi": a1, "c_l_hi": c1},
        "a_star_recomputed": a_star,
        "a_star_as_printed_by_xu": XU_CLAIMED_ENDPOINT,
        "abs_dev_from_xus_printed_endpoint": abs(a_star - XU_CLAIMED_ENDPOINT),
        "rounds_to_xus_printed_endpoint": bool(round(a_star, 4) == XU_CLAIMED_ENDPOINT),
        "lss_a_c_full": LSS_A_C_FULL,
        "rel_err_vs_lss": rel,
        "pct_err_vs_lss": 100.0 * rel,
        "xu_claimed_pct": XU_CLAIMED_AGREEMENT_PCT,
        "claim_consistent": bool(round(100.0 * rel, 2) == XU_CLAIMED_AGREEMENT_PCT),
        "local_slope_dcl_da": (c1 - c0) / (a1 - a0),
        "quote": ("sec 2: 'the computed c_l(a) decreases monotonically from 1 at a = 0 and "
                  "crosses zero at a* ~ 0.6888 (linear interpolation between the computed "
                  "branch values c_l(0.68) = 0.0185 and c_l(0.72) = -0.0659), to be "
                  "compared with the published a_c = 0.6890665 of [4].  The two agree to "
                  "0.04% relative error (Figure 1), which is the one quantitative check on "
                  "the recomputed branch.'"),
        "verdict": (f"Xu's endpoint is internally consistent: his two printed branch values "
                    f"give a* = {a_star:.7f}, which rounds to his printed {XU_CLAIMED_ENDPOINT}, "
                    f"and the relative error against LSS is {100.0 * rel:.3f}%, which rounds "
                    f"to his printed {XU_CLAIMED_AGREEMENT_PCT}%.  The third source's "
                    "arithmetic checks out."),
    }


# ---------------------------------------------------------------------------
# X3 -- the control that reports a different answer (lesson 90)
# ---------------------------------------------------------------------------
def x3_bracket_sensitivity_control():
    """Same interpolation, different Xu-printed bracket -> a different a*.

    Lesson 90: a control that cannot come out differently is not a control.  Here the code
    path is identical and only the input bracket changes -- both brackets are Xu's own
    published numbers -- so if a* moves, the headline 0.04% is a property of the bracket.
    """
    a0, c0 = 0.65, XU_TABLE_A065_CL
    a1, c1 = XU_BRACKET_HI_A, XU_BRACKET_HI_CL
    a_star_alt = a0 + (a1 - a0) * c0 / (c0 - c1)
    rel_alt = _rel(a_star_alt, LSS_A_C_FULL)

    a_star_main = (XU_BRACKET_LO_A + (XU_BRACKET_HI_A - XU_BRACKET_LO_A)
                   * XU_BRACKET_LO_CL / (XU_BRACKET_LO_CL - XU_BRACKET_HI_CL))
    rel_main = _rel(a_star_main, LSS_A_C_FULL)
    spread = abs(a_star_alt - a_star_main)

    # a third bracket, the two widest-separated table rows straddling the crossing
    a2, c2 = 0.60, 0.1691
    a_star_wide = a2 + (a1 - a2) * c2 / (c2 - c1)
    rel_wide = _rel(a_star_wide, LSS_A_C_FULL)

    return {
        "bracket_main": {"a_lo": XU_BRACKET_LO_A, "a_hi": XU_BRACKET_HI_A,
                         "a_star": a_star_main, "pct_err_vs_lss": 100.0 * rel_main},
        "bracket_from_table_a065": {"a_lo": a0, "c_l_lo": c0, "a_hi": a1, "c_l_hi": c1,
                                    "a_star": a_star_alt,
                                    "pct_err_vs_lss": 100.0 * rel_alt},
        "bracket_wide_a060": {"a_lo": a2, "c_l_lo": c2, "a_hi": a1, "c_l_hi": c1,
                              "a_star": a_star_wide,
                              "pct_err_vs_lss": 100.0 * rel_wide},
        "a_star_spread_main_vs_a065": spread,
        "pct_spread": 100.0 * spread / LSS_A_C_FULL,
        "ratio_alt_over_main_pct": (100.0 * rel_alt) / (100.0 * rel_main),
        "control_reports_a_different_answer": bool(spread > 1e-4),
        "verdict": (f"Three admissible brackets, all built from Xu's own published branch "
                    f"values through one code path, put the crossing at {a_star_main:.6f}, "
                    f"{a_star_alt:.6f} and {a_star_wide:.6f} -- a spread of {spread:.2e} in a, "
                    f"i.e. {100.0 * spread / LSS_A_C_FULL:.2f}% of a_c, which is "
                    f"{(100.0 * rel_alt) / (100.0 * rel_main):.1f}x the headline agreement "
                    "when the a = 0.65 bracket is used.  The 0.04% is bracket-dependent, "
                    "not a resolved determination."),
    }


# ---------------------------------------------------------------------------
# X4 -- Xu's own stated resolution, propagated to a*
# ---------------------------------------------------------------------------
def x4_resolution_propagated():
    """Does Xu's cross-check RESOLVE a_c, or merely fail to contradict it?"""
    slope = (XU_BRACKET_HI_CL - XU_BRACKET_LO_CL) / (XU_BRACKET_HI_A - XU_BRACKET_LO_A)
    delta_a_from_two_grid = XU_TWO_GRID_CL / abs(slope)
    delta_a_from_a0_floor = XU_A0_SOLUTION_ACCURACY / abs(slope)
    rel_two_grid = delta_a_from_two_grid / LSS_A_C_FULL
    a_star = (XU_BRACKET_LO_A + (XU_BRACKET_HI_A - XU_BRACKET_LO_A)
              * XU_BRACKET_LO_CL / (XU_BRACKET_LO_CL - XU_BRACKET_HI_CL))
    observed_rel = _rel(a_star, LSS_A_C_FULL)
    resolves = observed_rel > 3.0 * rel_two_grid
    return {
        "xu_two_grid_c_l": XU_TWO_GRID_CL,
        "xu_a0_solution_accuracy": XU_A0_SOLUTION_ACCURACY,
        "xu_c_l_at_zero": XU_CL_AT_ZERO,
        "xu_c_l_at_zero_err_vs_exact_1": abs(XU_CL_AT_ZERO - 1.0),
        "local_slope_dcl_da": slope,
        "implied_delta_a_from_two_grid": delta_a_from_two_grid,
        "implied_delta_a_from_a0_floor": delta_a_from_a0_floor,
        "implied_rel_uncertainty_on_a_star": rel_two_grid,
        "observed_rel_disagreement_with_lss": observed_rel,
        "observed_over_uncertainty": observed_rel / rel_two_grid,
        "cross_check_resolves_a_c": bool(resolves),
        "quote": ("sec 2: 'the two-grid difference is |c_l(N=1024) - c_l(2048)| <~ 5e-4 "
                  "(about three significant figures), a self-consistency measure rather "
                  "than a certified continuum error bound (it can understate the true error "
                  "against the high-precision branch of [4], which at nonzero a agrees only "
                  "to about two or three significant figures ...)'"),
        "verdict": (f"Xu's own two-grid self-consistency of {XU_TWO_GRID_CL:.0e} on c_l, "
                    f"pushed through his local slope dc_l/da = {slope:.3f}, is an "
                    f"uncertainty of {delta_a_from_two_grid:.2e} on a*, i.e. "
                    f"{100.0 * rel_two_grid:.3f}% of a_c.  His observed disagreement with "
                    f"LSS is {100.0 * observed_rel:.3f}%, only "
                    f"{observed_rel / rel_two_grid:.2f}x that -- and his own error bar is "
                    "explicitly NOT a bound and may understate.  The cross-check is "
                    "consistent with LSS but does not resolve a_c: it confirms two or "
                    "three significant figures, which is what he claims for it."),
    }


# ---------------------------------------------------------------------------
# X5 -- alpha(1/2) = 3: cited, not computed; and the row is under-resolved
# ---------------------------------------------------------------------------
def x5_alpha_half_provenance_and_precision():
    exact_cl = 1.0 / 3.0
    row = next(r for r in XU_TABLE_1 if r["a"] == 0.50)
    printed_cl, printed_s = row["c_l"], row["s_star_printed"]
    gap_to_exact = abs(printed_cl - exact_cl)
    ratio_to_resolution = gap_to_exact / XU_TWO_GRID_CL
    under_resolved = gap_to_exact < XU_TWO_GRID_CL

    # relative precision on c_l(1/2) for each of the three sources
    xu_rel = XU_TWO_GRID_CL / exact_cl          # his stated resolution, as a relative figure
    ladder = [
        {"source": "LSS arXiv:2010.01201 (35)-(36), leg 161 L2",
         "route": "root of the scalar equation 3p^2 - p = 0",
         "rel_precision_on_c_l": 0.0, "kind": "exact, closed form"},
        {"source": "ALS arXiv:2207.07548 (49)-(50), this repo J-3",
         "route": "cold integration of the published a = 1/2 pole system",
         "rel_precision_on_c_l": OURS_ALPHA_HALF_C_L_REL, "kind": "numerical"},
        {"source": "Xu arXiv:2607.19762 Table 1 a = 0.5 row",
         "route": "degree-6 interpolation of a Delta_a = 0.04 Newton branch",
         "rel_precision_on_c_l": xu_rel, "kind": "numerical, and CITED as exact"},
    ]
    ranked = sorted(ladder, key=lambda d: d["rel_precision_on_c_l"])
    return {
        "printed_c_l_half": printed_cl, "printed_s_star_half": printed_s,
        "exact_c_l_half": exact_cl,
        "gap_printed_vs_exact": gap_to_exact,
        "xu_two_grid_resolution": XU_TWO_GRID_CL,
        "gap_over_resolution": ratio_to_resolution,
        "row_is_under_resolved": bool(under_resolved),
        "row_kind_per_xu": row["row_kind"],
        "precision_ladder": ladder,
        "ranked_best_to_worst": [d["source"] for d in ranked],
        "xu_rel_precision_on_c_l_half": xu_rel,
        "ours_over_xu_precision_factor": xu_rel / OURS_ALPHA_HALF_C_L_REL,
        "quote_caption": "Table 1 caption: 'c_l(1/2) = 1/3 is exact ([20]; also [4, Thm. 2]).'",
        "quote_sec6": ("sec 6: 'The branch value is tested at a = 1/2, where s* = 3 exactly "
                       "(c_l(1/2) = 1/3 by the exact solution of [20]; also [4, Thm. 2]) ... "
                       "The only quantitative validation of the branch itself is the a_c "
                       "cross-check of Section 2.'"),
        "verdict": (f"Xu does not derive alpha(1/2) = 3: he cites it, twice, from J. Chen "
                    f"[20] and LSS [4, Thm. 2].  His own Table 1 row is a degree-6 "
                    f"interpolation printing c_l = {printed_cl}, which sits "
                    f"{gap_to_exact:.1e} from the exact 1/3 -- "
                    f"{1.0 / ratio_to_resolution:.0f}x BELOW his own {XU_TWO_GRID_CL:.0e} "
                    "resolution, so the row cannot distinguish a computation from a "
                    "transcription of the cited value and carries no independent "
                    f"information.  On alpha(1/2) this repository's cold ALS integration is "
                    f"{xu_rel / OURS_ALPHA_HALF_C_L_REL:.0f}x more precise than Xu's stated "
                    "branch resolution, and leg 161's LSS route is exact.  On this constant "
                    "Xu is the WORST of the three sources -- the mirror image of J-8."),
    }


# ---------------------------------------------------------------------------
# X6 -- what the spectral machinery itself returns, and where it stops
# ---------------------------------------------------------------------------
def x6_spectral_diagnostic_output():
    lo, hi = XU_EVANS_A_RANGE
    gap = LSS_A_C_FULL - hi
    return {
        "evans_n_disc_value": XU_EVANS_NDISC,
        "evans_a_range": [lo, hi],
        "a_c_reference": LSS_A_C_FULL,
        "coverage_gap_to_a_c": gap,
        "coverage_gap_frac_of_a_c": gap / LSS_A_C_FULL,
        "diagnostic_is_constant_over_range": True,
        "n_distinct_values_reported": 1,
        "quote_result": ("sec 3.2: 'On the parameter values we ran it returns n_disc(a) = 0 "
                         "for a in [0, 0.65]; we report this as exploratory evidence only.'"),
        "quote_status": ("sec 3.2: 'This strand is exploratory: the computation records a "
                         "per-point phase-increment and integer-defect diagnostic and "
                         "anchors the a = 0 value to the proven empty strip of Theorem 2, "
                         "but it does not enforce these diagnostics as hard gates, and its "
                         "run outputs are not retained.'"),
        "quote_gap": ("sec 1: 'beyond a = 0 the discrete exclusion rests on numerical "
                      "evidence at the sampled advections (Section 3.2)'"),
        "verdict": (f"The one spectral computation Xu runs across the advection branch "
                    f"returns the single constant integer {XU_EVANS_NDISC} over "
                    f"[{lo}, {hi}], is declared exploratory with three recorded gaps and "
                    "unretained outputs, and stops "
                    f"{gap:.4f} short of a_c ({100.0 * gap / LSS_A_C_FULL:.1f}% of the way "
                    "to it).  A constant carries no location information; nothing in the "
                    "spectral machinery locates a_c even in principle as run."),
    }


# ---------------------------------------------------------------------------
# X7 -- the provenance ledger and the gate
# ---------------------------------------------------------------------------
def x7_provenance_ledger():
    ledger = [
        {"constant": "a_c = 0.6890665",
         "xu_machinery": "spectral picture (sec 3: essential spectrum, gap 1/2, point "
                         "spectrum {0,1}, Hardy-Mellin resolvent, sec 3.2 Evans determinant)",
         "produces_it": False,
         "why": ("The spectral objects are functions of (Omega, c_l), which sec 2 supplies; "
                 "Table 1's far-field column is exactly 1 - c_l/2 (X1).  The only "
                 "branch-wide spectral computation returns a constant integer over "
                 "[0, 0.65] and never reaches a_c (X6)."),
         "quote": ("sec 1: 'We recompute c_l(a) independently ... to supply the operator "
                   "coefficients (Omega, c_l) that Proposition 1 and the exponent s* below "
                   "need at a > 0'")},
        {"constant": "a_c = 0.6890665",
         "xu_machinery": "profile continuation (sec 2: Newton continuation on a "
                         "compactified real-line grid)",
         "produces_it": True,
         "why": ("Genuinely independent of LSS -- started from the exact a = 0 CLM anchor "
                 "and stepped up in Delta_a = 0.04, using no LSS data -- and lands at "
                 "a* ~ 0.6888, 0.043% from LSS (X2).  But it is a profile-equation solve, "
                 "the same KIND of object as this repository's own instrument, not "
                 "spectral-gap machinery; it is bracket-dependent (X3) and does not resolve "
                 "a_c beyond two or three significant figures (X4)."),
         "quote": ("sec 2: 'we take theirs as the reference; the recomputation here is an "
                   "independent lower-order cross-check'")},
        {"constant": "alpha(1/2) = 3",
         "xu_machinery": "spectral picture (sec 3) and the sec 6 exponent s*(a) = 1/c_l",
         "produces_it": False,
         "why": ("s* is defined AS 1/c_l (Eq. (6.3)) -- an algebraic image of the profile "
                 "branch, verified exactly against every Table 1 row (X1) -- and Xu calls "
                 "it a formal scaling diagnostic, not a threshold."),
         "quote": ("sec 6.1: 's* is a formal scaling (dissipation-relevance) threshold read "
                   "off the self-similar exponent ... and s* is not the sharp critical "
                   "dissipation curve separating blow-up from global regularity, which for "
                   "this family remains unknown.'")},
        {"constant": "alpha(1/2) = 3",
         "xu_machinery": "profile continuation (sec 2 branch, Table 1 a = 0.5 row)",
         "produces_it": False,
         "why": ("Cited, not derived: the value is attributed to [20] and [4, Thm. 2] in "
                 "both the Table 1 caption and sec 6.  The interpolated row printing 0.3333 "
                 "sits 15x below Xu's own resolution and so carries no independent "
                 "information (X5)."),
         "quote": ("sec 6: 'The only quantitative validation of the branch itself is the "
                   "a_c cross-check of Section 2.'")},
    ]
    return {
        "ledger": ledger,
        "n_cells": len(ledger),
        "n_cells_producing": sum(1 for c in ledger if c["produces_it"]),
        "spectral_cells_producing": sum(1 for c in ledger
                                        if c["produces_it"] and "spectral" in c["xu_machinery"]),
        "materially_different_value_found": False,
        "verdict": ("Four cells (two constants x two machineries).  Exactly one produces a "
                    "number, and it is the non-spectral one: sec 2's profile continuation "
                    "on a_c.  Zero spectral cells produce either constant."),
    }


def main():
    t0 = time.time()
    out = {
        "leg": 189, "route": "ROUTE-XUTRI",
        "paper": "Xu, arXiv:2607.19762v1 [physics.flu-dyn], 22 Jul 2026",
        "paper_url": "https://arxiv.org/abs/2607.19762",
        "read_at": "full text, pdftotext -layout of the fetched PDF (Papers/ is gitignored)",
        "reference_values": {
            "lss_a_c_full": LSS_A_C_FULL,
            "lss_a_c_stored_here": LSS_A_C,
            "ours_a_c": OURS_A_C,
            "ours_a_c_pct_err": 100.0 * _rel(OURS_A_C, LSS_A_C_FULL),
            "ours_alpha_half_c_l_rel": OURS_ALPHA_HALF_C_L_REL,
        },
        "X1_spectral_columns_are_images_of_cl": x1_spectral_columns_are_images_of_cl(),
        "X2_endpoint_from_xus_own_bracket": x2_endpoint_from_xus_own_bracket(),
        "X3_bracket_sensitivity_control": x3_bracket_sensitivity_control(),
        "X4_resolution_propagated": x4_resolution_propagated(),
        "X5_alpha_half_provenance_and_precision": x5_alpha_half_provenance_and_precision(),
        "X6_spectral_diagnostic_output": x6_spectral_diagnostic_output(),
        "X7_provenance_ledger": x7_provenance_ledger(),
    }

    x2, x4, x5, x7 = (out["X2_endpoint_from_xus_own_bracket"],
                      out["X4_resolution_propagated"],
                      out["X5_alpha_half_provenance_and_precision"],
                      out["X7_provenance_ledger"])
    out["gate_question"] = (
        "does Xu's spectral-picture framework, applied to its own stated spectral data "
        "(not borrowed from ALS/LSS), reproduce a_c=0.6890665 and/or alpha(1/2)=3 to a "
        "precision comparable to this repository's existing re-derivations, using only "
        "techniques Xu's own paper states?")
    out["gate_answer"] = "NO -- and NOT materially different: null result, not a discrepancy"
    out["gate_branch_taken"] = ("no (Xu's framework doesn't bear on either constant) -> "
                                "report clearly, bank as closing the triangulation question "
                                "with a null result, not a discrepancy.  No escalation: no "
                                "materially different value exists.  literature_gates.py is "
                                "NOT touched -- the yes-branch does not apply.")
    out["gate_verdict"] = (
        "NO, on both constants, and for two different reasons.  (a) Xu's SPECTRAL machinery "
        "produces neither: its two branch-wide outputs are algebraic images of the profile "
        "quantity c_l -- the far-field line is exactly 1 - c_l/2 and s* is exactly 1/c_l, "
        f"reproduced with zero deviation on "
        f"{out['X1_spectral_columns_are_images_of_cl']['n_rows_exact_at_printed_precision']}"
        f"/{out['X1_spectral_columns_are_images_of_cl']['n_rows']} Table 1 rows while two "
        "decoy maps miss by 0.4-6 -- and its one branch-wide spectral computation returns a "
        "constant integer over [0, 0.65], declared exploratory, stopping short of a_c.  "
        "(b) Xu's NON-spectral sec 2 Newton continuation does independently recompute a_c, "
        f"landing at {x2['a_star_recomputed']:.7f}, {x2['pct_err_vs_lss']:.3f}% from LSS -- "
        "but Xu himself calls it 'an independent lower-order cross-check' against LSS as "
        f"'the reference', it is bracket-dependent, and his own resolution admits only "
        f"{x4['observed_over_uncertainty']:.2f}x margin over the observed disagreement, so "
        "it confirms two-to-three significant figures rather than resolving the constant.  "
        "On alpha(1/2) = 3 Xu is explicit that he CITES the value from J. Chen [20] and LSS "
        "[4, Thm. 2] and that 'the only quantitative validation of the branch itself is the "
        "a_c cross-check'; his interpolated Table 1 row is "
        f"{1.0 / x5['gap_over_resolution']:.0f}x under-resolved against his own error bar.  "
        "NO MATERIALLY DIFFERENT VALUE EXISTS ON EITHER CONSTANT, so there is no three-way "
        "disagreement and nothing to escalate.")
    out["what_this_changes"] = (
        "The 'worst of three sources' framing (J-8) survives on the NUMBER and is narrowed "
        "on the STRUCTURE: the third source is a self-declared lower-order cross-check "
        "against LSS, not a structurally independent derivation, and it is non-spectral.  "
        "So a_c has ONE primary determination (LSS) plus two lower-order replications of the "
        "same profile equation (Xu's, 0.043%; this repository's, 0.64%), not three "
        "independent sources.  On alpha(1/2) = 3 the ordering INVERTS: this repository's two "
        "derivations (LSS (35)-(36) exact; ALS (49)-(50) at 7.7e-5) are both stronger than "
        "Xu, who cites rather than computes it.")
    out["runtime_s"] = time.time() - t0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=False))

    x1, x3, x6 = (out["X1_spectral_columns_are_images_of_cl"],
                  out["X3_bracket_sensitivity_control"],
                  out["X6_spectral_diagnostic_output"])
    print("=== Route-XUTRI v1: is Xu a third INDEPENDENT source? ===")
    print(f"X1 spectral columns = f(c_l):  "
          f"{x1['n_rows_exact_at_printed_precision']}/{x1['n_rows']} rows exact; "
          f"decoys miss by {x1['decoy_worst_far_field_dev']:.3f} / "
          f"{x1['decoy_worst_s_star_dev']:.3f}  "
          f"[control fired: {x1['negative_control_fired']}]")
    print(f"X2 endpoint from Xu's bracket: a* = {x2['a_star_recomputed']:.7f}  "
          f"({x2['pct_err_vs_lss']:.3f}% vs LSS; Xu prints "
          f"{x2['a_star_as_printed_by_xu']} / {x2['xu_claimed_pct']}%)  "
          f"[consistent: {x2['claim_consistent']}]")
    print(f"X3 bracket control:            spread {x3['a_star_spread_main_vs_a065']:.2e} in a "
          f"= {x3['pct_spread']:.2f}% of a_c  "
          f"[reports differently: {x3['control_reports_a_different_answer']}]")
    print(f"X4 Xu's own resolution:        delta_a = "
          f"{x4['implied_delta_a_from_two_grid']:.2e}; observed/uncertainty = "
          f"{x4['observed_over_uncertainty']:.2f}x  "
          f"[resolves a_c: {x4['cross_check_resolves_a_c']}]")
    print(f"X5 alpha(1/2):                 CITED from [20]/[4]; row under-resolved by "
          f"{1.0 / x5['gap_over_resolution']:.0f}x; ours is "
          f"{x5['ours_over_xu_precision_factor']:.0f}x more precise")
    print(f"X6 spectral diagnostic:        n_disc = {x6['evans_n_disc_value']} constant on "
          f"{x6['evans_a_range']}, stops {x6['coverage_gap_to_a_c']:.4f} short of a_c")
    print(f"X7 provenance ledger:          {x7['n_cells_producing']}/{x7['n_cells']} cells "
          f"produce a number; spectral cells producing: "
          f"{x7['spectral_cells_producing']}")
    print()
    print(f"GATE: {out['gate_answer']}")
    print(f"wrote {OUT.relative_to(ROOT)}  ({out['runtime_s']:.2f} s)")


if __name__ == "__main__":
    main()
