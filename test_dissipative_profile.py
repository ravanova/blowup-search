"""Tests for solver/dissipative_profile.py (leg 125, Route-M2P).

The load-bearing checks are the KNOWN-ANSWER GATES: Chen arXiv:1908.09385 eq (2.2) is an
EXACT closed-form solution of the steady equation this module discretises, so if the module's
residual does not annihilate it, every number downstream is void.  The second class of check
is the lesson-90 one: `diffusion_consistency` must be able to report values other than the one
this leg found, or it is a tautology of the code rather than a measurement.
"""

import numpy as np

from solver.dissipative_profile import (
    DissipativeProfile, chen_constants, chen_profile, diffusion_consistency,
    nu_decay_rate, radii_budget, y0_measure, z2_quadratic_constant,
)
from solver.gclm_family import GCLMResidual


# -- tiny harness (repo convention: test_*.py are self-running scripts, no pytest) --------

class _A:
    """`x == _A(y, abs=tol)` -- an approximate-equality sentinel."""

    def __init__(self, value, abs=1e-9):
        self.value = float(value)
        self.tol = float(abs)

    def __eq__(self, other):
        return abs(float(other) - self.value) <= self.tol

    def __repr__(self):
        return f"_A({self.value!r}, abs={self.tol!r})"


class _raises:
    def __init__(self, exc):
        self.exc = exc

    def __enter__(self):
        return self

    def __exit__(self, et, ev, tb):
        assert et is not None and issubclass(et, self.exc), \
            f"expected {self.exc.__name__}, got {et}"
        return True


# -- Chen's constants, as transcribed ---------------------------------------------------

def test_chen_constants_are_internally_exact():
    c = chen_constants()
    b = c["b"]["value"]
    assert b ** 2 == _A(0.375, abs=1e-15)          # Chen p.4: b^2 = 3/8
    assert c["b_squared"]["value"] == 0.375
    assert 1.0 / b ** 2 == _A(8.0 / 3.0, abs=1e-14)  # Chen p.5: ubar_x(0) = 8/3
    assert c["ubar_x_at_0"]["value"] == _A(8.0 / 3.0)
    assert c["c_l"]["value"] == _A(1.0 / 3.0)
    assert c["c_omega"]["value"] == -1.0
    assert c["gamma"]["value"] == 2.0
    # 2 c_l + c_omega is exactly Chen's (2.40) exponent bound of -1/3
    assert nu_decay_rate(c["c_l"]["value"], c["c_omega"]["value"]) == _A(-1.0 / 3.0)
    assert c["nu_decay_rate_exact"]["value"] == _A(-1.0 / 3.0)


def test_unquantified_constants_are_reported_as_unquantified_not_bounded():
    """Lesson 73: when a quantity has no referent, say so instead of bounding it."""
    c = chen_constants()
    assert c["delta"]["value"] is None
    assert c["nu_0"]["value"] is None
    assert "UNQUANTIFIED" in c["delta"]["provenance"]


def test_chen_is_recorded_as_analytic_not_a_cap_precedent():
    assert chen_constants()["computer_assisted"]["value"] is False


def test_gamma_tension_is_recorded_with_both_disjoint_ranges():
    """Leg 64's tension: gamma=|a|^-1 is Chen sec 1.2 for a <= -1 ONLY; a > -1 gives gamma=1."""
    c = chen_constants()
    assert "a <= -1" in c["critical_dissipation_a_le_minus1"]["provenance"]
    assert c["critical_dissipation_a_gt_minus1"]["value"] == 1.0
    assert "a > -1" in c["critical_dissipation_a_gt_minus1"]["provenance"]


# -- the closed form itself ---------------------------------------------------------------

def test_chen_profile_velocity_is_the_antiderivative_of_its_own_Ux():
    X = np.linspace(-6, 6, 20001)
    Om, Ux, U = chen_profile(X)
    assert U[np.argmin(np.abs(X))] == _A(0.0, abs=1e-12)
    num = np.gradient(U, X)
    inner = np.abs(X) < 5.5
    # np.gradient is 2nd-order, so the floor is O(h^2 |U'''|) ~ 1e-5 on this grid
    assert np.abs(num - Ux)[inner].max() < 1e-4


def test_chen_profile_is_odd():
    X = np.linspace(-8, 8, 4001)
    Om, _, _ = chen_profile(X)
    assert np.abs(Om + Om[::-1]).max() < 1e-14


# -- KNOWN-ANSWER GATE --------------------------------------------------------------------

def test_known_answer_gate_chen_closed_form_nulls_the_steady_residual():
    dp = DissipativeProfile(a=0.5, n=601)
    Om, _, _ = chen_profile(dp.X)
    R = dp.residual(Om, c_l=1.0 / 3.0, c_omega=-1.0, nu=0.0)
    assert np.sqrt(np.mean(R ** 2)) < 1e-5


def test_known_answer_gate_floor_converges_under_refinement():
    floors = []
    for n in (401, 601, 801):
        dp = DissipativeProfile(a=0.5, n=n)
        Om, _, _ = chen_profile(dp.X)
        floors.append(float(np.abs(dp.residual(Om, 1.0 / 3.0, -1.0, 0.0)).max()))
    assert floors[2] < floors[0]


def test_high_order_velocity_beats_the_banked_trapezoid_one():
    """The whole reason a new cumulative operator exists (lesson 86)."""
    n = 601
    dp = DissipativeProfile(a=0.5, n=n)
    base = GCLMResidual(a=0.5, n=n)
    Om, _, U = chen_profile(dp.X)
    new_err = float(np.abs(dp.VH @ Om - U).max())
    old_err = float(np.abs(base.velocity(Om) - U).max())
    assert new_err < old_err / 10.0


def test_residual_matches_the_banked_gclm_family_convention_at_nu_zero():
    """Cross-check against the module capabilities.py already registers."""
    n = 601
    dp = DissipativeProfile(a=0.5, n=n)
    base = GCLMResidual(a=0.5, n=n)
    Om, _, _ = chen_profile(dp.X)
    mine = dp.residual(Om, c_l=1.0 / 3.0, c_omega=-1.0, nu=0.0)
    theirs, _, _ = base.residual(Om, c_omega=-1.0, c_l=1.0 / 3.0)
    # same convention; they differ only by the quadrature/derivative order
    assert np.abs(mine - theirs).max() < 1e-3
    assert np.sqrt(np.mean(mine ** 2)) < np.sqrt(np.mean(theirs ** 2))


# -- the dissipation term must actually do something (negative control) --------------------

def test_nu_term_changes_the_residual():
    dp = DissipativeProfile(a=0.5, n=401)
    Om, _, _ = chen_profile(dp.X)
    r0 = dp.residual(Om, 1.0 / 3.0, -1.0, nu=0.0)
    r1 = dp.residual(Om, 1.0 / 3.0, -1.0, nu=1e-2)
    assert np.abs(r1 - r0).max() > 1e-4
    assert np.abs(r1 - r0 - 1e-2 * (dp.D2 @ Om)).max() < 1e-12


# -- diffusion_consistency: the lesson-90 controls -----------------------------------------

def test_diffusion_consistency_can_report_zero():
    """If it could not, it would be a tautology of the code, not a measurement."""
    assert diffusion_consistency(0.5, -1.0) == 0.0


def test_diffusion_consistency_varies_across_known_profiles():
    chen = diffusion_consistency(1.0 / 3.0, -1.0)
    clm = diffusion_consistency(1.0, -1.0)          # a=0 CLM anchor: c_l = 1, c_omega = -1
    heat = diffusion_consistency(0.5, -1.0)
    assert chen == _A(-1.0 / 3.0)
    assert clm == _A(1.0)
    assert len({round(chen, 9), round(clm, 9), round(heat, 9)}) == 3


def test_diffusion_consistency_is_gauge_invariant():
    """Invariant under (Omega, c_l, c_omega) -> (kappa c_l, kappa c_omega)."""
    base = diffusion_consistency(1.0 / 3.0, -1.0)
    for kappa in (0.25, 2.0, 17.0):
        assert diffusion_consistency(kappa / 3.0, -kappa) == _A(base, abs=1e-14)


def test_nu_decay_rate_is_NOT_gauge_invariant_and_that_is_documented():
    assert nu_decay_rate(2.0 / 3.0, -2.0) == _A(2.0 * nu_decay_rate(1.0 / 3.0, -1.0))


def test_diffusion_consistency_refuses_a_vanishing_amplitude_exponent():
    with _raises(ValueError):
        diffusion_consistency(0.5, 0.0)
    with _raises(ValueError):
        diffusion_consistency(0.5, float("nan"))


# -- Newton -------------------------------------------------------------------------------

def test_newton_recovers_chen_constants_as_outputs():
    """c_l is a free unknown and H Omega(0) is never imposed: both are predictions."""
    dp = DissipativeProfile(a=0.5, n=601)
    Om, _, _ = chen_profile(dp.X)
    gauge = float(dp.D[dp.i0] @ Om)
    out = dp.newton(Om * (1.0 + 0.05 * np.exp(-dp.X ** 2)), c_l0=0.30, c_omega=-1.0,
                    nu=0.0, scale_gauge=gauge, iters=15)
    assert out["residual_rms"] < 1e-12
    assert out["c_l"] == _A(1.0 / 3.0, abs=1e-4)
    assert float((dp.H @ out["Omega"])[dp.i0]) == _A(8.0 / 3.0, abs=1e-4)


def test_newton_converges_quadratically():
    dp = DissipativeProfile(a=0.5, n=401)
    Om, _, _ = chen_profile(dp.X)
    gauge = float(dp.D[dp.i0] @ Om)
    out = dp.newton(Om * (1.0 + 0.05 * np.exp(-dp.X ** 2)), 0.30, -1.0, 0.0,
                    scale_gauge=gauge, iters=15)
    h = out["history"]
    assert len(h) >= 3 and h[-1] < 1e-12
    assert h[2] < h[1] ** 1.5          # quadratic-ish contraction


# -- Y_0 / budget -------------------------------------------------------------------------

def test_y0_and_budget_shapes():
    dp = DissipativeProfile(a=0.5, n=401)
    Om, _, _ = chen_profile(dp.X)
    y0, defect = y0_measure(dp, Om, 1.0 / 3.0, -1.0, 0.0, norm="sup")
    assert y0 >= 0.0 and defect >= 0.0
    z2 = z2_quadratic_constant(dp, Om, 1.0 / 3.0, -1.0, 0.0, norm="sup")
    assert z2["Z2"] > 0.0
    b = radii_budget(1e-12, 0.0, 0.9156181325483919, z2["Z2"])
    assert set(("Y0_max", "closes", "r_min")).issubset(b)


def test_y0_measure_refuses_an_unknown_norm():
    dp = DissipativeProfile(a=0.5, n=201)
    Om, _, _ = chen_profile(dp.X)
    with _raises(ValueError):
        y0_measure(dp, Om, 1.0 / 3.0, -1.0, 0.0, norm="frobenius")


if __name__ == "__main__":
    import sys
    fns = [(k, v) for k, v in sorted(globals().items()) if k.startswith("test_")]
    order = [
        "test_chen_constants_are_internally_exact",
        "test_unquantified_constants_are_reported_as_unquantified_not_bounded",
        "test_chen_is_recorded_as_analytic_not_a_cap_precedent",
        "test_gamma_tension_is_recorded_with_both_disjoint_ranges",
        "test_chen_profile_velocity_is_the_antiderivative_of_its_own_Ux",
        "test_chen_profile_is_odd",
        "test_known_answer_gate_chen_closed_form_nulls_the_steady_residual",
        "test_known_answer_gate_floor_converges_under_refinement",
        "test_high_order_velocity_beats_the_banked_trapezoid_one",
        "test_residual_matches_the_banked_gclm_family_convention_at_nu_zero",
        "test_nu_term_changes_the_residual",
        "test_diffusion_consistency_can_report_zero",
        "test_diffusion_consistency_varies_across_known_profiles",
        "test_diffusion_consistency_is_gauge_invariant",
        "test_nu_decay_rate_is_NOT_gauge_invariant_and_that_is_documented",
        "test_diffusion_consistency_refuses_a_vanishing_amplitude_exponent",
        "test_newton_recovers_chen_constants_as_outputs",
        "test_newton_converges_quadratically",
        "test_y0_and_budget_shapes",
        "test_y0_measure_refuses_an_unknown_norm",
    ]
    assert sorted(order) == sorted(k for k, _ in fns), "test list drifted from the runner"
    for name in order:
        globals()[name]()
        print(f"[ok] {name}")
    print(f"\nALL DISSIPATIVE-PROFILE TESTS PASSED ({len(order)}/{len(order)})")
