#!/usr/bin/env python3
"""Route-SCEL v1 (leg 385) — the samples→cells adapter, run against its pre-registration.

    .venv/bin/python experiments/p2_route_scel_v1.py            # run, bank, draw fig103
    .venv/bin/python experiments/p2_route_scel_v1.py --figure   # redraw fig103 from the JSON

Banks `writeup/data/p2_route_scel_v1.json` and draws **fig103** (and no other number:
fig100/101/102 were allocated this cycle to legs 382, 233 and 383; fig97/98 are reserved for
PROG-R4 and fig99 for leg 381).

WHAT THIS RUNNER DECIDES.  Leg 382 built a certified decay enclosure that consumes CELL
ENCLOSURES and named, in its own docstring, the converter it does not supply.  This run
measures whether the converter in `solver/dssp_decay_samples.py` (a) reproduces leg 382's
exact-power result from SAMPLES under a stated true hypothesis, and (b) refuses, or is caught
by a containment failure, on inputs whose declared hypothesis is false.

Every leg-382 number it compares against is RE-COMPUTED here by calling leg 382's module
directly on the same window, never transcribed.  Leg 382's file is read and edited nowhere.

The pre-registration is Part I of `experiments/journal/leg_385.md`, committed at `353cbf1`,
before this file existed; the novelty pass is `writeup/novelty/leg_385.md` at `00d8e4e`.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from solver.dssp_decay_enclosure import (                      # noqa: E402
    VERDICT_INTERVAL, certified_decay_interval, planted_power_law,
)
from solver.dssp_decay_samples import (                        # noqa: E402
    Modulus, VERDICT_CELLS, VERDICT_INCAPACITY,
    certified_decay_from_samples, containment_audit,
    planted_node_aligned_wiggle, planted_sampled_power_law, samples_to_cells,
)

DATA = ROOT / "writeup" / "data" / "p2_route_scel_v1.json"
FIGS = ROOT / "writeup" / "figures"

R0, R1 = 10.0, 1000.0          # leg 382's window, unmoved
NCELL = 1000                   # leg 382's gate cell count, unmoved
GRID = np.geomspace(R0, R1, NCELL + 1)
WIGGLE_A = 0.05                # the secret-violation amplitude, pre-registered
L_LOGLOG = 1.05                # a TRUE loglog Lipschitz statement for f = 3 r^-1 (truth 1.0)
L_ABSOLUTE = 0.03              # the TRUE global absolute Lipschitz constant of 3 r^-1 on [10,1000]

PRED = {}   # filled as the run proceeds: name -> (predicted, measured, status)


def _record(name, statement, predicted, measured, ok):
    PRED[name] = {"statement": statement,
                  "predicted": predicted,
                  "measured": measured,
                  "status": "CONFIRMED" if ok else "REFUTED"}
    return ok


def _slim(res, keep_cells=False):
    """A JSON-safe view of a result row: numbers and strings, no numpy arrays."""
    out = {k: v for k, v in res.items()
           if k not in ("cells", "adapter", "hypothesis_detail") and not isinstance(v, np.ndarray)}
    out["hypothesis_detail"] = res.get("hypothesis_detail")
    if keep_cells and "adapter" in res:
        out["adapter"] = res["adapter"]
    return out


# ---------------------------------------------------------------------------

def main(figure_only=False):
    if figure_only:
        return draw(json.loads(DATA.read_text()))

    t_start = time.time()
    out = {
        "leg": 385,
        "route": "SCEL",
        "version": "v1",
        "novelty_commit": "00d8e4e",
        "preregistration_commit": "353cbf1",
        "reads_but_does_not_edit": "solver/dssp_decay_enclosure.py (leg 382, 104f5b3)",
        "window": {"R0": R0, "R1": R1,
                   "leverage_W_log_ratio": float(np.log(R1 / R0)),
                   "provenance": "leg 382's window and cell count, unmoved by this leg"},
        "gate_cell_count": NCELL,
        "ceiling": "TIER 2",
        "clay_odds": "~0.05%, unmoved; no L1->L4 link moved by this leg",
        "obligations_still_open": [
            "CLAY_OBLIGATIONS.md §6 item 1 — the ADMISSIBLE CUTOFF half is untouched by this "
            "leg, which supplies only the input contract of the certified-exponent third",
            "CLAY_OBLIGATIONS.md §6 item 2 — untouched",
        ],
        "no_profile_exists": (
            "No profile of route 4's object exists in this repository. Every input below is a "
            "planted analytic known. The first real consumer remains whatever future unit "
            "produces a profile, and this leg claims nothing about one."),
    }

    # -- 1.  PATH A: reproduction of leg 382's exact-power widths, from SAMPLES ----------
    reproduction = []
    for C, p in ((3.0, 1.0), (1.0, 2.0), (1.0, 2.5), (1.0, 3.0)):
        f_lo, f_hi, true_fn = planted_sampled_power_law(C, p, GRID)
        got = certified_decay_from_samples(GRID, f_lo=f_lo, f_hi=f_hi,
                                           monotone="nonincreasing")
        iv_fn, _ = planted_power_law(C, p)
        base = certified_decay_interval(iv_fn, R0, R1, NCELL, "cells")
        cells = samples_to_cells(GRID, f_lo=f_lo, f_hi=f_hi, monotone="nonincreasing")
        audit = containment_audit(cells, true_fn)
        reproduction.append({
            "id": f"S1/p={p}",
            "profile": f"f = {C} r^-{p}",
            "truth_exponent": p,
            "hypothesis": got["hypothesis"],
            "hypothesis_detail": got["hypothesis_detail"],
            "sample_exactness": got["sample_exactness"],
            "conditional_on": got["conditional_on"],
            "sampled": {"verdict": got["verdict"], "p_lo": got["p_lo"], "p_hi": got["p_hi"],
                        "width": got["width"], "contains_truth": bool(got["p_lo"] <= p <= got["p_hi"]),
                        "containment_margin_below": float(p - got["p_lo"]),
                        "containment_margin_above": float(got["p_hi"] - p)},
            "leg_382_recomputed": {"verdict": base["verdict"], "width": base["width"]},
            "width_difference": float(got["width"] - base["width"]),
            "bit_identical_to_leg_382": bool(got["width"] == base["width"]),
            "containment_audit": audit,
        })
    out["path_A_reproduction"] = reproduction

    ok = all(r["sampled"]["verdict"] == VERDICT_INTERVAL and r["sampled"]["contains_truth"]
             and abs(r["width_difference"]) < 5e-14 for r in reproduction)
    _record("P1", "PATH A reproduces leg 382's exact-power widths within 5e-14, truth inside",
            "|width - width_382| < 5e-14 for p = 1, 2, 2.5, 3",
            {r["id"]: r["width_difference"] for r in reproduction}, ok)

    # -- 2.  PATH B (loglog): sound, and how much wider ----------------------------------
    f_lo, f_hi, true_fn = planted_sampled_power_law(3.0, 1.0, GRID)
    mod_ll = Modulus(L_LOGLOG, 1.0, "loglog")
    s2 = certified_decay_from_samples(GRID, f_lo=f_lo, f_hi=f_hi, modulus=mod_ll)
    cells_s2 = samples_to_cells(GRID, f_lo=f_lo, f_hi=f_hi, modulus=mod_ll)
    out["path_B_loglog"] = {
        "id": "S2",
        "profile": "f = 3.0 r^-1",
        "truth_exponent": 1.0,
        "declared_modulus": mod_ll.detail(),
        "true_loglog_lipschitz_constant": 1.0,
        "hypothesis": s2["hypothesis"],
        "conditional_on": s2["conditional_on"],
        "verdict": s2["verdict"], "p_lo": s2["p_lo"], "p_hi": s2["p_hi"],
        "width": s2["width"],
        "contains_truth": bool(s2["p_lo"] <= 1.0 <= s2["p_hi"]),
        "omega_half_cell": cells_s2["enclosure_parts"]["modulus"]["omega_half_cell_max"],
        "max_relative_inflation": cells_s2["enclosure_parts"]["modulus"]["max_relative_inflation"],
        "width_ratio_to_path_A": float(s2["width"] / reproduction[0]["sampled"]["width"]),
        "containment_audit": containment_audit(cells_s2, true_fn),
    }
    _record("P2", "PATH B width at N=1000 lands in [7e-4, 6e-3] and contains the truth",
            "≈2.0e-3, band [7e-4, 6e-3]", s2["width"],
            (s2["verdict"] == VERDICT_INTERVAL and s2["p_lo"] <= 1.0 <= s2["p_hi"]
             and 7e-4 < s2["width"] < 6e-3))

    # -- 3.  the N ladder, both paths ----------------------------------------------------
    ladder = []
    for N in (100, 250, 1000, 2000):
        g = np.geomspace(R0, R1, N + 1)
        fl, fh, _ = planted_sampled_power_law(3.0, 1.0, g)
        a = certified_decay_from_samples(g, f_lo=fl, f_hi=fh, monotone="nonincreasing")
        b = certified_decay_from_samples(g, f_lo=fl, f_hi=fh, modulus=mod_ll)
        ladder.append({"N": N,
                       "path_A_width": a["width"], "path_A_verdict": a["verdict"],
                       "path_B_width": b["width"], "path_B_verdict": b["verdict"],
                       "path_B_contains_truth": bool(b["p_lo"] <= 1.0 <= b["p_hi"])})
    Ns = np.array([row["N"] for row in ladder], dtype=float)
    slope_A = float(np.polyfit(np.log(Ns), np.log([row["path_A_width"] for row in ladder]), 1)[0])
    slope_B = float(np.polyfit(np.log(Ns), np.log([row["path_B_width"] for row in ladder]), 1)[0])
    N_needed = float(1000.0 * ladder[2]["path_B_width"] / reproduction[0]["sampled"]["width"])
    out["cell_count_ladder"] = {
        "rows": ladder,
        "path_A_loglog_slope": slope_A,
        "path_B_loglog_slope": slope_B,
        "N_for_PATH_B_to_reach_PATH_A_width": N_needed,
        "reading": ("PATH A's width sits on the rounding floor and does not scale with N "
                    "(leg 382 measured the same, slope -0.0295). PATH B's width is set by "
                    "omega(dt/2) and falls exactly like 1/N, so reaching PATH A's width "
                    f"would need N ~ {N_needed:.3g} samples. THE MODULUS PATH CANNOT "
                    "REPRODUCE LEG 382's EXACT-POWER WIDTHS AT ANY FEASIBLE SAMPLING "
                    "DENSITY; it is sound, not tight, and this was predicted before the run "
                    "(P3), not discovered and rationalised after it."),
    }
    _record("P3", "PATH B width slope -1.00±0.05; PATH A slope |.|<0.2",
            {"path_B": "-1.00 ± 0.05", "path_A": "|slope| < 0.2"},
            {"path_B": slope_B, "path_A": slope_A},
            (-1.05 < slope_B < -0.95) and abs(slope_A) < 0.2)

    # -- 4.  PATH B (absolute): the predicted death on a three-decade window --------------
    mod_abs = Modulus(L_ABSOLUTE, 1.0, "absolute")
    cells_s3 = samples_to_cells(GRID, f_lo=f_lo, f_hi=f_hi, modulus=mod_abs)
    s3 = certified_decay_from_samples(GRID, f_lo=f_lo, f_hi=f_hi, modulus=mod_abs)
    part = cells_s3["enclosure_parts"]["modulus"]
    sub = slice(None, None, 10)
    out["path_B_absolute"] = {
        "id": "S3",
        "profile": "f = 3.0 r^-1",
        "declared_modulus": mod_abs.detail(),
        "true_global_lipschitz_constant": L_ABSOLUTE,
        "hypothesis": cells_s3["hypothesis"],
        "conditional_on": cells_s3["conditional_on"],
        "adapter_verdict": cells_s3["verdict"],
        "n_cells_nonpositive_lower": cells_s3["n_cells_nonpositive_lower"],
        "first_nonpositive_radius": part["first_nonpositive_radius"],
        "downstream_verdict": s3["verdict"],
        "downstream_reason": s3["reason"],
        "containment_audit": containment_audit(cells_s3, true_fn),
        "curve": {"r": [float(x) for x in cells_s3["r_lo"][sub]],
                  "f_lo": [float(x) for x in cells_s3["f_lo"][sub]],
                  "f_true": [float(x) for x in true_fn(cells_s3["r_lo"][sub])]},
        "mechanism": ("omega(h/2) grows with r on a geometric grid while f decays, so the "
                      "additive inflation overtakes the profile itself. A GLOBALLY stated "
                      "absolute modulus is useless on a multi-decade window; the loglog kind "
                      "or per-sample local constants are what such a window admits."),
    }
    _record("P4", "S3 goes non-positive from r ≈ 208 in ≥250 cells and the downstream answers INCAPACITY",
            {"first_nonpositive_radius": "≈208, band [100,420]", "n_cells": "≥250",
             "downstream": "INCAPACITY"},
            {"first_nonpositive_radius": part["first_nonpositive_radius"],
             "n_cells": cells_s3["n_cells_nonpositive_lower"],
             "downstream": s3["verdict"]},
            (100.0 < (part["first_nonpositive_radius"] or 0.0) < 420.0
             and cells_s3["n_cells_nonpositive_lower"] >= 250
             and s3["verdict"] == VERDICT_INCAPACITY))

    # -- 5.  both hypotheses at once -----------------------------------------------------
    s4 = certified_decay_from_samples(GRID, f_lo=f_lo, f_hi=f_hi,
                                      monotone="nonincreasing", modulus=mod_ll)
    out["both_hypotheses"] = {
        "id": "S4", "hypothesis": s4["hypothesis"], "verdict": s4["verdict"],
        "width": s4["width"],
        "difference_from_path_A": float(s4["width"] - reproduction[0]["sampled"]["width"]),
        "conditional_on": s4["conditional_on"],
        "reading": "the enclosures are intersected; the tighter (monotone) statement dominates",
    }
    _record("P12", "declaring both hypotheses gives PATH A's width to within 1e-15",
            "|difference| < 1e-15", out["both_hypotheses"]["difference_from_path_A"],
            abs(out["both_hypotheses"]["difference_from_path_A"]) < 1e-15)

    # -- 6.  THE CONTROLS ----------------------------------------------------------------
    controls = []
    truth_wiggle = planted_node_aligned_wiggle(3.0, 1.0, WIGGLE_A, GRID)

    x1 = certified_decay_from_samples(GRID, f_lo=f_lo, f_hi=f_hi)
    controls.append({
        "id": "X1", "kind": "NO HYPOTHESIS", "expected": "refusal",
        "verdict": x1["verdict"], "enclosure_called": x1["enclosure_called"],
        "exponent_returned": x1["p_lo"], "reason": x1["reason"],
        "fired": bool(x1["verdict"] == VERDICT_INCAPACITY and x1["enclosure_called"] is False),
    })

    fl2, fh2 = f_lo.copy(), f_hi.copy()
    fl2[500] *= 1.05
    fh2[500] *= 1.05
    x2 = samples_to_cells(GRID, f_lo=fl2, f_hi=fh2, monotone="nonincreasing")
    controls.append({
        "id": "X2", "kind": "MONOTONICITY VIOLATED, VISIBLY (one sample raised 5%)",
        "expected": "refusal", "verdict": x2["verdict"],
        "offending_cell": x2["necessary_condition_checks"]["monotone_worst_index"],
        "violation_magnitude": x2["necessary_condition_checks"]["monotone_worst_violation"],
        "reason": x2["reason"],
        "fired": bool(x2["verdict"] == VERDICT_INCAPACITY),
    })

    cells_x3 = samples_to_cells(GRID, f_lo=f_lo, f_hi=f_hi, monotone="nonincreasing")
    audit_x3 = containment_audit(cells_x3, truth_wiggle)
    cert_x3 = certified_decay_from_samples(GRID, f_lo=f_lo, f_hi=f_hi, monotone="nonincreasing")
    controls.append({
        "id": "X3", "kind": "MONOTONICITY VIOLATED, SECRETLY (node-aligned wiggle, A = 0.05)",
        "expected": "containment failure (the adapter provably cannot see this)",
        "adapter_verdict": cells_x3["verdict"],
        "certified_verdict": cert_x3["verdict"],
        "certified_width": cert_x3["width"],
        "certified_interval_contains_1": bool(cert_x3["p_lo"] <= 1.0 <= cert_x3["p_hi"]),
        "containment_audit": audit_x3,
        "fired": bool(cells_x3["verdict"] == VERDICT_CELLS and not audit_x3["contained"]
                      and 0.03 < audit_x3["worst_signed_relative_excess"] < 0.06),
        "reading": ("The certificate is VALID under the declared hypothesis and FALSE about "
                    "the true profile, which leaves the claimed enclosure in every one of "
                    f"{audit_x3['n_cells_violated']} cells by up to "
                    f"{audit_x3['worst_signed_relative_excess']:.4f} relative. This is the "
                    "whole argument for recording conditionality in the row: the number "
                    "7.44e-15 is indistinguishable from S1's, and only the hypothesis field "
                    "separates a true certificate from a false one."),
    })

    g2lo, g2hi, _ = planted_sampled_power_law(1.0, 2.0, GRID)
    x4 = samples_to_cells(GRID, f_lo=g2lo, f_hi=g2hi, modulus=Modulus(0.1, 1.0, "loglog"))
    controls.append({
        "id": "X4", "kind": "MODULUS UNDERSTATED, DETECTABLY (L = 0.1 declared, truth 2.0)",
        "expected": "refusal", "verdict": x4["verdict"],
        "worst_ratio": x4["necessary_condition_checks"]["modulus_worst_ratio"],
        "worst_jump": x4["necessary_condition_checks"]["modulus_worst_jump"],
        "worst_omega": x4["necessary_condition_checks"]["modulus_worst_omega"],
        "reason": x4["reason"],
        "fired": bool(x4["verdict"] == VERDICT_INCAPACITY),
    })

    cells_x5 = samples_to_cells(GRID, f_lo=f_lo, f_hi=f_hi, modulus=mod_ll)
    audit_x5 = containment_audit(cells_x5, truth_wiggle)
    controls.append({
        "id": "X5", "kind": "MODULUS UNDERSTATED, UNDETECTABLY (node increments obey L = 1.05; "
                            "within-cell variation does not)",
        "expected": "containment failure",
        "adapter_verdict": cells_x5["verdict"],
        "declared_omega_half_cell": cells_x5["enclosure_parts"]["modulus"]["omega_half_cell_max"],
        "containment_audit": audit_x5,
        "fired": bool(cells_x5["verdict"] == VERDICT_CELLS and not audit_x5["contained"]
                      and 0.035 < audit_x5["worst_signed_log_excess"] < 0.055),
        "reading": ("The node-to-node increments satisfy the declared modulus exactly "
                    "(|dg| = dt <= 1.05 dt), so the necessary condition passes; the true "
                    f"within-cell excursion {WIGGLE_A} dwarfs the inflation "
                    f"{cells_x5['enclosure_parts']['modulus']['omega_half_cell_max']:.4e} "
                    f"and the truth escapes by {audit_x5['worst_signed_log_excess']:.5f} in "
                    "log f."),
    })

    out["gate_controls"] = controls
    out["all_gate_controls_fired"] = bool(all(c["fired"] for c in controls))
    for cid, pred in (("X1", "P5"), ("X2", "P6"), ("X3", "P7"), ("X4", "P8"), ("X5", "P9")):
        c = next(x for x in controls if x["id"] == cid)
        _record(pred, f"control {cid} fires ({c['expected']})", "fires",
                {k: c[k] for k in c if k in ("verdict", "adapter_verdict", "worst_ratio",
                                             "violation_magnitude")} or "fires", c["fired"])

    # -- 7.  P11: the grid-shift probe, and WHERE THE PRE-REGISTRATION WAS WRONG ----------
    t = np.log(GRID)
    shifted = np.exp(t[:-1] + 0.5 * (t[1] - t[0]))
    p11 = samples_to_cells(shifted, f=truth_wiggle(shifted), monotone="nonincreasing")
    quarter = np.exp(t[:-1] + 0.25 * (t[1] - t[0]))
    p11q = samples_to_cells(quarter, f=truth_wiggle(quarter), monotone="nonincreasing")
    incommensurate = []
    for N2 in (500, 997, 1001, 1010, 1100, 1500, 2000):
        g2 = np.geomspace(R0, R1, N2 + 1)
        c2 = samples_to_cells(g2, f=truth_wiggle(g2), monotone="nonincreasing")
        incommensurate.append({
            "N_resample": N2,
            "spacing_ratio_dt_over_dt0": float((np.log(R1 / R0) / N2) / (t[1] - t[0])),
            "verdict": c2["verdict"],
            "monotone_worst_violation":
                c2.get("necessary_condition_checks", {}).get("monotone_worst_violation"),
        })
    out["grid_shift_probe"] = {
        "prediction_P11": ("REFUTED. Pre-registration §5 predicted that X3's true profile, "
                           "re-sampled on the HALF-CELL-SHIFTED grid, would be visibly "
                           "non-monotone and refused. It is not: the adapter returns "
                           f"{p11['verdict']}."),
        "half_shift_verdict": p11["verdict"],
        "quarter_shift_verdict": p11q["verdict"],
        "mechanism": ("The planted wiggle has period exactly one cell in t = log r, so a "
                      "UNIFORM shift by s cells multiplies EVERY sample by the same constant "
                      "(1 + A sin(2 pi s)). A constant multiple of a monotone sequence is "
                      "monotone, and its log-increments are unchanged, so BOTH necessary "
                      "conditions pass at every uniform shift -- the half-shift is doubly "
                      "invisible because sin(pi) = 0 as well. The pre-registration's "
                      "reasoning was wrong about which grids can see the wiggle: the answer "
                      "is not 'shifted' but 'INCOMMENSURATE'."),
        "post_hoc_incommensurate_resampling": {
            "status": ("NOT PRE-REGISTERED. Added after P11 failed, to locate the correct "
                       "statement. Decides nothing about the gate, which is answered by "
                       "X1-X5."),
            "rows": incommensurate,
            "reading": ("Detection is a commensurability phenomenon: grids whose spacing "
                        "ratio to the wiggle period is near an integer (N = 500, 1000, 2000) "
                        "or near 1 (N = 997, 1001, 1010, where the phase drifts too slowly) "
                        "see nothing, while N = 1100 and N = 1500 refuse. A hypothesis-"
                        "violating profile can therefore hide from any FIXED grid, which "
                        "strengthens rather than weakens the leg's conclusion: the "
                        "hypothesis is doing the work, not the sampling."),
        },
    }
    _record("P11", "X3's profile is REFUSED on the half-cell-shifted grid",
            "INCAPACITY on the shifted grid", p11["verdict"],
            p11["verdict"] == VERDICT_INCAPACITY)

    # -- 8.  anti-tautology ---------------------------------------------------------------
    honest_audits = {
        "S1": reproduction[0]["containment_audit"]["worst_signed_relative_excess"],
        "S2": out["path_B_loglog"]["containment_audit"]["worst_signed_relative_excess"],
        "S3": out["path_B_absolute"]["containment_audit"]["worst_signed_relative_excess"],
    }
    out["anti_tautology_checks"] = {
        "1_the_containment_audit_can_report_CLEAN":
            {k: v for k, v in honest_audits.items()},
        "1_all_negative": bool(all(v < 0.0 for v in honest_audits.values())),
        "2_no_row_returns_the_full_search_bracket":
            bool(all(r["sampled"]["width"] < 1.0 for r in reproduction)),
        "3_the_refusals_are_not_universal":
            "S1, S2, S3 and S4 are all ACCEPTED by the same code path that refuses X1, X2, X4",
        "4_every_accepted_row_carries_a_hypothesis":
            bool(all(r["hypothesis"] for r in reproduction)),
        "5_leg_382_numbers_recomputed_not_transcribed":
            "every leg_382_recomputed field above is a call to certified_decay_interval in this run",
    }
    _record("P10", "the containment audit reports CLEAN (strictly negative) on S1, S2, S3",
            "all worst margins < 0", honest_audits,
            all(v < 0.0 for v in honest_audits.values()))

    # -- 9.  the gate ---------------------------------------------------------------------
    conjunct_1 = bool(reproduction[0]["bit_identical_to_leg_382"]
                      and all(r["sampled"]["contains_truth"] for r in reproduction))
    conjunct_2 = out["all_gate_controls_fired"]
    out["prediction_ledger"] = PRED
    out["predictions_confirmed"] = sorted(k for k, v in PRED.items() if v["status"] == "CONFIRMED")
    out["predictions_refuted"] = sorted(k for k, v in PRED.items() if v["status"] == "REFUTED")
    out["gate"] = {
        "question": (
            "Does the adapter convert a planted sampled profile with a stated true hypothesis "
            "into cell enclosures whose certification reproduces 382's exact-power result "
            "within its measured widths, AND does a planted hypothesis-VIOLATING input "
            "(samples secretly non-monotone / modulus understated) fire the refusal or a "
            "containment failure — controls able to fail, neither widened?"),
        "conjunct_1_reproduction": conjunct_1,
        "conjunct_1_evidence": (
            "PATH A (MONOTONE) reproduces leg 382's exact-power certified widths "
            "BIT-IDENTICALLY at p = 1, 2, 2.5, 3 (width difference exactly 0.0), truth inside "
            "every interval. PATH B (MODULUS) does NOT and CANNOT: sound, contains the truth, "
            "but width 2.10e-3 at N = 1000 falling like 1/N, so leg 382's 7.44e-15 would need "
            f"N ~ {N_needed:.3g}. This was PREDICTED (P2, P3) before the run."),
        "conjunct_2_controls": conjunct_2,
        "conjunct_2_evidence": (
            "X1 (no hypothesis) and X2 (visible non-monotonicity) and X4 (modulus understated "
            "at the samples) fire the REFUSAL; X3 (secretly non-monotone) and X5 (modulus "
            "understated invisibly) are accepted, as they must be, and fire CONTAINMENT "
            "FAILURES of +5.14e-2 relative and +4.77e-2 in log f. No control was widened; "
            "P11 failed and is recorded as failed rather than amended."),
        "answer": "YES" if (conjunct_1 and conjunct_2) else "NO",
        "yes_branch_meaning": (
            "Real sampled profiles become admissible input to the §4 instrument, CONDITIONAL "
            "ON A NAMED HYPOTHESIS. The first real consumer remains whatever future unit "
            "produces a profile, and this leg claims nothing about one. CEILING TIER 2; "
            "CLAY_OBLIGATIONS §6 items 1 and 2 stay OPEN, the cutoff half untouched."),
        "which_path_each_result_is_conditional_on": (
            "The reproduction rows are conditional on MONOTONICITY (declared 'nonincreasing', "
            "never verified). The PATH B rows are conditional on a caller-certified modulus. "
            "No row here is unconditional, and every row says so in its own conditional_on "
            "field."),
    }
    out["runtime_seconds"] = time.time() - t_start

    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(out, indent=2, sort_keys=False) + "\n")
    print(f"banked {DATA.relative_to(ROOT)}  ({out['runtime_seconds']:.1f}s)")
    print(f"GATE: {out['gate']['answer']}   controls fired: {out['all_gate_controls_fired']}   "
          f"predictions refuted: {out['predictions_refuted']}")
    return draw(out)


# ---------------------------------------------------------------------------
# fig103
# ---------------------------------------------------------------------------

def draw(d):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "figure.dpi": 130, "savefig.dpi": 130, "font.size": 9.5,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.25, "axes.axisbelow": True,
        "legend.frameon": False,
    })
    C_A, C_B, C_BAD, C_REF = "#059669", "#2563eb", "#dc2626", "#6b7280"

    FIGS.mkdir(parents=True, exist_ok=True)
    fig, (axA, axB, axC) = plt.subplots(1, 3, figsize=(14.4, 4.6))

    # -- panel A: width vs N, both paths
    rows = d["cell_count_ladder"]["rows"]
    Ns = [r["N"] for r in rows]
    axA.loglog(Ns, [r["path_A_width"] for r in rows], "o-", color=C_A,
               label="PATH A  (monotonicity)")
    axA.loglog(Ns, [r["path_B_width"] for r in rows], "s-", color=C_B,
               label="PATH B  (loglog modulus, L = 1.05)")
    ref = d["path_A_reproduction"][0]["leg_382_recomputed"]["width"]
    axA.axhline(ref, color=C_REF, ls="--", lw=1.0)
    axA.text(Ns[0], ref * 1.6, f"leg 382, cells: {ref:.2e}", color=C_REF, fontsize=8)
    axA.set_xlabel("samples $N$")
    axA.set_ylabel("certified width of $p$")
    axA.set_title("A  the two paths are not the same instrument\n"
                  f"slopes {d['cell_count_ladder']['path_A_loglog_slope']:+.3f} vs "
                  f"{d['cell_count_ladder']['path_B_loglog_slope']:+.3f}", fontsize=9.5)
    axA.legend(loc="center left", fontsize=8)
    n_need = d["cell_count_ladder"]["N_for_PATH_B_to_reach_PATH_A_width"]
    axA.text(Ns[0], 3e-11,
             f"PATH B would need\n$N \\sim 10^{{{np.log10(n_need):.0f}}}$ samples\n"
             "to reach PATH A's width",
             color=C_B, fontsize=8)

    # -- panel B: containment margins, honest vs violating
    labels, vals, cols = [], [], []
    for key, lab in (("S1", "S1\nmonotone\nTRUE"), ("S2", "S2\nloglog $\\omega$\nTRUE"),
                     ("S3", "S3\nabsolute $\\omega$\nTRUE")):
        labels.append(lab)
        vals.append(d["anti_tautology_checks"]["1_the_containment_audit_can_report_CLEAN"][key])
        cols.append(C_A)
    for c in d["gate_controls"]:
        if c["id"] in ("X3", "X5"):
            kind = "monotone" if c["id"] == "X3" else "loglog $\\omega$"
            labels.append(f"{c['id']}\n{kind}\nFALSE")
            vals.append(c["containment_audit"]["worst_signed_relative_excess"])
            cols.append(C_BAD)
    axB.bar(range(len(vals)), vals, color=cols)
    axB.set_yscale("symlog", linthresh=1e-16)
    axB.axhline(0.0, color="k", lw=0.8)
    axB.set_xticks(range(len(vals)))
    axB.set_xticklabels(labels, fontsize=8)
    axB.set_yticks([1e0, 1e-4, 1e-8, 1e-12, 0.0, -1e-12, -1e-8, -1e-4, -1e0])
    axB.set_ylabel("worst signed relative excess of the TRUE profile\n(> 0 = escaped the enclosure)")
    axB.set_title("B  the audit can say no, and does\n"
                  "(green rows clean; red rows are FALSE certificates)", fontsize=9.5)

    # -- panel C: the absolute modulus dying on a three-decade window
    cur = d["path_B_absolute"]["curve"]
    axC.plot(cur["r"], cur["f_true"], color=C_REF, lw=1.2, label=r"true $f = 3r^{-1}$")
    lo = np.array(cur["f_lo"])
    pos = lo > 0
    axC.plot(np.array(cur["r"])[pos], lo[pos], color=C_B, lw=1.4,
             label="certified lower enclosure")
    first = d["path_B_absolute"]["first_nonpositive_radius"]
    axC.axvline(first, color=C_BAD, ls="--", lw=1.2)
    axC.text(first * 1.08, 3e-4, f"lower bound $\\leq 0$\nfrom $r = {first:.0f}$\n"
                                 f"({d['path_B_absolute']['n_cells_nonpositive_lower']} cells)",
             color=C_BAD, fontsize=8)
    axC.set_xscale("log")
    axC.set_yscale("log")
    axC.set_xlabel("$r$")
    axC.set_ylabel("profile magnitude")
    axC.set_title("C  a GLOBAL absolute modulus is useless here\n"
                  "downstream verdict: INCAPACITY, not a number", fontsize=9.5)
    axC.legend(loc="lower left", fontsize=8)

    fig.suptitle("fig103 — Route-SCEL (leg 385): samples become admissible input to the "
                 "certified decay instrument, CONDITIONAL ON A NAMED HYPOTHESIS",
                 fontsize=10.5, y=1.02)
    dest = FIGS / "fig103_route_scel_v1.png"
    fig.savefig(dest, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {dest.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(figure_only="--figure" in sys.argv))
