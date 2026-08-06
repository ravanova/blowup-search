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

**THE REPAIR LANDED (leg 129, Route-SUR), AND ALL SEVEN PINS ARE NOW INVERTED.**  Leg 120 was
read-only on `solver/` and pinned seven defects rather than fixing them, each marked `PIN:`
with the correct behaviour stated beside it, so that the repair would have an exact target and
the defects could not drift.  Leg 129 made the repair and, in the same commit, turned every
pin around: each check below now asserts the CORRECT behaviour and would fail if the defect
returned.  **This file is therefore no longer a defect ledger -- it is the permanent regression
suite for the repair**, which is what leg 120's yes-branch prescribed.  The pinned magnitudes
are retained verbatim in the docstrings as the BEFORE column, because a regression suite that
has forgotten what it is defending against cannot report a magnitude when it fires.

The repair itself, in one line each: `dealias_mask` and `dealias_mask2d` cut at
`k <= (n-1)//3` (strictly below n/3); `derivative_hat` MULTIPLIES the Nyquist entry by zero
rather than assigning it; `velocity_hat` builds a complex128 output and multiplies the mean
mode by zero; `hilbert_hat`/`derivative_hat`/`velocity_hat` all validate `k` with the same
`ValueError`; `grid`/`wavenumbers`/`dealias_mask` refuse a degenerate `n` with the same
`ValueError`.  Every one is a measured no-op on finite input at every grid size this repository
has ever run -- 0 of 156 power-of-two and banked quantities moved in leg 129's bitwise A/B
against the pre-repair module, including three end-to-end gCLM runs at n = 64 and a Boussinesq
run at n = 32 (writeup/data/p2_route_sur_v1_repair.json).

THE SEVEN FINDINGS, AS MEASURED BEFORE THE REPAIR (magnitudes, measured by
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

SEVERITY, MEASURED, NOT ASSERTED: **no banked result was ever affected.**  Every grid size
declared on the `dealias_mask` path in the whole repository is a power of two -- {64, 256, 512,
1024, 2048, 4096, 8192}, plus the 2D n = 32 -- and no power of two is divisible by 3.  Leg 120
counted 107 banked `energy_balance_residual` records and found 0 exposed; leg 129 re-ran that
census after legs 103 and 133 banked their own post-repair data and found **129** records in
four files, still **0** exposed.  D1/D2 were LATENT -- exactly the severity shape of legs 66,
69 and 79 -- and the repair closed them before any run picked a round grid number.

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
    """REGRESSION (D1, repaired by leg 129): the 2/3 rule's GUARANTEE, not its docstring.

    `test_spectral_utils_dedicated.py::check_dealias_mask` asserts that the mask keeps
    `k <= n/3` and, at line 121, that `dealias_mask(96)[32]` is True ("k = n/3 must be
    retained (<=, not <)").  That check is self-consistent: it verifies the mask matches its
    own stated cut.  It cannot catch this defect, because the defect IS the stated cut.

    This check asks the different question: does the retained band actually deliver the
    property the 2/3 rule exists to provide -- that a quadratic product of retained modes
    contributes NOTHING spurious back inside the band?

    Bowman's experiment, verbatim in structure: put the field on the top retained mode K,
    square it, read mode K back.  The true coefficient there is exactly 0.

    REQUIRED BEHAVIOUR, now asserted at every n: alias-free everywhere, i.e. the mask keeps
    `k < n/3` strictly (equivalently `k <= (n - 1) // 3`).

    BEFORE the repair: spurious coefficient exactly 2.500e-01 at all 11 grids with 3 | n,
    against <= 4.83e-16 at all 12 without.  AFTER: <= 1.142e-15 at all 23.
    """
    out = {}

    # (a) every n NOT divisible by 3: alias-free, and this must never regress.
    # These grids were ALWAYS correct -- this half of the check is unchanged by the repair,
    # and it is what proves the repair did not simply move the defect somewhere else.
    worst_clean = 0.0
    for n in GRIDS_NOT_DIV3:
        spurious = _self_beat_coefficient(n)
        worst_clean = max(worst_clean, spurious)
        assert spurious < 1e-12, (n, spurious)
    out["worst_spurious_not_div3"] = worst_clean
    assert worst_clean < 1e-12, out

    # (b) every n divisible by 3: NOW ALSO ALIAS-FREE.  This is the inverted pin -- it
    # asserted `abs(spurious - 0.25) < 1e-12` before leg 129's repair.
    worst_div3 = 0.0
    for n in GRIDS_DIV3:
        spurious = _self_beat_coefficient(n)
        worst_div3 = max(worst_div3, spurious)
        assert spurious < 1e-12, (
            f"D1 REGRESSED at n={n}: spurious self-beat coefficient {spurious:.4e}, "
            "expected round-off. The 2/3 cut has gone back to `k <= n/3`; it must be "
            "`k <= (n - 1) // 3` (Bowman 2013: N >= 3K + 1). Pre-repair value was 0.25."
        )
    out["worst_spurious_div3"] = worst_div3
    out["n_contaminated"] = 0
    out["pre_repair_spurious_div3"] = 0.25

    # (c) Bowman's inequality now holds at EVERY n, not just where 3 does not divide it.
    for n in GRIDS_DIV3 + GRIDS_NOT_DIV3:
        k = wavenumbers(n)
        K = int(np.max(k[dealias_mask(n)]))
        assert K < n / 3.0, (                 # N >= 3K + 1, everywhere
            f"D1 REGRESSED at n={n}: top retained mode {K} violates K < n/3 = {n / 3.0}"
        )
        # and it is the LARGEST admissible one -- the repair must not over-truncate,
        # which would be a silent resolution loss rather than a fix.
        assert K + 1 >= n / 3.0, (n, K, "mask truncates more than the 2/3 rule requires")
    out["bowman_holds_at_all_n"] = True
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
    """REGRESSION (D2, repaired by leg 129): `energy_production` is documented as the "Exact
    rate d/dt E", and it is now exact to round-off at EVERY n.

    Before the repair it carried a percent-level alias error whenever 3 divided n, because it
    evaluates a CUBIC product on the grid and D1's over-wide retained band admitted the triad
    K + K + K = n.  This was the finding's teeth: D1 alone is a property of a mask, which a
    reader could dismiss as a convention; D2 was a wrong number in a quantity
    `solver/gclm.py` logs as an artifact guard on every run.

    BEFORE: relative error 1.6621e-01 at n = 81 (worst of nine 3 | n grids), vs 2.47e-14 at
    every n not divisible by 3.  AFTER: 1.4543e-15 worst over the same nine grids -- a gain
    of 14.1 decades, measured in writeup/data/p2_route_sur_v1_repair.json.
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

    # (b) NOW EXACT where it used to be contaminated.  This is the inverted pin -- it
    # asserted `worst_bad > 1e-3` before leg 129's repair.
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
    out["pre_repair_worst_rel_err_div3"] = 0.16621
    assert worst_bad < 1e-10, (
        f"D2 REGRESSED: relative alias error {worst_bad:.4e} at n={worst_n}, expected "
        "round-off. energy_production is documented as the EXACT rate and is logged as an "
        "artifact guard on every run. Pre-repair value was 1.6621e-01 at n=81."
    )
    # and the two columns are now the same order of magnitude -- there is no longer a
    # 3 | n class at all, which is the whole point of the repair.
    assert worst_bad / max(worst_clean, 1e-300) < 1e3, out
    return out


# =========================================================================
# D3 -- Nyquist poison erasure
# =========================================================================

def check_nyquist_poison_propagates():
    """REGRESSION (D3, repaired by leg 129): a non-finite Nyquist coefficient now SURVIVES
    `derivative_hat` instead of being erased.

    Johnson Algorithm 1 says MULTIPLY that coefficient by zero; the module used to ASSIGN
    `d[-1] = 0.0`.  `0.0 * nan = nan`, so the published form propagates and the assignment
    erased.  Leg 129 switched to `d[-1] = d[-1] * 0.0 + 0.0j`, which is Johnson's form with
    the signed zero normalized so that finite input still gives exactly 0+0j.

    BEFORE: 12/12 poisons erased, every one returning a fully finite spectrum with
    max|w_x| = 1.0000, indistinguishable from clean input.  AFTER: 12/12 propagate.
    """
    out = {"propagated": 0, "cases": 0}
    for n in (8, 16, 64, 256):
        k = wavenumbers(n)
        for tag, p in POISONS:
            wh = np.fft.rfft(np.sin(grid(n)))
            wh[-1] = p
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                with np.errstate(all="ignore"):
                    d = derivative_hat(wh.copy(), k, n)
            out["cases"] += 1
            if not np.all(np.isfinite(d)):
                out["propagated"] += 1
            assert not np.all(np.isfinite(d)), (
                f"D3 REGRESSED at n={n}, poison={tag}: the poisoned Nyquist coefficient was "
                "ERASED and the caller got a clean, wrong, fully finite derivative. "
                "derivative_hat must MULTIPLY the Nyquist entry by zero, not assign it "
                "(Johnson, Notes on FFT-based differentiation, Algorithm 1 step 2)."
            )
    assert out["propagated"] == out["cases"] == 12, out

    # THE NO-OP HALF, and it is the reason this repair was allowed to land: on FINITE input
    # the Nyquist coefficient is still EXACTLY +0.0 + 0.0j -- not -0.0, not 1e-17. If this
    # fails, the repair has changed a value on well-formed input, which it must never do.
    for n in (8, 16, 64, 256):
        k = wavenumbers(n)
        wh = np.fft.rfft(np.sin(grid(n)) + 0.5 * np.cos(3 * grid(n)))
        b = derivative_hat(wh.copy(), k, n)[-1]
        assert b == 0 and not np.signbit(b.real) and not np.signbit(b.imag), (n, b)
    out["exact_zero_on_finite_input"] = True
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

def check_velocity_hat_mean_mode_propagates():
    """REGRESSION (D4, repaired by leg 129): a poisoned mean-mode coefficient now propagates.

    The VALUE was always the intended convention (u is chosen zero-mean; see the module
    docstring), so this was never a wrong velocity.  What was pinned is that `w_hat[0] = nan`
    -- a signal that the caller's field is corrupt -- was destroyed rather than passed on,
    because `np.zeros_like` left index 0 at a fresh zero whatever came in.  Leg 129 multiplies
    the mean mode by zero instead, so the convention is unchanged on finite input and the
    corruption signal survives.

    BEFORE: 3/3 poisons erased.  AFTER: 3/3 propagate, and finite input still gives +0.0.
    """
    n = 64
    k = wavenumbers(n)
    out = {"propagated": 0, "cases": 0}
    for tag, p in POISONS:
        wh = np.fft.rfft(np.sin(grid(n)))
        wh[0] = p
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with np.errstate(all="ignore"):
                u = velocity_hat(wh.copy(), k)
        out["cases"] += 1
        assert not np.all(np.isfinite(u)), (
            f"D4 REGRESSED, poison={tag}: a non-finite mean mode was erased into a clean 0 "
            "and the caller cannot tell its field was corrupt."
        )
        out["propagated"] += 1
    assert out["propagated"] == 3, out

    # THE NO-OP HALF: the zero-mean convention is untouched on well-formed input, and the
    # mean mode is exactly +0.0 + 0.0j -- a multiplication can produce -0.0, so this is
    # checked bitwise rather than with `== 0`.
    u = velocity_hat(np.fft.rfft(np.sin(grid(n)) + 2.5), k)
    assert u[0] == 0 and not np.signbit(u[0].real) and not np.signbit(u[0].imag), u[0]
    out["mean_mode_exactly_plus_zero"] = True
    return out


def check_velocity_hat_dtype_promotes():
    """REGRESSION (D5, repaired by leg 129): integer input is no longer silently truncated.

    `u_hat = np.zeros_like(w_hat)` used to inherit the input dtype, and the float quotient
    `-w_hat[nz] / |k[nz]|` was then unsafe-cast on assignment.  `derivative_hat` and
    `hilbert_hat` both promote to complex128 on the same input; `velocity_hat` was the only
    one of the three that did not.  Leg 129 allocates complex128 explicitly.

    BEFORE: dtype int64, worst relative error 1.0000e+00 over 600 draws.  AFTER: complex128,
    worst relative error 0.0.
    """
    out = {}
    kk = np.arange(33.0)
    assert np.asarray(velocity_hat(np.zeros(33, dtype=np.int64), kk)).dtype == np.complex128
    assert np.asarray(derivative_hat(np.zeros(4, dtype=np.int64),
                                     np.arange(4.0), 6)).dtype == np.complex128
    assert np.asarray(hilbert_hat(np.zeros(4, dtype=np.int64),
                                  np.arange(4.0))).dtype == np.complex128
    out["all_three_promote"] = True

    rng = np.random.default_rng(SEED)
    worst = 0.0
    for scale in (1, 3, 10):
        for _ in range(200):
            a = (rng.standard_normal(33) * scale).astype(np.int64)
            a[0] = 0
            u = velocity_hat(a.copy(), kk)
            ex = np.zeros(33)
            ex[1:] = -a[1:] / kk[1:]
            rel = (float(np.max(np.abs(np.asarray(u).real - ex)))
                   / max(float(np.max(np.abs(ex))), 1e-300))
            worst = max(worst, rel)
    out["worst_rel_err"] = worst
    out["pre_repair_worst_rel_err"] = 1.0
    assert worst == 0.0, (
        f"D5 REGRESSED: velocity_hat truncated integer input, worst relative error "
        f"{worst:.4e} over 600 draws (pre-repair value was exactly 1.0)."
    )
    return out


# =========================================================================
# D6 -- malformed k
# =========================================================================

def check_malformed_k_refused():
    """REGRESSION (D6, repaired by leg 129): a malformed `k` is refused by all three
    functions, with the same exception type.

    `derivative_hat` used to validate `len(w_hat)` against `n` but never `k`, and
    `hilbert_hat` validated nothing, so a scalar or length-1 `k` BROADCAST into a
    full-length, plausible, wrong answer.  `velocity_hat` refused the same inputs only by
    accident of indexing `k`, and raised TypeError or IndexError depending on which -- so the
    module gave three different behaviours for one caller error.

    BEFORE: 8/15 malformed cases accepted silently, worst relative sup error 2.0000e+00
    (`hilbert_hat` with k = -1.0 returns the sign-flipped transform); refusals came as
    TypeError, IndexError or ValueError.  AFTER: 15/15 refused, all ValueError.
    """
    n = 64
    x = grid(n)
    wh = np.fft.rfft(np.sin(3 * x) + 0.4 * np.sin(11 * x))
    out = {"refused": 0, "cases": 0}

    malformed = (0.0, 1.0, -1.0, np.array([2.0]), wavenumbers(32))
    for bad in malformed:
        for fn, args in ((hilbert_hat, (wh.copy(), bad)),
                         (velocity_hat, (wh.copy(), bad)),
                         (derivative_hat, (wh.copy(), bad, n))):
            out["cases"] += 1
            try:
                fn(*args)
            except ValueError:
                out["refused"] += 1
            except Exception as exc:            # noqa: BLE001 -- the point is the TYPE
                raise AssertionError(
                    f"D6: {fn.__name__} refused a malformed k with {type(exc).__name__}, "
                    "not ValueError. All three must refuse alike -- the pre-repair module "
                    "raised three different types for one caller error."
                ) from exc
            else:
                raise AssertionError(
                    f"D6 REGRESSED: {fn.__name__} ACCEPTED a malformed k ({bad!r}) and "
                    "broadcast it into a full-length wrong answer."
                )
    assert out["refused"] == out["cases"] == 15, out

    # THE NO-OP HALF: a well-formed k is still accepted, and the transform is unchanged.
    k_ok = wavenumbers(n)
    h_ok = np.fft.irfft(hilbert_hat(wh.copy(), k_ok), n)
    assert np.isfinite(h_ok).all() and float(np.max(np.abs(h_ok))) > 0.5
    assert derivative_hat(wh.copy(), k_ok, n).shape == wh.shape
    assert velocity_hat(wh.copy(), k_ok).shape == wh.shape
    out["well_formed_k_still_accepted"] = True
    return out


# =========================================================================
# D7 -- degenerate n
# =========================================================================

def check_degenerate_n_refused():
    """REGRESSION (D7, repaired by leg 129): one consistent refusal at a degenerate `n`.

    BEFORE, three behaviours for one invalid input: `grid(0)` and `grid(-8)` returned EMPTY
    arrays silently, `wavenumbers(0)` and `dealias_mask(0)` raised ZeroDivisionError, and
    `wavenumbers(-8)` returned an empty array with no error.  `dealias_mask(1)` and
    `dealias_mask(2)` retained ZERO non-mean modes -- exactly the condition leg 89 made a
    hard ValueError in the 2D solver -- and the 1D path had no equivalent guard.

    AFTER: every one is a ValueError, and `dealias_mask` additionally refuses any n whose
    strict 2/3 cut retains no non-mean mode (n <= 3), which is leg 89's 2D guard in 1D.
    """
    out = {"refused": 0, "cases": 0}
    for fn in (grid, wavenumbers, dealias_mask):
        for bad in (0, -1, -8, 2.5):
            out["cases"] += 1
            try:
                fn(bad)
            except ValueError:
                out["refused"] += 1
            else:
                raise AssertionError(
                    f"D7 REGRESSED: {fn.__name__}({bad!r}) did not raise ValueError."
                )
    # n = 1, 2, 3: the strict cut retains no non-mean mode -- leg 89's 2D condition, in 1D
    for n in (1, 2, 3):
        out["cases"] += 1
        try:
            dealias_mask(n)
        except ValueError:
            out["refused"] += 1
        else:
            raise AssertionError(
                f"D7 REGRESSED: dealias_mask({n}) returned a mask retaining no non-mean "
                "mode instead of refusing."
            )
    assert out["refused"] == out["cases"] == 15, out

    # THE NO-OP HALF: every grid the repository actually runs is still accepted, and n = 4
    # (the smallest admissible size) still retains exactly one non-mean mode.
    for n in (64, 256, 512, 1024, 2048, 4096, 8192):
        assert int(dealias_mask(n).sum()) > 1, n
        assert grid(n).size == n and wavenumbers(n).size == n // 2 + 1, n
    assert int(np.sum(dealias_mask(4) & (wavenumbers(4) > 0))) == 1
    out["declared_grids_accepted"] = 7
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
    check_nyquist_poison_propagates,
    check_non_nyquist_poison_propagates,
    check_leg69_odd_n_regression,
    check_velocity_hat_mean_mode_propagates,
    check_velocity_hat_dtype_promotes,
    check_malformed_k_refused,
    check_degenerate_n_refused,
    check_integral_quantities_propagate,
    check_length_guard_exact,
]


def test_dealias_alias_free_guarantee():
    check_dealias_alias_free_guarantee()


def test_energy_production_aliasing():
    check_energy_production_aliasing()


def test_nyquist_poison_propagates():
    check_nyquist_poison_propagates()


def test_non_nyquist_poison_propagates():
    check_non_nyquist_poison_propagates()


def test_leg69_odd_n_regression():
    check_leg69_odd_n_regression()


def test_velocity_hat_mean_mode_propagates():
    check_velocity_hat_mean_mode_propagates()


def test_velocity_hat_dtype_promotes():
    check_velocity_hat_dtype_promotes()


def test_malformed_k_refused():
    check_malformed_k_refused()


def test_degenerate_n_refused():
    check_degenerate_n_refused()


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
    print("NOTE: leg 120 pinned 7 defects here (D1-D7); leg 129 REPAIRED all seven and")
    print("inverted every pin, so these now assert the CORRECT behaviour and fail if the")
    print("defect returns. Pre-repair magnitudes: writeup/data/p2_route_sua_v1_adversarial.json")
    print("Repair + no-op measurement:          writeup/data/p2_route_sur_v1_repair.json")
