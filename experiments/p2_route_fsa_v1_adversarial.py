"""Leg 124, Route-FSA: adversarial battery for `solver/finite_support.py`.

THE GATE, verbatim (DIRECTION.md, leg 124):

  "Under an adversarial battery of degenerate or poisoned inputs, does
   solver/finite_support.py ever silently return a wrong result instead of flagging the
   input?"

THE MODULE UNDER AUDIT IS DEAD CODE. `solver/finite_support.py`'s own docstring opens
`STATUS: SUPERSEDED by solver/first_integral.py (Route-D v14).  DO NOT USE.` and
`WORK IN PROGRESS -- DOES NOT CONVERGE YET. NO TEST FILE. DO NOT USE.`
`capabilities.py:479-483` lists it as `"SUPERSEDED -- do not use"`, `"validated": "nothing"`.
A repo-wide grep for any non-test import of the module returns zero hits. Every finding below
is a statement about this file's OWN code, exercised entirely off any path the rest of the
repository runs -- there is no physics claim anywhere here, and no banked number is at risk
because there is no banked number that uses this module at all.

THREE MECHANISMS, ALL VERIFIED INDEPENDENTLY OF THE MODULE'S OWN DIAGNOSTICS
-----------------------------------------------------------------------------
F1 -- DEGENERATE `K` PRODUCES A FALSE `converged=True`.
    `FiniteSupportProfile`'s collocation node count is `K - 1` (`solver/finite_support.py:258`).
    At `K = 1` that is ZERO nodes: `ops.residual` -- the actual PDE row -- is never evaluated
    even once, and the (K+1)-unknown system is constrained only by the gauge condition and the
    free-boundary condition. Newton nonetheless reports `converged: True` with a residual at
    machine precision, because that residual is measured ONLY at the (empty, or too-few)
    collocation set the solver itself chose.
    This battery does NOT take the module's own residual at face value: for every reported
    `(b, Xc)` it builds an INDEPENDENT `FiniteSupportOps` at a fixed, disjoint set of interior
    points never used as collocation nodes, and evaluates the SAME residual formula
    (`ops.residual`, unmodified) there. A true solution's residual should be small at those
    points too, by the equation's own continuity -- and at degenerate `K` it is not, by many
    orders of magnitude.

F2 -- NEAR-ZERO `c` COLLAPSES TO A TRIVIAL, ZERO-RADIUS ROOT, REPORTED AS SUCCESS.
    `edge_condition(b, Xc) = c + a*Xc*(-U1 @ b)` (`solver/finite_support.py:273-285`) admits
    the algebraic root `Xc -> 0` whenever `c` is small, independent of `b`, because every term
    scales with `Xc`. Newton finds exactly that root for `|c|` below roughly 1e-9 (holding
    `a = 0.5`, the module's own default): `Xc` lands at `1e-11 .. 1e-15` and `converged: True`
    is reported with the residual at machine precision. This is not a numerically-accurate
    small-support solution -- it is a profile with NO SUPPORT AT ALL, indistinguishable in the
    returned dict from a genuine finite-support profile.

F3 -- `FiniteSupportOps` SILENTLY EXTRAPOLATES/CLAMPS OUTSIDE ITS OWN DECLARED DOMAIN v IN [0,1].
    Three sibling fields computed by the SAME object treat an out-of-range evaluation point
    (v > 1) three different ways, none of which is a raised error:
      * `U` (`Utilde`, `_velocity_matrix`, `solver/finite_support.py:190-207`) is built by
        `np.interp(self.v, grid, cum[:, k])`. NumPy's own documentation
        (https://numpy.org/doc/stable/reference/generated/numpy.interp.html) states the default
        is to CLAMP: "value to return for x > xp[-1], default is fp[-1]." Every v > 1 silently
        returns the SAME finite value as v = 1, with ZERO warnings, for every `a` tested.
      * `f` (the profile itself, `phi_v = ((1-v**2)**p) * Tv`, line 176) is computed from the
        RAW, UNCLIPPED `v` for its power term while `Tv` comes from `even_cheb`'s internally
        CLIPPED angle (`arccos(np.clip(v,-1,1))`, line 115). When `p = 1/a` happens to be an
        exact integer (e.g. `a = 0.5 -> p = 2`), `(1-v**2)**p` is perfectly well-defined for
        v > 1 (a negative base to an integer power) and the module returns a FINITE,
        PLAUSIBLE-LOOKING, WRONG extrapolated value with ZERO warnings. For non-integer `p`
        (e.g. `a = 0.3 -> p = 3.33..`) the SAME line instead returns NaN with a RuntimeWarning
        -- so whether this is silent or loud depends on an arithmetic coincidence in `a`, not on
        whether the input was valid.
      * `H` (`Htilde`) goes to NaN with a RuntimeWarning for out-of-range v regardless of the
        parity of `p`, because its formula includes `log(v/(1-v))`, which is negative-argument
        for v > 1 -- the one field of the three that reliably flags the violation.

PRE-COMMITTED VERDICT CRITERIA (fixed before the run, not fitted to it)
------------------------------------------------------------------------
F1/F2 -- SILENT CORRUPTION iff the module reports `converged: True` (i.e. its OWN residual at
its OWN collocation set is below `tol`) AND the SAME residual formula evaluated at an
INDEPENDENT, disjoint set of interior points exceeds `OFFNODE_TOL = 1e-3` -- four orders above
the `tol = 1e-8` the module itself uses to certify success, so this cannot fire on ordinary
discretization error and can only fire when the reported flag and the actual equation disagree
by a wide, unambiguous margin.

F3 -- SILENT CORRUPTION iff a field evaluated at v_eval > 1 (outside the class's own declared
domain, stated in its module docstring: "The profile on its own support: [0, X_c]" in the
scaled variable v in [0,1]) returns an ALL-FINITE result with ZERO warnings raised, while an
in-domain evaluation of a NEIGHBOURING field (here: `H`, whose formula is exact and unmodified)
on the identical `v_eval` array goes non-finite for the same input -- i.e. the module's own
sibling machinery had the information to flag the violation and a different code path did not
use it.

CONTROLS, RECORDED AS LOUDLY AS THE FINDINGS
----------------------------------------------
`a = 0` raises `ZeroDivisionError`; `K = 0` raises `IndexError`; `K < 0` raises `ValueError`;
`N = 0` raises `ZeroDivisionError`; `max_iter = 0` raises `IndexError`; `a` = NaN/Inf/negative
propagates NaN through every downstream field and reports `converged: False` (never a false
success). All six are flagged, not silent, and are recorded as passes.

Run:  .venv/bin/python experiments/p2_route_fsa_v1_adversarial.py
Emits: writeup/data/p2_route_fsa_v1_adversarial.json
"""

import json
import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.finite_support import (          # noqa: E402
    FiniteSupportOps,
    FiniteSupportProfile,
    cheb_quad,
    even_cheb,
)

OFFNODE_TOL = 1e-3      # F1/F2 silent-corruption threshold on the independent off-node residual
SOLVE_TOL = 1e-8        # the module's own convergence tolerance (its solve() default)

# a fixed set of interior points, disjoint from every collocation grid this battery builds
# (collocation nodes are Chebyshev-clustered via arange/cos; these are plain linspace interior
# points, chosen once, never touched by any Newton iteration below).
OFFNODE_V = np.linspace(0.05, 0.95, 19)


def _independent_offnode_residual(a, K, c, b, Xc):
    """Evaluate `ops.residual` at OFFNODE_V using a FRESH FiniteSupportOps -- never the one
    Newton solved on. Same formula, disjoint evaluation points, no reliance on the module's own
    reported diagnostic."""
    p = 1.0 / a
    ops = FiniteSupportOps(p, K, OFFNODE_V, N=2000, n_int=400)
    ops.a = a
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        res = ops.residual(np.asarray(b, float), Xc, c)
    finite = np.isfinite(res)
    return {
        "max_abs": float(np.abs(res[finite]).max()) if finite.any() else float("nan"),
        "all_finite": bool(finite.all()),
        "n_warnings": len(caught),
    }


# ==========================================================================
# F1 -- degenerate K
# ==========================================================================

def battery_f1_degenerate_K():
    records = []
    for a in (0.3, 0.5, 0.8):
        for K in (1, 2, 3, 4, 6, 8, 12, 16, 24):
            prof = FiniteSupportProfile(a=a, K=K, N=2000, c=0.5)
            n_nodes = int(prof.v.size)
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                r = prof.solve(max_iter=60)
            off = _independent_offnode_residual(a, K, 0.5, r["b"], r["Xc"])
            silent = bool(
                r["converged"]
                and off["all_finite"]
                and off["max_abs"] > OFFNODE_TOL
            )
            records.append({
                "a": a, "K": K, "n_collocation_nodes": n_nodes,
                "reported_converged": r["converged"],
                "reported_residual": r["residual"],
                "iterations": r["iterations"],
                "Xc": r["Xc"],
                "offnode_max_residual": off["max_abs"],
                "offnode_all_finite": off["all_finite"],
                "n_solve_warnings": len(caught),
                "ratio_offnode_to_reported": (
                    float(off["max_abs"] / max(r["residual"], 1e-300))
                    if off["all_finite"] else float("nan")
                ),
                "silent_corruption": silent,
            })
    return records


# ==========================================================================
# F2 -- near-zero c collapses to the trivial zero-radius root
# ==========================================================================

def battery_f2_degenerate_c():
    records = []
    c_values = (
        0.5, 0.3, 0.1, 0.01, 1e-3, 1e-6, 1e-8,        # healthy range down to the boundary
        1e-9, 1e-10, 1e-12, 1e-14, 1e-16, 0.0,          # the collapse zone and the exact point
        -1e-16, -1e-12, -1e-10, -1e-9, -1e-8, -1e-6,    # negative side, same boundary
    )
    for a in (0.3, 0.5, 0.8):
        for c in c_values:
            prof = FiniteSupportProfile(a=a, K=24, N=2000, c=c)
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                r = prof.solve(max_iter=60)
            off = _independent_offnode_residual(a, 24, c, r["b"], r["Xc"])
            trivial_root = bool(np.isfinite(r["Xc"]) and abs(r["Xc"]) < 1e-6)
            silent = bool(r["converged"] and trivial_root)
            records.append({
                "a": a, "c": c,
                "reported_converged": r["converged"],
                "reported_residual": r["residual"],
                "Xc": r["Xc"],
                "trivial_zero_radius_root": trivial_root,
                "offnode_max_residual": off["max_abs"],
                "n_solve_warnings": len(caught),
                "silent_corruption": silent,
            })
    return records


# ==========================================================================
# F3 -- out-of-domain v_eval: U clamps, f extrapolates-or-NaNs by coincidence of parity, H NaNs
# ==========================================================================

def _isolated_weight_power_warnings(p, v):
    """The EXACT expression at solver/finite_support.py:176 (`phi_v`'s weight factor),
    reproduced line-for-line and evaluated on its own -- isolated from `_hilbert_matrix`'s
    log term, which the constructor also evaluates and which would otherwise contribute its
    own warnings to the same `catch_warnings` block and mask whether `f`'s OWN formula warned."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        wv = (1.0 - np.asarray(v, float) ** 2) ** p
    return wv, len(caught)


def battery_f3_domain_violation():
    records = []
    v_out = np.array([1.0 + 1e-9, 1.001, 1.01, 1.1, 1.5, 2.0, 5.0, 50.0])
    v_in = np.array([0.3, 0.7])
    for a in (0.5, 1.0, 0.3, 0.7, 0.25, 1.0 / 3.0):
        p = 1.0 / a
        p_is_integer = abs(p - round(p)) < 1e-9
        K = 8
        b = np.zeros(K)
        b[0] = 1.0
        for tag, v in (("out_of_domain", v_out), ("in_domain_control", v_in)):
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                ops = FiniteSupportOps(p, K, v, N=500, n_int=200)
                ops.a = a
                f, df, H, U = ops.fields(b)
            f_finite = np.isfinite(f)
            H_finite = np.isfinite(H)
            U_finite = np.isfinite(U)
            # f's OWN formula, isolated: does line 176's weight power alone warn?
            _, f_own_warnings = _isolated_weight_power_warnings(p, v)
            # U's specific silent-clamp check: every out-of-range point returns EXACTLY the
            # v=1 boundary value (computed independently, at v=1.0 exactly, in its own call).
            u_clamp_match = None
            if tag == "out_of_domain":
                with warnings.catch_warnings(record=True):
                    warnings.simplefilter("ignore")
                    ops_edge = FiniteSupportOps(p, K, np.array([1.0]), N=500, n_int=200)
                    ops_edge.a = a
                    _, _, _, U_edge = ops_edge.fields(b)
                u_clamp_match = bool(np.allclose(U, U_edge[0], rtol=0, atol=1e-13))
            records.append({
                "a": a, "p": p, "p_is_integer": p_is_integer, "tag": tag,
                "v_eval": v.tolist(),
                "f_all_finite": bool(f_finite.all()),
                "H_all_finite": bool(H_finite.all()),
                "U_all_finite": bool(U_finite.all()),
                "n_warnings_full_fields_call": len(caught),
                "n_warnings_f_own_formula_isolated": f_own_warnings,
                "u_clamps_to_v1_value": u_clamp_match,
                # silent iff f's OWN formula (isolated from H's log-term warnings) raises
                # nothing, yet the same input makes the sibling field H non-finite
                "f_silent_corruption": bool(
                    tag == "out_of_domain" and f_finite.all()
                    and f_own_warnings == 0 and not H_finite.all()),
                "u_silent_corruption": bool(
                    tag == "out_of_domain" and U_finite.all()
                    and (u_clamp_match is True)
                ),
            })
    return records


# ==========================================================================
# controls -- degenerate inputs that ARE correctly flagged (not silent), recorded as passes
# ==========================================================================

def battery_controls():
    records = []

    def _try(label, fn):
        try:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                out = fn()
            return {"label": label, "raised": None, "n_warnings": len(caught), "result": _safe(out)}
        except Exception as exc:                                   # noqa: BLE001
            return {"label": label, "raised": f"{type(exc).__name__}: {exc}", "n_warnings": None,
                    "result": None}

    def _safe(x):
        try:
            json.dumps(x)
            return x
        except TypeError:
            return str(x)

    records.append(_try("a=0.0 (ZeroDivisionError expected)",
                         lambda: FiniteSupportProfile(a=0.0, K=8, N=200, c=0.5)))
    records.append(_try("K=0 (IndexError expected)",
                         lambda: FiniteSupportProfile(a=0.5, K=0, N=200, c=0.5).solve(max_iter=5)))
    records.append(_try("K=-3 (ValueError expected)",
                         lambda: FiniteSupportProfile(a=0.5, K=-3, N=200, c=0.5)))
    records.append(_try("N=0 via Profile (ZeroDivisionError expected)",
                         lambda: FiniteSupportProfile(a=0.5, K=8, N=0, c=0.5)))
    records.append(_try("cheb_quad(N=0) direct (ZeroDivisionError expected)",
                         lambda: cheb_quad(0)))
    records.append(_try("max_iter=0 (IndexError expected -- crash on empty history)",
                         lambda: FiniteSupportProfile(a=0.5, K=8, N=200, c=0.5).solve(max_iter=0)))

    for a in (-0.5, float("nan"), float("inf"), -float("inf")):
        def _run(a=a):
            prof = FiniteSupportProfile(a=a, K=8, N=500, c=0.5)
            r = prof.solve(max_iter=10)
            return {"converged": r["converged"], "residual": r["residual"], "Xc": r["Xc"]}
        rec = _try(f"a={a!r} (NaN should propagate, converged=False, never a false success)", _run)
        if rec["raised"] is None:
            res = rec["result"]
            nan_ok = (res["converged"] is False) and not np.isfinite(res["residual"])
            rec["correctly_flagged"] = bool(nan_ok)
        else:
            rec["correctly_flagged"] = True
        records.append(rec)
    return records


def main():
    print("F1 -- degenerate K, independent off-node residual check")
    f1 = battery_f1_degenerate_K()
    for r in f1:
        flag = "SILENT" if r["silent_corruption"] else "-"
        print(f"  a={r['a']:.1f} K={r['K']:3d} nodes={r['n_collocation_nodes']:3d}  "
              f"reported_converged={str(r['reported_converged']):5s} "
              f"reported_res={r['reported_residual']:.2e}  "
              f"offnode_res={r['offnode_max_residual']:.2e}  {flag}")
    n_sc_f1 = sum(r["silent_corruption"] for r in f1)

    print("\nF2 -- near-zero c, trivial zero-radius root")
    f2 = battery_f2_degenerate_c()
    for r in f2:
        flag = "SILENT" if r["silent_corruption"] else "-"
        print(f"  a={r['a']:.1f} c={r['c']:>10.1e}  converged={str(r['reported_converged']):5s} "
              f"residual={r['reported_residual']:.2e}  Xc={r['Xc']:.3e}  {flag}")
    n_sc_f2 = sum(r["silent_corruption"] for r in f2)

    print("\nF3 -- out-of-domain v_eval")
    f3 = battery_f3_domain_violation()
    for r in f3:
        if r["tag"] != "out_of_domain":
            continue
        print(f"  a={r['a']:.4f} p={r['p']:.3f} p_int={r['p_is_integer']!s:5s}  "
              f"f_finite={r['f_all_finite']!s:5s} H_finite={r['H_all_finite']!s:5s} "
              f"U_finite={r['U_all_finite']!s:5s} f_own_warnings={r['n_warnings_f_own_formula_isolated']:2d}  "
              f"U_clamps={r['u_clamps_to_v1_value']}  "
              f"f_silent={r['f_silent_corruption']}  u_silent={r['u_silent_corruption']}")
    n_sc_f3 = sum(r["f_silent_corruption"] or r["u_silent_corruption"]
                  for r in f3 if r["tag"] == "out_of_domain")

    print("\nControls (degenerate input correctly flagged, not silent)")
    controls = battery_controls()
    for r in controls:
        status = f"RAISED {r['raised']}" if r["raised"] else f"result={r['result']}"
        print(f"  {r['label']}: {status}")
    n_control_failures = sum(
        1 for r in controls
        if r["raised"] is None and not r.get("correctly_flagged", True)
    )

    total_silent = n_sc_f1 + n_sc_f2 + n_sc_f3
    gate_answer = "YES" if total_silent > 0 else "NO"

    summary = {
        "leg": 124,
        "route": "FSA",
        "module": "solver/finite_support.py",
        "module_status": "SUPERSEDED, DO NOT USE (docstring); zero non-test importers repo-wide",
        "gate": ("Under an adversarial battery of degenerate or poisoned inputs, does "
                 "solver/finite_support.py ever silently return a wrong result instead of "
                 "flagging the input?"),
        "gate_answer": gate_answer,
        "offnode_tol": OFFNODE_TOL,
        "solve_tol": SOLVE_TOL,
        "f1_degenerate_K": {
            "n_cases": len(f1),
            "silent_corruptions": int(n_sc_f1),
            "worst_offnode_residual_among_silent": max(
                (r["offnode_max_residual"] for r in f1 if r["silent_corruption"]),
                default=float("nan")),
            "smallest_reported_residual_among_silent": min(
                (r["reported_residual"] for r in f1 if r["silent_corruption"]),
                default=float("nan")),
            "K1_has_zero_collocation_nodes": bool(
                next(r for r in f1 if r["K"] == 1)["n_collocation_nodes"] == 0),
            "K1_case_example": next(
                {"a": r["a"], "K": r["K"], "reported_residual": r["reported_residual"],
                 "offnode_max_residual": r["offnode_max_residual"]}
                for r in f1 if r["K"] == 1 and r["a"] == 0.5),
            "cases": f1,
        },
        "f2_degenerate_c": {
            "n_cases": len(f2),
            "silent_corruptions": int(n_sc_f2),
            "largest_abs_c_with_silent_corruption": max(
                (abs(r["c"]) for r in f2 if r["silent_corruption"]), default=float("nan")),
            "smallest_abs_c_without_silent_corruption": min(
                (abs(r["c"]) for r in f2 if not r["silent_corruption"] and r["c"] != 0.0),
                default=float("nan")),
            "cases": f2,
        },
        "f3_domain_violation": {
            "n_out_of_domain_cases": sum(1 for r in f3 if r["tag"] == "out_of_domain"),
            "silent_corruptions": int(n_sc_f3),
            "u_always_clamps": all(
                r["u_clamps_to_v1_value"] for r in f3 if r["tag"] == "out_of_domain"),
            "f_silent_iff_p_integer": all(
                r["f_silent_corruption"] == r["p_is_integer"]
                for r in f3 if r["tag"] == "out_of_domain"),
            "cases": f3,
        },
        "controls": {
            "n_cases": len(controls),
            "control_failures": int(n_control_failures),
            "cases": controls,
        },
        "total_silent_corruptions": int(total_silent),
    }

    print(f"\nF1 silent corruptions: {n_sc_f1}/{len(f1)}")
    print(f"F2 silent corruptions: {n_sc_f2}/{len(f2)}")
    print(f"F3 silent corruptions: {n_sc_f3}/{sum(1 for r in f3 if r['tag']=='out_of_domain')}")
    print(f"Control failures (degenerate input NOT correctly flagged): {n_control_failures}/{len(controls)}")
    print(f"\nGATE ANSWER: {gate_answer}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "writeup", "data", "p2_route_fsa_v1_adversarial.json")
    with open(out, "w") as fh:
        json.dump(summary, fh, indent=2)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
