#!/usr/bin/env python3
"""Leg 273 -- Route-NFS: what are leg 255's two non-fluid survivors actually worth?

SCOPING ONLY. Nothing is built, no certificate is constructed, no solver module is
instantiated or imported. This module evaluates two CLOSED-FORM profiles and one
weighted integral, and derives every verdict from recorded evidence fields.

The question, from DIRECTION.md sec 273:

  Do leg 255's two survivors (KS3D-EXPLICIT, KS3D-NONEXPLICIT) fill an EMPTY cell of
  leg 174's occupancy matrix, or do they duplicate DF-CGL's already-occupied
  dissipative-non-fluid cell?  For each survivor: (1) which cell exactly; (2) what a
  certificate would need to show and in what space; (3) whether its blow-up evidence
  tier survives full-text scrutiny; (4) the honest distance from Clay.

GATE
  Does at least one survivor occupy a genuinely EMPTY cell (not DF-CGL's, not any
  occupied one) AND carry a statable certificate target?

Verdicts are COMPUTED from the evidence rows (lesson 90), not asserted.  self_test()
perturbs the evidence and reaches every outcome code including BOTH gate branches.
assert_probe_is_live() fails the run outright if the measurement degenerates.

Reads (never edits): writeup/data/p2_route_p1a_v1_census.json.
Territory: experiments/p2_route_nfs_v1_scoping.py, writeup/data/p2_route_nfs_v1_scoping.json,
writeup/novelty/leg_273.md, experiments/journal/leg_273.md.
"""

from __future__ import annotations

import json
import math
import os
from typing import Callable

# --------------------------------------------------------------------------------------
# Locators.  Every number below that comes from a paper is pinned to a file + line.
# --------------------------------------------------------------------------------------

LOCATORS = {
    "breden_chu": {
        "arxiv": "2404.04054",
        "title": "Constructive proofs for some semilinear PDEs on H^2(e^{|x|^2/4}, R^d)",
        "authors": "Maxime Breden, Hugo Chu",
        "pdf_md5": "ff7a34b776bfe5edf97397e5eabdbb7a",
        "pdf_md5_matches_leg_255_pin": True,
        "text_extraction_md5": "4e7f064859e924244ad19b5bb0888a67",
        "extraction_lines": 2060,
        "equation_2_line": 84,
        "equation_2_verbatim": "Lu := -\\Delta u - (x/2) . \\nabla u = f(x, u, \\nabla u),  x in R^d",
        "corollary_17i_line": 601,
        "corollary_17i_verbatim": (
            "(i) If d in {1, 2, 3}, u in H^2(mu) ==> e^{|x|^2/8} u in L^infty(R^d)."
        ),
        "lemma_19_line": 609,
        "lemma_19_constants_d3": {"C0": 0.52319, "C1": 1.0228, "C2": 0.37467},
        "remark_18_line": 607,
        "remark_18_verbatim": (
            "Note that these embeddings are sufficient to cover the range of exponent p for "
            "the semilinear heat equation for which RAPIDLY DECAYING self-similar solutions "
            "are known to exist"
        ),
        "remark_40_line": 1687,
        "delta_inverse_caveat_line": 191,
        "delta_inverse_caveat_verbatim": (
            "the operator \\Delta alone does not have a well-behaved inverse with respect to "
            "this basis"
        ),
        "sign_slip_note": (
            "line 191's prose writes L := -Delta + (x/2).grad; the abstract (line 20) and the "
            "NUMBERED equation (2) (line 84) both give -Delta - (x/2).grad.  Two against one, "
            "so equation (2) is authoritative and line 191 is recorded as a slip, not resolved "
            "silently."
        ),
        "occurrences_of_blow": 1,
        "occurrence_of_blow_line": 1925,
        "occurrence_of_blow_context": "bibliography entry [16], Chen & Hou",
        "occurrences_of_backward": 0,
    },
    "gs_2209_11206": {
        "arxiv": "2209.11206",
        "title": "Stable singularity formation for the Keller-Segel system in three dimensions",
        "authors": "Irfan Glogic, Birgit Schoerkhuber",
        "pdf_md5": "4823d47f876be553ae8b3e380a015e0c",
        "extraction_lines": 2721,
        "equation_1_5_line": 107,
        "equation_1_5_verbatim": (
            "u_T(t,x) := (1/(T-t)) U(x/sqrt(T-t)),  where "
            "U(x) = 4(d-2)(2d + |x|^2) / (2(d-2) + |x|^2)^2"
        ),
        "explicit_profile_attributed_to": "reference [8] (Brenner et al.)",
        "interval_arithmetic_occurrences": 0,
        "computer_occurrences": 0,
    },
    "cz_2406_11358": {
        "arxiv": "2406.11358",
        "title": (
            "On the stability of Type I self-similar blowups for the Keller-Segel system in "
            "three dimensions and higher"
        ),
        "authors": "Charles Collot, Kaiqiang Zhang",
        "pdf_md5": "6febdf2a3242f0ee187d237161bdedaf",
        "extraction_lines": 3643,
        "theorem_1_1_line": 289,
        "theorem_1_1_scope": "Radial stability of U0 (the EXPLICIT profile). d = 3, or d >= 4 with N0 = 1.",
        "theorem_1_3_line": 350,
        "theorem_1_3_scope": (
            "Finite Lipschitz codimensional radial stability of U_n (the NON-EXPLICIT family), "
            "3 <= d <= 9, n >= 1; codimension = N_n - 1."
        ),
        "remark_1_4_line": 409,
        "remark_1_4_verbatim": (
            "The profile U1 has from numerical simulations N1 = 2 instable modes [8]. So IF "
            "N1 = 2 HOLDS RIGOROUSLY the set of Theorem 1.3 is a hypersurface."
        ),
        "interval_arithmetic_occurrences": 0,
        "computer_occurrences": 0,
    },
    "nwz_2503_02263": {
        "arxiv": "2503.02263",
        "title": (
            "Infinitely many self-similar blow-up profiles for the Keller-Segel system in "
            "dimensions 3 to 9"
        ),
        "authors": "Van Tien Nguyen, Zhi-An Wang, Kaiqiang Zhang",
        "pdf_md5": "e028431d7e0a2a80ee26d7260a1cc44d",
        "extraction_lines": 3270,
        "reduced_mass_line": 490,
        "reduced_mass_verbatim": "Phi(r) = (1 / (2 r^d)) * int_0^r U(s) s^{d-1} ds",
        "equation_2_2_line": 525,
        "equation_2_2_verbatim": (
            "\\Delta Phi - (1/2) Lambda Phi + 2 d Phi^2 + y . \\nabla(Phi^2) = 0,  y in R^{d+2},"
            "   with Lambda u := 2u + y . \\nabla u"
        ),
        "equation_2_3_line": 544,
        "equation_2_3_verbatim": "Phibar_2 = 1/|y|^2,   Phibar_3 = 2 / (2(d-2) + |y|^2)",
        "far_field_verbatim": (
            "the infinitely many backward self-similar profiles approximate the rescaling "
            "radial steady-state near the origin and 2(d-2)/|x|^2 at spatial infinity"
        ),
        "distinct_from_brenner_line": 447,
        "interval_arithmetic_occurrences": 0,
        "computer_occurrences": 0,
    },
    "leg_174_matrix": {
        "where": "experiments/journal/leg_174.md lines 53-56, writeup/data/p2_route_vbs_v1_scoping.json",
        "grade_A": "the certificate is ON the dissipative object -- the enclosed equation itself carries dissipation",
        "grade_B": "the THEOREM is about the dissipative PDE, but the enclosed object is an inviscid auxiliary",
    },
    "leg_261_c5": {
        "where": "experiments/p2_route_p1a2_v1_census2.py, measure_keller_segel_control_d3",
        "witness_used": "u = exp(-|x|^2)  -- a GAUSSIAN stand-in, not the blow-up profile",
        "what_it_measured": "the NONLINEARITY's mapping into L^2(mu); reported in_L2_mu = True",
        "what_it_did_not_measure": "MEMBERSHIP of the actual (algebraically decaying) profile in H^2(mu)",
    },
}

MU_GROWTH = 0.25   # mu = e^{|x|^2 / 4}
COR17_RATE = 0.125  # Corollary 17(i)'s pointwise witness factor e^{|x|^2 / 8}

# The exact knife edge: u ~ e^{-a r^2} lies in L^2(mu) iff 2a > 1/4, i.e. a > 1/8.
CRITICAL_GAUSSIAN_RATE = MU_GROWTH / 2.0


# --------------------------------------------------------------------------------------
# The two survivors, as closed-form profiles.
# --------------------------------------------------------------------------------------

def U_explicit(r: float, d: int = 3) -> float:
    """Brenner et al.'s explicit profile, arXiv:2209.11206 eq (1.5) line 107.

    U(x) = 4(d-2)(2d + |x|^2) / (2(d-2) + |x|^2)^2.   Far field ~ 4(d-2)/r^2.
    """
    return 4.0 * (d - 2) * (2.0 * d + r * r) / (2.0 * (d - 2) + r * r) ** 2


def U_nonexplicit_farfield(r: float, d: int = 3) -> float:
    """The NON-explicit family's proved far-field asymptote, arXiv:2503.02263.

    U_n(r) -> 2(d-2)/r^2 as r -> infinity.  The family members are not closed form, so the
    membership question is decided by the tail the paper PROVES they have, which is the
    only part of them that matters for an L^2(mu)-weight with GROWING weight.
    """
    return 2.0 * (d - 2) / (r * r) if r > 0 else float("inf")


def Phi_bar_3(r: float, d: int = 3) -> float:
    """The reduced-mass explicit solution, arXiv:2503.02263 eq (2.3) line 544, in R^{d+2}."""
    return 2.0 / (2.0 * (d - 2) + r * r)


def gaussian_control(r: float, d: int = 3) -> float:
    """Leg 261's C5 witness, u = e^{-|x|^2}.  The LIVE-PROBE control: must come out FINITE."""
    return math.exp(-r * r)


def knife_edge_control(r: float, d: int = 3) -> float:
    """u = e^{-r^2/8}: the EXACT threshold of L^2(mu) membership.  Must come out DIVERGENT
    (marginally): 2a = 1/4 = the weight's growth, so the weighted density is r^{d-1}, whose
    integral diverges.  Present to show the probe resolves the threshold rather than merely
    separating 'Gaussian' from 'algebraic'."""
    return math.exp(-CRITICAL_GAUSSIAN_RATE * r * r)


# --------------------------------------------------------------------------------------
# The measurement, entirely in log10 so nothing overflows.
# --------------------------------------------------------------------------------------

LOG10E = 1.0 / math.log(10.0)


def log10_weighted_density(profile: Callable[[float, int], float], r: float, d: int) -> float:
    """log10 of |u(r)|^2 * e^{r^2/4} * r^{d-1}, the integrand of ||u||_{L^2(mu)}^2 in radial form."""
    v = abs(profile(r, d))
    if v == 0.0:
        return float("-inf")
    return 2.0 * math.log10(v) + MU_GROWTH * r * r * LOG10E + (d - 1) * math.log10(r)


def log10_cor17_witness(profile: Callable[[float, int], float], r: float, d: int) -> float:
    """log10 of e^{r^2/8} |u(r)|.  Corollary 17(i) says this is BOUNDED for every u in H^2(mu).
    If it diverges, u is not in H^2(mu) -- a theorem-level exclusion, not a heuristic."""
    v = abs(profile(r, d))
    if v == 0.0:
        return float("-inf")
    return math.log10(v) + COR17_RATE * r * r * LOG10E


def log10_truncated_weighted_mass(
    profile: Callable[[float, int], float], R: float, d: int, n: int = 20000
) -> float:
    """log10 of int_0^R |u|^2 e^{r^2/4} r^{d-1} dr, by log-sum-exp over a uniform grid."""
    h = R / n
    terms = []
    for k in range(1, n + 1):
        r = k * h
        terms.append(log10_weighted_density(profile, r, d))
    finite = [t for t in terms if t > float("-inf")]
    if not finite:
        return float("-inf")
    m = max(finite)
    s = sum(10.0 ** (t - m) for t in finite)
    return m + math.log10(s) + math.log10(h)


RADII = [1.0, 2.0, 4.0, 8.0, 16.0, 32.0]
TRUNCATIONS = [2.0, 4.0, 8.0, 16.0, 32.0]


def measure_membership(name: str, profile: Callable[[float, int], float], d: int) -> dict:
    """Measure whether `profile` lies in H^2(mu).  Verdict COMPUTED from the two divergence
    diagnostics, not asserted."""
    witness = [log10_cor17_witness(profile, r, d) for r in RADII]
    density = [log10_weighted_density(profile, r, d) for r in RADII]
    mass = [log10_truncated_weighted_mass(profile, R, d) for R in TRUNCATIONS]

    # Divergence is decided by MONOTONE GROWTH over the last three measured radii, not by a
    # single value.  The two diagnostics are INDEPENDENT necessary conditions and are combined
    # by OR, not AND:
    #
    #   * a divergent Corollary-17(i) witness excludes u at THEOREM level (contrapositive of a
    #     necessary condition proved in arXiv:2404.04054);
    #   * a divergent weighted mass excludes u DIRECTLY, from the definition of L^2(mu).
    #
    # Neither implies the other, and the knife-edge control e^{-r^2/8} is exactly the object
    # that shows it: its Corollary-17 witness is bounded (identically 1) while its weighted
    # mass diverges like R^d.  An AND rule would wrongly admit it -- this was caught by
    # assert_probe_is_live() before anything was banked on it.
    witness_growing = witness[-1] > witness[-2] > witness[-3]
    mass_growing = mass[-1] > mass[-2] > mass[-3]
    witness_span = witness[-1] - witness[0]
    mass_span = mass[-1] - mass[0]

    in_space = not (witness_growing or mass_growing)
    if witness_growing and mass_growing:
        excluded_by = "BOTH -- Corollary 17(i) witness AND weighted L^2(mu) mass"
    elif witness_growing:
        excluded_by = "Corollary 17(i) witness (theorem-level)"
    elif mass_growing:
        excluded_by = "weighted L^2(mu) mass (definitional)"
    else:
        excluded_by = None

    return {
        "object": name,
        "ambient_dimension": d,
        "radii": RADII,
        "log10_cor17_witness_e_r2_over_8_times_u": witness,
        "log10_weighted_density": density,
        "truncation_radii": TRUNCATIONS,
        "log10_truncated_weighted_mass": mass,
        "cor17_witness_monotone_growing": witness_growing,
        "weighted_mass_monotone_growing": mass_growing,
        "log10_witness_span_over_measured_radii": witness_span,
        "log10_mass_span_over_measured_truncations": mass_span,
        "in_H2_mu": in_space,
        "excluded_by": excluded_by,
        "underflow_note": (
            "a -inf entry is an exact floating-point underflow to 0.0, not a missing "
            "measurement; it is the strongest possible form of the convergent verdict.  Leg "
            "261 recorded the same underflow for its C0 control."
        ),
        "decided_by": (
            "arXiv:2404.04054 Corollary 17(i) line 601: u in H^2(mu) ==> e^{|x|^2/8} u in "
            "L^infty(R^d).  A divergent witness is therefore a THEOREM-LEVEL exclusion."
        ),
    }


# --------------------------------------------------------------------------------------
# Leg 174's occupancy matrix, and where a KS certificate would land.
# --------------------------------------------------------------------------------------

OCCUPANCY = {
    ("fluid", "A"): [],
    ("fluid", "B"): ["arXiv:2208.09445 (BCG, 3D compressible Navier-Stokes)"],
    ("nonfluid", "A"): [
        "arXiv:2410.05480 (Dahne-Figueras, CGL) -- leg 174",
        "arXiv:1610.09496 (Biernat-Donninger, harmonic map heat flow, 2016) -- leg 255",
    ],
    ("nonfluid", "B"): [],
}


def classify_cell(row: dict) -> dict:
    """Which cell of leg 174's matrix would a certificate on this row occupy?  Derived from
    the row's own evidence fields."""
    fluid = "fluid" if row["fluid_adjacent"] else "nonfluid"
    # Grade A iff the enclosed object's own equation carries the dissipation.
    grade = "A" if row["profile_equation_carries_dissipation"] else "B"
    occupants = OCCUPANCY[(fluid, grade)]
    return {
        "cell": f"(fluid={row['fluid_adjacent']}, grade={grade})",
        "fluid_adjacent": row["fluid_adjacent"],
        "grade": grade,
        "grade_reason": (
            "the profile equation carries Delta at the same order as the drift (Type I / "
            "scale-invariant dissipation), so the enclosed object is itself dissipative"
            if grade == "A"
            else "the enclosed object would be an inviscid auxiliary"
        ),
        "existing_occupants": occupants,
        "n_existing_occupants": len(occupants),
        "cell_is_empty": len(occupants) == 0,
        "would_be_occupant_number": len(occupants) + 1,
    }


# --------------------------------------------------------------------------------------
# The two survivor rows, with their evidence.
# --------------------------------------------------------------------------------------

def survivor_rows() -> list[dict]:
    return [
        dict(
            key="KS3D-EXPLICIT",
            object=(
                "parabolic-elliptic Keller-Segel in d = 3, at Brenner et al.'s EXPLICIT "
                "self-similar blow-up profile U(x) = 4(d-2)(2d+|x|^2)/(2(d-2)+|x|^2)^2"
            ),
            fluid_adjacent=False,
            profile_equation_carries_dissipation=True,
            profile_is_closed_form=True,
            blowup_proved=True,
            blowup_tier="STABLE self-similar blow-up, PROVED",
            blowup_tier_locators=(
                "arXiv:2209.11206 (Glogic-Schoerkhuber, radial, d=3, resolves a >20-year "
                "conjecture); arXiv:2406.11358 Theorem 1.1 line 289 (radial stability of U0); "
                "arXiv:2501.07073 (nonradial)"
            ),
            stability_codimension=0,
            codimension_rigorously_known=True,
            existing_certificate=False,
            profile_farfield_exponent=-2.0,
            profile_farfield_constant_d3=4.0,
        ),
        dict(
            key="KS3D-NONEXPLICIT",
            object=(
                "parabolic-elliptic Keller-Segel in d = 3, at the NON-explicit self-similar "
                "profiles U_n (n >= 1) of arXiv:2503.02263"
            ),
            fluid_adjacent=False,
            profile_equation_carries_dissipation=True,
            profile_is_closed_form=False,
            blowup_proved=True,
            blowup_tier="FINITE-CODIMENSION stable self-similar blow-up; codimension N_n - 1",
            blowup_tier_locators=(
                "arXiv:2503.02263 (existence, matched asymptotics + Banach fixed point); "
                "arXiv:2406.11358 Theorem 1.3 line 350 (finite Lipschitz codimensional radial "
                "stability), Remark 1.4 line 409"
            ),
            stability_codimension=1,  # N_1 - 1 with N_1 = 2
            codimension_rigorously_known=False,
            codimension_caveat=(
                "arXiv:2406.11358 Remark 1.4 line 409: N_1 = 2 is taken FROM NUMERICAL "
                "SIMULATIONS, and the paper writes 'if N1 = 2 holds rigorously'.  The "
                "codimension of the only NON-vacuous target is therefore not a proved number."
            ),
            existing_certificate=False,
            profile_farfield_exponent=-2.0,
            profile_farfield_constant_d3=2.0,
        ),
    ]


# --------------------------------------------------------------------------------------
# The certificate target, per survivor: what would have to be shown, and in what space.
# --------------------------------------------------------------------------------------

def certificate_target(row: dict, membership: dict) -> dict:
    """Is there a STATABLE certificate target for this row -- an object to enclose, in a
    space it belongs to?  Computed from the row's evidence + the membership measurement."""
    has_something_to_enclose = not row["profile_is_closed_form"]

    formulations = [
        {
            "formulation": "system (u, c) in R^3",
            "equations": "u_t = Delta u - div(u grad c),  0 = Delta c + u",
            "dimension": 3,
            "inside_remark_40_dimension_range": True,
            "obstruction": (
                "the second equation requires inverting the BARE Laplacian in Breden-Chu's "
                "basis, and arXiv:2404.04054 line 191 states in its own words: 'the operator "
                "Delta alone does not have a well-behaved inverse with respect to this "
                "basis'.  Leg 255 recorded the elliptic equation as 'an extension of the "
                "setting, but not the introduction of a nonlocal term'; the extension lands "
                "on precisely the operator the paper names as ill-behaved there."
            ),
            "target_in_H2_mu": membership["in_H2_mu"],
        },
        {
            "formulation": "reduced-mass Phi in R^{d+2} = R^5",
            "equations": (
                "Delta Phi - (1/2) Lambda Phi + 2 d Phi^2 + y.grad(Phi^2) = 0, "
                "arXiv:2503.02263 eq (2.2) line 525"
            ),
            "dimension": 5,
            "inside_remark_40_dimension_range": False,
            "obstruction": (
                "d+2 = 5 exceeds Remark 40's stated d in {2,3} AND Corollary 17(i)'s d in "
                "{1,2,3}.  At d = 5 only Corollary 17(iii) applies, giving H^2(mu) subset "
                "L^p(mu) for p in [2, 2d/(d-4)] = [2, 10] -- NO L^infty.  The embedding that "
                "Remark 40's reach argument is GIVEN IN TERMS OF is unavailable in exactly "
                "the formulation that makes Keller-Segel local."
            ),
            "target_in_H2_mu": False,
            "target_farfield": "Phibar_3 ~ 2/|y|^2 (eq (2.3) line 544) -- algebraic, same exclusion",
        },
    ]

    # A target is STATABLE iff there is something to enclose AND at least one formulation
    # puts that object inside the space, in a dimension the reach clause covers.
    viable = [
        f for f in formulations
        if f["target_in_H2_mu"] and f["inside_remark_40_dimension_range"]
    ]
    statable = has_something_to_enclose and len(viable) > 0

    return {
        "has_something_to_enclose": has_something_to_enclose,
        "why_not": (
            None if has_something_to_enclose
            else "the profile is closed form; there is nothing for an interval enclosure to do"
        ),
        "what_a_certificate_would_have_to_show": (
            "existence of an exact solution U of the backward self-similar profile equation "
            "-Delta U + (y/2).grad U + U + div(U grad Phi_U) = 0 within a validated radius of "
            "a numerical approximation, via Newton-Kantorovich (Y_0, Z_0, Z_1, Z_2) bounds in "
            "a Banach space containing U -- plus, for the non-explicit family, a rigorous "
            "count of the unstable eigenmodes N_n, which arXiv:2406.11358 Remark 1.4 supplies "
            "only from numerical simulation."
        ),
        "formulations_examined": formulations,
        "n_viable_formulations": len(viable),
        "statable_certificate_target": statable,
        "drift_sign": {
            "breden_chu_operator": "-Delta - (x/2).grad   (FORWARD self-similar), eq (2) line 84",
            "keller_segel_blowup_operator": "-Delta + (y/2).grad   (BACKWARD self-similar), eq (2.2) line 525",
            "note": (
                "the drift signs are OPPOSITE.  Corroborating, not load-bearing: the exclusion "
                "below rests on Corollary 17(i), which is a statement about the space alone."
            ),
        },
        "the_space_that_would_be_needed": (
            "a space admitting ALGEBRAIC |y|^-2 tails -- i.e. NOT H^2(e^{|x|^2/4}).  Recorded "
            "as an observation only.  This leg does NOT propose it, does not name it, and does "
            "not request any ban lift; the standing re-posed ban requires a dedicated scoping "
            "leg for any namable fourth space and this is not that leg."
        ),
    }


# --------------------------------------------------------------------------------------
# The gate.
# --------------------------------------------------------------------------------------

def classify(rows: list[dict], memberships: dict) -> dict:
    per_survivor = []
    for row in rows:
        cell = classify_cell(row)
        mem = memberships[row["key"]]
        cert = certificate_target(row, mem)
        per_survivor.append(
            {
                "key": row["key"],
                "row": row,
                "matrix_cell": cell,
                "membership": mem,
                "certificate_target": cert,
                "occupies_empty_cell": cell["cell_is_empty"],
                "carries_statable_target": cert["statable_certificate_target"],
                "passes_gate": cell["cell_is_empty"] and cert["statable_certificate_target"],
            }
        )

    passers = [s for s in per_survivor if s["passes_gate"]]
    empty_cell = [s for s in per_survivor if s["occupies_empty_cell"]]
    statable = [s for s in per_survivor if s["carries_statable_target"]]

    if passers:
        code = "SURVIVOR_IN_EMPTY_CELL_WITH_STATABLE_TARGET"
        answer = "YES"
    elif empty_cell and not statable:
        code = "EMPTY_CELL_BUT_NO_STATABLE_TARGET"
        answer = "NO"
    elif statable and not empty_cell:
        code = "STATABLE_TARGET_BUT_CELL_IS_OCCUPIED"
        answer = "NO"
    else:
        code = "BOTH_CONJUNCTS_FAIL_DUPLICATION_AND_DEFICIENCY"
        answer = "NO"

    return {
        "per_survivor": per_survivor,
        "n_survivors": len(per_survivor),
        "n_in_empty_cell": len(empty_cell),
        "n_with_statable_target": len(statable),
        "n_passing_gate": len(passers),
        "verdict_code": code,
        "gate_answer": answer,
    }


# --------------------------------------------------------------------------------------
# Live-probe assertion and self test.
# --------------------------------------------------------------------------------------

def assert_probe_is_live(memberships: dict) -> dict:
    """Fail the run outright if the measurement degenerates into 'everything is excluded'."""
    checks = {}

    g = memberships["GAUSSIAN-CONTROL"]
    checks["gaussian_control_is_IN_the_space"] = g["in_H2_mu"]
    if not g["in_H2_mu"]:
        raise AssertionError(
            "PROBE DEAD: the Gaussian control e^{-|x|^2} (leg 261's C5 witness) must lie in "
            "H^2(mu).  If it does not, the measurement excludes everything and decides nothing."
        )

    k = memberships["KNIFE-EDGE-CONTROL"]
    checks["knife_edge_control_is_OUT_of_the_space"] = not k["in_H2_mu"]
    if k["in_H2_mu"]:
        raise AssertionError(
            "PROBE DEAD: e^{-r^2/8} sits exactly on the L^2(mu) threshold (2a = 1/4) and must "
            "come out EXCLUDED.  If it does not, the probe cannot resolve the threshold and is "
            "merely separating 'Gaussian' from 'algebraic'."
        )

    e = memberships["KS3D-EXPLICIT"]
    checks["explicit_profile_is_OUT_of_the_space"] = not e["in_H2_mu"]

    # Both discriminating outcomes must actually occur.
    outcomes = {m["in_H2_mu"] for m in memberships.values()}
    checks["both_outcomes_occur"] = outcomes == {True, False}
    if outcomes != {True, False}:
        raise AssertionError(
            "PROBE DEAD: every object measured came out the same way.  A membership test that "
            "cannot come out both ways is a property of the code, not of the objects."
        )

    return checks


def self_test() -> dict:
    """Perturb the evidence and confirm every outcome code is REACHABLE, including the
    gate's yes-branch.  Nothing here is banked as a finding."""
    memberships = _measure_all()
    outcomes = {}

    base = classify(survivor_rows(), memberships)
    outcomes[base["verdict_code"]] = "as measured"

    # (1) Force the yes-branch: pretend the matrix cell were empty AND the profile lay in the
    # space.  The answer this leg would most have liked, reachable on perturbed evidence.
    rows = survivor_rows()
    fake_mem = {k: dict(v) for k, v in memberships.items()}
    fake_mem["KS3D-NONEXPLICIT"]["in_H2_mu"] = True
    saved = OCCUPANCY[("nonfluid", "A")]
    OCCUPANCY[("nonfluid", "A")] = []
    try:
        r1 = classify(rows, fake_mem)
        outcomes[r1["verdict_code"]] = "reached by emptying the cell AND granting membership"
    finally:
        OCCUPANCY[("nonfluid", "A")] = saved

    # (2) Empty cell but no statable target.
    OCCUPANCY[("nonfluid", "A")] = []
    try:
        r2 = classify(survivor_rows(), memberships)
        outcomes[r2["verdict_code"]] = "reached by emptying the cell only"
    finally:
        OCCUPANCY[("nonfluid", "A")] = saved

    # (3) Statable target but occupied cell.
    fake_mem2 = {k: dict(v) for k, v in memberships.items()}
    fake_mem2["KS3D-NONEXPLICIT"]["in_H2_mu"] = True
    r3 = classify(survivor_rows(), fake_mem2)
    outcomes[r3["verdict_code"]] = "reached by granting membership only"

    return {
        "outcome_codes_reached": sorted(outcomes),
        "n_outcome_codes_reached": len(outcomes),
        "how": outcomes,
        "yes_branch_reachable": "SURVIVOR_IN_EMPTY_CELL_WITH_STATABLE_TARGET" in outcomes,
    }


# --------------------------------------------------------------------------------------

def _measure_all() -> dict:
    return {
        "KS3D-EXPLICIT": measure_membership("KS3D-EXPLICIT (Brenner et al. closed form)", U_explicit, 3),
        "KS3D-NONEXPLICIT": measure_membership(
            "KS3D-NONEXPLICIT (proved far-field 2(d-2)/r^2)", U_nonexplicit_farfield, 3
        ),
        "REDUCED-MASS-PHI": measure_membership("Phibar_3 in R^{d+2} = R^5", Phi_bar_3, 5),
        "GAUSSIAN-CONTROL": measure_membership("leg 261's C5 witness e^{-|x|^2}", gaussian_control, 3),
        "KNIFE-EDGE-CONTROL": measure_membership("e^{-r^2/8}, the exact threshold", knife_edge_control, 3),
    }


def read_leg_255_census() -> dict:
    """Read-only.  Confirms this leg is scoping the rows leg 255 actually banked."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "writeup", "data", "p2_route_p1a_v1_census.json")
    with open(path) as fh:
        census = json.load(fh)
    return {
        "path": "writeup/data/p2_route_p1a_v1_census.json",
        "leg": census["leg"],
        "survivors_as_banked": census["survivors"],
        "n_candidates": census["n_candidates"],
        "gate_answer": census["gate_answer"],
    }


def main() -> dict:
    census = read_leg_255_census()
    memberships = _measure_all()
    probe = assert_probe_is_live(memberships)
    rows = survivor_rows()
    result = classify(rows, memberships)
    st = self_test()

    assert set(census["survivors_as_banked"]) == {r["key"] for r in rows}, (
        "this leg must scope exactly the rows leg 255 banked"
    )

    out = {
        "leg": 273,
        "route": "NFS",
        "run_date": "2026-08-07",
        "question": (
            "Do leg 255's two non-fluid survivors fill an EMPTY cell of leg 174's occupancy "
            "matrix, or duplicate DF-CGL's already-occupied dissipative-non-fluid cell?"
        ),
        "reads_only": census,
        "locators": LOCATORS,
        "occupancy_matrix_as_of_this_leg": {
            f"fluid={k[0]},grade={k[1]}": v for k, v in OCCUPANCY.items()
        },
        "memberships": memberships,
        "probe_liveness_checks": probe,
        "result": result,
        "self_test": st,
        "gate_answer": result["gate_answer"],
        "verdict_code": result["verdict_code"],
        "gate_answer_wording": (
            "NO.  Neither survivor occupies an empty cell of leg 174's matrix -- a certificate "
            "on either would be the THIRD occupant of the already-occupied (fluid=False, "
            "grade=A) cell, behind Dahne-Figueras (CGL) and Biernat-Donninger (harmonic map "
            "heat flow, 2016).  And neither carries a statable certificate target: both "
            "profiles decay algebraically (~C/|x|^2) and are therefore excluded from "
            "H^2(e^{|x|^2/4}) by arXiv:2404.04054's OWN Corollary 17(i).  BOTH conjuncts fail, "
            "so leg 255's yes-branch produced ZERO actionable survivors."
        ),
        "secondary_goal_track": (
            "This leg's gate answered NO, so no dossier is banked as a packet candidate.  Had "
            "it answered YES it would have routed to the SECONDARY-GOAL track (useful novel "
            "findings) and NOT to the Clay path, which runs through leg 251's BCG candidate."
        ),
        "honest_ceiling": (
            "Scoping only.  Nothing built, nothing certified.  No link of the L1->L4 chain "
            "moves.  Both objects are NON-FLUID by construction -- a parabolic-elliptic "
            "chemotaxis system with no transport nonlinearity, no incompressibility, no "
            "Biot-Savart law, no pressure -- so a certificate on either, if it existed "
            "tomorrow, would not move L1, L2, L3 or L4.  Clay odds stay ~0.05%, behind Walls "
            "1 and 2, Wall 2 in its corrected form (time-dependent singularity formation, not "
            "dimension).  No stage claimed or closed; no ban lifted, narrowed or argued "
            "against; plan_of_record.py untouched."
        ),
    }
    return out


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    dest = os.path.join(here, "..", "writeup", "data", "p2_route_nfs_v1_scoping.json")
    data = main()
    with open(dest, "w") as fh:
        json.dump(data, fh, indent=1, sort_keys=False)
        fh.write("\n")

    r = data["result"]
    print("LEG 273 -- ROUTE-NFS")
    print(f"  survivors scoped              : {r['n_survivors']}")
    print(f"  in a genuinely EMPTY cell     : {r['n_in_empty_cell']}")
    print(f"  with a statable cert target   : {r['n_with_statable_target']}")
    print(f"  passing the gate (both)       : {r['n_passing_gate']}")
    for s in r["per_survivor"]:
        m = s["membership"]
        print(
            f"    {s['key']:20s} cell {s['matrix_cell']['cell']:26s} "
            f"occupants {s['matrix_cell']['n_existing_occupants']}  "
            f"in_H2(mu) {m['in_H2_mu']}  "
            f"log10 witness span {m['log10_witness_span_over_measured_radii']:+.2f}"
        )
    for k in ("GAUSSIAN-CONTROL", "KNIFE-EDGE-CONTROL", "REDUCED-MASS-PHI"):
        m = data["memberships"][k]
        print(
            f"    {k:20s} in_H2(mu) {str(m['in_H2_mu']):5s}  "
            f"log10 witness span {m['log10_witness_span_over_measured_radii']:+.2f}  "
            f"log10 mass span {m['log10_mass_span_over_measured_truncations']:+.2f}"
        )
    print(f"  self-test outcome codes       : {data['self_test']['n_outcome_codes_reached']}")
    print(f"  yes-branch reachable          : {data['self_test']['yes_branch_reachable']}")
    print(f"  VERDICT                       : {data['verdict_code']}")
    print(f"  GATE                          : {data['gate_answer']}")
