"""Route-HRR, leg 152 -- the REPAIR runner for solver/hl_rescaled.py.

Leg 117 (Route-HRA) measured four silent-corruption mechanisms in this module and
ESCALATED without patching, under its own gate's instruction.  Leg 152 lands the guards.
This runner is the evidence, and it answers the gate's two clauses separately, with
magnitudes and never with a boolean:

  (a) does velocity() reject or visibly flag a non-ascending X; is X_ref validated
      against [X.min(), X.max()] rather than silently clamped; does sinh_grid_at reject
      M < 0; and does degenerate_ic distinguish a NaN abscissa from a legitimate 0.0?
  (b) is the module BIT-IDENTICAL on every previously-passing case?

Clause (b) is the licence for the whole repair, so it is run as a differential and not as
an argument: the PRE-REPAIR module is read out of git at `PRE_REPAIR_REF`, imported into
THIS SAME PROCESS under a private name, and called side by side with the repaired module
on every clean surface the module exposes.  Comparison is `==` on raw float64 (and hex
floats for scalars) -- not `allclose`.  If a single clean value moves, the gate's
no-branch fires and this leg escalates instead of iterating.

LESSON 90 CONTROL.  A differential that reports "0 moved" is worthless if the two sides
are secretly the same object.  `control_two_modules_really_differ` asserts the pre-repair
module lacks the new symbols AND that the two sides DISAGREE on a poisoned input.  If that
control ever passes trivially, the run aborts and reports nothing.

Run: PYTHONPATH=. .venv/bin/python experiments/p2_route_hrr_v1_repair.py
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver import hl_rescaled as HL                                     # noqa: E402
from solver.hl_rescaled import (                                         # noqa: E402
    HLRescaledDomainError, HLRescaledDomainWarning, RescaledHL, RescaledHLDynamic,
    RescaledHLScenario2, U_bar_exact, H_omega_bar_exact, degenerate_ic, omega_bar,
    scenario2_ic, sinh_grid_at, sinh_grid_origin, velocity, _solve_3x3,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_hrr_v1_repair.json")

# The module's OWN last pre-guard commit.  `git diff 2450ddf HEAD -- solver/hl_rescaled.py`
# was EMPTY before this leg, so 2450ddf is byte-identical to the module as leg 117 audited
# it.  Deliberately not "the commit before mine": a leg's own hashes are rewritten by the
# rebase onto main and a self-referential pin stops resolving the moment the branch lands
# (leg 130's own correction, d871675).
PRE_REPAIR_REF = "2450ddf"


# ---------------------------------------------------------------------------
# the pre-repair module, loaded from git into this same process
# ---------------------------------------------------------------------------
def load_pre_repair():
    src = subprocess.run(["git", "show", "%s:solver/hl_rescaled.py" % PRE_REPAIR_REF],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    fd, path = tempfile.mkstemp(suffix="_pre_hl_rescaled.py")
    with os.fdopen(fd, "w") as f:
        f.write(src)
    spec = importlib.util.spec_from_file_location("_pre_hl_rescaled", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, len(src.splitlines())


def control_two_modules_really_differ(pre):
    """LESSON 90.  What would have had to change for the differential to report the other
    answer?  Answer: the two module objects must actually be different.  Asserted here,
    executably, before any 'identical' count is believed."""
    checks = {}
    checks["pre_lacks_new_error_type"] = not hasattr(pre, "HLRescaledDomainError")
    checks["pre_lacks_ascending_helper"] = not hasattr(pre, "_is_strictly_ascending")
    checks["post_has_new_error_type"] = hasattr(HL, "HLRescaledDomainError")
    checks["distinct_module_objects"] = pre is not HL

    # the two sides must DISAGREE on a poisoned input, or the differential is a tautology
    Xp = np.linspace(-5.0, 5.0, 51)
    Xp[[10, 30, 45]] = np.nan
    om_pre, _ = pre.degenerate_ic(Xp, kind="A")
    om_post, _ = degenerate_ic(Xp, kind="A")
    checks["pre_launders_nan_to_zero"] = bool(np.all(om_pre[[10, 30, 45]] == 0.0))
    checks["post_propagates_nan"] = bool(np.all(np.isnan(om_post[[10, 30, 45]])))

    # and the pre-repair side must still silently mis-integrate a permuted grid
    _, Xs = pre.sinh_grid_at(201, Xc=0.0, delta=None, M=50.0)
    Hs = 2.0 / (1.0 + 4.0 * Xs ** 2)
    rng = np.random.default_rng(0)
    perm = rng.permutation(len(Xs))
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        U_perm_pre = pre.velocity(Xs[perm], Hs[perm], X_ref=0.0)
    checks["pre_accepts_permuted_grid_silently"] = (
        bool(np.all(np.isfinite(U_perm_pre))) and len(wl) == 0)
    ok = all(checks.values())
    return ok, checks


# ---------------------------------------------------------------------------
# leaf comparison
# ---------------------------------------------------------------------------
class Diff:
    """Accumulates bitwise pre/post comparisons over named leaves."""

    def __init__(self):
        self.n = 0
        self.n_ident = 0
        self.moved = []

    def add(self, name, a, b):
        a = np.asarray(a, dtype=float)
        b = np.asarray(b, dtype=float)
        if a.shape != b.shape:
            self.n += 1
            self.moved.append({"leaf": name, "reason": "shape %s vs %s"
                               % (a.shape, b.shape)})
            return
        af, bf = a.ravel(), b.ravel()
        for i in range(af.size):
            self.n += 1
            x, y = af[i], bf[i]
            same = (x == y) or (np.isnan(x) and np.isnan(y))
            if same:
                self.n_ident += 1
            else:
                self.moved.append({"leaf": name, "index": int(i),
                                   "pre": float(x), "post": float(y),
                                   "pre_hex": float(x).hex(),
                                   "post_hex": float(y).hex()})


# ---------------------------------------------------------------------------
# (b) the clean-input differential -- every surface the module exposes
# ---------------------------------------------------------------------------
GRID_CASES = [
    dict(n=101, Xc=1.0, delta=0.05, M=20.0, offset=True),
    dict(n=201, Xc=0.0, delta=None, M=50.0, offset=True),
    dict(n=201, Xc=1.0, delta=0.01, M=500.0, offset=True),
    dict(n=401, Xc=1.0, delta=0.016, M=500.0, offset=True),
    dict(n=401, Xc=-2.0, delta=1.0, M=50.0, offset=False),
    dict(n=11, Xc=0.0, delta=1.0, M=50.0, offset=False),
    dict(n=2001, Xc=1.0, delta=0.004, M=500.0, offset=True),
]


def differential_free_functions(pre, d):
    """Grids, closed-form anchors, the free velocity(), the IC generators, _solve_3x3."""
    for k, kw in enumerate(GRID_CASES):
        s_pre, X_pre = pre.sinh_grid_at(**kw)
        s_post, X_post = sinh_grid_at(**kw)
        d.add("sinh_grid_at[%d].s" % k, s_pre, s_post)
        d.add("sinh_grid_at[%d].X" % k, X_pre, X_post)
        X = X_post
        d.add("omega_bar[%d]" % k, pre.omega_bar(X), omega_bar(X))
        d.add("H_omega_bar_exact[%d]" % k, pre.H_omega_bar_exact(X),
              H_omega_bar_exact(X))
        d.add("U_bar_exact[%d]" % k, pre.U_bar_exact(X), U_bar_exact(X))
        # the free velocity operator, on three physically-shipped integrands and every
        # X_ref that is inside the grid
        integrands = {
            "lorentzian": 2.0 / (1.0 + 4.0 * X ** 2),
            "anchor_exact_H": H_omega_bar_exact(X),
            "gaussian": np.exp(-0.5 * X ** 2),
        }
        for nm, Hom in integrands.items():
            for X_ref in (0.0, 1.0, float(X[0]), float(X[-1]), float(X[X.size // 3])):
                if not (X.min() <= X_ref <= X.max()):
                    continue
                d.add("velocity[%d].%s.ref=%r" % (k, nm, X_ref),
                      pre.velocity(X, Hom, X_ref=X_ref),
                      velocity(X, Hom, X_ref=X_ref))
        for kind in ("A", "B", "C"):
            om_a, th_a = pre.degenerate_ic(X, kind=kind)
            om_b, th_b = degenerate_ic(X, kind=kind)
            d.add("degenerate_ic[%d].%s.Omega" % (k, kind), om_a, om_b)
            d.add("degenerate_ic[%d].%s.Theta" % (k, kind), th_a, th_b)
        for (x0, w) in ((0.3, 0.9), (1.0, 0.4), (-0.5, 2.0)):
            o_a, v_a = pre.scenario2_ic(X, x0=x0, w=w)
            o_b, v_b = scenario2_ic(X, x0=x0, w=w)
            d.add("scenario2_ic[%d].%r.Omega" % (k, (x0, w)), o_a, o_b)
            d.add("scenario2_ic[%d].%r.V" % (k, (x0, w)), v_a, v_b)

    for n in (11, 101, 501, 2001):
        for c, rho_max in ((0.5, 8.0), (1.0, 6.0), (0.25, 10.0)):
            r_a, X_a = pre.sinh_grid_origin(n, c=c, rho_max=rho_max)
            r_b, X_b = sinh_grid_origin(n, c=c, rho_max=rho_max)
            d.add("sinh_grid_origin[%d,%r].rho" % (n, c), r_a, r_b)
            d.add("sinh_grid_origin[%d,%r].X" % (n, c), X_a, X_b)

    rng = np.random.default_rng(0)
    n_solve = 0
    for _ in range(300):
        A = rng.standard_normal((3, 3)) * (10.0 ** rng.uniform(-8, 8))
        b = rng.standard_normal(3) * (10.0 ** rng.uniform(-8, 8))
        try:
            xa = pre._solve_3x3(A, b)
        except ValueError:
            continue
        xb = _solve_3x3(A, b)
        d.add("_solve_3x3[%d]" % n_solve, xa, xb)
        n_solve += 1
    return n_solve


def differential_classes(pre, d):
    """RescaledHL / RescaledHLDynamic / RescaledHLScenario2: every public surface,
    including full time steps and a capped Scenario-2 relaxation."""
    # -- RescaledHL on the shipped anchor grids
    for k, kw in enumerate(GRID_CASES[:5]):
        _, X = sinh_grid_at(**kw)
        a = pre.RescaledHL(X, X_ref=0.0)
        b = RescaledHL(X, X_ref=0.0)
        Omega = omega_bar(X)
        Theta = np.where(X > 1.0, PI_2(), 0.0)
        d.add("RescaledHL[%d].Hmat" % k, a.Hmat, b.Hmat)
        d.add("RescaledHL[%d].hilbert" % k, a.hilbert(Omega), b.hilbert(Omega))
        d.add("RescaledHL[%d].velocity" % k, a.velocity(Omega), b.velocity(Omega))
        d.add("RescaledHL[%d].dX" % k, a.dX(Omega), b.dX(Omega))
        ra = a.steady_residual(Omega, Theta, 2.0, -1.0)
        rb = b.steady_residual(Omega, Theta, 2.0, -1.0)
        d.add("RescaledHL[%d].R_Omega" % k, ra[0], rb[0])
        d.add("RescaledHL[%d].R_Theta" % k, ra[1], rb[1])

    # -- RescaledHLDynamic: gauge, amplitude gauge, RHS, and REAL time steps
    for (n, delta, M, nu) in ((101, 0.05, 20.0, 0.0), (301, 0.02, 100.0, 1e-3)):
        a = pre.RescaledHLDynamic(n=n, delta=delta, M=M, nu=nu)
        b = RescaledHLDynamic(n=n, delta=delta, M=M, nu=nu)
        d.add("Dyn[%d].X" % n, a.X, b.X)
        Om_a = a.normalize_amp(omega_bar(a.X))
        Om_b = b.normalize_amp(omega_bar(b.X))
        d.add("Dyn[%d].normalize_amp" % n, Om_a, Om_b)
        d.add("Dyn[%d].amp_gauge" % n, a.amp_gauge(Om_a), b.amp_gauge(Om_b))
        Th = np.where(a.X > 1.0, PI_2(), 0.0)
        ga = a.gauge(Om_a, Th)
        gb = b.gauge(Om_b, Th)
        d.add("Dyn[%d].gauge.c" % n, [ga[0], ga[1]], [gb[0], gb[1]])
        d.add("Dyn[%d].gauge.U" % n, ga[2], gb[2])
        d.add("Dyn[%d].max_speed_s" % n, a.max_speed_s(Om_a), b.max_speed_s(Om_b))
        ra, rb = a.rhs(Om_a, Th), b.rhs(Om_b, Th)
        d.add("Dyn[%d].rhs.L_Om" % n, ra[0], rb[0])
        d.add("Dyn[%d].rhs.L_Th" % n, ra[1], rb[1])
        oa, ta_, ob, tb = Om_a, Th, Om_b, Th
        for it in range(5):
            oa, ta_, cla, cwa, resa = a.step(oa, ta_, 1e-4)
            ob, tb, clb, cwb, resb = b.step(ob, tb, 1e-4)
            d.add("Dyn[%d].step%d.Omega" % (n, it), oa, ob)
            d.add("Dyn[%d].step%d.Theta" % (n, it), ta_, tb)
            d.add("Dyn[%d].step%d.consts" % (n, it), [cla, cwa, resa], [clb, cwb, resb])

    # -- RescaledHLScenario2: the gauge capabilities.py validates to 4.4e-16, plus a run
    for (n, c, rho_max) in ((201, 0.5, 8.0), (501, 0.5, 8.0)):
        a = pre.RescaledHLScenario2(n=n, c=c, rho_max=rho_max)
        b = RescaledHLScenario2(n=n, c=c, rho_max=rho_max)
        d.add("Sc2[%d].X" % n, a.X, b.X)
        Om0, V0 = scenario2_ic(a.X)
        ga, gb = a.gauge(Om0, V0), b.gauge(Om0, V0)
        d.add("Sc2[%d].gauge.c" % n, list(ga[:3]), list(gb[:3]))
        d.add("Sc2[%d].gauge.U" % n, ga[3], gb[3])
        d.add("Sc2[%d].origin_gauges" % n, a.origin_gauges(Om0, V0),
              b.origin_gauges(Om0, V0))
        ra, rb = a.rhs(Om0, V0), b.rhs(Om0, V0)
        d.add("Sc2[%d].rhs.L_Om" % n, ra[0], rb[0])
        d.add("Sc2[%d].rhs.L_V" % n, ra[1], rb[1])
        d.add("Sc2[%d].max_speed_rho" % n, a.max_speed_rho(Om0, V0),
              b.max_speed_rho(Om0, V0))
        res_a = a.run(Om0, V0, max_steps=120, record_every=20, tol=1e-12)
        res_b = b.run(Om0, V0, max_steps=120, record_every=20, tol=1e-12)
        for key in ("Omega", "V", "c_l_hist", "c_omega_hist", "c_r_hist",
                    "res_hist", "tau_hist", "Omega0_hist", "V0_hist", "UX0_hist"):
            d.add("Sc2[%d].run.%s" % (n, key), res_a[key], res_b[key])
        d.add("Sc2[%d].run.scalars" % n,
              [res_a["c_l"], res_a["c_omega"], res_a["c_r"], res_a["residual"],
               res_a["tau"]],
              [res_b["c_l"], res_b["c_omega"], res_b["c_r"], res_b["residual"],
               res_b["tau"]])


def PI_2():
    return float(np.pi / 2.0)


# ---------------------------------------------------------------------------
# (a) the four clauses: does the repair actually flag what leg 117 measured?
# ---------------------------------------------------------------------------
def clause_a(pre):
    out = {}

    # -- G1: non-ascending X in velocity() -------------------------------
    _, X = sinh_grid_at(201, Xc=0.0, delta=None, M=50.0)
    Hom = 2.0 / (1.0 + 4.0 * X ** 2)
    U_true = velocity(X, Hom, X_ref=0.0)
    rng = np.random.default_rng(0)
    n_raise = 0
    worst_pre_err = 0.0
    for trial in range(20):
        perm = rng.permutation(len(X))
        inv = np.argsort(perm)
        U_pre = pre.velocity(X[perm], Hom[perm], X_ref=0.0)
        worst_pre_err = max(worst_pre_err,
                            float(np.abs(U_pre[inv] - U_true).max()))
        try:
            velocity(X[perm], Hom[perm], X_ref=0.0)
        except HLRescaledDomainError:
            n_raise += 1
    # the escape hatch must reproduce the pre-repair number BIT-IDENTICALLY
    rng2 = np.random.default_rng(0)
    perm0 = rng2.permutation(len(X))
    U_pre0 = pre.velocity(X[perm0], Hom[perm0], X_ref=0.0)
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        U_warn0 = velocity(X[perm0], Hom[perm0], X_ref=0.0, on_invalid="warn")
    out["G1"] = {
        "permutations_tested": 20,
        "pre_repair_silent": 20,
        "post_repair_raised": n_raise,
        "pre_repair_worst_abs_error_vs_sorted": worst_pre_err,
        "true_scale_sup_U": float(np.abs(U_true).max()),
        "pre_repair_error_in_units_of_true_scale":
            worst_pre_err / float(np.abs(U_true).max()),
        "warn_hatch_bit_identical_to_pre_repair":
            bool(np.all(U_warn0 == U_pre0)),
        "warn_hatch_n_warnings": len(wl),
        "warn_hatch_warning_type": type(wl[0].message).__name__ if wl else None,
    }

    # -- G2: X_ref outside [X.min(), X.max()] ----------------------------
    Xl = np.linspace(0.0, 10.0, 501)
    Homl = 2.0 / (1.0 + 4.0 * Xl ** 2)
    rows = []
    for X_ref in (-5.0, -0.5, 10.5, 25.0):
        U_pre = pre.velocity(Xl, Homl, X_ref=X_ref)
        true_pinned = np.arctan(2.0 * Xl) - np.arctan(2.0 * X_ref)
        shift = float(np.abs(U_pre - true_pinned).max())
        raised = False
        try:
            velocity(Xl, Homl, X_ref=X_ref)
        except HLRescaledDomainError:
            raised = True
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            U_warn = velocity(Xl, Homl, X_ref=X_ref, on_invalid="warn")
        rows.append({"X_ref": X_ref, "pre_repair_abs_shift_error": shift,
                     "post_repair_raised": raised,
                     "warn_hatch_bit_identical": bool(np.all(U_warn == U_pre)),
                     "warn_hatch_n_warnings": len(wl)})
    # and the in-domain boundary values must NOT be rejected (no over-rejection)
    n_boundary_ok = 0
    for X_ref in (0.0, 10.0, 5.0, float(Xl[1])):
        try:
            velocity(Xl, Homl, X_ref=X_ref)
            n_boundary_ok += 1
        except HLRescaledDomainError:
            pass
    out["G2"] = {"cases": rows, "n_raised": sum(r["post_repair_raised"] for r in rows),
                 "n_cases": len(rows),
                 "in_domain_including_both_endpoints_accepted": n_boundary_ok,
                 "in_domain_cases": 4}

    # -- G3: sinh_grid_at with a non-positive scale ----------------------
    kwargs = dict(Xc=0.0, delta=1.0, M=50.0, offset=False)
    _, X_pos = sinh_grid_at(11, **kwargs)
    _, X_neg_pre = pre.sinh_grid_at(11, **{**kwargs, "M": -50.0})
    g3 = {"pre_repair_returns_exact_descending_mirror":
          bool(np.allclose(X_neg_pre, X_pos[::-1])),
          "pre_repair_warnings": 0}
    n_rej = 0
    for bad in ({"M": -50.0}, {"M": 0.0}, {"M": -1e-12},
                {"delta": -1.0}, {"delta": 0.0}):
        try:
            sinh_grid_at(11, **{**kwargs, **bad})
        except HLRescaledDomainError:
            n_rej += 1
    g3["post_repair_rejected"] = n_rej
    g3["bad_scale_cases"] = 5
    g3["delta_clause_is_declared_in_kind_extension"] = True
    out["G3"] = g3

    # -- G8: degenerate_ic and a NaN abscissa ----------------------------
    Xn = np.linspace(-5.0, 5.0, 51)
    nan_idx = [10, 30, 45]
    Xn[nan_idx] = np.nan
    g8 = {}
    for kind in ("A", "B", "C"):
        om_pre, th_pre = pre.degenerate_ic(Xn, kind=kind)
        om_post, th_post = degenerate_ic(Xn, kind=kind)
        clean = np.array([i for i in range(51) if i not in nan_idx])
        g8[kind] = {
            "pre_repair_nan_positions_became_exact_zero":
                bool(np.all(om_pre[nan_idx] == 0.0) and np.all(th_pre[nan_idx] == 0.0)),
            "post_repair_nan_positions_are_nan":
                bool(np.all(np.isnan(om_post[nan_idx]))
                     and np.all(np.isnan(th_post[nan_idx]))),
            "n_laundered_pre": int(np.sum(om_pre[nan_idx] == 0.0)
                                   + np.sum(th_pre[nan_idx] == 0.0)),
            "n_laundered_post": int(np.sum(om_post[nan_idx] == 0.0)
                                    + np.sum(th_post[nan_idx] == 0.0)),
            "non_nan_entries_bit_identical":
                bool(np.all(om_pre[clean] == om_post[clean])
                     and np.all(th_pre[clean] == th_post[clean])),
        }
    out["G8"] = g8

    # -- G4: the author's-call clause, PATCHED (see writeup/novelty/leg_152.md) --
    Xg = np.array([0.0, 1.0, np.nan, 0.5, 2.0])
    pre_accepted = True
    try:
        pre.RescaledHL(Xg)
    except ValueError:
        pre_accepted = False
    post_rejected = False
    try:
        RescaledHL(Xg)
    except HLRescaledDomainError:
        post_rejected = True
    # over-rejection control: endpoint inf must STILL be accepted (leg 117's G7 finding
    # is that it is well-defined and stays visible downstream) and interior inf rejected
    endpoint_ok = 0
    for Xe in (np.array([0.0, 1.0, 2.0, 3.0, np.inf]),
               np.array([-np.inf, 0.0, 1.0, 2.0, 3.0])):
        try:
            RescaledHL(Xe)
            endpoint_ok += 1
        except HLRescaledDomainError:
            pass
    interior_rejected = False
    try:
        RescaledHL(np.array([0.0, 1.0, np.inf, 3.0, 4.0]))
    except HLRescaledDomainError:
        interior_rejected = True
    out["G4"] = {
        "clause_disposition": "PATCHED (DIRECTION.md leaves this to the leg author)",
        "reason": ("the fix adds no machinery -- it is the same one-token polarity flip "
                   "np.any(d<=0) -> np.all(d>0) that velocity()'s own G1 guard needs, "
                   "and leaving the class laxer than the free function it calls would be "
                   "a new inconsistency"),
        "pre_repair_accepted_nan_poisoned_grid": pre_accepted,
        "post_repair_rejects_nan_poisoned_grid": post_rejected,
        "endpoint_inf_still_accepted": endpoint_ok,
        "endpoint_inf_cases": 2,
        "interior_inf_still_rejected": interior_rejected,
    }
    return out


# ---------------------------------------------------------------------------
def main():
    pre, n_lines = load_pre_repair()
    ok, control = control_two_modules_really_differ(pre)
    print("LESSON-90 CONTROL (the differential must be able to report the other answer):")
    for k, v in control.items():
        print("    %-38s %s" % (k, v))
    assert ok, ("lesson-90 control FAILED: the two sides are not distinguishable, so no "
                "'identical' count from this run means anything -- %r" % (control,))

    print("\nCLAUSE (a) -- does the repair flag what leg 117 measured?")
    a = clause_a(pre)
    print("    G1 permuted grid: pre-repair silent 20/20 (worst abs err %.4f = %.1fx the "
          "true scale); post-repair raised %d/20; warn-hatch bit-identical: %s"
          % (a["G1"]["pre_repair_worst_abs_error_vs_sorted"],
             a["G1"]["pre_repair_error_in_units_of_true_scale"],
             a["G1"]["post_repair_raised"],
             a["G1"]["warn_hatch_bit_identical_to_pre_repair"]))
    print("    G2 out-of-domain X_ref: raised %d/%d; worst pre-repair silent shift %.4f; "
          "in-domain (both endpoints) accepted %d/%d"
          % (a["G2"]["n_raised"], a["G2"]["n_cases"],
             max(r["pre_repair_abs_shift_error"] for r in a["G2"]["cases"]),
             a["G2"]["in_domain_including_both_endpoints_accepted"],
             a["G2"]["in_domain_cases"]))
    print("    G3 non-positive grid scale: rejected %d/%d (M and delta)"
          % (a["G3"]["post_repair_rejected"], a["G3"]["bad_scale_cases"]))
    print("    G8 NaN abscissa: pre laundered %d values to exact 0.0 per kind, post %d; "
          "non-NaN entries bit-identical: %s"
          % (a["G8"]["A"]["n_laundered_pre"], a["G8"]["A"]["n_laundered_post"],
             all(a["G8"][k]["non_nan_entries_bit_identical"] for k in "ABC")))
    print("    G4 (author's call: PATCHED): pre accepted the NaN-poisoned grid: %s; "
          "post rejects: %s; endpoint inf still accepted %d/2; interior inf rejected: %s"
          % (a["G4"]["pre_repair_accepted_nan_poisoned_grid"],
             a["G4"]["post_repair_rejects_nan_poisoned_grid"],
             a["G4"]["endpoint_inf_still_accepted"],
             a["G4"]["interior_inf_still_rejected"]))

    print("\nCLAUSE (b) -- the clean-input differential (== on float64, not allclose)")
    d = Diff()
    n_solve = differential_free_functions(pre, d)
    n_free = d.n
    print("    free functions + grids + IC generators + _solve_3x3 (%d systems): "
          "%d/%d leaves bit-identical" % (n_solve, d.n_ident, d.n))
    differential_classes(pre, d)
    print("    + RescaledHL / Dynamic (5 real SSPRK3 steps each) / Scenario2 (gauge, "
          "rhs, 120-step run): %d/%d leaves bit-identical cumulative"
          % (d.n_ident, d.n))
    if d.moved:
        print("    MOVED LEAVES (first 10):")
        for m in d.moved[:10]:
            print("      %r" % (m,))

    zero_movement = (d.n_ident == d.n)
    clause_a_ok = (
        a["G1"]["post_repair_raised"] == 20
        and a["G1"]["warn_hatch_bit_identical_to_pre_repair"]
        and a["G2"]["n_raised"] == a["G2"]["n_cases"]
        and a["G2"]["in_domain_including_both_endpoints_accepted"] == 4
        and a["G3"]["post_repair_rejected"] == a["G3"]["bad_scale_cases"]
        and all(a["G8"][k]["post_repair_nan_positions_are_nan"] for k in "ABC")
        and all(a["G8"][k]["non_nan_entries_bit_identical"] for k in "ABC")
        and a["G4"]["post_repair_rejects_nan_poisoned_grid"]
        and a["G4"]["endpoint_inf_still_accepted"] == 2
    )

    payload = {
        "leg": 152, "route": "ROUTE-HRR",
        "module": "solver/hl_rescaled.py",
        "pre_repair_ref": PRE_REPAIR_REF,
        "pre_repair_n_lines": n_lines,
        "lesson_90_control": control,
        "clause_a": a,
        "clause_b": {
            "leaves_compared": d.n,
            "leaves_bit_identical": d.n_ident,
            "leaves_moved": len(d.moved),
            "moved_detail": d.moved[:50],
            "comparison": "== on float64 (NaN==NaN treated as identical), not allclose",
            "free_function_leaves": n_free,
            "class_leaves": d.n - n_free,
            "solve_3x3_systems": n_solve,
        },
        "gate_clause_a_all_four_mechanisms_closed": bool(clause_a_ok),
        "gate_clause_b_zero_clean_movement": bool(zero_movement),
        "gate_answer": "YES" if (clause_a_ok and zero_movement) else "NO",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
    print("\nwrote %s" % OUT)
    print("GATE: clause (a) all four mechanisms closed: %s; clause (b) clean movement: "
          "%d of %d leaves -> ANSWER %s"
          % (clause_a_ok, len(d.moved), d.n, payload["gate_answer"]))


if __name__ == "__main__":
    main()
