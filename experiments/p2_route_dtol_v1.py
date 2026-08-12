"""Route-DTOL v1 (leg 386) — the delta mode, PRE-REGISTERED and measured fresh.

Runs the leg-386 pre-registration (`experiments/journal/leg_386.md` PART I, committed in
caf48e8 BEFORE this file existed) against `solver/dssp_decay_enclosure.py`, and writes the
curated result to `writeup/data/p2_route_dtol_v1.json`.

    .venv/bin/python experiments/p2_route_dtol_v1.py

WHAT IS BEING MEASURED, in the gate's own terms — TWO CO-EQUAL CLAUSES.

CLAUSE 1.  At the freshly-measured delta*: do the three non-power planted cases certify with
contained truth and reported widths, does the exact power law still certify at delta = 0 with
382's widths reproduced, AND does a sub-delta* control remain EMPTY (the mode must not turn
the instrument into a fit with extra steps)?

CLAUSE 2.  Does the admissible-cutoff analysis of `CLAY_OBLIGATIONS.md` §4 tolerate delta > 0
AT ALL?  §4's cutoff radius is a function of the CERTIFIED exponent, so a tolerance passes
straight into the cutoff bound: delta must exceed the profile's own departure from a power law
and must simultaneously leave the certified LOWER endpoint above the physical threshold
(1 for fixed-ball energy and the critical L^3 tail, 3/2 for global L^2).  Measured directly,
not composed from two legs' laws.

INHERITANCE DISCIPLINE.  Leg 382's post-hoc numbers (width ~= 0.8686*delta; delta* =
3.352868 / 0.315697 / 0.069739 / 0) are LEADS ONLY.  Nothing in this file reads them as an
input; they appear solely in the comparison columns, so that a disagreement is reportable as
a disagreement.  Every prediction this runner is scored against is the CLOSED FORM derived in
the pre-registration: width = 4 log(1+delta)/log(R1/R0), delta* = exp(E_inf(phi)) - 1.

CEILING: TIER 2 in every branch of both clauses.  `CLAY_OBLIGATIONS.md` §6 items 1 and 2 stay
OPEN.  No L1 -> L4 link moves.  Clay stays ~0.05%.
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from solver.dssp_decay_enclosure import (          # noqa: E402
    VERDICT_EMPTY, VERDICT_INTERVAL,
    certified_decay_from_cell_enclosures,
    certified_decay_interval, critical_tolerance, cutoff_admissible_delta_window,
    planted_log_corrected, planted_power_law, planted_rational_cutoff,
    planted_two_power, predicted_width,
)

# ---- the pre-registered constants, copied from journal PART I §1 -----------
R0, R1 = 10.0, 1000.0
R0_SEC, R1_SEC = 10.0, 100.0
N_GATE = 1000
N_TOL = 200
BISECT_ITERS = 60
P_BRACKET = (0.0, 12.0)

DELTA_LADDER = (1e-9, 1e-6, 1e-3, 1e-2, 1e-1)

# leg 382's leads.  RECORDED FOR COMPARISON ONLY — never used as an input.
LEG382_LEADS = {
    "width_coefficient": 0.8686,
    "delta_star": {"C1": 0.315697, "C2": 3.352868, "C3": 0.069739, "K2": 0.0},
    "delta0_widths": {"K1": 7.438e-15, "K2": 1.599e-14, "K3": 1.998e-14, "K4": 1.554e-14},
}

# closed-form predictions from PART I §2, computed there BEFORE any run
PRED_DELTA_STAR = {"C1": 0.318807, "C2": 3.454378, "C3": 0.077025, "K2": 0.0}
PRED_P_C = {"C1": 1.500000, "C2": 3.047509, "C3": 1.761439, "K2": 2.0}

CONTROLS = {
    "C1": ("f = r^-2 + 0.01 r^-1 (two-power, crossover r* = 100 INSIDE the window)",
           lambda: planted_two_power(1.0, 2.0, 0.01, 1.0)),
    "C2": ("f = r^-2 / (1 + (r/300)^4) (rational far cutoff)",
           lambda: planted_rational_cutoff(1.0, 2.0, 300.0, 4)),
    "C3": ("f = r^-2 log r (log correction)",
           lambda: planted_log_corrected(1.0, 2.0)),
}

# CLAUSE 2's shape family, generalised in the nominal exponent p0.
SHAPES = {
    "two_power": ("f = r^-p0 + 0.01 r^-(p0-1)", lambda p0: planted_two_power(1.0, p0, 0.01, p0 - 1.0)),
    "rational_cutoff": ("f = r^-p0 / (1 + (r/300)^4)", lambda p0: planted_rational_cutoff(1.0, p0, 300.0, 4)),
    "log_corrected": ("f = r^-p0 log r", lambda p0: planted_log_corrected(1.0, p0)),
}
# PRE-REGISTERED p0 ladder was {1.0, 1.25, 1.5, 2.0, 2.5, 3.0}.  1.25 IS DROPPED and the
# deviation is disclosed in the journal: the planted generators go through
# `ipow_half_integer`, which by construction accepts only non-negative HALF-INTEGER exponents
# (the substrate has `ilog` but no `iexp`, so leg 382 deliberately stayed inside operations
# `solver/interval.py` already proves).  p0 = 1.25 is not representable by the generator; it
# is a limit of the PLANTED PROFILE, not of the enclosure, which searches the continuum
# p in [0, 12].  Nothing in the gate turns on the dropped point.
P0_LADDER = (1.0, 1.5, 2.0, 2.5, 3.0)
ALPHA_THRESHOLDS = {"fixed_ball_energy_and_critical_L3": 1.0, "global_L2": 1.5}


def local_slope_range(float_fn, r0, r1, n=200001):
    """Float REFERENCE range of the exact local log-log slope -(d log f / d log r).

    Not a certified quantity and never quoted as one: it is the "truth" a profile that is not
    a power law actually has (a non-power profile has no single exponent), and clause 1b asks
    whether the certified interval stays inside it."""
    t = np.linspace(np.log(r0), np.log(r1), n)
    g = np.log(float_fn(np.exp(t)))
    s = -np.gradient(g, t)
    return float(np.min(s[2:-2])), float(np.max(s[2:-2]))


def main():
    t_start = time.time()
    out = {
        "leg": 386, "route": "DTOL", "version": 1,
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "preregistration": "experiments/journal/leg_386.md PART I, commit caf48e8 (immutable)",
        "novelty_pass": "writeup/novelty/leg_386.md, commit 36d01c7 (before construction)",
        "ceiling": "TIER 2 in every branch of both clauses; CLAY_OBLIGATIONS §6 items 1 and 2 OPEN",
        "clay": "~0.05%, unmoved; no L1 -> L4 link moved",
        "config": {"window": [R0, R1], "secondary_window": [R0_SEC, R1_SEC],
                   "n_cells_gate": N_GATE, "n_cells_delta": N_TOL,
                   "bisection_iters": BISECT_ITERS, "p_bracket": list(P_BRACKET),
                   "mode": "cells"},
        "leg382_leads_recorded_for_comparison_never_used_as_input": LEG382_LEADS,
    }

    # ---------------------------------------------------------------- §1 width law
    print("== §1  width law, measured fresh against the closed form")
    width_rows = []
    for win_tag, (a, b) in (("primary_10_1000", (R0, R1)), ("secondary_10_100", (R0_SEC, R1_SEC))):
        iv_fn, _ = planted_power_law(1.0, 2.0)
        for d in DELTA_LADDER:
            r = certified_decay_interval(iv_fn, a, b, N_TOL, "cells", P_BRACKET, d)
            pred = predicted_width(d, a, b)
            width_rows.append({
                "window": win_tag, "delta": d, "verdict": r["verdict"],
                "rel_tolerance_recorded_in_row": r["rel_tolerance"],
                "hypothesis_recorded_in_row": r["hypothesis"],
                "width_measured": r["width"], "width_predicted_closed_form": pred,
                "ratio_measured_over_predicted": (r["width"] / pred if pred > 0 else None),
                "contains_truth_p0_2": bool(r["verdict"] == VERDICT_INTERVAL
                                            and r["p_lo"] <= 2.0 <= r["p_hi"]),
            })
            print(f"   [{win_tag}] delta={d:<8g} {r['verdict']:8s} "
                  f"w={r['width']:.6e} pred={pred:.6e} ratio={r['width']/pred:.6f}")
    ratios = [w["ratio_measured_over_predicted"] for w in width_rows]
    coef_primary = np.mean([w["width_measured"] / w["delta"] for w in width_rows
                            if w["window"] == "primary_10_1000" and w["delta"] <= 1e-3])
    coef_secondary = np.mean([w["width_measured"] / w["delta"] for w in width_rows
                              if w["window"] == "secondary_10_100" and w["delta"] <= 1e-3])
    width_law = {
        "rows": width_rows,
        "measured_small_delta_coefficient_primary": float(coef_primary),
        "measured_small_delta_coefficient_secondary": float(coef_secondary),
        "closed_form_coefficient_primary_4_over_log100": float(4.0 / np.log(100.0)),
        "closed_form_coefficient_secondary_4_over_log10": float(4.0 / np.log(10.0)),
        "secondary_over_primary_measured": float(coef_secondary / coef_primary),
        "secondary_over_primary_predicted": 2.0,
        "ratio_min": float(np.min(ratios)), "ratio_max": float(np.max(ratios)),
        "pass_band": [0.95, 1.05],
        "PASS_1a": bool(np.min(ratios) >= 0.95 and np.max(ratios) <= 1.05
                        and 0.95 <= (coef_secondary / coef_primary) / 2.0 <= 1.05),
        "disagreement_with_leg382_lead": {
            "leg382_lead_coefficient": LEG382_LEADS["width_coefficient"],
            "measured_coefficient": float(coef_primary),
            "relative_difference": float(coef_primary / LEG382_LEADS["width_coefficient"] - 1.0),
            "note": ("leg 382's 0.8686 is 4/log(100): a property of the WINDOW, not of the "
                     "instrument. The closed form predicts it and predicts that it DOUBLES "
                     "on [10, 100] — a window-dependence leg 382 never tested."),
        },
    }
    out["clause1_a_width_law"] = width_law

    # ------------------------------------------------------- §2 fresh delta* + clause 1b
    print("== §2  delta*, measured fresh against exp(E_inf(phi)) - 1")
    dstar = {}
    clause1b = []
    for tag, (desc, gen) in CONTROLS.items():
        iv_fn, float_fn = gen()
        lo, hi = critical_tolerance(iv_fn, R0, R1, N_TOL, "cells", P_BRACKET,
                                    hi=10.0, iters=BISECT_ITERS)
        pred = PRED_DELTA_STAR[tag]
        dstar[tag] = {
            "profile": desc, "delta_star_lo": float(lo),
            "delta_star_hi": (None if hi == float("inf") else float(hi)),
            "predicted_closed_form": pred,
            "ratio_measured_over_predicted": float(lo / pred) if pred > 0 else None,
            "within_20pc_pass_band": bool(pred > 0 and abs(lo / pred - 1.0) <= 0.20),
            "leg382_lead": LEG382_LEADS["delta_star"][tag],
            "relative_difference_vs_leg382_lead":
                float(lo / LEG382_LEADS["delta_star"][tag] - 1.0)
                if LEG382_LEADS["delta_star"][tag] > 0 else None,
        }
        print(f"   {tag}: delta* in [{lo:.6f}, {hi:.6f}]  pred={pred:.6f}  "
              f"382-lead={LEG382_LEADS['delta_star'][tag]:.6f}")

        # clause 1b: certify AT the freshly measured delta*
        s_min, s_max = local_slope_range(float_fn, R0, R1)
        r = certified_decay_interval(iv_fn, R0, R1, N_TOL, "cells", P_BRACKET, hi)
        contained = bool(r["verdict"] == VERDICT_INTERVAL
                         and s_min - 1e-9 <= r["p_lo"] and r["p_hi"] <= s_max + 1e-9)
        clause1b.append({
            "id": tag, "profile": desc, "delta_used": float(hi),
            "rel_tolerance_recorded_in_row": r["rel_tolerance"],
            "hypothesis_recorded_in_row": r["hypothesis"],
            "verdict": r["verdict"], "p_lo": r["p_lo"], "p_hi": r["p_hi"],
            "width": r["width"],
            "exact_local_slope_range_float_reference": [s_min, s_max],
            "interval_inside_local_slope_range": contained,
            "predicted_transition_exponent_p_c": PRED_P_C[tag],
            "p_c_measured_centre": (None if r["p_lo"] is None
                                    else float(0.5 * (r["p_lo"] + r["p_hi"]))),
            "contains_nominal_p0_2": bool(r["verdict"] == VERDICT_INTERVAL
                                          and r["p_lo"] <= 2.0 <= r["p_hi"]),
            "note": ("nominal-p0 containment is RECORDED, not required: a profile that is not "
                     "a power law has no true exponent, and PART I §2.3 predicted in advance "
                     "that p0 = 2 is NOT contained at delta*."),
        })
        print(f"       at delta*: {r['verdict']} [{r['p_lo']}, {r['p_hi']}] "
              f"slopes[{s_min:.6f}, {s_max:.6f}] inside={contained}")
    out["clause1_delta_star_fresh"] = dstar
    out["clause1_b_certify_at_delta_star"] = {
        "rows": clause1b,
        "PASS_1b": bool(all(x["verdict"] == VERDICT_INTERVAL
                            and x["interval_inside_local_slope_range"]
                            and x["width"] is not None for x in clause1b)),
    }

    # ---------------------------------------------------- §3 clause 1c: delta = 0 knowns
    print("== §3  clause 1c: exact power laws still certify at delta = 0")
    knowns = []
    for tag, C, p0 in (("K1", 3.0, 1.0), ("K2", 1.0, 2.0), ("K3", 0.25, 2.5), ("K4", 7.0, 3.0)):
        iv_fn, _ = planted_power_law(C, p0)
        r = certified_decay_interval(iv_fn, R0, R1, N_GATE, "cells", P_BRACKET, 0.0)
        lead = LEG382_LEADS["delta0_widths"][tag]
        knowns.append({
            "id": tag, "C": C, "p0": p0, "verdict": r["verdict"],
            "rel_tolerance_recorded_in_row": r["rel_tolerance"],
            "hypothesis_recorded_in_row": r["hypothesis"],
            "p_lo": r["p_lo"], "p_hi": r["p_hi"], "width": r["width"],
            "contains_truth": bool(r["p_lo"] <= p0 <= r["p_hi"]),
            "leg382_lead_width": lead,
            "ratio_to_leg382_lead": float(r["width"] / lead),
            "within_factor_10_of_lead": bool(0.1 <= r["width"] / lead <= 10.0),
        })
        print(f"   {tag} p0={p0}: {r['verdict']} w={r['width']:.4e} "
              f"(382 lead {lead:.4e}, ratio {r['width']/lead:.4f})")
    out["clause1_c_delta_zero_knowns"] = {
        "rows": knowns,
        "PASS_1c": bool(all(k["verdict"] == VERDICT_INTERVAL and k["contains_truth"]
                            and k["width"] <= 1e-13 and k["within_factor_10_of_lead"]
                            for k in knowns)),
    }

    # -------------------------------------------- §4 clause 1d: sub-delta* stays EMPTY
    print("== §4  clause 1d: sub-delta* controls stay EMPTY")
    sub = []
    for tag, (desc, gen) in CONTROLS.items():
        iv_fn, _ = gen()
        lo = dstar[tag]["delta_star_lo"]
        for frac in (0.9, 0.5):
            d = frac * lo
            r = certified_decay_interval(iv_fn, R0, R1, N_TOL, "cells", P_BRACKET, d)
            sub.append({"id": tag, "fraction_of_delta_star": frac, "delta": float(d),
                        "rel_tolerance_recorded_in_row": r["rel_tolerance"],
                        "hypothesis_recorded_in_row": r["hypothesis"],
                        "verdict": r["verdict"],
                        "contradiction_gap_p_lo_minus_p_hi":
                            (None if r["p_lo"] is None else float(r["p_lo"] - r["p_hi"]))})
            print(f"   {tag} at {frac:g}*delta* = {d:.6f}: {r['verdict']}")
    out["clause1_d_sub_delta_star_empty"] = {
        "rows": sub,
        "PASS_1d": bool(all(x["verdict"] == VERDICT_EMPTY for x in sub)),
    }

    # ------------------------------- §5 H-381 vs H-shift, the pre-registered discriminant
    print("== §5  H-381 vs H-shift: does the half-width vanish at delta = 0 or at delta*?")
    disc = []
    for tag, (desc, gen) in CONTROLS.items():
        iv_fn, _ = gen()
        ds = dstar[tag]["delta_star_hi"]
        for mult in (1.1, 1.5, 2.0, 4.0, 10.0):
            d = mult * ds
            r = certified_decay_interval(iv_fn, R0, R1, N_TOL, "cells", P_BRACKET, d)
            hw = None if r["width"] is None else 0.5 * r["width"]
            h381 = 0.43429448190325176 * d
            hshift = 0.43429448190325176 * (d - ds)
            disc.append({"id": tag, "multiple_of_delta_star": mult, "delta": float(d),
                         "verdict": r["verdict"], "half_width_measured": hw,
                         "H381_prediction_0p434_delta": float(h381),
                         "Hshift_prediction_0p434_delta_minus_delta_star": float(hshift),
                         "measured_over_H381": (None if hw is None else float(hw / h381)),
                         "measured_over_Hshift": (None if hw is None or hshift <= 0
                                                  else float(hw / hshift))})
            print(f"   {tag} delta={d:.6f} ({mult:g}x delta*): half-width={hw} "
                  f"H381={h381:.6f} Hshift={hshift:.6f}")
    at_1p1 = [x for x in disc if x["multiple_of_delta_star"] == 1.1]
    hshift_favoured = all(x["measured_over_H381"] is not None
                          and x["measured_over_H381"] < 0.5 for x in at_1p1)
    h381_favoured = all(x["measured_over_H381"] is not None
                        and abs(x["measured_over_H381"] - 1.0) <= 0.10 for x in at_1p1)
    out["clause2_halfwidth_law_discriminant"] = {
        "rows": disc,
        "decision_rule": ("H-shift favoured if measured half-width at 1.1*delta* is below "
                          "HALF of the H-381 value; H-381 favoured if within +/-10% of it; "
                          "anything else reported as 'neither law fits'"),
        "H_shift_favoured": bool(hshift_favoured),
        "H_381_favoured": bool(h381_favoured),
        "verdict": ("H-shift" if hshift_favoured else
                    ("H-381" if h381_favoured else "neither law fits")),
    }

    # ------------------------------------------------- §6 CLAUSE 2, measured directly
    print("== §6  CLAUSE 2: the composed delta window, measured directly")
    windows = []
    for shape, (sdesc, gen) in SHAPES.items():
        for p0 in P0_LADDER:
            iv_fn, float_fn = gen(p0)
            s_min, s_max = local_slope_range(float_fn, R0, R1)
            for thr_name, thr in ALPHA_THRESHOLDS.items():
                w = cutoff_admissible_delta_window(iv_fn, R0, R1, thr, n_cells=N_TOL,
                                                   p_bracket=P_BRACKET, delta_cap=10.0,
                                                   iters=50)
                ac = w["alpha_centre"]
                leg381_delta_max = (None if ac is None
                                    else (ac - thr) / 0.43429448190325176)
                w.update({"shape": shape, "shape_formula": sdesc, "p0": p0,
                          "threshold_name": thr_name,
                          "exact_local_slope_range_float_reference": [s_min, s_max],
                          "leg381_law_delta_max_alpha_centre_minus_thr_over_0p434":
                              leg381_delta_max,
                          "measured_over_leg381_delta_max":
                              (None if (leg381_delta_max is None or w["delta_max"] is None
                                        or leg381_delta_max <= 0)
                               else float(w["delta_max"] / leg381_delta_max))})
                windows.append(w)
                print(f"   {shape:16s} p0={p0:<4g} thr={thr:<4g} "
                      f"admissible={w['admissible']} "
                      f"window=[{w['delta_min']}, {w['delta_max']}] "
                      f"alpha_centre={w['alpha_centre']}")
    nominal_at_alpha1 = [w for w in windows if w["p0"] == 1.0
                         and w["threshold_name"] == "fixed_ball_energy_and_critical_L3"]
    nominal_admissible = [w for w in nominal_at_alpha1 if w["admissible"]]

    # -- §6b the REALISED-alpha reading, which is the one PART I §4 fixed ---------------
    # PART I §4: "The measured alpha_centre = (p_lo + p_hi)/2 of each row is recorded
    # alongside, so the clause is decided at the alpha ACTUALLY REALISED and not at a
    # nominal one."  The nominal-p0 tally above is kept and reported, because it is the
    # cruder reading and it answers the OPPOSITE way -- one shape (the rational cutoff)
    # carries nominal p0 = 1 while REALISING alpha_centre = 2.03, because the window
    # contains its cutoff and the profile there decays far faster than r^-1.  Reporting
    # only the nominal tally would credit the composed condition with an admissibility it
    # does not have at alpha = 1.
    print("== §6b  the realised-alpha reading: does admissibility hinge on alpha_centre?")
    dichotomy = []
    for w in windows:
        ac = w["alpha_centre"]
        predicted = (ac is not None and ac > w["alpha_threshold"])
        dichotomy.append({"shape": w["shape"], "p0": w["p0"],
                          "threshold": w["alpha_threshold"], "alpha_centre": ac,
                          "admissible": w["admissible"],
                          "predicted_by_alpha_centre_gt_threshold": bool(predicted),
                          "agrees": bool(predicted == w["admissible"])})
    exceptions = [x for x in dichotomy if not x["agrees"]]

    # How much headroom on the threshold does a positive tolerance BUY?  Measured by
    # asking whether the window survives a threshold set just below / just above the
    # realised centre.  If the crossover threshold is the centre itself, delta buys
    # exactly ZERO headroom -- which is the whole question §4's consumers have.
    headroom = []
    for shape, (sdesc, gen) in SHAPES.items():
        for p0 in (1.5, 2.5):
            iv_fn, _ = gen(p0)
            base = [w for w in windows if w["shape"] == shape and w["p0"] == p0
                    and w["alpha_threshold"] == 1.0][0]
            ac = base["alpha_centre"]
            below = cutoff_admissible_delta_window(iv_fn, R0, R1, ac * (1 - 1e-6),
                                                   n_cells=N_TOL, p_bracket=P_BRACKET,
                                                   delta_cap=10.0, iters=40)
            above = cutoff_admissible_delta_window(iv_fn, R0, R1, ac * (1 + 1e-6),
                                                   n_cells=N_TOL, p_bracket=P_BRACKET,
                                                   delta_cap=10.0, iters=40)
            headroom.append({"shape": shape, "p0": p0, "alpha_centre": ac,
                             "admissible_at_threshold_just_BELOW_centre": below["admissible"],
                             "admissible_at_threshold_just_ABOVE_centre": above["admissible"],
                             "window_width_just_below_centre": below["width"],
                             "crossover_threshold_is_the_centre":
                                 bool(below["admissible"] and not above["admissible"])})
            print(f"   {shape:16s} p0={p0:<4g} alpha_centre={ac:.6f}  "
                  f"below={below['admissible']} above={above['admissible']}")

    realised_admissible_at_alpha_le_1 = [
        x for x in dichotomy
        if x["threshold"] == 1.0 and x["alpha_centre"] is not None
        and x["alpha_centre"] <= 1.0 and x["admissible"]]

    out["clause2_delta_windows"] = {
        "rows": windows,
        "alpha_in_play_preregistered": 1.0,
        "alpha_in_play_source": ("CLAY_OBLIGATIONS.md §4 amendment 3: 'L^2 needs alpha > 3/2; "
                                 "the banked Type-I object gives alpha = 1 — deficit 0.5, "
                                 "ratio 1.5x'"),
        "nominal_p0_reading": {
            "n_admissible": len(nominal_admissible),
            "shapes": [w["shape"] for w in nominal_admissible],
            "why_not_operative": ("the rational cutoff carries nominal p0 = 1 but REALISES "
                                  "alpha_centre = %.6f, because the measurement window "
                                  "contains its cutoff; PART I §4 fixed the decision at the "
                                  "realised alpha, not the nominal one"
                                  % (nominal_admissible[0]["alpha_centre"]
                                     if nominal_admissible else float("nan"))),
        },
        "realised_alpha_reading_OPERATIVE": {
            "dichotomy_rows": dichotomy,
            "n_rows": len(dichotomy),
            "n_exceptions_to_admissible_iff_alpha_centre_gt_threshold": len(exceptions),
            "exceptions": exceptions,
            "headroom_probe": headroom,
            "delta_buys_zero_threshold_headroom": bool(
                all(h["crossover_threshold_is_the_centre"] for h in headroom)),
            "n_admissible_rows_with_realised_alpha_centre_le_1": len(
                realised_admissible_at_alpha_le_1),
        },
        "CLAUSE2_ADMISSIBLE_AT_ALPHA_IN_PLAY": bool(len(realised_admissible_at_alpha_le_1) > 0),
    }

    # ------------------------------------------------------- §7 anti-tautology checks
    print("== §7  anti-tautology checks")
    at = {}
    iv_fn, _ = planted_power_law(1.0, 2.0)
    at["1_no_known_returns_full_bracket_at_any_delta"] = bool(all(
        certified_decay_interval(iv_fn, R0, R1, N_TOL, "cells", P_BRACKET, d)["verdict"]
        == VERDICT_INTERVAL for d in (0.0,) + DELTA_LADDER))
    at["2_no_exact_power_law_ever_certified_EMPTY"] = bool(all(
        certified_decay_interval(planted_power_law(1.0, p0)[0], R0, R1, N_TOL, "cells",
                                 P_BRACKET, d)["verdict"] != VERDICT_EMPTY
        for p0 in (1.0, 2.0, 2.5, 3.0) for d in (0.0, 1e-6, 1e-2, 1e-1)))
    at["3_every_mismatch_EMPTY_at_delta_zero"] = bool(all(
        certified_decay_interval(gen()[0], R0, R1, N_TOL, "cells", P_BRACKET, 0.0)["verdict"]
        == VERDICT_EMPTY for _, gen in CONTROLS.values()))
    probe_rows = ([w for w in width_rows] + clause1b + knowns + sub)
    at["4_delta_recorded_in_every_row"] = bool(all(
        ("rel_tolerance_recorded_in_row" in row and row["rel_tolerance_recorded_in_row"] is not None)
        for row in probe_rows))
    zero_row = certified_decay_interval(lambda R: planted_power_law(1.0, 2.0)[0](R)
                                        - planted_power_law(1.0, 2.0)[0](R),
                                        R0, R1, 20, "cells", P_BRACKET, 3e-3)
    at["4b_delta_recorded_on_the_INCAPACITY_zero_crossing_path"] = bool(
        zero_row.get("rel_tolerance", None) == 3e-3)
    widths_mono = [certified_decay_interval(iv_fn, R0, R1, N_TOL, "cells", P_BRACKET, d)["width"]
                   for d in (0.0, 1e-9, 1e-6, 1e-3, 1e-2, 1e-1)]
    # 6. THE STANDING RULE (DM cycle 11g), checked the way leg 385 earned it.  X3's false
    # certificate had width 7.438494264988549e-15, bit-indistinguishable from true K1's.
    # So the check is not "is a hypothesis present" but "does the row distinguish two
    # certifications that the WIDTH cannot distinguish": a cells row and a nodes row of the
    # same profile must carry DIFFERENT hypotheses, and an undeclared caller must come back
    # UNDECLARED rather than inheriting a hypothesis it never declared.
    at["6_hypothesis_recorded_in_every_row"] = bool(all(
        ("hypothesis_recorded_in_row" in row and row["hypothesis_recorded_in_row"] is not None)
        for row in probe_rows))
    cells_row = certified_decay_interval(iv_fn, R0, R1, N_TOL, "cells", P_BRACKET, 0.0)
    nodes_row = certified_decay_interval(iv_fn, R0, R1, N_TOL, "nodes", P_BRACKET, 0.0)
    bare_row = certified_decay_from_cell_enclosures([10.0, 20.0], [20.0, 40.0],
                                                    [1.0, 0.25], [1.0, 0.25])
    at["6b_hypothesis_separates_what_the_width_cannot"] = bool(
        cells_row["hypothesis"] != nodes_row["hypothesis"]
        and bare_row["hypothesis"] == "UNDECLARED"
        and zero_row["hypothesis"] is not None)
    at["6c_composed_window_carries_the_hypothesis_it_was_composed_from"] = bool(
        cutoff_admissible_delta_window(iv_fn, R0, R1, 1.0, n_cells=100,
                                       iters=25)["hypothesis"] == cells_row["hypothesis"])
    at["5_widths_non_decreasing_in_delta"] = bool(all(
        widths_mono[i] <= widths_mono[i + 1] + 1e-15 for i in range(len(widths_mono) - 1)))
    for k, v in at.items():
        print(f"   {k}: {v}")
    out["anti_tautology"] = at

    # ------------------------------------------------------------------ verdicts
    c1 = bool(width_law["PASS_1a"] and out["clause1_b_certify_at_delta_star"]["PASS_1b"]
              and out["clause1_c_delta_zero_knowns"]["PASS_1c"]
              and out["clause1_d_sub_delta_star_empty"]["PASS_1d"])
    c2 = out["clause2_delta_windows"]["CLAUSE2_ADMISSIBLE_AT_ALPHA_IN_PLAY"]
    out["GATE"] = {
        "clause1_wording": ("At the freshly-measured delta*: do the three non-power planted "
                            "cases certify with contained truth and reported widths, does the "
                            "exact power law still certify at delta = 0 with 382's widths "
                            "reproduced, AND does a sub-delta* control remain EMPTY?"),
        "clause1_answer": ("YES" if c1 else "NO"),
        "clause1_subconditions": {"1a_width_law": width_law["PASS_1a"],
                                  "1b_certify_at_delta_star":
                                      out["clause1_b_certify_at_delta_star"]["PASS_1b"],
                                  "1c_delta_zero_knowns":
                                      out["clause1_c_delta_zero_knowns"]["PASS_1c"],
                                  "1d_sub_delta_star_empty":
                                      out["clause1_d_sub_delta_star_empty"]["PASS_1d"]},
        "clause2_wording": "Does the admissible-cutoff analysis tolerate delta > 0 AT ALL?",
        "clause2_answer": ("ADMISSIBLE" if c2 else "EMPTY"),
        "not_netted": ("The two clauses are reported side by side and are NOT combined into "
                       "one word."),
        "ceiling": "TIER 2 in both branches of both clauses",
        "clay_obligations_6_items_1_and_2": "OPEN in every branch",
    }
    out["runtime_seconds"] = float(time.time() - t_start)

    dest = ROOT / "writeup" / "data" / "p2_route_dtol_v1.json"
    dest.write_text(json.dumps(out, indent=2, sort_keys=False) + "\n")
    print()
    print(f"CLAUSE 1: {out['GATE']['clause1_answer']}   "
          f"CLAUSE 2: {out['GATE']['clause2_answer']}")
    print(f"wrote {dest.relative_to(ROOT)}  ({out['runtime_seconds']:.1f}s)")


if __name__ == "__main__":
    main()
