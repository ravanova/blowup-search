#!/usr/bin/env python3
"""Leg 406, unit `L6-b` -- ARTEFACT ADDENDUM: the terminal stationarity block.

BOTH GRADIENT COLUMNS ARE REPORTED EVERYWHERE, AND THAT IS A DISCLOSURE OBLIGATION, NOT A
STYLE CHOICE.  `scale_invariant_grad` GOVERNS -- the objective is invariant under
`x -> t x`, `||x|| ||grad J|| / |J|` is invariant under the same rescaling, and
`||grad J||_inf` is NOT: it can be driven down by rescaling the coefficients without moving
the geometry at all.  That is exactly how `L6`'s L-BFGS-B was fooled into a false
convergence report once already (`leg_401.md` SS7.3).  But the correct column governing is
not a licence to quote it alone: at `L6`'s own `J4` rung the two columns rank its six starts
in near-opposite orders, and its banked minimiser is the SMALLEST of the six by
`max_abs_grad` (252.2, against seeds 792-2,501) while being the LARGEST by
`scale_invariant_grad` (153.2, against seeds 4.65-16.58).  A reader given only the raw
column concludes the exact opposite of the truth.  So both go in, every time, with the
invariance argument attached.

`V-W6`'s recommendation, made binding by the Conductor mid-run and recorded in
`experiments/journal/leg_406.md` SS7.7 BEFORE the gate number existed: report the TERMINAL
`max_abs_grad` AND `scale_invariant_grad` at each of the three starts, not only rho and not
only J.  A residual reported at a point with a large scale-invariant gradient is a point on
a descent path, not a critical point, and the artefact must say so on its face.

This is a separate script rather than a change to `p2_route_l6b_v1.py` for one reason,
stated so it is not mistaken for convenience: THE PRODUCTION RUN WAS ALREADY LIVE when the
requirement arrived.  Editing the running module would not have affected the running
interpreter, and restarting the run to pick the edit up would have thrown away hours of the
gate's own budget.  Every number this script writes is COPIED from fields the run itself
banked (`starts.<name>.max_abs_grad`, `.scale_invariant_grad`, `.final_residual`,
`.coeff_norm`, `.iterations`, `.hit_maxiter`) -- it computes no new science, and the
comparison row for `L6` is read out of `L6`'s untouched artefact.

Idempotent: rerunning it reproduces the same block and the same `self_hash`.

    .venv/bin/python experiments/route4/l6b_terminal_stationarity.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "writeup" / "data" / "p2_route_l6b_v1.json"
L6_ART = ROOT / "writeup" / "data" / "p2_route_l6_profile_v1.json"

# a scale-invariant stationarity measure this large is not a critical point by any reading;
# fixed here rather than chosen against the numbers
NOT_CRITICAL = 1.0


def main():
    d = json.loads(ART.read_text())
    d6 = json.loads(L6_ART.read_text())

    l6_top = d6["ladder_results"]["B"][-1]
    l6_rows = {s["start"]: s for s in l6_top["starts"]}

    per = {}
    for name, st in d["starts"].items():
        per[name] = dict(
            J_terminal=st["final_residual"],
            smallest_J_over_the_run=st["smallest_residual_at_20000"],
            max_abs_grad=st["max_abs_grad"],
            scale_invariant_grad=st["scale_invariant_grad"],
            coeff_norm=st["coeff_norm"],
            iterations=st["iterations"],
            hit_maxiter=st["hit_maxiter"],
            is_a_critical_point=bool(st["scale_invariant_grad"] < NOT_CRITICAL),
        )

    still_descending = {
        n: bool(v["hit_maxiter"] and not v["is_a_critical_point"]) for n, v in per.items()
    }
    banked = per.get("banked_J4_minimiser", {})
    verdict = bool(banked.get("hit_maxiter") and not banked.get("is_a_critical_point", True))

    d["terminal_stationarity"] = dict(
        why=("V-W6's binding recommendation: a residual is not a result on its own.  The "
             "terminal gradient says whether the number is a critical point of the "
             "residual functional or a point on a descent path at which the budget ran "
             "out.  Reported for all three starts, whichever way the gate answers."),
        measure="scale_invariant_grad = ||x||_2 ||grad J||_2 / |J|, invariant under x -> t x "
                "(the objective is scale-invariant: leg_401.md SS7.3)",
        not_a_critical_point_above=NOT_CRITICAL,
        per_start=per,
        starts_still_descending_at_the_cap=still_descending,
        L6_same_quantities_at_its_own_J4_rung={
            n: dict(J=r["fun"], max_abs_grad=r["max_abs_grad"],
                    scale_invariant_grad=r["scale_invariant_grad"],
                    coeff_norm=r["coeff_norm"], nit=r["nit"],
                    hit_maxiter=r["hit_maxiter"])
            for n, r in l6_rows.items()},
        L6s_reported_minimum_was_never_a_critical_point=bool(
            l6_rows["continuation"]["scale_invariant_grad"] >= NOT_CRITICAL),
        L6s_reported_minimum_scale_invariant_grad=l6_rows["continuation"]["scale_invariant_grad"],
        L6s_reported_minimum_had_the_LARGEST_such_gradient_of_its_six_starts=bool(
            l6_rows["continuation"]["scale_invariant_grad"]
            == max(r["scale_invariant_grad"] for r in l6_rows.values())),
        finding=(
            "L6's reported branch-B minimum rho = 1.613811231995397 carries "
            f"||x|| ||grad J|| / |J| = {l6_rows['continuation']['scale_invariant_grad']:.1f}, "
            "the LARGEST of all six starts at its own J4 rung (the five seeds read "
            "4.65-16.58).  It is therefore NOT a critical point of the residual "
            "functional: it is the point at which an 800-iteration budget ran out on a "
            "descent path.  This is legible in L6's OWN BANKED ARTEFACT and was not "
            "stated by L6 or by the landing audit."
            + ("  THE SAME IS TRUE OF THIS UNIT AT 20,000: the banked_J4_minimiser start "
               "is still at the cap and still not a critical point, so this unit's own "
               "number is likewise a stopping point and NOT an infimum."
               if verdict else
               "  At 20,000 this unit's banked_J4_minimiser start did NOT end at the cap "
               "in a non-critical state, so the qualification above does not extend to "
               "this unit's own number in the same form; see per_start.")),
    )

    # --- the EXHAUSTIVE fact about L6's ladder, verified here from L6's own artefact -----
    # not taken on report: every start-record in the banked profile is re-counted.
    l6_all = []
    for br, rungs in d6["ladder_results"].items():
        for ru in rungs:
            for st in ru.get("starts", []):
                l6_all.append((br, st["start"], st["nit"], st["fun"],
                               st["max_abs_grad"], st["scale_invariant_grad"]))
    l6_noncrit = [r for r in l6_all if r[5] >= NOT_CRITICAL]
    l6_audit = dict(
        start_records=len(l6_all),
        distinct_nit_values=sorted({r[2] for r in l6_all}),
        every_record_hit_the_800_cap=bool(all(r[2] == 800 for r in l6_all)),
        records_not_critical_at_threshold_1=len(l6_noncrit),
        the_two_that_are_critical=[dict(branch=r[0], start=r[1], J=r[3],
                                        scale_invariant_grad=r[5])
                                   for r in l6_all if r[5] < NOT_CRITICAL],
        finding=("ALL 58 non-angular start-records in L6's banked profile -- both branches, "
                 "every rung -- have nit == 800.  100% hit the iteration cap; NOT ONE "
                 "terminated on a convergence criterion, and 56 of 58 are non-critical at "
                 "threshold 1.  L6 conceded its headline was not the infimum; its own "
                 "artefact supports the stronger statement that the ladder never located a "
                 "stationary point ANYWHERE, and therefore compared STOPPING POINTS across "
                 "rungs.  A refinement ladder built from stopping points measures the "
                 "budget as much as the ansatz."),
        verified_by="this script, recounted from p2_route_l6_profile_v1.json, not quoted",
    )

    l6_by_ginf = sorted(l6_rows, key=lambda n: l6_rows[n]["max_abs_grad"])
    l6_by_gsc = sorted(l6_rows, key=lambda n: l6_rows[n]["scale_invariant_grad"])
    d["terminal_stationarity"]["the_two_columns_rank_differently"] = dict(
        why_both_are_reported=("scale_invariant_grad governs, because the objective is "
                               "invariant under x -> t x and so is ||x||||grad J||/|J|, "
                               "while ||grad J||_inf is not and can be driven down by "
                               "rescaling coefficients without moving the geometry "
                               "(leg_401.md SS7.3).  Quoting the governing column ALONE is "
                               "still selection: the raw column points the other way here."),
        L6_J4_rank_by_max_abs_grad_ascending=l6_by_ginf,
        L6_J4_rank_by_scale_invariant_grad_ascending=l6_by_gsc,
        L6_minimiser_is_smallest_by_max_abs_grad=bool(l6_by_ginf[0] == "continuation"),
        L6_minimiser_is_largest_by_scale_invariant_grad=bool(l6_by_gsc[-1] == "continuation"),
        exact_reversal=bool(l6_by_ginf == l6_by_gsc[::-1]),
        note=("the reversal is NEAR-exact, not exact: seed401 and seed402 transpose between "
              "the two orderings.  Stated precisely rather than rounded up to 'opposite'."),
        this_unit_reports_both_for_all_three_starts=True,
    )
    d["terminal_stationarity"]["L6_ladder_exhaustive_audit"] = l6_audit

    # --- WHAT THE VERDICT LICENSES -- three-way, keyed on a field already banked ---------
    # CORRECTIONS SS41: the pre-committed NO reading is only available at a STATIONARY
    # terminal iterate.  A NO at scale_invariant_grad >= 1 does not separate the two
    # hypotheses the gate was built to separate.  Pre-registered at 7,000 iterations,
    # BEFORE this unit's gate number existed; the 1.45 threshold does NOT move.
    gate = d.get("gate", {})
    smallest = gate.get("smallest_residual_at_20000")
    threshold = gate.get("material_threshold", 1.45)
    dropped = smallest is not None and smallest < threshold
    best_name = min(per, key=lambda k: per[k]["smallest_J_over_the_run"]) if per else None
    best_gsc = per[best_name]["scale_invariant_grad"] if best_name else None
    stationary = bool(best_gsc is not None and best_gsc < NOT_CRITICAL)

    if dropped:
        row, licence = "drop_below_1.45", (
            "THE PRE-COMMITTED YES READING IN FULL: L6's ladder was measuring the OPTIMISER "
            "BUDGET, not the ansatz.  The refinement NO is then NOT a statement about route "
            "4, and the L7/L4 prices re-open.  Unaffected by stationarity: a drop below "
            "1.45 proves budget-limitation whether or not 20,000 iterations converged.")
    elif stationary:
        row, licence = "no_drop_and_stationary", (
            "THE PRE-COMMITTED NO READING IN FULL: the stall is the CONSTRUCTION, not the "
            "budget, and route 4's NO hardens into a real result about the ansatz.  "
            "Available because the terminal iterate IS critical at threshold 1.")
    else:
        row, licence = "no_drop_and_NOT_stationary", (
            "ONLY THIS, AND NOTHING STRONGER: '25x L6's budget, still not stationary -- "
            "budget alone does not reach 1.45.'  The L7/L4 prices stay OPEN.  The ansatz is "
            "NEITHER EXONERATED NOR CONVICTED.  The pre-committed NO sentence is NOT "
            "available here: it requires a stationary terminal iterate, and the plan's "
            "wording never required one.  A NO at scale_invariant_grad ~ 10^2 says the "
            "optimiser was still descending when the cap arrived, which is BUDGET-LIMITED "
            "-- the very hypothesis the NO was meant to eliminate.")

    d["verdict_licence"] = dict(
        pre_registered=("CORRECTIONS SS41, commit 7265627, at iteration 7,000 -- BEFORE this "
                        "unit's gate number existed, so it cannot be a reaction to a result"),
        threshold_unchanged=threshold,
        run_unchanged=True,
        what_changed="only the sentence a NO licenses; the gate, budget and threshold stand",
        keyed_on=dict(start=best_name, scale_invariant_grad=best_gsc,
                      not_critical_above=NOT_CRITICAL,
                      smallest_residual_at_20000=smallest, dropped_below_1_45=dropped,
                      terminal_iterate_is_stationary=stationary),
        row_that_fires=row,
        licence=licence,
        the_gate_was_sound_in_one_direction_and_defective_in_the_other=(
            "The YES branch is untouched.  The NO branch, as written in WAVE7_PLAN, asserted "
            "'the stall is the CONSTRUCTION' from a non-stationary stopping point, which "
            "does not follow.  Gates can be half-defective; this one was."),
    )

    # the driver banked WAVE7_PLAN's ORIGINAL NO sentence inline at gate.reading_that_fires.
    # It is left in place -- the artefact does not rewrite its own history -- but it is
    # flagged here, because in the no_drop_and_NOT_stationary row that sentence CLAIMS MORE
    # THAN THE RUN SUPPORTS.
    if "gate" in d:
        superseded = bool(row == "no_drop_and_NOT_stationary")
        d["gate"]["reading_that_fires_is_SUPERSEDED"] = superseded
        d["gate"]["reading_that_fires_superseded_by"] = (
            "verdict_licence.licence (CORRECTIONS SS41, pre-registered at iteration 7,000). "
            "The plan's original NO sentence asserts the stall is the CONSTRUCTION; that "
            "inference requires a stationary terminal iterate and this run did not reach "
            "one." if superseded else
            "not superseded: the row that fires supports the plan's own sentence in full")

    d.pop("self_hash", None)
    d["self_hash"] = hashlib.sha256(
        json.dumps(d, sort_keys=True).encode()).hexdigest()[:16]
    ART.write_text(json.dumps(d, indent=1, sort_keys=True))
    print(f"terminal_stationarity written; self_hash={d['self_hash']}")
    for n, v in per.items():
        print(f"  {n:24s} J={v['J_terminal']!r:22s} |g|inf={v['max_abs_grad']:.4g}  "
              f"gscaled={v['scale_invariant_grad']:.4g}  "
              f"critical_point={v['is_a_critical_point']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
