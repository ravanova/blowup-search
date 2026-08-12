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

SELF-AUDIT, generation 1: leg 71 (Route-CAP), 2026-08-06 -- all 42 rows run against the
suite, twice (at e203b52 and again at 10fed85 after rebase); 33 clean, 2 RED at HEAD
(test_fractional_boussinesq.py, test_profile_newton.py -- reported, NOT fixed here),
1 `test` field corrected (solver/ga_search.py, which cited a test that never loaded it).
See writeup/data/p2_route_cap_v1_audit.json and experiments/journal/leg_71.md.

SELF-AUDIT, generation 2: leg 292 (Route-CAPA), 2026-08-11, at 80c0cc4 -- 48 rows on six
axes, every count in writeup/data/p2_route_capa_v2_audit.json.
  S1 completeness  48 rows / 48 distinct modules / 48 solver/*.py on disk; 0 missing,
                   0 ghost, 0 duplicate.  The append-only convention holds over ~220 legs.
  S2 test presence 0 rows citing an absent file; 0 rows with an empty `test`.
  S3 greenness     47 of 47 distinct cited tests EXECUTED and green at 80c0cc4;
                   0 red, 0 timed out, 5396.5 s cumulative (47% of it one test,
                   test_advection_scope.py at 2512.2 s).  Leg 71's two reds
                   (test_fractional_boussinesq.py, test_profile_newton.py) are both
                   green now -- fixed by their owning legs, unrecorded until here.
  S4 gate prose    33 rows name a magnitude, 3 say "no known-answer gate" plainly, 12
                   claim validation with no number -- so the contract above is met in the
                   letter by 36/48 (75%).  The 12 are NAMED in the journal and were
                   deliberately NOT rewritten: supplying a magnitude for another leg's
                   module from an audit chair is the fabrication this field exists to stop.
                   If you own one of those 12 and have the number, this row is the cheapest
                   place in the repository to bank it.
  S5 relevance     Does the cited test actually LOAD the module citing it?  Leg 71 DID
                   measure this (per-row test_imports_module in its own JSON) and flagged
                   the same single row; what it could not do was repair it, because at
                   e203b52 no test in the repository loaded that module.  Leg 292's
                   contribution is not the axis but the repair, now possible: 1 of 48 rows
                   fails, the SUPERSEDED row at the bottom of this file, whose cited test
                   never loads it.  Leg 124 wrote the adversarial test that does, 53 legs
                   later, and no one moved the citation for ~220 legs -- the check was run
                   once, not standing.  `test` field corrected below; `validated` frozen.
                   CAUTION for future editors of that row: leg 124's S10 gate greps every
                   *.py in the tree for a line containing both the module's stem and the
                   word "imp"+"ort", so prose here that puts those two on ONE line turns
                   that test red.  Measured, not guessed: this header did exactly that.
  S6 references    19 repo paths cited inside row prose, 0 dangling.
NOTE: `test_capabilities.py` has received 0 commits since leg 71's base -- it still checks
only that `test` is non-empty, that the path EXISTS, and that `validated` is over 20
characters.  It does not run the test and does not check relevance.  S3 and S5 are
therefore not automatable inside it at merge-gate cost; re-run the leg-292 runner instead.
See writeup/data/p2_route_capa_v2_audit.json and experiments/journal/leg_292.md.
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
     "validated": ("relaxes to the exact CLM self-similar fixed point -4X/(1+4X^2) at the\n"
                   "                   validated gauge f(0) = -4. The fixed point is a one-parameter LINE\n"
                   "                   (Omega_0(lambda X) steady for every lambda) and the residual is\n"
                   "                   degree-1 in lambda, so run()'s stopping test is RELATIVE to the\n"
                   "                   frozen gauge, tol * max(|f(0)|/4, GAUGE_TOL_FLOOR) -- an absolute\n"
                   "                   tol was met by the initial data alone for lambda < 3.4e-09 and\n"
                   "                   reported convergence after 1 step (85, repaired). Exactly 1x at\n"
                   "                   f(0) = -4, so every banked number is unchanged"),
     "test": "test_gclm_rescaled.py"},
    {"module": "solver/rescaled_spectrum.py", "object": "gCLM rescaled linearization, spectrum",
     "holds": "dense spectrum of the linearization about the rescaled fixed point",
     "validated": ("point spectrum {0,1} at a=0, which XU Theorem 2 later proved -- but "
                   "in the LOOSE realization: our grid imposes NO origin condition (70)"),
     "test": "test_rescaled_spectrum.py"},
    {"module": "solver/origin_h2_certificate.py",
     "object": ("the a=0 CLM linearisation on the odd origin-H^2 space X -- the STRICT "
                "realization, the one WITH the spectral gap (Route-H2C, leg 176)"),
     "holds": ("L_0^+ = xi d/dxi + Volterra in the Laguerre basis, where it is EXACTLY "
               "tridiagonal with rational entries (-n/2, 1/2, (n-1)/2); the X Gram I + J^4 "
               "(exact, banded); Xu's two symmetry modes, which occupy exactly span{l_0,l_1}; "
               "the bordered formulation [[L_0^+, m],[ell, 0]] with ell_n = i(-1)^n(1-2n); "
               "Xu eq. (4.23)'s closed-form resolvent at z=0 with exact-Taylor inner integrals; "
               "the Blaschke y-space evaluator and its FFT inverse; X operator norms and the "
               "range-untruncated sigma_min diagnostic"),
     "validated": ("the four structural identities are EXACT zeros, not tolerances -- "
                   "L_0^+ b^-2 = b^-2, L_0^+ m = 0, ell.L_0^+ = 0 and ell(m) = 1 all to 0.0; "
                   "the tridiagonal entries agree with an independent Laguerre quadrature to "
                   "1.6e-13; Xu eq. (4.23) satisfies Xu's own ODE pointwise to 2.6e-15 relative "
                   "(leg 163's class was 2.8e-14); the X norm agrees between the Gram form and "
                   "an independent y-space quadrature to 1.3e-16.  CEILING: a=0 only, float64, "
                   "nothing interval-enclosed, and it certifies an object Xu already inverts "
                   "in closed form -- nothing transfers to a>0 or to HL_S2_nonsymmetric"),
     "test": "test_origin_h2_certificate.py"},
    {"module": "solver/fractional_gclm.py", "object": "gCLM with fractional dissipation",
     "holds": "Lambda^s dissipation, the critical exponent s_c, relevance thresholds",
     "validated": "s_c = alpha/2 against XU eq (6.3) row by row (PRE-EMPTED, Route-J)",
     "test": "test_fractional_gclm.py"},
    {"module": "solver/critical_dissipation.py", "object": "gCLM at exactly critical dissipation",
     "holds": "the marginal case and the invariant alpha_1",
     "validated": ("alpha_1 = 0 at a=0 == ALS eq (61); criticality sigma=3 at a=1/2 IS\n                   published (Xu arXiv:2607.19762 sec 6.1 + Table 1 row a=0.5 + Fig 3,\n                   's*(1/2)=3 exactly'); alpha_1 = +0.133683 there is SEARCHED-NOT-FOUND\n                   (leg 64, whole dissipative CLM corpus), i.e. measured, not\n                   independently validated"),
     "test": "test_critical_dissipation.py"},
    {"module": "solver/dissipative_profile.py",
     "object": "Chen arXiv:1908.09385's gamma=2 (full-Laplacian) gCLM candidate",
     "holds": ("Chen's transcribed constants with PER-CONSTANT provenance, the DISSIPATIVE "
               "steady self-similar residual and its exact Jacobian, Newton with both gauges "
               "fixed, the gauge-invariant gamma=2 obstruction Delta = 2 c_l/|c_omega| - 1, "
               "and the Y_0/Z_2/budget measurement (FLOAT, never a certificate)"),
     "validated": ("Chen's closed form eq (2.2) Omega = -2bx/(x^2+b^2)^2, b = sqrt(3/8) nulls "
                   "the steady residual to sup 3.74e-06 (n=601) falling to 2.36e-07 (n=1201), "
                   "and Newton RECOVERS his constants as free OUTPUTS -- c_l -> 0.333333435 "
                   "(Chen 1/3) and H Omega(0) -> 2.666666568 (Chen 8/3), shape sup error "
                   "4.18e-06 -> 2.61e-07 across n=601..1201.  Delta = -0.333317 at Chen's "
                   "a=1/2 against his own exact -1/3, derived independently of his (2.40).  "
                   "Lesson-90 controls: Delta returns EXACTLY 0.0 on the heat pair (1/2,-1) "
                   "and EXACTLY +1.0 at the a=0 CLM anchor, so it varies and can report the "
                   "other answer.  NOTE (leg 125): Chen has NO gamma=2 profile -- sec 2.6 "
                   "p.12, 'Since nu(t) converges to 0, such profile is the same as the "
                   "inviscid profile associated with a' -- so this module measures the "
                   "obstruction to one; it does not construct one"),
     "test": "test_dissipative_profile.py"},
    {"module": "solver/chen_inviscid_certificate.py",
     "object": ("Object A -- Chen arXiv:1908.09385 eq (2.2)'s INVISCID (nu=0) a=1/2 gCLM "
                "profile -- against EVERY radii-polynomial hypothesis, not just the budget"),
     "holds": ("exact Fraction rational-function arithmetic on the steady defect; the EXACT "
               "one-parameter dilation orbit Psi_g = -(16/3) g^{3/2} X/(X^2+g)^2 through the "
               "profile and its tangent (the kernel); the seven-clause certificate battery "
               "H1..H7; the far-field symbol clause sigma(s) = c_omega + s c_l; the bordered "
               "(phase-condition) repair; and the n-ladder that decides whether a clause is "
               "an operator fact or the grid.  Imports solver/dissipative_profile.py "
               "READ-ONLY for Chen's constants and operators; uses the ONE shared budget and "
               "the ONE shared hypothesis guard.  FLOAT throughout except the Fraction "
               "parts; never a certificate"),
     "validated": ("the defect numerator is the ZERO POLYNOMIAL in exact rational arithmetic "
                   "at g in {3/8, 1, 2, 1/7, 9/4} (g=3/8 is Chen eq (2.2) verbatim, and the "
                   "module's H Psi and U match leg 125's chen_profile to <1e-13), so Y_0 = 0 "
                   "EXACTLY -- while the certificate still cannot close, because the orbit "
                   "tangent is an exact kernel and (I - A DF)phi = phi forces Z_0+Z_1 >= 1 "
                   "for EVERY A.  Kernel is an operator fact, not the grid: its relative "
                   "defect falls 5.21e-05 -> 3.27e-06 across n=401..801 while a localised-bump "
                   "control stays flat at 0.689 (separation 2.11e05), and "
                   "sigma_min/sigma_max collapses like n^-6.68.  Z_2 ~ n^2.36 (9.44e10 -> "
                   "6.31e12 over n=201..1201), so it is NOT an operator constant here.  "
                   "Far-field symbol vanishes at s=3 = the profile's MEASURED decay exponent "
                   "2.999955 (X^-2 control measures -1.999911).  Lesson-90 controls that CAN "
                   "fail: perturbed amplitude, a=0, c_l=1/2, the bump, the X^-2 profile, and "
                   "the sigma-ratio collapse.  TRAP BANKED: pinv with default rcond silently "
                   "inverts the near-kernel (shadow 2.87e-09 instead of 1) whenever "
                   "sigma_min/sigma_max > n*eps; truncated at rcond=1e-6 it returns to "
                   "0.99998 -> 0.9999990"),
     "test": "test_chen_inviscid_certificate.py"},
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
    {"module": "solver/energy_coercivity.py",
     "object": ("the WEIGHTED-ENERGY (Chen-Hou-shaped) coercivity form of the a=0 CLM "
                "linearisation -- the THIRD realization (Route-WE, leg 111)"),
     "holds": ("the a=0 CLM linearisation applied POINTWISE in closed form (so no mode of "
               "L e_k is ever dropped) and as a coefficient matrix; the weighted L^2 Gram "
               "and form matrices; the coercivity gap -sup <L h,h>_phi/||h||^2_phi solved as "
               "a generalized symmetric eigenproblem with explicit whitening; the damping "
               "factor D_phi = (3/2)cos th + (1/2) sin th (log phi)' in closed form; a "
               "SEVEN-MEMBER weight family named in the module before any computation "
               "(two origin-singular power ladders); measured admissibility with the SHAPE "
               "of each divergence; the two published point-spectrum modes; and the "
               "Lambda^1-dissipation positive control"),
     "validated": ("the coefficient matrix is EXACTLY equal (0.0) to "
                   "spectral_certificate.bordered_linearization's interior block, so this is "
                   "the same operator the other two L1 realizations died on; pointwise vs "
                   "matrix agree to 1.9e-14; the two point-spectrum modes Xu arXiv:2607.19762 "
                   "publishes (L sin2th = 0, L(sin th + sin2th/2) = itself) reproduce to "
                   "2.2e-16; the flat-weight Gram is (pi/2)I to 1.4e-15 at n=64. THE CEILING "
                   "IS PART OF THE ENTRY: leg 111's gate answered NO. Every ADMISSIBLE member "
                   "of the family has a NEGATIVE gap converging to -(3-gamma)/2 (measured "
                   "-1.499886, -1.006201, -0.499924 at gamma = 0,1,2), because damping at the "
                   "origin needs gamma > 3 while the basis is in L^2_phi only for gamma < 3 -- "
                   "the SAME threshold, so the window has ZERO width ON THIS UNCONSTRAINED "
                   "ODD-SINE TRIAL SPACE (p=1 vanishing order). Leg 141 (Route-WEL) found "
                   "this content published -- not as this sentence, but as a special case: "
                   "Elgindi-Ghoul-Masmoudi arXiv:1906.05811 Prop 2.1 certifies a POSITIVE "
                   "gap of exactly 1/2 at gamma=4 on the SAME a=0 CLM linearization under "
                   "hypotheses that ARE these two thresholds, imposed on the perturbation "
                   "(not tested on a fixed basis); the window (3, 2p+1) by trial-space "
                   "vanishing order p is 0 at p=1, 2 at p=2, 4 at p=3, containing gamma=4 "
                   "for p>=2. Leg 111's own measurements are unchanged; what is capped is "
                   "reading them as a structural obstruction rather than a property of the "
                   "p=1 trial space. Independently verified line-by-line, leg 141's own "
                   "post-landing review (2026-08-06). gamma = 3's apparent "
                   "+4e-3 gap collapses like n^-1 (0.0426 -> 0.000121 over n = 16..256) AND "
                   "moves with the quadrature cutoff (+0.002938 -> +0.004005), i.e. it is a "
                   "statement about the code. The Lambda^1 positive control reports the OTHER "
                   "answer (-1.498 at mu=0 to +5.736 at mu=2), so the negative gap is a "
                   "measurement. Float64; measured on the friendliest object, so the wall "
                   "bounds HL_S2_nonsymmetric FROM BELOW only"),
     "test": "test_energy_coercivity.py"},
    {"module": "solver/certificate_guards.py",
     "object": "radii polynomial hypotheses, the ONE shared guard",
     "holds": ("the single validation predicate all three certificate-assembly modules "
               "call -- Y_0/Z_0/Z_1/Z_2 finite and nonnegative, r_min admissible, "
               "Holder-exponent ranges, weights that come from a norm"),
     "validated": ("leg 128: the same defect was measured three times -- "
                   "port_certification.py 11/25 (leg 79), interval_certificate.py 12/36\n"
                   "                   (leg 98), nk_bounds.py 21/52 (leg 116) -- and the "
                   "first two were repaired by COPYING one private function. Both copies "
                   "are now deleted and all three call this module: identity holds for "
                   "all three post-repair and for NONE pre-repair (the control comes out\n"
                   "                   differently), 0 inline copies remain (was 2 + 2), "
                   "and the three agree on a 7-case drift battery. 17 of leg 116's 21 "
                   "false-closing certificates now reject; the 4 that remain supply "
                   "constants that are nonnegative and finite, i.e. that SATISFY the\n"
                   "                   theorem's hypotheses and lie about a MAGNITUDE, "
                   "which no hypothesis guard can detect. NO known-answer gate of its own "
                   "-- it is exercised through the three modules' suites and through "
                   "test_repaired_all_three_modules_share_one_guard. Purely a REJECTION\n"
                   "                   layer: 4626/4626 clean-input values across the "
                   "three modules are bit-identical at 0 ULP against the pre-repair "
                   "sources, so no banked number moved. The documented differences "
                   "SURVIVE as parameters (port_certification's None-is-NOT-MEASURED\n"
                   "                   kill-switch, interval_certificate's raise-on-None, "
                   "three NaN parentheticals byte-for-byte, nk_bounds' fourth Z_0 slot)"),
     "test": "test_nk_bounds_adversarial.py"},
    {"module": "solver/nk_bounds.py", "object": "Newton-Kantorovich constants, upper bounds",
     "holds": "genuine upper bounds for the Route-D constants",
     "validated": ("agrees with hand-computed cases; Route-D v6 found the discrete-ball\n                   TRAP here -- the bound was true and useless. `budget` validated only\n"
                   "                   Z_2 > 0 until leg 128: leg 116 measured 21/52 "
                   "hypothesis-violating inputs returning a CLOSING certificate (19 "
                   "load-bearing), the sharpest a certified ball [0.8083, 1.1917] around "
                   "the NON-solution x=1.0 of F=x^2-2, containing no zero of F and\n"
                   "                   missing sqrt(2) by 1.161 ball radii. It now routes "
                   "hypothesis validation through solver/certificate_guards.py (17 of the "
                   "21 reject; the 4 remaining are hypothesis-SATISFYING magnitude lies), "
                   "refuses alpha >= 2 in farfield_modelling_error_bound (it returned a\n"
                   "                   max over a truncated window as a supremum, >5e7x "
                   "below the truth at alpha=3.0) and returns argmax_at_window_end, "
                   "refuses gamma outside (0,1] (a negative gamma flipped the 1/gamma "
                   "near-field term and REDUCED the claimed bound), and refuses\n"
                   "                   non-positive/NaN q_cod or v_cod (the "
                   "`1/q if q>0 else 0` mask dropped the dual bound 2.19x / 3.57x). "
                   "NOT repaired in value: _I_out's log-grid floor falls 2.12% below the "
                   "truth from X=1e11, because lowering it moves 15/15 clean live-range\n"
                   "                   values (worst 1.08e-04 relative); X > 1e10 WARNS "
                   "instead, and the live range tops out at X=3.2e7, 3.49 decades clear. "
                   "4527/4527 of this module's clean values bit-identical at 0 ULP"),
     "test": "test_nk_bounds.py"},
    {"module": "solver/op_lower.py", "object": "a LOWER bound on ||A||",
     "holds": "the lower bound that says how much room the upper bounds have left",
     "validated": ("brackets the dense operator norm from below wherever both are\n                   computable"),
     "test": "test_op_lower.py"},
    {"module": "solver/holder_norms.py", "object": "weighted-Holder spaces (two gradings)",
     "holds": "the two-grading space Route-D v3+v4 jointly demanded",
     "validated": ("norm axioms and the embedding constants; the weighted-l1 no-go and\n                   the discrete-ball trap are derived here and were SEARCHED at primary\n                   source (leg 65, 4 papers full-text + 39 forward citations) and NOT\n                   found -- nearest cousin arXiv:2607.15256 SS1.2, same genre, resolved\n                   not obstructed. Every entry point now REJECTS non-finite and\n                   degenerate input (finite grids, strictly increasing theta for the\n                   Jacobian check, gamma > 0): the four ordered-comparison filters used\n                   to DROP a NaN candidate instead of propagating it, so conformal_check\n                   -- the module's own self-validation -- returned its clean value\n                   bit-identically on a NaN-poisoned grid and (0.0, 0.0), i.e. exact\n                   agreement, on an all-NaN one, family_op_norm understated its own\n                   lower bound by 2.1053x, and holder_H_constant reported an embedding\n                   constant of 0.0 against a clean 0.891421 (100, repaired). 53/53 clean\n                   calls bit-identical, so every banked number is unchanged"),
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
                   "there; the headline is taken where no sample point leaves the grid "
                   "-- now CODE-ENFORCED (leg 84 adversarial audit + bench-repair): every "
                   "exponent-bearing function returns domain_valid/n_outside_grid and warns "
                   "on extrapolation (TargetNormDomainWarning); re-running the headline "
                   "margins with the guard active reproduces +0.394/+0.094 to 0.0 diff -- "
                   "confirmed NOT contaminated"),
     "test": "test_target_norm.py"},
    {"module": "solver/bc_weighted_sobolev.py",
     "object": "Breden-Chu weighted-Sobolev setting H^2(mu), mu = e^{|x|^2/4}/Z",
     "holds": ("the operator L = -Delta - (x/2).grad and its even half-Hermite/Laguerre "
               "eigenbasis psi_m = L_m^{(-1/2)}(x^2/4)e^{-x^2/4}/Zeta_m on the UNBOUNDED "
               "domain; Gauss-Laguerre nodes/log-weights WITHOUT scipy (Sturm bisection "
               "+ Newton); the six/four/two-product quadrature rules for products of "
               "psi and d_xpsi; eq. (54)'s self-similar viscous-Burgers profile (F, DF, "
               "Newton, an independent ODE-shooting seed); and all of arXiv:2404.04054 "
               "section 6's bounds Y, Zbar11/12/21/22, Z1, Z2, Z3 plus Corollary 21's "
               "radii polynomial.  NOT the ell^1_w/collocation/origin-H^2 machinery the "
               "plan of record bans -- the norm is the HILBERT ||L.||_{L^2(mu)} and the "
               "tail is controlled by L's Poincare gap, not by an ell^1 weight"),
     "validated": ("reproduces Breden-Chu's published Theorem 42 END TO END at their own "
                   "n = 1500 and their own quadrature sizes (N = 3n+3 / 2n+3): their "
                   "enclosure 1e-3 is a certified radius of THIS module's radii "
                   "polynomial, and an independently shot+Newton'd ubar matches their "
                   "released coefficients to 4.36e-10 in H^2(mu).  Y reproduces to "
                   "6.0e-05 relative and Z3 to their full print granularity; Z1 (1.31x) "
                   "and Z2 (0.81x) differ, and the difference is localised by ablation "
                   "to the L^infty bounds on psi_m, where their own code overshoots the "
                   "measured sup by up to 136x.  CEILING: float64, NOT interval "
                   "arithmetic -- this reproduces their CONSTANTS, not their proof; the "
                   "reproduction's own resolution is 1.6e-09 relative, measured by their "
                   "two exact rational quadrature identities and by <psi_a,psi_b> = "
                   "delta_ab over all modes"),
     "test": "test_bc_weighted_sobolev.py"},

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
     # Leg 71 (Route-CAP self-audit): was `test_ga.py`, which imports only the `ga/`
     # package and never touches this module -- `ga_search` appears nowhere in it or in
     # ga/. test_gclm_family.py is what actually exercises it (`from solver.ga_search
     # import ga_minimize, GAConfig`), including the determinism-per-seed property claimed
     # above. Factual `test`-field correction only; `validated` left frozen.
     "test": "test_gclm_family.py"},
    {"module": "solver/boussinesq.py", "object": "2D Boussinesq, physical space",
     "holds": "pseudo-spectral solver (Phase 1, Gate 1a)",
     "validated": ("dedicated: test_boussinesq_dedicated.py (17 checks) + "
                   "test_solver_boussinesq.py; odd-n derivative path checked correct "
                   "-- and now ALSO hardened against malformed input. Leg 89's 90-case "
                   "adversarial battery measured 19 of 82 gate-deciding cases silently "
                   "returning a plausible-looking wrong result; it is 0 of 82 (and 0 of "
                   "8 secondary) after the bench repair, with conservation_drift masking "
                   "a NaN limb in 0 of 90 rather than 13 of 90. Four defects closed: a "
                   "false blowup_candidate off a roundoff-level represented m0 (the "
                   "exact-zero omega0 guard is now scale-aware at 1e-13 x the state "
                   "scale), nu/kappa outside [0,inf) neither applied nor rejected (now "
                   "validated at entry -- the energy identity structurally cannot see "
                   "kappa, so no guard could ever have caught it), builtin max/min "
                   "dropping a NaN limb (now NaN-propagating, with a non-finite drift "
                   "reported as early_exit_reason='nonfinite_drift'), and a one-mode "
                   "degenerate grid plus non-finite detection thresholds. NO BANKED "
                   "PHASE-1 RESULT IS AFFECTED: all 5 call sites pass kappa=0.0, no "
                   "banked artifact records a solve_boussinesq blowup_candidate, and "
                   "phase1_spike.json's N=128 column reproduces exactly (4/4, worst "
                   "diff 0.0) -- see writeup/data/bench_boussinesq_silent_corruption_"
                   "check.json and test_boussinesq_adversarial.py"),
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
     # Leg 292 (Route-CAPA, the second-generation self-audit): this `test` field was
     # `test_first_integral.py`, a file containing zero occurrences of this module's name,
     # which therefore could not fail when the module broke -- the only such row of 48, and
     # the same defect leg 71 measured here at e203b52 and could not then repair.
     # test_finite_support_adversarial.py (leg 124, 1424da6) is the file that actually
     # loads the module; it is green at HEAD (30s), and its gate S10 re-checks the exact
     # property this `validated` field claims -- "zero importers, and the SUPERSEDED /
     # DO NOT USE banner is intact". It sat on disk, cited by NO row, for ~220 legs.
     # Factual `test`-field correction only; `validated` left frozen.
     # Do NOT write this module's stem and the word imp/ort on one line anywhere in the
     # tree: leg 124's S10 greps for that pair and a comment is indistinguishable from a
     # real importer to it. That is measured -- an earlier draft of this note turned the
     # test red, which is how a documentation comment became a test failure.
     "test": "test_finite_support_adversarial.py"},
    {"module": "solver/interval_mp.py",
     "object": "arbitrary-precision interval arithmetic (leg 312, Route-APIA)",
     "holds": ("decimal.Decimal-backed rigorous MPInterval (directed-rounding "
               "+ - * /, isum/dot, Taylor sin/cos/atan/pi with proved remainders) "
               "for pointwise-cancellation regimes float64 cannot resolve, plus "
               "flagged-non-rigorous banded Cholesky / banded triangular inverse "
               "/ banded matmul exploiting exact bandwidth-4 Gram structure"),
     "validated": ("test_interval_mp.py, 13/13: dsin/dcos/atan/pi checked against "
                   "an independent fractions.Fraction Taylor reference and a "
                   "65-digit pi string (caught 3 real bugs -- an atan recurrence "
                   "missing a ratio factor, bare abs()/negate silently rounding to "
                   "the ambient 28-digit decimal context, Decimal(1)/Decimal(239) "
                   "computed outside any explicit context -- all fixed); banded "
                   "linear algebra checked against exact Fraction arithmetic on "
                   "random banded SPD matrices; leg 178's own theta~3e-31 regime "
                   "directly tested"),
     "test": "test_interval_mp.py"},
    {"module": "solver/dssp_basis.py",
     "object": "enriched compactified basis for the DSSP boundary block (leg 350, "
               "Route-DSSP brick B2)",
     "holds": ("log-compactification u=-log(1-X) plus a fixed Boyd algebraic map "
               "v=u/(u+L) that carries the (1-X)^{1-i*kappa} far-field defect leg "
               "313 measured at X=1 into an entire exponential-times-oscillation "
               "function of u, then a finite Chebyshev-Lobatto/FFT basis on v; "
               "boundary_block/boundary_block_v, modes_for_rel_tol, the smooth "
               "control carried through the same map for falsification"),
     "validated": ("plain-X baseline reproduces leg 313's own banked table exactly "
                   "(823/1482/3564/7086/14149 modes at kappa=1/2/5/10/20 for 1e-6 "
                   "relative truncation; smooth-control separation 82.3x); the "
                   "enriched basis, ONE fixed map scale L=16 shared across every "
                   "kappa row, resolves the same target at 32/54/126/249/496 modes "
                   "-- a 25.7x-28.5x enrichment factor, stable to the mode across "
                   "an 8x resolution range (16384..131072). FALSIFICATION CONTROL: "
                   "the same map applied to leg 313's smooth positive control (no "
                   "boundary singularity) costs MORE modes (31 vs 10 direct), so "
                   "the enrichment is not a universal transform artefact"),
     "test": "test_dssp_basis.py"},
    {"module": "solver/dssp_biot_savart.py",
     "object": "3D Biot-Savart velocity recovery from a Type-I-enveloped "
               "vorticity witness, closed-form (leg 351, Route-DSSP brick B3)",
     "holds": ("Omega_B=2S(r)(-x2,x1,0), S(r)=(1+r^2)^-3/2 (algebraic, not "
               "Gaussian); u_B=curl A solves -Laplace A=Omega_B via the "
               "swirl ansatz A=a(r)(x2,-x1,0); a(r), a'(r), a''(r) are ALL "
               "closed-form (no quadrature, no interpolation table -- a(r) "
               "= -2G4(r)/(3r^3) - (2/3)/sqrt(1+r^2), derived by two "
               "integrations by parts of the ODE a''+4a'/r=2S(r)); "
               "vorticity_nonlinearity(u,w,Ju,Jw) for the mapping-bound "
               "numerator"),
     "validated": ("div u_B=0 and curl u_B=Omega_B to <1e-10 analytically "
                   "(no finite differences -- grad_uB/grad_omegaB depend "
                   "only on the closed forms); a(0)=-2/3 exactly, a(r)*r -> "
                   "-1 as r->infinity (Type-I decay, solved not assumed); "
                   "||Omega_B||_L2(R^3) matches an independent closed form "
                   "pi*sqrt(2) (Beta-function integral) to 3.8e-6 rel; "
                   "unweighted-L2 mapping-bound ratio actual/bound = "
                   "0.1952037, stable to 5 sig figs across both a 3-point "
                   "resolution ladder and a 5-point domain ladder "
                   "(R_hi 50..1e5, needed because this tail is algebraic "
                   "not Gaussian); FALSIFICATION CONTROL: a deliberately "
                   "wrong vorticity (Omega_B*1.01) fails the curl check by "
                   "~7.6e-3, confirming the check is not vacuous"),
     "test": "test_dssp_biot_savart.py"},
    {"module": "solver/dssp_step.py",
     "object": "rescaled-vorticity time-stepper, single-mode Galerkin "
               "truncation onto leg 351's closed-form witness (leg 354, "
               "Route-DSSP brick B4)",
     "holds": ("Galerkin projection of the true rescaled vorticity equation "
               "d_sOmega+Omega+(1/2)(y.grad)Omega+(V.grad)Omega-(Omega.grad)V"
               "=DeltaOmega onto Omega=c(s)*Omega_B, V=c(s)*u_B, giving the "
               "scalar ODE c'=alpha*c+beta*c^2 with alpha=-(1/4+G/M), "
               "beta=-N/M computed by 3D spherical quadrature; "
               "galerkin_coefficients, rk4_step/integrate_rk4 (the actual "
               "stepper), closed_form_c/blowup_time (the Riccati exact "
               "solution used to verify the stepper)"),
     "validated": ("quadrature M matches leg 351's OWN independent closed "
                   "form ||Omega_B||_L2^2=2*pi^2 to <1e-8 relative; alpha "
                   "converges to the exact rational -19/16 across 4 "
                   "resolution/domain settings (rel spread <1e-7); N/M is "
                   "machine-zero (~1e-15, an exact y3-parity identity, not "
                   "an accident) so beta=0 and the mode decays exactly "
                   "linearly; RK4 stepper reproduces the closed-form decay "
                   "c(s)=c0*exp(alpha*s) to <1e-6 rel inside the PRE-STATED "
                   "window S_max=5, n_steps=2000, decaying to 0.26% of c0; "
                   "FALSIFICATION CONTROL: a planted confinement-sign-flip "
                   "bug (alpha_bug=13/16>0, same c0, same window) makes the "
                   "identical initial data GROW 58x instead of decaying, "
                   "confirming the relaxation-to-trivial check is not "
                   "vacuous; a second synthetic-ODE control confirms the "
                   "integrator's own divergence-stop fires within one "
                   "step-width of a known finite blowup time"),
     "test": "test_dssp_step.py"},
    {"module": "solver/kolmogorov2d_nkbasin.py",
     "object": "2D Kolmogorov flow: pseudospectral DNS + matrix-free Newton-Krylov "
               "RPO solver (leg 353, Route-DSSP brick B5)",
     "holds": ("Kolmogorov2D (vorticity-streamfunction pseudospectral DNS, RK4 + "
               "exact viscous integrating factor, 2/3-rule dealiasing); shift_x "
               "and optimal_shift_residual (FFT cross-correlation recurrence-flow "
               "search, x-translation symmetry); a from-scratch matrix-free GMRES "
               "(gmres_matrix_free, no scipy); newton_krylov_rpo (Newton + "
               "phase-condition moving Poincare section, plain-Newton line search, "
               "NOT the paper's hookstep); measure_basin_radius"),
     "validated": ("laminar profile w_lam=-(Re/n)cos(n y) is an exact fixed point "
                   "of rhs_physical to ~7e-15 and integration-invariant to <1e-3 "
                   "relative drift over T=1; energy-balance dE/dt vs I-D matches to "
                   "1.4%; shift_x is a group action (identity at s=0, band-limited "
                   "field, avoids a Nyquist aliasing artefact under full-band "
                   "noise); optimal_shift_residual recovers a synthetic shift_x-"
                   "constructed pair to rel=3.4e-3 -- catching and fixing a genuine "
                   "SIGN BUG (the FFT cross-correlation peak sits at j=-s, not "
                   "+s; every recurrence-search candidate before this fix carried "
                   "a wrong-signed shift guess); gmres_matrix_free matches "
                   "np.linalg.solve on a small dense system to 2.9e-16 relative; "
                   "newton_krylov_rpo reduces the extended residual 99.3%, "
                   "monotonically, from a 1% perturbation of the exact laminar "
                   "fixed point (the control leg 353's gate verdict rests on: the "
                   "solver itself is not broken). GATE RESULT (leg 353, sign-"
                   "corrected run, T_total=2000 DNS, N=24, Re=60, n=4): all 5 "
                   "Newton-Krylov attempts at Lucas-Kerswell 2015 (arXiv:1406.1820) "
                   "Table IV published RPOs (UPO37 x2, UPO35, UPO9, UPO22), seeded "
                   "from the best recurrence-search candidates (relative seed "
                   "residual 0.18-0.26), FAILED to converge (reason="
                   "line_search_failed in every case, final |R| in [22.5, 29.5], "
                   "no attempt got within two orders of magnitude of tol=1e-8) -- "
                   "basin radius NOT MEASURED (nothing converged to perturb). See "
                   "writeup/data/p2_route_dsspb5_v1.json, writeup/figures/"
                   "fig94_route_dsspb5_v1_stall.png, experiments/journal/"
                   "leg_353.md"),
     "test": "test_kolmogorov2d_nkbasin.py"},
    {"module": "solver/dssp_screen.py",
     "object": "admissibility screen for DSSP candidates: L3(R^3) norm, "
               "fitted far-field decay exponent, lambda-from-trajectory, "
               "axisymmetry diagnostic, and a machine-read rigidity "
               "ledger (leg 357, Route-DSSP brick B7)",
     "holds": ("l3_norm_ladder (spherical-quadrature shell ladder in R_hi, "
               "converged flag on relative change of the last step); "
               "fitted_far_field_decay_exponent (log-log fit on a generic "
               "off-axis ray); lambda_from_trajectory (S0=2*log(lambda) "
               "period detection on a c(s) trajectory, or UNDEFINED if the "
               "trajectory relaxes to the trivial state); "
               "axisymmetry_residual (cylindrical-component spread over "
               "phi, normalised by the ring's own field magnitude); "
               "ledger_nrs_tsai/ledger_chae_tsai/ledger_pineau_vicol/"
               "machine_read_ledger (parse legs 326/330's landed JSON "
               "clause fields programmatically, not transcribed prose); "
               "screen_candidate (end-to-end orchestration). LEG 362 "
               "EXTENSION (backward-compatible, additive): "
               "decays_to_zero_at_infinity (Tsai 1998 Theorem 2's "
               "finishing-step hypothesis, 'U -> 0 at infinity', p.49, "
               "strictly weaker than L^q membership); classify_ss_ansatz "
               "(exact-SS vs DISCRETELY-self-similar-at-lambda>1, driven "
               "off lambda_from_trajectory's own measurement); "
               "ledger_nrs_tsai(l3_result, decay_result=None, "
               "ansatz_result=None) now optionally returns a THREE-WAY "
               "verdict -- EXCLUDED-BY-T1 / EXCLUDED-BY-T2 / "
               "NOT-REACHED-BY-ANSATZ -- when both optional args are "
               "supplied; omitting them (every leg-357 call site) "
               "reproduces the original two-way EXCLUDED/NOT-EXCLUDED "
               "reading byte-for-byte"),
     "validated": ("leg 351's Type-I witness (u_B ~ C/|x|) correctly "
                   "diverges under l3_norm_ladder (shells stay ~constant "
                   "per decade, not shrinking -- log-divergence "
                   "signature) and fits to decay exponent -0.997 "
                   "(expected -1); its swirl-ansatz axisymmetry residual "
                   "is 7.9e-16, and a PLANTED non-axisymmetric control "
                   "(explicit x1-term) is detected at residual 1.0 -- "
                   "diagnostic is not vacuous; a normalisation bug caught "
                   "during construction (dividing near-zero V_phi "
                   "roundoff by its own near-zero scale gave a false-"
                   "positive residual of 2.0) is fixed and pinned by a "
                   "regression test; lambda_from_trajectory correctly "
                   "reports UNDEFINED on leg 354's own landed decaying "
                   "trajectory and correctly detects a synthetic periodic "
                   "control's lambda to within 3.2% of exp(S0/2); "
                   "ledger_chae_tsai/ledger_pineau_vicol reproduce legs "
                   "326/330's landed verdicts (SILENT; lambda ceiling "
                   "1.6487212707001282) by JSON parse; ledger_nrs_tsai "
                   "correctly EXCLUDES leg 332's own landed L3=0.7307683991070311 "
                   "measurement (read from its JSON, not retyped) while "
                   "NOT excluding this family's divergent witness -- the "
                   "gate's own no-branch warning, demonstrated concretely. "
                   "LEG 362 (Route-B7X, closes leg 359's flagged gap, "
                   "writeup/data/p2_route_b7x_v1.json): all three gate "
                   "controls pass -- (1) a planted synthetic exact-SS "
                   "decay=-1 candidate (Tsai's own headline example) reads "
                   "NOT EXCLUDED under the old L3-only reading and "
                   "EXCLUDED-BY-T2 under the extended reading, "
                   "demonstrating leg 359's flagged gap then closing it; "
                   "(2) this repo's real DSS object (field_uB + a "
                   "genuinely periodic lambda=2.634>1 trajectory) reads "
                   "NOT-REACHED-BY-ANSATZ, citing Tsai 1998 eq (1.2)'s "
                   "exact-SS ansatz as the deciding clause; (3) leg 357's "
                   "banked writeup/data/p2_route_dsspb7_v1.json verdicts "
                   "reproduce with ZERO mismatches (diff-checked entry by "
                   "entry, only the worktree path and runtime_seconds "
                   "differ, both environment-dependent). "
                   "LEG 370 (Route-B7M, implements leg 368's WIDENS finding, "
                   "writeup/data/p2_route_b7m_v1.json): a THIRD ledger "
                   "entry, morrey_ball_average_sweep()/ledger_morrey(), "
                   "operationalizes arXiv:2006.15776 (Jiu-Wang-Wei) Theorem "
                   "1.2 -- U in M-dot_{q,1}(R^3), 3/2<q<6 ==> U==0 -- as a "
                   "ball-averaged L^1-mass sweep over the SAME shell ladder "
                   "l3_norm_ladder() uses, reusing _spherical_shell_nodes() "
                   "directly; the ansatz gate (Tsai eq (1.2)_1, exact-SS "
                   "only) is checked FIRST, exactly as for T1/T2; "
                   "machine_read_ledger()'s new morrey_result parameter "
                   "defaults to None and is OPT-IN (adds a 'Morrey' key "
                   "only when explicitly supplied alongside ansatz_result), "
                   "so every pre-existing call site's return-dict key set "
                   "is byte-for-byte unchanged. All three gate controls "
                   "pass -- (a) a planted synthetic exact-SS profile with a "
                   "narrow angular*radial bump on the sampled ray evades "
                   "BOTH T1 (L^3 stays genuinely log-divergent, angularly "
                   "narrow bump) and T2 (pushes the last sampled magnitude "
                   "above the first), reading NOT EXCLUDED under T1/T2 "
                   "alone and EXCLUDED-BY-MORREY once the new entry is "
                   "wired in, demonstrating leg 368's WIDENS gap then "
                   "closing it; (b) the real DSS object (field_uB + a "
                   "genuinely periodic lambda>1 trajectory) reads "
                   "NOT-REACHED-BY-ANSATZ under Morrey too, matching T1/T2; "
                   "(c) legs 357's and 362's banked JSON files are "
                   "byte-identical before/after (untouched, sha256-hashed) "
                   "and their own ledger-bearing verdict fields reproduce "
                   "in-process with ZERO mismatches. Operational scope, "
                   "STATED not silently assumed: sup_x is evaluated at "
                   "x=0 only (not the theorem's literal sup over all x in "
                   "R^3) and sup_R over a finite ladder swept across a "
                   "finite grid of q in the open interval (3/2,6) -- a "
                   "genuine at-resolution numerical test, not an "
                   "exhaustive one. "
                   "LEG 383 (Route-ST2G, writeup/data/p2_route_st2g_v1.json): "
                   "the two columns are now UNCONDITIONAL IN THE REPORT PATH. "
                   "Legs 362/370 landed them opt-in, so screen_candidate() -- "
                   "the single end-to-end path producing a candidate report -- "
                   "computed the far-field decay exponent, dropped it, called "
                   "machine_read_ledger(l3, lam) with two positional args, and "
                   "never computed the ansatz classification at all; leg 359's "
                   "flagged mis-classification therefore stayed live in the "
                   "report path. Re-measured on main at 104f5b3: a planted "
                   "exact-SS field at fitted exponent -1.0000000000000002 with "
                   "a log-divergent L^3 ladder (rel_change_last_step 0.1305 vs "
                   "tol 1e-4) was reported NOT EXCLUDED. screen_candidate() now "
                   "computes decays_to_zero_at_infinity() and "
                   "classify_ss_ansatz() on every call, passes both into "
                   "machine_read_ledger(), and returns them as top-level "
                   "'theorem2_decay_to_zero' and 'ss_ansatz' columns; "
                   "machine_read_ledger()'s own signature and defaults are "
                   "UNTOUCHED (leg 357's two-arg shape and leg 370's opt-in "
                   "Morrey key both still hold), and screen_candidate()'s "
                   "ledger key set is unmoved. Six PRE-REGISTERED planted "
                   "controls (writeup/novelty/leg_383.md, committed at 1ca4ce5 "
                   "BEFORE construction), all passing, THREE OF WHICH MUST "
                   "STAY SILENT so the instrument is not a tautology (leg 340): "
                   "C1 Tsai's headline example eq (1.5), fitted exponent "
                   "-1.0000000000000002 vs the source's exact -1 (|diff| "
                   "2.22e-16) -> EXCLUDED-BY-T2; C2 the repo's DSS object "
                   "(field_uB + periodic lambda=2.691234472349262) -> "
                   "NOT-REACHED-BY-ANSATZ citing Tsai eq (1.2)_1; C3 planted "
                   "exponent -2.0000000000000004, L^3 genuinely convergent "
                   "(rel_change_last_step 0.0) -> EXCLUDED-BY-T1, so T1 and T2 "
                   "are distinguishable; C4 a field rising to a NONZERO limit "
                   "(|U| 0.954545 -> 0.999500, exponent +0.008377) -> NOT "
                   "EXCLUDED, the anti-tautology control; C5 a static "
                   "non-periodic candidate -> ansatz EXACT-SS, satisfies=True, "
                   "NOT deflected to NOT-REACHED-BY-ANSATZ, so C2's verdict is "
                   "not vacuous; C6 a field GROWING like |y| (exponent "
                   "+1.0000000000000002) -> NOT EXCLUDED with no clause "
                   "claimed. All four verdicts are reachable through the report "
                   "path. CEILING: TIER 2 -- surviving this screen means only "
                   "'not already excluded by a published theorem reachable on "
                   "this repository's record', which is NOT evidence for "
                   "existence. The six controls live in their own self-running "
                   "battery, test_dssp_screen_t2.py (8/8), alongside leg 357/"
                   "362/370's test_dssp_screen.py (23/23), which is the file "
                   "this row's 'test' field names"),
     "test": "test_dssp_screen.py"},
    {"module": "solver/dssp_decay_enclosure.py",
     "object": ("CERTIFIED far-field decay exponent enclosure (leg 382, Route-DEXC) -- "
                "the instrument CLAY_OBLIGATIONS.md §4 asks for and §6 item 1 records "
                "as missing; does NOT replace dssp_screen's fitted column, which is "
                "left in place and recorded alongside"),
     "holds": ("an OUTER enclosure of P_cert = { p >= 0 : exists C > 0 with "
               "C r^-p = f(r) for ALL r in [R0,R1] }, computed by exact "
               "Fourier-Motzkin elimination of the amplitude from an interval-enclosed "
               "log-log tube, on solver/interval.py's Interval/ilog substrate (the one "
               "new primitive is isqrt, used only by the planted-profile generator). "
               "Three verdicts: INTERVAL, EMPTY (a PROOF that no exponent in the search "
               "bracket fits), INCAPACITY (bracket-limited, or profile enclosure touching "
               "zero). Two modes: 'cells' (whole-cell interval evaluation, statement "
               "covers the entire window) and 'nodes' (STRICTLY WEAKER, node-consistency "
               "only, reference use). Optional rel_tolerance delta relaxes to "
               "consistency within a stated relative accuracy the CALLER owes"),
     "validated": ("test_dssp_decay_enclosure.py, 12/12. Exact power laws p0 = 0.5, 1, "
                   "2, 2.5, 3 enclosed at N = 17/50/200/1000 in both modes; at the "
                   "leg-382 window [10,1000] and N=1000 the certified widths are "
                   "7.44e-15 (p0=1), 1.60e-14 (2), 2.00e-14 (2.5), 1.55e-14 (3), all "
                   "containing the exact truth, none reaching the [0,12] bracket. "
                   "Planted mismatches certified EMPTY with contradiction gaps: "
                   "two-power r^-2+0.01r^-1 (crossover INSIDE the window) 0.8174, "
                   "rational cutoff r^-2/(1+(r/300)^4) 3.9670, log correction 0.2448, "
                   "curvature kappa=1e-4 8.79e-4. MEASURED LIMIT, not hidden: at "
                   "delta=0 the set is EMPTY for ANY perturbation down to eps=1e-12 "
                   "(correct -- a perturbed power law has no exact exponent -- but it "
                   "means the zero-tolerance instrument cannot be applied to numerical "
                   "data). Under tolerance the width obeys ~= 0.8686*delta and the "
                   "critical tolerances separating mismatch from known are delta* = "
                   "0.3157 (two-power), 3.353 (cutoff), 0.0697 (log), 0 (exact). "
                   "p0=13 under bracket [0,12] returns INCAPACITY, not EMPTY. CEILING: "
                   "validated on PLANTED ANALYTIC KNOWNS ONLY -- no profile of route 4's "
                   "object exists, and the admissible-cutoff half of §4 is untouched, so "
                   "CLAY_OBLIGATIONS §6 item 1 does NOT close"),
     "test": "test_dssp_decay_enclosure.py"},

    {"module": "solver/dssp_decay_samples.py",
     "object": ("SAMPLES -> CERTIFIED CELL ENCLOSURES (leg 385, Route-SCEL) -- the input "
                "contract solver/dssp_decay_enclosure.py:354 NAMES and does not supply, so "
                "that a unit holding point samples can reach the §4 certified-decay "
                "instrument at all. Reads leg 382's module; edits it nowhere"),
     "holds": ("samples_to_cells(r, f | f_lo/f_hi, monotone=, modulus=) returning cell "
               "enclosures valid for EVERY r in each cell under a NAMED hypothesis, plus "
               "certified_decay_from_samples() which composes with leg 382's "
               "certified_decay_from_cell_enclosures and MERGES the hypothesis into its "
               "output row. Two paths: MONOTONE (declared nonincreasing/nondecreasing; the "
               "sample pair IS the enclosure, exact) and MODULUS (caller-certified "
               "omega(h)=L*h^alpha, alpha in {1/2,1}, kind 'absolute' or 'loglog', scalar or "
               "per-sample L; enclosure = sample hull inflated by omega(h/2)). Both may be "
               "declared and are then INTERSECTED. The loglog kind needs no iexp: it closes "
               "with e^-x >= 1-x and e^x <= 1/(1-x), outward, refusing omega >= 1. An input "
               "carrying NEITHER hypothesis returns INCAPACITY and leg 382's routine is "
               "never called -- there is no code path producing an exponent without a "
               "hypothesis attached. Necessary conditions (monotone samples; "
               "|delta| <= omega(h)) are checked and a CERTAIN violation refuses naming the "
               "cell. containment_audit() is a float64 VALIDATION device for planted knowns "
               "only, never part of a certificate"),
     "validated": ("test_dssp_decay_samples.py, 17/17; experiments/p2_route_scel_v1.py, "
                   "fig103, writeup/data/p2_route_scel_v1.json. PATH A reproduces leg 382's "
                   "four banked exact-power widths BIT-IDENTICALLY on [10,1000] N=1000 "
                   "(difference exactly 0.0 at K1 7.438494264988549e-15, K2 "
                   "1.5987211554602254e-14, K3 1.9984014443252818e-14, K4 "
                   "1.554312234475219e-14), truth inside every interval, because a monotone "
                   "profile's cell extremes sit at the sampled edges. PATH B is SOUND BUT "
                   "NOT TIGHT: loglog L=1.05 gives width 2.1046e-3 at N=1000 containing the "
                   "truth, slope -1.0068 (PATH A -0.0118), so matching PATH A would need "
                   "N ~ 2.83e14 -- THE MODULUS PATH CANNOT REPRODUCE 382's WIDTHS AT ANY "
                   "FEASIBLE DENSITY, predicted before the run. A GLOBALLY stated 'absolute' "
                   "modulus is useless on a 3-decade window: L=0.03 (the true global "
                   "Lipschitz constant) drives the lower enclosure non-positive from "
                   "r=207.97 in 341/1000 cells and leg 382 then answers INCAPACITY. Five "
                   "controls all fired, none widened: X1 no-hypothesis and X2 visible "
                   "non-monotonicity (cell 499, +1.3615e-3) and X4 modulus understated at "
                   "the samples (ratio 20.0) REFUSE; X3 secretly non-monotone (node-aligned "
                   "wiggle A=0.05) and X5 undetectably understated modulus are ACCEPTED AS "
                   "THEY MUST BE and caught by containment failures of +5.1420e-2 relative "
                   "(1000/1000 cells) and +4.7721e-2 in log f. X3's certificate is width "
                   "7.438494264988549e-15 -- numerically indistinguishable from K1's TRUE "
                   "one and FALSE about its profile; only the recorded hypothesis separates "
                   "them. Pre-registered P11 (a shifted grid detects the wiggle) was "
                   "REFUTED and recorded: a uniform shift multiplies every sample by one "
                   "constant, so detection is a COMMENSURABILITY effect (N=1100/1500 refuse, "
                   "N=500/997/1001/1010/2000 do not). CEILING: validated on PLANTED ANALYTIC "
                   "KNOWNS ONLY -- no profile of route 4's object exists, every certificate "
                   "is CONDITIONAL on a declared and unverifiable hypothesis, and "
                   "CLAY_OBLIGATIONS §6 items 1 and 2 stay OPEN with item 1's "
                   "admissible-cutoff half untouched"),
     "test": "test_dssp_decay_samples.py"},
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
