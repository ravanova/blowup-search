#!/usr/bin/env python3
"""Leg 303 / Route-GAF — Grade-A/fluid cell freshness sweep, mid-2026.

WHAT THIS ANSWERS
-----------------
`solver/viscous_novelty.py::PRECEDENTS` is this repository's occupancy matrix for
"certified blow-up" precedents.  Its Grade-A/fluid cell -- a computer-assisted
certificate whose ENCLOSED OBJECT still carries the dissipative term, for a FLUID
TRANSPORT model -- is empty, and Phase 1's premise ("no certified viscous blow-up
exists in any model, in any dimension, today") is exactly the claim that it is
still empty.  Leg 174 last swept for it on 2026-08-06T15:22Z with the 12 queries
banked in `SEARCH_LOG`; legs 242 and 291 re-checked only one author line and one
inviscid object respectively.  This runner re-sweeps.

Gate (pre-committed, writeup/novelty/leg_303.md):
    Does the sweep find at least one post-cutoff work claiming a certified
    dissipative blow-up or materially narrowing the cell?

HIT RULE (pre-committed, four clauses, all required):
    (a) computer-assisted / rigorous-numerics certificate,
    (b) of a blow-up or singular self-similar profile,
    (c) with the dissipative term INSIDE the certified object,
    (d) for a fluid transport model.
Fewer than four -> NEAR (with the failing clause named) or OFF.

METHOD NOTE, carried from leg 52/123/291: a topical query without a literal arXiv
ID does not reliably resurface a known paper in this environment, and the model's
own memory can masquerade as a hit.  Every link this runner records is traceable
to an Atom entry actually returned by export.arxiv.org during the run.  Counts are
recorded too, but the finding is stated in LINKS (leg-53 lesson).

The hit condition is NEW-TO-LEDGER, not new-to-arXiv.  Leg 174's own miss
(arXiv:2208.09445, a 2022 paper) was old; it was invisible because no query of
its 12 mentioned compressible/implosion.  So C2 asks that axis deliberately.

Usage:
    .venv/bin/python experiments/p2_route_gaf_v1_sweep.py            # live sweep
    .venv/bin/python experiments/p2_route_gaf_v1_sweep.py --offline  # re-curate
                                                                    # from raw log
Writes:
    writeup/data/p2_route_gaf_v1_sweep.json   (curated, committed)
    writeup/data/p2_route_gaf_v1_raw.json     (raw Atom-derived entries, committed)
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

DATA = os.path.join(ROOT, "writeup", "data")
CURATED = os.path.join(DATA, "p2_route_gaf_v1_sweep.json")
RAW = os.path.join(DATA, "p2_route_gaf_v1_raw.json")

API = "https://export.arxiv.org/api/query?"
ATOM = "{http://www.w3.org/2005/Atom}"

# --------------------------------------------------------------------------
# The window this leg is responsible for, dated from git, not remembered.
# --------------------------------------------------------------------------
WINDOW = {
    "last_broad_sweep": {
        "leg": 174,
        "route": "VBS",
        "closed_utc": "2026-08-06T14:22:38Z",
        "n_queries_banked": 12,
        "where": "solver/viscous_novelty.py::SEARCH_LOG",
        "known_gap": "no query mentions compressible / implosion / imploding -- which is "
                     "how arXiv:2208.09445 (2022) stayed out of the ledger until leg 197",
    },
    "since_then": [
        {"leg": 242, "route": "DFL2", "closed_utc": "2026-08-06T22:11:18Z",
         "scope": "author-scoped: complete arXiv listings of Dahne and Figueras only"},
        {"leg": 291, "route": "HLR2", "closed_utc": "2026-08-07T05:24:39Z",
         "scope": "object-scoped: HL_S2_nonsymmetric (an INVISCID target) and its anchors"},
    ],
    "gap_days_since_last_broad_sweep": None,  # filled at run time
}

# --------------------------------------------------------------------------
# CHANNELS -- every query string verbatim, committed in writeup/novelty/leg_303.md
# before the first request went out.
# --------------------------------------------------------------------------
# C1 is leg 174's own net, replicated verbatim from solver/viscous_novelty.py::SEARCH_LOG,
# together with the count it recorded, so growth is visible rather than asserted.
C1_LEG174 = [
    ('abs:"computer-assisted" AND abs:"self-similar" AND abs:blowup', 2),
    ('abs:"self-similar" AND abs:blowup AND abs:"fractional dissipation"', 1),
    ('abs:"Ginzburg-Landau" AND abs:"self-similar" AND abs:"computer-assisted"', 1),
    ('abs:"nonlinear heat equation" AND abs:"self-similar" AND abs:"computer-assisted"', 1),
    ('abs:"branches" AND abs:"self-similar" AND abs:"Ginzburg-Landau"', 1),
    ('abs:"self-similar" AND abs:blowup AND abs:"interval arithmetic"', 0),
    ('abs:"self-similar" AND abs:"blow-up" AND abs:"validated numerics"', 0),
    ('abs:"Boussinesq" AND abs:blowup AND abs:viscosity AND abs:"computer-assisted"', 0),
    ('abs:"self-similar" AND abs:blowup AND abs:"computer-assisted proof" AND abs:viscosity', 0),
    ('abs:"blowup" AND abs:"viscous" AND abs:"rigorous" AND abs:"continuation"', 0),
    ('abs:"hypodissipative" AND abs:"Navier-Stokes" AND abs:blowup', 1),
    ('abs:"self-similar" AND abs:"Navier-Stokes" AND abs:"computer-assisted"', 3),
]

# C2 -- the axis leg 174 never asked (its own recorded gap).
C2_COMPRESSIBLE = [
    'abs:"imploding" AND abs:"computer-assisted"',
    'abs:"implosion" AND abs:"self-similar" AND abs:"Navier-Stokes"',
    'abs:"compressible" AND abs:"singularity" AND abs:"computer-assisted"',
    'abs:"compressible Navier-Stokes" AND abs:"self-similar" AND abs:"blow-up"',
]

# C3 -- dissipation-inside-the-certificate machinery, model-agnostic.
C3_MACHINERY = [
    'abs:"radii polynomial" AND abs:"blow-up"',
    'abs:"radii polynomial" AND abs:"self-similar"',
    'abs:"Newton-Kantorovich" AND abs:"blow-up"',
    'abs:"validated numerics" AND abs:"dissipative" AND abs:"singularity"',
    'abs:"interval arithmetic" AND abs:"viscous"',
    'abs:"computer-assisted proof" AND abs:"parabolic" AND abs:"blow-up"',
    'abs:"rigorous numerics" AND abs:"blow-up"',
]

# C4 -- fluid transport models by name x certification vocabulary.
C4_MODELS = [
    'abs:"De Gregorio" AND abs:"dissipation"',
    'abs:"Constantin-Lax-Majda" AND abs:"dissipation"',
    'abs:"Hou-Luo" AND abs:"viscous"',
    'abs:"Boussinesq" AND abs:"computer-assisted"',
    'abs:"surface quasi-geostrophic" AND abs:"computer-assisted"',
    'abs:"Navier-Stokes" AND abs:"computer-assisted proof" AND abs:"singularity"',
    'abs:"Euler equations" AND abs:"computer-assisted" AND abs:"viscosity"',
]

# C5 -- the NRS/Tsai screen boundary.
C5_SCREEN = [
    'abs:"backward self-similar" AND abs:"Navier-Stokes"',
    'abs:"discretely self-similar" AND abs:"Navier-Stokes"',
    'abs:"Leray" AND abs:"self-similar" AND abs:"nonexistence"',
    'abs:"Type I" AND abs:"Navier-Stokes" AND abs:"blow-up"',
    'abs:"local energy" AND abs:"Navier-Stokes" AND abs:"self-similar"',
]

CHANNELS = [
    ("C1", "replication of leg 174's own 12-query net", [q for q, _ in C1_LEG174]),
    ("C2", "the compressible/implosion axis leg 174 never asked", C2_COMPRESSIBLE),
    ("C3", "dissipation-inside-the-certificate machinery, model-agnostic", C3_MACHINERY),
    ("C4", "fluid transport models by name x certification vocabulary", C4_MODELS),
    ("C5", "the NRS/Tsai screen boundary", C5_SCREEN),
]

MAX_RESULTS = 60
SLEEP = 3.1  # arXiv asks for >=3s between calls


def arxiv_query(search_query, max_results=MAX_RESULTS, retries=3):
    """Return (url, entries, error).  entries: list of dicts.  Never raises."""
    params = urllib.parse.urlencode({
        "search_query": search_query,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    url = API + params
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Unsolved-leg303/1.0"})
            with urllib.request.urlopen(req, timeout=60) as fh:
                body = fh.read()
            root = ET.fromstring(body)
            out = []
            for e in root.findall(ATOM + "entry"):
                aid = (e.findtext(ATOM + "id") or "").strip()
                m = re.search(r"abs/(.+?)(v\d+)?$", aid)
                out.append({
                    "arxiv_id": m.group(1) if m else aid,
                    "link": re.sub(r"v\d+$", "", aid).replace("http://", "https://"),
                    "title": " ".join((e.findtext(ATOM + "title") or "").split()),
                    "published": (e.findtext(ATOM + "published") or "").strip(),
                    "updated": (e.findtext(ATOM + "updated") or "").strip(),
                    "summary": " ".join((e.findtext(ATOM + "summary") or "").split()),
                })
            return url, out, None
        except Exception as exc:  # network, XML, anything
            last = f"{type(exc).__name__}: {exc}"
            time.sleep(2 + 3 * attempt)
    return url, None, last


# --------------------------------------------------------------------------
# The four-clause screen, applied mechanically to title+abstract.
# --------------------------------------------------------------------------
CERT = re.compile(r"computer[- ]assisted|computer[- ]aided|rigorous numeric|validated numeric|"
                  r"interval arithmetic|radii polynomial|newton-kantorovich|constructive proof",
                  re.I)
BLOWUP = re.compile(r"blow[- ]?up|blowup|singularit|implosion|imploding|finite[- ]time", re.I)
DISSIP = re.compile(r"viscous|viscosity|dissipat|navier[- ]stokes|parabolic|diffusi|"
                    r"hypodissipative|fractional laplacian|ginzburg-landau|heat equation", re.I)
FLUID = re.compile(r"navier[- ]stokes|euler equation|boussinesq|quasi-geostrophic|\bsqg\b|"
                   r"de gregorio|constantin[- ]lax[- ]majda|\bcml\b|hou[- ]luo|vorticity|"
                   r"incompressible|compressible fluid|fluid|water wave|transport equation",
                   re.I)


def screen(entry):
    """Mechanical pre-screen -> clause booleans.  Adjudication is separate and manual."""
    text = entry["title"] + " " + entry["summary"]
    return {
        "a_certificate": bool(CERT.search(text)),
        "b_blowup": bool(BLOWUP.search(text)),
        "c_dissipative": bool(DISSIP.search(text)),
        "d_fluid_model": bool(FLUID.search(text)),
    }


# --------------------------------------------------------------------------
# MANUAL ADJUDICATION -- filled in after reading the returned titles/abstracts,
# committed here so the curated JSON is reproducible and the grading cannot be
# quietly changed after the fact.  Anything not listed keeps its mechanical
# verdict.  Key = arXiv id (no version).
# --------------------------------------------------------------------------
from p2_route_gaf_v1_adjudications import (  # noqa: E402
    ADJUDICATIONS, SCREEN_BOUNDARY, METHOD_FINDINGS)


def ledger_ids():
    """The IDs already in solver/viscous_novelty.py::PRECEDENTS, read not remembered."""
    from solver import viscous_novelty as vn
    ids = set()
    for row in vn.PRECEDENTS:
        for m in re.finditer(r"(\d{4}\.\d{4,5})", row["id"]):
            ids.add(m.group(1))
    return ids, vn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true",
                    help="re-curate from the committed raw log instead of querying")
    ap.add_argument("--retry-unavailable", action="store_true",
                    help="re-query only the rows the last run could not reach (arXiv "
                         "rate-limits at ~3s spacing; this retries them slowly). An "
                         "UNAVAILABLE row is NOT a zero -- leg-123 precedent.")
    args = ap.parse_args()

    known, vn = ledger_ids()
    run_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    t0 = datetime.fromisoformat(WINDOW["last_broad_sweep"]["closed_utc"].replace("Z", "+00:00"))
    WINDOW["gap_days_since_last_broad_sweep"] = round(
        (datetime.now(timezone.utc) - t0).total_seconds() / 86400.0, 2)

    if args.offline or args.retry_unavailable:
        with open(RAW) as fh:
            raw = json.load(fh)
        run_utc = raw["run_utc"]
        WINDOW["gap_days_since_last_broad_sweep"] = raw["window"]["gap_days_since_last_broad_sweep"]

    if args.retry_unavailable:
        for rec in raw["queries"]:
            if rec["status"] == "OK":
                continue
            url, entries, err = arxiv_query(rec["query"], retries=5)
            if err is None:
                rec.update(status="OK", n=len(entries), entries=entries, url=url)
                rec.pop("error", None)
                rec["retried"] = True
            else:
                rec["error"] = err
            print(f"  retry {rec['channel']} n={rec['n']!s:>4} {rec['status']:<12} "
                  f"{rec['query']}", flush=True)
            time.sleep(25)
        raw["retry_utc"] = datetime.now(timezone.utc).replace(
            microsecond=0).isoformat().replace("+00:00", "Z")
        with open(RAW, "w") as fh:
            json.dump(raw, fh, indent=1, sort_keys=False)
    elif not args.offline:
        raw = {"run_utc": run_utc, "window": WINDOW, "queries": []}
        for cid, cdesc, queries in CHANNELS:
            for q in queries:
                url, entries, err = arxiv_query(q)
                rec = {"channel": cid, "query": q, "url": url}
                if err is None:
                    rec["n"] = len(entries)
                    rec["entries"] = entries
                    rec["status"] = "OK"
                else:
                    rec["status"] = "UNAVAILABLE"
                    rec["error"] = err
                    rec["entries"] = []
                    rec["n"] = None
                raw["queries"].append(rec)
                print(f"  {cid} n={rec['n']!s:>4} {rec['status']:<12} {q}", flush=True)
                time.sleep(SLEEP)
        with open(RAW, "w") as fh:
            json.dump(raw, fh, indent=1, sort_keys=False)

    # ---------------- curation ----------------
    by_id = {}
    for rec in raw["queries"]:
        for e in rec.get("entries") or []:
            slot = by_id.setdefault(e["arxiv_id"], dict(e, found_by=[]))
            if rec["query"] not in slot["found_by"]:
                slot["found_by"].append(rec["query"])

    hits, nears = [], []
    for aid, e in sorted(by_id.items()):
        cl = screen(e)
        verdict_auto = "HIT" if all(cl.values()) else (
            "NEAR" if sum(cl.values()) >= 3 else "OFF")
        adj = ADJUDICATIONS.get(aid)
        verdict = adj["verdict"] if adj else verdict_auto
        row = {
            "arxiv_id": aid,
            "link": e["link"],
            "title": e["title"],
            "published": e["published"],
            "updated": e["updated"],
            "clauses": cl,
            "verdict_mechanical": verdict_auto,
            "verdict": verdict,
            "already_in_PRECEDENTS": aid in known,
            "found_by": e["found_by"],
        }
        if adj:
            row["adjudication"] = adj.get("why", "")
            row["failing_clause"] = adj.get("failing_clause")
            for k in ("overrides_mechanical", "metadata", "what_this_leg_does_with_it",
                      "credibility_flags_visible_at_abstract_level"):
                if k in adj:
                    row[k] = adj[k]
        if verdict == "HIT":
            hits.append(row)
        elif verdict == "NEAR":
            nears.append(row)

    n_ok = sum(1 for r in raw["queries"] if r["status"] == "OK")
    n_unavail = sum(1 for r in raw["queries"] if r["status"] != "OK")
    growth = []
    for (q, n174), rec in zip(C1_LEG174, [r for r in raw["queries"] if r["channel"] == "C1"]):
        growth.append({"query": q, "leg174_n": n174, "leg303_n": rec["n"],
                       "delta": None if rec["n"] is None else rec["n"] - n174,
                       "url": rec["url"]})

    new_hits = [h for h in hits if not h["already_in_PRECEDENTS"]]
    gate_answer = "YES" if new_hits else "NO"

    n_overridden = sum(1 for r in hits + nears if r.get("overrides_mechanical"))
    leg174_unrecorded_links = sum(n for _, n in C1_LEG174)
    c1_identical = all(g["delta"] == 0 for g in growth) if growth else None

    curated = {
        "leg": 303,
        "route": "GAF",
        "title": "Grade-A/fluid cell freshness sweep, mid-2026",
        "run_utc": run_utc,
        "gate": ("Does the sweep find at least one post-cutoff work claiming a certified "
                 "dissipative blow-up or materially narrowing the cell?"),
        "gate_answer": gate_answer,
        "hit_rule": {
            "a_certificate": "computer-assisted / rigorous-numerics certificate",
            "b_blowup": "of a blow-up or singular self-similar profile",
            "c_dissipative": "dissipative term INSIDE the certified object",
            "d_fluid_model": "for a fluid transport model",
            "all_four_required": True,
            "committed_in": "writeup/novelty/leg_303.md sec 4, before the first query",
        },
        "window": raw["window"],
        "coverage": {
            "n_queries_total": len(raw["queries"]),
            "n_queries_ok": n_ok,
            "n_queries_unavailable": n_unavail,
            "n_channels": len(CHANNELS),
            "n_queries_new_vs_leg174": len(raw["queries"]) - len(C1_LEG174),
            "n_distinct_papers_returned": len(by_id),
            "superset_of_leg174_net": True,
        },
        "c1_replication": {
            "what": ("leg 174's own 12 queries re-run verbatim; a grown count is where a "
                     "new hit would be"),
            "rows": growth,
            "n_grown": sum(1 for g in growth if (g["delta"] or 0) > 0),
            "all_counts_identical_to_leg174": c1_identical,
            "leg174_links_never_recorded": leg174_unrecorded_links,
            "consequence": ("identical counts prove leg 174's net saw the same result sets; "
                            "because SEARCH_LOG banked counts and not links, WHICH of those "
                            "papers leg 174 read and rejected is unrecoverable (see MF2)"),
        },
        "cell_state": {
            "grade_A_fluid_occupants_before": 0,
            "grade_A_fluid_occupants_claimed_after": len(new_hits),
            "grade_A_fluid_occupants_ESTABLISHED_after": 0,
            "why_claimed_not_established": (
                "the one HIT is adjudicated from title+abstract, the depth this leg is scoped "
                "to; establishing occupancy needs the adversarial full-text read, which is "
                "reserve leg 309 by explicit dispatch. The cell is recorded as CLAIMED, not "
                "FILLED, and Phase 1's premise is NOT recorded as broken by this leg."),
            "n_hits_new_to_ledger": len(new_hits),
            "n_near_misses_recorded": len(nears),
            "n_mechanical_verdicts_overridden": n_overridden,
            "ledger_ids_known": sorted(known),
        },
        "screen_boundary_NRS_Tsai": SCREEN_BOUNDARY,
        "method_findings": METHOD_FINDINGS,
        "hits": hits,
        "near_misses": nears,
        "query_log": [{"channel": r["channel"], "query": r["query"], "url": r["url"],
                       "status": r["status"], "n": r["n"],
                       "links": [e["link"] for e in (r.get("entries") or [])]}
                      for r in raw["queries"]],
        "escalation": ("none" if not new_hits else
                       "ESCALATION-CANDIDATE, not an escalation as landed: arXiv:2604.09949 "
                       "CLAIMS the Grade-A/fluid cell. This leg lands normally because none of "
                       "the four escalations (ORCHESTRATION.md sec 8) is triggered -- no "
                       "plan_of_record change, no ban lifted, no Clay-chain movement claimed, "
                       "no banked result rewritten -- and because 'actually FILLS the cell' "
                       "cannot be established at abstract depth. Leg 309 is now load-bearing: "
                       "if its read holds the claim up, Phase 1's premise falls, and THAT is "
                       "the user's to weigh."),
        "clay_odds_note": ("unchanged at ~0.05%: a freshness re-check of a literature cell "
                           "moves no link of the L1->L4 chain"),
    }
    with open(CURATED, "w") as fh:
        json.dump(curated, fh, indent=1)

    print()
    print(f"queries: {len(raw['queries'])} ({n_ok} OK, {n_unavail} UNAVAILABLE) over "
          f"{len(CHANNELS)} channels")
    print(f"distinct papers returned: {len(by_id)}")
    print(f"C1 queries whose count grew since leg 174: {curated['c1_replication']['n_grown']}/12")
    print(f"HITs new to PRECEDENTS: {len(new_hits)}   NEAR misses: {len(nears)}")
    print(f"GATE: {gate_answer}")
    for h in hits:
        print(f"  HIT  {h['link']}  {h['title'][:70]}")
    for n in nears:
        print(f"  NEAR {n['link']}  {n['title'][:70]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
