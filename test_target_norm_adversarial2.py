"""ADVERSARIAL gates for solver/target_norm.py, AXES 2-5 -- Route-TNA2, leg 204.

WHY THIS FILE IS NOT `test_target_norm_adversarial.py`
--------------------------------------------------------------------------
That name is TAKEN: it is leg 84's suite (13 gates, inverted after the domain guard
landed), and overwriting it would delete a landed regression suite. This leg's declared
territory named it as a NEW file; the name was already in use, so this file takes the
route's own name instead. Recorded in `writeup/novelty/leg_204.md` as a deliberate,
documented deviation in the direction of destroying nothing.

WHAT IS PINNED HERE, AND WHY IT IS DELIBERATELY PINNING A DEFECT
--------------------------------------------------------------------------
Three suites already cover `solver/target_norm.py` -- leg 55 (physics), leg 84
(the DOMAIN axis, `n_outside_grid` / `domain_valid` / `TargetNormDomainWarning`), leg 94
(that guard's precision). All three look down the same axis. This file covers the four
axes none of them touched, and leg 204's gate answered **YES**: 17 of 41 adversarial and
degenerate cases return a **finite, plausible, WRONG** number with no exception, no
warning, and every diagnostic field reporting clean.

**These gates assert the CURRENT, DEFECTIVE behaviour on purpose**, exactly as leg 84's
did before its repair, and for the same reason: a defect that is not executable decays at
the rate of memory (lesson 68). Each gate below names the magnitude leg 204 measured and
the repair that would flip it.

    ** WHEN A REPAIR LANDS, THESE GATES MUST BE INVERTED, NOT WEAKENED. **

Gate 0 is the positive control and it can fail: 12 of the 41 cases DO raise, so this
harness demonstrably detects a guard where one exists. Without it, "nothing was flagged"
could mean the harness is blind.

`solver/target_norm.py` is READ-ONLY to this leg. If a gate here fails, the module has
been changed -- which is the point.

Run: `.venv/bin/python test_target_norm_adversarial2.py`
"""

import sys
import warnings

import numpy as np

sys.path.insert(0, ".")

from solver.hl_rescaled import sinh_grid_origin
from solver.target_norm import (
    TargetNormDomainWarning, X_of_theta, analytic_tail, calibration_family, domain_fields,
    fit_exponent, midpoint_theta_grid, norm_verdict, spectrum, weighted_partial_sums,
)

PASS, FAIL = "PASS", "FAIL"
results = []


def gate(name, ok, detail):
    results.append((PASS if ok else FAIL, name, detail))
    print(f"[{PASS if ok else FAIL}] {name}: {detail}")


def call(fn, *a, **kw):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            return fn(*a, **kw), None, [str(x.message) for x in w]
        except Exception as e:                                            # noqa: BLE001
            return None, f"{type(e).__name__}: {e}", [str(x.message) for x in w]


ALPHA, P_TRUE, M, N_GRID, K_LO, K_HI, S = 0.4, 1.4, 16384, 801, 32, 256, 0.3

_, X_BIG = sinh_grid_origin(N_GRID, rho_max=12.0)
F_BIG = calibration_family(X_BIG, ALPHA)
_, X_745 = sinh_grid_origin(N_GRID, rho_max=8.0)
F_745 = calibration_family(X_745, ALPHA)

SP_REF = spectrum(X_BIG, F_BIG, M=M, far_field="power", tail_exponent=-ALPHA)
K_REF, HK_REF = SP_REF["k"], SP_REF["hk"]
FIT_REF = fit_exponent(K_REF, HK_REF, K_LO, K_HI, n_outside_grid=SP_REF["n_outside_grid"])
P_REF = float(FIT_REF["p"])
SYS = abs(P_REF - P_TRUE)
BAND = np.flatnonzero((K_REF >= K_LO) & (K_REF <= K_HI))


# 0 -- POSITIVE CONTROL, and it can fail: the module DOES reject a whole class of input.
rejecting = [
    ("NaN in f", lambda: spectrum(X_BIG, np.where(np.arange(X_BIG.size) == 400, np.nan,
                                                  F_BIG), M=64, far_field="power",
                                  tail_exponent=-ALPHA)),
    ("Inf in f", lambda: spectrum(X_BIG, np.where(np.arange(X_BIG.size) == 400, np.inf,
                                                  F_BIG), M=64, far_field="power",
                                  tail_exponent=-ALPHA)),
    ("odd M", lambda: spectrum(X_BIG, F_BIG, M=17, far_field="power",
                               tail_exponent=-ALPHA)),
    ("single-point grid", lambda: spectrum(X_BIG[:1], F_BIG[:1], M=64,
                                           far_field="power", tail_exponent=-ALPHA)),
    ("empty grid", lambda: spectrum(X_BIG[:0], F_BIG[:0], M=64, far_field="power",
                                    tail_exponent=-ALPHA)),
    ("c = 0", lambda: spectrum(X_BIG, F_BIG, M=64, c=0.0, far_field="power",
                               tail_exponent=-ALPHA)),
    ("analytic_tail N = 0", lambda: analytic_tail(1.4, 0.5, 0, S)),
    ("analytic_tail N < 0", lambda: analytic_tail(1.4, 0.5, -512, S)),
]
n_raise = sum(1 for _, fn in rejecting if call(fn)[1] is not None)
gate("CONTROL: the harness detects a guard where one exists",
     n_raise == len(rejecting),
     f"{n_raise} of {len(rejecting)} hazards RAISE -- a non-finite sample anywhere in the "
     "input, an odd transform size, a degenerate grid, a zero scale, and analytic_tail's "
     "two checkpoint boundaries.  So the SILENT results below are a property of the "
     "module and not of a blind harness")


# 1 -- THE ADJACENT KEY.  spectrum returns the count AND the fraction in the same dict;
# domain_fields int()-truncates, so threading the fraction reports CLEAN.
with warnings.catch_warnings():
    warnings.simplefilter("ignore", TargetNormDomainWarning)
    sp745 = spectrum(X_745, F_745, M=M, far_field="power", tail_exponent=-ALPHA)
d_count = domain_fields(sp745["n_outside_grid"])
d_frac = domain_fields(sp745["frac_outside_grid"])
_, _, w_count = call(norm_verdict, 1.5654, 0.5, None, sp745["n_outside_grid"])
_, _, w_frac = call(norm_verdict, 1.5654, 0.5, None, sp745["frac_outside_grid"])
gate("DEFECT PINNED: frac_outside_grid, the key beside the count, reads as CLEAN",
     sp745["n_outside_grid"] == 14 and d_count["domain_valid"] is False
     and d_frac["domain_valid"] is True and d_frac["n_outside_grid"] == 0
     and len(w_count) == 1 and len(w_frac) == 0,
     f"spectrum returns n_outside_grid = {sp745['n_outside_grid']} and frac_outside_grid = "
     f"{sp745['frac_outside_grid']:.10f} in ONE dict; domain_fields gives "
     f"domain_valid = {d_count['domain_valid']} from the count and "
     f"{d_frac['domain_valid']} from the fraction, and norm_verdict warns "
     f"{len(w_count)} time(s) vs {len(w_frac)}.  A one-word slip re-silences leg 84's "
     "exact configuration.  REPAIR: reject non-integral counts instead of int()-truncating")


# 2 -- the truncation, swept: every fraction in (-1, 1), and strings, read as clean.
sweep = {repr(b): domain_fields(b) for b in (0.9, 0.5, 0.0008544921875, -0.5, -0.99, "0")}
n_clean = sum(1 for v in sweep.values() if v["domain_valid"] is True)
gate("DEFECT PINNED: domain_fields accepts str/bool/float with no type or range check",
     n_clean == len(sweep) and domain_fields("3")["n_outside_grid"] == 3
     and domain_fields(True)["n_outside_grid"] == 1,
     f"{n_clean} of {len(sweep)} type-compatible wrong values report domain_valid = True, "
     "including NEGATIVE fractions and the string '0'; the string '3' is accepted as a "
     "count of 3 and True as a count of 1.  REPAIR: require a non-negative int")


# 3 -- THE HEADLINE: the guard's window is max|X|, the data live on [X_min, X_max].
th = midpoint_theta_grid(M)
Xt = X_of_theta(th)
m = X_BIG > -10.0
Xa, Fa = X_BIG[m], F_BIG[m]
sp_a, exc_a, w_a = call(spectrum, Xa, Fa, M=M, far_field="power", tail_exponent=-ALPHA)
n_extrap = int(((Xt < Xa.min()) & (np.abs(Xt) <= np.abs(Xa).max())).sum())
fit_a = fit_exponent(sp_a["k"], sp_a["hk"], K_LO, K_HI, sp_a["n_outside_grid"])
nv_a = norm_verdict(fit_a["p"], S, n_outside_grid=sp_a["n_outside_grid"])
err_a = abs(fit_a["p"] - P_TRUE)
gate("DEFECT PINNED: an ASYMMETRIC grid extrapolates with domain_valid = True",
     n_extrap > 500 and sp_a["n_outside_grid"] == 0 and sp_a["domain_valid"] is True
     and not w_a and exc_a is None and err_a > 1.4 and fit_a["p"] < 0.0
     and nv_a["finite"] is False,
     f"data on [{Xa.min():.3f}, {Xa.max():.4g}] ({Xa.size} real points): {n_extrap} of {M} "
     f"theta-samples are polynomially EXTRAPOLATED outside the data, and the module "
     f"reports n_outside_grid = {sp_a['n_outside_grid']}, domain_valid = "
     f"{sp_a['domain_valid']}, {len(w_a)} warnings.  p = {fit_a['p']:+.6f} against the "
     f"exact {P_TRUE} -- error {err_a:.6f} = {err_a / SYS:.0f}x the systematic, the "
     f"exponent's SIGN is wrong, and norm_verdict flips to finite = {nv_a['finite']}.  "
     "compactify tests `|Xt| <= |X|.max()`, which equals the data interval only for a "
     "grid symmetric about 0.  REPAIR: test against X.min() and X.max() separately")


# 4 -- the guard is exactly right on the symmetric grid, so gate 3 is about ASYMMETRY and
# not about truncation in general.  This control can fail.
sp_sym, _, w_sym = call(spectrum, X_BIG, F_BIG, M=M, far_field="power",
                        tail_exponent=-ALPHA)
sp_short, _, w_short = call(spectrum, X_745, F_745, M=M, far_field="power",
                            tail_exponent=-ALPHA)
gate("CONTROL: on SYMMETRIC grids the guard is exactly right, both ways",
     sp_sym["n_outside_grid"] == 0 and sp_sym["domain_valid"] is True and not w_sym
     and sp_short["n_outside_grid"] == 14 and sp_short["domain_valid"] is False
     and len(w_short) == 1,
     f"symmetric and wide: {sp_sym['n_outside_grid']} outside, silent; symmetric and "
     f"short: {sp_short['n_outside_grid']} outside, {len(w_short)} warning.  So gate 3 "
     "isolates the ASYMMETRY, not truncation -- leg 84's finding is untouched")


# 5 -- NaN in hk is dropped from the fit, and n_points still reports the full band.
lad = []
for nn in (20, 80, 150):
    h2 = HK_REF.copy()
    h2[BAND[:nn]] = np.nan
    r, e, w = call(fit_exponent, K_REF, h2, K_LO, K_HI, 0)
    lad.append((nn, r["n_points"], BAND.size - nn, r["n_bins"], float(r["p"]), len(w),
                r["domain_valid"]))
gate("DEFECT PINNED: NaN coefficients are silently dropped, n_points overstates by 3x",
     all(n_rep == BAND.size and nb < FIT_REF["n_bins"] and np.isfinite(p)
         and nw == 0 and dv is True for _, n_rep, _, nb, p, nw, dv in lad)
     and lad[-1][1] / lad[-1][2] == 3.0,
     "; ".join(f"{nn} NaN -> n_points {rep} (only {true} finite), n_bins {nb}, "
               f"p {p:.6f}, {nw} warnings" for nn, rep, true, nb, p, nw, _ in lad)
     + f" -- at 150 of {BAND.size} the reported n_points overstates the modes actually "
     f"used by {lad[-1][1] / lad[-1][2]:.1f}x while p stays within "
     f"{abs(lad[-1][4] - P_TRUE):.6f} of exact, so nothing in the output looks wrong.  "
     "REPAIR: gate hk for finiteness, or report the count actually binned")


# 6 -- a NEGATIVE |h_k| is absorbed and MISLABELLED as a zero mode.
h_neg = HK_REF.copy()
h_neg[BAND[:50]] = -1e3
r_neg, _, w_neg = call(fit_exponent, K_REF, h_neg, K_LO, K_HI, 0)
gate("DEFECT PINNED: negative coefficient magnitudes are counted as ZERO modes",
     abs(r_neg["p"] - P_REF) < 1e-3 and not w_neg
     and abs(r_neg["frac_zero_modes"] - 50.0 / BAND.size) < 1e-9,
     f"50 of {BAND.size} |h_k| set to -1000 -- impossible for a magnitude -- gives "
     f"p = {r_neg['p']:.6f} against the clean {P_REF:.6f}, a difference of "
     f"{abs(r_neg['p'] - P_REF):.2e}, with {len(w_neg)} warnings.  The only trace is "
     f"frac_zero_modes = {r_neg['frac_zero_modes']:.4f}, whose `hh <= 0.0` test conflates "
     "'annihilated by a symmetry' (why the field exists) with 'negative' (impossible).  "
     "REPAIR: separate the two counts")


# 7 -- analytic_tail gates `margin` and nothing else.
t_nan = analytic_tail(1.4, float("nan"), 512, S, 0)
t_inf = analytic_tail(1.4, float("inf"), 512, S, 0)
t_neg = analytic_tail(1.4, -0.5, 512, S, 0)
t_pos = analytic_tail(1.4, +0.5, 512, S, 0)
t_Nn = analytic_tail(1.4, 0.5, float("nan"), S, 0)
gate("DEFECT PINNED: analytic_tail validates margin only -- C and N pass straight through",
     t_nan["finite"] and not np.isfinite(t_nan["bound"]) and t_nan["reason"] is None
     and t_inf["finite"] and np.isinf(t_inf["bound"])
     and t_neg["finite"] and t_neg["bound"] < 0
     and abs(t_neg["bound"] + t_pos["bound"]) < 1e-12
     and t_Nn["finite"] and not np.isfinite(t_Nn["bound"]),
     f"C = NaN -> finite = True, bound = {t_nan['bound']}, reason = {t_nan['reason']!r}; "
     f"C = Inf -> bound = {t_inf['bound']}; C = -0.5 -> bound = {t_neg['bound']:.6f}, a "
     f"NEGATIVE upper bound on a sum of non-negative terms (the same |C| gives "
     f"{t_pos['bound']:.6f}); N = NaN -> bound = {t_Nn['bound']}.  Only `margin` is gated. "
     "REPAIR: require C >= 0 and N > 0 finite, or set finite = False with a reason")


# 8 -- analytic_tail's ONE gated parameter is gated correctly (control, can fail).
t_edge = analytic_tail(1.0 + S, 0.5, 512, S, 0)
gate("CONTROL: the one parameter analytic_tail DOES gate, it gates correctly",
     t_edge["finite"] is False and t_edge["bound"] is None
     and t_edge["margin"] == 0.0 and "diverges" in t_edge["reason"],
     f"exactly at the threshold, margin = {t_edge['margin']:.1f}, finite = "
     f"{t_edge['finite']}, bound = {t_edge['bound']}, reason = {t_edge['reason']!r} -- it "
     "refuses to bound a divergent sum and says why (lesson 73) instead of returning a "
     "large number.  So gate 7 is about the UNGATED parameters specifically")


# 9 -- descending k silently destroys, then inflates, the norm.
S_ok = weighted_partial_sums(K_REF, HK_REF, S, [64, 4096], 0)
S_rev = weighted_partial_sums(K_REF[::-1], HK_REF, S, [64, 4096], 0)
ratio = S_rev[1]["S_N"] / S_ok[1]["S_N"]
gate("DEFECT PINNED: descending k gives S_64 = 0 and S_4096 inflated 6.9x",
     S_rev[0]["S_N"] == 0.0 and S_ok[0]["S_N"] > 1.0 and ratio > 6.0
     and S_rev[0]["domain_valid"] is True,
     f"true S_64 = {S_ok[0]['S_N']:.6f} but reversed k reports EXACTLY "
     f"{S_rev[0]['S_N']:.1f}; true S_4096 = {S_ok[1]['S_N']:.6f} but reversed reports "
     f"{S_rev[1]['S_N']:.6f}, an overstatement of {ratio:.2f}x -- a norm wrong in both "
     "directions, with domain_valid = True.  np.searchsorted assumes ascending and "
     "nothing checks.  REPAIR: assert k is sorted")


# 10 -- CONTROL, and it can fail: a DESCENDING X grid is handled exactly right.
sp_d, _, _ = call(spectrum, X_BIG[::-1], F_BIG[::-1], M=M, far_field="power",
                  tail_exponent=-ALPHA)
p_d = float(fit_exponent(sp_d["k"], sp_d["hk"], K_LO, K_HI, sp_d["n_outside_grid"])["p"])
gate("CONTROL: a descending X grid IS handled correctly (lesson 90)",
     abs(p_d - P_REF) < 1e-12,
     f"p = {p_d:.6f} vs the ascending reference {P_REF:.6f}, difference "
     f"{abs(p_d - P_REF):.2e} -- the rho mapping is sign-consistent.  This control could "
     "have come out differently, and it is what makes gate 9 a statement about "
     "searchsorted rather than 'the module is fragile to any reordering'")


# 11 -- a shuffled X/f pairing destroys the measurement with every flag clean.
rng = np.random.RandomState(0)
perm = rng.permutation(X_BIG.size)
sp_s, _, w_s = call(spectrum, X_BIG[perm], F_BIG[perm], M=M, far_field="power",
                    tail_exponent=-ALPHA)
p_s = float(fit_exponent(sp_s["k"], sp_s["hk"], K_LO, K_HI, sp_s["n_outside_grid"])["p"])
gate("DEFECT PINNED: a non-monotone X/f pairing returns p ~ 0 with every flag clean",
     abs(p_s - P_TRUE) > 1.39 and sp_s["n_outside_grid"] == 0
     and sp_s["domain_valid"] is True and not w_s,
     f"p = {p_s:.6e} against the exact {P_TRUE}, an error of {abs(p_s - P_TRUE):.6f} "
     f"({100 * abs(p_s - P_TRUE) / P_TRUE:.3f}% of the true exponent), with "
     f"n_outside_grid = {sp_s['n_outside_grid']}, domain_valid = {sp_s['domain_valid']}, "
     f"{len(w_s)} warnings.  lagrange_interp_uniform indexes by POSITION and assumes "
     "uniformity in rho; nothing checks that arcsinh(X/c) is monotone or evenly spaced.  "
     "REPAIR: check monotonicity and spacing once, in compactify")


# 12 -- a mismatched sinh scale c biases the exponent by up to 360x the systematic.
cs = {}
for cc in (1e-8, 1e8):
    sp_c, _, w_c = call(spectrum, X_BIG, F_BIG, M=M, c=cc, far_field="power",
                        tail_exponent=-ALPHA)
    p_c = float(fit_exponent(sp_c["k"], sp_c["hk"], K_LO, K_HI,
                             sp_c["n_outside_grid"])["p"])
    cs[cc] = (p_c, abs(p_c - P_TRUE), sp_c["domain_valid"], len(w_c),
              norm_verdict(p_c, S, n_outside_grid=sp_c["n_outside_grid"])["finite"])
gate("DEFECT PINNED: a mismatched sinh scale c flips the verdict, silently",
     all(v[1] / SYS > 100 and v[2] is True and v[3] == 0 and v[4] is False
         for v in cs.values()),
     "; ".join(f"c = {c:g} -> p = {v[0]:.6f}, err {v[1]:.6f} = {v[1] / SYS:.0f}x the "
               f"systematic, domain_valid = {v[2]}, {v[3]} warnings, finite = {v[4]}"
               for c, v in cs.items())
     + f" -- against the correct c = 0.5 giving p = {P_REF:.6f} and finite = True.  "
     "Nothing compares c to the grid it was handed.  REPAIR: check that arcsinh(X/c) is "
     "evenly spaced, which is the assumption c encodes")


# 13 -- a zero-norm profile is reported DIVERGENT.
sp_z, _, w_z = call(spectrum, X_BIG, np.zeros_like(X_BIG), M=M, far_field="power",
                    tail_exponent=-ALPHA)
fit_z = fit_exponent(sp_z["k"], sp_z["hk"], K_LO, K_HI, 0)
S_z = weighted_partial_sums(sp_z["k"], sp_z["hk"], S, [4096], 0)[0]
nv_z = norm_verdict(fit_z["p"], S, n_outside_grid=0)
gate("DEFECT PINNED: a profile of norm EXACTLY ZERO is reported DIVERGENT",
     S_z["S_N"] == 0.0 and not np.isfinite(fit_z["p"]) and nv_z["finite"] is False
     and not w_z and nv_z["domain_valid"] is True,
     f"the identically-zero profile has ||.||_w = {S_z['S_N']:.1f} over k >= 1 -- finite, "
     f"and trivially IN the space -- yet fit_exponent returns p = {fit_z['p']} (every bin "
     f"fails the mean>0 test) and norm_verdict returns finite = {nv_z['finite']} with "
     f"{len(w_z)} warnings and domain_valid = True.  The error is in the CONSERVATIVE "
     "direction, but 'the target is not in the space' is still the wrong answer.  "
     "REPAIR: distinguish 'no power law to fit' from 'diverges'")


# 14 -- M = 2 returns an empty spectrum as a normal result.
sp_2, exc_2, w_2 = call(spectrum, X_BIG, F_BIG, M=2, far_field="power",
                        tail_exponent=-ALPHA)
gate("DEFECT PINNED: M = 2 returns an EMPTY spectrum as a normal result",
     exc_2 is None and sp_2["k"].size == 0 and not w_2,
     f"kmax = M//2 - 1 = 0, so spectrum returns {sp_2['k'].size} resolved modes with no "
     f"exception and {len(w_2)} warnings; the failure only surfaces one function later, "
     "as a NaN exponent.  REPAIR: require M >= 8 (or whatever the band needs)")


n_fail = sum(1 for s, _, _ in results if s == FAIL)
print(f"\n{len(results) - n_fail}/{len(results)} gates pass")
print("NOTE: gates 1-3, 5-7, 9, 11-14 PIN DEFECTS leg 204 measured (17 of 41 adversarial "
      "cases return a finite, plausible, WRONG number with every flag clean).  They will "
      "FAIL the day a repair lands.  INVERT THEM, DO NOT WEAKEN THEM -- and keep the "
      "magnitude each one asserts.  Gates 0, 4, 8, 10 are controls that can fail.")
sys.exit(1 if n_fail else 0)
