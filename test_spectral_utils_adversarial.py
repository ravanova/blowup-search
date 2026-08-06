"""Adversarial battery for solver/spectral_utils.py -- the shared numerical core (leg 120,
Route-SUA).

WHY THIS FILE EXISTS, ALONGSIDE `test_spectral_utils_dedicated.py`.  The dedicated file
(leg 66) asks each helper a question it can fail on its own terms: a hand-computed value or an
exact spectral identity, on VALID input.  It found and pinned the odd-n `derivative_hat`
defect, which Leg 0 then fixed on `bench/fix-derivative-hat-odd-n`.  What it does not do -- and
was never meant to do -- is feed the module DEGENERATE OR POISONED input and ask whether the
wrong answer comes back silently.  Leg 120 does that.

THE GATE (DIRECTION.md, leg 120), answered YES:

    Under an adversarial battery of degenerate or poisoned inputs, does
    solver/spectral_utils.py ever silently return a wrong value instead of propagating or
    flagging the invalid input?

READ THIS BEFORE CHANGING ANYTHING HERE.  Several checks below PIN CURRENT, DEFECTIVE
BEHAVIOUR.  That is deliberate, and it is leg 66's own precedent: a leg whose territory is
read-only on `solver/` reports defects and pins them rather than fixing them silently, so the
defect cannot drift unnoticed and so the repair has an exact target.  **Every such check is
marked `PIN:` in its docstring and states what the CORRECT behaviour would be.  When the
repair lands, these checks WILL START FAILING -- that is the intended signal, not a
regression.**  Update the pin then, in the same commit as the repair.

THE SIX FINDINGS PINNED HERE (magnitudes, measured by
experiments/p2_route_sua_v1_adversarial.py, banked in
writeup/data/p2_route_sua_v1_adversarial.json):

  D1  `dealias_mask` keeps `k <= n/3`.  The published alias-free condition is `k < n/3`
      STRICTLY -- Bowman 2013 (`How Important is Dealiasing for Turbulence Simulations?`,
      U. Alberta, p.29): "one needs to pad to N >= 3m - 2 to prevent mode m - 1 from beating
      with itself to contaminate the most negative (first) mode".  With K = m - 1 that is
      N >= 3K + 1, i.e. K < N/3.  When 3 | n the mask retains exactly ONE MODE TOO MANY, and
      that mode beats with itself straight back into the retained band.
      MEASURED: spurious retained coefficient 2.500e-01 against a true value of EXACTLY 0,
      at 11/23 grid sizes tested -- precisely the 11 with 3 | n.  On every n not divisible
      by 3 the same probe gives <= 4.83e-16.

  D2  `energy_production` -- docstring "Exact rate d/dt E for gCLM", and the quantity that
      feeds `solver/gclm.py`'s per-run energy-balance residual (the artifact guard of
      LOGGING.md) -- inherits D1, because it evaluates a CUBIC product on the grid.
      MEASURED: relative error 1.6621e-01 at n = 81 against an alias-free 6x-refined
      evaluation of the same integral, vs 2.47e-14 worst case at every n not divisible by 3.
      12.8 decades of separation.

  D3  `derivative_hat` ERASES a non-finite Nyquist coefficient.  Johnson (MIT, `Notes on
      FFT-based differentiation`) Algorithm 1 step 2 prescribes "multiply Y_k ... by ZERO for
      k = N/2 (if N is even)".  A MULTIPLICATION.  The module ASSIGNS: `d[-1] = 0.0`.  On
      finite input the two are identical; on non-finite input they are not, because
      `0.0 * nan = nan` and `0.0 * inf = nan`.
      MEASURED: 12/12 poisoned Nyquist coefficients (n in {8,16,64,256} x {nan,+inf,-inf})
      returned a FULLY FINITE spectrum and a fully finite physical-space derivative,
      max|w_x| = 1.0 -- indistinguishable from clean input.  For the +-inf cases numpy even
      raised a RuntimeWarning inside the multiply and the assignment then discarded the
      result that warning was about.

  D4  `velocity_hat` erases a non-finite MEAN-mode coefficient: `u_hat = np.zeros_like(w_hat)`
      leaves index 0 at exactly 0 whatever came in.  MEASURED: 3/3 poisons erased.
      (Setting u's mean to zero is the intended convention -- see the module docstring -- so
      the VALUE is right; what is pinned is that a poisoned input becomes undetectable.)

  D5  `velocity_hat` silently TRUNCATES integer input: `zeros_like` inherits the dtype and the
      float quotient is unsafe-cast on assignment.  MEASURED: relative error 1.0000e+00 at
      int scale 1 and 3 (worst of 200 draws).  `derivative_hat` and `hilbert_hat` both promote
      to complex128 on the same input; `velocity_hat` is the only one of the three that does
      not.

  D6  `hilbert_hat` and `derivative_hat` silently BROADCAST a scalar or length-1 `k` into a
      full-length, plausible, wrong answer.  MEASURED: 8/15 malformed-`k` cases accepted with
      no exception, worst relative sup error 2.0000e+00 (`hilbert_hat` with `k = -1.0`, which
      returns the sign-flipped transform).  `velocity_hat` refuses all five.

  D7  Degenerate `n`: `grid(0)` and `grid(-8)` return EMPTY arrays with no error while
      `wavenumbers(0)` / `dealias_mask(0)` raise ZeroDivisionError -- inconsistent behaviour at
      the same invalid input.  `dealias_mask(1)` and `dealias_mask(2)` retain ZERO non-mean
      modes: exactly the condition leg 89 made a hard ValueError in the 2D solver
      (`solver/boussinesq.py:349`); the 1D path has no equivalent guard.

SEVERITY, MEASURED, NOT ASSERTED: **no banked result is affected.**  Every grid size declared
on the `dealias_mask` path in the whole repository is a power of two -- {64, 256, 512, 1024,
2048, 4096, 8192} -- and no power of two is divisible by 3.  All 107 banked
`energy_balance_residual` records (in `p2_route_gla_v1_adversarial.json`, N_SOLVE = 64, and
`p2_route_boa_v1_adversarial.json`, N = 32) are unexposed.  D1/D2 are LATENT, exactly the
severity shape of legs 66, 69 and 79.  Leg 120's pre-committed yes-branch is "escalate, do not
patch", and this leg edits no solver file.

NOT A RE-FIND OF LEG 66/69.  `check_leg69_odd_n_regression` is an explicit control that the
odd-n fix is intact.  It is a PASS, and it is the reason D3 is stated as being about the
ASSIGNMENT form rather than about the Nyquist zeroing, which is correct and published.

Test convention (repo-wide): self-running script, no pytest.
    .venv/bin/python test_spectral_utils_adversarial.py
"""

import warnings

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

SEED = 20260806
POISONS = (("nan", np.nan), ("+inf", np.inf), ("-inf", -np.inf))

# The grid sizes the repository actually runs on the dealias path (all powers of two),
# and the marginal 3 | n sizes that Bowman's strict inequality separates from them.
GRIDS_DIV3 = (6, 9, 12, 24, 27, 48, 81, 96, 192, 384, 768)
GRIDS_NOT_DIV3 = (10, 16, 20, 32, 40, 50, 64, 100, 128, 200, 256, 512)


# =========================================================================
# D1 -- the dealias boundary
# =========================================================================

def check_dealias_alias_free_guarantee():
    """PIN (D1): the 2/3 rule's GUARANTEE, not its docstring.

    `test_spectral_utils_dedicated.py::check_dealias_mask` asserts that the mask keeps
    `k <= n/3` and, at line 121, that `dealias_mask(96)[32]` is True ("k = n/3 must be
    retained (<=, not <)").  That check is self-consistent: it verifies the mask matches its
    own stated cut.  It cannot catch this defect, because the defect IS the stated cut.

    This check asks the different question: does the retained band actually deliver the
    property the 2/3 rule exists to provide -- that a quadratic product of retained modes
    contributes NOTHING spurious back inside the band?

    Bowman's experiment, verbatim in structure: put the field on the top retained mode K,
    square it, read mode K back.  The true coefficient there is exactly 0.

    CORRECT BEHAVIOUR: alias-free at every n, i.e. the mask should keep `k < n/3` strictly
    (equivalently `k <= (n - 1) // 3`).  The values below pin the CURRENT behaviour.
    """
    out = {}

    # (a) every n NOT divisible by 3: alias-free, and this must never regress.
    worst_clean = 0.0
    for n in GRIDS_NOT_DIV3:
        spurious = _self_beat_coefficient(n)
        worst_clean = max(worst_clean, spurious)
        assert spurious < 1e-12, (n, spurious)
    out["worst_spurious_not_div3"] = worst_clean
    assert worst_clean < 1e-12, out

    # (b) every n divisible by 3: CONTAMINATED, at amplitude exactly 1/4.  PINNED.
    for n in GRIDS_DIV3:
        spurious = _self_beat_coefficient(n)
        assert abs(spurious - 0.25) < 1e-12, (
            f"PIN D1 at n={n}: expected the pinned defect amplitude 0.25, got {spurious}. "
            "If a repair to dealias_mask has landed (keeping k < n/3 strictly), this "
            "assertion SHOULD fail -- update the pin in the same commit as the repair."
        )
    out["spurious_div3"] = 0.25
    out["n_contaminated"] = len(GRIDS_DIV3)

    # (c) the defect is EXACTLY the boundary case, nothing else.
    for n in GRIDS_DIV3 + GRIDS_NOT_DIV3:
        k = wavenumbers(n)
        K = int(np.max(k[dealias_mask(n)]))
        bowman_ok = K < n / 3.0            # N >= 3K + 1
        assert bowman_ok == (n % 3 != 0), (n, K, bowman_ok)
    out["defect_iff_3_divides_n"] = True
    return out


def _self_beat_coefficient(n):
    """|coefficient at the top retained mode K after squaring a field placed on K|."""
    k = wavenumbers(n)
    m = dealias_mask(n)
    K = int(np.max(k[m]))
    w = np.fft.irfft(np.fft.rfft(np.cos(K * grid(n))) * m, n)
    prod = np.fft.rfft(w * w) * m / n
    return float(np.abs(prod[K]))


# =========================================================================
# D2 -- the consequence in a shipped diagnostic
# =========================================================================

def _band_field(n, seed=SEED):
    rng = np.random.default_rng(seed)
    m = dealias_mask(n)
    wh = (rng.standard_normal(m.shape) + 1j * rng.standard_normal(m.shape)) * m
    wh[0] = wh[0].real
    w = np.fft.irfft(wh, n)
    return np.fft.irfft(np.fft.rfft(w) * m, n)


def _alias_free_production(w, n, a, nu, f=6):
    """The same integral energy_production computes, on an f-times finer grid where the
    cubic product is fully resolved -- so it carries no aliasing."""
    nf = f * n
    wh = np.fft.rfft(w)
    whf = np.zeros(nf // 2 + 1, dtype=complex)
    whf[:len(wh)] = wh * (nf / n)
    wf = np.fft.irfft(whf, nf)
    kf = wavenumbers(nf)
    hwf = np.fft.irfft(hilbert_hat(np.fft.rfft(wf), kf), nf)
    wxf = np.fft.irfft(derivative_hat(np.fft.rfft(wf), kf, nf), nf)
    return ((a / 2.0 + 1.0) * TWO_PI * float(np.mean(wf * wf * hwf))
            - nu * TWO_PI * float(np.mean(wxf * wxf)))


def check_energy_production_aliasing():
    """PIN (D2): `energy_production` is documented as the "Exact rate d/dt E".  It is exact
    to round-off when 3 does not divide n, and carries a percent-level alias error when it
    does -- because it evaluates a CUBIC product on the grid, and D1's retained band admits
    the triad K + K + K = n.

    This is the finding's teeth: D1 alone is a property of a mask, which a reader could
    dismiss as a convention. D2 is a wrong number in a quantity `solver/gclm.py` logs as an
    artifact guard on every run.

    CORRECT BEHAVIOUR: round-off at every n.  The n-not-divisible-by-3 bound is a real
    assertion; the divisible-by-3 floor pins the defect.
    """
    out = {}

    # (a) exact where the band is alias-free -- a genuine correctness assertion.
    worst_clean = 0.0
    for n in (16, 32, 64, 128, 256, 512):
        w = _band_field(n)
        got = energy_production(w, a=0.0, nu=0.0)
        ref = _alias_free_production(w, n, a=0.0, nu=0.0)
        rel = abs(got - ref) / max(abs(ref), 1e-300)
        worst_clean = max(worst_clean, rel)
        assert rel < 1e-10, (n, rel)
    out["worst_rel_err_not_div3"] = worst_clean

    # (b) contaminated where it is not.  PINNED, with the measured headline.
    worst_bad, worst_n = 0.0, None
    for n in (12, 24, 27, 48, 81, 96, 192, 384, 768):
        w = _band_field(n)
        got = energy_production(w, a=0.0, nu=0.0)
        ref = _alias_free_production(w, n, a=0.0, nu=0.0)
        rel = abs(got - ref) / max(abs(ref), 1e-300)
        if rel > worst_bad:
            worst_bad, worst_n = rel, n
    out["worst_rel_err_div3"] = worst_bad
    out["worst_n_div3"] = worst_n
    assert worst_bad > 1e-3, (
        f"PIN D2: expected the pinned alias error (measured 1.6621e-01 at n=81), got "
        f"{worst_bad:.4e} at n={worst_n}. If dealias_mask has been repaired this assertion "
        "SHOULD fail -- update the pin in the same commit as the repair."
    )
    assert worst_bad / max(worst_clean, 1e-300) > 1e6, out
    return out


# =========================================================================
# D3 -- Nyquist poison erasure
# =========================================================================

def check_nyquist_poison_erased():
    """PIN (D3): a non-finite Nyquist coefficient does not survive `derivative_hat`.

    Johnson Algorithm 1 says MULTIPLY that coefficient by zero; the module ASSIGNS
    `d[-1] = 0.0`.  `0.0 * nan = nan`, so the published form propagates and the assignment
    erases.  The correct fix is one character of intent -- multiply instead of assign, or
    check for non-finite input -- and it is NOT applied here (territory is read-only).

    CORRECT BEHAVIOUR: poison in, poison out.  Pinned as: poison in, clean number out.
    """
    out = {"erased": 0, "cases": 0}
    for n in (8, 16, 64, 256):
        k = wavenumbers(n)
        for tag, p in POISONS:
            wh = np.fft.rfft(np.sin(grid(n)))
            wh[-1] = p
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                with np.errstate(all="ignore"):
                    d = derivative_hat(wh.copy(), k, n)
                    phys = np.fft.irfft(d, n)
            out["cases"] += 1
            if np.all(np.isfinite(d)):
                out["erased"] += 1
            assert np.all(np.isfinite(d)), (
                f"PIN D3 at n={n}, poison={tag}: the poisoned Nyquist coefficient "
                "PROPAGATED. If derivative_hat has been repaired this assertion SHOULD "
                "fail -- update the pin in the same commit as the repair."
            )
            assert np.all(np.isfinite(phys)), (n, tag)
            # and the result is bit-indistinguishable from the clean input
            assert abs(float(np.max(np.abs(phys))) - 1.0) < 1e-9, (n, tag)
    assert out["erased"] == out["cases"] == 12, out
    return out


def check_non_nyquist_poison_propagates():
    """CONTROL for D3 (a PASS): poison anywhere OTHER than the Nyquist slot propagates.

    This is what makes D3 a statement about one line rather than about the module's NaN
    handling generally.
    """
    out = {"propagated": 0, "cases": 0}
    for n in (64, 256):
        k = wavenumbers(n)
        for slot in (1, 5, 17):
            for tag, p in POISONS:
                wh = np.fft.rfft(np.sin(grid(n)))
                wh[slot] = p
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    with np.errstate(all="ignore"):
                        d = derivative_hat(wh.copy(), k, n)
                out["cases"] += 1
                assert not np.all(np.isfinite(d)), (n, slot, tag)
                out["propagated"] += 1
    assert out["propagated"] == out["cases"], out
    return out


def check_leg69_odd_n_regression():
    """CONTROL (a PASS, and NOT a new finding): leg 66's odd-n defect stays fixed.

    Leg 66 measured relative sup error 1.000 on data at k = (n-1)/2 for odd n; Leg 0 fixed it
    on `bench/fix-derivative-hat-odd-n`.  Two things are checked: the derivative is exact at
    the top mode of an odd grid, and a poison there PROPAGATES (there is no Nyquist slot to
    erase it, so D3 cannot reach odd n).
    """
    out = {}
    for n in (17, 65, 129):
        k = wavenumbers(n)
        kt = (n - 1) // 2
        x = grid(n)
        w = np.sin(kt * x)
        dw = np.fft.irfft(derivative_hat(np.fft.rfft(w), k, n), n)
        ex = kt * np.cos(kt * x)
        rel = float(np.max(np.abs(dw - ex)) / np.max(np.abs(ex)))
        out[f"n{n}_top_mode_rel_err"] = rel
        assert rel < 1e-12, (n, rel)      # was 1.000 before leg 0's fix

        wh = np.fft.rfft(w)
        wh[-1] = np.nan
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with np.errstate(all="ignore"):
                d = derivative_hat(wh.copy(), k, n)
        assert not np.all(np.isfinite(d)), (n, "odd-n top-mode poison must propagate")
    return out


# =========================================================================
# D4 / D5 -- velocity_hat
# =========================================================================

def check_velocity_hat_mean_mode_erased():
    """PIN (D4): a poisoned mean-mode coefficient becomes exactly 0, undetectably.

    The VALUE is the intended convention (u is chosen zero-mean; see the module docstring),
    so this is not a wrong velocity.  What is pinned is that `w_hat[0] = nan` -- a signal
    that the caller's field is corrupt -- is destroyed rather than passed on.
    """
    n = 64
    k = wavenumbers(n)
    out = {"erased": 0, "cases": 0}
    for tag, p in POISONS:
        wh = np.fft.rfft(np.sin(grid(n)))
        wh[0] = p
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with np.errstate(all="ignore"):
                u = velocity_hat(wh.copy(), k)
        out["cases"] += 1
        assert u[0] == 0, (tag, u[0])
        assert np.all(np.isfinite(u)), (tag,)
        out["erased"] += 1
    assert out["erased"] == 3, out
    return out


def check_velocity_hat_dtype_truncation():
    """PIN (D5): integer input is silently truncated, and only in this one function.

    `u_hat = np.zeros_like(w_hat)` inherits the input dtype; the float quotient
    `-w_hat[nz] / |k[nz]|` is then unsafe-cast on assignment.  `derivative_hat` and
    `hilbert_hat` both promote to complex128 on the same input.

    CORRECT BEHAVIOUR: promote (or refuse).  Pinned as: truncate.
    """
    out = {}
    kk = np.arange(33.0)
    assert np.asarray(velocity_hat(np.zeros(33, dtype=np.int64), kk)).dtype == np.int64
    assert np.asarray(derivative_hat(np.zeros(4, dtype=np.int64),
                                     np.arange(4.0), 6)).dtype == np.complex128
    assert np.asarray(hilbert_hat(np.zeros(4, dtype=np.int64),
                                  np.arange(4.0))).dtype == np.complex128
    out["velocity_hat_inherits_int64"] = True

    rng = np.random.default_rng(SEED)
    worst = 0.0
    for scale in (1, 3, 10):
        for _ in range(200):
            a = (rng.standard_normal(33) * scale).astype(np.int64)
            a[0] = 0
            u = velocity_hat(a.copy(), kk)
            ex = np.zeros(33)
            ex[1:] = -a[1:] / kk[1:]
            rel = (float(np.max(np.abs(np.asarray(u, dtype=np.float64) - ex)))
                   / max(float(np.max(np.abs(ex))), 1e-300))
            worst = max(worst, rel)
    out["worst_rel_err"] = worst
    assert worst > 0.5, (
        f"PIN D5: expected the pinned truncation (measured rel err 1.0), got {worst:.4e}. "
        "If velocity_hat has been repaired this assertion SHOULD fail."
    )
    return out


# =========================================================================
# D6 -- malformed k
# =========================================================================

def check_malformed_k_broadcast():
    """PIN (D6): a scalar or length-1 `k` is broadcast into a full-length wrong answer.

    `derivative_hat` validates `len(w_hat)` against `n` but never validates `k`; `hilbert_hat`
    validates nothing.  `velocity_hat` refuses all five malformed cases (it indexes `k`), so
    the module is INTERNALLY INCONSISTENT about the same caller error.

    CORRECT BEHAVIOUR: refuse, as velocity_hat does.  Pinned as: 8/15 accepted.
    """
    n = 64
    x = grid(n)
    wh = np.fft.rfft(np.sin(3 * x) + 0.4 * np.sin(11 * x))
    k_ok = wavenumbers(n)
    h_ok = np.fft.irfft(hilbert_hat(wh.copy(), k_ok), n)
    out = {}

    # hilbert_hat with a scalar k: silently returns a full-length wrong transform
    h_zero = np.fft.irfft(hilbert_hat(wh.copy(), 0.0), n)
    assert np.all(h_zero == 0), "scalar k=0 should annihilate the whole transform"
    out["scalar_k0_rel_err"] = float(np.max(np.abs(h_zero - h_ok))
                                     / np.max(np.abs(h_ok)))
    h_neg = np.fft.irfft(hilbert_hat(wh.copy(), -1.0), n)
    out["scalar_kneg_rel_err"] = float(np.max(np.abs(h_neg - h_ok))
                                       / np.max(np.abs(h_ok)))
    assert out["scalar_k0_rel_err"] > 0.9, out
    assert out["scalar_kneg_rel_err"] > 1.9, out      # sign-flipped transform

    # derivative_hat with a scalar k: accepted, no exception
    d_bad = derivative_hat(wh.copy(), 1.0, n)
    assert d_bad.shape == wh.shape, d_bad.shape
    out["derivative_hat_accepts_scalar_k"] = True

    # velocity_hat refuses the same inputs -- the inconsistency, asserted
    for bad in (0.0, 1.0, -1.0):
        try:
            velocity_hat(wh.copy(), bad)
            raise AssertionError("velocity_hat should refuse a scalar k")
        except TypeError:
            pass
    try:
        velocity_hat(wh.copy(), np.array([2.0]))
        raise AssertionError("velocity_hat should refuse a length-1 k")
    except IndexError:
        pass
    out["velocity_hat_refuses_all_five"] = True

    # wrong-length k IS caught, by all three
    for fn in (lambda: hilbert_hat(wh.copy(), wavenumbers(32)),
               lambda: derivative_hat(wh.copy(), wavenumbers(32), n)):
        try:
            fn()
            raise AssertionError("wrong-length k should raise")
        except ValueError:
            pass
    return out


# =========================================================================
# D7 -- degenerate n
# =========================================================================

def check_degenerate_n():
    """PIN (D7): inconsistent behaviour at the same invalid `n`, and no 1D guard for the
    grid sizes leg 89 rejected in 2D.

    CORRECT BEHAVIOUR: one consistent refusal.  `solver/boussinesq.py:349` shows the shape
    it should take -- leg 89 made "the mask retains only the mean mode" a hard ValueError.
    """
    out = {}
    # grid() accepts nonsense silently; wavenumbers()/dealias_mask() raise on n = 0
    for n in (0, -1, -8):
        assert grid(n).size == 0, n
    out["grid_silent_on_nonpositive"] = True
    for fn in (wavenumbers, dealias_mask):
        try:
            fn(0)
            raise AssertionError("expected ZeroDivisionError at n = 0")
        except ZeroDivisionError:
            pass
    out["wavenumbers_raises_at_zero"] = True
    # negative n: no error anywhere, empty arrays everywhere
    for n in (-1, -8):
        assert wavenumbers(n).size == 0 and dealias_mask(n).size == 0, n
    out["negative_n_silent"] = True

    # n = 1, 2: the mask retains ZERO non-mean modes -- leg 89's 2D ValueError condition
    for n in (1, 2):
        m = dealias_mask(n)
        k = wavenumbers(n)
        assert int(np.sum(m & (k > 0))) == 0, n
    out["zero_non_mean_modes_at"] = [1, 2]
    assert int(np.sum(dealias_mask(3) & (wavenumbers(3) > 0))) == 1
    return out


# =========================================================================
# THE PASSES -- recorded as loudly as the failures
# =========================================================================

def check_integral_quantities_propagate():
    """PASS: `integral`, `l1_norm` and `energy` NEVER absorb poison.

    Every non-finite input yields a non-finite output; the empty grid yields nan and warns.
    Nothing here is a defect, and recording that is the point: the deliverable is a map of
    the module's behaviour, not a bug list.
    """
    n = 64
    base = np.sin(grid(n))
    out = {"absorbed": 0}
    poisoned = [
        ("one nan", np.where(np.arange(n) == 7, np.nan, base)),
        ("one +inf", np.where(np.arange(n) == 7, np.inf, base)),
        ("one -inf", np.where(np.arange(n) == 7, -np.inf, base)),
        ("all nan", np.full(n, np.nan)),
    ]
    for tag, f in poisoned:
        with np.errstate(all="ignore"):
            vals = (integral(f), l1_norm(f), energy(f))
        assert not all(np.isfinite(v) for v in vals), (tag, vals)
        if all(np.isfinite(v) for v in vals):
            out["absorbed"] += 1
    assert out["absorbed"] == 0, out

    # the empty grid: nan, and it warns rather than inventing a value
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        with np.errstate(all="ignore"):
            e = (integral(np.zeros(0)), l1_norm(np.zeros(0)), energy(np.zeros(0)))
    assert all(np.isnan(v) for v in e), e
    out["empty_warns"] = len(wl) > 0
    assert out["empty_warns"], "empty input should at least warn"

    # exact conventions, unchanged (energy of sin is pi/2, not pi)
    x = grid(n)
    assert abs(energy(np.sin(x)) - np.pi / 2.0) < 1e-12
    assert abs(integral(np.ones(n)) - TWO_PI) < 1e-12
    return out


def check_length_guard_exact():
    """PASS: `derivative_hat`'s length guard (added with leg 0's odd-n fix) fires on exactly
    the wrong-length coefficient arrays -- not one more, not one fewer."""
    out = {"cases": 0}
    for n, m in ((64, 33), (64, 32), (64, 34), (17, 9), (17, 8), (17, 10), (8, 5), (9, 5)):
        wh = np.zeros(m, dtype=complex)
        k = np.arange(float(m))
        correct = (m == n // 2 + 1)
        try:
            derivative_hat(wh, k, n)
            accepted = True
        except ValueError:
            accepted = False
        out["cases"] += 1
        assert accepted == correct, (n, m, correct, accepted)
    return out


CHECKS = [
    check_dealias_alias_free_guarantee,
    check_energy_production_aliasing,
    check_nyquist_poison_erased,
    check_non_nyquist_poison_propagates,
    check_leg69_odd_n_regression,
    check_velocity_hat_mean_mode_erased,
    check_velocity_hat_dtype_truncation,
    check_malformed_k_broadcast,
    check_degenerate_n,
    check_integral_quantities_propagate,
    check_length_guard_exact,
]


def test_dealias_alias_free_guarantee():
    check_dealias_alias_free_guarantee()


def test_energy_production_aliasing():
    check_energy_production_aliasing()


def test_nyquist_poison_erased():
    check_nyquist_poison_erased()


def test_non_nyquist_poison_propagates():
    check_non_nyquist_poison_propagates()


def test_leg69_odd_n_regression():
    check_leg69_odd_n_regression()


def test_velocity_hat_mean_mode_erased():
    check_velocity_hat_mean_mode_erased()


def test_velocity_hat_dtype_truncation():
    check_velocity_hat_dtype_truncation()


def test_malformed_k_broadcast():
    check_malformed_k_broadcast()


def test_degenerate_n():
    check_degenerate_n()


def test_integral_quantities_propagate():
    check_integral_quantities_propagate()


def test_length_guard_exact():
    check_length_guard_exact()


if __name__ == "__main__":
    for fn in CHECKS:
        metrics = fn()
        head = ", ".join(f"{k}={v:.3g}" if isinstance(v, float) else f"{k}={v}"
                         for k, v in list(metrics.items())[:4])
        print(f"PASS {fn.__name__}: {head}")
    print(f"\nall spectral_utils ADVERSARIAL checks passed ({len(CHECKS)} checks)")
    print("NOTE: 7 of these PIN CURRENT DEFECTIVE BEHAVIOUR (D1-D7, see module docstring).")
    print("They are expected to FAIL once solver/spectral_utils.py is repaired -- that is")
    print("the intended signal. Banked magnitudes: writeup/data/p2_route_sua_v1_adversarial.json")
