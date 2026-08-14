# OPTIONS — the deferred work ledger

> ## ⚠ THE LANE RANKING CHANGED ON 2026-08-14 — READ THIS BEFORE ANY ENTRY BELOW
>
> **USER RULING 2026-08-14** (`writeup/escalations/RULING_C1_EXEMPLAR_2026-08-14.md`, discharging
> `ESCALATION_C1_EXEMPLAR_2026-08-14.md`):
>
> - **LANE V — ACTIVE, PRIORITY LANE.** §C below. It decides whether **Tier 3 is reachable in
>   principle**; both branches are valuable.
> - **LANE L — ACTIVE, PRIORITY LANE.** §D below. It is **on every path**: leg 390 measured that
>   the torus does **not** retire `CLAY_OBLIGATIONS.md` §6(i)/(ii), so the two no-method
>   obligations are the last blockers on **every** branch, and **no unit in 395 legs has attacked
>   either.**
> - **LANE T — DEMOTED TO DEFERRED.** §E below carries its cost and its two re-open conditions, per
>   this file's own rule. Kept alive **only through `T2″`**. **`T3` is deferred with the lane, not
>   killed.** **Nothing measured is superseded** — the domain-shape obstruction is still not
>   refuted, Theorem NGX / leg 341 / the three dead realizations stand, and **W2 stands
>   strengthened.**
> - **LANE R — unchanged.** Runs continuously inside every unit's pre-registration and takes its
>   own units when a wave has room.
> - **C1 STANDS, EXEMPLAR-FREE**, and the scope **no longer carries any implied *"and this has been
>   demonstrated"***: **no unit may cite C1 as evidence the technology closes for any object
>   class.** Its **naming requirement is unchanged and binds every unit.**
> - **No ban is lifted, narrowed or reworded.** 26 recorded / 19 in force, unchanged.
>
> **The 2026-08-13 ruling's "pursue Lane T" is superseded as a RANKING only.** Every measurement
> that ruling rested on, and every other item it decided (A2, B1, the narrowed outreach hold),
> stands untouched.

**Adopted 2026-08-13 by user ruling: pursue Lane T, and record the other options so they are not
lost.** *(Superseded as a ranking 2026-08-14 — see the block above; retained because this file's
rule is that nothing is deleted from it.)* This file exists because `STATE.md` is regenerated at
every landing and is deliberately
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
| **B** | Relax the admission window to Chandler–Kerswell's `R_thres = 0.3` | ≈0.9 h re-mine + 0.0713 h/attempt (≈8 h for 100) | Buys supply. Leaves the realization intact, so the U3/U5 baselines stay comparable — which is why it was U5's second choice. **The supply multiplier cannot be read off U5's library** (pruned at 0.25); the re-mine is what measures it. | E's diagnostic shows the in-band conversion penalty is *not* intrinsic, i.e. H-hard weakens. |
| **C** | Carry `m` as an unknown in the residual (= Lane R's **R5**) | full unit, own milestone, ≈10 h compute + solver work | Changes the realization, so M1's reproduction no longer compares attempt for attempt. **U5 priced it: unlocks 334 anchored in-window candidates, 58.1% of the window, but only 1 of the 334 is in the published band.** Not a band fix — the fix for `\|s\| > 0.9`. | Taken on its own merits as the largest measured hole in the trial space, **not** as a route to the named rows. |
| **D** | Raise supply at source — longer DNS or finer `N` | ≈3.4 h per extra `T=1e5` + ≈0.9 h re-mine, plus attempts | Most expensive, buys supply, and does nothing about H-hard. `N` refinement invalidates the banked library entirely. | Only if the object itself changes and a fresh library is needed anyway. |

**Also deferred here: `U4`/`G2`, the basin radius.** Not an option — a **blocked unit**. It needs a
recovered *named* orbit to perturb and there is not one. The pre-committed reading makes it the unit
the basin-structure finding is really about, so it is the first thing to open if any named row is
ever recovered.

## B. Lane R — the units not taken

| id | unit | status | note |
|---|---|---|---|
| **R0** | the metric | **TAKEN**, wave 1, gate `yes` | Corrected `WALLS.md` twice and **retracted** "Lane R's first measured win". |
| **R1** | early abort on flatness | **TAKEN and CLOSED AGAINST ITSELF**, wave 1 | Already collected by U5 before commissioning; remaining headroom **+0.45 pp**; hold-out shows a rule tuned on U5's 9 convergences kills one of U3's 14. **Spend no more compute on this family.** |
| **R2** | deflation (Farrell–Birkisson–Funke) | **DEFERRED — and it is the strongest surviving Lane R item** | R0 measured the waste and it is worse than it looked: **57 of U5's 100 seeds were already spent by U3**, **5 of 9 convergences are bit-identical re-executions**, **4 of 5 distinct solutions are re-finds**, and U5's contribution new to the programme is **one orbit**. Deflate against the **union** of both runs' solutions, not just the current one's. Re-opens whenever Lane R gets a wave slot. |
| **R3** | multiple shooting | **DEFERRED** | Brick B6's own spec names it; U1 built the globalisation without it. Standard conditioning fix for long orbits, and long orbits are where the published targets live. **The basin-structure finding points here.** |
| **R4** | second-order-in-time stepper | **DEFERRED** | U3's is Lie–Trotter, globally **first** order (measured global ratio 2.00); the published rates being competed against come from higher-order codes. Invalidates M1's reproduction — own milestone. |
| **R5** | carry the `m` unknown | **DEFERRED** — same object as `PROG-R4` option **C** above | Do not double-count these: one unit, listed in both ledgers because it arrived from two directions. |

**Live ban on this lane:** leg 349's GA gate answered NO (0 of 6 properties cleared). A **learned or
evolved** seed-scoring function is banned territory. R2–R5 are all deterministic; keep it that way.

**A standing correction from R0 that applies to every future Lane R claim:** the metric
`distinct orbits per core-hour` removes re-finds **within** a run and not **between** runs. Any
future comparison must state which convention it uses, and the denominator is **worker-hours** —
physical core count appears in no numeric field of either JSON and was **not estimated**.

## C. Lane V — the viscous rung. **ACTIVE, PRIORITY LANE (user ruling 2026-08-14).**

**STATUS 2026-08-14: ACTIVE. `V2` is dispatched in wave 3 and is that wave's centre of gravity.**
The lane is no longer deferred by anything. The ruling's reason, in its own terms: **Lane V decides
whether any path exists** — `W3` is the rung that determines whether **Tier 3 is reachable in
principle**, and the information is worth as much on the negative branch as on the positive one.

**Two record items point here, and neither was found by looking for it:**
- **`O1`, leg 315's Taylor-model flow-map build** (§F below) — the genuinely new item C1 bought, a
  flow map on a finite-dimensional ODE that *"needs **no function space**."* It points at **this
  lane's direction, not Lane T's**, and `T5` found it while sweeping for Lane T.
- **Leg 174's own diagnosis** that the Grade-A × fluid cell is empty **"for want of a target, not a
  method"** — which makes *naming the target* the lane's first job, and `V2`'s.

**Binding on every unit here: C1's naming requirement**, unwaivable by the Conductor — name the
apparatus with a citation, and show it does not construct a single bounded approximate inverse
uniform in `M`. Absent both, the ℓ¹-Fourier/radii-polynomial ban applies in full. **And C1 may not
be cited as evidence any apparatus closes** for this or any object class.

*(Original entry, retained unchanged below.)*

**Attacks W3: the Grade-A × fluid cell is empty**, and empty **"for want of a target, not a
method"** (leg 174's own words; leg 242 confirms nobody filled it since).

~~**Deferred by the 2026-08-13 ruling to pursue Lane T, not by any measurement.**~~ **NO LONGER
DEFERRED — ACTIVE AND PRIORITY, user ruling 2026-08-14.** Recorded in full
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

~~**Re-opens:** the moment Lane T is either killed or blocked for longer than a wave, or on any user
ruling that wants the Tier-3-reachability question answered directly.~~ **RE-OPENED 2026-08-14 on
the second clause: the user ruled the Tier-3-reachability question to be a priority.**

## D. Lane L — the last obligations. **ACTIVE, PRIORITY LANE (user ruling 2026-08-14).**

**STATUS 2026-08-14: ACTIVE. `L2` and `L3′` are dispatched in wave 3 — the first units ever
dispatched at a final blocker.** The ruling's reason, in its own terms: **Lane L is on every path.**
Leg 390 measured that the torus does **not** retire `CLAY_OBLIGATIONS.md` §6(i)/(ii); the two
no-method obligations are therefore the last blockers on **every** branch, and **no unit in 395 legs
has ever attacked either.**

**The record's best lead on this lane arrived as a by-product**, found by `T6` and recorded rather
than dropped: **`arXiv:2308.01528` and the Chen–Hou line** — computer-assisted blow-up, **unbounded**
domain, **>1D**, **algebraic decay** — the exact combination leg 348's obstruction says the
Galerkin-plus-tail bridge cannot reach. It points at **route 4's actual `ℝ³` geometry — prize
statement (C)**. `L3′` reads it at full text. See §F.

*(Original entry, retained unchanged below.)*

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

~~**Deferred by the 2026-08-13 ruling, not by any measurement.** **Re-opens** whenever the wave
composition floor (`ORCHESTRATION.md` §3g) needs a Clay-chain unit and Lane T cannot supply one —
which is the live situation whenever Lane T is blocked on a ruling.~~ **RE-OPENED 2026-08-14 AND
PROMOTED TO A PRIORITY LANE by user ruling — not by the composition floor, and not because Lane T
stalled, but because §6(i)/(ii) are the last blockers on every branch.**

**A measured, honest "still no method, and here is precisely which hypothesis fails" is a real
result** — it is the one that would tell the user whether the Tier-2 ceiling is permanent.

## E. Lane T — **THE LANE ITSELF IS DEFERRED (user ruling 2026-08-14)**, and its own held units

**LANE T IS DEMOTED FROM PRIORITY 1 TO DEFERRED.** Recorded here with its cost and its re-open
conditions, per this file's own rule, exactly as every other deferred option is.

**WHAT DEFERRED THE LANE — a measurement, and it is the lane's own.** The lane was ranked priority 1
on four results lining up. **Item 3 of the four fell**: `arXiv:1902.00384`, recorded as *the crack in
W2*, is certified by **exactly the banned apparatus** and **both of its certified rows are 2D lifts**
(leg 393 / `T4`, `2c87244`, from the authors' data package; replicated independently by leg 394 /
`T6`, `e7db624`, from the authors' prose). **The strongest of the four arguments was that the
technology was *demonstrated*. It is not.** The user ruled that the priority-1 ranking does not
survive that loss.

**THE COST OF DEFERRING, stated because a deferral with no cost line is a silent drop:**
- **`T3`, the lane's real mathematical content, does not run.** It is **deferred with the lane, NOT
  killed.** The non-DSS `T³` ansatz remains open work nobody has done.
- **`T2′`** (the compliant rigidity search, ≈1.2–1.7 h now that the ruling has landed) does not run,
  so `T2`'s three coverage holes stay open and its `UNDER-RESOURCED` stays under-resourced.
- **The credit leg 390 called *unclaimed* stays unclaimed.** Deferring the lane does not collect it
  and does not concede it.
- **(D)'s data conditions (8) and (9) stay unread**, and leg 390 §5 item 1's owed `check_A` re-run
  stays owed. Cheap, unblocked, and now parked with the lane.

**RE-OPEN CONDITIONS — either one is sufficient, and both are stated so no later unit has to guess:**
1. **A demonstrated, genuinely-3D closure appears in the literature** — a certificate meeting **W2's
   own pre-committed test**, with its **three-dimensionality supplied by the certified object
   itself**: name the certified equation, show the dissipative term is inside it, and show the
   object is **not a lift** of a lower-dimensional one. *(A 2D lift does not re-open this lane. That
   is the measurement that closed it.)*
2. **`T2″` returns a rigidity picture favourable to a natively-periodic non-DSS ansatz.**

**WHAT IS NOT SUPERSEDED BY THE DEMOTION** — a ranking is a decision, and a decision supersedes no
measurement (§3h rule 1): the **domain-shape obstruction leg 348 named is still not refuted** (no
counter-instance appeared at full text either); **Theorem NGX** stands; **leg 341** stands; the
**three dead realizations** stay dead; **`W2` stands, strengthened**; and the `ℝ³` **exclusions still
reach** a `T³` object built by periodic extension of an `ℝ³` self-similar core (leg 309, GATE NO at
H11 — the one previous attempt at this lane's target, by anyone, died that way).

**`T2″` IS WHAT KEEPS THE LANE ALIVE.** It survives the exemplar's fall intact — a Type-I condition
is a **rate** condition, needs **no dilation symmetry**, and so carries to the torus **as a
question** whatever happened to `1902.00384`. It stays **deferred**, as the lane's sharp question and
as re-open condition 2.

| id | unit | status |
|---|---|---|
| **T1** | ban-wording escalation packet | **TAKEN**, wave 1, gate `yes`. Packet open on the user's desk. |
| **T2** | periodic-rigidity literature search | **TAKEN**, wave 1, gate = no theorem located → **`UNDER-RESOURCED`, not `no`**. Not a clearance. |
| **T2′** | the **compliant** rigidity search | **DEFERRED, costed at ≈1.2–1.7 h plus one user ruling.** Closes T2's three coverage holes: NRS 1996 / Tsai 1998 are pre-arXiv (needs a forward-citation pass), Semantic Scholar was throttled on 5 of 6 substantive queries (needs an S2 key), and battery `E` failed its own domain control (needs repair). |
| **T2″** | **the Type-I rigidity question on `T³`** | **DEFERRED — and as of 2026-08-14 it is the ONLY thing keeping Lane T alive, and re-open condition 2 for the lane.** The sharpest item Lane T owns. A Type-I condition is a *rate* condition (`\|u\| ≲ (T−t)^{−1/2}`), needs **no dilation symmetry**, and so carries to the torus intact **as a question**. Measured: `"Type I blowup" AND "periodic"` = **0**. Nothing located proves it. This is what a Lane T ansatz must survive or evade. |
| **T3** | the non-DSS `T³` ansatz | ~~**OPEN — RULED C1 2026-08-13.** … the priority unit.~~ **DEFERRED WITH THE LANE 2026-08-14 — NOT KILLED.** Still the lane's real mathematical content, still open work, and it runs when a re-open condition above is met. Binds: C1's naming requirement. |
| **T4** | reproduce `arXiv:1902.00384` row for row | **TAKEN**, wave 2, leg 393, **gate = `STOP` under pre-committed branch (c)** (`2c87244`). The paper is certified by **exactly the banned apparatus** and both certified rows are **2D lifts**. **CLOSED — there is nothing here to re-open**; it is the measurement that demoted the lane. |
| **T5** | **THE C1 SWEEP — TAKEN, wave 2, leg 395, gate = PASS** (`a6f0c38`): 7 refusals, APPARATUS 5 / REALIZATION 2, **2 re-openable and UNRANKED**, one of them (`O1`) pointing at **Lane V**. Original entry: | Grep the landed record for legs that declined, deferred or narrowed work citing the ℓ¹-Fourier/radii-polynomial ban, and report which of those refusals were **apparatus-based** and are now permitted under C1. The honest price of narrowing a ban, and it has never been paid for any ban here. |
| **T6** | **discharge leg 348's ceiling — TAKEN, wave 2, leg 394, gate ANSWERED** (`e7db624`): 7/7 at full text, **2 UNDERCUT** / 4 strengthen / 1 confirm, 0 `UNREACHABLE`, 0 `THROTTLED`. Original entry: | Leg 348 read its seven papers **at abstract level only** and flagged that a full-text pass could strengthen *or undercut* its classification. Lane T rests entirely on that classification, and the 2026-08-13 narrowing of the outreach hold makes full text readable. Cheap, and it can undercut the lane. |

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
