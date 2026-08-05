# Orchestration playbook — multi-agent runs on this repo

**How this is used:** the user pastes [ORCHESTRATOR_PROMPT.md](ORCHESTRATOR_PROMPT.md) into a
fresh Claude session. That session is the **orchestrator**: it runs a rolling pool of ten
leg agents, keeps the pool full, watches their pushes land on `main` unattended, and files
a report. This file is the durable contract the prompt points at, so the prompt stays short
and this stays versioned.

Three roles, three models:

- **Orchestrator** (the pasted session, Sonnet is fine): dispatch, collision avoidance,
  pool refill, honest reporting. It does **no mathematics itself** and no planning itself.
- **Planner** (Fable 5): plans every leg before it is dispatched — the first wave of ten,
  and each replacement brief as slots empty. Where the plan of record leaves the choice
  open, the planner chooses the work.
- **Leg agents** (ten × Opus 5, high effort): each owns one leg end-to-end in an isolated
  git worktree, pushes its finished leg directly to `main`, and is terminated. A fresh
  agent spawns into the empty slot on a fresh brief, so ten legs are always in progress.

---

## 1. Inherited law (nothing here overrides it)

1. **`plan_of_record.py` is the plan.** Run `.venv/bin/python plan_of_record.py` for the
   current stage, its pre-committed gate, and the live bans. `test_plan_of_record.py` fails
   if the plan, [CONTINUATION_PROMPT.md](CONTINUATION_PROMPT.md) and
   [CLAY_ROADMAP.md](CLAY_ROADMAP.md) disagree — the merge gate runs it on every push.
2. **Bans are machine-readable and agents inherit all of them.** A ban is lifted only by the
   lift condition it names, never by an agent's judgement.
3. **One leg at a time on the critical path.** The stage the plan marks `NEXT` is a single
   leg, executed by a single agent, with the gate answered exactly as pre-committed (both
   outcomes are already written down; the agent's job is to find out which one happened).
   Pool corollary: **at most one of the ten slots holds the critical-path stage at any
   time**; the other nine run plan-consistent parallel work. Parallelism widens the pool,
   it does not parallelize the critical path.
4. **The standing discipline in CONTINUATION_PROMPT.md** (gate the operator, magnitudes not
   booleans, name the realization, novelty pass before construction, negative controls that
   can fail, lesson 88, …) applies to every agent, not just the critical-path agent.
5. **Walls 1 and 2 stand.** No agent output is ever summarised as movement toward Clay
   unless a link of the L1→L4 chain actually moved, which has not happened in 52 legs.

## 2. The rolling ten-leg pool

There is no fixed agent split. The **planner (Fable 5)** writes every leg brief: ten for
the first wave, then one per empty slot for the rest of the run, each planned against the
`main` that exists at that moment. A brief states the objective and success criterion (the
pre-committed gate wording where one exists), the branch name (`leg/<short-slug>`), the
exclusive file set the leg owns (§3), and whether the leg is claim-bearing or mechanical.

Exactly one live brief is the critical-path stage (§1.3). For the other nine slots the
planner draws on the standing brick types — the lanes of the old six-agent split, now
briefs the planner issues as the state warrants:

| Brick type | What the brief looks like |
|---|---|
| **Verification** | Re-measure a recent leg's headline before anything builds on it (lesson 85): re-run its runner, check every number in its BLOG/TECHNICAL prose against its `writeup/data/*.json`, re-run its negative controls. **Report gaps, do not repair.** With legs pushing to `main` themselves, this is a rolling duty — the planner should keep at least one verification brief live whenever a claim-bearing leg has landed unreviewed. |
| **Literature** | The open literature items the plan records (currently: the arXiv:2604.01868 resurfacing flag; whether Breden–Desvillettes–Lessard arXiv:1503.06315 covers a zero-diagonal Fredholm operator). Fetch via `scripts/fetch_papers.sh`; append query logs to [LITERATURE_CHECK.md](LITERATURE_CHECK.md). |
| **Reproducibility** | Run every `test_*.py` at the repo root and report failures; regenerate figures via `writeup/build_figures.py` from `writeup/data/` and flag any that changed; run the `writeup/*/\*_evidence.py` scripts on a fresh clone and confirm they rebuild without re-runs. Fix *scripts*; never touch claims — a prose/JSON discrepancy is reported, not repaired. |
| **Docs** | The writeup tree's health: maintain `writeup/INDEX.md` (one line per leg: route, gate answer, links to BLOG/TECHNICAL/data/figure); check every route has the full quartet (§4) and list gaps; fix dead links; keep the root `README.md` orientation current. |
| **Prep** | The best plan-consistent parallel brick that is *not* the critical path. Currently: implement the two named repairs from the C-PILOT leg ([writeup/4_p2_lottery/TECHNICAL_P2_ROUTEC_PILOT_V0.md](writeup/4_p2_lottery/TECHNICAL_P2_ROUTEC_PILOT_V0.md) §4 — P2 and P3 failed) in `solver/weight_search.py`, then re-run the six-property viability gate. That re-run is the *only* recorded lift path for the GA-compute ban — and even a 6/6 pass does **not** authorize GA compute the same run; it is recorded for the next planning pass. |

When none of the above is clear — the critical path is occupied, the queue is empty — the
planner **chooses the work**: that is its mandate. Re-measurement of a recent headline is
always a valid brief; an idle slot is not.

All ten leg agents run **Opus 5 at high effort** in isolated git worktrees. There are no
Sonnet legs; Sonnet's role is the orchestrator session itself.

## 3. File ownership (collision avoidance)

Parallel agents never edit the same file. Ownership is **per brief, declared at planning
time**: every brief lists the exact files it owns, the orchestrator keeps a ledger across
the ten live legs, and a replacement brief that overlaps a live leg's set goes back to the
planner. Standing rules on top of the ledger:

- **Critical-path slot only:** `experiments/JOURNAL.md`, `PHASE2_P2_NOTES.md`,
  `plan_of_record.py`, `CONTINUATION_PROMPT.md`, `capabilities.py`, and the leg's own new
  files. No other slot may touch these; findings from other legs that belong in the
  journal go in their leg report and the run report, and the *next* critical-path leg
  carries them forward.
- **Verification briefs:** new files under `writeup/` named `VERIFY_*.md` plus their own
  re-run scripts in `experiments/`. A verification leg edits nothing it is verifying.
- **Literature briefs:** `LITERATURE_CHECK.md` (append-only sections) and new `writeup/`
  docs.
- **Reproducibility briefs:** `writeup/build_figures.py`, `writeup/figures/`, evidence
  scripts — *mechanics only*; any change that would alter a number in prose is a report,
  not an edit.
- **Docs briefs:** `writeup/INDEX.md`, `README.md`, link fixes in existing docs (never
  numeric content), `reports/`.
- **Prep briefs:** the specific solver/test files the brick names (currently
  `solver/weight_search.py`, `test_weight_search.py`) and their own writeup quartet.

`.claude/settings.json` and `scripts/` are orchestrator-owned; agents propose changes in
their leg reports instead of editing them.

**Preflight (user, once):** for the hands-off pool to run unprompted, the project
allowlist needs these entries alongside the existing ones — adding them is a settings
change Claude cannot make for you:
`"Bash(scripts/merge_gate.sh:*)"`, `"Bash(./scripts/merge_gate.sh:*)"`,
`"Bash(git merge:*)"`, `"Bash(git rebase:*)"`, `"Bash(git worktree:*)"`,
`"Bash(git push:*)"`, `"Bash(claude:*)"`.

## 4. The documentation contract (why this file exists at all)

**Every finding ships as a full quartet before its leg pushes — including, especially,
negative results.** The banked convention is `writeup/4_p2_lottery/`:

1. a runner in `experiments/` that produced the numbers (e.g. `p2_route_t_v1_border.py`),
2. curated data in `writeup/data/*.json` — every number quoted in prose must be in the JSON,
3. `BLOG_*.md` **and** `TECHNICAL_*.md` in the relevant `writeup/` subdirectory (the merge
   gate rejects one without the other), plus an `*_evidence.py` script that rebuilds the
   figures/claims from the curated JSON without re-running anything,
4. a figure registered in `writeup/build_figures.py`.

A result that exists only in a leg report, a chat transcript, or a terminal scroll does not
exist. "The negative construction stays in the artifact" (lesson 76) applies to prose:
what was tried and failed is written up with the same care as what worked.

## 5. Branch and push policy (hands-off by default)

- Branch names: `leg/<short-slug>`, e.g. `leg/tc-v1`, `leg/verify-leg52-headline`. Each
  leg agent commits to its branch in its worktree.
- **The leg agent pushes to `main` itself, without human approval, when:**
  1. its quartet is complete (§4),
  2. it has rebased onto the live `origin/main`, and
  3. `scripts/merge_gate.sh origin/main` prints `MERGE GATE: PASS` on the rebased branch.
  On a non-fast-forward rejection (another leg landed first) it re-fetches, re-rebases,
  re-gates, and pushes again until it lands. A failing gate is fixed in the worktree;
  a failing branch is never pushed.
- After the push lands, the agent reports its one-line finding and is **terminated**; the
  orchestrator refills the slot via a fresh planner pass against the new `main` (§2).
- Claim-bearing legs land without pre-push review; the compensating control is the rolling
  **verification brief** (§2) — the planner keeps one live whenever a claim-bearing leg
  has landed unreviewed, and a verification finding that contradicts a landed claim goes
  to the top of the report and into the next critical-path brief.
- Conflicting claims between two legs → a verification brief adjudicates on the evidence;
  the run report records the dispute and the resolution.

**Never pushed, ever, without the user** (the only escalations left):
- a change to `plan_of_record.py` other than the one the current gate's pre-committed
  YES/NO branch prescribes;
- lifting or weakening any ban other than via its recorded lift condition;
- any prose claiming movement on the Clay chain or odds better than the recorded ~0.05%;
- deleting or rewriting banked results in `writeup/`.

A leg that lands in one of these parks its branch **unpushed**, the orchestrator flags it
at the top of the report, and the slot refills. Everything else pushes the same run.

## 6. The run report

At close, the orchestrator commits `reports/REPORT_<YYYY-MM-DD>.md` to `main`:

- one row per completed leg: brief, outcome in one sentence, claim-bearing or mechanical,
  pushed / parked / failed;
- the critical-path leg's gate answer, verbatim in the pre-committed YES/NO form;
- what verification briefs contested and how each resolved;
- anything parked for the user (§5), at the top, not buried;
- the proposed direction for the next run's first wave, derived from the new
  `plan_of_record.py` state — so the next orchestrator session starts warm.

The report is a summary with links; the findings themselves live in the quartets (§4).
