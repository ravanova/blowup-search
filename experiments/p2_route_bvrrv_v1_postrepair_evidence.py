"""Route-BVRRV v1 (leg 233) -- EVIDENCE: every number the BLOG and TECHNICAL write-ups
quote, re-derived from `writeup/data/p2_route_bvrrv_v1_postrepair.json`. Also builds
`writeup/figures/fig101_route_bvrrv_v1.png`.

Nothing is re-run here. The sweeps behind the curated JSON cost ~1.9 h wall four-way
parallel (`experiments/p2_route_bvrrv_v1_postrepair.py` is the one script that runs them);
this script only reads the banked artifact and asserts the relations the prose asserts.

    .venv/bin/python experiments/p2_route_bvrrv_v1_postrepair_evidence.py
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "writeup", "data")
FIG = os.path.join(ROOT, "writeup", "figures", "fig101_route_bvrrv_v1.png")

VERDICTS = ["OK", "SILENT_WRONG", "RAISED", "NONFINITE", "NO_REFERENT", "RETURNED"]

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-70s %s" % ("ok" if ok else "FAIL", name, detail))


# --------------------------------------------------------------------------- checks
def checks_clause_a(j):
    a = j["clause_a"]
    committed = a["tally_committed_leg_205"]
    pre = a["tally_remeasured_pre_repair"]
    post = a["tally_post_repair"]

    check("(a1) battery size is 81 cases in all three columns",
          a["n_cases_before"] == a["n_cases_after"] == a["n_cases_committed"] == 81,
          f"{a['n_cases_before']}/{a['n_cases_after']}/{a['n_cases_committed']}")
    check("(a2) re-measured pre-repair column reproduces leg 205's committed tally",
          all(pre[v] == committed[v] for v in VERDICTS),
          " ".join(f"{v}={pre[v]}" for v in VERDICTS))
    check("(a3) agreement is case-by-case, not merely tally-for-tally: 0 of 81 mismatched",
          a["n_verdict_mismatch_vs_committed"] == 0 and a["verdict_mismatch_detail"] == [],
          f"n_verdict_mismatch_vs_committed={a['n_verdict_mismatch_vs_committed']}")
    check("(a4) SILENT_WRONG 18 -> 0",
          a["silent_wrong_before"] == 18 and a["silent_wrong_after"] == 0
          and committed["SILENT_WRONG"] == 18 and "SILENT_WRONG" not in post,
          f"{a['silent_wrong_before']} -> {a['silent_wrong_after']}, "
          f"cases left = {len(a['silent_wrong_after_cases'])}")

    t = a["transitions"]
    check("(a5) the 18 SILENT_WRONGs split 13 -> OK and 5 -> RAISED",
          t["SILENT_WRONG -> OK"] == 13 and t["SILENT_WRONG -> RAISED"] == 5,
          f"13/5 sums to {t['SILENT_WRONG -> OK'] + t['SILENT_WRONG -> RAISED']}")
    fate_ok = sum(1 for f in a["silent_wrong_fate"] if f["after"] == "OK")
    fate_raised = sum(1 for f in a["silent_wrong_fate"] if f["after"] == "RAISED")
    check("(a6) the per-case fate list agrees with the transition matrix",
          len(a["silent_wrong_fate"]) == 18 and fate_ok == 13 and fate_raised == 5,
          f"{len(a['silent_wrong_fate'])} cases: {fate_ok} OK / {fate_raised} RAISED")
    fate = a["silent_wrong_fate"]
    # the five F2 modulation cases carry a rel err but no scalar return value
    scalar_ok = [f for f in fate
                 if f["after"] == "OK" and f["before_returned"] is not None]
    worst = min(scalar_ok, key=lambda f: f["before_returned"])
    gentlest = max(scalar_ok, key=lambda f: f["before_returned"])
    check("(a6b) worst SILENT_WRONG recovered: 0.26930226 -> 2.00077595",
          abs(worst["before_returned"] - 0.26930226316474387) < 1e-12
          and abs(worst["after_returned"] - 2.0007759522991355) < 1e-12,
          f"{worst['before_returned']} -> {worst['after_returned']}")
    check("(a6c) gentlest SILENT_WRONG recovered: 1.99784673 -> 2.00076840 "
          "(rel err 1.077e-03 -> 3.842e-04)",
          abs(gentlest["before_returned"] - 1.9978467261707167) < 1e-12
          and abs(gentlest["after_returned"] - 2.000768398060092) < 1e-12
          and abs(gentlest["before_rel_err"] - 0.00107663691464166) < 1e-15,
          f"{gentlest['before_returned']} -> {gentlest['after_returned']}")
    raised = [f for f in fate if f["after"] == "RAISED"]
    check("(a6d) of the 5 SILENT_WRONG -> RAISED, 4 returned exactly 0.0 and one returned "
          "1.90612834",
          sum(1 for f in raised if f["before_returned"] == 0.0) == 4
          and [f["before_returned"] for f in raised if f["before_returned"] != 0.0]
          == [1.9061283431326006],
          f"{sum(1 for f in raised if f['before_returned'] == 0.0)} exact zeros")
    check("(a7) transition matrix conserves the battery (rows sum to 81)",
          sum(t.values()) == 81, f"sum={sum(t.values())}")
    check("(a8) every non-SILENT_WRONG class is preserved on the diagonal",
          t["RAISED -> RAISED"] == 11 and t["NONFINITE -> NONFINITE"] == 9
          and t["RETURNED -> RETURNED"] == 9 and t["NO_REFERENT -> NO_REFERENT"] == 2,
          "11 / 9 / 9 / 2")

    adj = a["ok_to_nonok_adjudication"]
    check("(a9) exactly 3 OK -> RAISED transitions, all adjudicated",
          t["OK -> RAISED"] == 3 and len(adj) == 3 and a["n_ok_left_ok"] == 3,
          f"OK->RAISED={t['OK -> RAISED']}, adjudicated={len(adj)}")
    check("(a10) verdict on all three: 3 JUSTIFIED_REFUSAL, 0 UNJUSTIFIED_REGRESSION",
          a["n_justified_refusals"] == 3 and a["n_ok_regressions"] == 0
          and a["ok_regressions"] == []
          and all(c["verdict"] == "JUSTIFIED_REFUSAL" for c in adj)
          and all(c["precondition_genuinely_fails"] for c in adj),
          f"{a['n_justified_refusals']} justified / {a['n_ok_regressions']} regressions")

    rank_def = [c for c in adj if c["failure_mode"].startswith("rank_deficient")]
    under = [c for c in adj if c["failure_mode"].startswith("under_determined")]
    check("(a11) two of the three are rank-2-of-3 design matrices with 21 and 32 window nodes",
          len(rank_def) == 2
          and sorted(c["measured_window_nodes"] for c in rank_def) == [21, 32]
          and all(c["measured_lstsq_rank"] == 2 and c["design_matrix_columns"] == 3
                  for c in rank_def),
          " ".join(f"{c['measured_window_nodes']} nodes rank "
                   f"{c['measured_lstsq_rank']}/{c['design_matrix_columns']}"
                   for c in rank_def))
    tol = adj[0]["module_acceptance_tol"]
    worst_frac = max(c["pre_margin_inside_tol"] / tol for c in rank_def)
    check("(a12) those two scored OK by 2.79e-07, i.e. 0.056% of the 5e-4 tolerance",
          all(abs(c["pre_margin_inside_tol"] - 2.79e-07) < 5e-10 for c in rank_def)
          and abs(worst_frac * 100 - 0.056) < 0.001,
          f"margin={rank_def[0]['pre_margin_inside_tol']:.6e} = "
          f"{worst_frac * 100:.3f}% of tol {tol}")
    check("(a13) their singular-value ratios are 4.13e-16 and 3.87e-15 (numerically singular)",
          sorted(round(np.log10(c["singular_value_ratio"]), 1) for c in rank_def)
          == [-15.4, -14.4],
          " ".join(f"{c['singular_value_ratio']:.3e}" for c in rank_def))
    check("(a13b) the rank-deficient pairs' singular values are [9.009e-04, 1.943e-11, "
          "3.716e-19] and [1.575e-03, 1.039e-10, 6.091e-18]",
          [len(c["singular_values"]) for c in rank_def] == [3, 3]
          and abs(rank_def[0]["singular_values"][2] - 3.716378204935402e-19) < 1e-31
          and abs(rank_def[1]["singular_values"][2] - 6.091104963656173e-18) < 1e-30,
          " | ".join(", ".join(f"{v:.3e}" for v in c["singular_values"])
                     for c in rank_def))
    check("(a14) the third is 2 window nodes against 3 parameters, min_points floor 3",
          len(under) == 1 and under[0]["measured_window_nodes"] == 2
          and under[0]["min_points_required"] == 3
          and under[0]["design_matrix_columns"] == 3,
          f"{under[0]['measured_window_nodes']} nodes / "
          f"{under[0]['design_matrix_columns']} params")
    check("(a14b) the under-determined case scored OK by 2.887e-04, 57.7% of the tolerance",
          abs(under[0]["pre_margin_inside_tol"] - 0.00028868454393665656) < 1e-15
          and abs(100 * under[0]["pre_margin_inside_tol"] / tol - 57.737) < 0.001,
          f"{under[0]['pre_margin_inside_tol']:.4e} = "
          f"{100 * under[0]['pre_margin_inside_tol'] / tol:.3f}% of tol")
    check("(a15) clause (a) passes",
          a["clause_a_pass"] is True and j["gate_answer"] == "yes",
          f"clause_a_pass={a['clause_a_pass']}, gate_answer={j['gate_answer']!r}")


def checks_lesson_90(j):
    m = j["lesson_90_control"]["magnitudes"]
    c = j["lesson_90_control"]["checks"]
    check("(L1) the two module objects are distinct and their signatures differ as the repair requires",
          c["distinct_function_objects"] and c["signatures_differ_as_the_repair_requires"]
          and sorted(m["signature_params_added"]) == ["max_rel_residual", "min_points"],
          f"added {m['signature_params_added']}")
    check("(L2) DEFECT B: pre-repair 0.26930226 (rel err 8.653e-01) against truth 2.0",
          abs(m["defect_B_pre"] - 0.26930226316474387) < 1e-12
          and abs(m["defect_B_pre_rel_err"] - 0.865348868417628) < 1e-12
          and m["defect_B_truth"] == 2.0,
          f"{m['defect_B_pre']} rel err {m['defect_B_pre_rel_err']:.4e}")
    check("(L3) DEFECT B: post-repair 2.00077595 (rel err 3.880e-04), inside the 5e-4 module tolerance",
          abs(m["defect_B_post"] - 2.0007759522991355) < 1e-12
          and m["defect_B_post_rel_err"] < m["module_acceptance_tol"],
          f"{m['defect_B_post']} rel err {m['defect_B_post_rel_err']:.4e} "
          f"< tol {m['module_acceptance_tol']}")
    check("(L4) DEFECT A: pre-repair returns exactly 0.0; post-repair raises ValueError",
          m["defect_A_pre"] == 0.0 and str(m["defect_A_post"]).startswith("ValueError")
          and c["pre_fabricates_exactly_zero_on_defect_A"] and c["post_rejects_on_defect_A"],
          f"pre={m['defect_A_pre']!r}, post={str(m['defect_A_post'])[:38]}...")
    check("(L5) the differential is not a module against itself: all 6 control checks pass",
          j["lesson_90_control"]["all_passed"] and all(c.values()),
          f"{sum(1 for v in c.values() if v)}/{len(c)}")


def checks_clause_b(j):
    b = j["clause_b"]
    tot = b["totals"]
    runs = b["runs"]
    suites = b["test_suite_runs"]

    check("(b1) 340,233 calls compared live, 340,233 bit-identical, 0 moved",
          tot["total_calls_compared_live"] == 340233
          and tot["total_calls_moved_live"] == 0
          and tot["calls_bit_identical_live"] == tot["calls_compared_live"] == 335092
          and tot["test_suite_calls_compared_live"] == 5141,
          f"{tot['calls_compared_live']} artifact + "
          f"{tot['test_suite_calls_compared_live']} suite = "
          f"{tot['total_calls_compared_live']}, moved {tot['total_calls_moved_live']}")
    check("(b2) the totals are the sum of the per-unit counts, not a separately reported number",
          sum(r["calls_compared"] for r in runs) == tot["calls_compared_live"]
          and sum(s["calls_compared"] for s in suites)
          == tot["test_suite_calls_compared_live"],
          f"{sum(r['calls_compared'] for r in runs)} + "
          f"{sum(s['calls_compared'] for s in suites)}")
    check("(b3) 6 of 6 banked artifacts ran live, 0 from cache, none skipped",
          tot["artifacts_run_live"] == tot["artifacts_in_registry"] == 6
          and tot["artifacts_not_run_live"] == 0 and b["not_run_live"] == []
          and all(r["ran_live"] and not r["from_cache"] for r in runs)
          and all(s["ran_live"] and not s["from_cache"] for s in suites),
          f"{tot['artifacts_run_live']}/{tot['artifacts_in_registry']} live, "
          f"{sum(1 for r in runs if r['from_cache'])} from cache")
    check("(b4) all six artifacts restored clean, no non-zero return codes, 3/3 suites passed",
          tot["all_artifacts_restored_clean"] and not tot["any_nonzero_returncode"]
          and tot["test_suites_all_passed"] and tot["test_suites_shimmed"] == 3
          and all(r["artifact_restored_clean"] for r in runs),
          f"suites shimmed {tot['test_suites_shimmed']}")

    check("(b5) per-unit artifact counts are 2 / 62 / 52,516 / 42,488 / 140,016 / 100,008",
          [r["calls_compared"] for r in runs] == [2, 62, 52516, 42488, 140016, 100008],
          str([r["calls_compared"] for r in runs]))
    check("(b6) per-unit suite counts are 4,999 / 0 / 142",
          [s["calls_compared"] for s in suites] == [4999, 0, 142],
          str([s["calls_compared"] for s in suites]))
    stepc = [r for r in runs if r["key"] == "spike1_stepC_gate"][0]
    check("(b7) the one divergence from leg 221 is spike1_stepC_gate at --steps 2500, +84,000 calls",
          tot["excess_over_leg_221_and_why"]["excess"] == 84000
          and stepc["argv"] == ["--logged", "--steps", "2500"]
          and stepc["calls_compared"] - 16008 == 84000
          and tot["total_calls_compared_live"]
          - tot["leg_221_headline_for_comparison"] == 84000,
          f"{stepc['calls_compared']} vs leg 221's 16008; total excess over "
          f"{tot['leg_221_headline_for_comparison']} is "
          f"{tot['excess_over_leg_221_and_why']['excess']}")
    check("(b8) leg 221's 256,233 headline reconciles as 251,092 banked + 5,141 suite",
          tot["leg_221_headline_for_comparison"] == 256233
          and 251092 + 5141 == 256233
          and tot["calls_compared_live"] - stepc["calls_compared"] + 16008 == 251092,
          "251092 + 5141 = 256233")

    check("(b9) the zero is EXPLAINED: cap_binds = 0 over all 340,233 calls",
          tot["cap_binds_live"] == 0
          and all(r["cap_binds"] == 0 for r in runs)
          and all(s["cap_binds"] == 0 for s in suites)
          and tot["cap_nonbinding_live"] == tot["calls_compared_live"],
          f"cap_binds={tot['cap_binds_live']}, "
          f"cap_nonbinding={tot['cap_nonbinding_live']}")
    occ = [r["per_call_differential"]["min_window_nodes"] for r in runs] + \
          [s["per_call_differential"]["min_window_nodes"] for s in suites
           if s["per_call_differential"]["min_window_nodes"] is not None]
    check("(b10) minimum window occupancy anywhere in the corpus is 4 nodes, floor is 3",
          min(occ) == 4
          and all(r["per_call_differential"]["n_window_below_3"] == 0 for r in runs),
          f"min={min(occ)} over {len(occ)} measured units, per-unit {sorted(occ)}")
    check("(b11) no post-repair call raised: raise_post = 0 across the corpus",
          tot["raise_post_live"] == 0
          and all(r["per_call_differential"]["raise_post"] == 0 for r in runs),
          f"raise_post={tot['raise_post_live']}")
    check("(b12) clause (b) passes over the live scope",
          b["clause_b_pass_over_live_scope"] is True
          and all(not r["contamination_by_calls"] for r in runs),
          f"clause_b_pass_over_live_scope={b['clause_b_pass_over_live_scope']}")


def checks_open_scope(j):
    b = j["clause_b"]
    tot = b["totals"]
    runs = b["runs"]

    check("(o1) the residual is instrumented on 2 of 6 artifacts / 64 of 340,233 calls",
          tot["artifacts_with_residual_instrumented"] == 2
          and tot["calls_with_residual_measured"] == 64
          and sum(1 for r in runs if r["residual_instrumented"]) == 2
          and sum(r["per_call_differential"].get("n_residual_measured") or 0
                  for r in runs) == 64,
          f"{tot['artifacts_with_residual_instrumented']}/6 artifacts, "
          f"{tot['calls_with_residual_measured']}/{tot['total_calls_compared_live']} calls")
    check("(o2) the four un-instrumented sweeps carry NO fabricated zero: the key is absent, "
          "not 0.0",
          all(r["per_call_differential"].get("max_rel_residual_seen") is None
              and r["per_call_differential"].get("n_residual_measured") is None
              for r in runs if not r["residual_instrumented"]),
          f"{sum(1 for r in runs if not r['residual_instrumented'])} artifacts marked "
          "residual_instrumented=false")
    instr = [r for r in runs if r["residual_instrumented"]]
    check("(o3) the live residual maxima are 1.296e-05 (2 calls) and 1.469e-01 (62 calls)",
          abs(instr[0]["per_call_differential"]["max_rel_residual_seen"]
              - 1.296274642159412e-05) < 1e-17
          and abs(instr[1]["per_call_differential"]["max_rel_residual_seen"]
                  - 0.1468941888932081) < 1e-13,
          " ".join(f"{r['key']}={r['per_call_differential']['max_rel_residual_seen']:.4e}"
                   for r in instr))
    worst = max(r["per_call_differential"]["max_rel_residual_seen"] for r in instr)
    check("(o4) 0 of 64 exceed the 0.5 backstop; the worst sits within 3.4x of it",
          tot["residual_over_backstop_live"] == 0
          and all(r["per_call_differential"]["n_residual_over_backstop"] == 0
                  for r in instr)
          and abs(0.5 / worst - 3.4) < 0.05,
          f"worst={worst:.4e}, 0.5/worst={0.5 / worst:.3f}")

    leaves = [(r["key"], r["artifact_comparison"]["leaves_compared"],
               r["artifact_comparison"]["leaves_moved"]) for r in runs]
    check("(o5) 700 artifact leaves move, out of 2,253 compared -- reported, not repaired",
          tot["artifact_leaves_moved_live"] == 700
          and sum(m for _, _, m in leaves) == 700
          and sum(c for _, c, _ in leaves) == 2253,
          f"{sum(m for _, _, m in leaves)} of {sum(c for _, c, _ in leaves)}; "
          f"leg 221 reported "
          f"{j['leg_221_claim_quoted_not_used']['artifact_leaves_moved_pre_existing']} "
          "over its own smaller scope")
    check("(o5b) the per-artifact moved leaves are 0 / 0 / 105 / 141 / 68 / 386",
          [m for _, _, m in leaves] == [0, 0, 105, 141, 68, 386]
          and [c for _, c, _ in leaves] == [28, 451, 273, 353, 120, 1028],
          str([m for _, _, m in leaves]))
    worst_by_run = {r["key"]: r["artifact_comparison"]["moved_detail_worst_by_rel_diff"]
                    for r in runs}
    check("(o5c) the worst movers are 2.818e-02 (K3 jv_step_study) and 2.409e-02 (L4 gmres_rel)",
          abs(worst_by_run["p2_route_k_v1_port"][0]["rel_diff"] - 0.028181915774792534) < 1e-15
          and abs(worst_by_run["p2_route_l_v1_precond"][0]["rel_diff"]
                  - 0.024091778385417734) < 1e-15
          and abs(worst_by_run["p2_route_g_v1_g2"][0]["rel_diff"]
                  - 2.4243831446619987e-12) < 1e-24,
          f"{worst_by_run['p2_route_k_v1_port'][0]['leaf']} and "
          f"{worst_by_run['p2_route_l_v1_precond'][0]['leaf']}")
    check("(o6) leg 335 confirmed as a side effect: the stepC worst leaf moves by 9.03e-12",
          abs([r for r in runs if r["key"] == "spike1_stepC_gate"][0]
              ["artifact_comparison"]["moved_detail_worst_by_rel_diff"][0]["rel_diff"]
              - 9.028459537851799e-12) < 1e-24,
          f"{[r for r in runs if r['key'] == 'spike1_stepC_gate'][0]['artifact_comparison']['moved_detail_worst_by_rel_diff'][0]['rel_diff']:.4e} "
          "at leg 335's corrected --steps 2500")


def checks_staleness_and_census(j):
    s = j["module_staleness"]
    f = s["fingerprints"]
    check("(s1) main differs from leg 221's final module by +123 bytes / +2 lines, raw",
          s["main_vs_leg221_final"]["byte_delta"] == 123
          and s["main_vs_leg221_final"]["line_delta"] == 2
          and not s["main_vs_leg221_final"]["raw_bytes_identical"]
          and f["main_head"]["n_bytes"] - f["leg_221_final_7e58419"]["n_bytes"] == 123,
          f"{f['leg_221_final_7e58419']['n_bytes']} -> {f['main_head']['n_bytes']} bytes")
    check("(s2) at docstring-stripped AST level main IS the repaired module, and is NOT the pre-repair one",
          s["main_vs_leg221_final"]["ast_nodoc_identical"]
          and s["main_vs_repair_commit"]["ast_nodoc_identical"]
          and not s["main_vs_pre_repair"]["ast_nodoc_identical"]
          and f["main_head"]["ast_nodoc_sha256"]
          == f["repair_commit_d2d9769"]["ast_nodoc_sha256"]
          != f["pre_repair_1a3e63c"]["ast_nodoc_sha256"],
          f"{f['main_head']['ast_nodoc_sha256'][:16]} == repair, != pre-repair "
          f"{f['pre_repair_1a3e63c']['ast_nodoc_sha256'][:16]}")
    c = j["census"]
    check("(s3) census re-grepped live: 15 real importers today, registry banks 6",
          c["n_real_importers_today"] == 15 and c["n_banked_in_registry"] == 6
          and len(c["real_importers_today"]) == 15
          and len(c["leg_221_registry_scripts"]) == 6,
          f"{c['n_real_importers_today']} importers, "
          f"{c['n_banked_in_registry']} banked")
    check("(s4) all 3 newcomers post-date the repair commit d2d9769, so none can carry contamination",
          len(c["newcomer_detail"]) == 3
          and all(n["postdates_repair_d2d9769"] for n in c["newcomer_detail"]),
          ", ".join(os.path.basename(n["script"]) for n in c["newcomer_detail"]))
    check("(s5) 2 files name the module in a string but do not import it",
          len(c["string_mentions_that_are_not_callers"]) == 2,
          ", ".join(c["string_mentions_that_are_not_callers"]))
    check("(s6) the module's own 3 suites pass unchanged",
          j["module_own_suites"]["all_passed"] and j["module_own_suites"]["n_suites"] == 3
          and all(s_["returncode"] == 0 for s_ in j["module_own_suites"]["suites"]),
          f"{j['module_own_suites']['n_suites']} suites, "
          f"{j['module_own_suites']['wall_seconds']} s")


# --------------------------------------------------------------------------- figure
C_PRE, C_POST, C_REF = "#dc2626", "#2563eb", "#6b7280"


def build_figure(j):
    a = j["clause_a"]
    b = j["clause_b"]
    runs, suites, tot = b["runs"], b["test_suite_runs"], b["totals"]

    fig, axes = plt.subplots(2, 2, figsize=(13.0, 8.6))

    # ---- Panel A: the three verdict columns, 18 -> 0 -------------------------
    ax = axes[0][0]
    cols = [("leg 205, committed", a["tally_committed_leg_205"], C_REF, 0.55),
            ("pre-repair, re-measured live", a["tally_remeasured_pre_repair"], C_PRE, 1.0),
            ("post-repair, main today", a["tally_post_repair"], C_POST, 1.0)]
    x = np.arange(len(VERDICTS))
    w = 0.27
    for i, (lab, tally, col, alpha) in enumerate(cols):
        vals = [tally.get(v, 0) for v in VERDICTS]
        ax.bar(x + (i - 1) * w, vals, w, color=col, alpha=alpha, label=lab,
               edgecolor="white", linewidth=0.6)
    ax.annotate("18 → 0", xy=(1 + w, 0.6), xytext=(1.65, 24),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
                fontsize=12, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([v.replace("_", "\n") for v in VERDICTS], fontsize=8)
    ax.set_ylabel("cases (of 81)")
    ax.set_ylim(0, 46)
    ax.set_title("A. Clause (a): leg 205's 81-case battery, three columns\n"
                 "pre-repair column reproduces leg 205 case-by-case, "
                 "0 of 81 verdicts mismatched", fontsize=9.5)
    ax.legend(fontsize=7.5, loc="upper center")

    # ---- Panel B: the three OK -> RAISED adjudications -----------------------
    ax = axes[0][1]
    adj = a["ok_to_nonok_adjudication"]
    tol = adj[0]["module_acceptance_tol"]
    labels, fracs, notes = [], [], []
    for c in adj:
        short = (c["case"].replace("F1 ", "")
                          .replace(" on the leg-73-class grid", "")
                          .replace(" -- UNDER-determined (3 params)", ""))
        labels.append("%s\n(%s)" % (short, c["failure_mode"].split(" (")[0]))
        fracs.append(100.0 * c["pre_margin_inside_tol"] / tol)
        notes.append("%d nodes, rank %d/%d" % (c["measured_window_nodes"],
                                               c["measured_lstsq_rank"],
                                               c["design_matrix_columns"]))
    y = np.arange(len(adj))
    ax.barh(y, fracs, 0.5, color=C_PRE, alpha=0.85, edgecolor="white")
    ax.axvline(100.0, color=C_REF, ls=":", lw=1.4)
    ax.text(115.0, 2.15, "the 5e-4 tolerance itself", color=C_REF, fontsize=8,
            ha="left", va="center")
    for yi, (fr, nt) in enumerate(zip(fracs, notes)):
        ax.text(fr * 1.5, yi, "  %.3f%% of tol  —  %s" % (fr, nt),
                va="center", fontsize=8)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xscale("log")
    ax.set_xlim(0.02, 4e4)
    ax.set_xlabel("pre-repair margin inside the module tolerance (% of 5e-4)")
    ax.set_title("B. The 3 OK → RAISED transitions leg 221 never reported\n"
                 "adjudicated 3 JUSTIFIED_REFUSAL / 0 UNJUSTIFIED_REGRESSION",
                 fontsize=9.5)

    # ---- Panel C: the 340,233-call differential ------------------------------
    ax = axes[1][0]
    units = [(r["key"], r["calls_compared"], r["calls_moved"], False) for r in runs] + \
            [(s["key"], s["calls_compared"], s["calls_moved"], True) for s in suites]
    units = [u for u in units if u[1] > 0]
    y = np.arange(len(units))
    ax.barh(y, [u[1] for u in units], 0.62,
            color=[C_POST if not u[3] else "#93c5fd" for u in units],
            edgecolor="white")
    for yi, u in enumerate(units):
        ax.text(u[1] * 1.15, yi, "%s  —  moved %d" % (f"{u[1]:,}", u[2]),
                va="center", fontsize=7.8)
    ax.set_yticks(y)
    ax.set_yticklabels([u[0] + ("  (suite)" if u[3] else "") for u in units], fontsize=7.5)
    ax.set_xscale("log")
    ax.set_xlim(1, 4e6)
    ax.set_xlabel("calls compared, pre-repair vs post-repair, bitwise (log scale)")
    ax.set_title("C. Clause (b): %s calls compared live, %s bit-identical, %d moved\n"
                 "6 of 6 artifacts ran_live, 0 from cache; cap_binds = %d"
                 % (f"{tot['total_calls_compared_live']:,}",
                    f"{tot['total_calls_compared_live']:,}",
                    tot["total_calls_moved_live"], tot["cap_binds_live"]),
                 fontsize=9.5)

    # ---- Panel D: why the zero holds -----------------------------------------
    ax = axes[1][1]
    occ = [(r["key"], r["per_call_differential"]["min_window_nodes"]) for r in runs] + \
          [(s["key"], s["per_call_differential"]["min_window_nodes"]) for s in suites]
    occ = [o for o in occ if o[1] is not None]
    y = np.arange(len(occ))
    ax.barh(y, [o[1] for o in occ], 0.55, color="#059669", edgecolor="white")
    ax.axvline(3, color=C_PRE, ls="--", lw=1.6)
    ax.text(3.4, len(occ) - 2.5, "min_points floor = 3", color=C_PRE, fontsize=8.5,
            va="center")
    for yi, o in enumerate(occ):
        ax.text(o[1] * 1.12, yi, str(o[1]), va="center", fontsize=8)
    ax.set_yticks(y)
    ax.set_yticklabels([o[0] for o in occ], fontsize=7.5)
    ax.set_xscale("log")
    ax.set_xlim(1, 3e3)
    ax.set_xlabel("minimum window occupancy over the unit's calls (nodes, log scale)")
    ax.set_title("D. Why the zero holds: no banked call comes near either guard\n"
                 "minimum occupancy anywhere = 4 nodes against a floor of 3",
                 fontsize=9.5)

    fig.suptitle("Route-BVRRV (leg 233): leg 221's repair and its zero-contamination "
                 "re-confirmation, both independently re-run — gate YES on both clauses",
                 fontweight="bold", y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.975))
    os.makedirs(os.path.dirname(FIG), exist_ok=True)
    fig.savefig(FIG, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {FIG}")


def main():
    with open(os.path.join(D, "p2_route_bvrrv_v1_postrepair.json")) as fh:
        j = json.load(fh)

    check("(0) the artifact is leg 233 / Route-BVRRV",
          j["leg"] == 233 and j["route"] == "BVRRV", f"{j['route']} at {j['commit'][:7]}")
    checks_lesson_90(j)
    checks_clause_a(j)
    checks_clause_b(j)
    checks_open_scope(j)
    checks_staleness_and_census(j)

    build_figure(j)

    n_fail = sum(1 for _, ok, _ in CHECKS if not ok)
    print(f"\n{len(CHECKS) - n_fail}/{len(CHECKS)} checks passed")
    if n_fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
