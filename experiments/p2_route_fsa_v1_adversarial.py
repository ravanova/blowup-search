"""Leg 124 / Route-FSA -- adversarial battery for solver/finite_support.py.

GATE (pre-committed, DIRECTION.md leg 124): under an adversarial battery of
degenerate or poisoned inputs, does solver/finite_support.py ever silently return
a wrong result instead of flagging the input?
  yes -> silent-corruption gap; report the exact failing case; ESCALATE, DO NOT PATCH.
  no  -> confirmed robust; bank the battery as a permanent regression test.

solver/finite_support.py is READ-ONLY under both branches.  This module edits
nothing and imports the target only to call it.

WHAT IS *NOT* CLAIMED (novelty pass writeup/novelty/leg_124.md sec 0 and 5):
no value of X_c, of ||A||, of p, of c, nothing about the two-scale profile, and
nothing about whether the module converges -- its own docstring already says it
does not.  Every number below is a discrepancy magnitude, a case count, or a
test outcome.

The module is SUPERSEDED (capabilities.py:535-538, "validated: nothing") and has
ZERO importers repo-wide, so every finding here is a LATENT trap, not a
contaminated banked result.  G10 measures that rather than assuming it.

Run:  .venv/bin/python experiments/p2_route_fsa_v1_adversarial.py
Out:  writeup/data/p2_route_fsa_v1_adversarial.json
"""

import json
import pathlib
import subprocess
import sys
import warnings

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.finite_support import (  # noqa: E402
    FiniteSupportOps,
    FiniteSupportProfile,
    cheb_quad,
    even_cheb,
)

OUT = ROOT / "writeup" / "data" / "p2_route_fsa_v1_adversarial.json"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def capture(fn, *args, **kwargs):
    """Call fn, returning (value|None, exception_name|None, [warning texts])."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            val, exc = fn(*args, **kwargs), None
        except Exception as e:                                   # noqa: BLE001
            val, exc = None, type(e).__name__
    return val, exc, [str(x.message) for x in w]


def finite_report(x):
    """'finite' / 'nonfinite' / 'raised:X' for an array-ish return."""
    a = np.atleast_1d(np.asarray(x, float))
    if a.size == 0:
        return "empty"
    return "finite" if np.all(np.isfinite(a)) else "nonfinite"


def cheb_T(n, x):
    """Exact T_n by the three-term recurrence -- an INDEPENDENT reference for
    even_cheb, which goes through arccos/cos and is therefore the thing under
    test.  Valid for |x| > 1 too, which is the whole point."""
    x = np.asarray(x, float)
    t0, t1 = np.ones_like(x), x
    if n == 0:
        return t0
    for _ in range(n - 1):
        t0, t1 = t1, 2.0 * x * t1 - t0
    return t1


def independent_residual(a, b, Xc, c=0.5, n_pts=200, N=8000, n_int=1200):
    """max |X_c R| on a grid that shares NO node with the module's collocation
    set, at 4x-10x the quadrature resolution the solve used.

    The Hilbert map this reuses is itself pinned to 4.6e-08 by G1's known answer,
    so this is a check of the SOLUTION, independent of the rows that produced it.
    """
    v = np.linspace(0.013, 0.987, n_pts)          # irrational-ish offsets, no node hits
    ops = FiniteSupportOps(1.0 / a, len(b), v, N=N, n_int=n_int)
    ops.a = a
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = ops.residual(np.asarray(b, float), float(Xc), c)
    return float(np.max(np.abs(r)))


# ---------------------------------------------------------------------------
# G1 -- the module's OWN "Gate 1", specified in its docstring and never written
# ---------------------------------------------------------------------------

def gate_1_known_answer():
    """POSITIVE CONTROL, and it can report the other answer.

    finite_support.py lines 85-89 name the check that "pins the quadrature, the
    subtraction and the sign convention at once":

        (1/pi) p.v. INT_{-1}^{1} sqrt(1-y^2) U_{n-1}(y) / (x-y) dy = T_n(x).

    At p = 1/2 the module's basis function is phi_k = sqrt(1-v^2) T_{2k}, and
    T_0 = U_0, T_m = (U_m - U_{m-2})/2 for m >= 2, so the exact answer is

        Htilde_0 = T_1,      Htilde_k = (T_{2k+1} - T_{2k-1})/2   (k >= 1).

    If this fails, every other number in this battery is about a broken
    quadrature rather than about domain hygiene, and the leg says so.
    """
    v = np.array([0.1, 0.2, 0.35, 0.5, 0.65, 0.8, 0.9, 0.97])
    K = 5
    ops = FiniteSupportOps(0.5, K, v, N=8000, n_int=100)
    exact = np.empty((v.size, K))
    exact[:, 0] = cheb_T(1, v)
    for k in range(1, K):
        exact[:, k] = 0.5 * (cheb_T(2 * k + 1, v) - cheb_T(2 * k - 1, v))
    err = np.abs(ops.H - exact)
    # convergence of the rule, so the number is a rate and not a single point
    errs = {}
    for N in (500, 1000, 2000, 4000, 8000):
        o = FiniteSupportOps(0.5, K, v, N=N, n_int=100)
        errs[N] = float(np.max(np.abs(o.H - exact)))
    return {
        "identity": "(1/pi) pv INT sqrt(1-y^2) U_{n-1}(y)/(x-y) dy = T_n(x)",
        "source": "solver/finite_support.py lines 85-89 (specified, never implemented)",
        "p": 0.5, "K": K, "n_eval_points": int(v.size),
        "max_abs_err_N8000": float(np.max(err)),
        "max_abs_err_per_mode": [float(x) for x in np.max(err, axis=0)],
        "max_abs_err_vs_N": {str(k): val for k, val in errs.items()},
        "verdict": ("PASS -- the finite-support Hilbert transform, the p.v. subtraction "
                    "and the sign convention are pinned by an exact known answer"
                    if np.max(err) < 1e-6 else
                    "FAIL -- the quadrature itself is wrong; read every other gate in that light"),
    }


# ---------------------------------------------------------------------------
# G2 -- H1: the np.clip in even_cheb
# ---------------------------------------------------------------------------

def gate_2_clip():
    outside = np.array([1.0 + 1e-12, 1.01, 1.5, 3.0, 50.0, -7.0])
    K = 6
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        T, dT = even_cheb(K, outside)
    n_warn = len(w)
    T1, _ = even_cheb(K, np.array([1.0]))
    dev_from_edge = float(np.max(np.abs(T - T1)))
    exact = np.column_stack([cheb_T(2 * k, outside) for k in range(K)])
    rel = np.abs(T - exact) / np.maximum(np.abs(exact), 1.0)
    per_point = {}
    for i, v in enumerate(outside):
        per_point[f"{v:g}"] = {
            "returned_T2": float(T[i, 1]), "exact_T2": float(exact[i, 1]),
            "abs_err_T2": float(abs(T[i, 1] - exact[i, 1])),
            "max_rel_err_over_modes": float(np.max(rel[i])),
        }
    return {
        "site": "solver/finite_support.py:115  np.arccos(np.clip(v, -1.0, 1.0))",
        "n_points_outside": int(outside.size),
        "max_dev_of_returned_from_its_value_at_v_eq_1": dev_from_edge,
        "n_returning_exactly_the_v_eq_1_value": int(np.sum(np.all(T == T1, axis=1))),
        "max_rel_err_vs_exact_recurrence": float(np.max(rel)),
        "max_abs_err_vs_exact_recurrence": float(np.max(np.abs(T - exact))),
        "eval_points": [float(x) for x in outside],
        "per_point": per_point,
        "n_warnings_from_even_cheb_itself": n_warn,
        "note": ("every |v| > 1 is silently evaluated AT v = 1 (deviation exactly 0.0), "
                 "with no exception and no warning from even_cheb itself"),
    }


# ---------------------------------------------------------------------------
# G3 -- H2: the a-dependence of the out-of-support fabrication
# ---------------------------------------------------------------------------

def gate_3_out_of_support():
    """The prefactor (1 - v^2)^p uses the UNCLIPPED v.  Whether that is a NaN
    (flagged) or a finite fabricated number (silent) depends on whether p = 1/a
    is an integer.  Truth outside the support is Omega == 0 exactly -- the
    module's own docstring, lines 50-53."""
    vs = np.array([1.01, 1.1, 1.5, 2.0, 5.0])
    rows, n_silent, n_flagged = [], 0, 0
    for a in (1.0, 0.5, 1.0 / 3.0, 0.25, 0.2, 0.3, 0.35, 0.7, 0.9, 1.2):
        p = 1.0 / a
        is_int = float(p).is_integer() or abs(p - round(p)) < 1e-12
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            ops = FiniteSupportOps(p, 6, vs, N=400, n_int=60)
        b = np.zeros(6); b[0] = 1.0
        with warnings.catch_warnings(record=True) as wf:
            warnings.simplefilter("always")
            f = ops.fields(b)[0]
        finite = bool(np.all(np.isfinite(f)))
        if finite:
            n_silent += 1
        else:
            n_flagged += 1
        rows.append({
            "a": float(a), "p": float(p), "p_is_integer": bool(is_int),
            "returned_Omega_outside": [None if not np.isfinite(x) else float(x) for x in f],
            "truth": 0.0,
            "all_finite": finite,
            "max_abs_returned": (float(np.max(np.abs(f))) if finite else None),
            "ratio_to_gauge_amplitude": (float(np.max(np.abs(f))) if finite else None),
            "sign_matches_interior": (bool(np.all(f < 0)) if finite else None),
            "n_warnings_during_construction": len(w),
            "n_warnings_in_the_fields_call_itself": len(wf),
        })
    # grid independence of the fabricated values -- structural, or an artifact?
    grid = {}
    for K in (6, 12, 24):
        for N in (400, 1600):
            o = FiniteSupportOps(2.0, K, np.array([2.0]), N=N, n_int=60)
            bb = np.zeros(K); bb[0] = 1.0
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                grid[f"K{K}_N{N}"] = float(o.fields(bb)[0][0])
    vals = np.array(list(grid.values()))
    return {
        "site": "solver/finite_support.py:157-162, 347  (1 - v**2) ** p on the UNCLIPPED v",
        "truth_outside_support": "Omega == 0 exactly (module docstring lines 50-53)",
        "eval_points": [float(x) for x in vs],
        "n_values_of_a_probed": len(rows),
        "n_a_silently_fabricating": n_silent,
        "n_a_flagged_by_nan": n_flagged,
        "silent_set": "a = 1/n for integer n (p integer): the fractional power never goes complex",
        "worst_fabricated_value": max(
            (r["max_abs_returned"] for r in rows if r["max_abs_returned"] is not None)),
        "grid_independence_at_a_0p5_v_2p0": grid,
        "grid_spread_rel": float((vals.max() - vals.min()) / abs(vals.mean())),
        "per_a": rows,
    }


# ---------------------------------------------------------------------------
# G4 -- H3: an evaluation point that lands on a quadrature node
# ---------------------------------------------------------------------------

def gate_4_node_collision():
    N = 400
    u, _ = cheb_quad(N)
    node = float(u[137])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ops = FiniteSupportOps(2.0, 6, np.array([0.5]), N=N, n_int=200)
        ref_ops = FiniteSupportOps(2.0, 6, np.array([0.5]), N=N + 1, n_int=200)
    # measured around the COLLIDING EVALUATION only -- construction emits 2
    # warnings from the v = 1 row of the internal velocity grid (benign, see G5)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        hit = ops._hilbert_matrix(np.array([node]))[0]
        near = ops._hilbert_matrix(np.array([node + 1e-7]))[0]
    n_warn_eval = len(w)
    ref = ref_ops._hilbert_matrix(np.array([node]))[0]      # same point, no collision
    rel_hit = float(np.max(np.abs(hit - ref) / np.maximum(np.abs(ref), 1e-14)))
    rel_near = float(np.max(np.abs(near - ref) / np.maximum(np.abs(ref), 1e-14)))
    # do the module's OWN default collocation nodes ever collide?
    collisions = 0
    for K in (8, 16, 24, 32):
        cv = 0.5 * (1.0 - np.cos(np.pi * (np.arange(K - 1) + 0.5) / (K - 1)))
        for Nq in (800, 2000):
            uq, _ = cheb_quad(Nq)
            collisions += int(np.sum(np.min(np.abs(cv[:, None] - uq[None, :]), axis=1) < 1e-15))
    return {
        "site": "solver/finite_support.py:178  d = np.where(np.abs(d) < 1e-300, 1e-300, d)",
        "colliding_point": node, "N": N,
        "rel_err_of_the_colliding_evaluation": rel_hit,
        "rel_err_of_a_point_1e-7_away": rel_near,
        "n_warnings_from_the_colliding_evaluation_itself": n_warn_eval,
        "amplification": (rel_hit / rel_near if rel_near > 0 else None),
        "n_collisions_among_module_default_collocation_nodes": collisions,
        "note": ("the floor turns the singular divided difference into exactly 0/1e-300 = 0, "
                 "dropping the term instead of flagging it; the module's own default node "
                 "sets never collide, so this is reachable only through the public "
                 "FiniteSupportOps(v_eval=...) entry point"),
    }


# ---------------------------------------------------------------------------
# G5 -- H4: v = 0 and v = 1 in the log term  (SOUNDNESS gate)
# ---------------------------------------------------------------------------

def gate_5_log_endpoints():
    ops = FiniteSupportOps(2.0, 4, np.array([0.5]), N=400, n_int=100)
    out = {}
    for name, v in (("v_eq_0", 0.0), ("v_eq_1", 1.0), ("v_eq_interior", 0.5)):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            H = ops._hilbert_matrix(np.array([v]))
        out[name] = {
            "finite": bool(np.all(np.isfinite(H))),
            "n_warnings": len(w),
            "warnings": [str(x.message) for x in w],
            "values": [None if not np.isfinite(x) else float(x) for x in H[0]],
        }
    out["verdict"] = (
        "v=0 is FLAGGED: the return is non-finite (+-inf), so nothing plausible is "
        "fabricated -- but note it carries NO warning, because log(0) = -inf under the "
        "errstate('divide') suppression is a valid inf rather than an invalid operation. "
        "v=1 is the reverse: it WARNS (0 * inf -> nan in the multiply) and then returns a "
        "correct finite value, because the phi_v != 0 mask discards the nan. Neither is a "
        "silent wrong number, so H4 does NOT contribute to the gate.")
    return out


# ---------------------------------------------------------------------------
# G6 -- H5/H6: the honesty of the `converged` flag
# ---------------------------------------------------------------------------

def gate_6_converged_flag():
    warnings.simplefilter("ignore")
    ladder = []
    for K in (1, 2, 3, 4, 6, 8, 12, 16, 24):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            P = FiniteSupportProfile(a=0.5, K=K, N=400, n_int=100)
            r = P.solve(max_iter=40)
        ind = independent_residual(0.5, r["b"], r["Xc"])
        ladder.append({
            "K": K,
            "collocation_rows": K - 1, "unknowns": K + 1,
            "equation_rows_present": bool(K - 1 > 0),
            "reported_converged": bool(r["converged"]),
            "reported_residual": float(r["residual"]),
            "independent_residual_off_grid": ind,
            "amplification_independent_over_reported": (
                float(ind / r["residual"]) if r["residual"] > 0 else None),
            "Xc": float(r["Xc"]),
            "iterations": int(r["iterations"]),
            "n_warnings": len(w),
        })
    conv = [row for row in ladder if row["reported_converged"]]
    xcs = np.array([row["Xc"] for row in conv])
    # the stale-history gap: `converged` reads hist[-1], `residual` re-evaluates
    P = FiniteSupportProfile(a=0.3, K=16, N=800)
    r = P.solve()
    stale = abs(float(r["residual"]) - float(r["history"][-1]))
    r1 = P.solve(max_iter=1)
    stale1 = abs(float(r1["residual"]) - float(r1["history"][-1]))
    return {
        "site_flag": "solver/finite_support.py:309-324  hist appended at loop TOP; "
                     "converged = hist[-1] < 1e-8 while the break uses tol = 1e-12",
        "K_ladder_at_a_0p5": ladder,
        "n_K_reporting_converged": len(conv),
        "n_K_total": len(ladder),
        "K_eq_1_degenerate": {
            "collocation_rows": 0,
            "reported_converged": ladder[0]["reported_converged"],
            "reported_residual": ladder[0]["reported_residual"],
            "independent_residual": ladder[0]["independent_residual_off_grid"],
            "note": ("with K = 1 the profile equation is evaluated at ZERO points: the "
                     "square system is the gauge row plus the edge row, so the reported "
                     "residual is exactly 0.0 and converged is True by construction"),
        },
        "Xc_spread_among_self_reported_converged": {
            "min": float(xcs.min()), "max": float(xcs.max()),
            "spread_rel": float((xcs.max() - xcs.min()) / xcs.mean()),
            "values_by_K": {str(row["K"]): row["Xc"] for row in conv},
        },
        "stale_history_gap_a0p3_K16": stale,
        "stale_history_gap_max_iter_1": stale1,
        "docstring_claim": ("lines 22-31 say the module DOES NOT CONVERGE and reports "
                            "residual 0.63 at a = 0.5; this battery makes no claim about "
                            "whether it converges -- only about the honesty of the flag"),
    }


# ---------------------------------------------------------------------------
# G7 -- H7: degenerate constructor arguments
# ---------------------------------------------------------------------------

def gate_7_degenerate_construction():
    rows = []
    for a in (0.0, -0.5, -1e-13, np.nan, np.inf, -np.inf, 1e-13):
        val, exc, w = capture(FiniteSupportProfile, a=a, K=6, N=200, n_int=50)
        entry = {"arg": "a", "value": (None if not np.isfinite(a) else float(a)),
                 "value_repr": repr(a), "exception": exc, "n_warnings": len(w),
                 "constructed": exc is None,
                 "p": (float(val.p) if val is not None and np.isfinite(val.p) else
                       (repr(val.p) if val is not None else None))}
        if val is not None:
            r, e2, w2 = capture(val.solve, max_iter=15)
            entry["solve_exception"] = e2
            entry["solve_converged"] = (bool(r["converged"]) if r else None)
            entry["solve_residual"] = (None if r is None or not np.isfinite(r["residual"])
                                       else float(r["residual"]))
            entry["solve_residual_repr"] = (repr(r["residual"]) if r else None)
        rows.append(entry)
    krows = []
    for K in (1, 2, 3, 0):
        val, exc, w = capture(FiniteSupportProfile, a=0.5, K=K, N=200, n_int=50)
        e = {"arg": "K", "value": K, "exception": exc, "n_warnings": len(w),
             "constructed": exc is None,
             "n_collocation_nodes": (int(val.v.size) if val is not None else None)}
        if val is not None:
            r, e2, _ = capture(val.solve, max_iter=15)
            e["solve_exception"] = e2
            e["solve_converged"] = (bool(r["converged"]) if r else None)
            e["solve_residual"] = (float(r["residual"]) if r else None)
            e["Xc"] = (float(r["Xc"]) if r else None)
        krows.append(e)
    return {
        "site": "solver/finite_support.py:250-259 -- no guard on a, K, N, c, n_int anywhere",
        "a_cases": rows,
        "K_cases": krows,
        "n_a_cases": len(rows),
        "n_a_raising": sum(1 for r in rows if r["exception"] is not None),
        "n_a_constructed_silently": sum(1 for r in rows
                                        if r["exception"] is None and r["n_warnings"] == 0),
        "worst": ("a = inf constructs silently with p = 0.0, i.e. the algebraic edge zero "
                  "(1-v^2)^p is replaced by the constant 1 and the ansatz the whole module "
                  "is built on is gone, with no exception and no warning"),
    }


# ---------------------------------------------------------------------------
# G8 -- H9: poisoned state through every evaluation entry point
# ---------------------------------------------------------------------------

def gate_8_poisoned_state():
    warnings.simplefilter("ignore")
    K = 12
    P = FiniteSupportProfile(a=0.5, K=K, N=400, n_int=100)
    clean = np.zeros(K); clean[0] = 1.0
    cases = {
        "clean": (clean, 2.4),
        "nan_in_b": (np.where(np.arange(K) == 3, np.nan, clean), 2.4),
        "inf_in_b": (np.where(np.arange(K) == 3, np.inf, clean), 2.4),
        "nan_Xc": (clean.copy(), np.nan),
        "inf_Xc": (clean.copy(), np.inf),
        "negative_Xc": (clean.copy(), -5.0),
        "zero_Xc": (clean.copy(), 0.0),
        "huge_b": (clean * 1e300, 2.4),
    }
    entries = ["system", "system_jacobian", "operator_norm", "profile_values",
               "gauge", "edge_condition"]
    table, n_silent = {}, 0
    for name, (b, Xc) in cases.items():
        row = {}
        for fn in entries:
            f = getattr(P, fn)
            if fn == "gauge":
                val, exc, w = capture(f, b)
            else:
                val, exc, w = capture(f, b, Xc)
            if exc is not None:
                row[fn] = "raised:" + exc
            else:
                v = val[1] if fn == "profile_values" else val
                row[fn] = finite_report(v)
        table[name] = row
        if name != "clean":
            poisoned_finite = [k for k, v in row.items() if v == "finite"]
            n_silent += len(poisoned_finite)
            table[name]["_silently_finite_entry_points"] = poisoned_finite
    return {
        "site": "every evaluation entry point -- no input validation anywhere in the module",
        "n_entry_points": len(entries),
        "n_poisoned_cases": len(cases) - 1,
        "table": table,
        "n_poisoned_entrypoint_pairs_returning_a_FINITE_number": n_silent,
        "n_poisoned_entrypoint_pairs_total": (len(cases) - 1) * len(entries),
        "note": ("nan/inf in the coefficient vector PROPAGATE (good); a negative or zero "
                 "support radius does NOT -- X_c < 0 is physically impossible and every "
                 "entry point accepts it"),
    }


# ---------------------------------------------------------------------------
# G9 -- H8: the kill switch computed by inverting a matrix nobody rank-tested
# ---------------------------------------------------------------------------

def gate_9_operator_norm():
    warnings.simplefilter("ignore")
    rows = []
    for K in (4, 8, 12, 16):
        P = FiniteSupportProfile(a=0.5, K=K, N=400, n_int=100)
        r = P.solve(max_iter=40)
        M = P.system_jacobian(r["b"], r["Xc"])
        cond = float(np.linalg.cond(M))
        nrm, exc, w = capture(P.operator_norm, r["b"], r["Xc"])
        rows.append({"K": K, "cond_of_jacobian": cond,
                     "operator_norm_returned_finite": nrm is not None and np.isfinite(nrm),
                     "exception": exc, "n_warnings": len(w),
                     "reported_converged": bool(r["converged"])})
    # a deliberately rank-deficient state: two identical rows are impossible to
    # build without editing, so use X_c -> 0, which makes the edge row degenerate
    P = FiniteSupportProfile(a=0.5, K=8, N=400, n_int=100)
    b = np.zeros(8); b[0] = 1.0
    deg = {}
    for Xc in (1e-14, 0.0, -1.0):
        M = P.system_jacobian(b, Xc)
        cond = np.linalg.cond(M)
        nrm, exc, w = capture(P.operator_norm, b, Xc)
        deg[str(Xc)] = {"cond": (None if not np.isfinite(cond) else float(cond)),
                        "cond_repr": repr(float(cond)),
                        "returned": (None if nrm is None or not np.isfinite(nrm)
                                     else float(nrm)),
                        "exception": exc, "n_warnings": len(w)}
    return {
        "site": "solver/finite_support.py:336-342  np.linalg.inv(M), no rank or "
                "condition test; this is the module's declared KILL SWITCH",
        "clean_states": rows,
        "degenerate_Xc": deg,
        "note": ("no value of ||A|| is reported by this leg -- only whether a number "
                 "comes back at all, and the conditioning of the matrix it came from"),
    }


# ---------------------------------------------------------------------------
# G10 -- blast radius, measured
# ---------------------------------------------------------------------------

def gate_10_blast_radius():
    def rg(pattern):
        p = subprocess.run(["grep", "-rn", "--include=*.py", pattern, "."],
                           cwd=ROOT, capture_output=True, text=True)
        return [l for l in p.stdout.splitlines() if l.strip()]

    importers = [l for l in rg("finite_support")
                 if ("import" in l and "finite_support" in l.split(":", 2)[-1])
                 and not l.startswith("./solver/finite_support.py")
                 and "experiments/p2_route_fsa" not in l
                 and "test_finite_support_adversarial" not in l]
    refs = [l for l in rg("finite_support")
            if not l.startswith("./solver/finite_support.py")
            and "experiments/p2_route_fsa" not in l
            and "test_finite_support_adversarial" not in l]
    return {
        "importers_outside_this_leg": importers,
        "n_importers": len(importers),
        "n_references_of_any_kind": len(refs),
        "references": refs,
        "capabilities_entry": "capabilities.py:535-538  object 'SUPERSEDED -- do not use', "
                              "validated 'nothing'",
        "verdict": ("ZERO importers: every finding in this battery is a LATENT trap. "
                    "No banked number in the repository is contaminated by any of it."
                    if not importers else
                    "LIVE call sites exist -- escalate as contamination, not as a latent trap"),
    }


# ---------------------------------------------------------------------------

def main():
    warnings.simplefilter("ignore")
    res = {
        "leg": 124, "route": "ROUTE-FSA", "target": "solver/finite_support.py",
        "gate": ("Under an adversarial battery of degenerate or poisoned inputs, does "
                 "solver/finite_support.py ever silently return a wrong result instead "
                 "of flagging the input?"),
        "target_module_edited": False,
        "G1_known_answer_positive_control": gate_1_known_answer(),
        "G2_clip_H1": gate_2_clip(),
        "G3_out_of_support_H2": gate_3_out_of_support(),
        "G4_node_collision_H3": gate_4_node_collision(),
        "G5_log_endpoints_H4": gate_5_log_endpoints(),
        "G6_converged_flag_H5_H6": gate_6_converged_flag(),
        "G7_degenerate_construction_H7": gate_7_degenerate_construction(),
        "G8_poisoned_state_H9": gate_8_poisoned_state(),
        "G9_operator_norm_H8": gate_9_operator_norm(),
        "G10_blast_radius": gate_10_blast_radius(),
    }

    g1 = res["G1_known_answer_positive_control"]
    silent = []
    if res["G2_clip_H1"]["n_returning_exactly_the_v_eq_1_value"] > 0:
        silent.append("H1 even_cheb clip")
    if res["G3_out_of_support_H2"]["n_a_silently_fabricating"] > 0:
        silent.append("H2 out-of-support fabrication (a = 1/n only)")
    if res["G4_node_collision_H3"]["rel_err_of_the_colliding_evaluation"] > 1e-8:
        silent.append("H3 quadrature-node collision")
    if res["G6_converged_flag_H5_H6"]["K_eq_1_degenerate"]["reported_converged"]:
        silent.append("H5 converged flag on a system with zero equation rows")
    if res["G7_degenerate_construction_H7"]["n_a_constructed_silently"] > 0:
        silent.append("H7 degenerate a accepted silently")

    res["summary"] = {
        "positive_control_G1": g1["verdict"],
        "positive_control_max_err": g1["max_abs_err_N8000"],
        "silent_corruption_sites": silent,
        "n_silent_corruption_sites": len(silent),
        "gate_answer": "YES" if silent else "NO",
        "action": ("ESCALATE, DO NOT PATCH -- the module stays byte-identical to origin/main"
                   if silent else
                   "CONFIRMED ROBUST -- bank the battery as a permanent regression test"),
        "blast_radius": res["G10_blast_radius"]["verdict"],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    def _jsonable(o):
        if isinstance(o, np.bool_):
            return bool(o)
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(f"not JSON serializable: {type(o)}")

    OUT.write_text(json.dumps(res, indent=2, sort_keys=False, default=_jsonable) + "\n")
    s = res["summary"]
    print(f"G1 positive control : {s['positive_control_max_err']:.3e}  -> {g1['verdict'][:40]}")
    print(f"silent-corruption sites: {s['n_silent_corruption_sites']}")
    for x in silent:
        print("   -", x)
    print("GATE ANSWER:", s["gate_answer"], "|", s["action"])
    print("blast radius:", s["blast_radius"][:70])
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
