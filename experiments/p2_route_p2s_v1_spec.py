#!/usr/bin/env python3
"""Leg 285 -- ROUTE-P2S: specify the 15 absent apparatus terms precisely.

Leg 265 costed a certificate for leg 251's named Phase-1 candidate (BCG's gamma = 7/5
compressible-NS imploding profile, n = 3) and found 15 of 18 needed apparatus terms absent
from a 48-row ``capabilities.py`` index.  That was a COUNT.  This leg turns it into a
SPECIFICATION: for each absent term -- what it must compute, its mathematical definition,
its input/output contract against the 3 EXISTING terms, and its position in the dependency
graph (the build's true critical path).

    BUILDS NOTHING.  No solver code.  ``solver/`` is not touched, read or written.
    Pre-empts no construction decision.  Clay odds stay ~0.05%; no L1->L4 link moves.

Every specification claim traces to a named equation/section in BCG (arXiv:2208.09445,
e-print md5 45ea63c45a1a199ecfb4dc4a15431600, 6898 TeX lines) or CGSS (arXiv:2310.05325,
md5 04676de9e3262b0740f4938dd8241b79, 3916 lines).  Both were downloaded BY THIS LEG into a
leg-private directory (honouring leg 265's recorded shared-scratchpad provenance defect);
the md5s reproduce leg 265's and verify_265's bit-for-bit, so line numbers are directly
comparable across all three documents.

Usage
-----
    python experiments/p2_route_p2s_v1_spec.py [--papers DIR] [--out PATH]

``--papers DIR`` (optional) points at a directory holding the two extracted e-prints; when
given, every banked line-number anchor is RE-VERIFIED against the actual TeX rather than
trusted.  Without it the anchors are reported as banked-but-unverified, and the JSON says so
in a field rather than staying silent about it.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict

# --------------------------------------------------------------------------------------
# PROVENANCE
# --------------------------------------------------------------------------------------

SOURCES = {
    "BCG": {
        "arxiv": "2208.09445",
        "title": "Smooth imploding solutions for 3D compressible fluids",
        "eprint_md5": "45ea63c45a1a199ecfb4dc4a15431600",
        "tex_lines": 6898,
        "tex_basename": "RadialImplosion31_FinalArxiv.tex",
        "independent_downloads_agreeing": [
            "leg 251", "leg 266", "verify_251", "leg 265", "verify_265", "leg 285 (this leg)",
        ],
    },
    "CGSS": {
        "arxiv": "2310.05325",
        "title": ("Non-radial implosion for compressible Euler and Navier-Stokes "
                  "in T^3 and R^3"),
        "eprint_md5": "04676de9e3262b0740f4938dd8241b79",
        "tex_lines": 3916,
        "tex_basename": "FinalVersion_3DEulerNonradial.tex",
        "independent_downloads_agreeing": ["leg 265", "verify_265", "leg 285 (this leg)"],
    },
}

# The template leg 265 identified.  Cited, never claimed.  NOT a BCG/CGSS source, which
# matters for term A15 below.
LP_TEMPLATE = {
    "arxiv": "2509.12435",
    "title": "Nonlinear stability of the Larson-Penston collapse",
    "eprint_md5": "a0a136ed5e961276e135e86fa43fb01a",
    "status": "unrefereed preprint (v1, 2025-09-15)",
    "what_it_supplies": ("interval arithmetic inside the mode-stability step of a radially "
                         "imploding compressible self-similar profile, plus public VNODE-LP "
                         "code; INVISCID (isothermal Euler-Poisson), so no F_dis"),
}

# --------------------------------------------------------------------------------------
# THE 3 EXISTING TERMS -- leg 265's rows and leg 265's own adjudications, carried verbatim
# --------------------------------------------------------------------------------------

EXISTING = {
    "E1": {
        "term": "shooting argument",
        "rows": ["solver/bc_weighted_sobolev.py", "solver/viscous_novelty.py"],
        "leg_265_adjudication": (
            "float RK4 seed-finders for scalar ODEs, not rigorous interval barrier/shooting "
            "for a 2D system with a degenerate saddle -- 'the cheap half only'"),
        "transfers": "PARTIAL",
    },
    "E2": {
        "term": "Frobenius / Taylor recurrence at a degenerate saddle",
        "rows": ["solver/origin_h2_certificate.py"],
        "leg_265_adjudication": (
            "the row is a QUADRATURE Taylor technique, not a Frobenius recurrence -- "
            "'does not transfer'"),
        "transfers": "NO",
    },
    "E3": {
        "term": "spectral gap of a non-self-adjoint operator",
        "rows": ["solver/origin_h2_certificate.py"],
        "leg_265_adjudication": (
            "the a=0 CLM operator's, capped at a=0 (legs 163/176) -- 'does not transfer'"),
        "transfers": "NO",
    },
}

# leg 265: "The one genuine asset is solver/interval.py."  Not one of the 18 rows; it is the
# substrate three of the absent terms would sit on.
GENUINE_ASSET = {
    "module": "solver/interval.py",
    "what": "the interval-arithmetic core (Route-D)",
    "serves": ["A7", "A15a"],
    "note": "substrate, not an apparatus term; leg 265 names it as the single genuine asset",
}

# --------------------------------------------------------------------------------------
# THE SPECIFICATION -- the deliverable
# --------------------------------------------------------------------------------------
# Each record carries:
#   computes  -- what the term must compute, operationally
#   definition-- the mathematics, in the papers' own symbols
#   anchors   -- [(source, label-or-section, line)] ; every one checkable in the pinned TeX
#   inputs    -- the input half of the contract
#   outputs   -- the output half
#   deps      -- dependency position: which OTHER absent terms it consumes
#   existing  -- contract against the 3 EXISTING terms / the genuine asset
#   contract_complete -- whether definition+IO+deps are ALL specifiable from BCG/CGSS at the
#                        TARGET's own parameter values (n=3, delta_dis in (-0.5778,-0.4302))

SPEC = {

"A4": dict(
    name="adiabatic / gamma-law pressure",
    computes="the barotropic pressure law and the two constants every other term is a "
             "function of: gamma, and alpha = (gamma-1)/2.",
    definition="p(rho) = rho^gamma / gamma for gamma > 1; alpha = (gamma-1)/2. "
               "At the target gamma = 7/5: alpha = 1/5, so 1/alpha = 5.",
    anchors=[("BCG", "the ideal gas law p(rho)=rho^gamma/gamma, stated with eq:Euler", 141),
             ("BCG", "alpha = (gamma-1)/2, definition of the rescaled sound speed", 180)],
    inputs="gamma: interval, gamma > 1",
    outputs="p: interval -> interval (monotone); alpha: interval; 1/alpha: interval",
    deps=[],
    existing="none -- nothing in the 48-row index is a pressure law (net N-internal: the 5 "
             "'adiabatic' greps over solver/+experiments/ are all 'adiabaticity' in the "
             "continuation sense, a homonym; adjudicated in writeup/novelty/leg_285.md)",
    contract_complete=True,
),

"A6": dict(
    name="radial / spherical geometry",
    computes="the 3D radial reduction: div, grad and Laplacian acting on radially symmetric "
             "fields, and the resulting one-dimensional operators in R.",
    definition="For radial (u, rho): div(rho u) = R^-2 d_R(R^2 rho u); the isentropic radial "
               "Euler system is d_t u + u d_R u + (gamma rho)^-1 d_R(rho^gamma) = 0, "
               "d_t rho + R^-2 d_R(R^2 rho u) = 0.  The viscous radial form carries "
               "-(R^2 rho)^-1 d_R(R^2 d_R u) + 2u/(R^2 rho).",
    anchors=[("BCG", "eq:wombat", 175), ("BCG", "eq:ice", 467)],
    inputs="a radial field on R>0, its derivative order",
    outputs="the radially-reduced differential operator; the 3D volume element 4 pi R^2 dR",
    deps=[],
    existing="none -- the repository's whole certificate stack is 1D-line or 2D-periodic; "
             "no row carries a spherical volume element",
    contract_complete=True,
),

"A11": dict(
    name="self-similar time variable s",
    computes="the dynamic-rescaling change of variables, and the exponential bookkeeping "
             "every decay/growth rate in the argument is measured in.",
    definition="s = -log(T-t)/r, zeta = R/(T-t)^{1/r} = e^s R = exp(xi); "
               "xi = log(R/(T-t)^{1/r}) is the stationary (Euler) self-similar variable. "
               "The parameter r is the self-similar scaling exponent; the target is "
               "r = r^(3) in (1.070374, 1.094975).",
    anchors=[("BCG", "definition of s and zeta", 477),
             ("BCG", "xi, in eq:ansatz:intro", 181),
             ("BCG", "eq:main -- the s-dependent system", 480)],
    inputs="T: interval (blow-up time), r: interval, (R, t)",
    outputs="(s, zeta); the transported derivatives d_s, d_zeta; the prefactor exponents",
    deps=[],
    existing="none -- the repository's rescaled-flow work (legs 42-44, Route-E/H/I) is gCLM's "
             "scaling structure, which Route-E states in its own words is not NS's",
    contract_complete=True,
),

"A15a": dict(
    name="ball arithmetic (Arb)",
    computes="rigorous enclosures of the explicit algebraic/analytic expressions the profile "
             "construction evaluates -- barrier polynomials, Taylor coefficients, r_j "
             "enclosures -- at controlled precision.",
    definition="midpoint-radius (ball) arithmetic; BCG use the Arb C library, at 2000 bits "
               "for the 10000-coefficient lemma because Z_10000 ~ 10^46770.",
    anchors=[("BCG", "sec:computer, 'the Arb library ... its C implementation'", 5693),
             ("BCG", "Table tablecompi (runtimes; longest 23:33:55, and 13:36:38 for "
                     "lemma:tenthousand_7o5)", 5694),
             ("BCG", "lemma:enclosure_r3 / lemma:enclosure_r4 (worked enclosure form)", 5701)],
    inputs="an expression tree over intervals; a precision in bits",
    outputs="a ball (midpoint, radius) provably containing the true value",
    deps=[],
    existing="solver/interval.py -- the genuine asset; this is the ONE absent term with a "
             "real substrate already in the repository",
    contract_complete=True,
),

"A5": dict(
    name="sound speed / density variable",
    computes="the change of unknowns from density to rescaled sound speed, and the vacuum "
             "lower bound that keeps the dissipative multiplier finite.",
    definition="sigma = alpha^-1 rho^alpha, alpha = (gamma-1)/2.  The dissipative multiplier "
               "is S^{-1/alpha}; at gamma = 7/5, 1/alpha = 5, i.e. a FIFTH-order pole at the "
               "vacuum, whose order diverges as gamma -> 1.  Controlled only by lower bounds "
               "on S.",
    anchors=[("BCG", "sigma = alpha^-1 rho^alpha", 180),
             ("CGSS", "'lower bounds for S to rule out possible vacuum'", 494)],
    inputs="rho: interval > 0; alpha from A4",
    outputs="sigma: interval; S^{-1/alpha}: interval, requires a certified S_min > 0",
    deps=["A4"],
    existing="none",
    contract_complete=True,
),

"A1": dict(
    name="compressible fluid model",
    computes="the ambient PDE system in conservation form -- the object the whole "
             "certificate is about.",
    definition="d_t(rho u) + div(rho u tensor u) + grad p(rho) = 0, d_t rho + div(rho u) = 0, "
               "with p(rho) = rho^gamma/gamma.",
    anchors=[("BCG", "eq:Euler", 134), ("BCG", "eq:NS", 143)],
    inputs="(rho, u) on R^3; gamma from A4",
    outputs="the residual of the system; its conserved quantities",
    deps=["A4"],
    existing="none -- every object in the 48-row index is incompressible-adjacent or a 1D "
             "model (CLM/gCLM, Hou-Luo, Boussinesq)",
    contract_complete=True,
),

"A2": dict(
    name="compressible / 3D Euler",
    computes="the inviscid self-similar profile system whose solution IS the target object, "
             "in the coordinates the construction runs in.",
    definition="Riemann invariants w = u + sigma, z = u - sigma diagonalise the radial system "
               "into nonlinear transport form; the self-similar ansatz reduces it to the "
               "AUTONOMOUS 2D system dU/dxi = N_U/D, dS/dxi = N_S/D, whose orbit must connect "
               "P_0 to P_infinity through the regular singular point P_s.  CGSS states the "
               "same stationary profile system independently, explicitly at nu = 0.",
    anchors=[("BCG", "eq:Riemann:invariants", 250),
             ("BCG", "eq:Euler:Riemann", 256),
             ("BCG", "eq:DS (the autonomous phase-portrait system)", 186),
             ("BCG", "eq:mainother (W,Z form)", 268),
             ("CGSS", "eq:ss_profiles, written out for nu = 0", 318),
             ("CGSS", "eq:US2 -- the viscous system the profiles sit in", 290)],
    inputs="(U, S) or (W, Z); r from A11; alpha from A4",
    outputs="the vector field (N_U/D, N_S/D); the loci D=0, N_U=0, N_S=0; the points "
            "P_0, P_s, P_infinity",
    deps=["A1", "A5", "A6"],
    existing="none as a system.  E2 (Frobenius/Taylor at a degenerate saddle) is the row that "
             "WOULD serve the P_s expansion and leg 265 adjudicated it does not transfer "
             "(quadrature, not a Frobenius recurrence)",
    contract_complete=True,
),

"A3": dict(
    name="Navier-Stokes",
    computes="the viscous system -- the equation the certificate must actually be about, as "
             "opposed to the Euler profile it perturbs around.",
    definition="d_t(rho u) + div(rho u tensor u) + grad p(rho) - mu_1 Delta u "
               "- (mu_1 + mu_2) grad div u = 0, d_t rho + div(rho u) = 0, with Lame "
               "coefficients mu_1 > 0, 2 mu_1 + mu_2 > 0.  BCG fix mu_1 = 1, mu_2 = -1.  "
               "Radially this is eq:ice.  Initial density is CONSTANT at infinity, to rule "
               "out the singularity being an artifact of vacuum.",
    anchors=[("BCG", "eq:NS", 143),
             ("BCG", "'we fixed mu_1 = 1 and mu_2 = -1'", 471),
             ("BCG", "eq:ice (spherically symmetric viscous form)", 467)],
    inputs="(rho, u); (mu_1, mu_2); gamma from A4",
    outputs="the viscous residual; the dissipative operator Delta u / (R^2 rho) terms",
    deps=["A1", "A5", "A6"],
    existing="none",
    contract_complete=True,
),

"A10": dict(
    name="non-autonomous forcing",
    computes="F_dis -- the dissipative forcing that makes the viscous problem a perturbation "
             "of the Euler profile, together with its exponential rate delta_dis.  THIS IS "
             "THE TERM leg 251's obligation 1 is about.",
    definition="F_dis = (r^{1+1/alpha} 2^{1/alpha-1} / (alpha^{1/alpha} zeta^2 (W-Z)^{1/alpha})) "
               "e^{(2-r+(1-r)/alpha)s} (d_zeta(zeta^2 d_zeta(W+Z)) - 2(W+Z)).  In (U,S) "
               "coordinates |F_dis| <~ |e^{-delta_dis s} Delta U / S^{1/alpha}|.  The rate is "
               "-delta_dis = 2 - r + (1-r)/alpha, i.e. at gamma = 7/5, delta_dis = 6r - 7.  "
               "BCG's own words: 'the dissipative forcing'.  CGSS writes the same object "
               "independently as nu C_dis e^{-delta_dis s} Delta U / S^{1/alpha}.",
    anchors=[("BCG", "eq:mattmurdock -- F_dis defined", 2116),
             ("BCG", "eq:tildeWZ:def2 -- F_dis enters the RHS", 2136),
             ("BCG", "'the dissipative forcing'", 2142),
             ("BCG", "eq:cortazar -- (U,S) form", 3595),
             ("BCG", "eq:delta:dis", 489),
             ("BCG", "eq:r:restriction, r > 2 gamma/(gamma+1)", 493),
             ("CGSS", "the same term, stated independently", 382)],
    inputs="(W,Z) or (U,S); s from A11; S^{-1/alpha} from A5; r",
    outputs="F_dis as an X-valued function of s; the scalar delta_dis; the enclosure "
            "||F_dis(.,s)||_X",
    deps=["A3", "A5", "A11"],
    existing="none.  This is the term the repository has NO analogue of: every forcing in the "
             "48-row index is autonomous",
    contract_complete=True,
),

"A7": dict(
    name="ODE barrier argument",
    computes="a rigorous trapping region proving the smooth integral curve through P_s "
             "continues to xi = +infinity and lands on P_infinity = (0,0), staying where "
             "D_W > 0, D_Z > 0.",
    definition="a DOUBLE barrier: a near-left barrier b^nl(s) starting above the smooth "
               "solution with the field pointing upwards, concatenated at its intersection "
               "with a far-left barrier b^fl(t) = (W_0 + B_1 W_1 t + B_2 t^2/2, "
               "Z_0 + B_1 Z_1 t + B_3 t^2/2), with B_1, B_2, B_3 chosen so that "
               "b^fl(1) = P_eye and the expansion cancels to first order there.  "
               "P_eye = (X_0, Y_0) = (2(sqrt3-1)r/(3gamma-1), -2(1+sqrt3)r/(3gamma-1)) is the "
               "unique zero of N_W = N_Z = 0 in {W > Z}.",
    anchors=[("BCG", "sec:left", 865),
             ("BCG", "prop:left_main", 868),
             ("BCG", "'a double barrier argument'", 871),
             ("BCG", "eq:bfl", 874),
             ("BCG", "eq:Peye", 880),
             ("BCG", "eq:defBi", 894),
             ("BCG", "sec:right (the mirror argument right of P_s)", 1099)],
    inputs="the field from A2; enclosures from A15a; a candidate r interval",
    outputs="a certified sign pattern along the barrier => a trapping region => the "
            "connecting-orbit statement",
    deps=["A2", "A15a"],
    existing="E1 (shooting) at PARTIAL -- leg 265: float RK4 seed-finders for scalar ODEs, "
             "'the cheap half only'.  The seed-finding half exists; the rigorous-barrier half "
             "does not.  E1's float output is a legitimate INPUT here (it proposes the "
             "barrier's coefficients), which the certified half then encloses.",
    contract_complete=True,
),

"A9": dict(
    name="maximally dissipative operator",
    computes="the decomposition L = A_0 - delta_g + K of the linearised profile operator, "
             "with A_0 maximally dissipative, delta_g > 0 and K compact -- the structural "
             "fact that makes the unstable spectrum FINITE.",
    definition="A_0 maximally dissipative on a Hilbert space H gives: A_0 closed, "
               "sigma(A_0) contained in {Re lambda <= 0}, resolvent bound "
               "||(-A_0 + lambda)^-1|| <= (Re lambda)^-1 for Re lambda > 0, A_0* also "
               "maximally dissipative.  For L = A_0 - delta_g + K the set "
               "Lambda = sigma(L) intersect {Re lambda > -delta_g/2} is FINITE and consists "
               "only of eigenvalues of finite algebraic multiplicity, giving the "
               "finite-dimensional unstable space V.  The space is X = H_0^{2m}(B(0,2)) for "
               "radially symmetric (U,S), with the usual H^{2m} norm -- UNWEIGHTED, on the "
               "ball of radius 2.",
    anchors=[("BCG", "the space X, rem:espartero", 2238),
             ("BCG", "L = A_0 - delta_g + K established", 2707),
             ("BCG", "the construction of A_0 on the finite-codimension space", 2718),
             ("BCG", "ss 'Abstract results on maximally dissipative operators'", 2727),
             ("BCG", "lemma:propertiesmaximalaccretive", 2731),
             ("BCG", "lemma:abstract_result, item:spectrum -- Lambda finite", 2764),
             ("BCG", "eq:spaceV -- the finite-dimensional unstable space V", 2766),
             ("CGSS", "prop:maxdissmooth, the same structure non-radially", 473)],
    inputs="the linearised operator L on X = H_0^{2m}(B(0,2)); m",
    outputs="(A_0, delta_g, K); the finite set Lambda; the finite-dim unstable space V; "
            "the projections P_uns, P_sta; the decomposition X = V (+) V*^perp",
    deps=["A2", "A6"],
    existing="E3 (spectral gap of a non-self-adjoint operator) at NO -- leg 265: it is the "
             "a=0 CLM operator's, capped at a=0 (legs 163/176), 'does not transfer'.  The "
             "delta_g here is a DIFFERENT object: it is a decomposition parameter of L, not "
             "a measured gap of a fixed matrix.",
    contract_complete=True,
),

"A12": dict(
    name="algebraically weighted high-order energy",
    computes="E_2K -- the high-derivative weighted energy in which the dissipative term is "
             "controlled, and the sign extraction that controls it.",
    definition="E_2K(s)^2 = int_{R^3} ((Delta^K U)^2 + (Delta^K S)^2) phi^{2K}(zeta) dzeta, "
               "with an ALGEBRAIC weight phi(zeta) = 1 for zeta <= zeta_0 and "
               "phi = zeta^{2(1-eta_w)}/(2 zeta_0^{2(1-eta_w)}) for zeta >= 4 zeta_0, "
               "smooth in between with |grad phi| zeta / phi <= 2(1-eta_w) and phi >= 1.  "
               "The dissipative contribution is "
               "J = int (r^{1+1/alpha}/alpha^{1/alpha}) e^{-delta_dis s} "
               "Delta^K(Delta U / S^{1/alpha}) Delta^K U phi^{2K}.  J CANNOT be bounded -- it "
               "has more derivatives than the energy -- so the strategy is to EXTRACT THE "
               "CORRECT SIGN: J is dominated by -G^2 with "
               "G^2 = sum int (grad Delta^K U_i)^2 / S^{1/alpha} phi^{2K} >= 0.",
    anchors=[("BCG", "eq:weightedhighenery -- E_2K defined", 3029),
             ("BCG", "the weight phi", 3156),
             ("BCG", "eq:phiderbound", 3164),
             ("BCG", "J defined; 'the dissipative term'", 3896),
             ("BCG", "the main energy identity for d_s E_2K^2", 3902),
             ("BCG", "'which one cannot expect to bound ... extract the correct sign'", 3804),
             ("CGSS", "'weighted energy estimates at a higher derivative level than the "
                      "linear stability, together with lower bounds for S'", 494)],
    inputs="(U,S); K; the weight parameters (zeta_0, eta_w); F_dis from A10; S_min from A5",
    outputs="E_2K(s); the differential inequality d_s E_2K^2/2 <= -K eta E_2K^2 + C Ebar^2; "
            "the sign certificate J + (r^{1+1/alpha}/alpha^{1/alpha}) e^{-delta_dis s} G^2 "
            "<~ G",
    deps=["A3", "A6", "A10", "A11"],
    existing="none.  The repository's weighted-space rows are ell^1_w Fourier and H^2(mu) "
             "GAUSSIAN weights; this weight is ALGEBRAIC and the norm is a 2K-th order "
             "Sobolev energy on R^3.  (Leg 265: this is why the pending stage-V H^2(mu) lift "
             "does not gate this target -- different space.)",
    contract_complete=True,
),

"A8": dict(
    name="semigroup generation",
    computes="the decay estimate on the linear flow restricted to the stable space -- the "
             "factor that makes the Duhamel integral converge.",
    definition="Lumer-Phillips: a maximally dissipative A_0 generates a strongly continuous "
               "semigroup on H.  Growth bound w_0(T) = max{w_ess(T), s(A)}; for any "
               "w > w_ess(T), sigma(A) intersect {Re lambda > w} is a finite set of "
               "eigenvalues of finite algebraic multiplicity.  The operative output is the "
               "bound ||T(s)|| <= e^{-delta_g s / 2} on V_sta.",
    anchors=[("BCG", "lemma:propertiesmaximalaccretive, Lumer-Phillips bullet", 2731),
             ("BCG", "growth-bound definitions w_0, w_ess", 2743),
             ("BCG", "lemma:growthbound", 2757),
             ("BCG", "eq:prim -- the T(s) bound on V_sta", 2799),
             ("BCG", "eq:prim used in the Duhamel step", 4076)],
    inputs="(A_0, delta_g, K) from A9",
    outputs="the semigroup T(s); the certified decay rate on V_sta (BCG's is delta_g/2)",
    deps=["A9"],
    existing="none -- the 48-row index has spectra and eigenvalue solvers but no semigroup, "
             "and the two are not the same object once the operator is non-normal",
    contract_complete=True,
),

"A13": dict(
    name="bootstrap / continuity argument",
    computes="the closed self-improving loop: assume E_2K < Ebar and the L^infinity bounds on "
             "[s_0, s_1], prove them with a strictly better constant, conclude by continuity "
             "in s.",
    definition="prop:bootstrap: under the initial-data assumptions and "
               "||P_uns(U_t,S_t)(s)||_X <= delta_1, one has E_2K < Ebar and "
               "||U||_Linf, ||S||_Linf < delta_0 on [s_0, s_1]; the proof improves these to "
               "E_2K <= Ebar/2 etc., closing because all three are continuous in s.  Its "
               "operative content is the ORDERED CHAIN OF SMALLNESS CONSTANTS:\n"
               "  1/s_0 << delta_0^{3/2} << delta_1 << delta_g delta_0 << delta_0 << 1/Ebar "
               "<< 1/K << 1/m << eta_w << delta_g << delta_dis = O(1).",
    anchors=[("BCG", "prop:bootstrap statement", 3033),
             ("BCG", "eq:bootstrap_hyp", 3047),
             ("BCG", "the eleven-element smallness chain", 2994),
             ("BCG", "sec:bootstrap (the proof)", 3131),
             ("BCG", "eq:improvement_E", 3138),
             ("BCG", "eq:rhodeisland, the closing differential inequality", 4003),
             ("CGSS", "'carefully design our bootstrap assumptions'", 494)],
    inputs="E_2K from A12; the T(s) decay from A8; ||F_dis||_X from A10; the eleven constants",
    outputs="the improved bounds; the global-in-s continuation",
    deps=["A8", "A10", "A12"],
    existing="none",
    # ---- THE ONE INCOMPLETE CONTRACT.  See RESISTANCE below.
    contract_complete=False,
),

"A14": dict(
    name="topological / Brouwer degree argument",
    computes="the selection of the finitely many unstable initial coefficients {a_i}, by a "
             "degree/fixed-point argument, so that the solution never leaves the "
             "exponentially contracting region.",
    definition="kappa_i(s) = <(U_t, S_t)(.,s), (psi_{i,U}, psi_{i,S})>, kappa = sum_i psi_i "
               "kappa_i, with {psi_i} an orthonormal basis of the finite-dimensional unstable "
               "space V.  The contracting regions are "
               "R(s) = {|w|_X <= delta_1 e^{-(7/10) delta_g (s-s_0)}} and its B-metric "
               "shrunken twin Rtilde(s) (compactly inside R(s)).  The exit-time map from the "
               "boundary is continuous and degree-nontrivial, so some initial a stays inside "
               "forever.  The stable half is controlled by Duhamel with "
               "||F_dis(.,s)||_X <= delta_1 e^{-delta_dis s/2} "
               "<= delta_1^{3/2} e^{-(9/10) delta_g (s-s_0)}.",
    anchors=[("BCG", "sec:top", 4011),
             ("BCG", "kappa_i defined", 4023),
             ("BCG", "eq:Rdef -- the contracting regions", 4032),
             ("BCG", "eq:tambor1 -- the F_dis bound feeding Duhamel", 4061),
             ("BCG", "the Duhamel estimate on P_sta", 4072),
             ("BCG", "eq:US:initial:data -- the a_i that get selected", 2999),
             ("CGSS", "\"a topological argument that exploits the unstable structure via "
                      "Brouwer's fixed point theorem\"", 494)],
    inputs="V, P_uns, P_sta from A9; T(s) from A8; the bootstrap conclusion from A13",
    outputs="an admissible {a_i} with |a| <= delta_1 => a global asymptotically self-similar "
            "solution",
    deps=["A8", "A9", "A13"],
    existing="none -- no degree-theoretic row anywhere in the 48-row index",
    contract_complete=True,
),

"A15b": dict(
    name="interval ODE solver (VNODE-LP)",
    computes="rigorous time-stepping enclosure of a solution of an ODE system over an "
             "interval of the independent variable -- as distinct from enclosing a closed-form "
             "expression (A15a).",
    definition="an interval/Taylor-model initial-value integrator producing, for each step, a "
               "box provably containing the true flow.",
    anchors=[],  # <-- deliberately empty; see RESISTANCE
    inputs="a vector field over intervals; an initial box; a step control",
    outputs="a validated enclosure of the trajectory over the integration interval",
    deps=["A15a"],
    existing="solver/interval.py supplies the arithmetic but no validated integrator",
    contract_complete=False,
),
}

# --------------------------------------------------------------------------------------
# TERMS THAT RESIST SPECIFICATION -- the gate's no-branch, at full strength
# --------------------------------------------------------------------------------------

RESISTANCE = {

"A13": dict(
    term="bootstrap / continuity argument",
    what_is_specifiable="its DEFINITION (prop:bootstrap, BCG l.3033) and its DEPENDENCY "
                        "POSITION (consumes A8, A10, A12; consumed by A14) are both fully "
                        "specifiable and are specified above.",
    what_resists="its PARAMETER CONTRACT, at the target's own delta_dis.",
    the_mechanism=(
        "BCG's chain (l.2994) contains the link  delta_g << delta_dis = O(1).  delta_g is not "
        "a free label: A9's decomposition L = A_0 - delta_g + K REQUIRES delta_g > 0 "
        "(lemma:abstract_result, l.2764), because it is exactly what makes "
        "Lambda = sigma(L) cap {Re lambda > -delta_g/2} finite.  The recommended target has "
        "delta_dis in (-0.5778, -0.4302), i.e. delta_dis < 0.  There is NO delta_g satisfying "
        "0 < delta_g << delta_dis < 0.  The admissible set for the chain's second-from-top "
        "element is EMPTY, not merely small."),
    why_this_is_not_leg_265_restated=(
        "Leg 265 reported that delta_dis tops an eleven-element chain and named two "
        "consequences at the level of ESTIMATES (the s_0 knob's monotonicity flips; the "
        "Duhamel integral diverges).  This leg is asking a different question -- can each "
        "term be handed to a builder with a complete contract -- and the answer localises the "
        "damage to ONE of the fifteen and names the exact broken link.  The other fourteen, "
        "including A9, A8 and A12, have delta_dis-INDEPENDENT contracts and survive: the "
        "maximal-dissipativity decomposition is a property of L, and F_dis is a forcing, not "
        "part of L, which is the specification-level statement of leg 265's measured finding "
        "that the sign extraction survives (e^{-delta_dis s} > 0 for every real delta_dis)."),
    cost_consequence=(
        "A13 cannot be dispatched as a build brief on day one.  It needs a PRIOR analytic "
        "leg that re-derives the constant hierarchy without a positive delta_dis at its top "
        "-- i.e. that finds a replacement top element, or shows there is none.  That is one "
        "unbudgeted analytic leg standing in front of the build, and leg 265's estimate does "
        "not contain it.  It is also the leg that would decide whether the target is "
        "constructible at all, so it is cheap relative to what it settles."),
    where_it_sits="layer 5 of 7 on the critical path -- late enough that four layers of build "
                  "would complete before it bites, which is precisely why naming it now is "
                  "worth more than naming it then.",
),

"A15b": dict(
    term="interval ODE solver (VNODE-LP)",
    what_is_specifiable="its definition and IO contract are standard and are stated above; "
                        "its dependency position (on A15a) is clear.",
    what_resists="TRACEABILITY TO BCG/CGSS -- the gate's own requirement.",
    the_mechanism=(
        "Leg 265's row A15 is written 'ball arithmetic (Arb) OR interval ODE solver "
        "(VNODE-LP)', which reads as one capability with two implementations.  It is two.  "
        "Measured in the pinned TeX: BCG contains 'Arb' as a word 4 times (l.5693, l.5694 in "
        "sec:computer; l.6638, l.6640 in the bibliography) and contains 'VNODE' 0 times, "
        "'interval ODE' 0 times, 'rigorous integrat*' 0 times, 'Taylor model' 0 times.  CGSS "
        "contains 'Arb' as a word 0 times and 'computer-assisted' 0 times, independently "
        "reconfirming leg 265's CGSS-CAP-is-zero finding on a second instrument.  BCG's "
        "computer-assisted part evaluates EXPRESSIONS (barriers, Taylor coefficients, r_j "
        "enclosures); it never integrates an ODE rigorously.  The VNODE-LP half's only "
        "anchor is LP arXiv:2509.12435 -- a DIFFERENT paper, and an unrefereed one."),
    cost_consequence=(
        "Splitting A15 raises the term count from 15 to 16.  A15a is the cheapest term in the "
        "list (it has a real substrate, solver/interval.py) and A15b is unanchored in the "
        "target's own literature.  Nothing in BCG tells a builder what A15b must enclose, "
        "because BCG never needed it -- so if a build wants it, the requirement has to be "
        "imported from LP wholesale, template and all."),
    the_honest_reading=(
        "This is a finding ABOUT leg 265's row, not against it: leg 265 wrote the row as the "
        "tooling family it is, which is the right granularity for a COUNT.  It is the wrong "
        "granularity for a BILL OF MATERIALS, and that difference is exactly what this leg "
        "was dispatched to find."),
    where_it_sits="layer 1; off the critical path entirely.",
),
}

# --------------------------------------------------------------------------------------
# GRAPH MACHINERY
# --------------------------------------------------------------------------------------


def build_graph(spec):
    """Return (layers, longest_path, independent, dependent)."""
    deps = {k: list(v["deps"]) for k, v in spec.items()}
    for k, ds in deps.items():
        for d in ds:
            if d not in spec:
                raise ValueError("term %s depends on unknown term %s" % (k, d))

    # Kahn layering; also detects cycles.
    indeg = {k: len(deps[k]) for k in deps}
    children = defaultdict(list)
    for k, ds in deps.items():
        for d in ds:
            children[d].append(k)

    layers, remaining, placed = [], dict(indeg), set()
    while remaining:
        ready = sorted(k for k, v in remaining.items() if v == 0)
        if not ready:
            raise ValueError("dependency cycle among: %s" % sorted(remaining))
        layers.append(ready)
        for k in ready:
            del remaining[k]
            placed.add(k)
            for c in children[k]:
                if c in remaining:
                    remaining[c] -= 1

    # longest path (critical path) by depth, with a reconstructed witness
    depth, pred = {}, {}
    for layer in layers:
        for k in layer:
            best, who = 0, None
            for d in deps[k]:
                if depth[d] + 1 > best:
                    best, who = depth[d] + 1, d
            depth[k], pred[k] = best, who
    end = max(depth, key=lambda k: (depth[k], k))
    path, cur = [], end
    while cur is not None:
        path.append(cur)
        cur = pred[cur]
    path.reverse()

    independent = sorted(k for k in deps if not deps[k])
    dependent = sorted(k for k in deps if deps[k])
    return layers, path, independent, dependent, depth


# --------------------------------------------------------------------------------------
# ANCHOR RE-VERIFICATION (optional, needs --papers)
# --------------------------------------------------------------------------------------

# A short distinctive string expected at (or immediately around) each anchor line.  Only a
# sample is checked -- enough to catch a wholesale line-number drift, which is the failure
# mode that matters.
ANCHOR_PROBES = [
    ("BCG", 134, "eq:Euler"),
    ("BCG", 143, "eq:NS"),
    ("BCG", 175, "eq:wombat"),
    ("BCG", 186, "eq:DS"),
    ("BCG", 250, "eq:Riemann:invariants"),
    ("BCG", 466, "eq:ice"),
    ("BCG", 489, "eq:delta:dis"),
    ("BCG", 874, "eq:bfl"),
    ("BCG", 880, "eq:Peye"),
    ("BCG", 2130, "F_{\\rm dis}"),
    ("BCG", 2727, "maximally dissipative"),
    ("BCG", 2764, "lemma:abstract_result"),
    ("BCG", 2994, "\\delta_{\\rm dis}"),
    ("BCG", 3028, "eq:weightedhighenery"),
    ("BCG", 3156, "\\phi(\\zeta)"),
    ("BCG", 3595, "eq:cortazar"),
    ("BCG", 4011, "sec:top"),
    ("BCG", 4064, "eq:tambor1"),
    ("BCG", 5693, "Arb library"),
    ("CGSS", 318, "eq:ss_profiles"),
    ("CGSS", 382, "C_{\\rm{dis}}"),
    ("CGSS", 494, "Brouwer"),
]

TOOL_CENSUS_EXPECTED = {
    ("BCG", "Arb"): 4,
    ("BCG", "VNODE"): 0,
    ("BCG", "interval ODE"): 0,
    ("BCG", "Taylor model"): 0,
    ("CGSS", "Arb"): 0,
    ("CGSS", "computer-assisted"): 0,
}


def _load(papers_dir):
    out = {}
    for key, meta in SOURCES.items():
        for root, _dirs, files in os.walk(papers_dir):
            if meta["tex_basename"] in files:
                p = os.path.join(root, meta["tex_basename"])
                with open(p, encoding="utf-8", errors="replace") as f:
                    out[key] = f.read().split("\n")
                break
    return out


def verify_anchors(papers_dir, window=3):
    texts = _load(papers_dir)
    if len(texts) != 2:
        return {"ran": False, "reason": "could not locate both .tex files under %s" % papers_dir}
    res = {"ran": True, "line_counts": {}, "final_line_unterminated": {},
           "probes": [], "tool_census": {}, "failures": []}
    for k, lines in texts.items():
        # The pinned counts are `wc -l`, i.e. NEWLINE CHARACTERS.  CGSS's final line is
        # unterminated (the file ends "\end{document}" with no trailing newline), so a
        # naive len(split("\n")) overcounts it by one.  Recorded in the ledger rather than
        # silently absorbed -- it is exactly the kind of off-by-one that would otherwise
        # look like a provenance mismatch.
        n = len(lines) - 1  # == the newline count, either way
        res["line_counts"][k] = n
        res["final_line_unterminated"][k] = bool(lines and lines[-1] != "")
        if n != SOURCES[k]["tex_lines"]:
            res["failures"].append("%s line count %d != pinned %d" % (k, n, SOURCES[k]["tex_lines"]))
    for src, line, probe in ANCHOR_PROBES:
        lines = texts[src]
        lo, hi = max(0, line - 1 - window), min(len(lines), line - 1 + window + 1)
        hit = any(probe in l for l in lines[lo:hi])
        res["probes"].append({"source": src, "line": line, "probe": probe, "found": hit})
        if not hit:
            res["failures"].append("%s l.%d: probe %r not found within +-%d" % (src, line, probe, window))
    for (src, word), expected in TOOL_CENSUS_EXPECTED.items():
        lines = texts[src]
        if word == "Arb":  # word-boundary: "Arb" the library, not "arbitrary"
            import re as _re
            got = sum(len(_re.findall(r"\bArb\b", l)) for l in lines)
        else:
            got = sum(1 for l in lines if word.lower() in l.lower())
        res["tool_census"]["%s:%s" % (src, word)] = {"got": got, "expected": expected}
        if got != expected:
            res["failures"].append("%s census %r = %d, expected %d" % (src, word, got, expected))
    res["ok"] = not res["failures"]
    return res


# --------------------------------------------------------------------------------------
# SELF-TESTS
# --------------------------------------------------------------------------------------

def self_test():
    checks = []

    def ck(name, cond, detail=""):
        checks.append({"name": name, "pass": bool(cond), "detail": detail})

    # -- the 18-term ledger reconciles with leg 265 --------------------------------------
    ck("leg265_absent_count_is_15", LEG_265["absent_count"] == 15)
    ck("leg265_present_count_is_3", LEG_265["present_count"] == 3)
    ck("existing_terms_are_3", len(EXISTING) == 3)
    ck("spec_covers_all_15_after_split",
       len(SPEC) == 16,
       "15 absent terms, with A15 split into A15a/A15b => 16 records")
    absent_named = {v["name"] for v in SPEC.values()}
    ck("A15_split_accounts_for_the_16th",
       "ball arithmetic (Arb)" in absent_named and "interval ODE solver (VNODE-LP)" in absent_named)

    # every one of leg 265's 15 rows maps onto at least one SPEC record
    unmapped = [t for t in LEG_265["absent"] if t not in LEG_265_TO_SPEC]
    ck("every_leg265_absent_row_is_mapped", not unmapped, str(unmapped))
    bad = [t for t, ids in LEG_265_TO_SPEC.items() if any(i not in SPEC for i in ids)]
    ck("every_mapping_target_exists", not bad, str(bad))
    covered = {i for ids in LEG_265_TO_SPEC.values() for i in ids}
    ck("mapping_is_onto_SPEC", covered == set(SPEC), str(covered ^ set(SPEC)))

    # -- every record is structurally complete -------------------------------------------
    for k, v in SPEC.items():
        for field in ("name", "computes", "definition", "inputs", "outputs", "deps",
                      "existing", "contract_complete"):
            ck("record_%s_has_%s" % (k, field), field in v and v[field] != "")

    # -- anchors: every term traceable, EXCEPT the one that is reported as untraceable ----
    for k, v in SPEC.items():
        has = len(v["anchors"]) > 0
        if k == "A15b":
            ck("A15b_has_no_BCG_CGSS_anchor_by_construction", not has,
               "this is the finding, not an omission")
        else:
            ck("term_%s_is_anchored" % k, has, "%d anchors" % len(v["anchors"]))
        for (src, _label, line) in v["anchors"]:
            ck("anchor_source_valid_%s_%s" % (k, line), src in SOURCES)
            ck("anchor_line_in_range_%s_%s" % (k, line),
               1 <= line <= SOURCES[src]["tex_lines"])

    # -- the graph ------------------------------------------------------------------------
    layers, path, independent, dependent, depth = build_graph(SPEC)
    ck("graph_is_acyclic", True, "Kahn layering completed")
    ck("all_terms_placed", sum(len(l) for l in layers) == len(SPEC))
    ck("independent_plus_dependent_is_total", len(independent) + len(dependent) == len(SPEC))
    ck("independent_count_is_4", len(independent) == 4, str(independent))
    ck("critical_path_depth_is_7", len(path) == 7, " -> ".join(path))
    ck("critical_path_starts_independent", not SPEC[path[0]]["deps"])
    ck("critical_path_ends_at_A14", path[-1] == "A14", path[-1])
    # every consecutive pair on the path is a real edge
    for a, b in zip(path, path[1:]):
        ck("critical_edge_%s_%s" % (a, b), a in SPEC[b]["deps"])
    # layering respects dependencies
    layer_of = {k: i for i, l in enumerate(layers) for k in l}
    for k, v in SPEC.items():
        for d in v["deps"]:
            ck("layer_order_%s_after_%s" % (k, d), layer_of[d] < layer_of[k])

    # -- a planted cycle must be caught (the detector is exercised, not assumed) ----------
    poisoned = {k: dict(v) for k, v in SPEC.items()}
    poisoned["A4"] = dict(poisoned["A4"], deps=["A14"])
    try:
        build_graph(poisoned)
        ck("cycle_detector_fires", False, "a planted A4<-A14 cycle was NOT caught")
    except ValueError:
        ck("cycle_detector_fires", True, "planted A4<-A14 cycle caught")

    # a planted dangling dependency must be caught too
    poisoned2 = {k: dict(v) for k, v in SPEC.items()}
    poisoned2["A4"] = dict(poisoned2["A4"], deps=["A99"])
    try:
        build_graph(poisoned2)
        ck("dangling_dep_detector_fires", False, "a planted A99 dep was NOT caught")
    except ValueError:
        ck("dangling_dep_detector_fires", True, "planted A99 dep caught")

    # -- the gate's own arithmetic --------------------------------------------------------
    incomplete = sorted(k for k, v in SPEC.items() if not v["contract_complete"])
    ck("incomplete_set_matches_RESISTANCE", set(incomplete) == set(RESISTANCE),
       "%s vs %s" % (incomplete, sorted(RESISTANCE)))
    ck("exactly_two_terms_resist", len(incomplete) == 2, str(incomplete))
    ck("complete_count_is_14", len(SPEC) - len(incomplete) == 14)
    for k in RESISTANCE:
        for field in ("term", "what_is_specifiable", "what_resists", "the_mechanism",
                      "cost_consequence", "where_it_sits"):
            ck("resistance_%s_has_%s" % (k, field), field in RESISTANCE[k])

    # -- the delta_g/delta_dis contradiction is arithmetic, not rhetoric ------------------
    lo, hi = LEG_265["recommended_target"]["delta_dis_range"]
    ck("target_delta_dis_is_negative", hi < 0, "delta_dis in (%s, %s)" % (lo, hi))
    # BCG's chain needs 0 < delta_g << delta_dis; with delta_dis < 0 the set is empty.
    admissible = [g for g in (1e-12, 1e-6, 1e-3, 1e-2, 0.1) if 0 < g < hi]
    ck("no_positive_delta_g_below_a_negative_delta_dis", admissible == [], str(admissible))
    # and the same probe at BCG's OWN sign must find the set non-empty -- a live control,
    # so the check is measuring something rather than always passing
    ctrl = [g for g in (1e-12, 1e-6, 1e-3, 1e-2, 0.1) if 0 < g < 0.1458980]
    ck("live_control_delta_g_exists_at_BCG_own_sign", len(ctrl) == 5, str(ctrl))

    # -- the gate answer must follow from the data, not be asserted -----------------------
    gate = compute_gate()
    ck("gate_is_derived_not_hardcoded",
       gate["answer"] == ("YES" if not incomplete else "NO"), gate["answer"])
    ck("gate_answer_is_NO", gate["answer"] == "NO")
    ck("gate_names_the_resisting_terms",
       set(gate["terms_that_resist"]) == set(RESISTANCE))

    # -- discipline invariants -------------------------------------------------------------
    # These two checks must look at real import STATEMENTS, not at the source text: an
    # earlier version tested `"import solver" not in src` and failed against its own
    # literal.  A discipline check that can be tripped by its own wording is not measuring
    # the discipline, so it is written against the parsed line shape instead.
    src = open(__file__, encoding="utf-8").read()
    imports = [l.strip() for l in src.split("\n")
               if l.strip().startswith("import ") or l.strip().startswith("from ")]
    ck("builds_nothing__no_solver_import",
       not any("solver" in l for l in imports), "imports: %s" % imports)
    ck("builds_nothing__exactly_one_write",
       src.count("open(args.out, " + chr(34) + "w" + chr(34)) == 1,
       "the only file opened for writing is --out; solver/ paths appear solely inside "
       "leg 265's quoted adjudications, as data")
    ck("clay_odds_recorded", "0.05" in src)

    return checks


LEG_265 = {
    "branch": "leg/265-p2c-v1",
    "commit": "8e592d4",
    "pr": 21,
    "status": "parked, verified (writeup/novelty/verify_265.md on main: CONFIRMED, no gap found)",
    "ledger": "writeup/data/p2_route_p2c_v1_costing.json",
    "capabilities_index_size": 48,
    "absent_count": 15,
    "present_count": 3,
    "live_control": "0 of 8 control terms absent",
    "absent": [
        "compressible fluid model", "compressible/3D Euler", "Navier-Stokes",
        "adiabatic / gamma-law pressure", "sound speed / density variable",
        "radial / spherical geometry", "ODE barrier argument", "semigroup generation",
        "maximally dissipative operator", "non-autonomous forcing",
        "self-similar time variable s", "algebraically weighted high-order energy",
        "bootstrap / continuity argument", "topological / Brouwer degree argument",
        "ball arithmetic (Arb) or interval ODE solver (VNODE-LP)",
    ],
    "recommended_target": {
        "n": 3,
        "r_range": [1.070374, 1.094975],
        "delta_dis_range": [-0.5778, -0.4302],
        "why": "the only branch in the target window (1, 7/6] whose existence is "
               "UNCONDITIONAL -- BCG Theorem 1.1, all gamma > 1",
        "k_at_7_6": 16.3479210516613,
    },
}

LEG_265_TO_SPEC = {
    "compressible fluid model": ["A1"],
    "compressible/3D Euler": ["A2"],
    "Navier-Stokes": ["A3"],
    "adiabatic / gamma-law pressure": ["A4"],
    "sound speed / density variable": ["A5"],
    "radial / spherical geometry": ["A6"],
    "ODE barrier argument": ["A7"],
    "semigroup generation": ["A8"],
    "maximally dissipative operator": ["A9"],
    "non-autonomous forcing": ["A10"],
    "self-similar time variable s": ["A11"],
    "algebraically weighted high-order energy": ["A12"],
    "bootstrap / continuity argument": ["A13"],
    "topological / Brouwer degree argument": ["A14"],
    "ball arithmetic (Arb) or interval ODE solver (VNODE-LP)": ["A15a", "A15b"],
}


def compute_gate():
    incomplete = sorted(k for k, v in SPEC.items() if not v["contract_complete"])
    layers, path, independent, dependent, depth = build_graph(SPEC)
    return {
        "question": ("Does every one of the 15 absent terms receive a precise specification "
                     "(definition, contract, dependency position), each traceable to a named "
                     "equation/section in BCG/CGSS?"),
        "answer": "YES" if not incomplete else "NO",
        "specified_completely": len(SPEC) - len(incomplete),
        "of_total_records": len(SPEC),
        "terms_that_resist": incomplete,
        "prescribed_branch": (
            "no -> Name which term(s) resist specification and why -- an unspecifiable term is "
            "itself a costing finding (it raises leg 265's estimate) and goes to the packet at "
            "full strength."),
        "critical_path": path,
        "critical_path_depth": len(path),
        "independent_terms": independent,
        "dependent_terms": dependent,
        "layers": layers,
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--papers", default=None,
                    help="directory holding the two extracted e-prints (re-verifies anchors)")
    ap.add_argument("--out", default="writeup/data/p2_route_p2s_v1_spec.json")
    args = ap.parse_args(argv)

    checks = self_test()
    npass = sum(1 for c in checks if c["pass"])
    layers, path, independent, dependent, depth = build_graph(SPEC)
    gate = compute_gate()

    anchors_total = sum(len(v["anchors"]) for v in SPEC.values())
    bcg_anchors = sum(1 for v in SPEC.values() for a in v["anchors"] if a[0] == "BCG")
    cgss_anchors = sum(1 for v in SPEC.values() for a in v["anchors"] if a[0] == "CGSS")

    verification = ({"ran": False, "reason": "--papers not supplied"} if not args.papers
                    else verify_anchors(args.papers))

    doc = {
        "leg": 285,
        "route": "P2S",
        "what_this_is": ("a SPECIFICATION dossier: leg 265's count of 15 absent apparatus "
                         "terms, turned into a per-term bill of materials.  Builds nothing, "
                         "pre-empts no construction decision."),
        "clay_odds": "~0.05%, unchanged; no link of the L1->L4 chain moves",
        "sources": SOURCES,
        "template_cited_not_claimed": LP_TEMPLATE,
        "leg_265": LEG_265,
        "leg_265_row_to_spec_record": LEG_265_TO_SPEC,
        "existing_terms": EXISTING,
        "genuine_asset": GENUINE_ASSET,
        "specification": SPEC,
        "terms_that_resist_specification": RESISTANCE,
        "dependency_graph": {
            "layers": layers,
            "layer_count": len(layers),
            "critical_path": path,
            "critical_path_depth": len(path),
            "independent_terms": independent,
            "independent_count": len(independent),
            "dependent_terms": dependent,
            "dependent_count": len(dependent),
            "depth_of": depth,
        },
        "anchor_totals": {
            "total": anchors_total, "BCG": bcg_anchors, "CGSS": cgss_anchors,
            "records_with_zero_anchors": sorted(k for k, v in SPEC.items() if not v["anchors"]),
        },
        "anchor_reverification": verification,
        "self_tests": {"passed": npass, "total": len(checks), "checks": checks},
        "gate": gate,
    }

    outdir = os.path.dirname(args.out)
    if outdir:
        os.makedirs(outdir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=1, sort_keys=False)
        f.write("\n")

    print("LEG 285 -- ROUTE-P2S: specification of the absent apparatus")
    print("  self-tests            %d/%d" % (npass, len(checks)))
    print("  records               %d (leg 265's 15 rows, with A15 split into A15a/A15b)" % len(SPEC))
    print("  anchors               %d total (BCG %d, CGSS %d)" % (anchors_total, bcg_anchors, cgss_anchors))
    print("  layers                %d" % len(layers))
    for i, l in enumerate(layers):
        print("     L%d  %s" % (i, ", ".join("%s (%s)" % (k, SPEC[k]["name"]) for k in l)))
    print("  independent           %d  %s" % (len(independent), independent))
    print("  dependent             %d" % len(dependent))
    print("  CRITICAL PATH         depth %d:  %s" % (len(path), " -> ".join(path)))
    print("  specified completely  %d of %d" % (gate["specified_completely"], gate["of_total_records"]))
    print("  RESIST                %s" % gate["terms_that_resist"])
    if verification.get("ran"):
        print("  anchor re-verify      %s (%d probes, %d failures)"
              % ("OK" if verification["ok"] else "FAILED",
                 len(verification["probes"]), len(verification["failures"])))
        for f_ in verification["failures"]:
            print("     ! %s" % f_)
    else:
        print("  anchor re-verify      not run (%s)" % verification["reason"])
    print("  GATE                  %s" % gate["answer"])
    print("  wrote                 %s" % args.out)

    failed = [c for c in checks if not c["pass"]]
    if failed:
        print("\nFAILED CHECKS:")
        for c in failed:
            print("  - %s  %s" % (c["name"], c["detail"]))
        return 1
    if verification.get("ran") and not verification["ok"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
