"""Arc-6 R2 fan-out evidence (leg 428): merged.json is what the journal says it is.

    .venv/bin/python writeup/arc6_merged_evidence.py

Re-runs the merge from the five shard files, compares with the banked merged
ledger, recomputes the four gate clauses, and checks every number the journal
quotes. Never touches ledger.json. Exits nonzero on drift.
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))
import arc6_merge_shards as M  # noqa: E402
J = re.sub(r"\s+", " ", (ROOT / "experiments" / "journal" / "leg_428.md").read_text())
fail = []
def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok: fail.append(label)

banked = json.loads(M.OUT.read_text())
fresh = M.run(write=False, verbose=False)
g, gf = banked["gate"], fresh["gate"]
print("== 1. reproducible")
for k in ("a_all_79", "n_merged", "b_all_nonempty", "c_hard_pages_per_shard", "d_mean_stmt_jaccard", "d_mean_eq_jaccard", "d_lowest_agreement_with_solo"):
    check(g[k] == gf[k], f"gate.{k} re-derives")
check([e["id"] for e in banked["entries"]] == [e["id"] for e in fresh["entries"]], "entry order re-derives")
print("== 2. the gate")
check(g["a_all_79"] and g["n_merged"] == 79 and not g["page_mismatch"], "(a) 79 merged, no page mismatch")
check(g["b_all_nonempty"], "(b) every merged entry non-empty")
shards = banked["shards"]
check({k: v["n_entries"] for k, v in shards.items()} == {"A": 11, "B": 11, "C": 20, "D": 15, "E": 19}, "shard entry counts 11/11/20/15/19")
check(all(v["n_preamble"] == 4 and v["stopped_at_page"] is None for v in shards.values()), "four preamble entries each, nobody stopped early")
check(g["c_hard_pages_per_shard"] == {"A": 6, "B": 6, "C": 8, "D": 5, "E": 8} and sum(g["c_hard_pages_per_shard"].values()) == 33, "(c) hard pages 6/6/8/5/8 = 33")
check((g["d_mean_stmt_jaccard"], g["d_mean_eq_jaccard"]) == (0.744, 0.791), "(d) mean Jaccard 0.744 / 0.791", str((g["d_mean_stmt_jaccard"], g["d_mean_eq_jaccard"])))
p11 = g["d_preamble_five_way"]["Theorem 1.1"]
check(set(p11["stmt_refs_in_all"]) == {"Proposition 10.1", "Lemma 10.3", "Lemma 10.4", "Lemma 10.5", "Theorem 3.1"} and len(p11["stmt_refs_union"]) == 11, "Theorem 1.1: five refs in all five readers, union 11")
check(p11["n_const"]["D"] == 9 and all(v == 4 for k, v in p11["n_const"].items() if k != "D"), "Theorem 1.1 constants 4,4,4,9,4")
p31 = g["d_preamble_five_way"]["Theorem 3.1"]
check(p31["stmt_refs_in_all"] == ["Proposition 9.9"] and set(p31["eq_in_all"]) == {"3.1", "3.2", "3.3", "3.4", "3.5", "3.6"}, "Theorem 3.1: only Proposition 9.9 in all five; (3.1)-(3.6) in all five")
b10 = g["d_corollary_B10_C_vs_E"]
check(b10["stmt_jaccard"] == 1.0 and b10["eq_jaccard"] == 1.0, "Corollary B.10: C and E cite identically")
check(len(banked["could_not_determine"]) == 29, "29 could-not-determine records")
emptyc = [(sh, e["id"]) for sh in ("A", "B", "C", "D") for e in banked["entries"] if e["id"] in ("Definition 3.2", "Definition 3.3") for sh2 in [sh] if not e["other_versions"].get(sh, {}).get("cites") and e["primary_shard"] != sh]
check(len(emptyc) == 8, "the two Definitions have empty cites in shards A-D", str(len(emptyc)))
check(all(e["primary_shard"] == {"Corollary B.10": "E", "Theorem 1.1": "D", "Theorem 3.1": "D", "Definition 3.2": "E", "Definition 3.3": "E"}.get(e["id"], e["primary_shard"]) for e in banked["entries"]), "primary overrides applied")
print("== 3. the journal quotes what the artefact holds")
for tok in ["0.744", "0.791", "33 notes", "29 could-not-determine", "**15**", "**12**", "11 | 4 | 6 | 6", "20 (19 +", "x = 202–261", "UNVERIFIED", "58-node spine"]:
    check(tok in J, f"journal quotes {tok!r}")
print()
if fail:
    print(f"DRIFT: {len(fail)}"); [print("  -", x) for x in fail]; sys.exit(1)
print("arc6 R2 fan-out evidence: all checks pass")
