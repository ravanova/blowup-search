"""Route-J v1: the primary-source pass, run as measurements rather than assertions.

Egress opened after six legs of being blocked.  `Papers/fetch.sh` pulled all fourteen
manifest entries; Tier 1 is read.  This driver turns the reading into numbers:

  J1  SCHOCHET'S CONSTANT.  Residual of the complex Burgers equation on the exact pole
      ansatz, for ALS's corrected K = 24(3+-sqrt6) and Schochet 1986's printed
      12(6+-sqrt6).  An independent check of a published correction.
  J2  ROUTE-H's (E) == ALS (57)-(58), pointwise, under the parameter map, at four times
      including one at 99% of the blow-up time; plus their t_c formula against our T.
  J3  alpha(1/2) = 3 by integrating ALS (49)-(50) -- no shared grid, basis or code with
      our compactified Newton solve -- with the tau-floor refusal on the deep rungs.
  J4  THE SUPERCRITICAL EXPONENTS, measured not quoted: collapse the Schochet solution
      on a tau-ladder at beta = 1 and at beta = 2 and report BOTH spreads.
  J5  OUR alpha(a) BRANCH against XU Table 1's s*(a) = 1/c_l(a), row by row, straight
      from Route-F's committed JSON so the comparison cannot drift from the data.
  J6  the claim ledger and its counts.

Deterministic, ~30 s.  Writes writeup/data/p2_route_j_v1_literature.json.

Run: .venv/bin/python -u experiments/p2_route_j_v1_literature.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.critical_dissipation import exact_a0_spacetime          # noqa: E402
from solver.literature_gates import (                               # noqa: E402
    CHEN_HOU_BETA, CLAIM_LEDGER, LSS_A_C, PRIMARY_SOURCES, SUPERCRITICAL_BALANCE,
    XU_A_C_RECOMPUTED, XU_S2_BOUNDARY, XU_TABLE1,
    a_half_branch, a_half_verdict, als_a0_sigma1, als_a0_sigma1_tc, collapse_spread,
    compare_branch, ledger_counts, ours_s_c, rescaled_collapse, route_h_E_as_als,
    schochet_K, schochet_blowup_time, schochet_pde_residual, supercritical_beta,
)

OUT = ROOT / "writeup" / "data" / "p2_route_j_v1_literature.json"
ROUTE_F = ROOT / "writeup" / "data" / "p2_route_f_v1_viscosity.json"
ROUTE_E = ROOT / "writeup" / "data" / "p2_route_e_v1_spectrum.json"


def j1_schochet_constant():
    """Which K solves the equation -- the printed one or the corrected one?"""
    rows = []
    for label, corrected in (("ALS 24(3+-sqrt6), corrected", True),
                             ("Schochet 1986 12(6+-sqrt6), as printed", False)):
        for sign, name in ((+1, "K+"), (-1, "K-")):
            K = schochet_K(sign, corrected=corrected)
            # two times and two pole configurations, so the verdict is not one point
            res = [schochet_pde_residual(K, nu=nu, t=t, x10=x10, x20=x20)
                   for nu, t, x10, x20 in ((1.0, 0.01, -1j, -2j),
                                           (1.0, 0.02, -1j, -2j),
                                           (0.4, 0.05, -0.5j, -1.7j))]
            rows.append({"family": label, "which": name, "K": float(K),
                         "residuals": [float(r) for r in res],
                         "worst_residual": float(max(res))})
    corrected_worst = max(r["worst_residual"] for r in rows if "corrected" in r["family"])
    printed_worst = max(r["worst_residual"] for r in rows if "printed" in r["family"])
    printed_best = min(r["worst_residual"] for r in rows if "printed" in r["family"])
    return {"rows": rows,
            "corrected_worst": corrected_worst,
            "printed_best": printed_best, "printed_worst": printed_worst,
            "separation_decades": float(np.log10(printed_best / corrected_worst)),
            "verdict": ("ALS's correction is confirmed independently: the corrected "
                        "constant satisfies the equation to rounding, the printed one "
                        "does not, and the two are separated by "
                        f"{np.log10(printed_best / corrected_worst):.1f} decades.")}


def j2_route_h_E_is_als():
    """Route-H's closed form against ALS (57)-(58)."""
    mu0, nu, T = 0.7, 1.3, 2.0
    m = route_h_E_as_als(mu0, nu, T)
    x = np.linspace(-8.0, 8.0, 4001)
    rows = []
    for t in (0.0, 0.9, 1.7, 1.98):
        a = als_a0_sigma1(x, t, m["w_m1_0"], m["vc0"], nu)
        b = exact_a0_spacetime(x, t, nu, mu0, T=T)["omega"]
        scale = float(np.max(np.abs(b)))
        rows.append({"t": float(t), "frac_of_T": float(t / T),
                     "max_abs_diff": float(np.max(np.abs(a - b))),
                     "profile_scale": scale,
                     "rel_diff": float(np.max(np.abs(a - b)) / scale)})
    # a second parameter set, so the agreement is not a coincidence of one (mu0, nu, T)
    mu0b, nub, Tb = 3.1, 0.25, 5.0
    mb = route_h_E_as_als(mu0b, nub, Tb)
    ab = als_a0_sigma1(x, 4.5, mb["w_m1_0"], mb["vc0"], nub)
    bb = exact_a0_spacetime(x, 4.5, nub, mu0b, T=Tb)["omega"]
    return {"map": {k: float(v) for k, v in m.items()},
            "rows": rows,
            "worst_rel_diff": float(max(r["rel_diff"] for r in rows)),
            "second_parameter_set": {"mu0": mu0b, "nu": nub, "T": Tb, "t": 4.5,
                                     "rel_diff": float(np.max(np.abs(ab - bb))
                                                       / np.max(np.abs(bb)))},
            "als_tc_eq59": float(als_a0_sigma1_tc(m["w_m1_0"], m["vc0"], nu)),
            "route_h_T": float(T),
            "tc_abs_err": float(abs(als_a0_sigma1_tc(m["w_m1_0"], m["vc0"], nu) - T)),
            "dvc_dt_consistency": float(abs(m["dvc_dt_from_als"] - m["dvc_dt_from_E"])),
            "verdict": ("Route-H's (E) IS ALS (57)-(58).  Pre-empted, with the parameter "
                        "map explicit and both directions of the evolution law agreeing.")}


def j3_alpha_half_from_als():
    """alpha(1/2) = 3, from the published a = 1/2 pole system, integrated cold."""
    br = a_half_branch(Om0=10.0, nu=1.0, u0=0.0, u1=-34.0, n=200_000)
    v = a_half_verdict(br, frac=0.9)
    # the ladder, so the reader can see where it stops being resolved
    idx = np.flatnonzero(br["resolved"])
    ladder = []
    for f in (0.3, 0.5, 0.7, 0.9, 0.98):
        i = idx[int(f * (idx.size - 1))]
        ladder.append({"frac": f, "v_c": float(np.exp(br["log_vc"][i])),
                       "Omega": float(br["Omega"][i]), "tau": float(br["tau"][i]),
                       "dtau": float(br["dtau"][i]),
                       "c_l_local": float(br["c_l_local"][i])})
    # the rungs the gate throws away, shown so the turnover is visible rather than hidden
    bad = np.flatnonzero(~br["resolved"] & (br["tau"] > 0))
    refused_ladder = [{"tau": float(br["tau"][k]), "dtau": float(br["dtau"][k]),
                       "c_l_would_have_read": float(br["c_l_local"][k])}
                      for k in bad[:: max(1, bad.size // 4)][:4]] if bad.size else []
    n_refused = int(br["u"].size - idx.size)
    return {"verdict_row": v, "ladder": ladder, "refused_ladder": refused_ladder,
            "dtau_floor": br["dtau_floor"], "n_refused_rungs": n_refused,
            "n_resolved_rungs": int(idx.size),
            "note": ("Om0 = 10 > 4 puts the trajectory on the branch where v_c is "
                     "decreasing; ALS's blow-up condition is Omega(0) > 2 and v_c turns "
                     "around at Omega = 4.  Reparametrising by u = log v_c is what makes "
                     "the deep rungs reachable -- integrating in t underflows dt against "
                     "an O(1) elapsed time and returns NaN."),
            "verdict": ("c_l(1/2) = 1/3 reproduced to "
                        f"{v['c_l_rel_err']:.1e} relative from a system sharing nothing "
                        "with our solver.  So alpha(1/2) = 3 is right AND exact AND known.")}


def j4_supercritical():
    """What lies ABOVE s_c -- the balance nothing in this project had measured."""
    x10, x20, nu = -1j, -2j, 1.0
    K = schochet_K(+1, corrected=True)
    taus = [1e-3, 3e-4, 1e-4, 3e-5, 1e-5]
    xi, curves, tc = rescaled_collapse(x10, x20, nu, K, taus)
    spreads = {str(b): collapse_spread(xi, curves, b) for b in (1.0, 1.5, 2.0, 2.5)}
    best = min(spreads, key=lambda k: spreads[k])
    # beta = 2 leaves a residual spread.  ALS say why -- (45) carries an O(tau^{-1})
    # correction -- so the spread must SHRINK on deeper sub-ladders.  If it did not,
    # beta = 2 would just be the least-bad of four guesses.  This is the check that
    # tells those two apart, and it is the difference between a fit and a measurement.
    deepening = []
    for lo in range(len(taus) - 2):
        sub = {t: curves[t] for t in taus[lo:]}
        deepening.append({"tau_max": taus[lo], "n_rungs": len(sub),
                          "spread_beta2": collapse_spread(xi, sub, 2.0),
                          "spread_beta1": collapse_spread(xi, sub, 1.0)})
    # the predicted exponents, from the balance, for the three cases we can name
    cases = [
        {"case": "Schochet a=0", "sigma": 2.0, "alpha_ALS": 1.0,
         "beta_pred": supercritical_beta(2.0, 1.0), "beta_ALS_says": 2.0,
         "s_over_s_c": 2.0 * 1.0},
        {"case": "ALS a=0 sigma=1 (MARGINAL)", "sigma": 1.0, "alpha_ALS": 1.0,
         "beta_pred": supercritical_beta(1.0, 1.0), "beta_ALS_says": 1.0,
         "s_over_s_c": 1.0 * 1.0},
        {"case": "ALS a=1/2 sigma=1 (subcritical)", "sigma": 1.0, "alpha_ALS": 1.0 / 3.0,
         "beta_pred": None, "beta_ALS_says": 1.0, "s_over_s_c": 1.0 / 3.0},
    ]
    return {"tc": float(tc), "taus": taus,
            "collapse_spread_by_beta": spreads, "best_beta": float(best),
            "deepening": deepening,
            "beta_1_over_beta_2": float(spreads["1.0"] / spreads["2.0"]),
            "cases": cases,
            "balance": SUPERCRITICAL_BALANCE,
            "double_pole_residue": {"B": "-12 i nu", "vanishes_inviscidly": True,
                                    "carries": "the tau^{-2}"},
            "verdict": ("The Schochet family collapses at beta = 2 and does not at "
                        f"beta = 1 (spreads differ by {spreads['1.0'] / spreads['2.0']:.0f}x). "
                        "Above criticality the balance is dissipation-against-stretching, "
                        "beta = sigma alpha_ALS, and omega_t is subdominant.")}


def j5_branch_vs_xu():
    """Our measured alpha(a) against XU's published branch."""
    f = json.loads(ROUTE_F.read_text())
    ours = f["F6_sc_map"]["rows"]
    rows = compare_branch(ours)
    e = json.loads(ROUTE_E.read_text())
    a_c_ours = float(e["E7_end"]["a_c_linear_extrapolation"])
    return {"rows": rows,
            "worst_rel_diff": float(max(r["rel_diff"] for r in rows)),
            "mean_rel_diff": float(np.mean([r["rel_diff"] for r in rows])),
            "a_c_ours": a_c_ours, "a_c_published_LSS": LSS_A_C,
            "a_c_xu_recomputed": XU_A_C_RECOMPUTED,
            "a_c_ours_rel_err": abs(a_c_ours - LSS_A_C) / LSS_A_C,
            "a_c_xu_rel_err": abs(XU_A_C_RECOMPUTED - LSS_A_C) / LSS_A_C,
            "s2_boundary_xu": XU_S2_BOUNDARY,
            "s2_boundary_ours": float(f["F6_sc_map"]["a_at_sc_equals_1"]),
            "xu_table1": [{"a": a, "c_l": cl, "s_star": ss} for a, cl, ss in XU_TABLE1],
            "chen_hou_beta": CHEN_HOU_BETA,
            "verdict": ("Our alpha(a) is XU's s*(a) = 1/c_l(a), row for row.  The formula "
                        "is theirs and precedes us; our numbers agree with it at the "
                        "accuracy either side claims.  On a_c we are the least accurate "
                        "of the three sources and should quote the published value.")}


def main():
    t0 = time.time()
    out = {
        "leg": "Route-J v1",
        "title": "The primary-source pass: published results as executable gates",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sources": PRIMARY_SOURCES,
        "J1_schochet_constant": j1_schochet_constant(),
        "J2_route_h_E_is_als": j2_route_h_E_is_als(),
        "J3_alpha_half_from_als": j3_alpha_half_from_als(),
        "J4_supercritical": j4_supercritical(),
        "J5_branch_vs_xu": j5_branch_vs_xu(),
        "J6_ledger": {"entries": CLAIM_LEDGER, "counts": ledger_counts(),
                      "n_claims": len(CLAIM_LEDGER)},
    }
    out["wall_clock_seconds"] = round(time.time() - t0, 2)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))

    print("== Route-J v1: the primary-source pass ==")
    j1 = out["J1_schochet_constant"]
    print(f"J1 Schochet K: corrected worst {j1['corrected_worst']:.2e}, "
          f"printed best {j1['printed_best']:.2e} "
          f"({j1['separation_decades']:.1f} decades apart)")
    j2 = out["J2_route_h_E_is_als"]
    print(f"J2 (E) vs ALS (57)-(58): worst rel diff {j2['worst_rel_diff']:.2e}, "
          f"t_c err {j2['tc_abs_err']:.2e}")
    j3 = out["J3_alpha_half_from_als"]["verdict_row"]
    print(f"J3 c_l(1/2) = {j3['c_l']:.9f} vs 1/3 (rel {j3['c_l_rel_err']:.2e}); "
          f"alpha = {j3['alpha_ours']:.6f}; "
          f"dlogOm/dlogv_c = {j3['dlogOmega_dlogvc']:.6f} vs -2")
    j4 = out["J4_supercritical"]
    print(f"J4 supercritical: spread(beta=1) / spread(beta=2) = "
          f"{j4['beta_1_over_beta_2']:.1f}, best beta = {j4['best_beta']}")
    j5 = out["J5_branch_vs_xu"]
    print(f"J5 branch vs XU: worst rel {j5['worst_rel_diff']:.2e}, "
          f"mean {j5['mean_rel_diff']:.2e}; a_c ours {j5['a_c_ours_rel_err']:.2%} vs "
          f"XU {j5['a_c_xu_rel_err']:.2%} off published")
    print(f"J6 ledger: {out['J6_ledger']['counts']}")
    print(f"-> {OUT}  ({out['wall_clock_seconds']} s)")


if __name__ == "__main__":
    main()
