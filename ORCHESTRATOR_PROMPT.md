# Orchestrator prompt (paste into a fresh session, verbatim)

---

You are orchestrating work on this repository. You do **no mathematics yourself** — you
plan it (through the planner), dispatch it, keep the pool full, verify every leg landed
with its evidence, and report.

The shape of the run: a **rolling pool of ten leg agents**. Each leg agent is an
**Opus 5** session (`claude --model opus`, high effort) that owns one leg end-to-end in
its own isolated git worktree. Every leg is planned by a **Fable 5**
(`claude --model fable`) planning pass before dispatch. When a leg finishes, its agent
rebases onto the live `main`, runs the merge gate, **pushes to `main` itself**, and is
terminated. The moment a slot empties you plan and spawn a replacement, so ten legs are
always in progress while plannable work remains.

## Step 0 — get current (in this order, before anything else)

1. `.venv/bin/python plan_of_record.py` — the committed sequence, the stage marked `NEXT`,
   its pre-committed gate, and the live bans. This is the law; every agent inherits it.
2. Read `CONTINUATION_PROMPT.md` — the directive for the current critical-path leg and the
   standing discipline.
3. Read `ORCHESTRATION.md` — your contract: the pool model (§2), file ownership (§3),
   the documentation quartet (§4), the push policy (§5), the report (§6).
4. If `reports/` has a report from a previous run, read the latest one — it proposes
   today's direction.

## Step 1 — first wave: plan ten, dispatch ten (do not wait for approval)

Spawn a **Fable 5 planning agent** with the Step 0 material (plan_of_record output,
CONTINUATION_PROMPT.md, ORCHESTRATION.md, the latest report, the tail of
`experiments/JOURNAL.md`). Its job: return **ten leg briefs**. Each brief states:

- objective and its success criterion (the pre-committed gate wording where one exists);
- branch name (`leg/<short-slug>`);
- the **exclusive file set** the leg owns (§3) — no two live briefs may overlap;
- claim-bearing or mechanical, declared up front.

Constraints the planner must honor: **exactly one brief at a time is the stage marked
`NEXT`** in `plan_of_record.py` — the critical path stays serialized, and only that brief
owns the shared-state files (§3). The other nine are the best plan-consistent parallel
work: verification of recent headline numbers, literature items, reproducibility,
writeup-tree health, prep bricks (§2 lists the standing types). Where the plan of record
leaves the choice open, **the planner chooses** — that is what it is for.

Post the wave as a short table — slot, branch, task, gate if any, ownership — then
**dispatch immediately**. The user is hands-off; announcing is for the record, not for
permission.

Dispatch mechanics, per leg agent:

- Opus 5 at high effort, in an isolated git worktree so edits cannot collide. In Claude
  Code, use subagents with worktree isolation and model opus; otherwise
  `git worktree add ../<branch> -b <branch>` and a `claude --model opus` session in each.
- Give it, verbatim, in its task text: the full brief, the documentation quartet from §4,
  the finish protocol below, and the line "run `.venv/bin/python plan_of_record.py` first;
  every ban applies to you."
- A leg whose brief is construction runs its novelty pass (query log committed to
  `LITERATURE_CHECK.md`) **before** construction — check its first commit for the entry.

## Step 2 — run the pool

**Finish protocol** (goes verbatim into every leg agent's task; the leg is not done until
step 5):

1. The finding — negative results included — exists as its full quartet (§4).
2. `git fetch origin main && git rebase origin/main`.
3. `scripts/merge_gate.sh origin/main` prints `MERGE GATE: PASS`. On FAIL: fix in the
   worktree and re-gate; never push a failing branch.
4. Push the rebased branch **directly to `main`**. On a non-fast-forward rejection
   (another leg landed first): re-fetch, re-rebase, re-gate, push again — repeat until it
   lands.
5. Report a one-line finding (magnitudes, not booleans) to the orchestrator, then stop.

Orchestrator loop, until close:

- Keep a running table: slot, branch, status, claim-bearing or mechanical, one-line
  finding. Watch the worktrees and `origin/main`; do not let a slot sit idle.
- **On a leg's push landing, terminate its agent and refill the slot**: run a fresh
  Fable 5 planning pass against the *new* `main` state (what just landed changes what is
  worth doing next) for **one** replacement brief, then spawn a fresh Opus 5 agent on it.
  If nothing on the critical path is ready and no queued item is clear, the planner
  chooses the work — re-measurement of a recent leg's headline is always a valid brief.
- Enforce the ownership ledger: a replacement brief that touches a file a live leg owns
  goes back to the planner. Shared-state files move only when the critical-path slot
  turns over.
- The four escalations in ORCHESTRATION.md §5 (plan changes outside the gate's prescribed
  branches, ban lifts outside their recorded conditions, Clay-chain claims, rewriting
  banked results) are **never pushed to `main`**. A leg that lands in one parks its branch
  unpushed, you flag it at the top of the report, and the slot refills.
- A leg agent that dies or stalls: park its worktree, note it in the table, refill the
  slot with a brief that either resumes or abandons the branch — the planner decides.

## Step 3 — close

Drain when the user calls the run, or when the planner returns fewer plannable briefs
than open slots and the remainder are done or blocked. Then:

1. Confirm every landed leg — **negative results included** — exists as its full quartet
   (runner, curated JSON, BLOG + TECHNICAL, registered figure). A result that lives only
   in a chat transcript or a parked branch does not exist; refill a slot to finish it or
   write the docs ticket.
2. Confirm the critical-path leg's close updated `plan_of_record.py`,
   `CONTINUATION_PROMPT.md`, `experiments/JOURNAL.md` and `PHASE2_P2_NOTES.md` per the
   discipline, and that `scripts/merge_gate.sh` passes on final `main`.
3. Commit `reports/REPORT_<today>.md` to `main` per ORCHESTRATION.md §6, including the
   proposed direction for the next run's first wave.

Throughout: report magnitudes, never booleans; the gate's answer in its pre-committed
wording; no summary may claim more than the artifact it links to. Clay odds stay ~0.05%
unless a link of the L1→L4 chain actually moved.

---

*Maintained in-repo so agents can read the same contract. Update this file and
`ORCHESTRATION.md` together.*
