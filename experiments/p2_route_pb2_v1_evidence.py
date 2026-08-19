#!/usr/bin/env python3
"""Leg 410 / unit PB2 -- rebuilds EVERY claim in the journal from the curated JSON.

Re-runs NOTHING.  ORCHESTRATION.md section 6 clause 3: the evidence script rebuilds the
figures/claims from `writeup/data/*.json` without re-running the experiment.

Run:  .venv/bin/python experiments/p2_route_pb2_v1_evidence.py
Exit: 0 iff every banked control fired as planted and every claim below reproduces.
"""

import json
import sys
from pathlib import Path

D = json.loads((Path(__file__).resolve().parents[1] / "writeup" / "data"
                / "p2_route_pb2_v1.json").read_text())

fails = []


n_checks = [0]


def check(name, cond, shown):
    n_checks[0] += 1
    print(("  OK   " if cond else "  FAIL ") + "%-52s %s" % (name, shown))
    if not cond:
        fails.append(name)


print("PB2 (leg 410) -- W4 clause (b), the mdot == 0 exit.  Rebuilt from the JSON.\n")
print("THE OBJECT (L5's mdot == 0 branch, modulation mode='SS')")
o = D["object"]
check("mdot is exactly zero", o["mdot"] == 0.0, "mdot = %s" % o["mdot"])
check("alpha is the pinned 1", o["alpha"] == 1.0, "alpha = %s, lambda = %s, a = %s"
      % (o["alpha"], o["lambda"], o["a"]))
check("a > 0, as Tsai (1.2) requires", o["a"] > 0, "a = %s" % o["a"])

print("\nCONTROLS")
for k, v in D["controls"].items():
    check(k, v["fired_as_planted"], "fired_as_planted = %s" % v["fired_as_planted"])

print("\nM1/M2 -- boundedness and the far-field amplitude")
m1, m2 = D["measurements"]["M1_sup_norm"], D["measurements"]["M2_far_field_amplitude"]
check("sup|U| finite => U in L^inf", m1["U_in_L_infinity"], "sup|U| = %.12f" % m1["sup_abs_U"])
check("sup|U| == 2|w| (attained at the origin)",
      abs(m1["sup_abs_U"] - 2 * o["abs_w"]) < 1e-9, "2|w| = %.12f" % (2 * o["abs_w"]))
check("|A| never vanishes on S^2", not m2["vanishes_anywhere_on_S2"],
      "min |A| = %.8f = |w|" % m2["min_over_S2_abs_A"])
check("numeric A matches the closed form", m2["max_rel_err"] < 1e-7,
      "max rel err = %.2e" % m2["max_rel_err"])

print("\nM3 -- the NRS (q = 3) hypothesis")
m3 = D["measurements"]["M3_q_equals_3_NRS_hypothesis"]
check("U is NOT in L^3(R^3)", m3["U_in_L3_R3"] is False, m3["int_R3_abs_U_cubed"])
check("decade increments are CONSTANT (log divergence)",
      abs(m3["increment_ratio_last_over_previous"] - 1.0) < 1e-6,
      "ratio = %.12f" % m3["increment_ratio_last_over_previous"])
check("log coefficient matches int_{S^2}|A|^3 analytically",
      m3["rel_error_vs_analytic"] < 1e-9,
      "measured %.10f vs analytic %.10f (rel %.1e)"
      % (m3["measured_log_coefficient"], m3["analytic_log_coefficient_int_S2_absA_cubed"],
         m3["rel_error_vs_analytic"]))

print("\nM4 -- the TSAI THEOREM 1 hypothesis (U in L^q, q in (3, inf])")
m4 = D["measurements"]["M4_q_gt_3_TSAI_THM1_hypothesis"]
for q, row in m4["norms"].items():
    check("q = %-6s finite, convergence-controlled" % q,
          row["finite"] and row["resolution_doubled_rel_change"] < 1e-8
          and row["seam_moved_rel_change"] < 1e-8,
          "||U||_q = %.12f  (res %.1e, seam %.1e, tail frac %.1e)"
          % (row["norm"], row["resolution_doubled_rel_change"], row["seam_moved_rel_change"],
             row["tail_fraction"]))
check("U in L^q for EVERY q in (3, inf]", m4["U_in_Lq_for_every_q_in_open_3_inf"], "yes")

print("\nM5 -- the TSAI THEOREM 2 hypothesis (the local energy estimate (1.4))")
m5 = D["measurements"]["M5_local_energy_estimate_TSAI_THM2_hypothesis"]
rows = m5["rows"]
# both tails approach their limits like O(1/lambda) (the |y|^-1 decay), so the honest check is
# RELATIVE change over the last two lambda decades -- and that the increments are SHRINKING.
kin = [r["half_L2_of_u_over_B1"] for r in rows]
gra = [r["int_ball_absGradU_squared"] for r in rows]
check("ess sup_t (1/2)int_{B_1}|u|^2 converges",
      abs(kin[-1] - kin[-2]) / kin[-1] < 1e-6 and abs(kin[-1] - kin[-2]) < abs(kin[-2] - kin[-3]),
      "-> %.9f  (last rel change %.1e, shrinking)"
      % (m5["ess_sup_t_half_L2_over_B1"], abs(kin[-1] - kin[-2]) / kin[-1]))
check("int_{R^3}|grad U|^2 converges",
      abs(gra[-1] - gra[-2]) / gra[-1] < 1e-6 and abs(gra[-1] - gra[-2]) < abs(gra[-2] - gra[-3]),
      "-> %.9f  (last rel change %.1e, shrinking)"
      % (m5["int_R3_absGradU_squared_converges_to"], abs(gra[-1] - gra[-2]) / gra[-1]))
check("(1.4) is FINITE", m5["estimate_1p4_finite"],
      "space-time Dirichlet integral = %.9f"
      % m5["space_time_dirichlet_integral_nu_1_T_minus_t3_1"])

print("\nTHE GATE")
g = D["gate"]
check("answer is YES", g["answer"] == "YES", g["answer"])
check("the carrier is Tsai, not NRS", "THEOREM 2" in g["which_theorem"]
      and "DOES NOT APPLY" in g["which_theorem"], g["which_theorem"])
check("clause (b) stands", g["clause_b_stands"], "True")
check("the ceiling is stated and is TIER 2", D["ceiling"].startswith("TIER 2"),
      "no L1->L4 link moved; Clay ~0.05%")

print("\n%s  (%d checks, %d failed)"
      % ("ALL CLAIMS REBUILD" if not fails else "REBUILD FAILED: " + ", ".join(fails),
         n_checks[0], len(fails)))
sys.exit(1 if fails else 0)
