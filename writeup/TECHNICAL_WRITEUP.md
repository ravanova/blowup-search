# Evolutionary Search for Navier–Stokes-type Finite-Time Blow-up
## A validated 1D quality-diversity pipeline, with resolution-confirmed candidates

*Technical writeup, 2026-07-23. All figures/numbers rebuild from
[`data/`](data/); see [README.md](README.md).*

---

## 1. The problem, and the honest version of the goal

The Clay Millennium problem for 3D incompressible Navier–Stokes asks to either
(a) prove smooth finite-energy initial data always yields globally smooth
solutions, or (b) exhibit smooth data whose solution blows up in finite time.
We pursue **(b)**: direction (a) is a universal statement over an
infinite-dimensional space and cannot be *searched* into existence, whereas (b)
is existential — one counterexample suffices — which is what a fitness-driven
search can climb toward. This mirrors real practice: Hou, Luo and collaborators
found near-singular 3D Euler solutions numerically; Buckmaster, Gómez-Serrano
and others later turned related numerical candidates into rigorous
computer-assisted proofs.

The central hazard of a computational blow-up search is **self-deception**:
an under-resolved simulation routinely *looks* like it is blowing up when it is
merely hitting the grid. The entire project is organized around a tiered
win-condition contract ([../WIN_CONDITION.md](../WIN_CONDITION.md)) that refuses
to conflate "the simulation looks like blow-up" with "we have a result":

- **Tier 1 — Candidate:** one run yields a credible blow-up signal — a
  negative-slope linear fit of `1/‖ω‖∞(t)` extrapolating to a finite `T*`
  ahead of the run, clearing a high R² gate. This is the Beale–Kato–Majda
  reciprocal-vorticity diagnostic. Cheap to produce, cheap to fake.
- **Tier 2 — Numerically confirmed:** the candidate's `T*` **stabilizes under
  grid refinement** (≥3 resolutions, finest two within a tight relative
  tolerance). Strong evidence of a genuine singularity — still not a proof.
- **Tier 3 — Rigorously proven:** validated/interval-arithmetic proof. **Only
  Tier 3 answers Clay.** No pipeline here; out of scope by design.

**Only Tier 3 counts.** Tiers 1–2 are progress markers, and "the search didn't
find blow-up" is explicitly *not* treated as evidence of regularity.

## 2. The model family (a continuous bridge, viscosity from the start)

Jumping to 3D is infeasible for a GA needing thousands of cheap evaluations, so
we work on the **generalized Constantin–Lax–Majda (gCLM)** family on the
periodic circle:

```
ω_t + a·u·ω_x = ω·u_x + ν·ω_xx,     u_x = H(ω)   (H = Hilbert transform)
```

Two parameters are first-class, not hard-coded:

- **`a` (advection):** `a=0` is CLM, which has a *closed-form* blow-up for
  generic smooth data (a real-PDE analog of `ẏ=y²`); `a=1` is De Gregorio,
  where whether smooth data blows up is subtle and actively studied. Making `a`
  continuous gives a bridge from *proven* smooth-data blow-up (`a=0`) toward the
  hard regime (`a=1`).
- **`ν` (viscosity):** built in from the start. `ν=0` is the inviscid model;
  `ν>0` is what makes the search informative about the *viscous* (real
  Navier–Stokes) question rather than only its inviscid analog.

**Regularity caveat (the deepest scientific risk).** Established De Gregorio
blow-ups are for limited-regularity (Hölder, `C^{1,α}`) data; smooth data on the
circle is widely believed possibly-global. A bandlimited Fourier genome is
`C^∞`, so the search could be chasing an ever-finer-scale near-singularity —
a resolution artifact. Mitigations: the genome carries an evolvable spectral
decay exponent `p` (so rough profiles are representable), and `a` starts where
smooth blow-up is proven. This risk is what Stage 3 (and 3.5) exist to test.

## 3. Method

**Solver (Stage 1).** Pseudo-spectral (`rfft`); the Hilbert transform is a
Fourier multiplier; RK4 on the quadratic nonlinearities with 2/3 dealiasing;
viscosity by an exact integrating-factor step. Adaptive `dt` satisfies **both**
a vorticity constraint and the **advective CFL** for the `a·u·ω_x` transport
term. Conserved-quantity drift (mean-invariant; viscous energy-balance
residual) is tracked every run as an always-on artifact guard. Validated at
three levels — CLM analytic blow-up time, pure-diffusion Gaussian decay, and
advection/invariant conservation — tracked across commits in
`experiments/solver_validation.jsonl`. Code: [`../solver/`](../solver),
[`../win_condition.py`](../win_condition.py).

**Fitness viability first (Stage 1.5).** Before building the GA, we swept ~20
hand-picked ICs to check the intended fitness is non-degenerate. Result: **ν_crit
(at `a=0`) is a clean, resolution-exact, shape-dependent axis** (chosen);
`a_crit` was *rejected* — it drifts with resolution (a foreshadowing that
recurs in Stage 3.5). This de-risk cost a cheap sweep, not a GA build. See
[../STAGE_1_5_RESULTS.md](../STAGE_1_5_RESULTS.md).

**Genome.** First-N sine coefficients + an evolvable `k^{-p}` envelope exponent
(`p` = the smooth↔rough regularity axis). **Every genome is renormalized to a
fixed L² energy** after every operator — CLM-type equations are scale-covariant
(`ω→λω` blows up λ× faster), so without this the GA would trivially "win" by
cranking amplitude. Search is **MAP-Elites** keyed on shape descriptors
(spectral tail slope × sign-changes): the deliverable is a *map* of which shapes
resist viscosity, which is natively a quality-diversity problem. Code:
[`../ga/genome.py`](../ga/genome.py), [`../ga/operators.py`](../ga/operators.py),
[`../ga/evolve.py`](../ga/evolve.py).

**The bisection oracle.** One fitness evaluation = one warm-started bisection
locating ν_crit, with carefully pinned semantics (horizon-relative fitness;
censored bracket-edges excluded from the archive; per-genome monotonicity
probes; held-out exponent fitting so non-generic blow-ups aren't rejected by a
linear-fit R² gate). Logging is single-writer, append-only, per-event flushed,
with full genome coefficients and per-evaluation RNG seeds so any row is
independently reproducible ([../LOGGING.md](../LOGGING.md)).

## 4. The fitness axis took three tries — and the failures are findings

The Stage 2 acceptance criterion is **budget-matched**: the GA's best-so-far
curve must dominate random search *at equal evaluation counts* (comparing a GA's
best over thousands of draws to random's best over hundreds manufactures a
margin by order statistics alone).

- **Stage 2 (ν_crit at `a=0`): FAILED — and that is the finding.** The landscape
  has a trivially-located optimum (pile ≥99.5% of energy into `k=1`); random
  sampling reaches it as fast as the GA. This is the `ν·k²` dissipation scaling
  as global optimum — a spectral-concentration cheat, not a search problem.
- **Stage 2.5 (redesigns): no viable axis** — every variant of ν_crit stayed
  dominated by the same scaling. We introduced a **six-property viability gate**
  (nonzero, finite, monotone, resolution-stable, wide-band, **non-trivial
  optimum**) that a candidate axis must pass *before* any GA compute.
- **Stage 2.6 (oracle v3 + `a=0.7`): PASSED the gate.** Hardening the oracle to
  amplification-only blow-up decisions (removing fit-quality flicker) and moving
  to `a=0.7` — where advection kills the `k=1` refuge, so viscosity-resistance
  *requires* evolved structure — produced an axis passing all six properties.
  See [../STAGE_2_6_RESULTS.md](../STAGE_2_6_RESULTS.md).

## 5. Result 1 — the search works (Stage 2 acceptance)

On the frozen `a=0.7` / v3 axis, across 3 seeds (pop 24 × 25 generations,
interleaved budget-matched random baseline, re-validated literature control):

| seed | GA best ν_crit | random best | margin (tol units) | beats literature |
|---|---|---|---|---|
| 1 | 0.16236 | 0.15908 | **3.3** | ✓ |
| 2 | 0.16311 | 0.15850 | **4.6** | ✓ |
| 3 | 0.16287 | 0.15967 | **3.2** | ✓ |

**PASS (3/3; the criterion requires every seed).** The GA dominates random over
the final half of the budget on every seed and exceeds the best literature
profile every time; random never does — figure
[`fig1`](figures/fig1_ga_vs_random.png), data
[`data/ga_vs_random.json`](data/ga_vs_random.json). Improvements came from
variation (mutation + crossover), not luckier random draws, and were still
arriving at the generation budget's end. Independent seeds converge on
substantially the same shape→resistance map (final-archive Jaccard 0.62–0.72).

This is the *"the search method actually works"* milestone: evolutionary search
demonstrably beats budget-matched random on a verified, non-degenerate PDE
blow-up fitness.

## 6. Result 2 — the blow-ups are real, not grid artifacts (Stage 3, Tier 2)

The automated resolution study ([`../ga/resolution_study.py`](../ga/resolution_study.py))
reran the top-3 elites of each seed (9 genomes, 9 distinct archive cells) at
N ∈ {256, 512, 1024} under each elite's own frozen config, at two operating
points: an **inviscid anchor** (ν=0, gates promotion) and a
**viscosity-resistance** point (ν = 0.5·ν_crit ≈ 0.081). Amplification was
raised to 10⁴× so the `1/M→0` extrapolation is stressed over four decades of
growth. Conservation drift is the artifact guard (a drifted "blow-up" is refused
promotion regardless of a clean fit).

**All 18 studies → `NUMERICALLY_CONFIRMED`:**

| operating point | n | T\*(finest) | \|Δ\|/T\* (512→1024), max | max drift | α |
|---|---|---|---|---|---|
| inviscid (ν=0) | 9 | 2.173–2.258 | **3.5×10⁻⁶** | 6.7×10⁻⁵ | 1.000 |
| viscous (ν≈0.081) | 9 | 3.593–3.702 | **4.1×10⁻⁴** | 5.6×10⁻⁵ | 1.000 |

The gate is 2×10⁻²; convergence beats it by 50–5000×. Drift *shrinks* with N —
the opposite of an under-resolved run — and the top elite is T\*-identical
(2.17320) at N=2048, i.e. the singularity is fully resolved by N=256 and finer
grids move T\* by nothing. Figure
[`fig2`](figures/fig2_resolution_convergence.png); the classic BKM diagnostic
(`max|ω|→∞`, `1/M→0` linearly) for one elite is figure
[`fig4`](figures/fig4_blowup_curve.png). Data:
[`data/stage3_resolution.json`](data/stage3_resolution.json), and the 18 genomes
**with coefficients** in
[`data/promoted_candidates.jsonl`](data/promoted_candidates.jsonl). See
[../STAGE_3_RESULTS.md](../STAGE_3_RESULTS.md).

**Honest read of the exponent.** Every confirmed blow-up fits **α = 1.000** —
the *generic* CLM exponent `M ~ (T*−t)⁻¹`, not a non-generic De Gregorio one.
The physically honest interpretation: these are the CLM singularity surviving
`a=0.7` advection, exactly what one expects between proven-blow-up CLM (`a=0`)
and subtle De Gregorio (`a=1`). Tier-2 confirmation validates the pipeline and
the map; it is **not** a novel singularity.

## 7. Result 3 — the cheap route to novelty is closed (Stage 3.5)

If the confirmed blow-ups are known-type, the scientifically *novel*,
Tier-3-worthy target is a **non-generic (α≠1)** De Gregorio-type singularity.
A 240-run gate ([`../nongenericity_sweep.py`](../nongenericity_sweep.py)) asked
whether the GA's edge overlaps that target: measure the candidate fitness
**|α−1|** inviscid across `a ∈ {0.7, 0.9, 1.0} × N ∈ {256, 512}` over the
40-shape roster, gate on the six properties (single-run adaptations).

| a | blow-up | non-generic (\|α−1\|>noise) | resolution flips | verdict |
|---|---|---|---|---|
| **0.7** (GA edge) | 37/40 | **0** — α≡1 for *all* p | 0 | FAIL: dead-flat |
| **0.9** | 35/40 | 3 | **15/40** | FAIL: artifact |
| **1.0** | **0/40** | 0 | 0 | FAIL: dead axis |

**They are disjoint.** At `a=0.7`, blow-up is uniformly generic (α=1.000) across
the whole regularity range — Spearman(|α−1|, p) = −0.07, so roughness doesn't
move the exponent. Non-genericity appears only at `a=0.9`, and only as a
**resolution artifact**: 15/40 shapes flip blow-up/fit-reliability between N=256
and 512, and the biggest apparent |α−1| shapes **rail to α=3.0 at N=256 then
collapse to 0.3–0.6 at N=512** (max cross-resolution Δα = 2.7). This is the
Stage 1.5 `a_crit` instability reappearing on the exponent. `a=1.0` yields no
blow-up in the horizon at all. Figure
[`fig3`](figures/fig3_nongenericity.png), data
[`data/nongenericity.json`](data/nongenericity.json). See
[../NONGENERICITY_RESULTS.md](../NONGENERICITY_RESULTS.md).

A GA on a gCLM non-genericity axis would be optimizing grid noise. The gate
caught this for ~2 minutes of compute, before any GA campaign — the
anti-self-deception protocol doing exactly its job.

## 8. What is, and is not, a contribution

- **Is:** a validated end-to-end pipeline (solver → viability gate → QD search →
  resolution study), a demonstration that evolutionary search beats
  budget-matched random on a verified viscous-blow-up fitness, resolution-
  confirmed (Tier-2) candidates, and a reproducible shape→viscosity-resistance
  map on which independent seeds converge. The *negative* results (two dead
  fitness axes; the disjointness of edge and novelty) are themselves honest,
  reusable findings about this problem class.
- **Is not:** a novel singularity (the confirmed blow-ups are known-type CLM),
  a result about 3D Navier–Stokes (this is a 1D scalar model), or a proof
  (Tier 2 ≠ Tier 3). "A De Gregorio genome blows up" would in any case largely
  reproduce known results (Chen–Hou, Elgindi–Jeong); the plausibly-novel output
  was always the *map*, not the existence of blow-up.

**Overall probability of solving Clay via this program: ~0.05%.** Two structural
walls, not effort, set that ceiling: a search can only ever argue *for* blow-up
(never for regularity), and the only regimes where blow-up is *provable* today
are 1D/2D models, not 3D NS. The reachable, defensible win is the pipeline and
the map — which is complete.

## 9. Reproducibility

Every logged run pins a git commit; GA runs also freeze a `config.json`; the
logbook refuses to launch on a dirty tree. Per-evaluation RNG seeds make any
single genome evaluation reproducible standalone. Four test suites gate the
code (`../test_win_condition.py`, `../test_solver_clm.py`, `../test_logbook.py`,
`../test_ga.py`, plus `../test_resolution_study.py`). This folder's figures and
numbers rebuild from committed data via `writeup/build_figures.py`; the raw logs
(gitignored, large) regenerate from the committed sweep/GA scripts per the stage
docs. Forward plan: [../CLAY_ROADMAP.md](../CLAY_ROADMAP.md).
