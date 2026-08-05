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
                   "the Scenario-2 contraction ratio reproduces CHL's -2.5114 to 2.09e-04 "
                   "(bordered line) / 8.78e-03 (relaxation line) -- NOT '~1%', which "
                   "understated the agreement by up to 42x (leg 78). CHL's own print "
                   "granularity is 3.98e-05 relative, 251x tighter than the stale figure; "
                   "no primary source publishes it any tighter (leg 78, 5 channels, 0 hits)"),
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
     "validated": ("alpha_1 = 0 at a=0 == ALS eq (61); criticality sigma=3 at a=1/2 IS\n                   published (Xu arXiv:2607.19762 sec 6.1 + Table 1 row a=0.5 + Fig 3,\n                   's*(1/2)=3 exactly'); alpha_1 = +0.133683 there is SEARCHED-NOT-FOUND\n                   (leg 64, whole dissipative CLM corpus), i.e. measured, not\n                   independently validated"),
     "test": "test_critical_dissipation.py"},
    {"module": "solver/marginal_flow.py", "object": "the augmented (Omega, mu) flow, driven",
     "holds": "time integration of (F_mu)+(M) as an initial-value problem",
     "validated": ("lambda_mu slope +2.0011 vs +2, zero at 1.50009 vs 1.5; `integrate` "
                   "reports `converged` and gate 11 enforces it (the NaN of leg 41)"),
     "test": "test_marginal_flow.py"},

    # -- 2D Boussinesq (the CERTIFIED object -- see solver/target_selection.py) ------
    {"module": "solver/boussinesq_velocity.py", "object": "2D Boussinesq velocity (Biot-Savart)",
     "holds": "polar-grid stream-function solve with the boundary, Thomas sweeps",
     "validated": ("manufactured stream-function solutions; the Route-L line sweep is\n                   gated to 9.5e-16 against the operator it inverts. FIRST EXTERNAL\n                   known-answer gate (leg 73): reproduces the classical Lamb corner-image\n                   velocity closed form (Lamb, Hydrodynamics Art. 155; Crosby-Johnson-\n                   Morrison, Phys. Fluids 25 (2013)) to 1.76e-4 relative at observed order\n                   2.00, pre-committed tolerance 1e-2 (57x margin)"),
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
                   "carry NO fabricated Y_0 or Z_1 -- and now ALSO validates the constants a "
                   "caller does supply: negative or non-finite Y_0/Z_1/Z_2 return "
                   "INVALID_INPUT ahead of the discriminant, per the theorem's hypothesis "
                   "that they are upper bounds on norms (van den Berg-Lessard, AMS Notices "
                   "62(9):1057). Leg 79's 39-case adversarial battery measured 11 of 25 "
                   "hypothesis-violating inputs coming back closes=True (44%, including the "
                   "sign flip (-1.0,0.9,1e4)) against the UNGUARDED function; it is 0 of 25 "
                   "with the guard, and the 11 are pinned by label in "
                   "test_port_certification_regression.py"),
     "test": "test_port_certification.py"},
    {"module": "solver/fractional_boussinesq.py", "object": "2D Boussinesq, fractional dissipation",
     "holds": "the critical-dissipation exponent for the 2D object",
     "validated": ("consistency with the 1D critical exponent; SEARCHED for an independent\n                   answer (leg 67) and none exists -- the literature's alpha+beta=1\n                   threshold (Stefanov-Wu-Xu-Ye arXiv:2606.03680) is a well-posedness\n                   scaling bound, not comparable to this arrest exponent; stored\n                   s_c=0.1711999849 remains internally-consistent-only"),
     "test": "test_fractional_boussinesq.py"},

    # -- the certificate: spaces, bounds, Newton-Kantorovich ------------------------
    {"module": "solver/interval.py", "object": "rigorous interval arithmetic",
     "holds": ("hand-rolled outward-rounded intervals; no scipy, no mpmath; plus "
               "dot2_matvec -- the COMPENSATED (Ogita-Rump-Oishi error-free-transformation) "
               "matvec whose bound is u|x.y| + gamma_m^2 sum|x_j y_j| + 8 m eta, i.e. relative "
               "to the ANSWER rather than to the terms, plus Rump's (BIT 2012) ABSOLUTE "
               "underflow term; the plain reductions isum/matvec carry gamma_m sum|terms| + "
               "2 m eta. Dekker's splitting RAISES OverflowError at |entry| >= 2^997 = 1.34e300 "
               "instead of returning a NaN error term, and the Interval constructor widens a "
               "NaN endpoint to the trivial enclosure [-inf, +inf] instead of storing it -- a "
               "NaN endpoint used to pass the lo <= hi guard vacuously and then pass every "
               "downstream containment check with it"),
     "validated": ("containment holds on adversarial cases, including the directed-rounding\n"
                   "                   edge cases where naive intervals lose the answer. Leg 69's "
                   "size- and\n                   conditioning-matched corpus (exact "
                   "fractions.Fraction ground truth, 14036\n                   cases): 0 false "
                   "negatives in 12356 normal-range cases -- accumulation\n                   "
                   "lengths 32 to 260, entry magnitudes 1e-100 to 1e100, the LIVE zero-diagonal\n"
                   "                   bordered_linearization at K = 16..128, rows cancelled to "
                   "~1e-32 relative --\n                   worst relative slack +5.06e-20 and no "
                   "case touching an endpoint. The 62\n                   subnormal-band false "
                   "negatives it found (scales 1e-150..1e-160, worst escape\n                   "
                   "6.58 eta = 3.25e-323) and the silent [nan, nan] above 2^997 are REPAIRED and\n"
                   "                   re-gated as soundness assertions: 0/200 across scales "
                   "1e-145..1e-165 through\n                   both reductions, and the Dekker "
                   "wall now raises. The repair is bit-for-bit\n                   inert in the "
                   "live operating range (entries 0.5 to 128, ~140 decades above\n                "
                   "   the subnormal band and ~298 below the wall): 100 pre/post enclosures on "
                   "the\n                   live operator and the normal-range battery are "
                   "identical endpoint bit\n                   patterns, the eta term first "
                   "moving a bit only near input scale 1e-310. Both bands are gated in\n"
                   "                   test_interval_stress.py"),
     "test": "test_interval.py"},
    {"module": "solver/interval_certificate.py",
     "object": "the certificate constants as RIGOROUS BOUNDS (Route-L1 step one, leg 50)",
     "holds": ("interval enclosures of F and DF for BOTH bordered systems (HL and CLM), the "
               "monotone-split point-matrix x interval-matrix product (four BLAS matmuls, no "
               "O(N^3) Python), weighted_rowsum_bound with every step rounded up, "
               "interval_constants and a conservative radii_verdict"),
     "validated": ("enclosures contain the EXACT RATIONAL value (fractions.Fraction) on "
                   "sampled rows of H, Uop and D; the rigorous Z_1/Z_2/||A|| dominate their "
                   "float readings; a 1e-06 poisoned iterate is rejected at 5.6e+03 while "
                   "1e-10 -- inside the certified ball -- is accepted. RESULT: the radii "
                   "polynomial CLOSES on HL_S2_nonsymmetric at n=201/401/801 "
                   "(Y_0/budget 2.28e-03, 2.20e-02, 2.07e-02). THE CEILING IS PART OF THE "
                   "ENTRY: this is the TRUNCATED DISCRETE system on |X|<=745 with the stored "
                   "operators as exact data -- the far-field tail and the consistency of "
                   "(H, D) are NOT bounded, so it is step one of L1 and not L1. FIRST "
                   "END-TO-END PUBLISHED KNOWN-ANSWER GATE (leg 61): run on CLN's Kawahara "
                   "problem at their own truncation, the certified interval [6.77e-15, "
                   "2.62e-02] contains CLN's published [2.27e-14, 1.5e-02] entirely -- "
                   "resolution ~0.5 decades, not a digit. This clears leg 56's 1.85e7x and "
                   "2.04e11x consistency defects by 6.5 and 10.5 decades respectively"),
     "test": "test_interval_certificate.py"},
    {"module": "solver/spectral_certificate.py",
     "object": ("the certificate in the COMPACTIFIED basis, where the operators are exact "
                "(Route-L1 step two, leg 51)"),
     "holds": ("the exact coefficient-space residual (clm_residual, finite and rational -- a "
               "K-mode profile has a 2K-mode residual with NO truncation error), the bordered "
               "linearisation with a dissipation dial, weighted l^1 norms in three classes "
               "(flat / algebraic (1+k)^s / geometric nu^k), the Banach algebra constant, "
               "rigorous finite-block constants, the TAIL BLOCK and its inverse norm, the "
               "homogeneous tail mode, exact rational inverse norms, and the executable "
               "exactness audit of the three operator identities (moebius_power)"),
     "validated": ("the a=0 CLM anchor's residual is EXACTLY Fraction(0) on all 18 modes; the "
                   "basis identities hold to 3.5e-15 through exact Gaussian rationals; the "
                   "velocity constants are (-1)^k k exactly; float weighted inverse norms "
                   "match exact rational Gauss-Jordan to 8.8e-15. THE CEILING IS PART OF THE "
                   "ENTRY: the tail operator's diagonal is exactly zero and its kernel is the "
                   "|X|^-1 far field, so the tail term diverges in EVERY weight class tried "
                   "(flat M^1.28, algebraic best M^0.64, geometric x nu per mode) -- the "
                   "positive control with Lambda^1 dissipation saturates, so that is a "
                   "measurement and not a broken instrument. LEG 52 bordered that tail with "
                   "the far field and BOUNDED it (7.46 -> 9.44 at s=0, 8.09 -> 11.37 at "
                   "s=0.3); LEG 53 (experiments/p2_route_tc_v1_assemble.py) ASSEMBLED the "
                   "four terms and the certificate still does not close -- with the "
                   "BLOCK-DIAGONAL approximate inverse the method requires, the COUPLING "
                   "sub-blocks of I - A L are 1.39 and 43.15 at the best split in the whole "
                   "sweep (K = 4..64, s = 0 and 0.3, both gauges), 20.47 over every "
                   "normalisation ablated, and they grow x2 and x4 per doubling of K because "
                   "the unbounded part is OFF-DIAGONAL and the bordered tail inverse is a "
                   "constant rather than a decaying multiplier. SCOPE (VERIFIER, leg 53 "
                   "review): the term that exceeds 1 CONTAINS Gamma^-1, so this is a "
                   "statement about the block-diagonal A and NOT that no finite block can "
                   "close it -- the finite-block-independent sub-block bottoms out at 0.9961. "
                   "Do not read the bounded tail as a certificate"),
     "test": "test_spectral_certificate.py"},
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
     "validated": ("norm axioms and the embedding constants; the weighted-l1 no-go and\n                   the discrete-ball trap are derived here and were SEARCHED at primary\n                   source (leg 65, 4 papers full-text + 39 forward citations) and NOT\n                   found -- nearest cousin arXiv:2607.15256 SS1.2, same genre, resolved\n                   not obstructed"),
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
    {"module": "solver/target_norm.py",
     "object": ("whether the TARGET is in the certificate's space at all -- the "
                "compactified-basis coefficient decay of HL_S2_nonsymmetric "
                "(Route-NB, leg 55)"),
     "holds": ("the tangent half-angle projection X = tan(theta/2) onto the FULL circle "
               "(the target is NON-symmetric, so cosines too), high-order Lagrange "
               "interpolation on the uniform rho grid with an explicit far-field closure, "
               "the coefficient magnitudes in both the complex and real conventions, a "
               "power-law exponent fitter robust to symmetry-annihilated modes, weighted "
               "l^1 partial sums with an analytic tail, and the controls: the CLM anchor, "
               "1/(1+|X|), the sawtooth, and the calibration family (1+X^2)^(-alpha/2)"),
     "validated": ("the map agrees with spectral_certificate.moebius_power to 1.3e-15, so "
                   "the projection lands in the certificate's OWN basis; the positive "
                   "control (a=0 CLM anchor, exactly one mode) returns ||h_1|-1| = 3.4e-15 "
                   "with every other mode under 1.7e-12, inside its pre-registered window; "
                   "the sawtooth matches its closed form 2/(pi k) to 1.6e-03 and sits at "
                   "p = 1.001 (the flat class's divergence threshold); 1/(1+|X|) sits at "
                   "p = 1.989 (the s = 1 threshold); the calibration family recovers "
                   "1 + alpha to 7.5e-03 over alpha = 0.1..1.5, and 3.9e-03 at the "
                   "target's own alpha -- ALL OF IT AT THE HEADLINE'S OWN TRANSFORM SIZE "
                   "M = 16384, because the systematic is a property of the (M, band) pair "
                   "and calibrating on a finer grid than the target can reach flatters "
                   "the instrument (VER-B review of leg 55). RESULT: the target decays "
                   "as k^-1.3937 (X_max = 4.1e+04) / k^-1.3963 (3.0e+05), resolution drift "
                   "3.8e-04, so ||.||_(l^1_w) is FINITE at s = 0 (margin +0.394, 101x the "
                   "systematic) and s = 0.3 (+0.094, 24x) and DIVERGENT at s = 1 (-0.606); "
                   "s = 0.39 is NOT RESOLVED (margin 0.96x the systematic). THE CEILING IS PART "
                   "OF THE ENTRY: this measures the OBJECT, not any certificate -- a "
                   "finite norm says the target is IN the space and says NOTHING about "
                   "whether a radii polynomial closes. It is also DOMAIN-limited, not "
                   "resolution-limited: at the shipped X_max = 745 the far-field closure "
                   "moves the exponent by 0.190 and the measurement is not trustworthy "
                   "there; the headline is taken where no sample point leaves the grid"),
     "test": "test_target_norm.py"},

    # -- literature, targets, search, plumbing --------------------------------------
    {"module": "solver/literature_gates.py", "object": "published results as executable gates",
     "holds": ("Route-J's CLAIM_LEDGER: twelve standing claims vs primary sources; "
               "Schochet's corrected constant; ALS/XU/CH/HTW transcriptions"),
     "validated": ("Schochet residual 5.2e-16 corrected vs 2.4e-2 as printed (13.7 "
                   "decades); Route-H's (E) == ALS (57)-(58) pointwise"),
     "test": "test_literature_gates.py"},
    {"module": "solver/certificate_shapes.py",
     "object": "the SHAPE dichotomy (Route-XS, leg 57): published CAP certificates classified",
     "holds": ("SHAPE_LEDGER: four published computer-assisted certificates x three "
               "questions -- is the unbounded part a MULTIPLIER or a SHIFT, is the "
               "approximate inverse block diagonal, does the tail inverse decay -- each "
               "row traced to a LOCATED FULL-TEXT statement (never an abstract); "
               "gate_answer() as an executable predicate; and the dichotomy as a MEASURED "
               "continuous dial via mu on solver/spectral_certificate.py's tail block"),
     "validated": ("gate answers NO over 4 published rows and flips to YES on a fictitious "
                   "control row, so the negative is a fact about the literature and not "
                   "about the code (lesson 90); mu = 0 alone fails -- M-exponent +1.021 "
                   "unbordered (the inverse does not exist, which is why leg 52 bordered) "
                   "and K-exponent +0.437 once bordered, vs -0.849..-0.946 for every "
                   "mu > 0. CORRECTS legs 52-53: the bordered tail inverse is NOT a "
                   "constant, it GROWS 2.191 -> 11.528 over K = 4..128 (5.26x), so the "
                   "2.19 those legs quote is the smallest rung of a rising ladder, not a "
                   "bound. SCOPE: the dichotomy is FOLKLORE IN PRINT (Cadiot "
                   "arXiv:2505.03091 sections 2 and 3 state both halves) -- this module "
                   "is BOOKKEEPING that makes it executable, NOT a finding of ours. BDL "
                   "arXiv:1503.06315 publish the NON-BLOCK-DIAGONAL approximate inverse "
                   "that MM's remaining free choice proposes, and their Prop 2.3 gets the "
                   "full multiplier-case decay gain s_L, but only under assumption (4), a "
                   "diagonal bounded below -- so the precedent does NOT extend to a zero "
                   "diagonal. Chen-Hou certify a genuine SHIFT and form no tail estimate "
                   "at all. Float64, no intervals; four papers is a corpus, not a theorem"),
     "test": "test_certificate_shapes.py"},
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
     "validated": ("dedicated: test_boussinesq_dedicated.py (17 checks) + "
                   "test_solver_boussinesq.py; odd-n derivative path checked correct"),
     "test": "test_boussinesq_dedicated.py"},
    {"module": "solver/gclm.py", "object": "gCLM, physical space",
     "holds": "pseudo-spectral solver (Stage 1)",
     "validated": ("dedicated: test_gclm_dedicated.py (14 checks) + test_solver_clm.py; "
                   "sin x exact stationary point of De Gregorio (a=1) to 2.1e-15"),
     "test": "test_gclm_dedicated.py"},
    {"module": "solver/spectral_utils.py", "object": "spectral helpers",
     "holds": "FFT plumbing for the pseudo-spectral solvers",
     "validated": ("dedicated: test_spectral_utils_dedicated.py (10 checks); odd-n "
                   "derivative_hat defect found by leg 66, FIXED (n is now a required "
                   "argument -- rfft length cannot reveal its parity)"),
     "test": "test_spectral_utils_dedicated.py"},
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
