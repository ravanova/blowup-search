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

## A. `PROG-R4` — the four options the user did not take. **Whole section retired verbatim 2026-08-19 → `WALLS_HISTORY.md` §OPTIONS-A-WHOLE** to pay for §G's `P0-NS12`. Nothing in it is closed. Option **E**'s field ensemble (`E-FE`, leg 408) is **STILL IN FLIGHT** at the stop — see `reports/ORCH_STATE.md` LIVE and `STATE.md`, not this file.

## B. Lane R — the units not taken

| id | unit | status | note |
|---|---|---|---|
| **R0**, **R1** | metric; early abort | **TAKEN, w1, VERIFIED by `V1`** — §3j, one line plus a pointer. | `R0` **retracted** *"Lane R's first measured win"*; `R1` **closed against itself**, U5 had already collected it — **spend no more compute on this family.** `WALLS_HISTORY.md` §R0/R1. |
| **R2** | deflation (Farrell–Birkisson–Funke) | **DEFERRED — the strongest surviving Lane R item** | R0 measured the waste: **57 of U5's 100 seeds were already spent by U3**, **5 of 9 convergences are bit-identical re-executions**, **4 of 5 distinct solutions are re-finds**, U5's contribution new to the programme is **one orbit**. Deflate against the **union** of both runs' solutions. Re-opens whenever Lane R gets a wave slot. |
| **R3** | multiple shooting | **DEFERRED** | Brick B6's own spec names it; U1 built the globalisation without it. Standard conditioning fix for long orbits, and long orbits are where the published targets live. **The basin-structure finding points here, and `E-iii` fired, which points here again.** |
| **R4** | second-order-in-time stepper | **DEFERRED — AND `E` PROMOTED IT** | U3's is Lie–Trotter, globally **first** order (measured ratio 2.00), so its periodic orbits are `O(dt)` perturbations of the true flow's while the published rates come from higher-order codes. Invalidates M1's reproduction — own milestone. **`E-ii` named `R4` in advance as where a non-recovery would point, and its antecedent IS satisfied.** `E`'s leg-353 comparison is **the first evidence pointing at the REALIZATION rather than the budget** — a better realization got closer (residuals [0.80, 10.32] vs [22.5, 29.5]) from strictly **worse** seeds and still recovered nothing. |
| **R5** | carry the `m` unknown | **DEFERRED** — = `PROG-R4` option **C** | One unit in two ledgers; do not double-count. |

**THE LANE-R RANKING — RULED 2026-08-18 BY THE CONDUCTOR: `R4` FIRST, `R2` SECOND, `R3` THIRD.**
Tie broken on **kind**: **`R4` is a VALIDITY fix, `R2`/`R3` are THROUGHPUT fixes.** `U3`'s stepper is Lie–Trotter, **first order, measured ratio 2.00**, so every
orbit either run produced is an `O(dt)` perturbation of the true flow's, and **deflating a
first-order solver buys faster production of objects whose status is in doubt.** `R4` can also
**falsify** something landed (`M1`); `R2` cannot — **57 core-hours bought ONE new orbit**. `R2`
beats `R3` because `R2`'s waste is **measured** and `R3`'s case is an inference. **`R4`'s first
unit is NOT a campaign re-run** (122.1 core-h): re-solve the **landed** orbits under TWO 2nd-order
steppers (`S1` CN-RK2, `S2` Strang-IF), measure displacement against the residual band. **§3g's floor stands — this ranks the
lane's units, it does not promote it.** Steppers NAMED, old pre-condition WITHDRAWN as defective: `WAVE8_PLAN.md` AMENDMENT 2. Reasoning + §3k gate: `WAVE7_PLAN.md` §0.
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
| **L4** | certify the decay | §6(i) wants *certified* decay + a built cutoff; `L2′` built neither. Row retired VERBATIM → `WALLS_HISTORY.md` §OPTIONS-L4. **`≥1 full wave` FLOOR**, and `§52` puts the profile it would certify on a divergent functional. | **≥1 full wave** |
| **L5** | W4 clause (b) | **TAKEN and CLOSED, `4be46ef`.** Gate `NO`, threshold-free. Row retired 2026-08-19 → `WALLS_HISTORY.md` §OPTIONS-L5; substance at `WALLS.md` W4(b). | done |
| **L6** | bank a discrete route-4 profile | **LANDED leg 401, `NO`.** Route 4's first: `ρ = 1.6138` in `L5`'s norm at `n_dof = 6720`, far-field amplitude normalised to 1, **not decreasing under refinement** (`−0.0222`, last 3 rungs). **Ceiling found ON LANDING: the minimum is reached by ONE start — the continuation; 5 independent seeds land 10–24× higher and WORSEN with `n_dof`, all capped at 800 iters.** `WALLS.md` W4. **CORRECTED 2026-08-19 by `V-W6`, `CORRECTIONS.md` §38: the seed spread is NEVER above 5.95× on branch A, not "10–24×"; it worsens with `n_dof` in the per-rung MINIMUM, not seed by seed; all 133 hit THEIR cap, 58 at 800 and 75 at 250. The cap sweep offered as the control is a post-hoc truncation of full-budget runs and controls NOTHING, and the banked minimiser is ~14 orders from its own `gtol` (153.22 vs 1e-12), worsening with `n_dof`. **`3.93–23.67×` WITHDRAWN as a cap artefact (§46); that withdrawal NARROWED 2026-08-19 by §50 — the LOW end SURVIVES (same seeds at 20,000 iters read `4.29`/`4.32×`, above `3.93`); `23.67×` and the width-as-basin-structure are what fall. VERIFIED-WITH-QUALIFICATION by `V-W6`; the gate answer and every banked number stand.** **⚠ HEADLINE AT RISK, §51: four rungs of refinement moved `−4.9946%`; ONE ×25 budget step at FIXED `n_dof` moved `−6.7518%` = ×1.3518 of the whole ladder — the rungs were differenced at a cap that dominates them. `J3` needs `7.2153%` to fall under `J4@20,000` and INVERT; `6.7517%` is measured one rung up. Margin 0.46 pp → `L6-e`.** | done, 2.30 h |
| **L7** | interval the commutator | **PRECONDITION NOT MET, and `§52` widens the gap — the residual `L7` would enclose is a truncation value of a DIVERGENT integral. Row retired VERBATIM → `WALLS_HISTORY.md` §OPTIONS-L7.** Do not dispatch. | blocked |
| **L6-b** | **is the stall the ANSATZ or the BUDGET?** | **NEW, from `L6`'s landing audit — cheapest thing that can overturn its `NO`.** Fix `n_dof = 6720`, start from `L6`'s banked minimiser, raise the cap **800 → 20,000**; two independent seeds too. `L6`'s own timing (1,240 s / start / 800 iters) prices it at ~8.6 h wall per start — **two orders below the ~10³ core-h `L6` priced for a full ladder.** Decisive both ways. | **~10–30 core-h** |
| **L6-e** | **does `L6`'s refinement ladder INVERT at an adequate budget?** | **NEW 2026-08-19 from `CORRECTIONS.md` §51 — the cheapest measurement in this record that could overturn Lane L's own headline.** One rung: `J3` (`Nr = 16`, 2400 dof), `L6`'s apparatus/norm/seed policy unchanged, cap **800 → 20,000**. ⚠ **GATE v2, REWRITTEN 2026-08-19 BEFORE DISPATCH (`§53`)** — `§51`'s v1 compared two rungs at `nq_r` 60 vs 72, i.e. two TRUNCATIONS of a divergent integral (`§52`). v2: report `ρ(J3@20k)` at `J3`'s native `nq_r=60` **AND** at `J4`'s reach (`nq_r=72`, `r ∈ [5.5e-4, 7.27e3]`); inverts iff the **MATCHED** value `< 1.504851895102804`; if they straddle, the ladder is undecidable at this reach and that is the result. Also report the far-field increment/decade at the new iterate, *"not decreasing under refinement"* WITHDRAWN as budget-confounded; `≥` ⟹ the ordering survives its first honest test. **Both outcomes are results.** Needs `7.2153%`; `6.7517%` measured one rung up at MORE dof. **Margin 0.46 pp.** | **~20–35 core-h**, ~6 h wall | **⛔ NEVER DISPATCHED — the run was STOPPED by user directive 2026-08-19 while it was HELD FOR CORES (load 27 on 12, `E-FE` live). PRICE ~20–35 core-h. RE-OPEN CONDITION: cores free. It is parked HERE, not in a brief.**
| **L-JVER** | **LANDED leg 409 `2acaa9e`, gate `NO`.** `1.0e-4`/`1.2e-4` at both minimisers, **`42.9%`** at a non-minimiser. Neither program miscoded (`X9`: `1e-14` on `L6`'s own rule) — **`J` is a DIVERGENT integral**, `§52`/`§53`. ~~**is `J(c)` AS CODED the norm it is documented to be?** | **NEW 2026-08-19, from `V-W6`'s §3i q5 — the CHEAPEST unit that can KILL this lane, and it now OPENS wave 8** (`WAVE8_PLAN.md` AMENDMENT 1; `L8`'s branch rule deferred verbatim to wave 9). Independently re-implement `W[V]` and `J` in a different basis and quadrature, from the written mathematics, never from `p2_route_l6_v1.py`. Gate: is `|J_new − J_L6| / J_L6 < 1e-3` at all three of branch B, branch A and a NON-minimiser — YES or NO? Every route-4 residual number (`c_mod`, `ρ = 1.6138`, `L6-b`'s answer) is downstream of this one function, and its only evidence is a selftest comparing two of `L6`'s OWN implementations (`T_D = 1.22e-4`). A `NO` goes to the user immediately. ~~ | **done**, 501 s + 1–5 core-h** |
| **L3** | attack §6(ii) — persistence under localisation | Published persistence techniques (the Chen–Hou line, `arXiv:2308.01528`) **never read against this object**. **DEFERRED — `L3′` died in wave 3 without committing.** | — |

**The record's best lead on this lane arrived as a by-product** (§F): **`arXiv:2308.01528`, the
Chen–Hou line**, which `L3′` was to read at full text. **A measured, honest "still no method, and here
is precisely which hypothesis fails" is a real result** — the one that would tell the user whether the
Tier-2 ceiling is permanent.

## E. Lane T — **DEFERRED (user ruling 2026-08-14).** Whole section retired verbatim 2026-08-19 → `WALLS_HISTORY.md` §OPTIONS-LANE-T, beside `WALLS.md`'s §LANE-T.

**What still binds, and is not superseded:** the lane is deferred by RULING, not by measurement; **both re-open conditions are unchanged and neither has fired**; `T1`/`T4`/`T5`/`T6` are TAKEN; **`T2` returned `UNDER-RESOURCED`, not `no` — it is not a clearance**.

**`T2″`** (Type-I rigidity on `T³`) is re-open condition (ii) and **the cheapest thing that could put a live W4 clause back in front of Lane L — cost before ranking**. **`T3`** (the non-DSS `T³` ansatz) is the lane's undone mathematical content, **deferred, NOT killed**. `T1`'s ban-wording packet is open on the user's desk and **I may not rule it**.

## F. Other standing options — whole section retired VERBATIM 2026-08-19 → `WALLS_HISTORY.md` §OPTIONS-F-WHOLE. Nothing in it is closed or declined; every re-open condition in it still stands.

## G. Wave-9 follow-ons — PARKED, NOT DISPATCHED (directive 2026-08-19); none entered a brief

- **`EFE-C7`** ~1 core-h — classify the **7 converged solutions** `E-FE` found and banked in `e_fe_converged_orbits.npz` (UPO9 Q ×3, UPO35 Q, UPO34 S, UPO32 Q, UPO22 Q). **None matched a named row, and nobody has asked what they ARE.** Cheapest of the three and the only one that could yield a positive. RE-OPEN: immediately, on its own merits (§60).
- **`EFE-C2`** ~1 container-h ELSEWHERE — reproduce the seed bank on a second machine. Inherited `R-bank` ceiling C2: the bank was only ever verified on this host, and all 160 attempts ran on that same host. RE-OPEN: before any cross-machine claim about the bank.
- **`EFE-C4`** ~91 core-h — a **second bank at a different declared draw order**. The 16 `C-REPRO` controls bound the PIPELINE, not the FIELDS; nothing shows the 144 previously-untouched fields are good fields. **Expensive and it is the honest price of the `NO`'s remaining half.** RE-OPEN: only if the 0-of-160 is ever cited as bearing on the published realization — which §60 says it does not.
- **`EFE-D7/D8`** ~20 min — add `fired_as_planted` to `C_N`/`C_P`/`C_R` (a machine check counts `17/20`, §60.4) and disambiguate `gate.closest_approach` by metric (§60.5). **Artefact is banked: a correction record goes BESIDE it, never an edit** (W3 ruling Q3). RE-OPEN: before any mechanical control audit of this artefact.
- **`EFE-D2`** ~5 min — `seedbank/manifest.json`'s `what` still says **1.2 GB**, the figure `R-bank`'s own D1 corrected to **268.9 MB**. A live artefact carrying a superseded number. RE-OPEN: immediately; cheapest item on this list.
- **`P0-NS12`** ~0.2 core-h (~12 min, 1 core) — re-run `L5-cmod`'s `c_mod` ladder at `ρ0 ∈ {1e3..1e7}` with **`n_s = 12`**, same `RES`, refit the slope. **`E5` FAILED** (§59): `n_s` `6→12` moves the per-decade increment by `×1.855293`, so §58's `−1.9900` slope is unmeasured at `n_s=12`. **GATE, pre-committed by the unit before its numbers existed:** survives iff slope within `±0.15` of `−2`; near `0` ⇒ `n_s=6` artefact and §53's flag is NOT discharged beyond the directly-measured band; between ⇒ `UNDER-RESOURCED`, and that is the result. RE-OPEN: **before any citation of §58's slope or of `c_mod` beyond `869.288`.**
- **`P2-F1`** ~2–4 core-h — bank the per-term decomposition in the gate's own `‖curl F‖_{L¹ₜL^{3/2}}`, not `L³` (§55). RE-OPEN: before P2 is submitted; one outcome makes its central sentence wrong.
- **`P2-F3`** ~30 min — re-bank `rho_exponent` beside its own fit window (§55). ⛔ **ESCALATE FIRST:** the naive repair reports summability available and BREAKS W4(b) off a transient. Not a unit's call.
- **`V8-HR`** ~15 min — anchor `test_headroom.py:46`; **NOT `count==1`** (§3j's verbatim retirement guarantees a 2nd `## LIVE`, §56.7). RE-OPEN: any edit above the live block; today 7,568/8,192 and TRUE.
- **`V8-VS`** ~30 min — re-run landed verifier suites at HEAD; `V-W7`'s is 22/25 (§56.11). RE-OPEN: next verifier dispatch.
- **`P4-F1`** ~1–2 h — bank §45's `32 of 49`; no artefact or classifier exists (§57). RE-OPEN: before it is cited again.
- **`P4-F3`** ~2–3 h — an instrument reading a verdict field against its object's own sibling fields (§57). **None exists; highest-value item here.**
