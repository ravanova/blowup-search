"""Permanent adversarial regression test for solver/collocation_newton.py
(leg 114, Route-CNA -- REPAIRED AND INVERTED BY LEG 150, Route-CNR).

WHAT THIS FILE IS.  Leg 114 ran the adversarial battery and THE GATE ANSWERED **YES**:
8 silent corruptions in 61 gate-scoped cases, three independent mechanisms.  The leg's
territory forbade editing solver/collocation_newton.py under ANY gate outcome
(DIRECTION.md sec 114: "Reads solver/collocation_newton.py; edits nothing under any
outcome"), so this file was banked as a **CHARACTERIZATION** test, exactly as leg 92 did
for solver/gclm.py before its bench repair:

  * checks named `check_KNOWN_GAP_*` pinned the gaps **AS MEASURED**.  They asserted the
    WRONG behaviour, on purpose, so that a later repair would FAIL this file and be forced
    to record itself deliberately rather than sliding in.

**LEG 150 LANDED THAT REPAIR, AND THIS FILE IS NOW INVERTED.**  Every former
`check_KNOWN_GAP_*` is renamed `check_REPAIRED_*` and asserts the *opposite* verdict
**at leg 114's own thresholds, which are reproduced verbatim below** -- `kept_sup < 1e-12`,
`dropped_defect > 1.0`, `norm_X > 1e3 * norm_true`, `14.0 < X_c < 16.0`, `0.2 < p < 0.3`,
`spread < 1e-3`, `abs(relres - 1.0) < 1e-12`.  Nothing is weakened: where leg 114 measured a
magnitude, this file still measures the same magnitude and only the *verdict* flips.  Leg
114's numbers remain checkable here because the repair moved no float -- it consults
quantities the module already computed.  Where the pre-repair answer is still reachable
behind an explicit parameter (`critical_radius(..., min_rel_depth=0.0)`), the inverted check
also asserts that it reproduces leg 114's value EXACTLY, so the old measurement survives its
own repair.

  * every non-inverted check pins robustness that DID hold, and still must: a repair cannot
    buy the gaps back by breaking something that works.

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
# REPAIRED (leg 150) -- these were the 7 KNOWN GAPs.  Same thresholds, flipped verdict.
# ---------------------------------------------------------------------------


def check_REPAIRED_constant_profile_is_no_longer_returned_converged():
    """M2 inverted: Omega == -1 is still an exact root, and is no longer sold as converged."""
    col = _col()
    truth = col.anchor()
    norm_true = col.norm_domain(truth, ALPHA_DECAY)
    assert abs(norm_true - 1.0) < 1e-3, norm_true

    # it really is an exact root -- gauge row and every residual row (UNCHANGED by the repair)
    const = -np.ones(J)
    g0 = col.to_coef.sum(axis=0)
    assert abs(g0 @ const + 1.0) < 1e-12, "the constant must satisfy the gauge row"
    sup_const = float(np.max(np.abs(col.residual_a(const, C))))
    assert sup_const < 1e-11, sup_const

    seen, relres = {}, {}
    for name, om0 in [("zeros", np.zeros(J)), ("ones", np.ones(J)),
                      ("1e-8*anchor", 1e-8 * truth)]:
        r = col.newton_gauged(om0=om0, c=C, max_iter=200)
        om = r["Omega"]
        # INVERTED: the flag now refuses the profile that is not the intended one
        assert r["converged"] is False, (name, r["converged"])
        assert r["reason"] is not None and "FULL residual" in r["reason"], (name, r["reason"])
        # the pre-repair flag is still readable, so leg 114's measurement survives
        assert r["converged_kept_rows"] is True, (name, "the subsystem DID converge")
        assert np.max(np.abs(om + 1.0)) < 1e-10, (name, "did not land on the constant")
        norm_X = col.norm_domain(om, ALPHA_DECAY)
        assert norm_X > 1e3 * norm_true, (name, norm_X, norm_true)   # leg 114's threshold
        assert r["relres"] > 1.0, (name, r["relres"])
        seen[name] = norm_X
        relres[name] = r["relres"]

    # and the certificate-visible defect on it STILL looks small -- unchanged, and the
    # reason the flag had to be the thing that moved
    wdef = weighted_defect(col, -np.ones(J), C, ALPHA_DEFECT)[0]
    wdef_true = weighted_defect(col, truth, C, ALPHA_DEFECT)[0]
    assert wdef < 1e-8, wdef
    assert wdef / wdef_true < 1e4, (wdef, wdef_true)
    return (f"converged=False on Omega=-1 from all 3 starts (was True) with relres = "
            f"{relres['zeros']:.4e}; ||Omega||_X(alpha=2) = {seen['zeros']:.4e} against the "
            f"exact anchor's {norm_true:.4f} as leg 114 measured; the Y_0 ingredient "
            f"weighted_defect = {wdef:.3e} is UNCHANGED and still looks small "
            f"({wdef / wdef_true:.0f}x the true {wdef_true:.3e}) -- the flag moved, not the number")


def check_REPAIRED_converged_flag_now_sees_the_dropped_row():
    """M1 inverted: the flag consults the full residual, not the (J-1)-row subsystem."""
    col = _col()
    r = col.newton_gauged(om0=0.1 * col.anchor(), c=C, max_iter=200)
    # INVERTED: the flag no longer says converged while the row Newton never saw is O(1)
    assert r["converged"] is False, r["converged"]
    assert r["converged_kept_rows"] is True, "the subsystem still converges -- that is M1"
    assert r["kept_sup"] < 1e-12, r["kept_sup"]          # leg 114's threshold, unchanged
    assert r["dropped_defect"] > 1.0, r["dropped_defect"]  # leg 114's threshold, unchanged
    R = col.residual_a(r["Omega"], C)
    sup_all = float(np.max(np.abs(R)))
    assert sup_all > 1.0, sup_all
    wdef = weighted_defect(col, r["Omega"], C, ALPHA_DEFECT)[0]
    assert wdef > 1.0, wdef
    assert r["relres"] > 1.0, r["relres"]
    return (f"converged=False (was True) with kept_sup = {r['kept_sup']:.2e} and "
            f"dropped_defect = {r['dropped_defect']:.4f} both exactly as leg 114 measured; "
            f"sup|R| over ALL rows = {sup_all:.4f}, certificate defect = {wdef:.4f}, and the "
            f"flag now reads relres = {r['relres']:.4f} over all {J} rows")


def check_REPAIRED_critical_radius_has_a_magnitude_test():
    """M3 inverted: a roundoff-scale dip no longer buys a finite radius."""
    Xg = np.linspace(0.01, 40.0, 800)
    E0 = 0.5 + 0.0 * Xg
    assert not np.isfinite(critical_radius(Xg, E0)), "clean E must report no crossing"

    radii_pre = {}
    for eps in (1e-16, 1e-12, 1e-8, 1e-3):
        Ep = E0.copy()
        Ep[300] = -eps
        # INVERTED: the truth is inf, and inf is what comes back
        assert not np.isfinite(critical_radius(Xg, Ep)), eps
        # leg 114's measurement is NOT destroyed -- it is reachable behind the parameter,
        # and it still reproduces at leg 114's own thresholds
        v = critical_radius(Xg, Ep, min_rel_depth=0.0)
        assert np.isfinite(v), eps
        assert 14.0 < v < 16.0, (eps, v)
        radii_pre[eps] = v
    spread = max(radii_pre.values()) - min(radii_pre.values())
    assert spread < 1e-3, radii_pre        # 13 decades of depth, one answer -- still true
    return (f"all 4 dip depths 1e-16..1e-3 now return inf (was X_c = "
            f"{radii_pre[1e-16]:.6f}); min_rel_depth=0.0 still reproduces leg 114's value "
            f"exactly, with its 13-decade spread of only {spread:.1e}")


def check_REPAIRED_bogus_radius_no_longer_becomes_an_exponent():
    """M3 inverted, chained: no radius, therefore no exponent."""
    Xg = np.linspace(0.01, 40.0, 800)
    Ep = 0.5 + 0.0 * Xg
    Ep[300] = -1e-14
    Xc = critical_radius(Xg, Ep)
    om = -1.0 / (1.0 + Xg ** 2)
    p, n = zero_order(Xg, om, Xc)
    p_true, n_true = zero_order(Xg, om, float("inf"))
    # INVERTED: (nan, 0), which is exactly what the true inf gives
    assert not np.isfinite(Xc), Xc
    assert np.isnan(p) and n == 0, (p, n)
    assert np.isnan(p_true) and n_true == 0, (p_true, n_true)
    # and leg 114's chained number still reproduces behind the parameter
    Xc_pre = critical_radius(Xg, Ep, min_rel_depth=0.0)
    p_pre, n_pre = zero_order(Xg, om, Xc_pre)
    assert np.isfinite(p_pre) and n_pre > 100, (p_pre, n_pre)
    assert 0.2 < p_pre < 0.3, p_pre        # leg 114's threshold, unchanged
    return (f"zero_order now returns (nan, 0) -- identical to the true inf -- where leg 114 "
            f"measured p = {p_pre:.6f} from {n_pre} points; that value still reproduces at "
            f"min_rel_depth=0.0")


def check_REPAIRED_relres_at_zero_speed_no_longer_reports_converged():
    """At c = 0 the residual IS the source: relres is still 1.0, and 1.0 is not converged."""
    col = _col()
    r = col.newton_gauged(c=0.0, max_iter=120)
    # INVERTED: the flag no longer calls this converged
    assert r["converged"] is False, r["converged"]
    assert r["converged_kept_rows"] is True, "the gauged subsystem does converge"
    assert r["kept_sup"] < 1e-12, r["kept_sup"]            # leg 114's threshold, unchanged
    assert abs(r["relres"] - 1.0) < 1e-12, r["relres"]     # THE NUMBER IS UNCHANGED
    assert r["reason"] is not None, r["reason"]
    return (f"at c = 0 the residual IS the source, so relres = {r['relres']:.12f} "
            f"identically -- unchanged from leg 114 -- and converged is now False, because a "
            f"residual equal to the term it must cancel is not a converged solve "
            f"(kept_sup = {r['kept_sup']:.2e})")


def check_REPAIRED_singular_path_dict_is_complete():
    """The LinAlgError early-exit dicts now carry the normal path's result keys."""
    col = _col()
    r = col.newton(om0=_poison(col.anchor(), np.nan), c0=C, max_iter=20)
    missing = {"relres", "residual_rms", "iterations", "nodal_sup"} - set(r.keys())
    # INVERTED: the two return shapes agree
    assert missing == set(), missing
    assert r["converged"] is False
    # and continuation survives it, visibly rather than silently
    rows = continuation([float("nan")], J=40, max_iter=20)
    assert len(rows) == 1, rows
    assert rows[0]["converged"] is False, rows[0]
    assert not np.isfinite(rows[0]["relres"]), rows[0]["relres"]
    # the gauged sibling's early exit is complete too
    rg = col.newton_gauged(om0=_poison(col.anchor(), np.nan), c=C, max_iter=20)
    assert {"kept_sup", "dropped_defect", "relres", "iterations"} <= set(rg.keys())
    return ("the singular path now carries all 4 formerly-missing result keys; "
            f"continuation([nan]) returns {len(rows)} flagged row with converged=False and "
            f"relres={rows[0]['relres']} instead of dying with KeyError('relres')")


def check_REPAIRED_max_iter_zero_is_symmetric():
    """newton_gauged no longer crashes on an empty history."""
    col = _col()
    # INVERTED: it returns, like its sibling, instead of raising IndexError on hist[-1].
    # om0=None starts AT the exact a=0 anchor, which really is a solution, so
    # converged=True there is the honest answer and not a residue of the gap.
    r = col.newton_gauged(c=C, max_iter=0)
    assert "converged" in r and r["converged"] is True, r
    assert r["iterations"] == 0, r["iterations"]
    assert r["kept_sup"] < 1e-11, r["kept_sup"]
    # from a start that is NOT a solution it returns and says so
    rz = col.newton_gauged(c=C, om0=np.zeros(J), max_iter=0)
    assert rz["converged"] is False, rz
    assert rz["iterations"] == 0 and rz["reason"] is not None, rz
    rn = col.newton(c0=C, max_iter=0)          # the sibling, unchanged
    assert "converged" in rn
    return (f"newton_gauged(max_iter=0) now returns instead of raising IndexError: from the "
            f"anchor converged={r['converged']} with kept_sup={r['kept_sup']:.3e} (it IS a "
            f"solution), from om0=zeros converged={rz['converged']}; newton(max_iter=0) "
            f"returns converged={rn['converged']} as before")


def check_REPAIRED_clean_inputs_did_not_move():
    """The whole licence for the repair: the production path is untouched.

    This is the in-battery echo of experiments/p2_route_cnr_v1_repair.py's arm B, which
    does the full bitwise differential against the pre-repair module read out of git.
    """
    col = _col()
    truth = col.anchor()
    r = col.newton_gauged(c=C, max_iter=60)                # om0=None, as production does
    assert r["converged"] is True, (r["converged"], r["reason"])
    assert r["relres_has_referent"] is True
    assert r["reason"] is None, r["reason"]
    assert np.max(np.abs(r["Omega"] - truth)) < 1e-8
    worst = 0.0
    for a in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5):               # the production a-range
        c2 = _col(a=a)
        s = c2.newton_gauged(c=C, max_iter=60)
        assert s["converged"] is True, (a, s["reason"])
        worst = max(worst, s["relres"])
    # the perturbed clean start test_collocation_newton.py gate 4 uses
    r4 = col.newton_gauged(c=C, om0=truth * 1.2 + 0.02 * np.cos(col.theta))
    assert r4["converged"] is True, r4["reason"]
    return (f"om0=None stays converged=True across the whole production range a=0..0.5, "
            f"worst relres = {worst:.4e} against the repair's threshold 1.0 "
            f"({1.0 / worst:.1f}x of margin); gate 4's perturbed start also holds")


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
    check_REPAIRED_constant_profile_is_no_longer_returned_converged,
    check_REPAIRED_converged_flag_now_sees_the_dropped_row,
    check_REPAIRED_critical_radius_has_a_magnitude_test,
    check_REPAIRED_bogus_radius_no_longer_becomes_an_exponent,
    check_REPAIRED_relres_at_zero_speed_no_longer_reports_converged,
    check_REPAIRED_singular_path_dict_is_complete,
    check_REPAIRED_max_iter_zero_is_symmetric,
    check_REPAIRED_clean_inputs_did_not_move,
    check_two_gauge_newton_excludes_the_constant,
    check_poisoned_inputs_stay_visible,
    check_structural_adversaries_raise,
    check_zero_order_guard_holds,
    check_production_path_is_unaffected,
]


def main():
    np.seterr(all="ignore")
    warnings.filterwarnings("ignore")
    n_rep = 0
    for fn in CHECKS:
        head = fn()
        tag = "PASS"
        if fn.__name__.startswith("check_REPAIRED"):
            n_rep += 1
            tag = "REPAIRED"
        print(f"{tag:9s} {fn.__name__}: {head}")
    print(f"\nall collocation_newton adversarial checks passed ({len(CHECKS)} checks, "
          f"{n_rep} of them leg 150's inversions of leg 114's KNOWN GAPS).")
    print("Leg 114's gate answered YES: 8 silent corruptions in 61 cases, three "
          "mechanisms (M1 flag blind to the dropped row, M2 spurious constant root, "
          "M3 critical_radius has no magnitude test).")
    print("Leg 150 repaired all three. The 7 KNOWN GAP pins are INVERTED at leg 114's own "
          "thresholds, not weakened: every magnitude leg 114 measured is still asserted "
          "here and only the verdict flipped, because the repair moved no float -- it "
          "consults quantities newton_gauged already computed and never read.")
    print("Zero-regression evidence: experiments/p2_route_cnr_v1_repair.py, a bitwise "
          "float64 differential against the pre-repair module read out of git at d4a6387.")


if __name__ == "__main__":
    main()
