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
2. **Generalized CLM (gCLM) family**: `ω_t + a·u·ω_x = ω·u_x`, `u_x = H(ω)`,
   with the **advection coefficient `a` a solver parameter**, not hardcoded.
   `a=0` recovers CLM (validation model above); `a=1` is the De Gregorio
   equation. The advection term `a·u·ω_x` fights the growth, and whether a
   given initial condition blows up or stays globally smooth is genuinely
   subtle and actively studied (Okamoto–Sakajo–Wunsch mapped this numerically;
   Jia–Stewart–Šverák and others have found regularity for some data classes;
   Elgindi–Jeong and Chen–Hou–Huang established blow-up for limited-regularity
   data — see the regularity caveat below). **The gCLM family is the real
   search target for the GA**, not just a validation exercise.

   Making `a` a first-class parameter is deliberate and high-value: it gives a
   *continuous bridge* from the regime where smooth-data blow-up is **proven**
   (`a=0`, CLM) into the subtle regime near `a=1`. That directly de-risks the
   central worry that smooth genomes may not blow up at all at `a=1` (see the
   regularity caveat), and it hands the GA a second, better-behaved fitness
   axis — `a_crit` — discussed under Stage 2.

**Regularity caveat — the genome is smooth, but the blow-up may not be.**
The established De Gregorio blow-up results are for *limited-regularity*
(Hölder, e.g. `C^{1,α}`) data, and smooth data on the circle is widely
believed to possibly stay regular. This is the same subtlety flagged for the
Elgindi 3D Euler precedent in the scope caveat: that landmark blow-up needed
`C^{1,α}` velocity, not smooth. A bandlimited truncated-Fourier genome is
`C^∞` by construction, so it may be searching an empty set, with growing `N`
just chasing a singularity that forms at ever-smaller scales — a resolution
artifact, not a discovery. **Mitigation is built into the genome
representation** (see Stage 2): the genome parameterizes a coefficient-decay
envelope so limited-regularity profiles are representable, rather than
assuming smoothness away.

**Method:** pseudo-spectral (FFT via `numpy.fft`) — the Hilbert transform is
a simple multiplication by `-i·sign(k)` in Fourier space. RK4 time-stepping.
2/3-rule dealiasing on the nonlinear product terms (both `a·u·ω_x` and
`ω·u_x` are quadratic, so 2/3 suffices). Adaptive `dt` must satisfy **two**
constraints, not one: `dt = min(c₁/max|ω|, c₂·dx/max|u|)`. The first shrinks
the step as a candidate approaches blow-up (as before); the second is the
**advective CFL** condition, which the earlier `1/max|ω|`-only policy omitted —
without it the `a·u·ω_x` transport term is under-resolved exactly when `a` is
large, silently corrupting the regime the search cares about. Log the realized
`dt` sequence (see LOGGING.md) so an adaptive run remains reproducible to
tolerance across machines.

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
- `solver/spectral_utils.py` — FFT helpers, Hilbert transform, dealiasing,
  and the conserved-quantity evaluations used as an artifact guard (below).
- `solver/gclm.py` — a single gCLM solver parameterized by `(a, ν)`; `a=0`
  is CLM, `a=1` is De Gregorio, so there is one code path to validate, not
  two divergent ones.
- `test_solver_clm.py` — validates the solver against known results at three
  levels (below).

**Acceptance criterion — three checks, because CLM alone does not exercise
the hard part.** CLM (`a=0`) has *no advection term*, and pure diffusion has
*no nonlinearity*, so a solver can pass both while its `a·u·ω_x` transport
operator is completely wrong — and that operator is the entire difficulty of
De Gregorio. All three must pass before Stage 1.5:
1. **Growth/Hilbert term (`a=0`, `ν=0`):** via
   `win_condition.estimate_blowup_time` on the simulated `max|ω(t)|`, match
   CLM's analytic blow-up time to within numerical tolerance across ≥3
   initial conditions.
2. **Diffusion term (`ν>0`, nonlinearity off):** pure-diffusion decay
   (`ω_t = ν·ω_xx` alone) against its known Gaussian-decay solution.
3. **Advection term (`a>0`) — the check the old plan was missing:** exercise
   transport directly, by at least one of — a frozen-`u` pure-transport test
   against a known translated solution; conservation of the gCLM invariants
   (tracked continuously, see below); and reproducing a published
   Okamoto–Sakajo–Wunsch critical-`a` value for a known profile. Do not let
   Stage 1 go green with advection untested.

**Conserved quantities as a cheap, always-on artifact guard.** The gCLM
family has invariants (energy-type / Hamiltonian quantities). Their numerical
drift is a direct, per-run signal that a simulation is under-resolved —
available on *every* evaluation, long before Stage 3's expensive resolution
study. `spectral_utils.py` exposes these; every solver run logs their drift
(see LOGGING.md), and a "blow-up" whose invariants drifted is treated as an
artifact regardless of how clean its `1/M` fit looks. **Two caveats the
implementation must respect.** First, an invariant can be *trivially* zero
under the active symmetry class — `∫ω dx` is conserved across the whole gCLM
family (both `∫ω·H(ω)` and `∫u·ω_x` vanish by the Hilbert transform's
antisymmetry), but it is identically zero for odd data, so under the odd
restriction its drift measures nothing; verify the tracked invariants are
informative under the configured symmetry, and normalize drift by a solution
scale (e.g. `‖ω‖₁`), never by the invariant's own possibly-zero value.
Second, for `ν>0` nothing is conserved at all — the viscous guard is the
**energy-balance residual** (nonlinear production minus `ν`-dissipation,
which nets to zero when resolved), not raw conservation.

---

## Stage 1.5 — Fitness-signal viability check (de-risk before building the GA)

> **DONE (2026-07-22) — verdict: `ν_crit` is the Stage 2 fitness axis.**
> Full numbers in [STAGE_1_5_RESULTS.md](STAGE_1_5_RESULTS.md). Summary:
> `ν_crit` (at a=0) passed all five acceptance properties — nonzero for
> 18/19 uncensored shapes, finite, monotone (0 probe violations),
> resolution-*exact* (every N=256 vs N=512 value identical), spread
> 0.006–0.053 with physically sensible structure. `a_crit` (at ν=0) failed
> resolution stability — tail(p=1)'s value halves from N=256 to N=512, and
> the a≈0.85–1.0 cluster wobbles by up to 13× the bisection tolerance —
> so it is rejected despite passing the other four. The sweep also forced
> two amendments to the bisection predicate that now bind Stage 2's oracle:
> an amplification stop is a blow-up regardless of tail-fit quality, and
> fit-based blow-up requires T* ≤ 1.5·t_max (uncapped forward extrapolation
> was the source of v1's censored-high/resolution-flip anomalies).

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
energy), and for each, sweep **both** control parameters directly — no GA:
- **`ν` sweep (viscosity-resistance):** measure `ν_crit` and whether the
  blow-up/no-blow-up response is monotone in `ν`.
- **`a` sweep (advection-resistance):** at `ν=0`, measure `a_crit` — the
  largest advection coefficient at which the shape still blows up — and its
  monotonicity in `a`.
Measure both at two solver resolutions (e.g. N=256 and N=512), holding one
fixed simulation horizon `t_max` across every sweep run — critical values
are horizon-relative (see Stage 2's fitness definition), so a sweep with
varying horizons measures nothing. **If `ν_crit` or `a_crit` drifts with
resolution, it is a numerical artifact, not a property of the shape** — the
analog of the Tier-1-vs-artifact problem one level up, and a showstopper for
using either as fitness.

**Why sweep `a` too — `ν_crit` is at real risk of being degenerate, `a_crit`
much less so.** In 1D, parabolic smoothing is strong, so there is a genuine
chance *any* `ν>0` regularizes every shape (`ν_crit ≡ 0`, dead-flat
landscape — risk #1 in Open Risks). `a_crit` is far more likely to be
well-behaved: "for which `a` does a given smooth shape blow up" is *precisely*
the actively-studied, positive, finite, shape-dependent question (Okamoto–
Sakajo–Wunsch, Elgindi–Jeong). It is also cheaper — inviscid runs, no viscous
stiffness. So this stage measures both up front and lets the data pick the
fitness, rather than committing Stage 2 to `ν_crit` and discovering it is flat
after `ga/` is built.

**Acceptance criterion:** *at least one* of `ν_crit` or `a_crit` is, across
the sample, nonzero for some shapes, finite, monotone in its parameter,
resolution-stable, and spans a wide enough band that shape differences are
resolvable above numerical noise. **Whichever passes becomes the Stage 2
fitness** (preferring `a_crit` if both pass, since it is cheaper and its
landscape is better-understood). **If neither passes, stop and redesign the
fitness before Stage 2** — further fallbacks: blow-up *rate* at a fixed small
`ν` or fixed `a`, or a multi-objective (speed × resistance) score. Do not
proceed to the full GA on an unverified fitness signal.

---

## Stage 2 — GA harness wired to `win_condition.py`

> **BUILT AND RUN (2026-07-22, commit d47b579) — acceptance criterion NOT
> MET, for a reason that is itself the finding.** Across 3 seeds
> (stage2-seed1/2/3: 600 GA + 612 baseline evals each, ~12,200 solver runs
> per seed), the GA's best-so-far `ν_crit` NEVER separated from the
> budget-matched random baseline (margins 0, 0, 0.2× tolerance): the
> `ν_crit` landscape at a=0 has a **trivially-located global optimum** —
> ≥99.5% of energy in k=1 — which both searches reach within ~12
> evaluations. This is the νk² scaling argument as global optimum; the
> "frequency-space cheating" risk below turned out to be the axis's honest
> answer, not a cheat. Sharper still: random sampling *beats* the GA at
> map-building too (74–79% archive coverage vs 46–58% at matched budget) —
> on a saturated landscape, fitness-driven selection is pure cost. The
> harness itself passed every operational check (censoring, monotonicity
> probes, warm starts, budget matching, single-writer logging) and is
> reusable as-is for any scalar fitness. Full numbers in
> [STAGE_2_RESULTS.md](STAGE_2_RESULTS.md); analysis in analyze_stage2.py.
> **Next milestone: Stage 2.5 below** — redesign the fitness axis, gate it
> on the extended six-property viability checklist, then rerun the 3-seed
> acceptance unchanged.

**Goal:** evolve De Gregorio initial conditions toward the fastest, most
convergent blow-up signal, using the Tier 1 diagnostic already built.

**Genome:** first `N` Fourier sine coefficients of `ω(x, 0)` (real vector,
`N` ≈ 32–64 to start), **plus an evolvable spectral-decay exponent `p`**
controlling the coefficient envelope. Rather than a hard truncation (which
forces a `C^∞`, bandlimited — hence possibly non-blow-up — profile; see the
Stage 1 regularity caveat), the genome multiplies its raw coefficients by a
`k^{-p}` envelope, so the GA can evolve toward limited-regularity (rough,
slowly-decaying-tail) shapes when those are what sustain blow-up. Small `p` =
rough/Hölder-like; large `p` = smooth. This makes the very regularity axis the
literature says matters (Hölder vs. smooth) a searchable genome dimension
instead of a hidden constant, and `p` doubles as a natural shape descriptor
(below). `N` is still the numerical truncation; `p` shapes how energy is
distributed *within* it.

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
  already logging** (`n_sign_changes`, `spectral_tail_slope`,
  `energy_top_k_frac`; see [LOGGING.md](LOGGING.md) schema #3): discretize
  that descriptor space into cells and keep the highest-fitness genome per
  cell. Prefer **`spectral_tail_slope`** (how fast the coefficient tail
  decays — directly the smooth-vs-Hölder regularity axis the physics cares
  about, and the same quantity the evolvable envelope exponent `p` controls)
  over `spectral_centroid`, which is strongly correlated with
  `energy_top_k_frac` and would waste an archive dimension. This structurally guarantees diversity (one elite per shape niche
  instead of a converged population) *and* its output archive — best shape
  per niche — is exactly the "shape → viscosity-resistance map" the project
  wants, produced directly rather than reconstructed after the fact. Tournament
  selection then draws parents from the archive; crossover/mutation/energy
  renormalization are unchanged. (If Stage 1.5 shows the descriptor space is
  poorly covered or the map is trivial, fall back to an island-model GA — but
  MAP-Elites is the default because it matches the deliverable.)

**Fitness function — search for resistance to regularization, not just
speed:** "blows up fastest at `ν=0`, `a=0`" is not informative about the real
question. Instead, fitness is the critical-resistance parameter chosen by
Stage 1.5 — **decided: `ν_crit` at fixed `a=0`** (`a_crit` failed Stage 1.5's
resolution-stability gate; see [STAGE_1_5_RESULTS.md](STAGE_1_5_RESULTS.md)).
Stage 2 config accordingly: `fitness_axis="nu_crit"`, `gclm_a=0.0`, bisection
range [0, 0.1] with tolerance ≤ 1e-3 (or log-ν bisection — the measured band
is 0–0.053 under the frozen stop criteria: t_max=12, amplification 100×,
tail fraction 0.15, held-out R² floor 0.9, T* cap 1.5·t_max). The generic
definition, for reference:
- `ν_crit(genome)`: critical viscosity above which the Tier 1 signal
  disappears.
- `a_crit(genome)`: at `ν=0`, critical advection coefficient above which it
  disappears — the largest `a` at which the shape still blows up.
The GA evolves shapes toward the most regularization-resistant blow-up, which
is the property that would matter for the real Navier–Stokes equation. Within
each bisection step, `max|ω(t)|` is fed into `estimate_blowup_time` exactly as
before. Everything downstream (MAP-Elites, logging, resolution study) is
written against a generic scalar fitness so switching `a_crit`↔`ν_crit`
touches only the bisection axis, not the rest of the pipeline.

**Pin down what the bisection oracle actually is — three decisions that
change the measured fitness:**

1. **The critical value is horizon-relative: fitness is `ν_crit(t_max, N)`,
   not `ν_crit`.** "No blow-up at this `ν`" can only ever mean "no blow-up
   within simulated time `t_max`" — a shape that blows up at `t=50` when the
   run stops at `t=10` gets classified regular. So the stopping criteria
   (`t_max`, max steps, the `max|ω|` amplification factor that declares
   blow-up) are frozen in each experiment's config exactly like
   `fitness_resolution_N` (see LOGGING.md schema #1), and critical values
   from runs with different horizons are never comparable.
2. **The blow-up predicate is "estimate exists AND held-out `R² ≥` a floor
   (~0.9)", recorded in config as `bisection.predicate_r2_floor`.** The two
   obvious choices are both wrong: bare "`estimate is not None`" lets any
   noisy negative-slope wobble count as blow-up, and Tier 1's 0.98 gate is
   too brittle for an oracle that gets queried precisely where fits are
   marginal (near the critical value). A middle floor makes the bisection
   robust while the 0.98 gate still decides what counts as a *candidate*.
   Edge semantics: a run cut short by the amplification threshold with too
   few samples to fit (`win_condition.InsufficientDataError`) **is a
   blow-up** — it hit the blow-up stop condition; treating the exception as
   "no signal" would flip the bisection against the fastest-blowing-up
   genomes. Any other short-run cause is an `error` event, not evidence.
3. **Bracket-edge outcomes are censored data, not measurements.** A genome
   regular at the easiest end of the range, or still blowing up at the
   hardest end, gets `critical_value` = the range edge with
   `bracket_censored` set ("low"/"high" in LOGGING.md schema #3) — and
   censored values never enter the MAP-Elites archive or any analysis as if
   they were true critical values. Both cases will happen constantly.

Relatedly, bisection *assumes* the response is monotone in the parameter and
cannot falsify that from its own samples — so `critical_value_monotone` is
measured explicitly by probing 1–2 parameter values beyond the located
critical value on the "regular" side after bisection converges (any blow-up
out there flags a broken fitness signal for that shape; Stage 1.5 checks
this globally, the probe keeps checking it per-genome forever).

**Detect blow-up with the exponent-fitting diagnostic, not the plain linear
fit.** The default `estimate_blowup_time` fits `1/max|ω|` as a straight line,
exact only for CLM-style generic blow-up (`M ~ (T*-t)^{-1}`). De Gregorio
blow-up is generally *non-generic* (`M ~ (T*-t)^{-α}`, `α ≠ 1`), making the
reciprocal curved — a linear fit then depresses `R²` and can reject genuine
blow-ups at the `R² ≥ 0.98` gate, i.e. throw away exactly what we're hunting.
Call `estimate_blowup_time(..., fit_exponent=True)` in the GA fitness path so
the exponent `α` is fit and logged. **The exponent is selected by held-out
(out-of-sample) validation, not by maximizing `R²` over the exponent grid** —
argmax-`R²` over ~55 candidate exponents is a garden-of-forking-paths trap
that inflates `R²` and manufactures false candidates; `win_condition.py` fits
`α` on the first half of the tail and gates on its `R²` over the held-out
second half (self-tested against a synthetic `α=2` blow-up), so the reported
`R²` is honest and the logged value is the one the Tier 1 gate judges.

**Fix and log the fitness solver resolution; guard the critical parameter
against resolution artifacts.** Blow-up drives energy to high wavenumbers,
where both the viscous term `ν·k²` and the sharpest transport gradients live —
so measured `ν_crit`/`a_crit` depends on solver resolution. Evaluate all
fitness at one fixed resolution and record it in every `genome_eval` entry
(not just in `solver_run`), so a critical value reported at low resolution can
never be silently compared against one at high resolution. Periodically
re-measure the current elites' fitness at a higher resolution (cheaper than,
and complementary to, the full Stage 3 resolution study); if it drifts, the
fitness signal for that region is artifact-driven, not physical.

**Guard against a frequency-space analog of amplitude-cheating.** Fixing L²
energy kills the obvious `ω → λω` cheat, but a low-frequency escape hatch
remains: for `ν_crit`, energy at low `k` survives `ν·k²` almost for free; for
`a_crit`, large smooth structures resist advective breakup. Either way, the
fitness can be gamed by piling energy into low-`k` modes — a scaling trick,
not genuine blow-up structure. Monitor `spectral_tail_slope`/`spectral_centroid`
(already logged) as a guardrail: if evolved high-fitness genomes drift toward
ever-smoother, lower-frequency shapes rather than sharp localized structure,
the fitness is being gamed and needs a bandwidth constraint or a
centroid-normalization alongside the energy budget. (This is the *opposite*
failure from the regularity caveat's over-smoothing worry, and the same
descriptor catches both — watch it in both directions.)

**Compute plan — four cheap mitigations for the bisection-cost risk.**
Bisection cost is this plan's top flagged compute risk; these four standard
mitigations plausibly buy a 5–20× effective speedup and cost little to
design in now (each is miserable to retrofit):

1. **Parallel fitness evaluation.** Evaluations are embarrassingly parallel;
   run them in a `multiprocessing` pool (`n_workers` in config).
   `blas_threads=1` is already pinned for determinism, which is exactly the
   right setting for process-level parallelism; per-evaluation RNG seeds
   (LOGGING.md's RNG principle) make results order-independent so
   parallelism cannot change outcomes. Logging consequence: workers never
   write files — all events go over a queue to the single writer process
   (see LOGGING.md).
2. **Warm-start the bisection bracket** from the parent's critical value ± a
   margin — children resemble parents, so most bisections start from a
   bracket far narrower than the full config range. If the bracket fails
   (both ends on the same side), widen toward the full range and count it
   (`n_bracket_expansions` in schema #3); a high expansion rate means the
   margin is mistuned.
3. **Early exit for clearly-decaying runs.** The expensive solver runs are
   the *no-blow-up* ones — they burn the whole `t_max`. An explicit
   early-decay rule (e.g. `max|ω|` below a fraction of its initial value and
   monotonically shrinking over a window; frozen in config's
   `stop_criteria`) cuts the dominant cost, logged as `early_exit_reason` so
   it is auditable.
4. **Fitness cache keyed on genome hash.** The solver is deterministic and
   elitism re-inserts identical genomes every generation — cache fitness by
   `genome_hash` so elites cost nothing to carry. Cache hits are still
   logged (`cache_hit: true`) so evaluation counts stay honest for the
   budget-matched baseline comparison below.

**Deliverables:**
- `ga/genome.py` — genome representation (coefficients + spectral-decay
  exponent `p`), energy-renormalization applied after the envelope.
- `ga/operators.py` — selection/crossover/mutation (including mutation of `p`).
- `ga/evolve.py` — main GA loop, logs best genome + tier per generation.
- `ga/logbook.py` — structured run/generation/genome logging; see
  [LOGGING.md](LOGGING.md) for the schema and rationale.
- `experiments/` — run logs and saved best-genome coefficient vectors
  (layout specified in LOGGING.md).

**Acceptance criterion — budget-matched, not just "beats baseline":** across
multiple independent GA runs (different random seeds), the GA's best-so-far
critical-fitness curve (`a_crit` or `ν_crit`, per Stage 1.5), plotted against
**cumulative fitness evaluations**, clearly dominates a random-search
baseline given the **same total evaluation budget** at the same energy
budget. The budget matching is the point: comparing the GA's best over
`population × generations` evaluations against a baseline's best over one
population's worth of draws manufactures a "clear margin" by order
statistics alone — the max of 5,000 draws beats the max of 100 from the same
distribution every time. The logs support the honest comparison for free
(`genome_eval` events are ordered and tagged by `operator`; see LOGGING.md).
Passing means evolved shapes sustain blow-up under meaningfully more
regularization than random search finds with identical compute.

---

## Stage 2.5 — Fitness-axis redesign (response to Stage 2's verdict)

> **RUN (2026-07-22, commits f3dc522 + a005ef8) — verdict: NO VIABLE AXIS;
> stopped for review without running the GA.** Candidate A fails the
> six-property gate at every a: a=1.0 is a dead axis (35/40 shapes
> censored low — smooth-data blow-up essentially vanishes at De Gregorio
> within the horizon); a=0.7 fails monotonicity, symptomatic of a systemic
> softness (100% of a>0 boundary decisions are fit-decided on slow α≈0.3
> growth with T* near the horizon cap, vs 100% amplification-decided at
> a=0); a=0.4 fails the non-trivial optimum (prior reaches within 7·tol of
> the top; ρ(ν_crit, k1frac)=0.79). Candidate B fails exactly by its
> pre-stated risk: the optimum pins to the k≤2=50% cap boundary (7-way tie
> at ν_crit=0.0379, all at exactly 0.5; best prior EQUALS best structured,
> gap 0.0·tol; ρ(k1)=0.91). Conclusion: ν_crit on gCLM at fixed horizon is
> dominated by the νk² dissipation scaling in every variant — a spectral-
> concentration quantity the init prior samples directly; no search method
> can beat prior sampling on it. The acceptance rerun was therefore NOT
> executed (per this stage's own gate). Full data and the three
> redesign-level paths forward (oracle v3 + a=0.7, rate-based fitness,
> scaling-normalized ν_crit, or accept the negative result):
> [STAGE_2_5_RESULTS.md](STAGE_2_5_RESULTS.md). **Review outcome
> (2026-07-22): proceed with paths 1+2 combined — harden the oracle AND
> reformulate the fitness quantity, gate everything through the
> six-property check before any GA compute. Spec: Stage 2.6 below.
> Path 3 (accept the negative result, re-scope to Stage 4) remains the
> documented fallback if Stage 2.6 also produces no viable axis.**

**Goal:** find a fitness axis whose optimum *requires evolved structure* —
per STAGE_2_RESULTS.md, `ν_crit` at a=0 is maximized by trivially piling
energy into k=1, so no search method can beat prior sampling on it — then
rerun the Stage 2 acceptance unchanged (the harness is generic over the
axis; the rerun is a config change).

**The extended viability checklist (six properties, all gating).** The five
Stage 1.5 properties — nonzero for some shapes, finite, monotone in the
parameter, resolution-stable, wide band — plus the property Stage 2 proved
necessary:

6. **Non-trivial optimum:** the best of ~20 init-prior random draws sits
   clearly below the best achievable value (hand-built or literature
   shapes), and the top of the landscape is not monotone in a trivially
   controllable quantity (for gCLM: `energy_top_k_frac` / k=1 dominance).
   An axis whose optimum is reachable by prior sampling gives selection
   nothing to do — this check costs ~20 bisections and must run before
   any GA time is spent.

**Candidate axis A (preferred): `ν_crit(t_max, N)` at fixed `a > 0`.**
Sweep the Stage 1.5 IC set *plus* ~20 init-prior random genomes (the same
prior `ga/evolve.py` draws from, so property 6 is measured against the
real prior) at a ∈ {0.4, 0.7, 1.0}, N ∈ {256, 512}, one frozen horizon
t_max=12, v2 oracle unchanged. Rationale: at a=1 (De Gregorio) `sin(x)` is
an *equilibrium* — the k=1 refuge stops being free precisely because
advection opposes it, so viscosity-resistance must come from structure;
intermediate a interpolates. The ν-bisection was the resolution-exact part
of Stage 1.5 (every N=256/512 decision identical), so `ν_crit` at fixed
a>0 has the best chance of passing resolution stability where `a_crit`
failed — but this must be re-verified per a, since the a-axis instability
lived in near-critical advection collapse scales. Known risks: near a=1
smooth data may not blow up within the horizon at any ν ≥ 0 (censored-low
everywhere → dead axis — exactly what the sweep measures before anything
is built); and Stage 1.5's a_crit values cluster at 0.85–1.0, so a=0.4/0.7
keep most shapes alive while a=1.0 probes the interesting edge.
**Selection rule: the largest a that passes all six properties** (largest =
closest to De Gregorio, most scientifically meaningful and most
transferable framing).

**Candidate axis B (fallback): bandwidth-constrained `ν_crit` at a=0.**
Cap the energy fraction in k ≤ 2 (e.g. ≤ 50%) as a genome constraint
enforced at normalization (project down the excess, then renormalize —
unit-test that both the cap and the energy budget hold after every
operator). Re-run the six-property check under the constraint. Risk: the
optimum pins to the arbitrary cap boundary and the landscape inherits its
value; use only if no a passes.

**Then: rerun the Stage 2 acceptance protocol verbatim** — 3 seeds,
budget-matched interleaved baseline, same frozen stop criteria, same
analysis — with the chosen axis, and *also* report the QD-replay
comparison (analyze_stage2.py), which Stage 2 showed catches failure modes
the scalar criterion shares. Passing means what Stage 2's criterion always
meant; failing again with a structured optimum would be a deeper finding
about GA-vs-random on this problem class and goes to review either way.

**Deliverables:** `stage2_5_sweep.py` (reuse stage1_5_sweep.py machinery +
`ga/fitness.py`'s bisection), `STAGE_2_5_RESULTS.md` with the six-property
table per candidate axis, the acceptance rerun logs, a verdict banner
here, and JOURNAL entries per experiment.

---

## Stage 2.6 — Oracle v3 + reformulated fitness quantities (approved review outcome of Stage 2.5)

**Decision record.** Stage 2.5 ended with no viable axis and three
redesign-level paths. On review (2026-07-22) the decision is to run paths
1 and 2 **together as one design iteration**, because they attack the two
independent failure mechanisms Stage 2.5 isolated: (1) soft, fit-decided
boundary semantics at a > 0 (measurement quality), and (2) fitness being a
thin proxy for the νk² dissipation scaling (quantity choice). Path 3 —
accept the negative result and re-scope — is the explicit fallback, taken
only if everything below fails its gate.

**Oracle v3 (path 1) — amplification-only boundary decisions.** The v2
oracle's fit-based blow-up rule (held-out R² floor + T* cap) is what made
every a>0 boundary soft: classification flickered with fit quality across
marginal slow-growth bands (STAGE_2_5_RESULTS.md). v3 removes the fit
from the *bisection decision entirely*: a run counts as blow-up iff it
hits the amplification stop (100×, unchanged) or diverges — the crisp,
physical criterion that decided 100% of a=0 boundaries in Stage 1.5.
Because slow growers need room to amplify, the horizon extends to
**t_max = 24** (2× Stage 2; v2's extrapolated boundary T* at a=0.7 was
17–18, so genuine blow-ups have ≥1.3× headroom to demonstrate
themselves). Early-decay exit unchanged. The tail fit is still computed
and logged (T*, R², α feed Tier 1 candidacy exactly as before) — it just
no longer decides the oracle. This redefines the fitness as
ν_crit(t_max=24, N, amp=100×); v3 values are never comparable to v2
values. The fit-flicker non-monotonicity mechanism is structurally
impossible under v3; the monotonicity probes stay on and now test physics
only.

**Candidate axes, all measured over the same 40-shape roster (20
Stage 1.5 ICs + 20 init-prior draws), N ∈ {256, 512}, gated on all six
properties before any GA time:**

- **A′ — ν_crit under v3 at a ∈ {0.4, 0.7, 1.0}** (path 1 proper): does
  a=0.7's structured top (the 21·tol gap, mixtures-beat-pure-modes
  landscape) survive being measured crisply? a=1.0 is re-checked because
  its "dead axis" verdict was horizon-relative and the horizon doubled.
- **B′ — ν_crit under v3 at a=0** (control + substrate for C): re-baseline
  of the known-crisp axis at the new horizon.
- **C — scaling-normalized resistance at a=0** (path 2): fitness =
  ν_crit(v3, a=0) · k_eff², with k_eff² = Σk²b_k²/Σb_k² the energy-
  weighted mean-square wavenumber. Rationale: Stage 1.5 measured
  ν_crit(sin kx) ∝ 1/k² almost exactly, so the pure-mode subfamily —
  every trivial optimum found so far — is *flat* under C by construction;
  whatever remains measures resistance beyond the dissipation scaling.
  Pure post-processing of B′ (zero extra solver cost). Known risk: the
  mirrored cheat — if ν_crit falls slower than 1/k² in some high-k
  family, C is trivially maximized by high-k concentration; property 6
  gates on monotonicity in k_eff (both directions) as well as k1
  dominance.
- **D — time-to-amplification at fixed handicap ν, a=0** (path 2,
  the Stage 1.5 fallback "blow-up rate" made crisp): fitness =
  t_max − t_amp(ν_fixed), single solver run per evaluation (no
  bisection, ~10× cheaper), amplification-decided by construction.
  Measured at ν_fixed ∈ {0.01, 0.03} (inside Stage 1.5's 0.006–0.053
  band; each gated separately). A shape that never amplifies within
  t_max is censored, not zero-fitness. Rationale: speed under a viscous
  handicap forces a genuine trade-off — sharp gradients accelerate
  blow-up but feed dissipation — so the optimum plausibly requires
  structure. Property adaptations (documented in the analyzer): no
  bisection ⇒ the monotonicity property is replaced by well-definedness
  (amplifies at both resolutions or neither), and the noise floor for
  the gap/band tests is the cross-resolution |Δt_amp| distribution.

**Gate and sequel:** each candidate faces the six-property checklist
(non-trivial optimum measured against the same real init prior). If one
or more pass, choose by precedence **A′ (largest passing a) > C > D**
(most transferable physics first), then rerun the Stage 2 acceptance
protocol verbatim — 3 seeds, budget-matched interleaved baselines,
analyze_stage2.py including QD replay — with config-only changes
(fitness axis, oracle mode, t_max, and for D a no-bisection fitness
path). If nothing passes, path 3 activates: STAGE_2_6_RESULTS.md records
the axis-family negative result as final for the 1D stage, and design
attention moves to Stage 4.

**Deliverables:** oracle-v3 mode in `ga/fitness.py` (config-selected,
v2 remains default for reproducibility of old runs), `stage2_6_sweep.py`,
`analyze_stage2_6.py`, `STAGE_2_6_RESULTS.md`, JOURNAL entries, and — if
a gate passes — the acceptance-rerun logs and verdict here.

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
│   ├── spectral_utils.py       (FFT/Hilbert/dealiasing + conserved-quantity evals)
│   └── gclm.py                 (one gCLM solver, parameterized by (a, ν))
├── test_solver_clm.py          (CLM + diffusion + advection validation)
├── ga/
│   ├── genome.py
│   ├── operators.py
│   ├── evolve.py
│   └── resolution_study.py
└── experiments/
    └── run_logs/
```

## Honest scope caveat

Stages 1–3 use the **gCLM family (CLM through De Gregorio), which are 1D toy
models** — not the real 3D Navier–Stokes equations. As of the latest revision,
viscosity is built into the solver from Stage 1 and Stage 2's fitness function
explicitly searches for blow-up that survives regularization — surviving
viscosity (`ν_crit`) and/or advection (`a_crit`) — which addresses the most
serious version of the earlier gap: we are no longer optimizing purely
inviscid, purely non-advective behavior and hoping it transfers.

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

- **Smooth-genome / limited-regularity mismatch** — arguably the deepest
  *scientific* risk: the established De Gregorio blow-up is for Hölder data,
  and a bandlimited genome is `C^∞`, so the search could be targeting an empty
  set with growing `N` chasing a resolution artifact. Mitigated by the
  evolvable spectral-decay exponent `p` in the genome (representable
  limited-regularity profiles) and by the tunable advection `a` (start where
  smooth blow-up is proven, at `a=0`, and push up). Not fully eliminated —
  this is the real 3D Elgindi caveat in miniature.
- **`ν_crit` degeneracy** — deepest risk to the *`ν_crit` version* of Stage 2:
  if any positive viscosity regularizes these 1D models, `ν_crit ≡ 0` and that
  landscape is flat. Mitigated two ways: Stage 1.5 rules it out with a cheap
  direct sweep *before* the GA is built, and `a_crit` is carried as a
  co-primary fitness precisely because its landscape is known to be non-trivial
  even if the `ν` landscape turns out flat.
- **Scale-covariance cheating** (amplitude) — mitigated by the
  fixed-energy-budget rule above; needs a unit test confirming
  renormalization is actually applied after every genetic operator (and after
  the `k^{-p}` envelope is applied, not before).
- **Frequency-space cheating** (the subtler sibling) — energy piled into
  low-`k`, smooth modes resists both viscosity and advection trivially, so the
  critical-fitness value can be gamed without genuine blow-up structure;
  monitored via `spectral_tail_slope`/`spectral_centroid`, may need a
  bandwidth constraint (see Stage 2 fitness section).
- **Critical-value resolution-dependence** — `a_crit`/`ν_crit` measured at
  fitness resolution can be a numerical artifact; mitigated by fixing/logging
  the fitness resolution, tracking conserved-quantity drift per run, and
  re-checking elites at higher resolution (Stage 1.5 and Stage 2).
- **Advection operator untested by CLM** — CLM (`a=0`) and pure diffusion
  never exercise the `a·u·ω_x` term, which is the whole difficulty; mitigated
  by Stage 1's third acceptance check (transport / invariants / OSW critical-`a`).
- **Numerical blow-up vs. resolution artifact** — this is exactly why Stage
  3 exists; a Tier 1 hit is never reported as more than a candidate.
- **Compute cost at Stage 4** — likely the biggest real bottleneck; sizing
  it accurately isn't possible until Stage 3 tells us how large a genome/
  resolution we actually need for a convincing candidate in 1D.
- **Bisection cost for the critical value** — locating `a_crit`/`ν_crit` per
  genome means multiple solver runs per fitness evaluation (roughly
  `log2(range/tolerance)`), multiplying Stage 2's compute cost. (`a_crit`
  bisection is cheaper per step — inviscid, no viscous stiffness — a further
  reason to prefer it if Stage 1.5 clears it.) Now partially designed
  against, rather than just watched: Stage 2's compute plan (parallel
  evaluation pool, parent-warm-started brackets, early-decay exit, fitness
  cache) attacks it from four sides, and the logged `n_bisection_steps` /
  `n_bracket_expansions` / `early_exit_reason` fields turn tuning it into a
  data question once real runs exist.

## Stopping point for design-only iteration

This plan has now been through several rounds of refinement without a line of
solver code written. Each was worth doing — the viscosity reframe, the
Stage 1.5 fitness-viability de-risk, the MAP-Elites reframe, and now the gCLM
`a`-parameter / `a_crit` fitness, the regularity-envelope genome, and the
advection-validation gate — all change parameterization or acceptance gates
and would have been expensive to retrofit once solver code existed. But
further paper-only iteration has clearly hit diminishing returns. The
remaining open items (bisection cost, exact MAP-Elites cell resolution,
which published Okamoto–Sakajo–Wunsch / De Gregorio results to check against)
are all better resolved by writing **Stage 1, then the Stage 1.5 viability
sweep**, and reacting to real numbers than by further speculation. Stage 1.5 in particular is deliberately cheap and comes *before*
the GA precisely so the biggest design risk (`ν_crit` degeneracy) is settled
empirically, not on paper. Next step is implementation, not another planning
pass — concretely: **Stage 1 → Stage 1.5 → decide fitness → Stage 2.**
