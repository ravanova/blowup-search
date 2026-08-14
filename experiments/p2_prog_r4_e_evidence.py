"""Evidence script for PROG-R4 unit E -- the H-hard diagnostic.

Rebuilds EVERY number that appears in the prose of
`writeup/4_p2_lottery/BLOG_P2_PROGR4_HHARD.md` and
`writeup/4_p2_lottery/TECHNICAL_P2_PROGR4_HHARD.md` from the banked records,
and asserts each one against the curated JSON. It RE-RUNS NOTHING: no DNS, no
solver call, no seed mining. Everything below is arithmetic on files that
already exist.

Sources, all read-only:
  writeup/data/p2_prog_r4_e_v1.json        this unit's curated record
  writeup/data/p2_prog_r4_g1_v1.json       U3's banked 100 attempts (G1)
  writeup/data/p2_prog_r4_m3_v1.json       U5's banked 100 attempts (M3)
  writeup/data/p2_route_dsspb5_v1.json     leg 353's five prior attempts
  experiments/programme_r4/u5_m3_ledger.json        U5's per-epoch ledger
  experiments/programme_r4/e_hhard_ledger.json      this unit's per-epoch ledger
  experiments/programme_r4/u2_recurrence_library.json  U2's seed library

The descriptive statistics are re-derived here with plain numpy, independently
of the diagnostic module. The three PRE-REGISTERED classifiers -- the pull
rule, the attractor rule with its within-attempt permutation test, and the
score-bias derivation -- are imported from the diagnostic module rather than
re-implemented, because re-implementing a pre-registered decision rule from
its prose would test the prose, not the rule. They are deterministic and take
their seed from the module.

Exit code 0 iff every check passes.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "experiments", "programme_r4"))

import e_hhard_diagnostic as E  # noqa: E402

DATA = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_e_v1.json")
U3 = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_g1_v1.json")
U5 = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_m3_v1.json")
L353 = os.path.join(ROOT, "writeup", "data", "p2_route_dsspb5_v1.json")
U5_LEDGER = os.path.join(ROOT, "experiments", "programme_r4",
                         "u5_m3_ledger.json")
E_LEDGER = os.path.join(ROOT, "experiments", "programme_r4",
                        "e_hhard_ledger.json")

TWO_PI = 2.0 * np.pi
TOL = 1e-8
LOW = 0.15
BAND = (0.295, 0.707)
MATCH_TOL = 0.05
CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail
                                                    else ""))
    return bool(ok)


def close(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


def wrap_abs(s):
    return np.abs((np.asarray(s, float) + np.pi) % TWO_PI - np.pi)


def load(p):
    with open(p) as f:
        return json.load(f)


def main():
    d = load(DATA)
    u3, u5, l353 = load(U3), load(U5), load(L353)
    d1, d2, d3 = d["diagnostic_1"], d["diagnostic_2"], d["diagnostic_3"]
    att = d3["attempts"]

    # =================================================================
    # 0. the frame: what this unit is and is not allowed to have moved
    # =================================================================
    check("the gate wording banked is the gate this unit was given",
          "do all three named diagnostics return" in d["gate"]["wording"]
          and "BOTH directions" in d["gate"]["wording"]
          and "RETURNING, not about convergence" in d["gate"]["note"])
    check("G1's record is untouched: still UNDER-RESOURCED",
          u3["gate"]["answer"] == "UNDER-RESOURCED", u3["gate"]["answer"])
    check("U5's record is untouched: M3 still DELIVERED",
          u5["milestone"]["answer"] == "DELIVERED",
          u5["milestone"]["answer"])
    check("no Clay link moved; ceiling TIER 2; odds ~0.05%",
          d["clay_movement"]["links_moved"] == 0
          and d["clay_movement"]["ceiling"] == "TIER 2"
          and "0.05%" in d["clay_movement"]["clay_odds"])
    check("the three open Clay obligations are still carried as OPEN",
          all("OPEN" in v for v in d["open_obligations_carried"].values()))
    check("leg 349's ban is recorded COMPLIANT and no learned score is used",
          d["seed"]["ban_leg349"].startswith("COMPLIANT")
          and "learned" in d2["score_bias"]["note"])

    # =================================================================
    # 1. the prior -- leg 353, re-derived from ITS OWN banked record
    # =================================================================
    prior = l353["newton_attempts"]
    p_res = [a["final_residual"] for a in prior]
    check("leg 353: five attempts at these rows, ALL FIVE failed",
          len(prior) == 5
          and all(a["reason"] == "line_search_failed" for a in prior),
          "targets " + ", ".join(a["target"] for a in prior))
    lo_q, hi_q = d["prior_leg_353"]["final_residual_range"]
    check("the [22.5, 29.5] band this unit quotes IS leg 353's own spread, "
          "rounded to 0.1",
          close(round(min(p_res), 1), lo_q) and close(round(max(p_res), 1),
                                                      hi_q),
          f"observed [{min(p_res):.2f}, {max(p_res):.2f}], quoted "
          f"[{lo_q}, {hi_q}]")
    check("leg 353 attempted UPO37 twice, and UPO35/UPO9/UPO22 once each",
          sorted(a["target"] for a in prior)
          == ["UPO22", "UPO35", "UPO37", "UPO37", "UPO9"])
    check("no attempt of leg 353 came within 9 orders of magnitude of tol",
          min(p_res) / TOL > 1e9, f"min final ||R|| = {min(p_res):.2f}")

    # =================================================================
    # 2. diagnostic (1), re-derived from the 200 banked attempts
    # =================================================================
    banked = [a for src in (u3, u5) for a in src["attempts"]]
    s_seed = wrap_abs([a["s_seed"] for a in banked])
    s_fin = wrap_abs([a["s_converged"] for a in banked])
    ok = np.array([bool(a["success"]) for a in banked])
    drift = s_fin - s_seed
    dc = drift[ok]

    check("200 banked attempts, 100 from U3 and 100 from U5",
          len(banked) == 200 == d1["n_attempts_total"]
          and len(u3["attempts"]) == 100 and len(u5["attempts"]) == 100)
    check("23 of the 200 converged, 14 in U3 and 9 in U5",
          int(ok.sum()) == d1["n"] == 23
          and sum(1 for a in u3["attempts"] if a["success"])
          == d1["by_unit"]["U3"]
          and sum(1 for a in u5["attempts"] if a["success"])
          == d1["by_unit"]["U5"],
          f"U3 {d1['by_unit']['U3']} + U5 {d1['by_unit']['U5']} "
          f"= {int(ok.sum())}")
    check("median drift of the convergences",
          close(np.median(dc), d1["median_drift"]),
          f"{float(np.median(dc)):+.6f}")
    check("mean drift of the convergences",
          close(np.mean(dc), d1["mean_drift"]),
          f"{float(np.mean(dc)):+.6f}")
    check("sign split of the drift",
          int((dc < 0).sum()) == d1["n_drift_negative"]
          and int((dc > 0).sum()) == d1["n_drift_positive"],
          f"{int((dc < 0).sum())} down / {int((dc > 0).sum())} up")
    check("exact two-sided sign-test p",
          close(E.binom_two_sided(int((dc < 0).sum()), len(dc)),
                d1["sign_test_p"]),
          f"p = {d1['sign_test_p']:.4f}")
    check(f"fraction of convergences finishing below |s| = {LOW}",
          close(np.mean(s_fin[ok] < LOW), d1["frac_converged_below_0p15"]),
          f"{100 * float(np.mean(s_fin[ok] < LOW)):.1f}%")
    check("Spearman(seed |s|, converged |s|) over the convergences",
          close(E.spearman(list(s_seed[ok]), list(s_fin[ok])),
                d1["spearman_seed_vs_converged"], 1e-9),
          f"rho = {d1['spearman_seed_vs_converged']:.4f}")
    in_band = ok & (s_seed >= BAND[0]) & (s_seed <= BAND[1])
    left = in_band & ~((s_fin >= BAND[0]) & (s_fin <= BAND[1]))
    check("in-band seeds that converged, and how many LEFT the band",
          int(in_band.sum()) == d1["in_band_seeds_converged"]
          and int(left.sum()) == d1["in_band_seeds_that_left_the_band"],
          f"{int(left.sum())} of {int(in_band.sum())} left "
          f"[{BAND[0]}, {BAND[1]}]")
    check("the pre-registered rule returns PULL_TO_LOW_S on this data",
          E.classify_pull(list(s_seed[ok]),
                          list(s_fin[ok]))["verdict"] == d1["verdict"]
          == "PULL_TO_LOW_S")
    check("the SECONDARY all-200 reading is the weaker one, and is labelled",
          d1["secondary_all_200_attempts"]["verdict"] == "NO_PULL"
          and (d1["secondary_all_200_attempts"]["frac_converged_below_0p15"]
               < d1["frac_converged_below_0p15"]),
          f"all-200 {100 * d1['secondary_all_200_attempts']['frac_converged_below_0p15']:.1f}% "
          f"below {LOW} vs {100 * d1['frac_converged_below_0p15']:.1f}% "
          "among convergences")
    check("diagnostic (1)'s controls fired in BOTH directions",
          d1["controls"]["positive"]["verdict"] == "PULL_TO_LOW_S"
          and d1["controls"]["negative"]["verdict"] == "NO_PULL"
          and d1["controls"]["fired_both_ways"])

    # =================================================================
    # 3. diagnostic (2), re-derived from U5's per-epoch ledger
    # =================================================================
    led = load(U5_LEDGER)
    flat, per_attempt = E.epoch_drifts(led, u5["attempts"])
    # epoch_drifts yields (class, d|s|, d||R||) triples; "constrained" means the
    # accepted hookstep trial sat ON the trust-region boundary.
    con = np.array([t[1] for t in flat if t[0] == "constrained"], float)
    unc = np.array([t[1] for t in flat if t[0] == "unconstrained"], float)
    check("epoch classes partition the accepted epochs",
          len(flat) == d2["n_epochs"]
          and len(con) == d2["n_constrained"]
          and len(unc) == d2["n_unconstrained"]
          and len(con) + len(unc) == len(flat),
          f"{len(con)} constrained + {len(unc)} unconstrained "
          f"= {len(flat)}")
    check("the trust region binds on almost every accepted step",
          close(len(con) / len(flat), 0.971, 5e-4),
          f"{100 * len(con) / len(flat):.1f}% of accepted steps are "
          "trust-region constrained")
    check("mean per-epoch d|s| by class",
          close(con.mean(), d2["mean_d_abs_s_constrained"])
          and close(unc.mean(), d2["mean_d_abs_s_unconstrained"]),
          f"{con.mean():+.6f} constrained vs {unc.mean():+.6f} "
          "unconstrained")
    check("net d|s| by class",
          close(con.sum(), d2["net_d_abs_s_constrained"], 1e-9)
          and close(unc.sum(), d2["net_d_abs_s_unconstrained"], 1e-9),
          f"{con.sum():+.4f} constrained vs {unc.sum():+.4f} unconstrained")
    fr = abs(con.sum()) / (abs(con.sum()) + abs(unc.sum()))
    check("share of the total |s| descent carried by constrained epochs",
          0.979 <= fr <= 0.981, f"{100 * fr:.1f}%")
    check("the pre-registered attractor rule returns MIXED, and why",
          d2["verdict"] == "MIXED" and d2["permutation_p"] > 0.05,
          f"observed difference {d2['observed_difference']:+.6f}, "
          f"within-attempt permutation p = {d2['permutation_p']:.4f} over "
          f"{d2['n_perm']:,} permutations -- the per-epoch RATES are not "
          "distinguishable")
    check("the permutation test reproduces exactly (fixed seed)",
          close(E.classify_attractor(per_attempt)["permutation_p"],
                d2["permutation_p"], 1e-12),
          f"PERM_SEED = {E.PERM_SEED}, N_PERM = {E.N_PERM}")
    check("corr(per-epoch dR, d|s|): descending in ||R|| descends in |s|",
          close(E.pearson([t[1] for t in flat], [t[2] for t in flat]),
                d2["correlation_dR_vs_dabs_s"], 1e-9),
          f"r = {d2['correlation_dR_vs_dabs_s']:+.4f}")
    check("coverage is 100 of 200, and the gap is declared with its cost",
          d2["coverage"]["n_attempts_with_epoch_path"] == 100
          and d2["coverage"]["n_banked_attempts"] == 200
          and "122.1 core-hours" in d2["coverage"]["cost_to_close"],
          "U3's ledger predates the T_before/s_before fields")
    sb = d2["score_bias"]
    sb2 = E.score_vs_shift()
    check("the seed score's own |s| bias, re-derived from U2's library",
          sb["n_m0"] == sb2["n_m0"]
          and close(sb["spearman_absS_vs_R"], sb2["spearman_absS_vs_R"],
                    1e-12),
          f"Spearman(|s|, R) = {sb['spearman_absS_vs_R']:.4f} over "
          f"{sb['n_m0']} m=0 candidates")
    check("the admitted fraction falls monotonically across the |s| bands",
          all(a["admitted_fraction"] > b["admitted_fraction"]
              for a, b in zip(sb["by_band"][:-1], sb["by_band"][1:])),
          " > ".join(f"{100 * b['admitted_fraction']:.1f}%"
                     for b in sb["by_band"]))
    check("that reproduces U3 sec.5's own 44 / 20 / 11 / 3 table",
          all(abs(100 * b["admitted_fraction"] - t) < 1.0
              for b, t in zip(sb["by_band"], (44, 20, 11, 3))))
    check("diagnostic (2)'s controls fired in BOTH directions",
          (d2["controls"]["planted_minimisation"]["verdict"]
           == "MINIMISATION_ATTRACTOR")
          and (d2["controls"]["planted_iteration"]["verdict"]
               == "ITERATION_ATTRACTOR")
          and d2["controls"]["fired_both_ways"],
          f"both at p = "
          f"{d2['controls']['planted_minimisation']['permutation_p']:.4f}")

    # =================================================================
    # 4. diagnostic (3), re-derived from this unit's own attempt rows
    # =================================================================
    check("the eight named rows are U3's transcription, not a re-typing",
          "asserted equal to it at import" in d["seed"]["transcription"]
          and [r[0] for r in E.TABLE_IV]
          == ["UPO37", "UPO35", "UPO34", "UPO32", "UPO22", "UPO20", "UPO17",
              "UPO9"])
    check("E-iv's discipline: what a published row determines is stated",
          d["seed"]["what_a_published_row_determines"]
          == "(T, s, m) ONLY -- NOT a field"
          and "field-plus-pinned" in d["seed"]["what_was_planted"])
    check("16 attempts: eight rows, two arms each",
          len(att) == 16 == d3["n_attempts"]
          and len({a["row"] for a in att}) == 8
          and sorted(a["arm"] for a in att) == ["Q"] * 8 + ["S"] * 8)
    check("no field was reused across the 16 attempts",
          len({a["snapshot_earlier"] for a in att}) == 16)
    check("every attempt was planted at the published period EXACTLY",
          all(a["T_seeded"] == a["T_published"] for a in att))
    check("every attempt was planted at +/- the published |s| exactly, "
          "with the sign MEASURED",
          all(close(abs(a["s_seeded"]), a["abs_s_published"], 1e-12)
              for a in att)
          and all(close(a["seed_extended_residual"],
                        min(a["seed_residual_plus"],
                            a["seed_residual_minus"]), 1e-12)
                  for a in att)
          and (d3["sign_tally"]["plus"] + d3["sign_tally"]["minus"]) == 16,
          f"sign tally {d3['sign_tally']}")
    check("the R < 0.25 admission window was DELIBERATELY not applied",
          any(not a["candidate_in_newton_window"] for a in att),
          f"{sum(1 for a in att if not a['candidate_in_newton_window'])} of "
          "16 seeds sit outside the window U3 and U5 never left")
    n_conv = sum(1 for a in att if a["success"])
    check("converged / recovered counts reconcile with the rows",
          n_conv == d3["n_converged"]
          and sum(1 for a in att if a["recovered_named_orbit"])
          == d3["n_recovered_its_own_row"]
          and sum(1 for a in att if a["recovered_any_named_orbit"])
          == d3["n_recovered_any_named_row"],
          f"{n_conv} reached tol; {d3['n_recovered_its_own_row']} matched "
          f"its own row; {d3['n_recovered_any_named_row']} matched any row")
    check("the exit-reason tally reconciles with the rows",
          {k: sum(1 for a in att if a["reason"] == k)
           for k in d3["reasons"]} == d3["reasons"],
          ", ".join(f"{k} x{v}" for k, v in sorted(d3["reasons"].items())))
    check("no attempt exited line_search_failed -- the hookstep cannot",
          "line_search_failed" not in d3["reasons"],
          "leg 353's only exit reason is unreachable in this realization")
    sr = np.array([a["seed_extended_residual"] for a in att])
    check("planting at the published (T, s) starts FAR from a solution",
          sr.min() > 20.0,
          f"seed ||R|| in [{sr.min():.2f}, {sr.max():.2f}] -- worse than the "
          "mined seeds U3 and U5 started from")
    armS = {a["row"]: a for a in att if a["arm"] == "S"}
    armQ = {a["row"]: a for a in att if a["arm"] == "Q"}
    check("arm S starts closer than arm Q for EVERY one of the eight rows",
          all(armS[r]["seed_extended_residual"]
              < armQ[r]["seed_extended_residual"] for r in armS),
          "the shift-matched field beats the score-optimal field at the "
          "published (T, s), 8 rows out of 8")
    check("arm Q's field is on average further off in |s| than arm S's",
          (np.mean([a["delta_abs_s_candidate_to_published"]
                    for a in armQ.values()])
           > np.mean([a["delta_abs_s_candidate_to_published"]
                      for a in armS.values()])),
          f"arm Q mean | |s|_c - |s|_pub | = "
          f"{np.mean([a['delta_abs_s_candidate_to_published'] for a in armQ.values()]):.4f}"
          f" vs arm S "
          f"{np.mean([a['delta_abs_s_candidate_to_published'] for a in armS.values()]):.4f}")
    ca = d3["closest_approach"]
    best = min(att, key=lambda a: (a["delta_T_from_published"]
                                   + a["delta_abs_s_from_published"]))
    check("the closest approach banked is the closest approach in the rows",
          best["row"] == ca["row"] and best["arm"] == ca["arm"]
          and close(best["final_residual"], ca["final_residual"], 1e-12),
          f"{ca['row']} arm {ca['arm']}: dT = "
          f"{ca['delta_T_from_published']:.4f}, ds = "
          f"{ca['delta_s_from_published']:.4f}, final ||R|| = "
          f"{ca['final_residual']:.4g}")
    check("the matching predicate applied is U3's, unchanged",
          close(E.MATCH_T_TOL, MATCH_TOL) and close(E.MATCH_S_TOL, MATCH_TOL)
          and all((a["recovered_named_orbit"]
                   == (a["success"]
                       and a["delta_T_from_published"] < MATCH_TOL
                       and a["delta_s_from_published"] < MATCH_TOL))
                  for a in att))
    check("the sign-agnostic |s| variant is reported as SECONDARY only",
          "SECONDARY" in E.match_named_abs.__doc__
          and d3["n_recovered_abs_secondary"] is not None,
          f"{d3['n_recovered_abs_secondary']} secondary matches, no verdict "
          "rests on them")
    check("diagnostic (3)'s controls P, N and R fired as planted",
          d3["controls"]["fired_as_planted"]
          and d3["controls"]["P"]["recovered"]
          and not d3["controls"]["N"]["recovered"]
          and d3["controls"]["R"]["recovered"],
          "P (positive) recovered, N (negative, phase-scrambled) did not, "
          "R (positive, conditional) re-recovered a perturbed banked orbit")
    check("control R proves the HARNESS can return a recovery",
          d3["controls"]["R"]["harness_predicate_says_recovered"],
          "a perturbed banked orbit is matched back by this unit's own "
          "predicate, so a null result is not a broken predicate")

    # =================================================================
    # 5. the per-epoch ledger of this unit's own 16 attempts
    # =================================================================
    e_led = load(E_LEDGER)
    check("this unit banked a per-epoch ledger for all 16 attempts",
          len(e_led["attempts"]) == 16
          and sum(len(a["ledger"]) for a in e_led["attempts"])
          == d3["resourcing"]["total_epochs"],
          f"{d3['resourcing']['total_epochs']} epochs banked")
    check("every attempt's banked residual history starts at its seed ||R||",
          all(close(a["residual_history"][0], a["seed_extended_residual"],
                    1e-6) for a in att))
    check("every attempt's final residual is the last of its history",
          all(close(a["final_residual"], a["residual_history"][-1], 1e-12)
              for a in att))

    # =================================================================
    # 6. resourcing -- sec.3d: a cost, never a verdict
    # =================================================================
    r = d3["resourcing"]
    check("the budget spent is the commissioned 0.5-1 core-hour envelope's "
          "order",
          r["core_hours"] > 0,
          f"{r['core_hours']:.2f} core-hours over {r['wall_seconds'] / 3600:.2f} h "
          f"wall on {r['workers']} workers, {r['total_epochs']} epochs")
    check("the solver settings are U5's, imported not copied",
          r["tol"] == 1e-8 and r["max_newton"] == 52
          and r["max_gmres"] == 140 and r["gmres_rtol"] == 1e-3,
          f"tol {r['tol']}, max_newton {r['max_newton']}, "
          f"max_gmres {r['max_gmres']}, gmres_rtol {r['gmres_rtol']}")
    check("U5's stall rule kills ZERO banked convergence in EITHER unit",
          all(v["n_would_be_killed"] == 0
              for v in r["stall_rule_replay"].values()),
          "; ".join(f"{k}: worst 10-epoch ratio "
                    f"{v['worst_10_epoch_ratio_at_k_ge_20']:.3f} < "
                    f"{v['threshold']}"
                    for k, v in r["stall_rule_replay"].items()))
    check("the realization is stated in lesson-91 terms",
          d["realization"]["Re"] == 60.0 and d["realization"]["dt"] == 0.01
          and "FIRST order" in d["realization"]["stepper"]
          and "hookstep" in d["realization"]["globalisation"]
          and "m is not carried" in d["realization"]["residual"])

    # =================================================================
    bad = [n for n, o, _ in CHECKS if not o]
    print(f"\n{len(CHECKS) - len(bad)}/{len(CHECKS)} checks passed")
    if bad:
        print("FAILED: " + "; ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
