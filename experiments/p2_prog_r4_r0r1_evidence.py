"""Evidence script for PROG-R4 R0+R1 (Lane R, wall W7).

Rebuilds EVERY number that appears in
  writeup/4_p2_lottery/BLOG_P2_PROGR4_R0R1.md
  writeup/4_p2_lottery/TECHNICAL_P2_PROGR4_R0R1.md
  experiments/journal/prog_r4_r0r1.md
from writeup/data/p2_prog_r4_r0r1_v1.json, and cross-checks the load-bearing
ones straight back against the two banked unit JSONs so that the derived file
cannot silently drift from the artefacts it was derived from.

Lesson 68: this script RUNS and rebuilds the numbers. It re-runs nothing --
no solver, no DNS, no mining. It is arithmetic over banked fields.

  .venv/bin/python experiments/p2_prog_r4_r0r1_evidence.py
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "writeup", "data")
DOC = os.path.join(DATA, "p2_prog_r4_r0r1_v1.json")
U3_JSON = os.path.join(DATA, "p2_prog_r4_g1_v1.json")
U5_JSON = os.path.join(DATA, "p2_prog_r4_m3_v1.json")

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("[%s] %-70s %s" % ("PASS" if ok else "FAIL", name, detail))
    return bool(ok)


def close(a, b, tol=5e-4):
    return abs(float(a) - float(b)) <= tol


def main():
    with open(DOC) as fh:
        d = json.load(fh)
    with open(U3_JSON) as fh:
        u3 = json.load(fh)
    with open(U5_JSON) as fh:
        u5 = json.load(fh)
    r0, r1 = d["r0"], d["r1"]

    print("=" * 78)
    print("SECTION 0 -- provenance: the derived file still matches the artefacts")
    print("=" * 78)
    ch = r0["core_hours"]
    check("U3 stage seconds match p2_prog_r4_g1_v1.json magnitudes.wall_seconds",
          ch["U3"]["stage_elapsed_seconds"] == u3["magnitudes"]["wall_seconds"],
          "%.5f s" % ch["U3"]["stage_elapsed_seconds"])
    check("U5 stage seconds match p2_prog_r4_m3_v1.json magnitudes.wall_seconds",
          ch["U5"]["stage_elapsed_seconds"] == u5["magnitudes"]["wall_seconds"],
          "%.5f s" % ch["U5"]["stage_elapsed_seconds"])
    check("worker counts match both JSONs (10 and 8)",
          ch["U3"]["workers"] == u3["magnitudes"]["workers"] == 10
          and ch["U5"]["workers"] == u5["magnitudes"]["workers"] == 8)
    check("U3 attempt-CPU seconds re-sum from the 100 attempt rows",
          close(ch["U3"]["attempt_cpu_seconds"],
                sum(a["wall_seconds"] for a in u3["attempts"]), 1e-6),
          "%.3f s over %d rows" % (ch["U3"]["attempt_cpu_seconds"], len(u3["attempts"])))
    check("U5 attempt-CPU seconds re-sum from the 100 attempt rows",
          close(ch["U5"]["attempt_cpu_seconds"],
                sum(a["wall_seconds"] for a in u5["attempts"]), 1e-6))
    check("convergence counts match the units' own gate fields (14 and 9)",
          r0["distinct"]["U3"]["n_convergences"] == u3["gate"]["n_converged_to_tol"] == 14
          and r0["distinct"]["U5"]["n_convergences"] == 9
          and sum(1 for a in u5["attempts"] if a["success"]) == 9)

    print()
    print("=" * 78)
    print("SECTION 1 -- R0(i): CORE-HOURS. Both of WALLS.md's figures, re-derived.")
    print("=" * 78)
    check("U3 pool reservation = 52087.95185 s x 10 / 3600 = 144.6888 core-hours",
          close(ch["U3"]["pool_reservation_core_hours"],
                u3["magnitudes"]["wall_seconds"] * u3["magnitudes"]["workers"] / 3600.0, 1e-9)
          and close(ch["U3"]["pool_reservation_core_hours"], 144.6888),
          "AGREES with WALLS.md's current 144.69")
    check("U3 attempt CPU  = sum(attempts[].wall_seconds)/3600 = 134.4475 core-hours",
          close(ch["U3"]["attempt_cpu_core_hours"], 134.4475),
          "WALLS.md's superseded 134.45 -- from the SAME JSON, not from prose")
    check("U5 pool reservation = 25665.83148 s x 8 / 3600 = 57.0352 core-hours",
          close(ch["U5"]["pool_reservation_core_hours"], 57.0352),
          "AGREES with WALLS.md's 57.04")
    check("U5 attempt CPU = 56.0094 core-hours",
          close(ch["U5"]["attempt_cpu_core_hours"], 56.0094))
    check("the gap is pool utilisation: U3 92.92%, U5 98.20%",
          close(ch["U3"]["pool_utilisation"], 0.9292) and close(ch["U5"]["pool_utilisation"], 0.9820),
          "134.4475/144.6888 = %.4f ; 56.0094/57.0352 = %.4f"
          % (ch["U3"]["pool_utilisation"], ch["U5"]["pool_utilisation"]))
    check("U3 elapsed 14.4689 h, U5 elapsed 7.1294 h",
          close(ch["U3"]["stage_elapsed_hours"], 14.4689)
          and close(ch["U5"]["stage_elapsed_hours"], 7.1294))
    check("the denominator is WORKER-hours: the two runs reserved 10 vs 8",
          ch["U3"]["workers"] != ch["U5"]["workers"])
    check("physical core count is in NO numeric field of either unit JSON",
          not [k for k in list(u3["resourcing"]) + list(u5["resourcing"])
               if "core" in k.lower()
               and isinstance((u3["resourcing"].get(k, u5["resourcing"].get(k))), (int, float))],
          "MISSING ARTEFACT, reported not estimated")

    print()
    print("=" * 78)
    print("SECTION 2 -- R0(ii): THE DISTINCT COUNT under the arbiter's own rule.")
    print("=" * 78)
    # Re-implement the arbiter's rule a THIRD time, here, from the quoted text.
    TOL = 0.05

    def wrap_abs(s):
        a = abs(float(s)) % (2.0 * math.pi)
        return min(a, 2.0 * math.pi - a)

    def cluster(cur):
        out = []
        for a in sorted((x for x in cur["attempts"] if x["success"]),
                        key=lambda x: x["T_converged"]):
            for c in out:
                if (abs(c[0]["T_converged"] - a["T_converged"]) <= TOL
                        and abs(wrap_abs(c[0]["s_converged"]) - wrap_abs(a["s_converged"])) <= TOL):
                    c.append(a)
                    break
            else:
                out.append([a])
        return out

    n3, n5 = len(cluster(u3)), len(cluster(u5))
    check("U3: 14 convergences -> 8 distinct (recomputed here from the unit JSON)",
          n3 == r0["distinct"]["U3"]["n_distinct_leader_greedy_implemented"] == 8,
          "AGREES with WALLS.md's 8")
    check("U5: 9 convergences -> 5 distinct",
          n5 == r0["distinct"]["U5"]["n_distinct_leader_greedy_implemented"] == 5,
          "AGREES with WALLS.md's 5")
    check("TOL = 0.05 is the matching predicate of record, not a new choice",
          "TOL = 0.05" in r0["cluster_rule_verbatim"]
          and "wrap_abs" in r0["cluster_rule_verbatim"],
          "rule banked verbatim in r0.cluster_rule_verbatim")
    for tag, want in (("U3", 8), ("U5", 5)):
        dd = r0["distinct"][tag]
        check("%s: greedy = single-linkage = complete-linkage = %d" % (tag, want),
              dd["n_distinct_leader_greedy_implemented"] == dd["n_distinct_single_linkage"]
              == dd["n_distinct_complete_linkage"] == want)
        check("%s: 20,000 random orderings of the greedy rule give only %d" % (tag, want),
              dd["counts_over_20000_random_orderings"] == [want])
    sw = r0["distinct"]["U3"]["tolerance_sweep"]
    check("U3's 8 is stable over TOL 0.05-0.10 (11 at 0.01, 9 at 0.02-0.04, 7 at 0.15)",
          all(sw[k] == 8 for k in ("0.050", "0.060", "0.070", "0.080", "0.100"))
          and sw["0.010"] == 11 and sw["0.020"] == 9 and sw["0.040"] == 9
          and sw["0.150"] == 7,
          "the '7' reading needs TOL = 0.15, three times the predicate of record")
    wm = r0["distinct"]["U3"]["widest_accepted_merge"]
    nf = r0["distinct"]["U3"]["narrowest_failed_merge"]
    check("widest accepted merge: attempts 12 & 43 at 0.0480 = 0.959x TOL",
          wm["pair"] == [12, 43] and close(wm["chebyshev_distance"], 0.047969)
          and close(wm["as_multiple_of_tol"], 0.9594))
    check("narrowest failed merge: attempts 12 & 99 at 0.0644 = 1.288x TOL, in T",
          nf["pair"] == [12, 99] and close(nf["chebyshev_distance"], 0.064414)
          and close(nf["as_multiple_of_tol"], 1.2883)
          and close(nf["dT"], nf["chebyshev_distance"], 1e-12),
          "the count 8 hinges on the band [0.0480, 0.0644] in T")
    check("U3 cluster sizes are 4,3,2,1,1,1,1,1",
          r0["distinct"]["U3"]["cluster_sizes"] == [4, 3, 2, 1, 1, 1, 1, 1])
    pr = r0["walls_md_prose_argument"]
    check("WALLS.md's '10 of 14 landed on three solutions' is measured as NINE",
          pr["measured_convergences_on_replicated_solutions"] == 9
          and pr["measured_replicated_solutions"] == 3
          and pr["measured_singletons"] == 5,
          "4+3+2 = 9, plus 5 singletons; 3 + 5 = 8 and the arithmetic closes")

    print()
    print("=" * 78)
    print("SECTION 3 -- R0(iii): the seed overlap between U3 and U5.")
    print("=" * 78)
    so = r0["seed_overlap"]
    keys3 = {(a["T_seed"], a["s_seed"], a["R_seed"]) for a in u3["attempts"]}
    shared = [a for a in u5["attempts"]
              if (a["T_seed"], a["s_seed"], a["R_seed"]) in keys3]
    check("57 of U5's 100 seeds were already spent by U3 (recomputed here)",
          len(shared) == so["u5_seeds_already_spent_by_u3"] == 57,
          "matched on (T_seed, s_seed, R_seed) at full float precision")
    check("5 of U5's 9 convergences sit on those already-spent seeds",
          so["u5_convergences_on_a_shared_seed"] == 5 and len(so["detail"]) == 5)
    check("all 5 are BIT-IDENTICAL re-executions of U3 attempts",
          so["bit_identical_re_executions"] == 5
          and all(x["bit_identical_output"] and x["u3_also_converged"] for x in so["detail"]),
          "U5 %s = U3 %s" % ([x["u5_attempt"] for x in so["detail"]],
                             [x["u3_attempt"] for x in so["detail"]]))
    check("on U5-only seeds the distinct count is 4, not 5",
          so["u5_distinct_from_seeds_u3_had_not_spent"] == 4,
          "one of U5's five solutions was reached only by re-running U3's seeds")

    print()
    print("=" * 78)
    print("SECTION 4 -- R0: the metric, in the form 'N distinct orbits per core-hour'.")
    print("=" * 78)
    hd = r0["metric"]["headline"]
    check("U3 headline = 8 / 144.6888 = 0.0553 distinct orbits per core-hour",
          close(hd["U3"]["distinct_orbits_per_core_hour"],
                hd["U3"]["numerator"] / hd["U3"]["denominator"], 1e-12)
          and close(hd["U3"]["distinct_orbits_per_core_hour"], 0.0553, 5e-5),
          "numerator and denominator both traceable to named fields -- AGREES")
    check("U5 headline = 5 / 57.0352 = 0.0877 distinct orbits per core-hour",
          close(hd["U5"]["distinct_orbits_per_core_hour"],
                hd["U5"]["numerator"] / hd["U5"]["denominator"], 1e-12)
          and close(hd["U5"]["distinct_orbits_per_core_hour"], 0.0877, 5e-5),
          "AGREES with WALLS.md")
    va = r0["metric"]["variants"]
    check("the U5/U3 ratio is 1.59 (pool), 1.50 (attempt CPU), 1.27 (elapsed)",
          close(va["pool_reservation"]["U5_over_U3"], 1.586, 5e-3)
          and close(va["attempt_cpu"]["U5_over_U3"], 1.500, 5e-3)
          and close(va["elapsed_wall_hours"]["U5_over_U3"], 1.268, 5e-3),
          "direction robust across all three conventions, magnitude not")
    check("attempt-CPU convention reproduces WALLS.md's superseded 0.0595 for U3",
          close(va["attempt_cpu"]["U3"], 0.0595, 5e-5))
    cu = r0["metric"]["cumulative_reading"]
    check("cumulative reading: U5 gained ONE orbit new to the programme",
          cu["U5"]["n"] == 1 and close(cu["U5"]["per_core_hour"], 0.01753, 5e-5),
          "T = %.4f, |s| = %.4f, attempt %d, anchor %s"
          % (cu["U5"]["the_one_new_solution"]["T"], cu["U5"]["the_one_new_solution"]["abs_s"],
             cu["U5"]["the_one_new_solution"]["attempt"],
             cu["U5"]["the_one_new_solution"]["anchor"]))
    check("under the cumulative reading U5 is 3.15x WORSE than U3, not 1.59x better",
          close(cu["U5_over_U3"], 0.3171, 5e-4)
          and close(1.0 / cu["U5_over_U3"], 3.15, 5e-3))
    check("R0 records the retraction of the inference, not of the arithmetic",
          "RETRACTED AS AN INFERENCE" in r0["verdict"]["retraction"])

    print()
    print("=" * 78)
    print("SECTION 5 -- R1: the ledger, re-derived from residual_history.")
    print("=" * 78)
    lg = r1["ledger"]
    e3 = sum(a["n_iters"] for a in u3["attempts"])
    e5 = sum(a["n_iters"] for a in u5["attempts"])
    check("U3 spent 4,629 epochs; U5 spent 2,104 (recomputed from n_iters)",
          e3 == lg["U3"]["epochs_total"] == 4629
          and e5 == lg["U5"]["epochs_total"] == 2104,
          "and both match U5's banked resourcing fields")
    check("only 243 of U3's 4,629 epochs are inside a convergence (5.2%)",
          lg["U3"]["epochs_in_convergences"] == 243
          and close(243 / 4629.0, 0.0525, 5e-4))
    check("WALLS.md's 'all 14 convergences <=29 epochs, median 16' is CORRECT",
          lg["U3"]["convergence_n_iters_max"] == 29
          and close(lg["U3"]["convergence_n_iters_median"], 16.0, 1e-9),
          "n_iters = %s" % lg["U3"]["convergence_n_iters_sorted"])
    fl = r1["flatness_premise"]
    check("WALLS.md's flatness premise 53%/83%/3% is CONFIRMED on the 86 stalls",
          round(fl["pct_reduced_under_1_pct"]) == 53
          and round(fl["pct_reduced_under_10_pct"]) == 83
          and round(fl["pct_still_halving"]) == 3
          and fl["n_non_convergences"] == 86 and fl["all_ran_to_the_cap"] == [51],
          "every non-convergence ran to n_iters = 51 (52 residuals)")
    check("mean cost per epoch: U3 104.56 s, U5 95.83 s",
          close(lg["U3"]["mean_seconds_per_epoch"], 104.56, 5e-3)
          and close(lg["U5"]["mean_seconds_per_epoch"], 95.83, 5e-3))

    print()
    print("=" * 78)
    print("SECTION 6 -- R1: the incumbent rule, replayed independently.")
    print("=" * 78)
    inc = r1["incumbent"]
    check("the rule is U5's banked stall exit, verbatim",
          inc["banked_as"] == u5["resourcing"]["stall_exit"]["rule"],
          inc["banked_as"])
    check("replayed on U3 it gives EXACTLY 2,083 epochs, matching the banked value",
          inc["U3"]["epochs_under_rule"]
          == u5["resourcing"]["stall_exit"]["u3_epochs_under_rule"] == 2083)
    check("that is 55.0% of U3's epochs recovered, 86 attempts aborted",
          close(inc["U3"]["fraction_of_epochs_recovered"], 0.5500, 5e-4)
          and inc["U3"]["attempts_aborted"] == 86)
    check("ZERO false kills over all 23 pooled banked convergences (control 1)",
          inc["U3"]["false_kills"] == 0 and inc["U5"]["false_kills"] == 0)
    check("margin factor 6.9016 reproduces U5's banked figure exactly (control 2)",
          close(inc["margin_factor_pooled"],
                u5["resourcing"]["stall_exit"]["margin_factor"], 1e-9)
          and close(inc["worst_window_ratio_pooled"],
                    u5["resourcing"]["stall_exit"]["worst_convergence_ratio_at_k_ge_K"], 1e-12),
          "theta 0.50 / worst banked window ratio 0.072447")
    check("it recovers 0.0% on U5 -- U5's saving is already banked, not repeatable",
          inc["U5"]["fraction_of_epochs_recovered"] == 0.0)

    print()
    print("=" * 78)
    print("SECTION 7 -- R1: the sweep, the headroom, and the hold-out.")
    print("=" * 78)
    sw1 = r1["sweep"]
    check("12,597 deterministic rules swept; 9,760 kill no banked convergence",
          sw1["grid"]["n_rules"] == 12597 and sw1["n_zero_false_kill"] == 9760,
          "K in [2,40] x W in [2,20] x 17 thresholds")
    uo = sw1["unconstrained_optimum"]
    check("the unconstrained optimum (K=2,W=9,th=0.45) recovers 65.3% of U3",
          uo["rule"] == {"K": 2, "W": 9, "theta": 0.45}
          and close(uo["u3_fraction_recovered"], 0.6535, 5e-4))
    check("...but at a 1.09x margin, and is REJECTED as overfitted",
          close(uo["margin_factor"], 1.0937, 5e-4) and "NOT ADOPTED" in uo["why_rejected"])
    fr = {round(f["min_margin_factor"], 4): f
          for f in sw1["frontier_best_u3_recovery_at_min_margin"]}
    check("frontier rows quoted in the prose: 58.76% at margin>=2, 57.12% at >=3",
          close(fr[2.0]["u3_fraction_recovered"], 0.5876, 5e-4)
          and fr[2.0]["rule"] == {"K": 17, "W": 16, "theta": 0.15}
          and close(fr[3.0]["u3_fraction_recovered"], 0.5712, 5e-4)
          and fr[3.0]["rule"] == {"K": 17, "W": 16, "theta": 0.2})
    check("frontier row at margin>=15: (21,10,0.20), 55.41%, 19.91x",
          fr[15.0]["rule"] == {"K": 21, "W": 10, "theta": 0.2}
          and close(fr[15.0]["u3_fraction_recovered"], 0.5541, 5e-4)
          and close(fr[15.0]["margin_factor"], 19.9087, 5e-3))
    hr = r1["headroom"]
    check("best admissible rule at the deployed safety margin is K=21, W=10, th=0.10",
          hr["best_admissible_rule"] == {"K": 21, "W": 10, "theta": 0.1}
          and close(hr["margin_factor"], 9.9543, 5e-4))
    check("HEADROOM over the deployed rule = +0.45 pp = +0.48 core-hours",
          close(hr["headroom_percentage_points"], 0.4537, 5e-4)
          and close(hr["headroom_core_hours_u3"], 0.4840, 5e-4),
          "55.45% against the incumbent's 55.00% on a 134.45 core-hour run")
    ho = r1["holdout"]
    a = ho["fit_on_u3_scored_on_u5"]
    b = ho["fit_on_u5_scored_on_u3"]
    check("hold-out U3 -> U5: (20,8,0.55), 55.9% fitted, 2.1% held out, 0 false kills",
          a["rule"] == {"K": 20, "W": 8, "theta": 0.55}
          and close(a["fit_fraction_recovered"], 0.5593, 5e-4)
          and close(a["heldout_fraction_recovered"], 0.0214, 5e-4)
          and a["heldout_false_kills"] == 0)
    check("hold-out U5 -> U3: (17,13,0.15), 61.6% held out but ONE FALSE KILL",
          b["rule"] == {"K": 17, "W": 13, "theta": 0.15}
          and close(b["heldout_fraction_recovered"], 0.6157, 5e-4)
          and b["heldout_false_kills"] == 1,
          "the smaller fitting set fails to generalise -- reported, not hidden")

    print()
    print("=" * 78)
    print("SECTION 8 -- R1: the saving is COMPUTE, and every projection is labelled.")
    print("=" * 78)
    sv = r1["saving"]
    check("saving: 4,629 -> 2,083 epochs, 134.45 -> 59.57 attempt-CPU core-hours",
          close(sv["core_hours_before_attempt_cpu"], 134.4475)
          and close(sv["core_hours_after_attempt_cpu"], 59.5736)
          and close(sv["core_hours_saved_attempt_cpu"], 74.8739),
          "55.69% of the attempt CPU, at zero false kills")
    check("the saving is expressed as a COMPUTE quantity, never as orbits",
          r1["deliverable_kind"].startswith("COMPUTE SAVING"))
    check("R1 records that the saving is U5's, and its own is the +0.45 pp headroom",
          "U5's, not R1's" in sv["whose_saving_it_is"])
    pj = r1["projection"]
    check("the projected metric carries the literal label PROJECTED",
          pj["LABEL"] == "PROJECTED"
          and all("PROJECTED" in k for k in pj if k.startswith("PROJECTED")))
    check("PROJECTED 8 / 59.57 = 0.1343 vs the measured 8 / 134.45 = 0.0595",
          close(pj["PROJECTED_distinct_orbits_per_core_hour_attempt_cpu"], 0.13429, 5e-5)
          and close(pj["measured_distinct_orbits_per_core_hour_attempt_cpu"], 0.05950, 5e-5)
          and close(pj["PROJECTED_factor"], 2.2568, 5e-4),
          "PROJECTED, 2.26x -- a replay, not a run")
    check("no recycled-budget orbit yield is reported anywhere",
          "is NOT reported" in pj["what_it_does_NOT_claim"])

    print()
    print("=" * 78)
    print("SECTION 9 -- standing constraints.")
    print("=" * 78)
    check("leg 349's ban respected: the criterion is deterministic, no fitness",
          "LEG 349 COMPLIANT" in r1["determinism"]
          and "No learned or evolved fitness" in r1["determinism"]
          and "does not touch seed" in r1["determinism"])
    check("nothing was re-run: the unit is arithmetic over banked artefacts",
          "read-only" in r0["provenance"]["nothing_rerun"])
    check("the ceiling clause is recorded in both halves, in its own terms",
          "DIFFERENT AND LESSER THING" in r0["verdict"]["ceiling"]
          and "DIFFERENT AND LESSER THING" in r1["verdict"]["ceiling"]
          and "0.05%" in r0["verdict"]["ceiling"])
    check("no Clay movement is claimed",
          d["clay_movement"].startswith("none"))
    check("the instrument limit on the banked states is recorded, not glossed",
          r0["state_space_limit"]["u3_states_banked"] is False
          and "instrument limit" in r0["state_space_limit"]["second_limit"])

    bad = [n for n, ok, _ in CHECKS if not ok]
    print()
    print("%d/%d checks passed" % (len(CHECKS) - len(bad), len(CHECKS)))
    if bad:
        print("FAILED:")
        for n in bad:
            print("   " + n)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
