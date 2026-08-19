"""Leg 411 / `PB1` -- EVIDENCE CHECKS for the P1 novelty gate.

`writeup/CORRECTIONS.md` Sec 45: 32 of 49 evidence scripts in this repo CANNOT DETECT AN
ERROR SHARED BETWEEN AN ARTEFACT AND ITS OWN CHECKER.  So `N/N passed` is not evidence
and THIS SCRIPT NEVER PRINTS IT AS ONE.  Sec 46b: a check that ASSERTS a claim instead of
VERIFYING a number fails in both directions -- it passes when the claim is wrong and it
fails when the claim is right but phrased differently.

Every check below therefore carries its CLASS, printed beside it, on every run:

  [P] recompute-from-primary  -- goes back to the PDF, the hash, or the live endpoint and
                                RECOMPUTES.  This class CAN catch a shared error, because
                                the primary source is not part of the artefact.
  [O] re-read-own-artefact    -- reads only this leg's own JSON/markdown.  Catches
                                transcription and internal inconsistency AND NOTHING MORE.
                                A [O] pass is NOT evidence that the claim is true.

The two classes are tallied SEPARATELY and the summary refuses to add them together.

The primary sources are PDFs under `Papers/`, which is GITIGNORED BY POLICY (copyrighted).
In a checkout where they are absent, the [P] checks report `UNRESOURCED` -- which is NOT a
pass and is NOT a failure and is NEVER counted as either.  That is the whole point of the
distinction: an under-resourced check is not a null result.

    .venv/bin/python experiments/p1_novelty_v1_evidence.py
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "Papers"
FT = ROOT / "writeup" / "data" / "p1_novelty_fulltext_v1.json"
MD = ROOT / "writeup" / "data" / "p1_novelty_v1.json"
NOVELTY = ROOT / "writeup" / "papers" / "P1_SELECTION_BIAS" / "NOVELTY.md"
MANIFEST = PAPERS / "MANIFEST.md"

RESULTS: list[tuple[str, str, str, str]] = []   # (class, id, status, detail)


def record(cls: str, cid: str, status: str, detail: str) -> None:
    RESULTS.append((cls, cid, status, detail))
    print(f"  [{cls}] {cid:<34} {status:<12} {detail}")


def norm(s: str) -> str:
    return " ".join(s.split())


def pages_of(pdf: Path, layout: bool = False) -> list[str] | None:
    cmd = ["pdftotext"] + (["-layout"] if layout else []) + [str(pdf), "-"]
    try:
        out = subprocess.run(cmd, capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return out.stdout.decode("utf-8", "replace").split("\f")


# ---------------------------------------------------------------- [P] checks

def check_quotes_are_on_the_pages_claimed(ft: dict) -> None:
    """[P] THE ANTI-FABRICATION CHECK.  For every banked probe hit, re-extract the PDF and
    verify the quote string ACTUALLY OCCURS on the PDF page the artefact names.

    This is the check that matters most in this leg.  FINDINGS.md F8 records that the
    output channel silently drops words from long displayed strings, so a quote that was
    read on screen and retyped can be a sentence the source does not contain.  This check
    goes back to the PDF and recomputes; it does not ask the JSON whether the JSON is right.
    """
    total = ok = missing_pdf = mismatch = 0
    bad: list[str] = []
    cache: dict[str, list[str] | None] = {}
    docmap = {c["id"]: c["file"] for c in ft["corpus"]}
    for probe in ft["probes"]:
        for hit in probe["hits"]:
            total += 1
            fn = docmap.get(hit["doc"])
            if fn is None:
                bad.append(f"{hit['doc']}: not in corpus manifest")
                mismatch += 1
                continue
            if fn not in cache:
                cache[fn] = (pages_of(PAPERS / fn, layout=True), pages_of(PAPERS / fn))
            lay, plain = cache[fn]
            if lay is None and plain is None:
                missing_pdf += 1
                continue
            idx = hit["pdf_page"] - 1
            want = norm(hit["quote"])
            found = False
            for pages in (lay, plain):
                if pages is None or not (0 <= idx < len(pages)):
                    continue
                if want in norm(pages[idx]):
                    found = True
                    break
            # a two-column paper can put one sentence across a page split under one
            # extraction mode and not the other; the CLAIM is "this text is on this page
            # of this paper", so both modes are tried and a hit in either is a hit.
            if found:
                ok += 1
            else:
                mismatch += 1
                bad.append(f"{hit['doc']} p{hit['pdf_page']}: {want[:60]!r}")
    if missing_pdf == total:
        record("P", "quotes_on_claimed_pages", "UNRESOURCED",
               f"{total} banked quotes; Papers/ absent (gitignored) -- NOT a pass, NOT a fail")
        return
    detail = f"{ok}/{total - missing_pdf} re-extracted quotes found on the exact page claimed"
    if missing_pdf:
        detail += f"; {missing_pdf} unresourced"
    if mismatch:
        detail += f"; MISMATCHES: {bad[:4]}"
    record("P", "quotes_on_claimed_pages", "FAIL" if mismatch else "PASS", detail)


def check_ck_table1_numbers() -> None:
    """[P] RECOMPUTE Chandler & Kerswell Table 1 from the PDF.

    FINDINGS.md F3 claims leg 358's `7/163` is confirmed at full text and that
    `SOURCES.md` row 25's depth register is therefore wrong.  That claim is worth exactly
    as much as this recomputation.  The check extracts the Series A Re=60 rows (e,f,g) and
    the Series B Re=60 row (p) and compares the guess/convergence counts to the numbers
    the artefacts quote.  It VERIFIES NUMBERS; it does not assert that the paper says
    something.
    """
    pages = pages_of(PAPERS / "1207.4682.pdf")
    if pages is None:
        record("P", "ck_table1_recompute", "UNRESOURCED",
               "Papers/1207.4682.pdf absent (gitignored) -- NOT a pass, NOT a fail")
        return
    # `pdftotext` renders Table 1 COLUMN-MAJOR: the Re=60 block of Series A appears as the
    # run labels, then the four parameter columns, then the guess column, then the
    # convergence column.  Verified against the `-layout` rendering, which puts the same
    # numbers in row order -- both are checked, so a single extraction quirk cannot pass it.
    flat_plain = norm("\f".join(pages))
    lay = pages_of(PAPERS / "1207.4682.pdf", layout=True)
    flat_lay = norm("\f".join(lay)) if lay else ""
    fails = []
    # Series A, Re = 60, runs e/f/g: 102/104/78 guesses -> 64/67/58 convergences
    if not re.search(r"Re = 60 e f g .{0,60}?102 104 78 64 67 58", flat_plain):
        fails.append("Series A Re=60 e/f/g did not reproduce as 102 104 78 -> 64 67 58 "
                     "in the column-major extraction")
    # Series B, Re = 60, run p: 163 guesses -> 7 convergences
    if not re.search(r"Re = 60 p 0\.30 0\.003 3 . 105 163 7", flat_plain):
        fails.append("Series B Re=60 run p did not reproduce as 163 -> 7 "
                     "in the column-major extraction")
    if flat_lay and not re.search(r"p 0\.30 0\.003 3 . 105 163 7", flat_lay):
        fails.append("Series B Re=60 run p did not reproduce in the -layout extraction")
    if fails:
        record("P", "ck_table1_recompute", "FAIL", "; ".join(fails))
    else:
        record("P", "ck_table1_recompute", "PASS",
               "Table 1 reproduces from the PDF in BOTH extraction modes: Series A Re=60 "
               "e/f/g 102/104/78 guesses -> 64/67/58 convergences; Series B Re=60 run p "
               "163 guesses -> 7 convergences (leg 358's 7/163 = 4.3% CONFIRMED from primary)")


def check_manifest_hashes() -> None:
    """[P] Re-hash every PDF named in the leg-411 MANIFEST blocks and compare against the
    abbreviated sha256 recorded there.  Catches a swapped or re-downloaded file, which
    would silently change every page number in the verdict.  Recomputes from the bytes.
    """
    rows = re.findall(r"\|\s*`([^`]+\.pdf)`\s*\|\s*`[^`]+`\s*\|[^|]*\|\s*`([0-9a-f]{8})…([0-9a-f]{5,10})`\s*\|",
                      MANIFEST.read_text())
    if not rows:
        record("P", "manifest_hashes", "FAIL", "no leg-411 hash rows parsed out of Papers/MANIFEST.md")
        return
    ok = bad = absent = 0
    wrong: list[str] = []
    for fn, head, tail in rows:
        p = PAPERS / fn
        if not p.exists():
            absent += 1
            continue
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        if h.startswith(head) and h.endswith(tail):
            ok += 1
        else:
            bad += 1
            wrong.append(fn)
    if absent == len(rows):
        record("P", "manifest_hashes", "UNRESOURCED",
               f"{len(rows)} rows; Papers/ absent (gitignored) -- NOT a pass, NOT a fail")
        return
    record("P", "manifest_hashes", "FAIL" if bad else "PASS",
           f"{ok}/{len(rows) - absent} PDFs re-hash to the manifest value"
           + (f"; {absent} unresourced" if absent else "")
           + (f"; WRONG: {wrong}" if wrong else ""))


def check_nonsense_control_from_primary(ft: dict) -> None:
    """[P] Re-run the FT3 nonsense negative control over the PDFs themselves.

    A nonsense control that is only re-read out of the JSON proves nothing -- the JSON
    would report 0 whether or not the search ever ran.  This one searches the corpus again.
    """
    ctl = next((c for c in ft["controls"] if c["control"].startswith("FT3")), None)
    if ctl is None:
        record("P", "nonsense_control_recompute", "FAIL", "FT3 control absent from the artefact")
        return
    phrase = ctl["phrase"].lower()
    seen = absent = 0
    for c in ft["corpus"]:
        pages = pages_of(PAPERS / c["file"])
        if pages is None:
            absent += 1
            continue
        if phrase in norm("\f".join(pages)).lower():
            seen += 1
    if absent == len(ft["corpus"]):
        record("P", "nonsense_control_recompute", "UNRESOURCED",
               "Papers/ absent (gitignored) -- NOT a pass, NOT a fail")
        return
    record("P", "nonsense_control_recompute", "FAIL" if seen else "PASS",
           f"{phrase!r} found in {seen} of {len(ft['corpus']) - absent} re-read documents "
           f"(planted: exactly 0)")


def check_served_namespace_live(md: dict) -> None:
    """[P] Re-ask the live arXiv endpoint what opensearch namespace it serves and compare
    to the string banked from the run.  This is leg 387's exact failure mode, so the check
    reads the namespace OFF THE RESPONSE and never off the request.

    A network failure here is `UNRESOURCED`, never a zero and never a pass.
    """
    banked = md.get("opensearch_namespace_served_verbatim") or []
    url = ("https://export.arxiv.org/api/query?search_query=all:%22Navier-Stokes%22"
           "&start=0&max_results=1")
    try:
        with urllib.request.urlopen(url, timeout=45) as r:
            body = r.read().decode("utf-8", "replace")
            code = r.status
    except Exception as exc:                                    # noqa: BLE001
        record("P", "served_namespace_live", "UNRESOURCED",
               f"endpoint unreachable in this container ({type(exc).__name__}) -- "
               f"NOT a pass, NOT a fail, and NOT a zero")
        return
    ns = sorted(set(re.findall(r'xmlns:opensearch="([^"]+)"', body)))
    tot = re.search(r"opensearch:totalResults[^>]*>(\d+)<", body)
    if not ns:
        record("P", "served_namespace_live", "FAIL", f"http {code} but no opensearch xmlns in the body")
        return
    same = sorted(set(banked)) == ns
    record("P", "served_namespace_live", "PASS" if same else "FAIL",
           f"http {code}; served now {ns}; banked {sorted(set(banked))}; "
           f"totalResults parses = {tot.group(1) if tot else 'NO'}")


# ---------------------------------------------------------------- [O] checks

def check_no_throttle_carries_a_total(md: dict) -> None:
    """[O] THROTTLED / FAILED records must carry `total = None`.  This is the structural
    guarantee that a non-measurement cannot be rendered as a zero by any downstream reader
    who never reads the journal.  It is [O] because it can only inspect this leg's own
    JSON -- it verifies a NUMBER (`total`) rather than asserting that the rule was followed.
    """
    bad = []
    recs = list(md["controls"])
    for b in md["batteries"].values():
        recs += b
    recs += md["s2"]
    for r in recs:
        if r["status"] != "MEASURED" and r["total"] is not None:
            bad.append(f"{r.get('control') or r.get('query')}: {r['status']} total={r['total']}")
    record("O", "throttle_never_a_total", "FAIL" if bad else "PASS",
           f"{len(recs)} records inspected; {len(bad)} non-MEASURED records carry a total"
           + (f": {bad[:3]}" if bad else ""))


def check_tally_recomputes(md: dict) -> None:
    """[O] Recompute the printed tally from the raw per-query records.  A summary line that
    disagrees with the records under it is leg 387's failure in miniature.
    """
    recs = list(md["controls"])
    for b in md["batteries"].values():
        recs += b
    arx = {"n": len(recs)}
    for s in ("MEASURED", "THROTTLED", "FAILED"):
        arx[s] = sum(1 for r in recs if r["status"] == s)
    arx["measured_zeros"] = sum(1 for r in recs if r["status"] == "MEASURED" and r["total"] == 0)
    s2 = {"n": len(md["s2"])}
    for s in ("MEASURED", "THROTTLED", "FAILED"):
        s2[s] = sum(1 for r in md["s2"] if r["status"] == s)
    s2["measured_zeros"] = sum(1 for r in md["s2"] if r["status"] == "MEASURED" and r["total"] == 0)
    want_a, want_s = md["tally"]["arxiv"], md["tally"]["semanticscholar"]
    ok = arx == want_a and s2 == want_s
    record("O", "tally_recomputes", "PASS" if ok else "FAIL",
           f"arxiv recomputed {arx} vs banked {want_a}; s2 recomputed {s2} vs banked {want_s}")


def check_failed_control_is_disclosed(md: dict, ft: dict) -> None:
    """[O] Any control with `fired_as_planted = False` must appear BY NAME in NOVELTY.md.

    This verifies a countable property (every failing control id occurs in the verdict
    text), not the vaguer claim "the leg was honest".  It is [O] and weak by construction:
    it proves the disclosure exists, NOT that the disclosure is adequate.
    """
    failed = [c["control"] for c in md["controls"] + ft["controls"] if not c["fired_as_planted"]]
    txt = NOVELTY.read_text()
    undisclosed = [c for c in failed if c not in txt]
    record("O", "failed_controls_disclosed", "FAIL" if undisclosed else "PASS",
           f"{len(failed)} control(s) did not fire as planted {failed}; "
           f"{len(failed) - len(undisclosed)} named in NOVELTY.md"
           + (f"; UNDISCLOSED: {undisclosed}" if undisclosed else ""))


def check_controls_all_fired_flag(md: dict, ft: dict) -> None:
    """[O] The top-level `controls_all_fired` boolean must agree with the per-control
    records.  A summary flag that says True over a control that failed is precisely the
    smoothing this leg is required not to do.
    """
    out = []
    for name, d in (("instrument1", md), ("instrument2", ft)):
        per = all(c["fired_as_planted"] for c in d["controls"])
        flag = d["controls_all_fired"]
        out.append(f"{name}: flag={flag} recomputed={per}" + ("" if flag == per else "  <-- DISAGREE"))
    record("O", "controls_all_fired_flag", "FAIL" if "DISAGREE" in " ".join(out) else "PASS", "; ".join(out))


def main() -> int:
    md = json.loads(MD.read_text())
    ft = json.loads(FT.read_text())
    v = subprocess.run(["pdftotext", "-v"], capture_output=True)
    print("leg 411 / PB1 -- evidence checks for the P1 novelty gate")
    print(f"pdftotext: {(v.stderr or v.stdout).decode().splitlines()[0] if (v.stderr or v.stdout) else 'ABSENT'}")
    print("\n[P] recompute-from-primary -- goes back to the PDF / the bytes / the endpoint")
    check_quotes_are_on_the_pages_claimed(ft)
    check_ck_table1_numbers()
    check_manifest_hashes()
    check_nonsense_control_from_primary(ft)
    check_served_namespace_live(md)
    print("\n[O] re-read-own-artefact -- internal consistency ONLY; not evidence of truth")
    check_no_throttle_carries_a_total(md)
    check_tally_recomputes(md)
    check_failed_control_is_disclosed(md, ft)
    check_controls_all_fired_flag(md, ft)

    def tally(cls):
        r = [x for x in RESULTS if x[0] == cls]
        return (sum(1 for x in r if x[2] == "PASS"),
                sum(1 for x in r if x[2] == "FAIL"),
                sum(1 for x in r if x[2] == "UNRESOURCED"))
    pp, pf, pu = tally("P")
    op, of, ou = tally("O")
    print("\nSUMMARY -- the two classes are NOT added together, deliberately.")
    print(f"  [P] recompute-from-primary : {pp} pass, {pf} fail, {pu} UNRESOURCED")
    print(f"  [O] re-read-own-artefact   : {op} pass, {of} fail, {ou} UNRESOURCED")
    print("  UNRESOURCED is neither a pass nor a fail and is never reported as a null result.")
    print("  A [O] pass is NOT evidence the verdict is correct: it cannot detect an error")
    print("  shared between this leg's artefact and this leg's checker (CORRECTIONS Sec 45).")
    print("  ONLY the [P] line bears on whether the gate answer is true, and it bears on it")
    print("  only to the extent that the PDFs are present in this checkout.")
    return 1 if (pf or of) else 0


if __name__ == "__main__":
    sys.exit(main())
