"""Route-PGF v1: does `PROGRESS.md`'s ⚠ NEEDS YOU ledger say what actually happened?

Leg 149.  A DOCUMENTATION/HYGIENE audit, not a physics leg.  It imports no solver module,
computes no physics number, derives nothing, and re-opens no closed stage.  It matches items
in two Markdown ledgers, read-only, and counts them.  Nothing outside this leg's own two
output paths is written -- in particular neither ledger is edited under either branch of the
gate, because `PROGRESS.md` is orchestrator-owned and `DIRECTION.md` is the DM's.

THE GATE, verbatim:

  "Does every escalation/parked-branch/open-question item in DIRECTION.md's Status and
   'Open direction questions' sections have an accurate, current PROGRESS.md `⚠ NEEDS YOU`
   entry, and does every PROGRESS.md `⚠ NEEDS YOU` entry correspond to something actually
   live in DIRECTION.md (no stale entry left behind after a ruling lands)?"

Both directions matter and they have different remedies, which is why they are counted
separately and never summed: a MISSING entry is fixed by adding to `PROGRESS.md`; a STALE
entry is fixed by retiring something -- and, as it turns out, sometimes on the DIRECTION side
rather than the PROGRESS side.

WHY ONE SIDE IS PINNED AND THE OTHER CANNOT BE.  `DIRECTION.md` is git-tracked, so every fact
about it is read out of the git object store at a single frozen commit (PINNED_SHA) via
`git show` -- sibling legs land on `main` while this leg runs, and an audit that read the
working tree would report a window nobody can reproduce.  `PROGRESS.md` is **git-ignored and
live**: it is in no commit, at any SHA, so it CANNOT be pinned.  It is read once from the
canonical main-worktree path, and its own self-declared timestamp line is recorded verbatim
in the JSON as the closest thing it has to a version.  Every PROGRESS-side finding below is
therefore a statement about the live file at read time, not a reproducible-forever fact, and
the JSON labels it as such.

The audit has six parts.  A1+A2+A3+A4 answer the gate; A5 and A6 are wider cross-checks the
gate does not ask for.

  A1  THE DIRECTION SIDE, ENUMERATED.  Two sources, kept apart because the gate names them
      separately: (i) the numbered items of the "Open direction questions for the user"
      section, split on the numbered-list markers, and (ii) the escalation/parked-branch
      assertions in Status and Live assignments.  Source (ii) is located by ANCHOR STRINGS,
      not by line number: each anchor is searched for in the pinned text and the script
      raises if one is not found, so the evidence cannot silently drift out from under the
      curation.

  A2  THE PROGRESS SIDE, ENUMERATED.  The `⚠ NEEDS YOU` block, split on its numbered items.

  A3  THE MATCH, UNDER TWO PREDICATES (lesson 90).  STRICT: two items match iff their
      leg-number anchor sets intersect.  LOOSE: iff their content-token sets reach a Jaccard
      floor.  Where the two disagree the pair is reported BORDERLINE, never silently counted
      either way.  The loose predicate is here precisely because it CAN return a different
      answer -- and A3 reports whether it did, per item.

  A4  ACCURACY, not just presence (lesson 75: two defects in the same problem are not the
      same defect).  A matched pair can still be wrong.  Every numeric literal quoted by a
      PROGRESS item is checked against its DIRECTION counterpart, and every RESOLVED/PENDING
      status marker on both sides is extracted and compared.  A present-but-contradicted
      entry is counted as STALE, not as MATCHED.

  A5  GROUND TRUTH FROM GIT, which neither ledger is.  Every leg number either ledger calls
      live, parked, blocked or reserve is checked against the set of legs that have actually
      landed on `main` at the pin (`^Leg N:` commit subjects, N != 0).  A ledger that says a
      branch is parked when its leg landed is wrong in a way no cross-ledger match can see.

  A6  PROGRESS.md's INTERNAL self-consistency: its own Now / Landed this cycle / Landed /
      Queue sections against each other and against A5's landed set.

Deterministic on the DIRECTION side, seconds, no PDE solve, no solver import.
Writes writeup/data/p2_route_pgf_v1_ledger_audit.json.

Run: .venv/bin/python -u experiments/p2_route_pgf_v1_ledger_audit.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

PINNED_SHA = "65d6ada7a99194143a059cd631e3de5f98a7168b"

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "writeup" / "data" / "p2_route_pgf_v1_ledger_audit.json"

# Jaccard floor for the LOOSE predicate.  Chosen so it is not trivially satisfiable: the
# median pairwise Jaccard over all cross-ledger item pairs is reported in the JSON, and the
# floor sits above it.  If every pair passed, the control would be a tautology (lesson 90).
LOOSE_JACCARD_FLOOR = 0.15

STOPWORDS = set(
    """a an and are as at be been but by for from has have in is it its no not of on or that
    the this to was were will with which what would could should now still not
    md progress direction leg legs your you user own file section item items""".split()
)


# --------------------------------------------------------------------------------------
# plumbing
# --------------------------------------------------------------------------------------
def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(REPO), *args],
        check=True, capture_output=True, text=True,
    ).stdout


def pinned_direction() -> str:
    """DIRECTION.md read from the git object store at the pin -- never the working tree."""
    return git("show", f"{PINNED_SHA}:DIRECTION.md")


def progress_path() -> Path:
    """PROGRESS.md is git-ignored, so it lives only in the MAIN worktree, never in a
    per-agent worktree.  Resolve the main worktree from the common git dir."""
    common = Path(git("rev-parse", "--path-format=absolute", "--git-common-dir").strip())
    main_root = common.parent
    for cand in (REPO / "PROGRESS.md", main_root / "PROGRESS.md"):
        if cand.is_file():
            return cand
    raise SystemExit("PROGRESS.md not found in this worktree or the main worktree")


def leg_anchors(text: str) -> set[int]:
    """Leg numbers named in an item.  Both `leg 63` and `Leg 63` and `63 (M2)` forms."""
    out: set[int] = set()
    for m in re.finditer(r"\blegs?\s+(\d{1,3})(?:\s*/\s*(\d{1,3}))?", text, re.I):
        out.add(int(m.group(1)))
        if m.group(2):
            out.add(int(m.group(2)))
    for m in re.finditer(r"\b(\d{2,3})\s*\((?:[A-Z0-9]{2,6})\)", text):
        out.add(int(m.group(1)))
    return {n for n in out if 1 <= n <= 200}


def branch_anchors(text: str) -> set[str]:
    return set(re.findall(r"leg/[a-z0-9][a-z0-9-]*", text))


def tokens(text: str) -> set[str]:
    raw = re.findall(r"[a-zA-Z][a-zA-Z0-9_]{2,}", text.lower())
    return {t for t in raw if t not in STOPWORDS}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def numerics(text: str) -> set[str]:
    """Numeric literals a prose item quotes, normalised (commas stripped)."""
    out = set()
    for m in re.finditer(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?(?:[eE][-+]?\d+)?)(?![\w])", text):
        tok = m.group(1).replace(",", "")
        if tok in {"1", "2", "3", "8"}:      # bare list ordinals carry no content
            continue
        out.add(tok)
    return out


STATUS_MARKERS = (
    ("RESOLVED", re.compile(r"\bRESOLVED\b")),
    ("PENDING_RULING", re.compile(r"pending (?:your|the user'?s?) ruling", re.I)),
    ("STILL_OPEN", re.compile(r"still[- ]open|still (?:itself )?parked", re.I)),
    ("PARKED", re.compile(r"\bparked\b", re.I)),
    ("OVERTAKEN", re.compile(r"\bovertaken\b", re.I)),
    ("EXHAUSTED", re.compile(r"\bEXHAUSTED\b")),
)


def markers(text: str) -> list[str]:
    return [name for name, rx in STATUS_MARKERS if rx.search(text)]


# --------------------------------------------------------------------------------------
# A1 -- the DIRECTION side
# --------------------------------------------------------------------------------------
def section(text: str, start_pat: str, end_pat: str | None) -> tuple[str, int]:
    m = re.search(start_pat, text, re.M)
    if not m:
        raise SystemExit(f"A1: section start not found: {start_pat!r}")
    start = m.start()
    if end_pat:
        m2 = re.search(end_pat, text[m.end():], re.M)
        end = m.end() + m2.start() if m2 else len(text)
    else:
        end = len(text)
    line_no = text[:start].count("\n") + 1
    return text[start:end], line_no


def split_numbered(block: str) -> list[tuple[int, str]]:
    """Split a markdown numbered list into (ordinal, body).  Only top-level `N. ` markers
    at column 0 start an item; indented `- ` sub-bullets stay with their parent."""
    idx = [(int(m.group(1)), m.start()) for m in re.finditer(r"(?m)^(\d+)\.\s", block)]
    out = []
    for i, (n, pos) in enumerate(idx):
        end = idx[i + 1][1] if i + 1 < len(idx) else len(block)
        out.append((n, block[pos:end].strip()))
    return out


# Escalation / parked-branch assertions in Status + Live assignments.  Located by ANCHOR
# STRING, not by line number: the script raises if an anchor has drifted, so this curation
# cannot go quietly out of date.  `window` = characters of context captured around it.
STATUS_ANCHORS = [
    (
        "S-PQ-PARKED",
        "**Leg 60 (Route-PQ) answered NO — escalation #4.**",
        900,
        "Status: leg 60 (Route-PQ), escalation #4 -- asserts the branch is parked AND that "
        "it is listed in PROGRESS.md's escalations for the user.",
    ),
    (
        "S-PARKED-PAIR",
        "Parked escalations, untouchable by any leg:",
        200,
        "Live assignments: the authoritative list of parked escalations binding every leg.",
    ),
    (
        "S-BX-EXHAUSTED",
        "leg 126 (BX) has landed, gate NO, and the committed sequence is",
        1400,
        "Status: stage B exhausted, escalation #1 for the user, written up in PROGRESS.md's "
        "NEEDS YOU alongside the M2 escalation and the exit-criterion question.",
    ),
    (
        "S-OQ-CLAIM",
        "These also appear under `⚠ NEEDS YOU` in `PROGRESS.md`.",
        120,
        "The file's own bidirectional invariant about the two ledgers -- the sentence this "
        "leg's gate is, in effect, a test of.  NOT itself an escalation item: it is excluded "
        "from the unmatched count, because a meta-sentence has no PROGRESS counterpart to "
        "be missing.",
    ),
]

# Status anchors that are genuine escalation/parked items and SHOULD have a PROGRESS
# counterpart.  The meta-invariant sentence is not one, and counting it as a missing entry
# would inflate the finding.
STATUS_ITEMS_EXPECTING_A_PROGRESS_ENTRY = {"S-PQ-PARKED", "S-PARKED-PAIR", "S-BX-EXHAUSTED"}


def direction_side(dtext: str) -> dict:
    oq_block, oq_line = section(
        dtext,
        r"^## Open direction questions for the user\s*$",
        r"^\*\*Unofficial sketch",
    )
    oq_items = []
    for n, body in split_numbered(oq_block):
        oq_items.append(
            {
                "id": f"D-OQ{n}",
                "source": "Open direction questions",
                "ordinal": n,
                "headline": " ".join(body.split())[:180],
                "leg_anchors": sorted(leg_anchors(body)),
                "branch_anchors": sorted(branch_anchors(body)),
                "status_markers": markers(body),
                "numerics": sorted(numerics(body)),
                "chars": len(body),
                "_tokens": tokens(body),
            }
        )

    st_items = []
    for key, anchor, window, why in STATUS_ANCHORS:
        pos = dtext.find(anchor)
        if pos < 0:
            raise SystemExit(f"A1: status anchor drifted, not found at pin: {anchor!r}")
        if dtext.find(anchor, pos + 1) >= 0:
            raise SystemExit(f"A1: status anchor is not unique at pin: {anchor!r}")
        body = dtext[pos: pos + window]
        st_items.append(
            {
                "id": key,
                "source": "Status / Live assignments",
                "line": dtext[:pos].count("\n") + 1,
                "anchor": anchor,
                "why_enumerated": why,
                "headline": " ".join(body.split())[:180],
                "leg_anchors": sorted(leg_anchors(body)),
                "branch_anchors": sorted(branch_anchors(body)),
                "status_markers": markers(body),
                "numerics": sorted(numerics(body)),
                "_tokens": tokens(body),
            }
        )

    return {
        "open_questions_section_line": oq_line,
        "open_question_items": oq_items,
        "status_items": st_items,
        "direction_total_lines": dtext.count("\n") + 1,
    }


# --------------------------------------------------------------------------------------
# A2 -- the PROGRESS side
# --------------------------------------------------------------------------------------
def progress_side(ptext: str) -> dict:
    block, line_no = section(ptext, r"^## ⚠ NEEDS YOU\s*$", r"^## ")
    items = []
    for n, body in split_numbered(block):
        items.append(
            {
                "id": f"P-{n}",
                "ordinal": n,
                "headline": " ".join(body.split())[:180],
                "leg_anchors": sorted(leg_anchors(body)),
                "branch_anchors": sorted(branch_anchors(body)),
                "status_markers": markers(body),
                "numerics": sorted(numerics(body)),
                "chars": len(body),
                "_tokens": tokens(body),
            }
        )
    ts = re.search(r"^- Timestamp:\s*(.+)$", ptext, re.M)
    return {
        "needs_you_section_line": line_no,
        "items": items,
        "progress_total_lines": ptext.count("\n") + 1,
        "self_declared_timestamp": ts.group(1).strip() if ts else None,
    }


# --------------------------------------------------------------------------------------
# A3 -- the match, under two predicates
# --------------------------------------------------------------------------------------
def match(pside: dict, dside: dict) -> dict:
    dall = dside["open_question_items"] + dside["status_items"]
    pairs, jacs = [], []
    for p in pside["items"]:
        for d in dall:
            strict = bool(set(p["leg_anchors"]) & set(d["leg_anchors"]))
            j = jaccard(p["_tokens"], d["_tokens"])
            jacs.append(j)
            loose = j >= LOOSE_JACCARD_FLOOR
            if strict or loose:
                pairs.append(
                    {
                        "progress_item": p["id"],
                        "direction_item": d["id"],
                        "direction_source": d["source"],
                        "strict": strict,
                        "loose": loose,
                        "jaccard": round(j, 4),
                        "shared_leg_anchors": sorted(
                            set(p["leg_anchors"]) & set(d["leg_anchors"])
                        ),
                        "verdict": "MATCHED" if strict and loose
                        else "BORDERLINE(strict-only)" if strict
                        else "BORDERLINE(loose-only)",
                    }
                )
    jacs_sorted = sorted(jacs)
    median = jacs_sorted[len(jacs_sorted) // 2] if jacs_sorted else 0.0

    matched_p = {x["progress_item"] for x in pairs}
    matched_d = {x["direction_item"] for x in pairs}
    return {
        "loose_jaccard_floor": LOOSE_JACCARD_FLOOR,
        "median_pairwise_jaccard": round(median, 4),
        "max_pairwise_jaccard": round(max(jacs), 4) if jacs else 0.0,
        "n_cross_pairs_evaluated": len(jacs),
        "pairs": pairs,
        "progress_items_unmatched": [
            p["id"] for p in pside["items"] if p["id"] not in matched_p
        ],
        "direction_oq_items_unmatched": [
            d["id"] for d in dside["open_question_items"] if d["id"] not in matched_d
        ],
        "direction_status_items_unmatched": [
            d["id"] for d in dside["status_items"]
            if d["id"] not in matched_d
            and d["id"] in STATUS_ITEMS_EXPECTING_A_PROGRESS_ENTRY
        ],
        "direction_status_items_excluded_as_meta": [
            d["id"] for d in dside["status_items"]
            if d["id"] not in STATUS_ITEMS_EXPECTING_A_PROGRESS_ENTRY
        ],
        "control_can_disagree": any(x["strict"] != x["loose"] for x in pairs),
        # A shared leg number alone is weak evidence (nearly every item names leg 63), so
        # the load-bearing relation is MATCHED = strict AND loose.  These are the counts the
        # prose quotes.
        "matched_pairs_only": [
            {"pair": f'{x["progress_item"]}~{x["direction_item"]}', "jaccard": x["jaccard"]}
            for x in pairs if x["verdict"] == "MATCHED"
        ],
        "progress_items_with_a_matched_counterpart": sorted(
            {x["progress_item"] for x in pairs if x["verdict"] == "MATCHED"}
        ),
        "direction_oq_items_with_no_matched_counterpart": sorted(
            d["id"] for d in dside["open_question_items"]
            if d["id"] not in {x["direction_item"] for x in pairs if x["verdict"] == "MATCHED"}
        ),
        "progress_items_matched_to_status_not_to_an_open_question": sorted(
            x["progress_item"] for x in pairs
            if x["verdict"] == "MATCHED" and x["direction_source"] == "Status / Live assignments"
        ),
    }


# --------------------------------------------------------------------------------------
# A5 -- ground truth from git
# --------------------------------------------------------------------------------------
def landed_legs() -> set[int]:
    out = git("log", "--format=%s", PINNED_SHA)
    legs = set()
    for line in out.splitlines():
        m = re.match(r"^Leg (\d+):", line)
        if m and int(m.group(1)) != 0:
            legs.add(int(m.group(1)))
    return legs


# --------------------------------------------------------------------------------------
# A6 -- PROGRESS.md internal self-consistency
# --------------------------------------------------------------------------------------
def progress_internal(ptext: str, landed: set[int]) -> dict:
    def legs_after(label: str) -> list[int]:
        m = re.search(label, ptext, re.M)
        if not m:
            return []
        # The bullet wraps over several physical lines, so a fixed character window is used
        # -- but it must be CUT at the end of the leg list, or the next sentence's "reserve
        # is down to 129 (SUR,..." leaks in and is miscounted as a live leg.  The list ends
        # at the first "). " (a route tag closing a sentence); every in-list separator is
        # "), " instead.
        tail = ptext[m.start(): m.start() + 400]
        cut = tail.find("). ")
        if cut >= 0:
            tail = tail[: cut + 1]
        # NB the route tag is often followed by a comma and prose -- "130 (HPR, YES)" -- so
        # the closing paren cannot be part of the pattern, or the entry is silently dropped.
        return sorted({int(x) for x in re.findall(r"\b(\d{2,3})\s*\([A-Z0-9]{2,6}[,)]", tail)})

    live = legs_after(r"^- Ten-leg contract\. Live this cycle:")
    landed_cycle = legs_after(r"^- Landed this cycle:")
    landed_detail = sorted(
        {int(m.group(1)) for m in re.finditer(r"^- (\d{2,3}) \([A-Z0-9]{2,5}\):", ptext, re.M)}
    )
    queue_m = re.search(r"^Reserve remaining.*$", ptext, re.M)
    queue_line = queue_m.group(0) if queue_m else ""
    reserve = sorted({int(x) for x in re.findall(r"\b(\d{2,3})\s*\([A-Z0-9]{2,6}[,)]", queue_line)})

    # Markdown hard-wraps mid-sentence, so this claim must be searched in whitespace-
    # normalised text -- "nine other exploration\n   legs" does not match the literal phrase.
    flat = " ".join(ptext.split())
    nine = re.search(r"nine other exploration legs", flat) is not None

    return {
        "live_this_cycle_declared": live,
        "live_this_cycle_count": len(live),
        "live_but_already_landed_on_main": sorted(set(live) & landed),
        "live_and_genuinely_unlanded": sorted(set(live) - landed),
        "landed_this_cycle_declared": landed_cycle,
        "landed_detail_section": landed_detail,
        "declared_landed_missing_from_detail": sorted(set(landed_cycle) - set(landed_detail)),
        "reserve_declared": reserve,
        "reserve_blocker_legs_already_landed": sorted(set(reserve) & landed) if reserve else [],
        "reserve_blocked_on_133_but_133_landed": 133 in landed,
        "landed_on_main_but_absent_from_progress_entirely": sorted(
            n for n in landed
            if n >= 126 and n not in set(live) | set(landed_cycle) | set(landed_detail)
        ),
        "text_claims_nine_other_exploration_legs": nine,
        "nine_vs_declared_live_count_delta": (9 - len(live)) if nine else None,
    }


# --------------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------------
def main() -> int:
    dtext = pinned_direction()
    ppath = progress_path()
    ptext = ppath.read_text(encoding="utf-8")

    dside = direction_side(dtext)
    pside = progress_side(ptext)
    landed = landed_legs()
    m = match(pside, dside)
    internal = progress_internal(ptext, landed)

    # --- A4/A5: parked branches, checked against GIT, not against the other ledger -------
    # The branch -> owning-leg mapping is COMPUTED from DIRECTION.md's own authoritative
    # sentence ("Parked escalations, untouchable by any leg: leg 63/M2 (`leg/m2-v1`) and
    # leg 60/PQ (`leg/pq-v1`)"), not hardcoded here -- lesson: a growth rate you cite must
    # be measured on the object you actually built.
    owner = {
        m.group(2): int(m.group(1))
        for m in re.finditer(r"leg (\d{1,3})/[A-Za-z0-9]+ \(`(leg/[a-z0-9-]+)`\)", dtext)
    }
    if not owner:
        raise SystemExit("A5: parked-branch -> leg mapping could not be parsed at the pin")

    pbs, seen = [], set()
    for d in dside["status_items"]:
        for br in sorted(d["branch_anchors"]):
            k = (d["id"], br)
            if k in seen:
                continue
            seen.add(k)
            owning = owner.get(br)
            pbs.append(
                {
                    "direction_item": d["id"],
                    "branch": br,
                    "declared_by_direction": "parked / not merged / untouchable by any leg",
                    "owning_leg_per_direction": owning,
                    "owning_leg_landed_on_main_at_pin": (owning in landed) if owning else None,
                    "verdict": (
                        "STALE — the branch's own leg has landed on main"
                        if owning in landed
                        else "CURRENT — leg has not landed"
                    ),
                    "legs_named_in_item": sorted(d["leg_anchors"]),
                }
            )

    # numeric agreement on the one pair that quotes numbers on both sides
    numeric_checks = []
    dall = {d["id"]: d for d in dside["open_question_items"] + dside["status_items"]}
    for pair in m["pairs"]:
        p = next(x for x in pside["items"] if x["id"] == pair["progress_item"])
        d = dall[pair["direction_item"]]
        shared = sorted(set(p["numerics"]) & set(d["numerics"]))
        only_p = sorted(set(p["numerics"]) - set(d["numerics"]))
        numeric_checks.append(
            {
                "pair": f'{pair["progress_item"]}~{pair["direction_item"]}',
                "numerics_agreeing": shared,
                "n_agreeing": len(shared),
                "progress_only_numerics": only_p,
                "progress_status_markers": p["status_markers"],
                "direction_status_markers": d["status_markers"],
                "status_markers_conflict": bool(
                    ("RESOLVED" in d["status_markers"] and "PENDING_RULING" in p["status_markers"])
                    or ("RESOLVED" in p["status_markers"] and "PENDING_RULING" in d["status_markers"])
                ),
            }
        )

    for it in pside["items"]:
        it.pop("_tokens", None)
    for it in dside["open_question_items"] + dside["status_items"]:
        it.pop("_tokens", None)

    # A conflict only counts against the gate on a MATCHED pair; on a BORDERLINE pair it is
    # recorded as PROPAGATED (the stale wording quoted by a neighbouring item), which is a
    # blast-radius measurement, not a second independent defect (lesson 75).
    verdict_of = {f'{x["progress_item"]}~{x["direction_item"]}': x["verdict"] for x in m["pairs"]}
    stale = [
        c for c in numeric_checks
        if c["status_markers_conflict"] and verdict_of.get(c["pair"]) == "MATCHED"
    ]
    propagated = [
        c for c in numeric_checks
        if c["status_markers_conflict"] and verdict_of.get(c["pair"]) != "MATCHED"
    ]
    direction_side_stale = [r for r in pbs if r["owning_leg_landed_on_main_at_pin"] is True]

    gate_yes = (
        not m["progress_items_unmatched"]
        and not m["direction_oq_items_unmatched"]
        and not m["direction_status_items_unmatched"]
        and not stale
        and not direction_side_stale
    )

    result = {
        "leg": 149,
        "route": "ROUTE-PGF",
        "kind": "documentation/hygiene audit -- no solver module, no physics number",
        "pinned_sha": PINNED_SHA,
        "pin_scope": "DIRECTION.md only; PROGRESS.md is git-ignored and CANNOT be pinned",
        "progress_path_read": str(ppath),
        "progress_self_declared_timestamp": pside["self_declared_timestamp"],
        "gate_verbatim": (
            "Does every escalation/parked-branch/open-question item in DIRECTION.md's Status "
            "and 'Open direction questions' sections have an accurate, current PROGRESS.md "
            "⚠ NEEDS YOU entry, and does every PROGRESS.md ⚠ NEEDS YOU entry "
            "correspond to something actually live in DIRECTION.md (no stale entry left "
            "behind after a ruling lands)?"
        ),
        "A1_direction_side": dside,
        "A2_progress_side": pside,
        "A3_match": m,
        "A4_accuracy": {
            "numeric_and_marker_checks": numeric_checks,
            "n_matched_pairs_with_status_marker_conflict": len(stale),
            "matched_pairs_in_conflict": [c["pair"] for c in stale],
            "n_borderline_pairs_propagating_the_same_conflict": len(propagated),
            "borderline_pairs_propagating": [c["pair"] for c in propagated],
        },
        "A5_ground_truth": {
            "n_legs_landed_on_main_at_pin": len(landed),
            "max_leg_landed": max(landed),
            "parked_branch_assertions": pbs,
            "n_direction_side_stale_parked_assertions": len(direction_side_stale),
        },
        "A6_progress_internal": internal,
        "gate_answer": "YES" if gate_yes else "NO",
        "counts_headline": {
            "progress_needs_you_items": len(pside["items"]),
            "direction_open_questions": len(dside["open_question_items"]),
            "direction_status_items_enumerated": len(dside["status_items"]),
            "progress_items_unmatched": len(m["progress_items_unmatched"]),
            "direction_oq_items_unmatched": len(m["direction_oq_items_unmatched"]),
            "direction_status_items_unmatched": len(m["direction_status_items_unmatched"]),
            "matched_pairs_with_contradicting_status_markers": len(stale),
            "direction_side_stale_parked_branch_assertions": len(direction_side_stale),
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    ch = result["counts_headline"]
    print(f"Route-PGF v1 -- ledger audit at pin {PINNED_SHA[:7]}")
    print(f"  PROGRESS.md read from : {ppath}")
    print(f"  PROGRESS timestamp    : {pside['self_declared_timestamp']}")
    print(f"  PROGRESS NEEDS YOU    : {ch['progress_needs_you_items']} items")
    print(f"  DIRECTION open Qs     : {ch['direction_open_questions']} items")
    print(f"  DIRECTION status items: {ch['direction_status_items_enumerated']} enumerated")
    print(f"  loose control disagreed anywhere: {m['control_can_disagree']} "
          f"(median pairwise Jaccard {m['median_pairwise_jaccard']}, floor {LOOSE_JACCARD_FLOOR})")
    print(f"  unmatched PROGRESS items       : {m['progress_items_unmatched']}")
    print(f"  unmatched DIRECTION open Qs    : {m['direction_oq_items_unmatched']}")
    print(f"  unmatched DIRECTION status     : {m['direction_status_items_unmatched']}")
    print(f"  status-marker conflicts        : {ch['matched_pairs_with_contradicting_status_markers']}")
    print(f"  DIRECTION-side stale parked    : {ch['direction_side_stale_parked_branch_assertions']}")
    print(f"  PROGRESS 'live' legs already landed: {internal['live_but_already_landed_on_main']}")
    print(f"  PROGRESS genuinely-live legs      : {internal['live_and_genuinely_unlanded']}")
    print(f"  landed on main, absent from PROGRESS entirely: "
          f"{internal['landed_on_main_but_absent_from_progress_entirely']}")
    print(f"  GATE: {result['gate_answer']}")
    print(f"  wrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
