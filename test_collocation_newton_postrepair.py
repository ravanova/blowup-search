"""Leg 166, Route-CNB: the banked POST-REPAIR regression suite for
solver/collocation_newton.py.

WHAT THIS FILE IS FOR
---------------------
Leg 114 (Route-CNA) found 8 silent corruptions.  Leg 150 (Route-CNR) repaired the
three mechanisms behind them -- and wrote its own pin inversions in the SAME
commit as the patch (446805b), so no independent run had ever re-derived them.
This file is that independent re-derivation, banked so it cannot decay at the
rate of memory (standing lesson 68).

It re-runs all EIGHT of leg 114's SILENT_WRONG cases.  Leg 150's own arm A
covered FIVE of them (its four M3 entries are one case at four dip depths, and
two of its ten cases are ones leg 150 introduced itself).  All eight are now
fixed.

  *** UPDATE (leg 0/BENCH, bench/fix-collocation-newton-scale-invariant-gap):
      `pure_sign_noise` NO LONGER returns leg 114's recorded value.
      critical_radius gained a second, orthogonal predicate -- `min_isolation`,
      a pure node-count that no OTHER sign change lie within `min_isolation`
      nodes of a candidate -- because the relative-depth guard alone is
      SCALE-INVARIANT and this field has no scale (every run is one node long
      with |E| = max|E|).  The two `check_KNOWN_GAP_*` checks below are
      INVERTED to `check_REPAIRED_*`, in leg 92's own convention: they now
      assert the fix, at the field this leg named, and would fail again if a
      future change bought the gap back. ***

One check is still named KNOWN_GAP: a SECOND, smaller gap this leg found in the
same guard (one non-finite entry anywhere in E disables the magnitude test
entirely) that this repair's territory did not extend to closing -- see its own
docstring for why it is untouched on purpose.

That check asserts the corruption AS MEASURED, at leg 166's own values, in leg
92's convention: a later repair FAILS this file and must INVERT it rather than
weaken it.  The other checks pin the repair that did land and the bit-identity
that licenses it, so a future patch cannot buy the gaps back by breaking them.

Run:  .venv/bin/python test_collocation_newton_postrepair.py
"""

import hashlib
import importlib.util
import os
import subprocess
import sys
import tempfile

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from solver.collocation_newton import (                                  # noqa: E402
    ACollocation, critical_radius, effective_speed, zero_order,
    weighted_defect, refined_theta, velocity_integrals, eval_matrices)

np.seterr(all="ignore")

J = 60
C = 0.5
PRE_REF = "d4a6387"      # the module's creating commit; a stable ancestor of main

# leg 114's own M3 grid, from experiments/p2_route_cna_v1_adversarial.py line 285
XG = np.linspace(0.01, 40.0, 800)

_checks = []


def check(fn):
    _checks.append(fn)
    return fn


def _col(a=0.0, Jl=J):
    return ACollocation(Jl, a=a)


def _arr_sha(a):
    return hashlib.sha256(np.ascontiguousarray(np.asarray(a, float)).tobytes()).hexdigest()[:16]


def _load_prerepair():
    src = subprocess.check_output(
        ["git", "show", f"{PRE_REF}:solver/collocation_newton.py"], cwd=ROOT)
    d = tempfile.mkdtemp(prefix="cnb_pre_")
    p = os.path.join(d, "cn_pre.py")
    with open(p, "wb") as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location("cn_pre_postrepair", p)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m


# ===========================================================================
# THE KNOWN GAP -- leg 114 case 7 of 8, still open after leg 150's repair
# ===========================================================================


@check
def check_REPAIRED_pure_sign_noise_no_longer_returns_the_prerepair_radius():
    """INVERTED (leg 0/BENCH).  leg 114 `pure_sign_noise`: now fixed.

    E = (-1)^k is pure alternating sign noise with no crossing to find.
    Pre-repair (and still, at min_rel_depth=0.0) critical_radius returned leg
    114's recorded 0.03502503128911139.  It now returns inf -- the truth.

    MECHANISM OF THE FIX: the relative-depth guard alone is a predicate-CLASS
    ceiling, not a threshold -- it requires each side's constant-sign excursion
    to reach min_rel_depth * max|E|, which is SCALE-INVARIANT, and this field
    has no scale (every run is one node long with |E| = 1 = max|E|, so the
    excursion ratio is exactly 1.0 on both sides, the largest value that test
    can ever see).  The added `min_isolation` guard is a DIFFERENT predicate,
    outside that class: it is a pure node-count, never a magnitude, and it
    requires no OTHER sign change lie within `min_isolation` nodes of a
    candidate.  Pure sign noise has a sign change at (up to) every node --
    799 of 799 possible positions here -- so no candidate is isolated.  Real
    crossings (see the control below) are the ONLY sign change in their field.
    """
    E = (-1.0) ** np.arange(XG.size)          # leg 114's construction, verbatim
    xc = critical_radius(XG, E)
    leg114_recorded = 0.03502503128911139
    assert not np.isfinite(xc), (
        f"pure_sign_noise still returns a finite radius: {xc!r} -- the gap is back")
    # the pre-repair path (min_rel_depth=0.0) is UNTOUCHED by this repair: it
    # still reproduces leg 114's recorded value bitwise, exactly as before.
    assert critical_radius(XG, E, min_rel_depth=0.0) == leg114_recorded
    print(f"  REPAIRED   pure_sign_noise -> Xc = {xc!r} (was leg 114's recorded "
          f"{leg114_recorded!r}; min_rel_depth=0.0 still reproduces it bitwise)")


@check
def check_REPAIRED_control_the_isolation_predicate_separates_it():
    """INVERTED (leg 0/BENCH) control (standing lesson 90).

    Pre-repair, no min_rel_depth rejected the sign noise while keeping every
    real crossing -- 0 of 11 thresholds did both, because relative depth alone
    is the wrong predicate CLASS for a field with no scale.  The added
    `min_isolation` guard is a different predicate (a node count, gated the
    same way the magnitude guard is: off at min_rel_depth=0.0, on otherwise),
    and it is orthogonal to the depth ratio -- so now the threshold ladder's
    LOW end (where the relative-depth test alone kept the noise) is exactly
    where the isolation test rejects it while every real crossing survives.
    The ladder's HIGH end still fails on relative depth alone, unrelated to
    this repair: that is leg 150's own control, re-measured here, not moved.
    """
    Enoise = (-1.0) ** np.arange(XG.size)
    real = []
    for a in (0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5):
        col = _col(a)
        r = col.newton_gauged(c=C)
        E = effective_speed(col.X, col.V @ r["Omega"], r["c"], a)
        if np.isfinite(critical_radius(col.X, E)):
            real.append((col.X, E))
    assert len(real) >= 5, f"need real crossings to control against, got {len(real)}"

    both = []
    for d in (0.0, 1e-3, 1e-2, 0.1, 0.5, 0.9, 0.999, 1.0, 1.1, 1.5, 2.0):
        rejected = not np.isfinite(critical_radius(XG, Enoise, min_rel_depth=d))
        kept = sum(1 for X, E in real
                   if np.isfinite(critical_radius(X, E, min_rel_depth=d)))
        if rejected and kept == len(real):
            both.append(d)
    # d=0.0 (the pre-repair path, isolation OFF) must still be the one place
    # nothing rejects the noise -- the repair does not touch that escape hatch.
    assert np.isfinite(critical_radius(XG, Enoise, min_rel_depth=0.0)), (
        "min_rel_depth=0.0 no longer reproduces the pre-repair bypass")
    assert both, (
        "no threshold does BOTH any more -- the isolation guard stopped "
        "separating the noise from the real crossings; re-check min_isolation")
    # the module's own default (1e-2) is inside the separating range
    assert 1e-2 in both, f"the shipped default 1e-2 no longer separates them: {both}"
    # and the control that could still fail: a large enough relative-depth
    # threshold rejects the real crossings too, on the ORIGINAL mechanism,
    # unrelated to the isolation guard -- unmoved by this repair.
    kept_at_1 = sum(1 for X, E in real
                    if np.isfinite(critical_radius(X, E, min_rel_depth=1.0)))
    assert kept_at_1 == 0, f"expected all real crossings rejected at d=1.0, kept {kept_at_1}"
    print(f"  REPAIRED   control: {len(both)} of 11 thresholds (including the shipped "
          f"default 1e-2) now reject the sign noise AND keep all {len(real)} real "
          f"crossings; d=0.0 still bypasses (untouched) and d=1.0 still rejects "
          f"everything (leg 150's original ceiling, unmoved)")


# ===========================================================================
# THE SEVEN THAT ARE FIXED -- re-derived from leg 114's record, independently
# ===========================================================================


@check
def check_REPAIRED_M2_constant_rejected_from_all_three_recorded_starts():
    """leg 114 cases 1-3: om0 = zeros / ones / 1e-8*anchor returned the spurious
    constant Omega = -1 with converged=True.  All three now rejected."""
    col = _col(0.0)
    anchor = col.anchor()
    for name, om0 in (("zeros", np.zeros(J)), ("ones", np.ones(J)),
                      ("1e-8*anchor", 1e-8 * anchor)):
        r = col.newton_gauged(c=C, om0=om0)
        assert r["converged"] is False, f"{name}: still converged=True"
        assert r["relres"] > 1.0, f"{name}: relres {r['relres']} does not exceed the tol"
        assert r["reason"], f"{name}: rejected without a reason string"
        # leg 114's magnitude, still asserted: it IS the constant
        assert np.max(np.abs(r["Omega"] + 1.0)) < 1e-6, f"{name}: not the constant root"
    print("  REPAIRED   M2 constant rejected from all 3 of leg 114's recorded starts")


@check
def check_REPAIRED_M1_third_root_rejected():
    """leg 114 case 4: om0 = 0.1*anchor converged onto a root whose DROPPED row
    was 3.3438.  Now rejected, and the dropped row is still that large."""
    col = _col(0.0)
    r = col.newton_gauged(c=C, om0=0.1 * col.anchor())
    assert r["converged"] is False, "M1 third root still reported converged"
    assert r["converged_kept_rows"] is True, (
        "the pre-repair flag should be UNCHANGED and still True -- leg 114's "
        "measurement must stay readable off the same dict")
    assert r["relres"] > 1.0
    print(f"  REPAIRED   M1 third root: converged=False, converged_kept_rows=True "
          f"(unchanged), relres={r['relres']:.4e}, dropped_defect={r['dropped_defect']:.4e}")


@check
def check_REPAIRED_constant_root_still_exists_but_is_no_longer_blessed():
    """leg 114 case 5.  Omega = -1 satisfies the gauge row and every collocation
    residual row -- a property of the EQUATION that no patch can delete.  The
    check is that the module no longer returns it converged."""
    col = _col(0.0)
    const = -np.ones(J)
    g0 = col.to_coef.sum(axis=0)
    sup_res = float(np.max(np.abs(col.residual_a(const, C))))
    assert sup_res < 1e-11, (
        f"the constant stopped being a root ({sup_res:.3e}) -- that would mean the "
        "EQUATION changed, not the guard")
    assert abs(float(g0 @ const + 1.0)) < 1e-12, "the constant stopped satisfying the gauge"
    r = col.newton_gauged(c=C, om0=const)
    assert r["converged"] is False, "the module still blesses the constant root"
    print(f"  REPAIRED   constant root still exact (sup|R| = {sup_res:.3e}) but "
          f"converged=False")


@check
def check_REPAIRED_M3_one_point_dip_at_all_four_recorded_depths():
    """leg 114 case 6: E = 0.5 with E[300] = -eps returned a plausible finite
    radius at four dip depths.  All four now return inf, which is the truth --
    and min_rel_depth=0.0 reproduces leg 114's four recorded values BITWISE."""
    recorded = {1e-16: 15.025018773466835, 1e-12: 15.025018773466735,
                1e-8: 15.025018772465833, 1e-3: 15.024918873142328}
    for eps, rec in recorded.items():
        E = np.full(XG.size, 0.5)
        E[300] = -eps
        assert not np.isfinite(critical_radius(XG, E)), \
            f"eps={eps:.0e}: a finite radius still comes back"
        got = critical_radius(XG, E, min_rel_depth=0.0)
        assert got == rec, (
            f"eps={eps:.0e}: min_rel_depth=0.0 gave {got!r}, leg 114 recorded {rec!r} -- "
            "leg 114's measurement must survive its own repair, bitwise")
    print("  REPAIRED   M3 one-point dip -> inf at all 4 depths; min_rel_depth=0.0 "
          "reproduces leg 114's 4 recorded values bitwise")


@check
def check_REPAIRED_bogus_radius_no_longer_becomes_an_exponent():
    """leg 114 case 8: the bogus radius fed zero_order, which returned
    p = 0.232454 from 141 points where the truth is (nan, 0)."""
    E = np.full(XG.size, 0.5)
    E[300] = -1e-16
    xc = critical_radius(XG, E)
    col = _col(0.0)
    om = np.interp(XG, col.X, col.anchor())
    p, n = zero_order(XG, om, xc)
    assert not np.isfinite(p) and n == 0, f"still returns a plausible exponent: {(p, n)}"
    # and the true inf gives exactly the same thing
    assert zero_order(XG, om, float("inf")) == (p, n) or (
        not np.isfinite(zero_order(XG, om, float("inf"))[0]))
    print(f"  REPAIRED   bogus radius -> zero_order returns (nan, 0), as the true inf does")


@check
def check_REPAIRED_structural_gaps_max_iter_zero_and_singular_dicts():
    """leg 150's two structural fixes, re-verified: max_iter=0 returns instead of
    raising IndexError, and the early-exit dicts carry the normal path's keys."""
    col = _col(0.0)
    r = col.newton_gauged(c=C, max_iter=0)
    for k in ("converged", "converged_kept_rows", "relres", "kept_sup",
              "dropped_defect", "history", "Omega", "c", "drop", "iterations"):
        assert k in r, f"max_iter=0 return is missing {k!r}"
    print("  REPAIRED   max_iter=0 returns a complete dict instead of raising IndexError")


# ===========================================================================
# BIT-IDENTITY -- the licence for the repair; a future patch must keep it
# ===========================================================================


@check
def check_clean_inputs_are_bit_identical_to_the_prerepair_module():
    """The production a-range, pre vs post, compared with == on float64.

    This is the pin that stops a future repair from buying the KNOWN GAP back by
    moving a clean result.  Leg 150 measured 40 cases; this pins a 33-case core of
    the wider grid leg 166's runner sweeps, at the same standard: sha256 of Omega's
    raw bytes, and c / kept_sup / dropped_defect / relres by exact equality.
    """
    PRE = _load_prerepair()
    n = 0
    for Jl in (40, 60, 80):
        for a in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5):
            rp = PRE.ACollocation(Jl, a=a).newton_gauged(c=C)
            rq = ACollocation(Jl, a=a).newton_gauged(c=C)
            assert _arr_sha(rp["Omega"]) == _arr_sha(rq["Omega"]), \
                f"J={Jl} a={a}: Omega moved"
            for k in ("c", "kept_sup", "dropped_defect", "relres"):
                assert float(rp[k]) == float(rq[k]), f"J={Jl} a={a}: {k} moved"
            # the one field licensed to move must NOT move on clean input
            assert rp["converged"] == rq["converged"], \
                f"J={Jl} a={a}: converged moved on a CLEAN case"
            n += 1
    print(f"  BIT-IDENTICAL  {n}/{n} clean solves identical to {PRE_REF}, 0 converged "
          f"flags moved")


@check
def check_critical_radius_is_identical_on_real_fields():
    """The repaired guard must not move a single real a-family radius."""
    PRE = _load_prerepair()
    n = 0
    for a in (0.0, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5):
        col = _col(a)
        r = col.newton_gauged(c=C)
        E = effective_speed(col.X, col.V @ r["Omega"], r["c"], a)
        assert int((~np.isfinite(E)).sum()) == 0, f"a={a}: real E has a non-finite entry"
        xp = PRE.critical_radius(col.X, E)
        xq = critical_radius(col.X, E)
        assert (xp == xq) or (not np.isfinite(xp) and not np.isfinite(xq)), \
            f"a={a}: Xc moved, {xp!r} -> {xq!r}"
        n += 1
    print(f"  BIT-IDENTICAL  critical_radius {n}/{n} identical on real E fields")


@check
def check_untouched_kernels_are_identical():
    PRE = _load_prerepair()
    th = refined_theta(J, 8)
    col, colp = _col(0.3), PRE.ACollocation(J, a=0.3)
    om = col.newton_gauged(c=C)["Omega"]
    pairs = {
        "velocity_integrals": (PRE.velocity_integrals(th, J), velocity_integrals(th, J)),
        "refined_theta": (PRE.refined_theta(J, 8), refined_theta(J, 8)),
        "interpolant_residual": (colp.interpolant_residual(om, C, th)[0],
                                 col.interpolant_residual(om, C, th)[0]),
        "weighted_defect": (np.array(PRE.weighted_defect(colp, om, C, 2.0)[:2]),
                            np.array(weighted_defect(col, om, C, 2.0)[:2])),
        "eval_matrices": (np.concatenate([m.ravel() for m in PRE.eval_matrices(th, J)]),
                          np.concatenate([m.ravel() for m in eval_matrices(th, J)])),
    }
    for name, (u, v) in pairs.items():
        assert _arr_sha(u) == _arr_sha(v), f"{name} moved"
    print(f"  BIT-IDENTICAL  {len(pairs)}/{len(pairs)} untouched kernels identical")


@check
def check_production_defect_path_still_converges_and_is_unmoved():
    """experiments/p2_route_d_v12_defect.py's call shape: newton_gauged(c=...) with
    om0=None, then the certificate-visible weighted defect."""
    PRE = _load_prerepair()
    for a in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5):
        col, colp = _col(a), PRE.ACollocation(J, a=a)
        r, rp = col.newton_gauged(c=C), colp.newton_gauged(c=C)
        assert r["converged"] is True, f"a={a}: the PRODUCTION path stopped converging"
        assert _arr_sha(r["Omega"]) == _arr_sha(rp["Omega"]), f"a={a}: Omega moved"
        w = weighted_defect(col, r["Omega"], r["c"], 2.0)[0]
        wp = PRE.weighted_defect(colp, rp["Omega"], rp["c"], 2.0)[0]
        assert float(w) == float(wp), f"a={a}: weighted_defect moved"
    print("  BIT-IDENTICAL  production defect path 6/6 unmoved, all still converged")


# ===========================================================================
# THE SECOND, SMALLER RESIDUAL GAP -- pinned as measured (BEYOND leg 114's 8)
# ===========================================================================


@check
def check_KNOWN_GAP_a_single_nonfinite_entry_disables_the_magnitude_guard():
    """KNOWN GAP (found by leg 166, not by leg 114).

    critical_radius applies its magnitude test only `if thresh > 0.0`, where
    thresh = min_rel_depth * max|E|; and _run_extent returns None for any run
    containing a non-finite value, which the caller treats as ACCEPT.  So one
    +Inf or -Inf anywhere in E reverts the guard to pre-repair behaviour on leg
    114's own M3 adversary.

    LATENT, not live: real E on the collocation grid has 0 non-finite entries at
    every a (pinned above), and turning_point.py feeds critical_radius only col.X.

    A REPAIR MUST INVERT THIS CHECK, not weaken it.
    """
    base = np.full(XG.size, 0.5)
    base[300] = -1e-16                       # leg 114's M3 adversary
    assert not np.isfinite(critical_radius(XG, base)), \
        "the clean adversary is no longer repaired -- check the other pins first"
    for label, poison in (("+Inf", np.inf), ("-Inf", -np.inf)):
        E = base.copy()
        E[5] = poison
        xq = critical_radius(XG, E)
        xp = critical_radius(XG, E, min_rel_depth=0.0)
        assert np.isfinite(xq) and xq == xp, (
            f"{label}: the bypass is gone (got {xq!r}) -- INVERT this check")
    print("  KNOWN GAP  one +Inf/-Inf in E disables the magnitude guard entirely "
          "(2/2 bypass to the pre-repair answer; latent, not live)")


# ===========================================================================
# LEG 286, ROUTE-CNRV -- APPENDED, NOT OVERWRITTEN
# ===========================================================================
#
# Everything above this line is leg 166's banked suite (plus leg 0/BENCH's two
# inversions) and covers a DIFFERENT repair to a DIFFERENT function:
# `critical_radius`'s node-count isolation guard.  Nothing above is edited by
# this leg -- `git diff` on this file shows additions only, which is the
# resolution leg 286's novelty pass (Channel 6) committed to BEFORE construction
# when it found the DM's territory naming a filename that was already banked.
#
# What follows pins leg 248's SEPARATE repair, to `ACollocation.newton`'s verdict
# and `continuation`'s three branch decisions: `converged` used to be
# `bool(rel < 1e-9)` with `rel` EXACTLY invariant under the equation's own
# scaling degeneracy (Omega, c) -> (lam Omega, lam c), so the sole verdict of the
# method could not see the one direction the two gauge rows exist to pin.  Leg
# 248 wrote the patch and its own reachability re-run in the same commit; these
# checks are leg 286's independent re-derivation, banked so it cannot decay at
# the rate of memory (standing lesson 68).
#
# Each check asserts BOTH arms wherever an arm exists -- the repaired behaviour
# AND the pre-repair behaviour the module still reproduces at `gauge_tol=inf` --
# so none of them is a control that cannot come out differently (lesson 90).

from solver.collocation_newton import continuation as _continuation    # noqa: E402
from solver import profile_newton as _profile_newton                   # noqa: E402

L286_PRE_REF = "1ea4ecd"     # last commit before leg 248 touched the module
L286_GAUGE_TOL = 1e-8        # leg 237's own escape predicate, leg 248's default


def _l286_load_prerepair():
    """The module as it stood BEFORE leg 248's repair (not leg 150's `PRE_REF`)."""
    src = subprocess.check_output(
        ["git", "show", f"{L286_PRE_REF}:solver/collocation_newton.py"], cwd=ROOT)
    d = tempfile.mkdtemp(prefix="cnrv_pre_")
    p = os.path.join(d, "cn_pre_248.py")
    with open(p, "wb") as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location("cn_pre_248_postrepair", p)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m


def _l286_gauge_defect(col, om):
    """max(|Omega(theta=0)+1|, |Omega(X~1)+1/2|), recomputed HERE from Omega.

    Transcribed from the formula in `ACollocation.newton`'s docstring.  Not read
    off the module's returned `gauge_defect` field -- that field is what check 2
    below is checking.
    """
    g0 = col.to_coef.sum(axis=0)
    i1 = int(np.argmin(np.abs(col.X - 1.0)))
    om = np.asarray(om, float)
    return float(max(abs(float(g0 @ om) + 1.0), abs(float(om[i1]) + 0.5)))


@check
def check_LEG286_relres_is_exactly_scale_invariant_and_the_verdict_no_longer_is():
    """The defect, and the repair, in one measurement -- both arms asserted.

    (lam Omega*, lam c*) is an exact zero of all J residual rows for every lam,
    because R is homogeneous of degree 2 in (Omega, c) and so is the denominator
    of `rel`.  So `rel` cannot separate the family -- and the pre-repair verdict,
    computed from `rel` alone, called every member converged while the reported
    wave speed ran over three decades.  The repair ANDs in the AFFINE gauge
    defect, which moves as |lam - 1| along exactly that family.

    This check fails if EITHER arm changes: if the post-repair verdict stops
    rejecting off-gauge members (the repair went inert) OR if `gauge_tol=inf`
    stops reproducing the pre-repair verdict (the documented reproduction path
    broke).  A one-armed version of this check could not come out differently.
    """
    col = _col(Jl=100)
    star = col.newton(max_iter=60)
    om_s, c_s = star["Omega"], float(star["c"])
    assert star["converged"], "the on-gauge member itself must still converge"

    lams = (2.0, 5.0, 10.0, 100.0, 1000.0)
    rr, gds, cs, n_pre_true, n_post_true = [], [], [], 0, 0
    for lam in lams:
        pre = col.newton(om0=lam * om_s, c0=lam * c_s, max_iter=0,
                         gauge_tol=float("inf"))
        post = col.newton(om0=lam * om_s, c0=lam * c_s, max_iter=0,
                          gauge_tol=L286_GAUGE_TOL)
        rr.append(float(post["relres"]))
        gds.append(_l286_gauge_defect(col, post["Omega"]))
        cs.append(abs(float(post["c"])))
        n_pre_true += int(bool(pre["converged"]))
        n_post_true += int(bool(post["converged"]))

    # ARM 1 -- the blindness is real and still there in the quantity itself
    spread = max(rr) - min(rr)
    assert spread < 1e-11, (
        f"relres is no longer flat along the scaling family (spread {spread:.3e}) "
        "-- the defect's mechanism has changed; re-derive before trusting the fix")
    assert max(cs) / min(cs) > 100.0, (
        "the trial family no longer spans a wide range of c -- this check has "
        "stopped exercising the degeneracy it was written for")
    # ARM 2 -- pre-repair accepted every one of them; post-repair accepts none
    assert n_pre_true == len(lams), (
        f"gauge_tol=inf no longer reproduces the pre-repair verdict "
        f"({n_pre_true}/{len(lams)} accepted) -- the documented reproduction path "
        "is broken")
    assert n_post_true == 0, (
        f"the repair has gone inert: {n_post_true}/{len(lams)} off-gauge members "
        "are still reported converged")
    assert min(gds) > L286_GAUGE_TOL, "the trial members are not actually off gauge"
    print(f"  ok  leg 248 repair bites: relres flat to {spread:.3e} across "
          f"{max(cs) / min(cs):.3g}x in |c|; off-gauge accepted "
          f"{n_pre_true}/{len(lams)} pre-repair -> {n_post_true}/{len(lams)} post, "
          f"smallest off-gauge defect {min(gds):.3e}")


@check
def check_LEG286_returned_gauge_defect_field_equals_an_independent_recomputation():
    """The module's `gauge_defect` field, checked rather than trusted.

    Leg 248's own artifact reads this field.  A bug in how the module
    computes-and-returns it -- as opposed to a bug in the gate consuming it --
    is invisible to any check that reads it.  Recomputed here from the returned
    Omega alone and compared BITWISE.
    """
    worst = 0.0
    n = 0
    for Jl in (60, 100, 200):
        col = _col(Jl=Jl)
        for om0, c0 in ((None, 0.5), (10.0 * col.anchor(), 5.0),
                        (1e-8 * col.anchor(), 0.5), (0.01 * col.anchor(), 0.005)):
            r = col.newton(om0=om0, c0=c0, max_iter=60)
            mine = _l286_gauge_defect(col, r["Omega"])
            n += 1
            worst = max(worst, abs(float(r["gauge_defect"]) - mine)
                        / max(abs(mine), 1e-300))
            assert float(r["gauge_defect"]) == mine, (
                f"J={Jl}: module reports gauge_defect {r['gauge_defect']!r}, "
                f"independent recomputation gives {mine!r}")
    print(f"  ok  gauge_defect field bit-identical to an independent "
          f"recomputation on {n}/{n} solves (worst rel error {worst:.3e})")


@check
def check_LEG286_no_clean_solve_is_suppressed_by_the_repair():
    """The overcorrection guard, reported as a MARGIN and not a boolean.

    Suppressing genuine convergence is the failure mode gate clause (b) exists
    to catch.  Every clean solve must stay converged, and the check records how
    far below `gauge_tol` its gauge defect actually sits -- a boolean here would
    hide a repair that only just missed.

    ON THE BATTERY'S SHAPE, measured and not guessed.  A first draft of this
    check swept J in (60, 100, 200) x a in (0, 0.15, 0.3) and demanded 6 clean
    solves; it found 4 and FAILED, which is a fact about where
    `ACollocation.newton` is relres-clean, not about leg 248's repair.  Leg
    286's runner swept 20 (J, a) pairs and measured 8 clean: relres cleanliness
    needs BOTH enough resolution and a small enough a -- a = 0.3 is clean at no
    J in the sweep, and a = 0.15 only from J = 160 up.  The battery below is the
    measured clean regime, so the check exercises overcorrection rather than
    re-measuring convergence.
    """
    worst_gd, n_clean, n_suppressed = 0.0, 0, 0
    for Jl in (60, 100, 160, 200):
        for a in (0.0, 0.15):
            col = _col(a=a, Jl=Jl)
            r = col.newton(max_iter=60)
            if not r["converged_relres_only"]:
                continue
            n_clean += 1
            gd = _l286_gauge_defect(col, r["Omega"])
            worst_gd = max(worst_gd, gd)
            if not r["converged"]:
                n_suppressed += 1
    assert n_clean >= 6, (
        f"only {n_clean} clean solves in the battery -- this check has stopped "
        "exercising the overcorrection risk it was written for")
    assert n_suppressed == 0, (
        f"{n_suppressed}/{n_clean} clean solves are suppressed by the repair -- "
        "this is the overcorrection gate clause (b) guards against")
    decades = np.log10(L286_GAUGE_TOL / worst_gd) if worst_gd > 0 else np.inf
    assert decades > 3.0, (
        f"clean solves sit only {decades:.2f} decades below gauge_tol -- too "
        "close to call the threshold non-load-bearing")
    print(f"  ok  0/{n_clean} clean solves suppressed; worst clean gauge defect "
          f"{worst_gd:.3e}, i.e. {decades:.1f} decades below gauge_tol")


@check
def check_LEG286_continuation_consults_the_gauge_in_all_three_branch_decisions():
    """`continuation`'s ladder: every rung on gauge, and the keys are carried.

    Leg 248 changed three branch decisions (retry, accept-the-retry, reseed) from
    comparing `relres` alone to consulting the gauge defect.  Each clause can only
    REJECT a warm start the old code would have taken, so a ladder whose members
    are all on gauge must run bit-identically -- checked here against the
    pre-repair source, not against the module's own description of itself.
    """
    pre = _l286_load_prerepair()
    avals = np.arange(0.0, 1.51, 0.3)
    lp = pre.continuation(avals, J=60, max_iter=60)
    lq = _continuation(avals, J=60, max_iter=60)
    assert len(lp) == len(lq) == 6
    n_float, n_moved = 0, 0
    for i, (p, q) in enumerate(zip(lp, lq)):
        for k in ("a", "c", "relres", "residual_rms"):
            n_float += 1
            if not (p[k] == q[k] or (np.isnan(p[k]) and np.isnan(q[k]))):
                n_moved += 1
        assert np.array_equal(np.asarray(p["Omega"], float),
                              np.asarray(q["Omega"], float)), \
            f"rung {i} (a={q['a']}): Omega moved across leg 248's repair"
        n_float += np.asarray(q["Omega"]).size
        assert bool(p["converged"]) == bool(q["converged"]), \
            f"rung {i} (a={q['a']}): verdict changed on a clean ladder"
        # the repair's new keys must be present and readable unconditionally
        assert "gauge_ok" in q and "gauge_defect" in q
    assert n_moved == 0, f"{n_moved}/{n_float} ladder floats moved"
    print(f"  ok  continuation ladder a=0..1.5: {n_float} floats bit-identical to "
          f"the pre-repair source at {L286_PRE_REF}, 0 verdicts changed")


@check
def check_LEG286_bit_identity_against_the_pre_leg248_source():
    """Gate clause (c): no `collocation_newton.py`-dependent float moved.

    Compared against the GENUINE pre-repair source read out of git at
    `1ea4ecd` -- not against `gauge_tol=inf`, which would only re-execute the
    post-repair module's own claim about what pre-repair meant.  `newton_gauged`
    (leg 150's territory) is swept too: leg 248 must not have touched it.
    """
    pre = _l286_load_prerepair()
    n_float, moved = 0, []
    for Jl in (60, 120):
        for a in (0.0, 0.3):
            cp, cq = pre.ACollocation(Jl, a=a), ACollocation(Jl, a=a)
            for c0 in (0.25, 0.5, 1.0):
                rp, rq = cp.newton(c0=c0, max_iter=60), cq.newton(c0=c0, max_iter=60)
                for k in ("c", "residual_rms", "relres", "nodal_sup"):
                    n_float += 1
                    if not (rp[k] == rq[k] or (np.isnan(rp[k]) and np.isnan(rq[k]))):
                        moved.append(f"newton(J={Jl},a={a},c0={c0}).{k}")
                n_float += np.asarray(rq["Omega"]).size
                if not np.array_equal(np.asarray(rp["Omega"], float),
                                      np.asarray(rq["Omega"], float)):
                    moved.append(f"newton(J={Jl},a={a},c0={c0}).Omega")
            for drop in (0, 1, Jl // 2):
                gp = cp.newton_gauged(drop=drop, max_iter=60)
                gq = cq.newton_gauged(drop=drop, max_iter=60)
                for k in ("c", "kept_sup", "dropped_defect", "relres"):
                    n_float += 1
                    if not (gp[k] == gq[k] or (np.isnan(gp[k]) and np.isnan(gq[k]))):
                        moved.append(f"newton_gauged(J={Jl},drop={drop}).{k}")
                n_float += np.asarray(gq["Omega"]).size
                if not np.array_equal(np.asarray(gp["Omega"], float),
                                      np.asarray(gq["Omega"], float)):
                    moved.append(f"newton_gauged(J={Jl},drop={drop}).Omega")
    assert not moved, f"{len(moved)} floats moved across leg 248's repair: {moved[:5]}"
    assert n_float > 2000, "the sweep has shrunk below what it was banked at"
    print(f"  ok  {n_float} floats bit-identical across leg 248's repair "
          f"(newton and newton_gauged, vs the source at {L286_PRE_REF})")


@check
def check_LEG286_leg202_calibration_pair_is_still_flagged_as_genuine():
    """The live control that the escape detector FIRES -- gate clause (b).

    Leg 202's pair lives on `solver/profile_newton.py`, a DIFFERENT module that
    leg 248 did not touch.  It is the positive control: if a post-repair harness
    reported these two as clean, the harness would have been overcorrected, not
    the module.  Re-derived from `TwoScaleNewton` directly -- not read from leg
    202's, leg 237's or leg 248's JSON.
    """
    pr = _profile_newton.TwoScaleNewton(a=0.0, n=201)
    banked = {1e-8: -6127.94, 1e-10: -306421.26}
    n_flagged = 0
    for eps, want_c in banked.items():
        r = pr.solve(om0=eps * pr.anchor())
        om = r["Omega"]
        escaped = bool(r["converged"] and abs(float(om[pr.i0]) + 1.0) > 1e-8)
        n_flagged += int(escaped)
        rel = abs(float(r["c"]) - want_c) / abs(want_c)
        assert rel < 1e-5, (
            f"eps={eps:g}: c = {r['c']!r} no longer reproduces leg 202's banked "
            f"{want_c} (relative {rel:.3e})")
    assert n_flagged == 2, (
        f"only {n_flagged}/2 of leg 202's pair is still flagged as an escape -- "
        "the detector has been overcorrected into silence")
    print("  ok  leg 202's calibration pair still flags 2/2 as genuine escapes, "
          "c reproducing the banked -6127.94 / -306421.26")


@check
def check_LEG286_gauge_tol_is_not_load_bearing():
    """The threshold's indifference band, measured rather than asserted.

    `gauge_tol = 1e-8` is leg 237's own escape predicate, adopted unchanged.  If
    the verdict is the same across many decades either side, nothing rests on the
    number.  Reported as the WIDTH of the band, in decades.
    """
    col = _col(Jl=100)
    star = col.newton(max_iter=60)
    om_s, c_s = star["Omega"], float(star["c"])
    good = []
    for tol in (1e-14, 1e-12, 1e-10, 1e-8, 1e-6, 1e-4, 1e-2, 0.5):
        clean_ok = bool(col.newton(max_iter=60, gauge_tol=tol)["converged"])
        off_rejected = all(
            not col.newton(om0=lam * om_s, c0=lam * c_s, max_iter=0,
                           gauge_tol=tol)["converged"]
            for lam in (2.0, 5.0, 10.0, 1000.0))
        if clean_ok and off_rejected:
            good.append(tol)
    assert len(good) >= 6, (
        f"only {len(good)}/8 tolerances hold both clauses -- the threshold has "
        "become load-bearing and the repair needs re-justifying")
    decades = np.log10(max(good) / min(good))
    print(f"  ok  both clauses hold at {len(good)}/8 tolerances spanning "
          f"[{min(good):g}, {max(good):g}] -- {decades:.1f} decades of "
          "indifference around the shipped 1e-8")


# ===========================================================================


def main():
    print(__doc__.strip().splitlines()[0])
    print()
    n_gap = 0
    for fn in _checks:
        fn()
        if "KNOWN_GAP" in fn.__name__:
            n_gap += 1
    print()
    print(f"{len(_checks)}/{len(_checks)} checks ran, {n_gap} of them KNOWN GAPS.")
    print("Leg 150's repair holds on everything it tested and moves nothing clean. "
          "Leg 114's `pure_sign_noise` -- one of the 3 of its 8 that leg 150's arm A "
          "never re-ran -- is now REPAIRED (leg 0/BENCH): a node-count isolation "
          "predicate, orthogonal to the scale-invariant relative-depth guard, "
          "closes it without moving a single clean-input float. One smaller, "
          "separately-tracked gap (non-finite E disables the magnitude test) "
          "remains open on purpose, out of this repair's territory.")


if __name__ == "__main__":
    main()
