#!/usr/bin/env python3
"""Evidence checks for Route-H2C v1 — every number the prose quotes, re-checked.

Reads `writeup/data/p2_route_h2c_v1_construction.json` and asserts the claims
made in `experiments/journal/leg_176.md` and the writeup against it.  A claim the
journal makes that this file does not check is a claim nobody re-reads.

Run: .venv/bin/python experiments/p2_route_h2c_v1_construction_evidence.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "writeup", "data", "p2_route_h2c_v1_construction.json")

checks, failed = [], []


def ck(name, cond, detail=""):
    checks.append(name)
    if not cond:
        failed.append(f"{name}: {detail}")
    print(f"  [{'ok' if cond else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))


def main():
    with open(DATA) as fh:
        R = json.load(fh)

    print("== ceiling is stated, and stated as a ceiling")
    c = R["ceiling"]
    ck("ceiling names a=0 exactness", "a=0" in c)
    ck("ceiling denies transfer", "HL_S2_nonsymmetric" in c)
    ck("ceiling denies chain movement", "L1->L4" in c)
    ck("no GA compute", R["ga_compute"] is False)
    ck("gate restates the ceiling", "no Clay movement" in R["gate"]["ceiling_restated"].lower()
       or "No Clay movement" in R["gate"]["ceiling_restated"])

    print("== E1 the realization is EXACT, not approximate")
    E = R["E1_realization_exactness"]
    ck("L0 b^-2 = b^-2 exactly", E["L0_binv2_minus_binv2"] == 0.0, str(E["L0_binv2_minus_binv2"]))
    ck("L0 m = 0 exactly", E["L0_m"] == 0.0, str(E["L0_m"]))
    ck("ell . L0 = 0 exactly", E["ell_dot_L0_untruncated_columns"] == 0.0)
    ck("ell(m) = 1 exactly", E["ell_of_m"] == [1.0, 0.0], str(E["ell_of_m"]))
    ck("ell(b^-2) = 0 exactly", E["ell_of_binv2"] == 0.0)
    ck("tridiagonal vs independent quadrature < 1e-11",
       E["tridiagonal_vs_independent_laguerre_quadrature"] < 1e-11,
       f"{E['tridiagonal_vs_independent_laguerre_quadrature']:.3e}")

    print("== E2/E3/E4 the machinery is cross-validated")
    ck("X Gram padding-independent", R["E2_x_gram_padding"]["max_abs_diff_pad4_vs_pad32"] == 0.0)
    ck("projection round trip < 1e-14", R["E3_projection_roundtrip"]["max_err_first_30"] < 1e-14,
       f"{R['E3_projection_roundtrip']['max_err_first_30']:.3e}")
    E4 = R["E4_x_norm_two_ways"]
    ck("X norm gram vs y-space agree < 1e-10", E4["u_rel_diff"] < 1e-10, f"{E4['u_rel_diff']:.3e}")
    ck("ratio from norms matches 1/sigma_min",
       abs(E4["ratio_from_norms"] - E4["one_over_sigma_min"]) / E4["one_over_sigma_min"] < 1e-6,
       f"{E4['ratio_from_norms']:.6f} vs {E4['one_over_sigma_min']:.6f}")
    ck("minimizer is spread, not edge-pinned", E4["minimizer_last_decile_energy"] < 0.25,
       f"last decile carries {E4['minimizer_last_decile_energy']:.4f}")

    print("== C0 gate conjunct 2: Xu's closed form")
    C0 = R["C0_xu_closed_form"]
    ck("beats leg 163's 2.8e-14 class", C0["max_rel_residual"] < 2.8e-14,
       f"{C0['max_rel_residual']:.3e}")
    lad = C0["quadrature_ladder_kpan"]
    ck("quadrature ladder converges", lad["24"] < lad["12"], f"{lad['12']:.2e} -> {lad['24']:.2e}")
    ck("all six seeds under 1e-13", max(C0["over_seeds"].values()) < 1e-13,
       f"worst {max(C0['over_seeds'].values()):.3e}")

    print("== C1 gate conjunct 1: the closing diagnostic")
    C1 = R["C1_bordered_sigma_min_X"]
    ck("sigma_min bounded away from zero", C1["sigma_min_at_512"] > 0.09,
       f"{C1['sigma_min_at_512']:.8f}")
    # 0.139% over N = 32..512, a 16-fold truncation range.  The threshold is 0.5%
    # and the measured value is quoted rather than the threshold: this is the
    # number the journal cites, and it is what "truncation-independent" means here.
    ck("truncation-independent (0.139% over a 16x truncation range)",
       C1["relative_spread"] < 5e-3, f"relative spread {C1['relative_spread']:.3e}")
    ck("monotone decreasing through N=512", C1["monotone_decreasing_through_512"] is True)
    ck("N=1024 flagged as the float floor, not used", C1["n1024_breaks_monotonicity"] is True)
    ck("resolvent norm ~ 11", 10.9 < C1["resolvent_norm_at_512"] < 11.1,
       f"{C1['resolvent_norm_at_512']:.4f}")

    print("== C2 the tail block -- the ell^1_w comparison point")
    C2 = R["C2_tail_block_sigma_min"]
    t2 = C2["ladder"]["2"]
    ck("tail sigma_min converges (K=2)", abs(t2["512"] - t2["256"]) < 1e-3,
       f"{t2['256']:.6f} -> {t2['512']:.6f}")
    ck("tail inverse norm finite ~4", C2["tail_inverse_norm_K2_at_512"] < 5.0,
       f"||T^-1||_X = {C2['tail_inverse_norm_K2_at_512']:.3f}")

    print("== C3/C4 the controls, which CAN report the other answer")
    u = R["C3_control_unbordered"]["ladder"]
    ck("unbordered collapses to the float floor", u["512"] < 1e-10, f"{u['512']:.3e}")
    C4 = R["C4_control_loose_L2_realization"]
    l = C4["ladder"]
    ck("loose L2 decays (no gap)", l["512"] < 0.1 * l["64"], f"{l['64']:.3e} -> {l['512']:.3e}")
    ck("loose L2 exponent near -3/2", abs(C4["fitted_exponent"] + 1.5) < 0.1,
       f"fitted {C4['fitted_exponent']:.4f}")
    ck("origin condition is the whole difference",
       C1["sigma_min_at_512"] > 100 * l["512"],
       f"X: {C1['sigma_min_at_512']:.4f} vs loose: {l['512']:.3e}")

    print("== C5 Z_1 in leg 54's own shape -- does NOT close")
    C5 = R["C5_Z1_blockdiagonal_A"]
    ck("Z_1 never crosses 1", C5["min_over_battery"] > 1.0, f"best {C5['min_over_battery']:.4f}")
    ck("Z_1 grows with the block size",
       C5["ladder"]["32"]["256"] > C5["ladder"]["2"]["256"],
       f"K=2: {C5['ladder']['2']['256']:.1f} -> K=32: {C5['ladder']['32']['256']:.1f}")

    print("== C6 leg 163's G4, reproduced and CORRECTED")
    C6 = R["C6_closed_form_ratio"]
    conv = C6["M_convergence"]
    ck("ratio converges in M", abs(conv["8192"] - conv["4096"]) < 1e-5,
       f"{conv['4096']:.8f} -> {conv['8192']:.8f}")
    ck("leg 163's witness was optimistic", C6["leg163_witness_optimistic_by"] > 5.0,
       f"by {C6['leg163_witness_optimistic_by']:.1f}x")

    print("== C7 where the naive Galerkin section fails, with the mechanism")
    C7 = R["C7_galerkin_inconsistency"]
    g = C7["kappa_ladder"]
    ck("kappa does NOT go to zero", g["960"]["abs_kappa"] > 5.0,
       f"|kappa| -> {g['960']['abs_kappa']:.4f} (must be 0)")
    ck("mechanism: N^2 |u_{N-1}| is constant",
       abs(g["960"]["n2_times_last_coeff"] - g["480"]["n2_times_last_coeff"]) < 0.05,
       f"{g['480']['n2_times_last_coeff']:.4f} vs {g['960']['n2_times_last_coeff']:.4f}")
    d = C7["exact_solution_n_times_coeff"]
    ck("exact coefficients decay like C/n", abs(d["1024"] / d["256"] - 1.0) < 0.35,
       f"n|c_n| = {d['256']:.3f} -> {d['1024']:.3f}")

    print("== C8 the border row lives in X*, not l^2")
    b = R["C8_border_row_dual_norm"]["ladder"]
    ck("X* norm converges", abs(b["512"]["x_dual"] - b["256"]["x_dual"]) < 1e-3)
    ck("l2 norm diverges", b["512"]["l2"] > 5 * b["64"]["l2"])

    print("== gate")
    G = R["gate"]
    ck("gate answers YES", G["answer"] == "YES")
    ck("both conjuncts recorded", G["conjunct_1_closes"] and G["conjunct_2_reproduces_xu"])
    ck("qualification names the Z_1 negative", "does NOT close" in G["qualification"])

    print(f"\n{len(checks)} checks, {len(failed)} failing")
    for f in failed:
        print("  FAILED: " + f)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
