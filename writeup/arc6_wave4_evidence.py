"""Arc-6 wave 4 evidence (leg 433): wave4/merged.json is what the journal says it is.

    .venv/bin/python writeup/arc6_wave4_evidence.py

Re-runs the merge from the five agent files, compares with the banked merge, checks the
pre-committed rule of leg_433_prereg.md §3 (a gate the adversary faked is NOT EVIDENCE whatever
the worker said), and checks every status the journal quotes. Exits nonzero on drift.
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))
import arc6_wave4_merge as M  # noqa: E402
J = re.sub(r"\s+", " ", (ROOT / "experiments" / "journal" / "leg_433.md").read_text())
fail = []
def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok: fail.append(label)

A = {k: json.loads((M.WD / f).read_text()) for k, f in M.FILES.items() if (M.WD / f).exists()}
banked = json.loads(M.OUT.read_text()); fresh = M.run(write=False, verbose=False)
print("== 1. five files, one author each")
check(sorted(A) == [3, 4, 5, 6, 7], "agents 3–7 present", str(sorted(A)))
check(all(a.get("schema") == "arc6_wave4_v1" and a.get("leg") == 433 and a.get("agent") == k for k, a in A.items()), "schema arc6_wave4_v1, leg 433, agent numbers")
check(all("Tier 2, not a proof" in json.dumps(a) for a in A.values()), "every file carries 'This is Tier 2, not a proof'")
check(all(a.get("could_not_determine") is not None for a in A.values()), "every file lists what it could not determine")
check(all(A[k].get("claimed") for k in (3, 4, 5, 6)), "every worker wrote a `claimed` block")
check(banked == json.loads(json.dumps(fresh, ensure_ascii=False)), "merged.json re-derives from the five files")
print("== 2. the pre-committed rule")
et = banked["evidence_table"]
check(sorted(et) == sorted(g for gs in M.GATES.values() for g in gs), "twelve gates in the evidence table")
for gid, r in et.items():
    faked = r["adversary"].upper().startswith("FAKEABLE")
    check((r["status"].startswith("NOT EVIDENCE") == faked), f"{gid}: status follows the rule (worker {r['worker']}, adversary {r['adversary']})")
check(banked["adversary"].get("X2"), "the adversary wrote its verdict paragraph X2")
print("== 3. the journal quotes the table")
for gid, r in et.items():
    check(gid in J and r["worker"] in J, f"journal names {gid} and the worker's answer {r['worker']!r}")
for tok in ["NOT EVIDENCE", "FAKEABLE", "Tier 2, not a proof", "UNVERIFIED", str(banked["counts"]["faked"]), str(banked["counts"]["workers_YES"])]:
    check(tok in J, f"journal quotes {tok!r}")
if fail:
    print(f"DRIFT: {len(fail)}"); [print("  -", x) for x in fail]; sys.exit(1)
print("arc6 wave 4 evidence: all checks pass")
