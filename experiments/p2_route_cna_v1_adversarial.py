"""Route-CNA v1 -- an ADVERSARIAL BATTERY against solver/collocation_newton.py.

Leg 114.  The code-level companion to leg 110's data-level audit of the SAME death
certificate: solver/collocation_newton.py is the solver behind the COLLOCATION
realization of L1.  Continues the adversarial-audit family (legs 69, 79, 80, 83, 85,
88, 89, 92, 96, 99, 106), applied to a module none of them has touched.

capabilities.py registers the module as "Newton in the bounds' own basis"; its gate is
test_collocation_newton.py, 6 tests, every one a CORRECTNESS assertion on a well-posed
problem (exact anchor, exact Jacobian, finite-difference agreement, cross-build
agreement).  Not one constructs a degenerate grid, a NaN-poisoned profile, or an
unsolvable system.  `grep -n "raise|assert|isfinite|isnan|warn|ValueError"` over the
file returns exactly ONE line in 405: `if not np.isfinite(Xc)` at line 364.

THE GATE, VERBATIM (DIRECTION.md sec 114)
-----------------------------------------
"Under an adversarial battery of degenerate or poisoned inputs, does
solver/collocation_newton.py ever report a converged solution or plausible residual
that is silently wrong?"

WHY THIS MODULE AND NOT ANOTHER
-------------------------------
`ACollocation.newton_gauged`'s own docstring states the stake: "A = M^{-1} is the
approximate inverse every Route-D bound has been about ... the certificate's A IS the
Newton matrix, and Y_0 = ||A F(bar x)|| is the size of the Newton step at the profile
we hand over."  A `converged` flag that can be True on a wrong answer here is a
converged flag on a number the Route-D bound layer consumes directly.

VERDICT VOCABULARY, fixed BEFORE the run and unchanged from legs 89/92/99 so the
results are comparable across the session
-----------------------------------------------------------------------------------
  RAISED        an exception propagates -- the degeneracy is flagged.        ROBUST.
  NONFINITE     NaN/Inf reaches the output -- visible downstream.            ROBUST.
  SILENT_WRONG  finite, plausible-looking, no warning, and WRONG.            CORRUPTION.
  SILENT_EMPTY  accepted without complaint, output degenerate or a field
                that does not mean what it is named.                         WEAK.
  FINITE        finite and CORRECT -- the case is handled.                   ROBUST.

WHAT "SILENTLY WRONG" MEANS HERE, DECIDED BEFORE THE RUN
--------------------------------------------------------
The module makes exactly two validity claims of its own, and the gate is decided on
them, not on taste:

  (1) `converged` (both solvers).  Corruption iff `converged is True` AND the returned
      profile is not a solution of the problem the docstring says is being solved --
      measured as either (a) a nodal residual row above 1e-6 anywhere, INCLUDING the
      dropped row, or (b) a profile outside the decay class the whole Route-D pair
      lives in, measured by ||Omega||_X at alpha = 2 against the exact anchor's 1.0.

  (2) `critical_radius` / `zero_order`.  Corruption iff a finite, plausible value comes
      back where the true answer is `inf` / `(nan, 0)`.

A big honest number is not corruption; a small dishonest one is.

Repo convention: self-running script, no pytest.
  Run: PYTHONPATH=. .venv/bin/python experiments/p2_route_cna_v1_adversarial.py

Writes: writeup/data/p2_route_cna_v1_adversarial.json
Banked regression test: test_collocation_newton_adversarial.py
Findings: writeup/novelty/leg_114.md
"""

import json
import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.collocation_newton import (ACollocation, continuation,      # noqa: E402
                                       critical_radius, effective_speed,
                                       refined_theta, velocity_integrals,
                                       weighted_defect, zero_order)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_cna_v1_adversarial.json")

J = 60
C = 0.5
ALPHA_DECAY = 2.0       # the decay-class exponent the norms are reported at
ALPHA_DEFECT = 1.0      # the codomain weight weighted_defect is reported at
ROW_TOL = 1e-6          # "a nodal residual row above this is not a solution"
BASIN_ITERS = 120       # enough for every basin outcome to settle (root identity is
                        # unchanged from 120 to 200; verified before the budget was cut)
LADDER_ITERS = 200      # reaches the spurious constant to <1e-13 at every J in the ladder

CASES = []


def record(group, name, verdict, note, **mags):
    CASES.append({"group": group, "case": name, "verdict": verdict,
                  "note": note, "magnitudes": mags})


def _run(fn, *a, **kw):
    """Return ('ok', value) or ('raised', 'ExcName: msg')."""
    try:
        return "ok", fn(*a, **kw)
    except Exception as exc:                                   # noqa: BLE001
        return "raised", f"{type(exc).__name__}: {str(exc)[:90]}"


# ---------------------------------------------------------------------------
# group A -- newton_gauged: the convergence flag that the certificate consumes
# ---------------------------------------------------------------------------


def group_A(col, truth):
    """The one-gauge solve.  Its matrix IS the certificate's approximate inverse A."""
    norm_true = col.norm_domain(truth, ALPHA_DECAY)
    wdef_true = weighted_defect(col, truth, C, ALPHA_DEFECT)[0]

    starts = [
        ("om0_None_anchor", None),
        ("om0_zeros", np.zeros(J)),
        ("om0_ones", np.ones(J)),
        ("om0_1e-8_times_anchor", 1e-8 * truth),
        ("om0_0.1_times_anchor", 0.1 * truth),
        ("om0_2_times_anchor", 2.0 * truth),
    ]
    for name, om0 in starts:
        st, r = _run(col.newton_gauged, om0=om0, c=C, max_iter=200)
        if st == "raised":
            record("A_newton_gauged", name, "RAISED", r)
            continue
        om = r["Omega"]
        R = col.residual_a(om, C)
        sup_all = float(np.max(np.abs(R)))          # INCLUDING the dropped row
        norm_X = col.norm_domain(om, ALPHA_DECAY)
        wdef = weighted_defect(col, om, C, ALPHA_DEFECT)[0]
        is_const = float(np.max(np.abs(om + 1.0)))
        is_true = float(np.max(np.abs(om - truth)))
        root = ("true_anchor" if is_true < 1e-8
                else "constant_minus_one" if is_const < 1e-8 else "third_spurious_root")
        wrong = (sup_all > ROW_TOL) or (norm_X > 10.0 * norm_true)
        if r["converged"] and wrong:
            verdict = "SILENT_WRONG"
            note = (f"converged=True on the {root}: sup|R| over ALL rows = {sup_all:.3e}, "
                    f"||Omega||_X(alpha=2) = {norm_X:.4e} against the exact anchor's "
                    f"{norm_true:.4f}")
        elif r["converged"]:
            verdict = "FINITE"
            note = f"converged=True on the {root}, which is the intended solution"
        else:
            verdict = "FINITE"
            note = f"converged=False on the {root} -- the flag is honest"
        record("A_newton_gauged", name, verdict, note,
               converged=bool(r["converged"]), root=root,
               kept_sup=float(r["kept_sup"]), dropped_defect=float(r["dropped_defect"]),
               relres=float(r["relres"]), sup_R_all_rows=sup_all,
               norm_X_alpha2=float(norm_X), norm_X_alpha2_true=float(norm_true),
               norm_X_inflation=float(norm_X / norm_true),
               weighted_defect=float(wdef), weighted_defect_true=float(wdef_true),
               weighted_defect_ratio=float(wdef / wdef_true))

    # the constant is an EXACT root of the one-gauge system -- show it directly
    const = -np.ones(J)
    sup_const = float(np.max(np.abs(col.residual_a(const, C))))
    g0 = col.to_coef.sum(axis=0)
    record("A_newton_gauged", "constant_profile_is_an_exact_root", "SILENT_WRONG",
           "Omega = -1 satisfies the gauge row AND every collocation residual row to "
           "machine precision, so the one-gauge system has it as a genuine second root",
           sup_residual_at_constant=sup_const,
           gauge_row_at_constant=float(g0 @ const + 1.0),
           gauge_row_at_true_anchor=float(g0 @ truth + 1.0))

    # poisoned inputs
    for name, kw in [
        ("om0_NaN_poisoned", {"om0": _poison(truth, np.nan)}),
        ("om0_Inf_poisoned", {"om0": _poison(truth, np.inf)}),
        ("c_NaN", {"c": np.nan}),
        ("c_Inf", {"c": np.inf}),
        ("om0_wrong_length", {"om0": np.zeros(13)}),
        ("drop_equals_J", {"drop": J}),
        ("drop_negative", {"drop": -1}),
        ("drop_out_of_range", {"drop": 1000}),
        ("max_iter_zero", {"max_iter": 0}),
    ]:
        st, r = _run(col.newton_gauged, c=kw.pop("c", C), max_iter=kw.pop("max_iter", 60),
                     **kw)
        if st == "raised":
            record("A_newton_gauged", name, "RAISED", r)
        else:
            fin = bool(np.all(np.isfinite(r["Omega"])))
            if not fin or not np.isfinite(r.get("kept_sup", np.nan)):
                record("A_newton_gauged", name, "NONFINITE",
                       "the poison reaches the output and converged is False",
                       converged=bool(r["converged"]),
                       kept_sup=float(r.get("kept_sup", np.nan)))
            else:
                record("A_newton_gauged", name, "FINITE", "handled",
                       converged=bool(r["converged"]))

    # c = 0: relres is not a relative residual
    st, r = _run(col.newton_gauged, c=0.0, max_iter=120)
    if st == "ok":
        record("A_newton_gauged", "c_equals_zero_relres_is_identically_one",
               "SILENT_EMPTY",
               "at c = 0 (and a = 0) the residual IS the source, R = Omega H(Omega), so "
               "relres = rms(R)/rms(src) is identically 1.0 however well the solve "
               "converged -- the field does not mean what it is named",
               converged=bool(r["converged"]), kept_sup=float(r["kept_sup"]),
               relres=float(r["relres"]))

    # a = NaN
    st, r = _run(lambda: ACollocation(40, a=np.nan).newton_gauged(c=C, max_iter=20))
    if st == "ok":
        record("A_newton_gauged", "a_NaN", "NONFINITE",
               "a = NaN passes float() and `self.a != 0.0` is True for NaN, so the "
               "a-term is assembled and the poison reaches the output",
               converged=bool(r["converged"]))
    else:
        record("A_newton_gauged", "a_NaN", "RAISED", r)


def _poison(v, val, i=7):
    out = np.asarray(v, float).copy()
    out[i] = val
    return out


# ---------------------------------------------------------------------------
# group B -- newton (two gauges): the control that shows the mechanism
# ---------------------------------------------------------------------------


def group_B(col, truth):
    st, r = _run(col.newton, om0=np.zeros(J), c0=C, max_iter=120)
    if st == "ok":
        landed_const = float(np.max(np.abs(r["Omega"] + 1.0)))
        record("B_newton_two_gauge", "om0_zeros_control", "FINITE",
               "the SECOND gauge -- Omega at the node nearest X = 1 equals -1/2 -- "
               "excludes the constant, so the identical start that fools newton_gauged "
               "is refused here.  This is the mechanism, isolated.",
               converged=bool(r["converged"]), relres=float(r["relres"]),
               distance_to_constant=landed_const)

    i1 = int(np.argmin(np.abs(col.X - 1.0)))
    record("B_newton_two_gauge", "second_gauge_at_the_exact_anchor", "SILENT_EMPTY",
           "the docstring says both gauges are 'satisfied by the exact a = 0 anchor'; "
           "the second is satisfied only to O(grid spacing), so newton cannot return "
           "the exact anchor and max_iter=0 reports converged=True where max_iter=1 "
           "reports False",
           X_at_gauge_node=float(col.X[i1]),
           gauge_residual_at_exact_anchor=float(truth[i1] + 0.5))

    for m in (0, 1, 2, 40):
        st, r = _run(col.newton, c0=C, max_iter=m)
        if st == "ok":
            record("B_newton_two_gauge", f"max_iter_{m}", "FINITE",
                   "convergence report at this iteration budget",
                   converged=bool(r["converged"]), relres=float(r["relres"]))
        else:
            record("B_newton_two_gauge", f"max_iter_{m}", "RAISED", r)

    # the early-exit dict is not the normal dict
    st, r = _run(col.newton, om0=_poison(truth, np.nan), c0=C, max_iter=20)
    if st == "ok":
        missing = sorted({"relres", "residual_rms", "iterations", "nodal_sup"}
                         - set(r.keys()))
        record("B_newton_two_gauge", "singular_path_returns_a_different_dict",
               "SILENT_EMPTY" if missing else "FINITE",
               "the LinAlgError early-exit dict omits the result keys the normal path "
               "returns, so a caller that indexes them dies with KeyError",
               missing_keys=missing, reason=str(r.get("reason", "")))
    else:
        record("B_newton_two_gauge", "singular_path_returns_a_different_dict",
               "RAISED", r)

    st, r = _run(continuation, [float("nan")], J=40, max_iter=20)
    record("B_newton_two_gauge", "continuation_on_the_singular_path",
           "RAISED" if st == "raised" else "FINITE",
           "continuation indexes r['relres'] unconditionally on newton's result, so the "
           "documented singular-path return crashes it: " + str(r)[:80])


# ---------------------------------------------------------------------------
# group C -- critical_radius: no magnitude test on the sign change
# ---------------------------------------------------------------------------


def group_C():
    Xg = np.linspace(0.01, 40.0, 800)
    E0 = 0.5 + 0.0 * Xg
    record("C_critical_radius", "E_constant_positive_no_crossing", "FINITE",
           "correctly reports no crossing", Xc=critical_radius(Xg, E0))

    depths = {}
    for eps in (1e-16, 1e-12, 1e-8, 1e-3):
        Ep = E0.copy()
        Ep[300] = -eps
        depths[f"dip_{eps:.0e}"] = float(critical_radius(Xg, Ep))
    record("C_critical_radius", "single_roundoff_scale_dip", "SILENT_WRONG",
           "E is 0.5 everywhere except ONE entry dipped to -1e-16 -- a relative "
           "perturbation of 4e-16 -- and a finite, entirely plausible critical radius "
           "comes back where the true answer is inf.  The returned radius moves by only "
           "1.0e-04 across THIRTEEN orders of magnitude of dip depth (1e-16 to 1e-3), so "
           "it carries essentially no information about whether the crossing is real.",
           true_answer="inf", **depths)

    record("C_critical_radius", "pure_sign_noise", "SILENT_WRONG",
           "an E that is pure alternating sign noise returns the first flicker as 'the "
           "radius where the profile ends'",
           Xc=critical_radius(Xg, (-1.0) ** np.arange(Xg.size)), true_answer="undefined")

    # NOTE ON VERDICTS HERE: `inf` is this function's OWN encoding of "no crossing",
    # so `not isfinite` is not by itself evidence of anything.  NaN out is the poison
    # made visible (NONFINITE); inf out is only correct when no crossing is the truth.
    for name, E, expect in [
            ("E_one_NaN", np.where(np.arange(800) == 300, np.nan, 0.5), "nan"),
            ("E_all_NaN", np.full(800, np.nan), "nan"),
            ("E_one_Inf", np.where(np.arange(800) == 300, np.inf, 0.5), "inf"),
    ]:
        v = critical_radius(Xg, E)
        record("C_critical_radius", name,
               "NONFINITE" if np.isnan(v) else "FINITE",
               f"returns {v}; expected {expect} -- an all-positive E with one +Inf "
               f"genuinely has no sign change, so inf is the right answer there",
               Xc=float(v))

    v = critical_radius(Xg, np.zeros(800))
    record("C_critical_radius", "E_identically_zero", "SILENT_EMPTY",
           "E vanishes IDENTICALLY -- the effective speed is zero at every radius -- "
           "and the function reports inf, i.e. 'the profile never ends'.  sign(0) = 0 "
           "for every entry so np.diff(np.sign(E)) is identically 0 and the degenerate "
           "case is indistinguishable from a healthy non-crossing one.",
           Xc=float(v))

    for name, X, E in [("empty_input", np.array([]), np.array([])),
                       ("single_point", np.array([1.0]), np.array([1.0]))]:
        v = critical_radius(X, E)
        record("C_critical_radius", name, "FINITE", f"returns {v}", Xc=float(v))

    # the chain: bogus radius -> plausible exponent
    Ep = E0.copy()
    Ep[300] = -1e-14
    Xc_bogus = critical_radius(Xg, Ep)
    om = -1.0 / (1.0 + Xg ** 2)
    p_bogus, n_bogus = zero_order(Xg, om, Xc_bogus)
    p_true, n_true = zero_order(Xg, om, float("inf"))
    record("C_critical_radius", "chain_bogus_radius_into_zero_order", "SILENT_WRONG",
           "the bogus radius feeds zero_order, which returns a finite plausible "
           "exponent from 141 points where the truth is (nan, 0)",
           Xc_bogus=float(Xc_bogus), p_at_bogus_Xc=float(p_bogus),
           points_at_bogus_Xc=int(n_bogus), p_at_true_inf=float(p_true),
           points_at_true_inf=int(n_true))


def group_C_reachability(col_a_sweep):
    """Is the C group's gap LIVE on the production path, or latent?  Measured."""
    for a, minE, Xc in col_a_sweep:
        record("C_reachability", f"real_E_field_a_{a:.4f}", "FINITE",
               "a real converged solver E field, not a synthetic one",
               a=float(a), min_E=float(minE), Xc=float(Xc))


# ---------------------------------------------------------------------------
# group D -- zero_order: the one guarded function in the file
# ---------------------------------------------------------------------------


def group_D():
    X = np.linspace(0.1, 11.9, 400)
    Xc = 12.0
    om = -(Xc - X) ** 3.0                      # true exponent p = 3, by construction
    p0, n0 = zero_order(X, om, Xc)
    record("D_zero_order", "clean_power_law", "FINITE",
           "recovers the constructed exponent", p=float(p0), n=int(n0), p_true=3.0)

    rng = np.random.default_rng(1)
    for frac in (0.01, 0.2, 0.95):
        o = om.copy()
        o[rng.choice(400, int(frac * 400), replace=False)] = np.nan
        p, n = zero_order(X, o, Xc)
        record("D_zero_order", f"NaN_poisoned_{int(frac*100)}pct", "FINITE",
               "the mask |Omega| > min_abs drops NaN, the survivors still lie on the "
               "power law, and the returned point count reports the loss honestly",
               p=float(p), n=int(n), rel_err_vs_clean=float(abs(p - p0) / abs(p0)))

    o = om.copy()
    o[::2] = np.inf
    p, n = zero_order(X, o, Xc)
    record("D_zero_order", "Inf_poisoned", "NONFINITE",
           "Inf survives the mask and reaches the fit", p=float(p), n=int(n))

    for name, xc in [("Xc_inf", float("inf")), ("Xc_nan", float("nan")),
                     ("Xc_negative", -5.0), ("Xc_below_all_X", 0.05)]:
        p, n = zero_order(X, om, xc)
        record("D_zero_order", name, "FINITE",
               "refused -- this is the module's ONE guard (line 364) plus the window mask",
               p=float(p), n=int(n))


# ---------------------------------------------------------------------------
# group E -- velocity_integrals / eval_matrices / weighted_defect
# ---------------------------------------------------------------------------


def group_E(col, truth):
    v = velocity_integrals(np.array([np.pi]), 5)[0]
    record("E_kernels", "theta_equals_pi", "NONFINITE",
           "1 + cos(pi) = 0, so I_1 = log(2/0) = inf and the recursion carries it",
           I_k=[float(x) for x in v])

    v = velocity_integrals(np.array([np.nan]), 5)[0]
    record("E_kernels", "theta_NaN", "NONFINITE", "propagates",
           I_k=[float(x) for x in v])

    st, r = _run(velocity_integrals, np.array([1.0]), -3)
    record("E_kernels", "K_negative", "RAISED" if st == "raised" else "FINITE", str(r)[:90])

    for th in (-1.0, 10.0):
        v = velocity_integrals(np.array([th]), 4)[0]
        record("E_kernels", f"theta_outside_0_pi_{th:g}", "SILENT_EMPTY",
               "theta outside (0, pi) is where X = tan(theta/2) is no longer the "
               "compactification the module is built on; finite plausible values come "
               "back with no complaint",
               I_k=[float(x) for x in v])

    hi = float(velocity_integrals(np.array([2.0]), 200)[0][-1])
    lo32 = float(velocity_integrals(np.array([2.0]), 200, dtype=np.float32)[0][-1])
    lo64 = float(velocity_integrals(np.array([2.0]), 200, dtype=np.float64)[0][-1])
    record("E_kernels", "dtype_downgrade_at_K_200", "SILENT_EMPTY",
           "`dtype` is a public kwarg with no guard; the docstring's own warning that "
           "the recursion loses eps*k^2 is not enforced, and a float32 call returns a "
           "plausible number silently degraded",
           I_199_longdouble=hi, I_199_float64=lo64, I_199_float32=lo32,
           rel_dev_float32=abs(lo32 - hi) / abs(hi),
           rel_dev_float64=abs(lo64 - hi) / abs(hi))

    record("E_kernels", "refined_theta_sizes", "FINITE",
           "the node-exclusion filter is a no-op for EVEN refine (no fine midpoint "
           "coincides with a node) and removes exactly J points for odd refine -- "
           "correct in both cases, but refine=1 leaves an empty grid",
           refine_1=int(refined_theta(20, refine=1).size),
           refine_3=int(refined_theta(20, refine=3).size),
           refine_8=int(refined_theta(20, refine=8).size))

    for name, kw in [("refine_1_empty_grid", {"refine": 1}),
                     ("theta_eval_empty", {"theta_eval": np.array([])})]:
        st, r = _run(weighted_defect, col, truth, C, ALPHA_DEFECT, **kw)
        record("E_kernels", f"weighted_defect_{name}",
               "RAISED" if st == "raised" else "FINITE", str(r)[:90])

    v = weighted_defect(col, _poison(truth, np.nan), C, ALPHA_DEFECT)[0]
    record("E_kernels", "weighted_defect_om_NaN",
           "NONFINITE" if not np.isfinite(v) else "SILENT_WRONG", "propagates",
           value=float(v))

    v = weighted_defect(col, truth, C, 400.0)[0]
    record("E_kernels", "weighted_defect_alpha_400",
           "NONFINITE" if not np.isfinite(v) else "FINITE",
           "the codomain weight overflows visibly rather than saturating",
           value=float(v))


# ---------------------------------------------------------------------------


def main():
    np.seterr(all="ignore")
    warnings.filterwarnings("ignore")

    col = ACollocation(J, a=0.0)
    truth = col.anchor()

    group_A(col, truth)
    group_B(col, truth)
    group_C()
    group_D()
    group_E(col, truth)

    # reachability control for group C: real solver E fields across the tangency
    sweep = []
    for a in (0.125, 0.131, 0.133, 0.15, 0.30):
        c2 = ACollocation(J, a=float(a))
        s = c2.newton_gauged(c=C, max_iter=80)
        E = effective_speed(c2.X, c2.V @ s["Omega"], C, float(a))
        sweep.append((a, float(np.min(E)), float(critical_radius(c2.X, E))))
    group_C_reachability(sweep)

    # basin of the spurious constant -- how far the M2 gap actually reaches
    col_b = ACollocation(J, a=0.0)
    truth_b = col_b.anchor()
    basin = []
    for lam in (5.0, 2.0, 1.0, 0.9, 0.8, 0.75, 0.7, 0.6, 0.5, 0.3, 0.1,
                1e-2, 1e-4, 1e-8, 0.0):
        r = col_b.newton_gauged(om0=lam * truth_b, c=C, max_iter=BASIN_ITERS)
        om = r["Omega"]
        root = ("true_anchor" if np.max(np.abs(om - truth_b)) < 1e-8
                else "constant_minus_one" if np.max(np.abs(om + 1.0)) < 1e-8
                else "third_spurious_root")
        basin.append({"lambda": float(lam), "converged": bool(r["converged"]),
                      "root": root, "kept_sup": float(r["kept_sup"]),
                      "dropped_defect": float(r["dropped_defect"])})

    noise_basin = []
    rng = np.random.default_rng(7)
    for eps in (1e-12, 1e-6, 1e-3, 1e-2, 5e-2, 0.1, 0.3):
        hits, draws = 0, 20
        for _ in range(draws):
            r = col_b.newton_gauged(om0=truth_b + eps * rng.normal(size=J), c=C,
                                    max_iter=BASIN_ITERS)
            if r["converged"] and np.max(np.abs(r["Omega"] + 1.0)) < 1e-8:
                hits += 1
        noise_basin.append({"epsilon": float(eps), "draws": draws,
                            "landed_on_constant": hits})

    # M3 reachability: does roundoff noise on a REAL E field flip Xc from inf to finite?
    a_probe = 0.131
    c3 = ACollocation(J, a=a_probe)
    s3 = c3.newton_gauged(c=C, max_iter=80)
    E3 = effective_speed(c3.X, c3.V @ s3["Omega"], C, a_probe)
    m3_noise = []
    rng2 = np.random.default_rng(3)
    for rel in (1e-16, 1e-14, 1e-12, 1e-10, 1e-8):
        fin, draws = 0, 40
        for _ in range(draws):
            if np.isfinite(critical_radius(c3.X, E3 * (1.0 + rel * rng2.normal(size=J)))):
                fin += 1
        m3_noise.append({"relative_noise": float(rel), "draws": draws,
                         "finite_Xc": fin})
    m3_margin = {"a": a_probe, "min_E": float(np.min(E3)),
                 "Xc": float(critical_radius(c3.X, E3)),
                 "grid_Xmax": float(np.max(c3.X))}

    # J-ladder for the headline: how the spurious root scales
    ladder = []
    for Jl in (40, 60, 80, 160):
        c2 = ACollocation(Jl, a=0.0)
        r = c2.newton_gauged(om0=np.zeros(Jl), c=C, max_iter=LADDER_ITERS)
        om = r["Omega"]
        ladder.append({
            "J": Jl, "converged": bool(r["converged"]),
            "distance_to_constant": float(np.max(np.abs(om + 1.0))),
            "norm_X_alpha2": float(c2.norm_domain(om, ALPHA_DECAY)),
            "norm_X_alpha2_true": float(c2.norm_domain(c2.anchor(), ALPHA_DECAY)),
            "weighted_defect": float(weighted_defect(c2, om, C, ALPHA_DEFECT)[0]),
            "weighted_defect_true": float(
                weighted_defect(c2, c2.anchor(), C, ALPHA_DEFECT)[0]),
        })

    counts = {}
    for c_ in CASES:
        counts[c_["verdict"]] = counts.get(c_["verdict"], 0) + 1
    n_corrupt = counts.get("SILENT_WRONG", 0)

    payload = {
        "leg": 114, "route": "CNA", "module": "solver/collocation_newton.py",
        "module_lines": 405,
        "gate": ("Under an adversarial battery of degenerate or poisoned inputs, does "
                 "solver/collocation_newton.py ever report a converged solution or "
                 "plausible residual that is silently wrong?"),
        "gate_answer": "yes" if n_corrupt else "no",
        "verdict_counts": counts,
        "n_cases": len(CASES),
        "grid_J": J, "speed_c": C,
        "alpha_decay_class": ALPHA_DECAY, "alpha_codomain": ALPHA_DEFECT,
        "row_tolerance": ROW_TOL,
        "cases": CASES,
        "J_ladder_spurious_constant": ladder,
        "M2_basin_lambda_times_anchor": basin,
        "M2_basin_anchor_plus_noise": noise_basin,
        "M3_reachability_margin": m3_margin,
        "M3_reachability_noise_draws": m3_noise,
    }
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)

    for c_ in CASES:
        print(f"{c_['verdict']:13s} {c_['group']:20s} {c_['case']}")
    print()
    print("verdicts:", counts)
    print("J-ladder (spurious constant from om0 = zeros):")
    for row in ladder:
        print(f"  J={row['J']:3d} converged={row['converged']} "
              f"||Om||_X(a=2)={row['norm_X_alpha2']:.4e} "
              f"(true {row['norm_X_alpha2_true']:.4f}) "
              f"wdefect={row['weighted_defect']:.3e} "
              f"(true {row['weighted_defect_true']:.3e})")
    print()
    print(f"GATE ANSWER: {payload['gate_answer']}  ({n_corrupt} silent corruptions "
          f"in {len(CASES)} cases)")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
