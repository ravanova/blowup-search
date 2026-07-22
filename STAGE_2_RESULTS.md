# Stage 2 Results — GA Harness Acceptance Runs

**Verdict: acceptance criterion NOT MET, replicated across all 3 seeds —
because the fitness axis, not the search, is degenerate: `ν_crit` at a=0
has a trivially-located global optimum (≥99.5% of energy in the k=1 mode),
reached by random sampling within ~12 draws of the init prior.** The GA
harness itself passed every operational check and is reusable unchanged
for any scalar fitness. The redesign plan is PLAN.md Stage 2.5.

Date: 2026-07-22. Harness: commit `d47b579` (ga/genome.py, ga/operators.py,
ga/fitness.py, ga/evolve.py; test_ga.py). Analysis: `analyze_stage2.py`
(commit `2c4ac14`). Runs: `stage2-shakedown` (pipeline check), then
`stage2-seed1/2/3` — pop 24 × 25 generations = 600 GA evaluations + 612
budget-matched baseline evaluations per seed, ~12,200 solver runs / ~64 min
per seed at 10 workers. Logs under `experiments/run_logs/<id>/`.

## Configuration (frozen, from Stage 1.5's verdict)

`fitness_axis = nu_crit` at `gclm_a = 0`, `fitness_resolution_N = 256`,
`t_max = 12`, amplification 100×, early-decay exit (0.1 / 2.0), v2 oracle
(amplification-first; fit-based blow-up needs held-out R² ≥ 0.9 AND
T* ≤ 1.5·t_max), bisection ν ∈ [0, 0.1] tol 1e-3 with parent-warm-started
brackets (±0.01). Genome: 32 sine coefficients + evolvable k^-p envelope
(p ∈ [0, 3.5]), L² energy renormalized after every operator and after the
envelope. MAP-Elites on (spectral_tail_slope, n_sign_changes), 12×8 cells.
Baselines: interleaved budget-matched `baseline_random` (same init prior),
`baseline_literature` re-sampled onto the genome at each run start.

## Primary result — best-so-far vs cumulative evaluations

| seed | GA best | random best | margin (in tol units) | literature best |
|---|---|---|---|---|
| 1 | 0.054297 | 0.054297 | 0.0 | 0.053516 |
| 2 | 0.054297 | 0.054297 | 0.0 | 0.053516 |
| 3 | 0.054453 | 0.054297 | 0.2 | 0.053516 |

Both curves saturate within ~12 evaluations on every seed — order
statistics of the init prior, not search. The acceptance criterion (clear
domination at matched budget on ≥3 seeds) fails decisively.

**Why:** all three seeds' best genomes are the same shape — ≥99.5% k=1
energy plus a few percent of one low harmonic (seed 1: k=3; seed 2: k=4;
seed 3: k=2, the only one found by crossover rather than raw init, buying
+0.0002 ≈ 0.2 tol over pure init draws). This is the νk² scaling argument
as a global optimum: energy in the lowest mode survives viscosity best,
and no structural blow-up mechanism at this horizon beats simply hiding
from dissipation. PLAN.md's "frequency-space cheating" guardrail worry was
the honest answer of this axis, not a cheat to be caught.

## Secondary result — random beats the GA at map-building too

Replaying both event streams through identical archive-insertion rules
(uncensored + monotone-clean + beats incumbent; `analyze_stage2.py`):

| seed | GA coverage | GA QD | random coverage | random QD |
|---|---|---|---|---|
| 1 | 58.3% | 2.222 | 79.2% | 2.703 |
| 2 | 51.0% | 2.043 | 76.0% | 2.748 |
| 3 | 45.8% | 2.061 | 74.0% | 2.643 |

On a saturated landscape, fitness-driven tournament selection concentrates
parents on a flat plateau; the exploration random search gets for free is
strictly better for the map deliverable. So the GA loses on *both* the
frozen metric and the QD metric — the negative is not an artifact of
metric choice.

## What held up

- **Operational health:** 0/1800 GA+random evaluations censored (the
  bump(κ=5) beyond-horizon literature control censored "low" as designed),
  6 non-monotone flags in 3,672 evaluations, ~6% warm-bracket expansion
  rate (warm starts saved ~2 solver runs/eval), zero cache hits (expected:
  MAP-Elites never re-evaluates elites). Literature control reproduced
  Stage 1.5 values (sin(x) 0.0535 vs 0.0527 at coarser tolerance; sin(2x)
  0.0137 exactly).
- **Map interior:** median ν_crit falls smoothly with oscillation count
  (0.054 at 2 sign changes → 0.028 at 20) and with tail roughness —
  real, physically sensible structure. Confound: per-bin *maxima* sit at
  ~0.054 nearly everywhere, because a 99%-k=1 genome can carry any tail
  slope in its negligible tail — the two archive descriptors do not pin
  k=1 dominance (`energy_top_k_frac` does).
- **Cross-seed convergence:** final GA archives agree at Jaccard
  0.61–0.69 with mean |Δfitness| ≈ 0.0064 (~6 tol) on shared cells.

## Methodology lesson (binds all future fitness axes)

Stage 1.5's five viability properties — nonzero, finite, monotone,
resolution-stable, wide band — are necessary but **not sufficient**: none
asks *where the optimum lives*. A sixth property is now required before
any axis reaches the GA:

> **Non-trivial optimum.** The best of ~20 init-prior random draws must sit
> clearly below the best achievable value (hand-constructed or
> literature), and the top of the landscape must not be monotone in a
> trivially controllable quantity (here: `energy_top_k_frac` / k=1
> dominance). An axis whose optimum is reachable by prior sampling gives
> selection nothing to do.

This check costs ~20 bisections and would have predicted this entire
outcome before `ga/` was built.

## Consequences (see PLAN.md Stage 2.5 for the full plan)

- The harness is generic over the fitness axis by design; the rerun is a
  config change, not a rebuild.
- Leading redesign candidates: (A) `ν_crit` at fixed a > 0 — at a=1
  (De Gregorio) sin(x) is an equilibrium and advection actively opposes
  low-k concentration, so resistance must come from structure; the ν
  bisection was the resolution-exact part of Stage 1.5, unlike the a-axis.
  Risk: near a=1, smooth data may not blow up within the horizon at all
  (censored-low everywhere → dead axis) — measure first. (B) Bandwidth-
  constrained `ν_crit` at a=0 (cap the k≤2 energy fraction at
  normalization). Risk: optimum pins to the arbitrary constraint boundary.
- Either candidate must pass all **six** properties (five from Stage 1.5
  + non-trivial optimum) before the 3-seed acceptance rerun.
