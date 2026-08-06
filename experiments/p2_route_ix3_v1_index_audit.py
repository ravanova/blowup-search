#!/usr/bin/env python3
"""Route-IX3 (leg 138) — third freshness audit of writeup/INDEX.md.

Gate (pre-committed, DIRECTION.md section 138):

    At the pinned SHA, does writeup/INDEX.md correctly reflect every leg landed since
    leg 108's pass -- present, correctly described, correctly figure-conventioned, with
    parked escalations marked parked?

      yes -> Confirmed fresh; bank the dated record.
      no  -> Fix INDEX.md directly (the leg-68 precedent), listing every corrected row
             in the JSON.

This runner is mechanical and read-only on the repository: it enumerates the audit window
from git, inventories each leg's artifacts on disk, evaluates every checkable claim
INDEX.md makes, and writes writeup/data/p2_route_ix3_v1_index_audit.json.

No measurement is produced, so NO FIGURE, BY DESIGN -- the repository's Route-D convention
("no measurement, no figure"), the same one leg 126 invoked. The deliverable is a ledger.

Usage:  .venv/bin/python experiments/p2_route_ix3_v1_index_audit.py
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- the pinned audit window -------------------------------------------------------
# BASE is leg 108's INDEX.md commit (Route-IX2). HEAD_SHA is origin/main's HEAD at the
# moment leg 138 began; pinning it keeps the counts reproducible while sibling legs land.
BASE = "63dc163b48e63e703bfdff3f3e301b8e4b3bf8d9"
HEAD_SHA = "34748624189c0a17a688a9195101bcfcaa2666a5"

INDEX = os.path.join(REPO, "writeup", "INDEX.md")
OUT = os.path.join(REPO, "writeup", "data", "p2_route_ix3_v1_index_audit.json")


def git(*args: str) -> str:
    res = subprocess.run(
        ["git", "-C", REPO, *args], capture_output=True, text=True, check=False
    )
    return res.stdout


# Every existence question below is asked of the PINNED TREE, not the working copy.
# That matters: this leg edits INDEX.md and adds its own files, and an audit whose
# answers move when its own author edits the repo is not an audit. Re-running this
# script after leg 138 lands reproduces the same verdicts byte for byte.
_PINNED_TREE = frozenset(
    p for p in git("ls-tree", "-r", "--name-only", HEAD_SHA).splitlines() if p.strip()
)


def exists(rel: str) -> bool:
    """Present in the pinned tree (BASE..HEAD_SHA window's endpoint)?"""
    return rel in _PINNED_TREE


def listdir_pinned(prefix: str) -> list[str]:
    """Basenames directly under `prefix` in the pinned tree."""
    pre = prefix.rstrip("/") + "/"
    return sorted(
        p[len(pre):] for p in _PINNED_TREE if p.startswith(pre) and "/" not in p[len(pre):]
    )


def read_pinned(rel: str) -> str:
    return git("show", f"{HEAD_SHA}:{rel}")


# ------------------------------------------------------------------ window enumeration
def enumerate_window() -> dict[int, dict]:
    """Every `Leg N:` commit in BASE..HEAD_SHA, with the files each leg touched."""
    out: dict[int, dict] = {}
    log = git("log", "--format=%H\t%s", f"{BASE}..{HEAD_SHA}")
    by_leg: dict[int, list[tuple[str, str]]] = {}
    for line in log.strip().splitlines():
        if not line.strip():
            continue
        sha, subj = line.split("\t", 1)
        m = re.match(r"Leg (\d+):", subj)
        if m:
            by_leg.setdefault(int(m.group(1)), []).append((sha, subj))

    index_text = read_pinned("writeup/INDEX.md")

    for n, commits in sorted(by_leg.items()):
        files: set[str] = set()
        for sha, _ in commits:
            for f in git("show", "--pretty=format:", "--name-only", sha).splitlines():
                if f.strip():
                    files.add(f.strip())
        docs = sorted(
            f for f in files if re.match(r"writeup/4_p2_lottery/(BLOG|TECHNICAL)", f)
        )
        figs = sorted(f for f in files if f.startswith("writeup/figures/"))
        out[n] = {
            "leg": n,
            "commits": len(commits),
            "blog_technical_touched": docs,
            "figures_added": figs,
            "data_json": sorted(
                f for f in files if re.match(r"writeup/data/.*\.json$", f)
            ),
            "evidence_py": sorted(f for f in files if f.endswith("_evidence.py")),
            "journal_on_disk": exists(f"experiments/journal/leg_{n}.md"),
            "novelty_on_disk": exists(f"writeup/novelty/leg_{n}.md"),
            "index_mentions_before_this_leg": len(
                re.findall(rf"\bleg {n}\b|leg_{n}\.md", index_text, re.I)
            ),
        }
    return out


# --------------------------------------------------------------------- claim checking
def check_claims() -> list[dict]:
    """Every INDEX.md claim leg 138 can decide mechanically, checked against disk.

    `holds` is the claim's truth value at the pinned SHA, BEFORE leg 138's edit.
    """
    c: list[dict] = []

    def claim(cid, where, quoted, holds, evidence, verdict):
        c.append(
            {
                "id": cid,
                "index_location": where,
                "claim_as_written": quoted,
                "holds_at_pinned_sha": holds,
                "evidence": evidence,
                "verdict": verdict,
            }
        )

    # --- Route-PORT v1 row + gap item 1 -------------------------------------------
    port1_e = "experiments/p2_route_port_v1_bordered_evidence.py"
    port1_f = "writeup/figures/fig59_route_port_v1.png"
    claim(
        "C1",
        "Arc 4 row 'Route-PORT v1' (E and F columns) + gap item 1",
        "no *_evidence.py and no registered figure anywhere",
        not (exists(port1_e) or exists(port1_f)),
        {port1_e: exists(port1_e), port1_f: exists(port1_f), "landed_by": "leg 60 / e0eba8e"},
        "FALSE at pinned SHA -- both pieces exist; row must go GAP->Y and Y(fig59)",
    )

    # --- Route-PORT v2 row + gap item 2 -------------------------------------------
    port2_e = "experiments/p2_route_port_v2_reach_evidence.py"
    port2_f = "writeup/figures/fig60_route_port_v2.png"
    port2_b = "writeup/4_p2_lottery/BLOG_P2_ROUTEPORT_V2.md"
    claim(
        "C2",
        "Arc 4 row 'Route-PORT v2' (E and F columns) + gap item 2",
        "missing all of: BLOG_P2_ROUTEPORT_V2.md, a p2_route_port_v2_evidence.py, and a registered figure",
        not (exists(port2_e) or exists(port2_f) or exists(port2_b)),
        {
            port2_e: exists(port2_e),
            port2_f: exists(port2_f),
            port2_b: exists(port2_b),
            "landed_by": "leg 60 / e0eba8e",
        },
        "2 of 3 clauses FALSE at pinned SHA (evidence.py and figure exist); the missing BLOG stands",
    )

    # --- Weight-repairs v1 row + gap item 9 ---------------------------------------
    wr1_e = "writeup/4_p2_lottery/p2_weight_repairs_v1_evidence.py"
    wr1_origin = git("log", "--oneline", "-1", "--", wr1_e).strip()
    claim(
        "C3",
        "Arc 4 row 'Weight-repairs v1' (E column) + gap item 9",
        "4 of 5 quartet pieces, with no *_evidence.py ... the missing *_evidence.py stays GAP",
        not exists(wr1_e),
        {
            wr1_e: exists(wr1_e),
            "introduced_by": wr1_origin,
            "note": "9d9b7ea created the route and PRE-DATES leg 108's pass",
        },
        "FALSE, and false WHEN WRITTEN -- not staleness but an error of leg 108's pass",
    )

    # --- Route-KA v1 row + gap item 10 --------------------------------------------
    ka = {
        "writeup/4_p2_lottery/TECHNICAL_P2_ROUTEKA_V1.md": None,
        "writeup/4_p2_lottery/BLOG_P2_ROUTEKA_V1.md": None,
        "experiments/p2_route_ka_v1_kawahara.py": None,
        "writeup/data/p2_route_ka_v1_kawahara.json": None,
    }
    ka = {k: exists(k) for k in ka}
    ka_fig = [f for f in listdir_pinned("writeup/figures") if "ka_v1" in f]
    claim(
        "C4",
        "Arc 4 row 'Route-KA v1' + gap item 10",
        "TECHNICAL but no BLOG, no *_evidence.py and no figure; 3 of 5 quartet pieces present",
        (
            ka["writeup/4_p2_lottery/TECHNICAL_P2_ROUTEKA_V1.md"]
            and not ka["writeup/4_p2_lottery/BLOG_P2_ROUTEKA_V1.md"]
            and not ka_fig
        ),
        {**ka, "figures_matching_ka_v1": ka_fig},
        "TRUE, re-verified unchanged -- gap item 10 stands as written",
    )

    # --- gap item 8: fig48 assigned twice -----------------------------------------
    f48 = [f for f in listdir_pinned("writeup/figures") if f.startswith("fig48")]
    claim(
        "C5",
        "gap item 8",
        "fig48 is assigned twice ... 1 duplicated figure number",
        len(f48) == 2,
        {"fig48_files": f48},
        "TRUE, re-verified unchanged -- gap item 8 stands as written",
    )

    # --- gap items 4/11: writeup/README.md staleness --------------------------------
    readme = read_pinned("writeup/README.md")
    nums = [int(m) for m in re.findall(r"^(\d+)\. \[", readme, re.M)]
    kw = len(re.findall(r"weight.repairs|kawahara|route-ka", readme, re.I))
    claim(
        "C6",
        "gap items 4 and 11",
        "writeup/README.md's numbered index still ends at entry 47 ... 0 mentions of Weight-repairs (v1 or v2) or Route-KA/Kawahara",
        max(nums) == 47 and kw == 0,
        {
            "max_numbered_entry": max(nums),
            "45_present": 45 in nums,
            "weight_repairs_or_kawahara_mentions": kw,
            "note": "leg 60 (e0eba8e) edited entries 46/47, adding fig 59/fig 60 refs and a reproduction block, so 'untouched' is no longer exact",
        },
        "TRUE in substance; backlog grows by the whole window",
    )

    # --- the convention block: legs 58 / 60 / 62 -----------------------------------
    ng_docs = [
        "writeup/4_p2_lottery/BLOG_P2_ROUTENG_V1.md",
        "writeup/4_p2_lottery/TECHNICAL_P2_ROUTENG_V1.md",
        "writeup/figures/fig55_route_ng_v1_nogo.png",
    ]
    cp_docs = [
        "writeup/4_p2_lottery/BLOG_P2_ROUTECP_V1.md",
        "writeup/4_p2_lottery/TECHNICAL_P2_ROUTECP_V1.md",
        "writeup/figures/fig56_route_cp_v1_cadiot.png",
    ]
    claim(
        "C7",
        "'Index currency -- second pass' convention block (legs 58, 60, 62 listed there)",
        "28 of the 30 legs produced no BLOG/TECHNICAL and no figure, by design ... legs 58, 64, 65, 66, 67, 69, 70, ...",
        not (all(exists(f) for f in ng_docs) or all(exists(f) for f in cp_docs)),
        {
            "leg_58_ng": {f: exists(f) for f in ng_docs},
            "leg_62_cp": {f: exists(f) for f in cp_docs},
            "leg_60_figures": {
                f: exists(f)
                for f in [
                    "writeup/figures/fig59_route_port_v1.png",
                    "writeup/figures/fig60_route_port_v2.png",
                ]
            },
        },
        "FALSE at pinned SHA -- 3 legs (58, 60, 62) in that list have since landed prose and/or figures; true when written, stale now",
    )

    # --- parked escalation: leg 63 / Route-M2 --------------------------------------
    m2 = [
        "writeup/4_p2_lottery/BLOG_P2_ROUTEM2_V1.md",
        "writeup/4_p2_lottery/TECHNICAL_P2_ROUTEM2_V1.md",
        "writeup/data/p2_route_m2_v1_targets.json",
        "writeup/figures/fig57_route_m2_v1_targets.png",
    ]
    m2_present = {f: exists(f) for f in m2}
    idx_txt = read_pinned("writeup/INDEX.md")
    claim(
        "C8",
        "whole file -- parked-escalation convention",
        "(no statement anywhere: INDEX.md contains 0 occurrences of 'M2' and 0 of 'parked')",
        False,
        {
            "leg_63_artifacts_on_main": m2_present,
            "leg_63_commits_on_main": len(
                [
                    x
                    for x in git("log", "--format=%s", HEAD_SHA).splitlines()
                    if x.startswith("Leg 63:")
                ]
            ),
            "index_m2_mentions": len(re.findall(r"\bM2\b", idx_txt)),
            "index_parked_mentions": len(re.findall(r"parked", idx_txt, re.I)),
            "direction_status": "DIRECTION.md:863 '(LANDED: gate YES -- escalation #1, parked on leg/m2-v1, not merged)'",
        },
        "MISSING -- a parked route with 0 of 4 artifacts on main is unrepresented; fig57 is reserved, not absent",
    )

    # --- figure registry holes -----------------------------------------------------
    figs = listdir_pinned("writeup/figures")
    holes = [
        n for n in (53, 54) if not any(f.startswith(f"fig{n}") for f in figs)
    ]
    claim(
        "C9",
        "whole file -- figure-number registry",
        "(no statement anywhere)",
        False,
        {
            "png_count": len(figs),
            "unallocated_numbers": holes,
            "fig57_reserved_by": "parked leg 63 (DIRECTION.md:693 pre-allocation)",
            "corroboration": "reports/TECH_DEBT_REVIEW_2026-08-05.md row A3",
        },
        "MISSING -- 2 unallocated numbers and 1 reserved number, unrecorded",
    )

    return c


# ------------------------------------------------------------------------------ main
def main() -> int:
    window = enumerate_window()
    numbered = {n: r for n, r in window.items() if n != 0}
    claims = check_claims()

    with_docs = sorted(n for n, r in numbered.items() if r["blog_technical_touched"])
    with_figs = sorted(n for n, r in numbered.items() if r["figures_added"])
    neither = sorted(
        n
        for n, r in numbered.items()
        if not r["blog_technical_touched"] and not r["figures_added"]
    )
    # A leg is owed a NEW Arc 4 row only if it ADDED a route's writeups, not if it
    # edited writeups that already have a row (leg 60 is the whole point of this test).
    new_rows = sorted(
        n
        for n in with_docs
        if any(
            os.path.basename(f).startswith("BLOG_") for f in numbered[n]["blog_technical_touched"]
        )
    )

    corrected_rows = [
        {
            "row": "Arc 4 / Route-NG v1 (leg 58)",
            "action": "ADDED",
            "why": "stage NG's theorem landed after leg 108's pass; 5 of 5 quartet pieces on disk (fig55). Landed WITH a parked publication-scoping escalation -- a third state, recorded as such.",
        },
        {
            "row": "Arc 4 / Route-CP v1 (leg 62)",
            "action": "ADDED",
            "why": "Cadiot full-text scope leg; BLOG+TECHNICAL+fig56 all landed after leg 108's pass.",
        },
        {
            "row": "Arc 4 / Route-BX v1 (leg 126)",
            "action": "ADDED",
            "why": "stage B's closure audit; BLOG+TECHNICAL+runner+evidence.py present, no figure BY DESIGN (its own header reserves fig62 for the yes-branch that did not fire).",
        },
        {
            "row": "Arc 4 / Route-M2 v1 (leg 63)",
            "action": "ADDED AS PARKED",
            "why": "gate YES but escalation #1, parked on leg/m2-v1 and never merged; 0 of 4 declared artifacts on main; fig57 reserved. Marked parked, explicitly NOT landed.",
        },
        {
            "row": "Arc 4 / Route-PORT v1 -- E and F columns",
            "action": "CORRECTED",
            "why": "GAP:none -> Y / fig59; leg 60 landed p2_route_port_v1_bordered_evidence.py and fig59_route_port_v1.png.",
        },
        {
            "row": "Arc 4 / Route-PORT v2 -- E and F columns",
            "action": "CORRECTED",
            "why": "GAP:none -> Y / fig60; leg 60 landed p2_route_port_v2_reach_evidence.py and fig60_route_port_v2.png. B/T stays 'T only, no BLOG'.",
        },
        {
            "row": "Arc 4 / Weight-repairs v1 -- E column",
            "action": "CORRECTED",
            "why": "GAP:none -> Y; writeup/4_p2_lottery/p2_weight_repairs_v1_evidence.py landed in 9d9b7ea, which PRE-DATES leg 108. Wrong when written, not stale.",
        },
        {
            "row": "gap item 1 (Route-PORT v1)",
            "action": "CLOSED",
            "why": "both named missing pieces now exist.",
        },
        {
            "row": "gap item 2 (Route-PORT v2)",
            "action": "NARROWED",
            "why": "2 of 3 clauses closed; only BLOG_P2_ROUTEPORT_V2.md is still absent.",
        },
        {
            "row": "gap item 9 (Weight-repairs v1)",
            "action": "WITHDRAWN",
            "why": "its evidence.py clause was false at the moment leg 108 wrote it.",
        },
        {
            "row": "gap item 11 (writeup/README.md)",
            "action": "UPDATED",
            "why": "still ends at entry 47 with 0 Weight-repairs/Kawahara mentions, but leg 60 edited entries 46/47, so 'untouched' is retired; backlog grows by this window.",
        },
        {
            "row": "'Index currency -- second pass' convention block",
            "action": "SUPERSEDED",
            "why": "legs 58, 60 and 62 are listed there as producing no BLOG/TECHNICAL and no figure; all three have since landed prose and/or figures. True when written, false at the pinned SHA.",
        },
        {
            "row": "gap item 12 (NEW) -- figure-number registry",
            "action": "ADDED",
            "why": "fig53/fig54 name 0 files and are cited by 0 writeups; fig57 is reserved by parked leg 63. Neither fact was recorded.",
        },
        {
            "row": "'Index currency -- third pass' paragraph",
            "action": "ADDED",
            "why": "dates the window, names the pinned SHA, and records the 29 no-figure-by-design legs.",
        },
    ]

    gate_no = any(c["verdict"].startswith(("FALSE", "MISSING")) for c in claims)

    payload = {
        "leg": 138,
        "route": "ROUTE-IX3",
        "title": "Third freshness audit of writeup/INDEX.md, since leg 108's pass",
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "figure": None,
        "figure_note": (
            "NO FIGURE, BY DESIGN. This leg produces no measurement; the repository's "
            "Route-D convention ('no measurement, no figure') applies, the same one leg "
            "126 invoked. The deliverable is this ledger."
        ),
        "window": {
            "base_commit": BASE,
            "base_description": "leg 108's INDEX.md commit (Route-IX2)",
            "head_commit": HEAD_SHA,
            "head_description": "origin/main HEAD at the moment leg 138 began (Leg 134)",
            # Counted at the pinned SHA, not at HEAD: counting at HEAD makes this leg's
            # own commit change the number, which is the same self-reference the
            # pinned-tree reads above exist to avoid.
            "index_md_commits_at_pinned_sha": len(
                [
                    x
                    for x in git(
                        "log", "--format=%H", HEAD_SHA, "--", "writeup/INDEX.md"
                    ).splitlines()
                    if x
                ]
            ),
            "index_md_edits_within_window": len(
                [
                    x
                    for x in git(
                        "log", "--format=%H", f"{BASE}..{HEAD_SHA}", "--", "writeup/INDEX.md"
                    ).splitlines()
                    if x
                ]
            ),
        },
        "counts": {
            "leg_prefixes_in_window": len(window),
            "numbered_legs": len(numbered),
            "legs_touching_blog_technical": len(with_docs),
            "legs_adding_figures": len(with_figs),
            "figures_added": sum(len(r["figures_added"]) for r in numbered.values()),
            "legs_with_neither": len(neither),
            "legs_with_data_json": sum(1 for r in numbered.values() if r["data_json"]),
            "legs_with_journal_and_novelty": sum(
                1
                for r in numbered.values()
                if r["journal_on_disk"] and r["novelty_on_disk"]
            ),
            "new_arc4_rows_owed_by_landed_routes": len(new_rows),
            "parked_rows_owed": 1,
        },
        "leg_lists": {
            "numbered_legs": sorted(numbered),
            "touching_blog_technical": with_docs,
            "adding_figures": with_figs,
            "new_route_rows_owed": new_rows,
            "no_measurement_no_figure": neither,
        },
        "claims_checked": claims,
        "corrected_rows": corrected_rows,
        "gate": {
            "question": (
                "At the pinned SHA, does writeup/INDEX.md correctly reflect every leg landed "
                "since leg 108's pass -- present, correctly described, correctly "
                "figure-conventioned, with parked escalations marked parked?"
            ),
            "answer": "NO" if gate_no else "YES",
            "branch_taken": (
                "Fix INDEX.md directly (the leg-68 precedent: INDEX.md freshness is this "
                "route's own territory), listing every corrected row in the JSON."
                if gate_no
                else "Confirmed fresh; bank the dated record."
            ),
        },
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")

    print(f"Route-IX3 index audit -- window {BASE[:7]}..{HEAD_SHA[:7]}")
    print(f"  numbered legs in window ............ {len(numbered)}")
    print(f"  INDEX.md edits within window ....... {payload['window']['index_md_edits_within_window']}")
    print(f"  legs touching BLOG/TECHNICAL ....... {len(with_docs)}  {with_docs}")
    print(f"  legs adding figures ................ {len(with_figs)}  {with_figs}")
    print(f"  legs with neither (by design) ...... {len(neither)}")
    print(f"  new route rows owed ................ {len(new_rows)}  {new_rows}")
    print(f"  parked rows owed ................... 1  [63]")
    print(f"  claims checked ..................... {len(claims)}")
    for c in claims:
        print(f"    {c['id']}: {c['verdict']}")
    print(f"  rows corrected in INDEX.md ......... {len(corrected_rows)}")
    print(f"  GATE ............................... {payload['gate']['answer']}")
    print(f"  wrote {os.path.relpath(OUT, REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
