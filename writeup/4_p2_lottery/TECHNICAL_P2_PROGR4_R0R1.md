# PROG-R4 R0 + R1 — the metric re-derived, and the flatness abort measured

**Unit:** PROG-R4 R0 + R1, Lane R (reformulation for scale and solver competitiveness), wall **W7**.
Dispatched as one worker in CONDUCTOR mode (`ORCHESTRATION.md` §3g), wave 1.
**Mode:** §3f SOLO. **UNVERIFIED** — produced and checked in one session, no paired verifier.
**Kind:** MEASUREMENT over banked artefacts. **≈0 new compute**: no solver attempt, no DNS step, no
mining, nothing re-run. U5 was not re-run (standing prohibition) and no additional seed supply is
proposed.
**Data of record:** `writeup/data/p2_prog_r4_r0r1_v1.json`, written by
`experiments/programme_r4/r0_metric.py` (20/20) and `experiments/programme_r4/r1_flatness.py`
(10/10).
**Read-only inputs:** `writeup/data/p2_prog_r4_g1_v1.json` (U3), `writeup/data/p2_prog_r4_m3_v1.json`
(U5), `experiments/programme_r4/u5_m3_converged_orbits.npz`, and
`experiments/p2_prog_r4_m3_evidence.py` §5 as the arbiter of "distinct". SHA-256 of all three data
artefacts is banked in `r0.provenance`.
**Evidence:** `experiments/p2_prog_r4_r0r1_evidence.py`, **66/66** — rebuilds every number below
from the JSON and cross-checks the load-bearing ones back against the two unit JSONs.
**Figure:** fig108, 12/12 checks.
**Journal:** `experiments/journal/prog_r4_r0r1.md`.

> **NO GATE IS RE-ANSWERED HERE.** G1 stays `UNDER-RESOURCED` as banked in
> `p2_prog_r4_g1_v1.json`; M3 stays `DELIVERED` as banked in `p2_prog_r4_m3_v1.json`. Neither file
> is written to by this unit.

> **TIER 2. CEILING CLAUSE.** No L1→L4 link moved. **A best-in-field orbit finder does NOT move a
> Clay link — it makes the questions affordable, which is a DIFFERENT AND LESSER THING.** Clay stays
> ~0.05%.

---

## 1. Why the unit exists, and why the obvious answer was not acceptable

`WALLS.md` §LANE R fixes the reported metric as **`DISTINCT ORBITS PER CORE-HOUR`**, with per-attempt
rate demoted to a secondary diagnostic, on the ground that per-attempt rate "is trivially inflated by
feeding the solver easier seeds … and it counts a re-find of a known orbit as a success."

Two figures behind that metric were in dispute — U3's core-hours (134.45 vs 144.69) and U3's
distinct count (8 vs 7). A concurrent session (commit `5c6d495`) had already written both
resolutions into `WALLS.md`'s prose. **Those resolutions are a transcription of U5's own numbers,
not an independent measurement** — the same move this unit exists to catch. R0 therefore re-derived
both figures from the artefacts under `ORCHESTRATION.md` §3e ("re-derive every number from
`writeup/data/*.json` and the banked ledgers, NEVER from prose") and reports agreement or
disagreement. **No figure in this document is cited from `WALLS.md`.**

---

## 2. R0(i) — core-hours

All four quantities from named fields of the two unit JSONs:

| | `magnitudes.wall_seconds` / 3600 | × `magnitudes.workers` | Σ `attempts[].wall_seconds` / 3600 | utilisation |
|---|---|---|---|---|
| U3 | 14.4689 h | **144.6888** | **134.4475** | 0.9292 |
| U5 | 7.1294 h | **57.0352** | **56.0094** | 0.9820 |

**Verdict: AGREE on the numbers, DISAGREE on the diagnosis.**

`WALLS.md`'s current 144.69 (U3) and 57.04 (U5) are confirmed:
`52087.95185184479 × 10 / 3600 = 144.6888` and `25665.83147907257 × 8 / 3600 = 57.0352`.

`WALLS.md` further states: *"This file first quoted 134.45 for U3 … Reconcile against the JSON, not
against prose."* **That characterisation is wrong.** 134.4475 is `Σ attempts[].wall_seconds / 3600`
over the 100 attempt rows of the same JSON — the attempt CPU time — and it is the figure U3's own
row in `writeup/INDEX.md` already carries ("14.47 h, 134.45 core-hours"). Nothing here was derived
from prose. The two figures are the **pool reservation** and the **attempt CPU**; the 10.2413
core-hour difference is straggler idle at 92.92% pool utilisation, against U5's 98.20% under
`imap_unordered` with `chunksize=1`. Both are correct measurements of different quantities and both
should be retained, with a convention label.

**Missing artefact, reported not estimated (§3d).** The denominator is strictly **worker-hours**:
U3 reserved 10, U5 reserved 8. The machine's physical core count appears in **no numeric field of
either JSON**; it exists only inside the prose string `resourcing.workers_note` in U5's file, which
§3e forbids using as a number. A machine-core-hour figure is therefore **not derivable from what is
banked**, and is not estimated. What would have to be banked: `magnitudes.physical_cores`, and
ideally per-attempt CPU time (`time.process_time`) alongside `wall_seconds`.

---

## 3. R0(ii) — the distinct count

### 3.1 The rule, verbatim from the arbiter

`experiments/p2_prog_r4_m3_evidence.py` §5 is the arbiter named in the commission. Its rule, banked
verbatim in `r0.cluster_rule_verbatim`:

```python
# Lucas & Kerswell 2015 Table IV: the |s| band the eight named rows live in.
BAND = (0.295, 0.707)
# The matching predicate of record (Ban 2): a convergence is a recovery only if
# it matches a named row on BOTH T and s to within this. Reused here as the
# clustering tolerance, so "distinct" is never finer than "recovered".
TOL = 0.05

def wrap_abs(s):
    """|s| on the circle: the domain is 2*pi periodic, so |s|=6.18 is 0.10."""
    a = abs(float(s)) % (2.0 * math.pi)
    return min(a, 2.0 * math.pi - a)

def cluster(attempts):
    """Group convergences into distinct solutions at the matching tolerance."""
    out = []
    for a in sorted(attempts, key=lambda a: a["T_converged"]):
        for c in out:
            if (abs(c[0]["T_converged"] - a["T_converged"]) <= TOL
                    and abs(c[0]["S"] - a["S"]) <= TOL):
                c.append(a)
                break
        else:
            out.append([a])
    return out
```

It is a **greedy leader** rule: each point is compared only against `c[0]`, the cluster's first
member. That is not an equivalence relation in general, so reproducing its output is not by itself
enough. The rule was re-implemented independently twice (in `r0_metric.py` and again in the evidence
script) rather than imported, so agreement is a check and not a tautology.

### 3.2 The result

**U3: 14 convergences → 8 distinct. U5: 9 → 5. AGREES with `WALLS.md` on both.**

| leader `T` | `wrap_abs(s)` | n | attempts | anchors |
|---|---|---|---|---|
| 16.524063 | 0.101863 | 4 | 20, 78, 80, 44 | UPO9, UPO17 |
| 16.810007 | 0.073009 | 1 | 99 | UPO17 |
| 16.874421 | 0.072938 | 3 | 12, 84, 43 | UPO9 |
| 17.165018 | 0.074073 | 1 | 98 | UPO9 |
| 17.349198 | 0.317371 | 1 | 61 | UPO22 |
| 19.284820 | 0.117770 | 2 | 76, 95 | UPO32 |
| 19.678710 | 0.085141 | 1 | 47 | UPO22 |
| 22.038920 | 0.134720 | 1 | 39 | UPO37 |

### 3.3 Robustness

| stress | U3 | U5 |
|---|---|---|
| greedy leader (as implemented) | 8 | 5 |
| single-linkage (transitive closure of the same predicate) | 8 | 5 |
| complete-linkage (join only within TOL of *every* member) | 8 | 5 |
| 20,000 random input orderings of the greedy rule | only 8 observed | only 5 |

The partition is a genuine equivalence class here, so the rule's greediness costs nothing on this
data. Tolerance sweep (U3): 0.01 → 11, 0.02–0.04 → 9, **0.05–0.10 → 8**, 0.15–0.20 → 7, 0.30 → 6.
The "7" reading requires TOL = 0.15, three times the predicate of record.

**Where the count is decided.** Widest **accepted** merge: attempts 12 & 43, Chebyshev distance
0.047969 = **0.959 × TOL**. Narrowest **failed** merge: attempts 12 & 99, 0.064414 =
**1.288 × TOL**, decided by `T` alone (their `|s|` differ by 7.13e-5). The count 8 lives in the band
[0.0480, 0.0644].

### 3.4 The prose error, located

`WALLS.md` §R0's argument for doubting the 8 was: *"10 convergences over 3 replicated solutions,
then 4 remaining cannot yield 5 more."* Measured: **9**, not 10 — cluster sizes 4 + 3 + 2 — with
**5** singletons. 3 + 5 = 8 and the arithmetic closes. The same "10 of U3's 14 convergences landed
on three solutions" sentence is still live in `WALLS.md` §R2 and in `STATE.md`. R2's conclusion is
unaffected (9 of 14 is still the majority).

### 3.5 Instrument limit

U3's converged **states** are not banked anywhere in this repository. Only U5's are, in
`u5_m3_converged_orbits.npz` (9 fields, each `(24,24) float64`). So U3's 8 — the headline numerator
— can be tested only in the `(T, |s|)` invariant pair, never in state space, and nothing banked can
adjudicate the 1.288 × TOL pair.

Even for U5 the npz cannot validate the rule: it banks **one snapshot per converged attempt at an
unspecified phase along the orbit**, so two snapshots of the same orbit need not be close. Measured
shift-invariant `|FFT2|` relative distances: attempts 64 and 76 (**same** cluster) 0.0014, attempts
40 and 52 (**same** cluster) **0.1992**, attempts 52 and 45 (**different** clusters) **0.0888**. A
same-cluster distance exceeding a cross-cluster one is reported here as an instrument limit, not as
support for or against the count. Settling it would need U3's 14 states plus a phase-aligned
distance minimised over the continuous shift and over time-translation — i.e. the stepper, i.e. new
compute. Not proposed.

---

## 4. R0(iii) — the seed overlap, and what it does to the metric

Not previously measured anywhere. Seeds matched on `(T_seed, s_seed, R_seed)` at full float
precision:

- **57 of U5's 100 seeds had already been spent by U3.**
- **5 of U5's 9 convergences sit on those seeds, and all 5 are bit-identical re-executions** — same
  `T_converged`, `s_converged`, `final_residual` and `n_iters` as the U3 attempt. U5 att40 = U3
  att80; att64 = U3 att12; att74 = U3 att39; att76 = U3 att43; att77 = U3 att44. All five U3
  attempts had themselves converged.
- **On U5-only seeds the distinct count is 4, not 5.** One of U5's five solutions was reached only
  by re-running seeds U3 had already spent.
- Clustering U5's five against U3's eight under the same rule, **four are re-finds**. U5's
  contribution new to the programme is **one** orbit: `T = 20.4175`, `|s| = 0.5867`, attempt 7,
  anchor UPO37.

**The metric therefore still counts a re-find as a success — one level up.** It removes the defect
within a run and not between runs, which is the level at which `WALLS.md`'s comparison is made.

| reading | U3 | U5 | U5 / U3 |
|---|---|---|---|
| pool reservation (headline) | 0.055291 | 0.087665 | **1.586×** |
| attempt CPU | 0.059503 | 0.089271 | 1.500× |
| elapsed wall-hours | 0.552911 | 0.701322 | 1.268× |
| **cumulative — orbits new to the programme** | 0.055291 | **0.017533** | **0.317×** (3.15× worse) |

### The retraction

**`WALLS.md`'s "U5 is above U3 on every variant — Lane R's first measured improvement" is RETRACTED
AS AN INFERENCE.** The arithmetic is confirmed: U5 is above U3 under all three derivable core-hour
conventions, 1.27× to 1.59×, direction robust, magnitude not. What does not stand is reading that as
Lane R's machinery having improved. The metric is per-run; the two runs are not independent samples
(57% seed overlap, 5 of 9 convergences bit-identical); and on the reading that tracks what the
programme actually gained, U5 is 3.15× worse. **Lane R may claim a cheaper run. It may not claim a
better orbit finder on this evidence.**

Retracting this was pre-committed as an allowed and expected outcome (branch (a)), and it fired.
Branch (b) — the prohibition on reporting a correction that flatters the programme as a win — did
not arise (the count did not resolve to 7) and is honoured anyway: nothing in this unit is reported
as strengthening the result.

---

## 5. R1 — early abort on flatness

`WALLS.md`'s name for the unit is "**R1 — early abort on flatness**", so the commissioned filename
`r1_flatness.py` already matches and **was not renamed**.

### 5.1 The premise, checked rather than taken

All of `WALLS.md` §R1's stated numbers are **CONFIRMED** from `residual_history` directly:

- all 14 U3 convergences finished in **≤ 29** epochs, **median 16** (`n_iters` =
  10,10,10,10,12,14,15,17,17,22,23,26,28,29);
- all **86** non-convergences ran to `n_iters` = 51 (52 residuals, the cap);
- over their final 10 epochs, **53%** reduced `‖R‖` by <1%, **83%** by <10%, **3%** were still
  halving.

Only **243 of U3's 4,629 epochs (5.2%)** sit inside a convergence.

### 5.2 The criterion family, and its determinism

> abort at epoch `k` **iff** `k ≥ K` **and** `‖R‖_k > θ · ‖R‖_{k−W}`

Three fixed constants and a comparison of two banked residuals, evaluated by **replaying**
`residual_history` for all 200 banked attempts.

**Leg 349 ban — compliance confirmed explicitly.** No learned or evolved seed-scoring fitness
appears anywhere in this unit. The criterion has no fitness, no scoring of seeds, no stochastic
component, and **does not touch seed selection at all** — it changes only the stopping time of an
already-launched attempt. Replaying it is exactly reproducible. R0's only randomness is 20,000
shuffles (seeded 20260813) used to *stress* a deterministic clustering rule, and the result is
invariant. Nothing here is a GA, is fitted against seed quality, or yields a score a future unit
could rank seeds by.

### 5.3 The controls

1. **Zero false kills** (asked for by `WALLS.md`): the rule must abort none of the 23 banked
   convergences.
2. **Safety margin factor**: `θ` divided by the worst window ratio `‖R‖_k / ‖R‖_{k−W}` any banked
   convergence actually exhibited where the rule looks. Zero false kills over 23 examples is a weak
   statement on its own; this quantifies how much worse a future convergence could behave.
3. **Hold-out both ways** (added by this unit): select on one unit's ledger, score on the other's.

### 5.4 The incumbent already exists

U5's banked `resourcing.stall_exit.rule` is "from epoch 20, stop if ‖R‖_k > 0.5 · ‖R‖_(k−10)" —
exactly `(K, W, θ) = (20, 10, 0.5)`.

| | epochs | under the rule | recovered | aborted | false kills | attempt-CPU saved |
|---|---|---|---|---|---|---|
| U3 | 4,629 | **2,083** | **55.00%** | 86 | **0** | **74.87** of 134.4475 (55.69%) |
| U5 | 2,104 | 2,104 | 0.00% | 0 | 0 | 0.00 (already deployed there) |

Replayed independently, it reproduces U5's banked `u3_epochs_under_rule = 2083` **to the epoch** and
its banked `margin_factor = 6.901609656627281` **to nine decimals** (`θ = 0.5` against a worst banked
convergence window ratio of 0.072447).

**So the "cheapest competitive win in the repository" was already collected, by U5, before R1 was
commissioned.**

### 5.5 The sweep, and the headroom

12,597 rules (`K ∈ [2,40] × W ∈ [2,20] × 17 thresholds`), scored on both banked ledgers.
**9,760 kill no banked convergence.** Best U3 recovery at each safety floor:

| min margin factor | rule (K, W, θ) | U3 epochs recovered | margin |
|---|---|---|---|
| none | (2, 9, 0.45) | 65.35% | **1.09×** — REJECTED |
| ≥ 2 | (17, 16, 0.15) | 58.76% | 2.33× |
| ≥ 3 | (17, 16, 0.20) | 57.12% | 3.11× |
| **≥ 6.9016** (the deployed margin) | **(21, 10, 0.10)** | **55.45%** | **9.95×** |
| ≥ 15 | (21, 10, 0.20) | 55.41% | 19.91× |

**HEADROOM over the deployed rule, at no loss of safety margin: +0.45 percentage points =
+0.48 core-hours** on a 134.45 core-hour run.

The unconstrained optimum is **rejected**: zero false kills but a 1.09× margin, i.e. a future
convergence behaving 9% worse than the worst banked one dies under it. Taking the maximum of a
statistic over 12,597 rules against 23 convergences is exactly how a stopping rule is overfitted.

### 5.6 Hold-out both ways — the control that decides it

At the deployed margin floor (≥ 6.9016 on the fitting set):

| direction | selected rule | on the fitting set | held out | false kills held out |
|---|---|---|---|---|
| fit U3 → score U5 | (20, 8, 0.55) | 55.93% of U3 | 2.14% of U5 | **0 — PASSES** |
| fit U5 → score U3 | (17, 13, 0.15) | 17.02% of U5 | 61.57% of U3 | **1 — FAILS** |

The asymmetry is the result. Nine convergences are not enough to fix a stopping rule, and the
direction that fails is the one with the smaller fitting set. Any future tuning of this family must
select on the larger ledger and score on the smaller, never the reverse.

### 5.7 Lesson 91 — the negatives, named

**Negative 1 (the retraction, §4).** *Realization:* PROG-R4's Newton–GMRES–hookstep solver on the
DSS/Kolmogorov flow at the banked `Re` and resolution, extended residual carrying `T` and continuous
shift `s`. *Trial space:* the two banked 100-attempt runs — U3's globally-ranked seed budget and
U5's `|s|`-stratified one — drawn from the same anchored admissible pool. *Basis:* the metric is
per-run and the runs overlap in 57 seeds, so a between-run comparison of per-run distinct-orbit
yield does not measure a change in the finder. A negative about the *comparison*, not about either
run.

**Negative 2 (the hold-out failure, §5.6).** *Realization:* the abort family
`k ≥ K ∧ ‖R‖_k > θ‖R‖_{k−W}` replayed on banked residual histories. *Trial space:* 12,597 rules,
selected on one unit's ledger and scored on the other's. *Basis:* selection on U5's 9 convergences
yields a rule that kills one of U3's 14. The family is usable; selection on the smaller ledger is
not.

---

## 6. THE GATES

> **R0 gate:** Are the programme's two headline figures — total core-hours and distinct-orbit count —
> **re-derived independently from the banked artefacts**, each with the derivation shown, and each
> reported as agreeing or disagreeing with the figure currently in `WALLS.md`?

**YES.**

- **Total core-hours — AGREE** with `WALLS.md`'s 144.69 (U3) and 57.04 (U5); **DISAGREE** with its
  account of the 134.45 figure, which is `Σ attempts[].wall_seconds/3600` from the same JSON and not
  prose. Derivation in §2.
- **Distinct-orbit count — AGREE**: 8 (U3) and 5 (U5), under the arbiter's own rule, robust to
  linkage convention, to 20,000 orderings and to TOL over 0.05–0.10; **DISAGREE** with the prose
  premise "10 of U3's 14 convergences landed on just three solutions", measured as **9**.
  Derivation in §3.

**The corrected metric, in the gate's required form:**

> **U3 achieved 0.0553 distinct orbits per core-hour.**
> **Numerator 8** = the number of clusters of `attempts[].{T_converged, s_converged}` in
> `writeup/data/p2_prog_r4_g1_v1.json`, under `experiments/p2_prog_r4_m3_evidence.py` §5's rule at
> `TOL = 0.05` with `s` wrapped to the circle.
> **Denominator 144.6888** = `magnitudes.wall_seconds` (52087.95185184479) ×
> `magnitudes.workers` (10) / 3600.
>
> **U5 achieved 0.0877 distinct orbits per core-hour.**
> **Numerator 5**, same field and same rule, from `writeup/data/p2_prog_r4_m3_v1.json`.
> **Denominator 57.0352** = `magnitudes.wall_seconds` (25665.83147907257) ×
> `magnitudes.workers` (8) / 3600.
>
> Both denominators are strictly **worker-hours**. The physical core count is not a banked numeric
> field and **is not estimated**; see §2.

> **R1 gate:** Is R1, as `WALLS.md`'s Lane R defines it, executed to a **measured** number on the
> banked data, with its saving expressed as a **compute** quantity?

**YES.** Measured on U3's banked ledger — `writeup/data/p2_prog_r4_g1_v1.json`, the
`residual_history` of all 100 attempts, replayed, nothing re-run. The criterion "from epoch 20, stop
if `‖R‖_k > 0.5 · ‖R‖_(k−10)`" recovers **55.00% of U3's 4,629 epochs (4,629 → 2,083)** =
**74.87 of its 134.4475 attempt-CPU core-hours (55.69%)**, at **zero false kills** over 23 banked
convergences and a **6.90× safety margin**.

**With the correction that this saving is U5's, not R1's.** R1's own measured contribution is the
search that closes the family: 12,597 deterministic rules, 9,760 admissible, and the best rule that
does not degrade the deployed safety margin buys **+0.45 percentage points = +0.48 core-hours**.
**R1 CLOSES**; no further compute should be spent tuning this criterion family.

---

## 7. The projection, labelled

U3 replayed under the deployed rule finds the **same 8** distinct orbits in **59.5736** rather than
134.4475 attempt-CPU core-hours:

> **PROJECTED 0.1343 distinct orbits per core-hour** (attempt-CPU convention), against the measured
> **0.0595**. **PROJECTED**, factor **2.26×**.

The zero-false-kill control supports the "same 8" clause for the 14 convergences, but this remains a
**replay, not a run**, and it is labelled **PROJECTED** in `r1.projection`, in fig108 panel C, in the
journal and in the blog. Pre-committed branch (c) fired.

**No recycled-budget orbit yield is reported.** The assumption that recovered compute converts into
further orbits at the observed rate is optimistic and is not made here: R0 measured that U5 spent
57.04 core-hours to gain **one** orbit new to the programme.

---

## 8. Corrections raised, and applied nowhere

Six corrections to `WALLS.md` / `STATE.md` are written verbatim in
`experiments/journal/prog_r4_r0r1.md` under **`CORRECTIONS FOR THE CONDUCTOR`** and are **applied
nowhere** — those files are Conductor-owned. In summary: (1) "10 of 14" should read **9**; (2) the
134.45 figure is not prose and both conventions should be kept with labels; (3) the denominator is
worker-hours and `magnitudes.physical_cores` should be banked; (4) the metric counts cross-run
re-finds, so both the per-run and cumulative rows should be reported and the "first measured
improvement" claim withdrawn as an inference; (5) §R1's own numbers are confirmed but R1 should be
marked **CLOSED — collected by U5, headroom +0.45 pp**; (6) U3's converged states are not banked,
which caps any future audit of the distinct count at the `(T, |s|)` proxy.

---

## 9. What this unit did not do

- No solver attempt, no DNS step, no mining. Nothing was re-run. U5 was not re-run.
- No proposal for additional PROG-R4 seed supply.
- No edit to `STATE.md`, `WALLS.md`, `DIRECTION.md`, `plan_of_record.py`, any `experiments/programme_r4/u*.py`,
  any banked ledger, `p2_prog_r4_g1_v1.json`, `p2_prog_r4_m3_v1.json`, `u5_m3_converged_orbits.npz`,
  or `p2_prog_r4_m3_evidence.py`. `DIRECTION.md` was not read.
- No gate answer changed. No estimate substituted for a missing artefact.
- No external outreach (standing user hold).

**Scale is not evidence. A faster solver is not a result. The gate is the deliverable** — and the
ceiling stands: this makes the questions affordable, which is a different and lesser thing than
progress on the Clay statement.

---

*Blog version: [BLOG_P2_PROGR4_R0R1.md](BLOG_P2_PROGR4_R0R1.md). Figure: fig108
(`writeup/figures/fig108_prog_r4_r0r1.py`). Evidence:
`experiments/p2_prog_r4_r0r1_evidence.py`, 66/66.*
