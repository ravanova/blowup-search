# PROG-R4 U5 — MILESTONE M3: stratifying the seed budget by SHIFT

**Unit:** PROG-R4 U5 (leg 380), `ORCHESTRATION.md` §3c programme lane. **BUILD unit — answers a
milestone, not a gate.** Under §3c the worker is not terminated on landing it, and U0's novelty
pass binds (no fresh pass run).
**Mode:** §3f SOLO. **UNVERIFIED** — produced and checked in one session, no paired verifier.
**Data of record:** `writeup/data/p2_prog_r4_m3_v1.json`; ledger
`experiments/programme_r4/u5_m3_ledger.json`; seed library
`experiments/programme_r4/u5_shift_library_admissible.json`.
**Evidence:** `experiments/p2_prog_r4_m3_evidence.py`, 27/27 — re-derives every number below from
the banked JSONs.
**Figure:** fig107, 16/16 checks.
**Pre-registration:** `experiments/journal/prog_r4_u2u3_prereg_addendum.md` §3g (**AMENDMENT 5**),
commit `4f6f33f`, before either stage ran.
**Journal:** `experiments/journal/prog_r4_u5.md`.

> **G1 IS NOT RE-ANSWERED HERE.** It stays `UNDER-RESOURCED` as banked in
> `writeup/data/p2_prog_r4_g1_v1.json`, which this unit does not write to. `n_recovered = 0` is a
> **count**, pre-registered as such; it is not a `no` at G1, and no G1 re-open is raised.

---

## 1. Milestone and answer

> **M3: THE SEED BUDGET IS STRATIFIED BY SHIFT** — the anchored reservoir is exhausted, the
> published `|s|` band is filled to a pre-committed quota, and the per-stratum yield is measured
> against U3's banked baseline.

**`DELIVERED`**, on all five pre-committed clauses:

| clause | required | realised |
|---|---|---|
| 1 mining exhaustive | every anchored strict local min not provably excluded | 75,873 taken; `R_red` max 0.2499996 (prune saturated) |
| 2 band filled | ≥ 50 of 100 seeded in `\|s\| ∈ [0.295, 0.707]` | **60** (U3: 31) |
| 3 settings unchanged, no iterations bought | caps, `tol`, window, `m=0`, anchor, match | asserted at startup; **2,104** epochs vs U3's **4,629** |
| 4 yield reported vs U3's baseline | per stratum, in-band as a magnitude either way | §5 |
| 5 controls fire as planted | P recovered ∧ N did not ∧ R recovered | **P ✓ N ✗(as planted) R ✓** |

`n_attempts = 100`, `n_converged_to_tol = 9`, `n_recovered = 0`, best final `‖R‖ = 8.67e-12`,
median final `‖R‖ = 3.14`, 42,228 Jacobian evaluations, 7.13 h at 8 workers.

**Ceiling: TIER 2.** No `L1 → L4` link moved. Clay stays ~0.05%.

## 2. Why the previous fix does not transfer

AMENDMENT 4 stratified the mining budget by **period**, because period is a coordinate of the
`(t, T)` plane the mining searches. Shift is not. `R_red` is built from amplitude spectra and is
**shift-invariant by construction** — the same property that makes it a lossless pre-filter
(`R_red ≤ R` pointwise, so `R_red ≥ 0.25` provably cannot hide `R < 0.25`). `|s|` does not exist
until the full minimisation over the continuous `x`-shift and discrete `y`-shift runs.

U5 therefore **exhausts** at the mining stage and **stratifies** downstream:

> **MINING RULE.** Take every anchored strict local minimum of `R_red` with `R_red < 0.25`.
> Nothing ranked, nothing truncated, no `per_anchor`, no researcher degree of freedom in the take.

## 3. Resourcing as run

| | value | note |
|---|---|---|
| `T_dns`, `N`, `Re`, forcing | `1.0e5`, 24, 60.0, `n=4` | U2 (M2); 578 real unknowns |
| globalisation | Newton–GMRES–hookstep trust region | U1 (M1), unchanged |
| `n_attempts`, `tol` | 100, `1e-8` | |
| `max_newton`, `max_gmres`, `gmres_rtol` | 52, 140, `1e-3` | **identical to U3, asserted at startup** |
| epochs spent | **2,104** | U3: 4,629 — 45.5%, against the rule's replayed 45.0% |
| wall | 7.13 h, 8 workers | 57.04 core-hours (attempts stage) |
| regeneration + re-mine wall | 48.2 min | block-parallel replay, 8 workers |
| shift sign | 99 minus, 1 plus | measured per seed, not assumed |
| `short_of_requested` | 0 | every stratum met quota; redistribution never fired |

Costed at 95 s/epoch (U3 erratum 2), **not** the probe's 54.7.

**Options explicitly not taken.** U3 §8's (b) relax the admission test, (c) carry an `m` unknown in
the residual, (d) buy iterations. (c) would change the realization and invalidate M1's
reproduction; it needs its own milestone. (d) is the opposite of what happened — see §3.1.

### 3.1 The stall exit, validated before it was used

`max_newton_hit` was replaced by an exit rule — after epoch 20, stop if `‖R‖_k > 0.5·‖R‖_{k−10}` —
and the rule was **replayed against U3's banked residual histories before U5 ran**:

| | value |
|---|---|
| U3 epochs, actual | 4,629 |
| U3 epochs, under the rule | 2,083 (45.0%) |
| U3 convergences the rule would have cut | **0 of 14** |
| worst true-convergence 10-epoch ratio at `k ≥ 20` | 0.0724 against the 0.50 threshold |
| margin | **6.9×** |

This is a spend **reduction**, not an iteration purchase, and clause 3 is checked in that
direction.

## 4. The supply side

**The take.** 913,301 strict local minima → **103,844 anchored** (within `T_ANCHOR_TOL = 1.0` of a
named period) → **75,873** with `R_red < 0.25`. U2 took 2,014: a **37.7×** deeper take.

**The funnel.** 75,873 mined → **575** in the Newton window `R < 0.25` → **241** with `m = 0` (all
575 already anchored) → **100** spent. **334 dropped for `m ≠ 0`** (58.1% of the window).

| stratum | `\|s\|` | supply | quota | realised | diversity skips |
|---|---|---|---|---|---|
| **P** published | `[0.295, 0.707]` | **72** | 60 | **60** | 9 |
| **L** low | `[0.000, 0.150)` | 89 | 20 | 20 | 3 |
| **M** mid | `[0.150, 0.295)` | 67 | 10 | 10 | 0 |
| **H** high | `(0.707, π]` | 13 | 10 | 10 | 1 |

U2's library offered **35** in-band admissible candidates; U5's offers **72**. That is the whole
supply-side intervention.

**Per-row in-band supply** (the per-row cap of 8 bound on UPO37, UPO22, UPO9 — which is what it is
for): UPO37 21, UPO9 16, UPO22 11, UPO32 9, UPO17 6, UPO35 5, UPO20 4, **UPO34 0**. UPO34 has no
in-band anchored admissible candidate anywhere in the exhaustive pool.

### 4.1 The admission table, remade on 38× the data

`TECHNICAL_P2_PROGR4_G1.md` §5 measured admission against `|s|` on 2,014 **globally-ranked**
candidates. That measurement is superseded here by the same measurement on the exhaustive pool —
same phenomenon, no ranking step in it:

| `\|s\|` | n | in window | & `m=0` | admissible rate | fraction `m=0` |
|---|---|---|---|---|---|
| `[0.000,0.150)` | 8,492 | 89 | 89 | 1.05% | 0.940 |
| `[0.150,0.295)` | 7,656 | 67 | 67 | 0.88% | 0.928 |
| `[0.295,0.450)` | 6,856 | 45 | 45 | 0.66% | 0.915 |
| `[0.450,0.550)` | 3,970 | 13 | 13 | 0.33% | 0.890 |
| `[0.550,0.707)` | 5,052 | 15 | 14 | 0.28% | 0.846 |
| `[0.707,0.900)` | 5,467 | 10 | 8 | 0.15% | 0.773 |
| `[0.900,1.500)` | 13,426 | 137 | **3** | 0.02% | 0.552 |
| `[1.500,3.142]` | 24,954 | 199 | **2** | 0.01% | 0.386 |

Admission falls monotonically with `|s|` to 0.9, then the pattern **breaks**: the *window* rate
recovers sharply while the `m = 0` rate collapses. Those cells are the `m ≠ 0` class the extended
residual cannot express. So "large shift is hard" and "large shift is a symmetry class this
realization is blind to" are separated by the `m = 0` column, and above `|s| = 0.9` it is
overwhelmingly the second.

**Read with its confound.** For a candidate that is not a genuine near-recurrence, the minimising
shift is a nuisance parameter and its `|s|` is close to meaningless, so the high-`|s|` bins mix
"shift is hard" with "this was never a recurrence". The `m = 0` column is the part that survives.

### 4.2 Containment, and a number that reads like a defect

U2's library contains 81 candidates with `R` below U5's pool minimum of 0.0685, global best 0.0165.
**All 81 are unanchored**, at `T ∈ [1.75, 2.5]` — trivial short-time near-recurrences far below the
smallest named period, outside an anchored-only rule by design. The check that binds: **all 133** of
U2's anchored admissible candidates are inside U5's 241, none disagreeing on `(R, s, m)` to full
float precision. Asserted in `u5_reduce_library.py`, not claimed.

**Parallel regeneration was checked before it was trusted, and the check fired.** The first
block-parallel implementation walked from `pos = block · CKPT_EVERY` and produced
`R = 2.50754 / 2.15963 / 2.06460` against U2's serial `2.28409 / 1.99639 / 2.03410`. Cause: `run_dns`
writes the checkpoint *before* the steps producing snapshot `k`, so `ckpt[b]` is the state at index
`b·CKPT_EVERY − 1`. Fixed; re-tested to `max|diff| = 0.000e+00` over 80 sampled snapshots, and 40
banked U2 candidates re-mined to **exact** equality in `(R, s, m)`.

## 5. Per-stratum yield, and the pre-registered fork

| stratum | U5 | rate [Wilson 95%] | U3 baseline | median seed `R`, U5 / U3 |
|---|---|---|---|---|
| **P** published | **5/60** | 8.3% [3.6, 18.1] | 1/31 | 0.2122 / 0.1897 |
| **L** low | 4/20 | 20.0% [8.1, 41.6] | 9/39 | 0.1731 / 0.1840 |
| **M** mid | 0/10 | 0.0% [0.0, 27.8] | 4/28 | 0.1324 / 0.1853 |
| **H** high | 0/10 | 0.0% [0.0, 27.8] | 0/2 | 0.2297 / 0.1592 |
| **overall** | 9/100 | 9.0% [4.8, 16.2] | 14/100 | 0.1913 / 0.1859 |

Every interval overlaps its U3 counterpart; **not one stratum's change resolves at 95%**. The
in-band rate rose from 1/31 to 5/60 and that is inside noise. Overall 9/100 against U3's 14/100 —
not distinguishable, and the seed pools are not the same anyway, which is what §5's matched-`R`
comparison is for.

AMENDMENT 5 named two rival readings of U3's in-band drought and what would kill each.

**H-supply — REFUTED as the operative explanation.** Its premise was repaired (supply 35 → 72,
spend 31 → 60) and its prediction — more in-band seeds produce a recovery — failed at 60 in-band
attempts and 0 recoveries.

**H-hard — FAVOURED, NOT RESOLVED.** A raw rate comparison confounds "the band is hard" with "these
seeds are worse", which is the same shape of confound this programme is about, so the comparison is
made at matched seed `R`, pooled over both runs' 200 attempts in common quartiles:

| `R` quartile | in-band | out-of-band |
|---|---|---|
| `[0.0836, 0.1630)` | 0/9 | 3/41 |
| `[0.1630, 0.1886)` | 0/21 | 7/29 |
| `[0.1886, 0.2128)` | 4/26 | 4/23 |
| `[0.2128, 0.2418]` | 2/35 | 3/16 |
| **pooled** | **6/91 = 6.6%** | **17/109 = 15.6%** |

Fisher exact two-sided **p = 0.073**. Above 0.05. This is a lean, reported as a lean. (Fisher is
implemented from scratch in the evidence script; no scipy dependency was added for one number.)

## 6. The result: convergences leave the band

Of the 9 convergences, 5 were seeded in-band. **4 of those 5 finished outside it.**

| seed `\|s\|` | final `\|s\|` | left band |
|---|---|---|
| 0.6187 | 0.5867 | no |
| 0.3966 | 0.1173 | **yes** |
| 0.4246 | 0.0997 | **yes** |
| 0.3114 | 0.1327 | **yes** |
| 0.3459 | 0.1008 | **yes** |

**8 of 9** convergences finished at `|s| < 0.15`; range 0.0729–0.5867.

**This is a replication, not a post-hoc reading.** The addendum recorded from U3's banked data,
before U5 ran, that 13 of its 14 convergences also finished at `|s| < 0.15`. (The addendum's wording
"moved `|s|` toward zero or stayed there" is loose — only 9 of 14 strictly decreased; the measured
invariant is the **endpoint**, and that is the form U5 replicates on an independent 60-attempt arm.)
Separately, commit `c67179e`, landed by a concurrent session **while U5 was still in flight and
before any U5 number was visible**, fixed that what decides U5 is where the converged orbits sit in
`|s|`. Its branch **(b)** fired: **the bias is in the BASIN STRUCTURE, not only in the seed supply.**

Not separated by this data: "the low-`|s|` basins are larger" vs "this hookstep globalisation drifts
that way". Both are claims about the solver's destination rather than its menu.

**Closest approach to a named row across all 100 attempts:** attempt 0 (UPO37), `ΔT = 0.127`,
`Δ|s| = 0.0099` — inside tolerance on `s`, outside on `T` — at final `‖R‖ = 2.20`, i.e. not a
solution. No attempt came close on both coordinates *and* converged. No near-miss is manufactured.

## 7. What the stratification bought, against U3's solution set

*Measured after the run, not pre-registered; changes no milestone clause.* Clustering at the
matching predicate's own tolerance (0.05 on both `T` and `|s|`, `s` wrapped to `(−π, π]`), U5's 9
convergences give **5 distinct solutions** and U3's 14 give **8**.

| `T` | `\|s\|` | attempts | strata | in U3's set |
|---|---|---|---|---|
| 16.5305 | 0.1008 | 3 | L, P | yes |
| 16.8744 | 0.0729 | 2 | L | yes |
| 19.2872 | 0.1173 | 1 | P | yes |
| **20.4175** | **0.5867** | 1 | P | **no — new** |
| 22.0389 | 0.1347 | 2 | L, P | yes |

The one new solution is **the only solution either unit has found inside the published band**, and
it is the single in-band convergence that did not leave (§6, first row). Read narrowly: it is not a
named Table IV row, `n_recovered` is still 0, G1 is still `UNDER-RESOURCED`.

**R0's metric** (distinct orbits per core-hour, which R0 fixed as the reported metric before this
landed, because per-attempt rate counts re-finds as successes): U5 **5 / 57.04 = 0.0877** against U3
**8 / 144.69 = 0.0553**. Two cautions owed to R0, neither resolved here — (i) R0's baseline quotes
134.45 core-hours for U3, where `p2_prog_r4_g1_v1.json` gives 52,087.95 s × 10 workers = **144.69**;
(ii) R0 disputes U3's distinct count of 8, and at 7 the baseline is 0.0484. Independent
re-clustering here reproduces **8**. U5 is above U3 on every variant, but the comparison stays
provisional until R0 lands.

**The case for deflation, sharpened.** 4 of 5 re-finds is *cross-unit*: a second 100-attempt budget
rediscovered what the first already had. This is what `R2` is queued against.

## 8. Option (c), priced

Carrying an `m` unknown in the extended residual would unlock **334 of the 575** in-window
candidates (58.1%). But of those 334, exactly **1** lies in the published `|s|` band. **Option (c)
is not a band fix; it is the `|s| > 0.9` fix.** Measured, not argued — evidence script §6.

## 9. Controls

Unchanged from U3's addendum §3, plus two structural controls added in §3g.6 that could have fired
against this unit: **L positive on the pipeline** (the low-`|s|` stratum must still converge, or the
stratification broke the seed pipeline) and **H against the monotone-in-`|s|` reading**.

`FIRED AS PLANTED := P recovered AND N did not recover AND (R recovered, if R ran)` — satisfied,
`failures = []`. A null from an instrument with a dead control would be uninterpretable.

## 10. Errata against this unit's own pre-registration

Full list in `experiments/journal/prog_r4_u5.md` §7. The one a reader most needs:

**(i) "Before either stage ran" is imprecise.** AMENDMENT 5 (`4f6f33f`, 12:31:10) quotes the
realised take — 75,873 candidates, 98,413 snapshots, 3,980 blocks — but the mining stage did not
finish until 13:29:33. Those three numbers come from the **prefilter prune alone** (913,301 →
103,844 anchored → 75,873, in 50.3 s), which performs no minimisation and computes no `|s|`. No
outcome-dependent number (the 72/89/67/13 supply, the 575, the 241) appears in that commit.

---

*Solo session, §3f. **UNVERIFIED**: self-checking is never recorded as verification, and every
number above is re-derivable by a fresh session from the banked JSONs via
`experiments/p2_prog_r4_m3_evidence.py`.*
