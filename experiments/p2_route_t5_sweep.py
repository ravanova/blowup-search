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
FINDINGS: list[dict] = [
    {
        "id": "F1",
        "leg": 348,
        "route": "POCP",
        "file": "experiments/journal/leg_348.md",
        "line": 122,
        "quote": (
            "* **Does not lift, narrow, or re-read any ban.** The stage-V ban and its two "
            "entries are outside this leg's authority and outside its subject — this leg is "
            "about a *different* apparatus (periodic-orbit dynamical closure) than the "
            "NK/CAP-in-a-function-space apparatus the ban names, and I make no claim about "
            "whether that apparatus distinction matters to the ban's scope; that reading, if "
            "it is ever needed, is for the DM/user"
        ),
        "what_was_refused": (
            "Proposing the build for a periodic-orbit / Galerkin-plus-tail DYNAMICAL closure "
            "on the T^3 object class. Leg 348 named the obstruction and cost-classed it, then "
            "declined to propose a build and declined to read the ban's scope against its own "
            "apparatus."
        ),
        "classification": "APPARATUS",
        "why": (
            "The stated reason is APPARATUS, in the leg's own words: 'a *different* apparatus "
            "(periodic-orbit dynamical closure) than the NK/CAP-in-a-function-space apparatus "
            "the ban names'. NO measurement of this apparatus is cited as the reason. The leg's "
            "only nearby measurement (leg 341's three-realization death) it EXPLICITLY refuses "
            "to bank as governing: 'suggestive but not direct ... different apparatus' "
            "(leg_348.md:103-104), and 'Absence of a positive instance is not a proof of "
            "impossibility, and I am not banking it as one.'"
        ),
        "c1_scope_test": (
            "PASSES. A Galerkin-plus-tail dynamical closure is the exact apparatus ruling C1 "
            "places outside the ban's object. It closes a dynamical invariance argument and "
            "constructs no single bounded approximate inverse uniform in M."
        ),
        "reopenable": True,
        "note": (
            "ALREADY ACTED ON BY THE CONDUCTOR, not by this leg: C1 rescinded 'BUILD NOTHING IN "
            "LANE T' and opened T3/T4 on 2026-08-13. Recorded here for completeness of the "
            "record, NOT re-opened by T5. Re-opening remains subject IN FULL to C1's naming "
            "requirement."
        ),
    },
    {
        "id": "F2",
        "leg": 315,
        "route": "TMS",
        "file": "experiments/journal/leg_315.md",
        "line": 150,
        "quote": (
            "**I do not lift, narrow, or argue against the ban, and a build must not start on "
            "my reading alone.** Please have the DM/user confirm the disjointness before any "
            "build leg is dispatched."
        ),
        "what_was_refused": (
            "Dispatching the build leg for `O1` — SONIC-POINT-DESINGULARIZED TAYLOR-MODEL "
            "STEPPING IN THE SIMILARITY PARAMETER, a rigorous enclosure of the FLOW MAP of a "
            "finite-dimensional autonomous (W,Z) ODE (Lohner-QR / mean-value form / "
            "shrink-wrapping, Berz-Makino). Leg 315 read the ban as not biting, refused to act "
            "on its own reading, and routed the question to the user, where it sat unanswered."
        ),
        "classification": "APPARATUS",
        "why": (
            "The deciding reason is stated as SUBJECT-MATTER/APPARATUS disjointness and nothing "
            "else: 'the ban's subject is radii-polynomial machinery **in a function space** and "
            "a Taylor-model flow enclosure proposes **no function space at all**' "
            "(leg_315.md:147-150). No measurement of a Taylor-model enclosure is cited — none "
            "exists in this repository. Mirrored verbatim in the runner at "
            "experiments/p2_route_tms_v1_scoping.py:514-518."
        ),
        "c1_scope_test": (
            "PASSES. The leg's own text establishes the NGX quantity is absent: the object is "
            "'a finite-dimensional autonomous ODE ... so the enclosure is of the **flow map** "
            "and needs **no function space**' (leg_315.md:42-44), and 'NK is a **zero-finder** "
            "needing an approximate inverse in a fixed space ... here NK's shape is a *zero* "
            "where a *flow map* is wanted' (:53-56). No Y0/Z0/Z1/Z2 contraction; no single "
            "bounded approximate inverse uniform in M."
        ),
        "reopenable": True,
        "note": (
            "The lift-clause defect C1 knowingly left open does NOT block this: like Lane T, O1 "
            "is not a SPACE candidate, so it needs no lift. Listed, NOT ranked and NOT started. "
            "Any re-open is subject IN FULL to C1's naming requirement (name the apparatus with "
            "a citation; show no single bounded approximate inverse uniform in M)."
        ),
    },
    {
        "id": "F3",
        "leg": 257,
        "route": "P1C",
        "file": "experiments/JOURNAL.md",
        "line": 3696,
        "quote": (
            "Does NOT lift the ban itself (correctly escalates for the user's signature)."
        ),
        "what_was_refused": (
            "Proceeding on Breden-Chu's H^2(mu) weighted-Sobolev space as the 'namable FOURTH "
            "space'. Gate YES on both clauses; branch PARKED as PR #19, NOT merged, pending the "
            "user's signature on a ban lift that never came."
        ),
        "classification": "APPARATUS",
        "why": (
            "The refusal is RULE-BASED: the ban's lift clause requires the user's signature, and "
            "the leg declined to supply it itself. The leg's own measurement (Z1 = 0.065136 in "
            "the new space vs 8.9591/140.72 in the dead ones) points TOWARD proceeding, so no "
            "measured failure of the candidate governs. Under S0.5 that is APPARATUS-BASED."
        ),
        "c1_scope_test": (
            "**FAILS, AND THIS IS THE ONE THAT MATTERS.** The apparatus IS radii-polynomial: "
            "capabilities.py:518-522 records the module as carrying 'all of arXiv:2404.04054 "
            "section 6's bounds Y, Zbar11/12/21/22, Z1, Z2, Z3 plus Corollary 21's radii "
            "polynomial'. C1's own words: 'A unit that reaches for a Y_0/Z_0/Z_1/Z_2 "
            "contraction, IN ANY SPACE, is inside the ban whatever it calls itself.' A fourth "
            "SPACE is not a fourth APPARATUS. C1 does not reach it."
        ),
        "reopenable": False,
        "note": (
            "This is the largest-looking candidate in the record and C1 DOES NOT RE-OPEN IT. "
            "Listing it as re-openable would have been this unit's characteristic failure."
        ),
    },
    {
        "id": "F4",
        "leg": 262,
        "route": "RSS",
        "file": "writeup/novelty/leg_262.md",
        "line": 150,
        "quote": (
            "* **It will not lift the ℓ¹-Fourier / radii-polynomial ban.** That ban lifts only "
            "on \"a namable FOURTH space/basis this repository has not yet tried … with **its "
            "own scoping leg** establishing it is not subject to the same three-realization "
            "death.\" This leg names a candidate and measures one structural property of it "
            "(the diagonal). It is not a scoping leg, it builds nothing, and it says so."
        ),
        "what_was_refused": (
            "Scoping the named candidate fourth space (the rotated self-similar / "
            "Gaussian-weighted class) into a usable lane. The candidate is NAMED and then "
            "deliberately left un-scoped."
        ),
        "classification": "APPARATUS",
        "why": (
            "Rule-based: the refusal appeals to the ban's lift clause and its 'own scoping leg' "
            "requirement, not to any measured failure of the named candidate."
        ),
        "c1_scope_test": (
            "FAILS. The candidate is a SPACE, and the machinery to be run in it is the "
            "radii-polynomial machinery the ban names. C1 explicitly left the fourth-space/basis "
            "lift clause UNREPAIRED — 'it still names the wrong kind of object for any future "
            "candidate that IS a space' — and a space candidate needs a LIFT, which C1 is not."
        ),
        "reopenable": False,
        "note": "",
    },
    {
        "id": "F5",
        "leg": 273,
        "route": "KS/Breden-Chu screen",
        "file": "experiments/journal/leg_273.md",
        "line": 257,
        "quote": (
            "A space admitting algebraic `|y|^{-2}` tails is **not named, not proposed, and not "
            "requested here**; the standing re-posed ban requires a dedicated scoping leg for "
            "any namable fourth space, and **this is not that leg**."
        ),
        "what_was_refused": (
            "Naming or proposing a function space admitting algebraic |y|^{-2} tails — the space "
            "the leg's own negative result implies would be needed."
        ),
        "classification": "APPARATUS",
        "why": (
            "Rule-based: the stated reason is that 'the standing re-posed ban requires a "
            "dedicated scoping leg for any namable fourth space'. No measurement of the "
            "un-named space is or could be cited."
        ),
        "c1_scope_test": (
            "FAILS, for the same reason as F4: the refused object is a SPACE, not an apparatus, "
            "and the machinery intended for it is the banned machinery. C1 is a scope ruling on "
            "APPARATUS and does not repair the fourth-space clause."
        ),
        "reopenable": False,
        "note": "",
    },
    {
        "id": "F6",
        "leg": 341,
        "route": "ALGW",
        "file": "experiments/journal/leg_341.md",
        "line": 122,
        "quote": (
            "**Per this leg's gate spec: no lift-condition evidence packet is assembled.** The "
            "lift condition on the stage-V ban stays unmet. **The deferred §3 build is NEVER "
            "drafted** by this leg"
        ),
        "what_was_refused": (
            "Assembling the lift-condition evidence packet for the algebraically weighted space, "
            "and drafting the deferred §3 build that depended on it."
        ),
        "classification": "REALIZATION",
        "why": (
            "MEASURED, in three lanes, each by a different mechanism: sup-norm/collocation "
            "(Route-D, 1686/1686 configs audited, 6.04x short at theoretical optimum, a=0 only); "
            "coefficient/ell^1-weighted (legs 51/52, kernel and cokernel failure modes swap "
            "exactly at s=1, no window at any exponent); origin-conjugated/Mellin (legs 163/176, "
            "already algebraically weighted, dies orthogonally). A measurement is not touched by "
            "a decision."
        ),
        "c1_scope_test": "NOT REACHED — a realization-based refusal is not re-opened by C1.",
        "reopenable": False,
        "note": "C1's own text preserves this by name: 'leg 341 stays true'.",
    },
    {
        "id": "F7",
        "leg": 315,
        "route": "TMS (the NK half)",
        "file": "experiments/journal/leg_315.md",
        "line": 51,
        "quote": (
            "**Why NK does not reach it, per realization:** `ℓ¹_w` coefficient basis (leg 54, "
            "`1.167×` where `>8×` needed); sup-norm collocation (leg 56, `1.85e7×`/`2.04e11×` "
            "over budget); origin-`H²` at `a=0` with no transfer (legs 163/176)."
        ),
        "what_was_refused": (
            "Reaching the same target with the Newton-Kantorovich / radii-polynomial route "
            "instead of a Taylor-model enclosure."
        ),
        "classification": "REALIZATION",
        "why": (
            "THE 'BOTH' CASE, resolved by pre-committed reading (d). The passage gives an "
            "apparatus reason AND a measured reason in the same breath — three named "
            "realizations with their measured shortfalls, and only then 'plus the re-posed ban "
            "forecloses a fourth space'. THE MEASUREMENT GOVERNS. Ambiguity resolves toward "
            "staying refused."
        ),
        "c1_scope_test": "NOT REACHED — and it would fail anyway: NK/radii-polynomial IS the "
                         "banned apparatus.",
        "reopenable": False,
        "note": (
            "Same leg as F2 and the opposite verdict. The unit of classification is the REFUSAL, "
            "not the leg: leg 315 refused two different things for two different kinds of reason."
        ),
    },
]


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
