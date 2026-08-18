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
| **A** | Spend the rest of the anchored pool — 141 attempts | ≈10.7 h | Grows the in-band arm 60 → 72 only. Lowest information per hour of the five, and buys supply. | Never on its own merits. |
| **B** | Relax the admission window to Chandler–Kerswell's `R_thres = 0.3` | ≈0.9 h re-mine + 0.0713 h/attempt (≈8 h for 100) (**wall**-h at 8 workers; the ~8× warning below is REFUTED) | Buys supply. Leaves the realization intact, so the U3/U5 baselines stay comparable — U5's second choice. **The supply multiplier cannot be read off U5's library** (pruned at 0.25); the re-mine is what measures it. | ~~E's diagnostic shows the in-band conversion penalty is *not* intrinsic.~~ **DID NOT FIRE — `E` returned and the penalty did not weaken.** One thing `E` left live: **the `R < 0.25` window remains a confound `E` could not separate**, and 1 of its 16 seeds deliberately sat outside it. So B re-opens only as *a measurement of that confound*, never as a supply buy. |
| **C** | Carry `m` as an unknown in the residual (= Lane R's **R5**) | own milestone, ≈10 h compute + solver work | Changes the realization, so M1's reproduction no longer compares attempt for attempt. **U5 priced it: 334 anchored in-window candidates, 58.1% of the window, but only 1 in the published band.** Not a band fix — the fix for `\|s\| > 0.9`. | On its own merits as the largest measured hole in the trial space, **not** as a route to the named rows. |
| **D** | Raise supply at source — longer DNS or finer `N` | ≈3.4 h per extra `T=1e5` + ≈0.9 h re-mine, plus attempts | Most expensive, buys supply, does nothing about H-hard. `N` refinement invalidates the banked library. | Only if the object itself changes and a fresh library is needed anyway. |

**`E` — THE H-HARD DIAGNOSTIC. TAKEN, LANDED `d0d72b1`, `UNVERIFIED`. Retired to one line plus a
pointer, §3j.** **2 of 16 converged, 0 recovered any named row**, both below the 0.15 `|s|` shelf;
positive control recovered through the unit's own predicate. **`E-iii` fired (→ `R3`/`R2`), `E-ii`'s
(→ `R4`) antecedent satisfied; the re-ranking between them is NOT made.** `experiments/journal/prog_r4_e.md`.

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
| **R5** | carry the `m` unknown | **DEFERRED** — same object as `PROG-R4` option **C** | One unit, listed in both ledgers because it arrived from two directions. Do not double-count. |

**THE LANE-R RANKING QUESTION `E` LEAVES OPEN, AND NO CONDUCTOR HAS RULED IT.** `E-iii` fired
(→ `R3`/`R2`) *and* `E-ii`'s antecedent is satisfied (→ `R4`). Both readings were pre-committed, both
honestly engaged, and they point at **different** units. **Which of `R2`/`R3`/`R4` is the highest-value
Lane R unit is a genuine re-ranking, and it belongs to a wave plan.** Not taken in wave 3 (no slot),
not taken in wave 4 (§3g's floor: **Lane R never sets a wave's direction**).

**Live ban on this lane:** leg 349's GA gate answered NO (0 of 6 properties cleared). A **learned or
evolved** seed-scoring function is banned territory; R2–R5 are deterministic, keep it that way. **`E`
came within one conditional and did not touch it:** diagnostic (2) was pre-committed to name a
**score** fix if the low-`|s|` solutions were attractors of the **minimisation** rather than the
hookstep. It returned **`MIXED`** (97.1% constrained, `p = 0.9317`) — **not
`MINIMISATION_ATTRACTOR`** — so the conditional **did not fire and nothing was proposed.**

**A standing correction from R0 for every future Lane R claim:** `distinct orbits per core-hour`
removes re-finds **within** a run, not **between** runs; any comparison must state its convention, and
the denominator is **worker-hours** — physical core count appears in no numeric field of either JSON.

## C. Lane V — the viscous rung. ~~*ACTIVE, PRIORITY.*~~ ~~**HELD 2026-08-18.**~~ **UN-HELD BY RULING.**

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

**⚠ 2026-08-18 — THE LANE LANDED TWO UNITS AND BOTH NARROWED IT.** `L2′` (`1493e5e`, **VERIFIED by `V-W4`**) shut W4 clause **(a)**; `L5` (`4be46ef`) shut clause **(b)**. Recorded once, at `WALLS.md` §W4, and not restated here.

| id | unit | what it is | cost |
|---|---|---|---|
| **L1**, **L2** | price §4 / attack §6(i) | **TAKEN by `L2′`, `1493e5e`, for the DECAY clause.** Pointer: `WALLS.md` §W4, `experiments/journal/leg_397.md` §§4–9. | — |
| **L1-res** | the 4 pre-arXiv primaries | NRŠ 1996, Tsai 1998, Bogovskiĭ 1979, Giga–Kohn banked **`UNREACHABLE` as declared in advance**, quoted through secondaries. **Low value.** No author contact — prohibited. | ~1 unit |
| **L4** | **certify the decay** | §6(i) wants *certified* decay + a built cutoff, and `L2′` built neither. Interval/NK enclosure on route 4's own profile + a cutoff controlled in a scaling-invariant norm. **`§6.2` predicts `α_hi = 1`, which does not pay the bill** — price that in before dispatching. | **≥1 full wave** |
| **L5** | W4 clause (b) | **TAKEN and CLOSED, `4be46ef`. GATE `NO`, threshold-free.** The ansatz does not escape the pin: what survives localisation is the modulation commutator `T3 ∝ ṁ`, size `ρ^{1-α}`, and `α = 1` makes it ρ-independent. `WALLS.md` §W4. | done |
| **L6** | **BANK A DISCRETE ROUTE-4 PROFILE** | `L5`'s own `UNDER-RESOURCED` residual, and the thing every Lane L number now waits on: **route 4 has no banked profile** (leg 382 line 174, leg 397 SS1), so `L5`'s exponent is a class property but its constant is a synthetic's. **This is construction, not reading.** | **~10² agent-h** |
| **L7** | interval the commutator | turn `L5`'s float exponent into a certified bound — a Route-D-style interval core over the annulus. **Needs `L6` first.** | ~10¹ agent-h **on top of L6** |
| **L3** | attack §6(ii) — persistence under localisation | The published persistence techniques (nonlinear stability with a finite unstable spectrum, the Chen–Hou line, `arXiv:2308.01528`) have **never been read against this object**. **DEFERRED — `L3′` died in wave 3 without committing.** | — |

**The record's best lead on this lane arrived as a by-product** (§F): **`arXiv:2308.01528`, the
Chen–Hou line**, which `L3′` was to read at full text. **A measured, honest "still no method, and here
is precisely which hypothesis fails" is a real result** — the one that would tell the user whether the
Tier-2 ceiling is permanent.

## E. Lane T — **THE LANE ITSELF IS DEFERRED (user ruling 2026-08-14)**, and its own held units

**WHAT DEFERRED THE LANE — a measurement, and it is the lane's own.** The lane was ranked priority 1
on four results lining up. **Item 3 fell**: `arXiv:1902.00384`, recorded as *the crack in W2*, is
certified by **exactly the banned apparatus** and **both of its certified rows are 2D lifts** —
`T4` from the authors' data package, `T6` from their prose, both VERIFIED. **The strongest of the
four arguments was that the technology was *demonstrated*. It is not.**

**THE COST OF DEFERRING, stated because a deferral with no cost line is a silent drop:** **`T3`, the
lane's real mathematical content, does not run** (deferred, **not killed** — the non-DSS `T³` ansatz
is open work nobody has done); **`T2′`** (≈1.2–1.7 h) does not run, so `T2`'s three coverage holes and
its `UNDER-RESOURCED` stand; **the credit leg 390 called *unclaimed* stays unclaimed** — deferring
neither collects nor concedes; and **(D)'s data conditions (8) and (9) stay unread** with leg 390 §5
item 1's `check_A` re-run still owed, cheap, unblocked, and parked with the lane.

**RE-OPEN CONDITIONS — either one is sufficient:**
1. **A demonstrated, genuinely-3D closure appears in the literature** — a certificate meeting **W2's
   own pre-committed test**, with its **three-dimensionality supplied by the certified object
   itself**: name the certified equation, show the dissipative term is inside it, and show the object
   is **not a lift**. *(A 2D lift does not re-open this lane. That is the measurement that closed it.)*
2. **`T2″` returns a rigidity picture favourable to a natively-periodic non-DSS ansatz.**

**WHAT IS NOT SUPERSEDED BY THE DEMOTION** (§3h rule 1): leg 348's **domain-shape obstruction is
still not refuted** (no counter-instance at full text either); **Theorem NGX**, **leg 341** and the
**three dead realizations** stand; **`W2` stands, strengthened**; and the `ℝ³` **exclusions still
reach** a `T³` object built by periodic extension of an `ℝ³` self-similar core (leg 309, GATE NO at
H11 — the one previous attempt at this lane's target, by anyone, died that way).

| id | unit | status |
|---|---|---|
| **T1**, **T4**, **T5**, **T6** | all TAKEN | **§3j — one line plus a pointer.** `T1` w1 gate `yes`, machine record DISCHARGED by `V-W2`, packet on the user's desk. `T4` `2c87244` **`STOP`**, `T5` `a6f0c38` **PASS** (left `O1` and leg 257, §F), `T6` `e7db624` **ANSWERED** 7/7 — all three VERIFIED by `V-W2`. Detail: `STATE.md` Landed. |
| **T2** | periodic-rigidity search | **TAKEN** w1, gate = no theorem located → **`UNDER-RESOURCED`, not `no`**. Not a clearance. |
| **T2′** | the **compliant** rigidity search | **DEFERRED, ≈1.2–1.7 h plus one user ruling.** Closes T2's three holes: NRS 1996 / Tsai 1998 are pre-arXiv (needs a forward-citation pass), Semantic Scholar was throttled on 5 of 6 substantive queries (needs an S2 key), battery `E` failed its own domain control (needs repair). |
| **T2″** | **the Type-I rigidity question on `T³`** | **DEFERRED — as of 2026-08-14 the ONLY thing keeping Lane T alive, and re-open condition 2.** The sharpest item the lane owns. A Type-I condition is a *rate* condition (`\|u\| ≲ (T−t)^{−1/2}`), needs **no dilation symmetry**, and carries to the torus intact **as a question**. Measured: `"Type I blowup" AND "periodic"` = **0**. Nothing located proves it. |
| **T3** | the non-DSS `T³` ansatz | ~~**OPEN — the priority unit.**~~ **DEFERRED WITH THE LANE — NOT KILLED.** Still the lane's real mathematical content; runs when a re-open condition is met. Binds: C1's naming requirement. |

## F. Other standing options, recorded so they are not lost

- **The DSS escalation packet** (legs 313/320, branches unmerged). Complete: both candidate theorems
  read at full text, neither reaches the screened object.
- **The three leg-382 follow-ups, all open.** **389 (CT2C)** wire 382's certified enclosure into the
  screen's second T2 column — but 386 clause 2 first: the δ-window is **EMPTY at every `α_centre ≤ 1`**
  and the banked object carries `α = 1`, so it reports an empty window and manufactures no headroom.
  **387 (DXNV)** discharge 382's owed novelty obligation; **leg 392 measured why it failed** — arXiv
  serves opensearch namespace `1.1`, 387's harness listed `1.0`, so it refused every response while
  reporting a zero, and **any re-run must use a namespace-agnostic parser**. **388 (CRVB)** bound
  382's curvature-detection threshold from below; the ladder bottomed out at ≤1e-6, one-sided.
- **`PROG-R4` U3's two owed novelty questions** — (i) are the **9 distinct solutions across both
  units** known in the literature at all? U5 contributed exactly one new, `T = 20.4175 / |s| = 0.5867`
  (stratum P, anchor UPO37), **the only solution either run found inside the published band**. (ii) Is
  the selection-bias caveat in `BLOG_P2_PROGR4_MINING_BAND.md` already published? Externally-facing
  and unchecked.

- **THE VERIFICATION DEBT — the standing §3f ledger.**
  **DISCHARGED:** wave 1 (`T1`, `T2`, `R0`+`R1`) by `V1`; wave 2 (`T4`, `T6`, `T5`) by `V-W2`, whose
  items (1) and (2) were re-measured from **re-fetched primary artefacts whose SHA-256 matched the
  banked digests exactly** — measurements, not transcription checks. `V-W2` also caught a Conductor
  wording defect and it was ruled at landing **against the Conductor's own wording** (`WALLS.md`
  History).
  **OUTSTANDING:** **`U2`, `U3` and `U5` themselves remain `UNVERIFIED`** — `V1` checked `R0`'s
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
