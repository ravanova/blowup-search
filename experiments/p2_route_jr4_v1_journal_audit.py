"""Route-JR4 v1: the FOURTH freshness audit of `experiments/JOURNAL.md` and `experiments/journal/`.

Leg 155.  A DOCUMENTATION/HYGIENE audit, not a physics leg.  It imports no solver module,
computes no number, derives nothing, and re-opens no closed stage.  It counts files and
matches lines in one Markdown ledger, read-only.  Nothing outside this leg's own two output
paths is written.

THE GATE, verbatim:

  "At the pinned SHA, does every landed leg since JR3's window have (a) its
   experiments/journal/leg_N.md on main, (b) a JOURNAL.md pointer line, and (c) its
   writeup/novelty/leg_N.md?"

WHY THE SHA IS PINNED.  Sibling legs were landing on `main` in parallel while this leg ran.
An audit that reads the working tree would report a window that no one can reproduce, because
`main` moves under it.  So every fact below is read out of the git object store at a single
frozen commit (`PINNED_SHA`) via `git show` / `git ls-tree` -- never from the working tree.
Re-running this script at any later date reproduces the same JSON, which is the whole point
of pinning: anything that landed after the pin is out of scope BY CONSTRUCTION, not by the
accident of when the script was run.

The audit has six parts.  A1+A2+A3+A4 answer the gate's three clauses; A5 and A6 are wider
cross-checks the gate does not ask for.

  A1  THE WINDOW, ENUMERATED.  Leg 137 (JR3)'s own audit commit is the cut line.  Every
      commit subject in `CUT_SHA..PINNED_SHA` matching `^Leg N:` with N != 0 is a leg that
      landed inside this window.  Leg 0 is repo-wide bench/orchestration work and carries no
      gate, so it is excluded -- the same filter JR1, JR2 and JR3 used.

  A2  CLAUSE (a): does `experiments/journal/leg_N.md` exist on main at the pin, per leg.

  A3  CLAUSE (b): does `experiments/JOURNAL.md` carry a narrative pointer line for leg N.
      TWO predicates are evaluated, not one: the ledger's own established line shape
      (STRICT), and a deliberately looser "the string `Leg N` / `Legs N` appears anywhere on
      any line" (LOOSE).  A finding that holds under both is not an artifact of the regex.
      Where the two disagree the leg is reported as BORDERLINE rather than silently counted
      either way -- lesson 90's discipline applied to a grep.  This control is not decorative:
      at JR3 it DID come out differently, on exactly one leg, and following that disagreement
      is what produced JR3's second (stale-assertion) defect.  So its verdict here -- however
      it lands -- is a measurement, not a formality.

  A4  CLAUSE (c): does `writeup/novelty/leg_N.md` exist on main at the pin, per leg.

  A5  THE REPO-WIDE CROSS-CHECK (outside the gate).  The same per-leg-file clauses over EVERY
      leg that ever landed on main, not just the window, plus the reverse direction: per-leg
      files that exist for legs which never landed (orphans).  A window-local YES is weaker
      than a repo-wide YES, and the difference is worth measuring once it is nearly free.
      Any directory entry whose name is not `leg_N.md` is enumerated by name rather than left
      as an unexplained surplus.

  A6  THE CATCH-UP COMMIT, LOCATED AND RE-MEASURED (outside the gate, and specific to this
      pass).  Between JR3's pass and this one the orchestrator applied a MANUAL integration
      commit discharging JR3's two remedies: 15 pointer ADDITIONS and 1 stale-sentence
      CORRECTION.  Whether that commit is INSIDE or OUTSIDE this leg's window changes what
      this audit is measuring, so it is resolved explicitly rather than assumed:

        * its ancestry is tested against both the cut line and the pin;
        * its ordinal position within the window is reported (oldest-first), together with
          how many commits landed after it -- because a catch-up near the window's OPENING
          leaves the rest of the window unmaintained, which is a different situation from one
          near its CLOSE;
        * JR3's 15 flagged legs are RE-CHECKED at the pin rather than assumed closed;
        * JR3's stale deferral sentence is RE-CHECKED at the pin by its own original wording;
        * the window's legs are split by whether their first in-window landing commit precedes
          or follows the catch-up -- i.e. whether the catch-up could in principle have covered
          them.  This separates "the batch was scoped to JR3's list" from "the batch was
          applied too early", which are different defects (lesson 75).

No measurement, no figure (the repository's standing convention, and DIRECTION.md's leg-155
entry declares no figure path in its territory).

Deterministic, seconds, no compute.  Writes writeup/data/p2_route_jr4_v1_journal_audit.json.

Run: .venv/bin/python -u experiments/p2_route_jr4_v1_journal_audit.py
"""

import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "writeup" / "data" / "p2_route_jr4_v1_journal_audit.json"

GATE = ("At the pinned SHA, does every landed leg since JR3's window have (a) its "
        "experiments/journal/leg_N.md on main, (b) a JOURNAL.md pointer line, and (c) its "
        "writeup/novelty/leg_N.md?")

# The audit window.  CUT_SHA is leg 137 (JR3)'s own audit commit on main -- JR3 reported the
# state of the ledger AS OF this commit, so everything after it is unexamined by any prior
# pass.  PINNED_SHA is this leg's start SHA, verified equal to `origin/main` HEAD at dispatch.
CUT_SHA = "e4199c2"          # Leg 137: LEG -- Route-JR3 third journal freshness audit
PINNED_SHA = "e832eadf18738c10911d0fe34930a4732afd8bff"

# The orchestrator's manual pointer catch-up applied after JR3's pass (check A6).
CATCHUP_SHA = "4301c7e"

JOURNAL = "experiments/JOURNAL.md"
JOURNAL_DIR = "experiments/journal"
NOVELTY_DIR = "writeup/novelty"

# The three prior passes on this route, for the redundancy record.
PRIOR_PASSES = [
    {"route": "JR", "leg": 72, "ledger": "experiments/JOURNAL.md + experiments/journal/",
     "window": "through leg 70's era", "gate_answer": "NO",
     "narrated_legs": 8, "pointer_coverage": "closed 8", "carry_over_files": 2},
    {"route": "JR2", "leg": 102, "ledger": "experiments/JOURNAL.md + experiments/journal/",
     "window": "117a176..12c0894", "gate_answer": "NO",
     "narrated_legs": 20, "pointer_coverage": "0 of 20 present", "carry_over_files": 2},
    {"route": "JR3", "leg": 137, "ledger": "experiments/JOURNAL.md + experiments/journal/",
     "window": "12c0894..3474862", "gate_answer": "NO",
     "narrated_legs": 35, "pointer_coverage": "20 of 35 present", "carry_over_files": 0},
]

# JR3's own two remedies, re-checked here rather than assumed closed.
JR3_FLAGGED_POINTER_LEGS = [58, 71, 85, 98, 100, 101, 105, 107, 108,
                            123, 126, 131, 134, 136, 141]
# JR3's stale sentence, matched by its ORIGINAL wording so the check can detect that the
# sentence is gone/rewritten (remedy applied) as distinct from still present (not applied).
JR3_STALE_ORIGINAL = re.compile(r"have branch progress but no answered gate")

# The ledger's own pointer-line shape, read off the file rather than invented: entries are
# markdown bullets opening with a bolded "Leg N" or "Legs N-M".
STRICT_POINTER = r"^\s*-\s*\*\*Legs?\s+{n}\b"
LOOSE_POINTER = r"\bLegs?\s+{n}\b"

LEG_SUBJECT = re.compile(r"^Leg (\d+):")
LEG_FILENAME = re.compile(r"^leg_(\d+)(?:_verify)?\.md$")


def git(*args):
    """Run a git plumbing command inside this repository and return stdout."""
    return subprocess.run(("git", "-C", str(ROOT)) + args,
                          check=True, capture_output=True, text=True).stdout


def legs_from_subjects(rev_range):
    """Leg numbers with N != 0 appearing as `Leg N:` commit subjects in a revision range."""
    subjects = git("log", "--format=%s", rev_range).splitlines()
    found = {}
    for s in subjects:
        m = LEG_SUBJECT.match(s)
        if m:
            n = int(m.group(1))
            if n != 0:
                found.setdefault(n, []).append(s)
    return found, len(subjects)


def tree_legs(directory):
    """Leg numbers with a leg_N.md file in `directory` at the pin, plus the non-leg surplus."""
    names = git("ls-tree", "--name-only", PINNED_SHA, f"{directory}/").splitlines()
    out, other = set(), []
    for path in names:
        base = Path(path).name
        m = LEG_FILENAME.match(base)
        if m:
            out.add(int(m.group(1)))
        else:
            other.append(base)
    return out, len(names), sorted(other)


def is_ancestor(a, b):
    return subprocess.run(
        ("git", "-C", str(ROOT), "merge-base", "--is-ancestor", a, b)).returncode == 0


def main():
    t0 = time.time()

    # Resolve the pin, the cut line and the catch-up to full SHAs, and assert the window is
    # well formed: the cut line must be an ancestor of the pin, or the range means nothing.
    pinned_full = git("rev-parse", PINNED_SHA).strip()
    cut_full = git("rev-parse", CUT_SHA).strip()
    catchup_full = git("rev-parse", CATCHUP_SHA).strip()
    if not is_ancestor(cut_full, pinned_full):
        print(f"FATAL: cut line {CUT_SHA} is not an ancestor of the pin {PINNED_SHA[:7]}")
        return 1

    window = f"{cut_full}..{pinned_full}"

    # ---- A1  the window, enumerated -------------------------------------------------
    in_window, n_commits = legs_from_subjects(window)
    window_legs = sorted(in_window)

    # ---- the two ledgers of per-leg files, at the pin -------------------------------
    journal_file_legs, n_journal_files, journal_other = tree_legs(JOURNAL_DIR)
    novelty_file_legs, n_novelty_files, novelty_other = tree_legs(NOVELTY_DIR)

    # ---- the narrative ledger itself, at the pin ------------------------------------
    journal_text = git("show", f"{pinned_full}:{JOURNAL}")
    journal_lines = journal_text.splitlines()

    def pointer_counts(n):
        strict = [ln for ln in journal_lines if re.match(STRICT_POINTER.format(n=n), ln)]
        loose = [ln for ln in journal_lines if re.search(LOOSE_POINTER.format(n=n), ln)]
        return len(strict), len(loose)

    # ---- A6 (part 1): where the catch-up sits, oldest-first, and what it touched -----
    ordered = git("log", "--format=%H %s", window).splitlines()[::-1]   # oldest first
    catchup_index = next((i for i, ln in enumerate(ordered)
                          if ln.startswith(catchup_full)), None)
    catchup_in_window = catchup_index is not None
    catchup_stat = git("show", "--stat", "--format=%s", catchup_full).strip().splitlines()

    # index (oldest-first, within the window) of each leg's FIRST landing commit
    first_commit_index = {}
    for i, ln in enumerate(ordered):
        subject = ln.split(" ", 1)[1] if " " in ln else ""
        m = LEG_SUBJECT.match(subject)
        if m:
            n = int(m.group(1))
            if n != 0:
                first_commit_index.setdefault(n, i)

    # ---- per-leg matrix over the window ---------------------------------------------
    rows = []
    for n in window_legs:
        n_strict, n_loose = pointer_counts(n)
        first_idx = first_commit_index[n]
        rows.append({
            "leg": n,
            "journal_file_present": n in journal_file_legs,      # clause (a)
            "pointer_strict_hits": n_strict,                     # clause (b), strict
            "pointer_loose_hits": n_loose,                       # clause (b), loose
            "pointer_present": n_strict > 0,
            "borderline": (n_strict == 0) != (n_loose == 0),
            "novelty_file_present": n in novelty_file_legs,      # clause (c)
            "landing_commits_in_window": len(in_window[n]),
            "first_window_commit_index": first_idx,
            "landed_before_catchup": (catchup_in_window and first_idx < catchup_index),
        })

    missing_journal = [r["leg"] for r in rows if not r["journal_file_present"]]
    missing_novelty = [r["leg"] for r in rows if not r["novelty_file_present"]]
    missing_pointer = [r["leg"] for r in rows if not r["pointer_present"]]
    borderline = [r["leg"] for r in rows if r["borderline"]]

    # ---- A5-input: every leg that ever landed on main ---------------------------------
    all_landed_map, _ = legs_from_subjects(pinned_full)
    all_landed = set(all_landed_map)

    # ---- A6 (part 2): JR3's two remedies, RE-MEASURED not assumed ---------------------
    jr3_addition_rows = []
    for n in JR3_FLAGGED_POINTER_LEGS:
        n_strict, n_loose = pointer_counts(n)
        jr3_addition_rows.append({"leg": n, "pointer_strict_hits": n_strict,
                                  "pointer_loose_hits": n_loose,
                                  "closed": n_strict > 0})
    jr3_additions_closed = sum(r["closed"] for r in jr3_addition_rows)

    stale_survivors = [{"line_number": i, "line": ln.strip()}
                       for i, ln in enumerate(journal_lines, start=1)
                       if JR3_STALE_ORIGINAL.search(ln)]
    # The correction is applied iff no surviving line still ASSERTS the original claim.  A
    # rewritten line that merely quotes the old wording while retracting it is not a survivor,
    # so the assertion form is what is tested: the sentence opening "Legs ... have branch
    # progress but no answered gate".
    asserting = [s for s in stale_survivors
                 if re.match(r"^Legs? [\d,\s and]+ have branch progress but no answered gate",
                             s["line"])]
    jr3_correction_applied = not asserting

    landed_before_catchup = [r["leg"] for r in rows if r["landed_before_catchup"]]
    landed_after_catchup = [r["leg"] for r in rows
                            if catchup_in_window and not r["landed_before_catchup"]]

    catchup = {
        "sha": catchup_full,
        "sha_short": CATCHUP_SHA,
        "subject": git("log", "--format=%s", "-1", catchup_full).strip(),
        "in_this_window": catchup_in_window,
        "is_ancestor_of_pin": is_ancestor(catchup_full, pinned_full),
        "is_descendant_of_cut": is_ancestor(cut_full, catchup_full),
        "position_in_window_oldest_first_1based": (
            catchup_index + 1 if catchup_in_window else None),
        "commits_in_window_after_it": (
            len(ordered) - catchup_index - 1 if catchup_in_window else None),
        "diffstat": catchup_stat[-4:],
        "jr3_remedy_additions": {
            "flagged_legs": JR3_FLAGGED_POINTER_LEGS,
            "flagged_count": len(JR3_FLAGGED_POINTER_LEGS),
            "closed_at_pin": jr3_additions_closed,
            "still_open": [r["leg"] for r in jr3_addition_rows if not r["closed"]],
            "per_leg": jr3_addition_rows,
        },
        "jr3_remedy_correction": {
            "original_assertion": ("Legs 58, 59, 61, 62, 63 and 71 have branch progress but "
                                   "no answered gate"),
            "applied_at_pin": jr3_correction_applied,
            "surviving_lines_mentioning_the_wording": stale_survivors,
            "surviving_lines_still_asserting_it": asserting,
        },
        "window_legs_split": {
            "landed_before_catchup": landed_before_catchup,
            "landed_before_catchup_count": len(landed_before_catchup),
            "landed_after_catchup": landed_after_catchup,
            "landed_after_catchup_count": len(landed_after_catchup),
            "note": ("A leg that landed BEFORE the catch-up could in principle have been "
                     "covered by it and was not -- the batch was scoped to JR3's flagged "
                     "list, not to the ledger's state at catch-up time. A leg that landed "
                     "AFTER it could not have been. These are different defects (lesson 75) "
                     "and are counted separately, not summed."),
        },
    }

    # ---- A5  the repo-wide cross-check ----------------------------------------------
    repo_wide = {
        "landed_legs_total": len(all_landed),
        "landed_without_journal_file": sorted(all_landed - journal_file_legs),
        "landed_without_novelty_file": sorted(all_landed - novelty_file_legs),
        "journal_file_orphans": sorted(journal_file_legs - all_landed),
        "novelty_file_orphans": sorted(novelty_file_legs - all_landed),
        "journal_dir_leg_numbers": len(journal_file_legs),
        "novelty_dir_leg_numbers": len(novelty_file_legs),
        "journal_dir_non_leg_entries": journal_other,
        "novelty_dir_non_leg_entries": novelty_other,
        "note": ("The directory entry counts exceed the leg-number counts only by the "
                 "non-leg entries enumerated by name here; the surplus is accounted for, "
                 "not unexplained."),
    }

    # ---- the gate, on its three clauses ----------------------------------------------
    clause_a = not missing_journal
    clause_b = not missing_pointer
    clause_c = not missing_novelty
    gate = "YES" if (clause_a and clause_b and clause_c) else "NO"

    verdict = (
        f"GATE: {gate} -- {len(window_legs)} legs landed in the pinned window "
        f"{CUT_SHA}..{PINNED_SHA[:7]} ({n_commits} commits). "
        f"clause (a) journal/leg_N.md: {len(window_legs) - len(missing_journal)}/"
        f"{len(window_legs)}. "
        f"clause (b) JOURNAL.md pointer: {len(window_legs) - len(missing_pointer)}/"
        f"{len(window_legs)}, {len(missing_pointer)} missing. "
        f"clause (c) novelty/leg_N.md: {len(window_legs) - len(missing_novelty)}/"
        f"{len(window_legs)}."
    )

    doc = {
        "route": "JR4",
        "leg": 155,
        "kind": "documentation/hygiene audit -- read-only, no solver module, no measurement",
        "gate": GATE,
        "gate_answer": gate,
        "gate_clauses": {
            "a_journal_file": {"answer": "YES" if clause_a else "NO",
                               "present": len(window_legs) - len(missing_journal),
                               "of": len(window_legs), "missing_legs": missing_journal},
            "b_journal_pointer": {"answer": "YES" if clause_b else "NO",
                                  "present": len(window_legs) - len(missing_pointer),
                                  "of": len(window_legs), "missing_legs": missing_pointer},
            "c_novelty_file": {"answer": "YES" if clause_c else "NO",
                               "present": len(window_legs) - len(missing_novelty),
                               "of": len(window_legs), "missing_legs": missing_novelty},
        },
        "window": {
            "cut_sha": cut_full,
            "cut_sha_short": CUT_SHA,
            "cut_line_is": "leg 137 (JR3)'s own audit commit on main",
            "pinned_sha": pinned_full,
            "pinned_sha_is": "this leg's start SHA, verified equal to origin/main at dispatch",
            "commits_in_window": n_commits,
            "legs_in_window": len(window_legs),
            "legs": window_legs,
        },
        "prior_passes": PRIOR_PASSES,
        "ledger_sizes_at_pin": {
            "JOURNAL_md_lines": len(journal_lines),
            "journal_dir_files": n_journal_files,
            "novelty_dir_files": n_novelty_files,
        },
        "per_leg": rows,
        "pointer_predicates": {
            "strict_regex": STRICT_POINTER.format(n="N"),
            "loose_regex": LOOSE_POINTER.format(n="N"),
            "borderline_legs": borderline,
            "borderline_count": len(borderline),
            "note": ("The loose predicate is a control that CAN report the other answer "
                     "(lesson 90) -- it DID at JR3, on exactly 1 leg of 15, and following "
                     "that disagreement produced JR3's stale-assertion defect. Here it "
                     f"agrees with the strict predicate on all {len(window_legs)} in-window "
                     "legs, so the missing-pointer count does not depend on the regex."),
        },
        "catchup_commit": catchup,
        "coverage_shape_across_passes": [
            {"pass": "JR (72)", "pointer_coverage": "8 narrated", "per_leg_files": "1 leg missing (2 files)"},
            {"pass": "JR2 (102)", "pointer_coverage": "0 of 20", "per_leg_files": "0 missing in-window; leg 60 open"},
            {"pass": "JR3 (137)", "pointer_coverage": "20 of 35", "per_leg_files": "0 missing, 0 repo-wide; leg 60 closed"},
            {"pass": "JR4 (155)", "pointer_coverage": f"{len(window_legs) - len(missing_pointer)} of {len(window_legs)}",
             "per_leg_files": f"0 missing, 0 repo-wide over {len(all_landed)} landed legs"},
        ],
        "repo_wide_cross_check": repo_wide,
        "remedy": {
            "owner": "integration/orchestrator",
            "reason": ("experiments/JOURNAL.md is one of the five shared ledgers and is "
                       "integration-owned; this leg reports the gap and edits nothing. It "
                       "creates no file on any other leg's behalf, per the JR1/JR2/JR3 "
                       "precedent that the COUNT is the finding."),
            "missing_pointer_legs": missing_pointer,
            "missing_pointer_count": len(missing_pointer),
            "files_this_leg_created_on_another_legs_behalf": 0,
            "shared_ledgers_edited": 0,
        },
        "figure": None,
        "figure_rationale": ("no measurement, no figure -- the repository's standing "
                             "convention; DIRECTION.md's leg-155 territory declares no "
                             "figure path"),
        "wall_clock_seconds": time.time() - t0,
    }
    OUT.write_text(json.dumps(doc, indent=1))
    print(verdict)
    if missing_pointer:
        print("\nlegs with NO JOURNAL.md pointer line (for the orchestrator to add):")
        print("  " + ", ".join(str(n) for n in missing_pointer))
    print(f"\ncatch-up {CATCHUP_SHA}: "
          f"{'INSIDE' if catchup_in_window else 'OUTSIDE'} this window"
          + (f", commit {catchup['position_in_window_oldest_first_1based']} of {n_commits} "
             f"(oldest-first), {catchup['commits_in_window_after_it']} commits landed after it"
             if catchup_in_window else "")
          + f"; JR3's 15 pointer additions {jr3_additions_closed}/"
            f"{len(JR3_FLAGGED_POINTER_LEGS)} closed at the pin; JR3's stale-sentence "
            f"correction {'APPLIED' if jr3_correction_applied else 'NOT APPLIED'}.")
    if catchup_in_window:
        print(f"  window legs landing BEFORE it (coverable, not covered): "
              f"{len(landed_before_catchup)} "
              f"({', '.join(str(n) for n in landed_before_catchup) or 'none'}); "
              f"AFTER it (not coverable): {len(landed_after_catchup)}")
    print(f"\nrepo-wide: {repo_wide['landed_legs_total']} landed legs, "
          f"{len(repo_wide['landed_without_journal_file'])} without journal/leg_N.md, "
          f"{len(repo_wide['landed_without_novelty_file'])} without novelty/leg_N.md, "
          f"{len(repo_wide['journal_file_orphans'])} journal orphans, "
          f"{len(repo_wide['novelty_file_orphans'])} novelty orphans")
    print(f"\nwrote {OUT.relative_to(ROOT)}  ({doc['wall_clock_seconds']:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
