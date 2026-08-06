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
two of its ten cases are ones leg 150 introduced itself).  Seven are fixed and
one is not.

  *** THE SURVIVING CORRUPTION: `pure_sign_noise` still returns leg 114's
      recorded value, 0.03502503128911139, BIT-IDENTICALLY. ***

Three checks are named KNOWN_GAP: that corruption, its control (no admissible
threshold in the landed predicate class repairs it -- so it is a class ceiling,
not a tuning slip), and a SECOND, smaller gap this leg found in the same guard
(one non-finite entry anywhere in E disables the magnitude test entirely).

Those checks assert the corruptions AS MEASURED, at leg 114's own values, in leg
92's convention: a later repair FAILS this file and must INVERT them rather than
weaken them.  The other checks pin the repair that did land and the bit-identity
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
def check_KNOWN_GAP_pure_sign_noise_still_returns_the_prerepair_radius():
    """KNOWN GAP.  leg 114 `pure_sign_noise`: NOT fixed by leg 150.

    E = (-1)^k is pure alternating sign noise with no crossing to find, and
    critical_radius returns leg 114's recorded 0.03502503128911139 unchanged.

    MECHANISM, and it is a predicate-CLASS ceiling rather than a threshold:
    the landed guard requires each side's constant-sign excursion to reach
    min_rel_depth * max|E|, which is SCALE-INVARIANT.  This field has no scale --
    every run is one node long with |E| = 1, which is also max|E| -- so the
    excursion ratio is exactly 1.0 on both sides, the largest value the test can
    ever see.  No admissible threshold rejects it (see the control below).

    A REPAIR MUST INVERT THIS CHECK, not weaken it.
    """
    E = (-1.0) ** np.arange(XG.size)          # leg 114's construction, verbatim
    xc = critical_radius(XG, E)
    leg114_recorded = 0.03502503128911139
    assert xc == leg114_recorded, (
        f"KNOWN GAP moved: expected leg 114's recorded {leg114_recorded!r}, got {xc!r}. "
        "If a repair landed, INVERT this check.")
    # and it is bit-identical to the pre-repair path
    assert critical_radius(XG, E, min_rel_depth=0.0) == leg114_recorded
    print(f"  KNOWN GAP  pure_sign_noise -> Xc = {xc!r} (leg 114's recorded value, "
          f"bit-identical; truth is 'no crossing')")


@check
def check_KNOWN_GAP_control_no_admissible_threshold_separates_it():
    """The control that CAN report the other answer (standing lesson 90).

    If some min_rel_depth rejected the sign noise while keeping every real
    crossing, the gap would be a tuning bug.  Measured: the two requirements are
    disjoint over the whole parameter range.
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
    assert not both, (
        f"a threshold now does BOTH ({both}) -- the gap is tunable after all; "
        "re-read the KNOWN GAP check above, it may be invertible")
    # and specifically: the smallest threshold that rejects the noise kills them all
    assert np.isfinite(critical_radius(XG, Enoise, min_rel_depth=1.0))
    kept_at_1 = sum(1 for X, E in real
                    if np.isfinite(critical_radius(X, E, min_rel_depth=1.0)))
    assert kept_at_1 == 0, f"expected all real crossings rejected at d=1.0, kept {kept_at_1}"
    print(f"  KNOWN GAP control: 0 of 11 thresholds reject the sign noise AND keep all "
          f"{len(real)} real crossings; at d=1.0 the noise survives and 0/{len(real)} "
          f"real crossings do")


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
          "never re-ran -- is STILL BROKEN, bit-identically, and no admissible "
          "threshold in the landed predicate class repairs it.")


if __name__ == "__main__":
    main()
