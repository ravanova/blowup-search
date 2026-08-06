"""ADVERSARIAL gates for solver/fractional_gclm.py -- Route-FGA, leg 91.

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

**Gates 2, 3, 5, 6, 7, 8, 9 and 13 PIN THAT SILENCE DELIBERATELY and will fail the day an
input guard lands in `solver/fractional_gclm.py`.  INVERT them, do not weaken them** --
keep every magnitude at the same threshold and flip only the sign of the SIGNAL claim
(the pattern leg 84 used and leg 87 followed).  Leg 91 was forbidden to patch the module
under its own authority; that is the orchestrator's call, not this file's.

Gates 1 and 4 are the positive controls.  Gates 10-12 record what the module gets RIGHT --
the report is a map of behaviour, not a bug list -- and they are ordinary regressions:
NaN and inf inputs must keep propagating, and they must not be "fixed" into silence.

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

# ---------------------------------------- 6: THE MASK -- visc[0] = 0.0 hides the inf
with warnings.catch_warnings(record=True) as ws_bad:
    warnings.simplefilter("always")
    g_bad = FractionalGCLM(n=N, a=0.0, nu=NU, s=-0.5)
    w_bad = [str(w.message) for w in ws_bad]
with np.errstate(all="ignore"):
    raw0 = float(np.abs(g_bad.k).astype(float)[0] ** (2.0 * -0.5))
gate("PIN (silent): the masking line overwrites the inf that says the operator is "
     "ill-defined",
     np.isinf(raw0) and g_bad.visc[0] == 0.0 and np.all(np.isfinite(g_bad.visc)),
     "at s = -0.5 the raw k = 0 entry of |k|^{2s} is %s, and `self.visc[0] = 0.0` on the "
     "NEXT LINE replaces it with 0.0, leaving visc entirely finite. Riesz theory puts the "
     "obstruction to a negative exponent exactly at k = 0; the line written for 'the mean "
     "is not dissipated' erases that signal as a side effect." % raw0)

# ------------------- 7: THE SUBSTANTIVE CORRUPTION, AND IT IS COMPLETELY UNFLAGGED
kmax = float(np.abs(g_bad.k).max())
ratio = float(g_bad.visc[-1] / g_bad.visc[1])
gate("PIN (silent): the surviving operator DECREASES in |k| -- a smoothing multiplier "
     "wearing the dissipation's name -- and nothing warns about it",
     np.all(np.diff(g_bad.visc[1:]) < 0.0)
     and abs(ratio - 1.0 / kmax) < 1e-12
     and all("power" in m for m in w_bad),
     "at s = -0.5, visc[k_max]/visc[1] = %.6g = 1/k_max exactly (k_max = %d): the "
     "multiplier is INVERTED relative to a fractional Laplacian, damping the largest "
     "scales hardest and leaving the small ones nearly untouched. The only warning "
     "raised is %r, which is about the k = 0 entry the next line overwrites -- the sign "
     "inversion itself emits NOTHING, and no field of any returned object records it."
     % (ratio, int(kmax), w_bad))

# --------------------------------- 8: the whole pipeline completes and returns a number
p_bad, out_bad, exc_bad, wp_bad = pipeline(-0.5)
p_bad2, out_bad2, exc_bad2, _ = pipeline(-2.0)
gate("PIN (silent): the full pipeline runs to completion on an invalid s and returns a "
     "finite, plausible-looking exponent",
     exc_bad is None and np.isfinite(p_bad) and exc_bad2 is None and np.isfinite(p_bad2)
     and out_bad not in ("EXCEPTION", "diverged"),
     "s = -0.5 -> p = %+.4f (outcome '%s'), s = -2.0 -> p = %+.4f (outcome '%s'), both "
     "with no exception. Nothing in the returned dict distinguishes these from the "
     "control's p = %+.4f. The p at s = -0.5 even lands within 10%% of the formula's own "
     "extrapolation (%+.2f), so a plausibility check on the VALUE cannot catch it either."
     % (p_bad, out_bad, p_bad2, out_bad2, p_ok, float(v_p)))

# ------------------------------------------ 9: THE HEADLINE -- the measured s_c moves
clean_s = [0.15, 0.35, 0.55, 0.75]
clean_p = [pipeline(s)[0] for s in clean_s]
c0 = np.polyfit(clean_s, clean_p, 1)
zero_clean = float(-c0[1] / c0[0])
c1 = np.polyfit(clean_s + [-2.0], clean_p + [p_bad2], 1)
zero_dirty = float(-c1[1] / c1[0])
shift = zero_dirty - zero_clean
gate("PIN (silent): one invalid-s point MOVES the measured s_c, with nothing to mark it",
     np.isfinite(zero_clean) and np.isfinite(zero_dirty) and abs(shift) > 1e-4
     and 0.3 < zero_dirty < 1.2,
     "the measured s_c is the zero crossing of the p(s) fit. Adding the single s = -2.0 "
     "point moves it %.6f -> %.6f = %+.6f (%+.2f%%) and flattens the slope %+.4f -> "
     "%+.4f. The contaminated value is finite and sits in the plausible band, so a "
     "consumer sees a normal number. (Both crossings are audit artefacts at n = %d and "
     "neither is a physics measurement; only the DIFFERENCE is claimed.)"
     % (zero_clean, zero_dirty, shift, 100.0 * shift / zero_clean, c0[0], c1[0], N))

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

# ------------------------------- 13: GAP PIN -- a NEGATIVE dissipation strength is silent
p_nuneg, out_nuneg, exc_nuneg, w_nuneg = pipeline(0.35, nu=-NU)
gate("PIN (silent): a NEGATIVE dissipation strength nu is accepted silently too",
     exc_nuneg is None and np.isfinite(p_nuneg) and not w_nuneg,
     "nu = -1e-3 -- anti-dissipation, an energy SOURCE -- gives a finite p = %+.4f "
     "against the control's %+.4f (%+.2f%%), outcome '%s', with no exception and no "
     "warning. The same gap as s < 0, on the other malformed input: the sign of the "
     "dissipation is never checked anywhere in the module."
     % (p_nuneg, p_ok, 100.0 * (p_nuneg - p_ok) / p_ok, out_nuneg))


n_fail = sum(1 for s, _, _ in results if s == FAIL)
print("\n%d/%d gates pass" % (len(results) - n_fail, len(results)))
print("NOTE: gates 2, 3, 5, 6, 7, 8, 9 and 13 PIN the module's current SILENCE on invalid "
      "dissipation input. They are expected to FAIL the day an input guard lands in "
      "solver/fractional_gclm.py -- INVERT them then, do not weaken them: keep every "
      "magnitude at the same threshold and flip only the sign of the signal claim. "
      "Gates 1 and 4 are positive controls; 10-12 are ordinary regressions on behaviour "
      "the module already gets right. Nothing here is a statement about the VALUE of "
      "s_c, which is PRE-EMPTED (Route-J) and settled.")
sys.exit(1 if n_fail else 0)
