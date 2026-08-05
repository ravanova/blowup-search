# Settings proposal: `.claude/settings.json` deny block for §5a ledgers (C4)

**Status:** proposal only. `.claude/settings.json` is orchestrator-owned; this file does not
modify it. The orchestrator should review and apply (or amend) the snippet below by hand.

**Source:** `reports/TECH_DEBT_REVIEW_2026-08-05.md`, item C4.

## Rationale

ORCHESTRATION.md §5a names six files as integration-owned and single-writer: `plan_of_record.py`,
`CONTINUATION_PROMPT.md`, `experiments/JOURNAL.md`, `PHASE2_P2_NOTES.md`, `LITERATURE_CHECK.md`
(all five orchestrator-only, one integration commit per cycle) and `DIRECTION.md` (Decision-Maker
only, per §5a's closing line and the DM's exclusive role elsewhere in the doc). §5a is explicit
that this single-writer discipline "is what makes ten-way parallelism possible at all" — but
`.claude/settings.json` currently has no `deny` block at all. `Edit`, `Write`, and `MultiEdit` are
unconditionally allowlisted, so nothing in the tool layer actually stops a leg, verifier, or
support agent from writing to these six files; the only thing enforcing §5a today is every agent
choosing to obey its own briefing. A `deny` block makes the rule mechanical instead of a promise,
which matters more as the parallel-leg count grows and briefings get compressed to fit context.

## Proposed `deny` block

Add a `permissions.deny` array (currently absent) with one `Edit` + `Write` + `MultiEdit` triple
per protected file. Patterns are **filename-exact, not directory-wide** — verified against the
actual paths in this repo (all six files live at the paths shown; none are inside a directory this
would need to blanket-deny):

```json
"deny": [
  "Edit(./plan_of_record.py)",
  "Write(./plan_of_record.py)",
  "MultiEdit(./plan_of_record.py)",

  "Edit(./CONTINUATION_PROMPT.md)",
  "Write(./CONTINUATION_PROMPT.md)",
  "MultiEdit(./CONTINUATION_PROMPT.md)",

  "Edit(./DIRECTION.md)",
  "Write(./DIRECTION.md)",
  "MultiEdit(./DIRECTION.md)",

  "Edit(./experiments/JOURNAL.md)",
  "Write(./experiments/JOURNAL.md)",
  "MultiEdit(./experiments/JOURNAL.md)",

  "Edit(./PHASE2_P2_NOTES.md)",
  "Write(./PHASE2_P2_NOTES.md)",
  "MultiEdit(./PHASE2_P2_NOTES.md)",

  "Edit(./LITERATURE_CHECK.md)",
  "Write(./LITERATURE_CHECK.md)",
  "MultiEdit(./LITERATURE_CHECK.md)"
]
```

**Non-collision check (the point this task asked to double-check):** §5a's own mechanism for
legs to contribute to `experiments/JOURNAL.md` and `LITERATURE_CHECK.md` is that each leg writes
its own `experiments/journal/leg_<N>.md` and `writeup/novelty/leg_<N>.md`, and the orchestrator
adds a one-line pointer into the ledger afterward. The patterns above match only the literal
strings `./experiments/JOURNAL.md` and `./LITERATURE_CHECK.md` — exact filenames, no wildcard,
no directory prefix match. A leg writing `experiments/journal/leg_57.md` or
`writeup/novelty/leg_57.md` is a different filename and is untouched by this deny block; a leg
still needs (and keeps) ordinary write access to its own per-leg files under `experiments/journal/`
and `writeup/novelty/`. Do not generalize any of these six patterns to `experiments/*` or
`writeup/*` — that would block the exact per-leg write path §5a depends on.

**Caveat the orchestrator should confirm before applying:** file-scoped `Edit`/`Write`/`MultiEdit`
deny does not stop a `Bash` tool call from overwriting these files directly (e.g. `cp foo.md
CONTINUATION_PROMPT.md`, or a redirect). Bash permission patterns in this file are prefix-matched
on the command string (`"Bash(cmd:*)"`), not argument-aware, so there is no equally precise way to
deny "any `cp`/`mv`/shell-redirect whose *destination* is one of these six files" without also
blocking legitimate uses of the same commands elsewhere. The `deny` block above is the load-bearing
fix for the common case (agents editing files with Edit/Write/MultiEdit, which is how ledger
violations have actually happened); closing the Bash-level gap is a smaller, separate hardening
step addressed below by narrowing the blanket `mv`/`cp` allow rather than trying to pattern-match
destinations.

## Other two cleanups flagged in C4

### 1. Duplicated `Bash(git push:*)` entry

`permissions.allow` currently has `"Bash(git push:*)"` twice — once on line 4 (grouped with the
merge/CI commands near the top) and once on line 31 (grouped with the rest of the `git`
subcommands). Functionally harmless (allow-list is a set), but it's dead weight and makes the
file harder to diff/review. Proposal: delete the line-4 occurrence and keep the one in the `git`
subcommand block (line 31), since that's where every other `git <subcommand>` entry lives.

### 2. Blanket `mv`/`cp` scope

Current entries:
```json
"Bash(cp:*)",
"Bash(mv:*)",
```
are unscoped — they allow moving or overwriting *any* file in the repo, including the six §5a
ledgers and `.claude/settings.json` itself, via a path the `Edit`/`Write` deny block above cannot
see (see caveat above). Proposal: narrow to the directories where legs and support agents actually
need `cp`/`mv` — `experiments/`, `writeup/`, and `Papers/` (paper PDFs) — for example:
```json
"Bash(cp experiments/*)",
"Bash(cp writeup/*)",
"Bash(cp Papers/*)",
"Bash(mv experiments/*)",
"Bash(mv writeup/*)",
"Bash(mv Papers/*)",
```
**Flag for the orchestrator:** confirm these argument-scoped patterns actually match the way
Claude Code's permission engine parses `Bash(...)` rules in the version this repo runs (the
existing file only uses the `cmd:*` prefix-wildcard form, e.g. `"Bash(git push:*)"`, never an
argument-position glob) — if argument-position globs aren't supported, the safe fallback is to
drop the blanket `cp:*`/`mv:*` allow entirely and let those calls fall through to a per-use
prompt, which is safe but adds friction for legitimate per-leg file moves.

### 3. Stale fetch-script reference

`permissions.allow` allowlists `scripts/fetch_papers.sh`, but the repo has two paper-fetch
scripts and `scripts/fetch_papers.sh` is the older/staler one:

- `scripts/fetch_papers.sh` — added 2026-07-28 (commit `cad66bd`). Hardcoded 4-paper table,
  no egress diagnosis beyond a one-line stderr hint.
- `Papers/fetch.sh` — added 2026-08-04 (commit `01cc35b`), i.e. newer. Driven by
  `Papers/MANIFEST.md`'s tiered paper list (14 papers across TIER1/2/3, vs. 4 hardcoded),
  probes egress first and fails loudly with the exact allowlist request when blocked (the
  documented fix for the recurring "five literature passes stayed search-level" failure mode —
  see `CONTINUATION_PROMPT.md` DIRECTIVE 1 / commit `01cc35b`), and is invoked as `bash
  Papers/fetch.sh` per its own header.

`Papers/fetch.sh` is not currently in the allowlist at all, so any agent following the newer,
better-documented script hits a permission prompt every time. Proposal: add it to `allow`
alongside (not instead of — `LITERATURE_CHECK.md` log entries show both scripts have been used
successfully in past sessions, and removing the older entry isn't this task's call) the existing
entry:
```json
"Bash(scripts/fetch_papers.sh:*)",
"Bash(./scripts/fetch_papers.sh:*)",
"Bash(Papers/fetch.sh:*)",
"Bash(bash Papers/fetch.sh:*)",
```
The orchestrator may separately choose to deprecate `scripts/fetch_papers.sh` in favor of
`Papers/fetch.sh` — that's a judgment call about which script stays canonical, out of scope for
this mechanical proposal.

## Summary of file this touches

Only `.claude/settings.json` (proposed, not applied). No other file's behavior is affected by
this proposal.
