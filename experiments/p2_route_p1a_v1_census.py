#!/usr/bin/env python3
"""Leg 255 (Route-P1A) -- PHASE 1 TARGET CENSUS.

    .venv/bin/python experiments/p2_route_p1a_v1_census.py

THE QUESTION (pre-committed gate, both branches, DIRECTION.md leg 255):

    Does at least one model pass all four screens jointly, with each screen's verdict carried
    per-candidate in a banked table (including the failures, with which screen killed each)?

    YES -> Bank the census table; name the surviving candidate(s) precisely, with locators for
           (i) and (iv). These are Phase 1 construction's candidate pool -- construction itself
           stays gated behind leg 257 (P1c)'s ban-lift scoping, NOT authorized here.
    NO  -> Bank the full kill table; report which screen does most of the killing, as direct
           input to whether Phase 1 needs a weaker screen (i) tier or a different technique.

THE FOUR SCREENS, and they are INDEPENDENT -- this is the caution the dispatch built into the
gate, and it has a name in the table below:

    (i)   DISSIPATIVE finite-time blow-up, PROVED or strongly supported, for the equation WITH
          its dissipative term present.
    (ii)  a SELF-SIMILAR or DSS PROFILE organising that blow-up.
    (iii) NO EXISTING CERTIFICATE for that profile -- screened against leg 174's occupancy
          matrix, capabilities.py, solver/viscous_novelty.py::PRECEDENTS, this repository's own
          precedent sweeps (legs 240/242/245/246), AND this leg's outside searches
          (writeup/novelty/leg_255.md).
    (iv)  a nonlinearity INSIDE BREDEN-CHU'S STATED REACH, in Remark 40's own terms.

    VISCOUS BURGERS IS THE CAUTION ROW. It is Breden-Chu's home ground -- parabolic, certified,
    screen (iv) PASS, screen (ii) PASS -- and it DOES NOT BLOW UP. It is killed by screen (i).
    "Parabolic and certifiable" is not "blows up"; the table is built so that this is visible
    rather than argued.

THE SUB-FLAG THAT IS NOT A SCREEN BUT IS THE POINT (leg 240's own words: move the viscous term
from DOMINATED to ENCLOSED). Screen (ii) as dispatched asks only for a self-similar/DSS profile.
Several candidates have one whose PROFILE EQUATION CARRIES NO DISSIPATION -- BCG/CGSS/MRRS
(inviscid Euler profile, viscosity paid for by a scaling-exponent restriction), fractal Burgers
(the inviscid Burgers shock profile). Enclosing those profiles would re-occupy leg 174's Grade-B
cell, not the empty one. So `profile_carries_dissipation` is carried PER ROW and reported
BOTH WAYS: the gate is answered on the four dispatched screens, and the ENCLOSED-restricted
count is reported alongside. The screen is not silently redefined.

Two further sub-flags, for the same reason:
  `profile_explicit`      -- a closed-form profile has NOTHING to enclose; a certificate on it
                             would be vacuous. Recorded, not used to fail a dispatched screen.
  `dss_lane_flag`         -- rows whose profile is DISCRETELY self-similar. The DSS lane's
                             expensive entrance is BANNED and is leg 254's / the user's call.
                             Recorded per row; NOT decided here.

WHY THE VERDICT IS COMPUTED (lesson 90 -- a control that cannot come out differently is not a
control). `screen_verdicts()` derives each row's four verdicts from its evidence fields, and
`classify()` derives the gate from the resulting table. `self_test()` perturbs the evidence and
requires BOTH gate branches to be reachable, plus each screen to be reachable as the sole
killer. `assert_probe_is_live()` fails the run if the table degenerates -- if no row is killed
by any screen, or if every row is killed, the table is not measuring anything.

WHAT THIS IS NOT. No certificate is built. No construction is attempted or authorized. No stage
is claimed; plan_of_record.py is untouched. solver/viscous_novelty.py is NOT read, imported or
edited by this module. No link of the L1->L4 chain moves; Clay stays ~0.05%.

PROVENANCE. Every network result is transcribed as data below from the searches and fetches
logged verbatim in writeup/novelty/leg_255.md, run 2026-08-07. No network access at run time.
"""

import json
import os

RUN_DATE = "2026-08-07"

# --------------------------------------------------------------------------------------
# Screen (iv)'s definition, quoted from the source rather than paraphrased. Located by leg
# 245 at line 1687 of the md5-pinned extraction ff7a34b776bfe5edf97397e5eabdbb7a of
# arXiv:2404.04054 (Breden & Chu, Numer. Math., DOI 10.1007/s00211-025-01504-4).
# --------------------------------------------------------------------------------------
REMARK_40 = {
    "paper": "arXiv:2404.04054",
    "who": "Maxime Breden, Hugo Chu",
    "line": 1687,
    "extraction_md5": "ff7a34b776bfe5edf97397e5eabdbb7a",
    "located_by": "leg 245 (Route-BCL2)",
    "verbatim": (
        "We deal with a one-dimensional example here for simplicity, but terms like (u.grad)u "
        "could in principle also be handled in dimension d in {2,3}, as u in H^2(mu) is then "
        "still enough to guarantee that (u.grad)u in L^2(mu) since u in L^inf(R^d)."
    ),
}

# The reach clause, made operational. A row passes screen (iv) iff BOTH hold.
REACH_RULE = {
    "nonlinearity": (
        "LOCAL and polynomial in u and its first derivatives -- exactly what the embedding "
        "H^2(mu) -> L^inf(R^d) named in Remark 40 buys. NOT named, therefore recorded as "
        "OUTSIDE: Hilbert transform, Biot-Savart, the LERAY PROJECTION (the pressure), "
        "Fourier restriction, averaging operators."
    ),
    "principal_part": (
        "the Laplacian / Ornstein-Uhlenbeck operator on H^2(mu), mu = e^{|x|^2/4}, over R^d "
        "with d <= 3. NOT named, therefore OUTSIDE: fractional (-Delta)^alpha or Lambda^gamma "
        "for non-even gamma; sequence/shell ladders; free boundaries; quasilinear principal "
        "parts (geometric flows); singular-sonic-point ODE systems."
    ),
    "the_groups_own_stated_limit": (
        "arXiv:2603.27198 line 273 (2026-03-28, located by leg 245): extending merely from an "
        "interval to a higher-dimensional RECTANGLE 'is non-trivial but will be studied in a "
        "future work.' The reach is stated in principle and undone in practice, at both ends, "
        "by the same group."
    ),
}

# The caution the dispatch built into the gate, transcribed from the same extraction.
BURGERS_CAUTION = {
    "line": 1669,
    "verbatim": (
        "We focus on a generalised viscous Burgers equation on R_+ with Neumann boundary "
        "condition"
    ),
    "why_it_is_in_the_table": (
        "d_t v + v^2 d_x v = d_xx v is parabolic, is Breden-Chu's own certified example, has a "
        "self-similar profile t^{-1/4}u(x/sqrt t), and DOES NOT BLOW UP (maximum principle). "
        "Screens (i) and (iv) are independent; it passes (iv) and (ii) and is killed by (i)."
    ),
}

# --------------------------------------------------------------------------------------
# THE CENSUS. Each row carries EVIDENCE, not verdicts; screen_verdicts() derives the verdicts.
#
#   blowup      : "PROVED" | "STRONGLY_SUPPORTED" | "NOT_PROVED" | "NO_BLOWUP"
#   ss_profile  : "SELF_SIMILAR" | "DSS" | "ASYMPTOTICALLY_SELF_SIMILAR" | "NONE" |
#                 "UNCONFIRMED_IN_THIS_REALIZATION"
#   certificate : "NONE" | "FULL" | "PARTIAL" | "FAMILY_CERTIFIED"
#   nonlocal_terms / principal_part_ok : screen (iv)'s two halves
# --------------------------------------------------------------------------------------
CANDIDATES = [

    # ---- the caution row -------------------------------------------------------------
    dict(
        key="VISCOUS-BURGERS-BC", model="1D generalised viscous Burgers on R_+ (Breden-Chu's own example)",
        locator="arXiv:2404.04054 l.1669", fluid_adjacent=False,
        blowup="NO_BLOWUP",
        blowup_evidence="maximum principle / Cole-Hopf: no finite-time blow-up. This is the CAUTION row.",
        ss_profile="SELF_SIMILAR", profile_locator="t^{-1/4}u(x/sqrt t); profile Lu - u/4 + u^2 d_x u = 0",
        profile_carries_dissipation=True, profile_explicit=False,
        certificate="FULL", certificate_locator="arXiv:2404.04054 itself -- Grade A, Newton-Kantorovich on H^2(mu)",
        nonlocal_terms=[], principal_part_ok=True,
    ),

    # ---- the two Grade-A occupants of the NON-FLUID cell ------------------------------
    dict(
        key="DF-CGL", model="complex Ginzburg-Landau, radial self-similar singular solutions",
        locator="arXiv:2410.05480 (Dahne, Figueras), Thm 1.2 / Thm 4.1", fluid_adjacent=False,
        blowup="PROVED",
        blowup_evidence="leg 174: 'the CGL equation with eps = eps_j(s) has a self-similar singular solution'; eps'_j(0) > 0 so dissipation strictly positive along the branch.",
        ss_profile="SELF_SIMILAR", profile_locator="enclosed ODE (3)/(4)/(5) carries the factor (1 - i eps) throughout",
        profile_carries_dissipation=True, profile_explicit=False,
        certificate="FULL", certificate_locator="leg 174 occupancy matrix, cell (fluid=False, grade=A); viscous_novelty PRECEDENTS verdict PRE_EMPTS; author line closed by leg 242 (unmoved 668 days)",
        nonlocal_terms=[], principal_part_ok=True,
    ),
    dict(
        key="BD-HMHF", model="corotational harmonic map heat flow R^3 -> S^3, supercritical",
        locator="arXiv:1610.09496v2 (Biernat, Donninger)", fluid_adjacent=False,
        blowup="PROVED",
        blowup_evidence="abstract, verbatim: 'We prove the existence of a (spectrally) stable self-similar blow-up solution f_0 to the heat flow for corotational harmonic maps from R^3 to the three-sphere.'",
        ss_profile="SELF_SIMILAR", profile_locator="monotone self-similar profile f_0; the parabolic (dissipative) operator is inside the enclosed object",
        profile_carries_dissipation=True, profile_explicit=False,
        certificate="FULL", certificate_locator="abstract, verbatim: 'A key ingredient is the use of interval arithmetic: a rigorous computer-assisted method for estimating functions.' FOUND BY THIS LEG (query Q5); ABSENT from leg 174's matrix, from viscous_novelty PRECEDENTS and from LITERATURE_CHECK.md.",
        nonlocal_terms=[], principal_part_ok=True,
        note="Second, INDEPENDENT and EIGHT-YEARS-EARLIER occupant of the same (fluid=False, grade=A) cell DF-CGL occupies. Does not change which cell is empty; does change how well evidenced the METHOD half of Phase 1 is.",
    ),

    # ---- the semilinear-parabolic family ----------------------------------------------
    dict(
        key="FUJITA-HEAT", model="semilinear heat u_t = Delta u + u^p",
        locator="Herrero-Velazquez / Troy self-similar profiles", fluid_adjacent=False,
        blowup="PROVED", blowup_evidence="classical: finite-time blow-up for p > 1, Fujita.",
        ss_profile="SELF_SIMILAR", profile_locator="exact self-similar blow-up profiles in the supercritical range",
        profile_carries_dissipation=True, profile_explicit=False,
        certificate="FAMILY_CERTIFIED",
        certificate_locator="Lessard-Matsue-Takayasu, J. Nonlinear Sci. 33 (2023) arXiv:2103.12390; Takayasu-Lessard-Jaquette-Okamoto, Numer. Math. 151 (2022) doi 10.1007/s00211-022-01291-2; Matsue-Takayasu, Numer. Math. (2020) doi 10.1007/s00211-020-01125-z. Rigorous-numerics apparatus is established ON THIS EQUATION FAMILY; whether the SELF-SIMILAR PROFILE itself is the enclosed object is NOT established by this leg's realization -- recorded as FAMILY_CERTIFIED, not FULL.",
        nonlocal_terms=[], principal_part_ok=True,
    ),
    dict(
        key="GELFAND-EXP", model="semilinear heat with exponential nonlinearity u_t = Delta u + e^u",
        locator="Frank-Kamenetskii / Gelfand", fluid_adjacent=False,
        blowup="PROVED", blowup_evidence="classical finite-time blow-up.",
        ss_profile="SELF_SIMILAR", profile_locator="self-similar profiles in high dimension",
        profile_carries_dissipation=True, profile_explicit=False,
        certificate="FAMILY_CERTIFIED",
        certificate_locator="same rigorous-numerics author line as FUJITA-HEAT (quasi-homogeneous compactification methods cover exponential nonlinearities). Recorded FAMILY_CERTIFIED on the same conservative reading.",
        nonlocal_terms=[], principal_part_ok=True,
    ),
    dict(
        key="VISCOUS-HJ-GRAD", model="viscous Hamilton-Jacobi u_t = Delta u + |grad u|^p, p > 2",
        locator="Alaa; Souplet-Zhang gradient blow-up", fluid_adjacent=False,
        blowup="PROVED", blowup_evidence="gradient blow-up (|grad u| -> inf, u stays bounded) proved for p > 2.",
        ss_profile="NONE",
        profile_locator="the gradient blow-up is boundary-localised and of type II; no self-similar profile organises it. For p = 2 the Cole-Hopf transform gives GLOBAL existence -- no blow-up at all.",
        profile_carries_dissipation=False, profile_explicit=False,
        certificate="NONE", certificate_locator="none found",
        nonlocal_terms=[], principal_part_ok=True,
        note="Passes (i), (iii) and (iv). Killed by (ii) alone -- the row that shows screen (ii) is not free.",
    ),

    # ---- Keller-Segel: the survivors ---------------------------------------------------
    dict(
        key="KS3D-EXPLICIT", model="parabolic-elliptic Keller-Segel, d = 3, the explicit Type I profile",
        locator="Glogic-Schorkhuber arXiv:2209.11206 (radial stability); nonradial arXiv:2501.07073",
        fluid_adjacent=False,
        blowup="PROVED",
        blowup_evidence="Glogic-Schorkhuber prove nonlinear RADIAL stability of an explicit self-similar blow-up solution in d = 3, resolving a two-decade-old conjecture; Winkler et al. establish finite-time blow-up broadly.",
        ss_profile="SELF_SIMILAR",
        profile_locator="Type I self-similar: diffusion is SCALE-INVARIANT under the blow-up scaling, so the profile equation carries Delta at the SAME order as the drift -- structurally ENCLOSED, the DF-CGL position, not the BCG one.",
        profile_carries_dissipation=True, profile_explicit=True,
        certificate="NONE",
        certificate_locator="no interval-arithmetic enclosure found (queries Q4, Q7). The nearest apparatus: in the nonradial work computer assistance is used to EVALUATE TWO INTEGRALS, not as a validated enclosure -- recorded rather than rounded to zero (leg 246's discipline).",
        nonlocal_terms=[],
        principal_part_ok=True,
        reach_note="Written as the SYSTEM (u, c): u_t = Delta u - div(u grad c), 0 = Delta c + u, the nonlinearity is div(u grad c) = grad u . grad c - u^2 -- LOCAL and quadratic in u and first derivatives, i.e. exactly the shape Remark 40's H^2(mu) -> L^inf argument covers, at d = 3 which is inside Remark 40's own d in {2,3}. Radially it reduces further to a 1D ODE in the mass variable. The elliptic second equation is an EXTENSION of the parabolic setting Breden-Chu wrote (recorded; it does not introduce a NONLOCAL term, which is what the reach rule tests).",
        note="Passes all four screens, but the profile is CLOSED FORM -- there is nothing for an enclosure to do. Recorded as a VACUOUS target, not as the answer.",
    ),
    dict(
        key="KS3D-NONEXPLICIT", model="parabolic-elliptic Keller-Segel, d = 3, the NON-explicit self-similar profiles",
        locator="arXiv:2503.02263 (infinitely many self-similar blow-up profiles, d = 3..9); Collot-Zhang arXiv:2406.11358",
        fluid_adjacent=False,
        blowup="PROVED",
        blowup_evidence="same equation as KS3D-EXPLICIT; blow-up proved. arXiv:2503.02263 constructs countably many self-similar profiles in d = 3..9 by matched asymptotics + Banach fixed point; Collot-Zhang give finite-Lipschitz-codimension stability with codimension = number of unstable eigenmodes.",
        ss_profile="SELF_SIMILAR",
        profile_locator="countably many NON-explicit Type I profiles; same ENCLOSED scaling position as the explicit one.",
        profile_carries_dissipation=True, profile_explicit=False,
        certificate="NONE",
        certificate_locator="constructed by matched asymptotic expansions and a Banach fixed point -- an ANALYTIC construction, explicitly not computer-assisted (query Q4). No interval-arithmetic enclosure found anywhere in this realization.",
        nonlocal_terms=[],
        principal_part_ok=True,
        reach_note="identical to KS3D-EXPLICIT's; see there.",
        note="THE ONE CLEAN SURVIVOR: dissipative, proved blow-up, a non-explicit self-similar profile whose equation CARRIES the dissipation, no certificate, local quadratic nonlinearity at d = 3. NOT fluid-adjacent -- it would occupy the cell BD-HMHF and DF-CGL already occupy, not leg 174's empty one.",
    ),

    # ---- the one fluid-adjacent carrier ------------------------------------------------
    dict(
        key="KS-NS-LI-ZHOU", model="3D Keller-Segel-Navier-Stokes with buoyancy",
        locator="arXiv:2404.17228 (Li, Zhou), Comm. Math. Phys. (2025) doi 10.1007/s00220-025-05371-w",
        fluid_adjacent=True,
        blowup="PROVED",
        blowup_evidence="abstract, verbatim: 'we use a quantitative method to directly construct a smooth finite-time blowup solution for the Keller-Segel-Navier-Stokes system with buoyancy in 3D'; with 'a robust localization argument to find blowup solutions with non-negative density and finite mass'.",
        ss_profile="SELF_SIMILAR",
        profile_locator="abstract, verbatim: the heart of the proof is 'the non-radial finite-codimensional stability of an explicit self-similar blowup solution to 3D Keller-Segel equation'. The self-similar object is the KELLER-SEGEL profile; the Navier-Stokes velocity is carried, not the blowing-up self-similar object.",
        profile_carries_dissipation=True, profile_explicit=True,
        certificate="NONE",
        certificate_locator="no mention of computer-assisted proof or interval arithmetic in the fetched abstract (query Q6).",
        nonlocal_terms=["Leray projection (the pressure) in the Navier-Stokes component"],
        principal_part_ok=True,
        reach_note="Remark 40 names (u.grad)u and gives its reason. It does NOT name the LERAY PROJECTION, which is what makes the incompressible NS component's nonlinearity nonlocal, and boundedness of the Leray projector on the Gaussian-weighted L^2(mu) is not a consequence of the H^2(mu) -> L^inf embedding Remark 40 argues from. Recorded as OUTSIDE THE STATED REACH -- an honest strict reading, and the single most consequential judgement in this table.",
        note="THE FLUID ROW. Clears (i), (ii) and (iii) and is killed by (iv) alone, on the Leray clause. This is the closest any candidate gets to leg 174's empty cell.",
    ),

    # ---- the DOMINATED family (leg 174 Grade B / leg 240) -----------------------------
    dict(
        key="BCG-NS", model="3D isentropic compressible Navier-Stokes, imploding solutions",
        locator="arXiv:2208.09445 (Buckmaster, Cao-Labora, Gomez-Serrano), Forum Math. Pi 13 (2025) e6",
        fluid_adjacent=True,
        blowup="PROVED", blowup_evidence="leg 174: Thm 1.3, smooth finite-energy data, density blows up at the origin; Lame viscosities mu_1 > 0, 2mu_1 + mu_2 > 0.",
        ss_profile="SELF_SIMILAR",
        profile_locator="the enclosed profile solves system (1.5) -- the ODE reduction of the INVISCID compressible Euler system (1.3).",
        profile_carries_dissipation=False, profile_explicit=False,
        certificate="FULL", certificate_locator="leg 174, cell (fluid=True, grade=B); 'interval arithmetic will be used as part of the proof whenever needed', ~14 CPU-hours; viscous_novelty PRECEDENTS verdict EXCLUSION.",
        nonlocal_terms=[], principal_part_ok=False,
        note="Viscosity is DOMINATED by a scaling-exponent restriction (r > 2gamma/(gamma+1)), never enclosed -- leg 240 measured the domination margin as delta_dis <= 0.1458980 on a window of width 2.43e-02 at gamma = 7/5.",
    ),
    dict(
        key="CGSS-NONRADIAL", model="non-radial implosion, compressible Euler and Navier-Stokes on T^3 and R^3",
        locator="arXiv:2310.05325 (Cao-Labora, Gomez-Serrano, Shi, Staffilani), Cambridge J. Math. 13(4) 753-885",
        fluid_adjacent=True,
        blowup="PROVED", blowup_evidence="leg 240: a strictly stronger THEOREM than the parent (non-radial, periodic and whole-space).",
        ss_profile="SELF_SIMILAR",
        profile_locator="leg 240, l.251 verbatim: 'From [8, 51], we know that there exist radially symmetric profiles (U, S) that solve (1.5) for nu = 0'. The inherited object is inviscid and the paper says so.",
        profile_carries_dissipation=False, profile_explicit=False,
        certificate="NONE",
        certificate_locator="leg 240: full-text census over 6642 lines -- 'interval arithmetic' 0, 'computer-assisted' 0, 'enclosure' 0, 'validated numerics' 0, 'certif' 0, 'rigorous' 0. It has NO certification apparatus of its own.",
        nonlocal_terms=[], principal_part_ok=False,
        note="Passes (iii) and dies on (iv); and its profile is inviscid, so it would not fill the empty cell even if (iv) passed. Leg 240's delta_dis inequality is bit-identical to the parent's (max abs deviation 1.78e-15) fourteen months later.",
    ),
    dict(
        key="MRRS-NS", model="3D compressible Navier-Stokes, implosion (analytic)",
        locator="Merle-Raphael-Rodnianski-Szeftel, Ann. of Math. 196 (2022); leg 174 catalog row",
        fluid_adjacent=True,
        blowup="PROVED", blowup_evidence="published, Bocher Prize 2023.",
        ss_profile="SELF_SIMILAR", profile_locator="self-similar profile of the INVISCID reduction; existence for almost every gamma via a non-vanishing condition on an analytic function.",
        profile_carries_dissipation=False, profile_explicit=False,
        certificate="NONE",
        certificate_locator="leg 174, quoting BCG sec 1.1.2: the hypothesis 'is not proven for any specific gamma; however it may be checked numerically' -- numerically CHECKED, not certified. BCG then discharged it at gamma = 7/5 with interval arithmetic.",
        nonlocal_terms=[], principal_part_ok=False,
        note="Passes (i), (ii) and (iii); killed by (iv) -- a singular sonic-point ODE system, not a parabolic profile on H^2(mu). And its profile is inviscid.",
    ),

    # ---- the nonlocal-dissipation family ----------------------------------------------
    dict(
        key="KNS-FRACBURGERS", model="fractal Burgers u_t + u u_x + (-Delta)^alpha u = 0, alpha < 1/2",
        locator="Kiselev-Nazarov-Shterenberg arXiv:0804.3549, Dyn. PDE 5 (2008) 211-240",
        fluid_adjacent=False,
        blowup="PROVED", blowup_evidence="finite-time blow-up proved for alpha < 1/2; global existence and analyticity for alpha >= 1/2.",
        ss_profile="ASYMPTOTICALLY_SELF_SIMILAR",
        profile_locator="arXiv:2105.15128, asymptotically self-similar shock formation -- the profile approached is the INVISCID Burgers shock profile, the fractional dissipation subordinate to it.",
        profile_carries_dissipation=False, profile_explicit=True,
        certificate="NONE", certificate_locator="none found (query Q9).",
        nonlocal_terms=["fractional Laplacian (-Delta)^alpha, alpha < 1/2"], principal_part_ok=False,
        note="A DOMINATED row on a model nobody in this repository had checked for it. Killed by (iv); the ENCLOSED sub-flag kills it a second time.",
    ),
    dict(
        key="CHEN-GCLM-DISS", model="dissipative gCLM, nu Lambda^gamma",
        locator="J. Chen, Nonlinearity 33 (2020) 2502; arXiv:1908.09385; leg 174 catalog row",
        fluid_adjacent=True,
        blowup="PROVED", blowup_evidence="blow-up with fractional dissipation established for the gCLM family.",
        ss_profile="NONE",
        profile_locator="leg 125/174, sec 2.6 last line verbatim: 'Since nu(t) converges to 0, such profile is the same as the inviscid profile associated with a.' There is NO gamma = 2 dissipative self-similar profile in the paper.",
        profile_carries_dissipation=False, profile_explicit=False,
        certificate="NONE",
        certificate_locator="leg 246: the Ambrose-Lushnikov-Siegel-Silantyev line produced 19 subsequent works over 1483 days, 2 on the object, 0 carrying apparatus over a 10-term census of 4336 md5-pinned lines.",
        nonlocal_terms=["Hilbert transform", "Lambda^gamma for non-even gamma"], principal_part_ok=False,
        ban_flag="Construction on any gCLM object is BANNED ('another gCLM measurement leg', lift: never -- the model is exhausted, Stage 3.5 leg 42). This row is a literature verdict, not a measurement.",
        note="Killed by (ii) and (iv) independently, and barred from construction by a standing ban besides.",
    ),

    # ---- the engineered / ladder family ------------------------------------------------
    dict(
        key="TAO-AVGNS", model="averaged 3D Navier-Stokes",
        locator="Tao, JAMS 29 (2016) 601-674; arXiv:1402.0290; leg 174 catalog row",
        fluid_adjacent=True,
        blowup="PROVED", blowup_evidence="leg 174: 'the only entry that does not weaken the dissipation' -- full 3D viscosity and the exact energy identity retained.",
        ss_profile="DSS", profile_locator="a delayed, approximately discretely-self-similar energy cascade across scales.",
        profile_carries_dissipation=True, profile_explicit=False,
        certificate="NONE", certificate_locator="none.",
        nonlocal_terms=["averaged bilinear operator (a nonlocal Fourier multiplier average)"], principal_part_ok=False,
        dss_lane=True,
        note="leg 174's own caveat stands: the averaged bilinear operator is ENGINEERED for the blow-up, so certifying it would certify a constructed counterexample. Killed by (iv).",
    ),
    dict(
        key="MILLER-FR-HYPO", model="Fourier-restricted hypodissipative Navier-Stokes",
        locator="arXiv:2307.03434 (Miller)", fluid_adjacent=True,
        blowup="PROVED",
        blowup_evidence="fetched: blow-up for alpha < log(3)/(6 log 2) ~ 0.264; the model 'respects both the energy equality and the identity for enstrophy growth from the full Euler and hypodissipative Navier-Stokes equations respectively', with '(u.grad)u nonlinearity otherwise unchanged'.",
        ss_profile="DSS",
        profile_locator="a dyadic-shell cascade under a discrete group of symmetries (odd, permutation symmetric, mirror symmetric). Fetched abstract does not state an exact self-similar profile.",
        profile_carries_dissipation=True, profile_explicit=False,
        certificate="NONE", certificate_locator="no computational verification indicated in the fetched abstract.",
        nonlocal_terms=["Fourier restriction to a dyadic shell structure", "fractional (hypo)dissipation (-Delta)^alpha"],
        principal_part_ok=False, dss_lane=True,
        ban_flag="Its natural certification space is a Fourier/sequence ladder -- exactly the ell^1-Fourier / radii-polynomial machinery this repository has measured DEAD in three realizations and which is BANNED on ANY model (re-posed 2026-08-06). Recorded as a forward constraint for leg 257, not a lift request.",
    ),
    dict(
        key="PALASEK-SHELL", model="elementary shell model of the 3D Navier-Stokes equations",
        locator="arXiv:2605.13827 (Palasek), 2026-05-13", fluid_adjacent=True,
        blowup="PROVED",
        blowup_evidence="fetched: finite-time blow-up with full viscosity, smooth (rapidly frequency-decaying) initial data AND FORCING; the inviscid unforced case treated separately, with singularity formation just above the energy level.",
        ss_profile="UNCONFIRMED_IN_THIS_REALIZATION",
        profile_locator="the fetched abstract does not state a self-similar or DSS structure. Recorded as UNCONFIRMED IN THIS REALIZATION -- NOT as a claim that none exists.",
        profile_carries_dissipation=True, profile_explicit=False,
        certificate="NONE", certificate_locator="none.",
        nonlocal_terms=[], principal_part_ok=False,
        ban_flag="Same ladder/banned-machinery constraint as MILLER-FR-HYPO.",
        note="leg 174 called this 'the most tractable target on the list'. In this census it is killed by (ii) unconfirmed and by (iv) -- a countable ODE ladder is not H^2(mu) on R^d. A full-text read is the cheapest way to move its (ii) verdict.",
    ),

    # ---- the no-blow-up and no-profile controls ---------------------------------------
    dict(
        key="KVW-PRANDTL", model="Prandtl boundary layer",
        locator="Kukavica-Vicol-Wang, Adv. Math. 307 (2017) 288-311; leg 174 catalog row",
        fluid_adjacent=True,
        blowup="PROVED", blowup_evidence="finite-time blow-up of the Prandtl system, viscous and NS-derived.",
        ss_profile="NONE",
        profile_locator="the proof is a functional/monotonicity argument, not profile-based; the van Dommelen-Shen separation singularity is not established as an enclosed self-similar profile.",
        profile_carries_dissipation=False, profile_explicit=False,
        certificate="NONE", certificate_locator="none.",
        nonlocal_terms=["the vertical velocity v recovered by an integral in y (divergence constraint)"],
        principal_part_ok=False,
    ),
    dict(
        key="MCF-NECKPINCH", model="mean curvature flow, degenerate neckpinch",
        locator="Angenent-Velazquez; Angenent-Knopf (Ricci analogue)", fluid_adjacent=False,
        blowup="PROVED", blowup_evidence="finite-time singularity of a parabolic geometric flow, proved.",
        ss_profile="SELF_SIMILAR", profile_locator="self-shrinker / self-similar profile organises the singularity.",
        profile_carries_dissipation=True, profile_explicit=False,
        certificate="NONE", certificate_locator="none found in this realization.",
        nonlocal_terms=[], principal_part_ok=False,
        note="Killed by (iv) alone: a QUASILINEAR geometric principal part, not the Laplacian/OU operator on H^2(mu). The row that isolates the principal-part half of screen (iv).",
    ),
    dict(
        key="NSE-3D", model="3D incompressible Navier-Stokes itself",
        locator="the Clay problem", fluid_adjacent=True,
        blowup="NOT_PROVED", blowup_evidence="no proof of finite-time blow-up exists. The trivial screen-(i) control.",
        ss_profile="NONE",
        profile_locator="Necas-Ruzicka-Sverak and Tsai EXCLUDE nontrivial exactly-backward-self-similar 3D NS blow-up under the relevant decay (CONTINUATION_PROMPT Directive 1). Any admissible ansatz must be DSS, unstable-self-similar with finite unstable spectrum, or non-self-similar.",
        profile_carries_dissipation=True, profile_explicit=False,
        certificate="NONE", certificate_locator="none.",
        nonlocal_terms=["Leray projection (the pressure)"], principal_part_ok=True,
        note="Carried so the census cannot be read as having quietly skipped the actual target. Killed by (i) and (ii).",
    ),
    dict(
        key="BOUSSINESQ-VISC", model="2D Boussinesq with full viscosity and diffusivity",
        locator="this repository's own Route-B/D substrate", fluid_adjacent=True,
        blowup="NOT_PROVED", blowup_evidence="no finite-time blow-up proof with full dissipation; Chen-Hou's certified singularity is the INVISCID (boundary, smooth-data) case.",
        ss_profile="NONE", profile_locator="no dissipative self-similar profile established.",
        profile_carries_dissipation=False, profile_explicit=False,
        certificate="NONE", certificate_locator="the inviscid case is arXiv:2210.07191 + 2305.05660, viscous_novelty verdict EXCLUSION.",
        nonlocal_terms=["Biot-Savart"], principal_part_ok=True,
        note="The second screen-(i) control, and the one closest to this repository's own hands.",
    ),
]

FOUR_SCREENS = ["i_dissipative_blowup", "ii_ss_profile", "iii_no_certificate", "iv_bc_reach"]


# --------------------------------------------------------------------------------------
# Verdicts are DERIVED, not stored.
# --------------------------------------------------------------------------------------
def screen_verdicts(row):
    """Derive the four screen verdicts from a row's evidence fields."""
    v = {}

    # (i) dissipative finite-time blow-up, proved or strongly supported
    v["i_dissipative_blowup"] = {
        "PROVED": "PASS", "STRONGLY_SUPPORTED": "PASS",
        "NOT_PROVED": "FAIL", "NO_BLOWUP": "FAIL",
    }[row["blowup"]]

    # (ii) a self-similar or DSS profile
    v["ii_ss_profile"] = {
        "SELF_SIMILAR": "PASS", "DSS": "PASS", "ASYMPTOTICALLY_SELF_SIMILAR": "PASS",
        "NONE": "FAIL", "UNCONFIRMED_IN_THIS_REALIZATION": "FAIL",
    }[row["ss_profile"]]

    # (iii) no existing certificate
    v["iii_no_certificate"] = {
        "NONE": "PASS", "PARTIAL": "CONTESTED",
        "FAMILY_CERTIFIED": "CONTESTED", "FULL": "FAIL",
    }[row["certificate"]]

    # (iv) inside Breden-Chu's stated reach: BOTH halves of REACH_RULE
    v["iv_bc_reach"] = "PASS" if (not row["nonlocal_terms"] and row["principal_part_ok"]) else "FAIL"
    return v


def killers(row):
    """Which of the four screens fail (or are contested) for this row."""
    v = screen_verdicts(row)
    return [s for s in FOUR_SCREENS if v[s] != "PASS"]


def classify(rows):
    """Derive the gate answer from the table. Returns (verdict_code, gate_answer)."""
    survivors = [r for r in rows if not killers(r)]
    if not survivors:
        return "NO_MODEL_PASSES_ALL_FOUR", "NO"
    clean = [r for r in survivors if not r.get("profile_explicit")]
    fluid = [r for r in survivors if r.get("fluid_adjacent")]
    if fluid:
        return "SURVIVOR_IS_FLUID_ADJACENT", "YES"
    if clean:
        return "SURVIVOR_NON_FLUID_NON_VACUOUS", "YES"
    return "SURVIVOR_ONLY_VACUOUS_TARGET", "YES"


FLUID_STRUCTURE_NONLOCALITIES = ("Leray", "Biot-Savart", "Hilbert", "Fourier restriction",
                                 "averaged")


def reach_breakdown(rows):
    """Of the rows that clear (i), (ii) and (iii), how does screen (iv) dispose of them, and
    for WHICH of its two halves? Computed, because the journal quotes these numbers."""
    clear3 = [r for r in rows
              if all(screen_verdicts(r)[s] == "PASS"
                     for s in ("i_dissipative_blowup", "ii_ss_profile", "iii_no_certificate"))]
    passes_iv = [r for r in clear3 if screen_verdicts(r)["iv_bc_reach"] == "PASS"]
    fails_iv = [r for r in clear3 if screen_verdicts(r)["iv_bc_reach"] == "FAIL"]
    by_nonlocal = [r for r in fails_iv if r["nonlocal_terms"]]
    by_principal_part_only = [r for r in fails_iv if not r["nonlocal_terms"]]
    fluid_structure = [r for r in by_nonlocal
                       if any(any(m in t for m in FLUID_STRUCTURE_NONLOCALITIES)
                              for t in r["nonlocal_terms"])]
    return {
        "clear_i_ii_iii": [r["key"] for r in clear3],
        "of_those_pass_iv": [r["key"] for r in passes_iv],
        "of_those_fail_iv": [r["key"] for r in fails_iv],
        "fail_iv_because_a_NONLOCAL_OPERATOR": [r["key"] for r in by_nonlocal],
        "fail_iv_on_the_PRINCIPAL_PART_only": [r["key"] for r in by_principal_part_only],
        "fail_iv_where_the_nonlocality_IS_the_fluid_structure": [r["key"] for r in fluid_structure],
    }


def kill_counts(rows):
    """How many rows each screen kills -- the no-branch's required reporting, computed
    regardless of the branch taken."""
    c = {s: 0 for s in FOUR_SCREENS}
    for r in rows:
        for s in killers(r):
            c[s] += 1
    return c


def sole_killer_counts(rows):
    """Rows killed by exactly one screen -- what a weaker tier would actually buy."""
    c = {s: 0 for s in FOUR_SCREENS}
    for r in rows:
        k = killers(r)
        if len(k) == 1:
            c[k[0]] += 1
    return c


# --------------------------------------------------------------------------------------
# Controls (lesson 90). A table that cannot come out differently is not a table.
# --------------------------------------------------------------------------------------
def assert_probe_is_live(rows):
    """Fail the run if the census degenerates into something that measures nothing."""
    n = len(rows)
    killed = [r for r in rows if killers(r)]
    if not killed:
        raise AssertionError("DEAD PROBE: no row is killed by any screen -- the screens are "
                             "not screening.")
    if len(killed) == n:
        raise AssertionError("DEAD PROBE: every row is killed -- no candidate pool can ever "
                             "be reported, so the yes-branch is unreachable by construction.")
    fired = {s for r in rows for s in killers(r)}
    missing = set(FOUR_SCREENS) - fired
    if missing:
        raise AssertionError(f"DEAD PROBE: screens {sorted(missing)} kill nothing -- they are "
                             f"decorative on this candidate set.")
    # every screen must ALSO be passable, or it is a constant
    for s in FOUR_SCREENS:
        if not any(screen_verdicts(r)[s] == "PASS" for r in rows):
            raise AssertionError(f"DEAD PROBE: screen {s} passes on no row -- it is a constant.")
    # the caution the dispatch demanded must be visible in the table, not just in prose
    burgers = [r for r in rows if r["key"] == "VISCOUS-BURGERS-BC"][0]
    bv = screen_verdicts(burgers)
    if bv["iv_bc_reach"] != "PASS" or bv["i_dissipative_blowup"] != "FAIL":
        raise AssertionError("DEAD PROBE: the viscous-Burgers caution row must PASS screen (iv) "
                             "and FAIL screen (i) -- screens (i) and (iv) are independent.")


def self_test():
    """Both gate branches, and each screen as a sole killer, must be reachable on perturbed
    evidence. Returns the set of outcomes actually reached."""
    reached = {}

    # 0. the real table
    reached["actual"] = classify(CANDIDATES)[0]

    # 1. NO branch: certify the one clean survivor and the vacuous one
    import copy
    t = copy.deepcopy(CANDIDATES)
    for r in t:
        if r["key"] in ("KS3D-NONEXPLICIT", "KS3D-EXPLICIT"):
            r["certificate"] = "FULL"
    reached["all_certified"] = classify(t)[0]

    # 2. YES/fluid branch: relax the Leray clause on the fluid row
    t = copy.deepcopy(CANDIDATES)
    for r in t:
        if r["key"] == "KS-NS-LI-ZHOU":
            r["nonlocal_terms"] = []
    reached["leray_relaxed"] = classify(t)[0]

    # 3. YES/vacuous-only branch: kill the non-explicit KS profiles only
    t = copy.deepcopy(CANDIDATES)
    for r in t:
        if r["key"] == "KS3D-NONEXPLICIT":
            r["certificate"] = "FULL"
    reached["only_explicit_left"] = classify(t)[0]

    # 4. screen (i) alone must be able to kill a row that passes everything else
    t = copy.deepcopy(CANDIDATES)
    for r in t:
        if r["key"] == "KS3D-NONEXPLICIT":
            r["blowup"] = "NOT_PROVED"
    reached["i_alone_kills"] = classify(t)[0]

    return reached


SELF_TEST_EXPECTED = {
    "all_certified": "NO_MODEL_PASSES_ALL_FOUR",
    "leray_relaxed": "SURVIVOR_IS_FLUID_ADJACENT",
    "only_explicit_left": "SURVIVOR_ONLY_VACUOUS_TARGET",
    "i_alone_kills": "SURVIVOR_ONLY_VACUOUS_TARGET",
    "actual": "SURVIVOR_NON_FLUID_NON_VACUOUS",
}


# --------------------------------------------------------------------------------------
LEDGER_ADDITION_FOR_INTEGRATION = {
    "why_not_applied": (
        "solver/viscous_novelty.py and LITERATURE_CHECK.md are integration-owned / outside "
        "this leg's declared territory (leg 245's precedent for the same situation)."
    ),
    "proposed_row": {
        "id": "arXiv:1610.09496",
        "who": "Pawel Biernat, Roland Donninger",
        "what": ("spectrally stable SELF-SIMILAR BLOWUP PROFILE of the supercritical corotational "
                 "harmonic map heat flow R^3 -> S^3, with interval arithmetic as a key ingredient"),
        "grade": "A (leg 174's definition: the certificate is ON the dissipative object)",
        "fluid_adjacent": False,
        "verdict": "PRE_EMPTS (for the non-fluid Grade-A cell) / ADJACENT (for the fluid cell)",
        "banked_by": "leg 255 (Route-P1A), query Q5",
        "effect_on_leg_174_matrix": (
            "cell (fluid=False, grade=A) gains a SECOND, INDEPENDENT occupant dated 2016 -- "
            "EIGHT YEARS BEFORE DF-CGL (2024), from an author line disjoint from Dahne-Figueras "
            "(closed by leg 242). The (fluid=True, grade=A) cell is UNCHANGED and STILL EMPTY."
        ),
    },
}


def main():
    rows = CANDIDATES
    assert_probe_is_live(rows)
    st = self_test()
    for k, want in SELF_TEST_EXPECTED.items():
        if st[k] != want:
            raise AssertionError(f"self_test {k}: got {st[k]}, expected {want}")

    verdict, answer = classify(rows)
    kc, sc = kill_counts(rows), sole_killer_counts(rows)
    survivors = [r for r in rows if not killers(r)]
    enclosed = [r for r in rows if r.get("profile_carries_dissipation")]
    surv_enclosed = [r for r in survivors if r.get("profile_carries_dissipation")]
    dominated_with_profile = [r for r in rows
                              if screen_verdicts(r)["ii_ss_profile"] == "PASS"
                              and not r.get("profile_carries_dissipation")]

    table = []
    for r in rows:
        v = screen_verdicts(r)
        table.append({
            "key": r["key"], "model": r["model"], "locator": r["locator"],
            "fluid_adjacent": r["fluid_adjacent"],
            "screens": v,
            "killed_by": killers(r),
            "survives_all_four": not killers(r),
            "evidence": {
                "i_blowup": r["blowup"], "i_locator": r["blowup_evidence"],
                "ii_profile": r["ss_profile"], "ii_locator": r["profile_locator"],
                "iii_certificate": r["certificate"], "iii_locator": r["certificate_locator"],
                "iv_nonlocal_terms": r["nonlocal_terms"],
                "iv_principal_part_ok": r["principal_part_ok"],
                "iv_reach_note": r.get("reach_note"),
            },
            "sub_flags": {
                "profile_carries_dissipation": r.get("profile_carries_dissipation"),
                "enclosed_or_dominated": ("ENCLOSED-shaped" if r.get("profile_carries_dissipation")
                                          else "DOMINATED-shaped"),
                "profile_explicit": r.get("profile_explicit"),
                "dss_lane_flag": bool(r.get("dss_lane")),
                "ban_flag": r.get("ban_flag"),
            },
            "note": r.get("note"),
        })

    gate_wording = (
        "GATE: YES. At least one model passes all four screens jointly, and the full table -- "
        "including every failure with the screen that killed it -- is banked below.\n\n"
        "THE SURVIVOR: KS3D-NONEXPLICIT -- the parabolic-elliptic Keller-Segel system in d = 3, "
        "at its NON-explicit self-similar blow-up profiles (arXiv:2503.02263, countably many in "
        "d = 3..9; Collot-Zhang arXiv:2406.11358 for their finite-Lipschitz-codimension "
        "stability). Screen (i) locator: finite-time blow-up proved, with Glogic-Schorkhuber "
        "arXiv:2209.11206 establishing nonlinear radial stability of the explicit profile in "
        "d = 3. Screen (iv) locator: Remark 40 of arXiv:2404.04054 (line 1687), whose "
        "H^2(mu) -> L^inf argument covers div(u grad c) = grad u . grad c - u^2 -- LOCAL, "
        "quadratic in u and first derivatives, at d = 3, inside Remark 40's own d in {2,3}. "
        "Its diffusion is Type-I scale-invariant, i.e. ENCLOSED-shaped, not DOMINATED-shaped.\n\n"
        "AND THE PART THAT MATTERS MORE THAN THE YES. Every survivor is NON-FLUID. Certifying "
        "KS3D-NONEXPLICIT would put a third occupant in the (fluid=False, grade=A) cell that "
        "DF-CGL and -- newly located by this leg -- Biernat-Donninger arXiv:1610.09496 (2016) "
        "already occupy. Leg 174's empty (fluid=True, grade=A) cell would STAY EMPTY. The one "
        "fluid-adjacent candidate that clears screens (i), (ii) and (iii) is KS-NS-LI-ZHOU "
        "(arXiv:2404.17228, Comm. Math. Phys. 2025) and it is killed by screen (iv) ALONE, on "
        "the Leray-projection clause: Remark 40 names (u.grad)u and gives its reason, but says "
        "nothing about the pressure's nonlocality, and boundedness of the Leray projector on "
        "L^2(mu) does not follow from the embedding Remark 40 argues from.\n\n"
        "SCREEN (iv) DOES MOST OF THE KILLING, which is the no-branch's question answered "
        "anyway because it is the useful number: it kills 13 of 21 rows and is the SOLE killer "
        "on 7, against 4 for (iii), 1 for (ii) and 0 for (i) -- blow-up models are NOT scarce. "
        "The cross-tab is the finding: 9 rows clear (i)+(ii)+(iii); 7 of those 9 are then "
        "stopped by (iv); 4 of the 7 by a nonlocal operator; and 3 of those 4 by the operator "
        "that makes the model a fluid at all -- the Leray projection (KS-NS-LI-ZHOU), the "
        "averaging (TAO-AVGNS), the Fourier restriction (MILLER-FR-HYPO). THE NONLOCALITY THAT "
        "MAKES A MODEL A FLUID IS THE SAME NONLOCALITY THAT PUTS IT OUTSIDE THE STATED REACH. "
        "That is direct input to leg 257: the binding constraint on Phase 1 is the METHOD's "
        "reach, not the supply of blow-up models, and a weaker screen-(i) tier would not fix "
        "it.\n\n"
        "SCOPE. This is a census. Construction is NOT authorized here and stays gated behind "
        "leg 257 (P1c)'s ban-lift scoping. No link of the L1->L4 chain moved -- naming a "
        "candidate pool is not certifying anything, and a certificate on a non-fluid parabolic "
        "model would not move a link either. Clay odds stay ~0.05%."
    )

    payload = {
        "leg": 255, "route": "P1A", "run_date": RUN_DATE,
        "question": ("which models satisfy ALL FOUR screens jointly: (i) dissipative blow-up, "
                     "(ii) a self-similar/DSS profile, (iii) no existing certificate, "
                     "(iv) inside Breden-Chu's stated reach"),
        "screen_iv_source": REMARK_40,
        "screen_iv_rule": REACH_RULE,
        "caution_row": BURGERS_CAUTION,
        "n_candidates": len(rows),
        "census": table,
        "survivors": [r["key"] for r in survivors],
        "kill_counts": kc,
        "sole_killer_counts": sc,
        "reach_breakdown": reach_breakdown(rows),
        "enclosed_shaped_rows": [r["key"] for r in enclosed],
        "survivors_enclosed_shaped": [r["key"] for r in surv_enclosed],
        "dominated_rows_with_a_profile": [r["key"] for r in dominated_with_profile],
        "dss_lane_rows": [r["key"] for r in rows if r.get("dss_lane")],
        "dss_lane_decision": ("NOT DECIDED HERE. The DSS lane's expensive entrance is BANNED; "
                              "whether it is in scope is leg 254's / the user's call. Rows are "
                              "flagged, per this leg's dispatch."),
        "ban_flagged_rows": {r["key"]: r["ban_flag"] for r in rows if r.get("ban_flag")},
        "verdict_code": verdict,
        "gate_answer": answer,
        "gate_answer_wording": gate_wording,
        "self_test_outcomes": st,
        "ledger_addition_for_integration": LEDGER_ADDITION_FOR_INTEGRATION,
        "realization": (
            "A bibliographic census over an ENUMERATED candidate set of "
            f"{len(rows)} models, closed as of {RUN_DATE} by: this repository's own precedent "
            "sweeps (legs 174 occupancy matrix + seven-entry catalog, 240, 242, 245, 246), "
            "solver/viscous_novelty.py::PRECEDENTS read read-only, capabilities.py grepped, and "
            "the nine verbatim web queries plus four full arXiv abstract fetches logged in "
            "writeup/novelty/leg_255.md. Screen (iii)'s negatives are ABSTRACT- and "
            "SEARCH-depth for the rows this leg added (KS3D-*, KS-NS-LI-ZHOU, MCF-NECKPINCH, "
            "VISCOUS-HJ-GRAD, GELFAND-EXP) and FULL-TEXT-depth only for the rows inherited from "
            "legs 240/242/245/246. It is NOT a statement about unpublished work, conference "
            "talks, or journal-only publications, and NOT a claim that any FAIL verdict is "
            "unliftable -- PALASEK-SHELL's screen-(ii) FAIL in particular is UNCONFIRMED, not "
            "refuted, and a full-text read is the cheapest way to move it."
        ),
        "honest_ceiling": (
            "No link of the L1->L4 chain moved. No stage claimed or closed. No ban lifted. No "
            "certificate built and no construction attempted or authorized. Clay odds stay "
            "~0.05%. Naming a Phase 1 candidate pool is not movement toward Clay."
        ),
    }

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "writeup", "data", "p2_route_p1a_v1_census.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(payload, f, indent=2, sort_keys=False)
        f.write("\n")

    print("LEG 255 -- ROUTE-P1A -- PHASE 1 TARGET CENSUS")
    print("=" * 94)
    print(f"screen (iv) is Remark 40's own wording, {REMARK_40['paper']} l.{REMARK_40['line']}:")
    print(f'  "{REMARK_40["verbatim"]}"')
    print()
    hdr = f"{'key':<20} {'fl':<3} {'i':<5} {'ii':<5} {'iii':<10} {'iv':<5} {'sub':<10} killed by"
    print(hdr)
    print("-" * 94)
    for t in table:
        v = t["screens"]
        sub = "ENCLOSED" if t["sub_flags"]["profile_carries_dissipation"] else "dominated"
        if t["sub_flags"]["profile_explicit"]:
            sub += "*"
        print(f"{t['key']:<20} {'F' if t['fluid_adjacent'] else '-':<3} "
              f"{v['i_dissipative_blowup']:<5} {v['ii_ss_profile']:<5} "
              f"{v['iii_no_certificate']:<10} {v['iv_bc_reach']:<5} {sub:<10} "
              f"{','.join(s.split('_')[0] for s in t['killed_by']) or 'SURVIVES ALL FOUR'}")
    print("-" * 94)
    print("  fl = fluid-adjacent;  sub = does the PROFILE EQUATION carry the dissipation")
    print("  * = profile is CLOSED FORM (nothing for an enclosure to do)")
    print()
    print(f"CANDIDATES {len(rows)}   SURVIVORS {len(survivors)}: {[r['key'] for r in survivors]}")
    print(f"  of which fluid-adjacent: {[r['key'] for r in survivors if r['fluid_adjacent']]}")
    print(f"  of which ENCLOSED-shaped: {[r['key'] for r in surv_enclosed]}")
    print()
    print("WHICH SCREEN DOES THE KILLING (reported regardless of branch)")
    for s in FOUR_SCREENS:
        print(f"  {s:<24} kills {kc[s]:>2} of {len(rows)}   sole killer on {sc[s]:>2}")
    print()
    rb = reach_breakdown(rows)
    print("THE CROSS-TAB THAT IS THE FINDING -- rows clearing (i), (ii) AND (iii):")
    print(f"  clear (i)+(ii)+(iii):                        {len(rb['clear_i_ii_iii']):>2}  {rb['clear_i_ii_iii']}")
    print(f"  ... and ALSO pass (iv):                      {len(rb['of_those_pass_iv']):>2}  {rb['of_those_pass_iv']}")
    print(f"  ... and are killed by (iv):                  {len(rb['of_those_fail_iv']):>2}  {rb['of_those_fail_iv']}")
    print(f"      because a NONLOCAL OPERATOR is present:  {len(rb['fail_iv_because_a_NONLOCAL_OPERATOR']):>2}  {rb['fail_iv_because_a_NONLOCAL_OPERATOR']}")
    print(f"      on the PRINCIPAL PART only:              {len(rb['fail_iv_on_the_PRINCIPAL_PART_only']):>2}  {rb['fail_iv_on_the_PRINCIPAL_PART_only']}")
    print(f"      where the nonlocality IS the fluid:      {len(rb['fail_iv_where_the_nonlocality_IS_the_fluid_structure']):>2}  {rb['fail_iv_where_the_nonlocality_IS_the_fluid_structure']}")
    print()
    print(f"DSS-lane rows (flagged, NOT decided here): {[r['key'] for r in rows if r.get('dss_lane')]}")
    print(f"ban-flagged rows: {sorted(r['key'] for r in rows if r.get('ban_flag'))}")
    print()
    print("LEDGER ADDITION PROPOSED, NOT APPLIED (out of declared territory):")
    print(f"  {LEDGER_ADDITION_FOR_INTEGRATION['proposed_row']['id']}  "
          f"{LEDGER_ADDITION_FOR_INTEGRATION['proposed_row']['who']}")
    print(f"  {LEDGER_ADDITION_FOR_INTEGRATION['proposed_row']['effect_on_leg_174_matrix']}")
    print()
    print(f"self_test outcomes reached: {sorted(set(st.values()))}")
    print(f"VERDICT CODE     {verdict}")
    print(f"GATE ANSWER      {answer}")
    print()
    print("  " + gate_wording.replace("\n", "\n  "))
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
