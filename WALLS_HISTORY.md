# WALLS_HISTORY — retracted and superseded text from `WALLS.md`, kept struck rather than deleted

Split out of `WALLS.md` on 2026-08-18 under §3j (headroom), struck text intact. Referenced from
`WALLS.md` as `## History`. **Nothing here is live.** A claim in this file has been retracted or
superseded by a measurement; the measurement that did it is named in place.


**§3j's remedy for this file's cap.** Nothing below is live; it is retained because a wall's history
is the point: a reader who finds only the corrected claim cannot tell whether it was ever wrong.
Full elaboration is in the journals and in git.

## W2's crack and Lane T's item 3 — the same claim, struck

> ~~Leg 348 located `arXiv:1902.00384` — **a certified periodic orbit of 3D Navier–Stokes with the
> viscous term inside the certified equation, on the three-torus.** Natively 3D, natively
> time-dependent, genuinely viscous, genuinely fluid. Not a blow-up, so it does not fill leg 174's
> Grade-A/fluid **blow-up** cell — but the *technology* clears W2's bar already, and only the
> *target* is missing.~~

**RETRACTED by `T4` / leg 393 (`2c87244`)**, from the authors' own data package, not from prose:
`N_x3 = 0`, arrays of extent 1 in `x₃`, `max|u⁽³⁾| = max|ω⁽¹⁾| = max|ω⁽²⁾| = 0.0` exactly against
`max|ω⁽³⁾| = 1.6351 / 1.5274` (so the zeros are structure, not an empty array), `setup = '2D'`; the
authors give the reason — a 3D solve's memory cost is *"for now, prohibitive."* **Certified by
exactly the banned apparatus besides**, and **VERIFIED by `V-W2`** from a re-fetched artefact whose
SHA-256 matched the banked digest. Leg 348 read it at abstract level and flagged that limit itself.
Detail: `experiments/journal/leg_393.md`.

## The `2409.09234` census correction, and the Conductor-wording defect inside it

**The ground is the FIRST clause, not the second** — this file and the dispatch quoting it had them
the wrong way round. **(i) PRIMARY**, `T6` verbatim: *"THIS PAPER CLOSES NO TAIL-DOMINATION ESTIMATE
AND IS NOT AN INSTANCE OF THAT TECHNOLOGY AT ALL"* — a theorem about a **1-D map fitted to DNS
data**; `V-W2` re-measured all five term counts at **0**. **(ii) SECONDARY**, *struck:* ~~"no-slip
walls, not periodicity"~~ — the paper never says *"no-slip"* and states moving-wall Dirichlet with
*"periodicity … enforced to the rest of boundaries"* (§2 p.4). **Count unchanged: 6 − 1 = 5.**
**Second Conductor-wording defect a verifier caught** (`V1` caught the first, on `R0`'s comparand);
**neither found by the Conductor.** Detail: `experiments/journal/verify_wave2.md`.


## §R0/R1 — Lane R's TAKEN and CLOSED units, retired from `WALLS.md` 2026-08-18

*Moved verbatim under ORCHESTRATION.md §3j's retirement amendment (2026-08-18): struck text is
evidence and is never dropped to make room; when the cap binds, history moves out and the live
walls stay. Nothing below is reworded. `WALLS.md` keeps the standing metric and a pointer here.*

### R0 — the metric, pre-committed BEFORE optimisation. **TAKEN, wave 1. Its inference RETRACTED.**

**The standing cross-unit metric is `ORBITS NEW TO THE PROGRAMME PER WORKER-HOUR`**; within-unit,
distinct orbits per worker-hour, per-attempt rate a secondary diagnostic beside it. **The denominator
is WORKER-hours, not machine-core-hours** — physical core count is in **no numeric field** of either
JSON; a future unit must bank `magnitudes.physical_cores` and per-attempt `time.process_time`.
**`V-W3` (2026-08-18) shows what that ambiguity costs: a claimed `8×` cost overrun for `E` was
`core ÷ wall` and equals the worker count. See `STATE.md`.**

| | distinct | worker-hours | distinct / worker-hour | NEW to programme / worker-hour |
|---|---|---|---|---|
| U3 | 8 | 144.69 | 0.0553 | 0.0553 |
| U5 | 5 | 57.04 | 0.0877 | **0.0175 — 3.15× WORSE** |

**THE INFERENCE FROM THIS TABLE IS RETRACTED** — ~~*"U5 is above U3 on every variant, Lane R's first
measured improvement"*~~ **WITHDRAWN.** The per-run arithmetic (1.27×–1.59×) is confirmed; the
inference is not — the metric counts **cross-run** re-finds as successes, the exact defect it was
introduced to remove, one level up. **57 of U5's 100 seeds were already spent by U3; U5's
contribution new to the programme is ONE orbit.** Report **both** rows. Core-hour convention:
**pool reservation (`wall × workers`)**. **`M3 = DELIVERED` SURVIVES** — adjudicated by `V1`, not by
the Conductor that planned it. **Instrument limit:** U3's converged states are **banked nowhere**, so
the numerator 8 is testable only in the `(T, |s|)` pair, deciding pair at **1.288 × TOL**
(`OPTIONS.md` §B).

### R1 — early abort on flatness. **CLOSED 2026-08-13 — the win was already taken.**

~~*"Cheapest competitive win in the repository."*~~ **Withdrawn.** R1's numbers are **CONFIRMED
exactly**, but **U5 had already collected the win** (`resourcing.stall_exit` **is** this criterion,
deployed). Headroom over 12,597 deterministic rules: **+0.48 worker-hours**, and **hold-out shows a
rule selected on U5's 9 convergences KILLS one of U3's 14.** Deployed rule: **zero false kills over
23 banked convergences, 6.90× margin — spend no more here.** The underlying measurement stands and
is reusable: U3's convergence is **bimodal** — all 14 convergences finished in **≤29 epochs**
(median 16) while the 86 non-convergences ran to the 52-epoch cap, **the majority of the run.**



## §E — Lane R's H-hard diagnostic, retired from `WALLS.md` 2026-08-18 under §3j retirement

**THE H-HARD DIAGNOSTIC HAS RUN — `E`, landed `d0d72b1`** — the hardest number Lane R has produced
about the named rows. Seeded at the published `(T, s)` of all eight Lucas–Kerswell Table IV rows, two
arms each: **2 of 16 converged, 0 recovered ANY named row**, both convergences genuine solutions of
this realization that are **not** their rows, **both below the 0.15 `|s|` shelf**. Not a broken
instrument — the positive control recovered a perturbed banked orbit through **this unit's own
predicate**. Full result: `experiments/journal/prog_r4_e.md`.

**What it does and does not do.** It does **not** convert `G1` to a `no` — a hand-placed seed is
**not** a mined seed, so `G1` stays `UNDER-RESOURCED` and was not written to. It does **not** refute
H-hard's alternatives: the `R < 0.25` window **remains a live confound `E` could not separate.** It
**moves the suspicion from the budget to the realization** — strictly closer than leg 353 from
strictly **worse** seeds, and still nothing. **`E-ii` named `R4` in advance; `E-iii` fired and points
at `R3`/`R2`. Both pointers are live; the re-ranking between them is not yet made.**



## §PRIORITIES — superseded lane-priority narrative, retired from `WALLS.md` 2026-08-18 under §3j retirement

**Two byproducts of wave 2 point at V and L, neither found by looking for them:** `T5`'s **`O1`**
(leg 315's Taylor-model flow-map, *"needs no function space"*) points at **Lane V**; `T6`'s Chen–Hou
near-miss (`arXiv:2308.01528` — computer-assisted blow-up, **unbounded** domain, **>1D**, **algebraic
decay**) points at **Lane L** and route 4's `ℝ³` geometry, statement **(C)**. **`O1` is unranked and
belongs to no unit yet.**

**⚠ IT WAS RE-EARNED AND IT DID NOT SURVIVE (§3i, 2026-08-18).** Lane V's rank rested on leg 174's
*"empty for want of a target"*. `V3` measured that premise instead of inheriting it, and **it did not
hold.** Lane L's rank is **unaffected** — it rests on leg 390's measurement, not on a survey — so
**Lane L is the sole priority lane. It has now landed, and what it landed CLOSES one of its own
attacks (W4 clause (a)) rather than opening one.** §3i q6 is therefore live: what Lane L has left is
clause (b) and `L3`/§6(ii), and neither has a costed unit yet. **This is the question wave 5 must
answer before it ranks anything.**

## §OPTIONS-A — the refuted `~8×` cost-model overrun, retired from `OPTIONS.md` §A 2026-08-18 under §3j retirement

Verbatim, struck text intact. `OPTIONS.md` §A carries a live pointer to this section.

**⚠ ~~THE COST MODEL UNDER ALL FOUR OPTIONS IS WRONG BY ~8×.~~ REFUTED 2026-08-18 by `V-W3`
(`2b8755e`): NO OVERRUN, THE `8×` WAS A UNITS ERROR** — `core ÷ wall` is the worker count. `0.0713`
**WALL**-h/attempt at 8 workers = `0.5704` **CORE**-h/attempt against `9.08843/16 = 0.56803`
measured: **0.9958, i.e. 0.4% UNDER.** **AND `V-W3`'s OWN EPOCH FIGURE IS CORRECTED** by `D-REPAIR`
(`036e56d`): its *"2.3% fewer epochs/attempt"* compared `E`'s `n_iters` against U5's **ledger rows**,
which differ by one row per non-converged attempt (`2195 − 2104 = 91 = 100 − 9`; `E`: `357 − 343 =
14 = 16 − 2`). **Like for like `E` used MORE: +1.9% on `n_iters`, +1.7% on ledger rows**, at
**95.389 s/epoch** against the banked 95 s model (+0.41%).

## §W4-PROV — `V-W4`'s correction of the `≤ 1` provenance, retired from `WALLS.md` W4 2026-08-18 under §3j retirement

Verbatim. Clause (a) is SHUT and VERIFIED; `WALLS.md` carries a live pointer here. The four
citation defects are registered in `writeup/CORRECTIONS.md` §33. **No banked JSON was touched.**

**⚠ `V-W4` CORRECTED THE `≤ 1` PROVENANCE; THE DIRECTION HOLDS, through a door the phrasing did not
open.** ~~restated independently by Pineau–Vicol~~: PV §1.2 state it for **rotated globally
self-similar** solutions, not DSS — independent **authors**, not an independent **proof**. Chae–Wolf's
`[5]` is ESŠ *Backward uniqueness* (ARMA 169), carrying **no NS regularity criterion**; the paper that
does is ESŠ *Russian Math. Surveys* **58** (2003). Both journal-only: **ESŠ banks `UNREACHABLE` at
primary, never as a zero.** The **global Leray–Hopf** form provably does **not** apply — this object's
global energy is measured infinite. The **local suitable-weak-solution** form does, stated by Seregin
(an ESŠ author), `arXiv:math/0510396` §1, **with no finite-energy hypothesis**, and the object supplies
its local hypotheses. Seregin's `m_T` separates the cases **exactly at the pin**: `α = 1` → `m_T = +∞`,
criterion **silent, case open**; `α > 1` → `m_T < ∞`, origin regular, DSS scaling forces `u ≡ 0`.
Detail: `experiments/journal/verify_wave4.md`.

## §PRIORITIES-Q6 — retired from `WALLS.md` 2026-08-18 under §3j (verbatim, wave 5's q6 answer)

**⚠ §3i q6 WAS LEFT LIVE FOR WAVE 5 TO ANSWER, AND WAVE 5 ANSWERED IT.** The question was what Lane
L has left once `L2′` closed W4 clause (a). **`L5` (leg 400) has now closed clause (b) too, on a
measurement**, and what remains inside W4 is **only clause (c) — the torus, deferred with Lane T.**
Lane L's rank is **unchanged and re-earned**: it still owns **W5** and **§6(i)/§6(ii)**, both
untouched and both no-method. **The live ranking question is no longer "what else does Lane L have"
but whether W4 clause (c) is enough on its own to re-open Lane T** — and re-open condition (i) or
(ii) is still what decides that, not a Conductor's preference. Retired narrative, verbatim:
`WALLS_HISTORY.md` §PRIORITIES.

## §W3-CELL — retired from `WALLS.md` 2026-08-18 under §3j when `V5`'s audit landed (verbatim)

> **THE CELL IS OCCUPIED AND THE WALL STILL STANDS — THESE ARE TWO DIFFERENT CLAIMS.**
> `arXiv:2509.25116` (Hou–Wang–Yang) satisfies **both** clauses of leg 174's Grade-A × fluid
> criterion — interval arithmetic (§7.3, p.55) enclosing a solution of a system carrying `−ΔŨ`
> (Prop. 1, eq. (1.15), p.5) for the unforced 3D incompressible Navier–Stokes equations (eq. (1.1)).
> **The certified object is NOT a finite-time singularity**: forward self-similar, from singular
> initial data, *"smooth for positive times"*, concluding **nonuniqueness of Leray–Hopf solutions**.
> The paper itself warns against confusing this with the backward setting (§1.2, p.2). **W3 asserts
> the absence of a certified SINGULARITY and is unrefuted; leg 174's cell asserts the absence of a
> Grade-A fluid ENCLOSURE and is refuted.** Graded by `V3` / leg 399, **UNVERIFIED and UNAUDITED**.

## §W2-C1 — retired from `WALLS.md` 2026-08-18 under §3j (verbatim)

**Second finding, separate and also adverse:** the paper is certified by **exactly the banned
apparatus** — a Newton–Kantorovich radii-polynomial contraction in a weighted `ℓ¹_η` Fourier space on
**one bounded approximate inverse** `A : X_{−2,−1} → X`, stated in its own abstract. **C1's
proposition is untouched but its EXEMPLAR falls; RULED 2026-08-14, C1 STANDS EXEMPLAR-FREE** — see
LANE PRIORITIES for what that does and does not license.

## §LANE-T-PRICE — retired from `WALLS.md` 2026-08-18 under §3j (verbatim; every number also in `OPTIONS.md` §E)

**The price, stated first, because free lunches here get repurchased** (full itemisation:
`OPTIONS.md` §E, leg 390).
- **0 of 4 rigidity clearances carry to `T³`** (leg 390). The §2 screen must be rebuilt from scratch.
- **THE CONVERSE, LOAD-BEARING.** *"0 of 4 carry"* says the `ℝ³` screen does not **help** on the
  torus; it does **not** say the `ℝ³` **exclusions** stop applying, **and they do not** — an `ℝ³`
  exclusion still reaches a `T³` object built by periodic extension of an `ℝ³` self-similar core.
  Not hypothetical: leg 309 read `2604.09949` at full text and reached **GATE NO, broken at H11**, on
  that ground. **The one previous attempt at Lane T's target, by anyone, died this way.** The torus
  buys an escape only for a **natively periodic** ansatz.
- **NO PERIODIC ANALOGUE OF NRS/TSAI LOCATED — NOT a clearance** (`T2`, `UNDER-RESOURCED` under §3d,
  not `no`): both sources pre-arXiv, S2 throttled on 5 of 6 substantive queries; arXiv clean
  **32/32 MEASURED**, no throttled query banked as a zero. Compliant search: **≈1.2–1.7 h**.
- **`T2″`, THE DE NOVO ITEM AND RE-OPEN CONDITION (ii): a TYPE-I RIGIDITY THEOREM ON `T³`.** A *rate*
  condition needs no dilation symmetry, so it carries to the torus **as a question**, unproven.
- **The DSS ansatz does not survive periodization.** 342 modes survive one DSS step at `λ = 1.7`;
  **0 survive two.** Lane T needs a **non-DSS** ansatz on `T³` — open work, not a lookup.
- **(D)'s data conditions (8) and (9) are readable** (the hold is author *contact* only). **Leg 390
  §5 item 1 owes the `check_A` re-run; the §4 disposition MAY CHANGE.**


## §OPTIONS-F — two discharged items, retired verbatim 2026-08-18 under §3j

Retired from `OPTIONS.md` §F to make room for the Lane-R ranking ruling. Verbatim, nothing edited.

### The DSS escalation packet

- **The DSS escalation packet** (legs 313/320, branches unmerged). Complete: both candidate theorems
  read at full text, neither reaches the screened object.

### The verification debt's DISCHARGED half

  **DISCHARGED:** wave 1 (`T1`, `T2`, `R0`+`R1`) by `V1`; wave 2 (`T4`, `T6`, `T5`) by `V-W2`, whose
  items (1) and (2) were re-measured from **re-fetched primary artefacts whose SHA-256 matched the
  banked digests exactly** — measurements, not transcription checks. `V-W2` also caught a Conductor
  wording defect and it was ruled at landing **against the Conductor's own wording** (`WALLS.md`
  History).

**Live consequence: nothing.** Both are closed items. `OPTIONS.md` §F keeps the **OUTSTANDING**
half of the verification ledger, which is the half that binds.


## §OPTIONS-A2 — rows A, B and D of `PROG-R4`'s option table, retired verbatim 2026-08-18

**Why they leave `OPTIONS.md`:** all three **buy seed supply**, and proposing more seed supply for
`PROG-R4` is a **standing user prohibition**. They are not deferred on my judgement; they are
forbidden, so carrying them in a live options table misrepresents them as choosable. Row **C**
stays live — it is the largest measured hole in the trial space, and it is not a supply buy.
Verbatim, nothing edited:

| **A** | Spend the rest of the anchored pool — 141 attempts | ≈10.7 h | Grows the in-band arm 60 → 72 only. Lowest information per hour of the five, and buys supply. | Never on its own merits. |
| **B** | Relax the admission window to Chandler–Kerswell's `R_thres = 0.3` | ≈0.9 h re-mine + 0.0713 h/attempt (≈8 h for 100) (**wall**-h at 8 workers; the ~8× warning below is REFUTED) | Buys supply. Leaves the realization intact, so the U3/U5 baselines stay comparable — U5's second choice. **The supply multiplier cannot be read off U5's library** (pruned at 0.25); the re-mine is what measures it. | ~~E's diagnostic shows the in-band conversion penalty is *not* intrinsic.~~ **DID NOT FIRE — `E` returned and the penalty did not weaken.** One thing `E` left live: **the `R < 0.25` window remains a confound `E` could not separate**, and 1 of its 16 seeds deliberately sat outside it. So B re-opens only as *a measurement of that confound*, never as a supply buy. |
| **D** | Raise supply at source — longer DNS or finer `N` | ≈3.4 h per extra `T=1e5` + ≈0.9 h re-mine, plus attempts | Most expensive, buys supply, does nothing about H-hard. `N` refinement invalidates the banked library. | Only if the object itself changes and a fresh library is needed anyway. |


## §OPTIONS-E — `E`'s summary paragraph, retired verbatim 2026-08-19

**Why:** its last clause — *"the re-ranking between them is NOT made"* — **went false** when the
Conductor ruled the Lane-R ranking on 2026-08-18 (`WAVE7_PLAN.md` §0, `R4` > `R2` > `R3`). Retired
rather than edited in place, so the wording that was true when written survives. Verbatim:

**`E` — THE H-HARD DIAGNOSTIC. TAKEN, LANDED `d0d72b1`, `UNVERIFIED`. Retired to one line plus a
pointer, §3j.** **2 of 16 converged, 0 recovered any named row**, both below the 0.15 `|s|` shelf;
positive control recovered through the unit's own predicate. **`E-iii` fired (→ `R3`/`R2`), `E-ii`'s
(→ `R4`) antecedent satisfied; the re-ranking between them is NOT made.** `experiments/journal/prog_r4_e.md`.


## §STATE-WAVE5 — wave 5's STATE.md section, retired verbatim 2026-08-19 under §3j

**Wave 5 is COMPLETE, LANDED and VERIFIED** (`V-W5`, leg 403), so its rows leave the working
surface. The precedent it set — a mid-wave gate change REFUSED — is the part worth keeping, and it
is kept here verbatim rather than paraphrased.

## WAVE 5 — COMPLETE 2026-08-18. Three planned, three dispatched, three landed.

**Gates and pre-committed readings, FINAL WORDING and verbatim: `writeup/waves/WAVE5_PLAN.md` @ `1e49a00`, committed BEFORE any dispatch.** The unit descriptions are in that file and are **retired from here** under §3j — a pointer to committed text is not a summary. SHAs `036e56d` (`D-REPAIR`), `4be46ef` (`L5`), `b46ee4d` (`V-W4`); integration `e42e7ab`. **The mechanical audits, `§3i`'s seven per unit and the headroom report are in `reports/ORCH_STATE.md`.**

**⚠ A PRECEDENT SET HERE: one request to change a gate mid-wave was REFUSED.** Ruling Q5 landed after dispatch asking `L5` to state what distinguishes a genuine natively-finite-energy ansatz from the same trap in a different hat. **Amending a gate after dispatch defeats pre-registration**, so it was required **at integration** instead — and `L5`'s own pre-registration `e2f13c1`, made **before the ruling existed**, already carried the discriminator: **Clay condition (7), `E(t)` bounded uniformly in `t`, measured across all three `κ` branches.**

## §LANE-T — Lane T's body, retired from `WALLS.md` 2026-08-19 under §3j retirement

Retired because the lane has been **DEFERRED since 2026-08-14** and every dispatched unit is TAKEN, so the body was 2.5 KB of settled record inside a file with 115 bytes free. **Verbatim, nothing unstruck.** The live pointer in `WALLS.md` keeps the deferral, `T2″` as the only thing holding the lane open, `T3` as its undone mathematical content, and both corrections.

## LANE T — THE TORUS LANE. ~~*Priority 1.*~~ **DEFERRED 2026-08-14.**

> **DEFERRED BY USER RULING 2026-08-14**, on the lane's own measurement. **Not killed, and nothing it
> measured is superseded.** `T3` is deferred **with** the lane; **`T2″` is what keeps it alive** and is
> re-open condition (ii). Full cost of deferring and both re-open conditions: **`OPTIONS.md` §E**.
> The lane's opening argument rested on four results, **one of which was measured FALSE** — see
> `## History`, "Lane T's opening argument".

**Attacks W2, W4, W6.** What survives after `T4`/`T6`:

1. **Leg 348's obstruction is NOT refuted, but its evidence base is thinner than the record said.**
   The only named obstruction is **domain shape**: the Galerkin-plus-tail bridge closes against a
   **compact domain with a discrete, geometrically decaying spectral basis**; route 4 wants unbounded
   `ℝ³` in an algebraic weight. **Leg 348 read `arXiv:1902.00384` at ABSTRACT LEVEL ONLY and flagged
   that limit itself** — an undischarged ceiling a lane, an escalation and a user ruling rested on
   for 45 legs. **`T6` discharged it at full text.**
2. **`T³` is the domain the obstruction asks for**, but **leg 348's `domain_census` OVER-COUNTS BY
   ONE** — `arXiv:2409.09234` is not an instance of the technology at all (`T6`, verified by `V-W2`).
   **6 − 1 = 5.** Leg 390's figure inherits the error. **Re-check before citing it.** `## History`.
3. ~~`arXiv:1902.00384` already certifies a periodic orbit of 3D Navier–Stokes on `T³`.~~
   **RETRACTED by `T4`: both certified rows are 2D LIFTS**, certified by **exactly the banned
   apparatus**. **This item can no longer carry weight.** See W2.
4. **(D) vacates §4 as an acceptance test but not the work** (W4). Leg 390 §5 item 4: ***"§1's POCP
   credit is unclaimed."***

**The price, stated first, because free lunches here get repurchased.** Full itemisation retired 2026-08-18 → `WALLS_HISTORY.md` §LANE-T-PRICE; **every number is in `OPTIONS.md` §E, which is the live ledger.** Lane T stays **DEFERRED**, alive only through **`T2″`**, and its price is the reason re-opening it needs condition (i) or (ii), **not a Conductor's preference.**

**All dispatched units are TAKEN** — `T1` (ruled), `T2` (`UNDER-RESOURCED`, named `T2″`), `T4`
(`STOP`), `T5`/`T6`. **`T3`, the non-DSS `T³` ansatz, is the lane's real mathematical content,
deferred WITH the lane, not killed**; leg 390 §5 item 3 prices it (one-step DSS margin decays with
band width at exponent **−0.99057**).

## §OPTIONS-L5 — `L5`'s option row, retired verbatim from `OPTIONS.md` §D 2026-08-19

Retired because the unit is **TAKEN and CLOSED** and every clause of the row is restated at `WALLS.md` W4(b), which is the live home. Verbatim.

| **L5** | W4 clause (b) | **TAKEN and CLOSED, `4be46ef`. GATE `NO`, threshold-free.** The ansatz does not escape the pin: what survives localisation is the modulation commutator `T3 ∝ ṁ`, size `ρ^{1-α}`, and `α = 1` makes it ρ-independent. `WALLS.md` §W4. | done |

## §OPTIONS-L1RES — the `L1-res` row, retired verbatim from `OPTIONS.md` §D 2026-08-19

Retired because `writeup/SOURCES.md` now records DEPTH for all four pre-arXiv primaries by name, which is strictly more than this row carried. The one live debt — NRŠ 1996, `SECOND HAND` — is queued as `L7-src`. Verbatim.

| **L1-res** | the 4 pre-arXiv primaries | NRŠ 1996, Tsai 1998, Bogovskiĭ 1979, Giga–Kohn banked **`UNREACHABLE` as declared in advance**, quoted through secondaries. **Low value.** No author contact — prohibited. | ~1 unit |

## §OPTIONS-382 — the three leg-382 follow-ups, retired verbatim from `OPTIONS.md` §F 2026-08-19

**STILL OPEN, not discharged.** Retired for headroom only. Each of 389 (CT2C), 387 (DXNV) and 388 (CRVB) carries a MEASURED reason it stalled — an empty δ-window, an opensearch namespace mismatch that made a zero-result look real, and a ladder that bottomed out — so re-running one blind repeats a known failure. Verbatim.

- **The three leg-382 follow-ups, all open.** **389 (CT2C)** wire 382's certified enclosure into the
  screen's second T2 column — but 386 clause 2 first: the δ-window is **EMPTY at every `α_centre ≤ 1`**
  and the banked object carries `α = 1`, so it reports an empty window and manufactures no headroom.
  **387 (DXNV)** discharge 382's owed novelty obligation; **leg 392 measured why it failed** — arXiv
  serves opensearch namespace `1.1`, 387's harness listed `1.0`, so it refused every response while
  reporting a zero, and **any re-run must use a namespace-agnostic parser**. **388 (CRVB)** bound
  382's curvature-detection threshold from below; the ladder bottomed out at ≤1e-6, one-sided.

## §STATE-WAVE6 — wave 6's STATE.md section, retired verbatim 2026-08-19 under §3j

Retired for headroom only. **Nothing here is superseded**, and `L6` is still `UNVERIFIED` —
`V-W6` is in flight in wave 7. Landing audit and the seven §3i answers in full:
`writeup/waves/WAVE6_CLOSE.md`.

## WAVE 6 — **COMPLETE 2026-08-19. Three planned, three dispatched, three landed.** Plan: `writeup/waves/WAVE6_PLAN.md` @ `e202653`.

**`L6` LANDED `e62c449`** (leg 401) — route 4's **first ever** discrete profile, gate **`NO`**: `ρ = 1.6138` in `L5`'s own norm at `n_dof = 6720`, far-field amplitude normalised to 1, **not decreasing under refinement** (`−0.0222` over the last 3 rungs, `NO` at every cap 50–800), evidence **30/30 reproduced independently by me**.
**CEILING I FOUND ON LANDING, not claimed by the unit: the minimum is reached by ONE start — the continuation — while 5 independent seeds land 10–24× higher and get WORSE as `n_dof` grows; every start hit the 800-iteration cap. The `NO` is about THIS CONSTRUCTION AT THIS BUDGET.** Reading (b) fires, and (d) `UNDER-RESOURCED` fires with it. **`V5` LANDED `dacc01c`** — **both
clauses YES**: the certificate **CLOSES** (24 constants re-derived at 50 dps, **four printed ones
fail**, worst `x_0^U` `1.44e-5` vs `1.45054706437e-5`, **non-conservative**; closure survives, but
`x_1^U` clears by **0.08% — luck, not margin**), and the profile **IS genuinely 3D** on W2's own
test (swirl **57%** of `max|u_r|`), answered **standing alone**. **Class A NOT verified — a LIMIT,
never a pass. W3 does NOT move: its prose test was not run.** Wave 4's `D1`–`D6`/`N1` discharged as
**`_v2` deltas, no `_v1` edited**. One defect of its own: its evidence script needed `mpmath`, which
was **not in `requirements.txt`** — it exited **3** on a clean checkout. `CORRECTIONS.md` §36, row 18.
**`V-W5` LANDED
`95cf861`** — five items reproduce, **`C6`'s tolerance NEVER moved** (`347676f`), **3 defects
located, 0 repaired** (`CORRECTIONS.md` §35, row 17): the passing `C6` criterion is **post-hoc**
(added at the landing commit), `c_mod` is **basis-dependent by `1.476×`**, and half the `0.9958`
ratio is **scraped from prose**. **Arithmetic verified, science NOT** — still Tier 2, still the
SYNTHETIC profile, no `L1→L4` link moved. §34 applied to every gate **before** dispatch: **every artefact
named in a wave-6 brief was checked to exist.** Handoff is planned for **wave 6's END** (§9d
fired on summarisation, not on cycles) — **not mid-wave**.

**Gates in FINAL WORDING in the plan file, not re-wordable after dispatch — including by a mid-wave ruling, which is taken at integration instead (§3g; refused once in wave 5).** §3f rule 3: construction opens, verifier last. **§3i q7 fired TWICE running** (last six landed: reading, grading, verification, infrastructure, construction, verification), so debt 1 is discharged by making `L6` **the wave's centre**, not a side unit.

| unit | lane | what it must return | status |
|---|---|---|---|
| **`L6`** | L | construction, dispatched first | **LANDED `e62c449`, gate `NO`.** `WALLS.md` W4; `OPTIONS.md` §D. Next: **`L6-b`** — is the stall the ansatz or the 800-iteration budget? |
| **`V5`** | V | **OBLIGATORY (ruling Q4).** Adversarial full-text audit of `arXiv:2509.25116` at leg-309 depth. **TWO clauses answered SEPARATELY:** does the certificate close, and — on **W2's own pre-committed test, NOT folded into the first** — is the profile genuinely **3D**. **Second deliverable: the wave-4 repair** (`D1`–`D6`, `N1`) as **new `_v2` files, `v1` UNTOUCHED** (Q3). | **PLANNED** |
| **`V-W5`** | — | **LAST.** Verifies wave 5, which it did not plan. Five items: `L5`'s `NO` and `ρ`-exponent re-derived from artefact+code, not report; its three positive controls; **was `C6`'s tolerance EVER moved**; both `self_hash`es; `D-REPAIR`'s epoch correction. **REPAIR NOTHING.** | **PLANNED** |

**⚠ A GATE DEFECT OF MINE, REGISTERED SO IT DOES NOT REPEAT.** `L5`'s wave-5 gate said measure *"on route 4's **banked** discrete profile"*. **Route 4 has no banked profile: the gate was unsatisfiable as worded.** `L5` said so in its artefact and used leg 381's banked **synthetic** (controls reproduce leg 381 to `1.996e-12`).
The `NO` is unaffected — threshold-free, resting on an **exponent** (`0.0001085`), not a constant — but **`c_mod = 869.288` is the stand-in's number, not route 4's**. `writeup/CORRECTIONS.md` §34, row 16. **No wave-6 gate names an artefact I have not checked exists.**

**OWED ON THE RUN'S OWN OUTPUT, QUEUED FOR WAVE 7 (not screening, so the standing stop does
not bite):** `L5` shipped a journal and a data file and **no `writeup/novelty/` entry** — the
dir stops at `leg_394.md`. The claim to check: Chae–Wolf's `α`-pin **and** NRŠ/Tsai's exclusion
of exactly-SS profiles **jointly** shut clause (b), because the one surviving obstruction term
is `∝ ṁ`. **This repo does not get to call that new until it is checked.**

**CARRIED FORWARD, NOT ATTEMPTED:** `fig81_route_egmf_v1_evidence.py` + the **52** cited-but-unrebuildable figures (`writeup/check_figure_coverage.py`). Real; not the priority while construction is the binding debt.

**THE RANKING QUESTION WAVE 6 INHERITS, AND DOES NOT ANSWER BY DISPATCHING.** W4 running out of clauses in Lane L does **NOT** re-open Lane T — a decision may not supersede a measurement. Both re-open conditions are unchanged and neither fired. What changed is the **value of `T2″`** (condition (ii)), now the cheapest thing that could put a live W4 clause back in front of Lane L. **Cost before ranking.**

## §OPTIONS-LANE-T — Lane T's whole `OPTIONS.md` §E, retired verbatim 2026-08-19 under §3j

Retired for headroom only, and to sit beside §LANE-T (the same lane's `WALLS.md` body).
**Nothing here is superseded.** The deferral is a user ruling of 2026-08-14, both re-open
conditions are unchanged, and neither has fired. `T2″` remains the cheapest thing that could
put a live W4 clause back in front of Lane L; `T3` remains the lane's undone content.

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
| **T3** | the non-DSS `T³` ansatz | **DEFERRED WITH THE LANE — NOT KILLED.** Still the lane's real mathematical content; runs when a re-open condition is met. Binds: C1's naming requirement. |

## §ORCH-W6-3i — wave 6's seven §3i answers, retired verbatim from the ORCH live block 2026-08-19 under §3j

Retired for headroom only, at the wave-8 planning boundary. **Nothing superseded.** Full text
with the landing audit it belongs to: `writeup/waves/WAVE6_CLOSE.md`.

**§3i, the seven, one line each.** (1) **No** `L1→L4` link moved; Clay ~0.05%. (2) Made FALSE:
`OPTIONS.md`'s `L7` price — *"needs `L6` first, ~10¹ h"* — because an enclosure needs a residual
small enough to contract and this one is **1.6 against a unit-normalised field**; same for `L4`.
`W4(b)` is **untouched** (threshold-free, rests on the exponent). (3) Lane L **keeps** its rank —
three consecutive narrowing units, the only lane on the FINAL blockers. (4) Live ceiling: **every
route-4 CONSTANT is still the synthetic stand-in's**; `L6` did not end that. Plus NRŠ 1996
`SECOND HAND`. (5) **CHEAPEST KILLER, NOW NEXT: `L6-b`** — fix `n_dof = 6720`, raise the cap **800 →
20,000** from `L6`'s banked minimiser plus two seeds, **~10¹ core-h against the ~10³ ladder `L6`
asked for**. Decisive both ways. (6) If Lane L died: Lane V — not cheaper in the way that matters,
it does not touch W4/W5. **No lane re-rank.** (7) **LOOP RISK REAL:** the last three units are
CONSTRUCTION / AUDIT / VERIFICATION — two of three audit-kind. **Applied, not noted:** wave 7's
Lane-L slot is `L6-b`, a measurement on the object; `R-prof` is instrument work, **capped at one
slot**, paired with `E-FE`, which measures the object.
