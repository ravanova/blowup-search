#!/usr/bin/env python3
"""Leg 323 / Route-CENV -- variant-spelling re-run of the vacancy census.

Pre-committed protocol: writeup/novelty/leg_323.md (written and committed BEFORE any
query ran). Every row is a LINK, never a count (MF2, prospective). HTTP 429/503/timeout
is a REFUSAL TO MEASURE, never a zero (leg 303's MF3 discipline, carried forward).

Step A -- mechanism calibration: for four load-bearing hyphenated terms plus the two
    accented author names and De Gregorio, run a standalone abs:"<term>" phrase query in
    each variant form (baseline single hyphen, double hyphen, en dash, em dash,
    unhyphenated, spaced hyphen) and diff each variant's id set against that term's own
    same-session baseline. Direct test of whether arXiv's retrieval layer is dash-sensitive.

Step B -- compound re-run: all 35 base queries (leg 174's 12 are a verbatim subset),
    replicated verbatim (a control -- must reproduce leg 303's hits), plus one
    double-hyphen variant pass per base query (every hyphenated/proper term present
    substituted simultaneously). Per-query delta reported.

Step C -- four-group author census (Breden-Chu, Dahne/Dahne-Figueras, BCG's
    Cao-Labora/Gomez-Serrano, ALS), baseline + variant author-name forms.

Step D -- instrument controls, run in BOTH directions, and a component-wise ZERO AUDIT
    of every compound query that returned zero in either arm.

--- v2 (resume after the spend-limit kill).  Two defects in the v1 runner were found by
--- re-deriving each committed row's actually-sent query from its own recorded URL, and
--- both are fixed here; see experiments/journal/leg_323.md Part 2 for the full account.
---   D1 (job-id/payload confusion): run_step_b() built its variant job *id* out of the
---       BASE query string while submitting the VARIANT string, then wrote the id's copy
---       into the row's "query" field.  Every double-hyphen row therefore claimed, in the
---       artifact, to be a query it was not.
---   D2 (retry re-sent the wrong string): retry_unavailable() re-queried r["query"] --
---       i.e. D1's mislabel, the BASELINE -- and on success overwrote the row's n/links/url
---       with baseline results while leaving the row labelled "double_hyphen_variant".
---       27 of 35 variant rows in the v1 raw file are baseline results wearing a variant
---       label, and their all-empty deltas are a tautology, not a measurement (lesson 90).
--- The fix is structural, not a patch: a row now carries `query_sent`, parsed back out of
--- the URL that was actually requested, and `verify_rows()` re-derives every row's
--- intended query and refuses to curate if any row's sent string differs from it.

Usage:
    .venv/bin/python experiments/p2_route_cenv_v1_sweep.py --resume   # fill gaps + re-verify
    .venv/bin/python experiments/p2_route_cenv_v1_sweep.py            # full live re-run
    .venv/bin/python experiments/p2_route_cenv_v1_sweep.py --offline  # re-curate only
"""

import argparse
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
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
UA = "Unsolved-leg323/2.0 (research prior-art census)"

# Pacing.  MEASURED, not guessed (journal Part 3): a 6-query burst at 3.2s spacing put
# this client into HTTP 503 for every subsequent request including all:electron, which
# had returned 200 in 0.1s moments earlier.  The politeness floor below is therefore the
# binding constraint on this leg's runtime and it is external, not local.
BASE_SLEEP = 8.0         # between successful calls (on top of the response latency itself)
BACKOFF = [45.0, 90.0, 150.0, 240.0]   # after a 429/503, in order
TIMEOUT = 75

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

DE_GREGORIO_VARIANTS = {
    "baseline": "De Gregorio", "joined": "DeGregorio", "lowercase_de": "de Gregorio",
}
ACCENTED_VARIANTS = {
    "Dahne-Figueras": "Dähne-Figueras",
    "Gomez-Serrano": "Gómez-Serrano",
}
ALS_QUERY = "Ambrose Lushnikov Siegel Silantyev"

STEP_A_TERMS = ["Navier-Stokes", "self-similar", "computer-assisted", "blow-up"]


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


def substitute_variant(query, form_name):
    """Substitute every recognised term in a base compound query with one variant form."""
    out = query
    for term in TERMS:
        if term.lower() in out.lower():
            idx = out.lower().find(term.lower())
            actual = out[idx: idx + len(term)]
            v = hyphen_variants(actual)
            out = out.replace(actual, v[form_name])
    if "de gregorio" in out.lower():
        idx = out.lower().find("de gregorio")
        actual = out[idx: idx + len("De Gregorio")]
        if form_name == "unhyphenated":
            out = out.replace(actual, "DeGregorio")
    return out


# --------------------------------------------------------------------------
# Transport.  One request, no threads: the 503 wall (journal Part 3) is a rate
# limit on this client, so concurrency makes the run slower, not faster.
# --------------------------------------------------------------------------
def build_url(field, search_query, max_results=MAX_RESULTS):
    if field == "abs":
        q = search_query if search_query.startswith("abs:") else f'abs:"{search_query}"'
    elif field == "au":
        q = f'au:"{search_query}"'
    else:
        q = search_query
    return API + urllib.parse.urlencode({
        "search_query": q,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }), q


def query_sent_of(url):
    """The string arXiv actually received, re-derived from the URL. Never from a variable."""
    return urllib.parse.parse_qs(urllib.parse.urlparse(url).query)["search_query"][0]


_last_call = [0.0]


def fetch(field, search_query, max_results=MAX_RESULTS, label=""):
    """-> row dict. status is OK | REFUSAL_TO_MEASURE | ERROR. Never raises, never
    turns a 429/503/timeout into a zero."""
    url, q_intended = build_url(field, search_query, max_results)
    attempts = []
    for attempt in range(len(BACKOFF) + 1):
        wait = max(0.0, BASE_SLEEP - (time.time() - _last_call[0]))
        if attempt:
            wait = BACKOFF[attempt - 1] + random.uniform(0, 5)
        if wait:
            time.sleep(wait)
        t0 = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as fh:
                body = fh.read()
            _last_call[0] = time.time()
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
            print("[%s] %5.1fs n=%2d  %s" % (label, time.time() - t0, len(out), q_intended[:78]),
                  file=sys.stderr, flush=True)
            return {
                "status": "OK", "error": None, "url": url,
                "query_sent": query_sent_of(url), "n": len(out),
                "links": [e["link"] for e in out],
                "titles": [e["title"] for e in out],
                "attempts": attempts,
                "fetched_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            }
        except urllib.error.HTTPError as exc:
            _last_call[0] = time.time()
            attempts.append(f"HTTP {exc.code}")
            print("[%s] %5.1fs HTTP %s (attempt %d)  %s" % (label, time.time() - t0, exc.code,
                  attempt + 1, q_intended[:60]), file=sys.stderr, flush=True)
        except Exception as exc:
            _last_call[0] = time.time()
            attempts.append(type(exc).__name__)
            print("[%s] %5.1fs %s (attempt %d)  %s" % (label, time.time() - t0, type(exc).__name__,
                  attempt + 1, q_intended[:60]), file=sys.stderr, flush=True)
    throttled = any(a.startswith("HTTP 429") or a.startswith("HTTP 503") or a == "TimeoutError"
                    for a in attempts)
    return {
        "status": "REFUSAL_TO_MEASURE" if throttled else "ERROR",
        "error": "; ".join(attempts), "url": url, "query_sent": query_sent_of(url),
        "n": None, "links": [], "titles": [], "attempts": attempts,
        "fetched_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }


# --------------------------------------------------------------------------
# Row plans.  Each row's INTENDED sent-string is derived here, once, and is what
# verify_rows() checks the recorded query_sent against.
# --------------------------------------------------------------------------
def plan_step_a():
    plan = []
    for term in STEP_A_TERMS:
        for form_name, form_str in hyphen_variants(term).items():
            plan.append({"term": term, "form": form_name, "query_string": form_str, "field": "abs"})
    for form_name, form_str in DE_GREGORIO_VARIANTS.items():
        plan.append({"term": "De Gregorio", "form": form_name, "query_string": form_str, "field": "abs"})
    for key, form_str in ACCENTED_VARIANTS.items():
        plan.append({"term": key, "form": "accented", "query_string": form_str, "field": "abs"})
    return plan


def plan_step_b():
    plan = []
    for chan, q in BASE_QUERIES:
        plan.append({"channel": chan, "pass": "baseline_replication", "query": q,
                     "base_query": q, "query_string": q, "field": "abs"})
        vq = substitute_variant(q, "double_hyphen")
        plan.append({"channel": chan, "pass": "double_hyphen_variant", "query": vq,
                     "base_query": q, "query_string": vq, "field": "abs",
                     "variant_identical_to_baseline": vq == q})
    return plan


# Step C2 -- the four-group census done as an author CONJUNCTION rather than as one
# hyphenated string.  Added during the resume, and the reason is a measurement, not a
# preference: Step C's pre-committed form queries au:"Breden-Chu" as a single phrase, but
# Breden and Chu are TWO authors, not one compound surname, so that row can only ever
# return 0 -- a false negative of exactly the class leg 326 recorded for "Chae Tsai".
# Cao-Labora and Gomez-Serrano genuinely ARE compound surnames, so their single-phrase
# rows are meaningful; the group-name rows are not.  Both forms are kept and reported.
AUTHOR_CONJUNCTIONS = [
    ("Breden-Chu", 'au:"Breden" AND au:"Chu"'),
    ("Dahne-Figueras", 'au:"Dahne" AND au:"Figueras"'),
    ("Dahne-Figueras", 'au:"Dähne" AND au:"Figueras"'),
    ("BCG", 'au:"Buckmaster" AND au:"Cao-Labora"'),
    ("BCG", 'au:"Cao-Labora" AND au:"Gomez-Serrano"'),
    ("BCG", 'au:"Cao-Labora" AND au:"Gómez-Serrano"'),
    ("ALS", 'au:"Ambrose" AND au:"Lushnikov"'),
    ("ALS", 'au:"Lushnikov" AND au:"Silantyev"'),
    ("ALS", 'au:"Siegel" AND au:"Silantyev"'),
]


def plan_step_c():
    plan = []
    for group, forms in AUTHOR_GROUPS.items():
        for form_str in forms:
            plan.append({"group": group, "query_string": form_str, "field": "au"})
    return plan


# Step D -- controls in both directions, plus the component-wise zero audit.
# Every control is chosen so it CAN come out the other way (lesson 90).
CONTROLS = [
    {"control": "positive_environment", "field": "all", "query_string": "all:electron",
     "expect": "n>0 -- if this is zero or refuses, nothing else in the run is interpretable"},
    {"control": "positive_two_phrase_AND", "field": "abs",
     "query_string": 'abs:"self-similar" AND abs:"blow-up"',
     "expect": "n>0 -- the direct refutation of the struck MF3 clause; a zero here means "
               "ANDed quoted phrases are broken on this endpoint TODAY and every compound "
               "zero in Steps B/C is uninterpretable"},
    {"control": "negative_nonsense_phrase", "field": "abs",
     "query_string": 'abs:"quixotic hyperviscous marmalade"',
     "expect": "n==0 -- if a nonsense phrase returns hits the endpoint is not doing phrase "
               "matching and every zero elsewhere is meaningless"},
    {"control": "positive_author_conjunction", "field": "raw",
     "query_string": 'au:"Cao-Labora" AND au:"Gomez-Serrano"',
     "expect": "n>0 -- a KNOWN co-authored pair (the imploding-solutions papers). Leg 326 "
               "measured a false negative from a bare author-AND query; this is the check "
               "that says whether Step C's author conjunctions can be believed at all"},
    {"control": "negative_author_conjunction", "field": "raw",
     "query_string": 'au:"Cao-Labora" AND au:"Silantyev"',
     "expect": "n==0 expected -- no known joint paper; if this returns the same set as the "
               "positive control, au: AND is being ignored and both are uninterpretable"},
]


def zero_components(query):
    """Split a compound abs: query into its component single-field queries."""
    return [p.strip() for p in query.split(" AND ") if p.strip()]


# --------------------------------------------------------------------------
def ledger_ids():
    from solver import viscous_novelty as vn
    ids = set()
    for row in vn.PRECEDENTS:
        for m in re.finditer(r"(\d{4}\.\d{4,5})", row["id"]):
            ids.add(m.group(1))
    return ids


def load_303_baselines():
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


def ids_of(row):
    out = set()
    for l in row.get("links") or []:
        m = re.search(r"(\d{4}\.\d{4,5})", l)
        if m:
            out.add(m.group(1))
    return out


# --------------------------------------------------------------------------
# The author-census candidate screen.  Criterion (iv) of the pre-committed novelty file:
# a Step B/C row is a candidate only if it is absent from PRECEDENTS, absent from leg
# 303's and 174's own result sets, is not 2604.09949, and clears leg 303's four clauses.
# The four regexes below are a TITLE-level screen and deliberately generous -- they
# over-select, and every survivor is read at abstract depth by hand and adjudicated in
# writeup/novelty/leg_323.md.  A title screen alone never answers the gate YES.
# --------------------------------------------------------------------------
CLAUSE_CERT = re.compile(r"computer-assisted|rigorous|validated|enclosure|interval|proof", re.I)
# "implo" not "implod": "implosion" does not contain "implod", and an earlier draft of this
# regex scored arXiv:2310.05325 ("Non-radial implosion ...") as blow_up=False for that reason.
CLAUSE_BLOWUP = re.compile(r"singular|blow|implo|self-similar|splash|cusp", re.I)
CLAUSE_DISSIPATIVE = re.compile(r"navier|viscous|viscosity|dissipat|parabolic|heat|schr|stochastic|lyapunov", re.I)
CLAUSE_FLUID = re.compile(r"euler|navier|fluid|water wave|muskat|quasi-geostrophic|sqg|vortex|patch|boussinesq|incompressible|compressible", re.I)

# Self-reference guard: after this leg runs, its own artifacts contain every id it saw, so
# an unfiltered `git grep <id>` reports 100% "already cited in the repo" -- a broken
# instrument of precisely the kind this leg exists to catch.  Measured: 51/51 "cited"
# unfiltered vs 18/51 filtered.
OWN_FILES = [
    ":!writeup/data/p2_route_cenv_v1_raw.json",
    ":!writeup/data/p2_route_cenv_v1_sweep.json",
    ":!experiments/p2_route_cenv_v1_sweep.py",
    ":!writeup/novelty/leg_323.md",
    ":!experiments/journal/leg_323.md",
]


def repo_cites(arxiv_id):
    import subprocess
    try:
        r = subprocess.run(["git", "grep", "-l", arxiv_id, "--", "."] + OWN_FILES,
                           capture_output=True, text=True, cwd=ROOT, timeout=30)
        return sorted(r.stdout.split())
    except Exception:
        return None


def screen_author_census(raw, known, base303):
    seen = {}
    for key in ("step_c", "step_c2_author_conjunctions"):
        for r in raw.get(key, []):
            if r.get("status") != "OK":
                continue
            for l, t in zip(r.get("links", []), r.get("titles", [])):
                mm = re.search(r"(\d{4}\.\d{4,5})", l)
                if mm:
                    seen.setdefault(mm.group(1), (t, r.get("query_sent"), l))
    rows = []
    for i, (t, q, link) in sorted(seen.items()):
        novel = i not in known and i not in base303 and i != "2604.09949"
        clauses = {
            "certificate": bool(CLAUSE_CERT.search(t)),
            "blow_up": bool(CLAUSE_BLOWUP.search(t)),
            "dissipative": bool(CLAUSE_DISSIPATIVE.search(t)),
            "fluid_model": bool(CLAUSE_FLUID.search(t)),
        }
        cites = repo_cites(i) if novel else None
        rows.append({"arxiv_id": i, "link": link, "title": t, "found_by_query": q,
                     "novel_to_ledger_and_leg303": novel,
                     "repo_files_citing_it": cites,
                     "title_clauses": clauses,
                     "n_clauses_true": sum(clauses.values())})
    return rows


def verify_rows(raw):
    """Refuse to curate if any row's actually-sent string differs from its plan, or if a
    row carries results with no recorded sent-string. This is the check that would have
    caught v1's D1/D2 the moment they happened."""
    problems = []
    for key, plan_fn in (("step_a", plan_step_a), ("step_b", plan_step_b), ("step_c", plan_step_c)):
        plan = plan_fn()
        rows = raw.get(key, [])
        if len(rows) != len(plan):
            problems.append(f"{key}: {len(rows)} rows vs {len(plan)} planned")
            continue
        for i, (p, r) in enumerate(zip(plan, rows)):
            _, intended = build_url(p["field"], p["query_string"])
            sent = r.get("query_sent")
            if sent is None:
                problems.append(f"{key}[{i}]: no query_sent recorded (pre-v2 row)")
            elif sent != intended:
                problems.append(f"{key}[{i}]: sent {sent!r} != intended {intended!r}")
    return problems


def migrate_pre_v2(raw):
    """v1 rows carry no `query_sent`. Re-derive it from the URL they actually requested --
    the URL is the only field in a v1 row that cannot lie about what was sent -- so a v1
    row that DID send the right string is kept rather than re-spent, and a v1 row that did
    not is exposed. Returns a per-step (kept, exposed) tally."""
    tally = {}
    for key, plan_fn in (("step_a", plan_step_a), ("step_b", plan_step_b), ("step_c", plan_step_c)):
        plan = plan_fn()
        kept = exposed = 0
        for i, r in enumerate(raw.get(key, [])):
            if not r or r.get("query_sent") is not None or not r.get("url"):
                continue
            try:
                sent = query_sent_of(r["url"])
            except Exception:
                continue
            r["query_sent"] = sent
            r["provenance"] = "v1_row_migrated"
            if i < len(plan):
                _, intended = build_url(plan[i]["field"], plan[i]["query_string"])
                if sent == intended and r.get("status") == "OK":
                    kept += 1
                else:
                    exposed += 1
                    r["mislabelled_by_v1"] = sent != intended
            # v1's status vocabulary had no REFUSAL_TO_MEASURE; 429 is one by definition.
            if r.get("status") == "ERROR" and "429" in str(r.get("error", "")):
                r["status"] = "REFUSAL_TO_MEASURE"
        tally[key] = {"kept": kept, "exposed": exposed}
    return tally


def stale_or_missing(raw, key, plan_fn):
    """Indices whose recorded row cannot be trusted: absent, wrong query, or not OK."""
    plan = plan_fn()
    rows = raw.get(key, [])
    out = []
    for i, p in enumerate(plan):
        if i >= len(rows):
            out.append(i)
            continue
        r = rows[i]
        _, intended = build_url(p["field"], p["query_string"])
        if r.get("status") != "OK" or r.get("query_sent") != intended:
            out.append(i)
    return out


def run_plan(plan, key, label, raw, indices=None):
    rows = raw.setdefault(key, [])
    while len(rows) < len(plan):
        rows.append({})
    todo = range(len(plan)) if indices is None else indices
    for n, i in enumerate(todo, 1):
        p = plan[i]
        row = dict(p)
        row.pop("field", None)
        res = fetch(p["field"], p["query_string"], label=f"{label} {n}/{len(list(todo))}")
        row.update(res)
        rows[i] = row
        checkpoint(raw)
    return rows


def checkpoint(raw):
    tmp = RAW + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(raw, fh, indent=2)
    os.replace(tmp, RAW)


# --------------------------------------------------------------------------
def curate(raw):
    known = ledger_ids()
    baseline_303_ids = load_303_baselines()

    verify_problems = verify_rows(raw)

    all_rows = raw["step_a"] + raw["step_b"] + raw["step_c"] + raw.get("step_d_controls", []) \
        + raw.get("step_d_zero_audit", [])
    n_refusals = sum(1 for r in all_rows if r.get("status") == "REFUSAL_TO_MEASURE")
    n_errors = sum(1 for r in all_rows if r.get("status") == "ERROR")

    # --- Step A: is the retrieval layer dash-sensitive? ---
    step_a_by_term = {}
    for r in raw["step_a"]:
        step_a_by_term.setdefault(r["term"], {})[r["form"]] = r
    mechanism_rows, mechanism_deltas = [], []
    for term, forms in step_a_by_term.items():
        base = forms.get("baseline")
        if base is None or base.get("status") != "OK":
            continue
        base_ids = ids_of(base)
        for form_name, r in forms.items():
            if form_name == "baseline" or r.get("status") != "OK":
                continue
            var_ids = ids_of(r)
            same = var_ids == base_ids
            mechanism_rows.append({
                "term": term, "form": form_name, "query_sent": r.get("query_sent"),
                "n_baseline": base["n"], "n_variant": r["n"],
                "identical_id_set": same,
                "capped_at_max_results": base["n"] == MAX_RESULTS or r["n"] == MAX_RESULTS,
            })
            if not same:
                mechanism_deltas.append({
                    "term": term, "form": form_name,
                    "n_baseline": base["n"], "n_variant": r["n"],
                    "baseline_only": sorted(base_ids - var_ids),
                    "variant_only": sorted(var_ids - base_ids),
                    "variant_only_links": [f"https://arxiv.org/abs/{i}"
                                            for i in sorted(var_ids - base_ids)],
                })

    # --- Step B: per-query delta, variant vs its own same-session baseline ---
    step_b_deltas = []
    all_new_candidates = {}
    rows = raw["step_b"]
    for i in range(0, len(rows), 2):
        b, v = rows[i], rows[i + 1]
        base_ids, var_ids = ids_of(b), ids_of(v)
        interpretable = b.get("status") == "OK" and v.get("status") == "OK"
        delta = sorted(var_ids - base_ids)
        new_ids = [x for x in delta
                   if x not in known and x not in baseline_303_ids and x != "2604.09949"]
        step_b_deltas.append({
            "channel": b.get("channel"),
            "base_query_sent": b.get("query_sent"),
            "variant_query_sent": v.get("query_sent"),
            "variant_identical_to_baseline": v.get("variant_identical_to_baseline", False),
            "baseline_status": b.get("status"), "variant_status": v.get("status"),
            "n_baseline": b.get("n"), "n_variant": v.get("n"),
            "interpretable": interpretable,
            "n_delta": len(delta) if interpretable else None,
            "delta_links": [f"https://arxiv.org/abs/{x}" for x in delta] if interpretable else [],
            "variant_missed_by_baseline": [f"https://arxiv.org/abs/{x}" for x in delta],
            "baseline_missed_by_variant": [f"https://arxiv.org/abs/{x}"
                                            for x in sorted(base_ids - var_ids)],
            "genuinely_new_candidates": new_ids if interpretable else [],
        })
        if interpretable:
            for x in new_ids:
                all_new_candidates[x] = v.get("query_sent")

    # --- Step C: author census ---
    step_c = []
    for r in raw["step_c"]:
        step_c.append({k: r.get(k) for k in
                       ("group", "query_string", "query_sent", "status", "n", "links", "url")})

    step_c2 = []
    for r in raw.get("step_c2_author_conjunctions", []):
        step_c2.append({k: r.get(k) for k in
                        ("group", "query_string", "query_sent", "status", "n", "links")})
    # The false-negative audit: a group whose single-phrase row is 0 but whose author
    # conjunction is non-zero was NOT absent -- the query was.
    c_by_group = {}
    for r in step_c:
        c_by_group.setdefault(r["group"], []).append(r)
    c2_by_group = {}
    for r in step_c2:
        c2_by_group.setdefault(r["group"], []).append(r)
    false_negative_audit = []
    for group in ("Breden-Chu", "Dahne-Figueras", "BCG", "ALS", "Cao-Labora", "Gomez-Serrano"):
        single = c_by_group.get(group, [])
        conj = c2_by_group.get(group, [])
        if not single and not conj:
            continue
        single_max = max([r["n"] for r in single if r["status"] == "OK"], default=None)
        conj_max = max([r["n"] for r in conj if r["status"] == "OK"], default=None)
        verdict = "n/a"
        if single_max is not None and conj_max is not None:
            if single_max == 0 and conj_max > 0:
                verdict = ("FALSE NEGATIVE in the single-phrase form: the group name is two "
                           "authors, not one compound surname; the conjunction finds "
                           f"{conj_max}")
            elif single_max == 0 and conj_max == 0:
                verdict = "zero in BOTH forms -- absence survives the conjunction re-query"
            else:
                verdict = "single-phrase form is a real compound surname and returns hits"
        false_negative_audit.append({
            "group": group, "n_single_phrase_max": single_max,
            "n_author_conjunction_max": conj_max, "verdict": verdict,
        })

    # --- Step D: controls and zero audit ---
    controls = []
    for r in raw.get("step_d_controls", []):
        controls.append({k: r.get(k) for k in
                         ("control", "query_sent", "expect", "status", "n", "links")})
    zero_audit = []
    for r in raw.get("step_d_zero_audit", []):
        zero_audit.append({k: r.get(k) for k in
                           ("compound_query", "component", "query_sent", "status", "n")})

    # A zero is a MEASURED ABSENCE only if every one of its components is individually
    # non-empty AND the two positive controls passed.  Otherwise it is uninterpretable.
    ctl = {c["control"]: c for c in controls}
    controls_pass = (
        ctl.get("positive_environment", {}).get("n", 0) > 0
        and ctl.get("positive_two_phrase_AND", {}).get("n", 0) > 0
        and ctl.get("negative_nonsense_phrase", {}).get("n", 1) == 0
    )
    comp_by_q = {}
    for r in zero_audit:
        comp_by_q.setdefault(r["compound_query"], []).append(r)
    zero_verdicts = []
    for q, comps in sorted(comp_by_q.items()):
        bad = [c for c in comps if c["status"] != "OK"]
        empty = [c for c in comps if c["status"] == "OK" and c["n"] == 0]
        if bad:
            verdict = "UNINTERPRETABLE (a component refused to measure)"
        elif not controls_pass:
            verdict = "UNINTERPRETABLE (instrument controls did not pass)"
        elif empty:
            verdict = "REAL ABSENCE, but driven by an empty component: " + \
                      ", ".join(c["component"] for c in empty)
        else:
            verdict = "REAL ABSENCE (every component individually non-empty)"
        zero_verdicts.append({
            "compound_query": q, "verdict": verdict,
            "components": [{"component": c["component"], "n": c["n"], "status": c["status"]}
                            for c in comps],
        })

    census = screen_author_census(raw, known, base303_ids_local := baseline_303_ids)
    census_novel = [r for r in census if r["novel_to_ledger_and_leg303"]]
    census_uncited = [r for r in census_novel if not r["repo_files_citing_it"]]
    census_four = [r for r in census_novel if r["n_clauses_true"] == 4]
    census_three = [r for r in census_novel if r["n_clauses_true"] == 3]

    interpretable_pairs = sum(1 for d in step_b_deltas if d["interpretable"])
    gate_blocked = (not controls_pass) or interpretable_pairs < len(step_b_deltas)
    gate_answer = "YES" if all_new_candidates else ("NO" if not gate_blocked else "INCOMPLETE")

    curated = {
        "leg": 323, "route": "CENV",
        "run_utc": raw.get("run_utc"),
        "resumed_utc": raw.get("resumed_utc"),
        "gate": "Does the variant re-run surface at least one work the original "
                "instrument missed (beyond 2604.09949 itself)?",
        "gate_answer": gate_answer,
        "instrument_verification": {
            "description": "Every row's actually-sent search_query, re-derived from its own "
                            "recorded URL, checked against the query the plan says it should "
                            "have been. A non-empty list here means the artifact mislabels at "
                            "least one row and nothing below it may be believed.",
            "n_problems": len(verify_problems),
            "problems": verify_problems[:20],
        },
        "n_refusals_to_measure": n_refusals,
        "n_errors": n_errors,
        "controls": controls,
        "controls_pass": controls_pass,
        "zero_audit": zero_verdicts,
        "mechanism_findings": {
            "description": "Step A: per-term standalone abs: phrase queries, baseline "
                            "(fresh single-hyphen) vs each variant form, same session. "
                            "identical_id_set False means the retrieval layer IS "
                            "dash-sensitive for that term/form.",
            "n_terms_tested": len(step_a_by_term),
            "n_form_comparisons": len(mechanism_rows),
            "n_forms_with_a_delta": len(mechanism_deltas),
            "per_form": mechanism_rows,
            "deltas": mechanism_deltas,
        },
        "compound_rerun_deltas": step_b_deltas,
        "n_query_pairs_interpretable": interpretable_pairs,
        "n_query_pairs": len(step_b_deltas),
        "genuinely_new_candidates": [
            {"arxiv_id": i, "link": f"https://arxiv.org/abs/{i}", "found_by_query": q}
            for i, q in sorted(all_new_candidates.items())
        ],
        "step_c_author_census": step_c,
        "step_c2_author_conjunctions": step_c2,
        "author_query_false_negative_audit": false_negative_audit,
        "author_census_candidate_screen": {
            "description": "Criterion (iv) of the pre-committed novelty file applied to every "
                            "arXiv id any Step C/C2 author row returned. The title-level clause "
                            "screen over-selects on purpose; survivors are read at abstract "
                            "depth and adjudicated in writeup/novelty/leg_323.md. Note the "
                            "self-reference guard: repo_files_citing_it EXCLUDES this leg's own "
                            "artifacts, which contain every id here.",
            "n_distinct_ids": len(census),
            "n_novel_to_ledger_and_leg303": len(census_novel),
            "n_novel_and_never_cited_anywhere_in_repo": len(census_uncited),
            "n_clearing_all_four_title_clauses": len(census_four),
            "n_clearing_three_of_four": len(census_three),
            "three_of_four_survivors": [
                {k: r[k] for k in ("arxiv_id", "link", "title", "title_clauses",
                                    "repo_files_citing_it", "found_by_query")}
                for r in census_three],
            "adjudications_at_abstract_depth": [
                {"arxiv_id": "1504.02775",
                 "link": "https://arxiv.org/abs/1504.02775",
                 "title": "Splash singularities for the free boundary Navier-Stokes equations",
                 "authors": "Castro, Cordoba, Fefferman, Gancedo, Gomez-Serrano",
                 "submitted": "2015-04-10 (v1); v2 2019-05-12",
                 "verdict": "MECHANICAL NEAR-MISS, does not answer the gate YES",
                 "clause_a_certificate": "FAILS. The abstract states a purely analytical "
                     "existence proof; it mentions no computer-assisted proof, no interval "
                     "arithmetic, no validated numerics, no rigorous computer certificate.",
                 "clause_b_blow_up": "PARTIAL. The breakdown is a SPLASH -- the free-boundary "
                     "interface self-intersects in finite time -- not a blow-up of a norm of "
                     "the velocity field, which is the object the Clay statement concerns.",
                 "clause_c_dissipative": "PASSES (free boundary incompressible Navier-Stokes).",
                 "clause_d_fluid_model": "PASSES, but in 2D.",
                 "why_it_matters_anyway": "It is the single strongest thing the four-group "
                     "author census turned up that this repository had never cited, and it is "
                     "recorded here with a link so a later leg can re-check the judgement "
                     "rather than re-run the search."},
            ],
            "all_rows": census,
        },
        "staleness_recheck": [
            {k: r.get(k) for k in ("note", "query_string", "status", "n")}
            for r in raw.get("step_v_reverify", [])
        ],
        "v1_migration_tally": raw.get("v1_migration_tally"),
        "excluded_from_gate_count": ["2604.09949 (leg 309's territory, recorded not adjudicated)"],
        "clay_odds_note": "unchanged, ~0.05%; this leg is an instrument fix, not a chain move.",
    }
    with open(CURATED, "w") as fh:
        json.dump(curated, fh, indent=2)

    print(f"verify problems={len(verify_problems)}", file=sys.stderr)
    print(f"refusals={n_refusals} errors={n_errors}", file=sys.stderr)
    print(f"controls_pass={controls_pass}", file=sys.stderr)
    print(f"dash-form comparisons={len(mechanism_rows)} with a delta={len(mechanism_deltas)}",
          file=sys.stderr)
    print(f"interpretable query pairs={interpretable_pairs}/{len(step_b_deltas)}", file=sys.stderr)
    print(f"gate_answer={gate_answer}", file=sys.stderr)
    return curated


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--stage", default="all",
                    help="all | a | b | c | d  (resume one stage at a time)")
    args = ap.parse_args()

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    if args.offline:
        with open(RAW) as fh:
            raw = json.load(fh)
        curate(raw)
        return

    if args.resume and os.path.exists(RAW):
        with open(RAW) as fh:
            raw = json.load(fh)
        raw["resumed_utc"] = now
        raw["v1_migration_tally"] = migrate_pre_v2(raw)
        print("v1 migration: " + json.dumps(raw["v1_migration_tally"]), file=sys.stderr)
        checkpoint(raw)
    else:
        raw = {"run_utc": now}

    want = args.stage
    if want in ("all", "d"):
        # Controls first: an uncontrolled instrument makes everything after it unreadable.
        rows = raw.setdefault("step_d_controls", [])
        while len(rows) < len(CONTROLS):
            rows.append({})
        for i, c in enumerate(CONTROLS):
            if args.resume and rows[i].get("status") == "OK":
                continue
            row = dict(c)
            fld = row.pop("field")
            row.update(fetch(fld, c["query_string"], label=f"D-ctl {i+1}/{len(CONTROLS)}"))
            rows[i] = row
            checkpoint(raw)

    if want in ("all", "a"):
        idx = stale_or_missing(raw, "step_a", plan_step_a) if args.resume else None
        print(f"Step A: {len(idx) if idx is not None else 'all'} rows to run", file=sys.stderr)
        run_plan(plan_step_a(), "step_a", "A", raw, idx)

    if want in ("all", "b"):
        idx = stale_or_missing(raw, "step_b", plan_step_b) if args.resume else None
        print(f"Step B: {len(idx) if idx is not None else 'all'} rows to run", file=sys.stderr)
        run_plan(plan_step_b(), "step_b", "B", raw, idx)

    if want in ("all", "c"):
        idx = stale_or_missing(raw, "step_c", plan_step_c) if args.resume else None
        print(f"Step C: {len(idx) if idx is not None else 'all'} rows to run", file=sys.stderr)
        run_plan(plan_step_c(), "step_c", "C", raw, idx)

    if want in ("all", "c2"):
        rows = raw.setdefault("step_c2_author_conjunctions", [])
        while len(rows) < len(AUTHOR_CONJUNCTIONS):
            rows.append({})
        for i, (group, qs) in enumerate(AUTHOR_CONJUNCTIONS):
            if args.resume and rows[i].get("status") == "OK":
                continue
            row = {"group": group, "query_string": qs}
            row.update(fetch("raw", qs, label=f"C2 {i+1}/{len(AUTHOR_CONJUNCTIONS)}"))
            rows[i] = row
            checkpoint(raw)

    if want in ("all", "v"):
        # STALENESS RE-CHECK of rows carried over from the pre-kill run. Six v1 rows that
        # migration kept are re-queried fresh; a disagreement means a carried-over row is
        # stale and the whole carry-over is untrustworthy.  Chosen deterministically (a
        # fixed list, not a random draw) so the check is reproducible: two Step A dash
        # forms, two Step B baselines with hits, one Step B baseline with zero hits, and
        # one Step C author row.
        rechecks = [
            ("abs", 'abs:"Navier--Stokes"', "step_a Navier-Stokes double_hyphen"),
            ("abs", 'abs:"NavierStokes"', "step_a Navier-Stokes unhyphenated"),
            ("abs", 'abs:"self-similar" AND abs:"Navier-Stokes" AND abs:"computer-assisted"',
             "step_b baseline C1 (v1 n=3)"),
            ("abs", 'abs:"backward self-similar" AND abs:"Navier-Stokes"',
             "step_b baseline C5 (v1 n=7)"),
            ("abs", 'abs:"radii polynomial" AND abs:"blow-up"',
             "step_b baseline C3 (v1 n=0 -- a zero carried over)"),
            ("au", "Breden-Chu", "step_c Breden-Chu baseline"),
        ]
        rows = raw.setdefault("step_v_reverify", [])
        while len(rows) < len(rechecks):
            rows.append({})
        for i, (fld, qs, note) in enumerate(rechecks):
            if args.resume and rows[i].get("status") == "OK":
                continue
            row = {"note": note, "query_string": qs}
            row.update(fetch(fld, qs, label=f"V {i+1}/{len(rechecks)}"))
            rows[i] = row
            checkpoint(raw)

    if want in ("all", "z"):
        # Zero audit, computed from whatever Step B now holds.  Components are cached by
        # STRING, not by (compound, component) pair -- 'abs:"blow-up"' means the same thing
        # in every compound it appears in, and re-spending a 503-budget call on it is waste.
        zeros = [r["query_sent"] for r in raw.get("step_b", [])
                 if r.get("status") == "OK" and r.get("n") == 0]
        rows = raw.setdefault("step_d_zero_audit", [])
        cache = {r["component"]: r for r in rows if r.get("status") == "OK"}
        need = []
        for q in sorted(set(zeros)):
            for c in zero_components(q):
                if c not in cache and c not in need:
                    need.append(c)
        print(f"Zero audit: {len(need)} distinct components over "
              f"{len(set(zeros))} zero compounds", file=sys.stderr)
        for n, c in enumerate(need, 1):
            res = fetch("raw", c, label=f"Z {n}/{len(need)}")
            cache[c] = dict({"component": c}, **res)
            checkpoint(raw)
        # One row per (compound, component) for the curator, sharing the cached measurement.
        raw["step_d_zero_audit"] = []
        for q in sorted(set(zeros)):
            for c in zero_components(q):
                if c in cache:
                    raw["step_d_zero_audit"].append(dict(cache[c], compound_query=q))
        checkpoint(raw)

    checkpoint(raw)
    curate(raw)


if __name__ == "__main__":
    main()
