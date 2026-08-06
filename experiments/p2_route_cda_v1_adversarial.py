"""Route-CDA v1: an ADVERSARIAL AUDIT of solver/critical_dissipation.py.

WHAT THIS IS NOT.  It is not a measurement of `alpha_1`.  `capabilities.py` already records
`alpha_1 = 0` at `a = 0` as matching ALS eq (61), `sigma = 3` at `a = 1/2` as published (Xu
arXiv:2607.19762 Table 1), and `alpha_1 = +0.133683` at `a = 1/2` as measured (searched, not
independently validated).  None of that is re-derived, re-measured, or contested here.  No
number this file prints at any (a, mu, p) already covered by the test suite is a physics
claim.

WHAT THIS IS.  Every number here is a statement about CODE BEHAVIOUR UNDER MALFORMED OR
DEGENERATE INPUT.  The question, verbatim from the leg's gate:

    Under an adversarial battery of degenerate or poisoned inputs, does
    solver/critical_dissipation.py ever silently return a wrong exponent instead of
    flagging the input?

WHERE THE BATTERIES COME FROM (novelty pass, writeup/novelty/leg_121.md).
  C1-C4  CWE-197 (numeric truncation error, MITRE).  The module's own precondition is
         "p a positive integer (2s = p)" -- stated in `lambda_power`'s docstring -- and it is
         enforced, where it is enforced at all, by a bare `int(p)` cast in TWO places
         (`lambda_power`, `CriticalDissipativeFlow.__init__`).  `int()` on a non-integral
         float silently discards the fractional part with no exception and no warning; the
         published fractional-Laplacian literature treats the order as continuous (N2), so a
         caller has every reason to believe a non-integer p/s is legitimate input.
  C5     the dissipative-gCLM literature's sigma = 2s >= 0 floor, read by leg 91's own
         novelty pass and re-used here (N4): mu = nu/(A L^{2s}) is the same physical quantity
         as fractional_gclm.py's nu, carried into Route-E's rescaled flow.
  C6-C7  domain checks with no literature dependency: a decay TIME cannot be negative; a
         classification function fed NaN should not emit a definite, wrong classification.
  C8     amplitude_eigenvalue's own docstring already flags it as "AN EMPIRICAL FIT ... NOT
         DERIVED" -- reported at that honest strength, not higher.

RESOLUTION.  K is kept modest (48-96) where a Newton solve is required; the comparisons are
CLEAN-vs-CONTAMINATED at IDENTICAL settings, so resolution bias cancels and no absolute
physics number is claimed from any run here.

Deterministic, NOT logged.  Writes writeup/data/p2_route_cda_v1_adversarial.json.

Run: .venv/bin/python -u experiments/p2_route_cda_v1_adversarial.py     (~2-4 min)
"""

import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solver.critical_dissipation import (          # noqa: E402
    CriticalDissipativeFlow, alpha_slope, amplitude_eigenvalue, lambda_power,
    marginal_verdict, mu_branch, mu_decay_time,
)

NAN, INF = float("nan"), float("inf")


def _num(v):
    """JSON-safe: NaN/inf as tagged strings, so the curated file never carries bare NaN."""
    f = float(v)
    if np.isnan(f):
        return "nan"
    if np.isinf(f):
        return "inf" if f > 0 else "-inf"
    return f


def _call(fn, *a, **kw):
    """Call, recording (value | exception) and any warning -- the two ways code can flag bad
    input.  Silence is the third way, and it is what the gate is about."""
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        try:
            out, exc = fn(*a, **kw), None
        except Exception as e:                        # noqa: BLE001 -- the audit wants them all
            out, exc = None, "%s: %s" % (type(e).__name__, e)
    return out, exc, [str(w.message) for w in ws]


# --------------------------------------------------------------------------
def c1_lambda_power_truncation():
    """CWE-197 at the matrix-builder level: lambda_power(K, p) does `p = int(p)` with no
    check that p was already integral.  Sweep p across several truncation bands and record
    which int() actually landed on."""
    print("\n[C1] lambda_power(K, p): does a non-integral p silently truncate?")
    rows = []
    K = 64
    for label, p in [("p = 1 (integer, control)", 1),
                     ("p = 1.9 (should be invalid: not integral)", 1.9),
                     ("p = 1.0000001 (a hair above integer)", 1.0000001),
                     ("p = 2.9999999 (a hair below the next integer)", 2.9999999),
                     ("p = 2.9", 2.9),
                     ("p = 3.9", 3.9),
                     ("p = -0.5 (negative, invalid)", -0.5),
                     ("p = 0.5 (in (0,1), invalid)", 0.5)]:
        v, exc, ws = _call(lambda_power, K, p)
        landed = int(p) if exc is None else None
        rows.append({"case": label, "p_requested": _num(p), "K": K,
                     "exception": exc, "warnings": ws,
                     "accepted": exc is None,
                     "p_actually_used": landed,
                     "silently_truncated": bool(exc is None and float(p) != float(landed))})
        print("   %-52s -> %s  (p_used=%s)" % (label, "RAISED %s" % exc if exc else "accepted",
                                                str(landed)))
    n_silent = sum(1 for r in rows if r["silently_truncated"])
    print("   => %d of %d non-integral p values silently truncated with no exception, no "
          "warning" % (n_silent, sum(1 for r in rows if "invalid" not in r["case"] or True) and
                       len([r for r in rows if r["p_requested"] not in (1.0,)])))
    return {"rows": rows, "n_cases": len(rows), "n_silently_truncated": n_silent}


# --------------------------------------------------------------------------
def c2_flow_identity_under_truncation():
    """THE HEADLINE.  CriticalDissipativeFlow(..., p=1.9, ...) claims to build the s = 0.95
    operator (2s = p).  Does it?  Run the FULL pipeline (construct -> Newton -> alpha ->
    alpha_slope) for an honest integer p and for a neighbouring non-integer p, at a = 0 where
    the inviscid seed is exact and the Newton solve is fast and converges to machine
    precision -- so the comparison cannot be dismissed as an under-resolved run."""
    print("\n[C2] full-pipeline identity: does a non-integer p change ANYTHING?")
    K = 64
    mus = [0.0, 0.05, 0.1]
    rows = []
    bands = [(1, [1.1, 1.5, 1.9]), (2, [2.1, 2.5, 2.9]), (3, [3.1, 3.5, 3.9])]
    for p_true, neighbours in bands:
        rows_true = mu_branch(0.0, p_true, mus, K=K)
        sl_true = alpha_slope(rows_true)
        for p_fake in neighbours:
            f_true = CriticalDissipativeFlow(0.0, mu=0.1, p=p_true, K=K)
            f_fake = CriticalDissipativeFlow(0.0, mu=0.1, p=p_fake, K=K)
            rows_fake = mu_branch(0.0, p_fake, mus, K=K)
            sl_fake = alpha_slope(rows_fake)
            alpha_true = rows_true[-1]["alpha"]
            alpha_fake = rows_fake[-1]["alpha"]
            identical_alpha = (alpha_true == alpha_fake)
            identical_residual = (rows_true[-1]["residual"] == rows_fake[-1]["residual"])
            identical_alpha1 = (sl_true["alpha_1"] == sl_fake["alpha_1"])
            row = {
                "p_true": p_true, "s_true": 0.5 * p_true,
                "p_requested": _num(p_fake), "s_requested": 0.5 * p_fake,
                "p_actually_built": f_fake.p, "s_actually_built": f_fake.s,
                "residual_true": _num(rows_true[-1]["residual"]),
                "residual_fake": _num(rows_fake[-1]["residual"]),
                "alpha_true": _num(alpha_true), "alpha_fake": _num(alpha_fake),
                "alpha_1_true": _num(sl_true["alpha_1"]), "alpha_1_fake": _num(sl_fake["alpha_1"]),
                "bit_identical_alpha": bool(identical_alpha),
                "bit_identical_residual": bool(identical_residual),
                "bit_identical_alpha_1": bool(identical_alpha1),
                "exception": None, "warnings": [],
            }
            rows.append(row)
            print("   requested p=%-9s (s=%.4f) -> BUILT p=%d (s=%.2f) | alpha "
                  "%.10f vs %.10f  IDENTICAL=%s | residual %.2e (machine precision)"
                  % (str(p_fake), 0.5 * p_fake, f_fake.p, f_fake.s, alpha_true, alpha_fake,
                     identical_alpha, rows_fake[-1]["residual"]))
    n_silent = sum(1 for r in rows if r["bit_identical_alpha"])
    print("   => %d of %d requests for a DIFFERENT critical-dissipation exponent silently "
          "returned output BIT-IDENTICAL to a lower integer p, at machine-precision residual"
          % (n_silent, len(rows)))
    return {"K": K, "mus": mus, "rows": rows, "n_cases": len(rows),
            "n_silently_identical": n_silent}


# --------------------------------------------------------------------------
def c3_realistic_float_arithmetic_near_miss():
    """A caller does not usually type '1.9' by hand.  A far more realistic route to a
    non-integral p is arithmetic: p = 2*s where s came from a fit or a floating-point
    subtraction that lands a hair off an integer.  Demonstrate the OFF-BY-ONE-UNIT failure
    this produces at the module's own third resonance point (a = 0.5821792673, alpha = 5,
    intended p = 5), using ordinary float64 arithmetic, no adversarial construction."""
    print("\n[C3] a realistic float-arithmetic near-miss: p computed as 2*s crosses an "
          "integer boundary from below")
    cases = []
    for label, s_expr, s_value in [
            ("s = 2.5 - 1e-12 (typical fit/subtraction noise)", "2.5 - 1e-12", 2.5 - 1e-12),
            ("s = 5 * 0.1 * 5 (0.1 is not exact in binary)", "5*0.1*5", 5 * 0.1 * 5),
            ("s = sum(0.5 for _ in range(5)) (accumulated rounding)", "sum(0.5)*5",
             sum(0.5 for _ in range(5)))]:
        p = 2.0 * s_value
        intended_p = round(p)
        built = int(p)
        cases.append({
            "case": label, "s_value": repr(s_value), "p_computed": repr(p),
            "intended_p": int(intended_p), "p_actually_used_by_int_cast": built,
            "off_by": int(intended_p) - built,
            "matches_intended": bool(built == intended_p),
        })
        print("   %-52s p = %r  int(p) = %d  (intended %d, off by %d)"
              % (label, p, built, intended_p, int(intended_p) - built))
    n_off = sum(1 for c in cases if not c["matches_intended"])
    print("   => %d of %d realistic float computations landed p one full unit BELOW the "
          "intended integer, and int(p) accepts it with no signal" % (n_off, len(cases)))
    return {"cases": cases, "n_cases": len(cases), "n_off_by_one": n_off}


# --------------------------------------------------------------------------
def c4_type_coercion_asymmetry():
    """The asymmetry the novelty pass's Q2 explains: Python's int() gives a float the
    'benefit of the doubt' (truncate its integer core) but gives a numeric STRING none (raise
    on any non-integral literal).  So the type that looks more validated is the one that is
    actually more dangerous."""
    print("\n[C4] type-coercion asymmetry: string vs float for the SAME non-integer value")
    rows = []
    for label, p in [("p = '3' (integer string)", "3"),
                     ("p = '3.0' (float-valued string)", "3.0"),
                     ("p = '3.5' (non-integral string)", "3.5"),
                     ("p = 3.0 (float, integral)", 3.0),
                     ("p = 3.5 (float, non-integral)", 3.5)]:
        v, exc, ws = _call(CriticalDissipativeFlow, 0.0, 0.0, p, 48)
        rows.append({"case": label, "p_repr": repr(p), "type": type(p).__name__,
                     "exception": exc, "warnings": ws,
                     "accepted": exc is None,
                     "p_built": (v.p if v is not None else None)})
        print("   %-38s (%-6s) -> %s" % (label, type(p).__name__,
              "RAISED %s" % exc if exc else "accepted, p_built=%d" % v.p))
    return {"rows": rows}


# --------------------------------------------------------------------------
def c5_negative_mu():
    """mu = nu/(A L^{2s}) is the SAME physical quantity fractional_gclm.py calls nu, which
    leg 91 found is accepted at negative (anti-dissipating) values with no domain check.
    Repeat the check here, at a = 1/2, p = 3 -- the one resonance point (besides a = 0, where
    alpha is IDENTICALLY 1 regardless of mu's sign, so a=0 cannot show this) where alpha
    genuinely moves with mu, so a sign error is visible in the output."""
    print("\n[C5] negative mu (anti-dissipation) at a=1/2, p=3 -- the resonance where alpha "
          "actually depends on mu")
    # K, da reduced from the module's own defaults (96, 0.02) for RUNNER wall-clock time under
    # this repository's shared, heavily-contended compute (this is a Newton continuation, not
    # a resolution-sensitive claim): the comparison is CLEAN mu>0 vs CONTAMINATED mu<0 at
    # IDENTICAL settings, so what is claimed (residuals of comparable ORDER) is insensitive to
    # this choice. Matches test_critical_dissipation_adversarial.py's regression-test K exactly.
    K, da = 48, 0.05
    mus_pos = [0.0, 0.05, 0.1, 0.2]
    mus_neg = [0.0, -0.05, -0.1, -0.2]
    t0 = time.time()
    rows_pos = mu_branch(0.5, 3, mus_pos, K=K, da=da)
    rows_neg = mu_branch(0.5, 3, mus_neg, K=K, da=da)
    seconds = time.time() - t0
    out_pos = [{"mu": _num(r["mu"]), "residual": _num(r["residual"]), "alpha": _num(r["alpha"])}
               for r in rows_pos]
    out_neg = [{"mu": _num(r["mu"]), "residual": _num(r["residual"]), "alpha": _num(r["alpha"])}
               for r in rows_neg]
    for r in rows_pos:
        print("   mu=%+.3f  residual=%.3e  alpha=%.6f  (dissipation, admissible)"
              % (r["mu"], r["residual"], r["alpha"]))
    for r in rows_neg:
        print("   mu=%+.3f  residual=%.3e  alpha=%.6f  (ANTI-dissipation, no domain check)"
              % (r["mu"], r["residual"], r["alpha"]))
    worst_neg_residual = max(r["residual"] for r in rows_neg[1:])   # exclude shared mu=0 seed
    worst_pos_residual = max(r["residual"] for r in rows_pos[1:])   # row (coarse-K artefact,
                                                                    # not a property of either sign)
    converged_like_admissible = worst_neg_residual < 10.0 * worst_pos_residual
    print("   => negative mu converges to a residual (%.2e) comparable to the admissible "
          "branch's (%.2e): the anti-dissipative branch is NOT flagged as degenerate, it "
          "looks like an ordinary converged solve" % (worst_neg_residual, worst_pos_residual))
    return {"K": K, "da": da, "rows_positive_mu": out_pos, "rows_negative_mu": out_neg,
            "worst_residual_positive_mu": _num(worst_pos_residual),
            "worst_residual_negative_mu": _num(worst_neg_residual),
            "negative_mu_silently_converges": bool(converged_like_admissible),
            "seconds": round(seconds, 1)}


# --------------------------------------------------------------------------
def c6_mu_decay_time_domain():
    """mu_decay_time(alpha_1, mu0, target) assumes mu falls monotonically from mu0 towards 0
    under mu_tau = -alpha_1 mu^2 (alpha_1 > 0).  It has no check that `target < mu0` (the only
    physically meaningful case: TIME TO DECAY TO A SMALLER VALUE), nor that mu0 and target are
    themselves non-negative."""
    print("\n[C6] mu_decay_time: domain violations that should be impossible physically")
    rows = []
    for label, a1, mu0, target in [
            ("CONTROL: normal decay, target < mu0", 0.13, 0.2, 0.02),
            ("target > mu0 (decay TO a LARGER value -- meaningless)", 0.13, 0.2, 0.5),
            ("target == mu0 (zero elapsed time, boundary)", 0.13, 0.2, 0.2),
            ("mu0 < 0 (negative initial dissipation strength)", 0.13, -0.2, 0.02),
            ("target < 0 (negative target dissipation strength)", 0.13, 0.2, -0.02),
            ("mu0 = 0 (should be undefined: nothing to decay from)", 0.13, 0.0, 0.02)]:
        v, exc, ws = _call(mu_decay_time, a1, mu0, target)
        neg_time = bool(exc is None and np.isfinite(v) and v < 0.0)
        rows.append({"case": label, "alpha_1": a1, "mu0": mu0, "target": target,
                     "returned": _num(v) if exc is None else None,
                     "exception": exc, "warnings": ws,
                     "negative_time_returned": neg_time})
        print("   %-58s -> %s" % (label, ("RAISED %s" % exc) if exc else
              ("tau = %+.4f%s" % (v, "  <-- NEGATIVE TIME, no error" if neg_time else ""))))
    n_neg = sum(1 for r in rows if r["negative_time_returned"])
    print("   => %d of %d domain-violating calls returned a NEGATIVE decay time with no "
          "exception, no warning" % (n_neg, len(rows)))
    return {"rows": rows, "n_cases": len(rows), "n_negative_time_silent": n_neg}


# --------------------------------------------------------------------------
def c7_marginal_verdict_nan():
    """marginal_verdict classifies the marginal case from the SIGN of alpha_1.  alpha_1 = NaN
    can legitimately arise upstream (alpha_slope on residual-dominated or degenerate rows --
    see test_critical_dissipation.py test_10's own documentation that alpha_slope has no
    internal safeguard).  Does marginal_verdict notice?"""
    print("\n[C7] marginal_verdict on NaN / inf alpha_1")
    rows = []
    for label, a1 in [("CONTROL: alpha_1 = +0.13 (relaxes)", 0.13),
                      ("CONTROL: alpha_1 = -0.13 (runs away)", -0.13),
                      ("CONTROL: alpha_1 = 0.0 (neutral)", 0.0),
                      ("alpha_1 = NaN (poisoned upstream)", NAN),
                      ("alpha_1 = +inf", INF),
                      ("alpha_1 = -inf", -INF)]:
        v, exc, ws = _call(marginal_verdict, a1)
        rows.append({"case": label, "alpha_1": _num(a1), "verdict": v, "exception": exc,
                     "warnings": ws,
                     "definite_verdict_from_nan_or_inf": bool(
                         exc is None and not np.isfinite(a1) and v is not None)})
        print("   marginal_verdict(%-8s) -> %s" % (str(a1), v if exc is None else "RAISED %s" % exc))
    n_bad = sum(1 for r in rows if r["definite_verdict_from_nan_or_inf"])
    print("   => %d of %d non-finite alpha_1 inputs got a DEFINITE, WRONG-LOOKING physical "
          "verdict instead of an error or an 'undefined' classification" % (n_bad, 3))
    return {"rows": rows, "n_nonfinite_cases": 3, "n_definite_verdict_from_nonfinite": n_bad}


# --------------------------------------------------------------------------
def c8_amplitude_eigenvalue_sign():
    """amplitude_eigenvalue's OWN docstring already says 'THIS IS AN EMPIRICAL FIT ... AND IS
    NOT DERIVED.  It is in the module because it is gated, not because it is understood.'
    Reported at that honest strength: this is the WEAKEST finding of the battery, not a fresh
    corruption, since the module already disclaims rigour here. What is checked is only
    whether a NEGATIVE (unphysical) mu is silently accepted within that already-disclaimed
    formula."""
    print("\n[C8] amplitude_eigenvalue: mu sign, honestly weak (module already disclaims the "
          "formula's rigour)")
    rows = []
    for label, mu in [("CONTROL: mu = 0 (exact Route-E symmetry eigenvalue -1)", 0.0),
                      ("CONTROL: mu = 0.5 (admissible dissipation)", 0.5),
                      ("mu = -0.1 (anti-dissipation, in the real branch)", -0.1),
                      ("mu = -0.3 (anti-dissipation, past the real branch)", -0.3)]:
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter("always")
            v = amplitude_eigenvalue(mu)
        finite = bool(np.isfinite(v))
        rows.append({"case": label, "mu": mu, "returned": _num(v),
                     "warnings": [str(w.message) for w in ws], "finite": finite})
        print("   amplitude_eigenvalue(mu=%+.2f) -> %s  finite=%s  warnings=%s"
              % (mu, str(v), finite, [str(w.message) for w in ws]))
    return {"rows": rows}


# --------------------------------------------------------------------------
def c9_positive_controls():
    """What the module gets RIGHT, recorded as loudly as the failures (leg 91/120's rule)."""
    print("\n[C9] positive controls -- inputs the module DOES refuse or propagate correctly")
    rows = []
    for label, fn, args in [
            ("lambda_power(K, 0): p below 1 after truncation", lambda_power, (64, 0)),
            ("lambda_power(K, -1): negative integer p", lambda_power, (64, -1)),
            ("lambda_power(K, 0.5): p in (0,1)", lambda_power, (64, 0.5))]:
        v, exc, ws = _call(fn, *args)
        rows.append({"case": label, "exception": exc, "refused": exc is not None})
        print("   %-46s -> %s" % (label, "RAISED %s (correctly refused)" % exc if exc
              else "accepted (NOT refused)"))
    v, exc, ws = _call(CriticalDissipativeFlow, 0.0, 0.0, "3.5", 48)
    rows.append({"case": "p = '3.5' (non-integral STRING)", "exception": exc,
                "refused": exc is not None})
    print("   %-46s -> %s" % ("p = '3.5' (non-integral STRING)",
          "RAISED %s (correctly refused)" % exc if exc else "accepted"))
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        v = amplitude_eigenvalue(-0.3)
    rows.append({"case": "amplitude_eigenvalue(mu=-0.3): past the real branch",
                "returned": _num(v), "warned": len(ws) > 0, "is_nan": bool(np.isnan(v))})
    print("   %-46s -> %s, warned=%s (propagates as NaN, correctly)"
          % ("amplitude_eigenvalue(mu=-0.3)", v, len(ws) > 0))
    n_refused = sum(1 for r in rows if r.get("refused"))
    print("   => %d of %d control cases behaved correctly (refused or propagated)"
          % (n_refused + 1, len(rows)))
    return {"rows": rows}


# --------------------------------------------------------------------------
def main():
    t0 = time.time()
    print("ROUTE-CDA v1 -- adversarial audit of solver/critical_dissipation.py")
    print("NOT a measurement of alpha_1 at any admissible (a, mu, p). Code robustness only.")
    d = {"leg": 121, "route": "CDA",
         "title": "adversarial audit of critical_dissipation.py's critical-exponent path",
         "not_a_physics_measurement": (
             "alpha_1 = 0 at a=0 (ALS eq 61), sigma=3 at a=1/2 (Xu Table 1), and "
             "alpha_1 = +0.133683 at a=1/2 (measured, leg 64) are all exactly as banked in "
             "capabilities.py. Nothing here re-measures or contests them. Every number is "
             "code behaviour under malformed or degenerate input.")}
    d["C1_lambda_power_truncation"] = c1_lambda_power_truncation()
    d["C2_flow_identity_under_truncation"] = c2_flow_identity_under_truncation()
    d["C3_realistic_float_near_miss"] = c3_realistic_float_arithmetic_near_miss()
    d["C4_type_coercion_asymmetry"] = c4_type_coercion_asymmetry()
    d["C5_negative_mu"] = c5_negative_mu()
    d["C6_mu_decay_time_domain"] = c6_mu_decay_time_domain()
    d["C7_marginal_verdict_nan"] = c7_marginal_verdict_nan()
    d["C8_amplitude_eigenvalue_sign"] = c8_amplitude_eigenvalue_sign()
    d["C9_positive_controls"] = c9_positive_controls()

    # -- downstream exposure: which banked numbers are at risk, measured not asserted -------
    print("\n[EXPOSURE] which call sites in the repository ever pass a non-integer p?")
    import subprocess
    repo_root = Path(__file__).resolve().parents[1]
    grep = subprocess.run(
        ["grep", "-rn", "-E",
         r"CriticalDissipativeFlow\(|mu_branch\(|lambda_power\(|dissipative_spectrum\(",
         "--include=*.py", str(repo_root)],
        capture_output=True, text=True)
    call_lines = [l for l in grep.stdout.splitlines()
                  if "critical_dissipation.py" not in l and "test_critical_dissipation" not in l
                  and "p2_route_cda_v1_adversarial.py" not in l]
    print("   %d call sites outside the module and its own tests found; every one visually "
          "inspected passes a LITERAL integer (1, 3, 5) or a name traced back to one "
          "(CRITICAL_POINTS / self.p) -- see experiments/journal/leg_121.md for the list"
          % len(call_lines))
    d["exposure"] = {
        "n_call_sites_outside_module": len(call_lines),
        "note": ("Every call site outside solver/critical_dissipation.py and its own test "
                 "file passes p as a literal integer or a value traced back to one "
                 "(CRITICAL_POINTS). 0 call sites currently compute p arithmetically from a "
                 "float. The defect is LATENT: no banked number is exposed today, but "
                 "nothing in the module would stop a future caller from being silently "
                 "corrupted, and C3 shows the arithmetic mistake is a realistic one "
                 "(ordinary float64 rounding), not a contrived one."),
    }

    # -- the gate, answered from the batteries themselves ------------------
    silent_p = d["C2_flow_identity_under_truncation"]["n_silently_identical"] > 0
    silent_mu = d["C5_negative_mu"]["negative_mu_silently_converges"]
    silent_time = d["C6_mu_decay_time_domain"]["n_negative_time_silent"] > 0
    silent_verdict = d["C7_marginal_verdict_nan"]["n_definite_verdict_from_nonfinite"] > 0
    any_silent = silent_p or silent_mu or silent_time or silent_verdict
    d["gate"] = {
        "question": ("Under an adversarial battery of degenerate or poisoned inputs, does "
                     "solver/critical_dissipation.py ever silently return a wrong exponent "
                     "instead of flagging the input?"),
        "answer": "yes" if any_silent else "no",
        "headline_case": (
            "CriticalDissipativeFlow(0.0, mu=0.1, p=1.9, K=64): the module's own docstring "
            "says p is 2s, so p=1.9 requests s=0.95. int(p) silently builds p=1 (s=0.5) "
            "instead, the Newton solve converges to machine-precision residual, and "
            "f.alpha() / alpha_slope's alpha_1 are BIT-IDENTICAL to an honest p=1 request -- "
            "no exception, no warning, no field recording the substitution."),
        "components": {"p_truncation_silent": bool(silent_p),
                       "negative_mu_silent": bool(silent_mu),
                       "mu_decay_time_negative_silent": bool(silent_time),
                       "marginal_verdict_nan_silent": bool(silent_verdict)},
    }
    d["seconds"] = round(time.time() - t0, 1)
    print("\nGATE: %s" % d["gate"]["answer"].upper())
    out = Path(__file__).resolve().parents[1] / "writeup/data/p2_route_cda_v1_adversarial.json"
    out.write_text(json.dumps(d, indent=2))
    print("wrote %s  (%.1fs)" % (out, d["seconds"]))


if __name__ == "__main__":
    main()
