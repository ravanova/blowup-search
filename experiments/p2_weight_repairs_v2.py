"""Weight-repairs v2 (leg 59, Route-WV): the wall is 2-D, and the FROZEN gate re-run.

WHERE THIS STARTS
-----------------------------------------------------------------------------
Stage B is blocked because C-PILOT's six-property viability gate answered FAIL 4/6
(leg 49) and leg 50's two named repairs moved it without passing: P2 finite fraction
0.775 -> 0.875 against a 0.90 floor, P3 worst |slope-1| 0.366 -> 0.342 against 0.05.
P2's own gate note names the suspect: the measured wall is a 1-D SLICE of what is
actually a 2-D boundary, so admissible weights are being scored against the wrong
geometry.

WHAT THIS LEG CHANGES, AND WHAT IT MAY NOT
-----------------------------------------------------------------------------
Changed: the MODEL of the conditioning wall. `lower_wall()` bisects Z_1 = 1 on a
single-factor slice and `in_box` then applies that crossing to the SUM p+q, i.e. it
assumes a half-plane. In this float rehearsal M = I - A DF is roundoff, so
Z_1 ~ eps * kappa * (max_i w_i / min_j w_j) -- the weight's DYNAMIC RANGE, which two
weights with equal p+q do not share once the two algebraic factors have different
scales. `TwoFactorWall` carries the level set of that range instead.

NOT changed: the thresholds, the roster construction, the resolutions (n=201/401),
the search settings (per_gene=9, refine=4), the seed. The gate is frozen. Repairing
the fitness is allowed; moving the goalposts is not. The wall's ONE number is
inherited from the same bisection leg 49 ran -- r_crit is the log-range at that
crossing -- so nothing here is fitted to this run's own data.

THREE MEASUREMENTS, IN ORDER
-----------------------------------------------------------------------------
  A  KNOWN ANSWER. Re-derive the analytic wall's growth rate in the 2-D geometry and
     check it against the exact CLM profile. The 1-D window is pre-committed: the
     1-D law predicted x7.39 and measured x7.39 over a 54.6x reach, so the 2-D law
     must reproduce that number on the 1-D slice, and must beat it where the two
     factors carry opposite-sign powers and the sup goes interior.
  B  DISAGREEMENT. How much of the observed Z_1 >= 1 failure set does each wall model
     explain, on the same draw of in-box weights?
  C  THE FROZEN GATE, re-run with the 2-D wall carried in the box.

NO GA COMPUTE RUNS HERE, on either branch of the gate. That ban lifts only on a gate
that PASSES, and lifting it is the user's call, not this leg's.

CEILING (carried, and it is not optional): leg 54 measured the shape of A dead on top
of leg 53's split and leg 52's space, so even a PASS here would unblock a stage whose
three degrees of freedom are separately measured worthless for this operator. Passing
the gate is worth knowing; it is not a route.

Writes writeup/data/p2_weight_repairs_v2.json.
Run: .venv/bin/python -u experiments/p2_weight_repairs_v2.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.weight_search import (                                    # noqa: E402
    BorderedCLM, FitnessEngine, WALL_LOWER_DELTA, WALL_RANGE_DELTA, exact_profile,
    log_range_analytic, lower_wall, six_property_gate, two_factor_wall,
    weight_log_range, weighted_sup_analytic, wall_model_disagreement,
)

OUT = ROOT / "writeup" / "data" / "p2_weight_repairs_v2.json"
V1_JSON = ROOT / "writeup" / "data" / "p2_weight_repairs_v1.json"
N_COARSE, N_FINE = 201, 401

# The known-answer battery. The first row is the 1-D slice whose answer is already
# banked (x7.39 predicted, x7.39 measured, capabilities.py); the rest are genuinely
# two-factor, and the last two are the interior-dominated ones the 1-D law cannot see.
GROWTH_CASES = [
    ("slice_1d", (1.5, 0.0, 0.0, 0.0)),
    ("two_factor_same_sign", (0.75, np.log10(2.0), 0.75, np.log10(0.5))),
    ("two_factor_split", (2.0, 0.0, -0.5, 1.0)),
    ("interior_dominated_a", (-1.0, -1.0, 2.5, np.log10(3.0))),
    ("interior_dominated_b", (3.0, np.log10(5.0), -1.5, np.log10(0.2))),
]


def measured_sup(theta, Xmax, n=200001):
    """sup nu |Omega_0| on a dense log grid -- the measurement the analytic law is
    checked against (the exact profile, so every defect here is the LAW's)."""
    X = np.logspace(-6.0, np.log10(Xmax), n)
    p, logL, q, logl = (float(t) for t in theta[:4])
    nu = ((1.0 + (X / 10.0 ** logL) ** 2) ** (0.5 * p)
          * (1.0 + (X / 10.0 ** logl) ** 2) ** (0.5 * q))
    return float(np.max(nu * np.abs(exact_profile(X))))


def measurement_a(res):
    """A -- the analytic growth rate in the 2-D geometry, against a known answer."""
    Xa = BorderedCLM(n=201, rho_max=6.0).Xmax
    Xb = BorderedCLM(n=201, rho_max=10.0).Xmax
    reach = Xb / Xa
    rows = []
    for name, th in GROWTH_CASES:
        m = measured_sup(th, Xb) / measured_sup(th, Xa)
        a2 = weighted_sup_analytic(th, Xb) / weighted_sup_analytic(th, Xa)
        a1 = reach ** (th[0] + th[2] - 1.0)
        rows.append({"case": name, "theta4": list(th), "far_field_power": th[0] + th[2],
                     "measured_growth": m, "predicted_2d": a2, "predicted_1d": a1,
                     "rel_err_2d": abs(m / a2 - 1.0),
                     "rel_err_1d": abs(m / a1 - 1.0),
                     "factor_1d_law_is_off": max(a1 / m, m / a1)})
        print(f"  {name:22s} p+q={th[0]+th[2]:+.2f}  measured x{m:.4f}  "
              f"2-D law x{a2:.4f} (rel {abs(m/a2-1):.1e})  "
              f"1-D law x{a1:.4f} (off {max(a1/m, m/a1):.2f}x)")
    res["A_growth_law"] = {
        "reach": reach, "X_max_small": Xa, "X_max_large": Xb,
        "window": ("PRE-COMMITTED: on the 1-D slice the banked answer is x7.39 "
                   "predicted and x7.39 measured (capabilities.py, leg 49)"),
        "cases": rows,
        "worst_rel_err_2d": max(r["rel_err_2d"] for r in rows),
        "worst_factor_1d_off": max(r["factor_1d_law_is_off"] for r in rows),
    }
    return res


def measurement_b(res, eng, wall, lw):
    """B -- what each wall model explains of the Z_1 >= 1 failure set."""
    dis = wall_model_disagreement(eng, wall, n=400, seed=11, lower_wall_power=lw)
    slim = {k: dis[k] for k in ("n", "n_fail", "wall_1d", "wall_2d")}
    slim["ratio_misclassified_1d_over_2d"] = (
        dis["wall_1d"]["misclassified"] / max(dis["wall_2d"]["misclassified"], 1))
    res["B_wall_disagreement"] = slim
    res["B_wall_disagreement_raw"] = {
        "far_field_power": dis["far_field_power"], "log_range": dis["log_range"],
        "Z1": dis["Z1"], "fails": dis["fails"]}
    print(f"  draw of {dis['n']} in-box weights, {dis['n_fail']} with Z_1 >= 1")
    for k in ("wall_1d", "wall_2d"):
        d = dis[k]
        print(f"  {k}: admits {d['admitted']}, of which {d['admitted_but_failing']} "
              f"fail ({100*d['failure_rate_among_admitted']:.1f}%); "
              f"excludes {d['excluded_but_fine']} that are fine; "
              f"{d['misclassified']} misclassified")
    return res


def main():
    t0 = time.time()
    res = {"route": "weight-repairs (Route-WV)", "version": "v2",
           "question": ("With a 2-D wall model, does the FROZEN six-property "
                        "viability gate pass 6/6 -- in particular P2 >= 0.90 and "
                        "P3 max |slope-1| <= 0.05?"),
           "frozen": ("thresholds, roster construction, resolutions (201/401), "
                      "seed 0, per_gene 9, refine 4 -- all unchanged from leg 49/50. "
                      "Only the wall MODEL changed."),
           "wall_constants": {"WALL_LOWER_DELTA": WALL_LOWER_DELTA,
                              "WALL_RANGE_DELTA": WALL_RANGE_DELTA,
                              "calibration": ("r_crit is the log-range AT the 1-D "
                                              "wall's own bisected crossing -- "
                                              "inherited, not refitted")}}

    print("[A] the analytic growth rate, re-derived in the 2-D geometry")
    res = measurement_a(res)

    pr_c = BorderedCLM(n=N_COARSE)
    z_c, _ = pr_c.newton()
    eng_c = FitnessEngine(pr_c, z_c)
    lw = lower_wall(eng_c)
    wall = two_factor_wall(eng_c)
    # the geometry check: the closed-form range against the range the grid actually
    # carries, over the box -- a known-answer test of `log_range_analytic`
    rng = np.random.default_rng(3)
    from solver.weight_search import BOX_LOWER, BOX_UPPER
    errs = []
    for _ in range(300):
        th = BOX_LOWER + rng.random(5) * (BOX_UPPER - BOX_LOWER)
        errs.append(abs(log_range_analytic(pr_c, th) - weight_log_range(pr_c, th)))
    res["wall_2d"] = {"p_minus_1d": wall.p_minus, "r_crit": wall.r_crit,
                      "log_range_analytic_vs_measured_max_decades": float(max(errs)),
                      "note": ("the residual is grid discreteness -- the interior "
                               "stationary point falls between grid points")}
    print(f"\n[wall] 1-D crossing p_- = {wall.p_minus:+.4f}  ->  r_crit = "
          f"{wall.r_crit:.4f} decades of weight range; closed-form range agrees with "
          f"the grid's to {max(errs):.3f} decades")

    print("\n[B] what each wall model explains of the Z_1 >= 1 failure set")
    res = measurement_b(res, eng_c, wall, lw)

    print("\n[C] the FROZEN six-property gate, re-run with the 2-D wall")
    v1 = json.loads(V1_JSON.read_text()) if V1_JSON.exists() else None
    if v1 is not None:
        res["before"] = {"source": str(V1_JSON.relative_to(ROOT)),
                         "verdict": v1["after"]["verdict"],
                         "properties": v1["after"]["gate"]["properties"]}
    gate = six_property_gate(BorderedCLM(n=N_COARSE), BorderedCLM(n=N_FINE),
                             n_random=32, seed=0, per_gene=9, refine=4,
                             wall_model="2d")
    res["after"] = {"verdict": gate["verdict"], "gate": gate}
    n_pass_after = int(sum(1 for v in gate["properties"].values() if v["pass"]))
    print(f"  verdict {gate['verdict']}  ({n_pass_after}/6)")
    for k, v in gate["properties"].items():
        print(f"    {'PASS' if v['pass'] else 'FAIL'}  {k}: "
              + ", ".join(f"{a}={b}" for a, b in v.items()
                          if a not in ("pass", "wall_model")))

    if v1 is not None:
        bp = v1["after"]["gate"]["properties"]
        ap = gate["properties"]
        n_pass_before = int(sum(1 for v in bp.values() if v["pass"]))
        res["delta"] = {
            "P2_finite_fraction": {"leg49": 0.775,
                                   "leg50_1d_wall": bp["P2_finite"]["finite_fraction"],
                                   "leg59_2d_wall": ap["P2_finite"]["finite_fraction"],
                                   "threshold": ap["P2_finite"]["threshold"]},
            "P3_max_slope_error": {"leg49": 0.3656058258949979,
                                   "leg50_1d_wall": bp["P3_monotone"]["max_slope_error"],
                                   "leg59_2d_wall": ap["P3_monotone"]["max_slope_error"],
                                   "threshold": 0.05},
            "P3_violations": {"leg50_1d_wall": bp["P3_monotone"]["violations"],
                              "leg59_2d_wall": ap["P3_monotone"]["violations"]},
            "P3_n_unresolved": {"leg50_1d_wall": bp["P3_monotone"]["n_unresolved"],
                                "leg59_2d_wall": ap["P3_monotone"]["n_unresolved"]},
            "n_pass": {"leg49": 4, "leg50_1d_wall": n_pass_before,
                       "leg59_2d_wall": n_pass_after},
        }
        d = res["delta"]
        print(f"\n[delta] P2 {d['P2_finite_fraction']['leg50_1d_wall']:.3f} -> "
              f"{d['P2_finite_fraction']['leg59_2d_wall']:.3f} (floor 0.90); "
              f"P3 worst |slope-1| {d['P3_max_slope_error']['leg50_1d_wall']:.3f} -> "
              f"{d['P3_max_slope_error']['leg59_2d_wall']:.3f} (floor 0.05); "
              f"gate {n_pass_before}/6 -> {n_pass_after}/6")

    # which weights still fail, and who carries the residual -- the substantive
    # question the FAIL branch has to answer
    labels = gate["labels"]
    vc = np.array(gate["fitness_coarse"])
    slopes = np.array(gate["defect_ladder"]["slopes"], dtype=float)
    infinite = [labels[i] for i in np.where(~np.isfinite(vc))[0]]
    resolved = [(labels[i], float(slopes[i])) for i in range(len(labels))
                if np.isfinite(slopes[i])]
    worst = sorted(resolved, key=lambda kv: -abs(kv[1] - 1.0))[:6]
    hand = [k for k, _ in worst if not k.startswith("rand_")]
    res["residual"] = {
        "infinite_fitness_labels": infinite,
        "worst_slope_weights": [{"label": k, "slope": v,
                                 "slope_error": abs(v - 1.0)} for k, v in worst],
        "worst_slope_is_hand_weight": bool(worst and not worst[0][0].startswith("rand_")),
        "hand_weights_among_worst_six": hand,
        "note": ("control and degenerate weights are part of the FROZEN roster and no "
                 "wall model can remove them -- if they carry the residual P3 error, "
                 "the defect is in the fitness's definition, not in its box"),
    }
    print(f"\n[residual] infinite-fitness weights: {infinite or 'none'}")
    print("[residual] worst |slope-1|: " + ", ".join(
        f"{k} {abs(v-1.0):.3f}" for k, v in worst))

    # -- D: WHAT CARRIES THE RESIDUAL. A DIAGNOSIS, NOT A REPAIR --------------------
    # The gate above is frozen and this measurement changes nothing in it. P3's probe
    # gives every weight an upper limit on eps (C / ||A||_w, leg 50's repair) and NO
    # lower limit. But Y_0(eps) = max_i w_i |A F(z*+eps d)|_i stops tracking eps once
    # the perturbation drops under the roundoff already in A F(z*):
    #
    #     eps_min(w) = Y_0(z*, w) / max_i w_i |d_i|,
    #
    # so each weight's probe has a WINDOW, [eps_min, eps_max], and the decade grid
    # puts points below its floor. This measures whether the fitted slope is a
    # function of that window's width rather than of the weight.
    print("\n[D] what carries P3's residual -- the probe's window, measured")
    th_r = np.array(gate["theta"])
    resn = gate["defect_ladder"]["resolution"]
    slopes_r = np.array(gate["defect_ladder"]["slopes"], dtype=float)
    rng2 = np.random.default_rng(7)
    dvec = rng2.standard_normal(pr_c.N)
    dvec /= np.abs(dvec).max()
    AF = np.abs(eng_c.A @ pr_c.F(z_c))
    rows = []
    for i, lab in enumerate(labels):
        if not resn[i]["resolved"] or not np.isfinite(slopes_r[i]):
            continue
        w, _ = pr_c.weight_vector(th_r[i])
        eps_min = float(np.max(w * AF) / np.max(w * np.abs(dvec)))
        width = float(np.log10(resn[i]["eps_max"] / eps_min))
        rows.append({"label": lab, "eps_min_noise_floor": eps_min,
                     "eps_max_linearity": resn[i]["eps_max"],
                     "window_width_decades": width, "slope": float(slopes_r[i]),
                     "slope_error": abs(float(slopes_r[i]) - 1.0)})
    width_v = np.array([r["window_width_decades"] for r in rows])
    err_v = np.array([r["slope_error"] for r in rows])
    order_w = np.argsort(np.argsort(width_v)).astype(float)
    order_e = np.argsort(np.argsort(err_v)).astype(float)
    order_w -= order_w.mean()
    order_e -= order_e.mean()
    rho = float(order_w @ order_e
                / np.sqrt((order_w @ order_w) * (order_e @ order_e)))
    passing = width_v[err_v <= 0.05]
    failing = width_v[err_v > 0.05]
    res["D_probe_window"] = {
        "rows": rows,
        "spearman_width_vs_slope_error": rho,
        "narrowest_window_meeting_P3": float(passing.min()) if passing.size else None,
        "widest_window_failing_P3": float(failing.max()) if failing.size else None,
        "worst_slope_error": float(err_v.max()),
        "worst_window_decades": float(width_v[np.argmax(err_v)]),
        "n_weights": len(rows),
        "reading": ("the fitted slope is a function of the probe WINDOW's width, not "
                    "of the weight: `defect_ladder` bounds eps above (leg 50's "
                    "repair) and not below, so weights whose window is narrow are "
                    "probed under their own noise floor. This is a defect in the "
                    "FITNESS's definition, not in the box the wall model draws -- "
                    "which is exactly what the gate's no-branch says a future B "
                    "proposal has to change. NOT applied to the gate above; the gate "
                    "is frozen."),
    }
    print(f"  Spearman(window width, |slope-1|) = {rho:+.3f} over {len(rows)} "
          f"resolved weights")
    print(f"  worst |slope-1| {err_v.max():.3f} at a "
          f"{width_v[np.argmax(err_v)]:.2f}-decade window; the narrowest window that "
          f"meets P3 is {passing.min() if passing.size else float('nan'):.2f} decades, "
          f"the widest that fails it "
          f"{failing.max() if failing.size else float('nan'):.2f}")

    res["ga_run"] = False
    res["ga_reason"] = ("plan_of_record bans GA compute on an unvalidated fitness, on "
                        "EITHER branch of this gate. The ban lifts only on a PASS, and "
                        "lifting it is the user's call, not this leg's.")
    res["ceiling"] = ("No link of the L1->L4 chain moved. This is a gate result on a "
                      "fitness measured in FLOAT on the a=0 CLM linearisation (closed "
                      "form since CLM 1985) -- not a certificate, and not a statement "
                      "about Hou-Luo. Leg 54 measured the shape of A on top of leg "
                      "53's split and leg 52's space, so even a PASS would unblock a "
                      "stage whose three degrees of freedom are separately measured "
                      "worthless for this operator.")
    res["elapsed_s"] = time.time() - t0
    OUT.write_text(json.dumps(res, indent=1))
    print(f"\nwrote {OUT}  ({res['elapsed_s']:.0f}s)")


if __name__ == "__main__":
    main()
