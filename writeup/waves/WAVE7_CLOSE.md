# WAVE 7 — INTEGRATION RECORD

One section per unit, written when the unit lands, not at the wave's end. Each section is the
Conductor's **independent** audit against the gate wording committed in `WAVE7_PLAN.md` **before**
dispatch, followed by §3i's seven questions answered against the RECORD.

---

## `R-prof` — leg 405, landed by the unit at `1f89ceb`. GATE ANSWER: **NO** (two-sided; a NO was pre-committed as a real and useful negative).

**Artefact:** `writeup/data/p2_r_prof_v1.json`.

### What the gate asked, and what came back

| clause | gate wording (pre-committed) | answer |
|---|---|---|
| (i) | a breakdown of one step that **sums to 100%** | 15 rows, sum **exactly 100.0**; `79.1%` of a clean step is transforms |
| (ii) | the **fixed-overhead fraction** by a size sweep | **0.596** over `N = 4..512`; cross-check 0.646 TRUSTED; a third OLS estimator 1.858 marked `TRUSTED: false` **by the unit itself** |
| (iii) | **within 3× of a named reference — YES or NO** | **NO.** `4.341×` (cpu clock, median of 60 rounds); wall median `4.212`; both clocks agree in sign and rough size |

### The independent audit (what I checked myself, not from the report)

- **Territory.** `git` shows the unit touched only its own artefact and scripts. `object_MODIFIED_BY_THIS_UNIT: false` is true: `object_sha256 = 282b6183…8ed47` **matches the live `solver/kolmogorov2d_nkbasin.py`** byte for byte. The profiler did not edit the thing it profiled.
- **Self-hash.** `sha256_of_artefact_without_this_field = 9d160dcd…5654c` **recomputes to a MATCH** under the artefact's own documented recipe (`json.dumps(obj, indent=2, sort_keys=True, default=float)`). Both script hashes match the live files.
- **(i) sums.** The 15-row table sums to **exactly** 100.0. `UNATTRIBUTED_python_frames` is 19.597% and is *named as unattributed* rather than silently distributed over the named rows — the honest form.
- **(ii).** The 0.596 rests on a real sweep, and the disagreeing third estimator is banked with `TRUSTED: false` **and a reason**, not dropped.
- **Corroboration outside the unit.** Per-step × 1934 steps = **2.0743 s** against `U3`'s banked Jacobian-action cost of **2.3673 s** — a ratio of 0.876. The record's cost *model* is coherent to 12.4%. This is the check the unit could not have faked, because `U3`'s number was banked legs earlier.
- **Disclosure of a failure.** `load_conditions.MACHINE_WAS_NOT_QUIET = true`, and the **positive control FAILED** (busy-loop ratio 7.15 against an expected ~4). Both are in the artefact. A unit that hides a failed control is worth nothing; this one printed it.
- **The remedy is priced, not landed.** Pre-planned FFTW3 transforms, 3.41×. The batched-numpy variant V1 is **bitwise identical** (`rel_sup_err` 0.0 at 1 and at 200 steps) for 1.618×; V2/V3 differ at 6.44e-17. The unit did **not** land it, and said why: a transform change perturbs every banked orbit at the last bit, *which is precisely the `R4` problem*.

### CONDUCTOR LANDING FINDING — one over-generalisation, and it is mine to state

The unit's summary says the worst of 60 rounds is 3.372, **so every round exceeds 3×**. That holds on
the **cpu clock only**. `raw_ratio_wall_clock.min = 1.9975010694418314` — below 3. The artefact
itself is honest about this: it banks the number as `worst_case_for_the_NO` and argues in
`note_on_the_worst_case` that the excursion is machine load, not code. The defect is that the
*prose* generalised one clock's statement to all rounds.

**The `NO` survives comfortably**: medians 4.34 (cpu) / 4.21 (wall), p10 3.58 / 3.45,
work-normalised 4.14. The verdict does not change. The wording does, and it is recorded here and in
`STATE.md`, `WALLS.md` W7 and `OPTIONS.md` `R6` rather than smoothed over.

### The pre-committed reading of a NO, applied

`WAVE7_PLAN.md` §C: *"report the factor and the single change that recovers most of it. Do NOT
rewrite the solver in the same unit: a stepper change invalidates every banked comparison, which is
precisely the `R4` problem, and it needs its own unit and its own equivalence check."* Done, and
obeyed by the unit. Nothing about the solver changed in this leg.

---

## §3i — THE DIRECTION CHECK for `R-prof`

**1. Did this unit move an `L1→L4` link?** **No.** Not one. It measured the cost of walking the
existing chain, not the chain. `PROG-R4` is Lane R; Lane R never sets direction.

**2. What did it make FALSE?**
- The implicit belief that `95.389 s/epoch` was a floor set by the physics. It is not: **~60% of a
  step is size-independent overhead**, and 79.1% is transforms, so the figure is set by the
  *implementation*.
- "We are roughly competitive with published codes." We are **4.3× off** a named reference on the
  same problem.
- My own restatement of the unit's claim that every round exceeds 3× — false on the wall clock
  (1.9975).
- It also makes false the cheap escape "the record's costings are guesses": they corroborate an
  independent banked measurement to 12.4%.

**3. Does Lane R still deserve its rank ON WHAT IS MEASURED NOW?** **Yes — unchanged, at the
bottom, continuous.** Lane R is explicitly the lane that never sets a wave's direction, and this
result is the strongest possible illustration of why: it is the largest single efficiency finding
Lane R has produced, and it moves **nothing** on the Clay chain. Within Lane R the internal ranking
*does* change: the FFTW3 transform swap is now the cheapest **measured** lever in the lane
(3.41× for one unit), where before it was an unpriced guess. It goes **behind** `R4`, because `R4`
is a *validity* fix and this is a *throughput* fix, and because both touch the same last bits of
every banked orbit — so they should be sequenced, `R4` first, in one equivalence-checked unit.

**4. Is any live claim resting on a source whose own recorded ceiling is undischarged?** Yes, and
none of them are this unit's. The two live ones remain: **W4 clause (b)** is recorded SHUT and
VERIFIED on two theorems this repository has never opened at primary (`PB2`, wave 8), and `L5`'s
`c_mod = 869.288` is a synthetic stand-in's constant, basis-dependent by 1.476×. `R-prof` adds no
new one: its reference implementation was named and its citation discharged **before** dispatch, per
§3k rule 2.

**5. What is the CHEAPEST unit that could KILL the priority lane, and why is it not next?** Lane L
dies if route 4's residual functional `J(c)` is not, as coded, the `L^{3/2}` norm of the curl of the
profile residual. `V-W6` prices an independent re-implementation of `W[V]` in a different basis at
~1 unit-week + 1–5 core-h. **Every route-4 residual number in the record is downstream of that one
function**, and the only internal evidence is a selftest comparing two of the unit's own
implementations. It is not next only because wave 8's four slots are already committed
(`L8` ‖ `PB2` ‖ `PB1` ‖ `V-W7`) and because `L6-b` is still running against the same object; it is
hereby **the leading candidate for wave 9's Clay-chain slot**, ahead of `L7`.

**6. If Lane L were dead tomorrow, what would we do instead — and is it cheaper?** Lane V (the
viscous rung) and W4 clause (c), the torus, which is Lane T's and currently deferred by ruling. Both
are cheaper per unit than Lane L and neither touches `CLAY_OBLIGATIONS.md` §6(i)/§6(ii), which is
the whole reason Lane L is priority. Cheaper is not the criterion; being on the Clay path is.

**7. Are we in an audit/instrument loop? Count the last three units by kind.** The last three
units to RETURN are `L6` (construction, wave 6), `V5` (audit, wave 6) and `R-prof` (instrument), with
`V-W6` (verifier) returning alongside and `L6-b` (construction) still running. That is a genuine
mix, and wave 7 carried `L6-b` as its Clay-chain unit, so the §3g composition floor was met.
**But the warning is live**: wave 8 as planned carries `PB1` and `PB2` (both source/instrument
checks) plus `V-W7` (verifier) against a single construction slot (`L8`). That is 3:1 the wrong way.
It is accepted this once **only because the user's 2026-08-19 directive ordered the paper pivot and
explicitly kept the composition floor**, and it is recorded here so that wave 9 must be
construction-heavy or the loop is real.

**Tier 2 is never a proof. No link moved. Clay ~0.05%.**

---

## `V-W6` — leg 407, landed by the unit at `c7f242c` (+ `280f421`, `1844b46`). VERDICTS: `V5` **VERIFIED**, `V-W5` **VERIFIED**, `L6` **VERIFIED-WITH-QUALIFICATION**.

**Artefact:** `writeup/data/p2_verify_wave6_v1.json`. I planned wave 6, so I could not verify it;
this unit did, and it was briefed to scrutinise my own landing audit as well. It did that too.

### The independent audit of the verifier

- **Self-hash** `5834da0a4ff30a3c` **recomputes to a MATCH** under the artefact's own stated rule.
- **Territory**: three files, all `A` (`writeup/data/p2_verify_wave6_v1.json`,
  `experiments/p2_verify_wave6_v1_evidence.py`, `experiments/journal/leg_407.md`). Nothing else in
  the tree was touched by any of its three commits. `banked_artefacts_edited: 0`,
  `defects_repaired: 0` — a verifier that repairs is no longer a verifier, and this one did not.
- **Evidence re-run by me**: `65 checks, 0 failures`, exit 0. `--deep` was **executed**, not merely
  offered: 68 checks, and all three unit evidence scripts re-run as subprocesses, all exit 0.
- **I re-derived its central corrections myself from `writeup/data/p2_route_l6_profile_v1.json`**,
  not from its word: the per-rung minimum is the `continuation` start at every rung above the
  coarsest on **both** branches; branch-B seed ratios 3.93–4.02 / 8.04–11.35 / 10.08–11.29 /
  18.32–23.67; branch A never above 5.95; `scale_invariant_grad` at the banked minimiser **153.22**
  with the ladder 23.05 → 24.06 → 60.11 → 153.22 on B and 1.16 → 1.75 → 3.11 → 16.12 on A; the main
  ladder is **58 starts at `nit = 800`** and the axis ladders are **75 at 250**, 133 total, every one
  `hit_maxiter = true`, `status = 1`. Every one of its numbers reproduced.
- **It states its own ceiling**: it verifies **arithmetic, provenance and gate-compliance**, not
  science. That is the correct ceiling for a verifier and it is banked, not implied.

### The ruling on my own landing audit — accepted in full

**Upheld:** the one-start finding, independently confirmed, and it is what forced the re-rank to
`L6-b`. **Overstated three times, wrong once conservatively, understated twice.** All seven items,
with my own re-derivation of each, are written to **`writeup/CORRECTIONS.md` §38**. Nothing is
smoothed: the "10–24×" band, "monotonically worse", "all 133 at 800" and "1.6 against a
unit-normalised field" are corrected in `WALLS.md`, `STATE.md` and `OPTIONS.md` in this commit.

### `D-VW6-7`, REPAIRED

`requirements.txt` declared scipy "intentionally NOT required" while `experiments/p2_route_l6_v1.py`
imports `scipy.optimize.minimize` and `scipy.special.lpmv`, so on a clean checkout `L6`'s evidence
script dies with an uncaught `ImportError` and reports **zero** checks. Verified by me at the source
lines (60–61). **Repaired in this commit.** The other ten defects stay open, unrepaired, in the
verifier's artefact — that is the record's job, not a verifier's.

---

## §3i — THE DIRECTION CHECK for `V-W6`, AND A RE-RANK

**1. Did this unit move an `L1→L4` link?** **No.** A verification cannot. It confirms that wave 6
moved none either.

**2. What did it make FALSE?**
- `L6`'s bolded §8.2 claim — that the stall is *"a fact about the construction, not the stopping
  point"* — **has no surviving support.** Its only control, the cap sweep, is a post-hoc truncation
  of the same full-budget runs, warm-started from below.
- The belief that the banked minimiser is a minimiser in any meaningful sense. **All 133 starts
  exited `status = 1`; not one converged by gradient or by `ftol`**, and the distance from
  stationarity **grows** with `n_dof`.
- Three of my own supporting numbers, and one of my inferences: `L7` is blocked **harder**, at 7.58
  on the genuinely unit-normalised branch, not 1.6.
- That a clean checkout can reproduce `L6`. It could not, until this commit.

**3. Does Lane L still deserve its rank ON WHAT IS MEASURED NOW?** **Yes as a lane — it is still the
only lane touching `CLAY_OBLIGATIONS.md` §6(i)/§6(ii) — but the ORDER INSIDE IT CHANGES, and that is
this integration's real output.** See q5.

**4. Is any live claim resting on a source whose own recorded ceiling is undischarged?** Yes, and
`V-W6` adds a new one that is worse than the source ceilings: **not a source, but a function.**
`D-VW6-5` re-flags NRŠ 1996 / Tsai 1998 held SECOND HAND under branch-B selection (already queued as
`L7-src`, absorbed into `PB2`). `D-VW6-6` records that `SOURCES.md` has no row and no DEPTH for
Byrd–Lu–Nocedal–Zhu 1995 (`L6`'s `C1`-discharging apparatus) or Chandrasekhar (its trial space) —
**that is the landing commit's gap, i.e. mine, and it is owed.**

**5. What is the CHEAPEST unit that could KILL the priority lane, and why is it not next? — IT IS
NOW NEXT. RE-RANKED IN THIS COMMIT.** `V-W6`'s single most important *unchecked* item: whether
`J(c)` **as coded** is actually the `L^{3/2}` norm of the curl of route 4's profile residual. The
only internal evidence is selftest `T_D` at `1.22e-4`, which compares **two of the unit's own
implementations**. **Every route-4 residual number in the record is downstream of that one
function** — `L5`'s `c_mod`, `L6`'s `ρ = 1.6138`, and `L6-b`'s answer whichever way it lands. Price:
an independent re-implementation of `W[V]` in a different basis, ~1 unit-week + 1–5 core-h.

**The re-rank.** Wave 8's Clay-chain slot was pre-committed as `L8`, a branch decision keyed to
`L6-b` (`WAVE8_PLAN.md` §1). It is **replaced by `L-JVER`**, the independent re-implementation, and
`L8`'s branch rule is **deferred verbatim to wave 9**, unchanged and still keyed to `L6-b`'s banked
answer, which does not expire. Two reasons, and the second is the one that decides it:

1. `L8` cannot be *chosen* until `L6-b` returns anyway, and `L6-b` is still running.
2. **Either branch of `L8` spends a full wave refining a functional nobody outside its own author
   has ever computed.** If `J(c)` is not the norm it is documented to be, `L6-c`/`L6-d` measure
   nothing, `L6-b` measures nothing, and `L5`'s clause-(b) closure is standing on it. Buying the
   check first is strictly cheaper than buying it after another ladder.

This satisfies the §3g composition floor: `L-JVER` is a Lane L unit attacking W4/W5 directly, and it
is a **construction** unit, not an instrument — which also repairs wave 8's 3:1 instrument skew
flagged in `R-prof`'s q7 above. The amendment is written into `WAVE8_PLAN.md` **before** dispatch,
with its gate, as §3g requires.

**6. If Lane L were dead tomorrow, what would we do instead — and is it cheaper?** Unchanged from
`R-prof`'s answer: Lane V, and W4 clause (c) on the torus, which is Lane T's and deferred by ruling.
Both cheaper per unit, neither on the §6 path. **Note the sharpening**: `L-JVER` is precisely the
unit that could *cause* that question to become live rather than hypothetical, which is why it is
worth a full wave slot.

**7. Are we in an audit/instrument loop?** The last three returned units are `R-prof` (instrument),
`V-W6` (verifier) and — still running — `L6-b` (construction). Two of three are non-construction.
**The re-rank in q5 is also the answer to q7**: wave 8 now opens with a construction unit
(`L-JVER`), per §3f rule 3, and carries the verifier last.

**Tier 2 is never a proof. No link moved. Clay ~0.05%.**
