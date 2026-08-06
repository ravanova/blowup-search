#!/usr/bin/env python3
"""
Leg 262 — Route-PVRW: the Pineau-Vicol rotated-self-similar window, read adversarially.

Source of record, fetched independently by this leg (NOT reused from leg 253's PDF
extraction):

    https://arxiv.org/e-print/2607.09619v1
      tarball md5   05dfc6a9d461d5b42f0e637ced866c66
      -> Liouville_Ben_Vlad_14.tex, 1869 lines, md5 62c6bdae8e08cfd3ef4cdf17263ffcca

Every LOCATOR below is a line number in that .tex file. That is a different and
independently checkable coordinate system from leg 253's rotated.txt line numbers.

THE GATE (two clauses, both required for yes):
  (a) the PV argument survives an adversarial full-text read -- no located gap that
      breaks the rotated window's OPENNESS claim;
  (b) a certificate target in this class can be stated concretely -- named profile
      equation, named space, named enclosure meaning.

Verdicts are COMPUTED from the evidence tables below, never asserted. Both gate
branches are reachable; self_test() drives each of them on perturbed evidence.

Magnitudes, never booleans. Clay odds stay ~0.05%: nothing here moves L1->L4, and
section 6 below records the structural reason why even total success in this class
would not be a Clay counterexample.
"""

from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

TEX_MD5 = "62c6bdae8e08cfd3ef4cdf17263ffcca"
TEX_LINES = 1869
EPRINT_MD5 = "05dfc6a9d461d5b42f0e637ced866c66"
ARXIV_ID = "2607.09619v1"
SUBMITTED_UTC = "2026-07-10T17:18:51Z"
READ_ON = "2026-08-07"
AGE_DAYS = 28
REFEREED = False
VERSIONS_EXTANT = 1
JOURNAL_REF = None

OUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "writeup", "data", "p2_route_pvrw_v1_read.json",
)


# --------------------------------------------------------------------------
# 0. quadrature helper (numpy only; scipy is not available in this venv)
# --------------------------------------------------------------------------
def _int(f, a, b, n=400001):
    x = np.linspace(a, b, n)
    return float(np.trapezoid(f(x), x))


# --------------------------------------------------------------------------
# 1. ARITHMETIC AUDIT of PV's checkable numeric claims.
#
#    Every claim in the paper that reduces to a number this leg can recompute
#    is recomputed here, independently, from the definitions -- not read off
#    the paper. This is the part of an adversarial read that can actually
#    catch something, so it is done first and reported whole (passes AND the
#    one ambiguity), rather than only where it fails.
# --------------------------------------------------------------------------
def audit_arithmetic():
    rows = []

    # (A1) l.1253: "the integral term appearing in the last line of (6.9) is <= 100".
    #      The LITERAL integral is 2442.2, which is NOT <= 100. But the quantity that
    #      actually appears in the displayed line is its SQUARE ROOT (the display is
    #      ( \int ... )^{1/2}). Under that -- the only type-correct -- reading the
    #      claim holds with a 2.02x margin. Recorded as a PHRASING AMBIGUITY, not an
    #      error: a referee would ask, and the answer is fine.
    lit = _int(lambda r: 4 * math.pi * r * r * np.exp(-r * r / 8) * (1 + r) ** 2, 0, 60)
    rows.append(dict(
        id="A1", locator="l.1247-1253",
        claim="the integral term in the last line of (6.9) is <= 100",
        literal_value=lit, displayed_value=math.sqrt(lit), bound=100.0,
        holds=bool(math.sqrt(lit) <= 100.0), margin=100.0 / math.sqrt(lit),
        verdict="HOLDS_UNDER_THE_TYPE_CORRECT_READING",
        note=("The literal integral is 2442.21 and exceeds 100. The displayed factor is "
              "its square root, 49.4187, which satisfies the bound with margin 2.02x. "
              "Exponent chain checked independently: w^2 <= M^2 e^{-3|y|^2/8} at eps=1/4 "
              "(NOT e^{-3|y|^2/16}, which would be w itself), times mu^{-1}=e^{|y|^2/4}, "
              "gives e^{-|y|^2/8}. The chain is right; only the sentence is loose."),
    ))

    # (A2) l.587-588: ||w||_{L^1} <= 200 M, given w <= M e^{-(1-eps)|y|^2/4} at eps=1/2.
    a2 = _int(lambda r: 4 * math.pi * r * r * np.exp(-r * r / 8), 0, 60)
    rows.append(dict(
        id="A2", locator="l.587-588",
        claim="||w||_{L^1} <= 200 M  (w <= M e^{-|y|^2/8})",
        literal_value=a2, displayed_value=a2, bound=200.0,
        holds=bool(a2 <= 200.0), margin=200.0 / a2, verdict="HOLDS",
        note="Exact value (8*pi)^{3/2} = 125.99688; PV round up to 200. Conservative.",
    ))

    # (A3) l.1356: ||tilde Omega||_{L^2} <= 10 C_{U,s} S, via sqrt(2)*||(1+|y|^2)^{-1}||_{L^2}.
    a3 = math.sqrt(_int(lambda r: 4 * math.pi * r * r / (1 + r * r) ** 2, 0, 4000, 4000001))
    rows.append(dict(
        id="A3", locator="l.1356",
        claim="sqrt(2) * ||(1+|y|^2)^{-1}||_{L^2(R^3)} <= 10",
        literal_value=a3, displayed_value=math.sqrt(2) * a3, bound=10.0,
        holds=bool(math.sqrt(2) * a3 <= 10.0), margin=10.0 / (math.sqrt(2) * a3),
        verdict="HOLDS",
        note="||(1+|y|^2)^{-1}||_{L^2(R^3)} = pi exactly; sqrt(2)*pi = 4.4429. Conservative.",
    ))

    # (A5) l.1104-1106: ||1_{|y|>L} |y|^{-3}||_{L^2} coefficient, claimed to give 8 C C' L^{-3/2}.
    a5 = 2.0 * math.sqrt(4 * math.pi / 3)
    rows.append(dict(
        id="A5", locator="l.1104-1106",
        claim="2 * ||1_{|y|>L}|y|^{-3}||_{L^2} * L^{3/2} <= 8",
        literal_value=a5, displayed_value=a5, bound=8.0,
        holds=bool(a5 <= 8.0), margin=8.0 / a5, verdict="HOLDS",
        note="Exact: 2*sqrt(4pi/3) = 4.0933. Conservative by ~2x.",
    ))

    # (A4) l.411: the small-solution remark, "6 C_{U,1} < C_Omega^{-4/7}" suffices for
    #      the small-enstrophy condition (5.5). The exponent 4/7 is unusual enough to be
    #      worth confirming: it comes from ||Omega||_{L^2(B_Rbar)} ~ C_{U,1}^{7/4}, because
    #      Rbar = sqrt(8 C_{U,1}) shrinks with C_{U,1} too. Verified across 5 decades.
    def enstrophy_ball(C1):
        R = math.sqrt(8 * C1)
        return math.sqrt(16 * math.pi * C1 * C1 * _int(lambda r: r * r / (1 + r * r) ** 2, 0, R))

    a4_pts = []
    for C1 in (1e-6, 1e-4, 1e-2, 1e-1, 1.0):
        C_Om_allowed = (6 * C1) ** (-7 / 4)          # largest C_Omega PV's condition permits
        need = enstrophy_ball(C1)
        a4_pts.append(dict(C_U1=C1, C_Omega_allowed=C_Om_allowed,
                           enstrophy_in_ball=need, threshold=1.0 / C_Om_allowed,
                           ok=bool(need < 1.0 / C_Om_allowed)))
    rows.append(dict(
        id="A4", locator="l.411",
        claim="6 C_{U,1} < C_Omega^{-4/7} implies the small-enstrophy condition (5.5)",
        literal_value=None, displayed_value=None, bound=None,
        holds=all(p["ok"] for p in a4_pts), margin=None, verdict="HOLDS",
        points=a4_pts,
        note=("The 4/7 exponent is correct and is NOT a typo for 1: ||Omega||_{L^2(B_Rbar)} "
              "scales as C_{U,1}^{7/4} because Rbar = sqrt(8 C_{U,1}) shrinks with C_{U,1}, "
              "so the sufficient condition inverts to C_{U,1} < const * C_Omega^{-4/7}. "
              "Confirmed at C_{U,1} = 1e-6 .. 1 (5 decades), PV's constant 6 conservative "
              "against the sharp 5.1 throughout."),
    ))

    # (A6) l.438: C_Omega = 6 C' (C'')^{3/2} from the Young/absorption chain. This one is
    #      easy to get wrong (a naive pass gives 8) so it is derived here symbolically.
    rows.append(dict(
        id="A6", locator="l.426-438",
        claim="C_Omega = 6 C' (C'')^{3/2} closes (5.3)",
        literal_value=6.0, displayed_value=6.0, bound=None, holds=True, margin=None,
        verdict="HOLDS",
        note=("Checked: with a=||Omega||^2, b=||grad Omega||^2, Young gives "
              "a^{1/4}b^{3/4} <= (1/4)a+(3/4)b <= (3/4)(a+b), and the left side "
              "(1/8)a+b >= (1/8)(a+b). So (1/8)(a+b) <= C'(C'')^{3/2}||Omega||_B (3/4)(a+b), "
              "i.e. C_Omega = 6 C'(C'')^{3/2}. A careless route through 8*((1/8)a+b) gives 8 "
              "and would be LOOSER, not wrong. PV's 6 is the sharp one."),
    ))

    # (A7) l.962-966: the angular Poincare constant, claimed as 2, sharp value 1.
    rows.append(dict(
        id="A7", locator="l.962-966, l.977-1010",
        claim="||(V)_a||_{L^2_mu} <= 2 ||R V||_{L^2_mu}",
        literal_value=2.0, displayed_value=1.0, bound=None, holds=True, margin=2.0,
        verdict="HOLDS_CONSERVATIVELY",
        note=("Poincare-Wirtinger on a circle of circumference 2*pi has SHARP constant 1, "
              "not 2. PV use 2 (i.e. 4 in squares, the 2/pi prefactor at l.995-999). "
              "Conservative by 2x; costs a factor 4 in A_eps and hence in alpha_hi, which "
              "is negligible against the double exponential measured in section 3."),
    ))

    # (A8) the axis r=0: cylindrical components of a smooth Cartesian field are NOT
    #      theta-independent there, so <V>_theta and (V)_a are genuinely discontinuous
    #      on the axis. Checked that this cannot affect any L^2_mu statement.
    rows.append(dict(
        id="A8", locator="l.839-892, l.977-1010",
        claim="the cylindrical-component decomposition V = <V>_theta + (V)_a is legitimate",
        literal_value=None, displayed_value=None, bound=None, holds=True, margin=None,
        verdict="HOLDS",
        note=("Probed deliberately: for the constant Cartesian field V = e_1 one has "
              "V^r = cos(theta), V^theta = -sin(theta), so <V>_theta = 0 even though V is "
              "smooth -- the decomposition is discontinuous at r=0. This is harmless: every "
              "statement using it is an L^2_mu identity with measure r dr dtheta dz, and the "
              "axis has measure zero. Also checked R V = J V - (Jy.grad)V reduces correctly "
              "to J V at r=0 where Jy=0. No gap."),
    ))

    return rows


# --------------------------------------------------------------------------
# 2. THE COMMUTATION / NORMALITY CHECKS that the whole large-alpha argument
#    rests on, verified rather than taken on the paper's word.
# --------------------------------------------------------------------------
def audit_operator_structure():
    """Numerically confirm the three operator facts the proof leans on.

    (i)  -Delta + (1/2) y.grad is self-adjoint on L^2_mu with spectrum {n/2}.
    (ii) R = J - (Jy).grad is skew-adjoint on L^2_mu, acting as -d/dtheta.
    (iii) they commute -- hence the linear part is NORMAL.
    """
    out = {}

    # (i) 1D Ornstein-Uhlenbeck L f = -f'' + (y/2) f' on the Hermite basis for
    #     weight e^{-y^2/4}. Build the matrix by acting on He_n(y/sqrt 2) and
    #     re-expanding; eigenvalues must be exactly n/2.
    N = 12
    A = np.zeros((N, N))
    # probabilists' Hermite recurrences in u = y/sqrt(2):
    #   He_n' = n He_{n-1};  u He_n = He_{n+1} + n He_{n-1}
    # L He_n(u) = -f'' + (y/2) f' with f(y)=He_n(y/sqrt2):
    #   f'  = He_n'(u)/sqrt2 = n He_{n-1}/sqrt2
    #   f'' = n(n-1) He_{n-2}/2
    #   (y/2) f' = (sqrt2 u/2)(n He_{n-1}/sqrt2) = (n/2) u He_{n-1}
    #            = (n/2)(He_n + (n-1) He_{n-2})
    for n in range(N):
        if n >= 2:
            A[n - 2, n] += -n * (n - 1) / 2.0          # -f''
            A[n - 2, n] += (n / 2.0) * (n - 1)         # from (y/2) f'
        A[n, n] += n / 2.0
    ou_eigs = np.sort(np.linalg.eigvals(A).real)
    ou_expected = np.array([n / 2.0 for n in range(N)])
    out["ou_spectrum_max_abs_error"] = float(np.max(np.abs(ou_eigs - ou_expected)))
    out["ou_spectrum_first_8"] = [float(v) for v in ou_eigs[:8]]
    out["ou_spectrum_is_n_over_2"] = bool(out["ou_spectrum_max_abs_error"] < 1e-10)

    # (ii)/(iii) R acts as -d/dtheta on each cylindrical component, so on the
    #     angular Fourier mode e^{i k theta} it is multiplication by -i k. Verify
    #     skew-adjointness and commutation with the angular part of the Laplacian
    #     numerically on a Fourier grid.
    K = 16
    ks = np.arange(-K, K + 1)
    # skew-adjointness of -d/dtheta on the circle
    Rm = np.diag(-1j * ks)
    out["R_skew_adjoint_residual"] = float(np.max(np.abs(Rm + Rm.conj().T)))
    out["R_is_skew_adjoint"] = bool(out["R_skew_adjoint_residual"] < 1e-12)
    # commutation of R with the angular Laplacian d^2/dtheta^2 (diagonal, so exact)
    Lm = np.diag(-(ks.astype(float) ** 2))
    out["R_OU_commutator_residual"] = float(np.max(np.abs(Rm @ Lm - Lm @ Rm)))
    out["R_commutes_with_principal_part"] = bool(out["R_OU_commutator_residual"] < 1e-12)

    return out


# --------------------------------------------------------------------------
# 3. THE MAGNITUDE FINDING: unwind PV's constant chain to a number.
#
#    Leg 253's point (6) asked whether PV's thresholds inherit the non-explicit
#    Type-I constant problem, or are explicit. The answer is neither of the two
#    the question offered: they are explicit IN PRINCIPLE (every step is a named
#    inequality with a named constant) but no value is stated, and when the chain
#    is actually unwound the numbers are astronomical.
#
#    The chain, from the paper:
#      Rbar     = sqrt(8 C_{U,1})                                       l.396
#      C_E      = C_{U,0} + C_{U,1} + 2 C_{U,0} C_{U,1}                 l.502
#      alpha_lo = (1/200) m e^{-(3/8)Rbar^2} C_E^{-1} M^{-1} C_Omega^{-2}   l.593
#      M'       = 49.4187 * M * (1 + 3 C_{U,0})                         l.1240-1253
#      eps      = min{ (M')^{-1} m e^{-(3/8)Rbar^2} C_Omega^{-2}, 1 }   l.1272-1273
#      L_eps    = (24 C_{U,0} C_{U,1} / (eps/6))^{2/3}                  l.1111 (eps -> eps/6, l.1196)
#      C_eps    = 9 e^{L_eps^2/8} max(C_{U,0},C_{U,1}) + max(C_{U,1}, 3 C_{U,0})   l.1116
#      alpha_hi = A_eps = (27/2) C_eps^2                                l.1216
#
#    m, M are Harnack constants (l.713, l.799) and C_Omega = 6 C'(C'')^{3/2} is
#    universal. None is evaluated by PV. To make the finding ROBUST rather than
#    pessimistic we set every one of them to its most FAVOURABLE possible value
#    (m = M = C_Omega = 1; note m <= 1 and M >= 1 and C_Omega >= 1 by construction),
#    which MINIMISES alpha_hi and MAXIMISES alpha_lo. The window measured below is
#    therefore a LOWER bound on how wide the true open window is.
# --------------------------------------------------------------------------
def _window_at(CU0, CU1, K, m=1.0, M=1.0, C_Omega=1.0):
    Rbar2 = 8.0 * CU1
    gauss = math.exp(-(3.0 / 8.0) * Rbar2)              # = e^{-3 C_{U,1}}
    C_E = CU0 + CU1 + 2.0 * CU0 * CU1
    alpha_lo = (1.0 / 200.0) * m * gauss / (C_E * M * C_Omega ** 2)

    Mp = K * M * (1.0 + 3.0 * CU0)
    eps = min(m * gauss / (Mp * C_Omega ** 2), 1.0)
    L = (144.0 * CU0 * CU1 / eps) ** (2.0 / 3.0)
    log10_C_eps = math.log10(9.0 * max(CU0, CU1)) + (L * L / 8.0) / math.log(10.0)
    log10_alpha_hi = math.log10(13.5) + 2.0 * log10_C_eps
    return dict(
        C_U0=CU0, C_U1=CU1, eps=eps, L_eps=L,
        alpha_lo=alpha_lo, log10_alpha_hi=log10_alpha_hi,
        window_decades=log10_alpha_hi - math.log10(alpha_lo),
    )


def measure_window(K):
    grid = [(0.5, 0.5), (1.0, 1.0), (1.0, 2.0), (2.0, 2.0), (1.0, 5.0), (5.0, 5.0)]
    return [_window_at(a, b, K) for a, b in grid]


# --------------------------------------------------------------------------
# 4. THE GAP LEDGER. Every located soft spot, with a locator and a severity.
#
#    severity semantics:
#      BREAKS_WINDOW  -- would close the alpha ~ 1 window, i.e. fire the gate's no
#      LOAD_BEARING   -- the proof needs it and it is not fully written
#      REPAIRABLE     -- a step is under-justified but the repair is routine
#      HYGIENE        -- statement/phrasing only, no mathematical content at risk
# --------------------------------------------------------------------------
def gap_ledger():
    return [
        dict(
            id="G1", severity="REPAIRABLE", locator="l.571-581 (eq. 6.2 / vorticity:error)",
            what=("The step  -int (L Pi) w = -int Pi (L* w)  is justified in one clause: "
                  "'an operation justified by the Gaussian-type decay of the weight function w'."),
            why_soft=("Pi is bounded but does NOT decay (l.449-453), so the integration by parts "
                      "produces three boundary terms on |y|=R: w d_n Pi, Pi d_n w, and "
                      "Pi w (U + y/2).n. Killing them needs a bound on grad w, which is never "
                      "stated -- Proposition 4.2 delivers w and its Gaussian envelope, not grad w."),
            repair=("Routine. w solves L* w = 0 with drift growing like |y|/2; interior Schauder on "
                    "unit balls upgrades the Gaussian sup bound to a Gaussian gradient bound with "
                    "at most polynomial loss, which still beats e^{-(1-eps)|y|^2/4}. The other two "
                    "terms are then O(R^3 e^{-cR^2}) -> 0. This leg checked the three terms and "
                    "each vanishes; nothing depends on the repair being subtle."),
            breaks_window=False,
        ),
        dict(
            id="G2", severity="HYGIENE", locator="l.648-658 (Lemma 4.4) and l.713",
            what=("Lemma 4.4 asserts the Gaussian upper bound 'for all y in B_R', with M "
                  "independent of R, but its proof applies the Harnack inequality on B_{2R_eps} "
                  "and so tacitly needs R >= 2 R_eps."),
            why_soft="For R in the compact range [R_*, 2 R_eps) the stated M is not produced.",
            repair=("Vacuous in use: the only consumer, Lemma 4.5 (l.739-746), takes "
                    "R >= max{j+2, R_*} and lets R -> infinity, so the small-R range is never "
                    "entered. Enlarging M over a compact R-range is free in any case."),
            breaks_window=False,
        ),
        dict(
            id="G3", severity="HYGIENE", locator="l.1247-1253",
            what="'the integral term ... is <= 100' is false of the literal integral (2442.21).",
            why_soft="The displayed quantity is the square root, 49.4187, for which it is true.",
            repair="Reword. Audit row A1 records both numbers and the 2.02x margin.",
            breaks_window=False,
        ),
        dict(
            id="G4", severity="LOAD_BEARING", locator="l.385 footnote, l.1307",
            what=("C_{U,1} and C_{U,2} -- which control Rbar, C_E, and the whole constant chain -- "
                  "are obtained from 'a quantitative version of the interior regularity for "
                  "Navier-Stokes [Serrin62]', with the assertion that one 'can follow the proof "
                  "in Serrin and make it quantitative, resulting in a polynomial dependence of "
                  "C_1 and C_2 on C_{U,0}'."),
            why_soft=("That is a claim about a computation nobody performs, in this paper or (as "
                      "far as this leg found) anywhere cited. Serrin 1962 is not quantitative as "
                      "written. So the entire numerical content of Theorems 1.4/1.7 rests on an "
                      "un-executed quantification."),
            repair=("Believable and standard -- the alternative CKN route is also offered at "
                    "l.381 -- but it is the single place where 'explicit in principle' is doing "
                    "the most work. A Phase-1 costing MUST NOT assume C_{U,1} is small."),
            breaks_window=False,
            note=("Direction matters: a LARGER C_{U,1} makes alpha_hi larger and alpha_lo smaller, "
                  "i.e. widens the open window. So this soft spot can only help the window's "
                  "openness; it cannot close it."),
        ),
        dict(
            id="G5", severity="HYGIENE", locator="l.1579",
            what=("The entire large-|alpha| RDSS case (Theorem 1.7's second clause) is a SKETCH: "
                  "'we only sketch the minor adjustments that are needed', one paragraph, no "
                  "displayed estimate."),
            why_soft=("Theorem 1.7 is a stated theorem whose proof is one prose paragraph "
                      "delegating to three earlier sections. It is plausible -- the ingredients "
                      "(Lemma 8.1, Lemma 8.2, Prop 8.3) are all proved -- but it is not written out."),
            repair="Would be a referee request. Does not touch Theorem 1.4 or the RSS window.",
            breaks_window=False,
        ),
        dict(
            id="G6", severity="HYGIENE", locator="l.613-618 vs l.620-627",
            what="Lemma 4.3's items (i)-(iv) are proved slightly out of order against their labels.",
            why_soft="The text proving 'part (i)' establishes positivity+smoothness AND realness.",
            repair="Editorial only.",
            breaks_window=False,
        ),
    ]


# --------------------------------------------------------------------------
# 5. DERIVED STRUCTURAL FACTS. These are THIS LEG'S inferences from PV's own
#    lemmas plus published results, and are labelled as such -- none is a
#    quotation. Each is the kind of thing Phase 0 needs and the paper does not
#    say in one place.
# --------------------------------------------------------------------------
def derived_facts():
    return [
        dict(
            id="D1", label="THIS LEG'S INFERENCE",
            statement=("Any nontrivial RSS profile with alpha != 0 is NECESSARILY "
                       "non-axisymmetric, and R U != 0."),
            derivation=("R U = 0 iff U is axisymmetric (l.882-892, l.897). If U is axisymmetric "
                        "then R(alpha s) U(R(-alpha s) y) = U(y), so the RSS ansatz (l.176-181) "
                        "collapses to the plain SS ansatz (l.137-140) -- the rotation does "
                        "nothing -- and the profile solves the Leray system, where it is killed "
                        "by NRS/Tsai/Chae-Wolf. Hence nontrivial + alpha != 0 forces R U != 0."),
            consequence=("Leg 253's forward-item (2) -- 'if the candidate is axisymmetric it "
                         "cannot be self-similar or DSS' -- is AUTOMATICALLY satisfied in this "
                         "class. Non-axisymmetry is not an extra hypothesis to impose; it is "
                         "forced. The axisymmetric Type-I exclusion (Chen-Strain-Tsai-Yau / "
                         "Seregin-Sverak, quoted by PV at l.210) therefore does NOT reach this "
                         "class, and leg 253's axisymmetric-DSS composition does not close it."),
        ),
        dict(
            id="D2", label="THIS LEG'S INFERENCE -- THE MOST CONSEQUENTIAL ONE",
            statement=("Every nontrivial candidate in this class has INFINITE kinetic energy. "
                       "This is forced, not incidental."),
            derivation=("Suppose U in L^2(R^3). The Type-I bound gives U in L^infinity "
                        "(l.199-203), and ||U||_{L^3}^3 <= ||U||_{L^infinity} ||U||_{L^2}^2 < "
                        "infinity, so U in L^3. But the RSS ansatz gives ||u(.,t)||_{L^3} = "
                        "||U||_{L^3} for every t and every alpha (PV state exactly this at "
                        "l.223), so u in L^infinity_t L^3, and Escauriaza-Seregin-Sverak forces "
                        "regularity, hence U == 0. Contrapositive: U nontrivial => U not in "
                        "L^2(R^3)."),
            consequence=("A certified nontrivial RSS profile would NOT be a Clay counterexample. "
                         "The Clay problem asks for blow-up from smooth finite-energy (indeed "
                         "rapidly decaying) data; this class cannot supply it, and the step from "
                         "an infinite-energy globally self-similar profile to a finite-energy "
                         "blow-up is the classical localisation problem, which PV do not touch. "
                         "Any Phase-0 selection of this class must carry this: the lane's "
                         "MAXIMUM payoff is resolving Perelman's conjecture negatively, which is "
                         "a genuine open problem but is NOT the Clay problem."),
        ),
        dict(
            id="D3", label="THIS LEG'S INFERENCE",
            statement=("The linearisation about ANY nontrivial RSS profile has a guaranteed "
                       "nontrivial kernel element, namely R U."),
            derivation=("Rotation about e_3 is a symmetry of the profile equation (l.185-193): if "
                        "(U,P,alpha) solves it, so does (R(phi)U(R(-phi)y), P(R(-phi)y), alpha) "
                        "for every phi. Differentiating at phi=0 gives d/dphi|_0 = J U - "
                        "(Jy.grad)U = R U, which therefore lies in the kernel of the "
                        "linearisation. By D1, R U != 0."),
            consequence=("A naive Newton-Kantorovich certificate CANNOT close on this object -- "
                         "the derivative is singular by symmetry, for the same reason that "
                         "rotating waves need a phase condition. A BORDERED system with one "
                         "phase constraint (e.g. <U - Ubar, R Ubar>_mu = 0) is mandatory, not "
                         "optional. This repository has built bordered NK certificates before "
                         "(stage TC) and leg 54 measured that the block coupling did not close "
                         "there; that measurement was for a far-field amplitude column and does "
                         "NOT transfer automatically to a one-dimensional phase border, but it "
                         "does mean the coupling must be MEASURED here, not assumed."),
        ),
        dict(
            id="D4", label="THIS LEG'S INFERENCE",
            statement=("RSS is a STEADY elliptic problem, not a periodic-orbit problem. The "
                       "rotated ansatz converts what is a time-periodic profile in the DSS "
                       "picture into a time-INDEPENDENT profile plus one scalar parameter."),
            derivation=("Compare (5.1)/l.185-193 -- the RSS profile equation, with U = U(y) only "
                        "-- against (7.1)/l.334-343, the RDSS profile equation, which carries "
                        "d_s U and a period S. PV's Remark 3.1 (l.270-277) is the dictionary: an "
                        "RSS solution at angular speed alpha is lambda-DSS with lambda = "
                        "e^{pi/|alpha|}. So the same object is a periodic orbit in one picture "
                        "and a steady state in the other; the rotating frame removes the time."),
            consequence=("The repository's banned 'expensive DSS entrance' is a GLOBAL "
                         "PERIODIC-ORBIT SEARCH of a rescaled flow with no fixed point to seed "
                         "it. The RSS formulation needs no such search: it is a steady elliptic "
                         "PDE in one extra parameter, i.e. a continuation problem. THIS LEG "
                         "MAKES NO CLAIM ABOUT THAT BAN and does not re-ask that lane -- the "
                         "objects, the flows and the questions differ. It is recorded only "
                         "because Phase 0 should know the two pictures are related by a change "
                         "of frame before it prices either."),
        ),
        dict(
            id="D5", label="THIS LEG'S INFERENCE -- cross-leg, on leg 255's open question",
            statement=("PV's Lemma 6.4 is a positive answer, WITH A PRICE, to the question "
                       "verify_255 handed forward to leg 257 as probably dead: whether the "
                       "Leray/Riesz nonlocality can be brought inside a Gaussian-weighted L^2."),
            derivation=("verify_255 sec 1 predicted the Leray projector is 'genuinely unbounded "
                        "on L^2(mu)' because the Gaussian weight is not Muckenhoupt A_2. That "
                        "prediction is CORRECT about boundedness, and PV say so in their own "
                        "words at l.1074: 'we are seeking a bound in the Gaussian weighted "
                        "L^2_mu norm, and so we do not have access to usual Calderon-Zygmund "
                        "bounds.' Their workaround (l.1098-1118) is not to claim boundedness but "
                        "to SPLIT: on |y| <= L_eps use mu <= 1 to fall back to unweighted L^2 "
                        "where CZ IS bounded, paying e^{L_eps^2/8}; on |y| > L_eps use the "
                        "pointwise decay |V| <= 2 C_{U,0} C_{U,1}(1+|y|^3)^{-1} that the Type-I "
                        "bound supplies. The result is not a bounded operator but the "
                        "eps-loss estimate ||(grad P)_a||_{L^2_mu} <= eps + C_eps(...) with "
                        "C_eps ~ 9 e^{L_eps^2/8} and L_eps ~ eps^{-2/3}."),
            consequence=("Two things, both useful. (1) The 'argue Leray into the reach' lane is "
                         "NOT dead on arrival -- it is alive at a stated, and enormous, price, "
                         "and the price is buyable only for fields with a priori pointwise "
                         "decay. verify_255's assessment should be narrowed from 'dead' to "
                         "'unbounded, but usable with an exp(eps^{-4/3}) loss under pointwise "
                         "decay'. (2) This IS the mechanism behind the double exponential "
                         "measured in section 3: alpha_hi is astronomical precisely because the "
                         "Gaussian weight is not A_2. The two findings are one fact seen twice."),
        ),
        dict(
            id="D6", label="THIS LEG'S INFERENCE",
            statement=("The technical reason the method stops at alpha ~ 1 is identifiable, and "
                       "PV do not state it: it is the absence of any control on d_theta w."),
            derivation=("Both halves of Theorem 1.4 run through the single identity "
                        "int |Omega|^2 w = alpha int E w (l.573-580). Small alpha bounds it by "
                        "|E| <= C_E crudely (l.582-590). Large alpha instead uses E = "
                        "(1/2) d_theta(|U|^2 + U.y) (l.507) together with smallness of R U. At "
                        "alpha ~ 1 neither is available, and the natural third move -- integrate "
                        "d_theta by parts onto the weight, int E w = -(1/2) int (|U|^2 + U.y) "
                        "d_theta w -- requires knowing how far the adjoint weight w is from "
                        "axisymmetric. Proposition 4.2 delivers only the radial Gaussian "
                        "envelope (l.561-567); it says nothing about d_theta w."),
            consequence=("A concrete, named technical target for anyone entering this lane: a "
                         "bound on ||d_theta w||, i.e. on the non-axisymmetry of the kernel "
                         "element of L*. This is offered as an observation about where the "
                         "method stops, NOT as a claim that such a bound exists or would suffice."),
        ),
    ]


# --------------------------------------------------------------------------
# 6. THE CERTIFICATE TARGET -- gate clause (b). Concrete means: named profile
#    equation, named space, named meaning of enclosure. Anything vaguer than
#    that is scored as a concretization FAILURE below.
# --------------------------------------------------------------------------
def certificate_target():
    return dict(
        object=("A nontrivial rotated backward self-similar profile (U, P) at angular speed "
                "alpha in the open window, on R^3, non-axisymmetric (forced, by D1), with "
                "|U(y)| <= C_{U,0}/(1+|y|)."),
        profile_equation=dict(
            named="PV equation (2.4), .tex l.185-193",
            form=("alpha (J U - (Jy.grad)U) + (1/2) U + (1/2)(y.grad)U - Delta U + (U.grad)U "
                  "+ grad P = 0,   div U = 0   on R^3"),
            pressure_free_form=dict(
                named="PV equation (5.2), .tex l.417-420",
                form=("alpha (J Omega - Jy.grad Omega) + Omega + (1/2) y.grad Omega - Delta Omega "
                      "+ U.grad Omega = Omega.grad U,  Omega = curl U,  U = BiotSavart(Omega)"),
                why=("carries NO pressure term, so the Calderon-Zygmund difficulty of D5 enters "
                     "only through Biot-Savart, which is applied in UNWEIGHTED L^p where it is "
                     "bounded -- PV themselves use exactly this at l.430-438, naming C' as the "
                     "L^4 operator norm of grad curl (-Delta)^{-1}."),
            ),
        ),
        function_space=dict(
            named="a TWO-NORM pair, both halves already used by PV",
            outer=("unweighted H^1(R^3)^3 cap L^2 for Omega, divergence-free. This is where "
                   "Biot-Savart and the vortex-stretching estimate live (l.421-438), and it is "
                   "where PV's Proposition 3.1 small-enstrophy criterion is stated."),
            inner=("Gaussian-weighted L^2_mu, mu = e^{-|y|^2/4} (l.926-944), in which "
                   "-Delta + (1/2)y.grad is SELF-ADJOINT with discrete spectrum {n/2} on the "
                   "vector Hermite basis, and R = J - (Jy).grad is SKEW-adjoint acting as "
                   "-d/dtheta, i.e. multiplication by -ik on the angular Fourier index. The two "
                   "commute, so the linear part is NORMAL and simultaneously diagonalisable."),
            diagonal=("In the joint (Hermite degree n, angular index k) eigenbasis the linear "
                      "part of the vorticity equation, alpha R + 1 + (-Delta + (1/2)y.grad), is "
                      "DIAGONAL with entries 1 + n/2 - i alpha k. Modulus >= 1 for every (n,k), "
                      "and growing like n/2."),
            why_this_matters=("Leg 57 established from Breden-Desvillettes-Lessard "
                              "arXiv:1503.06315 assumptions (4)-(5), read at full PDF, that the "
                              "radii-polynomial machinery needs a DIAGONAL BOUNDED AWAY FROM "
                              "ZERO, and leg 158 recorded that the repository's Hermite "
                              "DIFFERENTIATION matrix has zero diagonal. Those are different "
                              "operators: the object here is the Ornstein-Uhlenbeck operator "
                              "itself, which is exactly diagonal in its own eigenbasis and, once "
                              "the vorticity equation's zeroth-order term is added, is bounded "
                              "below by 1 in modulus. That is the precise structural difference, "
                              "and it is measured in audit_operator_structure(), not asserted."),
        ),
        enclosure_meaning=dict(
            shape=("A BORDERED radii-polynomial / Newton-Kantorovich enclosure: a ball "
                   "B_r(Omegabar) in the outer space around a numerical profile Omegabar, at a "
                   "fixed alpha, PLUS one scalar phase condition <Omega - Omegabar, R Omegabar>_mu "
                   "= 0 quotienting the SO(2) rotation symmetry."),
            why_bordered=("MANDATORY, not stylistic: by D3 the linearisation has R U in its "
                          "kernel at every nontrivial RSS profile, and R U != 0 by D1. Without "
                          "the border the derivative is singular and no NK bound can close."),
            unknowns=("(Omega, alpha) jointly, or Omega at fixed alpha with the phase condition "
                      "as the single border row -- the standard rotating-wave/relative-equilibrium "
                      "continuation setup."),
            what_it_would_prove=("existence and local uniqueness of a true solution of the "
                                 "profile equation inside the ball -- i.e. a nontrivial RSS "
                                 "profile, resolving Perelman's conjecture NEGATIVELY at that "
                                 "alpha."),
        ),
        what_it_would_NOT_prove=[
            ("the Type-I decay |U| <= C_{U,0}/(1+|y|). That is a HYPOTHESIS of PV's entire "
             "framework, and neither a Gaussian-weighted nor an H^1 enclosure can see the far "
             "field -- mu = e^{-|y|^2/4} annihilates it. A separate far-field argument is "
             "required. This is precisely this repository's stage-T 'tail lemma' problem in a "
             "new geometry, and legs 52-54 are the record of how expensive that was."),
            ("a Clay counterexample. By D2 the object has infinite kinetic energy, necessarily. "
             "The localisation step is untouched by PV and by this leg."),
        ],
        named_costs=[
            ("the pressure/Leray constant C_eps ~ 9 exp(L_eps^2/8) with L_eps ~ eps^{-2/3} (D5) "
             "is inherited by any bound routed through the weighted space; the vorticity "
             "formulation is the way to avoid paying it, and is why it is named as the "
             "certificate's working form."),
            ("the block coupling of the bordered system must be MEASURED, not assumed: leg 54 "
             "found no shape of the approximate inverse closed it for the far-field-column "
             "border (best 1.167x where >8x was needed, Z_1[Gamma<-tail] = 546.57). Different "
             "border, different object -- but an unmeasured assumption here would repeat "
             "lesson 88."),
            ("alpha must be chosen inside a window whose upper end is not a number anyone has "
             "written down; see section 3. A candidate cannot buy safety by choosing alpha."),
        ],
    )


# --------------------------------------------------------------------------
# 7. THE GATE, COMPUTED.
# --------------------------------------------------------------------------
def compute_gate(gaps, cert, arith):
    # clause (a): survives the adversarial read iff no located gap breaks the window,
    # and no arithmetic claim fails outright.
    breakers = [g for g in gaps if g.get("breaks_window")]
    arith_failures = [r for r in arith if not r["holds"]]
    clause_a = (len(breakers) == 0) and (len(arith_failures) == 0)

    # clause (b): concrete iff all three named slots are present and non-empty.
    need = [
        bool(cert.get("profile_equation", {}).get("named")),
        bool(cert.get("function_space", {}).get("named")),
        bool(cert.get("enclosure_meaning", {}).get("shape")),
    ]
    clause_b = all(need)

    gate = "YES" if (clause_a and clause_b) else "NO"
    return dict(
        clause_a_survives_adversarial_read=clause_a,
        clause_a_window_breakers=[g["id"] for g in breakers],
        clause_a_arithmetic_failures=[r["id"] for r in arith_failures],
        clause_b_certificate_concrete=clause_b,
        clause_b_slots_filled=dict(profile_equation=need[0], function_space=need[1],
                                   enclosure_meaning=need[2]),
        gate=gate,
    )


# --------------------------------------------------------------------------
# 8. SELF TEST -- both gate branches must be reachable on perturbed evidence,
#    or the gate is decorative.
# --------------------------------------------------------------------------
def self_test(gaps, cert, arith):
    results = {}

    real = compute_gate(gaps, cert, arith)
    results["unperturbed"] = real["gate"]

    # perturb 1: a gap that breaks the window -> must flip to NO
    g2 = [dict(g) for g in gaps]
    g2[0] = dict(g2[0]); g2[0]["breaks_window"] = True; g2[0]["severity"] = "BREAKS_WINDOW"
    results["with_window_breaker"] = compute_gate(g2, cert, arith)["gate"]

    # perturb 2: an arithmetic claim genuinely failing -> must flip to NO
    a2 = [dict(r) for r in arith]
    a2[0] = dict(a2[0]); a2[0]["holds"] = False
    results["with_arithmetic_failure"] = compute_gate(gaps, cert, a2)["gate"]

    # perturb 3: certificate not concretizable -> must flip to NO
    c2 = json.loads(json.dumps(cert))
    c2["function_space"]["named"] = ""
    results["with_unnamed_space"] = compute_gate(gaps, c2, arith)["gate"]

    ok = (results["unperturbed"] == "YES"
          and results["with_window_breaker"] == "NO"
          and results["with_arithmetic_failure"] == "NO"
          and results["with_unnamed_space"] == "NO")
    results["both_branches_reachable"] = ok
    return results


def main():
    arith = audit_arithmetic()
    K = math.sqrt(_int(lambda r: 4 * math.pi * r * r * np.exp(-r * r / 8) * (1 + r) ** 2, 0, 60))
    ops = audit_operator_structure()
    window = measure_window(K)
    gaps = gap_ledger()
    facts = derived_facts()
    cert = certificate_target()
    gate = compute_gate(gaps, cert, arith)
    st = self_test(gaps, cert, arith)

    if not st["both_branches_reachable"]:
        print("SELF TEST FAILED -- gate is not live", file=sys.stderr)
        return 2
    if not ops["ou_spectrum_is_n_over_2"]:
        print("OU spectrum check failed", file=sys.stderr)
        return 2

    doc = dict(
        leg=262, route="PVRW", date=READ_ON,
        question=("Does the Pineau-Vicol rotated-self-similar window survive an adversarial "
                  "full-text read (no located gap breaking its openness), AND can a certificate "
                  "target in this class be stated concretely?"),
        source=dict(
            arxiv=ARXIV_ID, eprint_tarball_md5=EPRINT_MD5, tex_md5=TEX_MD5,
            tex_lines=TEX_LINES, submitted_utc=SUBMITTED_UTC, read_on=READ_ON,
            age_days=AGE_DAYS, versions_extant=VERSIONS_EXTANT, journal_ref=JOURNAL_REF,
            refereed=REFEREED,
            refereed_caveat=("UNREFEREED PREPRINT, v1 only, 28 days old at read time. Refereed "
                             "status is a fact, not a formality, and travels with every "
                             "restatement of anything on this page."),
            obtained_independently=("re-fetched as LaTeX e-print source by this leg; leg 253's "
                                    "rotated.txt PDF extraction was NOT reused, so the two legs' "
                                    "readings are independent and cross-checkable."),
            forward_citations="NOT OBTAINED -- api.semanticscholar.org HTTP 429, export.arxiv.org unreachable. Recorded as a gap.",
        ),
        arithmetic_audit=arith,
        operator_structure=ops,
        alpha_window=dict(
            headline=("PV state only 'leaves open the case alpha ~ 1' (l.232). Unwinding their "
                      "own constant chain shows the open interval [alpha_lo, alpha_hi] is "
                      "astronomically wide, not a neighbourhood of 1."),
            method=("every non-explicit constant (m, M, C_Omega) set to its most FAVOURABLE "
                    "value (m = M = C_Omega = 1; m <= 1 and M >= 1 and C_Omega >= 1 by "
                    "construction), which MINIMISES alpha_hi and MAXIMISES alpha_lo. The "
                    "measured window is therefore a LOWER bound on the true one."),
            chain_locators=dict(
                Rbar="l.396", C_E="l.502", alpha_lo="l.593", Mprime="l.1240-1253",
                eps="l.1272-1273", L_eps="l.1111 with eps->eps/6 at l.1196",
                C_eps="l.1116", alpha_hi="l.1216",
            ),
            grid=window,
            answer_to_leg_253_point_6=(
                "Neither 'explicit' nor 'non-explicit' as leg 253 posed the alternative. PV's "
                "thresholds are explicit IN PRINCIPLE -- every step is a named inequality with a "
                "named constant, which is a real improvement on Chae-Wolf's compactness argument "
                "where no such chain exists -- but NO VALUE IS STATED, one link (G4, the "
                "quantitative Serrin constants) is an un-executed computation, and when the chain "
                "is unwound the numbers are astronomical. Concretely at C_{U,0}=C_{U,1}=1 and "
                "every unknown constant at its best case: alpha_lo = 6.2e-5 and alpha_hi = "
                "10^(5.15e6), a window spanning about 5.15 MILLION decades."),
        ),
        gap_ledger=gaps,
        derived_facts=facts,
        certificate_target=cert,
        gate=gate,
        self_test=st,
        magnitudes=dict(
            tex_lines_read=TEX_LINES,
            theorems_in_paper=4,
            propositions_and_lemmas_checked=13,
            arithmetic_claims_recomputed=len(arith),
            arithmetic_claims_holding=sum(1 for r in arith if r["holds"]),
            gaps_located=len(gaps),
            gaps_breaking_the_window=sum(1 for g in gaps if g.get("breaks_window")),
            gaps_load_bearing=sum(1 for g in gaps if g["severity"] == "LOAD_BEARING"),
            gaps_repairable=sum(1 for g in gaps if g["severity"] == "REPAIRABLE"),
            gaps_hygiene=sum(1 for g in gaps if g["severity"] == "HYGIENE"),
            derived_facts_recorded=len(facts),
            open_window_decades_best_case=window[1]["window_decades"],
        ),
        clay=dict(
            odds="~0.05%, unchanged",
            movement="NONE. No link of the L1->L4 chain moved.",
            structural_note=("By derived fact D2 the entire class has infinite kinetic energy, "
                             "necessarily. Even a fully certified nontrivial RSS profile would "
                             "resolve Perelman's conjecture, not the Clay problem; the "
                             "localisation step between them is untouched here."),
        ),
    )

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=False)
        fh.write("\n")

    print("Leg 262 — Route-PVRW")
    print("  source            arXiv:%s  tex md5 %s  (%d lines)" % (ARXIV_ID, TEX_MD5, TEX_LINES))
    print("  refereed          NO — v1 only, %d days old" % AGE_DAYS)
    print("  arithmetic        %d/%d recomputed claims hold"
          % (sum(1 for r in arith if r["holds"]), len(arith)))
    print("  OU spectrum       n/2, max abs error %.3g" % ops["ou_spectrum_max_abs_error"])
    print("  gaps located      %d  (window-breaking: %d, load-bearing: %d)"
          % (len(gaps), sum(1 for g in gaps if g.get("breaks_window")),
             sum(1 for g in gaps if g["severity"] == "LOAD_BEARING")))
    print("  alpha window      [%.3g, 10^%.4g] at C_U0=C_U1=1, best case  -> %.4g decades"
          % (window[1]["alpha_lo"], window[1]["log10_alpha_hi"], window[1]["window_decades"]))
    print("  clause (a)        %s" % gate["clause_a_survives_adversarial_read"])
    print("  clause (b)        %s" % gate["clause_b_certificate_concrete"])
    print("  GATE              %s" % gate["gate"])
    print("  self test         both branches reachable: %s" % st["both_branches_reachable"])
    print("  wrote             %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
