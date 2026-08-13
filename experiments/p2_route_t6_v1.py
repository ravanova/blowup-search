"""Leg 394 / Route-T6 -- fetch, at FULL TEXT, the seven papers leg 348 read at abstract level.

THE GATE (final wording, pre-committed by the Conductor, restated at
experiments/journal/leg_394.md sec 0.1; NOT re-scoped here)

    Read at FULL TEXT each of the seven papers leg 348 classified at abstract
    level.  For EACH, does the full text CONFIRM, STRENGTHEN, or UNDERCUT leg
    348's recorded classification of it?  Answer per paper, in a table, with the
    deciding sentence quoted verbatim and located by section or page.  A paper
    whose full text could not be obtained is banked as UNREACHABLE with the
    reason, NEVER as a confirmation.

WHAT THIS FILE IS

    The INSTRUMENT half only.  It fetches (a) the arXiv abstract of each of the
    seven ids -- needed because the pre-registered S-codes require showing a
    strengthening statement is ABSENT FROM THE ABSTRACT, measured in the same run
    rather than remembered -- and (b) the full-text PDF of each id, and extracts
    its text with pdftotext.  It banks a POSITIVE DATUM PROVING IT REACHED THE
    SERVICE on every record: HTTP status, byte count, sha256, extracted-character
    count, page count, and (for the API calls) the served opensearch namespace
    VERBATIM.

    It performs NO adjudication.  The confirm/strengthen/UNDERCUT/UNREACHABLE
    verdicts are made by a human reading the extracted text against sec 0.3's
    fixed rules and are written into the journal and, hand-checked, into the JSON
    by experiments/p2_route_t6_v1_adjudicate.py.

LEG 387'S BUG, AND THE RULE ADOPTED FROM IT

    Leg 387 hard-coded the opensearch namespace `1.0`; arXiv serves `1.1`; every
    response failed the harness's own well-formedness check and the leg REPORTED
    A ZERO -- clean, controlled, entirely fabricated.  THIS PARSER NAMES NO
    VERSION ANYWHERE.  The namespace is read out of the served bytes by a regex
    that matches whatever is there, and banked.  Any fetch that does not reach the
    service is banked THROTTLED or FAILED, NEVER as a zero and NEVER as
    a confirmation.

NO CONTACT.  HTTP GET only, against published-document endpoints.  No author,
group, maintainer or mailing list is contacted -- the outreach hold narrowed on
2026-08-13 authorises READING, not CONTACTING.

    .venv/bin/python experiments/p2_route_t6_v1.py
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "p2_route_t6_v1.json"
PAPERS = ROOT / "Papers"          # gitignored on purpose; PDFs are never committed
TEXTS = PAPERS / "t6_text"        # extracted text, also gitignored

ARXIV_API = "http://export.arxiv.org/api/query?"
ARXIV_PDF = "https://arxiv.org/pdf/"

DELAY_S = 12.0     # leg 348/392's spacing, kept; unauthenticated, pace politely
TIMEOUT_S = 120

# --- sec 0.2's seven, in the JSON's own order.  ids are read from leg 348's banked
# --- JSON at evidence time (control K10); this literal is the fetch order only.
SEVEN = [
    "math/0005247",
    "2305.08221",
    "1902.00384",
    "2409.09234",
    "2105.04148",
    "2009.12762",
    "2308.01528",
]

# K3, positive direction: a distinctive token that MUST appear in each full text.
# Pre-registered in the journal before the fetch.
K3_PRESENT = {
    "math/0005247": "Kuramoto",
    "2305.08221": "parabolic",
    "1902.00384": "Navier",
    "2409.09234": "Taylor",
    "2105.04148": "bifurcation",
    "2009.12762": "Navier",
    "2308.01528": "Hou",
}
# K3, negative direction: nonsense that MUST NOT appear anywhere.
K3_ABSENT = "zzqxjvbnmwkl"

# K4: the pre-registered UNDERCUT PROBE SET.  A hit is not automatically an
# undercut -- it routes a passage to adjudication.  If ZERO probes fire across
# ALL SEVEN papers the set is banked VACUOUS and the leg says so.
K4_PROBES = [
    "unbounded",
    "whole space",
    "R^3",
    "\\mathbb{R}^3",
    "real line",
    "Gaussian weight",
    "algebraic decay",
    "polynomial weight",
    "inviscid",
    "Euler equation",
    "two-dimensional reduction",
    "axisymmetric",
]

# Namespace-agnostic parsing.  NOTHING below names a namespace VERSION.
_NS = re.compile(r'xmlns:opensearch="([^"]+)"')
_TOTAL = re.compile(r"opensearch:totalResults[^>]*>(\d+)<")
_SUMMARY = re.compile(r"<summary>(.*?)</summary>", re.S)
_TITLE = re.compile(r"<title>(.*?)</title>", re.S)


def _clean(s: str) -> str:
    return " ".join(s.split())


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------------------
# ABSTRACT FETCH (arXiv API) -- needed for the S-code "absent from the abstract"
# half of control K5.
# ---------------------------------------------------------------------------
def fetch_abstract(arxiv_id: str, tries: int = 4) -> dict:
    url = ARXIV_API + urllib.parse.urlencode(
        {"search_query": f"id:{arxiv_id}", "max_results": 1, "start": 0}
    )
    rec = {
        "id": arxiv_id,
        "endpoint": "arxiv-api",
        "url": url,
        "status": None,
        "http": None,
        "bytes": None,
        "sha256": None,
        "opensearch_namespace_served": None,
        "total": None,
        "title": None,
        "abstract": None,
        "note": None,
    }
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "leg394-T6/1.0"})
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as fh:
                raw = fh.read()
                rec["http"] = fh.status
            break
        except urllib.error.HTTPError as exc:
            rec["http"] = exc.code
            if exc.code == 429 and attempt < tries - 1:
                time.sleep(DELAY_S * (attempt + 2))
                continue
            rec["status"] = "THROTTLED" if exc.code == 429 else "FAILED"
            rec["note"] = f"HTTPError {exc.code}"
            return rec
        except Exception as exc:  # noqa: BLE001
            if attempt < tries - 1:
                time.sleep(DELAY_S)
                continue
            rec["status"] = "FAILED"
            rec["note"] = f"{type(exc).__name__}: {exc}"
            return rec
    else:  # pragma: no cover
        rec["status"] = "FAILED"
        rec["note"] = "retries exhausted"
        return rec

    text = raw.decode("utf-8", "replace")
    rec["bytes"] = len(raw)
    rec["sha256"] = _sha(raw)
    ns = _NS.search(text)
    rec["opensearch_namespace_served"] = ns.group(1) if ns else None
    tot = _TOTAL.search(text)
    if tot is None:
        rec["status"] = "FAILED"
        rec["note"] = "200 but totalResults did not parse"
        return rec
    rec["total"] = int(tot.group(1))
    summ = _SUMMARY.search(text)
    titles = _TITLE.findall(text)
    rec["abstract"] = _clean(summ.group(1)) if summ else None
    rec["title"] = _clean(titles[1]) if len(titles) > 1 else None
    rec["status"] = "MEASURED"
    return rec


# ---------------------------------------------------------------------------
# FULL TEXT FETCH (arXiv PDF) + extraction
# ---------------------------------------------------------------------------
def fetch_fulltext(arxiv_id: str) -> dict:
    safe = arxiv_id.replace("/", "_")
    pdf = PAPERS / f"{safe}.pdf"
    txt = TEXTS / f"{safe}.txt"
    url = ARXIV_PDF + arxiv_id
    rec = {
        "id": arxiv_id,
        "endpoint": "arxiv-pdf",
        "url": url,
        "status": None,
        "http": None,
        "bytes": None,
        "sha256": None,
        "is_pdf_magic": None,
        "pages": None,
        "chars_extracted": None,
        "pdf_path": str(pdf.relative_to(ROOT)),
        "text_path": str(txt.relative_to(ROOT)),
        "k3_present_token": K3_PRESENT.get(arxiv_id),
        "k3_present_hits": None,
        "k3_absent_hits": None,
        "k4_probes_fired": None,
        "note": None,
    }

    if pdf.exists() and pdf.stat().st_size > 0:
        raw = pdf.read_bytes()
        rec["http"] = "cached"
    else:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "leg394-T6/1.0"})
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as fh:
                raw = fh.read()
                rec["http"] = fh.status
        except urllib.error.HTTPError as exc:
            rec["http"] = exc.code
            rec["status"] = "THROTTLED" if exc.code == 429 else "UNREACHABLE"
            rec["note"] = f"HTTPError {exc.code} on GET {url}"
            return rec
        except Exception as exc:  # noqa: BLE001
            rec["status"] = "UNREACHABLE"
            rec["note"] = f"{type(exc).__name__}: {exc} on GET {url}"
            return rec
        PAPERS.mkdir(exist_ok=True)
        pdf.write_bytes(raw)

    rec["bytes"] = len(raw)
    rec["sha256"] = _sha(raw)
    rec["is_pdf_magic"] = raw[:4] == b"%PDF"
    if not rec["is_pdf_magic"]:
        rec["status"] = "UNREACHABLE"
        rec["note"] = f"retrieved {len(raw)} bytes but they are not a PDF"
        return rec

    if shutil.which("pdftotext") is None:
        rec["status"] = "UNREACHABLE"
        rec["note"] = "pdftotext not available -- extraction impossible"
        return rec

    TEXTS.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["pdftotext", "-layout", str(pdf), str(txt)],
        capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0 or not txt.exists():
        rec["status"] = "UNREACHABLE"
        rec["note"] = f"pdftotext rc={proc.returncode}: {proc.stderr.strip()[:200]}"
        return rec

    body = txt.read_text("utf-8", "replace")
    rec["chars_extracted"] = len(body)
    rec["pages"] = body.count("\f")
    low = body.lower()
    rec["k3_present_hits"] = low.count((rec["k3_present_token"] or "").lower())
    rec["k3_absent_hits"] = low.count(K3_ABSENT)
    rec["k4_probes_fired"] = sorted(p for p in K4_PROBES if p.lower() in low)

    # K2: extraction sanity.  Below either threshold the paper is UNREACHABLE(parse),
    # NEVER a confirmation.
    if rec["chars_extracted"] < 20000 or rec["pages"] < 5:
        rec["status"] = "UNREACHABLE"
        rec["note"] = (
            f"parse: only {rec['chars_extracted']} chars / {rec['pages']} pages extracted "
            "(K2 floor 20000 chars and 5 pages)"
        )
        return rec

    rec["status"] = "MEASURED"
    return rec


def main() -> int:
    PAPERS.mkdir(exist_ok=True)
    TEXTS.mkdir(parents=True, exist_ok=True)

    out = {
        "leg": 394,
        "unit": "T6",
        "route": "ROUTE-T6",
        "role": "instrument only -- fetch and extract; adjudication is human, sec 0.3's fixed rules",
        "gate_question": (
            "Read at FULL TEXT each of the seven papers leg 348 classified at abstract level. "
            "For EACH, does the full text confirm, strengthen, or UNDERCUT leg 348's recorded "
            "classification of it? Answer per paper, in a table, with the deciding sentence quoted "
            "verbatim and located by section or page. A paper whose full text could not be obtained "
            "is banked as UNREACHABLE with the reason, never as a confirmation."
        ),
        "outreach": "READ ONLY. HTTP GET against published-document endpoints. No author, group, "
                    "maintainer or mailing list contacted. The 2026-08-13 narrowing authorises "
                    "reading, not contacting.",
        "parser_names_no_namespace_version": True,
        "k3_absent_probe": K3_ABSENT,
        "k4_probe_set": K4_PROBES,
        "abstracts": [],
        "fulltexts": [],
    }

    for i, pid in enumerate(SEVEN):
        if i:
            time.sleep(DELAY_S)
        rec = fetch_abstract(pid)
        print(f"[abs ] {pid:14s} {rec['status']:9s} http={rec['http']} "
              f"ns={rec['opensearch_namespace_served']} total={rec['total']}")
        out["abstracts"].append(rec)

    for pid in SEVEN:
        rec = fetch_fulltext(pid)
        print(f"[full] {pid:14s} {rec['status']:11s} http={rec['http']} "
              f"bytes={rec['bytes']} pages={rec['pages']} chars={rec['chars_extracted']} "
              f"k4={len(rec['k4_probes_fired'] or [])}")
        out["fulltexts"].append(rec)
        time.sleep(3.0)

    n_measured = sum(1 for r in out["fulltexts"] if r["status"] == "MEASURED")
    out["summary_fetch"] = {
        "n_fulltext_MEASURED": n_measured,
        "n_fulltext_UNREACHABLE": sum(1 for r in out["fulltexts"] if r["status"] == "UNREACHABLE"),
        "n_fulltext_THROTTLED": sum(1 for r in out["fulltexts"] if r["status"] == "THROTTLED"),
        "n_abstract_MEASURED": sum(1 for r in out["abstracts"] if r["status"] == "MEASURED"),
        "namespaces_served": sorted(
            {r["opensearch_namespace_served"] for r in out["abstracts"]
             if r["opensearch_namespace_served"]}
        ),
        "k4_any_probe_fired": any(r.get("k4_probes_fired") for r in out["fulltexts"]),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    print(json.dumps(out["summary_fetch"], indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
