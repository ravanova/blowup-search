"""POST-REPAIR regression gates for solver/target_norm.py's domain guard -- Route-TNB, leg 94.

The FALSE-POSITIVE direction, which is the one nothing else in the repo covers.

  * `test_target_norm.py` (leg 55) is the physics and predates the guard: it mentions
    `domain_valid` 0 times.
  * `test_target_norm_adversarial.py` (leg 84, inverted after the repair) proves the guard
    FIRES when it should -- the false-NEGATIVE direction. Its clean-side coverage is 3
    assertions, all on the single configuration `rho_max = 12, M = 16384, power,
    alpha = 0.4`.
  * The bench repair's A/B battery had 4 cases, of which 1 was in-window -- that same
    configuration.

So before this file, the entire claim that the guard does not reject legitimate input
rested on ONE in-window configuration. A guard that is too aggressive is a new,
self-inflicted correctness bug sitting on top of a fix, and it would be invisible to all
three of the above. These gates pin the guard's PRECISION: it must stay silent, report
`n_outside_grid = 0` and `domain_valid = True`, raise nothing, and change no number, on
every input where no theta-sample leaves the supplied grid -- and it must still fire on
inputs where one does (gate 8, without which the rest could pass vacuously; lesson 90).

`solver/target_norm.py` is READ-ONLY to this file's leg. If a gate here fails, the guard
has regressed toward over-rejection; the fix belongs in the module, never in the gate.

Run: `.venv/bin/python test_target_norm_postrepair.py`
"""

import sys
import warnings

import numpy as np

sys.path.insert(0, ".")

from solver.target_norm import (
    TargetNormDomainWarning, X_of_theta, analytic_tail, calibration_family,
    clm_anchor_profile, domain_fields, fit_exponent, inverse_X_profile,
    midpoint_theta_grid, norm_verdict, sawtooth_profile, spectrum,
    weighted_partial_sums,
)

PASS, FAIL = "PASS", "FAIL"
results = []


def gate(name, ok, detail):
    results.append((PASS if ok else FAIL, name, detail))
    print(f"[{PASS if ok else FAIL}] {name}: {detail}")


K_LO, K_HI = 32, 256
CHECKPOINTS = [16, 64, 256]
X_MAX_SHIPPED = 745.2                  # bordered_hl.py at rho_max = 8, c = 0.5
_REACH = {}


def X_reach(M):
    """max|X_j| over the staggered midpoint grid of size M, IN THE MODULE'S OWN FLOATS.

    Analytically `cot(pi/(2M))`, but the closed form must NOT be used as the criterion:
    `tan` is ill-conditioned at `theta/2 -> pi/2` and the two disagree by ~113 ulp at
    M = 512 (gate 3 pins that number). "In-window" is a statement about the floats
    `compactify` actually compares, so it is built from the module's grid constructors.
    """
    M = int(M)
    if M not in _REACH:
        _REACH[M] = float(np.abs(X_of_theta(midpoint_theta_grid(M))).max())
    return _REACH[M]


def grid_with_X_max(X_max, n=801, c=0.5):
    rho_max = float(np.arcsinh(float(X_max) / float(c)))
    return c * np.sinh(np.linspace(-rho_max, rho_max, int(n) | 1))


def grid_with_exact_X_max(T, n=801, c=0.5):
    """max|X| == T bit for bit, so gate 2 tests `<=` at equality and not one ulp away."""
    T = float(T)
    rho_max = float(np.arcsinh(T / float(c)))
    for _ in range(256):
        v = float(c * np.sinh(rho_max))
        if v == T:
            break
        rho_max = float(np.nextafter(rho_max, rho_max + (1.0 if v < T else -1.0)))
    X = c * np.sinh(np.linspace(-rho_max, rho_max, int(n) | 1))
    return X, bool(float(np.abs(X).max()) == T)


def call(fn, *a, **kw):
    """(value, exception_repr_or_None, [domain-warning messages])."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            v, exc = fn(*a, **kw), None
        except Exception as e:                                            # noqa: BLE001
            v, exc = None, f"{type(e).__name__}: {e}"
        return v, exc, [str(x.message) for x in w
                        if issubclass(x.category, TargetNormDomainWarning)]


def pipeline(X, f, M, far_field="power", tail_exponent=None, thread=True):
    """spectrum + all four downstream surfaces; counts warnings, flags and exceptions."""
    sp, exc, w = call(spectrum, X, f, M=M, far_field=far_field,
                      tail_exponent=tail_exponent)
    if sp is None:
        return {"exception": exc, "n_warnings": len(w), "flags": [], "ok_clean": False}
    n_out = int(sp["n_outside_grid"])
    arg = {"n_outside_grid": n_out} if thread else {}
    fit, e1, w1 = call(fit_exponent, sp["k"], sp["hk"], K_LO, K_HI, **arg)
    ps, e2, w2 = call(weighted_partial_sums, sp["k"], sp["hk"], 0.3, CHECKPOINTS, **arg)
    at, e3, w3 = call(analytic_tail, fit["p"], fit["C"], 4096, 0.3, **arg)
    nv, e4, w4 = call(norm_verdict, fit["p"], 0.3, **arg)
    flags = ([sp["domain_valid"], fit["domain_valid"], at["domain_valid"],
              nv["domain_valid"]] + [c["domain_valid"] for c in ps])
    nw = len(w) + len(w1) + len(w2) + len(w3) + len(w4)
    return {"exception": exc, "downstream_exceptions": [e for e in (e1, e2, e3, e4) if e],
            "n_outside_grid": n_out, "n_warnings": nw, "flags": flags,
            "X_max_data": float(sp["X_max_data"]), "sp": sp, "fit": fit, "ps": ps,
            "at": at, "nv": nv,
            "ok_clean": bool(exc is None and nw == 0 and n_out == 0
                             and all(v is True for v in flags)
                             and not [e for e in (e1, e2, e3, e4) if e])}


# --------------------------------------------------------------------------
# 1 -- the in-window ladder: no legitimate call is flagged, anywhere in the span
# --------------------------------------------------------------------------
rows, n_reads, n_true = [], 0, 0
for X_max in (50.0, 100.9, 400.0, X_MAX_SHIPPED):
    X = grid_with_X_max(X_max)
    f = calibration_family(X, 0.4)
    for M in (16, 32, 64, 128, 256, 512, 1024):
        if X_reach(M) > X_max:                     # genuinely out-of-window: gate 8's job
            continue
        for ff, te in (("power", -0.4), ("clamp", None), ("zero", None), ("none", None)):
            r = pipeline(X, f, M, far_field=ff, tail_exponent=te)
            rows.append((X_max, M, ff, r))
            n_reads += len(r["flags"])
            n_true += sum(1 for v in r["flags"] if v is True)
bad = [(x, m, ff) for x, m, ff, r in rows if not r["ok_clean"]]
gate("no legitimate in-window call is flagged, over the whole validated span",
     len(rows) >= 60 and not bad and n_true == n_reads,
     f"{len(rows)} in-window calls (X_max = 50 .. {X_MAX_SHIPPED}, M = 16 .. 1024, 4 "
     f"far-field settings), {n_reads} domain-field reads across spectrum + all four "
     f"downstream surfaces: {n_true} report domain_valid = True, "
     f"{sum(r['n_warnings'] for _, _, _, r in rows)} warnings raised, "
     f"{len(bad)} false positives")

# --------------------------------------------------------------------------
# 2 -- the `<=` at exact equality: max|X| == the largest sample, bit for bit
# --------------------------------------------------------------------------
M2 = 512
reach2 = X_reach(M2)
Xe, exact_ok = grid_with_exact_X_max(reach2)
r_eq = pipeline(Xe, calibration_family(Xe, 0.4), M2, far_field="power", tail_exponent=-0.4)
gate("a grid sitting EXACTLY on the boundary is accepted (compactify tests <=, not <)",
     exact_ok and r_eq["ok_clean"],
     f"max|X| == max|X_j| == {reach2!r} bit-exactly at M = {M2}: "
     f"n_outside_grid = {r_eq['n_outside_grid']}, {r_eq['n_warnings']} warnings, "
     f"{sum(1 for v in r_eq['flags'] if v is True)}/{len(r_eq['flags'])} surfaces "
     "domain_valid = True. A `<` here would reject a call in which every sample lies "
     "on data the grid actually holds")

# --------------------------------------------------------------------------
# 3 -- the threshold is SHARP, and the closed form is not the criterion
# --------------------------------------------------------------------------
closed = float(1.0 / np.tan(np.pi / (2.0 * M2)))
ulp_err = float((reach2 - closed) / np.spacing(reach2))
X_lo = grid_with_X_max(reach2 * (1.0 - 1e-14))
r_lo = pipeline(X_lo, calibration_family(X_lo, 0.4), M2, far_field="power",
                tail_exponent=-0.4)
gate("the threshold is sharp on both sides, and cot(pi/2M) is NOT the criterion",
     r_eq["n_outside_grid"] == 0 and r_lo["n_outside_grid"] >= 1
     and r_lo["n_warnings"] > 0 and ulp_err > 50.0,
     f"one relative 1e-14 BELOW the boundary, {r_lo['n_outside_grid']} sample(s) leave "
     f"and the guard fires ({r_lo['n_warnings']} warnings); exactly ON it, 0 leave and it "
     f"is silent. The closed form cot(pi/(2M)) = {closed!r} sits {ulp_err:.0f} ulp "
     f"(relative {(reach2 - closed) / reach2:.3e}) below the grid's true largest sample "
     f"{reach2!r}, so a criterion built from the closed form mislabels grids inside that "
     "band -- which is why X_reach() above is built from the module's own grid")

# --------------------------------------------------------------------------
# 4 -- the argument combinations an over-eager guard would most plausibly reject
# --------------------------------------------------------------------------
M4 = 256
X4 = grid_with_X_max(max(X_reach(M4) * 2.0, 400.0))
f4 = calibration_family(X4, 0.4)
r_none = pipeline(X4, f4, M4, far_field="none", tail_exponent=None)
r_notail = pipeline(X4, f4, M4, far_field="power", tail_exponent=None)
gate("in-window, the far-field branch does not run, so neither do its rejections",
     r_none["ok_clean"] and r_notail["ok_clean"],
     "far_field='none' returns a finite spectrum with no NaN "
     f"(n_outside = {r_none['n_outside_grid']}, {r_none['n_warnings']} warnings) and "
     "far_field='power' with tail_exponent omitted does NOT raise "
     f"(n_outside = {r_notail['n_outside_grid']}, exception = {r_notail['exception']}) "
     "-- both are legitimate in-window calls with no far field to close")

profiles = ([("clm_anchor", clm_anchor_profile(X4), -1.0),
             ("inverse_X", inverse_X_profile(X4), -1.0),
             ("sawtooth", sawtooth_profile(X4), 0.0)]
            + [(f"alpha={a}", calibration_family(X4, a), -a)
               for a in (0.1, 0.4, 0.8, 1.2, 1.5)])
prof_bad = [n for n, f, te in profiles
            if not pipeline(X4, f, M4, far_field="power", tail_exponent=te)["ok_clean"]]
gate("the guard is profile-blind: every library profile passes in-window",
     not prof_bad,
     f"{len(profiles)} profiles (the CLM anchor, both negative controls, and a 5-point "
     f"calibration sweep alpha = 0.1 .. 1.5) at X_max = {float(np.abs(X4).max()):.6g}, "
     f"M = {M4}: {len(prof_bad)} flagged. The guard reads a sample count, not the data")

# --------------------------------------------------------------------------
# 5 -- domain_fields: every flavour of a clean zero is True, and 1 is still False
# --------------------------------------------------------------------------
zeros = [("int 0", 0), ("np.int64 0", np.int64(0)), ("np.int32 0", np.int32(0)),
         ("float 0.0", 0.0)]
zbad = [n for n, v in zeros if domain_fields(v)["domain_valid"] is not True]
gate("domain_fields calls every flavour of zero clean, and a positive count dirty",
     not zbad and domain_fields(1)["domain_valid"] is False
     and domain_fields(None)["domain_valid"] is None,
     f"{len(zeros)} integer flavours of 0 -> domain_valid True ({len(zbad)} wrong); "
     "1 -> False; None -> None (unknown, falsy by design -- NOT a violation claim, and "
     "adversarial gate 13's standing gap-pin owns that case)")

# --------------------------------------------------------------------------
# 6 -- the downstream surfaces, called directly with a clean count
# --------------------------------------------------------------------------
k = np.arange(1, 2049, dtype=float)
hk = k ** -1.4
surf, sbad = [], []
for name, fn, args in (("fit_exponent", fit_exponent, (k, hk, K_LO, K_HI)),
                       ("weighted_partial_sums", weighted_partial_sums,
                        (k, hk, 0.3, CHECKPOINTS)),
                       ("analytic_tail", analytic_tail, (1.4, 1.0, 4096, 0.3)),
                       ("norm_verdict", norm_verdict, (1.4, 0.3))):
    v, exc, w = call(fn, *args, n_outside_grid=0)
    dv = [c["domain_valid"] for c in v] if isinstance(v, list) else [v["domain_valid"]]
    surf.append(name)
    if exc or w or not all(x is True for x in dv):
        sbad.append(name)
gate("all four downstream surfaces accept a clean count without complaint",
     not sbad and len(surf) == 4,
     f"{len(surf)} surfaces called directly with n_outside_grid=0: {len(sbad)} raised, "
     "warned, or reported anything but domain_valid = True")

# --------------------------------------------------------------------------
# 7 -- numeric invariance: the guard adds fields and changes no number
# --------------------------------------------------------------------------
inv_rows, n_diff = [], 0
for X_max, M in ((100.9, 128), (400.0, 512), (X_MAX_SHIPPED, 1024)):
    X = grid_with_X_max(X_max)
    f = calibration_family(X, 0.4)
    a = pipeline(X, f, M, far_field="power", tail_exponent=-0.4, thread=True)
    b = pipeline(X, f, M, far_field="power", tail_exponent=-0.4, thread=False)
    d = 0
    for tag in ("fit", "at", "nv"):
        for key, vb in b[tag].items():
            if key in ("n_outside_grid", "domain_valid"):
                continue
            va = a[tag].get(key, "<MISSING>")
            if not (va is vb or va == vb
                    or (isinstance(vb, float) and isinstance(va, float)
                        and np.isnan(vb) and np.isnan(va))):
                d += 1
    d += sum(1 for ca, cb in zip(a["ps"], b["ps"]) if ca["S_N"] != cb["S_N"])
    d += sum(1 for key in ("k", "hk", "hk_real_basis")
             if not np.array_equal(a["sp"][key], b["sp"][key]))
    n_diff += d
    inv_rows.append((X_max, M, d, b["nv"]["domain_valid"], b["n_warnings"]))
gate("threading the clean count changes no number, and omitting it warns nobody",
     n_diff == 0 and all(r[3] is None and r[4] == 0 for r in inv_rows),
     f"{len(inv_rows)} in-window configurations, every value returned with "
     f"n_outside_grid=0 threaded vs omitted: {n_diff} differences. The untold call "
     "reports domain_valid = None and stays silent, which is the documented conservative "
     "unknown, not a rejection")

# --------------------------------------------------------------------------
# 8 -- NEGATIVE CONTROL: without this, gates 1-7 could pass vacuously (lesson 90)
# --------------------------------------------------------------------------
neg, n_fired = [], 0
for label, X_max, M in (("one relative 1e-9 below the boundary", X_reach(512) * (1 - 1e-9),
                         512),
                        ("half the boundary", X_reach(512) * 0.5, 512),
                        ("the shipped 745.2 at leg 84's M = 16384", X_MAX_SHIPPED, 16384)):
    X = grid_with_X_max(X_max)
    r = pipeline(X, calibration_family(X, 0.4), M, far_field="power", tail_exponent=-0.4)
    neg.append((label, r["n_outside_grid"], r["n_warnings"]))
    if (r["n_outside_grid"] > 0 and r["n_warnings"] > 0
            and all(v is False for v in r["flags"])):
        n_fired += 1
n_at_shipped = neg[-1][1]
gate("the guard still fires on genuinely out-of-window input",
     n_fired == len(neg) and n_at_shipped == 14,
     f"{n_fired} of {len(neg)} out-of-window calls warn and report domain_valid = False "
     f"on every surface: {', '.join(f'{lab} -> {n} sample(s) out, {w} warnings' for lab, n, w in neg)}"
     f". The last reproduces leg 84's 14 of 16384 exactly, so gates 1-7 are a measurement "
     "of precision and not of a disabled guard")

# ==========================================================================
# GATES 9-13 -- ROUTE-TNRV, LEG 230.  The WINDOW's correctness on ASYMMETRIC grids.
# ==========================================================================
# Leg 94's gates above pin PRECISION on grids symmetric about zero, which is every grid
# this repository's solver actually produces.  Leg 220 then repaired the window from
# `|X| <= max|X|` to `[X.min(), X.max()]`, a change that is INVISIBLE to every gate above
# because all of them are symmetric, where the two windows coincide bit for bit.
#
# These gates pin the repaired behaviour on grids where the two windows DIFFER, against a
# CLOSED FORM rather than against a re-implementation of the module's own loop:
# theta_j = -pi + 2 pi (j + 1/2) / M is inside iff theta_j is in
# [2 arctan(X_lo), 2 arctan(X_hi)], which solves to two ceil/floor evaluations.
#
# `solver/target_norm.py` stays READ-ONLY here too.
import json as _json
import math as _math
import os as _os

_TNRV_M = 16384
_TNRV_ALPHA = 0.4


def _tnrv_closed_form_outside(X_lo, X_hi, M):
    """#{j : X_j outside [X_lo, X_hi]} in closed form.  No array is built."""
    M = int(M)
    def _u(t):
        return M * (t + _math.pi) / (2.0 * _math.pi) - 0.5
    n_below = min(max(_math.ceil(_u(2.0 * _math.atan(float(X_lo)))), 0), M)
    n_above = min(max(M - 1 - _math.floor(_u(2.0 * _math.atan(float(X_hi)))), 0), M)
    return int(n_below + n_above)


def _tnrv_grid(X_lo, X_hi, n=801, c=0.5):
    """X = c sinh(rho) on a UNIFORM rho grid, endpoints NOT assumed symmetric."""
    rho = np.linspace(_math.asinh(float(X_lo) / c), _math.asinh(float(X_hi) / c), int(n))
    return c * np.sinh(rho)


# (name, X_lo, X_hi, expected count -- the closed form is recomputed and must agree)
_TNRV_RUNGS = [
    ("clean_control",   -41000.0, 41000.0,     0),
    ("wide_asymmetric", -41000.0,   745.2,     7),
    ("symmetric_control", -745.2,   745.2,    14),
    ("right_truncated",   -745.2,     3.0,  1685),
    ("two_sided_offset",    -2.0,    50.0,  2522),
    ("excludes_zero",       0.25,   745.2,  9477),
    ("tiny_window",        -0.05,    0.05, 15862),
    ("near_symmetric",    -745.2,   744.0,    14),
]

_tnrv_rows = []
for _name, _lo, _hi, _pinned in _TNRV_RUNGS:
    _X = _tnrv_grid(_lo, _hi)
    _f = calibration_family(_X, _TNRV_ALPHA)
    _truth = _tnrv_closed_form_outside(_X.min(), _X.max(), _TNRV_M)
    # the PRE-REPAIR window, evaluated by the same closed form: [-max|X|, +max|X|]
    _pre = _tnrv_closed_form_outside(-float(np.abs(_X).max()), float(np.abs(_X).max()),
                                     _TNRV_M)
    with warnings.catch_warnings(record=True) as _w:
        warnings.simplefilter("always")
        try:
            _sp = spectrum(_X, _f, M=_TNRV_M, far_field="power",
                           tail_exponent=-_TNRV_ALPHA)
        except ValueError:
            # One-sided interval (`excludes_zero`): the power continuation normalises by
            # each side's OWN endpoint magnitude, which is <= 0 here, so the module
            # REFUSES rather than returning a number.  That refusal is the module's
            # documented "visible" behaviour and is measured in this leg's JSON; it is
            # not gated here, and the clamp ablation is used only so the guard fields
            # below can still be read on this rung.
            _sp = spectrum(_X, _f, M=_TNRV_M, far_field="clamp")
        _fit = fit_exponent(_sp["k"], _sp["hk"], K_LO, K_HI,
                            n_outside_grid=_sp["n_outside_grid"])
        _ps = weighted_partial_sums(_sp["k"], _sp["hk"], 0.0, CHECKPOINTS,
                                    n_outside_grid=_sp["n_outside_grid"])
        _tl = analytic_tail(_fit["p"], _fit["C"], CHECKPOINTS[-1], 0.0,
                            n_outside_grid=_sp["n_outside_grid"])
        _nv = norm_verdict(_fit["p"], 0.0, alpha=_TNRV_ALPHA,
                           n_outside_grid=_sp["n_outside_grid"])
    _tnrv_rows.append({
        "name": _name, "pinned": _pinned, "truth": _truth, "pre": _pre,
        "module": int(_sp["n_outside_grid"]),
        "valid": _sp["domain_valid"],
        "flags": [_fit["domain_valid"], _ps[-1]["domain_valid"], _tl["domain_valid"],
                  _nv["domain_valid"]],
        "n_warn": sum(1 for w in _w if issubclass(w.category, TargetNormDomainWarning)),
        "X_lo": float(_X.min()), "X_hi": float(_X.max()),
    })

# --------------------------------------------------------------------------
# GATE 9 -- the count is the TRUE one, on every rung, against the closed form
# --------------------------------------------------------------------------
_g9 = [r for r in _tnrv_rows if r["module"] == r["truth"] == r["pinned"]]
gate("the reported n_outside_grid equals the closed-form truth on every rung",
     len(_g9) == len(_tnrv_rows),
     f"{len(_g9)} of {len(_tnrv_rows)} rungs agree with a count derived on paper "
     f"(two ceil/floor evaluations, no array): "
     + ", ".join(f"{r['name']} {r['module']}" for r in _tnrv_rows)
     + ". These are pinned magnitudes, not 'greater than zero'")

# --------------------------------------------------------------------------
# GATE 10 -- every asymmetric rung is FLAGGED, and the clean control is NOT
# --------------------------------------------------------------------------
_g10_flag = [r for r in _tnrv_rows if r["truth"] > 0]
_g10_ok = [r for r in _g10_flag
           if r["module"] > 0 and r["valid"] is False and r["n_warn"] > 0]
_clean = next(r for r in _tnrv_rows if r["name"] == "clean_control")
gate("out-of-window rungs are flagged and the in-window rung is not",
     len(_g10_ok) == len(_g10_flag) and _clean["module"] == 0
     and _clean["valid"] is True and _clean["n_warn"] == 0,
     f"{len(_g10_ok)} of {len(_g10_flag)} out-of-window rungs report "
     f"domain_valid = False with a warning; the clean control at X_max = 41000 reports "
     f"{_clean['module']} outside, domain_valid = {_clean['valid']}, "
     f"{_clean['n_warn']} warnings. Without the clean row these gates could pass "
     "vacuously on a guard that always fires (lesson 90)")

# --------------------------------------------------------------------------
# GATE 11 -- the ANTI-TAUTOLOGY row: the pre-repair window would have said CLEAN
# --------------------------------------------------------------------------
_wide = next(r for r in _tnrv_rows if r["name"] == "wide_asymmetric")
_sym_rows = [r for r in _tnrv_rows
             if r["X_lo"] == -r["X_hi"]]
gate("the repaired window differs from the pre-repair one exactly where it must",
     _wide["pre"] == 0 and _wide["truth"] == 7 and _wide["module"] == 7
     and all(r["pre"] == r["truth"] for r in _sym_rows),
     f"on X in [{_wide['X_lo']:.6g}, {_wide['X_hi']:.6g}] the OLD symmetric window "
     f"[-max|X|, +max|X|] reports {_wide['pre']} outside -- perfectly clean -- where the "
     f"true data interval is escaped by {_wide['truth']} samples, and the module now "
     f"reports {_wide['module']}. On all {len(_sym_rows)} symmetric rungs the two windows "
     "coincide and the counts are equal, so this is a real difference and not a "
     "guard that changed everywhere. Worst undercount over the suite: "
     f"{max(r['truth'] - r['pre'] for r in _tnrv_rows)} samples")

# --------------------------------------------------------------------------
# GATE 12 -- the flag REACHES every downstream surface, not just `spectrum`
# --------------------------------------------------------------------------
_g12 = [r for r in _tnrv_rows if all(v is (r["valid"]) for v in r["flags"])]
gate("domain_valid propagates identically to all four downstream surfaces",
     len(_g12) == len(_tnrv_rows),
     f"{len(_g12)} of {len(_tnrv_rows)} rungs carry the same domain_valid through "
     "fit_exponent, weighted_partial_sums, analytic_tail and norm_verdict as through "
     "spectrum. A count nothing reads is not a guard")

# --------------------------------------------------------------------------
# GATE 13 -- leg 55's banked margins, pinned from the artifacts (lesson 68)
# --------------------------------------------------------------------------
# The re-solve itself is two bordered Newton solves (~110 s) and lives in
# experiments/p2_route_tnrv_v1_postrepair.py.  What is pinned HERE, cheaply and
# executably, is that its banked output still agrees with leg 55's banked output BIT FOR
# BIT, and that the margins satisfy the independent identity margin = p - s - 1.
_root = _os.path.dirname(_os.path.abspath(__file__))
_nb = _json.load(open(_os.path.join(_root, "writeup", "data",
                                    "p2_route_nb_v1_targetnorm.json")))["NB5_norms"]
_tnrv = _json.load(open(_os.path.join(_root, "writeup", "data",
                                      "p2_route_tnrv_v1_postrepair.json")))
_pb = _tnrv["part_b_banked_margins"]
_bank = {c["s"]: c["analytic_tail"]["margin"] for c in _nb["classes"]}
_ident = [r for r in _pb["classes"]
          if r["margin_rerun_leg230"] == _bank[r["s"]]
          and (_pb["p_rerun_leg230"] - r["s"] - 1.0) == r["margin_rerun_leg230"]]
gate("leg 55's banked margins survive the repair bit for bit",
     len(_ident) == len(_pb["classes"]) and _pb["p_rerun_leg230"] == _nb["p"]
     and len(_pb["classes"]) == 4,
     f"{len(_ident)} of {len(_pb['classes'])} classes re-solve to the banked margin under "
     f"`==` on raw float64 (never allclose): "
     + ", ".join(f"s={r['s']} -> {r['margin_rerun_leg230']!r}" for r in _pb["classes"])
     + f"; exponent p = {_pb['p_rerun_leg230']!r} against banked {_nb['p']!r}, "
     f"difference {_pb['p_difference']!r}. Each margin also equals p - s - 1 evaluated "
     "in plain Python here, so the agreement is not just two reads of one field")

# --------------------------------------------------------------------------
n_fail = sum(1 for r in results if r[0] == FAIL)
print(f"\n{len(results) - n_fail}/{len(results)} gates pass")
print("Route-TNRV, leg 230 added gates 9-13: the WINDOW's correctness on ASYMMETRIC "
      "grids, which every gate above is structurally blind to because symmetric grids "
      "make the repaired and pre-repair windows coincide.")
print("Route-TNB, leg 94: these gates pin the guard's PRECISION (it must not reject valid "
      "input). test_target_norm_adversarial.py pins its SENSITIVITY (it must catch "
      "violations). A failure here means the guard has drifted toward over-rejection; the "
      "fix belongs in solver/target_norm.py, never in these gates.")
sys.exit(1 if n_fail else 0)
