"""WHAT IS ALREADY BUILT -- the capability index, machine-readable and enforced.

--------------------------------------------------------------------------
WHY THIS FILE EXISTS
--------------------------------------------------------------------------
Route-M (leg 45) came within about ten minutes of rebuilding a Scenario-2 integrator
that had been sitting in `solver/hl_rescaled.py`, validated to 4.4e-16, since
2026-07-26.  It was found by grepping for an arXiv number, not by looking it up.

That is the same failure as the leg's own headline.  The certification port spent twenty
legs aimed at an object Chen-Hou had already certified, while the solver for an
UNCERTIFIED object sat unused in the same repository.  In both cases the missing thing
was not effort or insight -- it was **an index of what already exists**.

`plan_of_record.py` answers "what is next".  `PHASE2_P2_NOTES.md` answers "what
happened".  Neither answers "what do we HAVE", and after forty-five legs and thirty-five
solver modules that question can no longer be held in a session's head.  This file
answers it, and `test_capabilities.py` fails if it drifts from the tree.

Banked lesson (68) -- a check that is not executable decays at the rate of memory --
applied to the inventory rather than to the literature.

--------------------------------------------------------------------------
HOW TO USE IT
--------------------------------------------------------------------------
    .venv/bin/python capabilities.py             # everything, grouped by object
    .venv/bin/python capabilities.py hou-luo     # substring filter over every field

**Before building anything, grep this file for the object first.**

Each entry records the four things that decide whether existing code can be reused:
  `object`     what mathematical object it holds -- the key you will actually search on
  `holds`      what it computes, in one line
  `validated`  the strongest KNOWN-ANSWER gate it passes, with the magnitude, or
               "no known-answer gate" said plainly.  This is the field that stops a
               module being trusted further than it was tested.
  `test`       the file that re-checks the above
"""

import sys

# `object` is the mathematical object, not the file -- entries are searched on it.
CAPABILITIES = [
    # -- 1D Hou-Luo (the model that carries the top-ranked uncertified target) ------
    {"module": "solver/hl_rescaled.py", "object": "1D Hou-Luo model, dynamic rescaling",
     "holds": ("RescaledHL (velocity from H(Omega), pinned U(0)=0), RescaledHLDynamic "
               "(degenerate gauge (3.2)), RescaledHLScenario2 (CHL (4.1)/(4.2): the "
               "THREE-constant origin-pinned gauge with the translation DOF c_r)"),
     "validated": ("the (4.2) gauge nulls d_tau{Omega(0),Omega_X(0),V(0)} to 4.4e-16; "
                   "the exact Thm-2.3 singular anchor is a steady state on its support; "
                   "the Scenario-2 contraction ratio reproduces CHL's -2.5114 to ~1%"),
     "test": "test_hl_rescaled.py"},
    {"module": "solver/line_hilbert.py", "object": "Hilbert transform on the whole line",
     "holds": ("spline-analytic H on a NON-uniform grid, dense operator, and the cached "
               "slope operator `slope_matrix` (Route-M: 10x on the Scenario-2 step)"),
     "validated": ("the CLM known-answer pair to rel 1.6e-4; the cached slope operator "
                   "matches the Thomas sweeps to 2.7e-13"),
     "test": "test_line_hilbert.py"},

    # -- gCLM family ---------------------------------------------------------------
    {"module": "solver/gclm_family.py", "object": "gCLM a-family, rescaled steady residual",
     "holds": "R = (c_omega + H Omega) Omega - c_l X Omega_X - a U Omega_X on a sinh grid",
     "validated": "the exact a=0 profile -4X/(1+4X^2) nulls R to RMS 2.2e-7",
     "test": "test_gclm_family.py"},
    {"module": "solver/gclm_rescaled.py", "object": "1D CLM (a=0), dynamic rescaling",
     "holds": "rescaled flow, fixed point, upwind transport in the stretched coordinate",
     "validated": ("relaxes to the exact CLM self-similar fixed point -4X/(1+4X^2)"),
     "test": "test_gclm_rescaled.py"},
    {"module": "solver/rescaled_spectrum.py", "object": "gCLM rescaled linearization, spectrum",
     "holds": "dense spectrum of the linearization about the rescaled fixed point",
     "validated": ("point spectrum {0,1} at a=0, which XU Theorem 2 later proved -- but "
                   "in the LOOSE realization: our grid imposes NO origin condition (70)"),
     "test": "test_rescaled_spectrum.py"},
    {"module": "solver/fractional_gclm.py", "object": "gCLM with fractional dissipation",
     "holds": "Lambda^s dissipation, the critical exponent s_c, relevance thresholds",
     "validated": "s_c = alpha/2 against XU eq (6.3) row by row (PRE-EMPTED, Route-J)",
     "test": "test_fractional_gclm.py"},
    {"module": "solver/critical_dissipation.py", "object": "gCLM at exactly critical dissipation",
     "holds": "the marginal case and the invariant alpha_1",
     "validated": "alpha_1 = 0 at a=0 == ALS eq (61); a=1/2 is UNSEARCHED at primary source",
     "test": "test_critical_dissipation.py"},
    {"module": "solver/marginal_flow.py", "object": "the augmented (Omega, mu) flow, driven",
     "holds": "time integration of (F_mu)+(M) as an initial-value problem",
     "validated": ("lambda_mu slope +2.0011 vs +2, zero at 1.50009 vs 1.5; `integrate` "
                   "reports `converged` and gate 11 enforces it (the NaN of leg 41)"),
     "test": "test_marginal_flow.py"},

    # -- 2D Boussinesq (the CERTIFIED object -- see solver/target_selection.py) ------
    {"module": "solver/boussinesq_velocity.py", "object": "2D Boussinesq velocity (Biot-Savart)",
     "holds": "polar-grid stream-function solve with the boundary, Thomas sweeps",
     "validated": ("manufactured stream-function solutions; the Route-L line sweep is\n                   gated to 9.5e-16 against the operator it inverts"),
     "test": "test_boussinesq_velocity.py"},
    {"module": "solver/boussinesq_rescaled.py", "object": "2D Boussinesq, rescaled RHS",
     "holds": "the rescaled (omega, eta, xi) system, modulation (c_l, c_omega), relaxation",
     "validated": ("reproduces Chen-Hou's beta to 2.1% -- and Route-K showed the "
                   "relaxation LIMIT-CYCLES and its residual GROWS under refinement, so "
                   "'resolution-stable' here is not 'converged' (71)"),
     "test": "test_boussinesq_rescaled.py"},
    {"module": "solver/port_certification.py", "object": "the L1->L2 certification port",
     "holds": ("ProfileResidual, GMRES, Krylov ladders, the leading-order and LINE-SWEEP "
               "preconditioners (exact O(N) inverse of the full transport operator), "
               "radii_polynomial_status"),
     "validated": ("line sweep gated to 9.5e-16 against the operator it inverts; "
                   "radii_polynomial_status returns BLOCKED_AT_STEP_ONE and is gated to "
                   "carry NO fabricated Y_0 or Z_1"),
     "test": "test_port_certification.py"},
    {"module": "solver/fractional_boussinesq.py", "object": "2D Boussinesq, fractional dissipation",
     "holds": "the critical-dissipation exponent for the 2D object",
     "validated": "consistency with the 1D critical exponent; no independent known answer",
     "test": "test_fractional_boussinesq.py"},

    # -- the certificate: spaces, bounds, Newton-Kantorovich ------------------------
    {"module": "solver/interval.py", "object": "rigorous interval arithmetic",
     "holds": "hand-rolled outward-rounded intervals; no scipy, no mpmath",
     "validated": ("containment holds on adversarial cases, including the directed-rounding\n                   edge cases where naive intervals lose the answer"),
     "test": "test_interval.py"},
    {"module": "solver/nk_bounds.py", "object": "Newton-Kantorovich constants, upper bounds",
     "holds": "genuine upper bounds for the Route-D constants",
     "validated": ("agrees with hand-computed cases; Route-D v6 found the discrete-ball\n                   TRAP here -- the bound was true and useless"),
     "test": "test_nk_bounds.py"},
    {"module": "solver/op_lower.py", "object": "a LOWER bound on ||A||",
     "holds": "the lower bound that says how much room the upper bounds have left",
     "validated": ("brackets the dense operator norm from below wherever both are\n                   computable"),
     "test": "test_op_lower.py"},
    {"module": "solver/holder_norms.py", "object": "weighted-Holder spaces (two gradings)",
     "holds": "the two-grading space Route-D v3+v4 jointly demanded",
     "validated": ("norm axioms and the embedding constants; the weighted-l1 no-go is\n                   derived here and is UNSEARCHED at primary source"),
     "test": "test_holder_norms.py"},
    {"module": "solver/decay_grading.py", "object": "decay-graded function spaces",
     "holds": "algebraic-decay gradings on an unbounded domain",
     "validated": ("compare against CLN arXiv:2302.12877, which does the same job with "
                   "Hilbert/Fourier spaces -- read for Route-M, NOT yet a gate"),
     "test": "test_decay_grading.py"},
    {"module": "solver/decay_collocation.py", "object": "collocation in decay-graded sup norms",
     "holds": "the two-scale operator discretized in the norm the bounds live in",
     "validated": ("manufactured solutions on the graded grid, convergence under\n                   refinement"),
     "test": "test_decay_collocation.py"},
    {"module": "solver/collocation_newton.py", "object": "Newton in the bounds' own basis",
     "holds": "the Newton solve and the defect the certificate actually sees",
     "validated": ("matches the dense Newton solve on shared problems, and reports the\n                   defect the certificate sees"),
     "test": "test_collocation_newton.py"},
    {"module": "solver/reduced_certificate.py", "object": "the float rehearsal of the certificate",
     "holds": "the whole certificate in floats, and what it still needs to be rigorous",
     "validated": ("internally self-consistent across the reduced space; explicitly NOT a\n                   proof -- float64 throughout"),
     "test": "test_reduced_certificate.py"},
    {"module": "solver/nk_fourier.py", "object": "Fourier (circle) form of the two-scale operator",
     "holds": "the periodic representation and its bounds",
     "validated": ("multiplier symbols against the line form on shared test functions; "
                   "no independent published known answer"),
     "test": "test_nk_fourier.py"},
    {"module": "solver/nk_seminorm.py", "object": "domain seminorm of ||A||",
     "holds": "a derivative-gain closure free of J",
     "validated": ("bounds dominate the dense operator seminorm on sampled fields; "
                   "no independent published known answer"),
     "test": "test_nk_seminorm.py"},
    {"module": "solver/hilbert_holder.py", "object": "codomain seminorm: H in weighted Holder",
     "holds": "weighted-Holder boundedness of the Hilbert transform",
     "validated": "no known-answer gate; bounds checked against dense sampling",
     "test": "test_nk_hilbert_holder.py"},
    {"module": "solver/hilbert_pointwise.py", "object": "pointwise |H(h)| bound",
     "holds": "the sharper pointwise bound and the payer rule it exposes",
     "validated": "no known-answer gate; sampled", "test": "test_nk_hilbert_pointwise.py"},
    {"module": "solver/first_integral.py", "object": "first integral of the two-scale equation",
     "holds": "the profile on its own support (SUPERSEDES solver/finite_support.py)",
     "validated": "the closed form against the ODE; finite support is PARTIAL vs HTW Prop 2.3",
     "test": "test_first_integral.py"},
    {"module": "solver/turning_point.py", "object": "the turning point at X_c",
     "holds": "what actually makes the inverse diverge", "validated": ("locates the zero of c + aU to the ODE integrator's own tolerance"),
     "test": "test_turning_point.py"},
    {"module": "solver/profile_newton.py", "object": "Newton on the two-scale profile equation",
     "holds": "the other side of the inequality", "validated": ("converges to the known a=0 two-scale profile; residual falls to the\n                   Newton floor"),
     "test": "test_profile_newton.py"},
    {"module": "solver/advection_scope.py", "object": "where the advection term lives in a",
     "holds": "scope of the Route-D bound programme", "validated": ("agrees with the analytic small-a and large-a limits of the advection\n                   coefficient"),
     "test": "test_advection_scope.py"},

    # -- literature, targets, search, plumbing --------------------------------------
    {"module": "solver/literature_gates.py", "object": "published results as executable gates",
     "holds": ("Route-J's CLAIM_LEDGER: twelve standing claims vs primary sources; "
               "Schochet's corrected constant; ALS/XU/CH/HTW transcriptions"),
     "validated": ("Schochet residual 5.2e-16 corrected vs 2.4e-2 as printed (13.7 "
                   "decades); Route-H's (E) == ALS (57)-(58) pointwise"),
     "test": "test_literature_gates.py"},
    {"module": "solver/bordered_hl.py",
     "object": "HL_S2_nonsymmetric -- the BORDERED steady system (Route-PORT, legs 46/47)",
     "holds": ("the 2n+3 bordered residual for CHL (4.1)/(4.2) with the three gauge "
               "constants as UNKNOWNS, its exact analytic Jacobian, the exact quadratic "
               "remainder (F is degree 2, so Z_2 is exact), damped Newton, and the float "
               "certificate constants Y_0/Z_1/Z_2 in a weighted sup norm"),
     "validated": ("Newton to 5.66e-15 at n=201 (the relaxation of the same equations "
                   "FLOORS at ~1e-2); F(z+v) = F(z)+DF v+Q(v,v) gated to machine precision; "
                   "contraction ratio -2.5407 extrapolating to CHL's -2.5114 at 2.1e-04. "
                   "THE CEILING IS PART OF THE ENTRY: the polynomial closes around the "
                   "TRUNCATED object and the true object is 1.55e+08 ball radii outside it "
                   "(leg 46 P6b), and reach makes that WORSE (leg 47)"),
     "test": "test_bordered_hl.py"},
    {"module": "solver/viscous_novelty.py",
     "object": "certification UNDER DISSIPATION -- stage V's novelty gate (Route-V v0)",
     "holds": ("PRECEDENTS + novelty_verdict() (the gate, computed off the ledger); the "
               "Dahne-Figueras CGL/NLS profile ODE, an independent RK4 shooting solve, a "
               "three-term far field derived here, branch continuation THROUGH the fold "
               "(solve for (mu, eps) at fixed kappa), the ||J^-1|| margin proxy and its "
               "divergence exponent, and read_df_figure -- a published VECTOR figure read "
               "back as (eps, kappa) data"),
     "validated": ("their Tables 1/2 reproduced to 1.8e-07 on the j=1 rows (four rows in "
                   "all, worst 1.1e-05 at our xi_1=20 vs their 25); their Fig. 1a branch to "
                   "max 3.0e-06 / rms 1.9e-06 over 13 samples; their fold to 3.8e-07 in "
                   "eps*; the figure calibration self-checks against Table 1 to 1.0e-05; "
                   "the defect discriminates 351x under a 1e-04 kappa perturbation"),
     "test": "test_viscous_novelty.py"},
    {"module": "solver/weight_search.py",
     "object": "SEARCHING the certificate's function space (Route-C-PILOT, leg 49)",
     "holds": ("BorderedCLM -- the a=0 CLM steady system bordered with (c_l, c_omega) as "
               "IMPLICIT unknowns, exact analytic Jacobian, exact quadratic remainder; the "
               "weight fitness log10(Y_0/budget) over a two-factor algebraic weight family "
               "plus the scalar border weights; FitnessEngine (batched, Jacobian inverted "
               "once); the FROZEN six-property viability gate; grid_search; lower_wall; "
               "PRECEDENTS + novelty_verdict()"),
     "validated": ("the closed-form CLM profile nulls the residual and Newton converges to "
                   "it, 4.13e-05 -> 4.24e-07 over n=201..801, with c_omega -> -1 as "
                   "1/X_max; F(z+v)=F(z)+DF v+Q(v,v) to 9.7e-16; the fitness's global "
                   "gauge invariance to 4.4e-16; the analytic wall's growth rate x7.39 "
                   "measured vs x7.39 predicted. THE VERDICT IS PART OF THE ENTRY: the "
                   "gate returns FAIL 4/6 (P2 finite 0.775 < 0.90, P3 max|slope-1| 0.092 > "
                   "0.05), so NO GA has been run on this fitness, and the admissible band "
                   "shuts entirely at n ~ 3.2e3 because Z_1 is float conditioning"),
     "test": "test_weight_search.py"},
    {"module": "solver/target_selection.py", "object": "which object to certify (Route-M)",
     "holds": ("TARGET_LEDGER: six candidates x three questions; CERTIFICATION_RECORD; "
               "the radii-polynomial Y_0 BUDGET; the 3D-NS preprint closure audit"),
     "validated": ("reproduces CLN's published Kawahara radius exactly; the Y_0 budget "
                   "brackets the radii polynomial's root on four (Z1,Z2) pairs"),
     "test": "test_target_selection.py"},
    {"module": "solver/ga_search.py", "object": "generic real-coded genetic algorithm",
     "holds": "tournament + BLX-alpha + annealed mutation + elitism, deterministic per seed",
     "validated": "beats random search on the committed benchmark; NO fitness of its own",
     "test": "test_ga.py"},
    {"module": "solver/boussinesq.py", "object": "2D Boussinesq, physical space",
     "holds": "pseudo-spectral solver (Phase 1, Gate 1a)",
     "validated": "no dedicated test file -- exercised through test_solver_boussinesq.py",
     "test": "test_solver_boussinesq.py"},
    {"module": "solver/gclm.py", "object": "gCLM, physical space",
     "holds": "pseudo-spectral solver (Stage 1)",
     "validated": "no dedicated test file -- exercised through test_solver_clm.py",
     "test": "test_solver_clm.py"},
    {"module": "solver/spectral_utils.py", "object": "spectral helpers",
     "holds": "FFT plumbing for the pseudo-spectral solvers",
     "validated": "no dedicated test file -- exercised through the solvers above",
     "test": "test_solver_clm.py"},
    {"module": "solver/finite_support.py", "object": "SUPERSEDED -- do not use",
     "holds": "replaced by solver/first_integral.py (Route-D v14)",
     "validated": ("nothing -- SUPERSEDED, kept only so the name resolves to a warning "
                   "instead of to nothing"),
     "test": "test_first_integral.py"},
]


def find(term):
    """Every entry whose text mentions `term`, case-insensitively."""
    t = term.lower()
    return [c for c in CAPABILITIES
            if any(t in str(v).lower() for v in c.values())]


def modules():
    return {c["module"] for c in CAPABILITIES}


def _show(rows):
    for c in rows:
        print(f"\n{c['object']}")
        print(f"  module    {c['module']}")
        print(f"  holds     {c['holds']}")
        print(f"  validated {c['validated']}")
        print(f"  test      {c['test']}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        term = " ".join(sys.argv[1:])
        rows = find(term)
        print(f"CAPABILITIES matching {term!r}: {len(rows)} of {len(CAPABILITIES)}")
        _show(rows)
    else:
        print(f"CAPABILITY INDEX -- {len(CAPABILITIES)} modules.  "
              f"Grep this BEFORE building anything.")
        _show(CAPABILITIES)
