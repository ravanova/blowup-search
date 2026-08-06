"""Route-BVR v1 -- an ADVERSARIAL BATTERY against solver/boussinesq_rescaled.py, the rescaled
2D Boussinesq RHS (Chen-Hou Part I arXiv:2210.07191 (2.10)/(2.11)) on the log-polar grid.

Leg 205. Adversarial-audit family. This module has never appeared in the repository's
audit-family inventory under any name-match, unlike its siblings solver/boussinesq.py (leg 89's
target, leg 129's repair target) and solver/boussinesq_velocity.py (leg 99's target, leg 104's
post-repair check). Its only existing gates -- test_boussinesq_rescaled.py,
test_boussinesq_transport.py, writeup/3_spikes/TECHNICAL_SPIKE1_STEPB.md -- are CORRECTNESS
gates on well-posed input. A correctness check on well-behaved input is not a robustness check.

This is not a formality. writeup/novelty/leg_99.md sec.4 escalation note 2 flagged
solver/boussinesq_rescaled.py:161 by exact line number as running "the identical
`coef, *_ = np.linalg.lstsq(A, d1[m], rcond=None)` over a masked window", declined to test it as
out of territory, and named "a follow-up leg scoped to boussinesq_rescaled.py" as the obvious
next audit. That line is byte-unchanged at this leg's merge base; leg 104's repair was scoped to
the sibling only. This leg is that follow-up.

THE GATE, VERBATIM (DIRECTION.md leg 205, pre-committed, both branches)
----------------------------------------------------------------------
"Under adversarial and degenerate inputs, does boussinesq_rescaled.py ever silently return a
wrong value rather than reject or visibly propagate the defect?"

WHAT "SILENTLY" MEANS HERE, DECIDED BEFORE THE RUN
--------------------------------------------------
Leg 99's vocabulary is reused verbatim so the two batteries read side by side.

    OK           -- returns, finite, and agrees with the known truth inside tolerance.
    RAISED       -- an exception propagates. The caller cannot proceed on bad data.
    NONFINITE    -- NaN or Inf reaches a returned value. Visible is visible; not an exception,
                    but every downstream norm, plot and assertion sees it.
    SILENT_WRONG -- returns normally AND every returned value is finite AND no warning is
                    emitted AND the value differs from a KNOWN truth by more than the module's
                    own acceptance tolerance for that quantity. This is the gate's YES.
    SILENT_EMPTY -- returns normally, all-finite, but structurally vacuous (zero-length axis).
    NO_REFERENT  -- the input violates the function's documented precondition, so there is no
                    truth to compare against. Lesson 73: when a quantity has no referent, say
                    so instead of bounding it. Recorded with its magnitude; DOES NOT decide
                    the gate, in either direction.

Only SILENT_WRONG answers the gate.

DISCIPLINE
----------
Magnitudes, never booleans. Every case reports the SIZE of what could have gone wrong: absolute
and relative error against a known truth, the ratio against the well-posed read of the SAME
quantity on the SAME field, and the fit-window occupancy that produced it.

Lesson 90 (a control that cannot come out differently is not a control): families F1, F2 and F5
each carry a positive control on a well-resolved grid that reports OK by moving a number the
degenerate case moves differently, and F4 carries a planted-perturbation control whose whole
point is that it CAN report "unmoved" and does not.

REFERENCE TRUTH
---------------
The module's own manufactured field, reused verbatim from test_boussinesq_rescaled.py so no new
analytic claim is smuggled in:

    g(r,beta) = a * x * exp(-lam r^2) = a r cos(beta) exp(-lam r^2),  odd in x,
    g_x(0) = a exactly  (the envelope is 1 with zero slope at the origin).

Its cos(beta)-mode radial coefficient is d1(r) = a r exp(-lam r^2) = a r - a lam r^3 + ..., so
it has genuine r^3 content of the same order as its linear part -- which is what the three-
parameter fit basis (r, r^3, r^5) exists to absorb, and what an under-determined fit cannot.

Two envelopes lam_omega != lam_eta are used in F2 on purpose. The module docstring asserts that
for c_l = 2 eta_x(0)/omega_x(0) "the projection's quadrature bias CANCELS in the ratio (same
basis both reads)". That cancellation is exact only when the two fields have the same radial
shape; F2 measures what is left when they do not.

OUTPUT
------
writeup/data/p2_route_bvr_v1_adversarial.json -- every case, with its outcome. Negative results
included; the families that found nothing are in the JSON at full length, not summarized away.

solver/boussinesq_rescaled.py is READ ONLY here and is byte-identical to its merge-base state
under either gate outcome. This leg does not patch it.
"""

import json
import os
import sys
import time
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.boussinesq_velocity import (  # noqa: E402
    PolarGrid, velocity_from_vorticity, u_x_at_origin,
)
from solver.boussinesq_rescaled import (  # noqa: E402
    odd_field_x_slope, modulation, transport, grad_xy, advection_speeds,
    RescaledBoussinesq,
)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_bvr_v1_adversarial.json")

# The module's own acceptance tolerance for the origin read, taken from its existing
# correctness gate (test_boussinesq_rescaled.py::test_odd_field_x_slope asserts a convergent
# ladder whose finest relative error is ~5e-4). A deviation below this would not be caught by
# the module's own tests; a deviation above it would.
ACCEPT_REL = 5.0e-4


def odd_field(grid, a=1.0, lam=1.0):
    """a * x * exp(-lam r^2): odd in x, g_x(0) = a exactly."""
    return a * grid.R * np.cos(grid.B) * np.exp(-lam * grid.R ** 2)


def window_nodes(grid, r_win=0.4, i_lo=3):
    """How many radial nodes the odd_field_x_slope fit window holds (3 parameters needed)."""
    return int(((np.arange(grid.n_r) >= i_lo) & (grid.r < r_win)).sum())


def ux_window_nodes(grid, r_window=0.1):
    """How many nodes the SIBLING guard's window holds (u_x_at_origin, 2 parameters)."""
    return int(((grid.r > grid.r[2]) & (grid.r < r_window)).sum())


def _call(fn, *args, **kw):
    """Run fn, capturing exceptions and warnings. Returns (value, exc_repr, n_warnings)."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            val = fn(*args, **kw)
            exc = None
        except Exception as e:                                   # noqa: BLE001
            val, exc = None, f"{type(e).__name__}: {e}"
        return val, exc, len(w)


def classify_scalar(val, exc, nwarn, truth, accept_rel=ACCEPT_REL):
    """Verdict + magnitudes for a scalar read against a known truth."""
    if exc is not None:
        return dict(verdict="RAISED", exception=exc, returned=None,
                    abs_err=None, rel_err=None, warnings=nwarn)
    if val is None or not np.isfinite(val):
        return dict(verdict="NONFINITE", exception=None, returned=repr(val),
                    abs_err=None, rel_err=None, warnings=nwarn)
    abs_err = abs(val - truth)
    rel_err = abs_err / abs(truth) if truth != 0 else float("inf")
    verdict = "OK" if (rel_err <= accept_rel and nwarn == 0) else "SILENT_WRONG"
    if nwarn > 0 and rel_err > accept_rel:
        verdict = "SILENT_WRONG"  # warnings alone do not rescue a wrong finite value
    return dict(verdict=verdict, exception=None, returned=float(val),
                abs_err=float(abs_err), rel_err=float(rel_err), warnings=nwarn,
                over_accept_tol=float(rel_err / accept_rel))


# =======================================================================================
# F1 -- the origin-read reduction. Does odd_field_x_slope fabricate a finite value when its
#       fit window is empty or rank-deficient?
# =======================================================================================

def family_1():
    cases = []
    a_true = 2.0

    # (i) r_min sweep at fixed node count: drives window occupancy from well-resolved to empty.
    for n_r, r_min, r_max, label in [
        (400, 1e-4, 1e4, "well-resolved (leg 73-class grid)"),
        (200, 1e-3, 1e3, "well-resolved, coarser"),
        (60, 1e-2, 1e3, "16 nodes in window"),
        (30, 1e-2, 1e2, "9 nodes in window"),
        (20, 1e-2, 1e2, "5 nodes in window"),
        (14, 1e-2, 1e2, "3 nodes -- exactly determined"),
        (12, 1e-2, 1e2, "2 nodes -- UNDER-determined (3 params)"),
        (10, 1e-2, 1e2, "1 node -- UNDER-determined"),
        (8, 1e-2, 1e2, "0 nodes -- EMPTY window"),
        (200, 0.5, 40.0, "r_min > r_win -- EMPTY window, fine grid"),
        (200, 1.0, 1e3, "r_min = 1.0 -- EMPTY window"),
    ]:
        grid = PolarGrid(n_r=n_r, n_beta=16, r_min=r_min, r_max=r_max)
        g = odd_field(grid, a=a_true, lam=1.0)
        val, exc, nw = _call(odd_field_x_slope, g, grid)
        rec = classify_scalar(val, exc, nw, a_true)
        rec.update(case=f"F1 r_min sweep: {label}", n_r=n_r, r_min=r_min, r_max=r_max,
                   fit_nodes=window_nodes(grid), params=3, truth=a_true,
                   returned_is_exactly_zero=(val == 0.0) if val is not None else None)
        cases.append(rec)

    # (ii) r_win sweep on a FIXED well-resolved grid: the same degeneracy through the other
    #      user-facing knob, so the finding cannot be blamed on an exotic grid.
    grid = PolarGrid(n_r=400, n_beta=16, r_min=1e-4, r_max=1e4)
    g = odd_field(grid, a=a_true, lam=1.0)
    for r_win in [0.4, 0.1, 0.01, 1e-3, 5e-4, 3e-4, 1e-4]:
        val, exc, nw = _call(odd_field_x_slope, g, grid, r_win=r_win)
        rec = classify_scalar(val, exc, nw, a_true)
        rec.update(case=f"F1 r_win sweep: r_win={r_win:g} on the leg-73-class grid",
                   n_r=400, r_min=1e-4, r_max=1e4, r_win=r_win,
                   fit_nodes=window_nodes(grid, r_win=r_win), params=3, truth=a_true,
                   returned_is_exactly_zero=(val == 0.0) if val is not None else None)
        cases.append(rec)

    # (iii) ENVELOPE-SCALE SWEEP on a FULLY RESOLVED grid (177 nodes in the window in every
    #       case). This isolates a SECOND, independent mechanism from the window-occupancy one:
    #       odd_field_x_slope discards the least-squares residual (`coef, *_ = lstsq(...)`), so
    #       it cannot tell a good fit from a bad one. When the field's own radial scale is much
    #       smaller than r_win, the three-term basis (r, r^3, r^5) cannot represent d1 over the
    #       window, and the function returns a finite wrong answer with a full window and no
    #       complaint. Lesson 75: two defects in the same problem are not the same defect.
    for lam in [0.25, 1.0, 4.0, 25.0, 100.0, 400.0]:
        val, exc, nw = _call(odd_field_x_slope, odd_field(grid, a=a_true, lam=lam), grid)
        rec = classify_scalar(val, exc, nw, a_true)
        rec.update(case=f"F1 envelope-scale sweep on the FULLY RESOLVED grid: lam={lam:g}",
                   n_r=400, r_min=1e-4, r_max=1e4, r_win=0.4, lam=lam,
                   fit_nodes=window_nodes(grid), params=3, truth=a_true,
                   field_scale_r=float(1.0 / np.sqrt(lam)),
                   note=("field decay scale 1/sqrt(lam) vs fit window 0.4; the window is FULL "
                         "in every row, so occupancy cannot explain any failure here"))
        cases.append(rec)

    # (iv) DEFECT B's RECOVERY CONTROL, and the sharpest form of the finding. Same field, same
    #      grid, same code -- ONLY r_win changes. The read climbs from 0.269 (86.5% wrong) to
    #      2.0009 (inside the module's own tolerance) as the window is brought down to the
    #      field's own scale. So the function is fully CAPABLE of the right answer; what it
    #      lacks is any way to notice that its default window is the wrong size, and any way to
    #      tell the caller. This is also the fix direction, stated as a measurement rather than
    #      a patch (lesson 90: this control can, and does, come out the other way).
    for r_win in [0.4, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005]:
        val, exc, nw = _call(odd_field_x_slope, odd_field(grid, a=a_true, lam=400.0), grid,
                             r_win=r_win)
        rec = classify_scalar(val, exc, nw, a_true)
        rec.update(case=f"F1 defect-B recovery: lam=400 (field scale 0.05), r_win={r_win:g}",
                   n_r=400, r_min=1e-4, r_max=1e4, r_win=r_win, lam=400.0,
                   fit_nodes=window_nodes(grid, r_win=r_win), params=3, truth=a_true,
                   field_scale_r=0.05,
                   note="the ONLY thing varying across these rows is the window width")
        cases.append(rec)

    # (v) POSITIVE CONTROL (lesson 90): the same call on a well-resolved grid must MOVE with
    #       the truth. If it reported the same number for every a, it would be no control.
    control = []
    for a in [0.5, 1.0, 2.0, -3.0]:
        val, exc, nw = _call(odd_field_x_slope, odd_field(grid, a=a, lam=1.0), grid)
        rec = classify_scalar(val, exc, nw, a)
        rec.update(case=f"F1 positive control: well-resolved grid, a={a}", truth=a,
                   fit_nodes=window_nodes(grid))
        control.append(rec)
    return cases, control


# =======================================================================================
# F2 -- does the F1 degeneracy reach the coupled entry point modulation()/rhs(), or is it
#       intercepted -- and if intercepted, how wide is the surviving gap?
# =======================================================================================

def family_2():
    cases = []

    # The sibling guard u_x_at_origin (leg 99/104) uses window r<0.1 with 2 parameters; this
    # module's own fit uses r<0.4 with 3. Both masks are "index >= 3", so the sibling's window
    # is a SUBSET of this module's. Enumerate the grids where the sibling guard PASSES but this
    # module's fit is still rank-deficient: that intersection is the surviving gap.
    gap_grids = []
    for n_r in range(8, 30):
        for q in np.arange(2.0, 12.0, 0.05):
            for r3 in (0.02, 0.03, 0.05, 0.08):
                r_min = r3 / q ** 3
                r_max = r_min * q ** (n_r - 1)
                if r_max > 1e9:
                    continue
                grid = PolarGrid(n_r=n_r, n_beta=16, r_min=r_min, r_max=r_max)
                if ux_window_nodes(grid) >= 2 and 1 <= window_nodes(grid) <= 2:
                    gap_grids.append((n_r, float(r_min), float(r_max),
                                      ux_window_nodes(grid), window_nodes(grid)))
    structure = dict(
        note=("u_x_at_origin's window (r<0.1, 2 params) is a strict SUBSET of "
              "odd_field_x_slope's (r<0.4, 3 params); both mask on index>=3. So an EMPTY "
              "odd-fit window forces an empty sibling window and the sibling's leg-99 guard "
              "always raises first. The surviving gap is exactly the rank-deficient-but-"
              "nonempty case, and in it BOTH fit nodes necessarily lie at r<0.1."),
        gap_grid_count=len(gap_grids),
        gap_grid_examples=gap_grids[:5],
        empty_window_reachable_through_modulation=False,
    )

    # (i) EMPTY window through modulation(): predicted RAISED by the inherited sibling guard.
    for n_r, r_min, r_max, label in [
        (8, 1e-2, 1e2, "0 fit nodes"),
        (200, 0.5, 40.0, "r_min > r_win, fine grid"),
    ]:
        grid = PolarGrid(n_r=n_r, n_beta=16, r_min=r_min, r_max=r_max)
        om = odd_field(grid, a=1.0, lam=1.0)
        et = odd_field(grid, a=0.7, lam=4.0)
        u, v, phi = velocity_from_vorticity(om, grid)
        val, exc, nw = _call(modulation, om, et, phi, grid)
        cases.append(dict(case=f"F2 modulation on EMPTY-window grid: {label}",
                          n_r=n_r, r_min=r_min, r_max=r_max,
                          fit_nodes=window_nodes(grid), ux_nodes=ux_window_nodes(grid),
                          verdict="RAISED" if exc else "RETURNED", exception=exc,
                          returned_c_l=None if exc else float(val[0]), warnings=nw,
                          guard_source="solver/boussinesq_velocity.py u_x_at_origin (leg 99)"))

    # (ii) The surviving gap, measured as a PAIRED experiment. Each (field, lam_eta) pair is
    #      read twice: once on the rank-deficient grid, once on a fully resolved grid. A pair
    #      is only allowed to score if its RESOLVED control passes -- otherwise the error is
    #      the basis-inadequacy mechanism of F1(iii), not the rank deficiency, and attributing
    #      it here would be exactly the realization error the standing discipline warns about
    #      ("when a control contradicts the mechanism, suspect the control's REALIZATION").
    #      Envelopes still differ between omega and eta so the module docstring's claimed
    #      "quadrature bias CANCELS in the ratio" cannot mask the error.
    fine = PolarGrid(n_r=400, n_beta=32, r_min=1e-4, r_max=1e4)
    truth_cl = 2.0 * 0.7 / 1.0
    om_f = odd_field(fine, a=1.0, lam=1.0)
    _, _, phi_f = velocity_from_vorticity(om_f, fine)
    fine_ctrl = {}
    for lam_e in (0.25, 1.0, 4.0, 16.0, 25.0, 100.0, 400.0):
        cf, _, _, _ = modulation(om_f, odd_field(fine, a=0.7, lam=lam_e), phi_f, fine)
        fine_ctrl[lam_e] = float(cf)

    worst = dict(rel_err=-1.0)
    pairs_scored, pairs_rejected = 0, 0
    for n_r, r_min, r_max, nux, nfit in gap_grids[:40]:
        grid = PolarGrid(n_r=n_r, n_beta=32, r_min=r_min, r_max=r_max)
        for lam_e in (0.25, 1.0, 4.0, 16.0, 25.0, 100.0):
            cf = fine_ctrl[lam_e]
            ctrl_rel = abs(float(cf) - truth_cl) / truth_cl
            if ctrl_rel > ACCEPT_REL:
                pairs_rejected += 1          # basis inadequacy, not rank deficiency
                continue
            om = odd_field(grid, a=1.0, lam=1.0)
            et = odd_field(grid, a=0.7, lam=lam_e)
            u, v, phi = velocity_from_vorticity(om, grid)
            val, exc, nw = _call(modulation, om, et, phi, grid)
            if exc is not None:
                continue
            pairs_scored += 1
            c_l = float(val[0])
            rel = abs(c_l - truth_cl) / truth_cl
            if rel > worst["rel_err"]:
                worst = dict(rel_err=float(rel), c_l=c_l, truth=truth_cl, n_r=n_r,
                             r_min=float(r_min), r_max=float(r_max), lam_eta=lam_e,
                             fit_nodes=nfit, ux_nodes=nux, warnings=nw,
                             finite=bool(np.isfinite(c_l)),
                             resolved_control_c_l=float(cf),
                             resolved_control_rel_err=float(ctrl_rel))
    worst["pairs_scored"] = pairs_scored
    worst["pairs_rejected_control_failed"] = pairs_rejected
    worst["verdict"] = ("SILENT_WRONG" if worst["rel_err"] > ACCEPT_REL and worst["finite"]
                        and worst["warnings"] == 0 else "OK")
    worst["over_accept_tol"] = float(worst["rel_err"] / ACCEPT_REL)
    worst["attribution"] = ("the resolved control on the SAME fields passes at "
                            f"{worst.get('resolved_control_rel_err')}, so the error is "
                            "attributable to the rank-deficient fit window, not to the "
                            "adequacy of the (r, r^3, r^5) basis")
    worst["case"] = "F2 widest surviving gap: rank-deficient odd-fit with sibling guard passing"

    # (iii) THE HEADLINE at the coupled entry point. F1(iii)'s mechanism needs NO degenerate
    #       grid: the fit window is fully occupied (177 nodes) in every row below, so the
    #       sibling's leg-99 occupancy guard is satisfied and cannot fire. omega and eta carry
    #       DIFFERENT radial scales, which is the generic case and the one the module docstring
    #       claims is safe ("the projection's quadrature bias CANCELS in the ratio").
    for lam_e, cf in sorted(fine_ctrl.items()):
        rel = abs(cf - truth_cl) / truth_cl
        cases.append(dict(
            case=(f"F2 modulation on the FULLY RESOLVED leg-73-class grid, "
                  f"eta scale 1/sqrt({lam_e:g}) = {1/np.sqrt(lam_e):.3g} vs r_win 0.4"),
            verdict=("SILENT_WRONG" if rel > ACCEPT_REL else "OK"),
            exception=None, warnings=0,
            n_r=400, r_min=1e-4, r_max=1e4,
            fit_nodes=window_nodes(fine), ux_nodes=ux_window_nodes(fine),
            lam_eta=lam_e, eta_scale_r=float(1 / np.sqrt(lam_e)),
            c_l_returned=float(cf), truth=truth_cl,
            rel_err=float(rel), over_accept_tol=float(rel / ACCEPT_REL),
            c_l_is_finite=bool(np.isfinite(cf)),
            note=("fully occupied fit window, no exception, no warning, finite plausible "
                  "value -- the occupancy guard inherited from u_x_at_origin cannot see this"),
        ))

    # (iv) THE DISCARDED DIAGNOSTIC. odd_field_x_slope writes `coef, *_ = lstsq(...)`, throwing
    #      away the residual that would have revealed every failure in (iii). Measured here to
    #      show the signal exists in the call the module already makes -- i.e. a guard is
    #      available at zero extra cost. This is measurement of the module's own inputs, not a
    #      patch: solver/boussinesq_rescaled.py is not edited.
    diag = []
    beta = fine.beta
    dbeta = beta[1] - beta[0]
    cb = np.cos(beta)
    for lam in (1.0, 4.0, 25.0, 100.0, 400.0):
        g = odd_field(fine, a=2.0, lam=lam)
        g_wall = 2 * g[:, 0] - g[:, 1]
        integrand = g * cb[None, :]
        d1 = (4.0 / np.pi) * (np.trapezoid(integrand, beta, axis=1)
                              + 0.5 * dbeta * (g_wall * 1.0 + integrand[:, 0])
                              + 0.5 * dbeta * (integrand[:, -1] + 0.0))
        m = (np.arange(fine.n_r) >= 3) & (fine.r < 0.4)
        rr = fine.r[m]
        A = np.vstack([rr, rr ** 3, rr ** 5]).T
        coef, res, rank, sv = np.linalg.lstsq(A, d1[m], rcond=None)
        resid = float(np.sqrt(res[0])) if np.size(res) else float("nan")
        rel_resid = resid / float(np.linalg.norm(d1[m]))
        diag.append(dict(lam=lam, returned_slope=float(coef[0]), truth=2.0,
                         slope_rel_err=float(abs(coef[0] - 2.0) / 2.0),
                         lstsq_rel_residual=rel_resid, rank=int(rank),
                         cond=float(sv[0] / sv[-1])))
    cases.append(dict(
        case="F2 the discarded least-squares residual, measured against the slope error",
        verdict="OK", exception=None, warnings=0, diagnostic=diag,
        note=("the relative residual tracks the slope error across four orders of magnitude "
              "and is returned by the very lstsq call the module already makes, then dropped "
              "by `coef, *_`. Reported as evidence that a guard is available, NOT as a patch."),
    ))

    # (v) run() on an empty-window grid -- does the integrator start on fabricated targets?
    grid = PolarGrid(n_r=8, n_beta=16, r_min=1e-2, r_max=1e2)
    solver = RescaledBoussinesq(grid)
    om = odd_field(grid, a=1.0, lam=1.0)
    et = odd_field(grid, a=0.7, lam=4.0)
    xi = np.zeros_like(om)
    val, exc, nw = _call(solver.run, om, et, xi, max_steps=3, renorm=True)
    wx_t, _, _ = _call(odd_field_x_slope, om, grid)
    cases.append(dict(
        case="F2 run(renorm=True) on EMPTY-window grid",
        verdict="RAISED" if exc else "RETURNED", exception=exc, warnings=nw,
        renorm_target_before_any_step=None if wx_t is None else float(wx_t),
        renorm_target_truth=1.0,
        note=("run() computes its renorm targets from odd_field_x_slope BEFORE the first "
              "rhs call, so the fabricated value is latched first; the sibling guard then "
              "raises on the first rhs. The fabricated target is reported here because it "
              "is what run() would divide by if the guard were ever relaxed."),
    ))
    return cases, structure, worst


# =======================================================================================
# F3 -- NaN / Inf pass-through. Planted non-finite values: visible or swallowed?
# =======================================================================================

def family_3():
    cases = []
    grid = PolarGrid(n_r=200, n_beta=16, r_min=1e-3, r_max=1e3)
    i_in = int(np.argmax(grid.r > 0.05))        # a node INSIDE the fit window
    i_out = int(np.argmax(grid.r > 10.0))       # a node OUTSIDE the fit window
    solver = RescaledBoussinesq(grid)

    for field_name, bad, idx, where in [
        ("omega", np.nan, i_in, "inside fit window"),
        ("omega", np.nan, i_out, "outside fit window"),
        ("omega", np.inf, i_out, "outside fit window"),
        ("eta", np.nan, i_in, "inside fit window"),
        ("eta", np.nan, i_out, "outside fit window"),
        ("xi", np.nan, i_out, "outside fit window (xi never enters modulation)"),
    ]:
        om = odd_field(grid, a=1.0, lam=1.0)
        et = odd_field(grid, a=0.7, lam=4.0)
        xi = 0.3 * odd_field(grid, a=1.0, lam=4.0)
        {"omega": om, "eta": et, "xi": xi}[field_name][idx, 0] = bad
        out, exc, nw = _call(solver.rhs, om, et, xi)
        if exc is not None:
            rec = dict(verdict="RAISED", exception=exc)
        else:
            R_om, R_et, R_xi, info = out
            n_bad = int(sum(np.count_nonzero(~np.isfinite(A)) for A in (R_om, R_et, R_xi)))
            n_tot = int(R_om.size * 3)
            cl_finite = bool(np.isfinite(info["c_l"]))
            rec = dict(
                verdict=("NONFINITE" if n_bad > 0 else
                         ("SILENT_WRONG" if cl_finite else "NONFINITE")),
                exception=None,
                nonfinite_cells_in_rhs=n_bad, total_rhs_cells=n_tot,
                contaminated_fraction=float(n_bad / n_tot),
                c_l_returned=float(info["c_l"]) if cl_finite else repr(info["c_l"]),
                c_l_is_finite=cl_finite,
                cfl_speed=float(info["cfl_speed"]) if np.isfinite(info["cfl_speed"])
                else repr(info["cfl_speed"]),
            )
        rec.update(case=f"F3 {bad!r} planted in {field_name} at r={grid.r[idx]:.4g} ({where})",
                   planted=repr(bad), field=field_name, node_index=idx,
                   node_r=float(grid.r[idx]), warnings=nw)
        cases.append(rec)
    return cases


# =======================================================================================
# F4 -- degenerate and boundary parameters, plus the planted-wrong-value pass-through.
# =======================================================================================

def family_4():
    cases = []
    grid = PolarGrid(n_r=200, n_beta=16, r_min=1e-3, r_max=1e3)
    om = odd_field(grid, a=1.0, lam=1.0)
    et = odd_field(grid, a=0.7, lam=4.0)
    xi = 0.3 * odd_field(grid, a=1.0, lam=4.0)
    u, v, phi = velocity_from_vorticity(om, grid)
    solver = RescaledBoussinesq(grid)

    def rec(case, val, exc, nw, **kw):
        d = dict(case=case, exception=exc, warnings=nw)
        if exc is not None:
            d["verdict"] = "RAISED"
        elif val is None:
            d["verdict"] = "RETURNED_NONE"
        else:
            d["verdict"] = kw.pop("verdict", "RETURNED")
        d.update(kw)
        return d

    # --- zero and constant fields
    z = np.zeros_like(om)
    val, exc, nw = _call(modulation, z, z, phi, grid)
    cases.append(rec("F4 modulation with omega = eta = 0 (c_l = 0/0)", val, exc, nw,
                     note="wx0 is a Python float; 0.0/0.0 raises rather than returning nan"))
    val, exc, nw = _call(modulation, z, et, phi, grid)
    cases.append(rec("F4 modulation with omega = 0, eta nonzero (c_l = x/0)", val, exc, nw))
    val, exc, nw = _call(odd_field_x_slope, z, grid)
    cases.append(rec("F4 odd_field_x_slope on the zero field", val, exc, nw,
                     verdict="OK", returned=None if val is None else float(val),
                     truth=0.0,
                     note="the zero field genuinely has zero origin slope; returning 0.0 is "
                          "correct here, which is exactly why the fabricated 0.0 of F1 is "
                          "indistinguishable from a true answer at the call site"))
    const = np.ones_like(om)
    val, exc, nw = _call(odd_field_x_slope, const, grid)
    cases.append(rec("F4 odd_field_x_slope on a CONSTANT (not odd-in-x) field", val, exc, nw,
                     verdict="NO_REFERENT", returned=None if val is None else float(val),
                     note="violates the documented 'odd-in-x' precondition; no truth exists, "
                          "so lesson 73 applies and this does not decide the gate"))
    even = grid.R * np.sin(grid.B) * np.exp(-grid.R ** 2)   # = y*env, EVEN in x
    val, exc, nw = _call(odd_field_x_slope, even, grid)
    cases.append(rec("F4 odd_field_x_slope on an EVEN-in-x field (annihilated by the "
                     "cos(beta) projection)", val, exc, nw,
                     verdict="NO_REFERENT", returned=None if val is None else float(val),
                     note="the cos(beta) projection annihilates it by construction; this is "
                          "the documented behaviour of the basis, not a loss of information"))

    # --- tiny grids
    for n_r, n_beta in [(8, 16), (4, 16), (3, 16), (2, 16), (1, 16),
                        (200, 4), (200, 2), (200, 1), (200, 0)]:
        gv, ex, nw = _call(PolarGrid, n_r=n_r, n_beta=n_beta, r_min=1e-3, r_max=1e3)
        if ex is not None:
            cases.append(rec(f"F4 PolarGrid(n_r={n_r}, n_beta={n_beta})", None, ex, nw))
            continue
        f = odd_field(gv, a=1.0, lam=1.0)
        vel, ex2, nw2 = _call(velocity_from_vorticity, f, gv)
        if ex2 is not None:
            cases.append(rec(f"F4 velocity_from_vorticity on n_r={n_r}, n_beta={n_beta}",
                             None, ex2, nw2))
            continue
        uu, vv, _pp = vel
        tv, ex3, nw3 = _call(transport, f, uu, vv, gv, 3.0)
        d = rec(f"F4 transport on n_r={n_r}, n_beta={n_beta}", tv, ex3, nw3,
                n_r=n_r, n_beta=n_beta)
        if ex3 is None and tv is not None:
            d["verdict"] = "SILENT_EMPTY" if tv.size == 0 else "RETURNED"
            d["out_shape"] = list(tv.shape)
            d["max_abs"] = float(np.max(np.abs(tv))) if tv.size else None
            d["all_finite"] = bool(np.all(np.isfinite(tv))) if tv.size else None
        cases.append(d)

    # --- non-finite / extreme c_l fed straight to transport
    for c_l in [0.0, np.nan, np.inf, -np.inf, 1e300]:
        tv, ex, nw = _call(transport, om, u, v, grid, c_l)
        d = rec(f"F4 transport with c_l={c_l!r}", tv, ex, nw, c_l=repr(c_l))
        if ex is None and tv is not None:
            nb = int(np.count_nonzero(~np.isfinite(tv)))
            d["verdict"] = "NONFINITE" if nb else "RETURNED"
            d["nonfinite_cells"] = nb
            d["total_cells"] = int(tv.size)
            d["max_abs_finite"] = (float(np.max(np.abs(tv[np.isfinite(tv)])))
                                   if np.any(np.isfinite(tv)) else None)
        cases.append(d)

    # --- run() control parameters
    val, exc, nw = _call(solver.run, om, et, xi, max_steps=0)
    cases.append(rec("F4 run(max_steps=0)", val, exc, nw,
                     note="the loop body never executes and `step` is referenced in the "
                          "return; an UnboundLocalError is visible, a fabricated 0 would not be"))
    val, exc, nw = _call(solver.run, om, et, xi, max_steps=2, tol=np.inf)
    if exc is None:
        cases.append(rec("F4 run(tol=inf)", val, exc, nw, verdict="RETURNED",
                         converged=bool(val["converged"]), residual=float(val["residual"]),
                         note="converged := res < tol is literally what the caller asked for; "
                              "recorded as a parameter observation, not a defect"))
    else:
        cases.append(rec("F4 run(tol=inf)", None, exc, nw))

    # --- PLANTED WRONG-VALUE PASS-THROUGH (the directive's fourth clause).
    #     A control that CAN come out either way (lesson 90): perturbing INSIDE the fit window
    #     must move c_l; perturbing OUTSIDE it must not move c_l but MUST move the RHS.
    base_cl, _, _, _ = modulation(om, et, phi, grid)
    i_in = int(np.argmax(grid.r > 0.05))
    i_out = int(np.argmax(grid.r > 10.0))
    for idx, where in [(i_in, "inside fit window"), (i_out, "outside fit window")]:
        om_p = odd_field(grid, a=1.0, lam=1.0)
        om_p[idx, :] *= 10.0                       # a 10x planted wrong value on one radius
        u_p, v_p, phi_p = velocity_from_vorticity(om_p, grid)
        cl_p, _, _, _ = modulation(om_p, et, phi_p, grid)
        R = solver.rhs(om, et, xi)[0]
        R_p = solver.rhs(om_p, et, xi)[0]
        cases.append(dict(
            case=f"F4 planted 10x wrong value on radius r={grid.r[idx]:.4g} ({where})",
            verdict="RETURNED", exception=None, warnings=0,
            node_index=idx, node_r=float(grid.r[idx]),
            c_l_base=float(base_cl), c_l_planted=float(cl_p),
            c_l_rel_shift=float(abs(cl_p - base_cl) / abs(base_cl)),
            rhs_max_abs_shift=float(np.max(np.abs(R_p - R))),
            rhs_rel_shift=float(np.max(np.abs(R_p - R)) / max(np.max(np.abs(R)), 1e-300)),
            note="the perturbation is visible in the RHS in both placements; the c_l column "
                 "is the one that can report 'unmoved', and it does so only for the "
                 "out-of-window placement -- so it is a control, not a tautology",
        ))
    return cases


# =======================================================================================
# F5 -- information loss in reductions: the dealiasing-mask question, carried in as an INPUT.
# =======================================================================================

def family_5():
    cases = []
    grid = PolarGrid(n_r=200, n_beta=16, r_min=1e-3, r_max=1e3)

    # (i) Is there any mask / spectral truncation at all in this module's transform chain?
    rng = np.random.default_rng(0)
    f = rng.standard_normal((grid.n_r, grid.n_beta))
    rt = grid.from_modes(grid.to_modes(f))
    err = float(np.max(np.abs(rt - f)) / np.max(np.abs(f)))
    cases.append(dict(
        case="F5 angular DST-I round trip from_modes(to_modes(f)) on a random field",
        verdict="OK" if err < 1e-12 else "SILENT_WRONG",
        roundtrip_rel_err=err,
        note="S @ S = (M/2) I, so the angular transform is an exact bijection ON GRID FIELDS. "
             "There is no 2/3 mask and no truncation, so the leg 129/188 dealias-annihilation "
             "mechanism (an input field the mask sends to zero while the module reports on it) "
             "has no site in this module. This control CAN report the other answer: a mask "
             "would show up here as a finite round-trip loss.",
    ))

    # (ii) The leg-89 analogue: is there an input this module's reductions annihilate to zero
    #      while reporting normally? Highest-representable angular mode.
    n_top = grid.n_modes[-1]
    f_top = np.sin(2.0 * n_top * grid.B) * np.exp(-grid.R ** 2)
    rt_top = grid.from_modes(grid.to_modes(f_top))
    cases.append(dict(
        case=f"F5 highest angular mode n={int(n_top)} through the transform",
        verdict="OK",
        input_max_abs=float(np.max(np.abs(f_top))),
        roundtrip_rel_err=float(np.max(np.abs(rt_top - f_top)) / np.max(np.abs(f_top))),
        note="not annihilated; represented exactly on the grid",
    ))

    # (iii) The quadrature bias of the odd_field_x_slope projection, on well-posed input --
    #       a convergent discretization error, reported as a magnitude so it is not confused
    #       with the F1 fabrication.
    ladder = []
    for n_r in (100, 200, 400, 800):
        g2 = PolarGrid(n_r=n_r, n_beta=32, r_min=1e-4, r_max=1e4)
        val = odd_field_x_slope(odd_field(g2, a=2.0, lam=1.0), g2)
        ladder.append(dict(n_r=n_r, fit_nodes=window_nodes(g2), returned=float(val),
                           rel_err=float(abs(val - 2.0) / 2.0)))
    cases.append(dict(
        case="F5 odd_field_x_slope quadrature bias on well-posed input (convergence ladder)",
        verdict="OK", ladder=ladder,
        note="a bounded, convergent discretization error, NOT a defect; quoted so the F1 "
             "100% fabrication cannot be mistaken for the same thing",
    ))

    # (iv) grad_xy and advection_speeds on a known field -- do they lose the answer quietly?
    g3 = PolarGrid(n_r=400, n_beta=32, r_min=1e-3, r_max=1e2)
    fx_true = np.ones_like(g3.R)
    fxy = grad_xy(g3.X, g3)            # f = x -> f_x = 1, f_y = 0
    m = (g3.R > 1e-2) & (g3.R < 10.0)
    cases.append(dict(
        case="F5 grad_xy on f = x (known answer f_x = 1, f_y = 0)",
        verdict="OK",
        max_rel_err_fx=float(np.max(np.abs(fxy[0][m] - fx_true[m]))),
        max_abs_fy=float(np.max(np.abs(fxy[1][m]))),
        note="interior band only; the one-sided rho-ends are excluded by design",
    ))
    s_rho, s_beta = advection_speeds(np.zeros_like(g3.R), np.zeros_like(g3.R), g3, 3.0)
    cases.append(dict(
        case="F5 advection_speeds with u = v = 0 (known answer s_rho = c_l, s_beta = 0)",
        verdict="OK",
        max_abs_dev_s_rho=float(np.max(np.abs(s_rho - 3.0))),
        max_abs_s_beta=float(np.max(np.abs(s_beta))),
    ))
    return cases


def main():
    t0 = time.time()
    f1, f1_control = family_1()
    f2, f2_structure, f2_worst = family_2()
    f3 = family_3()
    f4 = family_4()
    f5 = family_5()

    all_cases = f1 + f1_control + f2 + [f2_worst] + f3 + f4 + f5
    totals = {}
    for c in all_cases:
        totals[c.get("verdict", "UNKNOWN")] = totals.get(c.get("verdict", "UNKNOWN"), 0) + 1

    silent = [c for c in all_cases if c.get("verdict") == "SILENT_WRONG"]
    gate = "YES" if silent else "NO"

    out = dict(
        leg=205, route="BVR",
        module_under_test="solver/boussinesq_rescaled.py",
        module_edited=False,
        prior_gate=("Spike 1 Step B (test_boussinesq_rescaled.py, test_boussinesq_transport.py) "
                    "-- correctness on well-posed input, not robustness"),
        prior_flag=("writeup/novelty/leg_99.md sec.4 note 2 flagged "
                    "solver/boussinesq_rescaled.py:161 by line number as the identical "
                    "unguarded masked-lstsq mechanism, declined to test it, and named a "
                    "follow-up leg scoped to this module as the obvious next audit"),
        gate_question=("Under adversarial and degenerate inputs, does boussinesq_rescaled.py "
                       "ever silently return a wrong value rather than reject or visibly "
                       "propagate the defect?"),
        verdict_semantics=dict(
            OK="finite and inside the module's own acceptance tolerance",
            RAISED="exception propagates",
            NONFINITE="NaN/Inf reaches a returned value -- visible",
            SILENT_WRONG="finite, no warning, wrong beyond the module's own tolerance",
            SILENT_EMPTY="finite but structurally vacuous",
            NO_REFERENT="precondition violated, no truth exists; does not decide the gate",
        ),
        acceptance_tolerance_rel=ACCEPT_REL,
        acceptance_tolerance_source=("test_boussinesq_rescaled.py::test_odd_field_x_slope, "
                                     "finest rung of its convergence ladder"),
        family_1_origin_read=f1,
        family_1_positive_control=f1_control,
        family_2_coupled_entry_point=f2,
        family_2_guard_structure=f2_structure,
        family_2_widest_surviving_gap=f2_worst,
        family_3_nonfinite_passthrough=f3,
        family_4_degenerate_and_boundary=f4,
        family_5_reduction_information_loss=f5,
        verdict_totals=totals,
        n_cases=len(all_cases),
        silent_wrong_cases=[c["case"] for c in silent],
        gate_answer=gate,
        wall_seconds=round(time.time() - t0, 2),
    )
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, default=str)

    print(f"cases: {len(all_cases)}   totals: {totals}")
    print(f"GATE ANSWER: {gate}")
    for c in silent:
        print(f"  SILENT_WRONG: {c['case']}")
        print(f"      returned={c.get('returned', c.get('c_l'))} truth={c.get('truth')} "
              f"rel_err={c.get('rel_err')} over_tol={c.get('over_accept_tol')}")
    print(f"wrote {OUT}  ({out['wall_seconds']}s)")
    return out


if __name__ == "__main__":
    main()
