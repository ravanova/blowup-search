#!/usr/bin/env python
"""Leg 174 -- Route-VBS v1: "a viscous certified blow-up in any model -- the missing rung",
sharpened against what this repository has already banked.

THE GATE, verbatim from DIRECTION.md section 174:

  (a) Does `arXiv:2410.05480`'s interval-verified CGL branch work constitute a completed
      certified blow-up (not merely a certified profile/branch short of the blow-up argument
      itself), and (b) does the published literature contain any OTHER viscous
      fluid/vortex-dynamics-adjacent model (beyond Chen's gamma=2 gCLM) with an existing
      analytic blow-up proof that has never been computer-certified?

    yes on (a) -> The "missing rung" already has an occupant, just not in a fluid-adjacent
           model -- report this precisely; it reframes but does not retract the user's point
           (fluid dynamics specifically still lacks one). ESCALATE the reframing to the user.
    no on (a) -> CGL's branch work falls short of a completed certified blow-up in a specific,
           named way. Report exactly what is missing; this confirms the rung is genuinely
           empty, strengthening leg 125's priority.
    For (b): report every candidate found, with its own analytic proof's citation, regardless
           of (a)'s answer -- this is the fallback catalog either way. Bank it; escalate
           nothing on its own (a catalog is not a claim).

WHAT THIS FILE IS.  A literature ledger with the gate computed FROM the ledger rather than
remembered, in the shape leg 48's `solver/viscous_novelty.py::PRECEDENTS` and leg 113's
`experiments/p2_route_ms_v1_lit.py` established.  It runs no solve, builds no certificate and
touches no solver module.  Every quote carries a locator; every classification is a predicate
over declared fields, so a reader can disagree with a field and recompute the gate.

THE DISTINCTION THIS LEG EXISTS TO MAKE.  "Certified blow-up" silently names two different
things, and the whole question turns on which one is meant:

  GRADE A -- the certificate is ON the dissipative object.  The interval arithmetic encloses a
             solution of an equation that itself carries the dissipative term.
  GRADE B -- the THEOREM is about the dissipative PDE, and computer assistance is an essential,
             non-removable step of its proof -- but the enclosed object may be an inviscid
             auxiliary (e.g. an inviscid self-similar profile that an analytic stability
             argument then transfers to the viscous equation).

Grade A implies Grade B.  Leg 113's ledger tracks Grade A only (its `clause_2_inviscid` is
defined on "the certified equation"), which is correct for leg 113's own gate and is exactly
the labelling that makes this rung look empty.

Usage:  .venv/bin/python experiments/p2_route_vbs_v1_scoping.py
Writes: writeup/data/p2_route_vbs_v1_scoping.json
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_vbs_v1_scoping.json")

GATE = ("(a) Does arXiv:2410.05480's interval-verified CGL branch work constitute a completed "
        "certified blow-up (not merely a certified profile/branch short of the blow-up "
        "argument itself), and (b) does the published literature contain any OTHER viscous "
        "fluid/vortex-dynamics-adjacent model (beyond Chen's gamma=2 gCLM) with an existing "
        "analytic blow-up proof that has never been computer-certified?")

# ---------------------------------------------------------------------------
# Field definitions.  Stated so a reader can dispute a field rather than a verdict.
# ---------------------------------------------------------------------------
FIELDS = {
    "pde_dissipative": "the PDE the theorem's CONCLUSION is about carries a dissipative "
                       "term with a positive coefficient (a viscosity, a +eps*Laplacian, a "
                       "fractional -(-Delta)^alpha). Judged on the conclusion, not on any "
                       "auxiliary equation used in the proof.",
    "fluid_adjacent": "the equation is a fluid or vortex-dynamics model: it has a transport "
                      "nonlinearity u.grad(u) or a vorticity/velocity relation. Semilinear "
                      "scalar equations with no transport structure are NOT fluid-adjacent, "
                      "however physically motivated.",
    "concludes_pde_singularity": "the theorem's conclusion is a finite-time singularity of a "
                                 "SOLUTION of the PDE, not merely existence of a profile or a "
                                 "branch of profiles solving an ODE.",
    "certified_object_dissipative": "GRADE A. The object enclosed in interval arithmetic is a "
                                    "solution of an equation that itself carries the "
                                    "dissipative term.",
    "computer_assistance_essential": "GRADE B. A computer-assisted / interval-arithmetic step "
                                     "is a non-removable ingredient of the proof as published.",
    "finite_energy_data": "the singular solution arises from data of finite energy/mass in the "
                          "natural space of the Cauchy problem for that PDE.",
    "stability_proved": "the paper proves the constructed singularity is dynamically stable "
                        "(or stable modulo finitely many directions).",
}

# ---------------------------------------------------------------------------
# THE LEDGER.  Every row located; every quote transcribed from the full text.
# ---------------------------------------------------------------------------
LEDGER = [
    # ---- the gate's clause (a) subject, and its own within-paper control ----
    {
        "key": "DF-CGL",
        "cite": "Dahne, Figueras -- Self-Similar Singular Solutions to the Nonlinear "
                "Schroedinger and the Complex Ginzburg-Landau Equations",
        "url": "https://arxiv.org/abs/2410.05480",
        "version": "v2, 20 Dec 2024",
        "equation": "Complex Ginzburg-Landau, i u_t + (1 - i*eps) Laplacian(u) + "
                    "(1 + i*delta)|u|^{2 sigma} u = 0 on R^d x (0,T), with eps > 0",
        "role": "THE GATE'S CLAUSE (a) SUBJECT",
        "pde_dissipative": True,
        "fluid_adjacent": False,
        "concludes_pde_singularity": True,
        "certified_object_dissipative": True,
        "computer_assistance_essential": True,
        "finite_energy_data": False,
        "stability_proved": False,
        "locator": "Theorem 4.1 (Case I, d=1, sigma=2.3); same form at Theorem 4.4 (Case II)",
        "quote": "In Case I (d = 1, sigma = 2.3) there exists (at least) 8 continuous curves, "
                 "{(eps_j(s), mu_j(s), kappa_j(s))}, such that for each s in [0,1] and each j, "
                 "the CGL equation with eps = eps_j(s) has a self-similar singular solution of "
                 "the form u(x,t) = ... Q(...)",
        "second_locator": "Theorem 1.2 (the eps = 0 NLS end of the same branches)",
        "second_quote": "There exists 8 nontrivial radial self-similar singular solutions u of "
                        "the form (2) with Q in C^infinity([0,infinity)) intersect "
                        "L^3([0,infinity)) satisfying Equation (1) for d = 1 and sigma = 2.3 "
                        "(and eps = delta = 0).",
        "third_locator": "Remark 1.6",
        "third_quote": "Proving these stability results would be of great interest.",
        "why_certified_object_dissipative": "the certified ODE (3)/(4)/(5) carries the factor "
                                            "(1 - i*eps) throughout, and Theorem 4.1's branches "
                                            "satisfy eps'_j(0) > 0, i.e. eps is strictly "
                                            "positive along the branch. The dissipation is "
                                            "INSIDE the enclosed object.",
        "why_not_fluid": "CGL is a semilinear scalar equation for a complex field. No transport "
                         "nonlinearity, no incompressibility constraint, no Biot-Savart law.",
        "why_not_finite_energy": "Q(xi) ~ xi^{-1/sigma - i*omega/kappa}, so the paper itself "
                                 "records Q in L^3 and NOT L^2 in Case I. The singular solution "
                                 "has infinite mass; it is an exact singular solution, not a "
                                 "blow-up from localised Cauchy data.",
        "repo_rederivation": "leg 48 re-derived their (mu, kappa) to 1.8e-07, their Fig 1a "
                             "branch to max 3.0e-06 / rms 1.9e-06, and their fold to 3.8e-07 "
                             "in eps* (LITERATURE_CHECK.md eighth pass).",
    },
    {
        # LESSON 90: the control that CAN report the other answer, and it is inside the SAME
        # paper, by the same authors, with the same method -- so nothing but the dissipation
        # parameter differs.  If Grade A were a tautology of the code, this row would match.
        "key": "DF-NLS",
        "cite": "Dahne, Figueras -- same paper, the eps = 0 theorems",
        "url": "https://arxiv.org/abs/2410.05480",
        "version": "v2, 20 Dec 2024",
        "equation": "focusing NLS, i u_t + Laplacian(u) + |u|^{2 sigma} u = 0 (eps = delta = 0)",
        "role": "LESSON-90 CONTROL -- same paper, same method, dissipation switched OFF",
        "pde_dissipative": False,
        "fluid_adjacent": False,
        "concludes_pde_singularity": True,
        "certified_object_dissipative": False,
        "computer_assistance_essential": True,
        "finite_energy_data": False,
        "stability_proved": False,
        "locator": "Theorem 3.2",
        "quote": "The nonlinear Schroedinger equation ... supports radial self-similar singular "
                 "solutions of the form u(x,t) = ...",
        "why_control": "This row differs from DF-CGL in exactly one input, eps, and it lands in "
                       "a different cell of the occupancy matrix. The Grade-A predicate "
                       "therefore varies over the ledger and is not a tautology of the code.",
    },

    # ---- the row the gate did not anticipate ----
    {
        "key": "BCG-NS",
        "cite": "Buckmaster, Cao-Labora, Gomez-Serrano -- Smooth imploding solutions for 3D "
                "compressible fluids",
        "url": "https://arxiv.org/abs/2208.09445",
        "journal_ref": "Forum of Mathematics, Pi 13 (2025) e6; doi 10.1017/fmp.2024.12",
        "equation": "3D isentropic compressible NAVIER-STOKES, d_t(rho u) + div(rho u x u) + "
                    "grad p(rho) - mu_1 Laplacian(u) - (mu_1 + mu_2) grad div u = 0, with "
                    "mu_1 > 0 and 2 mu_1 + mu_2 > 0",
        "role": "THE OCCUPANT OF THE RUNG, IN A GENUINE VISCOUS FLUID MODEL",
        "pde_dissipative": True,
        "fluid_adjacent": True,
        "concludes_pde_singularity": True,
        "certified_object_dissipative": False,
        "computer_assistance_essential": True,
        "finite_energy_data": True,
        "stability_proved": True,
        "locator": "Theorem 1.3 (gamma = 7/5), clauses 2 and 3",
        "quote": "The initial data (u_0, rho_0) is smooth and has finite energy ... At time T, "
                 "the solution (u, rho) becomes singular at the origin: for any eps > 0, "
                 "limsup_{t->T} |u(R,t)| = infinity and lim_{t->T} rho(0,t) = infinity.",
        "second_locator": "section 1.3 (the role of the computer)",
        "second_quote": "Furthermore, we employ a computer-assisted proof to compute the first "
                        "10000 coefficient pairs (W_j, Z_j) at r = r*, with rigorous error "
                        "bounds. ... In order to perform rigorous, error-free calculations, "
                        "interval arithmetic will be used as part of the proof whenever needed. "
                        "... This part of the calculation takes about 14 hours on a single CPU.",
        "third_locator": "section 7, opening paragraph",
        "third_quote": "The stability for the Euler equation will follow in general, while in "
                       "the Navier-Stokes case we need to restrict the parameter r to a regime "
                       "where the self-similar profile dominates the dissipation.",
        "why_not_certified_object_dissipative": "the enclosed object is the self-similar profile "
                                                "solving system (1.5), which is the ODE "
                                                "reduction of the INVISCID compressible Euler "
                                                "system (1.3). Theorem 1.3 reaches Navier-Stokes "
                                                "from that profile by the analytic stability "
                                                "argument of sections 7-8. Grade B, not A.",
        "why_computer_assistance_essential": "gamma = 7/5 is precisely the case that needs it: "
                                             "the table of contents carries 'Appendix B "
                                             "Implementation details of the computer-assisted "
                                             "part', and section 5 (the gamma = 7/5 analysis "
                                             "Theorem 1.2 rests on) proves its inequalities via "
                                             "Lemmas A.27/A.28, both computer-assisted. "
                                             "Theorem 1.3 consumes Theorem 1.2's profile.",
        "structural_caveat": "the viscous term is not overcome at its own scaling: it is "
                             "dominated by choosing the self-similar exponent r in a regime "
                             "where the dissipation decays exponentially in self-similar time "
                             "(section 7, quoted above). Contrast DF-CGL, where eps enters at "
                             "exactly the same scaling order as the dispersive term.",
        "repo_status": "PRESENT in this repository, in leg 113's ledger "
                       "experiments/p2_route_ms_v1_lit.py as key BCG-IMP, correctly labelled "
                       "clause_2_inviscid=True on leg 113's own definition ('the CERTIFIED "
                       "equation carries NO dissipative term'). ABSENT from "
                       "solver/viscous_novelty.py::PRECEDENTS and from LITERATURE_CHECK.md.",
    },

    # ---- clause (b): the fallback catalog. Viscous, fluid-adjacent, analytic, uncertified. ----
    {
        "key": "MRRS-NS",
        "cite": "Merle, Raphael, Rodnianski, Szeftel -- On the implosion of a compressible "
                "fluid II: singularity formation (and the Navier-Stokes companion)",
        "url": "https://arxiv.org/abs/1912.11009",
        "journal_ref": "Ann. of Math. 196 (2022) 567-778 and 779-889; Bocher Prize 2023",
        "equation": "3D isentropic compressible Navier-Stokes",
        "role": "CLAUSE (b) CATALOG -- and the analytic predecessor BCG certified",
        "pde_dissipative": True,
        "fluid_adjacent": True,
        "concludes_pde_singularity": True,
        "certified_object_dissipative": False,
        "computer_assistance_essential": False,
        "finite_energy_data": True,
        "stability_proved": True,
        "locator": "described in BCG arXiv:2208.09445 section 1.1.2",
        "quote": "The condition on gamma for which the result holds is described in terms of "
                 "the non-vanishing of an analytic function. This condition is not proven for "
                 "any specific gamma; however it may be checked numerically.",
        "why_catalog": "the strongest clause-(b) entry there is: an analytic finite-time "
                       "singularity theorem for a genuine viscous fluid equation whose "
                       "hypothesis is non-constructive at every INDIVIDUAL gamma. That is "
                       "exactly the shape of statement a certificate discharges -- and BCG "
                       "then discharged it at gamma = 7/5. Retained in the catalog as the "
                       "template of what certification buys.",
        "caveat": "MRRS additionally requires the initial density to decay at infinity; BCG "
                  "removes that (density constant at infinity) to rule out vacuum artefacts.",
    },
    {
        "key": "KVW-PRANDTL",
        "cite": "Kukavica, Vicol, Wang -- The van Dommelen and Shen singularity in the Prandtl "
                "equations",
        "url": "https://arxiv.org/abs/1512.07358",
        "journal_ref": "Adv. Math. 307 (2017) 288-311",
        "equation": "Prandtl boundary layer equations (viscous, derived from Navier-Stokes at "
                    "high Reynolds number)",
        "role": "CLAUSE (b) CATALOG",
        "pde_dissipative": True,
        "fluid_adjacent": True,
        "concludes_pde_singularity": True,
        "certified_object_dissipative": False,
        "computer_assistance_essential": False,
        "finite_energy_data": True,
        "stability_proved": False,
        "locator": "abstract / main theorem",
        "quote": "rigorously establishing the finite time blowup of the boundary layer "
                 "thickness, proving the 1980 van Dommelen and Shen numerical conjecture",
        "why_catalog": "a viscous equation of genuine fluid origin with an analytic finite-time "
                       "singularity proof and no computer-assisted certificate in the searched "
                       "literature. The singularity is of displacement-thickness type, not "
                       "self-similar-profile type, so a profile certificate is not the "
                       "obviously matching tool -- recorded as a caveat, not hidden.",
    },
    {
        "key": "KNS-FRACBURGERS",
        "cite": "Kiselev, Nazarov, Shterenberg -- Blow up and regularity for fractal Burgers "
                "equation",
        "url": "https://arxiv.org/abs/0804.3549",
        "journal_ref": "Dyn. Partial Differ. Equ. 5 (2008) 211-240",
        "equation": "u_t = u u_x - (-Laplacian)^alpha u, blow-up proved for alpha < 1/2",
        "role": "CLAUSE (b) CATALOG",
        "pde_dissipative": True,
        "fluid_adjacent": True,
        "concludes_pde_singularity": True,
        "certified_object_dissipative": False,
        "computer_assistance_essential": False,
        "finite_energy_data": True,
        "stability_proved": False,
        "locator": "abstract",
        "quote": "We prove existence of finite time blow up for the power of Laplacian alpha < "
                 "1/2, and global existence as well as analyticity of solution for alpha >= 1/2",
        "why_catalog": "the cleanest viscous-versus-blow-up dichotomy in the fluid-adjacent 1D "
                       "literature, with a sharp threshold, entirely analytic. Burgers is the "
                       "transport prototype; the authors state the results extend to SQG.",
        "caveat": "hypodissipative (alpha < 1/2): the dissipation is weaker than the transport "
                  "at the blow-up scaling, which is the opposite of the hard case.",
    },
    {
        "key": "TAO-AVGNS",
        "cite": "Tao -- Finite time blowup for an averaged three-dimensional Navier-Stokes "
                "equation",
        "url": "https://arxiv.org/abs/1402.0290",
        "journal_ref": "J. Amer. Math. Soc. 29 (2016) 601-674",
        "equation": "averaged 3D Navier-Stokes: full viscosity, exact energy identity, bilinear "
                    "term replaced by an averaged version of the Euler bilinear operator",
        "role": "CLAUSE (b) CATALOG",
        "pde_dissipative": True,
        "fluid_adjacent": True,
        "concludes_pde_singularity": True,
        "certified_object_dissipative": False,
        "computer_assistance_essential": False,
        "finite_energy_data": True,
        "stability_proved": False,
        "locator": "abstract",
        "quote": "we construct an example of a smooth solution to such an averaged Navier-Stokes "
                 "equation which blows up in finite time",
        "why_catalog": "keeps FULL 3D viscosity and the exact energy identity -- the only "
                       "clause-(b) entry that does not weaken the dissipation -- and weakens "
                       "the nonlinearity instead. Analytic; no certificate.",
        "caveat": "the averaged bilinear operator is engineered for the blow-up, so a "
                  "certificate of it would certify a constructed counterexample rather than a "
                  "physically-derived model. Its purpose is the supercriticality barrier.",
    },
    {
        "key": "CHEN-GCLM-DISS",
        "cite": "J. Chen -- Singularity formation and global well-posedness for the generalized "
                "Constantin-Lax-Majda equation with dissipation",
        "url": "https://arxiv.org/abs/1908.09385",
        "journal_ref": "Nonlinearity 33 (2020) 2502",
        "equation": "gCLM with dissipation nu * Lambda^gamma",
        "role": "CLAUSE (b) CATALOG -- and leg 125's retired candidate",
        "pde_dissipative": True,
        "fluid_adjacent": True,
        "concludes_pde_singularity": True,
        "certified_object_dissipative": False,
        "computer_assistance_essential": False,
        "finite_energy_data": True,
        "stability_proved": False,
        "locator": "section 2.6, final line of the proof of Theorem 1.1 (read at full text by "
                   "leg 125)",
        "quote": "Since nu(t) converges to 0, such profile is the same as the inviscid profile "
                 "associated with a.",
        "why_catalog": "listed for completeness and because DIRECTION.md's clause (b) says "
                       "'beyond Chen's gamma=2 gCLM'. It is retained with leg 125's finding "
                       "attached, not silently dropped.",
        "caveat": "LEG 125 RETIRED THIS ON LITERATURE GROUNDS. The paper contains no gamma = 2 "
                  "dissipative self-similar profile: the object Theorem 1.1's solution "
                  "converges to is the explicit INVISCID a = 1/2 pole-dynamics solution, "
                  "eq (2.2), a closed-form rational function. Certifying it would certify an "
                  "exact solution already covered analytically for the whole smooth branch "
                  "a <= 1 (arXiv:2305.05895 / 2308.01528).",
    },
    {
        "key": "MILLER-HYPO",
        "cite": "Miller -- Finite-time blowup for the Fourier-restricted Euler and "
                "hypodissipative Navier-Stokes model equations",
        "url": "https://arxiv.org/abs/2307.03434",
        "equation": "Fourier-restricted hypodissipative Navier-Stokes model",
        "role": "CLAUSE (b) CATALOG",
        "pde_dissipative": True,
        "fluid_adjacent": True,
        "concludes_pde_singularity": True,
        "certified_object_dissipative": False,
        "computer_assistance_essential": False,
        "finite_energy_data": True,
        "stability_proved": False,
        "locator": "title / abstract",
        "quote": "Finite-time blowup for the Fourier-restricted Euler and hypodissipative "
                 "Navier-Stokes model equations",
        "why_catalog": "a model that keeps the Navier-Stokes constraint structure (divergence "
                       "free, energy identity) and weakens only the dissipation exponent. "
                       "Analytic; no certificate found.",
        "caveat": "hypodissipative, and the nonlinearity is Fourier-restricted.",
    },
    {
        "key": "PALASEK-SHELL",
        "cite": "Palasek -- Finite-time blow-up in an elementary model of the 3D Navier-Stokes "
                "equations",
        "url": "https://arxiv.org/abs/2605.13827",
        "equation": "shell model of 3D Navier-Stokes with viscosity, smooth data and forcing",
        "role": "CLAUSE (b) CATALOG",
        "pde_dissipative": True,
        "fluid_adjacent": True,
        "concludes_pde_singularity": True,
        "certified_object_dissipative": False,
        "computer_assistance_essential": False,
        "finite_energy_data": True,
        "stability_proved": False,
        "locator": "title / abstract",
        "quote": "Finite-time blow-up in an elementary model of the 3D Navier-Stokes equations",
        "why_catalog": "the most recent entry found, and the one whose finite-dimensional "
                       "(shell/ODE) structure makes it the most tractable clause-(b) candidate "
                       "for an interval-arithmetic certificate -- a shell model IS a countable "
                       "ODE system, which is the setting rigorous numerics is strongest in.",
        "caveat": "a shell model discards the geometry of the nonlinearity entirely; it is "
                  "fluid-adjacent by scaling and energy structure, not by transport.",
    },

    # ---- inviscid controls, so the 'fluid + viscous' cell is not empty by construction ----
    {
        "key": "CHENHOU-BOUSS",
        "cite": "Chen, Hou -- 2D Boussinesq / 3D Euler with boundary: certified self-similar "
                "blow-up",
        "url": "https://arxiv.org/abs/2210.07191",
        "equation": "2D Boussinesq / 3D Euler with boundary -- INVISCID",
        "role": "CONTROL -- fluid + certified + inviscid, the cell that IS occupied",
        "pde_dissipative": False,
        "fluid_adjacent": True,
        "concludes_pde_singularity": True,
        "certified_object_dissipative": False,
        "computer_assistance_essential": True,
        "finite_energy_data": True,
        "stability_proved": True,
        "locator": "already in solver/viscous_novelty.py::PRECEDENTS as an EXCLUSION",
        "quote": "certified blow-up, INVISCID -- the certificate has no dissipation dial",
        "why_control": "shows the occupancy matrix's fluid row is not empty for reasons "
                       "unrelated to dissipation, so an empty viscous+fluid+GradeA cell is a "
                       "statement about dissipation and not about fluids.",
    },
]


# ---------------------------------------------------------------------------
# The gate, computed from the ledger.
# ---------------------------------------------------------------------------
def row(key):
    for r in LEDGER:
        if r["key"] == key:
            return r
    raise KeyError(key)


def grade(r):
    """Grade A / B / None for a row, from its declared fields."""
    if not (r["concludes_pde_singularity"] and r["pde_dissipative"]):
        return None
    if r["certified_object_dissipative"]:
        return "A"
    if r["computer_assistance_essential"]:
        return "B"
    return None


def gate_a():
    """(a) Is DF's CGL work a COMPLETED certified blow-up, or short of the argument?"""
    r = row("DF-CGL")
    complete = (r["concludes_pde_singularity"] and r["pde_dissipative"]
                and r["certified_object_dissipative"] and r["computer_assistance_essential"])
    return ("YES" if complete else "NO"), {
        "grade": grade(r),
        "conclusion_is_about_the_PDE": r["concludes_pde_singularity"],
        "dissipation_is_inside_the_certified_object": r["certified_object_dissipative"],
        "fluid_adjacent": r["fluid_adjacent"],
        "qualifications_that_do_NOT_make_it_incomplete": [
            "infinite mass: Q in L^3 and not L^2 (Case I), so it is an exact singular "
            "solution, not a blow-up from localised finite-mass Cauchy data",
            "stability unproved: Remark 1.6 leaves it open",
            "not fluid-adjacent: semilinear scalar, no transport nonlinearity",
        ],
        "why_not_short_of_the_argument": "the step from certified profile to singular PDE "
                                         "solution is exact substitution of Ansatz (2) into "
                                         "Equation (1). There is no further analytic argument "
                                         "that could be missing, and the paper states the "
                                         "conclusion in that form (Theorems 4.1, 4.4).",
    }


def gate_b():
    """(b) The catalog: viscous, fluid-adjacent, analytic proof, never computer-certified."""
    cat = [r for r in LEDGER
           if r["pde_dissipative"] and r["fluid_adjacent"]
           and r["concludes_pde_singularity"]
           and not r["computer_assistance_essential"]]
    return ("YES" if cat else "NO"), [r["key"] for r in cat]


def occupancy():
    """The 2x2(x2) matrix the whole question turns on."""
    cells = {}
    for fluid in (True, False):
        for g in ("A", "B"):
            keys = [r["key"] for r in LEDGER
                    if r["fluid_adjacent"] is fluid and grade(r) == g]
            cells["fluid=%s,grade=%s" % (fluid, g)] = keys
    return cells


# ---------------------------------------------------------------------------
# Read-only audit of this repository's own ledgers.  Never edits them.
# ---------------------------------------------------------------------------
def repo_audit():
    vn = os.path.join(ROOT, "solver", "viscous_novelty.py")
    lc = os.path.join(ROOT, "LITERATURE_CHECK.md")
    ms = os.path.join(ROOT, "experiments", "p2_route_ms_v1_lit.py")
    vn_src = open(vn).read()
    lc_src = open(lc).read()
    ms_src = open(ms).read()
    # the SEARCH_LOG queries, extracted rather than remembered
    block = vn_src.split("SEARCH_LOG = [", 1)[1].split("]", 1)[0]
    queries = re.findall(r"\('([^']*)'", block)
    # what would have had to appear in a query for it to return BCG: the equation
    # (compressible) or the phenomenon (implosion/imploding). "Ginzburg-Landau" is
    # deliberately NOT in this pattern -- those queries reach DF, not BCG.
    reach = [q for q in queries if re.search(r"compressib|implo", q, re.I)]
    return {
        "arXiv_2208.09445_in_viscous_novelty_PRECEDENTS": "2208.09445" in vn_src,
        "arXiv_2208.09445_in_LITERATURE_CHECK": "2208.09445" in lc_src,
        "arXiv_2208.09445_in_leg113_route_ms_ledger": "2208.09445" in ms_src,
        "leg113_labels_it_inviscid": '"clause_2_inviscid": True' in
                                     ms_src.split('"key": "BCG-IMP"', 1)[1].split("},", 1)[0],
        "viscous_novelty_SEARCH_LOG_n_queries": len(queries),
        "viscous_novelty_SEARCH_LOG_queries_that_could_reach_BCG": reach,
        "reading": "stage V's novelty gate could not have found arXiv:2208.09445: none of its "
                   "queries mentions compressible or implosion. Leg 113 DID find it, and "
                   "labelled it inviscid -- correctly, on leg 113's own definition, which is "
                   "about the CERTIFIED equation and not about the equation the theorem "
                   "concludes on.",
    }


def controls():
    """Lesson 90: a control that cannot come out differently is not a control."""
    a, b = row("DF-CGL"), row("DF-NLS")
    differing = [k for k in FIELDS if a.get(k) != b.get(k)]
    return {
        "within_paper_control": {
            "rows": ["DF-CGL", "DF-NLS"],
            "same_paper_same_method": True,
            "fields_that_differ": differing,
            "grades": {"DF-CGL": grade(a), "DF-NLS": grade(b)},
            "passes": grade(a) != grade(b) and differing == ["pde_dissipative",
                                                             "certified_object_dissipative"],
            "why_this_is_a_real_control": "two rows of the SAME paper, differing only in eps, "
                                          "land in different cells. The Grade predicate "
                                          "therefore reads off the ledger and is not a "
                                          "tautology of the code.",
        },
        "grade_predicate_varies": sorted({str(grade(r)) for r in LEDGER}),
        "fluid_row_not_empty_for_unrelated_reasons": occupancy()["fluid=True,grade=B"],
    }


def main():
    ans_a, detail_a = gate_a()
    ans_b, cat_b = gate_b()
    occ = occupancy()
    empty_cell = occ["fluid=True,grade=A"]
    ctrl = controls()

    result = {
        "leg": 174,
        "route": "ROUTE-VBS",
        "title": "A viscous certified blow-up in any model -- where the rung actually is",
        "gate": GATE,
        "field_definitions": FIELDS,
        "grade_definitions": {
            "A": "the interval arithmetic encloses a solution of an equation that itself "
                 "carries the dissipative term",
            "B": "the THEOREM is about the dissipative PDE and computer assistance is an "
                 "essential step of its proof, but the enclosed object may be inviscid",
        },
        "gate_a_answer": ans_a,
        "gate_a_detail": detail_a,
        "gate_b_answer": ans_b,
        "gate_b_catalog": cat_b,
        "occupancy_matrix": occ,
        "the_empty_cell": {
            "cell": "fluid_adjacent=True, grade=A",
            "occupants": empty_cell,
            "meaning": "no published work applies interval arithmetic to a DISSIPATIVE fluid "
                       "equation's own self-similar object. This is the rung that is genuinely "
                       "empty, and it is narrower than 'a viscous certified blow-up'.",
        },
        "headline": (
            "The rung is occupied twice over, but never in the cell the question meant. "
            "arXiv:2410.05480 is a Grade-A certified finite-time singularity of a dissipative "
            "PDE (CGL, eps > 0) -- complete as an argument, but infinite-mass, stability open, "
            "and not a fluid. arXiv:2208.09445 Thm 1.3 is a Grade-B certified finite-time "
            "singularity of a genuine viscous fluid equation (3D compressible Navier-Stokes, "
            "finite energy, density constant at infinity) -- but the object its interval "
            "arithmetic encloses is the INVISCID Euler profile. The empty cell is "
            "fluid + Grade A, and that is what leg 125 was aiming at."),
        "repo_ledger_audit": repo_audit(),
        "controls": ctrl,
        "ledger": LEDGER,
        "leg_125_context": {
            "gate_answered": "NO",
            "reason": "retired on LITERATURE grounds, not numerical ones: Chen arXiv:1908.09385 "
                      "contains no gamma = 2 dissipative self-similar profile at all. The "
                      "object its Theorem 1.1 converges to is the explicit inviscid a = 1/2 "
                      "pole-dynamics solution (eq 2.2), already covered analytically.",
            "why_the_rung_stayed_empty_after_125": "leg 125 was aiming at exactly the empty "
                                                   "cell (fluid + Grade A) and the candidate "
                                                   "dissolved: there was no dissipative object "
                                                   "to enclose. The cell is empty for want of a "
                                                   "TARGET, not for want of a method -- "
                                                   "arXiv:2404.04054 already does Grade-A "
                                                   "Newton-Kantorovich on viscous Burgers, "
                                                   "which is a non-fluid parabolic model.",
        },
        "honest_ceiling": {
            "moves_a_link_of_L1_to_L4": False,
            "clay_odds_unchanged": "~0.05%",
            "escalation": "gate (a) answered YES, so DIRECTION.md's pre-committed yes-branch "
                          "fires: ESCALATE the reframing. The reframing is larger than the "
                          "branch anticipated -- the occupant is not only CGL but compressible "
                          "Navier-Stokes -- and it is a catalog/scoping finding, not a claim of "
                          "progress on this repository's own object.",
        },
    }

    with open(OUT, "w") as f:
        json.dump(result, f, indent=2, sort_keys=False)

    print("Leg 174 -- Route-VBS scoping")
    print("  GATE (a):", ans_a, "-- grade", detail_a["grade"],
          "| fluid_adjacent:", detail_a["fluid_adjacent"])
    print("  GATE (b):", ans_b, "--", len(cat_b), "catalog entries:", ", ".join(cat_b))
    print()
    for cell, keys in occ.items():
        print("  %-22s %s" % (cell, ", ".join(keys) if keys else "-- EMPTY --"))
    print()
    print("  control (same paper, eps on/off) passes:",
          ctrl["within_paper_control"]["passes"],
          "| grades", ctrl["within_paper_control"]["grades"])
    aud = result["repo_ledger_audit"]
    print("  2208.09445 in viscous_novelty PRECEDENTS:",
          aud["arXiv_2208.09445_in_viscous_novelty_PRECEDENTS"],
          "| in LITERATURE_CHECK:", aud["arXiv_2208.09445_in_LITERATURE_CHECK"],
          "| in leg 113 ledger:", aud["arXiv_2208.09445_in_leg113_route_ms_ledger"])
    print("  stage V SEARCH_LOG queries that could have reached it:",
          aud["viscous_novelty_SEARCH_LOG_queries_that_could_reach_BCG"] or "NONE")
    print()
    print("  wrote", os.path.relpath(OUT, ROOT))

    assert ctrl["within_paper_control"]["passes"], "lesson-90 control failed"
    assert not empty_cell, "the empty cell is not empty -- re-read the ledger"
    assert ans_a == "YES" and ans_b == "YES"


if __name__ == "__main__":
    main()
