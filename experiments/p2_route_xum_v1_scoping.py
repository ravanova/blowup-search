#!/usr/bin/env python3
"""Leg 173 / Route-XUM -- SCOPING Xu arXiv:2607.19762's OWN certification method.

WHAT THIS IS.  A literature-plus-comparison ledger.  It builds NO certificate, ports
NO machinery, and runs no PDE compute.  Every prior use of Xu in this repository
(legs 127, 163, 171) mined the paper for CITATIONS -- the origin-H^2 invertibility
fact, the {0,1} point spectrum, the s*(a) = 1/c_l(a) exponent.  None opened the
paper's own METHOD.  This script catalogs the method technique by technique, with a
locator for each, and asks the DIRECTION.md 173 gate.

WHAT IT CHECKS RATHER THAN ASSERTS.  Three of Xu's own constants are re-derived here
(section A), each falsifiably:

  A1  Lemma 4.5's exact operator norm  ||T_z||_{L^2(0,inf)} = 1/(Re z + 1/2).
      Checked by minimising the Mellin symbol modulus |z + 1/2 - i xi|^{-1} over a
      xi-grid and confirming the sup sits at xi = Im z with value 1/alpha.  CAN FAIL:
      if the symbol were (z + 1/2 + i xi)^{-1} or if the sup were interior, the grid
      argmax would not land on Im z.

  A2  Lemma 4.5's kernel identity  int_0^1 s^z g(ys) ds = y^{-1-z} int_0^y t^z g(t) dt.
      Checked by numerical quadrature on a nontrivial g at several y and complex z.
      CAN FAIL: any exponent slip in -1-z shows up immediately.

  A3  Section 4.4's constant  c_G = 5/4 + sqrt(10) + 2.  This one is the real control.
      G'' = b^2 f'' + 4 b f' + 2 f with |b|^2 <= 5/4 and |b| <= sqrt(5)/2 on |t| <= 1.
      The NAIVE term-by-term route gives 4|b| <= 2 sqrt(5) = sqrt(20) and therefore
      c_G = 5/4 + sqrt(20) + 2, which does NOT match the paper.  The printed sqrt(10)
      is recovered only by additionally using the X_+ interpolation
      ||f'||_{L^2} <= ||f||_{X_+}/sqrt(2)  (from ab <= (a^2+b^2)/2 on a = ||f||,
      b = ||f''||), giving 4 (sqrt(5)/2)/sqrt(2) = sqrt(10) exactly.  So this check
      distinguishes two candidate readings of the paper and only one of them is right;
      lesson 90 satisfied -- it could have come out the other way, and on the first
      reading it did.

  A4  Section 4.4's exponent bookkeeping: the proof routes AROUND Lemma 4.5.  The
      integral actually estimated is I(y) = int_0^1 s^{z-2} G_2(ys) ds, whose exponent
      is z-2, not z; Lemma 4.5 applied at z-2 would give 1/(Re z - 3/2), not 1/alpha.
      The proof instead uses |G_2(t)| <= |t|^{3/2} ||G''||/sqrt(3) to reduce to the
      SCALAR Beta integral int_0^1 s^{alpha-1} ds = 1/alpha.  Checked here as the
      identity Re z - 1/2 == alpha - 1.  CAN FAIL on any off-by-one in alpha.

Run:  .venv/bin/python experiments/p2_route_xum_v1_scoping.py
Writes: writeup/data/p2_route_xum_v1_scoping.json
"""

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "writeup" / "data" / "p2_route_xum_v1_scoping.json"

PAPER = "arXiv:2607.19762v1 (Xu, 22 Jul 2026), 41 pp, physics.flu-dyn"


# ==========================================================================
# SECTION A -- re-derive Xu's own constants (falsifiable checks)
# ==========================================================================

def check_A1_hardy_mellin_exact_norm():
    """Lemma 4.5: ||T_z|| = 1/(Re z + 1/2), symbol (z + 1/2 - i xi)^{-1}."""
    results = []
    for z in (0.0 + 0.0j, -0.25 + 3.0j, 1.5 - 2.0j, -0.4 + 0.1j):
        alpha = z.real + 0.5
        xi = np.linspace(z.imag - 40.0, z.imag + 40.0, 400001)
        modulus = 1.0 / np.abs(z + 0.5 - 1j * xi)
        k = int(np.argmax(modulus))
        results.append({
            "z": [z.real, z.imag],
            "alpha": alpha,
            "argmax_xi": float(xi[k]),
            "argmax_at_Im_z": bool(abs(xi[k] - z.imag) < 1e-3),
            "sup_symbol_modulus": float(modulus[k]),
            "one_over_alpha": 1.0 / alpha,
            "agrees": bool(abs(modulus[k] - 1.0 / alpha) < 1e-6),
        })
    return {
        "locator": "Xu section 4.4, Lemma 4.5 (exact Hardy-Mellin norm)",
        "claim": "||T_z||_{L^2(0,inf)} = 1/(Re z + 1/2) = 1/alpha; symbol maximised at xi = Im z",
        "cases": results,
        "pass": all(r["agrees"] and r["argmax_at_Im_z"] for r in results),
    }


def check_A2_hardy_kernel_identity():
    """Lemma 4.5: int_0^1 s^z g(ys) ds == y^{-1-z} int_0^y t^z g(t) dt."""
    def g(t):
        return np.exp(-t) * (1.0 + t * t)

    # The two sides are evaluated by DELIBERATELY DIFFERENT quadratures. The obvious
    # move -- the same power substitution on both sides -- reproduces Xu's own change
    # of variables and makes the check a tautology of the code (lesson 90). So:
    #   LHS: s = exp(-v), giving int_0^V exp(-(z+1)v) g(y exp(-v)) dv, a smooth
    #        exponentially decaying integrand on a uniform v-grid.
    #   RHS: a graded direct mesh t = y (k/N)^4 in the original variable t.
    # Neither is derivable from the other, so a genuine exponent slip in y^{-1-z}
    # would still show up.
    results = []
    for z in (0.3 + 0.0j, -0.2 + 1.7j, 0.9 - 0.5j):
        for y in (0.4, 1.0, 2.5):
            v = np.linspace(0.0, 200.0, 1_000_001)
            lhs = np.trapezoid(np.exp(-(z + 1.0) * v) * g(y * np.exp(-v)), v)
            # u starts just off 0: the graded head t < y*1e-36 contributes O(1e-29).
            u = np.linspace(1e-9, 1.0, 1_000_001)
            t = y * u ** 4
            rhs = y ** (-1.0 - z) * np.trapezoid(t ** z * g(t), t)
            results.append({
                "z": [z.real, z.imag], "y": y,
                "lhs": [float(lhs.real), float(lhs.imag)],
                "rhs": [float(rhs.real), float(rhs.imag)],
                "abs_err": float(abs(lhs - rhs)),
                "agrees": bool(abs(lhs - rhs) < 1e-6 * max(1.0, abs(lhs))),
            })
    return {
        "locator": "Xu section 4.4, Lemma 4.5, eq (4.24)",
        "claim": "int_0^1 s^z g(ys) ds = y^{-1-z} int_0^y t^z g(t) dt",
        "cases": results,
        "pass": all(r["agrees"] for r in results),
    }


def check_A3_cG_constant():
    """Section 4.4: c_G = 5/4 + sqrt(10) + 2, and WHICH derivation produces it."""
    b_sq_max = 5.0 / 4.0          # |b|^2 = t^2 + 1/4 <= 5/4 on |t| <= 1
    b_max = math.sqrt(5.0) / 2.0  # |b| <= sqrt(5)/2

    naive = b_sq_max + 4.0 * b_max + 2.0                       # = 5/4 + sqrt(20) + 2
    interp = b_sq_max + 4.0 * b_max / math.sqrt(2.0) + 2.0     # = 5/4 + sqrt(10) + 2
    printed = 5.0 / 4.0 + math.sqrt(10.0) + 2.0

    return {
        "locator": "Xu section 4.4, paragraph before eq (4.25)",
        "claim_as_printed": "c_G = 5/4 + sqrt(10) + 2",
        "printed_value": printed,
        "naive_term_by_term": {
            "value": naive,
            "middle_term": 4.0 * b_max,
            "middle_term_is_sqrt": 20.0,
            "matches_printed": bool(abs(naive - printed) < 1e-12),
        },
        "with_X_plus_interpolation": {
            "value": interp,
            "middle_term": 4.0 * b_max / math.sqrt(2.0),
            "middle_term_is_sqrt": 10.0,
            "matches_printed": bool(abs(interp - printed) < 1e-12),
            "step_used": ("||f'||_{L^2} <= ||f||_{X_+}/sqrt(2), from "
                          "||f'|| <= (||f|| ||f''||)^{1/2} and ab <= (a^2+b^2)/2 "
                          "with ||f||_{X_+}^2 = ||f||^2 + ||f''||^2"),
        },
        "verdict": ("the printed constant is CORRECT and is reached only via the X_+ "
                    "interpolation; the naive term-by-term bound gives sqrt(20) and "
                    "does not match. Xu's c_G is explicit and re-derivable."),
        "pass": bool(abs(interp - printed) < 1e-12 and abs(naive - printed) > 1e-3),
    }


def check_A4_alpha_bookkeeping():
    """Section 4.4 routes around Lemma 4.5: exponent z-2 reduces to a scalar Beta."""
    cases = []
    for rez in (-0.49, -0.25, 0.0, 0.75, 1.4):
        alpha = rez + 0.5
        # |s^{z-2}| * s^{3/2} = s^{Re z - 1/2}; the Beta integral converges as s^{alpha-1}
        cases.append({
            "Re_z": rez, "alpha": alpha,
            "Re_z_minus_half": rez - 0.5,
            "alpha_minus_one": alpha - 1.0,
            "agrees": bool(abs((rez - 0.5) - (alpha - 1.0)) < 1e-15),
            "lemma45_at_z_minus_2_would_give": 1.0 / (rez - 1.5) if abs(rez - 1.5) > 1e-12 else None,
            "proof_actually_gives": 1.0 / alpha,
        })
    return {
        "locator": "Xu section 4.4, proof of Proposition 4.6",
        "claim": ("the integral estimated is I(y) = int_0^1 s^{z-2} G_2(ys) ds; Lemma 4.5 "
                  "applied at exponent z-2 would give 1/(Re z - 3/2), NOT 1/alpha. The "
                  "proof instead uses |G_2(t)| <= |t|^{3/2}||G''||/sqrt(3) to reduce to the "
                  "SCALAR integral int_0^1 s^{alpha-1} ds = 1/alpha -- Xu says so explicitly: "
                  "'the factor 1/alpha arising from the scalar integral ... rather than from "
                  "any operator norm'."),
        "consequence": ("Lemma 4.5's exact-norm result is STATED but is not the load-bearing "
                        "step of Proposition 4.6. Anything ported from section 4.4 needs the "
                        "Taylor-remainder control, not the Hardy operator norm."),
        "cases": cases,
        "pass": all(c["agrees"] for c in cases),
    }


# ==========================================================================
# SECTION B -- the technique catalog
# ==========================================================================
#
# "exact_only_at_a0" is the scope field that decides the gate: it records whether
# the technique's stated hypotheses hold away from the a = 0 CLM anchor.

TECHNIQUES = [
    {
        "id": "T1",
        "name": "Mellin diagonalization of the endpoint models",
        "locator": "sections 4.2-4.3, eqs (4.19)-(4.20); section 4.5",
        "what_it_does": (
            "After y = e^t the dilation generator -c~ y d/dy becomes constant-coefficient, "
            "so each endpoint model has a vertical-line L^2 spectrum located by the indicial "
            "exponent rho(lambda) = (-1 + HOmega(0) - lambda)/c~. At a = 0 the far-field line "
            "is {Re = -1/2} and the plain-L^2 origin line is {Re = +3/2}; at a = 1/2 the "
            "latter is {Re = +5/2}."),
        "explicit_constants": True,
        "requires": "profile with power-law endpoint asymptotics, hypotheses (H1)-(H3)",
        "exact_only_at_a0": False,
        "repo_has": "NONE. No Mellin/log-substitution machinery anywhere in solver/.",
    },
    {
        "id": "T2",
        "name": "Log-widening Weyl sequences with off-support kernel bounds",
        "locator": "section 4.3, eqs (4.17)-(4.18)",
        "what_it_does": (
            "Places the essential line by exhibiting singular sequences. The nonlocal terms "
            "are killed by splitting the kernel at sqrt(R_n) and using the off-support bound "
            "|H phi_n^{(k)}(y)| <= 2||phi_n^{(k)}||_{L^1}/(pi R_n), under R_n >= e^{8 L_n}."),
        "explicit_constants": True,
        "requires": "profile tail rates Omega = O(y^{-1/c_l}), Omega' = O(y^{-1-1/c_l})",
        "exact_only_at_a0": False,
        "repo_has": "NONE. No singular-sequence construction in solver/.",
        "wording_note": (
            "section 3.1 calls these 'explicit Hilbert-Schmidt bounds'. What section 4.3 "
            "actually writes are off-support kernel SUP bounds plus a support split -- a "
            "Schur-type estimate. Recorded as a wording gap in the paper's own summary, NOT "
            "as an error: a sup bound on a split kernel is what the argument needs and is "
            "what is proved. It matters here only because gap (2) below is about genuine "
            "trace-ideal membership, and this is the nearest thing in the paper to it."),
    },
    {
        "id": "T3",
        "name": "Constructive Hardy-Mellin resolvent bound (the alpha^{-3/2} majorant)",
        "locator": "section 4.4, Lemma 4.5, eqs (4.21)-(4.25), Proposition 4.6",
        "what_it_does": (
            "Empties the open strip CONSTRUCTIVELY: exhibits a bounded resolvent R_0(z) on X "
            "for every z in {Re z > -1/2}\\{0,1} by an explicit kernel formula (4.23), with "
            "the majorant ||R_0(z)||_X <= C(R,d) alpha^{-3/2} on the near-edge box "
            "S(R,d,alpha_0), uniformly in Im z, alpha = Re z + 1/2."),
        "explicit_constants": True,
        "requires": (
            "the single-simple-pole identity HOmega - i Omega = i/(y + i/2) (eq 3.9), which "
            "holds ONLY for the exact CLM profile Omega = -y/(y^2 + 1/4)"),
        "exact_only_at_a0": True,
        "repo_has": (
            "NONE of the technique. The repo DOES have solver/interval.py (outward-rounded "
            "interval arithmetic with Rump underflow terms), which is the arithmetic layer "
            "such a bound would be evaluated in."),
    },
    {
        "id": "T4",
        "name": "Hardy block-diagonalization + origin quantization (Theorem 2 / Lemma 1)",
        "locator": "sections 3.3, 5.3-5.6",
        "what_it_does": (
            "L_0 splits as L_0^+ (+) L_0^- on H^2_+ (+) H^2_-, collapsing the nonlocal operator "
            "to the SCALAR first-order L_0^+ = -1 - y d/dy + i/(y + i/2), whose solution space "
            "is spanned by u_lambda = y^{1-lambda}/(y + i/2)^2 for every complex lambda. "
            "Eigenvalue selection is then purely a domain question, and the sin(pi(1-lambda)) "
            "non-degeneracy forces 1-lambda in Z, hence lambda in {0,1}. Unconditional."),
        "explicit_constants": True,
        "requires": "the same eq (3.9) single-pole identity",
        "exact_only_at_a0": True,
        "repo_has": "NONE.",
    },
    {
        "id": "T5",
        "name": "Evans-determinant winding count n_disc(a)  <-- the user's three gaps",
        "locator": "section 3.2 (final paragraph) and section 7 ('Evans-determinant count')",
        "what_it_does": (
            "Splits L_a against its far field, forms the associated determinant on a weighted "
            "space in which the essential line is displaced left of the strip, and reads the "
            "number of strip eigenvalues as an integer winding count along a rectangular "
            "contour. Xu calls it 'a numerical analogue of' Hou-Wang-Yang's finite-rank "
            "certification architecture (section 1)."),
        "explicit_constants": False,
        "requires": (
            "Xu's own three recorded gaps, verbatim: 'a uniform large-imaginary-part bound, "
            "trace-ideal membership of the kernel, and quadrature-error bounds in the trace "
            "norm'"),
        "exact_only_at_a0": False,
        "repo_has": "NONE. Zero determinant, contour, winding or trace-ideal machinery.",
        "paper_status_verbatim": [
            "'This strand is exploratory'  (section 3.2)",
            "'it does not enforce these diagnostics as hard gates, and its run outputs are "
            "not retained'  (section 3.2)",
            "'we report this as exploratory evidence only'  (section 3.2)",
            "'still numerical evidence, not proof, with three explicitly recorded gaps'  "
            "(section 3.2)",
            "'which the code computes as diagnostics rather than enforcing as interval "
            "bounds'  (section 7)",
            "'Upgrading any of these would move this strand toward a computer-assisted "
            "proof.'  (sections 3.2 and 7, twice)",
        ],
    },
    {
        "id": "T6",
        "name": "Realization dichotomy (Proposition 2)",
        "locator": "sections 3.1, 4.6",
        "what_it_does": (
            "A NEGATIVE result about discretizations: on the maximal L^2 realization the whole "
            "strip {-1/2 <= Re lambda <= 3/2} is essential spectrum, filled by "
            "u_lambda = y^{1-lambda}/(y + i/2)^2, and a discretization imposing no origin "
            "condition renders THAT realization, not X."),
        "explicit_constants": True,
        "requires": "nothing beyond the exact profile",
        "exact_only_at_a0": True,
        "repo_has": (
            "ALREADY BANKED, and independently: leg RC's "
            "experiments/p2_route_rc_v1_realization_audit.py checked from the CODE (not from "
            "the paper) that solver/rescaled_spectrum.py imposes no origin condition at X = 0, "
            "i.e. renders the maximal-L^2 realization. This leg claims nothing new here."),
    },
]


# ==========================================================================
# SECTION C -- Xu's three gaps, one row each
# ==========================================================================

GAPS = [
    {
        "gap": "(1) a uniform large-imaginary-part bound",
        "what_it_would_do": (
            "Collapse the infinite contour to a compact one by bounding the modulus/imaginary "
            "part of any strip eigenvalue, so that a winding count over a finite rectangle is "
            "conclusive."),
        "does_the_paper_attach_a_number": False,
        "paper_gives": "the phrase only; no threshold, no estimate, no partial bound",
        "external_technology": {
            "status": "MATURE",
            "source": "Barker, M3AS 26 (2016) 2451-2469, arXiv:1601.00837",
            "what_it_supplies": (
                "an explicit radius R = (gamma + 1/2)^2 bounding any unstable eigenvalue "
                "(section 2.1, Lemma 3.5), then the winding count in INTLAB interval "
                "arithmetic with the wrapping effect handled (sections 2.2-2.3). Public "
                "tooling: STABLAB, https://github.com/nonlinear-waves/stablab"),
            "cost_on_record": "10.3 hours for one contour, in the hardest case reported",
            "transfers_to_Xu": "UNKNOWN -- Barker's bound comes from an energy estimate on a "
                               "finite-dimensional ODE system; Xu's operator is not one.",
        },
    },
    {
        "gap": "(2) trace-ideal membership of the kernel",
        "what_it_would_do": (
            "Make the determinant DEFINED: det(I + A) needs A in the trace class J_1 (or "
            "det_2 with A Hilbert-Schmidt). Without it there is no object to compute."),
        "does_the_paper_attach_a_number": False,
        "paper_gives": (
            "the phrase only. The word 'trace' appears in the paper in exactly two "
            "mathematical places -- the two statements of this gap list (sections 3.2 and 7) "
            "-- and otherwise only in the unrelated sense of boundary 'origin traces' "
            "(Appendix A). No singular-value estimate, no Hilbert-Schmidt norm of the Evans "
            "kernel, no candidate splitting written down anywhere."),
        "external_technology": {
            "status": "THEORY SETTLED, VERIFICATION BESPOKE",
            "source": ("Latushkin & Sukhtayev, Proc. R. Soc. A 471 (2015) 20140597 -- Evans "
                       "function = (2-modified) Fredholm determinant"),
            "what_it_supplies": (
                "the equivalence, but with trace-class (resp. Hilbert-Schmidt) membership as "
                "a HYPOTHESIS. Bornemann arXiv:0804.2543 section 2 lists sufficient "
                "conditions under which a kernel's operator can 'almost always be proven to "
                "be trace class' -- all smoothness/positivity conditions on a BOUNDED "
                "interval."),
            "cost_on_record": None,
            "transfers_to_Xu": (
                "NO off-the-shelf route. And the naive candidate is provably excluded on X: "
                "Xu himself proves the nonlocal term is not compact -- section 3.1, 'the "
                "Hilbert term Omega H phi is not relatively compact (a coefficient vanishing "
                "at both endpoints times an order-zero singular integral is not compact)', "
                "and section 4.6, 'the Mellin symbol m_H of H nonvanishing at xi = +-inf, so "
                "it is not compact'. Trace class is a subset of compact. A weighted space is "
                "asserted to displace the essential line, but the weight is never given."),
        },
    },
    {
        "gap": "(3) quadrature-error bounds in the trace norm",
        "what_it_would_do": (
            "Turn the computed finite-dimensional determinant into a rigorous enclosure of "
            "the true one, via ||det(I+A) - det(I+B)|| <= ||A-B||_{J_1} exp(1 + max(...)) "
            "(Bornemann eq 4.1)."),
        "does_the_paper_attach_a_number": False,
        "paper_gives": "the phrase only; no quadrature rule named, no order, no error figure",
        "external_technology": {
            "status": "MATURE, WITH EXPLICIT CONSTANTS",
            "source": "Bornemann, Math. Comp. 79 (2010) 871-915, arXiv:0804.2543",
            "what_it_supplies": (
                "Theorem 6.2 (Nystrom route): for K in C^{k-1,1}([a,b]^2) and a quadrature "
                "rule of order nu >= k with positive weights, "
                "|d_Q(z) - d(z)| <= c_k 2^k (b-a)^k nu^{-k} Phi(|z|(b-a)||K||_k); for K "
                "bounded analytic on a Bernstein ellipse E_rho x E_rho, "
                "|d_Q(z) - d(z)| <= (4 rho^{-nu}/(1 - rho^{-1})) Phi(|z|(b-a)||K||_Linf). "
                "Every constant named and computable. Theorem 5.1/5.2 (projection route) is "
                "the one literally in TRACE NORM, bounded by the singular-value tail (eq "
                "5.4); Bornemann declines a general quantitative form of it because it "
                "'requires ... detailed knowledge about the decay of the singular values ... "
                "and of the growth of the derivatives of the singular functions'. Unbounded "
                "domains and matrix kernels: arXiv:1406.5252."),
            "cost_on_record": None,
            "transfers_to_Xu": (
                "HYPOTHESIS MISMATCH, and it is the load-bearing one: Bornemann's theorems "
                "are stated on a BOUNDED interval [a,b] with the kernel continuous (Thm 6.2) "
                "or analytic (its second half) on [a,b]^2. Xu's operator lives on R, and its "
                "nonlocal part is an order-zero Cauchy-singular integral operator -- section "
                "7 records having to correct 'the principal-value diagonal of the "
                "g-representation Hilbert kernel ... to its finite part -1/(2 pi)'. A "
                "principal-value kernel is not in C([a,b]^2)."),
        },
    },
]


# ==========================================================================
# SECTION D -- infrastructure comparison against the four named solver files
# ==========================================================================

SOLVER_FILES = {
    "solver/holder_norms.py": {
        "supplies": ("Holder seminorm constants on the circle, conformal/Jacobian identity "
                     "checks, family operator norms in sup/Holder norms "
                     "(holder_H_constant, family_op_norm, conformal_check)"),
        "norm_family": "Holder / sup",
        "covers_any_Xu_technique": None,
        "why": ("Xu works entirely in L^2-based spaces (origin-H^2 X, Hardy H^2, weighted "
                "Y_theta). No Holder norm appears anywhere in the paper."),
    },
    "solver/hilbert_pointwise.py": {
        "supplies": ("POINTWISE bounds on the Hilbert transform of Holder profiles with an "
                     "explicit quadrature (n_quad=400) and eps-regularisation, plus a "
                     "discarded-head audit (pointwise_bound, _head_bound, _audit)"),
        "norm_family": "pointwise / weighted sup",
        "covers_any_Xu_technique": None,
        "why": ("This is the closest thing in the repo to 'quadrature error for a singular "
                "kernel' and it is still the wrong object twice over: it bounds |H psi(theta)| "
                "pointwise on the CIRCLE, where Xu needs a TRACE-NORM bound on an operator on "
                "R. A sup bound on a function does not bound a Schatten norm of an operator."),
    },
    "solver/op_lower.py": {
        "supplies": ("LOWER bounds on operator norms by sign patterns and stochastic ascent "
                     "(sign_pattern_lower, family_lower, ascend, best_lower)"),
        "norm_family": "weighted ell^1 / sup, lower bounds",
        "covers_any_Xu_technique": None,
        "why": ("Direction is wrong. Xu needs UPPER bounds on a resolvent (T3) and a lower "
                "bound on |determinant| along a contour (T5). op_lower bounds operator norms "
                "from below, which certifies non-invertibility, not invertibility."),
    },
    "solver/spectral_certificate.py": {
        "supplies": ("weighted-ell^1 finite-section + tail algebra, radii-polynomial constants, "
                     "rigorous_finite_block, tail_inverse_norm, bordered_tail_inverse_norm, "
                     "fredholm_sides, nogo_hypotheses"),
        "norm_family": "weighted ell^1 on Fourier coefficients, circle",
        "covers_any_Xu_technique": None,
        "why": ("This IS the ~70-leg lane, and it is a Fourier-coefficient basis on the "
                "CIRCLE with algebraic/geometric weights. Xu's every technique is a Mellin or "
                "Hardy decomposition on the LINE. Note fredholm_sides is Fredholm INDEX "
                "bookkeeping, not a Fredholm DETERMINANT -- a false friend, flagged."),
    },
}

# Assets outside the four named files that a port would actually use.
RELEVANT_ASSETS_ELSEWHERE = [
    {
        "file": "solver/interval.py",
        "why_relevant": ("Hand-rolled outward-rounded interval arithmetic with Rump (BIT 2012) "
                         "underflow terms. This is the arithmetic layer Barker gets from "
                         "INTLAB. It is the ONE piece of a rigorous winding count the repo "
                         "already owns."),
        "closes_which_gap": "none by itself -- it is arithmetic, not an estimate",
    },
    {
        "file": "solver/rescaled_spectrum.py",
        "why_relevant": ("A compactified-grid Jacobian spectrum -- the SAME instrument as Xu "
                         "section 7(i). By Xu's own Proposition 2 that instrument renders the "
                         "maximal-L^2 realization, whose strip is entirely spectrum."),
        "closes_which_gap": ("none -- and leg RC already banked, from the code, that this "
                             "module imposes no origin condition. It is a negative asset: "
                             "the tool the repo has is measuring the wrong realization."),
    },
]

# A false friend worth naming so no later leg trips on it.
FALSE_FRIENDS = [
    {
        "looks_like": "solver/hilbert_holder.py's |cot(t/2)| <= 2/|t| head bound (leg 153)",
        "actually": ("a bound on the CIRCLE's Hilbert KERNEL cot(t/2). Xu section 4.6 quotes "
                     "the odd-sector MELLIN SYMBOL of H as -cot(pi s/2), holomorphic on the "
                     "weight lines Re s = 1/2 and 3/2. Same trigonometric function, different "
                     "objects -- a kernel versus a symbol. Do not conflate."),
    },
    {
        "looks_like": "solver/spectral_certificate.py::fredholm_sides",
        "actually": "Fredholm INDEX bookkeeping, not a Fredholm DETERMINANT.",
    },
    {
        "looks_like": ("TECHNICAL_P2_ROUTENGX_V1.md:213's 'large-imaginary-part RESOLVENT "
                       "bounds'"),
        "actually": ("Xu's gap (1) is 'a uniform large-imaginary-part bound' with no "
                     "'resolvent'. Section 4.4 DOES contain a resolvent bound (T3) and it is a "
                     "different object, attached to a different technique, valid only at "
                     "a = 0. Conflating them would make the Evans strand look like it has "
                     "explicit constants. It has none."),
    },
]


# ==========================================================================
# SECTION E -- what "maturing by orders of magnitude" concretely means
# ==========================================================================

def classify_the_gap():
    """Precision gap, scope gap, or infrastructure gap? Answer with the census."""
    numeric_census = {
        "real_valued_quantities_the_Evans_strand_reports": 0,
        "integer_valued": 1,
        "the_integer": "n_disc(a) = 0 for all computed a in [0, 0.65]",
        "numbered_equations_in_the_Evans_strand": 0,
        "numbered_lemmas_or_propositions_in_the_Evans_strand": 0,
        "total_prose_devoted_to_it": ("two paragraphs: section 3.2 final paragraph and the "
                                      "'Evans-determinant count' block of section 7"),
        "run_outputs_retained": False,
        "code_public": False,
        "code_statement_section7": "'the code is supplied for rerunning'",
        "code_statement_data_availability": ("'available from the author upon reasonable "
                                             "request'"),
    }
    return {
        "precision_gap": {
            "is_it": False,
            "why": ("There is no number to sharpen. The Evans strand attaches ZERO real-valued "
                    "quantities to any of the three gaps -- no trace norm, no quadrature "
                    "error, no imaginary-part threshold. Its entire numerical output is one "
                    "integer, and its run outputs are not retained. A 'precision gap' "
                    "presupposes a loose bound; there is no bound."),
        },
        "scope_gap": {
            "is_it": True,
            "why": ("The two techniques that DO carry explicit constants, T3 and T4, both rest "
                    "on the single-simple-pole identity HOmega - i Omega = i/(y + i/2) "
                    "(eq 3.9), which holds only for the exact CLM profile. Xu states the "
                    "restriction himself in section 8: 'the closed-form scalar reduction of "
                    "Theorem 2 being exact only at the single-pole a = 0 profile.' Off a = 0 "
                    "the method does not degrade -- it stops being defined."),
            "named_missing_lemma": ("Xu section 8 names it precisely for the a > 0 discrete "
                                    "exclusion: 'a single imaginary-part-independent "
                                    "essential-edge (threshold-resonance) estimate'. That is a "
                                    "lemma for T3/T4, NOT for the Evans strand."),
            "named_missing_framework": ("Xu section 4.5 names the a > 0 exactness "
                                        "infrastructure and declines to build it: "
                                        "Lockhart-McOwen weighted Fredholm theory, Melrose's "
                                        "b-calculus, Lesch's Fuchs-type conormal symbols, and "
                                        "Rabinovich-Roch-Silbermann limit-operator "
                                        "(band-dominated) algebras -- 'these frameworks do not "
                                        "compose automatically, and we do not carry the "
                                        "argument out here.'"),
        },
        "infrastructure_gap": {
            "is_it": True,
            "why": ("Dominant for T5. No equations, no formula for the splitting, weight, "
                    "kernel or contour, no public code, no retained outputs, and the repo has "
                    "zero determinant/contour/trace-ideal machinery of its own. A port would "
                    "not be porting -- it would be constructing the object from a paragraph."),
        },
        "numeric_census": numeric_census,
    }


# ==========================================================================
# SECTION F -- the gate
# ==========================================================================

def gate():
    return {
        "question_verbatim": (
            "Does Xu's certification method, as stated in the paper, already reach -- or come "
            "within a scopeable, quantifiable distance of -- a working certificate for the "
            "operator class this repository's own certificate work targets, using only "
            "techniques the paper itself states (no new mathematics invented under this leg)?"),
        "answer": "NO",
        "answer_branch_verbatim": (
            "no (the gap is not quantifiable from the paper alone, or is structurally large) "
            "-> Report exactly which technique is farthest from usable and why. Bank this as a "
            "characterized negative on the 'different lane' question -- the paper's method "
            "exists but is not close to a working certificate by any measure this leg can "
            "establish."),
        "sharpest_form": (
            "Xu's method reaches exactly one operator -- the a = 0 CLM linearization -- and "
            "reaches it so completely that no certificate is needed there: Theorem 2 is "
            "closed-form, unconditional, and gives the whole point spectrum over C as {0,1} "
            "via u_lambda = y^{1-lambda}/(y + i/2)^2. Every operator this repository actually "
            "targets (a > 0 gCLM, HL_S2_nonsymmetric, Chen's gamma=2 dissipative gCLM) lies "
            "outside the exactness of the reduction, by Xu's own statement in section 8. So "
            "there is no distance to quantify: the method is not far from the target, it is "
            "undefined off its anchor. It succeeds precisely where nothing was needed."),
        "farthest_from_usable": {
            "technique": "T5 gap (2) -- trace-ideal membership of the kernel",
            "why_1_no_subject": (
                "The paper never writes down the operator whose trace-ideal membership is at "
                "issue. The Evans strand has zero numbered equations: no far-field splitting, "
                "no weight, no kernel, no contour. You cannot verify a hypothesis about an "
                "object that has not been defined."),
            "why_2_provably_excluded_on_X": (
                "The only nonlocal term a splitting could isolate is Omega H phi, and Xu "
                "PROVES it is not compact -- twice, sections 3.1 and 4.6, the second time via "
                "the Mellin symbol of H being nonvanishing at xi = +-infinity. Trace class is a "
                "subset of compact. The weighted space that is supposed to repair this is "
                "asserted and never specified."),
            "why_3_no_external_rescue": (
                "Unlike gaps (1) and (3), no off-the-shelf technology closes it. "
                "Latushkin-Sukhtayev take trace-class membership as a HYPOTHESIS; Bornemann's "
                "sufficient conditions are all for continuous kernels on a bounded interval. "
                "Both gaps (1) and (3) have mature external technology (Barker/STABLAB, "
                "Bornemann Thm 6.2) whose hypotheses one could at least go and CHECK. Gap (2) "
                "has nothing to check against."),
            "ranking_note": (
                "Gap (3) is a close second and fails for a different, cleaner reason: "
                "Bornemann's hypotheses are [a,b]^2 bounded with a continuous/analytic kernel, "
                "and Xu's kernel is principal-value Cauchy-singular on R. That is a stated, "
                "locatable hypothesis mismatch -- i.e. gap (3) IS scopeable, gap (2) is not."),
        },
        "escalate": False,
        "escalation_note": (
            "NO branch taken, so no escalation as a construction lane. Recorded for the DM as "
            "a characterized negative, not a candidate. The one thing worth the user's "
            "attention is stated in 'honest_positive' below and is deliberately NOT dressed as "
            "a lane."),
        "honest_positive": (
            "One technique IS mature, explicit-constant and portable: T3, the section 4.4 "
            "Hardy-Mellin resolvent bound. Lemma 4.5 gives an EXACT operator norm 1/alpha; the "
            "constant c_G = 5/4 + sqrt(10) + 2 = 6.4123 is explicit and is re-derived and "
            "confirmed by check A3 of this script; the majorant is C(R,d) alpha^{-3/2}; and "
            "solver/interval.py is already the arithmetic layer it would be evaluated in. The "
            "reason this is NOT a lane is check A4 plus the scope field: it certifies the "
            "a = 0 resolvent, which Theorem 2 already supplies in closed form, so porting it "
            "would produce a rigorous re-derivation of a result that is already rigorous. "
            "Zero new mathematical content, at real cost."),
        "what_would_change_this_answer": (
            "One thing, and it is specific: if Xu (or anyone) writes down the far-field "
            "splitting L_a = coercive + remainder together with the weight, and proves the "
            "remainder lies in J_1 or J_2 on that weighted space, then gap (2) acquires a "
            "subject, gap (3) becomes a Bornemann hypothesis check, and gap (1) becomes a "
            "Barker-style energy estimate. All three would then be scopeable at once. Until "
            "that splitting exists on paper, none of the three is."),
    }


# ==========================================================================

def main():
    checks = {
        "A1_hardy_mellin_exact_norm": check_A1_hardy_mellin_exact_norm(),
        "A2_hardy_kernel_identity": check_A2_hardy_kernel_identity(),
        "A3_cG_constant": check_A3_cG_constant(),
        "A4_alpha_bookkeeping": check_A4_alpha_bookkeeping(),
    }
    all_pass = all(c["pass"] for c in checks.values())

    payload = {
        "leg": 173,
        "route": "ROUTE-XUM",
        "title": ("Scoping Xu arXiv:2607.19762's own certification method as a different lane "
                  "from the ell^1-Fourier approach"),
        "paper": PAPER,
        "kind": "literature-plus-comparison scoping; no compute, no new solver module",
        "reads_read_only": [
            "solver/holder_norms.py", "solver/hilbert_pointwise.py",
            "solver/op_lower.py", "solver/spectral_certificate.py",
        ],
        "constant_rederivation_checks": checks,
        "all_checks_pass": all_pass,
        "technique_catalog": TECHNIQUES,
        "the_three_gaps": GAPS,
        "infrastructure_comparison": SOLVER_FILES,
        "relevant_assets_elsewhere": RELEVANT_ASSETS_ELSEWHERE,
        "false_friends": FALSE_FRIENDS,
        "maturing_by_orders_of_magnitude": classify_the_gap(),
        "gate": gate(),
        "prior_use_of_this_paper_in_repo": {
            "leg_127": ("cited the origin-H^2 invertibility fact and NAMED the three gaps "
                        "verbatim (writeup/novelty/leg_127.md:96); did not open the method"),
            "leg_163": "origin-H^2 feasibility -- a space question, not a method question",
            "leg_171": "different-spaces coverage",
            "leg_RC": ("experiments/p2_route_rc_v1_realization_audit.py -- checked Prop 2's "
                       "dichotomy against solver/rescaled_spectrum.py from the code"),
            "this_leg_adds": ("the first full-text reading of the method itself: the technique "
                              "catalog, the numeric census of the Evans strand, the external "
                              "technology survey for each gap, and the infrastructure "
                              "comparison"),
        },
        "claims_NOT_made": [
            "that the three-gap phrase is this leg's discovery -- it is leg 127's wording",
            "that Barker's or Bornemann's machinery applies to Xu's operator -- both "
            "hypotheses are recorded as MISMATCHED or UNKNOWN, never as satisfied",
            "that Xu's paper contains an error -- the one wording gap found (T2's "
            "'Hilbert-Schmidt bounds' realized as off-support sup bounds) is recorded as a "
            "summary/realization mismatch and the argument is sound as written",
            "that anything here moves a link of the L1->L4 chain -- it does not",
            "that any ban in plan_of_record.py is lifted -- none is, in either gate branch",
        ],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n")

    print("=" * 74)
    print("LEG 173 / ROUTE-XUM -- scoping Xu arXiv:2607.19762's own certification method")
    print("=" * 74)
    print()
    print("A. RE-DERIVING XU'S OWN CONSTANTS (falsifiable)")
    for k, c in checks.items():
        print(f"   [{'PASS' if c['pass'] else 'FAIL'}] {k}")
    a3 = checks["A3_cG_constant"]
    print(f"        c_G printed        = {a3['printed_value']:.10f}")
    print(f"        naive term-by-term = {a3['naive_term_by_term']['value']:.10f}"
          f"  (sqrt(20) middle term -- does NOT match)")
    print(f"        with interpolation = {a3['with_X_plus_interpolation']['value']:.10f}"
          f"  (sqrt(10) middle term -- MATCHES)")
    print()
    print("B. TECHNIQUE CATALOG")
    for t in TECHNIQUES:
        scope = "a=0 ONLY" if t["exact_only_at_a0"] else "all a"
        const = "explicit constants" if t["explicit_constants"] else "NO constants"
        print(f"   {t['id']}  {t['name'][:52]:<52}  [{scope:>8}] [{const}]")
    print()
    print("C. XU'S THREE GAPS -- does the paper attach a number?")
    for g in GAPS:
        ext = g["external_technology"]["status"]
        print(f"   {g['gap'][:46]:<46}  number: {g['does_the_paper_attach_a_number']}"
              f"   external: {ext}")
    print()
    print("D. INFRASTRUCTURE -- do the four named solver files cover any Xu technique?")
    for f, d in SOLVER_FILES.items():
        print(f"   {f:<36} covers: {d['covers_any_Xu_technique']}")
    print()
    print("E. WHAT 'MATURING' MEANS HERE")
    m = payload["maturing_by_orders_of_magnitude"]
    print(f"   precision gap      : {m['precision_gap']['is_it']}")
    print(f"   scope gap          : {m['scope_gap']['is_it']}")
    print(f"   infrastructure gap : {m['infrastructure_gap']['is_it']}")
    nc = m["numeric_census"]
    print(f"   Evans strand real-valued quantities reported: "
          f"{nc['real_valued_quantities_the_Evans_strand_reports']}")
    print(f"   Evans strand numbered equations             : "
          f"{nc['numbered_equations_in_the_Evans_strand']}")
    print()
    print("F. GATE")
    g = payload["gate"]
    print(f"   ANSWER: {g['answer']}")
    print(f"   farthest from usable: {g['farthest_from_usable']['technique']}")
    print()
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
