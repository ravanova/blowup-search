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
