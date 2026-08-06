"""Route-TNA, leg 84: DOES solver/target_norm.py SIGNAL A DOMAIN VIOLATION, OR RETURN
A NUMBER?

--------------------------------------------------------------------------
THE GATE, VERBATIM
--------------------------------------------------------------------------
"Under adversarial inputs that push sample points beyond the validated X_max = 745 window
(or otherwise into the region capabilities.py already flags as untrustworthy), does
`target_norm.py` silently return a result with no warning or flag, or does it correctly
signal the domain violation?"

--------------------------------------------------------------------------
WHAT IS AND IS NOT BEING RE-MEASURED
--------------------------------------------------------------------------
`capabilities.py`'s validated line for `solver/target_norm.py` (grepped first, per the
live ban) already states the PHYSICS of the window, measured by leg 55 (Route-NB):

    "... It is also DOMAIN-limited, not resolution-limited: at the shipped X_max = 745 the
     far-field closure moves the exponent by 0.190 and the measurement is not trustworthy
     there; the headline is taken where no sample point leaves the grid"

That is prior art and this leg does not claim it.  This leg audits the SOFTWARE: given an
input that lands inside the region that sentence calls untrustworthy, what does the module
tell its caller?  Three channels are the only ones a caller has:

    (1) an exception,
    (2) a `warnings.warn` record,
    (3) a field in the returned object that NAMES the violation.

Every probe below is run inside `warnings.catch_warnings(record=True)` with
`simplefilter("always")`, so channel (2) cannot be missed, and every returned object has
its keys enumerated, so channel (3) is decided by inspection and not by belief.

This leg EXTENDS NO DOMAIN.  `X_max` is varied downward and upward purely as the
adversarial knob; nothing here repairs, closes, or widens any gap, and no file outside the
leg's declared territory is touched.

--------------------------------------------------------------------------
WHY THE KNOWN-ANSWER OBJECT IS THE CALIBRATION FAMILY
--------------------------------------------------------------------------
`calibration_family(X, alpha) = (1 + X^2)^(-alpha/2)` has `p = 1 + alpha` EXACTLY, for
every alpha, and target_norm's own docstring says so.  Using it means every probe has a
truth value, so "how wrong is the number the caller silently received" is a MAGNITUDE and
not an adjective.  alpha = 0.4 is used throughout because `p_true = 1.4` sits next to the
target's own measured `p = 1.3937`, so the probes live at the target's own difficulty.
"""

import json
import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.hl_rescaled import sinh_grid_origin
from solver.target_norm import (
    analytic_tail, calibration_family, coefficient_magnitudes, compactify,
    fit_exponent, norm_verdict, spectrum, weighted_partial_sums,
)

ALPHA = 0.4
P_TRUE = 1.0 + ALPHA
TAIL_EXPONENT = -ALPHA          # far field |X|^-alpha, the honest closure
N_GRID = 801
M = 16384
K_LO, K_HI = 32, 256

# The window named by capabilities.py.  It is written here, in THIS file, precisely
# because the module under audit does not contain it as a constant anywhere.
X_MAX_VALIDATED_FLOOR = 745.0


def _record(fn, *a, **kw):
    """Call `fn`, returning (value, exception_repr, [warning messages])."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            val, exc = fn(*a, **kw), None
        except Exception as e:                                   # noqa: BLE001
            val, exc = None, f"{type(e).__name__}: {e}"
        return val, exc, [str(x.message) for x in w]


def _keys_naming_violation(obj):
    """Field names in `obj` that a caller could read as a domain-violation signal.

    Deliberately generous: ANY key containing one of these stems counts as a signal, so
    the count is an upper bound on what the module offers, not a strict reading.
    """
    stems = ("outside", "domain", "trust", "valid", "warn", "flag", "extrapol",
             "x_max", "xmax", "window", "clip", "guard")
    if not isinstance(obj, dict):
        return []
    return sorted(k for k in obj if any(s in k.lower() for s in stems))


# --------------------------------------------------------------------------
# PROBE 1 -- the X_max ladder, straddling the validated floor
# --------------------------------------------------------------------------
def probe_domain_ladder():
    """Walk X_max from far inside the untrustworthy region up past the headline domain.

    For each rung: how many of the M theta-samples fall outside the data, how wrong the
    silently-returned exponent is against the exact p = 1.4, and what the module said.
    """
    rungs = []
    for rho_max in (4.0, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0):
        _, X = sinh_grid_origin(N_GRID, rho_max=rho_max)
        X_max = float(np.abs(X).max())
        f = calibration_family(X, ALPHA)

        sp, exc, warned = _record(spectrum, X, f, M=M, far_field="power",
                                  tail_exponent=TAIL_EXPONENT)
        fit, fexc, fwarned = _record(fit_exponent, sp["k"], sp["hk"], K_LO, K_HI)

        rungs.append({
            "rho_max": rho_max,
            "X_max": X_max,
            "inside_validated_window": bool(X_max >= X_MAX_VALIDATED_FLOOR),
            "n_theta_samples_outside_data": int(sp["n_outside_grid"]),
            "frac_theta_samples_outside_data": float(sp["n_outside_grid"] / M),
            "p_returned": float(fit["p"]),
            "p_true": P_TRUE,
            "abs_exponent_error": float(abs(fit["p"] - P_TRUE)),
            "r2_of_the_bad_fit": float(fit["r2"]),
            "spectrum_raised": exc,
            "spectrum_warnings": warned,
            "fit_raised": fexc,
            "fit_warnings": fwarned,
            "spectrum_keys": sorted(sp.keys()),
            "spectrum_keys_naming_violation": _keys_naming_violation(sp),
            "fit_keys": sorted(fit.keys()),
            "fit_keys_naming_violation": _keys_naming_violation(fit),
        })
    return {"what": ("X_max = 1.4e+01 .. 4.1e+04 at fixed n = 801, M = 16384, on the "
                     "known-answer calibration family alpha = 0.4 (p = 1.4 exactly)"),
            "rungs": rungs}


# --------------------------------------------------------------------------
# PROBE 2 -- the far-field closure, where the caller cannot see it fire
# --------------------------------------------------------------------------
def probe_closure_ablation():
    """power / clamp / zero at the shipped X_max = 745 and at the headline 4.1e+04.

    capabilities.py says the closure "moves the exponent by 0.190" at 745.  The point
    here is not the spread -- leg 55 owns that -- it is that the spread is invisible to a
    caller who ran only one of the three, because all three return the same shape of
    object with the same keys and no indication that the choice mattered.
    """
    out = []
    for rho_max in (8.0, 12.0):
        _, X = sinh_grid_origin(N_GRID, rho_max=rho_max)
        X_max = float(np.abs(X).max())
        f = calibration_family(X, ALPHA)
        ps, keysets, msgs = {}, {}, {}
        for mode in ("power", "clamp", "zero"):
            sp, exc, warned = _record(spectrum, X, f, M=M, far_field=mode,
                                      tail_exponent=TAIL_EXPONENT)
            fit = fit_exponent(sp["k"], sp["hk"], K_LO, K_HI)
            ps[mode] = float(fit["p"])
            keysets[mode] = sorted(sp.keys())
            msgs[mode] = {"raised": exc, "warnings": warned}
        vals = list(ps.values())
        out.append({
            "X_max": X_max,
            "inside_validated_window": bool(X_max >= X_MAX_VALIDATED_FLOOR),
            "n_theta_samples_outside_data": int(
                compactify(X, f, M, far_field="power", tail_exponent=TAIL_EXPONENT)[2]),
            "p_by_closure": ps,
            "closure_spread_in_p": float(max(vals) - min(vals)),
            "worst_abs_error_vs_truth": float(max(abs(v - P_TRUE) for v in vals)),
            "all_three_return_identical_key_sets": bool(
                keysets["power"] == keysets["clamp"] == keysets["zero"]),
            "signals": msgs,
        })
    return {"what": ("power/clamp/zero at the shipped domain and at the headline domain; "
                     "the ablation's own magnitude is leg 55's, the KEY SETS are this "
                     "leg's"),
            "domains": out}


# --------------------------------------------------------------------------
# PROBE 3 -- the downstream surface: does the violation propagate at all?
# --------------------------------------------------------------------------
def probe_downstream_propagation():
    """Feed an exponent measured INSIDE the untrustworthy region to the norm verdict.

    `norm_verdict` and `analytic_tail` are the functions whose output a caller would
    actually quote ("the norm is finite at s = 0.3, margin +0.094").  Neither takes the
    spectrum, so neither can see `n_outside_grid`; the audit is whether their returned
    dicts carry any provenance at all, and how far the verdict moves between the
    untrustworthy domain and the headline domain.

    THE CLOSURE USED AT 745 IS "clamp", AND THAT CHOICE IS PART OF THE PROBE.  The
    calibration family's far field is EXACTLY a power law, so `far_field="power"` with the
    matching `tail_exponent` continues it exactly and the domain violation costs almost
    nothing (7.4e-08 in p, measured, and reported below as `power_closure_control`).  That
    is the kindest possible case and it would flatter the module.  A caller inside the
    untrustworthy region does not know the true tail exponent -- that is what "not
    trustworthy" means -- so the probe is run with the closure such a caller can actually
    reach without extra knowledge.
    """
    fits = {}
    for label, rho_max, mode in (("untrustworthy_745", 8.0, "clamp"),
                                 ("headline_41000", 12.0, "power")):
        _, X = sinh_grid_origin(N_GRID, rho_max=rho_max)
        f = calibration_family(X, ALPHA)
        sp = spectrum(X, f, M=M, far_field=mode, tail_exponent=TAIL_EXPONENT)
        fit = fit_exponent(sp["k"], sp["hk"], K_LO, K_HI)
        fits[label] = {"X_max": float(np.abs(X).max()),
                       "n_outside": int(sp["n_outside_grid"]),
                       "p": float(fit["p"]), "C": float(fit["C"]),
                       "k": sp["k"], "hk": sp["hk"]}

    # the kind case, kept as a control so the probe cannot be read as cherry-picking
    _, Xc = sinh_grid_origin(N_GRID, rho_max=8.0)
    sp_c = spectrum(Xc, calibration_family(Xc, ALPHA), M=M, far_field="power",
                    tail_exponent=TAIL_EXPONENT)
    p_power_745 = float(fit_exponent(sp_c["k"], sp_c["hk"], K_LO, K_HI)["p"])

    rows = []
    for s in (0.0, 0.3, 0.39, 0.45, 0.5, 1.0):
        v_bad = norm_verdict(fits["untrustworthy_745"]["p"], s)
        v_good = norm_verdict(fits["headline_41000"]["p"], s)
        t_bad = analytic_tail(fits["untrustworthy_745"]["p"],
                              fits["untrustworthy_745"]["C"], 512, s)
        rows.append({
            "s": s,
            "margin_from_untrustworthy_domain": v_bad["margin_in_exponent_units"],
            "margin_from_headline_domain": v_good["margin_in_exponent_units"],
            "margin_shift": float(v_bad["margin_in_exponent_units"]
                                  - v_good["margin_in_exponent_units"]),
            "verdict_flips_between_domains": bool(v_bad["finite"] != v_good["finite"]),
            "norm_verdict_keys": sorted(v_bad.keys()),
            "norm_verdict_keys_naming_violation": _keys_naming_violation(v_bad),
            "analytic_tail_keys": sorted(t_bad.keys()),
            "analytic_tail_keys_naming_violation": _keys_naming_violation(t_bad),
        })

    ps_bad = weighted_partial_sums(fits["untrustworthy_745"]["k"],
                                  fits["untrustworthy_745"]["hk"], 0.3, [64, 512])
    return {
        "what": ("an exponent fitted where capabilities.py says the measurement is not "
                 "trustworthy, pushed through the functions a caller quotes"),
        "p_untrustworthy": fits["untrustworthy_745"]["p"],
        "p_headline": fits["headline_41000"]["p"],
        "p_true": P_TRUE,
        "exponent_shift_between_domains": float(abs(fits["untrustworthy_745"]["p"]
                                                    - fits["headline_41000"]["p"])),
        "n_outside_untrustworthy": fits["untrustworthy_745"]["n_outside"],
        "n_outside_headline": fits["headline_41000"]["n_outside"],
        "rows": rows,
        "power_closure_control": {
            "what": ("the same domain violation with the closure that happens to be "
                     "exactly right for this object -- the kindest case"),
            "p_at_745_power_closure": p_power_745,
            "abs_error_vs_truth": float(abs(p_power_745 - P_TRUE)),
        },
        "verdict_flip_window_in_s": {
            "what": ("weights s for which the untrustworthy domain reports the norm "
                     "FINITE and the headline domain reports it DIVERGENT -- "
                     "(p_head - 1, p_bad - 1)"),
            "lo": float(fits["headline_41000"]["p"] - 1.0),
            "hi": float(fits["untrustworthy_745"]["p"] - 1.0),
            "width": float(fits["untrustworthy_745"]["p"]
                           - fits["headline_41000"]["p"]),
        },
        "weighted_partial_sums_keys": sorted(ps_bad[0].keys()),
        "weighted_partial_sums_keys_naming_violation": _keys_naming_violation(ps_bad[0]),
    }


# --------------------------------------------------------------------------
# PROBE 4 -- absurd but accepted inputs
# --------------------------------------------------------------------------
def probe_absurd_inputs():
    """Inputs no honest caller means, split into the ones that raise and the ones that do
    not.  This is where the module's REAL guard surface is counted."""
    _, X = sinh_grid_origin(N_GRID, rho_max=8.0)
    f = calibration_family(X, ALPHA)
    cases = []

    def add(name, kind, fn, *a, **kw):
        val, exc, warned = _record(fn, *a, **kw)
        num = None
        if isinstance(val, dict) and "p" in val:
            num = float(val["p"])
        elif isinstance(val, dict) and "hk" in val:
            num = float(np.max(val["hk"]))
        cases.append({"name": name, "hazard_kind": kind, "raised": exc,
                      "warnings": warned, "returned_a_number": bool(exc is None),
                      "value": num,
                      "keys_naming_violation": _keys_naming_violation(val)})

    # -- DOMAIN hazards: the caller has left the validated window ------------------
    _, X_short = sinh_grid_origin(N_GRID, rho_max=4.0)
    add("grid 55x shorter than validated (X_max = 1.4e+01)", "domain",
        spectrum, X_short, calibration_family(X_short, ALPHA),
        M=M, far_field="power", tail_exponent=TAIL_EXPONENT)
    add("shipped domain X_max = 745, the region called untrustworthy", "domain",
        spectrum, X, f, M=M, far_field="power", tail_exponent=TAIL_EXPONENT)
    add("clamp closure at 745 (injects alpha = 0)", "domain",
        spectrum, X, f, M=M, far_field="clamp")
    add("zero closure at 745 (injects a jump)", "domain",
        spectrum, X, f, M=M, far_field="zero")
    add("GROWING far field, tail_exponent = +3", "domain",
        spectrum, X, f, M=M, far_field="power", tail_exponent=+3.0)
    add("tail_exponent contradicting the data, -5 for an alpha = 0.4 profile", "domain",
        spectrum, X, f, M=M, far_field="power", tail_exponent=-5.0)
    add("M = 65536 on X_max = 745: 4x more samples outside the data", "domain",
        spectrum, X, f, M=65536, far_field="power", tail_exponent=TAIL_EXPONENT)
    add("fit band k = 512..4096, entirely above X_max/2 = 372", "domain",
        fit_exponent, *(lambda sp: (sp["k"], sp["hk"]))(
            spectrum(X, f, M=M, far_field="power", tail_exponent=TAIL_EXPONENT)),
        512, 4096)

    # -- ARGUMENT hazards: the guards that DO exist -------------------------------
    add("mismatched X and f shapes", "argument", compactify, X, f[:-1], M)
    add("far_field='power' without tail_exponent", "argument",
        compactify, X, f, M, far_field="power")
    add("unknown far_field='hope'", "argument", compactify, X, f, M, far_field="hope")
    add("far_field='none' leaves NaN, then FFT", "argument",
        lambda: coefficient_magnitudes(
            compactify(X, f, M, far_field="none")[1]))

    n_dom = [c for c in cases if c["hazard_kind"] == "domain"]
    n_arg = [c for c in cases if c["hazard_kind"] == "argument"]
    return {
        "what": "12 adversarial calls: 8 domain hazards, 4 argument hazards",
        "cases": cases,
        "n_domain_hazards": len(n_dom),
        "n_domain_hazards_that_raised": sum(1 for c in n_dom if c["raised"]),
        "n_domain_hazards_that_warned": sum(1 for c in n_dom if c["warnings"]),
        "n_domain_hazards_returning_a_number_silently": sum(
            1 for c in n_dom if not c["raised"] and not c["warnings"]),
        "n_argument_hazards": len(n_arg),
        "n_argument_hazards_that_raised": sum(1 for c in n_arg if c["raised"]),
    }


# --------------------------------------------------------------------------
# PROBE 5 -- the API surface, counted
# --------------------------------------------------------------------------
def probe_api_surface():
    """Which of the module's result-bearing entry points can carry a domain signal AT
    ALL, by their return type -- independent of any particular input."""
    _, X = sinh_grid_origin(N_GRID, rho_max=8.0)
    f = calibration_family(X, ALPHA)
    sp = spectrum(X, f, M=M, far_field="power", tail_exponent=TAIL_EXPONENT)
    fit = fit_exponent(sp["k"], sp["hk"], K_LO, K_HI)

    surfaces = [
        {"fn": "compactify", "returns": "tuple(theta, h, n_outside)",
         "carries_domain_diagnostic": True,
         "diagnostic": "third element: raw count of samples outside the data",
         "compared_against_a_threshold": False},
        {"fn": "spectrum", "returns": "dict",
         "carries_domain_diagnostic": "n_outside_grid" in sp,
         "diagnostic": "key 'n_outside_grid': raw count",
         "compared_against_a_threshold": False},
        {"fn": "coefficient_magnitudes", "returns": "tuple(k, hk, hk_real)",
         "carries_domain_diagnostic": False, "diagnostic": None,
         "compared_against_a_threshold": False},
        {"fn": "fit_exponent", "returns": "dict",
         "carries_domain_diagnostic": bool(_keys_naming_violation(fit)),
         "diagnostic": None, "compared_against_a_threshold": False},
        {"fn": "weighted_partial_sums", "returns": "list[dict]",
         "carries_domain_diagnostic": False, "diagnostic": None,
         "compared_against_a_threshold": False},
        {"fn": "analytic_tail", "returns": "dict",
         "carries_domain_diagnostic": False, "diagnostic": None,
         "compared_against_a_threshold": False},
        {"fn": "norm_verdict", "returns": "dict",
         "carries_domain_diagnostic": False, "diagnostic": None,
         "compared_against_a_threshold": False},
        {"fn": "noise_floor", "returns": "float",
         "carries_domain_diagnostic": False, "diagnostic": None,
         "compared_against_a_threshold": False},
    ]
    result_bearing = [s for s in surfaces if s["fn"] in
                      ("coefficient_magnitudes", "fit_exponent", "weighted_partial_sums",
                       "analytic_tail", "norm_verdict", "noise_floor")]
    return {
        "what": "the module's result-bearing entry points, by whether a signal can reach them",
        "surfaces": surfaces,
        "n_surfaces": len(surfaces),
        "n_carrying_any_domain_diagnostic": sum(
            1 for s in surfaces if s["carries_domain_diagnostic"]),
        "n_comparing_it_to_a_threshold": sum(
            1 for s in surfaces if s["compared_against_a_threshold"]),
        "n_exponent_or_norm_bearing": len(result_bearing),
        "n_exponent_or_norm_bearing_carrying_a_diagnostic": sum(
            1 for s in result_bearing if s["carries_domain_diagnostic"]),
    }


# --------------------------------------------------------------------------
def main():
    np.seterr(all="ignore")
    out = {
        "leg": 84,
        "route": "TNA",
        "gate": ("Under adversarial inputs that push sample points beyond the validated "
                 "X_max = 745 window (or otherwise into the region capabilities.py "
                 "already flags as untrustworthy), does target_norm.py silently return a "
                 "result with no warning or flag, or does it correctly signal the domain "
                 "violation?"),
        "capabilities_line_audited": (
            "DOMAIN-limited, not resolution-limited: at the shipped X_max = 745 the "
            "far-field closure moves the exponent by 0.190 and the measurement is not "
            "trustworthy there; the headline is taken where no sample point leaves the grid"),
        "known_answer_object": ("calibration_family alpha = 0.4, p = 1 + alpha = 1.4 "
                                "exactly"),
        "domain_ladder": probe_domain_ladder(),
        "closure_ablation": probe_closure_ablation(),
        "downstream_propagation": probe_downstream_propagation(),
        "absurd_inputs": probe_absurd_inputs(),
        "api_surface": probe_api_surface(),
    }

    lad = out["domain_ladder"]["rungs"]
    crossed = [r for r in lad if r["n_theta_samples_outside_data"] > 0]
    ai = out["absurd_inputs"]
    api = out["api_surface"]
    abl = out["closure_ablation"]["domains"][0]        # the shipped X_max = 745
    dn = out["downstream_propagation"]
    out["headline"] = {
        "n_ladder_rungs": len(lad),
        "n_ladder_rungs_crossing_the_window": len(crossed),
        "n_crossings_that_warned_or_raised": sum(
            1 for r in crossed if r["spectrum_warnings"] or r["spectrum_raised"]
            or r["fit_warnings"] or r["fit_raised"]),
        "worst_silent_exponent_error_matched_closure": max(
            r["abs_exponent_error"] for r in crossed),
        "worst_silent_exponent_error_any_closure_at_745":
            abl["worst_abs_error_vs_truth"],
        "closure_spread_in_p_at_745": abl["closure_spread_in_p"],
        "n_samples_outside_at_745": abl["n_theta_samples_outside_data"],
        "frac_samples_outside_at_745": float(abl["n_theta_samples_outside_data"] / M),
        "verdict_flip_window_width_in_s":
            dn["verdict_flip_window_in_s"]["width"],
        "worst_silent_r2": min(r["r2_of_the_bad_fit"] for r in crossed),
        "max_frac_samples_outside_data": max(
            r["frac_theta_samples_outside_data"] for r in crossed),
        "n_domain_hazards_silent": ai["n_domain_hazards_returning_a_number_silently"],
        "n_domain_hazards": ai["n_domain_hazards"],
        "n_argument_hazards_that_raised": ai["n_argument_hazards_that_raised"],
        "n_argument_hazards": ai["n_argument_hazards"],
        "n_exponent_bearing_surfaces_with_a_diagnostic":
            api["n_exponent_or_norm_bearing_carrying_a_diagnostic"],
        "n_exponent_bearing_surfaces": api["n_exponent_or_norm_bearing"],
        "n_surfaces_comparing_a_diagnostic_to_a_threshold":
            api["n_comparing_it_to_a_threshold"],
    }
    hd = out["headline"]
    out["gate_answer"] = ("YES_SILENT" if hd["n_crossings_that_warned_or_raised"] == 0
                          and hd["n_domain_hazards_silent"] == hd["n_domain_hazards"]
                          else "NO_FLAGS_CORRECTLY")

    def _clean(o):
        if isinstance(o, dict):
            return {k: _clean(v) for k, v in o.items() if not isinstance(v, np.ndarray)}
        if isinstance(o, list):
            return [_clean(v) for v in o]
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        return o

    out = _clean(out)
    dest = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "writeup", "data", "p2_route_tna_v1_domain_audit.json")
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=False)

    print("ROUTE-TNA leg 84 -- domain-guard audit of solver/target_norm.py")
    print(f"  ladder rungs crossing the validated window : "
          f"{hd['n_ladder_rungs_crossing_the_window']} of {hd['n_ladder_rungs']}")
    print(f"  of those, warning or exception raised      : "
          f"{hd['n_crossings_that_warned_or_raised']}")
    print(f"  worst silent p-error, matched closure      : "
          f"{hd['worst_silent_exponent_error_matched_closure']:.4f} "
          f"(r^2 {hd['worst_silent_r2']:.4f})")
    print(f"  worst silent p-error at 745, any closure   : "
          f"{hd['worst_silent_exponent_error_any_closure_at_745']:.4f} "
          f"(spread {hd['closure_spread_in_p_at_745']:.4f} from "
          f"{hd['n_samples_outside_at_745']} of {M} samples, "
          f"{100 * hd['frac_samples_outside_at_745']:.3f}%)")
    print(f"  silent FINITE-vs-DIVERGENT window in s     : "
          f"width {hd['verdict_flip_window_width_in_s']:.4f}")
    print(f"  max fraction of samples outside the data   : "
          f"{hd['max_frac_samples_outside_data']:.4f}")
    print(f"  domain hazards silently returning a number : "
          f"{hd['n_domain_hazards_silent']} of {hd['n_domain_hazards']}")
    print(f"  argument hazards that raised               : "
          f"{hd['n_argument_hazards_that_raised']} of {hd['n_argument_hazards']}")
    print(f"  exponent-bearing surfaces with a diagnostic: "
          f"{hd['n_exponent_bearing_surfaces_with_a_diagnostic']} of "
          f"{hd['n_exponent_bearing_surfaces']}")
    print(f"  GATE ANSWER: {out['gate_answer']}")
    print(f"  wrote {dest}")


if __name__ == "__main__":
    main()
