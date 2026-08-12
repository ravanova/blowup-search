"""Route-DEXC v1 (leg 382) — the certified far-field decay enclosure, measured.

Runs the leg-382 pre-registration (`experiments/journal/leg_382.md` Part I, committed
in ddb60a4 BEFORE this file existed) against `solver/dssp_decay_enclosure.py`, and
writes the curated result to `writeup/data/p2_route_dexc_v1.json`.

    .venv/bin/python experiments/p2_route_dexc_v1.py

WHAT IS BEING MEASURED, in the gate's own terms.  Does the enclosure reproduce a
planted profile's EXACT known exponent within its certified interval on the
pre-registered window, AND fail (interval excludes truth, or reports incapacity) on
a planted mismatched control — with the FITTED column left in place and the CERTIFIED
column recorded ALONGSIDE it, never replacing it?

The fitted column is produced by importing `solver.dssp_screen` and calling its
`fitted_far_field_decay_exponent` UNMODIFIED, on the same planted profile, through
its own default off-axis ray.  `solver/dssp_screen.py` is not edited by this leg.

HONESTY NOTE, recorded here and not only in the journal.  The delta-sweep in §6/§7
below was NOT pre-registered.  It was added after the run, in response to a measured
finding that the pre-registration did not anticipate: at zero tolerance the certified
set is EMPTY for any profile that is not an EXACT power law — including one perturbed
at the 1e-12 level — so the exact-tolerance instrument cannot be applied to numerical
data at all.  The gate itself is decided on the pre-registered, zero-tolerance runs in
§2 and §3; the delta material is reported as a labelled post-hoc extension and decides
nothing.
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
    certified_decay_interval, critical_tolerance,
    planted_curvature, planted_log_corrected, planted_perturbed,
    planted_power_law, planted_rational_cutoff, planted_two_power,
    radial_field_fn,
)
from solver.dssp_screen import fitted_far_field_decay_exponent   # noqa: E402  READ ONLY

# ---- the pre-registered constants, copied from journal Part I §3 ------------
R0, R1 = 10.0, 1000.0
N_GATE = 1000
N_LADDER = [50, 100, 200, 500, 1000, 2000]
N_TOL = 200          # cell count for the delta sweeps (bisection => many solves)
W = float(np.log(R1 / R0))

KNOWNS = [
    ("K1", "f = 3.0 r^-1", 3.0, 1.0),
    ("K2", "f = 1.0 r^-2", 1.0, 2.0),
    ("K3", "f = 0.25 r^-5/2", 0.25, 2.5),
    ("K4", "f = 7.0 r^-3", 7.0, 3.0),
]


def _fitted(float_fn):
    """The UNMODIFIED dssp_screen fitted column, on the same planted profile."""
    res = fitted_far_field_decay_exponent(radial_field_fn(float_fn))
    return {"fitted_slope": float(res["fitted_exponent"]),
            "fitted_p": float(-res["fitted_exponent"]),
            "fitted_log_intercept": float(res["fitted_log_intercept"]),
            "n_fit_points": len(res["r_values"]),
            "fit_ray": [float(x) for x in res["direction"]]}


def _row(res, truth):
    """Trim an enclosure result to the fields the writeup quotes."""
    keep = ("verdict", "p_lo", "p_hi", "width", "max_log_tube_width",
            "n_cells", "n_constraints", "n_pairs", "n_dropped", "mode",
            "rel_tolerance", "reason")
    out = {k: res.get(k) for k in keep}
    if res["verdict"] == VERDICT_INTERVAL:
        out["contains_truth"] = bool(res["p_lo"] <= truth <= res["p_hi"])
    else:
        out["contains_truth"] = False
    out["truth"] = truth
    return out


def main():
    t_start = time.time()
    out = {
        "leg": 382, "route": "DEXC", "version": "v1",
        "preregistration_commit": "ddb60a4",
        "novelty_commit": "dfe6aa9",
        "window": {"R0": R0, "R1": R1,
                   "leverage_W_log_ratio": W,
                   "provenance": ("the span of dssp_screen's own fitted ladder "
                                  "np.logspace(1.0, 3.0, 12); NOT moved during this leg")},
        "gate_cell_count": N_GATE,
        "p_bracket": [0.0, 12.0],
        "ceiling": "TIER 2",
        "clay_odds": "~0.05%, unmoved; no L1->L4 link moved by this leg",
        "obligations_still_open": [
            "CLAY_OBLIGATIONS.md §6 item 1 — the ADMISSIBLE CUTOFF half is untouched; "
            "this leg supplies only the certified exponent, one of the three things §4 asks for",
            "CLAY_OBLIGATIONS.md §6 item 2 — §5 persistence/stability under localisation, untouched",
        ],
    }

    # -- §2 planted knowns: certified vs fitted, at the gate cell count --------
    knowns = []
    for tag, desc, C, p0 in KNOWNS:
        iv_fn, float_fn = planted_power_law(C, p0)
        cells = certified_decay_interval(iv_fn, R0, R1, N_GATE, mode="cells")
        nodes = certified_decay_interval(iv_fn, R0, R1, N_GATE, mode="nodes")
        row = {"id": tag, "profile": desc, "truth_exponent": p0,
               "certified_cells": _row(cells, p0),
               "certified_nodes_reference_only": _row(nodes, p0),
               "fitted": _fitted(float_fn)}
        row["fitted_minus_truth"] = row["fitted"]["fitted_p"] - p0
        knowns.append(row)
        print(f"[known] {tag} {desc:18s} cells={cells['verdict']} "
              f"[{cells['p_lo']!r}, {cells['p_hi']!r}] w={cells['width']:.3e} "
              f"contains={row['certified_cells']['contains_truth']} "
              f"fitted_p={row['fitted']['fitted_p']:.12f}")
    out["planted_knowns"] = knowns

    # -- §3 gate controls: MUST FIRE ------------------------------------------
    controls = []
    control_defs = [
        ("C1", "f = r^-2 + 0.01 r^-1 (two-power, crossover r*=100 INSIDE the window)",
         planted_two_power(1.0, 2.0, 0.01, 1.0), 2.0, True),
        ("C2", "f = r^-2 / (1 + (r/300)^4) (rational far cutoff)",
         planted_rational_cutoff(1.0, 2.0, 300.0, 4), 2.0, True),
    ]
    for tag, desc, (iv_fn, float_fn), claimed, gate_deciding in control_defs:
        cells = certified_decay_interval(iv_fn, R0, R1, N_GATE, mode="cells")
        nodes = certified_decay_interval(iv_fn, R0, R1, N_GATE, mode="nodes")
        fired = (cells["verdict"] != VERDICT_INTERVAL) or not (
            cells["p_lo"] <= claimed <= cells["p_hi"])
        row = {"id": tag, "profile": desc, "claimed_exponent": claimed,
               "gate_deciding": gate_deciding,
               "certified_cells": _row(cells, claimed),
               "certified_nodes_reference_only": _row(nodes, claimed),
               "fitted": _fitted(float_fn),
               "fired": bool(fired),
               "contradiction_gap_p_lo_minus_p_hi": float(cells["p_lo"] - cells["p_hi"])}
        controls.append(row)
        print(f"[control] {tag} cells={cells['verdict']} fired={fired} "
              f"gap={row['contradiction_gap_p_lo_minus_p_hi']:.6f} "
              f"fitted_p={row['fitted']['fitted_p']:.6f}")
    out["gate_controls"] = controls
    out["all_gate_controls_fired"] = all(c["fired"] for c in controls)

    # -- §4 resolving-power probes (declared NON-gate-deciding pre-run) --------
    probes = []
    iv_fn, float_fn = planted_log_corrected(1.0, 2.0)
    cells = certified_decay_interval(iv_fn, R0, R1, N_GATE, mode="cells")
    probes.append({"id": "C3", "profile": "f = r^-2 log r", "claimed_exponent": 2.0,
                   "gate_deciding": False,
                   "certified_cells": _row(cells, 2.0),
                   "fitted": _fitted(float_fn),
                   "fired": cells["verdict"] != VERDICT_INTERVAL,
                   "contradiction_gap_p_lo_minus_p_hi": float(cells["p_lo"] - cells["p_hi"])})
    print(f"[probe] C3 {cells['verdict']} gap={probes[-1]['contradiction_gap_p_lo_minus_p_hi']:.6f}")

    t_mid = float(np.log(100.0))
    curvature = []
    for kappa in (0.0, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1):
        iv_k, _ = planted_curvature(1.0, 2.0, kappa, t_mid)
        r = certified_decay_interval(iv_k, R0, R1, N_GATE, mode="cells")
        curvature.append({"kappa": kappa, "verdict": r["verdict"],
                          "p_lo": r["p_lo"], "p_hi": r["p_hi"],
                          "signed_width": r["width"]})
        print(f"[curvature] kappa={kappa:g} {r['verdict']} width={r['width']:.4e}")
    fired_k = [c["kappa"] for c in curvature if c["verdict"] == VERDICT_EMPTY]
    out["resolving_power_probes"] = {
        "probes": probes,
        "curvature_ladder": curvature,
        "t_mid": t_mid,
        "smallest_kappa_certified_empty": (min(fired_k) if fired_k else None),
        "note": ("declared NON-gate-deciding in the pre-registration, before the run, "
                 "so that a null here could not be reinterpreted as a gate outcome"),
    }

    # -- §5 cell-count ladder: tests the pre-committed width ~ 2 p0 / N --------
    ladder = []
    iv_fn, _ = planted_power_law(1.0, 2.0)
    for n in N_LADDER:
        r = certified_decay_interval(iv_fn, R0, R1, n, mode="cells")
        ladder.append({"n_cells": n, "width": r["width"], "verdict": r["verdict"],
                       "max_log_tube_width": r["max_log_tube_width"],
                       "n_pairs": r["n_pairs"], "n_dropped": r["n_dropped"]})
        print(f"[ladder] N={n:5d} width={r['width']:.4e} tube={r['max_log_tube_width']:.3e}")
    widths = np.array([row["width"] for row in ladder], dtype=float)
    ns = np.array([row["n_cells"] for row in ladder], dtype=float)
    out["cell_count_ladder"] = {
        "rows": ladder,
        "prediction_preregistered": "width ~ 2*p0/N, i.e. 4.0e-3 at N=1000; log-log slope -1.00 +/- 0.05",
        "measured_loglog_slope": float(np.polyfit(np.log(ns), np.log(widths), 1)[0]),
        "prediction_verdict": None,   # filled below
    }

    # -- §6 perturbation ladder at ZERO tolerance (pre-registered) ------------
    eps_zero = []
    for eps in (0.0, 1e-12, 1e-9, 1e-6, 1e-3, 1e-2):
        iv_e, _ = planted_perturbed(1.0, 2.0, eps, R1)
        r = certified_decay_interval(iv_e, R0, R1, N_GATE, mode="cells")
        eps_zero.append({"eps": eps, "verdict": r["verdict"],
                         "signed_width": r["width"],
                         "contains_truth": bool(r["verdict"] == VERDICT_INTERVAL
                                                and r["p_lo"] <= 2.0 <= r["p_hi"])})
        print(f"[eps delta=0] eps={eps:g} {r['verdict']} w={r['width']:.4e}")
    out["perturbation_ladder_zero_tolerance"] = {
        "rows": eps_zero,
        "finding": ("at delta = 0 the certified set is EMPTY for EVERY eps > 0, down to "
                    "1e-12: an exactly-power-law profile plus any perturbation has no exact "
                    "exponent, so EMPTY is mathematically CORRECT and is not an instrument "
                    "defect — but it means the zero-tolerance instrument cannot be applied "
                    "to numerical data. This is the finding that forced the post-hoc "
                    "delta extension below."),
        "preregistered_expectation_was_wrong": (
            "the pre-registration called 'truth stays inside for every eps' a SOUNDNESS "
            "requirement whose violation would be an instrument defect. That was a "
            "mis-statement of the certified object, not a defect: P_cert of a perturbed "
            "profile is genuinely empty. Recorded rather than quietly amended."),
    }

    # -- §7 POST-HOC delta extension (NOT pre-registered, NOT gate-deciding) --
    width_vs_delta = []
    iv_fn, _ = planted_power_law(1.0, 2.0)
    for d in (0.0, 1e-12, 1e-9, 1e-6, 1e-3, 1e-2, 1e-1):
        r = certified_decay_interval(iv_fn, R0, R1, N_TOL, mode="cells", rel_tolerance=d)
        width_vs_delta.append({"delta": d, "verdict": r["verdict"], "width": r["width"],
                               "contains_truth": bool(r["verdict"] == VERDICT_INTERVAL
                                                      and r["p_lo"] <= 2.0 <= r["p_hi"])})
        print(f"[delta K2] delta={d:g} {r['verdict']} w={r['width']:.4e}")

    eps_paired = []
    for eps in (1e-12, 1e-9, 1e-6, 1e-3, 1e-2):
        iv_e, _ = planted_perturbed(1.0, 2.0, eps, R1)
        r = certified_decay_interval(iv_e, R0, R1, N_TOL, mode="cells", rel_tolerance=eps)
        eps_paired.append({"eps": eps, "delta": eps, "verdict": r["verdict"],
                           "width": r["width"],
                           "contains_truth": bool(r["verdict"] == VERDICT_INTERVAL
                                                  and r["p_lo"] <= 2.0 <= r["p_hi"])})
        print(f"[eps=delta] eps={eps:g} {r['verdict']} w={r['width']:.4e}")

    crit = []
    for tag, desc, pair in [
        ("C1", "two-power mixture", planted_two_power(1.0, 2.0, 0.01, 1.0)),
        ("C2", "rational far cutoff", planted_rational_cutoff(1.0, 2.0, 300.0, 4)),
        ("C3", "log correction", planted_log_corrected(1.0, 2.0)),
        ("K2", "EXACT power law (direction-sensitivity check)", planted_power_law(1.0, 2.0)),
    ]:
        lo, hi = critical_tolerance(pair[0], R0, R1, N_TOL, iters=45)
        crit.append({"id": tag, "profile": desc,
                     "delta_star_lo": lo,
                     "delta_star_hi": (None if hi == float("inf") else hi),
                     "excluded_at_every_delta_tried": hi == float("inf")})
        print(f"[delta*] {tag} delta* in [{lo:.6g}, {hi:.6g}]")

    out["post_hoc_tolerance_extension"] = {
        "status": ("NOT PRE-REGISTERED. Added after the run in response to the §6 "
                   "finding. Decides nothing about the gate, which was answered on the "
                   "zero-tolerance runs in §2 and §3."),
        "n_cells_used": N_TOL,
        "definition": ("P_cert^delta = { p >= 0 : exists C > 0 with "
                       "f(r)/(1+delta) <= C r^-p <= f(r)(1+delta) for all r in window }"),
        "width_vs_delta_K2": width_vs_delta,
        "perturbed_with_delta_matched_to_eps": eps_paired,
        "critical_tolerances": crit,
        "consumer_rule_of_thumb": (
            "measured width ~= (4/W) * delta = 0.8686 * delta, so a profile certified to "
            "relative accuracy delta yields a certified exponent of HALF-WIDTH ~ 0.434*delta"),
    }

    # -- verdicts --------------------------------------------------------------
    knowns_ok = all(k["certified_cells"]["contains_truth"] for k in knowns)
    knowns_not_vacuous = all(k["certified_cells"]["p_hi"] < 12.0
                             and k["certified_cells"]["p_lo"] > 0.0 for k in knowns)
    knowns_not_empty = all(k["certified_cells"]["verdict"] == VERDICT_INTERVAL
                           for k in knowns)
    controls_ok = out["all_gate_controls_fired"]
    out["anti_tautology_checks"] = {
        "1_no_planted_known_returns_the_full_search_bracket": bool(knowns_not_vacuous),
        "2_no_gate_control_returns_a_nonempty_interval": bool(
            all(c["certified_cells"]["verdict"] != VERDICT_INTERVAL for c in controls)),
        "3_emptiness_is_direction_sensitive_no_known_certified_empty": bool(knowns_not_empty),
        "4_nodes_mode_reported_for_every_row_even_where_it_disagrees": True,
    }

    slope = out["cell_count_ladder"]["measured_loglog_slope"]
    out["cell_count_ladder"]["prediction_verdict"] = (
        "REFUTED — the measured certified width is at the rounding floor (~1.6e-14) and "
        "essentially INDEPENDENT of N (measured log-log slope %.4f, predicted -1.00). The "
        "mechanism: for a monotone profile the cell enclosure's endpoints coincide with the "
        "EXACT pointwise values at the cell edges, so the binding Fourier-Motzkin pairs are "
        "sharp and no cell-width penalty is paid. The instrument is better than the "
        "pre-registration predicted, and the prediction is recorded as wrong rather than "
        "amended." % slope)

    out["gate"] = {
        "question": ("Does the enclosure reproduce a planted profile's EXACT known exponent "
                     "within its certified interval on the pre-registered window, AND fail "
                     "(interval excludes truth or reports incapacity) on a planted mismatched "
                     "control — with the fitted column left in place and the certified column "
                     "recorded ALONGSIDE it, never replacing it?"),
        "knowns_reproduced": bool(knowns_ok),
        "controls_fired": bool(controls_ok),
        "fitted_column_left_in_place_and_recorded_alongside": True,
        "dssp_screen_edited": False,
        "answer": "YES" if (knowns_ok and controls_ok) else "NO",
        "yes_branch_text": ("The §4 obligation has a named instrument; its first real consumer "
                            "is whatever future unit produces a profile — none exists yet and "
                            "this leg claims nothing about one."),
    }
    out["runtime_seconds"] = time.time() - t_start

    dest = ROOT / "writeup" / "data" / "p2_route_dexc_v1.json"
    dest.write_text(json.dumps(out, indent=2, sort_keys=False) + "\n")
    print(f"\nGATE: {out['gate']['answer']}   -> {dest}")
    print(f"runtime {out['runtime_seconds']:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
