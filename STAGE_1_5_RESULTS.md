# Stage 1.5 Results — Fitness-Signal Viability Sweep

**Verdict: `ν_crit` passes all five acceptance properties and becomes the
Stage 2 fitness axis. `a_crit` fails resolution stability and is rejected.**
(PLAN.md prefers `a_crit` when both pass; both do not pass.)

Date: 2026-07-22. Sweep code: `stage1_5_sweep.py` (commits `5c6dfc2` predicate
v1, `b05b9bf` predicate v2), analysis: `analyze_stage1_5.py`. Data:
`experiments/stage1_5_sweep.jsonl` (v1), `experiments/stage1_5_sweep_v2.jsonl`
(v2, authoritative). 80 bisections per sweep (~900 solver runs, ~15 min each).

## What was measured

20 hand-picked odd initial conditions, all rescaled to one L² energy
(`E = π/2`, the energy of `sin(x)`): 6 sine-combination profiles, 2 localized
bump pairs (κ=2, 5), 4 slowly-decaying spectral-tail profiles (p = 1, 1.5, 2,
alternating), and 8 seeded random shapes (`c_k ~ N(0,1)·k^{-1.5}`, k ≤ 16,
root seed 20260722). For each shape, at both N=256 and N=512, under one fixed
horizon `t_max = 12`:

- **`ν_crit`**: critical viscosity, bisected in ν ∈ [0, 1] at fixed a=0
  (CLM — the regime where smooth-data blow-up is proven, isolating the
  viscosity axis).
- **`a_crit`**: critical advection coefficient, bisected in a ∈ [0, 2] at
  ν=0 (the Okamoto–Sakajo–Wunsch question).

8 bisection iterations (tol: ν 0.0039, a 0.0078), then 2 monotonicity probes
beyond the critical value on the regular side. Bracket-edge outcomes censored
per PLAN.md. `bump(κ=5)` (analytic CLM T* ≈ 15.9 > t_max) was included as a
deliberate beyond-horizon control and correctly came back censored "low" on
both axes at both resolutions.

Blow-up oracle (final, v2): a run stopped by the 100× amplification threshold
is a blow-up regardless of its tail fit; otherwise blow-up requires the
held-out-R² exponent fit (`fit_exponent=True`, tail 0.15) to return an
estimate with R² ≥ 0.9 **and** T* ≤ 1.5·t_max. See "Predicate lessons" —
both deviations from the original PLAN.md predicate were forced by v1 data
and transfer directly to Stage 2's bisection oracle.

## ν_crit — passes (5/5)

| shape | N=256 | N=512 | shape | N=256 | N=512 |
|---|---|---|---|---|---|
| sin(x) | 0.0527 | 0.0527 | tail(p=1) | 0.0410 | 0.0410 |
| sin(2x) | 0.0137 | 0.0137 | tail(p=1.5) | 0.0488 | 0.0488 |
| sin+0.5sin2x | 0.0449 | 0.0449 | tail(p=2) | 0.0488 | 0.0488 |
| sin−0.5sin2x | 0.0488 | 0.0488 | tail(p=1.5,alt) | 0.0527 | 0.0527 |
| sin+0.3sin3x | 0.0527 | 0.0527 | random 0…7 | 0.0059–0.0527 | identical |
| sin+0.5sin4x | 0.0488 | 0.0488 | bump(κ=2) | 0.0332 | 0.0332 |

(bump(κ=5): censored low — beyond-horizon control, by design.)

1. **Nonzero**: 18/19 uncensored shapes have ν_crit > 2·tol; every uncensored
   shape blew up at a directly-simulated ν > 0. The "any viscosity
   regularizes ⇒ dead-flat landscape" risk (PLAN.md open risk #2) is
   empirically dead for this family at this horizon.
2. **Finite**: nothing censored high (no blow-up survives ν = 1).
3. **Monotone**: 0 violations across 38 probed bisections.
4. **Resolution-stable**: every N=256 vs N=512 critical value is *identical*
   (every bisection decision matched across resolutions; the measured noise
   floor at this tolerance is zero).
5. **Wide band**: spread 0.0059–0.0527 (9× ratio, 12× bisection tol) with
   physically sensible structure — e.g. sin(2x) lands at 0.0137 ≈ ν_crit(sin)/4,
   exactly the νk² scaling demands for a half-wavelength rescaling.

Cross-checks: consistent with the known bracket (sin blows up at ν=0.05,
decays at ν=0.5 — measured ν_crit = 0.0527); fitted blow-up exponents α ≈ 1
on clean CLM shapes with T* matching the closed form to ≲2%.

## a_crit — fails (resolution stability)

Representative v2 values (N=256 → N=512): sin(x) 0.887 → 0.973;
random seeds cluster 0.85–1.00 with |Δ| 0.008–0.102 (up to 13× tol);
**tail(p=1): 1.004 → 0.527** (a 90% shift); bump(κ=2) 0.340 → 0.340 and
sin+0.5sin2x 0.309 → 0.309 (stable only after the v2 predicate fix).

- **Passes**: nonzero (19/19), finite (after v2), monotone (0 probe
  violations), wide band (0.31–1.00).
- **Fails**: resolution stability. The roughest shape's a_crit halves when
  resolution doubles — the exact "critical value is a numerical artifact"
  showstopper PLAN.md Stage 1.5 names. The failure concentrating on the
  slowest-decaying spectral tail (p=1) is the regularity caveat made
  concrete: near-critical advection pushes the collapse to scales the grid
  sets, so the measured value tracks N, not the shape.
- Secondary defect: 15 of 19 shapes crowd into a ≈ 0.85–1.00, and within
  that cluster the resolution wobble (median 0.055) is comparable to the
  shape-to-shape differences — poor discrimination exactly where most
  shapes live.

## Predicate lessons (bind Stage 2's bisection oracle config)

1. **Amplification outranks the tail fit.** 41 of 292 amplification-stopped
   runs (14%) had held-out R² below the floor (bursty growth near critical
   parameters). PLAN.md's rule that InsufficientDataError-after-amplification
   is a blow-up generalizes: *any* amplification stop is a blow-up — its own
   rationale ("it hit the blow-up stop condition") does not depend on whether
   the fit ran. Without this, the bisection flips against exactly the
   marginal runs it is probing.
2. **Fit-based blow-up needs a horizon cap: T\* ≤ 1.5·t_max.** Under v1,
   runs that sat quietly until t_max and then fit a zero crossing at
   T* = 74–136 (6–11× the horizon, held-out R² barely over 0.9) were
   accepted as blow-ups; whether such unfalsifiable fits clear the floor
   flips with resolution. All v1 censored-high anomalies and part of the
   a-axis instability traced to this; the cap turned bump(κ=2) and
   sin+0.5sin2x from resolution-flipping to resolution-exact. tail(p=1)'s
   drift survives the cap — that one is physics/discretization, not
   predicate.
3. **Frozen stop criteria worked as designed** — t_max 12, amplification
   100×, tail fraction 0.15, R² floor 0.9, early-decay exit
   (fraction 0.1, window 2.0; fired on 158/896 runs, saving the dominant
   no-blow-up cost) — all runs, both axes, both resolutions.

## Artifact-guard notes

- ν-axis blow-up runs accumulate energy-balance residuals of 0.05–0.5 by the
  amplification stop. This is endgame *time*-integration error, not spatial
  under-resolution: halving (dt_max, c1) halves the residual and shifts
  ν_crit by exactly 0 (spot-checked at N=512 on sin(x), tail(p=1),
  random(seed=3) — the highest-drift shapes). Stage 2 should either accept
  this (the classification is dt-robust) or stop residual accumulation once
  amplification exceeds ~10× if the guard is wanted as a clean artifact
  signal; a-axis runs stay below ~10⁻³ throughout.
- `dt_min` in run logs is polluted by the final-step `t_max − t` clamp
  (values ~1e-13 are the clamp, not a dt collapse). Cosmetic; fix whenever
  the solver is next touched.

## Consequences for Stage 2 (applied to PLAN.md)

- `fitness_axis = "nu_crit"`, measured at fixed `gclm_a = 0.0`.
- Frozen stop criteria as above; bisection predicate = v2 oracle
  (amplification-first + R² floor 0.9 + T* ≤ 1.5·t_max).
- ν_crit's absolute band is narrow (0–0.053 under these stop criteria):
  Stage 2's bisection should use a range of [0, 0.1] with tolerance ≤ 1e-3
  (or bisect in log ν) so shape differences span many tolerance steps, and
  the warm-start bracket margin should be sized in those units.
- `a` remains a first-class solver parameter; nothing here forecloses
  revisiting an `a`-axis fitness later with a resolution-convergent oracle
  (e.g. requiring N-agreement per bisection step), but that is redesign
  work, not the Stage 2 default.
