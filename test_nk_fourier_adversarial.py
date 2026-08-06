"""Leg 140 / Route-NFA -- the banked adversarial battery for solver/nk_fourier.py.

Companion to test_nk_fourier.py, which gates the COMPLETENESS direction: six
known-answer predicates on well-formed input.  This file gates the SOUNDNESS
direction: what the module does when the input is NOT well formed.

READ-ONLY on the target.  solver/nk_fourier.py is not edited by this leg under
either branch of the gate (DIRECTION.md leg 140: yes -> escalate, do not patch).

TWO KINDS OF ASSERTION, and the difference is the whole point.

  HOLDS    a guard in this module that FIRES today.  These must keep passing
           forever.  They exist because of lesson 90: "there is no guard here" is
           only a measurement if some guard in the same module can be shown to
           come out the other way.  Four routines here do refuse
           (`tail_Z1_column` on k < 2, on the exact model's vanishing denominator
           and on an unknown model name; `tail_weight_obstruction` on k_lo = 1 and
           on an empty range; `weighted_ell1_op_norm` on a shape mismatch;
           `anchor` on N < 0).

  GAP-PIN  today's behaviour where the published theorem says the module should
           REFUSE.  Each such assertion pins the gap so that a future repair
           INVERTS it loudly rather than silently.  Every GAP-PIN carries the
           inversion instruction in its own message.

Nothing here is a claim of novelty: the novelty pass (writeup/novelty/leg_140.md)
established that the radii-polynomial constants are hypothesised positive in the
published theorem, that Galerkin truncation is textbook, that grey-box NaN/inf
auditing is published method, and that a weighted-ell^1 norm needs a positive
weight.  This file measures magnitudes on one module; that is all.

Run: .venv/bin/python test_nk_fourier_adversarial.py     (no pytest, ~1s)
"""

import math

import numpy as np

from solver.nk_fourier import (
    C_ANCHOR, anchor, kernel_directions, residual, jacobian, dc_column,
    gauged_system, ell1_op_norm, weighted_ell1_op_norm, radii_polynomial,
    tail_Z1_column, tail_weight_obstruction, n_modes_residual,
)

np.seterr(all="ignore")

INF = float("inf")
NAN = float("nan")

_PIN = ("GAP-PIN: this pins TODAY's behaviour, which the published theorem says "
        "should be a refusal. If a repair lands, this assertion must be INVERTED "
        "in the same commit, not deleted.")


# ---------------------------------------------------------------------------
# HOLDS -- the guards this module already has (lesson 90 positive controls)
# ---------------------------------------------------------------------------

def test_holds_existing_guards():
    """Four routines in this module DO refuse. They can come out the other way."""
    fired = []

    for k in (-5, 0, 1):
        try:
            tail_Z1_column(k)
            raise AssertionError(f"tail_Z1_column({k}) must refuse (documented k >= 2)")
        except ValueError as e:
            fired.append(f"tail_Z1_column(k={k}): {e}")

    try:
        tail_Z1_column(2, diag="exact")
        raise AssertionError("exact-diagonal model must refuse at its vanishing diagonal")
    except ValueError as e:
        fired.append(f"tail_Z1_column(2, exact): {e}")

    try:
        tail_Z1_column(5, diag="not_a_model")
        raise AssertionError("unknown diag model must refuse")
    except ValueError as e:
        fired.append(f"tail_Z1_column(diag=bad): {e}")

    try:
        tail_Z1_column(5, c=0.0)
        raise AssertionError("c = 0 must not return a number")
    except ZeroDivisionError as e:
        fired.append(f"tail_Z1_column(c=0): {e}")

    try:
        tail_weight_obstruction(lambda k: float(k), 1, 10)
        raise AssertionError("k_lo = 1 reaches u(0) = w(0)/0 and must not return")
    except ZeroDivisionError as e:
        fired.append(f"tail_weight_obstruction(k_lo=1): {e}")

    try:
        tail_weight_obstruction(lambda k: float(k), 10, 2)
        raise AssertionError("an empty k range must not return")
    except ValueError as e:
        fired.append(f"tail_weight_obstruction(empty): {e}")

    M = np.ones((3, 3))
    try:
        weighted_ell1_op_norm(M, np.ones(3), np.ones(4))
        raise AssertionError("a codomain weight of the wrong length must not broadcast")
    except ValueError as e:
        fired.append(f"weighted_ell1_op_norm(bad shape): {e}")

    try:
        anchor(-1)
        raise AssertionError("anchor(-1) must not return")
    except IndexError as e:
        fired.append(f"anchor(-1): {e}")

    assert len(fired) == 10, f"expected 10 guards to fire, got {len(fired)}"
    print(f"[ok] HOLDS: {len(fired)} guards in solver/nk_fourier.py fire on bad input")


def test_holds_admissible_inputs_are_right():
    """The module is correct where the theorem covers it -- the other control."""
    r = radii_polynomial(1e-3, 0.10, 0.20, 2.0)
    assert r["closes"] and 0 < r["r_min"] < r["r_max"], r
    assert abs(r["one_minus_Z"] - 0.7) < 1e-15
    # and it correctly REFUSES an admissible-but-non-closing tuple
    assert not radii_polynomial(1e-3, 0.6, 0.7, 2.0)["closes"], "1 - Z <= 0 must refuse"
    assert not radii_polynomial(0.5, 0.1, 0.2, 2.0)["closes"], "disc < 0 must refuse"

    # the weighted norm reproduces the unweighted one at w == 1
    rng = np.random.default_rng(140)
    M = rng.standard_normal((6, 5))
    assert abs(weighted_ell1_op_norm(M, np.ones(5), np.ones(6))
               - ell1_op_norm(M)) < 1e-12

    # the tail sandwich, the module's own headline
    for k in (3, 16, 1024):
        lo, hi = tail_Z1_column(k, diag="transport"), tail_Z1_column(k, diag="exact")
        assert lo <= 1.0 <= hi, f"k={k}: sandwich broken ({lo}, {hi})"
    # and it CAN report a value far from 1, so the sandwich is not a tautology
    sup, _, _ = tail_weight_obstruction(lambda k: float(np.exp(-k)), 2, 30)
    assert sup > 2.5, f"a decaying weight must report z_w >> 1, got {sup}"
    print(f"[ok] HOLDS: admissible inputs correct; the decaying-weight control "
          f"reports z_w = {sup:.4f} != 1, so the marginal 1.0 is not a tautology")


# ---------------------------------------------------------------------------
# GAP-PIN A -- radii_polynomial: the shared Y0/Z0/Z1 class (legs 79 / 98 / 116)
# ---------------------------------------------------------------------------

def test_gap_radii_polynomial_accepts_forbidden_constants():
    """Y0, Z0, Z1 >= 0 and Z2 > 0 finite are HYPOTHESES of the published theorem.

    `radii_polynomial` validates only Z2 > 0. This is the SAME guard class as
    port_certification (leg 79), interval_certificate (leg 98) and nk_bounds
    (leg 116) -- a fourth instance of a class leg 128's shared guard would absorb.
    """
    forbidden = {
        "Y0_negative_unit": (-1.0, 0.10, 0.20, 2.0),
        "Y0_negative_huge": (-1e6, 0.10, 0.20, 2.0),
        "Y0_negative_small": (-1e-3, 0.10, 0.20, 2.0),
        "Z0_negative": (1e-3, -1.0, 0.20, 2.0),
        "Z0_negative_large": (1e-3, -9.0, 0.20, 2.0),
        "Z1_negative": (1e-3, 0.10, -1.0, 2.0),
        "Z1_negative_large": (1e-3, 0.10, -9.0, 2.0),
        "Z0_and_Z1_negative": (1e-3, -1.0, -1.0, 2.0),
        "all_three_negative": (-1.0, -1.0, -1.0, 2.0),
    }
    closed = {k: radii_polynomial(*v) for k, v in forbidden.items()}
    n_close = sum(1 for r in closed.values() if r["closes"])
    assert n_close == 9, f"{_PIN} expected 9/9 forbidden tuples to close, got {n_close}"

    # the self-evident tell the module never checks: a NEGATIVE certified radius
    neg = {k: r["r_min"] for k, r in closed.items()
           if r["closes"] and r["r_min"] < 0}
    assert set(neg) == {"Y0_negative_unit", "Y0_negative_huge", "Y0_negative_small",
                        "all_three_negative"}, f"{_PIN} negative-radius set moved: {neg}"
    assert abs(neg["Y0_negative_huge"] - (-706.9318028416924)) < 1e-9, \
        f"{_PIN} sharpest negative radius moved: {neg['Y0_negative_huge']}"

    # NaN and inf ARE absorbed into a refusal -- report that, do not over-claim
    for lbl, args in (("Y0_nan", (NAN, 0.1, 0.2, 2.0)),
                      ("Z1_nan", (1e-3, 0.1, NAN, 2.0)),
                      ("Y0_inf", (INF, 0.1, 0.2, 2.0)),
                      ("Z2_nan", (1e-3, 0.1, 0.2, NAN))):
        assert not radii_polynomial(*args)["closes"], \
            f"{lbl} unexpectedly closes -- the NaN comparison guard has changed"
    print(f"[ok] GAP-PIN A: 9/9 forbidden (Y0,Z0,Z1) tuples close; 4 of them with a "
          f"NEGATIVE certified radius, worst r_min = {neg['Y0_negative_huge']:.6g}; "
          f"NaN/inf are correctly absorbed into a refusal")


def test_gap_certification_budget_inflates():
    """Y0_max is quoted by p2_route_d_dress.py as THE certification budget.

    It is (1 - Z0 - Z1)^2 / (4 Z2) with no check on Z0, Z1, so a forbidden negative
    pair inflates it quadratically.
    """
    base = radii_polynomial(0.0, 0.0, 0.0, 2.0)["Y0_max"]
    assert abs(base - 0.125) < 1e-15
    ladder = {(z0, z1): radii_polynomial(0.0, z0, z1, 2.0)["Y0_max"] / base
              for z0, z1 in [(-1.0, 0.0), (-1.0, -1.0), (-4.0, -4.0), (-9.0, -9.0)]}
    assert abs(ladder[(-1.0, 0.0)] - 4.0) < 1e-12, f"{_PIN} {ladder}"
    assert abs(ladder[(-1.0, -1.0)] - 9.0) < 1e-12, f"{_PIN} {ladder}"
    assert abs(ladder[(-9.0, -9.0)] - 361.0) < 1e-12, f"{_PIN} {ladder}"
    print(f"[ok] GAP-PIN A2: forbidden Z0 = Z1 = -9 inflates the certification "
          f"budget Y0_max by {ladder[(-9.0, -9.0)]:.0f}x")


# ---------------------------------------------------------------------------
# GAP-PIN B -- weighted_ell1_op_norm can return a NEGATIVE norm
# ---------------------------------------------------------------------------

def test_gap_weighted_norm_returns_negative():
    """ell^1(w) is defined only for w > 0. Nothing checks it, and the routine
    happily returns a negative number for a quantity that bounds a norm."""
    M = np.array([[1.0, 2.0, 0.5], [3.0, 4.0, 1.5], [0.25, 0.75, 2.0]])
    ones3 = np.ones(3)
    honest = weighted_ell1_op_norm(M, ones3, ones3)
    assert abs(honest - 6.75) < 1e-12, honest

    neg_dom = weighted_ell1_op_norm(M, -ones3, ones3)
    neg_cod = weighted_ell1_op_norm(M, ones3, -ones3)
    assert abs(neg_dom - (-4.0)) < 1e-12, f"{_PIN} negative-weight value {neg_dom}"
    assert abs(neg_cod - (-4.0)) < 1e-12, f"{_PIN} negative-cod value {neg_cod}"

    mixed = weighted_ell1_op_norm(M, np.array([1.0, -1.0, 1.0]), ones3)
    assert abs(mixed - 4.25) < 1e-12, f"{_PIN} mixed-sign value {mixed}"
    assert mixed < honest, "a mixed-sign weight UNDER-reports"

    # zero and non-finite weights are answered, not refused
    assert math.isinf(weighted_ell1_op_norm(M, np.zeros(3), ones3)), _PIN
    assert math.isnan(weighted_ell1_op_norm(M, np.full(3, NAN), ones3)), _PIN
    assert weighted_ell1_op_norm(M, np.full(3, INF), ones3) == 0.0, _PIN
    assert weighted_ell1_op_norm(M, ones3, np.zeros(3)) == 0.0, _PIN

    # on a matrix the MODULE ITSELF builds
    N = 8
    a = anchor(N).copy()
    a[4] += 1e-3
    _, J = gauged_system(a, C_ANCHOR, N)
    hp = weighted_ell1_op_norm(J, np.ones(N + 1), np.ones(N + 1))
    hn = weighted_ell1_op_norm(J, -np.ones(N + 1), np.ones(N + 1))
    assert abs(hp - 7.0) < 1e-12, hp
    assert abs(hn - (-1.251)) < 1e-9, f"{_PIN} in-module sign flip moved: {hn}"
    print(f"[ok] GAP-PIN B: weighted_ell1_op_norm returns {hn:.6g} on the module's own "
          f"gauged Jacobian where the honest norm is {hp:.6g}; a mixed-sign weight "
          f"under-reports 6.75 as 4.25; w = 0 gives inf, w = inf gives 0.0")


# ---------------------------------------------------------------------------
# GAP-PIN C -- ell1_op_norm on a 1-D array reads a VECTOR as a FUNCTIONAL
# ---------------------------------------------------------------------------

def test_gap_ell1_op_norm_shape_trap():
    """np.atleast_2d promotes a 1-D array to a ROW, so the routine returns
    max_k |v_k| where a caller holding a coefficient vector wants sum_k |v_k|.

    Both readings are correct for their own object and the routine signals
    nothing. Magnitude: exactly n on the flat vector.
    """
    for n in (2, 16, 256, 1024):
        v = np.ones(n)
        assert abs(ell1_op_norm(v) - 1.0) < 1e-15, _PIN
        assert abs(np.abs(v).sum() / ell1_op_norm(v) - n) < 1e-9, \
            f"{_PIN} under-report factor at n={n}"

    # on the vector the dress rehearsal actually forms for Y0
    N = 64
    a = anchor(N).copy()
    a[4] += 1e-3
    G, J = gauged_system(a, C_ANCHOR, N)
    v = np.linalg.inv(J) @ G
    correct, trapped = float(np.abs(v).sum()), ell1_op_norm(v)
    assert correct > trapped, _PIN
    ratio = correct / trapped
    assert 1.005 < ratio < 1.02, f"{_PIN} live Y0 under-report moved: {ratio}"

    # HOLDS half: on a genuine matrix it is exactly the max column sum
    rng = np.random.default_rng(3)
    Mx = rng.standard_normal((5, 4))
    assert abs(ell1_op_norm(Mx) - np.abs(Mx).sum(axis=0).max()) < 1e-15
    print(f"[ok] GAP-PIN C: ell1_op_norm under-reports the ell^1 norm of a 1-D "
          f"array by a factor n (up to 1024x on a flat vector, {ratio:.4f}x on the "
          f"live Y0 vector at N=64); it is exact on a 2-D matrix")


# ---------------------------------------------------------------------------
# GAP-PIN D -- tail_weight_obstruction cannot distinguish w from -w
# ---------------------------------------------------------------------------

def test_gap_weight_obstruction_off_hypothesis():
    """The docstring proves NO POSITIVE weight beats z_w = 1. Off that hypothesis
    the routine still answers.

    The negative-weight case is reported WITH its mechanism, not as a surprise:
    z_w = (u(k-1) + u(k+1)) / (2 u(k)) is homogeneous of DEGREE ZERO in w, so w and
    -w can never differ. That is a structural blind spot of the formula, and the
    honest way to state it (lesson 90) is as an identity, not as a coincidence.
    """
    pos, _, _ = tail_weight_obstruction(lambda k: float(k), 2, 200)
    neg, _, _ = tail_weight_obstruction(lambda k: -float(k), 2, 200)
    assert pos == 1.0, pos
    assert neg == pos, "degree-0 homogeneity: w and -w MUST agree"

    zero, _, _ = tail_weight_obstruction(lambda k: 0.0, 2, 20)
    assert math.isnan(zero), f"{_PIN} w == 0 gives {zero}"
    hole, _, _ = tail_weight_obstruction(lambda k: 0.0 if k == 5 else float(k), 2, 20)
    assert math.isinf(hole), f"{_PIN} a single zero weight gives {hole}"
    alt, _, _ = tail_weight_obstruction(lambda k: float(k) * (-1.0) ** k, 2, 20)
    assert abs(alt - (-1.0)) < 1e-12, f"{_PIN} sign-alternating weight gives {alt}"
    print(f"[ok] GAP-PIN D: a sign-alternating weight returns sup z_w = {alt:.4g} "
          f"(a NEGATIVE column weight) and a single zero weight returns inf, both "
          f"unflagged; w = -k returns {neg} identically to w = +k BY DEGREE-0 "
          f"HOMOGENEITY, which is a blind spot of the formula, not a coincidence")


# ---------------------------------------------------------------------------
# GAP-PIN E -- kernel_directions(1) breaks its own documented exactness
# ---------------------------------------------------------------------------

def test_gap_kernel_directions_truncate_silently():
    """`kernel_directions` docstring: "The two exact tangent directions ... Both are
    annihilated by the un-gauged [DF | dF/dc]".

    The dilation direction's second component sits at index 2 behind `if N >= 2`.
    At N = 1 it is silently dropped and the returned vector is NOT in the kernel,
    while the docstring still says it is. This is the one place in the module where
    truncation happens inside a routine documenting EXACTNESS -- the only kind of
    truncation this leg treats as a defect (Galerkin projection elsewhere is not).

    test_nk_fourier.py gate (3) checks this at N = 10 only.
    """
    def worst_residual(N):
        a = anchor(N)
        M = n_modes_residual(max(N, 1))
        J = jacobian(a, C_ANCHOR, M=M, n_cols=N + 1)
        dc = dc_column(a, M=M)
        return max(float(np.abs(J @ v + d * dc).max())
                   for v, d in kernel_directions(N)), J, dc

    w1, _, _ = worst_residual(1)
    assert abs(w1 - 0.0625) < 1e-15, f"{_PIN} N=1 kernel residual moved: {w1}"
    assert w1 / 1e-14 > 1e12, _PIN

    # N = 0 "passes" only because the whole operator is identically zero -- a
    # vacuous check, and saying so is the point (lesson 90).
    w0, J0, dc0 = worst_residual(0)
    assert w0 == 0.0 and np.abs(J0).max() == 0.0 and np.abs(dc0).max() == 0.0, \
        "N=0 annihilation must be vacuous, not a real pass"

    # N >= 2 is genuinely exact -- the control that comes out the other way
    for N in (2, 3, 5, 10, 40):
        wN, JN, _ = worst_residual(N)
        assert wN < 1e-14, f"N={N} must still be exact, got {wN}"
        assert np.abs(JN).max() > 0.0, f"N={N} operator must be non-trivial"

    # the same silent drop hits `anchor`: anchor(0) is NOT Omega_2
    a0 = anchor(0)
    assert a0.size == 1 and a0[0] == -0.5
    assert float(np.abs(residual(a0, C_ANCHOR)).max()) == 0.0, (
        "anchor(0)'s residual is 0 for the UNRELATED reason that every constant "
        "profile is an exact traveling wave -- a known-answer check that cannot fail")
    print(f"[ok] GAP-PIN E: kernel_directions(1) returns a vector with "
          f"|[DF|dF/dc] v|_sup = {w1:.4g}, i.e. {w1/1e-14:.3g}x the 1e-14 tolerance "
          f"its own known-answer gate uses at N = 10; N = 0 'passes' vacuously "
          f"(the operator is identically zero); N >= 2 is genuinely exact")


# ---------------------------------------------------------------------------
# GAP-PIN F -- the NaN fast-path in residual/jacobian
# ---------------------------------------------------------------------------

def test_gap_zero_coefficient_fast_path_cannot_skip_nan():
    """`if w == 0.0: continue` skips a vanishing contribution -- but it cannot skip
    w = inf * k * 0 = nan, so NaN is injected where the honest coefficient is
    exactly zero."""
    b = residual(np.zeros(7), INF)
    assert b.size == 12
    # Omega == 0 => F == 0 identically, so EVERY entry that is not exactly 0.0 is
    # manufactured by the fast path, not by the mathematics.
    manufactured = int((~(b == 0.0)).sum())
    assert manufactured == 7, f"{_PIN} manufactured-entry count moved: {manufactured}"
    assert int(np.isnan(b).sum()) == manufactured, "all of them are NaN"
    # the profile-side poison
    a = anchor(6).copy()
    a_nan = np.where(np.arange(7) == 3, NAN, a)
    bn = residual(a_nan, C_ANCHOR)
    Jn = jacobian(a_nan, C_ANCHOR, n_cols=7)
    assert int(np.isnan(bn).sum()) > 0 and int(np.isnan(Jn).sum()) > 0, \
        "NaN in the profile must propagate (it does; recorded, not a complaint)"
    print(f"[ok] GAP-PIN F: residual(0, c=inf) returns {manufactured} non-zero/NaN "
          f"entries of {b.size} where the honest answer is identically 0; a NaN "
          f"profile coefficient propagates into {int(np.isnan(bn).sum())}/{bn.size} "
          f"residual modes and {int(np.isnan(Jn).sum())}/{Jn.size} Jacobian entries")


# ---------------------------------------------------------------------------
# THE LOAD-BEARING CASE
# ---------------------------------------------------------------------------

def test_load_bearing_certified_ball_contains_no_zero():
    """One forbidden weight turns an honest REFUSAL into a certified ball that
    provably contains no zero of the module's own gauged system.

    Float64 throughout: a demonstration of the CODE's behaviour, not a proof about
    the operator.
    """
    N, c, delta = 8, C_ANCHOR, 1e-3
    a_star = anchor(N)
    x_hat = a_star.copy()
    x_hat[4] += delta
    dist = float(np.abs(x_hat - a_star).sum())

    G_star, _ = gauged_system(a_star, c, N)
    assert float(np.abs(G_star).sum()) == 0.0, "a_star must be an EXACT zero"

    G, J = gauged_system(x_hat, c, N)
    A_good = np.linalg.inv(J)
    A_bad = -A_good

    def const(A):
        return (float(np.abs(A @ G).sum()),
                ell1_op_norm(np.eye(N + 1) - A @ J),
                0.0,
                2.0 * ell1_op_norm(A))

    rp_good = radii_polynomial(*const(A_good))
    assert rp_good["closes"], "the honest certificate must close"
    assert dist <= rp_good["r_min"], "a_star must lie in the honest existence ball"

    Yb, Z0b, Z1b, Z2b = const(A_bad)
    assert abs(Z0b - 2.0) < 1e-12, Z0b
    assert not radii_polynomial(Yb, Z0b, Z1b, Z2b)["closes"], (
        "CONTROL: with the wrong inverse and an HONEST Z0 the module must refuse -- "
        "this is the assertion that can come out the other way")

    Z0_fab = weighted_ell1_op_norm(np.eye(N + 1) - A_bad @ J,
                                   -np.ones(N + 1), np.ones(N + 1))
    assert abs(Z0_fab - (-2.0)) < 1e-12, f"{_PIN} fabricated Z0 = {Z0_fab}"
    rp_fab = radii_polynomial(Yb, Z0_fab, Z1b, Z2b)
    assert rp_fab["closes"], f"{_PIN} the fabricated certificate must close today"

    r_f = rp_fab["r_min"]
    assert r_f <= rp_good["r_max"], "fabricated ball inside the uniqueness ball"
    assert dist > r_f, "fabricated ball must EXCLUDE the only zero"
    miss = (dist - r_f) / r_f
    assert abs(miss - 1.990135221338109) < 1e-9, f"{_PIN} miss margin moved: {miss}"
    print(f"[ok] LOAD-BEARING: honest Z0 = {Z0b:.6g} REFUSES; the same matrix through "
          f"weighted_ell1_op_norm with w_dom = -1 gives Z0 = {Z0_fab:.6g} and the "
          f"polynomial closes with r_min = {r_f:.6g}. The true zero sits at "
          f"{dist:.6g}, i.e. {dist/r_f:.4f} fabricated radii away, and the ball lies "
          f"inside the honest uniqueness ball -- so it contains NO zero, missing by "
          f"{miss:.4f} ball radii")


# ---------------------------------------------------------------------------
# LATENCY -- the finding's actual reach
# ---------------------------------------------------------------------------

def test_latency_live_callers_stay_clean():
    """Reproduce what the in-repo callers actually do, and confirm each stays in
    the region where the module is right. Every gap above is LATENT."""
    N, c = 16, C_ANCHOR
    a = anchor(N)
    G, J = gauged_system(a, c, N)
    A = np.linalg.inv(J)

    # p2_route_d_dress.py forms Y0 with the CORRECT ell^1 sum, not the shape trap
    b_full = residual(a, c)
    tail = float(sum(abs(b_full[m - 1]) / (c * m) for m in range(N + 1, b_full.size + 1)))
    Y0 = float(np.abs(A @ G).sum()) + tail
    Z0 = ell1_op_norm(np.eye(N + 1) - A @ J)
    n_extra = N + 2
    J_ext = jacobian(a, c, M=N, n_cols=N + 1 + n_extra)
    E = np.zeros((N + 1, n_extra))
    E[1:, :] = J_ext[:, N + 1:]
    Z1 = ell1_op_norm(A @ E) + tail_Z1_column(N + 1)
    Z2 = 2.0 * ell1_op_norm(A)
    for name, v in (("Y0", Y0), ("Z0", Z0), ("Z1", Z1), ("Z2", Z2)):
        assert v >= 0.0 and math.isfinite(v), f"live {name} = {v} is out of hypothesis"
    assert not radii_polynomial(Y0, Z0, Z1, Z2)["closes"], (
        "the module's banked structural negative must survive: the far field is "
        "exactly marginal, so 1 - Z0 - Z1 <= 0 at every truncation")
    print(f"[ok] LATENCY: the live dress-rehearsal path at N={N} produces "
          f"Y0={Y0:.3e}, Z0={Z0:.3e}, Z1={Z1:.6f}, Z2={Z2:.6f} -- all nonnegative "
          f"and finite, and the honest verdict is still 'does not close'. Every gap "
          f"pinned above is LATENT: no in-repo caller reaches one.")


if __name__ == "__main__":
    print("=" * 78)
    print("LEG 140 / ROUTE-NFA -- adversarial battery for solver/nk_fourier.py")
    print("  HOLDS   = a guard that fires today and must keep firing")
    print("  GAP-PIN = today's behaviour where the theorem says REFUSE; a repair")
    print("            must INVERT the assertion in the same commit")
    print("=" * 78)
    test_holds_existing_guards()
    test_holds_admissible_inputs_are_right()
    test_gap_radii_polynomial_accepts_forbidden_constants()
    test_gap_certification_budget_inflates()
    test_gap_weighted_norm_returns_negative()
    test_gap_ell1_op_norm_shape_trap()
    test_gap_weight_obstruction_off_hypothesis()
    test_gap_kernel_directions_truncate_silently()
    test_gap_zero_coefficient_fast_path_cannot_skip_nan()
    test_load_bearing_certified_ball_contains_no_zero()
    test_latency_live_callers_stay_clean()
    print("=" * 78)
    print("ALL PASS -- solver/nk_fourier.py NOT edited (gate says escalate, not patch)")
