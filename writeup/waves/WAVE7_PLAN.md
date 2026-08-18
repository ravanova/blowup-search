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
