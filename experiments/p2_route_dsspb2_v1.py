#!/usr/bin/env python3
"""Leg 350, Route-DSSP brick B2 -- DSSP-BASIS.

Gate (drafted at writeup/4_p2_lottery/TECHNICAL_P2_ROUTEDSSP_V1.md Section 5.1,
brick B2): does an enriched compactified basis resolve the (1-X)^{1-i*kappa}
boundary block at a LOWER mode count than leg 313's measured plain-Chebyshev
baseline (823 at kappa=1, 14149 at kappa=20, n(kappa) ~ 791*kappa^0.954), at
the SAME 1e-6 truncation, with the smooth-control separation (82.3x at the
cheapest kappa != 0 row) reproduced FIRST?

yes -> report the factor and B3 proceeds on the enriched basis.
no  -> report the factor (possibly 1.0) and B3 proceeds on the plain basis at
       the baseline cost, which is then the programme's resolution price.
CEILING: TIER 2 -- a basis is not a certificate; nothing here is a proof or a
Clay claim.

Everything reported below is computed live by solver/dssp_basis.py (a new
module, this brick's territory) so prose cannot drift from the JSON. Leg
313's baseline is READ (via its own measured table, quoted in the plan's
Section 2.6 and reproduced independently here on the identical target
function and truncation instrument -- not imported, not re-cited from a
different branch's file) and never edited; leg 343's B1 record is consumed as
a precondition, not re-litigated.

Runtime: a few seconds. Pure numpy. No scipy.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from solver.dssp_basis import (  # noqa: E402
    DEFAULT_L,
    boundary_block,
    boundary_block_v,
    modes_for_rel_tol,
    smooth_control_v,
    smooth_control_X,
)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_dsspb2_v1.json")

TOL = 1e-6
N_BASELINE = 1 << 20      # matches leg 313's own S3 resolution exactly
N_ENRICHED = 1 << 17      # resolution-study shows this saturates the answer
KAPPAS = [1.0, 2.0, 5.0, 10.0, 20.0]

# leg 313's banked table (branch leg/313-sdss-v1, writeup/data/p2_route_sdss_v1.json,
# quoted verbatim by the plan's Section 2.6) -- reproduced below independently, not
# transcribed on trust.
LEG313_BANKED = {1.0: 823, 2.0: 1482, 5.0: 3564, 10.0: 7086, 20.0: 14149}
LEG313_SMOOTH_MODES = 10
LEG313_COST_LAW = {"prefactor_C": 790.7087311475026, "exponent_q": 0.9540143412913629,
                    "max_rel_residual": 0.03923604963851447}

selftests: list[dict] = []


def check(name: str, ok: bool, detail: str) -> None:
    selftests.append({"name": name, "pass": bool(ok), "detail": detail})


def main() -> int:
    # ------------------------------------------------------------------
    # STEP 0 (FIRST, before anything else): reproduce the smooth-control
    # separation on the plain-X baseline instrument -- the sanity check that
    # this leg is working against the SAME baseline leg 313/343 measured.
    # ------------------------------------------------------------------
    n_smooth_baseline = modes_for_rel_tol(smooth_control_X, N_BASELINE, TOL)
    n_k1_baseline = modes_for_rel_tol(lambda X: boundary_block(X, 1.0), N_BASELINE, TOL)
    sep = n_k1_baseline / n_smooth_baseline
    check("STEP0.1 smooth control needs 10 modes at 1e-6 on the plain-X basis "
          "(leg 313's own number, reproduced)",
          n_smooth_baseline == LEG313_SMOOTH_MODES, f"measured {n_smooth_baseline}")
    check("STEP0.2 kappa=1 needs 823 modes at 1e-6 on the plain-X basis "
          "(leg 313's own number, reproduced)",
          n_k1_baseline == LEG313_BANKED[1.0], f"measured {n_k1_baseline}")
    check("STEP0.3 the 82.3x smooth-control separation at the cheapest kappa!=0 "
          "row is reproduced FIRST, before the enriched basis is touched",
          abs(sep - 82.3) < 0.1, f"measured {sep:.4f}x")

    # ------------------------------------------------------------------
    # STEP 1: full plain-X baseline table, every measured kappa row, on the
    # exact same instrument (N=2^20, 1e-6 relative tail truncation) leg 313
    # used -- so the enrichment factor below is computed against a number
    # this leg measured itself, not a cited one.
    # ------------------------------------------------------------------
    baseline_modes = {}
    for kap in KAPPAS:
        n = modes_for_rel_tol(lambda X, kap=kap: boundary_block(X, kap), N_BASELINE, TOL)
        baseline_modes[kap] = n
        check(f"STEP1 kappa={kap} plain-X baseline matches leg 313's banked "
              f"{LEG313_BANKED[kap]}",
              n == LEG313_BANKED[kap], f"measured {n}")

    # ------------------------------------------------------------------
    # STEP 2: the enriched basis. ONE fixed map scale L, chosen by a small
    # sweep (reported, not hidden) and then frozen -- the comparison below
    # is on a SINGLE instrument across every kappa row, not five tuned ones.
    # ------------------------------------------------------------------
    L_sweep_grid = [0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0]
    N_sweep = 1 << 15
    sweep_rows = {}
    for kap in KAPPAS:
        row = {}
        for L in L_sweep_grid:
            n = modes_for_rel_tol(lambda v, kap=kap, L=L: boundary_block_v(v, kap, L),
                                   N_sweep, TOL)
            row[str(L)] = n
        sweep_rows[str(kap)] = row
    check("STEP2.1 the L-sweep is not empty and every row has at least one "
          "finite entry", all(any(v > 0 for v in r.values()) for r in sweep_rows.values()),
          f"{len(sweep_rows)} kappa rows swept over L in {L_sweep_grid}")

    L_FIXED = DEFAULT_L
    check("STEP2.2 L=16.0 (frozen, used for every kappa row below) is at or "
          "within 5% of the best mode count the sweep found, for every kappa "
          "-- so freezing it costs almost nothing",
          all(sweep_rows[str(kap)][str(L_FIXED)]
              <= 1.05 * min(v for v in sweep_rows[str(kap)].values() if v > 0)
              for kap in KAPPAS),
          "; ".join(f"kappa={kap}: L=16 -> {sweep_rows[str(kap)][str(L_FIXED)]}, "
                    f"best -> {min(v for v in sweep_rows[str(kap)].values() if v > 0)}"
                    for kap in KAPPAS))

    enriched_modes = {}
    for kap in KAPPAS:
        n = modes_for_rel_tol(lambda v, kap=kap: boundary_block_v(v, kap, L_FIXED),
                               N_ENRICHED, TOL)
        enriched_modes[kap] = n
        check(f"STEP2.3 kappa={kap} enriched basis (L={L_FIXED}) resolves at "
              f"< the plain-X baseline ({baseline_modes[kap]})",
              0 < n < baseline_modes[kap], f"measured {n}")

    # ------------------------------------------------------------------
    # STEP 3: resolution stability of the enriched-basis mode counts (leg
    # 313's own S3.7 lesson, carried to the new instrument).
    # ------------------------------------------------------------------
    stability = {}
    for kap in KAPPAS:
        rows = {}
        for N in (1 << 14, 1 << 15, 1 << 16, 1 << 17):
            rows[str(N)] = modes_for_rel_tol(
                lambda v, kap=kap: boundary_block_v(v, kap, L_FIXED), N, TOL)
        stability[str(kap)] = rows
    check("STEP3 the enriched mode counts are stable (identical) across an 8x "
          "resolution range for every kappa row -- measures the object, not "
          "the array",
          all(len(set(rows.values())) == 1 for rows in stability.values()),
          "; ".join(f"kappa={kap}: {stability[str(kap)]}" for kap in KAPPAS))

    # ------------------------------------------------------------------
    # STEP 4: kappa=0 control on both instruments (lesson 90: must be able to
    # come out differently -- and does, since it is exact/terminating on
    # plain-X but not on the v-map, which is expected and reported, not
    # hidden).
    # ------------------------------------------------------------------
    n0_baseline = modes_for_rel_tol(lambda X: boundary_block(X, 0.0), N_BASELINE, TOL)
    n0_enriched = modes_for_rel_tol(lambda v: boundary_block_v(v, 0.0, L_FIXED),
                                     N_ENRICHED, TOL)
    check("STEP4 kappa=0 control: baseline is near-exact (a linear polynomial "
          "in X terminates at essentially 2 modes); the SAME object costs "
          "more under the v-map (expected: the map exists to buy the kappa!=0 "
          "boundary defect, not to compress an already-polynomial function)",
          n0_baseline <= 3 and n0_enriched > n0_baseline,
          f"baseline={n0_baseline}, enriched={n0_enriched}")

    # ------------------------------------------------------------------
    # STEP 5: FALSIFICATION CONTROL -- a function with NO boundary
    # singularity, carried through the SAME v-map, must get WORSE, not
    # better. If it didn't, the enrichment factor below would be a
    # transform artefact rather than a property of matching basis to
    # singularity.
    # ------------------------------------------------------------------
    n_smooth_enriched = modes_for_rel_tol(lambda v: smooth_control_v(v, L_FIXED),
                                           N_ENRICHED, TOL)
    check("STEP5 FALSIFICATION CONTROL: the smooth control (no boundary "
          "singularity) costs MORE modes under the v-map than on plain-X "
          "directly -- the enrichment is not a universal free lunch",
          n_smooth_enriched > n_smooth_baseline,
          f"plain-X={n_smooth_baseline}, v-mapped={n_smooth_enriched}")

    # ------------------------------------------------------------------
    # STEP 6: the enrichment factor, per row and overall -- this IS the gate.
    # ------------------------------------------------------------------
    factors = {kap: baseline_modes[kap] / enriched_modes[kap] for kap in KAPPAS}
    gate_yes = all(enriched_modes[kap] < baseline_modes[kap] for kap in KAPPAS)
    check("GATE all five measured kappa rows resolve at a lower mode count on "
          "the enriched basis than leg 313's plain-Chebyshev baseline, at the "
          "identical 1e-6 truncation",
          gate_yes,
          "; ".join(f"kappa={kap}: {baseline_modes[kap]} -> {enriched_modes[kap]} "
                    f"({factors[kap]:.2f}x)" for kap in KAPPAS))

    n_pass = sum(1 for t in selftests if t["pass"])
    payload = {
        "leg": 350,
        "route": "DSSP",
        "brick": "B2 (DSSP-BASIS)",
        "gate_pre_committed": (
            "does an enriched compactified basis resolve the (1-X)^{1-i*kappa} "
            "boundary block at a lower mode count than leg 313's measured "
            "plain-Chebyshev baseline (823 at kappa=1, 14149 at kappa=20), at "
            "the same 1e-6 truncation, with the smooth-control separation "
            "82.3x at the cheapest kappa!=0 row reproduced first?"),
        "gate_answer": "YES" if gate_yes else "NO",
        "branch_taken": (
            "enrichment factor reported; B3 proceeds on the enriched basis"
            if gate_yes else
            "enrichment factor reported (possibly 1.0); B3 proceeds on the "
            "plain basis at the baseline cost, which is the programme's "
            "resolution price"),
        "ceiling": "TIER 2 -- a basis is not a certificate; nothing here is a "
                   "proof or a Clay claim",
        "step0_smooth_control_reproduced_first": {
            "plain_X_smooth_modes_1e-6": n_smooth_baseline,
            "plain_X_kappa1_modes_1e-6": n_k1_baseline,
            "separation": sep,
            "leg313_banked_separation": 82.3,
        },
        "step1_full_baseline_table_reproduced": {
            "N_modes_used": N_BASELINE,
            "rows": {str(k): v for k, v in baseline_modes.items()},
            "leg313_banked_rows": {str(k): v for k, v in LEG313_BANKED.items()},
            "leg313_cost_law": LEG313_COST_LAW,
        },
        "step2_enriched_basis": {
            "construction": ("u = -log(1-X)  (log-compactification, sends the "
                              "boundary branch point to an entire exponential); "
                              "v = u/(u+L)  (Boyd algebraic map, u in [0,inf) to "
                              "v in [0,1)); Chebyshev-in-v with L fixed"),
            "L_sweep_grid": L_sweep_grid,
            "L_sweep_N": N_sweep,
            "L_sweep_rows": sweep_rows,
            "L_fixed_used_for_every_kappa": L_FIXED,
            "N_modes_used": N_ENRICHED,
            "rows": {str(k): v for k, v in enriched_modes.items()},
        },
        "step3_resolution_stability": stability,
        "step4_kappa0_control": {
            "plain_X_modes_1e-6": n0_baseline,
            "v_mapped_modes_1e-6": n0_enriched,
        },
        "step5_falsification_control_smooth_function_under_the_map": {
            "plain_X_modes_1e-6": n_smooth_baseline,
            "v_mapped_modes_1e-6": n_smooth_enriched,
            "got_worse_as_required": bool(n_smooth_enriched > n_smooth_baseline),
        },
        "step6_enrichment_factor": {
            "per_kappa": {str(k): v for k, v in factors.items()},
            "min": min(factors.values()),
            "max": max(factors.values()),
        },
        "walls": {
            "clay_odds": "~0.05%, unchanged",
            "links_of_L1_to_L4_moved": 0,
        },
        "selftests": selftests,
        "selftests_passed": f"{n_pass}/{len(selftests)}",
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)

    for t in selftests:
        print(("PASS " if t["pass"] else "FAIL ") + t["name"] + " :: " + t["detail"])
    print(f"\n{n_pass}/{len(selftests)} self-tests pass -> {OUT}")
    print(f"\nGATE: {payload['gate_answer']}  |  enrichment factor "
          f"{payload['step6_enrichment_factor']['min']:.1f}x - "
          f"{payload['step6_enrichment_factor']['max']:.1f}x")
    return 0 if n_pass == len(selftests) else 1


if __name__ == "__main__":
    sys.exit(main())
