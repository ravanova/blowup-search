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

# --------------------------------------------------------------------------
n_fail = sum(1 for r in results if r[0] == FAIL)
print(f"\n{len(results) - n_fail}/{len(results)} gates pass")
print("Route-TNB, leg 94: these gates pin the guard's PRECISION (it must not reject valid "
      "input). test_target_norm_adversarial.py pins its SENSITIVITY (it must catch "
      "violations). A failure here means the guard has drifted toward over-rejection; the "
      "fix belongs in solver/target_norm.py, never in these gates.")
sys.exit(1 if n_fail else 0)
