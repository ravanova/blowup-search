"""Leg 134 (Route-FGB) -- PERMANENT REGRESSION SUITE for solver/fractional_gclm.py.

WHAT THIS IS, AND WHY IT IS NOT test_fractional_gclm_adversarial.py
-------------------------------------------------------------------
Leg 91 (Route-FGA) measured a silent-acceptance gap in `solver/fractional_gclm.py`: `s < 0`
and `nu < 0` were accepted at construction, ran to completion, and returned a finite,
plausible-looking relevance exponent `p` -- which, injected into the `p(s)` fit whose zero
crossing IS the measured `s_c`, moved that crossing by up to +13.33 %. The bench repair
`8d4fdec` closed it. `test_fractional_gclm_adversarial.py` (14 gates) pins that story from
leg 91's side, with gates 6/7/8/9/13 inverted into fix-assertions.

Leg 134's gate asked whether the repair (a) really rejects every `s < 0` / `nu < 0` case in
leg 91's ORIGINAL battery at construction, and (b) leaves the banked `s_c` measurement
unmoved on the validated line -- and its yes-branch says to BANK LEG 91'S BATTERY AS A
PERMANENT REGRESSION SUITE. That is this file.

The difference from the adversarial file is the second half. That file asserts the guards.
This file additionally pins, as literals, the previously validated WELL-BEHAVED-INPUT numbers
the repair must never move -- Route-F's known-answer gate `F1` and its `F2` relevance line at
the production resolution `n = 8192`, the line whose zero crossing is the banked `s_c`. Those
are exactly the numbers an over-eager future guard, or a "harmless" refactor of the `visc`
construction, would break first, and until leg 134 nothing in the repo re-ran them at all.

MEASURED, NOT ASSERTED (leg 134; the pre-repair module read out of git and re-run in the same
environment as the control arm):
  - 7 gate-scoped `s < 0` / `nu < 0` silent-acceptance cases pre-repair -> 0 post-repair
  - 2 of 2 negative-`s` constructions that pre-repair built an INVERTED multiplier (decreasing
    in |k|, ratio exactly 1/k_max) now raise before `visc` exists
  - 2 of 2 invalid-`s` injections that pre-repair reached the `p(s)` fit (shifting its zero by
    -0.07 % and +13.33 %) now reach nothing
  - 6 of 6 admissible-`s` constructions and the admissible-`s` control `p` unaffected
    (`p = 0.4948162270066669`, unmoved to the bit)
  - 16 of 16 quantities on the banked `s_c` line and 5 of 5 on the known-answer gate are
    0 ULP between the pre-repair and post-repair modules: the guard is a bitwise no-op
  - against the 2026-08-02 archive the known-answer gate is 5/5 at 0 ULP, while the viscous
    line sits at up to 663 ULP (worst relative 1.19e-13) -- a NumPy/libm kernel difference,
    not a repair effect, and demonstrated so by a 1-ULP displacement of `visc` alone moving
    the same quantities by up to 484 ULP

WHY THE TWO HALVES ARE PINNED DIFFERENTLY, AND IT IS THE FINDING
----------------------------------------------------------------
`F1` runs at `nu = 0`, `s = 1`: `|k|^{2s}` is an exact integer power and `exp(-nu*visc*dt)`
is `exp(0) = 1`, so no transcendental kernel is exercised non-trivially and the numbers are
reproducible ACROSS environments. It is therefore pinned BITWISE. `F2` runs at `nu = 1e-3`
and fractional `s`, so both kernels are live and the result is reproducible bitwise only
WITHIN one environment. Pinning it bitwise would assert something measured to be false, so it
is pinned at `1e-12`, which is 130x above the 7.66e-15 drift leg 134 measured across a
four-day library change and still 1.7e-13 of Route-F's own dominant (fit-window) systematic.
A failure here at 1e-13 is an environment change; a failure at 1e-3 is a regression.

The pure closed forms `critical_s` / `relevance_exponent` still carry no domain -- the repair
was scoped to the operator. That is a KNOWN, NARROWED gap, pinned by gates 2/3/5 of
`test_fractional_gclm_adversarial.py`, and it is not re-pinned here.

Nothing in this file measures, re-derives or contests `s_c = alpha/2`, which is validated
against XU eq (6.3) and PRE-EMPTED under Route-J. The banked numbers are pinned only to check
that they do not move.

Companion battery: experiments/p2_route_fgb_v1_postrepair.py
Companion data:    writeup/data/p2_route_fgb_v1_postrepair.json
Pre-repair evidence (frozen, leg 91's): writeup/data/p2_route_fga_v1_adversarial.json
Banked line (frozen, Route-F's):        writeup/data/p2_route_f_v1_viscosity.json

`solver/fractional_gclm.py` is READ-ONLY to leg 134, under either branch of its gate.

Run: PYTHONPATH=. .venv/bin/python test_fractional_gclm_postrepair.py    (~25 s)
"""

import sys

import numpy as np

sys.path.insert(0, ".")

from solver.fractional_gclm import (           # noqa: E402
    FractionalGCLM, clm_blowup_time, clm_exact, estimate_T, fit_relevance,
)

NAN, INF = float("nan"), float("inf")

# Leg 91's own audit constants, VERBATIM from experiments/p2_route_fga_v1_adversarial.py --
# the control literal below was measured at these settings and is meaningless at any other.
N_AUDIT, NU_AUDIT, AMP_AUDIT, MAX_STEPS_AUDIT = 512, 1e-3, 3e3, 20000

# Route-F's production constants -- the validated line. Not re-tuned here.
N_LINE, AMP_LINE, NU_LINE, A_LINE = 8192, 1000.0, 1e-3, 0.0
S_LINE = (0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75)

# --- BANKED LITERALS, copied from writeup/data/p2_route_f_v1_viscosity.json ----------
# generated 2026-08-02T01:15:27Z. Never regenerated by this file.
BANKED_F1 = {"T_exact": 3.333333333333334,
             "solver_vs_exact_at_2.5": 1.8638939280890554e-09,
             "T_est": 3.333428324580673,
             "max_tail": 0.014784515203792828}
BANKED_F2_P = (0.7330916148392316, 0.5227460768873793, 0.31832443256996273,
               0.10917284508728227, -0.10024320762055065, -0.30888753017629811,
               -0.5027100741440663)
BANKED_F2_SLOPE = -2.0675856861670567
BANKED_F2_S_ZERO = 0.5033053850201455      # THE BANKED s_c MEASUREMENT

# The tolerance for the viscous line, and where it comes from (see the module docstring):
# leg 134 measured the worst archive-arm drift at 1.191e-13 relative on p and 7.66e-15
# absolute on s_zero, across a four-day NumPy/libm change, with the repair itself at 0 ULP.
FP_TOL = 1e-12

# Leg 91's admissible-s control value, unmoved by the repair to the bit (leg 134, B1/A5).
CONTROL_P_AUDIT = 0.4948162270066669


def w0(n):
    x = np.arange(n) * 2.0 * np.pi / n
    return np.sin(x) + 0.4 * np.sin(2.0 * x)


def pipeline(s, nu=NU_AUDIT, n=N_AUDIT):
    """The exact caller path Route-F's relevance line uses, at audit resolution."""
    try:
        g = FractionalGCLM(n=n, a=0.0, nu=nu, s=s)
        r = g.run(w0(n), amp_factor=AMP_AUDIT, sample_every=5, max_steps=MAX_STEPS_AUDIT)
        f = fit_relevance(r, estimate_T(r))
        return float(f.get("p", NAN)), r["outcome"], None
    except Exception as e:                       # noqa: BLE001 -- the suite wants them all
        return NAN, "EXCEPTION", "%s: %s" % (type(e).__name__, e)


def f2_line():
    """Route-F's F2 relevance line, recomputed at the production resolution."""
    ps = []
    for s in S_LINE:
        g = FractionalGCLM(n=N_LINE, a=A_LINE, nu=NU_LINE, s=s)
        r = g.run(w0(N_LINE), amp_factor=AMP_LINE, sample_every=5, max_steps=600000)
        ps.append(float(fit_relevance(r, estimate_T(r))["p"]))
    c = np.polyfit(np.array(S_LINE, float), np.array(ps), 1)
    return ps, float(c[0]), float(-c[1] / c[0])


# ------------------------------------------------------------------ clause (a)
def check_negative_s_is_rejected_before_the_operator_exists():
    """Leg 91's A2/A3 negative-s cases. The raise must precede `visc`, because the whole
    defect was that `visc[0] = 0.0` masked the `inf` that says the operator is ill-defined."""
    cases = (-0.5, -2.0, -1e-12, -1e6)
    for s in cases:
        try:
            FractionalGCLM(n=N_AUDIT, a=0.0, nu=NU_AUDIT, s=s)
        except ValueError as e:
            assert "sigma = 2 s >= 0" in str(e), "wrong reason for s = %r: %s" % (s, e)
        else:
            raise AssertionError("s = %r constructed an operator; leg 91 measured that this "
                                 "builds a multiplier DECREASING in |k| with the k=0 inf "
                                 "masked to 0.0, and returns a finite p" % s)
    # and the whole pipeline, not just the constructor
    for s in (-0.5, -2.0):
        p, outcome, exc = pipeline(s)
        assert not np.isfinite(p) and exc is not None and outcome == "EXCEPTION", (
            "s = %r reached the pipeline: p = %r, outcome %s" % (s, p, outcome))
    return ("%d negative-s constructions rejected with the sigma = 2s >= 0 reason, and "
            "2 of 2 pipeline calls raise instead of returning leg 91's p = +2.1864 / "
            "+3.2481" % len(cases))


def check_negative_dissipation_strength_is_rejected():
    """Leg 91's A5: nu = -1e-3 returned a finite p = +0.5264, +6.38 % off the control."""
    for nu in (-1e-3, -1e-300, -1.0):
        try:
            FractionalGCLM(n=N_AUDIT, a=0.0, nu=nu, s=0.35)
        except ValueError as e:
            assert "nu >= 0 is required" in str(e), "wrong reason for nu = %r: %s" % (nu, e)
        else:
            raise AssertionError("nu = %r constructed: an energy SOURCE wearing the "
                                 "dissipation's name" % nu)
    p, outcome, exc = pipeline(0.35, nu=-1e-3)
    assert not np.isfinite(p) and exc is not None, (
        "nu = -1e-3 reached the pipeline and returned p = %r (leg 91: +0.5264, +6.38 %% "
        "off control, silently)" % p)
    return ("3 of 3 negative-nu constructions and 1 of 1 pipeline call rejected; leg 91's "
            "+6.38 % silent shift on p is unreachable")


def check_no_invalid_point_can_reach_the_sc_fit():
    """Leg 91's A4, the headline. The zero crossing of the p(s) fit IS the measured s_c;
    pre-repair one injected point moved it by -0.07 % (s=-0.5) and +13.33 % (s=-2.0)."""
    reached = []
    for s_bad in (-0.5, -2.0):
        p, _, exc = pipeline(s_bad)
        if np.isfinite(p) and exc is None:
            reached.append((s_bad, p))
    assert not reached, ("invalid-s points still reach the s_c fit: %r" % reached)
    return ("0 of 2 invalid-s injections produce a finite p, so neither of leg 91's "
            "-0.000417 (-0.07 %) and +0.080308 (+13.33 %) shifts of the measured s_c is "
            "reachable through the solver")


# ------------------------------------------------- clause (a), the other direction
def check_the_guard_did_not_overshoot():
    """s = 0 is the literature's MARGINAL case (sigma = 0, the Oldroyd-B stress reading) and
    is ADMISSIBLE; nu = 0 is the inviscid case. A guard that rejected either is a regression,
    not a fix. This is the control that can come out the other way."""
    g0 = FractionalGCLM(n=N_AUDIT, a=0.0, nu=NU_AUDIT, s=0.0)
    assert np.all(g0.visc[1:] == 1.0) and g0.visc[0] == 0.0, "s = 0 built the wrong visc"
    gnu = FractionalGCLM(n=N_AUDIT, a=0.0, nu=0.0, s=1.0)
    assert np.all(np.isfinite(gnu.visc)), "nu = 0 built a non-finite visc"
    p0, out0, exc0 = pipeline(0.0)
    assert exc0 is None, "the marginal s = 0 was rejected: %s" % exc0
    built = 0
    for s in (0.0, 0.15, 0.35, 0.55, 0.75, 1.0, 60.0, 200.0):
        FractionalGCLM(n=N_AUDIT, a=0.0, nu=NU_AUDIT, s=s)
        built += 1
    p_ctrl, _, _ = pipeline(0.35)
    assert p_ctrl == CONTROL_P_AUDIT, (
        "the admissible-s control p moved: %.17g vs banked %.17g"
        % (p_ctrl, CONTROL_P_AUDIT))
    return ("%d of %d non-negative s values still construct (including the marginal s = 0, "
            "visc == 1 off the mean, pipeline outcome '%s'), and the admissible-s control "
            "p = %.16f is unmoved to the bit" % (built, built, out0, p_ctrl))


def check_the_operator_is_still_a_dissipation():
    """Positive control that can fail: at an admissible s, visc must INCREASE in |k|. This is
    the property whose inversion leg 91 found and which no code path ever checked."""
    g = FractionalGCLM(n=N_AUDIT, a=0.0, nu=NU_AUDIT, s=0.35)
    assert np.all(np.diff(g.visc[1:]) > 0.0), "visc is not increasing in |k| at s = 0.35"
    assert g.visc[0] == 0.0, "the mean mode is being dissipated"
    ratio = float(g.visc[-1] / g.visc[1])
    assert ratio > 1.0, "ratio %g" % ratio
    return ("s = 0.35: visc strictly increasing in |k|, mean undamped, "
            "visc[k_max]/visc[1] = %.4f > 1 (pre-repair, s = -0.5 gave exactly 1/k_max)"
            % ratio)


# ------------------------------------------------------------- regressions leg 91 passed
def check_the_already_correct_refusals_did_not_regress():
    """Leg 91 found four inputs the module ALREADY handled correctly. A repair must not turn
    any of them into a silently-accepted value -- these are banked so a future "fix" cannot."""
    rows = []
    for label, s, nu in (("s = 60 (just under the float64 wall)", 60.0, NU_AUDIT),
                         ("s = 200 (over the wall, visc = inf)", 200.0, NU_AUDIT),
                         ("s = NaN", NAN, NU_AUDIT),
                         ("nu = NaN", 0.35, NAN),
                         ("nu = +inf", 0.35, INF)):
        p, outcome, exc = pipeline(s, nu=nu)
        assert not np.isfinite(p), "%s returned a finite p = %r" % (label, p)
        rows.append((label, outcome))
    # NaN must still PROPAGATE, not be converted into an exception -- deliberate, leg 91 A5.
    gnan = FractionalGCLM(n=N_AUDIT, a=0.0, nu=NU_AUDIT, s=NAN)
    assert np.isnan(gnan.s), "NaN s was silently coerced"
    return ("5 of 5 already-correct refusals still refuse (%s), and a NaN s still PROPAGATES "
            "through construction rather than being converted into an exception"
            % ", ".join("%s->%s" % (o, "p=nan") for _, o in rows))


# ------------------------------------------------------------------ clause (b)
def check_known_answer_gate_is_bitwise_unmoved():
    """Route-F's F1, pinned BITWISE against the 2026-08-02 archive.

    nu = 0 and s = 1, so |k|^{2s} is an exact integer power and exp(-nu*visc*dt) = exp(0) = 1:
    no transcendental kernel is exercised non-trivially, and leg 134 measured 5 of 5
    quantities at 0 ULP across a four-day NumPy/libm change. Bitwise is the right pin here.
    """
    n = N_LINE
    w = w0(n)
    T0 = clm_blowup_time(w)
    g = FractionalGCLM(n=n, a=0.0, nu=0.0, s=1.0)
    mid = g.run(w, t_end=2.5, amp_factor=1e12, sample_every=5)
    err = float(np.max(np.abs(mid["omega"] - clm_exact(w, mid["t_final"]))))
    r = g.run(w, amp_factor=AMP_LINE, sample_every=5)
    Te = estimate_T(r)
    got = {"T_exact": float(T0), "solver_vs_exact_at_2.5": err,
           "T_est": float(Te), "max_tail": float(r["max_tail"])}
    for k, v in BANKED_F1.items():
        assert got[k] == v, ("F1 %s moved: %.17g vs banked %.17g" % (k, got[k], v))
    return ("4 of 4 known-answer quantities bitwise-identical to the 2026-08-02 archive "
            "(T_exact = %.13f, solver-vs-exact = %.4e, recovered T = %.10f)"
            % (got["T_exact"], got["solver_vs_exact_at_2.5"], got["T_est"]))


def check_the_banked_sc_line_is_unmoved():
    """Route-F's F2 at the production resolution n = 8192 -- the validated line whose zero
    crossing IS the banked s_c. Pinned at FP_TOL, not bitwise, for the reason in the module
    docstring: this line exercises pow and exp non-trivially, and leg 134 measured it drifting
    7.66e-15 (absolute, on s_zero) across a library change while the REPAIR itself moved it by
    0 ULP on all 16 quantities."""
    ps, slope, s_zero = f2_line()
    worst = 0.0
    for s, got, banked in zip(S_LINE, ps, BANKED_F2_P):
        rel = abs(got - banked) / abs(banked)
        worst = max(worst, rel)
        assert rel < FP_TOL, ("p(s=%.2f) moved: %.17g vs banked %.17g (relative %.3e, "
                              "tolerance %.0e)" % (s, got, banked, rel, FP_TOL))
    d_slope = abs(slope - BANKED_F2_SLOPE) / abs(BANKED_F2_SLOPE)
    d_zero = abs(s_zero - BANKED_F2_S_ZERO)
    assert d_slope < FP_TOL, "slope moved by %.3e relative" % d_slope
    assert d_zero < FP_TOL, ("THE BANKED s_c MEASUREMENT MOVED: %.17g vs banked %.17g "
                             "(absolute %.3e, tolerance %.0e)"
                             % (s_zero, BANKED_F2_S_ZERO, d_zero, FP_TOL))
    return ("7 of 7 p values, the slope (%.10f) and the zero crossing (%.13f) reproduce the "
            "banked line; worst relative move %.3e on p and %.3e absolute on s_zero, against "
            "a %.0e tolerance and Route-F's own 0.0452 fit-window systematic"
            % (slope, s_zero, worst, d_zero, FP_TOL))


CHECKS = [
    check_negative_s_is_rejected_before_the_operator_exists,
    check_negative_dissipation_strength_is_rejected,
    check_no_invalid_point_can_reach_the_sc_fit,
    check_the_guard_did_not_overshoot,
    check_the_operator_is_still_a_dissipation,
    check_the_already_correct_refusals_did_not_regress,
    check_known_answer_gate_is_bitwise_unmoved,
    check_the_banked_sc_line_is_unmoved,
]


def main():
    for fn in CHECKS:
        print("PASS %s: %s" % (fn.__name__, fn()))
    print("\nall fractional_gclm post-repair regression checks passed (%d checks)."
          % len(CHECKS))
    print("Leg 91's 7 gate-scoped s<0 / nu<0 silent-acceptance cases -> 0, and the banked "
          "s_c line moved 0 ULP on all 16 quantities between the pre-repair and post-repair "
          "modules (leg 134, Route-FGB).")


if __name__ == "__main__":
    main()
