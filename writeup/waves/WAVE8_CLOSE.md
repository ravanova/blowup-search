# WAVE 8 — LANDINGS AND THE §3i DIRECTION CHECK, ONE BLOCK PER UNIT AS IT RETURNS

§3i is run **every time a unit returns**, not once per wave. The wave is NOT closed while this
sentence is here: `L-JVER` (409), `PB1` (411) and `V-W7` (412) are in flight, and `E-FE` (408) is
a LATE RETURN whose verdict **may not influence this wave's ranking** (ruling `99421dd`).

---

## LANDING: `PB2` (leg 410, `a7ffa1e`) — **GATE `YES`**, and the jaw closes on a DIFFERENT THEOREM from the one the wall cites

### The gate, in its pre-committed wording (`WAVE8_PLAN.md` AMENDMENT 4)

> For the route-4 object as `L5` actually constructs it: **which named theorem excludes it at
> `ṁ ≡ 0`, and does that object satisfy that theorem's stated hypotheses?**

**Answer: `YES`. Tsai 1998 Theorem 2 carries it, and the object satisfies its hypotheses.** This is
AMENDMENT 4's **first** pre-committed reading, which was written down as *"a good outcome and the
likeliest"*: clause (b) STANDS and the `WALLS.md` citation was under-specified.

### What I verified myself, at primary, rather than taking from the unit

| claim | how I checked it | result |
|---|---|---|
| Tsai's hypothesis sentence | `pdftotext -layout Papers/TSAI1998.pdf`, line 236 | **exact**: *"we do not require the weak solution `u` to be a Leray-Hopf weak solution. Our only requirements (apart from self-similarity) are (i) and (ii): the Navier-Stokes equations and the local energy estimates."* |
| Theorem 2's statement | same extraction, lines 131–133 | **exact**: local energy estimates `(1.4)` in `Q₁(0,T)` + form `(1.2)₁` ⟹ `u ≡ 0`. **No `L^q`, no Leray–Hopf, no boundary condition.** |
| Theorem 1's statement | lines 128–129 | `U ∈ L^q(ℝ³)`, **`q ∈ (3,∞]`** ⟹ constant, zero if `q < ∞`. The range is **open at 3**, as leg 364 said. |
| NRŠ's actual reference | Tsai's own bibliography, `[NRS]` | **`Acta Math.` 176 (1996), 283–294** — verbatim. The repository's *`ARMA` 136 (1996) 55–98* is wrong in journal, volume and pages. |
| NRŠ's hypothesis | Tsai's introduction | *"the main result of `[NRS]`"* is for a weak solution **belonging to `L³(ℝ³)`** — exactly `q = 3`, the case Thm 1's range excludes. |
| the log-divergence arithmetic | recomputed: `60.4916579840 × ln 10` | **`139.28719`** against the banked `139.287`, rel. `1.4e-06`. The coefficient and the per-decade increment are consistent. |
| the `1021`-line residual | `wc -l` = **1002**, `grep -c $'\f'` = **19**, `pdfinfo` = **Pages: 19** | `1002 + 19 = 1021` **exactly**. Resolved, not `UNVERIFIED`. |
| hashes | `sha256sum Papers/TSAI1998.pdf` | `6d3182d5…` **matches** the leg-359 pin |
| territory | `git show --stat a7ffa1e` + `git log --all -- <artefacts>` | 6 files at landing, artefact and runner tracked at the earlier checkpoint `c98af80`. **Zero deletions in `WALLS.md`** — the `V-W5`-verified sentence is untouched, as the unit claimed. |
| the evidence suite | re-ran `p2_route_pb2_v1_evidence.py` | **31/31, exit 0** |

**So the substance holds and I am not qualifying it.** `W4` clause (b) is on a **stronger** footing
than its own citation implied: the theorem that carries it is one this repository holds at `FULL
TEXT`, and the source it has failed to obtain four times — NRŠ — **is not load-bearing for this
clause at all**, because the object is not in `L³`.

### Three things the unit did not check, and the first two are mine

**1. `WALLS.md` landed 2,151 BYTES OVER its §3j cap, through a `MERGE GATE: PASS`.** The unit added
25 lines; the file went 32,526 → 34,919 against a cap of 32,768. My `WAVE8_PLAN.md` §6 STANDING
CLAUSES — the block whose stated purpose is *"IN EVERY BRIEF"* — **does not mention §3j**, and the
merge gate has never checked it. **I had measured that cap by hand ninety minutes earlier and then
treated the number as a standing property.** `CORRECTIONS.md` §48. **Remedied by construction**:
`test_headroom.py`, wired into `scripts/merge_gate.sh` as an always-on check, mutation-tested on
four breaks — file over cap, row over 600 chars, LIVE block over cap, LIVE heading missing (which
it fails rather than skipping, because an unchecked cap is not a passed cap). Caps restored by
**verbatim retirement**, five blocks, nothing compacted and nothing deleted.

**2. The evidence script is 0 of 31 `recompute-from-primary`.** It imports `json`, `sys`, `pathlib`
and nothing else; all 31 checks re-read the artefact the unit itself wrote. The brief required
every check to carry its class; **the script carries zero labels and nothing checked that it did.**
But the deeper finding is not the unit's fault: `ORCHESTRATION.md` §6 clause 3 **requires** evidence
scripts to rebuild from the JSON *"without re-running anything"*. §45 called this drift across 32 of
49 scripts. **It is not drift, it is compliance** — the contract specifies a check that cannot fail
on the error class it exists to catch. `CORRECTIONS.md` §49. **The clause is not withdrawn**; it
has a real purpose, and amending an orchestration contract is a user decision, not mine.

**3. The citation defect is in FIVE places, not four.** The fifth is
`experiments/p2_route_l5_v1_driver.py:640` — **the generator of the fourth**. `PB2` searched the
prose and the banked JSON and found every occurrence there, but not the code that writes the JSON.
Driver corrected; the banked JSON left alone under the W3 Q3 ruling, with the divergence declared
in the driver itself. **And `WAVE8_PLAN.md` AMENDMENT 4, which I wrote to scope this very unit,
asserts the wrong citation in its own jaw table.** `CORRECTIONS.md` §47b.

### The quartet, priced not silently dropped

No `BLOG_*`/`TECHNICAL_*` pair (~1 h) and no registered figure (~15 min), following leg 364's
literature-unit precedent. §6's merge-gate rule is not tripped because neither was shipped. **This
is a recorded debt, not a discharge.**

### §3i — THE SEVEN, answered against the RECORD

**1. Did this unit move an `L1→L4` link?** **NO.** It verifies that a hypothesis of a published
theorem is met by a synthetic float64 profile. It proves no theorem. Tier 2. Clay stays ~0.05%.

**2. What did it make FALSE?** (i) That NRŠ is load-bearing for `W4` clause (b) — **it is not; its
`L³` hypothesis is not satisfied by this object.** (ii) That the two theorems in `WALLS.md`'s
clause-(b) sentence are interchangeable — **only Tsai Thm 2 applies as stated.** (iii) That NRŠ is
*ARMA* 136 (1996) 55–98 — **it is `Acta Math.` 176 (1996) 283–294.** (iv) `SOURCES.md` row 1's
`1021`-line residual as an open discrepancy — **resolved arithmetically.** (v) That the §3j caps
were being enforced — **they were not, and now they are.**

**3. Does Lane L still deserve its rank ON WHAT IS MEASURED NOW?** **Yes, and slightly more so.**
The clause the pivot was worried about is not merely still shut; it is shut on a source held at
`FULL TEXT` rather than on one at `SECOND HAND`. **W4's only unbroken clause remains (c)**, which
is Lane T's and deferred. Nothing here promotes another lane.

**4. Is any live claim resting on a source whose own recorded ceiling is undischarged?** **Yes,
and `PB2` narrowed it rather than closing it.** NRŠ 1996 is `UNREACHABLE` at primary for the fourth
independent time — **now with the positive network control leg 364 lacked** (arXiv HTTP 200;
Springer login wall; Euclid stub), so the refusal is the publisher's, not the container's. **Its
price against clause (b) is now ZERO.** It is *not* zero for `solver/dssp_screen.py`, whose `q = 3`
screen still cites Tsai Thm 1 — a range that excludes `q = 3` — and still rests on `SECOND HAND`.
**That is leg 364's finding, unchanged, and it does not touch this clause.** ESŠ remains
`UNREACHABLE` and carries the `α ≤ 1` half of the pin through Seregin.

**5. What is the CHEAPEST unit that could KILL the priority lane, and why is it not next?** Still
`L-JVER`, and it **is** running: if `J(c)` as coded is not the norm it is claimed to be, every
route-4 residual number in the lane is void, including this one's context. `PB2` does not change
that ranking; it is a literature unit and Lane R/paper units never set direction.

**6. If Lane L were dead tomorrow, what would we do instead — and is it cheaper?** Unchanged from
`L6-b`'s answer: Lane T's clause (c), which is deferred by user ruling and is not mine to un-defer.
`PB2` makes the alternative slightly *less* attractive, because it strengthens the case that (a)
and (b) are genuinely shut rather than shut on a citation.

**7. Are we in an audit/instrument loop? Count the last three units by kind.** `L6-b`
(**construction**), `R-prof` (**instrument**), `PB2` (**literature/audit**). One construction in
three, and the wave in flight opens with `L-JVER`, a construction. **Not a loop, but the margin is
thin, and note that this integration itself produced one construction (`test_headroom.py`) and
three corrections — the ratio the §3i q7 clause exists to watch.**

### RE-RANK: **NONE.**

Nothing in `PB2` changes the ordering. `L-JVER` → `L6-e` → `L8` stands. The one thing that would
have forced a re-rank — the second or third pre-committed reading, where clause (b) turned out to
depend on an unmeasured `L^q` membership or could not be determined — **did not fire**, and the
reading that did fire is the one AMENDMENT 4 called the likeliest before the unit ran.

**Ceiling on all of the above: Tier 2, float64, a measurement on `L5`'s synthetic `α = 1` profile.
Route 4 has no banked profile of its own here. No `L1→L4` link moved.**

---

# `V-W7` (leg 412, `aefe590`) and `PB1` (leg 411, `440f28c`) — INTEGRATED 2026-08-19

## `V-W7`: the verifier verified the wave and convicted the Conductor

Wave 7's three units — `R-bank`, `R-prof`, `L6-b` — are **VERIFIED** against their pre-committed
gates. *"Every discrepancy is in the integration, not the units."* **Seven defects ruled against my
own integration work.** I re-checked all seven from primaries rather than accepting them.

| # | `V-W7`'s ruling | my check | verdict |
|---|---|---|---|
| 1 | §46's support sentence FALSE: `seed406` reads `28.6934` at `k=800`, below the claimed `29.57–38.20` | read `l6b_ckpt/seed406.json` trajectory: **`28.693380532819674`**; `seed407` `35.560845905666` | **UPHELD** → §50 item 1 |
| 2 | §46's withdrawal too broad at the low end | 20,000-iter ratios **`4.29257`/`4.32093`**, both above `3.93` | **UPHELD** → §50 item 2 |
| 3 | §46's second clause voids §46's own evidence | the `×4.44`/`×5.47` column IS a cross-budget comparison | **UPHELD** → §50 item 3, rule replaced |
| 4 | `OPTIONS.md:163` never got the §46 patch | confirmed: the withdrawn range stood there as a *verified* `V-W6`/§38 correction, on a capped live surface | **UPHELD** → patched |
| 5 | §3j table at `c6287a2` overstated 2 of 4 rows, byte-identical to wave 6's | already re-measured; `test_headroom.py` now makes the class impossible | **UPHELD, ALREADY REMEDIED** → §50 item 5 |
| 6 | `04f9ff5`/`6ca49a6` swept `L6-b`'s live checkpoints under subjects naming neither | `git show --stat`: both carry `l6b_ckpt/seed406.json`, `seed407.json` | **UPHELD** → §50 item 4, §5b crossing |
| 7 | my repaired `R-prof` sentence "still false", citing `raw_ratio_cpu_clock.min = 2.89873` | that number is **`V-W7`'s own re-run**; the banked JSON has exactly one such key, `min = **3.3721551723168335**` | **UPHELD IN PART** → §50 item 6 |

Item 7 is the one I rule differently, and the difference is the finding: the sentence is **true of
the record and false on re-execution**. A ratio 12% above a threshold on a box the artefact itself
flags `MACHINE_WAS_NOT_QUIET` is not a stable property. Qualified as run-specific, not withdrawn.

`V-W7` also **UPHELD** my §41 row-2 reading as correct *and the narrowest the data supports*,
**UPHELD** §46b as accurate and not over-corrected, and **UPHELD** the verbatim retirements
(`§W4-L6CEIL`, 11/11 lines byte-identical). It found `R-bank`'s `--verify` **cannot fail** — zero
`raise`, `assert` or `sys.exit` in `verify()`. Remedy owed.

## The item that outweighs the other seven: `CORRECTIONS.md` §51

Not a wrong number. **An under-claim, in the record for eleven legs, past the unit, past my
integration, past a clean verifier.** Re-derived by me from the banked JSON:

- `L6`, four rungs of refinement, cap 800: `ρ` `1.6986514108481086 → 1.613811231995397` = **`−4.994561%`**
- `L6-b`, one ×25 budget step, `n_dof` **fixed**: `1.613811231995397 → 1.504851895102804` = **`−6.751678%`**
- **ratio `×1.3518`** — one budget step beat the entire refinement ladder
- `J3` = `1.6218749783288575` needs **`7.2153%`** to fall under `J4@20,000` and invert the ladder;
  **`6.7517%`** is measured one rung up **at more degrees of freedom**. **Margin `0.4636` pp.**

`L6`'s `NO` is **not overturned**. It is left resting on an ordering never measured at a budget where
the ordering means anything. Gate for `L6-e` pre-committed at §51, **both outcomes results**.

## `PB1`: `P1` is KILLED, and it was pre-committed as a good result

Both effects are in print at `FULL TEXT`, `S3`. `P1`'s framing word *silently* is **contradicted by
its own intended bibliography** — CK 2013 counts the duplication in a published table. One control
of twelve did not fire (`pos_topical`, measured 33 against a planted ≥50); disclosed, not re-planted,
nothing in the verdict rests on it. Semantic Scholar throttled on all three of its controls, so its
totals are used for nothing. **No external contact.** Its `manifest_hashes` check caught a
transposition in this leg's own banked MANIFEST that no `re-read-own-artefact` check could see —
§45 demonstrated live, prospectively.

**A paper died to a check that cost half a wave. That is the pivot working exactly as specified.**

---

# THE §3i DIRECTION CHECK — against the RECORD, not the plan

**(1) Did this unit move an L1→L4 link?** **No.** Neither did. `V-W7` is verification; `PB1` killed a
paper. Clay stays **~0.05%**. Tier 2 throughout.

**(2) What did it make FALSE?** A great deal, and most of it mine. §46's support sentence. §46's
rule, which forbade the experiment that resolved it. The `3.93–23.67×` withdrawal at its low end.
`OPTIONS.md:163`'s standing text. The reproducibility of the `R-prof` 3× sentence. `P1`'s novelty
premise, entirely. And — the big one — the *interpretability* of `L6`'s refinement ladder, which is
now known to have been differenced at a cap that dominates it.

**(3) Does Lane L still deserve its rank ON WHAT IS MEASURED NOW?** **Yes, and §51 sharpens rather
than weakens the reason** — but the *grounds* stated at wave 7's close were wrong and are narrowed
here. I recorded Lane L's rank as resting on `L6`/`L6-b` having *measured* that route 4's profile
does not close under refinement. It has not measured that. What it has measured is that the profile
does not close **at the budgets tried**, and that budget is the dominant term. Lane L keeps priority
because it remains the only lane whose units bear directly on a Clay obligation — not because its
refinement result is settled. **It is not settled.**

**(4) Is any live claim resting on a source whose own recorded ceiling is undischarged?** After
`PB2`, no on the literature side: `W4` clause (b) rests on Tsai Thm 2, read at `FULL TEXT`, and the
`UNREACHABLE` NRŠ is not load-bearing. But **yes on the internal side, and §51 is exactly that
shape**: `L6`'s headline rested on a ladder whose own resource ceiling was recorded and never
propagated into the claim built on it.

**(5) What is the CHEAPEST unit that could KILL the priority lane, and why is it not next?**
Changed by this integration. It is now **`L6-e`** — one rung, `J3` to 20,000 iterations, **~20–35
core-h**, cheaper than `L6-b` because `J3` carries fewer dof. It cannot kill the lane, but it can
overturn the lane's own headline on a **0.46 pp** margin, which is the nearest thing available.
**It IS next: queued at the head of wave 9.** `L-JVER` (in flight) remains the deeper kill —
if `J` as coded is not the norm it is documented to be, every ρ above is measuring the wrong thing.

**(6) If Lane L were dead tomorrow, what would we do instead — and is it cheaper?** Lane V, un-held,
with `V5`'s certificate result live. Cheaper per unit, further from the Clay chain. Unchanged by
this wave.

**(7) Are we in an audit/instrument loop? Count the last three units by kind.** `PB2` (audit),
`V-W7` (verifier), `PB1` (audit). **Three of three are instruments. That is a loop, and it is out of
contract to continue it.** The user's pivot authorised paper units as **additional**, and §3g's
composition floor stands. **Wave 9 opens with `L6-e` and `L-JVER`'s follow-on — construction and
measurement — before any drafting.** `P4` drafts only alongside them.

## RE-RANK

**Lane order UNCHANGED: L, V, T(deferred), R(continuous).** The order of units within Lane L
**CHANGES**: `L6-e` enters at the head, ahead of `L8`'s branch rule, on §51's margin.

**And the grounds recorded for answer (3) at wave 7's close are NARROWED, per above.** The
instruments have now run three deep. Wave 9 builds.

---

# `L-JVER` (leg 409) — INTEGRATED 2026-08-19. WAVE 8 IS THE WAVE THAT FOUND THE FLOOR MOVING.

Gate **`NO`**. Escalated to the user mid-run as its own pre-committed reading required, before this
integration existed.

## What I re-derived from primaries, not from the unit's summary

- **`X9` is the measurement that makes this a finding.** The unit's independent operator `W[V]`,
  evaluated on **`L6`'s own quadrature nodes with `L6`'s own weights**, reproduces `J_L6` at
  `1.10e-14`, `2.46e-15`, `5.90e-15`, `1.86e-14` — **including at P3, where the gate fails by 43%.**
  A disagreement that vanishes to machine precision when both codes share a rule, while each rule is
  separately converged, is not a coding error in either program.
- **§51's ladder rungs confirmed:** branch B `1.698651411`, `1.675613729`, `1.621874978`,
  `1.613811232`, with `nq_r` = 36, 48, 48, 60, 72.
- **Going further than the unit:** the divergence is present **at the minimiser** — `+6.226e-5`,
  `+6.246e-5`, `+6.212e-5` per decade over `r_max` `1e6 → 1e14`, three bands inside 1%. `P1`'s
  `1.00e-4` PASS is not evidence of convergence.
- **The sign is POSITIVE**, which is why every gate answer survives: less truncation ⟹ larger `ρ` ⟹
  further from `ρ < 1.45`. **`L6`'s `NO`, `L6-b`'s `NO` and `L5`'s `NO` all stand. Their numbers do
  not.**
- **§52 does NOT subsume §51**: divergence coefficient `6.22e-5`/decade against a last ladder step of
  `8.06e-3` — **×130**. Two independent defects in the same four numbers.
- **`W4` clause (b) is clear**, checked rather than assumed: `c_mod`, `869.288`, `J(`, `curl F`,
  `L1_t` all absent from `writeup/data/p2_route_pb2_v1.json`.

**Recorded as in flight, not as verified:** my re-run of `p2_route_ljver_v1_evidence.py` was still
executing when this was committed. It is not cited as evidence here.

**UPDATE, same day.** That re-run **did not complete**: it was killed by my own `timeout 900` at
SIGTERM (exit 143), against a unit-reported cost of 501 s on a quieter machine — `E-FE`'s shards are
holding cores. **This is a timeout of mine, not a check failure, and it is evidence of nothing in
either direction.** Re-launched without a timeout. Until it returns, every §53 claim rests on the
banked JSON fields I read directly, which is where they were derived from in the first place — no
§53 finding depends on the evidence suite passing. The unit reports 12/12
`recompute-from-primary`, 0 `re-read-own-artefact` — the first suite in this record to be entirely
of the class §45 says we lack.

## A defect of mine, found while landing this and recorded rather than quietly fixed

The §51 block I landed two commits ago went into **`WALLS.md`'s W7 — Compute** section, not W4.
`t.find("\n**⚠", i+5)` walked past W5 and W6 because neither carries a ⚠ block, and §52's block
then followed §51 into the wrong section. Both moved to W4; W7 verified intact. **§37's rule says
retire by slicing between ASSERTED line indices, and when an edit must search, ASSERT THE MATCH
COUNT — I asserted the count and not the neighbourhood, so the edit was well-formed and landed in
the wrong wall.** → `CORRECTIONS.md`, next revision.

## §3i, re-run because a unit returned

**(1) L1→L4?** No. **(2) What did it make FALSE?** That any `J` in this record is a value of the
functional it is named for. **(3) Does Lane L still deserve its rank?** **Yes — and this is the
strongest grounds it has had.** A lane that discovers its own measuring instrument is divergent, and
then measures the sign well enough to show its conclusions survive, is a lane doing the work.
**(4) Undischarged ceiling under a live claim?** `L5`'s `c_mod` — flagged, sweep owed, not
adjudicated. **(5) Cheapest unit that could kill the lane?** Unchanged in identity, **rewritten in
gate**: `L6-e` v2, at matched truncation (§53). **(6) If Lane L died?** Lane V. Unchanged.
**(7) Audit/instrument loop?** The last four are `PB2`, `V-W7`, `PB1`, **`L-JVER` — a CONSTRUCTION
unit, on object, and it is the one that found the floor.** The loop broke itself.

## RE-RANK

**Lane order UNCHANGED. Within Lane L: `L6-e` v2 at the head, then the `L5` `c_mod` sweep to
`1e8` (cheap, and it is the last unadjudicated flag from §53), then `L8`'s branch rule.**
`L7` and `L4` are pushed further out by §52 and their rows are retired accordingly.

**Wave 8 closes: `PB2` YES, `PB1` YES (`P1` killed), `V-W7` VERIFIED with seven against me,
`L-JVER` NO with the largest structural finding in the record. `E-FE` outstanding as a late return
and MAY NOT influence this ranking (ruling `99421dd`).**
