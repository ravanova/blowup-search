#!/usr/bin/env python3
"""Leg 395 / unit T5 -- THE C1 SWEEP.

Sweeps the landed record for every leg that DECLINED, DEFERRED or NARROWED work
citing the l1-Fourier / radii-polynomial ban, and classifies each refusal as
APPARATUS-BASED or REALIZATION-BASED (see experiments/journal/leg_395.md, S0.5).

This is the DISCOVERY + EVIDENCE script in one. It is gated by EXIT CODE
(lesson 68): it exits non-zero if any control fails, if the corpus enumeration
does not match its own pre-registered definition, or if any banked verbatim quote
no longer sits at the file:line it was banked at.

DIRECTION.md IS EXCLUDED BY NAME (ORCHESTRATION.md S3e). The exclusion is an
assertion here, not a promise in prose.

Usage:
    python experiments/p2_route_t5_sweep.py            # controls + verify banked findings
    python experiments/p2_route_t5_sweep.py --discover # also dump candidate windows
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "writeup" / "data" / "p2_route_t5_v1.json"

# --- S0.3 CORPUS DEFINITION ------------------------------------------------
STRATA = ("*.md", "*.py")
EXCLUDED = {
    "DIRECTION.md",                        # ORCHESTRATION.md S3e -- OUTSIDE THE READ SURFACE
    "experiments/journal/leg_395.md",       # this leg's own journal
    "experiments/p2_route_t5_sweep.py",     # this script
    "writeup/data/p2_route_t5_v1.json",     # this leg's artefact (not in strata, belt+braces)
}

# --- S0.4 THE EXACT PATTERNS (pre-registered, unedited) --------------------
BAN_TOKENS = {
    "B1": r"radii[\s\-_]?polynomial",
    "B2": r"(ℓ|ell|l)\s*[\^_]?\s*(¹|1)\s*[_-]?\s*w?\b.{0,24}"
          r"(fourier|basis|coefficient|space|norm)",
    "B3": r"ℓ¹",
    "B4": r"\bNGX\b",
    "B5": r"Y\s*[_₀]?\s*0|Z\s*[_₀₁₂]?\s*[012]\b",
    "B6": r"Newton[\s\-–]?Kantorovich",
    "B7": r"approximate inverse",
    "B8": r"collocation basis|ℓ¹_w|ell\^1_w|origin[\s\-]?H\^?²?2?\b",
}

REFUSAL_TOKENS = (
    r"banned|the ban|this ban|bans\b|forbid|prohibit|declin|defer|deferred|"
    r"narrow(ed|ing)?|refus|not permitted|may not|cannot|can't|must not|blocked|"
    r"out of scope|ruled out|excluded|abandon|did not attempt|does not attempt|"
    r"no attempt|not proposed|not pursued|drop(ped)?|stand down|stopped short|held|hold"
)

WINDOW = 6

BAN_RE = re.compile("|".join(f"(?P<{k}>{v})" for k, v in BAN_TOKENS.items()), re.I)
REF_RE = re.compile(REFUSAL_TOKENS, re.I)

# --- CONTROLS --------------------------------------------------------------
POS_A_STRING = "suggestive but not direct"
POS_A_FILE = "experiments/journal/leg_348.md"
POS_A_LINE = 103
NEG_A_STRING = "ZQXJVBRAN"

PLANTED = (
    "line one, nothing here\n"
    "we DECLINE to build the enclosure because the radii-polynomial machinery is banned\n"
    "line three, nothing here\n"
)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(REPO), *args], capture_output=True, text=True, check=True
    ).stdout


def enumerate_corpus() -> list[str]:
    paths: list[str] = []
    for pat in STRATA:
        paths.extend(p for p in git("ls-files", pat).splitlines() if p)
    return sorted(p for p in set(paths) if p not in EXCLUDED)


def read_lines(rel: str) -> list[str] | None:
    fp = REPO / rel
    try:
        return fp.read_text(encoding="utf-8", errors="strict").splitlines()
    except (UnicodeDecodeError, OSError):
        return None


def scan(lines: list[str]) -> list[dict]:
    """Stage 1 (ban token) + stage 2 (refusal token within +-WINDOW lines)."""
    ban_hits = []
    for i, ln in enumerate(lines):
        m = BAN_RE.search(ln)
        if m:
            ban_hits.append((i, m.lastgroup))
    out = []
    for i, tok in ban_hits:
        lo, hi = max(0, i - WINDOW), min(len(lines), i + WINDOW + 1)
        ref = None
        for j in range(lo, hi):
            r = REF_RE.search(lines[j])
            if r:
                ref = (j, r.group(0))
                break
        if ref is not None:
            out.append(
                {"line": i + 1, "ban_token": tok, "ban_text": lines[i].strip()[:400],
                 "refusal_line": ref[0] + 1, "refusal_word": ref[1]}
            )
    return out


# --- S0.5 THE BANKED FINDINGS ---------------------------------------------
# Filled in AFTER the hand-read of every candidate window. Each entry carries the
# DECIDING SENTENCE VERBATIM and its file:line, and this script re-verifies that
# the quote is still exactly there. A drifted quote is a FAILURE, not a warning.
FINDINGS: list[dict] = json.loads(
    (Path(__file__).resolve().parent / "p2_route_t5_findings.json").read_text()
) if (Path(__file__).resolve().parent / "p2_route_t5_findings.json").exists() else []


def main() -> int:
    fail: list[str] = []
    corpus = enumerate_corpus()

    # --- NEGATIVE CONTROL N-B: structural / S3e compliance -----------------
    if "DIRECTION.md" in corpus:
        fail.append("N-B: DIRECTION.md is in the corpus -- S3e VIOLATED")
    expected = set()
    for pat in STRATA:
        expected |= {p for p in git("ls-files", pat).splitlines() if p}
    expected -= EXCLUDED
    if set(corpus) != expected:
        fail.append("N-B: corpus enumeration != git ls-files minus exclusions")
    n_direction_would_have = len(scan(read_lines("DIRECTION.md") or []))

    # --- read the corpus ---------------------------------------------------
    texts: dict[str, list[str]] = {}
    unreadable = []
    n_bytes = 0
    for rel in corpus:
        lines = read_lines(rel)
        if lines is None:
            unreadable.append(rel)
            continue
        texts[rel] = lines
        n_bytes += (REPO / rel).stat().st_size

    # --- POSITIVE CONTROL P-A ---------------------------------------------
    pa_hits = [
        (rel, i + 1)
        for rel, lines in texts.items()
        for i, ln in enumerate(lines)
        if POS_A_STRING in ln
    ]
    if (POS_A_FILE, POS_A_LINE) not in pa_hits:
        fail.append(
            f"P-A: {POS_A_STRING!r} NOT found at {POS_A_FILE}:{POS_A_LINE} "
            f"-- the sweep's own read path is broken; every zero would be fabricated. "
            f"found={pa_hits}"
        )

    # --- POSITIVE CONTROL P-B: planted, end-to-end -------------------------
    with tempfile.TemporaryDirectory() as td:
        pf = Path(td) / "planted.md"
        pf.write_text(PLANTED, encoding="utf-8")
        pb = scan(pf.read_text(encoding="utf-8").splitlines())
    if len(pb) != 1 or pb[0]["line"] != 2:
        fail.append(f"P-B: planted refusal not recovered by scan(); got {pb}")

    # --- NEGATIVE CONTROL N-A ---------------------------------------------
    na_hits = [
        (rel, i + 1)
        for rel, lines in texts.items()
        for i, ln in enumerate(lines)
        if NEG_A_STRING in ln
    ]
    if na_hits:
        fail.append(f"N-A: nonsense token found -- {na_hits}")

    # --- THE SWEEP ---------------------------------------------------------
    windows: dict[str, list[dict]] = {}
    n_ban_lines = 0
    for rel, lines in texts.items():
        w = scan(lines)
        n_ban_lines += sum(1 for ln in lines if BAN_RE.search(ln))
        if w:
            windows[rel] = w

    # --- VERIFY THE BANKED FINDINGS ---------------------------------------
    for f in FINDINGS:
        rel, line, quote = f["file"], f["line"], f["quote"]
        lines = texts.get(rel)
        if lines is None:
            fail.append(f"FINDING {f['id']}: {rel} not in corpus")
            continue
        if not (1 <= line <= len(lines)):
            fail.append(f"FINDING {f['id']}: {rel}:{line} out of range")
            continue
        blob = "\n".join(lines[line - 1: line + 6])
        norm = re.sub(r"\s+", " ", blob)
        if re.sub(r"\s+", " ", quote).strip() not in norm:
            fail.append(f"FINDING {f['id']}: quote not found at {rel}:{line}")
        if f["classification"] not in ("APPARATUS", "REALIZATION"):
            fail.append(f"FINDING {f['id']}: bad classification")
        if f["classification"] == "REALIZATION" and f["reopenable"]:
            fail.append(
                f"FINDING {f['id']}: REALIZATION-based marked re-openable -- "
                "reading (b) forbids this"
            )

    result = {
        "leg": 395,
        "unit": "T5",
        "gate": (
            "Sweeping the landed record (DIRECTION.md excluded, S3e), for every leg that "
            "declined, deferred, or narrowed work citing the l1-Fourier / radii-polynomial "
            "ban: was that refusal APPARATUS-BASED or REALIZATION-BASED? Name, per leg, which "
            "refusals ruling C1 now permits re-opening -- each with the deciding sentence "
            "quoted verbatim and located by file and line. A zero is instrumented like any "
            "other zero."
        ),
        "corpus": {
            "strata": list(STRATA),
            "files_enumerated": len(corpus),
            "files_read": len(texts),
            "files_unreadable": unreadable,
            "bytes": n_bytes,
            "lines": sum(len(v) for v in texts.values()),
            "excluded_by_name": sorted(EXCLUDED),
            "DIRECTION_md_excluded": "DIRECTION.md" not in corpus,
            "DIRECTION_md_windows_forgone": n_direction_would_have,
        },
        "patterns": {"ban_tokens": BAN_TOKENS, "refusal_tokens": REFUSAL_TOKENS,
                     "window_lines": WINDOW},
        "controls": {
            "P-A": {"string": POS_A_STRING, "expected_at": f"{POS_A_FILE}:{POS_A_LINE}",
                    "found_at": [f"{a}:{b}" for a, b in pa_hits],
                    "pass": (POS_A_FILE, POS_A_LINE) in pa_hits},
            "P-B": {"planted_windows_recovered": len(pb), "pass": len(pb) == 1},
            "N-A": {"string": NEG_A_STRING, "hits": len(na_hits), "pass": not na_hits},
            "N-B": {"direction_md_in_corpus": "DIRECTION.md" in corpus,
                    "enumeration_matches": set(corpus) == expected,
                    "pass": "DIRECTION.md" not in corpus and set(corpus) == expected},
        },
        "sweep": {
            "ban_token_lines": n_ban_lines,
            "files_with_ban_token": sum(
                1 for lines in texts.values() if any(BAN_RE.search(l) for l in lines)
            ),
            "candidate_windows": sum(len(v) for v in windows.values()),
            "files_with_candidate_windows": len(windows),
        },
        "findings": FINDINGS,
        "tally": {
            "refusals": len(FINDINGS),
            "apparatus_based": sum(1 for f in FINDINGS if f["classification"] == "APPARATUS"),
            "realization_based": sum(
                1 for f in FINDINGS if f["classification"] == "REALIZATION"
            ),
            "reopenable_under_C1": sorted(
                (f["id"] for f in FINDINGS if f["reopenable"]),
            ),
        },
        "ceiling": (
            "TIER 2. This leg moved NO link of the L1->L4 chain. A list of re-openable "
            "questions is not movement toward Clay. Clay stays ~0.05%."
        ),
        "failures": fail,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"corpus: {len(corpus)} files, {n_bytes} bytes, "
          f"{result['corpus']['lines']} lines (DIRECTION.md EXCLUDED)")
    print(f"stage 1: {n_ban_lines} ban-token lines in "
          f"{result['sweep']['files_with_ban_token']} files")
    print(f"stage 2: {result['sweep']['candidate_windows']} candidate windows in "
          f"{len(windows)} files")
    for k, v in result["controls"].items():
        print(f"control {k}: {'PASS' if v['pass'] else 'FAIL'}")
    print(f"refusals banked: {len(FINDINGS)} "
          f"(APPARATUS {result['tally']['apparatus_based']} / "
          f"REALIZATION {result['tally']['realization_based']}), "
          f"re-openable {result['tally']['reopenable_under_C1']}")

    if "--discover" in sys.argv:
        for rel in sorted(windows):
            for w in windows[rel]:
                print(f"CAND {rel}:{w['line']} [{w['ban_token']}/{w['refusal_word']}] "
                      f"{w['ban_text'][:150]}")

    if fail:
        for f in fail:
            print("FAIL:", f, file=sys.stderr)
        return 1
    print("ALL CONTROLS AND ASSERTIONS PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
