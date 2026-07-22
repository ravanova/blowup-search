# Logging Plan

This is the logging design for the Stage 1–3 pipeline in [PLAN.md](PLAN.md).
`experiments/run_logs/` is already named as a Stage 2 deliverable there but
was never specified — this fills that in, before any solver/GA code exists,
so logging is designed in rather than bolted on later.

## Why this needs its own design, not just `print()`

Two things make ad hoc logging insufficient here:

1. **Every Tier 1/2 claim must be independently reproducible.**
   [WIN_CONDITION.md](WIN_CONDITION.md) exists precisely to stop us from
   fooling ourselves with a numerical artifact. A "candidate" or
   "numerically confirmed" result is only trustworthy if someone can take a
   log entry and regenerate the exact run — same genome, same solver
   parameters, same code — and get the same `T*`. If the log doesn't carry
   enough to do that, the tier classification isn't actually verifiable.
2. **The GA's value isn't just "did it find blow-up," it's "what did we
   learn."** Per PLAN.md Stage 2, the scientific payoff is in *which shapes*
   resist viscosity, not one lucky lineage. That question can only be
   answered by logging genomes and shape data, not just scalar fitness —
   otherwise every run is a black box that either did or didn't work, with
   no way to improve the GA's operators or the search space itself.

## Prerequisite: version control discipline

This directory is a git repository with commits, so `code_version` can point
at real hashes. The remaining discipline is **dirty trees**: a commit hash
only pins the code if the working tree actually matched it when the run
started. `ga/logbook.py` must check `git status` at experiment start and
**refuse to launch on a dirty tree** by default; the explicit override for
throwaway runs records `code_dirty: true` plus a hash of `git diff` in
`config.json` and `index.jsonl`, so a dirty run can never masquerade as a
reproducible one. An experiment silently run against uncommitted changes is
exactly the "reproduce this run, assuming nothing changed since" failure the
`code_version` field exists to prevent.

## Design principles

- **Append-only, structured, one file per experiment.** JSONL (one JSON
  object per line) — greppable, diffable, trivially loaded into `pandas` for
  analysis, no schema migration ceremony while the project is this young.
  Free-text logs are fine for human-readable progress messages but are never
  the source of truth for anything analyzed later.
- **Log genotypes, not just fitness scalars.** A row with only `ν_crit` can
  tell you a run succeeded; it can't tell you *why*. Every genome-evaluation
  entry carries the actual coefficient vector (or a reference to it) so
  shape-vs-fitness analysis is possible after the fact, not just in the
  moment.
- **Distinguish "no blow-up" from "solver failed."** These are not the same
  outcome. Per WIN_CONDITION.md's explicit non-goal, a genome that simply
  doesn't blow up is not a result worth agonizing over. A genome that made
  the solver diverge, hit NaN, or exceed a step budget is a *different*
  category — that's a debugging signal about the solver, and conflating the
  two would hide real bugs inside "the GA just didn't find anything."
- **Log compute cost per evaluation.** PLAN.md already flags bisection cost
  for the critical value (`a_crit`/`ν_crit`) as an open risk
  (`log2(range/tolerance)` solver runs per genome). Without per-run wall-clock
  and step-count logging, that risk stays a guess forever instead of something
  we can actually tune against.
- **Log conserved-quantity drift as a per-run artifact detector.** The gCLM
  family has invariants (energy-type / Hamiltonian quantities; see PLAN.md
  Stage 1). Their numerical drift over a run is a direct, cheap, always-on
  signal that a simulation is under-resolved — available on *every* evaluation,
  long before Stage 3's expensive resolution study runs. Every `solver_run`
  logs the max relative drift of these invariants, so a "blow-up" whose
  invariants drifted can be treated as a likely artifact regardless of how
  clean its `1/M` fit looks. This is a second, independent artifact guard
  alongside the resolution study, one level cheaper. Two traps to design
  around (see PLAN.md Stage 1): the invariant conserved across the whole gCLM
  family, `∫ω dx`, is **identically zero for odd data** — under the odd
  symmetry restriction its drift tells you nothing, and "relative drift"
  divides by ~0 — so drift is normalized by a solution scale (e.g. `‖ω‖₁`),
  never by the invariant's own value, and the chosen invariants must be
  verified non-trivial under the active symmetry class. And for `ν>0` nothing
  is conserved at all: viscous runs track the **energy-balance residual**
  (growth minus dissipation, which should net to zero when resolved), not raw
  conservation.
- **Summary always; raw fields only when it matters.** Full `ω(x,t)` time
  series for every one of thousands of GA evaluations would blow up storage
  before the GA blows up any vorticity. Log summary statistics
  (`t_star`, `r_squared`, `max|ω|` at a handful of checkpoints) for every
  run; keep the full field trajectory only for runs that clear Tier 1, where
  the detail is actually needed for resolution studies and later manual
  review.
- **The baseline is a logged citizen, and the comparison is budget-matched.**
  PLAN.md's Stage 2 acceptance criterion is a *comparison* against random
  search — and that comparison is only honest at **matched evaluation
  budgets**. Comparing the GA's best over `population × generations`
  evaluations against a baseline's best over one population's worth of draws
  manufactures a "clear margin" by order statistics alone (the max of 5,000
  draws beats the max of 100 draws even when both come from the same
  distribution). So the comparison is **best-so-far fitness vs. cumulative
  evaluation count**, GA curve against random-search curve at equal x-values —
  which the logs support for free, since `genome_eval` events are ordered and
  carry `operator`. The baseline gets evaluated and logged exactly like any
  other genome (see schema #3 below), not computed once and quoted from
  memory.
- **Flush every event immediately; checkpoint full population periodically.**
  Bisection makes each fitness evaluation expensive (PLAN.md's own flagged
  risk), so a crash 40 generations into a run losing all progress is a real
  cost, not a hypothetical. Every `append_event()` call flushes to disk
  immediately — never buffered — so a crash leaves a complete log up to the
  last event, and a full-population checkpoint (coefficients for every
  genome, not just the best) is written every K generations so the GA can
  resume from there instead of from scratch. **The checkpoint must include
  the RNG state**, not just the genomes — resuming without it makes the
  resumed run diverge from what a fresh, uninterrupted run would have
  produced, silently breaking reproducibility at exactly the crash the
  checkpoint exists to recover from. For MAP-Elites the archive (best genome
  per cell) is the run's primary scientific output — but **do not snapshot it
  per insertion**: early generations insert a new elite on nearly every
  evaluation, so per-insertion snapshots would thrash. Instead each insertion
  is logged as a cheap `archive_insertion` event (schema #4), making the
  archive at any moment reconstructable by replaying events on top of the
  last full checkpoint, and full snapshots happen only every K generations.
- **Modern RNG, per-evaluation seeds.** Use `np.random.Generator` seeded via
  `np.random.SeedSequence`, not the legacy global `np.random.get_state()`
  API. Each genome evaluation gets its own seed derived deterministically
  from `(random_seed, genome_id)` via `SeedSequence.spawn`-style derivation,
  logged as `eval_seed` in `genome_eval`. This buys two things at once: any
  single evaluation is reproducible *standalone* (which the reproducibility
  audit below requires — no need to replay the whole GA stream to reach it),
  and results stop depending on evaluation *order*, which is a hard
  prerequisite for the parallel evaluation pool PLAN.md Stage 2 calls for.
  Checkpoints store each generator's `bit_generator.state`.
- **One writer process, no matter how many workers.** Fitness evaluations are
  embarrassingly parallel, and PLAN.md Stage 2 runs them in a multiprocessing
  pool (`blas_threads=1` is pinned with exactly this in mind). Flush-per-event
  JSONL appends from multiple processes interleave and corrupt lines, so
  workers never touch `events.jsonl` directly: they send finished events over
  a queue to a single writer process that owns every file under the
  experiment directory. This is specified now, before any code exists,
  because a single-writer design is cheap to build in and miserable to
  retrofit under a corrupted-log incident.

## Log levels and schemas

Nested to match the pipeline: one experiment contains many generations,
each generation evaluates many genomes, each genome evaluation runs the
solver at several `ν` values during bisection.

**Every event carries an integer `schema_version`** (omitted from the field
lists below for brevity, present on every row). `code_version` (a git hash)
already pins the exact code, but resolving a hash to "what shape was this row"
means checking out that commit; a plain integer bumped whenever an event
schema changes lets a `pandas` loader branch on shape directly. The two are
complementary: `schema_version` for cheap shape-dispatch, `code_version` for
full reproducibility.

### 1. Experiment config (`experiments/run_logs/<experiment_id>/config.json`)

Written once at start, frozen for the run's duration:

```
experiment_id, timestamp_start, code_version (git commit hash),
code_dirty (bool; true only via the explicit throwaway-run override, with
        diff_hash alongside — see the version-control prerequisite above),
random_seed (root seed; per-evaluation seeds are derived from it and
        genome_id — see the RNG design principle),
symmetry ("odd" | "general"),
gclm_a (advection coefficient the model is run at; 0 = CLM, 1 = De Gregorio,
        or the fixed a when fitness_axis is "nu_crit"),
fitness_axis ("a_crit" | "nu_crit"; which critical parameter is the fitness,
              chosen per PLAN.md Stage 1.5),
genome_length_N, genome_envelope_p_range (evolvable spectral-decay exponent
        bounds; the k^-p envelope that lets the genome reach limited-regularity
        shapes — see PLAN.md Stage 2), population_size, n_generations,
fitness_resolution_N (solver resolution ALL fitness is measured at),
ga_operators: {selection, crossover, mutation_scale_schedule, elitism_k,
               search_scheme ("map_elites" | "island_ga"),
               map_elites: {descriptors, cells_per_axis,
                            descriptor_bounds (per-descriptor [min, max] the
                              cells discretize — without these, map_cell ids
                              are meaningless across runs),
                            out_of_range_policy ("clip" | "extend")} | null},
energy_budget,
stop_criteria: {t_max (simulation horizon), max_steps,
                omega_amplification_factor (max|ω| growth over its initial
                  value that terminates a run as "blowup_candidate"),
                early_decay_exit (rule for cutting clearly-decaying runs
                  short, e.g. max|ω| below a fraction of initial and
                  monotonically shrinking for a set time window)},
bisection: {axis ("a" | "nu"), range, tolerance,
            predicate_r2_floor (held-out R² a run must clear to count as
              "blows up" inside the bisection — see PLAN.md Stage 2),
            warm_start (parent-bracket policy: margin around the parent's
              critical value, and the fallback to full range)},
n_workers (parallel evaluation pool size),
solver_params: {dealiasing, dt_policy (incl. advective CFL constant),
                conserved_quantities (names tracked for drift; must be
                  non-trivial under `symmetry` — see design principles)},
env: {numpy_version, python_version, blas_threads, fft_backend}
```

`stop_criteria` is not solver bookkeeping — it is part of the *definition of
fitness*. "No blow-up at this `ν`" can only ever mean "no blow-up within
`t_max` at resolution `fitness_resolution_N`", so the measured critical value
is really `ν_crit(t_max, N)` (see PLAN.md Stage 2). Two runs with different
horizons have incomparable fitness for exactly the same reason two runs at
different resolutions do; freezing the horizon here is what makes the
comparison honest.

`fitness_resolution_N` is frozen for the run and pulled into every
`genome_eval` (schema #3): a critical value (`a_crit`/`ν_crit`) is only
comparable to another measured at the same resolution, and it drifts with
resolution because blow-up concentrates energy at high wavenumbers where both
the viscous term `ν·k²` and the sharpest transport gradients live (see PLAN.md
Stage 2). `fitness_axis` records which critical parameter is being optimized so
runs using different fitness definitions are never silently pooled. `env` is
what makes the reproducibility audit real: FFT results shift across NumPy
versions and thread counts, so "re-run this genome, get the same `T*`" needs
more than the git hash — pin `blas_threads=1` for fitness evaluations so runs
are deterministic across machines.

### 2. Generation summary (event type `generation`)

One per GA generation, in `events.jsonl`:

```
experiment_id, generation_index, timestamp,
fitness: {best, mean, std, worst},   (fitness = the a_crit/nu_crit critical value)
best_ever_fitness (running max as of this generation, not just this gen's best),
diversity_metric,
n_new_genomes, n_elite_carried,
best_genome_id
```

`best_ever_fitness` is redundant with data already in `genome_eval` events
but cheap to carry forward at write time — it turns "plot progress over a
run" into reading one field from `generation` events instead of a running
max over every `genome_eval` first.

### 3. Genome evaluation (event type `genome_eval`)

One per fitness evaluation (i.e. one full `ν_crit` bisection for one
genome):

```
experiment_id, generation_index, genome_id, parent_ids (0, 1, or 2),
operator ("init" | "mutation" | "crossover" | "baseline_random"
          | "baseline_literature"),
genome_hash (stable hash of coeffs + envelope p; identity for the fitness
  cache and the reproducibility audit),
eval_seed (this evaluation's derived RNG seed — makes the row re-runnable
  standalone),
cache_hit (bool: fitness served from the cache instead of re-evaluated —
  elitism re-inserts identical genomes every generation, and the solver is
  deterministic, so re-running them is pure waste; a cache-hit row echoes the
  cached values and points at the original via genome_hash),
genome_coeffs (or a path to a stored .npy),
genome_envelope_p (the evolvable k^-p spectral-decay exponent for this genome;
  the regularity axis — small p = rough/Hölder-like, large p = smooth),
energy (post-renormalization AND post-envelope, sanity check vs. energy_budget),
fitness_resolution_N (echoed from config; the resolution the critical value was
  measured at — a critical value is meaningless without it),
fitness_axis ("a_crit" | "nu_crit", echoed from config),
critical_value (the a_crit or nu_crit located by bisection = this genome's
  fitness; defined only relative to config's stop_criteria + resolution),
bracket_censored ("low" | "high" | null: null means the critical value was
  genuinely bracketed; "low" = no blow-up even at the easiest end of the
  range, "high" = still blows up at the hardest end — either way
  critical_value is a range edge, not a measurement, and must be excluded
  from the MAP-Elites archive and any analysis that treats fitness as real),
critical_value_monotone (bool — bisection *assumes* monotonicity and can
  never falsify it from its own samples, so this is measured explicitly:
  after bisection converges, probe 1–2 parameter values beyond the "regular"
  side and confirm they stay regular; any blow-up out there means the
  response is non-monotone and this shape's fitness signal is broken),
initial_bracket (the [lo, hi] bisection actually started from — the parent's
  critical value ± the warm-start margin, or the full config range),
n_bracket_expansions (times the warm-start bracket failed and was widened;
  persistently high values mean the warm-start margin is mistuned),
n_bisection_steps, wall_clock_seconds,
win_tier ("none" | "candidate"),
best_estimate: {t_star, r_squared, slope, exponent} | null,
map_cell (descriptor-space cell id this genome occupies, or null if not
  MAP-Elites),
shape_descriptors: {n_sign_changes, spectral_tail_slope, energy_top_k_frac}
```

`best_estimate.exponent` is the fitted blow-up exponent `α` from
`estimate_blowup_time(..., fit_exponent=True)` (see PLAN.md Stage 2): logging
it lets us tell CLM-generic (`α≈1`) blow-up apart from non-generic De Gregorio
blow-up after the fact, and spot if the gate is being cleared only by
particular exponent families. `best_estimate.r_squared` is the **held-out**
(out-of-sample) `R²` that `win_condition.py` now gates on — the honest number,
not the inflated in-sample max over the exponent grid — so a candidate's logged
`R²` is the same value that actually cleared Tier 1.

`shape_descriptors.spectral_tail_slope` (how fast the coefficient tail decays)
replaces the earlier `spectral_centroid`: it is the smooth-vs-Hölder regularity
axis the physics cares about (and is closely related to the genome's own
`genome_envelope_p`), where `spectral_centroid` was largely redundant with
`energy_top_k_frac`. It doubles as the MAP-Elites descriptor and the guardrail
against frequency-space cheating (PLAN.md Stage 2).

Two baseline operators, both run through the identical `genome_eval` path
and living in the same file (so the Stage 2 acceptance comparison is a
filter on `operator`, not a separate pipeline):
- `baseline_random`: random genomes at the same energy budget, evaluated up
  to the **same total evaluation budget as the GA** (they can be interleaved
  or run after — the comparison is best-so-far vs. cumulative evaluations,
  per the budget-matched design principle above). A population-sized sample
  alone is not a baseline: the GA's best over thousands of draws trivially
  beats the best of a hundred by order statistics, proving nothing.
- `baseline_literature`: a small set of known De Gregorio / gCLM near-blow-up
  profiles from the literature — a positive control. Beating random says the
  GA works at all; reaching or exceeding the literature profiles' critical
  value says it found something worth the compute. Without this, "did it
  work?" only ever gets answered against noise. **These profiles must be
  re-sampled onto the current grid and re-validated at the start of every run,
  not stored as fixed coefficient arrays** — a profile frozen at one `N`,
  symmetry, or resolution silently misrepresents the baseline once those change,
  quietly corrupting the one comparison the acceptance criterion depends on.

`shape_descriptors` are cheap statistics computed once, at write time, from
`genome_coeffs` — not reprocessed later. This is what makes "do independent
runs converge on structurally similar shapes" (see Analysis section) a
query over `events.jsonl` instead of a script that has to reload every raw
coefficient array first.

### 4. Archive insertion (event type `archive_insertion`, MAP-Elites only)

One per archive change — a genome first filling or displacing a cell. Cheap
by design: early generations insert on nearly every evaluation, so this is an
event, not a snapshot (see the checkpoint design principle). The archive at
any point in time is reconstructable by replaying these on top of the last
full checkpoint.

```
experiment_id, generation_index, timestamp, map_cell,
genome_id (the new elite), displaced_genome_id (nullable),
critical_value (the cell's new fitness)
```

### 5. Solver run (event type `solver_run`, optional/summarized)

One per individual `(genome, a, ν)` simulation inside a bisection. Logged as a
compact summary by default; only promoted to carrying the full `max|ω(t)|`
series when the parent `genome_eval` reaches `CANDIDATE` or better:

```
experiment_id, genome_id, a, nu, resolution_N,
outcome ("no_blowup" | "blowup_candidate" | "diverged" | "max_steps_hit"),
early_exit_reason (nullable; "decay_exit" when the early_decay_exit rule in
  config's stop_criteria cut the run short — the expensive runs are the
  no-blow-up ones that would otherwise burn the full t_max, so this is the
  main per-run compute saver and needs to be auditable),
wall_clock_seconds, n_timesteps, dt_min (smallest realized adaptive step —
  with dt_min plus n_timesteps the adaptive-dt trajectory is reproducible to
  tolerance; see PLAN.md's dt policy),
conservation_drift (max drift of the tracked invariants over the run,
  normalized by a solution scale like ‖ω‖₁ — never by the invariant's own
  value, which can be ~0 (e.g. ∫ω dx for odd data); for ν>0 this is the
  energy-balance residual, per the design principle above; a large value
  marks the run under-resolved — an artifact signal independent of the 1/M
  fit),
estimate: {t_star, r_squared, slope, last_time, n_points} | null,
series_path (path to stored raw max|ω(t)| array, only if outcome is
  "blowup_candidate")
```

Both `a` and `nu` are logged on every solver run regardless of which is the
bisection axis: the non-varying one is fixed from config, but recording both
makes each row self-describing and keeps `a_crit`- and `ν_crit`-axis runs
directly comparable. A run flagged as `blowup_candidate` but carrying a large
`conservation_drift` should be distrusted before it is ever fed to Stage 3.

### 6. Resolution study / Tier 2 promotion (event type `resolution_study`)

Triggered per PLAN.md Stage 3 (every N generations, or on a new best
genome):

```
experiment_id, generation_index, genome_id, timestamp,
resolutions_tested (list), t_star_by_resolution,
converged (bool), win_tier ("candidate" | "numerically_confirmed")
```

Any entry with `win_tier: "numerically_confirmed"` is rare and important
enough to also get mirrored into a top-level
`experiments/promoted_candidates.jsonl` — a single flat file across all
experiments, so a Tier 2 hit is never buried in one run's log and easy to
find without scanning every experiment directory.

### 7. Error/anomaly (event type `error`)

Solver exceptions, NaN detection, config validation failures — anything
that isn't a normal "no blow-up" outcome:

```
experiment_id, generation_index, genome_id (nullable),
error_type, message, traceback
```

### 8. Cross-experiment index (`experiments/index.jsonl`)

One line per experiment, appended at start and updated at end. This is the
answer to "did changing X actually help," without opening every experiment's
directory to find out. A crashed process cannot write its own
`status: "crashed"`, so crash marking is a **startup reconciliation**: every
time `logbook.py` starts an experiment, it scans the index for stale
`"running"` rows (no live process, or the newest event in that experiment's
`events.jsonl` older than a staleness threshold) and rewrites them as
`"crashed"` — so the index converges to the truth without relying on dying
processes to be polite.

```
experiment_id, code_version, code_dirty, timestamp_start, timestamp_end,
status ("running" | "completed" | "crashed"),
config_summary: {population_size, N, ga_operators, symmetry, gclm_a,
                 fitness_axis},
best_ever_fitness, best_genome_id,
baseline_fitness_mean, baseline_fitness_max,
n_tier2_promotions
```

`fitness_axis` in `config_summary` is what keeps the cross-run comparison
honest: an `a_crit` run and a `ν_crit` run have numerically incomparable
`best_ever_fitness` values, so any groupby that pools them must key on
`fitness_axis` first.

`config_summary` plus the two outcome fields is what makes hyperparameter
comparison across experiments a `pandas.read_json` one-liner instead of a
manual spreadsheet — e.g. "did the island-model diversity scheme beat plain
fitness sharing" is a groupby on this file, not a re-read of six separate
`config.json`s.

### 9. Solver validation (`experiments/solver_validation.jsonl`)

Separate from GA experiments — this tracks all three of Stage 1's acceptance
checks (CLM vs. analytic blow-up time; pure-diffusion Gaussian decay; **and
the advection check** — transport / gCLM-invariant conservation / an
Okamoto–Sakajo–Wunsch critical-`a` value) over time, tagged by `code_version`,
every time `test_solver_clm.py` runs:

```
code_version, timestamp,
check ("clm_analytic" | "diffusion_decay" | "advection_transport"
       | "invariant_conservation" | "osw_critical_a"),
initial_condition_label, error_metric, passed (bool)
```

The advection checks matter most here: CLM (`a=0`) and pure diffusion never
exercise the `a·u·ω_x` transport operator, so without a dedicated advection
entry a regression in the single hardest part of the solver stays invisible.
Without this whole series, a regression introduced by a later change (e.g.
tweaking dealiasing or the adaptive-`dt`/CFL policy) could silently degrade
accuracy for De Gregorio runs while the original CLM validation, run once and
forgotten, still shows green. This makes solver accuracy a tracked series
across commits, not a one-time gate.

## Storage layout

```
experiments/
├── index.jsonl                      (one line per experiment, for cross-run comparison)
├── promoted_candidates.jsonl        (cross-experiment, Tier 2 hits only)
├── solver_validation.jsonl          (Stage 1 acceptance checks, tracked across commits)
├── JOURNAL.md                       (hand-written notes, one entry per experiment_id)
└── run_logs/
    └── <experiment_id>/
        ├── config.json
        ├── events.jsonl             (generation/genome_eval/archive_insertion/
        │                             solver_run/error events, single writer)
        ├── checkpoints/             (full-population snapshots every K generations)
        ├── series/                  (raw max|ω(t)| arrays, candidates only)
        └── genomes/                 (coefficient vectors for best/candidate genomes)
```

`JOURNAL.md` is the one piece of this system that's manually written, not
generated. The structured logs answer "what happened"; they don't capture
*why* a run was configured the way it was ("tried N=64 because Stage 1's
N=32 runs looked under-resolved near the tail") or what a human noticed
skimming the results that isn't a clean metric. One short entry per
`experiment_id`, cross-referenced against `index.jsonl`, is enough to keep
that reasoning attached to the run instead of living only in someone's
memory of a Slack message or terminal scrollback.

## Deliverables

- `ga/logbook.py` — single `append_event()` writer plus the schemas above,
  implemented as the **one writer process** workers feed over a queue (see
  design principles), including: the dirty-tree guard at experiment start,
  the `experiments/index.jsonl` update-on-start/update-on-end logic with
  stale-`"running"` reconciliation, and periodic checkpoint writes. Slots
  into the `ga/` module list already planned in PLAN.md Stage 2. Not a new
  top-level system — just the thing that makes the existing `experiments/`
  deliverable real.
- A fitness cache keyed on `genome_hash` in `ga/evolve.py` — the solver is
  deterministic, and elitism re-inserts identical genomes every generation,
  so cached fitness makes elites free; cache hits are still logged
  (`cache_hit: true` in schema #3) so evaluation counts stay honest for the
  budget-matched baseline comparison.
- Budget-matched baseline evaluation as a required step in `ga/evolve.py`,
  not an optional analysis add-on — it has to run and log before Stage 2's
  acceptance criterion (best-so-far vs. evaluations, GA against random
  search) can even be checked.
- A small hook in `test_solver_clm.py` (Stage 1) that appends to
  `experiments/solver_validation.jsonl` on each run, tagged with the current
  `code_version`.
- Update PLAN.md's Stage 2 deliverables list to reference this file instead
  of leaving `experiments/` unspecified.
- Analysis scripts are **not** a deliverable yet — see below.

## Analysis this unlocks (the actual point)

This is what "improve our processes and/or genotypes" cashes out to, once
Stage 2 is producing real logs:

- **Process tuning**: fitness-over-generations curves per seed show whether
  the search is still improving or has stagnated; for the MAP-Elites scheme
  (PLAN.md's Stage 2 default) the `diversity_metric` is archive *coverage*
  (fraction of descriptor cells filled) and *QD-score* (sum of the critical
  value over filled cells) — rising coverage means the search is genuinely
  mapping shape space rather than collapsing onto one niche;
  `n_bisection_steps` distribution shows whether the `a`/`ν` search
  range/tolerance is well-tuned or wasting compute; the
  `critical_value_monotone` flag rate is a direct health check on whether the
  fitness signal itself is well-behaved; and the `conservation_drift`
  distribution over candidates flags whether the reported blow-ups are
  resolution-artifacts before any of them reach the resolution study.
- **Genotype insight**: with logged coefficient vectors and envelope exponent
  `p` for every high-fitness genome, we can compute shape descriptors (sign
  changes, spectral-tail slope, energy concentration) and check whether
  independent GA runs (different seeds) converge on structurally similar
  shapes — and in particular whether they converge on a similar *regularity*
  (tail slope / `p`), which is the axis the smooth-vs-Hölder question turns on.
  If they do, that's a real scientific signal about the search space, not an
  artifact of one run's luck — exactly the kind of finding raw fitness numbers
  alone can't surface.
- **Reproducibility audits**: given any logged `genome_id` with
  `win_tier: candidate` or better, re-run it standalone from
  `genome_coeffs` + `config.json` + `code_version` and confirm the same
  `t_star`/tier comes back. This should become a standard check before
  trusting any Tier 1 hit enough to feed it into Stage 3's resolution study.
- **Fast cross-run comparison**: `index.jsonl` alone answers "which of our
  last 10 experiments actually beat baseline, and by how much" without
  touching a single `events.jsonl` — this is the difference between
  treating each GA run as a one-off and actually accumulating process
  knowledge across them.
- **Solver regression tracking**: `solver_validation.jsonl` plotted against
  `code_version` shows whether a later solver change (new dealiasing rule,
  different `dt` policy) quietly degraded accuracy on the Stage 1 checks —
  catching that requires the historical series, not just today's pass/fail.

No dashboard or query tooling is being designed now — `pandas.read_json`
over `events.jsonl` is enough at this scale, and building analysis tooling
before there's a single real log line to analyze would be the same mistake
PLAN.md already called out for solver code: design now, build once there's
something to react to.

## Open risks

- **Schema drift.** As the solver/GA evolve, event schemas will too. The
  mitigation is twofold: the per-event `schema_version` integer lets a loader
  dispatch on shape without git archaeology, and `code_version` ties each row
  to exact code. A schema change bumps `schema_version` and lands in the same
  commit as the code change it reflects, so old logs stay interpretable
  relative to the commit they were written under.
- **Raw series storage growth.** The "summary always, raw only on
  candidates" rule is the guardrail; if Tier 1 hits turn out to be common
  enough that `series/` grows unmanageably, that's itself a useful signal
  (the R² threshold or symmetry restriction may be too permissive) rather
  than purely a storage problem.
