"""ADVERSARIAL gates for solver/target_norm.py -- Route-TNA, leg 84.

`test_target_norm.py` (leg 55) tests that the module MEASURES correctly.  This file tests
what the module SAYS when the caller has left the window inside which that measurement is
trustworthy.  `capabilities.py`'s validated line for the module records the window:

    "... DOMAIN-limited, not resolution-limited: at the shipped X_max = 745 the far-field
     closure moves the exponent by 0.190 and the measurement is not trustworthy there;
     the headline is taken where no sample point leaves the grid"

Leg 84's gate answered **YES (silent)**: nothing in the module compares anything to that
window.  So the gates below are of two kinds, and the difference is load-bearing.

  * **GUARD gates (5, 12)** assert behaviour that EXISTS and must not regress: the four
    argument-validation `raise` sites, and the one diagnostic the module does return
    (`n_outside_grid`).  Gate 5 is also the positive control for this whole file -- it
    proves the harness can detect a guard when there is one, so the silence the other
    gates report is a property of the module and not of the test.

  * **GAP-PIN gates (1-4, 6-11)** assert the CURRENT SILENCE, with magnitudes.  They are
    not an endorsement.  Leg 84 was forbidden to patch the module and did not touch it;
    these gates exist so the gap cannot quietly widen, and so that the moment somebody
    adds a real domain guard THIS FILE FAILS LOUDLY and has to be inverted on purpose.
    A gap that is not executable decays at the rate of memory (lesson 68); a gap that is
    pinned announces its own repair.

Every probe runs on the calibration family `(1 + X^2)^(-alpha/2)`, whose exponent is
`p = 1 + alpha` EXACTLY, so every silent answer is scored against a known truth and the
error is a magnitude rather than an adjective.
"""

import inspect
import io
import sys
import tokenize
import warnings

import numpy as np

sys.path.insert(0, ".")

from solver import target_norm
from solver.hl_rescaled import sinh_grid_origin
from solver.target_norm import (
    analytic_tail, calibration_family, coefficient_magnitudes, compactify, fit_exponent,
    norm_verdict, spectrum, weighted_partial_sums,
)

PASS, FAIL = "PASS", "FAIL"
results = []


def gate(name, ok, detail):
    results.append((PASS if ok else FAIL, name, detail))
    print(f"[{PASS if ok else FAIL}] {name}: {detail}")


ALPHA, P_TRUE = 0.4, 1.4
TAIL = -ALPHA
M, N_GRID, K_LO, K_HI = 16384, 801, 32, 256
X_MAX_VALIDATED_FLOOR = 745.0       # written HERE because the module has no such constant

_, X745 = sinh_grid_origin(N_GRID, rho_max=8.0)      # X_max = 745.2, the shipped domain
_, XBIG = sinh_grid_origin(N_GRID, rho_max=12.0)     # X_max = 4.07e+04, the headline
F745, FBIG = calibration_family(X745, ALPHA), calibration_family(XBIG, ALPHA)

VIOLATION_STEMS = ("outside", "domain", "trust", "valid", "warn", "flag", "extrapol",
                   "x_max", "xmax", "window", "clip", "guard")


def violation_keys(obj):
    if not isinstance(obj, dict):
        return []
    return sorted(k for k in obj if any(s in k.lower() for s in VIOLATION_STEMS))


def call(fn, *a, **kw):
    """(value, exception_repr_or_None, [warning messages])."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            return fn(*a, **kw), None, [str(x.message) for x in w]
        except Exception as e:                                   # noqa: BLE001
            return None, f"{type(e).__name__}: {e}", [str(x.message) for x in w]


# 1 -- GAP PIN: the validated window is not a constant anywhere in the module
src = inspect.getsource(target_norm)
# strip STRING and COMMENT tokens, so "prose mentions the window" and "code uses the
# window" are counted apart -- the whole point of gate 1 is that only the first happens
_code_only = []
for tok in tokenize.generate_tokens(io.StringIO(src).readline):
    if tok.type not in (tokenize.STRING, tokenize.COMMENT):
        _code_only.append(tok.string)
body = " ".join(_code_only)
n_745_body = body.count("745")
consts = [n for n in dir(target_norm)
          if n.isupper() or any(s in n.lower() for s in VIOLATION_STEMS)]
gate("no validated-domain constant in the module", n_745_body == 0 and consts == [],
     f"the literal 745 appears {src.count('745')} times in the module's prose and "
     f"{n_745_body} times in executable code (strings and comments tokenized away); "
     f"module-level names matching a "
     f"domain/validity stem: {consts}")

# 2 -- GAP PIN: no warning module is even imported
gate("the module has no warning channel", "warnings" not in dir(target_norm)
     and "warnings.warn" not in src,
     "solver/target_norm.py imports no `warnings` and calls `warnings.warn` 0 times "
     "(0 of 43 solver modules do -- this is the repo idiom, not a deviation)")

# 3 -- GAP PIN: crossing the window emits nothing, on a ladder that straddles it
rungs, n_signalled = [], 0
for rho_max in (4.0, 6.0, 8.0, 10.0, 12.0):
    _, Xr = sinh_grid_origin(N_GRID, rho_max=rho_max)
    sp, exc, warned = call(spectrum, Xr, calibration_family(Xr, ALPHA), M=M,
                           far_field="power", tail_exponent=TAIL)
    fit, fexc, fwarned = call(fit_exponent, sp["k"], sp["hk"], K_LO, K_HI)
    if exc or warned or fexc or fwarned:
        n_signalled += 1
    rungs.append((float(np.abs(Xr).max()), int(sp["n_outside_grid"]), float(fit["p"])))
crossed = [r for r in rungs if r[1] > 0]
gate("crossing the window is silent", n_signalled == 0 and len(crossed) >= 4,
     f"{len(crossed)} of {len(rungs)} rungs put samples outside the data "
     f"(X_max = {crossed[0][0]:.1f} .. {crossed[-1][0]:.1f}, "
     f"{crossed[0][1]} .. {crossed[-1][1]} samples of {M}) and {n_signalled} of them "
     "raised or warned")

# 4 -- GAP PIN: and the number it hands back is wrong, by a MAGNITUDE
ps = {}
for mode in ("power", "clamp", "zero"):
    sp_ = spectrum(X745, F745, M=M, far_field=mode, tail_exponent=TAIL)
    ps[mode] = float(fit_exponent(sp_["k"], sp_["hk"], K_LO, K_HI)["p"])
spread = max(ps.values()) - min(ps.values())
worst = max(abs(v - P_TRUE) for v in ps.values())
n_out_745 = compactify(X745, F745, M, far_field="power", tail_exponent=TAIL)[2]
gate("14 samples of 16384 move p by 0.4166", spread > 0.40 and worst > 0.24
     and n_out_745 == 14,
     f"at X_max = 745.2, {n_out_745} of {M} theta-samples ({100 * n_out_745 / M:.3f}%) "
     f"lie outside the data; power/clamp/zero give p = {ps['power']:.4f} / "
     f"{ps['clamp']:.4f} / {ps['zero']:.4f}, spread {spread:.4f}, worst error vs the "
     f"exact p = {P_TRUE} is {worst:.4f}")

# 5 -- GUARD (positive control): the four ARGUMENT guards do fire
arg_cases = [
    ("mismatched shapes", lambda: compactify(X745, F745[:-1], M)),
    ("power without tail_exponent", lambda: compactify(X745, F745, M,
                                                       far_field="power")),
    ("unknown far_field", lambda: compactify(X745, F745, M, far_field="hope")),
    ("NaN from far_field='none'", lambda: coefficient_magnitudes(
        compactify(X745, F745, M, far_field="none")[1])),
]
n_raised = sum(1 for _, fn in arg_cases if call(fn)[1] is not None)
gate("argument guards fire (control for this file)", n_raised == len(arg_cases),
     f"{n_raised} of {len(arg_cases)} argument hazards raise ValueError -- so this "
     "harness DOES detect a guard, and the silence gates 3-4 report is the module's")

# 6 -- GAP PIN: the domain hazards, by contrast, all return a number
dom_cases = [
    ("X_max = 13.6, 55x short", lambda: spectrum(
        *(lambda X: (X, calibration_family(X, ALPHA)))(
            sinh_grid_origin(N_GRID, rho_max=4.0)[1]),
        M=M, far_field="power", tail_exponent=TAIL)),
    ("shipped 745, called untrustworthy", lambda: spectrum(
        X745, F745, M=M, far_field="power", tail_exponent=TAIL)),
    ("clamp closure at 745", lambda: spectrum(X745, F745, M=M, far_field="clamp")),
    ("zero closure at 745", lambda: spectrum(X745, F745, M=M, far_field="zero")),
    ("GROWING far field, tail = +3", lambda: spectrum(
        X745, F745, M=M, far_field="power", tail_exponent=+3.0)),
    ("tail = -5 against alpha = 0.4 data", lambda: spectrum(
        X745, F745, M=M, far_field="power", tail_exponent=-5.0)),
    ("M = 65536: 4x more samples outside", lambda: spectrum(
        X745, F745, M=65536, far_field="power", tail_exponent=TAIL)),
]
n_silent = sum(1 for _, fn in dom_cases
               if (lambda r: r[1] is None and not r[2])(call(fn)))
gate("every domain hazard returns a number", n_silent == len(dom_cases),
     f"{n_silent} of {len(dom_cases)} domain hazards -- including a far field that GROWS "
     "like |X|^+3 on a decaying profile -- return a finite spectrum with no exception "
     "and no warning")

# 7 -- GAP PIN: a fit band entirely above the resolvable k is accepted
sp_745 = spectrum(X745, F745, M=M, far_field="power", tail_exponent=TAIL)
bad_band, bexc, bwarn = call(fit_exponent, sp_745["k"], sp_745["hk"], 512, 4096)
gate("unresolvable fit band accepted silently", bexc is None and not bwarn
     and np.isfinite(bad_band["p"]),
     f"k = 512..4096 sits entirely above X_max/2 = {X_MAX_VALIDATED_FLOOR / 2:.0f}, where "
     f"the coefficients are determined by the closure and not the data; the fitter "
     f"returns p = {bad_band['p']:.4f} (error {abs(bad_band['p'] - P_TRUE):.4f}) with "
     f"r^2 = {bad_band['r2']:.4f}")

# 8 -- GAP PIN: nothing domain-shaped reaches the exponent- and norm-bearing surfaces
k, hk, _ = coefficient_magnitudes(compactify(X745, F745, M, far_field="power",
                                             tail_exponent=TAIL)[1])
fit745 = fit_exponent(k, hk, K_LO, K_HI)
surfaces = {"fit_exponent": fit745,
            "analytic_tail": analytic_tail(fit745["p"], fit745["C"], 512, 0.3),
            "norm_verdict": norm_verdict(fit745["p"], 0.3),
            "weighted_partial_sums[0]": weighted_partial_sums(k, hk, 0.3, [512])[0]}
n_carry = sum(1 for v in surfaces.values() if violation_keys(v))
gate("0 of 4 result-bearing surfaces carry a domain field", n_carry == 0,
     "keys are " + "; ".join(f"{n}: {sorted(v.keys())}" for n, v in surfaces.items())
     + " -- none matches any of " + ", ".join(VIOLATION_STEMS))

# 9 -- GUARD: the ONE diagnostic that does exist, and its limit
sp_big = spectrum(XBIG, FBIG, M=M, far_field="power", tail_exponent=TAIL)
gate("n_outside_grid is a real, working count", sp_745["n_outside_grid"] == 14
     and sp_big["n_outside_grid"] == 0
     and isinstance(sp_745["n_outside_grid"], int),
     f"spectrum reports {sp_745['n_outside_grid']} outside at X_max = 745.2 and "
     f"{sp_big['n_outside_grid']} at 4.1e+04 -- a raw int the caller must know to read, "
     "compared by the module against no threshold")

# 10 -- GAP PIN: the count does not propagate one step downstream
gate("the count reaches nothing downstream", "n_outside_grid" not in fit745
     and set(fit745) & set(sp_745) == set(),
     f"fit_exponent's dict {sorted(fit745)} shares 0 keys with spectrum's "
     f"{sorted(sp_745)}, so an exponent, once fitted, carries no record of the domain "
     "it came from")

# 11 -- GAP PIN: and that costs a FINITE-vs-DIVERGENT verdict over a window in s
sp_clamp = spectrum(X745, F745, M=M, far_field="clamp")
p_bad = float(fit_exponent(sp_clamp["k"], sp_clamp["hk"], K_LO, K_HI)["p"])
p_good = float(fit_exponent(sp_big["k"], sp_big["hk"], K_LO, K_HI)["p"])
flip = [s for s in (0.42, 0.45, 0.5, 0.55)
        if norm_verdict(p_bad, s)["finite"] and not norm_verdict(p_good, s)["finite"]]
gate("verdict flips over a window of width 0.16 in s", len(flip) == 4
     and (p_bad - p_good) > 0.15,
     f"p = {p_bad:.4f} from the untrustworthy domain vs {p_good:.4f} from the headline "
     f"domain: for every s in {flip} norm_verdict says FINITE from the first and "
     f"DIVERGENT from the second, a window of width {p_bad - p_good:.4f}, and the "
     "returned dict says nothing about which domain produced p")

# 12 -- GUARD: the matched closure is the KIND case, so gate 4 is not cherry-picked
p_matched = ps["power"]
gate("with the exactly-right closure the violation is nearly free",
     abs(p_matched - P_TRUE) < 5e-3,
     f"far_field='power' with the profile's true tail exponent gives p = "
     f"{p_matched:.4f}, error {abs(p_matched - P_TRUE):.4f} -- the damage in gate 4 is "
     "the CLOSURE CHOICE a caller cannot make correctly without the knowledge the "
     "window is defined by, not the truncation alone")


n_fail = sum(1 for s, _, _ in results if s == FAIL)
print(f"\n{len(results) - n_fail}/{len(results)} gates pass")
print("NOTE: gates 1-4 and 6-11 PIN A KNOWN GAP (leg 84, gate answered YES/silent). "
      "If a domain guard is ever added to solver/target_norm.py they SHOULD fail, and "
      "the correct response is to invert them, not to weaken them.")
sys.exit(1 if n_fail else 0)
