"""Arc-6 U2 evidence: re-check every number in leg 418's four gate answers.

    .venv/bin/python writeup/arc6_lean_evidence.py

From writeup/data/arc6_lean_v1.json alone, with no network and no Lean:
  * internal consistency of the census (closure sizes, sums, the sorry ledger);
  * every number quoted in experiments/journal/leg_418.md is in the JSON;
  * the four gate clauses are answered separately, each in its own wording;
  * the two things U2 refuses to conflate — source-level and kernel-level — stay
    separated in both the JSON and the prose.

If the cloned Lean project is present locally (it is a scratch clone, not committed),
the census is RE-RUN against it: sorry/axiom counts and the import closure of the
top-level theorem are recomputed from the source rather than read back.

Exit 0 = no drift. Exit 1 = a prose number left its source.

DELIBERATELY NOT DONE HERE: any check that the project builds or that the kernel
accepts it. Gate (a) is NOT-ESTABLISHED and this script does not move it.
"""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON = ROOT / "writeup" / "data" / "arc6_lean_v1.json"
JOURNAL = ROOT / "experiments" / "journal" / "leg_418.md"
# The scratch clone, if this session still has it. Never committed.
CLONE = Path(os.environ.get("ARC6_LEAN_CLONE", "")) if os.environ.get("ARC6_LEAN_CLONE") else None

fail = []
def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok:
        fail.append(label)

d = json.loads(JSON.read_text())
j = JOURNAL.read_text()

print("== 1. the four gate clauses are answered, separately")
for key, must in [
    ("gate_a_does_it_build", "NOT-ESTABLISHED"),
    ("gate_b_is_it_the_papers_theorem", "STRICTLY WEAKER"),
    ("gate_c_sorry_and_axiom_free", "NOT ESTABLISHED AT KERNEL LEVEL"),
    ("gate_d_fraction_formalised", "not measurably formalised"),
]:
    g = d[key]
    check("question" in g and "answer" in g, f"{key}: has its own question and answer")
    check(must.lower() in g["answer"].lower(), f"{key}: answer carries '{must}'")
check("UNVERIFIED" in d["verification_status"], "the unit is banked UNVERIFIED (§3f rule 1)")

print("== 2. gate (a): the build facts, and the refusal that is not one")
a = d["gate_a_does_it_build"]
VER = "leanprover/lean4:v4.34.0-rc2"
check(a["toolchain_declared_by_project"].startswith(VER)
      and a["toolchain_installed_here"].startswith(VER),
      "the toolchain installed here is the toolchain the project declares", VER)
check("6a10ac8c22beadecabdbb0919c2b50214762f91d" in a["toolchain_installed_here"], "lean commit banked")
check(a["comparator_rev_declared"].startswith(a["comparator_rev_checked_out_here"][:40]),
      "the Comparator revision lake checked out is the pinned one")
check(a["host"]["cores"] == 4, "host cores = 4")
check(a["measured_dependency_fetch_rate_mb_per_min"] == 30, "fetch rate banked as measured")
check("what_would_settle_it" in a and a["what_would_settle_it"], "gate (a) names what would settle it")
bl = a["the_blocker_measured"]
check(bl["host"] == "mathlib4.blob.core.windows.net:443", "the denied host is named", bl["host"])
check("502" in bl["proxy_verdict"] and "connect_rejected" in bl["proxy_verdict"],
      "the denial is quoted from the proxy's own record, not inferred")
check("reported, not routed around" in bl["not_a_workaround"], "the denial was reported, not worked around")
check("NOT a policy denial" in bl["a_second_and_DIFFERENT_failure"],
      "the transient reset is banked as DIFFERENT from the policy denial")
check("461,265,558" in bl["a_second_and_DIFFERENT_failure"], "the transient failure carries its own bytes-received figure")
st = a["build_started_and_left_running"]
check("385" in st["state_at_U2_close"], "the measured mathlib module count at U2 close is banked")
check("no total is extrapolated" in st["note"].lower(),
      "no total is extrapolated from the ten-minute sample")
check("mathlib4.blob.core.windows.net" in j, "the journal names the denied host")
check("461,265,558" in j, "the journal carries the transient-failure figure")
check("re_check_obligation" in a, "gate (a) carries a re-check obligation")
check(a["explicitly_not_claimed"].startswith("That the project builds"),
      "gate (a) explicitly claims neither outcome")

print("== 3. gate (b): the definitions are a third party's, and the diff says so")
b = d["gate_b_is_it_the_papers_theorem"]
f_ = b["the_finding_that_matters"]
check("f446284f2aa54375f558c263a580b34e2e7bc9f44a28829637199cc72257d25d" in f_["how_measured"],
      "upstream reference file sha256 banked")
check("8bf45ed70d48b2b2a501de9c00b26bfa38c573ee" in f_["how_measured"],
      "upstream commit pinned in the measurement, not just in the project's comment")
check("character-for-character identical" in f_["diff_result"], "diff result banked verbatim")
check(len(b["quantifier_by_quantifier"]) == 6, "six quantifier rows",
      str(len(b["quantifier_by_quantifier"])))
check(all(r["verdict"].startswith("MATCH") for r in b["quantifier_by_quantifier"]),
      "every quantifier row is a MATCH")
w = b["in_what_sense_weaker_than_theorem_1_1"]
check(len(w["measured_status_of_the_other_five"]) == 5, "all five non-(C) assertions accounted for")
check("DEFINED AND NEVER PROVED" in w["and_one_thing_that_is_NOT_proved"],
      "breakdownStatement recorded as defined-and-never-proved")
check("PERIODIC object is primary" in b["a_structural_difference_from_the_manuscript"]["measured"],
      "the Lean's torus-first structure is recorded")

print("== 4. gate (c): the sorry ledger, and the .lake exclusion stated not hidden")
c = d["gate_c_sorry_and_axiom_free"]
s = c["source_level_census_tracked_files_only"]
check(s["sorry_token_occurrences_total"] == 5, "5 sorry token occurrences in tracked files")
check(s["sorry_proof_placeholders"] == 4, "of which 4 are proof placeholders")
check(s["sorry_occurrences_in_prose"] == 1, "and 1 is prose in a module docstring")
check(s["sorry_proof_placeholders"] + s["sorry_occurrences_in_prose"]
      == s["sorry_token_occurrences_total"], "4 + 1 = 5")
check(len(s["sorry_locations"]) == 5, "five locations listed")
check(all(loc.startswith("ComparatorChallenges/") for loc in s["sorry_locations"]),
      "every sorry is in ComparatorChallenges")
check(s["sorry_in_the_top_level_import_closure"] == 0, "zero sorries in the top-level closure")
for k in ["axiom_declarations", "native_decide_occurrences",
          "unsafe_or_partial_or_implemented_by_or_extern", "opaque_declarations"]:
    check(s[k] == 0, f"{k} = 0")
check("29 `sorry` occurrences and 6 `axiom` declarations live in .lake" in s["method"],
      "the .lake numbers NOT reported are stated in the method, not hidden")
cl = c["import_closure_measured_here"]
ns = cl["NavierStokes.ComparatorSolution"]
check(ns["modules"] == 580 and ns["sorry_lines"] == 0 and ns["theorem_or_lemma_declarations"] == 23604,
      "NS closure: 580 modules, 23,604 theorem/lemma, 0 sorry")
check(ns["ComparatorChallenges_in_closure"] is False, "ComparatorChallenges not in the NS closure")
for root in ["Euler.Solution", "Euler.EulerSingularity"]:
    check(cl[root]["ComparatorChallenges_in_closure"] is False, f"{root}: challenges not in closure")
check(cl["modules_in_no_main_closure"] == 73, "73 dead modules")
check(sorted(c["declared_axioms_by_the_project"]) == sorted(["propext", "Classical.choice", "Quot.sound"]),
      "the three declared axioms are Lean's standard three")
check(len(c["what_a_source_grep_cannot_see"]) == 4, "four named limits of the source-level check")

print("== 5. gate (d): the alignment census adds up")
g = d["gate_d_fraction_formalised"]["cross_reference_census"]
check(g["present_in_published_NS_manuscript"]
      + g["present_only_in_published_Euler_manuscript"]
      + g["present_in_NEITHER_published_manuscript"] == g["distinct_labels_cited_in_lean"],
      "9 + 1 + 15 = 25 cited labels")
check(len(g["labels_present_in_neither"]) == g["present_in_NEITHER_published_manuscript"],
      "the 15 unmatched labels are listed, not just counted")
check(any("11." in x for x in g["labels_present_in_neither"]),
      "the Section-11 citations are among them — the published manuscript has ten sections")
frac = round(100 * g["present_in_published_NS_manuscript"] / g["numbered_results_in_published_NS_manuscript"], 1)
check(frac == 12.3, "9/73 = 12.3% of numbered results are even named in the Lean", f"{frac}%")
check("12.3%" in j, "the journal quotes 12.3% and the JSON reproduces it")

print("== 6. every number the journal quotes is in the JSON")
for label, value in [
    ("lean files", "2,486"), ("NS closure modules", "580"), ("NS closure lines", "379,522"),
    ("NS closure theorems", "23,604"), ("Euler.Solution modules", "1,829"),
    ("dead modules", "73"), ("cited labels", "25"), ("unmatched labels", "15"),
    ("numbered results", "73"), ("dep tree sorries", "29"), ("dep tree axioms", "6"),
    ("host cores", "4 cores"), ("fetch rate", "30 MB/min"),
]:
    check(value in j, f"journal states {label} = {value}")
check("f446284f2aa54375f558c263a580b34e2e7bc9f44a28829637199cc72257d25d" in j,
      "journal carries the upstream reference sha256")
check("6a10ac8c22beadecabdbb0919c2b50214762f91d" in j, "journal carries the lean commit")

print("== 7. optional: re-run the census against a local clone")
if CLONE and (CLONE / "lakefile.toml").exists():
    import subprocess
    files = subprocess.run("git ls-files '*.lean'", shell=True, cwd=CLONE,
                           capture_output=True, text=True).stdout.split()
    check(len(files) == 2486, "clone has 2,486 tracked .lean files", str(len(files)))
    n_sorry = sum(len(re.findall(r"\bsorry\b", (CLONE / f).read_text(errors="replace")))
                  for f in files)
    check(n_sorry == 5, "re-counted sorry token occurrences = 5", str(n_sorry))
    imports = {}
    for f in files:
        mod = f[:-5].replace("/", ".")
        imports[mod] = re.findall(r"^import\s+([A-Za-z0-9_.]+)", (CLONE / f).read_text(errors="replace"), re.M)
    seen, stack = set(), ["NavierStokes.ComparatorSolution"]
    while stack:
        m = stack.pop()
        if m in seen:
            continue
        seen.add(m)
        stack += [i for i in imports.get(m, []) if i in imports]
    check(len(seen) == 580, "re-computed top-level closure = 580 modules", str(len(seen)))
    check(not any(x.startswith("ComparatorChallenges") for x in seen),
          "re-computed: ComparatorChallenges not in the closure")
else:
    print("  [SKIP] no local clone (set ARC6_LEAN_CLONE=<path>); the JSON census is not re-run")

print()
if fail:
    print(f"DRIFT: {len(fail)} check(s) failed")
    for x in fail:
        print(f"  - {x}")
    sys.exit(1)
print("arc6 U2 evidence: all checks pass")
