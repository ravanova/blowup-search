# Plan: Solver + Evolutionary Search

This is the build-out plan for the next milestone referenced in
[PROJECT.md](PROJECT.md): a real PDE solver and genetic algorithm that feed
real fitness data into [win_condition.py](win_condition.py), instead of the
toy ODE used in [test_win_condition.py](test_win_condition.py).

Jumping straight to full 3D Navier–Stokes/Euler is not a sensible first step
— each simulation is expensive, and a GA needs thousands of cheap
evaluations per generation. So this plan stages up from a cheap, well-studied
1D toy model to the real target, validating the whole pipeline at each stage
before the compute cost increases.

## Prerequisite

**NumPy is not currently installed** in this environment (checked — no
numpy, no scipy). Stage 1 needs it for FFT-based spectral methods. Install
it before starting:
```
pip install numpy
```
SciPy is optional (only useful later for adaptive ODE integrators); not
required for Stage 1.

---

## Stage 1 — 1D toy blow-up model solver

**Goal:** a working, validated numerical solver for a 1D model equation known
in the literature to capture the vortex-stretching mechanism believed
responsible for 3D blow-up, cheap enough to run thousands of times.

Two models, in order:

1. **Constantin–Lax–Majda (CLM) equation**: `ω_t = ω · H(ω)`, where `H` is
   the Hilbert transform, on a periodic domain. This equation has a known
   **closed-form blow-up solution** for generic initial data — same role as
   our `dy/dt = y²` toy test, but now a real PDE with spatial structure.
   Use it purely to validate the solver: does the simulated `max|ω(t)|`
   match the analytic blow-up time?
2. **De Gregorio equation**: `ω_t + u·ω_x = ω·u_x`, `u_x = H(ω)`. Adding the
   advection term `u·ω_x` changes the picture — whether a given initial
   condition blows up or stays globally smooth is genuinely subtle and
   actively studied (Jia–Stewart–Šverák and others have found regularity for
   some data classes; blow-up is not settled in general). **This is the real
   search target for the GA**, not just a validation exercise.

**Method:** pseudo-spectral (FFT via `numpy.fft`) — the Hilbert transform is
a simple multiplication by `-i·sign(k)` in Fourier space. RK4 time-stepping.
2/3-rule dealiasing on the nonlinear product term. Adaptive `dt` tied to
`1/max|ω|` since the timestep must shrink as a candidate approaches blow-up.

**Viscosity is a solver parameter from the start, not deferred to Stage 4.**
Add a diffusion term `ν·ω_xx` to both models — trivial in Fourier space
(multiply by `exp(-ν k² dt)`, an integrating-factor step alongside the RK4
nonlinear update). Setting `ν=0` recovers the plain inviscid solver used for
the CLM validation below; `ν>0` is what makes Stage 2 actually informative
about the real (viscous) Navier–Stokes question rather than only its
inviscid analog.

**Symmetry restriction (a documented bias, not a neutral default):**
initially restrict to **odd functions** (standard in this literature, e.g.
Do–Kiselev–Ryzhik–Yao), which halves the genome's degrees of freedom and
matches how these models are usually studied. This is a deliberate,
revisitable choice, not a settled one — it rules out an entire region of the
search space and could accidentally exclude the shapes that matter. Plan an
unrestricted (general, non-symmetric) genome sweep as a follow-up once the
odd-symmetric search has been run, rather than treating the restriction as
permanent.

**Cross-validate against more than one known result.** The CLM check below
validates the solver against a closed-form solution, but De Gregorio itself
has published regularity/blow-up results for specific classes of initial
data. Wherever the genome search space overlaps a case with a known answer,
check the solver agrees before trusting its output more broadly — if the GA
ever reports blow-up in a regime already proven globally regular, that
means a solver bug, not a discovery. (Look up the specific applicable
results — e.g. Jia–Stewart–Šverák-type regularity classes — when Stage 1 is
actually implemented, rather than guessing at them now.)

**Deliverables:**
- `solver/spectral_utils.py` — FFT helpers, Hilbert transform, dealiasing.
- `solver/clm.py`, `solver/de_gregorio.py` — the two solvers, sharing the
  spectral utilities.
- `test_solver_clm.py` — validates CLM's simulated blow-up time against its
  known closed-form solution (same spirit as the existing ODE self-test).

**Acceptance criterion:** CLM solver **at `ν=0`**, via
`win_condition.estimate_blowup_time` on the simulated `max|ω(t)|` series,
matches the analytic blow-up time to within numerical tolerance across at
least 3 different initial conditions. Separately, confirm the `ν>0` diffusion
step is correct by checking pure-diffusion decay (`ω_t = ν·ω_xx` alone, no
nonlinear term) against its known Gaussian-decay solution. Only then move to
Stage 1.5.

---

## Stage 1.5 — Fitness-signal viability check (de-risk before building the GA)

**Goal:** cheaply verify that the Stage 2 fitness function (`ν_crit`) is a
non-degenerate, searchable quantity *before* investing in the full GA and
logging apparatus. This is the highest-leverage checkpoint in the plan: if
`ν_crit` is degenerate, Stage 2 as designed cannot work, and it is far
cheaper to discover that now than after building `ga/`.

**Why this is not obvious.** The entire Stage 2 design rests on
**fitness = `ν_crit`** (the critical viscosity above which the Tier 1
blow-up signal disappears for a given shape). That presupposes four things,
none of which is currently established for the viscous CLM / De Gregorio
models — and each is plausibly false:

1. **`ν_crit > 0` for some shapes.** For many 1D vorticity models, *any*
   positive viscosity regularizes (global existence for all `ν>0`). If that
   holds here, `ν_crit ≡ 0` for every genome and the fitness landscape is
   dead flat — the GA has nothing to climb. This is, in miniature, the real
   Navier–Stokes question, so the answer is genuinely not known in advance.
2. **`ν_crit` is finite** (blow-up doesn't survive arbitrarily large `ν`).
3. **`ν_crit` varies smoothly with shape** — a flat or binary landscape
   gives selection no gradient.
4. **"Blows up at viscosity `ν`" is monotone in `ν`.** Bisection is only
   valid if below `ν_crit` blows up and above it doesn't; a non-monotone
   response silently breaks the bisection in Stage 2's fitness.

**Method:** hand-pick ~20 initial conditions (include literature
blow-up-prone De Gregorio profiles and a spread of random shapes at fixed
energy), and for each, sweep `ν` directly — no GA — measuring `ν_crit` and
whether the blow-up/no-blow-up response is monotone. Also measure `ν_crit`
at two solver resolutions (e.g. N=256 and N=512): **if `ν_crit` drifts with
resolution, it is a numerical artifact, not a property of the shape** — the
viscous analog of the Tier-1-vs-artifact problem, one level up, and a
showstopper for using it as fitness.

**Acceptance criterion:** `ν_crit` is nonzero for at least some shapes,
finite, monotone in `ν`, resolution-stable, and spans a wide enough band
across the sample that shape differences are resolvable above numerical
noise. **If any of these fail, stop and redesign the fitness function
before Stage 2** — candidate fallbacks: fitness on blow-up *rate* at a
single fixed small `ν`, or a multi-objective (speed × viscosity-resistance)
score. Do not proceed to the full GA on an unverified fitness signal.

---

## Stage 2 — GA harness wired to `win_condition.py`

**Goal:** evolve De Gregorio initial conditions toward the fastest, most
convergent blow-up signal, using the Tier 1 diagnostic already built.

**Genome:** first `N` Fourier sine coefficients of `ω(x, 0)` (real vector,
`N` ≈ 32–64 to start).

**Critical design constraint — fixed energy budget:** CLM-type equations are
scale-covariant (`ω → λω` blows up `λ`× faster). Without a constraint, the GA
"solves" the search trivially by cranking amplitude rather than evolving
genuine structure. **Every genome must be rescaled to a fixed L² energy after
mutation/crossover**, so fitness differences reflect *shape*, not scale.

**Operators:**
- Selection: tournament selection.
- Crossover: blend/arithmetic crossover between two parent coefficient
  vectors.
- Mutation: per-gene Gaussian perturbation, mutation scale decaying over
  generations.
- Elitism: carry the top 1–5 genomes unchanged into the next generation.
- Re-normalize energy after every mutation/crossover (see constraint above).
- **Diversity via quality-diversity (MAP-Elites), not a single-objective GA
  with diversity bolted on.** A plain GA (even with fitness sharing or
  islands) tends to collapse onto whichever single blow-up mechanism it
  finds first, and then only *defends* diversity. But the stated scientific
  payoff here is a *map* of **which shapes resist viscosity** — that is
  natively a quality-diversity problem, not a single-objective one.
  **Reframe the search as MAP-Elites keyed on the shape descriptors we are
  already logging** (`n_sign_changes`, `spectral_centroid`,
  `energy_top_k_frac`; see [LOGGING.md](LOGGING.md) schema #3): discretize
  that descriptor space into cells and keep the highest-`ν_crit` genome per
  cell. This structurally guarantees diversity (one elite per shape niche
  instead of a converged population) *and* its output archive — best shape
  per niche — is exactly the "shape → viscosity-resistance map" the project
  wants, produced directly rather than reconstructed after the fact. Tournament
  selection then draws parents from the archive; crossover/mutation/energy
  renormalization are unchanged. (If Stage 1.5 shows the descriptor space is
  poorly covered or the map is trivial, fall back to an island-model GA — but
  MAP-Elites is the default because it matches the deliverable.)

**Fitness function — search for viscosity resistance, not just speed:**
"blows up fastest at `ν=0`" is not informative about the real (viscous)
question. Instead, for each genome, run the solver across a small set of
`ν` values (bisection) to find `ν_crit(genome)` — the critical viscosity
above which the Tier 1 blow-up signal disappears for that shape. **Fitness
= `ν_crit`.** The GA evolves initial-condition shapes toward the most
viscosity-resistant blow-up, which is exactly the property that would
matter for the real Navier–Stokes equation. Within each bisection step,
`max|ω(t)|` is still fed into `estimate_blowup_time` exactly as before;
`None` at a given `ν` means "no blow-up at this viscosity," `BlowupEstimate`
means "blow-up survives" — bisect on that boolean outcome to locate
`ν_crit`.

**Detect blow-up with the exponent-fitting diagnostic, not the plain linear
fit.** The default `estimate_blowup_time` fits `1/max|ω|` as a straight line,
which is exact only for CLM-style generic blow-up (`M ~ (T*-t)^{-1}`). De
Gregorio blow-up is generally *non-generic* (`M ~ (T*-t)^{-α}`, `α ≠ 1`),
which makes the reciprocal curved — a linear fit then depresses `R²` and can
reject genuine blow-ups at the `R² ≥ 0.98` gate, i.e. throw away exactly what
we're hunting. Call `estimate_blowup_time(..., fit_exponent=True)` in the GA
fitness path so the exponent `α` is fit and logged (`win_condition.py`
already supports this and self-tests it against a synthetic `α=2` blow-up).

**Fix and log the fitness solver resolution; guard `ν_crit` against
resolution artifacts.** Blow-up drives energy to high wavenumbers, where the
viscous term `ν·k²` dominates — so measured `ν_crit` depends on solver
resolution. Evaluate all fitness at one fixed resolution and record it in
every `genome_eval` entry (not just in `solver_run`), so a `ν_crit` reported
at low resolution can never be silently compared against one at high
resolution. Periodically re-measure the current elites' `ν_crit` at a higher
resolution (this is cheaper than, and complementary to, the full Stage 3
resolution study); if `ν_crit` drifts, the fitness signal for that region is
artifact-driven, not physical.

**Guard against a frequency-space analog of amplitude-cheating.** Fixing L²
energy kills the obvious `ω → λω` cheat, but `ν·k²` means energy at *low*
wavenumbers survives viscosity almost for free. So `ν_crit` fitness can be
gamed by piling energy into low-`k` modes (large, smooth, viscosity-immune
structures) — a scaling trick, not genuine blow-up structure. Monitor
`spectral_centroid` (already logged) as a guardrail: if evolved high-`ν_crit`
genomes are drifting toward ever-lower centroid rather than developing sharp
localized structure, the fitness is being gamed and needs a bandwidth
constraint or a centroid-normalization alongside the energy budget.

**Deliverables:**
- `ga/genome.py` — genome representation, energy-renormalization.
- `ga/operators.py` — selection/crossover/mutation.
- `ga/evolve.py` — main GA loop, logs best genome + tier per generation.
- `ga/logbook.py` — structured run/generation/genome logging; see
  [LOGGING.md](LOGGING.md) for the schema and rationale.
- `experiments/` — run logs and saved best-genome coefficient vectors
  (layout specified in LOGGING.md).

**Acceptance criterion:** across multiple independent GA runs (different
random seeds), the population reliably evolves genomes whose `ν_crit`
clears a random-initial-condition-shape baseline by a clear margin — i.e.
evolved shapes sustain blow-up at meaningfully higher viscosity than
unoptimized shapes of the same energy.

---

## Stage 3 — Automated resolution-study loop (Tier 2 promotion)

**Goal:** automatically promote promising genomes from Tier 1 to Tier 2.

Periodically (e.g. every 10 generations, or whenever a new best genome
appears), rerun the current best genome(s) at increasing spectral resolution
(e.g. N = 256, 512, 1024 modes) and feed the resulting `T*` estimates into
`resolution_converged`. Genomes that pass become flagged
`NUMERICALLY_CONFIRMED` and are set aside for manual review — this is
expensive, so it should not run every generation on the whole population,
only on the current leaders.

**Deliverable:** `ga/resolution_study.py`, plus a log of any genome reaching
Tier 2.

**Acceptance criterion:** at least one De Gregorio genome reaches
`NUMERICALLY_CONFIRMED`, or we have strong reason to believe (after
substantial search) that De Gregorio initial data in the explored genome
space stays globular — in which case, per WIN_CONDITION.md, that is *not* a
proof of regularity, just a signal to widen the search (larger `N`, different
symmetry class, or move to Stage 4).

---

## Stage 4 — Scale-up to axisymmetric 3D Euler (stretch goal, unscheduled)

Once the 1D pipeline reliably produces Tier 2 candidates, repeat the same
genome → solver → fitness → GA → resolution-study loop on the **axisymmetric
3D Euler equations with swirl** — the actual scenario used in Hou & Luo's
numerical blow-up search, and the real target Navier–Stokes stepping stone.

This is a much larger lift: a finite-difference or spectral solver on a
cylindrical domain, adaptive mesh refinement near the developing
singularity, and likely enough compute cost to require a compiled solver
(not pure NumPy) or GPU acceleration. **Not scheduled with concrete steps
yet** — revisit sizing this once Stage 3 produces results, since what we
learn about genome representation and fitness shaping in 1D will directly
inform the 3D design.

---

## Stage 5 — Tier 3 rigorous computer-assisted proof pipeline (research spike, unscheduled)

Out of scope for the GA/solver work itself. Converting a Tier 2 numerical
candidate into an actual proof requires validated numerics / interval
arithmetic (e.g. tooling in the style used by Buckmaster & Gómez-Serrano).
Not worth designing in detail until Stage 3 or 4 hands us a concrete Tier 2
candidate to validate — the right tooling depends heavily on the specific
equation and profile involved.

---

## Proposed directory layout

```
Unsolved/
├── PROJECT.md
├── WIN_CONDITION.md
├── PLAN.md                     (this file)
├── millennium_prize_problems.md
├── win_condition.py            (done)
├── test_win_condition.py       (done)
├── solver/
│   ├── spectral_utils.py
│   ├── clm.py
│   └── de_gregorio.py
├── test_solver_clm.py
├── ga/
│   ├── genome.py
│   ├── operators.py
│   ├── evolve.py
│   └── resolution_study.py
└── experiments/
    └── run_logs/
```

## Honest scope caveat

Stages 1–3 use **CLM and De Gregorio, which are 1D toy models** — not the
real 3D Navier–Stokes equations. As of the latest revision, viscosity is
built into the solver from Stage 1 and Stage 2's fitness function explicitly
searches for blow-up that survives viscosity (`ν_crit`), which addresses the
most serious version of the earlier gap: we are no longer optimizing purely
inviscid behavior and hoping it transfers.

What remains genuinely open, and is **not** resolved by this revision:
- These are still 1D scalar models, not the actual 3D vector Navier–Stokes
  system — a high `ν_crit` in De Gregorio is evidence the overall strategy
  (evolve shapes for viscosity-resistant blow-up) is worth running at all,
  not evidence about the real equation. That transfer only starts to mean
  something at Stage 4 (axisymmetric 3D Euler/Navier–Stokes).
- Precedent for caution: Elgindi's 2021 proof of finite-time singularity
  formation for 3D Euler required Hölder-continuous (not smooth) velocity
  fields, and was inviscid — even that landmark result doesn't transfer
  cleanly to smooth data or to the viscous case, illustrating how much
  regularity and viscosity can matter to the outcome.
- Tier 3 (an actual rigorous proof, in either direction) still has no
  pipeline — Stage 5 remains unscheduled research.

**What would actually be novel here (so we don't spend compute rediscovering
known results).** De Gregorio finite-time blow-up for *specific* classes of
initial data is already studied and partly established (Chen–Hou–Huang,
Elgindi–Jeong lines of work). So "a De Gregorio genome blows up" is, on its
own, not a contribution — it may just reproduce a known result. The plausibly
novel output of Stages 1–3 is the **quality-diversity map of viscosity
resistance across shape space** (Stage 2's MAP-Elites archive): a systematic
picture of *which* shape families sustain blow-up at the highest viscosity,
and whether independent runs converge on the same families. Frame findings
against the existing literature results before claiming anything.

**Honest near-term definition of success.** Achieving the Clay problem itself
is gated entirely on Stage 4+, which is unscheduled and admittedly a large
lift. The *reachable* near-term win is Stages 1–3: a validated solver, a
non-degenerate fitness signal (Stage 1.5), and a working quality-diversity
pipeline that produces a defensible shape → viscosity-resistance map on De
Gregorio, with reproducible Tier-1/Tier-2 candidates. That is the finish line
these improvements are optimized for; the Millennium result is a stretch
beyond it, not the near-term deliverable.

## Open risks

- **`ν_crit` degeneracy** — the deepest risk to the whole Stage 2 design: if
  any positive viscosity regularizes these 1D models, `ν_crit ≡ 0` and the
  fitness landscape is flat. This is why Stage 1.5 exists — it must be ruled
  out with a cheap direct sweep *before* the GA is built, not discovered
  after.
- **Scale-covariance cheating** (amplitude) — mitigated by the
  fixed-energy-budget rule above; needs a unit test confirming
  renormalization is actually applied after every genetic operator.
- **Frequency-space cheating** (the subtler sibling) — energy piled into
  low-`k` modes resists viscosity trivially, so `ν_crit` fitness can be gamed
  without genuine blow-up structure; monitored via `spectral_centroid`, may
  need a bandwidth constraint (see Stage 2 fitness section).
- **`ν_crit` resolution-dependence** — `ν_crit` measured at fitness
  resolution can be a numerical artifact; mitigated by fixing/logging the
  fitness resolution and re-checking elites at higher resolution (Stage 1.5
  and Stage 2).
- **Numerical blow-up vs. resolution artifact** — this is exactly why Stage
  3 exists; a Tier 1 hit is never reported as more than a candidate.
- **Compute cost at Stage 4** — likely the biggest real bottleneck; sizing
  it accurately isn't possible until Stage 3 tells us how large a genome/
  resolution we actually need for a convincing candidate in 1D.
- **Bisection cost for `ν_crit`** — locating the critical viscosity per
  genome means multiple solver runs per fitness evaluation (roughly
  `log2(range/tolerance)`), multiplying Stage 2's compute cost. Worth
  watching once Stage 1/2 are actually running; not worth redesigning
  around before we have real timing data.

## Stopping point for design-only iteration

This plan has now been through three rounds of refinement without a line of
solver code written. Each was worth doing — the viscosity reframe, and now
the Stage 1.5 fitness-viability de-risk plus the MAP-Elites reframe, would
all have been expensive to retrofit later — but further paper-only iteration
has clearly hit diminishing returns. The remaining open items (bisection
cost, exact MAP-Elites cell resolution, which published De Gregorio results
to check against) are all better resolved by writing **Stage 1, then the
Stage 1.5 viability sweep**, and reacting to real numbers than by further
speculation. Stage 1.5 in particular is deliberately cheap and comes *before*
the GA precisely so the biggest design risk (`ν_crit` degeneracy) is settled
empirically, not on paper. Next step is implementation, not another planning
pass — concretely: **Stage 1 → Stage 1.5 → decide fitness → Stage 2.**
