# PROG-R4, unit U5 — MILESTONE M3

**Programme:** PROG-R4 (`ORCHESTRATION.md` §3c PROGRAMME lane, slot A, leg 380).
**Unit kind:** BUILD. This unit answers a **milestone**, not a gate. Under §3c the worker is
**not terminated** on landing it and U0's novelty pass **binds** — no fresh novelty pass was run.
**Mode:** §3f SOLO. No paired verifier, no DM, no orchestrator.
**Everything below is UNVERIFIED** in the repo's sense: built and checked in one session.
Verification is a fresh session or it is not verification.

**U5 does not re-answer G1.** G1 stays `UNDER-RESOURCED` as banked in
`writeup/data/p2_prog_r4_g1_v1.json`, which this unit does not write to.

---

## 1. The milestone, in its pre-committed wording

Fixed in `experiments/journal/prog_r4_u2u3_prereg_addendum.md` §3g (**AMENDMENT 5**), committed
as `4f6f33f` **before either stage of U5 ran** and not restated, softened or re-scoped here.

> **M3: THE SEED BUDGET IS STRATIFIED BY SHIFT — the anchored reservoir is exhausted, the
> published `|s|` band is filled to a pre-committed quota, and the per-stratum yield is measured
> against U3's banked baseline.**

**DELIVERED** iff all five of: (1) the mining takes every anchored strict local minimum not
provably excluded by the Newton window; (2) at least 50 of 100 attempts are seeded in
`|s| ∈ [0.295, 0.707]`, against U3's 31; (3) the run completes at U3's caps, `tol`, admission
test, `m = 0` requirement, anchor rule and matching predicate, **none changed and no iterations
bought**; (4) the per-stratum yield is reported against U3's banked baseline; (5) the planted
controls fire as planted. **NOT DELIVERED** otherwise, for exactly one of `SUPPLY`, `INSTRUMENT`
or `BUDGET`.

## 2. THE ANSWER

> ## M3 = **DELIVERED**

All five clauses hold, each re-derived from `writeup/data/p2_prog_r4_m3_v1.json` and not from
this prose:

| clause | required | realised |
|---|---|---|
| 1 mining exhaustive | every anchored strict local min not provably excluded | **75,873** taken, `R_red` max 0.2499996 (the prune is saturated); U2 took 2,014 |
| 2 band filled | **≥ 50** in `\|s\| ∈ [0.295, 0.707]` | **60** (U3: 31) |
| 3 settings unchanged, no iterations bought | caps, `tol`, window, `m=0`, anchor, match all U3's | asserted at startup; **2,104** epochs spent against U3's **4,629** |
| 4 yield reported vs U3's baseline | per stratum, in-band as a magnitude either way | §6 |
| 5 controls fire as planted | P recovered ∧ N did not ∧ R recovered | **P ✓ N ✗(as planted) R ✓** |

**Headline numbers.** 100 attempts, 7.13 h at 8 workers, 2,104 epochs, 42,228 Jacobian
evaluations. **9 converged** to `‖R‖ ≤ 1e-8`. **0 recovered a named Table IV row.** Best final
residual `8.67e-12`; median final residual `3.14` — the failures fail wide, not narrowly.

**What this does and does not settle.** M3 is a **milestone about the seed budget**, and the
budget is now stratified: the thing AMENDMENT 5 promised to build exists and works. It is
**not** a statement about the named orbits.

> **G1 is untouched.** It stays **`UNDER-RESOURCED`** exactly as banked in
> `writeup/data/p2_prog_r4_g1_v1.json`, which this unit does not write to. `n_recovered = 0` is
> a **count**, pre-registered as such in §3g.3. It is **not** a `no` at G1 — `no` is still not an
> available branch there, and §3d is why: a stop fires only on a null from an attempt resourced
> at the scale the question is posed at, and 100 attempts is not that scale. **No G1 re-open is
> raised**, because a re-open is what `n_recovered > 0` would have triggered.

**The finding, on a reading pre-committed elsewhere while this run was still in flight.** Commit
`c67179e` fixed, before any U5 number was visible, that what decides U5 is *where the converged
orbits sit in `|s|`*. They sit low: **8 of 9 convergences below `|s| = 0.15`**, **4 of 5 in-band
convergences left the band**, and the 9 collapse to **5 distinct solutions**, four below 0.14 —
from a pool that was stratified precisely so this could not be a supply artefact. That is its
branch **(b)**: **the bias is in the BASIN STRUCTURE, not only in the seed supply.** §9.1 reports
it against the pre-commitment; it is a finding, not a null, and it demotes three of §9's five
options.

**Ceiling: TIER 2.** Nothing here is a proof. No `L1 → L4` link moved; Clay stays ~0.05%.
**UNVERIFIED** — solo session, §3f.

## 3. What was manipulated, and what was held

The single manipulated variable is **which seeds are offered**. Everything else is held at U3's
values, and held by assertion against U3's own banked record rather than by hand-copying:
`tol = 1e-8`, `max_newton = 52`, `max_gmres = 140`, `gmres_rtol = 1e-3`, window `R < 0.25`,
`m = 0`, anchor `|ΔT| ≤ 1.0`, match `0.05` on both `T` and `s`. The run asserts
`caps == U3's banked caps` at startup and refuses to start otherwise.

U3 §8's options **(b)** relax the admission test, **(c)** carry an `m` unknown in the residual
and **(d)** buy iterations are **NOT taken**. (c) would change the realization and invalidate
M1's reproduction; it needs its own milestone.

## 4. The supply side: shift is not observable where the mining happens

`R_red` is built from amplitude spectra and is **shift-invariant by construction** — the same
invariance that makes the prefilter lossless. So `|s|` does not exist at the prefilter stage and
cannot be stratified on there. AMENDMENT 4 could stratify on period because period *is* a
coordinate of the `(t, T)` plane; shift is not. U5 therefore **exhausts** rather than stratifies
at the mining stage, and stratifies downstream at the only stage where `|s|` exists.

> **MINING RULE.** Take every anchored strict local minimum of `R_red` with
> `R_red < R_THRES_WINDOW = 0.25`. Nothing ranked, nothing truncated, no `per_anchor`, no
> researcher degree of freedom left in the take.

The prune is **lossless, not a tuning**: `R_red ≤ R` pointwise, so a cell with `R_red ≥ 0.25`
provably cannot have `R < 0.25` and is already outside the Newton window.

The realised counts this rule produced are in §5.

**The parallel replay was checked before it was trusted, and the check fired.** Block-parallel
regeneration from the stored `complex128` checkpoints is a scheduling change, not a numerical
one, and the pre-registration required it to reproduce U2's serial `regenerate` **bit for bit**
or abort. The first implementation did not: it walked from `pos = block * CKPT_EVERY` and
produced `R = 2.50754 / 2.15963 / 2.06460` against U2's `2.28409 / 1.99639 / 2.03410`. The cause
is a convention in `run_dns` — the checkpoint is written *before* the steps that produce
snapshot `k`, so `ckpt[b]` is the state at index `b·CKPT_EVERY − 1`, which is exactly what U2's
`regenerate` encodes and what the parallel version had dropped. Fixed, re-tested to
`max|diff| = 0.000e+00` over 80 sampled snapshots, and separately re-mined 40 banked U2
candidates to **exact** equality in `(R, s, m)`. A planted check that never fires is decoration;
this one caught a real defect before a single candidate was mined.

## 5. Realised counts

**The take.** 913,301 strict local minima in the `(t, T)` plane → **103,844 anchored** (within
`T_ANCHOR_TOL = 1.0` of a named period) → **75,873** with `R_red < 0.25`. Against U2's 2,014,
a **37.7×** deeper take. Each faces the identical full minimisation over the continuous `x`-shift
and discrete `y`-shift, the identical window test, `m = 0` requirement and anchor rule.

**The funnel to seeds.**

| stage | count |
|---|---|
| mined candidates | 75,873 |
| in Newton window `R < 0.25` | **575** |
| of those, `m = 0` (and all 575 already anchored) | **241** |
| dropped for `m ≠ 0` | **334** (58.1% of the window) |
| spent as seeds | **100** |

**Supply against quota — the band is no longer the binding constraint.**

| stratum | `\|s\|` | supply | quota | realised | diversity skips |
|---|---|---|---|---|---|
| **P** published | `[0.295, 0.707]` | **72** | 60 | **60** | 9 |
| **L** low | `[0.000, 0.150)` | 89 | 20 | 20 | 3 |
| **M** mid | `[0.150, 0.295)` | 67 | 10 | 10 | 0 |
| **H** high | `(0.707, π]` | 13 | 10 | 10 | 1 |

No stratum fell short, so the shortfall redistribution never fired and the realised counts equal
the quota exactly. **U2's library offered 35 in-band admissible candidates; U5's offers 72.** That
is the whole supply-side intervention, and it is what makes clause 2 reachable at all.

**Per-row in-band supply** (the per-row cap of 8 was the binding constraint on UPO37, UPO22 and
UPO9, which is what the cap is for): UPO37 21, UPO9 16, UPO22 11, UPO32 9, UPO17 6, UPO35 5,
UPO20 4, **UPO34 0**. UPO34 has no in-band anchored admissible candidate anywhere in the
exhaustive pool.

**A number that reads like a defect and is not.** U2's library contains 81 candidates with `R`
below U5's pool minimum of `0.0685`, including a global best of `0.0165`. **All 81 are
unanchored**, at `T ∈ [1.75, 2.5]` — trivial short-time near-recurrences, far below the smallest
named period. U5's mining rule is anchored-only by construction, so they are outside its take by
design, not by omission. The containment check that *does* bind is the one on admissible
candidates: **all 133** of U2's anchored admissible candidates are inside U5's 241, none
disagreeing on `(R, s, m)` to full float precision. That is a prediction of `R_red ≤ R`, not a
restatement of the rule, and it is asserted in `u5_reduce_library.py`, not claimed here.

**The admission table, remade on 38× the data.** U3 §5 measured admission against `|s|` on 2,014
globally-ranked candidates; this is the same measurement on the exhaustive pool:

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

Admission falls monotonically with `|s|` to 0.9, then the pattern **breaks**: above 0.9 the
*window* rate recovers sharply (137 and 199 in-window cells) while the `m = 0` rate collapses to
0.02% and 0.01%. Those cells are the **`m ≠ 0` class the extended residual cannot express**. So
"large shift is hard" and "large shift is a different symmetry class this realization is blind to"
are separated by the `m = 0` column, and above `|s| = 0.9` it is overwhelmingly the second.

**Read with its confound, which is stated because it is real.** For a candidate that is *not* a
near-recurrence, the minimising shift is a nuisance parameter and its `|s|` is close to
meaningless. The high-`|s|` bins therefore mix "shift is hard" with "this was never a recurrence".
The `m = 0` column is the part that survives the confound.

## 6. The per-stratum yield, and the H-supply / H-hard fork §3g.2 pre-named

### 6.1 The raw table, with intervals

| stratum | U5 | rate [Wilson 95%] | U3 baseline | rate [Wilson 95%] | median seed `R`, U5 / U3 |
|---|---|---|---|---|---|
| **P** published | **5/60** | 8.3% [3.6, 18.1] | 1/31 | 3.2% [0.6, 16.2] | 0.2122 / 0.1897 |
| **L** low | 4/20 | 20.0% [8.1, 41.6] | 9/39 | 23.1% [12.6, 38.3] | 0.1731 / 0.1840 |
| **M** mid | 0/10 | 0.0% [0.0, 27.8] | 4/28 | 14.3% [5.7, 31.5] | 0.1324 / 0.1853 |
| **H** high | 0/10 | 0.0% [0.0, 27.8] | 0/2 | 0.0% [0.0, 65.8] | 0.2297 / 0.1592 |
| **overall** | 9/100 | 9.0% [4.8, 16.2] | 14/100 | 14.0% [8.5, 22.1] | 0.1913 / 0.1859 |

**Every interval overlaps its counterpart. Not one stratum's change is resolved at 95%**, and the
in-band rise from 3.2% to 8.3% is stated here as a magnitude precisely because it is *not*
significant. Anyone reading "the in-band yield more than doubled" out of this table is reading it
wrong, and the next subsection is why.

### 6.2 The structural controls, both of which could have fired against this unit

- **Stratum L, positive control on the pipeline.** 4/20 = 20.0% against U3's 23.1%. The deeper
  mining and the new allocation did **not** break the seed pipeline; the in-band arm is
  interpretable. Had L come back at ~0% this whole unit would have been uninterpretable, and
  §3g.6 committed to saying so.
- **Stratum H, negative-side control on the monotone-in-`|s|` story.** H did **not** converge
  better than P (0/10 vs 5/60), so the pre-registered withdrawal condition did not trigger. But
  the monotone story is not clean either: **M returned 0/10** while P returned 8.3%, so yield is
  not monotone in `|s|` across the middle. At n = 10 per cell that is weak, and it is recorded as
  weak.

### 6.3 The fork, answered: **H-supply is refuted as the operative explanation; the evidence favours H-hard but does not resolve it**

§3g.2 pre-named two mechanisms for U3's in-band miss and said U5 is the experiment that separates
them. It does, in one direction cleanly and the other direction only partially.

**H-supply is refuted, in both of its parts.**

1. Its premise — "the library is starved in-band (35 of 133)" — was **true and is now repaired**:
   exhaustive mining raised in-band admissible supply 35 → **72**, and the spend 31 → **60**. The
   P quota filled with 12 candidates to spare, so in-band supply is no longer what limits the
   budget.
2. Its prediction — "**more in-band seeds → recovery**" — is **falsified at this scale**. 60
   in-band seeds returned **0** recoveries. Under §3d this does not become a `no`; it removes
   supply as the *explanation* while leaving the question under-resourced.

**H-hard: the direction is right, the significance is not there.** The raw in-band rise cannot be
read as evidence against H-hard, because U5's in-band seeds are measurably **worse** than U3's
(median `R` 0.2122 vs 0.1897) — filling a quota of 60 from a supply of 72 necessarily reaches
deeper into `R` than picking 31 off a global ranking. Controlling for that by binning both runs'
200 attempts into common seed-`R` quartiles:

| seed `R` bin | in-band | out-of-band |
|---|---|---|
| `[0.0836, 0.1630)` | 0/9 | 3/41 |
| `[0.1630, 0.1886)` | 0/21 | 7/29 |
| `[0.1886, 0.2128)` | 4/26 | 4/23 |
| `[0.2128, 0.2418]` | 2/35 | 3/16 |
| **pooled, 200 attempts** | **6/91 (6.6%)** | **17/109 (15.6%)** |

Fisher exact, two-sided: **p = 0.073**. At matched seed quality the in-band conversion rate is
**lower**, by a factor of ~2.4, in the same direction in three of four bins — but it does not
clear 0.05, and it is reported as not clearing it. (Fisher is implemented from scratch in the
analysis rather than adding a `scipy` dependency for one number.)

### 6.4 The sharpest result: **seeds converge out of the band**

This is a replication, not a post-hoc story. §3g.2 recorded from U3's banked record, *before U5
ran*, that of U3's 14 convergences **13 moved `|s|` toward zero or stayed there**, and that its
single in-band convergence went `|s| = 0.425 → 0.100`. U5 reproduces it on an independent
60-attempt in-band arm:

| seed `\|s\|` (stratum P) | converged `\|s\|` |
|---|---|
| 0.6187 | 0.5867 |
| 0.3966 | 0.1173 |
| 0.4246 | 0.0997 |
| 0.3114 | 0.1327 |
| 0.3459 | 0.1008 |

**4 of 5 in-band convergences left the band.** Across all 9 convergences, **8 have final
`|s| < 0.15`**; the range is 0.0729 to 0.5867.

And the 9 convergences are not 9 orbits. Clustering at the matching predicate's own tolerance
(0.05 on both `T` and `|s|`) gives **5 distinct solutions**:

| `T` | `\|s\|` | found by | strata | anchors |
|---|---|---|---|---|
| 16.5305 | 0.1008 | 3 attempts | L, P, P | UPO9, UPO17 |
| 16.8744 | 0.0729 | 2 attempts | L, L | UPO9 |
| 19.2872 | 0.1173 | 1 attempt | P | UPO22 |
| 20.4175 | 0.5867 | 1 attempt | P | UPO37 |
| 22.0389 | 0.1347 | 2 attempts | L, P | UPO37 |

Four of the five sit at `|s| < 0.14`. Two are reached from *different strata* and one from two
different anchors — so the run is repeatedly rediscovering a small set of low-shift solutions
regardless of where in `|s|` it is seeded.

**Closest approach to any named row across all 100 attempts**: attempt 0 (UPO37) at `ΔT = 0.127`,
`Δ|s| = 0.0099` — inside the matching tolerance on `s` and outside on `T` — but at final
`‖R‖ = 2.20`, i.e. not a solution at all. No attempt came close on both coordinates *and*
converged. There is no near-miss to report and none is manufactured.

### 6.5 What the epoch count says

2,104 epochs against U3's 4,629 — **45.5%**, against the stall rule's replayed prediction of
45.0%. The rule performed on live data exactly as it did on U3's banked ledger. **91 of 100
attempts exited `stalled`** and 9 converged; U3's corresponding split was 86 `max_newton_hit` and
14 converged. No attempt in either run was cut while still descending: the worst 10-epoch ratio
any U3 convergence exhibited at `k ≥ 20` was 0.0724 against the rule's 0.50 threshold, a factor
of 6.9. **U5 spent fewer iterations than U3 and bought none.**

## 7. Errata and departures against my own pre-registration

**(i) The pre-registration's "before either stage ran" is imprecise, and here is exactly what had
run.** AMENDMENT 5 (`4f6f33f`, 12:31:10) quotes the realised take — 75,873 candidates, 98,413
snapshots, 3,980 blocks — and the expensive mining stage did not finish until 13:29:33. Those
three numbers come from the **prefilter prune alone** (mining log line 1: 913,301 → 103,844
anchored → 75,873 in 50.3 s), which performs no minimisation. **Nothing M3 is evaluated on
existed at commit time**: `|s|` is undefined before the minimisation, and the per-stratum supply
(72/89/67/13), the window and `m = 0` counts (575, 241) and every outcome appear nowhere in the
amendment. Checked by grep against the commit, not asserted. The pre-registration is intact; the
wording should have said "before the minimisation, the allocation or any attempt ran", and §1's
restatement inherits the same imprecision.

**(ii) Two named rows sit outside the band the quota rule glosses as theirs.** §3g.4's table
calls `[0.295, 0.707]` "the band all eight named rows live in". On the wrapped `|s|` convention
used everywhere in this programme, that is inexact for two of the eight:

- **UPO35**: `|s| = 0.7071853071795857`, which is `1.853e-4` **above** 0.707 → stratum **H**;
- **UPO9**: `|s| = 0.29499999999999993`, which is `5.551e-17` **below** 0.295 → stratum **M**.

The rule as written was applied **unchanged** — the interval is the pre-registered object and
clause 2 is evaluated on the interval, not on the gloss. The gloss is what is wrong. This has no
effect on the allocation (strata are defined by the interval) and none on matching (the predicate
compares against each row's own published `(T, s)`, not against a band). All eight rows have
`m = 0`, so the `m = 0` requirement excludes no target.

**(iii) Three `RuntimeWarning`s new to U5; U3's log has zero.** Overflow in `rhs_physical`'s
advection product and the resulting non-finite FFT, from a hookstep trial that walked into a
blow-up. The driver has an explicit `nonfinite_residual` reject path, so these are *handled*
rather than silent, and the trust region contracts and continues. They are new to U5 because U5
seeds from a deeper, higher-`R` take. Reported as a count because a warning that appears in one
run and not another is a difference, and differences get reported.

**(iv) Deliberate departures from U3's *scheduling*, pre-registered in §3g.5, none of them a
change to the numerics.** 8 workers rather than 10 (measured contention optimum: 3.22 eval/s at 8
against 2.91 at 10 on this 6-core machine — U3 ran past the optimum, which is erratum (ii)'s
suspected mechanism now localised); `imap_unordered(chunksize=1)` rather than `Pool.map`, which
repairs erratum (i)'s tail-worker imbalance and is what made per-attempt progress reporting
possible; block-parallel snapshot regeneration, checked bit for bit. **Caps, `tol`, window,
`m = 0`, anchor rule and matching predicate are byte-identical to U3's banked values and asserted
at startup**, so the yields are comparable attempt for attempt.

**(v) Projected 7 h total, realised 7.13 h for the attempts alone** (plus 0.80 h mining, 0.68 h
controls; 8.6 h end to end). The attempts estimate of ~5.9 h was ~17% low. Epochs were costed at
95 s as required; the realised figure is 97.6 core-seconds per epoch, so the cost model was
right and the epoch count was slightly under-predicted (2,104 realised against 2,083 replayed).

## 8. Lesson 91: what this unit's negative names

A negative names its **realization, trial space and basis**. U5's zero-recovery count carries
U3's two clauses and adds a third that is new and is the point of the unit:

1. **Realization.** The stepper is a Lie–Trotter split, **first order in time** (measured global
   ratio 2.00). The named rows were computed in a different realization.
2. **Trial space.** The extended residual carries a **continuous `x`-shift only**. The `m ≠ 0`
   class cannot be expressed as a seed at all — and §5 now measures the size of that hole:
   **334 of 575 in-window candidates, 58.1%**, and above `|s| = 0.9` it is essentially the entire
   window.
3. **Basis — new at U5.** The seed pool is now shift-**stratified** rather than shift-**biased**.
   That is the one thing that changed, and it changed by design: 60 in-band attempts against 31,
   drawn from 72 in-band admissible candidates against 35. So the sentence "the mining starved the
   band" is **no longer available** as an explanation of a zero count. Whatever explains the
   remaining miss, it is not the shift bias in the take.

**What this negative therefore is.** Not "there are no relative periodic orbits at these
parameters" — the run converged to 5 distinct ones. Not "the named orbits are not there". It is:
*this first-order, `m = 0`-only realization, seeded from a shift-stratified exhaustive anchored
take at `N = 24`, `Re = 60`, `T = 1e5`, converges to a small set of low-`|s|` solutions and does
not reach the named rows within 100 attempts.* Every clause in that sentence is load-bearing and
each one is a place a successor unit could act.

## 9. Successor items, in order — NOT chosen

Under §3f I pre-commit the **next task**, but I do **not** choose my own continuation when the
outcome raises a fork. The options below are ordered with costs, for the user to rule on, exactly
as U3's §8 did.

**The next task is already fixed and is not part of this fork.** `STATE.md` item 2 — the two owed
novelty questions on U3's own output — is next regardless of how the fork below is ruled, and it
was not started in this session.

**Cost basis, measured this run, not estimated.** 0.0713 h wall per attempt at 8 workers (2,104
epochs / 100 attempts, epochs costed at 95 s as required); 0.68 h for the control set; 0.80 h for
a full re-mine; 3.44 h for a fresh `T = 1e5` DNS.

**The constraint that shapes every option: the anchored admissible pool is now exhausted at
`R < 0.25`.** 241 candidates exist, 100 are spent, **141 remain — of which only 12 are in-band**.
No option that keeps the current window can push the in-band arm past 72 attempts, ever.

---

**A. Spend the rest of the pool.** 141 attempts on the remaining anchored admissible candidates.
*Cost:* ≈ **10.7 h** (141 × 0.0713 + 0.68). *What it buys:* the in-band arm grows 60 → 72 only,
so it barely moves the measurement that matters; at U5's rate expect ~13 more convergences and,
on this evidence, ~0 recoveries. *Verdict:* **lowest information per hour of the five.** It is
listed first only because it is the one option requiring no new decision.

**B. Relax the admission window to Chandler & Kerswell's `R_thres = 0.3`** (U3's option (b)).
*Cost:* ≈ **0.9 h re-mine + 0.0713 h per attempt** (≈ 8 h for a fresh 100). *Caveat that must be
stated:* the supply multiplier **cannot be read off U5's library**, because the take was pruned
at `R_red < 0.25` — the re-mine is what measures it. *What it buys:* more supply, in-band
included, **without touching the realization**, so M1's reproduction still compares attempt for
attempt and the U3/U5 yield baselines stay usable. *Risk:* a looser window admits worse seeds, and
§6.3 already shows conversion falling with seed `R`; this could raise supply and lower yield
together.

**C. Carry `m` as an unknown in the residual** (U3's option (c)). *Cost:* a **full unit** —
new unknown, its Jacobian action and a phase condition, then a fresh attempt run; ≈ 10 h compute
plus the solver work, and **its own milestone**, since it changes the realization and M1's
reproduction no longer compares attempt for attempt. *What §5 now says about it, which U3 could
not:* it unlocks **334** anchored in-window candidates, 58.1% of the window — **but only 1 of the
334 is in the published band.** It is therefore **not a fix for the band**; it is the fix for
`|s| > 0.9`, where the `m = 0` rate collapses to 0.02%/0.01% while the window rate recovers.
Worth doing on its own merits as the largest measured hole in the trial space; wrong tool for the
named rows.

**D. Raise supply at source** — longer DNS or finer `N`. *Cost:* ≈ **3.4 h per additional
`T = 1e5`** plus ≈ 0.9 h re-mine per pass, plus attempts; `N` refinement costs more and
invalidates the banked library entirely. *What it buys:* supply scales roughly with `T`, so
doubling the trajectory roughly doubles all four strata. *What it does not buy:* nothing about
H-hard. If in-band conversion is genuinely ~2.4× worse at matched seed quality, this multiplies
attempts into that penalty rather than removing it.

**E. Attack H-hard directly, from data already banked.** §6.4 is the strongest unexplained result
in the unit: 4 of 5 in-band convergences **leave the band**, 8 of 9 convergences land at
`|s| < 0.15`, and 9 convergences collapse to 5 distinct solutions. A diagnostic unit on the **200
attempts already on disk** (U3's 100 + U5's 100) — converged-`|s|` distribution against seed
`|s|`, whether the low-`|s|` solutions are attractors of the hookstep iteration or of the
minimisation, and whether the named rows are reachable *at all* by seeding directly at their
published `(T, s)`. *Cost:* ≈ **0.5–1 h**, no new DNS, no new solver, no new mining. *Constraint:*
this is an instrument/diagnostic task; §3f rule 3 permits it here because U5 was construction, but
it cannot be followed by another one.

---

**Recommendation, for the user to rule on and not acted on.** **E, then B.** E is the cheapest
item on the list by an order of magnitude and it is the only one that addresses the mechanism U5
actually uncovered rather than adding attempts on top of it; B is the cheapest supply increase
that leaves the realization — and therefore the whole U3/U5 comparison — intact. A is dominated
by B. C is worth its own milestone but is aimed at a different target than the named rows, and
saying otherwise would misread §5's per-band count of 1. D is the most expensive and helps least
if H-hard is real.

**None of these has been started.**

### 9.1 A pre-committed reading landed on `main` while this run was in flight, and it fires

**This section was written after §9 and it amends §9.** While U5's attempts stage was still
running, a concurrent session committed `c67179e`, which promoted Lane R and — importantly —
**pre-committed how U5 was to be read, before any of its numbers were visible**. That is
exactly the discipline this programme is built on, so it binds here even though it arrived from
outside the unit, and it is answered rather than worked around. Its two branches:

> **(a)** A *lower* per-attempt convergence rate is the **predicted cost of stratification, not a
> failure** — U5 admits worse-scoring seeds on purpose. A rate at or above U3's 14% would suggest
> the stratification did not bind.
> **(b)** What decides U5 is **where the converged orbits sit in `|s|`**, not how many there are.
> If the rate falls **and** the converged orbits still cluster at small `|s|` despite a stratified
> pool, the bias is not (only) in the seed supply — it is in the **BASIN STRUCTURE**, i.e.
> large-shift orbits have intrinsically smaller Newton basins. That is a **finding rather than a
> null**; it points at `R3`/`R5` rather than at more seeds, and it makes `U4`/`G2` the interesting
> unit rather than a formality.

**(a) fired as predicted.** 9/100 against 14/100, with U5's in-band seeds worse by the score's own
metric (median `R` 0.2122 against 0.1897). The stratification bound.

**(b) FIRED, and it is this unit's finding.** The rate fell *and* the convergences still cluster
at small `|s|`: **8 of 9 below 0.15**, **4 of 5 in-band convergences left the band**, **5 distinct
solutions of which four sit at `|s| < 0.14`** (§6.4), with the matched-`R` comparison of §6.3
pointing the same way at `p = 0.073`. So **the bias is in the basin structure, not only in the seed
supply.**

**What that does to §9.** Options **A, B and D all buy supply**, and the pre-committed reading
points away from more seeds; they are **demoted**. **E is reinforced** — it is the option that
interrogates basin structure, and it is the cheapest on the list. **C is unaffected** and remains
aimed at `|s| > 0.9` rather than at the band. And **`U4`/`G2`, the basin radius**, becomes the unit
this result is really about, though it still cannot open: it needs a recovered *named* orbit to
perturb, and there is not one. §9's ordering is left standing as written, because the user rules on
it and rewriting a recommendation after seeing a reading would be the exact move this discipline
exists to prevent — but it should be read with A, B and D discounted.

**No third reading is constructed.** Both pre-committed branches are reported as they fired.

### 9.2 `R0`'s metric, computed here because `R0` fixed it before this unit landed

`c67179e` also made **distinct orbits per core-hour** the reported metric, per-attempt rate demoted
to a secondary diagnostic, on the grounds that per-attempt rate is inflatable by feeding easier
seeds — "exactly what U5 deliberately stops doing". Computed for U5, attempts stage only, like for
like with U3:

| | distinct orbits | core-hours (attempts) | **distinct / core-hour** |
|---|---|---|---|
| U3 | 8 (disputed, see below) | 144.69 | 0.0553 |
| **U5** | **5** | **57.04** | **0.0877** |

**Two cautions, both owed to `R0` and neither resolved here.** (i) `R0` baselines U3 at **134.45**
core-hours; `p2_prog_r4_g1_v1.json` gives 52,087.95 s × 10 workers = **144.69**, and `R0` should
reconcile the figure it baselines on before anything is measured against it. (ii) `R0` itself flags
U3's distinct count of 8 as unreconcilable with U3 §4's table; at 7 the baseline is 0.0484. U5 is
above U3 on every variant, and including U5's mining and control stages (68.91 core-hours total)
it is 0.0726, still above. **The comparison is provisional until `R0` lands**, and is recorded that
way rather than claimed.

## 10. Obligations and ceiling

- **Ceiling: TIER 2.** Unchanged, and stated here because every gate and milestone answer owes
  it. Nothing in this unit is a proof of anything.
- **No `L1 → L4` link moved.** Clay odds ~0.05%, unmoved. Nothing here is movement toward Clay.
- `CLAY_OBLIGATIONS.md` §6 obligations 1 and 2 — **OPEN**, no known method.
- `CLAY_OBLIGATIONS.md` §4 — **OPEN and not discharged**; stays open in every route-4 gate until
  leg 386 (ROUTE-DTOL) lands with a pre-registered δ mode (user ruling, 2026-08-12).

## 11. Artefacts

| What | Where |
|---|---|
| pre-registration (AMENDMENT 5) | `experiments/journal/prog_r4_u2u3_prereg_addendum.md` §3g, commit `4f6f33f` |
| mining stage | `experiments/programme_r4/u5_shift_mining.py` |
| attempts stage | `experiments/programme_r4/u5_stratified_attempts.py` |
| library reduction + its safety check | `experiments/programme_r4/u5_reduce_library.py` |
| curated record | `writeup/data/p2_prog_r4_m3_v1.json` |
| per-iteration ledger | `experiments/programme_r4/u5_m3_ledger.json` |
| committed seed library | `experiments/programme_r4/u5_shift_library_admissible.json` |
| figure | `writeup/figures/fig107_prog_r4_m3_shift_strata.py` / `.png` |
| run logs | `experiments/programme_r4/u5_mining_stdout.log`, `u5_attempts_stdout.log` |

The full 18 MB mined take is a **regenerable intermediate** and is gitignored beside the DNS
artefacts it derives from. What is committed reproduces the allocation exactly, and
`u5_reduce_library.py` **asserts** that rather than claiming it.
