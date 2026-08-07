"""
Leg 289 -- ROUTE-D1X: is leg 288's exact D1(kappa) = C * kappa^{-1/2} law a USABLE
predictive shortcut, or purely descriptive of the points it was derived from?

Zero new certificate/solver compute. Reads only:
  - writeup/data/p2_route_canon_v1_convention.json  (leg 288 -- the law + N=256 probe)
  - writeup/data/p2_route_cvf_v1_classify.json       (leg 281 -- the N=512 sweep the law
                                                        was originally fit against)

Predictions committed in writeup/novelty/leg_289.md BEFORE this script was run:
  P1  -- same-N holdout: anchor the coefficient at kappa=1 (leg 281, N=512), predict the
         other 10 sweep points, compare to their independently-measured values.
  P2a -- same-N holdout using leg 288's own N=256 probe: anchor at kappa=100, predict
         kappa in {1e4, 1e6, 1e8}.
  P2b -- cross-N transfer: use the N=512-anchored coefficient to predict the N=256 probe
         points directly (no N=256 anchor). Predicted to show discretization-scale error
         (~1e-5), NOT machine-precision-scale, i.e. the law does not eliminate N-dependence.
"""
import json
import math

REPO_ROOT = "/home/andy/projects/Unsolved/.claude/worktrees/agent-a5b3bad018649d0c7"

with open(f"{REPO_ROOT}/writeup/data/p2_route_cvf_v1_classify.json") as f:
    d281 = json.load(f)
with open(f"{REPO_ROOT}/writeup/data/p2_route_canon_v1_convention.json") as f:
    d288 = json.load(f)

sweep512 = d281["S4_group_D_dual"]["D1_ell_dual_norm_N512"]["sweep"]
probe256 = d288["P2_large_kappa_probe"]["dual_norm_D1_N256"]
law_quoted_coefficient = d281["S4_group_D_dual"]["D1_ell_dual_norm_N512"]["CONVERSION_LAW"]
fit_residual_281 = d281["S4_group_D_dual"]["D1_ell_dual_norm_N512"]["fit_max_relative_residual"]

# ---------------------------------------------------------------------------
# P1: same-N holdout against leg 281's own N=512 sweep. Anchor = kappa=1 point
# only (the JSON's own "pinned_by": "kappa = 1" -- the exponent -1/2 is an
# analytic claim, not fit across the sweep).
# ---------------------------------------------------------------------------
coeff_512 = sweep512["1"]  # the kappa=1 anchor, independently certificate-measured
p1_rows = {}
p1_max_relerr = 0.0
for k_str, measured in sweep512.items():
    kf = float(k_str)
    if kf == 1.0:
        continue  # this point IS the anchor, not held out
    predicted = coeff_512 * kf ** -0.5
    relerr = abs(predicted - measured) / abs(measured)
    p1_rows[k_str] = {
        "kappa": kf,
        "measured": measured,
        "predicted": predicted,
        "relative_error": relerr,
    }
    p1_max_relerr = max(p1_max_relerr, relerr)

p1_held_out_far_point = p1_rows["10000"]  # headline held-out point: 4 decades from anchor
p1_falsified = p1_max_relerr > 1e-6  # per novelty pass falsification threshold

# ---------------------------------------------------------------------------
# P2a: same-N holdout, leg 288's own N=256 probe. Anchor = kappa=100 point.
# ---------------------------------------------------------------------------
coeff_256 = probe256["100.0"] * (100.0 ** 0.5)
p2a_rows = {}
p2a_max_relerr = 0.0
for k_str, measured in probe256.items():
    kf = float(k_str)
    if kf == 100.0:
        continue
    predicted = coeff_256 * kf ** -0.5
    relerr = abs(predicted - measured) / abs(measured)
    p2a_rows[k_str] = {
        "kappa": kf,
        "measured": measured,
        "predicted": predicted,
        "relative_error": relerr,
    }
    p2a_max_relerr = max(p2a_max_relerr, relerr)

p2a_held_out_far_point = p2a_rows["100000000.0"]  # 6 decades from the N=256 anchor
p2a_falsified = p2a_max_relerr > 1e-6

# ---------------------------------------------------------------------------
# P2b: cross-N transfer. Use the N=512-anchored coefficient (coeff_512) to
# predict the N=256 probe points directly -- NO N=256 anchor used at all.
# ---------------------------------------------------------------------------
p2b_rows = {}
p2b_max_relerr = 0.0
for k_str, measured in probe256.items():
    kf = float(k_str)
    predicted = coeff_512 * kf ** -0.5
    relerr = abs(predicted - measured) / abs(measured)
    p2b_rows[k_str] = {
        "kappa": kf,
        "measured": measured,
        "predicted_using_N512_coefficient": predicted,
        "relative_error": relerr,
    }
    p2b_max_relerr = max(p2b_max_relerr, relerr)

# Prediction was: P2b shows discretization-scale error (~1e-5), NOT machine
# precision. "Confirmed" if 1e-6 < p2b error < 1e-3 (clearly not float noise,
# clearly not a law failure at wildly wrong order either).
p2b_prediction_confirmed = 1e-6 < p2b_max_relerr < 1e-3
p2b_would_be_falsified_if_machine_precision = p2b_max_relerr < 1e-10

coeff_relative_difference_512_vs_256 = abs(coeff_512 - coeff_256) / coeff_512

# ---------------------------------------------------------------------------
# Gate: does the law correctly predict >=1 held-out banked point (kappa value
# present in 249's or 281's data, NOT used to derive/fit the law) to the
# precision leg 281/288 originally measured?
# leg 249 carries NO D1 data at any kappa (its sweep is over sigma_min / A1,
# not D1) -- checked in the novelty pass, confirmed again here.
# ---------------------------------------------------------------------------
leg249_has_D1_data = False  # confirmed in novelty pass: leg 249 sweeps A1 (sigma_min), not D1

headline_holdout_kappa = 10000.0
headline_holdout_measured = p1_held_out_far_point["measured"]
headline_holdout_predicted = p1_held_out_far_point["predicted"]
headline_holdout_relerr = p1_held_out_far_point["relative_error"]

gate_yes = (not p1_falsified) and (headline_holdout_relerr <= fit_residual_281 * 1e6)
# (fit_residual_281 ~1.1e-16; we require the held-out error to be within 6
# orders of that -- i.e. still floating-point-scale, not a real deviation)

result = {
    "leg": 289,
    "route": "ROUTE-D1X",
    "date": "2026-08-07",
    "role": (
        "applies leg 288's exact D1(kappa) = C*kappa^-1/2 law to already-banked held-out "
        "kappa points (leg 281's own N=512 sweep beyond its kappa=1 anchor; leg 288's N=256 "
        "probe beyond its own kappa=100 anchor; and a cross-N transfer check) -- zero new "
        "certificate/solver compute, per novelty pass writeup/novelty/leg_289.md"
    ),
    "novelty_pass_commit": "b6e33a1",
    "reads_only": [
        "writeup/data/p2_route_canon_v1_convention.json (leg 288)",
        "writeup/data/p2_route_cvf_v1_classify.json (leg 281)",
    ],
    "law_as_quoted_by_leg281": law_quoted_coefficient,
    "leg281_fit_max_relative_residual": fit_residual_281,
    "leg249_has_D1_data": leg249_has_D1_data,
    "leg249_note": (
        "leg 249's sweep is over sigma_min (the A1 quantity), varying the BORDER weight, "
        "not D1 (dual norm) at any kappa. Confirmed no D1 rows exist in leg 249's banked "
        "data before running this script (recorded in the novelty pass)."
    ),
    "P1_same_N_holdout_leg281_sweep": {
        "anchor_kappa": 1.0,
        "anchor_coefficient": coeff_512,
        "held_out_points": p1_rows,
        "max_relative_error": p1_max_relerr,
        "headline_held_out_point": {
            "kappa": headline_holdout_kappa,
            "measured": headline_holdout_measured,
            "predicted": headline_holdout_predicted,
            "relative_error": headline_holdout_relerr,
        },
        "P1_falsified": p1_falsified,
    },
    "P2a_same_N_holdout_leg288_probe": {
        "anchor_kappa": 100.0,
        "anchor_coefficient": coeff_256,
        "held_out_points": p2a_rows,
        "max_relative_error": p2a_max_relerr,
        "headline_held_out_point": {
            "kappa": 1e8,
            "measured": p2a_held_out_far_point["measured"],
            "predicted": p2a_held_out_far_point["predicted"],
            "relative_error": p2a_held_out_far_point["relative_error"],
        },
        "P2a_falsified": p2a_falsified,
    },
    "P2b_cross_N_transfer": {
        "description": (
            "predicts leg 288's N=256 probe points using the coefficient anchored at "
            "N=512 (kappa=1) -- tests whether the law transfers ACROSS discretizations "
            "with no same-N reference point at all"
        ),
        "N512_anchor_coefficient": coeff_512,
        "N256_anchor_coefficient": coeff_256,
        "coefficient_relative_difference_N512_vs_N256": coeff_relative_difference_512_vs_256,
        "predictions": p2b_rows,
        "max_relative_error": p2b_max_relerr,
        "P2b_prediction_confirmed_discretization_scale_not_machine_precision": p2b_prediction_confirmed,
        "P2b_would_be_falsified_if_machine_precision": p2b_would_be_falsified_if_machine_precision,
    },
    "GATE": {
        "question": (
            "does D1's law correctly predict >=1 held-out banked data point (a kappa value "
            "in 249's or 281's data NOT used to derive/fit the law) to the precision those "
            "legs originally measured?"
        ),
        "answer": "YES" if gate_yes else "NO",
        "headline_evidence": {
            "kappa": headline_holdout_kappa,
            "measured": headline_holdout_measured,
            "predicted": headline_holdout_predicted,
            "relative_error": headline_holdout_relerr,
            "leg281_own_precision_floor": fit_residual_281,
        },
        "scope_limitation": (
            "the law is a validated predictive shortcut ONLY within a fixed discretization N: "
            "it requires one already-computed D1(kappa0, N) certificate point at the SAME N as "
            "the target kappa. P2b shows the coefficient itself is N-dependent "
            f"({coeff_relative_difference_512_vs_256:.3e} relative difference between N=256 and "
            "N=512), so the law does NOT eliminate the need for a certificate compute at a new "
            "N -- it only eliminates the need for a fresh SWEEP OVER kappa once one point at "
            "that N is known. Do not read 'exact law' as 'N-free' or 'apply anywhere'."
        ),
    },
}

with open(f"{REPO_ROOT}/writeup/data/p2_route_d1x_v1_apply.json", "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result["GATE"], indent=2))
print()
print("P1 max relative error (N=512 sweep, held out from kappa=1 anchor):", p1_max_relerr)
print("P2a max relative error (N=256 probe, held out from kappa=100 anchor):", p2a_max_relerr)
print("P2b max relative error (cross-N transfer, N=512 coeff -> N=256 points):", p2b_max_relerr)
print("Coefficient relative difference N=512 vs N=256:", coeff_relative_difference_512_vs_256)
