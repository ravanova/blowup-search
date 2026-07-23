"""Regularity unit tests for the C^{1,alpha} rough-data genome mode
(ga/genome.py, PLAN.md Stage 3.6 / Route A Phase 0).

The point of the rough-data mode is to represent genuine limited-regularity
(Holder) vorticity — omega in C^{0,h}, continuous but not C^1 for h<1 — rather
than the smooth/decaying shapes the random-phase k^{-p} envelope reaches. These
tests certify the *intended regularity* directly:

  - the real-space local Holder exponent at the cusp equals the requested h,
  - h=1 is exactly the smooth endpoint sin(x),
  - the profile is genuinely NOT C^1 for h<1 (its slope diverges as the grid
    refines, at the |x|^{h-1} rate), while h=1 stays bounded,
  - roughness is monotone: smaller h puts more energy in the high-k tail,
  - the GA-genome wrapper stays odd and energy-normalized.

Run: .venv/bin/python test_genome_rough.py
"""

import numpy as np

from ga.genome import (
    ENERGY_BUDGET,
    holder_profile,
    measure_holder_exponent,
    realize_holder,
    rough_genome,
    shape_descriptors,
)
from solver.spectral_utils import energy, grid, wavenumbers

H_VALUES = (0.2, 0.35, 0.5, 0.65, 0.8, 1.0)


def _max_abs_derivative(w):
    n = len(w)
    k = wavenumbers(n)
    w_hat = np.fft.rfft(w)
    w_x = np.fft.irfft(1j * k * w_hat, n)
    return float(np.max(np.abs(w_x)))


def test_holder_exponent_matches_requested():
    # The definitional regularity certificate: |f_h(x)| ~ x^h near the cusp,
    # so the fitted local exponent recovers h.
    for h in H_VALUES:
        measured = measure_holder_exponent(holder_profile(h))
        assert abs(measured - h) < 1e-3, f"h={h}: measured {measured:.4f}"


def test_smooth_endpoint_is_exactly_sine():
    x = grid(1024)
    assert np.max(np.abs(holder_profile(1.0)(x) - np.sin(x))) == 0.0


def test_rough_profile_is_not_c1():
    # For h<1 the cusp slope |f'| ~ |x|^{h-1} is unresolved, so max|f'| grows
    # without bound as the grid refines; h=1 (smooth) stays flat. This is the
    # C^{0,h}-not-C^1 signature the whole rough-data mode exists to provide.
    grids = (512, 2048, 8192, 32768)
    smooth = [_max_abs_derivative(holder_profile(1.0)(grid(n))) for n in grids]
    assert max(smooth) - min(smooth) < 1e-6, smooth  # bounded

    refine = grids[-1] / grids[0]  # total refinement factor (64x)
    for h in (0.2, 0.5, 0.8):
        d = [_max_abs_derivative(holder_profile(h)(grid(n))) for n in grids]
        # strictly increasing, and growing at ~the theoretical |x|^{h-1} rate
        # (max|f'| ~ N^{1-h}); require at least 0.6x that so the check tracks
        # the mechanism, not an arbitrary constant.
        assert all(b > a for a, b in zip(d, d[1:])), (h, d)
        assert d[-1] / d[0] > 0.6 * refine ** (1.0 - h), (h, d)


def test_roughness_is_monotone_in_h():
    # Analytic profile: energy fraction above a fixed mode rises as h falls.
    ng = 1 << 16
    x = grid(ng)
    fracs = []
    for h in (1.0, 0.8, 0.6, 0.4, 0.2):
        e = np.abs(np.fft.rfft(holder_profile(h)(x))) ** 2
        fracs.append(float(e[33:].sum() / e.sum()))  # energy above k=32
    assert all(b > a for a, b in zip(fracs, fracs[1:])), fracs

    # GA-genome wrapper: the logged spectral_tail_slope descriptor (the
    # smooth-vs-Holder axis) is less negative (rougher) for smaller h. (h=1 is
    # excluded: it is a single mode, sin x, whose tail is machine-zero and
    # whose slope is therefore undefined — the smooth endpoint is certified by
    # the analytic energy-fraction check above.)
    slopes = [shape_descriptors(rough_genome(h, 64))["spectral_tail_slope"]
              for h in (0.8, 0.6, 0.4, 0.2)]
    assert all(b > a for a, b in zip(slopes, slopes[1:])), slopes


def test_rough_genome_normalized_and_odd():
    for h in (0.2, 0.5, 0.9):
        g = rough_genome(h, 48)
        from ga.genome import realize

        assert abs(energy(realize(g, 512)) - ENERGY_BUDGET) < 1e-10, h
        # odd on the grid: f(x) = -f(2pi - x)
        w = realize(g, 512)
        assert np.max(np.abs(w[1:] + w[1:][::-1])) < 1e-9, h


def test_realize_holder_energy_and_grid():
    for h in (0.3, 0.7):
        for n in (256, 1024, 4096):
            w = realize_holder(h, n)
            assert len(w) == n
            assert abs(energy(w) - ENERGY_BUDGET) < 1e-10, (h, n)


def test_holder_exponent_domain_guard():
    for bad in (0.0, -0.3, 1.5):
        try:
            holder_profile(bad)
            raise AssertionError(f"h={bad} should be rejected")
        except ValueError:
            pass


if __name__ == "__main__":
    tests = [obj for name, obj in list(globals().items())
             if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print(f"\n{len(tests)}/{len(tests)} tests passed.")
