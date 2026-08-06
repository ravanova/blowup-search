"""Leg 100 (Route-HNA) -- the adversarial battery against `solver/holder_norms.py`.

THE QUESTION (the leg's gate, verbatim):

    Under an adversarial battery (NaN/Inf-poisoned weight-class parameters, degenerate
    grading exponents), does solver/holder_norms.py's norm or embedding-constant
    computation ever silently return a finite, plausible-looking wrong value instead of
    propagating or flagging the invalid input?

WHAT THIS IS NOT.  It is not a Route-D bound-sharpening leg, and it builds no new
machinery.  It is a pure robustness stress test of EXISTING code, the exact precedent leg
69 (IA) set for `solver/interval.py`: "does not sharpen a bound, pure stress test of
infrastructure."  Nothing here re-derives a constant, re-scores the weighted-ell^1 no-go,
or touches the (dead) B stage.  `solver/holder_norms.py` is READ-ONLY under this leg and is
NOT patched under either gate outcome.

THE PRE-COMMITTED CORRUPTION CRITERION (fixed before the run).  A case counts as SILENT
CORRUPTION when, on an input carrying a NaN, an Inf, or a degenerate grading exponent, the
call

  (a) returns an output in which EVERY float is finite (no NaN, no Inf anywhere in the
      returned scalar/tuple/list), AND
  (b) raises nothing, AND
  (c) emits no warning,

while a propagating implementation would have returned NaN (or refused).  Returning NaN,
returning +-inf, raising, or warning ALL count as FLAGGED, not silent.  Magnitudes are
reported either way: for every case the battery records what the module returned and what
the same call returns on the corresponding CLEAN input, so the damage is a number.

THE MODULE HAS NO VALIDATION SURFACE.  Gate A0 counts the argument-validation sites
(`raise`, `isfinite`, `isnan`, `assert`) in the module by AST, so "the module never checks"
is a measurement and not an impression.

**THE GAP THIS BATTERY MEASURED HAS SINCE BEEN CLOSED.**  Leg 100 answered its gate YES
and, per its territory rule, did not patch the module; a later bench repair added the
finiteness/degeneracy guard, and `test_holder_norms_adversarial.py` was INVERTED to assert
the refusals.  This battery is leg 100's own artefact and its JSON is a banked measurement
of the PRE-REPAIR module, so it must keep reproducing that measurement rather than
silently re-pointing at repaired code and reporting a different answer.  It therefore
loads its subject **by git blob hash** (`PREREPAIR_BLOB` below), which is content-addressed
and so survives rebase, branch deletion and the repair's own merge; the blob stays
reachable through history forever.  Set `HNA_AUDIT_LIVE=1` to audit the working-tree
module instead -- useful for confirming the guard holds, but it will NOT reproduce the
banked JSON, because the gaps below are closed and the calls now raise.

REPRODUCIBILITY NOTE (measured by the bench repair, 2026-08-06).  Re-run against the
pinned blob this battery reproduces every banked magnitude bit-identically -- the clean
conformal error 1.517287054473293e-04, the clean operator norm 661.2075718521894, the
2.1053x understatement, the clean embedding constant `random_best` 0.8914207747116539 --
with exactly two exceptions, both in `A6.clean_per_degree`: 0.8359515019975166 reproduces
as ...164 and 0.8548322678393498 as ...497, a 1-2 ULP difference, deterministic across
repeated runs on one machine (3/3 identical) and attributable to BLAS matmul
reduction-order differing between runners, not to any code change.  The committed JSON is
left as leg 100 banked it; `runtime_seconds` was never reproducible in any case.

Run:  python experiments/p2_route_hna_v1_adversarial.py
Writes: writeup/data/p2_route_hna_v1_adversarial.json
"""
from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import time
import types
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

NAN, INF = float("nan"), float("inf")
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE = os.path.join(HERE, "solver", "holder_norms.py")

# The exact solver/holder_norms.py leg 100 audited, content-addressed.  Do not "update"
# this to a branch name: the point is that it cannot drift.
PREREPAIR_BLOB = "b614a1167ebd1b87fa0f63b0f94ebc63abb3b4d1"
AUDIT_LIVE = os.environ.get("HNA_AUDIT_LIVE", "") not in ("", "0")


def _load_subject():
    """Import the module under audit: the pre-repair blob by default, else the live one."""
    if AUDIT_LIVE:
        src = open(MODULE).read()
        return src, __import__("solver.holder_norms", fromlist=["*"])
    src = subprocess.run(["git", "cat-file", "blob", PREREPAIR_BLOB],
                         cwd=HERE, capture_output=True, text=True, check=True).stdout
    mod = types.ModuleType("holder_norms_prerepair")
    mod.__dict__["__file__"] = MODULE
    exec(compile(src, f"<blob {PREREPAIR_BLOB[:12]}:solver/holder_norms.py>", "exec"),
         mod.__dict__)
    return src, mod


_SRC, _SUBJECT = _load_subject()
HolderNorm = _SUBJECT.HolderNorm
conformal_check = _SUBJECT.conformal_check
decay_weight = _SUBJECT.decay_weight
family_op_norm = _SUBJECT.family_op_norm
holder_H_constant = _SUBJECT.holder_H_constant
jacobian_identity_error = _SUBJECT.jacobian_identity_error
square_wave_partial_sum = _SUBJECT.square_wave_partial_sum


# ---------------------------------------------------------------------------
# instrumentation
# ---------------------------------------------------------------------------


def call(fn, *args, **kw):
    """Run `fn`, returning (value, exception_name, warning_names).

    numpy's own floating-point warnings are made visible (errstate 'warn') so that an
    invalid operation inside the module counts as a SIGNAL if it ever escapes.
    """
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            with np.errstate(all="warn"):
                val = fn(*args, **kw)
            exc = None
        except Exception as e:            # noqa: BLE001 -- classifying, not handling
            val, exc = None, type(e).__name__
    return val, exc, sorted({type(w.message).__name__ for w in caught})


def _floats(v):
    """Flatten a return value into a list of python floats."""
    if v is None:
        return []
    if isinstance(v, (list, tuple)):
        out = []
        for x in v:
            out.extend(_floats(x))
        return out
    a = np.asarray(v, dtype=float).ravel()
    return [float(x) for x in a]


def classify(val, exc, warns):
    """SILENT iff all-finite output, no exception, no warning.  Else FLAGGED, and how."""
    if exc is not None:
        return "FLAGGED_RAISE"
    if warns:
        return "FLAGGED_WARN"
    fs = _floats(val)
    if any(np.isnan(x) for x in fs):
        return "FLAGGED_NAN"
    if any(np.isinf(x) for x in fs):
        return "FLAGGED_INF"
    return "SILENT"


def probe(label, clean_value, fn, *args, **kw):
    """One battery row: run the poisoned call, classify it, quantify the damage."""
    val, exc, warns = call(fn, *args, **kw)
    verdict = classify(val, exc, warns)
    got, ref = _floats(val), _floats(clean_value)
    row = {
        "case": label,
        "verdict": verdict,
        "returned": got,
        "clean": ref,
        "exception": exc,
        "warnings": warns,
    }
    if verdict == "SILENT" and len(got) == len(ref):
        dev = [abs(g - r) for g, r in zip(got, ref)]
        row["max_abs_deviation_from_clean"] = max(dev) if dev else 0.0
        row["bit_identical_to_clean"] = all(
            (g == r) or (np.isnan(g) and np.isnan(r)) for g, r in zip(got, ref))
        row["ratio_to_clean"] = [
            (float("nan") if r == 0 else g / r) for g, r in zip(got, ref)]
    return row


def grid(J, eps=1e-3):
    th = np.linspace(-np.pi + eps, np.pi - eps, J)
    return th, np.tan(0.5 * th)


# ---------------------------------------------------------------------------
# A0 -- how much validation surface does the module have at all?
# ---------------------------------------------------------------------------


def gate_A0():
    src = _SRC                       # the audited source, not whatever is on disk today
    tree = ast.parse(src)
    n_raise = sum(1 for n in ast.walk(tree) if isinstance(n, ast.Raise))
    n_assert = sum(1 for n in ast.walk(tree) if isinstance(n, ast.Assert))
    names = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    names |= {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    guards = sorted(names & {"isfinite", "isnan", "isinf", "warn", "warns", "ValueError"})
    publics = sorted(n.name for n in tree.body
                     if isinstance(n, (ast.FunctionDef, ast.ClassDef))
                     and not n.name.startswith("_"))
    return {
        "n_raise_sites": n_raise,
        "n_assert_sites": n_assert,
        "finiteness_guard_names_present": guards,
        "public_entry_points": publics,
        "n_public_entry_points": len(publics),
        "note": "the count of argument-validation sites in the whole module; a zero here "
                "is the structural reason every other gate below can find silence",
    }


# ---------------------------------------------------------------------------
# A1 -- the module's OWN self-validation routine, on a poisoned grid
# ---------------------------------------------------------------------------


def gate_A1():
    """`conformal_check` is what the module's docstring credits with catching a wrong
    exponent in the first draft.  Its mask `|mid| * dth <= resolved` is an ORDERED
    comparison, so a NaN node makes the mask False and the poisoned pairs are dropped."""
    J = 128
    th, _ = grid(J)
    clean = conformal_check(th, 0.3)
    clean_jac = jacobian_identity_error(th)
    rows = []
    for idx in (7, 64, 120):
        t = th.copy(); t[idx] = NAN
        rows.append(probe(f"conformal_check, theta[{idx}] = NaN", clean, conformal_check, t, 0.3))
        t = th.copy(); t[idx] = INF
        rows.append(probe(f"conformal_check, theta[{idx}] = +Inf", clean, conformal_check, t, 0.3))
    t = th.copy(); t[64] = NAN
    rows.append(probe("jacobian_identity_error, theta[64] = NaN", clean_jac,
                      jacobian_identity_error, t))
    t = th.copy(); t[64] = t[63]
    rows.append(probe("conformal_check, duplicated grid node (dtheta = 0)", clean,
                      conformal_check, t, 0.3))
    n_silent = sum(1 for r in rows if r["verdict"] == "SILENT")
    n_identical = sum(1 for r in rows if r.get("bit_identical_to_clean"))
    return {
        "clean_conformal_check": list(clean),
        "clean_jacobian_identity_error": list(clean_jac),
        "n_cases": len(rows),
        "n_silent": n_silent,
        "n_bit_identical_to_clean": n_identical,
        "cases": rows,
    }


# ---------------------------------------------------------------------------
# A2 -- the vacuous pass: a grid on which NOTHING is checked reports perfection
# ---------------------------------------------------------------------------


def gate_A2():
    """`jacobian_identity_error` initialises `worst = 0.0` and `continue`s past every
    offset whose resolved-pair mask is empty.  A grid that resolves nothing therefore
    returns 0.0 -- the value that means EXACT agreement with the conformal identity."""
    rows = []
    for J in (4, 6, 8, 12, 16, 24, 32, 128):
        th, _ = grid(J)
        err, xmax = conformal_check(th, 0.3)
        rows.append({"J": J, "conformal_err": err, "largest_resolved_absX": xmax,
                     "resolved_anything": xmax > 0.0})
    allnan, exc, warns = call(conformal_check, np.full(16, NAN), 0.3)
    allinf, _, _ = call(conformal_check, np.full(16, INF), 0.3)
    return {
        "coarse_grid_sweep": rows,
        "all_nan_grid_returns": _floats(allnan),
        "all_nan_grid_exception": exc,
        "all_nan_grid_warnings": warns,
        "all_nan_grid_verdict": classify(allnan, exc, warns),
        "all_inf_grid_returns": _floats(allinf),
        "note": "conformal_check on a 16-node grid whose every entry is NaN returns "
                "(0.0, 0.0): worst deviation from the exact conformal identity = 0.0, "
                "i.e. a PERFECT pass, on a grid with no valid node at all",
    }


# ---------------------------------------------------------------------------
# A3 -- family_op_norm on a poisoned operator
# ---------------------------------------------------------------------------


def _substrate(J=48, scale=0.05, seed=1):
    th, X = grid(J)
    A = np.random.default_rng(seed).standard_normal((J, J)) * scale
    dn = HolderNorm(th, X, 1.0, 0.3)
    cn = HolderNorm(th, X, 1.0, 0.3)
    return th, X, A, dn, cn


def gate_A3():
    """`family_op_norm`'s two guards -- `if ng <= 0: continue` and `if r > best` -- are
    ordered comparisons.  Every NaN candidate is skipped, so a poisoned operator falls
    through to the initialiser `best, arg = 0.0, -1`."""
    th, X, A, dn, cn = _substrate()
    clean = family_op_norm(A, dn, cn)
    rows = []
    for tag, poison in (("NaN", NAN), ("+Inf", INF), ("-Inf", -INF)):
        for i, j in ((3, 7), (0, 0), (47, 47)):
            Ap = A.copy(); Ap[i, j] = poison
            rows.append(probe(f"family_op_norm, A[{i},{j}] = {tag}", clean,
                              family_op_norm, Ap, dn, cn))
    # the norm objects are built INSIDE the probed call, so any construction-time
    # numpy warning is attributed to the case that provoked it
    rows.append(probe("family_op_norm, codomain alpha = NaN", clean,
                      lambda: family_op_norm(A, dn, HolderNorm(th, X, NAN, 0.3))))
    rows.append(probe("family_op_norm, domain gamma = NaN", clean,
                      lambda: family_op_norm(A, HolderNorm(th, X, 1.0, NAN), cn)))
    n_silent = sum(1 for r in rows if r["verdict"] == "SILENT")
    n_zero = sum(1 for r in rows if r["verdict"] == "SILENT" and r["returned"][0] == 0.0)
    return {
        "clean_family_op_norm": list(clean),
        "n_cases": len(rows),
        "n_silent": n_silent,
        "n_silent_returning_exactly_zero": n_zero,
        "collapse_factor": float(clean[0]) if n_zero else None,
        "note": "a poisoned operator is reported as a lower bound of exactly 0.0 with "
                "arg = -1, numerically indistinguishable from the zero operator, while "
                "the clean operator scores %.6f" % clean[0],
        "cases": rows,
    }


# ---------------------------------------------------------------------------
# A4 -- the dropped maximizer: a finite, plausible, UNDERSTATED lower bound
# ---------------------------------------------------------------------------


def gate_A4():
    """The sharpest case.  Poison ONE member of the caller-supplied `extra` family --
    the one that is the true maximizer -- and `family_op_norm` returns the runner-up: a
    finite, entirely plausible number, with `arg` pointing at a legitimate clean vector.
    Nothing in the return value records that a test function was discarded."""
    th, X, A, dn, cn = _substrate()
    g_a = np.exp(-X ** 2)
    g_b = np.exp(-0.25 * X ** 2) * np.cos(th)
    r_a = dn(A @ g_a) / cn(g_a)
    r_b = dn(A @ g_b) / cn(g_b)
    hi, lo = (g_a, g_b) if r_a > r_b else (g_b, g_a)
    r_hi, r_lo = max(r_a, r_b), min(r_a, r_b)
    both_clean = family_op_norm(A, dn, cn, extra=[lo, hi], include_sup_extremizers=False)
    rows = []
    for tag, poison in (("NaN", NAN), ("+Inf", INF)):
        bad = hi.copy(); bad[len(hi) // 2] = poison
        rows.append(probe(f"family_op_norm, true maximizer poisoned with {tag}",
                          both_clean, family_op_norm, A, dn, cn,
                          extra=[lo, bad], include_sup_extremizers=False))
    # and the same poison inside the FULL family (sup extremizers on): invisible
    bad = hi.copy(); bad[len(hi) // 2] = NAN
    full_clean = family_op_norm(A, dn, cn, extra=[lo, hi])
    rows.append(probe("family_op_norm, poisoned extra inside the full family",
                      full_clean, family_op_norm, A, dn, cn, extra=[lo, bad]))
    silent = [r for r in rows if r["verdict"] == "SILENT"]
    return {
        "ratio_true_maximizer": r_hi,
        "ratio_runner_up": r_lo,
        "clean_two_vector_family": list(both_clean),
        "clean_full_family": list(full_clean),
        "understatement_factor": r_hi / r_lo,
        "n_cases": len(rows),
        "n_silent": len(silent),
        "note": "poisoning the maximizer returns the runner-up, %.6f instead of %.6f, "
                "a factor %.4f understatement of the module's own lower bound, with no "
                "NaN, no warning and no exception" % (r_lo, r_hi, r_hi / r_lo),
        "cases": rows,
    }


# ---------------------------------------------------------------------------
# A5 -- the norms themselves under poisoned weight-class parameters
# ---------------------------------------------------------------------------


def gate_A5():
    """The norm objects are the part that mostly BEHAVES: NaN in alpha, gamma or the grid
    reaches `np.max`, which propagates.  Recorded as magnitudes, and with the one
    IEEE-754 special case that does survive locally: `(1 + 0^2)**(NaN/2) == 1.0`."""
    J = 64
    th, X = grid(J)
    h = 1.0 / (1.0 + X ** 2)
    clean = HolderNorm(th, X, 1.0, 0.3)
    clean_val = [clean.sup_part(h), clean.seminorm(h), clean(h)]

    def norm_triple(**kw):
        n = HolderNorm(th, X, kw.pop("alpha"), kw.pop("gamma"), **kw)
        hh = kw.get("_h", h)
        return [n.sup_part(hh), n.seminorm(hh), n(hh)]

    rows = []
    for label, kw in (
        ("alpha = NaN", dict(alpha=NAN, gamma=0.3)),
        ("alpha = +Inf", dict(alpha=INF, gamma=0.3)),
        ("gamma = NaN", dict(alpha=1.0, gamma=NAN)),
        ("gamma = -0.5 (degenerate: negative grading)", dict(alpha=1.0, gamma=-0.5)),
        ("gamma = 0 (degenerate: no Holder grading)", dict(alpha=1.0, gamma=0.0)),
        ("gamma = 1 (degenerate: Lipschitz endpoint)", dict(alpha=1.0, gamma=1.0)),
        ("semi_alpha = NaN", dict(alpha=1.0, gamma=0.3, semi_alpha=NAN)),
        ("semi_alpha = NaN with sup_only=True", dict(alpha=1.0, gamma=0.3,
                                                    semi_alpha=NAN, sup_only=True)),
        ("gamma = NaN with sup_only=True", dict(alpha=1.0, gamma=NAN, sup_only=True)),
    ):
        rows.append(probe(f"HolderNorm({label})", clean_val, norm_triple, **kw))

    # poisoned GRID rather than poisoned exponent
    def poisoned_grid_triple():
        tX = X.copy(); tX[30] = NAN
        n = HolderNorm(th, tX, 1.0, 0.3)
        return [n.sup_part(h), n.seminorm(h), n(h)]

    rows.append(probe("HolderNorm, X[30] = NaN (poisoned grid)", clean_val,
                      poisoned_grid_triple))

    # the zero vector under an infinite weight: 0 * inf
    rows.append(probe("HolderNorm(alpha=+Inf).sup_part(zeros) [true answer 0.0]", [0.0],
                      lambda: [HolderNorm(th, X, INF, 0.3).sup_part(np.zeros(J))]))

    w0 = decay_weight(np.array([0.0, 1.0, 10.0]), NAN)
    return {
        "clean_sup_seminorm_norm": clean_val,
        "n_cases": len(rows),
        "n_silent": sum(1 for r in rows if r["verdict"] == "SILENT"),
        "decay_weight_at_X0_with_NaN_alpha": float(w0[0]),
        "decay_weight_offaxis_with_NaN_alpha": _floats(w0[1:]),
        "note": "IEEE-754 pow(1.0, NaN) = 1.0, so the node X = 0 keeps an exactly-1.0 "
                "weight under a NaN grading exponent; the sup over the grid still "
                "propagates NaN, so this one is latent, not live",
        "cases": rows,
    }


# ---------------------------------------------------------------------------
# A6 -- the EMBEDDING CONSTANT: holder_H_constant
# ---------------------------------------------------------------------------


def gate_A6():
    """`holder_H_constant` is the embedding-constant surface (the Holder bound for the
    Hilbert transform).  Its random-family branch guards with `if den > 0` and accumulates
    with python's builtin `max(best, x)` -- and `max(0.0, NaN)` returns 0.0, because the
    comparison `NaN > 0.0` is False.  So the random arm reports a constant of exactly
    zero on poisoned input."""
    J = 128
    th, _ = grid(J)
    degs = (4, 16, 64)
    clean_pd, clean_rb = holder_H_constant(th, 0.3, degrees=degs, n_random=60)
    rows = []
    for label, tt, gg in (
        ("gamma = NaN", th, NAN),
        ("gamma = -0.3 (degenerate)", th, -0.3),
        ("theta[7] = NaN", (lambda t: (t.__setitem__(7, NAN), t)[1])(th.copy()), 0.3),
        ("theta[7] = +Inf", (lambda t: (t.__setitem__(7, INF), t)[1])(th.copy()), 0.3),
    ):
        val, exc, warns = call(holder_H_constant, tt, gg, degrees=degs, n_random=60)
        per_deg, rb = (val if val is not None else ([], None))
        rows.append({
            "case": f"holder_H_constant, {label}",
            "per_degree": _floats(per_deg),
            "random_best": rb,
            "per_degree_propagates_nan": all(np.isnan(x) for x in _floats(per_deg)),
            "random_best_is_exactly_zero": rb == 0.0,
            "exception": exc,
            "warnings": warns,
            "verdict_whole_return": classify(val, exc, warns),
            "verdict_random_arm_alone": classify(rb, exc, warns),
        })
    degen = {}
    for g in (0.0, 1.0, 0.3):
        pd, rb = holder_H_constant(th, g, degrees=degs, n_random=60)
        degen[f"gamma={g}"] = {"per_degree": _floats(pd), "random_best": rb}
    n_zero = sum(1 for r in rows if r["random_best_is_exactly_zero"])
    return {
        "clean_per_degree": _floats(clean_pd),
        "clean_random_best": clean_rb,
        "n_cases": len(rows),
        "n_random_arm_silently_zero": n_zero,
        "degenerate_exponent_sweep": degen,
        "note": "the per-degree arm propagates NaN (it is a plain list comprehension), "
                "but the random arm collapses to 0.0 -- a caller who reads only the "
                "second return value is told the Holder-Hilbert constant is zero, "
                "against a clean value of %.6f" % clean_rb,
        "cases": rows,
    }


# ---------------------------------------------------------------------------
# A7 -- positive control: does ANY input make this module raise?
# ---------------------------------------------------------------------------


def gate_A7():
    """A battery that never sees a signal proves nothing unless the instrumentation can
    see one.  These calls are structurally malformed (wrong shapes / wrong dtype), and the
    module must fail on them -- if it does not, the harness is blind, not the module."""
    J = 32
    th, X = grid(J)
    rows = []
    n = HolderNorm(th, X, 1.0, 0.3)
    for label, fn, args in (
        ("HolderNorm called on a wrong-length vector", n, (np.ones(J + 1),)),
        ("family_op_norm with a non-conforming operator",
         family_op_norm, (np.ones((J, J + 3)), n, n)),
        ("square_wave_partial_sum with m = NaN", square_wave_partial_sum, (th, NAN)),
        ("holder_H_constant with random degree above grid size",
         holder_H_constant, (th, 0.3)),
    ):
        val, exc, warns = call(fn, *args)
        rows.append({"case": label, "exception": exc, "warnings": warns,
                     "signalled": exc is not None or bool(warns)})
    return {
        "n_cases": len(rows),
        "n_signalled": sum(1 for r in rows if r["signalled"]),
        "cases": rows,
        "note": "the harness CAN see a signal; every silence reported above is the "
                "module's, not the instrumentation's",
    }


# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# A8 -- how durable is the ONE signal the Inf cases produce?
# ---------------------------------------------------------------------------


def gate_A8():
    """Several Inf cases above are classified FLAGGED_WARN, but the flag is not the
    module's: it is an incidental numpy `RuntimeWarning: invalid value encountered`, and
    the RETURNED NUMBER is the same wrong one the NaN twin returns.  Python's DEFAULT
    warning filter shows a given warning once per location, so the second identical call
    in the same process is silent while returning the same wrong value.  This gate
    measures that decay rather than asserting it."""
    J = 128
    th, _ = grid(J)
    clean = conformal_check(th, 0.3)
    t_inf = th.copy(); t_inf[64] = INF
    _, X48, A, dn, cn = _substrate()
    A_inf = A.copy(); A_inf[3, 7] = INF
    clean_op = family_op_norm(A, dn, cn)

    rows = []
    for label, fn, args, ref in (
        ("conformal_check, theta[64] = +Inf", conformal_check, (t_inf, 0.3), list(clean)),
        ("family_op_norm, A[3,7] = +Inf", family_op_norm, (A_inf, dn, cn), list(clean_op)),
    ):
        seen = []
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("default")     # the interpreter's own default policy
            for k in range(3):
                before = len(caught)
                val = fn(*args)
                seen.append({"call": k + 1, "n_new_warnings": len(caught) - before,
                             "returned": _floats(val)})
        rows.append({
            "case": label,
            "clean": ref,
            "calls": seen,
            "warned_on_first_call": seen[0]["n_new_warnings"] > 0,
            "silent_from_call": next((s["call"] for s in seen
                                      if s["n_new_warnings"] == 0), None),
            "returned_value_constant_across_calls": all(
                s["returned"] == seen[0]["returned"] for s in seen),
        })
    n_decay = sum(1 for r in rows if r["silent_from_call"] is not None)
    return {
        "n_cases": len(rows),
        "n_that_go_silent_on_repeat": n_decay,
        "cases": rows,
        "note": "under the interpreter's default warning filter the RuntimeWarning is "
                "emitted once per source location; repeat calls return the identical "
                "wrong value with no signal at all, so the Inf cases are silent in every "
                "practical caller and the NaN/Inf distinction is one warning wide",
    }


def verdict(A0, A1, A2, A3, A4, A5, A6, A8=None):
    findings = []
    if A1["n_bit_identical_to_clean"]:
        findings.append(
            "conformal_check/jacobian_identity_error return values BIT-IDENTICAL to the "
            "clean grid on %d of %d NaN/Inf-poisoned grids (%.9g, unchanged)"
            % (A1["n_bit_identical_to_clean"], A1["n_cases"],
               A1["clean_conformal_check"][0]))
    if A2["all_nan_grid_verdict"] == "SILENT":
        findings.append(
            "conformal_check on an all-NaN grid returns %s -- worst deviation 0.0, a "
            "PERFECT pass" % (A2["all_nan_grid_returns"],))
    if A3["n_silent_returning_exactly_zero"]:
        findings.append(
            "family_op_norm returns exactly 0.0 (arg = -1) on %d of %d poisoned "
            "operators, against a clean %.6f"
            % (A3["n_silent_returning_exactly_zero"], A3["n_cases"],
               A3["clean_family_op_norm"][0]))
    if A4["n_silent"]:
        findings.append(
            "family_op_norm silently discards a poisoned test vector and returns the "
            "runner-up: %.6f instead of %.6f, a %.4fx understatement"
            % (A4["ratio_runner_up"], A4["ratio_true_maximizer"],
               A4["understatement_factor"]))
    if A6["n_random_arm_silently_zero"]:
        findings.append(
            "holder_H_constant's random arm returns exactly 0.0 on %d of %d poisoned "
            "inputs, against a clean %.6f"
            % (A6["n_random_arm_silently_zero"], A6["n_cases"],
               A6["clean_random_best"]))
    if A8 and A8["n_that_go_silent_on_repeat"]:
        findings.append(
            "the Inf twins of those cases return the same wrong value and are flagged "
            "only by an incidental numpy RuntimeWarning that stops firing from call %s "
            "onward under the default warning filter (%d of %d cases)"
            % (A8["cases"][0]["silent_from_call"], A8["n_that_go_silent_on_repeat"],
               A8["n_cases"]))
    return {
        "gate": "Under an adversarial battery (NaN/Inf-poisoned weight-class parameters, "
                "degenerate grading exponents), does solver/holder_norms.py's norm or "
                "embedding-constant computation ever silently return a finite, "
                "plausible-looking wrong value instead of propagating or flagging the "
                "invalid input?",
        "answer": "YES" if findings else "NO",
        "n_distinct_silent_mechanisms": len(findings),
        "findings": findings,
        "not_silent": [
            "the norm objects themselves (HolderNorm.sup_part / .seminorm / .__call__) "
            "propagate NaN through np.max on every poisoned exponent and every poisoned "
            "grid tested (gate A5): %d of %d cases SILENT"
            % (A5["n_silent"], A5["n_cases"]),
            "holder_H_constant's per-degree arm propagates NaN on every poisoned input",
        ],
        "disposition": "solver/holder_norms.py is NOT patched under this leg (territory "
                       "rule); the battery is banked as test_holder_norms_adversarial.py, "
                       "which PINS the silence and will fail the day a guard lands -- "
                       "invert it then, do not weaken it.",
    }


def main():
    t0 = time.time()
    A0, A1, A2 = gate_A0(), gate_A1(), gate_A2()
    A3, A4, A5 = gate_A3(), gate_A4(), gate_A5()
    A6, A7, A8 = gate_A6(), gate_A7(), gate_A8()
    out = {
        "leg": 100,
        "route": "HNA",
        "module_under_audit": "solver/holder_norms.py",
        "module_edited": False,
        "A0_validation_surface": A0,
        "A1_self_validation_on_poisoned_grid": A1,
        "A2_vacuous_pass": A2,
        "A3_poisoned_operator": A3,
        "A4_dropped_maximizer": A4,
        "A5_norms_under_poisoned_exponents": A5,
        "A6_embedding_constant": A6,
        "A7_positive_control": A7,
        "A8_warning_decay": A8,
        "verdict": verdict(A0, A1, A2, A3, A4, A5, A6, A8),
        "runtime_seconds": None,
    }
    out["runtime_seconds"] = round(time.time() - t0, 2)
    path = os.path.join(HERE, "writeup", "data", "p2_route_hna_v1_adversarial.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print(f"A0 validation surface: {A0['n_raise_sites']} raise, {A0['n_assert_sites']} "
          f"assert, guards {A0['finiteness_guard_names_present']} across "
          f"{A0['n_public_entry_points']} public entry points")
    print(f"A1 self-validation: {A1['n_silent']}/{A1['n_cases']} silent, "
          f"{A1['n_bit_identical_to_clean']} bit-identical to the clean grid "
          f"(clean err {A1['clean_conformal_check'][0]:.9g})")
    print(f"A2 vacuous pass: all-NaN grid -> {A2['all_nan_grid_returns']} "
          f"({A2['all_nan_grid_verdict']})")
    print(f"A3 poisoned operator: {A3['n_silent']}/{A3['n_cases']} silent, "
          f"{A3['n_silent_returning_exactly_zero']} return exactly 0.0 against a clean "
          f"{A3['clean_family_op_norm'][0]:.6f}")
    print(f"A4 dropped maximizer: {A4['ratio_runner_up']:.6f} returned vs "
          f"{A4['ratio_true_maximizer']:.6f} true, "
          f"{A4['understatement_factor']:.4f}x understatement, "
          f"{A4['n_silent']}/{A4['n_cases']} silent")
    print(f"A5 norms: {A5['n_silent']}/{A5['n_cases']} silent; "
          f"decay_weight(X=0, alpha=NaN) = {A5['decay_weight_at_X0_with_NaN_alpha']}")
    print(f"A6 embedding constant: random arm 0.0 on "
          f"{A6['n_random_arm_silently_zero']}/{A6['n_cases']} poisoned inputs, clean "
          f"{A6['clean_random_best']:.6f}")
    print(f"A7 positive control: {A7['n_signalled']}/{A7['n_cases']} signalled")
    print(f"A8 warning decay: {A8['n_that_go_silent_on_repeat']}/{A8['n_cases']} Inf cases "
          f"go silent from call {A8['cases'][0]['silent_from_call']} onward, same value")
    v = out["verdict"]
    print(f"VERDICT: {v['answer']} -- {v['n_distinct_silent_mechanisms']} distinct silent "
          f"mechanisms")
    for f in v["findings"]:
        print(f"  * {f}")
    print(f"wrote {path} in {out['runtime_seconds']}s")
    return out


if __name__ == "__main__":
    main()
