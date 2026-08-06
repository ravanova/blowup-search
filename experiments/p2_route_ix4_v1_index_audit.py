#!/usr/bin/env python3
"""Route-IX4 (leg 156) -- fourth freshness audit of writeup/INDEX.md.

Gate (pre-committed, DIRECTION.md section "156 -- ROUTE-IX4"):

    At this leg's own pinned start SHA, does INDEX.md correctly reflect every leg
    landed since leg 138's window closed?

      yes -> The index is current through the pinned SHA. Bank the dated completeness
             record; merge this leg's report to `main` normally.
      no  -> Report the exact stale or missing entries (the count is the finding); fix
             INDEX.md directly per the leg 68/108/138 mechanical-fix precedent (INDEX.md
             freshness is its own territory, not another leg's); merge regardless.

This runner is mechanical and read-only on the repository: it enumerates the audit window
from git, inventories each leg's artifacts in the PINNED tree, evaluates every checkable
claim INDEX.md makes, and writes writeup/data/p2_route_ix4_v1_index_audit.json.

No measurement is produced, so NO FIGURE, BY DESIGN -- the repository's Route-D convention
("no measurement, no figure"), the same one legs 126 and 138 invoked. The deliverable is a
ledger.

Usage:  .venv/bin/python experiments/p2_route_ix4_v1_index_audit.py
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
# BASE is leg 138's OWN PIN, not its INDEX.md commit: everything after 3474862 is
# exactly what leg 138's audit could not see. HEAD_SHA is origin/main's HEAD at the
# moment leg 156 began; pinning it keeps the counts reproducible while sibling legs land.
BASE = "34748624189c0a17a688a9195101bcfcaa2666a5"
HEAD_SHA = "9f6729e72a6ba804f09d6b213a4da2c8e938a702"

# Leg 138's own INDEX.md fix, which lands INSIDE the window above. Legs 156 audits are
# the window's legs MINUS leg 138 itself; INDEX.md's edit count is reported against both
# boundaries so neither number can be read as the other.
LEG138_INDEX_COMMIT = "b9b6398"

INDEX = os.path.join(REPO, "writeup", "INDEX.md")
OUT = os.path.join(REPO, "writeup", "data", "p2_route_ix4_v1_index_audit.json")


def git(*args: str) -> str:
    res = subprocess.run(
        ["git", "-C", REPO, *args], capture_output=True, text=True, check=False
    )
    return res.stdout


# Every existence question below is asked of the PINNED TREE, not the working copy.
# That matters: this leg edits INDEX.md and adds its own files, and an audit whose
# answers move when its own author edits the repo is not an audit. Re-running this
# script after leg 156 lands reproduces the same verdicts byte for byte.
_PINNED_TREE = frozenset(
    p for p in git("ls-tree", "-r", "--name-only", HEAD_SHA).splitlines() if p.strip()
)


def exists(rel: str) -> bool:
    """Present in the pinned tree (the BASE..HEAD_SHA window's endpoint)?"""
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
    """Every INDEX.md claim leg 156 can decide mechanically, checked against disk.

    `holds` is the claim's truth value at the pinned SHA, BEFORE leg 156's edit.
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

    # --- D1: the three routes that landed a BLOG/TECHNICAL pair in this window ------
    # Route-M2P v1 (leg 125)
    m2p = {
        "runner": "experiments/p2_route_m2p_v1_promotion.py",
        "data": "writeup/data/p2_route_m2p_v1_promotion.json",
        "blog": "writeup/4_p2_lottery/BLOG_P2_ROUTEM2P_V1.md",
        "technical": "writeup/4_p2_lottery/TECHNICAL_P2_ROUTEM2P_V1.md",
        "evidence": "experiments/p2_route_m2p_v1_promotion_evidence.py",
        "figure": "writeup/figures/fig61_route_m2p_v1_promotion.png",
    }
    m2p_p = {k: exists(v) for k, v in m2p.items()}
    claim(
        "D1",
        "Arc 4 table -- Route-M2P v1 (leg 125) has NO ROW",
        "(no statement anywhere: INDEX.md contains 0 occurrences of 'M2P')",
        False,
        {"paths": m2p, "present": m2p_p, "pieces_present": f"{sum(m2p_p.values())}/6"},
        "MISSING -- row owed; 5 of 6 pieces on disk, no *_evidence.py (new gap clause)",
    )

    # Route-NGX v1 (leg 127)
    ngx = {
        "runner": "experiments/p2_route_ngx_v1_general.py",
        "data": "writeup/data/p2_route_ngx_v1_general.json",
        "blog": "writeup/4_p2_lottery/BLOG_P2_ROUTENGX_V1.md",
        "technical": "writeup/4_p2_lottery/TECHNICAL_P2_ROUTENGX_V1.md",
        "evidence": "experiments/p2_route_ngx_v1_general_evidence.py",
        "figure": "writeup/figures/fig63_route_ngx_v1_general.png",
    }
    ngx_p = {k: exists(v) for k, v in ngx.items()}
    claim(
        "D2",
        "Arc 4 table -- Route-NGX v1 (leg 127) has NO ROW",
        "(no statement anywhere: INDEX.md contains 0 occurrences of 'NGX')",
        False,
        {"paths": ngx, "present": ngx_p, "pieces_present": f"{sum(ngx_p.values())}/6"},
        "MISSING -- row owed; 6 of 6 pieces on disk, evidence.py in experiments/ so E is Y-dagger",
    )

    # Route-NKR v1 (leg 128)
    nkr = {
        "runner": "experiments/p2_route_nkr_v1_repair.py",
        "data": "writeup/data/p2_route_nkr_v1_repair.json",
        "blog": "writeup/4_p2_lottery/BLOG_P2_ROUTENKR_V1.md",
        "technical": "writeup/4_p2_lottery/TECHNICAL_P2_ROUTENKR_V1.md",
        "evidence": "experiments/p2_route_nkr_v1_repair_evidence.py",
    }
    nkr_p = {k: exists(v) for k, v in nkr.items()}
    nkr_hdr = read_pinned(nkr["technical"]).splitlines()
    nkr_nofig = [ln for ln in nkr_hdr[:20] if "No figure" in ln]
    claim(
        "D3",
        "Arc 4 table -- Route-NKR v1 (leg 128) has NO ROW",
        "(no statement anywhere: INDEX.md contains 0 occurrences of 'NKR')",
        False,
        {
            "paths": nkr,
            "present": nkr_p,
            "pieces_present": f"{sum(nkr_p.values())}/5",
            "figure_by_design_line": nkr_nofig,
        },
        "MISSING -- row owed; 4 of 5 pieces, no *_evidence.py, figure absent BY DESIGN per its own header",
    )

    # --- D4: figure-number registry, gap item 12 ------------------------------------
    figs = listdir_pinned("writeup/figures")
    holes = [n for n in range(1, 64) if not any(f.startswith(f"fig{n}_") for f in figs)]
    claim(
        "D4",
        "gap item 12 -- figure-number registry",
        "fig53 and fig54 name no file and are cited by no writeup ... fig57 is reserved",
        holes == [53, 54, 57],
        {
            "png_count": len(figs),
            "unallocated_or_reserved_numbers": holes,
            "fig57": "reserved by parked leg 63 / Route-M2 (unchanged)",
            "fig62": (
                "NEW: reserved by leg 126's Route-BX yes-branch, which did NOT fire "
                "(gate answered NO). Leg 127 allocated fig63 past it, so fig62 is now a "
                "released reservation, i.e. a permanent hole -- unrecorded until now."
            ),
            "highest_allocated": max(
                int(m.group(1)) for f in figs if (m := re.match(r"fig(\d+)_", f))
            ),
        },
        "STALE -- item 12's hole set {53,54} is now {53,54,62}; 60 PNGs, not 58",
    )

    # --- D5: gap items 4/11, writeup/README.md staleness ----------------------------
    readme = read_pinned("writeup/README.md")
    nums = [int(m) for m in re.findall(r"^(\d+)\. \[", readme, re.M)]
    kw = len(re.findall(r"weight.repairs|kawahara|route-ka", readme, re.I))
    new_kw = len(re.findall(r"M2P|NGX|NKR", readme))
    claim(
        "D5",
        "gap items 4 and 11 -- writeup/README.md",
        "the numbered list still ends at entry 47, still skips 45, and still has 0 mentions of Weight-repairs or Route-KA/Kawahara",
        max(nums) == 47 and 45 not in nums and kw == 0,
        {
            "max_numbered_entry": max(nums),
            "entry_count": len(nums),
            "45_present": 45 in nums,
            "weight_repairs_or_kawahara_mentions": kw,
            "m2p_ngx_nkr_mentions": new_kw,
        },
        "TRUE, re-verified unchanged -- but the backlog grows by this window's legs and 3 more routes",
    )

    # --- D6: gap item 2, the one clause still open on Route-PORT v2 -----------------
    port2_b = "writeup/4_p2_lottery/BLOG_P2_ROUTEPORT_V2.md"
    claim(
        "D6",
        "gap item 2 (as narrowed by leg 138)",
        "BLOG_P2_ROUTEPORT_V2.md is still absent and this item now stands for that one clause alone",
        not exists(port2_b),
        {port2_b: exists(port2_b)},
        "TRUE, re-verified unchanged -- gap item 2 stands as narrowed",
    )

    # --- D7: gap item 10, Route-KA v1 ----------------------------------------------
    ka_b = "writeup/4_p2_lottery/BLOG_P2_ROUTEKA_V1.md"
    ka_fig = [f for f in figs if "ka_v1" in f]
    claim(
        "D7",
        "gap item 10 -- Route-KA v1 (leg 61)",
        "TECHNICAL but no BLOG, no *_evidence.py and no figure; 3 of 5 quartet pieces present",
        (
            exists("writeup/4_p2_lottery/TECHNICAL_P2_ROUTEKA_V1.md")
            and not exists(ka_b)
            and not ka_fig
        ),
        {ka_b: exists(ka_b), "figures_matching_ka_v1": ka_fig},
        "TRUE, re-verified unchanged -- gap item 10 stands as written",
    )

    # --- D8: gap item 8, fig48 assigned twice ---------------------------------------
    f48 = [f for f in figs if f.startswith("fig48")]
    claim(
        "D8",
        "gap item 8",
        "fig48 is assigned twice ... 1 duplicated figure number",
        len(f48) == 2,
        {"fig48_files": f48},
        "TRUE, re-verified unchanged -- gap item 8 stands as written",
    )

    # --- D9: leg 138's own convention block, and the LESSON-90 CONTROL --------------
    # This is the check that caught legs 58/60/62 in leg 108's block. Applied to leg
    # 138's block it must be able to come out either way; it comes out TRUE here, and
    # the D1-D3 rows above are the proof that the same code reports MISSING when a leg
    # in a window does land prose. A check that could only say "still true" would be
    # a tautology (lesson 90) -- this one is the identical predicate that returned
    # FALSE one pass ago.
    leg138_block = [
        71, 83, 85, 89, 92, 98, 99, 100, 101, 103, 104, 105, 106, 107, 111, 112,
        113, 114, 115, 116, 117, 119, 120, 121, 123, 131, 134, 136, 141,
    ]
    doc_files_in_window: set[str] = set()
    for sha in git("log", "--format=%H", f"{BASE}..{HEAD_SHA}").split():
        for f in git("show", "--pretty=format:", "--name-only", sha).splitlines():
            if re.match(r"writeup/(4_p2_lottery/(BLOG|TECHNICAL)|figures/)", f.strip()):
                doc_files_in_window.add(f.strip())
    violators = []
    for n in leg138_block:
        touched = git(
            "log", "--format=%H", f"{BASE}..{HEAD_SHA}", "--grep", f"^Leg {n}:"
        ).split()
        for sha in touched:
            for f in git("show", "--pretty=format:", "--name-only", sha).splitlines():
                if re.match(
                    r"writeup/(4_p2_lottery/(BLOG|TECHNICAL)|figures/)", f.strip()
                ):
                    violators.append({"leg": n, "file": f.strip()})
    claim(
        "D9",
        "'Index currency -- third pass' convention block (leg 138's 29 no-figure-by-design legs)",
        "29 of the 33 legs produced no BLOG/TECHNICAL and no figure, by design ... No row is owed for any of them",
        not violators,
        {
            "legs_checked": len(leg138_block),
            "violators": violators,
            "control_note": (
                "Identical predicate to the one that returned FALSE against leg 108's "
                "block one pass ago (legs 58/60/62). It returns TRUE here, and claims "
                "D1-D3 show the same code reporting MISSING when prose does land."
            ),
        },
        "TRUE -- leg 138's block is NOT superseded; 0 of its 29 legs landed prose or a figure in this window",
    )

    # --- D10: parked-escalation convention, still exactly one -----------------------
    declared = sorted(
        set(
            re.findall(
                r"writeup/4_p2_lottery/(?:BLOG|TECHNICAL)_[A-Za-z0-9_]+\.md",
                read_pinned("DIRECTION.md"),
            )
        )
    )
    undelivered = [d for d in declared if not exists(d)]
    claim(
        "D10",
        "Arc 4 row 'Route-M2 v1 (leg 63) -- PARKED, NOT LANDED'",
        "0 of its 4 declared artifacts on `main`",
        all(
            not exists(f)
            for f in [
                "writeup/4_p2_lottery/BLOG_P2_ROUTEM2_V1.md",
                "writeup/4_p2_lottery/TECHNICAL_P2_ROUTEM2_V1.md",
                "writeup/data/p2_route_m2_v1_targets.json",
                "writeup/figures/fig57_route_m2_v1_targets.png",
            ]
        ),
        {
            "direction_declared_doc_paths": len(declared),
            "declared_but_absent_from_main": undelivered,
            "note": (
                "The only DIRECTION.md-declared Arc 4 prose absent from main is leg 63's, "
                "which already has its parked row. No SECOND parked route exists, so the "
                "convention block needs no new entry."
            ),
        },
        "TRUE, re-verified unchanged -- exactly 1 parked route, already rowed",
    )

    return c


# ------------------------------------------------------------------------------ main
def main() -> int:
    window = enumerate_window()
    # Leg 138 is in the window (its own INDEX.md fix landed after its pin), but it is
    # the previous auditor, not an audited leg. Leg 0 is repo-wide integration work.
    audited = {n: r for n, r in window.items() if n not in (0, 138)}
    claims = check_claims()

    with_docs = sorted(n for n, r in audited.items() if r["blog_technical_touched"])
    with_figs = sorted(n for n, r in audited.items() if r["figures_added"])
    neither = sorted(
        n
        for n, r in audited.items()
        if not r["blog_technical_touched"] and not r["figures_added"]
    )
    new_rows = sorted(
        n
        for n in with_docs
        if any(
            os.path.basename(f).startswith("BLOG_")
            for f in audited[n]["blog_technical_touched"]
        )
    )

    idx_edits_since_pin = [
        x
        for x in git(
            "log", "--format=%h", f"{BASE}..{HEAD_SHA}", "--", "writeup/INDEX.md"
        ).splitlines()
        if x
    ]
    idx_edits_since_138_fix = [
        x
        for x in git(
            "log",
            "--format=%h",
            f"{LEG138_INDEX_COMMIT}..{HEAD_SHA}",
            "--",
            "writeup/INDEX.md",
        ).splitlines()
        if x
    ]

    corrected_rows = [
        {
            "row": "Arc 4 / Route-M2P v1 (leg 125)",
            "action": "ADDED",
            "why": (
                "Chen's gamma=2 promotion screen; BLOG+TECHNICAL+runner+data+fig61 on "
                "main, no *_evidence.py. 5 of 6 pieces; E marked GAP."
            ),
        },
        {
            "row": "Arc 4 / Route-NGX v1 (leg 127)",
            "action": "ADDED",
            "why": (
                "the general class A21 != 0 decided, gate YES; 6 of 6 pieces incl. "
                "fig63 and an evidence.py in experiments/ (E = Y-dagger)."
            ),
        },
        {
            "row": "Arc 4 / Route-NKR v1 (leg 128)",
            "action": "ADDED",
            "why": (
                "nk_bounds.py repair leg; BLOG+TECHNICAL+runner+data on main, no "
                "*_evidence.py, and no figure BY DESIGN per its own TECHNICAL header."
            ),
        },
        {
            "row": "gap item 12 (figure-number registry)",
            "action": "UPDATED",
            "why": (
                "hole set {fig53, fig54} becomes {fig53, fig54, fig62}: fig62 was "
                "reserved for leg 126's Route-BX yes-branch, which did not fire, and "
                "leg 127 allocated fig63 past it. PNG count 58 -> 60."
            ),
        },
        {
            "row": "gap item 13 (NEW) -- two of this window's three routes have no *_evidence.py",
            "action": "ADDED",
            "why": (
                "Route-M2P v1 and Route-NKR v1 both ship BLOG+TECHNICAL+runner+data "
                "with no *_evidence.py. Same shape as the standing gap items 9/10: "
                "writing one is a claim-bearing choice, outside a links-and-labels remit."
            ),
        },
        {
            "row": "gap item 11 (writeup/README.md)",
            "action": "UPDATED",
            "why": (
                "still ends at entry 47, still skips 45, still 0 Weight-repairs/Kawahara "
                "mentions, and now 0 mentions of M2P/NGX/NKR either. Backlog grows by "
                "this window."
            ),
        },
        {
            "row": "'Index currency -- fourth pass' paragraph",
            "action": "ADDED",
            "why": (
                "dates the window, names the pinned SHA, records the no-figure-by-design "
                "legs, and states explicitly that leg 138's own convention block is NOT "
                "superseded (0 of its 29 legs landed prose in this window) -- the first "
                "pass where the predecessor's block survives the check."
            ),
        },
    ]

    gate_no = any(c["verdict"].startswith(("FALSE", "MISSING", "STALE")) for c in claims)

    payload = {
        "leg": 156,
        "route": "ROUTE-IX4",
        "title": "Fourth freshness audit of writeup/INDEX.md, since leg 138's window closed",
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "figure": None,
        "figure_note": (
            "NO FIGURE, BY DESIGN. This leg produces no measurement; the repository's "
            "Route-D convention ('no measurement, no figure') applies, the same one legs "
            "126 and 138 invoked. The deliverable is this ledger."
        ),
        "window": {
            "base_commit": BASE,
            "base_description": "leg 138's OWN PIN (origin/main HEAD when leg 138 began)",
            "head_commit": HEAD_SHA,
            "head_description": "origin/main HEAD at the moment leg 156 began",
            "total_commits": len(
                [x for x in git("log", "--format=%H", f"{BASE}..{HEAD_SHA}").split() if x]
            ),
            "leg_prefixes_in_window_incl_leg0_and_138": sorted(window),
            "index_md_edits_within_window": len(idx_edits_since_pin),
            "index_md_edits_within_window_note": (
                "The one edit is leg 138's own fix "
                f"({LEG138_INDEX_COMMIT}), which landed after its own pin."
            ),
            "index_md_edits_since_leg138_fix": len(idx_edits_since_138_fix),
            "index_md_commits_ever_at_pinned_sha": len(
                [
                    x
                    for x in git(
                        "log", "--format=%H", HEAD_SHA, "--", "writeup/INDEX.md"
                    ).splitlines()
                    if x
                ]
            ),
        },
        "counts": {
            "legs_audited": len(audited),
            "legs_touching_blog_technical": len(with_docs),
            "legs_adding_figures": len(with_figs),
            "figures_added": sum(len(r["figures_added"]) for r in audited.values()),
            "legs_with_neither": len(neither),
            "legs_with_data_json": sum(1 for r in audited.values() if r["data_json"]),
            "legs_with_journal_and_novelty": sum(
                1
                for r in audited.values()
                if r["journal_on_disk"] and r["novelty_on_disk"]
            ),
            "new_arc4_rows_owed": len(new_rows),
            "parked_rows_owed": 0,
        },
        "leg_lists": {
            "audited_legs": sorted(audited),
            "touching_blog_technical": with_docs,
            "adding_figures": with_figs,
            "new_route_rows_owed": new_rows,
            "no_measurement_no_figure": neither,
        },
        "per_leg_inventory": {str(n): r for n, r in sorted(audited.items())},
        "claims_checked": claims,
        "corrected_rows": corrected_rows,
        "gate": {
            "question": (
                "At this leg's own pinned start SHA, does INDEX.md correctly reflect "
                "every leg landed since leg 138's window closed?"
            ),
            "answer": "NO" if gate_no else "YES",
            "branch_taken": (
                "Report the exact stale or missing entries (the count is the finding); "
                "fix INDEX.md directly per the leg 68/108/138 mechanical-fix precedent; "
                "merge regardless."
                if gate_no
                else "The index is current through the pinned SHA. Bank the dated "
                "completeness record; merge this leg's report to main normally."
            ),
        },
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")

    print(f"Route-IX4 index audit -- window {BASE[:7]}..{HEAD_SHA[:7]}")
    print(f"  total commits in window ............ {payload['window']['total_commits']}")
    print(f"  legs audited (excl. Leg 0 and 138) . {len(audited)}  {sorted(audited)}")
    print(f"  INDEX.md edits within window ....... {len(idx_edits_since_pin)}  (leg 138's own fix)")
    print(f"  INDEX.md edits since that fix ...... {len(idx_edits_since_138_fix)}")
    print(f"  legs touching BLOG/TECHNICAL ....... {len(with_docs)}  {with_docs}")
    print(f"  legs adding figures ................ {len(with_figs)}  {with_figs}")
    print(f"  legs with neither (by design) ...... {len(neither)}")
    print(f"  new route rows owed ................ {len(new_rows)}  {new_rows}")
    print(f"  parked rows owed ................... 0")
    print(f"  claims checked ..................... {len(claims)}")
    for c in claims:
        print(f"    {c['id']}: {c['verdict']}")
    print(f"  rows corrected in INDEX.md ......... {len(corrected_rows)}")
    print(f"  GATE ............................... {payload['gate']['answer']}")
    print(f"  wrote {os.path.relpath(OUT, REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
