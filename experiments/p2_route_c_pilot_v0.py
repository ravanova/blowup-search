"""Route-C-PILOT v0: is the certificate-weight fitness safe to hand to a GA?

Stage C-PILOT asks one question and `plan_of_record.py` pre-commits both answers:

    Does the new fitness pass the six-property viability gate?
      yes -> proceed to stage B with the validated fitness.
      no  -> STOP. Do not run the GA. Stage 3.5 is the precedent and it is
             non-negotiable -- a fitness that fails the gate produces confident
             garbage at scale.

with a standing ban on ANY GA compute until the gate reports.  This file is the gate.
Everything it does is deterministic and the whole run is about a minute.

PRE-COMMITTED CLAUSES, written before the run (both branches of each are reportable):

  C0-1  THE NOVELTY CHECK COMES FIRST, as it did at leg 48.  `novelty_verdict()` is
        computed off `solver.weight_search.PRECEDENTS`.  PRE_EMPTED -> report and stop.
        PROCEED_NARROW -> proceed, and state the claim as narrowly as the ledger allows.
  C0-2  THE SUBSTRATE MUST HAVE A KNOWN ANSWER, and it must be checked, not asserted:
        the discrete Newton profile against the closed-form CLM profile, and the
        recovered gauge constants against their exact values.  Reported as magnitudes.
  C0-3  THE PREMISE OF THE STAGE IS ITSELF A CLAIM.  Leg 46 measured 5186x between the
        naive and hand-tuned weights on the HL object.  If that does not reproduce on
        the known-answer object, the stage is built on a one-object accident and the
        leg says so.
  C0-4  THE GATE, on the FROZEN predicate in `solver/weight_search.py` (thresholds
        committed before this run).  Its verdict decides whether the GA runs AT ALL.
  C0-5  THE SEARCH.  A DETERMINISTIC grid optimum -- not the GA, which stays banned
        until C0-4 reports -- against the two hand-picked weights.
  C0-6  THE WALLS.  The analytic upper wall p+q <= 1 comes from the profile's tail and
        was known before the run.  Whether anything ELSE bounds the search space is a
        measurement, and it is taken on the same slice at four resolutions.
  C0-7  THE CEILING.  Whatever this leg finds, it moves no link of the L1->L4 chain,
        and a fitness that works on CLM is not a certificate of anything.

Writes writeup/data/p2_route_c_pilot_v0.json.

Run: .venv/bin/python -u experiments/p2_route_c_pilot_v0.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.weight_search import (                                    # noqa: E402
    BOX_LOWER, BOX_UPPER, EXACT_C_OMEGA, GENE_NAMES, PRECEDENTS, SEARCH_LOG,
    WALL_POWER, BorderedCLM, FitnessEngine, defect_ladder, exact_hilbert,
    exact_profile, far_field_power, grid_search, hand_weights, interior_margin,
    lower_wall, novelty_verdict, roster, six_property_gate,
)

OUT = ROOT / "writeup" / "data" / "p2_route_c_pilot_v0.json"
N_COARSE, N_FINE = 201, 401
LADDER_N = (201, 401, 801, 1601, 3201)


def main():
    t0 = time.time()
    res = {"route": "C-PILOT", "version": "v0",
           "question": "Does the certificate-weight fitness pass the six-property "
                       "viability gate, on an object whose answer is known?"}

    # -- C0-1 the novelty check, before anything is built ------------------
    answer, note, _ = novelty_verdict()
    res["C0_1_novelty"] = {
        "verdict": answer, "note": note, "n_queries": len(SEARCH_LOG),
        "search_log": [{"query": q, "hits": h, "note": nt} for q, h, nt in SEARCH_LOG],
        "precedents": PRECEDENTS,
    }
    print(f"[C0-1] novelty: {answer} -- {note}")
    if answer == "PRE_EMPTED":
        res["verdict"] = "STOPPED_BY_NOVELTY_GATE"
        OUT.write_text(json.dumps(res, indent=1))
        return

    # -- C0-2 the substrate's known answers --------------------------------
    known = {"profile_distance": [], "c_omega_vs_reach": []}
    for n in (201, 401, 801):
        pr = BorderedCLM(n=n)
        z, info = pr.newton()
        Om = z[:pr.n]
        known["profile_distance"].append({
            "n": n, "newton_residual": float(info["residual_ladder"][-1]),
            "sup_distance_to_exact": float(np.abs(Om - exact_profile(pr.X)).max()),
            "hilbert_error": float(np.abs(pr.H @ exact_profile(pr.X)
                                          - exact_hilbert(pr.X)).max()),
            "c_l": float(z[pr.n]), "c_omega": float(z[pr.n + 1]),
            "newton_ladder": info["residual_ladder"].tolist()})
    for rho_max in (6.0, 8.0, 10.0):
        pr = BorderedCLM(n=401, rho_max=rho_max)
        z, _ = pr.newton()
        known["c_omega_vs_reach"].append({
            "rho_max": rho_max, "X_max": pr.Xmax, "c_omega": float(z[pr.n + 1]),
            "error_vs_exact": float(abs(z[pr.n + 1] - EXACT_C_OMEGA))})
    res["C0_2_known_answers"] = known
    d = known["profile_distance"]
    print(f"[C0-2] |Omega - Omega_0|_sup: " +
          " -> ".join(f"{r['sup_distance_to_exact']:.2e}" for r in d) +
          "   c_omega err vs reach: " +
          " -> ".join(f"{r['error_vs_exact']:.2e}" for r in known["c_omega_vs_reach"]))

    # -- C0-3 does leg 46's premise reproduce here? -------------------------
    pr = BorderedCLM(n=N_COARSE)
    z, _ = pr.newton()
    eng = FitnessEngine(pr, z)
    hw = hand_weights()
    f_naive, f_tuned = eng.fitness(hw["naive"]), eng.fitness(hw["tuned_leg46"])
    # the same comparison under the OTHER gauge: c_l pinned directly rather than
    # implied. The weight family is identical; only the border rows differ.
    stiff = _stiff_gauge_gain(N_COARSE)
    res["C0_3_premise"] = {
        "leg46_reported_gain_HL": 5186.6,
        "fitness_naive": f_naive, "fitness_tuned_leg46": f_tuned,
        "gain_implicit_gauge": float(10.0 ** (f_naive - f_tuned)),
        "gain_stiff_gauge": stiff["gain"],
        "stiff_gauge_naive": stiff["naive"], "stiff_gauge_tuned": stiff["tuned"],
        "reproduces": bool(10.0 ** (f_naive - f_tuned) > 1e3),
    }
    print(f"[C0-3] naive->tuned gain: {10.0 ** (f_naive - f_tuned):.1f}x "
          f"(leg 46 on HL: 5186.6x); under the stiff gauge: {stiff['gain']:.2f}x")

    # -- C0-4 THE GATE ------------------------------------------------------
    gate = six_property_gate(BorderedCLM(n=N_COARSE), BorderedCLM(n=N_FINE),
                             n_random=32, seed=0, per_gene=9, refine=4)
    res["C0_4_gate"] = gate
    print(f"[C0-4] GATE VERDICT: {gate['verdict']}")
    for k, v in gate["properties"].items():
        print(f"        {'PASS' if v['pass'] else 'FAIL'}  {k}: "
              + ", ".join(f"{a}={b}" for a, b in v.items() if a != "pass"))

    # the P3 diagnosis: the known answer (slope 1) only holds where the
    # linearisation does, and ||A|| says where that is
    rost = roster(pr, n_random=16, seed=0)
    th = np.array([t for _, t in rost])
    J = pr.jacobian(z)
    rng = np.random.default_rng(7)
    dvec = rng.standard_normal(pr.N)
    dvec /= np.abs(dvec).max()
    lin_check = []
    for e in (1e-2, 1e-4, 1e-6, 1e-8):
        v = np.linalg.inv(pr.jacobian(z + e * dvec)) @ pr.F(z + e * dvec)
        lin_check.append({"eps": e,
                          "rel_dev_from_eps_d": float(np.abs(v - e * dvec).max()
                                                      / (e * np.abs(dvec).max()))})
    _, tab_w, sl_w = defect_ladder(pr, z, th, eps=(1e-6, 1e-7, 1e-8, 1e-9))
    fin = np.isfinite(sl_w)
    res["C0_4_p3_diagnosis"] = {
        "A_norm_at_tuned": pr.certificate_constants(z, hw["tuned_leg46"])["A_norm"],
        "linearity_check": lin_check,
        "window": [1e-6, 1e-7, 1e-8, 1e-9],
        "median_abs_slope_error": float(np.median(np.abs(sl_w[fin] - 1.0))),
        "max_abs_slope_error": float(np.max(np.abs(sl_w[fin] - 1.0))),
        "monotone_violations": int(np.sum([not np.all(np.diff(tab_w[:, j]) < 0)
                                           for j in range(tab_w.shape[1])
                                           if np.all(np.isfinite(tab_w[:, j]))])),
    }
    print(f"[C0-4] P3 in the valid window (eps <= 1e-6): median |slope-1| = "
          f"{res['C0_4_p3_diagnosis']['median_abs_slope_error']:.4f}, "
          f"max = {res['C0_4_p3_diagnosis']['max_abs_slope_error']:.4f}")

    # -- C0-5 the deterministic search vs the hands ------------------------
    g = grid_search(eng, per_gene=9, box=True, refine=4)
    res["C0_5_search"] = {
        "method": "deterministic grid + 4 refinements (NOT the GA: banned until C0-4)",
        "gene_names": list(GENE_NAMES), "box_lower": BOX_LOWER.tolist(),
        "box_upper": BOX_UPPER.tolist(),
        "theta_star": g["theta"].tolist(), "fitness_star": g["fitness"],
        "evaluations": g["evaluations"],
        "fitness_naive": f_naive, "fitness_tuned_leg46": f_tuned,
        "gain_over_naive": float(10.0 ** (f_naive - g["fitness"])),
        "gain_over_tuned": float(10.0 ** (f_tuned - g["fitness"])),
        "interior_margin": interior_margin(g["theta"]),
        "far_field_power": far_field_power(g["theta"]),
        "constants": {lab: pr.certificate_constants(z, thv)
                      for lab, thv in (("naive", hw["naive"]),
                                       ("tuned_leg46", hw["tuned_leg46"]),
                                       ("searched", g["theta"]))},
        "ga_run": False,
        "ga_reason": "plan_of_record bans GA compute on a fitness that has not passed "
                     "the gate; C0-4 reports " + gate["verdict"],
    }
    print(f"[C0-5] searched weight {np.round(g['theta'], 3)} -> {g['fitness']:+.4f}; "
          f"{10.0 ** (f_naive - g['fitness']):.4g}x over naive, "
          f"{10.0 ** (f_tuned - g['fitness']):.3g}x over leg 46's hand constant")

    # -- C0-6 the walls -----------------------------------------------------
    walls = []
    for n in LADDER_N:
        prn = BorderedCLM(n=n)
        zn, infn = prn.newton()
        en = FitnessEngine(prn, zn)
        Y0, Z1, Z2 = en.constants_many(np.atleast_2d(hw["tuned_leg46"]))
        walls.append({
            "n": n, "X_max": prn.Xmax,
            "newton_residual": float(infn["residual_ladder"][-1]),
            "p_minus": lower_wall(en), "wall_power_analytic": WALL_POWER,
            "Z1_at_p0": float(en.constants_many(
                np.array([[0.0, 0.0, 0.0, 0.0, -2.0]]))[1][0]),
            "fitness_tuned": float(en.fitness(hw["tuned_leg46"])),
            "fitness_naive": float(en.fitness(hw["naive"])),
            "Y0_tuned": float(Y0[0]), "Z1_tuned": float(Z1[0]), "Z2_tuned": float(Z2[0]),
            "closes": bool(en.fitness(hw["tuned_leg46"]) < 0.0)})
        print(f"[C0-6] n={n:5d}: p_- = {walls[-1]['p_minus']:+.4f}, "
              f"Z1(p=0) = {walls[-1]['Z1_at_p0']:.3e}, "
              f"fitness(tuned) = {walls[-1]['fitness_tuned']:+.3f}"
              f"{'  CLOSES' if walls[-1]['closes'] else ''}")
    res["C0_6_walls"] = {"analytic_upper_wall": WALL_POWER,
                         "derivation": "|Omega_0| ~ |X|^-1, so nu ~ |X|^(p+q) gives the "
                                       "TRUE profile an infinite weighted sup norm for "
                                       "p+q > 1",
                         "ladder": walls}

    # censoring is explained by the lower wall, or it is not -- measured
    vc = np.array(gate["fitness_coarse"])
    thc = np.array(gate["theta"])
    cens = ~np.isfinite(vc)
    res["C0_6_censoring"] = {
        "censored": int(cens.sum()), "total": int(cens.size),
        "max_far_field_power_among_censored": float(np.max(thc[cens, 0] + thc[cens, 2]))
        if cens.any() else None,
        "min_far_field_power_among_finite": float(np.min(thc[~cens, 0] + thc[~cens, 2])),
        "p_minus_at_n201": walls[0]["p_minus"],
    }
    print(f"[C0-6] censored {cens.sum()}/{cens.size}; every censored weight has "
          f"p+q <= {res['C0_6_censoring']['max_far_field_power_among_censored']:.2f}")

    # -- C0-7 the ceiling ---------------------------------------------------
    res["C0_7_ceiling"] = (
        "No link of the L1->L4 chain moved. The object here is CLM, whose profile has "
        "been in closed form since 1985; nothing is certified by this leg and no "
        "novelty is claimed for the idea of searching a certificate (see C0-1).")
    res["verdict"] = gate["verdict"]
    res["elapsed_s"] = time.time() - t0
    OUT.write_text(json.dumps(res, indent=1))
    print(f"\nwrote {OUT}  ({res['elapsed_s']:.0f}s)  VERDICT: {res['verdict']}")


def _stiff_gauge_gain(n):
    """C0-3's control: the SAME weight family under a gauge that pins c_l directly.

    This is the ablation that says where the weight effect lives. If the gain survives
    the gauge change it is a property of the weight family; if it collapses it is a
    property of the border rows, and stage B would have been searching the wrong thing."""
    from solver.line_hilbert import line_hilbert_matrix, slope_matrix
    from solver.hl_rescaled import sinh_grid_origin
    from solver.target_selection import y0_budget

    rho, X = sinh_grid_origin(n, c=0.5, rho_max=8.0)
    H, D = line_hilbert_matrix(X), slope_matrix(X)
    m, i0 = X.size, X.size // 2
    N, XD = m + 2, X[:, None] * D
    Om0 = exact_profile(X)

    def F(z):
        Om, c_l, c_om = z[:m], z[m], z[m + 1]
        return np.concatenate([(c_om + H @ Om) * Om - c_l * (XD @ Om),
                               [c_l - 1.0, D[i0] @ Om - (-4.0)]])

    def Jac(z):
        Om, c_l, c_om = z[:m], z[m], z[m + 1]
        J = np.zeros((N, N))
        J[:m, :m] = np.diag(c_om + H @ Om) + Om[:, None] * H - c_l * XD
        J[:m, m] = -(XD @ Om)
        J[:m, m + 1] = Om
        J[m, m] = 1.0
        J[m + 1, :m] = D[i0]
        return J

    z = np.concatenate([Om0, [1.0, -1.0]])
    for _ in range(12):
        z = z + np.linalg.solve(Jac(z), -F(z))
        if np.abs(F(z)).max() < 1e-14:
            break
    J, Fz = Jac(z), F(z)
    A = np.linalg.inv(J)
    out = {}
    for lab, wl in (("naive", X.max()), ("tuned", 0.01 * X.max())):
        w = np.concatenate([np.ones(m), [wl, 1.0]])
        Y0 = float(np.max(w * np.abs(A @ Fz)))
        Z1 = float(np.max(w * (np.abs(np.eye(N) - A @ J) @ (1.0 / w))))
        A_n = float(np.max(w * (np.abs(A) @ (1.0 / w))))
        B = float(np.max(np.abs(H) @ np.ones(m))) + 1.0 + \
            float(np.max(np.abs(XD) @ np.ones(m))) / wl
        Z2 = 2.0 * A_n * B
        out[lab] = float(np.log10(Y0 / y0_budget(Z1, Z2)))
    out["gain"] = float(10.0 ** (out["naive"] - out["tuned"]))
    return out


if __name__ == "__main__":
    main()
