"""Genome representation for the Stage 2 GA (PLAN.md Stage 2).

A genome is (raw sine coefficients c_1..c_N, spectral-decay exponent p).
The field it encodes is

    w(x) = sum_k  b_k sin(k x),      b_k = s * c_k * k^{-p}

with the single scale s chosen so the L2 energy (1/2)∫w² = (pi/2)·Σb_k²
equals the fixed energy budget. The k^{-p} envelope is the evolvable
regularity axis (small p = rough/Hölder-like, large p = smooth) — see the
Stage 1 regularity caveat; the energy renormalization is applied AFTER the
envelope, killing the scale-covariance cheat (`w -> λw` blows up λ× faster,
so without it the GA optimizes amplitude, not shape).

`normalize()` folds the scale into the raw coefficients as a single scalar
multiply, so amplitude-rescaled copies of a shape normalize to the same
coefficients up to float rounding (the fitness cache keys on the bitwise
`genome_hash`, whose hits come from byte-identical genomes). Every operator
in ga/operators.py returns normalized genomes; test_ga.py asserts the
realized energy equals the budget after each operator and after any
envelope change.

Energy identity used throughout (exact, not quadrature): for w = Σ b_k
sin(kx) on [0, 2π), (1/2)∫w² = (π/2)·Σ b_k². Grid quadrature in
solver.spectral_utils.energy agrees exactly for bandlimited fields, which
test_ga.py also checks.
"""

from dataclasses import dataclass

import numpy as np

from solver.spectral_utils import grid

ENERGY_BUDGET = float(np.pi) / 2.0  # L2 energy of sin(x) — same scale as Stage 1.5

# Grid the shape descriptors are computed on. Fixed and resolution-free by
# design (LOGGING.md: descriptors are computed once at write time from the
# genome, not from any particular solver grid).
_DESCRIPTOR_GRID_N = 512


@dataclass
class Genome:
    coeffs: np.ndarray  # raw sine coefficients c_1..c_N
    envelope_p: float

    @property
    def n(self):
        return len(self.coeffs)


def _envelope(n, p):
    return np.arange(1, n + 1, dtype=float) ** (-float(p))


def effective_coeffs(genome, energy_budget=ENERGY_BUDGET):
    """b_k after the envelope AND the energy renormalization — the
    coefficients of the field the solver actually integrates."""
    b = np.asarray(genome.coeffs, dtype=float) * _envelope(genome.n, genome.envelope_p)
    sum_sq = float(np.sum(b * b))
    if sum_sq <= 0.0:
        raise ValueError("genome encodes the zero field; cannot normalize")
    return b * np.sqrt(energy_budget / ((np.pi / 2.0) * sum_sq))


def normalize(genome, energy_budget=ENERGY_BUDGET):
    """Scale the raw coeffs (one scalar multiply) so the POST-envelope energy
    equals the budget. Applied after EVERY operator (PLAN.md's fixed-energy-
    budget constraint); after it, effective_coeffs is coeffs * k^{-p} up to
    float rounding."""
    coeffs = np.asarray(genome.coeffs, dtype=float)
    b = coeffs * _envelope(genome.n, genome.envelope_p)
    sum_sq = float(np.sum(b * b))
    if sum_sq <= 0.0:
        raise ValueError("genome encodes the zero field; cannot normalize")
    scale = np.sqrt(energy_budget / ((np.pi / 2.0) * sum_sq))
    return Genome(coeffs=coeffs * scale, envelope_p=float(genome.envelope_p))


def realize(genome, n_grid, energy_budget=ENERGY_BUDGET):
    """Evaluate the genome's field on the solver grid(n_grid)."""
    b = effective_coeffs(genome, energy_budget)
    if genome.n > n_grid // 3:
        raise ValueError(
            f"genome has modes up to k={genome.n} but the 2/3-dealiased band "
            f"at N={n_grid} keeps only k<={n_grid // 3}; raise the solver "
            "resolution or shrink the genome")
    x = grid(n_grid)
    return np.sin(np.outer(x, np.arange(1, genome.n + 1))) @ b


def random_genome(rng, n, p_range, energy_budget=ENERGY_BUDGET):
    """Init/baseline draw: c_k ~ N(0,1), p ~ U(p_range), normalized."""
    return normalize(
        Genome(coeffs=rng.standard_normal(n),
               envelope_p=float(rng.uniform(*p_range))),
        energy_budget,
    )


def from_sine_pairs(pairs, n, energy_budget=ENERGY_BUDGET):
    """Genome from explicit (k, c_k) sine pairs — how baseline_literature
    profiles are re-sampled onto the current genome length at run start
    (LOGGING.md schema #3). Modes above n are truncated; p=0 so the raw
    coefficients ARE the profile."""
    coeffs = np.zeros(n)
    for k, c in pairs:
        if 1 <= k <= n:
            coeffs[k - 1] += c
    return normalize(Genome(coeffs=coeffs, envelope_p=0.0), energy_budget)


def project_to_sines(fn, n, energy_budget=ENERGY_BUDGET):
    """Project an odd analytic profile onto the first n sine modes (exact
    sine transform on a fine grid) — re-sampling for non-bandlimited
    literature profiles like the localized bump pair."""
    n_fine = 4096
    x = grid(n_fine)
    w = fn(x)
    w_hat = np.fft.rfft(w)
    # For real odd data, w_hat[k] = -i * (n_fine/2) * b_k.
    coeffs = -2.0 * np.imag(w_hat[1:n + 1]) / n_fine
    return normalize(Genome(coeffs=coeffs, envelope_p=0.0), energy_budget)


def shape_descriptors(genome, energy_budget=ENERGY_BUDGET):
    """The three logged descriptors (LOGGING.md schema #3), computed from the
    effective coefficients: n_sign_changes, spectral_tail_slope (the MAP-
    Elites regularity axis and the frequency-cheating guardrail),
    energy_top_k_frac."""
    b = effective_coeffs(genome, energy_budget)
    n = len(b)

    x = grid(_DESCRIPTOR_GRID_N)
    w = np.sin(np.outer(x, np.arange(1, n + 1))) @ b
    sgn = np.sign(w)
    sgn[sgn == 0] = 1.0
    n_sign_changes = int(np.sum(np.diff(np.concatenate([sgn, sgn[:1]])) != 0))

    # Tail slope: least-squares slope of log|b_k| vs log k over the upper
    # half of the mode band (the tail — the smooth-vs-Hölder axis).
    k_tail = np.arange(n // 2, n + 1, dtype=float)
    b_tail = np.abs(b[n // 2 - 1:]) + 1e-14
    lk = np.log(k_tail)
    slope = float(np.polyfit(lk, np.log(b_tail), 1)[0])

    b_sq = np.sort(b * b)[::-1]
    top_k = min(4, n)
    energy_top_k_frac = float(np.sum(b_sq[:top_k]) / np.sum(b_sq))

    return {
        "n_sign_changes": n_sign_changes,
        "spectral_tail_slope": slope,
        "energy_top_k_frac": energy_top_k_frac,
    }
