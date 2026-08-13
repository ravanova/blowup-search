"""Leg 392 / Route-TRIG -- T2: search the PERIODIC (`T^3`) rigidity literature.

THE GATE (final wording, pre-registered at experiments/journal/leg_392.md §0, not
re-scoped here)

    Does the search locate a PUBLISHED THEOREM excluding a finite-time singularity
    for 3D Navier-Stokes on T^3 of the shape Lane T would need -- a periodic/torus
    analogue of the Necas-Ruzicka-Sverak / Tsai rigidity results?

WHY THIS RUNNER EXISTS AT ALL, AND WHY IT IS NOT A HAND-TYPED LITERATURE VERDICT

    Leg 387 FABRICATED A CONTROLLED ZERO.  Its harness listed opensearch namespace
    `1.0` while arXiv serves `1.1`, so it REFUSED every response -- a `len(entries)`
    implementation would have reported "0 results, no prior art" on precisely the
    question the leg existed to answer.  Leg 387 also hit HTTP 429.  Leg 315 banked
    six all-zero ANDed queries as an endpoint defect leg 314 could not reproduce.

    Therefore this file, and not a paragraph of prose, is the leg's instrument:

      * the opensearch namespace ACTUALLY SERVED is banked verbatim from the raw
        feed, and the parser is namespace-agnostic by construction (regex on
        `opensearch:totalResults`, no XML namespace map anywhere);
      * every query carries a per-query STATUS, and MEASURED requires HTTP 200 AND
        a parsed totalResults.  A 429 that survives backoff, a timeout, a non-200 or
        a parse failure is THROTTLED/FAILED and is NEVER rendered as a zero;
      * controls fire BEFORE any substantive verdict: positive, negative-nonsense,
        and an AND-operator pair known to intersect;
      * a DOMAIN positive control: the query set must RE-FIND the R^3 rigidity
        papers this repository already screened (2607.09619, 1304.7414, 2006.15776).
        If it cannot surface the R^3 originals it cannot be trusted to surface a
        periodic analogue, and its null is UNDER-RESOURCED, not `no`.

    Row 1's own sources -- Necas-Ruzicka-Sverak, Acta Math. 176 (1996) and Tsai,
    ARMA 143 (1998) -- are PRE-arXiv and were declared UNREACHABLE BY THIS
    INSTRUMENT in the pre-registration, before the run.  That is a hard coverage
    limit of an arXiv-first pass, not a zero.

WHAT THIS RUNNER IS NOT

    It is not an adjudication.  It measures; §0.5's K1-K4 rule is applied to the
    banked abstracts in the evidence script and the journal.  It builds no solver,
    adds no capabilities.py row, produces NO FIGURE (legs 334/348 precedent), and
    edits nothing outside its own territory.  CEILING: TIER 2.  No L1->L4 link
    moves.  Clay stays ~0.05%.  CLAY_OBLIGATIONS.md §6's two no-method obligations
    stay OPEN.

    NO EXTERNAL OUTREACH (standing user hold): arXiv and Semantic Scholar APIs
    only.  No author is contacted.  Statement (D)'s data conditions (8) and (9)
    stay UNREAD -- they need outreach, and this leg raises that rather than routing
    around it.

    .venv/bin/python experiments/p2_route_trig_v1.py
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "p2_route_trig_v1.json"

ARXIV = "http://export.arxiv.org/api/query?"
S2 = "https://api.semanticscholar.org/graph/v1/paper/search?"

DELAY_S = 12.0        # leg 348's spacing, kept
TIMEOUT_S = 60
MAX_RESULTS = 8

# Namespace-agnostic parsing.  NOTHING here names a namespace VERSION -- that is
# leg 387's exact bug and this line is the fix.
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


# ---------------------------------------------------------------------------
# THE INSTRUMENT
# ---------------------------------------------------------------------------
def arxiv_query(search_query: str, max_results: int = MAX_RESULTS, tries: int = 5) -> dict:
    """One arXiv API query.

    Returns a record whose `status` is one of:
        MEASURED    -- HTTP 200 and totalResults parsed.  `total` is a real count.
        THROTTLED   -- HTTP 429 survived the backoff.  `total` is None.
        FAILED      -- any other error, or a 200 whose totalResults did not parse.
                       `total` is None.
    `total` is None in every non-MEASURED case BY CONSTRUCTION, so a downstream
    reader cannot silently turn a non-measurement into a zero.
    """
    url = ARXIV + urllib.parse.urlencode(
        {"search_query": search_query, "max_results": max_results, "start": 0}
    )
    rec = {
        "query": search_query,
        "endpoint": "arxiv",
        "status": None,
        "http": None,
        "total": None,
        "n_entries": None,
        "opensearch_namespace_served": None,
        "hits": [],
        "note": None,
    }
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
        except Exception as exc:  # noqa: BLE001 -- timeouts, DNS, resets
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
        i = _ID.search(e)
        t = _TITLE.search(e)
        s = _SUMMARY.search(e)
        j = _JREF.search(e)
        d = _DOI.search(e)
        p = _PUB.search(e)
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


def s2_query(q: str, limit: int = 8, tries: int = 4) -> dict:
    """One Semantic Scholar query.  Same MEASURED / THROTTLED / FAILED contract.

    Semantic Scholar is in the plan for one reason: row 1's own sources
    (NRS 1996, Tsai 1998) are PRE-arXiv, so an arXiv-only pass cannot see the
    venue class the gate's word `published` lives in.  A pre-run probe from this
    environment returned HTTP 429 on the first call, so throttling here is
    EXPECTED and is reported as reduced coverage, never as absence.
    """
    url = S2 + urllib.parse.urlencode(
        {"query": q, "limit": limit,
         "fields": "title,year,venue,externalIds,abstract,publicationTypes"}
    )
    rec = {"query": q, "endpoint": "semanticscholar", "status": None, "http": None,
           "total": None, "n_entries": None, "hits": [], "note": None}
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "unsolved-leg392/1.0"})
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
                rec["http"] = resp.status
                data = json.loads(resp.read().decode("utf-8", "replace"))
            rec["status"] = "MEASURED"
            rec["total"] = data.get("total")
            hits = data.get("data", []) or []
            rec["n_entries"] = len(hits)
            for h in hits:
                ext = h.get("externalIds") or {}
                rec["hits"].append({
                    "title": h.get("title"),
                    "year": h.get("year"),
                    "venue": h.get("venue"),
                    "doi": ext.get("DOI"),
                    "arxiv": ext.get("ArXiv"),
                    "types": h.get("publicationTypes"),
                    "abstract": (h.get("abstract") or "")[:1200] or None,
                })
            time.sleep(4.0)
            return rec
        except urllib.error.HTTPError as exc:
            rec["http"] = exc.code
            if exc.code == 429 and attempt < tries - 1:
                time.sleep(20.0 * (attempt + 1))
                continue
            rec["status"] = "THROTTLED" if exc.code == 429 else "FAILED"
            rec["note"] = f"HTTPError {exc.code}; NOT a zero"
            time.sleep(4.0)
            return rec
        except Exception as exc:  # noqa: BLE001
            if attempt < tries - 1:
                time.sleep(10.0 * (attempt + 1))
                continue
            rec["status"] = "FAILED"
            rec["note"] = f"{type(exc).__name__}: {exc}; NOT a zero"
            time.sleep(4.0)
            return rec
    return rec


# ---------------------------------------------------------------------------
# THE QUERY SET -- pre-registered at journal §0.4, committed before it was run
# ---------------------------------------------------------------------------
CONTROLS = [
    ("pos_broad", 'all:"Navier-Stokes"', lambda n: n >= 1000,
     "a phrase that must return thousands; if this is small the endpoint is not answering"),
    ("pos_topic", 'all:"Liouville theorem"', lambda n: n >= 100,
     "second positive control, on this leg's own topic vocabulary"),
    ("neg_nonsense", 'all:"quasiperiodic rigidity of the Zlatohorsky enclosure torus"',
     lambda n: n == 0,
     "a phrase that must return nothing; if this is nonzero the endpoint is fuzzy-matching "
     "and every zero below is uninterpretable"),
    ("and_pair", 'all:"Liouville theorem" AND all:"Navier-Stokes"', lambda n: n > 0,
     "THE AND TEST: two exact phrases known to intersect. If 0, every ANDed zero below is "
     "an instrument artifact, not a measurement"),
    ("and_pair_b", 'all:"Navier-Stokes" AND all:"torus"', lambda n: n > 0,
     "second AND control, on this leg's own domain word"),
]

# The DOMAIN positive control: the ids the query set MUST re-find.  Pre-registered
# at journal §0.3.  Row 1 (NRS 1996 / Tsai 1998) is PRE-arXiv and is declared
# unreachable by this instrument in advance -- not a zero.
DOMAIN_CONTROL_IDS = {
    "row2_pineau_vicol": "2607.09619",
    "row3_chae_tsai": "1304.7414",
    "row4_jiu_wang_wei_morrey": "2006.15776",
}
DOMAIN_CONTROL_UNREACHABLE = {
    "row1_necas_ruzicka_sverak_1996": "Acta Math. 176 (1996) 283-294 -- PRE-arXiv, no eprint",
    "row1_tsai_1998": "Arch. Ration. Mech. Anal. 143 (1998) 29-51 -- PRE-arXiv, no eprint",
}

QUERIES = {
    # A -- the direct question: a torus/periodic rigidity or Liouville theorem for NS
    "A_direct_torus_rigidity": [
        'all:"Navier-Stokes" AND all:"torus" AND all:"Liouville"',
        'all:"Navier--Stokes" AND all:"torus" AND all:"Liouville"',
        'all:"Liouville type theorem" AND all:"periodic"',
        'all:"ancient solutions" AND all:"Navier-Stokes"',
        'all:"ancient solutions" AND all:"torus"',
        'all:"Navier-Stokes" AND all:"periodic boundary conditions" AND all:"blow-up"',
        'all:"three-torus" AND all:"Navier-Stokes" AND all:"regularity"',
        'all:"rigidity" AND all:"Navier-Stokes" AND all:"periodic"',
    ],
    # B -- row 1's counterpart: backward self-similar rigidity (NRS / Tsai)
    "B_row1_backward_self_similar": [
        'all:"backward self-similar"',
        'all:"backward self-similar" AND all:"Navier-Stokes"',
        'all:"backward self-similar" AND all:"periodic"',
        'all:"self-similar" AND all:"Navier-Stokes" AND all:"torus"',
        'all:"self-similar" AND all:"Navier--Stokes" AND all:"torus"',
    ],
    # D -- row 2's counterpart: DSS / Type I (Chae-Wolf, Pineau-Vicol)
    "D_row2_dss_typeI": [
        'all:"discretely self-similar" AND all:"Navier-Stokes"',
        'all:"discretely self-similar" AND all:"periodic"',
        'all:"Type I" AND all:"Navier-Stokes" AND all:"blow-up"',
        'all:"Type I" AND all:"Navier-Stokes" AND all:"torus"',
        'all:"Type I blowup" AND all:"periodic"',
    ],
    # E -- row 3's counterpart: time-periodic / self-similar Euler (Chae-Tsai)
    "E_row3_time_periodic": [
        'all:"time periodic" AND all:"Euler equations" AND all:"self-similar"',
        'all:"time-periodic" AND all:"Navier-Stokes" AND all:"torus"',
        'all:"self-similar" AND all:"Euler equations" AND all:"periodic"',
    ],
    # F -- row 4's counterpart: Morrey-space Liouville
    "F_row4_morrey": [
        'all:"Morrey" AND all:"Navier-Stokes" AND all:"Liouville"',
        'all:"Morrey space" AND all:"periodic"',
        'all:"Morrey" AND all:"torus" AND all:"Navier-Stokes"',
    ],
    # G -- THE BRANCH (b) TEST: broader-class exclusions on the torus.  A theorem
    #      here excluding singularity for a general bounded-energy periodic solution
    #      under a scaling-invariant smallness/regularity hypothesis BITES Lane T.
    "G_broader_class_on_the_torus": [
        'all:"global regularity" AND all:"Navier-Stokes" AND all:"torus"',
        'all:"global regularity" AND all:"Navier-Stokes" AND all:"periodic"',
        'all:"regularity criterion" AND all:"Navier-Stokes" AND all:"periodic"',
        'all:"blow-up criterion" AND all:"Navier-Stokes" AND all:"torus"',
        'all:"small initial data" AND all:"Navier-Stokes" AND all:"torus"',
        'all:"finite time singularity" AND all:"Navier-Stokes" AND all:"torus"',
        'all:"Serrin" AND all:"Navier-Stokes" AND all:"periodic"',
        'all:"Beale-Kato-Majda" AND all:"torus"',
    ],
}

S2_QUERIES = {
    "S_controls": [
        ("pos", "Navier-Stokes equations", lambda n: n is not None and n >= 1000),
        ("neg", "quasiperiodic rigidity of the Zlatohorsky enclosure torus",
         lambda n: n == 0),
    ],
    "S_substantive": [
        "Liouville theorem Navier-Stokes torus",
        "backward self-similar solutions Navier-Stokes nonexistence",
        "Liouville theorem periodic Navier-Stokes ancient solutions",
        "no finite time blow-up Navier-Stokes periodic boundary conditions",
        "Type I blowup Navier-Stokes torus",
        "Morrey space Liouville theorem Navier-Stokes",
    ],
}


def main() -> int:
    rec = {
        "leg": 392,
        "route": "TRIG",
        "unit": "T2 (WAVE 1, CONDUCTOR §3g), LANE T",
        "title": "the periodic (T^3) rigidity literature -- is a torus blow-up target already "
                 "excluded by a published theorem?",
        "date": time.strftime("%Y-%m-%d"),
        "gate_final_wording": (
            "Does the search locate a PUBLISHED THEOREM excluding a finite-time singularity for "
            "3D Navier-Stokes on T^3 of the shape Lane T would need -- a periodic/torus analogue "
            "of the Necas-Ruzicka-Sverak / Tsai rigidity results?"
        ),
        "ceiling": "TIER 2. No L1->L4 link moves. Clay ~0.05%. CLAY_OBLIGATIONS.md §6's two "
                   "no-method obligations stay OPEN; Lane T does not retire them (leg 390).",
        "no_outreach": "standing user hold: arXiv and Semantic Scholar APIs only; no author "
                       "contacted. (D)'s data conditions (8) and (9) stay UNREAD.",
        "figure": "NONE -- a pure-literature scoping leg declares no figure (legs 334, 348). "
                  "writeup/build_figures.py is not edited by this leg.",
        "instrument_contract": {
            "MEASURED": "HTTP 200 AND totalResults parsed; `total` is a real count",
            "THROTTLED": "HTTP 429 survived backoff; `total` is None, NEVER a zero",
            "FAILED": "any other error, or 200 with unparsable totalResults; `total` is None",
            "namespace": "parser is namespace-agnostic BY CONSTRUCTION (regex on "
                         "opensearch:totalResults). The namespace ACTUALLY SERVED is banked "
                         "per query. This is leg 387's exact bug, checked rather than assumed.",
            "spacing_s": DELAY_S,
        },
        "domain_positive_control": {
            "must_refind_ids": DOMAIN_CONTROL_IDS,
            "declared_unreachable_in_advance": DOMAIN_CONTROL_UNREACHABLE,
            "why": "if the query set cannot surface the R^3 originals this repository already "
                   "screened, it cannot be trusted to surface a periodic analogue, and its null "
                   "is UNDER-RESOURCED (§3d), not `no`.",
        },
        "controls": [],
        "controls_all_passed": None,
        "and_operator_verdict": None,
        "queries": {},
        "s2": {"controls": [], "substantive": []},
        "coverage": {},
    }

    print("== INSTRUMENT CONTROLS (arXiv) ==", flush=True)
    all_ok = True
    for name, q, pred, why in CONTROLS:
        r = arxiv_query(q, max_results=3)
        ok = (r["status"] == "MEASURED") and pred(r["total"])
        all_ok = all_ok and ok
        r.update({"control": name, "why": why, "passed": ok})
        rec["controls"].append(r)
        print(f"  {name:14s} {r['status']:9s} total={r['total']} passed={ok}  ns="
              f"{r['opensearch_namespace_served']}", flush=True)
    rec["controls_all_passed"] = all_ok

    and_ok = all(c["passed"] for c in rec["controls"] if c["control"].startswith("and_"))
    rec["and_operator_verdict"] = (
        "AND WORKS -- an ANDed zero below is a MEASUREMENT (absence)" if and_ok else
        "AND BROKEN -- every ANDed zero below is UNINTERPRETABLE and is banked as FAILED-BY-"
        "INSTRUMENT, not as absence"
    )
    print(f"  AND verdict: {rec['and_operator_verdict']}", flush=True)

    if not all_ok:
        print("  CONTROLS FAILED -- the substantive batteries still run, but every result is "
              "banked under a failed-control flag and NO verdict may be read off them.",
              flush=True)

    print("\n== SUBSTANTIVE BATTERIES (arXiv) ==", flush=True)
    for battery, qs in QUERIES.items():
        rec["queries"][battery] = []
        print(f"-- {battery}", flush=True)
        for q in qs:
            r = arxiv_query(q)
            rec["queries"][battery].append(r)
            print(f"   {r['status']:9s} total={str(r['total']):>6s}  {q}", flush=True)

    print("\n== SEMANTIC SCHOLAR (venue coverage arXiv cannot give) ==", flush=True)
    for name, q, pred in S2_QUERIES["S_controls"]:
        r = s2_query(q, limit=3)
        r["control"] = name
        r["passed"] = (r["status"] == "MEASURED") and pred(r["total"])
        rec["s2"]["controls"].append(r)
        print(f"  {name:5s} {r['status']:9s} total={r['total']} passed={r['passed']}", flush=True)
    for q in S2_QUERIES["S_substantive"]:
        r = s2_query(q)
        rec["s2"]["substantive"].append(r)
        print(f"  {r['status']:9s} total={str(r['total']):>8s}  {q}", flush=True)

    # ---- coverage, computed, never asserted -------------------------------
    flat = [r for b in rec["queries"].values() for r in b]
    n_planned = len(flat)
    n_measured = sum(1 for r in flat if r["status"] == "MEASURED")
    n_throttled = sum(1 for r in flat if r["status"] == "THROTTLED")
    n_failed = sum(1 for r in flat if r["status"] == "FAILED")
    measured_zeros = [r["query"] for r in flat if r["status"] == "MEASURED" and r["total"] == 0]

    s2_flat = rec["s2"]["controls"] + rec["s2"]["substantive"]
    s2_measured = sum(1 for r in s2_flat if r["status"] == "MEASURED")

    ids_seen = sorted({h["id"].split("v")[0] for b in rec["queries"].values() for r in b
                       for h in r["hits"] if h.get("id")})
    refound = {k: (v in ids_seen) for k, v in DOMAIN_CONTROL_IDS.items()}

    rec["coverage"] = {
        "arxiv_queries_planned": n_planned,
        "arxiv_queries_MEASURED": n_measured,
        "arxiv_queries_THROTTLED": n_throttled,
        "arxiv_queries_FAILED": n_failed,
        "arxiv_fraction_executed": round(n_measured / n_planned, 4) if n_planned else None,
        "arxiv_measured_zeros": measured_zeros,
        "arxiv_measured_zero_count": len(measured_zeros),
        "did_not_measure_count": n_throttled + n_failed,
        "s2_queries_planned": len(s2_flat),
        "s2_queries_MEASURED": s2_measured,
        "distinct_arxiv_ids_surfaced": len(ids_seen),
        "domain_control_refound": refound,
        "domain_control_all_refound": all(refound.values()),
        "namespaces_served": sorted({r["opensearch_namespace_served"] for r in flat
                                     if r.get("opensearch_namespace_served")}),
        "hard_coverage_limits": [
            "NRS (Acta Math. 1996) and Tsai (ARMA 1998) are PRE-arXiv: row 1's own sources are "
            "unreachable by the arXiv instrument. Declared in advance (journal §0.3).",
            "No MathSciNet / zbMATH / Crossref query: the pre-committed reading names arXiv and "
            "Semantic Scholar only.",
            "Abstract-level reading only; no PDF or LaTeX source fetched this leg.",
            "NO OUTREACH: (D)'s data conditions (8),(9) stay UNREAD.",
        ],
    }

    OUT.write_text(json.dumps(rec, indent=1) + "\n")
    print(f"\nwrote {OUT}", flush=True)
    print(f"coverage: {n_measured}/{n_planned} arXiv queries MEASURED, "
          f"{n_throttled} THROTTLED, {n_failed} FAILED; "
          f"{len(measured_zeros)} MEASURED zeros; "
          f"domain control re-found: {refound}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
