"""Regularity unit tests for the 2D rough-data mode (ga/genome2d.py, Gate 2).

The 2D analog of test_genome_rough.py. The point of the mode is genuine
limited-regularity (Holder) vorticity — w in C^{0,h}, continuous but not C^1 for
h<1 — in the Hou-Luo symmetry subspace, not the smooth data a finite Fourier
genome reaches. These certify the intended regularity directly:

  - the real-space local Holder exponent at the corner equals the requested h,
  - h=1 is exactly the smooth endpoint sin(x) sin(y),
  - the profile is genuinely NOT C^1 for h<1 (the cusp x-slope diverges as the
    grid refines, at the |x|^{h-1} i.e. N^{1-h} rate), while h=1 stays bounded,
  - roughness is monotone: smaller h puts more energy in the high-k tail,
  - the realized fields sit in the correct parity subspace (odd-x/odd-y for w,
    even-x/odd-y for th) and are energy-normalized.

Run: .venv/bin/python test_genome_rough_2d.py
"""

import numpy as np

from ga.genome2d import (
    ENERGY_BUDGET_2D,
    energy2d,
    holder_density_2d,
    holder_vorticity_2d,
    measure_holder_exponent_2d,
    realize_holder_density_2d,
    realize_holder_vorticity_2d,
)
from solver.boussinesq import grid2d, parity_residual, wavenumbers2d

H_VALUES = (0.2, 0.35, 0.5, 0.65, 0.8, 1.0)


def _max_abs_dx(w):
    """max |d w / dx| over the grid, spectrally."""
    n = w.shape[0]
    KX, KY, _, _ = wavenumbers2d(n)
    return float(np.max(np.abs(np.fft.ifft2(1j * KX * np.fft.fft2(w)).real)))


def test_holder_exponent_matches_requested():
    # |w_h(x, pi/2)| ~ x^h near the corner, so the fitted local exponent is h.
    for h in H_VALUES:
        measured = measure_holder_exponent_2d(h)
        assert abs(measured - h) < 1e-3, f"h={h}: measured {measured:.4f}"


def test_smooth_endpoint_is_exactly_sine():
    X, Y = grid2d(256)
    w = holder_vorticity_2d(1.0)(X, Y)
    assert np.max(np.abs(w - np.sin(X) * np.sin(Y))) < 1e-15


def test_rough_profile_is_not_c1():
    # For h<1 the corner slope |w_x| ~ |x|^{h-1} is unresolved, so max|w_x| grows
    # as N^{1-h} under refinement; h=1 (smooth) stays flat. The C^{0,h}-not-C^1
    # signature, in 2D.
    grids = (256, 512, 1024, 2048)
    smooth = []
    for n in grids:
        X, Y = grid2d(n)
        smooth.append(_max_abs_dx(holder_vorticity_2d(1.0)(X, Y)))
    assert max(smooth) - min(smooth) < 1e-6, smooth  # bounded

    refine = grids[-1] / grids[0]  # 8x
    for h in (0.2, 0.5, 0.8):
        d = []
        for n in grids:
            X, Y = grid2d(n)
            d.append(_max_abs_dx(holder_vorticity_2d(h)(X, Y)))
        assert all(b > a for a, b in zip(d, d[1:])), (h, d)
        # growing at ~the theoretical N^{1-h} rate; require >= 0.6x of it.
        assert d[-1] / d[0] > 0.6 * refine ** (1.0 - h), (h, d)


def test_roughness_is_monotone_in_h():
    # Energy fraction above a fixed 2D shell rises as h falls.
    n = 2048
    X, Y = grid2d(n)
    KX, KY, Ksq, _ = wavenumbers2d(n)
    shell = Ksq > 32.0 ** 2
    fracs = []
    for h in (1.0, 0.8, 0.6, 0.4, 0.2):
        e = np.abs(np.fft.fft2(holder_vorticity_2d(h)(X, Y))) ** 2
        fracs.append(float(e[shell].sum() / e.sum()))
    assert all(b > a for a, b in zip(fracs, fracs[1:])), fracs


def test_realized_fields_parity_and_energy():
    for h in (0.2, 0.5, 0.9, 1.0):
        w = realize_holder_vorticity_2d(h, 256)
        th = realize_holder_density_2d(h, 256)
        assert parity_residual(w, "odd_odd") < 1e-12, ("w", h)
        assert parity_residual(th, "even_odd") < 1e-12, ("th", h)
        assert abs(energy2d(w) - ENERGY_BUDGET_2D) < 1e-9, ("w energy", h)
        assert abs(energy2d(th) - ENERGY_BUDGET_2D) < 1e-9, ("th energy", h)


def test_realize_grid_sizes():
    for h in (0.3, 0.7):
        for n in (128, 256, 512):
            w = realize_holder_vorticity_2d(h, n)
            assert w.shape == (n, n)


def test_holder_exponent_domain_guard():
    for bad in (0.0, -0.3, 1.5):
        for factory in (holder_vorticity_2d, holder_density_2d):
            try:
                factory(bad)
                raise AssertionError(f"h={bad} should be rejected by {factory.__name__}")
            except ValueError:
                pass


if __name__ == "__main__":
    tests = [obj for name, obj in list(globals().items())
             if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print(f"\n{len(tests)}/{len(tests)} tests passed.")
