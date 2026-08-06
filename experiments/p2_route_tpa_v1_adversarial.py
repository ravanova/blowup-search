"""Leg 118 / Route-TPA -- adversarial audit of solver/turning_point.py.

GATE (DIRECTION.md 118, verbatim): "Under an adversarial battery (degenerate
branches, poisoned derivatives), does solver/turning_point.py ever silently return
a wrong classification instead of flagging the input?"
  yes -> Silent-corruption gap; report the exact failing case; escalate, do not patch.
  no  -> Confirmed robust; bank the battery as a permanent regression test.

solver/turning_point.py is READ-ONLY under this leg, under BOTH branches.  Nothing
here re-measures Route-D v13: not X_c, not either 1/a exponent, not ||A||, not the
cutoff ladder.  Every number produced is a returned value, a discrepancy magnitude,
or a case count.

THE OBJECT UNDER TEST IS A CLASSIFIER.  turning_point.py does not report bounds; it
reports *which mechanism is responsible* -- where the profile ends, with what
exponent, and what fraction of the extremal row's mass sits near X_c.  All of that
is defined relative to X_c EXISTING.  When E = c + aU never crosses zero (the a = 0
anchor is the canonical case, and the module's own tests run it), critical_radius
returns inf and none of those quantities has a referent.

critical_radius is consumed at THREE sites in the module (lines 100, 126, 187).
Exactly ONE carries the isfinite guard.  That asymmetry is the primary hazard AND
the leg's positive control: the guarded site proves the module CAN flag this input,
so a finite answer from an unguarded site on the SAME input is an omission, not a
design decision.

Run: .venv/bin/python experiments/p2_route_tpa_v1_adversarial.py
Writes: writeup/data/p2_route_tpa_v1_adversarial.json
"""

import json
import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.collocation_newton import (ACollocation, critical_radius,          # noqa: E402
                                       effective_speed)
from solver.turning_point import (bordered_norm, gauged_matrix,                # noqa: E402
                                  graded_norm_by_radius, homogeneous_far_field,
                                  inner_mode_exponent, log_growth_exponent,
                                  profile_far_field, solved_profile,
                                  source_of_the_row, square_bordered_smin)

ALPHA = 1.4
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_tpa_v1_adversarial.json")

# The module's OWN attribution threshold, read from test_turning_point.py line 96:
#     assert src["near_Xc_fraction"] > 0.5, src
# It is quoted, not chosen by this leg.
MODULE_ATTRIBUTION_THRESHOLD = 0.5


def _xc(col, om, c):
    """X_c exactly as all three consumer sites inside the module compute it."""
    return critical_radius(col.X, effective_speed(col.X, col.V @ om, c, col.a))


def classify(fn, *args, **kw):
    """Run one adversarial call and score it.

    FINITE    -- a finite value came back with no exception (candidate corruption;
                 whether it IS one depends on the truth, decided by the caller)
    NONFINITE -- nan/inf came back: the module declined to invent a number
    RAISED    -- an exception: the module flagged the input

    INSTRUMENT NOTE, recorded because the first run of this battery got it wrong.
    Scoring a whole returned dict conflates two different things: the module's
    HEADLINE classification and the DIAGNOSTIC keys it returns beside it.
    source_of_the_row returns {"Xc": inf, "near_Xc_fraction": 0.719, ...} at the
    a = 0 anchor -- one non-finite diagnostic and one fabricated classification.
    Scoring the dict as a whole reports NONFINITE and hides exactly the finding
    this leg exists to measure.  `field=` therefore scores a named key, and the
    whole-dict verdict is kept alongside it under "status_whole_dict" rather than
    replaced, so both readings are on the record.
    """
    field = kw.pop("_field", None)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            v = fn(*args, **kw)
        except Exception as e:                                   # noqa: BLE001
            return {"status": "RAISED", "exc": type(e).__name__,
                    "msg": str(e).splitlines()[0][:160], "value": None,
                    "field": field, "field_value": None, "n_warnings": len(w)}
        flat = np.asarray([x for x in np.atleast_1d(
            np.asarray(list(v.values()) if isinstance(v, dict) else v,
                       dtype=object)).ravel()
            if isinstance(x, (int, float, np.floating, np.integer))], dtype=float)
        whole = bool(flat.size) and bool(np.all(np.isfinite(flat)))
        fval = None
        if field is not None and isinstance(v, dict) and field in v:
            fval = float(v[field])
        status = ("FINITE" if (np.isfinite(fval) if fval is not None else whole)
                  else "NONFINITE")
        return {"status": status,
                "status_whole_dict": "FINITE" if whole else "NONFINITE",
                "exc": None, "msg": None, "field": field, "field_value": fval,
                "value": _jsonable(v), "n_warnings": len(w)}


def _jsonable(v):
    if isinstance(v, dict):
        return {k: _jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_jsonable(x) for x in v]
    if isinstance(v, (np.ndarray,)):
        a = np.asarray(v, float).ravel()
        return {"n": int(a.size), "first": float(a[0]), "last": float(a[-1]),
                "n_finite": int(np.isfinite(a).sum())}
    if isinstance(v, (float, np.floating, int, np.integer)):
        return float(v)
    return str(v)


# ---------------------------------------------------------------------------
# A.  THE MISSING GUARD -- the same input, the guarded site and the unguarded ones
# ---------------------------------------------------------------------------


def a_missing_guard(Js=(120, 200, 400)):
    """a = 0: there is NO turning point.  What does each consumer return?

    Truth is known exactly and is not a matter of tolerance: E = c + 0*U = c = 0.5
    is constant and positive at every node, so it never crosses zero, so X_c does
    not exist.  Every quantity defined relative to X_c is therefore WITHOUT A
    REFERENT (lesson 73) -- the honest return is a flag, not a number.
    """
    rows = []
    for J in Js:
        col, om, c = solved_profile(J, 0.0)
        E = effective_speed(col.X, col.V @ om, c, col.a)
        rec = {"J": J, "a": 0.0,
               "Xc_returned": float(_xc(col, om, c)),
               "E_min": float(np.min(E)), "E_max": float(np.max(E)),
               "E_sign_changes": int((np.diff(np.sign(E)) != 0).sum()),
               "guarded_site__homogeneous_far_field":
                   classify(homogeneous_far_field, col, om, c),
               "unguarded_site__source_of_the_row":
                   classify(source_of_the_row, col, om, c, ALPHA,
                            _field="near_Xc_fraction"),
               "unguarded_site__inner_mode_exponent":
                   classify(inner_mode_exponent, col, om, c)}
        rows.append(rec)
    return rows


def a2_attribution_control(a_values=(0.0, 0.2, 0.25, 0.3, 0.4), J=400):
    """near_Xc_fraction across a, INCLUDING the a = 0 control the module never runs.

    test_turning_point.py::test_5_attribution asserts near_Xc_fraction > 0.5 at
    a = 0.3 and runs an a = 0 control -- but applies the control ONLY to the
    by_cutoff ladder, never to near_Xc_fraction.  Lesson 90: a control that is not
    applied to the headline quantity is not a control of it.  This runs it.
    """
    rows = []
    for a in a_values:
        col, om, c = solved_profile(J, a)
        Xc = _xc(col, om, c)
        r = classify(source_of_the_row, col, om, c, ALPHA,
                     _field="near_Xc_fraction")
        frac = r["field_value"] if r["field_value"] is not None else float("nan")
        rows.append({"a": a, "J": J, "Xc": float(Xc),
                     "Xc_exists": bool(np.isfinite(Xc)),
                     "X_grid_max": float(col.X[-1]),
                     "near_Xc_fraction": frac,
                     "passes_module_threshold": bool(
                         np.isfinite(frac) and frac > MODULE_ATTRIBUTION_THRESHOLD),
                     "n_warnings": r["n_warnings"],
                     "status": r["status"],
                     "status_whole_dict": r.get("status_whole_dict")})
    # The comparison that IS the finding: the case with no X_c against the cases
    # that have one.  Reported as a magnitude, not a boolean.
    no_xc = [r for r in rows if not r["Xc_exists"] and np.isfinite(
        r["near_Xc_fraction"])]
    has_xc = [r for r in rows if r["Xc_exists"] and np.isfinite(
        r["near_Xc_fraction"])]
    inverted = [(r["a"], r["near_Xc_fraction"], q["a"], q["near_Xc_fraction"])
                for r in no_xc for q in has_xc
                if r["near_Xc_fraction"] > q["near_Xc_fraction"]]
    return {"rows": rows,
            "n_no_Xc_with_finite_fraction": len(no_xc),
            "n_pairs_where_no_Xc_beats_real_Xc": len(inverted),
            "inverted_pairs": inverted}


def a3_grid_too_short(a=0.2, Js=(20, 30, 40, 60, 80, 120, 200, 400)):
    """The SECOND route into the same gap, and this one has a > 0.

    X_c is a property of the profile; the grid's outer radius ~ 4J/pi is a property
    of the discretization.  The HYPOTHESIS was that a grid ending before X_c makes
    critical_radius return inf for a profile that genuinely HAS a turning point,
    giving a second route into the same gap with a > 0 and no poisoning.

    THE HYPOTHESIS WAS REFUTED and the refutation is reported, not deleted: at
    a = 0.2 the grid's outer radius exceeds X_c at every J down to 20, so this
    route does not exist.  What the sweep DID find is separate and is kept: the
    attribution fraction itself is wildly unstable in J at fixed a.
    """
    rows = []
    for J in Js:
        col, om, c = solved_profile(J, a)
        Xc = _xc(col, om, c)
        E = effective_speed(col.X, col.V @ om, c, col.a)
        r = classify(source_of_the_row, col, om, c, ALPHA,
                     _field="near_Xc_fraction")
        frac = r["field_value"] if r["field_value"] is not None else float("nan")
        rows.append({"J": J, "a": a, "X_grid_max": float(col.X[-1]),
                     "Xc": float(Xc), "Xc_exists": bool(np.isfinite(Xc)),
                     "grid_reaches_Xc": bool(float(col.X[-1]) > float(Xc)),
                     "E_min": float(np.min(E)),
                     "near_Xc_fraction": frac,
                     "passes_module_threshold": bool(
                         np.isfinite(frac) and frac > MODULE_ATTRIBUTION_THRESHOLD),
                     "guarded_site_status":
                         classify(homogeneous_far_field, col, om, c)["status"],
                     "status": r["status"]})
    fr = [r["near_Xc_fraction"] for r in rows if np.isfinite(r["near_Xc_fraction"])]
    return {"hypothesis": "a grid ending before X_c yields X_c = inf at a > 0",
            "hypothesis_refuted": all(r["grid_reaches_Xc"] for r in rows),
            "n_grids_short_of_Xc": sum(not r["grid_reaches_Xc"] for r in rows),
            "n_grids": len(rows),
            "attribution_fraction_min": min(fr) if fr else None,
            "attribution_fraction_max": max(fr) if fr else None,
            "attribution_fraction_n_exactly_zero": sum(x == 0.0 for x in fr),
            "rows": rows}


# ---------------------------------------------------------------------------
# B.  log_growth_exponent -- X_c arrives from the CALLER, unchecked
# ---------------------------------------------------------------------------


def b_caller_supplied_xc(a=0.3, J=400, factors=(0.1, 0.5, 0.9, 1.0, 1.1, 2.0, 10.0)):
    """The abscissa is log log(X/Xc).  Nothing checks the Xc the caller passes.

    h is integrated once, from the TRUE Xc, and then relabelled with a wrong one.
    The exponent that comes back is the module's headline classification (it is
    compared against 1/a with no free constant), so the magnitude by which a wrong
    Xc moves it is the magnitude by which the classification can be wrong.
    """
    col, om, c = solved_profile(J, a)
    X, h, Xc = homogeneous_far_field(col, om, c)
    true_q = log_growth_exponent(X, h, Xc)
    rows = []
    for f in factors:
        r = classify(log_growth_exponent, X, h, Xc * f)
        q = r["value"] if r["status"] == "FINITE" else float("nan")
        rows.append({"Xc_factor": f, "Xc_passed": float(Xc * f),
                     "exponent": q, "status": r["status"],
                     "abs_shift_vs_true": (abs(q - true_q)
                                           if np.isfinite(q) else float("nan")),
                     "rel_shift_vs_true": (abs(q - true_q) / abs(true_q)
                                           if np.isfinite(q) else float("nan")),
                     "within_module_gate_5pct": bool(
                         np.isfinite(q) and abs(q - 1.0 / a) / (1.0 / a) < 0.05)})
    special = {}
    for name, val in (("inf", float("inf")), ("nan", float("nan")),
                      ("zero", 0.0), ("negative", -1.0)):
        special[name] = classify(log_growth_exponent, X, h, val)
    return {"a": a, "J": J, "true_Xc": float(Xc), "true_exponent": float(true_q),
            "predicted_1_over_a": 1.0 / a, "rows": rows, "special": special}


# ---------------------------------------------------------------------------
# C.  the linear algebra -- inv() on a matrix that is singular to working precision
# ---------------------------------------------------------------------------


def c_conditioning(J=200):
    """Does the headline ladder stay plausible while cond blows up?

    graded_norm_by_radius DOES return cond and smin, so it is partly
    self-reporting.  The question is whether a caller who reads only by_cutoff --
    which is what the module's own test does -- can be misled.
    """
    rows = []
    cases = {
        "healthy_a0.3": ("solve", 0.3),
        "healthy_a0.0": ("solve", 0.0),
        "om_zeros": ("raw", np.zeros),
        "om_ones": ("raw", np.ones),
        "om_tiny": ("raw", lambda n: np.full(n, 1e-300)),
        "om_huge": ("raw", lambda n: np.full(n, 1e150)),
    }
    for name, (kind, spec) in cases.items():
        if kind == "solve":
            col, om, c = solved_profile(J, spec)
        else:
            col = ACollocation(J, a=0.3)
            om, c = spec(J), 0.5
        r = classify(graded_norm_by_radius, col, om, c, ALPHA)
        v = r["value"] if r["status"] == "FINITE" else {}
        rows.append({"case": name, "status": r["status"],
                     "cond": v.get("cond"), "smin": v.get("smin"),
                     "by_cutoff": v.get("by_cutoff"),
                     "argmax_X": v.get("argmax_X"),
                     "ladder_looks_plausible": bool(
                         isinstance(v.get("by_cutoff"), dict)
                         and all(np.isfinite(x) and 0 < x < 1e12
                                 for x in v["by_cutoff"].values()))})
    return rows


def c2_empty_cutoff(J=200, a=0.3):
    """A cutoff below every node: the one place the module DOES return nan."""
    col, om, c = solved_profile(J, a)
    r = classify(graded_norm_by_radius, col, om, c, ALPHA,
                 cutoffs=(1e-300, 0.0, -5.0, np.inf))
    return {"J": J, "a": a, "status": r["status"], "value": r["value"],
            "X_min": float(col.X.min())}


# ---------------------------------------------------------------------------
# D.  poisoned derivatives -- NaN / inf through every public entry point
# ---------------------------------------------------------------------------


def d_poison(J=120, a=0.3):
    col, om0, c0 = solved_profile(J, a)
    X, h, Xc = homogeneous_far_field(col, om0, c0, n=401)

    def poisoned(arr, val, idx):
        b = np.array(arr, float, copy=True)
        b[idx] = val
        return b

    poisons = {}
    for pname, val in (("nan", float("nan")), ("inf", float("inf"))):
        for site, idx in (("om_first", 0), ("om_mid", J // 2), ("om_last", J - 1)):
            poisons["%s_%s" % (pname, site)] = poisoned(om0, val, idx)

    entries = {
        "profile_far_field": lambda om, c, al: profile_far_field(col, om, c, 3.0),
        "homogeneous_far_field": lambda om, c, al: homogeneous_far_field(
            col, om, c, n=401),
        "inner_mode_exponent": lambda om, c, al: inner_mode_exponent(
            col, om, c, n=401),
        "graded_norm_by_radius": lambda om, c, al: graded_norm_by_radius(
            col, om, c, al),
        "source_of_the_row": lambda om, c, al: source_of_the_row(col, om, c, al),
        "bordered_norm": lambda om, c, al: bordered_norm(col, om, c, al),
        "square_bordered_smin": lambda om, c, al: square_bordered_smin(col, om, c),
        "gauged_matrix": lambda om, c, al: gauged_matrix(col, om, c)[0],
    }

    rows = []
    for pname, om in poisons.items():
        for ename, fn in entries.items():
            r = classify(fn, om, c0, ALPHA)
            rows.append({"poison": pname, "entry": ename, "status": r["status"],
                         "exc": r["exc"]})
    for cname, cval in (("c_nan", float("nan")), ("c_inf", float("inf"))):
        for ename, fn in entries.items():
            r = classify(fn, om0, cval, ALPHA)
            rows.append({"poison": cname, "entry": ename, "status": r["status"],
                         "exc": r["exc"]})
    for aname, aval in (("alpha_nan", float("nan")), ("alpha_inf", float("inf"))):
        for ename in ("graded_norm_by_radius", "source_of_the_row",
                      "bordered_norm"):
            r = classify(entries[ename], om0, c0, aval)
            rows.append({"poison": aname, "entry": ename, "status": r["status"],
                         "exc": r["exc"], "value": r["value"]})
    # log_growth_exponent is fed a poisoned h rather than a poisoned profile.
    # The magnitude that matters is not "finite or not" but how far the poison
    # moves the answer -- if it moves it by exactly 0.0 the poison was ABSORBED,
    # which is the leg-107 mask failure mode in a different module.
    clean_q = log_growth_exponent(X, h, Xc)
    for pname, val in (("h_nan_midpoint", float("nan")),
                       ("h_negative_midpoint", -1.0),
                       ("h_inf_midpoint", float("inf"))):
        hp = np.array(h, float, copy=True)
        hp[len(hp) // 2] = val
        r = classify(log_growth_exponent, X, hp, Xc)
        q = r["value"] if r["status"] == "FINITE" else float("nan")
        rows.append({"poison": pname, "entry": "log_growth_exponent",
                     "status": r["status"], "exc": r["exc"], "value": q,
                     "clean_value": float(clean_q),
                     "shift_from_clean": (abs(q - clean_q)
                                          if np.isfinite(q) else float("nan")),
                     "absorbed_exactly": bool(np.isfinite(q) and q == clean_q)})
    # ... and the positive control: poison INSIDE the fitted tail window must move
    # it.  tail=0.1, so index >= 0.9*n is fitted and anything below it is not.
    for frac_idx, label in ((0.95, "h_nan_inside_fit_window"),
                            (0.5, "h_nan_outside_fit_window")):
        hp = np.array(h, float, copy=True)
        hp[int(frac_idx * len(hp))] = float("nan")
        r = classify(log_growth_exponent, X, hp, Xc)
        q = r["value"] if r["status"] == "FINITE" else float("nan")
        rows.append({"poison": label, "entry": "log_growth_exponent",
                     "status": r["status"], "exc": r["exc"], "value": q,
                     "clean_value": float(clean_q),
                     "index_fraction": frac_idx,
                     "absorbed_exactly": bool(np.isfinite(q) and q == clean_q)})
    return rows


def d2_partial_poison_contamination(J=120, a=0.3, n_poison=(1, 2, 5)):
    """Does ONE poisoned node change a CLEAN answer, or is it absorbed?

    The failure mode leg 107 found downstream (NaN silently excluded by a mask, so
    the certificate still certifies) is the one this probes for here.
    """
    col, om0, c0 = solved_profile(J, a)
    clean = source_of_the_row(col, om0, c0, ALPHA)
    rows = []
    rng = np.random.default_rng(11801)
    for k in n_poison:
        idx = rng.choice(J, size=k, replace=False)
        om = np.array(om0, float, copy=True)
        om[idx] = float("nan")
        r = classify(source_of_the_row, col, om, c0, ALPHA)
        rows.append({"n_poisoned": int(k), "status": r["status"],
                     "clean_fraction": float(clean["near_Xc_fraction"]),
                     "poisoned_value": r["value"]})
    return rows


# ---------------------------------------------------------------------------
# E.  structural adversaries -- the unguarded public `drop`, and a second crossing
# ---------------------------------------------------------------------------


def e_drop_out_of_range(J=120, a=0.3):
    col, om, c = solved_profile(J, a)
    ref, _ = gauged_matrix(col, om, c, drop=0)
    rows = []
    for d in (0, 1, J - 1, J, J + 5, -1, -J, 10 ** 6):
        r = classify(gauged_matrix, col, om, c, d)
        shape = None
        exc = r["exc"]
        try:
            M, keep = gauged_matrix(col, om, c, drop=d)
            shape = list(M.shape)
            same = bool(M.shape == ref.shape and np.allclose(M, ref))
        except Exception as e:                                   # noqa: BLE001
            same, exc = None, type(e).__name__
        rows.append({"drop": int(d), "status": r["status"], "exc": exc,
                     "shape": shape, "identical_to_drop0": same,
                     "square": (None if shape is None else shape[0] == shape[1])})
    return rows


def e2_second_crossing(J=400, a=0.3, amps=(0.0, 0.5, 1.0, 2.0, 5.0, 20.0)):
    """H5: homogeneous_far_field starts at 1.5*Xc and assumes no further crossing.

    critical_radius returns only the FIRST crossing.  A bump added to the profile
    can put a second zero of E beyond it -- a pole in f = H/E that the trapezoid
    rule steps straight over.  Reported honestly: if no admissible construction
    produces a second crossing, that count is the result.
    """
    col, om0, c = solved_profile(J, a)
    Xc0 = _xc(col, om0, c)
    bump = np.exp(-((col.X - 3.0 * Xc0) / (1.0 * Xc0)) ** 2)
    rows, n_two = [], 0
    for amp in amps:
        om = np.asarray(om0, float) + amp * bump
        E = effective_speed(col.X, col.V @ om, c, col.a)
        pos = col.X > 0
        Xp, Ep = col.X[pos], E[pos]
        idx = np.where(np.diff(np.sign(Ep)) != 0)[0]
        n_cross = int(idx.size)
        crossings = [float(Xp[i]) for i in idx]
        Xc = _xc(col, om, c)
        X0 = 1.5 * Xc                       # homogeneous_far_field's own start
        # The claim is only live if a LATER crossing sits inside the integration
        # window [X0, X_max] -- otherwise the quadrature never sees the pole and
        # there is nothing to step over.  Measured, not assumed.
        later = [x for x in crossings if X0 < x < 1e8]
        r = classify(homogeneous_far_field, col, om, c, n=2001)
        q = float("nan")
        if r["status"] in ("FINITE", "NONFINITE"):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                try:
                    Xa, ha, Xca = homogeneous_far_field(col, om, c, n=2001)
                    q = log_growth_exponent(Xa, ha, Xca)
                except Exception:                                # noqa: BLE001
                    q = float("nan")
        n_two += int(len(later) > 0)
        rows.append({"bump_amp": amp, "n_sign_changes_positive_X": n_cross,
                     "crossings_X": crossings, "Xc_first": float(Xc),
                     "integration_starts_at": float(X0),
                     "crossings_inside_integration_window": later,
                     "n_poles_inside_window": len(later),
                     "status": r["status"], "exponent": q,
                     "predicted_1_over_a": 1.0 / a,
                     "rel_error_vs_prediction": (abs(q - 1.0 / a) * a
                                                 if np.isfinite(q) else float("nan")),
                     "finite_and_plausible": bool(np.isfinite(q) and 0 < q < 100)})
    return {"a": a, "J": J, "Xc_unbumped": float(Xc0),
            "n_constructions_with_a_pole_inside_the_integration_window": n_two,
            "n_constructions": len(rows), "rows": rows}


# ---------------------------------------------------------------------------
# F.  reachability -- does the path production actually walks hit any of this?
# ---------------------------------------------------------------------------


def f_reachability():
    """Read from the banked runner, not asserted.

    experiments/p2_route_d_v13_turning.py is the only runner that calls the
    unguarded entry points.  Its own argument lists decide whether the gap is live
    or latent, and they are quoted here rather than re-derived.
    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = open(os.path.join(root, "experiments", "p2_route_d_v13_turning.py")).read()
    tst = open(os.path.join(root, "test_turning_point.py")).read()
    return {
        "runner": "experiments/p2_route_d_v13_turning.py",
        "s3_attribution_a_values_include_0": "a_values=(0.0, 0.2, 0.3)" in src,
        "s4_source_a_values": "a_values=(0.2, 0.3, 0.4)",
        "s4_source_includes_a0": "def s4_source(a_values=(0.0" in src,
        "test_5_asserts_near_Xc_fraction": 'src["near_Xc_fraction"] > 0.5' in tst,
        # INSTRUMENT NOTE: the first run counted every occurrence of the name,
        # which includes the `from solver.turning_point import ...` line, and so
        # reported a control that does not exist.  Count CALL sites only.
        "n_source_of_the_row_call_sites_in_test":
            tst.count("source_of_the_row("),
        "n_source_of_the_row_call_sites_in_runner":
            src.count("source_of_the_row("),
        "test_5_runs_a0_control_on_near_Xc_fraction":
            tst.count("source_of_the_row(") > 1,
        "test_file_mentions_nan_or_inf":
            any(k in tst for k in ("isnan", "isinf", "np.nan", "np.inf")),
    }


# ---------------------------------------------------------------------------


def main():
    np.seterr(all="ignore")
    res = {
        "leg": 118, "route": "ROUTE-TPA",
        "module_under_test": "solver/turning_point.py",
        "module_is_read_only": True,
        "alpha": ALPHA,
        "module_attribution_threshold_quoted_from_test": MODULE_ATTRIBUTION_THRESHOLD,
        "A_missing_guard": a_missing_guard(),
        "A2_attribution_control": a2_attribution_control(),
        "A3_grid_too_short": a3_grid_too_short(),
        "B_caller_supplied_xc": b_caller_supplied_xc(),
        "C_conditioning": c_conditioning(),
        "C2_empty_cutoff": c2_empty_cutoff(),
        "D_poison": d_poison(),
        "D2_partial_poison": d2_partial_poison_contamination(),
        "E_drop_out_of_range": e_drop_out_of_range(),
        "E2_second_crossing": e2_second_crossing(),
        "F_reachability": f_reachability(),
    }

    d = res["D_poison"]
    res["summary"] = {
        "poison_cases": len(d),
        "poison_FINITE": sum(r["status"] == "FINITE" for r in d),
        "poison_NONFINITE": sum(r["status"] == "NONFINITE" for r in d),
        "poison_RAISED": sum(r["status"] == "RAISED" for r in d),
        "a0_guarded_site_raised": all(
            r["guarded_site__homogeneous_far_field"]["status"] == "RAISED"
            for r in res["A_missing_guard"]),
        "a0_unguarded_source_FINITE": sum(
            r["unguarded_site__source_of_the_row"]["status"] == "FINITE"
            for r in res["A_missing_guard"]),
        "a0_unguarded_inner_RAISED": sum(
            r["unguarded_site__inner_mode_exponent"]["status"] == "RAISED"
            for r in res["A_missing_guard"]),
        "a0_unguarded_source_fabricated_fraction": [
            r["unguarded_site__source_of_the_row"]["field_value"]
            for r in res["A_missing_guard"]],
        "a0_unguarded_source_warnings": sum(
            r["unguarded_site__source_of_the_row"]["n_warnings"]
            for r in res["A_missing_guard"]),
        "no_Xc_cases_passing_module_threshold": sum(
            (not r["Xc_exists"]) and r["passes_module_threshold"]
            for r in res["A2_attribution_control"]["rows"]),
        "no_Xc_cases_total": sum(
            not r["Xc_exists"] for r in res["A2_attribution_control"]["rows"]),
        "n_pairs_where_no_Xc_beats_real_Xc":
            res["A2_attribution_control"]["n_pairs_where_no_Xc_beats_real_Xc"],
        "log_growth_poison_absorbed_exactly": sum(
            bool(r.get("absorbed_exactly")) for r in d),
        "poles_inside_integration_window":
            res["E2_second_crossing"][
                "n_constructions_with_a_pole_inside_the_integration_window"],
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1, sort_keys=True, default=str)

    s = res["summary"]
    print("Route-TPA adversarial battery -- solver/turning_point.py (READ-ONLY)")
    print("  A  guarded site raised on every a=0 grid:  %s"
          % s["a0_guarded_site_raised"])
    print("  A  unguarded source_of_the_row FINITE:     %d/%d grids"
          % (s["a0_unguarded_source_FINITE"], len(res["A_missing_guard"])))
    print("  A  unguarded inner_mode_exponent RAISED:   %d/%d grids"
          % (s["a0_unguarded_inner_RAISED"], len(res["A_missing_guard"])))
    print("  A  fabricated near_Xc_fraction at a=0 (no X_c exists):  %s"
          % ", ".join("%.6f" % x
                      for x in s["a0_unguarded_source_fabricated_fraction"]))
    print("  A  warnings emitted while fabricating it:               %d"
          % s["a0_unguarded_source_warnings"])
    print("  A2 near_Xc_fraction with NO X_c passing the module's own >0.5 gate: "
          "%d/%d" % (s["no_Xc_cases_passing_module_threshold"],
                     s["no_Xc_cases_total"]))
    for r in res["A2_attribution_control"]["rows"]:
        print("       a=%.2f  Xc_exists=%-5s  near_Xc_fraction=%.6f  passes=%s"
              % (r["a"], r["Xc_exists"], r["near_Xc_fraction"],
                 r["passes_module_threshold"]))
    print("  A2 (a with NO X_c) beats (a with a REAL X_c) in %d pair(s): %s"
          % (s["n_pairs_where_no_Xc_beats_real_Xc"],
             res["A2_attribution_control"]["inverted_pairs"]))
    print("  A3 hypothesis 'grid ends before X_c' refuted: %s (%d/%d grids short)"
          % (res["A3_grid_too_short"]["hypothesis_refuted"],
             res["A3_grid_too_short"]["n_grids_short_of_Xc"],
             res["A3_grid_too_short"]["n_grids"]))
    print("  A3 attribution fraction range at fixed a=0.2 over J=20..400: "
          "%.6f .. %.6f (exactly 0.0 at %d of %d grids)"
          % (res["A3_grid_too_short"]["attribution_fraction_min"],
             res["A3_grid_too_short"]["attribution_fraction_max"],
             res["A3_grid_too_short"]["attribution_fraction_n_exactly_zero"],
             res["A3_grid_too_short"]["n_grids"]))
    print("  B  exponent shift from a wrong caller-supplied Xc: "
          + ", ".join("x%g->%.4f" % (r["Xc_factor"], r["exponent"])
                      for r in res["B_caller_supplied_xc"]["rows"]))
    print("  B  wrong-Xc cases still passing the module's own 5%% gate: %d/%d"
          % (sum(r["within_module_gate_5pct"]
                 for r in res["B_caller_supplied_xc"]["rows"]),
             len(res["B_caller_supplied_xc"]["rows"])))
    print("  D  poison: %d FINITE / %d NONFINITE / %d RAISED of %d"
          % (s["poison_FINITE"], s["poison_NONFINITE"], s["poison_RAISED"],
             s["poison_cases"]))
    print("  D  log_growth_exponent poisons absorbed with shift EXACTLY 0.0: %d"
          % s["log_growth_poison_absorbed_exactly"])
    print("  E2 constructions with a pole of H/E INSIDE the integration window: "
          "%d/%d" % (s["poles_inside_integration_window"],
                     res["E2_second_crossing"]["n_constructions"]))
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
