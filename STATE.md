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

| lane | attacks | one line |
|---|---|---|
| **T — TORUS** | W2, W4, W6 | **Priority 1, the breakthrough candidate.** POCP's only named obstruction is *domain shape*; `T³` is that domain; `arXiv:1902.00384` already certifies a viscous 3D-NS periodic orbit there; leg 390 flagged the credit **unclaimed**. Needs a **non-DSS** ansatz and a rigidity screen rebuilt from zero. |
| **V — VISCOUS RUNG** | W3 | Fill the Grade-A × fluid cell in the lowest dimension admitting fluid structure. Empty **"for want of a target, not a method"**. Both branches valuable — that is what makes it cheap. |
| **L — LOCALISATION** | W4 on `ℝ³` | §4's "no known method" is the one load-bearing roadmap claim never checked to this repo's own standard. Price it; it may also break. |
| **R — REFORMULATION + SOLVER COMPETITIVENESS** | W7 | **Promoted 2026-08-13: raise the recovery rate until this machinery is best-in-field.** Runs continuously inside every unit's pre-registration (*what makes this answerable an order of magnitude cheaper?*) **and** as its own units R0–R5. Every factor removed is permanent and transfers to Lane T unchanged. |

## In flight

| What | State |
|---|---|
| **`PROG-R4`** (route-4 DSS programme, leg 380) | **U0–U3, U5 LANDED. U4 BLOCKED — but now *interesting*, see below.** U2 answered **MILESTONE M2** (T=1e5 DNS on the attractor, `D/D_lam`=0.0645±0.0253). U3 answered **GATE G1 = `UNDER-RESOURCED`**, controls fired as planted — 0 of 100 recovered a named orbit, 14 of 100 converged onto eight *other* RPOs. **U5 answered `MILESTONE M3 = DELIVERED`** (2026-08-13): the budget is now stratified by SHIFT — exhaustive re-mine 2,014 → **75,873** candidates, in-band admissible supply 35 → **72**, in-band spend 31 → **60**, controls fired as planted, **2,104 epochs against U3's 4,629 (no iterations bought)**. **9 of 100 converged, 0 recovered a named row**, and **U5's pre-committed reading fired on branch (b) — the bias is in BASIN STRUCTURE, not only seed supply.** **§3d's stop did NOT fire; route 4 is NOT stopped.** **G1 is untouched and stays `UNDER-RESOURCED`** — `n_recovered=0` is a count, not a `no`, and no G1 re-open is raised. U4 (G2, basin radius) still cannot open — it needs a recovered **named** orbit — but the pre-committed reading makes it the interesting unit rather than a formality. Tier-2 ceiling; Clay unmoved. **UNVERIFIED** under §3f. |

## Next tasks — pre-committed, in order

Re-ranking requires its own commit stating why (`ORCHESTRATION.md` §3f/§3g). In CONDUCTOR mode
these are drawn into waves of 2–4 from **different lanes**, so one stalled lane cannot sink a wave.

**Wave 1 — dispatch these four together. Two are cheap and can kill or unblock a lane.**

1. **`T1` — the ban-scope reading. ESCALATION, NOT A LEG'S CALL.** *Lane T, blocking the whole
   lane.* Does the ℓ¹-Fourier/radii-polynomial ban reach a Zgliczyński-style **Galerkin-plus-tail
   dynamical closure**, which is a different apparatus (dynamical closure, not a
   Newton–Kantorovich contraction in a function space)? Leg 348 raised this precise question and
   **correctly refused to answer it**: *"I make no claim about whether that apparatus distinction
   matters to the ban's scope; that reading is for the DM/user."* Prepare both readings with the
   evidence for each and **escalate to the user (§8)**. Do **not** rule it inside the lane, and do
   **not** build anything in Lane T until it is ruled. Note this is the *third* pending ban-wording
   escalation (Cadiot; stage V's "needs L1 first") — bundle all three.

2. **`T2` — search the periodic-rigidity literature.** *Lane T, literature, never done.* Leg 390
   §5 item 2: the §2 screen's four rows are **ℝ³-only, 0 of 4 carry to `T³`**, and this repository
   has never searched the `T³` rigidity literature at all. This decides whether a torus blow-up
   target is already excluded by a published theorem **before anything is built**. Run it early
   precisely because it can kill Lane T cheaply. Full novelty-pass instrument discipline, controls
   both ways.

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

4. **`R0` + `R1` — the metric, then early abort on flatness.** *Lane R, competitiveness, and R1 is
   the cheapest measured win in the repository.* **R0 first and it is not optional:** per-attempt
   convergence rate is inflatable by feeding easier seeds and counts re-finds as successes, so the
   reported metric is **distinct orbits per core-hour**, baselined at U3's **0.0595** (8 distinct /
   134.45 core-hours) — *after* reconciling U3 §4's table, which accounts for 10 convergences over
   3 solutions and cannot then yield 5 more distinct from 4 remaining. Then **R1**: U3 measured
   convergence bimodal (all 14 finished ≤29 epochs; 86 ran flat to the 52-epoch cap, 53% moving
   `‖R‖` <1% over their final 10 epochs). Kill flat attempts, recycle the budget into fresh seeds.
   Plant a control that the criterion never kills an attempt U3's ledger shows would have
   converged. No realization change, so no milestone re-run.

**Wave 2 — plan after wave 1 lands and is audited. Expected shape:**

5. **`R2` — deflation.** 10 of 14 convergences landed on three solutions; Newton keeps re-finding
   what it has found. Deflated continuation (Farrell–Birkisson–Funke) removes located solutions
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
   literature. **U5 enlarges the target set**: it independently re-found U3's most-replicated
   solution (`T=16.5305/|s|=0.1008`, three attempts, two strata, anchors UPO9 and UPO17) plus four
   more distinct ones, states in `experiments/programme_r4/u5_m3_converged_orbits.npz`. (ii) Is the
   selection-bias caveat in `BLOG_P2_PROGR4_MINING_BAND.md` already published? It is
   externally-facing and unchecked. Claim neither outcome before measuring it.

**Held:** `T3` (the non-DSS `T³` ansatz — the lane's real mathematical content, opens after T1/T2)
· leg 389 (CT2C, wire 382's certified enclosure into the screen's second T2 column; note 386's
clause 2 — the δ-window is **EMPTY at every `α_centre ≤ 1`** and the banked object carries `α = 1`,
so it reports an empty window honestly and does not manufacture headroom) · leg 387 (DXNV,
discharge 382's owed novelty obligation after arXiv/Semantic Scholar returned HTTP 429) · leg 388
(CRVB, bound 382's curvature-detection threshold from below; the ladder is one-sided at ≤1e-6).

## Open — needs the user, not a task

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

2. **Three ban-wording escalations, to be bundled by `T1`.** (a) **Cadiot** — pending since
   2026-08-11; leg 304 resolved the open question and the resolution *confirmed* the ban's
   justification, so the lift clause's literal reading and its evident purpose now disagree.
   (b) **Stage V's "needs L1 first"** — unliftable as written. (c) **The apparatus question** —
   does the ℓ¹-Fourier ban reach a dynamical Galerkin-plus-tail closure? All three are wording
   questions, and `ORCHESTRATION.md` §3h rule 1 forbids an agent from ruling them.
3. **The POCP spend — SUPERSEDED 2026-08-13, now Lane T.** Leg 348: **(ii) OPEN-AND-REACHABLE**,
   cost class C. Retained here because its two adverse inputs still bind Lane T: exactly one
   viable basis (leg 374 ADVERSE, Hermite sole survivor, decay concern cleared by leg 377) and
   **no discrete spectral anchors** on `ℝ³` (leg 376, both channels continuous) — the second of
   which is exactly what `T³` supplies and `ℝ³` does not.
4. **Statement (D)'s data conditions (8) and (9) require OUTREACH to read verbatim** (leg 390 §4).
   Until read, `CLAY_OBLIGATIONS.md`'s "(D) carries no decay condition" is narrowed to (D)'s
   **solution** conditions. **No external outreach is authorised** — this is a standing user hold,
   and it now sits on Lane T's critical path.
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
`scripts/merge_gate.sh origin/main` must PASS · **no external outreach** · no output described
as movement toward Clay unless a link actually moved · **§3h rule 2: scale is not evidence** —
a large build is not a result, and the gate is the deliverable.

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
| Banked numbers | `writeup/data/*.json` | **re-derive from these, never from prose** |
