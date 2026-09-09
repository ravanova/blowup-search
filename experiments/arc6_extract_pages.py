"""Arc 6 R1 (leg 424): per-page extraction of the manuscript with page provenance.

    .venv/bin/python experiments/arc6_extract_pages.py

Reads Papers/openai-navier-stokes.pdf (gitignored; sha256 pinned below and in
writeup/data/arc6_acquire_v1.json), extracts EVERY PAGE SEPARATELY with PyMuPDF,
strips the running headers ("N OPENAI" on even pages, "FINITE TIME BLOWUP FOR
NAVIER–STOKES N" on odd pages -- only when they carry the page number, so the
author line on page 1 survives), and writes

  writeup/data/arc6/manuscript_pages.jsonl   one record per line: {page, line, text}
  writeup/data/arc6/manuscript_pages.txt     the same text with <<<PAGE N>>> markers
  writeup/data/arc6/extract_manifest.json    sha256 of the PDF and of both outputs,
                                             page count, header lines stripped, and
                                             the R1 gate result

Why per page. Naive concatenation corrupts statements that straddle a page
break and injects running headers mid-sentence; Corollary 10.6 (pp. 125-126)
is the demonstrated case. Keeping the page number on every line makes every
later quotation traceable to a page, which is what the ledger in R2 needs.

Nothing here interprets the mathematics. This is provenance.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import pymupdf as fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "Papers" / "openai-navier-stokes.pdf"
OUT = ROOT / "writeup" / "data" / "arc6"
OUT.mkdir(parents=True, exist_ok=True)
PINNED_SHA = "0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f"

HEADER_EVEN = re.compile(r"^\s*\d{1,3}\s+OPENAI\s*$")
HEADER_ODD = re.compile(r"^\s*FINITE TIME BLOWUP FOR NAVIER.STOKES\s+\d{1,3}\s*$")

# Theorem 1.1 as the charter states it, verbatim. The gate compares against this.
CHARTER_THM = (
    "For every ν > 0 there exist a force f ∈ C∞_c(R³×(0,∞); R³), a compact set "
    "K ⊂ R³, and smooth velocity and pressure fields u, p on R³×[0,1) satisfying "
    "∂_t u + (u·∇)u − νΔu + ∇p = f, ∇·u = 0, u(·,0) = 0, "
    "such that supp u(·,t) ∪ supp p(·,t) ⊂ K for every 0 ≤ t < 1, "
    "sup_{0≤t<1} ‖u(t)‖_L²(R³) < ∞, limsup_{t↑1} ‖u(t)‖_L∞(R³) = ∞."
)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    got = sha(PDF)
    if got != PINNED_SHA:
        print(f"PDF sha256 {got} != pinned {PINNED_SHA}; refusing to extract a different file")
        return 2
    doc = fitz.open(PDF)
    records, stripped, txt_parts = [], [], []
    for pno in range(len(doc)):
        page = doc[pno]
        # sorted text with reading order; keep line structure
        text = page.get_text("text", sort=True)
        lines = text.split("\n")
        kept = []
        for ln in lines:
            if HEADER_EVEN.match(ln) or HEADER_ODD.match(ln):
                stripped.append({"page": pno + 1, "text": ln.strip()})
                continue
            kept.append(ln.rstrip())
        # drop trailing blank lines
        while kept and not kept[-1].strip():
            kept.pop()
        txt_parts.append(f"<<<PAGE {pno + 1}>>>")
        for i, ln in enumerate(kept, 1):
            records.append({"page": pno + 1, "line": i, "text": ln})
            txt_parts.append(ln)
    jsonl = OUT / "manuscript_pages.jsonl"
    with jsonl.open("w") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    txt = OUT / "manuscript_pages.txt"
    txt.write_text("\n".join(txt_parts) + "\n")

    # ---- the R1 gate: Theorem 1.1, character for character modulo whitespace
    # locate it in the page-1 records
    p1 = " ".join(r["text"] for r in records if r["page"] == 1)
    i = p1.find("Theorem 1.1.")
    j = p1.find("Consequently", i)
    extracted = p1[i + len("Theorem 1.1."):j].strip()

    def norm(s: str) -> str:
        s = re.sub(r"\s+", "", s)
        return s

    # The PDF text layer renders math as glyph runs; the charter renders it in
    # ASCII-ish TeX. Compare the PROSE words first (a hard, whitespace-only test),
    # then the math tokens, and report every difference rather than a bare NO.
    def words(s: str):
        return re.findall(r"[A-Za-z][A-Za-z,\.]*", s)

    prose_ok = words(extracted) == words(CHARTER_THM)
    exact_ok = norm(extracted) == norm(CHARTER_THM)
    import difflib
    diff = list(difflib.unified_diff(
        [norm(CHARTER_THM)], [norm(extracted)], "charter", "extracted", lineterm="", n=0))
    wdiff = list(difflib.unified_diff(words(CHARTER_THM), words(extracted),
                                      "charter-words", "extracted-words", lineterm="", n=0))

    # ---- the SAME two strings after NAMED typographic normalisations. Each rule
    # is one known difference between a PDF text layer and a TeX transcription,
    # listed so the reader sees exactly what was forgiven and can reject any of it.
    RULES = [
        ("R1 drop the displayed-equation label '(1.1)'", lambda s: s.replace("(1.1)", "")),
        ("R2 superscript digits: R³→R3, L²→L2", lambda s: s.replace("³", "3").replace("²", "2")),
        ("R3 TeX sub/superscript markers '_' '{' '}' removed", lambda s: re.sub(r"[_{}]", "", s)),
        ("R4 Laplacian glyph U+2206 '∆' → U+0394 'Δ'", lambda s: s.replace("∆", "Δ")),
        ("R5 norm bars U+2225 '∥' → U+2016 '‖'", lambda s: s.replace("∥", "‖")),
        ("R6 'lim sup' → 'limsup'", lambda s: s.replace("limsup", "lim sup").replace("lim sup", "limsup")),
        ("R7 sup/limsup limits displaced by layout: strip the subscript limits from BOTH sides",
         lambda s: s.replace("0≤t<1", "").replace("t↑1", "")),
    ]
    a, b = norm(CHARTER_THM), norm(extracted)
    fired = []
    for name, f in RULES:
        a2, b2 = f(a), f(b)
        if (a2, b2) != (a, b):
            fired.append(name)
        a, b = a2, b2
    normalised_ok = (a == b)
    # R7 removes information; check separately that the limits are PRESENT in the
    # extraction, just displaced to the line below (layout), not missing.
    limits_present = ("0≤t<1" in norm(extracted)) and ("t↑1" in norm(extracted))

    # ---- the statement index: every numbered Theorem / Proposition / Lemma /
    # Corollary / Definition, with the page its STATEMENT is printed on. This is
    # R2's denominator and its scaffold, so it is produced here, reproducibly,
    # rather than typed.
    #
    # Header shape: "Kind S.n." or "Kind S.n (Title)." -- the optional title is
    # what a first regex missed (Lemma 6.3, Definitions 6.4/6.5 are titled).
    # A line can also BEGIN with a citation ("Lemma 4.4." bare, or "Theorem 1.1.
    # Rescaling gives ..." which is 'Proof of Theorem 1.1.' wrapped). Statements
    # are distinguished from citations by rule: the statement line is the one
    # followed by statement text (a titled header, or a period then a capital
    # letter beginning a sentence with a hypothesis word), and where two lines
    # both qualify the earlier page is the statement UNLESS it lies in §3's
    # outline (pp. 6-23), whose forward references are prose.
    hdr = re.compile(r"^\s*(Theorem|Proposition|Lemma|Corollary|Definition)\s+([0-9A-C]+)\.(\d+)\s*(\([^)]*\))?\s*\.(.*)$")
    occ: dict = {}
    for r in records:
        m = hdr.match(r["text"])
        if not m:
            continue
        kind, sec, num, title, rest = m.group(1), m.group(2), int(m.group(3)), m.group(4), m.group(5).strip()
        occ.setdefault((kind, sec, num), []).append({"page": r["page"], "line": r["line"],
                                                    "title": (title or "").strip("()") or None,
                                                    "rest": rest[:80]})
    HYP = re.compile(r"^(For|Let|There|Fix|Suppose|Assume|Given|If|The|Each|Every|A|An|In|Under|With|Consider|Define|Denote)\b")
    index = []
    for key in sorted(occ, key=lambda k: (k[1].isalpha(), k[1] if k[1].isalpha() else int(k[1]), k[2])):
        cands = occ[key]
        good = [c for c in cands if c["title"] or HYP.match(c["rest"])]
        good = [c for c in good if not (6 <= c["page"] <= 23)] or good or cands
        c = good[0]
        # Two section-opening forward references defeat the hypothesis-word rule
        # ("Lemma 7.7. The additional velocity terms ..." on p.73 opens §7;
        # "Lemma 8.2. For a source depending on ..." on p.88 opens §8). They are
        # overridden BY NAME with the reason, rather than the rule being tuned
        # until it happens to fit; the evidence script asserts exactly these two.
        OVERRIDES = {("Lemma", "7", 7): (86, "p.73 is §7's opening paragraph, a forward reference"),
                     ("Lemma", "8", 2): (90, "p.88 is §8's opening paragraph, a forward reference")}
        override = None
        if key in OVERRIDES:
            pg, why = OVERRIDES[key]
            c = next(x for x in cands if x["page"] == pg)
            override = why
        index.append({"id": f"{key[0]} {key[1]}.{key[2]}", "kind": key[0], "section": key[1],
                      "number": key[2], "page": c["page"], "line": c["line"], "title": c["title"],
                      "n_lines_starting_with_this_header": len(cands),
                      "page_chosen_by": "override: " + override if override else "rule",
                      "other_line_starts": [(x["page"], x["line"]) for x in cands if x is not c]})
    kinds = {}
    secs = {}
    for e in index:
        kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
        secs[e["section"]] = secs.get(e["section"], 0) + 1
    (OUT / "statement_index.json").write_text(json.dumps(
        {"schema": "arc6_statement_index_v1", "leg": 424, "count": len(index),
         "by_kind": kinds, "by_section": secs,
         "charter_expectation": {"count": 79, "by_kind": {"Theorem": 3, "Proposition": 26, "Lemma": 38, "Corollary": 7, "Definition": 5},
                                 "by_section": {"1": 1, "3": 3, "4": 11, "5": 5, "6": 6, "7": 8, "8": 8, "9": 9, "10": 6, "A": 10, "B": 9, "C": 3}},
         "statements": index}, indent=1, ensure_ascii=False) + "\n")
    print(f"statement index: {len(index)} statements  by kind {kinds}")
    print(f"                 by section {secs}")

    manifest = {
        "schema": "arc6_extract_manifest_v1", "leg": 424, "unit": "R1",
        "pdf": {"path": "Papers/openai-navier-stokes.pdf", "sha256": got,
                "bytes": PDF.stat().st_size, "pages": len(doc)},
        "extractor": {"library": "pymupdf", "version": fitz.VersionBind, "mode": "text, sort=True"},
        "outputs": {
            "manuscript_pages.jsonl": {"sha256": sha(jsonl), "bytes": jsonl.stat().st_size,
                                       "records": len(records)},
            "manuscript_pages.txt": {"sha256": sha(txt), "bytes": txt.stat().st_size},
        },
        "statement_index": {"file": "statement_index.json", "count": len(index), "by_kind": kinds, "by_section": secs},
        "running_headers_stripped": {"count": len(stripped),
                                     "first": stripped[:3], "last": stripped[-2:]},
        "gate": {
            "question": "Does the extracted Theorem 1.1 match the charter's verbatim text, character for character modulo whitespace?",
            "charter_text": CHARTER_THM,
            "extracted_text": extracted,
            "exact_match_modulo_whitespace": exact_ok,
            "prose_words_match": prose_ok,
            "answer": "YES" if exact_ok else "NO-AND-HERE-IS-THE-DIFF",
            "after_named_typographic_normalisations": {
                "match": normalised_ok,
                "rules_that_fired": fired,
                "rules_available": [r[0] for r in RULES],
                "sup_and_limsup_limits_present_in_extraction": limits_present,
                "residual_diff_if_any": (list(difflib.unified_diff([a], [b], "charter", "extracted",
                                                                   lineterm="", n=0))[2:] if not normalised_ok else []),
            },
            "diff_normalised": diff,
            "diff_prose_words": wdiff,
            "reading": (
                "An exact character match is not expected between a PDF text layer and a "
                "TeX-style transcription: the text layer renders C^infty_c as separate glyph "
                "runs, sub/superscripts as adjacent characters, and some operators as private "
                "glyphs. The gate therefore reports BOTH the strict answer and the prose-word "
                "answer, and prints the diff so the reader sees exactly which characters differ."
            ),
        },
    }
    (OUT / "extract_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"pages {len(doc)}  records {len(records)}  headers stripped {len(stripped)}")
    print(f"GATE (strict, modulo whitespace): {manifest['gate']['answer']}")
    print(f"      prose words match          : {prose_ok}")
    print(f"      after {len(fired)} named typographic rules: {'MATCH' if normalised_ok else 'STILL DIFFERS'}")
    for r in fired: print("        fired:", r)
    print(f"      sup/limsup limits present in extraction (displaced by layout): {limits_present}")
    print("extracted Theorem 1.1:\n  " + extracted)
    if not exact_ok:
        print("diff (normalised):")
        for l in diff[2:]:
            print("  " + l[:400])
        print("diff (prose words):", wdiff[2:] if len(wdiff) > 2 else "none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
