"""Arc-6 R3 evidence: dag.json is what the leg-426 journal says it is.

    .venv/bin/python writeup/arc6_dag_evidence.py

Re-runs the three passes from the banked ledger and page text, compares them
with dag.json, recomputes the gate, and checks every number the journal
quotes. Exits nonzero on drift.
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))
import arc6_dag as G  # noqa: E402
J = re.sub(r"\s+", " ", (ROOT / "experiments" / "journal" / "leg_426.md").read_text())
fail = []
def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok: fail.append(label)

banked = json.loads(G.OUT.read_text())
fresh = G.run(write=False, verbose=False)
print("== 1. the artefact is reproducible")
for p in ("ledger_pass", "text_pass", "equation_pass"):
    for k in ("gate", "counts", "spine_m"):
        check(banked[p][k] == fresh[p][k], f"{p}.{k} re-derives")
check(banked["prereg"]["spine_list_length"] == 38 and banked["prereg"]["prereg_summary_line_said"] == 36, "prereg list 38, summary line said 36 (banked, not edited)")
check(banked["prereg"]["text_pass_is_post_hoc"] is True, "post-hoc passes labelled so")

print("== 2. the gate")
L, T, Q = banked["ledger_pass"], banked["text_pass"], banked["equation_pass"]
check(all(P["gate"]["acyclic"] == "YES" for P in (L, T, Q)), "acyclic YES in all three passes")
check(L["counts"]["raw_cycles_no_rules"] == 19, "19 raw cycles without the rules", str(L["counts"]["raw_cycles_no_rules"]))
check(L["gate"]["complete"].startswith("NO") and Q["gate"]["complete"].startswith("NO"), "complete: NO-AND-HERE-ARE-THE-DANGLING-NODES")
check(any("Remark B.9" in d["cite"] for d in L["gate"]["dangling"]), "Remark B.9 is a dangling node")
check(Q["counts"]["unresolved_labels"] == {"Corollary B.10": ["B.40"]}, "(B.40) is the one unresolved label")
check(len(Q["gate"]["prose_nodes_reached"]) == 10, "ten prose nodes reached in the equation pass")
outside = set(Q["gate"]["outside_closure"])
check(outside == {"Proposition 9.6", "Proposition 9.5", "Proposition 8.4", "Corollary 8.5", "Lemma 8.6", "Lemma 8.8", "Corollary 7.8", "Lemma 6.3", "Corollary 10.6"},
      "the nine un-cited statements", str(sorted(outside)))
check(set(banked["closure_union_all_passes"]) | outside == {e["id"] for e in json.loads(G.LEDGER.read_text())["entries"]} and len(banked["closure_union_all_passes"]) == 70,
      "closure over the union of passes is 70 of 79")
check(Q["outside_invoked_by_narrative"]["Proposition 9.6"] == [7, 13, 14, 15, 24, 73, 88, 100, 101, 106], "Proposition 9.6 is named only in narrative, on those ten pages")
check((L["gate"]["closure_size"], T["gate"]["closure_size"], Q["gate"]["closure_size"]) == (56, 51, 70), "closures 56 / 51 / 70")
check((L["gate"]["longest_chain_edges"], T["gate"]["longest_chain_edges"], Q["gate"]["longest_chain_edges"]) == (22, 14, 27), "chains 22 / 14 / 27")
check((len(L["gate"]["outside_closure"]), len(T["gate"]["outside_closure"]), len(Q["gate"]["outside_closure"])) == (23, 28, 9), "outside 23 / 28 / 9")
check((L["gate"]["spine_contains_4_7_9"], T["gate"]["spine_contains_4_7_9"], Q["gate"]["spine_contains_4_7_9"]) == ("NO-AND-MISSING-7", "NO-AND-MISSING-7", "YES"), "§7 missing by citation, present by equation")
check((L["n_passed"], T["n_passed"], Q["n_passed"]) == (4, 2, 5), "prereg checks 4 / 2 / 5 of 8")
check(Q["gate"]["longest_chain"][0] == "Theorem 1.1" and Q["gate"]["longest_chain"][-1] == "Definition 3.2" and "Proposition 7.2" in Q["gate"]["longest_chain"], "the 27-edge chain runs Theorem 1.1 -> ... -> Proposition 7.2 -> ... -> Definition 3.2")
check(len(banked["r4_spine"]) == 58 and set(banked["r4_spine_named_additions"]) == {"Lemma 4.8", "Lemma 9.7"}, "R4 spine has 58 nodes, two named additions", str(len(banked["r4_spine"])))

print("== 3. the journal quotes what the artefact holds")
for tok in ["199", "126", "278", "361", "134", "19", "56", "51", "70", "22", "14", "27", "23", "28", "4 of 8", "2 of 8", "5 of 8",
            "NO-AND-MISSING-7", "NO-AND-HERE-ARE-THE-DANGLING-NODES", "Remark B.9", "(B.40)", "Proposition 9.6", "pp. 7, 13, 14, 15, 24, 73, 88, 100, 101, 106",
            "36", "38", "27-edge", "58 nodes", "UNVERIFIED", "post hoc"]:
    check(tok in J, f"journal quotes {tok!r}")
print()
if fail:
    print(f"DRIFT: {len(fail)}"); [print("  -", x) for x in fail]; sys.exit(1)
print("arc6 R3 evidence: all checks pass")
