# WAVE 7 — RULINGS COMMITTED, SLOTS PROVISIONAL

**Committed 2026-08-18.** §0 is a **RULING and it is final**. §§1–3 are **candidate slots with their
gates in final wording**; they are **NOT dispatched**, because `L6` is still in flight and §3i is
answered **when a unit returns**, not when a Conductor feels ready. Whoever runs wave 7 answers
§3i on `L6` first, then dispatches from here or says in the integration commit why not.

---

## §0 — RULING: THE LANE-R RANKING. `R4` FIRST, `R2` SECOND, `R3` THIRD.

**This ranking has been open since `E` landed and no Conductor had ruled it.** `E-iii` fired
(→ `R3`/`R2`) *and* `E-ii`'s antecedent was satisfied (→ `R4`). Both readings were pre-committed,
both were honestly engaged, and they point at **different** units. It is ruled here, with the
reasons, against the record.

### The tie is broken on KIND, not on which conditional fired

1. **`R4` is a VALIDITY fix. `R2` and `R3` are THROUGHPUT fixes.** `U3`'s time-stepper is
   **Lie–Trotter, globally first order — measured, ratio 2.00**, not assumed. So **every periodic
   orbit either campaign has produced is an `O(dt)` perturbation of the true flow's**, while the
   published rates this programme is trying to reproduce come from higher-order codes. Deflation
   (`R2`) and multiple shooting (`R3`) both make the solver find **more** objects, **faster**.
   Applied to a first-order solver, that is **faster production of objects whose status is in
   doubt.** Fix what the objects ARE before optimising how many arrive.

2. **`R4` can FALSIFY something already landed. `R2` cannot.** `R4` **invalidates `M1`'s
   reproduction** if the displacement is real. §3i values a falsification above throughput, and this
   programme's own history agrees: every real move this year came from something being made FALSE.

3. **`R2`'s measured upside is small, and it is bounded by the same exhausted pool.** `R0` measured
   the waste `R2` targets: **57 of `U5`'s 100 seeds had already been spent by `U3`**, **5 of 9
   convergences were bit-identical re-executions**, **4 of `U5`'s 5 distinct solutions were
   re-finds**. But the net: a second 100-attempt budget costing **57 core-hours bought ONE new
   orbit**. Deflation makes the re-finds stop; it does not make the pool bigger, and the anchored
   pool is **exhausted at `R < 0.25`** (141 remain, only **12 in-band**).

4. **`R2` beats `R3` on measurement, not on taste.** `R2`'s target is a **measured** loss (the three
   numbers above). `R3`'s case — long-orbit conditioning, the basin-structure finding, `E-iii` — is
   an **inference** about where the difficulty lives. An inference ranks below a measurement.

### What the record says AGAINST this ruling, stated because it does

`OPTIONS.md` §B has carried `R2` as **"the strongest surviving Lane R item"** since it was written,
and `R4` only as "`E` PROMOTED IT". **I am overturning that**, and the ground is that the standing
assessment was written **before** `E` measured the first-order stepper's consequence for recovery.
Ranking on what is measured **now** (§3i q3) puts validity first. If a future unit shows the
displacement is negligible, `R2` returns to the top **automatically** — that is the point of §1's
gate below.

### `R4`'s first unit is NOT a campaign re-run

**Do not re-run `U3`'s 100 attempts under a new stepper** — `prog_r4_e.md` §6 prices that at
**122.1 core-hours** and it answers a different question. The cheap decisive unit:

> **Re-solve the LANDED orbits under a second-order (Strang) stepper and measure the displacement
> in `(T, s)` and in state against the residual band the originals were accepted at.**
> Below the band ⟹ `R4` is a **non-issue**, `M1`'s reproduction survives **on measurement**, and the
> ranking flips to `R2` in the next integration commit. Above the band ⟹ **`M1`'s reproduction is
> invalidated**, which is the finding, and it is worth more than any number of new seeds.

### Two bans this ruling does not touch, and must not be read as touching

- **The GA ban stands and is correct.** Leg 349's gate: **0 of 6 properties cleared**. Leg 160 is why
  the ban is not merely procedural — the original fitness passed **6/6 at `n = 101/151`** and failed
  **5/6 at `n = 201/401`**: *the property stopped failing because the probe stopped measuring.*
  Liftable **only** by a repaired fitness passing the six-property gate at `n = 201/401` **or
  strictly finer**. It is not available as a shortcut, and `R2`–`R5` are deterministic — keep them so.
- **No grinder, and no supply.** Refuted in advance **and physically bounded**: `U3` 100 attempts →
  **0** orbits; `U5` 100 attempts with seed supply fixed (in-band supply 35→72, spend 31→60) → **0**;
  `E` **16 attempts seeded directly at published `(T, s)`** → **0**. The anchored pool is exhausted
  at `R < 0.25` — 141 candidates, **12 in-band** — so **nothing can push the in-band arm past 72
  attempts, ever**, and a grinder exhausts its legal fuel in **~10.7 h**. Options **A**, **B** and
  **D** of `PROG-R4`'s table have accordingly been **retired, not deferred**
  (`WALLS_HISTORY.md` §OPTIONS-A2): all three buy supply, which is a standing user prohibition, so
  they were never choosable and should not have sat in a live options table.

### §3k BINDS ALL THREE BEFORE A LINE OF CODE IS WRITTEN

`writeup/SOURCES.md` §"Owed at pre-registration" is the gate. **A construction unit in this lane
that cannot fill its row is not dispatchable.**

| lane | must name, at primary | current state |
|---|---|---|
| `R4` | operator splitting / Strang for the incompressible NSE | **UNNAMED** |
| `R2` | deflated continuation — `OPTIONS.md` already writes "Farrell–Birkisson–Funke" | **NAMED, UNREAD** — naming is not reading, and the register records **no depth** |
| `R3` | multiple shooting for periodic-orbit BVPs | **UNNAMED** — "standard technique" is not a citation |

**§3g's floor is untouched: Lane R never sets a wave's direction.** This ruling says which Lane-R
unit takes the lane's slot **when it gets one**. It does not give it one.

---

## §1 — CANDIDATE SLOT: `R4-a`, the displacement measurement. Construction. ~2–4 core-h.

**Pre-condition (§3k rule 3):** the Strang-splitting citation is in `writeup/SOURCES.md` at
`FULL TEXT`, **in the same commit as the pre-registration**, or the unit does not run.

**GATE, final wording.** Re-solve **every landed orbit of `U3` and `U5`** (the 9 distinct solutions)
under a **second-order** stepper at the **same** `dt`, and report, **with the numbers**: the
displacement in `T`, in `|s|`, and in the state norm, **each against the residual band the original
was accepted at**; and the **measured convergence order** of the new stepper (it must be ≈2, or the
unit has not built what it claims). Answer **YES or NO**: *does any landed orbit move by more than
its own acceptance band?* A `NO` is a real result and must not be reported as a disappointment.

**Pre-committed reading, both directions, before dispatch:**
- **NO** (no orbit moves beyond its band) ⟹ `M1`'s reproduction **survives on measurement**, `R4`
  drops **below** `R2`, and the ranking above is amended in that integration commit.
- **YES** (any orbit moves beyond its band) ⟹ **`M1`'s reproduction is invalidated**; `WALLS.md` W7
  and `STATE.md` both change, and no Lane-R throughput unit runs until the objects are re-established.

---

## §2 — CANDIDATE SLOT: `L7-src`, the primary-read unit §3k(b) asks for. Reading. ~1–2 h.

**The directive asked for Chae–Wolf + the ESŠ step + NRŠ/Tsai at primary. The record shows three of
the four are already discharged** (`writeup/SOURCES.md` rows 1, 2, 4). **The live debt is one item.**

**GATE, final wording.** **NRŠ 1996 (ARMA 136) is the only load-bearing source in this programme
never obtained at primary.** Establish, with evidence: (i) whether it is obtainable at all without
author contact (**prohibited**) or paywall circumvention (**prohibited**) — a refusal is a result and
must be banked as one; (ii) if not obtainable, a **forward-citation pass** (`OPTIONS.md` `T2′`)
fixing its Theorem-1 hypothesis from **three** independent full-text sources, not two; (iii) whether
the pincer in `WALLS.md` **closes as cited** — and if it does not, say so in exactly those words.
Update `writeup/SOURCES.md` **in the same commit**.

**Pre-committed reading:** if (iii) returns "does not close as cited", **`L5`'s NO is not withdrawn**
— its ρ-exponent measurement stands on its own — but W4 clause (b)'s **citation** changes, and that
is a `WALLS.md` edit, not a re-opening.

---

## §3 — CANDIDATE SLOT: `L5-nov`, the owed novelty pass. ~0.5 h. **Queued since wave 6.**

Owed work **on this run's own output**, so the standing screening stop does not bite.
`writeup/novelty/` stops at `leg_394.md`. The claim to check: Chae–Wolf's `α`-pin **and** NRŠ/Tsai's
exclusion applied to a **natively finite-energy** DSS ansatz — is that combination published?

---

## Standing clauses, in every brief

**COMMIT DURING THE RUN, NOT ONLY AT THE GATE.** Checkpoint above ~1 h wall **to a tracked path** —
wave 3 lost 3 of 4 units and the only one that left anything behind had committed, and `E`'s
gitignored checkpoints died with the container twice. **Tier 2 is never a proof. No output is
movement toward Clay unless a link actually moved. Clay is ~0.05%. Read, do not contact.**

---

# AMENDMENT — USER DIRECTIVE 2026-08-18. THREE UNITS QUEUED. §0'S RANKING STANDS.

**The user has WITHDRAWN "price, do not queue" on `E`'s field ensemble** as over-cautious: 91
core-hours at 8 workers is **~11.4 h wall — one overnight run**, which defers nothing, and `E` never
declined it on cost (its dispatch forbade new compute, so pricing it for a successor was correct).

**These are ADDITIONS, not a re-rank.** §0's `R4` > `R2` > `R3` is untouched. `R4-a` (§1) remains
the head of the Lane-R *ranking*; the three units below run first because they are **cheaper and
upstream**, not because they outrank it.

## Execution order, and why

| # | unit | kind | cost | why here |
|---|---|---|---|---|
| **A** | `R-bank` — bank the seed fields | reproducibility | **~0.5 h** | **Prerequisite for B and C.** Without it every shard pays the DNS again |
| **B** | `E-FE` — the field ensemble | measurement at scale | **~91 core-h, ~11.4 h wall** | The wave's centre. Closes `E`'s one structural limit |
| **C** | `R-prof` — profile the inner loop | measurement | **~1–2 h** | Runs **alongside** B. Upstream of every cost figure in the record |

**§3i q7 (are we in an instrument loop?) — answered before it is asked.** The last three units were
construction (`L6`, in flight), verification (`V5`), verification (`V-W5`). `R-bank` and `R-prof`
are instrument-class, so the wave is **centred on `E-FE`**, which is measurement at scale on the
programme's actual object — not another instrument. §3f rule 3 is satisfied.

---

## A. `R-bank` — BANK THE SEED FIELDS. **The blocker on parallelism is a `.gitignore` line.**

**Verified against the repo, not taken on report.** `experiments/programme_r4/.gitignore` reads, in
its own words: *"Large binary artefacts of the T=1e5 DNS: regenerated by
`u2_m2_dns_recurrence.py --stage dns`, **never committed** (~1.2 GB)"* — `u2_dns_ckpt.npy`,
`u2_dns_feat.f32`. And `e_hhard_diagnostic.py`'s own header states the seed construction:
*"field: exact re-integration (`u2_m2_dns_recurrence.regenerate`, bit-for-bit) of one snapshot of
`U2`'s `T = 1e5` trajectory, selected by rule in `select_seeds()`"*. It imports that module directly.
**So a shard cannot build a seed without the 1.2 GB artefact, and the artefact died with a container
once already.** Split 8 ways, the 3.4 h DNS becomes **~27 core-h of duplicated overhead on a 91
core-h job**, and it gets worse with shard count.

**The fields themselves are tiny.** The state is a `24 × 24` real vorticity field —
`24 × 24 × 8 = 4,608 bytes`. **160 fields = 737 KB.** (The directive's ~5 MB estimate is
conservative; even at complex128 it is 1.5 MB.) **Committable, by two orders of magnitude.**

**GATE, final wording.** Bank the **160 seed fields** the ensemble will use, as a committed
artefact under `experiments/programme_r4/`, with a manifest recording for each field: the row, the
arm, the field index, the snapshot index it came from, the selection rule that chose it, and a
**SHA-256 of the field bytes**. Then answer, **with the numbers**: **is every field bit-identical to
what `u2_m2_dns_recurrence.regenerate` produces from the same snapshot index — YES or NO, over how
many of the 160?** Re-verify `E`'s **16 original** fields against its banked ledger specifically, and
report that count separately. Then demonstrate the point: **run one attempt from the banked artefact
in a tree with the DNS checkpoint absent**, and report whether it reproduces `E`'s banked result for
that attempt **bit for bit**.

**Pre-committed reading.** Anything short of 160/160 bit-identical ⟹ **the ensemble does not launch
from this artefact**; the shortfall is a finding about the re-integration path's determinism and it
is reported as one, not patched around. A `NO` here is more valuable than the ensemble.

---

## B. `E-FE` — THE FIELD ENSEMBLE. **QUEUED.** 8 rows × 2 arms × 10 fields = 160 attempts.

**What it closes.** `E`'s 0-of-16 is currently **a statement about sixteen field draws, not about
the eight rows**: a published row supplies `(T, s)` and **not** a field, so one draw per arm measures
one draw. Ten independent fields per (row, arm) converts that into a statement about the rows.

**GATE, final wording.** Run **160 attempts** — the same 8 rows and 2 arms `E` used, with **10
independent fields per (row, arm)** drawn by `E`'s own recorded selection rule from the banked
artefact of **A**. Report, **with the numbers**: **how many of the 160 converge, and how many
recover a named row** — and, per (row, arm), **the recovery rate out of 10** with its exact binomial
confidence interval. Answer explicitly: **does any row recover in ANY of its 10 draws, YES or NO?**

**Pre-committed reading, both directions, before dispatch:**
- **0 of 160** ⟹ the null is no longer about draws. With 10 draws per arm, a per-draw recovery
  probability above **26%** is excluded at 95% for every row. That is a **statement about the rows in
  this realization**, and it is the strongest negative this programme can buy for ~11 h wall.
  **It is not a statement about the rows in the published realization** — `E-iv`'s realization gap
  and the `N = 24` resolution limit both survive it, and must be restated in the artefact.
- **≥ 1 recovery** ⟹ `E`'s null was a **draw artefact**, `M1`'s comparison changes, and Lane R's
  ranking is re-opened in that integration commit.

**Mandatory, from the 2026-08-14 loss.** Per-(row, arm, field) partials committed to a **tracked**
path — a gitignored checkpoint is a within-run optimisation, **not** a cross-container one, and
`E`'s died twice. Expected cost of a host exit with this in place: **~0.57 core-h of 91, 0.6%.**

---

## C. `R-prof` — PROFILE THE INNER LOOP. **In 403 legs no unit has ever done it.**

**Every cost figure in `OPTIONS.md` inherits one unexamined constant** — 95.389 s/epoch — and so
does **my own** 90.9 core-hour price for **B**. A speedup multiplies every future run in every lane,
which is exactly what Lane R is for.

### Premise check, run by the Conductor before committing this gate — and it changes the wording

The directive's hypothesis was *"an FFT-based step at that size should be tens of microseconds"*.
**The solver is ALREADY FFT-based.** `solver/kolmogorov2d_nkbasin.py` documents itself as
*"full fft2 (complex spectra, real fields), 2/3-rule dealiasing"* with an **exact integrating factor**
for the viscous term and RK4 on the non-stiff part. So the comparison is **implementation against
implementation**, not FFT against not-FFT. **The gate below is re-worded accordingly, before
dispatch, not after** — `CORRECTIONS.md` §34's lesson applied to my own gate.

**A smoke measurement, not the unit's work, taken to check the gate is answerable** (load average
21.5 on 12 cores while `L6` runs, so absolute numbers are inflated ~2×; the **ratios** are not):

| quantity | measured |
|---|---|
| `_rk4_step` at `N = 24` | **4,306 µs** |
| bare `np.fft.fft2` on `24 × 24` | **197 µs** |
| bare `np.fft.fft2` on `32 × 32` | **189 µs** — *the same*, for 1.9× the work |
| bare `np.fft.fft2` on `256 × 256` | 6,519 µs — 198× the work for 33× the time |
| 20 transforms per step (4 RK stages × 5) | **~2,964 µs = 69% of the step** |

**Flat cost from `N = 24` to `N = 32` is the signature of fixed per-call overhead, not arithmetic.**
The loop appears **overhead-bound, not FLOP-bound**, and its structure pays that overhead **20 times
per step**. That is a hypothesis with a measurement behind it; it is **not** the unit's answer.

**GATE, final wording.** Profile `_rk4_step` and `integrate` at `N = 24` against a **named,
cited reference implementation of the same scheme** (§3k — see below), and answer, **with the
numbers**: **(i)** where the per-step time goes, by call, summing to 100%; **(ii)** what fraction is
fixed per-call overhead — established by the size-sweep, not asserted; **(iii)** **is the per-step
cost within 3× of the reference at `N = 24`, YES or NO?**

**Pre-committed reading, both directions:**
- **YES, within 3×** ⟹ **a real and useful negative**: the record's cost figures are honest, `W7`'s
  compute wall is where the record says it is, and the constraint is elsewhere. Bank it and stop.
- **NO** ⟹ report the factor and **the single change that recovers most of it**. Do **not** rewrite
  the solver in the same unit: a stepper change invalidates every banked comparison, which is
  precisely the `R4` problem, and it needs its own unit and its own equivalence check.

**§3k, and it is not optional here.** Name the reference before writing a line: FFT-based
pseudospectral steppers are **published**, and this realization's own source (Chandler–Kerswell's
2D Kolmogorov flow, already cited in `OPTIONS.md` for `R_thres`) is the first place to look for the
reference loop. **Do not hand-roll a benchmark and call it the reference** — a self-authored
comparison measures the author's assumptions. The row in `writeup/SOURCES.md` must be filled at
`FULL TEXT` in the same commit as the pre-registration.

---

## What this amendment does NOT change

**NO GRINDER on the current realization.** Refuted three times (`U3` 100 → 0, `U5` 100 → 0, `E` 16
seeded at published `(T, s)` → 0) and the legal pool is **exhausted**: 141 candidates left, **12
in-band**, so nothing keeping the `R < 0.25` window can push the in-band arm past **72 attempts,
ever**. **`E-FE` is not a grinder** — it is 160 attempts at **fixed** rows and arms, varying **only**
the draw, with a pre-committed reading in both directions and its own milestone. **NO GA** (leg 349:
0 of 6; leg 160 measured why the ban pins the grid). **No new seed supply.**
