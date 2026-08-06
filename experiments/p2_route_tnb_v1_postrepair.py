"""ROUTE-TNB, leg 94 -- POST-REPAIR REGRESSION CHECK of target_norm.py's domain guard.

THE GATE (verbatim from DIRECTION.md):

    "Across a battery of legitimate in-window inputs spanning the validated range up to
     X_max=745, does target_norm.py's new domain guard ever incorrectly flag a valid input
     as a violation (a false positive)?"

Leg 84 (Route-TNA) answered the FALSE-NEGATIVE direction: the module silently accepted
out-of-window input, `0 of 6` result-bearing surfaces said so, and the closure choice moved
the fitted exponent by `0.4166` invisibly.  A bench repair added the guard; the bench's own
A/B confirmed leg 55's banked margins survive it bit-identically.  What neither did is
dedicate a battery to the OPPOSITE failure: a guard so aggressive it rejects legitimate
in-window input, which would be a new, self-inflicted correctness bug sitting on top of the
fix.  That is this leg, and only that.

`solver/target_norm.py` is READ-ONLY here, under either branch of the gate.

--------------------------------------------------------------------------
WHAT "IN-WINDOW" MEANS, EXACTLY -- AND WHY IT IS A PROPERTY OF (X_max, M)
--------------------------------------------------------------------------
The guard's threshold is `n_outside_grid > 0`, evaluated against the CALLER'S OWN
`max|X|`, not the literal 745 (`capabilities.py`: "the headline is taken where no sample
point leaves the grid").  `compactify` samples the staggered midpoint grid

    theta_j = -pi + 2 pi (j + 1/2) / M,   X_j = tan(theta_j / 2),

whose largest magnitude is

    X_reach(M) = tan(pi/2 * (1 - 1/M)) = cot(pi / (2 M)) ~ 2M/pi.

THE CLOSED FORM IS NOT USABLE AS THE CRITERION, and finding that out is part of the result:
`tan` is catastrophically ill-conditioned at `theta/2 -> pi/2`, so at `M = 512` the closed
form and the grid's actual largest sample differ by **113 ulp (relative 1.97e-14)**.  This
runner's first pass used the closed form and scored two boundary rows as false positives
that were nothing of the kind -- the extreme sample really did lie outside the data.
`X_reach(M)` below is therefore computed from the module's own grid constructors, and the
discrepancy is banked in `B2` as a magnitude rather than quietly fixed.

So a call is LEGITIMATELY IN-WINDOW exactly when `X_max >= X_reach(M)`: every theta-sample
then lands inside the data and the far-field closure never runs.  A guard is a FALSE
POSITIVE iff it flags such a call.  This is the criterion every block below tests, and it
is the module's own criterion -- computed here independently from the definition of the
grid, never read out of the module.

Note what this makes of the shipped domain: at `X_max = 745.2`, `M` may be at most 1170,
and leg 84's `M = 16384` needs `X_reach = 1.04e+04`.  Leg 84's 14 outside samples were a
TRUE positive.  The battery below therefore has to construct its in-window cases, not
inherit them.

--------------------------------------------------------------------------
THE BATTERY
--------------------------------------------------------------------------
  B1  IN-WINDOW LADDER.  Every (X_max, M) pair with X_max in a sweep spanning the
      validated range up to 745.2 and M a power of two with X_reach(M) <= X_max, across
      four far-field settings.  Every one is legitimate; the guard must be silent, must
      report n_outside_grid = 0 and domain_valid = True, at spectrum AND at all four
      downstream surfaces.
  B2  THE <= BOUNDARY.  compactify's test is `|X_j| <= X_max`.  One grid whose max|X|
      equals the largest sample BIT-EXACTLY (the row that would catch a `<` written where
      a `<=` belongs), plus a straddle at X_reach(M) * (1 + eps) through positive and
      negative eps.  Reports the SMALLEST relative headroom at which the guard is still
      clean and the largest at which it fires -- how sharp the threshold is.
  B3  PROFILES AND ARGUMENT COMBINATIONS.  Every library profile and a calibration sweep,
      in-window, including the two combinations an over-eager guard would most plausibly
      reject: far_field='none' (whose NaN branch must NOT run in-window) and
      far_field='power' with tail_exponent omitted (whose ValueError must NOT fire
      in-window, because there is no far field to close).
  B4  DOWNSTREAM SURFACES AND domain_fields ITSELF.  n_outside_grid = 0 in every integer
      flavour a caller might thread (int, numpy int, float 0.0) must give
      domain_valid = True and no warning.
  B5  NUMERIC INVARIANCE.  For every B1 case, every value returned with
      n_outside_grid = 0 threaded must be bit-identical to the same call with the
      argument omitted.  The guard must add fields and change no number.
  B6  NEGATIVE CONTROLS.  Genuinely out-of-window calls, including one sample past the
      boundary, must fire.  Without this the sweep could pass vacuously (lesson 90: make
      the instrument flip on a control).

Every block records magnitudes.  The verdict is computed from the counts, not asserted.
"""

import json
import os
import sys
import warnings

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from solver.target_norm import (                                          # noqa: E402
    TargetNormDomainWarning, X_of_theta, analytic_tail, calibration_family,
    clm_anchor_profile, domain_fields, fit_exponent, inverse_X_profile,
    midpoint_theta_grid, norm_verdict, sawtooth_profile, spectrum,
    weighted_partial_sums,
)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_tnb_v1_postrepair.json")

# the capabilities.py line this leg is a regression check ON (quoted, never edited):
CAPABILITY_QUOTE = (
    "It is also DOMAIN-limited, not resolution-limited: at the shipped X_max = 745 the "
    "far-field closure moves the exponent by 0.190 and the measurement is not trustworthy "
    "there; the headline is taken where no sample point leaves the grid -- now "
    "CODE-ENFORCED (leg 84 adversarial audit + bench-repair): every exponent-bearing "
    "function returns domain_valid/n_outside_grid and warns on extrapolation "
    "(TargetNormDomainWarning); re-running the headline margins with the guard active "
    "reproduces +0.394/+0.094 to 0.0 diff -- confirmed NOT contaminated")

X_MAX_SHIPPED = 745.2                 # bordered_hl.py at rho_max = 8, c = 0.5
K_LO, K_HI = 32, 256
CHECKPOINTS = [16, 64, 256, 1024]
S_VALUES = (0.0, 0.3, 1.0)


_REACH = {}


def X_reach(M):
    """max |X_j| over the staggered midpoint grid of size M -- IN THE MODULE'S OWN FLOATS.

    Analytically this is `cot(pi/(2M))`, and the closed form is what the first version of
    this runner used.  IT IS NOT USABLE AS THE CRITERION, and the disagreement is a
    finding in its own right: `tan` is catastrophically ill-conditioned at `theta/2 ->
    pi/2`, so at `M = 512` the closed form `1/tan(pi/(2M)) = 325.94830079770134` and the
    grid's actual largest sample `max|X_of_theta(midpoint_theta_grid(M))| =
    325.94830079770776` differ by **113 ulp, relative 1.97e-14**.  Classifying a call as
    in-window with the closed form therefore mislabels grids inside that band, which is
    exactly what happened on this runner's first pass: two boundary rows were scored as
    false positives when the extreme sample really did lie outside the supplied data.

    "In-window" is a statement about the numbers `compactify` actually compares, so it is
    computed here from the module's own grid constructors (`midpoint_theta_grid`,
    `X_of_theta`) -- never from the guard, and never from a closed form.
    """
    M = int(M)
    if M not in _REACH:
        _REACH[M] = float(np.abs(X_of_theta(midpoint_theta_grid(M))).max())
    return _REACH[M]


def grid_with_X_max(X_max, n=801, c=0.5):
    """Uniform-in-rho grid X = c sinh(rho) whose max|X| is `X_max` to within rounding."""
    rho_max = float(np.arcsinh(float(X_max) / float(c)))
    rho = np.linspace(-rho_max, rho_max, int(n) | 1)
    return c * np.sinh(rho)


def grid_with_exact_X_max(T, n=801, c=0.5):
    """Grid whose max|X| equals `T` BIT-EXACTLY, for probing compactify's `<=` at equality.

    `c sinh(arcsinh(T/c))` is generally a ulp off `T`, which would make an "exactly at the
    boundary" probe test something one ulp away from the boundary instead.  `rho_max` is
    nudged by `nextafter` until the endpoint lands on `T` exactly; `np.linspace` reproduces
    its endpoint exactly, so `max|X| == T` holds bit for bit.
    """
    T = float(T)
    rho_max = float(np.arcsinh(T / float(c)))
    for _ in range(256):
        v = float(c * np.sinh(rho_max))
        if v == T:
            break
        rho_max = float(np.nextafter(rho_max, rho_max + (1.0 if v < T else -1.0)))
    rho = np.linspace(-rho_max, rho_max, int(n) | 1)
    X = c * np.sinh(rho)
    return X, bool(float(np.abs(X).max()) == T)


def call(fn, *a, **kw):
    """(value, exception_repr_or_None, [domain-warning messages])."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            v, exc = fn(*a, **kw), None
        except Exception as e:                                            # noqa: BLE001
            v, exc = None, f"{type(e).__name__}: {e}"
        msgs = [str(x.message) for x in w
                if issubclass(x.category, TargetNormDomainWarning)]
    return v, exc, msgs


def run_pipeline(X, f, M, far_field="power", tail_exponent=None, thread=True):
    """spectrum + the four downstream surfaces, counting warnings and flags separately.

    `thread=True` passes n_outside_grid= down (the correct calling convention); False
    omits it, which is the legacy call and must report domain_valid = None, not False.
    """
    sp, exc, w_sp = call(spectrum, X, f, M=M, far_field=far_field,
                         tail_exponent=tail_exponent)
    rec = {"exception": exc, "n_warnings": len(w_sp), "warnings": w_sp}
    if sp is None:
        return rec
    n_out = int(sp["n_outside_grid"])
    arg = {"n_outside_grid": n_out} if thread else {}
    fit, e1, w1 = call(fit_exponent, sp["k"], sp["hk"], K_LO, K_HI, **arg)
    ps, e2, w2 = call(weighted_partial_sums, sp["k"], sp["hk"], 0.3, CHECKPOINTS, **arg)
    at, e3, w3 = call(analytic_tail, fit["p"], fit["C"], 4096, 0.3, **arg)
    nv, e4, w4 = call(norm_verdict, fit["p"], 0.3, **arg)
    flags = ([sp["domain_valid"], fit["domain_valid"], at["domain_valid"],
              nv["domain_valid"]] + [c["domain_valid"] for c in ps])
    rec.update({
        "n_outside_grid": n_out,
        "frac_outside_grid": float(sp["frac_outside_grid"]),
        "X_max_data": float(sp["X_max_data"]),
        "domain_valid_spectrum": sp["domain_valid"],
        "domain_valid_all": flags,
        "n_surfaces_flagged_false": sum(1 for v in flags if v is False),
        "n_surfaces_flagged_true": sum(1 for v in flags if v is True),
        "n_surfaces_unknown": sum(1 for v in flags if v is None),
        "n_warnings": len(w_sp) + len(w1) + len(w2) + len(w3) + len(w4),
        "warnings": w_sp + w1 + w2 + w3 + w4,
        "downstream_exceptions": [e for e in (e1, e2, e3, e4) if e],
        "p": float(fit["p"]), "C": float(fit["C"]), "r2": float(fit["r2"]),
        "verdict_finite": bool(nv["finite"]),
        "margin_in_exponent_units": float(nv["margin_in_exponent_units"]),
        "_sp": sp, "_fit": fit, "_ps": ps, "_at": at, "_nv": nv,
    })
    return rec


def strip(rec):
    return {k: v for k, v in rec.items() if not k.startswith("_")}


# --------------------------------------------------------------------------
# B1 -- the in-window ladder across the validated range up to X_max = 745
# --------------------------------------------------------------------------
def b1_in_window_ladder():
    X_MAXES = [13.6, 25.0, 50.0, 100.9, 200.0, 400.0, 600.0, X_MAX_SHIPPED]
    MS = [16, 32, 64, 128, 256, 512, 1024]
    cases, skipped = [], 0
    for X_max in X_MAXES:
        X = grid_with_X_max(X_max)
        for M in MS:
            if X_reach(M) > X_max:            # genuinely out-of-window: not this block's
                skipped += 1
                continue
            for ff, te in (("power", -0.4), ("clamp", None), ("zero", None),
                           ("none", None)):
                rec = run_pipeline(X, calibration_family(X, 0.4), M,
                                   far_field=ff, tail_exponent=te)
                rec.update({"X_max_requested": float(X_max), "M": int(M),
                            "X_reach_M": X_reach(M),
                            "headroom_ratio": float(X_max / X_reach(M)),
                            "far_field": ff})
                cases.append(rec)
    fp = [strip(c) for c in cases
          if c.get("exception") or c["n_warnings"] > 0
          or c.get("n_outside_grid", -1) != 0
          or c["n_surfaces_flagged_false"] > 0 or c["downstream_exceptions"]]
    return {"what": ("every (X_max, M) pair with X_reach(M) <= X_max, X_max spanning "
                     "13.6 .. 745.2 and M = 16 .. 1024, x 4 far-field settings; all are "
                     "legitimately in-window, so a warning or a domain_valid = False "
                     "anywhere is a FALSE POSITIVE"),
            "n_cases": len(cases),
            "n_pairs_skipped_as_genuinely_out_of_window": skipped,
            "X_max_span": [min(c["X_max_requested"] for c in cases),
                           max(c["X_max_requested"] for c in cases)],
            "M_span": [min(c["M"] for c in cases), max(c["M"] for c in cases)],
            "headroom_ratio_span": [min(c["headroom_ratio"] for c in cases),
                                    max(c["headroom_ratio"] for c in cases)],
            "n_total_surface_reads": sum(len(c["domain_valid_all"]) for c in cases),
            "n_surface_reads_true": sum(c["n_surfaces_flagged_true"] for c in cases),
            "n_warnings_total": sum(c["n_warnings"] for c in cases),
            "n_false_positives": len(fp),
            "false_positives": fp,
            "cases": [strip(c) for c in cases]}


# --------------------------------------------------------------------------
# B2 -- the <= boundary: how sharp is the threshold, and is "exactly at" accepted?
# --------------------------------------------------------------------------
def b2_boundary():
    M, rows = 512, []
    reach = X_reach(M)
    closed_form = float(1.0 / np.tan(np.pi / (2.0 * M)))

    # (a) EXACT EQUALITY: max|X| == max|X_j| bit for bit.  compactify tests `<=`, so this
    # is legitimate in-window input and the guard must be silent.  If `<` had been written
    # instead of `<=`, this single row is what would catch it.
    Xe, exact_ok = grid_with_exact_X_max(reach)
    rec = run_pipeline(Xe, calibration_family(Xe, 0.4), M,
                       far_field="power", tail_exponent=-0.4)
    rows.append({"eps": 0.0, "label": "max|X| == max|X_j| EXACTLY (the `<=` itself)",
                 "X_max_requested": reach, "constructed_exactly": exact_ok,
                 "X_max_realised": rec.get("X_max_data"),
                 "in_window": bool(rec.get("X_max_data", 0.0) >= reach), **strip(rec)})

    # (b) the straddle, in relative units of the boundary
    for eps in (1e-2, 1e-4, 1e-6, 1e-9, 1e-12, 1e-14,
                -1e-14, -1e-12, -1e-9, -1e-6, -1e-4, -1e-2):
        X_max = reach * (1.0 + eps)
        X = grid_with_X_max(X_max)
        rec = run_pipeline(X, calibration_family(X, 0.4), M,
                           far_field="power", tail_exponent=-0.4)
        rows.append({"eps": float(eps), "label": f"boundary * (1 + {eps:g})",
                     "X_max_requested": float(X_max),
                     "X_max_realised": rec.get("X_max_data"),
                     "in_window": bool(rec.get("X_max_data", 0.0) >= reach),
                     **strip(rec)})

    clean = [r for r in rows if r.get("n_outside_grid") == 0]
    fired = [r for r in rows if r.get("n_outside_grid", 0) > 0]
    # a false positive = a row whose realised max|X| >= the grid's own largest sample
    # (so every sample is inside the data) but which fired anyway
    fp = [r for r in rows if r["in_window"]
          and (r.get("n_outside_grid", 0) > 0 or r["n_warnings"] > 0)]
    return {"what": ("grids whose max|X| straddles the grid's own largest sample by "
                     "relative eps, plus one grid sitting on it BIT-EXACTLY, testing "
                     "compactify's `|X_j| <= X_max` at its own edge"),
            "M": M, "X_reach_M": reach,
            "closed_form_cot_pi_over_2M": closed_form,
            "closed_form_ulp_error": float((reach - closed_form) / np.spacing(reach)),
            "closed_form_relative_error": float((reach - closed_form) / reach),
            "exact_equality_row_is_exact": rows[0]["constructed_exactly"],
            "exact_equality_row_n_outside": rows[0].get("n_outside_grid"),
            "exact_equality_row_n_warnings": rows[0]["n_warnings"],
            "n_rows": len(rows), "n_clean": len(clean), "n_fired": len(fired),
            "smallest_clean_headroom": (min(r["X_max_realised"] / reach - 1.0
                                            for r in clean) if clean else None),
            "largest_fired_headroom": (max(r["X_max_realised"] / reach - 1.0
                                           for r in fired) if fired else None),
            "n_outside_at_first_firing": (min(r["n_outside_grid"] for r in fired)
                                          if fired else None),
            "n_false_positives": len(fp), "false_positives": fp,
            "rows": rows}


# --------------------------------------------------------------------------
# B3 -- profiles and the argument combinations an over-eager guard would reject
# --------------------------------------------------------------------------
def b3_profiles():
    M = 256
    X_max = max(X_reach(M) * 2.0, 400.0)
    X = grid_with_X_max(X_max)
    profiles = [("clm_anchor", clm_anchor_profile(X), -1.0),
                ("inverse_X", inverse_X_profile(X), -1.0),
                ("sawtooth", sawtooth_profile(X), 0.0)]
    for a in (0.1, 0.4, 0.8, 1.2, 1.5):
        profiles.append((f"calibration_alpha={a}", calibration_family(X, a), -a))
    rows = []
    for name, f, te in profiles:
        rec = run_pipeline(X, f, M, far_field="power", tail_exponent=te)
        rows.append({"profile": name, "tail_exponent": te, **strip(rec)})
    # the two argument combinations an over-eager guard would most plausibly reject
    edge = []
    for label, ff, te in (("far_field='none' in-window (the NaN branch must NOT run)",
                           "none", None),
                          ("far_field='power' with tail_exponent omitted, in-window "
                           "(the ValueError must NOT fire: there is no far field)",
                           "power", None)):
        rec = run_pipeline(X, calibration_family(X, 0.4), M, far_field=ff,
                           tail_exponent=te)
        edge.append({"case": label, "far_field": ff, "tail_exponent": te, **strip(rec)})
    allrows = rows + edge
    fp = [r for r in allrows if r.get("exception") or r["n_warnings"] > 0
          or r.get("n_outside_grid", -1) != 0 or r.get("downstream_exceptions")]
    return {"what": ("every library profile and a 5-point calibration sweep, plus the two "
                     "argument combinations most likely to be over-rejected, all at "
                     f"X_max = {X_max:.6g} with M = {M} (X_reach = {X_reach(M):.6g})"),
            "M": M, "X_max": float(X_max), "X_reach_M": X_reach(M),
            "n_rows": len(allrows), "n_false_positives": len(fp), "false_positives": fp,
            "profiles": rows, "argument_edge_cases": edge}


# --------------------------------------------------------------------------
# B4 -- domain_fields itself, and the downstream surfaces at n_outside_grid = 0
# --------------------------------------------------------------------------
def b4_domain_fields():
    flavours = [("python int 0", 0), ("numpy int64 0", np.int64(0)),
                ("numpy int32 0", np.int32(0)), ("float 0.0", 0.0),
                ("python int 1 (control)", 1), ("None (unknown)", None)]
    rows = []
    for label, val in flavours:
        d, exc, w = call(domain_fields, val)
        rows.append({"input": label, "exception": exc, "n_warnings": len(w),
                     "domain_valid": None if d is None else d["domain_valid"],
                     "n_outside_grid": None if d is None else d["n_outside_grid"]})
    surfaces = []
    k = np.arange(1, 2049, dtype=float)
    hk = 1.0 * k ** -1.4
    for name, fn, args in (("fit_exponent", fit_exponent, (k, hk, K_LO, K_HI)),
                           ("weighted_partial_sums", weighted_partial_sums,
                            (k, hk, 0.3, CHECKPOINTS)),
                           ("analytic_tail", analytic_tail, (1.4, 1.0, 4096, 0.3)),
                           ("norm_verdict", norm_verdict, (1.4, 0.3))):
        v, exc, w = call(fn, *args, n_outside_grid=0)
        dv = ([c["domain_valid"] for c in v] if isinstance(v, list)
              else [v["domain_valid"]])
        surfaces.append({"surface": name, "exception": exc, "n_warnings": len(w),
                         "domain_valid": dv,
                         "all_true": all(x is True for x in dv)})
    # a false positive = a clean-zero flavour reported as not-valid, or any warning
    fp = [r for r in rows if r["input"].startswith(("python int 0", "numpy", "float"))
          and (r["domain_valid"] is not True or r["n_warnings"] > 0)]
    fp += [s for s in surfaces if not s["all_true"] or s["n_warnings"] > 0 or s["exception"]]
    return {"what": ("domain_fields at every integer flavour of zero a caller might "
                     "thread, and the four downstream surfaces called directly with "
                     "n_outside_grid=0"),
            "domain_fields_rows": rows, "surface_rows": surfaces,
            "n_false_positives": len(fp), "false_positives": fp}


# --------------------------------------------------------------------------
# B5 -- numeric invariance: threading n_outside_grid = 0 must change no number
# --------------------------------------------------------------------------
def b5_invariance():
    rows = []
    for X_max, M in ((100.9, 128), (400.0, 512), (X_MAX_SHIPPED, 1024)):
        X = grid_with_X_max(X_max)
        f = calibration_family(X, 0.4)
        a = run_pipeline(X, f, M, far_field="power", tail_exponent=-0.4, thread=True)
        b = run_pipeline(X, f, M, far_field="power", tail_exponent=-0.4, thread=False)
        diffs = []
        for tag in ("_fit", "_at", "_nv"):
            for key, vb in b[tag].items():
                if key in ("n_outside_grid", "domain_valid"):
                    continue
                va = a[tag].get(key, "<MISSING>")
                same = (va is vb or va == vb
                        or (isinstance(vb, float) and isinstance(va, float)
                            and np.isnan(vb) and np.isnan(va)))
                if not same:
                    diffs.append([tag, key, repr(vb), repr(va)])
        for ca, cb in zip(a["_ps"], b["_ps"]):
            if ca["S_N"] != cb["S_N"]:
                diffs.append(["_ps", f"S_N@{cb['N']}", repr(cb["S_N"]), repr(ca["S_N"])])
        for key in ("k", "hk", "hk_real_basis"):
            if not np.array_equal(a["_sp"][key], b["_sp"][key]):
                diffs.append(["_sp", key, "<array>", "<array differs>"])
        rows.append({"X_max": float(X_max), "M": int(M),
                     "n_outside_grid": a["n_outside_grid"],
                     "domain_valid_threaded": a["domain_valid_spectrum"],
                     "domain_valid_untold": b["_nv"]["domain_valid"],
                     "warnings_threaded": a["n_warnings"],
                     "warnings_untold": b["n_warnings"],
                     "n_value_differences": len(diffs), "differences": diffs})
    return {"what": ("in-window, every number returned with n_outside_grid=0 threaded vs "
                     "omitted; the guard must add fields and change no value. The untold "
                     "call reports domain_valid = None (unknown, falsy by design, adversarial "
                     "gate 13's standing gap-pin), which is NOT a false positive: it is not a "
                     "claim of violation"),
            "rows": rows,
            "n_value_differences_total": sum(r["n_value_differences"] for r in rows),
            "n_untold_reported_false": sum(1 for r in rows
                                           if r["domain_valid_untold"] is False),
            "n_untold_reported_none": sum(1 for r in rows
                                          if r["domain_valid_untold"] is None)}


# --------------------------------------------------------------------------
# B6 -- negative controls: the guard must still fire when it should (lesson 90)
# --------------------------------------------------------------------------
def b6_negative_controls():
    rows = []
    # (a) one sample past the boundary -- the sharpest TRUE positive available
    M = 512
    reach = X_reach(M)
    for label, X_max in (("one hair BELOW X_reach(M): 2 samples must leave",
                          reach * (1.0 - 1e-9)),
                         ("half of X_reach(M)", reach * 0.5),
                         ("the shipped X_max = 745.2 at leg 84's M = 16384",
                          X_MAX_SHIPPED)):
        Mi = 16384 if "16384" in label else M
        X = grid_with_X_max(X_max)
        rec = run_pipeline(X, calibration_family(X, 0.4), Mi,
                           far_field="power", tail_exponent=-0.4)
        rows.append({"case": label, "M": Mi, "X_max": float(X_max),
                     "X_reach_M": X_reach(Mi), **strip(rec)})
    n_fired = sum(1 for r in rows
                  if r.get("n_outside_grid", 0) > 0 and r["n_warnings"] > 0
                  and r["n_surfaces_flagged_false"] == len(r["domain_valid_all"]))
    return {"what": ("genuinely out-of-window calls; if these did NOT fire, a clean sweep "
                     "above would be vacuous"),
            "rows": rows, "n_rows": len(rows), "n_fired_correctly": n_fired,
            "n_outside_at_one_hair_below": rows[0].get("n_outside_grid")}


# --------------------------------------------------------------------------
def main():
    res = {
        "leg": 94, "route": "TNB", "kind": "post-repair regression check",
        "gate": ("Across a battery of legitimate in-window inputs spanning the validated "
                 "range up to X_max=745, does target_norm.py's new domain guard ever "
                 "incorrectly flag a valid input as a violation (a false positive)?"),
        "module_under_test": "solver/target_norm.py (READ-ONLY under this leg)",
        "capabilities_line_quoted": CAPABILITY_QUOTE,
        "in_window_criterion": ("X_max >= X_reach(M) = cot(pi/(2M)); computed here from "
                                "the definition of the staggered grid, not read from the "
                                "module"),
    }
    res["B1_in_window_ladder"] = b1_in_window_ladder()
    res["B2_boundary"] = b2_boundary()
    res["B3_profiles"] = b3_profiles()
    res["B4_domain_fields"] = b4_domain_fields()
    res["B5_invariance"] = b5_invariance()
    res["B6_negative_controls"] = b6_negative_controls()

    # CONTEXT, not a claim: staying in-window at the shipped domain caps M at ~1170
    # (X_reach(1024) = 651.9, X_reach(2048) = 1303.8 > 745.2), and the calibration family's
    # exponent is not converged there.  This is leg 55's own tension -- the trustworthy
    # domain and the resolved exponent pull apart -- restated as a magnitude.  It is NOT a
    # defect of the guard (which computes nothing), NOT a claim about the target, and NOT
    # an argument for widening the domain, which a live ban forbids and this leg does not do.
    ladder = [c for c in res["B1_in_window_ladder"]["cases"]
              if c["far_field"] == "power" and c["X_max_requested"] == X_MAX_SHIPPED]
    res["context_resolution_cost_of_staying_in_window"] = {
        "note": ("magnitudes only; the exponent is leg 55's object and nothing here "
                 "re-measures or re-claims it"),
        "X_max": X_MAX_SHIPPED, "p_true_calibration_alpha_0.4": 1.4,
        "largest_in_window_M": max(c["M"] for c in ladder),
        "p_by_M": {str(c["M"]): [c["p"], abs(c["p"] - 1.4)] for c in sorted(
            ladder, key=lambda c: c["M"])},
    }

    n_fp = (res["B1_in_window_ladder"]["n_false_positives"]
            + res["B2_boundary"]["n_false_positives"]
            + res["B3_profiles"]["n_false_positives"]
            + res["B4_domain_fields"]["n_false_positives"])
    n_probes = (res["B1_in_window_ladder"]["n_cases"] + res["B2_boundary"]["n_clean"]
                + res["B3_profiles"]["n_rows"]
                + len(res["B4_domain_fields"]["domain_fields_rows"])
                + len(res["B4_domain_fields"]["surface_rows"]))
    controls_ok = (res["B6_negative_controls"]["n_fired_correctly"]
                   == res["B6_negative_controls"]["n_rows"])
    res["headline"] = {
        "n_in_window_probes": n_probes,
        "n_surface_reads_in_window": res["B1_in_window_ladder"]["n_total_surface_reads"],
        "n_false_positives": n_fp,
        "n_warnings_on_in_window_input": res["B1_in_window_ladder"]["n_warnings_total"],
        "n_value_differences_from_the_guard":
            res["B5_invariance"]["n_value_differences_total"],
        "negative_controls_all_fired": bool(controls_ok),
        "gate_answer": ("NO" if (n_fp == 0 and controls_ok) else
                        ("YES" if n_fp > 0 else "INDETERMINATE")),
        "verdict": ("NO_FALSE_POSITIVE" if (n_fp == 0 and controls_ok) else
                    ("FALSE_POSITIVE_FOUND" if n_fp > 0 else
                     "VACUOUS: negative controls did not fire")),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(json.dumps(res["headline"], indent=2))
    print(f"\nwrote {OUT}")
    for key in ("B1_in_window_ladder", "B2_boundary", "B3_profiles", "B4_domain_fields",
                "B5_invariance", "B6_negative_controls"):
        b = res[key]
        print(f"  {key}: " + ", ".join(
            f"{k}={b[k]}" for k in ("n_cases", "n_rows", "n_clean", "n_fired",
                                    "n_false_positives", "n_warnings_total",
                                    "n_value_differences_total", "n_fired_correctly",
                                    "smallest_clean_headroom", "largest_fired_headroom",
                                    "n_outside_at_one_hair_below")
            if k in b))
    return res


if __name__ == "__main__":
    main()
