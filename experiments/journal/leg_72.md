# Leg 72 — Route-JR: the `experiments/JOURNAL.md` / `experiments/journal/` freshness audit

**Branch** `leg/jr-v1`. **Light mechanical/documentation leg, not critical path.**
**Territory:** `experiments/JOURNAL.md` (append-only), `writeup/novelty/leg_72.md`,
`experiments/journal/leg_72.md`. No solver, runner, curated data file or figure was produced
or modified. Individual `experiments/journal/leg_N.md` files were **read, never written**.

## The gate, verbatim

> Does `experiments/JOURNAL.md`'s narrative and `experiments/journal/`'s per-leg file exist
> for every leg that has landed (gate has answered) since the "Legs 54-57" entry?

**Answer: NO.** Of the **8** legs whose gate has answered since that entry (60, 64, 65, 66,
67, 68, 69, 70), **0 of 8** had a narrative pointer in `experiments/JOURNAL.md`, and **1 of
8** has no per-leg file on `main` (`experiments/journal/leg_60.md`). So the no-branch applied:
one pointer-only block appended, and the missing file reported rather than authored.

## Order of work

1. `plan_of_record.py` — read (from `/home/andy/projects/Unsolved/.venv/bin/python`; the
   worktree has no `.venv` of its own). `NG` is `NEXT`. Every live ban is a research ban —
   gCLM measurement, Route-D bound-sharpening, DSS re-asks, 2D beta, the scaling gauge, GA
   compute on an unvalidated fitness, and the several no-re-reading-of-legs-51-53 clauses.
   **This leg runs nothing, measures nothing, and derives no number**, so none of them bind;
   the closest is the standing prohibition on re-deriving settled numbers, which this leg
   honours by copying every headline verbatim from the source leg's own journal.
2. **Novelty pass FIRST**, committed before a line was appended (`writeup/novelty/leg_72.md`,
   commit `0162725`). For an audit leg the pass is the inventory itself — the counts the edit
   claims — not a literature sweep.
3. The append to `experiments/JOURNAL.md`, then this journal.

## What was stale, in counts

At merge base `08be572`:

- `experiments/JOURNAL.md` is **2789 lines**; its last entry is `## Legs 54-57 (2026-08-05)`.
  Legs 58 through 71 appear in it **0 times**.
- **8 answered gates with 0 pointers.** Missing narrative entries: **8**.
- **7 of 8** per-leg files present on `main` (64, 65, 66, 67, 68, 69, 70). **1 missing**:
  `experiments/journal/leg_60.md`.
- **6 legs correctly absent** (branch progress, gate not answered): 58, 59, 61, 62, 63, 71.

## The one correction this audit makes to its own dispatch

The dispatch and `DIRECTION.md` line 92 record `experiments/journal/leg_60.md` as **missing
entirely**. Measured: it is missing from `main` and from every worktree cut from `main` — so
the operational finding stands, an agent searching by leg number cannot find leg 60 — but the
file **exists on `origin/leg/pq-v1`**, alongside 9 other leg-60 artifacts including
`writeup/novelty/leg_60.md`, both figures and both evidence scripts.

This is a **merge gap, not an authoring gap.** Leg 60 did write its journal; parking the
branch under escalation #4 kept it off `main`. That is why this leg authors no replacement:
a fresh file would duplicate, not recover, and the real fix (merge, cherry-pick, or leave
parked) is the DM's call on an escalation that is still open.

## What was appended

One block, `## Legs 60-70 (2026-08-06)`, mirroring the `Legs 54-57` block's style: a header
naming the outcome, a pointer sentence, one bullet per leg carrying that leg's route, its
gate answer and its headline numbers, and the standing `no link of the L1->L4 chain moved /
Clay unchanged at ~0.05%` close. **42 lines inserted, 0 deleted, 0 reordered** — the
append-only discipline that makes a leg touching an integration-owned ledger safe.

## Reported, not fixed (out of territory)

- **`experiments/journal/leg_60.md` is absent from `main`.** Recoverable from
  `origin/leg/pq-v1`; belongs to leg 60's territory and to escalation #4, not to this audit.
- **`verify/64-a12-review` was unmerged at merge base**, 2 files ahead
  (`experiments/journal/leg_64_verify.md`, `writeup/novelty/leg_64_verify.md`) — and **landed
  at `ac92516` during this leg's run**, closing that gap without this leg's help. Leg 64's
  review confirmed both halves of its gate and reports three defects in the "two traps"
  section (chief: J. Chen's `a=1/2` criticality misattributed as `gamma=2`). Recorded here
  because the audit's counts are stated as-of a commit: **0 unmerged verify passes at
  `ac92516`, 1 at `08be572`.** No new leg gate answered in that window, so the 8-leg count
  in the appended block is unchanged.
- **`verify/70-rc-review` is 0 commits ahead of `main`** — no verify artifact exists for leg
  70, in contrast to legs 58 and 65, which both have landed `*_verify.md` journals.
- The same staleness one level up was leg 68's (`writeup/INDEX.md`, caught up to leg 57).
  `INDEX.md` is now stale again by the same 8 legs; that is `INDEX.md`'s territory, not this
  leg's, and is the obvious next audit in this family.
