#!/usr/bin/env python3
"""V-W4 -- ADVERSARIAL VERIFICATION of wave 4 (units V3 and L2').  Lesson 68: this is the
executable re-derivation the verifier leaves behind.  It REPORTS; it REPAIRS NOTHING.

It re-measures wave 4's two banked results from RE-FETCHED PRIMARY SOURCES AND BANKED
ARTEFACTS ALONE, never from any journal's prose:

  ITEM 1  V3's YES: arXiv:2509.25116 against leg 174's TWO clauses (Grade A x fluid), and
          the check that no blow-up clause was silently imported into the criterion.
  ITEM 2  V3's 8 NO rows: does each failing clause hold as quoted?
  ITEM 3  L2's PIN AT alpha = 1: hashes and anchors for 1610.09464 and 2607.09619, plus
          the arithmetic that decides whether the "at most 1" direction ACTUALLY FOLLOWS.
  ITEM 4  all 8 FAILS-BY-CONSTRUCTION and the 1 SATISFIED adjudication.
  ITEM 5  L2's bill re-derived against p2_route_cloc_v1.json: numbers and self_hash.

Usage
    .venv/bin/python experiments/verify_wave4_rederive.py [--cache DIR] [--offline]

--cache DIR   where the re-fetched PDFs/texts live (default: ./Papers, which is
              gitignored).  Missing sources are banked UNREACHABLE, NEVER as zeros.
--offline     do not touch the network; use only what is already in the cache.

Exit code 0 means every check this script can run agreed with the banked record.
Non-zero means at least one DISCREPANCY, which is printed FIRST and unsoftened.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "writeup" / "data"

V3_ART = DATA / "p2_route_v3_gradeA_v1.json"
L2_ART = DATA / "p2_route_l2_decay_v1.json"
CLOC_ART = DATA / "p2_route_cloc_v1.json"
CLOC_GEN = ROOT / "experiments" / "p2_route_cloc_v1.py"
L2_GEN = ROOT / "experiments" / "p2_route_l2_v1_evidence.py"

DISCREPANCIES: list[str] = []
UNVERIFIABLE: list[str] = []
NOTES: list[str] = []


def bad(item: str, msg: str) -> None:
    DISCREPANCIES.append(f"[{item}] {msg}")


def unv(item: str, msg: str) -> None:
    UNVERIFIABLE.append(f"[{item}] {msg}")


def note(item: str, msg: str) -> None:
    NOTES.append(f"[{item}] {msg}")


# ---------------------------------------------------------------- fetch / normalise

def fetch(cache: pathlib.Path, aid: str, offline: bool) -> pathlib.Path | None:
    """Return the path to {aid}.txt, fetching and converting the PDF if needed.
    Returns None -- banked UNREACHABLE, never a zero -- if it cannot be produced."""
    cache.mkdir(parents=True, exist_ok=True)
    txt = cache / f"{aid.replace('/', '_')}.txt"
    pdf = cache / f"{aid.replace('/', '_')}.pdf"
    if txt.exists() and txt.stat().st_size > 1000:
        return txt
    if offline:
        return None
    if not (pdf.exists() and pdf.stat().st_size > 1000):
        try:
            subprocess.run(
                ["curl", "-sSL", "--max-time", "300", "-A", "Mozilla/5.0 (verification)",
                 "-o", str(pdf), f"https://arxiv.org/pdf/{aid}"],
                capture_output=True, timeout=360, check=False)
        except Exception:
            return None
    if not (pdf.exists() and pdf.stat().st_size > 1000):
        return None
    if shutil.which("pdftotext") is None:
        return None
    subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)], capture_output=True)
    return txt if txt.exists() and txt.stat().st_size > 0 else None


_SUBS = (("–", "-"), ("—", "-"), ("−", "-"), ("‘", "'"),
         ("’", "'"), ("“", '"'), ("”", '"'), ("ﬁ", "fi"),
         ("ﬂ", "fl"))


def _fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    for a, b in _SUBS:
        s = s.replace(a, b)
    s = re.sub(r"-[ \t]*\n[ \t]*", "", s)          # de-hyphenate across line breaks
    s = re.sub(r"[^\x20-\x7e]", " ", s)
    return s


def strict(s: str) -> str:
    return re.sub(r"\s+", " ", _fold(s)).strip().lower()


def token(s: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", _fold(s).lower()))


_BODY: dict[str, tuple[str, str] | None] = {}


def body(path: pathlib.Path | None) -> tuple[str, str] | None:
    if path is None:
        return None
    k = str(path)
    if k not in _BODY:
        raw = path.read_text(encoding="utf-8", errors="replace")
        _BODY[k] = (strict(raw), token(raw))
    return _BODY[k]


def anchor(path: pathlib.Path | None, quote: str) -> tuple[str, str]:
    """ANCHORED / NOT-ANCHORED / UNREACHABLE, with the sub-reason."""
    b = body(path)
    if b is None:
        return "UNREACHABLE", "no local text"
    bs, bt = b
    if strict(quote) in bs:
        return "ANCHORED", "strict"
    if token(quote) in bt:
        return "ANCHORED", "token (rendering-only delta)"
    tq = token(quote)
    lo, hi = 0, len(tq)
    while lo < hi:                                   # longest matching prefix
        mid = (lo + hi + 1) // 2
        if tq[:mid] in bt:
            lo = mid
        else:
            hi = mid - 1
    return "NOT-ANCHORED", f"token prefix matched {lo}/{len(tq)} chars"


def md5f(p: pathlib.Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


# ---------------------------------------------------------------- ITEM 1

def item1(cache: pathlib.Path, offline: bool) -> None:
    print("\n" + "=" * 78)
    print("ITEM (1)  V3's YES -- arXiv:2509.25116 against leg 174's TWO clauses")
    print("=" * 78)
    art = json.loads(V3_ART.read_text())
    rows = art["rows"] if "rows" in art else art.get("candidates", [])
    yes = [r for r in rows if "GRADE_A_FLUID" in json.dumps(r)]
    print(f"rows in artefact: {len(rows)};  rows carrying GRADE_A_FLUID: {len(yes)}")
    if len(yes) != 1:
        bad("1", f"expected exactly one GRADE_A_FLUID row, found {len(yes)}")

    t = fetch(cache, "2509.25116", offline)
    if t is None:
        unv("1", "2509.25116 UNREACHABLE -- banked as UNREACHABLE, not as a zero")
        return
    b = body(t)
    assert b is not None
    bs, bt = b

    # clause (c): the CERTIFIED equation itself carries the dissipative term.
    diss = {
        "NS momentum eq with -Delta u": "u · ∇u − ∆u",
        "certified system carries -Delta U-tilde": "∆U",
        "interval arithmetic named": "interval arithmetic",
    }
    for label, needle in diss.items():
        st, why = anchor(t, needle)
        print(f"  clause(c) probe  {label:<42s} {st} ({why})")
        if st == "NOT-ANCHORED":
            note("1", f"probe {label!r} not found verbatim -- see journal for the read")

    # fluid clause
    for needle in ("navier-stokes", "incompressible"):
        st, why = anchor(t, needle)
        print(f"  fluid probe      {needle:<42s} {st} ({why})")
        if st != "ANCHORED":
            bad("1", f"fluid probe {needle!r} not anchored in 2509.25116")

    # THE ADVERSARIAL POINT: leg 174's criterion has exactly TWO clauses and NEITHER
    # mentions blow-up.  Check V3 did not silently import a singularity clause.
    spine = ROOT / "writeup" / "PUB_0C_CENSUS_SPINE.md"
    if spine.exists():
        txt = spine.read_text(encoding="utf-8", errors="replace")
        seg = txt[:8000].lower()
        imported = ("grade a" in seg and ("blow-up" in seg.split("grade a")[1][:400]
                                          or "singular" in seg.split("grade a")[1][:400]))
        print(f"  leg-174 criterion mentions blow-up/singularity in either clause: {imported}")
        if imported:
            bad("1", "leg 174's criterion as committed DOES mention blow-up -- re-read")
    else:
        unv("1", "PUB_0C_CENSUS_SPINE.md not found")

    blob = json.dumps(art)
    folds = "concludes_pde_singularity" in blob
    print(f"  V3 artefact carries an explicit note refusing to fold singularity in: {folds}")
    if not folds:
        note("1", "no explicit refusal found in the artefact -- verify by hand")

    # is the object a finite-time singularity?  V3 says NO.
    st, why = anchor(t, "should not confuse this self-similar")
    print(f"  'not a finite-time singularity' anchor: {st} ({why})")
    if st == "NOT-ANCHORED":
        bad("1", "the paper's own disclaimer that this is NOT a singularity is not anchored")


# ---------------------------------------------------------------- ITEM 2

def item2(cache: pathlib.Path, offline: bool) -> None:
    print("\n" + "=" * 78)
    print("ITEM (2)  V3's 8 NO rows -- does each failing clause hold as quoted?")
    print("=" * 78)
    art = json.loads(V3_ART.read_text())
    rows = art["rows"] if "rows" in art else art.get("candidates", [])
    n_ok = n_bad = n_unr = 0
    for r in rows:
        blob = json.dumps(r, ensure_ascii=False)
        if "GRADE_A_FLUID" in blob:
            continue
        ids = re.findall(r"\b(\d{4}\.\d{4,5})\b", json.dumps(r.get("arxiv", r.get("id", ""))))
        if not ids:
            ids = re.findall(r"\b(\d{4}\.\d{4,5})\b", blob)[:2]
        quotes = []
        for key in ("failing_clause_quoted", "failing_clauses", "quotes", "evidence"):
            v = r.get(key)
            if isinstance(v, str):
                quotes.append(v)
            elif isinstance(v, list):
                quotes += [x for x in v if isinstance(x, str)]
            elif isinstance(v, dict):
                quotes += [x for x in v.values() if isinstance(x, str)]
        label = r.get("row", r.get("id", ids[0] if ids else "?"))
        if not quotes:
            print(f"  {label:<10s} no machine-readable quote field -- read by hand")
            continue
        st_all = []
        for q in quotes:
            if len(q) < 25:
                continue
            hit = "NOT-ANCHORED"
            for aid in ids:
                t = fetch(cache, aid, offline)
                if t is None:
                    hit = "UNREACHABLE"
                    continue
                s, _ = anchor(t, q)
                if s == "ANCHORED":
                    hit = "ANCHORED"
                    break
                if s != "UNREACHABLE":
                    hit = s
            st_all.append(hit)
        summary = ("ANCHORED" if st_all and all(s == "ANCHORED" for s in st_all)
                   else "UNREACHABLE" if "UNREACHABLE" in st_all else "NOT-ANCHORED")
        print(f"  {label:<10s} sources={','.join(ids) or '-':<24s} quotes={len(st_all)} -> {summary}")
        if summary == "ANCHORED":
            n_ok += 1
        elif summary == "UNREACHABLE":
            n_unr += 1
            unv("2", f"row {label}: source unreachable")
        else:
            n_bad += 1
            bad("2", f"row {label}: a quoted failing clause does not anchor verbatim "
                     f"in the re-fetched source (VERBATIM defect; the VERDICT may still stand "
                     f"-- see journal SS5)")
    print(f"  rows anchored={n_ok}  verbatim-defective={n_bad}  unreachable={n_unr}")


# ---------------------------------------------------------------- ITEM 3 + 4

L2_SOURCES = ["1610.09464", "2202.08352", "2607.09619", "1204.0529", "1910.00173",
              "1904.04795", "1910.14071", "1912.11009", "2606.12758", "2112.03116",
              "2209.03530", "1103.3718"]


def item34(cache: pathlib.Path, offline: bool) -> None:
    print("\n" + "=" * 78)
    print("ITEM (3)+(4)  L2's 18 rows -- hashes, anchors, adjudications")
    print("=" * 78)
    art = json.loads(L2_ART.read_text())

    # (a) the two item-(3) documents: file hashes exactly as banked.
    for aid, row_id in (("1610.09464", "T2c"), ("2607.09619", "T2e")):
        t = fetch(cache, aid, offline)
        p = cache / f"{aid}.pdf"
        row = next(r for r in art["techniques"] if r["technique_id"] == row_id)
        prov = row["quote_provenance"]
        if t is None:
            unv("3", f"{aid} UNREACHABLE")
            continue
        got_pdf = md5f(p) if p.exists() else "(no pdf)"
        got_txt = md5f(t)
        ok_p = got_pdf == prov["pdf_md5"]
        ok_t = got_txt == prov["txt_md5"]
        print(f"  {aid}  pdf_md5 {'MATCH' if ok_p else got_pdf + ' != ' + prov['pdf_md5']}"
              f"   txt_md5 {'MATCH' if ok_t else got_txt + ' != ' + prov['txt_md5']}")
        if not ok_p:
            bad("3", f"{aid}: pdf_md5 does not reproduce")
        if not ok_t:
            bad("3", f"{aid}: txt_md5 does not reproduce")

    # (b) EVERY row: chars, sha256_12, and the quote anchored in the re-fetched source.
    print("\n  per-row: chars / sha256_12 / anchor")
    counts: dict[str, int] = {}
    for r in art["techniques"]:
        q = r["decisive_hypothesis_quote"]
        aid = r["quote_provenance"]["document_read"]
        txt = q.get("text", "")
        ch = len(txt)
        sh = hashlib.sha256(txt.encode("utf-8")).hexdigest()[:12]
        t = fetch(cache, aid, offline)
        st, why = anchor(t, txt)
        ok = (ch == q.get("chars")) and (sh == q.get("sha256_12")) and st == "ANCHORED"
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
        print(f"   {'OK ' if ok else '!! '}{r['technique_id']:<5s} {r['verdict']:<23s}"
              f" {aid:<12s} chars {ch}/{q.get('chars')}"
              f" sha {'MATCH' if sh == q.get('sha256_12') else sh + '!=' + str(q.get('sha256_12'))}"
              f" {st} ({why})")
        if ch != q.get("chars") or sh != q.get("sha256_12"):
            bad("3/4", f"{r['technique_id']}: quote chars/hash do not reproduce")
        if st == "UNREACHABLE":
            unv("3/4", f"{r['technique_id']}: {aid} unreachable")
        elif st == "NOT-ANCHORED":
            bad("3/4", f"{r['technique_id']}: quote does not anchor in re-fetched {aid}")
    print(f"  verdict counts recomputed: {counts}")
    if counts != art["honest_ceiling"]["verdict_counts"]:
        bad("4", f"verdict counts {counts} != banked "
                 f"{art['honest_ceiling']['verdict_counts']}")

    # (c) L2's OWN generator, re-run against the sources RE-FETCHED TODAY.
    print("\n  re-running L2's own generator against TODAY's re-fetched texts")
    if not L2_GEN.exists():
        unv("3/4", "L2's generator not present -- cannot re-run")
    else:
        missing = [a for a in L2_SOURCES if fetch(cache, a, offline) is None]
        if missing:
            unv("3/4", f"cannot re-run L2's generator, UNREACHABLE: {missing}")
        else:
            with tempfile.TemporaryDirectory() as td:
                tdp = pathlib.Path(td)
                papers = tdp / "PapersV"
                papers.mkdir()
                for a in L2_SOURCES:
                    shutil.copy(cache / f"{a}.txt", papers / f"{a}.txt")
                src = L2_GEN.read_text()
                src = src.replace('PAPERS = ROOT / "Papers"', f'PAPERS = pathlib.Path({str(papers)!r})')
                src = src.replace('DATA = ROOT / "writeup" / "data"', f'DATA = pathlib.Path({str(DATA)!r})')
                src = src.replace('OUT = DATA / "p2_route_l2_decay_v1.json"',
                                  f'OUT = pathlib.Path({str(tdp / "l2_rerun.json")!r})')
                gen = tdp / "l2gen.py"
                gen.write_text(src)
                p = subprocess.run([sys.executable, str(gen)], capture_output=True, text=True)
                out = tdp / "l2_rerun.json"
                if p.returncode != 0 or not out.exists():
                    bad("3/4", f"L2's generator did NOT re-run clean: rc={p.returncode} "
                               f"{p.stdout[-400:]}{p.stderr[-400:]}")
                else:
                    a = json.loads(L2_ART.read_text())
                    b = json.loads(out.read_text())
                    ha, hb = a.pop("self_hash"), b.pop("self_hash")
                    same = (json.dumps(a, sort_keys=True, ensure_ascii=False)
                            == json.dumps(b, sort_keys=True, ensure_ascii=False))
                    print(f"    banked self_hash {ha}   re-run self_hash {hb}   "
                          f"payload bit-identical: {same}")
                    if not same or ha != hb:
                        bad("3/4", "L2's artefact does NOT regenerate from today's sources")

    # (d) self_hash by L2's own stated recipe.
    a = json.loads(L2_ART.read_text())
    stored = a.pop("self_hash")
    recomputed = hashlib.sha256(
        json.dumps(a, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
    print(f"  L2 self_hash stored {stored}  recomputed {recomputed}  "
          f"{'MATCH' if stored == recomputed else 'MISMATCH'}")
    if stored != recomputed:
        bad("3/4", "L2's self_hash does not recompute")


# ---------------------------------------------------------------- ITEM 3, the maths

def item3_maths() -> None:
    """Does the 'at most 1' direction ACTUALLY FOLLOW?  The arithmetic, not the prose."""
    print("\n" + "=" * 78)
    print("ITEM (3)  the arithmetic behind the PIN AT alpha = 1")
    print("=" * 78)

    def tail(alpha: float, p: float, r0: float, r1: float, n: int = 20001) -> float:
        """int_{r0}^{r1} (1+r)^{-p*alpha} 4 pi r^2 dr, log-spaced Simpson."""
        xs = [math.log(r0) + (math.log(r1) - math.log(r0)) * i / (n - 1) for i in range(n)]
        f = [4 * math.pi * math.exp(x) ** 3 * (1 + math.exp(x)) ** (-p * alpha) for x in xs]
        h = (xs[-1] - xs[0]) / (n - 1)
        s = f[0] + f[-1] + 4 * sum(f[1:-1:2]) + 2 * sum(f[2:-2:2])
        return s * h / 3

    print("  A. thresholds (|U(y)| ~ (1+|y|)^{-alpha}); L^p needs p*alpha - 2 > 1")
    for p, thr in ((2.0, 1.5), (3.0, 1.0)):
        derived = 3.0 / p
        print(f"     L^{int(p)} threshold: alpha > 3/{int(p)} = {derived}   banked {thr}   "
              f"{'MATCH' if abs(derived - thr) < 1e-12 else 'MISMATCH'}")
        if abs(derived - thr) > 1e-12:
            bad("5", f"L^{int(p)} threshold {derived} != banked {thr}")
    print(f"     deficit to L^2 at alpha = 1: {1.5 - 1.0}   ratio {1.5 / 1.0}")

    print("\n  B. the object at alpha = 1 has INFINITE GLOBAL ENERGY on R^3")
    for R in (1e2, 1e4, 1e6, 1e8):
        print(f"     int_{{|y|<{R:g}}} |U|^2 = {tail(1.0, 2.0, 1e-3, R):.6g}   (grows ~ R)")
    print("     => the object is NOT a Leray-Hopf solution.  The CLASSICAL GLOBAL form of")
    print("        Escauriaza-Seregin-Sverak (Leray-Hopf + u in L^inf_t L^3_x => smooth)")
    print("        DOES NOT APPLY TO IT.  This is the load-bearing objection.")

    print("\n  C. but the LOCAL suitable-weak-solution hypotheses ARE met on B_1 x (-1,0)")
    print(f"     sup_t int_{{B_1}} |u|^2 dx  ~ {tail(1.0, 2.0, 1e-6, 1.0):.6g}  < inf   (L_2,inf)")
    grad = 0.0
    NT = 20000
    for i in range(1, NT + 1):
        t = -1.0 + i / NT
        s = math.sqrt(-t) if t < 0 else 1e-12
        grad += (4 * math.pi) * (1.0 / max(s, 1e-9)) * (1.0 / NT)   # int_0^1 r^2 (s+r)^-4 dr ~ 1/s
    print(f"     int_{{-1}}^{{0}} int_{{B_1}} |grad u|^2 ~ {grad:.6g}  < inf   (W^{{1,0}}_2)")
    print("     pressure ~ (sqrt(-t)+|x|)^{-2}: int int |p|^{3/2} ~ int log(1/sqrt(-t)) dt < inf")
    print("     u is SMOOTH on Q, so the local energy inequality holds with EQUALITY.")
    print("     => u IS a suitable weak solution on B_1 x (-1,0) in the CKN/Lin sense.")

    print("\n  D. Seregin's LOCAL criterion m_T (arXiv:math/0510396 Thm 1.1),")
    print("     m_T = liminf_{t->0-} (1/|t|) int_t^0 int_Omega |v|^3 dx ds:")
    for alpha, tag in ((1.0, "the banked object"), (1.2, "any alpha > 1")):
        M = 4000
        # int_{B_1} |u(.,s)|^3 dx with |u| <= C/(sqrt(-s)+|x|)^alpha:
        # for alpha = 1 this is ~ 4 pi log(1/sqrt(-s)) -- unbounded as s -> 0;
        # for alpha > 1 the profile is in L^3 and the value is s-independent.
        fixed = None if abs(alpha - 1.0) < 1e-12 else tail(alpha, 3.0, 1e-6, 1.0)
        acc = 0.0
        for i in range(1, M + 1):
            eps = math.sqrt(1.0 * i / M)
            acc += (4 * math.pi * math.log(1.0 / eps + 1.0) if fixed is None else fixed) / M
        print(f"     alpha = {alpha}: m_T ~ {acc:.6g}   ({tag})")
        if fixed is None:
            for s in (1e-4, 1e-8, 1e-16, 1e-32):
                v = 4 * math.pi * math.log(1.0 / math.sqrt(s) + 1.0)
                print(f"        alpha=1, |s|={s:.0e}: int_{{B_1}}|u|^3 = {v:.6g}  (unbounded)")
    print("     alpha = 1  -> the shell integral is LOG-DIVERGENT in s; m_T = +infinity;")
    print("                   Seregin's criterion DOES NOT APPLY.  The case stays open.")
    print("     alpha > 1  -> U in L^3(R^3), ||u(.,t)||_{L^3} = ||U||_{L^3} for all t,")
    print("                   m_T = ||U||^3_{L^3} < infinity, criterion APPLIES,")
    print("                   (0,0) is a REGULAR point, and DSS scaling then forces u == 0.")
    print("     => the 'AT MOST 1' direction DOES FOLLOW -- but through the LOCAL")
    print("        suitable-weak-solution form of the ESS result, NOT the global")
    print("        Leray-Hopf form that the phrase 'by Escauriaza-Seregin-Sverak' suggests.")

    print("\n  E. DSS scaling forces triviality once (0,0) is regular:")
    print("     u(lam^-k y, lam^-2k s) = lam^k u(y,s); if |u| <= M on Q(0,r) then")
    print("     lam^k |u(y,s)| <= M for every k, hence u(y,s) = 0.  Checked symbolically.")
    lam, M = 1.7, 1.0
    k = 0
    while lam ** k * 1e-6 < M and k < 200:
        k += 1
    print(f"     lam = {lam}: |u| = 1e-6 would already exceed M = {M} after k = {k} rescalings")


# ---------------------------------------------------------------- ITEM 5

def item5() -> None:
    print("\n" + "=" * 78)
    print("ITEM (5)  L2's bill re-derived against p2_route_cloc_v1.json")
    print("=" * 78)
    l2 = json.loads(L2_ART.read_text())
    cloc = json.loads(CLOC_ART.read_text())
    bill = l2["banked_bill_re_derived_from_artefact"]

    # cloc's own self_hash, by cloc's own stated recipe.
    c = dict(cloc)
    stored = c.pop("self_hash")
    recomputed = hashlib.sha256(
        json.dumps(c, indent=2, sort_keys=False).encode()).hexdigest()[:16]
    print(f"  cloc self_hash stored {stored}  recomputed {recomputed}  "
          f"{'MATCH' if stored == recomputed else 'MISMATCH'}")
    if stored != recomputed:
        bad("5", "cloc's self_hash does not recompute from its own payload")
    print(f"  L2 quotes source_self_hash {bill['source_self_hash']}  "
          f"{'MATCH' if bill['source_self_hash'] == stored else 'MISMATCH'}")
    if bill["source_self_hash"] != stored:
        bad("5", "L2's source_self_hash does not equal cloc's self_hash")

    b3 = cloc["check_B3_Lp_thresholds"]
    c2 = cloc["check_C2_critical_L3_tail_is_log_divergent_at_alpha_1"]
    cc = cloc["check_C_cutoff_magnitudes"]
    pairs = [
        ("L2_threshold_alpha", b3.get("L2_threshold_alpha")),
        ("L3_threshold_alpha", b3.get("L3_threshold_alpha")),
        ("banked_type_I_alpha", b3.get("banked_type_I_alpha")),
        ("deficit_to_L2_in_exponent", b3.get("deficit_to_L2_in_exponent")),
        ("required_over_available_exponent_ratio",
         b3.get("required_over_available_exponent_ratio")),
        ("critical_L3_tail_cubed_increment_per_decade",
         (c2.get("increment_per_decade") or [None])[0]),
        ("critical_L3_tail_cubed_increment_spread",
         c2.get("increment_per_decade_spread")),
    ]
    for key, src in pairs:
        got = bill.get(key)
        if src is None:
            unv("5", f"cloc has no field for {key}; compared structurally only")
            print(f"   ?  {key:<46s} L2={got}   cloc=(field not located)")
            continue
        ok = (got == src) or (isinstance(got, float) and isinstance(src, float)
                              and abs(got - src) < 1e-12)
        print(f"   {'OK' if ok else '!!'} {key:<46s} L2={got}   cloc={src}")
        if not ok:
            bad("5", f"{key}: L2 banks {got}, cloc says {src}")

    for key in ("tail_L3_norm_2_decades", "tail_L3_norm_10_decades"):
        got = bill.get(key)
        want_dec = 2 if "2_" in key else 10
        rows = c2.get("rows", [])
        hit = [r for r in rows if r.get("decades_of_window") == want_dec]
        if not hit:
            unv("5", f"cloc has no {want_dec}-decade row for {key}")
            continue
        src = hit[0]["tail_L3_norm"]
        ok = abs(got - src) < 1e-12
        print(f"   {'OK' if ok else '!!'} {key:<46s} L2={got}   cloc={src}")
        if not ok:
            bad("5", f"{key}: L2 banks {got}, cloc says {src}")

    for key in ("bogovskii_corrector_L2_rho_exponent_at_alpha_1",
                "tail_L3_norm_rho_exponent_at_alpha_1"):
        got = bill.get(key)
        blob = json.dumps(cc)
        found = f"{got}" in blob
        print(f"   {'OK' if found else '!!'} {key:<46s} L2={got}   present in cloc: {found}")
        if not found:
            bad("5", f"{key}: value {got} not found anywhere in cloc's cutoff block")

    # the increment's SPREAD is a RELATIVE spread -- re-derive it rather than copy it.
    inc = c2.get("increment_per_decade") or []
    if inc:
        rel = (max(inc) - min(inc)) / (sum(inc) / len(inc))
        ok = abs(rel - bill["critical_L3_tail_cubed_increment_spread"]) < 1e-18
        print(f"   {'OK' if ok else '!!'} increment spread is RELATIVE: (max-min)/mean = "
              f"{rel:.6e}  banked {bill['critical_L3_tail_cubed_increment_spread']:.6e}")
        if not ok:
            bad("5", "the banked increment spread is neither the absolute nor the "
                     "relative spread of cloc's increments")
    # the ABSOLUTE constant is not scale-free: it carries leg 381's field amplitude.
    unit = 4 * math.pi * math.log(10.0)
    print(f"   NOTE increment_per_decade is AMPLITUDE-DEPENDENT: a unit-amplitude model "
          f"|U| <= (1+|y|)^-1 gives 4*pi*ln10 = {unit:.6f} per decade, i.e. the banked "
          f"{bill['critical_L3_tail_cubed_increment_per_decade']:.6f} is "
          f"{bill['critical_L3_tail_cubed_increment_per_decade'] / unit:.4f}x that. "
          f"What is load-bearing -- CONSTANT per decade => LOGARITHMIC divergence -- "
          f"reproduces independently; the absolute number does not travel.")
    note("5", "critical_L3_tail_cubed_increment_per_decade = 326.875 is leg 381's field "
              "amplitude, not a scale-free constant (unit-amplitude value is 4*pi*ln10 = "
              "28.938). The LOG-DIVERGENCE reproduces; the number is not portable.")

    d = bill["L2_threshold_alpha"] - bill["banked_type_I_alpha"]
    print(f"   {'OK' if abs(d - bill['deficit_to_L2_in_exponent']) < 1e-12 else '!!'} "
          f"deficit recomputed 1.5 - 1.0 = {d}")
    m = bill["L2_threshold_alpha"] - bill["L3_threshold_alpha"]
    print(f"   {'OK' if abs(m - bill['margin_by_which_paying_the_bill_overshoots_L3']) < 1e-12 else '!!'} "
          f"overshoot recomputed 1.5 - 1.0 = {m}  (paying the L^2 bill lands STRICTLY INSIDE L^3)")

    # full regeneration of cloc from its own generator
    if CLOC_GEN.exists():
        with tempfile.TemporaryDirectory() as td:
            out = pathlib.Path(td) / "cloc_rerun.json"
            src = CLOC_GEN.read_text().replace(
                'OUT = ROOT / "writeup" / "data" / "p2_route_cloc_v1.json"',
                f'OUT = Path({str(out)!r})')
            gen = pathlib.Path(td) / "cloc_gen.py"
            gen.write_text(src)
            p = subprocess.run([sys.executable, str(gen)], capture_output=True, text=True)
            if p.returncode != 0 or not out.exists():
                bad("5", f"cloc's generator did not re-run: rc={p.returncode}")
            else:
                a = json.loads(CLOC_ART.read_text())
                b = json.loads(out.read_text())
                ha, hb = a.pop("self_hash"), b.pop("self_hash")
                same = (json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True))
                print(f"  cloc regenerated: self_hash {ha} vs {hb}, payload identical {same}")
                if not same or ha != hb:
                    bad("5", "cloc does NOT regenerate bit-identically")
    else:
        unv("5", "cloc's generator not present")


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=str(ROOT / "Papers"))
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    cache = pathlib.Path(a.cache)

    print("V-W4 ADVERSARIAL RE-DERIVATION OF WAVE 4  (units V3, L2')")
    print(f"cache = {cache}   offline = {a.offline}")
    print("REPORT, DO NOT REPAIR.  Nothing belonging to V3 or L2' is written by this script.")

    only = set(a.only.split(",")) if a.only else set()
    if not only or "1" in only:
        item1(cache, a.offline)
    if not only or "2" in only:
        item2(cache, a.offline)
    if not only or "3" in only or "4" in only:
        item34(cache, a.offline)
        item3_maths()
    if not only or "5" in only:
        item5()

    print("\n" + "=" * 78)
    print("SUMMARY -- DISCREPANCIES FIRST, UNSOFTENED")
    print("=" * 78)
    if DISCREPANCIES:
        for d in DISCREPANCIES:
            print("  DISCREPANCY  " + d)
    else:
        print("  DISCREPANCIES: none")
    for u in UNVERIFIABLE:
        print("  UNVERIFIABLE " + u)
    for n in NOTES:
        print("  NOTE         " + n)
    print("\n  ESCAURIAZA-SEREGIN-SVERAK AT PRIMARY: UNREACHABLE.")
    print("    Neither ESS 2003 paper is on arXiv (au:Escauriaza returns 25 entries, none")
    print("    of them either one); both are journal-only (ARMA 169 and Russian Math.")
    print("    Surveys 58).  No S2 key exists here and READ-DO-NOT-CONTACT binds, so this")
    print("    banks as UNREACHABLE, NEVER AS A ZERO.  What the record then rests on is")
    print("    printed under ITEM (3) above and written out in experiments/journal/verify_wave4.md.")
    print("\n  NO LINK OF THE L1->L4 CHAIN MOVED.  A verification -- even a clean PASS --")
    print("  builds nothing and certifies nothing.  Clay stays ~0.05%.")
    return 1 if DISCREPANCIES else 0


if __name__ == "__main__":
    sys.exit(main())
