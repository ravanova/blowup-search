# Orchestration playbook — continuous four-leg operation

## How to start a run

**Paste the full text of [ORCHESTRATOR_PROMPT.md](ORCHESTRATOR_PROMPT.md) — and nothing else —
into a fresh Claude Code session set to Sonnet 5, in this repository.** That session becomes
the **orchestrator**: it dispatches the agents defined here, keeps four legs running in
parallel, audits the legs' own pushes to `main` and merges the support work unattended,
writes a live progress file the user can read at any time, and hands off to a fresh
orchestrator session before its own context runs out.

**This manual paste is only needed to start the run, or to intervene by hand.** Once running,
the orchestrator hands off by scheduling its own successor (§9e) — no cron, no human
re-pasting. The one case that still needs a manual paste: a session died before it could
schedule its successor (check `reports/ORCH_STATE.md` for a `## SELF-CHAIN FAILED` block, or
just a stale timestamp with no explanation) — then paste `ORCHESTRATOR_PROMPT.md` fresh, same
as starting a new run.

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

Four legs live at all times. Each leg is **one Opus 5 agent, end to end** — its own novelty
pass, its own construction, its own measurement, its own gate answer, its own quartet (§6),
and **its own push to `main`** (§7b). When its push lands the agent is terminated and a
fresh agent spawns into the slot on the next brief, so four legs are always in progress.
One verifier is paired to each leg. Everything else is repo-wide support that serves all four.

The four legs must pursue **different ideas or different directions**, chosen so they do not
depend on each other's results and do not touch each other's files. That independence is the
Decision Maker's responsibility to design and the orchestrator's to enforce (§5).

**Do not shard a leg.** Splitting one leg across several agents was measured on 2026-08-05 to
be slower *and* more expensive than one agent doing the whole thing. One agent per leg is the
default; the one deliberate exception is the sharding control arm in §10.

## 3. The Decision Maker (DM)

**One extra agent, Fable 5, outside the 20-slot pool.** The DM decides *what to work on*; the
orchestrator decides *how it lands*. The orchestrator never invents a leg — and when the plan
and the queue leave the next leg genuinely unclear, **the DM chooses the work**. That mandate
is the DM's alone; an empty leg slot is never the answer.

The DM owns [DIRECTION.md](DIRECTION.md) and nothing else. That file is its durable state, so
a bloated DM can be discarded and recreated cheaply from it. DIRECTION.md carries:

- **the leg queue** — ranked candidate legs, each with a route name, a one-paragraph thesis,
  a **pre-committed gate naming both branches**, and its **file territory** (§5);
- **live assignments** — which leg number and route each of the four leg slots holds;
- **the ranking rationale** — why this order, refreshed whenever a gate answers;
- **open direction questions** — resolved by the DM itself under the standing directive
  (§8) wherever possible; only a question the directive genuinely cannot answer surfaces
  for the user (via the progress file, §9a), with the DM's note on why it could not decide.

**Queue ranking.** Prefer, in this order: (a) a leg that could actually move a link of the
L1→L4 chain; (b) a leg whose gate can answer either way within a leg's work; (c) a leg
independent of the other three. A leg with no pre-committed failure branch is not a leg.

**Steering.** When the user gives the orchestrator input — a change of direction, a review of
goals, a new priority — the orchestrator forwards it **verbatim** to the DM via `SendMessage`
and asks for a revised queue. The orchestrator does not interpret the steer itself.

The DM may reason mathematically about direction. It may not build, measure, or write up.

### 3a. Reserve queue bookkeeping and watermark

**Diagnosed 2026-08-06.** The reserve (queued-but-undispatched legs) ran completely dry this
session — drained to two items with no buffer and no earlier signal — because DIRECTION.md
tracked it only as prose scattered across a long, repeatedly-superseded history, plus a
`(RESERVE)`/`(ASSIGNED)` tag on each leg's own heading that goes stale the moment that leg is
promoted somewhere else in the file. Nobody was wrong to trust it; there was simply no single
place that said the current count, so the only way to know it was hand-counting tags across a
file that explicitly warns its own older paragraphs are superseded.

**The fix: DIRECTION.md's Status section carries one canonical, always-current line**, e.g.
`**Reserve queue: 4 undispatched legs (117, 118, 119, 121).**` — updated by the DM every time
it touches the file, in the same edit that adds or promotes a leg. This is additive to the
existing queue entries and ranking rationale, not a replacement for them; it exists so the
count can be read in one line instead of re-derived by hand.

**Watermark.** The moment that count is **at or below 2**, the DM drafts at least 4 more
candidate legs — fully specified, same rigor as the initial queue (§3 above: thesis,
pre-committed gate naming both branches, disjoint file territory, difficulty class) —
**immediately, unprompted.** Waiting for the count to reach 0, or for the next time the
orchestrator happens to ask, is exactly the failure this fixes. If the orchestrator notices
the line is missing, stale, or already at/below the watermark, it asks the DM for a refresh
in the same message as its next refill request (§4a) rather than waiting for a dedicated cycle.

**Preconditions and pre-authorised dispatch (ported 2026-08-11 from the Project Building
Engine's first external run).** Every reserve leg carries, in its DIRECTION.md entry, an
explicit **`Preconditions:` line** — what must have landed first, which territory must be
free, any merge-order constraint. "None" is a valid value and must be written, not implied.
**The orchestrator may dispatch, without a live DM round-trip, the highest-ranked reserve leg
whose `Preconditions:` line reads entirely true at dispatch time** — this is what makes a
drafted reserve leg a *ready* reserve rather than a suggestion. Rules:

1. All preconditions true → dispatch the leg **as written**. Any one false or ambiguous →
   skip to the next-ranked reserve leg. **Never improvise a variant** to make a leg
   dispatchable — that is inventing a leg, which the orchestrator does not do.
2. The per-vacancy DM ping (§4a) still happens — it is how the DM re-ranks and refills the
   reserve — it is simply no longer a *blocking* dependency for filling the slot.
3. The composition floor (§3b) and territory disjointness (§5b) are still checked at
   dispatch, exactly as for a DM-assigned leg.
4. Two classes still require the DM before dispatch regardless of preconditions: a leg whose
   stated assumptions have been broken by something that landed after it was drafted, and a
   leg whose subject matter touches a §8 escalation.

### 3b. The composition floor — a quota, not a preference

**Diagnosed 2026-08-06, by external review.** The §3a watermark trigger refills the reserve
on demand, and an audit/repair/verify leg is the cheapest kind to draft — every module in
`solver/` can support one. Left unconstrained, the reserve refills with audits by default and
the live roster inherits that composition: one review found leg 0 (orchestrator integration
commits) at 57% of the last 60 commits on `main`, up from 25/60 and 9/60 in the two reviews
before it, and a full roster of audit/repair/verify legs with zero math, literature,
or construction legs. A prior "math-over-review" standing preference did not survive an
orchestrator restart, because a preference recorded only in prose is exactly the kind of rule
lesson 68 warns decays at the rate of memory.

**The rule, executable, not a preference:** **at least 2 of the 4 live slots must at all
times hold a leg whose primary output is mathematics, external literature, or construction**
(not an adversarial audit, a repair, or a post-construction verification). The §3a watermark
trigger **may not** fill a slot with an audit/repair/verify leg while the roster is below this
floor. If the reserve contains no eligible math/literature/construction candidate at the
moment a slot needs refilling and the floor is not met, the trigger **fails loudly** — the DM
drafts an eligible candidate before the orchestrator dispatches anything else into that slot,
rather than filling it with whatever cheap audit is sitting in reserve.

**The orchestrator checks the floor at every refill** (`ORCHESTRATION.md` §4a's per-slot
refill step): before dispatching a leg into a newly-vacated slot, count how many of the
remaining three live slots are math/literature/construction-typed; if the floor would be
breached by filling this slot with an audit/repair/verify candidate, request an eligible
candidate from the DM instead, even if that means a slot sits briefly unfilled rather than
filled with an ineligible type. `test_plan_of_record.py` or the merge gate should assert this
floor directly from `DIRECTION.md`'s own slot table if a checkable form can be added there —
an unenforced rule is a rule that will drift again.

| Band | Slots | Model | Lane | Branch prefix | Role |
|---|---|---|---|---|---|
| **LEG-A…D** | 4 | Opus, high effort | local worktree | `leg/<N>-<slug>` | One whole leg each, end to end: novelty pass → construction → measurement → gate answer → full quartet → **its own rebase, gate, and push to `main`** (§7b). Owns only its own files (§5). Terminated once its push lands; the slot refills with a fresh agent. |
| **VER-A…D** | 4 | Opus, high effort | local worktree | `verify/<N>-<slug>` | Paired 1:1 to a leg. Re-measure any prior headline that leg *consumes* (lesson 85) **before** it builds on it; then line-by-line review of the leg's landing on `main`, after the fact. **Reports gaps, does not repair.** Spawned when its leg has something to verify, not idle-running. |
| **LIT-1,2** | 2 | Sonnet | cloud or local | `lit/<N>-<slug>` | Standing literature flags, and deep dives a leg requests. A leg's *own* novelty pass stays with the leg — LIT does not replace it. |
| **REPRO-1,2** | 2 | Sonnet | cloud or local | `repro/<N>-<slug>` | Mechanical reproducibility: every root `test_*.py` **with `.venv/bin/python`**, raw per-file pass/fail counts (never a rolled-up summary); figures via `writeup/build_figures.py`; `*_evidence.py` scripts rebuild without re-runs. Fixes *scripts*; a prose/JSON discrepancy is reported, never repaired. |
| **DOCS-1,2** | 2 | Sonnet | cloud or local | `docs/<N>-<slug>` | `writeup/INDEX.md`, quartet-completeness audit, dead links, `README.md`, `writeup/README.md` index. Checks each leg's BLOG/TECHNICAL against the docs contract before merge. |
| **PREP-1,2** | 2 | Sonnet | cloud or local | `prep/<N>-<slug>` | Plan-consistent bricks that are not on any leg's critical path. |
| **BENCH** | 4 | assigned | assigned | assigned | Unassigned capacity. |

**Bench priority, in this order:**
1. **Refill a leg slot the moment one vacates** (§4a) — four legs live is the target, not a
   ceiling reached once. Refill is per-slot and immediate: terminate the finished agent, get
   the next brief from the DM, spawn fresh.
2. **Repair work integration found.** A failing gate, a broken test on `main`, a bug an agent
   tripped over: spawn a bench agent to fix it. Issues get *worked*, not queued.
3. **A fifth+ parallel route** from the DM's queue, if every other slot is saturated and
   the queue has a ready, independent item.

### 3c. The PROGRAMME lane — sustained construction on one object

**Adopted 2026-08-11 by user ruling: stop screening; build for one object.** Everything above
describes a *leg* economy — short units, each a question with a pre-committed two-branch gate,
each agent terminated on landing (§7b). That economy is correct for screening and it is
structurally incapable of the other mode. A bespoke apparatus built for one object cannot be
assembled in units that die on landing and restart with no memory; the comparable published
efforts took years of sustained work on a single object, most of it unpublishable while in
progress. Four mechanisms in this contract enforce the leg economy, and a programme suspends
each of them **for its own units only** — every other leg on the board keeps the full contract.

1. **No termination on landing.** A programme's worker is long-lived and keeps its state across
   units. §7b's "terminated once its push lands, slot refills with a fresh agent on a fresh
   brief" does not apply to it. The programme occupies its slot until it completes, stops on
   its own rule, or the user ends it.
2. **Milestones, not gates, for construction units.** Pre-committed gates stay mandatory for
   every unit that makes a **claim** — a measurement, a verdict, a number that enters prose.
   A unit that only *builds* reports against a declared milestone instead. Do not manufacture
   a two-branch question for work that has no answer to give; that is how a build gets
   deformed into a screen.
3. **One novelty pass per programme, not per unit.** Run it at programme start, in full, and
   it binds the whole programme. Requiring every unit to first ask "has anyone already done
   this" is the screening reflex institutionalised, and on day nine of building a solver it
   produces nothing. A unit that later makes a novelty *claim* still needs its own pass.
4. **Literature legs stop counting toward §3b's composition floor while a programme is live.**
   The floor exists to keep math/construction on the board; a literature leg satisfies it
   while being pure screening, which is precisely the substitution that must not happen now.
   Construction and mathematics still count; literature does not.

**What does NOT change, and matters more here, not less:** the three-tier win condition,
lesson 91 (name the realization), the merge gate, territory discipline, the honesty rules of
§6, and the requirement that no output is described as movement toward Clay unless a link of
the chain actually moved. A programme is a change to the *unit of work*, never to the standard
of evidence.

### 3d. Stop thresholds — a null from an under-resourced attempt is a cost, not a verdict

**Diagnosed 2026-08-11.** A pre-committed stop is only as good as the attempt that fires it.
Leg 353 fired route 4's stop on a `NO` whose own text reads *"the failure is
seed-quality/no-hookstep-globalisation (this leg's affordable `T_total=2000` DNS vs the
literature's `T~1e4-1e6`), NOT a broken extraction layer"* — two to three orders of magnitude
short of the scale the question is posed at, with its own control converging cleanly at 99.3%
residual reduction and thereby proving the apparatus sound. A route was recorded as stopped on
evidence that measured the budget, not the route.

**The rule: a stop fires only on a null from an attempt resourced at the scale the question is
posed at.** An under-resourced attempt that fails returns **a cost estimate for the compliant
attempt**, and its gate answers `UNDER-RESOURCED`, never `NO`. Any leg whose gate could fire on
an attempt it already knows to be minimum-viable must say so in its own pre-registration and
name the compliant scale — if it cannot name that scale, it is not ready to be dispatched.

This is general. It applies to every route, and it is the reason a cheap first attempt must
never be allowed to close a lane.

### 3e. The READ SURFACE — `STATE.md` first, archives only by pointer

**Adopted 2026-08-12. This binds BOTH modes and it is the single largest cost in the run.**
`DIRECTION.md` is **23,699 lines / 1.5 MB (~380k tokens)**; with `plan_of_record.py`,
`capabilities.py`, `CONTINUATION_PROMPT.md`, `STATUS.md` and `ORCH_STATE.md` the mandatory read
surface is **~480k tokens** — paid by *every agent* in orchestrated mode and on *every task* in
solo mode. Almost all of it is accumulated cycle history that the task at hand does not need.

**The rule.** `STATE.md` is the read surface. It carries the mode, the goal and ceiling, what is
in flight, the pre-committed next tasks, the open user decisions, the 19 live bans one line
each, the standing discipline, and a pointer table. **Read it instead of `DIRECTION.md`.**
Consult an archive only when `STATE.md` names the specific entry you need, and read **that
entry**, not the file.

- `DIRECTION.md` — a task's own spec, that entry only. **Never read whole.**
- `plan_of_record.py`, `capabilities.py` — **execute them**, do not read them. `capabilities.py`
  takes a substring argument; that is the grep the standing ban requires.
- `writeup/data/*.json` — the banked numbers. **Re-derive from these, never from prose.**

**`STATE.md` is regenerated as part of finishing a task**, in the same commit, the way
`JOURNAL.md` pointers are. A stale `STATE.md` is worse than none: it is the one file every
agent trusts without checking. If it disagrees with an archive, **the archive wins and
`STATE.md` is repaired in the same turn**.

### 3f. SOLO mode — one instance, one task at a time

**Adopted 2026-08-12 by user ruling** (usage constraints). The four-slot contract, the DM, the
orchestrator, the paired verifiers and the composition floor are all **suspended**. What
replaces them is not a smaller version of the same thing, and the difference must be stated
honestly rather than assumed away.

**What survives the collapse, because it is mechanical:** pre-committed gates; the novelty pass
before construction; **planted controls that must fire in both directions**; `merge_gate.sh`;
re-derivation from banked JSON; exact/rational arithmetic where the problem admits it. These
work regardless of who runs them, and in solo mode they are the *whole* defence — weight them
accordingly, not less.

**What does NOT survive, because it depended on independence:** a paired verifier re-measuring a
headline; the DM ranking against the record rather than the worker's preference; the
orchestrator auditing landings. A large fraction of this repository's caught defects came from a
*different* agent re-running the work — legs 233, 286, 300, 310, 384, 212, 193 and 229 among
them. That capability is gone, and three rules replace it:

1. **VERIFICATION IS A FRESH SESSION OR IT IS NOT VERIFICATION.** A result may be recorded as
   verified only if the check was run in a session with **no memory of the construction**,
   re-deriving from banked JSON alone. Otherwise the result is labelled **`UNVERIFIED`** and
   says so in its own gate answer. **Self-checking is never silently recorded as verification** —
   that substitution is the single way solo mode goes wrong, and it is invisible afterwards.
2. **Pre-commit the NEXT task, not only the gate.** The sharpest solo drift is choosing what to
   do next based on how the last one went. `STATE.md` carries the next three; re-ranking them
   requires its own commit stating why, held to the same standard as a gate.
3. **No more than two consecutive audit / repair / regression tasks** before a mathematics or
   construction task. The composition floor is meaningless without slots; the audit-loop drift
   it defended against is not, and it recurred three times with a Decision Maker watching.

**Task size goes up, not down.** Under a usage constraint the saving is in *fewer context
loads*, not cheaper tokens: one larger task carrying its state through a single context beats
several small ones that each re-read the surface.

**Unchanged in solo mode:** the three-tier win condition, lesson 91, §3d's stop threshold,
territory discipline where it still applies, the merge gate, no external outreach, and the rule
that no output is described as movement toward Clay unless a link actually moved.

### 3g. CONDUCTOR mode — the Decision Maker and the orchestrator are one entity

**Adopted 2026-08-13 by user ruling**, together with `CLAY_ROADMAP.md` §7.6 and `WALLS.md`. This
is the mode the wall programme runs in. It sits between §3f solo (one instance, no parallelism)
and the four-slot contract of §§2–5 (two roles, four long-lived legs, a composition floor).

**The single role.** One long-lived entity — the **Conductor** — owns *both* direction and
integration. It ranks the work, dispatches workers, audits what they return, lands it on `main`,
and re-ranks against what it just learned. It owns `STATE.md`, `WALLS.md`, `DIRECTION.md` and
`plan_of_record.py`.

**Why the merge is safe, when the two roles were split deliberately.** The split existed to stop
the orchestrator from re-ranking the queue to suit its own integration convenience. That failure
needs an *integration pressure* to act on — a slot to fill, a leg mid-flight to keep fed. The wave
model below removes it: workers are dispatched in a batch, they self-terminate, and the Conductor
does not re-rank until the batch is complete and audited. There is nothing to be convenient about.
**§4a's notification contract is discharged structurally** — the entity that learns the finding is
the entity that ranks the queue, so the gap it defended against cannot open.

**The wave, which is the unit of work in this mode.**

1. **PLAN.** Read `STATE.md` and `WALLS.md`. Choose the next 2–4 units, from *different lanes*
   where possible so a single wave cannot be sunk by one lane stalling. Write them into `STATE.md`
   with their gates pre-committed, and **commit that before dispatching** — the ranking is on
   record before any result can influence it.
2. **DISPATCH.** One worker per unit, each with a written brief carrying: its unit, its gate in
   final wording, its file territory (§5b), its lane, and the §3d resourcing statement. Workers do
   **not** read `DIRECTION.md` (§3e). Territories must not overlap.
3. **WORK.** Workers run to their gate and **self-terminate**. A worker never picks its own next
   unit and never re-scopes its gate. If it finishes early it reports early; it does not find more
   to do.
4. **INTEGRATE.** The Conductor audits each return against the pre-committed gate, lands it,
   regenerates `STATE.md`, and **pushes to `main`**. Do this per wave at minimum — more often if a
   unit lands cleanly on its own.
5. **RE-PLAN.** Only now. Re-ranking states its reason in the commit message.

**The one thing the Conductor may not do: verify its own waves.** It planned them, so it is not
independent of them — §3f rule 1 applies to it with more force, not less, because it has more
context to be biased by. **Verification is a worker with no memory of the construction,
re-deriving from banked JSON.** Budget one verifier per wave, dispatched in the *following* wave
so it cannot be briefed by the construction it is checking. Anything not so verified is labelled
**`UNVERIFIED`** and says so in its own gate answer.

**Wave sizing.** 2–4 workers. Below 2 this is §3f solo with extra ceremony; above 4 the audit
becomes the bottleneck and the Conductor's context becomes the constraint the whole mode exists to
protect. Prefer fewer, larger units — §3f's "task size goes up, not down" holds here.

**Wave composition floor (adopted 2026-08-13).** **Every wave carries at least one unit attacking a
wall on the Clay chain directly** — a Lane T, V or L unit in `WALLS.md`'s terms. This is §3b's
composition floor re-posed for waves, and it defends against the specific drift this programme is
now exposed to: Lane R work is real, it is currently the most productive thing in the repository,
it always has a next increment, and it is *satisfying* in a way that literature and escalation
units are not. A programme can spend a year becoming excellent at finding orbits it was never going
to certify. **A wave of pure Lane R units is out of contract**, and so is a wave whose only
non-Lane-R unit is an audit.

**Self-chaining and handoff state.** §9e applies unchanged: the Conductor continues into the next
wave without a human re-pasting the prompt, and hands off per §9d before its own context runs out.
A handoff writes `STATE.md` and pushes first; a handoff that loses the plan loses the wave.

**`reports/ORCH_STATE.md` is written AT EVERY WAVE BOUNDARY, not only at handoff (added
2026-08-13, closing a defect in this section's first draft).** §9d's trigger — hand off after 12
cycles or on noticing a summarisation — is a *handoff* trigger, and §9e is explicit that **a session
which dies before reaching it never schedules a successor and the chain stops silently**. For the
old four-slot orchestrator that cost one cycle. For a Conductor it costs the whole wave plan, the
pre-committed readings, and the audit state, because one entity holds all of it. **So the Conductor
refreshes `ORCH_STATE.md` in the same commit as the wave plan (§3g step 1) and again in the same
commit as the wave's integration (step 4).** Two extra writes per wave against losing a wave.

**What a Conductor's live block carries** — §9d's list was written for a role that no longer exists
in this mode, so it is restated rather than reinterpreted:

- the **wave number** and its **units**, each with its gate in final wording and its **pre-committed
  reading**, because a reading that survives only in the Conductor's context is not pre-committed;
- **every live worker: its unit, its branch, and how far it got** — branches, never handles.
  Subagent handles do not survive the session that spawned them (§9d), so a successor gates and
  merges whatever the abandoned branches contain and re-spawns for anything mid-flight;
- **`main`'s SHA**, the units landed this wave, and any unit **audited but not yet landed**;
- **open escalations** and whether each is awaiting the user;
- **which lane the composition floor was met from**, so a successor does not have to re-derive it;
- **what the next Conductor must do first**, in one imperative sentence.

**The accumulating sections are carried forward VERBATIM** — `## Environment notes`,
`## Known flakes`, `## Incidents and root causes`. §9d's rule is unchanged and binds a Conductor
identically: a handoff that rewrites the file from scratch and drops them has destroyed the only
mechanism stopping the next session from re-diagnosing the same incident. Add to them; delete an
entry only when it is provably obsolete.

**A superseded stop block is marked superseded, never deleted.** If `ORCH_STATE.md` opens with a
`⛔ STOP` block from an earlier run, the Conductor does not remove it — it prepends its own live
block and annotates the old one with the ruling that superseded it and the date. The stop happened;
the record of it is history, and a successor reading a silently-deleted stop learns nothing about
why the board looks the way it does.

**Inherited unchanged:** §3c (the PROGRAMME lane — `PROG-R4` keeps its exemptions), §3d (stop
thresholds), §3e (the read surface), §5a/§5b (territory), §7 (commits, branches, merge policy),
§8 (the four escalations — a Conductor that both raises and rules an escalation has defeated the
mechanism; escalations still go to the **user**), and the composition floor of §3b **as a
per-wave rather than per-cycle quota**.

### 3h. Attacking a wall — what ambition does and does not license

**Adopted 2026-08-13 with §3g.** `WALLS.md` authorises building whatever a lane needs, at any
size, without a further ruling. That authorisation is real, and these four rules are what keep it
from becoming the failure mode it most resembles.

1. **A ban is superseded by a measurement, never by a decision.** The permitted move is the
   2026-08-11 *scoping* of the DSS expensive-entrance ban: read the ban's own text, identify an
   object it does not name, and open that lane while the measurement stays true. The forbidden
   move is deciding a ban is obsolete because the goal got more ambitious. **A ban whose wording
   has become defective is a USER ESCALATION** (§8), not an agent's reading — two are already
   pending (Cadiot, and stage V's unliftable "needs L1 first").
2. **Scale is not evidence.** A large build is not a result. The gate is the deliverable and the
   pre-committed wording is unchanged by how much was constructed to reach it. This matters most
   exactly when a lane has been expensive.
3. **The ceiling clause survives the ambition.** Every gate answer in every lane carries its Tier
   statement, and **no output is described as movement toward Clay unless a link of the `L1 → L4`
   chain actually moved.** Under a wall-breaking mandate this rule is easier to erode, not harder —
   §7.5 said so, and it is repeated here for the same reason.
4. **A wall may be reported as unbroken.** Every wall in `WALLS.md` carries a pre-committed
   statement of what breaking it consists of, precisely so that "we did not break it" is a
   reportable, landable, valuable answer rather than a failure to be worked around. §3d still
   governs: an under-resourced attempt returns `UNDER-RESOURCED` and a cost, never `NO`.

### 4a. Refill is triggered by vacancy, not only by landing on `main`

**Diagnosed 2026-08-06.** A slot vacates in exactly two ways: a leg's push lands on `main`
(§7b), or a leg **escalates** and parks its branch instead (§8) — never `main`. Both empty the
slot the same way, and §8 already says so ("the orchestrator parks the item, refills the slot,
and keeps every other leg moving"). The gap this closes: mechanical instructions elsewhere have
been phrased around "the moment a leg's push **lands**," which reads as not covering the
escalation case at all — and in practice it didn't. Two slots sat `VACANT` in the live progress
file this session, both from escalations, waiting on a DM ruling on the *finding* when nothing
about that ruling should have kept the *slot* empty — routing an escalated result and refilling
its slot are independent decisions, and the second one never needs the first.

**So: treat an escalation's branch-park exactly like a landing for refill purposes.** The
slot is vacant the instant the escalation is reported, not the instant (if ever) the user or
the DM resolves it. Refill it in the same turn, from the DM's queue or a promoted reserve item,
same as any other closed leg.

**Batches.** When several slots vacate in the same cycle — a run of landings, an escalation
alongside them, several of either at once — refill each one as it is detected, not after every
landed leg has been audited and every support branch merged. Detecting a vacancy and requesting
its replacement from the DM is one action, not two steps apart in the loop; do not let "audit
what landed" finish for the whole batch before the first refill request goes out.

Never exceed 20 concurrent workers plus the DM. Steady state is ~10–15; the headroom is what
makes "assign an idle agent to a new leg" possible without starving verification.

**Routing the finding is the other half, and it is NOT optional.** §4a deliberately separates
*refilling the slot* from *routing the result*, so that a pending ruling never holds a slot
empty. That separation is correct, and it leaves the second half unowned unless it is stated:
before the landing audit is closed, **the orchestrator informs the DM of every completed
leg** — landed or escalated — with, in one line each: the leg number and route, the gate
answer **in the gate's own pre-committed wording**, the landing SHA (or the parked branch),
and any clause the leg explicitly left to a successor. §7b's post-landing-verification rule
("the orchestrator hands the verifier's finding to the DM") covers the one case where a
verifier confirms a gap; this covers every completed leg, gap or no gap.

**Why it is a contract clause and not a habit.** The DM ranks the queue, and it can only rank
against results it knows about. A finding that lands without reaching the DM leaves the queue
ranked on stale state — the next refill is drawn against a board that no longer exists, a
completed leg can be re-dispatched, and a leg whose precondition just landed can sit in reserve
unpromoted. Every one of those has occurred. The failure is silent by construction: nothing in
the merge gate, the floor table or the slot table can detect a DM that was never told.

**Mechanically:** the notification happens in the same turn the vacancy is detected, alongside
the refill request of §4a — one message carrying both, never two decisions taken apart. If the
DM is mid-turn, it goes in the next cycle's opening note rather than being dropped. **A leg is
not closed until its finding has reached the DM**, even though its slot is free the instant it
reports.

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

This is what makes four-way parallelism possible at all: the shared files that every leg used
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
   slot refills with a fresh agent on a fresh brief — four legs stay live.

An outcome that falls under an escalation (§8) is the one exception: the agent pushes its
*branch* only, never `main`, and reports it as parked. This still vacates the slot exactly like
a landing does, and it still refills immediately (§4a) — the escalation is a property of the
*finding*, not a reason to leave the *slot* empty.

**Liveness — the two ways a leg silently stalls (ported 2026-08-11 from the Project Building
Engine's first external run; this repo has paid for both — the 2026-08-06 incident in §9f, and
the 2026-08-11 handoff that found five legs holding WIP nobody had pushed).** The largest
source of lost wall-clock is not failure, it is **silence**: an agent that has neither
finished nor failed, holding a slot, with nothing scheduled to wake it. Both known variants
are the leg's own bug to prevent, and both belong in every leg's brief:

1. **The push-rejection stall.** Step 5 above is a retry loop, and a loop that waits on an
   external signal can wait forever. After a non-fast-forward rejection, **never wait
   passively to be re-prompted** — re-fetch and check whether `main` has caught up to your
   rebase; if your commit is now a clean fast-forward, push it immediately. An idle leg whose
   commit already fast-forwards `main` is a bug in that leg's own loop, not a scheduling
   matter.
2. **Idling between iterations.** At every iteration boundary exactly one of these holds:
   (a) a process you launched is running *and* you have a wakeup that reliably resumes you
   when it completes; (b) you are actively working; (c) the leg is finished and pushed. If
   none holds — uncommitted work, an unfixed failing test, a gate run you lost track of —
   **the next action is yours, right now.** Being between iterations is not a stopping state.

**In support of both: commit local work-in-progress checkpoints as you go** (after the
novelty pass, after construction, after measurement — restating §9f's hardening as the leg's
own duty, not just the orchestrator's insurance). A stall that gets nudged back to life must
never find hours of uncommitted work, and a replaced leg must leave its partial work
recoverable on its branch.

The orchestrator's backstop for a leg that breaks these rules anyway is the liveness sweep,
§9g — a backstop, not a substitute.

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
parks the item, refills the slot, and keeps every other leg moving. "Refills the slot" means
immediately, in the same turn the escalation is reported (§4a) — not once the user or the DM
has ruled on the escalated finding; those are two separate decisions, and only the first one
is the orchestrator's to make unprompted. Everything else lands as it turns green.

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
2. `## Now` — timestamp, cycle number, `main` SHA, stop-file status, agents live / 20.
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
ledger, and what the next orchestrator must do first), refresh `PROGRESS.md`, **schedule the
successor session** (below), tell the user, and exit.

**Two kinds of content live in `ORCH_STATE.md` and they age differently (ported 2026-08-11
from the Project Building Engine).** The live state above is rewritten at every handoff — it
describes *now*. The **`## Environment notes`, `## Known flakes`, and `## Incidents and root
causes` sections accumulate**: they are the run's institutional memory, things a session
learned by losing time to them (host-specific gotchas, specs that fail under load and pass in
isolation, incident root causes). Every handoff **carries them forward verbatim**, adds to
them, and deletes an entry only when it is provably obsolete — a handoff that rewrites the
file from scratch and drops them has destroyed the only mechanism that stops the next session
re-diagnosing the same incident.

**Be honest about what a handoff costs.** Subagent handles do not survive the session that
spawned them — a fresh orchestrator cannot `SendMessage` the old agents. That is exactly why
`ORCH_STATE.md` records **branches, not handles**: the new session gates and merges whatever
the abandoned branches contain, and re-spawns a fresh agent for any leg that was mid-flight.
Record in `ORCH_STATE.md` which legs were interrupted and how far they got.

### 9e. Self-chaining — the run continues without a human re-pasting the prompt

**User directive (2026-08-06):** rather than wait on a cron tick to notice a handoff (which
means real downtime — the minimum cron interval is one hour, and a run typically hands off
well before that), the orchestrator schedules its own successor at the exact moment it decides
to hand off, via a one-time `RemoteTrigger` (`run_once_at`, ~3 minutes out — enough buffer for
the `ORCH_STATE.md` push in §9d to land before the successor clones the repo). The full
mechanics are in `ORCHESTRATOR_PROMPT.md` Step 5; this section is the rationale and the
standing configuration, which is orchestrator-owned (agents don't touch it).

**Why this is safe against the collision problem a periodic cron would have.** A cron fires on
a wall-clock schedule regardless of whether the previous run is still going — with this run's
actual cadence (single sessions running for hours), a cron would very likely fire mid-run and
create two orchestrators dispatching against the same `DIRECTION.md` and the same four leg
slots. Self-chaining doesn't have this failure mode **by construction**: a session only ever
creates its successor at the moment it has already decided to stop, so there is never more
than one link of the chain live. No lock file is needed for this path.

**What this does NOT cover, by the user's explicit choice (2026-08-06): a session that dies
before reaching Step 5** — a hard crash, an unhandled error, being killed — never schedules a
successor, and the chain silently stops. The alternative (a coarse safety-net cron with a lock
file, checked at Step 0) was offered and declined in favor of simplicity. If the run appears to
have gone quiet, check `reports/ORCH_STATE.md`'s last commit time and `reports/STATUS.md`
before assuming everything is fine — a stale one with no `## SELF-CHAIN FAILED` heading and no
newer routine visible at https://claude.ai/code/routines usually means a mid-run crash, not a
graceful stop.

**Standing configuration (change here, not in `ORCHESTRATOR_PROMPT.md`):**

| Setting | Value |
|---|---|
| Environment | `env_01ABQhVSqMhLqttSew8uQBm6` ("More Freedom") |
| Model | `claude-sonnet-5` |
| Delay before the successor fires | 3 minutes from the moment Step 5 schedules it |
| Repo | whatever `git remote get-url origin` returns in the handing-off session |

**A failed self-trigger call is never silent.** Since there is no cron backstop, `ORCHESTRATOR_
PROMPT.md` Step 5 requires one retry and, on a second failure, an explicit `## SELF-CHAIN
FAILED` block in `ORCH_STATE.md` plus a plain statement to the user — a quiet exit with no
successor scheduled and no error surfaced is the one outcome this mechanism must never produce.

**Routines cannot be deleted via the API** — each fired one-time trigger stays listed (as
"Ran") at https://claude.ai/code/routines. This is cosmetic clutter, not a functional problem,
but a human doing periodic hygiene on that page is reasonable.

### 9f. Heartbeat — keeping the session alive while agents work

**Diagnosed 2026-08-06.** An orchestrator session that dispatches a batch of background agents
and then only waits for their completion notifications can itself go idle and be reclaimed —
taking every dispatched agent with it. In the incident that prompted this section, 13
background agents (2 re-spawned legs, 7 new legs, 4 bench agents) all stopped simultaneously
about ten minutes after dispatch, every one mid-novelty-pass and none further, with the
orchestrator's own `TaskOutput`/`SendMessage` access to all 13 breaking at the same moment.
The git worktrees survived on disk (their commits were recovered and pushed by hand after the
fact), but the live agent processes and the orchestrator's tracking of them did not — the
uniform stopping point and the simultaneous loss of tracking point at the orchestrating
session (and its container) being judged idle and suspended, not at 13 independent agent
failures.

**The fix: never let the orchestrator's own turn go quiet for long stretches while agents are
in flight.** Immediately after any dispatch that leaves agents running unattended for more
than a few minutes — the initial four-leg dispatch in Step 2, and every refill in Step 3's
Terminate-and-refill step — arm a short heartbeat:

```
send_later(delay_minutes: 5-8, message: "Heartbeat: check on <N> in-flight agents — <list of
  leg numbers/branches>. Poll git log / git worktree list for real progress since the last
  heartbeat, refresh PROGRESS.md, and re-arm the next heartbeat if any are still pending.")
```

`send_later` is a scheduled Routine (the same mechanism §9e's self-chain uses), not a passive
wait — it fires from outside the container and can wake a suspended session back up, which is
exactly the property a completion notification cannot guarantee once the session has already
gone quiet. On each heartbeat: check for real progress (new commits in each agent's worktree
or branch, not just elapsed time), log it, and re-arm another heartbeat if agents are still
pending. Stop re-arming for a given batch once every agent in it has landed, been collected, or
been confirmed dead and re-spawned.

**This does not replace completion notifications** — a notification that arrives is still the
faster, preferred signal and should be acted on immediately. The heartbeat is a backstop for
the case where the session goes quiet long enough that no notification ever gets the chance to
arrive.

**Secondary hardening, cheap and worth doing regardless of the heartbeat:**
- Leg and bench agents should commit locally more than once during a leg (after the novelty
  pass, again after construction, again after measurement) rather than saving every commit for
  the finish protocol — cheap insurance if a worktree is ever actually lost, not just its live
  process.
- Don't fill every slot immediately just because it's empty if doing so means a large batch of
  agents will all run unattended for a long stretch at once — four legs plus a handful of
  support/bench agents is the designed ceiling, not an instruction to always dispatch that many
  in one go regardless of how long they'll run before the next heartbeat or notification. **This
  is a caution about the size of one dispatch batch, not license to defer the refill itself
  (§4a)** — requesting the DM's next brief and spawning the replacement agent for a vacated slot
  happens the same turn regardless; only "how many fresh agents get launched in the same breath"
  is what this bullet paces.

### 9g. Standing orchestrator practices — the liveness sweep, flakes, worktree hygiene

**Ported 2026-08-11 from the Project Building Engine's first external run.** Three disciplines
that run every cycle, not only when something looks wrong — each learned by losing time to its
absence.

**1. The idle-worktree liveness sweep.** Once per cycle (fold it into the §9f heartbeat's
progress poll), for every live leg answer two questions: *is a process actually running in its
worktree* (`ps aux` filtered to that path) and *how does its HEAD relate to `main`'s tip*. The
diagnostic:

| Live process? | Commit vs `main` | Reading |
|---|---|---|
| yes | anything | Working. Leave it. |
| no | behind / diverged | Stalled mid-rebase or mid-fix. Nudge with the specific state observed. |
| no | **clean fast-forward of `main`** | **Stalled in the finish protocol (§7b liveness rule 1).** Nudge to push now — this one is pure lost time; the work is done. |

Nudge directly (`SendMessage`) with what you observed; do not replace an agent that only needs
waking. This is a *scheduled* sweep, not a reaction to noticing something — the whole failure
mode is that a silent stall draws no attention to itself.

**2. Flakes are diagnosed before they are believed.** A test that fails while many worktrees
gate at once on a loaded host, and passes in isolation, is a flake, not a regression — and
treating it as a regression burns a bench agent on nothing. Before attributing a `main`
failure to whatever just landed, **re-run that test alone, under low load.** Confirmed flake
patterns are recorded in `reports/ORCH_STATE.md`'s `## Known flakes` table (which test, what
load it flakes under, how many times re-confirmed clean) so the next session recognises it
instead of re-diagnosing it.

**3. Clean up worktrees once landed and audited.** `git worktree remove <path> --force` after
the post-landing audit passes. Stale worktrees accumulate, hold obsolete configs, and make the
sweep in practice 1 read a stalled agent that no longer exists.

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

**User directive (2026-08-05, count revised 2026-08-11):** the four leg slots stay Opus and stay research. Tech debt is
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

## 12. The performance review (periodic, one agent)

**User directive (2026-08-05):** alongside the maintenance sweep, a periodic **performance
review agent** tightens the test scripts and the scripts/code paths that are run often or
reused across legs. One Sonnet agent, dispatched by the orchestrator on the same cadence as
§11 (run start and date boundaries), counting **inside** the sweep's five-agent cap.

**Targets, in priority order** — time spent where runs actually repeat:

1. the merge gate's always-on tests (`test_plan_of_record.py`, `test_capabilities.py`) —
   these run on *every* landing, so a second saved here is saved dozens of times a day;
2. the root `test_*.py` scripts the gate maps to frequently-edited modules;
3. `scripts/merge_gate.sh` itself and the rebuild path (`writeup/build_figures.py`, the
   `*_evidence.py` scripts REPRO re-runs);
4. `solver/` modules with many importers (e.g. `gclm.py`, `boussinesq.py`) — hot by reuse.

**Discipline (this is the part that keeps it safe):**

- **Measure first, magnitudes always.** Keep a timing ledger in `reports/PERF_REVIEW.md`:
  wall-clock per target before and after, dated. No before/after pair, no change. "Faster"
  is not a number. (Route-M M3 is the banked warning: parallelising the refinement ladder
  *cost* 12× — assume nothing.)
- **Behaviour-preserving only.** Every touched module's known-answer test must pass with its
  `capabilities.py` `validated` magnitudes unchanged. A speedup that loosens a tolerance,
  lowers a resolution, skips a case, or changes any recorded magnitude is **not a speedup,
  it is a claim change** — claim-bearing, to the DM, leg + verifier.
- Test scripts may be tightened (shared setup, cheaper fixtures, dead branches removed) but
  never weakened: the set of properties asserted must not shrink, and negative controls
  stay able to fail.
- Same law as everyone: §1, §5a, declared territory (§5b), support-branch merge path (§7).

---

*Maintained in-repo so cloud agents read the same contract. Update this file and
[ORCHESTRATOR_PROMPT.md](ORCHESTRATOR_PROMPT.md) together — but keep the split: rules and
usage notes belong **here**, and the prompt stays pure instruction with nothing in it that
describes itself (see "How to start a run" above).*
