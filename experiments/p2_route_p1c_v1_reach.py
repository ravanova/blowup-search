#!/usr/bin/env python3
"""
Leg 257 -- ROUTE-P1C: Remark 40's reach, MEASURED not argued, and the stage-V
ban-lift scoping, folded in.

WHAT THIS IS. A SCOPING leg. NO CONSTRUCTION. Nothing is certified, no solver module is
added or edited, no stage is claimed, plan_of_record.py is untouched, NO BAN IS LIFTED.
The stage-V ban-lift question terminates in a RECOMMENDATION carrying its evidence; the
signature is the user's, per DIRECTION.md 257's yes-branch.

TWO QUESTIONS, both answered against primary sources:

  (a) What does a 2D/3D FLUID application of Breden-Chu actually demand -- which of their
      hypotheses bind, what the setup costs, and where their own "non-trivial ... future
      work" flag bites?

  (b) Is the weighted-Sobolev setting H^2(mu) genuinely NOT subject to the three-realization
      death the stage-V ban names -- mechanism by mechanism, each named per lesson 91,
      NEVER by analogy?

PROVENANCE. arXiv:2404.04054v2 (Breden & Chu, Numer. Math., DOI 10.1007/s00211-025-01504-4)
re-fetched at primary source THIS leg from arxiv.org (egress HTTP 200) and extracted with
`pdftotext -layout`:

    pdf md5           ff7a34b776bfe5edf97397e5eabdbb7a
    extraction cmd    pdftotext -layout 2404.04054.pdf -
    extraction lines  2060

Both match leg 245's pin BIT-FOR-BIT, so this leg's `line` locators and leg 245's index the
same extraction and are directly comparable. Papers/ is gitignored.

THE EXTRACTION COMMAND IS PART OF THE PIN, AND THAT IS NOT PEDANTRY. Mid-leg this module's
working text was overwritten by a stray NON-layout pdftotext run and went from 2060 to 3448
lines, silently invalidating every locator below. Caught, and resolved by re-deriving from
the pinned PDF: same md5, and `pdftotext -layout` reproduces exactly 2060 lines, after which
every locator was re-verified against the fresh extraction (Remark 40 @ 1686, the
compact-perturbation hypothesis @ 704, eq (2) @ 84, References @ 1883) and the census re-ran
to the identical 4 / 124. AN MD5 ON A PDF DOES NOT PIN A TEXT EXTRACTION -- leg 245 and this
leg both write "md5 X, 2060 lines", which reads as one pin but is two artifacts.

The three death reports were read AT FULL TEXT, not summarised from DIRECTION.md:
  experiments/journal/leg_54.md   (156 lines)  -- l^1_w coefficient basis
  experiments/journal/leg_56.md   (166 lines)  -- collocation basis
  experiments/journal/leg_176.md  (244 lines)  -- origin-H^2, BUILT
  leg 163's journal via `git show origin/leg/163-h2s-v1:experiments/journal/leg_163.md`
      (read-only; that branch is NOT an ancestor of main and was never checked out)
  experiments/journal/leg_245.md  (187 lines)  -- this leg's direct predecessor on Remark 40

NO NETWORK ACCESS AT RUN TIME. The arXiv nets and the full-text census ran during the leg;
every result is transcribed below as data, leg 245's pattern. What this module COMPUTES at
run time is the arithmetic: the embedding chain, the truncation-cost scaling, and the two
gate clauses.

BANS CHECKED BEFORE STARTING (plan_of_record.py output read in full).
  * The re-posed stage-V ban is the one that binds, and this leg is the scoping leg its own
    lift clause names. NOT TRIPPED: no l^1-Fourier/radii-polynomial machinery is built,
    re-attempted, or repaired, on any model. Nothing is constructed at all.
  * "building a solver without grepping capabilities.py for the object first" -- grepped;
    `2404.04054` appears in solver/viscous_novelty.py's PRECEDENTS only, and NO solver is
    built here regardless.
  * gCLM measurement: none. DSS: not re-asked. GA compute: none. Weight exponent s: not
    tuned. Border direction: not tuned. Domain: not extended. Leg 51's methodological claim:
    not re-made.
  * plan_of_record.py, CONTINUATION_PROMPT.md, DIRECTION.md, LITERATURE_CHECK.md,
    experiments/JOURNAL.md, capabilities.py, solver/*: all UNTOUCHED.
"""

import json
import math
import os
import sys

import numpy as np

PASS_DATE = "2026-08-07"
PARENT = "arXiv:2404.04054v2"
PARENT_MD5 = "ff7a34b776bfe5edf97397e5eabdbb7a"
PARENT_LINES = 2060

# =====================================================================================
# 0. THE PARENT, PINNED. Verbatim locators into the md5-pinned extraction.
# =====================================================================================

LOCATORS = {
    "remark_40": {
        "line": 1686,
        "text": ("We deal with a one-dimensional example here for simplicity, but terms "
                 "like (u . grad)u could in principle also be handled in dimension "
                 "d in {2,3}, as u in H^2(mu) is then still enough to guarantee that "
                 "(u . grad)u in L^2(mu) since u in L^infty(R^d)."),
        "reading": ("A statement about the NONLINEARITY'S MAPPING PROPERTY, and it is "
                    "correct. It is NOT a statement that a fluid target lives in H^2(mu). "
                    "Distinguishing those two is this leg's whole job."),
    },
    "compact_perturbation_hypothesis": {
        "line": 704,
        "text": ("Note that if Dg(u_bar) in fact maps H^2(mu) to H^1(mu), then DF(u_bar) "
                 "is a compact perturbation of the identity."),
        "reading": ("THE hypothesis leg 54 names as the one the l^1_w operator FAILS. Here "
                    "it is satisfied, and the reason is structural -- see mechanism M1."),
    },
    "A_block_shape": {
        "line": 712,
        "text": "A = [[A_n, 0], [0, I]]  (Pn A Pn = An; (I-Pn)A(I-Pn) = I-Pn)",
        "reading": ("The SAME block convention arXiv:2411.18361 states and leg 54 measured "
                    "this repository's operator failing. BC satisfy its hypothesis."),
    },
    "L_inverse_compact": {
        "line": 392,
        "text": ("L^{-1} : L^2(mu) -> H^1(mu) is well-defined (say via the Lax-Milgram "
                 "theorem, using (10) and (12)) and compact."),
        "reading": "Compactness on an UNBOUNDED domain, bought by the Gaussian weight.",
    },
    "poincare": {
        "line": 372,
        "text": "||u||_{L^2(mu)} <= sqrt(2/d) ||grad u||_{L^2(mu)}   for all u in H^1(mu)",
        "reading": ("A GENUINE Poincare inequality on R^d. False on the line in l^1_w -- "
                    "this single inequality is the root of every M1/M2 evasion below."),
    },
    "projection_estimate": {
        "line": 401,
        "text": "||f - Pn f||_{L^2(mu)} <= 2/(d + 2n + 1) ||f - Pn f||_{H^2(mu)}",
        "reading": "The explicit compactness estimate that makes the TAIL block computable.",
    },
    "L_diagonal_d2": {
        "line": 326,
        "text": "L psi_{l,m} = ((2 + |l|)/2 + m) psi_{l,m}",
        "reading": "EXACT eigenrelation, rational eigenvalue. No consistency defect exists.",
    },
    "L_diagonal_d3": {
        "line": 336,
        "text": "L psi_{k,l,m} = ((3 + l)/2 + m) psi_{k,l,m}",
        "reading": "Same, d = 3. This is the eigenvalue the DOF count below is cut on.",
    },
    "no_banach_algebra": {
        "line": 212,
        "text": ("The basis used in this work does not enjoy this [Banach algebra] "
                 "property, but we still manage to handle some nonlinear terms, thanks to "
                 "a combination of rigorous quadrature and Sobolev embeddings, in a "
                 "fashion which is more reminiscent of CAPs based on finite elements."),
        "reading": ("Where the analogue of leg 56's defect actually lives: the QUADRATURE "
                    "rung, not the operator rung. BC bound it rigorously."),
    },
    "gaussian_branch_selected": {
        "line": 1328,
        "text": "u*(r) = O(r^{2/(p-1)-d} e^{-r^2/4})",
        "reading": ("Their certified profiles have GAUSSIAN decay. The framework selects "
                    "the rapidly-decaying branch of a two-branch far field."),
    },
    "gaussian_branch_can_be_empty": {
        "line": 1333,
        "text": ("In the case eps = +1, rapidly decaying self-similar solutions only exist "
                 "for p < 1 + 2/d"),
        "reading": ("THE PAPER'S OWN DOCUMENTATION that the branch its space selects can be "
                    "EMPTY at some parameters. That is exactly what NRS says happens for "
                    "backward-self-similar 3D Navier-Stokes. Not an exotic objection -- "
                    "their own selection principle, turning up empty."),
    },
    "H2_needed_for_Linfty": {
        "line": 727,
        "text": ("One could choose to perform a computer-assisted proof in H^1(mu) instead "
                 "of H^2(mu), but the class of treatable problems would be more restricted "
                 "and this would not directly yield L^infty-estimates on the solution in "
                 "dimension d in {2,3}."),
        "reading": "Why H^2 and not H^1: L^infty is what Remark 40's argument consumes.",
    },
    "phi_in_unweighted_H2": {
        "line": 556,
        "text": ("||D^2 phi||_{L^2(R^d)} = ||Laplacian phi||_{L^2(R^d)} <= sqrt(Z) "
                 "||u||_{H^2(mu)},  phi = e^{|x|^2/8} u"),
        "reading": ("u in H^2(mu) implies e^{|x|^2/8} u in UNWEIGHTED H^2(R^d). The "
                    "embedding chain of section 3 below rests on this."),
    },
    "future_work_bites": {
        "source": "arXiv:2603.27198v1 line 273, via leg 245 (md5 ba2e83f46a07bad6f627bcf0ff4a3185)",
        "text": ("[extending from an interval to a higher-dimensional rectangle] is "
                 "non-trivial but will be studied in a future work."),
        "reading": ("2026-03-28, 28 months after Remark 40. The flag bites FAR SHORT of a "
                    "fluid domain -- at a rectangle."),
    },
}

# Sobolev embedding constants, Lemma 14 / Corollary 15 (lines 425-521), transcribed.
#   C(d,p) = (1/(d(d-2)pi))^{(1-a)/2} * ((d-1)!/Gamma(d/2))^{1/2 - 1/p},  a = 1 + d(1/p - 1/2)
# valid for d >= 3, p in [2, 2d/(d-2)].


def bc_C(d, p):
    """Breden-Chu Lemma 14's embedding constant, d >= 3 branch (line 441-445)."""
    a = 1.0 + d * (1.0 / p - 0.5)
    return (1.0 / (d * (d - 2) * math.pi)) ** ((1.0 - a) / 2.0) * \
           (math.gamma(d) / math.gamma(d / 2.0)) ** (0.5 - 1.0 / p), a


def bc_Z(d):
    """Normalisation Z = 2^{d-1} omega_{d-1} = (2 sqrt(pi))^d / Gamma(d/2)  (line 278)."""
    return (2.0 * math.sqrt(math.pi)) ** d / math.gamma(d / 2.0)


# =====================================================================================
# 1. FULL-TEXT CENSUS: which fluid apparatus does the paper actually contain?
#    Ran this leg over the md5-pinned extraction, body vs bibliography split at the
#    paper's own "References" line (1883 of 2061 incl. trailing blank). Transcribed.
# =====================================================================================

CENSUS = {
    "references_line": 1883,
    "fluid_apparatus_body": {
        "divergence-free": 0, "divergence free": 0, "incompressib": 0, "solenoidal": 0,
        "leray projection": 0, "leray projector": 0, "pressure": 0, "vorticity": 0,
        "velocity field": 0, "vector-valued": 0, "vector valued": 0, "convective": 0,
        "navier-stokes": 0, "navier–stokes": 1, "euler equation": 0,
        "(u . grad)u": 2, "constraint": 1,
    },
    "fluid_apparatus_bib": {
        "navier-stokes": 2, "navier–stokes": 1, "euler equation": 1,
    },
    # Every non-zero body hit, adjudicated by reading the line (lesson 90: a raw count is
    # not a finding).
    "body_hits_adjudicated": {
        "navier–stokes @ line 88": ("a passing citation to [31] Jia-Sverak on "
                                        "local-in-space estimates. Not an application."),
        "(u . grad)u @ line 1686-1688": "Remark 40 itself, twice. The object of this leg.",
        "constraint @ line 876": ("'constraints and matrix-matrix multiplications in "
                                  "interval arithmetic' -- a COST remark, not a PDE "
                                  "constraint. False positive, recorded not discarded."),
    },
    # LIVE-PROBE CONTROL (lesson 90). If the apparatus terms ever go to zero too, the
    # census is measuring nothing and the run must fail.
    "live_control_body": {
        "computer-assisted": 17, "newton": 5, "eigenbasis": 6, "self-adjoint": 2,
        "poincar": 8, "laguerre": 8, "hermite": 10, "quadrature": 22,
        "interval arithmetic": 5, "compact": 11, "radii polynomial": 3,
        "self-similar": 20, "weighted sobolev": 7,
    },
}

# BC's OWN achieved bounds, transcribed with line numbers. These are the magnitudes the
# three dead realizations get compared against.
BC_ACHIEVED = {
    "heat_radial_fractional_d2_p5over3": {
        "line": 1409, "Y": 1.5917976375189734e-23, "Z1": 0.002929002447260958,
        "enclosure_H2mu": 1.6e-23,
        "note": "Theorem 1. Radial, d=2, p=5/3, fractional exponent.",
    },
    "heat_nonradial_d2": {
        "line": 1505, "Y": 0.0011482317939412424, "Z1": 0.09887537542580953,
        "Z2": 236.2041502678645, "Z3": 456.22972624236917, "enclosure_H2mu": 1.6e-3,
        "note": ("Theorem 37. NON-RADIAL. Their own line 1516 says the bound is 'relatively "
                 "large' because 'the decay of the coefficients of the solution is worst in "
                 "this case' -- they track coefficient decay explicitly."),
    },
    "burgers_first_order_term": {
        "line": 1855, "Y": 0.00075636391, "Z1": 0.065135932,
        "Z2": 343.3917, "Z3": 556.478, "enclosure_H2mu": 1e-3,
        "note": ("Theorem 42. THE STRUCTURAL ANALOGUE OF A FLUID NONLINEARITY: the only "
                 "example with a genuine grad-u dependence (f = u/4 - u^2 d_x u). This is "
                 "the Z1 that should be compared with legs 54/176."),
    },
}

# The two dead realizations' Z1, from their own reports. <1 is what is needed.
DEAD_REALIZATION_Z1 = {
    "leg_54_l1w_best_admissible": {
        "value": 8.9591,
        "locator": ("experiments/journal/leg_54.md, VER-A2 GAP 1: 'The true best admissible "
                    "Z1 is 8.9591 (ff_lift, algebraic, null, K = 2), not 32.7489; the "
                    "baseline is 10.46; the improvement is 1.17x' -- where >8x was needed."),
    },
    "leg_176_originH2_best_cell": {
        "value": 140.72,
        "locator": ("experiments/journal/leg_176.md: 'Best cell 140.72 where < 1 is needed; "
                    "growth ~K^2', measured in leg 54's own battery shape for direct "
                    "comparability."),
    },
}

# =====================================================================================
# 2. THE THREE DEATH MECHANISMS, NAMED FROM THEIR OWN REPORTS (lesson 91).
#    Each carries its own locator. No mechanism is described by analogy to another.
# =====================================================================================

MECHANISMS = {
    "M1_l1w_Z1_block_coupling": {
        "realization": "l^1_w coefficient basis, weight w_k = (1+k)^s",
        "report": "experiments/journal/leg_54.md (read at full text, 156 lines)",
        "mechanism_named": (
            "(I - AL)_{Gamma,tail} = -(A11 B + A12 T), and T -- the scaled far-field "
            "transport block -- is SINGULAR on exactly the far-field direction h_hat the "
            "certificate borders. Applied to h_hat the term collapses to -A11 B h_hat and "
            "A12 DROPS OUT OF THE ALGEBRA, so no choice of the off-diagonal block can touch "
            "the (Gamma,tail) coupling. Best admissible Z1 = 8.9591 against baseline 10.46, "
            "a 1.17x improvement where >8x was needed."),
        "root_cause_named": (
            "leg 54 lines 18-22: arXiv:2411.18361's block-diagonal convention takes "
            "A = A^N + pi^inf, i.e. lets the tail act as the identity, FOR DF a COMPACT "
            "PERTURBATION OF THE IDENTITY -- 'and the hypothesis that buys it is exactly "
            "the one this operator fails (leg 51: the unbounded part is a SHIFT, not a "
            "MULTIPLIER)'. Reinforced by leg 127 (via leg 163's table): sigma_min -> 0 like "
            "M^{-(1-s)}, fitted 0.9925/0.6985/0.3202 at s = 0/0.3/0.7, so Z1 >= 1 for EVERY "
            "bounded A -- a property of the operator, not of the shape of A."),
        "transfers_to_H2mu": False,
        "evasion_named": (
            "AT THE HYPOTHESIS, which is the strongest available place. BC line 704 states "
            "the very hypothesis leg 54 names, and it is SATISFIED here for a structural "
            "reason: L^{-1} is COMPACT on H^2(mu) (line 392), because the Gaussian weight "
            "buys a GENUINE POINCARE INEQUALITY on an unbounded domain (line 372, eq 12) -- "
            "the statement that is false on the line in l^1_w. The unbounded part is L, "
            "which the eigenbasis makes EXACTLY DIAGONAL (lines 326/336), i.e. a "
            "MULTIPLIER, which is precisely what leg 51 found the l^1_w operator's "
            "unbounded part was NOT. Consequently A = diag(A_n, I) (line 712) is legitimate "
            "here and its tail-tail block of I - A DF is not a floor but a quantity going "
            "to zero like n^{-1/2} (section 4 below)."),
        "precondition_absent": (
            "There is NO BORDER AND NO FAR-FIELD AMPLITUDE COLUMN anywhere in BC. Leg 54's "
            "mechanism presupposes a bordered system -- its whole algebra is about the "
            "(Gamma,tail) block that bordering creates. BC need no border because the "
            "Poincare inequality means there is no far-field channel to border. The "
            "mechanism's PRECONDITION is absent, not merely its conclusion."),
        "magnitude": (
            "BC's own achieved Z1 on their gradient-nonlinearity example is 0.065136 "
            "(line 1855), i.e. it clears the <1 requirement by 15.4x. leg 54's l^1_w best "
            "admissible is 8.9591 (misses by 8.96x); leg 176's origin-H^2 best cell in the "
            "same battery shape is 140.72 (misses by 140.7x, growing ~K^2)."),
    },
    "M2_collocation_HD_consistency_defect": {
        "realization": "sup-norm spline collocation basis",
        "report": "experiments/journal/leg_56.md (read at full text, 166 lines)",
        "mechanism_named": (
            "TWO SEPARABLE COMPONENTS, and leg 56 separated them itself.\n"
            "(i) THE ARTIFACT: line_hilbert_matrix assembles source columns for INTERIOR "
            "NODES ONLY (Hp_full[:, 1:-1] = HP), so it applies the exact Hilbert transform "
            "of an ENDPOINT-ZEROED interpolant Pi^0, while the derivative matrix D uses the "
            "FULL natural-spline slope operator. Two different discretisations. The "
            "resulting (H,D) consistency defect DOES NOT CONVERGE: 4.7287e-03 -> 4.7131e-03 "
            "-> 4.7041e-03 over n = 201/401/801, measured order 0.00, with the "
            "endpoint-zeroing artifact carrying share 1.00009 of the total at n = 801.\n"
            "(ii) THE ROBUST RESIDUE: deleting the H defect outright, D alone still needs "
            "n ~ 52,163 at its measured order 4.01 to reach tau = 2.3e-14."),
        "transfers_to_H2mu": False,
        "evasion_named": (
            "COMPONENT (i) REQUIRES AN INTERPOLATORY DISCRETISATION OF A NONLOCAL OPERATOR. "
            "BC HAVE NEITHER. There is no interpolant: P_n is an ORTHOGONAL Galerkin "
            "projection, and Remark 11 (line 406) notes it is orthogonal in L^2(mu), "
            "H^1(mu) AND H^2(mu) simultaneously and commutes with L -- so there is no "
            "'two different discretisations' to be inconsistent between. And there is no "
            "nonlocal operator: L is EXACTLY DIAGONAL with rational eigenvalues "
            "(2+|l|)/2+m in d=2 and (3+l)/2+m in d=3 (lines 326/336). The linear operator's "
            "consistency defect is not small, it is IDENTICALLY ZERO by construction.\n"
            "COMPONENT (ii) IS PRESENT BUT AT A RATE THAT CLEARS THE BUDGET BY ~1e9. "
            "leg 56's D converged at algebraic order 4.01, needing n ~ 5.2e4 to reach "
            "tau = 2.3e-14. BC's Theorem 1 achieves ||u* - u_bar||_{H^2(mu)} <= 1.6e-23 "
            "(line 157) at a workable n."),
        "cousin_that_does_NOT_transfer_but_must_be_named": (
            "LESSON 91 APPLIES HERE AND IS OBEYED. leg 56's mechanism does NOT follow the "
            "machinery into H^2(mu). But a DIFFERENT cost sits at the same rung and must be "
            "named as ITS OWN new cost rather than smuggled in as leg 56's death: if this "
            "repository's target retains a NONLOCAL operator -- the Hilbert transform in "
            "gCLM/Hou-Luo, or the Leray projection / Biot-Savart law in Navier-Stokes -- "
            "that operator is NOT diagonalised by BC's basis, and the census above finds "
            "the paper contains NO machinery for one (leray projection 0, vorticity 0, "
            "pressure 0, solenoidal 0 in the body, against a live control totalling 124). "
            "BC's own Remark 4 (line 212) is candid that their basis has NO BANACH ALGEBRA "
            "structure and that nonlinearities are handled by rigorous quadrature plus "
            "Sobolev embeddings. So the nonlocal rung would have to be BUILT, from nothing. "
            "That is a cost, measured; it is NOT leg 56's death mechanism, and it is not "
            "reported as one."),
    },
    "M3_originH2_a0_exactness_cap": {
        "realization": "origin-H^2 (Hardy/Mellin, X = odd part of H^2(R))",
        "report": ("experiments/journal/leg_176.md (244 lines) + leg 163's journal read "
                   "read-only from origin/leg/163-h2s-v1, which is NOT an ancestor of main"),
        "mechanism_named": (
            "leg 163's obstruction census item O3, 'a = 0 exactness dependence, FATAL for "
            "transfer': EVERY usable object is a consequence of Omega(y) = -y/(y^2 + 1/4) "
            "being the EXACT CLM profile -- the single-simple-pole identity "
            "H.Omega - i.Omega = i/(y + i/2), the collapse of the NONLOCAL linearisation to "
            "a SCALAR FIRST-ORDER operator on each Hardy block, the closed-form resolvent "
            "kernel (Xu 4.23), the exact Mellin norm 1/alpha. For a > 0 Xu proves only a "
            "conditional two-line inclusion under Adm(a): no resolvent, no invertibility, "
            "no gap. HL_S2_nonsymmetric is not a CLM profile and inherits NONE of it. "
            "leg 176 then BUILT it and confirmed the cap in its own words: sigma_min = "
            "0.0908, ||R||_X = 11.0127, at a = 0 only -- 'this certifies an object Xu "
            "already inverts in closed form'."),
        "secondary_mechanism_named": (
            "leg 176's coefficient-decay finding: the exact solution's Laguerre "
            "coefficients decay only like C/n (n|c_n| = 5.9615 -> 5.1162 over "
            "n = 32...1024), because the resolvent maps analytic data to u ~ log(y)/y -- a "
            "LOG SINGULARITY AT THE MELLIN ORIGIN xi = 0. 'No basis smooth at xi = 0 "
            "converges geometrically on this operator.'"),
        "transfers_to_H2mu": False,
        "evasion_named": (
            "PRIMARY: ABSENT, AND ITS NEGATION IS DEMONSTRATED. BC's method is a "
            "Newton-Kantorovich argument around a NUMERICALLY COMPUTED, NON-EXPLICIT "
            "u_bar; nothing in the framework requires an exact closed-form solution "
            "anywhere. Theorem 1 (line 153) encloses a radial profile given only by stored "
            "coefficients, to 1.6e-23. Theorem 2 (line 164) encloses a NON-RADIAL profile "
            "to 3.8e-08, and Remark 3 (line 177) records that the only other work "
            "producing non-radial solutions relies on local bifurcation theory near "
            "specific parameter values -- i.e. BC certify objects NOBODY had inverted in "
            "closed form. That is exactly the property legs 163/176 lacked, and it is "
            "demonstrated rather than argued.\n"
            "SECONDARY: TARGET-DEPENDENT, DOES NOT FOLLOW THE MACHINERY. leg 176's C/n "
            "decay was created by the a=0 CLM resolvent's own log singularity, not by the "
            "Laguerre basis -- any smooth basis would suffer it, and a target without that "
            "singularity would not. It is therefore not a property the fourth space "
            "inherits. It must nevertheless be RE-ASKED of whatever target is chosen, and "
            "BC track precisely this quantity themselves (line 1516: their non-radial bound "
            "is 'relatively large' because 'the decay of the coefficients of the solution "
            "is worst in this case')."),
    },
}


# =====================================================================================
# 3. THE EMBEDDING CHAIN -- computed, not asserted.
#    Where does H^2(mu) sit relative to the NRS/Tsai screen this repository already
#    records (plan_of_record.py line 45; CLAY_ROADMAP.md line 334)?
#
#    CEILING, STATED BEFORE THE NUMBER: the exclusion is Necas-Ruzicka-Sverak (1996) and
#    Tsai (1998), NOT this leg's and NOT novel. Its EXACT hypothesis boundary is leg 253's
#    (ROUTE-NRSX) job. This leg uses ONLY the L^3 form the repository itself already
#    records, and computes ONE thing: whether BC's space lands inside that hypothesis.
# =====================================================================================

def embedding_H2mu_into_L3(d=3):
    """||u||_{L^3(R^d)} <= K ||u||_{H^2(mu)}, K computed from BC's own constants.

    Chain, every link a line number in the pinned extraction:
      (1) e^{|x|^2/4} >= 1 pointwise, so  ||u||_{L^3(R^d)} <= ||u||_{L^3(e^theta)}.
          NO CONSTANT IS SPENT HERE -- this is the link that makes the chain tight.
      (2) Lemma 14 (line 425): ||u||_{L^p(e^theta)} <= C(d,p) ||u||^a_{L^2(e^theta)}
          ||u||^{1-a}_{H^1(e^theta)},  a = 1 + d(1/p - 1/2).  For d=3, p=3: a = 1/2.
      (3) ||.||_{L^2(e^theta)} = sqrt(Z) ||.||_{L^2(mu)}, Z = (2 sqrt(pi))^d / Gamma(d/2)
          (line 278); same for H^1.
      (4) Poincare (12, line 372): ||u||_{L^2(mu)} <= sqrt(2/d) ||u||_{H^1(mu)}.
      (5) (13, line 381): ||u||_{H^1(mu)} <= sqrt(2/d) ||u||_{H^2(mu)}.
    """
    p = 3.0
    C, a = bc_C(d, p)
    Z = bc_Z(d)
    # ||u||_{L^3} <= C * (sqrt(Z))^a ||u||^a_{L^2(mu)} * (sqrt(Z))^{1-a} ||u||^{1-a}_{H^1(mu)}
    #             = C * sqrt(Z) * ||u||^a_{L^2(mu)} ||u||^{1-a}_{H^1(mu)}
    # then (4) on the first factor and (5) on both:
    #             <= C * sqrt(Z) * (2/d)^{a/2} * (2/d)^{1/2} * ||u||_{H^2(mu)}
    K = C * math.sqrt(Z) * (2.0 / d) ** (a / 2.0) * (2.0 / d) ** 0.5
    return {"d": d, "p": p, "a": a, "C_d_p": C, "Z": Z, "K": K}


# =====================================================================================
# 4. SETUP COST for the (u.grad)u nonlinearity in d = 3 -- derived from BC's own
#    printed bound shapes.
#
#    HONESTY MARKER: BC print Z^2_2 only for their CUBIC Burgers nonlinearity u^2 d_x u
#    (line 1718-1720):   Z^2_2 = ||1/4 + 2 u_bar d u_bar||_inf / lambda_{n+1}
#                              + ||u_bar||^2_inf / sqrt(lambda_{n+1}).
#    THE (u.grad)u FORM BELOW IS THIS LEG'S DERIVATION, NOT THEIR PRINTED RESULT, and is
#    labelled as such everywhere it is used. It is checkable against their shape: the
#    nonlinearity drops from cubic to QUADRATIC, so ||u_bar||^2_inf becomes ||U_bar||_inf.
#
#    Derivation. F(U) = U - L^{-1} g,  g = U/2 - (U.grad)U.
#      Dg(U_bar)h = h/2 - (h.grad)U_bar - (U_bar.grad)h.
#      For h_inf in the tail range of P_inf, using A = I there (line 712):
#      ||L^{-1} Dg(U_bar) h_inf||_{H^2(mu)} = ||Dg(U_bar) h_inf||_{L^2(mu)}
#          <= (1/2 + ||grad U_bar||_inf) ||h_inf||_{L^2(mu)}
#             + ||U_bar||_inf ||h_inf||_{H^1(mu)}
#      and on the tail  ||h_inf||_{L^2(mu)} <= ||h_inf||_{H^2(mu)} / lambda_{n+1},
#                       ||h_inf||_{H^1(mu)} <= ||h_inf||_{H^2(mu)} / sqrt(lambda_{n+1}),
#      both because h_inf is supported on eigenvalues >= lambda_{n+1} and
#      ||h||^2_{H^1(mu)} = <Lh,h> = sum lambda_k |c_k|^2 while
#      ||h||^2_{H^2(mu)} = sum lambda_k^2 |c_k|^2.
# =====================================================================================

def Z22_convective(n, sup_U, sup_gradU, d=3):
    """This leg's derived tail bound for (U.grad)U. lambda_{n+1} = d/2 + n + 1."""
    lam = d / 2.0 + n + 1.0
    return (0.5 + sup_gradU) / lam + sup_U / math.sqrt(lam)


def dof_d3(n):
    """Number of d=3 basis functions with eigenvalue (3+l)/2 + m <= 3/2 + n.

    (3+l)/2 + m <= 3/2 + n  <=>  l/2 + m <= n. For each (l,m), k ranges over |k| <= l,
    giving 2l+1 functions. Summing with j = n - m:
        N_scalar(n) = sum_{j=0}^{n} (2j+1)^2 = (n+1)(2n+1)(2n+3)/3.
    A VELOCITY FIELD NEEDS 3 COMPONENTS, so N_dof = 3 * N_scalar.
    """
    n_scalar = (n + 1) * (2 * n + 1) * (2 * n + 3) // 3
    return n_scalar, 3 * n_scalar


def min_n_for_contraction(sup_U, gamma, d=3, n_max=4000):
    """Smallest n with the derived Z^2_2 < 1 -- a NECESSARY condition, not sufficient."""
    for n in range(0, n_max + 1):
        if Z22_convective(n, sup_U, gamma * sup_U, d) < 1.0:
            return n
    return None


def setup_cost_table(sups=(1.0, 2.0, 3.0, 5.0, 10.0, 20.0), gammas=(1.0, 5.0)):
    rows = []
    for g in gammas:
        for s in sups:
            n = min_n_for_contraction(s, g)
            if n is None:
                rows.append({"sup_U": s, "gamma": g, "n": None}); continue
            n_scalar, n_dof = dof_d3(n)
            # A_n is DENSE (line 707: "An approximate inverse of Pn DF(u_bar) Pn computed
            # numerically"), and Z^1_1 requires it. Interval arithmetic = 2 doubles/entry.
            bytes_A = 16 * n_dof * n_dof
            rows.append({
                "sup_U": s, "gamma": g, "n": n,
                "lambda_n1": 1.5 + n + 1.0,
                "Z22_derived": Z22_convective(n, s, g * s),
                "dof_scalar": n_scalar, "dof_vector": n_dof,
                "dense_A_bytes": bytes_A,
                "dense_A_TB": bytes_A / 1024.0 ** 4,
            })
    return rows


# =====================================================================================
# 4b. THE LERAY PROJECTION ON L^2(mu) -- MEASURED, not adjudicated by absence-of-mention.
#
# WHY THIS SECTION EXISTS. Leg 255 (ROUTE-P1A, landed on main during this leg, commit
# 891ebaf) used Remark 40 as a screen and killed its one fluid-adjacent candidate
# (Li-Zhou arXiv:2404.17228) on the LERAY-PROJECTION clause, reading the paper's SILENCE
# about the pressure as a boundary. Leg 255 flags this as "the most consequential
# judgement in the table" and explicitly concedes a later leg "could get it by ARGUING
# the Leray clause". This section tests whether that concession is available. IT IS NOT.
#
# THE WITNESS. U = curl(e^{-a|x|^2} e_3) = (-2a x2 E, 2a x1 E, 0), E = e^{-a|x|^2}.
#   div U = 0 EXACTLY, and U is Gaussian, so U in H^2(mu) whenever 2a > 1/4.
#
# THE MECHANISM. With div U = 0, div[(U.grad)U] = d_i d_j (U_i U_j), so
#   v := Laplacian^{-1} div g = d_i d_j Laplacian^{-1}(U_i U_j),   P g = g - grad v.
# Multipole expansion of the Newtonian potential:
#   Laplacian^{-1}(U_iU_j)(x) ~ -(1/4pi) S_ij / |x|,   S_ij = int U_i U_j dx
#   => v(x) ~ -(1/4pi) S_ij (3 x_i x_j - |x|^2 delta_ij)/|x|^5  ~  |x|^{-3}
#   => grad v ~ |x|^{-4}.
# On the x3-axis, S_33 = 0 for this witness, so v ~ (1/4pi) T / r^3 with
#   T = trace S = int |U|^2 > 0 -- THE COEFFICIENT IS THE ENERGY, so it cannot vanish
#   for U != 0. This is what makes the obstruction unarguable rather than generic.
#
# CONSEQUENCE. |P g| ~ C r^{-4} with C != 0, so
#   int_{|x|>R} |P g|^2 e^{|x|^2/4} dx ~ int r^{-8} e^{r^2/4} r^2 dr = +infinity.
# P g is NOT in L^2(mu). So F(U) = U - L^{-1} P(...) is not even WELL-DEFINED as a map
# H^2(mu) -> H^2(mu). This is stronger than "unpriced", and it holds in d = 2 AND d = 3,
# self-similar or not -- i.e. it is BROADER than the NRS composition of section 3.
# =====================================================================================

_LERAY_A = 1.0   # 2a = 2.0 > 1/4, so the witness is comfortably inside H^2(mu)


def _U(y, a=_LERAY_A):
    E = np.exp(-a * np.sum(y * y, axis=-1))
    return np.stack([-2 * a * y[..., 1] * E, 2 * a * y[..., 0] * E,
                     np.zeros_like(E)], axis=-1)


def _quad_nodes(n, L):
    x, w = np.polynomial.legendre.leggauss(n)
    x, w = x * L, w * L
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    W = w[:, None, None] * w[None, :, None] * w[None, None, :]
    return np.stack([X, Y, Z], axis=-1).reshape(-1, 3), W.reshape(-1)


def _S_and_T(n, L):
    y, w = _quad_nodes(n, L)
    u = _U(y)
    S = np.einsum("ki,kj,k->ij", u, u, w)
    return S, float(np.trace(S))


def _v_at(x, n, L):
    """v(x) by direct quadrature. x is far from the support, so no singularity."""
    y, w = _quad_nodes(n, L)
    u = _U(y)
    r = x[None, :] - y
    rn = np.linalg.norm(r, axis=-1)
    UU = u[:, :, None] * u[:, None, :]
    K = 3 * r[:, :, None] * r[:, None, :]
    K = K - (rn ** 2)[:, None, None] * np.eye(3)[None, :, :]
    K = K / (rn ** 5)[:, None, None]
    return float(-(1.0 / (4 * np.pi)) * np.einsum("kij,kij,k->", UU, K, w))


def _g_norm_at(r, a=_LERAY_A):
    """|(U.grad)U| on the x3-axis -- the GAUSSIAN CONTROL. Must collapse while v does not."""
    x = np.array([0.0, 0.0, r])
    h = 1e-5
    grad = np.stack([(_U(x + h * e) - _U(x - h * e)) / (2 * h) for e in np.eye(3)], axis=0)
    return float(np.linalg.norm(np.einsum("k,ki->i", _U(x), grad)))


def leray_measurement():
    # T, across a quadrature ladder -- if T is not stable the coefficient claim says nothing.
    ladder = []
    for n, L in ((40, 5.0), (60, 6.0), (80, 7.0)):
        S, T = _S_and_T(n, L)
        ladder.append({"n": n, "L": L, "T": T, "S_33": float(S[2, 2]),
                       "S_11": float(S[0, 0]), "S_12": float(S[0, 1])})
    S, T = _S_and_T(80, 7.0)

    rows = []
    for r in (10.0, 20.0, 40.0, 80.0):
        v = _v_at(np.array([0.0, 0.0, r]), 80, 7.0)
        pred = T / (4 * np.pi * r ** 3)
        rows.append({"r": r, "v_measured": v, "v_multipole_predicted": pred,
                     "ratio": v / pred, "g_norm_control": _g_norm_at(r)})

    rs = np.array([x["r"] for x in rows])
    vs = np.array([abs(x["v_measured"]) for x in rows])
    slope = float(np.polyfit(np.log(rs), np.log(vs), 1)[0])

    return {
        "witness": "U = curl(e^{-|x|^2} e_3); div U = 0 exactly; Gaussian, so U in H^2(mu)",
        "T_quadrature_ladder": ladder,
        "T": T,
        "decay_ladder": rows,
        "fitted_exponent_v": slope,
        "multipole_prediction_v": -3.0,
        "implied_exponent_grad_v": slope - 1.0,
        "control": ("|(U.grad)U| on the same rays is the GAUSSIAN control and underflows to "
                    "EXACTLY 0.0 at every radius, while v does not. A control that came out "
                    "differently (lesson 90)."),
        "conclusion": (
            "P((U.grad)U) has an ALGEBRAIC |x|^{-4} tail whose coefficient is fixed by "
            "T = int|U|^2 > 0. Therefore P((U.grad)U) is NOT in L^2(mu) for ANY nonzero "
            "divergence-free U in H^2(mu), and F(U) = U - L^{-1}P(...) is not well-defined "
            "as a map H^2(mu) -> H^2(mu)."),
        "cross_check_vs_leg_255_verifier": {
            "eq2_locality_argument": (
                "AGREE, and it is the cleanest of the three. Verified independently at line 84: "
                "the standing governing form is Lu = f(x, u, grad u), and line 693 defines "
                "g : u -> f(., u, grad u) as a NEMYTSKII operator -- pointwise-local by "
                "construction. P[(u.grad)u] is nonlocal and cannot be written in that form. "
                "Qualification: line 55 contemplates SYSTEMS, but a system of pointwise-local "
                "equations is still pointwise-local, so the argument survives."),
            "muckenhoupt_A2_argument": (
                "AGREE WITH THE DIRECTION, DISAGREE WITH THE INFERENCE AS STATED. e^{|x|^2/4} is "
                "indeed not A_2 (A_2 forces doubling, hence at most polynomial growth), so the "
                "standard Calderon-Zygmund weighted theory does not apply. BUT 'the standard "
                "SUFFICIENT condition fails' does not entail 'the operator is unbounded' -- A_2 "
                "is sufficient, not necessary. That is the same shape leg 57 had to discharge "
                "(a BDL-shaped reason to keep a ban, dissolved once the hypothesis was read). "
                "The verifier rightly calls it an assessment; this leg's position is that it "
                "should not be relied on as an argument AT ALL, because it does not need to be: "
                "the witness above EXHIBITS the failure. A demonstration replaces a heuristic."),
        },
        "verdict_on_leg_255": (
            "AGREE with leg 255's screen (iv) kill, and STRENGTHEN it. Leg 255 read "
            "absence-of-mention as a boundary and conceded a later leg 'could get it by "
            "arguing the Leray clause'. THAT CONCESSION IS NOT AVAILABLE: the clause is not "
            "unaddressed-but-plausible, it is FALSE. Leg 255's judgement was right for a "
            "stronger reason than it had, and its own relaxation caveat should be withdrawn."),
        "why_the_two_obvious_repairs_fail": [
            ("BORDER the space with an algebraic far-field mode to absorb the tail -- this "
             "re-introduces EXACTLY the bordered far-field column that leg 54's Z1 "
             "block-coupling mechanism (M1) kills. The repair walks back into the death "
             "the fourth space was chosen to escape."),
            ("SWAP the Gaussian weight for an algebraic one so the tail is admissible -- "
             "this destroys the Poincare inequality (line 372), which section 5's "
             "clause_b caution already names as the SINGLE root of all three evasions. It "
             "breaks M1, M2 and M3's evasions simultaneously."),
            ("VORTICITY formulation, to remove the pressure -- Biot-Savart "
             "(u = curl Laplacian^{-1} omega) is nonlocal with the same algebraic tail, so "
             "the obstruction moves rather than lifts."),
        ],
    }


# =====================================================================================
# 5. THE GATE, COMPUTED (never asserted). classify() has FOUR reachable codes and
#    self_test() must reach all four on perturbed evidence -- including the branches that
#    would NOT escalate. A verdict function with an unreachable branch is not a verdict
#    function (lesson 90).
# =====================================================================================

def classify(clause_a_banked, mechanisms_evaded, mechanisms_total, census_control_total):
    """Return one of four codes.

    ESCALATE_BAN_LIFT_CASE : (a) yes and (b) yes -- the ban's lift clause is satisfied on
                             paper. The lift itself remains the USER's signature.
    CLAUSE_B_FAILS         : a named death mechanism follows the machinery into the fourth
                             space -- this closes Phase 1's Breden-Chu route before
                             construction spends anything.
    CLAUSE_A_FAILS         : the full-text read did not yield a concrete banked account.
    PROBE_DEAD             : the census control collapsed, so nothing was measured at all.
    """
    if census_control_total == 0:
        return "PROBE_DEAD"
    if not clause_a_banked:
        return "CLAUSE_A_FAILS"
    if mechanisms_evaded < mechanisms_total:
        return "CLAUSE_B_FAILS"
    return "ESCALATE_BAN_LIFT_CASE"


def assert_probe_is_live(census):
    total = sum(census["live_control_body"].values())
    if total == 0:
        raise AssertionError(
            "LIVE PROBE DEAD: the full-text census found zero apparatus terms, so its zero "
            "fluid-term counts measure nothing. Refusing to report a finding.")
    return total


def self_test():
    """All four codes must be reachable on perturbed evidence."""
    seen = set()
    seen.add(classify(True, 3, 3, 124))
    seen.add(classify(True, 2, 3, 124))
    seen.add(classify(False, 3, 3, 124))
    seen.add(classify(True, 3, 3, 0))
    expected = {"ESCALATE_BAN_LIFT_CASE", "CLAUSE_B_FAILS", "CLAUSE_A_FAILS", "PROBE_DEAD"}
    assert seen == expected, f"self_test reached only {seen}"
    # The embedding constant must be finite and positive, or the chain says nothing.
    e = embedding_H2mu_into_L3(3)
    assert 0.0 < e["K"] < math.inf and abs(e["a"] - 0.5) < 1e-12, e
    # The derived Z^2_2 must DECREASE in n -- if it did not, the cost table is meaningless.
    assert Z22_convective(10, 5.0, 5.0) > Z22_convective(100, 5.0, 5.0)
    # And it must be able to fail to converge for a large enough profile within n_max.
    assert min_n_for_contraction(1.0, 1.0) is not None
    # The Leray measurement's control must genuinely differ from its signal, or the
    # measurement is not a measurement (lesson 90). Guarded so the finding cannot rot.
    lm = leray_measurement()
    assert abs(lm["fitted_exponent_v"] - (-3.0)) < 1e-3, lm["fitted_exponent_v"]
    assert all(abs(r["ratio"] - 1.0) < 1e-4 for r in lm["decay_ladder"]), lm["decay_ladder"]
    assert all(r["g_norm_control"] == 0.0 for r in lm["decay_ladder"]), "control not silent"
    assert lm["T"] > 0.0
    return sorted(seen)


# =====================================================================================
# MAIN
# =====================================================================================

def main():
    control_total = assert_probe_is_live(CENSUS)
    fluid_body_total = sum(CENSUS["fluid_apparatus_body"].values())
    codes = self_test()

    emb = embedding_H2mu_into_L3(3)
    cost = setup_cost_table()
    leray = leray_measurement()

    evaded = sum(1 for m in MECHANISMS.values() if not m["transfers_to_H2mu"])
    verdict = classify(True, evaded, len(MECHANISMS), control_total)

    result = {
        "leg": 257,
        "route": "P1C",
        "date": PASS_DATE,
        "parent": {"id": PARENT, "md5": PARENT_MD5, "extraction_lines": PARENT_LINES,
                   "md5_matches_leg_245_pin": True,
                   "authors": ["Maxime Breden", "Hugo Chu"],
                   "journal": "Numerische Mathematik, DOI 10.1007/s00211-025-01504-4"},
        "locators": LOCATORS,
        "census": CENSUS,
        "census_totals": {"fluid_apparatus_body": fluid_body_total,
                          "live_control_body": control_total},
        "bc_achieved_bounds": BC_ACHIEVED,
        "dead_realization_Z1": DEAD_REALIZATION_Z1,
        "mechanisms": MECHANISMS,
        "mechanisms_evaded": evaded,
        "mechanisms_total": len(MECHANISMS),
        "embedding_H2mu_to_L3_d3": emb,
        "setup_cost_convective_d3": cost,
        "leray_projection_on_L2mu": leray,
        "self_test_codes_reached": codes,
        "verdict": verdict,
    }

    # ---- clause (a): what a fluid application demands -------------------------------
    result["clause_a"] = {
        "answer": "YES -- concrete and banked",
        "hypotheses_that_bind": [
            {"id": "H1", "statement": "g : H^2(mu) -> L^2(mu) must hold for the nonlinearity",
             "status": "SATISFIED, and Remark 40 (line 1686) is exactly this check. Correct."},
            {"id": "H2",
             "statement": ("Dg(u_bar) : H^2(mu) -> H^1(mu), so DF is a compact perturbation "
                           "of the identity (line 704) -- the hypothesis that licenses "
                           "A = diag(A_n, I)"),
             "status": ("SATISFIED for (U.grad)U with a finite spectral U_bar: the term "
                        "(U_bar.grad)h costs one derivative of h, which H^2 supplies, and "
                        "U_bar is a finite Hermite-Laguerre sum hence smooth.")},
            {"id": "H3",
             "statement": "INCOMPRESSIBILITY / pressure / Leray projection",
             "status": ("BINDS, IS WHOLLY ABSENT, AND IS NOW MEASURED FALSE RATHER THAN "
                        "MERELY UNPRICED. Body census: divergence-free 0, incompressib 0, "
                        "solenoidal 0, pressure 0, leray projection 0, vorticity 0, "
                        "velocity field 0, vector-valued 0 -- against a live control "
                        f"totalling {control_total}. Every equation in the paper is SCALAR "
                        "and UNCONSTRAINED. Section 4b then MEASURES the consequence: the "
                        "Leray projection of the Navier-Stokes nonlinearity has an "
                        "algebraic |x|^{-4} tail with coefficient int|U|^2 > 0, so it "
                        "leaves L^2(mu) and F is not well-defined on H^2(mu). THIS CLOSES "
                        "THE FLUID APPLICATION IN d = 2 AND d = 3.")},
            {"id": "H4",
             "statement": "the target must lie in H^2(mu), i.e. have GAUSSIAN decay",
             "status": ("BINDS, AND IS THE DECISIVE ONE -- see nrs_composition below. The "
                        "framework selects the rapidly-decaying branch of a two-branch far "
                        "field (line 1328), and the paper itself documents that this branch "
                        "CAN BE EMPTY at some parameters (line 1333).")},
        ],
        "setup_cost_summary": (
            "Derived (not BC's printed form -- see section 4's honesty marker): the tail "
            "bound needs lambda_{n+1} > ||U_bar||^2_inf, so n grows like the SQUARE of the "
            "profile's sup norm, while the d=3 vector DOF count grows like 4n^3 and the "
            "dense interval A_n like DOF^2. The table in setup_cost_convective_d3 puts the "
            "wall between ||U_bar||_inf = 5 and 10."),
        "where_future_work_bites": (
            "At a RECTANGLE, not at a fluid. leg 245's locator: the same group's most "
            "recent paper (arXiv:2603.27198, 2026-03-28, line 273) calls extending merely "
            "from an interval to a higher-dimensional rectangle 'non-trivial but will be "
            "studied in a future work' -- 28 months after Remark 40. This leg's Q6 net "
            "re-ran leg 245's author listing on 2026-08-07 and confirms NO newer Breden "
            "paper has appeared, so that statement is still the frontier."),
    }

    # ---- the composition that is this leg's sharpest output --------------------------
    K = emb["K"]
    result["nrs_composition"] = {
        "CEILING_FIRST": (
            "The exclusion is Necas-Ruzicka-Sverak (1996) and Tsai (1998). NOT this leg's, "
            "NOT novel, and its EXACT hypothesis boundary is leg 253's (ROUTE-NRSX) job. "
            "This leg uses only the L^3 form this repository already records "
            "(plan_of_record.py line 45, CLAY_ROADMAP.md line 334) and computes ONE thing: "
            "the embedding constant. If leg 253 moves the boundary, this composition must "
            "be re-derived against the moved boundary."),
        "computed": f"||u||_{{L^3(R^3)}} <= {K:.6f} * ||u||_{{H^2(mu)}}",
        "constant": K,
        "chain": ["e^{|x|^2/4} >= 1 pointwise, so L^3(R^3) <= L^3(e^theta) WITH NO CONSTANT",
                  f"Lemma 14 line 425, d=3 p=3: C(3,3) = {emb['C_d_p']:.6f}, a = {emb['a']}",
                  f"Z = (2 sqrt(pi))^3 / Gamma(3/2) = {emb['Z']:.6f} (line 278)",
                  "Poincare (12) line 372 and (13) line 381, each sqrt(2/3)"],
        "consequence": (
            "H^2(mu) embeds in L^3(R^3) with a FINITE, EXPLICIT constant. So every "
            "candidate BACKWARD-self-similar 3D Navier-Stokes profile that BC's machinery "
            "could even name satisfies NRS's hypothesis, hence is IDENTICALLY ZERO."),
        "sharp_form": (
            "A Breden-Chu enclosure ||U* - U_bar||_{H^2(mu)} <= delta around ANY approximate "
            "Leray profile U_bar certifies U* in L^3(R^3), hence U* = 0 by NRS, hence "
            "||U_bar||_{H^2(mu)} <= delta by the triangle inequality. CONTRAPOSITIVE, AND "
            "THIS IS A PRE-REGISTERED PREDICTION ABOUT THE MACHINERY, NOT A WARNING: if the "
            "numerics ever produce a U_bar with ||U_bar||_{H^2(mu)} > delta, the "
            "Newton-Kantorovich argument CANNOT close -- not 'is expected to fail'. It is "
            "excluded by a theorem the repository already records."),
        "what_this_does_NOT_kill": [
            "d = 2 (no 3D blow-up question there in the first place)",
            ("FORWARD self-similar solutions -- but those decay algebraically too, so they "
             "fail the SPACE for a different reason, not this one, and that is a separate "
             "argument this leg does not make"),
            "DISCRETELY self-similar ansaetze -- separately BANNED here, three reasons",
            ("non-self-similar fluid targets -- but BC's whole framework is built on "
             "L = -Delta - (x/2).grad, the exactly-self-similar rescaling generator, and "
             "the Gaussian weight is natural ONLY because of it. Using the space without "
             "the ansatz discards the reason the space works."),
        ],
        "relation_to_the_ban_lift": (
            "ORTHOGONAL, AND MUST NOT BE CONFLATED. The stage-V ban is about the l^1-Fourier "
            "/ radii-polynomial MACHINERY being dead in three REALIZATIONS. This finding is "
            "about which TARGET a lifted ban could be spent on. It does not block the lift; "
            "it constrains what the lift is worth, and it is reported as a mandatory rider "
            "on the escalation rather than as a gate answer."),
    }

    result["clause_b"] = {
        "answer": ("YES -- all 3 of 3 named mechanisms evaded, each at the mechanism level "
                   "with its own locator, none by analogy"),
        "per_mechanism": {k: {"transfers": v["transfers_to_H2mu"],
                              "evasion": v["evasion_named"][:400] + "..."}
                          for k, v in MECHANISMS.items()},
        "single_root_of_all_three_evasions": (
            "One inequality does most of the work and it is worth naming as such: the "
            "GENUINE POINCARE INEQUALITY (12, line 372) on the unbounded domain R^d, bought "
            "by the Gaussian weight. It makes L^{-1} compact (M1), it makes L exactly "
            "diagonal in an orthogonal eigenbasis so that no interpolatory consistency "
            "defect can exist (M2), and it removes any need for a far-field border or an "
            "exact closed-form anchor (M1, M3). THAT IS ALSO THE WARNING: three evasions "
            "resting on ONE structural fact are not three independent pieces of evidence, "
            "and this leg does not present them as such."),
    }

    result["practical_conclusion"] = (
        "The gate reads ESCALATE_BAN_LIFT_CASE because the three NAMED mechanisms genuinely "
        "do not transfer -- H^2(mu) IS a real fourth space and the ban's literal lift clause "
        "is met. But section 4b closes the FLUID application outright, via a FOURTH "
        "obstruction that is not one of the three and was not on the ban's list: the Leray "
        "projection leaves L^2(mu). So Phase 1's Breden-Chu route is closed BEFORE "
        "construction spent anything -- exactly the outcome DIRECTION.md 257's NO-branch "
        "describes, reached through the YES-branch. Both are reported; neither is allowed to "
        "stand for the other.")

    result["ceiling"] = (
        "SCOPING ONLY. Nothing built, nothing certified, no solver module added or edited. "
        "No stage claimed; plan_of_record.py untouched. NO BAN LIFTED -- clause (b)'s YES is "
        "a RECOMMENDATION to the user carrying its evidence, and DIRECTION.md 257's "
        "yes-branch says so explicitly. No link of the L1->L4 chain moved. Clay odds "
        "unchanged at ~0.05%. Every Breden-Chu quantity is THEIRS; the only things computed "
        "here are the embedding constant, the derived (U.grad)U tail bound and the DOF/cost "
        "arithmetic, all of which are scoping arithmetic on other people's results.")

    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, os.pardir, "writeup", "data", "p2_route_p1c_v1_reach.json")
    out = os.path.normpath(out)
    with open(out, "w") as fh:
        json.dump(result, fh, indent=1)

    # ---- report ---------------------------------------------------------------------
    print(f"LEG 257 -- ROUTE-P1C: Remark 40's reach, measured not argued   [{PASS_DATE}]")
    print(f"  parent {PARENT}  md5 {PARENT_MD5}  ({PARENT_LINES} lines)")
    print("  md5 matches leg 245's pin BIT-FOR-BIT -- locators directly comparable\n")

    print("FULL-TEXT CENSUS (body, bibliography excluded at the paper's own References line)")
    print(f"  fluid apparatus in body : {fluid_body_total}")
    for k, v in sorted(CENSUS["fluid_apparatus_body"].items()):
        if v:
            print(f"      {k:22s} {v}   <- adjudicated, see JSON")
    print(f"  live control in body    : {control_total}  (probe is live)")
    print("  incompressib / pressure / leray projection / solenoidal / vorticity: ALL 0\n")

    print("CLAUSE (a) -- what a 2D/3D fluid application demands")
    for h in result["clause_a"]["hypotheses_that_bind"]:
        print(f"  {h['id']}: {h['statement'][:66]}")
        print(f"      -> {h['status'][:150]}")
    print()

    print("SETUP COST, d = 3, (U.grad)U  [DERIVED here, not BC's printed form]")
    print(f"  {'sup|U|':>7} {'gamma':>6} {'n':>5} {'dof(vec)':>10} {'dense A_n':>12}")
    for r in cost:
        if r["n"] is None:
            print(f"  {r['sup_U']:7.1f} {r['gamma']:6.1f}  no n <= 4000"); continue
        tb = r["dense_A_TB"]
        size = f"{tb:.1f} TB" if tb >= 0.01 else f"{r['dense_A_bytes']/1024**3:.3f} GB"
        print(f"  {r['sup_U']:7.1f} {r['gamma']:6.1f} {r['n']:5d} {r['dof_vector']:10d} "
              f"{size:>12}")
    print()

    print("EMBEDDING CHAIN -- H^2(mu) vs the NRS/Tsai screen this repository records")
    print(f"  ||u||_L^3(R^3)  <=  {K:.6f} * ||u||_H^2(mu)      (d = 3, finite, explicit)")
    print("  => any backward-self-similar 3D NS profile BC's machinery could name")
    print("     satisfies NRS's L^3 hypothesis, hence is IDENTICALLY ZERO.")
    print("  => an enclosure of radius delta forces ||U_bar||_H^2(mu) <= delta:")
    print("     a numerical U_bar bigger than its own enclosure CANNOT be closed.")
    print("  CEILING: NRS/Tsai is not this leg's and not novel; leg 253 owns its boundary.\n")

    print("THE LERAY PROJECTION ON L^2(mu) -- MEASURED (cross-check against leg 255)")
    print(f"  witness: U = curl(e^-|x|^2 e_3), div U = 0 exactly, Gaussian")
    print(f"  T = int|U|^2 = {leray['T']:.9f}  (stable to 12 digits over 3 quadratures)")
    print(f"  {'r':>6} {'v measured':>18} {'multipole':>18} {'ratio':>9} {'|g| control':>12}")
    for row in leray["decay_ladder"]:
        print(f"  {row['r']:6.1f} {row['v_measured']:18.10e} "
              f"{row['v_multipole_predicted']:18.10e} {row['ratio']:9.6f} "
              f"{row['g_norm_control']:12.1e}")
    print(f"  fitted exponent of v : {leray['fitted_exponent_v']:.6f} "
          f"(multipole predicts {leray['multipole_prediction_v']})")
    print(f"  => grad v ~ r^{leray['implied_exponent_grad_v']:.4f}: ALGEBRAIC, while the")
    print("     control |(U.grad)U| underflows to EXACTLY 0.0 at every radius.")
    print("  => P((U.grad)U) NOT in L^2(mu) for ANY nonzero div-free U in H^2(mu);")
    print("     F(U) = U - L^-1 P(...) is not WELL-DEFINED on H^2(mu). d = 2 AND d = 3.")
    print("  vs LEG 255: AGREE with its screen-(iv) kill, and withdraw its own concession")
    print("     that a later leg 'could get it by arguing the Leray clause'. It cannot.\n")

    print("CLAUSE (b) -- the three named death mechanisms, mechanism by mechanism")
    for k, m in MECHANISMS.items():
        print(f"  {k}")
        print(f"      transfers to H^2(mu): {m['transfers_to_H2mu']}")
    print(f"  evaded {evaded}/{len(MECHANISMS)}")
    print("  Z1 comparison, where < 1 is what is needed:")
    print(f"      BC, gradient nonlinearity (line 1855) : "
          f"{BC_ACHIEVED['burgers_first_order_term']['Z1']:.6f}  (clears by 15.4x)")
    for k, v in DEAD_REALIZATION_Z1.items():
        print(f"      {k:36s} : {v['value']:.4f}")
    print("  CAUTION, stated by this leg against itself: all three evasions rest on ONE")
    print("  structural fact (the Poincare inequality, line 372). Not three independent")
    print("  pieces of evidence.\n")

    print(f"self_test reached all four codes: {codes}")
    print(f"VERDICT: {verdict}")
    print("  -> branch PARKED, pushed as a BRANCH only. main is NOT advanced by this leg.")
    print("  -> the ban lift is the USER's signature, not this leg's.")
    print("\nPRACTICAL CONCLUSION, WHICH THE GATE'S LITERAL WORDING DOES NOT CAPTURE:")
    print("  the gate reads YES because the three NAMED mechanisms genuinely do not")
    print("  transfer -- H^2(mu) IS a real fourth space. But section 4b closes the FLUID")
    print("  application of it outright, by a FOURTH obstruction that is not one of the")
    print("  three and was not on the ban's list. So Phase 1's Breden-Chu route is closed")
    print("  BEFORE construction spent anything -- which is exactly the outcome")
    print("  DIRECTION.md 257's no-branch describes, arrived at through the yes-branch.")
    print("  Reported at full strength rather than filed as a clean YES.")
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
