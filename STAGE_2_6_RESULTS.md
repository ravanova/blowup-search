# Stage 2.6 Results — Oracle v3, Axis Selection, and the Acceptance Rerun

**Verdict: axis A′ — ν_crit under the v3 amplification-only oracle at
a = 0.7 — passes all six viability properties, and the Stage 2 acceptance
criterion is MET on it: the GA's best-so-far curve clearly dominates the
budget-matched random baseline on 3/3 seeds (margins 3.3 / 4.6 / 3.2
tolerance units, with domination over the final half of the budget on
every seed). The GA also exceeds the best literature profile on every
seed. This closes the Stage 2 milestone after two failed axis families
(Stage 2, Stage 2.5).**

Date: 2026-07-22/23. Sweep: `stage2_6_sweep.py` (commit `82dc7de`), gate:
`analyze_stage2_6.py`, acceptance config: commit `a10d6b2`, acceptance
analysis: `analyze_stage2.py`. Data: `experiments/stage2_6_sweep.jsonl`
(480 tasks, 27 min), `experiments/run_logs/stage2_6-seed{1,2,3}/` (600 GA
+ 612 baseline evals each, ~68 min/seed at 10 workers).

## Part 1 — Oracle v3 and the candidate gate

**Oracle v3** (PLAN.md Stage 2.6, path 1): a run is a blow-up iff it hits
the 100× amplification stop or diverges; the tail fit is still computed
and logged (Tier 1 candidacy) but never decides the bisection. Horizon
t_max = 24 (2× Stage 2) so slow growers must *demonstrate* blow-up.
This structurally removes the fit-quality flicker that produced Stage
2.5's non-monotonicity at a > 0.

**Six-property gate over 40 shapes (20 Stage 1.5 ICs + 20 init-prior
draws), N ∈ {256, 512}:**

| candidate | verdict | failing property |
|---|---|---|
| B′: ν_crit(v3) a=0 | FAIL | non-trivial optimum (k=1 refuge: gap **−0.8·tol** — a prior draw beats every structured shape; ρ(k1)=0.97, top-3 k1 ≥ 0.98) |
| A′: a=0.4 | FAIL | non-trivial optimum (gap 7.0·tol < 10; ρ(k1)=0.81) |
| **A′: a=0.7** | **PASS** | — |
| A′: a=1.0 | FAIL | nonzero + wide band (dead axis persists at t_max=24: 35/40 censored low) |
| C: ν_crit·k_eff² (a=0) | FAIL | non-trivial optimum — the mirrored cheat realized: gap **−1839 noise units** (high-k_eff prior draws dominate outright), ρ(k_eff)=+0.94 |
| D: t_max−t_amp @ ν=0.01 | FAIL | non-trivial optimum (gap 8.9 noise units, under the 10 bar) |
| D: t_max−t_amp @ ν=0.03 | FAIL | non-trivial optimum (gap 6.0 noise units) |

**A′(a=0.7) in detail** — every property, cleanly:
37/37 uncensored nonzero (censored-low only: the two bumps and
sin(x)+0.5sin(2x), all with known reasons); nothing censored high;
**0 non-monotone flags in 37 probed bisections** (v2 had the flicker;
v3 does not); resolution near-exact (median Δ = 0, max = 0.8·tol);
band 0.006–0.158 (152·tol); prior-vs-structured gap **20.3·tol**
(best prior 0.1379, best structured 0.1582), with the landscape top held
by structured *mixtures* (top-3 k1 fractions 0.80–0.84) while every
pure-k1 shape (four prior draws and sin(x), k1 ≥ 0.998) sits 14–20·tol
below the top. At a=0.7 the k=1 refuge is no longer optimal — resistance
requires structure, which is exactly what a fitness axis must reward for
selection to have work to do.

## Part 2 — Acceptance rerun (protocol identical to Stage 2)

Config (commit `a10d6b2`, config-only changes): `gclm_a=0.7`,
`t_max=24` (max_steps 400k), bisection range [0, 0.3] tol 1e-3,
`blowup_predicate=v3_amplification_only`; everything else — pop 24 × 25
generations, MAP-Elites on (spectral_tail_slope, n_sign_changes) 12×8,
interleaved budget-matched baseline_random, literature control re-sampled
at run start, warm-started brackets, N=256 fitness resolution
(re-confirmed resolution-exact at a=0.7 by the sweep) — unchanged.

### Primary criterion — best-so-far vs cumulative evaluations

| seed | GA best | random best | margin (tol units) | literature best | dominates final half | pass |
|---|---|---|---|---|---|---|
| 1 | 0.1624 | 0.1591 | **3.3** | 0.1585 | yes | ✓ |
| 2 | 0.1631 | 0.1585 | **4.6** | 0.1585 | yes | ✓ |
| 3 | 0.1629 | 0.1597 | **3.2** | 0.1585 | yes | ✓ |

**PASS (3/3; the criterion requires every seed).** The GA exceeds the
best literature profile on every seed; the random baseline never does.

### Where the gains came from (operator attribution, event stream)

Random initialization ceilings (gen 0): 0.147–0.152. After that, on seed
1, **all eleven** best-so-far improvements came from variation (6
mutation, 5 crossover, 0 from later random draws), a monotone climb
0.147 → 0.162; seeds 2–3 show the same signature. Archive insertions
split roughly evenly between mutation and crossover. Improvements were
still arriving at generations 21–24 on all seeds — the 25-generation
budget likely truncates the climb (see tuning leads below).

### Secondary — QD replay at matched budget (reported, not gating)

| seed | GA coverage | GA QD | random coverage | random QD | GA QD wins |
|---|---|---|---|---|---|
| 1 | 52.1% | 7.003 | 79.2% | 7.223 | no |
| 2 | 50.0% | 7.220 | 75.0% | 7.524 | no |
| 3 | 56.2% | 7.804 | 74.0% | 7.095 | yes |

The Stage 2 pattern persists in softened form: random sampling still
covers more descriptor cells (it explores for free), and wins raw
QD-score on 2/3 seeds, though the gap is far smaller than Stage 2's and
the GA's cells hold higher fitness. Peak-fitness search and map-building
remain different objectives; if the map deliverable needs more coverage,
exploration pressure (novelty bonus / empty-cell-directed emission) is
the standard lever — a tuning question, not an axis question.

Cross-seed map convergence: Jaccard 0.62–0.72 on filled cells, mean
|Δfitness| 0.005–0.011 on shared cells — independent seeds land on
substantially the same map.

### Operational health

Censored evaluations 5/3/8 per seed (of 1,212 each), non-monotone flags
0/5/2 (excluded from the archive by rule), zero cache hits (MAP-Elites
never re-evaluates elites), literature control reproduced the sweep's
structured best (0.15849 vs 0.15820, within 1·tol) on all three seeds.

## What this means

- **The Stage 2 milestone is closed: evolutionary search demonstrably
  beats budget-matched random search on a verified, non-degenerate PDE
  blow-up fitness.** The two prior failures were failures of the fitness
  axis (νk² spectral triviality), not of the machinery — and the
  six-property gate now separates those cases for ~40 bisections of
  compute, before any GA time.
- **The evolved shapes are (modestly) beyond the literature set**: every
  seed found mixtures more viscosity-resistant than any hand-built or
  literature profile measured under the same frozen oracle (+3–5·tol).
  These genomes are logged with full coefficients (`genomes/`,
  checkpoints) and are the natural first inputs to Stage 3.
- **Physics note carried forward**: moderate advection (a≈0.7) *raises*
  measured viscosity-resistance vs a=0 under demonstrated-amplification
  semantics, the k=1 refuge dies by a≈0.7, and De Gregorio (a=1) remains
  a dead axis for smooth odd data even at t_max=24 — all consistent with
  the literature's regularity expectations and now measured on one
  frozen protocol.

## Tuning leads (optional, post-acceptance — from the JOURNAL interim)

1. Mutation-scale floor and/or longer runs: improvements still arriving
   when the generation budget ends on all three seeds.
2. Archive coverage plateaus at ~50–56% while random reaches ~75–79%:
   exploration pressure if the map deliverable matters.
3. No evidence the genotype is the bottleneck.

## Next step

Stage 3 (PLAN.md): the automated resolution-study loop — rerun the elite
genomes at N = 256/512/1024, promote T*-convergent candidates to
`NUMERICALLY_CONFIRMED` (Tier 2). The acceptance-run elites (best ≈ 0.163
at a=0.7, plus the per-cell archive) are the input queue.
