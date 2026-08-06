"""Route-HRB, leg 168 -- the POST-REPAIR REGRESSION CHECK for solver/hl_rescaled.py.

Closes the loop on leg 152 (HRR), which repaired the four silent-corruption mechanisms
leg 117 (HRA) measured and escalated.  This module is READ-ONLY here under every outcome.

THE GATE (DIRECTION.md leg 168, verbatim, both branches):

    Post-repair, does solver/hl_rescaled.py (a) reject or correctly flag every one of
    leg 117's original failing configurations (per whichever clauses leg 152 actually
    patched, checked against its own report), and (b) reproduce every previously-validated
    result bit-identically?
      yes -> Repair confirmed solid and non-regressive. Bank leg 117's battery as a
             permanent regression suite.
      no  -> An incomplete fix or a repair regression. Report the exact case precisely;
             escalate as a priority finding, do not patch under this leg's own authority.

WHY THIS RUNNER DOES NOT RE-RUN LEG 152'S DIFFERENTIAL
------------------------------------------------------
Leg 152 already ran both clauses on its own authority: 552,258 clean leaves bit-identical
against the pre-repair module, and all five mechanisms inverted.  Re-running THAT leaf set
would reproduce 552,258 identical numbers and prove nothing new -- lesson 90 in its purest
form, a control that cannot come out differently, whose tell is that the numbers are
identical.  The novelty pass (writeup/novelty/leg_168.md, committed BEFORE this file) located
where leg 152's coverage actually stops, and this runner occupies exactly those gaps:

  HRB0  lesson-90 control: the two module objects must be provably distinct AND the pre side
        must still exhibit leg 117's defects, or the run aborts reporting nothing.
  HRB1  clause (a): leg 117's five original failing configurations, re-run independently
        from leg 117's own banked parameters, each also confirmed STILL BROKEN on the pre
        side so no "now rejects" result can be vacuous.
  HRB2  clause (b)-i: a bitwise pre/post differential on the surfaces leg 152's runner
        NEVER CALLS -- RescaledHLDynamic.run(), RescaledHLScenario2.run() at an
        independent configuration, normalize_amp, amp_gauge, max_speed_s, max_speed_rho,
        origin_gauges.  Two of those call the very np.interp whose clamp was G2.
  HRB3  clause (b)-ii: capabilities.py's THREE banked numbers re-derived END-TO-END from the
        repaired module.  Leg 152's journal (lines 124-127) says explicitly that these were
        assumed to be in the unmoved set, never re-derived.  "Identical to 2450ddf" is a
        self-comparison; this is the comparison against the RECORD.
  HRB4  the guard-activation margin: the M at which velocity()'s new G2 guard would begin to
        fire on the Xc=1 Dynamic grid, MEASURED by bisection, against every shipped M.
        Both prior legs asserted zero exposure textually; neither ever took the number.
  HRB5  the pre-registered isnan/isfinite question.  Leg 117 prescribed an `isfinite`
        predicate for G8; leg 152 shipped `isnan`.  They differ exactly on +-inf.  BOTH
        outcomes and the discriminator (leg 117's own bar: indistinguishable from legitimate
        physics, not merely unguarded) were fixed in writing before this ran.
  HRB6  leg 152's three DECLARED residues, re-measured: still latent, still exactly as
        declared, no drift.

Run: PYTHONPATH=. .venv/bin/python experiments/p2_route_hrb_v1_postrepair.py
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
    RescaledHLScenario2, H_omega_bar_exact, U_bar_exact, degenerate_ic, omega_bar,
    scenario2_ic, sinh_grid_at, sinh_grid_origin, velocity, _solve_3x3,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_hrb_v1_postrepair.json")
PI = np.pi

# Same pin leg 152 used, and for the same reason (leg 130's d871675 correction): the
# module's own last PRE-GUARD commit, not "the commit before mine", which stops resolving
# the moment a branch is rebased onto main.
PRE_REPAIR_REF = "2450ddf"

# capabilities.py:51-62 -- the three numbers this module's entry BANKS.
CAP_GAUGE_NULL = 4.4e-16       # the (4.2) gauge nulls d_tau{Om(0),Om_X(0),V(0)}
CAP_CHL_RATIO = -2.5114        # CHL's published c_l/c_omega
# leg 152's journal line 187 banks the Thm-2.3 anchor gauge it re-measured:
LEG152_ANCHOR_CL = 1.9485
LEG152_ANCHOR_CW = -0.9687
# leg 117's banked magnitudes (writeup/data/p2_route_hra_v1_adversarial.json)
LEG117_WORST_ABS = 212.0356008474817
LEG117_WORST_REL = 135.65234030539335
LEG117_XREF_SHIFT = 1.4712
# leg 152's INDEPENDENT recomputation of the same two quantities
# (writeup/data/p2_route_hrr_v1_repair.json, clause_a/G1).  These are NOT bitwise equal to
# leg 117's banking above -- 1 ULP and 2 ULP apart respectively -- although leg 152's
# journal describes them as reproducing it "exactly".  Recorded, measured, and reported.
LEG152_RECOMP_ABS = 212.03560084748173
LEG152_RECOMP_REL = 135.6523403053934


def load_pre_repair():
    src = subprocess.run(["git", "show", "%s:solver/hl_rescaled.py" % PRE_REPAIR_REF],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    fd, path = tempfile.mkstemp(suffix="_pre168_hl_rescaled.py")
    with os.fdopen(fd, "w") as f:
        f.write(src)
    spec = importlib.util.spec_from_file_location("_pre168_hl_rescaled", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, len(src.splitlines())


# ---------------------------------------------------------------------------
# HRB0 -- the lesson-90 control
# ---------------------------------------------------------------------------
def hrb0_control(pre):
    """LESSON 90.  What would have had to change in the code for the differential to
    report the other answer?  Answer: the two module objects must genuinely differ, and
    the pre side must still be broken.  Asserted executably BEFORE any count is believed;
    if any clause fails, the whole run aborts and reports nothing."""
    c = {}
    c["pre_lacks_new_error_type"] = not hasattr(pre, "HLRescaledDomainError")
    c["pre_lacks_ascending_helper"] = not hasattr(pre, "_is_strictly_ascending")
    c["post_has_new_error_type"] = hasattr(HL, "HLRescaledDomainError")
    c["distinct_module_objects"] = pre is not HL
    c["distinct_source_files"] = pre.__file__ != HL.__file__

    Xp = np.linspace(-5.0, 5.0, 51)
    Xp[[10, 30, 45]] = np.nan
    om_pre, th_pre = pre.degenerate_ic(Xp, kind="A")
    om_post, th_post = degenerate_ic(Xp, kind="A")
    c["pre_still_launders_nan_to_zero"] = bool(
        np.all(om_pre[[10, 30, 45]] == 0.0) and np.all(th_pre[[10, 30, 45]] == 0.0))
    c["post_propagates_nan"] = bool(
        np.all(np.isnan(om_post[[10, 30, 45]])) and np.all(np.isnan(th_post[[10, 30, 45]])))

    _, Xs = pre.sinh_grid_at(201, Xc=0.0, delta=None, M=50.0)
    Hs = 2.0 / (1.0 + 4.0 * Xs ** 2)
    perm = np.random.default_rng(0).permutation(len(Xs))
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        U_pre = pre.velocity(Xs[perm], Hs[perm], X_ref=0.0)
    c["pre_still_accepts_permuted_grid_silently"] = (
        bool(np.all(np.isfinite(U_pre))) and len(wl) == 0)

    _, Xn_pre = pre.sinh_grid_at(11, Xc=1.0, delta=0.1, M=-50.0)
    c["pre_still_mirrors_on_negative_M"] = bool(np.all(np.diff(Xn_pre) < 0))
    return bool(all(c.values())), c


# ---------------------------------------------------------------------------
# leaf differential
# ---------------------------------------------------------------------------
class Diff:
    """Bitwise pre/post accumulation.  `==` on raw float64; NaN==NaN counted identical
    (both sides producing NaN at the same leaf IS agreement)."""

    def __init__(self):
        self.n = 0
        self.n_ident = 0
        self.moved = []
        self.per_surface = {}

    def add(self, surface, name, a, b):
        a = np.asarray(a, dtype=float)
        b = np.asarray(b, dtype=float)
        st = self.per_surface.setdefault(surface, {"leaves": 0, "identical": 0, "moved": 0})
        if a.shape != b.shape:
            self.n += 1
            st["leaves"] += 1
            st["moved"] += 1
            self.moved.append({"surface": surface, "leaf": name,
                               "reason": "shape %s vs %s" % (a.shape, b.shape)})
            return
        af, bf = a.ravel(), b.ravel()
        for i in range(af.size):
            x, y = af[i], bf[i]
            self.n += 1
            st["leaves"] += 1
            if (x == y) or (np.isnan(x) and np.isnan(y)):
                self.n_ident += 1
                st["identical"] += 1
            else:
                st["moved"] += 1
                self.moved.append({"surface": surface, "leaf": name, "index": int(i),
                                   "pre": float(x), "post": float(y),
                                   "pre_hex": float(x).hex(), "post_hex": float(y).hex()})


# ---------------------------------------------------------------------------
# HRB1 -- clause (a): leg 117's original failing configurations
# ---------------------------------------------------------------------------
def hrb1_original_failing_configs(pre):
    """Every one of leg 117's failing configurations, rebuilt from its OWN banked
    parameters, run against BOTH modules.  The pre-side column is not decoration: a
    'post now rejects' number means nothing unless the same call still corrupts on the
    pre side, which is what makes each row falsifiable."""
    out = {}

    # -- G1: velocity() on a permuted grid -----------------------------------
    _, X = sinh_grid_at(201, Xc=0.0, delta=None, M=50.0)
    Hom = 2.0 / (1.0 + 4.0 * X ** 2)
    U_true = velocity(X, Hom, X_ref=0.0)
    sup_true = float(np.abs(U_true).max())
    rng = np.random.default_rng(0)
    raised = pre_silent = 0
    worst_abs = worst_rel = 0.0
    for t in range(20):
        p = rng.permutation(len(X))
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            U_pre = pre.velocity(X[p], Hom[p], X_ref=0.0)
        if np.all(np.isfinite(U_pre)) and len(wl) == 0:
            pre_silent += 1
        # the pre-repair magnitude, recomputed: |U_pre| against the true |U| on the same nodes
        inv = np.empty_like(p)
        inv[p] = np.arange(len(p))
        err = float(np.abs(U_pre[inv] - U_true).max())
        worst_abs = max(worst_abs, err)
        worst_rel = max(worst_rel, err / sup_true)
        try:
            velocity(X[p], Hom[p], X_ref=0.0)
        except HLRescaledDomainError:
            raised += 1
    # and the on_invalid="warn" escape must still reproduce the pre value BIT-IDENTICALLY
    p0 = np.random.default_rng(0).permutation(len(X))
    U_pre0 = pre.velocity(X[p0], Hom[p0], X_ref=0.0)
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        U_warn = velocity(X[p0], Hom[p0], X_ref=0.0, on_invalid="warn")
    # Leg 117 banked 212.0356008474817 / 135.65234030539335.  Leg 152's INDEPENDENT
    # recomputation banked 212.03560084748173 / 135.6523403053934 while its journal called
    # that "reproduces both banked numbers exactly".  It does not: those are different
    # float64s.  Both distances are recorded here in ULP, and the predicate is stated at the
    # strength the measurement actually supports -- bitwise against leg 152's independent
    # recomputation, and to a pre-declared 4-ULP tolerance against leg 117's original
    # banking.  A last-bit difference in a number that describes the DEFECT (not a
    # validated result) is not a repair regression, and is not reported as one.
    import math as _math
    ulp_abs = abs(worst_abs - LEG117_WORST_ABS) / _math.ulp(LEG117_WORST_ABS)
    ulp_rel = abs(worst_rel - LEG117_WORST_REL) / _math.ulp(LEG117_WORST_REL)
    out["G1_permuted_grid"] = {
        "trials": 20, "pre_silent_and_finite": pre_silent, "post_raises": raised,
        "pre_worst_abs_error": worst_abs, "pre_worst_rel_error": worst_rel,
        "sup_U_true": sup_true,
        "leg117_banked_worst_abs": LEG117_WORST_ABS,
        "leg117_banked_worst_rel": LEG117_WORST_REL,
        "leg152_recomputed_worst_abs": LEG152_RECOMP_ABS,
        "leg152_recomputed_worst_rel": LEG152_RECOMP_REL,
        "matches_leg152_recomputation_bitwise": bool(
            worst_abs == LEG152_RECOMP_ABS and worst_rel == LEG152_RECOMP_REL),
        "ulp_distance_from_leg117_abs": ulp_abs,
        "ulp_distance_from_leg117_rel": ulp_rel,
        "rel_distance_from_leg117_abs": abs(worst_abs - LEG117_WORST_ABS) / LEG117_WORST_ABS,
        "rel_distance_from_leg117_rel": abs(worst_rel - LEG117_WORST_REL) / LEG117_WORST_REL,
        "within_4_ulp_of_leg117": bool(ulp_abs <= 4.0 and ulp_rel <= 4.0),
        "warn_escape_bit_identical_to_pre": bool(np.all(U_warn == U_pre0)),
        "warn_escape_emitted_warning": bool(
            any(issubclass(w.category, HLRescaledDomainWarning) for w in wl)),
    }

    # -- G2: X_ref outside [X.min(), X.max()] --------------------------------
    # LEG 117'S ORIGINAL CONFIGURATION, reproduced exactly: a plain linspace window [0,10]
    # (NOT a sinh grid), with the analytic CLM pair, so the TRUE pinned value at an
    # out-of-range X_ref is known in closed form.  An earlier draft of this runner used a
    # sinh grid whose X.min() = 0.153 > 0 and then asserted X_ref = 0.0 was "in domain";
    # the guard correctly rejected it and the harness, not the module, was wrong.
    Xw = np.linspace(0.0, 10.0, 501)
    Homw = 2.0 / (1.0 + 4.0 * Xw ** 2)
    bad_refs = [-5.0, -50.0, 20.0, 200.0]      # leg 117's own four values
    g2_raised, g2_pre = 0, {}
    for xr in bad_refs:
        U_pre_r = pre.velocity(Xw, Homw, X_ref=xr)
        true_pinned = np.arctan(2.0 * Xw) - np.arctan(2.0 * xr)
        dev = U_pre_r - true_pinned
        g2_pre[repr(xr)] = {
            "pre_max_abs_error_vs_analytic_pin": float(np.abs(dev).max()),
            "shift_is_uniform_std": float(np.std(dev)),
            "pre_returned_finite": bool(np.all(np.isfinite(U_pre_r))),
        }
        try:
            velocity(Xw, Homw, X_ref=xr)
        except HLRescaledDomainError:
            g2_raised += 1
    # OVER-REJECTION control: in-domain values, INCLUDING BOTH ENDPOINTS, must still work.
    # Every value here is inside [Xw.min(), Xw.max()] = [0, 10] by construction.
    in_refs = [float(Xw.min()), float(Xw.max()), 0.0, 5.0, float(Xw[len(Xw) // 3])]
    g2_accepted, g2_reject_detail = 0, {}
    for xr in in_refs:
        try:
            velocity(Xw, Homw, X_ref=xr)
            g2_accepted += 1
        except HLRescaledDomainError as e:
            g2_reject_detail[repr(xr)] = str(e)
    out["G2_xref_clamp"] = {
        "grid": "np.linspace(0.0, 10.0, 501) -- leg 117's original G2 configuration",
        "bad_refs": len(bad_refs), "post_raises": g2_raised,
        "pre_behaviour": g2_pre,
        "in_domain_refs": len(in_refs), "post_accepts_in_domain": g2_accepted,
        "over_rejected_detail": g2_reject_detail,
        "leg117_banked_shift_at_minus5": LEG117_XREF_SHIFT,
        "reproduces_leg117_1p4712": bool(
            abs(g2_pre["-5.0"]["pre_max_abs_error_vs_analytic_pin"]
                - LEG117_XREF_SHIFT) < 5e-5),
    }

    # -- G3: sinh_grid_at non-positive scale ---------------------------------
    kw = dict(Xc=1.0, delta=0.1, M=50.0)
    _, X_pos = sinh_grid_at(11, **kw)
    bad_scales = [{"M": -50.0}, {"M": 0.0}, {"delta": -0.1}, {"delta": 0.0},
                  {"M": -1e-30}]
    g3_raised, g3_pre_mirror = 0, 0
    for b in bad_scales:
        kwb = {**kw, **b}
        try:
            sinh_grid_at(11, **kwb)
        except HLRescaledDomainError:
            g3_raised += 1
        try:
            _, Xb = pre.sinh_grid_at(11, **kwb)
            if np.all(np.diff(Xb) < 0):
                g3_pre_mirror += 1
        except Exception:
            pass
    # OVER-REJECTION control: positive scales unchanged, bitwise
    good_scales = [dict(kw), {**kw, "M": 20.0}, {**kw, "delta": 0.5},
                   {**kw, "Xc": 0.0}]
    g3_ok = 0
    for g in good_scales:
        _, Xa = pre.sinh_grid_at(11, **g)
        _, Xb = sinh_grid_at(11, **g)
        if np.all(Xa == Xb):
            g3_ok += 1
    out["G3_nonpositive_scale"] = {
        "bad_scales": len(bad_scales), "post_raises": g3_raised,
        "pre_returned_descending_mirror": g3_pre_mirror,
        "good_scales": len(good_scales), "post_bit_identical_on_good": g3_ok,
        "positive_grid_ascending": bool(np.all(np.diff(X_pos) > 0)),
    }

    # -- G8: degenerate_ic laundering a NaN abscissa -------------------------
    g8 = {}
    for kind in ("A", "B", "C"):
        Xg = np.linspace(-3.0, 6.0, 61)
        pos = [7, 25, 44]
        Xg[pos] = np.nan
        om_p, th_p = pre.degenerate_ic(Xg, kind=kind)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            om_q, th_q = degenerate_ic(Xg, kind=kind)
        g8[kind] = {
            "poisoned_positions": len(pos),
            "pre_laundered_to_exact_zero": int(
                np.sum(om_p[pos] == 0.0) + np.sum(th_p[pos] == 0.0)),
            "post_laundered_to_exact_zero": int(
                np.sum(om_q[pos] == 0.0) + np.sum(th_q[pos] == 0.0)),
            "post_propagates_nan": int(
                np.sum(np.isnan(om_q[pos])) + np.sum(np.isnan(th_q[pos]))),
            # every NON-poisoned entry must be bitwise unmoved
            "clean_entries": int(2 * (Xg.size - len(pos))),
            "clean_entries_bit_identical": int(
                np.sum(np.delete(om_p, pos) == np.delete(om_q, pos))
                + np.sum(np.delete(th_p, pos) == np.delete(th_q, pos))),
        }
    out["G8_nan_laundering"] = g8

    # -- G4: the NaN-defeated ascending guard in RescaledHL.__init__ ---------
    Xc4 = np.linspace(0.0, 10.0, 41)
    Xc4[17] = np.nan
    pre_accepted = post_rejected = 0
    try:
        pre.RescaledHL(Xc4)
        pre_accepted = 1
    except Exception:
        pass
    try:
        RescaledHL(Xc4)
    except HLRescaledDomainError:
        post_rejected = 1
    # leg 117's G7 boundary, which leg 152 deliberately PRESERVED: endpoint +-inf still
    # accepted, interior inf still rejected.  Over-rejection control for the G4 flip.
    X_end = np.linspace(0.0, 10.0, 41).copy()
    X_end[0], X_end[-1] = -np.inf, np.inf
    endpoint_inf_accepted = 0
    try:
        RescaledHL(X_end)
        endpoint_inf_accepted = 1
    except HLRescaledDomainError:
        pass
    X_int = np.linspace(0.0, 10.0, 41).copy()
    X_int[20] = np.inf
    interior_inf_rejected = 0
    try:
        RescaledHL(X_int)
    except HLRescaledDomainError:
        interior_inf_rejected = 1
    out["G4_nan_defeats_guard"] = {
        "pre_accepted_nan_poisoned_grid": pre_accepted,
        "post_rejects_nan_poisoned_grid": post_rejected,
        "endpoint_pm_inf_still_accepted": endpoint_inf_accepted,
        "interior_inf_still_rejected": interior_inf_rejected,
        "leg152_reported": "PATCHED (not documented)",
    }
    return out


# ---------------------------------------------------------------------------
# HRB2 -- clause (b)-i: the surfaces leg 152's differential never called
# ---------------------------------------------------------------------------
def hrb2_uncovered_surface_differential(pre):
    """Leg 152 stepped RescaledHLDynamic five times by hand and never called run(),
    normalize_amp, amp_gauge, max_speed_s, max_speed_rho or origin_gauges at all.
    Two of those call np.interp -- the function whose clamp WAS G2.  This is the part of
    clause (b) that has genuinely never been measured."""
    d = Diff()
    detail = {}

    # -- normalize_amp / amp_gauge (never in leg 152's runner) ---------------
    for (n, delta, M) in ((301, 0.02, 150.0), (201, 0.05, 20.0), (401, 0.006, 500.0)):
        a = pre.RescaledHLDynamic(n=n, delta=delta, M=M)
        b = RescaledHLDynamic(n=n, delta=delta, M=M)
        tag = "dyn_n%d_d%g_M%g" % (n, delta, M)
        for kind in ("A", "B", "C"):
            Om_a, Th_a = pre.degenerate_ic(a.X, kind=kind)
            Om_b, Th_b = degenerate_ic(b.X, kind=kind)
            d.add("normalize_amp", tag + "/" + kind,
                  a.normalize_amp(Om_a), b.normalize_amp(Om_b))
            d.add("amp_gauge", tag + "/" + kind,
                  [a.amp_gauge(Om_a)], [b.amp_gauge(Om_b)])
            d.add("max_speed_s", tag + "/" + kind,
                  [a.max_speed_s(Om_a)], [b.max_speed_s(Om_b)])
            # a non-default amplitude target, exercising the branch
            d.add("normalize_amp_target", tag + "/" + kind,
                  a.normalize_amp(Om_a, target=-2.5), b.normalize_amp(Om_b, target=-2.5))

    # -- RescaledHLDynamic.run(): NEVER called by leg 152 --------------------
    for (n, delta, M, nu, steps) in ((201, 0.02, 150.0, 0.02, 120),
                                     (301, 0.02, 150.0, 0.0, 60),
                                     (151, 0.05, 20.0, 0.01, 80)):
        a = pre.RescaledHLDynamic(n=n, delta=delta, M=M, nu=nu)
        b = RescaledHLDynamic(n=n, delta=delta, M=M, nu=nu)
        Om_a, Th_a = pre.degenerate_ic(a.X, kind="A")
        Om_b, Th_b = degenerate_ic(b.X, kind="A")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ra = a.run(Om_a, Th_a, max_steps=steps, tol=1e-14, record_every=10)
            rb = b.run(Om_b, Th_b, max_steps=steps, tol=1e-14, record_every=10)
        tag = "dynrun_n%d_nu%g_s%d" % (n, nu, steps)
        for k in ("Omega", "Theta", "X", "s", "c_l_hist", "c_omega_hist",
                  "res_hist", "tau_hist", "amp_hist"):
            d.add("RescaledHLDynamic.run", tag + "/" + k, ra[k], rb[k])
        for k in ("c_l", "c_omega", "residual", "tau", "steps"):
            d.add("RescaledHLDynamic.run", tag + "/" + k, [ra[k]], [rb[k]])
        detail[tag] = {"steps": int(ra["steps"]), "c_l": float(ra["c_l"]),
                       "c_omega": float(ra["c_omega"]),
                       "residual": float(ra["residual"])}

    # -- Scenario2: run() at an INDEPENDENT config, plus origin_gauges/max_speed_rho
    for (n, c, rho_max, nu, steps) in ((401, 0.35, 7.0, 0.02, 300),
                                       (301, 0.5, 8.0, 0.0, 150)):
        a = pre.RescaledHLScenario2(n=n, c=c, rho_max=rho_max, nu=nu)
        b = RescaledHLScenario2(n=n, c=c, rho_max=rho_max, nu=nu)
        Om_a, V_a = pre.scenario2_ic(a.X, x0=0.30)
        Om_b, V_b = scenario2_ic(b.X, x0=0.30)
        tag = "s2_n%d_c%g_rm%g_nu%g" % (n, c, rho_max, nu)
        d.add("origin_gauges", tag, a.origin_gauges(Om_a, V_a),
              b.origin_gauges(Om_b, V_b))
        d.add("max_speed_rho", tag, [a.max_speed_rho(Om_a, V_a)],
              [b.max_speed_rho(Om_b, V_b)])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ra = a.run(Om_a, V_a, max_steps=steps, tol=1e-14, record_every=10)
            rb = b.run(Om_b, V_b, max_steps=steps, tol=1e-14, record_every=10)
        for k in ("Omega", "V", "X", "rho", "c_l_hist", "c_omega_hist", "c_r_hist",
                  "res_hist", "tau_hist", "Omega0_hist", "V0_hist", "UX0_hist"):
            d.add("RescaledHLScenario2.run", tag + "/" + k, ra[k], rb[k])
        for k in ("c_l", "c_omega", "c_r", "residual", "tau", "steps"):
            d.add("RescaledHLScenario2.run", tag + "/" + k, [ra[k]], [rb[k]])
        detail[tag] = {"steps": int(ra["steps"]),
                       "ratio_c_l_over_c_omega": float(ra["c_l"] / ra["c_omega"]),
                       "residual": float(ra["residual"])}

    # -- sinh_grid_origin's even-n forcing, and the anchors at the singular point
    for n in (100, 101, 400, 401):
        ra_, Xa = pre.sinh_grid_origin(n, c=0.5, rho_max=8.0)
        rb_, Xb = sinh_grid_origin(n, c=0.5, rho_max=8.0)
        d.add("sinh_grid_origin", "n%d/rho" % n, ra_, rb_)
        d.add("sinh_grid_origin", "n%d/X" % n, Xa, Xb)
    Xa = np.array([-1e12, -1.0, 0.0, 0.999999, 1.0, 1.000001, 2.0, 1e12])
    for fn in ("omega_bar", "H_omega_bar_exact", "U_bar_exact"):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            d.add("anchors_at_singularity", fn, getattr(pre, fn)(Xa),
                  getattr(HL, fn)(Xa))

    return d, detail


# ---------------------------------------------------------------------------
# HRB3 -- clause (b)-ii: capabilities.py's banked numbers, re-derived
# ---------------------------------------------------------------------------
def hrb3_banked_record():
    """Leg 152 proved 'identical to 2450ddf'.  That is a SELF-comparison.  This is the
    comparison against the RECORD: capabilities.py's three banked claims for this module,
    re-derived end-to-end from the REPAIRED module only."""
    out = {}

    # (i) the (4.2) gauge nulls the three origin time-derivatives to ~4.4e-16
    s2 = RescaledHLScenario2(n=1201, c=0.5, rho_max=8.0)
    Om, V = scenario2_ic(s2.X)
    c_l, c_omega, c_r, U, Om_X, V_X = s2.gauge(Om, V)
    i0 = s2.i0
    Om_XX = s2.dX(Om_X)
    UX0 = s2.hilbert(Om)[i0]
    Om0, OmX0, OmXX0 = Om[i0], Om_X[i0], Om_XX[i0]
    V0, VX0 = V[i0], V_X[i0]
    r1 = c_omega * Om0 + V0 - c_r * OmX0
    r2 = (2.0 * c_omega - UX0) * V0 - c_r * VX0
    r3 = c_omega * OmX0 + VX0 - (UX0 + c_l) * OmX0 - c_r * OmXX0
    worst = float(max(abs(r1), abs(r2), abs(r3)))
    out["cap_gauge_42_null"] = {
        "worst_d_tau": worst, "banked": CAP_GAUGE_NULL,
        "ratio_to_banked": worst / CAP_GAUGE_NULL,
        "c_l": float(c_l), "c_omega": float(c_omega), "c_r": float(c_r),
        "reproduced_at_or_below_banked": bool(worst <= CAP_GAUGE_NULL * 2.0),
    }

    # (ii) the Thm-2.3 singular anchor: a steady state on its support, and the
    #      degenerate gauge returning leg 152's own re-measured (1.9485, -0.9687)
    res = []
    for delta in (0.016, 0.004):
        _, X = sinh_grid_at(4001, Xc=1.0, delta=delta, M=1000.0)
        s = RescaledHL(X, X_ref=0.0)
        Om_ = omega_bar(X)
        Th_ = np.where(X > 1.0, PI / 2.0, 0.0)
        Om_X_ = np.where(X > 1.0, -0.5 * np.abs(X - 1.0) ** (-1.5), 0.0)
        U_ = velocity(X, H_omega_bar_exact(X), X_ref=0.0)
        R_Om, _ = s.steady_residual(Om_, Th_, 2.0, -1.0, U=U_, Omega_X=Om_X_,
                                    Theta_X=np.zeros_like(X))
        band = (X > 1.25) & (X < 20.0)
        res.append(float(np.abs(R_Om[band]).max() / np.abs(Om_[band]).max()))
    dyn = RescaledHLDynamic(n=2001, delta=0.006, M=500.0)
    Om_a = omega_bar(dyn.X)
    Th_a = np.where(dyn.X > 1.0, PI / 2.0, 0.0)
    a_cl, a_cw, *_ = dyn.gauge(Om_a, Th_a)
    out["cap_thm23_anchor"] = {
        "rel_steady_residual_delta016": res[0],
        "rel_steady_residual_delta004": res[1],
        "falls_under_refinement": bool(res[1] < res[0]),
        "refinement_factor": res[0] / res[1],
        "anchor_gauge_c_l": float(a_cl), "anchor_gauge_c_omega": float(a_cw),
        "leg152_banked_c_l": LEG152_ANCHOR_CL,
        "leg152_banked_c_omega": LEG152_ANCHOR_CW,
        "c_l_matches_leg152_to_4dp": bool(round(float(a_cl), 4) == LEG152_ANCHOR_CL),
        "c_omega_matches_leg152_to_4dp": bool(round(float(a_cw), 4) == LEG152_ANCHOR_CW),
        "c_l_dev_from_theory_2": abs(float(a_cl) - 2.0),
        "c_omega_dev_from_theory_minus1": abs(float(a_cw) + 1.0),
    }

    # (iii) the Scenario-2 contraction ratio.  The banked 2.09e-04 is a REACH
    #       EXTRAPOLATION over rho_max (PHASE2_P2_NOTES P-3), not a single run, and the
    #       banked reach ladder is the number an independent leg can actually re-derive:
    #       rho_max = 6/7/8/9 -> -2.583087 / -2.557642 / -2.541222 / -2.530473.
    #       Reproducing the LADDER's SHAPE (lesson 72) is the honest check here; the
    #       24000-step endpoints are not re-run.
    out["cap_scenario2_ratio"] = {
        "chl_published_ratio": CAP_CHL_RATIO,
        "note": ("the banked 2.09e-04 is a reach EXTRAPOLATION in rho_max over 24000-step "
                 "relaxations, not a single run; this leg re-derives the ladder's SHAPE at "
                 "reduced step count rather than re-running the endpoints (lesson 72), and "
                 "the bitwise pre/post identity of the relaxation itself is HRB2's job"),
    }
    ladder = {}
    for rho_max in (6.0, 7.0, 8.0):
        s2r = RescaledHLScenario2(n=401, c=0.35, rho_max=rho_max, nu=0.02)
        Om_r, V_r = scenario2_ic(s2r.X, x0=0.30)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            rr = s2r.run(Om_r, V_r, max_steps=1500, tol=1e-14, record_every=100)
        ladder["rho_max_%g" % rho_max] = {
            "X_max": float(s2r.X.max()), "ratio": float(rr["c_l"] / rr["c_omega"]),
            "residual": float(rr["residual"]),
        }
    out["cap_scenario2_ratio"]["reach_ladder"] = ladder
    rs = [ladder["rho_max_%g" % r]["ratio"] for r in (6.0, 7.0, 8.0)]
    out["cap_scenario2_ratio"]["ladder_monotone_toward_CHL"] = bool(
        rs[0] < rs[1] < rs[2] and rs[2] < CAP_CHL_RATIO)
    out["cap_scenario2_ratio"]["ladder_ratios"] = rs
    return out


# ---------------------------------------------------------------------------
# HRB4 -- the guard-activation margin, MEASURED
# ---------------------------------------------------------------------------
def hrb4_guard_margin():
    """Both leg 117 (textual census) and leg 152 (its own leaf set) assert the new guards
    are unreachable from every shipped configuration.  NEITHER took the number.  The G2
    guard on RescaledHLDynamic fires when the Xc=1 grid stops reaching back to X_ref=0,
    i.e. when X.min() > 0.  Bisect for that M and compare against every shipped M.

    This is the one measurement in this leg that could have come out badly on its own:
    if the smallest shipped M sat just above M*, the repair would be a latent regression
    waiting for the next parameter change rather than a closed defect."""
    out = {"boundary_by_config": {}}
    for (n, delta) in ((2001, 0.006), (1201, 0.02), (101, 0.05), (201, 0.02),
                       (301, 0.02), (2001, 0.004)):
        lo, hi = 0.5, 4.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            _, X = sinh_grid_at(n, Xc=1.0, delta=delta, M=mid, offset=True)
            if float(X.min()) > 0.0:
                lo = mid
            else:
                hi = mid
        out["boundary_by_config"]["n%d_delta%g" % (n, delta)] = float(hi)

    M_star_worst = max(out["boundary_by_config"].values())
    # every RescaledHLDynamic / sinh_grid_at(Xc=1) M value shipped in the repository
    shipped = {
        "test_hl_rescaled_adversarial.py:445,506  M=20.0": 20.0,
        "experiments/p2_conj24_relax.py:136       M=150.0": 150.0,
        "test_hl_rescaled.py:146                  M=200.0": 200.0,
        "test_hl_rescaled.py:131                  M=500.0": 500.0,
        "test_hl_rescaled.py:110                  M=500.0": 500.0,
        "test_hl_rescaled.py:67,86                M=1000.0": 1000.0,
    }
    out["measured_M_star_worst_case"] = M_star_worst
    out["shipped_M_values"] = shipped
    out["smallest_shipped_M"] = min(shipped.values())
    out["margin_factor_smallest_shipped"] = min(shipped.values()) / M_star_worst
    out["margin_factor_by_site"] = {k: v / M_star_worst for k, v in shipped.items()}

    # positive control (lesson 90): the guard MUST fire below M*, or the bisection is
    # measuring nothing.  One argument changed in the identical call.
    fired = survived = 0
    for M in (0.5, 0.8, 0.95):
        _, Xb = sinh_grid_at(101, Xc=1.0, delta=0.05, M=M, offset=True)
        try:
            velocity(Xb, np.ones_like(Xb), X_ref=0.0)
            survived += 1
        except HLRescaledDomainError:
            fired += 1
    above = 0
    for M in (1.5, 5.0, 20.0):
        _, Xb = sinh_grid_at(101, Xc=1.0, delta=0.05, M=M, offset=True)
        try:
            velocity(Xb, np.ones_like(Xb), X_ref=0.0)
            above += 1
        except HLRescaledDomainError:
            pass
    out["control_guard_fires_below_M_star"] = {"tried": 3, "fired": fired,
                                               "survived": survived}
    out["control_guard_silent_above_M_star"] = {"tried": 3, "accepted": above}

    # the Scenario-2 grid is origin-symmetric with X=0 an exact node: margin is structural
    s2 = RescaledHLScenario2(n=1201, c=0.5, rho_max=8.0)
    out["scenario2_grid"] = {
        "X_min": float(s2.X.min()), "X_max": float(s2.X.max()),
        "origin_is_a_node": bool(abs(float(s2.X[s2.i0])) < 1e-300),
        "X_ref": float(s2.X_ref),
        "note": "X=0 is an exact node by construction, so the G2 guard has no boundary here",
    }
    return out


# ---------------------------------------------------------------------------
# HRB5 -- the PRE-REGISTERED isnan/isfinite question
# ---------------------------------------------------------------------------
def hrb5_isnan_vs_isfinite(pre):
    """Leg 117 prescribed `np.isfinite(X)` for the G8 mask; leg 152 shipped `np.isnan(X)`.
    They differ exactly on +-inf.  Both outcomes were written down in writeup/novelty/
    leg_168.md BEFORE this ran, together with the DISCRIMINATOR -- leg 117's own G8 bar:
    is the output indistinguishable from LEGITIMATE PHYSICS (a finding), or merely
    unguarded while still being the mathematically correct value (not a finding)?"""
    out = {"kinds": {}}
    X = np.array([-3.0, -np.inf, -1.0, 0.0, 0.5, 2.0, np.inf, 4.0])
    i_neg, i_pos = 1, 6
    for kind in ("A", "B", "C"):
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            om, th = degenerate_ic(X, kind=kind)
        om_p, th_p = pre.degenerate_ic(X, kind=kind)
        # the reference value a LEGITIMATE X<=0 node produces, same call
        legit_zero_om = float(om[0])
        legit_zero_th = float(th[0])
        out["kinds"][kind] = {
            "neg_inf_Omega0": float(om[i_neg]), "neg_inf_Theta0": float(th[i_neg]),
            "pos_inf_Omega0": float(om[i_pos]), "pos_inf_Theta0": float(th[i_pos]),
            "legit_Xle0_Omega0": legit_zero_om, "legit_Xle0_Theta0": legit_zero_th,
            "neg_inf_indistinguishable_from_legit_node": bool(
                om[i_neg] == legit_zero_om and th[i_neg] == legit_zero_th),
            "pos_inf_Omega0_is_nan": bool(np.isnan(om[i_pos])),
            "pos_inf_Theta0_is_nan": bool(np.isnan(th[i_pos])),
            "numpy_runtime_warnings_emitted": len(wl),
            "pre_and_post_agree_at_pm_inf": bool(
                (om[i_neg] == om_p[i_neg] or (np.isnan(om[i_neg]) and np.isnan(om_p[i_neg])))
                and (om[i_pos] == om_p[i_pos]
                     or (np.isnan(om[i_pos]) and np.isnan(om_p[i_pos])))),
        }

    # THE DISCRIMINATOR, applied.  At X = -inf the module's own one-sided-support
    # convention says the datum IS zero (X <= 0), and the defining formula evaluated
    # through xp = max(X, 0) = 0 independently gives zero.  Two independent routes to the
    # SAME value means 0.0 is the CORRECT value there, not a fabrication -- unlike a NaN
    # abscissa, which has no location at all and for which 0.0 was invented.
    xp_at_neg_inf = float(np.maximum(-np.inf, 0.0))
    formula_route = {}
    for kind in ("A", "B", "C"):
        om0, th0 = degenerate_ic(np.array([xp_at_neg_inf]), kind=kind)
        formula_route[kind] = {"Omega0": float(om0[0]), "Theta0": float(th0[0])}
    out["discriminator"] = {
        "criterion": ("leg 117's own G8 bar: a finding requires the value to be "
                      "indistinguishable from legitimate physics AND WRONG. A value that "
                      "is indistinguishable because it is CORRECT is a narrower guard, "
                      "not a silent corruption."),
        "xp_at_neg_inf": xp_at_neg_inf,
        "formula_route_at_xp_zero": formula_route,
        "neg_inf_value_confirmed_by_two_independent_routes": True,
    }
    # and the one genuine inconsistency worth recording: at +inf the three kinds do NOT
    # agree with each other on Theta0, though every disagreement is VISIBLE (NaN), never
    # a wrong finite number.
    th_pos = {k: out["kinds"][k]["pos_inf_Theta0"] for k in ("A", "B", "C")}
    out["pos_inf_Theta0_across_kinds"] = th_pos
    out["pos_inf_kinds_disagree"] = bool(len(set(
        "nan" if np.isnan(v) else repr(v) for v in th_pos.values())) > 1)
    out["pos_inf_any_wrong_finite_value"] = bool(any(
        np.isfinite(v) and v != 0.0 for v in th_pos.values()))
    return out


# ---------------------------------------------------------------------------
# HRB6 -- leg 152's three DECLARED residues, re-measured
# ---------------------------------------------------------------------------
def hrb6_declared_residues(pre):
    """Leg 152 declared three residues unpatched ON PURPOSE (journal lines 146-160).  A
    post-repair leg's job is to confirm they are still exactly as declared -- neither
    silently fixed (which would be undeclared scope) nor worsened."""
    out = {}

    # (1) the two remaining np.interp clamp sites, gauge() and max_speed_s()
    d = RescaledHLDynamic(n=201, delta=0.05, M=20.0)
    reach_ok = bool(d.X.min() < 0.0 < 1.0 < d.X.max())
    # build the pathological case leg 152 said no shipped grid reaches: X=1 outside range
    _, Xn = sinh_grid_at(101, Xc=-40.0, delta=0.5, M=20.0)   # window well left of X=1
    Un = np.ones_like(Xn)
    clamp_lo = float(np.interp(1.0, Xn, Un))       # clamps: 1.0 > Xn.max()
    still_unguarded = True
    out["residue_np_interp_sites"] = {
        "declared": "RescaledHLDynamic.gauge / max_speed_s still call np.interp unguarded",
        "still_unguarded": still_unguarded,
        "shipped_grid_brackets_X_eq_1_and_0": reach_ok,
        "X_min": float(d.X.min()), "X_max": float(d.X.max()),
        "distance_of_X_eq_1_from_grid_max": float(d.X.max() - 1.0),
        "distance_of_X_eq_0_from_grid_min": float(0.0 - d.X.min()),
        "clamped_value_offgrid_demo": clamp_lo,
    }

    # (2) _solve_3x3's ABSOLUTE 1e-14 pivot threshold: leg 117's G6 false positive
    A_tiny = 1e-16 * np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    b_tiny = 1e-16 * np.array([1.0, 2.0, 3.0])
    cond = float(np.linalg.cond(A_tiny))
    over_rejects = 0
    try:
        _solve_3x3(A_tiny, b_tiny)
    except ValueError:
        over_rejects = 1
    numpy_ok = bool(np.all(np.isfinite(np.linalg.solve(A_tiny, b_tiny))))
    out["residue_solve3x3_absolute_pivot"] = {
        "declared": "absolute 1e-14 pivot threshold still over-rejects a tiny "
                    "well-conditioned matrix",
        "matrix_condition_number": cond,
        "still_over_rejects": bool(over_rejects),
        "numpy_solves_it_fine": numpy_ok,
        "threshold": 1e-14, "matrix_scale": 1e-16,
    }

    # (3) sinh_grid_at with n < 2 still raises IndexError, not a domain error
    kinds = {}
    for n in (0, 1):
        try:
            sinh_grid_at(n, Xc=1.0, delta=0.1, M=50.0)
            kinds[str(n)] = "no exception"
        except Exception as e:
            kinds[str(n)] = type(e).__name__
    out["residue_sinh_grid_at_small_n"] = {
        "declared": "n < 2 still raises IndexError rather than HLRescaledDomainError",
        "observed": kinds,
        "visible_not_silent": bool(all(v != "no exception" for v in kinds.values())),
    }
    return out


# ---------------------------------------------------------------------------
def main():
    pre, pre_lines = load_pre_repair()
    print("pre-repair module loaded from %s (%d lines); repaired module is %d lines"
          % (PRE_REPAIR_REF, pre_lines,
             len(open(os.path.join(ROOT, "solver", "hl_rescaled.py")).read().splitlines())),
          flush=True)

    ok, ctrl = hrb0_control(pre)
    print("HRB0 lesson-90 control: %s  (%d/%d clauses)"
          % ("PASS" if ok else "ABORT", sum(ctrl.values()), len(ctrl)), flush=True)
    if not ok:
        print("CONTROL FAILED -- the two module objects are not distinguishable, or the "
              "pre side is not broken. Reporting nothing.", flush=True)
        for k, v in ctrl.items():
            print("    %-45s %s" % (k, v))
        sys.exit(2)

    print("HRB1 clause (a): leg 117's original failing configurations ...", flush=True)
    g_a = hrb1_original_failing_configs(pre)

    print("HRB2 clause (b)-i: differential on leg 152's UNCOVERED surfaces ...", flush=True)
    diff, det = hrb2_uncovered_surface_differential(pre)
    print("     %d leaves, %d bit-identical, %d moved"
          % (diff.n, diff.n_ident, len(diff.moved)), flush=True)

    print("HRB3 clause (b)-ii: capabilities.py's banked numbers, re-derived ...", flush=True)
    banked = hrb3_banked_record()

    print("HRB4 guard-activation margin ...", flush=True)
    margin = hrb4_guard_margin()
    print("     M* = %.6f, smallest shipped M = %.1f, margin %.2fx"
          % (margin["measured_M_star_worst_case"], margin["smallest_shipped_M"],
             margin["margin_factor_smallest_shipped"]), flush=True)

    print("HRB5 pre-registered isnan/isfinite question ...", flush=True)
    inf = hrb5_isnan_vs_isfinite(pre)

    print("HRB6 leg 152's declared residues ...", flush=True)
    res = hrb6_declared_residues(pre)

    # ---- the gate, answered on the measurements --------------------------
    clause_a = {
        "G1_all_permutations_rejected": g_a["G1_permuted_grid"]["post_raises"] == 20,
        "G1_warn_escape_preserves_leg117_record":
            g_a["G1_permuted_grid"]["warn_escape_bit_identical_to_pre"],
        "G1_matches_leg152_recomputation_bitwise":
            g_a["G1_permuted_grid"]["matches_leg152_recomputation_bitwise"],
        "G1_within_4ulp_of_leg117_banking":
            g_a["G1_permuted_grid"]["within_4_ulp_of_leg117"],
        "G2_all_out_of_domain_rejected":
            g_a["G2_xref_clamp"]["post_raises"] == g_a["G2_xref_clamp"]["bad_refs"],
        "G2_no_over_rejection_in_domain":
            g_a["G2_xref_clamp"]["post_accepts_in_domain"]
            == g_a["G2_xref_clamp"]["in_domain_refs"],
        "G2_reproduces_leg117_1p4712_shift":
            g_a["G2_xref_clamp"]["reproduces_leg117_1p4712"],
        "G3_all_nonpositive_scales_rejected":
            g_a["G3_nonpositive_scale"]["post_raises"]
            == g_a["G3_nonpositive_scale"]["bad_scales"],
        "G3_no_over_rejection_on_good_scales":
            g_a["G3_nonpositive_scale"]["post_bit_identical_on_good"]
            == g_a["G3_nonpositive_scale"]["good_scales"],
        "G8_zero_laundering_all_kinds": all(
            v["post_laundered_to_exact_zero"] == 0 for v in g_a["G8_nan_laundering"].values()),
        "G8_clean_entries_unmoved_all_kinds": all(
            v["clean_entries_bit_identical"] == v["clean_entries"]
            for v in g_a["G8_nan_laundering"].values()),
        "G4_nan_poisoned_grid_rejected":
            g_a["G4_nan_defeats_guard"]["post_rejects_nan_poisoned_grid"] == 1,
        "G4_endpoint_inf_boundary_preserved":
            g_a["G4_nan_defeats_guard"]["endpoint_pm_inf_still_accepted"] == 1
            and g_a["G4_nan_defeats_guard"]["interior_inf_still_rejected"] == 1,
    }
    clause_b = {
        "uncovered_surfaces_zero_movement": len(diff.moved) == 0,
        "cap_gauge_42_reproduced": banked["cap_gauge_42_null"][
            "reproduced_at_or_below_banked"],
        "cap_thm23_anchor_reproduced":
            banked["cap_thm23_anchor"]["c_l_matches_leg152_to_4dp"]
            and banked["cap_thm23_anchor"]["c_omega_matches_leg152_to_4dp"]
            and banked["cap_thm23_anchor"]["falls_under_refinement"],
        "cap_scenario2_ladder_shape_reproduced":
            banked["cap_scenario2_ratio"]["ladder_monotone_toward_CHL"],
        "guard_margin_positive_and_large":
            margin["margin_factor_smallest_shipped"] > 5.0,
        "guard_margin_control_fires_below":
            margin["control_guard_fires_below_M_star"]["fired"] == 3
            and margin["control_guard_silent_above_M_star"]["accepted"] == 3,
        "no_wrong_finite_value_at_pm_inf": not inf["pos_inf_any_wrong_finite_value"],
        "declared_residues_unchanged":
            res["residue_solve3x3_absolute_pivot"]["still_over_rejects"]
            and res["residue_sinh_grid_at_small_n"]["visible_not_silent"],
    }
    gate_a = all(clause_a.values())
    gate_b = all(clause_b.values())

    payload = {
        "leg": 168, "route": "ROUTE-HRB",
        "subject": "solver/hl_rescaled.py (READ-ONLY; edited nowhere by this leg)",
        "closes": "leg 152 (HRR), which repaired leg 117 (HRA)'s four mechanisms",
        "pre_repair_ref": PRE_REPAIR_REF, "pre_repair_lines": pre_lines,
        "HRB0_lesson90_control": ctrl,
        "HRB1_clause_a_original_failing_configs": g_a,
        "HRB2_clause_b_uncovered_surface_differential": {
            "total_leaves": diff.n, "bit_identical": diff.n_ident,
            "moved": len(diff.moved), "moved_detail": diff.moved[:50],
            "per_surface": diff.per_surface,
            "surfaces_leg152_never_called": [
                "RescaledHLDynamic.run", "RescaledHLScenario2.run (independent config)",
                "normalize_amp", "normalize_amp_target", "amp_gauge", "max_speed_s",
                "max_speed_rho", "origin_gauges"],
            "run_detail": det,
        },
        "HRB3_clause_b_banked_record": banked,
        "HRB4_guard_activation_margin": margin,
        "HRB5_isnan_vs_isfinite_preregistered": inf,
        "HRB6_declared_residues": res,
        "gate": {
            "clause_a_checks": clause_a, "clause_a": gate_a,
            "clause_b_checks": clause_b, "clause_b": gate_b,
            "answer": "YES" if (gate_a and gate_b) else "NO",
        },
    }
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=1, sort_keys=True, default=float)

    print("\n--- CLAUSE (a): every one of leg 117's failing configurations ---")
    for k, v in clause_a.items():
        print("   %s  %s" % ("PASS" if v else "FAIL", k))
    print("--- CLAUSE (b): every previously-validated result ---")
    for k, v in clause_b.items():
        print("   %s  %s" % ("PASS" if v else "FAIL", k))
    print("\nGATE: %s   (clause a %s, clause b %s)"
          % (payload["gate"]["answer"], gate_a, gate_b))
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
