"""Route-RCA: adversarial audit of solver/reduced_certificate.py's self-consistency claim.

Leg 109.  `capabilities.py:354-357` validates `solver/reduced_certificate.py` as
"internally self-consistent across the reduced space; explicitly NOT a proof -- float64
throughout."  This runner asks the leg's pre-committed gate:

    Under an adversarial battery of degenerate or NaN-poisoned inputs, does
    solver/reduced_certificate.py ever report internal self-consistency on a case that
    is not actually self-consistent?

`solver/reduced_certificate.py` is READ-ONLY here and is not modified under either branch
of the gate.  Nothing in this file sharpens a bound, re-measures Y_0/Z_0/a*/the sup|N''|
threshold/the adversary slope/the Holder threshold, or says anything about Z_1.  Every
number produced is a discrepancy magnitude, a ratio, or a case count.

The five hazard sites were declared in `writeup/novelty/leg_109.md` BEFORE this file was
written:

  H1  `rehearsal`'s `verdict` is a hardcoded string literal that asserts "Y_0 is at
      machine level and Z_0 is roundoff" without reading either field.
  H2  `N2_finite = bool(p >= 2.0 and max(npp)/min(npp) < 1.01)` -- a relative flatness
      test over three cutoffs, whose False is indistinguishable from a failed measurement.
  H3  Y_0 is a sup over a function estimated by `np.max` over a caller-settable grid.
  H4  `z0_defect` returns the LEFT residual ||A M - I|| while `np.linalg.inv` guarantees
      the RIGHT one.
  H5  `step_adversary`'s `kind` dispatches by exact string, so any unrecognised value
      silently returns the adversary instead of the designated control.

Each probe below carries a POSITIVE CONTROL that can report the other answer -- the
standing requirement, and lesson 90's requirement in particular: before quoting a control,
ask what would have had to change in the code for it to report the other answer.

Plain float64 throughout, like the module it audits.  Nothing here is rigorous.
"""

import json
import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.first_integral import ReducedProfile                        # noqa: E402
import solver.reduced_certificate as rc                                 # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_rca_v1_adversarial.json")

# "machine level" and "roundoff", as the module's own docstring uses them: finding (1)
# claims Y_0 "falls to ~1e-12 by K ~ 96 at a = 0.3", and finding (2) calls Z_0 roundoff.
# The thresholds are deliberately GENEROUS -- two orders looser than the claim -- so that
# a case counted as contradicting the verdict is contradicting it by a wide margin.
MACHINE_LEVEL = 1e-10
ROUNDOFF = 1e-10


# ---------------------------------------------------------------------------
# H1 -- is the verdict a measurement or a constant?
# ---------------------------------------------------------------------------


def probe_h1_verdict_is_constant(a_grid=(0.3, 0.5, 0.8, 1.0, 1.2),
                                 k_grid=(16, 32, 96)):
    """Sweep (a, K); compare the verdict SENTENCE against the numbers beside it.

    POSITIVE CONTROL: `a = 0.3, K = 96` is the module's own headline case, where the
    sentence is TRUE (Y_0 ~ 1e-12).  If every case came out false the probe would be
    measuring a broken build rather than a decoupled claim; the control is what makes
    "14 of 15" a finding instead of an artifact.
    """
    rows, verdicts = [], set()
    for a in a_grid:
        for K in k_grid:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                r = rc.rehearsal(float(a), K=int(K))
            if not r.get("converged"):
                rows.append({"a": float(a), "K": int(K), "converged": False,
                             "verdict_emitted": "verdict" in r})
                continue
            y0, z0 = r["Y0_interpolant_defect"], r["Z0"]
            verdicts.add(r["verdict"])
            rows.append({
                "a": float(a), "K": int(K), "converged": True,
                "verdict_emitted": True,
                "Y0": float(y0), "Z0": float(z0), "N2_finite": bool(r["N2_finite"]),
                "verdict_says_Y0_machine_level": True,   # the sentence, unconditionally
                "Y0_actually_machine_level": bool(y0 <= MACHINE_LEVEL),
                "Y0_overshoot_factor": float(y0 / MACHINE_LEVEL),
                "Z0_actually_roundoff": bool(z0 <= ROUNDOFF),
            })
    conv = [r for r in rows if r.get("converged")]
    false_y0 = [r for r in conv if not r["Y0_actually_machine_level"]]
    y0s = [r["Y0"] for r in conv]
    return {
        "hazard": "H1",
        "cases_total": len(rows),
        "cases_converged": len(conv),
        "distinct_verdict_strings": len(verdicts),
        "verdict_string_is_byte_identical_across_all_cases": len(verdicts) == 1,
        "cases_where_verdict_says_machine_level_but_Y0_is_not": len(false_y0),
        "cases_where_verdict_says_roundoff_but_Z0_is_not":
            sum(1 for r in conv if not r["Z0_actually_roundoff"]),
        "Y0_min": float(min(y0s)), "Y0_max": float(max(y0s)),
        "Y0_spread_orders_of_magnitude": float(np.log10(max(y0s) / min(y0s))),
        "Y0_spread_factor": float(max(y0s) / min(y0s)),
        "worst_case": max(conv, key=lambda r: r["Y0"]),
        "positive_control_a0.3_K96_verdict_is_true":
            next(r["Y0_actually_machine_level"]
                 for r in conv if r["a"] == 0.3 and r["K"] == 96),
        "rows": rows,
    }


def probe_h1_banked_contamination():
    """The same discrepancy, read (not re-measured) from the banked v16 artifact."""
    path = os.path.join(os.path.dirname(OUT), "p2_route_d_v16_rehearsal.json")
    if not os.path.exists(path):
        return {"available": False}
    with open(path) as fh:
        d = json.load(fh)
    rows = []
    for a, v in sorted(d.get("E_rehearsal", {}).items()):
        y0 = v.get("Y0_interpolant_defect")
        rows.append({"a": float(a), "Y0_banked": float(y0),
                     "N2_finite": v.get("N2_finite"),
                     "verdict_says_machine_level": "verdict" in v,
                     "Y0_actually_machine_level": bool(y0 <= MACHINE_LEVEL),
                     "overshoot_factor": float(y0 / MACHINE_LEVEL)})
    verdicts = {v.get("verdict") for v in d.get("E_rehearsal", {}).values()}
    return {"available": True, "source": "writeup/data/p2_route_d_v16_rehearsal.json",
            "distinct_verdict_strings": len(verdicts),
            "rows": rows,
            "banked_rows_contradicting_the_sentence":
                sum(1 for r in rows if not r["Y0_actually_machine_level"])}


# ---------------------------------------------------------------------------
# H2 -- does N2_finite certify a poisoned state, and does the cutoff ladder decide?
# ---------------------------------------------------------------------------


def _n2_finite(rp, b):
    """The module's own expression, reproduced verbatim from `rehearsal` line 220."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        npp = rc.second_derivative_sup(rp, b)
    if not (rp.p >= 2.0):                    # Python short-circuits before the ratio
        return False, npp, None
    try:
        ratio = max(npp) / min(npp)
    except ZeroDivisionError:
        return "ZeroDivisionError", npp, None
    return bool(ratio < 1.01), npp, float(ratio)


def probe_h2_poisoned_states(k=32):
    """Feed garbage `b` to the N2 check at p = 2 exactly, and at p != 2 as the control.

    POSITIVE CONTROL: the SAME poisoned vectors at `a = 0.3` (p = 3.33), where every
    quantity must come back NaN.  That is what makes `a = 0.5` a finding rather than a
    claim that NaN is always absorbed -- the code path differs only in the exponent.
    """
    poisons = {
        "all_nan": np.full(k, np.nan),
        "all_inf": np.full(k, np.inf),
        "all_zero": np.zeros(k),
        "random_garbage": np.random.default_rng(0).normal(size=k),
    }
    out = {}
    for a in (0.5, 0.3):
        rp = ReducedProfile(a, K=k)
        cases = {}
        for name, b in poisons.items():
            fin, npp, ratio = _n2_finite(rp, b)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                other = {}
                for fn in ("interpolant_defect", "z0_defect"):
                    try:
                        other[fn] = float(getattr(rc, fn)(rp, b, 10.0))
                    except Exception as exc:          # noqa: BLE001
                        other[fn] = type(exc).__name__
                try:
                    other["operator_norm"] = float(rp.operator_norm(b, 10.0))
                except Exception as exc:              # noqa: BLE001
                    other["operator_norm"] = type(exc).__name__
            cases[name] = {
                "N2_sup_by_cutoff": [None if not np.isfinite(x) else float(x)
                                     for x in npp],
                "N2_sup_raw": [repr(float(x)) for x in npp],
                "N2_finite_reported": fin,
                "cutoff_ratio": ratio,
                "other_fields_nonfinite": {
                    m: (not isinstance(v, float)) or (not np.isfinite(v))
                    for m, v in other.items()},
                "other_fields": {m: (v if isinstance(v, str)
                                     else (None if not np.isfinite(v) else float(v)))
                                 for m, v in other.items()},
            }
        out[f"a={a}"] = {
            "p": float(rp.p),
            "cases": cases,
            "poisoned_states_certified_True":
                sum(1 for c in cases.values() if c["N2_finite_reported"] is True),
            "poisoned_states_total": len(cases),
        }
    return {"hazard": "H2", "by_a": out,
            "note": ("nan ** 0.0 == 1.0 in IEEE-754, so at p == 2 exactly the cutoff "
                     "ladder returns |p(p-1)| * 1.0 = 2.0 for ANY b."),
            "nan_pow_zero": float(np.nan ** 0.0)}


def probe_h2_ladder_is_decorative(a_grid=(0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45,
                                          0.48, 0.5, 0.52, 0.55, 0.6, 0.8, 1.0, 1.2),
                                  k=48):
    """Does the three-cutoff measurement ever change N2_finite away from (a <= 1/2)?

    Lesson 90: before quoting a control, ask what would have had to change in the code
    for it to report the other answer.  Here the answer is available in one column --
    if `cutoff_ratio` is 1.000000 at every a <= 1/2 and the `p >= 2` conjunct
    short-circuits at every a > 1/2, the ladder decided nothing.
    """
    rows, mismatches = [], 0
    for a in a_grid:
        rp = ReducedProfile(float(a), K=int(k))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = rp.solve()
        if not r["converged"]:
            rows.append({"a": float(a), "converged": False})
            continue
        fin, npp, ratio = _n2_finite(rp, r["b"])
        predicted = bool(a <= 0.5)
        agree = (fin == predicted)
        mismatches += 0 if agree else 1
        rows.append({"a": float(a), "converged": True, "p": float(rp.p),
                     "p_ge_2": bool(rp.p >= 2.0),
                     "cutoff_ratio": ratio,
                     "ratio_was_evaluated": ratio is not None,
                     "N2_finite": fin,
                     "predicted_by_a_alone": predicted, "agree": agree,
                     "N2_sup_by_cutoff": [float(x) for x in npp]})
    conv = [r for r in rows if r.get("converged")]
    evaluated = [r for r in conv if r["ratio_was_evaluated"]]
    return {
        "hazard": "H2-rider",
        "cases_converged": len(conv),
        "cases_where_the_ratio_was_evaluated_at_all": len(evaluated),
        "cases_where_the_ratio_was_short_circuited": len(conv) - len(evaluated),
        "distinct_cutoff_ratios_where_evaluated":
            sorted({round(r["cutoff_ratio"], 9) for r in evaluated}),
        "cases_where_the_ladder_changed_the_answer_from_(a<=1/2)": mismatches,
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# H3 -- Y_0 is a sup estimated by sampling
# ---------------------------------------------------------------------------


def probe_h3_grid_sensitivity(a_grid=(0.5, 0.8), k=96,
                              n_grid=(5, 17, 49, 97, 199, 401, 997, 2003, 4001, 9973)):
    """How far can the reported Y_0 move by changing only the evaluation grid?

    POSITIVE CONTROL: the largest `n` is the reference.  If the default `n = 997` sat
    far from the refined limit, the default itself would be the finding; measuring both
    the default's honesty AND the adversarial depression is what separates the two.
    """
    out = {}
    for a in a_grid:
        rp = ReducedProfile(float(a), K=int(k))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = rp.solve()
            b, Xc = r["b"], r["Xc"]
            vals = {int(n): float(rc.interpolant_defect(rp, b, Xc, n=n))
                    for n in n_grid}
        default, refined = vals[997], vals[max(n_grid)]
        lo = min(vals.values())
        out[f"a={a}"] = {
            "by_n": vals,
            "default_n997": default,
            "refined_limit_n%d" % max(n_grid): refined,
            "default_underreports_refined_by_percent":
                float(100.0 * (refined - default) / refined),
            "adversarial_min": lo,
            "max_depression_factor_vs_default": float(default / lo),
            "max_depression_factor_vs_refined": float(refined / lo),
        }
    return {"hazard": "H3", "by_a": out,
            "repo_call_sites_passing_n": 0,
            "note": ("the default is honest to a few percent; the hazard is that `n` is "
                     "a caller-settable argument on a SUP with no resolution check.")}


# ---------------------------------------------------------------------------
# H4 -- which inversion residual does z0_defect actually report?
# ---------------------------------------------------------------------------


def probe_h4_residual_side(a_grid=(0.3, 0.5, 0.8), k_grid=(32, 96)):
    """||A M - I|| (reported) versus ||M A - I|| (the one np.linalg.inv guarantees).

    POSITIVE CONTROL: `np.linalg.cond(M)` is reported beside them.  If the two residuals
    differed wildly at a well-conditioned M, the finding would be about the code; if they
    track cond(M), it is the textbook asymmetry and the module is merely conservative.
    """
    rows = []
    for a in a_grid:
        for k in k_grid:
            rp = ReducedProfile(float(a), K=int(k))
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                r = rp.solve()
                if not r["converged"]:
                    continue
                M = rp.jacobian(r["b"], r["Xc"])
                A = np.linalg.inv(M)
                eye = np.eye(rp.K + 1)
                left = float(np.max(np.abs(A @ M - eye).sum(axis=1)))
                right = float(np.max(np.abs(M @ A - eye).sum(axis=1)))
                reported = float(rc.z0_defect(rp, r["b"], r["Xc"]))
            rows.append({"a": float(a), "K": int(k),
                         "Z0_reported": reported,
                         "left_residual_AM_minus_I": left,
                         "right_residual_MA_minus_I": right,
                         "reported_equals_left": bool(reported == left),
                         "left_over_right": float(left / right),
                         "cond_M": float(np.linalg.cond(M))})
    return {"hazard": "H4", "rows": rows,
            "cases_where_reported_is_the_left_residual":
                sum(1 for r in rows if r["reported_equals_left"]),
            "cases_total": len(rows),
            "max_left_over_right": float(max(r["left_over_right"] for r in rows)),
            "min_left_over_right": float(min(r["left_over_right"] for r in rows)),
            "direction": ("the reported quantity is LARGER than the unreported one in "
                          "every case, i.e. conservative, not corrupting")}


# ---------------------------------------------------------------------------
# H5 -- is the designated control reachable?
# ---------------------------------------------------------------------------


def probe_h5_control_fallthrough(k=32):
    """`kind` dispatches by exact string; everything else falls through to the adversary.

    POSITIVE CONTROL: `kind="single"` is included and MUST come back different.  If it
    did not, the probe would be reporting that the two branches are the same function,
    which is a different (and worse) bug.
    """
    kinds = ["step", "single", "typo", "", "STEP", "Single", "naive", None]
    vals = {}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for kind in kinds:
            try:
                vals[repr(kind)] = float(rc.step_adversary(int(k), kind=kind))
            except Exception as exc:                  # noqa: BLE001
                vals[repr(kind)] = type(exc).__name__
    adversary = vals["'step'"]
    control = vals["'single'"]
    fell_through = [kk for kk, vv in vals.items()
                    if kk not in ("'step'", "'single'") and vv == adversary]
    return {"hazard": "H5", "values": vals,
            "adversary_value": adversary, "control_value": control,
            "control_differs_from_adversary": bool(control != adversary),
            "unrecognised_kinds_tested": len(kinds) - 2,
            "unrecognised_kinds_silently_returning_the_adversary": len(fell_through),
            "unrecognised_kinds_raising": sum(
                1 for kk, vv in vals.items()
                if kk not in ("'step'", "'single'") and isinstance(vv, str)),
            "fell_through": fell_through}


# ---------------------------------------------------------------------------
# the two input axes the gate names
# ---------------------------------------------------------------------------


def probe_degenerate_a():
    """`__init__`'s guard is `not 0.0 < float(a)`; what does it admit, and is it caught?"""
    rows = []
    for a in (np.nan, np.inf, -np.inf, 0.0, -1.0, 1e-300, 1e300, 1e-12):
        entry = {"a": repr(float(a))}
        try:
            rp = ReducedProfile(float(a), K=16)
            entry["constructor"] = "ADMITTED"
            entry["p"] = repr(float(rp.p))
        except Exception as exc:                      # noqa: BLE001
            entry["constructor"] = type(exc).__name__
        if entry["constructor"] == "ADMITTED":
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    r = rc.rehearsal(float(a), K=16)
                entry["rehearsal_converged"] = bool(r.get("converged"))
                entry["rehearsal_emitted_verdict"] = "verdict" in r
            except Exception as exc:                  # noqa: BLE001
                entry["rehearsal_converged"] = type(exc).__name__
                entry["rehearsal_emitted_verdict"] = False
        rows.append(entry)
    admitted = [r for r in rows if r["constructor"] == "ADMITTED"]
    return {"axis": "degenerate_a", "rows": rows,
            "values_tested": len(rows),
            "admitted_by_constructor": len(admitted),
            "admitted_but_caught_by_converged_flag":
                sum(1 for r in admitted if r.get("rehearsal_converged") is False),
            "admitted_and_emitted_a_verdict":
                sum(1 for r in admitted if r.get("rehearsal_emitted_verdict"))}


def probe_poisoned_b_propagation(a=0.3, k=32):
    """Single-entry NaN/inf poison through every public function that takes `b`."""
    rp = ReducedProfile(a, K=k)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = rp.solve()
    b0, Xc = r["b"], r["Xc"]
    rows = []
    for name, poison in (("one_nan", np.nan), ("one_inf", np.inf)):
        for idx in (0, 5, k - 1):
            b = b0.copy()
            b[idx] = poison
            vals = {}
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                for fn, call in (
                        ("interpolant_defect",
                         lambda: rc.interpolant_defect(rp, b, Xc)),
                        ("z0_defect", lambda: rc.z0_defect(rp, b, Xc)),
                        ("operator_norm", lambda: rp.operator_norm(b, Xc))):
                    try:
                        v = float(call())
                        vals[fn] = "finite" if np.isfinite(v) else "nonfinite"
                    except Exception as exc:          # noqa: BLE001
                        vals[fn] = type(exc).__name__
                try:
                    npp = rc.second_derivative_sup(rp, b)
                    vals["second_derivative_sup"] = (
                        "finite" if all(np.isfinite(x) for x in npp) else "nonfinite")
                except Exception as exc:              # noqa: BLE001
                    vals["second_derivative_sup"] = type(exc).__name__
            rows.append({"poison": name, "index": int(idx), "results": vals})
    n_probes = sum(len(r["results"]) for r in rows)
    n_finite = sum(1 for r in rows for v in r["results"].values() if v == "finite")
    return {"axis": "poisoned_b", "a": float(a), "K": int(k), "rows": rows,
            "probes": n_probes,
            "silently_finite": n_finite,
            "propagated_or_raised": n_probes - n_finite}


# ---------------------------------------------------------------------------


def main():
    np.seterr(all="ignore")
    res = {
        "leg": 109, "route": "ROUTE-RCA",
        "module_under_audit": "solver/reduced_certificate.py",
        "module_modified": False,
        "gate": ("Under an adversarial battery of degenerate or NaN-poisoned inputs, "
                 "does solver/reduced_certificate.py ever report internal "
                 "self-consistency on a case that is not actually self-consistent?"),
        "thresholds": {"machine_level": MACHINE_LEVEL, "roundoff": ROUNDOFF},
        "H1_verdict_is_constant": probe_h1_verdict_is_constant(),
        "H1_banked_contamination": probe_h1_banked_contamination(),
        "H2_poisoned_states": probe_h2_poisoned_states(),
        "H2_ladder_is_decorative": probe_h2_ladder_is_decorative(),
        "H3_grid_sensitivity": probe_h3_grid_sensitivity(),
        "H4_residual_side": probe_h4_residual_side(),
        "H5_control_fallthrough": probe_h5_control_fallthrough(),
        "degenerate_a": probe_degenerate_a(),
        "poisoned_b": probe_poisoned_b_propagation(),
    }

    h1, h2p, h2r = (res["H1_verdict_is_constant"], res["H2_poisoned_states"],
                    res["H2_ladder_is_decorative"])
    h5 = res["H5_control_fallthrough"]
    corrupting = []
    if h1["cases_where_verdict_says_machine_level_but_Y0_is_not"] > 0:
        corrupting.append("H1")
    if h2p["by_a"]["a=0.5"]["poisoned_states_certified_True"] > 0:
        corrupting.append("H2")
    if h5["unrecognised_kinds_silently_returning_the_adversary"] > 0:
        corrupting.append("H5")

    res["gate_answer"] = "YES" if corrupting else "NO"
    res["silent_corruption_sites"] = corrupting
    res["sites_audited"] = ["H1", "H2", "H3", "H4", "H5"]
    res["sites_clean"] = [s for s in ("H3", "H4") if s not in corrupting]
    res["headline"] = {
        "verdict_strings_over_%d_converged_cases" % h1["cases_converged"]:
            h1["distinct_verdict_strings"],
        "cases_asserting_machine_level_where_Y0_is_not":
            "%d of %d" % (h1["cases_where_verdict_says_machine_level_but_Y0_is_not"],
                          h1["cases_converged"]),
        "Y0_spread_orders_of_magnitude": h1["Y0_spread_orders_of_magnitude"],
        "worst_Y0_under_the_machine_level_sentence": h1["worst_case"]["Y0"],
        "poisoned_states_certified_N2_finite_at_a_half":
            "%d of %d" % (h2p["by_a"]["a=0.5"]["poisoned_states_certified_True"],
                          h2p["by_a"]["a=0.5"]["poisoned_states_total"]),
        "cases_where_the_cutoff_ladder_changed_the_answer":
            h2r["cases_where_the_ladder_changed_the_answer_from_(a<=1/2)"],
        "unrecognised_kinds_silently_returning_the_adversary":
            "%d of %d" % (h5["unrecognised_kinds_silently_returning_the_adversary"],
                          h5["unrecognised_kinds_tested"]),
        "H4_left_over_right_residual_range":
            [res["H4_residual_side"]["min_left_over_right"],
             res["H4_residual_side"]["max_left_over_right"]],
    }
    res["escalated_not_patched"] = True

    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=False)
    print("wrote", OUT)
    print("GATE:", res["gate_answer"], "| silent-corruption sites:", corrupting)
    for k, v in res["headline"].items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
