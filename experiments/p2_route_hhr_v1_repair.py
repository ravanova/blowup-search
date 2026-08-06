"""Route-HHR (leg 153): the domain guard lands on solver/hilbert_holder.py.

Leg 119 (Route-HHA) answered its gate YES and ESCALATED rather than patching: two entirely
NaN-free configurations of `gamma` make `increment_pair_bound` return a finite,
plausible-looking `(u_S, u_T)` that an explicit adversarial `h` EXCEEDS by up to 1.2311x.
This leg is the authorised repair, following the leg 130 / `hilbert_pointwise.py` precedent
exactly: on the failing configuration, either reject the input loudly or return a bound
verified to dominate -- NEVER a sharpened bound.

    GATE (verbatim, DIRECTION.md 153 -- ROUTE-HHR).  Post-repair: (a) does
    hilbert_holder.py's reported bound now either raise on the failing configuration or
    provably dominate the true value there, with the PIN inverted, and (b) is the module
    bit-identical on every previously-passing case, including any capabilities.py validated
    line?

Clause (b) is the ENTIRE LICENCE for the repair.  If any clean-input result moves at all --
`==` on float64, not `allclose` -- this leg escalates and does NOT iterate.  So the runner's
centrepiece is R4: a float64-hex census of every value on the declared bit-identity surface,
captured from the pre-repair module and re-captured after the guard.

The plan-of-record ban "another Route-D bound-sharpening leg" applies literally: every effect
of this leg is a REJECTION, a WARNING, or an INFLATION.  No constant gets smaller.

Run: .venv/bin/python experiments/p2_route_hhr_v1_repair.py     (~3 min)
Writes: writeup/data/p2_route_hhr_v1_repair.json
"""

import json
import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.hilbert_holder import (                                     # noqa: E402
    HEAD_WARN_TOL, HilbertHolderDomainError, HilbertHolderTruncationWarning,
    HilbertHolderUnsoundWarning, _head_bound, hilbert_holder_constant,
    increment_pair_bound, increment_regime, pair_grid, wrap)
from experiments.p2_route_hha_v1_adversarial import (                   # noqa: E402
    ALPHA, GAMMA, T_seminorm, psi_generic)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_hhr_v1_repair.json")

THETA1, SIGMA = 1.0, 0.05          # leg 119's pair; every violation is stated here
SHIPPED = (1.5, 0.5)               # the shipped Route-D configuration
PRODUCTION = (1.4, 0.15)           # the (alpha, gamma) map's own production optimum

#: leg 119's two banked violators, plus the rest of the gamma <= 0 family it probed.
FAILING = [("V1_gamma_0.0", 0.0), ("V2_gamma_-0.5", -0.5),
           ("gamma_-1.0", -1.0), ("gamma_-0.3", -0.3)]


def guarded_pair_ratio(theta1, sigma, alpha, gamma, delta, on_unsound,
                       n_quad=4000, eps=1e-10):
    """leg 119's `pair_ratio`, with the guard policy threaded through.

    Identical arithmetic to `experiments.p2_route_hha_v1_adversarial.pair_ratio` (which
    this leg's territory does not include and does not edit); the only difference is that
    `on_unsound` reaches `increment_pair_bound`, so the post-guard battery can keep
    MEASURING leg 119's gap under `"extrapolate"` instead of deleting the measurement.
    """
    th2 = theta1 + sigma
    dphi_true = abs(psi_generic(theta1, theta1, delta, alpha)
                    - psi_generic(th2, theta1, delta, alpha))
    S = 1.0
    T = T_seminorm(theta1, delta, alpha, gamma)
    uS, uT = increment_pair_bound(theta1, sigma, alpha, gamma, n_quad=n_quad, eps=eps,
                                  on_unsound=on_unsound)
    w = np.cos(0.5 * min(abs(theta1), abs(th2))) ** -(1.0 - gamma)
    lhs = w * dphi_true / abs(sigma) ** gamma
    bound = uS * S + uT * T
    return {"delta": delta, "S": S, "T": T, "u_S": float(uS), "u_T": float(uT),
            "true_weighted_increment": float(lhs), "bound": float(bound),
            "ratio_true_over_bound": float(lhs / bound) if bound > 0 else float("inf")}


def _outcome(fn):
    """Value, or a tag naming the exception -- never a boolean.  Lesson: magnitudes."""
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            v = fn()
        tag = ("|WARN:" + ";".join(sorted({type(w.message).__name__ for w in caught}))
               if caught else "")
        if isinstance(v, tuple):
            return {"returned": [float(x) for x in v], "raised": None, "warned": tag}
        return {"returned": v, "raised": None, "warned": tag}
    except Exception as exc:                                            # noqa: BLE001
        return {"returned": None, "raised": type(exc).__name__,
                "message_head": str(exc)[:180]}


# ---------------------------------------------------------------------------
# R1 -- the guard fires on every configuration leg 119 banked as failing
# ---------------------------------------------------------------------------


def r1_guard_fires():
    low, asm = {}, {}
    for label, g in FAILING:
        low[label] = _outcome(lambda g=g: increment_pair_bound(THETA1, SIGMA, ALPHA, g))
        asm[label] = _outcome(
            lambda g=g: hilbert_holder_constant(ALPHA, g, n_theta=16, n_d=10, n_quad=100))
    for label, a, g in (("gamma_nan", ALPHA, np.nan), ("gamma_inf", ALPHA, np.inf),
                        ("alpha_nan", np.nan, GAMMA), ("alpha_inf", np.inf, GAMMA)):
        low[label] = _outcome(
            lambda a=a, g=g: increment_pair_bound(THETA1, SIGMA, a, g))
        asm[label] = _outcome(
            lambda a=a, g=g: hilbert_holder_constant(a, g, n_theta=16, n_d=10, n_quad=100))
    # and the sound configurations must NOT be rejected
    sound = {}
    for label, (a, g) in (("shipped_1.5_0.5", SHIPPED), ("production_1.4_0.15", PRODUCTION),
                          ("gamma_1e-3", (ALPHA, 1e-3)), ("gamma_0.01", (ALPHA, 0.01)),
                          ("gamma_0.05", (ALPHA, 0.05)), ("gamma_0.9", (ALPHA, 0.9))):
        sound[label] = _outcome(
            lambda a=a, g=g: increment_pair_bound(THETA1, SIGMA, a, g))
    n_rej = sum(1 for v in low.values() if v["raised"] == "HilbertHolderDomainError")
    n_sound_rej = sum(1 for v in sound.values() if v["raised"] is not None)
    return {"low_level_increment_pair_bound": low,
            "assembly_hilbert_holder_constant": asm,
            "sound_configurations_must_pass": sound,
            "n_failing_rejected_at_low_level": n_rej,
            "n_failing_probed": len(low),
            "n_sound_wrongly_rejected": n_sound_rej,
            "note": ("pre-repair, ALL of these returned silently at the low level and the "
                     "assembly API was differently unsafe: gamma=0.0 died with a bare "
                     "ZeroDivisionError inside nk_seminorm.hilbert_split_bound's own "
                     "/gamma, while gamma=-0.3 returned a finite (46.7564, 4.9190).  "
                     "Neither polarity was safe; they were just differently unsafe.")}


# ---------------------------------------------------------------------------
# R2 -- the "inflate" policy returns a pair that TRULY dominates
# ---------------------------------------------------------------------------


def r2_inflate_dominates():
    unbounded = {}
    for label, g in FAILING:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            uS, uT = increment_pair_bound(THETA1, SIGMA, ALPHA, g, on_unsound="inflate")
        unbounded[label] = {"u_S": float(uS), "u_T": float(uT),
                            "head_bound": float(_head_bound(THETA1, SIGMA, ALPHA, g, 1e-10)),
                            "both_infinite": bool(np.isinf(uS) and np.isinf(uT))}
    # on an ACCEPTED-but-warned configuration, inflate must exceed raw by exactly the head
    accepted = {}
    for label, (a, g) in (("production_1.4_0.15", PRODUCTION), ("shipped_1.5_0.5", SHIPPED)):
        th, sg = 3.1305223634, -1.19
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            rS, rT = increment_pair_bound(th, sg, a, g)
            head = _head_bound(th, sg, a, g, 1e-10)
        accepted[label] = {"theta1": th, "sigma": sg, "raw": [float(rS), float(rT)],
                           "head": float(head),
                           "inflated_would_be": [float(rS + head), float(rT + head)],
                           "inflation_factor_on_sum": float((rS + rT + 2 * head)
                                                            / (rS + rT))}
    return {"gamma_le_0_is_honestly_unbounded": unbounded, "accepted_pairs": accepted,
            "why": ("the head's split between the S and T accounts is unknown, so inflate "
                    "adds it to BOTH coefficients -- valid because h_S S + h_T T <= "
                    "head (S + T) for S, T >= 0.  At gamma <= 0 the head is +inf, so the "
                    "honest dominating pair is (inf, inf): correct, and useless, which is "
                    "the entire content of leg 119's V1/V2.")}


# ---------------------------------------------------------------------------
# R3 -- "extrapolate" reproduces the pre-repair number BIT-IDENTICALLY
# ---------------------------------------------------------------------------


def r3_extrapolate_preserves_the_measurement():
    """Leg 119's banked numbers, re-measured through the guard's escape hatch."""
    rows = []
    for label, g in FAILING:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            uS, uT = increment_pair_bound(THETA1, SIGMA, ALPHA, g,
                                          on_unsound="extrapolate")
        rows.append({"case": label, "gamma": g, "u_S": float(uS), "u_T": float(uT),
                     "u_S_hex": float(uS).hex(), "u_T_hex": float(uT).hex(),
                     "warned": sorted({type(w.message).__name__ for w in caught})})
    # leg 119's own eps ladder, still measurable after the repair
    ladder = {}
    for label, g in (("gamma_0.0", 0.0), ("gamma_-0.5", -0.5), ("shipped_gamma_0.5", 0.5)):
        vals = []
        for e in (1e-6, 1e-8, 1e-10, 1e-12, 1e-14, 1e-16):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                u = increment_pair_bound(THETA1, SIGMA, ALPHA, g, n_quad=4000, eps=e,
                                         on_unsound="extrapolate")
            vals.append({"eps": e, "u_S": float(u[0]), "u_T": float(u[1])})
        ladder[label] = {"rows": vals,
                         "drift_sum_1e-16_over_1e-6":
                             float((vals[-1]["u_S"] + vals[-1]["u_T"])
                                   / (vals[0]["u_S"] + vals[0]["u_T"]))}
    # and the adversary itself: the ratio leg 119 measured is UNCHANGED under extrapolate
    adv = {}
    for label, g in (("V1_gamma_0.0", 0.0), ("V2_gamma_-0.5", -0.5)):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            adv[label] = [guarded_pair_ratio(THETA1, SIGMA, ALPHA, g, d, "extrapolate")
                          for d in (1e-9, 1e-30, 1e-50)]
    return {"banked_pairs_reproduced": rows, "eps_ladder": ladder,
            "adversary_under_extrapolate": adv,
            "worst_ratio_still_measurable":
                float(max(r["ratio_true_over_bound"]
                          for rows_ in adv.values() for r in rows_)),
            "why": ("leg 130's precedent, its own words: the escape hatch is what lets the "
                    "original battery keep MEASURING the gap after the guard lands, "
                    "instead of the repair deleting its own evidence.")}


# ---------------------------------------------------------------------------
# R4 -- gate (b): the bit-identity census
# ---------------------------------------------------------------------------


def r4_bit_identity(configs=((1.5, 0.5), (1.4, 0.15), (1.5, 0.3), (1.2, 0.7), (2.0, 0.9))):
    """Every value on the declared clean surface, as float64 hex.

    The pre-repair capture lives in this leg's journal as a SHA-pinned procedure: run this
    function on the module at the merge base, then again after the guard, and diff with
    `==`.  The digest recorded here is what the two runs must agree on leaf for leaf.
    """
    rec, n = {}, 0
    for (A, G) in configs:
        rows = []
        for th, sig in pair_grid(n_theta=24, n_d=14):
            inc = None
            if increment_regime(th, sig):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", HilbertHolderTruncationWarning)
                    uS, uT = increment_pair_bound(th, sig, A, G, n_quad=200)
                inc = [float(uS).hex(), float(uT).hex()]
            rows.append([float(th).hex(), float(sig).hex(), inc])
            n += 2 + (2 if inc else 0)
        rec["pairs_%g_%g" % (A, G)] = rows
    consts = []
    for (A, G) in configs:
        for rule in ("increment", "sum", "pointwise"):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", HilbertHolderTruncationWarning)
                r = hilbert_holder_constant(A, G, n_theta=24, n_d=14, n_quad=200, rule=rule)
            consts.append([A, G, rule, float(r["b_sup"]).hex(),
                           float(r["b_semi"]).hex(), r["n_increment_route"]])
            n += 3
    rec["constant"] = consts
    blob = json.dumps(rec, sort_keys=True)
    return {"n_float64_leaves": n, "n_configurations": len(configs),
            "sha256_of_hex_dump": __import__("hashlib").sha256(blob.encode()).hexdigest(),
            "surfaces": sorted(rec),
            "note": ("the full leaf-by-leaf diff (17509 leaves over 10 surface groups, "
                     "including the eps ladder, sweep_convergence, cq_sup_split, "
                     "quadratic_constant_full, conjugate, weighted_seminorm, wrap, "
                     "near_padding and decomposition_exact) is reported in the journal; "
                     "this digest is the reproducible core of it.")}


# ---------------------------------------------------------------------------
# R5 -- the one free constant: HEAD_WARN_TOL, and both of its measured margins
# ---------------------------------------------------------------------------


def r5_head_warning_band():
    out = {}
    for label, (A, G) in (("shipped_1.5_0.5", SHIPPED),
                          ("production_1.4_0.15", PRODUCTION)):
        worst, arg, n_warn, n = 0.0, None, 0, 0
        for th, sig in pair_grid(n_theta=24, n_d=14):
            if not increment_regime(th, sig):
                continue
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", HilbertHolderTruncationWarning)
                uS, uT = increment_pair_bound(th, sig, A, G, n_quad=200)
            head = _head_bound(th, sig, A, G, 1e-10)
            tot = uS + uT
            n += 1
            if tot > 0.0:
                r = head / tot
                if r > HEAD_WARN_TOL:
                    n_warn += 1
                if r > worst:
                    worst, arg = r, [float(th), float(sig), float(uS), float(uT),
                                     float(head)]
        out[label] = {"n_pairs": n, "worst_head_over_value": float(worst),
                      "argmax": arg, "n_pairs_warned": n_warn,
                      "fraction_warned": float(n_warn) / n if n else 0.0}
    # THE CONTROL (lesson 90: what would have had to change for the other answer?).
    # "Under-refinement, not divergence" is a claim that REFINING fixes it.  So drive eps
    # down: at a sound gamma the head/value must collapse; at gamma <= 0 it must not.
    refine = {}
    for label, g in (("production_gamma_0.15", 0.15), ("shipped_gamma_0.5", 0.5),
                     ("UNSOUND_gamma_0.0", 0.0), ("UNSOUND_gamma_-0.5", -0.5)):
        th, sg, a = 3.1305223634, -1.19, 1.4
        rows = []
        for e in (1e-10, 1e-20, 1e-30, 1e-40):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                uS, uT = increment_pair_bound(th, sg, a, g, n_quad=200, eps=e,
                                              on_unsound="extrapolate")
            head = _head_bound(th, sg, a, g, e)
            tot = uS + uT
            rows.append({"eps": e, "head": float(head), "value": float(tot),
                         "head_over_value": float(head / tot) if tot > 0 else None})
        # The claim under test is about the HEAD -- the closed-form quantity -- because
        # `_raw`'s own float64 arithmetic returns NaN at this wide pair below eps ~ 1e-20
        # (a PRE-EXISTING limit of the module, untouched by this leg: repairing it would
        # move numbers).  So the control reads the head, and records the NaN separately.
        h0, h1 = rows[0]["head"], rows[-1]["head"]
        refine[label] = {"rows": rows, "head_at_eps_1e-10": float(h0),
                         "head_at_eps_1e-40": float(h1),
                         "head_shrink_factor":
                             float(h0 / h1) if np.isfinite(h0) and h1 > 0 else None,
                         "head_vanishes_under_refinement": bool(np.isfinite(h1)),
                         "resolved_by_refinement": bool(
                             np.isfinite(h1) and h1 < HEAD_WARN_TOL * rows[0]["value"]),
                         "raw_value_went_nan_below_eps":
                             next((r["eps"] for r in rows
                                   if not np.isfinite(r["value"])), None)}
    ship = out["shipped_1.5_0.5"]["worst_head_over_value"]
    prod = out["production_1.4_0.15"]["worst_head_over_value"]
    return {"by_configuration": out, "refinement_control": refine,
            "HEAD_WARN_TOL": HEAD_WARN_TOL,
            "margin_below_worst_shipped": float(HEAD_WARN_TOL / ship),
            "margin_above_worst_production": float(prod / HEAD_WARN_TOL),
            "production_over_shipped": float(prod / ship),
            "why_warn_not_reject": ("gamma = 0.15 > 0, so the exact majorant is FINITE "
                                    "here: this is under-refinement, not divergence.  "
                                    "Rejecting it would be a claim about a sound object, "
                                    "and leg 119 separately measured true/bound = 0.1081 "
                                    "at this configuration -- a ~9x margin the head does "
                                    "not close.  The warning changes NO returned value, "
                                    "which is what keeps gate (b) true.")}


# ---------------------------------------------------------------------------
# R6 -- the correction to leg 119's eps-drift DIAGNOSTIC (not to its verdict)
# ---------------------------------------------------------------------------


def r6_drift_diagnostic_is_not_the_predicate():
    rows = []
    for g in (-1.0, -0.5, -0.1, 0.0, 1e-6, 1e-3, 0.01, 0.05, 0.15, 0.5, 0.9, 1.5):
        vals = []
        for e in (1e-6, 1e-16):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                u = increment_pair_bound(THETA1, SIGMA, ALPHA, g, eps=e,
                                         on_unsound="extrapolate")
            vals.append(float(u[0] + u[1]))
        rows.append({"gamma": g, "sound_by_predicate": bool(g > 0.0),
                     "u_sum_eps_1e-6": vals[0], "u_sum_eps_1e-16": vals[1],
                     "drift": float(vals[1] / vals[0])})
    sound = [r["drift"] for r in rows if r["sound_by_predicate"]]
    unsound = [r["drift"] for r in rows if not r["sound_by_predicate"]]
    # reading A: against leg 119's OWN BANKED threshold (its quoted unsound floor, 1.98)
    vs_banked = [r["gamma"] for r in rows if r["sound_by_predicate"] and r["drift"] > 1.98]
    # reading B: against a threshold RE-FITTED to this leg's own extended ladder
    margin_119 = 1.98 / 1.34
    margin_here = min(unsound) / max(sound)
    return {"rows": rows, "max_drift_sound": float(max(sound)),
            "min_drift_unsound": float(min(unsound)),
            "leg_119_claimed_gap": {"max_when_sound": 1.34, "min_when_unsound": 1.98,
                                    "gamma_ladder_floor": 0.05,
                                    "separation_margin": float(margin_119)},
            "re_measured_gap": {"max_when_sound": float(max(sound)),
                                "min_when_unsound": float(min(unsound)),
                                "gamma_ladder_floor": 1e-6,
                                "separation_margin": float(margin_here)},
            "margin_collapse_factor": float(margin_119 / margin_here),
            "sound_gammas_above_leg_119s_banked_unsound_floor": vs_banked,
            "n_sound_misclassified_against_leg_119s_banked_threshold": len(vs_banked),
            "n_sound_misclassified_against_a_refitted_threshold":
                len([r for r in rows if r["sound_by_predicate"]
                     and r["drift"] > min(unsound)]),
            "finding": ("leg 119's ladder stopped at gamma = 0.05 and reported a clean gap "
                        "(max 1.34x sound vs min 1.98x unsound, a 1.478x separation "
                        "margin).  Extending the ladder to gamma = 1e-6 collapses that "
                        "margin to 1.103x -- and the true max-when-sound is 2.3816, not "
                        "1.34, so THREE sound configurations (gamma = 1e-6, 1e-3, 0.01) "
                        "sit ABOVE leg 119's banked 1.98 unsound floor and would be "
                        "rejected by a guard using its numbers.  A threshold re-fitted to "
                        "this ladder still separates, but by 1.103x, and it must be "
                        "re-fitted again for every new gamma probed: the drift is "
                        "continuous through gamma = 0+, because the discarded head ~ "
                        "s0^gamma/gamma -> inf there, so NO fixed threshold is safe.  The "
                        "drift is a good DIAGNOSTIC and a bad PREDICATE; the guard uses "
                        "the exact Plemelj-Privalov condition instead.  This corrects leg "
                        "119's diagnostic commentary, NOT its verdict -- its verdict rests "
                        "on the exact predicate, which stands.")}


# ---------------------------------------------------------------------------
# R7 -- the blast-radius control, re-run through the guard
# ---------------------------------------------------------------------------


def r7_blast_radius_control():
    out = {}
    for label, (A, G) in (("shipped_1.5_0.5", SHIPPED),
                          ("production_1.4_0.15", PRODUCTION)):
        rows = []
        for th, sg in ((0.2, 0.02), (1.0, 0.05), (2.5, 0.05), (3.0, 0.02)):
            for d in (1e-9, 1e-20, 1e-30, 1e-40, 1e-50):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    r = guarded_pair_ratio(th, sg, A, G, d, "raise")
                rows.append({"theta1": th, "sigma": sg, **r})
        out[label] = {"rows": rows,
                      "max_ratio_over_all_pairs":
                          float(max(r["ratio_true_over_bound"] for r in rows)),
                      "n_rejected_by_guard": 0}
    return {"by_configuration": out,
            "reading": ("the guard accepts every one of these -- gamma > 0 -- and the "
                        "adversary never exceeds the bound at any of them.  The ratio "
                        "falls TOWARD ZERO as the feature narrows, the opposite "
                        "asymptotics from the rejected gamma <= 0 rows, exactly as leg 119 "
                        "measured pre-repair.")}


# ---------------------------------------------------------------------------


def main():
    warnings.simplefilter("ignore", HilbertHolderUnsoundWarning)
    rec = {
        "leg": 153, "route": "ROUTE-HHR", "repairs": "solver/hilbert_holder.py",
        "repairs_finding_of_leg": 119, "precedent": "leg 130 / solver/hilbert_pointwise.py",
        "gate": ("Post-repair: (a) does hilbert_holder.py's reported bound now either raise "
                 "on the failing configuration or provably dominate the true value there, "
                 "with the PIN inverted, and (b) is the module bit-identical on every "
                 "previously-passing case, including any capabilities.py validated line?"),
        "predicate": "gamma > 0, plus finiteness of the arguments and eps in (0, 1)",
        "R1_guard_fires_on_every_failing_configuration": r1_guard_fires(),
        "R2_inflate_returns_a_dominating_pair": r2_inflate_dominates(),
        "R3_extrapolate_preserves_leg_119s_measurement":
            r3_extrapolate_preserves_the_measurement(),
        "R4_bit_identity_census": r4_bit_identity(),
        "R5_head_warning_band": r5_head_warning_band(),
        "R6_drift_diagnostic_is_not_the_predicate": r6_drift_diagnostic_is_not_the_predicate(),
        "R7_blast_radius_control": r7_blast_radius_control(),
    }
    with open(OUT, "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True, default=str)
    r1 = rec["R1_guard_fires_on_every_failing_configuration"]
    r5 = rec["R5_head_warning_band"]
    r6 = rec["R6_drift_diagnostic_is_not_the_predicate"]
    print("wrote %s" % OUT)
    print("R1  guard rejects %d/%d failing configurations at the low level; "
          "%d/%d sound configurations wrongly rejected"
          % (r1["n_failing_rejected_at_low_level"], r1["n_failing_probed"],
             r1["n_sound_wrongly_rejected"], len(r1["sound_configurations_must_pass"])))
    print("R3  leg 119's worst adversary ratio still measurable under 'extrapolate': %.4f"
          % rec["R3_extrapolate_preserves_leg_119s_measurement"]["worst_ratio_still_measurable"])
    print("R4  bit-identity digest over %d float64 leaves: %s"
          % (rec["R4_bit_identity_census"]["n_float64_leaves"],
             rec["R4_bit_identity_census"]["sha256_of_hex_dump"][:16]))
    print("R5  worst head/value: shipped %.4g (warns on %d/%d pairs), production %.4g "
          "(warns on %d/%d); HEAD_WARN_TOL %.0e sits %.0fx above shipped and %.0fx below "
          "production"
          % (r5["by_configuration"]["shipped_1.5_0.5"]["worst_head_over_value"],
             r5["by_configuration"]["shipped_1.5_0.5"]["n_pairs_warned"],
             r5["by_configuration"]["shipped_1.5_0.5"]["n_pairs"],
             r5["by_configuration"]["production_1.4_0.15"]["worst_head_over_value"],
             r5["by_configuration"]["production_1.4_0.15"]["n_pairs_warned"],
             r5["by_configuration"]["production_1.4_0.15"]["n_pairs"],
             HEAD_WARN_TOL, r5["margin_below_worst_shipped"],
             r5["margin_above_worst_production"]))
    print("R5c CONTROL, head at eps 1e-10 -> 1e-40: " + "; ".join(
        "%s %s%s" % (k, ("shrinks %.4gx" % v["head_shrink_factor"])
                     if v["head_shrink_factor"] else "stays +inf",
                     " RESOLVED" if v["resolved_by_refinement"] else " NOT-RESOLVED")
        for k, v in sorted(r5["refinement_control"].items())))
    print("R6  drift diagnostic: leg 119's banked threshold misclassifies %d SOUND gammas "
          "%r; its separation margin collapses %.2fx (1.478 -> %.3f) once the ladder "
          "reaches gamma = 1e-6, where max-when-sound is %.4f not 1.34"
          % (r6["n_sound_misclassified_against_leg_119s_banked_threshold"],
             r6["sound_gammas_above_leg_119s_banked_unsound_floor"],
             r6["margin_collapse_factor"], r6["re_measured_gap"]["separation_margin"],
             r6["max_drift_sound"]))


if __name__ == "__main__":
    main()
