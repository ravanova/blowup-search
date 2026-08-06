"""ADVERSARIAL gates for solver/hilbert_holder.py -- Route-HHA, leg 119.

`test_nk_hilbert_holder.py` tests that the module's codomain-seminorm bound is SHARP-ISH
and that it dominates on nine smooth profiles, at two hand-picked (alpha, gamma) pairs, both
gamma > 0.  This file tests the one property that makes the bound safe to use downstream --
that it is never EXCEEDED by the true weighted increment of psi = H(h) -- on inputs that are
degenerate or NaN-poisoned.  `capabilities.py`'s validated line for the module is what made
the question live:

    "no known-answer gate; bounds checked against dense sampling"

**Leg 119's gate answered YES.**  Two computable, entirely NaN-free configurations exceed
`increment_pair_bound`'s reported (u_S, u_T):

  (V1) `gamma = 0.0`.  The near-pole singularity's mass is charged entirely to the sup
       account (`u_S = 0.0` exactly, all mass in `u_T`), whose account does NOT vanish as the
       pair separation shrinks -- `increment_pair_bound`'s quadrature starts at `s = eps*lo`,
       not `s = 0`, so the returned coefficient is an eps-truncation of a divergent integral.
  (V2) `gamma = -0.5`.  Same mechanism, mirrored to the other account (`u_S` now carries the
       divergent mass).  Neither needs a NaN anywhere.

This is a direct structural analogue of leg 106's V2 (`gamma = 0` on the *pointwise* bound in
`hilbert_pointwise.py`), transplanted to hilbert_holder.py's *codomain-seminorm* bound, whose
`_increment_env` routing rule (`take_T = cT <= cS`) has the identical shape without a `rho`
parameter to poison instead.

**solver/hilbert_holder.py is NOT patched by leg 119** -- the gate's yes-branch escalates, it
does not repair.  So gates 2, 3, 4 and 8 (the unsound rows) are GAP-PINS in the sense of leg
84: they assert the CURRENT unsound behaviour so that it cannot decay at the rate of memory,
and

    **they must be INVERTED, not weakened, the day a guard lands.**

The repair, when authorised, is a guard on `increment_pair_bound` and `hilbert_holder_constant`
-- reject `gamma <= 0` (and non-finite `gamma`/`alpha`) -- not a change to the majorant, which
is correct wherever the payer rule selects the seminorm account on a neighbourhood of the
near-pole singularity.  Gate 5 is the CONTROL that establishes the blast radius: the shipped
(alpha=1.5, gamma=0.5) and production (alpha~1.4, gamma~0.15) configurations are not affected.

Gate 1 is the positive control for the whole file: the battery's own |H(h)| quadrature is
known-answer checked against `solver.hilbert_holder.conjugate` (cos k th -> sin k th, exact),
and separately the module's OWN `decomposition_exact` is checked against the same exact
answer, BEFORE any verdict is read from either.

Run: .venv/bin/python test_hilbert_holder_adversarial.py
"""

import json
import os
import warnings

import numpy as np

from solver.hilbert_holder import (
    conjugate, hilbert_holder_constant, increment_pair_bound, increment_regime, near_padding,
)
from experiments.p2_route_hha_v1_adversarial import ALPHA, GAMMA, pair_ratio, psi_of_poly

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "writeup", "data",
                    "p2_route_hha_v1_adversarial.json")
THETA1, SIGMA = 1.0, 0.05          # the pair every violation gate is stated at


def _banked():
    with open(DATA) as f:
        return json.load(f)


# ---------------------------------------------------------------------------


def test_1_known_answer_positive_control():
    """The battery's |H(h)| machinery, AND the module's own decomposition_exact, both
    reproduce the EXACT conjugate on cosine polynomials."""
    from solver.hilbert_holder import decomposition_exact
    worst, n = 0.0, 0
    for coef in (np.array([0.0, 1.0]), np.array([0.0, 0.0, 0.0, 1.0]),
                 np.array([0.3, 1.0, -0.5, 0.2, 0.1, -0.4])):
        for th in (0.03, 0.4, 1.2, 2.5, 3.0, 3.14):
            worst = max(worst, abs(psi_of_poly(coef, th) - float(conjugate(coef, [th])[0])))
            n += 1
    assert worst < 1e-7, worst
    zero = max(abs(psi_of_poly(np.array([1.0]), th)) for th in (0.2, 1.5, 3.0))
    assert zero < 1e-12, zero
    dec_worst = 0.0
    for coef in (np.array([0.0, 1.0]), np.array([0.3, 1.0, -0.5, 0.2, 0.1, -0.4])):
        for th, sig in ((0.7, 0.05), (0.7, -0.3), (2.9, 0.02), (1.0, 1.5)):
            got = decomposition_exact(coef, th, sig, n_quad=8000)
            exact = float(conjugate(coef, [th])[0] - conjugate(coef, [th + sig])[0])
            dec_worst = max(dec_worst, abs(got - exact))
    assert dec_worst < 1e-3, dec_worst
    print("[ok] (1) POSITIVE CONTROL: the battery's own quadrature matches the exact "
          "cos k th -> sin k th answer to %.1e over %d cases (p.v. of a constant is "
          "%.1e), and the module's OWN decomposition_exact matches it to %.1e -- the "
          "violations below are measured against a known-answer-checked psi"
          % (worst, n, zero, dec_worst))


def test_2_GAPPIN_violation_gamma_zero():
    """V1: gamma = 0.0 -- no NaN anywhere, all mass silently charged to one account."""
    u_S, u_T = increment_pair_bound(THETA1, SIGMA, ALPHA, 0.0)
    assert u_S == 0.0, u_S
    assert 27.0 < u_T < 28.0, u_T
    ratios = {d: pair_ratio(THETA1, SIGMA, ALPHA, 0.0, d)["ratio_true_over_bound"]
              for d in (1e-9, 1e-30, 1e-50)}
    assert ratios[1e-9] < 1.0, ratios              # not yet -- the feature is too wide
    assert ratios[1e-30] < 1.0, ratios
    assert ratios[1e-50] > 1.2, ratios              # EXCEEDED
    print("[ok] (2) GAP-PIN V1: gamma = 0.0 returns (u_S, u_T) = (%.4f, %.4f) -- u_S is "
          "exactly zero -- and the adversary of width delta = 1e-50 attains true/bound = "
          "%.4f, up from %.4f at delta = 1e-9.  INVERT THIS GATE, DO NOT WEAKEN IT, when a "
          "gamma > 0 guard lands" % (u_S, u_T, ratios[1e-50], ratios[1e-9]))


def test_3_GAPPIN_violation_gamma_negative():
    """V2: gamma = -0.5 -- the same mechanism, mirrored to the other account."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        u_S, u_T = increment_pair_bound(THETA1, SIGMA, ALPHA, -0.5)
        ratios = {d: pair_ratio(THETA1, SIGMA, ALPHA, -0.5, d)["ratio_true_over_bound"]
                  for d in (1e-9, 1e-30, 1e-50)}
    assert u_S > 10.0, u_S
    assert ratios[1e-9] < 1.0, ratios
    assert ratios[1e-50] > 1.2, ratios
    # the assembly-level public API also returns a finite pair, silently (mod warnings)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        hhc = hilbert_holder_constant(ALPHA, -0.3, n_theta=24, n_d=14, n_quad=200)
    assert np.isfinite(hhc["b_sup"]) and np.isfinite(hhc["b_semi"]), hhc
    assert len(caught) > 0                          # it warns, but it does NOT raise
    print("[ok] (3) GAP-PIN V2: gamma = -0.5 returns (u_S, u_T) = (%.4f, %.4f) and is "
          "exceeded %.4fx at delta = 1e-50 (from %.4fx at 1e-9); the ASSEMBLY-level "
          "hilbert_holder_constant(1.5, -0.3, ...) returns a finite (%.2f, %.2f) across "
          "the whole 24x14 pair grid with only %d warnings, never raising.  INVERT WHEN "
          "GUARDED" % (u_S, u_T, ratios[1e-50], ratios[1e-9], hhc["b_sup"], hhc["b_semi"],
                       len(caught)))


def test_4_GAPPIN_eps_truncation_mechanism():
    """The mechanism: the coefficient is where the quadrature was cut off, not a bound."""
    scan = [(e, increment_pair_bound(THETA1, SIGMA, ALPHA, 0.0, n_quad=4000, eps=e)[1])
            for e in (1e-6, 1e-10, 1e-14, 1e-16)]
    vals = [v for _, v in scan]
    assert all(b > a for a, b in zip(vals, vals[1:])), scan   # strictly growing, no plateau
    assert vals[-1] / vals[0] > 2.0, scan
    # the shipped gamma does NOT do this
    ship = [sum(increment_pair_bound(THETA1, SIGMA, ALPHA, GAMMA, n_quad=4000, eps=e))
            for e in (1e-8, 1e-16)]
    assert ship[1] / ship[0] < 1.01, ship
    print("[ok] (4) GAP-PIN mechanism: at gamma = 0 the seminorm coefficient grows %.2f -> "
          "%.2f (%.2fx) as eps goes 1e-6 -> 1e-16 with NO plateau, while the shipped "
          "gamma = 0.5 moves the same sum by only %.3f%% over the identical sweep"
          % (vals[0], vals[-1], vals[-1] / vals[0], 100 * (ship[1] / ship[0] - 1.0)))


def test_5_CONTROL_shipped_and_production_are_safe():
    """The blast radius: (alpha=1.5, gamma=0.5) and (alpha~1.4, gamma~0.15) are NOT affected."""
    b = _banked()["A6_CONTROL_shipped_and_production_are_safe"]
    for label in ("shipped_1.5_0.5", "production_1.4_0.15"):
        d = b[label]
        assert d["max_ratio_over_all_pairs"] < 1.0, (label, d)
        for pair in d["by_pair"]:
            ratios = [r["ratio_true_over_bound"] for r in pair["rows"]]
            # monotonically falling toward zero as delta shrinks -- the opposite of V1/V2
            assert ratios[-1] <= ratios[0], (label, pair)
            assert ratios[-1] < 1e-3, (label, pair)
    # live re-check at one pair, so this gate is not a pure JSON echo
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        live = pair_ratio(THETA1, SIGMA, ALPHA, GAMMA, 1e-9)
    assert live["ratio_true_over_bound"] < 0.01, live
    print("[ok] (5) CONTROL: both the shipped and production configurations dominate at "
          "every probed pair and delta, worst ratio %.4f (shipped) / %.4f (production); "
          "the ratio falls toward ZERO (not toward one) as the feature narrows -- opposite "
          "asymptotics from the violating gamma <= 0 rows"
          % (b["shipped_1.5_0.5"]["max_ratio_over_all_pairs"],
             b["production_1.4_0.15"]["max_ratio_over_all_pairs"]))


def test_6_GAPPIN_the_silence_and_crash_inventory():
    """What the module SAYS when the input is wrong: mostly nothing, once loudly."""
    silent_finite = []
    for label, fn in (("gamma=0.0", lambda: increment_pair_bound(THETA1, SIGMA, ALPHA, 0.0)),
                      ("gamma=-0.5", lambda: increment_pair_bound(THETA1, SIGMA, ALPHA, -0.5)),
                      ("gamma=-1.0", lambda: increment_pair_bound(THETA1, SIGMA, ALPHA, -1.0))):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            v = fn()
        if not caught and all(np.isfinite(v)):
            silent_finite.append(label)
    # every gamma <= 0 case tried is silent at default (n_quad, eps) -- no warning at all
    assert set(silent_finite) == {"gamma=0.0", "gamma=-0.5", "gamma=-1.0"}, silent_finite
    # gamma = 0.0 fed to the FULL public API crashes instead of returning silently
    try:
        hilbert_holder_constant(ALPHA, 0.0, n_theta=16, n_d=10, n_quad=100)
        raised = False
    except ZeroDivisionError:
        raised = True
    assert raised
    # but gamma = -0.3 through the SAME public API does not raise -- only warns
    with warnings.catch_warnings(record=True) as caught2:
        warnings.simplefilter("always")
        hhc = hilbert_holder_constant(ALPHA, -0.3, n_theta=16, n_d=10, n_quad=100)
    assert np.isfinite(hhc["b_sup"]) and np.isfinite(hhc["b_semi"])
    assert len(caught2) > 0
    # near_padding(0) raises rather than returning silently -- a loud failure, checked here
    try:
        near_padding(0.0)
        raised_np = False
    except ZeroDivisionError:
        raised_np = True
    assert raised_np
    assert increment_regime(1.0, 3.0) is False        # too wide, correctly excluded
    print("[ok] (6) at the LOW-LEVEL function, ALL THREE of gamma = 0.0/-0.5/-1.0 are "
          "silent-finite at default (n_quad, eps) -- no warning, no exception, just a "
          "plausible-looking pair.  At the PUBLIC ASSEMBLY API the polarity flips for "
          "gamma = 0.0 exactly: it CRASHES (ZeroDivisionError in the pointwise route's "
          "hilbert_split_bound) while gamma = -0.3 returns silently (mod warnings) -- "
          "neither polarity is safe, they are just differently unsafe")


def test_7_alpha_inf_is_vacuous_not_a_finding():
    """Pre-declared in the novelty pass: alpha = inf collapses the admissible ball to {0}."""
    b = _banked()["A7_alpha_inf_is_vacuous_not_a_finding"]
    assert b["a_sup"] == 0.0 and b["a_semi"] == 0.0, b
    assert all(w == float("inf") for w in b["decay_weight_at_alpha_inf_away_from_theta0"])
    # live: no candidate h with a genuinely finite S=1 and alpha=inf exists away from theta=0
    thetas = np.array([0.3, 1.0, 2.0, 3.0])
    with np.errstate(over="ignore"):
        w = np.cos(0.5 * thetas) ** (-np.inf)
    assert np.all(np.isinf(w)), w
    print("[ok] (7) alpha = inf's (0, 0) 'bound' is VACUOUSLY true, not a silent "
          "corruption: the decay weight is +inf at every theta != 0, so no nonzero "
          "function has finite S there -- reported as a control, not a finding, exactly "
          "as the novelty pass anticipated")


def test_8_GAPPIN_soundness_predicate():
    """The exact predicate: gamma > 0.  Mapped against the eps-drift diagnostic."""
    b = _banked()["A8_soundness_predicate"]
    ok = [r for r in b["rows"] if r["predicted_sound"]]
    bad = [r for r in b["rows"] if not r["predicted_sound"]]
    assert len(ok) >= 4 and len(bad) >= 4, b
    assert b["max_eps_drift_sound"] < 1.4, b            # gamma=0.05 is the marginal case
    assert b["min_eps_drift_unsound"] > 1.9, b
    # live spot check at the boundary itself
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        b1 = increment_pair_bound(THETA1, SIGMA, ALPHA, 0.0, n_quad=4000, eps=1e-8)
        b2 = increment_pair_bound(THETA1, SIGMA, ALPHA, 0.0, n_quad=4000, eps=1e-16)
    assert sum(b2) / sum(b1) > 1.3
    print("[ok] (8) GAP-PIN: the analytic predicate gamma > 0 separates sound from unsound "
          "cleanly -- max eps-drift %.4fx when sound vs min %.4fx when not, with no "
          "marginal gamma where the diagnostic and the predicate disagree (unlike leg "
          "106's pointwise sibling). INVERT WHEN GUARDED"
          % (b["max_eps_drift_sound"], b["min_eps_drift_unsound"]))


def test_9_the_banked_verdict_is_the_one_this_file_asserts():
    b = _banked()
    assert b["gate_answer"] == "YES", b["gate_answer"]
    assert b["read_only"] is True
    assert b["A4_VIOLATION_gamma_zero"]["n_violating_cases"] >= 2
    assert b["A5_VIOLATION_gamma_negative"]["n_violating_cases"] >= 2
    assert b["A6_CONTROL_shipped_and_production_are_safe"]["shipped_1.5_0.5"][
        "max_ratio_over_all_pairs"] < 1.0
    print("[ok] (9) writeup/data/p2_route_hha_v1_adversarial.json banks gate_answer = "
          "YES with %d + %d violating cases and shipped/production margins both < 1.0, "
          "and records the disposition as ESCALATE-do-not-patch"
          % (b["A4_VIOLATION_gamma_zero"]["n_violating_cases"],
             b["A5_VIOLATION_gamma_negative"]["n_violating_cases"]))


if __name__ == "__main__":
    test_1_known_answer_positive_control()
    test_2_GAPPIN_violation_gamma_zero()
    test_3_GAPPIN_violation_gamma_negative()
    test_4_GAPPIN_eps_truncation_mechanism()
    test_5_CONTROL_shipped_and_production_are_safe()
    test_6_GAPPIN_the_silence_and_crash_inventory()
    test_7_alpha_inf_is_vacuous_not_a_finding()
    test_8_GAPPIN_soundness_predicate()
    test_9_the_banked_verdict_is_the_one_this_file_asserts()
    print("\nALL HILBERT-HOLDER ADVERSARIAL GATES PASSED "
          "(gate answer: YES -- escalated, module unpatched)")
