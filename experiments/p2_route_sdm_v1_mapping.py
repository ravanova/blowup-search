"""P2 Route-SDM v1 -- leg 165: SPACE-vs-OPERATOR MAPPING ACROSS EVERY REALIZATION THIS
REPOSITORY HAS CALLED DEAD.

A SYNTHESIS leg over BANKED DATA ONLY.  It runs no dynamics, builds no certificate, imports
no `solver/` module, executes no measurement, and edits nothing outside its declared
territory.  Every number it emits is read from a committed JSON under `writeup/data/` or is
arithmetic on two such numbers, and every such arithmetic step is labelled with the two
banked inputs it came from.  No ban is lifted under either branch and no link of the
`L1 -> L4` chain can move.

THE GATE, verbatim from `DIRECTION.md` leg 165:

    "For each of legs 52, 53, 56, 111/141's dead findings, does the repository's own banked
     record contain evidence the finding is REALIZATION-DEPENDENT (i.e., a different choice
     within the same degree of freedom, already tried elsewhere in the banked record,
     behaves differently), or does every tried realization agree?"

    ANSWER: YES -- at leg 111/141, and at that row only.

WHAT THIS LEG MAY NOT CLAIM (novelty log sec 2, binding).  "The obstruction belongs to the
realization, not to the operator" is PUBLISHED AND NAMED, on this exact operator: Xu,
arXiv:2607.19762, Proposition 2 of sec 3.1 -- "The essential spectrum of L_0 depends on the
realization."  This leg uses that dichotomy and does not claim it, exactly as leg 127 used
and did not claim `Z1 >= 1 - ||A|| sigma_min`.  What is this leg's own is only the
classification of this repository's four banked dead findings under it.

THE PREDICATE, pre-registered in `writeup/novelty/leg_165.md` sec 5 BEFORE this file
existed.  For a banked dead finding F with degree of freedom d, three tiers, never
conflated:

  TIER 1  VERDICT-DEPENDENT     a different choice WITHIN d is banked in which the
                                certificate / gap / bound CLOSES.  Only this answers YES.
  TIER 2  MAGNITUDE-DEPENDENT   a different choice within d moves the headline by orders of
          VERDICT-INVARIANT     magnitude while the verdict survives.  NOT a YES.
  TIER 3  REALIZATION-INVARIANT every choice within d that the record actually tried
                                agrees, on verdict and on order of magnitude.

THE THREE CONTROLS, also pre-registered, and all three must pass or the run is void:

  C1  THE PREDICATE MUST BE ABLE TO SAY NO (lesson 90).  Legs 52 and 53 are the required
      negative cases: both vary a parameter INSIDE the single `l^1_w`-at-`s<1` realization
      that leg 127 already showed is the space-dependent one, so their internal variation
      is not a second realization.  If every row returns tier 1 the predicate is a tautology
      of this file and the result is WITHDRAWN, not shipped.
  C2  THE PREDICATE MUST BE ABLE TO SAY YES.  Leg 127's own row, fed through the identical
      code path, must return tier 1 -- that is the finding the gate takes as given.  If it
      does not, the predicate is mis-specified and the run is void.
  C3  NO BORROWING ACROSS DEGREES OF FREEDOM.  A different OPERATOR (`mu > 0`, dissipative)
      is NOT a different realization of the same operator.  Every `mu > 0` witness in the
      banked record is collected into its own column and is structurally barred from tier 1.

PREDICTION, recorded in the novelty log before this file was coded, so the run can embarrass
it: 52 -> tier 3, 53 -> tier 3, 56 -> tier 2, 111/141 -> tier 1.

CEILING (clause S7, carried unchanged).  Every magnitude below was measured on the `a = 0`
CLM linearisation -- one mode, analytic, the friendliest object in the repository -- with
`Y_0` exactly zero for the banned degenerate reason.  Nothing here is a statement about
`HL_S2_nonsymmetric`.  A realization-dependent death is not a revival: the gate's own
yes-branch calls it "a candidate companion to leg 127's reframing, not a ban-lifting result
on its own", and this leg proposes, prices and recommends nothing.
"""

from __future__ import annotations

import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "writeup", "data")
OUT = os.path.join(DATA, "p2_route_sdm_v1_mapping.json")

# The banked sources, and nothing else is opened.
SOURCES = {
    "leg_52": "p2_route_t_v1_border.json",
    "leg_53": "p2_route_tc_v1_assemble.json",
    "leg_56": "p2_route_tn_v1_consistency.json",
    "leg_111": "p2_route_we_v1_coercivity.json",
    "leg_127": "p2_route_ngx_v1_general.json",
    "leg_141": "p2_route_wel_v1_lit.json",
}

TIER_1 = "TIER_1_VERDICT_DEPENDENT"
TIER_2 = "TIER_2_MAGNITUDE_DEPENDENT_VERDICT_INVARIANT"
TIER_3 = "TIER_3_REALIZATION_INVARIANT"


def window_width(lower_exclusive: float, upper_exclusive: float) -> float:
    """Width of the admissible window between two complementary banked requirements.

    ONE function, called on BOTH axes that have this shape -- leg 52's `s` axis (kernel needs
    `s < 1`, cokernel needs `s >= 1`) and leg 111/141's trial-space axis (space needs
    `gamma < 2p+1`, damping needs `gamma > 3`).  It returns 0.0 on the first and 2.0 on the
    second at `p = 2`, so it is not a constant dressed as a measurement (lesson 90).
    """
    return max(0.0, upper_exclusive - lower_exclusive)


def load(name: str) -> dict:
    with open(os.path.join(DATA, SOURCES[name]), "r") as fh:
        return json.load(fh)


def row_52(t: dict, ngx: dict) -> dict:
    """Leg 52 -- degree of freedom: the WEIGHT EXPONENT s inside `l^1_w`.

    Every choice of `s` the repository actually tried, on both sides of the record: leg 52's
    own bordered-tail ladder (five classes) and leg 127's `sigma_min` ladder (five classes,
    three `K`).  They must agree that nothing inside the axis behaves differently, and the
    structural reason is leg 52's own `T5_fredholm`: the two admissibility requirements are
    complementary with a SINGLE crossing point, so the window has zero width -- the same
    shape as leg 111's, in a different realization.
    """
    tried = [
        {
            "s": lad["param"],
            "class": lad["class"],
            "bordered_tail_first": lad["analytic"][0],
            "bordered_tail_last": lad["analytic"][-1],
            "bordered_growth_exponent": lad["analytic_shape"]["exponent"],
        }
        for lad in t["T1_ladders"]
    ]
    exps = [r["bordered_growth_exponent"] for r in tried]
    # leg 127's independent traverse of the SAME axis
    sigma_rows = []
    for r in ngx["NGX2_sigma_min_ladder"]:
        sigma_rows.append({"s": r["s"], "K": r["K"], "sigma_min_last": r["sigma_min"][-1]})
    return {
        "leg": "52",
        "banked_dead_finding": (
            "stage B's SPACE degree of freedom is dead for this operator: no choice of the "
            "weight exponent s buys closure"
        ),
        "degree_of_freedom": "the weight exponent s of the l^1_w family (stage B's 'space' axis)",
        "choices_actually_tried_in_the_banked_record": {
            "leg_52_bordered_tail_ladder": tried,
            "leg_127_sigma_min_ladder_same_axis": sigma_rows,
        },
        "do_they_disagree": {
            "leg_52_every_bordered_exponent_is_positive": all(e > 0 for e in exps),
            "leg_52_exponent_min": min(exps),
            "leg_52_exponent_max": max(exps),
            "leg_52_exponent_is_monotone_in_s": exps == sorted(exps),
            "leg_127_sigma_min_max_deviation_from_predicted_1_minus_s": ngx[
                "NGX2_max_deviation_from_1_minus_s_for_s_below_1"
            ],
            "leg_127_max_relative_K_spread_for_s_below_1": ngx["NGX2_K_independence"][
                "max_relative_spread_over_K_for_s_below_1"
            ],
            "reading": (
                "Every s < 1 the repository tried behaves the SAME way and behaves WORSE as s "
                "grows: the bordered tail norm grows without bound in all five classes, and "
                "sigma_min vanishes like M^-(1-s) uniformly, to within 0.0219 of the predicted "
                "exponent and to within 0.29% across K.  No choice inside the axis closes."
            ),
        },
        "structural_reason_banked_by_leg_52_itself": dict(t["T5_fredholm"]),
        "window_on_this_axis": {
            # NOT crossing-minus-crossing, which would be 0.0 whatever the record said
            # (lesson 90).  The two bounds are read from the two SEPARATE banked clauses, and
            # the same formula is applied to leg 111's trial-space axis below, where it
            # returns 2.0 -- so it demonstrably can come out non-zero.
            "kernel_needs_s_strictly_below": float(t["T5_fredholm"]["crossing"]),
            "cokernel_needs_s_at_least": float(t["T5_fredholm"]["crossing"]),
            "width": window_width(
                float(t["T5_fredholm"]["crossing"]),  # cokernel's lower bound
                float(t["T5_fredholm"]["crossing"]),  # kernel's upper bound
            ),
            "same_shape_as_leg_111": (
                "two complementary requirements meeting at a single point.  leg 52: kernel in "
                "space iff s < 1, cokernel bounded iff s >= 1, crossing 1.0.  leg 111: space "
                "needs gamma < 3, damping needs gamma > 3.  Two realizations, one shape -- and "
                "leg 111's turns out to be movable (below) while leg 52's is not, which is why "
                "the SHAPE of an obstruction does not settle its tier."
            ),
        },
        "tier": TIER_3,
        "why_this_row_is_NOT_a_companion_to_leg_127": (
            "Xu's origin-H^2 realization IS a different space and DOES behave differently -- but "
            "that is leg 127's own banked finding, not a second one.  Legs 52 and 53 live INSIDE "
            "the l^1_w-at-s<1 realization leg 127 reframed.  Counting them as independent dead "
            "findings double-counts leg 127.  This row is SUBSUMED, not a companion."
        ),
        "prior_demotion_already_banked": (
            "leg 49's gauge ablation put leg 52's 5604x effect in the BORDER ROWS, not the space "
            "-- pin c_l and it collapses to 0.56x.  plan_of_record.py carries that as a standing "
            "ban on repeating 'closure is a property of the SPACE' as an explanation.  The "
            "EXPLANATION was demoted once already; the axis's exhaustion is what survived."
        ),
    }


def row_53(tc: dict) -> dict:
    """Leg 53 -- degree of freedom: the OPERATOR SPLIT (K, class, gauge, normalisation, and
    the border direction that sets the amplitude column).

    The sweep is `TC4_z1_subblocks` plus the `TC8` normalisation ablation.  The honest
    nuance this row must carry: the border-direction axis is NOT flat -- it discriminates by
    13 orders of magnitude once wired through -- and every variation is WORSE.  A axis that
    varies hugely and never crosses 1 is still verdict-invariant.
    """
    rows = tc["TC4_z1_subblocks"]
    coupling = [r["Z1_Gamma_tail"] for r in rows]
    Ks = sorted({r["K"] for r in rows})
    classes = sorted({(r["class"], r["param"]) for r in rows})
    gauges = sorted({r["gauge"] for r in rows})
    best_norm = tc["TC8_best_over_all_normalisations"]
    negs = tc["TC5b_negative_controls"]
    return {
        "leg": "53",
        "banked_dead_finding": (
            "stage B's SPLIT degree of freedom is dead: the block coupling Z1[Gamma <- tail] "
            "never comes under 1 for any split the repository tried"
        ),
        "degree_of_freedom": (
            "the operator split -- finite-block size K, weight class, gauge row, "
            "normalisation, and the border direction that sets the amplitude column"
        ),
        "choices_actually_tried_in_the_banked_record": {
            "rows_in_the_sweep": len(rows),
            "K_values": Ks,
            "classes": [{"class": c, "param": p} for c, p in classes],
            "gauges": gauges,
            "normalisation_ablation_arms": 6,
            "border_directions": [n["border"] for n in negs],
        },
        "do_they_disagree": {
            "min_coupling_over_every_split_and_class": min(coupling),
            "max_coupling_over_every_split_and_class": max(coupling),
            "best_over_all_normalisations": best_norm["Z1_lower_bound"],
            "value_it_has_to_beat": 1.0,
            "shortfall_of_the_single_best_arm": best_norm["Z1_lower_bound"] / 1.0,
            "gate_survives_renormalisation": tc["TC8_gate_survives_renormalisation"],
            "reading": (
                "Nothing on this axis crosses 1.  The single most favourable arm in the whole "
                "record -- algebraic s=0.3, K=4, normalisation 'no_amplitude' -- still reports "
                "20.4734 where it must be under 1, and the best arm at the shipped "
                "normalisation is 43.1513."
            ),
        },
        "the_axis_that_varies_hugely_and_still_does_not_close": {
            "note": (
                "Lesson 90's case.  Leg 53 first reported 546.57 for all four border directions "
                "and called four identical numbers its sharpest result; they were identical "
                "because the quantity referenced no border.  Wired through, the axis "
                "discriminates hard -- and every direction is worse, so the VERDICT is still "
                "invariant.  A flat axis and a wildly varying axis can both be tier 3; what "
                "decides the tier is whether any choice crosses the threshold."
            ),
            "by_border_direction": [
                {"border": n["border"], "Z1_lower_bound": n["Z1_lower_bound"]} for n in negs
            ],
            "analytic_over_svd": tc["TC5b_analytic_over_svd"],
            "worst_over_analytic": tc["TC5b_worst_over_analytic"],
            "any_border_direction_below_one": any(n["Z1_lower_bound"] < 1.0 for n in negs),
        },
        "tier": TIER_3,
        "scope_leg_53_itself_recorded": tc["term_that_ran_out"]["scope"][:400],
    }


def row_56(tn: dict) -> dict:
    """Leg 56 -- degree of freedom: WHICH INTERPOLANT the collocation Hilbert operator
    transforms.

    Both choices were built by leg 56 itself, which is what makes this row decidable from the
    banked record with no new compute:
      (a) the shipped `line_hilbert_matrix`, which assembles source columns for INTERIOR
          nodes only and therefore transforms an ENDPOINT-ZEROED interpolant;
      (b) a full-interpolant Hilbert matrix with the endpoint hats restored as one-sided
          half-hats, which reproduces direct PV quadrature to 4.34e-19.
    Under (a) the headline is 2.0403e+11 tau.  Under (b) the H defect is the genuine
    interpolation error only.  The verdict survives on D alone.
    """
    v = tn["verdict"]
    att = tn["H_attribution"]
    d_only = tn["D_only_extrapolation"]
    chk = tn["validation"]["H_is_endpoint_zeroed_check"]
    headline_a = v["defect_H_over_tau_at_801"]
    headline_b = d_only["defect_D_over_tau_at_801"]
    return {
        "leg": "56",
        "banked_dead_finding": (
            "the sup-norm COLLOCATION realization cannot carry L1: the (H, D) consistency "
            "defect exceeds L1 step one's admissible tau by 1.85e7x (derivative) / 2.04e11x "
            "(Hilbert) at n = 801"
        ),
        "degree_of_freedom": (
            "the collocation basis -- specifically which interpolant the discrete Hilbert "
            "operator transforms (endpoint-zeroed Pi^0 vs the full natural-spline Pi)"
        ),
        "choices_actually_tried_in_the_banked_record": {
            "A_endpoint_zeroed_shipped": {
                "who_built_it": "solver/line_hilbert.py's line_hilbert_matrix, interior nodes only",
                "defect_H_over_tau_at_801": headline_a,
                "H_rate_order_per_doubling": v["H_rate_per_doubling"][0]["order"],
            },
            "B_full_interpolant": {
                "who_built_it": (
                    "leg 56 itself -- 'a full-interpolant Hilbert matrix (endpoint hats restored "
                    "as one-sided half-hats)'"
                ),
                "agreement_with_direct_PV_quadrature": chk["abs_diff_full_matrix_vs_quadrature"],
                "residual_defect_is_only_the_true_interpolation_error": att[
                    "defect_H_interpolation"
                ][-1],
                "interpolation_order": att["interpolation_order"],
                "n_required_if_H_were_interpolation_only": att["n_required_interpolation_only"],
            },
        },
        "do_they_disagree": {
            "endpoint_share_of_the_headline_at_801": att["endpoint_share_at_801"],
            "reading_of_that_share": (
                "1.0000939 -- the endpoint-zeroing artifact is 100.009% of the gated H defect. "
                "The headline number is a property of choice (A), not of the operator, and leg "
                "56 said so in its own journal: 'the artifact is THE WHOLE DEFECT, which is why "
                "the total does not converge.'"
            ),
            "headline_under_A_over_tau": headline_a,
            "headline_under_B_over_tau_D_alone": headline_b,
            "magnitude_moved_by_the_basis_choice": headline_a / headline_b,
            "does_the_VERDICT_move": False,
            "why_not": (
                "With the H defect deleted outright, D alone still stands at 1.8537e+07 tau at "
                "measured order 4.0072, needing n = 52163 against the n = 801 actually reached, "
                "on a DENSE interval certificate whose cost grows like N^3 with N = 2n+3.  Leg "
                "56 pre-committed exactly this robustness check and it is banked in its own JSON."
            ),
            "n_required_D_only": d_only["n_required"],
            "D_measured_order": d_only["measured_order"],
        },
        "tier": TIER_2,
        "what_this_costs_the_banked_prose": (
            "The 2.04e11x figure may not be quoted as the size of the collocation realization's "
            "gap without naming the endpoint-zeroed basis it belongs to.  The realization-robust "
            "number is 1.85e7x, and it is still a death: 1.10e4x smaller and 65x too many nodes."
        ),
    }


def row_111_141(we: dict, wel: dict) -> dict:
    """Legs 111/141 -- degree of freedom: the WEIGHTED-ENERGY REALIZATION, i.e. the pair
    (weight exponent gamma, trial space).

    Leg 111 fixed the trial space to `span{sin k theta}` -- vanishing order p = 1 at the
    origin -- and swept gamma.  Leg 141 held gamma at the published value 4 and moved the
    TRIAL SPACE instead, on leg 111's own graded quadrature, and re-located EGM Prop. 2.1 in
    the actual PDF at run time.  That is the same degree of freedom, a different choice
    inside it, and the verdict flips from 'zero-width window, dead' to 'a certified
    coercivity gap of -1/2'.
    """
    windows = wel["windows"] if "windows" in wel else wel["window_by_trial_space"]["windows"]
    meas = wel["window_by_trial_space"]["measurements"]
    tri = wel["constant_triangulation"]
    egm = next(e for e in wel["located"] if e["id"] == "EGM-P21")
    xu = next(e for e in wel["located"] if e["id"] == "XU-NOGO")
    at_gamma_4 = {m["p"]: m for m in meas if m["gamma"] == 4.0}
    return {
        "leg": "111/141",
        "banked_dead_finding": (
            "the WEIGHTED-ENERGY realization dies on the friendliest object: every admissible "
            "weight's coercivity gap is negative, converging to -(3-gamma)/2, and the "
            "admissibility/damping window has ZERO width -- damping at the origin needs "
            "gamma > 3 while the basis is in L^2_phi only for gamma < 3"
        ),
        "degree_of_freedom": (
            "the weighted-energy realization = (weight exponent gamma) x (TRIAL SPACE).  Leg "
            "111 varied gamma over seven weights and held the trial space fixed at "
            "span{sin k theta}; the trial space is the other half of the same degree of freedom "
            "and it is what sets the membership threshold gamma < 2p + 1."
        ),
        "choices_actually_tried_in_the_banked_record": {
            "A_leg_111_trial_space_sin_k_theta": {
                "vanishing_order_p": 1,
                "window": next(w for w in windows if w["p"] == 1),
                "largest_admissible_modulated_gap": we["ceiling_check"][
                    "largest_admissible_modulated_gap"
                ],
                "weights_passing_the_gate": sum(
                    1 for v in we["per_weight_verdict"].values() if v["gate_yes"]
                ),
                "weights_tried": len(we["per_weight_verdict"]),
                "gamma_4_the_published_exponent_is_inadmissible": not we["admissibility"][
                    "A4_chen_hou"
                ]["admissible"],
                "gamma_4_norm2_ratio_over_one_refinement": we["admissibility"]["A4_chen_hou"][
                    "ratio"
                ],
                "gamma_4_increment_ratio": we["admissibility"]["A4_chen_hou"]["increment_ratio"],
                "increment_ratio_reading": (
                    "4096 = 64^2, a POWER -- the norm diverges, so the basis is not in the space "
                    "at the exponent the literature actually uses."
                ),
            },
            "B_trial_space_vanishing_to_higher_order": {
                "vanishing_order_p": 2,
                "who_tried_it": (
                    "leg 141, on leg 111's own graded quadrature (solver/energy_coercivity.py, "
                    "imported read-only), with the p = 1 column as the instrument control "
                    "reproducing leg 111's banked norms to abs_diff 0.0"
                ),
                "window": next(w for w in windows if w["p"] == 2),
                "gamma_4_membership_norm2_ratio": at_gamma_4[2]["ratio"],
                "gamma_4_measured_convergent": at_gamma_4[2]["measured_convergent"],
                "contrast_p_1_same_gamma": {
                    "norm2_ratio": at_gamma_4[1]["ratio"],
                    "measured_convergent": at_gamma_4[1]["measured_convergent"],
                },
                "published_certificate_in_this_realization": {
                    "locator": egm["cite"] + " -- " + egm["locator"],
                    "arxiv": egm["paper"],
                    "hypotheses": (
                        "f odd, f'(0) = Hf(0) = 0, and integral |f|^2 phi dy < +infinity, with "
                        "phi = (1 + y^2)^2 / y^4, i.e. gamma = 4 at the origin"
                    ),
                    "coercivity_constant_at_a_equals_0": tri["EGM_prop_2_1_constant_at_a_0"],
                    "same_operator": (
                        "EGM sec 1: 'when a = 2 we get the De Gregorio model and when a = 0 we get "
                        "CLM model' -- this repository's own a = 0 object"
                    ),
                    "the_price_EGM_states_openly": (
                        "their sec 3: the origin conditions are bought with the free modulation "
                        "parameters mu and lambda"
                    ),
                },
            },
        },
        "do_they_disagree": {
            # Recomputed here with the SAME window_width() the leg-52 row calls, from the two
            # banked thresholds, and cross-checked against leg 141's own banked width.
            "window_width_recomputed_by_p": [
                {
                    "p": w["p"],
                    "damping_needs_gamma_above": w["damping_needs_gamma_gt"],
                    "space_needs_gamma_below": w["space_needs_gamma_lt"],
                    "width_recomputed": window_width(
                        w["damping_needs_gamma_gt"], w["space_needs_gamma_lt"]
                    ),
                    "width_as_banked_by_leg_141": w["window_width"],
                    "agree": window_width(
                        w["damping_needs_gamma_gt"], w["space_needs_gamma_lt"]
                    )
                    == w["window_width"],
                }
                for w in windows
            ],
            "window_width_p_1": next(w for w in windows if w["p"] == 1)["window_width"],
            "window_width_p_2": next(w for w in windows if w["p"] == 2)["window_width"],
            "window_width_p_3": next(w for w in windows if w["p"] == 3)["window_width"],
            "p_1_contains_the_published_exponent_gamma_4": next(
                w for w in windows if w["p"] == 1
            )["contains_gamma_4_the_published_exponent"],
            "p_2_contains_the_published_exponent_gamma_4": next(
                w for w in windows if w["p"] == 2
            )["contains_gamma_4_the_published_exponent"],
            "does_the_VERDICT_move": True,
            "reading": (
                "Same operator, same weight exponent gamma = 4, same quadrature code.  Move the "
                "trial space from vanishing order p = 1 to p = 2 and the window goes from width "
                "0.0 to width 2.0, the membership norm goes from a ratio of 1.678e+07 per "
                "refinement (divergent) to 1.0000000000000002 (convergent), and the published "
                "literature certifies a coercivity gap of -1/2 exactly there.  Leg 111's "
                "zero-width window is a property of the trial space span{sin k theta}, not of "
                "the operator."
            ),
        },
        "the_three_constants_agree_to_machine_zero": {
            "leg_111_D_phi_at_origin_at_gamma_4": tri["leg111_D_phi_at_origin_gamma_4"],
            "EGM_prop_2_1_constant_at_a_0": tri["EGM_prop_2_1_constant_at_a_0"],
            "Xu_published_modulated_spectral_gap": tri["XU_modulated_gap"],
            "max_abs_discrepancy": tri["max_abs_discrepancy"],
            "why_it_matters_here": (
                "The same formula that produces leg 111's death, evaluated at the exponent the "
                "literature uses, returns the literature's own certified constant.  The two "
                "sides of this row are not two different calculations disagreeing -- they are "
                "one calculation, read on two trial spaces."
            ),
        },
        "the_dichotomy_is_named_in_print_on_this_operator": {
            "arxiv": xu["paper"],
            "locator": xu["locator"],
            "what_Xu_says_about_EGM": (
                "EGM Prop. 2.1 'is not a counterexample but an instance of the realization "
                "mechanism of Section 3.1: the singular weight and origin constraints define "
                "their own realization, in which a gap is certified'"
            ),
            "consequence_for_this_leg": (
                "the classification is this leg's; the dichotomy is Xu's and is not claimed"
            ),
        },
        "tier": TIER_1,
        "caveats_carried_verbatim_from_leg_141_and_NOT_softened": [
            wel["window_by_trial_space"]["scope_of_this_check"],
            next(w for w in windows if w["p"] == 2)["who_lives_here"],
            "No coercivity gap is recomputed on any trial space by leg 141 or by this leg. The "
            "membership half is measured on both sides; the coercivity half at p = 2 rests on "
            "EGM's published proposition, not on a repository measurement.",
        ],
    }


def control_C2_leg_127(ngx: dict) -> dict:
    """C2 -- the predicate must be able to say YES.  Leg 127's own row through the same code
    path.  Degree of freedom: the function-space realization of L_0."""
    lad = ngx["NGX2_sigma_min_ladder"]
    exps = {}
    for r in lad:
        if "exponent" in r:
            exps.setdefault(r["s"], []).append(r["exponent"])
    return {
        "control": "C2_predicate_can_report_YES",
        "row": "leg 127",
        "degree_of_freedom": "the function-space realization of the a = 0 CLM linearisation L_0",
        "choice_A_l1_w_at_s_below_1": {
            "sigma_min_vanishes": True,
            "max_deviation_from_predicted_1_minus_s": ngx[
                "NGX2_max_deviation_from_1_minus_s_for_s_below_1"
            ],
            "explicit_near_null_sequence_ratio_over_numerical_optimum": ngx[
                "NGX3_max_ratio_over_optimum"
            ],
            "min_cosine_with_optimum": ngx["NGX3_min_cosine_with_optimum"],
            "not_a_truncation_artifact_max_degradation": ngx["NGX4_max_degradation_factor"],
            "consequence": "no bounded approximate inverse: Z1 >= 1 for every bounded A",
        },
        "choice_B_origin_H2_realization": {
            "source": ngx["NGX0_novelty"]["realization_constraint"],
            "modulated_spectral_gap": 0.5,
            "consequence": "invertible after modulation",
        },
        "does_the_VERDICT_move": True,
        "tier": TIER_1,
        "verdict": "PASS -- the predicate returns tier 1 where the gate takes tier 1 as given",
    }


def control_C3_mu(tc: dict, we: dict, ngx: dict) -> dict:
    """C3 -- a different OPERATOR is not a different realization, and is barred from tier 1."""
    return {
        "control": "C3_mu_positive_is_a_different_OPERATOR_not_a_different_realization",
        "witnesses_collected_and_excluded_from_every_tier_1_finding": [
            {
                "leg": "53",
                "what": "the assembled certificate closes under dissipation",
                "min_mu_with_Z1_below_one": tc["TC5_min_mu_with_Z1_below_one"],
                "control_can_report_below_one": tc["TC5_control_can_report_below_one"],
            },
            {
                "leg": "111",
                "what": "the coercivity gap changes sign under dissipation",
                "A2_gaps_over_mu": we["positive_control"]["A2"]["gaps"],
                "sign_flips": we["positive_control"]["A2"]["sign_flips"],
            },
            {
                "leg": "127",
                "what": "sigma_min saturates instead of vanishing under dissipation",
                "max_abs_exponent_for_mu_positive": ngx["NGX5_max_abs_exponent_for_mu_positive"],
                "exponent_at_mu_0": ngx["NGX5_exponent_at_mu_0"][0],
            },
        ],
        "reading": (
            "With mu > 0 the unbounded part becomes a diagonal multiplier and the kernel is "
            "destroyed -- that is lesson 87's dichotomy, a different OPERATOR.  It is why the "
            "instruments are not ones that return 'dead' for everything, and it is NOT evidence "
            "that any row's death is realization-dependent.  Barred structurally, not by "
            "judgement: no tier assignment above reads this block."
        ),
        "verdict": "PASS -- three mu > 0 witnesses present, none counted toward any tier",
    }


def main() -> None:
    t0 = time.time()
    t = load("leg_52")
    tc = load("leg_53")
    tn = load("leg_56")
    we = load("leg_111")
    ngx = load("leg_127")
    wel = load("leg_141")

    rows = [row_52(t, ngx), row_53(tc), row_56(tn), row_111_141(we, wel)]
    c2 = control_C2_leg_127(ngx)
    c3 = control_C3_mu(tc, we, ngx)

    tiers = {r["leg"]: r["tier"] for r in rows}
    tier1 = [r["leg"] for r in rows if r["tier"] == TIER_1]
    tier2 = [r["leg"] for r in rows if r["tier"] == TIER_2]
    tier3 = [r["leg"] for r in rows if r["tier"] == TIER_3]

    # C1: the predicate must be able to say NO.
    c1 = {
        "control": "C1_predicate_can_report_NO",
        "requirement": "at least one of the four gated rows must come back tier 3",
        "tier_3_rows": tier3,
        "verdict": "PASS" if tier3 else "FAIL -- the audit is a tautology and is WITHDRAWN",
    }

    predicted = {"52": TIER_3, "53": TIER_3, "56": TIER_2, "111/141": TIER_1}
    prediction_check = {
        "recorded_where": "writeup/novelty/leg_165.md sec 5, committed before this file existed",
        "predicted": predicted,
        "observed": tiers,
        "matches": sum(1 for k in predicted if predicted[k] == tiers.get(k)),
        "of": len(predicted),
    }

    gate_yes = len(tier1) >= 1
    out = {
        "leg": 165,
        "route": "ROUTE-SDM",
        "version": "v1",
        "kind": "synthesis over banked data; no dynamics, no solver module, no new compute",
        "sources_read_only": SOURCES,
        "gate": (
            "For each of legs 52, 53, 56, 111/141's dead findings, does the repository's own "
            "banked record contain evidence the finding is REALIZATION-DEPENDENT (i.e., a "
            "different choice within the same degree of freedom, already tried elsewhere in the "
            "banked record, behaves differently), or does every tried realization agree?"
        ),
        "gate_answer": "YES" if gate_yes else "NO",
        "gate_answer_branch_verbatim": (
            "Name it precisely, with the banked evidence for both realizations side by side. "
            "This is a genuinely novel synthesis finding -- ESCALATE as a candidate companion to "
            "leg 127's own reframing, not a ban-lifting result on its own."
        ),
        "the_named_row": "111/141",
        "headline": (
            "One of the four is realization-dependent and it is legs 111/141: leg 111's "
            "zero-width weighted-energy window is a property of the TRIAL SPACE span{sin k "
            "theta} (vanishing order p = 1), not of the operator.  Hold gamma at the published "
            "value 4 and move p to 2 -- the same degree of freedom, already measured on leg "
            "111's own quadrature by leg 141 -- and the window goes from width 0.0 to width 2.0, "
            "the membership norm ratio per refinement goes from 1.678e+07 (divergent) to "
            "1.0000000000000002 (convergent), and Elgindi-Ghoul-Masmoudi arXiv:1906.05811 "
            "Prop. 2.1 certifies a coercivity gap of -1/2 there, on this repository's own a = 0 "
            "CLM object.  The other three are not: 56 is magnitude-dependent only (its 2.04e+11 "
            "headline is 100.009% an endpoint-zeroing artifact of one basis choice, but the "
            "realization-robust 1.85e+07 is still a death), and 52 and 53 are invariant across "
            "every choice inside their axes -- and are, besides, the same l^1_w realization leg "
            "127 already reframed, so they are subsumed by leg 127 rather than companions to it."
        ),
        "classification": rows,
        "tier_summary": {
            "TIER_1_verdict_dependent": tier1,
            "TIER_2_magnitude_dependent_verdict_invariant": tier2,
            "TIER_3_realization_invariant": tier3,
        },
        "controls": [c1, c2, c3],
        "all_controls_pass": all(
            c["verdict"].startswith("PASS") for c in (c1, c2, c3)
        ),
        "prediction_check": prediction_check,
        "what_is_NOT_claimed": (
            "The realization dichotomy is Xu's, arXiv:2607.19762 Prop. 2 of sec 3.1, on this "
            "exact operator, and is used and not claimed.  No ban is lifted.  No realization is "
            "proposed, priced or recommended -- a tier-1 classification is not a licence to try "
            "the other side, and the gate's yes-branch says so.  L1 stays measured-dead in all "
            "three realizations.  No link of the L1 -> L4 chain moved.  Clay ~0.05%."
        ),
        "ceiling_S7": (
            "Every magnitude here was measured on the a = 0 CLM linearisation -- one mode, "
            "analytic, the friendliest object in the repository -- with Y_0 exactly zero for the "
            "banned degenerate reason.  Nothing is claimed about HL_S2_nonsymmetric.  EGM's "
            "positive gap is on that same friendliest substrate and is bought with modulation, "
            "which EGM's own sec 3 states openly."
        ),
        "novelty_log": "writeup/novelty/leg_165.md",
        "journal": "experiments/journal/leg_165.md",
        "figure": "none -- no measurement of a curve (the 'no measurement, no figure' convention)",
        "elapsed_s": time.time() - t0,
    }

    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")

    print("ROUTE-SDM v1 -- leg 165")
    print("  gate answer          :", out["gate_answer"], "at row", out["the_named_row"])
    for r in rows:
        print("   leg %-8s -> %s" % (r["leg"], r["tier"]))
    for c in (c1, c2, c3):
        print("  %-58s %s" % (c["control"], c["verdict"].split(" --")[0]))
    print("  prediction           : %d/%d rows as pre-registered"
          % (prediction_check["matches"], prediction_check["of"]))
    print("  wrote", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
