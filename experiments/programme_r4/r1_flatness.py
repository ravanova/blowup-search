"""PROG-R4 unit R1 -- EARLY ABORT ON FLATNESS, measured on the banked ledgers.

WALLS.md, Lane R, names this unit "R1 -- early abort on flatness. *Cheapest
competitive win in the repository, and it is measured.*" and asks for the
recoverable fraction to be estimated from U3's banked ledger BEFORE building
it, with a control that the criterion never kills an attempt U3's ledger shows
would have converged. The given filename r1_flatness.py already matches that
name, so no rename was needed.

ITS DELIVERABLE IS A COMPUTE SAVING, NOT ORBITS. Every quantity below is
epochs or core-hours. Any orbit yield is a PROJECTION and is labelled
PROJECTED in this file, in the JSON, in the figure and in the prose.

THE CRITERION FAMILY (deterministic; leg 349's ban is in force and respected --
there is no learned or evolved fitness anywhere here, nothing is fitted by a
search over seeds, and the rule never touches seed SELECTION, only when an
already-launched attempt stops):

    abort at epoch k  iff  k >= K  and  ||R||_k > theta * ||R||_{k-W}

three integers-and-a-float, evaluated by replaying residual_history from the
banked JSONs. THE MEASUREMENT IS A REPLAY. No solver runs. No DNS runs.

TWO CONTROLS, both demanded by WALLS.md and both reported whether they pass
or fail:
  (1) FALSE KILLS. A rule is admissible only if, replayed over every banked
      convergence in BOTH units, it aborts none of them.
  (2) SAFETY MARGIN. Zero false kills on 23 convergences is a weak statement.
      The margin factor is theta divided by the worst window ratio any banked
      convergence actually exhibited in the region the rule inspects: how many
      times worse a future convergence could behave before the rule kills it.

AND ONE THIS UNIT ADDS, because WALLS.md did not ask for it and it is the one
that decides whether the answer generalises:
  (3) HOLD-OUT BOTH WAYS. Select the rule on one unit's ledger, score it on
      the other's. Reported below including the direction that FAILS.

  .venv/bin/python experiments/programme_r4/r1_flatness.py [--write]
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "writeup", "data")
U3_JSON = os.path.join(DATA, "p2_prog_r4_g1_v1.json")
U5_JSON = os.path.join(DATA, "p2_prog_r4_m3_v1.json")
OUT = os.path.join(DATA, "p2_prog_r4_r0r1_v1.json")

# The rule U5 already deployed, quoted from p2_prog_r4_m3_v1.json's
# resourcing.stall_exit.rule: "from epoch 20, stop if ||R||_k > 0.5 * ||R||_(k-10)"
INCUMBENT = (20, 10, 0.5)

THETAS = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50,
          0.55, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99]
GRID = [(K, W, th) for K in range(2, 41) for W in range(2, 21) for th in THETAS]

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-66s %s" % ("ok" if ok else "FAIL", name, detail))
    return bool(ok)


def series(cur):
    """One tuple per attempt: (id, converged?, epochs, residuals, wall seconds)."""
    return [(a["attempt"], bool(a["success"]), a["n_iters"],
             list(a["residual_history"]), a["wall_seconds"])
            for a in cur["attempts"]]


def replay(rule, s):
    """Epochs this attempt would have spent under the rule, and whether aborted."""
    K, W, th = rule
    _, _, n, r, _ = s
    for k in range(max(K, W), n):
        if r[k] > th * r[k - W]:
            return k, True
    return n, False


def evaluate(rule, ss):
    """(epochs, false kills, seconds saved, attempts aborted) over a unit."""
    epochs = kills = aborted = 0
    saved = 0.0
    for s in ss:
        k, ab = replay(rule, s)
        epochs += k
        if ab:
            aborted += 1
            saved += (s[2] - k) * (s[4] / s[2])     # per-epoch cost of THAT attempt
            if s[1]:
                kills += 1
    return epochs, kills, saved, aborted


def worst_window_ratio(rule, convs):
    """The largest ||R||_k / ||R||_(k-W) any banked CONVERGENCE exhibited in the
    region the rule inspects. theta must stay above this or a convergence dies."""
    K, W, th = rule
    worst = 0.0
    seen = False
    for s in convs:
        _, _, n, r, _ = s
        for k in range(max(K, W), n):
            worst = max(worst, r[k] / r[k - W])
            seen = True
    return worst if seen else None


def margin_factor(rule, convs):
    w = worst_window_ratio(rule, convs)
    return (rule[2] / w) if (w and w > 0.0) else float("inf")


def analyse():
    with open(U3_JSON) as fh:
        u3 = json.load(fh)
    with open(U5_JSON) as fh:
        u5 = json.load(fh)
    s3, s5 = series(u3), series(u5)
    c3 = [s for s in s3 if s[1]]
    c5 = [s for s in s5 if s[1]]
    E3 = sum(s[2] for s in s3)
    E5 = sum(s[2] for s in s5)

    res = {"unit": "R1", "programme": "PROG-R4", "lane": "R",
           "walls_md_name": "R1 -- early abort on flatness",
           "filename_note":
               "WALLS.md calls R1 'early abort on flatness', so the commissioned "
               "filename r1_flatness.py already matches and was NOT renamed.",
           "deliverable_kind": "COMPUTE SAVING (epochs and core-hours), not orbits",
           "criterion_family":
               "abort at epoch k iff k >= K and ||R||_k > theta * ||R||_{k-W}",
           "determinism":
               "LEG 349 COMPLIANT. Three fixed parameters and a comparison of two "
               "banked residuals. No learned or evolved fitness, no scoring of "
               "seeds, no stochastic component; the rule does not touch seed "
               "selection at all, only the stopping time of an already-launched "
               "attempt. Replaying it on the ledger is exactly reproducible."}

    # ------------------------------------------------- the ledger, re-derived
    print("=== R1(0)  THE LEDGER FACTS, re-derived from residual_history ===")
    ledger = {}
    for tag, ss, cs, cur in (("U3", s3, c3, u3), ("U5", s5, c5, u5)):
        it = sorted(s[2] for s in cs)
        ledger[tag] = {
            "attempts": len(ss),
            "convergences": len(cs),
            "epochs_total": sum(s[2] for s in ss),
            "epochs_in_convergences": sum(s[2] for s in cs),
            "epochs_in_non_convergences": sum(s[2] for s in ss if not s[1]),
            "convergence_n_iters_sorted": it,
            "convergence_n_iters_max": it[-1],
            "convergence_n_iters_median":
                it[len(it) // 2] if len(it) % 2
                else 0.5 * (it[len(it) // 2 - 1] + it[len(it) // 2]),
            "attempt_cpu_core_hours": sum(s[4] for s in ss) / 3600.0,
            "mean_seconds_per_epoch": sum(s[4] for s in ss) / sum(s[2] for s in ss),
        }
        print("  %s: %d attempts, %d convergences, %d epochs (%d in convergences), "
              "n_iters max %d median %g, %.2f s/epoch"
              % (tag, ledger[tag]["attempts"], ledger[tag]["convergences"],
                 ledger[tag]["epochs_total"], ledger[tag]["epochs_in_convergences"],
                 ledger[tag]["convergence_n_iters_max"],
                 ledger[tag]["convergence_n_iters_median"],
                 ledger[tag]["mean_seconds_per_epoch"]))
    res["ledger"] = ledger
    check("U3's banked epoch total is 4629, matching U5's resourcing.u3_epochs_spent",
          E3 == 4629 == u5["resourcing"]["u3_epochs_spent"], "re-derived, not cited")
    check("U5's banked epoch total is 2104, matching its own resourcing.epochs_spent",
          E5 == 2104 == u5["resourcing"]["epochs_spent"])
    check("WALLS.md's 'all 14 convergences in <=29 epochs, median 16' is correct",
          ledger["U3"]["convergence_n_iters_max"] == 29
          and ledger["U3"]["convergence_n_iters_median"] == 16,
          "n_iters = %s" % ledger["U3"]["convergence_n_iters_sorted"])

    # WALLS.md's premise for R1, checked rather than taken.
    nc = [s for s in s3 if not s[1]]
    flat = {
        "walls_md_claim":
            "53% reduced ||R|| by <1% over their final 10 epochs, 83% by <10%, "
            "only 3% still halving",
        "n_non_convergences": len(nc),
        "all_ran_to_the_cap": sorted({s[2] for s in nc}),
        "pct_reduced_under_1_pct": 100.0 * sum(1 for s in nc if s[3][-1] / s[3][-11] > 0.99) / len(nc),
        "pct_reduced_under_10_pct": 100.0 * sum(1 for s in nc if s[3][-1] / s[3][-11] > 0.90) / len(nc),
        "pct_still_halving": 100.0 * sum(1 for s in nc if s[3][-1] / s[3][-11] <= 0.5) / len(nc),
        "verdict": "CONFIRMED to the reported precision",
    }
    res["flatness_premise"] = flat
    print("  flatness premise: %.0f%% / %.0f%% / %.0f%% over the final 10 epochs of the %d non-convergences"
          % (flat["pct_reduced_under_1_pct"], flat["pct_reduced_under_10_pct"],
             flat["pct_still_halving"], flat["n_non_convergences"]))
    check("WALLS.md's flatness premise (53% / 83% / 3%) is CONFIRMED",
          round(flat["pct_reduced_under_1_pct"]) == 53
          and round(flat["pct_reduced_under_10_pct"]) == 83
          and round(flat["pct_still_halving"]) == 3,
          "measured on the 86 non-convergences, all of which ran to n_iters = 51")

    # ---------------------------------------------------------- the incumbent
    print("\n=== R1(1)  THE INCUMBENT: U5's already-deployed stall exit ===")
    inc = {"rule": {"K": INCUMBENT[0], "W": INCUMBENT[1], "theta": INCUMBENT[2]},
           "banked_as": u5["resourcing"]["stall_exit"]["rule"],
           "who_deployed_it": "U5, before this unit existed"}
    for tag, ss, tot in (("U3", s3, E3), ("U5", s5, E5)):
        e, k, sv, na = evaluate(INCUMBENT, ss)
        inc[tag] = {"epochs_baseline": tot, "epochs_under_rule": e,
                    "fraction_of_epochs_recovered": 1.0 - e / float(tot),
                    "false_kills": k, "attempts_aborted": na,
                    "core_hours_saved": sv / 3600.0}
        print("  %s: %d -> %d epochs (%.1f%% recovered), %d aborted, %d false kills, %.2f core-hours saved"
              % (tag, tot, e, 100 * (1 - e / float(tot)), na, k, sv / 3600.0))
    inc["margin_factor_pooled"] = margin_factor(INCUMBENT, c3 + c5)
    inc["worst_window_ratio_pooled"] = worst_window_ratio(INCUMBENT, c3 + c5)
    inc["margin_factor_u3_only"] = margin_factor(INCUMBENT, c3)
    print("  margin: theta 0.50 against a worst banked convergence window ratio of "
          "%.6f -> %.3fx" % (inc["worst_window_ratio_pooled"], inc["margin_factor_pooled"]))
    res["incumbent"] = inc
    check("incumbent replayed on U3 gives EXACTLY U5's banked 2083 epochs",
          inc["U3"]["epochs_under_rule"] == u5["resourcing"]["stall_exit"]["u3_epochs_under_rule"] == 2083,
          "independent replay reproduces the banked figure to the epoch")
    check("incumbent's margin factor reproduces U5's banked 6.9016",
          abs(inc["margin_factor_pooled"] - u5["resourcing"]["stall_exit"]["margin_factor"]) < 1e-9,
          "%.6f" % inc["margin_factor_pooled"])
    check("incumbent kills none of the 23 pooled banked convergences",
          inc["U3"]["false_kills"] == 0 and inc["U5"]["false_kills"] == 0,
          "control (1) PASSES for the incumbent")
    check("incumbent recovers 0.0% on U5 because it was already deployed there",
          inc["U5"]["fraction_of_epochs_recovered"] == 0.0,
          "so U5's saving is BANKED, not available again")

    # ------------------------------------------------------------- the sweep
    print("\n=== R1(2)  THE SWEEP: %d rules, both ledgers, controls applied ===" % len(GRID))
    rows = []
    for rule in GRID:
        e3, k3, sv3, _ = evaluate(rule, s3)
        e5, k5, sv5, _ = evaluate(rule, s5)
        if k3 + k5:
            continue
        rows.append({"rule": rule, "e3": e3, "e5": e5, "saved_s": sv3 + sv5,
                     "saved3": sv3, "saved5": sv5,
                     "mf": margin_factor(rule, c3 + c5),
                     "rec": 1.0 - (e3 + e5) / float(E3 + E5),
                     "rec3": 1.0 - e3 / float(E3), "rec5": 1.0 - e5 / float(E5)})
    print("  %d of %d rules kill none of the 23 banked convergences" % (len(rows), len(GRID)))

    def best_at(lo, key="rec3"):
        sub = [r for r in rows if r["mf"] >= lo]
        return max(sub, key=lambda r: r[key]) if sub else None

    frontier = []
    for lo in (0.0, 1.5, 2.0, 3.0, 5.0, inc["margin_factor_pooled"], 8.0, 10.0, 15.0):
        b = best_at(lo)
        if b is None:
            continue
        frontier.append({
            "min_margin_factor": lo,
            "rule": {"K": b["rule"][0], "W": b["rule"][1], "theta": b["rule"][2]},
            "u3_fraction_recovered": b["rec3"], "u5_fraction_recovered": b["rec5"],
            "pooled_fraction_recovered": b["rec"],
            "core_hours_saved_u3": b["saved3"] / 3600.0,
            "core_hours_saved_u5": b["saved5"] / 3600.0,
            "margin_factor": b["mf"]})
        print("  margin >= %6.3fx : best U3 recovery %5.1f%%  K=%2d W=%2d theta=%.2f  "
              "(U5 %.1f%%)  saved %.2f core-h on U3  margin %.2fx"
              % (lo, 100 * b["rec3"], b["rule"][0], b["rule"][1], b["rule"][2],
                 100 * b["rec5"], b["saved3"] / 3600.0, b["mf"]))
    res["sweep"] = {
        "grid": {"K": [2, 40], "W": [2, 20], "theta": THETAS, "n_rules": len(GRID)},
        "n_zero_false_kill": len(rows),
        "frontier_best_u3_recovery_at_min_margin": frontier,
        "scored_on": "the pooled banked residual_history of 200 attempts "
                     "(U3 100 + U5 100), replayed; no attempt re-run",
    }

    unconstrained = max(rows, key=lambda r: r["rec3"])
    res["sweep"]["unconstrained_optimum"] = {
        "rule": {"K": unconstrained["rule"][0], "W": unconstrained["rule"][1],
                 "theta": unconstrained["rule"][2]},
        "u3_fraction_recovered": unconstrained["rec3"],
        "core_hours_saved_u3": unconstrained["saved3"] / 3600.0,
        "margin_factor": unconstrained["mf"],
        "why_rejected":
            "zero false kills but a margin factor of %.2fx: a future convergence "
            "behaving %.0f%% worse than the worst banked one dies under it. "
            "Selecting the maximum of a statistic over 12,597 rules on 23 "
            "convergences is exactly how one overfits a stopping rule. NOT ADOPTED."
            % (unconstrained["mf"], 100 * (unconstrained["mf"] - 1.0)),
    }
    print("  UNCONSTRAINED optimum K=%d W=%d theta=%.2f recovers %.1f%% of U3 but at margin %.2fx -- REJECTED"
          % (unconstrained["rule"][0], unconstrained["rule"][1], unconstrained["rule"][2],
             100 * unconstrained["rec3"], unconstrained["mf"]))

    # ---------------------------------------- the headline: is there headroom?
    at_inc = best_at(inc["margin_factor_pooled"])
    head = {
        "question": "At no loss of safety margin against the deployed rule, how "
                    "much more of U3's compute is recoverable?",
        "incumbent_u3_recovery": inc["U3"]["fraction_of_epochs_recovered"],
        "best_admissible_rule": {"K": at_inc["rule"][0], "W": at_inc["rule"][1],
                                 "theta": at_inc["rule"][2]},
        "best_admissible_u3_recovery": at_inc["rec3"],
        "headroom_percentage_points":
            100.0 * (at_inc["rec3"] - inc["U3"]["fraction_of_epochs_recovered"]),
        "headroom_core_hours_u3":
            (at_inc["saved3"] - inc["U3"]["core_hours_saved"] * 3600.0) / 3600.0,
        "margin_factor": at_inc["mf"],
    }
    res["headroom"] = head
    print("\n=== R1(3)  HEADROOM over the deployed rule, at equal safety ===")
    print("  incumbent recovers %.1f%% of U3's epochs; the best admissible rule "
          "(K=%d W=%d theta=%.2f) recovers %.1f%%."
          % (100 * head["incumbent_u3_recovery"], head["best_admissible_rule"]["K"],
             head["best_admissible_rule"]["W"], head["best_admissible_rule"]["theta"],
             100 * head["best_admissible_u3_recovery"]))
    print("  HEADROOM = %+.1f percentage points = %+.2f core-hours on a 134.45 core-hour run."
          % (head["headroom_percentage_points"], head["headroom_core_hours_u3"]))

    # ------------------------------------------------------ hold-out both ways
    print("\n=== R1(4)  HOLD-OUT BOTH WAYS -- the control WALLS.md did not ask for ===")

    def fit(ss_fit, convs_fit, floor):
        best = None
        for rule in GRID:
            e, k, sv, _ = evaluate(rule, ss_fit)
            if k:
                continue
            if margin_factor(rule, convs_fit) < floor:
                continue
            if best is None or e < best[0]:
                best = (e, rule, sv, margin_factor(rule, convs_fit))
        return best

    floor = inc["margin_factor_pooled"]
    ho = {}
    b = fit(s3, c3, floor)
    e5, k5, sv5, _ = evaluate(b[1], s5)
    ho["fit_on_u3_scored_on_u5"] = {
        "rule": {"K": b[1][0], "W": b[1][1], "theta": b[1][2]},
        "fit_fraction_recovered": 1.0 - b[0] / float(E3),
        "fit_margin_factor": b[3],
        "heldout_fraction_recovered": 1.0 - e5 / float(E5),
        "heldout_false_kills": k5,
        "verdict": "PASSES the false-kill control on unseen data"}
    print("  fit on U3 (margin >= %.2f): K=%d W=%d theta=%.2f, %.1f%% of U3 recovered"
          % (floor, b[1][0], b[1][1], b[1][2], 100 * (1 - b[0] / float(E3))))
    print("    HELD OUT on U5: %.1f%% recovered, %d false kills -> PASSES"
          % (100 * (1 - e5 / float(E5)), k5))
    b = fit(s5, c5, floor)
    e3, k3, sv3, _ = evaluate(b[1], s3)
    ho["fit_on_u5_scored_on_u3"] = {
        "rule": {"K": b[1][0], "W": b[1][1], "theta": b[1][2]},
        "fit_fraction_recovered": 1.0 - b[0] / float(E5),
        "fit_margin_factor": b[3],
        "heldout_fraction_recovered": 1.0 - e3 / float(E3),
        "heldout_false_kills": k3,
        "verdict": "FAILS the false-kill control on unseen data: it aborts an "
                   "attempt U3's ledger shows converged"}
    print("  fit on U5 (margin >= %.2f): K=%d W=%d theta=%.2f, %.1f%% of U5 recovered"
          % (floor, b[1][0], b[1][1], b[1][2], 100 * (1 - b[0] / float(E5))))
    print("    HELD OUT on U3: %.1f%% recovered but %d FALSE KILL(S) -> FAILS"
          % (100 * (1 - e3 / float(E3)), k3))
    ho["reading"] = (
        "The control is asymmetric and that asymmetry is the result. A rule "
        "selected on U3's 14 convergences transfers to U5 with zero false "
        "kills; a rule selected on U5's 9 transfers to U3 and kills one. Nine "
        "convergences are not enough to fix a stopping rule, and the direction "
        "that fails is the one with the smaller fitting set. Any future tuning "
        "of this criterion must be selected on the LARGER ledger and scored on "
        "the smaller, never the reverse.")
    res["holdout"] = ho
    check("hold-out U3 -> U5 passes with zero false kills",
          ho["fit_on_u3_scored_on_u5"]["heldout_false_kills"] == 0)
    check("hold-out U5 -> U3 FAILS with one false kill (reported, not hidden)",
          ho["fit_on_u5_scored_on_u3"]["heldout_false_kills"] == 1,
          "a genuine generalisation failure in the smaller-fitting-set direction")

    # ------------------------------------------------- the saving, and PROJECTION
    print("\n=== R1(5)  THE SAVING (compute) and the PROJECTION (labelled) ===")
    u3_cpu = ledger["U3"]["attempt_cpu_core_hours"]
    saved = inc["U3"]["core_hours_saved"]
    saving = {
        "measured_on": "U3's banked ledger, writeup/data/p2_prog_r4_g1_v1.json, "
                       "100 attempts x residual_history, replayed",
        "rule": inc["banked_as"],
        "epochs_before": E3, "epochs_after": inc["U3"]["epochs_under_rule"],
        "fraction_of_epochs_recovered": inc["U3"]["fraction_of_epochs_recovered"],
        "core_hours_before_attempt_cpu": u3_cpu,
        "core_hours_saved_attempt_cpu": saved,
        "core_hours_after_attempt_cpu": u3_cpu - saved,
        "fraction_of_core_hours_saved": saved / u3_cpu,
        "false_kills": 0,
        "margin_factor": inc["margin_factor_pooled"],
        "whose_saving_it_is":
            "U5's, not R1's. The rule was built and deployed by U5 before this "
            "unit was commissioned. R1's own measurement is the HEADROOM above "
            "it, which is %+.1f percentage points."
            % head["headroom_percentage_points"],
    }
    print("  measured saving of the deployed rule on U3: %.2f of %.2f core-hours (%.1f%%), 0 false kills"
          % (saved, u3_cpu, 100 * saved / u3_cpu))
    print("  R1's OWN marginal saving above the deployed rule, at equal safety: %+.2f core-hours"
          % head["headroom_core_hours_u3"])

    n3 = 8      # R0's re-derived distinct count for U3, under the arbiter's rule
    proj = {
        "LABEL": "PROJECTED",
        "what_it_assumes":
            "that U3 replayed under the rule finds the SAME 8 distinct orbits "
            "in %.2f rather than %.2f core-hours. The zero-false-kill control "
            "supports this for the 14 convergences; it is still a replay, not a run."
            % (u3_cpu - saved, u3_cpu),
        "PROJECTED_distinct_orbits_per_core_hour_attempt_cpu": n3 / (u3_cpu - saved),
        "measured_distinct_orbits_per_core_hour_attempt_cpu": n3 / u3_cpu,
        "PROJECTED_factor": (n3 / (u3_cpu - saved)) / (n3 / u3_cpu),
        "what_it_does_NOT_claim":
            "It does NOT claim the recovered %.2f core-hours would convert into "
            "further orbits at the observed rate. R0 measured that U5 spent "
            "57.04 core-hours to gain ONE orbit new to the programme, so the "
            "conversion assumption is optimistic and is not made here. A "
            "recycled-budget yield is NOT reported." % saved,
    }
    res["saving"] = saving
    res["projection"] = proj
    print("  PROJECTED %.4f distinct orbits per core-hour (attempt-CPU convention), "
          "against the measured %.4f -- PROJECTED, %.2fx"
          % (proj["PROJECTED_distinct_orbits_per_core_hour_attempt_cpu"],
             proj["measured_distinct_orbits_per_core_hour_attempt_cpu"],
             proj["PROJECTED_factor"]))

    res["verdict"] = {
        "gate":
            "YES. R1 is executed to a measured number on the banked data and "
            "its saving is expressed as compute. The criterion recovers %.1f%% "
            "of U3's 4,629 epochs = %.2f of its %.2f attempt-CPU core-hours, "
            "with zero false kills over 23 banked convergences and a %.2fx "
            "safety margin." % (100 * inc["U3"]["fraction_of_epochs_recovered"],
                                saved, u3_cpu, inc["margin_factor_pooled"]),
        "the_correction":
            "That saving is NOT new. U5 built and deployed exactly this rule "
            "before R1 was commissioned, and WALLS.md's 'cheapest competitive "
            "win in the repository' has therefore already been collected. R1's "
            "own contribution is the search that shows there is almost nothing "
            "left in it: over 12,597 deterministic rules, %d of them killing "
            "no banked convergence, the best rule that does not degrade the "
            "deployed safety margin recovers %+.1f percentage points more of "
            "U3's epochs -- %+.2f core-hours on a 134-core-hour run."
            % (len(rows), head["headroom_percentage_points"],
               head["headroom_core_hours_u3"]),
        "what_closes":
            "R1 CLOSES. The apparent 65%%-recovery rules exist but sit at a "
            "%.2fx margin, and the hold-out shows a rule selected on the "
            "smaller ledger already kills a real convergence on the larger. "
            "No further compute should be spent tuning this criterion family."
            % unconstrained["mf"],
        "ceiling":
            "TIER 2. A cheaper solver does not move an L1->L4 link. It makes "
            "the questions affordable, which is a DIFFERENT AND LESSER THING "
            "than progress on the Clay statement. Clay stays ~0.05%.",
    }
    for k, v in res["verdict"].items():
        print("\n  [%s] %s" % (k.upper(), v))
    return res


def main():
    res = analyse()
    bad = [n for n, ok, _ in CHECKS if not ok]
    print("\n%d/%d R1 checks passed" % (len(CHECKS) - len(bad), len(CHECKS)))
    if bad:
        print("FAILED: " + ", ".join(bad))
    if "--write" in sys.argv:
        doc = {}
        if os.path.exists(OUT):
            with open(OUT) as fh:
                doc = json.load(fh)
        doc.setdefault("unit", "R0+R1")
        doc.setdefault("programme", "PROG-R4")
        doc.setdefault("lane", "R")
        doc.setdefault("wall", "W7")
        doc.setdefault("kind", "MEASUREMENT (metric reconciliation + flatness abort)")
        doc.setdefault("clay_movement", "none -- no L1-L4 link moved by this unit")
        doc["r1"] = res
        with open(OUT, "w") as fh:
            json.dump(doc, fh, indent=1, sort_keys=True)
        print("wrote %s" % OUT)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
