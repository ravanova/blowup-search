"""Adversarial gates for the damped Newton solve in solver/bordered_hl.py (leg 80, Route-BHN).

test_bordered_hl.py validates the module on WELL-POSED data: a good initial guess, a
converging ladder, a published ratio at the end. This file validates the other half --
what the solver says when the input is hostile. It banks leg 80's battery so the answer
cannot silently regress.

The gate leg 80 answered, verbatim:

  "Under an adversarial battery (near-singular Jacobian at the starting iterate,
   NaN/Inf-poisoned initial guess, a residual sequence oscillating just above and below
   tolerance), does solver/bordered_hl.py's damped Newton solve ever incorrectly report
   convergence?"

Answered NO on the module's own system, over 336 cases, 0 false reports. A FALSE REPORT
is defined here exactly as it was there, and is never read off the returned ladder:

  converged is True AND ( ||F(z_returned)||_inf >= tol, RECOMPUTED from the returned
  iterate, OR z_returned is not all finite ).

TWO KINDS OF TEST LIVE IN THIS FILE, AND THEY MUST NOT BE CONFUSED
------------------------------------------------------------------
1. SOUNDNESS gates (`test_no_false_convergence_*`). These assert the property. If one
   ever fails, the solver has started lying about convergence.

2. CHARACTERIZATION gates (`test_characterize_*`). These pin behaviour that leg 80
   measured and reported as a WEAKNESS but was not authorised to repair: an unpopulated
   `cond` history, a backtracking loop that accepts an uphill step when its budget runs
   out, a `converged=True` returned at a point where DF is exactly singular, and a
   residual criterion that accepts a system with no root at all. They PASS today because
   they describe today's code. When a leg is authorised to repair any of them these tests
   will start FAILING, and that is the intended signal -- exactly the discipline leg 69
   set for test_interval_stress.py. THEY MUST NOT BE WEAKENED TO MAKE A REPAIR LOOK
   UNNECESSARY, and they must not be read as endorsements.

Run: .venv/bin/python test_bordered_hl_adversarial.py
"""

import os

# Set before numpy is imported. On a 12-core host an unpinned np.linalg.solve on this
# module's N=205 matrix costs ~1.0 s against ~0.8 ms pinned; without this cap the file
# takes minutes rather than seconds. Environment effect, not a solver property.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import warnings  # noqa: E402

import numpy as np  # noqa: E402

from solver.bordered_hl import BorderedHL  # noqa: E402

SEED = 20260806


def _fresh(n=101, rho_max=8.0, x0=0.3, w=0.9):
    """The well-posed non-symmetric starting data of test_bordered_hl.py."""
    b = BorderedHL(n=n, rho_max=rho_max)
    Om = np.exp(-((b.X - x0) ** 2) / (2.0 * w ** 2))
    V = 0.8 * np.exp(-((b.X - 1.3 * x0) ** 2) / (2.0 * (1.1 * w) ** 2))
    z0 = b.pack(Om, V, 1.06, -0.42, 0.077)
    b.set_pin_from(z0)
    return b, z0


def _false_report(b, z_ret, hist, tol):
    """The predicate, recomputed independently of the ladder the solver returned."""
    if not hist["converged"]:
        return False, float("nan")
    if not np.isfinite(z_ret).all():
        return True, float("nan")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = float(np.abs(b.F(z_ret)).max())
    return (not (r < tol)), r


def _quiet_newton(b, z0, **kw):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return b.newton(z0, **kw)


# --------------------------------------------------------------------------- #
# 1. SOUNDNESS
# --------------------------------------------------------------------------- #
def test_no_false_convergence_under_a_near_singular_jacobian():
    """Drive cond(DF(z0)) from 4e3 to exactly infinite; the flag must never say True.

    The degeneracy is the module's own, not a contrived matrix: the last three columns
    of DF are (X*Om_X, -Omega, Om_X) over (X*V_X, -2V, V_X), all of which vanish with the
    profile amplitude, so scaling (Omega, V) by eps sends the three gauge columns to zero
    and DF to rank deficiency 3. Leg 80's novelty pass predicted, from the scipy/numpy
    record, that LAPACK would NOT raise on the near-singular members; the assertion below
    is on the flag, and the print records how far past raising the sweep actually got."""
    b, z0 = _fresh()
    zstar, _ = _quiet_newton(b, z0, tol=1e-13, max_iter=60)
    worst_cond, raised_at, worst_uphill = 0.0, [], 1.0
    for eps in (1e-1, 1e-4, 1e-8, 1e-10, 1e-13, 0.0):
        ze = zstar.copy()
        ze[:2 * b.n] *= eps
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sv = np.linalg.svd(b.jacobian(ze), compute_uv=False)
            try:
                np.linalg.solve(b.jacobian(ze), -b.F(ze))
            except np.linalg.LinAlgError:
                raised_at.append(eps)
        cond = float(sv[0] / sv[-1]) if sv[-1] > 0 else float("inf")
        z, h = _quiet_newton(b, ze, tol=1e-13, max_iter=40)
        bad, r = _false_report(b, z, h, 1e-13)
        assert not bad, f"eps={eps:.0e}: converged=True at recomputed residual {r:.3e}"
        if np.isfinite(cond):
            worst_cond = max(worst_cond, cond)
        L = np.asarray(h["residual_ladder"], dtype=float)
        for i in range(1, L.size):
            if np.isfinite(L[i]) and L[i - 1] > 0 and L[i] > L[i - 1]:
                worst_uphill = max(worst_uphill, L[i] / L[i - 1])
    assert raised_at == [0.0], (
        f"LinAlgError fired at {raised_at}; leg 80 measured it firing ONLY at exact "
        f"singularity, which is why the except-branch is not the guard it looks like")
    print(f"    finite conditioning swept to {worst_cond:.3e}; LinAlgError raised only at "
          f"eps=0; worst uphill step accepted along the way {worst_uphill:.3e}")
    print("[ok] a near-singular Jacobian at the starting iterate never produced a "
          "convergence report")


def test_no_false_convergence_from_a_nan_or_inf_poisoned_initial_guess():
    """NaN, +Inf and -Inf in every kind of slot, and in the border targets.

    The flag's only defence is np.isfinite applied to the RESIDUAL; nothing checks the
    returned iterate. Leg 80 measured that the poison DOES reach the returned iterate in
    the large majority of cases -- so this gate is about the flag refusing anyway."""
    b, z0 = _fresh()
    zstar, _ = _quiet_newton(b, z0, tol=1e-13, max_iter=60)
    pin0 = b.pin
    idxs = sorted(set(list(range(0, b.N, 17)) +
                      [0, b.i0, b.n - 1, b.n, b.n + b.i0,
                       2 * b.n, 2 * b.n + 1, 2 * b.n + 2]))
    cases = nonfinite = 0
    for val, tag in ((np.nan, "nan"), (np.inf, "+inf"), (-np.inf, "-inf")):
        for idx in idxs:
            b.pin = pin0
            zp = zstar.copy()
            zp[idx] = val
            z, h = _quiet_newton(b, zp, tol=1e-13, max_iter=8)
            bad, r = _false_report(b, z, h, 1e-13)
            assert not bad, f"poison {tag} at slot {idx}: converged=True (residual {r:.3e})"
            cases += 1
            nonfinite += int(not np.isfinite(z).all())
    for val in (np.nan, np.inf):
        for slot in range(3):
            pin = list(pin0)
            pin[slot] = val
            b.pin = tuple(pin)
            z, h = _quiet_newton(b, zstar, tol=1e-13, max_iter=8)
            bad, r = _false_report(b, z, h, 1e-13)
            assert not bad, f"poisoned border target {slot}: converged=True ({r:.3e})"
            cases += 1
    b.pin = pin0
    print(f"    {cases} poisoned starts over {len(idxs)} slots of {b.N} + 6 poisoned "
          f"border targets; {nonfinite} returned a NON-FINITE iterate and every one of "
          f"the {cases} reported converged=False")
    print("[ok] a NaN/Inf-poisoned initial guess never produced a convergence report")


def test_no_false_convergence_when_the_residual_oscillates_across_tolerance():
    """Find a ladder that dips and rises, then place tol strictly inside the dip.

    This forces the solve to stop at the bottom of an oscillation it was about to climb
    out of -- the gate's third family, made concrete rather than hoped for. Leg 80's
    finding is that these stops are HONEST: the dip is a real residual, and the Jacobian
    at the stopping point is well away from singular. The mechanism is that this object's
    round-off floor sits in [1.4e-15, 7.4e-15] while the module's own tol is 1e-13, about
    1.1 decades above it, so the oscillation lives strictly below any tolerance in use."""
    b, _ = _fresh()
    rng = np.random.default_rng(SEED)
    found = 0
    rises, sig_min = [], []
    for _ in range(300):
        if found >= 3:
            break
        Om = np.exp(-((b.X - rng.uniform(-1, 1)) ** 2) /
                    (2 * rng.uniform(0.4, 2.0) ** 2)) * rng.uniform(0.2, 3)
        V = np.exp(-((b.X - rng.uniform(-1, 1)) ** 2) /
                   (2 * rng.uniform(0.4, 2.0) ** 2)) * rng.uniform(0.2, 3)
        zz = b.pack(Om, V, rng.uniform(-3, 3), rng.uniform(-3, 3), rng.uniform(-1, 1))
        _, h = _quiet_newton(b, zz, tol=1e-16, max_iter=40)
        L = np.asarray(h["residual_ladder"], dtype=float)
        for i in range(1, L.size - 1):
            if np.isfinite(L[i]) and L[i] < L[i - 1] and L[i + 1] > L[i] and L[i] < 1e-4:
                tol = float(np.sqrt(L[i] * L[i + 1]))
                z2, h2 = _quiet_newton(b, zz, tol=tol, max_iter=40)
                bad, r = _false_report(b, z2, h2, tol)
                assert not bad, (f"tol {tol:.3e} inside a dip: converged=True at "
                                 f"recomputed residual {r:.3e}")
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    sv = np.linalg.svd(b.jacobian(z2), compute_uv=False)
                rises.append(L[i + 1] / L[i])
                sig_min.append(float(sv[-1]))
                found += 1
                break
    assert found >= 3, f"only {found} oscillating ladders found; the family did not run"
    print(f"    {found} dips, rise ratios {min(rises):.2f}x..{max(rises):.2f}x, tol placed "
          f"strictly inside each; sigma_min at every stopping point >= {min(sig_min):.2e}")
    print("[ok] a residual oscillating across tolerance never produced a FALSE "
          "convergence report -- every stop was a genuine sub-tolerance residual")


def test_the_flag_certifies_a_residual_and_not_an_iterate():
    """What "Newton to 5.66e-15" is worth in ITERATE units, measured, not assumed.

    capabilities.py's validated line for this module quotes a residual. A residual is not
    an error: ||dz|| <= ||F|| / sigma_min(DF). This gate measures sigma_min at the
    converged root and, independently of any linearization, perturbs the root ALONG the
    smallest right singular direction to read the residual response directly. It asserts
    only the ORDER of the gap, so it is a magnitude gate and not a brittle equality."""
    b, z0 = _fresh(n=101)
    z, h = _quiet_newton(b, z0, tol=1e-13, max_iter=60)
    assert h["converged"], "the well-posed baseline stopped converging"
    J = b.jacobian(z)
    _, S, Vt = np.linalg.svd(J)
    slope = min(float(np.abs(b.F(z + t * Vt[-1])).max()) / t for t in (1e-6, 1e-3, 1e-1))
    err = 1e-13 / slope
    assert S[-1] < 1e-2, f"sigma_min {S[-1]:.3e} is larger than measured; re-derive"
    assert err > 1e-11, (f"one tol now hides only {err:.2e} of iterate error; the gap leg "
                         f"80 measured has changed and the capabilities line needs re-reading")
    print(f"    sigma_min(DF) = {S[-1]:.3e}, cond = {S[0]/S[-1]:.3e}; residual response "
          f"along the softest direction {slope:.3e} per unit iterate error")
    print(f"    => a converged tol of 1e-13 pins the iterate only to ~{err:.2e} in the sup "
          f"norm, about {np.log10(err/1e-13):.1f} decades weaker than the residual quoted")
    print("[ok] the convergence flag is a statement about the residual, and its iterate "
          "content is measured")


# --------------------------------------------------------------------------- #
# 2. CHARACTERIZATION -- these describe TODAY's code. See the module docstring.
# --------------------------------------------------------------------------- #
def test_characterize_cond_history_is_advertised_and_never_populated():
    """`cond_hist = []` is allocated in newton() and nothing is ever appended to it.

    Every run returns hist["cond"] as a length-0 array. A caller guarding with
    `np.all(hist["cond"] < X)` gets True vacuously; one calling `.max()` gets an
    exception. WILL FAIL when the diagnostic is actually populated -- that is the signal."""
    b, z0 = _fresh()
    lens = []
    for tol in (1e-13, 1e-8, 1e-3):
        _, h = _quiet_newton(b, z0, tol=tol, max_iter=40)
        lens.append(int(np.asarray(h["cond"]).size))
    assert lens == [0, 0, 0], f"cond history is now populated ({lens}) -- update this gate"
    assert bool(np.all(np.array([]) < 0.0)), "numpy changed the empty-all convention"
    print(f"    hist['cond'] length {lens} across three tolerances; `np.all(empty < x)` "
          f"is True, so a guard written that way tests nothing")
    print("[ok] CHARACTERIZED: the conditioning diagnostic is returned empty")


def test_characterize_lambda_collapse_accepts_an_uphill_step():
    """`while lam > 1/1024` exits AT 1/1024 and then steps unconditionally.

    When no damping factor in the budget reduces the residual, the module takes the
    smallest one anyway, uphill or not, and leaves no signal beyond lambda == 1/1024.
    Deuflhard's NLEQ-ERR treats that same event as a termination criterion. Leg 80
    measured collapse in 78 of 80 random starts, with a worst accepted uphill ratio of
    2.798e+05. WILL FAIL if the loop learns to stop instead of stepping."""
    b, z0 = _fresh()
    rng = np.random.default_rng(SEED + 1)
    runs = collapsed = 0
    worst = 1.0
    for _ in range(24):
        Om = rng.normal(0, float(rng.choice([0.1, 1.0, 5.0])), b.n)
        V = rng.normal(0, float(rng.choice([0.1, 1.0, 5.0])), b.n)
        zz = b.pack(Om, V, rng.normal(0, 2), rng.normal(0, 2), rng.normal(0, 2))
        z, h = _quiet_newton(b, zz, tol=1e-12, max_iter=30)
        lam = np.asarray(h["lambda"], dtype=float)
        L = np.asarray(h["residual_ladder"], dtype=float)
        runs += 1
        collapsed += int(lam.size > 0 and lam.min() <= 1.0 / 1024)
        for i in range(1, L.size):
            if np.isfinite(L[i]) and L[i - 1] > 0 and L[i] > L[i - 1]:
                worst = max(worst, L[i] / L[i - 1])
        bad, _ = _false_report(b, z, h, 1e-12)
        assert not bad, "a lambda-collapse run reported convergence falsely"
    assert collapsed > runs // 2, (
        f"lambda now collapses in only {collapsed}/{runs} runs; leg 80 measured 78/80. "
        f"If the damping was repaired, this gate has done its job -- do not weaken it, "
        f"convert it into an assertion that collapse TERMINATES the solve")
    assert worst > 10.0, f"the worst accepted uphill ratio is now only {worst:.2f}x"
    print(f"    lambda bottomed out at 1/1024 in {collapsed}/{runs} random starts; the "
          f"largest residual INCREASE accepted by the line search was {worst:.3e}x")
    print("[ok] CHARACTERIZED: exhausting the backtracking budget takes the step anyway")


def test_characterize_converged_true_at_an_exactly_singular_jacobian():
    """The zero profile is an exact root at which DF has a three-dimensional kernel.

    Omega = V = 0 nulls both interior equations for ANY (c_l, c_omega, c_r), so with the
    border targets pinned at zero the residual is EXACTLY 0.0 and the three gauge
    constants are wholly undetermined -- the module's docstring says the whole point of
    bordering is that "the constants are unknowns of the SAME Newton system from the
    first iterate", and here they are not determined at all. The solve returns
    converged=True in zero iterations with the constants exactly as passed in.

    This is NOT a false report: the residual really is below tol. It is the precise sense
    in which converged=True does not mean "a locally unique root was found", which is what
    every downstream certificate consumer needs. WILL FAIL if the flag learns to inspect
    the Jacobian at the returned iterate."""
    b = BorderedHL(n=101, rho_max=8.0)
    b.pin = (0.0, 0.0, 0.0)
    seen = []
    for trip in ((1.06, -0.42, 0.077), (1e6, 1e6, 1e6), (-3.7, 91.2, -0.5)):
        zz = b.pack(np.zeros(b.n), np.zeros(b.n), *trip)
        z, h = _quiet_newton(b, zz, tol=1e-13, max_iter=20)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sv = np.linalg.svd(b.jacobian(z), compute_uv=False)
        nul = int((sv < 1e-12 * sv[0]).sum())
        _, _, cl, com, cr = b.unpack(z)
        assert h["converged"], "the degenerate root no longer reports convergence"
        assert float(h["residual_ladder"][-1]) == 0.0, "the residual is no longer exactly 0"
        assert nul == 3, f"nullity at the returned iterate is {nul}, not 3"
        assert (cl, com, cr) == trip, "the constants moved; the kernel is no longer flat"
        seen.append((trip, nul, float(sv[-1])))
    print(f"    three different constant triples, all returned unchanged, all "
          f"converged=True at residual exactly 0.0 with DF nullity 3 "
          f"(sigma_min = {seen[0][2]:.1e})")
    print("[ok] CHARACTERIZED: converged=True is returned where DF is exactly singular")


class _Rootless:
    """F(x) = exp(-x): smooth, NO root anywhere, and |F| -> 0 as x -> +inf."""

    def F(self, z):
        return np.exp(-np.asarray(z, dtype=float))

    def jacobian(self, z):
        return np.diag(-np.exp(-np.asarray(z, dtype=float)))


def test_characterize_residual_criterion_accepts_a_system_with_no_root():
    """The production loop, unbound, driven on a residual that vanishes without a root.

    This is fault injection into the ALGORITHM and says nothing about the bordered
    system's own F, which is a degree-2 polynomial. It is banked because it fixes the
    scope of the convergence flag exactly: `res[-1] < tol` cannot distinguish "found a
    root" from "walked out along a decaying tail". Documented limitation of residual-only
    termination (leg 80 novelty pass, Q1/Q2), exercised through this code path.
    WILL FAIL if the loop ever gains a step-norm or Jacobian-based criterion."""
    z, h = BorderedHL.newton(_Rootless(), np.array([0.0]), tol=1e-12, max_iter=60)
    assert h["converged"], "the loop no longer accepts a rootless decaying residual"
    assert float(np.exp(-z[0])) < 1e-12, "the returned point is not sub-tolerance"
    lam = np.asarray(h["lambda"], dtype=float)
    assert lam.size and float(lam.min()) == 1.0, "damping fired; the walk is not undamped"
    print(f"    converged=True after {np.asarray(h['residual_ladder']).size - 1} full "
          f"(lambda=1) steps at x = {z[0]:.1f}, residual {float(np.exp(-z[0])):.2e} < "
          f"1e-12, on a system whose residual has NO zero at any finite x")
    print("[ok] CHARACTERIZED: the criterion cannot distinguish a root from a decaying tail")


# =========================================================================== #
# LEG 198 (Route-BHA) -- the CERTIFICATE-CONSTANTS path
# =========================================================================== #
# Leg 80, above, audited newton()'s `converged` flag and answered NO. Its runner never
# called certificate_constants, constants_vs_weight, quadratic, induced_sup_norm,
# weights, velocity_matrix, tail_exponent or profile_shape -- eight public symbols, and
# among them the one that returns Y_0/Z_1/Z_2. Leg 198 audited that surface and its gate
# answered YES: four silent-corruption sites. solver/bordered_hl.py was NOT edited (leg
# 198 was read-only on it under both branches), so every leg-198 defect gate below is a
# CHARACTERIZATION gate in the sense this file already defines: it passes because it
# describes today's code, and it MUST start failing when a repair lands. That is the
# signal. Do not weaken one to make a repair look unnecessary.
#
# The leg-198 SOUNDNESS gates bank the four families that came back clean, so those
# cannot regress either.

from solver.bordered_hl import (  # noqa: E402
    induced_sup_norm, velocity_matrix, tail_exponent)


def _converged(n=101):
    b, z0 = _fresh(n=n)
    z, _ = _quiet_newton(b, z0, tol=1e-12, max_iter=40)
    return b, z


# --------------------------------------------------------------------------- #
# leg 198 -- CHARACTERIZATION: the four silent-corruption sites
# --------------------------------------------------------------------------- #
def test_characterize_negative_weight_returns_a_negative_operator_norm():
    """THE HEADLINE. induced_sup_norm has no sign check on its weights.

    ||M||_w = max_i w_row_i * sum_j |M_ij| / w_col_j is a norm only for w > 0. With a
    negative w_col entry the inner sum can go negative and np.max returns it, so the
    function hands back a NEGATIVE operator norm -- finite, unwarned, unraised.

    Pinned on a 2x2 whose weighted norm is hand-computable:
        M = [[1, 100], [3, 4]],  w = (1,1)  ->  max(1+100, 3+4) = 101 exactly.
    WILL FAIL when a positivity guard lands on the weights."""
    M = np.array([[1.0, 100.0], [3.0, 4.0]])
    assert induced_sup_norm(M, np.array([1.0, 1.0]), np.array([1.0, 1.0])) == 101.0, \
        "the hand-computed control moved; the known answer is wrong"
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        got = induced_sup_norm(M, np.array([1.0, 1.0]), np.array([1.0, -1.0]))
        got_tiny = induced_sup_norm(M, np.array([1.0, 1.0]), np.array([1.0, -1e-9]))
    assert not ws, "a warning is now emitted; the corruption is no longer silent"
    assert got == -1.0, f"negative-weight return moved from -1.0 to {got}"
    assert np.isfinite(got) and got < 0.0, "no longer returns a finite negative norm"
    assert abs(got_tiny + 3999999997.0) < 1.0, f"w=-1e-9 case moved: {got_tiny}"
    print(f"    true weighted norm 101.0; w_col=(1,-1) returns {got}, "
          f"w_col=(1,-1e-9) returns {got_tiny:.6e} -- both finite, both unwarned")
    print("[ok] CHARACTERIZED: a negative weight yields a negative 'operator norm'")


def test_characterize_negative_weight_fabricates_a_closing_certificate():
    """The consequence, at the level the certificate is actually read.

    Same magnitude, one sign flipped, nothing else changed. The honest constants at
    w_r=+1e-6 give a radii polynomial with NO real root -- the certificate does not
    close, which is this object's documented ceiling (legs 46/47). Flip the sign and a
    root appears. Zero is REJECTED (ZeroDivisionError); only the negative half is silent.
    WILL FAIL when a positivity guard lands."""
    b, z = _converged()
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        pos = b.certificate_constants(z, p=0.0, w_r=+1e-6)
        neg = b.certificate_constants(z, p=0.0, w_r=-1e-6)
    assert not ws, "a warning is now emitted; the corruption is no longer silent"
    assert pos["Z2"] > 0 and pos["B"] > 0, "the positive-weight control is no longer sane"
    assert neg["Z2"] < 0 and neg["B"] < 0, "Z_2/B no longer go negative under w_r < 0"
    assert all(np.isfinite(neg[k]) for k in ("Y0", "Z1", "Z2", "A_norm", "B")), \
        "the negative-weight branch is no longer silent (non-finite now)"
    z1_under = pos["Z1"] / neg["Z1"]
    a_under = pos["A_norm"] / neg["A_norm"]
    assert z1_under > 1e8, f"Z_1 understatement collapsed to {z1_under:.4g}x"
    assert a_under > 1e8, f"||A|| understatement collapsed to {a_under:.4g}x"
    # zero is rejected -- the asymmetry is the point
    for kw in (dict(w_l=0.0), dict(w_om=0.0), dict(w_r=0.0)):
        try:
            b.certificate_constants(z, p=0.0, **kw)
            raise AssertionError(f"a zero weight {kw} is no longer rejected")
        except ZeroDivisionError:
            pass
    print(f"    w_r=+1e-6: Z_2={pos['Z2']:.6e} (>0).  w_r=-1e-6: Z_2={neg['Z2']:.6e} (<0)")
    print(f"    Z_1 understated {z1_under:.4g}x, ||A|| understated {a_under:.4g}x, "
          f"all finite, no warning; w=0 IS rejected")
    print("[ok] CHARACTERIZED: one sign flip understates the constants and inverts Z_2")


def test_characterize_velocity_matrix_accepts_a_permuted_grid():
    """velocity_matrix is a trapezoidal antiderivative assuming an ASCENDING grid.

    This is the exact gap leg 117 found and leg 152 closed in the sibling module
    solver/hl_rescaled.py, where a permuted grid now raises HLRescaledDomainError. Here
    it is still accepted. Known answer: U = W @ cos = sin, pinned at U(0)=0.
    WILL FAIL when a monotonicity guard lands on this module."""
    n = 401
    X = np.linspace(-2.0, 2.0, n)
    f = np.cos(X)
    err_sorted = float(np.max(np.abs(velocity_matrix(X, n // 2) @ f - np.sin(X))))
    assert err_sorted < 1e-4, f"the instrument itself is broken: {err_sorted:.3e}"
    perm = np.random.default_rng(SEED + 3).permutation(n)
    Xp = X[perm]
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        Wp = velocity_matrix(Xp, int(np.argmin(np.abs(Xp))))
    assert not ws, "a warning is now emitted on a permuted grid"
    assert np.all(np.isfinite(Wp)), "the permuted grid no longer returns finite garbage"
    err_perm = float(np.max(np.abs(Wp @ f[perm] - np.sin(Xp))))
    assert err_perm / err_sorted > 1e4, \
        f"permuted-grid error collapsed to {err_perm / err_sorted:.4g}x"
    print(f"    sorted grid reproduces sin to {err_sorted:.3e}; permuted grid errs by "
          f"{err_perm:.4f}, a factor {err_perm / err_sorted:.6g}, silently and finitely")
    print("[ok] CHARACTERIZED: a permuted grid is accepted (leg 152's gap, unclosed here)")


def test_characterize_pin_of_wrong_arity_is_silently_truncated():
    """BorderedHL(pin=...) does not check that the pin has three entries.

    An over-long pin is stored whole and its extra targets are silently ignored; an
    under-long one is not caught at construction either, only later as an IndexError
    from inside F. WILL FAIL when the constructor validates arity."""
    b3 = BorderedHL(n=101, rho_max=8.0, pin=(1.0, 2.0, 3.0))
    b5 = BorderedHL(n=101, rho_max=8.0, pin=(1.0, 2.0, 3.0, 4.0, 5.0))
    assert len(b5.pin) == 5, "the over-long pin is no longer stored whole"
    _, z0 = _fresh()
    assert np.allclose(b3.F(z0), b5.F(z0)), \
        "the 4th/5th targets now affect F; they used to be ignored"
    b2 = BorderedHL(n=101, rho_max=8.0, pin=(1.0, 2.0))
    try:
        b2.F(z0)
        raise AssertionError("an arity-2 pin no longer fails at all")
    except IndexError:
        pass
    print("    pin arity 5 stored as 5, F identical to arity 3 (entries 4,5 discarded); "
          "arity 2 raises IndexError from inside F, not from the constructor")
    print("[ok] CHARACTERIZED: pin arity is unchecked at construction")


def test_characterize_tail_exponent_silently_drops_nan_samples():
    """tail_exponent's `np.abs(f) > 0` mask is False for NaN, so NaN samples are
    EXCLUDED from the fit rather than propagating. The module's docstring calls this an
    INTERNAL KNOWN-ANSWER CHECK, so a diagnostic that launders poison is worse than
    none. WILL FAIL when NaN is propagated or rejected."""
    b, _ = _fresh()
    X = b.X
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        f = np.abs(X) ** -0.4 + 1e-12
    honest = tail_exponent(X, f, 1.0, 100.0)
    assert abs(honest + 0.4) < 1e-9, f"the control power law moved: {honest}"
    idx = np.where((X >= 1.0) & (X <= 100.0))[0]
    g = f.copy()
    g[idx[:len(idx) // 2]] = np.nan            # half the fitting window is NaN
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        got = tail_exponent(X, g, 1.0, 100.0)
    assert not ws, "a warning is now emitted when the window contains NaN"
    assert np.isfinite(got), "NaN now propagates to the returned exponent"
    assert abs(got - honest) < 1e-9, f"the reported exponent moved by {abs(got - honest):.3e}"
    print(f"    {len(idx) // 2} of {idx.size} window samples set to NaN; reported exponent "
          f"moves from {honest:.15f} to {got:.15f}, a shift of {abs(got - honest):.3e}")
    print("[ok] CHARACTERIZED: NaN samples are silently dropped from the tail fit")


# --------------------------------------------------------------------------- #
# leg 198 -- SOUNDNESS: the four families that came back clean
# --------------------------------------------------------------------------- #
def test_z1_detects_a_planted_approximate_inverse():
    """certificate_constants takes A from the caller. Z_1 = ||I - A J|| is the only
    check that A is what it claims, and it works: every planted A that changes A J
    raises Z_1, and the exact A is not flagged. This is the leg 116/128/146
    fabrication-acceptance probe coming back NEGATIVE, and it must stay negative."""
    b, z = _converged()
    J = b.jacobian(z)
    Ahat = np.linalg.inv(J)
    base = b.certificate_constants(z, p=0.0, A=Ahat)
    _, z_other = _fresh()
    planted = {
        "halved": 0.5 * Ahat, "doubled": 2.0 * Ahat, "zero": np.zeros((b.N, b.N)),
        "identity": np.eye(b.N), "transposed": Ahat.T.copy(),
        "wrong_state": np.linalg.inv(b.jacobian(z_other)),
        "border_cols_zeroed": np.where(
            np.arange(b.N)[None, :] >= 2 * b.n, 0.0, Ahat),
        "one_entry_x1e6": Ahat * np.where(
            (np.arange(b.N)[:, None] == 0) & (np.arange(b.N)[None, :] == 0), 1e6, 1.0),
    }
    for name, A in planted.items():
        c = b.certificate_constants(z, p=0.0, A=A)
        rise = c["Z1"] / base["Z1"]
        assert rise > 100.0, f"planted A '{name}' is no longer detected (Z_1 rise {rise:.4g}x)"
    assert base["Z1"] < 1e-6, f"the exact A is now flagged: Z_1 = {base['Z1']:.3e}"
    print(f"    exact A: Z_1 = {base['Z1']:.3e} (not flagged); "
          f"{len(planted)}/{len(planted)} planted inverses raise Z_1 by >100x")
    print("[ok] SOUND: Z_1 is a real check on a caller-supplied approximate inverse")


def test_degenerate_matching_condition_propagates_visibly():
    """The gate's named configuration. Make the Omega_X(0) border row collinear with the
    Omega(0) row, so the bordered Jacobian loses rank IN THE BORDER BLOCK -- the
    matching condition itself degenerates. Y_0 must EXPLODE, not shrink: a degenerate
    matching condition that quietly produced a small Y_0 would be the worst finding
    available on this module, and it does not happen."""
    b_ctl, z_ctl = _fresh()
    ctl = b_ctl.certificate_constants(z_ctl, p=0.0)
    for label, eps in [("exactly collinear", None), ("near", 1e-14), ("near", 1e-10)]:
        b, z = _fresh()
        b.Drow0 = np.zeros(b.n)
        b.Drow0[b.i0] = 1.0
        if eps is not None:
            b.Drow0[b.i0 + 1] = eps
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            c = b.certificate_constants(z, p=0.0)
        assert c["Y0"] > 1e6 * ctl["Y0"], \
            f"{label} eps={eps}: Y_0 = {c['Y0']:.3e} did NOT explode over {ctl['Y0']:.3e}"
    b, z = _fresh()
    b.Drow0 = np.zeros(b.n)
    b.Drow0[b.i0] = 1.0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        c = b.certificate_constants(z, p=0.0)
    print(f"    honest control Y_0 = {ctl['Y0']:.4e}; exactly-degenerate border rows give "
          f"Y_0 = {c['Y0']:.4e}, an inflation of {c['Y0'] / ctl['Y0']:.4g}x")
    print("[ok] SOUND: a degenerate matching condition inflates Y_0, it does not hide")


def test_poisoned_state_propagates_through_the_estimator():
    """One poisoned entry of z, at 7 positions x 4 poisons. Every one must reach the
    reported constants -- either non-finite, or inflated past 1e6x. 0 silently absorbed."""
    b, z = _converged()
    base = b.certificate_constants(z, p=0.0)
    spots = [5, b.i0, b.n + 5, b.n + b.i0, 2 * b.n, 2 * b.n + 1, 2 * b.n + 2]
    absorbed = []
    for poison in (np.nan, np.inf, -np.inf, 1e300):
        for idx in spots:
            zz = z.copy()
            zz[idx] = poison
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                try:
                    c = b.certificate_constants(zz, p=0.0)
                except Exception:
                    continue                      # an exception is visible rejection
            ok = (not all(np.isfinite(c[k]) for k in ("Y0", "Z1", "Z2"))
                  or c["Y0"] > 1e6 * base["Y0"])
            if not ok:
                absorbed.append((idx, poison))
    assert not absorbed, f"{len(absorbed)} poisoned states are now silently absorbed: {absorbed[:5]}"
    print(f"    {len(spots) * 4}/{len(spots) * 4} poisoned states propagate, 0 absorbed")
    print("[ok] SOUND: the estimator does not launder a poisoned state")


def test_exact_quadratic_identity_holds_and_discriminates():
    """F is degree 2, so F(z+v) - F(z) - DF(z) v = Q(v,v) exactly. Banked BOTH ways: it
    holds at machine precision across 1e-3..1e6, AND a 1e-6 relative corruption of Q is
    separated from the true Q by ~1e9, so the identity is discriminating, not vacuous."""
    b, z = _converged()
    rng = np.random.default_rng(SEED + 2)
    for scale in (1e-3, 1.0, 1e3, 1e6):
        v = rng.normal(size=b.N) * scale
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            lhs = b.F(z + v) - b.F(z) - b.jacobian(z) @ v
            rhs = b.quadratic(v)
        rel = float(np.max(np.abs(lhs - rhs)) / max(np.max(np.abs(rhs)), 1e-300))
        assert rel < 1e-10, f"the identity broke at scale {scale:g}: rel = {rel:.3e}"
    v = rng.normal(size=b.N)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        lhs = b.F(z + v) - b.F(z) - b.jacobian(z) @ v
        good = b.quadratic(v)
    rel_good = float(np.max(np.abs(lhs - good)) / np.max(np.abs(good)))
    bad = good * 1.000001
    rel_bad = float(np.max(np.abs(lhs - bad)) / np.max(np.abs(bad)))
    assert rel_bad / rel_good > 1e6, \
        f"the identity no longer discriminates a 1e-6 corruption ({rel_bad / rel_good:.3g}x)"
    print(f"    identity holds to {rel_good:.3e}; a 1e-6 corruption of Q reads "
          f"{rel_bad:.3e}, a separation of {rel_bad / rel_good:.4g}x")
    print("[ok] SOUND: the exact-quadratic known-answer check is real and discriminating")


def test_constants_vs_weight_agrees_with_per_p_calls():
    """constants_vs_weight inverts DF once and reuses A across the whole p-curve, on the
    stated ground that A is p-independent. Measured, not assumed: exact agreement."""
    b, z = _converged()
    ps = [0.0, 0.5, 1.0, 2.0]
    curve = b.constants_vs_weight(z, ps)
    worst = 0.0
    for i, p in enumerate(ps):
        one = b.certificate_constants(z, p=p)
        for k in ("Y0", "Z1", "Z2"):
            worst = max(worst, abs(curve[i][k] - one[k]) / max(abs(one[k]), 1e-300))
    assert worst == 0.0, f"the curve no longer reproduces per-p calls exactly: {worst:.3e}"
    print(f"    {len(ps)} exponents x 3 constants, worst relative disagreement {worst:.1e}")
    print("[ok] SOUND: reusing one inverse across the p-curve is exact")


if __name__ == "__main__":
    test_no_false_convergence_under_a_near_singular_jacobian()
    test_no_false_convergence_from_a_nan_or_inf_poisoned_initial_guess()
    test_no_false_convergence_when_the_residual_oscillates_across_tolerance()
    test_the_flag_certifies_a_residual_and_not_an_iterate()
    test_characterize_cond_history_is_advertised_and_never_populated()
    test_characterize_lambda_collapse_accepts_an_uphill_step()
    test_characterize_converged_true_at_an_exactly_singular_jacobian()
    test_characterize_residual_criterion_accepts_a_system_with_no_root()
    print("\n--- leg 198 (Route-BHA): the certificate-constants path ---")
    test_characterize_negative_weight_returns_a_negative_operator_norm()
    test_characterize_negative_weight_fabricates_a_closing_certificate()
    test_characterize_velocity_matrix_accepts_a_permuted_grid()
    test_characterize_pin_of_wrong_arity_is_silently_truncated()
    test_characterize_tail_exponent_silently_drops_nan_samples()
    test_z1_detects_a_planted_approximate_inverse()
    test_degenerate_matching_condition_propagates_visibly()
    test_poisoned_state_propagates_through_the_estimator()
    test_exact_quadratic_identity_holds_and_discriminates()
    test_constants_vs_weight_agrees_with_per_p_calls()
    print("\nALL BORDERED-HL ADVERSARIAL TESTS PASSED")
