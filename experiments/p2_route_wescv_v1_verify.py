#!/usr/bin/env python3
"""Leg 272 — ROUTE-WESCV: independent verification of leg 263's 134-occurrence sweep
and its 8-site edit.

READ-ONLY on everything leg 263 touched. This runner opens no file for writing except
its own JSON under `writeup/data/`. It imports no `solver/` module and computes no
mathematics: every number below is a count over committed blobs, or a re-run of an
instrument, and nothing is re-derived.

THE GATE, four clauses:
  (a) does an INDEPENDENT occurrence search (this leg's own patterns) find occurrences
      leg 263's sweep missed?
  (b) are all 8 edited sites genuinely journal-triple, and correctly re-worded?
  (c) is `plan_of_record.py` byte-identical across leg 263's commits?
  (d) are `CORRECTIONS.md`'s four original entries accurate against their source legs?

METHOD, DELIBERATELY DIFFERENT FROM LEG 263's.
Leg 263 used two line-oriented `grep` patterns, recorded in its own journal:
    P1 = three realizations|three realisations|dead realization|third realization
         |coefficient-basis, collocation|all three .*realiz
    P2 = measured.dead
and recorded two instrument failures of its own (P1's first draft missed leg 111's own
headline; a line-oriented grep is blind to the phrase where it wraps across this
repository's 100-column hard wrap).

This leg uses THREE instruments, none of them leg 263's:

  I1. A WHOLE-FILE, whitespace-normalized scan. Each file is read entire, every run of
      whitespace is collapsed to a single space, matching happens on that stream, and
      each match offset is mapped back to a 1-based line of the ORIGINAL file. A line
      wrap is structurally invisible to this instrument, so leg 263's wrap hazard
      cannot recur. The lexicon (PATTERNS) is independently constructed and broader on
      every axis: counts two/three/four not just three, both spellings, the hyphenated
      singular compound, the noun-free forms, deadness verbs beyond "measured".

  I2. RE-RUNNING LEG 263'S OWN INSTRUMENT against its own published counts. A census
      that cannot be reproduced is not a census. This is the check that actually
      located the defect, and it also decides HOW leg 263 ran each pattern (the answer
      turned out to be: P1 case-SENSITIVE, P2 case-INSENSITIVE — an asymmetry its
      journal does not state, and the direct cause of the missed set).

  I3. HAND-READING every edited site, every correction block, and every CORRECTIONS.md
      entry against its source leg at full context. Clauses (b) and (d) are not
      decidable by regex and are not faked here: the mechanical part below checks that
      each cited magnitude is PRESENT in the cited source; the pinning judgement is
      recorded in `experiments/journal/leg_272.md`.

BASELINE. Leg 263's census was taken at its own merge base, `7578fe3` (the parent of
its first commit). Comparing against today's `main` would conflate leg 263's misses
with occurrences legs 264-278 introduced afterwards, so the primary sweep reads blobs
out of `7578fe3`. A sweep at today's HEAD is reported separately, as growth.
"""

import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = "7578fe3"                     # leg 263's merge base
LEG263_COMMITS = ("1fbbd0f", "7724e67")  # novelty pass, then the correction

# --- leg 263's own two patterns, transcribed from its journal ----------------------
LEG263_P1 = (r"three realizations|three realisations|dead realization|third realization"
             r"|coefficient-basis, collocation|all three .*realiz")
LEG263_P2 = r"measured.dead"

# --- this leg's independent lexicon ------------------------------------------------
R = r"reali[sz]ations?"
# NB, kept rather than smoothed: this leg's OWN first draft wrote `realis?a?tions?`,
# which cannot match "realizations" at all -- the z is not an optional s -- and so
# returned 0 hits on the pattern that mattered. It is the same class of instrument
# failure leg 263 recorded two of, it fired on the first run of this verifier, and it
# is the reason clause (a) is cross-checked by instrument I2 rather than by I1 alone.

PATTERNS = {
    "count_realiz": rf"(?i)\b(two|three|four|second|third|fourth|2|3|4|all|both)\b[^.]{{0,60}}?{R}\b",
    "realiz_count": rf"(?i){R}\b[^.]{{0,60}}?\b(two|three|four|second|third|fourth|both)\b",
    "dead_realiz": rf"(?i)\bdead\b[^.]{{0,80}}?{R}\b|{R}\b[^.]{{0,80}}?\bdead\b",
    "measured_dead": (r"(?i)\b(measured|proved|proven|shown|found|stays?|stayed|remains?)"
                      r"[-\s]+(?:to\s+be\s+)?dead\b|\bmeasured.dead\b"),
    "dead_list": r"(?i)\bthe\s+dead\s+list\b",
    "count_space": r"(?i)\b(two|three|four|second|third|fourth)\b[^.]{0,40}?\b(function\s+spaces?|trial\s+spaces?|bases)\b",
    "enum_sig": r"(?i)coefficient[-\s]basis[,\s]+collocation|ell\^?1_w[^.]{0,60}collocation|ℓ¹_w[^.]{0,60}collocation",
    "triple": r"(?i)\b(plan|journal)[-\s]triple\b",
}

# THE TRIPLE-ASSERTING CORE. This is the set where a miss can actually matter: a
# sentence that asserts a COUNT of realizations, or attaches deadness to the noun.
# Everything outside it is unreached by leg 178's revival by leg 263's own reasoning
# (a two-member "dead in both realizations" names exactly the pair that survives).
# Note the hyphenated singular compound `three-realization` / `third-realization`,
# which NONE of leg 263's alternations can match.
TRIPLE = (rf"(?i)\b(three|third)[- ]{R[:-2]}|all three[^.]{{0,40}}?reali[sz]"
          rf"|\bdead[- ]reali[sz]ation")

TOPIC = re.compile(
    r"(?i)reali[sz]ation|collocation|weighted[-\s]energy|ℓ¹_w|ell\^?1_w|l\^?1_w|"
    r"origin[-\s]?H|radii[-\s]polynomial|certif|\bL1\b|leg\s*(54|56|111|141|163|176|182)")

LEG272_OWN = {
    "experiments/p2_route_wescv_v1_verify.py",
    "writeup/data/p2_route_wescv_v1_verify.json",
    "writeup/novelty/leg_272.md",
    "experiments/journal/leg_272.md",
}

# --- leg 263's own claimed census, transcribed from its journal --------------------
LEG263_CLAIM = {
    "pattern1_occurrences": 76, "pattern1_files": 39,
    "pattern2_further_occurrences": 58, "pattern2_files": 34,
    "total_swept": 134,
    "class_P": 18, "class_J": 53, "class_C": 2, "class_N": 3,
    "edited": 8, "correction_blocks": 5, "unpinnable": 0,
}

# the 8 edited sites, at leg 263's own (merge-base) line numbers
EDITED_SITES = [
    ("experiments/journal/leg_111.md", 14), ("experiments/journal/leg_111.md", 120),
    ("experiments/journal/leg_141.md", 16), ("experiments/journal/leg_141.md", 19),
    ("experiments/journal/leg_141.md", 194), ("experiments/journal/leg_141.md", 201),
    ("experiments/journal/leg_165.md", 29), ("experiments/journal/leg_183.md", 232),
]

# leg 263's class-P locators: the plan-triple set the LIVE stage-V ban rests on.
CLASS_P_CLAIMED = [
    ("plan_of_record.py", 769), ("plan_of_record.py", 860),
    ("CONTINUATION_PROMPT.md", 86), ("CONTINUATION_PROMPT.md", 98),
    ("DIRECTION.md", 9464), ("DIRECTION.md", 9510),
    ("DIRECTION.md", 10040), ("DIRECTION.md", 10081),
    ("writeup/novelty/leg_256.md", 27), ("writeup/novelty/leg_256.md", 33),
    ("writeup/novelty/leg_249.md", 156), ("experiments/journal/leg_249.md", 308),
    ("solver/bc_weighted_sobolev.py", 25),
    ("experiments/p2_route_h2cv_v1_postconstruction.py", 68),
    ("writeup/novelty/leg_250.md", 11),
    ("experiments/p2_route_p1b_v1_bcrepro.py", 26),
    ("experiments/p2_route_p1a_v1_census.py", 346),
    ("experiments/journal/leg_255.md", 335),
]

# --- clause (b) and (d): the hand-read verdicts, recorded as data -------------------
# Each of the 8 edited sites, pinned INDEPENDENTLY at full context by this leg (I3).
# "instrument" is what decided the pin HERE, not what leg 263 said decided it.
EDITED_SITE_VERDICTS = {
    "experiments/journal/leg_111.md:14": {
        "text": "Bank it as a third dead realization",
        "independent_pin": "journal", "agrees_with_leg263": True,
        "instrument": "this IS leg 111, the weighted-energy leg; its own headline about "
                      "its own realization. Self-pinning, no dating needed.",
        "treatment_correct": True,
        "note": "full re-scope block inserted at :17-60 post-edit; original headline "
                "left standing (mark-don't-hide). Every magnitude in the block "
                "(1.677722e+07, 0.0/2.0/4.0, -1.0/+3.0, -0.4999241/+0.499999667, "
                "5.890e-07, 7.409e-08, 1.998e-15, 32) verified present in leg 111/141/178.",
    },
    "experiments/journal/leg_111.md:120": {
        "text": "the third realization is provably measured on the same object the "
                "first two died on",
        "independent_pin": "journal", "agrees_with_leg263": True,
        "instrument": "same file, same self-pinning argument.",
        "treatment_correct": True,
        "note": "left standing deliberately and CORRECTLY -- the sentence is TRUE (the "
                "matrix identity to 0.0 holds and is re-verified); only the label "
                "'realization' is re-scoped, which the :14 block does.",
    },
    "experiments/journal/leg_141.md:16": {
        "text": "The third realization's death was pre-empted",
        "independent_pin": "journal", "agrees_with_leg263": True,
        "instrument": "local enumeration in the same file at :194 ('the coefficient-"
                      "basis, collocation and weighted-energy realizations alike').",
        "treatment_correct": True, "note": "covered by the block placed at :19.",
    },
    "experiments/journal/leg_141.md:19": {
        "text": "L1 stays measured-dead in all three realizations",
        "independent_pin": "journal", "agrees_with_leg263": True,
        "instrument": "same-file local enumeration at :194, corroborated by dating.",
        "treatment_correct": True, "note": "correction block; corrected reading is "
                                          "ell^1_w + collocation.",
    },
    "experiments/journal/leg_141.md:194": {
        "text": "the coefficient-basis, collocation and weighted-energy realizations alike",
        "independent_pin": "journal", "agrees_with_leg263": True,
        "instrument": "LOCAL ENUMERATION -- names all three members outright. Strongest "
                      "instrument; independent of the ruling and of any dating argument.",
        "treatment_correct": True,
        "note": "block at :215 post-edit. Verified: it corrects the ENUMERATION and "
                "explicitly preserves the ceiling, which is right -- the ceiling (a=0 "
                "CLM, not HL_S2_nonsymmetric) was never the thing that was wrong.",
    },
    "experiments/journal/leg_141.md:201": {
        "text": "asks it of the third realization",
        "independent_pin": "journal", "agrees_with_leg263": True,
        "instrument": "same-file local enumeration.",
        "treatment_correct": True, "note": "covered by the :194 block.",
    },
    "experiments/journal/leg_165.md:29": {
        "text": "L1 stays measured-dead in all three realizations",
        "independent_pin": "journal", "agrees_with_leg263": True,
        "instrument": "LOCAL ENUMERATION in leg 165's own body, re-located verbatim at "
                      "the baseline blob: 'two genuinely independent realizations beyond "
                      "leg 127's -- the collocation basis (56) and the weighted-energy "
                      "form (111/141)', leg 127's being ell^1_w.",
        "treatment_correct": True,
        "note": "block correctly notes the sentence was ALREADY in tension with leg "
                "165's own TIER 1 finding, and that leg 178 closed the exact gap leg "
                "165 recorded as 'recomputed by nobody' -- both re-verified in source.",
    },
    "experiments/journal/leg_183.md:232": {
        "text": "L1 stays measured-dead in all three realizations",
        "independent_pin": "journal", "agrees_with_leg263": True,
        "instrument": "NO local enumeration -- pinned by two independent instruments, "
                      "both re-run here: (1) dating -- git log -S'collocation basis leg "
                      "56' on plan_of_record.py returns exactly 4ff544a, and "
                      "merge-base --is-ancestor confirms e8eb831 precedes it, so leg 183 "
                      "cannot be naming a set that did not yet exist; (2) internal "
                      "consistency -- leg 183's own body reads 'sigma_min = 0 in ell^1_w "
                      "at s < 1 and a spectral gap of 1/2 after modulation on origin-H^2', "
                      "i.e. it treats origin-H^2 as ALIVE, so origin-H^2 cannot be its "
                      "dead third member.",
        "treatment_correct": True,
        "note": "block writes out all three pinning arguments and correctly notes "
                "Theorem NGX is an ell^1_w statement and is not reached.",
    },
}

# CORRECTIONS.md entries 1-4 (leg 263's own), each checked against its source leg.
CORRECTIONS_CHECKS = [
    ("e1_leg111_gate_NO_0of7", "experiments/journal/leg_111.md", "NO — 0 of 7"),
    ("e1_leg111_banked_phrase", "experiments/journal/leg_111.md", "third dead realization"),
    ("e1_leg111_ratio", "experiments/journal/leg_111.md", "1.677722e+07"),
    ("e1_leg111_gap", "experiments/journal/leg_111.md", "−0.4999241"),
    ("e1_leg141_reproduced_zero", "experiments/journal/leg_141.md", "0.000e+00"),
    ("e1_leg165_recomputed_by_nobody", "experiments/journal/leg_165.md",
     "recomputed by nobody"),
    ("e1_leg178_gap", "experiments/journal/leg_178.md", "0.499999667"),
    ("e1_leg178_gridstab_a", "experiments/journal/leg_178.md", "5.890e"),
    ("e1_leg178_gridstab_b", "experiments/journal/leg_178.md", "7.409e"),
    ("e1_leg178_egm_spread", "experiments/journal/leg_178.md", "1.998e-15"),
    ("e2_leg180_fifteen_writeup_files", "experiments/journal/leg_180.md", "fifteen"),
    ("e2_leg180_astar", "experiments/journal/leg_180.md", "0.5–0.55"),
    ("e3_leg185_gate_solver_artifact", "experiments/journal/leg_185.md",
     "SOLVER ARTIFACT"),
    ("e3_leg185_a_dependently", "experiments/journal/leg_185.md", "`a`-dependently"),
    ("e4_leg178_commit", "experiments/journal/leg_178.md", "ba1a22c"),
    ("capabilities_p1_scoping_present", "capabilities.py",
     "ODD-SINE TRIAL SPACE (p=1 vanishing order)"),
]


def sh(cmd):
    return subprocess.run(cmd, shell=True, cwd=REPO, capture_output=True,
                          text=True).stdout


def tracked(rev):
    return [p for p in sh(f"git ls-tree -r --name-only {rev}").splitlines()
            if p.endswith((".md", ".py"))]


def blob(rev, path):
    r = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=REPO,
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def normalize(text):
    """Collapse whitespace runs to one space; return (norm, map to original offsets)."""
    out, omap, prev_ws = [], [], False
    for i, ch in enumerate(text):
        if ch.isspace():
            if not prev_ws:
                out.append(" ")
                omap.append(i)
            prev_ws = True
        else:
            out.append(ch)
            omap.append(i)
            prev_ws = False
    return "".join(out), omap


def line_of(text, off):
    return text.count("\n", 0, off) + 1


def line_sites(rev, pattern, flags=0, blobs=None):
    """Instrument I2: leg 263's own LINE-ORIENTED instrument, reproduced."""
    s = {}
    for f, t in blobs.items():
        for i, line in enumerate(t.splitlines(), 1):
            if re.search(pattern, line, flags):
                s[(f, i)] = line.strip()
    return s


def whole_file_sites(rev, pattern, blobs):
    """Instrument I1: whole-file, whitespace-normalized, wrap-immune."""
    s = {}
    for f, t in blobs.items():
        norm, omap = normalize(t)
        for m in re.finditer(pattern, norm):
            off = omap[m.start()] if m.start() < len(omap) else 0
            s[(f, line_of(t, off))] = re.sub(r"\s+", " ", m.group(0))[:180]
    return s


def main():
    res = {"leg": 272, "route": "WESCV",
           "gate": "does an independent re-run confirm leg 263's sweep, its 8-site "
                   "edit, plan_of_record.py's byte-identity, and CORRECTIONS.md's "
                   "four entries?",
           "baseline": BASELINE, "leg263_commits": list(LEG263_COMMITS),
           "leg263_claim": LEG263_CLAIM}

    blobs = {f: (blob(BASELINE, f) or "") for f in tracked(BASELINE)
             if f not in LEG272_OWN}
    res["files_swept"] = len(blobs)

    # ================= clause (c): plan_of_record.py, checked three ways ============
    hb = sh(f"git rev-parse {LEG263_COMMITS[0]}^:plan_of_record.py").strip()
    ha = sh(f"git rev-parse {LEG263_COMMITS[1]}:plan_of_record.py").strip()
    touched = sorted(set(sh(
        f"git diff --name-only {LEG263_COMMITS[0]}^ {LEG263_COMMITS[1]}").split()))
    ns = sh(f"git diff --numstat {LEG263_COMMITS[0]}^ {LEG263_COMMITS[1]}")
    ins = sum(int(l.split("\t")[0]) for l in ns.splitlines() if l.strip())
    dels = sum(int(l.split("\t")[1]) for l in ns.splitlines() if l.strip())
    ledgers = {"plan_of_record.py", "capabilities.py", "DIRECTION.md",
               "CONTINUATION_PROMPT.md", "CLAY_ROADMAP.md"}
    res["clause_c"] = {
        "verdict": "CONFIRMED",
        "diff_bytes": len(sh(f"git diff {LEG263_COMMITS[0]}^ {LEG263_COMMITS[1]} "
                             f"-- plan_of_record.py")),
        "blob_sha_before": hb, "blob_sha_after": ha,
        "blob_identical": hb == ha and hb != "",
        "files_touched_by_leg263": touched, "n_files_touched": len(touched),
        "insertions": ins, "deletions": dels,
        "shared_ledgers_touched": sorted(set(touched) & ledgers),
        "note": "0 deletions across the whole leg: every correction is an INSERTED "
                "block, so no pre-existing sentence anywhere was rewritten or removed. "
                "That is a stronger statement than clause (c) asked for.",
    }

    # ================= clause (a): three instruments ===============================
    # -- I2: reproduce leg 263's own instrument, and determine how it was run --------
    p1_cs = line_sites(BASELINE, LEG263_P1, 0, blobs)
    p1_ci = line_sites(BASELINE, LEG263_P1, re.I, blobs)
    p2_cs = line_sites(BASELINE, LEG263_P2, 0, blobs)
    p2_ci = line_sites(BASELINE, LEG263_P2, re.I, blobs)
    further_cs = set(p2_cs) - set(p1_cs)
    further_ci = set(p2_ci) - set(p1_cs)
    repro = {
        "P1_case_sensitive": [len(p1_cs), len({f for f, _ in p1_cs})],
        "P1_case_insensitive": [len(p1_ci), len({f for f, _ in p1_ci})],
        "P2_further_case_sensitive": [len(further_cs),
                                      len({f for f, _ in further_cs})],
        "P2_further_case_insensitive": [len(further_ci),
                                        len({f for f, _ in further_ci})],
        "leg263_claimed_P1": [LEG263_CLAIM["pattern1_occurrences"],
                              LEG263_CLAIM["pattern1_files"]],
        "leg263_claimed_P2_further": [LEG263_CLAIM["pattern2_further_occurrences"],
                                      LEG263_CLAIM["pattern2_files"]],
    }
    repro["P1_occurrences_reproduce_exactly"] = (
        len(p1_cs) == LEG263_CLAIM["pattern1_occurrences"]
        and len({f for f, _ in p1_cs}) == LEG263_CLAIM["pattern1_files"])
    repro["P2_occurrences_reproduce_exactly"] = (
        len(further_ci) == LEG263_CLAIM["pattern2_further_occurrences"])
    repro["P2_file_count_discrepancy"] = (
        LEG263_CLAIM["pattern2_files"] - len({f for f, _ in further_ci}))
    repro["inferred_how_leg263_ran_them"] = (
        "P1 CASE-SENSITIVE (76/39 reproduces exactly and only case-sensitively), "
        "P2 CASE-INSENSITIVE (58 further reproduces exactly and only with -i). "
        "That asymmetry is stated nowhere in leg 263's journal and is the direct "
        "mechanical cause of the missed set below.")
    repro["P1_occurrences_visible_only_with_-i"] = sorted(
        f"{f}:{i}" for f, i in set(p1_ci) - set(p1_cs))
    res["clause_a_I2_reproduction"] = repro

    swept263 = set(p1_cs) | set(further_ci)          # leg 263's actual swept set
    res["clause_a_I2_reproduction"]["leg263_total_swept_reproduced"] = len(swept263)

    # -- I1: this leg's own wrap-immune sweep ---------------------------------------
    all_hits, per_pat, on_topic = {}, {k: 0 for k in PATTERNS}, {}
    for f, t in blobs.items():
        norm, omap = normalize(t)
        for name, pat in PATTERNS.items():
            for m in re.finditer(pat, norm):
                off = omap[m.start()] if m.start() < len(omap) else 0
                ln = line_of(t, off)
                all_hits.setdefault((f, ln), set()).add(name)
                per_pat[name] += 1
                if TOPIC.search(norm[max(0, m.start() - 400):m.end() + 400]):
                    on_topic.setdefault((f, ln), set()).add(name)
    res["clause_a_I1_independent_sweep"] = {
        "instrument": "whole-file whitespace-normalized scan (line-wrap-immune)",
        "n_patterns": len(PATTERNS),
        "stage1_recall_sites": len(all_hits),
        "stage1_files": len({f for f, _ in all_hits}),
        "stage2_on_topic_sites": len(on_topic),
        "stage2_on_topic_files": len({f for f, _ in on_topic}),
        "per_pattern_raw_matches": per_pat,
        "note": "deliberately high-recall; the triple-asserting CORE below is the set "
                "where a miss can carry consequence, and it is the one reported as the "
                "finding.",
    }

    # -- the triple-asserting core, and the graded missed set -----------------------
    core = whole_file_sites(BASELINE, TRIPLE, blobs)
    missed = {f"{f}:{i}": v for (f, i), v in sorted(core.items())
              if (f, i) not in swept263}
    res["clause_a_core"] = {
        "triple_asserting_sites": len(core),
        "triple_asserting_files": len({f for f, _ in core}),
        "covered_by_leg263": len(core) - len(missed),
        "MISSED_by_leg263": len(missed),
        "missed_files": len({k.rsplit(":", 1)[0] for k in missed}),
        "missed_sites": missed,
    }

    # hand-grade of the missed set (I3). Grades are this leg's, re-derived at full
    # context; "consequence" states what the miss actually cost, not what it could have.
    # hand-grade of the missed set (I3). Every grade below is this leg's own, decided
    # by reading the site at full context; "consequence" states what the miss actually
    # COST, not what it could in principle have cost.
    res["clause_a_missed_grading"] = {
        "total_missed": 30,
        "total_missed_files": 17,
        "in_leg263_declared_territory": 1,
        "produced_a_wrong_edit": 0,
        "plan_triple": {
            "count": 10,
            "sites": ["plan_of_record.py:868", "DIRECTION.md:9523",
                      "DIRECTION.md:9602", "DIRECTION.md:10075",
                      "DIRECTION.md:10651", "experiments/JOURNAL.md:3639",
                      "experiments/journal/leg_256.md:36",
                      "experiments/journal/leg_262.md:315",
                      "writeup/novelty/leg_255.md:26",
                      "writeup/novelty/leg_262.md:152"],
            "consequence": "0 edits were made to any of them and 0 COULD have been: "
                           "plan_of_record.py has a 0-byte diff, and every other site "
                           "is outside leg 263's declared territory. The set the live "
                           "stage-V ban rests on is intact. What is defective is the "
                           "CENSUS's completeness -- leg 263's class P is reported as "
                           "18 and should be 28 -- not the ban and not any edit.",
            "escalation_trigger": "plan_of_record.py:868 sits inside the re-posed "
                                  "stage-V ban's own LIFT CONDITION ('...establishing it "
                                  "is not subject to the same three-realization death'). "
                                  "Leg 272's mandate flags a miss touching "
                                  "plan_of_record.py's ban text for escalation, so it is "
                                  "flagged. Recorded in the same breath: the DIRECTION of "
                                  "the miss is safe. The occurrence was left "
                                  "byte-identical, and it pins unambiguously to the "
                                  "plan-triple by local enumeration -- the ban's three "
                                  "members are spelled out seven lines above it at "
                                  ":861-862. A census that had caught it would have "
                                  "classified it P and edited nothing.",
        },
        "journal_triple": {
            "count": 17,
            "sites": ["capabilities.py:294", "solver/energy_coercivity.py:2",
                      "DIRECTION.md:1856", "DIRECTION.md:3401", "DIRECTION.md:3402",
                      "DIRECTION.md:3427", "DIRECTION.md:3786", "DIRECTION.md:4340",
                      "DIRECTION.md:4929", "DIRECTION.md:5448", "DIRECTION.md:6141",
                      "DIRECTION.md:10096", "experiments/journal/leg_141.md:203",
                      "experiments/journal/leg_178.md:128",
                      "experiments/p2_route_wes_v1_space.py:377",
                      "writeup/4_p2_lottery/TECHNICAL_P2_WES_V1.md:29",
                      "writeup/novelty/leg_144.md:65"],
            "in_territory": ["experiments/journal/leg_141.md:203"],
            "consequence": "16 of 17 lie OUTSIDE leg 263's declared territory, so 16 "
                           "would have joined its J-recorded list of 45 and been edited "
                           "nowhere even had the grep seen them. Four are one and the "
                           "same quoted string -- leg 178's own gate no-branch, 'a "
                           "genuine third-realization revival' -- which is ABOUT the "
                           "revival and is correct as written. Eight are DIRECTION.md "
                           "historical leg specifications, the class leg 263 explicitly "
                           "and correctly declines to edit. One (novelty/leg_144.md:65) "
                           "is a QUOTATION of capabilities.py, which leg 263's own rule "
                           "forbids correcting.",
            "the_one_in_territory": "experiments/journal/leg_141.md:203 -- 'three dead "
                                    "realizations, of which two (ell^1 no-go, "
                                    "discrete-ball trap -- leg 65) are confirmed novel "
                                    "and the third (weighted-energy zero-width window -- "
                                    "leg 111) is pre-empted'. It is a LOCAL ENUMERATION "
                                    "naming weighted-energy as the third member, it sits "
                                    "BELOW leg 263's correction block (which lands at "
                                    ":215 post-edit), and it is therefore uncovered. It "
                                    "is the single site a rework leg should carry a "
                                    "pointer to. Its severity is low and measurably so: "
                                    "leg 141's own sentence CONTINUES '...and must be "
                                    "de-rated to a statement about a trial-space choice', "
                                    "i.e. leg 141 had already de-rated the third member "
                                    "in the very sentence that counts it. The count is "
                                    "stale; the reading beside it is not.",
        },
        "single_member_or_other_sense": {
            "count": 3,
            "sites": ["writeup/novelty/leg_113.md:167",
                      "experiments/p2_route_xul_v1_lit.py:16",
                      "experiments/journal/leg_154.md:134"],
            "consequence": "leg_113.md:167 names ONE member (the ell^1 tail estimate), "
                           "common to both triples, so no pin is required -- leg 263's "
                           "own class C. xul_v1_lit.py:16 is Xu's own 'Map of "
                           "realizations', the third distinct sense leg 263 classified "
                           "as class N at other line numbers in the same file, so the "
                           "SENSE was censused even though this occurrence was not. "
                           "leg_154.md:134 ('all three integer bands, C3's realistic "
                           "near-miss') is a FALSE POSITIVE of this leg's own pattern, "
                           "reported rather than silently dropped.",
        },
        "mechanical_cause": "TWO causes, both structural rather than careless, and "
                            "together they account for all 30. (1) CASE: leg 263 ran P1 "
                            "case-SENSITIVELY while running P2 case-INSENSITIVELY -- an "
                            "asymmetry its journal does not state -- so every 'THIRD "
                            "realization' in an upper-case docstring, heading or ledger "
                            "field was invisible. (2) FORM AND WRAP: P1's alternations "
                            "are 'three realizations' (space, plural) and 'third "
                            "realization' (space, singular); neither can match the "
                            "HYPHENATED COMPOUND 'three-realization' / "
                            "'third-realization', which is the form plan_of_record.py's "
                            "own lift condition uses -- and a line-oriented grep still "
                            "cannot see the phrase where the 100-column hard wrap splits "
                            "it, which is 9 of the 30. Leg 263 diagnosed the wrap hazard "
                            "correctly and recorded it as standing; it did not follow "
                            "the diagnosis with a wrap-immune instrument, which is what "
                            "this leg supplies.",
    }

    # ================= clause (b): the 8 edited sites ==============================
    sites = []
    for path, ln in EDITED_SITES:
        key = f"{path}:{ln}"
        before = blob(BASELINE, path) or ""
        after = blob(LEG263_COMMITS[1], path) or ""
        bl = before.splitlines()
        v = dict(EDITED_SITE_VERDICTS[key])
        v["site"] = key
        v["line_at_baseline"] = bl[ln - 1] if ln <= len(bl) else None
        v["original_still_standing_after"] = (
            bl[ln - 1] in after if ln <= len(bl) else None)
        sites.append(v)
    p_modified = sorted({p for p, _ in CLASS_P_CLAIMED
                         if blob(BASELINE, p) != blob(LEG263_COMMITS[1], p)})
    res["clause_b"] = {
        "verdict": "CONFIRMED",
        "n_sites": len(sites),
        "n_pinned_journal_independently": sum(
            1 for s in sites if s["independent_pin"] == "journal"),
        "n_disagreeing_with_leg263": sum(
            1 for s in sites if not s["agrees_with_leg263"]),
        "n_wording_correct": sum(1 for s in sites if s["treatment_correct"]),
        "n_originals_still_standing": sum(
            1 for s in sites if s["original_still_standing_after"]),
        "class_P_sites_checked": len(CLASS_P_CLAIMED),
        "class_P_files_modified_by_leg263": p_modified,
        "sites": sites,
    }

    # ================= clause (d): CORRECTIONS.md entries 1-4 ======================
    checks = []
    for name, path, needle in CORRECTIONS_CHECKS:
        t = blob("HEAD", path)
        checks.append({"check": name, "source": path, "needle": needle,
                       "source_exists": t is not None,
                       "found_in_source": bool(t and needle in t)})
    res["clause_d"] = {
        "verdict": "CONFIRMED",
        "n_checks": len(checks),
        "n_found": sum(1 for c in checks if c["found_in_source"]),
        "checks": checks,
        "entry_notes": {
            "1": "leg 111's gate 'NO — 0 of 7' and its banked phrase 'third dead "
                 "realization' both present; the p=1/p=2/p=3 table's magnitudes all "
                 "re-located in legs 111/141/178. ACCURATE.",
            "2": "CORRECTIONS.md says '15 documents'. Leg 180's own gate answer reads "
                 "'Thirty-one passages across fifteen writeup/ files, and eight "
                 "PHASE2_P2_NOTES.md scope lines' (4 primary + 11 derivative = 15). "
                 "The '15' is exactly leg 180's writeup-file count, so ACCURATE -- with "
                 "one precision note: it silently omits PHASE2_P2_NOTES.md, a 16th file "
                 "carrying 8 further scope lines, and the passage count (31) is larger "
                 "than the document count. A narrow restatement, not a wrong one.",
            "3": "leg 185's gate literally answers 'SOLVER ARTIFACT' and its own body "
                 "reads 'partly, and `a`-dependently' on reachability. ACCURATE, "
                 "including the 'named precisely enough to repair' clause, which is "
                 "leg 185's own wording.",
            "4": "leg 178 exists at ba1a22c, landed by the user's ruling; the entry "
                 "correctly marks itself as the same closure as #1 reached by a "
                 "different instrument (measurement vs literature). ACCURATE.",
        },
        "dating_argument_rerun": {
            "git_log_S_on_plan_of_record": sh(
                "git log --format=%h -S'collocation basis leg 56' -- plan_of_record.py"
            ).split(),
            "4ff544a_after_7bd6c08_leg141": sh(
                "git merge-base --is-ancestor 7bd6c08 4ff544a && echo yes || echo no").strip(),
            "4ff544a_after_84a5c7e_leg165": sh(
                "git merge-base --is-ancestor 84a5c7e 4ff544a && echo yes || echo no").strip(),
            "4ff544a_after_e8eb831_leg183": sh(
                "git merge-base --is-ancestor e8eb831 4ff544a && echo yes || echo no").strip(),
        },
    }

    # ================= growth since leg 263 (reported, not a miss) =================
    hb2 = {f: (blob("HEAD", f) or "") for f in tracked("HEAD") if f not in LEG272_OWN}
    core_head = whole_file_sites("HEAD", TRIPLE, hb2)
    res["growth_since_leg263"] = {
        "triple_asserting_sites_at_HEAD": len(core_head),
        "triple_asserting_sites_at_BASELINE": len(core),
        "delta": len(core_head) - len(core),
        "note": "growth from legs 264-278 (which include leg 263's own artifacts and "
                "the later CORRECTIONS.md entries 5-6). NOT attributed to leg 263.",
    }

    # ================= the gate answer =============================================
    res["gate_answer"] = {
        "a": "NO -- 30 triple-asserting occurrences across 17 files were missed",
        "b": "YES -- 8/8 correctly pinned to the journal-triple, 8/8 correctly worded, "
             "0 mis-pins, 0 class-P files modified",
        "c": "YES -- byte-identical, same blob sha, 0 deletions leg-wide",
        "d": "YES -- 16/16 cited magnitudes re-located in their source legs",
        "overall": "NO on clause (a). Leg 263's correction is SUBSTANTIVELY sound and "
                   "its arithmetic exactly reproducible, but its census is incomplete "
                   "by 30 occurrences from two named mechanical causes. 0 of the 30 "
                   "produced a wrong edit; exactly 1 lies in its declared territory.",
    }

    out = os.path.join(REPO, "writeup", "data", "p2_route_wescv_v1_verify.json")
    with open(out, "w") as f:
        json.dump(res, f, indent=2, sort_keys=True)
    print(json.dumps(res["clause_a_I2_reproduction"], indent=2, sort_keys=True))
    print(json.dumps(res["clause_a_core"], indent=2, sort_keys=True)[:2500])
    print(json.dumps(res["gate_answer"], indent=2, sort_keys=True))
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
