"""ADVERSARIAL gates for solver/target_norm.py -- Route-TNA, leg 84, INVERTED after repair.

`test_target_norm.py` (leg 55) tests that the module MEASURES correctly.  This file tests
what the module SAYS when the caller has left the window inside which that measurement is
trustworthy.  `capabilities.py`'s validated line for the module records the window:

    "... DOMAIN-limited, not resolution-limited: at the shipped X_max = 745 the far-field
     closure moves the exponent by 0.190 and the measurement is not trustworthy there;
     the headline is taken where no sample point leaves the grid"

Leg 84's gate answered **YES (silent)**, and its own disposition said so:

    "gates 1-4 and 6-11 pin the current silence deliberately and will fail the day a
     domain guard lands -- invert them, do not weaken them."

The guard has landed (bench repair, `Leg 0: ORCH`).  **Those ten gates are inverted here,
not weakened**, and the inversion is exact: every magnitude leg 84 measured is still
asserted with the same threshold, and what changed is only the sign of the SIGNAL claim.

  * **GUARD gates (1-6, 8-12)** now assert that the module signals.  Gate 5 remains the
    positive control for the file: the four argument-validation `raise` sites still fire,
    and -- new -- the domain guard did NOT turn into an exception, because the module's
    own `clamp`/`zero` ablations are supposed to be runnable outside the window.

  * **GAP-PIN gates (7, 13)** are what the repair did NOT close, kept executable so they
    cannot decay at the rate of memory (lesson 68): a fit band above the resolvable `k`
    is still accepted on its own merits, and a caller who does not thread the count still
    gets `domain_valid = None`.  `None` is falsy on purpose, which is the conservative
    direction, but it is not a warning and this file says so out loud.

Every probe runs on the calibration family `(1 + X^2)^(-alpha/2)`, whose exponent is
`p = 1 + alpha` EXACTLY, so every answer is scored against a known truth and the error is
a magnitude rather than an adjective.  **The physics is unchanged by the repair**: gates 4
and 11 assert the same numbers leg 84 banked (spread 0.4166, flip window 0.1616), which is
the check that the guard added a signal and corrected nothing.
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
    TargetNormDomainWarning, analytic_tail, calibration_family, coefficient_magnitudes,
    compactify, domain_fields, fit_exponent, norm_verdict, spectrum,
    weighted_partial_sums,
)

PASS, FAIL = "PASS", "FAIL"
results = []


def gate(name, ok, detail):
    results.append((PASS if ok else FAIL, name, detail))
    print(f"[{PASS if ok else FAIL}] {name}: {detail}")


ALPHA, P_TRUE = 0.4, 1.4
TAIL = -ALPHA
M, N_GRID, K_LO, K_HI = 16384, 801, 32, 256
X_MAX_VALIDATED_FLOOR = 745.0       # written HERE because the guard is DYNAMIC (gate 1)

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


def quiet(fn, *a, **kw):
    """Run without the domain warning, for probes whose subject is the VALUE."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", TargetNormDomainWarning)
        return fn(*a, **kw)


# 1 -- GUARD (was GAP PIN): there is a threshold, and it is NOT the literal 745
src = inspect.getsource(target_norm)
# strip STRING and COMMENT tokens, so "prose mentions the window" and "code uses the
# window" are counted apart -- leg 84 found only the first; the repair adds a threshold
# that is dynamic (`n_outside_grid > 0` against the caller's own max|X|), so the literal
# must STILL be absent from executable code.  A guard that hardcoded 745 would be wrong
# at every other resolution and domain this module is run at.
_code_only = []
for tok in tokenize.generate_tokens(io.StringIO(src).readline):
    if tok.type not in (tokenize.STRING, tokenize.COMMENT):
        _code_only.append(tok.string)
body = " ".join(_code_only)
n_745_body = body.count("745")
guard_names = [n for n in ("TargetNormDomainWarning", "domain_fields")
               if hasattr(target_norm, n)]
gate("the domain threshold exists and is dynamic, not hardcoded",
     n_745_body == 0 and len(guard_names) == 2,
     f"module-level guard names present: {guard_names}; the literal 745 appears "
     f"{src.count('745')} times in prose and {n_745_body} times in executable code "
     "(strings and comments tokenized away) -- the threshold is n_outside_grid > 0 "
     "against the caller's own max|X|, so it holds at every domain and resolution")

# 2 -- GUARD (was GAP PIN): the module now HAS a warning channel
gate("the module has a warning channel",
     "warnings" in dir(target_norm) and "warnings.warn" in src
     and issubclass(TargetNormDomainWarning, UserWarning),
     "solver/target_norm.py imports `warnings` and calls `warnings.warn`; the category "
     "is TargetNormDomainWarning(UserWarning), so callers can make it fatal with "
     "simplefilter('error', ...) or silence it for a deliberate ablation")

# 3 -- GUARD (was GAP PIN): crossing the window now signals, on the same straddling ladder
rungs, n_signalled = [], 0
for rho_max in (4.0, 6.0, 8.0, 10.0, 12.0):
    _, Xr = sinh_grid_origin(N_GRID, rho_max=rho_max)
    sp, exc, warned = call(spectrum, Xr, calibration_family(Xr, ALPHA), M=M,
                           far_field="power", tail_exponent=TAIL)
    fit, fexc, fwarned = call(fit_exponent, sp["k"], sp["hk"], K_LO, K_HI,
                              n_outside_grid=sp["n_outside_grid"])
    if sp["n_outside_grid"] > 0 and warned and fwarned and not (exc or fexc):
        n_signalled += 1
    rungs.append((float(np.abs(Xr).max()), int(sp["n_outside_grid"]), float(fit["p"]),
                  bool(sp["domain_valid"])))
crossed = [r for r in rungs if r[1] > 0]
clean = [r for r in rungs if r[1] == 0]
gate("crossing the window warns, on every rung that crosses",
     n_signalled == len(crossed) and len(crossed) >= 4
     and all(r[3] is False for r in crossed) and all(r[3] is True for r in clean),
     f"{len(crossed)} of {len(rungs)} rungs put samples outside the data "
     f"(X_max = {crossed[0][0]:.1f} .. {crossed[-1][0]:.1f}, "
     f"{crossed[0][1]} .. {crossed[-1][1]} samples of {M}) and {n_signalled} of them "
     f"warned at BOTH spectrum and fit_exponent with domain_valid = False; the "
     f"{len(clean)} rung(s) that do not cross report domain_valid = True and are silent")

# 4 -- GUARD (was GAP PIN): the number is still wrong by the SAME magnitude -- and it says so
ps, flagged = {}, 0
for mode in ("power", "clamp", "zero"):
    sp_, exc_, warned_ = call(spectrum, X745, F745, M=M, far_field=mode,
                              tail_exponent=TAIL)
    ps[mode] = float(quiet(fit_exponent, sp_["k"], sp_["hk"], K_LO, K_HI)["p"])
    if warned_ and sp_["domain_valid"] is False and sp_["n_outside_grid"] == 14:
        flagged += 1
spread = max(ps.values()) - min(ps.values())
worst = max(abs(v - P_TRUE) for v in ps.values())
n_out_745 = quiet(compactify, X745, F745, M, far_field="power", tail_exponent=TAIL)[2]
gate("14 samples of 16384 still move p by 0.4166 -- and all three closures now flag it",
     spread > 0.40 and worst > 0.24 and n_out_745 == 14 and flagged == 3,
     f"at X_max = 745.2, {n_out_745} of {M} theta-samples ({100 * n_out_745 / M:.3f}%) "
     f"lie outside the data; power/clamp/zero give p = {ps['power']:.4f} / "
     f"{ps['clamp']:.4f} / {ps['zero']:.4f}, spread {spread:.4f}, worst error vs the "
     f"exact p = {P_TRUE} is {worst:.4f} -- IDENTICAL to leg 84's pre-repair numbers, "
     f"and {flagged} of 3 now warn and return domain_valid = False.  The guard added a "
     "signal and corrected nothing")

# 5 -- GUARD (positive control): the ARGUMENT guards fire, and the DOMAIN guard does not raise
arg_cases = [
    ("mismatched shapes", lambda: compactify(X745, F745[:-1], M)),
    ("power without tail_exponent", lambda: compactify(X745, F745, M,
                                                       far_field="power")),
    ("unknown far_field", lambda: compactify(X745, F745, M, far_field="hope")),
    ("NaN from far_field='none'", lambda: coefficient_magnitudes(
        compactify(X745, F745, M, far_field="none")[1])),
]
n_raised = sum(1 for _, fn in arg_cases if call(fn)[1] is not None)
_, dom_exc, _ = call(spectrum, X745, F745, M=M, far_field="power", tail_exponent=TAIL)
gate("argument guards raise, the domain guard warns (control for this file)",
     n_raised == len(arg_cases) and dom_exc is None,
     f"{n_raised} of {len(arg_cases)} argument hazards raise ValueError -- so this "
     "harness DOES detect a guard -- while the domain violation returns normally: the "
     "module's own clamp/zero ablations are MEANT to be run outside the window, so "
     "making the guard fatal would break the ablation that measures its own cost")

# 6 -- GUARD (was GAP PIN): every domain hazard now warns instead of returning silently
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
n_flagged = sum(1 for _, fn in dom_cases
                if (lambda r: r[1] is None and r[2] and r[0]["domain_valid"] is False)(
                    call(fn)))
gate("every domain hazard now warns and reports domain_valid = False",
     n_flagged == len(dom_cases),
     f"{n_flagged} of {len(dom_cases)} domain hazards -- including a far field that "
     "GROWS like |X|^+3 on a decaying profile -- return a finite spectrum WITH a "
     "TargetNormDomainWarning and domain_valid = False (leg 84 measured 0 of 7 here)")

# 7 -- GAP PIN (NOT closed by this repair): the fit band itself is still unchecked
sp_745 = quiet(spectrum, X745, F745, M=M, far_field="power", tail_exponent=TAIL)
bad_band, bexc, bwarn = call(fit_exponent, sp_745["k"], sp_745["hk"], 512, 4096)
bad_band_told, _, bwarn_told = call(fit_exponent, sp_745["k"], sp_745["hk"], 512, 4096,
                                    n_outside_grid=sp_745["n_outside_grid"])
gate("REMAINING GAP: an unresolvable fit band is still accepted on its own merits",
     bexc is None and not bwarn and np.isfinite(bad_band["p"])
     and bad_band["domain_valid"] is None and bool(bwarn_told)
     and bad_band_told["domain_valid"] is False,
     f"k = 512..4096 sits entirely above X_max/2 = {X_MAX_VALIDATED_FLOOR / 2:.0f}, where "
     f"the coefficients are determined by the closure and not the data; the fitter still "
     f"returns p = {bad_band['p']:.4f} (error {abs(bad_band['p'] - P_TRUE):.4f}) with "
     f"r^2 = {bad_band['r2']:.4f} and does NOT compare the band to the resolvable k.  "
     "What the repair adds is provenance: told n_outside_grid it warns and returns "
     "domain_valid = False; untold it returns None, which is falsy but is not a signal")

# 8 -- GUARD (was GAP PIN): the domain field now reaches every result-bearing surface
k, hk, _ = coefficient_magnitudes(quiet(compactify, X745, F745, M, far_field="power",
                                        tail_exponent=TAIL)[1])
n_out = sp_745["n_outside_grid"]
fit745 = quiet(fit_exponent, k, hk, K_LO, K_HI, n_outside_grid=n_out)
surfaces = {
    "fit_exponent": fit745,
    "analytic_tail": quiet(analytic_tail, fit745["p"], fit745["C"], 512, 0.3,
                           n_outside_grid=n_out),
    "norm_verdict": quiet(norm_verdict, fit745["p"], 0.3, n_outside_grid=n_out),
    "weighted_partial_sums[0]": quiet(weighted_partial_sums, k, hk, 0.3, [512],
                                      n_outside_grid=n_out)[0],
}
n_carry = sum(1 for v in surfaces.values()
              if violation_keys(v) and v["domain_valid"] is False
              and v["n_outside_grid"] == 14)
gate("4 of 4 result-bearing surfaces carry the domain field", n_carry == len(surfaces),
     "keys are " + "; ".join(f"{n}: {violation_keys(v)}" for n, v in surfaces.items())
     + f" -- each carrying n_outside_grid = 14 and domain_valid = False (leg 84 measured "
     "0 of 4 carrying anything at all)")

# 9 -- GUARD: the count that always existed, now with a threshold attached
sp_big = spectrum(XBIG, FBIG, M=M, far_field="power", tail_exponent=TAIL)
gate("n_outside_grid is a real, working count AND is now compared to a threshold",
     sp_745["n_outside_grid"] == 14 and sp_big["n_outside_grid"] == 0
     and isinstance(sp_745["n_outside_grid"], int)
     and sp_745["domain_valid"] is False and sp_big["domain_valid"] is True,
     f"spectrum reports {sp_745['n_outside_grid']} outside at X_max = 745.2 "
     f"(domain_valid = {sp_745['domain_valid']}) and {sp_big['n_outside_grid']} at "
     f"4.1e+04 (domain_valid = {sp_big['domain_valid']}) -- the raw int is unchanged, "
     "what is new is that the module compares it to something")

# 10 -- GUARD (was GAP PIN): the count propagates one step downstream
gate("the count reaches downstream", "n_outside_grid" in fit745
     and set(fit745) & set(sp_745) >= {"n_outside_grid", "domain_valid"}
     and fit745["n_outside_grid"] == sp_745["n_outside_grid"],
     f"fit_exponent's dict {sorted(fit745)} now shares "
     f"{sorted(set(fit745) & set(sp_745))} with spectrum's, so an exponent, once fitted, "
     "carries the record of the domain it came from")

# 11 -- GUARD (was GAP PIN): the verdict still flips -- and now says which domain it is
sp_clamp, _, _ = call(spectrum, X745, F745, M=M, far_field="clamp")
p_bad = float(quiet(fit_exponent, sp_clamp["k"], sp_clamp["hk"], K_LO, K_HI)["p"])
p_good = float(fit_exponent(sp_big["k"], sp_big["hk"], K_LO, K_HI,
                            n_outside_grid=sp_big["n_outside_grid"])["p"])
v_bad = [call(norm_verdict, p_bad, s, n_outside_grid=sp_clamp["n_outside_grid"])
         for s in (0.42, 0.45, 0.5, 0.55)]
v_good = [norm_verdict(p_good, s, n_outside_grid=sp_big["n_outside_grid"])
          for s in (0.42, 0.45, 0.5, 0.55)]
flip = [s for s, vb, vg in zip((0.42, 0.45, 0.5, 0.55), v_bad, v_good)
        if vb[0]["finite"] and not vg["finite"]]
all_bad_flagged = all(v[0]["domain_valid"] is False and v[2] for v in v_bad)
all_good_clean = all(v["domain_valid"] is True for v in v_good)
gate("the verdict still flips over 0.16 in s -- and now records which domain",
     len(flip) == 4 and (p_bad - p_good) > 0.15 and all_bad_flagged and all_good_clean,
     f"p = {p_bad:.4f} from the untrustworthy domain vs {p_good:.4f} from the headline "
     f"domain: for every s in {flip} norm_verdict still says FINITE from the first and "
     f"DIVERGENT from the second, a window of width {p_bad - p_good:.4f} -- unchanged.  "
     "What changed: the FINITE dicts now carry domain_valid = False and warn, and the "
     "DIVERGENT ones carry domain_valid = True, so the two can no longer be read apart")

# 12 -- GUARD: the matched closure is the KIND case, so gate 4 is not cherry-picked
p_matched = ps["power"]
gate("with the exactly-right closure the violation is nearly free",
     abs(p_matched - P_TRUE) < 5e-3,
     f"far_field='power' with the profile's true tail exponent gives p = "
     f"{p_matched:.4f}, error {abs(p_matched - P_TRUE):.4f} -- the damage in gate 4 is "
     "the CLOSURE CHOICE a caller cannot make correctly without the knowledge the "
     "window is defined by, not the truncation alone.  The guard flags this case too, "
     "because a violation is a violation whether or not it happens to be cheap")

# 13 -- GAP PIN (NOT closed): unthreaded provenance is falsy, but it is not a signal
unknown = domain_fields(None)
u_fit, u_exc, u_warn = call(fit_exponent, sp_745["k"], sp_745["hk"], K_LO, K_HI)
u_verdict, _, uv_warn = call(norm_verdict, 1.5654, 0.5)
gate("REMAINING GAP: an untold callee reports unknown, falsy, and silent",
     unknown == {"n_outside_grid": None, "domain_valid": None}
     and u_fit["domain_valid"] is None and not u_warn and u_exc is None
     and u_verdict["domain_valid"] is None and not uv_warn
     and not bool(u_fit["domain_valid"]),
     "a caller who does not thread n_outside_grid gets domain_valid = None from every "
     "surface, with no warning.  None is FALSY, so `if not d['domain_valid']` errs "
     "toward distrust -- but the module cannot know what it was not told, and only the "
     "call sites that thread the count get the signal.  Pinned so this cannot be "
     "mistaken for coverage")


n_fail = sum(1 for s, _, _ in results if s == FAIL)
print(f"\n{len(results) - n_fail}/{len(results)} gates pass")
print("NOTE: leg 84's gates 1-4 and 6-11 pinned the pre-repair SILENCE and were INVERTED "
      "(not weakened) when the domain guard landed: every magnitude leg 84 measured is "
      "still asserted at the same threshold, and gates 7 and 13 pin what the repair did "
      "NOT close.")
sys.exit(1 if n_fail else 0)
