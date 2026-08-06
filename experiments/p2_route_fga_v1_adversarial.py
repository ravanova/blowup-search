"""Route-FGA v1: an ADVERSARIAL AUDIT of solver/fractional_gclm.py's critical-exponent path.

WHAT THIS IS NOT.  It is not a measurement of `s_c`.  `s_c = alpha/2` is validated against
XU eq (6.3) row by row and is marked PRE-EMPTED under Route-J -- settled physics, treated
here as fixed background and never re-derived, re-measured, or contested.  No number this
file prints is a statement about the value of `s_c` for any physically admissible `s`.

WHAT THIS IS.  Every number here is a statement about CODE BEHAVIOUR UNDER INVALID INPUT.
The question, verbatim from the leg's gate:

    Under an adversarial battery (negative s, s above the model's admissible threshold,
    NaN-poisoned dissipation strength), does solver/fractional_gclm.py's critical-exponent
    computation ever silently return a finite, plausible-looking s_c instead of propagating
    or flagging the invalid input?

WHERE THE BOUNDARY COMES FROM (novelty pass, writeup/novelty/leg_91.md).  The dissipative-gCLM
literature parametrises dissipation as `Lambda^sigma`-hat = |k|^sigma with **sigma = 2s**, and
works at **sigma >= 0** throughout; the lowest exponent anyone treats is the "marginal"
sigma = 0.  So `s < 0` is outside every published range and is the literature-backed invalid
case.  There is no published UPPER bound, so the upper wall is a property of the CODE and is
measured here (the float64 overflow of |k|^{2s}), not asserted.

WHERE TO LOOK, AND WHY (novelty pass N2).  Riesz-potential theory: for sigma < 0 the multiplier
|xi|^sigma has a singularity at xi = 0 and the operator "is not well defined on Schwartz space".
solver/fractional_gclm.py builds `visc = |k|^{2s}` and on the VERY NEXT LINE executes
`visc[0] = 0.0` ("the mean is not dissipated").  For s > 0 that is harmless.  For s < 0 it
overwrites the `inf` that is the mathematical signal the operator is ill-defined.  A1/A2
instrument that line directly.

THE FIVE BATTERIES
  A1  the two pure closed-form functions -- critical_s(alpha), relevance_exponent(s, alpha) --
      under negative, zero, NaN, inf and string-typed arguments.
  A2  OPERATOR CONSTRUCTION.  What `visc` becomes for each adversarial s: finiteness, the
      value at k=0 BEFORE and AFTER the masking line, and MONOTONICITY IN |k| -- the
      substantive corruption, which emits no warning at all.  Plus the measured float64
      overflow wall s_ovf(n).
  A3  THE FULL PIPELINE, end to end: run -> estimate_T -> fit_relevance, one row per
      adversarial input, recording exactly what a caller would see.
  A4  THE HEADLINE -- CONTAMINATION OF THE MEASURED s_c.  F2's relevance line locates the
      measured s_c as the ZERO CROSSING of a linear fit of p(s).  Inject one invalid-s point
      into that fit and measure how far the zero crossing moves.  That is the gate's
      "silently return a finite, plausible-looking s_c", quantified.
  A5  the NaN/inf/negative dissipation-strength cases, reported as PASSES where they pass --
      the novelty pass (N4) requires the report to be a map of behaviour, not a bug list.

RESOLUTION.  n = 512, deliberately modest.  This is an audit of control flow under invalid
input; the comparisons are CLEAN-vs-CONTAMINATED at IDENTICAL settings, so resolution bias
cancels in the difference and no absolute physics number is claimed from any run here.

Deterministic, NOT logged.  Writes writeup/data/p2_route_fga_v1_adversarial.json.

Run: .venv/bin/python -u experiments/p2_route_fga_v1_adversarial.py
"""

import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solver.fractional_gclm import (           # noqa: E402
    FractionalGCLM, critical_s, estimate_T, fit_relevance, relevance_exponent,
)

N_AUDIT = 512
NU_AUDIT = 1e-3
AMP = 3e3
MAX_STEPS = 20000
CLEAN_S = (0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75)
NAN, INF = float("nan"), float("inf")


def w0(n=N_AUDIT):
    x = np.arange(n) * 2.0 * np.pi / n
    return np.sin(x) + 0.4 * np.sin(2.0 * x)


def _num(v):
    """JSON-safe: NaN/inf as tagged strings, so the curated file never carries bare NaN."""
    f = float(v)
    if np.isnan(f):
        return "nan"
    if np.isinf(f):
        return "inf" if f > 0 else "-inf"
    return f


def _call(fn, *args):
    """Call, recording (value | exception) and any warning raised -- the two ways code can
    flag bad input.  Silence is the third way, and it is the one the gate is about."""
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        try:
            out, exc = fn(*args), None
        except Exception as e:                       # noqa: BLE001 -- the audit wants them all
            out, exc = None, "%s: %s" % (type(e).__name__, e)
    return out, exc, [str(w.message) for w in ws]


# --------------------------------------------------------------------------
def a1_pure_functions():
    """The closed forms.  s_c = alpha/2 and p = 1 - 2s/alpha have no guards at all; this
    records what each malformed argument actually returns."""
    print("\n[A1] the closed-form critical-exponent functions under malformed arguments")
    rows = []
    for label, alpha in [("alpha = -1 (negative decay exponent)", -1.0),
                         ("alpha = 0 (degenerate)", 0.0),
                         ("alpha = NaN", NAN),
                         ("alpha = +inf", INF),
                         ("alpha = '0.8' (a STRING)", "0.8")]:
        v, exc, ws = _call(critical_s, alpha)
        rows.append({"fn": "critical_s", "case": label, "arg": str(alpha),
                     "returned": _num(v) if exc is None else None,
                     "exception": exc, "warnings": ws,
                     "finite": bool(exc is None and np.isfinite(float(v)))})
        print("   critical_s(%-6s) -> %-10s exc=%s" % (str(alpha), str(v), exc))
    for label, s, alpha in [("s = -0.5 (invalid: sigma = 2s < 0)", -0.5, 1.0),
                            ("s = -2.0 (invalid)", -2.0, 1.0),
                            ("s = NaN", NAN, 1.0),
                            ("s = 1e6 (far above any admissible s)", 1e6, 1.0),
                            ("alpha = 0 with valid s", 0.35, 0.0)]:
        with np.errstate(all="ignore"):
            v, exc, ws = _call(relevance_exponent, s, alpha)
        rows.append({"fn": "relevance_exponent", "case": label,
                     "arg": "s=%s, alpha=%s" % (s, alpha),
                     "returned": _num(v) if exc is None else None,
                     "exception": exc, "warnings": ws,
                     "finite": bool(exc is None and np.isfinite(float(v)))})
        print("   relevance_exponent(s=%-8s alpha=%-4s) -> %-8s exc=%s"
              % (str(s) + ",", str(alpha), str(v), exc))
    n_silent = sum(1 for r in rows if r["finite"] and not r["exception"] and not r["warnings"])
    print("   => %d of %d malformed arguments returned a FINITE value with no exception and "
          "no warning" % (n_silent, len(rows)))
    return {"rows": rows, "n_cases": len(rows), "n_silent_finite": n_silent}


# --------------------------------------------------------------------------
def a2_operator_construction():
    """What (-Delta)^s BECOMES for an invalid s, and whether the masking line hides it.

    The diagnostic that matters is MONOTONICITY: a fractional Laplacian has visc increasing
    in |k| (it damps high modes hardest).  For s < 0 it DECREASES -- a smoothing/Riesz-type
    multiplier wearing the dissipation's name.  Nothing in the module checks this.
    """
    print("\n[A2] operator construction: what visc = |k|^{2s} becomes, and the visc[0] mask")
    rows = []
    for s in (1.0, 0.35, 0.0, -0.5, -2.0, NAN, 60.0, 200.0):
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter("always")
            try:
                g, exc = FractionalGCLM(n=N_AUDIT, a=0.0, nu=NU_AUDIT, s=s), None
            except Exception as e:                   # noqa: BLE001
                g, exc = None, "%s: %s" % (type(e).__name__, e)
            wmsgs = [str(w.message) for w in ws]
        if exc is not None:
            rows.append({"s": _num(s), "exception": exc, "warnings": wmsgs})
            print("   s=%-8s RAISED %s" % (str(s), exc))
            continue
        v = g.visc
        # what the k=0 entry would have been WITHOUT the masking line
        with np.errstate(all="ignore"):
            raw0 = float(np.abs(g.k).astype(float)[0] ** (2.0 * float(s)))
        lo, hi = float(v[1]), float(v[-1])
        finite = bool(np.all(np.isfinite(v)))
        mono = bool(finite and np.all(np.diff(v[1:]) >= 0.0))
        rows.append({"s": _num(s), "exception": None, "warnings": wmsgs,
                     "visc_all_finite": finite,
                     "visc_k0_raw_before_mask": _num(raw0),
                     "visc_k0_after_mask": _num(v[0]),
                     "mask_hid_a_nonfinite_k0": bool(not np.isfinite(raw0)
                                                     and np.isfinite(v[0])),
                     "visc_at_k1": _num(lo), "visc_at_kmax": _num(hi),
                     "monotone_increasing_in_k": mono,
                     "ratio_kmax_over_k1": _num(hi / lo) if lo != 0 else "nan"})
        print("   s=%-8s finite=%-5s visc[1]=%-11.4g visc[kmax]=%-11.4g monotone_up=%-5s "
              "k0_raw=%-8s mask_hid_nonfinite=%s"
              % (str(s), finite, lo, hi, mono, "%.3g" % raw0, rows[-1]["mask_hid_a_nonfinite_k0"]))
    # the code's own upper wall, measured
    kmax = float(np.abs(FractionalGCLM(n=N_AUDIT).k).max())
    s_ovf = float(np.log(np.finfo(float).max) / (2.0 * np.log(kmax)))
    print("   measured float64 overflow wall at n=%d (k_max=%d): visc goes non-finite for "
          "s > %.4f" % (N_AUDIT, int(kmax), s_ovf))
    return {"rows": rows, "k_max": kmax, "s_overflow_wall": s_ovf, "n": N_AUDIT}


# --------------------------------------------------------------------------
def _pipeline(s, nu=NU_AUDIT, a=0.0, n=N_AUDIT):
    """Exactly the caller path F2 uses: construct -> run -> estimate_T -> fit_relevance."""
    t0 = time.time()
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        try:
            g = FractionalGCLM(n=n, a=a, nu=nu, s=s)
            r = g.run(w0(n), amp_factor=AMP, sample_every=5, max_steps=MAX_STEPS)
            T = estimate_T(r)
            f = fit_relevance(r, T)
            exc = None
        except Exception as e:                       # noqa: BLE001
            r, T, f, exc = {"outcome": "EXCEPTION", "steps": 0, "max_tail": 0.0}, NAN, {}, \
                "%s: %s" % (type(e).__name__, e)
        wmsgs = sorted({str(w.message) for w in ws})
    p = float(f.get("p", NAN))
    return {"s": _num(s), "nu": _num(nu), "outcome": r["outcome"], "steps": int(r["steps"]),
            "T_est": _num(T), "p": _num(p), "n_fit_points": int(f.get("n_points", 0)),
            "fit_rms": _num(f.get("fit_rms", NAN)), "max_tail": _num(r["max_tail"]),
            "p_finite": bool(np.isfinite(p)), "exception": exc, "warnings": wmsgs,
            "seconds": round(time.time() - t0, 2)}


def a3_pipeline():
    """One row per adversarial input, recording exactly what a caller would see."""
    print("\n[A3] the full pipeline under adversarial s  (control row first)")
    # `invalid` is set from the LITERATURE (novelty pass N1): sigma = 2s >= 0 is the studied
    # range, floor sigma = 0.  So s = 0 is ADMISSIBLE and a finite p there is correct
    # behaviour, not a defect -- it is carried as a second control, never counted as a gap.
    rows = []
    for label, s, invalid in [("CONTROL: valid s", 0.35, False),
                              ("CONTROL: s = 0, literature's admissible floor", 0.0, False),
                              ("negative s (invalid, sigma = 2s < 0)", -0.5, True),
                              ("strongly negative s (invalid)", -2.0, True),
                              ("s just under the float64 wall", 60.0, True),
                              ("s over the float64 wall (visc = inf)", 200.0, True),
                              ("s = NaN", NAN, True)]:
        r = _pipeline(s)
        r["case"], r["invalid_input"] = label, invalid
        rows.append(r)
        print("   %-46s outcome=%-16s p=%-10s finite=%-5s T=%-10s (%.1fs)"
              % (label, r["outcome"], str(r["p"])[:9], r["p_finite"], str(r["T_est"])[:9],
                 r["seconds"]))
    silent = [r for r in rows if r["invalid_input"] and r["p_finite"] and r["exception"] is None]
    refused = [r for r in rows if r["invalid_input"] and not r["p_finite"]]
    print("   => of %d INVALID-s inputs: %d returned a FINITE p with no exception "
          "(%s); %d refused with p = nan (%s)"
          % (len(silent) + len(refused), len(silent), ", ".join("s=%s" % r["s"] for r in silent),
             len(refused), ", ".join("s=%s" % r["s"] for r in refused)))
    return {"rows": rows, "n_silent_finite_p": len(silent), "n_refused": len(refused),
            "silent_s_values": [r["s"] for r in silent],
            "refused_s_values": [r["s"] for r in refused]}


# --------------------------------------------------------------------------
def a4_sc_contamination(clean_rows):
    """THE HEADLINE.  How far does one invalid-s point move the MEASURED s_c?

    F2 locates the measured s_c as the zero crossing of a straight-line fit of p(s).  This
    re-runs that fit with a single invalid-s point added and reports the shift.  Only the
    DIFFERENCE is claimed; the absolute zero crossing at n=512 is an audit artefact and is
    explicitly NOT a physics number.
    """
    print("\n[A4] contamination of the MEASURED s_c (the zero crossing of the p(s) fit)")
    ss = np.array([r["s"] for r in clean_rows], float)
    pp = np.array([r["p"] for r in clean_rows], float)
    c = np.polyfit(ss, pp, 1)
    zero_clean = float(-c[1] / c[0])
    print("   clean line:      %d points, slope %+.4f, zero crossing s = %.6f"
          % (len(ss), c[0], zero_clean))
    out = {"clean_s_values": [float(v) for v in ss], "clean_p_values": [float(v) for v in pp],
           "clean_slope": float(c[0]), "clean_zero": zero_clean, "contaminations": []}
    for s_bad in (-0.5, -2.0):
        r = _pipeline(s_bad)
        if not r["p_finite"]:
            print("   s=%.2f did not produce a finite p -- no contamination possible" % s_bad)
            out["contaminations"].append({"s_injected": s_bad, "p_injected": r["p"],
                                          "contaminated_zero": "nan", "shift": "nan",
                                          "propagated_or_flagged": True})
            continue
        s2 = np.append(ss, float(s_bad))
        p2 = np.append(pp, float(r["p"]))
        c2 = np.polyfit(s2, p2, 1)
        z2 = float(-c2[1] / c2[0])
        shift = z2 - zero_clean
        print("   inject s=%+.2f (p=%+.4f, finite, no exception): zero moves %.6f -> %.6f "
              "= %+.6f  (%+.1f%%), slope %+.4f -> %+.4f"
              % (s_bad, r["p"], zero_clean, z2, shift, 100.0 * shift / zero_clean,
                 c[0], c2[0]))
        out["contaminations"].append({
            "s_injected": s_bad, "p_injected": r["p"], "p_injected_finite": True,
            "outcome": r["outcome"], "exception": r["exception"], "warnings": r["warnings"],
            "contaminated_slope": float(c2[0]), "contaminated_zero": z2,
            "shift": shift, "shift_percent": 100.0 * shift / zero_clean,
            "propagated_or_flagged": False})
    return out


# --------------------------------------------------------------------------
def a5_dissipation_strength():
    """NaN/inf/negative nu.  Reported as PASSES where they pass (novelty pass N4)."""
    print("\n[A5] the dissipation STRENGTH nu: NaN-poisoned, infinite, negative")
    ctrl = _pipeline(0.35, nu=NU_AUDIT)
    p_ctrl = float(ctrl["p"])
    print("   %-38s outcome=%-14s p=%-10s  (control)"
          % ("nu = +1e-3 (valid)", ctrl["outcome"], str(ctrl["p"])[:9]))
    rows = []
    for label, nu in [("nu = NaN (the gate's NaN poisoning)", NAN),
                      ("nu = +inf", INF),
                      ("nu = -1e-3 (anti-dissipation)", -1e-3)]:
        r = _pipeline(0.35, nu=nu)
        r["case"] = label
        r["p_vs_control_percent"] = (_num(100.0 * (float(r["p"]) - p_ctrl) / p_ctrl)
                                     if r["p_finite"] else "nan")
        rows.append(r)
        verdict = "SILENT-FINITE" if r["p_finite"] else "propagated/flagged"
        print("   %-38s outcome=%-14s p=%-10s -> %-18s dp/p = %s"
              % (label, r["outcome"], str(r["p"])[:9], verdict,
                 str(r["p_vs_control_percent"])[:7]))
    return {"rows": rows, "control_p": _num(p_ctrl),
            "n_silent_finite_p": sum(1 for r in rows if r["p_finite"])}


# --------------------------------------------------------------------------
def main():
    t0 = time.time()
    print("ROUTE-FGA v1 -- adversarial audit of solver/fractional_gclm.py")
    print("NOT a measurement of s_c (PRE-EMPTED, Route-J, settled). Code robustness only.")
    d = {"leg": 91, "route": "FGA", "n": N_AUDIT, "nu": NU_AUDIT, "amp_factor": AMP,
         "title": "adversarial audit of fractional_gclm.py's critical-exponent path",
         "not_a_physics_measurement": (
             "s_c = alpha/2 is validated against XU eq (6.3) and PRE-EMPTED (Route-J). "
             "Nothing here re-measures or contests it. Every number is code behaviour "
             "under invalid input.")}
    d["A1_pure_functions"] = a1_pure_functions()
    d["A2_operator_construction"] = a2_operator_construction()
    d["A3_pipeline"] = a3_pipeline()

    print("\n[A4-pre] the clean relevance line (the baseline the contamination is measured "
          "against)")
    clean = []
    for s in CLEAN_S:
        r = _pipeline(s)
        print("   s=%.2f  p=%+.4f  outcome=%s  (%.1fs)" % (s, r["p"], r["outcome"],
                                                           r["seconds"]))
        clean.append({"s": float(s), "p": float(r["p"]), "outcome": r["outcome"]})
    d["A4_sc_contamination"] = a4_sc_contamination(clean)
    d["A5_dissipation_strength"] = a5_dissipation_strength()

    # -- the gate, answered from the batteries themselves ------------------
    silent = (d["A3_pipeline"]["n_silent_finite_p"] > 0
              or any(not c["propagated_or_flagged"]
                     for c in d["A4_sc_contamination"]["contaminations"]))
    d["gate"] = {
        "question": ("Under an adversarial battery (negative s, s above the model's "
                     "admissible threshold, NaN-poisoned dissipation strength), does "
                     "solver/fractional_gclm.py's critical-exponent computation ever "
                     "silently return a finite, plausible-looking s_c instead of "
                     "propagating or flagging the invalid input?"),
        "answer": "yes" if silent else "no"}
    d["seconds"] = round(time.time() - t0, 1)
    print("\nGATE: %s" % d["gate"]["answer"].upper())
    out = Path(__file__).resolve().parents[1] / "writeup/data/p2_route_fga_v1_adversarial.json"
    out.write_text(json.dumps(d, indent=2))
    print("wrote %s  (%.1fs)" % (out, d["seconds"]))


if __name__ == "__main__":
    main()
