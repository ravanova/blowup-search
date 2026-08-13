# PROG-R4 U3 — GATE G1: seeded recovery of named Table IV RPOs at the compliant scale

**Unit:** PROG-R4 U3 (leg 380), `ORCHESTRATION.md` §3c programme lane. **CLAIM unit — answers a
gate.**
**Mode:** §3f SOLO. **UNVERIFIED** — produced and checked in one session, no paired verifier.
**Data of record:** `writeup/data/p2_prog_r4_g1_v1.json`; ledger
`experiments/programme_r4/u3_g1_ledger.json`.
**Figure:** fig97, 22/22 checks.
**Pre-registration:** `experiments/journal/prog_r4_prereg.md`;
`experiments/journal/prog_r4_u2u3_prereg_addendum.md` §§3–3f.

---

## 1. Gate and answer

> **G1: DOES AT LEAST ONE NAMED TABLE-IV RPO RECOVER TO tol=1e-8?**

**`UNDER-RESOURCED`.** `n_recovered = 0`, `n_converged_to_tol = 14`, `n_attempts = 100`,
`controls_fired_as_planted = true`, `control_failures = []`.

Branch selection is mechanical and was fixed before the run:

```python
answer = (("YES" if recovered else "UNDER-RESOURCED")
          if controls_fired else "UNANSWERED")
```

with `"NO"` removed from the branch set by AMENDMENT 3 on measured cost. §3d's stop does **not**
fire; route 4 is **not** stopped on measurement.

## 2. The controls, which license the answer

A negative-side answer is admissible only from an instrument shown able to produce a positive.
Three controls, pre-registered in addendum §3 before the recurrence stage and before any attempt:

| control | role | planted as | result |
|---|---|---|---|
| **P** | positive, unconditional | exact fixed point of the **discrete** map in closed form, `ŵ* = dt·f̂·decay/(1−decay)`; `‖Φ_dt(w*) − w*‖ = 7.6e-14` | **recovered**, `‖R‖ = 7.75e-9` |
| **N** | negative | phase-scrambled field at a real anchor's published period | **not recovered**, `‖R‖ = 1.75` |
| **R** | positive, conditional | perturbation of a converged orbit; exercises the `(T, s)` directions | **recovered**, `‖R‖ = 3.26e-9` |

`FIRED AS PLANTED := P recovered AND N did not recover AND (R recovered, if R ran)` — satisfied.

Control P is the one that has already earned its keep: in the cap-fixing work it exposed a defect
in `newton_hookstep_rpo` that discarded a converged iterate and returned `success=False`, which at
G1 would have recorded a non-recovery on an attempt that recovered — a fabricated `no` on the one
gate whose `no` stops route 4. Documented separately in `TECHNICAL_P2_PROGR4_CONTROL_CATCH.md`.

P is also run at `T_P = 2.65`, not the pre-registered `T = 19.33`, per AMENDMENT 1: at `T = 19.33`
the equilibrium's Lyapunov exponent (2.88) amplifies by `~1e24`, which is not a control, it is a
different problem. `T_P` is defined as the multiple of `dt` at which the equilibrium's measured
amplification equals the attractor's `8.73e2`, obtained by log-interpolating the measured
amplification table between `T=2` (99.9) and `T=3` (2.81e3).

## 3. Resourcing as run

| | value | note |
|---|---|---|
| `T_dns` | `1.0e5` | unit U2, MILESTONE M2 |
| `N`, `Re`, forcing | 24, 60.0, `n=4` | 578 real unknowns in the extended system |
| globalisation | Newton–GMRES–hookstep trust region | unit U1, MILESTONE M1 |
| `n_attempts` | 100 | pre-registered count |
| `tol` | `1e-8` | |
| `max_newton`, `max_gmres`, `gmres_rtol` | 52, 140, `1e-3` | AMENDMENT 3 |
| wall | **14.47 h** | 134.45 core-hours, 10 workers |
| seed funnel | 2014 → 579 → 234 → 133 → 100 | candidates → `R<0.25` → `m=0` → anchored → run |
| `short_of_requested` | 0 | AMENDMENT 4 restored the pre-registered count |
| shift sign | 98 minus, 2 plus | **measured per seed, not assumed** |

`P(0 successes in 100)` at the sourced rates: `1.2e-2` (C&K 4.3%), `3e-5` (L&K ~10%). Leg 353
baseline: 5 attempts at `T = 2000`, line search, `any_converged = false`.

## 4. Convergence behaviour

**Rate.** 14/100 = **14%** per attempt, above both sourced rates.

**Magnitudes.** Best final `‖R‖ = 8.673594e-12`; the 14 convergences span `8.67e-12` to
`8.64e-09`; the next-best non-convergence is `2.80e-02`. The distribution is **cleanly bimodal**
with a gap of six orders of magnitude and nothing in it.

**Epochs.** Convergences: min 10, median 16, **max 29** — all well inside `max_newton = 52`.
Non-convergences: all at the cap (51 recorded steps).

**Krylov.** Max dimension over all attempts **25**, p95 = 24, against `max_gmres = 140`. Clause
(a) of the cap rule was satisfied by 5.8×.

**Stall diagnostic on the 86 non-convergences**, reduction in `‖R‖` over the final 10 epochs:

| | |
|---|---|
| median reduction factor | 0.9941 |
| fraction with < 1% reduction | **0.53** |
| fraction with < 10% reduction | **0.83** |
| fraction still halving (< 0.5) | 0.03 |
| median final `‖R‖` | 2.11 |
| median total reduction from seed | 0.087 |

They are stalled, not descending.

## 5. The eight converged solutions

Shifts wrapped to `(−π, π]`; `±s` are the same orbit under the flow's reflection symmetry.

| `T` | `\|s\|` | found | seed anchors | best `‖R‖` |
|---|---|---|---|---|
| 16.5241 – 16.5358 | 0.0997 – 0.1019 | **4** | UPO9, UPO17 | 7.42e-11 |
| 16.8100 – 16.9224 | 0.0729 – 0.0738 | **4** | UPO9, UPO17 | 7.14e-11 |
| 17.1650 | 0.0741 | 1 | UPO9 | 3.24e-09 |
| 17.3492 | 0.3174 | 1 | UPO22 | 1.16e-09 |
| 19.2848 / 19.2929 | 0.1178 / 0.1157 | **2** | UPO32 | 9.98e-12 |
| 19.6787 | 0.0851 | 1 | UPO22 | 2.23e-09 |
| 22.0389 | 0.1347 | 1 | UPO37 | 8.67e-12 |

The replications are across **different snapshots and different anchors**, agreeing to `0.012` in
`T` and `0.002` in `|s|`. That is internal replication of a genuine solution, not a repeated
number.

**`n_recovered = 0`.** The gate's predicate is convergence to tol **and** a match to a named row
within `MATCH_T_TOL = MATCH_S_TOL = 0.05` on both `T` and `s`. Nothing satisfies it. fig97 asserts
this separation explicitly:

```python
check("no attempt is marked recovered without matching a named row on BOTH T and s",
      all((not a["recovered_named_orbit"])
          or (a["delta_T_from_published"] <= 0.05
              and a["delta_s_from_published"] <= 0.05) for a in att))
```

## 6. The second selection bias

Converged `|s| ∈ [0.073, 0.317]`, 12/14 below 0.14. Published `|s| ∈ [0.295, 0.707]`. Disjoint but
for one point.

Measured on the library's 1153 `m = 0` candidates: **rank correlation `corr(|s|, R) = 0.50`**, and
admission by `R < R_thres_window = 0.25` is monotone decreasing in shift:

| `\|s\|` band | n | median `R` | admitted |
|---|---|---|---|
| 0.000 – 0.150 | 322 | 0.3205 | 0.44 |
| 0.150 – 0.295 | 213 | 0.5067 | 0.20 |
| 0.295 – 0.750 *(published band)* | 395 | 0.8317 | 0.11 |
| 0.750 – 3.200 | 223 | 1.1278 | 0.03 |

Admitted pool median `|s| = 0.112`; 21% of it exceeds the smallest published shift. All candidates
regardless of window: median `|s| = 0.824`. **The population exists; the window removes it.**

Newton converges near its seed, so the seed pool's shift distribution propagates to the solution
set. The observed 14 solutions are the expected image of the admitted pool under the solver, not
an anomaly of the solver.

**Structural identity with AMENDMENT 4.** U2 found the same failure in the period coordinate: a
global top-N ranked by `R_red` left exactly 1 of 400 candidates near a published period, because
short intervals score better for reasons unrelated to being an orbit. Both are: *a scalar score
used as an admission filter, systematically monotone in a coordinate on which the targets are
selected.* The period case was fixed by stratifying the budget; the shift case is **unfixed**,
because it was not anticipated.

## 7. Errata against AMENDMENT 3 (addendum §3e)

1. **Envelope arithmetic ignored `Pool.map` chunking.** Sized as `ceil(100/10) = 10` balanced
   rounds; actual chunksize `ceil(100/(4·10)) = 3` gives 34 chunks and a 12-attempt tail worker.
   Errs safe.
2. **Per-epoch cost underestimated ~1.7×.** Probe 54.7 s/epoch; run ~95 s/epoch (134.45
   core-hours / 100 attempts / ~51 epochs). Probable cause: the probe did not run at ten-way
   concurrency. Cost successors at 95.
3. **The `max_newton_required = 238` model is wrong about the mechanism.** It assumed slow
   convergence (2× a censored median of 119 epochs to convergence-or-stall). Observed behaviour is
   bimodal: ≤29 epochs or flat. Neither cap bound any attempt that converged.

`UNDER-RESOURCED` remains correct — the run *was* below the named budget and `no` was correctly
unavailable — but the named cost (36.2 h at 10 workers, 15.1 core-days) is **the wrong purchase**.
Buying 238 epochs extends 86 flat sequences.

## 8. Lesson 91 — what this negative names

Realization: **first-order in time** (Lie–Trotter: RK4 on the nonstiff part then the exact viscous
factor; measured local ratio 4.00, global ratio 2.00 — the splitting error, not RK4, sets the
order). Its periodic orbits are `O(dt)` perturbations of the continuous flow's.

Trial space: the extended residual `R(w₀, T, s) = σ_s Φ_T(w₀) − w₀` carries a **continuous
`x`-shift only**; there is no `m` unknown, so 345 in-window candidates cannot be *expressed* as
seeds. All eight named rows have `m_published = 0`, so nothing named is lost, but the sentence
must carry the limitation.

Seed supply: an admission filter monotone in `|s|`, per §6.

**Full form of the negative:** *no named Table IV row was recovered by a first-order-in-time
realization, from a seed pool whose admission filter is monotone in the coordinate that separates
the targets, inside an iteration budget below the one the cap rule named.* Not "the orbits are not
there"; not "Newton cannot find them" — it found eight others, reproducibly.

## 9. Successor ordering

1. **Stratify the seed budget by shift.** 395 `m=0` candidates already lie in the published band,
   11% already inside the window. Cheapest untried action, targets the measured cause.
2. Replace or condition the `R < 0.25` admission test, which is confounded with `|s|`.
3. Add an `m` unknown to the residual — a realization change, invalidates M1's reproduction, needs
   its own milestone.
4. Buy iterations **last**. The bimodality says this is the lowest-yield spend.

Not started here; selecting one would be choosing the unit's own next task.

## 10. Obligations

`CLAY_OBLIGATIONS` §6 items 1 and 2 **OPEN**. §4 **OPEN and NOT discharged** pending leg 386's
pre-registered δ mode. **Ceiling TIER 2.** No `L1 → L4` link moved. **Clay ~0.05%.**

Gate G2 (U4, basin radius, brick B5 c-iii) **UNANSWERED, not opened** — it requires a recovered
*named* orbit to perturb.
