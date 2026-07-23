"""Smooth 2D genome over the Hou-Luo parity subspace (Route A Phase 1, Gate 3).

The smooth-data counterpart to ga/genome2d.py's rough mode (deprioritised per
PHASE1_SPIKE_RESULTS.md: rough C^{0,a} data is resolution-starved from t=0 on a
uniform grid). A genome is a pair of low-bandwidth truncated Fourier coefficient
tables in the symmetry subspace the solver enforces (solver/boussinesq.py):

    omega(x,y) = sum_{j,k=1..K}     a_jk sin(j x) sin(k y)     (odd-x, odd-y)
    theta(x,y) = sum_{j=0..K,k=1..K} b_jk cos(j x) sin(k y)    (even-x, odd-y)

with K small (default 4) so every active mode sits well inside the 2/3-dealiased
band -- the fields are C^infinity and grid-resolved from t=0, the regime the spike
found viable. This is the 2D analog of ga/genome.py.

Normalization (the amplitude-cheat guard, PHASE1_PLAN.md fixed-energy-budget
principle): the raw (a, b) are rescaled by a SINGLE joint scalar so the total
field energy E_omega + E_theta equals TOTAL_BUDGET_2D. Overall amplitude is thus
pinned -- the 2D amplitude cheat (scale both fields up so more viscosity is needed
to kill them, the analog of the 1D w -> lambda*w cheat) is removed -- while the
physically meaningful omega/theta ENERGY RATIO (buoyancy strength) stays free and
is read off as the `split` descriptor. Because normalization is one scalar
multiply, amplitude-rescaled copies of a shape normalize to the same coefficients
(up to float rounding), so the fitness cache can key on the genome hash.

Descriptors (all four LOGGED per genome; the archive BINS on the first two, per
the Gate-3 design decision -- anisotropy x centroid are pure-geometry,
mutually orthogonal on random draws (|r| < 0.02), and put the property-6
low-mode-collapse trap legibly on the centroid axis; alignment + split are logged
diagnostics that Gate 4 can re-bin onto for free from the logs):
  - anisotropy = energy-weighted (<j^2> - <k^2>) / (<j^2> + <k^2>) of omega,
    in [-1, 1]: +1 = all x-structure (tall thin fronts), -1 = all y-structure.
  - centroid   = energy-weighted <sqrt(j^2+k^2)> of omega, the scale axis, in
    [sqrt(2), sqrt(2)*K].
  - split      = E_theta / (E_theta + E_omega), the buoyancy-strength ratio.
  - alignment  = normalized spatial correlation of the buoyancy torque theta_x
    with omega, in [-1, 1]: how the forcing overlaps the vorticity at t=0.
All four are scale-invariant (ratios / normalized correlations), so they are read
straight off the raw genome without needing normalization first.
"""

import hashlib
from dataclasses import dataclass

import numpy as np

from ga.genome2d import ENERGY_BUDGET_2D, energy2d
from solver.boussinesq import grid2d, project_even_odd, project_odd_odd

DEFAULT_K = 4

# Total field-energy budget split between the two fields; the split=0.5 point puts
# each field at ENERGY_BUDGET_2D (energy of sin x sin y), matching ga/genome2d.py.
TOTAL_BUDGET_2D = 2.0 * ENERGY_BUDGET_2D

# Grid the (grid-based) descriptors are computed on. Fixed and resolution-free by
# design: exact for bandlimited K << N/2 fields (LOGGING.md -- descriptors are a
# property of the genome, not of any solver grid).
_DESCRIPTOR_GRID_N = 64

# MAP-Elites archive geometry (the Gate-3 design decision). Bin on the two
# pure-geometry axes; log all four so binning is a post-hoc, re-runnable choice.
MAP_ELITES_2D = {
    "descriptors": ["anisotropy", "centroid"],
    "cells_per_axis": [12, 10],
    "descriptor_bounds": {
        "anisotropy": [-1.0, 1.0],
        "centroid": [float(np.sqrt(2.0)), float(np.sqrt(2.0) * DEFAULT_K)],
    },
    "logged_descriptors": ["anisotropy", "centroid", "split", "alignment"],
}


@dataclass
class Genome2D:
    """Smooth Hou-Luo-subspace initial condition. `a` is (K, K): a[j-1, k-1]
    multiplies sin(jx) sin(ky), j,k = 1..K. `b` is (K+1, K): b[j, k-1] multiplies
    cos(jx) sin(ky), j = 0..K, k = 1..K (the j=0 row is the x-constant theta
    modes, present in the Luo-Hou benchmark IC)."""

    a: np.ndarray  # (K, K)   vorticity coeffs
    b: np.ndarray  # (K+1, K) density coeffs

    def __post_init__(self):
        self.a = np.asarray(self.a, dtype=float)
        self.b = np.asarray(self.b, dtype=float)
        if self.a.ndim != 2 or self.a.shape[0] != self.a.shape[1]:
            raise ValueError(f"a must be a square (K,K) array, got {self.a.shape}")
        if self.b.shape != (self.a.shape[0] + 1, self.a.shape[0]):
            raise ValueError(
                f"b must be (K+1,K)=({self.a.shape[0]+1},{self.a.shape[0]}), "
                f"got {self.b.shape}")

    @property
    def K(self):
        return self.a.shape[0]


def _jk_meshes(K):
    """(J, Kk) integer meshes over the omega modes j,k = 1..K, shape (K, K)."""
    j = np.arange(1, K + 1)
    return np.meshgrid(j, j, indexing="ij")


def _fields_raw(genome, n):
    """The (unnormalized) omega, theta fields the raw coeffs encode, on grid2d(n).
    Built directly from the sin/cos basis (exact parity to machine precision)."""
    X, Y = grid2d(n)
    K = genome.K
    om = np.zeros((n, n))
    th = np.zeros((n, n))
    for j in range(1, K + 1):
        sjx = np.sin(j * X)
        for k in range(1, K + 1):
            aa = genome.a[j - 1, k - 1]
            if aa != 0.0:
                om += aa * sjx * np.sin(k * Y)
    for j in range(0, K + 1):
        cjx = np.cos(j * X)
        for k in range(1, K + 1):
            bb = genome.b[j, k - 1]
            if bb != 0.0:
                th += bb * cjx * np.sin(k * Y)
    return om, th


def _raw_energies(genome, n=_DESCRIPTOR_GRID_N):
    om, th = _fields_raw(genome, n)
    return energy2d(om), energy2d(th)


def _joint_scale(genome, n=_DESCRIPTOR_GRID_N):
    """The single scalar s with s^2*(E_omega + E_theta) = TOTAL_BUDGET_2D. Energy
    of a bandlimited field is grid-independent (exact quadrature for n > 2K), so s
    is the same whether measured on the descriptor grid or the solver grid."""
    e_om, e_th = _raw_energies(genome, n)
    e = e_om + e_th
    if e <= 0.0:
        raise ValueError("genome encodes the zero field; cannot normalize")
    return float(np.sqrt(TOTAL_BUDGET_2D / e))


def normalize(genome):
    """Rescale (a, b) by the single joint scalar so the total field energy equals
    the budget. Applied after every operator (the fixed-energy-budget constraint).
    One scalar multiply, so amplitude-rescaled copies map to the same coeffs up to
    float rounding (the genome-hash cache-key property)."""
    s = _joint_scale(genome)
    return Genome2D(a=genome.a * s, b=genome.b * s)


def realize(genome, n):
    """Evaluate the genome's (omega0, theta0) on grid2d(n), energy-normalized to
    the budget and parity-projected (exact wall, against roundoff). Raises if the
    bandwidth K exceeds the 2/3-dealiased band k <= n//3 at this resolution."""
    K = genome.K
    if K > n // 3:
        raise ValueError(
            f"genome bandwidth K={K} exceeds the 2/3-dealiased band k<={n // 3} "
            f"at N={n}; raise the solver resolution or shrink K")
    om, th = _fields_raw(genome, n)
    e = energy2d(om) + energy2d(th)
    if e <= 0.0:
        raise ValueError("genome encodes the zero field; cannot realize")
    s = np.sqrt(TOTAL_BUDGET_2D / e)
    return project_odd_odd(om * s), project_even_odd(th * s)


def random_genome(rng, K=DEFAULT_K, envelope_range=(0.0, 3.0)):
    """Init/baseline draw: each field's coeffs ~ N(0,1) times an independent
    random spectral envelope (j^2+k^2)^(-p/2) whose exponent p ~ U(envelope_range)
    spreads draws across the centroid (scale) axis, then joint-normalized."""
    JJ, KK = _jk_meshes(K)
    p = float(rng.uniform(*envelope_range))
    a = rng.standard_normal((K, K)) * (JJ ** 2 + KK ** 2) ** (-p / 2.0)
    q = float(rng.uniform(*envelope_range))
    jt = np.arange(0, K + 1)
    JT, KT = np.meshgrid(jt, np.arange(1, K + 1), indexing="ij")
    b = rng.standard_normal((K + 1, K)) * (JT ** 2 + KT ** 2 + 1.0) ** (-q / 2.0)
    return normalize(Genome2D(a=a, b=b))


def genome2d_hash(genome):
    """Stable identity of a normalized genome -- keys the fitness cache and the
    reproducibility audit, the 2D analog of ga.logbook.genome_hash."""
    g = normalize(genome)
    h = hashlib.sha256()
    h.update(np.ascontiguousarray(g.a, dtype=np.float64).tobytes())
    h.update(np.ascontiguousarray(g.b, dtype=np.float64).tobytes())
    h.update(f"K={g.K}".encode())
    return h.hexdigest()


def shape_descriptors(genome):
    """The four logged descriptors (anisotropy, centroid, split, alignment),
    computed from the raw genome -- all are scale-invariant, so no normalization
    is needed. anisotropy/centroid come from the omega mode weights analytically;
    split/alignment from the fields on the fixed descriptor grid."""
    K = genome.K
    JJ, KK = _jk_meshes(K)
    w = genome.a * genome.a
    wsum = float(w.sum())
    if wsum <= 0.0:
        raise ValueError("omega component is zero; anisotropy/centroid undefined")
    denom = float(np.sum(w * (JJ ** 2 + KK ** 2)))
    anisotropy = float(np.sum(w * (JJ ** 2 - KK ** 2)) / denom)
    centroid = float(np.sum(w * np.sqrt(JJ ** 2 + KK ** 2)) / wsum)

    e_om, e_th = _raw_energies(genome)
    split = float(e_th / (e_om + e_th)) if (e_om + e_th) > 0.0 else 0.0

    # alignment: normalized correlation of the buoyancy torque theta_x with omega
    # (both odd-x/odd-y). theta_x = -sum b_jk j sin(jx) sin(ky).
    X, Y = grid2d(_DESCRIPTOR_GRID_N)
    om, _ = _fields_raw(genome, _DESCRIPTOR_GRID_N)
    thx = np.zeros_like(om)
    for j in range(1, K + 1):  # j=0 contributes nothing to theta_x
        sjx = np.sin(j * X)
        for k in range(1, K + 1):
            bb = genome.b[j, k - 1]
            if bb != 0.0:
                thx += -bb * j * sjx * np.sin(k * Y)
    n1 = float(np.sqrt(np.mean(thx * thx)))
    n2 = float(np.sqrt(np.mean(om * om)))
    alignment = float(np.mean(thx * om) / (n1 * n2)) if (n1 > 0.0 and n2 > 0.0) else 0.0

    return {
        "anisotropy": anisotropy,
        "centroid": centroid,
        "split": split,
        "alignment": alignment,
    }
