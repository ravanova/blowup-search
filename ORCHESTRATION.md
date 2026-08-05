# Orchestration playbook — multi-agent days on this repo

**How this is used:** the user pastes [ORCHESTRATOR_PROMPT.md](ORCHESTRATOR_PROMPT.md) into a
fresh Claude session. That session is the **orchestrator**: it dispatches the agents defined
here, tracks them, merges their work to `main` unattended, and files a daily report. This
file is the durable contract the prompt points at, so the prompt stays short and this stays
versioned.

The orchestrator does **no mathematics itself**. Its job is dispatch, collision avoidance,
gate-keeping, and honest reporting.

---

## 1. Inherited law (nothing here overrides it)

1. **`plan_of_record.py` is the plan.** Run `.venv/bin/python plan_of_record.py` for the
   current stage, its pre-committed gate, and the live bans. `test_plan_of_record.py` fails
   if the plan, [CONTINUATION_PROMPT.md](CONTINUATION_PROMPT.md) and
   [CLAY_ROADMAP.md](CLAY_ROADMAP.md) disagree — the merge gate runs it on every merge.
2. **Bans are machine-readable and agents inherit all of them.** A ban is lifted only by the
   lift condition it names, never by an agent's judgement.
3. **One leg per day on the critical path.** The stage the plan marks `NEXT` is a single
   leg, executed by a single agent, with the gate answered exactly as pre-committed (both
   outcomes are already written down; the agent's job is to find out which one happened).
4. **The standing discipline in CONTINUATION_PROMPT.md** (gate the operator, magnitudes not
   booleans, name the realization, novelty pass before construction, negative controls that
   can fail, lesson 88, …) applies to every agent, not just the leg agent.
5. **Walls 1 and 2 stand.** No agent output is ever summarised as movement toward Clay
   unless a link of the L1→L4 chain actually moved, which has not happened in 52 legs.

## 2. The default six-agent split

| # | Codename | Lane | Model | Branch prefix | Task |
|---|----------|------|-------|---------------|------|
| 1 | **LEG** | local worktree | Opus, high effort | `leg/` | Execute the stage marked `NEXT` in `plan_of_record.py`, exactly as CONTINUATION_PROMPT.md directs, including its own novelty pass (query log committed to [LITERATURE_CHECK.md](LITERATURE_CHECK.md)) *before* construction. Owns the shared-state files (§3). |
| 2 | **VERIFIER** | local worktree | Opus, high effort | `verify/` | Re-measure the previous leg's headline before LEG builds on it (lesson 85): re-run its runner, check every number in its BLOG/TECHNICAL prose against its `writeup/data/*.json`, re-run its negative controls. **Report gaps, do not repair.** Then line-by-line review of LEG's PR before it merges. |
| 3 | **LIT** | cloud | Sonnet | `lit/` | The open literature items the plan records (currently: the arXiv:2604.01868 resurfacing flag; whether Breden–Desvillettes–Lessard arXiv:1503.06315 covers a zero-diagonal Fredholm operator). Fetch via `scripts/fetch_papers.sh` (cloud: allowlist `arxiv.org` first; try ar5iv HTML when a PDF fails to extract). Append query logs to LITERATURE_CHECK.md. |
| 4 | **REPRO** | cloud | Sonnet | `repro/` | Mechanical reproducibility: run every `test_*.py` at the repo root and report failures; regenerate figures via `writeup/build_figures.py` from `writeup/data/` and flag any that changed; run the `writeup/*/\*_evidence.py` scripts on the fresh clone and confirm they rebuild without re-runs. Fix *scripts*; never touch claims — a prose/JSON discrepancy is reported, not repaired. |
| 5 | **DOCS** | cloud | Sonnet | `docs/` | The writeup tree's health: maintain `writeup/INDEX.md` (one line per leg: route, gate answer, links to BLOG/TECHNICAL/data/figure); check every route has the full quartet (§4) and list gaps; fix dead links; keep the root `README.md` orientation current. Reviews LEG's BLOG/TECHNICAL for the docs contract before merge. |
| 6 | **PREP** | local worktree or cloud | Sonnet | `prep/` | The best plan-consistent parallel brick that is *not* the critical path. Currently: implement the two named repairs from the C-PILOT leg ([writeup/4_p2_lottery/TECHNICAL_P2_ROUTEC_PILOT_V0.md](writeup/4_p2_lottery/TECHNICAL_P2_ROUTEC_PILOT_V0.md) §4 — P2 and P3 failed) in `solver/weight_search.py`, then re-run the six-property viability gate. That re-run is the *only* recorded lift path for the GA-compute ban — and even a 6/6 pass does **not** authorize GA compute the same day; it is recorded for the next planning pass. |

Re-derive this table each day from the repo state before dispatching — the codenames and
lanes are stable, the concrete tasks follow the plan of record. If a lane is unavailable
(no cloud access, say), collapse it into a local worktree agent rather than dropping the task.

## 3. File ownership (collision avoidance)

Parallel agents never edit the same file. Ownership:

- **LEG only:** `experiments/JOURNAL.md`, `PHASE2_P2_NOTES.md`, `plan_of_record.py`,
  `CONTINUATION_PROMPT.md`, `capabilities.py`, and the leg's own new files. No other agent
  may touch these; findings from other agents that belong in the journal go in their PR
  description and the daily report, and the *next* leg carries them forward.
- **VERIFIER:** new files under `writeup/` named `VERIFY_*.md` plus its own re-run scripts
  in `experiments/`. It edits nothing it is verifying.
- **LIT:** `LITERATURE_CHECK.md` (append-only sections) and new `writeup/` docs.
- **REPRO:** `writeup/build_figures.py`, `writeup/figures/`, evidence scripts — *mechanics
  only*; any change that would alter a number in prose is a report, not an edit.
- **DOCS:** `writeup/INDEX.md`, `README.md`, link fixes in existing docs (never numeric
  content), `reports/`.
- **PREP:** the specific solver/test files its brick names (currently
  `solver/weight_search.py`, `test_weight_search.py`) and its own writeup quartet.

`.claude/settings.json` and `scripts/` are orchestrator-owned; agents propose changes in PR
descriptions instead of editing them.

**Preflight (user, once):** for the hands-off merge flow to run unprompted, the project
allowlist needs these entries alongside the existing ones — adding them is a settings change
Claude cannot make for you:
`"Bash(scripts/merge_gate.sh:*)"`, `"Bash(./scripts/merge_gate.sh:*)"`,
`"Bash(git merge:*)"`, `"Bash(git rebase:*)"`, `"Bash(git worktree:*)"`, `"Bash(claude:*)"`.

## 4. The documentation contract (why this file exists at all)

**Every finding ships as a full quartet before the day closes — including, especially,
negative results.** The banked convention is `writeup/4_p2_lottery/`:

1. a runner in `experiments/` that produced the numbers (e.g. `p2_route_t_v1_border.py`),
2. curated data in `writeup/data/*.json` — every number quoted in prose must be in the JSON,
3. `BLOG_*.md` **and** `TECHNICAL_*.md` in the relevant `writeup/` subdirectory (the merge
   gate rejects one without the other), plus an `*_evidence.py` script that rebuilds the
   figures/claims from the curated JSON without re-running anything,
4. a figure registered in `writeup/build_figures.py`.

A result that exists only in a PR body, a chat transcript, or a terminal scroll does not
exist. "The negative construction stays in the artifact" (lesson 76) applies to prose:
what was tried and failed is written up with the same care as what worked.

## 5. Branch, PR and merge policy (hands-off by default)

- Branch names: `<prefix><short-slug>`, e.g. `leg/tc-v1`, `verify/leg52-headline`.
  Worktree agents commit to their branch and push; cloud sessions open PRs as usual.
- Every PR description states up front: **claim-bearing** (touches a mathematical claim,
  a gate answer, or any number in prose) or **mechanical** (scripts, figures, links,
  index, infrastructure).
- **The orchestrator merges to `main` without human approval when:**
  1. `scripts/merge_gate.sh origin/main` prints `MERGE GATE: PASS` on the branch, and
  2. for **claim-bearing** PRs only: VERIFIER has reviewed it and its review found no
     unresolved gap (DOCS additionally checks the quartet is complete).
- Merge order: mechanical PRs merge as they turn green; **LEG's PR merges last**, rebased
  on the day's main, so the drift detector runs against the final state.
- Conflicting claims between two PRs → VERIFIER adjudicates on the evidence; the
  orchestrator merges the survivor and records the dispute in the daily report.

**Never merged, ever, without the user** (the only escalations left):
- a change to `plan_of_record.py` other than the one the current gate's pre-committed
  YES/NO branch prescribes;
- lifting or weakening any ban other than via its recorded lift condition;
- any prose claiming movement on the Clay chain or odds better than the recorded ~0.05%;
- deleting or rewriting banked results in `writeup/`.

These are parked as open PRs, flagged at the top of the daily report, and left for the user.
Everything else merges the same day.

## 6. The daily report

At close, the orchestrator commits `reports/REPORT_<YYYY-MM-DD>.md` to `main`:

- one row per agent: task, outcome in one sentence, claim-bearing or mechanical,
  merged / parked / failed;
- the leg's gate answer, verbatim in the pre-committed YES/NO form;
- what VERIFIER contested and how it resolved;
- anything parked for the user (§5), at the top, not buried;
- a proposed six-agent split for the next day, derived from the new `plan_of_record.py`
  state — so the next orchestrator session starts warm.

The report is a summary with links; the findings themselves live in the quartets (§4).
