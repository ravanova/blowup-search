"""Arc-6 R6 evidence (leg 431): lean/merged.json is what the journal says it is.

    .venv/bin/python writeup/arc6_lean_evidence.py

Re-runs the merge from the five agent files, compares with the banked merge,
re-derives the five gate answers (a)-(e) from the agent files themselves, and
checks every number the journal quotes. Nothing is built or kernel-checked
here: the point of this script is that the journal cannot claim more than the
five files hold. Exits nonzero on drift.
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))
import arc6_lean_merge as M  # noqa: E402
J = re.sub(r"\s+", " ", (ROOT / "experiments" / "journal" / "leg_431.md").read_text())
fail = []
def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok: fail.append(label)

A = {k: json.loads((M.LD / f).read_text()) for k, f in M.FILES.items()}
banked = json.loads(M.OUT.read_text())
fresh = M.run(write=False, verbose=False)

print("== 1. five files, one author each, one clone")
check(sorted(A) == [1, 2, 3, 4, 5] and all(a["schema"] == "arc6_lean_v1" and a["agent"] == k and a["leg"] == 431 for k, a in A.items()), "five agent files, schema arc6_lean_v1, agent numbers 1..5, leg 431")
check(len({a["clone_head"] for a in A.values()}) == 1 and A[1]["clone_head"].startswith("8937a8f4"), "all five read the same clone HEAD 8937a8f4")
check(banked == fresh, "merged.json re-derives from the five files")
check(banked["present"] == [1, 2, 3, 4, 5] and not banked["absent"], "no agent absent")

print("== 2. the five gate answers, re-derived from the agent files")
b = A[1]["build"]; kc = A[1]["kernel_check"]
check(kc["verdict"] == "NOT-ESTABLISHED" and kc["attempted"] and "does not exist" in kc["output"], "(a) build: kernel check attempted, NOT-ESTABLISHED because the module was never reached")
check(b["errors_in_log"] == 0 and b["oleans_after"] > b["oleans_before"] and b["project_modules_built_count"] == 1, "(a) build: no errors, oleans advanced, one project module (the problem statement) written", f"{b['oleans_before']}→{b['oleans_after']}, wall {b['wall_s']} s")
check(b["wall_s"] < 2400 and "KILLED" in b["exit_code_or_timeout"], "(a) build: killed by the agent before the 40 min cap (the Conductor's mis-statement of the cap is recorded in the journal)")
v = A[2]["verdict"]; d11 = {c["clause"]: c["status"] for c in A[2]["diff_vs_theorem_1_1"]}
check(v["relation"] == "weaker", "(b) statement: the Lean top-level theorem is strictly WEAKER than Theorem 1.1")
absent = [c for c, s in d11.items() if s == "ABSENT"]
check(len(absent) == 5 and any("compact K" in c for c in absent) and any("L²" in c or "L2" in c for c in absent) and any("limsup" in c for c in absent), "(b) statement: the existence clauses of Theorem 1.1 (compact K, bounded energy, limsup L∞ = ∞, ...) are ABSENT", str(absent))
check(all(c["status"] == "PRESENT" for c in A[2]["diff_vs_fefferman_C"]), "(b) statement: every clause of Fefferman's (C) is PRESENT")
check(all(c["status"] in ("PRESENT", "STRONGER") for c in A[2]["diff_vs_fefferman_D"]), "(b) statement: (D) PRESENT clause for clause, periodic pressure STRONGER")
check([t["name"] for t in A[2]["main_theorems"]] == ["NavierStokes.Comparator.navier_stokes_breakdown_R3", "NavierStokes.Comparator.navier_stokes_breakdown_periodic"], "(b) statement: the two exported theorems are the (C)/(D) comparator statements")
c3 = A[3]["counts"]
check(c3["sorry_in_code"] == 4 == len(A[3]["sorry_declarations"]) and all("ComparatorChallenges/" in s["file"] for s in A[3]["sorry_declarations"]), "(c) census: 4 code-level sorry, all four in ComparatorChallenges/")
check(c3["axiom"] == 0 and c3["admit"] == 0 and c3["native_decide"] == 0 and c3["set_option_any"] == 0 and c3["unsafe"] == 0 and c3["implemented_by"] == 0 and c3["extern"] == 0, "(c) census: 0 axiom / admit / native_decide / set_option / unsafe / implemented_by / extern")
check(A[3]["kernel_level"]["verdict"] == "NOT-ESTABLISHED", "(c) census: kernel-level verdict NOT-ESTABLISHED (a source count is necessary, not sufficient)")
cs = A[3]["import_closure"]["closure_stats"]
check(cs["reachable_from_either_main_file"] == 2409 and cs["unreachable_from_both_main_files"] == 73, "(c) census: 2409 modules reachable from the two main files, 73 dead", str({k: cs[k] for k in ("reachable_from_either_main_file", "unreachable_from_both_main_files")}))
ch = [c["result"] for c in A[4]["checks_performed"]]
check(ch.count("PASS") == 7 and ch.count("NOT-ESTABLISHED") == 4 and ch.count("FAIL") == 0 and len(ch) == 11, "(d) comparator: 11 checks, 7 PASS / 4 NOT-ESTABLISHED / 0 FAIL")
check(any("never" in s.lower() and "run" in s.lower() for s in [A[4]["gate_answer"]]), "(d) comparator: the comparator itself was never run")
sm = A[5]["summary"]
check(sm == {**sm, "FORMALIZED": 74, "PARTIAL": 5, "STATED-ONLY": 0, "ABSENT": 0, "UNCLEAR": 0, "total": 79}, "(e) coverage: 74 FORMALIZED / 5 PARTIAL / 0 STATED-ONLY / 0 ABSENT / 0 UNCLEAR of 79")
ids = [m["id"] for m in A[5]["map"]]
ledger_ids = sorted(e["id"] for e in json.loads((ROOT / "writeup" / "data" / "arc6" / "ledger.json").read_text())["entries"])
check(len(ids) == 79 == len(set(ids)) and sorted(ids) == ledger_ids, "(e) coverage: the map carries exactly the ledger's 79 ids, once each")
check(sorted(sm["partial_ids"]) == sorted(["Theorem 3.1", "Definition 3.3", "Lemma 4.4", "Corollary 7.3", "Lemma 9.7"]), "(e) coverage: the five PARTIAL ids")
check("not a kernel check" in A[5]["gate_answer"], "(e) coverage: the agent says FORMALIZED is a source-level judgement, not a kernel check")

print("== 3. cross-agent facts")
x = banked["cross_agent"]
check(x["mathlib_rev_agree"] and x["sorry_only_in_comparator_challenges"] and x["sorry_counts_by_scope"]["consistent"], "mathlib rev agrees (1 vs 3); sorry counts agree once scopes are aligned (3: whole clone 4, 5: NavierStokes/ 0)")
check(x["no_agent_ran_a_kernel_check"] and x["kernel_verdicts"] == {"1": "NOT-ESTABLISHED", "3": "NOT-ESTABLISHED"}, "no agent ran a kernel check; both kernel verdicts NOT-ESTABLISHED")
check(all(a.get("could_not_determine") for a in A.values()), "every agent lists what it could not determine")

print("== 3b. the Conductor's kernel check (leg 435 addendum), banked verbatim")
kc = M.LD / "kernel_check_conductor.json"
if kc.exists():
    K = json.loads(kc.read_text())
    check(K["result"]["navier_stokes_breakdown_R3_axioms"] == ["propext", "Classical.choice", "Quot.sound"] == K["result"]["navier_stokes_breakdown_periodic_axioms"] and K["result"]["exit_code"] == 0, "both exported theorems depend on exactly [propext, Classical.choice, Quot.sound]")
    check("depends on axioms: [propext, Classical.choice, Quot.sound]" in K["output_verbatim"] and K["clone_head"].startswith("8937a8f4") and K["build_state_at_check"]["error_lines_in_build_log"] == 0, "output banked verbatim; same clone HEAD; zero build errors")
    check("ESTABLISHED-HERE" in J and "§7. ADDENDUM" in J and "UNVERIFIED" in J, "the journal's §7 addendum records it as ESTABLISHED-HERE and UNVERIFIED by a second agent")
    check("addendum" in K["run_by"].lower() or "after the five R6 agents" in K["run_by"], "the artefact says who ran it and when")
else:
    print("  [----] no kernel_check_conductor.json — (a) stands as the agents left it")
print("== 4. the journal quotes what the artefacts hold")
for tok in ["NOT-ESTABLISHED", "WEAKER", "74", "4 `sorry`", "7 PASS", "UNVERIFIED", "no kernel check", "13.6 min", "2409", "73 dead", str(b["oleans_after"]), "never run"]:
    check(tok in J, f"journal quotes {tok!r}")

if fail:
    print(f"DRIFT: {len(fail)}"); [print("  -", x) for x in fail]; sys.exit(1)
print("OK: lean/merged.json and leg_431.md agree with the five agent files")
