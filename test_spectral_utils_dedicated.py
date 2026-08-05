"""Dedicated unit tests for solver/spectral_utils.py (leg 66, Route-QF).

`capabilities.py` recorded this module as having "no dedicated test file --
exercised through the solvers above". Leg 66's coverage audit
(writeup/novelty/leg_66.md) found that five of its ten public symbols
(`dealias_mask`, `velocity_hat`, `derivative_hat`, `l1_norm`,
`energy_production`) are named by NONE of the repository's 52 test files.
They are executed on the hot path of every gCLM run, so a catastrophic error
would surface end-to-end; anything short of catastrophic would not.

This file asks each helper a question it can fail on its own terms: a
hand-computed value, an exact spectral identity, or a reference computed
WITHOUT the module's own machinery.

Test convention (repo-wide): self-running script, no pytest.
    .venv/bin/python test_spectral_utils_dedicated.py

FINDING (leg 66, gate answered YES): `derivative_hat` is wrong on ODD-length
grids -- see check_derivative_odd_n_known_defect below. Pinned, not patched:
under this leg's territory rules a bug in solver/ is reported, not silently
fixed.
"""

import numpy as np

from solver.spectral_utils import (
    TWO_PI,
    dealias_mask,
    derivative_hat,
    energy,
    energy_production,
    grid,
    hilbert_hat,
    integral,
    l1_norm,
    velocity_hat,
    wavenumbers,
)

TOL = 1e-12


def _d(w, n):
    """Physical-space spectral derivative of w on an n-point grid."""
    return np.fft.irfft(derivative_hat(np.fft.rfft(w), wavenumbers(n)), n)


def _h(w, n):
    """Physical-space Hilbert transform of w on an n-point grid."""
    return np.fft.irfft(hilbert_hat(np.fft.rfft(w), wavenumbers(n)), n)


# --- grid / wavenumbers / dealias_mask: exact combinatorial facts ---------


def check_grid():
    """grid(n) is 0, 2pi/n, ..., 2pi(n-1)/n -- no endpoint duplication."""
    out = {}
    for n in (1, 2, 7, 16, 64):
        x = grid(n)
        assert len(x) == n, n
        assert x[0] == 0.0, n
        if n > 1:
            spacing = np.diff(x)
            out[f"n{n}_spacing_err"] = float(
                np.max(np.abs(spacing - TWO_PI / n))
            )
            assert out[f"n{n}_spacing_err"] < TOL, (n, out)
            # the grid must NOT contain 2*pi (that would duplicate x=0)
            assert x[-1] < TWO_PI - 1e-15, n
            assert abs(x[-1] - TWO_PI * (n - 1) / n) < TOL, n
    return out


def check_wavenumbers():
    """wavenumbers(n) is exactly the integers 0..n//2 -- even AND odd n.

    rfftfreq(n, d=1/n) is documented to return floats; the solvers use these
    as integer wavenumbers, so the integrality is load-bearing (a 0.5 offset
    would silently detune every multiplier in the module).
    """
    out = {}
    for n in (2, 8, 9, 15, 16, 17, 64, 65):
        k = wavenumbers(n)
        expected = np.arange(n // 2 + 1, dtype=float)
        assert len(k) == n // 2 + 1, (n, len(k))
        err = float(np.max(np.abs(k - expected)))
        out[f"n{n}_int_err"] = err
        assert err == 0.0, (n, err)
        # rfft of a real n-vector has exactly this many modes
        assert len(np.fft.rfft(np.zeros(n))) == len(k), n
    return out


def check_dealias_mask():
    """2/3 rule: keep |k| <= n/3, boundary included, counted exactly.

    Named by zero existing tests. The off-by-one that matters is at the
    cut itself, so both n divisible by 3 (cut is an attained integer) and
    n not divisible by 3 are checked.
    """
    out = {}
    for n in (16, 32, 48, 64, 96, 128):
        mask = dealias_mask(n)
        k = wavenumbers(n)
        assert len(mask) == len(k), n
        n_kept = int(mask.sum())
        n_expected = int(np.sum(k <= n / 3.0))
        assert n_kept == n_expected, (n, n_kept, n_expected)
        out[f"n{n}_kept"] = n_kept
        # boundary, explicitly: highest kept mode and lowest dropped mode
        k_hi = int(np.max(k[mask]))
        out[f"n{n}_k_hi"] = k_hi
        assert k_hi <= n / 3.0, (n, k_hi)
        assert k_hi + 1 > n / 3.0, (n, k_hi)
        assert bool(mask[0]), n  # the mean mode is always kept
    # n = 96: the cut 32 is exactly attained and MUST be kept (<=, not <)
    assert bool(dealias_mask(96)[32]), "k = n/3 must be retained"
    assert not bool(dealias_mask(96)[33])
    return out


# --- hilbert_hat: the sign convention the whole repository rests on -------


def check_hilbert_convention():
    """H(sin x) = -cos x, H(cos x) = sin x, H(const) = 0.

    The module docstring pins this convention because the CLM closed-form
    blow-up solution used for validation depends on it. A global sign flip
    here would turn blow-up into decay, so it is worth an assertion that
    does not go through a solver.
    """
    out = {}
    n = 64
    x = grid(n)
    for label, w, expected in [
        ("sin", np.sin(x), -np.cos(x)),
        ("cos", np.cos(x), np.sin(x)),
        ("sin3x", np.sin(3 * x), -np.cos(3 * x)),
        ("const", np.ones(n), np.zeros(n)),
        ("const+sin", 5.0 + np.sin(x), -np.cos(x)),
    ]:
        err = float(np.max(np.abs(_h(w, n) - expected)))
        out[f"{label}_err"] = err
        assert err < TOL, (label, err)
    return out


def check_hilbert_algebra():
    """H^2 = -Id on zero-mean data; H is skew: int f*H(g) = -int g*H(f).

    Both are exact for band-limited data, and neither is implied by the
    single-mode checks above.
    """
    out = {}
    n = 64
    x = grid(n)
    rng = np.random.default_rng(66)
    w = np.zeros(n)
    for k in range(1, 12):
        w += rng.standard_normal() * np.sin(k * x) + rng.standard_normal() * np.cos(k * x)
    hh = _h(_h(w, n), n)
    out["h_squared_err"] = float(np.max(np.abs(hh + w))) / float(np.max(np.abs(w)))
    assert out["h_squared_err"] < 1e-13, out

    g = np.zeros(n)
    for k in range(1, 12):
        g += rng.standard_normal() * np.sin(k * x) + rng.standard_normal() * np.cos(k * x)
    lhs = integral(w * _h(g, n))
    rhs = -integral(g * _h(w, n))
    out["skew_err"] = abs(lhs - rhs) / max(abs(lhs), 1e-300)
    assert out["skew_err"] < 1e-12, out
    return out


# --- velocity_hat: u_x = H(w), zero mean ---------------------------------


def check_velocity_hat():
    """u_hat = -w_hat/|k| really does solve u_x = H(w) with mean(u) = 0.

    Named by zero existing tests, yet it defines the transport velocity of
    every gCLM run with a != 0.
    """
    out = {}
    n = 64
    x = grid(n)
    k = wavenumbers(n)

    # single mode, hand value: w = sin(3x) -> u = -sin(3x)/3
    w = np.sin(3 * x)
    u = np.fft.irfft(velocity_hat(np.fft.rfft(w), k), n)
    out["single_mode_err"] = float(np.max(np.abs(u + np.sin(3 * x) / 3.0)))
    assert out["single_mode_err"] < TOL, out

    # general band-limited data: u_x must equal H(w) exactly
    rng = np.random.default_rng(1966)
    w = np.zeros(n)
    for j in range(1, 12):
        w += rng.standard_normal() * np.sin(j * x) + rng.standard_normal() * np.cos(j * x)
    w += 3.7  # a nonzero mean, to exercise the k = 0 branch
    w_hat = np.fft.rfft(w)
    u = np.fft.irfft(velocity_hat(w_hat, k), n)
    scale = float(np.max(np.abs(_h(w, n))))
    out["u_x_vs_Hw_err"] = float(np.max(np.abs(_d(u, n) - _h(w, n)))) / scale
    assert out["u_x_vs_Hw_err"] < 1e-13, out
    out["u_mean_abs"] = abs(float(np.mean(u)))
    assert out["u_mean_abs"] < 1e-14, out

    # a pure mean field has no velocity at all
    u0 = np.fft.irfft(velocity_hat(np.fft.rfft(np.full(n, 2.5)), k), n)
    out["mean_only_u_max"] = float(np.max(np.abs(u0)))
    assert out["mean_only_u_max"] == 0.0, out
    return out


# --- derivative_hat ------------------------------------------------------


def check_derivative_even_n():
    """Spectral d/dx is exact on band-limited data for EVEN n."""
    out = {}
    for n in (16, 32, 64, 128):
        x = grid(n)
        # highest mode strictly below Nyquist
        kt = n // 2 - 1
        for label, w, dw in [
            ("sin3x", np.sin(3 * x), 3 * np.cos(3 * x)),
            ("const", np.full(n, 4.2), np.zeros(n)),
            ("top", np.sin(kt * x), kt * np.cos(kt * x)),
        ] + (
            # exp(sin x) is entire but not band-limited: its spectrum is only
            # resolved to round-off once n is large enough, so this case is
            # asked at n >= 64 only.
            [("analytic", np.exp(np.sin(x)), np.cos(x) * np.exp(np.sin(x)))]
            if n >= 64 else []
        ):
            scale = max(float(np.max(np.abs(dw))), 1.0)
            err = float(np.max(np.abs(_d(w, n) - dw))) / scale
            out[f"n{n}_{label}"] = err
            assert err < 1e-12, (n, label, err)
    return out


def check_derivative_odd_n_known_defect():
    """KNOWN DEFECT, leg 66 -- PINNED, NOT FIXED.

    `derivative_hat` ends with

        d = 1j * k * w_hat
        if len(w_hat) > 1:
            d[-1] = 0.0

    zeroing the LAST rfft coefficient. For EVEN n that entry is the Nyquist
    mode and zeroing it is the standard, correct treatment of odd derivatives
    of real fields (checked above). For ODD n there IS no Nyquist mode: the
    last entry is k = (n-1)/2, an ordinary, fully resolved wavenumber, and
    zeroing it DESTROYS it. The returned derivative of sin(((n-1)/2) x) is
    identically zero.

    Magnitude: relative sup error 1.000 (the whole mode is lost) on data
    supported at k = (n-1)/2; 7.62e-01 at n = 65 on sin(x) + 0.1*sin(32x).
    On smooth analytic data the top mode is negligible and the error stays at
    round-off (7.3e-15 for exp(sin x) at n = 65), which is why every indirect
    test misses it -- and why it is dangerous: it is invisible until the field
    develops grid-scale content, which is exactly the regime a blow-up study
    runs in.

    Every call site in this repository currently passes an even n, so the
    defect is LATENT, not active. No recorded measurement is affected.

    This test pins the CURRENT (wrong) behaviour and simultaneously records
    the reference the corrected operator must reproduce. When `d[-1] = 0.0`
    is made conditional on n being even, THIS TEST WILL FAIL -- that failure
    is the intended signal to delete the pin and keep `corrected_err`.
    """
    out = {}
    for n in (17, 65, 129):
        x = grid(n)
        kt = (n - 1) // 2  # the highest resolved mode; NOT Nyquist
        w = np.sin(kt * x)
        dw_exact = kt * np.cos(kt * x)
        got = _d(w, n)

        rel = float(np.max(np.abs(got - dw_exact))) / float(np.max(np.abs(dw_exact)))
        out[f"n{n}_current_rel_err"] = rel
        assert rel > 0.99, (n, rel)  # PINNED DEFECT: the mode is destroyed
        out[f"n{n}_returned_max_abs"] = float(np.max(np.abs(got)))
        assert out[f"n{n}_returned_max_abs"] < 1e-9, (n, out)

        # what the operator would give without the unconditional d[-1] = 0
        corrected = np.fft.irfft(1j * wavenumbers(n) * np.fft.rfft(w), n)
        cerr = float(np.max(np.abs(corrected - dw_exact))) / float(np.max(np.abs(dw_exact)))
        out[f"n{n}_corrected_rel_err"] = cerr
        assert cerr < 1e-12, (n, cerr)

    # the mixed-content magnitude quoted in the docstring
    n = 65
    x = grid(n)
    kt = (n - 1) // 2
    w = np.sin(x) + 0.1 * np.sin(kt * x)
    dw_exact = np.cos(x) + 0.1 * kt * np.cos(kt * x)
    out["n65_mixed_rel_err"] = float(
        np.max(np.abs(_d(w, n) - dw_exact))
    ) / float(np.max(np.abs(dw_exact)))
    assert out["n65_mixed_rel_err"] > 0.5, out

    # smooth data is unaffected -- this is the reason no indirect test caught it
    w = np.exp(np.sin(x))
    dw_exact = np.cos(x) * w
    out["n65_smooth_rel_err"] = float(
        np.max(np.abs(_d(w, n) - dw_exact))
    ) / float(np.max(np.abs(dw_exact)))
    assert out["n65_smooth_rel_err"] < 1e-12, out
    return out


# --- integral / l1_norm / energy: hand-computable values -----------------


def check_integral_quantities():
    """Closed-form values on a uniform periodic grid (spectrally exact)."""
    out = {}
    n = 256
    x = grid(n)

    cases = [
        ("integral_const", integral(np.full(n, 3.0)), 3.0 * TWO_PI),
        ("integral_sin", integral(np.sin(x)), 0.0),
        ("integral_1pcos", integral(1.0 + np.cos(x)), TWO_PI),
        # for sign-definite data |f| is smooth and the quadrature is exact
        ("l1_const", l1_norm(np.full(n, -1.5)), 1.5 * TWO_PI),
        ("l1_positive", l1_norm(2.0 + np.sin(x)), 2.0 * TWO_PI),
        # E = (1/2) int sin^2 = pi/2
        ("energy_sin", energy(np.sin(x)), 0.5 * np.pi),
        ("energy_sin3x", energy(np.sin(3 * x)), 0.5 * np.pi),
        ("energy_const", energy(np.full(n, 2.0)), 0.5 * 4.0 * TWO_PI),
        ("energy_zero", energy(np.zeros(n)), 0.0),
    ]
    for label, got, want in cases:
        err = abs(got - want) / max(abs(want), 1.0)
        out[label] = err
        assert err < 1e-10, (label, got, want)

    # For sign-CHANGING data |f| has corners, so the trapezoid rule is only
    # second-order, not spectral. int|sin x| = 4 is therefore approached, not
    # attained; the rate is asserted so the helper's accuracy is on record
    # (this is the number `mean_drift` is normalized by in every run).
    errs = [abs(l1_norm(np.sin(grid(m))) - 4.0) for m in (64, 128, 256, 512)]
    out["l1_sin_err_n256"] = errs[2]
    assert errs[0] < 1e-2, errs
    for lo, hi in zip(errs, errs[1:]):
        out.setdefault("l1_sin_rate_min", 10.0)
        out["l1_sin_rate_min"] = min(out["l1_sin_rate_min"], lo / hi)
    assert out["l1_sin_rate_min"] > 3.5, out  # ~4x per doubling == O(h^2)
    out["l1_2sin_scaling"] = abs(
        l1_norm(2.0 * np.sin(x)) - 2.0 * l1_norm(np.sin(x))
    )
    assert out["l1_2sin_scaling"] < 1e-13, out

    # l1_norm is a norm: homogeneity and the triangle inequality
    rng = np.random.default_rng(7)
    f, g = rng.standard_normal(n), rng.standard_normal(n)
    out["l1_homog"] = abs(l1_norm(-2.5 * f) - 2.5 * l1_norm(f)) / l1_norm(f)
    assert out["l1_homog"] < 1e-13, out
    assert l1_norm(f + g) <= l1_norm(f) + l1_norm(g) + 1e-12
    # energy is quadratic
    out["energy_homog"] = abs(energy(3.0 * f) - 9.0 * energy(f)) / energy(f)
    assert out["energy_homog"] < 1e-13, out
    return out


# --- energy_production: against an INDEPENDENT reference -----------------


def _reference_energy_production(a, nu):
    """dE/dt for w = sin x + sin 2x, computed without touching the module.

    H(sin x + sin 2x) = -cos x - cos 2x and w_x = cos x + 2 cos 2x are written
    out analytically; the two integrals are then taken by the trapezoid rule
    on a 1<<15 grid (spectrally exact for these trigonometric polynomials).
    Formula under test: (a/2 + 1) * int w^2 H(w)  -  nu * int w_x^2.
    """
    m = 1 << 15
    xs = TWO_PI * np.arange(m) / m
    w = np.sin(xs) + np.sin(2 * xs)
    hw = -np.cos(xs) - np.cos(2 * xs)
    wx = np.cos(xs) + 2 * np.cos(2 * xs)
    prod = (a / 2.0 + 1.0) * TWO_PI * float(np.mean(w * w * hw))
    diss = nu * TWO_PI * float(np.mean(wx * wx))
    return prod - diss


def check_energy_production():
    """energy_production matches an analytically-built reference.

    Named by zero existing tests, yet it is one of the two artifact-guard
    numbers every gCLM run logs. The reference above never calls the module,
    so a sign error or a wrong (a/2 + 1) coefficient cannot cancel.
    """
    out = {}
    n = 128
    x = grid(n)
    w = np.sin(x) + np.sin(2 * x)
    for a, nu in [(0.0, 0.0), (1.0, 0.0), (0.0, 0.1), (1.0, 0.05), (-0.5, 0.2)]:
        got = energy_production(w, a, nu)
        want = _reference_energy_production(a, nu)
        err = abs(got - want) / max(abs(want), 1e-12)
        out[f"a{a}_nu{nu}"] = err
        assert err < 1e-10, (a, nu, got, want)

    # the dissipation term alone, on a single mode: -nu * int w_x^2 = -nu*pi*k^2
    for k in (1, 3, 7):
        got = energy_production(np.sin(k * x), a=0.0, nu=0.25)
        want = -0.25 * np.pi * k * k  # int sin^2 * H(sin) = 0 for a single mode
        err = abs(got - want) / abs(want)
        out[f"diss_k{k}"] = err
        assert err < 1e-11, (k, got, want)

    # the a-dependence is exactly affine with slope (1/2) * int w^2 H(w)
    p0 = energy_production(w, a=0.0, nu=0.0)
    p2 = energy_production(w, a=2.0, nu=0.0)
    p1 = energy_production(w, a=1.0, nu=0.0)
    out["a_affine"] = abs((p0 + p2) / 2.0 - p1) / max(abs(p1), 1e-300)
    assert out["a_affine"] < 1e-12, out
    return out


CHECKS = [
    check_grid,
    check_wavenumbers,
    check_dealias_mask,
    check_hilbert_convention,
    check_hilbert_algebra,
    check_velocity_hat,
    check_derivative_even_n,
    check_derivative_odd_n_known_defect,
    check_integral_quantities,
    check_energy_production,
]


def test_grid():
    check_grid()


def test_wavenumbers():
    check_wavenumbers()


def test_dealias_mask():
    check_dealias_mask()


def test_hilbert_convention():
    check_hilbert_convention()


def test_hilbert_algebra():
    check_hilbert_algebra()


def test_velocity_hat():
    check_velocity_hat()


def test_derivative_even_n():
    check_derivative_even_n()


def test_derivative_odd_n_known_defect():
    check_derivative_odd_n_known_defect()


def test_integral_quantities():
    check_integral_quantities()


def test_energy_production():
    check_energy_production()


if __name__ == "__main__":
    for fn in CHECKS:
        metrics = fn()
        head = ", ".join(f"{k}={v:.3g}" if isinstance(v, float) else f"{k}={v}"
                         for k, v in list(metrics.items())[:4])
        print(f"PASS {fn.__name__}: {head}")
    print("\nall spectral_utils dedicated checks passed "
          f"({len(CHECKS)} checks)")
