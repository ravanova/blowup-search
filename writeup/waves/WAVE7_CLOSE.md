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


---

## `R-bank` — leg 404, landed by the unit at `8019c35`. GATE ANSWER: **YES on all three.**

### What the gate asked, and what came back

| clause | question (WAVE7_PLAN.md §A) | answer | the number |
|---|---|---|---|
| (i) | is every banked field bit-identical to what `u2_m2_dns_recurrence.regenerate` produces for the same snapshot index? | **YES** | **160 / 160**, zero mismatches, SHA-256 over the IEEE-754 float64 C-order buffer. Run **both ways** — one snapshot per call (the shard case) **160/160**, and all 160 in one call (the case `E` actually ran) **160/160**, because `regenerate`'s block-walking makes batch context a live confound. |
| (ii) | do `E`'s 16 originals match `E`'s banked ledger? | **YES** | **16 / 16**, `ulp_gap 0`, and separately **16/16** against `writeup/data/p2_prog_r4_e_v1.json`. |
| (iii) | does one of `E`'s attempts reproduce with the DNS artefacts absent? | **YES** | attempt 15 (`UPO9`, arm Q): **16/16 scalar fields** and **12/12 per-Newton-iteration ledger entries** byte-equal. `converged`, `‖R‖ = 2.0552353500244844e-10`. |

`self_hash 3b592e3c21bf7a42`. Cost **1.06 core-h** against a briefed ~10⁰ core-h; `UNDER_RESOURCED false`.

### The independent audit — what I checked myself, not from the report

1. **`self_hash` RECOMPUTED from the committed blob** (`git show 8019c35:writeup/data/p2_r_bank_v1.json`), under the recipe the file states: **`3b592e3c21bf7a42`, MATCH.**
2. **The seedbank is genuinely tracked.** All three files appear in `git ls-files`; `git check-ignore -v` returns nothing for `seed_fields.npy`; `git ls-tree -l 8019c35` shows the blobs at **737,408 / 123,799 / 3,571 B**. This was the whole point of the unit and it is the one thing a report could most easily assert falsely.
3. **Manifest ↔ `.npy` consistency, all 160.** I hashed every slice of `seed_fields.npy` myself against `manifest.json`'s per-field `sha256`: **160/160 match, 0 mismatches.** Arithmetic closes: 4,608 B × 160 = 737,280 + 128 B npy header = **737,408 B**. Shape `(160, 24, 24)` float64, C-contiguous. 8 rows × 2 arms × 10 `field_index` = 160; exactly **16** rows carry `is_E_original`, and they are exactly the `field_index == 0` entries.
4. **`regenerate` re-run by me, not by the unit.** I called `r_bank_build._regenerate` on a 4-field sample — one `is_E_original` and three not, across three rows and both arms (`UPO37/S fi=0`, `UPO20/Q fi=1`, `UPO17/S fi=5`, `UPO17/Q fi=7`). **4/4 bitwise equal, `maxabsdiff = 0.000e+00`.** That is a 2.5% independent sample of gate (i), and it is corroboration of the unit's own result, not a substitute for it.
5. **Gate (iii)'s tree audited in place.** `scratchpad/nodns` still exists. `u2_dns_ckpt.npy` and `u2_dns_feat.f32` are **both absent**; its seedbank is byte-identical to the tracked one (same SHA-256). I read the call graph: `demo_attempt` → `load_seed` → the bank; nothing on that path opens the checkpoint, the feature file, or `e_hhard_converged_orbits.npz` — which matters, because that `.npz` *is* present in the tree and seeding from it would have been circular. It is not read.
6. **Disclosure the unit did not make.** Three DNS *metadata* files **are** present in the no-DNS tree — `u2_dns_meta.json` (1,211 B), `u2_dns_progress.txt` (62 B), `u2_dns_stdout.log` (100 B). They carry no field data and `regenerate` cannot use them, and the flag `dns_artefacts_absent_in_this_tree` is *defined in code* as exactly the two field-carrying files, with `demo15.log` printing both as `present: False`. The claim is sound; the **wording is looser than the check**, and a referee would say so. Recorded, not smoothed.

### CONDUCTOR LANDING FINDING — the `~1.2 GB` defect is sharper than "wrong by 4.5×", and it is mine

`R-bank` found `D1`: `experiments/programme_r4/.gitignore`'s header calls the DNS artefacts **"~1.2 GB"**, and the measurement is **268,864,256 B = 268.9 MB**. It correctly declined to rewrite the banked line (W3 ruling Q3 — a banked datum gets a correction *beside* it) and correctly left my files alone.

**The root cause is not an arithmetic slip.** `experiments/programme_r4/u2_m2_dns_recurrence.py:127-136` says, in `U2`'s own words, that storing all 400,000 snapshots as float32 *"would need ~1.2 GB and this machine has 1.5 GB free"*, and that the archive actually written costs *"~280 MB instead of ~1.2 GB"*. **`1.2 GB` is the size of the archive `U2` decided NOT to write.** The `.gitignore` header then attached that counterfactual to the files it actually lists. `U2`'s own `~280 MB` estimate agrees with the measurement to **4%** — so the repository had the right number all along and copied the wrong one.

It then propagated: into `WAVE7_PLAN.md` §A and `OPTIONS.md`'s `R7` row — **both mine** — and onward into `r_bank_build.py`, `u5_reduce_library.py`, `seedbank/manifest.json` and `reports/ORCH_STATE.md`'s superseded block. `OPTIONS.md` is a live ranking document and is corrected in this commit. `WAVE7_PLAN.md` is a committed pre-dispatch record and gets a correction appended, **not an edit**. The superseded ORCH block and the banked artefacts are left verbatim. `CORRECTIONS.md §39`.

**A second process finding, smaller and mine.** Three `--verify` runs produced three different `self_hash`es (`183cb1…`, `ff3b62…`, `3b592e…`). **None is a reproducibility failure** — the document gained its `cost_and_shortfall` / `ceilings` / `defects_found` blocks between runs, and then `self_hash_recipe` was added to `VOLATILE` to remove a self-reference that made the hash chase itself. The final value is a fixed point and I verified it. The cost of learning it was ~19 min of a 19-min verify on a box at load 15, which is why I intervened and told the unit to stop re-verifying and land; it then used `--rehash` in seconds. The lesson is now in `E-FE`'s brief as a named instruction.

### The pre-committed reading, applied

> *"anything short of 160/160 bit-identical means the ensemble DOES NOT LAUNCH from that artefact; the shortfall is a finding about the re-integration path's determinism, reported and not patched around."*

**160/160 fired.** Nothing was loosened — and the unit's own note on that is the right one: the comparator is a SHA-256 over a float64 buffer and **contains no tolerance to loosen**. `E-FE`'s launch condition is therefore **DISCHARGED**, and `E-FE` was dispatched at 6 shards immediately after this audit.

### What this does NOT license

No `L1→L4` link moved. **No wall moved** — and I am not writing an entry into `WALLS.md` for this, because `W7` is the claim that *the search is too big*, and taking 27.5 core-h off one 90.9 core-h ensemble is an operational fact about this box, not a statement about the object. **Scale is not evidence**: 737 KB of committed fields is a portability fact. 160 fields is not 10× more evidence than 16 — it is 10× more **draws**. `E`'s 0-of-16, `E-iv`'s realization gap and the `N = 24` limit are all untouched, and **no seed supply was added**. **Tier 2 is never a proof. Clay ~0.05%.**

## §3i THE DIRECTION CHECK on `R-bank`

**q1 — Did this unit move an `L1→L4` link?** **No.** It is Lane R infrastructure and says so itself. What it moved is a *prerequisite*: a shard no longer needs a 3.44 h DNS it cannot fetch, measured, not argued.

**q2 — What did it make FALSE?** (a) That the DNS artefacts are ~1.2 GB — they are 268.9 MB, and the figure was a counterfactual all along. (b) That a seed cannot be built without the checkpoint — gate (iii) reproduced an attempt bit for bit with both field-carrying artefacts absent. (c) That the seedbank was safely ignored — the `.gitignore` line was the blocker, and it is now a tracked 737,408 B blob that cannot die with a container, which the DNS checkpoints have done **twice**.

**q3 — Does its lane still deserve its rank on what is measured NOW?** Lane R is continuous and **never sets a wave's direction**; that is unchanged and `R-bank` does not change it. Its rank *within* Lane R was "runs first, because it unblocks the ensemble", and it delivered exactly that at 1.06 core-h.

**q4 — Is any live claim resting on a source whose own recorded ceiling is undischarged?** **YES, two.** (a) The big one is not this unit's: **`W4` clause (b) is recorded SHUT and VERIFIED on Chae–Wolf Thm 1.1 / Rmk 1.2 and the ESŠ step, and this repository has never opened either.** That is `PB2`, wave 8, and the user directive requires any failure there to come to them immediately rather than at a wave's end. (b) Within this unit: ceiling **C2** — gate (i) establishes the bank is what `regenerate` produces *here, on this CPU, under this numpy/FFT build*. **The artefact is now the DEFINITION of the seed, not a cache of a machine-independent one.** `E-FE`'s entire 160 attempts rest on that, cross-machine agreement is unpriced, and I have written C2 into `E-FE`'s brief rather than letting it be rediscovered.

**q5 — What is the CHEAPEST unit that could KILL the priority lane, and why is it not next?** Unchanged from the `V-W6` re-rank: **`L-JVER`**, because every route-4 residual number is downstream of one `J` whose only evidence is a selftest comparing two of `L6`'s own implementations. **It IS next** — slot 1 of wave 8, ahead of `L8`.

**q6 — If Lane L were dead tomorrow, what would we do instead, and is it cheaper?** Lane V (the `L5` norm) and Lane T (the torus — `W4` clause (c), **UNTESTED, NOT CLOSED**). Lane T is cheaper per unit and is *still* held on a ban-wording question that is on the user's desk, not mine to rule. That has not changed and I am not treating it as changed.

**q7 — Are we in an audit/instrument loop? Count the last three units by kind.** `R-prof` (instrument) → `V-W6` (verifier) → `R-bank` (infrastructure). **Three non-construction units in a row, and I am flagging it rather than explaining it away.** The mitigation was already committed before this landing, not invented for it: `L6-b` (construction) has been live throughout and is 3,900/20,000 iterations in, and wave 8 **opens** with `L-JVER` (construction) per §3f rule 3. The count is the count; the correction is in place.

### Dispatch record — `E-FE`, leg 408, 6 shards

Launched immediately on the discharged condition. Not a re-decision: the shard count is **6, not the price sheet's 8**, decided on a measurement (12 cores; `L6-b` holding ~5; `R-prof`'s banked `MACHINE_WAS_NOT_QUIET = true` with a positive control that failed at 7.15× against an expected ~4×). **Consequence stated up front: ~15.2 h wall instead of ~11.4; core-hours unchanged at ~91.** The brief carries `R-bank`'s C2 and C4 as inherited ceilings, the row-major draw order as a **declared choice** so the null names its own realization (lesson 91), the tracked-partials requirement from the 2026-08-14 loss, and the `self_hash` fixed-point lesson learned above.

---

## CONDUCTOR MEASUREMENT 2026-08-19 02:35 — WHAT `E-FE` COST `L6-b`, MEASURED FROM THE OUTSIDE

My `E-FE` brief (staged, now consumed) told the unit to report *"shards used, wall clock, core-hours,
and the load average at start and end."* That instruction has a hole in it which I am recording rather
than repairing after the fact: **a unit can report the load it ran under, but it cannot report the cost
it imposed on the job it was sharing the box with.** Only the CONDUCTOR is positioned to see that, and
only while both are still running. So I measured it.

Source: `experiments/route4/l6b_ckpt/banked_J4_minimiser.json`, field
`trajectory_k_sec_J_ginf_gscaled` — `L6-b`'s own in-run checkpoint, written by the running job, read by
me without touching it. Rate over rolling 250-iteration windows, wall-clock stamped from the checkpoint
mtime minus its `seconds` field:

| iterations | wall | rate |
|---|---|---|
| 3,800 – 4,050 | 02:10 | 0.988 it/s |
| 4,050 – 4,300 | 02:13 | 1.143 it/s |
| 4,300 – 4,550 | 02:17 | 1.121 it/s |
| 4,550 – 4,800 | 02:21 | **1.178 it/s** |
| 4,800 – 5,050 | 02:26 | **0.712 it/s** |
| 5,050 – 5,300 | 02:32 | 0.701 it/s |

**The break is between 02:21 and 02:26, and it is a 40% loss of throughput** (1.178 → 0.701 it/s).
`E-FE`'s six shards came up in that window. `uptime` at 02:31 read `16.94` on a 12-core box.

**Three things this fixes in the record, and one it does not.**

1. **The schedule.** `L6-b` was projected to return ~07:15 at its then-current 0.905 it/s. At 0.701 it/s
   the remaining 14,700 iterations take **5.8 h**, so the honest projection is **~08:20**, and it stays
   contended for `E-FE`'s whole ~15 h rather than recovering. **This is a projection, not a measurement,
   and it is conditional on `E-FE` holding six shards** — which my brief forbade it from changing.
2. **My own price sheet, corrected by a measurement.** I priced the box at ~11 of 12 busy with six
   shards. It ran at ~17. I have already recorded that `L6-b` holds 6 cores and not the ~5 I assumed;
   this is the *other half* of the same error, and it lands on the throughput of the job I under-counted.
3. **A defect in the brief wording, stated as a defect.** *"Report the load average at start and end"*
   is a self-report of the weather, not of the unit's own footprint. **A concurrency brief should ask
   for the delta it imposes on a named co-tenant, not the ambient load** — and where no co-tenant exists
   to measure, it should say so. Carried to `CORRECTIONS.md` as a brief-wording defect, not a result.

**What this does NOT license.** It is not a reason to lower `E-FE`'s shard count mid-run — that was
pre-committed against, and a changing shard count destroys the per-attempt cost figure the ensemble
owes the record. It is not a reason to touch `L6-b`. And **it says nothing whatever about either unit's
gate**: it is a fact about this machine on this night, not about Route 4, W4, or the field ensemble.
`E-FE`'s own start/end load figures stay in its artefact unedited; this sits BESIDE them (W3 ruling Q3).

## CONDUCTOR PRE-REGISTRATION 2026-08-19 03:20 — A DEFECT IN `L6-b`'s OWN `NO` BRANCH, RECORDED BEFORE THE NUMBER EXISTS

**Timestamp discipline first.** `L6-b` is at 7,000 of 20,000 iterations. The gate number does not
exist yet and neither I nor the unit can know it. Everything below is therefore a statement about
the gate's WORDING, not about its outcome, and it is committed now so that it cannot later be read
as a reaction to a result I did not like. **I wrote that wording. This is a defect in my own
pre-committed reading.**

### 1. The fact that provokes it: nothing in `L6` ever converged, and this is exhaustive

Read out of `writeup/data/p2_route_l6_profile_v1.json` directly, all 58 non-angular start-records
across branches A and B, every rung:

| | count | share |
|---|---|---|
| start-records | 58 | |
| **hit the 800-iteration cap (`nit == 800`)** | **58** | **100%** |
| not a critical point at `‖x‖‖∇J‖/|J| ≥ 1` | 56 | 97% |
| critical by that threshold | 2 | branch A rung 0, `seed403` (0.888) and `seed405` (0.965) — the COARSEST rung only |

**Not one record in `L6`'s ladder terminated on a convergence criterion.** Every single one stopped
because it ran out of iterations. `L6`'s §8.4 conceded the headline number "is not the infimum";
the stronger statement the artefact supports is that **no rung of either branch, at any resolution,
ever produced a stationary point at all.** The ladder compared STOPPING POINTS.

### 2. The rank inversion, and which measure governs — this must be disclosed, not chosen

Branch B, top rung, the rung that produced `ρ = 1.6138`:

| start | `nit` | `max_abs_grad` | `scale_invariant_grad` |
|---|---|---|---|
| `seed401` | 800 | 2500.7 | 11.90 |
| `seed402` | 800 | 2473.1 | 16.58 |
| `seed403` | 800 | 1446.1 | 9.67 |
| `seed404` | 800 | 792.0 | 4.65 |
| `seed405` | 800 | 1265.2 | 5.54 |
| **`continuation`** (the banked minimiser) | 800 | **252.2 — the SMALLEST** | **153.22 — the LARGEST** |

**The two gradient columns rank the six starts in opposite orders, and a reader who takes the raw
one reaches the opposite conclusion.** `max_abs_grad = 252` says the banked minimiser is the closest
to stationary of the six; `scale_invariant_grad = 153` says it is by far the furthest.

**The scale-invariant column governs, and the reason is in this repository's own record, not in a
preference.** The objective is invariant under `x → t·x`. `‖x‖‖∇J‖/|J|` is invariant under the same
rescaling; `‖∇J‖_∞` is not, and can be driven down by rescaling the coefficient vector without
moving the geometry at all. That is not a hypothetical: **`L6`'s L-BFGS-B falsely reported
convergence exactly once, for exactly this reason** (`experiments/journal/leg_401.md` §7.3). The raw
gradient column is the one that defect knows how to fool. `L6-b`'s
`experiments/route4/l6b_terminal_stationarity.py` fixes `NOT_CRITICAL = 1.0` a priori and states the
measure on its face, which is correct.

**Disclosure obligation, and it is the point of writing this down.** The banked artefact carries
both columns. Any write-up — including `P4` — that quotes `153.22` as "the largest of its six" while
omitting that the same start has the smallest raw gradient is presenting a selected column. **Both
go in, with the invariance argument, every time.** My own earlier phrasing of this finding gave the
scale-invariant figure alone; that is the omission this paragraph exists to close.

### 3. THE DEFECT: `L6-b`'s `NO` branch does not distinguish what it says it distinguishes

`WAVE7_PLAN.md` pre-committed, verbatim:

> **No material drop** ⟹ **the stall is the CONSTRUCTION, and `L6`'s `NO` hardens into a real
> result about route 4's ansatz.**

**That inference requires the 20,000-iteration iterate to be stationary, and the wording never said
so.** If the run reaches 20,000 with `scale_invariant_grad` still of order 10² — which is where the
banked start sits at 7,000 (`116.9`, having been `205.1` at 4,700 and `161.8` earlier, oscillating
in a 66–274 band rather than decaying toward zero) — then the honest reading of "no material drop"
is **"25× the budget did not move it, and it is still descending"**, which is a bound on what budget
alone buys. It is NOT "the stall is the construction", because a non-stationary terminal iterate is
by definition still budget-limited. **The two hypotheses the gate was built to separate are not
separated by a `NO` at a non-critical point.**

**The `YES` branch is untouched and I want that asymmetry on the record.** A drop below `1.45` proves
`L6`'s ladder was budget-limited regardless of whether 20,000 converged — a descent that keeps
descending is exactly the evidence that branch needs. So the gate is sound in one direction and
under-specified in the other. **Gates can be half-defective and this one is.**

### 4. The amendment, stated as a rule for the reading and not as a change to the threshold

**`1.45` does not move. The gate number is the gate number.** What changes is the sentence the `NO`
licenses, and it is now three-way rather than two-way, keyed to a quantity the unit is already
instrumented to report:

| at 20,000 | `scale_invariant_grad` | what a `NO` licenses |
|---|---|---|
| no drop below 1.45 | **< 1** (critical) | the pre-committed reading STANDS IN FULL: the stall is the construction, `L6`'s `NO` hardens into a result about the ansatz |
| no drop below 1.45 | **≥ 1** (still descending) | **ONLY**: "25× `L6`'s budget, and still not stationary — budget alone does not reach 1.45." `L7`/`L4` prices stay OPEN. The ansatz is NOT exonerated and NOT convicted. |
| drop below 1.45 | either | the pre-committed `YES` reading stands in full, unaffected |

**On present evidence the middle row is the one that will fire**, and it is the weakest of the three
— which is precisely why it is written down at 7,000 iterations instead of at the landing. The
degenerate outcome this forecloses is the one where the unit lands a clean `NO`, the plan's sentence
is quoted, and `W4`'s route-4 arm is recorded as closed on a comparison between two arbitrary
stopping points.

**What this does NOT do.** It moves no `L1→L4` link. It does not touch `E-FE`, `W4` clause (b), or
`PB2`'s subject. It changes nothing the unit is doing — the run continues untouched to 20,000, and
the three-way table reads fields it already banks. **And it is not progress**: it is a gate I wrote
being found under-specified before it fired, which §3i q7 counts against the instrument, not for it.

## CONDUCTOR MEASUREMENT 2026-08-19 03:20 — `E-FE`'s SCHEDULE, RE-PRICED FROM ITS OWN PER-ATTEMPT HOURS

From the unit's own progress lines (`[3/163]`–`[6/163]`), four completed attempts: `0.39 h`
converged, `0.70 / 0.77 / 0.78 h` stalled at the 20-epoch cap. Mean **`0.660 h/attempt`** against a
briefed `0.569` (`91 core-h / 160`).

| | core-h | wall at 6 shards | vs brief |
|---|---|---|---|
| briefed | 91.0 | 15.2 h | — |
| at the observed mean | 105.6 | 17.6 h | **×1.16** |
| if stalls dominate (`0.750 h`) | 120.0 | 20.0 h | **×1.32** |

**ETA `20:00`–`22:30` today**, not the `~17:30` on my task list, which is corrected. `n = 4` and the
recovery rate is `1 in 4` — far too few for an interval, and none is claimed. **My first projection
of this was `×2.09` and it was wrong**; the error and its class are recorded at `CORRECTIONS.md`
§42, together with the two other throughput-arithmetic errors of the last day.

**Consequence for wave 8, stated now.** `E-FE` holds 6 of 12 cores until ~20:00–22:30. Wave 8 is
`L-JVER` ‖ `PB2` ‖ `PB1` ‖ `V-W7`, and **three of those four are reading-and-writing units with no
solver load** — `PB2` reads two theorems at primary, `PB1` runs a novelty check, `V-W7` audits. The
overrun therefore does **not** block the wave-8 dispatch, and no shard count is changed mid-run:
that was pre-committed against, and changing it destroys the per-attempt cost figure the ensemble
owes the record.
