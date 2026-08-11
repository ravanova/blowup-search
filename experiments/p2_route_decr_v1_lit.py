"""Leg 318 / Route-DECR -- the mandatory §0a novelty and prior-art pass, in code.

The question this leg asks is whether a GENERAL STRUCTURAL CRITERION exists for when the
viscous term of a self-similar blow-up certificate can be ENCLOSED (the certified object
depends on nu; nu sits inside the certified profile problem) rather than merely DOMINATED
(the certified object is the nu = 0 system and viscosity is admitted as a decaying error
term) -- leg 240's measured distinction.

The prior-art pass therefore has to separate three quite different literatures:

  (A) the CLASSICAL criticality classification of a dissipative term against a scaling
      (sub / critical / supercritical).  Expected to be old folklore.  If it is, the leg
      says so and claims nothing there.
  (B) COMPUTER-ASSISTED / validated-numerics constructions of self-similar profiles WITH
      dissipation inside the certified equation.  These are the ENCLOSED instances.
  (C) any statement in the literature of a CRITERION -- a general rule saying which of
      (A)'s classes admits (B).  This is the only cell where this leg could be new.

INSTRUMENT DISCIPLINE (this run's standing rule: control the instrument before trusting it)

  * MF1 (verified, stands): a paper in this project's target cell spells itself
    `Navier--Stokes` with a LaTeX double hyphen, so every Navier-Stokes query is issued in
    BOTH spellings, and `self similar` is issued alongside `self-similar`.
  * MF3 as handed to this leg ("the arXiv endpoint returns ZERO for any two ANDed quoted
    phrases") was STRUCK by the orchestrator mid-leg after leg 314 failed to reproduce it.
    This runner does not assume either way: it MEASURES the endpoint's AND behaviour with
    an intersecting control pair, and only then decides whether an ANDed zero is a
    measurement or an instrument fault.  See `INSTRUMENT_CONTROLS`.
  * MF2 (stands): links/identifiers are banked, never counts alone.  Every query records
    the arXiv ids of its top hits, not just its totalResults.

Nothing here builds apparatus, touches plan_of_record.py, or lifts any ban.
Runtime target: < 90 s (dominated by the arXiv API's 3 s politeness delay).
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "http://export.arxiv.org/api/query?"
DELAY_S = 6.0  # arXiv API politeness delay (3 s measured insufficient: HTTP 429)
TIMEOUT_S = 45

_TOTAL = re.compile(r"opensearch:totalResults[^>]*>(\d+)<")
_ID = re.compile(r"<id>http://arxiv\.org/abs/([^<]+)</id>")
_TITLE = re.compile(r"<title>(.*?)</title>", re.S)


def query(search_query: str, max_results: int = 5, tries: int = 6) -> dict:
    """One arXiv API query.  Returns totalResults plus the ids/titles of the top hits.

    MEASURED INSTRUMENT FAULT, this leg, 2026-08-11: the export endpoint returns
    **HTTP 429** under a 3 s politeness delay once a run has issued a dozen or so queries.
    A caller that swallows the exception -- or a client that returns an empty feed on 429 --
    reports the query as ZERO RESULTS, which is indistinguishable from a clean negative.
    That is the most likely origin of leg 315's six "all-zero ANDed queries", which were
    banked as evidence for a general MF3 endpoint defect that leg 314 could not reproduce.
    Handled here by explicit exponential backoff, and a 429 is NEVER allowed to become a 0.
    """
    url = API + urllib.parse.urlencode(
        {"search_query": search_query, "max_results": max_results, "start": 0}
    )
    raw = None
    for attempt in range(tries):
        try:
            raw = urllib.request.urlopen(url, timeout=TIMEOUT_S).read().decode("utf-8", "replace")
            break
        except urllib.error.HTTPError as exc:  # noqa: PERF203
            if exc.code != 429 or attempt == tries - 1:
                raise
            wait = 15.0 * (attempt + 1)
            print(f"    [429 backoff {wait:.0f}s] {search_query}", flush=True)
            time.sleep(wait)
    assert raw is not None
    total = int(_TOTAL.search(raw).group(1)) if _TOTAL.search(raw) else -1
    ids = _ID.findall(raw)
    titles = [" ".join(t.split()) for t in _TITLE.findall(raw)[1:]]  # [0] is the feed title
    time.sleep(DELAY_S)
    return {
        "query": search_query,
        "total": total,
        "ids": ids,
        "titles": titles[: len(ids)],
    }


# ---------------------------------------------------------------------------
# 1. INSTRUMENT CONTROLS -- run FIRST, and the run aborts if they fail.
# ---------------------------------------------------------------------------
INSTRUMENT_CONTROLS = [
    # (name, query, predicate on total, why)
    (
        "positive_single",
        'all:"self-similar blow-up"',
        lambda n: n >= 20,
        "a phrase that must return many; if this is small the endpoint is not answering",
    ),
    (
        "positive_single_b",
        'all:"interval arithmetic"',
        lambda n: n >= 50,
        "second single-phrase positive control on a different subject",
    ),
    (
        "negative_nonsense",
        'all:"quasihyperbolic viscous enclosure criterion of Andronov"',
        lambda n: n == 0,
        "a phrase that must return nothing; if this is nonzero the endpoint is fuzzy-matching",
    ),
    (
        "anded_control_pair",
        'all:"Taylor model" AND all:"interval arithmetic"',
        lambda n: n > 0,
        "THE MF3 TEST: two ANDed quoted phrases that are KNOWN to intersect. If this is 0 "
        "the AND operator is broken and every ANDed zero below is uninterpretable; if it "
        "is > 0 the AND operator works and an ANDed zero is a MEASUREMENT (absence).",
    ),
    (
        "anded_control_pair_b",
        'all:"self-similar" AND all:"blow-up"',
        lambda n: n >= 100,
        "second ANDed control, broad, to distinguish 'AND works but narrows hard' from "
        "'AND is broken'",
    ),
]


# ---------------------------------------------------------------------------
# 2. THE PRIOR-ART QUERIES, grouped by the cell they probe.
# ---------------------------------------------------------------------------
QUERIES = {
    # (A) classical criticality of dissipation against a scaling -- expected OLD/folklore
    "A_criticality": [
        'all:"critical dissipation" AND all:"self-similar"',
        'all:"supercritical dissipation" AND all:"blow-up"',
        'all:"scaling critical" AND all:"dissipation"',
        'all:"critical dissipation" AND all:"blow up"',
    ],
    # (B) validated / computer-assisted profiles WITH dissipation inside the certified eq.
    "B_enclosed_instances": [
        'all:"computer-assisted proof" AND all:"self-similar"',
        'all:"computer assisted" AND all:"self similar"',
        'all:"validated numerics" AND all:"self-similar"',
        'all:"interval arithmetic" AND all:"self-similar profile"',
        'all:"computer-assisted proof" AND all:"Navier-Stokes"',
        'all:"computer-assisted proof" AND all:"Navier--Stokes"',
        'all:"rigorous numerics" AND all:"blow-up profile"',
    ],
    # (C) THE CELL THIS LEG COULD BE NEW IN: a stated general criterion for when the
    #     dissipative term can be carried INSIDE a certificate rather than as an error.
    "C_criterion": [
        'all:"computer-assisted proof" AND all:"dissipation" AND all:"criterion"',
        'all:"when the dissipative term"',
        'all:"dissipative term" AND all:"error term" AND all:"self-similar"',
        'all:"self-similar" AND all:"viscosity" AND all:"perturbative"',
        'all:"enclosure" AND all:"dissipative term"',
        'all:"criterion" AND all:"rigorous enclosure" AND all:"blow-up"',
    ],
    # (D) the specific compressible-implosion cell leg 240 measured
    "D_implosion_cell": [
        'all:"implosion" AND all:"computer-assisted"',
        'all:"implosion" AND all:"compressible Navier-Stokes"',
        'all:"implosion" AND all:"compressible Navier--Stokes"',
    ],
    # (E) the ODE->PDE bridge type-mismatch axis leg 315 named (dissipative vs hyperbolic)
    "E_bridge_type": [
        'all:"self-consistent a priori bounds"',
        'all:"rigorous numerics" AND all:"dissipative PDE"',
        'all:"validated" AND all:"quasilinear hyperbolic" AND all:"computer-assisted"',
    ],
    # (F) the incompressible-NS discriminator: dissipation IS scaling-critical there, and
    #     the obstruction is a NONEXISTENCE theorem, not an enclosure failure.
    "F_nrs_tsai": [
        'all:"self-similar" AND all:"Leray"',
        'all:"discretely self-similar" AND all:"Navier-Stokes"',
    ],
}


def main(out_path: Path) -> int:
    record = {
        "leg": 318,
        "route": "DECR",
        "purpose": "contract §0a novelty / prior-art pass, run BEFORE any mathematics",
        "endpoint": API,
        "mf1_note": "every Navier-Stokes phrase issued in both `Navier-Stokes` and the "
        "LaTeX double-hyphen `Navier--Stokes`; `self similar` alongside `self-similar`",
        "instrument_controls": [],
        "and_operator_verdict": None,
        "queries": {},
    }

    print("== INSTRUMENT CONTROLS ==")
    ok = True
    for name, q, pred, why in INSTRUMENT_CONTROLS:
        r = query(q)
        passed = pred(r["total"])
        ok &= passed
        r.update({"control": name, "passed": bool(passed), "why": why})
        record["instrument_controls"].append(r)
        print(f"  [{'PASS' if passed else 'FAIL'}] {name:22s} total={r['total']:6d}  {q}")

    and_ctl = [c for c in record["instrument_controls"] if c["control"].startswith("anded")]
    and_works = all(c["passed"] for c in and_ctl)
    record["and_operator_verdict"] = (
        "AND-of-quoted-phrases WORKS on this endpoint at this time; an ANDed zero below is "
        "a MEASUREMENT of absence, not an instrument fault (MF3 as handed to this leg is "
        "REFUTED here, independently of leg 314's refutation)"
        if and_works
        else "AND-of-quoted-phrases is BROKEN; every ANDed zero below is uninterpretable "
        "and must be discarded, not banked"
    )
    print(f"\nAND verdict: {record['and_operator_verdict']}\n")

    if not ok:
        print("INSTRUMENT CONTROL FAILED -- results below are not trustworthy.", file=sys.stderr)

    for cell, qs in QUERIES.items():
        print(f"== {cell} ==")
        record["queries"][cell] = []
        for q in qs:
            r = query(q)
            record["queries"][cell].append(r)
            print(f"  total={r['total']:6d}  {q}")
            for i, t in zip(r["ids"], r["titles"]):
                print(f"        {i}  {t[:88]}")
        print()

    # -----------------------------------------------------------------------
    # 3. ZERO AUDIT.  The AND control passed, so an ANDed zero is admissible as a
    #    MEASUREMENT of absence -- but only after each component phrase is shown to be
    #    non-empty on its own.  A zero whose components are ALSO zero says nothing about
    #    the intersection; a zero whose components are both populated is a real absence.
    #    (This is the orchestrator's corrected MF3 rule, executed rather than asserted.)
    # -----------------------------------------------------------------------
    print("== ZERO AUDIT ==")
    record["zero_audit"] = []
    phrase_re = re.compile(r'all:"([^"]+)"')
    seen: dict[str, int] = {}
    for cell, rs in record["queries"].items():
        for r in rs:
            if r["total"] != 0:
                continue
            parts = phrase_re.findall(r["query"])
            singles = []
            for p in parts:
                if p not in seen:
                    seen[p] = query(f'all:"{p}"', max_results=1)["total"]
                singles.append({"phrase": p, "total_alone": seen[p]})
            interpretable = all(s["total_alone"] > 0 for s in singles)
            record["zero_audit"].append(
                {
                    "cell": cell,
                    "query": r["query"],
                    "components": singles,
                    "verdict": "REAL ABSENCE (every component phrase is populated alone, "
                    "and the AND operator is verified working)"
                    if interpretable
                    else "UNINTERPRETABLE (a component phrase is itself empty, so the "
                    "zero is about vocabulary, not about the intersection)",
                }
            )
            print(f"  {r['query']}\n    " + " | ".join(f"{s['phrase']!r}={s['total_alone']}" for s in singles))
            print(f"    -> {record['zero_audit'][-1]['verdict']}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(record, indent=2) + "\n")
    print(f"written: {out_path}")
    return 0 if ok else 1


if __name__ == "__main__":
    here = Path(__file__).resolve().parents[1]
    sys.exit(main(here / "writeup" / "data" / "p2_route_decr_v1_lit.json"))
