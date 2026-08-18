#!/usr/bin/env python3
"""Leg 397 (unit L2', lane L) -- STEP 1 of 3: the arXiv search instrument.

Runs the queries pre-registered in experiments/journal/leg_397.md SS2.3, with the
two controls of SS2.2 planted BEFORE the run, and banks a per-query positive datum
for every single query:

    url, http status, the SERVED opensearch namespace URI, opensearch:totalResults,
    entries parsed, and the arXiv ids returned.

WHY THE PARSER IS NAMESPACE-AGNOSTIC (SS2.2, and leg 387's fabricated zero).  arXiv
serves the opensearch namespace `http://a9.com/-/spec/opensearch/1.1/`.  A harness
that hard-codes `.../1.0/` matches nothing, reads zero entries, and reports a clean
negative that is actually a broken instrument.  This parser therefore matches on
LOCAL TAG NAME ONLY (`tag.split('}')[-1]`) and banks the served namespace URI as
evidence the source was reached.

A query that raises, times out, or returns no parsable totalResults is banked
`UNREACHABLE`; an HTTP 429 is banked `THROTTLED`.  Neither is ever a zero.

    python3 experiments/p2_route_l2_v1_search.py
"""
from __future__ import annotations

import json
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

API = "http://export.arxiv.org/api/query?"
TIMEOUT_S = 40
PACE_S = 3.5          # unauthenticated; arXiv asks for >= 3s between hits
OUT = pathlib.Path(__file__).resolve().parent.parent / "writeup" / "data" / "p2_route_l2_search_v1.json"


def _local(tag: str) -> str:
    return tag.split("}")[-1]


def _ns_of(tag: str) -> str:
    return tag[1:].split("}")[0] if tag.startswith("{") else ""


def query(label: str, search: str, max_results: int = 25) -> dict:
    """One arXiv query.  Returns a banked record -- never a bare count."""
    url = API + urllib.parse.urlencode(
        {"search_query": search, "start": 0, "max_results": max_results,
         "sortBy": "relevance", "sortOrder": "descending"}
    )
    rec = {"label": label, "query": search, "url": url}
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_S) as r:
            rec["http_status"] = r.status
            raw = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        rec["http_status"] = e.code
        rec["status"] = "THROTTLED" if e.code == 429 else "UNREACHABLE"
        rec["reason"] = f"HTTPError {e.code}: {e.reason}"
        return rec
    except Exception as e:                                   # noqa: BLE001
        rec["status"] = "UNREACHABLE"
        rec["reason"] = f"{type(e).__name__}: {e}"
        return rec

    rec["bytes"] = len(raw)
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        rec["status"] = "UNREACHABLE"
        rec["reason"] = f"ParseError: {e}"
        return rec

    total, ns_seen = None, set()
    for el in root.iter():
        n = _ns_of(el.tag)
        if n:
            ns_seen.add(n)
        if _local(el.tag) == "totalResults":
            total = int((el.text or "0").strip())
    entries = []
    for el in root.iter():
        if _local(el.tag) != "entry":
            continue
        e = {}
        for ch in el:
            lt = _local(ch.tag)
            if lt == "id":
                e["id"] = (ch.text or "").rsplit("/", 1)[-1]
            elif lt == "title":
                e["title"] = " ".join((ch.text or "").split())
            elif lt == "published":
                e["published"] = (ch.text or "")[:10]
        entries.append(e)

    rec["served_namespaces"] = sorted(ns_seen)
    rec["opensearch_namespace_served"] = next(
        (n for n in sorted(ns_seen) if "opensearch" in n), None)
    if total is None:
        rec["status"] = "UNREACHABLE"
        rec["reason"] = "no opensearch:totalResults element found -- NOT a zero"
        return rec
    rec["status"] = "OK"
    rec["total_results"] = total
    rec["entries_parsed"] = len(entries)
    rec["entries"] = entries
    return rec


# -- SS2.2 controls, planted before the run ---------------------------------
CONTROLS = [
    ("POSITIVE_CONTROL", 'all:"discretely self-similar" AND all:"Navier-Stokes"'),
    ("NEGATIVE_CONTROL", 'all:"zqxjkvwbrfmp discretely self-similar cutoff"'),
]

# -- SS2.3's seven technique families ---------------------------------------
QUERIES = [
    ("F1_rigidity_integrability", 'all:"Leray" AND all:"self-similar" AND all:"Navier-Stokes" AND all:"rigidity"'),
    ("F2_dss_apriori_decay",      'all:"discretely self-similar" AND all:"Navier-Stokes" AND all:"decay"'),
    ("F2b_dss_removing",          'ti:"discretely self-similar" AND abs:"Navier-Stokes"'),
    ("F3_local_leray",            'all:"local Leray" AND all:"self-similar"'),
    ("F3b_forward_ss_large_data", 'all:"forward self-similar" AND all:"Navier-Stokes"'),
    ("F4_cutoff_finite_energy",   'all:"finite energy" AND all:"finite speed of propagation" AND all:"blow-up"'),
    ("F4b_elgindi_c1alpha",       'all:"self-similar" AND all:"Euler" AND all:"finite energy" AND all:"singularity"'),
    ("F5_implosion",              'all:"implosion" AND all:"compressible" AND all:"self-similar"'),
    ("F6_semilinear_heat_trunc",  'all:"self-similar" AND all:"blow-up" AND all:"truncation" AND all:"heat equation"'),
    ("F7_bogovskii",              'all:"Bogovskii" AND all:"divergence equation"'),
    ("X_localisation_infinite_energy", 'all:"infinite energy" AND all:"Navier-Stokes" AND all:"localization"'),
    # -- targeted lookups for the AUTHORS NAMED IN SS2.3.  These are not list-building
    # -- backwards from what was easy to find: SS2.3 fixed the names before any fetch.
    ("T_necas_ruzicka_sverak", 'all:"Leray" AND all:"self-similar" AND all:"Navier-Stokes" AND all:"L^3"'),
    ("T_tsai_local_energy",    'au:"Tsai_T" AND all:"self-similar"'),
    ("T_bradshaw_tsai_decay",  'au:"Bradshaw" AND all:"discretely self-similar"'),
    ("T_kang_miura_tsai",      'au:"Miura" AND all:"self-similar" AND all:"Navier-Stokes"'),
    ("T_lai_miao_zheng",       'all:"discretely self-similar" AND all:"Besov"'),
    ("T_mrrs_implosion",       'ti:"implosion" AND all:"compressible fluid"'),
    ("T_elgindi_c1alpha",      'au:"Elgindi_T" AND all:"finite time"'),
    ("T_chen_hou",             'au:"Hou_T" AND all:"Boussinesq" AND all:"blowup"'),
    ("T_giga_kohn_heat",       'all:"backward self-similar" AND all:"semilinear heat"'),
    ("T_semilinear_heat_cut",  'all:"cut-off" AND all:"self-similar" AND all:"blow-up"'),
    ("T_bogovskii_weighted",   'all:"Bogovskii operator"'),
    ("T_dss_type_I",           'all:"discretely self-similar" AND all:"Type I"'),
]


def main() -> int:
    recs = []
    for label, q in CONTROLS + QUERIES:
        rec = query(label, q)
        recs.append(rec)
        print(f"{label:34s} {str(rec.get('status')):12s} "
              f"total={rec.get('total_results')} parsed={rec.get('entries_parsed')} "
              f"ns={rec.get('opensearch_namespace_served')}", flush=True)
        time.sleep(PACE_S)

    by = {r["label"]: r for r in recs}
    pos, neg = by["POSITIVE_CONTROL"], by["NEGATIVE_CONTROL"]
    verdict = {
        "positive_control_fired": pos.get("status") == "OK" and (pos.get("total_results") or 0) >= 1,
        "positive_control_total": pos.get("total_results"),
        "negative_control_fired": neg.get("status") == "OK" and neg.get("total_results") == 0,
        "negative_control_total": neg.get("total_results"),
        "opensearch_namespace_served": pos.get("opensearch_namespace_served"),
        "namespace_served_is_1_1":
            (pos.get("opensearch_namespace_served") or "").endswith("1.1/"),
    }
    verdict["instrument_is_live"] = bool(
        verdict["positive_control_fired"] and verdict["negative_control_fired"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(
        {"leg": 397, "unit": "L2'", "what": "arXiv search instrument for leg 397 SS2.3, with SS2.2 controls",
         "controls": verdict, "queries": recs}, indent=1) + "\n")
    print(f"\nwrote {OUT}")
    print(json.dumps(verdict, indent=1))
    if not verdict["instrument_is_live"]:
        print("\nINSTRUMENT NOT LIVE -- every zero in this leg is VOID (SS2.2).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
