# STATE — the compact working surface

**This file is the read surface for ALL modes.** Read it first and read it instead of
`DIRECTION.md`. Everything else is archive, consulted only when a pointer here names it.

**Why it exists.** `DIRECTION.md` is 23,699 lines / 1.5 MB (~380k tokens). With the other
mandatory reads the per-agent load is ~480k tokens — paid by *every* agent in orchestrated
mode, and on *every task* in solo mode. That cost is pure overhead: a task needs its own
entry, the live bans, and what landed recently, not the accumulated cycle history.

**Regenerate at every landing.** Stale state is worse than no state — this file is only
trustworthy if it is rewritten as part of finishing a task, the way `JOURNAL.md` pointers are.

---

## Mode

**CONDUCTOR** — one long-lived entity owning both direction and integration, dispatching waves
of 2–4 self-terminating workers. See `ORCHESTRATION.md` **§3g** for the contract and **§3h** for
what a wall-breaking mandate does and does not license.

*(§3f SOLO and the four-slot contract of §§2–5 both remain available and are unchanged.)*

> **WOUND UP 2026-08-14 ON THE USER'S INSTRUCTION — WAVES 1 AND 2 BOTH COMPLETE, NOTHING IN FLIGHT,
> EVERYTHING PUSHED.** All nine units of both waves returned, were audited against their
> pre-committed gates and landed; `main` is clean, synced and `MERGE GATE: PASS`. **This is a
> wind-up, not a stop:** no lane is held, no ban changed, and the programme resumes by planning
> wave 3 under §3g step 1 — **plan first, commit the plan, then dispatch.**
>
> **WAVE 3 IS OBLIGED TO CARRY THE VERIFIER FOR `T4`, `T6`, `T5` AND `E`.** This Conductor planned
> all four and **may not check any of them** (§3f rule 1). `V1` discharged wave 1's debt for `T1`,
> `T2` and `R0`+`R1` **only** — `E` landed after `V1` ran. **And a verifier is an audit**, so both
> the composition floor (≥1 unit attacking a wall on the Clay chain — Lane T, V or L) and §3f rule 3
> (no more than two consecutive audit/repair/instrument tasks) require a **real mathematics or
> construction unit alongside it.**
>
> **ONE ESCALATION IS OPEN ON THE USER'S DESK** and the top of the wave-3 ranking depends on it:
> `writeup/escalations/ESCALATION_C1_EXEMPLAR_2026-08-14.md`. See "Open — needs the user" item 0.
> The full handoff — board, ranked candidates, and the four dispatch-brief rules this run paid for —
> is in `reports/ORCH_STATE.md` under *"WOUND UP BY USER INSTRUCTION, 2026-08-14"*.

## Goal, posture, odds

- **Goal:** a full Clay solve (user ruling 2026-08-06). Prize direction is Fefferman
  statement **(C)** — breakdown on `ℝ³`. **Statement (D), the torus, is now under active attack
  as Lane T** and is no longer only an open option.
- **Posture (user ruling 2026-08-13):** *the walls are the work.* Seven blockers are enumerated
  in **`WALLS.md`**, each with its evidence separated from its assumption and each with a
  pre-committed statement of what breaking it consists of. Four lanes attack them. **Every lane
  is authorised to build whatever it needs, at any size, without a further ruling.**
- **Ceiling right now: Tier 2.** Route 4 produces a candidate; no certification route is
  built. `CLAY_OBLIGATIONS.md` §6 names the two obligations with **no known method**.
- **Clay odds ~0.05%**, unmoved. No `L1 → L4` link has ever moved. This line stays in the same
  section as the ambition, under a ruling that raises it — not in spite of that ruling.

## The lanes — read `WALLS.md` before working in any of them

**USER RULING 2026-08-13: PURSUE LANE T.** The other lanes are **deferred, not rejected**, and every
deferred option is recorded with its cost and its re-open condition in **`OPTIONS.md`** — read that
file alongside this one when planning a wave. Nothing is dropped because a lane was not chosen.

**LANE T IS UNBLOCKED — the user ruled all four escalation items on 2026-08-13.** The ruling is
authoritative at **`writeup/escalations/RULING_BAN_WORDING_2026-08-13.md`** and is **transcription
work for the Conductor**, which applies it to `plan_of_record.py` in one commit per item:

- **(c) RULED C1 — the ℓ¹-Fourier/radii-polynomial ban names an APPARATUS.** A Zgliczyński-style
  Galerkin-plus-tail **dynamical closure** is a different apparatus and is outside it. **SCOPE, not
  a lift.** `T3` and `T4` **OPEN**. Nothing measured is superseded: the three dead realizations stay
  dead, Theorem NGX stays true, leg 341 stays true. **NAMING REQUIREMENT — binds every unit:** any
  unit claiming this scope must, in its own pre-registration, **name its apparatus** *and* **show it
  does not construct a single bounded approximate inverse uniform in `M`** (the precise quantity NGX
  excludes). **Absent both, the ban applies in full.** **SWEEP OWED:** C1 makes this ban narrower
  than the record has been treating it, so a unit must grep the landed record for legs that declined
  work citing it and report which refusals C1 now permits.
- **(a) RULED A2 — the Cadiot ban STANDS**, lift clause marked **CLOSED**, 2026-08-11 escalation
  **DISCHARGED**.
- **(b) RULED B1 — editorial.** *"which needs L1 first"* is **STRUCK** from stage V's lift clause.
- **(d) OUTREACH HOLD NARROWED — reading is authorised, contacting is not.** Any published document
  may be fetched and read. **Contacting an author, group, maintainer or list remains held.**

**COMPOUND CONSEQUENCE, recorded because neither item carries it alone: (b) + (c) also open Lane V.**
A fluid transport target attacked with a dynamical closure is outside both bans, subject to (c)'s
naming requirement. Lane V is therefore **deferred by the user's Lane T priority, NOT blocked** —
`OPTIONS.md` §C is updated to say so.

| lane | attacks | one line |
|---|---|---|
| **T — TORUS** | W2, W4, W6 | **⚠ THE PREMISE THIS RANKING RESTED ON IS MEASURED FALSE, 2026-08-14 (`T4` `2c87244`, `T6` `e7db624`).** ~~Priority 1, the breakthrough candidate. POCP's only named obstruction is *domain shape*; `T³` is that domain; `arXiv:1902.00384` already certifies a viscous 3D-NS periodic orbit there.~~ **It does not.** Both its certified rows are **2D lifts**, and it is certified by **the banned apparatus**. The domain-shape obstruction is **still not refuted** and `T³` is still the domain it asks for — but **no instance demonstrates the technology closing for a genuinely 3D object**, so the lane no longer has a worked example to build on. **Leg 390's "credit unclaimed" stands; what fell is the belief the method was already demonstrated.** **Re-ranking Lane T is deferred to the user** — `ESCALATION_C1_EXEMPLAR_2026-08-14.md` question 2. Still needs a **non-DSS** ansatz and a rigidity screen rebuilt from zero, now **without** a reproduction to lean on. |
| **V — VISCOUS RUNG** | W3 | Fill the Grade-A × fluid cell in the lowest dimension admitting fluid structure. Empty **"for want of a target, not a method"**. Both branches valuable — that is what makes it cheap. |
| **L — THE LAST OBLIGATIONS** | W4, **W5**, and `CLAY_OBLIGATIONS` **§6(i) and §6(ii)** | **Widened 2026-08-13.** The ONLY lane touching the final blockers. §6's two no-method obligations are the literal last things between a Tier-2 candidate and a Clay answer, **leg 390 confirmed the torus does NOT retire them** (open in both branches), and **no unit in 390 legs has ever attacked either.** Breaking one is the most valuable outcome available to this programme. |
| **R — REFORMULATION + SOLVER COMPETITIVENESS** | W7 | **Promoted 2026-08-13: raise the recovery rate until this machinery is best-in-field.** Runs continuously inside every unit's pre-registration (*what makes this answerable an order of magnitude cheaper?*) **and** as its own units R0–R5. Every factor removed is permanent and transfers to Lane T unchanged. |

## In flight

| What | State |
|---|---|
| **WAVE 2** (`T4`, `T6`, `V1`, `T5`) | **COMPLETE, AUDITED AND INTEGRATED 2026-08-14** (`46fe612`). All four returned; each audited against the gate committed at `c1a8d5e` *before it existed*. Planned and committed before dispatch per §3g step 1; `ORCH_STATE.md` refreshed in both the plan and the integration commit. **THE WAVE'S RESULT: Lane T's central premise is measured FALSE**, twice, by two units, by two different methods. **Wave 2 is `UNVERIFIED` and this Conductor planned it — WAVE 3 MUST CARRY ITS VERIFIER.** |
| **`T4` / leg 393** (Lane T) | **LANDED 2026-08-14** (`2c87244`), **GATE = `STOP`, pre-committed branch (c)** — not `yes`, not `no`, not `UNDER-RESOURCED`. `arXiv:1902.00384` is certified by **exactly the banned apparatus** (Newton–Kantorovich radii-polynomial in weighted `ℓ¹_η`, on **one bounded approximate inverse** `A : X_{−2,−1} → X`; *approximate inverse* ×7, *Newton-Kantorovich* ×4) — **and this is stated in the ABSTRACT leg 348 read**. **Both certified rows are 2D LIFTS**: `N_x3 = 0` in Table 1 and `Nrec`, decoded arrays of extent 1 in `x₃`, `max|u⁽³⁾| = max|ω⁽¹⁾| = max|ω⁽²⁾| = 0.0` exactly while `max|ω⁽³⁾| = 1.6351 / 1.5274`, `setup = '2D'`; the authors' reason is that a 3D solution's memory cost is *"for now, prohibitive."* **W2's own test requires showing the object is not a lift. It is one.** `C−` could have fired and did not — all six closure terms **0**, Zgliczyński only as bibliography [48]. The gate's **first** conjunct was met on both rows (criterion (4.32) verified; `r_min`/`r_max` deviations to `5.6e-15`; both `r_sol^Ω` exact; norm check `δ = 5.3e-06` vs `1e-3`), by arithmetic on published constants — **no operator, no `Y₀/Z₀/Z₁/Z₂`** (leg 316's precedent). **W2 STANDS, STRENGTHENED. W6 UNTOUCHED** — `inf` over nonzero modes of `μ(n)` equals `ν` exactly, a truncation-independent floor, against NGX's `σ_min(L_M) → 0`; **not** a counterexample to NGX. Cost of the apparatus, authors' Table 1: **95 CPU-days, 110 GB RAM — for a 2D row.** Pre-registration landed **before any computation** with `H1 → branch (c) → STOP` written in advance; evidence 68/68, exit 0. **UNVERIFIED.** |
| **`T6` / leg 394** (Lane T) | **LANDED 2026-08-14** (`e7db624`), **GATE ANSWERED: 7/7 full texts read — 2 UNDERCUT / 4 strengthen / 1 confirm, 0 `UNREACHABLE`, 0 `THROTTLED`, 0 zeros banked.** **UNDERCUT 1 = the independent replication of `T4`.** `T6` was **never told** what `T4` found; it reached the same conclusion by reading the authors' **prose** where `T4` reproduced from their **data package**: *"the solutions we present in Theorem 1.1 below are two-dimensional (in space) time-periodic solutions"* … *"they are independent of `x₃` and the third component of the velocity vanishes"* (§1, p.3). **Verified by the Conductor against the PDF in BOTH workers' separately fetched copies** (lines 118, 132). It confirms the apparatus finding too — Thm 2.15 (p.13) is literally a `Y₀/Z₀/Z₁/Z₂` contraction with a bounded `A`. **Not overclaimed:** the viscous term genuinely **is** inside the certified equation, the domain genuinely **is** `T³`, and the reduction's reason is **memory, not mathematics** — the 3D case is not claimed impossible. **UNDERCUT 2, new:** `arXiv:2409.09234` does not belong in leg 348's `domain_census` — 1-D map fitted to DNS data, **no-slip walls, not periodicity** — so **the census OVER-COUNTS BY ONE and leg 390's "6 compact/periodic" inherits it.** **WHAT SURVIVES: the obstruction leg 348 named is NOT refuted** — no counter-instance appeared either. Its **evidence base is thinner than the record said, not wrong.** Two leg-348 record errors found and **amended NEITHER** — leg 348 was its object, not its territory, and it sha256-locked the file to prove it. Evidence 77/77, exit 0. **UNVERIFIED.** |
| **`V1`** (verification) | **LANDED 2026-08-14** (`2fb399f`). **All five wave-1 claims reproduce** from banked JSON and landed evidence scripts alone; no banked figure disagreed; distinct counts held under leader/single/complete linkage with the arbiter rule **re-implemented, not imported**. **The verification debt on `T1`, `T2`, `R0`+`R1` is DISCHARGED.** **`M3 = DELIVERED` SURVIVES** U5's 57% seed overlap on M3's own pre-committed wording — **no clause conditions DELIVERED on seed novelty**, and clause 1 *requires* exhausting the same reservoir U3 drew from, so the overlap **is** compliance. The overlap falsifies the per-run orbits-per-core-hour inference, which `R0` already retracted. **Two defects banked, not reconciled:** (i) **`T1` banked NO machine record** — no JSON, no evidence script; item (5) checks out against **prose only** (field-scoped scan: zero hits). A banking-discipline defect, **not** evidence the claim is false; T1's gate answer stands. (ii) the gate's own comparand was ambiguous — **the Conductor's wording**, ruled at landing: `0.0553` is **U3's baseline**. Run 1 committed **as it ran** (exit 1, 34/37) before its repair; **no wave-1 artefact adjusted** to make a check pass. Evidence 38/38, exit 0. |
| **`T5` / leg 395** (Lane T) | **LANDED 2026-08-14** (`a6f0c38`), **GATE = PASS.** An **obligation** discharged. Corpus 1428 tracked `*.md`+`*.py`, 417,476 lines, **`DIRECTION.md` excluded by name with the exclusion asserted executably**. **7 refusals: APPARATUS 5 / REALIZATION 2.** **Re-openable under C1 — 2, UNRANKED, NOT STARTED:** leg 348's Galerkin-plus-tail build, and **leg 315's `O1`** sonic-point-desingularized **Taylor-model flow-map** enclosure, which *"needs **no function space**"* — **the genuinely new item, and it points at LANE V, not Lane T.** **Leg 257 is NOT re-openable**: its apparatus **is** the Corollary-21 radii polynomial merely in a **fourth space**, and **a fourth SPACE is not a fourth APPARATUS** — the known live defect, now measured. Sharpest structural point: **the unit of classification is the REFUSAL, not the leg** (leg 315 appears twice with opposite verdicts, correctly). **C1 did not cost nothing, but what it bought is two unranked entries, one pointing away from the lane it was ruled for.** Mutation-tested by the Conductor: corrupting the script's anchor → **exit 1**. Evidence exit 0, four controls PASS. **UNVERIFIED.** |
| **WAVE 1** (`T1`, `T2`, `R0+R1`, `E`) | **COMPLETE — ALL FOUR UNITS LANDED, 2026-08-14** (`E` last, at `d0d72b1`). **PLANNED AND COMMITTED 2026-08-13, before dispatch**, per §3g step 1. Gates in final wording and pre-committed readings are below. Composition floor met by **two** Lane T units, not one. **No verifier in this wave** — §3g forbids the Conductor verifying a wave it planned; wave 2 carried it for `T1`/`T2`/`R0`+`R1` and **DISCHARGED that debt**. **`E` LANDED AFTER `V1` RAN AND IS THEREFORE STILL `UNVERIFIED` — wave 3 owes a verifier to `E` as well as to all of wave 2.** |
| **`E`** (Lane R, instrument) | **LANDED 2026-08-14** (`d0d72b1`), **GATE = PASS in its pre-committed wording** — all three named diagnostics **RETURN**, each with a planted control demonstrated firing in **both** directions. Per that wording this is a PASS *regardless of convergence*. **PRE-COMMITTED BRANCH FIRED: `E-iii`, "it converges to something ELSE."** **DIAGNOSTIC (3) — the sharpest single test of H-hard available, never run at this realization before.** 16 attempts = 8 named Lucas–Kerswell Table IV rows × 2 arms, each planted at the published period **exactly** and at ±the published `|s|` **exactly, with the sign MEASURED** (tally 5 plus / 11 minus): **2 converged, 0 recovered their own named row, 0 recovered ANY named row, 0 secondary `|s|` matches**, exits `{stalled 14, converged 2}`. The two convergences are **genuine solutions of this realization and neither is its row** — UPO35 arm Q at `‖R‖ 4.83e-09` (`ΔT 3.124`, `Δ|s| 0.572`) and UPO9 arm Q at `‖R‖ 2.06e-10` (`ΔT 1.761`, `Δ|s| 0.196` unsigned / `0.394` signed) — and **BOTH LANDED BELOW DIAGNOSTIC (1)'s 0.15 SHELF**: U5 §9's basin structure reappearing **at the strongest seed quality this programme can construct**. **WHY THE NULL IS A MEASUREMENT AND NOT A BROKEN PREDICATE:** three controls fired as planted, `failures = []` — **P** (closed-form fixed point) recovered at `7.75e-09`, **N** (phase-scrambled) did **not**, `‖R‖ 51.46`, **R** matched a *perturbed banked orbit* back at `1.52e-10`, `ΔT 3.0e-07`. **Control R is load-bearing: it proves this unit's own predicate CAN return a recovery.** **`E-ii`'s antecedent is ALSO literally satisfied** (0 of 16 recovered any named row) and `E` **recorded that openly rather than suppressing it**, reporting `E-iii` as the more specific. `E-i` did not fire; **no fifth branch was constructed.** **`E-iv`'s discipline was kept and it is why the result is readable at all** — a published row supplies `(T, s)` but **NOT a field**; `E` seeded **field-plus-pinned-`(T,s)`** and said so in those words, never calling it "seeding at the published orbit." **LEG 353, stated as required rather than rediscovered:** *agrees* nothing was recovered; *disagrees* on distance — residuals **[0.80, 10.32]** here vs leg 353's **[22.5, 29.5]**, from **worse** seeds (20.06–54.94 vs mined 14–19), and **no attempt exited `line_search_failed`**, leg 353's only exit reason and **unreachable under the hookstep**. Diagnostics (1) `PULL_TO_LOW_S` (17/6, `p = 0.0347`, 91.3% below 0.15) and (2) `MIXED` (97.1% constrained, `p = 0.9317`) unchanged as landed, both two-sided. **WHAT DOES NOT FOLLOW:** **`G1` STAYS `UNDER-RESOURCED` and was not written to** (§3d — a hand-placed seed at published coordinates is **not** a mined seed); (2) returned `MIXED`, **not** `MINIMISATION_ATTRACTOR`, so the score-fix conditional **does not fire and NOTHING is proposed** — **leg 349's ban untouched**; the `R < 0.25` window **remains a live confound this unit could not separate**. Conductor audit: pre-registration `70f3962` landed **2026-08-13 23:05, hours before stage 3 ran**, already carrying all four branches; evidence **60/60 exit 0** re-run from the branch and again on `main`; **headline re-derived by the Conductor directly from the 16 raw attempt rows**, independent of `E`'s summary fields — matches. Territory clean, 11 files, **4895 insertions / 0 deletions**, nothing Conductor-owned touched. **§3d:** 5.687 core-hours + 0.806 h controls; **the commissioned model under-estimated by ~8×** (0.0713 vs ~0.57 h/attempt) **for a structural reason worth carrying — direct seeds do not fail fast.** Priced, not bought: field ensemble ≈91 ch, `N=48` lift ≈730 ch, closing (2)'s coverage gap 122.1 ch. Tier 2; no `L1→L4` link moved. **UNVERIFIED.** |
| **`T1` / leg 391** (Lane T) | **LANDED 2026-08-13** (`829c8db`), **GATE = `yes`**. The ban-wording escalation packet is at `writeup/escalations/ESCALATION_BAN_WORDING_2026-08-13.md` and is **OPEN ON THE USER'S DESK**. Four items: (a) Cadiot, (b) stage V's *"needs L1 first"*, (c) **the apparatus question — which blocks the whole of Lane T**, (d) the outreach hold, raised rather than routed around. Pre-committed reading honoured exactly: (a)'s scoping precedent recorded as **available in shape and NOT exercised**; under C2 Lane T is blocked on a **lift, not a scope — a materially worse position**, reported unsoftened; the **fourth-space/basis vs fourth-*apparatus*** mismatch surfaced as a defect and **left unresolved**. *(The row's `BUILD NOTHING IN LANE T` hold is **RESCINDED 2026-08-13** — the user ruled C1 and Lane T is unblocked by SCOPE. See "Open" item 2.)* No `L1→L4` link moved. |
| **`R0`+`R1`** (Lane R) | **LANDED 2026-08-13** (`ba512e0`), **BOTH GATES = `yes`** — and the headline claim is **RETRACTED**. Core-hours and distinct count re-derived from the banked artefacts and **independently re-derived again by the Conductor before landing**: U3 **8 / 144.69 = 0.0553**, U5 **5 / 57.04 = 0.0877**, both AGREE with `WALLS.md`. **But `WALLS.md`'s framing was itself wrong on core-hours**: 134.45 was never prose — it is `Σ attempts[].wall_seconds/3600` (attempt CPU) from the same JSON, against 144.69 (pool reservation); both are real, the gap is 92.92% utilisation, and what they needed was a **convention label**, not a replacement. **`Lane R's first measured win` is WITHDRAWN as an inference.** The per-run arithmetic (1.27×–1.59×) stands; the inference does not, because the metric counts **cross-run** re-finds as successes — the defect it was introduced to remove, one level up. Measured: **57 of U5's 100 seeds were already spent by U3**, **5 of 9 convergences are bit-identical re-executions**, **4 of 5 distinct solutions are re-finds**, and **U5's contribution new to the programme is ONE orbit** → cumulative **0.0175 vs U3's 0.0553, 3.15× WORSE**. **`R1` = CLOSED, against itself**: the "cheapest competitive win in the repository" was **already collected** — U5's deployed `resourcing.stall_exit` *is* the criterion — and the remaining headroom is **+0.45 pp**, with hold-out showing a rule tuned on U5's 9 convergences **kills one of U3's 14**. Spend no more compute on the family. Denominator is **worker-hours**; physical cores are in no numeric field and were **not estimated**. Deterministic throughout (leg 349's ban respected). Evidence 68/68. **UNVERIFIED** under §3f — wave 2 carries it. |
| **`T2` / leg 392** (Lane T) | **LANDED 2026-08-13** (`b5f8bac`), **GATE = no theorem located → returned `UNDER-RESOURCED`, NOT `no`** (§3d). **Branch (b) fired**: torus/periodic *global-regularity* theorems do exist under scaling-invariant smallness / LPS hypotheses (`1909.09125`, `math/9811161`, `0710.1604`) — real in shape, thin in substance, since every clause is somewhere a blow-up ansatz would already be. **A CONTROLLED ZERO IS NOT A CLEARANCE**, and this one is not even fully controlled: NRS 1996 / Tsai 1998 are **pre-arXiv** and were declared unreachable in advance, Semantic Scholar was **throttled on 5 of 6** substantive queries, and one battery **failed its own domain control** (`1304.7414` not re-found). arXiv itself was clean — **32/32 MEASURED**, served namespace banked as **1.1** on every query, **zero** non-MEASURED records carrying a total, negative control 0 in both instruments. Evidence 41/41. **Compliant search costed at ≈1.2–1.7 h plus one user ruling.** **THE ADVERSE FINDING, now in `WALLS.md`:** "0 of 4 clearances carry to `T³`" does **not** mean the `ℝ³` *exclusions* stop applying — **they still reach a `T³` object built by periodic extension of an `ℝ³` self-similar core.** Leg 309 read `2604.09949` at full text and hit **GATE NO at H11** on exactly that ground. **The one previous attempt at Lane T's target, by anyone, died this way.** **De novo item named:** a **Type-I rigidity theorem on `T³`** — a *rate* condition needs no dilation symmetry, so it carries to the torus intact as a question. **UNVERIFIED** under §3f. |
| **`plan_of_record.py` posture** | **LANDED 2026-08-13** (`1ca9e91`), the Conductor's first act under §3g. Additive only — 75 insertions, 0 deletions: `POSTURE`, `MODE`, `BLOCKERS_FILE` → `WALLS.md`, `LANES` (T/V/L/R with the walls each attacks), `POSTURE_LIMITS` (§3h restated executably). **No ban lifted, narrowed, reworded or re-read**; the `BANNED` table is byte-identical and `test_plan_of_record.py` still reports 26 bans / 19 in force, ALL GATES PASS. |
| **`PROG-R4`** (route-4 DSS programme, leg 380) | **U0–U3, U5 LANDED. U4 BLOCKED — but now *interesting*, see below.** U2 answered **MILESTONE M2** (T=1e5 DNS on the attractor, `D/D_lam`=0.0645±0.0253). U3 answered **GATE G1 = `UNDER-RESOURCED`**, controls fired as planted — 0 of 100 recovered a named orbit, 14 of 100 converged onto eight *other* RPOs. **U5 answered `MILESTONE M3 = DELIVERED`** (2026-08-13): the budget is now stratified by SHIFT — exhaustive re-mine 2,014 → **75,873** candidates, in-band admissible supply 35 → **72**, in-band spend 31 → **60**, controls fired as planted, **2,104 epochs against U3's 4,629 (no iterations bought)**. **9 of 100 converged, 0 recovered a named row**, and **U5's pre-committed reading fired on branch (b) — the bias is in BASIN STRUCTURE, not only seed supply.** **§3d's stop did NOT fire; route 4 is NOT stopped.** **G1 is untouched and stays `UNDER-RESOURCED`** — `n_recovered=0` is a count, not a `no`, and no G1 re-open is raised. U4 (G2, basin radius) still cannot open — it needs a recovered **named** orbit — but the pre-committed reading makes it the interesting unit rather than a formality. Tier-2 ceiling; Clay unmoved. **UNVERIFIED** under §3f. **UPDATED 2026-08-14 BY `E` (`d0d72b1`): the named rows are not reachable even from their own published coordinates.** 0 of 16 direct-seeded attempts recovered any named row, with a positive control proving the predicate can return a recovery. **This tightens G1's `UNDER-RESOURCED` without converting it to a `no`** — and it makes **U4/G2 harder to open, not easier**, since direct seeding was the last cheap route to a recovered named orbit. **THE OPEN QUESTION `E` LEAVES, and it is the ranking question for Lane R:** `E-iii` fired (points at **`R3`** multiple shooting / **`R2`** deflation), but **`E-ii`'s antecedent is also satisfied**, and `E-ii` was pre-committed to point at **`R4`** — U3's stepper is **Lie–Trotter, globally first order** (measured global ratio 2.00), so its periodic orbits are `O(dt)` perturbations of the true flow's. **`E`'s leg-353 comparison is the first evidence in this programme pointing at the REALIZATION rather than the budget**: a strictly better realization got strictly closer (residuals [0.80, 10.32] vs [22.5, 29.5]) from strictly worse seeds — and still recovered nothing. **Which of `R2`/`R3`/`R4` that makes the highest-value Lane R unit is a live re-ranking for wave 3 and this Conductor has NOT ruled it.** |

## WAVE 2 — PLANNED AND COMMITTED 2026-08-14, BEFORE DISPATCH

**Ranked after the user's ban-wording ruling of 2026-08-13 and against `OPTIONS.md`, which §3g now
requires be read alongside this file when planning every wave.** The ruling is the reason the
ranking changed: Lane T is unblocked **by scope**, `T3` and `T4` are OPEN, and two units became
obligations rather than options.

**Composition floor (§3g, per-wave): met by THREE Lane T units** — `T4`, `T6`, `T5` — each
attacking W2/W6 on the Clay chain. A wave of pure Lane R would be out of contract; this is the
opposite failure risk (one lane carrying three of four units), and it is taken deliberately because
Lane T is the user's priority-1 lane and has just spent two waves blocked. `V1` is the
counterweight: it is lane-independent and audits Lane R.

**§3f rule 3 is binding on this wave and was pre-committed in wave 1's own plan:** `E` was an
instrument task, so **wave 2 may not be a second instrument/audit/repair unit before a mathematics
or construction unit.** `T4` is that construction unit. It is dispatched first and it is the
wave's centre of gravity.

**Why `T4` and not `T3`, when `T3` is the lane's real mathematical content.** `T3` (the non-DSS
`T³` ansatz) is the bigger prize and it stays the priority unit. It is **not** taken this wave for
two measured reasons, not from timidity. (i) `T6` runs this wave and **can undercut the
classification `T3` would be built on** — leg 348 read its seven papers at abstract level only,
and the lane's whole thesis rests on that reading. Spending the lane's largest unit on a premise
being re-tested in the same wave is the one sequencing error available here. (ii) `T4` builds the
**apparatus** `T3` needs — a Galerkin-plus-tail dynamical closure, which is precisely the object
ruling C1 put outside the ban — against a target whose answer is already published. `T3` without
it is a build with no known-answer substrate, and leg 45's `M1` is the standing measurement that
that goes badly. **`T4` de-risks `T3`; it does not replace it.** `T3` is the first unit ranked for
wave 3.

**Every gate below is in FINAL WORDING and every unit carries a PRE-COMMITTED READING**, fixed here
before any worker is dispatched and before any number exists.

**C1's naming requirement binds `T4` and `T3` and is not waivable by the Conductor:** a unit
claiming the Galerkin-plus-tail scope must, **in its own pre-registration**, both **(1) name its
apparatus** — the closure it uses, with a citation — and **(2) show it does not construct a single
bounded approximate inverse uniform in `M`**. Absent both, the ℓ¹-Fourier/radii-polynomial ban
applies in full, and a unit reaching for a `Y₀/Z₀/Z₁/Z₂` contraction **in any space** is inside the
ban whatever it calls itself.

---

### 1. `T4` — REPRODUCE `arXiv:1902.00384` ROW FOR ROW. *Lane T, CONSTRUCTION. leg 393*

The crack in **W2**. `arXiv:1902.00384` certifies a **periodic orbit of 3D Navier–Stokes on `T³`
with the viscous term inside the certified equation** — natively 3D, natively time-dependent,
genuinely viscous, genuinely fluid. Leg 348 located it; leg 390 flagged the credit **unclaimed**;
nobody here has ever run it. The precedent is exact: **leg 316 reproduced Dahne–Figueras
row-for-row while a ban was in force**, clearing by individuating on three realizations. This is
the same move against a different paper, now with C1's scope ruling rather than an individuation
argument doing the work.

**Novelty is not at issue and no novelty pass is owed** — the target is a published theorem and the
unit's entire purpose is to re-derive someone else's numbers. **This is a known-answer substrate,
which is what makes it a legitimate first construction after two blocked waves.**

> **GATE (final wording).** Does the unit reproduce at least one published enclosure row of
> `arXiv:1902.00384` — the certified quantity, its interval, and the paper's own criterion for the
> row being certified — to within the paper's stated precision, **using an apparatus named and
> shown compliant with ruling C1 in the unit's own pre-registration**?
> **yes →** name the row, the reproduced interval, the paper's interval, and the agreement; state
> the apparatus and the C1 compliance argument; state what the reproduction does **and does not**
> establish about Lane T's target.
> **no →** return the **furthest point reached** — which row, which quantity, what failed, and a
> **cost** for reaching it (§3d). **A reproduction that runs out of budget is `UNDER-RESOURCED`,
> never `no`.**

**PRE-COMMITTED READING.** **(a) A successful reproduction is a CAPABILITY, NOT A RESULT ON THE
CLAY CHAIN.** It shows this repository can run the apparatus W2's crack is made of. It moves **no**
link of `L1 → L4`, and the write-up must say so in its own words — §3h rule 2, scale is not
evidence, and a reproduction of a published theorem is by construction not new mathematics.
**(b) If the reproduction succeeds, the object reproduced is a PERIODIC ORBIT, NOT A BLOW-UP.** W2
is about the *technology* clearing the bar, and W3 — the empty Grade-A × fluid **blow-up** cell —
is untouched by it. Do not let a success be read as filling leg 174's cell. **(c) If the apparatus
turns out, when actually implemented, to require a bounded approximate inverse uniform in `M`, THE
UNIT STOPS AND SAYS SO.** That is the C1 compliance test failing in practice rather than on paper,
it puts the unit inside the ban, and it is a **more valuable** finding than a reproduction: it
would mean the scope ruling does not reach a real implementation, which is a fact about the ban
nobody here has measured. Report it as a stop, not as a failure. **(d) A partial reproduction that
gets the shape right and the interval wrong is NOT a reproduction** and is reported as `no` with
the discrepancy quantified — leg 316's standard, applied unchanged.

**Territory.** `experiments/journal/leg_393.md`, `experiments/p2_route_t4_*.py`,
`writeup/data/p2_route_t4_v1.json`, `writeup/novelty/leg_393.md`, **figure `fig110`** (allocated
here, at dispatch, per the figure-collision incident). **Resourcing (§3d):** this is a
reproduction of a published computation and is resourced as a **full unit** — build whatever the
closure needs. An under-resourced attempt returns `UNDER-RESOURCED` **and a cost**, never `no`.

### 2. `T6` — DISCHARGE LEG 348'S OWN CEILING, AT FULL TEXT. *Lane T, literature. leg 394*

**An obligation, not an option** (`OPTIONS.md` §E; the user, 2026-08-13). Leg 348 read its **seven
papers at ABSTRACT LEVEL ONLY** and recorded, in its own words, that a full-text pass could
**strengthen OR UNDERCUT** its classification. **The whole Lane T thesis rests on that
classification**, and the 2026-08-13 narrowing of the outreach hold makes full text readable for
the first time. **It runs early precisely because it can undercut the lane** — which is the only
reason to run it before the lane's construction rather than after.

> **GATE (final wording).** Read at **full text** each of the seven papers leg 348 classified at
> abstract level. For **each**, does the full text **confirm**, **strengthen**, or **UNDERCUT** leg
> 348's recorded classification of it?
> **Answer per paper, in a table, with the deciding sentence quoted verbatim and located by section
> or page.** A paper whose full text could not be obtained is banked as **`UNREACHABLE`** with the
> reason, **never as a confirmation.**
> **yes (all seven answered) →** report the table; state explicitly whether Lane T's premise
> survives, and **name any paper whose full text moves it.**
> **no →** name which papers could not be reached and what it would take (§3d).

**PRE-COMMITTED READING.** **(a) AN UNDERCUT IS THE VALUABLE BRANCH AND IS REPORTED FIRST**, not
buried under six confirmations. If full text contradicts leg 348 on `arXiv:1902.00384`
specifically, that **also lands on `T4`** — the Conductor is told immediately and `T4`'s target may
be void. **(b) A CONFIRMATION IS NOT A STRENGTHENING.** "The full text is consistent with the
abstract" discharges the ceiling and adds nothing; only a full-text clause that leg 348 could not
have seen counts as strengthening, and it must be quoted. **(c) `UNREACHABLE` is not a confirmation
and not a zero** — leg 387's namespace failure fabricated exactly that once already
(`reports/ORCH_STATE.md`, Incidents). Bank a positive datum proving the source was reached.
**(d) This unit READS. It does not CONTACT.** Papers, problem statements, proceedings, theses,
publisher pages, full texts: authorised. **Contacting an author, group, maintainer or mailing list:
still held by the user, and needs its own ruling.** **(e) No Semantic Scholar key exists.** Pace
against the unauthenticated rate limits, back off rather than assuming a key, and **bank a
throttled query as `THROTTLED`, never as a zero.**

**Territory.** `experiments/journal/leg_394.md`, `writeup/data/p2_route_t6_v1.json`,
`writeup/novelty/leg_394.md`. No figure. **Resourcing (§3d):** seven full texts, ≈1–2 h.

### 3. `V1` — THE WAVE-1 VERIFIER. *Verification. §3g's per-wave budget, owed and now paid.*

**`T1`, `T2` and `R0`+`R1` are all `UNVERIFIED`, and the Conductor planned all three.** §3g is
explicit that this is the one thing a Conductor may not do for itself, with *more* force rather
than less because it has more context to be biased by. **`V1` is a fresh session with no memory of
the construction, re-deriving from banked JSON**, and it is briefed on the *claims*, never on the
reasoning that produced them.

> **GATE (final wording).** Re-deriving **from the banked JSON and the landed evidence scripts
> alone**, does each of the following claims reproduce **exactly**?
> **(1)** `R0`'s metric: U3 = **8 distinct / 144.69 worker-hours = 0.0553**, U5 = **5 / 57.04 =
> 0.0877**, and the **134.45 vs 144.69** reconciliation (attempt CPU `Σ attempts[].wall_seconds/3600`
> against pool reservation `wall_seconds × workers`, 92.92% utilisation).
> **(2)** The **retraction**: 57 of U5's 100 seeds already spent by U3; 5 of 9 convergences
> bit-identical re-executions; 4 of 5 distinct solutions re-finds; **U5's contribution new to the
> programme = ONE orbit**, cumulative **0.0175 vs 0.0553**.
> **(3)** `R1`'s closure: the remaining headroom is **+0.45 pp**, and a rule tuned on U5's 9
> convergences **kills one of U3's 14** on hold-out.
> **(4)** `T2`'s instrument discipline: **32/32 arXiv queries MEASURED**, served namespace **1.1**
> banked on every one, **zero** non-MEASURED records carrying a total, negative control 0 in both
> instruments, and **5 of 6** Semantic Scholar substantive queries `THROTTLED`.
> **(5)** `T1`'s packet **rules none of the three questions** — re-run the ruling-language sweep
> independently.
> **yes →** each claim reproduces; say so per claim, with the number you got.
> **no →** name the claim, the number you got, the number claimed, and the file and line the
> discrepancy is in. **A discrepancy is the deliverable, not a failure of the unit.**

**AND ONE QUESTION THE CONDUCTOR DELIBERATELY DID NOT ANSWER, HANDED TO `V1` BECAUSE THE CONDUCTOR
PLANNED THE WAVE THAT RAISED IT:** U5's 57/100 seed overlap with U3 was **not** known when
`MILESTONE M3 = DELIVERED` was written. **Does `M3 = DELIVERED` survive the overlap, on M3's own
pre-committed wording?** Answer it against the wording, not against the achievement. `yes` or `no`,
with M3's text quoted.

**PRE-COMMITTED READING.** **(a) AGREEMENT IS THE EXPECTED OUTCOME AND IS WORTH LITTLE ON ITS
OWN.** The Conductor already re-derived (1) and (2) independently before landing them; `V1`'s value
is concentrated in (3), (4), (5) and the M3 question, which nobody has re-derived. **(b) A
DISAGREEMENT IS BANKED AS A DISAGREEMENT AND NOT RECONCILED BY THE VERIFIER.** `V1` reports the two
numbers and stops; deciding which is right is the Conductor's job and doing it inside the verifier
destroys the independence the unit exists for. **(c) If `V1` cannot re-derive a claim because the
JSON does not carry the field, that is `UNVERIFIABLE`, not `no`** — and it is a finding about the
banking discipline, which lesson 68 says decays at the rate of memory. **(d) `V1` MUST NOT READ**
`WALLS.md`, `STATE.md`, `DIRECTION.md`, the wave-1 briefs, or the wave-1 journals' reasoning
sections. It reads the **claims** listed in this gate, the **banked JSON**, and the **evidence
scripts**. A transcription is not a measurement — `R0` proved that this wave, when `WALLS.md`'s
prose framing of the core-hours discrepancy turned out to be wrong.

**Territory.** `experiments/journal/verify_wave1.md`, `writeup/data/p2_verify_wave1_v1.json`.
**Writes no source, no figure, and none of the Conductor-owned files.**

### 4. `T5` — THE C1 SWEEP. *Lane T. AN OBLIGATION OF THE RULING, NOT AN OPTION. leg 395*

**The price of narrowing a ban, and it has never been paid here.** C1 means the
ℓ¹-Fourier/radii-polynomial ban is **narrower than the repository has been treating it**. That cuts
both ways and the second way has never been checked: **work may have been declined, deferred, or
never proposed on a reading the ruling now says was too wide.** The ruling calls this an obligation
in terms — *"not an optional follow-up"*.

> **GATE (final wording).** Grep the **landed record** — journals, write-ups, `plan_of_record.py`
> annotations, `DIRECTION.md` excluded per §3e — for every leg that **declined, deferred, or
> narrowed** work citing the ℓ¹-Fourier/radii-polynomial ban. For **each**, was the refusal
> **apparatus-based** (it assumed the ban reaches any certification machinery) or
> **realization-based** (it rested on one of the three dead realizations, or on Theorem NGX's
> exclusion of a single bounded `A` uniform in `M`)?
> **yes →** report the full list with the citation for each, **and name which refusals C1 now
> permits to be re-opened.** Each named refusal must carry the sentence that made it, quoted.
> **no →** state that no landed leg cites this ban as a reason not to proceed, **with the search
> commands and their coverage shown** — a zero here is a claim about the record and must be
> instrumented like any other zero.

**PRE-COMMITTED READING.** **(a) A PERMITTED RE-OPENING IS NOT A RECOMMENDATION TO RE-OPEN.** `T5`
lists what C1 unblocks; it **does not rank it, does not propose units, and does not re-open
anything.** Ranking is the Conductor's and the results go to `OPTIONS.md`. **(b) A REALIZATION-BASED
REFUSAL STAYS REFUSED.** The three dead realizations stay dead, Theorem NGX stays true, leg 341
stays true — **C1 supersedes no measurement**, and any entry the sweep marks as newly permitted must
survive that test explicitly or it is not listed. **(c) IF THE SWEEP FINDS NOTHING, C1 COST NOTHING
AND BOUGHT ONLY LANE T** — report that plainly rather than manufacturing a list. **(d) The sweep may
find refusals that were BOTH.** Those are listed under realization-based, the stricter of the two.

**Territory.** `experiments/journal/leg_395.md`, `writeup/data/p2_route_t5_v1.json`. No figure.
**Resourcing (§3d):** a record sweep, ≈0.5–1 h.

---

### What `OPTIONS.md` offered and was NOT taken this wave, and why

§3g as amended requires `OPTIONS.md` be read alongside this file when planning every wave, and a
deferred option that is never *said* to be deferred is an option that was silently dropped.

| option | why not this wave |
|---|---|
| **`T3`** — the non-DSS `T³` ansatz | **Deferred by SEQUENCING, and it is the first unit ranked for wave 3.** `T6` can undercut its premise this wave, and `T4` builds the apparatus it needs against a known answer. Not deferred for size — §3h licenses building whatever the lane needs. |
| **`T2′`** — the compliant rigidity search | **Deferred by COST-BENEFIT, and it is now cheaper than costed.** `T2` priced it at ≈1.2–1.7 h **plus one user ruling**; the ruling has landed and full text is readable, so the price is now the hours alone. It is ranked behind `T6`, which tests a premise rather than widening a search. |
| **`T2″`** — Type-I rigidity on `T³` | **Deferred, and it is the sharpest item Lane T owns.** A *rate* condition needs no dilation symmetry, so it carries to the torus intact **as a question**, and `"Type I blowup" AND "periodic"` measured **0**. It is a de-novo mathematics unit and it wants the apparatus `T4` is building. Ranked for wave 3 alongside `T3`. |
| **Lane V** (`OPTIONS.md` §C) | **DEFERRED BY PRIORITY, NOT BLOCKED** — rulings (b) and (c) together opened it, and this file records it as deferred, per the ruling's explicit instruction. Lane T is the user's priority 1. |
| **Lane L** — `L1`/`L2`/`L3` (`OPTIONS.md` §D) | **Deferred, and it is the most valuable lane by leg 390's own measurement** — §6(i) and §6(ii) are the literal last blockers and **no unit in 390 legs has attacked either**. Not taken because wave 2 is already three-quarters Lane T and adding a fourth lane would put five units in a wave §3g caps at four. **Ranked for wave 3.** |
| **`R2`–`R5`** (`OPTIONS.md` §B) | **Deferred by contract.** `R1` closed against itself and told us to spend no more compute on that family; a wave of pure Lane R is out of contract; and the basin-structure finding points at `R3`/`R5` only once `E` returns. **`E`'s result reopens this ranking, not this wave.** |
| **`PROG-R4` options A/B/D** (`OPTIONS.md` §A) | **Demoted by the pre-committed reading**, which fired on branch (b): the bias is in **basin structure**, not seed supply, and all three buy supply. Not re-ranked here. |
| **U3's two owed novelty questions** (`OPTIONS.md` §F) | **Deferred.** Owed novelty work on a run's own output is allowed (screening as a unit is the standing stop, and this is not that). It is small, it is real, and it loses to three Lane T obligations. |
| **Legs 387/388/389** (`OPTIONS.md` §F) | **Deferred.** 387's cause is now known — the namespace bug is diagnosed and banked — so a re-run is cheap but buys a novelty discharge for a route the ruling did not touch. |
| **(D)'s data conditions (8),(9)** | **Deferred by one wave, and it is now UNBLOCKED** — the outreach narrowing made it an ordinary literature unit. Leg 390 §5 item 1 owes the `check_A` re-run and **the §4 disposition may change.** It is a natural pairing with `T6` and is ranked for wave 3 unless `T6` reaches it incidentally, in which case `T6` banks it and says so. |

---

## WAVE 1 — PLANNED AND COMMITTED 2026-08-13, BEFORE DISPATCH

Re-ranking requires its own commit stating why (`ORCHESTRATION.md` §3f/§3g). In CONDUCTOR mode
these are drawn into waves of 2–4 from **different lanes**, so one stalled lane cannot sink a wave.

**Composition floor (§3g, per-wave):** four units — **T1 and T2 are Lane T**, attacking W2/W6 and
W4 on the Clay chain directly. **The floor is met by two units, not one.** A wave of pure Lane R
would be out of contract, and so would a wave whose only non-Lane-R unit is an audit; neither
applies here. **No verifier in this wave** — §3g forbids the Conductor verifying waves it planned,
so wave 2 carries the verifier for whichever wave-1 unit makes a claim.

**Every gate below is in FINAL WORDING and every unit carries a PRE-COMMITTED READING** — what each
branch of the outcome *means* — fixed here, before any worker is dispatched and before any number
exists. This is not ceremony: on 2026-08-13 a reading committed to `main` while U5 was mid-run bound
that unit's interpretation, and U5 honoured it rather than working around it, which is the only
reason the basin-structure result is a **finding** rather than a story assembled after the numbers.

---

### 1. `T1` — the ban-wording escalation packet. *Lane T. ESCALATION, NOT A LEG'S CALL.* leg 391

*Blocks the whole of Lane T.* Does the ℓ¹-Fourier/radii-polynomial ban reach a Zgliczyński-style
**Galerkin-plus-tail dynamical closure** — a different apparatus (a dynamical closure, not a
Newton–Kantorovich contraction in a function space)? Leg 348 raised this precise question and
**correctly refused to answer it**: *"I make no claim about whether that apparatus distinction
matters to the ban's scope; that reading is for the DM/user."* **The Conductor refuses too:** §3h
rule 1 makes a defective ban *wording* a user escalation, and §3g notes that an entity which both
raises and rules an escalation has defeated the mechanism. **Bundle all three pending wording
escalations** (Cadiot; stage V's "needs L1 first"; the apparatus question).

> **GATE (final wording).** Does the packet state, for **each** of the three pending ban-wording
> questions, **both** supportable readings with the evidence for each drawn from the ban's own text
> and the landed record — **without the packet itself ruling any of them**?
> **yes →** the packet escalates to the user under §8; Lane T stays blocked until the user rules.
> **no →** name which question could not be given two supportable readings and why; that question
> is then not a wording defect and is withdrawn from the escalation rather than carried.

**PRE-COMMITTED READING.** **(a)** If the ℓ¹-Fourier ban's own text names an **apparatus** (an NK
contraction / radii-polynomial bounds in a function space) and not a dynamical Galerkin-plus-tail
closure, then the 2026-08-11 *scoping* precedent is available **in shape** — and availability is not
exercise. T1 records that it is available and **does not exercise it**. **(b)** If the ban's text
names the **conclusion** (a certificate for this object class) rather than the apparatus, then T3/T4
are inside the ban whatever the apparatus, and Lane T is blocked on a *lift*, not a *scope* — a
materially worse position that must be reported as such and not softened. **(c)** Either way, the
lift clause reads *"a namable **FOURTH space/basis**"*, and a fourth **apparatus** is not literally a
fourth space or basis: T1 must surface that mismatch as part of the defect rather than resolve it.
**BUILD NOTHING IN LANE T UNTIL THE USER RULES** — that includes T3 and T4.

### 2. `T2` — search the periodic-rigidity literature. *Lane T, literature, never done here.* leg 392

Leg 390 §5 item 2: the §2 screen's four rows are **ℝ³-only, 0 of 4 carry to `T³`**, and this
repository has **never searched the `T³` rigidity literature at all.** This decides whether a torus
blow-up target is already excluded by a published theorem **before anything is built**. It runs
early precisely because it can kill Lane T cheaply, and a kill is a landable, valuable answer.

> **GATE (final wording).** Does the search locate a **published theorem** excluding a finite-time
> singularity for 3D Navier–Stokes on `T³` of the shape Lane T would need — a periodic/torus
> analogue of the Nečas–Růžička–Šverák / Tsai rigidity results?
> **yes →** name the theorem, its hypotheses **verbatim**, and which hypothesis a Lane T ansatz
> would have to violate. Lane T is killed or narrowed accordingly.
> **no →** report a **controlled** negative with full novelty-pass instrument discipline (positive
> and negative controls, both firing), **and** state which of the §2 screen's four rows have no
> periodic counterpart in the literature at all — i.e. what Lane T would have to establish de novo.

**PRE-COMMITTED READING.** **(a)** A located `T³` theorem covering only **self-similar or
asymptotically self-similar** objects does **NOT** kill Lane T — the lane needs a **non-DSS** ansatz
anyway, because the DSS ansatz does not survive periodization (342 modes survive one step at
`λ=1.7`, **zero** survive two). Record it as *narrowing*, not killing, and say exactly what is left.
**(b)** A located theorem covering a **broader** class (any bounded-energy periodic solution under a
scaling-invariant smallness or regularity hypothesis) **bites Lane T directly**, and the lane must
state what object class survives before anything is built. **(c) A controlled zero is NOT evidence
Lane T is clear.** Leg 348's own ceiling clause governs: absence of an instance is not a theorem of
impossibility. Report it as *"not excluded by anything located, with the search's coverage stated"* —
never as *"clear"*, and never as a result that advances Lane T. **(d)** **No external outreach**
(standing user hold): arXiv / Semantic Scholar APIs only, and (D)'s data conditions **(8)** and **(9)**
stay unread — they need outreach, the hold sits on Lane T's critical path, and T2 raises that rather
than routing around it. Leg 387 hit HTTP 429; handle rate limits and **report a throttled query as
throttled, never as a zero** (leg 387's own namespace bug fabricated a controlled zero once already).

3. **~~`PROG-R4` U5 — stratify the seed budget by SHIFT.~~ LANDED 2026-08-13, `M3 = DELIVERED`.**
   *Lane R + construction, §3c.* Journal `experiments/journal/prog_r4_u5.md`, data
   `writeup/data/p2_prog_r4_m3_v1.json`, figure `fig107` (16/16 own checks). Exhaustive re-mine
   2,014 → **75,873**; in-band admissible supply 35 → **72**; in-band spend 31 → **60** against a
   required 50; caps/`tol`/window/`m=0`/anchor/match asserted identical to U3's; **2,104 epochs
   against U3's 4,629 — fewer, not more**. **9/100 converged, 0 recovered a named row.**
   **G1 untouched, still `UNDER-RESOURCED`; no re-open raised.** U5 declined to choose its own
   continuation — five costed options at its §9, now item 1 of "Open — needs the user".

   **PRE-COMMITTED READING, fixed 2026-08-13 while U5 was mid-run and BEFORE its numbers were
   seen.** Two things follow from U3's own measurements and must not be discovered afterwards:
   (a) **A LOWER per-attempt convergence rate is the PREDICTED COST of stratification, not a
   failure.** U3 measured median `R` at 0.32 for `|s|<0.15` against 0.83 in the published band, so
   large-shift candidates are worse seeds *by the score's own metric* and U5 admits them on
   purpose. A rate at or above U3's 14% would suggest the stratification did not bind. (b) **What
   decides U5 is where the converged orbits sit in `|s|`, not how many there are.** U3's fourteen
   ran 0.073–0.317, twelve below 0.14; the published rows live at 0.295–0.707. **If the rate falls
   AND the converged orbits still cluster at small `|s|` despite a stratified pool, the bias is not
   (only) in the seed supply — it is in the BASIN STRUCTURE, i.e. large-shift orbits have
   intrinsically smaller Newton basins.** That is a genuine finding rather than a null, it explains
   U3 without the selection-bias account carrying all the weight, it points at `R3`/`R5` rather
   than at more seeds, and it makes U4/G2 (the basin radius) the interesting unit rather than a
   formality. Record whichever of these fires; do not construct a third reading after the fact.

   **WHICH FIRED — recorded 2026-08-13 against the reading above, and no third reading is
   constructed.** **(a) fired as predicted:** 9/100 against U3's 14/100. The stratification bound —
   U5's in-band seeds are worse by the score's own metric (median `R` 0.2122 against U3's 0.1897)
   because filling a quota of 60 from a supply of 72 reaches deeper than picking 31 off a global
   ranking. **(b) FIRED, and it is the finding.** The rate fell **and** the converged orbits still
   cluster at small `|s|` despite a stratified pool: **8 of 9 convergences landed at `|s| < 0.15`**,
   and **4 of the 5 in-band convergences left the band** (seeds at 0.31–0.42 converging to
   0.10–0.13). The 9 convergences collapse to **5 distinct solutions**, four of them at `|s|<0.14`.
   Independent support at matched seed quality: pooling both runs' 200 attempts into common seed-`R`
   bins, in-band converts **6/91 (6.6%)** against out-of-band **17/109 (15.6%)**, Fisher exact
   **p = 0.073** — direction consistent, significance not reached, and reported as not reached.
   **So the bias is in the BASIN STRUCTURE, not only in the seed supply**, exactly as pre-committed:
   large-shift orbits appear to have intrinsically smaller Newton basins. This **points at `R3`/`R5`
   and at `U4`/`G2`, and away from buying more seeds** — which demotes options A, B and D of U5 §9's
   fork, all of which buy supply. U5's own §9 recommendation (E then B) was written before this
   commit was visible; **E survives and is reinforced, B is demoted by the pre-committed reading.**
   Note also that **H-supply is independently refuted** on its own terms: its premise (the band was
   starved) was true and is now repaired, and its prediction ("more in-band seeds → recovery") is
   falsified at this scale.

   **On `R0`'s metric, computed for U5 since R0 fixed it before this landing.** Distinct orbits per
   core-hour, attempts stage only, like for like: **U5 = 5 / 57.04 = 0.0877**; U3 = 8 / **144.69** =
   0.0553. Two cautions, both owed to R0 and neither resolved here: (i) R0's baseline quotes
   **134.45** core-hours for U3, but `p2_prog_r4_g1_v1.json` gives 52,087.95 s × 10 workers =
   **144.69** — R0 should reconcile the figure it baselines on; (ii) R0 already flags U3's distinct
   count of 8 as unreconcilable with its own §4 table, and at 7 the baseline is 0.0484. U5's number
   is above U3's on every variant, but the comparison stays **provisional until R0 lands**.
   *Datum for R0:* clustering U3's 14 convergences independently, at the matching predicate's own
   0.05 tolerance and with `s` wrapped to `(-π, π]`, reproduces **8** — see
   `experiments/p2_prog_r4_m3_evidence.py` §5. R0 should reconcile against that rather than against
   prose.

### 3. `R0` + `R1` — the metric with its two reconciliations, then early abort on flatness. *Lane R.*

**R0 first and it is not optional.** Per-attempt convergence rate is inflatable by feeding easier
seeds — exactly what U5 deliberately stops doing — and it counts a **re-find** as a success, so the
reported metric is **distinct orbits per core-hour**. **R0's two reconciliations are corrections to
`WALLS.md` itself**, and both are to be settled against *artefacts*, never against prose:

- **(i) Core-hours.** `WALLS.md` §R0 first quoted **134.45** for U3;
  `writeup/data/p2_prog_r4_g1_v1.json` gives 52,087.95 s × 10 workers = **144.69**.
  **Reconcile against the JSON.**
- **(ii) The distinct count.** `WALLS.md` **argued from prose** that U3's 8 was unreconcilable with
  its §4 table. U5 **measured** it instead: clustering U3's 14 convergences at the matching
  predicate's own 0.05 tolerance with `s` wrapped to `(-π, π]` reproduces **8**
  (`experiments/p2_prog_r4_m3_evidence.py` §5). **Reconcile against that script.**
  **The lesson generalises and is the reason this unit is ranked here:** a count derived from prose
  is not a measurement, and this repository's own strategy file made that mistake **twice in one
  paragraph, one day after being written.**

> **WHAT CHANGED UNDER R0 WHILE THIS WAVE WAS BEING PLANNED, AND WHY IT SHARPENS THE UNIT RATHER
> THAN RETIRING IT.** A concurrent session landed `5c6d495`, which **wrote both corrections into
> `WALLS.md`'s prose** and banked the standing table (U3 144.69 / 8 / 0.0553, U5 57.04 / 5 /
> 0.0877). **That is a transcription of U5's numbers, not an independent measurement**, and it is
> the *same* move the unit exists to catch — U5 measured its own metric, and no second agent has
> re-derived it from the artefacts. **R0's job is therefore now the harder one: re-derive both
> figures from `p2_prog_r4_g1_v1.json` and `p2_prog_r4_m3_evidence.py` §5 independently, and report
> agreement or disagreement with `WALLS.md`'s current numbers.** Agreement is a real result and
> makes the baseline usable; disagreement is a bigger one. **R0 may not simply cite `WALLS.md`.**

Then **`R1`**: U3 measured convergence **bimodal** — all 14 convergences finished in **≤29 epochs**
(median 16) while **86 ran flat to the 52-epoch cap**, 53% moving `‖R‖` <1% over their final 10
epochs, 83% by <10%, only 3% still halving. Those epochs are the majority of the run and are pure
waste. No realization change, so **no milestone re-run**.

> **GATE (final wording), R0.** Does the metric land with **both** reconciliations closed against
> the artefacts named — core-hours against `p2_prog_r4_g1_v1.json`, and the distinct count against
> `p2_prog_r4_m3_evidence.py` §5 — yielding a single banked baseline figure for U3 and for U5?
> **yes →** bank both; route the `WALLS.md` corrections to the Conductor **verbatim**.
> **no →** name which reconciliation could not be closed and exactly which artefact is missing.
>
> **GATE (final wording), R1.** On U3's and U5's banked ledgers, does a **deterministic** flatness
> abort criterion exist that (α) kills **zero** attempts the ledgers show converged, and (β)
> recovers a stated fraction of the epochs actually spent?
> **yes →** report the criterion in final form, the recovered epoch fraction, and the **projected**
> distinct-orbits-per-core-hour under it, labelled PROJECTED and never as measured.
> **no →** report the epoch fraction recoverable at **zero** false kills even if it is small. A
> small number is the answer, not a failure — U5 already measured the margin as wide (the worst
> 10-epoch ratio any U3 convergence exhibited at `k ≥ 20` was 0.0724 against a 0.50 threshold, a
> factor of 6.9), so a null here would itself be informative.

**PRE-COMMITTED READING.** **(a)** If the reconciliation moves U3's baseline **down** — fewer
core-hours or more distinct orbits — **U5's margin narrows or vanishes, and R0 is licensed to
retract "Lane R's first measured win" outright.** `WALLS.md`'s 0.0595 and STATE's 0.0553 / 0.0877 are
all **provisional** and any of them may fall. A metric unit that cannot retract the claim that
motivated it is not a metric unit. **(b)** If the count resolves to **7**, U3's baseline is 0.0484
and U5's margin *widens* — **do not report that as strengthening Lane R.** It is the same
measurement read against a corrected denominator, and saying otherwise would be the exact move R0
exists to prevent. **(c)** R1's saving is **compute, not orbits.** A recovered-epoch fraction moves
distinct-orbits-per-core-hour only if the recycled budget converts at the *observed* rate; R1 must
state that assumption explicitly and must not report a projection as a measured improvement
(§3h rule 2 — scale is not evidence). **(d) Ceiling.** Nothing in R0 or R1 moves an `L1 → L4` link.
Lane R makes the questions **affordable**, which is a different and lesser thing, and the writeup
must say so. **(e)** Leg 349's ban binds: the criterion stays **deterministic** — no learned or
evolved scoring, and R1 does not touch seed selection at all.

### 4. `E` — THE H-HARD DIAGNOSTIC. *Lane R, instrument. RULED BY THE USER 2026-08-13, run it.*

U5 §9 option **E**, reinforced by the pre-committed reading that fired on branch (b). On the **200
attempts already on disk** (U3's 100 + U5's 100): no new DNS, no new mining, no new solver, ≈0.5–1 h.
**§3f rule 3: this is an instrument task, permitted here because U5 was construction, and IT CANNOT
BE FOLLOWED BY ANOTHER ONE** — wave 2 may not queue a second instrument/audit/repair unit before a
mathematics or construction unit. Recorded here so wave 2 cannot forget it.

> **GATE (final wording).** On the 200 banked attempts, do all three named diagnostics return, each
> with a planted control demonstrated firing in **both** directions: **(1)** the converged-`|s|`
> distribution against seed `|s|`; **(2)** whether the low-`|s|` solutions are attractors of the
> **hookstep iteration** or of the **minimisation**; and **(3)** whether the named Table IV rows are
> reachable **at all** when seeded directly at their published `(T, s)`?
> **yes →** report all three. **(3) is the sharpest single test of H-hard available and has never
> been run at this realization.**
> **no →** name which diagnostic the banked data cannot support, and what it would take — a cost,
> not a verdict (§3d).

**PRE-COMMITTED READING — all four branches fixed before the run, and no fifth is constructed after.**

- **(E-i) Direct seeding CONVERGES to the named row** (within the matching predicate's own 0.05
  tolerance): the named rows **are** solutions of this discrete map at achievable tolerance, and the
  failure is one of **basin size / seed reachability**. This **refutes the strong form of H-hard**
  ("the named rows are not solutions of our realization at all"), promotes **`R3`** (multiple
  shooting) and **`U4`/`G2`** (basin radius) to the operative work. **`G1` stays `UNDER-RESOURCED`
  and does NOT become a recovery** — a hand-placed seed at published coordinates is not a mined seed
  and does not answer the question G1 asks.
- **(E-ii) It does NOT converge:** the rows are unreachable even from their own published
  coordinates, so the obstruction is in the **REALIZATION, not the search.** That points at **`R4`**
  — U3's stepper is **Lie–Trotter, globally first order** (measured global ratio 2.00), so its
  periodic orbits are `O(dt)` perturbations of the true flow's — and would make R4, not R2, the
  highest-value Lane R unit. It would be the **first evidence in this programme that the realization
  rather than the budget is what G1 has been measuring.** It still does **not** make G1 a `no`
  (§3d), but it changes *what* would have to be resourced.
- **(E-iii) It converges to something ELSE** — a different orbit, or drifts to `|s| < 0.15`: that is
  the basin-structure finding reproduced **at the strongest possible seed quality**, the sharpest
  available form of U5's result, and it means no amount of seed quality fixes this. Points at
  `R3`/`R2`.
- **(E-iv) The instrument limit, named in advance so it is not discovered afterwards.** A published
  row supplies `(T, s)` but **NOT a field.** E must state exactly what it seeded, and **must not
  describe a field-plus-pinned-`(T,s)` seed as "seeding at the published orbit."** If the published
  `(T, s)` cannot be expressed as a seed under the `m = 0` residual at all, that is an **instrument
  limit** (and `R5` prices it: 334 candidates unlocked, but only **1 of the 334 in the published
  band**), reported as a limit and never as a null.
- **On diagnostic (2):** if the low-`|s|` solutions are attractors of the **minimisation** rather
  than of the hookstep, the fix is in the **score**, not the solver — and leg 349's ban binds the
  repair to stay **deterministic**. Name it; do not build it.
- **THE PRIOR THAT MUST BE STATED, NOT REDISCOVERED.** **Leg 353 already attempted all five of
  UPO37 ×2 / UPO35 / UPO9 / UPO22 and all five failed** (`line_search_failed`, final `‖R‖` 22.5–29.5,
  basin radius never measured). E is **not** re-walking that: leg 353 ran at `T_total = 2000` DNS
  against U2's `T = 1e5`, and with **plain-Newton line search, not the hookstep** U1 later built. E
  must say so explicitly and must report leg 353 as the prior its own result agrees or disagrees
  with. U5's closest approach on record is attempt 0 (UPO37): `ΔT = 0.127`, `Δ|s| = 0.0099` — inside
  tolerance on `s`, outside on `T`, final `‖R‖ 2.20`.

---

**Wave 2 — planned only after wave 1 lands and is audited. `WAVE 2 SHOULD OPEN LANE L`,** which
touches `CLAY_OBLIGATIONS.md` §6's two no-method obligations and **has zero units run in 390 legs.**
**L1** prices §4 on `ℝ³` — read the published attempts to localise a self-similar profile to finite
energy and state, **per attempt, the named hypothesis that fails for DSS**. **L2** attacks §6(i),
where leg 381 banked the bill (critical `L³` tail **326.875 per decade**; `α > 1.5` required against
`α = 1.0` available) — **a deficit of 0.5 in a decay exponent is a NUMBER, not an impossibility**,
and no unit has ever asked what would supply it. **L3** attacks §6(ii) against the
nonlinear-stability-with-finite-unstable-spectrum literature, never read against this object.
**A measured "still no method, and here is precisely which hypothesis fails" is a real result** — it
is the one that tells the user whether the Tier-2 ceiling is permanent. Wave 2 also carries **the
verifier for wave 1** (§3g: dispatched in the following wave so it cannot be briefed by the
construction it checks) and is bound by §3f rule 3 not to open with a second instrument task after
`E`. Further expected shape:

5. **`R2` — deflation.** **NINE** of 14 convergences landed on three solutions (corrected from "10" 2026-08-13 by R0, measured under the arbiter's rule; still the majority, so R2 is unaffected); Newton keeps re-finding
   what it has found. **U5 makes this worse than it looked, and cross-unit**: 4 of U5's 5 distinct
   solutions were already in U3's set, so a second 100-attempt budget at 57 core-hours bought
   **one** solution the first had not reached. Deflated continuation (Farrell–Birkisson–Funke) removes located solutions
   from the residual. Improves the R0 metric directly rather than by making attempts cheaper.
6. **`V1` — Lane V's opening escalation + target selection.** The stage-V ban's lift condition
   (*"unless the question is re-posed for a FLUID transport model, which needs L1 first"*) is
   **unliftable as written** — L1 has three dead attempts and no fourth candidate. Escalate the
   wording (bundle with T1's), and *in parallel* do the part that needs no ruling: **name the
   target.** Leg 174 says the cell is empty for want of one.
7. **`T4` — reproduce `arXiv:1902.00384` row for row**, the way leg 316 reproduced Dahne–Figueras.
   Until reproduced here it is a citation, not a capability. Fires only if T1 rules Lane T open.
8. **The verifier for wave 1.** §3g: dispatched in the *following* wave so it cannot be briefed by
   the construction it checks. Targets whichever wave-1 unit made a claim.
9. **Discharge `PROG-R4` U3's two owed novelty questions.** *Literature, owed work on the run's own
   output — NOT screening.* (i) Are the recovered RPOs known at all? None is a named Table IV
   row — **that verdict does not change here**; the unasked question is whether they are in the
   literature. **U5 enlarges the target set by exactly one.** Measured, not asserted
   (`experiments/p2_prog_r4_m3_evidence.py` §5): U5's 9 convergences give 5 distinct solutions, of
   which **4 are re-finds of U3's 8** — including U3's most-replicated
   (`T=16.5305/|s|=0.1008`, three attempts, two strata, anchors UPO9 and UPO17) — and **one is new**,
   `T=20.4175/|s|=0.5867`, stratum P, anchor UPO37. The new one is the only solution either run has
   found **inside the published band**. So the literature question is asked of **9 distinct
   solutions across both units**, states in `experiments/programme_r4/u5_m3_converged_orbits.npz`
   and U3's counterpart. (ii) Is the
   selection-bias caveat in `BLOG_P2_PROGR4_MINING_BAND.md` already published? It is
   externally-facing and unchecked. Claim neither outcome before measuring it.

**Held:** `T3` (the non-DSS `T³` ansatz — the lane's real mathematical content, opens after T1/T2)
· leg 389 (CT2C, wire 382's certified enclosure into the screen's second T2 column; note 386's
clause 2 — the δ-window is **EMPTY at every `α_centre ≤ 1`** and the banked object carries `α = 1`,
so it reports an empty window honestly and does not manufacture headroom) · leg 387 (DXNV,
discharge 382's owed novelty obligation after arXiv/Semantic Scholar returned HTTP 429) · leg 388
(CRVB, bound 382's curvature-detection threshold from below; the ladder is one-sided at ≤1e-6).

## Open — needs the user, not a task

0. **⚠ NEW AND TOP OF THE DESK — C1's EXEMPLAR HAS FALLEN.**
   `writeup/escalations/ESCALATION_C1_EXEMPLAR_2026-08-14.md`, raised on `T4`'s return, updated with
   `T6`'s independent replication. **You ruled C1 on 2026-08-13 on a packet carrying leg 348's
   error.** `arXiv:1902.00384` — recorded as the crack in W2 and the paper Lane T was ranked on — is
   certified by **exactly the banned apparatus**, and **both certified rows are 2D lifts**. Measured
   twice, two units, two methods; the authors' own sentence verified against the PDF in both
   workers' separately fetched copies. **Three questions are yours, and the Conductor has ruled none
   of them:** (1) does C1 need a replacement exemplar, or none at all — its proposition can be true
   with no instance in the literature, which would make Lane T thinner than it was ranked on; (2)
   does Lane T's priority-1 ranking survive the loss of the demonstrated-technology argument; (3) was
   the packet's defect material to C1. **What does NOT fall, so this is not over-read:** C1's general
   proposition, your ruling that Lane T is unblocked by **scope**, Theorem NGX, leg 341, and the
   three dead realizations. **A measurement supersedes a ban; it does not silently reverse a
   scoping.** **Work has not stopped.** The Conductor corrected only the factual claims — `WALLS.md`
   W2 and its four-results items 2 and 3, `CLAY_ROADMAP.md` §7.6 item 3 — keeping superseded wording
   inline and struck, and did **not** re-rank Lane T, name a replacement exemplar, or touch C1's
   transcription in `plan_of_record.py`.

1. **`PROG-R4` after U5 — five costed options, NOT chosen.** U5 delivered M3 and, under §3f,
   raised its continuation rather than picking one. Full text and costs:
   `experiments/journal/prog_r4_u5.md` §9. **The constraint shaping all of them:** the anchored
   admissible pool is now *exhausted* at `R<0.25` — 241 exist, 100 spent, **141 left of which
   only 12 are in-band** — so nothing that keeps the current window can push the in-band arm
   past 72 attempts, ever.
   - **A. Spend the rest of the pool** — 141 attempts, ≈10.7 h. Grows the in-band arm 60→72
     only; lowest information per hour.
   - **B. Relax the window to C&K's `R_thres=0.3`** (U3's option (b)) — ≈0.9 h re-mine + 0.071 h
     per attempt (≈8 h for 100). The supply multiplier **cannot** be read off U5's library (it
     was pruned at 0.25); the re-mine is what measures it. Leaves the realization intact, so the
     U3/U5 baselines stay comparable.
   - **C. Carry `m` as an unknown in the residual** (U3's option (c)) — a full unit, own
     milestone, ≈10 h compute plus solver work; changes the realization, so M1's reproduction no
     longer compares attempt for attempt. U5 now **prices it**: it unlocks 334 anchored
     in-window candidates (58.1% of the window) **but only 1 of the 334 is in the published
     band** — so it is *not* a band fix, it is the fix for `|s|>0.9`.
   - **D. Raise supply at source** (longer DNS / finer `N`) — ≈3.4 h per extra `T=1e5` plus
     ≈0.9 h re-mine, plus attempts. Does nothing about H-hard.
   - **E. Attack H-hard from data already banked** — ≈0.5–1 h, no new DNS/solver/mining, using
     the 200 attempts on disk. U5's sharpest unexplained result is that **seeds converge *out* of
     the band**: 4 of 5 in-band convergences left it, 8 of 9 landed at `|s|<0.15`, and the 9
     convergences collapse to **5 distinct solutions**. *Instrument task* — §3f rule 3 permits it
     after U5's construction but it cannot be followed by another one.

   **U5's recommendation, not a decision: E, then B.** A is dominated by B; C is worth its own
   milestone but aimed elsewhere; D costs most and helps least if H-hard is real.

   **RULED 2026-08-13 BY THE USER: TAKE OPTION E.** It is queued as wave-1 item 4 below. A, B and
   D stay **unqueued** — all three buy supply, the pre-committed reading points away from it, and
   the anchored admissible pool is exhausted at `R<0.25` in any case. C stays unqueued and keeps
   its own milestone, aimed at `|s|>0.9` rather than at the named rows. **`PROG-R4` is not
   stopped.** U5's five options are preserved verbatim at `experiments/journal/prog_r4_u5.md` §9
   if the ruling is ever revisited.

   **AMENDED BY THE PRE-COMMITTED READING, which U5 could not see when it wrote the above.**
   Branch (b) fired, so the bias is in the basin structure and the reading explicitly points
   "at `R3`/`R5` rather than at more seeds". **A, B and D all buy supply and are demoted by it;
   E is reinforced**, and `U4`/`G2` — the basin radius — becomes the unit this result is really
   about. The fork is left standing as U5 wrote it because the user rules on it, but it should be
   read with A/B/D discounted.

   *What U5 settled about the earlier fork:* §3g.2 pre-named **H-supply** vs **H-hard**.
   **H-supply is refuted** — its premise (the band was starved) was true and is now repaired
   (35→72 supply, 31→60 spend), and its prediction ("more in-band seeds → recovery") is
   falsified at this scale (60 in-band seeds, 0 recoveries). **H-hard is favoured but not
   resolved:** at matched seed `R` across both runs' 200 attempts, in-band converts **6/91
   (6.6%)** against out-of-band **17/109 (15.6%)**, Fisher exact two-sided **p = 0.073**. Every
   per-stratum Wilson interval overlaps its U3 counterpart; the in-band rise 3.2%→8.3% is **not**
   significant and is reported as a magnitude only.

2. **Three ban-wording escalations — RULED 2026-08-13, DISCHARGED, AND TRANSCRIBED.**
   The user's ruling is at **`writeup/escalations/RULING_BAN_WORDING_2026-08-13.md`** (`e2f618d`).
   **(c) RULED C1 — the ℓ¹-Fourier/radii-polynomial ban names an APPARATUS, so a Zgliczyński-style
   Galerkin-plus-tail DYNAMICAL closure is outside its object. LANE T IS UNBLOCKED BY SCOPE, NOT BY
   A LIFT: `T3` and `T4` are OPEN and *"BUILD NOTHING IN LANE T"* is RESCINDED.** No measurement is
   superseded — the three dead realizations stay dead, Theorem NGX stays true, leg 341 stays true.
   **The naming requirement binds every unit:** any unit claiming this scope must, in its own
   pre-registration, both **name its apparatus** (with a citation) and **show it does not construct
   a single bounded approximate inverse uniform in `M`**. Absent both, the ban applies in full; a
   unit reaching for a `Y₀/Z₀/Z₁/Z₂` contraction in **any** space is inside it whatever it calls
   itself. **(a) RULED A2 — the Cadiot ban STANDS**, its lift clause is **CLOSED**, not open.
   **(b) RULED B1 — *"which needs L1 first"* is STRUCK** as an editorial correction. **(b) and (c)
   together open Lane V**, which is therefore **DEFERRED BY PRIORITY, NOT BLOCKED** (`OPTIONS.md`
   §C). **(d) the outreach hold is NARROWED: reading any published document is authorised;
   contacting an author, group, maintainer or list is still held.**
   Transcribed one commit per item — (c) `42b2c45`, (a) `cc0f036`, (b) `1f2d00c`, (d) `8654fca` —
   with `test_plan_of_record.py` ALL GATES PASS after each. **No ban lifted, ban counts unchanged.**
   **Two units are now obligations, not options** (`OPTIONS.md` §E): **`T5`**, the C1 sweep of the
   landed record for refusals that cited this ban and were apparatus-based, which is the price of
   narrowing a ban; and **`T6`**, discharging leg 348's own ceiling — it read its seven papers at
   **abstract level only** and flagged that full text could strengthen **or undercut** the
   classification the whole lane rests on. Full text is now readable.
   **One known live defect, not repaired:** the lift clause still names a *"FOURTH space/basis"*,
   the wrong kind of object for an apparatus candidate. Moot for Lane T; recorded, not ruled.

   *What the packet itself did, retained because the audit is on it:* **PACKET DELIVERED
   2026-08-13.**
   `T1`/leg 391 landed it at **`writeup/escalations/ESCALATION_BAN_WORDING_2026-08-13.md`**, gate
   `yes`, audited by the Conductor against the wording pre-committed at `a384d92`. It states **both**
   supportable readings for each question and **rules none**; a ruling-language sweep found only its
   own disclaimers. *(Its `BUILD NOTHING IN LANE T` hold is **RESCINDED** by C1 above.)*
   All 19 bans stand in force, unchanged.
   What the packet *measured* rather than argued, on (b): `git log -S "which needs L1 first" --
   plan_of_record.py` returns **exactly one commit**, `561bb68` (2026-08-05). The 2026-08-06 ban
   review `4ff544a` **does not appear** — it deleted the *V-rigorous* entry, whose lift field was the
   bare string `"L1"` and which never contained the phrase. So that review's **declared** act and its
   **actual** edit do not coincide, and **both** readings of (b) survive rather than one.
   Disclosed limit: `DIRECTION.md` was not read (§3e). Text bearing on (b) sits at lines **755, 2262,
   2275, 9798, 9997**, located by grep and named as unread artefacts for whoever rules (b).
   The three questions, unchanged: (a) **Cadiot** — pending since
   2026-08-11; leg 304 resolved the open question and the resolution *confirmed* the ban's
   justification, so the lift clause's literal reading and its evident purpose now disagree.
   (b) **Stage V's "needs L1 first"** — unliftable as written. (c) **The apparatus question** —
   does the ℓ¹-Fourier ban reach a dynamical Galerkin-plus-tail closure? All three are wording
   questions, and `ORCHESTRATION.md` §3h rule 1 forbids an agent from ruling them.
3. **The POCP spend — SUPERSEDED 2026-08-13, now Lane T.** Leg 348: **(ii) OPEN-AND-REACHABLE**,
   cost class C. Retained here because its two adverse inputs still bind Lane T: **ZERO fully
   viable bases — corrected 2026-08-13 by leg 391, which found the prior wording overstated.**
   Leg 374's own headline is *"no row publishes a result meeting all four of the bridge's asks
   simultaneously"*; every genuinely spectral candidate located is **1D/scalar in its published
   form, with no `ℝ³` or vector/Leray-projected extension located for any of them.** Generalized
   Hermite is the **closest weight-match, not a survivor**: leg 377 cleared *only* Boyd (1980)'s
   decay concern (ADEQUATE, `γ=s` against leg 260's measured `s>1`) and states in terms that the
   row still **fails (i) `ℝ³` dimension, is ambiguous-to-unaddressed on (ii) vector/Leray state
   space, and fails (iii) CAP-grade rigor**. The prior line implied one basis survived; none did.
   This makes the `ℝ³` basis position **worse**, not better — which is the premise Lane T's `T³`
   pivot exists to relieve. And
   **no discrete spectral anchors** on `ℝ³` (leg 376, both channels continuous) — the second of
   which is exactly what `T³` supplies and `ℝ³` does not.
4. **Statement (D)'s data conditions (8) and (9) are UNREAD — but they are now READABLE** (leg
   390 §4; outreach narrowing, 2026-08-13). Fefferman's official problem description may be
   fetched and (8),(9) read verbatim. Until that runs, `CLAY_OBLIGATIONS.md`'s "(D) carries no
   decay condition" stays narrowed to (D)'s **solution** conditions, and **leg 390 §5 item 1 owes
   the re-run of `check_A` against them — the §4 disposition MAY CHANGE** if either condition
   carries a data-side decay or regularity requirement. This is no longer blocked on a ruling; it
   is an ordinary literature unit sitting on Lane T's critical path.
5. **The DSS escalation packet** (legs 313/320, branches unmerged). Complete: both candidate
   theorems read at full text and neither reaches the screened object.

## Live bans — 19, one line each

Full text and lift conditions: `.venv/bin/python plan_of_record.py`. **Run it when a task
could touch one**; do not paraphrase from here. **§3h rule 1: a ban is superseded by a
measurement, never by a decision** — and a defective ban *wording* is a user escalation.

gCLM measurement · DSS cheap entrance (bifurcation off a fixed point) · DSS expensive entrance
(**SCOPED 2026-08-11: a *seeded* search is outside it; name the seed or the ban applies**) ·
2D β re-measurement · scaling-gauge near-null · GA compute on unvalidated fitness ·
"closure is a property of the space" · stage V as posed · ℓ¹-Fourier/radii-polynomial on any
model · V-rigorous's L1 prerequisite (superseded) · closing the truncation gap by extending the
domain · three readings of legs 51/53 · `Z₁` block-coupling by tuning · weight exponent toward
leg 51's minimum · leg 51's finding at full strength · leg 51's zero `Y₀` as progress ·
Chen–Hou 2D as a target · leg 44's 2D near-null · building a solver without grepping
`capabilities.py`.

## Standing discipline — non-negotiable in every mode

Three-tier win condition (Tier 2 is never a proof) · pre-committed gates on every claim ·
novelty pass before construction (**once per programme**, not per unit, under §3c) ·
**lesson 91**: a negative names its realization/trial-space/basis · **§3d**: a stop fires only
on a null from an attempt resourced at the scale the question is posed at — an under-resourced
null returns a cost and answers `UNDER-RESOURCED` · planted controls that can fire both ways ·
`scripts/merge_gate.sh origin/main` must PASS · **reading published material is authorised;
CONTACTING an author, group, maintainer or list is HELD** (narrowed 2026-08-13) · no output described
as movement toward Clay unless a link actually moved · **§3h rule 2: scale is not evidence** —
a large build is not a result, and the gate is the deliverable.

**WAVE COMPOSITION FLOOR (adopted 2026-08-13, `ORCHESTRATION.md` §3g).** **Every wave carries at
least one unit that attacks a wall on the Clay chain directly** — a Lane T, V or L unit. Lane R
work is real and it is currently the most productive thing here, which is exactly why this floor
exists: efficiency work is satisfying, it always has a next increment, and a programme can spend a
year getting very good at finding orbits it was never going to certify. A wave of pure Lane R units
is out of contract.

## Where the detail lives — consult by pointer, never wholesale

| Need | Read | Size |
|---|---|---|
| **The blockers and the lanes** | **`WALLS.md`** | **7 walls, 4 lanes — read whole** |
| The strategic ruling | `CLAY_ROADMAP.md` §7.5 + **§7.6** | two addenda |
| A task's own spec | `DIRECTION.md`, that entry only | 23,699 lines — never read whole |
| Bans, stage, gate | `.venv/bin/python plan_of_record.py` | executable, ~40 lines out |
| Does a module exist | `.venv/bin/python capabilities.py <term>` | executable, grep don't read |
| The contract | `ORCHESTRATION.md` §3c–§3h | 3g = CONDUCTOR, 3h = walls |
| What a Tier-2 candidate owes | `CLAY_OBLIGATIONS.md` | 8 sections, §4 verified |
| Per-leg record | `experiments/journal/leg_N.md`, `writeup/novelty/leg_N.md` | one leg each |
| **Deferred options, with costs and re-open conditions** | **`OPTIONS.md`** |
| Banked numbers | `writeup/data/*.json` | **re-derive from these, never from prose** |
