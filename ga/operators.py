"""Genetic operators for the Stage 2 GA (PLAN.md Stage 2).

Every operator returns a NORMALIZED genome (fixed L2 energy budget, applied
after the k^{-p} envelope) — the scale-covariance guard. test_ga.py asserts
this for each operator individually.

Selection draws parents from the MAP-Elites archive (tournament over
randomly chosen filled cells), per the PLAN.md quality-diversity reframe:
the archive structurally holds one elite per shape niche, and tournament
pressure among niches is the only fitness pressure on parent choice.
"""

import numpy as np

from ga.genome import ENERGY_BUDGET, Genome, normalize


def tournament_select(archive_entries, rng, k=3):
    """Pick the highest-fitness of k uniformly drawn archive elites.
    `archive_entries` is a sequence of dicts with a "fitness" key."""
    if not archive_entries:
        raise ValueError("cannot select from an empty archive")
    picks = rng.choice(len(archive_entries), size=min(k, len(archive_entries)),
                       replace=False)
    return max((archive_entries[i] for i in picks), key=lambda e: e["fitness"])


def blend_crossover(parent_a, parent_b, rng, energy_budget=ENERGY_BUDGET):
    """Arithmetic blend with one random weight for the coefficients and an
    independent one for the envelope exponent p."""
    w = float(rng.uniform(0.0, 1.0))
    wp = float(rng.uniform(0.0, 1.0))
    child = Genome(
        coeffs=w * np.asarray(parent_a.coeffs) + (1 - w) * np.asarray(parent_b.coeffs),
        envelope_p=wp * parent_a.envelope_p + (1 - wp) * parent_b.envelope_p,
    )
    return normalize(child, energy_budget)


def mutate(genome, rng, scale, p_scale, p_range, energy_budget=ENERGY_BUDGET):
    """Per-gene Gaussian perturbation, sized relative to the RMS coefficient
    so the pressure is scale-free; p gets its own Gaussian step, clipped to
    the evolvable range. `scale` follows the decaying schedule in config."""
    coeffs = np.asarray(genome.coeffs, dtype=float)
    rms = float(np.sqrt(np.mean(coeffs * coeffs)))
    child = Genome(
        coeffs=coeffs + rng.normal(0.0, scale * rms, size=len(coeffs)),
        envelope_p=float(np.clip(genome.envelope_p + rng.normal(0.0, p_scale),
                                 p_range[0], p_range[1])),
    )
    return normalize(child, energy_budget)


def mutation_scale(schedule, generation_index):
    """Decaying mutation scale: initial * decay^generation."""
    return schedule["initial"] * schedule["decay"] ** generation_index
