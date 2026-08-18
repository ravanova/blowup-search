#!/usr/bin/env python3
"""Leg 400 / unit L5 -- the EVIDENCE CHECK for writeup/data/p2_route_l5_finite_energy_v1.json.

Lesson 68: an artefact that nobody can re-derive from is a claim, not evidence.  This script
re-derives, from the SOURCE artefact `writeup/data/p2_route_cloc_v1.json` and from the L5
artefact's own rows, every number the journal quotes, and EXITS NON-ZERO on any disagreement.
It quotes no prose and reads no STATE.md (pre-committed reading (d)).

Run:  .venv/bin/python experiments/p2_route_l5_v1_evidence.py
"""

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
L5J = ROOT / "writeup" / "data" / "p2_route_l5_finite_energy_v1.json"
CLOCJ = ROOT / "writeup" / "data" / "p2_route_cloc_v1.json"

fails = []


def ck(name, ok, detail=""):
    print("%-58s %s   %s" % (name, "OK  " if ok else "FAIL", detail))
    if not ok:
        fails.append(name)


def fit(xs, ys):
    x = np.log(np.asarray(xs, float))
    y = np.log(np.maximum(np.asarray(ys, float), 1e-300))
    A = np.vstack([x, np.ones_like(x)]).T
    sol, *_ = np.linalg.lstsq(A, y, rcond=None)
    return float(sol[0])


def main():
    if not L5J.exists():
        print("MISSING %s" % L5J)
        return 2
    d = json.loads(L5J.read_text())
    c = json.loads(CLOCJ.read_text())

    # --- 1.  the bill was copied from the ARTEFACT, not from prose --------------------------
    b = d["bill_from_artefact"]
    ck("bill.source_self_hash == cloc self_hash",
       b["source_self_hash"] == c["self_hash"], b["source_self_hash"])
    b3 = c["check_B3_Lp_thresholds"]
    for k in ("L2_threshold_alpha", "L3_threshold_alpha", "deficit_to_L2_in_exponent",
              "required_over_available_exponent_ratio"):
        ck("bill.%s re-read from cloc" % k, b[k] == b3[k], repr(b[k]))
    ck("bill.increment_per_decade re-read from cloc",
       b["increment_per_decade_L3_cube"]
       == c["check_C2_critical_L3_tail_is_log_divergent_at_alpha_1"]["increment_per_decade"][0],
       repr(b["increment_per_decade_L3_cube"]))

    # --- 2.  controls ------------------------------------------------------------------------
    C = d["controls"]
    c1 = C["C1_reproduces_leg381"]
    ck("C1 reproduces leg 381 banked rho-exponents",
       c1["fired_as_planted"], "max|dev| = %.3e" % c1["max_abs_disagreement_vs_banked"])
    # independently re-fit C1's own rows -- the artefact must not be able to lie about its fit
    worst = 0.0
    for a in ("alpha=1", "alpha=1.25"):
        rows = c1[a]["rows"]
        for k, v in c1[a]["reimplemented_rho_exponents"].items():
            e = fit([r["rho"] for r in rows], [r[k] for r in rows])
            worst = max(worst, abs(e - v))
    ck("C1 exponents re-fit from C1's own rows", worst < 1e-9, "max|dev| = %.3e" % worst)

    c2 = C["C2_negative_no_cutoff"]
    ck("C2 chi==1 gives R_loc == 0", c2["max_abs_R_loc_without_cutoff"] == 0.0,
       "max|R_loc| = %r" % c2["max_abs_R_loc_without_cutoff"])

    cc = C["C4b_exact_DSS_collapse_reading_c"]
    ck("reading (c): kappa=0 branch IS exactly DSS",
       cc["kappa=0_similarity_frozen"]["is_exactly_DSS"],
       "defect %.2e" % cc["kappa=0_similarity_frozen"]["max_rel_dss_defect"])
    ck("reading (c): kappa=a branch is NOT exactly DSS",
       not cc["kappa=a_physical_frozen"]["is_exactly_DSS"],
       "defect %.4f" % cc["kappa=a_physical_frozen"]["max_rel_dss_defect"])

    c8 = C["C8_energy_Clay_condition_7"]
    ck("C8 energy: beta = kappa - a in all three branches",
       c8["max_abs_beta_error_vs_prediction"] < 1e-3,
       "max|dev| = %.2e" % c8["max_abs_beta_error_vs_prediction"])
    ck("C8 both directions fire", c8["fired_as_planted"])

    c3p = C["C3p_modulation_amplitude_linearity"]
    ck("C3' error is LINEAR in the modulation amplitude",
       c3p["linear_in_amplitude_rel_spread"] < 1e-2,
       "rel spread %.2e" % c3p["linear_in_amplitude_rel_spread"])

    c6 = C["C6_basis"]
    ck("C6 exponent independent of the cutoff basis", c6["fired_as_planted"],
       "dL3 %.2e dcurl %.2e" % (c6["exponent_disagreement_L3"], c6["exponent_disagreement_curl"]))

    c9 = C["C9_refinement"]
    ck("C9 norms stable under refinement", c9["worst_rel_change"] < 5e-2,
       "worst rel change %.2e" % c9["worst_rel_change"])

    c7 = C["C7_modulation_absorption_falsifier"]
    ck("C7 falsifier reported (either direction)", "flips_gate_to_YES" in c7,
       "exponent before %.4f -> after %.4f, flips=%s"
       % (c7["rho_exponent_before"], c7["rho_exponent_after"], c7["flips_gate_to_YES"]))

    # --- 3.  the sweep: every banked exponent re-fit from the banked rows ---------------------
    sw = d["sweep"]
    worst = 0.0
    for key, ent in sw.items():
        rr = [v["rho0"] for v in ent["rows"]]
        for k in ("L3", "curl_L32"):
            worst = max(worst, abs(fit(rr, [v[k] for v in ent["rows"]])
                                   - ent[k + "_rho_exponent"]))
    ck("sweep exponents re-fit from the banked rows", worst < 1e-9, "max|dev| = %.3e" % worst)

    # --- 4.  the structural facts the gate rests on -------------------------------------------
    kA = "alpha=1|kappa=a_physical_frozen|DSS"
    kS = "alpha=1|kappa=a_physical_frozen|SS"
    k0 = "alpha=1|kappa=0_similarity_frozen|DSS"
    e = sw[kA]
    ck("C4: T1+T2 cancel at kappa=a", e["T12_over_T1_at_largest_rho"] < 1e-5,
       "|T1+T2|/|T1| = %.2e" % e["T12_over_T1_at_largest_rho"])
    ck("total error IS the modulation commutator T3",
       abs(e["total_over_T3_at_largest_rho"] - 1.0) < 5e-2,
       "|R_loc|/|T3| = %.6f" % e["total_over_T3_at_largest_rho"])
    ck("DSS kappa=a: velocity exponent is 0 (rho buys nothing)",
       abs(e["L3_rho_exponent_tail3"]) < 5e-2, "%.6f" % e["L3_rho_exponent_tail3"])
    ck("DSS kappa=a: vorticity exponent is 0 (rho buys nothing)",
       abs(e["curl_L32_rho_exponent_tail3"]) < 5e-2, "%.6f" % e["curl_L32_rho_exponent_tail3"])
    ck("C3: the SS control DOES fall off (exponent ~ -2)",
       sw[kS]["curl_L32_rho_exponent_tail3"] < -1.5,
       "%.6f" % sw[kS]["curl_L32_rho_exponent_tail3"])
    ck("C4: kappa=0 does NOT cancel T1+T2",
       sw[k0]["T12_over_T1_at_largest_rho"] > 1e-3,
       "|T1+T2|/|T1| = %.4f" % sw[k0]["T12_over_T1_at_largest_rho"])

    # --- 5.  C5, the alpha bill: exponent must track 1 - alpha --------------------------------
    devs = []
    for a in (1.0, 1.25, 1.6):
        k = "alpha=%g|kappa=a_physical_frozen|DSS" % a
        devs.append((a, sw[k]["curl_L32_rho_exponent_tail3"], 1.0 - a))
    worst = max(abs(m - p) for _, m, p in devs)
    ck("C5: measured exponent tracks 1 - alpha", worst < 8e-2,
       "; ".join("a=%g meas %.4f pred %.2f" % t for t in devs))

    # --- 6.  the gate arithmetic re-derived --------------------------------------------------
    g = d["gate"]
    per_s = sw[kA]["curl_L32_at_largest_rho"]
    ck("gate.c_mod_per_unit_s == sweep value", abs(g["c_mod_per_unit_s"] - per_s) < 1e-12,
       "%.6f" % g["c_mod_per_unit_s"])
    per_period = per_s * c["check_A_field_is_what_it_claims"]["period_in_s"]
    ck("gate.c_mod_per_DSS_period = c_mod * 2 log lambda",
       abs(g["c_mod_per_DSS_period"] - per_period) < 1e-9, "%.6f" % per_period)
    for eps in g["N_periods_affordable_by_threshold"]:
        n = float(eps) / per_period
        ck("gate.N(eps=%s) = eps / (c_mod 2 log lambda)" % eps,
           abs(g["N_periods_affordable_by_threshold"][eps] - n) < 1e-9 * max(1.0, n),
           "%.6g periods" % n)
    ck("gate answer is NO", g["answer"] == "NO", g["answer"])
    ck("gate is threshold-free (holds for every eps_close > 0)",
       g["threshold_free"] is True)
    ck("no L1->L4 link moved", d["chain"]["links_moved"] == [])

    print("")
    if fails:
        print("EVIDENCE CHECK: FAIL (%d)" % len(fails))
        for f in fails:
            print("   - " + f)
        return 1
    print("EVIDENCE CHECK: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
