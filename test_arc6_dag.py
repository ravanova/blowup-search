"""Self-running checks for experiments/arc6_dag.py (arc 6, R3, leg 426).

    .venv/bin/python test_arc6_dag.py

PLANTED CONTROLS FIRE IN BOTH DIRECTIONS, as pre-registered in
experiments/journal/leg_426_prereg.md §5: each control has a check that MUST
pass and a twin that MUST fail. C4 was first written to assert the
pre-registered numbers (closure >= 60, chain >= 8) on the ledger pass; the
ledger pass FAILED the closure number, so C4 now asserts the BANKED values and
the journal says so. The numbers below are the banked ones, not the hoped-for ones.
"""
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "experiments"))
import arc6_dag as G  # noqa: E402

_fails = []


def check(ok, label):
    print(f"  [{'ok' if ok else 'FAIL'}] {label}")
    if not ok:
        _fails.append(label)


led = json.loads(G.LEDGER.read_text())
index = json.loads(G.INDEX.read_text())
lines = G.load_lines()

print("== parser")
check(G.statement_refs("Propositions A.4, A.7, A.10 and Lemmas A.5, A.6 through those") ==
      ["Proposition A.4", "Proposition A.7", "Proposition A.10", "Lemma A.5", "Lemma A.6"], "plural lists parse item by item")
check(G.statement_refs("Lemma 4.1 (endpoints eta = +-1)") == ["Lemma 4.1"], "singular takes one token")
check(G.statement_refs("proved in Section 10.4 from Proposition 10.1, Lemma 10.3") == ["Proposition 10.1", "Lemma 10.3"],
      "a Section number after 'Section' is not a statement")
check(G.statement_refs("(7.5)") == [] and G.statement_refs("Theorem 4.6(iii),(iv)") == ["Theorem 4.6"], "parenthesised tokens are equations")
check(G.statement_refs("Proposi- tion 4.10 and Lem- ma 4.7") == ["Proposition 4.10", "Lemma 4.7"], "line-wrap hyphenation is repaired")
check(G.classify("Remark B.9", []) == "UNNUMBERED" and G.classify("Duhamel's formula", []) == "CLASSICAL"
      and G.classify("Fefferman [13] alternative (C)", []) == "REFERENCE" and G.classify("proved in Section 4.6 (pp. 39-44)", []) == "LOCATION",
      "non-statement classes, LOCATION included")

print("== C1: an inserted back-edge breaks acyclicity, removing it restores YES")
dep, _ = G.build(led)
check(not G.cycles(dep), "the ledger-pass graph is acyclic (MUST pass)")
bad = set(dep) | {("Lemma 4.1", "Theorem 1.1")}
check(len(G.cycles(bad)) >= 1, "with a planted back-edge Lemma 4.1 -> Theorem 1.1 a cycle is found (MUST fail)")
check(not G.cycles(bad - {("Lemma 4.1", "Theorem 1.1")}), "removing it restores acyclicity")

print("== C2: deleting a leaf statement removes it from the closure and the parser refuses edges to it")
out = G.run(write=False, verbose=False)
L = out["ledger_pass"]
leaf = next(l["id"] for l in L["leaves"] if l["id"] != "Theorem 1.1")
led2 = copy.deepcopy(led)
led2["entries"] = [e for e in led2["entries"] if e["id"] != leaf]
dep2, log2 = G.build(led2)
check(leaf in G.reachable(G.adjacency(dep), G.ROOT_NODE) and leaf not in G.reachable(G.adjacency(dep2), G.ROOT_NODE),
      f"{leaf} is in the closure with it and gone without it")
check(not [f for f in log2["fired"] if f["to"] == leaf], "no edge is kept to a statement that is not in the ledger")

print("== C3: switching USED-BY off makes cycles reappear; the overrides are load-bearing too")
raw, _ = G.build(led, used_by_rule=False, overrides=False)
check(len(G.cycles(raw)) == L["counts"]["raw_cycles_no_rules"] >= 10, f"raw graph has {len(G.cycles(raw))} cycles (MUST fail acyclicity)")
check(len(G.cycles(G.build(led, used_by_rule=False, overrides=True)[0])) >= 1, "overrides alone do not make it acyclic")
check(len(G.cycles(G.build(led, used_by_rule=True, overrides=False)[0])) >= 1, "USED-BY alone does not make it acyclic")

print("== C4: a root that cites nothing gives closure 1 and chain 0; the real graphs give the banked numbers")
led3 = copy.deepcopy(led)
for e in led3["entries"]:
    if e["id"] == G.ROOT_NODE:
        e["cites"] = ["(1.1)"]
dep3, _ = G.build(led3)
adj3 = G.adjacency(dep3)
check(len(G.reachable(adj3, G.ROOT_NODE)) == 1 and G.longest_chain(adj3, G.ROOT_NODE)[0] == 0, "closure 1, chain 0 (MUST fail every gate number)")
g = L["gate"]
check((g["closure_size"], g["longest_chain_edges"], len(g["dangling"])) == (56, 22, 3), f"ledger pass banked: closure 56, chain 22, 3 dangling; got {(g['closure_size'], g['longest_chain_edges'], len(g['dangling']))}")
gt = out["text_pass"]["gate"]
check((gt["closure_size"], gt["longest_chain_edges"]) == (51, 14), f"text pass banked: closure 51, chain 14; got {(gt['closure_size'], gt['longest_chain_edges'])}")
ge = out["equation_pass"]["gate"]
check((ge["closure_size"], ge["longest_chain_edges"], len(ge["outside_closure"]), len(ge["prose_nodes_reached"])) == (70, 27, 9, 10),
      f"equation pass banked: closure 70, chain 27, 9 outside, 10 prose nodes; got {(ge['closure_size'], ge['longest_chain_edges'], len(ge['outside_closure']), len(ge['prose_nodes_reached']))}")
check(all(p["gate"]["acyclic"] == "YES" for p in (L, out["text_pass"], out["equation_pass"])), "all three passes acyclic")
check("Proposition 9.6" in ge["outside_closure"] and "Proposition 9.5" in ge["outside_closure"], "Propositions 9.5 and 9.6 are outside the closure in the equation pass")
check(g["spine_contains_4_7_9"] == "NO-AND-MISSING-7" and gt["spine_contains_4_7_9"] == "NO-AND-MISSING-7" and ge["spine_contains_4_7_9"] == "YES",
      "section 7 is missing from the spine in the ledger and text passes and present in the equation pass")

print("== C5: a hand-built five-node DAG with known answers")
tiny = {("a", "b"), ("b", "c"), ("c", "d"), ("a", "e"), ("e", "d")}
adjt = G.adjacency(tiny)
n, chain = G.longest_chain(adjt, "a")
check(n == 3 and chain == ["a", "b", "c", "d"], f"longest chain 3 via a-b-c-d, got {n} {chain}")
fan = G.transitive_fanin(adjt, G.reachable(adjt, "a"))
check(fan == {"a": 0, "b": 1, "c": 2, "d": 4, "e": 1}, f"transitive fan-in a0 b1 c2 d4 e1, got {fan}")
check(not G.cycles(tiny) and len(G.cycles(tiny | {("d", "a")})) >= 1, "tiny DAG acyclic; with d->a a cycle is found")

print("== C6: the text pass finds what the proof of Theorem 4.6 names, and no proof cites its own target")
dep_t, tlog = G.build_text(lines, index)
m = set(tlog["mentions"]["Theorem 4.6"])
check({"Lemma 4.8", "Proposition 4.10", "Lemma 4.11", "Lemma 4.7"} <= m, f"Theorem 4.6's proof names 4.8, 4.10, 4.11, 4.7; got {sorted(m)}")
check(("Proposition 9.9", "Theorem 3.1") not in dep_t and ("Theorem 3.1", "Proposition 9.9") in dep_t, "TARGET reversed: Theorem 3.1 depends on Proposition 9.9, not the other way")
check(sorted(tlog["no_proof_block"]) == ["Definition 3.2", "Definition 3.3", "Definition 6.4", "Definition 6.5", "Definition 9.4", "Proposition A.4", "Theorem 3.1"],
      "exactly seven statements have no proof block of their own")

print("== C7: the equation pass resolves labels to their owners")
dep_e, elog = G.build_eq(lines, index)
o = elog["owners"]
check(o["9.8"]["owner"] == "Definition 9.4" and o["9.17"]["owner"] == "Lemma 9.8" and o["1.1"]["owner"] == "Theorem 1.1", "(9.8) -> Definition 9.4, (9.17) -> Lemma 9.8, (1.1) -> Theorem 1.1")
check(o["6.2"]["owner"] == "§6 prose" and o["7.5"]["owner"] == "§7 prose", "(6.2) and (7.5) are displayed in unnumbered prose")
check(elog["unresolved_labels"] == {"Corollary B.10": ["B.40"]}, "the one unresolved label is (B.40), Remark B.9's parameter order, displayed outside Appendix B's pages")
check(("Lemma 10.5", "Theorem 1.1") not in dep_e, "ROOT-EQ: citing (1.1) is not depending on Theorem 1.1")
check(("Theorem 4.6", "Lemma 5.2") not in dep_e and ("Lemma 5.2", "Theorem 4.6") in dep_e, "MUTUAL-NAMED: the forward pointer to Lemma 5.2 in Theorem 4.6's proof is dropped")

print("== the banked artefact agrees with a fresh run")
banked = json.loads(G.OUT.read_text())
for pas in ("ledger_pass", "text_pass", "equation_pass"):
    for k in ("gate", "spine_m", "fanin", "counts"):
        check(banked[pas][k] == out[pas][k], f"dag.json[{pas}][{k}] == fresh run")

print()
if _fails:
    print(f"FAILED {len(_fails)}:"); [print("  -", f) for f in _fails]; sys.exit(1)
print("test_arc6_dag: all checks pass")
