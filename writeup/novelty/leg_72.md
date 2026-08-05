# Leg 72 (Route-JR) — novelty pass: the journal-coverage inventory for legs 58–71

This leg is a documentation-freshness audit, so its "novelty pass" is not a literature pass.
It is the thing the edit actually claims: **exactly which legs have answered their gate since
the `Legs 54-57` entry, which of them have a narrative pointer in `experiments/JOURNAL.md`,
and which of them have a per-leg file in `experiments/journal/`.** Everything below was read
from `git log`, `git ls-tree` and a directory listing in this worktree at merge base
`08be572` — nothing is inferred from `DIRECTION.md`'s prose or from a dispatch summary.

Committed **before** a single line was appended to `experiments/JOURNAL.md`.

## Counts, up front

- `experiments/JOURNAL.md` last entry: **`## Legs 54-57 (2026-08-05)`**, file length **2789
  lines**. Legs 58–71 appear in it **0 times**.
- Legs whose gate has answered since that entry: **8** — 60, 64, 65, 66, 67, 68, 69, 70.
- Narrative pointers present for those 8 in `experiments/JOURNAL.md`: **0 of 8**. Missing: **8**.
- Per-leg files present for those 8 in `experiments/journal/` on `main`: **7 of 8**.
  Missing on `main`: **1** — `experiments/journal/leg_60.md`.
- Legs with branch progress but **no** answered gate (correctly absent from both): **6** —
  58, 59, 61, 62, 63, 71.

## Which legs have answered, and where the answer lives

Landed on `main` (a `Leg N: LEG —` commit reachable from `main`):

| leg | route | gate answer, as its own journal states it | `experiments/journal/leg_N.md` |
|-----|-------|-------------------------------------------|-------------------------------|
| 64 | A12 | SPLIT — YES on the `sigma = 3` half, NO on the `alpha_1` half | present |
| 65 | L1G | NO | present |
| 66 | QF  | YES | present |
| 67 | FD  | NO (for the quantity this repository holds) | present |
| 68 | IX  | YES — 25/25 quartet pieces | present |
| 69 | IA  | NO — stop-the-line | present |
| 70 | RC  | NO — no origin condition imposed | present |

Answered but **parked, branch not merged** (ORCHESTRATION.md §8 escalation #4):

| leg | route | gate answer | file state |
|-----|-------|-------------|-----------|
| 60 | PQ | NO on its literal terms — 3 of 114 quoted numbers do not re-derive | `experiments/journal/leg_60.md` **absent from `main`**, **present on `origin/leg/pq-v1`** |

**Correction to this leg's own dispatch thesis, measured not assumed.** The dispatch (and
`DIRECTION.md` line 92) records `experiments/journal/leg_60.md` as "missing entirely". It is
missing *from `main` and from every worktree cut from `main`* — which is what an agent
searching by leg number experiences, so the finding stands operationally — but it is **not
missing from the repository**: `git ls-tree -r origin/leg/pq-v1` lists 10 leg-60 artifacts,
including `experiments/journal/leg_60.md` and `writeup/novelty/leg_60.md`. The gap is a
**merge gap, not an authoring gap**. Leg 60 wrote its journal; the park kept it off `main`.
That distinction changes the fix (merge or cherry-pick, a DM call) and is why this leg does
not author a replacement file — it would duplicate, not recover, work that already exists.

## Legs correctly absent

These have novelty passes and/or partial work on unmerged branches, but no answered gate, so
neither a narrative entry nor a landed journal file is owed yet:

| leg | branch | latest commit subject (truncated) |
|-----|--------|-----------------------------------|
| 58 | `leg/ng-v1`  | NG-0 novelty pass, committed before construction |
| 59 | `leg/wv-v1`  | frozen six-property gate re-run answers FAIL 5/6 |
| 61 | `leg/ka-v1`  | Route-KA novelty pass |
| 62 | `leg/cp-v1`  | Route-CP novelty pass, committed before construction |
| 63 | `leg/m2-v1`  | Route-M2 novelty pass, committed before construction |
| 71 | `leg/cap-v1` | novelty pass: pin what `capabilities.py` claims (42 rows, 40 tests) |

Leg 59's commit does carry a gate result (`FAIL 5/6`), but that is the frozen six-property
weight gate, not the leg's dispatch gate, and the branch is unmerged; it is left out of the
narrative rather than summarized from a commit subject.

## The verify lane, reported not fixed

Out of this leg's territory, recorded because the same staleness pattern touches it:

- `verify/58-ng-headline` — merged; `experiments/journal/leg_58_verify.md` present.
- `verify/65-l1g-review` — merged; `experiments/journal/leg_65_verify.md` present.
- `origin/verify/64-a12-review` — **unmerged**, 2 files ahead of `main`
  (`experiments/journal/leg_64_verify.md`, `writeup/novelty/leg_64_verify.md`). Leg 64's
  post-landing review CONFIRMED both halves of the gate and reports three defects; none of
  that is reachable from `main`. **1 unmerged verify pass**, flagged for the orchestrator.
- `verify/70-rc-review` — 0 commits ahead of `main`; no verify artifact exists for leg 70.

## Sourcing rule honoured

Every headline in the appended `experiments/JOURNAL.md` block is copied from the named leg's
own `experiments/journal/leg_N.md` (for leg 60, from the same file on `origin/leg/pq-v1`).
**No number in the appended block was recomputed, re-fit, or re-derived by this leg.**
