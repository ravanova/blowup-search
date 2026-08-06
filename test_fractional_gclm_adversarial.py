"""ADVERSARIAL gates for solver/fractional_gclm.py -- Route-FGA, leg 91, INVERTED after repair.

`test_fractional_gclm.py` (Route-F) tests that the module MEASURES correctly, at
physically admissible `s`.  This file tests what the module SAYS when the caller hands it
a dissipation exponent that is not admissible at all.

**THIS FILE MAKES NO CLAIM ABOUT THE VALUE OF s_c.**  `s_c = alpha/2` is validated against
XU eq (6.3) row by row and is marked PRE-EMPTED under Route-J.  That is settled physics,
treated here as fixed background, and nothing below re-derives, re-measures or contests it.
Every assertion is about CODE BEHAVIOUR UNDER INVALID INPUT.

WHERE "INVALID" COMES FROM.  Not from taste.  The dissipative-gCLM literature writes the
dissipation as `Lambda^sigma`-hat = |k|^sigma with **sigma = 2s**, and works at
**sigma >= 0** throughout; the lowest exponent anyone treats is the "marginal" sigma = 0
(Oldroyd-B stress).  So `s < 0` is outside every published range.  `s = 0` is ADMISSIBLE
and is carried below as a second positive control, never as a defect.  There is no
published upper bound, so the upper wall is a property of the CODE and is measured
(the float64 overflow of `|k|^{2s}`), not asserted.  See `writeup/novelty/leg_91.md`.

LEG 91'S GATE ANSWERED **YES (silent)**.  The failing case, exactly:

    FractionalGCLM(s = -0.5) builds `visc = |k|^{2s}`, whose k = 0 entry is `inf` -- and
    Riesz-potential theory says k = 0 is PRECISELY where a negative exponent is
    ill-defined.  The VERY NEXT LINE, `self.visc[0] = 0.0` ("the mean is not dissipated"),
    overwrites that `inf`.  What survives is a finite, all-real multiplier that DECREASES
    in |k| -- a smoothing operator wearing the dissipation's name -- and the run, the
    T-estimate and the relevance fit all complete and return finite numbers.  Injected
    into the p(s) fit whose zero crossing IS the measured s_c, one such point moved that
    crossing by +0.0803 (+13.3%) at s = -2.0 and by -0.00042 (-0.07%) at s = -0.5.

Leg 91 was forbidden to patch the module under its own authority and said so; the guard has
since landed (bench repair, `Leg 0: ORCH`) as a domain check in `FractionalGCLM.__init__`
that raises `ValueError` for `s < 0` and for `nu < 0`, before `visc` is built.

**Gates 6, 7, 8, 9 and 13 are INVERTED here, not weakened.**  The inversion is exact, in
the sense leg 84 set and leg 87 followed: every magnitude leg 91 measured is still asserted
at the same threshold -- the raw `k = 0` entry is still `inf`, the would-be multiplier still
inverts with ratio exactly `1/k_max` -- and what changed is only the sign of the SIGNAL
claim, from "and nothing says so" to "and the constructor refuses before reaching the line
that would hide it."

**Gates 2, 3 and 5 remain GAP PINS and still pass unchanged**, kept executable so they
cannot decay at the rate of memory (lesson 68).  The repair was scoped to the *operator*:
`critical_s` and `relevance_exponent` are pure closed forms with no domain attached, they
build no `visc`, and they were deliberately left alone.  A caller who evaluates the LINE
`p = 1 - 2s/alpha` at an invalid `s` still gets a number that sits on the valid points'
line.  That is a narrower hole than the one that closed -- it can no longer be reached
through the solver -- but it is still open, and this file says so out loud.

Gates 1 and 4 are the positive controls.  Gates 10-12 record what the module gets RIGHT --
the report is a map of behaviour, not a bug list -- and they are ordinary regressions:
NaN and inf inputs must keep propagating, and they must not be "fixed" into silence.  The
guard is written so they still do: `NaN < 0.0` is `False`, so NaN reaches the integrating
factor exactly as before.  Gate 14 is new with the repair and is the check that the guard
did not OVERSHOOT: `s = 0` is the literature's marginal case, it is ADMISSIBLE, and it must
keep constructing and running.

Run: .venv/bin/python test_fractional_gclm_adversarial.py
"""

import sys
import warnings

import numpy as np

sys.path.insert(0, ".")

from solver.fractional_gclm import (           # noqa: E402
    FractionalGCLM, critical_s, estimate_T, fit_relevance, relevance_exponent,
)

N = 256
NU = 1e-3
AMP = 1e3
MAX_STEPS = 4000
NAN, INF = float("nan"), float("inf")

PASS, FAIL = "PASS", "FAIL"
results = []


def gate(name, ok, detail):
    status = PASS if ok else FAIL
    results.append((status, name, detail))
    print("[%s] %s\n      %s" % (status, name, detail))


def call(fn, *args, **kw):
    """(value, exception, warnings) -- the three ways a module can answer bad input.
    Silence with a finite value is the fourth, and it is what this file measures."""
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        try:
            v, exc = fn(*args, **kw), None
        except Exception as e:                       # noqa: BLE001
            v, exc = None, "%s: %s" % (type(e).__name__, e)
    return v, exc, [str(w.message) for w in ws]


def w0(n=N):
    x = np.arange(n) * 2.0 * np.pi / n
    return np.sin(x) + 0.4 * np.sin(2.0 * x)


def pipeline(s, nu=NU, n=N):
    """The exact caller path Route-F's relevance line uses."""
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        try:
            g = FractionalGCLM(n=n, a=0.0, nu=nu, s=s)
            r = g.run(w0(n), amp_factor=AMP, sample_every=5, max_steps=MAX_STEPS)
            f = fit_relevance(r, estimate_T(r))
            exc = None
        except Exception as e:                       # noqa: BLE001
            r, f, exc = {"outcome": "EXCEPTION"}, {}, "%s: %s" % (type(e).__name__, e)
    return (float(f.get("p", NAN)), r["outcome"], exc,
            sorted({str(w.message) for w in ws}))


# ---------------------------------------------------------------- 1: control
p_ok, out_ok, exc_ok, _ = pipeline(0.35)
g_ok = FractionalGCLM(n=N, a=0.0, nu=NU, s=0.35)
gate("CONTROL: at an admissible s the module works and the operator is a dissipation",
     exc_ok is None and np.isfinite(p_ok) and np.all(np.diff(g_ok.visc[1:]) > 0.0)
     and g_ok.visc[0] == 0.0,
     "s = 0.35: visc is STRICTLY INCREASING in |k| (visc[1] = %.6g, visc[k_max] = %.6g), "
     "the mean mode is undamped, and the pipeline returns p = %+.4f with outcome '%s'. "
     "Everything below is measured against this row."
     % (g_ok.visc[1], g_ok.visc[-1], p_ok, out_ok))

# ------------------------------------------------- 2: the closed form has no guard at all
v_neg, e_neg, w_neg = call(critical_s, -1.0)
gate("PIN (silent): critical_s has no guard -- a negative decay exponent gives a "
     "negative s_c",
     e_neg is None and not w_neg and float(v_neg) == -0.5,
     "critical_s(alpha = -1.0) returns exactly %.4f -- a NEGATIVE critical dissipation "
     "exponent, which is meaningless for an operator |k|^{2 s_c} -- with no exception and "
     "no warning. s_c = alpha/2 is arithmetic with no domain attached." % float(v_neg))

# ------------------------------------------------------- 3: it is type-loose as well
v_str, e_str, w_str = call(critical_s, "0.8")
gate("PIN (silent): critical_s accepts a STRING argument",
     e_str is None and not w_str and float(v_str) == 0.4,
     "critical_s('0.8') returns %.4f. np.asarray(x, float) coerces, so a caller who "
     "threads an unparsed config value gets a plausible number instead of a TypeError."
     % float(v_str))

# ------------------------------------------------------ 4: control -- NaN does propagate
v_nan, e_nan, _ = call(critical_s, NAN)
v_rel, _, _ = call(relevance_exponent, NAN, 1.0)
gate("CONTROL: the closed forms DO propagate NaN",
     e_nan is None and np.isnan(float(v_nan)) and np.isnan(float(v_rel)),
     "critical_s(NaN) -> nan and relevance_exponent(NaN, 1.0) -> nan. NaN in, NaN out: "
     "these two are correct and must stay correct.")

# ------------------------------------- 5: relevance_exponent extrapolates through s < 0
v_p, e_p, w_p = call(relevance_exponent, -0.5, 1.0)
gate("PIN (silent): relevance_exponent extrapolates straight through the invalid s < 0",
     e_p is None and not w_p and float(v_p) == 2.0,
     "relevance_exponent(s = -0.5, alpha = 1.0) returns exactly %+.4f. The formula "
     "p = 1 - 2s/alpha is a line and has no idea where its domain ends, so the invalid "
     "point gets a value that sits ON the valid points' line -- which is exactly what "
     "makes the corruption downstream undetectable." % float(v_p))

# ------------------- 6: THE MASK -- the constructor now refuses BEFORE the masking line
with warnings.catch_warnings(record=True) as ws_bad:
    warnings.simplefilter("always")
    g_bad, exc_bad_ctor = None, None
    try:
        g_bad = FractionalGCLM(n=N, a=0.0, nu=NU, s=-0.5)
    except Exception as e:                               # noqa: BLE001
        exc_bad_ctor = "%s: %s" % (type(e).__name__, e)
    w_bad = [str(w.message) for w in ws_bad]
with np.errstate(all="ignore"):
    raw0 = float(np.abs(FractionalGCLM(n=N).k).astype(float)[0] ** (2.0 * -0.5))
gate("GUARD: the constructor refuses s < 0 before the masking line can overwrite the inf "
     "that says the operator is ill-defined",
     np.isinf(raw0) and g_bad is None
     and exc_bad_ctor is not None and exc_bad_ctor.startswith("ValueError")
     and not w_bad,
     "the raw k = 0 entry of |k|^{2s} at s = -0.5 is still %s -- Riesz theory's signal "
     "that a negative exponent is ill-defined exactly there, unchanged by the repair. "
     "What changed is that `self.visc[0] = 0.0` is never reached: the constructor raises "
     "%r first. No visc is built, so there is no inf left to mask and no 'divide by zero "
     "in power' warning to mistake for the whole story (warnings raised: %r)."
     % (raw0, exc_bad_ctor, w_bad))

# ------------------- 7: THE SUBSTANTIVE CORRUPTION IS NOW UNREACHABLE THROUGH THE CLASS
kmax = float(np.abs(g_ok.k).max())
with np.errstate(all="ignore"):
    would_be = np.abs(g_ok.k).astype(float) ** (2.0 * -0.5)
would_be[0] = 0.0
ratio = float(would_be[-1] / would_be[1])
gate("GUARD: the inverted multiplier is exactly as corrupt as leg 91 measured -- and can "
     "no longer be built through FractionalGCLM at all",
     np.all(np.diff(would_be[1:]) < 0.0)
     and abs(ratio - 1.0 / kmax) < 1e-12
     and exc_bad_ctor is not None and exc_bad_ctor.startswith("ValueError"),
     "constructed BY HAND from the same wavenumbers, the s = -0.5 multiplier still has "
     "visc[k_max]/visc[1] = %.6g = 1/k_max exactly (k_max = %d) and still DECREASES in "
     "|k| -- the same magnitude leg 91 banked, asserted at the same threshold, because "
     "the repair corrected no arithmetic. It closed the door instead: FractionalGCLM "
     "never builds this object, it raises %r. The sign inversion that used to emit "
     "NOTHING is now unreachable rather than unflagged." % (ratio, int(kmax), exc_bad_ctor))

# ------------------------------- 8: the whole pipeline now refuses on an invalid s
p_bad, out_bad, exc_bad, wp_bad = pipeline(-0.5)
p_bad2, out_bad2, exc_bad2, _ = pipeline(-2.0)
gate("GUARD: the full pipeline REFUSES an invalid s instead of running to completion and "
     "returning a finite, plausible-looking exponent",
     exc_bad is not None and exc_bad.startswith("ValueError") and np.isnan(p_bad)
     and exc_bad2 is not None and exc_bad2.startswith("ValueError")
     and np.isnan(p_bad2)
     and out_bad == "EXCEPTION" and out_bad2 == "EXCEPTION",
     "s = -0.5 -> ValueError, p = nan, outcome '%s'; s = -2.0 -> ValueError, p = nan, "
     "outcome '%s'. Before the repair these returned p = +2.1864 and p = +3.2481 with no "
     "exception, indistinguishable in form from the control's p = %+.4f -- and the "
     "s = -0.5 value landed within 10%% of the formula's own extrapolation (%+.2f), so a "
     "plausibility check on the VALUE could never have caught it. Refusal is the only "
     "thing that could. Message: %s" % (out_bad, out_bad2, p_ok, float(v_p), exc_bad))

# --------------- 9: THE HEADLINE -- the invalid point can no longer enter the s_c fit
clean_s = [0.15, 0.35, 0.55, 0.75]
clean_p = [pipeline(s)[0] for s in clean_s]
c0 = np.polyfit(clean_s, clean_p, 1)
zero_clean = float(-c0[1] / c0[0])
gate("GUARD: no invalid-s point can reach the p(s) fit whose zero crossing IS the "
     "measured s_c",
     np.isfinite(zero_clean) and 0.3 < zero_clean < 1.2
     and all(np.isfinite(p) for p in clean_p)
     and np.isnan(p_bad2) and exc_bad2 is not None,
     "the clean 4-point line still fits and crosses at s = %.6f with slope %+.4f, "
     "unchanged by the repair (n = %d, an audit artefact and not a physics measurement). "
     "The contamination is gone at the source: leg 91 moved this crossing by +0.080308 "
     "(+13.33%%) at s = -2.0 and by -0.000417 (-0.07%%) at s = -0.5 by injecting one "
     "silently-accepted point, and the -0.07%% shift was the disquieting one because it "
     "is invisible. There is now no p to inject -- s = -2.0 yields nan behind a "
     "ValueError -- so the contaminated fit cannot be constructed by accident at all."
     % (zero_clean, c0[0], N))

# --------------------------------------------- 10: PASS -- s = NaN propagates properly
p_snan, out_snan, exc_snan, _ = pipeline(NAN)
gate("CORRECT (regression): s = NaN propagates and the run refuses",
     exc_snan is None and np.isnan(p_snan) and out_snan == "diverged",
     "s = NaN gives outcome '%s' and p = nan. The NaN reaches the integrating factor, the "
     "state stops being finite, and the run's own `np.all(np.isfinite(w))` check breaks "
     "out. This is the module doing the right thing and must not regress." % out_snan)

# ------------------------------------- 11: PASS -- NaN/inf dissipation STRENGTH refuses
p_nunan, out_nunan, exc_nunan, _ = pipeline(0.35, nu=NAN)
p_nuinf, out_nuinf, _, _ = pipeline(0.35, nu=INF)
gate("CORRECT (regression): a NaN-poisoned or infinite dissipation strength nu refuses",
     exc_nunan is None and np.isnan(p_nunan) and out_nunan == "diverged"
     and np.isnan(p_nuinf) and out_nuinf == "diverged",
     "nu = NaN -> outcome '%s', p = nan; nu = +inf -> outcome '%s', p = nan. The gate's "
     "NaN-poisoning case is handled correctly: nothing plausible-looking comes back."
     % (out_nunan, out_nuinf))

# --------------------------------- 12: PASS -- the upper wall refuses rather than lies
s_wall = float(np.log(np.finfo(float).max) / (2.0 * np.log(kmax)))
g_hi = FractionalGCLM(n=N, a=0.0, nu=NU, s=s_wall * 0.99)
with np.errstate(over="ignore"):
    g_over = FractionalGCLM(n=N, a=0.0, nu=NU, s=s_wall * 1.5)
p_over, out_over, exc_over, _ = pipeline(s_wall * 1.5)
gate("CORRECT (regression): above the float64 wall visc goes non-finite and the pipeline "
     "refuses with nan",
     np.all(np.isfinite(g_hi.visc)) and not np.all(np.isfinite(g_over.visc))
     and exc_over is None and np.isnan(p_over),
     "the code's own upper wall at n = %d (k_max = %d) is s = %.4f: visc is finite at "
     "0.99x and non-finite at 1.5x. At 1.5x the pipeline returns p = nan with outcome "
     "'%s' -- it refuses, it does not invent. The wall is a float64 property of |k|^{2s}, "
     "measured here, not a published admissibility bound (the literature gives none)."
     % (N, int(kmax), s_wall, out_over))

# ---------------------------- 13: GUARD -- a NEGATIVE dissipation strength is refused too
p_nuneg, out_nuneg, exc_nuneg, w_nuneg = pipeline(0.35, nu=-NU)
gate("GUARD: a NEGATIVE dissipation strength nu is refused, not accepted silently",
     exc_nuneg is not None and exc_nuneg.startswith("ValueError")
     and np.isnan(p_nuneg) and out_nuneg == "EXCEPTION",
     "nu = -1e-3 -- anti-dissipation, an energy SOURCE -- now raises ValueError, p = nan, "
     "outcome '%s'. Before the repair it returned a finite p = +0.5264 against the "
     "control's +0.4948 (+6.38%%) with no exception and no warning; the control here is "
     "%+.4f. The sign of the dissipation is now checked at the same place as the sign of "
     "the exponent. Message: %s" % (out_nuneg, p_ok, exc_nuneg))

# -------------- 14: THE GUARD DID NOT OVERSHOOT -- s = 0 and nu = 0 stay admissible
exc_s0, exc_nu0, p_s0 = None, None, NAN
try:
    g_s0 = FractionalGCLM(n=N, a=0.0, nu=NU, s=0.0)
    p_s0, out_s0, _, _ = pipeline(0.0)
except Exception as e:                                   # noqa: BLE001
    exc_s0, out_s0 = "%s: %s" % (type(e).__name__, e), "EXCEPTION"
try:
    g_nu0 = FractionalGCLM(n=N, a=0.0, nu=0.0, s=1.0)
except Exception as e:                                   # noqa: BLE001
    exc_nu0 = "%s: %s" % (type(e).__name__, e)
gate("CONTROL (new with the repair): the guard did NOT overshoot -- the marginal s = 0 "
     "and the inviscid nu = 0 are admissible and still run",
     exc_s0 is None and exc_nu0 is None
     and np.all(g_s0.visc[1:] == 1.0) and g_s0.visc[0] == 0.0
     and np.all(np.isfinite(g_nu0.visc)) and out_s0 != "EXCEPTION",
     "s = 0 constructs (visc == 1 on every k != 0, mean undamped) and the pipeline "
     "returns outcome '%s' with p = %+.4f; nu = 0 constructs too. The literature's floor "
     "is sigma = 2s = 0, the 'marginal' Oldroyd-B case -- it is INSIDE the admissible "
     "range, and leg 91 carried it as a positive control after its first draft wrongly "
     "counted it as a defect. A guard that rejected s = 0 would be a regression, not a "
     "fix." % (out_s0, p_s0))


n_fail = sum(1 for s, _, _ in results if s == FAIL)
print("\n%d/%d gates pass" % (len(results) - n_fail, len(results)))
print("NOTE: gates 6, 7, 8, 9 and 13 were leg 91's silence-pins and are now INVERTED, not "
      "weakened -- every magnitude leg 91 measured is still asserted at the same "
      "threshold (the k = 0 entry is still inf, the would-be multiplier still inverts "
      "with ratio exactly 1/k_max), and only the sign of the signal claim flipped. Gates "
      "2, 3 and 5 remain GAP PINS and still pass: the repair was scoped to the operator, "
      "so the pure closed forms critical_s and relevance_exponent still have no domain "
      "attached -- a narrower hole than the one that closed, since it can no longer be "
      "reached through the solver, but still open. Gates 1, 4 and 14 are positive "
      "controls (14 checks the guard did not overshoot onto the admissible s = 0); 10-12 "
      "are ordinary regressions on behaviour the module already got right, and the guard "
      "is written so NaN/inf still propagate exactly as before. Nothing here is a "
      "statement about the VALUE of s_c, which is PRE-EMPTED (Route-J) and settled.")
sys.exit(1 if n_fail else 0)
