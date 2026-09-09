"""Arc-6 R4 evidence (leg 429): spine/merged.json is what the journal says it is.

    .venv/bin/python writeup/arc6_spine_evidence.py

Re-runs the merge from the five agent files, compares with the banked merge,
recomputes the gate, and checks every number the journal quotes. Exits nonzero on drift.
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))
import arc6_spine_merge as M  # noqa: E402
J = re.sub(r"\s+", " ", (ROOT / "experiments" / "journal" / "leg_429.md").read_text())
fail = []
def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok: fail.append(label)

banked = json.loads(M.OUT.read_text())
fresh = M.run(write=False, verbose=False)
print("== 1. reproducible")
for k in ("counts", "verifier_counts", "agreement", "verified", "gaps", "verifier_gaps", "missing", "escalation_candidates"):
    check(banked[k] == fresh[k], f"{k} re-derives")
print("== 2. the gate")
check(banked["spine_size"] == 58 and banked["nodes_with_verdict"] == 58 and not banked["missing"], "58 of 58 nodes carry a verdict")
check(banked["counts"] == {"CHECKED": 58, "GAP": 0, "NOT-CHECKED": 0}, "58 CHECKED / 0 GAP / 0 NOT-CHECKED", str(banked["counts"]))
check(banked["verifier_counts"] == {"CHECKED": 10, "GAP": 0, "NOT-CHECKED": 0}, "verifier 10 / 0 / 0")
check(banked["agreement"]["n"] == 10 and banked["agreement"]["rate"] == 1.0 and not banked["agreement"]["disagreements"], "agreement 10 of 10")
check(set(banked["verified"]) == {"Lemma 4.4", "Proposition 4.10", "Lemma 6.3", "Lemma 8.8", "Proposition 9.1", "Lemma 9.8", "Proposition 9.9", "Lemma B.7", "Proposition B.8", "Proposition C.3"}, "the ten VERIFIED nodes are the seed-428 sample")
check(sorted(banked["sampled"]) == sorted(banked["verified"]), "every sampled node was reproduced blind")
check(all(not v for v in banked["escalation_candidates"].values()), "no escalation candidates")
per = {}
tot_rec = tot_steps = tot_art = 0
for k in (1, 2, 3, 4):
    d = json.loads((M.SP / f"agent_{k}.json").read_text())
    per[k] = d["summary"]; tot_rec += sum(len(n.get("recomputed", [])) for n in d["nodes"]); tot_steps += sum(len(n.get("steps_checked", [])) for n in d["nodes"]); tot_art += len(d.get("extraction_artefacts_found", []))
v = json.loads((M.SP / "agent_5_verifier.json").read_text())
tot_rec += sum(len(n.get("recomputed", [])) for n in v["nodes"]); tot_steps += sum(len(n.get("steps_checked", [])) for n in v["nodes"]); tot_art += len(v.get("extraction_artefacts_found", []))
check(per == {1: {"CHECKED": 15, "GAP": 0, "NOT-CHECKED": 0}, 2: {"CHECKED": 12, "GAP": 0, "NOT-CHECKED": 0}, 3: {"CHECKED": 10, "GAP": 0, "NOT-CHECKED": 0}, 4: {"CHECKED": 21, "GAP": 0, "NOT-CHECKED": 0}}, "per-agent 15/12/10/21")
check((tot_rec, tot_steps, tot_art) == (301, 480, 53), "301 recomputed, 480 steps, 53 extraction artefacts", str((tot_rec, tot_steps, tot_art)))
es = banked["existence_source"]
check(all("9.6" in (es[k].get("agent") or "") + (es[k].get("verifier") or "") for k in ("Proposition 9.9", "Lemma 9.8")), "existence_source names Proposition 9.6 for 9.9 and 9.8")
check(v.get("seed") == 428 and len(v["nodes_assigned"]) == 10, "verifier seed 428, ten nodes")
print("== 3. the journal quotes what the artefact holds")
for tok in ["**58** | **0** | **0**", "10 of 10", "301 recomputed", "480", "53", "0.07", "eight", "UNVERIFIED (48)", "seed 428", "1.0"]:
    check(tok in J, f"journal quotes {tok!r}")
print()
if fail:
    print(f"DRIFT: {len(fail)}"); [print("  -", x) for x in fail]; sys.exit(1)
print("arc6 R4 evidence: all checks pass")
