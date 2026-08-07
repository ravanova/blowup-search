"""Adversarial gates for `solver/dissipative_profile.py` (leg 207, Route-DPA).

`test_dissipative_profile.py` (leg 125's own, 20 tests) validates the module on WELL-FORMED
input: Chen's constants are internally exact, the profile is odd, the closed form nulls the
steady residual, the floor converges under refinement, the 4th-order velocity beats the banked
trapezoid, `nu` changes the residual, `newton` recovers Chen's constants and converges
quadratically, and `diffusion_consistency` is gauge-invariant and *can report zero*. Eighteen
of those twenty inputs are legal and in-domain; exactly two are guard tests. This file
validates the other half -- what the module does when the input is NOT well formed -- and banks
leg 207's battery so the answer cannot silently regress.

The gate leg 207 answered, verbatim:

  "Under adversarial and degenerate inputs (including parameters bracketing leg 185's own
   measured `a* = 0.3865` sign-flip boundary), does `dissipative_profile.py` ever silently
   return a wrong value rather than reject or visibly propagate the defect?"

Answered **YES**, on four independent sites. `solver/dissipative_profile.py` was NOT edited --
leg 207 had no patch authority under its own gate, so all four findings are PINNED here rather
than repaired. All four are **LATENT**: every landed call site in leg 125's runner, leg 187's
certificate substrate and leg 125's own test file avoids all four mechanisms, and leg 185
cannot reach two of them at all (it imports only `DissipativeProfile` and `chen_profile`). So
**no recorded number moves**.

WHAT "TRUE" MEANS HERE, AND WHERE IT COMES FROM
------------------------------------------------
Not this leg's invention -- each reference is the module's OWN documented contract:

  * module header: "`Delta` is measured here, not assumed: `newton_profile` solves for `c_l`
    and it is free to land anywhere."
  * `newton` docstring: "`scale_gauge` (the value of `Omega_X(0)`) kills the second [symmetry].
    `c_l` is then a genuine OUTPUT -- the whole point, since `Delta` is built from it."
  * `newton_gamma2` docstring: "...asks whether (i) can then be solved at a given `nu > 0`,
    with the advection `a` as the free unknown."
  * `y0_measure`: `raise ValueError(f"unknown norm {norm!r}: use 'sup' or 'l1'")`, gated by
    leg 125's own `test_y0_measure_refuses_an_unknown_norm`. `z2_quadratic_constant` takes the
    same argument in the same file.

PRIOR ART, CREDITED (gate 13). The collapse of `newton_gamma2` to `Omega == 0` at `nu = 1.0`
is **leg 185's** finding, not this leg's -- its journal banks `a = -10.092461405320627` and
`residual_relative = 5.485652392436699` and names "collapse to Omega == 0" outright. Gate 13
reproduces both numbers as an independent check and does not claim them. What leg 207 adds is
the *converse* sharpening: leg 185's D3 states that "`newton`, the other routine in the same
module, DOES impose it (`scale_gauge`)" -- gates 6 and 8 measure that this protection is
conditional on the caller, not a property of the routine.

TWO KINDS OF GATE LIVE IN THIS FILE, AND THEY MUST NOT BE CONFUSED
-------------------------------------------------------------------
1. SOUNDNESS gates (`test_guard_*`, `test_latency_*`). These assert a property that HOLDS.
   If one fails, the module has started absorbing bad input somewhere it previously rejected
   it, or a banked number has become exposed.

2. CHARACTERIZATION gates (`test_pinned_*`). These assert the CURRENT, WRONG behaviour, so a
   later repair leg is forced to come back and update this file deliberately. A failure here
   is not necessarily bad news -- it may mean the defect was fixed. Each one names the repair
   that would flip it, and none may be "fixed" by loosening a tolerance.

Self-running, no pytest: `.venv/bin/python test_dissipative_profile_adversarial.py`. ~50 s.
The canonical full-fidelity measurement is the runner's, not this file's: every magnitude
quoted in `experiments/journal/leg_207.md` comes from
`writeup/data/p2_route_dpa_v1_adversarial.json`.
"""

import ast
import os

import numpy as np

from solver.dissipative_profile import (
    DissipativeProfile, chen_profile, diffusion_consistency, radii_budget,
    y0_measure, z2_quadratic_constant, _drho_matrix4, _cumint_matrix4,
)

ROOT = os.path.dirname(os.path.abspath(__file__))
# [PROVENANCE POINTER ADDED 2026-08-07 BY LEG 283 (Route-M2SR) -- comment only; the value,
#  every assertion and every threshold in this file are UNCHANGED.  A_STAR is a bracketing
#  INPUT to the battery, never a claim.  Per leg 210 (parked leg/210-m2sv-v1 @ 6e06880):
#  (i) 0.3864963972206034 is leg 125's / Route-M2P's value (Delta(a) sweep at nu = 0, rel.
#  residual 1.933e-15), not leg 185's own measurement; (ii) leg 185's claim that its nu(a)
#  crossing LANDS ON it is UNPINNED -- its own two starts straddle zero at a = 0.3865
#  (+0.00000035 / -0.00425080) and leg 210's independent bracket is [0.36, 0.37].  The SIGN
#  FLIP is confirmed and is gauge-independent (nu -> mu^2 nu, mu^2 > 0), so the region
#  bracketed here is real.  Index: writeup/CORRECTIONS.md #9.]
A_STAR = 0.3864963972206034      # leg 185's measured sign-flip boundary
A_MODULE, A0_M7 = 0.39, 0.386    # leg 125's M7 setup
C_L_IMPOSED, C_OMEGA = 0.5, -1.0
N = 201                          # battery grid; the runner re-confirms at 401 and 801


def _fresh(a=0.5, n=N):
    dp = DissipativeProfile(a=a, n=n)
    Om, _, _ = chen_profile(dp.X)
    return dp, Om


def _gauge(dp, Om):
    return float(dp.D[dp.i0] @ Om)


# ===========================================================================
# SOUNDNESS GATES -- guards that DO fire (lesson 90: the battery must be two-sided)
# ===========================================================================

def test_guard_diffusion_consistency_refuses_a_degenerate_amplitude_exponent():
    """`Delta` has no referent when `c_omega` vanishes or is not finite; the module says so."""
    n_raised = 0
    for bad in (0.0, float("nan"), float("inf"), -float("inf")):
        try:
            diffusion_consistency(0.5, bad)
        except ValueError:
            n_raised += 1
    print(f"[1] SOUNDNESS: diffusion_consistency rejects {n_raised}/4 degenerate c_omega")
    assert n_raised == 4, "the module's own documented c_omega guard has regressed"


def test_guard_y0_measure_refuses_an_unknown_norm():
    """The sibling of gate 7's defect. This one is guarded; gate 7 pins that the other is not."""
    dp, Om = _fresh()
    n_raised = 0
    for bad in ("frobenius", "L1", "sup ", "2"):
        try:
            y0_measure(dp, Om, 1.0 / 3.0, C_OMEGA, 0.0, norm=bad)
        except ValueError:
            n_raised += 1
    print(f"[2] SOUNDNESS: y0_measure rejects {n_raised}/4 unrecognised norms")
    assert n_raised == 4, "y0_measure's norm guard has regressed"


def test_guard_nan_and_inf_propagate_visibly_and_are_not_absorbed():
    """NaN/Inf in `nu`, in `Omega0`, or in `scale_gauge` must never yield a quiet finite answer."""
    dp, Om = _fresh()
    for bad in (float("nan"), float("inf")):
        R = dp.residual(Om, 1.0 / 3.0, C_OMEGA, bad)
        assert not np.all(np.isfinite(R)), f"nu={bad} was silently absorbed by residual()"
        try:
            dp.newton(Om.copy(), c_l0=1.0 / 3.0, c_omega=C_OMEGA, nu=bad, iters=5)
            raise AssertionError(f"newton returned quietly on nu={bad}")
        except np.linalg.LinAlgError:
            pass
    Omb = Om.copy()
    Omb[5] = float("nan")
    try:
        dp.newton(Omb, c_l0=1.0 / 3.0, c_omega=C_OMEGA, nu=0.0, iters=5)
        raise AssertionError("newton returned quietly on a NaN in Omega0")
    except np.linalg.LinAlgError:
        pass
    for bad in (float("nan"), float("inf")):
        try:
            dp.newton(Om.copy(), c_l0=0.30, c_omega=C_OMEGA, nu=0.0, scale_gauge=bad, iters=5)
            raise AssertionError(f"newton returned quietly on scale_gauge={bad}")
        except np.linalg.LinAlgError:
            pass
    print("[3] SOUNDNESS: NaN/Inf in nu, Omega0 and scale_gauge all raise LinAlgError")


def test_guard_radii_budget_passthrough_rejects_out_of_hypothesis_input():
    """`radii_budget` is a documented thin pass-through; nk_bounds' hypothesis check must fire."""
    bad = [(float("nan"), 0.0, 0.9, 1e9), (-1e-3, 0.0, 0.9, 1e9),
           (1e-12, 0.0, float("inf"), 1e9)]
    for args in bad:
        b = radii_budget(*args)
        assert b.get("violations"), f"radii_budget absorbed out-of-hypothesis input {args}"
        assert not b.get("closes"), f"radii_budget claimed closure on {args}"
    ok = radii_budget(1e-12, 0.0, 0.9, 1e9)
    assert not ok.get("violations"), "the well-formed control must NOT be flagged"
    print(f"[4] SOUNDNESS: radii_budget pass-through rejects {len(bad)}/3, control clean")


def test_guard_private_operators_are_exact_at_degenerate_small_n():
    """A place a defect could have been and is not: the 4th-order operators at tiny n."""
    worst_D = worst_C = 0.0
    for n in (3, 4, 5, 6, 7):
        D = _drho_matrix4(n, 1.0)
        C = _cumint_matrix4(n, 1.0, n // 2)
        worst_D = max(worst_D, float(np.max(np.abs(D @ np.ones(n)))))
        worst_C = max(worst_C, float(np.max(np.abs(
            C @ np.ones(n) - (np.arange(n) - n // 2) * 1.0))))
    print(f"[5] SOUNDNESS: small-n operators exact -- D@ones {worst_D:.2e}, "
          f"cumint err {worst_C:.2e}")
    assert worst_D < 1e-12 and worst_C < 1e-12


def test_guard_planted_wrong_values_move_Y0():
    """Y_0 is not norm-blind: planted amplitude, parity and c_l errors all inflate it."""
    dp, Om = _fresh()
    y_ok, _ = y0_measure(dp, Om, 1.0 / 3.0, C_OMEGA, 0.0, norm="sup")
    y_amp, _ = y0_measure(dp, Om * 1.5, 1.0 / 3.0, C_OMEGA, 0.0, norm="sup")
    y_par, _ = y0_measure(dp, np.abs(Om), 1.0 / 3.0, C_OMEGA, 0.0, norm="sup")
    y_cl, _ = y0_measure(dp, Om, 1.0, C_OMEGA, 0.0, norm="sup")
    print(f"[6] SOUNDNESS: planted defects inflate Y_0 by "
          f"{y_amp / y_ok:.2f}x (amplitude), {y_par / y_ok:.2f}x (parity), "
          f"{y_cl / y_ok:.2f}x (c_l)")
    assert y_amp > 2.0 * y_ok and y_par > 2.0 * y_ok and y_cl > 2.0 * y_ok


def test_guard_a_star_bracketing_never_hangs_or_raises():
    """The dispatch's boundary inputs: bracketing leg 185's a*, the module always returns."""
    n_ok = 0
    for a_mod in (0.3855, A_STAR, 0.3875):
        for nu in (0.05, 0.3):
            dp, Om = _fresh(a=a_mod)
            out = dp.newton_gamma2(Om.copy(), a0=a_mod, nu=nu, c_l=C_L_IMPOSED,
                                   c_omega=C_OMEGA, iters=40)
            assert np.isfinite(out["residual_rms"]) and np.isfinite(out["a"])
            n_ok += 1
    print(f"[7] SOUNDNESS: {n_ok}/6 a*-bracketing cases return finite values, none hang")
    assert n_ok == 6


# ===========================================================================
# CHARACTERIZATION GATES -- these PIN the current, wrong behaviour
# ===========================================================================

def test_pinned_newton_gamma2_solved_a_cannot_reach_y0_measure():
    """SITE 1 (severe). `y0_measure`/`z2_quadratic_constant` have no `a` parameter.

    `newton_gamma2`'s whole contract is that `a` is the free unknown, yet the module's own
    Y_0/Z_2 consumers silently re-evaluate at the CONSTRUCTOR's `a`, so the reported Y_0 is
    a norm of a different operator's defect.

    REPAIR THAT FLIPS THIS: add an `a=None` parameter to `y0_measure` and
    `z2_quadratic_constant` forwarding to `residual`/`jacobian_Omega`, or have
    `newton_gamma2` refuse to return an `a` that differs from `dp.a`. Not by loosening a
    tolerance."""
    import inspect
    for fn in (y0_measure, z2_quadratic_constant):
        assert "a" not in inspect.signature(fn).parameters, \
            f"{fn.__name__} grew an `a` parameter -- SITE 1 may be repaired; update this gate"
    dp, Om = _fresh(a=A_MODULE)
    out = dp.newton_gamma2(Om.copy(), a0=A0_M7, nu=0.3, c_l=C_L_IMPOSED,
                           c_omega=C_OMEGA, iters=40)
    R_ctor = float(np.max(np.abs(dp.residual(out["Omega"], C_L_IMPOSED, C_OMEGA, 0.3))))
    R_solv = float(np.max(np.abs(dp.residual(out["Omega"], C_L_IMPOSED, C_OMEGA, 0.3,
                                             a=out["a"]))))
    infl = R_ctor / max(R_solv, 1e-300)
    print(f"[8] PINNED SITE 1: solved a={out['a']:.8f} vs constructor a={dp.a}; "
          f"defect {R_solv:.3e} -> {R_ctor:.3e} ({infl:.2e}x) with no error raised")
    assert abs(out["a"] - dp.a) > 1e-3, "the free unknown no longer drifts; re-check this gate"
    assert infl > 1e8, "SITE 1's inflation collapsed -- verify the defect, do not relax this"


def test_pinned_zero_profile_echoes_c_l0_back_at_residual_exactly_zero():
    """SITE 2 (severe). `newton(zeros, c_l0)` returns residual_rms == 0.0 and c_l == c_l0.

    `R(0; c_l, ...) == 0` for every `c_l`, and with `scale_gauge=None` the gauge target is
    read off the (zero) initial guess, so the gauge row is satisfied too. Newton breaks on
    iteration 1 and never touches `c_l`. At leg 125's own `c_l0 = 1/3` the module hands back
    Delta = -1/3 -- Chen's exact headline value -- from an identically zero profile, and
    every health indicator it exposes reads perfect.

    REPAIR THAT FLIPS THIS: reject a scale-gauge target that does not pin the amplitude (e.g.
    require `|target| > 0` when `scale_gauge is None`), or return a convergence/degeneracy
    flag. Not by loosening a tolerance."""
    dp, _ = _fresh()
    for c_l0 in (1.0 / 3.0, 0.30, 7.5):
        r = dp.newton(np.zeros(dp.n), c_l0=c_l0, c_omega=C_OMEGA, nu=0.0, iters=15)
        assert r["c_l"] == c_l0, "c_l is no longer echoed -- SITE 2 may be repaired"
        assert r["residual_rms"] == 0.0, "residual_rms is no longer exactly 0.0"
        assert len(r["history"]) == 1, "newton no longer breaks on iteration 1"
    r = dp.newton(np.zeros(dp.n), c_l0=1.0 / 3.0, c_omega=C_OMEGA, nu=0.0, iters=15)
    fabricated = diffusion_consistency(r["c_l"], C_OMEGA)
    print(f"[9] PINNED SITE 2: zero profile -> residual_rms={r['residual_rms']!r}, "
          f"1 iteration, Delta={fabricated!r} (Chen's exact -1/3, fabricated)")
    assert abs(fabricated - (-1.0 / 3.0)) < 1e-15


def test_pinned_z2_quadratic_constant_silently_substitutes_the_l1_norm():
    """SITE 3 (moderate). Any unrecognised `norm` becomes ord=1, with no record of the swap.

    `ordr = np.inf if norm == "sup" else 1`. The sibling `y0_measure` raises on the same
    input (gate 2). The returned dict has no `norm` key, so the substitution is unrecoverable
    downstream, and the inflation grows with n.

    REPAIR THAT FLIPS THIS: validate `norm` in `z2_quadratic_constant` exactly as
    `y0_measure` does, and/or record the norm in the returned dict. Not by loosening a
    tolerance."""
    dp, Om = _fresh()
    sup = z2_quadratic_constant(dp, Om, 1.0 / 3.0, C_OMEGA, 0.0, norm="sup")
    l1 = z2_quadratic_constant(dp, Om, 1.0 / 3.0, C_OMEGA, 0.0, norm="l1")
    assert "norm" not in sup, "z2 now records its norm -- SITE 3 may be repaired"
    for bad in ("frobenius", "Sup", "inf", "linf", "", "2"):
        b = z2_quadratic_constant(dp, Om, 1.0 / 3.0, C_OMEGA, 0.0, norm=bad)
        assert b == l1, f"norm={bad!r} no longer falls back to l1 -- SITE 3 may be repaired"
    infl = l1["Z2"] / sup["Z2"]
    print(f"[10] PINNED SITE 3: 6/6 unrecognised norms silently give the l1 value; "
          f"Z_2 {sup['Z2']:.4e} -> {l1['Z2']:.4e} ({infl:.4f}x at n={N})")
    assert infl > 1.1


def test_pinned_degenerate_scale_gauge_is_accepted_and_corrupts_Delta():
    """SITE 4 (moderate). A degenerate dilation gauge does not pin the amplitude.

    `newton` exposes no convergence flag -- only `residual_rms` -- so a caller reading `c_l`
    (the documented output) without separately policing `residual_rms` against the ~1e-16
    floor gets a badly wrong Delta with no signal.

    REPAIR THAT FLIPS THIS: reject a `scale_gauge` that does not pin the dilation orbit, or
    return a convergence flag. Not by loosening a tolerance."""
    dp, Om = _fresh()
    g = _gauge(dp, Om)
    honest = dp.newton(Om.copy(), c_l0=0.30, c_omega=C_OMEGA, nu=0.0, scale_gauge=g, iters=15)
    d_honest = diffusion_consistency(honest["c_l"], C_OMEGA)
    assert honest["residual_rms"] < 1e-12, "the honest control no longer converges"
    n_wrong = 0
    worst = 0.0
    for gv in (0.0, 1e-14, -g, 1e6):
        r = dp.newton(Om.copy(), c_l0=0.30, c_omega=C_OMEGA, nu=0.0, scale_gauge=gv, iters=15)
        d = diffusion_consistency(r["c_l"], C_OMEGA)
        if abs(d - d_honest) > 1e-6:
            n_wrong += 1
            worst = max(worst, abs(d - d_honest))
    print(f"[11] PINNED SITE 4: {n_wrong}/4 degenerate gauges accepted without raising; "
          f"honest Delta={d_honest:.6f}, worst |dDelta|={worst:.4g}")
    assert n_wrong == 4, "degenerate gauges are now rejected -- SITE 4 may be repaired"
    assert worst > 0.1


# ===========================================================================
# LATENCY -- no banked number is exposed
# ===========================================================================

def _calls_in(path):
    with open(path) as fh:
        tree = ast.parse(fh.read())
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
            out.append((name, {k.arg for k in node.keywords if k.arg}, node.lineno,
                        [ast.unparse(k.value) for k in node.keywords if k.arg == "norm"]))
    return out


def test_latency_no_banked_call_site_traverses_any_of_the_four_sites():
    """All four sites are LATENT. This gate fails the moment a landed call site becomes exposed."""
    p125 = os.path.join(ROOT, "experiments", "p2_route_m2p_v1_promotion.py")
    p185 = os.path.join(ROOT, "experiments", "p2_route_m2sd_v1_diagnostic.py")
    p187 = os.path.join(ROOT, "solver", "chen_inviscid_certificate.py")

    for path in (p125, p187):
        calls = _calls_in(path)
        ungauged = [c[2] for c in calls if c[0] == "newton" and "scale_gauge" not in c[1]]
        assert not ungauged, (f"{os.path.basename(path)}: newton called without an explicit "
                              f"scale_gauge at lines {ungauged} -- SITES 2/4 now EXPOSED")
        bad_norm = [c[2] for c in calls if c[0] == "z2_quadratic_constant"
                    and (not c[3] or c[3][0] not in ("'sup'", '"sup"', "'l1'", '"l1"'))]
        assert not bad_norm, (f"{os.path.basename(path)}: z2_quadratic_constant called with an "
                              f"unrecognised/defaulted norm at lines {bad_norm} -- SITE 3 EXPOSED")

    with open(p125) as fh:
        src = fh.read()
    composed = [ln for ln in src.splitlines()
                if ("y0_measure" in ln or "z2_quadratic_constant" in ln)
                and "newton_gamma2" in ln]
    assert not composed, f"leg 125 now feeds newton_gamma2 into Y_0/Z_2 -- SITE 1 EXPOSED: {composed}"

    with open(p185) as fh:
        tree = ast.parse(fh.read())
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "solver.dissipative_profile":
            imported |= {a.name for a in node.names}
    assert not (imported & {"y0_measure", "z2_quadratic_constant"}), \
        f"leg 185 can now reach the Y_0/Z_2 path -- SITE 1 EXPOSED: {sorted(imported)}"
    print(f"[12] LATENCY: 0 exposed call sites across legs 125/185/187 "
          f"(leg 185 imports only {sorted(imported)})")


def test_latency_leg_185_banked_stall_numbers_reproduce_exactly():
    """PRIOR ART, credited. Leg 185 owns the newton_gamma2 collapse; this leg re-derives it.

    Leg 185's journal banks `a = -10.092461405320627` and `residual_relative =
    5.485652392436699` at its stalled case. Reproducing both is an independent check on leg
    185's diagnostic and pins that this leg claims neither."""
    dp = DissipativeProfile(a=A_MODULE, n=401)
    Om, _, _ = chen_profile(dp.X)
    out = dp.newton_gamma2(Om.copy(), a0=A0_M7, nu=1.0, c_l=C_L_IMPOSED,
                           c_omega=C_OMEGA, iters=60)
    R = dp.residual(out["Omega"], C_L_IMPOSED, C_OMEGA, 1.0, a=out["a"])
    amp = float(np.sqrt(np.mean(out["Omega"] ** 2)))
    rel = float(np.sqrt(np.mean(R ** 2))) / max(amp, 1e-300)
    da = abs(out["a"] - (-10.092461405320627))
    dr = abs(rel - 5.485652392436699)
    print(f"[13] PRIOR ART (leg 185): a={out['a']:.12f} (|diff|={da:.2e}), "
          f"relative residual={rel:.12f} (|diff|={dr:.2e}), "
          f"amplitude collapsed to {np.max(np.abs(out['Omega'])):.3e}")
    assert da < 1e-9 and dr < 1e-9, "leg 185's banked stall numbers no longer reproduce"


if __name__ == "__main__":
    test_guard_diffusion_consistency_refuses_a_degenerate_amplitude_exponent()
    test_guard_y0_measure_refuses_an_unknown_norm()
    test_guard_nan_and_inf_propagate_visibly_and_are_not_absorbed()
    test_guard_radii_budget_passthrough_rejects_out_of_hypothesis_input()
    test_guard_private_operators_are_exact_at_degenerate_small_n()
    test_guard_planted_wrong_values_move_Y0()
    test_guard_a_star_bracketing_never_hangs_or_raises()
    test_pinned_newton_gamma2_solved_a_cannot_reach_y0_measure()
    test_pinned_zero_profile_echoes_c_l0_back_at_residual_exactly_zero()
    test_pinned_z2_quadratic_constant_silently_substitutes_the_l1_norm()
    test_pinned_degenerate_scale_gauge_is_accepted_and_corrupts_Delta()
    test_latency_no_banked_call_site_traverses_any_of_the_four_sites()
    test_latency_leg_185_banked_stall_numbers_reproduce_exactly()
    print("\nAll leg-207 adversarial gates passed: 7 soundness gates hold, 4 "
          "characterization gates PIN the four escalated silent-corruption sites, and 2 "
          "latency gates confirm no banked number is exposed (see "
          "experiments/journal/leg_207.md). solver/dissipative_profile.py was NOT edited.")
