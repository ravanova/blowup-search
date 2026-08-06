"""Leg 118 (Route-TPA) -- the adversarial battery against turning_point.py's CLASSIFICATION.

THE QUESTION (the leg's gate, verbatim):

    Under an adversarial battery (degenerate branches, poisoned derivatives), does
    solver/turning_point.py ever silently return a wrong classification instead of
    flagging the input?

**THE ANSWER IS YES.** `solver/turning_point.py` and `solver/collocation_newton.py` (which
supplies `critical_radius`/`effective_speed`, the detection primitive every public function
in `turning_point.py` relies on) are READ-ONLY under this leg and are NOT patched: the gate's
yes-branch escalates, it does not repair.

WHAT THIS IS NOT.  No exponent, constant or bound in the module is sharpened, contested or
re-derived.  `test_turning_point.py`'s 6 gates (a real, converged, non-degenerate profile)
are not touched and are not re-measured; every number below is about what happens on a
*degenerate* or *poisoned* input, never about the module's physics on a well-posed one.

--------------------------------------------------------------------------------
THE MECHANISM
--------------------------------------------------------------------------------
`critical_radius(X, E)` (solver/collocation_newton.py) is "the smallest X > 0 where E changes
sign", implemented as

    s = np.where(np.diff(np.sign(E)) != 0)[0]
    if s.size == 0: return inf
    i = s[0]; t = -E[i] / (E[i+1] - E[i]); return X[i] + t*(X[i+1]-X[i])

The classical bracketing test for "does [X_i, X_{i+1}] contain a genuine crossing" is the
STRICT product inequality E[i]*E[i+1] < 0 (Bolzano's theorem; scipy.optimize.brentq enforces
exactly this and raises ValueError "f(a) and f(b) must have different signs" otherwise).
`np.sign(E[i+1]) != np.sign(E[i])` is a different, weaker test: it ALSO fires whenever either
endpoint is exactly 0.0, i.e. at a TANGENCY -- a local extremum of E that grazes zero without
E ever actually going negative.  A tangency is not a turning point under the module's own
physical picture (E ~ -a*h_c*(X-X_c), a genuinely transversal zero), yet nothing downstream
checks for one, and the tangency case produces a fully FINITE X_c with zero warnings.

Every public function of turning_point.py that needs X_c inherits whatever critical_radius
returns without re-validating it: homogeneous_far_field only checks `np.isfinite(Xc)`, which
a tangency-produced Xc passes trivially.

--------------------------------------------------------------------------------
HOW THE ADVERSARY IS BUILT
--------------------------------------------------------------------------------
Two complementary constructions, both stated explicitly so the ground truth is never in doubt:

  (A) MONKEYPATCH `solver.turning_point.effective_speed` (the name imported into that
      module's namespace) to a fully-specified, closed-form E(X), restored in a `finally`
      block immediately after each case.  This is a standard dependency-injection technique:
      every OTHER function in the call graph (profile_far_field's Sm/Im evaluation,
      homogeneous_far_field's integrator, critical_radius itself) is the real, unmodified
      code from the two solver files; only the one input quantity under adversarial control
      is fixed to a value whose true classification (turning point or not, and where) is
      known analytically and stated before the case is run.
  (B) A genuinely adversarial `om` (a "poisoned derivative": one Fourier coefficient of a
      real, Newton-converged profile perturbed by a large factor), run through EVERY function
      with zero monkeypatching, to show the same finite/no-warning propagation reachable from
      the ordinary calling convention, not only from a synthetic E.

All magnitudes below are measured, not asserted; every number quoted in the leg's writeup is
in the curated JSON this script produces.
"""

import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import solver.turning_point as tp                                        # noqa: E402
from solver.turning_point import (bordered_norm, graded_norm_by_radius,  # noqa: E402
                                  homogeneous_far_field, inner_mode_exponent,
                                  log_growth_exponent, solved_profile,
                                  source_of_the_row, square_bordered_smin)
from solver.collocation_newton import ACollocation, critical_radius, effective_speed  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "writeup" / "data" / "p2_route_tpa_v1_adversarial.json"

J_DEFAULT = 100
A_DEFAULT = 0.3


def _call(fn, *args, **kw):
    """Run fn, capturing warnings, and report (ok, result_or_exc_repr, n_warnings)."""
    with warnings.catch_warnings(record=True) as wrec:
        warnings.simplefilter("always")
        try:
            r = fn(*args, **kw)
            return {"raised": None, "n_warnings": len(wrec), "warnings": [str(w.message) for w in wrec]}, r
        except Exception as e:
            return {"raised": "%s: %s" % (type(e).__name__, e), "n_warnings": len(wrec),
                    "warnings": [str(w.message) for w in wrec]}, None


def jsonable(x):
    if isinstance(x, dict):
        return {k: jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    if isinstance(x, (np.floating, np.integer)):
        return float(x)
    if isinstance(x, np.ndarray):
        return jsonable(x.tolist())
    if isinstance(x, float):
        if np.isnan(x):
            return "nan"
        if np.isinf(x):
            return "inf" if x > 0 else "-inf"
        return x
    return x


def g1_positive_control(col, om, c):
    """G1 -- baseline: a real converged profile has exactly one crossing and the module
    finds it, matching its own known-answer gates.  Not a re-measurement of the physics;
    a sanity check that this script's harness reproduces the module's ordinary behaviour."""
    Xc_direct = critical_radius(col.X, effective_speed(col.X, col.V @ om, c, col.a))
    meta, (X, h, Xc) = _call(homogeneous_far_field, col, om, c, n=1001)
    q = log_growth_exponent(X, h, Xc)
    p, Xc_inner = inner_mode_exponent(col, om, c, n=1001)
    return {"Xc_direct": Xc_direct, "Xc_from_hff": Xc, "outer_exponent": q,
            "inner_exponent": p, "predicted_1_over_a": 1.0 / col.a,
            "hff_meta": meta, "h_all_finite": bool(np.isfinite(h).all())}


def g2_offgrid_no_crossing_control(col, om, c):
    """G2 -- negative control: E genuinely never crosses zero AND does not land exactly on
    a grid node.  The module must say so (Xc = inf, homogeneous_far_field raises).  Run at
    several offsets so a single lucky placement cannot be mistaken for robustness."""
    real_es = tp.effective_speed
    cases = []
    offsets = [0.37, 1.13, 5.29, 17.001, 50.5]
    for off in offsets:
        X0 = float(col.X[0]) + off      # deliberately NOT equal to any grid node

        def E_of(Xarr, U, c_, a_, X0=X0):
            Xarr = np.asarray(Xarr, dtype=float)
            return (Xarr - X0) ** 2 + 1e-6      # strictly positive everywhere: TRUE = no crossing

        tp.effective_speed = E_of
        try:
            Xc_direct = critical_radius(col.X, E_of(col.X, None, c, col.a))
            meta, res = _call(homogeneous_far_field, col, om, c, n=201)
            cases.append({"X0": X0, "Xc_direct": Xc_direct,
                          "correctly_infinite": bool(not np.isfinite(Xc_direct)),
                          "hff_raised": meta["raised"], "hff_correctly_raised": meta["raised"] is not None})
        finally:
            tp.effective_speed = real_es
    return cases


def g3_nan_inf_controls(col, om, c):
    """G3 -- NaN/Inf poisoning is FLAGGED (nan output, or a raised ValueError), not
    silently absorbed into a plausible finite classification.  Also: a distant +inf that
    does not touch the real crossing must not disturb it (regression safety)."""
    out = {}
    U = col.V @ om
    E_clean = effective_speed(col.X, U, c, col.a)
    Xc_clean = critical_radius(col.X, E_clean)

    E_nan = E_clean.copy()
    i_cross = int(np.argmin(np.abs(E_clean)))
    E_nan[max(i_cross - 1, 0)] = np.nan
    Xc_nan = critical_radius(col.X, E_nan)
    out["nan_at_crossing"] = {"Xc": jsonable(Xc_nan), "is_nan": bool(np.isnan(Xc_nan))}

    om_nan = om.copy()
    om_nan[5] = np.nan
    meta, res = _call(homogeneous_far_field, col, om_nan, c, n=201)
    out["nan_om_hff"] = {"raised": meta["raised"], "correctly_flagged": meta["raised"] is not None}

    E_farinf = E_clean.copy()
    j_far = 2
    if j_far < i_cross - 5:
        E_farinf[j_far] = np.inf
        Xc_farinf = critical_radius(col.X, E_farinf)
        out["distant_inf_does_not_disturb_crossing"] = {
            "Xc_clean": Xc_clean, "Xc_with_distant_inf": Xc_farinf,
            "unchanged": bool(Xc_clean == Xc_farinf)}
    return out


def g4_ongrid_tangency_defect(col, om, c):
    """G4 -- THE DEFECT.  E touches EXACTLY 0.0 at one grid node and is single-signed
    (never crosses) on both sides.  Ground truth: NO turning point exists (Xc should be
    inf).  Sweep several node positions and both signs (touch-from-above / touch-from-below).
    Uses the SAME (col, om, c) throughout -- effective_speed is the only patched name, so
    homogeneous_far_field/inner_mode_exponent/source_of_the_row see the exact grid the touch
    was placed on."""
    real_es = tp.effective_speed
    n = len(col.X)
    idxs = sorted(set(max(2, min(n - 3, int(f * n))) for f in (0.1, 0.25, 0.5, 0.65, 0.85)))
    cases = []
    for idx in idxs:
        X0 = float(col.X[idx])
        for sign, label in ((1.0, "touch_from_above"), (-1.0, "touch_from_below")):

            def E_of(Xarr, U, c_, a_, X0=X0, sign=sign):
                Xarr = np.asarray(Xarr, dtype=float)
                return sign * (Xarr - X0) ** 2

            tp.effective_speed = E_of
            try:
                E_grid = E_of(col.X, None, c, col.a)
                exact_zero = bool(E_grid[idx] == 0.0)
                never_negative_or_positive = bool(np.all(sign * E_grid >= 0.0))
                Xc_direct = critical_radius(col.X, E_grid)
                meta_hff, res_hff = _call(homogeneous_far_field, col, om, c, n=201)
                if res_hff is not None:
                    X, h, Xc2 = res_hff
                    meta_q, q = _call(log_growth_exponent, X, h, Xc2)
                    h_finite = bool(np.isfinite(h).all())
                else:
                    meta_q, q, h_finite = None, None, None
                # inner_mode_exponent has NO isfinite guard on Xc at all; only probe it
                # when Xc is finite (the case that matters for this gate) to avoid
                # hammering LAPACK with the already-documented inf-Xc crash path.
                if np.isfinite(Xc_direct):
                    inner_meta, inner_res = _call(inner_mode_exponent, col, om, c, n=201)
                else:
                    inner_meta, inner_res = {"raised": None, "skipped": "Xc not finite"}, None
                src_meta, src_res = _call(source_of_the_row, col, om, c, 1.4)
                cases.append({
                    "touch_index": idx, "X0": X0, "kind": label,
                    "E_exactly_zero_at_touch": exact_zero,
                    "E_single_signed_elsewhere": never_negative_or_positive,
                    "Xc_reported": jsonable(Xc_direct),
                    "silently_finite_not_inf": bool(np.isfinite(Xc_direct)),
                    "hff_meta": meta_hff, "hff_h_all_finite": h_finite,
                    "inner_mode_meta": inner_meta,
                    "inner_mode_result": jsonable(inner_res),
                    "log_growth_result": jsonable(q) if res_hff is not None else None,
                    "source_of_the_row_meta": src_meta,
                    "source_of_the_row_result": jsonable(src_res),
                })
            finally:
                tp.effective_speed = real_es
    return cases


def g5_composite_masks_real_crossing(col, om, c):
    """G5 -- THE SHARPEST INSTANCE.  A spurious tangency sits BEFORE a real, well-separated
    transversal crossing.  Ground truth: the only genuine sign change is at X_true (far out);
    the touch at X0_touch is provably not a crossing (E is a perfect square there, >= 0
    everywhere up to the transition).  Measure how far the reported Xc is from X_true.
    Uses the SAME (col, om, c) as everywhere else in this file."""
    real_es = tp.effective_speed
    cases = []
    touch_fracs = [0.05, 0.1, 0.2]
    for frac in touch_fracs:
        idx = max(2, int(frac * len(col.X)))
        X0_touch = float(col.X[idx])
        WIDTH = 0.5
        SLOPE = 0.05
        edge = X0_touch + WIDTH
        edge_val = WIDTH ** 2
        X_true = edge + edge_val / SLOPE

        def E_of(Xarr, U, c_, a_, X0_touch=X0_touch, edge=edge, edge_val=edge_val):
            Xarr = np.asarray(Xarr, dtype=float)
            return np.where(Xarr <= edge, (Xarr - X0_touch) ** 2, edge_val - SLOPE * (Xarr - edge))

        tp.effective_speed = E_of
        try:
            E_grid = E_of(col.X, None, c, col.a)
            Xc_direct = critical_radius(col.X, E_grid)
            meta_hff, res_hff = _call(homogeneous_far_field, col, om, c, n=1001)
            ratio = (X_true / Xc_direct) if (Xc_direct and np.isfinite(Xc_direct) and Xc_direct != 0) else None
            cases.append({
                "touch_frac_of_grid": frac, "X0_touch": X0_touch, "X_true_turning_point": X_true,
                "Xc_reported": jsonable(Xc_direct),
                "reported_equals_spurious_touch": bool(abs(Xc_direct - X0_touch) < 1e-9) if np.isfinite(Xc_direct) else False,
                "true_over_reported_ratio": ratio,
                "hff_meta": meta_hff,
                "hff_finite": bool(np.isfinite(res_hff[1]).all()) if res_hff is not None else None,
            })
        finally:
            tp.effective_speed = real_es
    return cases


def g6_natural_reachability(J_list=(60, 100), a_list=(0.15, 0.2, 0.3, 0.4)):
    """G6 -- SEVERITY, MEASURED.  Does any currently-computable, Newton-converged real
    profile's own U = col.V @ om have an interior local extremum (the only way a REAL,
    unmodified physics run could organically produce the tangency of G4/G5, since a
    monotone U can only ever cross zero transversally)?  If none do, the defect is latent
    under every configuration this repository's own experiments actually run."""
    found_any = False
    rows = []
    for J in J_list:
        for a in a_list:
            col, om, c = solved_profile(J, a)
            U = col.V @ om
            is_extremum = (U[1:-1] - U[:-2]) * (U[2:] - U[1:-1]) < 0
            n_extrema = int(is_extremum.sum())
            found_any = found_any or (n_extrema > 0)
            rows.append({"J": J, "a": a, "n_interior_extrema_of_U": n_extrema,
                        "U_monotonic": bool(n_extrema == 0)})
    return {"rows": rows, "any_real_profile_has_interior_extremum": found_any}


def g7_poisoned_om_no_monkeypatch(col, om, c):
    """G7 -- REACHABILITY WITHOUT ANY MONKEYPATCH.  A single poisoned Fourier coefficient
    of a REAL converged profile, run through the ordinary, completely unmodified call
    path.  Reports the resulting classification change; does not claim a 'true' answer for
    the corrupted profile (there isn't one), only the magnitude of the silent change and
    whether it is flagged."""
    Xc_clean = critical_radius(col.X, effective_speed(col.X, col.V @ om, c, col.a))
    out = []
    for k, scale in [(3, 1e4), (3, 1e8), (len(om) // 2, 1e6)]:
        om_p = om.copy()
        om_p[k] = om_p[k] + scale
        meta, res = _call(homogeneous_far_field, col, om_p, c, n=201)
        Xc_p = critical_radius(col.X, effective_speed(col.X, col.V @ om_p, c, col.a))
        out.append({"coefficient_index": k, "additive_perturbation": scale,
                    "Xc_clean": Xc_clean, "Xc_perturbed": jsonable(Xc_p),
                    "hff_meta": meta, "hff_finite": bool(np.isfinite(res[1]).all()) if res is not None else None})
    return out


def g8_matrix_functions_under_poison(col, om, c):
    """G8 -- the matrix-inversion side (graded_norm_by_radius, bordered_norm,
    square_bordered_smin, source_of_the_row) under the same NaN/Inf poisoning.  These are
    NOT the classification primitive, but they are public functions of the same module and
    the gate asks about the whole module.  Reports whether poisoning is flagged (raised /
    nan) or silently absorbed into a finite number."""
    ALPHA = 1.4
    cases = []
    om_nan = om.copy(); om_nan[5] = np.nan
    om_inf = om.copy(); om_inf[5] = np.inf
    for label, omx, cx in [("clean", om, c), ("NaN_om", om_nan, c), ("inf_om", om_inf, c),
                            ("c_is_NaN", om, float("nan"))]:
        row = {"case": label}
        for fname, fn, args in [
            ("graded_norm_by_radius", graded_norm_by_radius, (col, omx, cx, ALPHA)),
            ("source_of_the_row", source_of_the_row, (col, omx, cx, ALPHA)),
            ("bordered_norm", bordered_norm, (col, omx, cx, ALPHA)),
            ("square_bordered_smin", square_bordered_smin, (col, omx, cx)),
        ]:
            meta, res = _call(fn, *args)
            silently_finite = False
            if meta["raised"] is None and res is not None:
                flat = res if not isinstance(res, dict) else list(res.values())
                try:
                    silently_finite = bool(np.all(np.isfinite(np.array(
                        [v for v in (flat if isinstance(flat, (list, tuple)) else [flat])
                         if isinstance(v, (int, float, np.floating))] or [np.nan]))))
                except Exception:
                    silently_finite = False
            row[fname] = {"raised": meta["raised"], "result": jsonable(res),
                          "silently_finite": silently_finite}
        cases.append(row)
    return cases


def _t(label, t0):
    print("  ...%s done at +%.2fs" % (label, time.time() - t0)); sys.stdout.flush()


def main():
    t0 = time.time()
    col, om, c = solved_profile(J_DEFAULT, A_DEFAULT)
    _t("solved_profile", t0)

    data = {
        "leg": 118, "route": "TPA", "module_under_audit": "solver/turning_point.py",
        "detection_primitive": "solver/collocation_newton.py:critical_radius (imported into turning_point.py's namespace)",
        "gate": ("Under an adversarial battery (degenerate branches, poisoned derivatives), does "
                "solver/turning_point.py ever silently return a wrong classification instead of "
                "flagging the input?"),
        "J_default": J_DEFAULT, "a_default": A_DEFAULT,
    }
    data["g1_positive_control"] = g1_positive_control(col, om, c); _t("g1", t0)
    data["g2_offgrid_no_crossing_control"] = g2_offgrid_no_crossing_control(col, om, c); _t("g2", t0)
    data["g3_nan_inf_controls"] = g3_nan_inf_controls(col, om, c); _t("g3", t0)
    data["g4_ongrid_tangency_defect"] = g4_ongrid_tangency_defect(col, om, c); _t("g4", t0)
    data["g5_composite_masks_real_crossing"] = g5_composite_masks_real_crossing(col, om, c); _t("g5", t0)
    data["g6_natural_reachability"] = g6_natural_reachability(); _t("g6", t0)
    data["g7_poisoned_om_no_monkeypatch"] = g7_poisoned_om_no_monkeypatch(col, om, c); _t("g7", t0)
    data["g8_matrix_functions_under_poison"] = g8_matrix_functions_under_poison(col, om, c); _t("g8", t0)
    data["wall_time_s"] = None
    data["wall_time_s"] = round(time.time() - t0, 3)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(jsonable(data), f, indent=1, sort_keys=False)
        f.write("\n")
    print("wrote", OUT, "in %.2fs" % data["wall_time_s"])

    # ---- headline printout ----
    n_defect = sum(1 for c_ in data["g4_ongrid_tangency_defect"] if c_["silently_finite_not_inf"])
    n_g4 = len(data["g4_ongrid_tangency_defect"])
    print("G4 (on-grid tangency, ground truth = NO turning point): %d/%d cases report a "
          "SILENT FINITE (wrong) Xc" % (n_defect, n_g4))
    for c_ in data["g5_composite_masks_real_crossing"]:
        print("G5 touch_frac=%.2f: reported Xc=%r == spurious touch (%s); true turning point "
              "missed by %r x" % (c_["touch_frac_of_grid"], c_["Xc_reported"],
                                  c_["reported_equals_spurious_touch"], c_["true_over_reported_ratio"]))
    print("G6 any real converged profile reaches the defect naturally:",
          data["g6_natural_reachability"]["any_real_profile_has_interior_extremum"])


if __name__ == "__main__":
    main()
