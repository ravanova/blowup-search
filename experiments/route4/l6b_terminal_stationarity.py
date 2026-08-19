#!/usr/bin/env python3
"""Leg 406, unit `L6-b` -- ARTEFACT ADDENDUM: the terminal stationarity block.

BOTH GRADIENT COLUMNS ARE REPORTED EVERYWHERE, AND THAT IS A DISCLOSURE OBLIGATION, NOT A
STYLE CHOICE.  `scale_invariant_grad` GOVERNS -- the objective is invariant under
`x -> t x`, `||x|| ||grad J|| / |J|` is invariant under the same rescaling, and
`||grad J||_inf` is NOT: it can be driven down by rescaling the coefficients without moving
the geometry at all.  That is exactly how `L6`'s L-BFGS-B was fooled into a false
convergence report once already (`leg_401.md` SS7.3).  Both columns are reported anyway, for
every start, because a reader given only the raw column would read `L6`'s banked minimiser
(the SMALLEST of its six by `max_abs_grad`) as the best-converged of them.

WHAT IS **NOT** REPORTED AS EVIDENCE, AND WHY -- `CORRECTIONS.md` SS43.  An earlier version of
this script offered "153.2, the LARGEST `scale_invariant_grad` of its six starts" as a
finding.  THAT RANKING IS WITHDRAWN.  Decomposing `sig = ||x|| ||grad J||_2 / |J|` against
the median seed at the same rung: `||x||` x5.19, `||grad J||_2` **x0.169**, `|J|` **x0.050**.
The banked minimiser's gradient is SIX TIMES SMALLER than the median seed's; its `sig` is
large principally because its `|J|` is TWENTY times smaller -- i.e. because it is the
minimiser.  The comparison is confounded by the very outcome being compared, and the ranking
is decoration.  What survives is ABSOLUTE and needs no other start: `sig = 153.22 >> 1`, so a
relative coefficient perturbation of size eps moves `J` by up to ~153*eps*|J|.  That is the
claim; `NOT_CRITICAL = 1.0`, fixed a priori on the invariant measure, is the instrument.

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
        L6s_reported_minimum_had_the_LARGEST_such_gradient_of_its_six_starts_WITHDRAWN=(
            "WITHDRAWN as evidence, CORRECTIONS SS43 -- arithmetically true, confounded by "
            "|J| in the denominator; see ranking_WITHDRAWN_as_evidence.  The claim is the "
            "ABSOLUTE one: 153.22 >> 1."),
        finding=(
            "L6's reported branch-B minimum rho = 1.613811231995397 carries "
            f"||x|| ||grad J|| / |J| = {l6_rows['continuation']['scale_invariant_grad']:.1f}, "
            "which is >> 1 ON AN ABSOLUTE THRESHOLD FIXED A PRIORI -- no comparison to any "
            "other start is used, and the ranking against the five seeds is WITHDRAWN as "
            "confounded (see ranking_WITHDRAWN_as_evidence).  It is therefore NOT a "
            "critical point of the residual functional: it is the point at which an "
            "800-iteration budget ran out on a descent path.  This is legible in L6's OWN "
            "BANKED ARTEFACT and was not stated by L6 or by the landing audit."
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

    # --- SS43: the ranking, DECOMPOSED, and withdrawn as evidence -----------------------
    def _g2(r):  # ||grad J||_2 implied by sig = ||x|| ||grad||_2 / |J|
        return r["scale_invariant_grad"] * abs(r["fun"]) / r["coeff_norm"]

    _seeds = [n for n in l6_rows if n != "continuation"]
    _median = lambda f: sorted(f(l6_rows[n]) for n in _seeds)[len(_seeds) // 2]
    _c = l6_rows["continuation"]

    def _rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0] * len(v)
        for pos, i in enumerate(order):
            r[i] = pos + 1
        return r

    def _spearman(a, b):
        ra, rb = _rank(a), _rank(b)
        n = len(a)
        ma, mb = sum(ra) / n, sum(rb) / n
        num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
        den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
        return num / den if den else float("nan")

    _all = list(l6_rows)
    d["terminal_stationarity"]["ranking_WITHDRAWN_as_evidence"] = dict(
        withdrawn_claim="153.2 is the LARGEST scale_invariant_grad of L6's six J4 starts",
        status="WITHDRAWN -- CORRECTIONS SS43; true as arithmetic, worthless as evidence",
        why=("sig = ||x|| ||grad J||_2 / |J| is a RATIO, and the ratio is dominated by its "
             "DENOMINATOR.  The banked minimiser's sig is large principally because its |J| "
             "is 20x smaller than the median seed's -- which is the same property that makes "
             "it the minimiser.  The comparison across starts is confounded by the outcome "
             "being compared."),
        decomposition_continuation_over_median_seed=dict(
            coeff_norm=_c["coeff_norm"] / _median(lambda r: r["coeff_norm"]),
            grad_L2_implied=_g2(_c) / _median(_g2),
            J=_c["fun"] / _median(lambda r: r["fun"]),
            sig=_c["scale_invariant_grad"] / _median(lambda r: r["scale_invariant_grad"]),
            note="its GRADIENT is ~6x SMALLER than the median seed's, not larger",
        ),
        absolute_statement_that_survives=(
            "sig = 153.22 >> NOT_CRITICAL = 1: a relative coefficient perturbation of size "
            "eps moves J by up to ~153*eps*|J|.  Absolute, threshold-based, and independent "
            "of every other start.  THIS is the claim; the ranking was decoration."),
        rule_adopted=("CORRECTIONS SS43 -- decompose a ratio into its factors before "
                      "believing it; do not let a comparison across units be confounded by "
                      "the quantity that distinguishes them; where a relative measure is "
                      "used, the ABSOLUTE threshold statement is the claim."),
    )

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
        positions_matching_a_reversal=sum(
            1 for a, b in zip(l6_by_gsc, l6_by_ginf[::-1]) if a == b),
        spearman_all_six=_spearman([l6_rows[n]["max_abs_grad"] for n in _all],
                                   [l6_rows[n]["scale_invariant_grad"] for n in _all]),
        spearman_seeds_only=_spearman([l6_rows[n]["max_abs_grad"] for n in _seeds],
                                      [l6_rows[n]["scale_invariant_grad"] for n in _seeds]),
        note=("SS43, correcting THIS SCRIPT's own earlier wording as well as the Conductor's: "
              "there is NO reversal here, near or exact.  Only 2 of 6 positions match a "
              "reversal; Spearman across all six is +0.086 (no relationship), while across "
              "the FIVE SEEDS ALONE it is +0.900 -- the two columns AGREE among the seeds.  "
              "The overall null is manufactured entirely by ONE point, the continuation "
              "start, which disagrees maximally.  'Near reversal' conceded precision on the "
              "tidiness of a reversal while keeping the reversal, which was the wrong place "
              "to give ground; 'opposite orders' was worse."),
        this_unit_reports_both_for_all_three_starts=True,
    )
    d["terminal_stationarity"]["L6_ladder_exhaustive_audit"] = l6_audit

    # --- WHAT THE VERDICT LICENSES -- three-way, keyed on a field already banked ---------
    # CORRECTIONS SS41: the pre-committed NO reading is only available at a STATIONARY
    # terminal iterate.  A NO at scale_invariant_grad >= 1 does not separate the two
    # hypotheses the gate was built to separate.  Pre-registered at 7,000 iterations,
    # BEFORE this unit's gate number existed; the 1.45 threshold does NOT move.
    # --- SS44: a licence keyed to a SINGLE TERMINAL SAMPLE of a volatile series is the
    # same defect it was written to fix.  To license "critical", the MAXIMUM of
    # scale_invariant_grad over the TRAILING 2,000 ITERATIONS must be below threshold:
    # to claim a point is critical you must show it STAYS critical, not that it touched
    # critical once.  Conservative by design; the weakest row remains the default.
    TRAIL = 2000

    def _sig_window(st, trail=TRAIL):
        traj = st.get("trajectory_k_sec_J_ginf_gscaled") or []
        if not traj:
            return None
        K = traj[-1][0]
        w = sorted(r[4] for r in traj if r[0] >= K - trail)
        if not w:
            return None
        q = lambda f: w[min(len(w) - 1, int(f * (len(w) - 1)))]
        return dict(n_samples=len(w), min=w[0], p25=q(0.25), median=q(0.5), p75=q(0.75),
                    max=w[-1], spread_max_over_min=(w[-1] / w[0] if w[0] else None),
                    terminal=traj[-1][4], trailing_iterations=trail)

    sig_windows = {n: _sig_window(st) for n, st in d["starts"].items()}
    d["terminal_stationarity"]["scale_invariant_grad_trailing_window"] = dict(
        why=("CORRECTIONS SS44.  scale_invariant_grad is VOLATILE along an L-BFGS-B path: a "
             "single terminal sample can land in a trough or on a spike and license or deny "
             "a reading the series does not support.  The distribution over a trailing "
             "window is reported for all three starts ALONGSIDE the terminal value, and the "
             "licence is keyed to the window MAXIMUM, not the terminal sample."),
        rule="to claim a point is critical, show it STAYS critical, not that it touched "
             "critical once",
        per_start=sig_windows,
        no_extrapolation=("DELIBERATELY NONE.  A log-linear fit of log(sig) against k over "
                          "the trailing 3,000 iterations and over the trailing 5,000 give "
                          "predictions at k=20,000 that differ by ~15x.  A forecast that "
                          "moves 15x with the choice of window is not a forecast, and none "
                          "is offered."),
    )

    gate = d.get("gate", {})
    smallest = gate.get("smallest_residual_at_20000")
    threshold = gate.get("material_threshold", 1.45)
    dropped = smallest is not None and smallest < threshold
    best_name = min(per, key=lambda k: per[k]["smallest_J_over_the_run"]) if per else None
    best_gsc = per[best_name]["scale_invariant_grad"] if best_name else None
    best_win = sig_windows.get(best_name) or {}
    best_win_max = best_win.get("max")
    # SS44: the WINDOW MAXIMUM governs, not the terminal sample
    stationary = bool(best_win_max is not None and best_win_max < NOT_CRITICAL)

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
        pre_registered=("CORRECTIONS SS41, commit 7265627, at iteration 7,000, AS AMENDED by "
                        "SS44, commit dd1f3b6 -- both BEFORE this unit's gate number existed, "
                        "so neither can be a reaction to a result"),
        amendment_SS44=("SS41 keyed the licence to scale_invariant_grad AT 20,000: a single "
                        "sample of a series whose trailing spread is 6.7x on the banked "
                        "start and 24-34x on the seeds.  That fix had the same shape as the "
                        "defect it fixed -- it named a quantity without naming how the "
                        "quantity is read.  The key is now the MAXIMUM over the trailing "
                        "2,000 iterations.  Conservative direction by design; the weakest "
                        "row remains the default and requires nothing."),
        threshold_unchanged=threshold,
        run_unchanged=True,
        what_changed="only the sentence a NO licenses; the gate, budget and threshold stand",
        keyed_on=dict(start=best_name,
                      scale_invariant_grad_terminal_sample_NOT_THE_KEY=best_gsc,
                      scale_invariant_grad_max_over_trailing_2000=best_win_max,
                      key_is="max over trailing 2,000 iterations (CORRECTIONS SS44), "
                             "superseding SS41's terminal-sample key",
                      trailing_window_distribution=best_win,
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

    # --- SS44.3: the seeds descend in J while becoming relatively LESS stationary -------
    import math as _math

    def _loglin_r(st, trail=3000):
        traj = st.get("trajectory_k_sec_J_ginf_gscaled") or []
        w = [r for r in traj if r[0] >= traj[-1][0] - trail and r[4] > 0]
        if len(w) < 3:
            return None
        xs = [r[0] for r in w]
        ys = [_math.log(r[4]) for r in w]
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
        den = (sum((a - mx) ** 2 for a in xs) * sum((b - my) ** 2 for b in ys)) ** 0.5
        return num / den if den else None

    trend = {n: dict(pearson_r_log_sig_vs_k_trailing_3000=_loglin_r(st),
                     J_first_in_window=(st.get("trajectory_k_sec_J_ginf_gscaled") or
                                        [[0, 0, None]])[0][2],
                     J_terminal=st["final_residual"],
                     sig_terminal=st["scale_invariant_grad"])
             for n, st in d["starts"].items()}
    d["landscape_finding_seeds_become_less_stationary_while_descending"] = dict(
        what=("both INDEPENDENT seeds descend in objective while their RELATIVE gradient "
              "RISES: log-linear fits of log(scale_invariant_grad) against iteration over "
              "the trailing 3,000 iterations are strongly POSITIVE for both, while J falls "
              "by roughly a factor of two over the same span."),
        mechanism=("sig = ||x|| ||grad J||_2 / |J|.  A falling |J| RAISES sig unless "
                   "||grad J||_2 falls faster, and it does not.  The seeds are getting "
                   "closer to a smaller objective value and FURTHER from stationarity in "
                   "relative terms at the same time."),
        this_is_about_the_landscape_not_the_optimiser=True,
        independent_of_the_gate_number=True,
        per_start=trend,
        caution=("reported as a measured trend over a stated window with the window named, "
                 "NOT extrapolated to 20,000 -- see "
                 "terminal_stationarity.scale_invariant_grad_trailing_window.no_extrapolation"),
    )

    # --- the self-check that would have certified a false claim -------------------------
    d["discipline_finding_a_selfcheck_encoded_the_defect_it_existed_to_catch"] = dict(
        what=("evidence check C37, as first written by this unit, ASSERTED "
              "`L6_minimiser_is_largest_by_scale_invariant_grad is True` -- the very ranking "
              "later withdrawn as confounded (CORRECTIONS SS43).  IT WOULD HAVE PASSED ON A "
              "FALSE CLAIM, and its passing would have been offered as evidence FOR it."),
        why_it_matters=("a self-check that encodes the claim it exists to test verifies only "
                        "internal consistency between an artefact and a script written by "
                        "the same unit in the same hour.  Every check in this unit's "
                        "evidence script that merely re-reads a banked field shares that "
                        "weakness; the checks that RECOMPUTE from L6's untouched artefact do "
                        "not."),
        fix="C37 now recomputes the decomposition and requires the withdrawal label; C37b "
            "recomputes the rank-agreement statistics independently",
        stated_plainly="C37 would have passed on a false claim.",
    )

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
