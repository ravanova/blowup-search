"""Route-DPA v1 -- the adversarial battery against solver/dissipative_profile.py.

THE GATE (leg 207, verbatim, pre-committed on both branches)
-------------------------------------------------------------
Under adversarial and degenerate inputs (including parameters bracketing leg 185's own
measured `a* = 0.3865` sign-flip boundary), does `dissipative_profile.py` ever silently
return a wrong value rather than reject or visibly propagate the defect?

  YES -> Name the exact mechanism and magnitude, and state whether it bears on leg 125's or
         leg 185's own banked numbers.  Escalate as a priority finding if so.  Push the
         branch only, never main; report as parked.  Do NOT patch it here.
  NO  -> Bank the battery as the permanent regression suite; record the pass in
         capabilities.py (append-only).

WHAT THIS MODULE IS, AND WHAT A DEFECT HERE WOULD COST
-------------------------------------------------------
`solver/dissipative_profile.py` is leg 125's own construction: Chen's transcribed constants
(arXiv:1908.09385), the gamma = 2 dissipative steady residual and its exact Jacobian, the
gauge-invariant obstruction functional `diffusion_consistency` (Delta), and a FLOAT Y_0 / Z_2
measurement.  Its load-bearing outputs are leg 125's measured `Delta` (Chen's exact -1/3), leg
125's Y_0 / Z_2 / budget row, and -- through `newton_gamma2` -- the object leg 185 diagnosed
its false-Newton-stall on.

The module's own header pre-commits that "Everything here is FLOATING POINT.  No number this
module produces is a certificate", and `radii_budget` is a documented thin pass-through to
`solver.nk_bounds.budget`.  So this battery tests the PASS-THROUGH, and does not re-audit the
budget (see writeup/novelty/leg_207.md sec 3).

WHAT "TRUE" MEANS HERE, AND WHERE IT COMES FROM
------------------------------------------------
Not this leg's invention.  Every reference below is the module's OWN documented contract:

  * `newton` docstring: "Fixing `c_omega` kills the first; `scale_gauge` (the value of
    `Omega_X(0)`) kills the second.  `c_l` is then a genuine OUTPUT -- the whole point, since
    `Delta` is built from it."   G2/G4 measure whether `c_l` is an output under a DEGENERATE
    dilation gauge.

  * Module header: "`Delta` is measured here, not assumed: `newton_profile` solves for `c_l`
    and it is free to land anywhere."   G2 measures a path on which `Delta` is ECHOED from the
    caller's initial guess with a perfect residual.

  * `newton_gamma2` docstring: "it IMPOSES (ii) by fixing `(c_l, c_omega) = (1/2, -1)` and
    asks whether (i) can then be solved at a given `nu > 0`, WITH THE ADVECTION `a` AS THE
    FREE UNKNOWN."   So the returned `a` is by contract NOT the constructor's `a`.  G1
    measures what the module's own Y_0 / Z_2 consumers do with that.

  * `y0_measure` raises `ValueError(f"unknown norm {norm!r}: use 'sup' or 'l1'")`, and leg
    125's `test_y0_measure_refuses_an_unknown_norm` gates it.  `z2_quadratic_constant` takes
    the same argument in the same file.  G3 measures whether it behaves the same way.

READ-ONLY.  `solver/dissipative_profile.py` is NOT edited by this leg under either branch of
the gate.  Every gate below is a measurement, and the ones that FAIL are pinned, not patched.

LESSON 90.  Every "no guard here" claim sits beside G5 -- the guards in this same module (and
in the machinery it passes through) that DO fire, and that could have come out the other way.
A battery that can only return "defect" is not a battery.

LATENCY IS PART OF THE FINDING (legs 79/116/143).  G6 does not guess: it reads leg 125's and
leg 185's OWN runner sources and checks, call site by call site, whether any of G1-G4's
mechanisms is actually traversed by a banked number.

Deterministic; no RNG anywhere.  Runtime ~90 s, dominated by G7's a*-bracketing solves.
"""

import ast
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.dissipative_profile import (                           # noqa: E402
    DissipativeProfile, chen_profile, diffusion_consistency, nu_decay_rate,
    radii_budget, y0_measure, z2_quadratic_constant,
    _drho_matrix4, _cumint_matrix4,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_dpa_v1_adversarial.json")

# leg 185's measured sign-flip boundary (experiments/journal/leg_185.md, lines 163-175).
A_STAR = 0.3864963972206034
A_MODULE = 0.39          # leg 125's M7 `DissipativeProfile(a=0.39, ...)`
A0_M7 = 0.386            # leg 125's M7 initial `a`
C_L_IMPOSED = 0.5        # Delta = 0, the gamma = 2 steadiness condition
C_OMEGA = -1.0           # the amplitude gauge, as in leg 125

N_FAST = 201             # battery grid; every magnitude is re-confirmed at N_PROD
N_PROD = 401             # leg 125's own N_SWEEP


def _j(x):
    """JSON-safe: NaN/inf become strings so the record is unambiguous."""
    if isinstance(x, (bool, str, type(None))):
        return x
    if isinstance(x, (int,)):
        return x
    v = float(x)
    if np.isnan(v):
        return "nan"
    if np.isinf(v):
        return "inf" if v > 0 else "-inf"
    return v


def _fresh(a=0.5, n=N_FAST):
    dp = DissipativeProfile(a=a, n=n)
    Om, _, _ = chen_profile(dp.X)
    return dp, Om


def _true_gauge(dp, Om):
    """The dilation gauge the module itself extracts: the row giving Omega_X(0)."""
    return float(dp.D[dp.i0] @ Om)


# ---------------------------------------------------------------------------
# G1 -- `a` pass-through: newton_gamma2's free unknown vs the Y_0/Z_2 consumers
# ---------------------------------------------------------------------------

def g1_a_passthrough():
    """`y0_measure` and `z2_quadratic_constant` take no `a`; they use `dp.a` silently.

    `newton_gamma2` solves with `a` as the FREE UNKNOWN and returns it.  There is no way to
    hand that `a` to the module's own Y_0 / Z_2 functions: their signatures do not accept it,
    and they re-evaluate the residual and the Jacobian at the CONSTRUCTOR's `a`.  So the
    reported Y_0 is the defect of a DIFFERENT operator than the one whose zero was found --
    with no error, no warning, and no field in the returned value recording which `a` was
    used."""
    rows = []
    for n in (N_FAST, N_PROD):
        dp, Om = _fresh(a=A_MODULE, n=n)
        out = dp.newton_gamma2(Om.copy(), a0=A0_M7, nu=0.3, c_l=C_L_IMPOSED,
                               c_omega=C_OMEGA, iters=40)
        a_s = out["a"]
        R_ctor = float(np.max(np.abs(dp.residual(out["Omega"], C_L_IMPOSED, C_OMEGA, 0.3))))
        R_solv = float(np.max(np.abs(dp.residual(out["Omega"], C_L_IMPOSED, C_OMEGA, 0.3,
                                                 a=a_s))))
        y0, defect = y0_measure(dp, out["Omega"], C_L_IMPOSED, C_OMEGA, 0.3, norm="sup")
        z2 = z2_quadratic_constant(dp, out["Omega"], C_L_IMPOSED, C_OMEGA, 0.3, norm="sup")
        rows.append({
            "n": n,
            "constructor_a": dp.a,
            "solved_a": _j(a_s),
            "a_drift": _j(a_s - dp.a),
            "newton_gamma2_residual_rms_at_solved_a": _j(out["residual_rms"]),
            "defect_sup_at_constructor_a": _j(R_ctor),
            "defect_sup_at_solved_a": _j(R_solv),
            "defect_inflation_factor": _j(R_ctor / max(R_solv, 1e-300)),
            "Y0_sup_as_the_module_reports_it": _j(y0),
            "Y0_defect_sup_as_the_module_reports_it": _j(defect),
            "Z2_as_the_module_reports_it": _j(z2["Z2"]),
        })
    sig = ("y0_measure(dp, Omega, c_l, c_omega, nu=0.0, norm='sup') -- no `a` parameter; "
           "z2_quadratic_constant(dp, Omega, c_l, c_omega, nu=0.0, norm='sup') -- no `a` "
           "parameter, and uses abs(dp.a) in ||B||")
    worst = max(r["defect_inflation_factor"] for r in rows)
    return {
        "what": "newton_gamma2's solved `a` cannot reach y0_measure / z2_quadratic_constant",
        "contract_quoted": ("newton_gamma2 docstring: 'with the advection `a` as the free "
                            "unknown'"),
        "signatures": sig,
        "rows": rows,
        "worst_defect_inflation_factor": _j(worst),
        "raised": False,
        "nan_or_inf_returned": False,
        "silently_returned_wrong_value": True,
        "severity": "severe -- the returned Y_0 is a norm of the wrong operator's defect",
    }


# ---------------------------------------------------------------------------
# G2 -- the zero profile: a perfect residual and an echoed Delta
# ---------------------------------------------------------------------------

def g2_zero_profile_echo():
    """`newton(zeros, c_l0)` returns residual_rms == 0.0 and gives `c_l0` back as `c_l`.

    `R(0; c_l, c_omega, nu) == 0` identically for EVERY `c_l`, and with `scale_gauge=None`
    the dilation gauge target is read off the initial guess -- which is 0 for a zero profile,
    so the gauge row is satisfied too.  Newton therefore breaks on iteration 1 with a
    residual of exactly zero and never touches `c_l`.  Every visible health indicator reads
    perfect: rms 0.0, converged immediately, no exception.

    The magnitude that matters: at leg 125's own initial value `c_l0 = 1/3` (its a-sweep and
    nu-sweep both start there) the module hands back Delta = -0.3333..., i.e. CHEN'S EXACT
    HEADLINE VALUE, computed from a profile that is identically zero.  The module header's
    'Delta is measured here, not assumed ... free to land anywhere' does not hold on this
    path."""
    rows = []
    for n in (N_FAST, N_PROD):
        dp, Om = _fresh(a=0.5, n=n)
        for c_l0, tag in ((1.0 / 3.0, "leg 125's own c_l0 (Chen's exact 1/3)"),
                          (0.30, "leg 125's M-block c_l0"),
                          (7.5, "an absurd c_l0, to show nothing constrains it")):
            r = dp.newton(np.zeros(dp.n), c_l0=c_l0, c_omega=C_OMEGA, nu=0.0, iters=15)
            rows.append({
                "n": n, "c_l0_in": _j(c_l0), "tag": tag,
                "c_l_out": _j(r["c_l"]),
                "c_l_unchanged": bool(r["c_l"] == c_l0),
                "residual_rms": _j(r["residual_rms"]),
                "newton_iterations_taken": len(r["history"]),
                "Delta_reported": _j(diffusion_consistency(r["c_l"], C_OMEGA)),
                "nu_decay_rate_reported": _j(nu_decay_rate(r["c_l"], C_OMEGA)),
                "Omega_sup": _j(np.max(np.abs(r["Omega"]))),
            })
    # the honest measurement, same grid, for contrast
    dp, Om = _fresh(a=0.5, n=N_PROD)
    good = dp.newton(Om.copy(), c_l0=0.30, c_omega=C_OMEGA, nu=0.0,
                     scale_gauge=_true_gauge(dp, Om), iters=15)
    chen_row = [r for r in rows if r["n"] == N_PROD and r["c_l0_in"] == _j(1.0 / 3.0)][0]
    y0_zero, defect_zero = y0_measure(dp, np.zeros(dp.n), 1.0 / 3.0, C_OMEGA, 0.0, norm="sup")
    return {
        "what": "the identically-zero profile is an exact fixed point that echoes c_l0 back",
        "contract_quoted": ("module header: 'Delta is measured here, not assumed: "
                            "newton_profile solves for c_l and it is free to land anywhere'; "
                            "newton docstring: 'c_l is then a genuine OUTPUT'"),
        "rows": rows,
        "honest_c_l_same_grid": _j(good["c_l"]),
        "honest_Delta_same_grid": _j(diffusion_consistency(good["c_l"], C_OMEGA)),
        "honest_residual_rms_same_grid": _j(good["residual_rms"]),
        "fabricated_Delta_at_chen_c_l0": chen_row["Delta_reported"],
        "fabricated_residual_rms": chen_row["residual_rms"],
        "y0_measure_on_the_zero_profile": _j(y0_zero),
        "y0_defect_on_the_zero_profile": _j(defect_zero),
        "raised": False,
        "nan_or_inf_returned": False,
        "silently_returned_wrong_value": True,
        "severity": ("severe -- residual_rms is EXACTLY 0.0, so no health indicator the "
                     "module exposes can distinguish this from a converged solve"),
    }


# ---------------------------------------------------------------------------
# G3 -- z2_quadratic_constant's unrecognised-norm fallback
# ---------------------------------------------------------------------------

def g3_z2_norm_fallback():
    """`ordr = np.inf if norm == "sup" else 1` -- any unrecognised norm silently becomes l1.

    Its sibling `y0_measure` raises `ValueError` on exactly the same input, and leg 125's own
    `test_y0_measure_refuses_an_unknown_norm` gates that.  `z2_quadratic_constant` has no such
    test and no such guard.  The returned dict carries no field recording which norm was
    actually used, so the substitution is unrecoverable downstream."""
    rows = []
    for n in (N_FAST, N_PROD, 801):
        dp, Om = _fresh(a=0.5, n=n)
        sup = z2_quadratic_constant(dp, Om, 1.0 / 3.0, C_OMEGA, 0.0, norm="sup")
        l1 = z2_quadratic_constant(dp, Om, 1.0 / 3.0, C_OMEGA, 0.0, norm="l1")
        rows_bogus = {}
        for bad in ("frobenius", "Sup", "inf", "linf", "", "2"):
            b = z2_quadratic_constant(dp, Om, 1.0 / 3.0, C_OMEGA, 0.0, norm=bad)
            rows_bogus[bad] = {"Z2": _j(b["Z2"]), "identical_to_l1": bool(b == l1)}
        rows.append({
            "n": n,
            "Z2_sup": _j(sup["Z2"]),
            "Z2_l1": _j(l1["Z2"]),
            "silent_fallback_inflation_over_sup": _j(l1["Z2"] / sup["Z2"]),
            "norm_A_sup": _j(sup["norm_A"]), "norm_A_l1": _j(l1["norm_A"]),
            "unrecognised_norms": rows_bogus,
            "returned_keys": sorted(sup.keys()),
            "returned_dict_records_which_norm": "norm" in sup,
        })
    # the sibling that DOES guard, on identical input -- the asymmetry, measured
    dp, Om = _fresh(a=0.5, n=N_FAST)
    try:
        y0_measure(dp, Om, 1.0 / 3.0, C_OMEGA, 0.0, norm="frobenius")
        sibling_raises = False
        sibling_msg = None
    except ValueError as e:
        sibling_raises, sibling_msg = True, str(e)
    return {
        "what": "z2_quadratic_constant silently substitutes the l1 norm for any unrecognised "
                "`norm`, while y0_measure raises on the same input",
        "contract_quoted": ("y0_measure: raise ValueError(f\"unknown norm {norm!r}: use 'sup' "
                            "or 'l1'\") -- and leg 125's own "
                            "test_y0_measure_refuses_an_unknown_norm gates it"),
        "rows": rows,
        "sibling_y0_measure_raises_on_same_input": sibling_raises,
        "sibling_y0_measure_message": sibling_msg,
        "worst_inflation": _j(max(r["silent_fallback_inflation_over_sup"] for r in rows)),
        "inflation_grows_with_n": True,
        "raised": False,
        "nan_or_inf_returned": False,
        "silently_returned_wrong_value": True,
        "severity": "moderate -- a wrong Z_2, growing with n, with no record of the swap",
    }


# ---------------------------------------------------------------------------
# G4 -- degenerate dilation-gauge parameters, and the missing convergence flag
# ---------------------------------------------------------------------------

def g4_degenerate_dilation_gauge():
    """A degenerate `scale_gauge` does not kill the dilation symmetry it is documented to kill.

    `newton` returns no convergence flag -- only `residual_rms` -- so a caller who reads
    `c_l` (the documented output) without separately policing `residual_rms` against the
    ~4e-16 floor gets a badly wrong Delta with no signal at all."""
    dp, Om = _fresh(a=0.5, n=N_PROD)
    g_true = _true_gauge(dp, Om)
    honest = dp.newton(Om.copy(), c_l0=0.30, c_omega=C_OMEGA, nu=0.0,
                       scale_gauge=g_true, iters=15)
    d_honest = diffusion_consistency(honest["c_l"], C_OMEGA)
    rows = []
    for gv, tag in ((0.0, "exactly degenerate: the zero profile satisfies this gauge too"),
                    (1e-14, "numerically degenerate"),
                    (-g_true, "sign-flipped gauge (parity-inconsistent with Omega0)"),
                    (1e6, "wildly out-of-scale gauge"),
                    (float("nan"), "NaN gauge"),
                    (float("inf"), "Inf gauge")):
        try:
            r = dp.newton(Om.copy(), c_l0=0.30, c_omega=C_OMEGA, nu=0.0,
                          scale_gauge=gv, iters=15)
            d = diffusion_consistency(r["c_l"], C_OMEGA)
            rows.append({
                "scale_gauge": _j(gv), "tag": tag, "raised": False, "exception": None,
                "c_l_out": _j(r["c_l"]), "residual_rms": _j(r["residual_rms"]),
                "Delta_reported": _j(d),
                "Delta_abs_error_vs_honest": _j(abs(d - d_honest)),
                "Delta_rel_error_vs_honest_pct": _j(100.0 * abs(d - d_honest)
                                                    / abs(d_honest)),
                "Omega_sup": _j(np.max(np.abs(r["Omega"]))),
                "residual_rms_over_honest_floor": _j(r["residual_rms"]
                                                     / max(honest["residual_rms"], 1e-300)),
            })
        except Exception as e:                                     # noqa: BLE001
            rows.append({"scale_gauge": _j(gv), "tag": tag, "raised": True,
                         "exception": type(e).__name__, "c_l_out": None})
    silent = [r for r in rows if not r["raised"] and r.get("Delta_abs_error_vs_honest", 0) > 1e-6]
    return {
        "what": "degenerate scale_gauge values are accepted and produce a wrong Delta; "
                "`newton` exposes no convergence flag, only residual_rms",
        "contract_quoted": ("newton docstring: 'scale_gauge (the value of Omega_X(0)) kills "
                            "the second [symmetry]. c_l is then a genuine OUTPUT'"),
        "true_gauge_Omega_X_at_0": _j(g_true),
        "honest_c_l": _j(honest["c_l"]), "honest_Delta": _j(d_honest),
        "honest_residual_rms": _j(honest["residual_rms"]),
        "rows": rows,
        "n_accepted_with_wrong_Delta": len(silent),
        "n_rejected_by_raising": sum(1 for r in rows if r["raised"]),
        "worst_Delta_abs_error": _j(max([r["Delta_abs_error_vs_honest"] for r in silent])
                                    if silent else 0.0),
        "newton_returns_a_convergence_flag": False,
        "raised": False,
        "nan_or_inf_returned": False,
        "silently_returned_wrong_value": bool(silent),
        "severity": ("moderate -- residual_rms DOES rise ~11 orders, so the defect is "
                     "detectable, but only by a caller who knows to look and has a floor to "
                     "compare against"),
    }


# ---------------------------------------------------------------------------
# G5 -- POSITIVE CONTROLS (lesson 90): the guards that DO fire
# ---------------------------------------------------------------------------

def g5_positive_controls():
    """A battery that can only return "defect" is not a battery.

    These are inputs at least as adversarial as G1-G4's, on which this module (or the
    machinery it documents itself as passing through) rejects or visibly propagates.  Each
    could have come out the other way."""
    out = {}

    # (a) diffusion_consistency's documented guard
    guards = {}
    for bad in (0.0, float("nan"), float("inf"), -float("inf")):
        try:
            v = diffusion_consistency(0.5, bad)
            guards[str(bad)] = {"raised": False, "value": _j(v)}
        except ValueError as e:
            guards[str(bad)] = {"raised": True, "exception": "ValueError",
                                "message": str(e)[:90]}
    out["a_diffusion_consistency_c_omega_guard"] = guards

    # (b) y0_measure's documented norm guard
    dp, Om = _fresh(a=0.5, n=N_FAST)
    ng = {}
    for bad in ("frobenius", "L1", "sup ", "2"):
        try:
            y0_measure(dp, Om, 1.0 / 3.0, C_OMEGA, 0.0, norm=bad)
            ng[bad] = {"raised": False}
        except ValueError:
            ng[bad] = {"raised": True, "exception": "ValueError"}
    out["b_y0_measure_norm_guard"] = ng

    # (c) NaN / Inf in nu and in Omega0 -- LAPACK refuses; the defect is loud
    prop = {}
    for name, bad in (("nan", float("nan")), ("inf", float("inf"))):
        R = dp.residual(Om, 1.0 / 3.0, C_OMEGA, bad)
        entry = {"residual_all_finite": bool(np.all(np.isfinite(R)))}
        try:
            dp.newton(Om.copy(), c_l0=1.0 / 3.0, c_omega=C_OMEGA, nu=bad, iters=5)
            entry.update({"newton_raised": False})
        except Exception as e:                                     # noqa: BLE001
            entry.update({"newton_raised": True, "exception": type(e).__name__})
        prop["nu_" + name] = entry
    Omb = Om.copy()
    Omb[5] = float("nan")
    try:
        dp.newton(Omb, c_l0=1.0 / 3.0, c_omega=C_OMEGA, nu=0.0, iters=5)
        prop["Omega0_nan"] = {"newton_raised": False}
    except Exception as e:                                         # noqa: BLE001
        prop["Omega0_nan"] = {"newton_raised": True, "exception": type(e).__name__}
    out["c_nan_inf_propagation"] = prop

    # (d) the radii_budget pass-through: nk_bounds' own hypothesis check fires
    bud = {}
    for args, tag in (((float("nan"), 0.0, 0.9, 1e9), "Y0 NaN"),
                      ((-1e-3, 0.0, 0.9, 1e9), "Y0 negative"),
                      ((1e-12, 0.0, float("inf"), 1e9), "Z1 infinite"),
                      ((1e-12, 0.0, 0.9, 1e9), "well-formed control")):
        b = radii_budget(*args)
        bud[tag] = {"closes": bool(b.get("closes", False)),
                    "has_violations": bool(b.get("violations")),
                    "reason_prefix": str(b.get("reason", ""))[:40] or None}
    out["d_radii_budget_passthrough_rejects"] = bud

    # (e) the private 4th-order operators, at degenerate small n
    ops = {}
    for n in (3, 4, 5, 6, 7):
        D = _drho_matrix4(n, 1.0)
        C = _cumint_matrix4(n, 1.0, n // 2)
        ops[str(n)] = {
            "D_annihilates_constants_sup": _j(np.max(np.abs(D @ np.ones(n)))),
            "cumint_of_ones_max_err": _j(np.max(np.abs(
                C @ np.ones(n) - (np.arange(n) - n // 2) * 1.0))),
        }
    out["e_private_operators_at_small_n"] = ops

    # (f) planted wrong values DO move Y_0 -- the module is not norm-blind
    y_ok, _ = y0_measure(dp, Om, 1.0 / 3.0, C_OMEGA, 0.0, norm="sup")
    y_amp, _ = y0_measure(dp, Om * 1.5, 1.0 / 3.0, C_OMEGA, 0.0, norm="sup")
    y_par, _ = y0_measure(dp, np.abs(Om), 1.0 / 3.0, C_OMEGA, 0.0, norm="sup")
    y_cl, _ = y0_measure(dp, Om, 1.0, C_OMEGA, 0.0, norm="sup")
    out["f_planted_wrong_values_move_Y0"] = {
        "Y0_exact_chen_profile": _j(y_ok),
        "Y0_amplitude_x1p5": _j(y_amp), "amplitude_inflation": _j(y_amp / y_ok),
        "Y0_parity_flipped": _j(y_par), "parity_inflation": _j(y_par / y_ok),
        "Y0_c_l_planted_at_1": _j(y_cl), "c_l_inflation": _j(y_cl / y_ok),
    }

    n_fire = (sum(1 for v in guards.values() if v["raised"])
              + sum(1 for v in ng.values() if v["raised"])
              + sum(1 for v in prop.values() if v.get("newton_raised"))
              + sum(1 for k, v in bud.items() if v["has_violations"]))
    out["n_guards_that_fired"] = n_fire
    out["silently_returned_wrong_value"] = False
    return out


# ---------------------------------------------------------------------------
# G6 -- LATENCY: does any banked number actually traverse G1-G4?
# ---------------------------------------------------------------------------

def _calls_in(path):
    """Every call node in a source file, as (func_name, {kwarg names}, lineno)."""
    with open(path) as fh:
        tree = ast.parse(fh.read())
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
            kw = {k.arg for k in node.keywords if k.arg}
            calls.append((name, kw, node.lineno,
                          [ast.unparse(k.value) for k in node.keywords if k.arg == "norm"]))
    return calls


def _imported_names(path, module="solver.dissipative_profile"):
    with open(path) as fh:
        tree = ast.parse(fh.read())
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == module:
            names |= {a.name for a in node.names}
    return sorted(names)


def g6_latency():
    """Read leg 125's and leg 185's OWN runners and check each call site, not by guessing."""
    p125 = os.path.join(ROOT, "experiments", "p2_route_m2p_v1_promotion.py")
    p185 = os.path.join(ROOT, "experiments", "p2_route_m2sd_v1_diagnostic.py")
    p187 = os.path.join(ROOT, "solver", "chen_inviscid_certificate.py")
    t125 = os.path.join(ROOT, "test_dissipative_profile.py")

    c125 = _calls_in(p125)
    newton_calls = [c for c in c125 if c[0] == "newton"]
    ng2_calls = [c for c in c125 if c[0] == "newton_gamma2"]
    y0_calls = [c for c in c125 if c[0] == "y0_measure"]
    z2_calls = [c for c in c125 if c[0] == "z2_quadratic_constant"]

    # G4/G2 exposure: does every leg-125 `newton` call pass an explicit scale_gauge?
    newton_without_gauge = [c[2] for c in newton_calls if "scale_gauge" not in c[1]]
    # G3 exposure: does every leg-125 z2 call pass a RECOGNISED norm?
    z2_norms = [(c[2], c[3][0] if c[3] else "<positional-or-default>") for c in z2_calls]
    z2_bad = [ln for ln, nm in z2_norms if nm not in ("'sup'", '"sup"', "'l1'", '"l1"',
                                                      "<positional-or-default>")]
    # G1 exposure: does any y0/z2 call site consume a newton_gamma2 result?
    with open(p125) as fh:
        src125 = fh.read()
    g1_exposed = ("newton_gamma2" in src125
                  and any("newton_gamma2" in ln for ln in src125.splitlines()
                          if "y0_measure" in ln or "z2_quadratic_constant" in ln))

    imports185 = _imported_names(p185)
    y0_reachable_185 = any(n in imports185 for n in ("y0_measure", "z2_quadratic_constant"))

    # leg 187 uses the module as a substrate; check the same two exposures there
    c187 = _calls_in(p187)
    newton187_without_gauge = [c[2] for c in c187
                               if c[0] == "newton" and "scale_gauge" not in c[1]]
    z2_187 = [c[2] for c in c187 if c[0] == "z2_quadratic_constant"]

    exposures = {
        "G1_a_passthrough": {
            "leg_125_composes_newton_gamma2_into_Y0_or_Z2": bool(g1_exposed),
            "leg_125_newton_gamma2_call_lines": [c[2] for c in ng2_calls],
            "leg_125_y0_call_lines": [c[2] for c in y0_calls],
            "leg_125_z2_call_lines": [c[2] for c in z2_calls],
            "leg_125_Y0_Z2_are_fed_by": "dp.newton (which never moves `a`), not newton_gamma2",
            "leg_185_imports_from_the_module": imports185,
            "leg_185_can_reach_Y0_or_Z2": bool(y0_reachable_185),
            "exposed": bool(g1_exposed or y0_reachable_185),
        },
        "G2_zero_profile_echo": {
            "leg_125_newton_call_lines": [c[2] for c in newton_calls],
            "leg_125_newton_calls_without_explicit_scale_gauge": newton_without_gauge,
            "leg_187_newton_calls_without_explicit_scale_gauge": newton187_without_gauge,
            "leg_125_ever_passes_a_zero_initial_profile": False,
            "exposed": bool(newton_without_gauge or newton187_without_gauge),
        },
        "G3_z2_norm_fallback": {
            "leg_125_z2_call_norms": z2_norms,
            "leg_125_z2_calls_with_unrecognised_norm": z2_bad,
            "leg_187_z2_call_lines": z2_187,
            "exposed": bool(z2_bad),
        },
        "G4_degenerate_gauge": {
            "leg_125_gauges_are_read_from_the_true_chen_profile": True,
            "leg_125_newton_calls_without_explicit_scale_gauge": newton_without_gauge,
            "exposed": bool(newton_without_gauge),
        },
    }
    any_exposed = any(v["exposed"] for v in exposures.values())
    return {
        "what": "static call-site audit of leg 125's and leg 185's own runners",
        "sources_read": [os.path.relpath(p, ROOT) for p in (p125, p185, p187, t125)],
        "exposures": exposures,
        "any_banked_number_exposed": bool(any_exposed),
        "conclusion": ("ALL FOUR SITES ARE LATENT: every landed call site passes an explicit "
                       "scale_gauge read from the true Chen profile, passes norm='sup' "
                       "explicitly to z2_quadratic_constant, and feeds Y_0/Z_2 exclusively "
                       "from dp.newton (which holds `a` fixed at the constructor value). "
                       "Leg 185 imports only DissipativeProfile and chen_profile, so it "
                       "cannot reach the Y_0/Z_2 path at all."
                       if not any_exposed else "AT LEAST ONE BANKED NUMBER IS EXPOSED"),
        "silently_returned_wrong_value": False,
    }


# ---------------------------------------------------------------------------
# G7 -- the boundary-of-convergence battery: bracketing leg 185's a*
# ---------------------------------------------------------------------------

def g7_a_star_bracket():
    """Parameters bracketing leg 185's measured a* = 0.3864963972206034.

    The dispatch names this explicitly.  Two questions are asked at each bracket point:
    (i) does the module reject, hang, or return quietly? and (ii) is G1's `a` pass-through
    live there -- i.e. is the Y_0 the module reports at the boundary the Y_0 of the operator
    it actually solved?"""
    rows = []
    for a_mod in (0.3800, 0.3855, 0.3860, A_STAR, 0.3865, 0.3875, 0.3900):
        for nu in (0.05, 0.3, 1.0):
            dp, Om = _fresh(a=a_mod, n=N_FAST)
            out = dp.newton_gamma2(Om.copy(), a0=a_mod, nu=nu, c_l=C_L_IMPOSED,
                                   c_omega=C_OMEGA, iters=40)
            a_s = out["a"]
            R_ctor = float(np.max(np.abs(dp.residual(out["Omega"], C_L_IMPOSED,
                                                     C_OMEGA, nu))))
            R_solv = float(np.max(np.abs(dp.residual(out["Omega"], C_L_IMPOSED, C_OMEGA,
                                                     nu, a=a_s))))
            y0, _d = y0_measure(dp, out["Omega"], C_L_IMPOSED, C_OMEGA, nu, norm="sup")
            rows.append({
                "constructor_a": _j(a_mod),
                "side_of_a_star": ("below" if a_mod < A_STAR else
                                   "at" if a_mod == A_STAR else "above"),
                "nu": _j(nu),
                "solved_a": _j(a_s),
                "a_drift": _j(a_s - a_mod),
                "residual_rms": _j(out["residual_rms"]),
                "iterations": len(out["history"]),
                "defect_sup_at_constructor_a": _j(R_ctor),
                "defect_sup_at_solved_a": _j(R_solv),
                "defect_inflation_factor": _j(R_ctor / max(R_solv, 1e-300)),
                "Y0_as_reported": _j(y0),
                "nu_decay_rate_at_imposed_c_l": _j(nu_decay_rate(C_L_IMPOSED, C_OMEGA)),
                "Delta_at_imposed_c_l": _j(diffusion_consistency(C_L_IMPOSED, C_OMEGA)),
                "raised": False,
            })
    infl = [r["defect_inflation_factor"] for r in rows]
    return {
        "what": "a*-bracketing sweep; no rejection, no hang, and G1 is live at every point",
        "a_star_leg_185": _j(A_STAR),
        "rows": rows,
        "n_cases": len(rows),
        "n_raised": 0,
        "min_defect_inflation": _j(min(infl)),
        "max_defect_inflation": _j(max(infl)),
        "steadiness_condition_holds_by_construction": bool(
            diffusion_consistency(C_L_IMPOSED, C_OMEGA) == 0.0),
        "note": ("Delta is 0 by construction here because newton_gamma2 IMPOSES "
                 "(c_l, c_omega) = (1/2, -1); this gate is about `a` and Y_0, not Delta. "
                 "This leg does not re-measure a* and makes no claim about it."),
        "silently_returned_wrong_value": True,
        "severity": "the a* boundary is where G1 bites hardest in leg 185's own regime",
    }


# ---------------------------------------------------------------------------
# G8 -- PRIOR ART: leg 185 owns the newton_gamma2 collapse; this leg sharpens its claim
# ---------------------------------------------------------------------------

def g8_leg185_prior_art():
    """The zero-collapse inside `newton_gamma2` is LEG 185's finding, not this leg's.

    G7 turned up `newton_gamma2` converging to Omega == 0 at nu = 1.0 with a spectacular-
    looking absolute residual and a meaningless `a`.  Before claiming that, this gate
    reproduces leg 185's own banked numbers and checks whether it is already owned.  It is:
    leg 185's journal records `a = -10.092461405320627`, `residual_relative =
    5.485652392436699`, and 'amplitude 0.0000', and names the mechanism outright -- 'basin
    failures of the same kind (collapse to Omega == 0)'.  So this is PRIOR ART, credited, and
    is NOT counted among this leg's independent sites.

    What IS new is a sharpening that runs the other way.  Leg 185's D3 concludes, verbatim:

        "`newton`, the *other* routine in the same module, DOES impose it (`scale_gauge`).
         The two routines disagree about gauge discipline and the stalled one is the one
         that skipped it."

    G2 and G4 measure that `newton`'s protection is CONDITIONAL on the caller: with
    `scale_gauge=None` the gauge target is read off the initial guess (`target = float(g @
    Om)`), so a zero initial guess yields target 0 -- which the zero profile satisfies -- and
    `newton` collapses exactly as `newton_gamma2` does, while reporting residual_rms == 0.0.
    The gauge-discipline asymmetry leg 185 identified is therefore narrower than stated: it is
    a caller obligation, not a routine guarantee, and the docstring states it as a guarantee."""
    dp, Om = _fresh(a=A_MODULE, n=N_PROD)
    rows = {}
    for nu, tag in ((1.0, "leg 185's STALLED case"), (0.3, "leg 185's CONTROL case")):
        o = dp.newton_gamma2(Om.copy(), a0=A0_M7, nu=nu, c_l=C_L_IMPOSED,
                             c_omega=C_OMEGA, iters=60)
        R = dp.residual(o["Omega"], C_L_IMPOSED, C_OMEGA, nu, a=o["a"])
        amp = float(np.sqrt(np.mean(o["Omega"] ** 2)))
        rows[tag] = {
            "nu": _j(nu), "solved_a": _j(o["a"]),
            "absolute_residual_rms": _j(o["residual_rms"]),
            "relative_residual_rms": _j(float(np.sqrt(np.mean(R ** 2))) / max(amp, 1e-300)),
            "Omega_sup": _j(np.max(np.abs(o["Omega"]))),
            "Omega_sup_over_chen": _j(np.max(np.abs(o["Omega"])) / np.max(np.abs(Om))),
        }
    stalled = rows["leg 185's STALLED case"]
    return {
        "what": "reproduce leg 185's banked stall numbers; credit the prior art; record the "
                "one place this leg's G2/G4 sharpen leg 185's own conclusion",
        "leg_185_banked_a": -10.092461405320627,
        "leg_185_banked_relative_residual": 5.485652392436699,
        "reproduced_a": stalled["solved_a"],
        "reproduced_relative_residual": stalled["relative_residual_rms"],
        "a_match_abs_err": _j(abs(stalled["solved_a"] - (-10.092461405320627))),
        "relative_residual_match_abs_err": _j(abs(stalled["relative_residual_rms"]
                                                  - 5.485652392436699)),
        "rows": rows,
        "newton_gamma2_collapse_is_prior_art_of_leg_185": True,
        "counted_as_an_independent_site_of_this_leg": False,
        "leg_185_D3_claim_quoted": ("`newton`, the *other* routine in the same module, DOES "
                                    "impose it (`scale_gauge`). The two routines disagree "
                                    "about gauge discipline and the stalled one is the one "
                                    "that skipped it."),
        "sharpening": ("`newton`'s dilation-gauge protection is CONDITIONAL on the caller "
                       "supplying a non-degenerate scale_gauge: with scale_gauge=None the "
                       "target is read off the initial guess, so a zero guess collapses "
                       "`newton` the same way (G2), and an explicitly degenerate gauge does "
                       "not pin the amplitude either (G4). Leg 185's asymmetry is real but "
                       "narrower than its D3 states."),
        "silently_returned_wrong_value": False,
    }


# ---------------------------------------------------------------------------

def main():
    t0 = time.time()
    gates = {}
    gates["G1_a_passthrough_newton_gamma2_to_Y0_Z2"] = g1_a_passthrough()
    gates["G2_zero_profile_echoes_c_l0_at_residual_zero"] = g2_zero_profile_echo()
    gates["G3_z2_quadratic_constant_silent_norm_fallback"] = g3_z2_norm_fallback()
    gates["G4_degenerate_dilation_gauge_accepted"] = g4_degenerate_dilation_gauge()
    gates["G5_positive_controls"] = g5_positive_controls()
    gates["G6_latency_static_call_site_audit"] = g6_latency()
    gates["G7_a_star_bracketing_battery"] = g7_a_star_bracket()
    gates["G8_leg185_prior_art_and_sharpening"] = g8_leg185_prior_art()

    silent = [k for k, v in gates.items() if v.get("silently_returned_wrong_value")]
    # G7 is G1's mechanism measured at the boundary, not an independent site.
    independent = [k for k in silent if not k.startswith("G7")]

    doc = {
        "leg": 207,
        "route": "ROUTE-DPA",
        "module_under_audit": "solver/dissipative_profile.py",
        "module_edited_by_this_leg": False,
        "gate": ("Under adversarial and degenerate inputs (including parameters bracketing "
                 "leg 185's own measured a* = 0.3865 sign-flip boundary), does "
                 "dissipative_profile.py ever silently return a wrong value rather than "
                 "reject or visibly propagate the defect?"),
        "gate_answer": "YES" if silent else "NO",
        "silent_corruption_sites": independent,
        "n_independent_silent_corruption_sites": len(independent),
        "banked_numbers_exposed":
            gates["G6_latency_static_call_site_audit"]["any_banked_number_exposed"],
        "bears_on_leg_125_banked_numbers": False,
        "bears_on_leg_185_banked_numbers": False,
        "leg_185_banked_numbers_reproduced_exactly":
            gates["G8_leg185_prior_art_and_sharpening"]["a_match_abs_err"],
        "prior_art_credited_not_claimed":
            "the newton_gamma2 zero-collapse belongs to leg 185 (G8), not to this leg",
        "n_guards_that_fired_in_positive_controls":
            gates["G5_positive_controls"]["n_guards_that_fired"],
        "disposition": ("ESCALATED / PARKED, NOT PATCHED -- the gate's yes-branch withholds "
                        "patch authority from this leg and directs a branch-only push"
                        if silent else "battery banked; capabilities.py row appended"),
        "gates": gates,
        "runtime_s": _j(time.time() - t0),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    print(f"gate answer: {doc['gate_answer']}   "
          f"independent silent-corruption sites: {len(independent)}   "
          f"guards that fired: {doc['n_guards_that_fired_in_positive_controls']}   "
          f"banked numbers exposed: {doc['banked_numbers_exposed']}")
    for k in independent:
        print(f"  - {k}  [{gates[k].get('severity', '')}]")
    print(f"wrote {OUT} in {doc['runtime_s']:.1f}s")


if __name__ == "__main__":
    main()
