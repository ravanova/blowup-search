"""Leg 135 (Route-FIB) -- leg 107's battery, BANKED as a permanent regression suite.

Run:  .venv/bin/python test_first_integral_postrepair.py       (~60 s)

WHAT THIS FILE IS FOR, AND WHY IT IS NOT test_first_integral_adversarial.py
---------------------------------------------------------------------------
`test_first_integral_adversarial.py` was rewritten inside the bench repair's own commit
(`9c08287`, 395 of 467 lines), converting leg 107's characterization gates into soundness
gates.  It is a legitimate pin and it is not duplicated here.  What it cannot be is
INDEPENDENT of the repair.  This file is: every assertion below is driven from leg 107's
own runner, read out of git at `5e03e13` -- i.e. the version BEFORE the repair commit
edited it -- and executed against the CURRENT module through its DEFAULT policy path.

The distinction is load-bearing.  The repair threaded `on_outside="extrapolate"` /
`on_nonfinite="drop"` through leg 107's file so its escalated numbers keep reproducing.
Sensible, but the consequence is that the runner NOW on `main` asks the repaired module
for the pre-repair arithmetic: it reports leg 107's original 96/96 and 397/400 whether or
not the repair is present, so running it proves nothing about the fix (lesson 90 -- a
control that cannot come out differently).  Reading the runner out of git restores its
power to distinguish.

`test_2` is the negative control that keeps this file honest: the SAME harness, bound to
the pre-repair module, must still report 96 fabricated values.  If it ever stops doing
so, this suite has gone vacuous and every other test here is meaningless.

READ-ONLY.  `solver/first_integral.py` is not edited by leg 135 under either branch.
Full measurement: `experiments/p2_route_fib_v1_postrepair.py` /
`writeup/data/p2_route_fib_v1_postrepair.json`.
"""

import os
import sys
import warnings

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from experiments.p2_route_fib_v1_postrepair import (   # noqa: E402
    LEG107, PRE, bitdiff, git_show, load_module_from_source, nan_ladder_ab,
    run_original_battery)

import solver.first_integral as FI                     # noqa: E402

PASS, FAIL = [], []


def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}   {detail}")


def _pre_module():
    return load_module_from_source(git_show(f"{PRE}:solver/first_integral.py"),
                                   "first_integral_prerepair_test")


# ---------------------------------------------------------------------------
def test_1_original_battery_rejects_every_fabricated_value():
    print("\n[1] leg 107's ORIGINAL G1 (git 5e03e13), DEFAULT policy, current module")
    res = run_original_battery(FI, "test_post")
    g1 = res["gates"]["G1_turning_point_continuation"]
    vals = [x for r in g1["rows"] for x in r["omega_outside"].values()]
    exact_pos_zero = sum(1 for x in vals
                         if isinstance(x, float) and x == 0.0 and not np.signbit(x))
    print(f"      {g1['evaluations']} evaluations outside the support over "
          f"a=0.25/0.3/0.5/0.8 x K=48/64/96")
    check("0 fabricated finite nonzero values where the module's own docstring says "
          "Omega == 0", g1["finite_nonzero_returns"] == 0,
          f"{g1['finite_nonzero_returns']}/{g1['evaluations']}")
    check("every out-of-support value is EXACTLY +0.0 (not -0.0, not tiny)",
          exact_pos_zero == g1["evaluations"],
          f"{exact_pos_zero}/{g1['evaluations']}")
    check("the guard announces itself rather than answering silently",
          res["warnings_by_category"].get("FirstIntegralSupportWarning", 0) > 0,
          f"{res['warnings_by_category']}")
    return res


# ---------------------------------------------------------------------------
def test_2_negative_control_pre_repair_module_still_fabricates():
    print("\n[2] NEGATIVE CONTROL -- the same harness on the pre-repair module")
    res = run_original_battery(_pre_module(), "test_pre")
    g1 = res["gates"]["G1_turning_point_continuation"]
    worst = max(abs(x) for r in g1["rows"] for x in r["omega_outside"].values()
                if isinstance(x, float))
    check("reproduces leg 107's escalated count exactly -- so this suite CAN fail",
          g1["finite_nonzero_returns"] == 96,
          f"{g1['finite_nonzero_returns']}/{g1['evaluations']} fabricated")
    check("and its largest fabricated value, against a gauge amplitude of 1",
          299.0 < worst < 302.0, f"|Omega| = {worst:.6f}")
    return res


# ---------------------------------------------------------------------------
def test_3_nan_census_refuses_every_poisoned_rung():
    print("\n[3] leg 107's G4 ladder -- the NaN census, both modules")
    lad = nan_ladder_ab(_pre_module(), FI)
    for r in lad["rows"]:
        print(f"      {r['n_nan']:3d}/400 NaN -> pre {str(r['pre_defect']):<24}"
              f"post {r['post_defect']}")
    check("0 of 9 rungs absorbed post-repair (was 6 of 9)",
          lad["post_absorbed_rungs"] == 0 and lad["pre_absorbed_rungs"] == 6,
          f"pre {lad['pre_absorbed_rungs']}/9 absorbed, worst "
          f"{lad['pre_max_nan_absorbed']}/400 still certified; post "
          f"{lad['post_absorbed_rungs']}/9")
    # and the finite-poison control leg 107 used must still be CAUGHT, unchanged
    a, c, N = 0.3, 0.5, 400
    X = np.linspace(0.01, 3.0, N)
    E = c * np.exp(-X ** 2 / 4.0)
    Om = -(E / c) ** (1.0 / a)
    d = FI.first_integral_defect(np.where(np.arange(N) == 200, Om * 2.0, Om),
                                 (E - c) / a, a, c)
    check("a FINITE one-point poison is still caught (leg 107's own control)",
          abs(d - 1.0) < 1e-9, f"defect {d:.6f}")


# ---------------------------------------------------------------------------
def test_4_in_support_values_are_bit_identical():
    print("\n[4] in-support surfaces, same process, pre vs post, bit-for-bit")
    pre = _pre_module()
    SHAPE = np.linspace(0.0, 1.0, 401)
    nd = nv = nw = 0
    for a, K in ((0.35, 32), (0.6, 56)):
        with warnings.catch_warnings(record=True) as rec:
            warnings.simplefilter("always")
            rpo, rpn = pre.ReducedProfile(a, K=K), FI.ReducedProfile(a, K=K)
            ro, rn = rpo.solve(Xc0=10.0), rpn.solve(Xc0=10.0)
            assert ro["converged"] and rn["converged"]
            bo, bn, Xo, Xn = ro["b"], rn["b"], ro["Xc"], rn["Xc"]
            for x, y in ((bo, bn), ([Xo], [Xn]),
                         (rpo.omega_of(bo, SHAPE), rpn.omega_of(bn, SHAPE)),
                         (rpo.e_of(bo, SHAPE), rpn.e_of(bn, SHAPE)),
                         (rpo.jacobian(bo, Xo), rpn.jacobian(bn, Xn)),
                         ([rpo.mass(bo, Xo)], [rpn.mass(bn, Xn)]),
                         ([rpo.operator_norm(bo, Xo)], [rpn.operator_norm(bn, Xn)])):
                d = bitdiff(x, y)
                nd += d["n_bit_differences"]
                nv += d["n"]
        nw += len(rec)
    check("0 bit-differences and 0 spurious warnings on in-support input",
          nd == 0 and nw == 0, f"{nv} values, {nd} bit-differences, {nw} warnings")


# ---------------------------------------------------------------------------
def test_5_the_support_edge_v_equals_one_stays_inside():
    print("\n[5] v = 1 EXACTLY -- the support edge, and it is load-bearing")
    rp = FI.ReducedProfile(0.3, K=48)
    r = rp.solve(Xc0=10.0)
    one = np.array([1.0])
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        om = float(rp.omega_of(r["b"], one)[0])
        e = float(rp.e_of(r["b"], one)[0])
        T, _ = FI.even_cheb(48, one)
    finite = np.isfinite(om) and np.isfinite(e) and bool(np.all(np.isfinite(T)))
    print(f"      omega_of(1)={om!r}  e_of(1)={e:.3e}  T finite={bool(np.all(np.isfinite(T)))}"
          f"  warnings={len(rec)}")
    check("the edge is INSIDE: finite, unwarned, and Omega(1) is a signed zero not a NaN",
          finite and len(rec) == 0, f"{len(rec)} warnings")
    # this is exactly what solver/reduced_certificate.py hands even_cheb (max |v| = 1.0),
    # so a guard at |v| >= 1 instead of |v| > 1 + 4eps would NaN out a downstream module
    # the repair's own A/B never ran.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        e_out = float(rp.e_of(r["b"], np.array([1.0 + 1e-9]))[0])
        om_out = float(rp.omega_of(r["b"], np.array([1.0 + 1e-9]))[0])
    check("and the first value strictly outside is refused",
          (not np.isfinite(e_out)) and om_out == 0.0,
          f"e_of(1+1e-9)={e_out!r}, omega_of(1+1e-9)={om_out!r}")


# ---------------------------------------------------------------------------
def test_6_downstream_reduced_certificate_is_unmoved():
    print("\n[6] solver/reduced_certificate.py -- the consumer the bench A/B never ran")
    pre = _pre_module()
    rc_src = open(os.path.join(ROOT, "solver", "reduced_certificate.py")).read()

    def load_rc(fi_mod, name):
        saved = sys.modules.get("solver.first_integral")
        sys.modules["solver.first_integral"] = fi_mod
        try:
            return load_module_from_source(rc_src, name)
        finally:
            if saved is not None:
                sys.modules["solver.first_integral"] = saved
            else:
                sys.modules.pop("solver.first_integral", None)

    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        old = load_rc(pre, "rc_pre_test").rehearsal(0.3, K=32)
        new = load_rc(FI, "rc_post_test").rehearsal(0.3, K=32)
    nd = sum(bitdiff([old[f]], [new[f]])["n_bit_differences"]
             for f in ("Xc_over_c", "newton_residual", "Y0_interpolant_defect",
                       "Z0", "opnorm"))
    nd += bitdiff(old["N2_sup_by_cutoff"], new["N2_sup_by_cutoff"])["n_bit_differences"]
    print(f"      Y_0 {old['Y0_interpolant_defect']:.6e} -> "
          f"{new['Y0_interpolant_defect']:.6e},  ||A|| {old['opnorm']:.9f} -> "
          f"{new['opnorm']:.9f}")
    check("all 8 rehearsal fields bit-identical, 0 guard warnings raised downstream",
          nd == 0 and len(rec) == 0, f"{nd} bit-differences, {len(rec)} warnings")


# ---------------------------------------------------------------------------
def test_7_the_modules_own_long_gate_4():
    print("\n[7] test_first_integral.py gate 4 -- first_integral_defect WITH a mask")
    print("      (the repair's census runs BEFORE the mask, so this is the most "
          "exposed gate in the repo)")
    import test_first_integral as tfi
    tfi.PASS.clear()
    tfi.FAIL.clear()
    tfi.test_4_identity_on_independent_profiles()
    check("gate 4 passes on the repaired module, unchanged",
          len(tfi.FAIL) == 0 and len(tfi.PASS) == 1,
          f"{len(tfi.PASS)} pass, {len(tfi.FAIL)} fail")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 72)
    print("leg 135 (Route-FIB) -- leg 107's battery as a permanent regression suite")
    print("=" * 72)
    print(f"battery source: git {LEG107}:experiments/p2_route_fia_v1_adversarial.py")
    print(f"negative control module: git {PRE}:solver/first_integral.py")
    test_1_original_battery_rejects_every_fabricated_value()
    test_2_negative_control_pre_repair_module_still_fabricates()
    test_3_nan_census_refuses_every_poisoned_rung()
    test_4_in_support_values_are_bit_identical()
    test_5_the_support_edge_v_equals_one_stays_inside()
    test_6_downstream_reduced_certificate_is_unmoved()
    test_7_the_modules_own_long_gate_4()
    print("\n" + "=" * 72)
    print(f"{len(PASS)}/{len(PASS) + len(FAIL)} passed")
    if FAIL:
        for f in FAIL:
            print(f"  FAILED: {f}")
        sys.exit(1)
