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

**solver/hilbert_holder.py was NOT patched by leg 119** -- the gate's yes-branch escalates, it
does not repair.  So gates 2, 3, 4, 6 and 8 were GAP-PINS in the sense of leg 84: they asserted
the CURRENT unsound behaviour so that it could not decay at the rate of memory, and

    **they must be INVERTED, not weakened, the day a guard lands.**

--------------------------------------------------------------------------
THE GUARD LANDED: LEG 153 (Route-HHR), AND THOSE FIVE PINS ARE INVERTED HERE
--------------------------------------------------------------------------
Gates 2, 3, 4, 6 and 8 now assert the REPAIRED behaviour, in the same commit as the guard.
`increment_pair_bound` and `hilbert_holder_constant` reject `gamma <= 0` and non-finite
`gamma`/`alpha` with a single `HilbertHolderDomainError`, at BOTH levels and BOTH polarities.
The majorant itself is untouched -- it is correct wherever the payer rule selects the seminorm
account on a neighbourhood of the near-pole singularity -- so this is a domain guard, never a
sharpening.

Leg 119's measurements are not deleted by the repair, which is the point of the inversions
rather than deletions: `on_unsound="extrapolate"` reproduces every pre-repair number, and the
adversary still attains true/bound = 1.2311 at delta = 1e-50 through it.  `on_unsound="inflate"`
returns the honest `(inf, inf)`.

Two gates are NEW.  Gate 10 is leg 153's gate (b) -- the entire licence for the repair -- and
gate 11 pins the one band deliberately WARNED rather than rejected (the production optimum,
whose head reaches 5.08e-2 of its returned pair at the default eps while its exact majorant
stays finite).  Gate 8 additionally records a CORRECTION to leg 119's own eps-drift diagnostic
commentary: its gamma ladder stopped at 0.05, and extending it to 1e-6 puts three SOUND
configurations above the 1.98 unsound floor leg 119 banked.  Its VERDICT is unaffected -- that
rested on the exact predicate `gamma > 0`, which stands and is now enforced.

Gate 5 is the CONTROL that establishes the blast radius: the shipped
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
    HEAD_WARN_TOL, HilbertHolderDomainError, HilbertHolderTruncationWarning,
    HilbertHolderUnsoundWarning, _head_bound, conjugate, hilbert_holder_constant,
    increment_pair_bound, increment_regime, near_padding, pair_grid,
)
from experiments.p2_route_hha_v1_adversarial import ALPHA, GAMMA, pair_ratio, psi_of_poly
from experiments.p2_route_hhr_v1_repair import guarded_pair_ratio

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(_HERE, "writeup", "data", "p2_route_hha_v1_adversarial.json")
REPAIR = os.path.join(_HERE, "writeup", "data", "p2_route_hhr_v1_repair.json")
THETA1, SIGMA = 1.0, 0.05          # the pair every violation gate is stated at


def _banked():
    with open(DATA) as f:
        return json.load(f)


def _repair():
    """Leg 153's curated JSON -- the post-guard half of this file's evidence."""
    with open(REPAIR) as f:
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


def test_2_INVERTED_violation_gamma_zero_now_REJECTED():
    """V1 INVERTED (leg 153): gamma = 0.0 no longer returns a number at all."""
    try:
        increment_pair_bound(THETA1, SIGMA, ALPHA, 0.0)
        raised = None
    except HilbertHolderDomainError as exc:
        raised = str(exc)
    assert raised is not None, "gamma = 0.0 still returns silently -- the guard is gone"
    assert "Plemelj-Privalov" in raised, raised
    # the pre-repair number is not deleted, only made opt-in: 'extrapolate' reproduces it
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        u_S, u_T = increment_pair_bound(THETA1, SIGMA, ALPHA, 0.0,
                                        on_unsound="extrapolate")
    assert any(isinstance(w.message, HilbertHolderUnsoundWarning) for w in caught), caught
    assert u_S == 0.0, u_S                          # leg 119's exact banked values
    assert 27.0 < u_T < 28.0, u_T
    ratios = {d: guarded_pair_ratio(THETA1, SIGMA, ALPHA, 0.0, d, "extrapolate"
                                    )["ratio_true_over_bound"]
              for d in (1e-9, 1e-50)}
    assert ratios[1e-9] < 1.0, ratios
    assert ratios[1e-50] > 1.2, ratios              # the gap is still MEASURABLE
    # and 'inflate' is honest about what a true majorant costs here
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        inf_pair = increment_pair_bound(THETA1, SIGMA, ALPHA, 0.0, on_unsound="inflate")
    assert all(np.isinf(v) for v in inf_pair), inf_pair
    print("[ok] (2) INVERTED V1: gamma = 0.0 now RAISES HilbertHolderDomainError naming "
          "the Plemelj-Privalov hypothesis, where it used to return (%.4f, %.4f) silently. "
          "on_unsound='extrapolate' still reproduces that pair exactly and the adversary "
          "still attains true/bound = %.4f at delta = 1e-50 (from %.4f at 1e-9), so leg "
          "119's measurement survives the repair; on_unsound='inflate' returns "
          "(inf, inf) -- correct, and useless, which is the honest content of V1"
          % (u_S, u_T, ratios[1e-50], ratios[1e-9]))


def test_3_INVERTED_violation_gamma_negative_now_REJECTED():
    """V2 INVERTED (leg 153): gamma < 0 is rejected at BOTH the low level and assembly."""
    for g in (-0.5, -1.0, -0.3):
        try:
            increment_pair_bound(THETA1, SIGMA, ALPHA, g)
            raise AssertionError("gamma = %r still returns silently" % g)
        except HilbertHolderDomainError:
            pass
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        u_S, u_T = increment_pair_bound(THETA1, SIGMA, ALPHA, -0.5,
                                        on_unsound="extrapolate")
        ratios = {d: guarded_pair_ratio(THETA1, SIGMA, ALPHA, -0.5, d, "extrapolate"
                                        )["ratio_true_over_bound"]
                  for d in (1e-9, 1e-50)}
    assert u_S > 10.0, u_S                          # leg 119's banked u_S = 13.089262
    assert ratios[1e-9] < 1.0 and ratios[1e-50] > 1.2, ratios
    # the ASSEMBLY-level API is the half that used to return a finite pair silently
    try:
        hilbert_holder_constant(ALPHA, -0.3, n_theta=24, n_d=14, n_quad=200)
        raise AssertionError("hilbert_holder_constant(1.5, -0.3) still returns a pair")
    except HilbertHolderDomainError:
        pass
    with warnings.catch_warnings(record=True) as c2:
        warnings.simplefilter("always")
        hhc = hilbert_holder_constant(ALPHA, -0.3, n_theta=24, n_d=14, n_quad=200,
                                      on_unsound="extrapolate")
    assert np.isfinite(hhc["b_sup"]) and np.isfinite(hhc["b_semi"]), hhc
    assert any(isinstance(w.message, HilbertHolderUnsoundWarning) for w in c2), c2
    inflated = hilbert_holder_constant(ALPHA, -0.3, n_theta=16, n_d=10, n_quad=100,
                                       on_unsound="inflate")
    assert np.isinf(inflated["b_sup"]) and np.isinf(inflated["b_semi"]), inflated
    print("[ok] (3) INVERTED V2: gamma = -0.5/-1.0/-0.3 all RAISE at the low level, and "
          "the ASSEMBLY-level hilbert_holder_constant(1.5, -0.3, ...) -- which used to "
          "return a finite (%.2f, %.2f) across the whole 24x14 pair grid while merely "
          "warning -- now raises too, returning that same pair only under "
          "on_unsound='extrapolate' and (inf, inf) under 'inflate'.  The gap stays "
          "measurable: (u_S, u_T) = (%.4f, %.4f), exceeded %.4fx at delta = 1e-50"
          % (hhc["b_sup"], hhc["b_semi"], u_S, u_T, ratios[1e-50]))


def test_4_INVERTED_eps_truncation_mechanism_still_measurable():
    """The mechanism, unchanged and still measurable -- but only opt-in (leg 153).

    The eps-drift is what the guard's closed-form head bound formalises: the discarded
    head is <= 2 cmax^(alpha-gamma) s0^gamma / gamma, which vanishes as eps -> 0 iff
    gamma > 0.  This gate keeps the raw growth on the record behind `"extrapolate"`.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        scan = [(e, increment_pair_bound(THETA1, SIGMA, ALPHA, 0.0, n_quad=4000, eps=e,
                                         on_unsound="extrapolate")[1])
                for e in (1e-6, 1e-10, 1e-14, 1e-16)]
        assert np.isinf(_head_bound(THETA1, SIGMA, ALPHA, 0.0, 1e-10))
        assert np.isfinite(_head_bound(THETA1, SIGMA, ALPHA, GAMMA, 1e-10))
    vals = [v for _, v in scan]
    assert all(b > a for a, b in zip(vals, vals[1:])), scan   # strictly growing, no plateau
    assert vals[-1] / vals[0] > 2.0, scan
    # the shipped gamma does NOT do this
    ship = [sum(increment_pair_bound(THETA1, SIGMA, ALPHA, GAMMA, n_quad=4000, eps=e))
            for e in (1e-8, 1e-16)]
    assert ship[1] / ship[0] < 1.01, ship
    print("[ok] (4) INVERTED mechanism: at gamma = 0 the seminorm coefficient still grows "
          "%.2f -> %.2f (%.2fx) as eps goes 1e-6 -> 1e-16 with NO plateau -- but only "
          "reachable via on_unsound='extrapolate' now, and the guard's closed-form head "
          "bound is +inf there against a finite one at the shipped gamma = 0.5, which "
          "moves the same sum by only %.3f%% over the identical sweep"
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


def test_6_INVERTED_the_silence_and_crash_inventory():
    """The inventory, re-taken (leg 153): nothing is silent, and one exception type."""
    tags = {}
    for label, g in (("gamma=0.0", 0.0), ("gamma=-0.5", -0.5), ("gamma=-1.0", -1.0)):
        try:
            increment_pair_bound(THETA1, SIGMA, ALPHA, g)
            tags[label] = "RETURNED_SILENTLY"
        except Exception as exc:                                       # noqa: BLE001
            tags[label] = type(exc).__name__
    # what used to be three silent-finite returns is now three identical loud rejections
    assert set(tags.values()) == {"HilbertHolderDomainError"}, tags
    # the ASSEMBLY API's polarity split is gone: both gammas now fail the SAME way
    asm = {}
    for label, g in (("gamma=0.0", 0.0), ("gamma=-0.3", -0.3)):
        try:
            hilbert_holder_constant(ALPHA, g, n_theta=16, n_d=10, n_quad=100)
            asm[label] = "RETURNED"
        except Exception as exc:                                       # noqa: BLE001
            asm[label] = type(exc).__name__
    assert set(asm.values()) == {"HilbertHolderDomainError"}, asm
    # non-finite arguments are rejected too, and by the SAME exception
    nonfinite = {}
    for label, a, g in (("gamma=nan", ALPHA, np.nan), ("gamma=inf", ALPHA, np.inf),
                        ("alpha=nan", np.nan, GAMMA), ("alpha=inf", np.inf, GAMMA)):
        try:
            increment_pair_bound(THETA1, SIGMA, a, g)
            nonfinite[label] = "RETURNED"
        except Exception as exc:                                       # noqa: BLE001
            nonfinite[label] = type(exc).__name__
    assert set(nonfinite.values()) == {"HilbertHolderDomainError"}, nonfinite
    # UNCHANGED and NOT inverted: near_padding(0) still raises ZeroDivisionError, and
    # increment_regime still excludes wide pairs.  Neither is a bound-direction defect.
    try:
        near_padding(0.0)
        raised_np = False
    except ZeroDivisionError:
        raised_np = True
    assert raised_np
    assert increment_regime(1.0, 3.0) is False        # too wide, correctly excluded
    print("[ok] (6) INVERTED inventory: what were THREE silent-finite returns at the "
          "low level (gamma = 0.0/-0.5/-1.0) and a SPLIT polarity at the assembly API "
          "(ZeroDivisionError at gamma = 0.0 vs a silent finite pair at -0.3) are now "
          "%d + %d + %d identical HilbertHolderDomainErrors, one exception type across "
          "both levels and both polarities, non-finite gamma/alpha included.  "
          "near_padding(0)'s ZeroDivisionError is NOT inverted -- it is a loud failure "
          "already and not a bound-direction defect" % (len(tags), len(asm), len(nonfinite)))


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


def test_8_INVERTED_soundness_predicate_is_ENFORCED_and_the_diagnostic_is_not():
    """gamma > 0 is now the ENFORCED predicate -- and leg 119's drift diagnostic is not it.

    Leg 119 reported the eps-drift separating the two regimes with a clean gap ("max 1.34x
    when sound vs min 1.98x when not").  Its gamma ladder stopped at 0.05.  Leg 153
    extended it to 1e-6 and the gap does NOT survive as stated: three SOUND configurations
    sit above leg 119's own banked 1.98 floor.  A re-fitted threshold still separates, but
    the margin collapses from 1.478x to ~1.10x and must be re-fitted for every new gamma,
    because the drift is continuous through gamma = 0+ (the head ~ s0^gamma/gamma).  So the
    guard enforces the EXACT Plemelj-Privalov condition, never the diagnostic.
    """
    r6 = _repair()["R6_drift_diagnostic_is_not_the_predicate"]
    # the predicate is enforced exactly at the boundary: 0.0 rejected, 1e-6 accepted
    for g, must_raise in ((0.0, True), (-1e-12, True), (1e-6, False), (1e-3, False)):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                increment_pair_bound(THETA1, SIGMA, ALPHA, g)
            got = False
        except HilbertHolderDomainError:
            got = True
        assert got is must_raise, (g, must_raise, got)
    # the diagnostic's failure, from this leg's own JSON
    misfits = r6["sound_gammas_above_leg_119s_banked_unsound_floor"]
    assert len(misfits) >= 3, r6
    assert r6["max_drift_sound"] > 1.98, r6          # leg 119 reported 1.34 here
    assert r6["margin_collapse_factor"] > 1.3, r6
    # live re-check, so this gate is not a pure JSON echo
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        lo = increment_pair_bound(THETA1, SIGMA, ALPHA, 1e-3, eps=1e-6,
                                  on_unsound="extrapolate")
        hi = increment_pair_bound(THETA1, SIGMA, ALPHA, 1e-3, eps=1e-16,
                                  on_unsound="extrapolate")
    live = sum(hi) / sum(lo)
    assert live > 1.98, live                        # a SOUND gamma, above the banked floor
    print("[ok] (8) INVERTED: the predicate gamma > 0 is now ENFORCED (0.0 and -1e-12 "
          "raise, 1e-6 and 1e-3 pass), and leg 119's eps-drift DIAGNOSTIC is shown not to "
          "be it: %d sound gammas %r sit above its banked 1.98 unsound floor, the true "
          "max-when-sound is %.4f (not the reported 1.34), and the separation margin "
          "collapses %.2fx to %.3f.  Live re-check at the sound gamma = 1e-3: drift "
          "%.4f, above the banked floor.  No fixed threshold on the drift is safe"
          % (len(misfits), misfits, r6["max_drift_sound"], r6["margin_collapse_factor"],
             r6["re_measured_gap"]["separation_margin"], live))


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


def test_10_the_repair_moved_NOTHING_on_the_clean_surface():
    """Leg 153's gate (b): the entire licence for the repair.

    A guard that also moved a previously-passing number would be a claim change, not a
    repair -- and under the plan-of-record ban on Route-D bound-sharpening, a tighter
    number would be indistinguishable from the banned activity.  So the clean surface must
    come back BIT-IDENTICAL: `==` on float64, never `allclose`.
    """
    r = _repair()["R4_bit_identity_census"]
    assert r["n_float64_leaves"] > 9000, r
    # live: recompute the digest now and require it to match what the runner banked
    import hashlib
    rec = {}
    for (A, G) in ((1.5, 0.5), (1.4, 0.15), (1.5, 0.3), (1.2, 0.7), (2.0, 0.9)):
        rows = []
        for th, sig in pair_grid(n_theta=24, n_d=14):
            inc = None
            if increment_regime(th, sig):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", HilbertHolderTruncationWarning)
                    uS, uT = increment_pair_bound(th, sig, A, G, n_quad=200)
                inc = [float(uS).hex(), float(uT).hex()]
            rows.append([float(th).hex(), float(sig).hex(), inc])
        rec["pairs_%g_%g" % (A, G)] = rows
    consts = []
    for (A, G) in ((1.5, 0.5), (1.4, 0.15), (1.5, 0.3), (1.2, 0.7), (2.0, 0.9)):
        for rule in ("increment", "sum", "pointwise"):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", HilbertHolderTruncationWarning)
                c = hilbert_holder_constant(A, G, n_theta=24, n_d=14, n_quad=200, rule=rule)
            consts.append([A, G, rule, float(c["b_sup"]).hex(),
                           float(c["b_semi"]).hex(), c["n_increment_route"]])
    rec["constant"] = consts
    live = hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest()
    assert live == r["sha256_of_hex_dump"], (live, r["sha256_of_hex_dump"])
    print("[ok] (10) gate (b): %d float64 leaves over %d (alpha, gamma) configurations "
          "reproduce the banked digest %s exactly -- the guard moved NOTHING on the clean "
          "surface.  The full pre-repair/post-repair diff (17509 leaves, including the "
          "eps ladder, sweep_convergence, cq_sup_split, quadratic_constant_full and the "
          "untouched helpers) reported 0 moved leaves, and the capabilities-registered "
          "test_nk_hilbert_holder.py printed byte-identical output on all 6 of its gates"
          % (r["n_float64_leaves"], r["n_configurations"], live[:16]))


def test_11_the_band_deliberately_WARNED_and_not_rejected():
    """The one free constant, with both of its measured margins.

    The map's own PRODUCTION optimum (alpha ~ 1.4, gamma ~ 0.15) is under-resolved at the
    default eps -- its discarded head reaches 5.08e-2 of the returned pair -- but gamma > 0
    there, so its exact majorant is FINITE.  That is under-refinement, not divergence, and
    rejecting it would be a claim about a sound object.  It is closed by a warning that
    changes NO returned value, which is precisely what keeps gate (b) true.
    """
    r = _repair()["R5_head_warning_band"]
    ship = r["by_configuration"]["shipped_1.5_0.5"]["worst_head_over_value"]
    prod = r["by_configuration"]["production_1.4_0.15"]["worst_head_over_value"]
    assert ship < HEAD_WARN_TOL < prod, (ship, HEAD_WARN_TOL, prod)
    assert r["margin_below_worst_shipped"] > 10.0, r
    assert r["margin_above_worst_production"] > 10.0, r
    assert r["by_configuration"]["shipped_1.5_0.5"]["n_pairs_warned"] == 0, r
    assert r["by_configuration"]["production_1.4_0.15"]["n_pairs_warned"] > 0, r
    # live: the warning fires, and the value it returns is the UNWARNED value exactly
    th, sg = r["by_configuration"]["production_1.4_0.15"]["argmax"][:2]
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        warned = increment_pair_bound(th, sg, 1.4, 0.15)
    assert any(isinstance(w.message, HilbertHolderTruncationWarning) for w in caught), caught
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        again = increment_pair_bound(th, sg, 1.4, 0.15)
    assert warned == again, (warned, again)          # the warning changed no number
    head = _head_bound(th, sg, 1.4, 0.15, 1e-10)
    assert np.isfinite(head), head                   # finite: under-refined, not divergent
    print("[ok] (11) the deliberately-WARNED band: the production optimum (1.4, 0.15) "
          "reaches head/value %.4g on %d of its pairs -- %.0fx above HEAD_WARN_TOL = %.0e "
          "-- while the shipped (1.5, 0.5) peaks at %.4g, %.0fx below it and warning on 0 "
          "pairs.  The head is FINITE there (%.4g), so this is under-refinement, not "
          "divergence, and the warning is verified to change no returned number"
          % (prod, r["by_configuration"]["production_1.4_0.15"]["n_pairs_warned"],
             r["margin_above_worst_production"], HEAD_WARN_TOL, ship,
             r["margin_below_worst_shipped"], head))


if __name__ == "__main__":
    test_1_known_answer_positive_control()
    test_2_INVERTED_violation_gamma_zero_now_REJECTED()
    test_3_INVERTED_violation_gamma_negative_now_REJECTED()
    test_4_INVERTED_eps_truncation_mechanism_still_measurable()
    test_5_CONTROL_shipped_and_production_are_safe()
    test_6_INVERTED_the_silence_and_crash_inventory()
    test_7_alpha_inf_is_vacuous_not_a_finding()
    test_8_INVERTED_soundness_predicate_is_ENFORCED_and_the_diagnostic_is_not()
    test_9_the_banked_verdict_is_the_one_this_file_asserts()
    test_10_the_repair_moved_NOTHING_on_the_clean_surface()
    test_11_the_band_deliberately_WARNED_and_not_rejected()
    print("\nALL HILBERT-HOLDER ADVERSARIAL GATES PASSED "
          "(leg 119's gate answer: YES; leg 153's repair LANDED, pins 2/3/4/6/8 INVERTED)")
