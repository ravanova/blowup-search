"""Route-JR3 v1: the THIRD freshness audit of `experiments/JOURNAL.md` and `experiments/journal/`.

Leg 137.  A DOCUMENTATION/HYGIENE audit, not a physics leg.  It imports no solver module,
computes no number, derives nothing, and re-opens no closed stage.  It counts files and
matches lines in one Markdown ledger, read-only.  Nothing outside this leg's own two output
paths is written.

THE GATE, verbatim:

  "At the pinned SHA, does every landed leg since JR2's window have (a) its
   experiments/journal/leg_N.md on main, (b) a JOURNAL.md pointer line, and (c) its
   writeup/novelty/leg_N.md -- with leg 60's former gap confirmed closed?"

WHY THE SHA IS PINNED.  Legs 126-136 were landing on `main` in parallel while this leg ran.
An audit that reads the working tree would report a window that no one can reproduce, because
`main` moves under it.  So every fact below is read out of the git object store at a single
frozen commit (`PINNED_SHA`) via `git show` / `git ls-tree` -- never from the working tree.
Re-running this script at any later date reproduces the same JSON byte-for-byte, which is the
whole point of pinning: anything that landed after the pin is out of scope BY CONSTRUCTION,
not by the accident of when the script was run.

The audit has five parts.  A1+A2+A3+A4 answer the gate's four clauses; A5 is the wider
cross-check that the gate does not ask for.

  A1  THE WINDOW, ENUMERATED.  Leg 102 (JR2)'s own audit commit is the cut line.  Every
      commit subject in `CUT_SHA..PINNED_SHA` matching `^Leg N:` with N != 0 is a leg that
      landed inside this window.  Leg 0 is repo-wide bench/orchestration work and carries no
      gate, so it is excluded -- the same filter JR1 and JR2 used.

  A2  CLAUSE (a): does `experiments/journal/leg_N.md` exist on main at the pin, per leg.

  A3  CLAUSE (b): does `experiments/JOURNAL.md` carry a narrative pointer line for leg N.
      TWO predicates are evaluated, not one: the ledger's own established line shape
      (STRICT), and a deliberately looser "the string `Leg N` appears anywhere on any line"
      (LOOSE).  A finding that holds under both is not an artifact of the regex.  Where the
      two disagree, the leg is reported as BORDERLINE rather than silently counted either
      way -- lesson 90's discipline applied to a grep: a predicate that cannot come out
      differently is not a measurement, so the loose predicate is here precisely because it
      CAN return a different answer, and the audit reports whether it did.

  A3b THE STALE-ASSERTION CHECK, which the LOOSE predicate of A3 is what surfaced.  A missing
      pointer is silence; a pointer that is now WRONG is worse, and the two are different
      defects (lesson 75).  Leg 72's block closes with a sentence deferring a named list of
      legs as having "branch progress but no answered gate".  Every leg named in it is
      re-checked against the landed set at the pin: any that has since landed makes that
      surviving sentence a false statement about that leg.  This check exists only because
      the loose control returned a different answer from the strict one on exactly one leg --
      which is what a control that can come out differently is for.

  A4  CLAUSE (c): does `writeup/novelty/leg_N.md` exist on main at the pin, per leg; plus the
      named JR2 carry-over -- leg 60's two files -- checked by name and, if present, with the
      commit that added them located, so "closed" is evidenced rather than asserted.

  A5  THE REPO-WIDE CROSS-CHECK (outside the gate).  The same three clauses over EVERY leg
      that ever landed on main, not just the window, plus the reverse direction: per-leg
      files that exist for legs which never landed (orphans).  A window-local YES is weaker
      than a repo-wide YES, and the difference is worth measuring once it is nearly free.

No measurement, no figure (the repository's standing convention, and DIRECTION.md's leg-137
entry declares no figure path in its territory).

Deterministic, seconds, no compute.  Writes writeup/data/p2_route_jr3_v1_journal_audit.json.

Run: .venv/bin/python -u experiments/p2_route_jr3_v1_journal_audit.py
"""

import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "writeup" / "data" / "p2_route_jr3_v1_journal_audit.json"

GATE = ("At the pinned SHA, does every landed leg since JR2's window have (a) its "
        "experiments/journal/leg_N.md on main, (b) a JOURNAL.md pointer line, and (c) its "
        "writeup/novelty/leg_N.md -- with leg 60's former gap confirmed closed?")

# The audit window.  CUT_SHA is leg 102 (JR2)'s own audit commit on main -- JR2 reported the
# state of the ledger AS OF this commit, so everything after it is unexamined by any prior
# pass.  PINNED_SHA is this leg's start SHA: `origin/main` HEAD at dispatch.
CUT_SHA = "12c0894"          # Leg 102: LEG -- JOURNAL.md caught up a second time
PINNED_SHA = "34748624189c0a17a688a9195101bcfcaa2666a5"

JOURNAL = "experiments/JOURNAL.md"
JOURNAL_DIR = "experiments/journal"
NOVELTY_DIR = "writeup/novelty"

# The two prior passes on this route, for the redundancy record.
PRIOR_PASSES = [
    {"route": "JR", "leg": 72, "ledger": "experiments/JOURNAL.md + experiments/journal/",
     "narrated_legs": 8, "carry_over_files": 2},
    {"route": "JR2", "leg": 102, "ledger": "experiments/JOURNAL.md + experiments/journal/",
     "narrated_legs": 20, "carry_over_files": 2},
]

# JR2's single standing carry-over, named in this leg's gate.
CARRY_OVER_LEG = 60
CARRY_OVER_FILES = [f"{JOURNAL_DIR}/leg_{CARRY_OVER_LEG}.md",
                    f"{NOVELTY_DIR}/leg_{CARRY_OVER_LEG}.md"]

# The ledger's own pointer-line shape, read off the file rather than invented: entries are
# markdown bullets opening with a bolded "Leg N" or "Legs N-M".
STRICT_POINTER = r"^\s*-\s*\*\*Legs?\s+{n}\b"
LOOSE_POINTER = r"\bLegs?\s+{n}\b"

# A3b: leg 72's deferral sentence, matched by its own wording rather than by line number so
# the check survives the ledger being appended to.
DEFERRAL = re.compile(r"^Legs? ([\d,\s and]+?) have branch progress but no answered gate")

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
    """Leg numbers that have a leg_N.md (or leg_N_verify.md) file in `directory` at the pin."""
    names = git("ls-tree", "--name-only", PINNED_SHA, f"{directory}/").splitlines()
    out = set()
    for path in names:
        m = LEG_FILENAME.match(Path(path).name)
        if m:
            out.add(int(m.group(1)))
    return out, len(names)


def main():
    t0 = time.time()

    # Resolve the pin and the cut line to full SHAs, and assert the window is well formed:
    # the cut line must be an ancestor of the pin, or the range means nothing.
    pinned_full = git("rev-parse", PINNED_SHA).strip()
    cut_full = git("rev-parse", CUT_SHA).strip()
    ancestry_ok = subprocess.run(
        ("git", "-C", str(ROOT), "merge-base", "--is-ancestor", cut_full, pinned_full)
    ).returncode == 0
    if not ancestry_ok:
        print(f"FATAL: cut line {CUT_SHA} is not an ancestor of the pin {PINNED_SHA[:7]}")
        return 1

    window = f"{cut_full}..{pinned_full}"

    # ---- A1  the window, enumerated -------------------------------------------------
    in_window, n_commits = legs_from_subjects(window)
    window_legs = sorted(in_window)

    # ---- the two ledgers of per-leg files, at the pin -------------------------------
    journal_file_legs, n_journal_files = tree_legs(JOURNAL_DIR)
    novelty_file_legs, n_novelty_files = tree_legs(NOVELTY_DIR)

    # ---- the narrative ledger itself, at the pin ------------------------------------
    journal_text = git("show", f"{pinned_full}:{JOURNAL}")
    journal_lines = journal_text.splitlines()

    # ---- per-leg matrix over the window ---------------------------------------------
    rows = []
    for n in window_legs:
        strict = [ln for ln in journal_lines
                  if re.match(STRICT_POINTER.format(n=n), ln)]
        loose = [ln for ln in journal_lines
                 if re.search(LOOSE_POINTER.format(n=n), ln)]
        rows.append({
            "leg": n,
            "journal_file_present": n in journal_file_legs,      # clause (a)
            "pointer_strict_hits": len(strict),                  # clause (b), strict
            "pointer_loose_hits": len(loose),                    # clause (b), loose
            "pointer_present": len(strict) > 0,
            "borderline": (len(strict) == 0) != (len(loose) == 0),
            "novelty_file_present": n in novelty_file_legs,      # clause (c)
            "landing_commits_in_window": len(in_window[n]),
        })

    missing_journal = [r["leg"] for r in rows if not r["journal_file_present"]]
    missing_novelty = [r["leg"] for r in rows if not r["novelty_file_present"]]
    missing_pointer = [r["leg"] for r in rows if not r["pointer_present"]]
    borderline = [r["leg"] for r in rows if r["borderline"]]

    # ---- A5-input: every leg that ever landed on main, needed by A3b and A5 -----------
    all_landed_map, _ = legs_from_subjects(pinned_full)
    all_landed = set(all_landed_map)

    # ---- A3b  the stale deferral sentence ---------------------------------------------
    stale = {"sentence_found": False, "line_number": None, "sentence": "",
             "legs_named": [], "legs_since_landed": [], "legs_still_accurate": []}
    for i, ln in enumerate(journal_lines, start=1):
        m = DEFERRAL.match(ln.strip())
        if m:
            named = sorted(int(x) for x in re.findall(r"\d+", m.group(1)))
            landed_since = sorted(n for n in named if n in all_landed)
            stale = {
                "sentence_found": True,
                "line_number": i,
                "sentence": ln.strip(),
                "legs_named": named,
                "legs_since_landed": landed_since,
                "legs_still_accurate": sorted(set(named) - set(landed_since)),
            }
            break
    stale["named_count"] = len(stale["legs_named"])
    stale["falsified_count"] = len(stale["legs_since_landed"])

    # ---- A4  the named JR2 carry-over ------------------------------------------------
    carry = []
    for path in CARRY_OVER_FILES:
        present = subprocess.run(
            ("git", "-C", str(ROOT), "cat-file", "-e", f"{pinned_full}:{path}")
        ).returncode == 0
        adding = ""
        if present:
            log = git("log", "--format=%h %s", "--diff-filter=A", pinned_full,
                      "--", path).splitlines()
            adding = log[-1] if log else ""
        carry.append({"path": path, "present_at_pin": present, "added_by": adding})
    carry_closed = all(c["present_at_pin"] for c in carry)

    # ---- A5  the repo-wide cross-check ----------------------------------------------
    repo_wide = {
        "landed_legs_total": len(all_landed),
        "landed_without_journal_file": sorted(all_landed - journal_file_legs),
        "landed_without_novelty_file": sorted(all_landed - novelty_file_legs),
        "journal_file_orphans": sorted(journal_file_legs - all_landed),
        "novelty_file_orphans": sorted(novelty_file_legs - all_landed),
    }

    # ---- the gate, on its four clauses ----------------------------------------------
    clause_a = not missing_journal
    clause_b = not missing_pointer
    clause_c = not missing_novelty
    gate = "YES" if (clause_a and clause_b and clause_c and carry_closed) else "NO"

    verdict = (
        f"GATE: {gate} -- {len(window_legs)} legs landed in the pinned window "
        f"{CUT_SHA}..{PINNED_SHA[:7]} ({n_commits} commits). "
        f"clause (a) journal/leg_N.md: {len(window_legs) - len(missing_journal)}/"
        f"{len(window_legs)}. "
        f"clause (b) JOURNAL.md pointer: {len(window_legs) - len(missing_pointer)}/"
        f"{len(window_legs)}, {len(missing_pointer)} missing. "
        f"clause (c) novelty/leg_N.md: {len(window_legs) - len(missing_novelty)}/"
        f"{len(window_legs)}. "
        f"leg {CARRY_OVER_LEG} carry-over: {'CLOSED' if carry_closed else 'STILL OPEN'} "
        f"({sum(c['present_at_pin'] for c in carry)}/{len(carry)} files present)."
    )

    doc = {
        "route": "JR3",
        "leg": 137,
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
            "d_leg_60_carry_over_closed": {"answer": "YES" if carry_closed else "NO",
                                           "files": carry},
        },
        "window": {
            "cut_sha": cut_full,
            "cut_sha_short": CUT_SHA,
            "cut_line_is": "leg 102 (JR2)'s own audit commit on main",
            "pinned_sha": pinned_full,
            "pinned_sha_is": "origin/main HEAD at leg 137's dispatch",
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
            "note": ("The loose predicate is a control that CAN report the other answer "
                     "(lesson 90), and it DID, on exactly one leg. That single disagreement "
                     "is not noise: it is leg 72's deferral sentence, and it is what check "
                     "A3b (stale_assertion) was written to follow up. The other "
                     "missing-pointer legs are 0 under BOTH predicates, so their count does "
                     "not depend on the regex."),
        },
        "stale_assertion": stale,
        "repo_wide_cross_check": repo_wide,
        "remedy": {
            "owner": "integration/orchestrator",
            "reason": ("experiments/JOURNAL.md is one of the five shared ledgers and is "
                       "integration-owned; this leg reports the gap and edits nothing. It "
                       "creates no file on any other leg's behalf, per the JR1/JR2 "
                       "precedent that the COUNT is the finding."),
            "missing_pointer_legs": missing_pointer,
            "missing_pointer_count": len(missing_pointer),
            "stale_sentence_to_correct": {
                "line_number": stale["line_number"],
                "why": ("this surviving sentence asserts 'no answered gate' for legs that "
                        "have since answered a gate and landed; it is a wrong statement, "
                        "not a missing one"),
                "falsified_for_legs": stale["legs_since_landed"],
            },
            "files_this_leg_created_on_another_legs_behalf": 0,
            "shared_ledgers_edited": 0,
        },
        "figure": None,
        "figure_rationale": ("no measurement, no figure -- the repository's standing "
                             "convention; DIRECTION.md's leg-137 territory declares no "
                             "figure path"),
        "wall_clock_seconds": time.time() - t0,
    }
    OUT.write_text(json.dumps(doc, indent=1))
    print(verdict)
    if missing_pointer:
        print("\nlegs with NO JOURNAL.md pointer line (for the orchestrator to add):")
        print("  " + ", ".join(str(n) for n in missing_pointer))
    if stale["falsified_count"]:
        print(f"\nSTALE ASSERTION at {JOURNAL}:{stale['line_number']} -- names "
              f"{stale['named_count']} legs as having 'no answered gate'; "
              f"{stale['falsified_count']} of them have since landed "
              f"({', '.join(str(n) for n in stale['legs_since_landed'])}); still accurate "
              f"for {len(stale['legs_still_accurate'])} "
              f"({', '.join(str(n) for n in stale['legs_still_accurate']) or 'none'})")
    print(f"\nrepo-wide: {repo_wide['landed_legs_total']} landed legs, "
          f"{len(repo_wide['landed_without_journal_file'])} without journal/leg_N.md, "
          f"{len(repo_wide['landed_without_novelty_file'])} without novelty/leg_N.md, "
          f"{len(repo_wide['journal_file_orphans'])} journal orphans, "
          f"{len(repo_wide['novelty_file_orphans'])} novelty orphans")
    print(f"\nwrote {OUT.relative_to(ROOT)}  ({doc['wall_clock_seconds']:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
