"""Adversarial battery for `solver/finite_support.py` (leg 124, Route-FSA).

THE GATE (DIRECTION.md, leg 124), answered **YES**:

    "Under an adversarial battery of degenerate or poisoned inputs, does
     solver/finite_support.py ever silently return a wrong result instead of flagging the
     input?"

THE MODULE UNDER AUDIT IS DEAD CODE, and every finding below is about a file that is not on
any path the rest of the repository runs. `solver/finite_support.py`'s own docstring opens
`STATUS: SUPERSEDED by solver/first_integral.py (Route-D v14).  DO NOT USE.` and
`WORK IN PROGRESS -- DOES NOT CONVERGE YET. NO TEST FILE. DO NOT USE.`; `capabilities.py`
lists it `"SUPERSEDED -- do not use"`, `"validated": "nothing"`; a repo-wide grep for a
non-test import of the module returns zero hits. **No banked physics number anywhere in this
repository is at risk from anything pinned here.**

READ THIS BEFORE CHANGING ANYTHING HERE. Every check below is marked `PIN:` and states what
correct behaviour would look like. They PIN CURRENT, DEFECTIVE BEHAVIOUR deliberately (leg 66's
precedent, reused by legs 92, 99, 120): a leg whose territory is read-only on `solver/` reports
and pins a defect rather than repairing it silently, so it cannot drift unnoticed and a future
repair has an exact target. THEY MUST NOT BE WEAKENED, and passing today is not an endorsement.

THREE MECHANISMS PINNED HERE (magnitudes, measured by
experiments/p2_route_fsa_v1_adversarial.py, banked in
writeup/data/p2_route_fsa_v1_adversarial.json):

  F1  `FiniteSupportProfile.solve()` reports `converged: True` at machine-precision residual
      for degenerate `K`, because its own residual is measured ONLY at its own `K - 1`
      collocation nodes -- which is EMPTY at `K = 1`. The same `(b, Xc)` evaluated at an
      independent, disjoint set of interior points shows the actual PDE residual off by many
      orders of magnitude (K=1, a=0.5: reported 5.55e-17, independent 3.30e-01). 14/27
      (K, a) combinations tested are silent by this criterion.

  F2  Newton collapses onto the trivial, zero-measure root `Xc -> 0` for `|c|` below ~1e-9
      (holding the module's own default `a`), across three `a` values, both signs of `c`, and
      the exact point `c = 0.0`. `converged: True` is reported for a "finite-support profile"
      with no support. 30/57 (a, c) combinations tested are silent by this criterion. The
      transition is sharp and reproducible: silent at `|c| <= 1e-9`, not silent at
      `|c| >= 1e-8`.

  F3  `FiniteSupportOps.fields` treats out-of-domain `v > 1` three different ways in the same
      call: `U` (`np.interp`) SILENTLY CLAMPS to the `v=1` boundary value for every `a` tested
      (NumPy's own documented default -- https://numpy.org/doc/stable/reference/generated/numpy.interp.html
      -- the module adds no range guard of its own); `f`'s weight power is evaluated on the
      RAW, unclipped `v` and is silently finite and wrong whenever `p = 1/a` happens to land on
      an exact integer (6/6 cases where `p` is an integer); `H` alone reliably goes non-finite
      via its `log(v/(1-v))` term. All 6 out-of-domain `a` values tested produce at least one
      silent field.

CONTROLS, RECORDED AS LOUDLY AS THE FINDINGS. `a=0`, `K=0`, `K<0`, `N=0`, `max_iter=0` all
raise; `a` = NaN/Inf/negative propagates NaN through and reports `converged: False`, never a
false success. None of these six is silent, and they stay pinned as passes so a future change
that makes any of them silent is caught.

Run: .venv/bin/python test_finite_support_adversarial.py
"""

import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from experiments.p2_route_fsa_v1_adversarial import (   # noqa: E402
    OFFNODE_TOL,
    _independent_offnode_residual,
    _isolated_weight_power_warnings,
)
from solver.finite_support import (                     # noqa: E402
    FiniteSupportOps,
    FiniteSupportProfile,
    cheb_quad,
)


# ==========================================================================
# F1 -- PIN: degenerate K reports false convergence
# ==========================================================================

def test_pin_K1_zero_collocation_nodes_reports_false_convergence():
    """PIN: K=1 has ZERO collocation nodes (`self.v` is empty), so `ops.residual` is never
    evaluated even once, yet `solve()` reports `converged: True` at machine precision.

    CORRECT behaviour: `solve()` should refuse (raise, or set `converged: False`) whenever the
    collocation node count is too small to constrain the system at all, or at minimum should
    cross-check its own residual against points other than the ones it chose."""
    prof = FiniteSupportProfile(a=0.5, K=1, N=2000, c=0.5)
    assert prof.v.size == 0, "K=1 no longer has zero collocation nodes -- update this pin"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = prof.solve(max_iter=60)
    off = _independent_offnode_residual(0.5, 1, 0.5, r["b"], r["Xc"])
    print(f"    K=1: reported converged={r['converged']}, reported residual={r['residual']:.3e}, "
          f"independent off-node residual={off['max_abs']:.3e}")
    assert r["converged"] is True, "K=1 no longer reports false convergence -- update this pin"
    assert r["residual"] < 1e-10, "the reported residual is no longer near machine precision"
    assert off["max_abs"] > OFFNODE_TOL, (
        "the independent off-node residual is no longer large -- if this genuinely repaired "
        "itself, DELETE this pin, do not weaken it")
    print("[ok] PINNED: K=1 reports converged=True while the PDE is unconstrained off its "
          "own (empty) collocation set")


def test_pin_degenerate_K_false_convergence_battery():
    """PIN: the K=1 case is not isolated -- K in {2, 4} also report false convergence at most
    of the three `a` values tested (8/9 total across K in {1,2,4}), by the SAME mechanism (too
    few collocation rows to constrain the physics), even though their node count is nonzero."""
    silent = []
    for a in (0.3, 0.5, 0.8):
        for K in (1, 2, 4):
            prof = FiniteSupportProfile(a=a, K=K, N=2000, c=0.5)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                r = prof.solve(max_iter=60)
            off = _independent_offnode_residual(a, K, 0.5, r["b"], r["Xc"])
            if r["converged"] and off["all_finite"] and off["max_abs"] > OFFNODE_TOL:
                silent.append((a, K, r["residual"], off["max_abs"]))
    print(f"    silent (a, K, reported_residual, offnode_residual): {silent}")
    assert len(silent) >= 8, (
        "fewer than 8/9 silent (a, K) combinations at K in {1,2,4} -- if this genuinely "
        "improved, DELETE or narrow this pin, do not weaken the assertion silently")
    print(f"[ok] PINNED: {len(silent)}/9 degenerate-K cases at K in {{1,2,4}} report false "
          f"convergence")


def test_control_K0_raises():
    """CONTROL (not a defect): K=0 raises IndexError -- flagged, not silent."""
    try:
        FiniteSupportProfile(a=0.5, K=0, N=200, c=0.5).solve(max_iter=5)
        raise AssertionError("K=0 no longer raises -- this MUST be re-audited as a possible "
                              "NEW silent-corruption case, not silently accepted")
    except IndexError:
        print("[ok] K=0 raises IndexError (flagged, not silent)")


def test_control_K_negative_raises():
    """CONTROL (not a defect): K<0 raises ValueError -- flagged, not silent."""
    try:
        FiniteSupportProfile(a=0.5, K=-3, N=200, c=0.5)
        raise AssertionError("K=-3 no longer raises -- re-audit as a possible new gap")
    except ValueError:
        print("[ok] K=-3 raises ValueError (flagged, not silent)")


# ==========================================================================
# F2 -- PIN: near-zero c collapses to the trivial zero-radius root
# ==========================================================================

def test_pin_near_zero_c_collapses_to_trivial_root():
    """PIN: for |c| <= 1e-9 (a=0.5), Newton converges to Xc essentially 0 -- a zero-measure
    "finite-support profile" -- and reports full success.

    CORRECT behaviour: `solve()` should distinguish a genuine small-support solution from the
    algebraically trivial root `Xc = 0` (e.g. by rejecting `Xc` below some floor, or by
    checking that the profile carries nonzero mass)."""
    results = {}
    for c in (1e-9, 1e-10, 1e-14, 0.0, -1e-9):
        prof = FiniteSupportProfile(a=0.5, K=24, N=2000, c=c)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = prof.solve(max_iter=60)
        results[c] = r
        print(f"    c={c:.1e}: converged={r['converged']}, residual={r['residual']:.3e}, "
              f"Xc={r['Xc']:.3e}")
    for c, r in results.items():
        assert r["converged"] is True, f"c={c:.1e} no longer reports converged=True"
        assert abs(r["Xc"]) < 1e-6, f"c={c:.1e} no longer collapses to a trivial Xc"
    print("[ok] PINNED: |c| <= 1e-9 collapses to the trivial zero-radius root and reports "
          "converged=True")


def test_pin_collapse_boundary_is_sharp():
    """PIN: the transition is sharp -- |c| = 1e-8 does NOT collapse (correctly reports
    converged=False), while |c| = 1e-9 does (silently). This pins the exact boundary so a
    partial repair that only moves it can be measured against a fixed reference."""
    prof8 = FiniteSupportProfile(a=0.5, K=24, N=2000, c=1e-8)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r8 = prof8.solve(max_iter=60)
    prof9 = FiniteSupportProfile(a=0.5, K=24, N=2000, c=1e-9)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r9 = prof9.solve(max_iter=60)
    print(f"    c=1e-8: converged={r8['converged']} (should be False)")
    print(f"    c=1e-9: converged={r9['converged']} (should be True -- the silent case)")
    assert r8["converged"] is False, "c=1e-8 now also reports converged=True -- boundary moved"
    assert r9["converged"] is True, "c=1e-9 no longer silently converges -- update this pin"
    print("[ok] PINNED: collapse boundary sits between |c|=1e-9 (silent) and |c|=1e-8 (flagged)")


def test_control_a_zero_raises():
    """CONTROL (not a defect): a=0.0 raises ZeroDivisionError -- flagged, not silent."""
    try:
        FiniteSupportProfile(a=0.0, K=8, N=200, c=0.5)
        raise AssertionError("a=0.0 no longer raises -- re-audit as a possible new gap")
    except ZeroDivisionError:
        print("[ok] a=0.0 raises ZeroDivisionError (flagged, not silent)")


def test_control_nonfinite_a_propagates_never_false_success():
    """CONTROL (not a defect): a = NaN/Inf/negative propagates NaN through every downstream
    field and reports converged=False -- never a false success."""
    for a in (-0.5, float("nan"), float("inf"), -float("inf")):
        prof = FiniteSupportProfile(a=a, K=8, N=500, c=0.5)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = prof.solve(max_iter=10)
        assert r["converged"] is False, f"a={a!r} now reports converged=True -- re-audit"
        assert not np.isfinite(r["residual"]), f"a={a!r} now has a finite residual -- re-audit"
    print("[ok] a in {-0.5, nan, inf, -inf}: NaN propagates, converged=False always (control)")


def test_control_N_zero_raises():
    """CONTROL (not a defect): N=0 raises ZeroDivisionError (both directly in `cheb_quad`
    and through the `FiniteSupportProfile` constructor) -- flagged, not silent."""
    try:
        cheb_quad(0)
        raise AssertionError("cheb_quad(0) no longer raises")
    except ZeroDivisionError:
        pass
    try:
        FiniteSupportProfile(a=0.5, K=8, N=0, c=0.5)
        raise AssertionError("N=0 via FiniteSupportProfile no longer raises")
    except ZeroDivisionError:
        pass
    print("[ok] N=0 raises ZeroDivisionError, both directly and via FiniteSupportProfile "
          "(flagged, not silent)")


def test_control_max_iter_zero_raises():
    """CONTROL (not a defect, but not graceful either): max_iter=0 raises IndexError on an
    empty history list rather than returning a sensible result. It still FAILS LOUDLY, which
    is what this pin cares about, but a future leg with edit authority could make this a
    clean, documented error instead of an incidental IndexError."""
    try:
        FiniteSupportProfile(a=0.5, K=8, N=200, c=0.5).solve(max_iter=0)
        raise AssertionError("max_iter=0 no longer raises")
    except IndexError:
        print("[ok] max_iter=0 raises IndexError (flagged, not silent, if inelegantly)")


# ==========================================================================
# F3 -- PIN: out-of-domain v silently clamps (U) or extrapolates (f, when p is an integer)
# ==========================================================================

def test_pin_U_silently_clamps_outside_domain():
    """PIN: `FiniteSupportOps.fields`'s `U` (Utilde, via `np.interp`) silently clamps to the
    v=1 boundary value for ANY v > 1, with zero warnings, for every `a` tested. This is
    `np.interp`'s documented default (no `left`/`right` override is passed), but
    `FiniteSupportOps` adds no domain check of its own before calling it.

    CORRECT behaviour: reject or warn on `v_eval` outside [0, 1] in `FiniteSupportOps.__init__`,
    or pass `left=nan, right=nan` to `np.interp` so an out-of-range query is at least as loud as
    the sibling field `H` already is."""
    K = 8
    b = np.zeros(K)
    b[0] = 1.0
    v_out = np.array([1.5, 2.0, 50.0])
    for a in (0.5, 0.3, 1.0):
        p = 1.0 / a
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            ops = FiniteSupportOps(p, K, v_out, N=500, n_int=200)
            ops.a = a
            f, df, H, U = ops.fields(b)
            ops_edge = FiniteSupportOps(p, K, np.array([1.0]), N=500, n_int=200)
            ops_edge.a = a
            _, _, _, U_edge = ops_edge.fields(b)
        print(f"    a={a}: U(v>1)={U}, U(v=1)={U_edge[0]:.6f}, H finite={np.isfinite(H).all()}")
        assert np.isfinite(U).all(), f"a={a}: U is no longer silently finite outside [0,1]"
        assert np.allclose(U, U_edge[0], atol=1e-13), (
            f"a={a}: U no longer clamps to the v=1 boundary value -- update this pin")
        assert not np.isfinite(H).all(), (
            f"a={a}: H no longer flags the same out-of-domain input -- re-derive the contrast")
    print("[ok] PINNED: U clamps silently to the v=1 boundary value for v > 1, at every `a` "
          "tested, while H correctly goes non-finite on the identical input")


def test_pin_f_silently_extrapolates_when_p_is_integer():
    """PIN: `f`'s weight power `(1 - v**2)**p` (solver/finite_support.py:176) is evaluated on
    the RAW, unclipped `v`, not the clipped angle `even_cheb` uses for the polynomial part.
    When `p = 1/a` is an exact integer, a negative base to an integer power is well-defined and
    the module returns a finite, wrong, UNWARNED extrapolated value. When `p` is not an
    integer, the SAME line instead raises RuntimeWarning and returns NaN -- so whether this is
    silent or loud is an arithmetic coincidence of `a`, not a property of whether v was valid."""
    v_out = np.array([1.5, 2.0, 50.0])
    integer_p_cases = [(0.5, 2), (1.0, 1), (0.25, 4), (1.0 / 3.0, 3)]
    fractional_p_cases = [(0.3, 10.0 / 3.0), (0.7, 10.0 / 7.0)]

    for a, p_expected in integer_p_cases:
        p = 1.0 / a
        assert abs(p - round(p)) < 1e-9, f"a={a} no longer gives an integer p -- update the case"
        wv, n_warn = _isolated_weight_power_warnings(p, v_out)
        print(f"    a={a} (p={p:.3f}, integer): wv={wv}, warnings={n_warn}")
        assert np.isfinite(wv).all(), f"a={a}: the weight power is no longer silently finite"
        assert n_warn == 0, f"a={a}: the weight power now warns -- update this pin"

    for a, p_approx in fractional_p_cases:
        p = 1.0 / a
        wv, n_warn = _isolated_weight_power_warnings(p, v_out)
        print(f"    a={a} (p={p:.3f}, fractional): wv={wv}, warnings={n_warn}")
        assert not np.isfinite(wv).all(), f"a={a}: fractional p no longer goes non-finite"
        assert n_warn > 0, f"a={a}: fractional p no longer warns"

    print("[ok] PINNED: f's weight power is silently finite-and-wrong outside [0,1] iff "
          "p = 1/a is an exact integer; otherwise it correctly warns and goes non-finite")


def test_control_v_in_domain_is_unaffected():
    """CONTROL (not a defect): in-domain evaluation points are completely unaffected by the
    domain-violation mechanism above -- a regression here would mean the pin itself is broken,
    not the module."""
    K = 8
    b = np.zeros(K)
    b[0] = 1.0
    v_in = np.array([0.1, 0.3, 0.5, 0.7, 0.9])
    for a in (0.5, 0.3):
        p = 1.0 / a
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            ops = FiniteSupportOps(p, K, v_in, N=500, n_int=200)
            ops.a = a
            f, df, H, U = ops.fields(b)
        assert np.isfinite(f).all() and np.isfinite(H).all() and np.isfinite(U).all(), (
            f"a={a}: in-domain evaluation is no longer all-finite")
    print("[ok] in-domain evaluation points (v in [0,1]) are unaffected (control)")


if __name__ == "__main__":
    tests = [
        test_pin_K1_zero_collocation_nodes_reports_false_convergence,
        test_pin_degenerate_K_false_convergence_battery,
        test_control_K0_raises,
        test_control_K_negative_raises,
        test_pin_near_zero_c_collapses_to_trivial_root,
        test_pin_collapse_boundary_is_sharp,
        test_control_a_zero_raises,
        test_control_nonfinite_a_propagates_never_false_success,
        test_control_N_zero_raises,
        test_control_max_iter_zero_raises,
        test_pin_U_silently_clamps_outside_domain,
        test_pin_f_silently_extrapolates_when_p_is_integer,
        test_control_v_in_domain_is_unaffected,
    ]
    for t in tests:
        print(f"\n{t.__name__}")
        t()
    print(f"\nAll {len(tests)} leg-124 adversarial checks passed "
          f"(gate answers YES: solver/finite_support.py silently returns wrong results on "
          f"degenerate K, near-zero c, and out-of-domain v -- escalated, not patched; the "
          f"module is dead code with zero non-test importers).")
