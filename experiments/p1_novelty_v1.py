"""Leg 411 / `PB1` -- P1's OWED NOVELTY CHECK.  Instrument 1: candidate enumeration.

THE GATE (final wording, pre-registered at experiments/journal/leg_411.md Sec 0, not
re-worded here)

    Are EITHER of P1's two effects already in print:
      (a) that a SCALAR RECURRENCE SCORE USED AS AN ADMISSION FILTER BIASES THE
          RECOVERED ORBIT SET along any coordinate the score is monotone in; and
      (b) that RE-MINING A FIXED TRAJECTORY SILENTLY RE-FINDS what the first run
          already found?
    Search the Chandler-Kerswell / Lucas-Kerswell / Cvitanovic line and the wider
    recurrence-mining literature.  Answer PER EFFECT: is it in print -- YES or NO --
    and if YES, in which paper, at which page, stated how strongly?

WHAT THIS FILE IS, AND -- MORE IMPORTANTLY -- WHAT IT IS NOT

    THE arXiv API SEARCHES METADATA, NOT FULL TEXT.  `all:` covers title, abstract,
    authors and comments.  Both of P1's effects are the kind of remark that lives in
    a METHOD SECTION.  Therefore THIS FILE IS A CANDIDATE-ENUMERATION INSTRUMENT AND
    NOT AN ADJUDICATION INSTRUMENT, and AN ANDed ZERO FROM IT IS NEAR-WORTHLESS AS
    EVIDENCE OF ABSENCE.  That is declared in the pre-registration, before the run.
    Adjudication is instrument 2, `p1_novelty_fulltext_v1.py`, a full-text grep over
    fetched PDFs with its own planted controls.

    It is not an adjudication in a second sense either: Sec 0.5's grading rule is
    applied by a human read of full text, never by this script.

LEG 387'S FAILURE, WHICH THIS FILE EXISTS NOT TO REPEAT

    Leg 387 listed opensearch namespace `1.0` while arXiv serves `1.1`, refused every
    response, and REPORTED ZEROS.  So here:
      * the served namespace is banked VERBATIM FROM THE RAW FEED and the parser
        names no namespace version anywhere (regex on `opensearch:totalResults`);
      * MEASURED requires HTTP 200 AND a parsed totalResults; a 429 surviving
        backoff, a timeout, a non-200 or a parse failure is THROTTLED / FAILED and
        `total` is None BY CONSTRUCTION, so a non-measurement cannot be rendered as
        a zero by any downstream reader;
      * controls fire BEFORE any substantive verdict: generic positive, TOPICAL
        positive, nonsense negative that must be exactly 0, and AND-operator pairs.

    A pre-run probe returned HTTP 429 from Semantic Scholar on the first call, so
    throttling on that arm is EXPECTED and is reported as reduced coverage.

    CEILING: TIER 2.  No L1->L4 link moves.  Clay stays ~0.05%.  No figure.  No
    outreach of any kind.  No paywall circumvention.

    .venv/bin/python experiments/p1_novelty_v1.py
"""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "p1_novelty_v1.json"

# https: the http:// form 301-redirects, and a redirect is one more thing that can
# silently change what was measured.
ARXIV = "https://export.arxiv.org/api/query?"
S2 = "https://api.semanticscholar.org/graph/v1/paper/search?"

DELAY_S = 12.0
TIMEOUT_S = 60
MAX_RESULTS = 10

# NOTHING below names a namespace VERSION.  That is leg 387's exact bug and this is
# the fix.
_TOTAL = re.compile(r"opensearch:totalResults[^>]*>(\d+)<")
_NS = re.compile(r'xmlns:opensearch="([^"]+)"')
_ENTRY = re.compile(r"<entry>(.*?)</entry>", re.S)
_ID = re.compile(r"<id>https?://arxiv\.org/abs/([^<]+)</id>")
_TITLE = re.compile(r"<title>(.*?)</title>", re.S)
_SUMMARY = re.compile(r"<summary>(.*?)</summary>", re.S)
_JREF = re.compile(r"<arxiv:journal_ref[^>]*>(.*?)</arxiv:journal_ref>", re.S)
_DOI = re.compile(r"<arxiv:doi[^>]*>(.*?)</arxiv:doi>", re.S)
_PUB = re.compile(r"<published>([^<]+)</published>")


def _clean(s: str) -> str:
    return " ".join(s.split())


def arxiv_query(search_query: str, max_results: int = MAX_RESULTS, tries: int = 5) -> dict:
    """One arXiv query.  status in {MEASURED, THROTTLED, FAILED}; total is None
    unless MEASURED, BY CONSTRUCTION."""
    url = ARXIV + urllib.parse.urlencode(
        {"search_query": search_query, "max_results": max_results, "start": 0}
    )
    rec = {"query": search_query, "endpoint": "arxiv", "status": None, "http": None,
           "total": None, "n_entries": None, "opensearch_namespace_served": None,
           "hits": [], "note": None}
    raw = None
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=TIMEOUT_S) as resp:
                rec["http"] = resp.status
                raw = resp.read().decode("utf-8", "replace")
            break
        except urllib.error.HTTPError as exc:
            rec["http"] = exc.code
            if exc.code == 429 and attempt < tries - 1:
                wait = 20.0 * (attempt + 1)
                print(f"    [429 backoff {wait:.0f}s] {search_query}", flush=True)
                time.sleep(wait)
                continue
            rec["status"] = "THROTTLED" if exc.code == 429 else "FAILED"
            rec["note"] = f"HTTPError {exc.code}; NOT a zero"
            time.sleep(DELAY_S)
            return rec
        except Exception as exc:  # noqa: BLE001
            if attempt < tries - 1:
                time.sleep(15.0 * (attempt + 1))
                continue
            rec["status"] = "FAILED"
            rec["note"] = f"{type(exc).__name__}: {exc}; NOT a zero"
            time.sleep(DELAY_S)
            return rec

    ns = _NS.search(raw or "")
    rec["opensearch_namespace_served"] = ns.group(1) if ns else None
    m = _TOTAL.search(raw or "")
    if m is None:
        rec["status"] = "FAILED"
        rec["note"] = "HTTP 200 but totalResults did not parse; NOT a zero"
        time.sleep(DELAY_S)
        return rec

    rec["status"] = "MEASURED"
    rec["total"] = int(m.group(1))
    entries = _ENTRY.findall(raw)
    rec["n_entries"] = len(entries)
    for e in entries:
        i, t, s = _ID.search(e), _TITLE.search(e), _SUMMARY.search(e)
        j, d, p = _JREF.search(e), _DOI.search(e), _PUB.search(e)
        rec["hits"].append({
            "id": i.group(1) if i else None,
            "title": _clean(t.group(1)) if t else None,
            "published": p.group(1) if p else None,
            "journal_ref": _clean(j.group(1)) if j else None,
            "doi": _clean(d.group(1)) if d else None,
            "abstract": _clean(s.group(1)) if s else None,
        })
    time.sleep(DELAY_S)
    return rec


def s2_query(q: str, limit: int = 10, tries: int = 4) -> dict:
    """Semantic Scholar.  Same contract.  Present for ONE reason: the venue class
    an arXiv-only pass cannot see -- reviews, book chapters and pre-arXiv journal
    papers, which is exactly where methodological folklore gets written down."""
    url = S2 + urllib.parse.urlencode(
        {"query": q, "limit": limit,
         "fields": "title,year,venue,externalIds,abstract,publicationTypes"})
    rec = {"query": q, "endpoint": "semanticscholar", "status": None, "http": None,
           "total": None, "n_entries": None, "hits": [], "note": None}
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "unsolved-leg411/1.0"})
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
                rec["http"] = resp.status
                data = json.loads(resp.read().decode("utf-8", "replace"))
            rec["status"] = "MEASURED"
            rec["total"] = data.get("total")
            for h in (data.get("data", []) or []):
                ext = h.get("externalIds") or {}
                rec["hits"].append({"title": h.get("title"), "year": h.get("year"),
                                    "venue": h.get("venue"), "doi": ext.get("DOI"),
                                    "arxiv": ext.get("ArXiv"),
                                    "types": h.get("publicationTypes"),
                                    "abstract": (h.get("abstract") or "")[:1500] or None})
            rec["n_entries"] = len(rec["hits"])
            time.sleep(5.0)
            return rec
        except urllib.error.HTTPError as exc:
            rec["http"] = exc.code
            if exc.code == 429 and attempt < tries - 1:
                time.sleep(25.0 * (attempt + 1))
                continue
            rec["status"] = "THROTTLED" if exc.code == 429 else "FAILED"
            rec["note"] = f"HTTPError {exc.code}; NOT a zero"
            time.sleep(5.0)
            return rec
        except Exception as exc:  # noqa: BLE001
            if attempt < tries - 1:
                time.sleep(12.0 * (attempt + 1))
                continue
            rec["status"] = "FAILED"
            rec["note"] = f"{type(exc).__name__}: {exc}; NOT a zero"
            time.sleep(5.0)
            return rec
    return rec


# ---------------------------------------------------------------------------
# CONTROLS -- pre-registered at journal Sec 0.2, fire BEFORE any substantive query
# ---------------------------------------------------------------------------
CONTROLS = [
    ("pos_generic", 'all:"Navier-Stokes"', lambda n: n >= 1000,
     "generic positive: must return thousands, else the endpoint is not answering"),
    ("pos_topical", 'all:"exact coherent structures"', lambda n: n >= 50,
     "TOPICAL positive control -- IN THIS LITERATURE, not a generic one.  If the endpoint "
     "cannot see this field's own name, its zeros about this field mean nothing"),
    ("pos_topical_2", 'all:"unstable periodic orbits" AND all:"turbulence"', lambda n: n >= 20,
     "second topical positive, on the exact object P1 is about"),
    ("neg_nonsense", 'all:"recurrence-filtered shadowing bias of the Grznarov admission funnel"',
     lambda n: n == 0,
     "invented phrase; MUST be exactly 0.  If nonzero the endpoint is fuzzy-matching and every "
     "zero below is uninterpretable"),
    ("and_pair_generic", 'all:"periodic orbit" AND all:"turbulence"', lambda n: n > 0,
     "THE AND TEST: two phrases certain to intersect.  If 0, every ANDed zero below is an "
     "instrument artifact, not a measurement"),
    ("and_pair_topical", 'all:"Kolmogorov flow" AND all:"periodic orbits"', lambda n: n > 0,
     "second AND control, in this leg's own topical vocabulary -- proves the operator works on "
     "the words actually being ANDed below"),
    ("and_pair_effect_vocab", 'all:"recurrent flow" AND all:"turbulence"', lambda n: n > 0,
     "third AND control, on the phrase the effect batteries lean on hardest"),
]

# DOMAIN positive control -- pre-registered at journal Sec 0.3.
DOMAIN_CONTROL_IDS = {
    "chandler_kerswell_2013": "1207.4682",
    "lucas_kerswell_2015": "1406.1820",
    "viswanath_2007": "physics/0604062",
}

# ---------------------------------------------------------------------------
# THE QUERY SET -- fixed before any query was issued
#   D = domain control battery (must re-find the three ids above)
#   A = effect (a): admission filter biases the recovered set
#   B = effect (b): re-mining re-finds
#   W = the wider recurrence-mining / cycle-search literature
# ---------------------------------------------------------------------------
BATTERIES = {
    "D_domain": [
        'au:"Chandler" AND au:"Kerswell"',
        'au:"Lucas" AND au:"Kerswell"',
        'au:"Viswanath" AND all:"periodic"',
        'all:"Kolmogorov flow" AND all:"invariant solutions"',
        'all:"recurrent flow analysis"',
    ],
    "A_bias": [
        'all:"periodic orbits" AND all:"bias"',
        'all:"invariant solutions" AND all:"bias"',
        'all:"periodic orbit" AND all:"selection bias"',
        'all:"recurrence" AND all:"bias" AND all:"turbulence"',
        'all:"biased" AND all:"exact coherent structures"',
        'all:"near-recurrence" AND all:"periodic orbits"',
        'all:"recurrence threshold" AND all:"periodic orbits"',
        'all:"residual" AND all:"guess" AND all:"periodic orbits"',
        'all:"short period" AND all:"periodic orbit" AND all:"turbulence"',
        'all:"sampling bias" AND all:"invariant solutions"',
        'all:"detection bias" AND all:"periodic orbits"',
        'all:"which solutions are found" AND all:"turbulence"',
    ],
    "B_refind": [
        'all:"periodic orbits" AND all:"duplicates"',
        'all:"periodic orbits" AND all:"diminishing returns"',
        'all:"distinct solutions" AND all:"converged" AND all:"turbulence"',
        'all:"repeatedly converge" AND all:"periodic orbits"',
        'all:"same solutions" AND all:"periodic orbit search"',
        'all:"saturation" AND all:"number of periodic orbits"',
        'all:"rediscover" AND all:"periodic orbits"',
        'all:"redundant" AND all:"periodic orbit" AND all:"search"',
        'all:"unique" AND all:"converged" AND all:"recurrent flows"',
    ],
    "W_wider": [
        'all:"cycle search" AND all:"periodic orbits"',
        'all:"periodic orbit" AND all:"completeness" AND all:"cycle expansion"',
        'all:"close return" AND all:"periodic orbit"',
        'all:"recurrence plot" AND all:"unstable periodic orbit"',
        'all:"Newton" AND all:"hookstep" AND all:"turbulence"',
        'all:"convolutional autoencoder" AND all:"periodic orbits"',
        'all:"machine learning" AND all:"exact coherent structures"',
        'all:"adjoint" AND all:"invariant solutions" AND all:"Navier-Stokes"',
        'all:"variational method" AND all:"periodic orbits" AND all:"turbulence"',
        'all:"pipe flow" AND all:"travelling waves" AND all:"search"',
    ],
}

S2_QUERIES = [
    ("s2_pos_generic", "Navier-Stokes equations", "positive control"),
    ("s2_pos_topical", "exact coherent structures turbulence", "TOPICAL positive control"),
    ("s2_neg_nonsense", "Grznarov admission funnel recurrence shadowing bias",
     "nonsense negative control, must be 0"),
    ("s2_a1", "bias recurrent flow analysis periodic orbits turbulence", "effect (a)"),
    ("s2_a2", "recurrence measure threshold selection invariant solutions bias", "effect (a)"),
    ("s2_b1", "duplicate converged periodic orbits recurrent flow analysis", "effect (b)"),
    ("s2_b2", "diminishing returns new periodic orbits longer simulation", "effect (b)"),
    ("s2_rev", "significance of simple invariant solutions in turbulent flows review",
     "the REVIEW venue class an arXiv-only pass cannot see"),
]


def main() -> None:
    rec = {
        "leg": 411, "unit": "PB1", "wave": 8,
        "gate": ("Are either of P1's two effects already in print: (a) a scalar recurrence "
                 "score used as an admission filter biases the recovered orbit set along any "
                 "coordinate the score is monotone in; (b) re-mining a fixed trajectory "
                 "silently re-finds what the first run already found?"),
        "instrument_role": ("CANDIDATE ENUMERATION ONLY.  The arXiv API searches metadata, not "
                            "full text; both effects are method-section statements.  An ANDed "
                            "zero here is NEAR-WORTHLESS as evidence of absence.  Adjudication "
                            "is instrument 2 (p1_novelty_fulltext_v1.py)."),
        "throttled_is_never_a_zero": True,
        "controls": [], "domain_control": {}, "batteries": {}, "s2": [],
    }

    print("== CONTROLS (fire before any substantive query) ==", flush=True)
    for name, q, pred, why in CONTROLS:
        r = arxiv_query(q, max_results=3)
        fired = (r["status"] == "MEASURED") and bool(pred(r["total"]))
        r.update({"control": name, "why": why, "fired_as_planted": fired})
        rec["controls"].append(r)
        print(f"  {name:22s} {r['status']:9s} total={r['total']}  fired={fired}", flush=True)

    print("== BATTERIES ==", flush=True)
    for bname, qs in BATTERIES.items():
        rec["batteries"][bname] = []
        for q in qs:
            r = arxiv_query(q)
            rec["batteries"][bname].append(r)
            print(f"  [{bname}] {r['status']:9s} total={r['total']:>6} :: {q}", flush=True)

    # DOMAIN CONTROL: did the batteries actually surface the three ids?
    seen = set()
    for bl in rec["batteries"].values():
        for r in bl:
            for h in r["hits"]:
                if h["id"]:
                    seen.add(h["id"].split("v")[0])
    for k, v in DOMAIN_CONTROL_IDS.items():
        rec["domain_control"][k] = {"id": v, "re_found": v in seen}
    rec["domain_control"]["_ids_seen_total"] = len(seen)
    print("== DOMAIN CONTROL ==", flush=True)
    for k, v in DOMAIN_CONTROL_IDS.items():
        print(f"  {k:26s} {v:16s} re_found={rec['domain_control'][k]['re_found']}", flush=True)

    print("== SEMANTIC SCHOLAR (429 EXPECTED; throttles are NOT zeros) ==", flush=True)
    for name, q, why in S2_QUERIES:
        r = s2_query(q)
        r.update({"control": name, "why": why})
        rec["s2"].append(r)
        print(f"  {name:18s} {r['status']:9s} total={r['total']}", flush=True)

    # Summary counts.  THROTTLED and FAILED are counted SEPARATELY and are never
    # folded into a zero anywhere.
    def tally(records):
        return {
            "n": len(records),
            "MEASURED": sum(1 for r in records if r["status"] == "MEASURED"),
            "THROTTLED": sum(1 for r in records if r["status"] == "THROTTLED"),
            "FAILED": sum(1 for r in records if r["status"] == "FAILED"),
            "measured_zeros": sum(1 for r in records
                                  if r["status"] == "MEASURED" and r["total"] == 0),
        }

    arx = rec["controls"] + [r for bl in rec["batteries"].values() for r in bl]
    rec["tally"] = {"arxiv": tally(arx), "semanticscholar": tally(rec["s2"])}
    ns = {r["opensearch_namespace_served"] for r in arx
          if r["opensearch_namespace_served"] is not None}
    rec["opensearch_namespace_served_verbatim"] = sorted(ns)
    rec["controls_all_fired"] = all(c["fired_as_planted"] for c in rec["controls"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rec, indent=2))
    print(f"\nwrote {OUT}")
    print(f"arxiv   {rec['tally']['arxiv']}")
    print(f"s2      {rec['tally']['semanticscholar']}")
    print(f"namespace served (verbatim from feed): {rec['opensearch_namespace_served_verbatim']}")
    print(f"controls_all_fired = {rec['controls_all_fired']}")


if __name__ == "__main__":
    main()
