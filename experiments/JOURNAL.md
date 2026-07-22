# Experiment Journal

Hand-written context per experiment (see LOGGING.md — the structured logs
answer "what happened"; this records *why* and what a human noticed).

## stage2-seed1 / seed2 / seed3 (d47b579) — 2026-07-22

Why configured this way: the Stage 2 acceptance runs — 3 independent seeds,
pop 24 × 25 generations = 600 GA evals each, budget-matched interleaved
baseline_random (612 with the literature control), frozen fitness config
(nu_crit at a=0, N=256, t_max=12, bisection [0, 0.1] tol 1e-3, v2 oracle).
~12,200 solver runs / ~64 min per seed at 10 workers.

**Verdict: acceptance NOT MET, decisively and in triplicate — and the
reason is a finding, not a bug.** The nu_crit landscape at a=0 has a
trivially-located global optimum: pile energy into k=1. Numbers:

- Best-so-far: GA 0.0543 / 0.0543 / 0.0545 vs random 0.0543 / 0.0543 /
  0.0543. Margin 0, 0, and 0.2× tolerance. Both sides hit the ceiling
  within ~12 evaluations (order-statistics of the init prior, not search).
- All three seeds' best genomes are >= 99.5% k=1 energy with a few % of
  one low harmonic (k=2..4). Two of three were raw init draws; seed 3's
  crossover polish bought +0.0002 (~0.2 tol). This is the nu*k^2 scaling
  argument, rediscovered empirically: lowest mode survives viscosity best.
  PLAN.md's "frequency-space cheating" guardrail worry turns out to be the
  honest global optimum of this axis, not a cheat.
- Sharper: random *dominates the GA on map-building too* — replaying both
  event streams through identical archive-insertion rules, random reaches
  74–79% coverage / QD 2.6–2.7 vs the GA's 46–58% / 2.0–2.2 at the same
  budget. Fitness-driven tournament selection concentrates parents on a
  flat plateau; exploration is all cost, no signal. On a saturated
  landscape MAP-Elites' selection pressure is strictly worse than prior
  sampling for the map deliverable.
- The pipeline itself behaved to spec: 0/1800 GA+random evals censored
  (bump(κ=5) control aside), 6 non-monotone flags in 3,672 evals, ~6%
  bracket-expansion rate, warm starts saving ~2 runs/eval, zero cache
  hits (expected: MAP-Elites never re-evaluates elites).
- The map interior is real but partially confounded: median nu_crit falls
  smoothly with oscillation count (0.054 at 2 sign changes → 0.028 at 20)
  and with tail roughness — but per-bin maxima sit at ~0.054 nearly
  everywhere because the two archive descriptors don't pin k=1 dominance
  (a 99%-k=1 genome can carry any tail slope in its negligible tail).
  Cross-seed final archives: Jaccard 0.61–0.69, mean |Δfitness| on shared
  cells ≈ 0.0064 (~6 tol) — moderate convergence, consistent with sparse
  per-cell sampling.

Lesson recorded for any future fitness axis: Stage 1.5's viability
properties (nonzero, finite, monotone, resolution-stable, wide band) are
necessary but NOT sufficient — they never asked *where the optimum lives*.
Add a sixth check: the optimum must not be reachable by trivial sampling
of the init prior (e.g. require the best of ~20 random draws to sit well
below the best hand-constructed shape).

Redesign options for a non-degenerate axis (review decision, in rough
order of preference): (1) bandwidth-constrained nu_crit — cap the k=1 (or
top-k) energy fraction, or pin the spectral centroid, so resistance must
come from structure; (2) move to a > 0 (De Gregorio side) where advection
fights growth and low-k concentration stops being free — requires the
resolution-convergent oracle Stage 1.5 says the a-axis needs; (3) score
QD/map metrics directly rather than scalar best-so-far.

## stage2-shakedown (d47b579) — 2026-07-22

Why configured this way: first end-to-end run of the Stage 2 GA harness —
deliberately tiny (pop 6, 3 generations, seed 999) to shake out the
pipeline before the real 3-seed acceptance runs, per PLAN.md. Full frozen
fitness config (N=256, t_max=12, bisection [0, 0.1] tol 1e-3, v2 oracle).

What a human noticed skimming the results:

- The literature positive control lands where Stage 1.5 put it: sin(x)
  0.0535 (vs 0.0527 at the coarser Stage 1.5 tolerance), sin(2x) 0.0137
  exactly, and bump(κ=5) censored "low" — the beyond-horizon control
  behaves inside the GA harness too.
- Warm-started child evaluations took a median 9 solver runs vs 11 cold,
  with 0 bracket expansions in 12 — the ±0.01 margin is, if anything,
  generous; leaving it.
- Median 15.3s per evaluation, ~2× the Stage 1.5 per-bisection cost:
  the [0, 0.1] range concentrates bisection samples near the critical
  value, where no-blow-up runs burn the whole t_max. Real-run sizing
  (~25 min/seed at 10 workers) accounts for it.
- A random init genome (0.0543) edged out sin(x) immediately — the
  landscape above 0.053 is reachable, but the random baseline found it
  too. Whether the GA can *separate* from the baseline is exactly what
  the 3-seed acceptance runs measure.

## stage1_5_sweep (v1: 5c6dfc2, v2: b05b9bf) — 2026-07-22

Why configured this way: t_max=12 chosen after computing analytic CLM T*
for all 20 normalized ICs (live shapes span 1.0–6.5; bump(κ=5) at 15.9 kept
deliberately as a beyond-horizon censoring control). ν bisected at a=0 to
isolate viscosity in the proven-blow-up regime; a bisected at ν=0. One
energy scale (E of sin(x)) across all shapes so critical values compare
shape, not amplitude.

What a human noticed skimming the results:

- The ν axis is astonishingly clean: all 80 v1-vs-v2 and 256-vs-512
  ν-bisections take *identical* decision paths. The sin(2x) value landing at
  ν_crit(sin)/4 (νk² scaling) was not designed in — good sign the number is
  physical.
- The v1 a-axis anomalies (censored-high at N=512 only, for two shapes) all
  traced to one predicate flaw: accepting held-out-R²≈0.9 fits whose
  extrapolated T* was 6–11× beyond the horizon. Capping T* at 1.5·t_max
  (v2) fixed every one; tail(p=1)'s 2× resolution drift survived the fix
  and is the real, physical reason a_crit was rejected.
- 14% of amplification-stopped runs had tail fits below the R² floor
  (bursty near-critical growth) — the amplification-first predicate rule
  mattered in practice, not just in principle.
- Energy-balance residuals up to 0.5 on ν-axis blow-up runs looked alarming
  but are endgame dt-integration error: halving dt halves them and moves
  ν_crit by exactly zero (3-shape spot-check at N=512).
