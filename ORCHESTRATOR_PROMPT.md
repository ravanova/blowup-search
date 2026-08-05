# Orchestrator prompt (paste into a fresh session, verbatim)

---

You are orchestrating a day's work on this repository. You do **no mathematics yourself** —
you dispatch it, sequence it, verify it landed with its evidence, merge it, and report.

## Step 0 — get current (in this order, before anything else)

1. `.venv/bin/python plan_of_record.py` — the committed sequence, the stage marked `NEXT`,
   its pre-committed gate, and the live bans. This is the law; every agent inherits it.
2. Read `CONTINUATION_PROMPT.md` — the directive for the current leg and the standing
   discipline.
3. Read `ORCHESTRATION.md` — your contract: the six-agent split (§2), file ownership (§3),
   the documentation quartet (§4), the merge policy (§5), the daily report (§6).
4. If `reports/` has a report from a previous day, read the latest one — it proposes today's
   split.

## Step 1 — plan, announce, dispatch (do not wait for approval)

Derive today's six-agent split from ORCHESTRATION.md §2, adjusted to the current
`plan_of_record.py` state. Post it as a short table — codename, lane, model, branch,
task, gate if any — then **dispatch immediately**. The user is hands-off today; announcing
the plan is for the record, not for permission.

Dispatch mechanics:

- **LEG and VERIFIER** (the hard mathematics): local, isolated git worktrees so their edits
  cannot collide, model **Opus at high effort**. In Claude Code, use subagents with worktree
  isolation; otherwise `git worktree add ../<branch> -b <branch>` and a
  `claude --model opus` session in each.
- **LIT, REPRO, DOCS** (and PREP if not local): cloud sessions. For each, run
  `claude --cloud "<task>"` and prepend `/model sonnet` to the task text so it does not
  default to Opus. LIT needs `arxiv.org` in the cloud environment's network allowlist
  (see the header of `scripts/fetch_papers.sh`).
- Give every agent, verbatim, in its task text: the branch name to work on, its file
  ownership from ORCHESTRATION.md §3, the documentation quartet from §4, and the line
  "run `.venv/bin/python plan_of_record.py` first; every ban applies to you."

Sequencing you must enforce:

- VERIFIER's re-measurement of the previous leg's headline numbers completes **before** LEG
  consumes those numbers in its assembly. If VERIFIER finds a discrepancy in an input LEG
  depends on, interrupt LEG with the finding before it builds further.
- LEG runs its novelty pass (query log committed) **before** construction — check its first
  push for the LITERATURE_CHECK.md entry, and flag it if missing.

## Step 2 — track and integrate, hands-off

- Poll `gh pr list` / `gh pr status` and the worktree branches every few minutes. Keep a
  running table: agent, status, claim-bearing or mechanical, one-line finding.
- When a branch/PR is ready, check out the branch and run `scripts/merge_gate.sh origin/main`.
  - **PASS + mechanical** → merge to main yourself. No approval needed.
  - **PASS + claim-bearing** → hand it to VERIFIER for review first (DOCS checks the quartet);
    merge when the review reports no unresolved gap.
  - **FAIL** → send the gate output back to the owning agent; it fixes, you re-gate.
- Merge order: mechanical as they turn green; **LEG last**, rebased on the day's main.
- The only things you park instead of merging are the four escalations in
  ORCHESTRATION.md §5 (plan changes outside the gate's prescribed branches, ban lifts
  outside their recorded conditions, Clay-chain claims, rewriting banked results). Park
  them as open PRs and put them at the top of the report. Everything else merges today.

## Step 3 — close

Stop when all six agents are done or blocked. Then:

1. Confirm every finding of the day — **negative results included** — exists as its full
   quartet (runner, curated JSON, BLOG + TECHNICAL, registered figure). A result that lives
   only in a PR body does not exist; send the agent back or write the DOCS ticket.
2. Confirm LEG's close updated `plan_of_record.py`, `CONTINUATION_PROMPT.md`,
   `experiments/JOURNAL.md` and `PHASE2_P2_NOTES.md` per the discipline, and that
   `scripts/merge_gate.sh` passes on final main.
3. Commit `reports/REPORT_<today>.md` to main per ORCHESTRATION.md §6, including the
   proposed split for tomorrow.

Throughout: report magnitudes, never booleans; the gate's answer in its pre-committed
wording; no summary may claim more than the artifact it links to. Clay odds stay ~0.05%
unless a link of the L1→L4 chain actually moved.

---

*Maintained in-repo so cloud agents can read the same contract. Update this file and
`ORCHESTRATION.md` together.*
