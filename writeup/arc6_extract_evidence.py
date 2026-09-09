"""Arc-6 R1 evidence: the banked extraction is what the journal says it is.

    .venv/bin/python writeup/arc6_extract_evidence.py

Re-hashes the banked outputs against the manifest, re-counts the statement
index against the charter's 79, re-checks that no running header survived, and
checks every number the leg-424 journal quotes. Does NOT re-extract the PDF —
the PDF is gitignored and the point of banking the text is that a reader without
it can still check everything below.
"""
import hashlib, json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "writeup" / "data" / "arc6"
J = re.sub(r"\s+", " ", (ROOT / "experiments" / "journal" / "leg_424.md").read_text())
fail = []
def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok: fail.append(label)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
m = json.loads((D / "extract_manifest.json").read_text())
print("== 1. provenance")
check(m["pdf"]["sha256"] == "0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f", "PDF sha256 is the leg-417 pin")
check(m["pdf"]["bytes"] == 2959204 and m["pdf"]["pages"] == 166, "2,959,204 B, 166 pages")
for f in ("manuscript_pages.jsonl", "manuscript_pages.txt"):
    check(sha(D / f) == m["outputs"][f]["sha256"], f"{f} re-hashes to the manifest", sha(D / f)[:16])
check(m["running_headers_stripped"]["count"] == 165, "165 running headers stripped")
txt = (D / "manuscript_pages.txt").read_text()
check(len(re.findall(r"^[0-9]{1,3} OPENAI$|^FINITE TIME BLOWUP FOR NAVIER.STOKES [0-9]+$", txt, re.M)) == 0, "0 running headers survive")
check(txt.count("<<<PAGE ") == 166, "166 page markers")
recs = [json.loads(l) for l in (D / "manuscript_pages.jsonl").open()]
check(len(recs) == m["outputs"]["manuscript_pages.jsonl"]["records"], "JSONL record count matches manifest", str(len(recs)))
check(all("page" in r and "line" in r and "text" in r for r in recs), "every record carries page, line, text")
check(sorted({r["page"] for r in recs}) == list(range(1, 167)), "every page 1..166 has at least one record")
print("== 2. the gate")
g = m["gate"]
check(g["answer"] == "NO-AND-HERE-IS-THE-DIFF", "strict answer is NO-AND-HERE-IS-THE-DIFF")
n = g["after_named_typographic_normalisations"]
check(n["match"] is True, "after named rules: MATCH")
check(len(n["rules_that_fired"]) == 6, "exactly six rules fired", str(len(n["rules_that_fired"])))
check(n["residual_diff_if_any"] == [], "residual diff is empty")
check(n["sup_and_limsup_limits_present_in_extraction"] is True, "the displaced limits ARE present in the extraction")
check("NO-AND-HERE-IS-THE-DIFF" in J and "six named typographic normalisations" in J, "journal states both halves of the answer")
print("== 3. the statement index vs the charter")
si = json.loads((D / "statement_index.json").read_text())
check(si["count"] == 79, "79 statements", str(si["count"]))
check(si["by_kind"] == si["charter_expectation"]["by_kind"], "by kind = 3/26/38/7/5", str(si["by_kind"]))
check(si["by_section"] == si["charter_expectation"]["by_section"], "by section = charter's", str(si["by_section"]))
ids = [e["id"] for e in si["statements"]]
check(len(set(ids)) == 79, "identifiers are unique")
multi = [e for e in si["statements"] if e["n_lines_starting_with_this_header"] > 1]
check(len(multi) == 11, "eleven identifiers began a line more than once, each banked with its alternatives", str(len(multi)))
check(all(1 <= e["page"] <= 166 for e in si["statements"]) and all(e["page"] not in range(6, 24) or e["section"] in ("1", "3") for e in si["statements"]),
      "no statement outside §§1,3 is placed inside §3's outline pages 6-23")
ov = {e["id"]: e for e in si["statements"] if e["page_chosen_by"].startswith("override")}
check(sorted(ov) == ["Lemma 7.7", "Lemma 8.2"], "exactly two overrides, and they are 7.7 and 8.2", str(sorted(ov)))
check(ov["Lemma 7.7"]["page"] == 86 and ov["Lemma 8.2"]["page"] == 90, "overridden to pp. 86 and 90")
check(all("forward reference" in e["page_chosen_by"] for e in ov.values()), "each override carries its reason")
check("nine of the eleven" in J and "overridden by name" in J, "journal states the 9-by-rule / 2-by-override split")
t11 = [e for e in si["statements"] if e["id"] == "Theorem 1.1"][0]
check(t11["page"] == 1, "Theorem 1.1 is placed on page 1, not at its proof on 117")
for tok in ["79", "165", "599,585", "876,552", "2,959,204"]:
    check(tok in J, f"journal quotes {tok}")
print()
if fail:
    print(f"DRIFT: {len(fail)}"); [print("  -", x) for x in fail]; sys.exit(1)
print("arc6 R1 evidence: all checks pass")
