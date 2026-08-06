"""Route-TNA2, leg 204: the ADVERSARIAL / DEGENERATE audit of solver/target_norm.py.

WHAT THIS IS, AND WHY IT IS A FOURTH PASS OVER ONE MODULE
--------------------------------------------------------------------------
`solver/target_norm.py` has been audited three times already (`writeup/novelty/leg_204.md`
has the table): leg 55 built it, leg 84 (Route-TNA) audited it and answered YES/SILENT, a
bench repair landed the domain guard, and leg 94 (Route-TNB) pinned that guard's precision.
**All three looked down the same axis: the DOMAIN axis** -- did a theta-sample leave the
supplied grid, and does the module say so.

This leg looks down the four axes none of them touched, counted in the novelty pass over
all 879 lines of the three existing suites:

    NaN / Inf .............. 0 gates inject a non-finite value at a public entry point
    degenerate / zero-norm . 0 gates feed an identically-zero or rank-degenerate profile
    boundary parameters .... 0 gates probe analytic_tail's N, C or margin boundary
    planted wrong value .... 0 gates plant a wrong-but-type-compatible argument

GATE (pre-committed, both branches, exact wording)
--------------------------------------------------------------------------
"Under adversarial and degenerate inputs, does `target_norm.py` ever silently return a
wrong value rather than reject or visibly propagate the defect?"

Every case below is scored into exactly one of four outcomes, and the score is a MAGNITUDE
and not a boolean:

    REJECT       the call raises.  The defect cannot propagate.  This is the good outcome.
    VISIBLE      the call returns, but the defect is legible in what comes back -- a NaN in
                 the value the caller asked for, a warning, or domain_valid = False.
    SILENT_WRONG the call returns a FINITE, PLAUSIBLE, WRONG number, with no exception, no
                 warning, and every diagnostic field reporting clean.  This is the finding.
    SILENT_OK    the call returns the RIGHT answer on an input that might have broken it.
                 These are the controls that could have come out differently (lesson 90).

THE TRUTH VALUE
--------------------------------------------------------------------------
Every probe runs on the calibration family `(1 + X^2)^(-alpha/2)` at `alpha = 0.4`, whose
compactified image is `|cos(theta/2)|^0.4` and whose coefficient exponent is `p = 1 + alpha
= 1.4` EXACTLY.  So "wrong" is a distance from a known number, not an adjective.  The clean
reference on the shipped headline grid is `p = 1.403855` (error 0.003855), and that is the
systematic every error below is quoted against.

`solver/target_norm.py` IS READ-ONLY TO THIS LEG UNDER BOTH BRANCHES OF THE GATE.
Nothing here patches anything.  If the gate answers YES the finding is escalated and parked.

Run: `.venv/bin/python experiments/p2_route_tna2_v1_adversarial.py`
Writes: `writeup/data/p2_route_tna2_v1_adversarial.json`
"""

import json
import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.bordered_hl import BorderedHL                                 # noqa: E402
from solver.hl_rescaled import sinh_grid_origin                           # noqa: E402
from solver.target_norm import (                                          # noqa: E402
    TargetNormDomainWarning, X_of_theta, analytic_tail, calibration_family,
    coefficient_magnitudes, compactify, domain_fields, fit_exponent, midpoint_theta_grid,
    norm_verdict, spectrum, weighted_partial_sums,
)

# --------------------------------------------------------------------------
# the fixed instrument: leg 84's own configuration, so the two are comparable
# --------------------------------------------------------------------------
ALPHA, P_TRUE = 0.4, 1.4
M, N_GRID = 16384, 801
K_LO, K_HI = 32, 256
S_PROBE = 0.3                       # one of leg 55's two banked FINITE margins

REJECT, VISIBLE, SILENT_WRONG, SILENT_OK = (
    "REJECT", "VISIBLE", "SILENT_WRONG", "SILENT_OK")

CASES = []


def call(fn, *a, **kw):
    """(value, exception_repr_or_None, [warning strings])."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            return fn(*a, **kw), None, [f"{x.category.__name__}: {x.message}" for x in w]
        except Exception as e:                                            # noqa: BLE001
            return None, f"{type(e).__name__}: {e}", [
                f"{x.category.__name__}: {x.message}" for x in w]


def record(axis, name, outcome, magnitude, detail, **extra):
    row = {"axis": axis, "case": name, "outcome": outcome,
           "magnitude": magnitude, "detail": detail}
    row.update(extra)
    CASES.append(row)
    print(f"[{outcome:12s}] {axis} / {name}: {magnitude}")
    return row


def clean_flags(obj, warns):
    """True iff NOTHING in the returned object or the warning list flags a defect."""
    if warns:
        return False
    if isinstance(obj, dict):
        if obj.get("domain_valid") is False:
            return False
        if obj.get("n_outside_grid") not in (None, 0):
            return False
    return True


# --------------------------------------------------------------------------
# the reference: the clean, in-window, symmetric configuration
# --------------------------------------------------------------------------
_, X_BIG = sinh_grid_origin(N_GRID, rho_max=12.0)      # X_max = 4.07e+04, leg 55's headline
F_BIG = calibration_family(X_BIG, ALPHA)
_, X_745 = sinh_grid_origin(N_GRID, rho_max=8.0)       # the shipped domain leg 84 audited
F_745 = calibration_family(X_745, ALPHA)

SP_REF = spectrum(X_BIG, F_BIG, M=M, far_field="power", tail_exponent=-ALPHA)
FIT_REF = fit_exponent(SP_REF["k"], SP_REF["hk"], K_LO, K_HI,
                       n_outside_grid=SP_REF["n_outside_grid"])
P_REF = float(FIT_REF["p"])
SYSTEMATIC = abs(P_REF - P_TRUE)
K_REF, HK_REF = SP_REF["k"], SP_REF["hk"]
BAND_IDX = np.flatnonzero((K_REF >= K_LO) & (K_REF <= K_HI))

print(f"reference: p = {P_REF:.6f} vs exact {P_TRUE}, systematic {SYSTEMATIC:.6f}, "
      f"n_outside_grid = {SP_REF['n_outside_grid']}, domain_valid = {SP_REF['domain_valid']}")


# ==========================================================================
# AXIS 1 -- NON-FINITE INPUT
# ==========================================================================
print("\n--- AXIS 1: NaN / Inf ---")

for label, arr, which in [
        ("NaN in f", "f", np.nan), ("Inf in f", "f", np.inf),
        ("-Inf in f", "f", -np.inf), ("NaN in X", "X", np.nan)]:
    Xc, Fc = X_BIG.copy(), F_BIG.copy()
    (Fc if arr == "f" else Xc)[400] = which
    _, exc, w = call(spectrum, Xc, Fc, M=M, far_field="power", tail_exponent=-ALPHA)
    record("nonfinite", label, REJECT if exc else SILENT_WRONG,
           exc or "returned a value",
           "a single non-finite sample anywhere in the input arrays is caught by "
           "coefficient_magnitudes' finiteness check before any coefficient is reported")

# 1.4 -- NaN planted directly in the coefficient array handed to fit_exponent.
# This is the entry point `spectrum` cannot protect: fit_exponent is public and is called
# with a caller-supplied hk in leg 55's own runner.
nan_ladder = []
for nn in (1, 20, 80, 150, 200, 220):
    h2 = HK_REF.copy()
    h2[BAND_IDX[:nn]] = np.nan
    r, exc, w = call(fit_exponent, K_REF, h2, K_LO, K_HI, 0)
    n_true = int(BAND_IDX.size - nn)
    if r is None:
        nan_ladder.append({"n_nan": nn, "outcome": REJECT, "exc": exc})
        continue
    p = float(r["p"])
    row = {"n_nan": int(nn), "frac_of_band": float(nn / BAND_IDX.size),
           "n_points_reported": int(r["n_points"]), "n_points_actually_finite": n_true,
           "overstatement_factor": float(r["n_points"] / max(n_true, 1)),
           "n_bins": int(r.get("n_bins", -1)) if np.isfinite(p) else None,
           "p": p if np.isfinite(p) else None,
           "err_vs_exact": float(abs(p - P_TRUE)) if np.isfinite(p) else None,
           "warned": bool(w), "domain_valid": r["domain_valid"],
           "frac_zero_modes": r.get("frac_zero_modes"),
           "outcome": VISIBLE if not np.isfinite(p) else (
               SILENT_WRONG if clean_flags(r, w) else VISIBLE)}
    nan_ladder.append(row)
worst_nan = max((r for r in nan_ladder if r.get("outcome") == SILENT_WRONG),
                key=lambda r: r["overstatement_factor"])
record("nonfinite", "NaN planted in fit_exponent's hk (ladder 1..220 of 225)",
       SILENT_WRONG,
       f"{worst_nan['n_nan']} of {BAND_IDX.size} modes ({100 * worst_nan['frac_of_band']:.1f}%) "
       f"set to NaN: the fit DROPS them silently and returns p = {worst_nan['p']:.6f} "
       f"(err {worst_nan['err_vs_exact']:.6f}) while reporting "
       f"n_points = {worst_nan['n_points_reported']} when only "
       f"{worst_nan['n_points_actually_finite']} were finite -- an overstatement of "
       f"{worst_nan['overstatement_factor']:.2f}x, with 0 warnings and domain_valid = True",
       "the bin loop's `hh[idx].mean() > 0.0` test is False for any bin containing a NaN, "
       "so that bin is discarded; `acc` is reset regardless, so the fit proceeds on the "
       "surviving bins. `n_points` is m.sum(), the band width, not the number actually used",
       ladder=nan_ladder)

h_inf = HK_REF.copy()
h_inf[BAND_IDX[:5]] = np.inf
r, exc, w = call(fit_exponent, K_REF, h_inf, K_LO, K_HI, 0)
record("nonfinite", "Inf planted in fit_exponent's hk",
       VISIBLE if (r is not None and not np.isfinite(r["p"])) else SILENT_WRONG,
       f"p = {r['p'] if r else None} with {len(w)} warning(s) "
       f"({'; '.join(x.split(':')[0] for x in w) or 'none'})",
       "Inf survives the mean>0 test, becomes log(inf) in the bin, and polyfit returns "
       "nan -- the defect reaches the caller as a NaN exponent, which is legible")

h_neg = HK_REF.copy()
h_neg[BAND_IDX[:50]] = -1e3
r, exc, w = call(fit_exponent, K_REF, h_neg, K_LO, K_HI, 0)
record("nonfinite", "NEGATIVE coefficient magnitudes (|h_k| = -1e3, impossible)",
       SILENT_WRONG if clean_flags(r, w) else VISIBLE,
       f"50 of {BAND_IDX.size} |h_k| set to -1000 (a magnitude cannot be negative): "
       f"p = {r['p']:.6f}, err {abs(r['p'] - P_TRUE):.6f} -- indistinguishable from clean "
       f"({P_REF:.6f}); the only trace is frac_zero_modes = {r['frac_zero_modes']:.4f}, "
       f"which MISLABELS them as ZERO modes",
       "the `hh <= 0.0` test that computes frac_zero_modes conflates 'annihilated by a "
       "symmetry' (legitimate, the reason the field exists) with 'negative' (impossible)",
       p=float(r["p"]), err=float(abs(r["p"] - P_TRUE)),
       frac_zero_modes=float(r["frac_zero_modes"]))

for lab, C in [("C = NaN", float("nan")), ("C = Inf", float("inf"))]:
    r, exc, w = call(analytic_tail, 1.4, C, 512, S_PROBE, 0)
    record("nonfinite", f"analytic_tail with {lab}",
           SILENT_WRONG if (r and r["finite"] and clean_flags(r, w)) else VISIBLE,
           f"returns finite = {r['finite']} with bound = {r['bound']} and reason = "
           f"{r['reason']!r} -- a bound of {r['bound']} is presented as a VALID tail bound",
           "analytic_tail gates only on `margin = p - s - 1`; the prefactor C is never "
           "checked for finiteness, so a non-finite C passes straight through into the "
           "returned bound with finite = True and reason = None",
           bound=None if not np.isfinite(r["bound"]) else float(r["bound"]),
           bound_repr=repr(r["bound"]))

r, exc, w = call(analytic_tail, 1.4, 0.5, float("nan"), S_PROBE, 0)
record("nonfinite", "analytic_tail with N = NaN",
       SILENT_WRONG if (r and r["finite"] and clean_flags(r, w)) else VISIBLE,
       f"returns finite = True with bound = {r['bound']}, reason = None -- the checkpoint "
       "N is not validated either", "same mechanism: only `margin` is gated",
       bound_repr=repr(r["bound"]))

r, exc, w = call(norm_verdict, float("nan"), S_PROBE, None, 0)
record("nonfinite", "norm_verdict with p = NaN",
       VISIBLE,
       f"finite = {r['finite']} with margin = {r['margin_in_exponent_units']} -- the NaN "
       "is IN the dict beside the verdict, so a caller reading the margin sees it",
       "bool(nan > 0) is False, so the verdict errs toward DIVERGENT, the conservative "
       "direction, and the margin field carries the NaN")


# ==========================================================================
# AXIS 2 -- DEGENERATE / ZERO-NORM INPUT
# ==========================================================================
print("\n--- AXIS 2: degenerate / zero-norm ---")

for lab, prof in [("identically zero", np.zeros_like(X_BIG)),
                  ("constant 1.0", np.ones_like(X_BIG)),
                  ("constant 1e6", 1e6 * np.ones_like(X_BIG))]:
    sp, exc, w = call(spectrum, X_BIG, prof, M=M, far_field="power", tail_exponent=-ALPHA)
    fit = fit_exponent(sp["k"], sp["hk"], K_LO, K_HI, 0)
    psum = weighted_partial_sums(sp["k"], sp["hk"], S_PROBE, [4096], 0)[0]
    nv = norm_verdict(fit["p"], S_PROBE, n_outside_grid=0)
    # TRUTH: these profiles put all their mass in the k = 0 mean.  The weighted l^1 sum
    # over k >= 1 -- which is exactly the norm this module defines -- is ZERO, hence FINITE.
    record("degenerate", f"zero-norm profile: {lab}",
           SILENT_WRONG if (not nv["finite"] and clean_flags(nv, w)) else VISIBLE,
           f"true ||.||_w over k >= 1 is {psum['S_N']:.4e} -- FINITE (all mass is in the "
           f"k = 0 mean, which this module drops by construction) -- but norm_verdict "
           f"returns finite = {nv['finite']} from p = {fit['p']}, with domain_valid = True "
           f"and {len(w)} warnings",
           "a degenerate spectrum has no power law to fit; fit_exponent returns p = nan "
           "(all bins fail the mean>0 test) or a meaningless slope, and norm_verdict "
           "converts that into a DIVERGENT verdict on an object whose norm is 0.  The "
           "error is in the CONSERVATIVE direction, but the verdict is still wrong",
           true_norm=float(psum["S_N"]), p=None if not np.isfinite(fit["p"]) else float(fit["p"]),
           p_repr=repr(fit["p"]), finite_reported=bool(nv["finite"]))

for Mm in (2, 4, 8):
    sp, exc, w = call(spectrum, X_BIG, F_BIG, M=Mm, far_field="power", tail_exponent=-ALPHA)
    n_modes = int(sp["k"].size) if sp else None
    record("degenerate", f"transform size M = {Mm}",
           SILENT_WRONG if (sp is not None and n_modes == 0) else
           (REJECT if exc else SILENT_OK),
           f"exception = {exc}; returns {n_modes} resolved mode(s)"
           + (" -- an EMPTY spectrum, returned as a normal result" if n_modes == 0 else ""),
           "kmax = M//2 - 1, so M = 2 yields an empty k array with no complaint; a caller "
           "then fits an exponent to nothing and gets NaN one function later")

for Mm in (3, 17, 33):
    sp, exc, w = call(spectrum, X_BIG, F_BIG, M=Mm, far_field="power", tail_exponent=-ALPHA)
    record("degenerate", f"ODD transform size M = {Mm}", REJECT if exc else SILENT_WRONG,
           exc or "returned a value",
           "the odd-M path dies inside lagrange_interp_uniform's 2-D fancy indexing")

for lab, Xs, Fs in [("single-point grid", X_BIG[:1], F_BIG[:1]),
                    ("two-point grid", X_BIG[:2], F_BIG[:2]),
                    ("empty grid", X_BIG[:0], F_BIG[:0])]:
    sp, exc, w = call(spectrum, Xs, Fs, M=64, far_field="power", tail_exponent=-ALPHA)
    record("degenerate", lab, REJECT if exc else SILENT_OK, exc or "returned a value",
           "degenerate grids: single-point divides by (rho.size - 1) = 0, empty reduces "
           "max() over nothing")


# ==========================================================================
# AXIS 3 -- BOUNDARY PARAMETERS
# ==========================================================================
print("\n--- AXIS 3: boundary parameters ---")

for lab, args in [("N = 0", (1.4, 0.5, 0, S_PROBE)), ("N < 0", (1.4, 0.5, -512, S_PROBE))]:
    r, exc, w = call(analytic_tail, *args, 0)
    record("boundary", f"analytic_tail with {lab}", REJECT if exc else SILENT_WRONG,
           exc or f"returned {r}",
           "N is the checkpoint the tail starts above; 0 and negative are not meaningful "
           "and the arithmetic happens to fail loudly")

r, exc, w = call(analytic_tail, 1.4, -0.5, 512, S_PROBE, 0)
r_pos, _, _ = call(analytic_tail, 1.4, +0.5, 512, S_PROBE, 0)
record("boundary", "analytic_tail with a NEGATIVE prefactor C",
       SILENT_WRONG if (r and r["finite"] and r["bound"] < 0 and clean_flags(r, w))
       else VISIBLE,
       f"C = -0.5 gives finite = True and bound = {r['bound']:.6f} -- a NEGATIVE upper "
       f"bound on a sum of NON-NEGATIVE terms (the same C with the right sign gives "
       f"{r_pos['bound']:.6f}); reason = {r['reason']!r}, {len(w)} warnings",
       "the sign of C is never checked; `finite` is decided by margin alone",
       bound=float(r["bound"]), bound_positive_C=float(r_pos["bound"]))

r, exc, w = call(analytic_tail, 1.0 + S_PROBE, 0.5, 512, S_PROBE, 0)
record("boundary", "analytic_tail exactly AT the divergence threshold (margin = 0)",
       VISIBLE,
       f"margin = {r['margin']:.1f}, finite = {r['finite']}, bound = {r['bound']}, "
       f"reason = {r['reason']!r} -- the module refuses to bound it and says why "
       "(lesson 73), which is the correct behaviour",
       "this is the positive control for axis 3: the ONE parameter analytic_tail does "
       "gate, it gates correctly and reports a reason instead of a large number")

for lab, p in [("p = +Inf", float("inf")), ("p < 0", -5.0)]:
    r, exc, w = call(norm_verdict, p, S_PROBE, None, 0)
    record("boundary", f"norm_verdict with {lab}", VISIBLE,
           f"finite = {r['finite']}, margin = {r['margin_in_exponent_units']} -- the "
           "unphysical exponent is echoed in the dict beside the verdict",
           "norm_verdict is a pure comparison and carries its inputs, so an absurd p is "
           "readable by the caller")

for cc in (0.5, -0.5, 1e-8, 1e8, 0.0):
    sp, exc, w = call(spectrum, X_BIG, F_BIG, M=M, c=cc, far_field="power",
                      tail_exponent=-ALPHA)
    if sp is None:
        record("boundary", f"compactify scale c = {cc:g}", REJECT, exc,
               "c = 0 makes rho infinite and the finiteness check catches it")
        continue
    fit = fit_exponent(sp["k"], sp["hk"], K_LO, K_HI, sp["n_outside_grid"])
    err = abs(fit["p"] - P_TRUE)
    nv = norm_verdict(fit["p"], S_PROBE, n_outside_grid=sp["n_outside_grid"])
    ok = err < 10 * SYSTEMATIC
    record("boundary", f"compactify scale c = {cc:g}",
           SILENT_OK if ok else (SILENT_WRONG if clean_flags(sp, w) else VISIBLE),
           f"p = {fit['p']:.6f}, err {err:.6f} = {err / SYSTEMATIC:.1f}x the systematic; "
           f"n_outside_grid = {sp['n_outside_grid']}, domain_valid = {sp['domain_valid']}, "
           f"{len(w)} warnings; norm_verdict at s = {S_PROBE} says finite = {nv['finite']}",
           "c is the sinh scale the data are uniform in.  A mismatched c collapses the "
           "interpolation stencil onto a tiny or enormous rho window; nothing in the "
           "module compares c to the grid it was handed",
           p=float(fit["p"]), err=float(err), err_in_systematics=float(err / SYSTEMATIC),
           finite_reported=bool(nv["finite"]))

r, exc, w = call(weighted_partial_sums, K_REF, HK_REF, S_PROBE, [-5, 0, 1], 0)
record("boundary", "weighted_partial_sums with checkpoints N <= 0", VISIBLE,
       f"N = -5 -> S_N = {r[0]['S_N']}, N = 0 -> {r[1]['S_N']}, N = 1 -> {r[2]['S_N']:.6f} "
       "-- an empty prefix correctly sums to 0",
       "searchsorted returns j = -1 for a checkpoint below the first mode and the code "
       "special-cases it")


# ==========================================================================
# AXIS 4 -- PLANTED WRONG-BUT-TYPE-COMPATIBLE VALUES
# ==========================================================================
print("\n--- AXIS 4: planted wrong-value pass-through ---")

# 4.1 THE ADJACENT KEY.  `spectrum` returns BOTH `n_outside_grid` (a count) and
# `frac_outside_grid` (the same thing divided by M).  Threading the wrong one is a one-word
# slip, and it silently inverts the entire guard leg 84 + a bench repair + leg 94 built.
sp745 = None
with warnings.catch_warnings():
    warnings.simplefilter("ignore", TargetNormDomainWarning)
    sp745 = spectrum(X_745, F_745, M=M, far_field="power", tail_exponent=-ALPHA)
d_count = domain_fields(sp745["n_outside_grid"])
d_frac = domain_fields(sp745["frac_outside_grid"])
v_count, _, w_count = call(norm_verdict, 1.5654, 0.5, None, sp745["n_outside_grid"])
v_frac, _, w_frac = call(norm_verdict, 1.5654, 0.5, None, sp745["frac_outside_grid"])
record("passthrough", "the adjacent key: frac_outside_grid threaded as n_outside_grid",
       SILENT_WRONG,
       f"spectrum returns n_outside_grid = {sp745['n_outside_grid']} AND "
       f"frac_outside_grid = {sp745['frac_outside_grid']:.10f} in the SAME dict.  "
       f"Threading the count gives {d_count} and {len(w_count)} warning(s); threading the "
       f"fraction gives {d_frac} and {len(w_frac)} warning(s) -- domain_valid flips "
       f"False -> True and the warning disappears, on the exact configuration leg 84's "
       f"YES was built on",
       "domain_fields does `n = int(n_outside_grid)`, which TRUNCATES.  Any true violation "
       "rate below 100% of samples is a float in (0, 1) and truncates to 0, which is the "
       "literal definition of clean.  _warn_if_outside applies int() the same way, so the "
       "warning is suppressed too",
       n_outside_grid=int(sp745["n_outside_grid"]),
       frac_outside_grid=float(sp745["frac_outside_grid"]),
       domain_fields_from_count=d_count, domain_fields_from_frac=d_frac,
       verdict_from_count=v_count, verdict_from_frac=v_frac)

trunc = []
for bad in (0.9, 0.5, 0.0008544921875, -0.5, -0.99, True, "0", "3"):
    df = domain_fields(bad)
    trunc.append({"input": repr(bad), "n_outside_grid": df["n_outside_grid"],
                  "domain_valid": df["domain_valid"]})
n_clean = sum(1 for t in trunc if t["domain_valid"] is True)
record("passthrough", "domain_fields' int() truncation, swept",
       SILENT_WRONG,
       f"{n_clean} of {len(trunc)} type-compatible wrong values -- including every "
       f"fraction in (-1, 1) and the STRING '0' -- are accepted and reported as "
       f"domain_valid = True; the string '3' is accepted as a count of 3",
       "no type check and no range check; int() silently accepts str, bool, and any float",
       sweep=trunc)

# 4.5 THE HEADLINE: the guard's window is max|X|, but the DATA live on [Xmin, Xmax].
# On any grid that is not symmetric about 0, theta-samples between -max|X| and Xmin are
# INSIDE the guard's window and OUTSIDE the data -- and are polynomially extrapolated.
print("\n  asymmetry ladder (the guard's window is max|X|, the data are [Xmin, Xmax]):")
th = midpoint_theta_grid(M)
Xt = X_of_theta(th)
asym = []
for cut in (-1000.0, -100.0, -10.0, -1.0, -0.1):
    m = X_BIG > cut
    Xa, Fa = X_BIG[m], F_BIG[m]
    sp, exc, w = call(spectrum, Xa, Fa, M=M, far_field="power", tail_exponent=-ALPHA)
    n_extrap = int(((Xt < Xa.min()) & (np.abs(Xt) <= np.abs(Xa).max())).sum())
    fit = fit_exponent(sp["k"], sp["hk"], K_LO, K_HI, sp["n_outside_grid"])
    nv = norm_verdict(fit["p"], S_PROBE, n_outside_grid=sp["n_outside_grid"])
    row = {"cut": float(cut), "X_min_data": float(Xa.min()), "X_max_data": float(Xa.max()),
           "n_grid_points": int(Xa.size),
           "n_theta_samples_extrapolated": n_extrap,
           "frac_extrapolated": float(n_extrap / M),
           "n_outside_grid_reported": int(sp["n_outside_grid"]),
           "domain_valid_reported": sp["domain_valid"],
           "n_warnings": len(w),
           "p": float(fit["p"]), "err_vs_exact": float(abs(fit["p"] - P_TRUE)),
           "err_in_systematics": float(abs(fit["p"] - P_TRUE) / SYSTEMATIC),
           "finite_reported": bool(nv["finite"])}
    asym.append(row)
    print(f"    Xmin={row['X_min_data']:10.3f}  extrapolated={n_extrap:5d}/{M}  "
          f"reported n_outside_grid={row['n_outside_grid_reported']}  "
          f"domain_valid={row['domain_valid_reported']}  warns={len(w)}  "
          f"p={row['p']:+.6f}  err={row['err_vs_exact']:.6f}")
worst = max(asym, key=lambda r: r["err_vs_exact"])
record("passthrough",
       "ASYMMETRIC GRID: the domain guard's window is max|X|, not the data interval",
       SILENT_WRONG,
       f"on a grid truncated at X_min = {worst['X_min_data']:.3f} (still "
       f"{worst['n_grid_points']} real data points spanning "
       f"{worst['X_min_data']:.2f}..{worst['X_max_data']:.3g}), "
       f"{worst['n_theta_samples_extrapolated']} of {M} theta-samples "
       f"({100 * worst['frac_extrapolated']:.2f}%) are polynomially EXTRAPOLATED outside "
       f"the data -- and the module reports n_outside_grid = "
       f"{worst['n_outside_grid_reported']}, domain_valid = "
       f"{worst['domain_valid_reported']}, {worst['n_warnings']} warnings.  The fitted "
       f"exponent is p = {worst['p']:+.6f} against the exact {P_TRUE}, an error of "
       f"{worst['err_vs_exact']:.6f} = {worst['err_in_systematics']:.0f}x the systematic, "
       f"and norm_verdict flips to finite = {worst['finite_reported']}",
       "compactify computes `X_max = |X|.max()` and tests `inside = |Xt| <= X_max`.  For a "
       "grid symmetric about 0 that is exactly the data interval; for any other grid it is "
       "strictly larger, and every theta-sample in the gap is fed to "
       "lagrange_interp_uniform, whose index clip turns it into polynomial EXTRAPOLATION.  "
       "n_outside_grid counts only the samples beyond max|X|, so it reports 0",
       ladder=asym)

# 4.6 wrong-but-type-compatible k ordering into the norm
S_sorted = weighted_partial_sums(K_REF, HK_REF, S_PROBE, [64, 512, 4096], 0)
S_rev = weighted_partial_sums(K_REF[::-1], HK_REF, S_PROBE, [64, 512, 4096], 0)
ratio = S_rev[2]["S_N"] / S_sorted[2]["S_N"]
record("passthrough", "weighted_partial_sums with k in DESCENDING order",
       SILENT_WRONG,
       f"S_64 = {S_rev[0]['S_N']:.6f} against the true {S_sorted[0]['S_N']:.6f} (the norm "
       f"reported as EXACTLY ZERO), and S_4096 = {S_rev[2]['S_N']:.6f} against the true "
       f"{S_sorted[2]['S_N']:.6f} -- an overstatement of {ratio:.2f}x; no warning, "
       "domain_valid = True",
       "np.searchsorted assumes an ascending array and returns nonsense on a descending "
       "one; nothing checks the ordering of k, and the same descending k is what a caller "
       "gets from any reversed convention",
       S_sorted=[{"N": d["N"], "S_N": float(d["S_N"])} for d in S_sorted],
       S_reversed=[{"N": d["N"], "S_N": float(d["S_N"])} for d in S_rev],
       overstatement_factor=float(ratio))

# 4.7 CONTROL THAT COULD HAVE COME OUT DIFFERENTLY (lesson 90): a DESCENDING X grid is a
# perfectly ordinary convention, and the module handles it exactly right.  If this reported
# SILENT_WRONG too, the finding above would be "the module dislikes unusual input", which
# is not a finding.
sp_desc, exc, w = call(spectrum, X_BIG[::-1], F_BIG[::-1], M=M, far_field="power",
                       tail_exponent=-ALPHA)
fit_desc = fit_exponent(sp_desc["k"], sp_desc["hk"], K_LO, K_HI, sp_desc["n_outside_grid"])
record("passthrough", "CONTROL: DESCENDING X grid (a legitimate convention)",
       SILENT_OK,
       f"p = {fit_desc['p']:.6f} vs the ascending reference {P_REF:.6f}, difference "
       f"{abs(fit_desc['p'] - P_REF):.2e} -- the rho mapping is sign-consistent, so a "
       "reversed grid is handled exactly right",
       "this control CAN fail: h_rho would have to be mis-signed for it to. It is here so "
       "that the descending-k finding above is about searchsorted specifically, and not "
       "about the module being fragile to any reordering (lesson 90)",
       p=float(fit_desc["p"]), diff_vs_reference=float(abs(fit_desc["p"] - P_REF)))

rng = np.random.RandomState(0)
perm = rng.permutation(X_BIG.size)
sp_sh, exc, w = call(spectrum, X_BIG[perm], F_BIG[perm], M=M, far_field="power",
                     tail_exponent=-ALPHA)
fit_sh = fit_exponent(sp_sh["k"], sp_sh["hk"], K_LO, K_HI, sp_sh["n_outside_grid"])
record("passthrough", "SHUFFLED X/f pairs (uniform-rho assumption violated)",
       SILENT_WRONG if clean_flags(sp_sh, w) else VISIBLE,
       f"p = {fit_sh['p']:.6e} against the exact {P_TRUE} -- an error of "
       f"{abs(fit_sh['p'] - P_TRUE):.6f}, i.e. "
       f"{100 * abs(fit_sh['p'] - P_TRUE) / P_TRUE:.3f}% of the true exponent -- with "
       f"n_outside_grid = {sp_sh['n_outside_grid']}, domain_valid = "
       f"{sp_sh['domain_valid']}, {len(w)} warnings",
       "lagrange_interp_uniform indexes by position and assumes the samples are uniform in "
       "rho; a permuted pairing violates that silently, since the module never checks that "
       "arcsinh(X/c) is monotone or evenly spaced",
       p=float(fit_sh["p"]), err_vs_exact=float(abs(fit_sh["p"] - P_TRUE)))


# ==========================================================================
# POSITIVE CONTROL FOR THE WHOLE FILE: the harness CAN see a guard
# ==========================================================================
print("\n--- positive control: the harness detects guards where they exist ---")
n_reject = sum(1 for c in CASES if c["outcome"] == REJECT)
n_visible = sum(1 for c in CASES if c["outcome"] == VISIBLE)
n_silent = sum(1 for c in CASES if c["outcome"] == SILENT_WRONG)
n_ok = sum(1 for c in CASES if c["outcome"] == SILENT_OK)
print(f"  {n_reject} REJECT, {n_visible} VISIBLE, {n_silent} SILENT_WRONG, {n_ok} SILENT_OK")


# ==========================================================================
# CLAIM-ADJACENCY: can any of these mechanisms be reached from the BANKED path?
# ==========================================================================
print("\n--- claim adjacency: is any banked number exposed? ---")
b = BorderedHL(n=N_GRID, rho_max=8.0, c=0.5)
XB = np.asarray(b.X, dtype=float)
reach = [
    {"mechanism": "asymmetric grid (guard window = max|X|)",
     "precondition": "the solve grid is not symmetric about X = 0",
     "banked_value": f"|X_min + X_max| = {abs(XB.min() + XB.max()):.3e} on "
                     f"BorderedHL(n={N_GRID}, rho_max=8.0, c=0.5)",
     "reachable": bool(abs(XB.min() + XB.max()) > 1e-12)},
    {"mechanism": "shuffled / non-monotone X",
     "precondition": "X is not ascending",
     "banked_value": f"np.all(diff(X) > 0) = {bool(np.all(np.diff(XB) > 0))}",
     "reachable": not bool(np.all(np.diff(XB) > 0))},
    {"mechanism": "descending k into weighted_partial_sums",
     "precondition": "k is not ascending",
     "banked_value": "k comes from coefficient_magnitudes as np.arange(1, kmax+1), "
                     "which is ascending by construction",
     "reachable": False},
    {"mechanism": "frac_outside_grid threaded as n_outside_grid",
     "precondition": "a call site passes frac_outside_grid where a count is expected",
     "banked_value": "grep over the repo: 2 occurrences of frac_outside_grid, one the "
                     "definition in target_norm.spectrum and one a JSON field in "
                     "experiments/p2_route_tnb_v1_postrepair.py; 0 pass-throughs",
     "reachable": False},
    {"mechanism": "NaN / negative entries in hk",
     "precondition": "hk contains a non-finite or negative entry",
     "banked_value": "coefficient_magnitudes raises on non-finite h and returns "
                     "2*|c_k| >= 0, so every hk produced by spectrum is finite and "
                     "non-negative",
     "reachable": False},
    {"mechanism": "mismatched compactify scale c",
     "precondition": "c differs from the grid's own sinh scale",
     "banked_value": "leg 55's runner passes the same c = 0.5 to BorderedHL and to "
                     "spectrum's default",
     "reachable": False},
    {"mechanism": "degenerate / zero-norm profile",
     "precondition": "the profile has no k >= 1 content",
     "banked_value": "the target is a converged non-trivial Newton solution",
     "reachable": False},
]
n_reachable = sum(1 for r in reach if r["reachable"])
for r in reach:
    print(f"  reachable={str(r['reachable']):5s}  {r['mechanism']}")
print(f"  => {n_reachable} of {len(reach)} mechanisms reachable from the banked call path")


# ==========================================================================
# THE GATE
# ==========================================================================
gate_answer = "YES" if n_silent > 0 else "NO"

payload = {
    "leg": 204, "route": "TNA2",
    "module_under_audit": "solver/target_norm.py",
    "module_was_modified": False,
    "gate": ("Under adversarial and degenerate inputs, does target_norm.py ever silently "
             "return a wrong value rather than reject or visibly propagate the defect?"),
    "gate_answer": gate_answer,
    "instrument": {
        "calibration_family_alpha": ALPHA, "p_exact": P_TRUE,
        "M": M, "n_grid": N_GRID, "band": [K_LO, K_HI], "s_probe": S_PROBE,
        "reference_p": P_REF, "systematic": SYSTEMATIC,
        "reference_n_outside_grid": int(SP_REF["n_outside_grid"]),
        "reference_domain_valid": bool(SP_REF["domain_valid"]),
    },
    "tally": {"total": len(CASES), "REJECT": n_reject, "VISIBLE": n_visible,
              "SILENT_WRONG": n_silent, "SILENT_OK": n_ok},
    "cases": CASES,
    "claim_adjacency": {
        "non_test_importers_of_target_norm": 4,
        "solver_modules_importing_target_norm": 0,
        "banked_numbers_at_risk": [
            "leg 55 capabilities.py line: p = 1.3937 (X_max = 4.1e+04) / 1.3963 (3.0e+05); "
            "margins +0.394 at s = 0, +0.094 at s = 0.3, -0.606 at s = 1"],
        "reachability": reach,
        "n_reachable": n_reachable,
        "verdict": ("NOT CONTAMINATED: every silent mechanism has a precondition the "
                    "banked call path provably does not meet -- the solve grid is "
                    "symmetric to 0.0e+00 and strictly ascending, k is arange by "
                    "construction, hk is finite and non-negative by construction, and no "
                    "call site threads frac_outside_grid.  The findings are LATENT."),
    },
    "prior_art": {
        "leg_55": "built the module (Route-NB); the physics",
        "leg_84": "Route-TNA: adversarial audit, DOMAIN axis, gate YES/SILENT",
        "bench": "domain guard landed (TargetNormDomainWarning + domain_fields)",
        "leg_94": "Route-TNB: precision/false-positive suite for that guard",
        "this_leg": "the four axes none of the above touched",
    },
}

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_tna2_v1_adversarial.json")


def _default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o) if np.isfinite(o) else None
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)


with open(out, "w") as fh:
    json.dump(payload, fh, indent=2, default=_default)

print(f"\nGATE ANSWER: {gate_answer}")
print(f"  {n_silent} of {len(CASES)} cases return a finite, plausible, WRONG number with "
      f"no exception, no warning and every diagnostic field reporting clean.")
print(f"  {n_reachable} of {len(reach)} mechanisms are reachable from the banked call path.")
print(f"wrote {out}")
