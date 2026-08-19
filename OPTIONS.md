# OPTIONS — the deferred work ledger

> ## ⚠ THE LANE RANKING CHANGED ON 2026-08-14 — READ THIS BEFORE ANY ENTRY BELOW
>
> **USER RULING 2026-08-14**, in full at `writeup/escalations/RULING_C1_EXEMPLAR_2026-08-14.md`
> (discharging `ESCALATION_C1_EXEMPLAR_2026-08-14.md`); lane consequences in `WALLS.md`
> §LANE PRIORITIES. **Lanes V (§C) and L (§D) ACTIVE and PRIORITY; Lane T DEFERRED (§E); Lane R
> unchanged.** The three clauses that bind every entry below:
>
> - **C1 STANDS, EXEMPLAR-FREE.** Its scope carries **no** implied *"and this has been demonstrated"*:
>   **no unit may cite C1 as evidence the technology closes for any object class.** Its **naming
>   requirement is unchanged and binds every unit.**
> - **No ban is lifted, narrowed or reworded.** 26 recorded / 19 in force, unchanged.
> - **A ranking is a decision, and a decision supersedes no measurement.** The 2026-08-13 ruling's
>   "pursue Lane T" is superseded **as a RANKING only**; every measurement it rested on, and A2 / B1 /
>   the narrowed outreach hold, stand untouched.

**Why this file exists.** `STATE.md` is regenerated at every landing, so anything living only in its
"Open" section is one rewrite away from disappearing. Nothing here has been rejected; each entry
carries **what it is, what it costs, why it is deferred, and what would re-open it.** An option later
taken is marked `TAKEN`, one later killed `KILLED` with the measurement that killed it.

**§3j compaction, 2026-08-18:** the cap forced the named remedy — **`TAKEN` and `KILLED` entries are
compressed to one line plus a pointer.** Their full text is in the unit journals and in git history;
nothing is dropped, and no live entry was touched except to correct what a measurement made stale.

**Rule for the Conductor:** a deferred item lands here in the same commit. At every wave plan this
file is read alongside `STATE.md` — a deferred option whose re-open condition has fired is a
candidate, and the plan must say why it was or was not taken.

---

## A. `PROG-R4` — the four options the user did not take

U5 raised five costed options (`experiments/journal/prog_r4_u5.md` §9); **the user ruled option E on
2026-08-13** and the other four are recorded here.

**The constraint shaping all of them:** the anchored admissible pool is **exhausted** at `R < 0.25` —
241 exist, 100 spent, **141 remain, only 12 in-band** — so nothing keeping the current window can push
the in-band arm past 72 attempts, ever. **And U5's pre-committed reading fired on branch (b): the bias
is in the BASIN STRUCTURE, not the seed supply.**

| id | option | cost | why deferred | re-opens if |
|---|---|---|---|---|
| **A**, **B**, **D** | all three **BUY SUPPLY** | — | **RETIRED, NOT DEFERRED**: proposing more seed supply for `PROG-R4` is a **standing user prohibition**, so these were never choosable. Verbatim → `WALLS_HISTORY.md` §OPTIONS-A2. | Only by a user ruling that lifts the prohibition. |
| **C** | Carry `m` as an unknown in the residual (= Lane R's **R5**) | own milestone, ≈10 h compute + solver work | Changes the realization, so M1's reproduction no longer compares attempt for attempt. **U5 priced it: 334 anchored in-window candidates, 58.1% of the window, but only 1 in the published band.** Not a band fix — the fix for `\|s\| > 0.9`. | On its own merits as the largest measured hole in the trial space, **not** as a route to the named rows. |

**`E` — THE H-HARD DIAGNOSTIC. LANDED `d0d72b1`, `UNVERIFIED`.** 2 of 16 converged, **0
recovered any named row**. Summary retired 2026-08-19 → `WALLS_HISTORY.md` §OPTIONS-E (its "the
re-ranking is NOT made" went false when I ruled it). `experiments/journal/prog_r4_e.md`.

**`E`'s FIELD ENSEMBLE — QUEUED 2026-08-19, "price do not queue" WITHDRAWN by the user.** 160
attempts, **90.9 core-h, ~11.4 h wall**; closes `E-iv` (a row supplies `(T,s)`, **not a field**).
**Not a grinder** — fixed rows/arms, only the draw varies. `WAVE7_PLAN.md` §B; price
`writeup/prices/FIELD_ENSEMBLE_2026-08-18.md`. **90.9 is an OUTTURN, not a floor** (see `R6`).

**`U4`/`G2`, basin radius: BLOCKED, not an option** — it needs a recovered *named* orbit to perturb
and there is not one. **`G1` stays `UNDER-RESOURCED`; `E` did not write to it** (hand-placed seed at
published coordinates, not a mined seed).

**⚠ THE `~8×` COST-MODEL OVERRUN IS REFUTED, and the epoch figure that refuted it is itself
corrected.** Full text retired 2026-08-18 under §3j → `WALLS_HISTORY.md` §OPTIONS-A. **Live
consequence: the banked cost model STANDS** (`0.9958` of measured, 0.4% under), so **no option
in this table is re-priced.**

## B. Lane R — the units not taken

| id | unit | status | note |
|---|---|---|---|
| **R0**, **R1** | metric; early abort | **TAKEN, w1, VERIFIED by `V1`** — §3j, one line plus a pointer. | `R0` **retracted** *"Lane R's first measured win"*; `R1` **closed against itself**, U5 had already collected it — **spend no more compute on this family.** `WALLS_HISTORY.md` §R0/R1. |
| **R2** | deflation (Farrell–Birkisson–Funke) | **DEFERRED — the strongest surviving Lane R item** | R0 measured the waste: **57 of U5's 100 seeds were already spent by U3**, **5 of 9 convergences are bit-identical re-executions**, **4 of 5 distinct solutions are re-finds**, U5's contribution new to the programme is **one orbit**. Deflate against the **union** of both runs' solutions. Re-opens whenever Lane R gets a wave slot. |
| **R3** | multiple shooting | **DEFERRED** | Brick B6's own spec names it; U1 built the globalisation without it. Standard conditioning fix for long orbits, and long orbits are where the published targets live. **The basin-structure finding points here, and `E-iii` fired, which points here again.** |
| **R4** | second-order-in-time stepper | **DEFERRED — AND `E` PROMOTED IT** | U3's is Lie–Trotter, globally **first** order (measured ratio 2.00), so its periodic orbits are `O(dt)` perturbations of the true flow's while the published rates come from higher-order codes. Invalidates M1's reproduction — own milestone. **`E-ii` named `R4` in advance as where a non-recovery would point, and its antecedent IS satisfied.** `E`'s leg-353 comparison is **the first evidence pointing at the REALIZATION rather than the budget** — a better realization got closer (residuals [0.80, 10.32] vs [22.5, 29.5]) from strictly **worse** seeds and still recovered nothing. |
| **R6** | **profile the inner loop** | **TAKEN 2026-08-19, leg 403 — gate (iii) `NO`** | **In 403 legs no unit has profiled it**, and every cost figure here inherits `95.389 s/epoch` unexamined. Smoke test: transform cost **flat from `N=24` to `N=32`** — per-call **overhead**, paid 20× per step. Two-sided; a YES is a **useful negative**. §C. **ANSWERED (`1f89ceb`, `writeup/data/p2_r_prof_v1.json`): 4.34× slower than the named reference (cpu median; wall 4.21; worst wall round 1.9975, so the unit's "every round exceeds 3×" is cpu-clock-only — Conductor finding). 79.1% transforms, fixed fraction 0.596. Remedy pre-planned FFTW3 3.41×, PRICED NOT LANDED — it perturbs every banked orbit at the last bit, which is `R4`'s problem, so it needs its own unit and its own equivalence check. A speedup breaks no wall.** |
| **R7** | **bank the seed fields** | **QUEUED 2026-08-19 — runs FIRST** — `R-bank` | The parallelism blocker is a **`.gitignore` line**: `u2_dns_ckpt.npy` (1.2 GB) is "never committed" and **died with a container once**, so every shard re-runs 3.4 h of DNS (~27 core-h at 8 shards). Fields are `24×24` f64 = **4,608 B**; **160 = 737 KB, committable**. §A. |
| **R5** | carry the `m` unknown | **DEFERRED** — = `PROG-R4` option **C** | One unit in two ledgers; do not double-count. |

**THE LANE-R RANKING — RULED 2026-08-18 BY THE CONDUCTOR: `R4` FIRST, `R2` SECOND, `R3` THIRD.**
Tie broken on **kind**: **`R4` is a VALIDITY fix, `R2`/`R3` are THROUGHPUT fixes.** `U3`'s stepper is Lie–Trotter, **first order, measured ratio 2.00**, so every
orbit either run produced is an `O(dt)` perturbation of the true flow's, and **deflating a
first-order solver buys faster production of objects whose status is in doubt.** `R4` can also
**falsify** something landed (`M1`); `R2` cannot — **57 core-hours bought ONE new orbit**. `R2`
beats `R3` because `R2`'s waste is **measured** and `R3`'s case is an inference. **`R4`'s first
unit is NOT a campaign re-run** (122.1 core-h): re-solve the **landed** orbits under a Strang
stepper, measure the displacement against the residual band. **§3g's floor stands — this ranks the
lane's units, it does not promote it.** Reasoning + §3k gate: `writeup/waves/WAVE7_PLAN.md` §0.
**No grinder** — the in-band arm cannot exceed 72 attempts ever.

**Live ban on this lane:** leg 349's GA gate answered NO (0 of 6 properties cleared). A **learned or
evolved** seed-scoring function is banned territory; R2–R5 are deterministic, keep it that way. **`E`
came within one conditional and did not touch it:** diagnostic (2) was pre-committed to name a
**score** fix if the low-`|s|` solutions were attractors of the **minimisation** rather than the
hookstep. It returned **`MIXED`** (97.1% constrained, `p = 0.9317`) — **not
`MINIMISATION_ATTRACTOR`** — so the conditional **did not fire and nothing was proposed.**

**A standing correction from R0 for every future Lane R claim:** `distinct orbits per core-hour`
removes re-finds **within** a run, not **between** runs; any comparison must state its convention, and
the denominator is **worker-hours** — physical core count appears in no numeric field of either JSON.

## C. Lane V — the viscous rung. **ACTIVE** (held 2026-08-18, **UN-HELD BY RULING**).

**The premise was measured, then ruled to have survived.** `V3` (leg 399, `16ba44e`) graded 9 fluid
blow-up CAPs against leg 174's **own, unchanged** criterion: **`arXiv:2509.25116` (Hou–Wang–Yang)
passes both clauses** — interval arithmetic (§7.3 p.55) enclosing a solution of a system carrying
`−ΔŨ` (Prop. 1 eq. (1.15) p.5) for the **unforced 3D incompressible Navier–Stokes equations** — and
had **never been graded here**. 8 rows `NO`, clause quoted per row; legs 309/342/123 **cited, not
redone**. Reading (a) — *a YES kills Lane V's premise* — **FIRED, honoured as written.**

**BUT THE OBJECT IS NOT A BLOW-UP** (paper's §1.2 p.2: forward self-similar, singular data, *"smooth
for positive times"*, concluding nonuniqueness of Leray–Hopf solutions). **RULED 2026-08-18 (Q1),
`RULING_W3_WORDING_2026-08-18.md`: W3's prose test governs, W3 STANDS, and the lane's premise
SURVIVES** — the certified singularity the lane exists to supply is still missing. The cell is
occupied and the wall stands; **these are two different claims.** **The YES remains UNAUDITED:** one
database, title-screened, S2 banked a **gap not a zero** (no key here).

**UNITS.**
- **`V3-audit`, ≈4–8 h — OBLIGATORY IN WAVE 6 (ruling Q4), no longer optional.** Adversarial
  full-text audit of `2509.25116` to leg-309 depth. **Scope fixed by the ruling:** enumerate the
  load-bearing constants **before** adjudicating; recompute what is recomputable; check the
  localisation step from the `ℝ³` self-similar profile to a genuine Leray–Hopf solution (Remark 2,
  §1.3 + §2); **pre-commit both branches**; and report as a **SEPARATE CLAUSE** whether the certified
  profile is genuinely 3D rather than symmetry-reduced — **it bears on W2, W2's own pre-committed
  test is the arbiter, and it must not be folded into the W3 verdict or claimed without the test.**
- **`V-net`, 6–10 h** — a real coverage net, ≥8 nets over ≥3 databases plus author pages. **Needs an
  S2 or OpenAlex key**, or half the channels bank `THROTTLED`.
- **`V2`** (wave 3 killed it without a byte) — name a dissipative fluid target, open the feasibility
  of a C1-compliant apparatus against it. **RE-OPENED by the ruling**: the cell is empty of a
  certified *singularity*, which is exactly its re-open condition. Unranked against `V3-audit`, which
  the ruling puts first.

**C1 binds every unit here, not waivable by the Conductor:** name the apparatus with a citation and
show it constructs no single bounded approximate inverse uniform in `M`; absent both, the ban applies
in full. **C1 may not be cited as evidence any apparatus closes for any object class.** **B1** struck
*"which needs L1 first"* from stage V's lift clause, so a fluid transport target attacked with a
dynamical closure is **outside both bans**.

**⚠ NEW 2026-08-18, FROM `V-W4` — AND IT IS A USER ESCALATION, NOT AN OPTION.** `arXiv:2509.25116`
**carries no journal-ref**: it is an **unrefereed preprint**, while `PUB_0C_CENSUS_SPINE.md` §1
speaks of *"any **published** work."* **The Conductor has not ruled it** — a defective criterion
wording is the user's. Packet: `writeup/escalations/ESCALATION_PUB0C_PUBLISHED_2026-08-18.md`.
**Nothing waits on it:** W3 stands on the prose test either way (ruling Q1), and `V3-audit` proceeds.

**`V-REPAIR` — the correction record `V-W4` earned, NOT a re-grading.** `D1`–`D4` are quote and
attribution defects in `V3`'s banked rows; `D5`/`D6` are the pin's provenance; `N1` is that
`326.875` per decade is **amplitude-dependent**, not portable. **Ruling Q3 governs: a correction
RECORD in `writeup/CORRECTIONS.md`, banked artefacts UNTOUCHED.** Cheap; ride it with a
construction unit rather than spend a slot. | **~1–2 h**

## D. Lane L — the last obligations. **ACTIVE, PRIORITY LANE (user ruling 2026-08-14).**

**The ruling's reason: Lane L is on every path.** Leg 390 measured that the torus does **not** retire
`CLAY_OBLIGATIONS.md` §6(i)/(ii) — **OPEN in both branches** — and (D)'s gain on §4 is *"the
acceptance test, not the work."* **Nothing queued anywhere retires them.**

**⚠ THREE UNITS LANDED, ALL NARROWING.** `L2′` shut W4 clause **(a)**, `L5` clause **(b)**, and `L6` (leg 401) priced route 4's construction for the first time. Recorded once at `WALLS.md` §W4.

| id | unit | what it is | cost |
|---|---|---|---|
| **L1**, **L2** | price §4 / attack §6(i) | **TAKEN by `L2′`, `1493e5e`, for the DECAY clause.** Pointer: `WALLS.md` §W4, `experiments/journal/leg_397.md` §§4–9. | — |
| **L1-res** | the 4 pre-arXiv primaries | **SUPERSEDED 2026-08-19 by `writeup/SOURCES.md`** (rows 2, 3, 19, 20). Live debt is NRŠ 1996 alone → `L7-src`. | see `L7-src` |
| **L4** | **certify the decay** | §6(i) wants *certified* decay + a built cutoff; `L2′` built neither. Interval/NK enclosure on route 4's own profile — **and `L6` measures that no accurate such profile exists yet (`ρ ≈ 1.6`), so `≥1 full wave` is a FLOOR, not an estimate** — plus a cutoff in a scaling-invariant norm. **`§6.2` predicts `α_hi = 1`, which does not pay the bill.** | **≥1 full wave** |
| **L5** | W4 clause (b) | **TAKEN and CLOSED, `4be46ef`.** Gate `NO`, threshold-free. Row retired 2026-08-19 → `WALLS_HISTORY.md` §OPTIONS-L5; substance at `WALLS.md` W4(b). | done |
| **L6** | bank a discrete route-4 profile | **LANDED leg 401, `NO`.** Route 4's first: `ρ = 1.6138` in `L5`'s norm at `n_dof = 6720`, far-field amplitude normalised to 1, **not decreasing under refinement** (`−0.0222`, last 3 rungs). **Ceiling found ON LANDING: the minimum is reached by ONE start — the continuation; 5 independent seeds land 10–24× higher and WORSEN with `n_dof`, all capped at 800 iters.** `WALLS.md` W4. | done, 2.30 h |
| **L7** | interval the commutator | **PRECONDITION NOT MET — "needs `L6` first" is discharged IN LETTER ONLY.** An enclosure needs a residual small enough for a contraction to close; `L6`'s is **1.6** against a unit-normalised field. **Do not dispatch until `L6-b` rules.** The `~10¹` price assumed banking a profile meant banking an ACCURATE one. | **re-price after `L6-b`** |
| **L6-b** | **is the stall the ANSATZ or the BUDGET?** | **NEW, from `L6`'s landing audit — cheapest thing that can overturn its `NO`.** Fix `n_dof = 6720`, start from `L6`'s banked minimiser, raise the cap **800 → 20,000**; two independent seeds too. `L6`'s own timing (1,240 s / start / 800 iters) prices it at ~8.6 h wall per start — **two orders below the ~10³ core-h `L6` priced for a full ladder.** Decisive both ways. | **~10–30 core-h** |
| **L3** | attack §6(ii) — persistence under localisation | Published persistence techniques (the Chen–Hou line, `arXiv:2308.01528`) **never read against this object**. **DEFERRED — `L3′` died in wave 3 without committing.** | — |

**The record's best lead on this lane arrived as a by-product** (§F): **`arXiv:2308.01528`, the
Chen–Hou line**, which `L3′` was to read at full text. **A measured, honest "still no method, and here
is precisely which hypothesis fails" is a real result** — the one that would tell the user whether the
Tier-2 ceiling is permanent.

## E. Lane T — **DEFERRED (user ruling 2026-08-14).** Whole section retired verbatim 2026-08-19 → `WALLS_HISTORY.md` §OPTIONS-LANE-T, beside `WALLS.md`'s §LANE-T.

**What still binds, and is not superseded:** the lane is deferred by RULING, not by measurement; **both re-open conditions are unchanged and neither has fired**; `T1`/`T4`/`T5`/`T6` are TAKEN; **`T2` returned `UNDER-RESOURCED`, not `no` — it is not a clearance**.

**`T2″`** (Type-I rigidity on `T³`) is re-open condition (ii) and **the cheapest thing that could put a live W4 clause back in front of Lane L — cost before ranking**. **`T3`** (the non-DSS `T³` ansatz) is the lane's undone mathematical content, **deferred, NOT killed**. `T1`'s ban-wording packet is open on the user's desk and **I may not rule it**.

## F. Other standing options, recorded so they are not lost

- **The DSS escalation packet** (legs 313/320) — **COMPLETE, retired** → `WALLS_HISTORY.md` §OPTIONS-F.
- **The three leg-382 follow-ups (389 CT2C, 387 DXNV, 388 CRVB) — ALL STILL OPEN.** Detail retired 2026-08-19 verbatim → `WALLS_HISTORY.md` §OPTIONS-382; each carries a MEASURED reason it stalled, so re-running one blind repeats a known failure.
- **`PROG-R4` U3's two owed novelty questions** — (i) are the **9 distinct solutions across both
  units** known in the literature at all? U5 contributed exactly one new, `T = 20.4175 / |s| = 0.5867`
  (stratum P, anchor UPO37), **the only solution either run found inside the published band**. (ii) Is
  the selection-bias caveat in `BLOG_P2_PROGR4_MINING_BAND.md` already published? Externally-facing
  and unchecked.

- **THE VERIFICATION DEBT — the standing §3f ledger.**
  **DISCHARGED:** waves 1–2, detail retired → `WALLS_HISTORY.md` §OPTIONS-F.
ain `UNVERIFIED`** — `V1` checked `R0`'s
  *reading* of them, not the runs. **`E` (wave 1, landed `d0d72b1`) is `UNVERIFIED`.** **`V-W2`
  (wave 3, landed `594ff89`) is `UNVERIFIED`.** Wave 3 landed nothing else. **A candidate emerging
  from an unverified pipeline is worth a fraction of one that did not.**

- **THE CHEN–HOU THREAD — the best lead the programme has on the compact-domain obstruction, found by
  `T6` as a near-miss it recorded rather than dropped.** `arXiv:2308.01528` §1 describes Chen–Hou as
  **computer-assisted blow-up on an UNBOUNDED domain in >1D with algebraic decay** — the exact
  combination leg 348's obstruction says the Galerkin-plus-tail bridge cannot reach. It **does not**
  fire U6 (target stationary self-similar not time-periodic; apparatus energy estimates not
  Galerkin-plus-tail), so it is no counter-instance to the obstruction as posed. **It is the sharpest
  available attack on the obstruction itself**, and it points at Lane L / route 4's actual geometry
  rather than `T³`. Unranked; ranking happens in a wave plan.

- **`O1`, THE TMS BUILD (leg 315) — RE-OPENABLE UNDER C1. Found by `T5`.** Sonic-point-desingularized
  **Taylor-model flow-map enclosure**. The C1 scope test passes on leg 315's own text: a flow map on a
  **finite-dimensional ODE**, which *"needs **no function space**."* Leg 315 refused it citing the ban
  and declined to lift it on its own reading. **The genuinely new item C1 bought** — and it points at
  **Lane V's direction, not Lane T's.** Still subject in full to C1's naming requirement. **Unranked
  and owned by no unit.**

- **LEG 257 IS *NOT* RE-OPENABLE, and the reason is the known live defect.** `T5` measured that its
  apparatus **is** the Corollary-21 radii polynomial (`capabilities.py:518-522`) merely in a **fourth
  space**, and C1 says a `Y₀/Z₀/Z₁/Z₂` contraction **in any space** is inside the ban. **A fourth
  SPACE is not a fourth APPARATUS.** Legs 262/273 refuse *spaces*, which would need a **lift**; C1 was
  a *scoping* and left that clause unrepaired. Recorded so no later unit mistakes the mismatch for an
  opening. **The wording defect is recorded, not ruled** — a ban-wording question is a user
  escalation, never a Conductor's call.

- **`fig107` IS NOT REGISTERED IN `build_figures.py`. Flagged by `E`; CONFIRMED BY THE CONDUCTOR.**
  `writeup/figures/fig107_prog_r4_m3_shift_strata.py` exists and its `.png` is banked, but the script
  is in **no** entry of `P2_EVIDENCE` — `build_figures.py` registers `fig108`/`fig109` and skips it.
  So fig107 is never rebuilt or self-checked and nothing detects it going stale against
  `p2_prog_r4_u5_v1.json`. One line, in numeric order. **Owed, not optional; lesson 68.**

- **A DISPATCH RULE `E` PAID FOR: MANDATORY CHECKPOINTING ABOVE ~1 h WALL.** The host killed `E`'s
  unattended run **twice**; it survived on per-attempt `.pkl` checkpoints. The rules adopted after the
  2026-08-14 process-exit incident — **commit early and often on the branch**, **poll long jobs from
  inside the turn** — are necessary but **were not sufficient**; what saved 5.7 core-hours was
  checkpointing *inside the computation*. **Every brief above ~1 h wall must require checkpointing to
  disk at a resumable granularity, and say where.** **Wave 3 paid for it again:** three of four units
  died and only the one that had committed left anything behind.
