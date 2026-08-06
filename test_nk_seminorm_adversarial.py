"""Leg 142 / Route-NSA: the adversarial battery for solver/nk_seminorm.py, PINNED.

The gate answered YES and, per its own instruction, the module was NOT patched.
These tests therefore pin the CURRENT (gap-carrying) behaviour, exactly as legs
100 and 115 pinned theirs: each gap-pin asserts the gap is still there, with the
magnitude in the message, so that

  * a future repair leg BREAKS these tests -- which is the signal that the repair
    landed, and the pin is then INVERTED (leg 130's template on the sibling
    module hilbert_pointwise.py, commit 5905138), and
  * nothing silently "fixes itself" without anyone noticing.

Gates 1-4 pin the four counted silent-corruption / fabrication-acceptance gaps.
Gate 5 pins the entry-point asymmetry.  Gate 6 is the POSITIVE CONTROL and is
the one test here that asserts correctness rather than a gap: the shipped
configuration must keep reproducing test_nk_seminorm.py's banked fixed point.  If
gate 6 fails, the harness is wrong and gates 1-5 mean nothing.

Run: PYTHONPATH=. python test_nk_seminorm_adversarial.py    (no scipy; ~40 s)
"""

import warnings

import numpy as np

from solver.nk_seminorm import (
    C_ANCHOR, hilbert_split_bound, hilbert_split_curves, interpolation_constant,
    holder_interpolation_bound, derivative_bound, seminorm_closure,
    operator_norm_upper, required_X0,
)

ALPHA, GAMMA = 1.5, 0.5
C_SUP_SHIPPED = 5.5543

# banked by test_nk_seminorm.py (5) and reproduced by this leg's runner
T_BANKED = 63.8213165652836
A_BANKED = 69.37561656528361


def _silent(fn):
    """(value, warning_names) -- asserts nothing was raised and nothing warned."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        value = fn()
    return value, sorted({w.category.__name__ for w in caught})


def test_1_negative_c_sup_gives_negative_norm_bound():
    """GAP-PIN 1: a negative C_sup yields a NEGATIVE claimed bound on ||A||."""
    curves = hilbert_split_curves(ALPHA, GAMMA)
    for C in (-1.0, -5.5543, -1.0e6):
        d, w = _silent(lambda C=C: seminorm_closure(ALPHA, GAMMA, C, curves=curves))
        assert w == [], f"C_sup={C} now warns {w} -- gap 1 may be repaired"
        assert d["closes"] is True, f"C_sup={C}: closes={d['closes']}"
        assert d["T_upper"] == 0.0, f"C_sup={C}: T={d['T_upper']}"
        assert d["A_upper"] == C, (
            f"C_sup={C}: A_upper={d['A_upper']}; an operator-norm UPPER BOUND "
            f"cannot be negative, and this one equals C_sup exactly")
        assert operator_norm_upper(ALPHA, GAMMA, C, curves=curves) == C
    # and the third, magnitude-dependent behaviour: a SMALL negative C_sup makes
    # (2S)**(1-gamma) complex, and the loop's own `nxt > T_cap` then raises.
    try:
        seminorm_closure(ALPHA, GAMMA, -1e-12, curves=curves)
    except TypeError as exc:
        assert "complex" in str(exc), str(exc)
    else:
        raise AssertionError("C_sup=-1e-12 no longer raises the complex TypeError")
    print("[pinned] 1  negative C_sup -> closes=True, T=0, A_upper=C_sup<0, silent; "
          "at -1e-12 the iterate goes COMPLEX and raises TypeError instead")


def test_2_negative_anchor_speed_deletes_the_seminorm_part():
    """GAP-PIN 2: c < 0 collapses ||A|| to its sup part, understating by 12.49x."""
    curves = hilbert_split_curves(ALPHA, GAMMA)
    ref, _ = _silent(lambda: seminorm_closure(ALPHA, GAMMA, C_SUP_SHIPPED,
                                              c=C_ANCHOR, curves=curves))
    assert abs(ref["A_upper"] - A_BANKED) < 1e-9
    for c in (-C_ANCHOR, -1.0, -1e-3):
        d, w = _silent(lambda c=c: seminorm_closure(ALPHA, GAMMA, C_SUP_SHIPPED,
                                                    c=c, curves=curves))
        assert w == [], f"c={c} now warns {w} -- gap 2 may be repaired"
        assert d["closes"] is True and d["T_upper"] == 0.0, (c, d)
        assert d["A_upper"] == C_SUP_SHIPPED, (c, d["A_upper"])
    factor = ref["A_upper"] / C_SUP_SHIPPED
    assert abs(factor - 12.490433819794324) < 1e-9, factor
    print(f"[pinned] 2  c=-0.5 -> A_upper={C_SUP_SHIPPED} vs {ref['A_upper']:.6f} at "
          f"c=+0.5: the claimed upper bound is understated {factor:.4f}x, silently")


def test_3_nan_is_absorbed_by_the_fixed_point_loop():
    """GAP-PIN 3: NaN in, closes=True and T_upper=NaN out; +inf is the control."""
    curves = hilbert_split_curves(ALPHA, GAMMA)
    for kw in ({"C_sup": float("nan")}, {"c": float("nan")}):
        args = {"C_sup": C_SUP_SHIPPED, "curves": curves}
        args.update(kw)
        d, w = _silent(lambda a=dict(args): seminorm_closure(ALPHA, GAMMA, **a))
        assert w == [], f"{kw} now warns {w} -- gap 3 may be repaired"
        assert d["closes"] is True, (kw, d)
        assert np.isnan(d["T_upper"]) and np.isnan(d["A_upper"]), (kw, d)
    # THE CONTROL, and it comes out differently: +inf and 1e300 take the T_cap
    # branch and are reported honestly. Only NaN slips through, because both loop
    # exits are comparisons that are False for NaN.
    for C in (float("inf"), 1e300):
        d, _ = _silent(lambda C=C: seminorm_closure(ALPHA, GAMMA, C, curves=curves))
        assert d["closes"] is False and "no fixed point" in d["reason"], (C, d)
    print("[pinned] 3  NaN C_sup/c -> closes=True with T_upper=NaN, silent; "
          "the +inf and 1e300 control DOES report closes=False honestly")


def test_4_required_x0_accepts_a_negative_contraction_constant():
    """GAP-PIN 4: Z1 < 0 passes `z <= target`, so found=True at the cheapest X0."""
    grid = [1e2, 1e3, 1e4, 1e5]
    d, w = _silent(lambda: required_X0(A_BANKED, lambda X0: -1.0, grid, target=1.0))
    assert w == [] and d["found"] is True and d["Z1"] < 0.0, d
    # the full fabricated chain: V1 feeds V4, and nothing warns at either link
    bad = seminorm_closure(ALPHA, GAMMA, -1.0,
                           curves=hilbert_split_curves(ALPHA, GAMMA))["A_upper"]
    chain, w2 = _silent(lambda: required_X0(bad, lambda X0: 1.0 / X0, grid,
                                            target=1.0))
    assert w2 == [] and chain["found"] is True and chain["Z1"] == -0.01, chain
    assert abs(chain["J_needed"] - 78.53981633974483) < 1e-9
    # control: NaN does NOT pass (z <= target is False for NaN), honest found=False
    nan_d, _ = _silent(lambda: required_X0(A_BANKED, lambda X0: float("nan"), grid))
    assert nan_d["found"] is False
    print("[pinned] 4  required_X0 accepts Z1=-69.38 as satisfying Z1<=1; chained "
          "with gap 1 it returns found=True, Z1=-0.01, J_needed=78.54, all silent")


def test_5_domain_is_enforced_at_one_entry_point_only():
    """GAP-PIN 5: seminorm_closure guards alpha/gamma; the other four do not."""
    # what IS enforced -- including this module's own stated gamma=1 exclusion,
    # which is the question leg 131 left open
    for bad_alpha in (0.8, 0.0, -1.0):
        try:
            seminorm_closure(bad_alpha, GAMMA, 1.0)
        except ValueError:
            pass
        else:
            raise AssertionError(f"alpha={bad_alpha} must be refused")
    for bad_gamma in (0.0, 1.0, 1.5, -0.5):
        try:
            seminorm_closure(ALPHA, bad_gamma, 1.0)
        except ValueError:
            pass
        else:
            raise AssertionError(f"gamma={bad_gamma} must be refused")
    # what is NOT enforced anywhere else
    v, w = _silent(lambda: derivative_bound(C_SUP_SHIPPED, 1.0, 0.5, GAMMA))
    assert w == [] and np.isfinite(v), (v, w)
    v, w = _silent(lambda: hilbert_split_bound(1.0, ALPHA, 1.0))
    assert w == [] and all(np.isfinite(x) for x in v), (v, w)
    for g in (-0.5, 1.5):
        c = interpolation_constant(g)
        assert isinstance(c, complex), (g, c)
        b, _ = holder_interpolation_bound(C_SUP_SHIPPED, 182.0, g)
        assert isinstance(b, complex), (g, b)
    print("[pinned] 5  seminorm_closure refuses alpha<1 and gamma outside (0,1) "
          "(its own gamma=1 exclusion IS enforced there); derivative_bound, "
          "hilbert_split_bound, interpolation_constant and "
          "holder_interpolation_bound refuse nothing -- the last two return "
          "COMPLEX 'bounds' for gamma outside [0,1]")


def test_6_positive_control_shipped_configuration_unmoved():
    """CONTROL (not a gap): the shipped configuration reproduces the banked numbers.

    This can come out differently -- it is the test that would catch a harness
    that perturbed the module. It asserts correctness, and it must keep passing
    after any future repair.
    """
    curves = hilbert_split_curves(ALPHA, GAMMA)
    d, w = _silent(lambda: seminorm_closure(ALPHA, GAMMA, C_SUP_SHIPPED,
                                            curves=curves))
    assert w == [] and d["closes"] is True
    assert abs(d["T_upper"] - T_BANKED) < 1e-9, (d["T_upper"], T_BANKED)
    assert abs(d["A_upper"] - A_BANKED) < 1e-9, (d["A_upper"], A_BANKED)
    assert 0.0 < d["contraction_slope"] < 1.0, d["contraction_slope"]
    # the fixed point really is one, re-derived here rather than trusted
    P = derivative_bound(d["C_sup"], d["T_upper"], ALPHA, GAMMA, curves=curves)
    back, kappa = holder_interpolation_bound(d["C_sup"], P, GAMMA)
    assert abs(back - d["T_upper"]) / d["T_upper"] < 1e-9
    assert abs(kappa - d["kappa_star"]) / d["kappa_star"] < 1e-9
    assert abs(interpolation_constant(0.5) - 2.0) < 1e-14
    # the truncated-grid sup understates: shipped n_X=120 against n_X=2000
    fine = seminorm_closure(ALPHA, GAMMA, C_SUP_SHIPPED,
                            curves=hilbert_split_curves(ALPHA, GAMMA, n_X=2000))
    rel = (fine["T_upper"] - d["T_upper"]) / fine["T_upper"]
    assert 0.0 < rel < 1e-3, rel
    print(f"[ok]     6  shipped config unmoved: T={d['T_upper']:.6f}, "
          f"A_upper={d['A_upper']:.6f}, slope={d['contraction_slope']:.6f}; "
          f"the n_X=120 sup understates the n_X=2000 value by {rel:.2e} relative")


if __name__ == "__main__":
    test_1_negative_c_sup_gives_negative_norm_bound()
    test_2_negative_anchor_speed_deletes_the_seminorm_part()
    test_3_nan_is_absorbed_by_the_fixed_point_loop()
    test_4_required_x0_accepts_a_negative_contraction_constant()
    test_5_domain_is_enforced_at_one_entry_point_only()
    test_6_positive_control_shipped_configuration_unmoved()
    print("\nALL NK-SEMINORM ADVERSARIAL PINS HOLD "
          "(4 silent gaps pinned, 1 entry-point asymmetry pinned, control green)")
