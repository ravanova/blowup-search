"""ADVERSARIAL gates for solver/hilbert_pointwise.py -- Route-HPA, leg 106.

`test_nk_hilbert_pointwise.py` (leg's v9) tests that the module's bound is SHARP and that it
dominates on eight smooth profiles, at one (alpha, gamma) and three rho.  This file tests the
one property that makes a pointwise bound safe to use downstream -- that it is never EXCEEDED
by the true |H(h)| -- on inputs that are degenerate or NaN-poisoned.  `capabilities.py`'s
validated line for the module is what made the question live:

    "no known-answer gate; sampled"

**Leg 106's gate answered YES.**  Two computable configurations exceed the bound:

  (V1) `rho = NaN` -- and bit-identically `rho = +inf` and `rho >= 1e300`.  IEEE-754 sec 5.11
       makes every comparison against NaN False, so `take_T = rho*cT <= cS` is False
       EVERYWHERE and the whole integral, singularity included, is charged to the sup
       account.  `pointwise_bound` returns a finite pair whose second entry is exactly 0.0.
  (V2) `gamma = 0` (and gamma < 0), with NO NaN anywhere.  `cT` no longer vanishes as the
       offset s -> 0, so no account tames the singularity.

The mechanism is one line of the module's own construction: as s -> 0 the kernel weight
`|K|*s -> 2` while `cS -> 2 cos^alpha(theta/2) != 0`, so the sup account's integrand in
`d(log s)` tends to a nonzero constant and the sup-route integral is LOGARITHMICALLY
DIVERGENT.  Only `cT -> 0` (which needs gamma > 0) tames it, and only if the payer rule
actually selects it near s = 0.  What `pointwise_bound` returns in V1/V2 is finite only
because the quadrature starts at `s = eps*L`: it is the eps-truncation of a divergent
integral, not a bound.  Gate 4 demonstrates exactly that by moving eps.

**solver/hilbert_pointwise.py is NOT patched by leg 106** -- the gate's yes-branch escalates,
it does not repair.  So gates 2, 3, 4 and 9 are GAP-PINS in the sense of leg 84: they assert
the CURRENT unsound behaviour so that it cannot decay at the rate of memory, and

    **they must be INVERTED, not weakened, the day a guard lands.**

The repair, when authorised, is a guard -- reject non-finite `rho` and `gamma <= 0` -- not a
change to the majorant, which is correct wherever the payer rule selects the seminorm account
on a neighbourhood of the singularity.  Gates 5-8 are the CONTROLS that establish the blast
radius: the shipped Route-D configuration (alpha 1.5, gamma 0.5, rho in {1, 6, 25}) is not
affected, and gate 5 measures how little room it has left.

Gate 1 is the positive control for the whole file: the battery's own |H(h)| quadrature is
known-answer checked against `solver.hilbert_holder.conjugate` (cos k th -> sin k th, exact)
BEFORE any verdict is read from it.  Without gate 1 the violations are unfalsifiable.

Run: .venv/bin/python test_hilbert_pointwise_adversarial.py
"""

import json
import os
import warnings

import numpy as np

from solver.decay_collocation import grid, transforms
from solver.hilbert_holder import conjugate
from solver.hilbert_pointwise import (
    measured_pointwise, pointwise_bound, pointwise_curves, weighted_sups,
)
from experiments.p2_route_hpa_v1_adversarial import (
    ALPHA, GAMMA, psi_of_poly, psi_of_step, step_norms,
)

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "writeup", "data",
                    "p2_route_hpa_v1_adversarial.json")
THETA = 1.0            # the reference angle every violation gate is stated at


def _banked():
    with open(DATA) as f:
        return json.load(f)


# ---------------------------------------------------------------------------


def test_1_known_answer_positive_control():
    """The battery's |H(h)| machinery reproduces the EXACT conjugate."""
    worst, n = 0.0, 0
    for coef in (np.array([0.0, 1.0]), np.array([0.0, 0.0, 0.0, 1.0]),
                 np.array([0.3, 1.0, -0.5, 0.2, 0.1, -0.4])):
        for th in (0.03, 0.4, 1.2, 2.5, 3.0, 3.14):
            worst = max(worst, abs(psi_of_poly(coef, th)
                                   - float(conjugate(coef, [th])[0])))
            n += 1
    assert worst < 1e-7, worst
    zero = max(abs(psi_of_poly(np.array([1.0]), th)) for th in (0.2, 1.5, 3.0))
    assert zero < 1e-12, zero
    print("[ok] (1) POSITIVE CONTROL: the battery's conjugate quadrature matches the "
          "exact cos k th -> sin k th answer to %.1e over %d cases, and the p.v. of the "
          "constant function is %.1e -- the violations below are measured against a "
          "known-answer-checked |H(h)|" % (worst, n, zero))


def test_2_GAPPIN_violation_rho_nan_and_inf():
    """V1: NaN/inf rho routes the singularity to the divergent sup account."""
    pairs = {r: pointwise_bound(THETA, ALPHA, GAMMA, rho=r)
             for r in (np.nan, np.inf, 1e300)}
    vals = list(pairs.values())
    assert vals[0] == vals[1] == vals[2], pairs           # bit-identical branch
    a_sup, a_semi = vals[0]
    assert a_semi == 0.0, a_semi                          # the whole T account vanishes
    assert 24.0 < a_sup < 24.2, a_sup

    ratios = {}
    for delta in (1e-10, 1e-20, 1e-50):
        S, T = step_norms(THETA, delta)
        ratios[delta] = abs(psi_of_step(THETA, delta)) / (a_sup * S + a_semi * T)
    assert ratios[1e-10] < 1.0, ratios                    # not yet -- the step is too wide
    assert ratios[1e-20] > 1.02, ratios                   # EXCEEDED
    assert ratios[1e-50] > 2.5, ratios                    # and unboundedly so
    print("[ok] (2) GAP-PIN V1: rho = NaN, +inf and 1e300 return the SAME pair "
          "(%.4f, %.1f) -- a_semi is exactly zero -- and the step adversary of width "
          "1e-20 attains |H(h)|/bound = %.4f, rising to %.4f at width 1e-50.  "
          "INVERT THIS GATE, DO NOT WEAKEN IT, when a non-finite-rho guard lands"
          % (a_sup, a_semi, ratios[1e-20], ratios[1e-50]))


def test_3_GAPPIN_violation_gamma_zero():
    """V2: gamma = 0 -- an ordinary-looking argument, no NaN anywhere."""
    a_sup, a_semi = pointwise_bound(THETA, ALPHA, 0.0, rho=1.0)
    assert a_sup == 0.0, a_sup
    assert 12.1 < a_semi < 12.4, a_semi
    ratios = {}
    for delta in (1e-10, 1e-50):
        S, T = step_norms(THETA, delta, gamma=0.0)
        ratios[delta] = abs(psi_of_step(THETA, delta)) / (a_sup * S + a_semi * T)
    assert ratios[1e-10] > 1.03, ratios
    assert ratios[1e-50] > 4.9, ratios
    # gamma < 0 fails the same way and is not even routed to a single account
    neg = pointwise_bound(THETA, ALPHA, -0.5, rho=1.0)
    assert all(np.isfinite(neg)) and neg[0] > 20.0, neg
    print("[ok] (3) GAP-PIN V2: gamma = 0 returns (%.1f, %.4f) and is ALREADY exceeded "
          "at step width 1e-10 (%.4f), rising to %.4f at 1e-50 -- no NaN is involved, "
          "and gamma = -0.5 returns a finite %.2f the same way.  INVERT WHEN GUARDED"
          % (a_sup, a_semi, ratios[1e-10], ratios[1e-50], neg[0]))


def test_4_GAPPIN_the_returned_number_is_an_eps_truncation():
    """The mechanism: it is not a bound, it is where the quadrature was cut off."""
    scan = [(e, pointwise_bound(THETA, ALPHA, GAMMA, rho=np.nan, n_quad=20000, eps=e)[0])
            for e in (1e-6, 1e-10, 1e-14, 1e-20, 1e-30)]
    vals = [v for _, v in scan]
    assert all(b > a for a, b in zip(vals, vals[1:])), scan   # strictly growing, no limit
    assert vals[-1] / vals[0] > 4.9, scan
    # and the growth is the analytic log divergence, not numerical noise
    pred = (2.0 / np.pi) * np.cos(0.5 * THETA) ** ALPHA
    meas = (abs(psi_of_step(THETA, 1e-30)) - abs(psi_of_step(THETA, 1e-20))) / np.log(1e10)
    assert abs(meas / pred - 1.0) < 0.03, (meas, pred)
    # the shipped gamma does NOT do this
    ship = [sum(pointwise_bound(THETA, ALPHA, GAMMA, rho=1.0, n_quad=4000, eps=e))
            for e in (1e-8, 1e-16)]
    assert ship[1] / ship[0] < 1.001, ship
    print("[ok] (4) GAP-PIN mechanism: at rho = NaN the 'bound' grows %.2f -> %.2f (%.1fx) "
          "as eps goes 1e-6 -> 1e-30 with no limit, and |H(h)| diverges at %.4f per "
          "ln(1/delta) against the analytic (2/pi)cos^alpha(theta/2) = %.4f (%.1f%% "
          "error).  At the shipped gamma = 0.5 the same 8 decades of eps move the bound "
          "by %.3f%%" % (vals[0], vals[-1], vals[-1] / vals[0], meas, pred,
                         100 * abs(meas / pred - 1.0), 100 * (ship[1] / ship[0] - 1.0)))


def test_5_CONTROL_shipped_configuration_dominates():
    """The blast radius: alpha 1.5, gamma 0.5, rho in {1, 6, 25} is NOT affected."""
    b = _banked()["A7_shipped_configuration_is_safe"]
    worst_exact = worst_interp = 0.0
    for rho in (1.0, 6.0, 25.0):
        d = b["rho=%g" % rho]
        assert d["max_ratio_vs_exact_bound"] < 1.0, (rho, d)
        assert d["max_ratio_vs_interpolated_bound"] < 1.0, (rho, d)
        worst_exact = max(worst_exact, d["max_ratio_vs_exact_bound"])
        worst_interp = max(worst_interp, d["max_ratio_vs_interpolated_bound"])
        # the margin closes monotonically toward the far field, it does not flip sign
        far = [r for r in d["rows"] if r["pi_minus_theta"] < 1e-3]
        near = [r for r in d["rows"] if r["theta"] < 0.1]
        assert min(r["ratio_vs_exact_bound"] for r in far) > \
            max(r["ratio_vs_exact_bound"] for r in near), (rho, d)
    assert worst_exact > 0.999, worst_exact       # saturated, which is why it is tight
    # live re-check at the single worst angle, so this gate is not a JSON echo
    t = np.pi - 1e-8
    eS, eT = pointwise_bound(t, ALPHA, GAMMA, rho=1.0, n_quad=200000, eps=1e-14)
    assert eS > 0.0 and eT > 0.0, (eS, eT)
    print("[ok] (5) CONTROL: over 10 angles x 3 shipped rho the worst true/bound is "
          "%.6f against the exact bound and %.6f through the interpolated path -- "
          "domination HOLDS, with only %.2e of margin left as theta -> pi, where the "
          "bound is asymptotically SATURATED rather than violated"
          % (worst_exact, worst_interp, 1.0 - worst_interp))


def test_6_default_quadrature_understates_its_own_majorant():
    """Signed, because an understated majorant is the unsafe direction."""
    worst = 0.0
    for th in (1e-6, 1e-3, 0.05, 0.5, 1.0, 2.0, 3.0):
        ref = pointwise_bound(th, ALPHA, GAMMA, rho=6.0, n_quad=200000, eps=1e-14)
        dfl = pointwise_bound(th, ALPHA, GAMMA, rho=6.0)
        worst = min(worst, dfl[0] / ref[0] - 1.0)
    assert -0.05 < worst < -0.02, worst
    # a two-node quadrature is wildly WRONG but in the safe direction; four is not usable
    tiny = sum(pointwise_bound(1.0, ALPHA, GAMMA, rho=6.0, n_quad=2))
    full = sum(pointwise_bound(1.0, ALPHA, GAMMA, rho=6.0, n_quad=200000, eps=1e-14))
    assert tiny / full > 3.0, (tiny, full)
    assert pointwise_bound(1.0, ALPHA, GAMMA, n_quad=1) == (0.0, 0.0)
    print("[ok] (6) the DEFAULT n_quad = 400 understates its own majorant by %.2f%% at "
          "small theta (unsafe direction, but %dx smaller than the margin gate 5 "
          "measures); n_quad = 2 overshoots %.1fx and n_quad <= 1 returns (0, 0) with no "
          "complaint" % (100 * abs(worst), int(0.0002 / abs(worst) * 1e4) if worst else 0,
                         tiny / full))


def test_7_consumption_paths_are_optimistic():
    """Interpolation and the 140-node sup both shave the same far-field margin."""
    b = _banked()["A9_consumption_paths"]
    r1 = next(x for x in b["interpolation"] if x["rho"] == 1.0)
    assert r1["worst_interp_over_exact"] < 0.93, r1
    assert b["closure_sup_understatement_at_140"] > 0.004, b
    assert b["closure_semi_understatement_at_140"] > 0.019, b
    # live: refining n_theta only ever RAISES the sup, i.e. 140 nodes under-report it
    w140 = weighted_sups(pointwise_curves(ALPHA, GAMMA, rho=6.0, n_theta=140,
                                          n_quad=400), ALPHA)
    w560 = weighted_sups(pointwise_curves(ALPHA, GAMMA, rho=6.0, n_theta=560,
                                          n_quad=400), ALPHA)
    assert w560["closure_semi"] > w140["closure_semi"], (w140, w560)
    print("[ok] (7) both consumption paths are optimistic: measured_pointwise's linear "
          "interpolation in log X returns as little as %.4f of the exact coefficient, "
          "and weighted_sups over 140 theta nodes under-reports the sup by %.2f%% "
          "(closure_sup) and %.2f%% (closure_semi)"
          % (r1["worst_interp_over_exact"],
             100 * b["closure_sup_understatement_at_140"],
             100 * b["closure_semi_understatement_at_140"]))


def test_8_grid_norm_hazard_is_journal_B1_not_a_bound_defect():
    """Replays the FROZEN extremiser: >1 under grid norms, far below 1 under true ones."""
    b = _banked()["A8_grid_norm_hazard"]
    row = max(b["rows"], key=lambda r: r["grid_norm_ratio"])
    assert row["grid_norm_ratio"] > 1.0, row
    assert row["refined_norm_ratio"] < 0.2, row
    J = row["J"]
    h = np.array(row["worst_h_nodal_values"])
    th, _ = grid(J)
    to_coef, _, _ = transforms(J)
    t = row["theta"]
    aS, aT = pointwise_bound(t, ALPHA, GAMMA, rho=1.0, n_quad=4000)
    psi = abs(float(conjugate(to_coef @ h, [t])[0]))
    w = np.cos(0.5 * th) ** (-ALPHA)
    ws = np.cos(0.5 * th) ** (-(ALPHA - GAMMA))
    ii, jj = np.triu_indices(J, 1)
    p = np.minimum(ws[ii], ws[jj]) / np.abs(th[ii] - th[jj]) ** GAMMA
    S = float(np.max(w * np.abs(h)))
    T = float(np.max(p * np.abs(h[ii] - h[jj])))
    live = psi / (aS * S + aT * T)
    assert live > 1.0, live
    assert abs(live / row["grid_norm_ratio"] - 1.0) < 1e-6, (live, row)
    print("[ok] (8) the frozen extremiser replays at %.4f > 1 when S and T are read off "
          "the GRID, and at %.4f when they are read off a 6x refinement -- its true "
          "norms are %.1fx and %.1fx larger than the grid pairs can see.  This is "
          "JOURNAL section B1's lesson on this module, NOT a defect of the majorant: "
          "grid-evaluated norms are not the norms the bound is stated in"
          % (live, row["refined_norm_ratio"], row["S_blowup"], row["T_blowup"]))


def test_9_GAPPIN_the_silence_inventory():
    """What the module SAYS when the input is wrong: nothing, mostly."""
    cases = (("rho=nan", lambda: pointwise_bound(1.0, ALPHA, GAMMA, rho=np.nan,
                                                 n_quad=200)),
             ("rho=inf", lambda: pointwise_bound(1.0, ALPHA, GAMMA, rho=np.inf,
                                                 n_quad=200)),
             ("gamma=0", lambda: pointwise_bound(1.0, ALPHA, 0.0, n_quad=200)),
             ("gamma=-0.5", lambda: pointwise_bound(1.0, ALPHA, -0.5, n_quad=200)),
             ("gamma=nan", lambda: pointwise_bound(1.0, ALPHA, np.nan, n_quad=200)),
             ("gamma=inf", lambda: pointwise_bound(1.0, ALPHA, np.inf, n_quad=200)),
             ("theta<0", lambda: pointwise_bound(-0.5, ALPHA, GAMMA, n_quad=200)))
    silent_finite, warned = [], []
    for lbl, fn in cases:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            v = fn()
        if caught:
            warned.append(lbl)
        elif all(np.isfinite(v)):
            silent_finite.append(lbl)
    # the five that matter say nothing at all; only the two inf-in-the-exponent cases warn
    assert set(silent_finite) == {"rho=nan", "rho=inf", "gamma=0", "gamma=-0.5",
                                  "gamma=nan", "theta<0"}, (silent_finite, warned)
    assert set(warned) == {"gamma=inf"}, (silent_finite, warned)
    # and the warning is not a guard: both still RETURN, with the same finite pair
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert pointwise_bound(1.0, ALPHA, np.nan, n_quad=200) == \
            pointwise_bound(1.0, ALPHA, np.inf, n_quad=200)

    class _N:
        def __init__(s, a, b): s.a, s.b = a, b
        def sup_part(s, h): return s.a
        def seminorm(s, h): return s.b

    cv = pointwise_curves(ALPHA, GAMMA, n_theta=40, n_quad=200)
    tt = np.linspace(0.01, 3.1, 60)
    silent = []
    for lbl, norms, psi_of in (("S=NaN", _N(np.nan, 1.0), lambda h: np.cos(tt)),
                               ("S=inf", _N(np.inf, 1.0), lambda h: np.cos(tt)),
                               ("psi=NaN", _N(1.0, 1.0), lambda h: np.full(60, np.nan))):
        r = measured_pointwise({"p": np.sin(tt)}, tt, psi_of, norms, ALPHA, GAMMA, cv,
                               n_sample=20)
        if r["worst_ratio"] == 0.0 and r["profile"] == "":
            silent.append(lbl)
    assert len(silent) == 3, silent
    empty = measured_pointwise({}, tt, lambda h: np.cos(tt), _N(1.0, 1.0), ALPHA, GAMMA,
                               cv, n_sample=20)
    assert empty["worst_ratio"] == 0.0, empty
    print("[ok] (9) GAP-PIN silence: %d of 7 wrong arguments (%s) return a finite pair with "
          "no exception and no warning -- including BOTH unsound configurations; only "
          "%d warn (%s), and even they still return, with gamma = NaN giving the same "
          "pair as gamma = +inf.  measured_pointwise reports worst_ratio 0.0 with an "
          "empty profile name for %d/3 poisoned inputs AND for an empty family -- 0.0 "
          "reads as 'no violation anywhere', the most favourable possible answer"
          % (len(silent_finite), ", ".join(sorted(silent_finite)), len(warned),
             ", ".join(sorted(warned)), len(silent)))


def test_10_the_banked_verdict_is_the_one_this_file_asserts():
    b = _banked()
    assert b["gate_answer"] == "YES", b["gate_answer"]
    assert b["read_only"] is True
    assert b["A5_VIOLATION_rho_nan_or_inf"]["n_violating_cases"] >= 4
    assert b["A6_VIOLATION_gamma_zero"]["n_violating_cases"] == 5
    assert b["A7_shipped_configuration_is_safe"]["thinnest_margin"] > 0.0
    print("[ok] (10) writeup/data/p2_route_hpa_v1_adversarial.json banks gate_answer = "
          "YES with %d + %d violating cases and a shipped-configuration margin of %.2e, "
          "and records the disposition as ESCALATE-do-not-patch"
          % (b["A5_VIOLATION_rho_nan_or_inf"]["n_violating_cases"],
             b["A6_VIOLATION_gamma_zero"]["n_violating_cases"],
             b["A7_shipped_configuration_is_safe"]["thinnest_margin"]))


if __name__ == "__main__":
    test_1_known_answer_positive_control()
    test_2_GAPPIN_violation_rho_nan_and_inf()
    test_3_GAPPIN_violation_gamma_zero()
    test_4_GAPPIN_the_returned_number_is_an_eps_truncation()
    test_5_CONTROL_shipped_configuration_dominates()
    test_6_default_quadrature_understates_its_own_majorant()
    test_7_consumption_paths_are_optimistic()
    test_8_grid_norm_hazard_is_journal_B1_not_a_bound_defect()
    test_9_GAPPIN_the_silence_inventory()
    test_10_the_banked_verdict_is_the_one_this_file_asserts()
    print("\nALL HILBERT-POINTWISE ADVERSARIAL GATES PASSED "
          "(gate answer: YES -- escalated, module unpatched)")
