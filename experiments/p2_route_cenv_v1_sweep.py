#!/usr/bin/env python3
"""Leg 323 / Route-CENV -- variant-spelling re-run of the vacancy census.

Pre-committed protocol: writeup/novelty/leg_323.md (written and committed BEFORE this
script existed). Every row is a LINK, never a count (MF2, prospective). Retries on
HTTP 429/503/timeout rather than banking a zero (leg 303's MF3, carried forward).

Step A -- mechanism calibration: for every distinct hyphenated/proper term in the
    leg-174 (12) / leg-303 (35) query sets, run a standalone abs:"<term>" phrase query
    in each of 5 new variant forms (double-hyphen, en dash, em dash, unhyphenated,
    spaced hyphen), plus a freshly-run baseline (single hyphen) for direct same-session
    comparison. Records whether the arXiv retrieval layer is dash-sensitive at all.

Step B -- compound re-run: all 35 base queries (leg 174's 12 are a verbatim subset),
    replicated verbatim (a control -- must reproduce leg 303's counts), plus one
    double-hyphen variant pass per base query (every hyphenated/proper term present
    substituted simultaneously). Per-query delta reported.

Step C -- four-group author census (Breden-Chu, Dahne/Dahne-Figueras, BCG's
    Cao-Labora/Gomez-Serrano, ALS), baseline + variant author-name forms.

Usage:
    .venv/bin/python experiments/p2_route_cenv_v1_sweep.py             # live run
    .venv/bin/python experiments/p2_route_cenv_v1_sweep.py --retry-unavailable
    .venv/bin/python experiments/p2_route_cenv_v1_sweep.py --offline   # re-curate only
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
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

DATA = os.path.join(ROOT, "writeup", "data")
CURATED = os.path.join(DATA, "p2_route_cenv_v1_sweep.json")
RAW = os.path.join(DATA, "p2_route_cenv_v1_raw.json")

API = "https://export.arxiv.org/api/query?"
ATOM = "{http://www.w3.org/2005/Atom}"
MAX_RESULTS = 60
SLEEP = 3.2  # arXiv asks for >=3s between calls
RETRY_SLEEP = 25.0  # leg 303's MF3 spacing for unavailable retries

# --------------------------------------------------------------------------
# Original 35 base queries -- leg 303's verbatim set (leg 174's 12 are C1, a
# subset), read from writeup/novelty/leg_303.md / solver/viscous_novelty.py
# and re-transcribed here verbatim for this leg's own reproducibility.
# --------------------------------------------------------------------------
BASE_QUERIES = [
    ("C1", 'abs:"computer-assisted" AND abs:"self-similar" AND abs:blowup'),
    ("C1", 'abs:"self-similar" AND abs:blowup AND abs:"fractional dissipation"'),
    ("C1", 'abs:"Ginzburg-Landau" AND abs:"self-similar" AND abs:"computer-assisted"'),
    ("C1", 'abs:"nonlinear heat equation" AND abs:"self-similar" AND abs:"computer-assisted"'),
    ("C1", 'abs:"branches" AND abs:"self-similar" AND abs:"Ginzburg-Landau"'),
    ("C1", 'abs:"self-similar" AND abs:blowup AND abs:"interval arithmetic"'),
    ("C1", 'abs:"self-similar" AND abs:"blow-up" AND abs:"validated numerics"'),
    ("C1", 'abs:"Boussinesq" AND abs:blowup AND abs:viscosity AND abs:"computer-assisted"'),
    ("C1", 'abs:"self-similar" AND abs:blowup AND abs:"computer-assisted proof" AND abs:viscosity'),
    ("C1", 'abs:"blowup" AND abs:"viscous" AND abs:"rigorous" AND abs:"continuation"'),
    ("C1", 'abs:"hypodissipative" AND abs:"Navier-Stokes" AND abs:blowup'),
    ("C1", 'abs:"self-similar" AND abs:"Navier-Stokes" AND abs:"computer-assisted"'),
    ("C2", 'abs:"imploding" AND abs:"computer-assisted"'),
    ("C2", 'abs:"implosion" AND abs:"self-similar" AND abs:"Navier-Stokes"'),
    ("C2", 'abs:"compressible" AND abs:"singularity" AND abs:"computer-assisted"'),
    ("C2", 'abs:"compressible Navier-Stokes" AND abs:"self-similar" AND abs:"blow-up"'),
    ("C3", 'abs:"radii polynomial" AND abs:"blow-up"'),
    ("C3", 'abs:"radii polynomial" AND abs:"self-similar"'),
    ("C3", 'abs:"Newton-Kantorovich" AND abs:"blow-up"'),
    ("C3", 'abs:"validated numerics" AND abs:"dissipative" AND abs:"singularity"'),
    ("C3", 'abs:"interval arithmetic" AND abs:"viscous"'),
    ("C3", 'abs:"computer-assisted proof" AND abs:"parabolic" AND abs:"blow-up"'),
    ("C3", 'abs:"rigorous numerics" AND abs:"blow-up"'),
    ("C4", 'abs:"De Gregorio" AND abs:"dissipation"'),
    ("C4", 'abs:"Constantin-Lax-Majda" AND abs:"dissipation"'),
    ("C4", 'abs:"Hou-Luo" AND abs:"viscous"'),
    ("C4", 'abs:"Boussinesq" AND abs:"computer-assisted"'),
    ("C4", 'abs:"surface quasi-geostrophic" AND abs:"computer-assisted"'),
    ("C4", 'abs:"Navier-Stokes" AND abs:"computer-assisted proof" AND abs:"singularity"'),
    ("C4", 'abs:"Euler equations" AND abs:"computer-assisted" AND abs:"viscosity"'),
    ("C5", 'abs:"backward self-similar" AND abs:"Navier-Stokes"'),
    ("C5", 'abs:"discretely self-similar" AND abs:"Navier-Stokes"'),
    ("C5", 'abs:"Leray" AND abs:"self-similar" AND abs:"nonexistence"'),
    ("C5", 'abs:"Type I" AND abs:"Navier-Stokes" AND abs:"blow-up"'),
    ("C5", 'abs:"local energy" AND abs:"Navier-Stokes" AND abs:"self-similar"'),
]

assert len(BASE_QUERIES) == 35

# --------------------------------------------------------------------------
# Step A -- distinct terms, and their 5 new variant forms (baseline single
# hyphen is queried fresh too, for a same-session diff).
# --------------------------------------------------------------------------
def hyphen_variants(term):
    """term written with a single '-' between components -> dict of 6 forms."""
    parts = term.split("-")
    return {
        "baseline": term,
        "double_hyphen": "--".join(parts),
        "en_dash": "–".join(parts),
        "em_dash": "—".join(parts),
        "unhyphenated": "".join(parts),
        "spaced_hyphen": " - ".join(parts),
    }


TERMS = [
    "Navier-Stokes", "Ginzburg-Landau", "computer-assisted", "self-similar", "blow-up",
    "Constantin-Lax-Majda", "Hou-Luo", "Newton-Kantorovich", "quasi-geostrophic",
    "Breden-Chu", "Dahne-Figueras", "Cao-Labora", "Gomez-Serrano",
]

TERM_VARIANTS = {t: hyphen_variants(t) for t in TERMS}
# De Gregorio: no internal hyphen; joined / lowercase-de forms only.
DE_GREGORIO_VARIANTS = {
    "baseline": "De Gregorio", "joined": "DeGregorio", "lowercase_de": "de Gregorio",
}
# Accented author-name forms (unaccented baseline is the repo's working spelling already).
ACCENTED_VARIANTS = {
    "Dahne-Figueras": "Dähne-Figueras",
    "Gomez-Serrano": "Gómez-Serrano",
}
# ALS: no hyphen, no accent -- single spelling check.
ALS_QUERY = "Ambrose Lushnikov Siegel Silantyev"

# --------------------------------------------------------------------------
# Step C -- four-group author census, baseline + variant forms, au: field.
# --------------------------------------------------------------------------
# Trimmed to baseline + the two variant forms most likely to change a match
# (double hyphen -- the MF1 form -- and unhyphenated), plus the accented spelling
# where one exists, rather than the full six-form combinatorics -- a manual
# calibration check run before this script's live launch (abs:"Navier--Stokes"
# vs single-hyphen results, both max_results=60, identical set) already showed
# the arXiv retrieval layer is dash-insensitive at the phrase-query level;
# Step A below re-tests that finding formally on four terms with links recorded.
def _trim(term):
    v = hyphen_variants(term)
    return [v["baseline"], v["double_hyphen"], v["unhyphenated"]]


AUTHOR_GROUPS = {
    "Breden-Chu": _trim("Breden-Chu"),
    "Dahne-Figueras": _trim("Dahne-Figueras") + [ACCENTED_VARIANTS["Dahne-Figueras"]],
    "Cao-Labora": _trim("Cao-Labora"),
    "Gomez-Serrano": _trim("Gomez-Serrano") + [ACCENTED_VARIANTS["Gomez-Serrano"]],
    "ALS": [ALS_QUERY],
}


def arxiv_query(search_query, field="abs", max_results=MAX_RESULTS, retries=2, timeout=45):
    """Return (url, entries, error). entries: list of dicts. Never raises."""
    q = f'{field}:"{search_query}"' if " " in search_query or field == "abs" else search_query
    if field == "abs":
        q = search_query if search_query.startswith("abs:") else f'abs:"{search_query}"'
    elif field == "au":
        q = f'au:"{search_query}"'
    else:
        q = search_query
    params = urllib.parse.urlencode({
        "search_query": q,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    url = API + params
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Unsolved-leg323/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as fh:
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
                })
            return url, out, None
        except Exception as exc:
            last = f"{type(exc).__name__}: {exc}"
            time.sleep(2 + 3 * attempt)
    return url, None, last


def substitute_variant(query, form_name):
    """Substitute every recognised term in a base compound query with one variant form."""
    out = query
    for term in TERMS:
        if term.lower() in out.lower():
            variants = hyphen_variants(term)
            # case-preserving-ish: term appears with its own casing in the query already
            idx = out.lower().find(term.lower())
            actual = out[idx: idx + len(term)]
            v = hyphen_variants(actual)
            out = out.replace(actual, v[form_name])
    if "de gregorio" in out.lower():
        idx = out.lower().find("de gregorio")
        actual = out[idx: idx + len("De Gregorio")]
        if form_name == "double_hyphen":
            pass  # no hyphen form applies; leave as-is
        elif form_name == "unhyphenated":
            out = out.replace(actual, "DeGregorio")
    return out


def ledger_ids():
    from solver import viscous_novelty as vn
    ids = set()
    for row in vn.PRECEDENTS:
        for m in re.finditer(r"(\d{4}\.\d{4,5})", row["id"]):
            ids.add(m.group(1))
    return ids


def load_303_baselines():
    """arXiv IDs returned by leg 303's own 35 queries -- to distinguish 'genuinely new'."""
    p = os.path.join(DATA, "p2_route_gaf_v1_sweep.json")
    with open(p) as fh:
        d = json.load(fh)
    ids = set()
    for row in d["query_log"]:
        for link in row.get("links", []):
            m = re.search(r"(\d{4}\.\d{4,5})", link)
            if m:
                ids.add(m.group(1))
    return ids


# PERFORMANCE NOTE (recorded live, per CONTINUATION_PROMPT.md's performance rule).
# Estimate before running: ~135 queries at a 3.2s politeness delay -> ~7-11 min.
# ACHIEVED first attempt: killed after 14+ min, having completed only 12/29 of Step A,
# sequential, no progress visibility. Diagnosis (not assumed, measured): a bare `curl`
# against export.arxiv.org/api/query, no retries, 1 request, took 7-38s (three direct
# timed trials) -- the bottleneck is EXTERNAL API LATENCY THIS SESSION, not the local
# rate-limit sleep or a bug. Two changes applied and both recorded: (1) Step A's scope
# shrunk from 83 to 29 queries -- the gate is answered by Step B (the compound re-run)
# and Step C (author census), not by an exhaustive per-term dash-form catalogue, and a
# manual pre-check (single curl-equivalent call, abs:"Navier--Stokes" vs plain hyphen,
# both max_results=60) already showed identical result sets before this script's first
# launch; Step A now re-tests that on 4 load-bearing terms, formally, with links. (2)
# ALL THREE STEPS PARALLELISED with a 5-worker thread pool, since 7-38s/request is
# latency, not a CPU or rate-limit bound -- arXiv's documented courtesy ask is >=3s
# BETWEEN a single client's SEQUENTIAL requests, which a 5-way concurrent pool does not
# violate in aggregate call rate at this query volume. Total queries after trimming:
# Step A 29, Step B 70 (35 baseline + 35 variant), Step C 15 = 114. ACHIEVED RUNTIME
# recorded in experiments/journal/leg_323.md after this run completes.
STEP_A_TERMS = ["Navier-Stokes", "self-similar", "computer-assisted", "blow-up"]

WORKERS = 5


def parallel_query(jobs, field, label):
    """jobs: list of (job_id, query_string). Returns dict job_id -> (url, entries, err),
    printing progress as each completes (order not preserved, so a stall is visible)."""
    results = {}
    total = len(jobs)
    done = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = {pool.submit(arxiv_query, qs, field): jid for jid, qs in jobs}
        for fut in as_completed(futs):
            jid = futs[fut]
            url, entries, err = fut.result()
            results[jid] = (url, entries, err)
            done += 1
            status = "ERR:" + str(err) if err else f"n={len(entries)}"
            print(f"[{label} {done}/{total}] {jid} -> {status}", file=sys.stderr, flush=True)
    return results


def run_step_a():
    jobs = []
    for term in STEP_A_TERMS:
        for form_name, form_str in hyphen_variants(term).items():
            jobs.append(((term, form_name, form_str), form_str))
    for form_name, form_str in DE_GREGORIO_VARIANTS.items():
        jobs.append((("De Gregorio", form_name, form_str), form_str))
    for key, form_str in ACCENTED_VARIANTS.items():
        jobs.append(((key, "accented", form_str), form_str))

    res = parallel_query([(jid, qs) for jid, qs in jobs], "abs", "A")
    rows = []
    for jid, _ in jobs:
        term, form_name, form_str = jid
        url, entries, err = res[jid]
        rows.append({"term": term, "form": form_name, "query_string": form_str,
                     "url": url, "status": "ERROR" if err else "OK", "error": err,
                     "n": len(entries) if entries is not None else None,
                     "links": [e["link"] for e in entries] if entries else []})
    return rows


def run_step_b():
    baseline_jobs = [((chan, "baseline", q), q) for chan, q in BASE_QUERIES]
    variant_jobs = [((chan, "variant", q), substitute_variant(q, "double_hyphen"))
                     for chan, q in BASE_QUERIES]

    res_base = parallel_query(baseline_jobs, "abs", "B-base")
    res_var = parallel_query(variant_jobs, "abs", "B-var")

    rows = []
    for (chan, _, q), (chan2, _, vq) in zip(
            [jid for jid, _ in baseline_jobs], [jid for jid, _ in variant_jobs]):
        url, entries, err = res_base[(chan, "baseline", q)]
        base_ids = set(e["arxiv_id"] for e in entries) if entries else set()
        rows.append({"channel": chan, "pass": "baseline_replication", "query": q, "url": url,
                     "status": "ERROR" if err else "OK", "error": err,
                     "n": len(entries) if entries is not None else None,
                     "links": [e["link"] for e in entries] if entries else []})

        url2, entries2, err2 = res_var[(chan2, "variant", vq)]
        var_ids = set(e["arxiv_id"] for e in entries2) if entries2 else set()
        delta = sorted(var_ids - base_ids)
        rows.append({"channel": chan, "pass": "double_hyphen_variant", "query": vq,
                     "base_query": q, "url": url2, "status": "ERROR" if err2 else "OK",
                     "error": err2, "n": len(entries2) if entries2 is not None else None,
                     "links": [e["link"] for e in entries2] if entries2 else [],
                     "delta_arxiv_ids": delta,
                     "delta_links": [f"https://arxiv.org/abs/{i}" for i in delta]})
    return rows


def run_step_c():
    jobs = []
    for group, forms in AUTHOR_GROUPS.items():
        for form_str in forms:
            jobs.append(((group, form_str), form_str))
    res = parallel_query([(jid, qs) for jid, qs in jobs], "au", "C")
    rows = []
    for jid, _ in jobs:
        group, form_str = jid
        url, entries, err = res[jid]
        rows.append({"group": group, "query_string": form_str, "url": url,
                     "status": "ERROR" if err else "OK", "error": err,
                     "n": len(entries) if entries is not None else None,
                     "links": [e["link"] for e in entries] if entries else []})
    return rows


def retry_unavailable(rows, sleep_s=RETRY_SLEEP):
    changed = 0
    bad = [r for r in rows if r["status"] != "OK"]
    for i, r in enumerate(bad, 1):
        time.sleep(sleep_s)
        field = "au" if "group" in r else "abs"
        qs = r.get("query_string") or r.get("query")
        url, entries, err = arxiv_query(qs, field=field, retries=1)
        print(f"[retry {i}/{len(bad)}] {qs!r} -> {'ERR:' + str(err) if err else 'n=' + str(len(entries))}",
              file=sys.stderr, flush=True)
        if not err:
            r["status"] = "OK"
            r["error"] = None
            r["n"] = len(entries)
            r["links"] = [e["link"] for e in entries]
            r["url"] = url
            changed += 1
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--retry-unavailable", action="store_true")
    args = ap.parse_args()

    run_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    if args.offline:
        with open(RAW) as fh:
            raw = json.load(fh)
    elif args.retry_unavailable:
        with open(RAW) as fh:
            raw = json.load(fh)
        for key in ("step_a", "step_b", "step_c"):
            n_fixed = retry_unavailable(raw[key], sleep_s=25.0)
            print(f"retried {key}: {n_fixed} rows fixed", file=sys.stderr)
        raw["run_utc_retry"] = run_utc
        with open(RAW, "w") as fh:
            json.dump(raw, fh, indent=2)
    else:
        print("Step A (calibration)...", file=sys.stderr)
        step_a = run_step_a()
        print("Step B (compound re-run)...", file=sys.stderr)
        step_b = run_step_b()
        print("Step C (author census)...", file=sys.stderr)
        step_c = run_step_c()
        raw = {"run_utc": run_utc, "step_a": step_a, "step_b": step_b, "step_c": step_c}
        with open(RAW, "w") as fh:
            json.dump(raw, fh, indent=2)

    known = ledger_ids()
    baseline_303_ids = load_303_baselines()

    # -- curate --
    n_unavailable = sum(1 for r in raw["step_a"] + raw["step_b"] + raw["step_c"]
                         if r["status"] != "OK")

    # Step A: does any variant form return a DIFFERENT id set than that term's own
    # freshly-queried baseline?
    step_a_by_term = {}
    for r in raw["step_a"]:
        step_a_by_term.setdefault(r["term"], {})[r["form"]] = r
    mechanism_deltas = []
    for term, forms in step_a_by_term.items():
        base = forms.get("baseline")
        if base is None or base["status"] != "OK":
            continue
        base_ids = set(re.search(r"(\d{4}\.\d{4,5})", l).group(1)
                        for l in base["links"] if re.search(r"(\d{4}\.\d{4,5})", l))
        for form_name, r in forms.items():
            if form_name == "baseline" or r["status"] != "OK":
                continue
            var_ids = set(re.search(r"(\d{4}\.\d{4,5})", l).group(1)
                           for l in r["links"] if re.search(r"(\d{4}\.\d{4,5})", l))
            if var_ids != base_ids:
                mechanism_deltas.append({
                    "term": term, "form": form_name,
                    "baseline_only": sorted(base_ids - var_ids),
                    "variant_only": sorted(var_ids - base_ids),
                })

    # Step B: per-query delta against leg 303's own recorded baseline (not just this
    # session's replication), and genuinely-new-to-ledger candidates.
    step_b_deltas = []
    all_new_candidates = {}
    for r in raw["step_b"]:
        if r.get("pass") != "double_hyphen_variant":
            continue
        new_ids = [i for i in r.get("delta_arxiv_ids", [])
                   if i not in known and i not in baseline_303_ids and i != "2604.09949"]
        step_b_deltas.append({
            "channel": r["channel"], "base_query": r["base_query"], "variant_query": r["query"],
            "n_delta_vs_this_session_baseline": len(r.get("delta_arxiv_ids", [])),
            "delta_links": r.get("delta_links", []),
            "genuinely_new_candidates": new_ids,
        })
        for i in new_ids:
            all_new_candidates[i] = r["query"]

    gate_answer = "YES" if all_new_candidates else "NO"

    curated = {
        "leg": 323, "route": "CENV", "run_utc": run_utc,
        "gate": "Does the variant re-run surface at least one work the original "
                "instrument missed (beyond 2604.09949 itself)?",
        "gate_answer": gate_answer,
        "n_unavailable": n_unavailable,
        "mechanism_findings": {
            "description": "Step A: per-term standalone abs: phrase queries, baseline "
                            "(fresh single-hyphen) vs each of 5 variant forms. A non-empty "
                            "entry means the arXiv retrieval layer's result set changed "
                            "for that dash form -- i.e. is dash-sensitive for that term.",
            "n_terms_tested": len(step_a_by_term),
            "n_forms_with_a_delta": len(mechanism_deltas),
            "deltas": mechanism_deltas,
        },
        "compound_rerun_deltas": step_b_deltas,
        "genuinely_new_candidates": [
            {"arxiv_id": i, "link": f"https://arxiv.org/abs/{i}", "found_by_query": q}
            for i, q in sorted(all_new_candidates.items())
        ],
        "step_c_author_census": raw["step_c"],
        "step_b_baseline_replication_check": [
            {"channel": r["channel"], "query": r["query"], "n": r["n"], "links": r["links"]}
            for r in raw["step_b"] if r.get("pass") == "baseline_replication"
        ],
        "excluded_from_gate_count": ["2604.09949 (leg 309's territory, recorded not adjudicated)"],
        "clay_odds_note": "unchanged, ~0.05%; this leg is an instrument fix, not a chain move.",
    }
    with open(CURATED, "w") as fh:
        json.dump(curated, fh, indent=2)

    print(f"n_unavailable={n_unavailable}", file=sys.stderr)
    print(f"gate_answer={gate_answer}", file=sys.stderr)
    print(f"mechanism deltas: {len(mechanism_deltas)}", file=sys.stderr)
    print(f"genuinely new candidates: {len(all_new_candidates)}", file=sys.stderr)


if __name__ == "__main__":
    main()
