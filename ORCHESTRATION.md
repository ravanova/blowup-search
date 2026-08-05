# Orchestration playbook — continuous ten-leg operation

## How to start a run

**Paste the full text of [ORCHESTRATOR_PROMPT.md](ORCHESTRATOR_PROMPT.md) — and nothing else —
into a fresh Claude Code session set to Sonnet 5, in this repository.** That session becomes
the **orchestrator**: it dispatches the agents defined here, keeps ten legs running in
parallel, audits the legs' own pushes to `main` and merges the support work unattended,
writes a live progress file the user can read at any time, and hands off to a fresh
orchestrator session before its own context runs out.

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
   other nine are exploration legs from the Decision Maker's queue in `DIRECTION.md`. Only
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

Ten legs live at all times. Each leg is **one Opus 5 agent, end to end** — its own novelty
pass, its own construction, its own measurement, its own gate answer, its own quartet (§6),
and **its own push to `main`** (§7b). When its push lands the agent is terminated and a
fresh agent spawns into the slot on the next brief, so ten legs are always in progress.
One verifier is paired to each leg. Everything else is repo-wide support that serves all ten.

The ten legs must pursue **different ideas or different directions**, chosen so they do not
depend on each other's results and do not touch each other's files. That independence is the
Decision Maker's responsibility to design and the orchestrator's to enforce (§5).

**Do not shard a leg.** Splitting one leg across several agents was measured on 2026-08-05 to
be slower *and* more expensive than one agent doing the whole thing. One agent per leg is the
default; the one deliberate exception is the sharding control arm in §10.

## 3. The Decision Maker (DM)

**One extra agent, Fable 5, outside the 32-slot pool.** The DM decides *what to work on*; the
orchestrator decides *how it lands*. The orchestrator never invents a leg — and when the plan
and the queue leave the next leg genuinely unclear, **the DM chooses the work**. That mandate
is the DM's alone; an empty leg slot is never the answer.

The DM owns [DIRECTION.md](DIRECTION.md) and nothing else. That file is its durable state, so
a bloated DM can be discarded and recreated cheaply from it. DIRECTION.md carries:

- **the leg queue** — ranked candidate legs, each with a route name, a one-paragraph thesis,
  a **pre-committed gate naming both branches**, and its **file territory** (§5);
- **live assignments** — which leg number and route each of the ten leg slots holds;
- **the ranking rationale** — why this order, refreshed whenever a gate answers;
- **open direction questions** — resolved by the DM itself under the standing directive
  (§8) wherever possible; only a question the directive genuinely cannot answer surfaces
  for the user (via the progress file, §9a), with the DM's note on why it could not decide.

**Queue ranking.** Prefer, in this order: (a) a leg that could actually move a link of the
L1→L4 chain; (b) a leg whose gate can answer either way within a leg's work; (c) a leg
independent of the other nine. A leg with no pre-committed failure branch is not a leg.

**Steering.** When the user gives the orchestrator input — a change of direction, a review of
goals, a new priority — the orchestrator forwards it **verbatim** to the DM via `SendMessage`
and asks for a revised queue. The orchestrator does not interpret the steer itself.

The DM may reason mathematically about direction. It may not build, measure, or write up.

## 4. The 32-slot roster

| Band | Slots | Model | Lane | Branch prefix | Role |
|---|---|---|---|---|---|
| **LEG-A…J** | 10 | Opus, high effort | local worktree | `leg/<N>-<slug>` | One whole leg each, end to end: novelty pass → construction → measurement → gate answer → full quartet → **its own rebase, gate, and push to `main`** (§7b). Owns only its own files (§5). Terminated once its push lands; the slot refills with a fresh agent. |
| **VER-A…J** | 10 | Opus, high effort | local worktree | `verify/<N>-<slug>` | Paired 1:1 to a leg. Re-measure any prior headline that leg *consumes* (lesson 85) **before** it builds on it; then line-by-line review of the leg's landing on `main`, after the fact. **Reports gaps, does not repair.** Spawned when its leg has something to verify, not idle-running. |
| **LIT-1,2** | 2 | Sonnet | cloud or local | `lit/<N>-<slug>` | Standing literature flags, and deep dives a leg requests. A leg's *own* novelty pass stays with the leg — LIT does not replace it. |
| **REPRO-1,2** | 2 | Sonnet | cloud or local | `repro/<N>-<slug>` | Mechanical reproducibility: every root `test_*.py` **with `.venv/bin/python`**, raw per-file pass/fail counts (never a rolled-up summary); figures via `writeup/build_figures.py`; `*_evidence.py` scripts rebuild without re-runs. Fixes *scripts*; a prose/JSON discrepancy is reported, never repaired. |
| **DOCS-1,2** | 2 | Sonnet | cloud or local | `docs/<N>-<slug>` | `writeup/INDEX.md`, quartet-completeness audit, dead links, `README.md`, `writeup/README.md` index. Checks each leg's BLOG/TECHNICAL against the docs contract before merge. |
| **PREP-1,2** | 2 | Sonnet | cloud or local | `prep/<N>-<slug>` | Plan-consistent bricks that are not on any leg's critical path. |
| **BENCH** | 4 | assigned | assigned | assigned | Unassigned capacity. |

**Bench priority, in this order:**
1. **Refill a leg slot the moment one closes** — ten legs live is the target, not a ceiling
   reached once. Refill is per-slot and immediate: terminate the finished agent, get the
   next brief from the DM, spawn fresh.
2. **Repair work integration found.** A failing gate, a broken test on `main`, a bug an agent
   tripped over: spawn a bench agent to fix it. Issues get *worked*, not queued.
3. **An eleventh+ parallel route** from the DM's queue, if every other slot is saturated and
   the queue has a ready, independent item.

Never exceed 32 concurrent workers plus the DM. Steady state is ~16–24; the headroom is what
makes "assign an idle agent to a new leg" possible without starving verification.

**Context hygiene.** Agents are cheap to recreate and expensive to keep talking to.
- `SendMessage` for **at most 3 follow-ups** to the same agent. Past that, recreate with a
  written brief instead.
- **Always recreate at a leg boundary.** A leg agent that has answered its gate never gets
  the next leg — spawn a fresh one.
- **Support agents are recreated per cycle**, not continued; their tasks are independent.
- Subagents cannot be `/clear`ed. Recreating *is* the clear.

## 5. Collision avoidance under ten parallel legs

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

This is what makes ten-way parallelism possible at all: the shared files that every leg used
to want to append to are now written once, by one writer, after the landings.

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

Territories are checked again at landing time: a leg checks its own diff before it pushes
(§7b), and the orchestrator audits every landing. For support branches, which the
orchestrator merges itself, a diff outside the declared territory is a gate failure sent
back to the owning agent.

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

### 7b. Landing policy (hands-off by default)

**Leg branches: the leg agent pushes to `main` itself.** No human approval, no orchestrator
merge. A leg's finish protocol, in order, none skippable:

1. quartet complete (§6), gate answered in its pre-committed wording;
2. `git diff --name-only` against the merge base confirms every path is inside the declared
   territory (§5b);
3. `git fetch origin main && git rebase origin/main`;
4. `scripts/merge_gate.sh origin/main` prints `MERGE GATE: PASS` on the rebased branch — a
   FAIL is fixed in the worktree and never pushed;
5. push to `main`; on a non-fast-forward rejection (another leg landed first), re-fetch,
   re-rebase, re-gate, and push again until it lands;
6. report the one-line finding and stop. The agent is terminated once its push lands and the
   slot refills with a fresh agent on a fresh brief — ten legs stay live.

An outcome that falls under an escalation (§8) is the one exception: the agent pushes its
*branch* only, never `main`, and reports it as parked.

**Claim-bearing legs land without pre-push review; the compensating control is post-landing
verification.** Every landing that touches a mathematical claim, a gate answer, or any number
in prose gets its paired verifier's line-by-line review on `main`, after the fact, plus a
DOCS quartet check. A confirmed gap becomes a **rework leg, not a user question**: the
orchestrator hands the verifier's finding to the DM, which cuts a correction leg at the top
of the queue — same territory as the flawed landing, gate pre-committed to the corrected
measurement — and it lands forward on `main` like any other leg (landed history is never
rewritten). The gap and its correction are recorded in the report. The one exception: a
correction that would delete or rewrite a banked result is escalation #4 and waits for the
user.

**Support branches (`verify/`, `lit/`, `repro/`, `docs/`, `prep/`): the orchestrator merges
them** when the gate prints PASS and the diff stays in territory. FAIL → gate output back to
the owning agent (or a bench agent if it is gone); it fixes, the orchestrator re-gates.
First ready, first merged; a support branch still open after a landing rebases on the new
`main` and re-gates before its own turn.

Every leg brief and support branch states up front: **claim-bearing** (touches a mathematical
claim, a gate answer, or any number in prose) or **mechanical** (scripts, figures, links,
index, infrastructure).

Conflicting claims between two legs → the verifiers adjudicate on the evidence; the
orchestrator records the dispute and its resolution in the progress file and the report.

## 8. The four escalations (unchanged, and still the only ones)

**Never merged without the user:**

- a change to `plan_of_record.py` other than the one the current gate's pre-committed YES/NO
  branch prescribes — *including promoting an exploration route into the committed sequence*;
- lifting or weakening any ban other than via its recorded lift condition;
- any prose claiming movement on the Clay chain, or odds better than the recorded ~0.05%;
- deleting or rewriting banked results in `writeup/`.

These are parked as pushed *branches* (never `main`), listed at the **top** of `PROGRESS.md`
under `⚠ NEEDS YOU`, and left for the user. **Work does not stop for them** — the orchestrator
parks the item, refills the slot, and keeps every other leg moving. Everything else lands as
it turns green.

**Everything short of these four is decided, not asked.** The user's standing answer is on
record:

> *Pursue the option that is best for the overall goal of pursuing a Clay solve, and the
> secondary goal of producing useful novel findings.*

Direction questions go to the DM, which decides under that directive; operational questions
the orchestrator decides the same way, and either records the decision and its reasoning in
the report. The directive governs **what to try, never what to claim** — the walls in §1
stand, and it lifts no ban and promotes no route into the plan (those remain escalations
above). Verification rework is a leg (§7b), not a question. `⚠ NEEDS YOU` is reserved for
the four escalations plus the rare question the standing directive genuinely cannot answer —
and such an entry states why the directive could not decide it, with the decider's
recommended option first.

## 9. The progress file, the report, and stopping

### 9a. `PROGRESS.md` — the live dashboard (git-ignored, never committed)

Rewritten **every integration cycle, and at minimum every ~10 minutes**, so the user can read
it at any time without asking. Sections, in this order:

1. `## ⚠ NEEDS YOU` — numbered, exact question, options, what is blocked and what is not.
   Say "nothing" when there is nothing; never omit the heading. With the standing directive
   (§8) in force this section normally holds the four escalations or "nothing" — a question
   here means the directive could not decide it, and the entry says why.
2. `## Now` — timestamp, cycle number, `main` SHA, stop-file status, agents live / 32.
3. `## Legs` — one row per live leg: number, route, agent, branch, phase
   (`novelty` → `build` → `measure` → `writeup` → `verify` → `gating` → `merged`), started,
   last event.
4. `## Support` — one row per live support agent.
5. `## Landed` — merged commits since the last report, one line each.
6. `## Queue` — the next legs from `DIRECTION.md`.
7. `## Stop` — the three stop files, restated every time.

Because it is git-ignored it never churns `main`. Whenever anything lands on `main` — a leg's
own push or an orchestrator merge — the orchestrator also refreshes `reports/STATUS.md` — a
committed snapshot of sections 1–3 — so the same view is readable from a cloud or mobile
session.

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

## 11. The maintenance sweep (periodic tech debt)

**User directive (2026-08-05):** the ten leg slots stay Opus and stay research. Tech debt is
handled by **Sonnet support agents, at most five live at once**, and the sweep is **kicked
off by the orchestrator periodically** — it is not a standing lane and it never displaces a
leg slot.

- **Cadence:** at run start (before the first dispatch cycle settles), and again at each
  date boundary alongside the report (§9b). Off-cadence only if integration trips over debt
  that blocks it (a broken index, a dead reference in a handoff file).
- **Seed:** the newest `reports/TECH_DEBT_REVIEW_*.md`. The sweep *refreshes* it rather than
  starting blind: re-audit docs/code/structure for drift, mark items closed with the fixing
  commit, append new ones. Every item carries evidence (file:line), a size, and a
  **claim-bearing vs mechanical** flag.
- **Mechanical items** (links, indexes, stale state files, script and registration fixes)
  are worked directly by sweep agents under declared territories (§5b) and land through the
  normal support-branch merge path (§7).
- **Claim-bearing items are never worked by the sweep.** Anything touching a numeric claim,
  gate wording, banked prose, the merge criterion, or the ledgers goes to the DM as a queue
  candidate and gets a leg + verifier like any other claim-bearing change.
- Sweep agents obey all of §1 and §5a: no ledger edits, no `DIRECTION.md`, no banked-result
  rewrites. A sweep finding that *requires* one of those is a report line, not an edit.

---

*Maintained in-repo so cloud agents read the same contract. Update this file and
[ORCHESTRATOR_PROMPT.md](ORCHESTRATOR_PROMPT.md) together — but keep the split: rules and
usage notes belong **here**, and the prompt stays pure instruction with nothing in it that
describes itself (see "How to start a run" above).*
