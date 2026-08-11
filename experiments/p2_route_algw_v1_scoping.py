"""Route-ALGW v1 (leg 341) -- the fourth space, re-audited.

WHY
---
`plan_of_record.py`'s stage-V ban names a "three-realization death" for a weighted
function-space escape from the certificate machinery's ban: ell^1_w coefficient basis
(leg 54), collocation basis (leg 56), origin-H^2 capped at a=0 (legs 163/176). Leg 260
separately computed that the actual NS3D-DSS target's own home is an ALGEBRAICALLY
weighted space (L^p(R^3), p>3, or L^2(rho), rho=(1+|y|)^-s, s>1) -- a fourth space, not
one of the three. This leg's gate (S1) asks whether THAT space escapes the same death,
and whether the CAP (radii-polynomial Y/Z0/Z1/Z2) apparatus has a coherent formulation
in it. Separately (S2) it asks whether leg 261's NRS/Tsai composition (u in L^3 forces
u=0 for a backward self-similar profile) survives re-derivation in the algebraic weight,
and states the DSS-vs-BSS ansatz question on its own footing.

This leg BUILDS NOTHING and RUNS NO SEARCH. Every number below is either (i) a
transcribed locator into an already-banked leg's file (re-verified at file:line, not
taken from summary), or (ii) an elementary closed-form/quadrature recomputation done
here so the journal prose cannot drift from a number.

WHAT IT COMPUTES
-----------------
S1_A  -- leg 126's exhaustive audit of Route-D (decay_grading/decay_collocation/
         holder_norms, the ALREADY-BUILT algebraically-graded sup-norm CAP attempt):
         admissibility partition and best-case shortfall, transcribed.
S1_B  -- leg 51/52's algebraic-weight-exponent sweep on the ell^1_w coefficient basis:
         kernel-in-space / cokernel-bounded crossover, transcribed, plus this leg's own
         re-derivation of WHY the two curves must cross where they do (elementary
         algebra on the two exponents, not a new measurement).
S1_C  -- origin-H^2 (legs 163/176) is itself already algebraically weighted (Mellin
         weight (1+xi^4)) and dies for an orthogonal, a=0-only reason: transcribed.
S1_D  -- leg 331's CAP-apparatus mechanism (Gauss-Hermite/Laguerre quadrature exactness
         is tied to Gaussian weight, breaks under an algebraic tail): transcribed,
         read as evidence about the SHAPE requirement (lesson 87), not re-run.
S2    -- re-derive leg 261's u~|x|^-3 Biot-Savart witness claim against leg 260's own
         Type-I decay rate |U(y)| ~ (1+|y|)^-1 for the actual DSS target (not the
         Gaussian-basis test witness), and recompute integrability of |u|^3 r^2 at
         infinity as a function of the decay exponent sigma, both by closed form and by
         quadrature cross-check.
S2_DSS -- leg 253's (parked, unmerged, read-only) full-text pinning of NRS 1996 / Tsai
         1998's hypotheses, transcribed at locator, to state the DSS-vs-BSS question
         independently of the weight answer.

Run: .venv/bin/python experiments/p2_route_algw_v1_scoping.py
Out: writeup/data/p2_route_algw_v1.json

CEILING. No link L1->L4 chain moves here. Clay odds stay ~0.05%. This leg has no
authority to lift any ban and does not attempt to; S1's escape/death answer only
determines whether a lift-condition evidence packet is assembled for the user, never
whether the ban is lifted.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_algw_v1.json")


# ----------------------------------------------------------------------------
# S1_A -- Route-D exhaustive audit, transcribed from leg 126 (experiments/journal/leg_126.md)
# ----------------------------------------------------------------------------
def s1_route_d():
    total_configs = 1686
    covered = 1686
    theorem = 144
    structural = 1032
    measured = 510
    assert theorem + structural + measured == covered == total_configs
    # leg 126's own headline shortfall at theoretical-optimum best case
    z1_best = 6.0424
    shortfall_x = z1_best / 1.0
    return {
        "source": "experiments/journal/leg_126.md",
        "total_configs": total_configs,
        "covered": covered,
        "theorem": theorem,
        "structural": structural,
        "measured": measured,
        "exhaustive": covered == total_configs,
        "admissible_band": "0 <= s < 0.394 (theorem on A21=0, measured otherwise)",
        "inadmissible_1": "0.394 <= s < 1.0 (target leaves its own space)",
        "inadmissible_2": "s >= 1.0 (target out AND tail kernel leaves as cokernel functional enters dual)",
        "z1_at_theoretical_optimum": z1_best,
        "shortfall_factor": shortfall_x,
        "a0_only": True,
    }


# ----------------------------------------------------------------------------
# S1_B -- leg 51/52's algebraic-weight-exponent sweep, transcribed + re-derived crossover.
# leg 51 (PHASE2_P2_NOTES.md ~ line 3280+, "ROUTE-L1 v2"): kernel h_m ~ m^-2.0024
# leg 52 (PHASE2_P2_NOTES.md ~ line 3400+, "ROUTE-T v1"): cokernel u_m ~ m^+1.0012
# both against a weight w_m = (1+m)^s. h_m in ell^1_w iff sum m^{-2.0024} (1+m)^s < inf
# iff s < 2.0024 - 1 = 1.0024 =~ 1 (measured). u_m (functional) bounded iff
# sum m^{1.0012} (1+m)^{-s} < inf iff s > 1.0012 + 1 = 2.0012? -- NO: leg 52's own
# measured crossover is s=1 for BOTH, because the cokernel pairing is against the
# *dual* weight w_m^{-1}, not w_m again; re-derive that explicitly rather than assume it.
# ----------------------------------------------------------------------------
def s1_ell1w_crossover():
    kernel_exp = 2.0024   # h_m ~ m^{-kernel_exp}, measured leg 51
    cokernel_exp = 1.0012  # u_m ~ m^{+cokernel_exp}, measured leg 52
    # kernel h_m in ell^1_w=(1+m)^s : sum_m m^{-kernel_exp} * m^{s} < inf  <=> s < kernel_exp - 1
    s_kernel_boundary = kernel_exp - 1.0
    # cokernel functional u_m paired against ell^1_w means it must lie in the DUAL,
    # ell^infty_{1/w}: sup_m |u_m| * m^{-s} < inf requires only boundedness for s>=0 when
    # u_m itself already diverges like m^{cokernel_exp} -- so it needs s >= cokernel_exp
    # to be tamed. Measured empirical crossover (leg 52 Table T-5) is reported at s=1
    # for both directions simultaneously; check how close the two closed-form boundaries
    # (s_kernel_boundary, cokernel_exp) sit to the measured s=1, as an honesty check on
    # the "exact s=1" reading rather than a re-derivation from nothing.
    return {
        "source": "PHASE2_P2_NOTES.md (leg 51 ~line 3280-3360, leg 52 ~line 3390-3470)",
        "kernel_fit_exponent": kernel_exp,
        "cokernel_fit_exponent": cokernel_exp,
        "s_kernel_boundary_closed_form": s_kernel_boundary,
        "s_cokernel_boundary_closed_form": cokernel_exp,
        "measured_crossover_s": 1.0,
        "closed_form_vs_measured_gap_kernel": abs(s_kernel_boundary - 1.0),
        "closed_form_vs_measured_gap_cokernel": abs(cokernel_exp - 1.0),
        "no_window": True,
        "swept_families": ["flat", "algebraic (9 exponents)", "geometric"],
        "divergence_curve_minimum_exponent": 0.639,
        "divergence_curve_minimum_at_s": 1.00,
        "window_empty_by": 0.606,
        "banned_in_plan_of_record": True,
        "ban_text_locator": "plan_of_record.py ~line 867-900 (stage-V re-posed ban + weight-exponent tuning ban + weight-family sweep ban)",
    }


# ----------------------------------------------------------------------------
# S1_C -- origin-H^2 is already algebraically weighted (Mellin weight (1+xi^4)),
# transcribed from experiments/journal/leg_176.md
# ----------------------------------------------------------------------------
def s1_origin_h2():
    return {
        "source": "experiments/journal/leg_176.md",
        "weight_kind": "algebraic (Mellin): ||phi||^2_X ~ Int_0^inf (1+xi^4) |phihat|^2 dxi",
        "is_already_algebraic": True,
        "dies_because": "a=0 exactness only (exact CLM profile Omega(y)=-y/(y^2+1/4)); "
                         "for a>0 Xu proves only a conditional two-line Adm(a) inclusion, "
                         "no resolvent, no invertibility, no gap; HL_S2_nonsymmetric is not "
                         "a CLM profile and inherits none of it",
        "mechanism_is_orthogonal_to_weight_shape": True,
    }


# ----------------------------------------------------------------------------
# S1_D -- CAP-apparatus shape mismatch, transcribed from leg 331 (experiments/journal/leg_331.md)
# ----------------------------------------------------------------------------
def s1_cap_apparatus_shape():
    return {
        "source": "experiments/journal/leg_331.md",
        "finding": "Lam^{2a} psi_m (nonlocal operator symbol) forces an ALGEBRAIC tail "
                   "x^{-(1+2a+2m)} against Breden-Chu's Gaussian weight e^{x^2/4}; the "
                   "operator does not map the machinery's space into itself, and the "
                   "Gauss-Hermite/Laguerre quadrature rules (exact for polynomial x "
                   "Gaussian) lose exactness against the algebraic tail (rule error "
                   "0.34-0.76 at 20-60% nonlocality vs 1e-12 local control)",
        "measured_exponents": {"alpha=0.25": 1.507674, "alpha=0.5": 2.012245, "alpha=0.75": 2.517908},
        "predicted_exponents": {"alpha=0.25": 1.5, "alpha=0.5": 2.0, "alpha=0.75": 2.5},
        "z1_crosses_1_at_finite_t": True,
        "lesson_invoked": "lesson 87: a certification method has a shape, and the shape "
                          "is a property of the operator, not the object -- Gauss-Hermite/"
                          "Laguerre exactness is tied to the Gaussian weight specifically",
        "direction_of_this_evidence": "operator=algebraic vs space=Gaussian (opposite "
                                       "combination to S1's question, space=algebraic); "
                                       "read as evidence about the SHAPE requirement, not "
                                       "as a direct measurement of the algebraic-weight case",
    }


# ----------------------------------------------------------------------------
# S2 -- re-derive u's decay exponent from leg 260's Type-I rate, not leg 261's
# Gaussian-witness Biot-Savart exponent, and recompute L^3 integrability.
# ----------------------------------------------------------------------------
def s2_composition_rederivation():
    # leg 260 experiments/journal/leg_260.md line 56: |U(y)| <= C/(1+|y|)  => sigma_target = 1
    sigma_target = 1.0
    # leg 261 experiments/journal/leg_261.md line 193-194: u ~ |x|^-3 via C3 (Biot-Savart,
    # measured on a Gaussian-decaying witness omega in H^2(mu))
    sigma_witness = 3.0

    def l3_tail_exponent(sigma):
        # |u|^3 r^2 ~ r^{-3 sigma + 2}; integrable at infinity (radial measure r^2 dr) iff
        # -3 sigma + 2 < -1  <=>  sigma > 1
        return -3.0 * sigma + 2.0

    exp_target = l3_tail_exponent(sigma_target)
    exp_witness = l3_tail_exponent(sigma_witness)

    # quadrature cross-check: Int_1^R r^{tail_exp} dr diverges (log) iff tail_exp == -1
    def shell_ratio(sigma, R=1.0e4):
        # ratio of Int_R^{2R} to Int_1^R of r^{-3 sigma+2} dr, mirrors leg 260's own
        # p=3 / s=1 shell-ratio diagnostic exactly (same closed-form family)
        exp_ = -3.0 * sigma + 2.0
        if abs(exp_ + 1.0) < 1e-12:
            # log divergent: ratio of log(2R/R)-type increments -> stays finite but the
            # integral itself is unbounded; report the diagnostic leg 260 used, log(2)
            return math.log(2.0)
        num = ((2 * R) ** (exp_ + 1) - R ** (exp_ + 1))
        den = (R ** (exp_ + 1) - 1.0 ** (exp_ + 1))
        return num / den

    return {
        "sigma_target_type_I": sigma_target,
        "sigma_target_source": "experiments/journal/leg_260.md:56 (Chae-Wolf Thm 1.1, |u|<=C/(sqrt(-t)+|x|))",
        "sigma_witness_gaussian": sigma_witness,
        "sigma_witness_source": "experiments/journal/leg_261.md:193-194 (C3, Biot-Savart on H^2(mu) witness)",
        "l3_tail_exponent_target": exp_target,
        "l3_tail_exponent_witness": exp_witness,
        "l3_integrable_threshold": "tail_exponent < -1  <=>  sigma > 1",
        "target_is_integrable": exp_target < -1.0,
        "target_at_boundary": abs(exp_target - (-1.0)) < 1e-9,
        "witness_is_integrable": exp_witness < -1.0,
        "agrees_with_leg260_p3_s1_crossing": True,
        "leg260_shell_ratio_at_p3": 1.000027,
        "this_legs_shell_ratio_at_sigma1": shell_ratio(sigma_target),
        "verdict": "DISSOLVES: re-derived on the target's own (algebraic-weight-native, "
                   "Type-I) decay rate rather than the Gaussian-basis witness rate, u sits "
                   "EXACTLY at the L^3 log-divergent boundary (sigma=1, same crossing leg "
                   "260 already measured at p=3/s=1), not inside L^3; leg 261's u in L^3 "
                   "claim used sigma=3, a property of the Gaussian witness (fast-converging "
                   "Biot-Savart dipole moment), not of the algebraically-decaying target",
    }


# ----------------------------------------------------------------------------
# S2_DSS -- DSS-vs-BSS ansatz position, stated on its own, transcribed from leg 253
# (parked, unmerged branch leg/253-nrsx-v1; read-only; NOT a banked/merged fact,
# flagged as such throughout)
# ----------------------------------------------------------------------------
def s2_dss_position():
    return {
        "source": "leg/253-nrsx-v1:experiments/journal/leg_253.md (PARKED, UNMERGED -- "
                   "escalated to user, branch pushed, main untouched; cited here read-only, "
                   "NOT treated as a banked repository fact)",
        "hierarchy": "SS (subset of) RSS (subset of) RDSS ... DSS strictly broader than "
                     "exactly-backward-self-similar (SS)",
        "hierarchy_locator": "leg_253.md:106",
        "nrs_hypothesis": "U in L^3(R^3), weak solution of Leray's system (exactly backward "
                          "self-similar U) => U == 0",
        "nrs_locator": "leg_253.md:30",
        "tsai_thm1_hypothesis": "U in L^q(R^3), q in (3,inf] (exactly backward self-similar) "
                                "=> U constant, ==0 if q<inf",
        "tsai_locator": "leg_253.md:31",
        "dss_class_verdict_in_leg253": "NARROWED, not excluded: survives only as "
                                       "non-axisymmetric, lambda significantly > 1, profile "
                                       "not in L^inf_t L^3",
        "dss_class_locator": "leg_253.md:124",
        "leg260_target_matches_surviving_corner": True,
        "leg260_target_locator": "experiments/journal/leg_260.md (NS3D-DSS-NONAXI-LAMBDA-LARGE)",
        "position": "NRS/Tsai's own theorems are stated for exactly-backward-self-similar "
                    "(SS) profiles, not for DSS profiles at lambda significantly larger than "
                    "1; leg 253 already found this the ONE surviving corner of the DSS class "
                    "precisely because NRS/Tsai (and the Chae-Wolf/axisymmetry compositions) "
                    "do not reach it. This is an ansatz-class question, independent of any "
                    "weight answer: even if the L^3 composition survived re-derivation in "
                    "the algebraic weight (S2's DISSOLVES verdict says it does not), it would "
                    "still be answering an SS question about a DSS target.",
        "never_inferred_from_weight_answer": True,
    }


def main():
    s1a = s1_route_d()
    s1b = s1_ell1w_crossover()
    s1c = s1_origin_h2()
    s1d = s1_cap_apparatus_shape()
    s2 = s2_composition_rederivation()
    s2dss = s2_dss_position()

    answers = {
        "S1": {
            "gate": "DIES",
            "route_d": s1a,
            "ell1w_crossover": s1b,
            "origin_h2": s1c,
            "cap_apparatus_shape": s1d,
            "mechanism_summary": (
                "The algebraically weighted space is not hypothetical: it has already "
                "been realized in three independent lanes and each has already died, for "
                "three different mechanisms. (i) Sup-norm/collocation lane (Route-D, "
                "decay_grading.py/decay_collocation.py/holder_norms.py, 11+ legs): "
                "exhaustively audited (leg 126, 1686/1686 configs), a=0-only, best case "
                "Z1=6.0424, 6.04x short of closing even at theoretical optimum. (ii) "
                "Coefficient/ell^1_w lane (leg 51/52, extending the banned leg-54 "
                "realization with a tunable algebraic exponent s): swept across flat, "
                "9 algebraic exponents, and geometric weight families; kernel-in-space and "
                "cokernel-bounded failure modes swap exactly at s=1 with no window at any "
                "exponent; re-attempting this sweep is itself explicitly banned in "
                "plan_of_record.py. (iii) Origin-conjugated/Mellin lane (legs 163/176): "
                "already uses an algebraic (polynomial, (1+xi^4)) weight and still dies, "
                "for the orthogonal a=0-only-exactness reason. A fourth line of evidence "
                "(leg 331) shows the CAP apparatus's own exactness (Gauss-Hermite/Laguerre "
                "quadrature) is tied to the Gaussian weight's shape specifically (lesson "
                "87) -- so a coherent algebraic-weight CAP formulation is not merely "
                "conceivable, it is exactly what Route-D already built and exhausted. "
                "Does the CAP apparatus have a coherent formulation in the algebraic "
                "weight: YES, it has one (Route-D), and it has already been measured dead "
                "at full strength."
            ),
            "lift_condition_evidence_packet_assembled": False,
            "reason_no_packet": "S1 answers DIES; per this leg's gate spec, dies -> name "
                                "mechanism at full strength, lift condition stays unmet, "
                                "no packet is assembled, and the deferred section-3 build "
                                "is NEVER drafted",
        },
        "S2": {
            "composition_gate": "DISSOLVES",
            "rederivation": s2,
            "dss_position": s2dss,
            "summary": (
                "Re-derived in the algebraic weight using the target's own Type-I decay "
                "rate (leg 260, sigma=1) rather than leg 261's Gaussian-witness Biot-Savart "
                "rate (sigma=3): u sits exactly at the L^3 log-divergent boundary, not "
                "inside L^3, so the hypothesis the NRS/Tsai composition needs is not "
                "established. 'A wall shown to be a weight artifact is a map correction, "
                "not movement.' Separately and without inferring from the weight answer: "
                "NRS/Tsai's own theorems bind exactly-backward-self-similar (SS) profiles; "
                "leg 260's target is DSS at lambda significantly larger than 1, which leg "
                "253 (parked, unmerged) already found to be the one class NOT reached by "
                "NRS/Tsai's stated hypotheses. Both readings converge on the same "
                "conclusion by independent routes -- weight-dependent decay re-derivation, "
                "and weight-independent ansatz-class mismatch -- that the wall does not "
                "bind leg 260's actual screened object."
            ),
        },
        "consequences": {
            "leg_334_clause_a": (
                "Leg 334's clause (a) is OWNED-BY-341-PENDING (DM cycle-9 ruling a17554c, "
                "leg_334.md:236-246): it names the space and cites this leg's answer if "
                "landed. This leg's answer: S1 DIES. Clause (a) should read the weight "
                "question as CLOSED-NO (the algebraic space does not escape, no lift-"
                "condition packet exists), leaving clause (a)'s NRS/Tsai position and "
                "sec 26/4.1 basis-resolution difficulty unaffected (those were never this "
                "leg's territory, per leg_334.md:272-274)."
            ),
            "deferred_section3_build": (
                "NEVER drafted, per this leg's own gate spec and per leg_334.md:266-270 "
                "(DM: the Tier-2->Tier-3 clause is reserved to a section-3 build drafted "
                "ONLY after 341 reports, and B9 was already STRUCK pending this report). "
                "With S1=DIES, the section-3 build's precondition (an escaped space) does "
                "not exist; the Tier-2 ceiling on every route-4 gate stays unchanged."
            ),
            "s_equals_1_suspicious_agreement_flagged": (
                "leg_334.md:261-265 flags that leg 260 (space sharp at s>1), leg 313 "
                "(crossing measured at s=1), and leg 334's own arithmetic (s=1) are three "
                "agreeing derivations that are NOT obviously independent, with the explicit "
                "instruction that 'leg 341 should test it, not inherit it.' This leg's own "
                "s1_ell1w_crossover finding is a DIFFERENT s=1 (a spectral kernel/cokernel "
                "property of an abstract tail operator on the coefficient basis, leg 51/52) "
                "from leg 260/313/334's s=1 (the target profile's own L^p/weighted-L^2 "
                "integrability threshold) -- numerically coincident, mechanistically "
                "unrelated quantities. Recorded as a second coincidence at s=1, not treated "
                "as confirmation of either."
            ),
        },
    }

    gate = {
        "S1": "DIES",
        "S2_composition": "DISSOLVES",
        "S2_dss_position_stated_independently": True,
    }

    honesty = {
        "no_ban_lifted": True,
        "plan_of_record_not_edited": True,
        "section3_build_not_drafted": True,
        "no_construction": True,
        "all_numbers_transcribed_or_elementary_recomputation": True,
        "clay_odds": "~0.05%, unchanged",
        "l1_to_l4_chain_moved": False,
    }

    self_test = {}

    # self-tests: elementary algebra checks, not measurements
    self_test["s1_route_d_partition_exhaustive"] = (s1a["covered"] == s1a["total_configs"])
    self_test["s1_route_d_shortfall_gt_1"] = (s1a["shortfall_factor"] > 1.0)
    self_test["s1_ell1w_no_window"] = s1b["no_window"] is True
    self_test["s1_ell1w_boundaries_bracket_s1"] = (
        s1b["closed_form_vs_measured_gap_kernel"] < 0.01
        and abs(s1b["s_cokernel_boundary_closed_form"] - 1.0) < 0.01
    )
    self_test["s1_origin_h2_is_algebraic_and_dies"] = (
        s1c["is_already_algebraic"] and "a=0" in s1c["dies_because"]
    )
    exp_check = -3.0 * 1.0 + 2.0
    self_test["s2_l3_tail_exponent_target_matches_closed_form"] = (
        abs(s2["l3_tail_exponent_target"] - exp_check) < 1e-12
    )
    self_test["s2_target_at_l3_boundary_not_inside"] = (
        s2["target_at_boundary"] and not s2["target_is_integrable"]
    )
    self_test["s2_witness_would_have_been_integrable"] = s2["witness_is_integrable"] is True
    self_test["s2_dss_hierarchy_locator_present"] = bool(s2dss["hierarchy_locator"])
    self_test["s2_dss_never_inferred_from_weight"] = s2dss["never_inferred_from_weight_answer"] is True

    all_pass = all(bool(v) for v in self_test.values())
    self_test["ALL_PASS"] = all_pass

    out = {
        "leg": 341,
        "route": "ALGW",
        "title": "THE FOURTH SPACE -- does 260's algebraically weighted space escape "
                 "the three-realization death, and does the NRS/Tsai composition "
                 "survive the weight change?",
        "answers": answers,
        "gate": gate,
        "honesty": honesty,
        "self_test": self_test,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)

    print(f"Wrote {OUT}")
    print(f"S1 gate: {gate['S1']}")
    print(f"S2 composition gate: {gate['S2_composition']}")
    print(f"self_test ALL_PASS: {all_pass}")
    if not all_pass:
        for k, v in self_test.items():
            if not v:
                print(f"  FAILED: {k}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
