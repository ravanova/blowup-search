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


if __name__ == "__main__":
    test_no_false_convergence_under_a_near_singular_jacobian()
    test_no_false_convergence_from_a_nan_or_inf_poisoned_initial_guess()
    test_no_false_convergence_when_the_residual_oscillates_across_tolerance()
    test_the_flag_certifies_a_residual_and_not_an_iterate()
    test_characterize_cond_history_is_advertised_and_never_populated()
    test_characterize_lambda_collapse_accepts_an_uphill_step()
    test_characterize_converged_true_at_an_exactly_singular_jacobian()
    test_characterize_residual_criterion_accepts_a_system_with_no_root()
    print("\nALL BORDERED-HL ADVERSARIAL TESTS PASSED")
