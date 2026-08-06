"""Adversarial gates for `solver/first_integral.py` (leg 107, Route-FIA).

`test_first_integral.py` validates the module on WELL-FORMED parameters: the quadrature
against exact moments, the finite Hilbert transform against a Chebyshev known answer, the
a -> 0 anchor, the identity on independent profiles, the analytic Jacobian, the radius
against a cross-build, and the reconstruction nulling the original ODE residual. Every
input in that file is legal and in-domain. This file validates the other half — what the
module does at and beyond its own free boundary, and on NaN-poisoned samples — and banks
leg 107's battery so the answer cannot silently regress.

The gate leg 107 answered, verbatim:

  "Under an adversarial battery (inputs near the documented turning point, NaN-poisoned
   profile parameters), does solver/first_integral.py ever silently return a finite,
   plausible-looking wrong profile value instead of propagating or flagging the
   ill-conditioning?"

Answered **YES**, on two independent sites. `solver/first_integral.py` was NOT edited —
leg 107 had no patch authority under its own gate, so both findings are PINNED here rather
than repaired.

WHAT "TRUE" MEANS OUTSIDE THE SUPPORT, AND WHERE IT COMES FROM
--------------------------------------------------------------
Not this leg's invention. `solver/first_integral.py`'s own module docstring, lines 29-33:

    THE PROFILE ENDS, and it is forced rather than assumed. E is decreasing ... so E
    reaches zero at a finite X_c; beyond it E < 0 and E^{1/a} is not real, so Omega == 0.

`solver/turning_point.py` states the same thing with the outside asymptotics
E ~ (a m / pi) log(X / X_c) < 0. So for v = X / X_c > 1 the true profile value is EXACTLY
ZERO, and any nonzero return there is wrong by its own full magnitude. The module's
`omega_of` computes `-np.abs(e) ** self.p`; the `abs` erases the branch cut that is the
entire reason the profile is compactly supported.

TWO KINDS OF TEST LIVE IN THIS FILE, AND THEY MUST NOT BE CONFUSED
-------------------------------------------------------------------
1. SOUNDNESS gates (`test_no_silent_*`, `test_constructor_*`, `test_solve_*`). These
   assert a property that HOLDS. If one fails, the module has started absorbing bad input
   somewhere it previously propagated it.

2. CHARACTERIZATION gates (`test_characterize_*`). These pin behaviour leg 107 MEASURED,
   REPORTED and ESCALATED but was not authorised to repair. **They pass while the gap is
   open.** If one of them fails, that is very likely GOOD NEWS — someone has fixed the
   gap — and the correct response is to read leg 107's escalation
   (`experiments/journal/leg_107.md`), confirm the fix, and convert the gate to a
   soundness gate. It must NOT be "fixed" by loosening the tolerance.

Self-running, no pytest: `.venv/bin/python test_first_integral_adversarial.py`. ~12 s.
"""

import numpy as np

from solver.first_integral import (ReducedProfile, even_cheb,
                                   first_integral_defect)

K = 48
A_CASES = (0.3, 0.5)


def _solved(a, k=K):
    rp = ReducedProfile(a, K=k)
    r = rp.solve(Xc0=10.0)
    assert r["converged"], f"a={a}: the clean solve must converge first ({r})"
    return rp, r["b"], r["Xc"]


# ---------------------------------------------------------------------------
# 0. the fixture itself, before anything is concluded from it
# ---------------------------------------------------------------------------
def test_clean_reference_selfcheck():
    """Every gate below is read against a converged profile; gate that first."""
    print("\n[0] clean reference self-check")
    for a in A_CASES:
        rp, b, Xc = _solved(a)
        res = float(np.max(np.abs(rp.residual(b, Xc))))
        e_nodes = rp.e_of(b)
        interior = np.abs(rp.omega_of(b, np.linspace(0.0, 1.0, 201)))
        print(f"    a={a}: X_c/c = {Xc:.6f}, residual {res:.2e}, "
              f"min e at nodes {e_nodes.min():.3e} (>0), "
              f"max |Omega| on support {interior.max():.6f}")
        assert res < 1e-10, "the clean solve is not converged; nothing below is meaningful"
        assert e_nodes.min() > 0.0, "e must be positive on the support"
        # the amplitude gauge: Omega(0) = -1, so the profile's own range is [0, 1]
        assert abs(interior.max() - 1.0) < 1e-9, interior.max()
    print("[ok] fixture converged, e > 0 on the support, gauge |Omega| <= 1 holds")


# ---------------------------------------------------------------------------
# 1. CHARACTERIZATION -- the turning point (finding A, escalated, unpatched)
# ---------------------------------------------------------------------------
def test_characterize_profile_continues_past_its_own_support():
    """PINS A KNOWN GAP. Truth outside the support is 0; the module returns a number.

    Failure of this test most likely means `omega_of` learned to refuse or flag v > 1,
    which is the repair leg 107 recommended. Confirm against leg 107's escalation and
    promote this to a soundness gate; do not relax it.
    """
    print("\n[1] CHARACTERIZE: omega_of past the turning point (truth: exactly 0)")
    for a in A_CASES:
        rp, b, Xc = _solved(a)
        vals = {}
        for v in (1.0 + 1e-9, 1.001, 1.1, 1.5, 2.0):
            vals[v] = float(rp.omega_of(b, np.array([v]))[0])
        print(f"    a={a}: " + "  ".join(f"Om({v})={x:+.3e}" for v, x in vals.items()))
        for v, x in vals.items():
            assert np.isfinite(x), (a, v, x)      # nothing is flagged
            assert x != 0.0, (a, v, x)            # and it is NOT the true value, 0
        # the returned values sit INSIDE the profile's own range |Omega| <= 1, i.e.
        # magnitude alone cannot tell a caller the point is out of domain
        assert abs(vals[1.5]) < 1.0, vals[1.5]
        # ... and the band of such v is wider than the support itself
        T, _ = even_cheb(rp.K, np.array([1.0]))
        v_plaus = float(np.sqrt(1.0 + 1.0 / float(T[0] @ b)))
        print(f"          every v in (1, {v_plaus:.4f}) returns a value inside the "
              f"profile's own range -- a band {v_plaus - 1.0:.2f} supports wide")
        assert v_plaus > 1.5, v_plaus
    print("[ok] pinned: 10/10 out-of-support evaluations return finite nonzero values, "
          "0 exceptions, 0 NaNs")


def test_characterize_out_of_support_value_mirrors_a_legitimate_one():
    """PINS A KNOWN GAP. Omega(1+d) is numerically a legitimate interior value.

    This is what makes the gap dangerous rather than merely untidy: a caller whose grid
    overshoots X_c by a fraction of a percent gets a value it cannot distinguish from a
    real one by inspection.
    """
    print("\n[2] CHARACTERIZE: the mirror |Omega(1+d)/Omega(1-d) - 1|")
    worst = 0.0
    for a in A_CASES:
        rp, b, Xc = _solved(a)
        line = []
        for d in (1e-7, 1e-4, 1e-2):
            i = float(rp.omega_of(b, np.array([1.0 - d]))[0])
            o = float(rp.omega_of(b, np.array([1.0 + d]))[0])
            rel = abs(o / i - 1.0)
            worst = max(worst, rel)
            line.append(f"d={d:g}:{rel:.1e}")
        print(f"    a={a}: " + "  ".join(line))
    print(f"    worst relative deviation at any d <= 1e-2: {worst:.2e}")
    assert worst < 5e-2, (
        "the out-of-support value stopped mirroring the interior one -- re-derive")
    print("[ok] pinned: within 1% of X_c the wrong value agrees with the legitimate "
          "mirror value to better than 5e-2 relative")


def test_characterize_even_cheb_clips_silently():
    """PINS A KNOWN GAP. Every v > 1 is evaluated AT v = 1 (np.clip in even_cheb),

    while `e_of` keeps the UNCLIPPED (1 - v^2) prefactor, so the two halves of e(v)
    disagree about which point they describe. The resulting e is not the true E outside
    either: it overstates |E| against the module's own outer quadrature.
    """
    print("\n[3] CHARACTERIZE: even_cheb's silent clip")
    T_far, _ = even_cheb(6, np.array([1.5, 3.0, 50.0]))
    T_edge, _ = even_cheb(6, np.array([1.0]))
    dev = float(np.max(np.abs(T_far - T_edge[0][None, :])))
    print(f"    max |T_2k(v) - T_2k(1)| for v in (1.5, 3, 50): {dev:.1e}")
    assert dev == 0.0, "the clip is gone -- confirm against leg 107 and promote this gate"
    a = 0.3
    rp, b, Xc = _solved(a)
    wq = -np.abs(rp.PHI_u @ b) ** rp.p
    for v, lo in ((1.1, 1.05), (2.0, 2.0)):
        y = np.geomspace(1.0, v, 2001)
        Hy = ((wq[None, :] / (y[:, None] - rp.u[None, :])) @ rp.w) / np.pi
        e_true = (a / rp.c) * Xc * float(np.sum(0.5 * (Hy[1:] + Hy[:-1]) * np.diff(y)))
        e_poly = float(rp.e_of(b, np.array([v]))[0])
        print(f"    v={v}: e_poly={e_poly:+.4e}  e_true(outer)={e_true:+.4e}  "
              f"ratio={e_poly / e_true:.3f}")
        assert e_poly / e_true > lo, (v, e_poly / e_true)
    print("[ok] pinned: the clip is silent and the extrapolated e overstates the true "
          "|E| by 1.1x at v=1.1 rising past 2x at v=2")


# ---------------------------------------------------------------------------
# 2. CHARACTERIZATION -- the validator's NaN blindness (finding B, unpatched)
# ---------------------------------------------------------------------------
def test_characterize_defect_absorbs_nan_points():
    """PINS A KNOWN GAP. `first_integral_defect`'s default mask drops NaN silently.

    The function's documented job is "max/min - 1 of |Omega| / E^{1/a} -- zero iff (FI)
    holds on the sample". Its default mask is `(|Omega| > 1e-11) & (E > 1e-8)`, and every
    comparison against NaN is false (IEEE-754 5.11), so poisoned points leave the sample
    instead of poisoning the answer. It then reports machine-precision agreement for a
    sample it never checked.
    """
    print("\n[4] CHARACTERIZE: first_integral_defect on NaN-poisoned samples")
    a, c, N = 0.3, 0.5, 400
    X = np.linspace(0.01, 3.0, N)
    E = c * np.exp(-X ** 2 / 4.0)
    U = (E - c) / a
    Om = -(E / c) ** (1.0 / a)
    clean = first_integral_defect(Om, U, a, c)
    print(f"    clean defect {clean:.3e}")
    assert clean < 1e-12, clean
    worst_absorbed = 0
    for nbad in (1, 100, 397, 398, 400):
        Op = Om.copy()
        Op[:nbad] = np.nan
        d = first_integral_defect(Op, U, a, c)
        flagged = bool(np.isnan(d))
        print(f"      {nbad:3d}/{N} NaN -> {d!s:<24}"
              f"{'FLAGGED' if flagged else 'reported as HOLDS'}")
        if not flagged:
            worst_absorbed = max(worst_absorbed, nbad)
            assert d < 1e-12, (nbad, d)
    print(f"    largest NaN count silently absorbed: {worst_absorbed}/{N} "
          f"({100.0 * worst_absorbed / N:.2f}% of the sample)")
    assert worst_absorbed >= 397, (
        "the validator stopped absorbing NaN -- confirm the fix against leg 107 and "
        "promote this gate to a soundness gate")
    # it only flags once fewer than 3 points survive, i.e. by the arity guard, not by
    # noticing the poison at all
    assert np.isnan(first_integral_defect(np.full(N, np.nan), U, a, c))
    print("[ok] pinned: 397 of 400 points may be NaN and the identity still reports "
          "1.3e-15; the flag at 398 is the <3-survivors guard, not poison detection")


def test_no_silent_absorption_of_finite_poison():
    """SOUNDNESS. A poison that is a NUMBER rather than a NaN IS caught."""
    print("\n[5] SOUNDNESS: a finite poison is caught")
    a, c, N = 0.3, 0.5, 400
    X = np.linspace(0.01, 3.0, N)
    E = c * np.exp(-X ** 2 / 4.0)
    U = (E - c) / a
    Om = -(E / c) ** (1.0 / a)
    d = first_integral_defect(np.where(np.arange(N) == 200, Om * 2.0, Om), U, a, c)
    print(f"    one point doubled -> defect {d:.6f} (clean is ~6e-15)")
    assert d > 0.5, d
    dinf = first_integral_defect(np.where(np.arange(N) == 3, np.inf, Om), U, a, c)
    print(f"    one point +inf     -> defect {dinf}")
    assert np.isinf(dinf), dinf
    for bad, label in ((float("nan"), "a"), (float("nan"), "c")):
        got = (first_integral_defect(Om, U, bad, c) if label == "a"
               else first_integral_defect(Om, U, a, bad))
        print(f"    {label}=nan -> {got}")
        assert np.isnan(got), (label, got)
    print("[ok] finite poison, inf poison and NaN SCALARS all propagate or flag")


# ---------------------------------------------------------------------------
# 3. SOUNDNESS -- everything the module gets right
# ---------------------------------------------------------------------------
def test_no_silent_corruption_from_nan_coefficients():
    """SOUNDNESS. A NaN in b_k reaches every derived quantity as NaN."""
    print("\n[6] SOUNDNESS: NaN in a Chebyshev coefficient propagates")
    rp, b, Xc = _solved(0.3)
    probes, finite = 0, 0
    for k in (0, 1, 10, rp.K - 1):
        bp = b.copy()
        bp[k] = np.nan
        with np.errstate(all="ignore"):
            outs = {"mass": rp.mass(bp, Xc),
                    "edge_amplitude": rp.edge_amplitude(bp, Xc),
                    "omega_of(0.5)": float(rp.omega_of(bp, np.array([0.5]))[0]),
                    "operator_norm": rp.operator_norm(bp, Xc),
                    "residual": float(np.max(np.abs(rp.residual(bp, Xc))))}
        for name, x in outs.items():
            probes += 1
            if np.isfinite(x):
                finite += 1
                print(f"    !! b[{k}]=nan -> {name} returned finite {x}")
    print(f"    finite values returned across {probes} probes: {finite}")
    assert finite == 0, "a NaN coefficient is being absorbed somewhere -- escalate"
    print("[ok] 0 silent finite values across 20 poisoned-coefficient probes")


def test_constructor_rejects_degenerate_a():
    """SOUNDNESS (with one pinned edge). a <= 0 and a = nan are refused."""
    print("\n[7] SOUNDNESS: the constructor's guard on a")
    for label, aa in (("nan", float("nan")), ("zero", 0.0), ("negative", -0.5)):
        try:
            ReducedProfile(aa, K=8)
        except ValueError:
            print(f"    a={label}: ValueError (refused)")
        else:
            raise AssertionError(f"a={label} was accepted")
    # PINNED EDGE: a = inf passes the guard (0.0 < inf) and gives p = 0, but the solve
    # then refuses rather than returning a number.
    rp = ReducedProfile(float("inf"), K=16)
    assert rp.p == 0.0, rp.p
    with np.errstate(all="ignore"):
        r = rp.solve(Xc0=10.0)
    print(f"    a=inf: accepted by the guard (p={rp.p}), solve converged="
          f"{r['converged']} residual={r['residual']}")
    assert not r["converged"], "a=inf now converges to something -- re-derive"
    print("[ok] nan/0/negative refused at construction; inf is admitted but never "
          "yields a converged answer")


def test_solve_never_lies_about_convergence():
    """SOUNDNESS. `converged` is true only when the residual really is below 1e-10."""
    print("\n[8] SOUNDNESS: the honesty of solve()['converged']")
    rp, b, Xc = _solved(0.3)
    bad = b.copy()
    bad[3] = np.nan
    with np.errstate(all="ignore"):
        cases = [("b0 poisoned", rp.solve(Xc0=10.0, b0=bad)),
                 ("Xc0 = nan", rp.solve(Xc0=float("nan"))),
                 ("Xc0 = -10", rp.solve(Xc0=-10.0)),
                 ("Xc0 = 1e9", rp.solve(Xc0=1e9))]
    for label, r in cases:
        drift = abs(r["Xc"] / Xc - 1.0) if r["converged"] else float("nan")
        print(f"    {label:12s} converged={r['converged']!s:5s} "
              f"residual={r['residual']:.2e}" +
              (f"  X_c drift {drift:.1e}" if r["converged"] else ""))
        assert r["converged"] == bool(r["residual"] < 1e-10), label
        if r["converged"]:
            # an extreme but legal start must land on the SAME radius
            assert drift < 1e-10, (label, drift)
    assert not cases[0][1]["converged"] and not cases[1][1]["converged"]
    print("[ok] 0 dishonest flags in 4 cases; extreme legal starts land on the same "
          "X_c to better than 1e-10 relative")


def test_negative_e_inside_the_support_is_visible_to_the_equation():
    """SOUNDNESS. Where the equation is ENFORCED, the abs() cannot hide a bad state.

    This is the counterpart to gate 1 and the reason the finding is scoped to
    EVALUATION rather than to the solver: `omega_of` on a sign-flipped state returns a
    plausible number, but `residual` on the same state is 13 decades above the clean one,
    and `solve`'s line search refuses the step outright.
    """
    print("\n[9] SOUNDNESS: e < 0 inside the support is caught by the residual")
    rp, b, Xc = _solved(0.3)
    bneg = b.copy()
    bneg[0] *= -1.0
    e_min = float(rp.e_of(bneg).min())
    om = float(rp.omega_of(bneg, np.array([0.5]))[0])
    res = float(np.max(np.abs(rp.residual(bneg, Xc))))
    clean = float(np.max(np.abs(rp.residual(b, Xc))))
    print(f"    min e at nodes {e_min:.4f} (<0); omega_of(0.5) = {om:.4e} (plausible)")
    print(f"    residual {res:.3e} vs clean {clean:.2e}  ({res / clean:.1e}x)")
    assert e_min < 0.0 and np.isfinite(om)
    assert res > 1e10 * clean, (res, clean)
    print("[ok] the evaluation path is silent but the equation path is 13 decades loud")


if __name__ == "__main__":
    test_clean_reference_selfcheck()
    test_characterize_profile_continues_past_its_own_support()
    test_characterize_out_of_support_value_mirrors_a_legitimate_one()
    test_characterize_even_cheb_clips_silently()
    test_characterize_defect_absorbs_nan_points()
    test_no_silent_absorption_of_finite_poison()
    test_no_silent_corruption_from_nan_coefficients()
    test_constructor_rejects_degenerate_a()
    test_solve_never_lies_about_convergence()
    test_negative_e_inside_the_support_is_visible_to_the_equation()
    print("\nAll leg-107 adversarial gates passed: 6 soundness gates hold, 4 "
          "characterization gates PIN the two escalated gaps (see "
          "experiments/journal/leg_107.md).")
