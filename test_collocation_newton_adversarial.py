"""Permanent adversarial regression test for solver/collocation_newton.py (leg 114, Route-CNA).

WHAT THIS FILE IS.  Leg 114 ran the adversarial battery and THE GATE ANSWERED **YES**:
8 silent corruptions in 61 gate-scoped cases, three independent mechanisms.  The leg's
territory forbids editing solver/collocation_newton.py under ANY gate outcome
(DIRECTION.md sec 114: "Reads solver/collocation_newton.py; edits nothing under any
outcome"), so this file is banked as a **CHARACTERIZATION** test, exactly as leg 92 did
for solver/gclm.py before its bench repair:

  * checks named `check_KNOWN_GAP_*` pin the gaps **AS MEASURED**.  They assert the
    WRONG behaviour, on purpose, so that a later repair FAILS this file and is forced
    to record itself deliberately rather than sliding in.  When the repair lands, these
    are INVERTED (not weakened) at the same thresholds -- leg 92's convention.
  * every other check pins robustness that DID hold, so a repair cannot buy the gaps
    back by breaking something that works.

test_collocation_newton.py (6 gates) covers correctness on well-posed input and is
untouched by this file; this is the robustness complement, not a replacement.

THE GATE, VERBATIM (DIRECTION.md sec 114)
-----------------------------------------
"Under an adversarial battery of degenerate or poisoned inputs, does
solver/collocation_newton.py ever report a converged solution or plausible residual
that is silently wrong?"

ANSWER (leg 114): **yes**.  Three mechanisms.

  M1  THE CONVERGENCE FLAG IS BLIND TO THE ROW IT DROPS.  `newton_gauged` builds
      F = [gauge row ; residual rows EXCEPT `drop`] and sets
      `converged = hist[-1] < 1e-11` from that F alone.  The dropped row -- the one the
      docstring itself calls "the one row it does not see" -- is recomputed afterwards
      into `dropped_defect` and never consulted.  So `converged is True` is structurally
      guaranteed for ANY root of the (J-1)-row subsystem however large the dropped row's
      residual is.  Measured: `converged=True` with `dropped_defect = 3.34`.

  M2  THE ONE-GAUGE SYSTEM HAS A SECOND, SPURIOUS ROOT, AND IT IS REPORTED CONVERGED.
      Omega == -1 satisfies the gauge row Omega(theta=0) = -1 AND every collocation
      residual row to 2.8e-13, because H(constant) = 0 and Omega_X = 0.  It is not in
      the decay class the entire Route-D pair lives in: ||Omega||_X at alpha = 2 is
      5.84e+03 against the exact anchor's 1.0000 at J = 60, and it GROWS with J
      (2.59e+03 / 5.84e+03 / 1.04e+04 at J = 40 / 60 / 80).  `newton_gauged` returns it
      with `converged=True` from om0 = zeros, om0 = ones and om0 = 1e-8 * anchor.
      The certificate-visible defect on it -- `weighted_defect`, the Y_0 ingredient --
      is 1.72e-11 on the solver's own iterate and 4.65e-10 on the exact constant, i.e.
      72x to 1950x the true anchor's 2.38e-13 and still, in absolute terms, a defect
      no bound layer would flag.
      The sibling `newton` is IMMUNE: its second gauge (Omega at the node nearest X = 1
      equals -1/2) excludes the constant.  That control isolates the mechanism.

  M3  `critical_radius` HAS NO MAGNITUDE TEST ON THE SIGN CHANGE.  Its only test is
      `np.diff(np.sign(E)) != 0`.  An E that is 0.5 everywhere except one entry dipped
      to -1e-16 -- a relative perturbation of 4e-16 -- returns X_c = 15.025019 where the
      truth is `inf`, and the returned radius moves by only 1.0e-04 across THIRTEEN
      orders of magnitude of dip depth (1e-16 to 1e-3), so it carries essentially no
      information about whether the crossing is real.  Fed onward, `zero_order` turns
      that non-existent radius into a
      plausible exponent p = 0.2325 from 141 points where the truth is (nan, 0).

REACHABILITY, MEASURED AND REPORTED HONESTLY (it is why this is a characterization test
and not an escalation).  None of the three fires on the current production path:
`experiments/p2_route_d_v12_defect.py` calls `newton_gauged(c=...)` with om0=None, which
lands on the true anchor; and real converged E fields cross zero cleanly -- min(E) at the
tangency is +1.10e-03 on the J=60 grid, 5.5e+12 times the roundoff floor, and 40 draws of
relative noise up to 1e-08 never flipped X_c from inf to finite.  The gaps are LATENT.
`om0` is nonetheless a documented public parameter whose most natural degenerate value
(zeros) triggers M2.

Repo convention: self-running script, no pytest.
  Run: PYTHONPATH=. .venv/bin/python test_collocation_newton_adversarial.py

Companion battery: experiments/p2_route_cna_v1_adversarial.py
Companion data:    writeup/data/p2_route_cna_v1_adversarial.json
Findings:          writeup/novelty/leg_114.md
"""

import warnings

import numpy as np

from solver.collocation_newton import (ACollocation, continuation, critical_radius,
                                       effective_speed, velocity_integrals,
                                       weighted_defect, zero_order)

J = 60
C = 0.5
ALPHA_DECAY = 2.0
ALPHA_DEFECT = 1.0


def _col(a=0.0, Jl=J):
    return ACollocation(Jl, a=a)


def _poison(v, val, i=7):
    out = np.asarray(v, float).copy()
    out[i] = val
    return out


# ---------------------------------------------------------------------------
# KNOWN GAPS -- these assert the WRONG behaviour on purpose.  Invert on repair.
# ---------------------------------------------------------------------------


def check_KNOWN_GAP_constant_profile_is_returned_converged():
    """M2: Omega == -1 is an exact root of the one-gauge system, reported converged."""
    col = _col()
    truth = col.anchor()
    norm_true = col.norm_domain(truth, ALPHA_DECAY)
    assert abs(norm_true - 1.0) < 1e-3, norm_true

    # it really is an exact root -- gauge row and every residual row
    const = -np.ones(J)
    g0 = col.to_coef.sum(axis=0)
    assert abs(g0 @ const + 1.0) < 1e-12, "the constant must satisfy the gauge row"
    sup_const = float(np.max(np.abs(col.residual_a(const, C))))
    assert sup_const < 1e-11, sup_const

    seen = {}
    for name, om0 in [("zeros", np.zeros(J)), ("ones", np.ones(J)),
                      ("1e-8*anchor", 1e-8 * truth)]:
        r = col.newton_gauged(om0=om0, c=C, max_iter=200)
        om = r["Omega"]
        # KNOWN GAP: converged is True on a profile that is not the intended one
        assert r["converged"] is True, (name, r["converged"])
        assert np.max(np.abs(om + 1.0)) < 1e-10, (name, "did not land on the constant")
        norm_X = col.norm_domain(om, ALPHA_DECAY)
        assert norm_X > 1e3 * norm_true, (name, norm_X, norm_true)
        seen[name] = norm_X

    # and the certificate-visible defect on it still LOOKS small
    wdef = weighted_defect(col, -np.ones(J), C, ALPHA_DEFECT)[0]
    wdef_true = weighted_defect(col, truth, C, ALPHA_DEFECT)[0]
    assert wdef < 1e-8, wdef
    assert wdef / wdef_true < 1e4, (wdef, wdef_true)
    return (f"converged=True on Omega=-1 from 3 starts; ||Omega||_X(alpha=2) = "
            f"{seen['zeros']:.4e} against the exact anchor's {norm_true:.4f}; the "
            f"Y_0 ingredient weighted_defect = {wdef:.3e} still looks small "
            f"({wdef / wdef_true:.0f}x the true {wdef_true:.3e})")


def check_KNOWN_GAP_converged_flag_is_blind_to_the_dropped_row():
    """M1: converged is computed from F, which excludes the dropped row by construction."""
    col = _col()
    r = col.newton_gauged(om0=0.1 * col.anchor(), c=C, max_iter=200)
    # KNOWN GAP: the flag says converged while the row Newton never saw is O(1)
    assert r["converged"] is True, r["converged"]
    assert r["kept_sup"] < 1e-12, r["kept_sup"]
    assert r["dropped_defect"] > 1.0, r["dropped_defect"]
    R = col.residual_a(r["Omega"], C)
    sup_all = float(np.max(np.abs(R)))
    assert sup_all > 1.0, sup_all
    wdef = weighted_defect(col, r["Omega"], C, ALPHA_DEFECT)[0]
    assert wdef > 1.0, wdef
    return (f"converged=True with kept_sup = {r['kept_sup']:.2e} but dropped_defect = "
            f"{r['dropped_defect']:.4f}; sup|R| over ALL rows = {sup_all:.4f} and the "
            f"certificate defect = {wdef:.4f}")


def check_KNOWN_GAP_critical_radius_has_no_magnitude_test():
    """M3: a 4e-16 relative dip in an everywhere-positive E returns a finite radius."""
    Xg = np.linspace(0.01, 40.0, 800)
    E0 = 0.5 + 0.0 * Xg
    assert not np.isfinite(critical_radius(Xg, E0)), "clean E must report no crossing"

    radii = {}
    for eps in (1e-16, 1e-12, 1e-8, 1e-3):
        Ep = E0.copy()
        Ep[300] = -eps
        v = critical_radius(Xg, Ep)
        # KNOWN GAP: a finite plausible radius where the truth is inf
        assert np.isfinite(v), eps
        assert 14.0 < v < 16.0, (eps, v)
        radii[eps] = v
    spread = max(radii.values()) - min(radii.values())
    assert spread < 1e-3, radii            # 13 decades of depth, one answer
    return (f"E = 0.5 with ONE entry at -1e-16 returns X_c = {radii[1e-16]:.6f} where "
            f"the truth is inf; across dip depths 1e-16..1e-3 the answer moves by only "
            f"{spread:.1e}, so it carries no information about whether the crossing is real")


def check_KNOWN_GAP_bogus_radius_becomes_a_plausible_exponent():
    """M3, chained: the non-existent radius produces a finite exponent."""
    Xg = np.linspace(0.01, 40.0, 800)
    Ep = 0.5 + 0.0 * Xg
    Ep[300] = -1e-14
    Xc = critical_radius(Xg, Ep)
    om = -1.0 / (1.0 + Xg ** 2)
    p, n = zero_order(Xg, om, Xc)
    p_true, n_true = zero_order(Xg, om, float("inf"))
    # KNOWN GAP: a finite exponent from a radius that does not exist
    assert np.isfinite(p) and n > 100, (p, n)
    assert 0.2 < p < 0.3, p
    assert np.isnan(p_true) and n_true == 0, (p_true, n_true)
    return (f"zero_order at the bogus X_c = {Xc:.6f} returns p = {p:.6f} from {n} points; "
            f"at the true inf it correctly returns (nan, 0)")


def check_KNOWN_GAP_relres_is_identically_one_at_zero_speed():
    """newton_gauged's `relres` is not a relative residual when the transport term dies."""
    col = _col()
    r = col.newton_gauged(c=0.0, max_iter=120)
    # KNOWN GAP: a well-converged solve reports relres exactly 1.0
    assert r["converged"] is True, r["converged"]
    assert r["kept_sup"] < 1e-12, r["kept_sup"]
    assert abs(r["relres"] - 1.0) < 1e-12, r["relres"]
    return (f"at c = 0 the residual IS the source, so relres = {r['relres']:.12f} "
            f"identically while kept_sup = {r['kept_sup']:.2e}")


def check_KNOWN_GAP_singular_path_dict_is_incomplete():
    """The LinAlgError early-exit dicts omit the normal path's result keys."""
    col = _col()
    r = col.newton(om0=_poison(col.anchor(), np.nan), c0=C, max_iter=20)
    missing = {"relres", "residual_rms", "iterations", "nodal_sup"} - set(r.keys())
    # KNOWN GAP: the two return shapes differ
    assert missing == {"relres", "residual_rms", "iterations", "nodal_sup"}, missing
    assert r["converged"] is False
    # and it takes `continuation` down with it
    raised = None
    try:
        continuation([float("nan")], J=40, max_iter=20)
    except KeyError as exc:
        raised = str(exc)
    assert raised is not None and "relres" in raised, raised
    return (f"the singular path omits {len(missing)} result keys "
            f"({', '.join(sorted(missing))}); continuation indexes r['relres'] "
            f"unconditionally and dies with KeyError({raised})")


def check_KNOWN_GAP_max_iter_zero_is_asymmetric():
    """newton_gauged crashes on an empty history where newton returns."""
    col = _col()
    raised = None
    try:
        col.newton_gauged(c=C, max_iter=0)
    except IndexError as exc:
        raised = type(exc).__name__
    # KNOWN GAP: hist[-1] on an empty list
    assert raised == "IndexError", raised
    r = col.newton(c0=C, max_iter=0)          # the sibling handles it
    assert "converged" in r
    return ("newton_gauged(max_iter=0) raises IndexError on hist[-1] while "
            f"newton(max_iter=0) returns converged={r['converged']}")


# ---------------------------------------------------------------------------
# ROBUSTNESS THAT HELD -- a repair must not buy the gaps back by breaking these
# ---------------------------------------------------------------------------


def check_two_gauge_newton_excludes_the_constant():
    """The control that isolates M2: the second gauge is the whole difference."""
    col = _col()
    r = col.newton(om0=np.zeros(J), c0=C, max_iter=120)
    assert r["converged"] is False, r["converged"]
    assert np.max(np.abs(r["Omega"] + 1.0)) > 0.1, "must NOT land on the constant"
    i1 = int(np.argmin(np.abs(col.X - 1.0)))
    const_gauge = -1.0 + 0.5                  # the constant's value at that node, +1/2
    assert abs(const_gauge) > 0.4, const_gauge
    return (f"the identical om0=zeros start that fools newton_gauged gives "
            f"converged=False here (relres = {r['relres']:.4e}); the second gauge "
            f"Omega(X~1) = -1/2 misses the constant by {abs(const_gauge):.2f}")


def check_poisoned_inputs_stay_visible():
    """NaN/Inf in om0 or c never come back as a converged finite answer."""
    col = _col()
    truth = col.anchor()
    for name, kw in [("om0 NaN", {"om0": _poison(truth, np.nan)}),
                     ("om0 Inf", {"om0": _poison(truth, np.inf)}),
                     ("c NaN", {"c": np.nan}),
                     ("c Inf", {"c": np.inf})]:
        r = col.newton_gauged(c=kw.pop("c", C), max_iter=40, **kw)
        assert r["converged"] is False, name
        assert not np.isfinite(r["kept_sup"]), (name, r["kept_sup"])
    v = weighted_defect(col, _poison(truth, np.nan), C, ALPHA_DEFECT)[0]
    assert np.isnan(v), v
    assert not np.isfinite(velocity_integrals(np.array([np.pi]), 5)[0][1])
    assert np.isnan(critical_radius(np.linspace(0.1, 10, 50),
                                    np.where(np.arange(50) == 20, np.nan, 1.0)))
    return ("4 poisoned solves report converged=False with a non-finite kept_sup; "
            "weighted_defect, velocity_integrals(theta=pi) and critical_radius all "
            "propagate rather than swallow")


def check_structural_adversaries_raise():
    """Shape and index degeneracies are exceptions, not quiet answers."""
    col = _col()
    cases = [
        ("om0 wrong length", lambda: col.newton_gauged(om0=np.zeros(13), c=C)),
        ("drop == J", lambda: col.newton_gauged(drop=J, c=C)),
        ("drop negative", lambda: col.newton_gauged(drop=-1, c=C)),
        ("drop out of range", lambda: col.newton_gauged(drop=1000, c=C)),
        ("K negative", lambda: velocity_integrals(np.array([1.0]), -3)),
        ("refine=1 empty grid", lambda: weighted_defect(col, col.anchor(), C,
                                                        ALPHA_DEFECT, refine=1)),
        ("theta_eval empty", lambda: weighted_defect(col, col.anchor(), C, ALPHA_DEFECT,
                                                     theta_eval=np.array([]))),
    ]
    for name, fn in cases:
        try:
            fn()
        except (ValueError, IndexError):
            continue
        raise AssertionError(f"{name} returned instead of raising")
    return f"all {len(cases)} structural adversaries raise ValueError/IndexError"


def check_zero_order_guard_holds():
    """The module's one guard, plus the window mask, do their job."""
    X = np.linspace(0.1, 11.9, 400)
    Xc = 12.0
    om = -(Xc - X) ** 3.0                     # true exponent 3, by construction
    p0, n0 = zero_order(X, om, Xc)
    assert abs(p0 - 3.0) < 1e-9, p0
    rng = np.random.default_rng(1)
    for frac in (0.01, 0.2, 0.95):
        o = om.copy()
        o[rng.choice(400, int(frac * 400), replace=False)] = np.nan
        p, n = zero_order(X, o, Xc)
        assert abs(p - 3.0) < 1e-9, (frac, p)     # survivors still on the power law
        assert n < 400, (frac, n)                 # and the loss is reported
    for xc in (float("inf"), float("nan"), -5.0, 0.05):
        p, n = zero_order(X, om, xc)
        assert np.isnan(p) and n == 0, (xc, p, n)
    return ("exponent 3.000000 recovered exactly under 1%, 20% and 95% NaN poisoning "
            "with the surviving point count reported; inf/nan/negative/too-small Xc all "
            "refused as (nan, 0)")


def check_production_path_is_unaffected():
    """The reachability control: none of the three gaps fires as production calls it."""
    col = _col()
    truth = col.anchor()
    r = col.newton_gauged(c=C, max_iter=60)               # om0=None, as production does
    assert r["converged"] is True
    assert np.max(np.abs(r["Omega"] - truth)) < 1e-8, "must land on the true anchor"
    assert r["dropped_defect"] < 1e-10, r["dropped_defect"]
    wdef = weighted_defect(col, r["Omega"], C, ALPHA_DEFECT)[0]
    assert wdef < 1e-10, wdef

    # real converged E fields cross cleanly; the tangency margin is far above roundoff
    margins = {}
    for a in (0.125, 0.131):
        c2 = _col(a=a)
        s = c2.newton_gauged(c=C, max_iter=80)
        E = effective_speed(c2.X, c2.V @ s["Omega"], C, a)
        assert np.min(E) > 0.0, (a, np.min(E))
        assert not np.isfinite(critical_radius(c2.X, E)), a
        margins[a] = float(np.min(E))
    for a in (0.15, 0.30):
        c2 = _col(a=a)
        s = c2.newton_gauged(c=C, max_iter=80)
        E = effective_speed(c2.X, c2.V @ s["Omega"], C, a)
        assert np.isfinite(critical_radius(c2.X, E)), a
    return (f"om0=None lands on the true anchor with dropped_defect = "
            f"{r['dropped_defect']:.2e} and certificate defect {wdef:.3e}; the tangency "
            f"margin min(E) = {margins[0.131]:.3e} at a = 0.131 is ~1e+13 times the "
            f"roundoff floor, so M3 does not fire on real E fields")


CHECKS = [
    check_KNOWN_GAP_constant_profile_is_returned_converged,
    check_KNOWN_GAP_converged_flag_is_blind_to_the_dropped_row,
    check_KNOWN_GAP_critical_radius_has_no_magnitude_test,
    check_KNOWN_GAP_bogus_radius_becomes_a_plausible_exponent,
    check_KNOWN_GAP_relres_is_identically_one_at_zero_speed,
    check_KNOWN_GAP_singular_path_dict_is_incomplete,
    check_KNOWN_GAP_max_iter_zero_is_asymmetric,
    check_two_gauge_newton_excludes_the_constant,
    check_poisoned_inputs_stay_visible,
    check_structural_adversaries_raise,
    check_zero_order_guard_holds,
    check_production_path_is_unaffected,
]


def main():
    np.seterr(all="ignore")
    warnings.filterwarnings("ignore")
    n_gap = 0
    for fn in CHECKS:
        head = fn()
        tag = "PASS"
        if fn.__name__.startswith("check_KNOWN_GAP"):
            n_gap += 1
            tag = "KNOWN GAP"
        print(f"{tag:9s} {fn.__name__}: {head}")
    print(f"\nall collocation_newton adversarial checks passed ({len(CHECKS)} checks, "
          f"{n_gap} of them leg 114 KNOWN GAPS pinned AS MEASURED).")
    print("Leg 114's gate answered YES: 8 silent corruptions in 61 cases, three "
          "mechanisms (M1 flag blind to the dropped row, M2 spurious constant root, "
          "M3 critical_radius has no magnitude test).")
    print("A repair to solver/collocation_newton.py MUST fail the 7 KNOWN GAP checks "
          "and invert them at these same thresholds -- it must not weaken them.")


if __name__ == "__main__":
    main()
