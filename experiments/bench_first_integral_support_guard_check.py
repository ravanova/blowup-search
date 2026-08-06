"""BENCH REPAIR CHECK -- does the support guard change any number leg 107's callers use?

Not a leg.  This is the verification half of the bench repair that added a compact-support
guard and a NaN census to `solver/first_integral.py` after leg 107 (Route-FIA) measured the
module continuing its profile past its own free boundary and its own validator certifying
NaN-poisoned samples.  It answers three questions and computes no new mathematics:

  A. **ZERO REGRESSION, BIT FOR BIT.**  For every in-support surface the repo actually
     calls, is the repaired module's output bit-identical to the pre-repair module's?  The
     pre-repair module is loaded straight out of git (`git show <BASE>:solver/
     first_integral.py`) and imported alongside the repaired one, so this is a real A/B
     and not a re-reading of the same code.  Equality is checked on the RAW BIT PATTERN
     (`ndarray.view(np.int64)`), not with `np.allclose` -- a guard that "only" moves the
     last ulp is a guard that moved a number, and `-0.0` vs `+0.0` at the support edge
     `v = 1` is exactly the kind of difference a tolerance would hide.

  B. **THE THREE LIVE `omega_of` CALL SITES AND THE TWO LIVE `first_integral_defect`
     CALL SITES**, reproduced at their own parameters rather than at convenient ones:

       1. `experiments/p2_route_d_v14_first_integral.py:71` -- edge exponent fit,
          `omega_of(b, 1 - geomspace(1e-7, 1e-4, 60))`, `a` in {0.25, 0.3, 0.4, 0.5, 0.8},
          `K = 96`.  This is where Route-D v14's banked edge exponent comes from.
       2. `experiments/p2_route_d_v14_first_integral.py:77` -- the banked profile shape,
          `omega_of(b, linspace(0, 1, 401))`.  Note it hits `v = 1` EXACTLY, which is why
          the guard treats the support edge as inside and leaves the sign of the zero
          alone.
       3. `test_first_integral.py:233` -- the edge-exponent gate, same shape as (1) at
          `a` in {0.25, 0.3, 0.5}.
       4. `experiments/p2_route_d_v14_first_integral.py:50` and
          `test_first_integral.py:128` -- `first_integral_defect` on the whole-line
          `ACollocation` build, with a caller-supplied mask.

     Leg 107 measured 0 of 3 and 0 of 2 of these in the affected region.  This re-measures
     it as a DIFFERENCE rather than an inspection: the obligation of a repair to a latent
     bug is to prove the bug was latent.

  C. **HOW BIG THE REPAIR IS**, on the same battery leg 107 escalated: how many
     out-of-support evaluations now return the module's own documented truth instead of a
     fabricated number, and how many NaN-poisoned samples are now refused instead of
     certified.  Reported as counts and magnitudes, never as a boolean.

Runtime is dominated by the Newton solves (cached per `(module, a, K)`, which is only
sound because the repair does not touch the Newton path -- part A proves that first) and
by the whole-line `ACollocation` build in part B4.  `BENCH_SKIP_COLLOCATION=1` drops B4.
"""

import json
import os
import subprocess
import sys
import types
import warnings

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from solver import first_integral as new                                  # noqa: E402

OUT = os.path.join(ROOT, "writeup", "data",
                   "bench_first_integral_support_guard_check.json")

# the commit the repair is based on -- leg 107's tip, i.e. the module BEFORE the guard
BASE = os.environ.get("BENCH_BASE_REF", "origin/leg/fia-v1")

# the call sites' own parameters, transcribed from the files named above
SITE1_A = (0.25, 0.3, 0.4, 0.5, 0.8)          # p2_route_d_v14 block_b
SITE3_A = (0.25, 0.3, 0.5)                    # test_first_integral test 7
SITE_K = 96
EDGE_S = np.geomspace(1e-7, 1e-4, 60)
SHAPE_V = np.linspace(0.0, 1.0, 401)

A_GRID = (0.25, 0.3, 0.5, 0.8)                # leg 107's G1 grid
K_GRID = (48, 64, 96)

# B4 is the only part that builds the whole-line ACollocation, and one build is minutes
# of CPU.  One (a, J) rung of the live call sites is enough for a BIT-LEVEL A/B; the
# remaining rungs are covered by test_first_integral.py gate 6, which runs the real call
# site at J = 200, 400, 800 for a = 0.2 and 0.3 and is part of the merge gate.
COLLOCATION_CASES = ((0.2, 200),)
V_OUT = (1.0 + 1e-9, 1.0 + 1e-6, 1.001, 1.01, 1.1, 1.5, 2.0, 5.0)


def _j(x):
    """JSON-safe: NaN/inf become strings so the record is unambiguous."""
    if isinstance(x, (bool, str)) or x is None:
        return x
    x = float(x)
    if np.isnan(x):
        return "nan"
    if np.isinf(x):
        return "inf" if x > 0 else "-inf"
    return x


def load_prepatch():
    """Import `solver/first_integral.py` as it stood at BASE, from git, into a module."""
    src = subprocess.check_output(["git", "show", f"{BASE}:solver/first_integral.py"],
                                  cwd=ROOT).decode()
    mod = types.ModuleType("first_integral_prepatch")
    mod.__file__ = f"<{BASE}:solver/first_integral.py>"
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)               # noqa: S102
    return mod, src


def bitdiff(x, y):
    """Number of entries whose RAW BIT PATTERN differs, and the max absolute difference.

    Bits, not `allclose`: the question a zero-regression proof asks is whether the number
    MOVED, and `-0.0 == 0.0` is true while the two are different floats.  NaN is compared
    by bit pattern too, so a NaN that replaced a number is counted as a difference.
    """
    x = np.atleast_1d(np.asarray(x, float))
    y = np.atleast_1d(np.asarray(y, float))
    if x.shape != y.shape:
        return {"n": int(x.size), "n_bit_differences": int(x.size),
                "max_abs_diff": "shape mismatch"}
    nb = int(np.count_nonzero(x.view(np.int64) != y.view(np.int64)))
    with np.errstate(invalid="ignore"):
        mx = float(np.nanmax(np.abs(x - y))) if x.size else 0.0
    return {"n": int(x.size), "n_bit_differences": nb, "max_abs_diff": _j(mx)}


def quiet(fn):
    """Run `fn()` with the guard's own warnings recorded rather than printed."""
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        val = fn()
    return val, sum(1 for w in rec
                    if issubclass(w.category, new.FirstIntegralGuardWarning))


_SOLVED = {}


def solved(mod, tag, a, K):
    """Cached `(profile, solve-result, guard-warnings)`; the Newton solves dominate runtime.

    Caching is safe precisely because the repair does not touch the Newton path: the same
    `(a, K)` gives the same answer every time, and part A proves that answer is the
    pre-repair one bit-for-bit before any other part relies on it.
    """
    key = (tag, a, K)
    if key not in _SOLVED:
        rp = mod.ReducedProfile(a, K=K)
        r, nw = quiet(lambda: rp.solve(Xc0=10.0))
        assert r["converged"], (tag, a, K, r["residual"])
        _SOLVED[key] = (rp, r, nw)
    return _SOLVED[key]


# ---------------------------------------------------------------------------
# A -- zero regression on every in-support surface
# ---------------------------------------------------------------------------
def part_a(old):
    print("\n[A] zero-regression A/B, pre-repair module loaded from "
          f"{BASE}", flush=True)
    rows, worst = [], 0
    for a in SITE1_A:
        rpo, ro, _ = solved(old, "old", a, SITE_K)
        rpn, rn, nw_solve = solved(new, "new", a, SITE_K)
        bo, bn, Xo, Xn = ro["b"], rn["b"], ro["Xc"], rn["Xc"]
        surfaces = {
            # the Newton path itself -- untouched by design, so this must be exact
            "solve.b": bitdiff(bo, bn),
            "solve.Xc": bitdiff([Xo], [Xn]),
            "solve.residual": bitdiff([ro["residual"]], [rn["residual"]]),
            "residual(b,Xc)": bitdiff(rpo.residual(bo, Xo), rpn.residual(bn, Xn)),
            "jacobian(b,Xc)": bitdiff(rpo.jacobian(bo, Xo).ravel(),
                                      rpn.jacobian(bn, Xn).ravel()),
            # the guarded evaluation surfaces, on IN-SUPPORT input
            "omega_of(nodes)": bitdiff(rpo.omega_of(bo), rpn.omega_of(bn)),
            "omega_of(1-s)  [call site 1/3]":
                bitdiff(rpo.omega_of(bo, 1.0 - EDGE_S), rpn.omega_of(bn, 1.0 - EDGE_S)),
            "omega_of(linspace(0,1,401))  [call site 2]":
                bitdiff(rpo.omega_of(bo, SHAPE_V), rpn.omega_of(bn, SHAPE_V)),
            "e_of(nodes)": bitdiff(rpo.e_of(bo), rpn.e_of(bn)),
            "e_of(linspace(0,1,401))": bitdiff(rpo.e_of(bo, SHAPE_V),
                                               rpn.e_of(bn, SHAPE_V)),
            "even_cheb(u).T": bitdiff(old.even_cheb(SITE_K, rpo.u)[0].ravel(),
                                      new.even_cheb(SITE_K, rpn.u)[0].ravel()),
            "even_cheb(u).dT": bitdiff(old.even_cheb(SITE_K, rpo.u)[1].ravel(),
                                       new.even_cheb(SITE_K, rpn.u)[1].ravel()),
            "even_cheb([1.0])": bitdiff(old.even_cheb(SITE_K, np.array([1.0]))[0].ravel(),
                                        new.even_cheb(SITE_K, np.array([1.0]))[0].ravel()),
            # the derived quantities the far-field law is built from
            "mass": bitdiff([rpo.mass(bo, Xo)], [rpn.mass(bn, Xn)]),
            "edge_amplitude": bitdiff([rpo.edge_amplitude(bo, Xo)],
                                      [rpn.edge_amplitude(bn, Xn)]),
            "operator_norm(e)": bitdiff([rpo.operator_norm(bo, Xo)],
                                        [rpn.operator_norm(bn, Xn)]),
            "operator_norm(Omega)": bitdiff(
                [rpo.operator_norm(bo, Xo, measure="Omega")],
                [rpn.operator_norm(bn, Xn, measure="Omega")]),
            "outer_velocity.U0": bitdiff([rpo.outer_velocity(bo, Xo)[0]],
                                         [rpn.outer_velocity(bn, Xn)[0]]),
            "predicted_radius": bitdiff([rpo.predicted_radius(bo, Xo)],
                                        [rpn.predicted_radius(bn, Xn)]),
        }
        nd = sum(s["n_bit_differences"] for s in surfaces.values())
        nv = sum(s["n"] for s in surfaces.values())
        worst = max(worst, nd)
        rows.append({"a": a, "K": SITE_K, "Xc": Xn,
                     "n_values_compared": nv, "n_bit_differences": nd,
                     "warnings_raised_on_the_clean_path": nw_solve,
                     "surfaces": surfaces})
        print(f"    a={a}: {nv} values compared over {len(surfaces)} surfaces, "
              f"{nd} bit-differences, {nw_solve} warnings on the clean solve", flush=True)
    total_vals = sum(r["n_values_compared"] for r in rows)
    total_diff = sum(r["n_bit_differences"] for r in rows)
    total_warn = sum(r["warnings_raised_on_the_clean_path"] for r in rows)
    print(f"    TOTAL: {total_diff} bit-differences in {total_vals} compared values; "
          f"{total_warn} spurious warnings", flush=True)
    return {"rows": rows, "n_values_compared": total_vals,
            "n_bit_differences": total_diff,
            "n_spurious_warnings_on_clean_input": total_warn,
            "all_bit_identical": bool(total_diff == 0)}


# ---------------------------------------------------------------------------
# B -- the live call sites, at their own parameters
# ---------------------------------------------------------------------------
def part_b_profile():
    """Sites 1, 2 and 3: every `omega_of` the repo actually performs."""
    print("\n[B1-3] the three live omega_of call sites, at their own parameters",
          flush=True)
    sites = []
    for label, a_grid, v, source in (
            ("edge_exponent_fit", SITE1_A, 1.0 - EDGE_S,
             "experiments/p2_route_d_v14_first_integral.py:71"),
            ("banked_profile_shape", SITE1_A, SHAPE_V,
             "experiments/p2_route_d_v14_first_integral.py:77"),
            ("edge_exponent_gate", SITE3_A, 1.0 - EDGE_S,
             "test_first_integral.py:233")):
        rows = []
        for a in a_grid:
            rpn, rn, _ = solved(new, "new", a, SITE_K)
            det, nw = quiet(lambda: rpn.omega_of(rn["b"], v, detail=True))
            rows.append({"a": a, "n_points": det["n_points"],
                         "n_outside_support": det["n_outside_support"],
                         "max_abs_v": det["max_abs_v"],
                         "support_valid": det["support_valid"],
                         "warnings": nw})
        n_out = sum(r["n_outside_support"] for r in rows)
        n_pts = sum(r["n_points"] for r in rows)
        print(f"    {source}: {n_out} of {n_pts} evaluated points outside the support, "
              f"{sum(r['warnings'] for r in rows)} warnings", flush=True)
        sites.append({"site": label, "source": source, "rows": rows,
                      "n_points": n_pts, "n_outside_support": n_out,
                      "in_the_affected_region": bool(n_out > 0)})
    return sites


def part_b_defect():
    """Sites 4 and 5: `first_integral_defect` on the whole-line ACollocation build."""
    print("\n[B4-5] the two live first_integral_defect call sites", flush=True)
    if os.environ.get("BENCH_SKIP_COLLOCATION"):
        print("    SKIPPED (BENCH_SKIP_COLLOCATION set)", flush=True)
        return {"skipped": True}
    from solver.collocation_newton import ACollocation                    # noqa: E402
    old, _ = load_prepatch()
    rows = []
    for a, J in COLLOCATION_CASES:
        col = ACollocation(J=J, a=a)
        r = col.newton_gauged(c=0.5, tol=1e-14)
        om = r["Omega"]
        U = col.V @ om
        mask = (np.abs(om) > 1e-11) & (col.X > 0) & (col.X < 3.0)
        d_old = old.first_integral_defect(om, U, a, 0.5, mask)
        (d_new, nw) = quiet(
            lambda: new.first_integral_defect(om, U, a, 0.5, mask))
        det, _ = quiet(lambda: new.first_integral_defect(
            om, U, a, 0.5, mask, detail=True))
        bd = bitdiff([d_old], [d_new])
        rows.append({"a": a, "J": J, "defect_prepatch": _j(d_old),
                     "defect_repaired": _j(d_new),
                     "n_bit_differences": bd["n_bit_differences"],
                     "n_points": det["n_points"], "n_used": det["n_used"],
                     "n_nonfinite": det["n_nonfinite"],
                     "sample_valid": det["sample_valid"], "warnings": nw})
        print(f"    a={a} J={J}: defect {d_old:.6e} -> {d_new:.6e}, "
              f"{bd['n_bit_differences']} bit-differences, "
              f"{det['n_nonfinite']} non-finite of {det['n_points']}, "
              f"{det['n_used']} used", flush=True)
    return {"skipped": False, "rows": rows,
            "n_bit_differences": sum(r["n_bit_differences"] for r in rows),
            "n_nonfinite_total": sum(r["n_nonfinite"] for r in rows),
            "source": ["experiments/p2_route_d_v14_first_integral.py:50",
                       "test_first_integral.py:128"]}


# ---------------------------------------------------------------------------
# C -- the size of the repair, on leg 107's own battery
# ---------------------------------------------------------------------------
def part_c(old):
    print("\n[C] the size of the repair, on leg 107's own escalated battery", flush=True)
    rows, n_eval = [], 0
    n_fab_old = n_true_new = n_warned = n_raised = 0
    for a in A_GRID:
        for K in K_GRID:
            rpo, ro, _ = solved(old, "old", a, K)
            rpn, rn, _ = solved(new, "new", a, K)
            v = np.array(V_OUT)
            om_old = rpo.omega_of(ro["b"], v)
            om_new, nw = quiet(lambda: rpn.omega_of(rn["b"], v))
            om_leg, _ = quiet(
                lambda: rpn.omega_of(rn["b"], v, on_outside="extrapolate"))
            n_eval += v.size
            n_fab_old += int(np.count_nonzero(om_old != 0.0))
            n_true_new += int(np.count_nonzero(om_new == 0.0))
            n_warned += nw
            try:
                rpn.omega_of(rn["b"], v, on_outside="raise")
            except ValueError:
                n_raised += 1
            rows.append({"a": a, "K": K, "v": list(V_OUT),
                         "omega_prepatch": [_j(x) for x in om_old],
                         "omega_repaired": [_j(x) for x in om_new],
                         "omega_legacy_policy": [_j(x) for x in om_leg],
                         "legacy_reproduces_prepatch": bool(
                             np.array_equal(om_old.view(np.int64),
                                            om_leg.view(np.int64))),
                         "warnings": nw})
    n_legacy_ok = sum(1 for r in rows if r["legacy_reproduces_prepatch"])
    worst_fab = max(abs(float(x)) for r in rows for x in r["omega_prepatch"]
                    if not isinstance(x, str))
    print(f"    out-of-support evaluations: {n_eval}", flush=True)
    print(f"    pre-repair returning a FABRICATED nonzero value: {n_fab_old}/{n_eval} "
          f"(largest {worst_fab:.4f}, against a gauge amplitude of 1)", flush=True)
    print(f"    repaired returning the module's own truth 0.0: {n_true_new}/{n_eval}",
          flush=True)
    print(f"    calls that warned: {n_warned}/{len(rows)}; that raised under "
          f"on_outside='raise': {n_raised}/{len(rows)}", flush=True)
    print(f"    legacy policy reproduces the pre-repair value bit-for-bit: "
          f"{n_legacy_ok}/{len(rows)} cases", flush=True)

    # the validator half
    a, c, N = 0.3, 0.5, 400
    X = np.linspace(0.01, 3.0, N)
    E = c * np.exp(-X ** 2 / 4.0)
    U = (E - c) / a
    Om = -(E / c) ** (1.0 / a)
    ladder, absorbed_old, absorbed_new = [], 0, 0
    for nbad in (1, 10, 100, 300, 390, 397, 398, 399, 400):
        Op = Om.copy()
        Op[:nbad] = np.nan
        d_old = old.first_integral_defect(Op, U, a, c)
        d_new, nw = quiet(lambda: new.first_integral_defect(Op, U, a, c))
        d_leg, _ = quiet(
            lambda: new.first_integral_defect(Op, U, a, c, on_nonfinite="drop"))
        if not np.isnan(d_old):
            absorbed_old = max(absorbed_old, nbad)
        if not np.isnan(d_new):
            absorbed_new = max(absorbed_new, nbad)
        ladder.append({"n_nan": nbad, "n_total": N, "defect_prepatch": _j(d_old),
                       "defect_repaired": _j(d_new), "defect_legacy_policy": _j(d_leg),
                       "legacy_reproduces_prepatch": bool(
                           (np.isnan(d_old) and np.isnan(d_leg)) or d_old == d_leg),
                       "warnings": nw})
    clean_old = old.first_integral_defect(Om, U, a, c)
    clean_new, nw_clean = quiet(lambda: new.first_integral_defect(Om, U, a, c))
    print(f"    clean sample: {clean_old:.6e} -> {clean_new:.6e}, "
          f"{bitdiff([clean_old], [clean_new])['n_bit_differences']} bit-differences, "
          f"{nw_clean} warnings", flush=True)
    print(f"    largest NaN count silently absorbed: pre-repair {absorbed_old}/{N} "
          f"({100.0 * absorbed_old / N:.2f}%), repaired {absorbed_new}/{N}", flush=True)
    return {"profile": {"rows": rows, "evaluations": n_eval,
                        "prepatch_fabricated_nonzero": n_fab_old,
                        "repaired_exactly_zero": n_true_new,
                        "largest_fabricated_abs_value": worst_fab,
                        "calls_warned": n_warned, "calls": len(rows),
                        "calls_raised_under_strict_policy": n_raised,
                        "legacy_policy_reproduces_prepatch_cases": n_legacy_ok},
            "validator": {"ladder": ladder,
                          "clean_defect_prepatch": _j(clean_old),
                          "clean_defect_repaired": _j(clean_new),
                          "clean_bit_differences": bitdiff(
                              [clean_old], [clean_new])["n_bit_differences"],
                          "clean_warnings": nw_clean,
                          "max_nan_absorbed_prepatch": absorbed_old,
                          "max_nan_absorbed_repaired": absorbed_new,
                          "n_total": N}}


def main():
    old, _src = load_prepatch()
    pay = {"what": ("bench repair check: solver/first_integral.py compact-support guard "
                    "and NaN census (leg 107 / Route-FIA findings A and B)"),
           "not_a_leg": True, "base_ref_for_prepatch_module": BASE}
    pay["A_zero_regression"] = part_a(old)
    pay["B_live_call_sites"] = {"omega_of": part_b_profile(),
                                "first_integral_defect": part_b_defect()}
    pay["C_size_of_the_repair"] = part_c(old)

    a, b, c = (pay["A_zero_regression"], pay["B_live_call_sites"],
               pay["C_size_of_the_repair"])
    prof_out = sum(s["n_outside_support"] for s in b["omega_of"])
    prof_pts = sum(s["n_points"] for s in b["omega_of"])
    pay["headline"] = {
        "in_support_values_compared": a["n_values_compared"],
        "in_support_bit_differences": a["n_bit_differences"],
        "spurious_warnings_on_clean_input": a["n_spurious_warnings_on_clean_input"],
        "live_omega_of_points_evaluated": prof_pts,
        "live_omega_of_points_outside_support": prof_out,
        "live_defect_bit_differences": (None if b["first_integral_defect"]["skipped"]
                                        else b["first_integral_defect"]
                                        ["n_bit_differences"]),
        "out_of_support_evaluations": c["profile"]["evaluations"],
        "prepatch_fabricated_nonzero": c["profile"]["prepatch_fabricated_nonzero"],
        "repaired_exactly_zero": c["profile"]["repaired_exactly_zero"],
        "largest_fabricated_abs_value": c["profile"]["largest_fabricated_abs_value"],
        "max_nan_absorbed_prepatch_of_400":
            c["validator"]["max_nan_absorbed_prepatch"],
        "max_nan_absorbed_repaired_of_400":
            c["validator"]["max_nan_absorbed_repaired"],
        "leg_107_escalation_reproducible_under_legacy_policy": bool(
            c["profile"]["legacy_policy_reproduces_prepatch_cases"]
            == c["profile"]["calls"]
            and all(r["legacy_reproduces_prepatch"] for r in c["validator"]["ladder"])),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(pay, fh, indent=1, sort_keys=True, default=float)
    print("\n" + json.dumps(pay["headline"], indent=2))
    print(f"\nwrote {OUT}")
    return pay


if __name__ == "__main__":
    main()
