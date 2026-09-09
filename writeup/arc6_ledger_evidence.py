"""Arc-6 R2 evidence: the statement ledger is what the leg-425 journal says it is.

    .venv/bin/python writeup/arc6_ledger_evidence.py

Re-computes the R2 gate from the banked ledger rather than trusting the journal:
(a) one entry per statement in statement_index.json, (b) every entry carries
non-empty hypotheses, conclusion and dependencies, (c) the hardest pages are
named with a reason and lie inside the manuscript. Then it checks every number
the journal quotes, and one thing the journal does NOT claim but R3 will lean
on: every statement-to-statement citation in the ledger resolves to a statement
in the index (no dangling cross-reference). It exits nonzero on any drift.
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "writeup" / "data" / "arc6"
sys.path.insert(0, str(ROOT / "experiments"))
from arc6_ledger import validate, REQ  # noqa: E402
J = re.sub(r"\s+", " ", (ROOT / "experiments" / "journal" / "leg_425.md").read_text())
fail = []
def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok: fail.append(label)

led = json.loads((D / "ledger.json").read_text())
si = json.loads((D / "statement_index.json").read_text())
idx = {s["id"]: s for s in si["statements"]}
E = led["entries"]
CHARTER_KIND = {"Theorem": 3, "Proposition": 26, "Lemma": 38, "Corollary": 7, "Definition": 5}
CHARTER_SEC = {"1": 1, "3": 3, "4": 11, "5": 5, "6": 6, "7": 8, "8": 8, "9": 9, "10": 6, "A": 10, "B": 9, "C": 3}

print("== 1. the gate, recomputed")
ga, gb, problems, absent = validate(led, verbose=False)
check(ga, "(a) every one of the 79 indexed statements has exactly one entry", f"{len(E)} entries, absent {absent}")
check(gb and not problems, "(b) every entry has non-empty hypotheses, conclusion and dependencies", "; ".join(problems[:3]))
check(all(k in e for e in E for k in REQ), "every entry carries all nine charter fields")
hp = led["hard_pages"]
check(len(hp) == 13, "(c) thirteen hard-page notes", str(len(hp)))
check(all(h["why"].strip() and len(h["why"]) > 200 for h in hp), "every hard-page note gives a reason of substance (>200 chars)")
pages_ok = True
for h in hp:
    for a, b in re.findall(r"(\d+)-(\d+)", h["pages"]):
        pages_ok &= 1 <= int(a) <= int(b) <= 166
check(pages_ok, "every hard-page range lies inside pages 1..166")
check(led["cursor"]["read_through_page"] == 166, "cursor at page 166: the read is complete", str(led["cursor"]))
check(led["cursor"]["sections_done"] == ["1-2", "3", "4", "5", "6", "7", "8", "9", "10", "A", "B", "C"], "all twelve section passes recorded in order")

print("== 2. the ledger against the charter's counts")
kinds = {}; secs = {}
for e in E:
    kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
    secs[e["section"]] = secs.get(e["section"], 0) + 1
check(kinds == CHARTER_KIND, "by kind = 3/26/38/7/5", str(kinds))
check(secs == CHARTER_SEC, "by section = charter's", str(secs))
check(all(e["page"] == idx[e["id"]]["page"] for e in E), "every entry's page equals the index page")
check(all(e["kind"] == e["id"].split()[0] for e in E), "kind agrees with the identifier")
check(all(e["section"] == e["id"].split()[1].split(".")[0] for e in E), "section agrees with the identifier")

print("== 3. the dependency graph R3 will build on")
pat = re.compile(r"\b(Theorem|Proposition|Lemma|Corollary|Definition)\s+([0-9]{1,2}|[ABC])\.(\d+)\b")
edges, dangling, eqs = set(), set(), set()
for e in E:
    for c in e["cites"]:
        for m in pat.finditer(c):
            t = f"{m.group(1)} {m.group(2)}.{m.group(3)}"
            (edges if t in idx else dangling).add((e["id"], t))
        for m in re.finditer(r"\(([0-9ABC]+\.\d+)\)", c):
            eqs.add(m.group(1))
check(not dangling, "no statement-to-statement citation dangles", str(sorted(dangling))[:120])
check(len(edges) == 196, "196 statement-to-statement edges", str(len(edges)))
check(len(eqs) == 304, "304 distinct displayed-equation labels cited", str(len(eqs)))
check(all(a != b for a, b in edges), "no statement cites itself")
ncites = sum(len(e["cites"]) for e in E); nhyp = sum(len(e["hypotheses"]) for e in E); ncon = sum(len(e["constants"]) for e in E)
check((ncites, nhyp, ncon) == (696, 158, 270), "696 citation strings, 158 hypothesis strings, 270 constant strings", str((ncites, nhyp, ncon)))
noconst = sorted(e["id"] for e in E if not e["constants"])
check(noconst == ["Definition 3.2", "Definition 3.3"], "exactly two entries carry no constants, both Definitions", str(noconst))

print("== 4. the journal quotes what the ledger holds")
for tok in ["79", "196", "304", "696", "158", "270", "thirteen", "166", "Definition 3.2", "Definition 3.3"]:
    check(tok in J, f"journal quotes {tok!r}")
check("UNVERIFIED" in J, "journal marks its own gate answers UNVERIFIED (§3f rule 1)")
for pg in ["107–111", "74–77", "129–137"]:
    check(pg in J, f"journal names pp. {pg} among the hardest")
nbytes = (D / "ledger.json").stat().st_size
check(f"{nbytes:,}" in J, f"journal quotes the ledger size {nbytes:,} B")
print()
if fail:
    print(f"DRIFT: {len(fail)}"); [print("  -", x) for x in fail]; sys.exit(1)
print("arc6 R2 evidence: all checks pass")
