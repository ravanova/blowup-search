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

**`E` HAS RETURNED — landed `d0d72b1`, and it changes the re-open conditions below.** Its diagnostic
(3) seeded all eight named Table IV rows directly at their published `(T, s)` and **recovered none:
0 of 16, positive control firing.** So **option B's re-open condition did NOT fire** — if anything it
hardened, because the failure now survives at seed quality no amount of supply can beat. **A, B and D
all buy supply, and supply is now refuted twice over.**

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

**`E` — THE H-HARD DIAGNOSTIC. TAKEN, LANDED `d0d72b1`, gate ANSWERED, `UNVERIFIED`.** **2 of 16
converged, 0 recovered any named row** (both are genuine solutions of this realization that are not
their rows, both below the 0.15 `|s|` shelf); positive control **R** at `‖R‖ 1.5e-10` through the
unit's own predicate; diagnostics (1) `PULL_TO_LOW_S`, (2) `MIXED` (`p = 0.9317`). **`E-iii` fired
(→ `R3`/`R2`), `E-ii`'s (→ `R4`) antecedent is satisfied; the re-ranking between them is NOT made.**
`V-W3` reproduced all six figures. Detail: `experiments/journal/prog_r4_e.md`,
`writeup/data/p2_prog_r4_e_v1.json`. *(Struck 2026-08-18: this read "IT DID NOT RETURN … `6a706f7`",
which described the wave-1 host kill. `E` was re-run and landed.)*

**`U4`/`G2`, the basin radius — BLOCKED, not an option.** It needs a recovered *named* orbit to
perturb and there is not one; direct seeding at the published `(T, s)` was the last cheap route and
returned **0 of 16**, so `U4` is blocked behind a *realization or method* change, not a budget.
**`G1` stays `UNDER-RESOURCED` — `E` did not write to it**: a hand-placed seed at published
coordinates is not a mined seed.

**⚠ ~~THE COST MODEL UNDER ALL FOUR OPTIONS IS WRONG BY ~8×.~~ REFUTED 2026-08-18 by `V-W3`
(`2b8755e`) — NO OVERRUN; THE `8×` WAS A UNITS ERROR.** `0.0713` is **WALL**-h/attempt at **8
workers**, `0.57` is **CORE**-h/attempt. Like for like: U5's model predicts `0.0713 × 8 = 0.5704`
core-h, `E` measured `9.08843/16 = 0.56803` — **ratio 0.9958, 0.4% UNDER**; the `8×` is `core ÷ wall`
and equals the worker count (`7.967`). The structural story is contradicted too: `E` ran **21.44**
epochs/attempt vs U5's **21.95** at **95.389 s/epoch** vs a 95 s model — **both factors accurate.**
~~*every `h/attempt` above is a floor*~~ **WITHDRAWN**; the figures above are wall-hours at 8 workers
and sound as written. Priced but not bought: field ensemble **≈91 ch**, `N=48` lift **≈730 ch**,
diagnostic (2)'s coverage gap **122.1 ch**.

## B. Lane R — the units not taken

| id | unit | status | note |
|---|---|---|---|
| **R0** | the metric | **TAKEN**, wave 1, gate `yes`, VERIFIED by `V1` | Corrected `WALLS.md` twice and **retracted** "Lane R's first measured win". `WALLS.md` §R0. |
| **R1** | early abort on flatness | **TAKEN and CLOSED AGAINST ITSELF**, wave 1, VERIFIED by `V1` | Already collected by U5 before commissioning. **Spend no more compute on this family.** `WALLS.md` §R1. |
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

## C. Lane V — the viscous rung. ~~*ACTIVE, PRIORITY.*~~ **HELD 2026-08-18 on `V3`'s return.**

**The lane's premise was measured and it did not hold.** `V3` (leg 399, `16ba44e`) graded 9 fluid
blow-up CAPs against leg 174's **own, unchanged** criterion: **`arXiv:2509.25116` (Hou–Wang–Yang)
passes both clauses** — interval arithmetic (§7.3 p.55) enclosing a solution of a system carrying
`−ΔŨ` (Prop. 1 eq. (1.15) p.5) for the **unforced 3D incompressible Navier–Stokes equations** — and
had **never been graded here**. 8 rows `NO`, clause quoted per row; legs 309/342/123 **cited, not
redone**. Reading (a) — *a YES kills Lane V's premise* — **FIRED, honoured as written.**

**BUT THE OBJECT IS NOT A BLOW-UP** (paper's §1.2 p.2: forward self-similar, singular data,
*"smooth for positive times"*), and **W3's prose test requires a finite-time singularity while leg
174's criterion — named in the same sentence as `V3`'s predicate — does not.** Which governs is (Q1)
of an **OPEN user escalation**, `ESCALATION_W3_WORDING_2026-08-18.md`. **W3: DISPUTED / UNRULED, not
ruled by the Conductor; HELD rather than KILLED is the consequence.** **The YES is UNAUDITED:** one
database, title-screened, S2 banked a **gap not a zero** (no key here).

**HELD UNITS — all three wait on the ruling, because what they should test depends on it.**
- **`V3-audit`, 4–8 h** — adversarial full-text audit of `2509.25116` to leg-309 depth, incl. the
  localisation step to a genuine Leray–Hopf solution. *Decides whether the YES survives contact.*
- **`V-net`, 6–10 h** — a real coverage net, ≥8 nets over ≥3 databases plus author pages. **Needs an
  S2 or OpenAlex key**, or half the channels bank `THROTTLED`.
- **`V2`** (wave 3 killed it without a byte) — name a dissipative fluid target, open the feasibility
  of a C1-compliant apparatus against it. **Re-opens only if the ruling leaves the cell empty of a
  certified singularity.**

**C1 binds every unit here, not waivable by the Conductor:** name the apparatus with a citation and
show it constructs no single bounded approximate inverse uniform in `M`; absent both, the ban applies
in full. **C1 may not be cited as evidence any apparatus closes for any object class.** **B1** struck
*"which needs L1 first"* from stage V's lift clause, so a fluid transport target attacked with a
dynamical closure is **outside both bans**.

## D. Lane L — the last obligations. **ACTIVE, PRIORITY LANE (user ruling 2026-08-14).**

**The ruling's reason: Lane L is on every path.** Leg 390 measured that the torus does **not** retire
`CLAY_OBLIGATIONS.md` §6(i)/(ii) — **OPEN in both branches** — and (D)'s gain on §4 is *"the
acceptance test, not the work."* **Nothing queued anywhere retires them.**

**⚠ THIS LANE HAS LANDED ZERO UNITS IN 398 LEGS.** `L2` was dispatched in wave 3 and **died with its
pre-registration committed and its gate unanswered** (`leg/397-l2-decay` @ `a9a4370`, §§0–3 complete
and fully resumable). `L3′` was dispatched in wave 3 and **died without committing a byte.**

| id | unit | what it is |
|---|---|---|
| **L1** | price §4 on `ℝ³` | Read the published attempts to localise a self-similar profile to finite energy; state, **per attempt**, the named hypothesis that fails for DSS. Converts an assumption into a measurement. **DEFERRED.** |
| **L2** | attack §6(i) — certified far-field decay + admissible cutoff | Leg 381 banked the bill: `L³` tail **326.875 per decade**, required `α > 1.5` against available `α = 1.0`. **A deficit of 0.5 in a decay exponent is a number, not an impossibility**, and no unit has ever asked what would supply it. **The most tractable-looking item on the entire no-method list. IN FLIGHT as `L2′`.** |
| **L3** | attack §6(ii) — persistence under localisation | The published techniques for persistence of singular behaviour under perturbation (nonlinear stability with a finite unstable spectrum, the Chen–Hou line) have **never been read against this object**. **DEFERRED — `L3′` died in wave 3 without committing.** |

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
| **T1** | ban-wording escalation packet | **TAKEN** w1, gate `yes`; machine record DISCHARGED by `V-W2` (`writeup/data/p2_route_t1_packet_v1.json`). Packet open on the user's desk. |
| **T2** | periodic-rigidity literature search | **TAKEN** w1, gate = no theorem located → **`UNDER-RESOURCED`, not `no`**. Not a clearance. |
| **T2′** | the **compliant** rigidity search | **DEFERRED, ≈1.2–1.7 h plus one user ruling.** Closes T2's three holes: NRS 1996 / Tsai 1998 are pre-arXiv (needs a forward-citation pass), Semantic Scholar was throttled on 5 of 6 substantive queries (needs an S2 key), battery `E` failed its own domain control (needs repair). |
| **T2″** | **the Type-I rigidity question on `T³`** | **DEFERRED — as of 2026-08-14 the ONLY thing keeping Lane T alive, and re-open condition 2.** The sharpest item the lane owns. A Type-I condition is a *rate* condition (`\|u\| ≲ (T−t)^{−1/2}`), needs **no dilation symmetry**, and carries to the torus intact **as a question**. Measured: `"Type I blowup" AND "periodic"` = **0**. Nothing located proves it. |
| **T3** | the non-DSS `T³` ansatz | ~~**OPEN — the priority unit.**~~ **DEFERRED WITH THE LANE — NOT KILLED.** Still the lane's real mathematical content; runs when a re-open condition is met. Binds: C1's naming requirement. |
| **T4** | reproduce `arXiv:1902.00384` row for row | **TAKEN** w2, `2c87244`, gate **`STOP`** on pre-committed branch (c); VERIFIED. **CLOSED.** |
| **T5** | the C1 sweep | **TAKEN** w2, `a6f0c38`, gate **PASS**; VERIFIED. Left **2 re-openable, UNRANKED**: `O1` (§F, → Lane V), leg 257 (§F, NOT re-openable). |
| **T6** | discharge leg 348's ceiling | **TAKEN** w2, `e7db624`, gate **ANSWERED**; VERIFIED. 7/7 at full text, 2 UNDERCUT / 4 strengthen / 1 confirm. By-product: the Chen–Hou thread (§F). |

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

- **`writeup/INDEX.md` ROWS — A CONDUCTOR-OWNED DEBT.** `T4`, `T6`, `T5`, `V1`, `E` and `V-W2` all
  landed without INDEX rows, because this Conductor did not put `INDEX.md` in anyone's territory and
  did not write the rows itself. `E` flagged its own missing row and correctly left it alone. Owed:
  six rows, or an explicit ruling that `INDEX.md` is retired.

- **A DISPATCH RULE `E` PAID FOR: MANDATORY CHECKPOINTING ABOVE ~1 h WALL.** The host killed `E`'s
  unattended run **twice**; it survived on per-attempt `.pkl` checkpoints. The rules adopted after the
  2026-08-14 process-exit incident — **commit early and often on the branch**, **poll long jobs from
  inside the turn** — are necessary but **were not sufficient**; what saved 5.7 core-hours was
  checkpointing *inside the computation*. **Every brief above ~1 h wall must require checkpointing to
  disk at a resumable granularity, and say where.** **Wave 3 paid for it again:** three of four units
  died and only the one that had committed left anything behind.
