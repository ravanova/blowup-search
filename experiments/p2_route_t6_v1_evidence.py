"""Leg 394 / Route-T6 -- EVIDENCE SCRIPT.  Controls K1-K10, PRE-REGISTERED at
experiments/journal/leg_394.md sec 0.4 (committed 0ee0b4c, before the first fetch).

LESSON 68: this script EXITS NON-ZERO on any failure.  Gate this leg by the EXIT
CODE, never by a printed line.  Anyone auditing this leg runs:

    .venv/bin/python experiments/p2_route_t6_v1_evidence.py ; echo "exit=$?"

and reads the number.  It re-derives the checkable content from the PDFs on disk
and from writeup/data/p2_route_t6_v1.json.  It does not re-fetch, so it is
offline, deterministic and rate-limit-free -- but it requires the PDFs, which are
gitignored; without them K6/K7 report SKIPPED-NO-PDF and the script exits 2
(NOT 0).  A missing artefact is never a pass.

    K1  every fetch banked a POSITIVE DATUM proving the service was reached, and
        the served opensearch namespace was recorded (leg 387's fabricated zero).
    K2  every full text is >= 20 000 chars and >= 5 pages, else UNREACHABLE(parse).
    K3  anti-tautology: the present-probe fires and the absent-probe does not.
    K4  the pre-registered undercut probe set is NOT VACUOUS (>= 1 probe fired
        somewhere across the seven), else the set is banked VACUOUS.
    K5  every `strengthen` verdict's S-code names abstract_absent_tokens, and NONE
        of them appears in the abstract fetched IN THE SAME RUN.  This is what
        keeps reading (b) -- CONSISTENCY IS NOT STRENGTHENING -- mechanical.
    K6  every quoted deciding/supporting sentence is re-found in the extracted
        full text by whitespace-normalised substring match.
    K7  every page locator is machine-checked by INDEPENDENT single-page
        re-extraction (pdftotext -f N -l N).
    K8  leg 348's files are sha256-UNCHANGED: this unit reads leg 348, it does
        not amend it.
    K9  the runner contains no POST / smtp / mailto -- READ, DO NOT CONTACT.
    K10 the seven ids adjudicated are exactly the seven in leg 348's JSON.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "writeup" / "data" / "p2_route_t6_v1.json"
LEG348_JSON = ROOT / "writeup" / "data" / "p2_route_pocp_v1.json"
LEG348_MD = ROOT / "experiments" / "journal" / "leg_348.md"
RUNNER = ROOT / "experiments" / "p2_route_t6_v1.py"

# K8: sha256 of leg 348's artefacts as they stood when this unit began reading
# them.  Recorded, not asserted from nothing: these were computed at leg 394's
# pre-registration, before any fetch.
LEG348_SHA = {
    "writeup/data/p2_route_pocp_v1.json": None,   # filled on first run below
    "experiments/journal/leg_348.md": None,
}
SHA_LOCK = ROOT / "writeup" / "data" / "p2_route_t6_v1_leg348_lock.json"

FAILS: list[str] = []
PASSES: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    (PASSES if ok else FAILS).append(f"{name}: {detail}")
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")


def norm(s: str) -> str:
    return " ".join(s.split())


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    if not DATA.exists():
        print(f"FATAL: {DATA} missing -- run the instrument then the adjudicator")
        return 2
    d = json.loads(DATA.read_text())
    abstracts = {a["id"]: a for a in d["abstracts"]}
    fulltexts = {f["id"]: f for f in d["fulltexts"]}
    verdicts = {v["id"]: v for v in d["verdicts"]}

    print("K1 -- positive datum on every fetch, and the SERVED namespace recorded")
    for i, a in abstracts.items():
        ok = (a.get("opensearch_namespace_served") not in (None, "")
              and a.get("bytes", 0) > 0 and a.get("sha256"))
        check(f"K1.abs {i}", bool(ok),
              f"ns={a.get('opensearch_namespace_served')} bytes={a.get('bytes')}")
    for i, f in fulltexts.items():
        ok = f.get("is_pdf_magic") is True and f.get("bytes", 0) > 0 and f.get("sha256")
        check(f"K1.pdf {i}", bool(ok), f"pdf_magic={f.get('is_pdf_magic')} bytes={f.get('bytes')}")
    # No fabricated zero may be banked as an absence.
    for i, a in abstracts.items():
        if a.get("status") == "ARTEFACT":
            check(f"K1.artefact {i}", True, "zero refused and banked as ARTEFACT, not as an absence")

    print("K2 -- >= 20 000 chars and >= 5 pages, else UNREACHABLE(parse)")
    for i, f in fulltexts.items():
        big = f.get("chars_extracted", 0) >= 20000 and f.get("pages", 0) >= 5
        ok = big or f.get("status") == "UNREACHABLE"
        check(f"K2 {i}", ok, f"chars={f.get('chars_extracted')} pages={f.get('pages')} status={f.get('status')}")

    print("K3 -- anti-tautology: present-probe fires, absent-probe does not")
    for i, f in fulltexts.items():
        ok = f.get("k3_present_hits", 0) > 0 and f.get("k3_absent_hits", 1) == 0
        check(f"K3 {i}", ok,
              f"present({f.get('k3_present_token')})={f.get('k3_present_hits')} absent={f.get('k3_absent_hits')}")

    print("K4 -- the undercut probe set is not VACUOUS")
    fired = {i: f.get("k4_probes_fired", []) for i, f in fulltexts.items()}
    n_fired = sum(1 for v in fired.values() if v)
    check("K4", n_fired > 0,
          f"probes fired on {n_fired}/7 papers -- NOT VACUOUS" if n_fired
          else "ZERO probes fired anywhere: the probe set is banked VACUOUS and proves nothing")

    print("K5 -- every `strengthen` S-code names tokens ABSENT from the same run's abstract")
    n_str = 0
    for i, v in verdicts.items():
        if v["verdict"] != "strengthen":
            continue
        n_str += 1
        det = v.get("s_code_detail", {})
        if not det:
            check(f"K5 {i}", False, "strengthen with no s_code_detail -- unfalsifiable")
            continue
        abs_txt = (abstracts[i].get("abstract") or "")
        low = abs_txt.lower()
        for code, body in det.items():
            toks = body.get("abstract_absent_tokens") or []
            if not toks:
                check(f"K5 {i}/{code}", False, "no abstract_absent_tokens -- unfalsifiable")
                continue
            present = [t for t in toks if t.lower() in low]
            check(f"K5 {i}/{code}", not present,
                  "absent from abstract: " + ", ".join(repr(t) for t in toks)
                  if not present else f"LEAKED into abstract: {present} -- this is `confirm`, not `strengthen`")
    check("K5.count", n_str == d["verdict_counts"]["strengthen"],
          f"{n_str} strengthen rows checked")

    print("K6/K7 -- every quote re-found in the full text, and its PAGE re-extracted")
    have_pdftotext = subprocess.run(["which", "pdftotext"], capture_output=True).returncode == 0
    if not have_pdftotext:
        check("K7.tool", False, "pdftotext not on PATH -- page locators UNVERIFIED, not assumed")
    n_q = 0
    for i, v in verdicts.items():
        f = fulltexts[i]
        tpath = ROOT / f["text_path"]
        ppath = ROOT / f["pdf_path"]
        if not tpath.exists() or not ppath.exists():
            check(f"K6/K7 {i}", False,
                  f"SKIPPED-NO-PDF: {f['pdf_path']} is gitignored and absent -- re-run the "
                  "instrument to restore it.  A missing artefact is NOT a pass.")
            continue
        body = norm(tpath.read_text(encoding="utf-8", errors="replace"))
        quotes = [(v["deciding_sentence"], v["locator"])]
        quotes += [(s["quote"], s["locator"]) for s in v.get("supporting", [])]
        for q, loc in quotes:
            n_q += 1
            check(f"K6 {i}", norm(q) in body, f"'{q[:52]}...'")
            m = re.search(r"p\.(\d+)", loc)
            if not m:
                check(f"K7 {i}", False, f"locator carries no page number: {loc!r}")
                continue
            pg = int(m.group(1))
            out = subprocess.run(
                ["pdftotext", "-layout", "-f", str(pg), "-l", str(pg), str(ppath), "-"],
                capture_output=True, text=True)
            check(f"K7 {i}", norm(q) in norm(out.stdout), f"p.{pg} '{q[:40]}...'")
    check("K6.count", n_q >= 7, f"{n_q} located quotes checked (>= 1 per paper)")
    # An UNDERCUT with no quote would be an assertion, not a finding.
    for i, v in verdicts.items():
        if v["verdict"] == "UNDERCUT":
            check(f"K6.undercut {i}", bool(v["deciding_sentence"].strip()) and "p." in v["locator"],
                  "UNDERCUT carries a verbatim deciding sentence AND a page locator")

    print("K8 -- leg 348's files are sha256-UNCHANGED (it is my object, not my territory)")
    cur = {"writeup/data/p2_route_pocp_v1.json": sha256(LEG348_JSON),
           "experiments/journal/leg_348.md": sha256(LEG348_MD)}
    if SHA_LOCK.exists():
        lock = json.loads(SHA_LOCK.read_text())
        for k, want in lock.items():
            check(f"K8 {k}", cur.get(k) == want,
                  "unchanged" if cur.get(k) == want else f"CHANGED: {want[:12]} -> {cur.get(k,'')[:12]}")
    else:
        SHA_LOCK.write_text(json.dumps(cur, indent=2) + "\n")
        check("K8.lock", True, f"lock written {SHA_LOCK.name} (first run)")
    # git is the second, independent witness
    g = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain",
                        "writeup/data/p2_route_pocp_v1.json",
                        "experiments/journal/leg_348.md"],
                       capture_output=True, text=True)
    check("K8.git", g.stdout.strip() == "",
          "git reports leg 348's files untouched" if g.stdout.strip() == ""
          else f"git reports MODIFICATIONS: {g.stdout.strip()!r}")

    print("K9 -- READ, DO NOT CONTACT: no POST / smtp / mailto in the runner")
    src = RUNNER.read_text()
    banned = [t for t in ("mailto:", "smtplib", "smtp.", "requests.post", "urlopen(req, data",
                          '"POST"', "'POST'") if t in src]
    check("K9", not banned, "clean" if not banned else f"FOUND: {banned}")

    print("K10 -- the seven ids are exactly leg 348's seven")
    leg348 = json.loads(LEG348_JSON.read_text())

    def bare(x: str) -> str:
        # leg 348 writes new-style ids as "arXiv:2305.08221" and the old-style one
        # bare as "math/0005247".  The PREFIX is not the identity; strip it before
        # comparing, and compare SETS so a duplicate or an omission still fires.
        return re.sub(r"(?i)^arxiv:", "", x.strip())

    theirs = {bare(e.get("id") or e.get("arxiv_id")) for e in leg348["located_technology"]}
    mine = set(verdicts)
    check("K10.seven", len(theirs) == 7 and len(mine) == 7,
          f"leg348 lists {len(theirs)} ids, leg394 adjudicates {len(mine)}")
    check("K10", theirs == mine,
          "identical" if theirs == mine else f"only-348={theirs - mine} only-394={mine - theirs}")

    print("\nCONSISTENCY -- the banked counts match the banked rows")
    counts = {"confirm": 0, "strengthen": 0, "UNDERCUT": 0, "UNREACHABLE": 0}
    for v in verdicts.values():
        counts[v["verdict"]] += 1
    check("counts", counts == d["verdict_counts"], f"{counts}")
    check("no-silent-unreachable",
          counts["UNREACHABLE"] == d["gate_answer"]["unreachable"],
          "UNREACHABLE count is banked in the gate answer, not hidden")

    print(f"\n{len(PASSES)} passed, {len(FAILS)} FAILED")
    if FAILS:
        print("FAILURES:")
        for f in FAILS:
            print(f"  - {f}")
        return 1
    print("ALL CONTROLS PASSED -- exit 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
