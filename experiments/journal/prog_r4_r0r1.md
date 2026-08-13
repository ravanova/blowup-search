# PROG-R4 — units R0 + R1 (Lane R, wall W7)

**Unit:** R0 + R1, dispatched as one worker in CONDUCTOR mode (ORCHESTRATION.md §3g), wave 1.
**Branch:** `prog-r4/r0r1-metric`.
**Resourcing:** analysis of banked artefacts. ≈0 new compute. **No solver attempt was run, no DNS
step was taken, U5 was not re-run, and no additional seed supply is proposed.** Every number below
is arithmetic over fields that were already in the repository.
**Tier:** 2. No L1→L4 link moved. Clay stays ~0.05%.

Deliverables:

| file | what it is |
|---|---|
| `experiments/programme_r4/r0_metric.py` | the R0 re-derivation (20 checks) |
| `experiments/programme_r4/r1_flatness.py` | the R1 sweep on the banked ledgers (10 checks) |
| `writeup/data/p2_prog_r4_r0r1_v1.json` | the banked record, written by those two |
| `experiments/p2_prog_r4_r0r1_evidence.py` | rebuilds every prose number from the JSON (66 checks) |
| `writeup/figures/fig108_prog_r4_r0r1.py` | fig108, four panels (12 checks) |
| `writeup/4_p2_lottery/BLOG_P2_PROGR4_R0R1.md`, `TECHNICAL_P2_PROGR4_R0R1.md` | the write-up pair |

`writeup/build_figures.py` received exactly one additive line, registering fig108. Nothing else in
that file was touched.

---

## 0. Scope, quoted from `WALLS.md` rather than paraphrased

**R0**, from `WALLS.md` §LANE R:

> ### R0 — the metric, pre-committed BEFORE any optimisation
>
> **Per-attempt convergence rate is the wrong headline and must not be the reported one.** It is
> trivially inflated by feeding the solver easier seeds — which is precisely what U5 deliberately
> stops doing — and it counts a re-find of a known orbit as a success. **U3's own numbers show the
> problem: 14 convergences, but 10 of them landed on just three solutions.**
>
> **The reported metric is `DISTINCT ORBITS PER CORE-HOUR`,** with per-attempt rate retained as a
> secondary diagnostic and always alongside it.
>
> - **Core-hours.** This file first quoted **134.45** for U3. `p2_prog_r4_g1_v1.json` gives
>   52,087.95 s × 10 workers = **144.69**. Reconcile against the JSON, not against prose.
> - **The distinct count.** This file first argued U3's 8 was unreconcilable with its §4 table
>   (10 convergences over 3 replicated solutions, then 4 remaining cannot yield 5 more). **U5
>   measured it instead of arguing it** … **R0 reconciles against that script, not against this
>   paragraph** — and the lesson is the one this repository already knows: a count derived from
>   prose is not a measurement.

**R1**, verbatim:

> ### R1 — early abort on flatness. *Cheapest competitive win in the repository, and it is measured.*
>
> U3 measured convergence as **bimodal**: all 14 convergences finished in **≤29 epochs** (median 16),
> while the 86 non-convergences ran to the 52-epoch cap and were **flat there** — 53% reduced `‖R‖`
> by <1% over their final 10 epochs, 83% by <10%, only 3% still halving. **Those epochs are pure
> waste and they are the majority of the run.** A flatness criterion that kills an attempt and
> recycles its budget into a fresh seed converts wasted compute directly into extra attempts, with no
> change to the per-attempt rate and no change to the realization. Estimate the recoverable fraction
> from U3's banked ledger *before* building it, and plant a control that the criterion never kills an
> attempt that U3's ledger shows would have converged.

**Filename.** `WALLS.md` calls R1 "early abort on flatness". The commissioned filename
`r1_flatness.py` already matches that name, so **no rename was needed**; this is recorded because the
commission asked for the check to be made and stated either way.

**The sharpening.** A concurrent session (commit `5c6d495`) wrote both of U5's corrections into
`WALLS.md`'s prose. That is a transcription of U5's numbers, not an independent measurement — the
exact move this unit exists to catch. R0 therefore re-derived both figures from the artefacts and
reports agreement or disagreement below. **No figure in this journal is cited from `WALLS.md`.**

---

## 1. R0(i) — core-hours

Re-derived from `writeup/data/p2_prog_r4_g1_v1.json` and `p2_prog_r4_m3_v1.json` alone:

| | `magnitudes.wall_seconds`/3600 | × `magnitudes.workers` | Σ `attempts[].wall_seconds`/3600 | utilisation |
|---|---|---|---|---|
| U3 | 14.4689 h | **144.6888** | **134.4475** | 92.92% |
| U5 | 7.1294 h | **57.0352** | **56.0094** | 98.20% |

**AGREEMENT on the numbers. DISAGREEMENT on the diagnosis.**

`WALLS.md`'s 144.69 for U3 and 57.04 for U5 are **confirmed** — they are the pool reservation, wall
elapsed times workers, and my derivation reproduces them to five figures from the named fields.

But `WALLS.md` says of the earlier figure: *"This file first quoted 134.45 for U3 … Reconcile
against the JSON, not against prose."* **That is wrong, and it is wrong in the direction that
matters.** 134.4475 is *not* a prose number. It is `sum(attempts[].wall_seconds)/3600` from the very
same JSON — the total CPU time the 100 attempts actually consumed — and it is the figure U3's own
row in `writeup/INDEX.md` already carries ("14.47 h, 134.45 core-hours"). Two correct measurements
of two different quantities were treated as one measurement and one error.

The gap, 10.24 core-hours, is **straggler idle**: U3 reserved a 10-wide pool for 14.47 h but its
attempts only kept it 92.92% busy. U5's 98.20% is the imap_unordered/chunksize-1 scheduling
difference, not a solver difference.

**A caveat neither figure escapes.** The denominator is **worker-hours, not core-hours**, and the
two units did not reserve the same width (10 vs 8). A true machine-core-hour figure is **not
derivable from what is banked**: the physical core count appears in **no numeric field of either
JSON**. It appears only inside the prose string `resourcing.workers_note` in U5's file, which §3e
forbids me to use as a number. **Reported as a missing artefact; not estimated.** See
`CORRECTIONS FOR THE CONDUCTOR` (3) for what would have to be banked.

## 2. R0(ii) — the distinct count

The arbiter is `experiments/p2_prog_r4_m3_evidence.py` §5. Its rule is banked verbatim in
`r0.cluster_rule_verbatim`: greedy leader clustering of the convergences sorted by `T_converged`,
joining to a cluster iff **both** `|ΔT| ≤ TOL` and `|Δ wrap_abs(s)| ≤ TOL` against the cluster's
**first** member, with `TOL = 0.05` (the matching predicate of record, Ban 2) and
`wrap_abs(s) = min(a, 2π − a)`, `a = |s| mod 2π`.

I re-implemented that rule twice independently (once in `r0_metric.py`, once again in the evidence
script) rather than importing it, so that reproducing the count is a check and not a tautology.

**U3: 14 convergences → 8 distinct. U5: 9 → 5. AGREES with `WALLS.md` on both.**

| leader T | \|s\| | n | attempts | anchors |
|---|---|---|---|---|
| 16.524063 | 0.101863 | 4 | 20, 78, 80, 44 | UPO9, UPO17 |
| 16.810007 | 0.073009 | 1 | 99 | UPO17 |
| 16.874421 | 0.072938 | 3 | 12, 84, 43 | UPO9 |
| 17.165018 | 0.074073 | 1 | 98 | UPO9 |
| 17.349198 | 0.317371 | 1 | 61 | UPO22 |
| 19.284820 | 0.117770 | 2 | 76, 95 | UPO32 |
| 19.678710 | 0.085141 | 1 | 47 | UPO22 |
| 22.038920 | 0.134720 | 1 | 39 | UPO37 |

The count is not an artefact of the rule's greediness, which was the obvious way for it to be
fragile:

- **leader-greedy = single-linkage = complete-linkage = 8** (and = 5 for U5). The partition happens
  to be a genuine equivalence class on this data, so the non-transitive rule costs nothing here.
- **20,000 random input orderings** of the greedy rule: the only count ever observed is 8 (and 5).
- **Tolerance sweep** (U3): 0.01 → 11, 0.02–0.04 → 9, **0.05–0.10 → 8**, 0.15–0.20 → 7, 0.30 → 6.
  The "7" reading requires TOL = 0.15, three times the predicate of record.
- The count hinges on a narrow band in `T`: the **widest accepted merge** is attempts 12 & 43 at
  0.047969 = **0.959 × TOL**; the **narrowest failed merge** is attempts 12 & 99 at 0.064414 =
  **1.288 × TOL**, decided by `T` alone (their `|s|` differ by 7.1e-5).

**Where the "7" came from.** `WALLS.md`'s original argument — 10 convergences over 3 replicated
solutions leaves 4, which cannot yield 5 more — fails on its own input. **Measured: 9 of 14, not
10** (cluster sizes 4 + 3 + 2), leaving **5 singletons**, and 3 + 5 = 8 exactly. The count was never
in doubt; the prose's premise was off by one. The same "10 of 14" sentence is still live in
`WALLS.md` §R2 and in `STATE.md`. See `CORRECTIONS FOR THE CONDUCTOR` (1).

**Instrument limit, stated rather than glossed.** U3's converged states are **not banked anywhere**
in this repository — only U5's are, in `u5_m3_converged_orbits.npz` (9 fields). So U3's 8, which is
the headline numerator, can be tested only in the `(T, |s|)` invariant pair and never in state
space, and nothing banked can adjudicate the 1.288 × TOL pair. Even for U5 the npz banks one
snapshot per attempt at an unspecified phase along the orbit, so it cannot validate the rule either:
measured shift-invariant spectral distances put attempts 40 and 52 (**same** cluster) at 0.1992,
further apart than attempts 52 and 45 (**different** clusters) at 0.0888. Reported as an instrument
limit, not as support.

## 3. R0 — the finding the commission did not anticipate

The metric was introduced because per-attempt rate "counts a re-find of a known orbit as a success".
It removes that defect **within** a run. It does not remove it **between** runs, and I measured that
it bites:

- **57 of U5's 100 seeds are literally identical to seeds U3 had already spent**, matched on
  `(T_seed, s_seed, R_seed)` at full float precision.
- **5 of U5's 9 convergences are bit-identical re-executions of U3 attempts** — same
  `T_converged`, same `s_converged`, same `final_residual`, same `n_iters`. U5 att40 = U3 att80,
  att64 = U3 att12, att74 = U3 att39, att76 = U3 att43, att77 = U3 att44. All five U3 attempts had
  already converged.
- **One of U5's five distinct solutions was reached only by re-running U3's seeds**: on U5-only
  seeds the count is 4, not 5.
- Comparing U5's five clusters against U3's eight under the same rule, **four are re-finds**.
  U5 gained **one** orbit new to the programme: T = 20.4175, |s| = 0.5867, attempt 7, anchor UPO37.

So there are two readings, and they point opposite ways:

| reading | U3 | U5 | U5 / U3 |
|---|---|---|---|
| per-run, pool reservation (the headline) | 0.0553 | 0.0877 | **1.59×** |
| per-run, attempt CPU | 0.0595 | 0.0893 | 1.50× |
| per-run, elapsed wall-hours | 0.5529 | 0.7013 | 1.27× |
| **cumulative — orbits new to the programme** | 0.0553 | **0.0175** | **0.32×, i.e. 3.15× worse** |

## 4. R1 — early abort on flatness

**The premise first, checked rather than taken.** `WALLS.md`'s flatness figures are **confirmed
exactly**: all 86 non-convergences ran to `n_iters` = 51 (52 residuals, the cap); over their final
10 epochs **53%** reduced `‖R‖` by <1%, **83%** by <10%, **3%** were still halving. Its
convergence figures are also confirmed: max 29 epochs, **median 16**. Only 243 of U3's 4,629 epochs
(5.2%) sit inside a convergence.

**The criterion family** (deterministic, and see §6): abort at epoch `k` iff `k ≥ K` and
`‖R‖_k > θ · ‖R‖_{k−W}`. Evaluated by **replaying** the banked `residual_history` of all 200
attempts. Two controls: (1) **zero false kills** — the rule must abort none of the 23 banked
convergences; (2) **safety margin factor** = `θ` divided by the worst window ratio any banked
convergence actually exhibited where the rule looks, i.e. how many times worse a future convergence
could behave before dying.

**The incumbent already exists.** U5's banked `resourcing.stall_exit.rule` is
"from epoch 20, stop if ‖R‖_k > 0.5 · ‖R‖_(k−10)" — exactly `(K, W, θ) = (20, 10, 0.5)`. Replayed
independently on U3 it gives **exactly 2,083 epochs**, matching U5's banked `u3_epochs_under_rule`
to the epoch, with **0 false kills** and a margin factor of **6.9016**, matching U5's banked
`margin_factor` to nine decimals.

| | epochs | under the rule | recovered | aborted | false kills | core-hours saved |
|---|---|---|---|---|---|---|
| U3 | 4,629 | 2,083 | **55.0%** | 86 | 0 | **74.87** of 134.4475 (55.7%) |
| U5 | 2,104 | 2,104 | 0.0% | 0 | 0 | 0.00 — already deployed there |

**So the "cheapest competitive win in the repository" has already been collected, by U5, before R1
was commissioned.** R1's own question is therefore the one worth asking: *is there anything left in
it?*

**The sweep.** 12,597 rules (`K ∈ [2,40] × W ∈ [2,20] × 17 thresholds`), scored on both banked
ledgers. **9,760 kill no banked convergence.** Ranked by U3 epochs recovered at each safety floor:

| min margin | best rule | U3 recovered | margin |
|---|---|---|---|
| none | (2, 9, 0.45) | 65.3% | **1.09×** — REJECTED |
| ≥ 2 | (17, 16, 0.15) | 58.8% | 2.33× |
| ≥ 6.9016 (the deployed margin) | **(21, 10, 0.10)** | **55.45%** | 9.95× |
| ≥ 15 | (21, 10, 0.20) | 55.41% | 19.91× |

**The headroom over the deployed rule, at no loss of safety margin, is +0.45 percentage points =
+0.48 core-hours on a 134-core-hour run.** The 65.3% rules exist but sit at a 1.09× margin: a future
convergence behaving 9% worse than the worst banked one dies under them, and taking the maximum of a
statistic over 12,597 rules against 23 convergences is exactly how one overfits a stopping rule.

**Hold-out both ways** — a control `WALLS.md` did not ask for, and the one that decides whether any
of this generalises. At the deployed margin floor:

- **fit on U3 → scored on U5**: (20, 8, 0.55), 55.9% of U3 recovered; held out on U5, 2.1%
  recovered and **0 false kills**. PASSES.
- **fit on U5 → scored on U3**: (17, 13, 0.15), 17.0% of U5 recovered; held out on U3, 61.6%
  recovered but **1 FALSE KILL** — it aborts an attempt U3's ledger shows converged. **FAILS.**

The asymmetry *is* the result: nine convergences are not enough to fix a stopping rule, and the
direction that fails is the one with the smaller fitting set. Any future tuning of this family must
select on the larger ledger and score on the smaller, never the reverse.

**R1 closes.** The saving is real, it is 74.87 core-hours on U3's ledger at zero false kills, and it
is already banked. What remains in this criterion family is half a percentage point and a
demonstrated generalisation failure. No further compute should be spent on it.

**The projection, labelled.** U3 replayed under the rule finds the **same 8** distinct orbits in
59.5736 rather than 134.4475 attempt-CPU core-hours:
**PROJECTED 0.1343 distinct orbits per core-hour**, against the measured 0.0595 —
**PROJECTED, 2.26×**. It is a replay, not a run. **No recycled-budget orbit yield is reported**:
R0 measured that U5 spent 57.04 core-hours to gain one orbit new to the programme, so the assumption
that recovered budget converts at the observed rate is optimistic and is not made here.

---

## 5. THE GATES

> **R0 gate:** Are the programme's two headline figures — total core-hours and distinct-orbit count —
> **re-derived independently from the banked artefacts**, each with the derivation shown, and each
> reported as agreeing or disagreeing with the figure currently in `WALLS.md`?
> **yes →** the corrected metric is stated in the form "N distinct orbits per core-hour", with N's
> numerator and denominator each traceable to a named artefact field.

**YES.** Both were re-derived independently, from the artefacts, with the derivation shown in §1–§2
and re-executed by `experiments/p2_prog_r4_r0r1_evidence.py`.

- **Total core-hours: AGREE** with `WALLS.md`'s 144.69 (U3) and 57.04 (U5). **DISAGREE** with its
  account of the earlier 134.45, which is not prose but `Σ attempts[].wall_seconds/3600` from the
  same JSON; both are correct measurements of different quantities.
- **Distinct-orbit count: AGREE** — 8 for U3 and 5 for U5. **DISAGREE** with the prose premise
  `WALLS.md` used to doubt it: "10 of U3's 14 convergences landed on just three solutions" is
  measured as **9**.

The corrected metric, in the gate's own form:

> **U3 achieved 0.0553 distinct orbits per core-hour.**
> Numerator **8** = the number of clusters of `attempts[].{T_converged, s_converged}` in
> `writeup/data/p2_prog_r4_g1_v1.json` under `p2_prog_r4_m3_evidence.py` §5's rule at TOL = 0.05.
> Denominator **144.6888** = `magnitudes.wall_seconds` (52087.95185184479) ×
> `magnitudes.workers` (10) / 3600.
>
> **U5 achieved 0.0877 distinct orbits per core-hour.**
> Numerator **5**, same field and same rule, from `writeup/data/p2_prog_r4_m3_v1.json`.
> Denominator **57.0352** = `magnitudes.wall_seconds` (25665.83147907257) ×
> `magnitudes.workers` (8) / 3600.
>
> Both denominators are strictly **worker-hours**; the physical core count is not a banked numeric
> field and is not estimated.

> **R1 gate:** Is R1, as `WALLS.md`'s Lane R defines it, executed to a **measured** number on the
> banked data, with its saving expressed as a **compute** quantity?
> **yes →** state the measured saving and the data it was measured on.

**YES.** Measured on U3's banked ledger — `writeup/data/p2_prog_r4_g1_v1.json`, the
`residual_history` of all 100 attempts, replayed with no re-run. The criterion
"from epoch 20, stop if ‖R‖_k > 0.5 · ‖R‖_(k−10)" recovers **55.0% of U3's 4,629 epochs
(4,629 → 2,083)**, which is **74.87 of its 134.4475 attempt-CPU core-hours (55.7%)**, at **zero
false kills** over 23 banked convergences and a **6.90× safety margin**.

**With the correction that the saving is U5's, not R1's** — U5 built and deployed this rule before
R1 was commissioned. R1's own measured contribution is the search that closes the unit: over 12,597
deterministic rules, 9,760 of them admissible, the best rule that does not degrade the deployed
safety margin recovers **+0.45 percentage points = +0.48 core-hours** more.

## 6. Pre-committed branches, and which fired

- **(a) FIRED.** R0 was licensed to retract "Lane R's first measured win" outright. **The inference
  is retracted.** The arithmetic stands: U5 is above U3 under all three derivable core-hour
  conventions, 1.27× to 1.59×. What does not stand is reading that as Lane R's machinery having
  improved. The metric is per-run; the two runs are not independent samples — 57% of U5's seeds were
  U3's, and 5 of its 9 convergences are bit-identical re-executions of U3 attempts; and on the only
  reading that tracks what the programme actually gained, U5 is 3.15× worse. **Lane R may claim a
  cheaper run. It may not claim a better orbit finder on this evidence.**
- **(b) DID NOT FIRE, and its prohibition is honoured anyway.** The count did not resolve to 7 — it
  is 8, robustly. The margin did not widen. Nothing in this unit is reported as strengthening the
  result; the one place the correction flatters the programme (the 55.0% saving is larger than a
  first reading of "estimate the recoverable fraction" might have suggested) is reported as U5's
  already-banked saving, not as R1's win.
- **(c) FIRED.** R1's saving is compute. The single projected quantity carries the literal label
  **PROJECTED** in this journal, in `r1.projection` in the JSON, in fig108's panel C, and in both
  write-ups. No recycled-budget orbit yield is reported at all.
- **(d) FIRED, and is stated in its own terms.** Tier 2 is never a proof. **A best-in-field orbit
  finder does not move a Clay link — it makes the questions affordable, which is a DIFFERENT AND
  LESSER THING.** Clay stays ~0.05%. This sentence appears in `r0.verdict.ceiling`,
  `r1.verdict.ceiling`, and both write-ups.
- **(e) COMPLIANCE CONFIRMED EXPLICITLY.** Leg 349's ban on learned or evolved seed-scoring fitness
  is in force and is respected. The R1 criterion is three fixed constants and a comparison of two
  banked residuals: **no learned or evolved fitness, no scoring of seeds, no stochastic component,
  and it does not touch seed selection at all** — it only changes when an already-launched attempt
  stops. Replaying it on the ledger is exactly reproducible. R0 touches no scoring of any kind; its
  only randomness is 20,000 shuffles used to *stress* a deterministic clustering rule, seeded at
  20260813, and the result is invariant. Nothing in this unit is a GA, is fitted against seed
  quality, or produces a score a future unit could rank seeds by.

## 7. Lesson 91 — what the negatives name

The retraction in (a) is a negative and names its three parts. **Realization:** PROG-R4's Newton–
GMRES–hookstep solver on the DSS/Kolmogorov flow at the banked Re and resolution, extended residual
carrying `T` and continuous shift `s`. **Trial space:** the two banked 100-attempt runs, U3's
globally-ranked seed budget and U5's |s|-stratified one, drawn from the same anchored admissible
pool. **Basis:** the metric is per-run and the runs overlap in 57 seeds; a cross-run re-find scores
as a success, so a between-run comparison of per-run distinct-orbit yield does not measure a change
in the finder. It is a negative about the *comparison*, not about either run.

The hold-out failure in §4 is a negative too. **Realization:** the abort family
`k ≥ K ∧ ‖R‖_k > θ‖R‖_{k−W}` replayed on banked residual histories. **Trial space:** 12,597 rules,
selected on one unit's ledger and scored on the other's. **Basis:** selection on U5's 9
convergences yields a rule that kills one of U3's 14. The family is usable; selection on the smaller
ledger is not.

## 8. What this unit did NOT do

- Did not run a solver attempt, a DNS step, or any mining. Nothing was re-run.
- Did not re-run U5 (explicit standing prohibition), and does not propose more seed supply for
  PROG-R4.
- Did not edit `STATE.md`, `WALLS.md`, `DIRECTION.md`, `plan_of_record.py`, any `u*.py`, any banked
  ledger, `p2_prog_r4_g1_v1.json`, `p2_prog_r4_m3_v1.json`, `u5_m3_converged_orbits.npz`, or
  `p2_prog_r4_m3_evidence.py`. `DIRECTION.md` was not read.
- Did not touch a gate answer. G1 stays **UNDER-RESOURCED**; M3 stays **DELIVERED**.
- Did not estimate the missing machine-core figure. It is reported as missing.
- No external outreach (standing user hold).

---

## CORRECTIONS FOR THE CONDUCTOR

Written here verbatim and **applied nowhere**. These are for the Conductor to land or reject.

**(1) `WALLS.md` §R0 and §R2, and `STATE.md`: "10 of U3's 14 convergences landed on three
solutions" should read NINE.**
Measured from `p2_prog_r4_g1_v1.json` under `p2_prog_r4_m3_evidence.py` §5's rule: the replicated
clusters have sizes **4 + 3 + 2 = 9**, and there are **5** singletons. This is the premise
`WALLS.md` §R0 used to argue that 8 was unreconcilable ("10 convergences over 3 replicated
solutions, then 4 remaining cannot yield 5 more"); with the correct 9, 3 + 5 = 8 and the arithmetic
closes. §R2's opening sentence carries the same number and the same error. R2's *conclusion* —
that replication is the largest waste after R1 — is unaffected: 9 of 14 is still the majority.

**(2) `WALLS.md` §R0's characterisation of the 134.45 figure is wrong.**
It reads: *"This file first quoted **134.45** for U3. `p2_prog_r4_g1_v1.json` gives 52,087.95 s ×
10 workers = **144.69**. Reconcile against the JSON, not against prose."* 134.4475 **is** from the
JSON — it is `Σ attempts[].wall_seconds / 3600`, the attempt CPU time — and it is the figure U3's
own row in `writeup/INDEX.md` reports ("14.47 h, 134.45 core-hours"). Both numbers are correct
measurements of different quantities: pool reservation vs attempt CPU. The gap is U3's 92.92% pool
utilisation against U5's 98.20%. **Nothing was derived from prose here**, and the "not against
prose" framing mislabels a real second measurement as a defect. §W7's "`PROG-R4` U3 spent **134.45
core-hours**" is likewise correct under the attempt-CPU convention and needs a convention label
rather than a replacement number.

**(3) The metric's denominator is worker-hours, not core-hours, and the physical core count is not
a banked field.**
U3 reserved 10 workers, U5 reserved 8, so "core-hours" as currently reported is
`wall × workers`. The machine's physical core count appears in **no numeric field** of either unit
JSON; it exists only inside the prose string `resourcing.workers_note` in `p2_prog_r4_m3_v1.json`,
which §3e forbids using as a number. **To make a true machine-core-hour figure derivable, a future
unit must bank `magnitudes.physical_cores` (and ideally per-attempt CPU time, e.g.
`time.process_time`, alongside `wall_seconds`).** Until then the metric compares two different
reservation widths on one machine, and the honest label on the axis is "worker-hours". I have not
estimated it.

**(4) The metric still counts cross-run re-finds as successes, one level above the defect it was
introduced to remove.**
`WALLS.md` §R0 adopts distinct-orbits-per-core-hour because per-attempt rate "counts a re-find of a
known orbit as a success". Measured: **57 of U5's 100 seeds are identical to seeds U3 had already
spent** (matched on `(T_seed, s_seed, R_seed)`), **5 of U5's 9 convergences are bit-identical
re-executions of U3 attempts**, **4 of U5's 5 distinct solutions are re-finds of U3's**, and on
U5-only seeds the count is **4, not 5**. U5's contribution new to the programme is **one** orbit.
Consequence for §R0's table: the "U5 is above U3 on every variant — Lane R's first measured
improvement" line is true per-run (1.27×–1.59×) and reverses under the cumulative reading
(0.0175 vs 0.0553, **3.15× worse**). Suggested repair: report **both** rows, and make the standing
metric "orbits new to the programme per core-hour" for cross-unit comparisons, keeping the per-run
figure as the within-unit diagnostic. **The claim "Lane R's first measured improvement" should be
withdrawn as an inference**; the arithmetic behind it is confirmed.

**(5) `WALLS.md` §R1's own numbers are CONFIRMED, and R1 should be marked closed.**
"all 14 convergences ≤29 epochs (median 16)", "53% / 83% / 3%" over the final 10 epochs of the 86
stalls — all confirmed exactly. But R1's headline, *"Cheapest competitive win in the repository, and
it is measured"*, describes a win **U5 already collected**: `resourcing.stall_exit` in
`p2_prog_r4_m3_v1.json` is exactly this criterion, deployed. The remaining headroom at no loss of
safety margin is **+0.45 percentage points**. Suggested amendment: mark R1 **CLOSED — collected by
U5, headroom measured at +0.45 pp / +0.48 core-hours, hold-out shows selection on the smaller ledger
kills a real convergence**, and spend no further compute on the family.

**(6) A missing artefact that limits any future distinct-count audit.**
U3's converged states are not banked anywhere; only U5's are. The headline numerator (8) can
therefore only ever be tested in the `(T, |s|)` pair, and the pair that decides it sits at
1.288 × TOL. And U5's own npz banks one snapshot per attempt at an unspecified orbital phase, so it
cannot validate the rule either (measured: same-cluster distance 0.1992 exceeds a cross-cluster
0.0888). Banking U3's 14 converged states plus a phase-aligned distance would settle it — but that
needs the stepper, i.e. new compute, and is not proposed here.
