"""Route-TNR, leg 220: the REPAIR of `solver/target_norm.py`'s domain-guard WINDOW.

WHAT THIS REPAIRS, AND WHAT IT DOES NOT
--------------------------------------------------------------------------
Leg 204 (Route-TNA2) ran a fourth adversarial pass over `solver/target_norm.py` and found a
hole in the very guard legs 84, `dc812c1` (bench) and 94 were spent building and validating.
The guard's THRESHOLD was right (`n_outside_grid > 0`, dynamic) and its PROPAGATION was
right (threaded through all five result-bearing surfaces).  Its **window** was wrong:

    compactify tested   inside = |Xt| <= |X|.max()

For a grid symmetric about zero that IS the data interval `[min X, max X]`.  For any other
grid it is strictly larger, and every theta-sample in the gap was handed to
`lagrange_interp_uniform`, whose index clip turns it into polynomial EXTRAPOLATION.
`n_outside_grid` counted only samples beyond `max|X|`, so it reported **0** -- with
`domain_valid = True` and zero warnings.

The repair is one predicate wide, plus the two far-field sites that read the same symmetric
assumption (leg 204 named the predicate; it did not name these two -- see
`writeup/novelty/leg_220.md` R2):

    inside = (Xt >= X_lo) & (Xt <= X_hi)        # the window IS the data interval
    above  = Xt > X_hi                          # was `Xt > 0`: which edge to continue FROM
    scale  = where(above, X_hi, -X_lo)          # was `X_max` for both sides

**ONE of leg 204's seven mechanisms is repaired here.**  The other six are untouched and
explicitly NOT closed: `domain_fields`' `int()` truncation, `analytic_tail`'s unvalidated
`C`/`N`, the fitter's `n_points` overstatement, descending `k` into `weighted_partial_sums`,
shuffled `X`/`f` pairing, and a mismatched sinh scale `c`.  Part D re-measures all six
against the repaired module so that "not closed" is a number and not a promise.

GATE (pre-committed, both branches, exact wording)
--------------------------------------------------------------------------
"Does repairing the domain guard to window on the true data interval (per leg 204's own
identified mechanism) cause the asymmetric-grid extrapolation case to now be correctly
flagged (`n_outside_grid>0`/`domain_valid=False`), while leg 55's own banked margins and
every other live call stay bit-identical?"

    yes -> Bank the repair; leg 204's finding closes cleanly.  A postrepair-verification leg
           should be queued once a slot is available.  Normal landing straight to `main`.
    no  -> Report exactly which case resists the fix or which banked margin moved; escalate
           immediately.  Push the branch only, never `main`.

THE FOUR PARTS
--------------------------------------------------------------------------
  A. ZERO REGRESSION, A/B.  The pre-repair module is loaded straight out of git at
     `dc812c1` -- the bench repair that landed the guard, the module's last-touching commit,
     an old stable ancestor of `origin/main` (leg 130's correction: never pin this leg's own
     hashes, the rebase rewrites them).  Both versions are imported into the SAME process
     and called on every symmetric-grid surface.  Comparison is `==` on raw float64, never
     `allclose`.  Every value the old module returned must be bit-identical; only new KEYS
     may appear.
  B. THE HEADLINE: leg 204's asymmetry ladder, re-run against both modules.  The repaired
     module must flag every rung the old one silently passed, with the extrapolated-sample
     count now REPORTED rather than computed by the harness.
  C. LEG 55'S BANKED MARGINS, the load-bearing regression check.  Leg 55's OWN `nb5_norms`
     path -- its `solve_target`, its `_measure`, imported from
     `experiments/p2_route_nb_v1_targetnorm.py`, not reimplemented -- re-run through the
     repaired module and compared to the two banked numbers at `== 0.0` difference.
  D. WHAT IS STILL OPEN.  Leg 204's other six mechanisms, re-measured post-repair.

Run:    `.venv/bin/python experiments/p2_route_tnr_v1_repair.py`
Writes: `writeup/data/p2_route_tnr_v1_repair.json`
"""

import json
import os
import subprocess
import sys
import types
import warnings

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

from solver import target_norm as new                                     # noqa: E402
from solver.hl_rescaled import sinh_grid_origin                           # noqa: E402
from solver.target_norm import TargetNormDomainWarning                    # noqa: E402
from p2_route_nb_v1_targetnorm import (                                   # noqa: E402
    BAND, S_VALUES, _measure, solve_target,
)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_tnr_v1_repair.json")

# The module as it stood BEFORE this leg: the bench repair that landed the guard.  The
# module is byte-unchanged between dc812c1 and origin/main, and dc812c1 is an ancestor of
# origin/main, so this pin survives any rebase (leg 130's correction, d871675).
PRE_REPAIR_REF = os.environ.get("TNR_PRE_REPAIR_REF", "dc812c1")

# leg 204's instrument, verbatim, so the two legs' numbers are directly comparable
ALPHA, P_TRUE = 0.4, 1.4
M, N_GRID = 16384, 801
K_LO, K_HI = 32, 256
S_PROBE = 0.3

# leg 55's two banked margins, transcribed from
# writeup/data/p2_route_nb_v1_targetnorm.json (NB5_norms.classes[*].verdict.
# margin_in_exponent_units), via experiments/bench_target_norm_domain_guard_check.py.
# READ, NEVER WRITTEN.
LEG55_BANKED = {0.0: 0.39374453128859876, 0.3: 0.09374453128859872}
LEG55_BANKED_P = 1.3937445312885988
LEG55_HEADLINE_RHO_MAX = 12.0        # nb5_norms(n=801, rho_max=12.0)
LEG55_SHIPPED_RHO_MAX = 8.0          # the domain where leg 84's 14 samples fall outside


def load_prerepair():
    """Import the PRE-repair solver/target_norm.py out of git as a separate module."""
    src = subprocess.run(["git", "show", f"{PRE_REPAIR_REF}:solver/target_norm.py"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    mod = types.ModuleType("target_norm_prerepair")
    mod.__file__ = f"<{PRE_REPAIR_REF}:solver/target_norm.py>"
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod, src


def _same(vn, vo):
    """Bit-identity on raw float64.  NaN == NaN counts as same; nothing else is relaxed."""
    if isinstance(vo, np.ndarray) or isinstance(vn, np.ndarray):
        return bool(np.array_equal(np.asarray(vn), np.asarray(vo), equal_nan=True))
    if isinstance(vo, float) and isinstance(vn, float) and np.isnan(vo) and np.isnan(vn):
        return True
    return bool(vn is vo or vn == vo)


def cmp_dict(a, b):
    """Every key the OLD dict carried must be present in the new one and bit-identical."""
    bad = []
    for key, vo in b.items():
        vn = a.get(key, "<MISSING>")
        if not _same(vn, vo):
            bad.append((key, repr(vo), repr(vn)))
    return bad


# --------------------------------------------------------------------------
# A -- zero regression on every symmetric-grid surface
# --------------------------------------------------------------------------
def control_two_modules_really_differ(old, src):
    """LESSON 90 / leg 129's failure mode, asserted executably before any 0-moved is believed.

    A differential reporting "0 values moved" is worth nothing if the two sides are secretly
    the same module object -- leg 129 hit exactly that, and its CONTROL silently reported
    0/33 too.  So: the two modules must be distinct objects, and the pre-repair source must
    provably contain the OLD predicate and provably lack the NEW one.  If any of these fail,
    this runner refuses to report a regression result at all.
    """
    new_src = open(os.path.join(ROOT, "solver", "target_norm.py")).read()
    checks = {
        "distinct_module_objects": bool(old is not new),
        "distinct_compactify_functions": bool(old.compactify is not new.compactify),
        "prerepair_source_has_old_predicate": bool(
            "inside = np.abs(Xt) <= X_max" in src),
        "prerepair_source_lacks_new_predicate": bool(
            "(Xt >= X_lo) & (Xt <= X_hi)" not in src),
        "repaired_source_has_new_predicate": bool(
            "inside = (Xt >= X_lo) & (Xt <= X_hi)" in new_src),
        "repaired_source_lacks_old_predicate": bool(
            "inside = np.abs(Xt) <= X_max" not in new_src),
    }
    # and the behavioural version of the same thing: one input on which they MUST disagree
    Xa = np.linspace(-1.0, 745.0, 601)
    Fa = new.calibration_family(Xa, ALPHA)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", TargetNormDomainWarning)
        _, _, no_o = old.compactify(Xa, Fa, 4096, far_field="power", tail_exponent=-ALPHA)
        _, _, no_n = new.compactify(Xa, Fa, 4096, far_field="power", tail_exponent=-ALPHA)
    checks["disagree_on_an_asymmetric_grid"] = bool(int(no_o) != int(no_n))
    checks["prerepair_count_on_that_grid"] = int(no_o)
    checks["repaired_count_on_that_grid"] = int(no_n)
    ok = all(v for k, v in checks.items() if isinstance(v, bool))
    checks["control_passes"] = ok
    print(f"  control (lesson 90): the two modules really differ -- "
          f"{'PASS' if ok else 'FAIL'}; on an asymmetric probe grid the pre-repair module "
          f"reports {int(no_o)} outside and the repaired one reports {int(no_n)}")
    if not ok:
        raise AssertionError(
            f"the A/B control FAILED, so no 'bit-identical' claim below is admissible: "
            f"{checks}")
    return checks


def part_a(old):
    tail = -ALPHA
    _, X745 = sinh_grid_origin(N_GRID, rho_max=8.0)
    _, XBIG = sinh_grid_origin(N_GRID, rho_max=12.0)
    _, XSML = sinh_grid_origin(201, rho_max=6.0)
    cases, n_leaves = [], 0

    for label, X, ff, te, order in (
            ("in-window     rho_max=12, power, order=8", XBIG, "power", tail, 8),
            ("in-window     rho_max=12, power, order=4", XBIG, "power", tail, 4),
            ("out-of-window rho_max=8,  power", X745, "power", tail, 8),
            ("out-of-window rho_max=8,  clamp", X745, "clamp", None, 8),
            ("out-of-window rho_max=8,  zero", X745, "zero", None, 8),
            ("out-of-window rho_max=6,  n=201, power", XSML, "power", tail, 8),
            ("out-of-window rho_max=6,  n=201, clamp", XSML, "clamp", None, 8),
    ):
        f_new = new.calibration_family(X, ALPHA)
        f_old = old.calibration_family(X, ALPHA)
        assert _same(f_new, f_old), "the calibration family itself moved"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", TargetNormDomainWarning)
            th_n, h_n, no_n = new.compactify(X, f_new, M, far_field=ff,
                                             tail_exponent=te, order=order)
            sp_n = new.spectrum(X, f_new, M=M, far_field=ff, tail_exponent=te, order=order)
            fit_n = new.fit_exponent(sp_n["k"], sp_n["hk"], K_LO, K_HI,
                                     n_outside_grid=sp_n["n_outside_grid"])
            ps_n = new.weighted_partial_sums(sp_n["k"], sp_n["hk"], S_PROBE, [512, 4096],
                                             n_outside_grid=sp_n["n_outside_grid"])
            at_n = new.analytic_tail(fit_n["p"], fit_n["C"], 4096, S_PROBE,
                                     n_outside_grid=sp_n["n_outside_grid"])
            nv_n = new.norm_verdict(fit_n["p"], S_PROBE,
                                    n_outside_grid=sp_n["n_outside_grid"])
            nf_n = new.noise_floor(sp_n["hk"], sp_n["k"])

            th_o, h_o, no_o = old.compactify(X, f_old, M, far_field=ff,
                                             tail_exponent=te, order=order)
            sp_o = old.spectrum(X, f_old, M=M, far_field=ff, tail_exponent=te, order=order)
            fit_o = old.fit_exponent(sp_o["k"], sp_o["hk"], K_LO, K_HI,
                                     n_outside_grid=sp_o["n_outside_grid"])
            ps_o = old.weighted_partial_sums(sp_o["k"], sp_o["hk"], S_PROBE, [512, 4096],
                                             n_outside_grid=sp_o["n_outside_grid"])
            at_o = old.analytic_tail(fit_o["p"], fit_o["C"], 4096, S_PROBE,
                                     n_outside_grid=sp_o["n_outside_grid"])
            nv_o = old.norm_verdict(fit_o["p"], S_PROBE,
                                    n_outside_grid=sp_o["n_outside_grid"])
            nf_o = old.noise_floor(sp_o["hk"], sp_o["k"])

        diffs = (cmp_dict(sp_n, sp_o) + cmp_dict(fit_n, fit_o) + cmp_dict(at_n, at_o)
                 + cmp_dict(nv_n, nv_o)
                 + [d for i in range(2) for d in cmp_dict(ps_n[i], ps_o[i])])
        # the raw compactify leaves too -- the interpolated field itself, all M of it
        raw = []
        if not _same(th_n, th_o):
            raw.append(("compactify.theta", "<array>", "<array>"))
        if not _same(h_n, h_o):
            nd = int(np.sum(~((h_n == h_o) | (np.isnan(h_n) & np.isnan(h_o)))))
            raw.append(("compactify.h", f"{nd} of {h_n.size} samples", "moved"))
        if not _same(int(no_n), int(no_o)):
            raw.append(("compactify.n_outside", repr(no_o), repr(no_n)))
        if not _same(float(nf_n), float(nf_o)):
            raw.append(("noise_floor", repr(float(nf_o)), repr(float(nf_n))))
        diffs += raw
        # leaf count: every scalar/array element actually compared
        n_leaves += (h_n.size + th_n.size + sum(len(d) for d in (sp_o, fit_o, at_o, nv_o))
                     + sum(len(p) for p in ps_o) + 2)

        cases.append({
            "case": label, "far_field": ff, "interp_order": order,
            "X_lo_data": float(X.min()), "X_hi_data": float(X.max()),
            "grid_symmetric_to": float(abs(X.min() + X.max())),
            "n_outside_grid_prerepair": int(no_o),
            "n_outside_grid_repaired": int(no_n),
            "domain_valid_prerepair": sp_o["domain_valid"],
            "domain_valid_repaired": sp_n["domain_valid"],
            "p_prerepair": float(fit_o["p"]), "p_repaired": float(fit_n["p"]),
            "p_bit_identical": bool(float(fit_o["p"]) == float(fit_n["p"])),
            "margin_prerepair": float(nv_o["margin_in_exponent_units"]),
            "margin_repaired": float(nv_n["margin_in_exponent_units"]),
            "margin_bit_identical": bool(float(nv_o["margin_in_exponent_units"])
                                         == float(nv_n["margin_in_exponent_units"])),
            "n_value_differences": len(diffs),
            "differences": [list(d) for d in diffs],
            "new_keys_spectrum": sorted(set(sp_n) - set(sp_o)),
        })
        print(f"  [{'OK ' if not diffs else 'MOVED'}] {label}: "
              f"n_out {no_o} -> {no_n}, p = {float(fit_n['p']):.9f}, "
              f"{len(diffs)} value difference(s)")

    # far_field='none' deliberately leaves NaN and `coefficient_magnitudes` REFUSES it, so
    # it has no downstream to compare -- but the compactified field itself, NaNs and all,
    # must still be leaf-for-leaf identical, and the refusal must still be a refusal.
    none_cases = []
    for label, X in (("rho_max=8", X745), ("rho_max=6, n=201", XSML)):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", TargetNormDomainWarning)
            th_n, h_n, no_n = new.compactify(X, new.calibration_family(X, ALPHA), M,
                                             far_field="none")
            th_o, h_o, no_o = old.compactify(X, old.calibration_family(X, ALPHA), M,
                                             far_field="none")
        refused_n = refused_o = None
        try:
            new.coefficient_magnitudes(h_n)
        except ValueError as e:
            refused_n = type(e).__name__
        try:
            old.coefficient_magnitudes(h_o)
        except ValueError as e:
            refused_o = type(e).__name__
        ident = _same(h_n, h_o) and _same(th_n, th_o) and int(no_n) == int(no_o)
        n_leaves += h_n.size + th_n.size + 2
        none_cases.append({
            "case": f"out-of-window {label}, far_field='none'",
            "n_nan_left_prerepair": int(np.sum(~np.isfinite(h_o))),
            "n_nan_left_repaired": int(np.sum(~np.isfinite(h_n))),
            "n_outside_grid_prerepair": int(no_o),
            "n_outside_grid_repaired": int(no_n),
            "field_bit_identical_including_nan_positions": bool(ident),
            "downstream_refusal_prerepair": refused_o,
            "downstream_refusal_repaired": refused_n,
            "refusal_preserved": bool(refused_n == refused_o == "ValueError"),
        })
        print(f"  [{'OK ' if ident else 'MOVED'}] out-of-window {label}, "
              f"far_field='none': {int(np.sum(~np.isfinite(h_n)))} NaN left, "
              f"downstream still refuses ({refused_n})")

    return {"what": ("A/B of the repaired module against the pre-repair module loaded from "
                     f"git {PRE_REPAIR_REF}, both in the same process; every value the old "
                     "module returned must be bit-identical on raw float64, only new KEYS "
                     "may appear.  All eight cases are on grids SYMMETRIC about zero, "
                     "which is what every live caller supplies"),
            "pre_repair_ref": PRE_REPAIR_REF,
            "cases": cases, "n_cases": len(cases),
            "far_field_none_cases": none_cases,
            "n_leaves_compared": int(n_leaves),
            "n_cases_with_any_value_difference": sum(
                1 for c in cases if c["n_value_differences"]),
            "all_bit_identical": bool(
                all(not c["n_value_differences"] for c in cases)
                and all(c["field_bit_identical_including_nan_positions"]
                        and c["refusal_preserved"] for c in none_cases))}


# --------------------------------------------------------------------------
# B -- THE HEADLINE: leg 204's asymmetry ladder, before and after
# --------------------------------------------------------------------------
def part_b(old):
    """Leg 204's five rungs, verbatim, against both modules.

    The count of extrapolated samples was computed BY THE HARNESS in leg 204, because the
    module would not report it.  Here it is read off the repaired module's own
    `n_outside_grid` as well, and the two must agree -- that agreement is what makes the
    repair a fix and not a different number.
    """
    _, X_BIG = sinh_grid_origin(N_GRID, rho_max=12.0)
    F_BIG = new.calibration_family(X_BIG, ALPHA)
    Xt = new.X_of_theta(new.midpoint_theta_grid(M))
    rungs = []
    print("\n  asymmetry ladder (leg 204's five rungs), pre-repair -> repaired:")
    for cut in (-1000.0, -100.0, -10.0, -1.0, -0.1):
        m = X_BIG > cut
        Xa, Fa = X_BIG[m], F_BIG[m]
        # leg 204's own harness-side truth: samples inside |X|<=max|X| but outside the data
        n_gap_truth = int(((Xt < Xa.min()) & (np.abs(Xt) <= np.abs(Xa).max())).sum())
        n_truth_outside_data = int(((Xt < Xa.min()) | (Xt > Xa.max())).sum())

        with warnings.catch_warnings(record=True) as wo:
            warnings.simplefilter("always")
            sp_o = old.spectrum(Xa, Fa, M=M, far_field="power", tail_exponent=-ALPHA)
            fit_o = old.fit_exponent(sp_o["k"], sp_o["hk"], K_LO, K_HI,
                                     n_outside_grid=sp_o["n_outside_grid"])
            nv_o = old.norm_verdict(fit_o["p"], S_PROBE,
                                    n_outside_grid=sp_o["n_outside_grid"])
        with warnings.catch_warnings(record=True) as wn:
            warnings.simplefilter("always")
            sp_n = new.spectrum(Xa, Fa, M=M, far_field="power", tail_exponent=-ALPHA)
            fit_n = new.fit_exponent(sp_n["k"], sp_n["hk"], K_LO, K_HI,
                                     n_outside_grid=sp_n["n_outside_grid"])
            nv_n = new.norm_verdict(fit_n["p"], S_PROBE,
                                    n_outside_grid=sp_n["n_outside_grid"])
        row = {
            "cut": float(cut),
            "X_min_data": float(Xa.min()), "X_max_data": float(Xa.max()),
            "n_grid_points": int(Xa.size),
            "harness_truth_samples_in_the_gap": n_gap_truth,
            "harness_truth_samples_outside_data": n_truth_outside_data,
            "prerepair": {
                "n_outside_grid_reported": int(sp_o["n_outside_grid"]),
                "domain_valid": sp_o["domain_valid"],
                "n_warnings": len(wo),
                "p": float(fit_o["p"]),
                "err_vs_exact": float(abs(fit_o["p"] - P_TRUE)),
                "finite_reported": bool(nv_o["finite"]),
            },
            "repaired": {
                "n_outside_grid_reported": int(sp_n["n_outside_grid"]),
                "domain_valid": sp_n["domain_valid"],
                "n_warnings": len(wn),
                "p": float(fit_n["p"]),
                "err_vs_exact": float(abs(fit_n["p"] - P_TRUE)),
                "finite_reported": bool(nv_n["finite"]),
            },
        }
        row["count_now_matches_truth"] = bool(
            row["repaired"]["n_outside_grid_reported"] == n_truth_outside_data)
        row["now_flagged"] = bool(row["repaired"]["n_outside_grid_reported"] > 0
                                  and row["repaired"]["domain_valid"] is False
                                  and row["repaired"]["n_warnings"] > 0)
        row["was_silent"] = bool(row["prerepair"]["n_outside_grid_reported"] == 0
                                 and row["prerepair"]["domain_valid"] is True
                                 and row["prerepair"]["n_warnings"] == 0)
        rungs.append(row)
        print(f"    Xmin={row['X_min_data']:10.3f}  gap={n_gap_truth:5d}/{M}  "
              f"PRE: n_out={row['prerepair']['n_outside_grid_reported']:5d} "
              f"valid={str(row['prerepair']['domain_valid']):5s} "
              f"warn={row['prerepair']['n_warnings']}  ->  "
              f"POST: n_out={row['repaired']['n_outside_grid_reported']:5d} "
              f"valid={str(row['repaired']['domain_valid']):5s} "
              f"warn={row['repaired']['n_warnings']}")

    worst = max(rungs, key=lambda r: r["prerepair"]["err_vs_exact"])
    return {"what": ("leg 204's asymmetry ladder verbatim (writeup/data/"
                     "p2_route_tna2_v1_adversarial.json, the `ladder` field of the "
                     "ASYMMETRIC GRID case), re-run against both module versions"),
            "rungs": rungs,
            "n_rungs": len(rungs),
            "n_rungs_silent_prerepair": sum(1 for r in rungs if r["was_silent"]),
            "n_rungs_flagged_repaired": sum(1 for r in rungs if r["now_flagged"]),
            "n_rungs_count_matches_truth": sum(
                1 for r in rungs if r["count_now_matches_truth"]),
            "worst_rung": {
                "X_min_data": worst["X_min_data"],
                "n_grid_points": worst["n_grid_points"],
                "samples_in_the_gap": worst["harness_truth_samples_in_the_gap"],
                "prerepair_reported": worst["prerepair"]["n_outside_grid_reported"],
                "repaired_reported": worst["repaired"]["n_outside_grid_reported"],
                "prerepair_p": worst["prerepair"]["p"],
                "prerepair_err_vs_exact": worst["prerepair"]["err_vs_exact"],
            },
            "reading": ("the repair does not make the extrapolated ANSWER right -- it "
                        "cannot, the data are not there.  It makes the answer VISIBLE: "
                        "the same p comes back, now with a positive count, "
                        "domain_valid = False and a TargetNormDomainWarning attached")}


# --------------------------------------------------------------------------
# C -- leg 55's banked margins, the load-bearing regression check
# --------------------------------------------------------------------------
def rerun_leg55(rho_max, n=801):
    """Leg 55's nb5_norms path verbatim -- its solve, its _measure, its S_VALUES."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        s = solve_target(n, rho_max=rho_max)
        sp, fit = _measure(s["b"].X, s["Omega"], s["c_omega"] / s["c_l"])
        k, hk = sp["k"], sp["hk"]
        p, C = fit["p"], fit["C"]
        n_out = int(sp["n_outside_grid"])
        classes = []
        for sv in S_VALUES:
            ps = new.weighted_partial_sums(k, hk, sv, [16, 64, 256, 1024, 4096],
                                           n_outside_grid=n_out)
            tail = new.analytic_tail(p, C, 4096, sv, n_outside_grid=n_out)
            v = new.norm_verdict(p, sv, alpha=s["alpha"], n_outside_grid=n_out)
            classes.append({"s": float(sv), "verdict": v,
                            "S_N_at_4096": float(ps[-1]["S_N"]),
                            "tail_finite": bool(tail["finite"])})
        warned = [str(x.message) for x in w
                  if issubclass(x.category, TargetNormDomainWarning)]
    X = s["b"].X
    return {"rho_max": float(rho_max), "n": int(n),
            "X_lo_data": float(X.min()), "X_hi_data": float(X.max()),
            "grid_symmetric_to": float(abs(X.min() + X.max())),
            "grid_strictly_ascending": bool(np.all(np.diff(X) > 0)),
            "alpha": float(s["alpha"]), "p": float(p), "C": float(C),
            "converged": bool(s["converged"]), "residual": float(s["residual"]),
            "n_theta_points_outside_grid": n_out,
            "domain_valid": sp["domain_valid"],
            "n_domain_warnings_raised": len(warned),
            "classes": classes}


def part_c():
    head = rerun_leg55(LEG55_HEADLINE_RHO_MAX)
    ship = rerun_leg55(LEG55_SHIPPED_RHO_MAX)
    rows = []
    for sv in (0.0, 0.3):
        ch = next(c for c in head["classes"] if c["s"] == sv)
        cs = next(c for c in ship["classes"] if c["s"] == sv)
        banked = LEG55_BANKED[sv]
        got = float(ch["verdict"]["margin_in_exponent_units"])
        rows.append({
            "s": sv,
            "leg55_banked_margin": banked,
            "rerun_margin_through_repaired_module": got,
            "abs_difference_vs_banked": abs(got - banked),
            "bit_identical_to_banked": bool(got == banked),
            "headline_domain_valid": ch["verdict"]["domain_valid"],
            "headline_finite": bool(ch["verdict"]["finite"]),
            "counterfactual_margin_at_shipped_745_domain": float(
                cs["verdict"]["margin_in_exponent_units"]),
            "counterfactual_domain_valid": cs["verdict"]["domain_valid"],
        })
        print(f"    s = {sv}: banked {banked:.17g}  rerun {got:.17g}  "
              f"diff {abs(got - banked):.3g}  bit-identical "
              f"{bool(got == banked)}")
    print(f"    p: banked {LEG55_BANKED_P:.17g}  rerun {head['p']:.17g}  "
          f"bit-identical {bool(head['p'] == LEG55_BANKED_P)}")
    return {"what": ("leg 55's OWN nb5_norms path -- its solve_target, its _measure, its "
                     "S_VALUES, imported from experiments/p2_route_nb_v1_targetnorm.py and "
                     "not reimplemented -- re-run through the REPAIRED module.  This is the "
                     "load-bearing regression check: the two margins are cited across the "
                     "repo and must not move by one ULP"),
            "headline_domain": head, "shipped_domain": ship,
            "banked_p": LEG55_BANKED_P,
            "rerun_p": head["p"],
            "p_bit_identical_to_banked": bool(head["p"] == LEG55_BANKED_P),
            "margins": rows,
            "n_margins_bit_identical": sum(1 for r in rows if r["bit_identical_to_banked"]),
            "n_margins": len(rows),
            "why_it_could_not_move": (
                "the solve grid is symmetric about zero to "
                f"{head['grid_symmetric_to']:.1e} and strictly ascending, so X_lo = -X_hi "
                "exactly and all three repaired expressions reduce to the pre-repair ones "
                "bit for bit.  This is measured here, not argued: the equality is on raw "
                "float64 against the transcribed banked constants")}


# --------------------------------------------------------------------------
# D -- what is still open: leg 204's other six mechanisms, post-repair
# --------------------------------------------------------------------------
def part_d():
    """Six mechanisms this leg did NOT repair, re-measured so 'open' is a number."""
    _, X = sinh_grid_origin(N_GRID, rho_max=12.0)
    F = new.calibration_family(X, ALPHA)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", TargetNormDomainWarning)
        sp = new.spectrum(X, F, M=M, far_field="power", tail_exponent=-ALPHA)
    k, hk = sp["k"], sp["hk"]
    rows = []

    # 1. domain_fields' int() truncation
    sweep = []
    for bad in (0.9, 0.5, 0.0008544921875, -0.5, True, "0", "3"):
        df = new.domain_fields(bad)
        sweep.append({"input": repr(bad), "n_outside_grid": df["n_outside_grid"],
                      "domain_valid": df["domain_valid"]})
    n_clean = sum(1 for t in sweep if t["domain_valid"] is True)
    rows.append({"mechanism": "domain_fields int() truncation / no type check",
                 "status": "STILL OPEN",
                 "magnitude": (f"{n_clean} of {len(sweep)} type-compatible wrong values "
                               "still read domain_valid = True, including every fraction "
                               "in (-1, 1) and the STRING '0'"),
                 "sweep": sweep})

    # 2. analytic_tail's unvalidated C and N
    at = []
    for label, C, N in (("C = NaN", float("nan"), 4096), ("C = Inf", float("inf"), 4096),
                        ("C = -0.5", -0.5, 4096), ("N = NaN", 1.0, float("nan"))):
        d = new.analytic_tail(1.4, C, N, S_PROBE)
        at.append({"case": label, "finite": bool(d["finite"]),
                   "bound": (None if d["bound"] is None else float(d["bound"])),
                   "reason": d.get("reason")})
    rows.append({"mechanism": "analytic_tail validates margin and nothing else",
                 "status": "STILL OPEN",
                 "magnitude": (f"{sum(1 for a in at if a['finite'])} of {len(at)} corrupt "
                               "parameter sets still return finite = True, including a "
                               "NEGATIVE upper bound on a sum of non-negative terms"),
                 "cases": at})

    # 3. descending k into weighted_partial_sums
    S_ok = new.weighted_partial_sums(k, hk, S_PROBE, [64, 4096], n_outside_grid=0)
    S_rev = new.weighted_partial_sums(k[::-1], hk, S_PROBE, [64, 4096], n_outside_grid=0)
    ratio = float(S_rev[1]["S_N"] / S_ok[1]["S_N"])
    rows.append({"mechanism": "descending k into weighted_partial_sums (searchsorted)",
                 "status": "STILL OPEN",
                 "magnitude": (f"S_64 = {float(S_rev[0]['S_N']):.6f} against the true "
                               f"{float(S_ok[0]['S_N']):.6f}, and S_4096 overstated by "
                               f"{ratio:.2f}x; domain_valid = True, 0 warnings"),
                 "S_64_wrong": float(S_rev[0]["S_N"]), "S_64_true": float(S_ok[0]["S_N"]),
                 "S_4096_overstatement": ratio})

    # 4. shuffled X/f pairing -- NOT a windowing defect, so the repair must not catch it
    rng = np.random.default_rng(0)
    perm = rng.permutation(F.size)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        sp_sh = new.spectrum(X, F[perm], M=M, far_field="power", tail_exponent=-ALPHA)
        fit_sh = new.fit_exponent(sp_sh["k"], sp_sh["hk"], K_LO, K_HI,
                                  n_outside_grid=sp_sh["n_outside_grid"])
    rows.append({"mechanism": "shuffled X/f pairing",
                 "status": "STILL OPEN",
                 "magnitude": (f"p = {float(fit_sh['p']):.6e} against the exact {P_TRUE}, "
                               f"with n_outside_grid = {int(sp_sh['n_outside_grid'])}, "
                               f"domain_valid = {sp_sh['domain_valid']}, {len(w)} warnings"),
                 "p": float(fit_sh["p"]),
                 "n_outside_grid": int(sp_sh["n_outside_grid"]),
                 "domain_valid": sp_sh["domain_valid"], "n_warnings": len(w)})

    # 5. mismatched sinh scale c
    mism = []
    for cval in (1e-8, 1e8):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", TargetNormDomainWarning)
            spc = new.spectrum(X, F, M=M, c=cval, far_field="power", tail_exponent=-ALPHA)
            fc = new.fit_exponent(spc["k"], spc["hk"], K_LO, K_HI,
                                  n_outside_grid=spc["n_outside_grid"])
        mism.append({"c": cval, "p": float(fc["p"]),
                     "err_vs_exact": float(abs(fc["p"] - P_TRUE)),
                     "n_outside_grid": int(spc["n_outside_grid"]),
                     "domain_valid": spc["domain_valid"]})
    rows.append({"mechanism": "mismatched sinh scale c",
                 "status": "STILL OPEN",
                 "magnitude": ("c = 1e-08 -> p = {:.6f}, c = 1e+08 -> p = {:.6f}, "
                               "against the exact 1.4".format(mism[0]["p"], mism[1]["p"])),
                 "cases": mism})

    # 6. NaN coefficients absorbed by the fitter, n_points overstated.
    # Leg 204's case verbatim: 150 of the 225 IN-BAND modes set to NaN (poisoning
    # out-of-band modes is a different, weaker probe -- the fitter never reads them).
    in_band = np.flatnonzero((k >= K_LO) & (k <= K_HI))
    hk_nan = hk.copy().astype(float)
    rng6 = np.random.default_rng(204)
    hk_nan[rng6.choice(in_band, size=150, replace=False)] = np.nan
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        f_nan = new.fit_exponent(k, hk_nan, K_LO, K_HI, n_outside_grid=0)
    n_finite = int(np.sum(np.isfinite(hk_nan[in_band])))
    p_nan = float(f_nan["p"])
    rows.append({"mechanism": "fitter absorbs NaN coefficients and overstates n_points",
                 "status": "STILL OPEN",
                 "magnitude": (
                     f"{150} of {in_band.size} in-band modes set to NaN: p = {p_nan:.6f} "
                     f"against the exact {P_TRUE} (error {abs(p_nan - P_TRUE):.6f}), while "
                     f"n_points is reported as {int(f_nan['n_points'])} and only "
                     f"{n_finite} were finite -- a "
                     f"{int(f_nan['n_points']) / max(n_finite, 1):.1f}x overstatement, "
                     f"{len(w)} warnings, domain_valid = {f_nan['domain_valid']}"),
                 "n_in_band_modes": int(in_band.size), "n_set_to_nan": 150,
                 "p": p_nan, "err_vs_exact": float(abs(p_nan - P_TRUE)),
                 "n_points_reported": int(f_nan["n_points"]),
                 "n_points_finite": n_finite,
                 "overstatement": float(int(f_nan["n_points"]) / max(n_finite, 1)),
                 "n_warnings": len(w)})

    for r in rows:
        print(f"    [{r['status']}] {r['mechanism']}: {r['magnitude']}")
    return {"what": ("leg 204 found SEVEN silent mechanisms.  This leg's declared territory "
                     "is 'the domain-guard windowing logic only', so it repairs ONE.  The "
                     "other six are re-measured here against the REPAIRED module so that "
                     "'not closed' is a number and not a promise"),
            "n_mechanisms_leg204_found": 7,
            "n_repaired_by_this_leg": 1,
            "n_still_open": len(rows),
            "mechanisms": rows}


# --------------------------------------------------------------------------
def _default(o):
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(repr(o))


def main():
    old, src = load_prerepair()
    print(f"Route-TNR, leg 220: repair of solver/target_norm.py's domain-guard WINDOW")
    print(f"pre-repair module loaded from git {PRE_REPAIR_REF} "
          f"({len(src.splitlines())} lines)\n")

    print("A -- ZERO REGRESSION on symmetric grids (A/B, raw float64):")
    ctrl = control_two_modules_really_differ(old, src)
    A = part_a(old)
    A["control_two_modules_really_differ"] = ctrl
    print(f"  => {A['n_leaves_compared']} leaves compared, "
          f"{A['n_cases_with_any_value_difference']} of {A['n_cases']} cases moved\n")

    print("B -- THE HEADLINE: leg 204's asymmetry ladder")
    B = part_b(old)
    print(f"  => {B['n_rungs_silent_prerepair']}/{B['n_rungs']} rungs silent pre-repair; "
          f"{B['n_rungs_flagged_repaired']}/{B['n_rungs']} flagged after; "
          f"{B['n_rungs_count_matches_truth']}/{B['n_rungs']} counts match truth\n")

    print("C -- LEG 55'S BANKED MARGINS (two bordered Newton solves, this takes a while):")
    C = part_c()
    print(f"  => {C['n_margins_bit_identical']}/{C['n_margins']} margins bit-identical\n")

    print("D -- STILL OPEN: leg 204's other six mechanisms, post-repair")
    D = part_d()
    print()

    gate_yes = bool(
        ctrl["control_passes"]
        and A["all_bit_identical"]
        and B["n_rungs_flagged_repaired"] == B["n_rungs"]
        and B["n_rungs_count_matches_truth"] == B["n_rungs"]
        and C["n_margins_bit_identical"] == C["n_margins"]
        and C["p_bit_identical_to_banked"])

    payload = {
        "leg": 220, "route": "TNR", "role": "LEG",
        "what": ("the repair of solver/target_norm.py's domain-guard WINDOW: the guard "
                 "tested |Xt| <= max|X| and now tests X.min() <= Xt <= X.max()"),
        "repairs_finding_of": "leg 204 (Route-TNA2), finding 1",
        "pre_repair_ref": PRE_REPAIR_REF,
        "gate": ("Does repairing the domain guard to window on the true data interval (per "
                 "leg 204's own identified mechanism) cause the asymmetric-grid "
                 "extrapolation case to now be correctly flagged (n_outside_grid>0/"
                 "domain_valid=False), while leg 55's own banked margins and every other "
                 "live call stay bit-identical?"),
        "gate_answer": "YES" if gate_yes else "NO",
        "A_zero_regression": A,
        "B_asymmetry_ladder": B,
        "C_leg55_banked_margins": C,
        "D_still_open": D,
        "ceiling": ("this repairs an input guard.  It moves no bound, certifies nothing, "
                    "re-measures no physics and touches no link of the L1->L4 chain.  It "
                    "extends no domain -- it NARROWS the accepted window to a subset, so a "
                    "call can only move from silently-accepted to flagged, never the "
                    "reverse"),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=2, default=_default)
    print(f"GATE: {payload['gate_answer']}")
    print(f"wrote {OUT}")
    return 0 if gate_yes else 1


if __name__ == "__main__":
    sys.exit(main())
