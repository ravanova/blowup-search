"""Arc-6 U5 evidence: rebuild every number in leg 421's prose from the artefact.

    .venv/bin/python writeup/arc6_w4_port_evidence.py

Checks, without re-running the experiment:
  * the pre-registration banked in the artefact is the one committed at 4688459;
  * W4's break clause (a) is quoted VERBATIM in the artefact and matches WALLS.md;
  * the gate is evaluated by the pre-committed rule from the banked numbers;
  * the log verdict is derived from the INCREMENTS, not from a power exponent —
    and the check fails if a power exponent alone is what decided it;
  * M6's UNDER-RESOURCED status is banked and the conclusion is not drawn from it;
  * every number quoted in the journal is in the JSON.

Exit 0 = no drift. Exit 1 = a prose number, or a scoring rule, left its source.

DELIBERATELY NOT DONE HERE: re-running the port. A script that re-runs the
experiment it checks cannot disagree with it — CORRECTIONS.md §54.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON = ROOT / "writeup" / "data" / "arc6_w4_port_v1.json"
JOURNAL = ROOT / "experiments" / "journal" / "leg_421.md"
PREREG = ROOT / "experiments" / "journal" / "leg_421_prereg.md"
WALLS = ROOT / "WALLS.md"

fail = []
def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok:
        fail.append(label)

d = json.loads(JSON.read_text())
j = re.sub(r"\s+", " ", JOURNAL.read_text())
pr = re.sub(r"\s+", " ", PREREG.read_text())
walls = re.sub(r"\s+", " ", WALLS.read_text())
P = d["prereg"]

print("== 1. the pre-registration, and W4's own text")
check(P["commit"] == "4688459", "prereg commit banked", P["commit"])
check(P["expected_gate_answer"] == "NO", "the expected answer was recorded IN ADVANCE")
check(P["M1_core_exponent"] == -1.5 and P["M1_tol"] == 0.05, "M1 prediction and tolerance")
check(P["M4_delta"].startswith("MEASURED"), "M4 carried NO prediction, by design")
check(P["max_spread_allowed"] == 0.025, "spread limit 0.025")
clause = d["W4_break_clause_a_verbatim"]
check(clause.startswith("(a) a localisation argument"), "clause (a) banked verbatim")
check(re.sub(r"\s+", " ", clause) in walls,
      "and the banked clause is a SUBSTRING OF WALLS.md — not a paraphrase")
check("A LOG IS FLAGGED IN ADVANCE" in pr, "the prereg flagged a log in advance")
check("are run and reported whatever" in pr and "says" in pr,
      "the prereg forbade stopping at M1")

print("== 2. M1 — why (a3) fails on route 4's own object")
m1 = d["M1_core"]
check(abs(m1["reported_exponent"] + 1.5) < 1e-6, "M1 exponent is -1.500000",
      f"{m1['reported_exponent']:.6f}")
check(m1["abs_error"] < 1e-6, "|err| against the pre-committed -1.5 is 0.000000")
check(m1["spread_across_rho"] < P["max_spread_allowed"], "spread inside the limit",
      f"{m1['spread_across_rho']:.2e}")
check(m1["spread_across_rho"] < 1e-6, "and it is 3.47e-07")
check(m1["inside_tolerance"] is True, "M1 inside tolerance")
check("−1.500000" in j and "3.47e-07" in j, "the journal quotes both")

print("== 3. M2 — (a1) is judged on the LADDER, not on a power exponent")
m2 = d["M2_energy"]
cls = m2["classification"]
check(cls["verdict"].startswith("CONVERGENT"), "energy ladder classified CONVERGENT",
      cls["verdict"])
inc = cls["per_decade_increment"]
check(all(inc[i + 1] < inc[i] for i in range(len(inc) - 1)),
      "its increments fall monotonically")
check(all(0.25 < r < 0.4 for r in cls["increment_ratios"]),
      "geometrically, by a factor ~0.31 each decade",
      str([round(r, 4) for r in cls["increment_ratios"]]))
check(abs(m2["exponent"]) < 0.01,
      "the POWER exponent is -0.0008 — which alone would not distinguish this from a log")
check(d["gate"]["clause_a1_bounded_energy"] is True, "(a1) TRUE")
check("judged on the LADDER" in d["gate"]["clause_a1_note"],
      "and the artefact says the verdict came from the ladder")

print("== 4. THE LOG — the finding with reach")
L = d["THE_LOG"]
check(L["flagged_in_advance"] is True, "banked as flagged in advance")
key = f"{P['rho_reported']:g}"
lb = L["per_rho"][key]
check(lb["verdict"].startswith("LOGARITHMIC"), "verdict LOGARITHMIC", lb["verdict"])
check(lb["increment_spread"] < 0.01, "per-decade increments constant to <0.01",
      f"{lb['increment_spread']:.2e}")
check(len(lb["per_decade_increment_of_f"]) == 4, "four increments")
check(all(abs(i - 0.743) < 0.01 for i in lb["per_decade_increment_of_f"]),
      "each ~0.743", str([round(i, 4) for i in lb["per_decade_increment_of_f"]]))
check(lb["log_fit_r2"] > lb["power_fit_r2"],
      "the log fit BEATS the power fit — and that comparison, not a preference, is the verdict",
      f"{lb['log_fit_r2']:.10f} > {lb['power_fit_r2']:.10f}")
check(abs(lb["log_fit_slope_per_decade"] - 0.743203) < 1e-5, "b = 0.743203")
check(abs(lb["power_fit_exponent"] + 0.005321) < 1e-5,
      "while the power exponent is -0.005321 — what a log looks like to a power fit")
check("0.743203" in j and "0.9999976208" in j, "the journal quotes b and the log R^2")
check("−0.005321" in j, "and the misleading power exponent, so a reader sees both")

print("== 5. M6 — UNDER-RESOURCED, and the conclusion is NOT drawn from it")
s = d["M6_direct_stencil_status"]
check(s["verdict"] == "UNDER-RESOURCED", "M6 direct stencil is UNDER-RESOURCED")
check(s["spread_across_rho"] > P["max_spread_allowed"], "its spread exceeds the limit",
      f"{s['spread_across_rho']:.3f}")
check(abs(s["coarsest_level_rho_1e-2"] + 0.998616) < 1e-5,
      "the coarsest level reads -0.998616")
check(s["log_fit_prediction"] == -1.0, "and the log fit predicts exactly -1")
check(s["agreement"] < 0.002, "agreeing to 0.0014", f"{s['agreement']:.4f}")
check("conclusion is NOT drawn from it" in s["note"], "and the artefact says so")
check("UNDER-RESOURCED" in j, "the journal states it")

print("== 6. M3 and M4 — two measurements worth banking on their own")
ff = d["M3_M4_farfield"]
check(abs(ff["alpha_mean"] + 1.0) < 1e-4, "alpha = -1.000004, the pin confirmed",
      f"{ff['alpha_mean']:.6f}")
check(ff["alpha_abs_error"] < 1e-4, "to 4e-6 of the pinned -1")
check(len(ff["per_ray"]) == 2, "measured on two independent rays")
check(1.9 < ff["delta_mean"] < 2.0, "delta = 1.974126", f"{ff['delta_mean']:.6f}")
rays = sorted(v["delta"] for v in ff["per_ray"].values())
check(abs(rays[1] - rays[0]) < 0.05, "the two rays agree to 0.025",
      f"{rays[1]-rays[0]:.4f}")

print("== 7. the gate, by the pre-committed rule")
g = d["gate"]
check(g["question"] == "Does W4 break under its own test?", "the pre-committed question")
check(g["answer"] in ("YES", "NO", "UNDER-RESOURCED"), "one of the permitted answers")
check(g["answer"] == "NO", "answered NO")
check(g["matched_expectation"] is True, "which is what was expected in advance")
check(g["clause_a1_bounded_energy"] is True, "(a1) TRUE")
check(g["clause_a2_still_blows_up"] is True, "(a2) TRUE")
check("BY CONSTRUCTION, NOT MEASURED" in g["clause_a2_note"],
      "and (a2) is labelled by-construction rather than passed off as a measurement")
check(g["clause_a3_force_admissible"] is False, "(a3) FALSE")
check("NO" in j and "no escalation is raised" in j.lower(),
      "the journal states the answer and that no escalation is raised")

print("== 8. controls, including the one that failed")
kc = d["controls"]
k1 = kc["K1_typeII_gamma0.7"]
check(k1["abs_err"] > P["M1_tol"],
      "K1 FAILED its pre-committed tolerance", f"{k1['abs_err']:.6f} > {P['M1_tol']}")
check(k1["moved_toward_prediction_on_tail"] is True,
      "and its tail fit moved toward the prediction")
check(k1["tail_abs_err"] < 0.01, "to |err| 0.0033", f"{k1['tail_abs_err']:.6f}")
check(d["controls_all_as_predicted"] is False,
      "so controls_all_as_predicted is FALSE — the failure is reported, not re-scored")
check("FAILED at the pre-committed tolerance" in j, "the journal calls it a failure")
k2 = kc["K2_uscale2.5"]
check(k2["shift_from_P0"] < 1e-6,
      "K2: scaling the profile by 2.5 moves the exponent by 1e-08 — a scaling, not an amplitude")
check(kc["K5_exact_shear"]["max_abs_residual"] < 1e-6, "K5 exact solution: residual 0")
check(kc["K6_shear_1pc_wrong"]["max_abs_residual"] > 1e-4, "K6 1% wrong: nonzero")
check(kc["K3_planted_delta1.5"]["abs_err"] <= 0.10, "K3 recovers a planted delta 1.5")
check(kc["K4_planted_delta3.0"]["abs_err"] <= 0.10, "K4 recovers a planted delta 3.0")

print("== 9. the counterfactual is labelled one, and the ceiling holds")
cf = d["M5_M6_annulus_counterfactual"]
check(cf["is_a_counterfactual"] is True, "M5/M6 banked as a counterfactual")
check("SOLVES its equation" in cf["what_it_grants"], "and what it grants is stated")
cm = d["clay_movement"]
check(cm["links_moved"] == 0 and cm["walls_moved"] == "none", "no link, no wall")
check("0.05" in cm["clay_odds"], "Clay unchanged")
check("UNVERIFIED" in d["verification_status"], "banked UNVERIFIED")
check("no known method" in j, "the journal keeps W4's own wording about what it claims")

print()
if fail:
    print(f"DRIFT: {len(fail)} check(s) failed")
    for x in fail:
        print(f"  - {x}")
    sys.exit(1)
print("arc6 U5 evidence: all checks pass")
