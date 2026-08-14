# OPTIONS — the deferred work ledger

**Adopted 2026-08-13 by user ruling: pursue Lane T, and record the other options so they are not
lost.** This file exists because `STATE.md` is regenerated at every landing and is deliberately
compact — anything living only in its "Open" section is one rewrite away from disappearing. Nothing
here has been rejected. Each entry carries **what it is, what it costs, why it is deferred, and what
would re-open it.**

**Nothing is deleted from this file.** An option that is later taken is marked `TAKEN` with its unit
and date; an option that is later killed is marked `KILLED` with the measurement that killed it. The
file only grows.

**Rule for the Conductor:** when a unit defers something, it lands here in the same commit. When a
wave is planned, this file is read alongside `STATE.md` — a deferred option whose re-open condition
has been met is a candidate for the wave, and the plan must say why it was or was not taken.

---

## A. `PROG-R4` — the four options the user did not take

U5 raised five costed options at `experiments/journal/prog_r4_u5.md` §9 and declined to choose.
**The user ruled option E on 2026-08-13** (the H-hard diagnostic, dispatched in wave 1). The other
four are recorded here in full.

**`E` HAS NOW RETURNED — landed `d0d72b1`, 2026-08-14 — and it changes the re-open conditions
below.** Its diagnostic (3) seeded all eight named Table IV rows directly at their published
`(T, s)` and **recovered none of them: 0 of 16, with a positive control proving the predicate can
return a recovery.** Read against these options: **the in-band conversion penalty was NOT shown to
be non-intrinsic, so option B's re-open condition did NOT fire** — if anything it hardened, because
the failure now survives at seed quality no amount of supply can beat. **A, B and D all still buy
supply, and supply is now refuted twice over.**

**The constraint shaping all of them:** the anchored admissible pool is **exhausted** at `R < 0.25`
— 241 exist, 100 spent, **141 remain of which only 12 are in-band** — so nothing that keeps the
current window can push the in-band arm past 72 attempts, ever.

**And the reason all of A/B/D are demoted rather than merely unqueued:** U5's pre-committed reading
fired on branch (b). The bias is in the **basin structure**, not the seed supply. A, B and D all buy
supply. H-supply is refuted on its own terms — its premise (the band was starved) was true and is
now repaired, and its prediction (more in-band seeds → recovery) is falsified at this scale.

| id | option | cost | why deferred | re-opens if |
|---|---|---|---|---|
| **A** | Spend the rest of the anchored pool — 141 attempts | ≈10.7 h | Grows the in-band arm 60 → 72 only. Lowest information per hour of the five, and it buys supply. | Never on its own merits; only as a by-product of something else needing the pool spent. |
| **B** | Relax the admission window to Chandler–Kerswell's `R_thres = 0.3` | ≈0.9 h re-mine + 0.0713 h/attempt (≈8 h for 100) — **but see the ~8× warning below** | Buys supply. Leaves the realization intact, so the U3/U5 baselines stay comparable — which is why it was U5's second choice. **The supply multiplier cannot be read off U5's library** (pruned at 0.25); the re-mine is what measures it. | ~~E's diagnostic shows the in-band conversion penalty is *not* intrinsic, i.e. H-hard weakens.~~ **DID NOT FIRE — `E` returned 2026-08-14 and the penalty did not weaken.** One thing `E` did leave live: **the `R < 0.25` window remains a confound `E` could not separate**, and 1 of its 16 seeds deliberately sat outside it. So B re-opens only as *a measurement of that confound*, never as a supply buy. |
| **C** | Carry `m` as an unknown in the residual (= Lane R's **R5**) | full unit, own milestone, ≈10 h compute + solver work | Changes the realization, so M1's reproduction no longer compares attempt for attempt. **U5 priced it: unlocks 334 anchored in-window candidates, 58.1% of the window, but only 1 of the 334 is in the published band.** Not a band fix — the fix for `\|s\| > 0.9`. | Taken on its own merits as the largest measured hole in the trial space, **not** as a route to the named rows. |
| **D** | Raise supply at source — longer DNS or finer `N` | ≈3.4 h per extra `T=1e5` + ≈0.9 h re-mine, plus attempts | Most expensive, buys supply, and does nothing about H-hard. `N` refinement invalidates the banked library entirely. | Only if the object itself changes and a fresh library is needed anyway. |

**Also deferred here: `U4`/`G2`, the basin radius.** Not an option — a **blocked unit**. It needs a
recovered *named* orbit to perturb and there is not one. The pre-committed reading makes it the unit
the basin-structure finding is really about, so it is the first thing to open if any named row is
ever recovered. **`E` HAS MADE THIS HARDER, NOT EASIER:** direct seeding at the published `(T, s)`
was the last cheap route to a recovered named orbit and it returned **0 of 16**. `U4` is now blocked
behind a *realization or method* change, not behind a budget.

**AND THE COST MODEL UNDER ALL FOUR OPTIONS IS WRONG BY ~8×, MEASURED.** `E` commissioned at
`0.0713 h/attempt` and measured **≈0.57 h/attempt** — 5.687 core-hours + 0.806 h of controls for 16
attempts, per-attempt sum 9.088 core-hours. **The reason is structural and applies to any option
that seeds well: good seeds do not fail fast.** The `0.0713` figure came from runs dominated by
quick rejections. **Every `h/attempt` number in the table above inherits this and should be treated
as a floor, not an estimate**, whenever the seeds are better than U3's mined ones. Costs `E` priced
but did not buy: **field ensemble ≈91 ch**, **`N=48` lift ≈730 ch**, **closing diagnostic (2)'s
coverage gap 122.1 ch**.

## B. Lane R — the units not taken

| id | unit | status | note |
|---|---|---|---|
| **R0** | the metric | **TAKEN**, wave 1, gate `yes` | Corrected `WALLS.md` twice and **retracted** "Lane R's first measured win". |
| **R1** | early abort on flatness | **TAKEN and CLOSED AGAINST ITSELF**, wave 1 | Already collected by U5 before commissioning; remaining headroom **+0.45 pp**; hold-out shows a rule tuned on U5's 9 convergences kills one of U3's 14. **Spend no more compute on this family.** |
| **R2** | deflation (Farrell–Birkisson–Funke) | **DEFERRED — and it is the strongest surviving Lane R item** | R0 measured the waste and it is worse than it looked: **57 of U5's 100 seeds were already spent by U3**, **5 of 9 convergences are bit-identical re-executions**, **4 of 5 distinct solutions are re-finds**, and U5's contribution new to the programme is **one orbit**. Deflate against the **union** of both runs' solutions, not just the current one's. Re-opens whenever Lane R gets a wave slot. |
| **R3** | multiple shooting | **DEFERRED** | Brick B6's own spec names it; U1 built the globalisation without it. Standard conditioning fix for long orbits, and long orbits are where the published targets live. **The basin-structure finding points here** — and `E`'s branch `E-iii` fired, which points here again. |
| **R4** | second-order-in-time stepper | **DEFERRED — AND `E` HAS JUST PROMOTED IT** | U3's is Lie–Trotter, globally **first** order (measured global ratio 2.00), so its periodic orbits are `O(dt)` perturbations of the true flow's; the published rates being competed against come from higher-order codes. Invalidates M1's reproduction — own milestone. **`E`'s pre-committed branch `E-ii` named `R4` in advance as where a non-recovery would point, and `E-ii`'s antecedent IS satisfied: 0 of 16 recovered any named row, seeded at the published coordinates themselves.** `E`'s leg-353 comparison is **the first evidence in this programme pointing at the REALIZATION rather than the budget** — a strictly better realization got strictly closer (residuals [0.80, 10.32] vs [22.5, 29.5]) from strictly **worse** seeds, and still recovered nothing. |
| **R5** | carry the `m` unknown | **DEFERRED** — same object as `PROG-R4` option **C** above | Do not double-count these: one unit, listed in both ledgers because it arrived from two directions. |

**Live ban on this lane:** leg 349's GA gate answered NO (0 of 6 properties cleared). A **learned or
evolved** seed-scoring function is banned territory. R2–R5 are all deterministic; keep it that way.
**`E` came within one conditional of touching this and did not:** its diagnostic (2) was
pre-committed to name a **score** fix if the low-`|s|` solutions turned out to be attractors of the
**minimisation** rather than the hookstep. It returned **`MIXED`** (97.1% constrained, `p = 0.9317`)
— **not `MINIMISATION_ATTRACTOR`** — so the conditional **did not fire and nothing was proposed.**
The "trust region drags us downhill" story was **tested and declined**, not assumed away.

**THE LANE-R RANKING QUESTION `E` LEAVES OPEN, AND THIS CONDUCTOR HAS NOT RULED IT.** `E-iii` fired
(→ `R3`/`R2`) *and* `E-ii`'s antecedent is satisfied (→ `R4`). Both readings were pre-committed;
both are honestly engaged; they point at **different** units. `E` reported `E-iii` as the more
specific and recorded `E-ii` openly rather than suppressing it — the right call at the unit's level.
**Which of `R2`/`R3`/`R4` is now the highest-value Lane R unit is a genuine re-ranking and it
belongs to whoever plans wave 3, against `WALLS.md` and this file.**

**A standing correction from R0 that applies to every future Lane R claim:** the metric
`distinct orbits per core-hour` removes re-finds **within** a run and not **between** runs. Any
future comparison must state which convention it uses, and the denominator is **worker-hours** —
physical core count appears in no numeric field of either JSON and was **not estimated**.

## C. Lane V — the viscous rung. NOT STARTED.

**Attacks W3: the Grade-A × fluid cell is empty**, and empty **"for want of a target, not a
method"** (leg 174's own words; leg 242 confirms nobody filled it since).

**Deferred by the 2026-08-13 ruling to pursue Lane T, not by any measurement.** Recorded in full
because it is the only lane whose *negative branch* is as valuable as its positive one: if a viscous
blow-up cannot be certified for a dissipative fluid equation in **one** dimension, then 3D
Navier–Stokes is not a question of compute and the honest ceiling of the whole programme is Tier 2.

**STATUS CORRECTED 2026-08-13: DEFERRED BY PRIORITY, NOT BLOCKED.** Both halves of `V1` are now
open. The user ruled **(b) = B1**, striking *"which needs L1 first"* from stage V's lift clause, and
**(c) = C1**, putting a Galerkin-plus-tail dynamical closure outside the ℓ¹-Fourier/radii-polynomial
ban. **A fluid transport target attacked with a dynamical closure is outside both bans** — subject in
full to C1's naming requirement (name the apparatus; show it does not construct a single bounded
approximate inverse uniform in `M`). See `writeup/escalations/RULING_BAN_WORDING_2026-08-13.md`.

**`V1`, the opening unit, has two halves and NEITHER is now blocked:**
- **Was blocked, now open:** the stage-V ban's lift condition read *"unless the question is re-posed
  for a FLUID transport model, which needs L1 first"* — and L1 has three dead attempts and no fourth
  candidate, so the precondition was **unliftable as written**. **RULED B1 2026-08-13: the clause is
  editorial and the precondition is STRUCK.**
- **Needs no ruling:** **name the target.** Leg 174 says the cell is empty for want of one, so
  supplying a named dissipative fluid target — 1D, any model, dissipative term inside the certified
  equation — is unblocked work that can proceed while (b) is pending.

**Re-opens:** the moment Lane T is either killed or blocked for longer than a wave, or on any user
ruling that wants the Tier-3-reachability question answered directly.

## D. Lane L — the last obligations. NOT STARTED.

**`CLAY_OBLIGATIONS.md` §6's two obligations with NO KNOWN METHOD are the literal last things
between a Tier-2 candidate and a Clay answer**, and **no unit in 390 legs has ever attacked either.**
Leg 390 checked whether the torus disposes of them and recorded that it does **not** — they stay
**OPEN in both branches**, and (D)'s gain on §4 is *"the acceptance test, not the work."* So Lane T
does not retire them; nothing currently queued does.

| id | unit | what it is |
|---|---|---|
| **L1** | price §4 on `ℝ³` | Read the published attempts to localise a self-similar profile to finite energy; state, **per attempt**, the named hypothesis that fails for DSS. Converts an assumption into a measurement. |
| **L2** | attack §6(i) — certified far-field decay + admissible cutoff | Leg 381 banked the bill: `L³` tail **326.875 per decade**, required `α > 1.5` against available `α = 1.0`. **A deficit of 0.5 in a decay exponent is a number, not an impossibility**, and no unit has ever asked what would supply it. **The most tractable-looking item on the entire no-method list.** |
| **L3** | attack §6(ii) — persistence under localisation | The published techniques for persistence of singular behaviour under perturbation (nonlinear stability with a finite unstable spectrum, the Chen–Hou line) have **never been read against this object**. |

**Deferred by the 2026-08-13 ruling, not by any measurement.** **Re-opens** whenever the wave
composition floor (`ORCHESTRATION.md` §3g) needs a Clay-chain unit and Lane T cannot supply one —
which is the live situation whenever Lane T is blocked on a ruling.

**A measured, honest "still no method, and here is precisely which hypothesis fails" is a real
result** — it is the one that would tell the user whether the Tier-2 ceiling is permanent.

## E. Lane T's own held units

| id | unit | status |
|---|---|---|
| **T1** | ban-wording escalation packet | **TAKEN**, wave 1, gate `yes`. Packet open on the user's desk. |
| **T2** | periodic-rigidity literature search | **TAKEN**, wave 1, gate = no theorem located → **`UNDER-RESOURCED`, not `no`**. Not a clearance. |
| **T2′** | the **compliant** rigidity search | **DEFERRED, costed at ≈1.2–1.7 h plus one user ruling.** Closes T2's three coverage holes: NRS 1996 / Tsai 1998 are pre-arXiv (needs a forward-citation pass), Semantic Scholar was throttled on 5 of 6 substantive queries (needs an S2 key), and battery `E` failed its own domain control (needs repair). |
| **T2″** | **the Type-I rigidity question on `T³`** | **DEFERRED — and it is the sharpest item Lane T owns.** A Type-I condition is a *rate* condition (`\|u\| ≲ (T−t)^{−1/2}`), needs **no dilation symmetry**, and so carries to the torus intact **as a question**. Measured: `"Type I blowup" AND "periodic"` = **0**. Nothing located proves it. This is what a Lane T ansatz must survive or evade. |
| **T3** | the non-DSS `T³` ansatz | **OPEN — RULED C1 2026-08-13.** The lane's real mathematical content, and the priority unit. Binds: C1's naming requirement. |
| **T4** | reproduce `arXiv:1902.00384` row for row | **OPEN — RULED C1 2026-08-13.** Precedent: leg 316 reproduced Dahne–Figueras row-for-row **while this ban was in force**, clearing it by individuating on the three realizations. |
| **T5** | **THE C1 SWEEP — an obligation of the ruling, not an option** | Grep the landed record for legs that declined, deferred or narrowed work citing the ℓ¹-Fourier/radii-polynomial ban, and report which of those refusals were **apparatus-based** and are now permitted under C1. The honest price of narrowing a ban, and it has never been paid for any ban here. |
| **T6** | **discharge leg 348's own recorded ceiling** | Leg 348 read its seven papers **at abstract level only** and flagged that a full-text pass could strengthen *or undercut* its classification. Lane T rests entirely on that classification, and the 2026-08-13 narrowing of the outreach hold makes full text readable. Cheap, and it can undercut the lane. |

## F. Other standing options, recorded so they are not lost

- **The DSS escalation packet** (legs 313/320, branches unmerged). Complete: both candidate theorems
  read at full text and neither reaches the screened object.
- **Leg 389 (CT2C)** — wire 382's certified enclosure into the screen's second T2 column. Note 386's
  clause 2 first: the δ-window is **EMPTY at every `α_centre ≤ 1`** and the banked object carries
  `α = 1`, so this reports an empty window honestly and does not manufacture headroom.
- **Leg 387 (DXNV)** — discharge 382's owed novelty obligation, after arXiv and Semantic Scholar
  both returned HTTP 429. **Leg 392 measured the cause of leg 387's failure**: arXiv serves the
  opensearch namespace `1.1` and leg 387's harness listed `1.0`, so it refused every response while
  reporting a zero. Any re-run must use a namespace-agnostic parser.
- **Leg 388 (CRVB)** — bound 382's curvature-detection threshold from below; the ladder bottomed out
  at ≤1e-6 and is currently one-sided.
- **`PROG-R4` U3's two owed novelty questions** — (i) are the **9 distinct solutions across both
  units** known in the literature at all? U5 contributed exactly one new one,
  `T = 20.4175 / |s| = 0.5867` (stratum P, anchor UPO37), **the only solution either run has found
  inside the published band**. (ii) Is the selection-bias caveat in
  `BLOG_P2_PROGR4_MINING_BAND.md` already published? It is externally-facing and unchecked.
- **The verification debt.** Every `PROG-R4` unit — U2, U3, U5 — and both wave-1 Lane R units are
  **`UNVERIFIED`** under §3f. A candidate emerging from an unverified pipeline is worth a fraction
  of one that did not.
  **UPDATED 2026-08-14 — PARTIALLY DISCHARGED.** `V1` (`verify/wave1`, landed) verified the wave-1
  units `T1`, `T2` and `R0`+`R1`: all five claims reproduce from banked JSON and landed evidence
  scripts alone, and `M3 = DELIVERED` survives U5's 57% seed overlap on M3's own pre-committed
  wording. **`U2`, `U3` and `U5` themselves remain `UNVERIFIED`** — `V1` checked `R0`'s *reading* of
  them, not the runs. **Wave 2's own units are `UNVERIFIED` and wave 3 must carry their verifier.**

- **THE CHEN–HOU THREAD — the best lead the programme now has on the compact-domain obstruction.
  Found by `T6`, 2026-08-14, as a near-miss it recorded rather than dropped.** `arXiv:2308.01528` §1
  describes Chen–Hou as **computer-assisted blow-up on an UNBOUNDED domain in >1D with algebraic
  decay** — which is the exact combination leg 348's obstruction says the Galerkin-plus-tail bridge
  cannot reach. It **does not** fire U6: the target is stationary self-similar rather than
  time-periodic, and the apparatus is energy estimates rather than Galerkin-plus-tail. So it is not
  a counter-instance to the obstruction as posed. **It is the sharpest available attack on the
  obstruction itself**, and it points at Lane L / route 4's actual geometry rather than at `T³`.
  Unranked here; ranking is done in a wave plan, not in the ledger.

- **`O1`, THE TMS BUILD (leg 315) — RE-OPENABLE UNDER C1. Found by `T5`, 2026-08-14.** Sonic-point-
  desingularized **Taylor-model flow-map enclosure**. The C1 scope test passes on leg 315's own
  text: a flow map on a **finite-dimensional ODE**, which *"needs **no function space**."* Leg 315
  refused it citing the ban and explicitly declined to lift it on its own reading. **This is the
  genuinely new item C1 bought**, and note where it points — **Lane V's direction, not Lane T's.**
  Still subject in full to C1's naming requirement. `T5` ranked nothing and neither does this entry.

- **LEG 257 IS *NOT* RE-OPENABLE, and the reason is the known live defect.** `T5` measured that leg
  257's apparatus **is** the Corollary-21 radii polynomial (`capabilities.py:518-522`) merely in a
  **fourth space** — and C1 says a `Y₀/Z₀/Z₁/Z₂` contraction **in any space** is inside the ban.
  **A fourth SPACE is not a fourth APPARATUS.** Legs 262 and 273 refuse *spaces*, which would need a
  **lift**; C1 was a *scoping* and left that clause unrepaired. Recorded so no later unit mistakes
  the fourth-space mismatch for an opening.

- **`T1` OWES A MACHINE RECORD. Found by `V1`, 2026-08-14; an obligation, not an option.** Leg 391
  landed **no `writeup/data/*.json` and no evidence script**. Its gate answer checks out against
  **prose only** — `writeup/escalations/ESCALATION_BAN_WORDING_2026-08-13.md`. Confirmed by a
  field-scoped scan of every banked JSON's `leg`/`route`/`unit` fields: **zero hits**. Lesson 68
  says a check that is not executable decays at the rate of memory, and T1's does not exist. **This
  does not disturb T1's gate answer** and is not evidence the claim is false (`V1` reading (c)); it
  is a banking-discipline defect in a unit this Conductor landed. Owed: a banked record of the
  packet's three questions and the fact that it ruled none of them, with an evidence script that
  exits non-zero if the record and the escalation document disagree. Cheap — well under an hour.
  **Note for whoever takes it:** filename-substring search is insufficient and will mislead you —
  `p2_route_p2t1_v1.json` is **leg 302, route P2T1**, unrelated.

- **`fig107` IS NOT REGISTERED IN `build_figures.py`. Flagged by `E`, 2026-08-14; CONFIRMED BY THE
  CONDUCTOR.** `writeup/figures/fig107_prog_r4_m3_shift_strata.py` exists (15,094 bytes, U5's M3
  shift-strata figure) and its `.png` is banked, but the script appears in **no** entry of
  `P2_EVIDENCE` — `build_figures.py` registers `fig108` and `fig109` and skips `fig107`. **`E`
  flagged it and correctly did NOT fix it: `build_figures.py` was outside its territory**, and its
  diff there is `+1/-0`. Consequence: fig107 is **not rebuilt or self-checked by the figure build**,
  so nothing detects it going stale against `p2_prog_r4_u5_v1.json`. Trivial to repair — one line,
  in the same list, in numeric order. **Owed, not optional; lesson 68 again.**

- **`E` OWES A `writeup/INDEX.md` ROW, and so does every wave-2 unit.** `E` flagged that it landed no
  INDEX row because `INDEX.md` was outside its territory — correct behaviour. Confirmed: `INDEX.md`
  carries U5's fig107 row and **no row for `E`/fig109**. **This is a Conductor-owned file and
  therefore a CONDUCTOR-OWNED DEBT**, not a worker's: `T4`, `T6`, `T5`, `V1` and `E` all landed
  without INDEX rows because this Conductor did not put `INDEX.md` in anyone's territory and did not
  write the rows itself. Owed: five rows, or an explicit ruling that `INDEX.md` is retired.

- **A DISPATCH RULE `E` PAID FOR: MANDATORY CHECKPOINTING ABOVE ~1 h WALL.** `E` reports **the host
  killed its unattended run twice**; it survived because it wrote per-attempt `.pkl` checkpoints and
  resumed from them (the stage-3 log shows eight attempts *"reused from checkpoint"*). The two rules
  already adopted after the 2026-08-14 process-exit incident — **commit early and often on the
  unit's branch**, **poll long jobs from inside the turn** — are necessary but **were not sufficient
  on their own**; what actually saved this unit's 5.7 core-hours was checkpointing *inside the
  computation*. **Add to every brief whose compute exceeds ~1 h wall: the unit must checkpoint to
  disk at a granularity it can resume from, and must say where.**
