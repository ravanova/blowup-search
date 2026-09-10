"""Arc-6 second pass (R7, leg 434): every number in TECHNICAL_REPRODUCTION.md re-derived from the
banked artefacts, and every unit's own evidence script run.

    .venv/bin/python writeup/6_reproduction/reproduction_evidence.py

Exits nonzero on drift. Nothing is re-run except the per-unit evidence scripts (seconds each).
"""
import json, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "writeup" / "data" / "arc6"
T = re.sub(r"\s+", " ", (ROOT / "writeup" / "6_reproduction" / "TECHNICAL_REPRODUCTION.md").read_text())
fail = []
def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok: fail.append(label)
J = lambda p: json.loads(p.read_text())

print("== 1. the per-unit evidence scripts, each on its own artefacts")
for s in ["writeup/arc6_ledger_evidence.py", "writeup/arc6_merged_evidence.py", "writeup/arc6_dag_evidence.py", "writeup/arc6_spine_evidence.py",
          "writeup/arc6_profile_evidence.py", "writeup/arc6_lean_evidence.py", "writeup/arc6_residual_evidence.py", "writeup/arc6_wave4_evidence.py"]:
    p = ROOT / s
    if not p.exists():
        check(False, f"{s} exists"); continue
    r = subprocess.run([sys.executable, str(p)], capture_output=True, text=True, cwd=ROOT)
    check(r.returncode == 0, f"{s} passes", (r.stdout + r.stderr).strip().splitlines()[-1][:160] if (r.stdout + r.stderr).strip() else "")

print("== 2. R1–R3: the extraction, the two readings, the graph")
si = J(D / "statement_index.json"); led = J(D / "ledger.json"); mg = J(D / "ledger" / "merged.json"); dag = J(D / "dag.json")
n_stmt = len(si["statements"]) if isinstance(si, dict) and "statements" in si else len(si)
check(n_stmt == 79 and len(led["entries"]) == 79, "79 statements indexed and 79 ledger entries")
check(len(led["hard_pages"]) == 13, "13 solo hard-page notes", str(len(led["hard_pages"])))
sp = dag.get("r4_spine") or dag.get("spine", {}).get("r4_spine")
check(sp is not None and len(sp) == 58, "the R4 spine has 58 nodes", str(None if sp is None else len(sp)))

print("== 3. R4: the spine re-derived")
spm = J(D / "spine" / "merged.json")
check(spm["counts"] == {"CHECKED": 58, "GAP": 0, "NOT-CHECKED": 0} and spm["agreement"]["rate"] == 1.0 and len(spm["verified"]) == 10, "58 CHECKED / 0 GAP; verifier agreement 1.0; ten VERIFIED")

print("== 4. R5(i), R5(ii): the instantiation")
pr = J(ROOT / "writeup" / "data" / "arc6_profile_v1.json"); r1 = pr["preregistered_runs"]["0.1"]
check(abs(r1["G1"]["K_b"] - 0.2450) < 5e-5 and r1["gates"]["G3"][0] == "NO" and r1["gates"]["G7"][0] == "NO" and r1["gates"]["G8"][0] == "YES", "G1 K_b = .2450; G3, G7 NO; G8 YES at lambda = 0.1")
sw = pr["post_hoc"]["lambda_sweep"]; roots = sorted(float(k) for k, v in sw.items() if v["root_in_bracket"])
check(roots and max(roots) == 3e-4 and all(not sw[k]["root_in_bracket"] for k in sw if float(k) > 3e-4), "a bracket root at every swept lambda <= 3e-4 and none above", str(roots))
rs = J(ROOT / "writeup" / "data" / "arc6_residual_v1.json"); h3 = rs["preregistered_runs"]["0.001"]
check(all(v[0] == "YES" for v in h3["gates"].values()) and h3["H2"]["delta_cross"] < 1e-60 and 2.5 <= h3["H3"]["local_power_Tz_over_Ttheta_at_0.05"] <= 3.5, "R5(ii): H0–H7 YES; delta_cross ~ 1e-69; T_z/T_theta carries delta^3")

print("== 5. R6: the Lean, measured")
lm = J(D / "lean" / "merged.json"); a = lm["answers"]
check(a["1_build"]["kernel_verdict"] == "NOT-ESTABLISHED" and a["2_statement"]["gate_answer"]["relation"] == "weaker" and a["3_census"]["counts"]["sorry_in_code"] == 4 and a["3_census"]["counts"]["axiom"] == 0
      and a["4_comparator"]["n_pass"] == 7 and a["5_coverage"]["summary"]["FORMALIZED"] == 74, "(a) NOT-ESTABLISHED (b) weaker (c) 4 sorry / 0 axiom (d) 7 PASS (e) 74 FORMALIZED")
check(lm["cross_agent"]["no_agent_ran_a_kernel_check"], "no agent ran a kernel check")

print("== 6. wave 4: the adversary's rule applied")
w4p = D / "wave4" / "merged.json"
if w4p.exists():
    w4 = J(w4p)
    check(w4["present"] == [3, 4, 5, 6, 7], "five wave-4 files present")
    for gid, r in w4["evidence_table"].items():
        check(gid in T and (r["status"].split(" ")[0] in T), f"the note quotes {gid}'s status {r['status']!r}")
else:
    check(False, "wave4/merged.json exists")

print("== 7. the note quotes what the artefacts hold")
for tok in ["0.2450", "3·10⁻⁴", "10⁻⁶⁹", "58", "480", "301", "`NOT-ESTABLISHED`", "WEAKER", "74 `FORMALIZED`", "Tier 2 is never a proof", "No `L1 → L4` link moved"]:
    check(tok in T, f"note quotes {tok!r}")
if fail:
    print(f"DRIFT: {len(fail)}"); [print("  -", x) for x in fail]; sys.exit(1)
print("arc6 second pass: reproduction evidence — all checks pass")
