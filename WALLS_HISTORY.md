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

## §W3-TITLE — retired verbatim from `WALLS.md` W3 on 2026-08-19 (§3j headroom).

*Former title, struck not deleted:* ~~The Grade-A × fluid cell is empty~~ — **false as a matter of
fact**: on leg 174's own definitions the cell is OCCUPIED. A wall whose title and whose test
disagree is how the next over-read gets built.

## §W3-PREDICATE — retired verbatim from `WALLS.md` W3 on 2026-08-19 (§3j headroom).

**The predicate is not tightened and the YES is not withdrawn.** `V3` applied leg 174's criterion
unchanged, having been told not to tighten it, and recorded the YES first with the disqualifying
qualification beside it. Leg 174's predicate stays exactly as written and **stops being described as
W3's test**. Also **struck:** ~~leg 242 confirms nobody filled it since~~ — that over-read stays
struck. **The audit of the YES is QUEUED FOR WAVE 6 and is NOT optional** (ruling Q4, ≈4–8 h): one
database, title-screened, S2 banked a **gap not a zero**. `writeup/data/p2_route_v3_gradeA_v1.json` ·
`experiments/journal/leg_399.md`.

## §W7-COMPLAINT — retired verbatim from `WALLS.md` W7 on 2026-08-19 (§3j headroom).

**Why it is a wall and not a complaint.** Under §3d an unresourced programme cannot return `NO` — it
returns `UNDER-RESOURCED` forever, an unbounded sequence of honest non-answers indistinguishable
from no programme at all.

## §W4-SCOPE — retired verbatim from `WALLS.md` W4 on 2026-08-19 (§3j headroom).

**WHAT THIS DOES AND DOES NOT DO.** It does **not** break W4 — a wall breaks when (a), (b) or (c)
*succeeds*; two are **shut**, the opposite. It says **nothing** about whether 3D NS is regular and
retires neither §6(i) nor §6(ii). **W4's ONLY UNBROKEN CLAUSE IS NOW (c)** — and (c) is **UNTESTED, NOT CLOSED** — — a target not imposing
condition (7): the torus, **deferred with Lane T.** A ranking question, not a wall movement.

## §W-3I-Q6 — retired verbatim from `WALLS.md` LANE PRIORITIES on 2026-08-19 (§3j headroom).

**§3i q6 ("what would we do if Lane L died?") WAS LEFT LIVE FOR WAVE 5, AND WAVE 5 ANSWERED IT.** Narrative retired verbatim 2026-08-18 → `WALLS_HISTORY.md` §PRIORITIES-Q6. **Live consequence: `L2′` shut W4 (a) and `L5` shut (b) — SHUT-UNVERIFIED until `V-W5` reports — so what Lane L has left is re-earned, NOT retired: §6(i)/§6(ii), both no-method. Two clauses closing does NOT re-open Lane T: a decision may not supersede a measurement.**

## §ORCH-W6-L6AUDIT — retired verbatim from `reports/ORCH_STATE.md` on 2026-08-19. **Three of its numbers are CORRECTED at `writeup/CORRECTIONS.md` §38 by `V-W6`; it is kept here as written.**

**`L6`'s LANDING AUDIT AND ITS §3i — FULL TEXT IN `writeup/waves/WAVE6_CLOSE.md`.** What I checked
myself: evidence **30/30**, `C18` re-synthesises `ρ = 1.613811231995` from banked coefficients;
territory **7 files, all added, zero modifications**. **One clause of the unit's summary I do NOT
adopt** — it calls the `NO` *"a fact about the construction, not the stopping point"*. At every rung
above the coarsest, `ρ` is reached by **ONE start, the continuation**; five independent seeds land
**10–24× higher and get WORSE as `n_dof` grows**, all capped at 800 iterations. A ladder whose rungs
each start at the predecessor's minimiser, at a budget too small for the added dimensions, is biased
toward measuring "no change". **The `NO` is about THIS CONSTRUCTION AT THIS BUDGET**, and reading (d)
`UNDER-RESOURCED` is the DOMINANT reading, not a secondary one.

## §ORCH-W6-DISPATCH — retired verbatim from `reports/ORCH_STATE.md` on 2026-08-19 (§3j headroom).

Plan `e202653`, pointer `5c49486`, **both before any worker started**; gates carried **verbatim**
into self-contained briefs. **`V-W5` `95cf861`; `V5` `dacc01c`; `L6` `e62c449`.** Dispatch narrative
retired → `## Superseded — wave 6's dispatch record`. **I planned this wave, so I do not verify it**
— `V-W5` verified **wave 5**; **`L6` is `UNVERIFIED`** and a verifier for it belongs in wave 7.

## §STATE-WAVE34 — the wave 3/4 detail paragraph, retired verbatim from STATE.md 2026-08-19 under §3j
(Retired to make room for `R-bank`'s landing and `E-FE`'s dispatch. Nothing reworded.)

**Wave 3 closed with ONE unit of four returning** (`V-W2`); three worktrees were lost to a host
process exit with their pre-registrations committed and their partial JSON not. That is why every
brief since carries **COMMIT DURING THE RUN, NOT ONLY AT THE GATE**. **Wave 4 returned all three**
(`V3`, `V-W3`, `L2′`), each row in the **Landed** table above with its SHA and its gate answer in the
gate's own wording. Narrative, headroom and the §3i answers for both waves: `reports/ORCH_STATE.md`
Superseded LIVE blocks (verbatim, nothing reworded) and the integration commits `6320790`, `391fd8f`.

## §STATE-WAVE5-PRECEDENT — retired verbatim from STATE.md 2026-08-19 under §3j

(Retired for headroom at `R-bank`'s landing. The rule itself stays live in STATE.md as a one-liner.)

**The precedent it set, kept live because it binds every wave:** a request to change a gate
**mid-wave was REFUSED**. Plan verbatim: `writeup/waves/WAVE5_PLAN.md` @ `1e49a00`.

## §STATE-LANDED-UNVERIFIED — three Landed-table rows retired verbatim from STATE.md 2026-08-19 under §3j

(Retired for headroom at `R-bank`'s landing. All three are still **UNVERIFIED** and that obligation stays
live in `STATE.md` as a single pointer row. Nothing reworded.)

| unit | gate answer | SHA | state |
|---|---|---|---|
| **`D-REPAIR`** (wave 5, infra) | **GATE `NO`, twice, with the enumeration.** The record cites **110** figure ids: **45 rebuilt, 22 self-checked, 52 cited-with-a-`.png`-and-no-rebuild-path.** `NO` **before the repair and `NO` after** — the four debts were one figure of 66. **`V-W3`'s D3 is WRONG IN SIGN** (`E` used **+1.9% MORE** epochs/attempt, not −2.3% fewer) and its D5 *cannot close* is wrong (subset recovered, **9.0884 core-h**); **D2 no longer exists.** Detail and 11 unrepaired flags: `experiments/journal/d_repair.md`. | `036e56d` | **UNVERIFIED** |
| **`V-W3`** (wave 4, verification) | **3 of 4 CONFIRMED, 1 REFUTED.** `E`'s headline reproduces 6/6; `V-W2` confirms on both parts from **re-fetched primaries** (`.mat` fields **bitwise**); `fig107`'s `P2_EVIDENCE` gap confirmed by `ast.literal_eval` (36 entries, `107` the only gap in 99–110). **REFUTED: `E`'s `8×` overrun — `0.0713` is WALL-h, `0.57` is CORE-h; like for like `E` came in 0.4% UNDER.** 6 defects **unrepaired**, 0 `UNREACHABLE`. | `2b8755e` | **UNVERIFIED** |
| **`V1`** (wave 2, verification) | **All five wave-1 claims reproduce** from banked JSON and landed evidence scripts alone; **`M3 = DELIVERED` SURVIVES** U5's 57% seed overlap. Two defects banked, not reconciled. | `2fb399f` | **UNVERIFIED** |

## §W4-PROV2 — the `V-W4` provenance paragraph, retired verbatim from WALLS.md 2026-08-19 under §3j

(Retired for headroom before `L6-b`'s landing. The clause that MATTERS — ESŠ is `UNREACHABLE` at
primary and the pin rests on secondaries — is kept live in `WALLS.md`. Nothing reworded.)

**⚠ `V-W4` CORRECTED THE `≤ 1` PROVENANCE; THE DIRECTION HOLDS and (a) STAYS SHUT** — not
through the **global** Leray–Hopf ESŠ theorem (this object's global energy is measured
**infinite**) but through the **local** suitable-weak form (Seregin, `arXiv:math/0510396` §1),
whose `m_T` separates the cases **exactly at the pin**. **ESŠ is `UNREACHABLE` at primary: the
pin rests on secondaries.** Four citation defects, verbatim → `WALLS_HISTORY.md` §W4-PROV;
register `writeup/CORRECTIONS.md` §33; detail `experiments/journal/verify_wave4.md`.

## §HIST-NOTE — WALLS.md's own `# History` rationale paragraph, retired verbatim 2026-08-19 under §3j

(Retired for headroom before `L6-b`'s landing. It is a one-time PROCESS note, not a statement about
any wall. The rule it records is unchanged and still in force: nothing deleted, nothing unstruck.)

**MOVED 2026-08-18 to `WALLS_HISTORY.md`, struck text intact and byte-for-byte.** WALLS.md's §3j cap
is 32 KB and the named remedy — *retracted text stays struck but moves to a `## History` section at
the foot* — had stopped buying headroom once the section itself grew to ~2.9 KB. The remedy is
extended one step rather than abandoned: **nothing is deleted, nothing is unstruck**, and every
`## History` pointer in this file now resolves to `WALLS_HISTORY.md`. Flagged, not silent.


## §W4-L6CEIL — `L6`'s landing ceiling, retired VERBATIM from `WALLS.md` 2026-08-19 on `L6-b`'s landing

Retired because `L6-b` (leg 406) measured two of its numbers and **one of them was a property of
the iteration cap, not of the construction** (`CORRECTIONS.md` §46). Kept verbatim, not compacted,
so the withdrawn figure stays legible beside its correction. `V-W6` had **upheld** this text.

**CEILING, MEASURED BY THE CONDUCTOR ON LANDING, NOT CLAIMED BY THE UNIT, RULED ON BY `V-W6`: at
every rung above the coarsest, `ρ` is attained by ONE start — the continuation. UPHELD both
branches.** Seed spread **3.93–23.67× on B, never above 5.95× on A** (my "10–24×" was the top of the
range quoted as the range — `CORRECTIONS.md` §38); it worsens with `n_dof` in the per-rung
**minimum**, not seed by seed; all 133 hit **their** cap, 58 at 800 and 75 at 250. **`V-W6` adds two
facts I missed, both stronger:** the cap sweep is a post-hoc TRUNCATION of the same full-budget runs,
warm-started from below, so it **controls nothing**; and the banked minimiser is **~14 orders from
its pre-registered `gtol`** (`153.22` vs `1e-12`), growing with `n_dof` on both. The ladder inherits
its predecessor's minimiser at a budget too small to explore the added dimensions. **The `NO` is
about THIS CONSTRUCTION AT THIS BUDGET**; `L6-b` separates budget from ansatz.

---

## §STATE-WAVE7-RETURNS — retired from `STATE.md` 2026-08-19 under §3j when wave 8 was dispatched. VERBATIM, seven rows.

**RETURNED — `V-W6`** (leg 407, `c7f242c`, `writeup/data/p2_verify_wave6_v1.json`). **`V5` VERIFIED. `V-W5` VERIFIED. `L6` VERIFIED-WITH-QUALIFICATION** — gate answered exactly, artefact fully re-derivable, **no arithmetic defect anywhere in wave 6**. 65 checks 0 fail (`--deep` 68); self_hash recomputes; territory 3 files all `A`; **0 repaired, 0 artefacts edited**. 11 defects open.

`V-W6` cont.: my `L6` landing audit **UPHELD on the one-start finding** (its genuine find, the unit never said it), **overstated 3×**, **wrong once conservatively** (`1.6` is branch B; the unit-normalised branch is A at **7.58**, so `L7` is blocked HARDER). **Understated twice**: the cap sweep controls nothing, and the minimiser is **~14 orders from its `gtol`**. `CORRECTIONS.md` §38.

**`V-W6`'s most serious finding (`D-VW6-2`)**: all 133 starts exited `status = 1`, not one converged by gradient or `ftol`; `scale_invariant_grad = 153.22` against a pre-registered `1e-12`, growing monotonically with `n_dof` on both branches. **`L6`'s bolded §8.2 claim has no surviving support.** `D-VW6-7` (undeclared scipy) **REPAIRED** in the integration commit.

**RETURNED — `R-prof`** (leg 405, `1f89ceb`, `writeup/data/p2_r_prof_v1.json`). Gate (iii) **NO**: `PROG-R4`'s loop is **4.34× slower** than the named reference (cpu median; wall 4.21; **worst wall round 1.9975** — "every round exceeds 3×" is true on the **cpu clock only**, a Conductor landing finding the unit's prose over-generalised).

`R-prof` cont.: (i) 15-row table sums to **exactly 100.0**, **79.1% transforms**; (ii) fixed fraction **0.596** (`N = 4..512`). Remedy pre-planned FFTW3 **3.41×**, **priced not landed** (it moves every banked orbit at the last bit). Solver **unmodified**, sha256 matches live. Machine not quiet, positive control **failed** — both disclosed. **W7 unmoved; no link moved.**

**RETURNED — `R-bank`** (leg 404, `8019c35`, `writeup/data/p2_r_bank_v1.json`). **`YES` on all three.** (i) **160/160** bit-identical to `regenerate`, run both one-per-call and all-in-one-call; (ii) **16/16** vs `E`'s ledger, `ulp_gap 0`; (iii) attempt 15 reproduces **12/12 ledger entries byte-equal with the two DNS artefacts ABSENT**. `self_hash 3b592e3c…` recomputed MATCH. 1.06 core-h.

`R-bank` cont.: seedbank **TRACKED, 737,408 B** — it cannot die with a container, which the DNS ckpts have **twice**. I re-hashed all 160 slices vs the manifest and re-ran `regenerate` on 4 fields myself, bitwise. Defect **§39**: `~1.2 GB` is **268.9 MB**, and was `U2`'s *rejected* archive size. **No wall moved; no link moved.**

---

## §W4-L6-L6B — retired from `WALLS.md` 2026-08-19 under §3j at `PB2`'s integration, when the file went 2,151 B OVER cap. VERBATIM.

**⚠ ROUTE 4 NOW HAS A DISCRETE PROFILE — `L6`, leg 401 — AND IT DOES NOT CLOSE.** First ever
built on route 4's own object (λ-DSS, `a = 0.5`, poloidal–toroidal, `div V ≡ 0` identically, **no
Bogovskiĭ corrector**), measured in **`L5`'s own load-bearing norm**. Smallest residual at the best
affordable resolution (`n_dof = 6720`): **`ρ = 1.6138`** with the `α = 1` far-field amplitude
normalised to **1** — *order one*, not small. **It does NOT decrease under refinement:**
`d log ρ / d log n_dof = −0.0222` over the last three rungs, **0.497 %** at the top. Evidence
reproduces independently (30/30; banked coefficients re-synthesise `ρ` exactly). **The `Ks = 0`
of freedom are load-bearing — the construction did NOT collapse to (D)SS.**
**CEILING ON `L6`, MEASURED ON LANDING, RULED ON BY `V-W6` — AND PARTLY WITHDRAWN 2026-08-19 BY
`L6-b`.** At every rung above the coarsest, `ρ` is attained by ONE start, the continuation: **this
STANDS**, and `L6-b` re-measured it at 25× budget — both fresh seeds reach only `6.46`/`6.50`,
outside `[1.55,1.70]`. **WITHDRAWN: the magnitude.** *"Seed spread 3.93–23.67× on B"* is a property
of the **800-iteration cap**, not the landscape — the same seeds read `17.81–22.07×` at `k=800` and
**`4.29–4.32×` at `k=20,000`** (`CORRECTIONS.md` §46; `V-W6` upheld the withdrawn version).
**All 133 starts hit their cap; all 58 at 800; 56/58 non-critical — the ladder compared STOPPING
POINTS, never stationary ones.** `V-W6`'s two harder facts stand: the cap sweep is a post-hoc
TRUNCATION of the same warm-started runs and **controls nothing**; the banked minimiser is ~14
orders from its pre-registered `gtol`. **`L6-b` (leg 406, `4df0ca0`) ANSWERED: `NO`.** 20,000
iterations, 43.3 core-h → **`ρ = 1.5048519`, −6.75%**, threshold `<1.45` not met; terminal
`‖x‖‖∇J‖₂/|J|` = **44.6/12.0/5.2**, none stationary. **It licenses ONLY: budget alone does not
reach 1.45; `L7`/`L4` prices stay OPEN; the ansatz is NEITHER exonerated NOR convicted** — the
plan's *"the stall is the CONSTRUCTION"* needed a stationary iterate and is SUPERSEDED
(`CORRECTIONS.md` §41). SS-collapse control does **not** fire (`1.88e-3` vs `1e-6`).

---

## §W7-U3QUEUE — retired from `WALLS.md` 2026-08-19 under §3j at `PB2`'s integration. VERBATIM.

**2026-08-18 — SIZE IS NOT THE BINDING RISK, PERSISTENCE IS.** `U3` **finished**: 14.47 h wall,
144.69 core-h reserved, 92.9% utilised. Every recorded loss (13 agents 08-06, 5 on 08-07, `E`
killed twice, 3 of 4 in wave 3) was a suspended session or a **gitignored** checkpoint, never a
job too big. **QUEUED 2026-08-18 by user directive** (the "price, do not queue" clause was
WITHDRAWN): `writeup/prices/FIELD_ENSEMBLE_2026-08-18.md`, 160 attempts, ~91 core-h.


---

## §W4-CUTOFFBILL — retired from `WALLS.md` 2026-08-19 under §3j at `PB2`'s integration. VERBATIM.

**What is measured.** Leg 381's cutoff bill: the critical `L³` tail runs at **326.875 per decade**
(increment of the *cube*; the norm itself runs 8.679 → 14.841), required decay exponent `α > 1.5`
against an a-priori `α = 1.0`, **deficit 0.5**. Leg 390 priced the torus alternative: `α > 2.996995`
to wrap the uncut profile, deficit 1.996995 — **3.99399× worse** — but **0.0 if the profile is cut
first** (disjoint supports at `L > 2ρ`), in which case leg 381's bill is inherited unchanged. Leg
390's own words: **"(D) deletes the acceptance test, not the work."**


---

## §W3-V5AUDIT — retired from `WALLS.md` 2026-08-19 under §3j at `PB2`'s integration. VERBATIM.

§W3-CELL. **`V5` (leg 402) has now AUDITED the occupant at full text: the certificate DOES close**
— 24 recomputable constants re-derived at 50 dps, **four printed constants fail** (`H28`, `H30`,
`H32`, `H33`; the real one is `x_0^U`, `1.44e-5` printed against `1.45054706437e-5`, from
substituting `η₂ = 0.005` where the certified `M_2^U ≤ 0.0061` belongs), and **carrying the
corrections through, closure survives** — `x_1^U` clears by **0.08%**, recorded as **luck, not
margin**. **Class A (22 interval-arithmetic inputs) was NOT verified and is banked as a LIMIT OF
THE AUDIT, never as a pass.** **W3 IS UNMOVED: the audit did not run W3's prose test.**
`CORRECTIONS.md` §36.

**Predicate not tightened, `YES` not withdrawn; leg 242's over-read struck; the wave-6 audit that
ruling Q4 made non-optional is DONE (`V5`, leg 402, VERIFIED by `V-W6`). Retired verbatim 2026-08-19
→ `WALLS_HISTORY.md` §W3-PREDICATE.**

---

## §R2R5-LEDGER — retired from `WALLS.md` 2026-08-19 under §3j at `PB2`'s integration. VERBATIM.

- **R2 deflation** — strongest surviving item; attacks the largest measured waste (`R0`: **57 of U5's
  100 seeds already spent by U3**). Deflate against the union of both runs' solutions.
- **R3 multiple shooting** — named by route-DSSP brick **B6's own spec**, built without it.
- **R4 second-order stepper** — U3's is **Lie–Trotter, globally first order** (measured ratio 2.00),
  so its orbits are `O(dt)` perturbations of the true flow's. **`E-iii` promoted it. Invalidates M1's
  reproduction; must re-run it.**
- **R5 carry `m`** — every negative here about orbit recovery carries *"with a residual that cannot
  represent one of the two shift classes."* **CORRECTED by U5: R5 does NOT help the band** (334
  anchored candidates, **1** in the published `|s|` band). It is the fix for `|s| > 0.9`, and is the
  same unit as `PROG-R4` **C** — don't double-count.

## §OPTIONS-R6R7 — OPTIONS.md rows R6 and R7, retired VERBATIM 2026-08-19

Both units are TAKEN and LANDED (`R6` = leg 403 `1f89ceb`; `R7` = leg 404 `8019c35`), both VERIFIED
by `V-W7` (leg 412, `aefe590`). Retired to fund the `L6-e` row and the §51 ladder finding on a
capped surface (`ORCHESTRATION.md` §3j). Moved, not compacted; not one character altered.

| **R6** | **profile the inner loop** | **TAKEN 2026-08-19, leg 403 — gate (iii) `NO`** | **In 403 legs no unit has profiled it**, and every cost figure here inherits `95.389 s/epoch` unexamined. Smoke test: transform cost **flat from `N=24` to `N=32`** — per-call **overhead**, paid 20× per step. Two-sided; a YES is a **useful negative**. §C. **ANSWERED (`1f89ceb`, `writeup/data/p2_r_prof_v1.json`): 4.34× slower than the named reference (cpu median; wall 4.21; worst wall round 1.9975, so the unit's "every round exceeds 3×" is cpu-clock-only — Conductor finding). 79.1% transforms, fixed fraction 0.596. Remedy pre-planned FFTW3 3.41×, PRICED NOT LANDED — it perturbs every banked orbit at the last bit, which is `R4`'s problem, so it needs its own unit and its own equivalence check. A speedup breaks no wall.** |
| **R7** | **bank the seed fields** | **TAKEN 2026-08-19, leg 404 `8019c35` — `YES` on all three: 160/160, 16/16, and one attempt bit-for-bit with NO DNS** | Blocker was a **`.gitignore` line** — now a **tracked 737,408 B** blob that cannot die with a container (it has, twice). Buys `E-FE` ~27.5 of 90.9 core-h. `1.2 GB` was wrong: measured **268.9 MB** — §39, and it was `U2`'s *rejected* archive size. Ceiling **C2**: the bank is now the seed's **definition** on this CPU, not a cache. |

## §W4-A-PROV — WALLS.md W4 clause (a), the `V-W4` provenance correction, retired VERBATIM 2026-08-19

Clause (a) is SHUT by `L2′` and VERIFIED by `V-W4`; the provenance of the `≤ 1` was corrected by
that verifier and the direction held. Settled, unchallenged since, and cited nowhere as live.
Retired to fund `CORRECTIONS.md` §51's ladder finding on a capped surface (`ORCHESTRATION.md` §3j).
Moved verbatim, 21 lines, not compacted.

**⚠ `V-W4` CORRECTED THE `≤ 1` PROVENANCE; THE DIRECTION HOLDS and (a) STAYS SHUT** — through the
**local** suitable-weak ESŠ form (Seregin `arXiv:math/0510396` §1), not the global Leray–Hopf one.
**ESŠ is `UNREACHABLE` at primary: the pin rests on SECONDARIES** — which is `PB2`'s subject.
Paragraph + 4 citation defects verbatim → `WALLS_HISTORY.md` §W4-PROV, §W4-PROV2; `CORRECTIONS.md` §33.

**(b) SHUT, ✅ VERIFIED by `V-W5` (leg 403) — an ENDPOINT not a gap. Five items
reproduce; `C6`'s tolerance was NEVER moved (`347676f`). ⚠ **Arithmetic, not science**, and the
CONSTANT is basis-dependent by **1.476×**: `CORRECTIONS.md` §35.** The ansatz was **built**: cut-off **potential**
(`div V ≡ 0` exactly, no Bogovskii corrector to grow), physical support frozen at `κ = a`, **Clay
condition (7) verified by measurement.** Gate **`NO`, threshold-free** — in `‖curl F‖_{L¹_t L^{3/2}_x}`
the error saturates at **`c_mod = 869.288` per unit similarity time**, ρ-exponent **`+1.09e-04`** out
to `|y| = 1261.7`: **enlarging the cutoff buys nothing**, `Σ(∞) = ∞`, so it fails for **every**
`ε_close > 0`. What survives is **exactly the modulation commutator `T3 ∝ ṁ`** (`‖R_loc‖/‖T3‖ =
0.999998`), size `ρ^{1-α}`. **Both exits are shut by the SAME pin:** `α > 1` strictly — which (a)
shows destroys the object — or `ṁ ≡ 0`, exactly self-similar, excluded by **Nečas–Růžička–Šverák**
(ARMA 136, 1996) and **Tsai** (ARMA 143, 1998). It did **not** collapse into (D)SS: `κ = 0` **is**
exactly DSS (`7.5e-16`), called a `NO` and stopped; `κ = a` is **not** (`1.0857`). Controls carry it:
at `α = 1.25`, `1.6` the machinery returns `−0.2498`, `−0.5996`, tracking `1 − α`. **Ceiling: Tier 2,
float64, SYNTHETIC profile — route 4 has none banked. The EXPONENT is a class property and is settled;
the CONSTANT is not route 4's number.**

## §STATE-W7-RBANK-RPROF — two STATE.md wave-7 return rows, retired VERBATIM 2026-08-19

Both units VERIFIED by `V-W7` (leg 412, `aefe590`) against their pre-committed gates. Substance
lives at `WALLS.md` W7, `OPTIONS.md` R6/R7 and `CORRECTIONS.md` §50 item 6. Retired to hold
`ORCHESTRATION.md` §3j's STATE.md cap while landing `V-W7` and `PB1`. Moved, not compacted.

**RETURNED — `R-prof`** (leg 405, `1f89ceb`): gate (iii) **`NO`** — the loop is **4.34×** a named reference, not the 3× the unit's own wording claimed for every round (that was **cpu-clock-only**; worst wall 1.9975). Remedy priced, **not landed**; breaks no wall. Detail VERBATIM → §STATE-WAVE7-RETURNS.

**RETURNED — `R-bank`** (leg 404, `8019c35`): **`YES` ×3**; 160/160 bit-identical, seedbank **TRACKED**, both DNS field artefacts **ABSENT**. I re-hashed all 160 and regenerated 4 — bitwise. My own `~1.2 GB` estimate was **268.9 MB** in fact (`CORRECTIONS.md` §39). Detail VERBATIM → §STATE-WAVE7-RETURNS.

## §STATE-W6-V5 — the STATE.md `V5` row, retired VERBATIM 2026-08-19

`V5` (leg 402) is landed and VERIFIED by `V-W6`. Substance lives at `WALLS.md` W2/W3 and
`CLAY_OBLIGATIONS.md`. Retired to hold §3j's STATE.md cap while landing `V-W7` and `PB1`.

**`V5` `dacc01c`** — both clauses **YES**: the `2509.25116` certificate **CLOSES** (24 constants at 50 dps, **four printed ones fail**, `x_1^U` clears by **0.08% — luck, not margin**) and the profile **IS genuinely 3D** (swirl **57%** of `max|u_r|`). **Class A NOT verified — a LIMIT, never a pass. W3 does NOT move: its prose test was not run.** **`V-W5` `95cf861`** — five items reproduce, **`C6`'s tolerance NEVER moved**, 3 defects found. `L6` remains **`UNVERIFIED`**.

## §W-LANEL-FIRSTTWO — the WALLS.md Lane-L "first two units in 400 legs" block, retired VERBATIM 2026-08-19

The two units it celebrates are `L5` and `L6`. Both are now heavily qualified by the same day's
work: `CORRECTIONS.md` §51 (the ladder was differenced at an iteration cap that dominates it), §52
(`J` is a divergent integral; every finite value is a truncation value) and §53 (the Conductor's
landing audit: the divergence reaches the minimiser, but its SIGN protects both `NO`s). The block is
retired because its framing — two clean landings — is no longer the shortest true description, not
because anything in it was found false. Substance now lives in the W4 blocks above it. Retired to
fund §52/§53 under `ORCHESTRATION.md` §3j. Moved verbatim, 26 lines, not compacted.

**⚠ 2026-08-18 — THE LANE LANDED ITS FIRST TWO UNITS IN 400 LEGS, AND BOTH NARROWED IT.** `L2′`
(leg 397, `1493e5e`, **VERIFIED by `V-W4`**) closed **W4 clause (a)**; `L5` (leg 400) closed **clause
(b)**, threshold-free, with the number. Both are recorded in full at **W4** and neither is restated
here. **What this lane has left is W5, §6(i) and §6(ii) — all three untouched, all three no-method —
and inside W4 only clause (c), which is Lane T's.** A lane that closes its own attacks is doing its
job; it is not the same thing as progress, and no `L1→L4` link moved for either unit.

**L1 — price §4 on `ℝ³`.** ~~Read the published attempts to localise a self-similar profile to
finite energy; state, per attempt, the named hypothesis that fails for DSS.~~ **DONE by `L2′` for
the decay clause** (18 techniques, 7 families). Residual: the **four pre-arXiv primaries**
(NRŠ 1996, Tsai 1998, Bogovskiĭ 1979, Giga–Kohn) banked **`UNREACHABLE` as declared in advance**
and quoted through secondaries — ~1 unit, **low value**, and **no author contact** (prohibited).
**L2 — attack §6(i).** ~~Is certified far-field decay plus an admissible cutoff genuinely without
method, or without an *attempt*?~~ **ANSWERED: without method, and the method cannot exist for this
object.** §6(i) is **NOT retired** — it wants *certified* decay and a built cutoff, and `L2′`
produced neither. Certifying it costs **≥ 1 full wave** (interval/NK enclosure on route 4's own
profile + a cutoff controlled in a scaling-invariant norm), and **§6.2 predicts the answer is
`α_hi = 1`** — which does not pay the bill.
**L3 — attack §6(ii).** Persistence under localisation — downstream of L2 in logic but not in
literature: the published techniques (nonlinear stability with a finite unstable spectrum, the
Chen–Hou line) have never been read against *this* object.

**BREAKING EITHER OF §6's OBLIGATIONS IS THE SINGLE MOST VALUABLE OUTCOME AVAILABLE TO THIS
PROGRAMME** — more valuable than a Tier-2 candidate, because a candidate without them is what we
already know how to produce. **A measured "still no method, and here is precisely which hypothesis
fails" is also a real result** — the one that says whether the Tier-2 ceiling is permanent.

## §OPTIONS-L7 — the OPTIONS.md L7 row, retired VERBATIM 2026-08-19

`L7`'s precondition is NOT MET and is now further from met: `§52` shows the residual it would
enclose is a truncation value of a divergent integral. Retired to fund the `L6-e` v2 gate under
`ORCHESTRATION.md` §3j. Moved verbatim, not compacted.

| **L7** | interval the commutator | **PRECONDITION NOT MET — "needs `L6` first" is discharged IN LETTER ONLY.** An enclosure needs a residual small enough for a contraction to close; `L6`'s is **7.58** on the genuinely unit-normalised branch A — **CORRECTED 2026-08-19**: the 1.6138 is branch B, whose Gaussian-weighted interior `L²` is 0.0022, 0.22% of A's (`CORRECTIONS.md` §38). **`L7` is blocked HARDER than the landing audit said, not less.** **Do not dispatch until `L6-b` rules.** The `~10¹` price assumed banking a profile meant banking an ACCURATE one. | **re-price after `L6-b`** |

## §OPTIONS-L4 — the OPTIONS.md L4 row, retired VERBATIM 2026-08-19

Retired to hold `ORCHESTRATION.md` §3j's OPTIONS.md cap while landing `L-JVER`/§52/§53.
Substance at `CLAY_OBLIGATIONS.md` §6(i) and `WALLS.md` W4. Moved verbatim, not compacted.

| **L4** | **certify the decay** | §6(i) wants *certified* decay + a built cutoff; `L2′` built neither. Interval/NK enclosure on route 4's own profile — **and `L6` measures that no accurate such profile exists yet (`ρ ≈ 1.6`), so `≥1 full wave` is a FLOOR, not an estimate** — plus a cutoff in a scaling-invariant norm. **`§6.2` predicts `α_hi = 1`, which does not pay the bill.** | **≥1 full wave** |

## §STATE-W67-L6 — three STATE.md rows (`V-W6`, `L6-b`, `L6`), retired VERBATIM 2026-08-19

All three are superseded in their READING, not in their numbers, by `CORRECTIONS.md` §51/§52/§53:
the ladder was differenced at a dominating iteration cap, and the functional is a divergent
integral whose finite values are truncation values. The gate answers stand. Retired to hold
`ORCHESTRATION.md` §3j's STATE.md cap while landing `L-JVER`. Moved verbatim, not compacted.

**RETURNED — `V-W6`** (leg 407, `c7f242c`): **`V5` VERIFIED, `V-W5` VERIFIED, `L6` VERIFIED-WITH-QUALIFICATION**; 11 defects open, 0 repaired. My own landing audit came back **3 numbers overstated, 1 wrong conservatively, 2 UNDERSTATED** (`CORRECTIONS.md` §38). Its `D-VW6-2` (no start converged by `ftol`; `scale_invariant_grad 153.22` vs pre-registered `1e-12`) is what `L6-b` and §41 act on. Rows retired VERBATIM → `WALLS_HISTORY.md` §STATE-WAVE7-RETURNS.

**RETURNED — `L6-b`** (leg 406, `4df0ca0`, `writeup/data/p2_route_l6b_v1.json`). Gate **`NO`**: `ρ = 1.5048519` at 20,000 iters (25× `L6`), **−6.75%**, threshold `<1.45` not met; 43.3 core-h; 57/57. Terminal `‖x‖‖∇J‖₂/|J|` **44.6/12.0/5.2 — not stationary**, so §41 bites: the plan's *"the stall is the CONSTRUCTION"* is **SUPERSEDED**. Licenses ONLY *budget alone does not reach 1.45; `L7`/`L4` OPEN; ansatz neither exonerated nor convicted*. Both cold seeds `6.46`/`6.50`, outside `[1.55,1.70]`.

**`L6` `e62c449`** (leg 401) — route 4's first discrete profile, gate **`NO`**: `ρ = 1.6138` in `L5`'s norm at `n_dof = 6720`, not decreasing under refinement (`−0.0222`). **Its landing ceiling is PARTLY WITHDRAWN** — the seed-spread magnitude was a property of the 800-iter cap (`CORRECTIONS.md` §46); what stands is that `ρ` is attained by the continuation start alone. Superseded on budget by `L6-b` above.

## §STATE-PIVOT-FLOOR — the STATE.md paper-pivot composition-floor row, retired VERBATIM 2026-08-19

Standing user directive, unchanged and still binding; retired from STATE.md only to hold
`ORCHESTRATION.md` §3j's cap. It governs wave 9 exactly as written. Moved verbatim, not compacted.

**§3g's composition floor STANDS: paper units are ADDITIONAL, not a substitute.** Two units come before any drafting — **`PB1`** (`P1`'s owed novelty check; a YES kills `P1` and is a GOOD result) and **`PB2`** (both jaws of `P2`'s pincer read at PRIMARY). **`PB2` is not a paper errand: W4 clause (b) is recorded SHUT AND VERIFIED on two theorems this repository has never opened.** A jaw that does not close as cited goes to the user **immediately**.


---

## §STATE-WAVE8 — `STATE.md`'s WAVE 8 block, retired VERBATIM 2026-08-19 at the wind-down (§3j). Nothing edited. Wave 8 is CLOSED AND INTEGRATED; the live summary that replaced it is in `STATE.md` and the full audit is in `writeup/waves/WAVE8_CLOSE.md`.

## WAVE 8 — **IN FLIGHT 2026-08-19: `L-JVER` ‖ `PB2` ‖ `PB1` ‖ `V-W7`** (legs 409–412), plan `writeup/waves/WAVE8_PLAN.md` + 4 amendments, committed **before** dispatch. Composition floor: `L-JVER` (re-implements `W[V]`/`J(c)` in a different basis; gate `|ΔJ|/J < 1e-3`). `V-W7` verifies **wave 7 AND my seventeen integration commits** — I planned it, I may not. `E-FE` is a LATE RETURN and **may not influence this wave's ranking** (`99421dd`).

**RETURNED — `PB2`** (leg 410, `a7ffa1e`): gate **`YES`**. **`W4` clause (b) is carried by TSAI 1998 THM 2** — hypotheses (i) equations + (ii) local energy estimates, **no `L^q` at all** — verified by me at FULL TEXT, and met by measurement. **NRŠ does NOT apply** (`∫|U|³` log-divergent at `α=1`), so the one `UNREACHABLE` source is **not load-bearing**. Clause (b) STANDS, stronger than its citation. 31/31, but **0/31 recompute-from-primary**.

**RETURNED — `L-JVER`** (leg 409, `2acaa9e`): gate **`NO`** — `1.0e-4`/`1.2e-4` at both minimisers, **`42.9%`** at a non-minimiser. **NEITHER PROGRAM IS MISCODED**: `X9` runs the unit's own operator on `L6`'s nodes+weights, reproduces `J_L6` to `1e-14` at all four points.

**⟹ `J` IS A DIVERGENT INTEGRAL** (`§52`), log-divergent at `r→∞` and `r→0`. **Every finite `J` in this record is a value of `L6`'s 72-node, `r ∈ [5.5e-4, 7.27e3]` truncation, not of the functional.**

**⚠⚠⚠ MY LANDING AUDIT (`§53`) GOES FURTHER:** the divergence reaches **the minimiser** — `+6.226e-5`/`+6.246e-5`/`+6.212e-5` per decade over `r_max` `1e6→1e14`, **three bands inside 1%**. `ρ = 1.6138` has **no limit**; P1's PASS is not convergence.

**AND THEN LIMITS IT. THE SIGN IS POSITIVE**: less truncation ⟹ larger `ρ` ⟹ **further** from `<1.45`. **`L6`'s and `L6-b`'s `NO`s SURVIVE; the numbers do not.** §52 does **NOT** subsume §51 — the divergence coeff is **×130 below** the last ladder step. Two independent defects, same four numbers.

**`W4`(b) NOT affected** — `PB2` closes it on Tsai Thm 2 hypotheses measured directly; `c_mod`/`J`/`curl F` absent from its artefact (I searched). **`L5`'s `c_mod = 869.288` FLAGGED**: its ρ-exponent `0.000109` "saturation" is what a log divergence fits to, and its sweep stops ~3 decades short. **NOT adjudicated; sweep owed.**

**RETURNED — `V-W7`** (leg 412, `aefe590`): wave 7 **VERIFIED** — `R-bank`, `R-prof`, `L6-b` all clean against their pre-committed gates. *"Every discrepancy is in the integration, not the units."* **SEVEN defects ruled against ME.** All seven re-checked at primary by me: **6 UPHELD, 1 UPHELD IN PART** (§50–§51).

**⚠⚠ THE WAVE'S BIGGEST ITEM IS AN UNDER-CLAIM, NOT A DEFECT — `CORRECTIONS.md` §51.** `L6`'s four-rung refinement ladder moved `−4.994561%`; `L6-b`'s ONE ×25 budget step at FIXED `n_dof` moved `−6.751678%` = **×1.3518 of the ENTIRE ladder**. Both banked, both correct, **nobody divided one by the other for 11 legs.** `L6`'s *"not decreasing under refinement"* is budget-confounded; `J3` needs `7.2153%` to INVERT and `6.7517%` is measured one rung up. **Margin 0.46 pp** → `L6-e` (~20–35 core-h, gate pre-committed, wave 9).

**RETURNED — `PB1`** (leg 411, `440f28c`): gate **`YES` — `P1` IS KILLED, and that was pre-committed as a GOOD result.** Both effects are in print at `FULL TEXT`: score-monotone admission bias (Page–Holey–Brenner–Kerswell, *JFM* **991** (2024) A10, p.18; Chandler–Kerswell 2013 p.13 — **twelve years old**), and re-mining re-finds (CK13 p.14 Table 1; LK15 p.5). **`P1`'s framing word *silently* is contradicted by its own intended bibliography.** 1 of 12 controls did not fire (`pos_topical`), disclosed, not re-planted, nothing rests on it.




---

## §OPTIONS-R6R7-L1RES — three `OPTIONS.md` rows retired VERBATIM 2026-08-19 at the wind-down (§3j), to pay for `L6-e`'s never-dispatched annotation. Nothing edited. `R6` and `R7` are DONE and VERIFIED by `V-W7`; `L1-res` is SUPERSEDED by `writeup/SOURCES.md`.

| **R6** | profile the inner loop | **DONE leg 403 `1f89ceb`, VERIFIED `V-W7`.** Gate (iii) `NO`, 4.34×. Row retired verbatim → `WALLS_HISTORY.md` §OPTIONS-R6R7; substance at `WALLS.md` W7. | done |
| **R7** | bank the seed fields | **DONE leg 404 `8019c35`, VERIFIED `V-W7`.** Row retired verbatim → `WALLS_HISTORY.md` §OPTIONS-R6R7. ⚠ `--verify` CANNOT FAIL (0 `raise`/`assert`/`sys.exit`) — `V-W7` §, remedy owed. | done |
| **L1-res** | the 4 pre-arXiv primaries | **SUPERSEDED 2026-08-19 by `writeup/SOURCES.md`** (rows 2, 3, 19, 20). Live debt is NRŠ 1996 alone → `L7-src`. | see `L7-src` |


## §OPTIONS-A3 — retired verbatim 2026-08-19 under §3j (wind-down): OPTIONS.md §A, the pool constraint on the four not-taken PROG-R4 options

**The constraint shaping all of them:** the anchored admissible pool is **exhausted** at `R < 0.25` —
241 exist, 100 spent, **141 remain, only 12 in-band** — so nothing keeping the current window can push
the in-band arm past 72 attempts, ever. **And U5's pre-committed reading fired on branch (b): the bias
is in the BASIN STRUCTURE, not the seed supply.**


## §OPTIONS-A2ROW — retired verbatim 2026-08-19 under §3j (wind-down): OPTIONS.md §A table row A/B/D (body already at §OPTIONS-A2)

| **A**, **B**, **D** | all three **BUY SUPPLY** | — | **RETIRED, NOT DEFERRED**: proposing more seed supply for `PROG-R4` is a **standing user prohibition**, so these were never choosable. Verbatim → `WALLS_HISTORY.md` §OPTIONS-A2. | Only by a user ruling that lifts the prohibition. |


## §OPTIONS-U4G2 — retired verbatim 2026-08-19 under §3j (wind-down): OPTIONS.md §A, U4/G2 basin radius and G1

**`U4`/`G2`, basin radius: BLOCKED, not an option** — it needs a recovered *named* orbit to perturb
and there is not one. **`G1` stays `UNDER-RESOURCED`; `E` did not write to it** (hand-placed seed at
published coordinates, not a mined seed).


### §OPTIONS-A-WHOLE — `OPTIONS.md` section A retired VERBATIM 2026-08-19 to pay for `§G`'s `P0-NS12` entry (`CORRECTIONS.md` §59). Nothing here is closed; it is moved.

## A. `PROG-R4` — the four options the user did not take

U5 raised five costed options (`experiments/journal/prog_r4_u5.md` §9); **the user ruled option E on
2026-08-13** and the other four are recorded here.

**The pool constraint on all four:** retired verbatim 2026-08-19 → `WALLS_HISTORY.md` §OPTIONS-A3.

| id | option | cost | why deferred | re-opens if |
|---|---|---|---|---|
| **C** | Carry `m` as an unknown in the residual (= Lane R's **R5**) | own milestone, ≈10 h compute + solver work | Changes the realization, so M1's reproduction no longer compares attempt for attempt. **U5 priced it: 334 anchored in-window candidates, 58.1% of the window, but only 1 in the published band.** Not a band fix — the fix for `\|s\| > 0.9`. | On its own merits as the largest measured hole in the trial space, **not** as a route to the named rows. |

**`E` — THE H-HARD DIAGNOSTIC. LANDED `d0d72b1`, `UNVERIFIED`.** 2 of 16 converged, **0
recovered any named row**. Summary retired 2026-08-19 → `WALLS_HISTORY.md` §OPTIONS-E (its "the
re-ranking is NOT made" went false when I ruled it). `experiments/journal/prog_r4_e.md`.

**`E`'s FIELD ENSEMBLE — QUEUED 2026-08-19, "price do not queue" WITHDRAWN by the user.** 160
attempts, **90.9 core-h, ~11.4 h wall**; closes `E-iv` (a row supplies `(T,s)`, **not a field**).
**Not a grinder** — fixed rows/arms, only the draw varies. `WAVE7_PLAN.md` §B; price
`writeup/prices/FIELD_ENSEMBLE_2026-08-18.md`. **90.9 is an OUTTURN, not a floor** (see `R6`).

**`U4`/`G2` basin radius, and `G1`:** retired verbatim 2026-08-19 → `WALLS_HISTORY.md` §OPTIONS-U4G2.

**⚠ THE `~8×` COST-MODEL OVERRUN IS REFUTED, and the epoch figure that refuted it is itself
corrected.** Full text retired 2026-08-18 under §3j → `WALLS_HISTORY.md` §OPTIONS-A. **Live
consequence: the banked cost model STANDS** (`0.9958` of measured, 0.4% under), so **no option
in this table is re-priced.**

