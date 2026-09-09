"""Arc-6 U4 evidence: rebuild every number in leg 420's prose from the artefact.

    .venv/bin/python writeup/arc6_instantiate_evidence.py

Checks, without re-running the experiment:
  * the pre-registration banked in the artefact is the one committed at d026cd4,
    field by field — so a prereg edited after the fact would show up here;
  * every number quoted in experiments/journal/leg_420.md is in the JSON;
  * the gate's pre-committed conjunction is evaluated from the banked numbers,
    and the artefact's own answer agrees with that evaluation;
  * the post-hoc corrected formula is banked as POST HOC and is NOT what the
    gate is scored against.

Exit 0 = no drift. Exit 1 = a prose number, or a scoring rule, left its source.

DELIBERATELY NOT DONE HERE: re-running the residual measurement. That is
experiments/arc6_instantiate_v1.py's job, and a script that re-runs the
experiment it is supposed to check cannot disagree with it — CORRECTIONS.md §54.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON = ROOT / "writeup" / "data" / "arc6_instantiate_v1.json"
JOURNAL = ROOT / "experiments" / "journal" / "leg_420.md"
PREREG = ROOT / "experiments" / "journal" / "leg_420_prereg.md"

fail = []
def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok:
        fail.append(label)

d = json.loads(JSON.read_text())
j = re.sub(r"\s+", " ", JOURNAL.read_text())
pr = PREREG.read_text()
P = d["prereg"]

print("== 1. the banked pre-registration is the committed one, field by field")
check(P["commit"] == "d026cd4", "prereg commit banked", P["commit"])
check(P["predicted_exponent"] == -1.51, "predicted exponent -1.51")
check(P["tolerance"] == 0.05, "tolerance 0.05")
check(P["max_spread_allowed"] == 0.025, "spread limit 0.025")
check(P["rho_levels"] == [1e-2, 1e-3, 1e-4], "three rho levels")
check(P["rho_reported"] == 1e-3, "reported level is the middle one")
check(len(P["tau_ladder"]) == 5, "five-rung tau ladder")
check(abs(P["systematic_floor_derived"] - 0.0201) < 1e-9, "derived floor 0.0201")
check(P["tolerance"] > 2 * P["systematic_floor_derived"],
      "the tolerance is above twice the derived floor, as the prereg argues")
for tok in ["-3/2 - h = -1.51", "0.05", "0.0201", "0.025"]:
    check(tok in pr or tok.replace("-", "−") in pr, f"prereg text carries {tok}")
check("TOLERANCE: `|measured − (−1.51)| ≤ 0.05`" in pr,
      "prereg states the tolerance in its own words")

print("== 2. P0 against the two pre-committed numbers")
cases = {c["name"]: c for c in d["cases"]}
p0 = cases["P0_instantiation"]
check(abs(p0["reported_exponent"] + 1.498218) < 5e-6,
      "P0 measured -1.498218", f"{p0['reported_exponent']:.6f}")
check(abs(p0["abs_error_vs_prediction"] - 0.011782) < 5e-6, "P0 |err| 0.011782")
check(p0["abs_error_vs_prediction"] <= P["tolerance"], "P0 inside the tolerance")
check(p0["spread_across_rho"] < P["max_spread_allowed"], "P0 spread inside the limit",
      f"{p0['spread_across_rho']:.2e}")
check(p0["spread_across_rho"] < 1e-6, "and the spread is 2.11e-07, six orders under it")
check("−1.498218" in j and "0.011782" in j and "2.11e-07" in j,
      "the journal quotes all three")

print("== 3. the gate's pre-committed conjunction, evaluated from the banked numbers")
g = d["gate"]
conj = (p0["inside_tolerance"] and p0["spread_ok"] and g["controls_all_as_predicted"])
check(g["answer"] == "YES-BUT-CONTROLS-FAILED", "the artefact's gate string", g["answer"])
check(conj is False, "the pre-committed conjunction evaluates to FALSE")
check(g["controls_all_as_predicted"] is False, "and the artefact records that")
check(g["which_control_failed"] == "C2_A0.51_D0.70", "it names which control failed")
check("PRE-REGISTRATION'S FORMULA WAS WRONG" in g["answer_in_full"],
      "and says the failure is the prereg's, not the instrument's")
check("not re-scored" in g["answer_in_full"] or "rather than re-scored" in g["answer_in_full"],
      "and refuses to re-score the control against the corrected formula")
check("THE PRE-COMMITTED CONJUNCTION IS NOT MET" in j,
      "the journal states the conjunction is not met")

print("== 4. C2's failure, and the omitted term")
c2 = cases["C2_A0.51_D0.70"]
check(abs(c2["predicted_exponent"] + 1.72) < 1e-9, "C2's PRE-COMMITTED prediction was -1.72")
check(abs(c2["reported_exponent"] + 1.909028) < 5e-6, "C2 measured -1.909028")
check(abs(c2["abs_error_vs_prediction"] - 0.189028) < 5e-6, "C2 |err| vs prereg 0.189028")
check(c2["inside_tolerance"] is False, "C2 is OUTSIDE its pre-committed tolerance")
ph = d["posthoc_corrected_formula"]
check(ph["prereg_formula"] == "-max(A + 1, 2A + D)", "the prereg formula is banked verbatim")
check(ph["corrected_formula"] == "-max(A + 1, 2A + D, A + 2D)", "and the corrected one")
check("axial diffusion" in ph["omitted_term"], "the omitted term is named")
check(ph["status"].startswith("POST HOC"), "the correction is labelled POST HOC")
check("Not used to answer the gate" in ph["status"], "and excluded from the gate")
rows = {r["name"]: r for r in ph["rows"]}
check(abs(rows["C2_A0.51_D0.70"]["corrected_prediction"] + 1.91) < 1e-9,
      "corrected prediction for C2 is -1.91")
check(rows["C2_A0.51_D0.70"]["abs_error_vs_corrected"] < 0.001,
      "against which C2 lands at |err| < 0.001",
      f"{rows['C2_A0.51_D0.70']['abs_error_vs_corrected']:.6f}")
check("PH1_A0.51_D0.60" in rows and "PH2_A0.60_D0.55" in rows,
      "two FRESH exponent pairs test the corrected formula rather than fit it")
check(rows["PH2_A0.60_D0.55"]["abs_error_vs_corrected"] > P["tolerance"],
      "and PH2 lands OUTSIDE tolerance — reported, not hidden",
      f"{rows['PH2_A0.60_D0.55']['abs_error_vs_corrected']:.6f}")

print("== 5. the contamination prediction, made before it was checked")
t = d["posthoc_tail_fit"]
check("must move TOWARD" in t["prediction_made_before_looking"],
      "the prediction is banked in its own words")
check(t["all_moved_toward"] is True, "and every case moved toward its prediction")
for row in t["rows"]:
    check(row["moved_toward_prediction"] is True, f"{row['name']} moved toward")
c1t = [r for r in t["rows"] if r["name"] == "C1_A0.80_D0.49"][0]
check(c1t["abs_error_tail"] < c1t["abs_error_full"] / 2,
      "C1's error more than halves on the tail fit", f"{c1t['abs_error_tail']:.6f}")

print("== 6. the controls that behaved")
c3 = cases["C3_amplitudes_rescaled"]
_c3d = abs(c3["reported_exponent"] - p0["reported_exponent"])
check(_c3d < 1e-9,
      "C3: rescaling amplitudes moves the exponent by 1.4e-11 — roundoff, not a shift; "
      "an amplitude is not an exponent", f"{_c3d:.2e}")
check(c3["B_scale"] == 3.7 and c3["S_scale"] == 0.4, "C3 really did rescale")
ops = {o["name"]: o for o in d["operator_controls"]}
check(ops["C4_rigid_rotation"]["relative_to_velocity_scale"] < 1e-8,
      "C4 rigid rotation: residual is zero to discretisation error")
check(ops["C5_bessel_shear"]["relative_to_velocity_scale"] < 1e-8,
      "C5 Bessel shear: same")
check(ops["C6_bessel_shear_1pc_wrong"]["relative_to_velocity_scale"] > 1e-4,
      "C6 the same field 1% wrong: NONZERO — C4/C5 are not vacuous")
check(d["radial_balance_relative_residual"] < 1e-10,
      "the pressure satisfies the leading radial balance identically",
      f"{d['radial_balance_relative_residual']:.3e}")

print("== 7. the exterior moment identities, reported as FAILING")
check(d["exterior_moments_expected_to_fail"] is True, "banked as expected to fail")
check(abs(d["exterior_moment_int_r2_Rtheta"]) > 1.0, "int r^2 R_theta is not zero")
ratio = abs(d["exterior_moment_int_r2_Rtheta"]) / d["exterior_moment_int_r2_Rtheta_abs"]
check(abs(ratio - 1.0) < 1e-6,
      "and its |.| ratio is 1.0000 — R_theta has ONE SIGN, so no amplitude cancels its moment",
      f"{ratio:.4f}")
check(abs(d["exterior_moment_int_r_Rz"]) > 1.0, "int r R_z is not zero either")
check("ratio 1.0000" in j, "the journal quotes the one-sign ratio")

print("== 8. the ceiling")
cm = d["clay_movement"]
check(cm["links_moved"] == 0 and cm["walls_moved"] == "none", "no link, no wall")
check("0.05" in cm["clay_odds"], "Clay unchanged")
check("UNVERIFIED" in d["verification_status"], "banked UNVERIFIED")

print()
if fail:
    print(f"DRIFT: {len(fail)} check(s) failed")
    for x in fail:
        print(f"  - {x}")
    sys.exit(1)
print("arc6 U4 evidence: all checks pass")
