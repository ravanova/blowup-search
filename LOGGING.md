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

## Prerequisite: version control

This directory isn't a git repository yet (`git status` confirms no `.git`).
Every log entry below carries a `code_version` field, which is meaningless
without commits to point at. **Run `git init` and start committing before
Stage 1 lands**, so solver/GA runs can be tagged with a real commit hash —
otherwise "reproduce this run" silently degrades to "reproduce this run,
assuming nothing changed since."

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
  for `ν_crit` as an open risk (`log2(range/tolerance)` solver runs per
  genome). Without per-run wall-clock and step-count logging, that risk stays
  a guess forever instead of something we can actually tune against.
- **Summary always; raw fields only when it matters.** Full `ω(x,t)` time
  series for every one of thousands of GA evaluations would blow up storage
  before the GA blows up any vorticity. Log summary statistics
  (`t_star`, `r_squared`, `max|ω|` at a handful of checkpoints) for every
  run; keep the full field trajectory only for runs that clear Tier 1, where
  the detail is actually needed for resolution studies and later manual
  review.
- **The baseline is a logged citizen, not a side calculation.** PLAN.md's
  own Stage 2 acceptance criterion is a *comparison*: evolved genomes must
  clear "a random-initial-condition-shape baseline by a clear margin." If
  baseline runs aren't logged in the same structured way as evolved genomes,
  that comparison ends up redone ad hoc, differently, each time someone asks
  "did this actually work?" The baseline gets evaluated and logged exactly
  like any other genome (see schema #3 below), not computed once and quoted
  from memory.
- **Flush every event immediately; checkpoint full population periodically.**
  Bisection makes each fitness evaluation expensive (PLAN.md's own flagged
  risk), so a crash 40 generations into a run losing all progress is a real
  cost, not a hypothetical. Every `append_event()` call flushes to disk
  immediately — never buffered — so a crash leaves a complete log up to the
  last event, and a full-population checkpoint (coefficients for every
  genome, not just the best) is written every K generations so the GA can
  resume from there instead of from scratch. **The checkpoint must include
  the numpy RNG state** (`np.random.get_state()`), not just the genomes —
  resuming without it makes the resumed run diverge from what a fresh,
  uninterrupted run would have produced, silently breaking reproducibility at
  exactly the crash the checkpoint exists to recover from. For MAP-Elites the
  checkpoint is the archive itself (best genome per cell), which is also the
  run's primary scientific output, so checkpoint on every new-elite insertion
  as well as every K generations.

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
random_seed, model ("clm" | "de_gregorio"), symmetry ("odd" | "general"),
genome_length_N, population_size, n_generations,
fitness_resolution_N (solver resolution ALL fitness ν_crit is measured at),
ga_operators: {selection, crossover, mutation_scale_schedule, elitism_k,
               search_scheme ("map_elites" | "island_ga"),
               map_elites: {descriptors, cells_per_axis} | null},
energy_budget, nu_bisection: {range, tolerance},
solver_params: {dealiasing, dt_policy},
env: {numpy_version, python_version, blas_threads, fft_backend}
```

`fitness_resolution_N` is frozen for the run and pulled into every
`genome_eval` (schema #3): a `ν_crit` is only comparable to another measured
at the same resolution, and `ν_crit` drifts with resolution because blow-up
concentrates energy where the viscous term `ν·k²` dominates (see PLAN.md
Stage 2). `env` is what makes the reproducibility audit real: FFT results
shift across NumPy versions and thread counts, so "re-run this genome, get the
same `T*`" needs more than the git hash — pin `blas_threads=1` for fitness
evaluations so runs are deterministic across machines.

### 2. Generation summary (event type `generation`)

One per GA generation, in `events.jsonl`:

```
experiment_id, generation_index, timestamp,
fitness: {best, mean, std, worst},
best_ever_nu_crit (running max as of this generation, not just this gen's best),
diversity_metric,
n_new_genomes, n_elite_carried,
best_genome_id
```

`best_ever_nu_crit` is redundant with data already in `genome_eval` events
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
genome_coeffs (or a path to a stored .npy),
energy (post-renormalization, sanity check against energy_budget),
fitness_resolution_N (echoed from config; the resolution ν_crit was measured
  at — a ν_crit is meaningless without it),
nu_crit, nu_crit_monotone (bool: was the blow-up/no-blowup response monotone
  in ν during bisection? a false flags a broken fitness signal for this shape),
n_bisection_steps, wall_clock_seconds,
win_tier ("none" | "candidate"),
best_estimate: {t_star, r_squared, slope, exponent} | null,
map_cell (descriptor-space cell id this genome occupies, or null if not
  MAP-Elites),
shape_descriptors: {n_sign_changes, spectral_centroid, energy_top_k_frac}
```

`best_estimate.exponent` is the fitted blow-up exponent `α` from
`estimate_blowup_time(..., fit_exponent=True)` (see PLAN.md Stage 2): logging
it lets us tell CLM-generic (`α≈1`) blow-up apart from non-generic De Gregorio
blow-up after the fact, and spot if the R²-gate is being cleared only by
particular exponent families.

Two baseline operators, both run through the identical `genome_eval` path at
experiment start and living in the same file (so the Stage 2 acceptance
comparison is a filter on `operator`, not a separate pipeline):
- `baseline_random`: the same number of random genomes at the same energy
  budget as the real population — shows whether the GA beats noise.
- `baseline_literature`: a small set of known De Gregorio near-blow-up
  profiles from the literature — a positive control. Beating random says the
  GA works at all; reaching or exceeding the literature profiles' `ν_crit`
  says it found something worth the compute. Without this, "did it work?" only
  ever gets answered against noise.

`shape_descriptors` are cheap statistics computed once, at write time, from
`genome_coeffs` — not reprocessed later. This is what makes "do independent
runs converge on structurally similar shapes" (see Analysis section) a
query over `events.jsonl` instead of a script that has to reload every raw
coefficient array first.

### 4. Solver run (event type `solver_run`, optional/summarized)

One per individual `(genome, ν)` simulation inside a bisection. Logged as a
compact summary by default; only promoted to carrying the full `max|ω(t)|`
series when the parent `genome_eval` reaches `CANDIDATE` or better:

```
experiment_id, genome_id, nu, resolution_N,
outcome ("no_blowup" | "blowup_candidate" | "diverged" | "max_steps_hit"),
wall_clock_seconds, n_timesteps,
estimate: {t_star, r_squared, slope, last_time, n_points} | null,
series_path (path to stored raw max|ω(t)| array, only if outcome is
  "blowup_candidate")
```

### 5. Resolution study / Tier 2 promotion (event type `resolution_study`)

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

### 6. Error/anomaly (event type `error`)

Solver exceptions, NaN detection, config validation failures — anything
that isn't a normal "no blow-up" outcome:

```
experiment_id, generation_index, genome_id (nullable),
error_type, message, traceback
```

### 7. Cross-experiment index (`experiments/index.jsonl`)

One line per experiment, appended at start and updated at end (or on
crash). This is the answer to "did changing X actually help," without
opening every experiment's directory to find out:

```
experiment_id, code_version, timestamp_start, timestamp_end, status
  ("running" | "completed" | "crashed"),
config_summary: {population_size, N, ga_operators, symmetry, model},
best_ever_nu_crit, best_genome_id,
baseline_nu_crit_mean, baseline_nu_crit_max,
n_tier2_promotions
```

`config_summary` plus the two outcome fields is what makes hyperparameter
comparison across experiments a `pandas.read_json` one-liner instead of a
manual spreadsheet — e.g. "did the island-model diversity scheme beat plain
fitness sharing" is a groupby on this file, not a re-read of six separate
`config.json`s.

### 8. Solver validation (`experiments/solver_validation.jsonl`)

Separate from GA experiments — this tracks Stage 1's own acceptance
criteria (CLM vs. analytic blow-up time, pure-diffusion Gaussian decay)
over time, tagged by `code_version`, every time
`test_solver_clm.py` runs:

```
code_version, timestamp, check ("clm_analytic" | "diffusion_decay"),
initial_condition_label, error_metric, passed (bool)
```

Without this, a solver regression introduced by a later change (e.g.
tweaking dealiasing or the adaptive-`dt` policy) could silently degrade
accuracy for De Gregorio runs while the original CLM validation, run once
and forgotten, still shows green. This makes solver accuracy a tracked
series across commits, not a one-time gate.

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
        ├── events.jsonl             (generation/genome_eval/error events)
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
  including the `experiments/index.jsonl` update-on-start/update-on-end
  logic and periodic checkpoint writes; slots into the `ga/` module list
  already planned in PLAN.md Stage 2. Not a new top-level system — just the
  thing that makes the existing `experiments/` deliverable real.
- Baseline evaluation as a required step in `ga/evolve.py`'s experiment
  startup, not an optional analysis add-on — it has to run and log before
  Stage 2's acceptance criterion can even be checked.
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
  (fraction of descriptor cells filled) and *QD-score* (sum of `ν_crit` over
  filled cells) — rising coverage means the search is genuinely mapping shape
  space rather than collapsing onto one niche; `n_bisection_steps`
  distribution shows whether the `ν` search range/tolerance is well-tuned or
  wasting compute; the `nu_crit_monotone` flag rate is a direct health check
  on whether the fitness signal itself is well-behaved.
- **Genotype insight**: with logged coefficient vectors for every
  high-`ν_crit` genome, we can compute shape descriptors (sign changes,
  spectral centroid, energy concentration) and check whether independent GA
  runs (different seeds) converge on structurally similar shapes. If they
  do, that's a real scientific signal about the search space, not an
  artifact of one run's luck — exactly the kind of finding raw fitness
  numbers alone can't surface.
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
