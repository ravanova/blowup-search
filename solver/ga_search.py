"""A small, problem-agnostic real-coded genetic algorithm (global search).

Deliberately generic: it knows nothing about gCLM, profiles, or residuals -- it
minimizes an arbitrary `fitness(genome) -> float` over a bounded box. This keeps
the SEARCH separated from the PROBLEM (solver/gclm_family.py), so the same engine
serves both the gCLM two-scale transition map now and, later, the Route-D
"guess" stage (find an approximate steady profile a rigorous interval-Newton
step then certifies).

Why a GA and not the local relaxation we already have: the self-similar profile
is a fixed point of a rescaled flow, and the family can have MULTIPLE fixed
points (different blowup mechanisms). Dynamic-rescaling relaxation slides into
whichever attractor you seed near -- it is blind to the others. A global search
over (shape params + exponents) can map the whole fixed-point set and catch
where it bifurcates, which is exactly the two-scale-vs-two-stage question. The
GA only earns its keep if it finds what relaxation cannot; the a=0 known-answer
gate (must recover the exact CLM profile) is the guard against it flailing.

No scipy: everything is numpy + the stdlib RNG via numpy Generator. Real-coded
with tournament selection, blend (BLX-alpha) crossover, Gaussian mutation, and
elitism -- the standard, well-understood operators; nothing exotic.
"""

from dataclasses import dataclass, field

import numpy as np


@dataclass
class GAConfig:
    pop_size: int = 60
    n_generations: int = 120
    elite_frac: float = 0.1          # top fraction copied unchanged each gen
    tournament_k: int = 3            # selection pressure
    crossover_alpha: float = 0.5     # BLX-alpha spread
    mutation_prob: float = 0.3       # per-gene probability of a Gaussian kick
    mutation_frac: float = 0.15      # kick sigma as a fraction of each gene's box width
    mutation_decay: float = 0.995    # sigma *= decay each generation (anneal)
    seed: int = 0
    # optional: stop early once best fitness <= this (e.g. residual floor reached)
    target_fitness: float = -np.inf


@dataclass
class GAResult:
    best_genome: np.ndarray
    best_fitness: float
    history: list = field(default_factory=list)   # best fitness per generation
    mean_history: list = field(default_factory=list)
    generations: int = 0


def ga_minimize(fitness, lower, upper, config=None):
    """Minimize `fitness(genome)->float` over the box [lower, upper].

    fitness       : callable, genome (1-D np.ndarray) -> scalar to MINIMIZE.
                    May return np.inf / np.nan for invalid genomes (handled).
    lower, upper  : array-like box bounds, same length = genome dimension.
    Returns a GAResult. Deterministic given config.seed.
    """
    cfg = config or GAConfig()
    lower = np.asarray(lower, dtype=float)
    upper = np.asarray(upper, dtype=float)
    dim = lower.size
    width = upper - lower
    rng = np.random.default_rng(cfg.seed)

    def evaluate(pop):
        vals = np.array([fitness(ind) for ind in pop], dtype=float)
        vals[~np.isfinite(vals)] = np.inf   # invalid -> worst
        return vals

    # initial population: uniform over the box
    pop = lower + rng.random((cfg.pop_size, dim)) * width
    vals = evaluate(pop)

    n_elite = max(1, int(round(cfg.elite_frac * cfg.pop_size)))
    sigma = cfg.mutation_frac * width      # per-gene mutation scale
    history, mean_history = [], []

    best_i = int(np.argmin(vals))
    best_genome = pop[best_i].copy()
    best_fitness = float(vals[best_i])

    for gen in range(cfg.n_generations):
        # --- record ---
        history.append(best_fitness)
        finite = vals[np.isfinite(vals)]
        mean_history.append(float(finite.mean()) if finite.size else np.inf)
        if best_fitness <= cfg.target_fitness:
            break

        # --- elitism: carry the best n_elite unchanged ---
        order = np.argsort(vals)
        new_pop = [pop[order[i]].copy() for i in range(n_elite)]

        # --- fill the rest by tournament -> crossover -> mutation ---
        while len(new_pop) < cfg.pop_size:
            p1 = _tournament(pop, vals, cfg.tournament_k, rng)
            p2 = _tournament(pop, vals, cfg.tournament_k, rng)
            child = _blx_crossover(p1, p2, cfg.crossover_alpha, rng)
            child = _mutate(child, sigma, cfg.mutation_prob, rng)
            np.clip(child, lower, upper, out=child)
            new_pop.append(child)

        pop = np.array(new_pop)
        vals = evaluate(pop)
        sigma = sigma * cfg.mutation_decay

        gi = int(np.argmin(vals))
        if vals[gi] < best_fitness:
            best_fitness = float(vals[gi])
            best_genome = pop[gi].copy()
        # keep the incumbent best inside the population (elitism already does,
        # but guard against a generation that lost it to clipping)
        if best_fitness < vals.min():
            worst = int(np.argmax(vals))
            pop[worst] = best_genome
            vals[worst] = best_fitness

    return GAResult(
        best_genome=best_genome,
        best_fitness=best_fitness,
        history=history,
        mean_history=mean_history,
        generations=len(history),
    )


def _tournament(pop, vals, k, rng):
    """Pick k random contestants, return a copy of the fittest (min val)."""
    idx = rng.integers(0, pop.shape[0], size=k)
    winner = idx[int(np.argmin(vals[idx]))]
    return pop[winner].copy()


def _blx_crossover(p1, p2, alpha, rng):
    """BLX-alpha: child gene uniform in the interval spanned by the parents,
    widened by alpha on each side. Standard real-coded recombination."""
    lo = np.minimum(p1, p2)
    hi = np.maximum(p1, p2)
    d = hi - lo
    return lo - alpha * d + rng.random(p1.shape) * (d * (1 + 2 * alpha))


def _mutate(child, sigma, prob, rng):
    """Per-gene Gaussian kick with probability `prob` and scale `sigma`."""
    mask = rng.random(child.shape) < prob
    child = child + mask * rng.normal(0.0, 1.0, child.shape) * sigma
    return child
