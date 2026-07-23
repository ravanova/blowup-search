"""2D rough-data representation for Route A Phase 1 (PHASE1_PLAN.md, Gate 2).

The 2D analog of ga/genome.py's C^{1,alpha} rough-data mode. Phase 0 established
the "rough-data representation principle": the provable De Gregorio / 2D-Boussinesq
blow-ups (Elgindi-Jeong, Chen-Hou, Buckmaster-Gomez-Serrano) need genuine
limited-regularity data — Holder velocity u in C^{1,alpha}, i.e. vorticity in
C^{0,alpha} (continuous, alpha-Holder, NOT C^1) — not the smooth data a
finite-mode Fourier genome reaches. This module builds exactly that in 2D, in the
Hou-Luo symmetry subspace the solver enforces (solver/boussinesq.py):

    vorticity  w  odd in x AND odd in y
    density    th even in x AND odd in y

The construction is the separable Holder product of the 1D profile
P_h(x) = sign(sin x) |sin x|^h (h in (0,1]; h=1 is the smooth endpoint sin x):

    w_h(x, y)  = P_h(x) * P_h(y)              (odd-x, odd-y)
    th_h(x, y) = |sin x|^h * P_h(y)           (even-x, odd-y)

Both carry a genuine C^{0,h} Holder cusp along the wall/axis lines meeting at the
singular corner (0,0). The slice of w_h at y=pi/2 is exactly P_h(x), so the 1D
regularity certificate (real-space local Holder exponent, the |x|^{h-1} slope
blow-up, monotone tail energy) transfers verbatim — see test_genome_rough_2d.py.
Refining the grid resolves more of the cusp (realize_* keeps every grid mode),
which is the knob the Gate 2 fine-N exponent probe turns.
"""

import numpy as np

from ga.genome import holder_profile  # the 1D P_h, reused as the building block
from solver.boussinesq import grid2d, project_even_odd, project_odd_odd

# L2 energy of the smooth endpoint w = sin(x) sin(y): (1/2)*int int w^2 =
# (1/2)*(2pi)^2*mean(sin^2 x sin^2 y) = (1/2)*pi^2. Same role as the 1D
# ENERGY_BUDGET (energy of sin x): one scale for all shapes so fitness compares
# shape, not amplitude.
ENERGY_BUDGET_2D = 0.5 * float(np.pi) ** 2

TWO_PI = 2.0 * np.pi


def energy2d(w):
    """E = (1/2) int int w^2 over [0,2pi)^2 = (1/2)*(2pi)^2*mean(w^2)."""
    return 0.5 * TWO_PI * TWO_PI * float(np.mean(w * w))


def holder_vorticity_2d(h):
    """The odd-x/odd-y rough vorticity callable w_h(X, Y) = P_h(x) P_h(y).
    h in (0,1]: small h = rough (Holder-h cusp along the axes into the corner),
    h=1 = smooth (sin x sin y). Regularity unit-tested in test_genome_rough_2d.py."""
    p = holder_profile(h)  # validates h in (0,1]

    def fn(X, Y):
        return p(X) * p(Y)

    return fn


def holder_density_2d(h):
    """The even-x/odd-y rough density callable th_h(X, Y) = |sin x|^h P_h(y),
    the th-parity partner of holder_vorticity_2d (same cusp regularity)."""
    if not (0.0 < float(h) <= 1.0):
        raise ValueError(f"Holder exponent h must be in (0, 1], got {h}")
    p = holder_profile(h)

    def fn(X, Y):
        return np.abs(np.sin(X)) ** float(h) * p(Y)

    return fn


def realize_holder_vorticity_2d(h, n_grid, energy_budget=ENERGY_BUDGET_2D):
    """w_h evaluated on grid2d(n_grid), projected onto the odd-x/odd-y subspace
    (a no-op up to roundoff — it is already there — but keeps the wall exact) and
    rescaled to the L2 energy budget. Keeps every grid mode, so refining n
    resolves more of the Holder tail: the knob the fine-N exponent probe turns."""
    X, Y = grid2d(n_grid)
    w = project_odd_odd(holder_vorticity_2d(h)(X, Y))
    return w * np.sqrt(energy_budget / energy2d(w))


def realize_holder_density_2d(h, n_grid, energy_budget=ENERGY_BUDGET_2D):
    """th_h on grid2d(n_grid), projected onto even-x/odd-y and energy-normalized."""
    X, Y = grid2d(n_grid)
    th = project_even_odd(holder_density_2d(h)(X, Y))
    return th * np.sqrt(energy_budget / energy2d(th))


def measure_holder_exponent_2d(h, n_slice=1 << 16, x_lo=1e-6, x_hi=1e-2, n=60):
    """Fit the local real-space Holder exponent of w_h at the corner along the
    slice y=pi/2, where w_h(x, pi/2) = P_h(x) exactly. |w_h| ~ C x^h as x->0+,
    so the log-log slope over a small window IS h — the definitional regularity
    certificate, identical in spirit to the 1D measure_holder_exponent."""
    xs = np.logspace(np.log10(x_lo), np.log10(x_hi), n)
    p = holder_profile(h)
    ys = np.abs(p(xs) * p(np.array([np.pi / 2.0])))  # P_h(x) * P_h(pi/2) = P_h(x)
    good = ys > 0.0
    return float(np.polyfit(np.log(xs[good]), np.log(ys[good].ravel()), 1)[0])
