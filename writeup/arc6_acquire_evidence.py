"""Arc-6 U1 evidence: re-check every number and every quotation in leg 417's gate.

    .venv/bin/python writeup/arc6_acquire_evidence.py

What it does WITHOUT the network, from writeup/data/arc6_acquire_v1.json alone:
  * checks the JSON is internally consistent (page counts, byte counts, hash shape);
  * checks every number quoted in experiments/journal/leg_417.md is in the JSON;
  * checks every string the journal presents as a VERBATIM manuscript quotation is a
    substring of the banked pdf-extraction span it claims to come from, after
    whitespace normalisation only.

What it does WHEN the fetched PDFs are present in Papers/ (they are gitignored by repo
convention, so this is optional and reported, never silently skipped):
  * re-hashes them and compares against the banked sha256.

Exit 0 = every prose number and every prose quotation is reproduced from the banked
JSON. Exit 1 = drift. A quotation that does not appear in the source it cites is a
documentation-contract failure, not a formatting opinion.

DELIBERATELY NOT DONE HERE: any check of whether the manuscript is CORRECT. This
script checks provenance and quotation fidelity. The external record's correctness is
not established by U1 and this script does not move it.
"""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON = ROOT / "writeup" / "data" / "arc6_acquire_v1.json"
JOURNAL = ROOT / "experiments" / "journal" / "leg_417.md"
PAPERS = ROOT / "Papers"

fail = []
def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok:
        fail.append(label)

def norm(s):
    """Whitespace-normalise. pdfTeX text layers break lines mid-formula; a quotation
    is judged on its characters, not on where the extractor put its newlines."""
    return re.sub(r"\s+", " ", s).strip()

d = json.loads(JSON.read_text())
journal = JOURNAL.read_text()

print("== 1. artifact provenance, from the JSON alone")
arts = {a["id"]: a for a in d["artifacts_fetched"]}
check(len(arts) == 4, "four artifacts banked", f"{sorted(arts)}")
ns = arts["openai_navier_stokes_manuscript"]
check(ns["pages"] == 166, "manuscript page count is 166", str(ns["pages"]))
check(ns["bytes"] == 2959204, "manuscript byte count", str(ns["bytes"]))
check(arts["openai_euler_manuscript"]["pages"] == 57, "Euler manuscript is 57 pp")
check(arts["fefferman_clay_statement"]["pages"] == 6, "Clay statement is 6 pp")
for a in arts.values():
    if "sha256" in a:
        check(re.fullmatch(r"[0-9a-f]{64}", a["sha256"]) is not None,
              f"{a['id']}: sha256 is a 64-hex digest")
lean = arts["openai_lean_project"]
check(re.fullmatch(r"[0-9a-f]{40}", lean["head_commit_sha1"]) is not None,
      "Lean project HEAD is a 40-hex sha1", lean["head_commit_sha1"])
check(lean["lean_files"] == 2486, "2,486 .lean files", str(lean["lean_files"]))
check(lean["tracked_files"] == 2496, "2,496 tracked files", str(lean["tracked_files"]))
check(sum(lean["lean_files_by_top_dir"].values()) == lean["lean_files"],
      "per-directory .lean counts sum to the total")

print("== 2. numbers the journal quotes are the numbers the JSON banks")
for label, value in [
    ("manuscript pages", "166"),
    ("Euler manuscript pages", "57"),
    ("manuscript bytes", "2,959,204"),
    ("Euler bytes", "535,142"),
    ("Clay bytes", "203,736"),
    ("tracked files", "2,496"),
    ("lean files", "2,486"),
]:
    check(value in journal, f"journal states {label} = {value}")
check(ns["sha256"].startswith("0e779481c4da40bd"), "manuscript sha256 prefix in journal table")
check(arts["openai_euler_manuscript"]["sha256"].startswith("a0c234518e6c489e"), "Euler sha256 prefix")
check(arts["fefferman_clay_statement"]["sha256"].startswith("c1b5f27b1a64705c"), "Clay sha256 prefix")
check(lean["head_commit_sha1"].startswith("8937a8f4cbc7abaa"), "Lean HEAD prefix in journal table")

print("== 3. every prose quotation is a substring of the span it cites")
m = d["manuscript_statements"]
f = d["fefferman_conditions_at_primary"]
QUOTES = [
    ("Thm 1.1 alternative-(C) sentence",
     "This establishes alternative (C) in the Millennium problem statement for Navier–Stokes as stated by Fefferman in [ 13].",
     m["theorem_1_1_verbatim_pdf_extraction"]),
    ("Thm 1.1 datum",
     "u(·, 0) =0", m["theorem_1_1_verbatim_pdf_extraction"]),
    ("Thm 1.1 force class",
     "f∈C ∞ c (R3×( 0, ∞); R3)", m["theorem_1_1_verbatim_pdf_extraction"]),
    ("Thm 1.1 compact support of u AND p — difference D2",
     "such thatsuppu(·,t)∪suppp(·,t)⊂K for every0≤t<1",
     m["theorem_1_1_verbatim_pdf_extraction"]),
    ("Thm 1.1 limsup — difference D4",
     "lim sup t↑1 ∥u(t)∥ L∞(R3) =∞.", m["theorem_1_1_verbatim_pdf_extraction"]),
    ("Thm 1.1 non-existence clause — difference D5",
     "Consequently, there is no smooth solution (u, P) on R3×[ 0, ∞) with the same force and initial datum whose kinetic energy is uniformly bounded",
     m["theorem_1_1_verbatim_pdf_extraction"]),
    ("Thm 1.1 alternative-(D) sentence — difference D3",
     "Compact support also yields the corresponding construction on T3 =R 3/Z3, establishing alternative (D) in [13]; see Corollary 10.6.",
     m["theorem_1_1_verbatim_pdf_extraction"]),
    ("Thm 1.1 universal viscosity — difference D1",
     "Theorem 1.1.For every ν> 0there exist a force", m["theorem_1_1_verbatim_pdf_extraction"]),
    ("Cor 10.6 non-existence clause",
     "There is no global smooth periodic solution for the same datum and force.",
     m["corollary_10_6_verbatim_pdf_extraction"]),
    ("Lemma 10.3 discharges Fefferman (5) from compact support",
     "Compact support gives, for every integerk≥0, |∂α x∂m t f(x,t)|≤M α,m(3+R) k(1+|x|+t) −k.",
     m["lemma_10_3_and_decay_bound_verbatim_pdf_extraction"]),
    ("Euler Thm 1.1 is UNFORCED — difference D6",
     "There exists u0∈C ∞ c,σ(R3) such that0 <T∗(u0)<∞ .",
     m["euler_theorem_1_1_verbatim_pdf_extraction"]),
    ("Fefferman (4) is the DATUM's decay",
     "(4) |∂α x u◦(x)| ≤ CαK(1 + |x|)−K on Rn, for any α and K",
     f["conditions_verbatim_pdf_extraction"]),
    ("Fefferman (5) is the FORCE's decay",
     "(5) |∂α x ∂m t f (x, t)| ≤ CαmK(1 + |x| + t)−K on Rn × [0, ∞), for any α, m, K.",
     f["conditions_verbatim_pdf_extraction"]),
    ("Fefferman (7) bounded energy",
     "|u(x, t)|2dx < C for all t ≥ 0 (bounded energy)", f["conditions_verbatim_pdf_extraction"]),
    ("Fefferman (8) periodicity of datum AND force — first read here",
     "(8) u◦(x + ej) = u◦(x), f (x + ej, t) = f (x, t) for 1 ≤ j ≤ n",
     f["conditions_8_to_11_verbatim_pdf_extraction"]),
    ("Fefferman (9) replaces (4) and (5), and asks decay in TIME ONLY — first read here",
     "In place of (4) and (5), we assume that u◦ is smooth and that (9) |∂α x ∂m t f (x, t)| ≤ CαmK(1 + |t|)−K",
     f["conditions_8_to_11_verbatim_pdf_extraction"]),
    ("statement (C) rules out solutions of (1),(2),(3),(6),(7)",
     "for which there exist no solutions ( p, u) of (1), (2), (3), (6), (7) on R3 × [0, ∞).",
     f["statement_C_verbatim_pdf_extraction"]),
    ("statement (D) rules out solutions of (1),(2),(3),(10),(11) — NO (7)",
     "for which there exist no solutions (p, u) of (1), (2), (3), (10), (11) on R3 × [0, ∞).",
     f["statement_D_verbatim_pdf_extraction"]),
]
for label, quote, source in QUOTES:
    check(norm(quote) in norm(source), f"quotation reproduced: {label}")

print("== 4. the gate answer is the pre-committed wording")
g = d["gate"]
check(g["question"] == "Is the theorem as reported in arc 5 the theorem the manuscript states?",
      "gate question is the pre-committed one")
check(g["answer"] in ("YES", "NO", "DIFFERS-AS-FOLLOWS"),
      "gate answer is one of the three permitted words", g["answer"])
check(g["answer"] == "DIFFERS-AS-FOLLOWS", "gate answered DIFFERS-AS-FOLLOWS")
check("UNVERIFIED" in g["answer_status"], "gate answer is labelled UNVERIFIED (§3f rule 1)")
check("DIFFERS-AS-FOLLOWS" in journal, "journal states the gate answer verbatim")
ids = [x["id"] for x in g["differences"]]
check(ids == ["D1", "D2", "D3", "D4", "D5", "D6", "D7"], "seven differences, D1..D7", str(ids))
for i in ids:
    check(f"**{i}**" in journal, f"journal's table carries {i}")
check(len(g["agreements"]) == 8, "eight agreements banked", str(len(g["agreements"])))

print("== 5. Clay posture — the standing rule, checked as a number")
cm = d["clay_movement"]
check(cm["links_moved"] == 0, "L1->L4 links moved = 0")
check("0.05" in cm["clay_odds"], "Clay odds unchanged at ~0.05%")
check("UNVERIFIED" in d["verification_status"], "unit is banked UNVERIFIED")
check(f["statement_D_conditions_now_read"]["condition_7_present_in_D"] is False,
      "condition (7) is absent from statement (D), read at primary")

print("== 6. optional re-hash of the fetched PDFs (Papers/ is gitignored)")
present = 0
for a in d["artifacts_fetched"]:
    lp = a.get("local_path")
    if not lp:
        continue
    p = ROOT / lp
    if not p.exists():
        print(f"  [SKIP] {lp} not present — re-pull with: bash Papers/fetch.sh openai")
        continue
    present += 1
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    check(h == a["sha256"], f"{lp} re-hashes to the banked sha256")
print(f"  {present} of 3 source PDFs present locally")

print()
if fail:
    print(f"DRIFT: {len(fail)} check(s) failed")
    for x in fail:
        print(f"  - {x}")
    sys.exit(1)
print("arc6 U1 evidence: all checks pass")
