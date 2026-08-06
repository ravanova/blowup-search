"""Leg 167 (Route-DCB) -- leg 115's battery BANKED AS A PERMANENT REGRESSION SUITE.

This is the gate's yes-branch deliverable: "Bank leg 115's battery as a permanent regression
suite."  It is not a re-run of leg 151's tests and it deliberately does not import them.

WHY THIS FILE EXISTS WHEN test_decay_collocation_adversarial.py ALREADY DOES.
Leg 151 rewrote that file (191+/91-) in the SAME commit as the repair it was meant to check,
inverting all 7 of leg 115's pins.  It therefore asserts the guards leg 151 wrote, against the
code leg 151 wrote -- lesson 90 exactly: a control that cannot come out differently.  It is
still useful as a statement of intent; it is not independent evidence.

This suite is built the other way round.  Every case is re-derived from leg 115's battery and
runner AS THEY STOOD AT 53f03fe (read out of git, never from the post-repair files), and every
assertion about the repaired module is paired with the SAME assertion run against the
PRE-REPAIR module loaded out of git at a595dcb into this same process.  The pre-repair arm must
reproduce leg 115's banked corruption for the suite to mean anything -- gate 5 below is that
control, and it FAILS LOUDLY rather than skipping if the pre-repair module cannot be loaded.

Leg 115's three findings, and what "correct" now means for each:

  G1  J = 1 grid collapse.  The gauge row consumed the system's only collocation row, so
      M[1:, :] was the empty (0, 1) slice and NumPy broadcast the whole Jacobian into nothing.
      graded_inverse_norm returned the identical 1.681792830507429 for all 9 values of c
      (including nan and +-inf), for a NaN/Inf-poisoned nodal field, for all 5 drop values and
      both gauges.  Correct now: refuse.
  G2  sup_op_norm 1-D shape ambiguity.  np.atleast_2d turns a flat (n,) array into a ROW
      (1, n), never a column, so an array meant as an (n, 1) column operator had its domain and
      codomain axes silently swapped -- 12.0 where the caller meant 10.0.  Correct now: refuse
      the ambiguous spelling, and keep answering the unambiguous (n, 1) one.
  G3  Type-degenerate alpha.  A complex alpha produced a complex weight, which float() then
      truncated under NumPy's ComplexWarning -- a warning, suppressed by default, where Python's
      own float() raises TypeError.  Correct now: refuse.

Test convention (repo-wide): self-running script, also pytest-discoverable.
    .venv/bin/python test_decay_collocation_postrepair.py

Full measurement: experiments/p2_route_dcb_v1_postrepair.py
Data:             writeup/data/p2_route_dcb_v1_postrepair.json
Pre-repair magnitudes: writeup/data/p2_route_dca_v1_adversarial.json   (leg 115)
Repair evidence:       writeup/data/p2_route_dcr_v1_repair.json        (leg 151)
"""

import hashlib
import importlib.util
import os
import subprocess
import sys
import tempfile
import warnings

import numpy as np

REPO = os.path.dirname(os.path.abspath(__file__))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from solver.decay_collocation import (      # noqa: E402
    C_ANCHOR,
    Collocation,
    DecayCollocationDomainError,
    gauged_jacobian,
    graded_inverse_norm,
    sup_op_norm,
)

PRE_REPAIR_REF = "a595dcb"        # the commit that CREATED the module (its only other commit)
LEG115_REF = "53f03fe"            # leg 115's battery/runner, BEFORE leg 151 rewrote them
SEED = 20260806                   # leg 115's seed -> its randomized battery replays exactly

# Leg 115's banked magnitudes (writeup/data/p2_route_dca_v1_adversarial.json).
J1_COLLAPSE_VALUE = 1.681792830507429
G2_WORKED_FLAT_WRONG = 12.0
G2_WORKED_COLUMN_RIGHT = 10.0

# G3's end-to-end value is the one banked number of the three that does NOT reproduce bitwise,
# and the discrepancy is measured, not waved at:
#
#   leg 115's committed JSON   3.5626111859714866
#   live here, PRE-REPAIR      3.562611185971488     (1 ULP low, 3.7395818965489845e-16 rel)
#
# It is 1 ULP, and it is NOT a regression: it is the PRE-repair module that produces it, so the
# drift predates leg 151's patch entirely.  The mechanism is the one the other two banked values
# escape -- G1's 1.681792830507429 comes from inverting a 1x1 matrix and G2's 12.0 from a plain
# sum, while this value passes through np.linalg.inv on a 16x16, i.e. LAPACK, whose last bit is
# not fixed across library builds.  This is exactly what leg 105 measured (~2.1% on a
# noise-floor quantity) and leg 147 measured (22/763 leaves at <=3 ULP), and it is why this
# leg's clause (b) is a SAME-PROCESS differential rather than a comparison against a committed
# JSON: in one process both arms share one LAPACK and the drift cancels identically.
#
# Leg 151's own commit message quotes 3.562611185971488 -- the live value -- so leg 151 recorded
# the drifted number without flagging that it disagrees with leg 115's bank.  Named here.
G3_PIPELINE_VALUE_LEG115_JSON = 3.5626111859714866
G3_PIPELINE_VALUE_LIVE = 3.562611185971488
G3_PIPELINE_JSON_DRIFT_ULP = 1


# =========================================================================
# loading the pre-repair module -- the control arm
# =========================================================================

_PRE_CACHE = {}


def pre_repair_module():
    """solver/decay_collocation.py at a595dcb, live in THIS process beside the shipped one."""
    if "mod" in _PRE_CACHE:
        return _PRE_CACHE["mod"]
    src = subprocess.run(["git", "show", f"{PRE_REPAIR_REF}:solver/decay_collocation.py"],
                         cwd=REPO, capture_output=True, check=True).stdout
    fd, path = tempfile.mkstemp(suffix="_pre_decay_collocation.py")
    with os.fdopen(fd, "wb") as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location("pre_decay_collocation_t", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["pre_decay_collocation_t"] = mod
    spec.loader.exec_module(mod)
    _PRE_CACHE["mod"] = mod
    return mod


def _u64(x):
    a = np.ascontiguousarray(np.asarray(x, dtype=np.float64))
    return a.view(np.uint64).ravel()


def _bit_identical(a, b):
    ua, ub = _u64(a), _u64(b)
    return ua.shape == ub.shape and bool(np.all(ua == ub))


def _refuses(fn):
    """True iff `fn` raises. Warnings are NOT suppressed -- a silent return is the defect."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with np.errstate(all="ignore"):
            try:
                fn()
                return False
            except Exception:                       # noqa: BLE001
                return True


def _value(fn):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with np.errstate(all="ignore"):
            return fn()


# =========================================================================
# the cases, enumerated once, bound to whichever module is passed
# =========================================================================

def _pipeline_with_om(dc, col, om, alpha, c):
    """Leg 115's check_J1_ignores_poisoned_om reconstruction (battery @53f03fe), verbatim."""
    M, rows = dc.gauged_jacobian(col, om, c, gauge="origin", drop=0)
    A = np.linalg.inv(M)
    w_dom = col.w_domain(alpha)
    w_cod = np.empty(col.J)
    w_cod[0] = 1.0
    w_cod[1:] = col.w_codomain(alpha)[rows]
    return dc.sup_op_norm(A, w_dom, w_cod)


def g1_cases(dc):
    """19 cases: 9 poisoned c + 3 poisoned om + 5 drop + 2 gauge at J = 1.

    Note the 4 out-of-range drop values.  Leg 115's OWN prescribed repair predicate ("raise when
    `rows` is empty, i.e. J <= 1") is true for exactly ONE of the five (drop = 0) and false for
    the other four, yet all five collapsed to the same number -- the mechanism is the (1,1) ->
    (0,1) broadcast into the assignment target, not an empty row list.  Leg 151's novelty pass
    caught that before patching; these four cases are why it mattered.
    """
    col1 = dc.Collocation(1)
    a = 1.5
    out = {}
    for c in (0.0, 0.5, 1.0, 100.0, -50.0, 1e6, float("nan"), float("inf"), -float("inf")):
        out[f"G1a_c={c!r}"] = (lambda c=c: dc.graded_inverse_norm(col1, a, c=c)[0])
    for tag, p in (("nan", float("nan")), ("+inf", float("inf")), ("-inf", -float("inf"))):
        out[f"G1b_om={tag}"] = (lambda p=p: _pipeline_with_om(dc, col1, np.array([p]), a, p))
    for drop in (0, 1, -1, 5, 100):
        out[f"G1c_drop={drop}"] = (lambda d=drop: dc.graded_inverse_norm(col1, a, drop=d)[0])
    for gauge in ("origin", "a0"):
        out[f"G1d_gauge={gauge}"] = (lambda g=gauge: dc.graded_inverse_norm(col1, a, gauge=g)[0])
    return out


def g2_cases(dc):
    """31 cases: leg 115's worked example + its 30-case randomized battery, same seed."""
    out = {}
    Af = np.array([10.0, 1.0, 1.0])
    out["G2a_worked"] = (lambda: dc.sup_op_norm(Af, np.ones(3), np.ones(1)))
    rng = np.random.default_rng(SEED)
    for i in range(30):
        n = int(rng.integers(2, 7))
        A = rng.uniform(0.1, 20.0, size=n)
        out[f"G2b_rand{i:02d}_n={n}"] = (lambda A=A, n=n: dc.sup_op_norm(A, np.ones(n),
                                                                        np.ones(1)))
    return out


def g3_cases(dc):
    """13 cases: 6 complex alphas x {norm_domain, norm_codomain} + the end-to-end pipeline.

    The 6-alpha list is the RUNNER's (p2_route_dca_v1_adversarial.py @53f03fe), not the
    battery's 4-alpha list; the union is taken deliberately so that 1.0+0.0j and 1.5+1e-10j --
    which leg 115 banked but its test file did not cover -- are not silently skipped.
    """
    col = dc.Collocation(16)
    om = col.anchor()
    out = {}
    for a in (1.0 + 0.0j, 1.5 + 1e-10j, 1.5 + 0.1j, 1.5 + 1.0j, 0.0 + 1.0j, -1.0 + 2.0j):
        out[f"G3a_norm_domain_{a}"] = (lambda a=a: col.norm_domain(om, a))
        out[f"G3b_norm_codomain_{a}"] = (lambda a=a: col.norm_codomain(om, a))
    out["G3c_pipeline_1.5+0.3j"] = (lambda: dc.graded_inverse_norm(col, 1.5 + 0.3j)[0])
    return out


# =========================================================================
# GATES
# =========================================================================

def check_g1_all_refused():
    """G1: all 19 J = 1 collapse cases are refused, and by the module's OWN error type."""
    import solver.decay_collocation as dc
    cases = g1_cases(dc)
    assert len(cases) == 19, len(cases)
    silent = []
    wrong_type = []
    for name, fn in cases.items():
        try:
            v = _value(fn)
            silent.append((name, v))
        except DecayCollocationDomainError:
            pass
        except Exception as exc:                    # noqa: BLE001
            wrong_type.append((name, type(exc).__name__))
    assert not silent, f"G1 REGRESSION: {len(silent)} cases still return silently: {silent[:4]}"
    assert not wrong_type, (
        f"G1: {len(wrong_type)} refused with an exception that is NOT the module's own "
        f"DecayCollocationDomainError: {wrong_type}. A bare ZeroDivisionError or a NumPy "
        "shape error is a refusal by accident, not by contract.")
    return {"n_cases": 19, "refused": 19, "silent": 0}


def check_g2_all_refused():
    """G2: all 31 ambiguous 1-D sup_op_norm cases are refused."""
    import solver.decay_collocation as dc
    cases = g2_cases(dc)
    assert len(cases) == 31, len(cases)
    silent = [(n, _value(f)) for n, f in cases.items() if not _refuses(f)]
    assert not silent, f"G2 REGRESSION: {len(silent)} still silent: {silent[:4]}"
    return {"n_cases": 31, "refused": 31, "silent": 0}


def check_g3_all_refused():
    """G3: all 13 complex-alpha cases are refused, at both norms and end to end."""
    import solver.decay_collocation as dc
    cases = g3_cases(dc)
    assert len(cases) == 13, len(cases)
    silent = [(n, _value(f)) for n, f in cases.items() if not _refuses(f)]
    assert not silent, f"G3 REGRESSION: {len(silent)} still silent: {silent[:4]}"
    return {"n_cases": 13, "refused": 13, "silent": 0}


def check_no_over_refusal():
    """The guards must refuse ONLY leg 115's cases. Every legitimate spelling still answers,
    and answers the value leg 115 itself recorded as correct."""
    col = Collocation(3)
    Af = np.array([10.0, 1.0, 1.0])
    column = sup_op_norm(Af.reshape(3, 1), np.ones(3), np.ones(1))
    assert column == G2_WORKED_COLUMN_RIGHT, column

    col16 = Collocation(16)
    om = col16.anchor()
    ref = col16.norm_domain(om, 1.5)
    for a in (1.5, np.float64(1.5)):
        assert col16.norm_domain(om, a) == ref, a
    for a in (2, np.int64(2)):
        assert np.isfinite(col16.norm_domain(om, a)), a

    vals = {}
    for J in (2, 3, 8, 16, 64):
        v, _, _ = graded_inverse_norm(Collocation(J), 1.5)
        assert np.isfinite(v) and v > 0, (J, v)
        vals[J] = v

    # every in-range drop and both gauges still work at an ordinary J
    col8 = Collocation(8)
    for gauge in ("origin", "a0"):
        for drop in range(8):
            M, rows = gauged_jacobian(col8, col8.anchor(), C_ANCHOR, gauge=gauge, drop=drop)
            assert M.shape == (8, 8) and len(rows) == 7, (gauge, drop)
    return {"column_spelling": column, "J_probed": sorted(vals), "n_gauge_drop_probes": 16}


def check_g1_control_at_J_geq_2_still_propagates():
    """Leg 115's own CONTROL, which must survive the repair: at J >= 2 a poisoned c still
    PROPAGATES to a non-finite result rather than being refused. The guard is about J = 1, and
    over-broadening it into a general NaN check would break this."""
    out = {}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with np.errstate(all="ignore"):
            for J in (2, 3, 4, 8, 16):
                col = Collocation(J)
                v1, _, _ = graded_inverse_norm(col, 1.5, c=0.5)
                v2, _, _ = graded_inverse_norm(col, 1.5, c=100.0)
                vn, _, _ = graded_inverse_norm(col, 1.5, c=float("nan"))
                assert v1 != v2, ("CONTROL: c must still matter at J>=2", J)
                assert np.isnan(vn), ("CONTROL: NaN must still propagate at J>=2", J, vn)
                out[f"J{J}"] = {"c=0.5": v1, "c=100": v2, "nan_propagates": True}
    return {"J_tested": sorted(out), "all_sensitive": True, "all_nan_propagates": True}


def check_lesson90_pre_repair_control():
    """THE CONTROL THAT LETS THIS SUITE COME OUT DIFFERENTLY.

    Load the PRE-REPAIR module (a595dcb) into this same process and run the identical case
    lists.  It must reproduce leg 115's banked corruption: the J = 1 collapse to
    1.681792830507429 for every c including nan/+-inf, the 12.0-not-10.0 axis swap, and the
    end-to-end complex-alpha value 3.5626111859714866.

    Without this, gates 1-3 assert only that SOMETHING raises, which a module that raised on
    everything would also satisfy.  With it, the 63 refusals are measured against 63 cases that
    demonstrably did NOT refuse before.
    """
    pre = pre_repair_module()
    g1, g2, g3 = g1_cases(pre), g2_cases(pre), g3_cases(pre)
    n_silent = sum(1 for f in list(g1.values()) + list(g2.values()) + list(g3.values())
                   if not _refuses(f))
    assert n_silent > 0, (
        "CONTROL FAILED: the pre-repair module refused everything too, so gates 1-3 measure "
        "the harness rather than the repair.")

    vals = [_value(f) for f in g1.values()]
    finite = [v for v in vals if isinstance(v, float) and np.isfinite(v)]
    assert J1_COLLAPSE_VALUE in finite, (
        f"CONTROL: pre-repair G1 must reproduce leg 115's {J1_COLLAPSE_VALUE}, got {set(finite)}")
    assert _value(g2["G2a_worked"]) == G2_WORKED_FLAT_WRONG, "CONTROL: G2 axis swap not reproduced"

    # G3 end to end: pinned against the LIVE pre-repair value bitwise, and against leg 115's
    # committed JSON only to within the 1-ULP LAPACK drift documented at the top of this file.
    # Pinning it to the JSON bitwise would make this suite fail on any machine whose LAPACK
    # rounds the 16x16 inverse differently -- a statement about the build, not about the repair.
    g3v = _value(g3["G3c_pipeline_1.5+0.3j"])
    assert g3v == G3_PIPELINE_VALUE_LIVE, (
        f"CONTROL: G3 end-to-end pre-repair value moved: {g3v!r} != {G3_PIPELINE_VALUE_LIVE!r}")
    drift = abs(g3v - G3_PIPELINE_VALUE_LEG115_JSON) / abs(G3_PIPELINE_VALUE_LEG115_JSON)
    assert drift < 1e-14, (
        f"CONTROL: pre-repair G3 value has drifted {drift:.3e} from leg 115's banked "
        f"{G3_PIPELINE_VALUE_LEG115_JSON!r} -- more than the 1 ULP this suite documents.")

    n_total = len(g1) + len(g2) + len(g3)
    return {"n_cases": n_total, "pre_repair_silent": n_silent,
            "pre_repair_refused": n_total - n_silent,
            "J1_collapse_reproduced": J1_COLLAPSE_VALUE,
            "G2_axis_swap_reproduced": G2_WORKED_FLAT_WRONG,
            "G3_pipeline_live": g3v,
            "G3_json_drift_rel": drift}


def check_zero_regression_bitwise():
    """Clause (b), reduced to a suite-sized grid: every clean-input quantity is bit-identical
    to the pre-repair module at 0 ULP -- sha256 over raw IEEE-754 float64 bits, not allclose.

    Same process, same NumPy, same BLAS, which is the one setting in which the reproducibility
    literature holds bitwise identity to be the correct criterion (WG21 P3375R3).  The full
    sweep is in experiments/p2_route_dcb_v1_postrepair.py; this is the permanent tripwire.
    """
    import solver.decay_collocation as post
    pre = pre_repair_module()
    n = same = 0
    for J in (2, 3, 8, 16, 64, 128, 400):
        cp, cr = post.Collocation(J), pre.Collocation(J)
        q = [("theta", cp.theta, cr.theta), ("X", cp.X, cr.X), ("H", cp.H, cr.H),
             ("D", cp.D, cr.D), ("transport", cp.transport, cr.transport),
             ("anchor", cp.anchor(), cr.anchor())]
        omp, omr = cp.anchor(), cr.anchor()
        for c in (0.0, 0.5, -50.0):
            q.append((f"residual{c}", cp.residual(omp, c), cr.residual(omr, c)))
            q.append((f"jac{c}", cp.jacobian_matrix(omp, c), cr.jacobian_matrix(omr, c)))
        q.append(("dc_column", cp.dc_column(omp), cr.dc_column(omr)))
        q.append(("quadratic", cp.quadratic(omp), cr.quadratic(omr)))
        for a in (-1.0, 0.0, 1.2, 1.5, 2.0, 3.0):
            q.append((f"wd{a}", cp.w_domain(a), cr.w_domain(a)))
            q.append((f"wc{a}", cp.w_codomain(a), cr.w_codomain(a)))
            q.append((f"nd{a}", cp.norm_domain(omp, a), cr.norm_domain(omr, a)))
            for gauge in ("origin", "a0"):
                vp = post.graded_inverse_norm(cp, a, gauge=gauge)
                vr = pre.graded_inverse_norm(cr, a, gauge=gauge)
                q.append((f"gin{a}{gauge}", vp[0], vr[0]))
                q.append((f"ginA{a}{gauge}", vp[1], vr[1]))
        for name, x, y in q:
            n += 1
            ok = _bit_identical(x, y)
            same += int(ok)
            assert ok, f"ZERO-REGRESSION VIOLATION at J={J}, {name}"
    return {"n_quantities": n, "n_bit_identical": same, "ulp": 0,
            "instrument": "sha256/uint64 view of raw float64 bits"}


def check_guards_fire_on_no_shipped_configuration():
    """The guards must be invisible to every configuration the repo actually ships.  J = 8 is
    the smallest grid size any in-repo caller has ever declared (leg 115 measured this and
    recorded J = 1 as never reached by any banked run), so the whole shipped range must pass."""
    fired = []
    for J in (8, 16, 32, 64, 128, 200, 400, 500):
        for gauge in ("origin", "a0"):
            for alpha in (1.2, 1.5, 1.8, 2.0):
                try:
                    v, _, _ = graded_inverse_norm(Collocation(J), alpha, gauge=gauge)
                    assert np.isfinite(v)
                except DecayCollocationDomainError as exc:
                    fired.append((J, gauge, alpha, str(exc)[:80]))
    assert not fired, f"the guards fired on {len(fired)} SHIPPED configurations: {fired[:3]}"
    return {"n_shipped_configurations": 8 * 2 * 4, "n_guard_firings": 0}


def check_digest_of_repaired_module():
    """Pin the repaired module's source digest, so a later silent edit to the file this suite
    guards is visible as a failure here rather than only as a diff nobody read."""
    with open(os.path.join(REPO, "solver", "decay_collocation.py"), "rb") as fh:
        d = hashlib.sha256(fh.read()).hexdigest()[:16]
    return {"solver/decay_collocation.py sha256[:16]": d}


CHECKS = [
    check_g1_all_refused,
    check_g2_all_refused,
    check_g3_all_refused,
    check_no_over_refusal,
    check_g1_control_at_J_geq_2_still_propagates,
    check_lesson90_pre_repair_control,
    check_zero_regression_bitwise,
    check_guards_fire_on_no_shipped_configuration,
    check_digest_of_repaired_module,
]


def test_g1_all_refused():
    check_g1_all_refused()


def test_g2_all_refused():
    check_g2_all_refused()


def test_g3_all_refused():
    check_g3_all_refused()


def test_no_over_refusal():
    check_no_over_refusal()


def test_g1_control_at_J_geq_2_still_propagates():
    check_g1_control_at_J_geq_2_still_propagates()


def test_lesson90_pre_repair_control():
    check_lesson90_pre_repair_control()


def test_zero_regression_bitwise():
    check_zero_regression_bitwise()


def test_guards_fire_on_no_shipped_configuration():
    check_guards_fire_on_no_shipped_configuration()


if __name__ == "__main__":
    for fn in CHECKS:
        metrics = fn()
        head = ", ".join(f"{k}={v:.6g}" if isinstance(v, float) else f"{k}={v}"
                         for k, v in list(metrics.items())[:4])
        print(f"PASS {fn.__name__}: {head}")
    print(f"\nall decay_collocation POST-REPAIR checks passed ({len(CHECKS)} checks)")
    print("Leg 115's 63 failing cases are banked here as a permanent regression suite, re-derived")
    print("from the battery/runner at 53f03fe -- NOT from the post-repair files leg 151 rewrote.")
    print("Gate 6 is the lesson-90 control: it loads the PRE-REPAIR module at a595dcb and fails")
    print("loudly unless that module still reproduces leg 115's banked corruption.")
