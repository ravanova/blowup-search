# Orchestration playbook — continuous four-leg operation

## How to start a run

**Paste the full text of [ORCHESTRATOR_PROMPT.md](ORCHESTRATOR_PROMPT.md) — and nothing else —
into a fresh Claude Code session set to Sonnet 5, in this repository.** That session becomes
the **orchestrator**: it dispatches the agents defined here, keeps four legs running in
parallel, merges their work to `main` unattended, writes a live progress file the user can
read at any time, and hands off to a fresh orchestrator session before its own context runs
out.

Three things make that paste work, and breaking any of them brings back the failure where the
session answers "I don't see a request yet":

1. **`ORCHESTRATOR_PROMPT.md` contains no framing *about* itself.** It opens in the second
   person, tells the session to start at Step 0 immediately, and ends telling it to begin. It
   carries no title naming it a prompt, no "written for…" note, and no maintenance footer — a
   pasted document that describes itself is read as a document, and the correct response to a
   document is to ask what to do with it. **Usage notes about the prompt live here, in this
   file, never in the prompt.**
2. **Paste the contents, not the path.** A session handed `ORCHESTRATOR_PROMPT.md` as a
   filename has been given a reading suggestion, not an instruction.
3. **Do not paste it together with a question.** Any accompanying text becomes the actual
   request and the run does not start.

The file-role split, which the rest of this document assumes:

| File | Role | Addressed to |
|---|---|---|
| [ORCHESTRATOR_PROMPT.md](ORCHESTRATOR_PROMPT.md) | **The paste-able prompt.** Pure instruction, start to finish. | the orchestrator session |
| `ORCHESTRATION.md` (this file) | **The contract.** How the run is shaped, who owns what, what the rules are. | humans, and agents reading for reference |
| [CONTINUATION_PROMPT.md](CONTINUATION_PROMPT.md) | The critical-path leg's directive and the standing discipline. | leg agents |
| [DIRECTION.md](DIRECTION.md) | The leg queue and live slot assignments. | the Decision Maker (sole writer) |
| [reports/ORCH_STATE.md](reports/ORCH_STATE.md) | Handoff state between orchestrator sessions. | the next orchestrator |

---

## What the run is

The orchestrator does **no mathematics itself**. Its job is dispatch, collision avoidance,
gate-keeping, integration, and honest reporting. Direction is the **Decision Maker's** job
(§3), not the orchestrator's.

This is not a "day" contract any more. **Work is continuous.** Legs open and close
independently; the queue refills from [DIRECTION.md](DIRECTION.md); the run ends when the
user stops it (§9) or the direction genuinely runs out.

---

## 1. Inherited law (nothing here overrides it)

1. **`plan_of_record.py` is the plan.** Run `.venv/bin/python plan_of_record.py` for the
   committed sequence, the stage marked `NEXT`, its pre-committed gate, and the live bans.
   `test_plan_of_record.py` fails if the plan, [CONTINUATION_PROMPT.md](CONTINUATION_PROMPT.md)
   and [CLAY_ROADMAP.md](CLAY_ROADMAP.md) disagree — the merge gate runs it on every merge.
2. **Bans are machine-readable and every agent inherits all of them.** A ban is lifted only
   by the lift condition it names, never by an agent's judgement, never by the Decision Maker.
3. **Exactly one stage is `NEXT`, and that invariant is load-bearing.** Parallel legs do
   **not** each claim a stage. One leg is the critical path (the stage marked `NEXT`); the
   other three are exploration legs from the Decision Maker's queue in `DIRECTION.md`. Only
   promoting a route into `plan_of_record.py`'s committed sequence touches the plan, and that
   is an escalation (§8).
4. **The standing discipline in CONTINUATION_PROMPT.md** (gate the operator, magnitudes not
   booleans, name the realization, novelty pass before construction, negative controls that
   can fail, lessons 84–90) applies to every agent, on every leg, critical path or not.
5. **Walls 1 and 2 stand.** No agent output, no progress file, no report is ever summarised
   as movement toward Clay unless a link of the L1→L4 chain actually moved — which has not
   happened in 53 legs. Ordering the queue by proximity to the chain (§3) is a *choice of
   what to try*, never a claim about what happened.

## 2. Shape of the run

Four legs live at all times. Each leg is **one agent, end to end** — its own novelty pass,
its own construction, its own measurement, its own gate answer, its own quartet (§6). One
verifier is paired to each leg. Everything else is repo-wide support that serves all four.

The four legs must pursue **different ideas or different directions**, chosen so they do not
depend on each other's results and do not touch each other's files. That independence is the
Decision Maker's responsibility to design and the orchestrator's to enforce (§5).

**Do not shard a leg.** Splitting one leg across several agents was measured on 2026-08-05 to
be slower *and* more expensive than one agent doing the whole thing. One agent per leg is the
default; the one deliberate exception is the sharding control arm in §10.

## 3. The Decision Maker (DM)

**One extra agent, Opus 5, outside the 24-slot pool.** The DM decides *what to work on*; the
orchestrator decides *how it lands*. The orchestrator never invents a leg.

The DM owns [DIRECTION.md](DIRECTION.md) and nothing else. That file is its durable state, so
a bloated DM can be discarded and recreated cheaply from it. DIRECTION.md carries:

- **the leg queue** — ranked candidate legs, each with a route name, a one-paragraph thesis,
  a **pre-committed gate naming both branches**, and its **file territory** (§5);
- **live assignments** — which leg number and route each of the four leg slots holds;
- **the ranking rationale** — why this order, refreshed whenever a gate answers;
- **open direction questions** — things the DM wants the user to decide (these also surface
  in the progress file, §7).

**Queue ranking.** Prefer, in this order: (a) a leg that could actually move a link of the
L1→L4 chain; (b) a leg whose gate can answer either way within a leg's work; (c) a leg
independent of the other three. A leg with no pre-committed failure branch is not a leg.

**Steering.** When the user gives the orchestrator input — a change of direction, a review of
goals, a new priority — the orchestrator forwards it **verbatim** to the DM via `SendMessage`
and asks for a revised queue. The orchestrator does not interpret the steer itself.

The DM may reason mathematically about direction. It may not build, measure, or write up.

## 4. The 24-slot roster

| Band | Slots | Model | Lane | Branch prefix | Role |
|---|---|---|---|---|---|
| **LEG-A…D** | 4 | Opus, high effort | local worktree | `leg/<N>-<slug>` | One whole leg each, end to end: novelty pass → construction → measurement → gate answer → full quartet. Owns only its own files (§5). |
| **VER-A…D** | 4 | Opus, high effort | local worktree | `verify/<N>-<slug>` | Paired 1:1 to a leg. Re-measure any prior headline that leg *consumes* (lesson 85) **before** it builds on it; then line-by-line review of the leg's PR. **Reports gaps, does not repair.** Spawned when its leg has something to verify, not idle-running. |
| **LIT-1,2** | 2 | Sonnet | cloud or local | `lit/<N>-<slug>` | Standing literature flags, and deep dives a leg requests. A leg's *own* novelty pass stays with the leg — LIT does not replace it. |
| **REPRO-1,2** | 2 | Sonnet | cloud or local | `repro/<N>-<slug>` | Mechanical reproducibility: every root `test_*.py` **with `.venv/bin/python`**, raw per-file pass/fail counts (never a rolled-up summary); figures via `writeup/build_figures.py`; `*_evidence.py` scripts rebuild without re-runs. Fixes *scripts*; a prose/JSON discrepancy is reported, never repaired. |
| **DOCS-1,2** | 2 | Sonnet | cloud or local | `docs/<N>-<slug>` | `writeup/INDEX.md`, quartet-completeness audit, dead links, `README.md`, `writeup/README.md` index. Checks each leg's BLOG/TECHNICAL against the docs contract before merge. |
| **PREP-1,2** | 2 | Sonnet | cloud or local | `prep/<N>-<slug>` | Plan-consistent bricks that are not on any leg's critical path. |
| **BENCH** | 8 | assigned | assigned | assigned | Unassigned capacity. |

**Bench priority, in this order:**
1. **Refill a leg slot the moment one closes** — four legs live is the target, not a ceiling
   reached once.
2. **Repair work integration found.** A failing gate, a broken test on `main`, a bug an agent
   tripped over: spawn a bench agent to fix it. Issues get *worked*, not queued.
3. **A fifth+ parallel route** from the DM's queue, if every other slot is saturated and the
   queue has a ready, independent item.

Never exceed 24 concurrent workers plus the DM. Steady state is ~12–16; the headroom is what
makes "assign an idle agent to a new leg" possible without starving verification.

**Context hygiene.** Agents are cheap to recreate and expensive to keep talking to.
- `SendMessage` for **at most 3 follow-ups** to the same agent. Past that, recreate with a
  written brief instead.
- **Always recreate at a leg boundary.** A leg agent that has answered its gate never gets
  the next leg — spawn a fresh one.
- **Support agents are recreated per cycle**, not continued; their tasks are independent.
- Subagents cannot be `/clear`ed. Recreating *is* the clear.

## 5. Collision avoidance under four parallel legs

Parallel agents never edit the same file. Two mechanisms:

### 5a. The shared ledgers are integration-owned

These five files are edited **only by the orchestrator**, in one integration commit per
cycle. No leg, no verifier, no support agent touches them:

| File | How content gets in |
|---|---|
| `plan_of_record.py` | Orchestrator applies the gate's own pre-committed branch. Anything else is escalation §8. |
| `CONTINUATION_PROMPT.md` | Orchestrator, in step with the plan. Budget: ≤400 lines, ≤2 session-close blocks (`test_plan_of_record.py` test 8 enforces it). |
| `experiments/JOURNAL.md` | Each leg writes `experiments/journal/leg_<N>.md`; the orchestrator adds a one-line pointer. |
| `PHASE2_P2_NOTES.md` | Frozen for agents. Orchestrator appends one pointer block per merged leg. |
| `LITERATURE_CHECK.md` | Each leg/LIT writes `writeup/novelty/leg_<N>.md`; the orchestrator adds a one-line pointer. |

This is what makes four-way parallelism possible at all: the four files that every leg used
to want to append to are now written once, by one writer, after the merges.

`capabilities.py` is the exception agents may touch: **append** an entry at the end of your
own object's section, never reorder. `test_capabilities.py` runs on every merge.

`.claude/settings.json` and `scripts/` are orchestrator-owned; agents propose changes in PR
descriptions.

### 5b. Every leg declares a file territory before it starts

The DM assigns each queued leg an explicit, disjoint territory in `DIRECTION.md`: the
`experiments/` runners, `solver/` modules, `test_*.py`, `writeup/` subdirectory, and
`writeup/data/*.json` it may create or edit. New leg code goes in `experiments/leg<N>_*.py`
unless the territory says otherwise.

**The orchestrator refuses to dispatch a leg whose territory overlaps a live leg's.** If two
queued routes want the same `solver/` module, they are not parallel — send one back to the DM
to re-cut or re-order.

Territories are checked again at merge: a diff outside the declared territory is a gate
failure, sent back to the owning agent.

## 6. The documentation contract

**Every finding ships as a full quartet before its leg closes — including, especially,
negative results.** The banked convention is `writeup/4_p2_lottery/`:

1. a runner in `experiments/` that produced the numbers,
2. curated data in `writeup/data/*.json` — every number quoted in prose must be in the JSON,
3. `BLOG_*.md` **and** `TECHNICAL_*.md` in the relevant `writeup/` subdirectory (the merge
   gate rejects one without the other), plus an `*_evidence.py` script that rebuilds the
   figures/claims from the curated JSON without re-running anything,
4. a figure registered in `writeup/build_figures.py`.

A result that exists only in a PR body, a chat transcript, or a terminal scroll does not
exist. "The negative construction stays in the artifact" (lesson 76) applies to prose: what
was tried and failed is written up with the same care as what worked.

## 7. Commits, branches, and the merge policy

### 7a. Commit message convention — every commit names its leg

```
Leg <N>: <ROLE> — <what changed>
```

- `<N>` is the leg number the work serves. **`Leg 0:`** for repo-wide work that serves no
  single leg (infrastructure, orchestration, cross-cutting docs, the daily report).
- `<ROLE>` is one of `LEG`, `VERIFY`, `LIT`, `REPRO`, `DOCS`, `PREP`, `ORCH`, `DM`.
- Merge commits: `Leg <N>: merge <branch> — <one-line outcome>`.

Examples: `Leg 54: LEG — non-block-diagonal A, gate answers NO`,
`Leg 54: VERIFY — re-derived the K² closed form independently`,
`Leg 0: ORCH — integration cycle 7, plan updated for MM's NO branch`.

Branches follow the same numbering: `leg/54-mm-v1`, `verify/54-mm-review`, `docs/0-index`.

### 7b. Merge policy (hands-off by default)

The orchestrator merges to `main` without human approval when:

1. `scripts/merge_gate.sh origin/main` prints `MERGE GATE: PASS` on the branch, **and**
2. the diff stays inside the branch's declared territory (§5b), **and**
3. for **claim-bearing** PRs only: the paired verifier has reviewed it and found no
   unresolved gap (DOCS additionally confirms the quartet is complete).

Every PR description states up front: **claim-bearing** (touches a mathematical claim, a gate
answer, or any number in prose) or **mechanical** (scripts, figures, links, index,
infrastructure).

**Merge order under parallelism:** first ready, first merged. There is no "leg merges last"
any more — with disjoint territories there is nothing to be last for. Every branch still open
after a merge **rebases on the new `main` and re-gates** before its own turn.

**FAIL** → send the gate output back to the owning agent; it fixes, you re-gate. If the
owning agent is gone, spawn a bench agent with the branch and the gate output.

Conflicting claims between two legs → the verifiers adjudicate on the evidence; the
orchestrator merges the survivor and records the dispute in the progress file and the report.

## 8. The four escalations (unchanged, and still the only ones)

**Never merged without the user:**

- a change to `plan_of_record.py` other than the one the current gate's pre-committed YES/NO
  branch prescribes — *including promoting an exploration route into the committed sequence*;
- lifting or weakening any ban other than via its recorded lift condition;
- any prose claiming movement on the Clay chain, or odds better than the recorded ~0.05%;
- deleting or rewriting banked results in `writeup/`.

These are parked as open PRs, listed at the **top** of `PROGRESS.md` under `⚠ NEEDS YOU`, and
left for the user. **Work does not stop for them** — the orchestrator parks the item and keeps
every other leg moving. Everything else merges as it turns green.

Anything else that genuinely needs a human decision goes in the same `⚠ NEEDS YOU` section
with the exact question and the options, and the run continues around it.

## 9. The progress file, the report, and stopping

### 9a. `PROGRESS.md` — the live dashboard (git-ignored, never committed)

Rewritten **every integration cycle, and at minimum every ~10 minutes**, so the user can read
it at any time without asking. Sections, in this order:

1. `## ⚠ NEEDS YOU` — numbered, exact question, options, what is blocked and what is not.
   Say "nothing" when there is nothing; never omit the heading.
2. `## Now` — timestamp, cycle number, `main` SHA, stop-file status, agents live / 24.
3. `## Legs` — one row per live leg: number, route, agent, branch, phase
   (`novelty` → `build` → `measure` → `writeup` → `verify` → `gating` → `merged`), started,
   last event.
4. `## Support` — one row per live support agent.
5. `## Landed` — merged commits since the last report, one line each.
6. `## Queue` — the next legs from `DIRECTION.md`.
7. `## Stop` — the three stop files, restated every time.

Because it is git-ignored it never churns `main`. Whenever the orchestrator merges anything it
also refreshes `reports/STATUS.md` — a committed snapshot of sections 1–3 — so the same view is
readable from a cloud or mobile session.

### 9b. `reports/REPORT_<YYYY-MM-DD>.md` — the durable record (committed)

At each date boundary, and at any stop: one row per agent (task, one-sentence outcome,
claim-bearing or mechanical, merged/parked/failed); each leg's gate answer **verbatim in its
pre-committed wording**; what the verifiers contested and how it resolved; everything parked
for the user, at the top; the sharding-experiment ledger (§10); and the state of the queue.

The report is a summary with links; the findings live in the quartets (§6).

### 9c. Stopping the run

The orchestrator checks for these files **at the top of every cycle**. All three are
git-ignored.

| File | Effect |
|---|---|
| `touch PAUSE` | Stop dispatching new legs. Keep integrating, verifying, and merging what is already in flight. Delete the file to resume. |
| `touch STOP` | **Graceful.** Stop dispatching. Let in-flight agents finish, gate and merge what lands, write `PROGRESS.md` + the report + `reports/ORCH_STATE.md`, then exit. |
| `touch STOP-NOW` | **Hard.** `TaskStop` every agent immediately. Merge nothing further. Write `PROGRESS.md` + the report naming every abandoned branch and what was lost, then exit. |

The user typing "stop" / "pause" in chat means the same thing and takes effect immediately.

### 9d. Handing off before the orchestrator's own context runs out

The orchestrator cannot measure its own context, so it uses proxies: **after 12 integration
cycles, or the first time it notices its context has been summarised, it hands off** —
whichever comes first.

Handoff is: write and commit `reports/ORCH_STATE.md` (cycle count, `main` SHA, every live
agent with its leg number and branch, the queue, in-flight PRs, open escalations, the sharding
ledger, and what the next orchestrator must do first), refresh `PROGRESS.md`, print the resume
instruction, and exit.

**Be honest about what a handoff costs.** Subagent handles do not survive the session that
spawned them — a fresh orchestrator cannot `SendMessage` the old agents. That is exactly why
`ORCH_STATE.md` records **branches, not handles**: the new session gates and merges whatever
the abandoned branches contain, and re-spawns a fresh agent for any leg that was mid-flight.
Record in `ORCH_STATE.md` which legs were interrupted and how far they got.

## 10. The sharding experiment (run it once, then stop)

The 2026-08-05 day suggested sharding a leg across agents cost more and took longer. Test it
on the first four parallel legs rather than arguing about it:

- **LEG-A, LEG-B, LEG-C: unsharded.** One agent, whole leg. This is the default and the
  hypothesis.
- **LEG-D: the control arm, sharded** into leg agent + one dedicated support agent for its
  construction, as the old contract did.
- **Pre-register before dispatch:** the DM records each leg's difficulty class
  (`light` / `standard` / `heavy`) in `DIRECTION.md` *before* any agent starts. Without this
  the comparison is worthless, because leg difficulty is the obvious confound.
- **Measure, per leg:** wall-clock dispatch → merged; number of agent invocations plus
  follow-up messages; rework rounds (times a branch failed the gate or a review and came back).
- **Write it up** in `reports/EXPERIMENT_SHARDING.md`, and state plainly that this is n=3 vs
  n=1 on legs of unequal difficulty — suggestive, not a measurement. If the unsharded arm
  wins, drop the control and never shard again; record that in this file.

---

*Maintained in-repo so cloud agents read the same contract. Update this file and
[ORCHESTRATOR_PROMPT.md](ORCHESTRATOR_PROMPT.md) together — but keep the split: rules and
usage notes belong **here**, and the prompt stays pure instruction with nothing in it that
describes itself (see "How to start a run" above).*
