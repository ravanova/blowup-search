# Arc 5 — Outpaced: the target statement, answered elsewhere

**Technical note. Arc 5 is the concluding arc of the search programme.**

| | |
|---|---|
| **Date** | 2026-09-09 |
| **Curated data** | [`../data/arc5_outpaced_v1.json`](../data/arc5_outpaced_v1.json) |
| **Evidence script** | [`outpaced_evidence.py`](outpaced_evidence.py) — rebuilds every quoted number from the JSON, no re-run of anything |
| **Narrative companion** | [`BLOG_OUTPACED.md`](BLOG_OUTPACED.md) |
| **Rigor level** | **None.** This note contains no measurement of any fluid equation. It banks an external record and does arithmetic over the programme's own already-landed measurements. |
| **Clay movement** | **NONE.** No link of the `L1 → L4` chain moved. Clay stays ~0.05%. Tier 2 is never a proof. |

---

## 0. What this note is, and the two provenance classes in it

On 2026-09-08 a manuscript was published claiming finite-time blowup for the
forced 3D incompressible Navier–Stokes equations on `ℝ³` — **Fefferman's
Alternative (C)**, which is the statement this programme was aiming at
(`STATE.md`, *Goal, posture, odds*).

This note does three things:

1. banks the external record at its actual verification status;
2. answers, with the programme's own measured throughput, the question *how
   long would the plan have taken to get there* — three ways, with the
   assumptions of each stated so the numbers cannot be quoted without them;
3. states the structural reason all three prices are beside the point, and
   opens the charter for the one remaining arc.

**Two provenance classes are mixed here and they are not interchangeable.**

| class | what it is | status |
|---|---|---|
| `external_record` | public announcement, preprint abstract page, press coverage, read 2026-09-09 | **UNVERIFIED.** Not audited at full text here. Not reproduced. No Lean file compiled here. Stays UNVERIFIED in this prose and in every draft until an audit unit says otherwise. |
| `this_programme` | fields read from this repository's own landed files, each citing its file | **PRIMARY** |
| `derived` | arithmetic over the two above | recomputed by the evidence script, never restated from prose |

The standing rule this obeys: *a paper is a view of the record, never a source*
(`STATE.md`, wave-8 pivot). An external announcement is a view of somebody
else's record, and is banked at the status it actually has.

---

## 1. The external record, as reported

### 1.1 The theorem

> There exist a smooth, compactly supported force `f` and a time `T` such that
> the solution `u` of the forced 3D incompressible Navier–Stokes equations on
> `ℝ³`, starting from rest, is smooth on `[0, T)` and `sup|u|` becomes unbounded
> as `t → T`, while the kinetic energy remains uniformly bounded for all
> `t < T`.

| field | value |
|---|---|
| Clay alternative addressed | **(C)** |
| Domain | `ℝ³` |
| Initial data | **rest**, `u₀ = 0` |
| Forcing | smooth, compactly supported in space and time |
| Energy | `L²` norm uniformly bounded for `t < T` |
| Manuscript | 166 pages |
| Lean project | `github.com/openai/NavierStokesAndEuler`, review status **self-assessed** |

### 1.2 The construction, as reported

1. a **self-similar concentrating axisymmetric vortex**, shrinking to a point
   in similarity coordinates as `t → T`;
2. **small-scale, spatially-localised oscillatory pulses** in a cylindrical
   annulus, whose **Reynolds stress cancels the momentum residual**;
3. an **iterative correction scheme** removing higher-order residuals **while
   preserving compact support of `f`**.

### 1.3 Resourcing, as reported

| quantity | value |
|---|---|
| concurrent agents | ~10,000 |
| hours to proof | 88 |
| hours of Lean verification | 17 |
| total | **105 h** |
| messages (this problem) | ~2.7 M (~4.9 M across all trials) |
| tokens (this problem) | ~130 B |
| cost | "millions of dollars" (company estimate, unaudited) |

### 1.4 What is **not** established

- **The prize is not awarded and the problem is not closed.** CMI's 2018 rules
  (already banked in `CLAY_OBLIGATIONS.md` §7, checked against the published
  rules at leg 384, HTTP 200) impose four conditions: a qualifying refereed
  publication; **two years** elapsed; general acceptance in the global
  mathematics community *at CMI's sole discretion*; and a determination that
  the official questions were satisfactorily answered, again at CMI's sole
  discretion. None is met. OpenAI has stated it will not claim the prize.
- **Independent verification is incomplete.** The Lean review is self-assessed.
- **A priority dispute is unresolved.** Buckmaster alleges use of unpublished
  drafts from his collaboration; OpenAI denies accessing specific user data
  while acknowledging it cannot rule out de-identified usage data having helped
  its models; the bibliography grew 16 → 22 entries and critics note missing
  references including Chen–Hou.
- **(A) and (B) are untouched.** The unforced problem is open. ~~So is **(D)**.~~
  **STRUCK 2026-09-09 (leg 423, arc 6 R0; `CORRECTIONS.md` §66).** The manuscript's Theorem 1.1
  ends: *"Compact support also yields the corresponding construction on `T³ = ℝ³/ℤ³`,
  establishing alternative (D) in [13]; see Corollary 10.6."* Corollary 10.6 is stated and proved
  (pp. 125–126, every `ν > 0`) and the Lean project declares
  `NavierStokes.Comparator.navier_stokes_breakdown_periodic` a proved main result. **(D) is
  CLAIMED.** Whether the claim is correct is not decided by this note.
- **Nothing here makes any Tier-2 result in this repository a proof.**

### 1.5 The companion Euler result

A separate 112-page preprint (Alpöge–Buckmaster) constructs finite-time blowup
for **forced 3D Euler**, building on Córdoba–Martínez-Zoroa, developed with
substantial LLM iteration using Anthropic models, with Lean verification
completed earlier. Tao's reported remark: the method *"does not seem far from
showing blowup for Navier–Stokes too,"* though *"a large amount of compute and
detail-checking"* would be involved. This is the line the Navier–Stokes
construction descends from, and it is the reason the priority dispute exists.

---

## 2. The specific miss — leg 381

This is the substantive finding of the arc, and it is a finding **about this
repository**, not about the news.

Leg 381 (`7aecf78`) audited `CLAY_OBLIGATIONS.md`'s reading of Fefferman's
official problem statement, clause by clause: **4 confirmed, 1 corrected, 1
refuted.** The refuted clause was the reviewer's *"with `f ≡ 0`"*. Leg 381 was
right and the reviewer was wrong: `f ≡ 0` appears only in the **existence**
statements (A) and (B). Statement (C) permits a forcing.

Leg 381 then wrote, verbatim:

> This is a genuine relaxation of the target — the candidate need not be
> force-free — but leg 381 recorded explicitly why it is **not** a shortcut:
> the forcing must itself satisfy (4),(5), so it buys no escape from the decay
> and bounded-energy obligations that §4 and §5 price.

**Against the reported construction, that inference is wrong, and wrong in a
nameable way.**

| leg 381's model | the reported construction |
|---|---|
| `f` is an additional object that must independently satisfy (4),(5), so it adds obligations without removing any | `f` is the **free variable** into which the momentum residual is discharged |
| the localisation problem (`W4`) stays on the solution and must be paid for there | the oscillatory pulses' **Reynolds stress absorbs the residual**, and the iteration hands the remainder to `f` |
| condition (5) on `f` is a cost of the same order as (4)/(7) on `u` | **compact support** discharges (5) at no analytic cost |

`W4` — finite energy, the localisation problem — is this repository's own named
wall, and `CLAY_OBLIGATIONS.md`'s reviewer note already identified it as the
hard one:

> the gap between them is the localisation problem, which is unattempted here
> and is where comparable programmes have historically spent their hardest
> years. If one clause here is worth verifying first, it is that one.

The clause worth verifying first was verified — and the escape route out of it
was priced away in a subordinate sentence two paragraphs above.

> **Status of §2: UNVERIFIED.** It is a reading of third-party summaries of a
> manuscript nobody here has read at full text. It is banked as the **first
> thing arc 6 must check**, not as a landed finding. It is banked *at all*
> because of lesson 76 — the negative construction stays in the artifact — and
> because a wrong inference that closed the winning door is the most
> informative row this repository can carry, and precisely the row a programme
> is tempted to smooth over.

---

## 3. How long would the plan have taken? Three prices

### 3.1 Measured throughput (primary)

| quantity | value | source |
|---|---|---|
| legs run | 416 | highest leg in the record; wave 9 = legs 413–416 (`reports/ORCH_STATE.md`) |
| span | 2026-07-22 → 2026-08-19 = **28 days** | `ARCHIVE.md` earliest dated stage artefact; `reports/ORCH_STATE.md` run stop |
| cadence | **14.86 legs/day** | derived |
| live leg slots | **4**, each one Opus 5 agent end to end | `ORCHESTRATION.md` |
| worker ceiling | 20 concurrent, steady state ~10–15 | `ORCHESTRATION.md` |
| decision maker | **one Fable 5**, outside the 20-slot pool | `ORCHESTRATION.md` |
| `L1 → L4` links moved | **0** | `STATE.md` |
| self-assessed Clay odds | **~0.05%**, unmoved | `STATE.md`, `WALLS.md`, `CLAY_ROADMAP.md` |
| ceiling | **Tier 2** | `STATE.md` |

The counterfactual asked about is **10 Opus leg slots under one Fable
decision-maker**. That is 2.5× the leg slots actually run, and sits inside the
existing 20-worker ceiling. Nominal 2.5× is an overestimate: integration
serialises through a single Conductor, and `ORCHESTRATION.md` §5 (collision
avoidance) exists because parallel legs contend for shared files. The honest
bracket is **1.5×–2.5×**, i.e. ~22–37 legs/day.

### 3.2 Price A — agent-hour parity

```
10,000 agents × 105 h            = 1,050,000 agent-hours
1,050,000 / 10 agents            =   105,000 hours
                                 =     4,375 days
                                 =      11.98 years
```

Proof only, excluding Lean: 880,000 agent-hours → **10.04 years**.

> **Assumption, and it is false.** This assumes our ten agents run *their*
> method, on *their* model, at *their* efficiency. They do none of the three.
> Price A is the cost of **burning the equivalent fuel**, not of arriving.

### 3.3 Price B — the programme's own odds

Treating 0.05% as a per-programme probability and a programme as 28 days:

| speedup | programme length | 2000 programme-equivalents |
|---|---|---|
| 2.5× | 11.2 d | **61.3 years** |
| 2.0× | 14.0 d | **76.7 years** |
| 1.75× | 16.0 d | **87.6 years** |
| 1.5× | 18.7 d | **102.2 years** |

> **Assumption.** That programmes are independent repeats of a 0.05% trial. The
> record says the opposite: the odds are logged as *"unmoved"* across 416 legs,
> i.e. not a per-trial rate that accumulates. Price B is the most charitable
> reading of a number the programme wrote down about itself.

### 3.4 Price C — what the record actually measures

Zero successes in 416 legs. The one-sided 95% Clopper–Pearson upper bound on
the per-leg probability of moving an `L1 → L4` link:

```
1 − 0.05^(1/416)  =  0.007175   (0.72%)
1 / 0.007175      =  139.4 legs per link, at the bound
139.4 / 14.86     =    9.4 days per link at measured cadence
                  ≈    6 days per link at 10 slots
```

> **Assumption.** That legs are independent Bernoulli trials at a constant
> rate. They are not — they are a directed programme whose lanes were re-ranked
> repeatedly. This is a bound on the **data**, not a model of the work.
>
> **Direction.** It bounds the rate **above**, therefore it bounds the time
> **below**. It yields a **floor** of roughly a couple more months and **no
> ceiling at all**. Read the other way round it is a fabrication, and this note
> says so here so that no later draft can quote the 6-day figure as a forecast.

### 3.5 Why all three are beside the point

Because the point estimate of the rate is **zero**, the point estimate of the
time is undefined, and the correct answer is not a number.

---

## 4. Why the plan could not have arrived, at any speed

Four reasons, all of them already written down by this repository about itself
before the announcement existed.

### 4.1 The ceiling is Tier 2 and the programme says so

`CLAY_OBLIGATIONS.md` §6 names two obligations with **no known method**:

1. certified far-field decay and the admissible cutoff — *"Fitted decay exists;
   certified decay does not, and the cutoff analysis has not been attempted
   here."*
2. persistence/stability under localisation, including the unstable-manifold
   question leg 314 classified OPEN — *"This requires a theorem of a kind
   nobody in this repository has produced, and — per leg 314 — of a kind
   computation cannot supply."*

`STATE.md`: *"Ceiling: Tier 2. Route 4 produces a candidate; no certification
route is built."* And: *"The cheapest unit that could move one: **NO SUCH UNIT
IS KNOWN**."*

### 4.2 The object is not in the search space

`ga/genome.py` defines the genome over spectral coefficients of an **initial
field** under an energy budget (`Genome`, `random_genome`, `rough_genome`,
`realize`, `normalize`). There is no force term anywhere in the search.

The reported solution **starts from rest**: `u₀ = 0`. Its entire content is a
force. A fitness landscape over `u₀` does not contain that object at any
budget, for any number of generations, at any resolution. This is not a
resourcing gap. It is a representational one, and no quantity of agents
addresses it.

### 4.3 The ladder position

| rung | state at the stop |
|---|---|
| 1D gCLM | **banked, Tier 2** — and `STAGE_3_RESULTS.md` says out loud it is the CLM singularity surviving `a = 0.7` advection, `α = 1.000` throughout, **not** a novel De Gregorio blow-up |
| 2D Boussinesq | Route A, Phase 1 |
| 3D Euler | **Stage 4, unscheduled** |
| 3D Navier–Stokes | the target |

### 4.4 The apparatus

Tier 3 here was to be a Newton–Kantorovich radii-polynomial contraction, scoped
by `C1`. The reported proof uses no interval arithmetic, no DNS and no search:
it is analysis, then Lean. The two are different apparatuses in exactly the
sense `C1` was written to police.

### 4.5 Compute was never the binding constraint — measured, not asserted

`W7` was measured from the inside at leg 403 (`R-prof`, `1f89ceb`,
[`../data/p2_r_prof_v1.json`](../data/p2_r_prof_v1.json)):

| quantity | value |
|---|---|
| transform share of a solver step | **79.1%** |
| fixed fraction, `N = 4..512` | 0.596 |
| best priced speedup (FFTW3) | **3.41×**, priced not landed |
| `PROG-R4` U3 attempt CPU | 134.45 core-h (144.69 worker-h reserved, 92.92% utilised) |
| source papers, **2D** problem | ~10.2 GPU-days |

The wall's own verdict: **W7 UNMOVED** — *"a speedup breaks no wall, and no
link moved."*

**Ten Opus agents under a Fable buys roughly twice the Tier-2 legs per day, in
a lane whose documented ceiling is Tier 2.**

---

## 5. Arc 6 — the charter

**Status: PROPOSED, NOT RULED.** The direction question belongs to the user.
`ORCHESTRATION.md` §8 escalation discipline is explicit that an entity which
both raises and rules an escalation has defeated the mechanism, and this note
does not rule one.

Arc 6 is the last arc. It is where this programme delivers a result of its own
rather than a measurement of its own limits.

### A6-AUDIT — adversarial full-text audit + Lean compile-and-check

**Why it is ours.** Independent verification of the external result is
incomplete and self-assessed, so the work is wanted and is not duplicated. This
repository has landed exactly this kind of unit before: leg 174's census; `PB2`
re-verifying `W4` clause (b) against Tsai 1998 Theorem 2 at primary; `V-W7`'s
seven defects re-checked one by one (6 upheld, 1 upheld in part).

**Pre-committed gate — four clauses, each answered in its own wording:**

1. Is the reported theorem the theorem the manuscript proves? (statement,
   hypotheses, and the exact Fefferman conditions claimed)
2. Does the Lean project compile, and what does it actually certify **versus**
   what the prose claims? (a formalisation of a lemma is not a formalisation of
   the theorem, and the gate must distinguish them)
3. Is the momentum-residual absorption where the localisation problem is
   discharged — i.e. is §2 of this note right?
4. Are Chen–Hou and the Córdoba–Martínez-Zoroa line cited where they are used?

**Reachable: yes.**

### A6-PORT — port the residual-absorption mechanism onto our own profile

**Why it is ours.** `W4` is our wall, with our pre-committed statement of what
breaking it consists of. The reported oscillatory-pulse mechanism is aimed at
exactly the residual `W4` names. Whether it transfers to a profile this
repository actually holds is open and measurable.

**What would count:** either a break of `W4` under its own pre-committed test,
or a measured statement of why the mechanism does not transfer. Both are
results. **Neither is a Clay claim.**

**Reachable: yes.** **Caveat:** this is a *construction* unit and the
composition floor (`ORCHESTRATION.md` §3g) applies. It must not be dispatched
as an audit wearing a construction hat.

### A6-D — statement (D), the torus

**Why it is ours.** `W4`'s only surviving break clause is (c), and clause (c)
**is** statement (D). It sits in Lane T, deferred, behind
`writeup/escalations/ESCALATION_D_BUNDLING_2026-08-18.md` — recorded in
`reports/ORCH_STATE.md` as *"the most direction-relevant open item on the
board, and it has never been ruled."* ~~With (C) now claimed, (D) is the nearest
unclaimed Fefferman statement.~~ ~~Note also that (D)'s data conditions (8) and (9)
are still **unread** here, and are readable since the outreach narrowing.~~

> **STRUCK 2026-09-09 (leg 423, arc 6 R0; `CORRECTIONS.md` §66). A6-D IS DEAD.** Its premise
> was false on the manuscript's own text when it was written: (D) is **claimed**, by Corollary
> 10.6, for every `ν > 0`, and the Lean project formalises a torus result under the same name.
> A charter item whose stated reason for existing is that a statement is *unclaimed* cannot
> survive that statement being claimed in the same document that claims (C). The **escalation
> packet it names is unaffected and still unruled** — Lane T's deferral is a user ruling and this
> note does not touch it. (8) and (9) were read at primary at leg 417 (§61); the second struck
> sentence is stale for that reason, not for the first.

**Reachable: BLOCKED ON A USER RULING, not on work.** Lane T's two re-open
conditions are already written and neither has been met.

### A6-A — the unforced problem, (A) and (B)

**Not ours, on a theorem rather than on effort.** `W1`: a search of this class
can only ever argue *for* blow-up; direction (a) is closed by Tao's
averaged-Navier–Stokes supercriticality barrier. Recorded here only so nobody
rediscovers it as news.

### What arc 6 may not do

- Soften the three-tier win condition. **Tier 2 is never a proof.**
- Describe any output as movement toward Clay unless a link of the `L1 → L4`
  chain actually moves.
- Cite this note or its blog companion as a source. A paper is a view of the
  record, never a source.
- Treat the external record as verified. It is **UNVERIFIED** here until
  A6-AUDIT says otherwise, and it stays UNVERIFIED in every draft until then.

---

## 6. Documentation-contract compliance, and the two deliberate gaps

`ORCHESTRATION.md` §6 asks for four things per finding. This arc ships:

| item | state |
|---|---|
| 1. a runner in `experiments/` that produced the numbers | **N/A, and stated rather than skipped.** This arc runs no experiment. Its primaries are the repository's own landed files and an external public record. |
| 2. curated data in `writeup/data/*.json`, every number in prose present in the JSON | ✅ [`../data/arc5_outpaced_v1.json`](../data/arc5_outpaced_v1.json) |
| 3. `BLOG_*.md` **and** `TECHNICAL_*.md`, plus an `*_evidence.py` that rebuilds claims from the JSON without re-running anything | ✅ this file, [`BLOG_OUTPACED.md`](BLOG_OUTPACED.md), [`outpaced_evidence.py`](outpaced_evidence.py) |
| 4. a figure registered in `writeup/build_figures.py` | ❌ **deliberate gap.** This arc has no measurement of its own to plot; a chart of somebody else's press numbers would be decoration, and the repository already carries a live defect about figures without rebuild paths. Recorded as a gap, not omitted silently. |

**One further owed item, recorded and not done.** `STATE.md` is the file a
restarting session reads, and it should carry a row pointing here. It is not
modified by this arc: it is the Conductor's working surface, it is under the
§3j byte cap with **833 B** of headroom at the time of writing, and §5 file
ownership puts it outside this arc's territory. A restarting Conductor owes it
that row.

---

## 7. Summary of movement

| | |
|---|---|
| Walls moved | **none** |
| `L1 → L4` links moved | **0** |
| Clay odds | **~0.05%**, unchanged |
| Tier | this arc produces no tier; the programme's ceiling is Tier 2 and is unchanged |
| New verified findings | **none** — §2 is UNVERIFIED and is arc 6's first gate |
| What the arc actually establishes | that the programme's target statement was answered elsewhere, by an apparatus outside the programme's search space; that the programme's own leg 381 identified the relaxation that mattered and priced it away; and that no amount of additional agents addressed any of the four structural reasons the plan could not arrive |
