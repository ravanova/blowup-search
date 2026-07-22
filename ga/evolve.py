"""Stage 2 GA harness: MAP-Elites over gCLM initial conditions, fitness =
nu_crit(t_max, N) at a=0 (the axis Stage 1.5 selected; see
STAGE_1_5_RESULTS.md).

Search scheme (PLAN.md Stage 2): MAP-Elites keyed on
(spectral_tail_slope, n_sign_changes) — one elite genome per shape-descriptor
cell, tournament parents drawn from the archive, blend crossover + Gaussian
mutation (both energy-renormalized), no separate elitism (the archive IS the
elite store, and the genome_hash fitness cache makes re-evaluating an elite
free anyway; elitism_k: 0 in config records this). Censored bracket-edge
fitness never enters the archive; neither does a genome whose monotonicity
probe failed (its fitness signal is broken by definition).

Baselines (mandatory, budget-matched — LOGGING.md design principle):
- baseline_random: after every generation's GA evaluations, the same number
  of random draws from the init distribution is evaluated and logged through
  the identical path, so at every cumulative-evaluation count the GA and the
  baseline have spent the same budget. Cache hits count as evaluations on
  the GA side (they are logged evaluations; the baseline never repeats a
  genome, so this is conservative in the baseline's favor on solver time).
- baseline_literature: Stage 1.5's structured profiles re-sampled onto the
  current genome length at run start (never stored as fixed arrays), logged
  once with generation_index null — a positive control, outside the
  GA-vs-random budget comparison.

Compute plan (PLAN.md): multiprocessing pool (workers get the EventSink,
never touch files), warm-started brackets from the parent's critical value,
early-decay exit inside the solver, fitness cache on genome_hash.

Usage:
    .venv/bin/python -m ga.evolve --seed 1                  # full run
    .venv/bin/python -m ga.evolve --seed 1 --smoke          # tiny shakedown
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")  # pin BLAS for process parallelism

import argparse
import multiprocessing
import sys
import time

import numpy as np

from ga.fitness import evaluate_genome
from ga.genome import (
    ENERGY_BUDGET,
    Genome,
    from_sine_pairs,
    project_to_sines,
    random_genome,
)
from ga.logbook import ExperimentWriter, genome_hash
from ga.operators import blend_crossover, mutate, mutation_scale, tournament_select

# Stage 2.6 acceptance config (PLAN.md Stage 2.6): fitness axis A' —
# nu_crit under the v3 amplification-only oracle at a=0.7, the only
# candidate passing all six viability properties (STAGE_2_6_RESULTS.md).
# Changes from the Stage 2 config are config-only: gclm_a 0->0.7,
# t_max 12->24 (max_steps doubled with it), bisection range [0,0.1]->[0,0.3]
# (measured v3 band at a=0.7 is 0.006-0.158), blowup_predicate v2->v3.
DEFAULT_CONFIG = {
    "symmetry": "odd",
    "gclm_a": 0.7,
    "fitness_axis": "nu_crit",
    "genome_length_N": 32,
    "genome_envelope_p_range": [0.0, 3.5],
    "population_size": 24,
    "n_generations": 25,
    "fitness_resolution_N": 256,  # Stage 1.5: exact vs N=512 on every nu bisection
    "energy_budget": ENERGY_BUDGET,
    # Stage 2.5 candidate B: cap on the energy fraction in modes k <= k_max,
    # enforced at normalization after every operator (None = no constraint).
    "bandwidth_cap": None,
    "tier1_r2_threshold": 0.98,
    "checkpoint_every_k": 5,
    "ga_operators": {
        "selection": "tournament",
        "tournament_k": 3,
        "crossover": "blend_arithmetic",
        "crossover_rate": 0.5,
        "mutation_scale_schedule": {"initial": 0.3, "decay": 0.92},
        "p_mutation_scale": 0.25,
        "elitism_k": 0,  # MAP-Elites archive is the elite store
        "search_scheme": "map_elites",
        "map_elites": {
            "descriptors": ["spectral_tail_slope", "n_sign_changes"],
            "cells_per_axis": [12, 8],
            "descriptor_bounds": {
                "spectral_tail_slope": [-5.0, 1.0],
                "n_sign_changes": [2, 34],
            },
            "out_of_range_policy": "clip",
        },
    },
    # Frozen stop criteria from STAGE_1_5_RESULTS.md — part of the fitness
    # definition (nu_crit is horizon-relative), never per-run tunables.
    "stop_criteria": {
        "t_max": 24.0,
        "max_steps": 400_000,
        "omega_amplification_factor": 100.0,
        "early_decay_exit": {"fraction": 0.1, "window": 2.0},
    },
    "bisection": {
        "axis": "nu",
        "range": [0.0, 0.3],  # measured Stage 2.6 v3 band at a=0.7: 0.006-0.158
        "tolerance": 1e-3,
        "tail_fraction": 0.15,
        "predicate_r2_floor": 0.9,   # still gates Tier 1 candidacy
        "t_star_cap_factor": 1.5,    # idem; neither decides the v3 oracle
        "blowup_predicate": "v3_amplification_only",
        "warm_start": {"margin": 0.01, "fallback": "full_range"},
        "probe_fractions": [0.05, 0.15],
        "max_iters": 30,
    },
    "solver_params": {
        "dealiasing": "2/3",
        "dt_policy": {"dt_max": 1e-2, "c1": 0.05, "c2": 0.4},
        "conserved_quantities": ["mean_omega_drift_over_l1",
                                 "energy_balance_residual"],
    },
}


# --- MAP-Elites archive ----------------------------------------------------


class Archive:
    """Best genome per descriptor cell. Insertion requires an uncensored,
    monotone-clean fitness (censored values are range edges, not
    measurements — LOGGING.md schema #3)."""

    def __init__(self, map_cfg):
        self.descriptors = map_cfg["descriptors"]
        self.cells_per_axis = map_cfg["cells_per_axis"]
        self.bounds = [map_cfg["descriptor_bounds"][d] for d in self.descriptors]
        self.cells = {}  # cell id "i,j" -> entry dict

    def cell_of(self, shape_descriptors):
        idx = []
        for d, (lo, hi), n_cells in zip(self.descriptors, self.bounds,
                                        self.cells_per_axis):
            frac = (float(shape_descriptors[d]) - lo) / (hi - lo)
            idx.append(int(np.clip(int(frac * n_cells), 0, n_cells - 1)))
        return ",".join(str(i) for i in idx)

    def maybe_insert(self, payload, genome):
        """Returns (inserted, cell, displaced_genome_id)."""
        cell = self.cell_of(payload["shape_descriptors"])
        if payload["bracket_censored"] is not None:
            return False, cell, None
        if payload["critical_value_monotone"] is False:
            return False, cell, None
        incumbent = self.cells.get(cell)
        if incumbent is not None and incumbent["fitness"] >= payload["critical_value"]:
            return False, cell, None
        self.cells[cell] = {
            "genome_id": payload["genome_id"],
            "fitness": payload["critical_value"],
            "coeffs": [float(c) for c in genome.coeffs],
            "envelope_p": float(genome.envelope_p),
            "descriptors": payload["shape_descriptors"],
        }
        return True, cell, incumbent["genome_id"] if incumbent else None

    @property
    def entries(self):
        return list(self.cells.values())

    def coverage(self):
        return len(self.cells) / int(np.prod(self.cells_per_axis))

    def qd_score(self):
        return float(sum(e["fitness"] for e in self.cells.values()))

    def snapshot(self):
        return dict(self.cells)


# --- literature baseline (re-sampled at run start, per LOGGING.md) ---------


def literature_genomes(n_genome, energy_budget, bandwidth_cap=None):
    """Stage 1.5's structured profiles as genomes on the CURRENT genome
    length — recomputed here every run start, never stored as arrays.
    Under a bandwidth cap, profiles with no energy above the capped band
    (e.g. pure sin(x)) are infeasible by construction and skipped."""
    sine_sets = [
        ("sin(x)", [(1, 1.0)]),
        ("sin(2x)", [(2, 1.0)]),
        ("sin(x)+0.5sin(2x)", [(1, 1.0), (2, 0.5)]),
        ("sin(x)-0.5sin(2x)", [(1, 1.0), (2, -0.5)]),
        ("sin(x)+0.3sin(3x)", [(1, 1.0), (3, 0.3)]),
        ("sin(x)+0.5sin(4x)", [(1, 1.0), (4, 0.5)]),
    ]
    for p in (1.0, 1.5, 2.0):
        sine_sets.append((f"tail(p={p:g})",
                          [(k, k ** (-p)) for k in range(1, 21)]))
    sine_sets.append(("tail(p=1.5,alt)",
                      [(k, ((-1.0) ** (k + 1)) * k ** (-1.5))
                       for k in range(1, 21)]))
    out = []
    for label, pairs in sine_sets:
        try:
            out.append((label, from_sine_pairs(pairs, n_genome, energy_budget,
                                               bandwidth_cap)))
        except ValueError:
            print(f"[lit] skipping {label}: infeasible under bandwidth cap",
                  flush=True)
    for kappa in (2.0, 5.0):
        out.append((f"bump(kappa={kappa:g})", project_to_sines(
            lambda x, k=kappa: np.sin(x) * np.exp(k * (np.cos(x) - 1.0)),
            n_genome, energy_budget, bandwidth_cap)))
    return out


# --- the evolutionary loop -------------------------------------------------


class Evolver:
    def __init__(self, config, writer, pool):
        self.cfg = config
        self.writer = writer
        self.pool = pool
        self.archive = Archive(config["ga_operators"]["map_elites"])
        self.cache = {}  # genome_hash -> logged genome_eval payload
        self.n_evals_ga = 0
        self.n_evals_baseline = 0
        self.n_cache_hits = 0
        self.best_ever = None  # (fitness, genome_id)
        self.baseline_fitnesses = []  # uncensored baseline_random only
        self._id_counter = 0

    def next_id(self, prefix):
        self._id_counter += 1
        return f"{prefix}{self._id_counter:05d}"

    # -- one logged batch of evaluations (cache-aware) --

    def evaluate_and_log(self, batch, generation_index, is_baseline=False):
        """batch: list of dicts {genome, genome_id, operator, parent_ids,
        warm_center, label?}. Cache hits are logged without re-running
        (evaluation counts stay honest — LOGGING.md); misses go through the
        worker pool. Returns the logged payload rows in submission order."""
        tasks, cached_rows = [], []
        for entry in batch:
            genome = entry["genome"]
            h = genome_hash(genome.coeffs, genome.envelope_p)
            if h in self.cache and not is_baseline:
                row = dict(self.cache[h])
                row.pop("candidate_series", None)
                row.pop("label", None)
                row.update(
                    generation_index=generation_index,
                    genome_id=entry["genome_id"],
                    operator=entry["operator"],
                    parent_ids=entry["parent_ids"], cache_hit=True,
                    n_solver_runs=0, n_bisection_steps=0,
                    wall_clock_seconds=0.0,
                )
                cached_rows.append((row, genome))
            else:
                task = {
                    "coeffs": np.asarray(genome.coeffs),
                    "envelope_p": genome.envelope_p,
                    "genome_id": entry["genome_id"],
                    "operator": entry["operator"],
                    "parent_ids": entry["parent_ids"],
                    "warm_center": entry["warm_center"],
                    "generation_index": generation_index,
                    "config": self.cfg,
                    "sink": self.writer.sink,
                }
                if "label" in entry:
                    task["label"] = entry["label"]
                tasks.append(task)

        if self.pool is None:
            results = [evaluate_genome(t) for t in tasks]
        else:
            results = self.pool.map(evaluate_genome, tasks, chunksize=1)

        genome_by_id = {e["genome_id"]: e["genome"] for e in batch}
        rows = [(row, genome_by_id[row["genome_id"]]) for row in results]
        for row, _ in rows:
            self.cache[row["genome_hash"]] = row
        rows.extend(cached_rows)
        order = {e["genome_id"]: i for i, e in enumerate(batch)}
        rows.sort(key=lambda rg: order[rg[0]["genome_id"]])

        for row, genome in rows:
            row["map_cell"] = self.archive.cell_of(row["shape_descriptors"])
            self.writer.append_event("genome_eval", row)
            if row["cache_hit"]:
                self.n_cache_hits += 1
            if is_baseline:
                self.n_evals_baseline += 1
                if (row["operator"] == "baseline_random"
                        and row["bracket_censored"] is None):
                    self.baseline_fitnesses.append(row["critical_value"])
            else:
                self.n_evals_ga += 1
                if row["bracket_censored"] is None and (
                        self.best_ever is None
                        or row["critical_value"] > self.best_ever[0]):
                    self.best_ever = (row["critical_value"], row["genome_id"])
                if not row["cache_hit"]:
                    inserted, cell, displaced = self.archive.maybe_insert(row, genome)
                    if inserted:
                        self.writer.append_event("archive_insertion", {
                            "generation_index": generation_index,
                            "map_cell": cell,
                            "genome_id": row["genome_id"],
                            "displaced_genome_id": displaced,
                            "critical_value": row["critical_value"],
                        })
        return [r for r, _ in rows]

    # -- offspring production --

    def random_entry(self, rng, operator="init"):
        return {
            "genome": random_genome(rng, self.cfg["genome_length_N"],
                                    self.cfg["genome_envelope_p_range"],
                                    self.cfg["energy_budget"],
                                    self.cfg.get("bandwidth_cap")),
            "genome_id": self.next_id("rb" if operator == "baseline_random"
                                      else "g"),
            "operator": operator, "parent_ids": [], "warm_center": None,
        }

    def make_children(self, rng, generation_index):
        ops = self.cfg["ga_operators"]
        scale = mutation_scale(ops["mutation_scale_schedule"], generation_index)
        p_range = self.cfg["genome_envelope_p_range"]
        cap = self.cfg.get("bandwidth_cap")
        children = []
        for _ in range(self.cfg["population_size"]):
            entries = self.archive.entries
            if not entries:
                # Nothing uncensored in the archive yet: keep drawing from
                # the init prior rather than crashing on an empty archive.
                children.append(self.random_entry(rng))
                continue
            pa = tournament_select(entries, rng, ops["tournament_k"])
            if len(entries) >= 2 and rng.uniform() < ops["crossover_rate"]:
                pb = tournament_select(entries, rng, ops["tournament_k"])
                child = blend_crossover(
                    Genome(np.array(pa["coeffs"]), pa["envelope_p"]),
                    Genome(np.array(pb["coeffs"]), pb["envelope_p"]),
                    rng, self.cfg["energy_budget"], cap)
                child = mutate(child, rng, scale, ops["p_mutation_scale"],
                               p_range, self.cfg["energy_budget"], cap)
                fitter = pa if pa["fitness"] >= pb["fitness"] else pb
                children.append({
                    "genome": child, "genome_id": self.next_id("g"),
                    "operator": "crossover",
                    "parent_ids": [pa["genome_id"], pb["genome_id"]],
                    "warm_center": fitter["fitness"],
                })
            else:
                child = mutate(Genome(np.array(pa["coeffs"]), pa["envelope_p"]),
                               rng, scale, ops["p_mutation_scale"],
                               p_range, self.cfg["energy_budget"], cap)
                children.append({
                    "genome": child, "genome_id": self.next_id("g"),
                    "operator": "mutation", "parent_ids": [pa["genome_id"]],
                    "warm_center": pa["fitness"],
                })
        return children


def run(config, writer, seed, n_workers):
    root = np.random.SeedSequence(seed)
    ga_ss, baseline_ss = root.spawn(2)
    ga_rng = np.random.default_rng(ga_ss)
    baseline_rng = np.random.default_rng(baseline_ss)

    pool = (multiprocessing.get_context().Pool(n_workers)
            if n_workers > 0 else None)
    ev = Evolver(config, writer, pool)
    t_run0 = time.perf_counter()
    try:
        # Positive control: literature profiles on the current grid, once.
        lit_batch = [{"genome": g, "genome_id": ev.next_id("lit"),
                      "operator": "baseline_literature", "parent_ids": [],
                      "warm_center": None, "label": label}
                     for label, g in literature_genomes(
                         config["genome_length_N"], config["energy_budget"],
                         config.get("bandwidth_cap"))]
        lit_rows = ev.evaluate_and_log(lit_batch, generation_index=None,
                                       is_baseline=True)
        lit_best = max((r["critical_value"] for r in lit_rows
                        if r["bracket_censored"] is None), default=None)
        print(f"[lit] {len(lit_rows)} literature profiles, best uncensored "
              f"nu_crit = {lit_best}", flush=True)

        for gen in range(config["n_generations"]):
            t0 = time.perf_counter()
            if gen == 0:
                batch = [ev.random_entry(ga_rng)
                         for _ in range(config["population_size"])]
            else:
                batch = ev.make_children(ga_rng, gen)
            ga_rows = ev.evaluate_and_log(batch, gen)

            # Budget-matched interleaved baseline: the same number of logged
            # evaluations as the GA, at every generation.
            base_batch = [ev.random_entry(baseline_rng, "baseline_random")
                          for _ in range(len(ga_rows))]
            ev.evaluate_and_log(base_batch, gen, is_baseline=True)

            fits = [r["critical_value"] for r in ga_rows
                    if r["bracket_censored"] is None]
            writer.append_event("generation", {
                "generation_index": gen,
                "fitness": {
                    "best": max(fits) if fits else None,
                    "mean": float(np.mean(fits)) if fits else None,
                    "std": float(np.std(fits)) if fits else None,
                    "worst": min(fits) if fits else None,
                },
                "best_ever_fitness": ev.best_ever[0] if ev.best_ever else None,
                "best_genome_id": ev.best_ever[1] if ev.best_ever else None,
                "n_censored": sum(1 for r in ga_rows
                                  if r["bracket_censored"] is not None),
                "diversity_metric": {
                    "archive_coverage": ev.archive.coverage(),
                    "qd_score": ev.archive.qd_score(),
                    "n_cells_filled": len(ev.archive.cells),
                },
                "n_new_genomes": len(ga_rows),
                "n_elite_carried": 0,
                "n_cache_hits_so_far": ev.n_cache_hits,
                "cumulative_evals_ga": ev.n_evals_ga,
                "cumulative_evals_baseline": ev.n_evals_baseline,
                "wall_clock_seconds": time.perf_counter() - t0,
            })
            if (gen + 1) % config["checkpoint_every_k"] == 0 or \
                    gen == config["n_generations"] - 1:
                writer.write_checkpoint(
                    gen,
                    [{"genome_id": e["genome_id"],
                      "coeffs": [float(c) for c in e["genome"].coeffs],
                      "envelope_p": float(e["genome"].envelope_p),
                      "operator": e["operator"]} for e in batch],
                    {"ga": ga_rng.bit_generator.state,
                     "baseline": baseline_rng.bit_generator.state},
                    archive=ev.archive.snapshot(),
                )
            best = ev.best_ever[0] if ev.best_ever else None
            print(f"[gen {gen:3d}] best_ever={best} "
                  f"coverage={ev.archive.coverage():.3f} "
                  f"qd={ev.archive.qd_score():.4f} "
                  f"cache_hits={ev.n_cache_hits} "
                  f"({time.perf_counter() - t0:.1f}s)", flush=True)

        writer.finish(
            status="completed",
            best_ever_fitness=ev.best_ever[0] if ev.best_ever else None,
            best_genome_id=ev.best_ever[1] if ev.best_ever else None,
            baseline_fitness_mean=(float(np.mean(ev.baseline_fitnesses))
                                   if ev.baseline_fitnesses else None),
            baseline_fitness_max=(max(ev.baseline_fitnesses)
                                  if ev.baseline_fitnesses else None),
            n_tier2_promotions=0,
        )
        print(f"run complete in {time.perf_counter() - t_run0:.0f}s: "
              f"{ev.n_evals_ga} GA evals, {ev.n_evals_baseline} baseline evals",
              flush=True)
    except BaseException:
        writer.finish(status="crashed")
        raise
    finally:
        if pool is not None:
            pool.close()
            pool.join()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--population", type=int)
    ap.add_argument("--generations", type=int)
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--smoke", action="store_true",
                    help="tiny end-to-end shakedown (small pop/gens)")
    ap.add_argument("--allow-dirty", action="store_true")
    ap.add_argument("--experiment-id")
    args = ap.parse_args(argv)

    config = _json_roundtrip(DEFAULT_CONFIG)
    config["random_seed"] = args.seed
    if args.smoke:
        config["population_size"] = 6
        config["n_generations"] = 3
    if args.population:
        config["population_size"] = args.population
    if args.generations:
        config["n_generations"] = args.generations
    config["n_workers"] = args.workers

    writer = ExperimentWriter(config, allow_dirty=args.allow_dirty,
                              experiment_id=args.experiment_id)
    print(f"experiment_id = {writer.experiment_id}", flush=True)
    run(config, writer, args.seed, args.workers)


def _json_roundtrip(obj):
    """Deep-copy via JSON so the frozen config written to config.json and the
    dict handed to workers are byte-identical in content."""
    import json
    return json.loads(json.dumps(obj))


if __name__ == "__main__":
    sys.exit(main())
