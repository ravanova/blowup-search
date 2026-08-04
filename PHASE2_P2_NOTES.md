# Phase-2 P2 working notes — the lottery-ticket leg (1D Hou–Luo singular profiles)

Status as of 2026-07-25. Newest context on top. This is the working doc; the banked
record is writeup/4_p2_lottery/TECHNICAL_P2_HL_ANCHOR.md + BLOG_P2_HL_ANCHOR.md + fig12 (rebuilds from
committed writeup/data/p2_hl_anchor.json via `python writeup/4_p2_lottery/p2_hl_anchor_evidence.py`).

## TOP STATUS — anchor DONE (§2); HH23 scout DONE (§5, NO-GO on the literal link); dynamic-
## relaxation leg DONE (§6, Conjecture-2.4 LOCAL attractor confirmed at POC, global basin not —
## PARTIAL/Tier-2). REGULAR-PROFILE REFRAME DONE (§7, 2026-07-25 scout): the §6 "generic → a
## DIFFERENT state" that we filed as an honest NEGATIVE is actually a REGULAR, strictly-positive
## profile = CHL's Stage-1 / Scenario-2 object (qualitatively) — NOT a POC artifact. The scout also
## SCOPED the fork: B1 (implement CHL's modified (4.1)/(4.2) to pin the regular profile; cheap,
## clean known-answer) is the recommended next brick; B2 (the Stage-1→Stage-2 transition) is NOT
## reachable on a fixed grid and mostly re-confirms CHL. **B1 DONE (§8, 2026-07-26): implemented
## CHL's (4.1)/(4.2), logged run 5/5 PARTIAL — the invariant exponent c_l/c_ω → −2.533 (CHL
## −2.5114) as a genuine IC-independent attractor to a regular positive profile; res floors ~2e-2,
## absolute triple normalization-dependent.** **GA FRAMEWORK DONE (§9, 2026-07-26): built + validated
## the GLOBAL-search infrastructure for the gCLM two-scale↔two-stage probe — the gCLM `a`-family
## rescaled residual (solver/gclm_family.py) + a generic GA engine (solver/ga_search.py); a=0
## one-scale known-answer gate PASSES (residual 2.2e-7; GA recovers the exact steady DILATION FAMILY,
## invariant A²/B=4); diagnostic LOCKED. Validated tooling, NOT a science result.** **TWO-SCALE
## a-SWEEP DONE + LOGGED (§9, 2026-07-26): derived the two-scale residual R₂=ΩHΩ−c_tw Ω_X−a U Ω_X
## (HQW25's moving-frame ansatz → leading order = a PURE TRAVELING WAVE; a=0 anchor Ω₂=−1/(1+X²)
## nulls to 1.5e-9, c_tw=1/2), locked predicate T1–T6, logged GA sweep 5/6 PARTIAL. Result: HQW25's
## exact a=0 two-scale traveling wave DEFORMS SMOOTHLY under advection — persists (relres<1e-2) to
## a_p≈0.40, floor rises to 0.18 at a=1 (De Gregorio), STAYS EVEN, no sharp collapse. T4 FAIL (honest):
## mid-range floor is partly GENOME-LIMITED (K=3 cuts a=0.5 floor 4×) → genome-relative upper bound,
## survival boundary not sharply pinned; BUT a=1 degradation robust to K=3. NOVEL toy-model result
## (Tier-1/2), NOT a proof, NOT a Clay solve.** **a_p(K) CONVERGENCE MAP DONE + LOGGED (§9-cont2,
## 2026-07-26): SHARPENS that T4 FAIL. Added even_lorentz_sq cross-check basis (+test, 12/12); a
## pre-run plateau scout caught that near-transition floors are SEARCH-limited at the old budget
## (a=0.6 K4 drops 45% at 2× budget) → fixed budget pop150/gen250/8seeds (converged) + in-JSON
## budget/K6 spot-checks. Locked T1–T7 (commit 44a507c), logged 7/7. RESULT: a_p(K)=0.40→0.50→0.50
## SATURATES; boundary a*≈0.5–0.55 is GA-converged (K4 1.7×-budget within 5%), genome-converged (K6
## does NOT beat K4), and BASIS-independent (mixed Lorentzian+squared within 3× of K3); far-end
## robust (K4 floor 1.28e-1 at a=1); resolution fine (min 35 pts). Honest nuance: a* is a SOFT
## crossing (bases straddle 1e-2 at 0.55), not a razor edge. The T4 "soft boundary" caveat is now a
## converged, genuine feature — NOT genome-limited. Still Tier-1/2, NOT a Clay solve.** Read
## §5→§6→§7→§8→§9→§9-cont2→§10→§11→§12→§13→§14.
## Not novel-enough-to-be-a-proof; a genuine (now convergence-guarded) map.
## **ROUTE-D v1 DONE (§10, 2026-07-26): interval core + a=0 NK framing. Level-1 tooling + scoping, NOT a
## certificate.** Built solver/interval.py (hand-rolled rigorous interval arithmetic, +test 5/5, suite now
## 8 files green) + the deterministic a=0 probe (experiments/p2_route_d_probe.py → fig19). FOUR results:
## Q1 the interval enclosure carries the NK defect Y₀ (overhead ~10%); Q2 the a=0 zero set is a 2-param
## scaling valley → EXACTLY 2 gauge conditions isolate a nondegenerate zero (naive ‖DF⁻¹‖=∞); Q3 under
## X=tan(θ/2) the line Hilbert = circular conjugate (cos kθ↦sin kθ, ~1e-7), anchor = 2-term Fourier;
## Q4 ⇒ DF is TRIDIAGONAL + rank-1 (cos→sin), so finite-section Z₀+Z₁<1 is PLAUSIBLE. Framing =
## radii-polynomial NK; F quadratic ⇒ Z₂ constant. Open risks G(gauge/index)/R(θ=±π endpoint)/T(tail)/
## a≠0(no exact anchor off 0). BLOG/TECHNICAL_P2_ROUTED.md.
## **ROUTE-D v2 DONE (§11, 2026-07-28): the FLOAT DRESS REHEARSAL — the NK ball does NOT close, and CANNOT
## (0/13 on N=4..256; at any N, any gauge, any weight). Cause ISOLATED BY ABLATION: the transport term
## c(1+cosθ)∂_θ degenerates at θ=±π (X=∞) — replace (1+cosθ)→1 and ‖A_N‖ goes flat at 4.0 vs N^0.97.
## Sub-task G (gauge) EXONERATED, sub-task R (far field) promoted to blocker. Certification budget
## Y₀^max ≡ 0 at every N. CONSTRUCTIVE HALF: the inverse loses EXACTLY one power of decay (‖A e_m‖≈1.97m,
## predicted by the far-field ODE), so grading the codomain by one mode power gives ‖A‖=3.000 FLAT in N —
## the asymmetric space pair a working certificate must use. New solver/nk_fourier.py + test_nk_fourier.py
## (6/6; suite 9 files green); fig20; BLOG/TECHNICAL_P2_ROUTED_DRESS.md. Level-1 tooling + a structural
## negative, NOT a certificate.**
## **ROUTE-D v3 DONE (§12, 2026-07-30): the SPACE-PAIR NO-GO. v2's own repair is RETIRED, and with it the
## WHOLE weighted-ell^1 category: the two NK requirements are separated by exactly one grading power and the
## separation is CONSERVED (||A_N|| ~ N^(1-g), S_K ~ K^g with g=t-s; min exponent sum over the entire family
## = 0.98, must be 0). Control (1+cos->1): min sum 0.00, boundary falls by TWO powers = the order 1+cos
## vanishes to. Root cause reframed: a diagonal weight measures SMOOTHNESS, not DECAY (cos k(pi) = +-1 never
## decays). POSITIVE HALF: DECAY-graded spaces satisfy BOTH (H(h) ~ (int h)/(pi X) => hH(h) gains one power),
## the far field is RESONANT at alpha=2 = the anchor's own decay = the homogeneous solution
## (||L^-1|| = 2/|alpha-2| to 0.008%), and detuning has an INTERIOR OPTIMUM alpha* ~ 1.44 => certify
## X^-3/2 profiles with X^-5/2 residuals, Z2 ~ 13, budget ~1e-2 (thin). New solver/decay_grading.py +
## test_decay_grading.py (7/7; suite 10 files green); fig21; BLOG/TECHNICAL_P2_ROUTED_SPACES.md. Level-1
## tooling + a no-go theorem, NOT a certificate.**
## **ROUTE-D v4 DONE (§13, 2026-07-30): the FULL operator in the decay-graded pair, in a THIRD independent
## discretization (nodal spectral collocation + weighted sup norms). TWO results. (a) v3's far-field pricing
## SURVIVES contact with the full gauged operator: the model law 2/|a-2| predicts ||A|| to 6% on a in
## [1.4,1.7] (2% on [1.5,1.7]), Z2_min = 13.4 at a~1.5 vs v3's predicted 13.3 at 1.44 — the compact core
## costs almost nothing — and the full ||A|| has its OWN interior minimum at a~1.40 (far-field price rises
## toward a=2, core price toward a=1). (b) BUT the decay-graded SUP pair does NOT control the quadratic: H is
## unbounded on L^inf, shown with the conjugate-extremal square-wave family (C_Q grows +0.41/e-fold), while
## RANDOM sampling FALLS and would have reported it bounded. UNIFIED STATEMENT: v3 = a diagonal weight
## measures smoothness, we needed decay; v4 = a sup norm measures decay, we also need smoothness. The
## certificate space must carry BOTH gradings; no one-parameter family does. New solver/decay_collocation.py
## + test_decay_collocation.py (6/6; suite 11 files green); fig22; BLOG/TECHNICAL_P2_ROUTED_V4.md. Level-1
## tooling + scoping, NOT a certificate.**
## **ROUTE-D v5 DONE (§14, 2026-07-30): the TWO-GRADING SPACE (decay x smoothness). v4's obstruction is
## REMOVED: the square-wave adversary that broke the sup pair is DEFUSED for gamma >= 0.35 (Holder ratio
## x0.83 at gamma=0.5 vs sup x2.26), the quadratic constant drops to <1 and its adversary growth falls below
## 1, and C_H(gamma) BOWLS (min 1.12 at gamma~0.35) so SMOOTHNESS has its own interior optimum -- the same
## shape decay has (v4: ||A|| bowls at alpha~1.4). Z2 = 3.29 vs v4's 13.4; budget ceiling 7.6e-2 vs 1.9e-2.
## ONE MARGINAL DIRECTION LEFT: at the codomain's CRITICAL decay rate the inverse creeps logarithmically
## (J^+0.14), while every delta>0 saturates to 4 s.f. across 16x in J -- v3's resonance one level down, same
## fix (keep the residual class OPEN), and this time the detuning is nearly FREE (costs go DOWN with delta,
## because it tightens the codomain rather than loosening the domain). The seminorm weight is alpha-gamma NOT
## alpha (forced by the exact Jacobian dX/dth=(1+X^2)/2; with alpha the profile f_alpha itself has infinite
## seminorm -- the numerical conformal check caught this). New solver/holder_norms.py + test_holder_norms.py
## (6/6; suite 12 files green); fig23; BLOG/TECHNICAL_P2_ROUTED_V5.md. Level-1 tooling + scoping, NOT a
## certificate; operator norms are FAMILY-RESTRICTED lower bounds and Z1 is still unbounded.**
## **ROUTE-D v6 DONE (§15, 2026-07-30): the FIRST GENUINE UPPER BOUNDS + the DISCRETE-BALL TRAP. THREE of
## eight NK constants move MEASURED -> BOUNDED (Z1 far-field modelling error; ||A|| domain sup part,
## 5.536->5.631 over J=125..1600 = SATURATES; C_Q sup part). METHODOLOGICAL HEADLINE: computing an induced
## norm by DUALITY over the DISCRETE unit ball is UNSOUND -- the extremizer it picks is a grid-scale sign
## pattern inflated ~J^2 (3e3 at J=125 -> 5e4 at J=500) in the CONTINUUM norm, so the ||A|| ~ J^0.5 it
## reported under three routes and every gauge choice is FICTION. Sound route: use only inequalities the
## continuum norm implies (two_point_dual). EXACT identity (DF-L)h = h/(X(1+X^2)) - H(h)/(1+X^2) (1.5e-16)
## + a Holder-paid |H(h)| bound on the EVEN kernel gives the far-field Z1 bound (decays X0^{alpha-2},
## validated 1.1-3.0x headroom). CONSEQUENCE: **v5's joint optimum alpha=1.8 is DEAD** (Z1 = 2.3-4.3, no
## closure at any X0); optimum moves to alpha~1.2, conditional budget 1.18e-2. STILL OPEN: ||A|| domain
## seminorm part, core<->far coupling, core discretization. New solver/nk_bounds.py + test_nk_bounds.py
## (6/6; suite 13 files green); fig24; BLOG/TECHNICAL_P2_ROUTED_V6.md. NOT a certificate.**
## **ROUTE-D v7 DONE (§16, 2026-07-31): the DOMAIN SEMINORM PART OF ||A||, CLOSED. v6 recommended the
## band-limited-subspace route; a ten-minute diagnostic disqualified it STRUCTURALLY (the J^gamma sits
## entirely on NEAR-DIAGONAL pairs — a faithfulness defect of the ball cannot know whether two domain
## indices are adjacent, and the J^gamma does), so this leg did the analytic route instead. Solve the
## equation for the derivative (exact rearrangement, 1.9e-16), split every pair at a fixed multiple of
## the LOCAL X-scale — the weights then cancel identically at every scale — and get
## T <= C(gamma)(P/2)^gamma(2S)^{1-gamma} with **NO J and NO GRID**. The feedback is LINEAR in T while
## the gain is SUBLINEAR (T^gamma), so the closure holds for ANY constants: **no smallness condition**,
## and gamma=1 is excluded for a THIRD independent reason. RESULT: **the first uniform upper bound on
## the WHOLE of ||A|| in seven legs** (69.1 -> 70.3 over J=125..1600, J^+0.006, drift inherited entirely
## from v6's C_sup) and the **first (alpha,gamma) interior optimum made of upper bounds**
## ((1.4,0.15), Z2 <= 242). Honest: the bracket is 0.85 <= (seminorm part) <= 63.6, a factor ~75 wide,
## and pricing the honest ||A|| costs the conditional budget another order of magnitude (2.8e-3 ->
## 2.0e-4) — the SECOND CONSECUTIVE leg where an upper bound cost an order, i.e. **the constants must
## be roughly SHARP, not merely bounded.** Also surfaced an older defect: the interpolant's
## decay-graded norm is INFINITE at every J (trig polys do not vanish at theta=pi where sec^alpha
## diverges); soft (h(pi) ~ J^-3.01) but it is a change of ANSATZ, h=(1+X^2)^{-alpha/2}p(theta). Six of
## ten constants bounded. New solver/nk_seminorm.py + test_nk_seminorm.py (6/6; suite 14 files green);
## fig25; BLOG/TECHNICAL_P2_ROUTED_V7.md. NOT a certificate.**
## **ROUTE-D v8 DONE (§17, 2026-07-31): the CODOMAIN SEMINORM PART OF C_Q — the last unpriced
## constant in Z2, and the FIRST COMPLETE Z2. The needed weight is 1-gamma, NOT alpha-gamma: H does
## NOT inherit h's decay (H(h) -> (int h)/(pi X) however fast h falls), so psi's grading is 1 — the
## third time in this series a weight exponent was the whole difficulty and the right one was FORCED.
## Estimate: change variables so NOTHING WRAPS (in absolute theta, (theta~pi, phi~-pi) are
## NEIGHBOURS on the circle), split near/far, charge the near part to smoothness and the far part to
## decay, keep every constant: **T_psi <= 1.1936 S + 4.9410 T** at (1.5,0.5), flat to 4e-6 under a 4x
## pair-grid refinement. The only route v6/v7 had (pointwise) is **237x worse**. Gated by a SECOND
## BUILD of the decomposition against the exact conjugate (5.6e-6) — which caught two sign errors a
## domination test could never see, since a majorant of a WRONG decomposition is still a valid
## inequality about something. RESULTS: (i) **the first COMPLETE Z2 map** — every constant an upper
## bound, nothing omitted — with optimum at **(1.4, 0.15), Z2 <= 261**, the SAME location v7's
## incomplete map gave (242), so v7's provisional optimum HOLDS; (ii) **v7's stated reason for calling
## it provisional was BACKWARDS** — the correction is 0.1% at gamma=0.05 and 28% at 0.9, because v6's
## sup-only C_Q already carried the same 1/gamma near-region divergence; (iii) **the budget history
## 7.6e-2 -> 1.18e-2 -> 2.58e-4 -> 2.39e-4: three order-of-magnitude losses, then one of 7%.** v7's
## headline negative (every honesty step costs an order) DOES NOT CONTINUE. Honest: 2.4e-4 is still
## ~40x below the GA floor, the new bound is itself ~4x lossy, and this is no evidence the remaining
## three ledger items are cheap. **Seven of ten constants bounded; Z2 COMPLETE.** New
## solver/hilbert_holder.py + test_nk_hilbert_holder.py (6/6; suite 15 files green); fig26;
## BLOG/TECHNICAL_P2_ROUTED_V8.md. NOT a certificate.**
## **ROUTE-D v9 DONE (§18, 2026-07-31): THE SHARPNESS LEG — and a NEGATIVE WITH A MECHANISM.
## Rebuilt the |H(h)| bound on the exact folded kernel K = 2 sin(th)/(cos phi - cos th), whose p.v.
## over (0,pi) is EXACTLY ZERO (it is the conjugate of the constant function), so the singularity
## needs ONE GLOBAL SUBTRACTION instead of v6's band + matching scale + remainder. Sharper at every
## X (ratio 0.09-0.99) and nearly ATTAINED (0.97 on the anchor). Also found that the PAYER RULE —
## which part of the norm pays at each point — is a free parameter with an INTERIOR optimum, and
## that the neutral choice (compare at S=T=1, v8's default) is WORSE than the crude bound it
## replaces: **tune the rule to the T/S ratio of the ANSWER, not to 1.** ||A||: 69.15 -> 47.05
## (-32%), the largest single gain since the closure was built. **AND THE BUDGET DID NOT MOVE
## (2.39e-4 -> 2.40e-4).** Why: the closure is T <= C(g)(P/2)^g(2S)^{1-g} and the |H| bound enters
## ONLY through P, so at the map's optimum (gamma=0.15) a 30% better P moves T by 4% — gain by
## point 32%/11%/3%/0%. Worse, the optimum sits at small gamma BECAUSE that is where ||A|| barely
## depends on this input. **THE ELASTICITY TABLE (one minute, should have come first):
## d log||A||/d log C_sup = +1.00 at the operating point; d log||A||/d log|H| = +0.11.** The last
## TWO legs both worked on inputs with elasticity <= 0.5 and both moved the budget by <= 7%. Also
## re-caught banked lesson 15: an "oracle C_sup" substitution reported a 19x available gain that was
## an artifact of a bad lower bound. NEXT is decided by the table: C_sup (the only elasticity-1
## input left, ~2x available), and BEFORE that a REAL lower bound on ||A|| — without one, no bracket
## in this project can be attributed. New solver/hilbert_pointwise.py + test_nk_hilbert_pointwise.py
## (6/6; suite 16 files green); fig27; BLOG/TECHNICAL_P2_ROUTED_V9.md. NOT a certificate.**
## **ROUTE-D v10 DONE (§19, 2026-07-31): A LOWER BOUND ON ||A|| WORTH READING. Every bracket this
## project has quoted had a lower end that was a maximum over SIGN PATTERNS, and the tell nobody
## checked is that it gets WORSE with J (0.973 -> 0.921) — it was never converging to anything
## about the operator, only measuring how badly a jagged vector is punished by a Holder seminorm.
## Replaced by an adversary family the Y-ball actually contains (1/v times a slowly varying shape:
## powers, low cosines, swept bumps, smoothed steps, boxes); validity is free since any g gives
## ||A|| >= ||Ag||/||g||. Reference bracket **50x -> 16x**; and at the OPERATING point (1.4,0.15),
## where the budget has been evaluated for three legs, **2.74 <= ||A|| <= 20.94 — a factor 7.7, not
## 50.** The extremizer is a WIDE FAR-FIELD BUMP (theta=3.12, X~93), the same place v2's far-field
## degeneracy, v3's resonance and v6's X0 all point. **THE VERDICT (the first MEASURED ceiling on
## sharpening in ten legs): a PERFECT upper bound on ||A|| would move the budget 2.45e-4 -> 1.88e-3
## and no further, i.e. ~5x short of the GA floor rather than 40x — better than it looked, and NOT
## enough on its own** (it would also need C_Q's ~4x, and the two together only just reach the floor
## with nothing spare for the three open Z1 items). New solver/op_lower.py + test_op_lower.py (6/6;
## suite 17 files green); fig28; BLOG/TECHNICAL_P2_ROUTED_V10.md. NOT a certificate.**
## **ROUTE-D v11 DONE (§20, 2026-07-31): NEWTON ON THE PROFILE. Unknowns (Omega,c), TWO gauges
## (the a=0 zero set is the 2-parameter family A/(1+BX^2), so one gauge leaves the Jacobian
## singular and a direct solve crawls to 1.8e-6 in 40 iterations; two in least squares reach
## 2e-15 in 5). **The ~1e-2 residual floor that section 9 read as a property of the problem is a
## property of the SEARCH: Newton reaches machine precision, TWELVE orders below it**, for every a
## below the boundary. Newton also converged at large a — which for an hour looked like "the
## boundary is a genome artifact" — but **the grid test overturns that**: spread in c across
## n=401/801/1601 is 3e-5 at a=0.5 and 1.3e-2 at a=1.0, with only 1 of 3 grids converging there,
## so the large-a successes are solver artifacts and **the GA's a*~0.5-0.55 stands, confirmed a
## FOURTH time by a genome-free method**. What it does to Y0 is a change of BINDING CONSTRAINT,
## not a solved problem: the certificate sees the WEIGHTED sup defect, which is 6+ orders larger
## (1e-8..1e-7 typically, 1.5e-2 at a=0.45, ABOVE the 2.45e-4 budget) because the codomain weight
## amplifies the far field where the truncation lives. **Y0 is no longer SEARCH-limited, it is
## DISCRETIZATION-limited** — already a ledger item, and a much better problem to have. New
## solver/profile_newton.py + test_profile_newton.py (6/6; suite 18 files green); fig29;
## BLOG/TECHNICAL_P2_ROUTED_V11.md. NOT a certificate.**
## **ROUTE-D v12 DONE (§21, 2026-07-31): Y0 MEASURED IN THE BOUNDS' OWN BASIS — and the
## a>0 profile ENDS. Built the a-transport term in the compactified theta-basis (velocity
## U = sum_k A_k I_k, exact recursion, longdouble), so the residual of the INTERPOLANT is
## evaluable anywhere: A is the Newton matrix and Y0 is the Newton step. Newton zeroes the
## rows it enforces (1.5e-13) while the row the gauge displaced carries 9.1e-3 at a=0.5 —
## zero at the nodes is not zero as a function. **THE MECHANISM: the true transport
## coefficient is E = c + aU, and U ~ (int Omega/pi) log X -> -infinity, so E crosses zero at
## a FINITE X_c ~ e^{c/a}; near it Omega ~ (X_c - X)^{1/a} (no free constant) and beyond it
## Omega = 0 solves the equation exactly.** Two independent discretizations agree on X_c/c to
## 0.06-0.11%; the fitted zero order tracks 1/a to 7-9%. The a=0 anchor — the object the whole
## decay-graded programme was built on — is the degenerate X_c = infinity limit. CONSEQUENCE:
## **||A|| at the REAL profile DIVERGES with J (J^+2.86 at a=0.2, J^+2.75 at 0.3) while it is
## FLAT at the anchor (J^-0.003)**, because linearizing about a zero of order p has a
## homogeneous mode ~ s^{-p} that is in no sup norm. So the seven bounded ledger constants are
## constants for the ANCHOR and do not transfer, and the one number that came in 7.7x UNDER
## budget (a=0.2, J=1600) was priced with the wrong operator. The boundary a*~0.5 gets a
## candidate mechanism (X_c descending into the core) but the a=1/3 control kills the sharp
## version, so v12 does NOT predict a*. New solver/collocation_newton.py +
## test_collocation_newton.py (6/6; suite 19 files green); fig30; BLOG/TECHNICAL_P2_ROUTED_V12.md.
## REPAIR (v13): finite interval [0, X_c] with X_c a free-boundary UNKNOWN — the far field
## disappears; kill switch is ||A|| vs J in that formulation. NOT a certificate.**
## **ROUTE-D v13 DONE (§22, 2026-07-31): THE TURNING POINT — §21's MECHANISM WAS WRONG.
## The mode AT X_c vanishes like (X_c-X)^{+1/a} (§21 said -1/a: a dropped sign in
## d/dX -> d/ds), and nothing is singular there. **The obstruction is in the FAR FIELD:
## outside X_c the same equation gives h ~ (log(X/X_c))^{1/a}, which GROWS, against a
## domain space that is a DECAY class — a codimension-1 RANGE obstruction no refinement
## touches.** Measured with an instrument independent of the matrix: q = 4.9988/3.9980/
## 3.3307/2.8536/2.4855 vs 1/a = 5/4/3.3333/2.8571/2.5 (0.02-0.6%, no fitted constant);
## the a=0.5 outlier (q=0.054) refines to 1.84/1.70 and is the instrument, as §21 T4
## predicted. So **1/a appears THREE times: the profile's zero order, the vanishing inner
## mode, the growing outer mode.** The divergence is now ATTRIBUTED: with the domain sup
## restricted to a fixed outer radius the J-slopes fall +2.86 -> +1.06 -> +0.54 -> +0.31
## (a=0.2) while the a=0 control is flat at EVERY cutoff, and 87-97% of the extremal row's
## mass comes from within 10% of X_c (sourced at the turning point, damage in the far
## field). The residual J^+0.3 at fixed radius is NOT attributed. **The cheap repair is
## DISQUALIFIED: restoring the speed c adds KERNEL, not range (dilation is a symmetry) —
## the square bordered system at a=0 has cond 4.4e18.** New solver/turning_point.py +
## test_turning_point.py (6/6; suite 20 files green); fig31; BLOG/TECHNICAL_P2_ROUTED_V13.md;
## §21's writeups corrected IN PLACE with the change MARKED. REPAIR (v14): remove the far
## field from the DOMAIN — [0, X_c] with X_c an unknown. NOT a certificate.**

After Spike 1 (the 2D Boussinesq dynamic-rescaling machine, which reproduced the *proven*
Chen–Hou regular profile), we scoped P2 = the actual novelty frontier. Decision (with the
user, from evidence): **attack the 1D Hou–Luo (HL) model, not 2D Boussinesq.**

Target paper: **Chen–Huang–Li, arXiv:2604.01868** (Papers/, gitignored — `Read` page by page).
Their novel result: *degenerate* initial data (ω⁰ₓ(0)=θ⁰ₓₓ(0)=0) develops **singular**
self-similar profiles via a **two-stage** L^∞-then-L^p blowup. This is a **not-rigorously-proven
frontier** — only *weak existence* of the explicit profile is proven (their Thm 2.3); the
*asymptotic stability* (that generic degenerate data converges to it) is **numerical only**.
That gap is where a lottery ticket could live.

### Why 1D-HL over 2D (the scout, §1)
- The novel phenomenon lives first in the 1D HL model (ωₜ+uωₓ=θₓ, θₜ+uθₓ=0, uₓ=H(ω)),
  which "models the boundary behaviour of the Hou–Luo / 3D-axisymmetric-Euler scenario."
- 1D reuses machinery we already have (solver/line_hilbert.py 6/6, gclm rescaling 5/5).
- 2D would compound the exact far-field-tail problem Spike-1 Step C already hit, at higher cost.
- **Feasibility probe (decisive):** our line-Hilbert operator **survives** the singular profile.
  Against the exact H I derived (below), the (X−1)^{−1/2} *core* is representable to a few %
  and improving; the only real error is the slow X^{−1/2} *tail*, which is **truncation-limited**
  (halves with domain reach M, immune to node clustering) — the known semi-analytic-outer-patch
  gap, NOT a failure to resolve the singularity. (fig12 panel C.)

## §2 — The validation anchor (DONE, 2026-07-25). VALIDATION, not novelty.

Rescaled HL dynamics (their (2.4)), fields Ω (vorticity), Θ (buoyancy), velocity U:
```
Ω_τ + (U + c_l X) Ω_X = c_ω Ω + Θ_X
Θ_τ + (U + c_l X) Θ_X = (c_l + 2 c_ω) Θ
U_X = H(Ω),  U(0)=0.
```
Two genuinely new pieces vs the CLM solver: the velocity U is the *integral* of H(Ω) pinned at
U(0)=0 (CLM's transport speed was purely algebraic), and the second buoyancy field Θ.

**Explicit exact anchor — their Theorem 2.3:**
```
Ω̄(X) = (X−1)^{−1/2} 1_{X>1},   Θ̄ = (π/2) 1_{X>1},   c̄_l = 2,  c̄_ω = −1.
```
**Derived here (a small self-contained result):** from the classical Hilbert pair
H(x₊^{−1/2}) = −(−x)₊^{−1/2} (Fourier multiplier −i·sgn(ξ)),
```
H(Ω̄)(X) = −(1−X)^{−1/2} 1_{X<1},    U̅(X) = 2√(1−X) − 2  (X<1),  −2  (X≥1),
```
which satisfies (U̅+2X)Ω̄_X + Ω̄ = 0 on X>1 (the strong steady form; Remark 5.4) and U̅(0)=0,
U̅(1⁻)=−2. A free consistency check: c̄_l+2c̄_ω = 0 exactly ⇒ the Θ steady equation is trivial.

**Built:** solver/hl_rescaled.py (velocity operator, rescaled RHS, steady residual, both grids).
**Tests:** test_hl_rescaled.py **5/5** —
- velocity operator vs analytic arctan(2X): 1.1e−5; full pipeline through the dense H: 1.8e−3
- velocity on the singular anchor → U̅, converges under δ-refinement (½-order — the √-singularity)
- steady residual of the explicit Thm 2.3 profile → 6.2e−3, converging
- c̄_l+2c̄_ω=0 consistency: exactly 0.

## §3 — Performance (line_hilbert.py, the shared operator)
The build bottleneck was in the shared operator, not the new P2 code:
- batched Thomas solve for the slope operator: `_slope_matrix` 6.15s → 0.29s (21×);
- Horner + shared + shortened `L(s)` series (dominant cost): n=4001 matrix build 65s → 19.7s (3.3×);
- lazy Hilbert matrix in RescaledHL (anchors that use exact H never build it).
Net: HL suite >120s → 3.9s. Accuracy **identical** (line_hilbert 6/6, gclm 5/5, hl 5/5 all green).

## §4 — THE OPEN WORK (the actual lottery ticket; NOT yet started)
The anchor above reproduces a *proven* result — it validates the singular machinery, nothing more
(Tier-1/2, not novel, not a proof; same category as Spike 1). Novelty begins with the **dynamic
relaxation + degenerate-case normalization**:
- Build the SSPRK3 time stepper for (2.4) with a normalization that works when the origin slopes
  vanish (CHH22's origin-slope gauge is degenerate for degenerate data — need a higher-order or
  norm-based gauge). LOCK a predicate BEFORE the logged run.
- **Novelty target:** does *generic smooth degenerate data* converge to the singular profile (the
  asymptotic stability CHL only asserted)? A resolution-confirmed yes/no is a Tier-2-style
  contribution. Beyond that: unexplored degeneracy orders / profile families; the flagged-open
  link to Hou–Huang two-scale 3D-axisymmetric-Euler (HH23).
- The slow X^{−1/2} tail will need a fixed-τ protocol + semi-analytic r^α outer patch (same fix
  flagged for Spike-1 Step-C polish). Bounded, known.

Honest odds unchanged: overall Clay ~0.05%. The realistic prize is novel toy-model singularity
research + a shareable, data-backed writeup. This leg is the first genuine swing at it.

## §5 — HH23 SCOUT (2026-07-25). Go/no-go on the flagged-open Hou–Huang link. Verdict: NO-GO on
the literal link; the scout surfaced a SHARPER, 1D-tractable adjacent question. No logged run.

Grounded in CHL (2604.01868) itself (pdftotext → grep, not vibes). Key passages: intro p.6
(the "intriguing question"); §2.3 (two-scale mechanism); §3 conclusion (their two-STAGE finding).

**What [HH23] actually is** — the CHL bibliography (not the paper; HH23 is not in Papers/):
T. Y. Hou & D. Huang, *Potential singularity formation of incompressible axisymmetric Euler
equations with degenerate viscosity coefficients*, MMS 21(1):218–268, 2023. A **numerical
two-SCALE self-similar blowup of 3D axisymmetric Euler on ℝ³, with NO boundary**, smooth data.

**What CHL actually claim about the link** (verbatim, intro): their singular profiles "share
qualitative similarities with those observed in ... Hou–Huang [HH23], which suggested a potential
two-scale self-similar blowup of 3D axisymmetric Euler ... in the absence of a boundary. Whether
these phenomena are fundamentally linked remains an intriguing question." An *aspirational intro
remark about profile appearance* — not a worked reduction.

**The decisive structural mismatch (why NO-GO):**
1. HH23 = two-**SCALE** (spatial multi-scale: a bulk traveling at r(t) in a coarse scale (T−t)^γ
   + a fine inner scale (T−t)^γ̂; connected to traveling waves; the CHL eq-(2.8)/[HQW25] structure).
2. CHL's HL result = two-**STAGE** (temporal: local L^∞ blowup at T̃ off-origin, then weak
   continuation to an L^p blowup at the origin at T). And CHL **explicitly report NO numerical
   evidence of a two-scale mechanism in HL** (§3: "we find no numerical evidence supporting a
   two-scale blowup mechanism for the HL model analogous to that described in [HQW25]"). The very
   feature that DEFINES HH23 (two-scale) is the one CHL looked for in HL and did NOT find.
3. Geometry: 1D HL models the *boundary* behaviour of the Hou–Luo scenario. HH23 is *boundary-free*
   ℝ³. The 1D HL model is not a reduction of the no-boundary 3D scenario.
⇒ A 1D-HL machine cannot address "are they fundamentally linked" without overclaiming — that is a
3D structural question, wrong geometry, and CHL's own data points AWAY from a shared mechanism.
Chasing it as a "link to 3D Euler" would be exactly the self-deception WIN_CONDITION guards against.

**The scout's payoff — the genuinely-open, 1D-tractable question hiding behind the remark:**
the **two-scale-vs-two-stage question inside the 1D CLM/HL family.** The two-scale mechanism (the
thing that *resembles* HH23) is PROVEN for the CLM model (Huang–Qin–Wang [HQW25], SIAM J Math Anal
57(4):4068–4096, 2025) and was **conjectured by Liu [Liu17] for HL** — but CHL found HL is
two-STAGE, not two-scale. That is a LIVE discrepancy (Liu's conjecture vs CHL's numerics), entirely
in 1D, and CHL themselves pose it: "If singular profiles are observed, is their formation related
to a two-scale blowup mechanism?" Our exact machinery (line_hilbert + rescaled HL + the
dynamic-relaxation stepper we're about to build) is precisely the tool to settle it — track the
peak LOCATION and test for a moving bulk at a coarse scale (two-scale signature) vs a τ→∞
convergence to the fixed singular profile at X=1 (two-stage signature), across degeneracy classes.

**Honesty ceiling on that too:** confirming CHL's "no two-scale in HL" = Tier-2 independent
confirmation. Finding two-scale in some HL degeneracy class CHL missed (vindicating Liu) would be a
genuinely new *1D* result — the better lottery ticket — but odds are it's absent (CHL looked), and
even a positive is a 1D analogue, still NOT a proven link to 3D Euler.

## §6 — DYNAMIC-RELAXATION LEG DONE (2026-07-25). Conjecture 2.4 at POC: LOCAL attractor
confirmed, global basin not. PARTIAL / Tier-2-style. Full record: writeup/4_p2_lottery/TECHNICAL_P2_CONJ24.md
+ BLOG_P2_CONJ24.md; fig13 from committed writeup/data/p2_conj24_relax.json
(`python writeup/4_p2_lottery/p2_conj24_evidence.py`). Logged harness (predicate locked in git first):
experiments/p2_conj24_relax.py --logged. Machinery: solver/hl_rescaled.py::RescaledHLDynamic,
test_hl_rescaled.py now 7/7.

**The novel piece BUILT + VALIDATED: CHL's degenerate normalization gauge (their (3.2)).** The
CHH22 gauge pins the origin slope Omega_x(0) = 0 for degenerate data (dead). CHL read the NONLOCAL
U_X(0)=H(Omega)(0) (alive) for amplitude + c_l=-U(1) for location. Known-answer test on the exact
Thm-2.3 anchor → (c_l,c_omega)=(1.949,-0.969)≈(2,-1); degeneracy sidestep: |Omega_x(0)|~1e-4 vs
|H(Omega)(0)|~1.24. Two new unit tests.

**The wall (diagnosed):** non-dissipative SSPRK3+upwind+spline is UNSTABLE at the singular profile
— starting AT the regularized anchor, residual grows 25→1e9 by τ~1.4 (spline slopes ring at the
X=1 discontinuity; the stiff Theta_X delta-source amplifies). Fix = subgrid dissipation nu*d²/ds²
(a POC crutch, O(nu) profile bias, NOT CHL's WENO/adaptive mesh). Added as solver `nu` param.

**Logged result (n=801, nu=0.02, 2500 steps; 9/9 pre-committed clauses PASS, PARTIAL by design):**
- anchor hold → (c_l,c_omega)=(1.939,-0.927), res 180→3.4 plateau (stable HOLD, NOT →0), shape 4.9%.
- 2 perturbations → same fixed point (within 0.06), res drops >5× → LOCAL asymptotic stability.
- nu=0.04 → (1.936,-0.925), unchanged → fixed point robust to the stabilizer (not a nu artifact).
- generic far degenerate IC → (0.680,-0.487), a DIFFERENT self-similar state (low res, wrong
  constants, 29% shape) → GLOBAL basin beyond a fixed-grid POC (the honest predicted negative).

**Honest status:** validated the degenerate gauge + the LOCAL stability of CHL's singular fixed
point (independently reproduces the local content of a numerical-only claim). NOT achieved:
residual→0 (POC dissipation floor) and the global basin. Both need WENO/adaptive mesh +
vanishing-viscosity + semi-analytic X^{-1/2} outer patch (same tail fix as Spike-1 Step C).
Tier-2-style, NOT novel, NOT a proof. 1D HL is a toy (boundary behaviour of Hou–Luo). Clay ~0.05%.

**Next (reassess with user):** the genuinely-new leg is the §5 two-scale-vs-two-stage question
(Liu conjecture vs CHL finding), which needs exactly the global-basin numerics above. Options:
invest in the heavier numerics (WENO/adaptive/tail patch) to reach generic-data convergence + the
two-scale probe, OR bank P2 as a shareable data-backed Tier-2 writeup and pivot.

## §7 — REGULAR-PROFILE REFRAME + B1/B2 SCOUT (2026-07-25). EXPLORATORY (non-logged scout), but
it upgrades §6's most important caveat and scopes the fork. Evidence: writeup/
p2_regular_profile_evidence.py → fig14 from committed writeup/data/p2_regular_profile.json (two
fixed-point fields) + p2_regular_profile_traj.json (8000-step generic trajectory). No new solver
code; used RescaledHLDynamic as-is. NOT a logged gate run (no pre-committed predicate).

**The reframe (grounded in CHL §2.5 + §4).** CHL's rescaled HL system has TWO fixed points, not one:
- the SINGULAR anchor (§2 / §6): Ω̄=(X−1)^{−1/2}1_{X>1}, (c_l,c_ω)=(2,−1) — CHL's Stage-2 attractor;
- a REGULAR, strictly-positive profile (their Scenario 2, §4) — CHL's Stage-1 attractor: "a
  non-symmetric regular profile that remains strictly positive throughout," peaked off the singular pt.
The §6 logged run's "generic far degenerate IC → (0.680,−0.487), a DIFFERENT self-similar state
(honest predicted NEGATIVE)" is NOT a POC artifact: characterizing that final field shows it is
**smooth (max|Ω_X|/peak≈0.3 vs 1061 for the singular anchor), strictly positive (single-signed),
peaked at X≈0.35 (away from X=1), finite** — i.e. qualitatively CHL's Stage-1 regular profile. So our
machinery reaches BOTH CHL fixed points; the "negative" is really the first half of CHL's two-STAGE
structure, captured independently. (fig14 panels A vs B.)

**HONESTY GUARDS.** (1) Reached with the STANDARD (2.4)+degenerate-gauge, NOT CHL's modified
Scenario-2 formulation (2.9)/(4.1) — so this is a QUALITATIVE match (regular, +ve, peak off X=1),
NOT a proven identity to their profile. (2) The raw constants differ as expected under a different
normalization (ours c_l≈0.5, c_ω≈−0.45; theirs (c_l,c_ω,c_r)=(1.0636,−0.4235,0.0765), ratio
−2.5114). (3) It does NOT converge under our gauge — see the trajectory below. Not novel, not a proof.

**THE B1/B2 SCOUT (8000-step generic trajectory, fig14 panel C).** Under the degenerate gauge the
trajectory TRANSITS the CHL-S2 neighborhood (c_l≈1.06, c_ω≈−0.45 near step 1200 — the constants
nearly coincide) but CANNOT hold it, then WANDERS in the low-c_l regular regime (c_l oscillates
0.38–0.49, res floor ~0.12), and **NEVER approaches the singular anchor c_l=2.** Diagnosis: our gauge
pins c_l=−U(1) (stagnation at X=1) — a MISMATCH for a regular profile peaked at X≈0.35. CHL's (4.2)
normalization instead pins behavior at the ORIGIN (∂_τΩ(0)=∂_τΩ_X(0)=∂_τV(0)=0), exactly the right
stabilizer for the regular profile. Two decisive reads for the fork:
- **B1 (implement CHL's modified formulation) is the recommended next brick and is CHEAP + clean.**
  Formulation (4.1) = our (2.4) with ONE extra constant c_r in the transport speed (U+c_l X+c_r) +
  the V:=Θ_X change of variable; normalization (4.2) = a 3×3 linear solve for (c_l,c_ω,c_r) each step.
  KNOWN-ANSWER target: (c_l,c_ω,c_r,c_l/c_ω)=(1.0636,−0.4235,0.0765,−2.5114) (their Fig 4.2). We
  already fly within ~0.005 of c_l=1.0636 at the transit, so pinning there is very plausible. Outcome
  = "both CHL scenarios reproduced" + a shape overlay confirming the Stage-1 identification. Tier-2.
- **B2 (the Stage-1→Stage-2 transition / two-scale-vs-two-stage probe) is NOT reachable on this fixed
  grid** (the trajectory heads AWAY from c_l=2) and needs the adaptive-mesh rebuild; even a clean B2
  mostly RE-CONFIRMS CHL's already-published two-stage finding (low novel upside). Wrong brick now.

**Honest ceiling (unchanged).** B1 reproduces a CHL object → Tier-2, not the lottery ticket. The
genuinely-new math is elsewhere: (i) the gCLM-family two-scale-vs-two-stage transition — where in the
parameter 'a' does CLM's PROVEN two-scale (HQW25) give way to HL's two-stage (CHL)? Nobody has mapped
this, and we already have solver/gclm_rescaled.py; or (ii) a rigor step on Conjecture 2.4. Both are
harder + longer odds. B1 is the grounded consolidation brick that de-risks either.

## §8 — B1 DONE (2026-07-26). CHL Scenario 2 reproduced: the modified rescaling (4.1)/(4.2).
LOGGED run, predicate LOCKED in git before the run (commit b5294ff). PARTIAL/Tier-2 by design —
NOT novel, NOT a proof. Full data: committed `writeup/data/p2_scenario2_relax.json`; harness
`experiments/p2_scenario2_relax.py --logged`.

**What was built (the transferable deliverable).** `solver/hl_rescaled.py::RescaledHLScenario2` —
CHL's modified formulation (4.1): transport `(U+c_l X)→(U+c_l X+c_r)` with a spatial-shift DOF
`c_r`, evolving `V:=Θ_X`. Normalization (4.2): pin `∂_τΩ(0)=∂_τΩ_X(0)=∂_τV(0)=0` at the shifted
ORIGIN via a hand-rolled 3×3 solve (`_solve_3x3`, no scipy) each step for `(c_l,c_ω,c_r)`. Grid is
origin-clustered with **X=0 a node** (so the gauge reads Ω(0),Ω_X(0),Ω_XX(0),V(0),V_X(0),U_X(0)=
H(Ω)(0) at a node — the accuracy this brick buys over §6's X=1 grid). `scenario2_ic` = generic
non-symmetric positive **origin-NONdegenerate** data (Scenario 2 lives at a non-symmetry origin:
Ω_X(0)≠0 is the coefficient of c_l — degenerate_ic would make the gauge singular). Unit tests
`test_hl_rescaled.py` **9/9**: `_solve_3x3` matches numpy (7e-14) + flags singular systems, and the
KNOWN-ANSWER gauge test — the (4.2) solve nulls `∂_τ{Ω(0),Ω_X(0),V(0)}` to **4.4e-16**.

**WHY this is the right brick (honoring the user's steer):** the §6/§7 degenerate gauge pins
`c_l=−U(1)` (stagnation at X=1) — the reframe scout MEASURED that it cannot HOLD a profile peaked
away from X=1. CHL's (4.2) origin-pinned gauge CAN. That origin-pinned gauge is exactly what a gCLM
two-scale↔two-stage sweep (the actual lottery-ticket angle) needs to hold regular profiles across
the parameter `a`. B1 = "the gCLM-ready gauge, VALIDATED against a known answer", not a trophy.

**LOGGED RESULT (n=801, nu=0.02, 2 ICs × 14000 steps, adaptive dt → τ≈42; 5/5 PARTIAL):**
- **S1 ratio known-answer PASS:** generic IC (x0=0.30) → `c_l/c_ω = −2.5334` (CHL −2.5114, ~0.9%).
- **S2 attractor PASS:** 2nd IC (x0=0.45, different width) → −2.5352, same ratio ⇒ genuine
  IC-independent attractor (not a tuned initial condition).
- **S3 regular positive PASS:** min Ω=5.6e-2>0, min V>0, smoothness max|Ω_X|/peak=0.73 (vs ≈1061
  for the singular anchor), peaked at X*=0.82 (non-symmetric). = CHL's Scenario-2 object.
- **S4 residual bounded+falling PASS:** res 15→2.2e-2 (≈680×), no blowup.
- **S5 HONEST CEILING PASS (predicted):** res FLOORS at 2.2e-2 (does NOT reach CHL's 1e-6) AND the
  absolute triple stays off CHL's raw `(1.0636,−0.4235,0.0765)` — ours drift to `(1.59,−0.63,0.21)`.

**THE HONEST READ.** The amplitude-INVARIANT contraction exponent `γ=c_l/c_ω` — the physical
Scenario-2 prediction — is reproduced to ~1% as a real attractor to a regular positive profile.
The ABSOLUTE `(c_l,c_ω,c_r)` are IC-normalization-dependent (the (4.2) gauge holds Ω(0),Ω_X(0),V(0)
at their initial values; matching CHL's raw triple needs matching their IC normalization) AND the
fixed grid floors the residual at ~2e-2 (CHL reach 1e-6 with an adaptive mesh). So: **both CHL
scenarios now reproduced** (§2 singular Stage-2 anchor + §8 regular Stage-2/Scenario-2 exponent).
Tier-2 consolidation. The lottery ticket still lives elsewhere — the gCLM two-scale↔two-stage
transition (uses the now-validated origin-pinned gauge machinery) or a rigor step on Conj 2.4.

## §9 — GA GLOBAL-SEARCH FRAMEWORK DONE (2026-07-26). Validated INFRASTRUCTURE for the gCLM two-scale↔two-stage probe. NOT a science result.

Banked record: writeup/4_p2_lottery/TECHNICAL_P2_GA_FRAMEWORK.md + BLOG_P2_GA_FRAMEWORK.md + fig16 (rebuilds from
committed writeup/data/p2_ga_framework.json via `python writeup/4_p2_lottery/p2_ga_framework_evidence.py`).
Code: solver/gclm_family.py, solver/ga_search.py; tests test_gclm_family.py (6/6; full suite **7/7**).

**The user's steer this session:** pursue the gCLM two-scale↔two-stage transition as the novelty
swing, and do it VIA a genetic algorithm (their idea) — build the GA so it also serves Route D. Target
chosen (with the user): **gCLM axis first (anchored, tractable), then bridge to HL.**

**Why a GA (honest).** The self-similar profile is a fixed point of a rescaled flow; a family can have
MULTIPLE fixed points (different mechanisms). Relaxation (§6, §8) is LOCAL — slides into the attractor
you seed near, blind to the rest. A GLOBAL search over (shape + exponents) can map the fixed-point set
and its bifurcations = the open two-scale↔two-stage question. A GA proves nothing (Tier-1/2 only); its
two honest roles are (i) this global mapper and (ii) the "guess" stage for a Route-D interval-Newton
certification. Framework built to serve both (the residual object is reusable).

**Key upstream fact banked.** The two-scale ANCHOR paper is **[HQW25] = arXiv:2401.14615** (Huang–Qin–
Wang, SIAM J Math Anal 57(4) 2025) — downloaded to Papers/2401.14615v_HQW25.pdf (gitignored). It gives
the EXACT a=0 two-scale profile Ω₂(z) = −a³b^{3/2}c/(a⁴c²+b⁴z²) (an EVEN Lorentzian bump, c_ω=−3/2,
c_l=1, c_s=1/2) — a clean known answer for the two-scale end. NOTE the original "bisect in `a` between
CLM and HL" framing was corrected: HQW25 two-scale is CLM=a=0 (scalar gCLM family); CHL two-stage is
the HL COUPLED (ω,θ) system — NOT the same `a`-axis. So the well-posed gCLM-axis question is: **does
HQW25's a=0 two-scale mechanism survive advection as `a` grows?** (bridge to HL is a separate later leg).

**What was BUILT + VALIDATED:**
- `solver/gclm_family.py::GCLMResidual` — the gCLM `a`-family rescaled steady residual
  R = (c_ω+HΩ)Ω − c_l XΩ_X − a U Ω_X, with velocity U=∫₀ˣHΩ (cached cumulative-trapezoid `Vmat`,
  U(0)=0), on the sinh grid, reusing the dense line-Hilbert operator. SEPARATE from the relaxation
  solvers (this evaluates a candidate's residual; they time-step). `a` is a sweep parameter.
- `solver/ga_search.py::ga_minimize` — generic real-coded GA (tournament + BLX-α + annealed Gaussian
  mutation + elitism; no scipy; deterministic per seed). Problem-agnostic (Route-D reusable).
- Parametric genomes: `odd_rational` (one-scale/De-Gregorio; K=1 @ (−4,4) = exact Ω₀), `even_lorentz`
  (two-scale bump symmetry).

**a=0 KNOWN-ANSWER GATE (passes):** exact Ω₀=−4X/(1+4X²) nulls R to RMS **2.2e-7** (c_ω=−0.99914);
velocity integrates to arctan(2X) (bulk err 8.5e-3; tail error where Ω_X→0, harmless); odd parity
1e-13; a≠0 breaks the a=0 profile (R climbs ~linearly in a — the map's target). The GA recovers the
exact steady set — but as a **1-parameter DILATION FAMILY** {A=−4β,B=4β²}: the rescaling gauge is
dilation-invariant, so only the invariant **A²/B=4.000** (and the shape) is a "match" (Fig16A = a
valley, not a basin). Pinning B=4 → A=−3.9999. This is the banked "report gauge-invariants only"
lesson appearing in the optimization landscape itself.

**DIAGNOSTIC LOCKED (the crux, pre-any-logged-run):**
- **D1 scale separation (primary):** L_wid/L_loc → 0 with log-log slope c_l/c_s=2 ⟺ two-scale;
  O(1) ⟺ one-scale.
- **D2 blowup power (confirm):** invariant c_l/c_ω = −2/3 (two-scale, c_ω=−3/2) vs −1 (one-scale).
- **Resolution guard (mandatory):** D1 valid only while L_wid spans ≳8 grid pts; below → INCONCLUSIVE
  / "needs adaptive mesh", NEVER "scales merged" (same floor that capped B1/§6).

**DIAGNOSTIC REFINED AT DERIVATION TIME (honest correction to the pre-derivation D1/D2 above).** Once
the two-scale residual was actually derived (below), "two-scale" turned out to mean an EVEN, TRAVELING
(c_tw≠0) localized profile — a pure traveling wave, NOT a dilation scale-separation object. So the
logged sweep measures the scale-invariant residual FLOOR + the traveling speed c_tw + the profile
symmetry/width, not the L_wid/L_loc slope. The resolution guard (≳8 grid pts, else INCONCLUSIVE) was
kept verbatim and PASSED (min 49 pts). D1/D2's exponent framing belongs to the *blowup*, not the
traveling-wave *profile* the GA maps; noting the swap here so the record is honest.

### §9 (cont.) — TWO-SCALE RESIDUAL DERIVED + a-SWEEP LOGGED (2026-07-26). 5/6 PARTIAL. Novel, Tier-1/2.

**THE DERIVATION (the hard part, now done).** HQW25 §2.4: the two-scale blowup profile is an EXACT
TRAVELING WAVE. Carry ω=(T−t)^{c_ω}Ω(z), z=(x−r(t)(T−t)^{c_s})/(T−t)^{c_l} (c_ω=−3/2,c_l=1,c_s=1/2)
through gCLM ω_t+a u ω_x=ωHω. Leading (T−t)^{−3} balance: the dilation −c_l XΩ_X and amplitude c_ω Ω
terms are SUBLEADING ((T−t)^{−5/2}) and DROP; the moving-frame term survives as a pure TRANSLATION.
Advection enters at the SAME order as stretching. Result:
  **R₂(Ω) = Ω H(Ω) − c_tw Ω_X − a U Ω_X**,  U=∫₀ˣHΩ,  c_tw=c_s·r  (traveling-wave speed = gauge).
STRUCTURALLY a translation (const×Ω_X), NOT the one-scale dilation (X×Ω_X). a=0 anchor (a=b=c=1 norm):
**Ω₂=−1/(1+X²), H(Ω₂)=−X/(1+X²), c_tw=1/2**; nulls R₂ to **1.5e-9**. EVERY even_lorentz A/(1+BX²) is an
exact a=0 TW with c_tw=−A/(2√B) → a=0 set is a **2-parameter scaling valley** (deeper form of "report
invariants"). Code: solver/gclm_family.py::{residual_two_scale, gauge_c_tw, residual_two_scale_relnorm,
clm_two_scale, rational_mixed}; tests test_gclm_family.py 11/11 (full suite 7 files green).

**THE FITNESS BUG (caught pre-lock).** Plain RMS ‖R₂‖ is NOT scale-invariant — GA drives amplitude→0
(c_tw→0), trivial null (scratch showed it). Use **relres=‖R₂‖/‖ΩHΩ‖** (scale-invariant; one-scale Ω₀
scores >0.1, not gamed). Pre-lock scout: floor INVARIANT across n=601/801/1201 & rho_max=8/10 (physical,
not tail artifact) + GA-converged. Config locked n=801, 6 seeds; predicate T1–T6 in the harness docstring,
committed 6fc1ff0 before the run.

**RESULT (5/6, commit-after-run).** T1 known-answer PASS (a=0 relres 5.8e-8). T2 persistence PASS
(a_p=0.40, relres<1e-2). T3 monotone-degradation PASS (floor→0.18 at a=1). T5 symmetry PASS (odd-frac
<0.013; mixed genome free to skew STAYS EVEN). T6 resolution-guard PASS (min 49 pts). **T4 FAIL =
GENOME-LIMITED (the honest headline):** at a=0.5 even-K3 cuts floor 4× (2.45e-2→5.6e-3) → K=2 map is a
genome-relative UPPER BOUND, survival boundary NOT sharply pinned (pre-committed INCONCLUSIVE branch,
reported). BUT a=1 K=3 does NOT rescue (1.83e-1→1.43e-1) → De Gregorio-end degradation robust.
**Picture:** HQW25's exact a=0 two-scale traveling wave DEFORMS SMOOTHLY under advection — no sharp
collapse, persists small-a, degrades to De Gregorio, stays even, advection SELECTS a scale (lifts the
valley). Fig17 (writeup/4_p2_lottery/p2_two_scale_sweep_evidence.py, rebuilds from writeup/data/p2_two_scale_sweep.json).
TECHNICAL/BLOG_P2_TWO_SCALE.md.

**HONEST CEILING + NEXT.** A GA proves nothing (Tier-1/2); this is a genuine NEW MAP (HQW25 anchor + §9
machinery), the lottery ticket's first scientific brick — but NOT a proof, NOT a Clay solve. Did NOT
re-run to chase T4 (the fail is the machine catching its own limit). NEXT candidates: (a) richer/spectral
genome or a Route-D interval-Newton on these guesses to sharpen a_p; (b) the SEPARATE coupled-system leg
(HL two-stage — HL is not a scalar gCLM member). Clay odds unchanged ~0.05%.

## §10 — ROUTE-D v1 DONE (2026-07-26): interval core + a=0 NK framing. Level-1 tooling + scoping, NOT a certificate.

The first brick on the RIGOR LADDER (Level-1→Level-2). Delivered: (a) a hand-rolled rigorous
interval-arithmetic core solver/interval.py (no scipy/mpmath; outward-rounded +−×÷, reciprocal,
isum/dot/matvec with the γ_m accumulation bound) + test_interval.py 5/5 gated with `fractions` as the
exact oracle (full suite now 8 files green); (b) the deterministic a=0 probe experiments/p2_route_d_probe.py
→ writeup/data/p2_route_d_probe.json → fig19 (writeup/4_p2_lottery/p2_route_d_evidence.py). NOT a logged Tier run (no GA,
no seeds, no predicate lock — every number is a deterministic property of the anchor + fixed operators).
BLOG/TECHNICAL_P2_ROUTED.md.

FOUR evidence pieces (all banked, do not relearn):
  Q1 ARITHMETIC PRECISION. Rigorous interval enclosure of R₂ at the exact anchor Ω₂=−1/(1+X²), c_tw=1/2:
     defect 8.9e-10, enclosure WIDTH 8.5e-11 → overhead ~10% (n=2001). The interval core is precise enough
     to carry the NK defect bound Y₀. Genome-box sup|R₂| grows slope-1 (Lipschitz ~190), not wrapping.
  Q2 DEGENERACY COUNTED. a=0 zero set = 2-parameter scaling valley (amplitude (Ω,c)↦(λΩ,λc) + dilation
     (Ω,c)↦(Ω(·/μ),μc)). Jacobian SVs: gauge-slaved c → [2.0e-7,1.3e-7] (BOTH tiny = 2-dim kernel); fixed
     c=1/2 → [5.90,9.3e-7] (1-dim kernel). ⇒ EXACTLY TWO gauge conditions (speed + one normalization)
     isolate a nondegenerate zero. Concrete: fix c=1/2 + Ω(0)=−1 forces μ=1 (the c-preserving fiber is
     λμ=1, Ω(0)↦(1/μ)Ω(0)). The naive un-gauged interval-Newton has ‖DF⁻¹‖=∞ — gauge quotient NOT optional.
  Q3 DIAGONALIZATION (the structural gift). Under X=tan(θ/2) the LINE Hilbert transform = the CIRCULAR
     conjugate (cos kθ↦sin kθ), verified ~1e-7 for k=1..6 on the DECAYING (endpoint-vanishing at θ=±π)
     subspace. Anchor is then a 2-term Fourier object: Ω₂=−(1+cosθ)/2 (a₀=a₁=−1/2), H(Ω₂)=−½sinθ.
  Q4 BANDED OPERATOR. R₂ is ODD (Ω even ⇒ ΩHΩ,Ω_X odd) ⇒ DF maps cosine→sine coeffs. With Ω₂ degree-1,
     DF is TRIDIAGONAL (bandwidth 1) + a rank-1 c_tw column (−Ω₂,ₓ=−½sinθ−¼sin2θ). Closed-form band built
     in the probe (q4_operator_structure), cross-checks the grid operator to 3.9e-2 (the residual = the
     θ=±π Cayley endpoint correction = flagged sub-task R). Banded ⇒ finite-section NK bounds Z₀+Z₁<1 are
     PLAUSIBLE (tail dominated by c·(ik), O(1/(cN)) inverse bound).

THE FRAMING (writeup/4_p2_lottery/TECHNICAL_P2_ROUTED.md §7; full paper draft was scratch/ROUTE_D_FRAMING.md). Standard
radii-polynomial NK: Y₀≥‖A F(x̄)‖, Z₀≥‖I−AA†‖, Z₁≥‖A(A†−DF)‖, Z₂≥‖A·D²F‖; p(r)=Z₂r²−(1−Z₀−Z₁)r+Y₀;
CLOSES iff Z₀+Z₁<1 and (1−Z₀−Z₁)²≥4Y₀Z₂. Two real simplifications: F QUADRATIC ⇒ Z₂ constant (no 3rd-order
term); anchor a finite trig poly ⇒ zero convolution tail. Space: weighted ℓ¹_ν cosine coeffs ⊕ ℝ.
OPEN RISKS (honest, do not drop): G = the exact gauge/Fredholm-index square system (fixed-c+1-norm vs
c-floating-bordered) — THE CRUX; R = the θ=±π endpoint rank-1 correction (the 3.9e-2); T = rigorous
O(1/(cN)) tail-inverse bound; a≠0 = no exact anchor off a=0 (Y₀ jumps ~1e-9→~1e-2) so a boundary certificate
likely will NOT close — probable honest "certifies at a=0, not yet at a≈0.5".

NEXT BRICK (user-confirmed direction): the FLOAT DRESS REHEARSAL — build DF as a finite (N+1)-mode matrix in
plain float, invert the finite section, compute Y₀/Z₀/Z₁/Z₂ + the radii polynomial across an N-ladder with
the §Q2 gauge. Answers the ONLY gating question — does Z₀+Z₁<1 and does the ball close at the anchor? — at
near-zero cost BEFORE any interval hardening. Green-lights the verified build or surfaces which sub-task
(G/R/T) blocks it (a legit publishable negative either way). Only after it closes in float do we harden with
solver/interval.py. HONEST CEILING unchanged: even full success = computer-assisted TOY-MODEL certification
(Chen–Hou / Gómez-Serrano genre), NOT a Clay solve. Clay odds ~0.05%.

## §11 — ROUTE-D v2 DONE (2026-07-28): the FLOAT DRESS REHEARSAL. **The NK ball does NOT close** — a
## structural NEGATIVE with a constructive repair. Level-1 tooling + scoping, NOT a certificate.

The §10 "next brick", executed. Built solver/nk_fourier.py (the EXACT closed-form Fourier operator — no
grid, no quadrature) + test_nk_fourier.py 6/6 (suite now **9 files green**); ran the deterministic ladder
experiments/p2_route_d_dress.py → writeup/data/p2_route_d_dress.json → fig20
(writeup/4_p2_lottery/p2_route_d_dress_evidence.py). NOT a logged Tier run (deterministic; no GA/seeds/
predicate lock). BLOG/TECHNICAL_P2_ROUTED_DRESS.md.

**HEADLINE: the radii polynomial closes at NO truncation (0/13 on N=4..256), and the measurements show it
CANNOT — at any N, under any gauge, with any positive weight. Cause located and confirmed by ablation:
the transport term c(1+cosθ)∂_θ DEGENERATES at θ=±π (X=∞).** Certification budget
Y₀^max=(1−Z₀−Z₁)²/(4Z₂) is IDENTICALLY ZERO at every N. (So the §10 worry that a≠0's Y₀~1e-2 would be too
big was beside the point: the apparatus cannot certify defect ZERO either.)

Exact operator (banked; supersedes the grid version for Route D):
  H(cos kθ)=sin kθ for EVERY k≥0, H(1)=0 — UNCONDITIONAL (Hardy/Cayley: e^{iθ}=(1+iX)/(1−iX) holomorphic in
  the UHP, G_k=e^{ikθ}−(−1)^k decays, H(Re G)=Im G). §10 Q3's "on the decaying subspace" caveat is
  unnecessary. f_X=(1+cosθ)f_θ. Anchor a=(−1/2,−1/2,0,…), c=1/2 nulls the residual EXACTLY (both terms are
  sinθ/4+sin2θ/8) — a sharper gate than the grid's 1e-9. Kernel directions in closed form: amplitude
  (½,½,0,…;δc=−½), dilation (⅛,0,−⅛,0,…;δc=−¼); fixed-c kernel w=−¼cosθ(1+cosθ)=(−⅛,−¼,−⅛,0,…).

SIX evidence pieces (do not relearn):
  D1 LADDER. ‖A_N‖_{ℓ¹} ~ N^0.97 (5.0→198.7 over N=4→256), σ_min ~ N^−0.98, cond ~ N^2.03. The gauged
     finite-section inverse is UNBOUNDED ⇒ not boundedly invertible in unweighted ℓ¹ ⇒ no truncation can
     certify. Y₀=0.0 exactly (anchor is an exact zero AND a degree-1 trig poly ⇒ zero convolution tail).
  D2 BOUNDS. Z₀~1e-11 (rounding only). Z₁ ≥ N+1 EXACTLY from the truncation coupling alone (5,17,65,257 at
     N=4,16,64,256) — the finite section couples MORE strongly to what it discards as N grows; bigger is
     strictly WORSE. Z₂=2‖A‖ diverges. Even the fiction "ignore the far field" does not close at any N.
  D3 GAUGE EXONERATED. origin / a0 / a1 normalizations ALL give N^0.97, curves on top of each other.
     **Sub-task G is NOT the blocker** (it still must be right for a real certificate, but it is cleared here).
  D4 CAUSAL ISOLATION (the decisive test). Replace the transport factor (1+cosθ)→1, change nothing else:
     ‖A_N‖ goes FLAT at exactly 4.0 (N^0.00) vs 198.7 (N^0.97). **Sub-task R (the θ=±π far field) is the
     CAUSE, not a suspect** — promoted from footnote to blocker.
  D5 FAR-FIELD MARGINALITY. Far-field DF columns are exactly tridiagonal (sub,diag,sup)=(ck/2, ck−½, ck/2−½).
     The Z₁ column weight → 1 from BELOW under the transport-diagonal tail model and from ABOVE under the true
     diagonal, both at O(1/k), c-independently ⇒ sup_{k>N} = 1 for every N; NOT a tail-model artifact. Root
     cause: multiplication by the symbol 1+cosφ has ℓ¹ norm 2 = exactly 2× its mean, because it VANISHES at
     φ=π. **No positive weight repairs it** (proof: z_w(k)≈(u_{k−1}+u_{k+1})/(2u_k), u_k=w_k/k; z_w≤1−δ forces
     u_{k+1}≤2(1−δ)u_k−u_{k−1} whose characteristic roots lie ON the unit circle ⇒ oscillation ⇒ any positive
     solution goes negative). Best possible = u affine (w_k=k(α+βk)) giving z_w≡1. Numerics agree.
  D6 THE REPAIR (the constructive half). Far-field ODE −c h_X − h/X = g with c=1/2 ⇒ (X²h)′=−2X²g ⇒
     h=2X^{−2}∫_X^∞ s²g ⇒ the inverse LOSES EXACTLY ONE POWER OF DECAY. Mode m resolves X~m, so predict
     ‖A e_m‖_{ℓ¹} ∝ m; MEASURED 1.97·m (fit on m≤N/8; the roll-over at m→N is the finite-section edge, where
     ‖A e_N‖=4 exactly at every N). Grade the CODOMAIN by one mode power (v_m=m, gauge row 1):
     **‖A‖ = 3.000, FLAT from N=8 to N=384 (N^0.00).** Other pairings diverge (ℓ¹→graded: N^1.94;
     graded→graded: N^0.95). ⇒ the certificate needs an ASYMMETRIC space pair one decay power apart.

BUG FIXED in the §10 probe: the closed-form band's k=0 column had an unfolded sin(−θ) (−1/4 instead of
−1/2); v1's grid cross-check only ran k≥1 so it never exercised the fold. experiments/p2_route_d_probe.py
fixed + cross-check extended to k=0; the two independently-written closed forms now agree to 0.0. Grid
cross-check unchanged at 3.9e-2 (that residual is the θ=±π endpoint correction, a different thing). Also
added the missing sys.path bootstrap to that probe.

NEXT BRICK (specification, NOT a promise): rebuild the bounds in the GRADED pair — domain ℓ¹ cosine coeffs,
codomain graded by one mode power, far-field block handled by the EXACT ODE inverse above instead of a
diagonal model (the standard "compact core + explicit far field" two-region structure of the Chen–Hou /
Gómez-Serrano genre). TWO things must be re-derived and neither is free: (i) the quadratic D²F[h,h]=2hH(h)
must land in the GRADED codomain — the Wiener-algebra bound only gives ℓ¹, so the DOMAIN norm likely has to
move too; (ii) the far-field inverse must be interval-enclosed, not asymptotic. Alternative lanes if that
stalls: the separate coupled-system HL two-stage leg, or extending the a_p(K) map to the odd/one-scale
channel (lower value). HONEST CEILING unchanged: everything in §11 is plain float64, nothing is
interval-enclosed, nothing is rigorous — running the rehearsal FIRST is exactly what saved hardening a set
of bounds that could never have closed. Clay odds ~0.05%.

## §12 — ROUTE-D v3 DONE (2026-07-30): the SPACE-PAIR SCOPING LEG. **A NO-GO THEOREM for the whole
## weighted-ell^1 category** (which retires v2's own repair), plus the decay-graded pair that replaces it.
## Level-1 tooling + scoping, NOT a certificate.

The §11 "next brick", with its own gating condition discharged FIRST as §11 instructed: before rebuilding in
the graded pair, check on paper that the quadratic D^2F[h,h] = 2hH(h) lands in the graded codomain. It does
not — and neither does any other diagonal-weight choice. Built solver/decay_grading.py + test_decay_grading.py
7/7 (suite now **10 files green**); ran the deterministic probe experiments/p2_route_d_v3_spaces.py ->
writeup/data/p2_route_d_v3_spaces.json -> fig21 (writeup/4_p2_lottery/p2_route_d_v3_evidence.py). NOT a
logged Tier run. BLOG/TECHNICAL_P2_ROUTED_SPACES.md.

**HEADLINE: over the entire two-parameter family of diagonal weights u_k=(1+k)^s, v_m=(1+m)^t, both NK
requirements depend only on the GAP g = t-s, and their growth exponents are EXACT COMPLEMENTS:
||A_N||_{Y->X} ~ N^(1-g) and the sharp quadratic constant S_K ~ K^g. A certificate needs BOTH to be 0; the
SUM is >=1 everywhere (=1 on 0<=g<=1). Measured minimum over the whole family: 0.98. The one power the far
field loses must be paid by one bound or the other; the weights only choose WHICH.**

SIX evidence pieces (do not relearn):
  S1 THE PURE-CONVOLUTION IDENTITY. Q(h) = hH(h) = (1/2) sum_m (sum_{j+k=m} h_j h_k) sin(m th) — NO
     difference frequencies (h+iH(h) is a Hardy boundary value, 2hH(h) = Im of its square, squaring a
     holomorphic function only adds frequencies). Independent second build vs nk_fourier.residual agrees to
     3.2e-17 (0.0 at the anchor). Sharp weighted constant: ||Q(h)||_Y <= M||h||_X^2 for all h  <=>
     S := sup_{j,k} v_{j+k}/(u_j u_k) < oo, with S/4 <= M <= S/2 (necessity via h = xi e_j + eta e_k
     optimized). Unweighted S=1 => M=1/2, **2x sharper than the Wiener constant v2 used** (changes no v2
     conclusion; its budget was identically zero).
  S2 WHAT THE INVERSE COSTS. Minimal admissible codomain weight v_m^min(u) = ||A e_m||_{ell^1_u}; the ratio
     v_m^min/(m u_m) is O(1) (1.3–3.2) across s in [0,2] and m in [2,32]. The price really is exactly one
     mode power, for weighted domains as well as flat (s=0 reproduces v2's 1.97m).
  S3 THE NO-GO, PROVED AND MEASURED. Proof: S<oo with k=0 gives v_m <= S u_0 u_m, i.e. v_m/u_m BOUNDED; a
     bounded inverse needs v_m/u_m >~ 2m. Incompatible, with a margin growing linearly in m. (If a_0 is
     gauged out, take k=1 and any non-decreasing weight: same conclusion.) Mechanism in words: the constant
     mode multiplies at FULL strength, e_0 H(h) = H(h), no decay gained. Measured: region I (A bounded)
     t >= s+1, region II (quadratic bounded) t <= s, strip between them EMPTY; boundaries pinned
     grid-independently ON the candidate lines (t=s-1: 1.96, t=s: 0.98, t=s+1: 0.00–0.06; algebra t=s: 0.00,
     t=s+0.25: 0.25 — all flat in s).
  S4 THE CONTROL. (1+cos th) -> 1, nothing else changed: the inverse boundary falls from t >= s+1 to
     t >= s-1 — **TWO powers**, exactly the order to which 1+cos th vanishes at th=+-pi (a non-degenerate
     first-order transport GAINS one power on inversion; this one LOSES one). Min exponent sum 0.98 -> 0.00;
     overlap 0/9 -> 9/9 values of s. The obstruction is this operator's far field, not the method.
  S5 THE RESONANCE (both sides). Far-field model L h = -c h_X - h/X between DECAY-graded sup norms
     (sup X^a|h| ; sup X^(a+1)|g|): **||L^-1|| = 2/|alpha-2|**, measured to <=0.008% vs the exact
     finite-domain value over 15 alphas (2nd-order trapezoid in tau=log X on [1,1e12]; M-matrix so the
     induced norm is ONE pass). Operator side, no ODE model and no quadrature:
     lim X^(a+1) DF[f_a] = c*alpha - 1 = (alpha-2)/2, measured to <=0.3%. The pole at alpha=2 is structural:
     X^-2 is BOTH the homogeneous far-field solution at c=1/2 AND the decay of the anchor Omega_2. **v2's
     "loses exactly one power" IS this resonance seen at integer grading** (generic alpha loses nothing;
     alpha=2 loses a log; integer weights round that to a full power). Admissible window 1<alpha<2
     (alpha>1 for integrability; alpha<2 because Omega_2 H(h) ~ X^-3 would otherwise dominate).
  S6 THE PAIR THAT WORKS + ITS PRICE. In X={|h| <~ X^-a}, Y={|g| <~ X^-a-1} EVERY term lands in Y: transport
     and hH(Omega_2) exactly, Omega_2 H(h) faster, and **the quadratic exactly** — because
     H(h)(X) -> (int h)/(pi X) for integrable h, so hH(h) decays ONE POWER FASTER than h. Verified against
     the closed form int f_a = sqrt(pi) Gamma((a-1)/2)/Gamma(a/2) (<0.1% after fitting the known O(X^(1-a))
     second term). Price: far-field 2/(2-a) vs quadratic constant (int f_a)/pi -> **INTERIOR OPTIMUM
     alpha* ~ 1.44** (3/2 within 1%; broad — within 1% over [1.35,1.55]), Z2 ~ 13.3, budget ~1/(4Z2) ~ 1.9e-2.
     => certify profiles decaying like X^-3/2 with residuals measured in X^-5/2, deliberately NOT the
     anchor's own X^-2. SCOPING ESTIMATE ONLY: leading-order far-field constants, no compact core, float64.

WHAT CHANGES FOR ROUTE D. RETIRED: v2 D6's literal recipe ("grade the codomain by one mode power; that is the
pair"). The measurement was right, the inference was not — in that pair Z2 diverges exactly as fast as ||A||
converges. ESTABLISHED: the whole diagonal-weight category is closed, with a proof, a 2-parameter sweep, a
grid-independent boundary check, and a causal control. SPECIFIED: the replacement is a decay-graded
(two-region) pair with alpha ~ 3/2 and Z2 ~ 13. STILL OPEN (unchanged): the compact-core block; a rigorous
ENCLOSURE of the far-field inverse rather than an asymptotic one; core/far-field matching; and a != 0.

HONEST CEILING unchanged: plain float64 throughout, nothing interval-enclosed, no rung climbed. Z2 ~ 13
implies a budget ~1e-2 BEFORE the compact core, Z1 and interval overhead are paid, against an a != 0 residual
floor of ~1e-2 — the margin, if any, is thin, and it is better to know that from an afternoon of algebra than
after building a two-region solver. Clay odds ~0.05%.

## §13 — ROUTE-D v4 DONE (2026-07-30): THE FULL OPERATOR IN THE DECAY-GRADED PAIR. v3's far-field pricing
## CONFIRMED; a SECOND structural requirement on the space found. Level-1 tooling + scoping, NOT a certificate.

The §12 "next brick" (the compact-core block), executed. Every number v3 produced came from the far-field
MODEL operator L h = -c h_X - h/X — no Hilbert coupling, no core, no gauge — so the obvious failure mode was
that the core contributes something the model cannot see. Built solver/decay_collocation.py (nodal spectral
collocation on the midpoint theta-grid with weighted sup norms; the THIRD independent construction of this
operator — v1/v2/v3 were all coefficient-space) + test_decay_collocation.py 6/6 (suite now **11 files
green**); ran experiments/p2_route_d_v4_graded.py -> writeup/data/p2_route_d_v4_graded.json -> fig22
(writeup/4_p2_lottery/p2_route_d_v4_evidence.py). NOT a logged Tier run. BLOG/TECHNICAL_P2_ROUTED_V4.md.

**HEADLINE (a): v3's far-field estimate STANDS.** On a in [1.4,1.7] the model law 2/|a-2| predicts the FULL
gauged inverse norm to 6% (2% on [1.5,1.7]); Z2_min = 13.4 at a~1.5 against v3's 13.3 at 1.44; C_Q on smooth
data matches v3's closed form (int f_a)/pi to <2% for a>=1.3. The compact core costs almost nothing.
**HEADLINE (b): the decay-graded SUP pair does NOT control the quadratic.** H is unbounded on L^inf, so no
purely-sup norm can bound Q(h) = hH(h). The space needs a SMOOTHNESS component as well as the decay grading.

SIX evidence pieces (do not relearn):
  W1 THE THIRD BUILD reproduces v2's negative + v3's repair: ungraded ||A|| 11.9->17.4 over J=125..2000
     (+1.37/doubling, ~J^0.13, no sign of stopping), graded (a=3/2) 3.79->4.07 (~J^0.017, increments
     halving, settling ~4.07). NOTE the divergence is LOGARITHMIC in sup norms vs LINEAR (N^0.97) in v2's
     ell^1 — different norm, milder slope, same verdict. Gates: collocated residual/jacobian/dc-column agree
     with nk_fourier to 2.6e-13; anchor an exact zero (6.5e-13); both kernel directions annihilated.
  W2 THE CORE IS CHEAP. ||A||: 4.07(a=1.05), 3.81(1.2), **3.54(1.4)**, 4.07(1.5), 5.06(1.6), 6.58(1.7),
     9.29(1.8), 14.39(1.9) vs 2/|a-2| = 2.11, 2.50, 3.33, 4.00, 5.00, 6.67, 10.0, 20.0. Core excess +1.97 at
     1.05 falling to +0.07 at 1.5. **The full ||A|| has its OWN interior minimum at a~1.40** (far-field price
     rises toward the a=2 resonance, core price toward a=1) — a second, independent argument landing on the
     same a. CAVEAT: at a>=1.8 the negative "core excess" is NOT a core effect, it is incomplete J-convergence
     (J-exponent 0.108 at a=1.9; finite-domain correction (X0/Xmax)^(2-a) = 43% there).
  W3 THE MISSING HALF. ||Q(h)||_Y <= ||h||_X sup (1+X^2)^{1/2}|H(h)|, so the quadratic reduces to: is H
     bounded X_a -> X_1? NO — classical. Demonstrated with the CONJUGATE-EXTREMAL family p_m = the degree-m
     Fourier partial sum of sign(cos th) (bounded ~1.18 by Gibbs, ||H p_m||_inf >= (2/pi) log m at the jump
     th=pi/2, i.e. X=1, where BOTH weights are O(1)): C_Q = 0.74,1.26,1.81,2.40,2.73 over m=4..512, +0.41 per
     e-fold. **METHODOLOGICAL: the first version of this test used RANDOM perturbations of the same degree —
     they FALL (1.40->0.84) and reported the quadratic as comfortably bounded.** Sampling can refute a
     proposed bound and can give a lower bound; it can NEVER establish boundedness and cannot reveal
     unboundedness. You must BUILD the adversary.
  W4 THE PRICE. Z2 = 2||A||C_Q with C_Q on the smooth family: 22.2(1.2), 17.0(1.3), 13.6(1.4), **13.4(1.5)**,
     14.6(1.6), 21.7(1.8); budget CEILING 1/(4Z2) <= 1.9e-2 at a~1.5. A CEILING: assumes Z1=0 and prices no
     smoothness component. Against an a!=0 residual floor ~1e-2 the margin is thin — thinner than v3's number,
     which was itself a ceiling.
  W5 OPERATIONAL. The gauge must replace a CORE collocation equation: dropping rows at X=0.001/0.4/1.0 gives
     ||A|| = 4.03/4.41/5.70, but dropping the OUTERMOST (X=1273) gives **1.06e5** — the far field goes
     unconstrained. Gauge spread (origin vs a0) 1.7x, core-row spread 1.4x: modest, consistent with v2 D3.
  W6 THE Z1-ANALOGUE, QUANTIFIED NOT BOUNDED. Decay-class elements are not band-limited (f_a is only C^a at
     th=pi), so collocation truncates them: graded-codomain error vs the exact operator 6.6e-3->9.3e-5
     (J^-2.08) at a=1.2, 3.3e-3->2.6e-5 (J^-2.36) at 1.5, 9.7e-4->4.3e-6 (J^-2.64) at 1.8. Clean algebraic
     convergence, NOT a bound. Nothing closes without it.

**THE UNIFIED STATEMENT (carry this forward).** v3: a diagonal weight on Fourier coefficients measures
SMOOTHNESS; we needed DECAY. v4: a weighted sup norm measures DECAY; we also need SMOOTHNESS. Two legs, two
one-parameter families, each missing exactly what the other has — the far-field transport forces a decay
grading, the Hilbert transform forces a smoothness scale, and the certificate's space must carry BOTH at
once. Natural candidates: weighted Holder C^{0,gamma} with a decay weight (Holder is where H IS bounded), or
a decay-adapted basis carrying a smoothness-graded ell^1. That is the §14 question and — following the rule
that has now paid off twice — it should be settled ON PAPER before any solver is written.

HONEST CEILING unchanged: plain float64, nothing interval-enclosed, no rung climbed. Clay odds ~0.05%.

## §14 — ROUTE-D v5 DONE (2026-07-30): THE TWO-GRADING SPACE (decay x smoothness). v4's obstruction REMOVED;
## one marginal direction left, with a nearly-free fix. Level-1 tooling + scoping, NOT a certificate.

The §13 "next brick", done on paper first as the rule requires. v3 and v4 each found half of one requirement
(v3: weights measure smoothness, we needed decay; v4: sup norms measure decay, we also need smoothness), so
the space must carry BOTH. Built solver/holder_norms.py + test_holder_norms.py 6/6 (suite now **12 files
green**); ran experiments/p2_route_d_v5_holder.py -> writeup/data/p2_route_d_v5_holder.json -> fig23
(writeup/4_p2_lottery/p2_route_d_v5_evidence.py). NOT a logged Tier run. BLOG/TECHNICAL_P2_ROUTED_V5.md.

THE SPACE: ||h||_{a,g} = sup w^(a)|h| + sup_{j!=k} min(w^(a-g)) |dh| / |dth|^g, w^(b) = (1+X^2)^{b/2}.
**The seminorm weight is a-g, NOT a, and it is FORCED**: the exact Jacobian dX/dth = (1+X^2)/2 turns the
conformal far-field seminorm (1+X^2)^{(a+g)/2}|dh|/|dX|^g into 2^g (1+X^2)^{(a-g)/2}|dh|/|dth|^g -- the g in
the exponent is eaten by the Jacobian. The first draft used weight a, under which **f_alpha itself has
infinite seminorm** (the space would not contain the object the certificate is about); the numerical
conformal check caught it. Second time in three legs a cheap check has caught an algebra slip. PAYOFF: after
the identity, the whole weighted-conformal seminorm is a PLAIN theta-Holder seminorm with a diagonal weight
-- no local windows, no scale-dependent pair selection, one O(J^2) broadcast. That is the only reason this
leg was cheap. Checked pointwise (alpha-independent: the ratio is the Jacobian identity to the g) to 0.04%
out to X~121.

FIVE evidence pieces (do not relearn):
  U1 THE DEFUSAL. v4's adversary p_m (degree-m partial sums of sign(cos th), bounded ~1.18 with conjugate
     ~ (2/pi)log m): sup ratio x2.26 over m=8..512 AT EVERY gamma (it does not care about the decay weight
     -- v4's point); Holder ratio x1.41 (g=0.15), **x0.96 (g=0.35), x0.83 (g=0.5), x0.76 (g=0.85)**. Defused
     for g >~ 0.35. Mechanism: in a Holder norm the adversary pays for its own oscillation ([p_m]_g ~ m^g in
     the denominator). Failure at small g is expected -- g->0 IS the sup norm.
  U2 SMOOTHNESS HAS ITS OWN INTERIOR OPTIMUM. C_H(g) = 1.60, 1.21, **1.12**, 1.13, 1.18, 1.20, 1.29 for
     g = 0.15..0.85 -- a BOWL, min at g~0.35-0.5, rising at both ends for different reasons (g->0 is the sup
     norm where H is unbounded; g->1 is Lipschitz where H fails again). **Same shape as decay** (v4: ||A||
     bowls at alpha~1.4 from far-field vs core). Two gradings, two interior optima, four unrelated
     mechanisms. Caveat: C_H is a max over a finite family = a lower bound; the g->1 rise is under-resolved.
  U3c THE ONE MARGINAL DIRECTION. The coarse (a,g) sweep and a focused ladder disagreed about J-saturation;
     the cause is which test direction dominates. Residuals g = f_{a+1+delta} at a=1.5, g=0.5:
     **delta=0 (the codomain's CRITICAL rate) creeps 1.956->2.879 over J=125..2000 (J^+0.14, a LOG), while
     delta=0.1/0.25/0.5/1.0 are FLAT TO 4 S.F. across a 16x range in J** (1.777, 1.763, 1.711, 1.597).
     This is v3's resonance one level down: the far-field inverse gives a log exactly at the critical
     exponent, a clean power otherwise. SAME FIX: keep the residual class OPEN (decay strictly faster than
     X^-(a+1)). **This detuning is nearly FREE and the constants go DOWN with delta** -- unlike v3's 2/eps --
     because it TIGHTENS the codomain rather than LOOSENING the domain off its own kernel.
  U4 THE QUADRATIC. At a=1.5, adversary growth over m=8..512: x1.63 (g=0.15), x1.13 (0.25), **x0.77 (0.35),
     x0.42 (0.5), x0.11 (0.85)**; C_Q (smooth family dominates) 0.86..1.14. v4's sup-pair value was 2.73 at
     m=512 AND STILL CLIMBING. Transition at g~0.3, consistent with U1.
  U5 THE JOINT OPTIMUM (defused region g>=0.35): (a,g) = (1.8, 0.35), ||A||=2.45, C_Q=0.67, **Z2 = 3.29**
     (v4: 13.4), budget ceiling **7.6e-2** (v4: 1.9e-2) -- about 4x better. FOUR reasons not to celebrate:
     (i) ||A|| is FAMILY-RESTRICTED, a lower bound (the exact induced norm between two polyhedral norms is an
     LP and this project has no scipy), so Z2 is a lower bound and the ceiling an upper bound on an upper
     bound; (ii) C_Q likewise; (iii) Z1 is STILL not bounded anywhere in Route D; (iv) the argmax sits at
     a=1.8, the edge of the swept grid, in a row with an unconverged-J artifact near the a=2 resonance --
     the optimum's LOCATION is not firm, its EXISTENCE is.

WHAT CHANGES FOR ROUTE D. RESOLVED: v4's quadratic obstruction; the two-grading space exists, is cheap to
compute in, and its constants are single digits rather than tens. NEWLY IDENTIFIED AND FIXED: the
critical-rate marginality, at almost no cost. STILL OPEN (the whole list): Z1 (quantified in v4 at
J^-2.1..-2.6, never bounded -- now the LARGEST gap and no longer a scoping question); exact (not
family-restricted) operator norms, which need an LP or an analytic Holder-to-Holder estimate (the analytic
route is more likely: closed-form far field + finite-dimensional core); interval arithmetic
(solver/interval.py has existed since v1 and has still never been pointed at any of this -- correctly, since
nothing has closed in float); and a != 0 (no exact anchor, floor ~1e-2 against a 7.6e-2 ceiling that has not
paid its debts).

HONEST CEILING unchanged: plain float64, nothing interval-enclosed, no rung climbed. Clay odds ~0.05%.

## §15 — ROUTE-D v6 DONE (2026-07-30): the FIRST GENUINE UPPER BOUNDS + the DISCRETE-BALL TRAP.
## Three of eight NK constants move from MEASURED to BOUNDED. Still NOT a certificate.

The §14 "next brick" (bound Z₁; turn family-restricted norms into real upper bounds). Built
solver/nk_bounds.py + test_nk_bounds.py 6/6 (suite now **13 files green**); deterministic ladder
experiments/p2_route_d_v6_bounds.py → writeup/data/p2_route_d_v6_bounds.json → fig24
(writeup/4_p2_lottery/p2_route_d_v6_evidence.py). NOT a logged Tier run. BLOG/TECHNICAL_P2_ROUTED_V6.md.

**THE FRAMING PROBLEM v1–v5 ALL SHARED (say it plainly): every constant reported through v5 was a
family-restricted maximum = a LOWER bound, and Z₁ was never bounded at all. A budget assembled from
lower bounds is not a quantity a certificate can use.** v6 fixes part of that and disqualifies the
obvious method for the rest.

SIX evidence pieces (do not relearn):
  B1 **THE DISCRETE-BALL TRAP (the methodological headline).** Computing an induced norm by DUALITY
     over the DISCRETE unit ball is UNSOUND. A discrete Hölder seminorm only inspects pairs of GRID
     NODES, so duality's extremizer is a grid-scale sign pattern whose interpolant thrashes between
     nodes. Measured over the same θ-range, its continuum/discrete norm ratio is **3.0e3 (J=125) →
     5.0e4 (J=500), ~J^2.03**, while a smooth element of the same class stays faithful to 3%. The
     "worst direction" is not within 4 orders of magnitude of the unit ball. It reported ‖A‖ ~ J^0.5
     (unbounded) under THREE independent routes and EVERY gauge-row choice — all fiction.
  B2 **WHAT SURVIVES.** Use only inequalities the CONTINUUM norm implies: |g_m| ≤ ‖g‖/v_m and
     |g_m−g_{m₀}| ≤ ‖g‖/q_{m,m₀}. Then ‖c‖_{Y*} ≤ min_{m₀}[|Σc_m|/v_{m₀} + Σ|c_m|/q_{m,m₀}]
     (two_point_dual; minimising over a SUBSET of m₀ stays valid). Domain **SUP part SATURATES:
     5.536→5.631 over J=125..1600 (J^+0.006)** = the project's FIRST uniform upper bound on any part
     of ‖A‖, bracketing v5's family lower bound (~2.2–2.9) by ~2×. Domain SEMINORM part is valid but
     LOSSY (J^+0.496 = J^γ) — B1 says exactly why (it is still pricing the fake direction).
     Continuum expectation: it IS finite (the inverse gains a whole derivative, h_X=−(g+H(h)+Xh)/c ⇒
     g∈C^{0,γ} puts h∈C^{1,γ}). **Closing this is now the sharpest open question in Route D.**
  B3 **THE MODELLING IDENTITY (exact).** (DF−L)h = h/(X(1+X²)) − H(h)/(1+X²), where L is v3's
     far-field model −c h_X − h/X. Verified vs the collocation operator to **1.5e-16 relative**.
  B4 **THE FAR-FIELD Z₁ BOUND = the first bounded piece of Z₁ in six legs.** Split the p.v. at
     half-scale on the **EVEN kernel K(X,y)=2X/(X²−y²)**: singular half charged to the Hölder
     seminorm, rest to the decay envelope. X-side Hölder envelope is
     2^γ(1+X_min²)^{−(α+γ)/2} — **weight α+γ, NOT α−γ** (v5's θ-weight pushed through
     |dθ|≤2|dX|/(1+X_min²)). Using the EVEN kernel is NOT cosmetic: the two-sided 1/(X−y) split
     DIVERGES logarithmically as X→0 (where the truth is 0 by parity) and loses a factor 2 far out;
     the even form is finite at 0 and recovers the SHARP constant (X·bound→1.681 vs M_α/π=1.669).
     Validated on RESOLVED nodes (|X|dθ≤1): X₀=20/50/100 → headroom 3.0×/1.7×/1.1×. Decays at the
     predicted X₀^{α−2} for every α (measured −0.874…−0.240 vs predicted −0.9…−0.2).
     Same bound ⇒ **C_Q ≤ sup_X (1+X²)^{1/2}·B(X) = 3.13** at (1.5,0.5) (v5 family LB 0.86–1.14).
  B5 **PRICING Z₁ MOVES THE OPTIMUM — v5's (α,γ)=(1.8,0.35) IS DEAD.** At α=1.8, Z₁^far = 4.32/3.13/
     2.34 at X₀=200/800/3200 — all ≫ 1, no closure at any X₀. Structural: the modelling error decays
     like X₀^{α−2}, so α=1.8 needs the far field 10⁵× further out for the same margin, while
     ‖A‖=2/(2−α) runs away toward the α=2 resonance. **New optimum α≈1.2, conditional budget
     Y₀^max = 1.18e-2** (at X₀=3200). CAREFUL: the a≈0.5 GA residual floor is ALSO ~1e-2 — that
     coincidence is NOT a claim the boundary profile could be certified. The budget is CONDITIONAL and
     OPTIMISTIC (far-field Z₁ only; far-field ‖A‖, which v4 validated to 6% only on α∈[1.4,1.7], NOT
     where the optimum now sits; three constants omitted). Honest reading: the target is no longer out
     of reach by ORDERS OF MAGNITUDE. That is all.
  B6 **THE LEDGER.** EXACT: Y₀ (anchor). BOUNDED: Z₀; **Z₁ far-field modelling error (NEW)**;
     **‖A‖ domain sup part (NEW)**; **C_Q sup part (NEW)**. OPEN: Z₁ core↔far coupling (sharp split
     has a 1/(X−X₀) seam — H is nonlocal — so it needs a smooth cutoff + a commutator estimate);
     ‖A‖ domain seminorm part (three routes, all lossy); Z₁ core discretization (v4 W6 J^−2.1..−2.6,
     measured only). **Three of eight moved; three remain, now named precisely enough to attack one
     at a time rather than scoped.**

NEXT: the three open ledger items, in order of sharpness — (1) the domain-seminorm part of ‖A‖ (the
continuum argument says finite; find a computation that shows it, e.g. restrict to a band-limited
subspace with a quantified faithfulness factor, or bound via the C^{1,γ} gain); (2) the core↔far
smooth-cutoff commutator; (3) the core discretization. Only when ALL of Y₀/Z₀/Z₁/Z₂ are real upper
bounds should the float radii polynomial be assembled, and the same stopping rule applies: if it does
not close in float with margin, STOP, do not harden. solver/interval.py has existed since v1 and has
still never been pointed at any of this — correctly, because nothing has closed in float.
HONEST CEILING unchanged: plain float64, nothing interval-enclosed, nothing rigorous. Clay odds ~0.05%.

## §16 — ROUTE-D v7 DONE (2026-07-31): the DOMAIN SEMINORM PART OF ‖A‖, CLOSED BY A DERIVATIVE GAIN.
## The FIRST uniform upper bound on the WHOLE of ‖A‖ — and the first (α,γ) optimum made of upper
## bounds. Still NOT a certificate.

The §15 "next brick", item (1) — the sharpest of the three open ledger items. Built
solver/nk_seminorm.py + test_nk_seminorm.py 6/6 (suite now **14 files green**); deterministic ladder
experiments/p2_route_d_v7_seminorm.py → writeup/data/p2_route_d_v7_seminorm.json → fig25
(writeup/4_p2_lottery/p2_route_d_v7_evidence.py). NOT a logged Tier run. BLOG/TECHNICAL_P2_ROUTED_V7.md.

**v6 recommended route (a) (restrict to a band-limited subspace with a measured faithfulness factor)
and kept route (b) (the analytic C^{1,γ} derivative gain) in reserve. This leg did (b), because a
ten-minute diagnostic showed (a) was aimed at the wrong mechanism** — v6 had reasoned by analogy to
its OWN headline finding (the discrete-ball trap) and the analogy was false.

SIX evidence pieces (do not relearn):
  V1 **WHERE THE J^γ ACTUALLY LIVES.** v6's dual bound on the seminorm part, restricted to pairs with
     |Δθ| ≥ Δ for FIXED Δ (so it covers more grid points as J grows): all 17.2→24.2→34.2 (J^+0.494);
     Δ=0.05 9.09→9.78 (J^+0.053); **Δ=0.1 6.95→7.12 (J^+0.018)**. **All of the growth sits on the
     NEAR DIAGONAL.** That disqualifies route (a) STRUCTURALLY, not numerically: a faithfulness defect
     of the ball is a statement about which directions are admissible and does not know whether the two
     domain indices being compared are adjacent; the J^γ does. What it actually is: ‖A_j· − A_k·‖_{Y*}
     was priced ROW BY ROW, discarding the near-cancellation of neighbouring rows of an inverse and
     then dividing by |Δθ|^γ ~ (π/J)^γ. **No refinement of the dual recovers a cancellation the dual
     cannot see, because the cancellation is a property of the EQUATION, not of the rows.**
  V2 **THE SPLIT HILBERT BOUND (free sharpening).** v6's |H(h)| bound charges the TOTAL norm; its own
     derivation already separates the payers (p.v. band increment ← seminorm, rest of the line ←
     decay envelope). Keeping them apart: |H(h)(X)| ≤ a_sup(X)·S + a_semi(X)·T, sum = v6's bound to
     2.1e-16. Weighted sups at (α,γ)=(1.5,0.5): 1.031 and 1.277 vs v6's combined 1.928 — **~30% on the
     final closure (T ≤ 93.5 unsplit vs 63.6 split), up to 4.3× sharper pointwise.**
  V3 **THE CLOSURE = the estimate itself.** (P) Solve the equation for the derivative:
     c h_X = −g − hX/(1+X²) − H(h)/(1+X²) (exact rearrangement, gate 1.9e-16) ⇒
     P := sup (1+X²)^{(α+1)/2}|h_X| ≤ (1/c)[‖g‖_Y + S + sup (1+X²)^{(α−1)/2}(a_sup S + a_semi T)] (D).
     (I) Split each pair at δ(θ₁)=κ(1+X₁²)^{−1/2} (a fixed multiple of the LOCAL X-scale): separated
     pairs pay 2Sκ^{−γ}, near pairs pay (1/2)Pκ^{1−γ}, and **the weights cancel identically at every
     scale** (the compactification again doing the far-field bookkeeping for free) ⇒
     **T ≤ C(γ)(P/2)^γ(2S)^{1−γ}, C(γ)=(1−γ)^{γ−1}γ^{−γ}, C(1/2)=2. NO J, NO GRID.** Hypothesis α≥1
     (used once; `seminorm_closure` REFUSES α<1 rather than silently extending). Gate: (I) verified on
     32 profiles × 4 (α,γ) incl. α=1, worst ratio T/bound = 0.461.
     **WHY IT NEVER FAILS:** (D)+(I) read T ≤ F(T) with F concave, increasing, F(0)>0, so F(T)−T
     changes sign exactly once ⇒ a UNIQUE fixed point T*, and {T : T ≤ F(T)} = [0,T*]. The feedback is
     LINEAR in T (through |H(h)|) while the gain is SUBLINEAR (F ~ T^γ) — **so for every γ<1 the
     closure holds regardless of the size of the constants: no smallness condition, no contraction to
     lose.** Only γ=1 turns it into a genuine contraction condition — a **THIRD independent reason**
     γ=1 is excluded (alongside v5 U2's blow-up at both ends and the classical unboundedness of H on
     Lipschitz functions). Gate 5: T=F(T) to 1e-9, slope 0.445<1, closes for C_sup up to 5e3,
     F(2T)/F(T)=1.414=2^γ.
     **THE NUMBER (α,γ)=(1.5,0.5):** T ≤ 63.61/63.56/63.53/63.82/64.70 over J=125..1600, ‖A‖ ≤ 69.15
     →70.33 (**J^+0.0059**, drift inherited ENTIRELY from v6's C_sup; the closure contains no J).
     **First uniform upper bound on the WHOLE of ‖A‖ in seven legs.** Bracket, said honestly:
     **0.85 ≤ (seminorm part) ≤ 63.6 — a factor ~75 wide.** v6's dual on the same quantity grew J^+0.49.
  V4 **THE (α,γ) MAP MADE OF UPPER BOUNDS.** J=800, α∈[1.1,1.8], γ∈[0.05,0.8] (past where the answer
     was expected — lesson 8). **‖A‖ alone falls monotonically as γ→0** (a weaker domain norm is easier
     to bound) so optimizing it alone runs off the grid edge (argmin at γ=0.05). **Z₂=2‖A‖C_Q BOWLS in
     BOTH knobs: interior optimum (α,γ)=(1.4,0.15), Z₂ ≤ 242.4** — the quadratic pays for exactly the
     weakness that makes ‖A‖ cheap. **First interior optimum in this project computed entirely from
     upper bounds** (v5's was family-restricted maxima and v6 killed it). CAVEAT that must travel with
     it: Z₂ here still OMITS the codomain seminorm part of C_Q, which is unbounded, and that omission
     is worst exactly where γ is smallest — so the LOCATION is provisional, again.
  V5 **WHAT THE HONEST ‖A‖ COSTS.** v6's conditional budget substituted the far-field inverse norm
     2/(2−α)≈2.5 for ‖A‖ (justified by v4 W2 — but that was validated in SUP norms). In the Hölder
     norm the real bound is **10–20× larger**. At γ=0.35, requiring Z₁ ≤ 0.5: α=1.2 needs X₀~2e3
     (J~1e3), α=1.4 X₀~6e3 (J~4e3), α=1.5 X₀~3e4 (J~2e4, dense J×J = 3.2e9 entries — out of reach).
     **SURVIVABLE** for α ≤ 1.4: inside what the existing dense collocation reaches. **EXPENSIVE:**
     the conditional budget drops from 2.8e-3 to **2.0e-4** — from the same order as the GA residual
     floor (~1e-2) to a factor ~50 below it. **SECOND CONSECUTIVE LEG in which replacing a lower bound
     by an upper bound cost the budget an order of magnitude** (v6 B5 did it to v5's optimum). That
     pattern is the leg's most important negative: **the approach does not merely need the constants
     bounded, it needs them roughly SHARP** — three of four bounded ones are lossy by ≥1 order, and
     the losses MULTIPLY inside Z₁ and Z₂.
  V6 **THE INTERPOLANT IS NOT IN THE SPACE (a defect older than this leg).** A nodal vector on the
     midpoint grid stands for an even TRIGONOMETRIC POLYNOMIAL in θ, which does not vanish at θ=π,
     where w_α=sec^α(θ/2) diverges ⇒ **sup w_α|h| is INFINITE for the interpolant at every J.** Every
     discrete norm in v1…v7 is finite only because the midpoint grid stops half a step short of π.
     Measured on h=Ae_{J/2}: w|h| at the last node 8.4e-3→6.0e-4 over J=200..1600, but at θ=π−1e-6 it
     is 1.09e3→2.08e0; h(π) ~ **J^{−3.01}** — the failure is SOFT (the discretization converges to
     something that does live in the space) but it is a change of REPRESENTATION, not a small
     correction. **Repair (explicit): write h = (1+X²)^{−α/2} p(θ) with p a trigonometric polynomial**,
     so the weighted sup norm becomes the plain sup norm of p and the weighted seminorm a mildly
     weighted θ-seminorm of p. NOTE the §V3 closure is IMMUNE — it is a continuum statement about the
     true solution of DF h = g, which does decay; the defect is in the HYPOTHESIS S ≤ C_sup, which is
     currently supported by grid measurements.
  V7 **THE LEDGER.** EXACT: Y₀. BOUNDED: Z₀; Z₁ far-field modelling error (v6); ‖A‖ domain SUP part
     (v6); **‖A‖ domain SEMINORM part (NEW)**; C_Q sup part (v6). OPEN: Z₁ core↔far coupling; Z₁ core
     discretization (measured only); C_Q codomain SEMINORM part; **discrete↔continuum transfer (NEW,
     V6 above)**. **Six of ten bounded** — and two of the four open items are new NAMES for things that
     were previously invisible rather than new problems.

NEXT (in order of sharpness): (1) **the C_Q codomain seminorm part** — weighted Hölder boundedness of
H with an explicit constant; v5 U2 MEASURED it (~1.12) and never bounded it, and it is the one term
that would make the V4 map's optimum LOCATION trustworthy; (2) **the change of ansatz**
h=(1+X²)^{−α/2}p(θ) that fixes V6's interpolant defect and would let every discrete measurement in
v5–v7 be re-read as a statement about a space the objects actually live in; (3) the core↔far cutoff
commutator; (4) the core discretization. Same stopping rule: **if the radii polynomial does not close
in float with margin, STOP, do not harden.** solver/interval.py still correctly unused.
HONEST CEILING unchanged: plain float64, nothing interval-enclosed, nothing rigorous. Clay odds ~0.05%.

## §17 — ROUTE-D v8 DONE (2026-07-31): the CODOMAIN SEMINORM PART OF C_Q — the last unpriced
## constant in Z₂, and the FIRST COMPLETE Z₂. The three-legs-in-a-row order-of-magnitude
## budget loss DOES NOT CONTINUE. Still NOT a certificate.

The §16 "next brick", item (1). Built solver/hilbert_holder.py + test_nk_hilbert_holder.py 6/6
(suite now **15 files green**); deterministic sweep experiments/p2_route_d_v8_quadratic.py →
writeup/data/p2_route_d_v8_quadratic.json → fig26
(writeup/4_p2_lottery/p2_route_d_v8_evidence.py). NOT a logged Tier run. BLOG/TECHNICAL_P2_ROUTED_V8.md.

SIX evidence pieces (do not relearn):
  X0 **WHAT HAD TO BE BOUNDED, AND THE WEIGHT.** Expanding the product increment about the INNER
     point: w_{α+1−γ}|ΔQ|/d^γ ≤ S·{w_{1−γ}|Δψ|/d^γ} + T·w_1(θ_i)B(θ_o), ψ=H(h). The SECOND term
     needs no new work (w increases in |θ| ⇒ w_1(θ_i)B(θ_o) ≤ sup w_1 B = v6's C_Q sup part). The
     FIRST needs the weighted Hölder seminorm of ψ **with weight 1−γ, NOT α−γ**: **H does not
     inherit h's decay** (H(h) → (∫h)/(πX) however fast h decays), so ψ's decay grading is 1.
     Asking for α−γ would have produced an infinite constant with nothing to point at. **Third time
     in the series a weight exponent was the whole difficulty and the right one was FORCED.**
  X1 **THE ESTIMATE + BOTH CONVERGENCES + THE ABLATION.** Change variables to t = φ−θ₁ (in t
     NOTHING WRAPS — in absolute θ the pair (θ≈π, φ≈−π) are NEIGHBOURS on the circle, so a near
     region defined as an interval of the line would leave a kernel singularity in the "far"
     region). ψ(θ₁)−ψ(θ₂) = (1/2π)[E_N+E_F+G] with N=[min(0,σ)−pd, max(0,σ)+pd]; majorants: h's
     increments by whichever norm part is cheaper POINTWISE (a rule independent of S,T, which is
     what keeps the bound LINEAR in (S,T)), the kernels EXACTLY (far difference in the stable form
     sin(σ/2)/(sin(t/2)sin((σ−t)/2)), which preserves the O(d) cancellation), G in closed form
     (→2log(3/2)). **At (1.5,0.5): T_ψ ≤ 1.1936 S + 4.9410 T**, flat to 4e-6 over a 4× pair-grid
     refinement and 4e-4 over 150→2400 quadrature points. **ABLATION: with only the pointwise route
     — all v6/v7 had for this quantity — the same sweep returns 1452 instead of 6.13 (237×).** And
     the per-pair RULE matters: "smaller coefficient SUM" inflates b_sup 1.19→2.61; the route choice
     must be ONE rule applied to both coefficients.
     **THE PADDING BUG WORTH REMEMBERING:** the first draft restricted the estimate to d ≤ (π−θ_i)/6
     — which is what the SCALING ARGUMENT needs — and the sweep returned a constant **12× too large**,
     entirely from pairs just outside that cutoff where the crude fallback took over. The
     DECOMPOSITION only needs (1+p)d ≤ π. **Do not let the regime of an ARGUMENT become the regime of
     the CODE.**
  X2 **THE SECOND BUILD (the gate that earned its keep).** A majorant of a WRONG decomposition is
     still a valid inequality about something, and no domination test notices. E_N+E_F+G rebuilt with
     the TRUE increments and compared against the exact conjugate (cos kθ→sin kθ): **5.6e-6**
     (quadrature-limited) over 7 pairs × 3 profiles. It caught two sign errors, one of which was ALSO
     wrong in the module docstring, where it had been sitting looking correct.
  X3 **THE BRACKET.** Measured (family-restricted ⇒ LOWER) vs the bound over 10 profiles at four
     (α,γ): worst ratio 0.222–0.246. Valid everywhere, **~4× lossy** — the same order of slack v7's
     closure carried, and per v7's own conclusion that slack is now the quantity of interest.
  X4 **THE γ STRUCTURE — AND v7's PREDICTION IS BACKWARDS.** Both endpoint divergences present:
     b_semi 18.6 (γ=0.05, near region ∫|t|^{γ−1}~1/γ) → 4.94 (0.5) → 7.16 (0.9, far region
     ∫d|t|^{γ−2}~1/(1−γ)); C_Q complete BOWLS, interior min 3.330 at γ=0.65. BUT the RATIO
     complete/sup-only is **1.001 at γ=0.05, 1.09 at 0.35, 1.28 at 0.9** — worst at the OPPOSITE end
     from v7's prediction. Reason: **v6's sup-only C_Q already carried the same 1/γ near-region
     divergence** (through the seminorm-paid half of its own |H(h)| bound), so nothing NEW blows up
     at small γ.
  X5 **THE FIRST COMPLETE Z₂ MAP.** Z₂=2‖A‖C_Q at J=800 with ‖A‖ = v6 dual + v7 closure and C_Q =
     v6 sup part (split by payer) + v8 seminorm part: **every constant an upper bound, NOTHING
     omitted — the first Z₂ in the project of which that is true.** **Optimum (α,γ)=(1.4,0.15),
     Z₂ ≤ 261.1 — the SAME LOCATION v7's incomplete map reported (242.4), 7.7% higher.** v7 called
     that location provisional BECAUSE of this omission; the omission is priced and the location
     holds.
  X6 **THE BUDGET, AND THE TREND THAT DOES NOT CONTINUE.** At the optimum, Z₁ ≤ 0.5 needs X₀=3.2e3
     (J~2.5e3, 6.2e6 dense entries — inside reach). **History: 7.6e-2 (v5) → 1.18e-2 (v6) →
     2.58e-4 (v7) → 2.39e-4 (v8).** (v7's own writeup quoted 2.0e-4, its γ=0.35 row; 2.58e-4 is v7's
     map priced over the same sweep, the like-for-like number.) **Three order-of-magnitude losses,
     then one of 7%.** v7's most important negative — every honesty step costs an order — **does not
     continue through this leg**, for the two reasons in X4/X1 (the old term already carried the new
     one's worst divergence; v7's split-by-payer sharpening recovers most of the cost). Honest
     reading: this does NOT make the budget large (2.4e-4 is still ~40× below the GA residual floor)
     and it is NOT evidence the remaining three items are cheap; it is evidence that "each step costs
     an order" was a pattern in three data points with a common cause, not a law about the method.
  X7 **THE LEDGER.** EXACT: Y₀. BOUNDED: Z₀; Z₁ far-field (v6); ‖A‖ sup part (v6); ‖A‖ seminorm part
     (v7); C_Q sup part (v6, sharpened v7/v8); **C_Q codomain seminorm part (NEW)**. OPEN: Z₁ core↔far
     coupling; Z₁ core discretization (measured only); discrete↔continuum transfer (v7).
     **Seven of ten bounded — and Z₂ is COMPLETE.** All three remaining are Z₁-side or
     representational.

NEXT (in order): (1) **the core↔far-field cutoff commutator [H,φ]** — the last structural piece of
Z₁ (φ′~1/X₀ ⇒ O(1/X₀); the scale is right, the estimate is the work); (2) **the change of ansatz**
h=(1+X²)^{−α/2}p(θ) (v7 V6) — cheap, and it retro-fits every discrete measurement in v5–v8 into a
space the objects actually live in; (3) the core discretization (v4 W6). **THE SHARPNESS QUESTION IS
NOW AS IMPORTANT AS THE BOUNDEDNESS QUESTION:** ‖A‖'s bracket is ~75× wide and C_Q's is ~4×, and the
budget scales inversely with their product. A leg that SHARPENS ‖A‖ (e.g. by not routing the whole
seminorm through the interpolation inequality) may now be worth more than a leg that bounds one more
open item. Same stopping rule: **if the radii polynomial does not close in float with margin, STOP,
do not harden.** solver/interval.py still correctly unused.
HONEST CEILING unchanged: plain float64, nothing interval-enclosed, nothing rigorous. Clay odds ~0.05%.

## §18 — ROUTE-D v9 DONE (2026-07-31): THE SHARPNESS LEG. A 32% sharper |H(h)| bound that buys
## ~NOTHING at the operating point — plus the ELASTICITY TABLE that explains why and redirects
## the next leg. A negative with a mechanism. Still NOT a certificate.

The §17 "next brick", item (1) (sharpen ‖A‖). Built solver/hilbert_pointwise.py +
test_nk_hilbert_pointwise.py 6/6 (suite now **16 files green**); deterministic sweep
experiments/p2_route_d_v9_sharpen.py → writeup/data/p2_route_d_v9_sharpen.json → fig27
(writeup/4_p2_lottery/p2_route_d_v9_evidence.py). NOT a logged Tier run. BLOG/TECHNICAL_P2_ROUTED_V9.md.

**WHY THIS LEG:** v8 left Z₂ complete and seven of ten bounded, so the question changed from
COVERAGE to SHARPNESS — budget ~ 1/(‖A‖C_Q), ‖A‖'s bracket ~70× wide. Target picked itself: v7's
closure is dominated by its own feedback (the |H(h)| term supplies **81 of the 93 units** in the
derivative bound at the reference point) and that feedback is v6's crude-majorant bound.

SIX evidence pieces (do not relearn):
  Y1 **THE BOUND.** Fold onto (0,π): ψ(θ) = (1/2π)p.v.∫_0^π h(φ)K_θ(φ)dφ,
     **K_θ(φ) = 2sinθ/(cosφ−cosθ) = −sinθ/(sin((φ+θ)/2)sin((φ−θ)/2))**. Three properties, each
     removing something v6 needed: (i) **the decay is IN the kernel** (sinθ→0 at π — v6's
     even-kernel point in θ coordinates); (ii) **p.v.∫_0^π K dφ = 0 EXACTLY** (it is the conjugate
     of the constant function; the antiderivative −2log|sin((φ−θ)/2)/sin((φ+θ)/2)| vanishes at BOTH
     ends) ⇒ the p.v. is handled by ONE GLOBAL SUBTRACTION — **no band, no matching scale, no
     remainder term**, all three of which v6 needed and each of which cost a constant; (iii) the
     second form is the one to EVALUATE — near θ=π both cosines → −1 and the difference has no
     significant digits (the first draft NaN'd at X≳1e4); parameterising by the offset s=|φ−θ|
     makes sin((φ−θ)/2)=sin(±s/2) exact. **Ratio to v6 across 8 decades: 0.09 / 0.26 / 0.66 / 0.87
     / 0.65 / 0.67 / 0.85 / 0.95 / 0.99.** Gated by an exact second build (1.5e-7) and nearly
     ATTAINED (0.97 on the anchor).
  Y2 **THE PAYER RULE (the transferable part).** Any FIXED rule for choosing which norm part pays
     at each φ gives a valid linear bound; v8's default compared them at S=T=1. **Wrong default:
     tune the rule to the T/S ratio of the ANSWER, not to 1.** With ρ (seminorm pays iff ρc_T≤c_S):
     ‖A‖ = 74.7(ρ=1) / 63.4 / 53.1 / 48.4 / **47.2(ρ=6–9)** / 50.6 / 54.0, an INTERIOR optimum —
     and **the neutral ρ=1 gives 74.7, WORSE than the 69.4 of the crude bound it replaces** (in the
     closure T ~ 10S, so minimising the S=T=1 sum charges the expensive account). C_Q, maximising
     over the unit simplex where the ratio is O(1), wants ρ≈2 instead. Both valid; each caller picks.
  Y3 **THE NEW ‖A‖:** 69.15 → **47.05** at (1.5,0.5), still J-flat (J^+0.0059, inherited from
     C_sup). Largest single improvement to ‖A‖ since the closure was built.
  Y4 **THE GAIN DOES NOT TRANSFER (the leg's actual result).** Reduction in ‖A‖ by point:
     **32% (1.5,0.50) / 11% (1.4,0.35) / 3% (1.4,0.25) / −0% (1.4,0.15) / −1% (1.2,0.15)** — and
     **(1.4,0.15) is the map's optimum**, where the budget is evaluated and has been for three legs.
     MECHANISM: the closure is T ≤ C(γ)(P/2)^γ(2S)^{1−γ} and the |H| bound enters **ONLY through P**,
     so at γ=0.15 a 30% improvement in P moves T by 4%. Worse: the operating point sits at small γ
     precisely BECAUSE that is where ‖A‖ is cheap — i.e. where it barely depends on the input this
     leg improved. **The optimiser had already walked to the corner where the improvement cannot
     matter.**
  Y5 **THE ELASTICITY TABLE (what should have come first, and costs a minute).** Scale each input
     and fit the log-log slope: **d log‖A‖/d log C_sup = +0.98 (reference), +1.00 (operating);
     d log‖A‖/d log|H| = +0.46 (reference), +0.11 (operating).** ‖A‖ is PROPORTIONAL to C_sup —
     v6's two-point dual on the sup part — and at the operating point essentially blind to the |H|
     bound. **The last TWO legs (v8's codomain seminorm, v9's pointwise bound) both worked on inputs
     with elasticity ≤ 0.5 and both moved the budget by ≤ 7%. That is the table read backwards, and
     neither leg computed it beforehand.**
  Y6 **THE TRAP ON THE WAY OUT (banked lesson 15, missed again).** The tempting next step is to
     substitute a MEASURED C_sup and read off the available gain. An earlier draft of this leg did
     exactly that and reported a **19× available gain — an artifact**: the "measured C_sup" was a
     family lower bound computed by dividing the SUP PART of an image by the FULL codomain norm of a
     sign pattern (whose Hölder seminorm is enormous), an order of magnitude below any plausible
     sharp value. What survives: elasticity says C_sup is the input worth attacking; v6 B2's own
     bracket says C_sup is ~2× lossy, so **~2× is on the table there, not an order of magnitude**;
     and the wider bracket (47× vs a family LB of ~1.0) **cannot be attributed at all** until there
     is a decent LOWER bound — a maximum over a few sign patterns says almost nothing about how
     lossy an upper bound is.
  Y7 **MAP + BUDGET + LEDGER.** Complete Z₂ map (ρ chosen per cell from {1,3,6,12}): optimum
     **(1.4, 0.15), Z₂ ≤ 260.7** — third leg running at the same place (v8: 261.1). Budget history
     **7.6e-2 → 1.18e-2 → 2.58e-4 → 2.39e-4 → 2.40e-4**: three order-of-magnitude losses, then three
     legs of nothing in either direction. Ledger coverage UNCHANGED (seven of ten; Z₂ complete);
     the status note on C_sup is rewritten to record that it is now the DOMINANT input.

NEXT — decided by Y5, not by intuition: (1) **C_sup, the two-point dual on the sup part.** It is the
only input left with elasticity ≈ 1, it has not been touched since v6 first bounded it, and ~2× is
plausibly available. (2) **A REAL LOWER BOUND on ‖A‖** (an LP over the polyhedral ball, or a proper
adversary construction rather than sign patterns) — without it, no bracket in this project can be
attributed, and we cannot tell a lossy bound from a large truth. Arguably (2) BEFORE (1), since (2)
is what tells us whether (1) is worth doing. (3) the core↔far cutoff commutator; (4) the change of
ansatz h=(1+X²)^{−α/2}p(θ); (5) the core discretization. Same stopping rule: **if the radii
polynomial does not close in float with margin, STOP, do not harden.**
HONEST CEILING unchanged: plain float64, nothing interval-enclosed, nothing rigorous. Clay odds ~0.05%.

## §19 — ROUTE-D v10 DONE (2026-07-31): A LOWER BOUND ON ‖A‖ WORTH READING. The bracket falls
## 50× → 8×, and for the first time the project can quote a MEASURED CEILING on what sharpening
## can buy. Still NOT a certificate.

The §18 "next brick", item (1) — done BEFORE touching C_sup, because it is what tells us whether
touching C_sup is worth it. Built solver/op_lower.py + test_op_lower.py 6/6 (suite now
**17 files green**); deterministic sweep experiments/p2_route_d_v10_lower.py →
writeup/data/p2_route_d_v10_lower.json → fig28. NOT a logged Tier run. BLOG/TECHNICAL_P2_ROUTED_V10.md.

SIX evidence pieces (do not relearn):
  W0 **WHY SIGN PATTERNS FAIL, AND THE TELL NOBODY CHECKED.** g = sign(A_i·)/v is the exact
     extremizer of the SUP-TO-SUP problem; here it is terrible for exactly v6's discrete-ball
     reason in reverse — **a sign pattern's Hölder seminorm is enormous**, so dividing by the full
     codomain norm discards everything the numerator gained. **THE TELL: the baseline gets WORSE
     with J (0.973 → 0.921 over J=200..800). It was never converging to anything about the
     operator.** Nobody had looked, through six legs of quoting it.
  W1 **THE CONSTRUCTION.** The Y-ball says what to look for: finite codomain norm ⇒ decay at least
     like 1/v = cos^{α+1}(θ/2) AND no oscillation. So the family is **1/v × a slowly varying
     shape** (powers, low-order cosines, bumps swept over centre and width, smoothed steps, boxes).
     Validity is FREE (any g gives ‖A‖ ≥ ‖Ag‖_X/‖g‖_Y), so the whole problem is construction.
     Reference (1.5,0.5), J=400: **0.942 → 2.884**; bracket **50× → 16×**. A random ascent in a
     smooth cosine basis from the family's best adds **1.000×** — reported, because a flat maximum
     is information.
  W2 **THE BRACKET THAT ACTUALLY MATTERS.** At the OPERATING point (1.4, 0.15) — where the budget
     has been evaluated for three legs — **2.74 ≤ ‖A‖ ≤ 20.94, a factor of 7.7.** Quoting the
     bracket at the REFERENCE point was itself part of the confusion: a second, quieter version of
     the same mistake.
  W3 **WHAT THE EXTREMIZER IS.** A **wide, far-field-supported, slowly varying** shape — a bump at
     θ=3.12 (X≈93) of width 0.5, with its neighbours next. Nothing oscillatory is close. Same place
     every other Route-D finding points at (v2's far-field degeneracy, v3's α=2 resonance, v6's X₀):
     a small independent check that the number means something.
  W4 **ACROSS THE MAP:** 10.7× (1.2,0.15) / **8.2× (1.4,0.15)** / 14.2× (1.4,0.35) / 16.2×
     (1.5,0.50) / 10.8× (1.6,0.25) / 10.4× (1.8,0.15) — 8–16× everywhere and **tightest at the
     optimum**; the upper bound is worst exactly where the closure leans hardest on the
     interpolation inequality (large γ).
  W5 **THE VERDICT — the first MEASURED CEILING on sharpening in ten legs.** A PERFECT upper bound
     on ‖A‖ multiplies the conditional budget by the bracket and no more: **2.45e-4 → 1.88e-3**
     (×7.7) against the GA residual floor 1e-2. BOTH readings matter: (i) **better than it looked**
     — the recoverable part lands ~5× short of the floor, not 40×; (ii) **not enough alone** —
     closing the gap also needs C_Q's ~4× slack (v8 X2), and the two together only just reach the
     floor with nothing spare for the three open Z₁ items. Caveats: the true norm is somewhere
     INSIDE the bracket, not at its bottom, so 7.7× over-estimates the achievable gain; the lower
     bound is still a finite family; the budget is still CONDITIONAL.
  W6 **LEDGER:** coverage unchanged (seven of ten; Z₂ complete). What changed is that the bracket
     on the DOMINANT constant is now interpretable, so the next leg can be chosen on evidence.

NEXT: (1) **C_sup, the two-point dual** — elasticity ≈1 (v9 Y5), untouched since v6, and now with a
measured ceiling on the payoff; (2) the core↔far cutoff commutator [H,φ]; (3) the change of ansatz
h=(1+X²)^{−α/2}p(θ); (4) the core discretization. **AND A STANDING RULE EARNED HERE: a bracket is
two numbers and BOTH have to be earned before any decision is made from it.**
HONEST CEILING unchanged: plain float64, nothing interval-enclosed, nothing rigorous. Clay odds ~0.05%.

## §20 — ROUTE-D v11 DONE (2026-07-31): NEWTON ON THE PROFILE — the 1e-2 residual floor was the
## SEARCH, not the equation (12 orders); the survival boundary a*≈0.5 SURVIVES a fourth,
## genome-free confirmation; and Y₀'s binding constraint moves from SEARCH to DISCRETIZATION.

The §19 "next brick", item (1) — the other side of the inequality. Built solver/profile_newton.py
+ test_profile_newton.py 6/6 (suite now **18 files green**); experiments/p2_route_d_v11_anchor.py →
writeup/data/p2_route_d_v11_anchor.json → fig29. NOT a logged Tier run (deterministic Newton, no
GA, no seeds). BLOG/TECHNICAL_P2_ROUTED_V11.md.

**WHY:** v10 measured that the constants alone cannot close the gap (7.7× × 4× only just reaches
the 1e-2 floor, nothing spare). Y₀ enters the radii polynomial LINEARLY and had never been
attacked — every a≠0 profile came from a GA over a small genome or fixed-grid relaxation, both of
which floor at ~1e-2.

SIX evidence pieces (do not relearn):
  V0 **TWO GAUGES, NOT ONE.** The a=0 zero set is the two-parameter family A/(1+BX²) (§9), which
     v1 Q2 already found: one gauge leaves the Jacobian SINGULAR and a direct solve crawls to
     **1.8e-6 in 40 iterations**; two gauges in least squares reach **2e-15 in 5**. Analytic
     Jacobian gated against finite differences to 6.6e-11.
  V1 **THE KNOWN-ANSWER GATE, read correctly.** At a=0 Newton finds a zero of the DISCRETE system
     (1.1e-15) while the **exact continuum anchor scores 7.7e-9 on the same equations** — its own
     discretization error. **A solver that reproduced the continuum profile exactly would be
     reporting something impossible.**
  V2 **THE FLOOR WAS THE SEARCH: 12 ORDERS.** relres 9.7e-15 (a=0) … 2.0e-14 (a=0.5) vs the GA /
     relaxation ~1e-2 at every a. The banked discipline lesson ("fixed-grid dynamic relaxation
     FLOORS the residual ~1e-2") is about the METHOD, and §9 read it as being about the problem.
  V3/V4 **THE CHECK THAT DECIDES, AND THE BOUNDARY THAT SURVIVES.** Newton also converged at large
     a — for an hour that looked like "the boundary is a genome artifact". **It is not.** Machine
     precision on a DISCRETE system proves nothing alone; the test is whether the SOLUTION stops
     moving with n. Spread in c over n=401/801/1601: **8e-4 (a=0) / 3e-4 (0.2) / 3e-5 (0.5) /
     3.7e-3 (0.8) / 1.3e-2 (1.0)**, and grids reaching machine precision 3/3/2/**1**/**1**. So
     solutions are continuum objects up to **a ≈ 0.5** and not beyond: **the GA's a*≈0.5–0.55
     confirmed a FOURTH time, now by a method with no genome, no search budget and no
     stochasticity** — and sharpened: below a*, an exact discrete traveling wave EXISTS.
  V5 **WHAT IT DOES TO Y₀ — a change of BINDING CONSTRAINT, not a solved problem.** The
     certificate does not see the RMS; it sees the **weighted sup defect** sup(1+X²)^{(α+1)/2}|R₂|,
     which is **6+ orders larger** (the codomain weight amplifies exactly the far field where the
     truncation lives) and **not uniformly under the budget**: 2.3e-14 (a=0.1) / 1.1e-8 (0.2) /
     2.2e-7 (0.3) / **1.5e-2 (0.45, ABOVE the 2.45e-4 budget)** / 7.5e-7 (0.5). **Y₀ is no longer
     SEARCH-limited; it is DISCRETIZATION-limited** — which is already a ledger item (Z₁ core
     discretization, v4 W6 measured J^−2.1..−2.6 and never bounded it). "Find a better profile"
     was the wrong problem; "control the far-field discretization of a profile we can now compute
     exactly" is the right one, and it is a statement about a KNOWN OBJECT rather than a search.

NEXT: (1) **carry the Newton profile into the θ-collocation basis the bounds live in and measure
Y₀ there** (the number above is in the Route-A ρ-discretization; the two are different);
(2) **price the core discretization error** — now the binding item for Y₀; (3) C_sup (elasticity
≈1, ~2× available); (4) the core↔far commutator. **LESSON: a number that appears in every
measurement is the hardest instrument artifact to see — we carried 1e-2 for five legs as physics
when both tools producing it shared the same weakness. And the thing that stopped the correction
becoming an over-claim was one table: refine the grid, see whether the answer moves.**
HONEST CEILING unchanged: plain float64, nothing interval-enclosed, nothing rigorous. Clay odds ~0.05%.


## §21 — ROUTE-D v12 DONE (2026-07-31): Y₀ MEASURED IN THE BOUNDS' OWN BASIS — and the
## a>0 profile turns out to END at a finite radius, which invalidates the space eleven
## legs were built on and makes ‖A‖ DIVERGE at the object the certificate is about.

The §20 "next brick", item (1). Built solver/collocation_newton.py + test_collocation_newton.py
6/6 (suite now **19 files green**); experiments/p2_route_d_v12_defect.py →
writeup/data/p2_route_d_v12_defect.json → fig30. NOT a logged Tier run (deterministic Newton +
deterministic sweeps). BLOG/TECHNICAL_P2_ROUTED_V12.md.

**THE BUILD.** The a-transport term in the compactified θ-basis. The one non-local object,
U = ∫₀^X H(Ω)dX', has a closed form there: U = Σ_k A_k I_k(θ) with I_k = ∫₀^θ sin kt/(1+cos t)dt,
I_0=0, I_1=log(1+X²), **I_{k+1} = 2(1−cos kθ)/k − 2I_k − I_{k−1}** (from 2 sin kt cos t =
sin(k+1)t + sin(k−1)t with cos t = (1+cos t) − 1). Homogeneous solutions (A+Bk)(−1)^k, and I_k
itself grows at the same rate near θ=π, so relative error is fine and absolute error tracks εk²
(**1.7e-11 at k=800 in float64** ⇒ assembled in longdouble). Because I_k is a formula, the
residual of the INTERPOLANT is evaluable at ANY θ — which is the whole point.

SEVEN evidence pieces (do not relearn):
  T0/T1 **A IS THE NEWTON MATRIX.** `gauged_jacobian` = [gauge row; DF rows except one] with c
     FIXED, and A = M⁻¹; the Newton iteration for that same square system is x ← x − A F(x), so
     **Y₀ = ‖A F‖ is the size of the Newton step.** Newton drives the rows it enforces to
     1.5e-13…2.4e-13 at every a. The row the gauge DISPLACED goes 7.1e-13 (a=0, the control —
     the anchor is an exact solution) → 4.8e-7 (0.1) → 9.3e-5 (0.3) → 9.1e-3 (0.5). **Zero at
     the nodes is not zero as a function**, and the gap is 6–10 orders. Structural, not sloppy:
     ΩH(Ω) has degree <2J and collocation imposes J conditions on it.
  T2 **Y₀ IN THE CODOMAIN NORM at (1.4,0.15), J=400.** ‖F‖_Y = 3.7e-11 (a=0 control) / 4.4e-4
     (0.05) / 8.4e-6 (0.1) / 4.4e-5 (0.2) / 1.5e-2 (0.3) / 7.9e-1 (0.4) / 1.7e0 (0.5) ⇒
     Y₀ ≤ 20.94‖F‖ = 0.7× budget only at a=0.1; 1256× at 0.3; 1.4e5× at 0.5. **NOT MONOTONE in
     a, and the arg-max is the OUTERMOST evaluation point at every single a.** Both are the tell.
  T3 **THE MECHANISM — THE PROFILE ENDS.** E(X) = c + aU(X) is the true transport coefficient.
     H(Ω)→m/(πX) with m=∫Ω<0 ⇒ **U = U₀ + (m/π)log X → −∞**, so **E crosses zero at a finite
     X_c ≈ e^{c/a}** (using the anchor's m=−π, U₀=0). Near it E ≈ −a h_c s (s = X_c−X,
     h_c = H(Ω)(X_c)) and Ω = A s^p gives A s^p h_c = a h_c p A s^p ⇒ **p = 1/a, no free
     constant** (A and h_c cancel). Beyond X_c, Ω ≡ 0 solves the equation exactly. **The a=0
     anchor is the degenerate X_c = ∞ limit**, and the SAME balance at a=0 gives Ω ~ X^{m/(πc)}
     = X^{−2} — i.e. the anchor's tail and v3's α=2 resonance are the a→0 corner of this
     picture. MEASURED in two independent discretizations, compared through the dilation
     invariant X_c/c: gap **0.06% / 0.11% / 0.00% / 0.01%** at a=0.2…0.5 (3.0% at a=0.1, where
     the θ-grid stops resolving X_c≈290 — the instrument, not the object). Fitted zero order
     5.40 / 3.59 / 2.73 / 2.20 vs 1/a = 5 / 3.33 / 2.50 / 2.00 — **7–9% high uniformly**, which
     is what a leading-order fit over a finite window does.
  T4 **THE RATE, AND THE ONE NUMBER THAT GOES THE RIGHT WAY.** ‖F‖_Y vs J: J^−2.31 (a=0.2),
     J^−1.02 (0.3), **J^−0.04 (0.4 — flat over a 16× refinement)**, against the naive
     C^{1/a}-aliasing prediction J^−(1/a+1) = −6/−4.33/−3.5. Slower than the profile's own
     regularity because **the error measured is not the aliasing of the zero, it is the Gibbs
     ringing left by representing a COMPACTLY SUPPORTED function in a GLOBAL spectral basis,
     amplified by a codomain weight that grows like X^{α+1}**. At a=0.2, J=1600:
     **Y₀ ≤ 3.17e-5 vs budget 2.45e-4 — 7.7× UNDER, the first time this side of the inequality
     has come in under target at a≠0.** See T5 for why that is not the result it looks like.
  T5 **THE OPERATOR DOES NOT TRANSFER — AND DOES NOT EXIST.** Every constant in the budget was
     computed at the a=0 anchor; the certificate linearizes at the profile it certifies. Graded
     sup-to-sup ‖A‖ (exact induced norm between discrete sup norms — v6's B1 discrete-ball trap
     does NOT apply) at α=1.4: 3.54 (a=0) / 3.88 (0.1) / **2.1e3 (0.2) / 7.6e4 (0.3) / 5.0e5
     (0.4) / 1.6e7 (0.5)**, while cond(M) stays 1.4e6…1.8e7 — so it is the WEIGHTED norm, not
     the matrix. **THE LADDER IS THE MEASUREMENT THAT DECIDES: a=0 gives J^−0.003 (3.551 →
     3.542 → 3.537 over J=200/400/800) and a=0.2 gives J^+2.86, a=0.3 J^+2.75.** Flat at the
     anchor, DIVERGENT at the real profile, same code. MECHANISM: linearizing about a solution
     with a zero of order p has a homogeneous solution ~ s^{−p}, in no sup norm at all. So the
     a=0.2 near-miss in T4 priced a new object with an old object's constants; correcting for
     the real ‖A‖ (budget ∝ 1/‖A‖) turns 7.7× under into ~3 orders over. **Both sides move the
     wrong way, by one mechanism.**
  T6 **THE BOUNDARY: A CANDIDATE MECHANISM, AND THE CONTROL THAT REFUSES TO CONFIRM IT.**
     X_c falls 10.63 (a=0.25) → 3.08 (0.50) → 2.12 (0.70), and the core half-width stays ~1, so
     X_c/half-width tracks X_c. Two readings: GEOMETRIC (no room for two scales once X_c reaches
     the core) and ARITHMETIC (p = 1/a hits the integer 2 exactly at a=1/2, where H of
     (X_c−X)^p_+ grows a log — landing exactly on the four-times-confirmed a*≈0.5). They differ
     at **a = 1/3 (p = 3, also integer, X_c ≈ 5.8 still far outside the core)** and the control
     says the arithmetic reading is WRONG: a=1/3 sits smoothly between its neighbours in every
     column. What survives is a smooth monotone trend with **nothing special at 0.5** —
     consistent with §9-cont2's "soft crossing", and **v12 does NOT predict a\***.
  T7 **LEDGER.** Nothing moved OPEN→BOUNDED. What changed is the SPECIFICATION: Y₀ is now
     measured in the right basis, and a new item joins the open list — **every bounded constant
     in the ledger is a constant for the ANCHOR's linearization, and T5 shows they do not
     transfer to the object the certificate is about.**

**THE REPAIR (v13's spec, with its own kill switch).** Beyond X_c the profile is exactly zero,
so a certificate can work on the **FINITE INTERVAL [0, X_c] with X_c as an UNKNOWN**, and the
far field — eleven legs of decay grading, resonances and tail bounds — is handled in closed form
because there is nothing out there. The price is the interior singularity at X_c, and the
standard reason to expect it refundable is that the singular mode s^{−1/a} is precisely
∂/∂X_c of the solution family: **adding the free boundary as an unknown is the usual way an
apparent singularity of a linearization stops being one.** UNTESTED. Kill switch: build the
free-boundary system at ONE a and measure ‖A‖ against J. If the singular direction is not
absorbed, ‖A‖ still diverges and the framing needs REPLACING, not repairing.

**LESSONS.** (29) **A constant is attached to a POINT, not to a problem.** Seven of ten ledger
constants were bounded — all at the a=0 anchor, because that is where the exact solution is, and
nobody wrote down that the certificate needs them at the a≠0 profile instead. One ladder at the
real profile turned "bounded" into "divergent". Before pricing anything, write down the point at
which the price is quoted. (30) **A number that is under budget is not a result until the
budget was computed for the same object.** T4's 7.7×-under looked like the leg's headline for
half an hour. (31) **When a measurement misbehaves in TWO ways at once (non-monotone in the
parameter, arg-max pinned to the domain edge), stop measuring and ask what object you are
looking at.** Both anomalies were one fact.
HONEST CEILING unchanged: plain float64, nothing interval-enclosed, nothing rigorous.
Clay odds ~0.05%.


## §22 — ROUTE-D v13 DONE (2026-07-31): THE TURNING POINT — §21's MECHANISM WAS WRONG
## (dropped sign); the obstruction is a GROWING FAR-FIELD MODE (log(X/X_c))^{1/a}, the
## divergence is now ATTRIBUTED by measurement, and the cheap repair is DISQUALIFIED.

Built solver/turning_point.py + test_turning_point.py 6/6 (suite now **20 files green**);
experiments/p2_route_d_v13_turning.py → writeup/data/p2_route_d_v13_turning.json → fig31.
NOT a logged Tier run. BLOG/TECHNICAL_P2_ROUTED_V13.md. §21's writeups are corrected IN PLACE
with the change MARKED (banner + struck passages), not quietly edited.

  S1 **THE CORRECTION.** §21 attributed the ‖A‖ divergence to a homogeneous mode
     ~ (X_c−X)^{−1/a}. **Wrong: a sign dropped converting d/dX to d/ds.** With s = X_c−X,
     h_X = −h_s and E = −a h_c s, the homogeneous equation h_c h − a h_c s h_s = 0 gives
     h_s/h = 1/(as) ⇒ **h ~ s^{+1/a}, which VANISHES at X_c**; and the inhomogeneous solve is
     bounded there too (integrating factor s^{−1/a} ⇒ h → g(X_c)/h_c as s→0). **Nothing is
     singular at the turning point.** Measured: +5.28/+4.21/+3.51/+3.01/+2.65/+2.14 over
     a=0.2…0.5 vs +1/a = 5/4/3.33/2.86/2.5/2 — right sign, 5–7% high (the same finite-window
     fit bias as everywhere in this series).
  S2 **WHERE THE WALL IS: THE FAR FIELD.** Outside X_c the same equation has the same exponent
     and it GROWS. H(Ω)~m/(πX), E ~ (am/π)log(X/X_c) ⇒ h_X/h ~ 1/(aX log(X/X_c)) ⇒
     **h ~ (log(X/X_c))^{1/a}**. The domain space is a DECAY class, the amplitude is fixed by
     matching to the inner solve rather than free ⇒ the image generically LEAVES the space:
     **a codimension-1 RANGE obstruction of the continuum operator, which no refinement
     touches** — strictly worse than the local singularity §21 named, which would at least
     have been a resolution problem. Measured with an instrument independent of the matrix
     (integrate h_X = (H(Ω)/E)h outward on the profile's exact H(Ω), E, to X=1e8):
     q = **4.9988 / 3.9980 / 3.3307 / 2.8536 / 2.4855** vs 1/a = 5 / 4 / 3.3333 / 2.8571 / 2.5
     — **0.02–0.6%, no fitted constant**. Quadrature converged (1.6e-4 over a 16× refinement).
  S2b **THE ROW THAT DID NOT FIT, REFINED NOT DROPPED.** a=0.5 returns q=0.054 vs 2. J-ladder:
     a=0.5 → 0.054 / 1.838 / 1.696 over J=400/800/1600 while the a=0.4 control is
     2.4855 / 2.5035 / 2.5014 (four digits). **The outlier is the instrument** — §21 T4 had
     already reported the collocation profile stops converging there.
  S3 **1/a APPEARS THREE TIMES, IN THREE ROLES:** the order of the profile's zero at X_c; the
     exponent of the vanishing INNER mode; the power of the log by which the OUTER mode grows.
     All three from one leading balance, none with a fitted constant.
  S4 **THE DIVERGENCE, ATTRIBUTED RATHER THAN ARGUED.** Recompute ‖A‖ with the DOMAIN sup
     restricted to a FIXED outer radius (the grid's own radius ~4J/π grows with J):
     J-slopes at X≤20 / 50 / 200 / all = **J^−0.00 ×4 (a=0, control)**, **+0.31/+0.54/+1.06/
     +2.86 (a=0.2)**, **+0.53/+1.15/+1.42/+2.75 (a=0.3)**. Monotone in the cutoff, nearly gone
     without the far field, and the a=0 control is flat at EVERY cutoff. Complementary: the
     fraction of the extremal row's mass from codomain slots within 10% of X_c is
     69→86→92% (a=0.2) and 87→93→97% (a=0.4) over J=200/400/800 ⇒ **sourced at the turning
     point, damage done in the far field** — exactly a growing mode excited at X_c.
     **NOT ATTRIBUTED (say it): the residual J^+0.3…0.5 at X≤20.** Small, real, unexplained.
  S5 **THE CHEAP REPAIR IS DISQUALIFIED, FOR A REASON ALREADY IN THESE NOTES.** §21 recommended
     bordering with the speed c. **Dilation Ω(X)→Ω(X/μ), c→μc is a SYMMETRY of the zero set at
     every a, so restoring c supplies KERNEL, not range** — which is why v1 Q2 and v11 V0 both
     found the one-gauge system singular. Measured anyway: the SQUARE bordered system at a=0
     has **cond 4.4e18, smin 4.4e-17** (singular to machine precision), and the overdetermined
     version's norm GROWS with J **even at the anchor** (J^+1.40, where the plain system is
     flat), and J^+1.57 / J^+1.86 at a=0.2/0.3.
  S6 **WHAT THE REPAIR HAS TO DO NOW.** Not "border the operator" — **remove the far field
     from the DOMAIN**: pose the problem on [0, X_c] with X_c an unknown and perturbations
     supported there, so the growing mode has nowhere to live. Consistent, because the residual
     Ω H(Ω) − E Ω_X vanishes identically outside the support (every term carries Ω or Ω_X)
     even though H(Ω) does not. Kill switch unchanged: build it at ONE a, measure ‖A‖ vs J.

**LESSONS.** (32) **A mechanism is a claim and needs its own gate.** §21's measurements were
gated six ways; the SENTENCE explaining them was not gated at all, and it was wrong. Fitting
the exponent it predicts costs ten minutes and is now test_turning_point gate 1. **If a writeup
asserts an exponent, fit it.** (33) **Attribute a divergence by making the suspected cause stop
moving.** "It is the far field" became a measurement the moment the domain sup was restricted
to a fixed radius — and the same ladder produced the honest residual (J^+0.3 at fixed radius)
that the story does not explain. (34) **The cheapest disqualification is a symmetry count.**
Restoring c to fix a range obstruction was disqualified on paper by a fact recorded twice
already in these notes; measuring it took three minutes and made the paper argument checkable.
HONEST CEILING unchanged: plain float64, nothing interval-enclosed, nothing rigorous.
Clay odds ~0.05%.


## §23 — ROUTE-D v14 DONE (2026-08-01): THE EQUATION HAS A FIRST INTEGRAL, and on its own
## support THE KILL SWITCH PASSES — ||A|| FLAT in K against the whole line's J^+2.80.

Built solver/first_integral.py + test_first_integral.py 11/11 (suite now **21 files green**);
experiments/p2_route_d_v14_first_integral.py → writeup/data/p2_route_d_v14_first_integral.json
→ fig32. NOT a logged Tier run (deterministic). BLOG/TECHNICAL_P2_ROUTED_V14.md.

**THE IDENTITY.** E := c + aU has E_X = a H(Omega) by definition, so on {Omega != 0}

    R = Omega H(Omega) - E Omega_X = 0  <=>  (log|Omega|)_X = (1/a)(log E)_X
    =>  |Omega| = C E^{1/a},  and the gauge Omega(0) = -1 gives C = c^{-1/a}:

        **Omega(X) = -( E(X)/c )^{1/a},   E = c + aU,   U_X = H(Omega).**      (FI)

Thirteen legs discretized an equation that integrates once in closed form.

**GATES (three, all against something that is not this module).**
- **a -> 0 IS the anchor.** (1+aU/c)^{1/a} -> exp(U/c); on the anchor U = -(1/2)log(1+X^2),
  c = 1/2, so Omega = -1/(1+X^2) **exactly** — measured **1.11e-16**, and the finite-a form
  approaches it at the predicted O(a) (fitted a^1.011).
- **On the whole-line collocation build, which knows nothing about it.** Spread of
  |Omega|/E^{1/a} over the core: a=0.2 **5.9e-8 -> 1.0e-11** over J=200..1600 (profile relres
  1.8e-6 -> 8.7e-10); a=0.3 **2.3e-6 -> 5.1e-9** (relres 6.2e-5 -> 4.5e-7). The defect is an
  order BELOW the profile's own residual at every J and falls FASTER (x251 vs x126; x20 vs x9)
  — the signature of an exact identity on an approximate object. Gate written as a RATE, not
  a threshold, because a threshold would only have measured the profile.
- **The reconstruction solves the ORIGINAL R.** Off-node, independent quadrature:
  max|R| = 6.8e-7 -> 4.3e-8 -> 2.7e-9 -> **1.9e-10** as the U-quadrature refines (n^-1.98).

**WHAT (FI) GIVES FOR FREE (three §21 measurements become one-liners).**
- **The profile ENDS, forced not discovered.** E decreases (E_X = aH(Omega) < 0 for X>0),
  hits 0 at finite X_c, beyond which E^{1/a} is not real => Omega == 0, self-consistently.
  CAVEAT SAID OUT LOUD: needs H(Omega)<0 for X>0 — true on every solution found, not proved.
- **Zero of order 1/a WITH the amplitude.** E vanishes linearly at X_c, so
  Omega ~ -A (X_c-X)^{1/a}, A = (2 s(1)/X_c)^{1/a}. Fitted exponents 4.000019/3.333350/
  2.500014/2.000013/1.250017 vs 1/a at a=0.25/0.3/0.4/0.5/0.8 (rel err <= 1.4e-5).
- **Only finitely smooth.** Omega in C^{1/a} at the edge; classical (C^1) exactly while a<1.
  **At a=1 (De Gregorio) the edge is a CORNER**; a>1 is a cusp. Flagged as an OBSERVATION,
  not a claim — needs the literature check, not another leg.

**THE REDUCED SYSTEM (RS).** v=X/X_c, e(v)=E(X_c v)/c; the finite Hilbert transform is scale
invariant so X_c leaves H:  c e' + a X_c Hpv[e^{1/a}] = 0, e(0)=1, e(1)=0, c a pure scale
(report the dilation invariant X_c/c). TWO structural reasons it converges where the direct
build did not, both worth carrying:
  1. **e(1)=0 goes in the ANSATZ** (e = (1-v^2)s, s even Chebyshev), so the order-1/a zero is
     an OUTPUT, not something a grid resolves and not something put in by hand.
  2. **The edge row is NON-DEGENERATE.** R itself is identically 0 at X_c (every term carries
     Omega or Omega_X), so a collocation row there carries no information and a direct build
     must append an ad-hoc free-boundary condition; (RS) has c e'(1) = -a X_c Hpv[w](1) with
     both sides nonzero. **The free boundary is priced by the equation.**
solver/finite_support.py (the direct build) never converged — residual 1.4 after 59 iterations
at a=0.3. (RS) converges from a **COLD START** (s==1, X_c0=10 at every a) in **5-10 Newton
steps to ~1e-14**, for every a in 0.2..1.2. Numerics: one p.v. subtraction against the exact
log((1+v)/(1-v)), composite Gauss-Legendre on geometrically graded panels; gated against the
exact airfoil family (1/pi)p.v.INT sqrt(1-u^2)U_{n-1}/(v-u) = T_n to **5.3e-14** (deliberately
harsher than anything the module meets: sqrt is endpoint order 1/2, the profiles are 1/a>=2).
CROSS-BUILD: X_c/c vs the whole-line profile's own E-crossing **3.9e-6 / 4.3e-6 / 7.3e-5** at
a=0.3/0.4/0.5 (§21's two builds agreed to 0.06-0.11%); K-converged to **3.7e-13** over K=64..192.

**THE KILL SWITCH — IT PASSES.**
  a=0.2:  6.274 7.426 7.528 7.320 7.301 7.299 7.304 7.306  (K=16..192)  **K^-0.0009** (K>=48)
  a=0.3:  4.528 4.505 4.508 4.513 4.518 4.518 4.519 4.520               **K^+0.0009**
  a=0.4:  3.063 3.060 3.062 3.068 3.070 3.072 3.071 3.073               **K^+0.0010**
  a=0.5:  2.207 2.206 2.208 2.213 2.214 2.215 2.215 2.216               **K^+0.0011**
CONTROL, same code and same decay grading that produced §21's number (turning_point.
graded_norm_by_radius, alpha=1.4): a=0 **J^-0.004** (§21: -0.003), a=0.2 **J^+2.800**
(§21: +2.86), a=0.3 **J^+2.785**. Same object, reproduced.
TWO HONESTY ITEMS: (i) the a=0.2 FULL-ladder slope is K^+0.0308 — the K=16 point is
under-resolved, because X_c/c=34.3 while the core stays O(1), so v carries a layer of width
~1/X_c and needs K >~ X_c; both slopes are reported. (ii) **The flatness is not an artifact of
an unweighted norm**: repeating with the decay grading at alpha=1.4 gives K^-0.0030/+0.0008/
+0.0011/+0.0013. It HAS to — on a COMPACT interval every such weight is bounded above and
below. Worth saying because the UNWEIGHTED whole-line norm grows J^+0.99 **even at the anchor**,
purely from the grid's outer radius ~4J/pi growing with J.

**THE RADIUS LAW, CONSTANTS MEASURED (recommended brick (3), delivered).**
log(X_c/c) = -pi(c/a + U_0)/m with the profile's OWN m = INT Omega and U_0 (measured OUTSIDE
the support, where Omega==0 and there is no p.v.). §21's e^{c/a} is this law with the ANCHOR's
m = -pi; the real m runs -4.55 -> -2.43 over a=0.2..1.0, so the coefficient of 1/a is
-pi c/m ~ 0.69 at a=0.2, NOT 1. Law/measured: **0.997 / 0.986 / 0.971 / 0.954 / 0.938 / 0.909
/ 0.887** at a=0.2/0.3/0.4/0.5/0.6/0.8/1.0 — improving monotonically as a->0, which ATTRIBUTES
the error (a far-field expansion evaluated at X_c, and X_c grows as a falls).

**§20's FOURTH CONFIRMATION OF a* DOES NOT SURVIVE (the other three do).** §20 read a
whole-line grid spread (3.7e-3 at a=0.8, 1.3e-2 at a=1.0 vs 3e-5 at 0.5) as "continuum objects
only up to a~0.5". On (RS) the same object is K-converged to **6.3e-13 / 4.9e-12 / 2.2e-10 /
2.3e-9 / 7.6e-9** at a=0.5/0.6/0.8/1.0/1.2, cold start at every one. The spread was the global
basis failing on a compactly supported profile whose edge regularity is C^{1/a} and therefore
gets WORSE as a grows — the same artifact family as §21's ringing (lesson 31). **What is
retired is §20's ARGUMENT, not a\*:** the other three confirmations (§9-cont2 GA-/genome-/basis-
convergence) are about the two-scale GA problem, a different question this leg does not touch.
So a* is confirmed THREE times, and separately the compactly supported traveling wave exists
as a grid-converged continuum object well past it.

**NOT CLAIMED.** Not a certificate — Y0, Z0, Z1, Z2 have not been computed in the reduced
space; ||A|| converging says the approximate inverse EXISTS in the limit, nothing about the
radii polynomial closing. **4.52 is NOT "better than 47"**: v7-v9's bounds are a DIFFERENT
operator in a DIFFERENT space, and the comparable quantity is the SLOPE, not the value
(quoting the value as a gain would be lesson 28 in a new costume). ||A|| here is an exact
measured induced norm of the discrete matrix, not a continuum upper bound. The reduced <->
original equivalence is for even, negative, unimodal profiles. **Novelty UNCHECKED** — a first
integral of a scalar traveling-wave equation is exactly the sort of thing that is folklore to
people who work on gCLM/De Gregorio, and the literature search (standing item (5)) blocks any
novelty claim. What is not in doubt is that this project spent thirteen legs discretizing an
equation that reduces in one line.

NEW LESSONS BANKED. (36) **Before discretizing, try to integrate.** Thirteen legs of space
design, norm design, adversary construction and constant-pricing were spent on an equation with
a closed-form first integral, and the integration is two lines. The tell was in the notes the
whole time: E was DEFINED in §21 and its derivative is the equation's own nonlinearity.
(37) **A degenerate row is a formulation smell, not a bookkeeping nuisance.** The direct build
needed an ad-hoc free-boundary condition precisely because the residual carries no information
at the edge; the formulation in which the edge row is nonzero is the one that converges from a
cold start. When a build needs a condition "appended", ask what the equation forgot.
(38) **When you change formulations, re-measure the CONTROL with the new code.** The contrast
"flat vs J^+2.8" is only a contrast if both sides are the same norm; an unweighted whole-line
ladder diverges J^+0.99 at the ANCHOR, and quoting that as the control would have manufactured
a result out of a grid radius. (39) **A repair that works also re-opens what the broken version
had banked.** Fixing the formulation retired a banked confirmation of a\* — because the evidence
for it was a symptom of the same instrument defect. Re-run the OLD conclusions through the NEW
formulation, not only the new question.
HONEST CEILING unchanged: plain float64, nothing interval-enclosed, nothing rigorous.
Clay odds ~0.05%.


## §24 — ROUTE-D v15 DONE (2026-08-01): THE LITERATURE CHECK. L1 IS OCCUPIED TERRITORY;
## v14's first integral must be PRESUMED KNOWN; the swing moves to the DSS lane.

No code, no figure, no measurement — this is scoping, Level-0. Data
writeup/data/p2_literature_scope.json (every lead with an explicit confidence and a
must_verify list). Writeups TECHNICAL/BLOG_P2_LITERATURE_SCOPE.md.

**THE LIMITATION, FIRST: NOT ONE PAPER WAS READ.** This container's network policy blocks
arxiv.org and every publisher domain reached — WebFetch and curl both 403 at the proxy's
CONNECT step. The only instrument was web SEARCH. Identifiers (titles, authors, arXiv
numbers, DOIs) are reliable; every technical statement below is a paraphrase of a search
summary and is a LEAD, not a fact. Recorded anyway because a labelled unverified lead is
useful and an unlabelled one is a liability.

**WHAT IT FOUND.**
- **arXiv:2603.25104 (Huang, Tong, Wang, 2026-03-26)** — gCLM self-similar blowups with
  singular profiles. Abstract-level: the two-scale blowup's INNER PROFILE IS GOVERNED BY A
  TRAVELING WAVE on the smaller scale and **THE EXISTENCE OF THOSE TRAVELING WAVES IS
  ESTABLISHED RIGOROUSLY VIA A FIXED-POINT METHOD**. That is THIS PROJECT'S OBJECT. Also, and
  this is the highest-value unverified item in the whole leg: the two-scale scenario is
  described as the **a <= 0** case, with **a > 0 giving ONE-scale self-similar blowups**. This
  project has worked the two-scale object at a > 0 throughout. **If that sign is right the
  question is not whether our object is novel but whether it is the RIGHT OBJECT.**
- **arXiv:2305.05895 (same group, 2023)** — exact self-similar gCLM profiles for all a <= 1,
  "either smooth on the whole real line or **COMPACTLY SUPPORTED** and smooth in the interior
  of their closed supports"; existence via the fixed point of an a-dependent nonlinear map
  R_a with Omega(x) = -x f(x) and the scaling constants explicit integrals of f; a=0 and
  a=1/2 strictly negative on (0,inf), **a=1 compactly supported**. So §21's "the profile ends"
  is a known phenomenon and §23's reduction is a known technique.
- **Okamoto-Sakajo-Wunsch, DCDS 34 (2014) 3155-3170** — gCLM steady states AND TRAVELING WAVES
  computed, asymptotics described, existence for every a > 0 argued numerically. Since 2014.
- **arXiv:2209.08232** — infinitely many compactly supported self-similar De Gregorio
  solutions on the line (omega odd, supported on [-1,1]).
- **THE DECISION-RELEVANT ONE:** computer-assisted proofs by interval arithmetic (INTLAB) +
  Newton-Kantorovich are **ROUTINE in this exact family** (Chen-Hou rigorous numerics; and per
  search summary, one-scale asymptotically self-similar CLM blowups already certified).
- **arXiv:2604.09949 (2026-04-10, single author)** claims stable finite-time singularity for
  3D Navier-Stokes with a computer-assisted Newton-Kantorovich validation. **DO NOT USE, DO
  NOT REPEAT AS A RESULT, DO NOT RE-PLAN AROUND IT.** Recorded only so a later session does
  not rediscover it and get excited.

**WHAT IT DOES TO L1.** L1 = "a certified (Level-2, computer-assisted) blow-up profile for the
1D gCLM/HL toy model at some a > 0". **On this evidence it is OCCUPIED TERRITORY**: the
technique is routine for the groups in this area and the specific object's existence appears
to have been settled analytically five months ago. Finishing the certificate is therefore a
**CAPABILITY DEMONSTRATION and a REPRODUCTION** — which is exactly what standing brick (4)
always said it was, in a bullet the project had been quietly ignoring. **The marginal value of
the next Route-D leg just dropped, for a reason external to the work.**
WHAT IT DOES NOT DO: does not touch the two structural walls; does not change the ~0.05% Clay
odds; does not invalidate one measurement in v3-v14. **Being second is not being wrong.**

**v14's NOVELTY CLAIM, RETRACTED TO THE RIGHT LEVEL.** §23 hedged ("novelty unchecked");
the hedge was right and is now stronger — **presume the first integral is KNOWN**. §23's
writeups are corrected IN PLACE with the change MARKED (banner + struck passage), not quietly
edited (lesson 35). The mathematics is unaffected.

**RECOMMENDATION CHANGE (this is the output of the leg).**
  (1) **VERIFY THE TWO LOAD-BEARING READINGS** — the a-sign in arXiv:2603.25104, and whether
      its fixed point IS this first integral. Both need a PDF, i.e. a session with arXiv
      access or a human. **The binding constraint on the next decision is ACCESS, not compute
      and not cleverness.** Until then treat the a > 0 two-scale object as POSSIBLY WRONG.
  (2) **THE DSS LANE (standing item (1)) BECOMES THE SWING.** It was already ranked first on
      theory — Necas-Ruzicka-Sverak/Tsai rule out exactly self-similar NS blowup, so a
      Clay-relevant candidate must be discretely self-similar; a DSS blowup is a PERIODIC ORBIT
      of the rescaled flow, which is a global search problem, which is what this project's
      tooling is actually good at. The search did not turn up anyone doing that particular
      profile search — **and that is the WEAKEST inference in the leg. Absence of search hits
      is not absence of literature. Never let it harden into "nobody has done it".**
  (3) **Finish the certificate anyway, cheaply, and stop calling it the result.** Every other
      lane needs a pipeline that demonstrably closes.

NEW LESSONS BANKED. (40) **Check the literature BEFORE the fourteenth leg, not after.** The
search cost under an hour and it re-priced fifteen legs of work. Everything about the project's
own discipline — gate the mechanism, build the adversary, price the elasticity — is aimed at
not fooling yourself with your own instruments, and none of it can tell you that someone else
finished first. **A project that only measures itself against its own previous leg will walk a
long way in a direction that is already occupied.** (41) **Record the negative lead with its
confidence, or it will be re-found and re-believed.** The extraordinary NS-singularity preprint
is in the data file explicitly flagged "do not use", precisely so the next session does not
spend a day on it. (42) **When the binding constraint is ACCESS rather than compute, say so
and name what would unblock it.** The cheapest decisive act available to this project is now
"read one paper", and it is blocked by a network policy — that is a fact about the situation
worth writing down rather than routing around.
HONEST CEILING unchanged: plain float64, nothing interval-enclosed, nothing rigorous.
Clay odds ~0.05%.


## §25 — ROUTE-D v16 DONE (2026-08-01): THE FLOAT REHEARSAL. Y_0 IS FINALLY MACHINE-LEVEL;
## Z_2 DOES NOT EXIST IN THE SUP SETTING, AND THE FAR FIELD IS NOT WHY.

Built solver/reduced_certificate.py + test_reduced_certificate.py 16/16 (suite **22 files
green**); experiments/p2_route_d_v16_rehearsal.py → writeup/data/p2_route_d_v16_rehearsal.json
→ fig33. NOT a logged Tier run (deterministic). BLOG/TECHNICAL_P2_ROUTED_V16.md.
Framing set by §24: the certificate is a **one-chunk CAPABILITY build**, not the result.

**Y_0 REACHES MACHINE PRECISION — the first genuinely good number in the ledger.** The defect
that matters is the residual of the INTERPOLANT as a function (§21's distinction, and it
survives the change of formulation): off-node sup|F| at a=0.3 runs **1.5e-2 → 4.0e-5 → 2.0e-10
→ 1.5e-12** over K=16..96, against a NODAL control flat at 1e-14 by construction. Fitted
K^-13.0 (a=0.3) / K^-16.3 (a=0.4) above the 1e-11 float floor vs the K^-(2/a+1) the (1-v)^{1/a}
branch predicts (-7.7/-6.0) — **the fits are floor-contaminated, so the honest claim is
"faster than algebraic and it reaches machine precision", NOT a rate.** For scale: GA floor
~1e-2 for five legs; §22's anchor-priced budget 2.4e-4. **Z_0 = ||I - A DF|| = 1.6e-11**
(roundoff, as it must be; reported for ledger completeness only).

**Z_2 IS INFINITE IN THE SUP SETTING. TWO INDEPENDENT REASONS, NEITHER THE FAR FIELD.**
- **(a) H IS UNBOUNDED ON SUP — ON A BOUNDED INTERVAL.** §13's W3 is a LOCAL fact (it is about
  a jump, not about infinity) and a bounded domain does not repair it. **Removing the far field
  killed the DECAY grading and left the SMOOTHNESS one completely untouched.** Adversary built
  inside the actual perturbation space de=(1-v^2)ds (Chebyshev partial sums of a step):
  **1.350/1.601/2.061/2.351/2.727/3.040 over K=8..256, LINEAR IN log K at +0.499 per e-fold**
  (classical 2/pi=0.637; the deficit is the (1-v^2) damping the jump region).
  **THE INSTRUMENT CHECK THAT MAKES IT TRUSTWORTHY:** the NAIVE probe (one high Chebyshev mode)
  ALSO reports a divergence — 0.998/2.935/6.436 at K=64/128/256 — **and it is entirely the
  quadrature**: under a 4x refinement (levels/order 20/20 → 30/80) the naive row at K=256
  collapses **6.436 → 3.007 → 2.985 → 0.999** while the adversary row is **2.991 → 3.038 →
  3.040 → 3.041**. One row moves, one does not. Lessons 9 and 14 in one table; BOTH rows are
  kept in the module and the figure, not just the one that supports the conclusion.
- **(b) sup|N''| IS FINITE EXACTLY FOR a <= 1/2.** N(e)=e^{1/a}, N''=p(p-1)e^{p-2}, p=1/a, and
  e vanishes LINEARLY at the edge ⇒ finite iff p>=2 iff **a <= 1/2** — **exactly where
  Omega = -e^{1/a} loses C^2**. Displayed as GROWTH under an edge cutoff tightened over eight
  decades (1e-2 → 1e-10), because quoting whatever a grid reached would hide the divergence:
  growth factor **1.00 for a=0.2/0.25/0.3/0.4/0.45/0.5** and **28.5 / 466 / 3.8e4 / 1.0e6 for
  a=0.55/0.6/0.7/0.8**. At a=1/2 the value is p(p-1)=2 EXACTLY (code returns 2.000000000000,
  hand-checkable).
  **THREE THINGS THIS IS NOT.** (i) NOT a statement about the equation — §23 solves the profile
  grid-converged to a=1.2; **the traveling wave exists, it is the CERTIFICATE'S NORM that
  fails**. (ii) **NORM-DEPENDENT** — a domain weight vanishing like (1-v)^{(2-1/a)/2} restores
  finiteness at the price of requiring perturbations to vanish at the edge (lesson 13's trade,
  in a new place). (iii) **NOT an explanation of a\***. The coincidence with the independently
  measured a*~0.5-0.55 is recorded BECAUSE it is striking and because recording it is how the
  next person disproves it. §22's a=1/3 control is the precedent — a tantalising coincidence at
  a* that a control killed. **No control has been run here, so it stays an observation.**

**Z_1 IS NOT COMPUTED AT ALL** — the infinite-dimensional tail is the entire content of a real
CAP. `rehearsal()` returns it as **None, not zero**, and **deliberately REFUSES to return a
radii polynomial**: assembling one from a ledger with a hole or an infinity in it is exactly
lesson 15's failure mode.

**VERDICT: THE SUP-TO-SUP REHEARSAL DOES NOT CLOSE**, and not for the reason §21/§22 found.
**THE REPAIR IS §14's AND IT IS MEASURED, NOT ASSUMED:** the same adversary against
||de||_gamma = sup|de| + [de]_gamma gives slopes **+0.066 (0.15) / +0.014 (0.25) / -0.021
(0.35) / -0.049 (0.5) / -0.057 (0.65) / -0.050 (0.85)** — the divergence stops at
**gamma >~ 0.35**, and gamma=0.15 STILL CREEPS, which is what shows the threshold is real
rather than an artefact of dividing by any seminorm at all. **§14 U1 found the SAME 0.35 on the
whole line — a genuine INDEPENDENT check, because §14's norm ALSO carried a decay grading and
this one has none, so the threshold belongs to the SMOOTHNESS half.** So §14/§17's Holder
machinery is the next brick and NOT wasted: its compact-interval version has **no decay
grading, no resonance, no matching radius X_0 and no tail bound** — roughly §16-§18 with the
expensive half deleted.

**CORRECTION TO §23:** "the cold start converges at every a" is slightly overstated. At
**a=0.7 the cold start (X_c0=10) misses the basin** and continuation from the neighbouring a is
needed; every other value in 0.2..1.2 converges cold. Small, but it was a claim.

NEW LESSONS BANKED. (43) **When a repair removes an obstruction, enumerate the OTHER
obstructions before assuming they went with it.** §23 removed the far field and I carried an
unstated assumption that the smoothness requirement went too. It did not, and it never could
have: H's unboundedness on sup is about a jump, not about infinity. **Ask which of the old
requirements were actually ABOUT the thing you removed.** (44) **Two independent-looking signs
of the same conclusion can be one real fact and one instrument artifact — and they will not
feel different.** The naive single-mode probe and the step adversary both said "divergent";
refining the quadrature killed one and left the other untouched. Reaching the right conclusion
for a wrong reason is how a wrong reason survives several legs. **Refine the instrument on
EVERY row, including the ones you agree with.** (45) **A ledger entry that is unknown must be
None, never zero, and the assembly must refuse to run.** Returning a budget with Z_1 silently
absent would have produced a closed-looking result off a ledger with a hole in it.
HONEST CEILING unchanged: plain float64, nothing interval-enclosed, nothing rigorous.
Clay odds ~0.05%.


## §26 — ROUTE-E v1 DONE (2026-08-02): THE DSS LANE OPENS AND ITS CHEAPEST ENTRANCE IS SHUT.
## NO EIGENVALUE IS AVAILABLE FOR A HOPF BIFURCATION; THE LOG-PERIODIC DIRECTIONS ARE
## CONTINUOUS SPECTRUM. Two self-caught errors, both banked.

Built solver/rescaled_spectrum.py + test_rescaled_spectrum.py 8/8 (suite **23 files green**);
experiments/p2_route_e_v1_spectrum.py → writeup/data/p2_route_e_v1_spectrum.json → fig34. NOT
a logged Tier run (deterministic). BLOG/TECHNICAL_P2_ROUTEE_V1.md.

**WHY THIS LEG.** §24 said L1 is occupied territory and moved the swing to DSS. Necas-Ruzicka-
Sverak (ext. Tsai) rules out EXACTLY self-similar NS blowup, so the surviving candidate class is
DISCRETELY self-similar — and in dynamic-rescaling variables **self-similar = FIXED POINT, DSS =
PERIODIC ORBIT**. The cheapest way a periodic orbit could exist near this project's objects is a
**HOPF bifurcation off the fixed point**, which is one dense eigenvalue solve. That is the
gate-check's "cheapest experiment that would tell us the route is dead", run before any DSS
search machinery was built. **It moves NO link of the chain (L1-L4) and is not Clay progress.**

**THE BUILD.** Compactify X = tan(theta/2), odd sines. Then **H(sin k theta) = -cos k theta +
(-1)^k**, **X d/dX = sin(theta) d/d theta** and **d/dX = (1+cos theta) d/d theta** are all EXACT
— the dilation term, which is what makes the far field expensive everywhere else, is a bounded
exact operator on the circle. The velocity is exact too: N_k := ((-1)^k - cos kt)/(1+cos t)
satisfies **N_{k+1} = -2N_k - N_{k-1} - 2 cos kt** (N_0=0, N_1=-1), so every N_k is a TRIG
POLYNOMIAL (the 1+cos t always cancels) and U = sum_k b_k int_0^theta N_k is elementary. **No
quadrature anywhere.** The a=0 self-similar anchor is then ONE MODE, **Omega_0 = -sin theta =
-2X/(1+X^2)**, H(Omega_0) = 1+cos theta, c_omega = -1, residual **1.1e-16**.

**A GAUGE THE PROJECT HAD BEEN CARRYING IS WRONG FOR a != 0.** solver/gclm_family.residual uses
c_omega = 1 - H(Omega)(0) at every a. Differentiate the residual at the origin: R_X(0) =
-a H(Omega)(0) Omega_X(0), so for a != 0 **that flow has NO fixed point at all**. The forced
repair is **c_omega = 1 + (a-1) H(Omega)(0)**, which reduces to the old one at a=0.

**TWO EIGENVALUES ARE EXACT AT EVERY a AND ARE PURE SYMMETRY.** L(X Omega_X) = 0 (dilation) and
**L(Omega) = -Omega + X Omega_X** (amplitude, five lines from the profile equation + the gauge)
⇒ span{Omega, X Omega_X} invariant with matrix [[-1,0],[1,0]] ⇒ **lambda = 0 and -1, always.**
Gated, not trusted: defects **3.0e-15 / 3.3e-16** at a=0 and **1.3e-10 / 9.1e-15** at a=1/2, the
2x2 block exact to 6.1e-16. **AND THEY DOUBLE AS A FREE ERROR BAR** — lambda=0 is exact, so its
COMPUTED value is the spectrum's error at that a: **0.35 at a=0.2, 8.9e-5 at a=1/2.** That
number decided which rows of the sweep were allowed to carry a conclusion.

**AT a=0 THE REST IS CLOSED FORM.** With w = e^{-i theta}, Z = H Omega + i Omega (anchor
Z_0 = 1+w), the linearization in s = delta Z is L s = w s - ((w^2-1)/2) s_w - s(1)(1+w), and
**s_lambda = (w-1)^{1-lambda}(w+1)^{1+lambda}** solves L s = lambda s (one line:
((w^2-1)/2)s_w = s(w-lambda)). Admissible for **-1 < Re lambda < 1** — a CONTINUUM, every member
carrying a fractional power at X=0. Analyticity forces 1-lambda in Z_{>=0} ⇒ exactly {0,-1}.
**THE MEMBER THAT MATTERS: lambda = iy gives s ~ X^{1-iy} against e^{iy tau} = exp(iy(tau -
log X)) — a wave travelling OUTWARD IN log X at unit speed, exactly tau-periodic.** The
log-periodic structure a DSS solution is made of IS in this operator — as CONTINUOUS spectrum,
i.e. dilation transport carrying a scale-invariant wave to infinity, not a bound state.
**Nothing there can cross an axis: that is the MECHANISM behind the negative.**

**THE BRANCH.** alpha(a) = -c_omega(a) is an OUTPUT (far-field balance c_omega Omega =
(X + a U_inf) Omega_X). Richardson over K=64/128/256: **1.000000 / 1.141397 / 1.334497 /
1.617244 / 2.079464 / 3.000000** at a = 0 … 0.5. Followed finely it is lost at **a = 0.65**
(alpha = 11.5 at the last good point) with 1/alpha extrapolating to zero at **a_c ~ 0.694**.
Non-integer alpha = a branch point at X=infinity ⇒ algebraic convergence (K^-2ish at a=0.3).

**THE RESONANCES (and the rule, hypothesised, tested, wrongly retracted, restored).** Odd-integer
alpha ⇒ Omega ~ (pi-theta)^alpha smooth ⇒ spectral. **a=0 (alpha=1, exact); a=1/2 (alpha=3,
c_omega = -3.000000000000, residual 1.4e-14 at K=192, geometric coefficients)** — the a=1/2 point
was FOUND by a residual scan showing a single ten-order dip exactly there. The rule then rested
on two points, so E8c located the third by secant: **alpha=5 at a = 0.5821792673**. Its ladder:
3.19e-2 / 1.12e-2 / 7.92e-4 / 2.87e-5 / 9.24e-7 / 2.55e-8 over K=96..384, implied order **3.6 →
6.5 → 11.5 → 15.4 → 19.7**. **ON THE FIRST TWO RUNGS I WROTE THE RULE OFF AS FALSE AND COMMITTED
IT; the full ladder is exponential and the rule HOLDS at all three points** (the alpha=5 profile
is steeper, so it reaches its asymptotic regime later — exactly when a short ladder misleads).
Corrected in place and MARKED in both writeups. **What stays unexplained is narrower: alpha=3
lands on exactly a=1/2 while alpha=5 lands on 0.5821792673, which is not a special number.**
NOVELTY UNCHECKED (PDF access still blocked — three legs now). A rational ansatz
Omega = -cX/(X^2+gamma)^2 fits the a=1/2 profile to **7e-5** while the profile itself is computed
to 2e-14: a near miss, **the closed form was NOT identified**.

**THE EIGENVALUE THAT WASN'T (the leg's other self-caught error).** The filter kept a THIRD value
at a=1/2 near -2, and its K-ladder made it look BETTER: **-2.007293 / -2.001677 / -2.000467 /
-1.999999** over K=96..256. Six digits of grid-convergence, and it is not a mode. **E9: the two
singular endpoints fix the essential spectrum.** Near X=infinity the local operator is
c_omega + xi d/dxi; near X=0 it is (c_omega + H Omega(0)) - theta d/dtheta; and in THIS space the
minimum far-field exponent is 1 because every sin(k theta) vanishes linearly at theta=pi. So

    **[ c_omega + 1 , c_omega + H(Omega)(0) ]**  =  [0, 1] at a=0  and  [-2, +5] at a=1/2,

measured **[-1.0000, +0.0000] at a=0** (with **99% of the spectrum sitting exactly on the left
edge**) and **[-2.0005, +4.5641] at a=1/2**. The "third eigenvalue" IS the left edge. **The
control was free and decisive: at a=0 the identical edge sits at 0 and carries 99% of the
discretized spectrum — nobody would call that an isolated eigenvalue.** Tightening the filter
would have made the artefact MORE convincing.

**THE VERDICT.** At the two points where the instrument can see (a=0 exactly, a=1/2 spectrally),
**the only grid-converged ISOLATED eigenvalues are 0 and -1 — the two exact symmetry modes. No
complex pair, nothing near the imaginary axis, NO HOPF.** POSITIVE CONTROL: the same filter on
the same operator with a planted smooth bump returns **+1.083 (V=6)** and **+4.578 (V=12)**,
isolated and in the right half plane — so "only symmetry survives" is a measurement, not a blind
spot. **SAID ALONGSIDE, NOT BURIED: the flow is NOT spectrally stable — its ESSENTIAL spectrum
reaches c_omega + H(Omega)(0) = +1 (a=0) and +5 (a=1/2), complex members included (|Im| ~ 150).
Those are the directions with a fractional power at X=0 — a CORNER AT THE ORIGIN grows relative
to the profile. It is norm-dependent, it is the familiar low-regularity essential instability of
self-similar linearizations, and A CONTINUUM HAS NO EIGENVALUE TO MOVE.**

**NOT CLAIMED:** not that gCLM has no DSS solution (only that one is not BORN from a Hopf off the
branch continuing from CLM); nothing about NS (gCLM's scaling is not NS's); nothing at generic a
(the instrument cannot resolve even the modes it is known to have there, and the symmetry error
bar is how that is known rather than guessed); one gauge only.

**NEXT.** The DSS lane is **not closed — its cheap entrance is.** Entering costs a real build (a
periodic-orbit search with no fixed point nearby to seed it), and §4.1 says where such an orbit
would have to live: the log-periodic directions, which are continuum and of limited regularity at
the origin. Weigh that against **(2) the Hou-Luo critical-viscosity map** (well-posed, publishable
either way, directly probes "can a blowup beat viscosity") and **(3) the L1→L2 port to 2D
Boussinesq**. Do NOT default into the expensive DSS build.

**NEW LESSONS.** (46) **A symmetry audit is cheaper than an eigenvalue solve and predicts part of
the answer** — enumerate the symmetry modes first; they are the null result's baseline.
(47) **A null result needs a PLANTED POSITIVE, not just a control** — when the finding is
absence, show the instrument detecting a presence of the same kind. (48) **When you generalize a
gauge, RE-DERIVE it, do not extend it** — lesson (29) in the gauge's clothes. (49) **The
regularity of the object sets the convergence rate of everything built on it, and it can vary
with the parameter** — find where your object is smooth and quote your sharp numbers there.
(50) **An exactly known eigenvalue is a free error bar on every other one** — plot the symmetry
mode's deviation next to every claim about the rest. (51) **A convergence filter can be fooled by
the EDGE of a continuum, and the fix is a CONTROL POINT, not a tighter tolerance** — before
believing an isolated eigenvalue, ask where the continuum's edges are and go look at the same
object where you already understand it. (52) **Two points define a line through anything — and
two RUNGS define a convergence rate through anything.** I wrote the first half of this lesson and
then committed the second half. **Add rungs until the exponent stops moving**; a steeper object
reaches its asymptotic regime later, which is when a short ladder is most misleading.

HONEST CEILING unchanged: plain float64, nothing interval-enclosed, nothing rigorous, no link of
the chain moved. Clay odds ~0.05%.


## §27 — ROUTE-F v1 DONE (2026-08-02): THE CRITICAL DISSIPATION EXPONENT IS HALF THE FAR-FIELD
## DECAY EXPONENT, s_c = alpha/2 — AND NAVIER-STOKES IS THE MARGINAL MEMBER (alpha = 2).

Built solver/fractional_gclm.py + test_fractional_gclm.py 6/6 (suite **24 files green**);
experiments/p2_route_f_v1_viscosity.py → writeup/data/p2_route_f_v1_viscosity.json → fig35.
NOT a logged Tier run (deterministic, ~6 min). BLOG/TECHNICAL_P2_ROUTEF_V1.md.

**WHY THIS LEG.** §26 shut the DSS lane's cheap entrance, which promoted ranked item (2) —
**the only item on the list that probes the ACTUAL obstruction between a toy certificate and
NS rather than polishing the toy**: take a blow-up that exists, add dissipation, find the
scaling at which dissipation kills it. **It moves NO link of the chain.**

**THE PREDICTION, AND IT REUSES §26's BY-PRODUCT.** For omega_t + a u omega_x = omega u_x -
nu(-Delta)^s omega: a self-similar blowup has omega ~ (T-t)^-1 and L ~ (T-t)^beta, and §26's
rescaling ODEs integrate to L ~ (T-t)^{c_l/alpha}, i.e. **beta = 1/alpha** with alpha the
profile's FAR-FIELD DECAY EXPONENT. Comparing nu omega/L^{2s} with omega^2:

    D/N ~ nu (T-t)^{1 - 2s/alpha}     =>     **s_c(a) = alpha(a)/2**.

**AND THAT IS THE NS SENTENCE.** NS's natural scaling is L ~ (T-t)^{1/2} ⇒ beta = 1/2 ⇒
**alpha = 2 ⇒ s_c = 1 EXACTLY — the ordinary Laplacian.** NS is critical; every scaling
argument returns zero information because the two sides balance identically. **In gCLM alpha
is a measured function of a dial**, so the family WALKS THROUGH the point where NS is stuck.
That is the toy's value here: not that it blows up, but that it is off-critical in a
controlled way.

**MEASURE AN EXPONENT, NOT A THRESHOLD.** A binary blowup sweep near a critical exponent is
biased, resolution-dependent, and biased IN THE DIRECTION YOU EXPECT — three ways to fool
yourself in one measurement. Instead fit **D/N ~ (T-t)^p against p = 1 - 2s/alpha**, which
predicts a whole LINE whose slope, intercept and zero are separately checkable.

**F1 KNOWN ANSWER.** a=0, nu=0 is exactly solvable ON THE CIRCLE TOO: z = z_0/(1 - t z_0/2),
z = H(omega)+i omega. Checked against an independent RK4 to **2.3e-14**; the solver reproduces
it to **1.9e-9** at t=2.5. T = 2/max{H(omega_0): omega_0=0}. And alpha(0)=1 EXACTLY, so
s_c(0) = 1/2 — the classical dissipative-CLM value, i.e. **a genuine known-answer gate**.

**F2 THE LINE, WITH NOTHING FITTED** (a=0, n=8192, nu=1e-3, window 0.40-0.94):
p = **+0.733/+0.523/+0.318/+0.109/-0.100/-0.309/-0.503** at s = 0.15..0.75 against predicted
+0.700/+0.500/+0.300/+0.100/-0.100/-0.300/-0.500. Slope **-2.068** vs -2; zero at **s=0.5033**
vs 0.5000.

**F3 THE CROSS-CHECK — THE PART WORTH KEEPING.** alpha comes from §26's STEADY COMPACTIFIED
SOLVE ON THE LINE; dp/ds comes from TIME-DEPENDENT PERIODIC simulation. **No shared grid,
basis, formulation or fitted constant.**

    a          0.0      0.2      0.3      0.4
    alpha    1.0000   1.3345   1.6172   2.0795     (Route-E, steady, line)
    -dp/ds   2.0838   1.5193   1.2560   0.9780     (Route-F, time-dependent, periodic)
    2/alpha  2.0000   1.4987   1.2367   0.9618
    ratio    1.0419   1.0137   1.0157   1.0169

**Ratio 1.022 +- 0.014 while alpha itself DOUBLES** — a uniform ~2% bias, NOT an a-dependent
failure. The SHAPE of the relation is confirmed to sub-percent by an instrument that knows
nothing about the one that produced alpha.

**F4 THE nu CONTROL — PASSES, BUT WEAKLY, and say so.** The prediction contains s and alpha and
NOT nu. Slopes **-1.866/-2.051/-2.110** at nu=1e-2/1e-3/1e-4, spread **0.245**. -2 is inside
the range and the middle decade is within 2.6%, but the spread is not small; the two ends are
where the asymptotic argument is stressed from opposite sides (nu=1e-2 perturbs the blowup,
nu=1e-4 makes D/N noise-limited). **The measurement most worth tightening if revisited.**

**F5 RESOLUTION.** p = +0.395/+0.347/+0.330/+0.318 over n=1024..8192 at s=0.35 (pred +0.300);
whole ladder spans 7.6e-2, **the two finest differ by 1.2e-2**, monotone toward the prediction.
So resolution contributes ~0.01 — an order BELOW the window systematic.

**F7 THE WINDOW, SWEPT NOT CHOSEN (the dominant systematic).** slope
-1.896/-2.043/-2.068/-2.074/-2.001 and zero 0.568/0.518/0.503/0.498/0.478 over windows
0.20-0.80 … 0.60-0.98 ⇒ **slope -2.02 +- 0.09 (pred -2); s_c 0.51 +- 0.05 (pred 0.500)**.
Individual exponents move +-0.07 and approach the prediction MONOTONICALLY FROM ABOVE — an
asymptotic regime being entered. **The slope is far steadier because every s shares the window
and the bias cancels in the difference**, which is why the claims are about slope and zero.

**F6 THE MAP.** s_c = 0.500/0.571/0.667/0.809/**1.040**/**1.500** at a = 0/0.1/0.2/0.3/0.4/0.5;
**s_c crosses the ordinary Laplacian s=1 at a ~ 0.383**, i.e. exactly where alpha = 2.

**THE SENTENCE TO BE CAREFUL WITH.** Above a ~ 0.383 the SCALING says the blowup beats ordinary
viscosity. That is arithmetic about **gCLM's own scaling** and **NOT a statement about NS**. It
does **not** say a viscous gCLM blowup EXISTS there — the scaling says which term dominates
GIVEN the self-similar form; showing a solution reaches it is the whole difficulty. NS's alpha
is pinned at 2 by dimensional analysis and is not a dial. **What the map is good for is
ORIENTATION: it exhibits a family that walks through the point where NS is stuck.**

**THE RESOLUTION GUARD TOOK THREE TRIES** and the failures are instructive. (i) Energy above
2/3 k_max reads **exactly 0.0** at some n and a real number at others, because the 2/3 rule has
ALREADY zeroed that band and whether it lands inside the cutoff depends on rounding in n — a
guard that is zero by construction reads as "perfectly resolved". (ii) Energy above n/6 reads
**~0.37 for every run**, resolved or not: a near-singular spectrum is genuinely fat, so a broad
band measures physics, not discretization. (iii) What discriminates is the amplitude **AT THE
CUTOFF** relative to the peak: 1.0/1.0/1.0/1.0/1.7e-1/1.4e-2/2.0e-4 over n=128..8192. The run
now **REFUSES** ("under_resolved") rather than returning a number off an unresolved state.

**NEW LESSONS.** (53) **When two legs measure the same constant through unrelated machinery,
that cross-check is worth more than either leg's internal error bar.** Refining one computation
cannot test the other; agreement across two tests both. **Look for a second, structurally
different route to a number you already have** — alpha sat in §26's data file as a by-product,
and using it twice turned a curiosity into a check. (54) **A systematic that is UNIFORM across a
sweep is pointing at a shared input, not at the mechanism.** Every p sat above its prediction
with a shallower slope: that is what a wrong singular time does, not what a wrong exponent does.
**Read the PATTERN of the residuals before adjusting the model.** (55) **A guard that can return
"perfect" by construction is worse than no guard.** Two of the three definitions here were
silently degenerate — one identically zero at half the grid sizes, one identically fat at all of
them. **Before trusting a diagnostic, check it on a case you KNOW is bad and one you know is
good, and confirm it separates them.**

HONEST CEILING unchanged: plain float64, nothing interval-enclosed, nothing rigorous, no link of
the chain moved, and this is orientation rather than evidence about NS. Clay odds ~0.05%.


## §28 — ROUTE-G v1 DONE (2026-08-02): THE PORT BROKE THE PREVIOUS LEG'S FORMULA, AND THAT
## IS THE RESULT. The invariant law is s_c = 1/(2 beta), NS is beta = 1/2, and the proven 2D
## blow-up is on the LOSING side of the ordinary Laplacian by a factor of six.

solver/fractional_boussinesq.py + test_fractional_boussinesq.py; experiments/
p2_route_g_v1_collapse.py → writeup/data/p2_route_g_v1_collapse.json (+ _g2.json, merged)
→ fig36. BLOG/TECHNICAL_P2_ROUTEG_V1.md. Deterministic, NOT a logged Tier run.
**This section was MISSING from these notes until 2026-08-03** — the leg was written up in
writeup/ and indexed in the README, but never landed here; §B recorded only its ops. Fixed.

**WHY THIS LEG.** §27 merged ranked items (2) and (3): the same s_c arithmetic applied to a 2D
object is the version of the viscosity question that is about a real mechanism rather than a 1D
caricature. **It moves NO link of the chain.**

**THE PORT BREAKS THE FORMULA, WHICH IS THE POINT.** Route-F's s_c = alpha/2 is true in gCLM
ONLY because that rescaling pins c_l = 1. The invariant statement is

    s_c = 1/(2 beta),   L ~ (T-t)^beta,

with 1D the beta = 1/alpha case. **NS is beta = 1/2 ⇒ s_c = 1 exactly.** Two things invisible in
1D: (i) **s_c DECREASES with beta**, so a FASTER collapse loses to viscosity more easily and
beating ordinary viscosity needs an anomalously SLOW collapse (beta < 1/2); (ii) the far-field
decay exponent and the collapse rate are ONE fact (alpha = -1/beta — the statement that the
blow-up does not disturb the outer solution), which is why alpha/2 looked like a law.

**WHERE THE PROVEN OBJECT SITS.** Chen–Hou 2D Boussinesq: **beta = 2.92, s_c = 0.171** — nearly
six times the NS collapse rate, and nowhere near beating the ordinary Laplacian.

**G2, OUR OWN beta.** Measured by this project's own dynamically-rescaled 2D machine as a
modulation constant rather than taken from the paper, on a steps ladder and a resolution/domain
ladder. See §B for how that stage was orphaned by a killed container, recovered without a
re-run, and then cut from ~41 min to ~16.

**G3 THE DIRECT ROUTE, PRICED AND REFUSED**, with the window report and the underpowered p(s)
line kept for its SIGN STRUCTURE rather than its magnitudes. G4 cross-model calibration on
gCLM's dial, including a continuation to a < 0.

HONEST CEILING: plain float64, nothing interval-enclosed, nothing rigorous, no link of the chain
moved. This is arithmetic about collapse rates, NOT a claim about NS and NOT a claim that a
viscous blow-up exists anywhere on the map.


## §29 — ROUTE-H v1 DONE (2026-08-03): THE MARGINAL CASE. mu BECOMES A DYNAMICAL VARIABLE, so
## Route-F's s_c is an EIGENVALUE and criticality reduces to the SIGN OF ONE NUMBER, alpha_1.
## Dissipation DOES discretize Route-E's continuum — and the DSS lane stays shut anyway.

solver/critical_dissipation.py + test_critical_dissipation.py **10/10**; experiments/
p2_route_h_v1_critical.py → writeup/data/p2_route_h_v1_critical.json → **fig37**.
BLOG/TECHNICAL_P2_ROUTEH_V1.md. Deterministic, NOT a logged Tier run (~10 min).

**WHY THIS LEG.** §27 and §28 both stopped at the same wall: AT s = s_c the two terms balance
identically and scaling returns ZERO INFORMATION. **That is exactly where NS sits** (beta = 1/2
⇒ s_c = 1, the ordinary Laplacian), so the marginal case is not a corner of the map — it is the
case. **It moves NO link of the chain.**

**THE REFRAME.** Keep the dissipative term through the dynamic rescaling and its coefficient
mu = nu/(A L^{2s}) becomes an autonomous DYNAMICAL VARIABLE:

    Omega_tau = (c_omega + H Omega) Omega - X Omega_X - a U Omega_X - mu Lambda^{2s} Omega
    mu_tau    = (2s - alpha[Omega, mu]) mu ,        alpha = -c_omega .

**(i) Route-F's s_c is the EIGENVALUE lambda_mu = 2s - alpha_0** of the inviscid fixed point in
the mu-direction — a scaling exponent becomes a stability exponent. **(ii) AT criticality that
eigenvalue is exactly zero**, so the quadratic term decides: mu_tau = -alpha_1 mu^2 with
alpha_1 = d alpha/d mu. **ONE NUMBER, and only its sign.**

**THE GAUGE HAD TO BE RE-DERIVED** (banked lesson 48 applied to the previous leg's own gauge):
Lambda^{2s} Omega is odd, so its X-derivative at 0 is NOT zero and
c_omega = 1 + (a-1)H(Omega)(0) + mu (Lambda^{2s}Omega)_X(0)/Omega_X(0). Gate 3 finite-differences
the resulting Jacobian to **4.0e-11** because (N') contributes a quotient.

**H1 THE KNOWN ANSWER.** At a = 0, s = 1/2 complexification (z = H(omega)+i omega, Lambda z =
i z_x) turns the viscous CLM equation into z_t + i nu z_x = z^2/2, whose characteristics are a
CONSTANT complex shift. Out drops an exact viscous blow-up
omega = -2(1+mu_0) kappa x/(kappa^2(T-t)^2 + x^2) with ||omega||_inf = (1+mu_0)/(T-t), for EVERY
nu and every mu_0. PDE residual in closed form (no quadrature, no differencing): **6.3e-16**.

**H2 a = 0 CARRIES A LINE.** In rescaled variables that family is Omega = -(1+mu_0) sin theta
with **alpha == 1 IDENTICALLY**, so alpha_1 = 0 and the marginal direction is neutral to ALL
orders. Newton from a cold start rediscovers it: alpha = 1.00000000000000 and |num-exact| <=
8.4e-15 at mu = 0 ... 4, i.e. where the dissipative term is FOUR TIMES everything else.

**H3 a = 1/2, s = 3/2: alpha_1 = 0.133683 > 0, so mu DECAYS** — verdict relaxes_to_inviscid.
K = 96/144/192/240 gives 0.132770/0.133470/0.133628/0.133683, **spread 9.1e-4**, while the
Lambda^3 truncation falls 0.084 -> 0.010. **THE CHORD IS NOT THE DERIVATIVE**: a straight fit of
alpha vs mu over mu <= 0.2 returns 0.1264 against the extrapolated 0.1337, **5.5% wrong in the
one number the verdict is quoted from**, so the SECANTS are fitted and extrapolated to mu = 0.

**H4 THE THIRD POINT IS NOT REACHED, AND THE REFUSAL PREDICATE IS THE LESSON.** At a =
0.5821792673, s = 5/2 the K = 288 rung converges to a respectable-looking 1e-4 and
alpha_slope returns **alpha_1 = -0.0017, the OPPOSITE verdict to a = 1/2**. It is not a
measurement: the whole excursion of alpha across the mu-window is **2.0e-5, a factor of 19 BELOW
the residual**. Refusing on the residual alone would NOT have caught it. The gate is now
`drift > 10 x worst residual` — "is there signal above the solve error", a stricter question
than "did it converge" — and it is unit-tested (gate 10) against those exact numbers.
**Second finding: §2's "lucky alignment" was overstated and is corrected in place.** Landing on
an odd-integer alpha makes Lambda^{2s} a FINITE matrix; it does not make the COMPOSITE accurate.
Lambda^p weights mode k by k^p and so amplifies precisely the coefficients the single final
truncation discards — measured worst truncation ratio **1.7e4 at K = 192 and 1.5e3 at K = 288** (p = 5). It DOES
fall (~K^-4) but from so far above 1 that trustworthy Lambda^5 needs K ~ 3000.
The alignment buys p = 1 and p = 3 and does not buy p = 5. **alpha_1 at the third resonance is
UNMEASURED and the two-point trend has no third point holding it up.**

**H5 THE DSS RE-ASK — THE LEG'S MOST INTERESTING NEGATIVE.** §26 shut the DSS lane with a
MECHANISM: the non-symmetry spectrum is CONTINUOUS, and a continuum has no eigenvalue to move.
**Dissipation removes that mechanism.** Converged eigenvalues go **2 -> 8** as mu runs 0 -> 4 and
condense onto a ladder of NEGATIVE INTEGERS ([-1,0] at mu=0; [-7,...,-2,0] at mu=4).
**And the lane stays shut anyway, on better evidence:** everything that condenses lands on the
negative real axis, max Re = **+3.3e-13** (i.e. zero), and nothing is complex — the pair flagged
at mu = 2 sits at Re = -3 split by **|Im| = 1.8e-5**, a degenerate real pair resolved to noise.
**The boolean "any complex?" read TRUE for that pair**, so the driver now reports the largest
|Im| instead. The one mode that moves is the amplitude mode, at **-sqrt(1+4mu) to 2.1e-9** —
EMPIRICAL, not derived — and it moves LEFT: more stable, not less. Positive control (lesson 47):
planting a localized potential takes the same filter 6 -> 9 converged with one at **Re = +1.58**.

**H7 CROSS-CHECK THROUGH UNRELATED MACHINERY** (periodic pseudo-spectral, RK4, fitted T — nothing
about the compactified steady solve enters it): at s = 1/2 exactly the prediction is p = 0 and
the measurement (n = 8192) is **p = +0.006, spread 0.007 across nu**, with a within-nu window
spread of ~0.04 that is LARGER than the deviation from zero — so the window is the honest error bar.
**Caveat stated, not buried: every run ends `under_resolved`**; the solver refuses to integrate
past its tail criterion (lesson 45), so each trajectory stops short of T. What softens it is the `reached`
column, recorded for exactly this reason: **each run gets to 99.97% of the fitted singular
time** before refusing.

**H6 THE VERDICT, WITH THE TIME SCALE.** alpha_1 > 0 means mu decays **ALGEBRAICALLY**,
mu ~ 1/(alpha_1 tau), because the linear term is gone. At alpha_1 = 0.1337, mu: 0.2 -> 0.02 costs
tau = 337 and -> 0.002 costs tau = 3703 — **nine times per decade, forever**, and tau is itself
logarithmic in (T-t). Criticality is not a barrier, it is a tar pit.

**NOVELTY: UNCHECKED, AND PROBABLY THIN.** (E) is at HIGH risk — explicit viscous CLM solutions
by complexification go back to Schochet (CPAM 1986), and the dissipative-gCLM relevance exponent
is reported in arXiv:1908.09385 / arXiv:2207.07548, which already puts Route-F at risk;
lambda_mu = 2s - alpha_0 is the same statement in spectral clothing and inherits that risk in
full. The three METHODOLOGICAL candidates — mu as an autonomous coordinate, alpha_1 as the
marginal invariant, and H5's discretization-without-crossing — remain unchecked. See
LITERATURE_CHECK.md.

**LESSONS BANKED.** (56) **A fitted chord is not a derivative** — extrapolate the secants, and
say by how much the chord was wrong. (57) **"Did it converge?" is the wrong refusal predicate for
a derivative; "is the signal above the solve error?" is the right one** — and the wrong one
would have shipped a sign flip. (58) **Report a magnitude, not a boolean, for anything you are
claiming the absence of** — "any complex eigenvalues?" answered TRUE for a pair split by 1.8e-5.
(59) **A structural coincidence that makes an operator FINITE does not make it ACCURATE**;
price the composite, not the ingredient. (60) **Check the monotonicity of your own headline IN
WORDS, as a test.** "alpha_1 > 0 ⇒ mu DECAYS" is the opposite of the reflex reading ("more
dissipation, more dissipation"); `marginal_verdict` returns a sentence and gate 6 asserts which
sentence, so a dropped sign fails a test instead of shipping.

HONEST CEILING unchanged: plain float64, nothing interval-enclosed, nothing rigorous, no link of
the chain moved, s = 3/2 is HYPERviscosity, and (E) decays like 1/x so it is NOT finite energy —
the toy analogue of the class that ESCAPES Necas-Ruzicka-Sverak, not a counterexample to it.
Clay odds ~0.05%.


## §30 — ROUTE-I v1 DONE (2026-08-03): THE MARGINAL FLOW DRIVEN. THE STABILITY INVERSION —
## the INVISCID self-similar point has ~K unstable directions and ANY mu>0 has NONE; and the
## unstable directions ARE Route-E's log-periodic band, i.e. mu DELETES the DSS-shaped modes.

solver/marginal_flow.py + test_marginal_flow.py **11/11**; experiments/p2_route_i_v1_driven.py
→ writeup/data/p2_route_i_v1_driven.json → **fig38**. BLOG/TECHNICAL_P2_ROUTEI_V1.md.
Deterministic, NOT a logged Tier run (~5 min). **It moves NO link of the chain.**

**WHY THIS LEG.** §29 wrote the augmented flow and read it STATICALLY (Newton at frozen mu,
alpha off the branch, dynamics INFERRED). Two numbers came out that way and NEITHER was ever
integrated. This integrates (F_mu)+(M) as an initial-value problem, which also answers the
piece of ranked item (2) §27/§28 left open: **the scaling says which term dominates GIVEN the
self-similar form — does a viscous solution actually REACH it?**

**THE HEADLINE, AND IT WAS FOUND ON THE WAY.** At a=1/2 the INVISCID rescaled fixed point has
**45/48, 93/96, 141/144 unstable directions (max Re +4.52/+4.55/+4.56)** — §26's essential
spectrum seen as a COUNT. Nothing generic reaches a fixed point with a 141-dimensional
unstable manifold. **Any mu>0 removes ALL of it**: the spectrum collapses to a discrete
negative ladder (0, ~-1, ~-4.7) whose gap is flat in mu across four decades.

**THE ARTIFACT TEST IS THE CROSSOVER'S K-SCALING.** Dissipation beats growth rate g once
mu K^p >~ g, so mu*(K) ~ g/K^p should FALL under refinement — an artifact would have mu* flat
or rising. Measured [1e-5,1e-4] at K=48, [1e-6,1e-5] at K=96 and K=144. **HONESTY ABOUT WHAT
THAT RESOLVES:** the mu-ladder is DECADE-SPACED. 48→96 moves a full decade (x10 vs (C)'s x8)
and carries the claim; 96→144 predicts only **x3, BELOW the ladder's resolution**, and duly
does not move (x1.0) — consistent with (C) but **NOT independent evidence for it**. A finer
mu ladder is the obvious next spend if this ever has to carry weight.

**WHERE THE INSTABILITY LIVES — the part worth keeping.** The leading inviscid eigenvalue is
**+4.5455 + 430.35i**, and max Re RISES with |Im| (+0.31/+0.72/+1.00/+2.25/+3.37/+4.55 at
|Im|<=2/5/10/30/100/all, K=96), with max|Im| growing with K (430 at 96, 661 at 144). Those are
Route-E's log-periodic continuum modes — **exactly what a DSS solution is built out of. So the
fastest-growing inviscid directions ARE the DSS-shaped ones, and mu DELETES them rather than
damping them** (at mu=0.05 the whole band is gone, max Re +2.6e-6). **Third independent reason
the cheap DSS entrances do not work**, and sharper than §26's ("a continuum has no eigenvalue
to move") or §29's ("dissipation discretizes it, and nothing crosses").

**THE TWO CROSS-CHECKS PASS.** (i) **lambda_mu = 2s - alpha_0 as a GROWTH RATE**: predicted
-2/-1/0/+1 measured **-2.00141/-1.00042/-0.00026/+1.00030**; line slope **+2.0011** (pred +2),
zero at **s=1.50009** (pred 1.5), worst kept |err| 1.4e-3. Different grid, basis, formulation
and fitted quantity from §27's. (ii) **alpha_1 dynamic vs static at MATCHED K**: 0.13236/0.13277
(0.31%), 0.13330/0.13347 (0.13%), 0.13349/0.13363 (0.10%) at K=96/144/192 — **converging TOWARD
each other**. Adiabaticity measured not assumed: distance to the frozen-mu branch **1.2e-4 →
1.6e-6** over tau=0..600.

**REFUSALS CARRY THIS LEG — FOUR OF THEM.** (1) **p=5 refused on the OPERATOR** (Lambda^p
truncation **1.77**) even though its number, +2.00699, is the CLOSEST agreement in the table.
**Gate the operator, not the agreement** — Route-H's H4 recurring. (2) **ALL THREE a=0.3 rungs
refused on the PROFILE** (seed residual 6e-4..4e-3 vs 1e-9..1e-8 at the resonance), so **THIS
LEG HAS NO OFF-RESONANCE CONTROL** and the law is confirmed at ONE a; p=3 there returns -3.39
against a predicted +1.38. (3) a rate fit returning **+11.79 vs +4.62** because mu left the
linear regime by tau=1.2 — bound the fit by the VARIABLE, not the TIME. (4) in the nonlinear
control, **mu=0 and mu=1e-3 quoted as NOT ASYMPTOTIC** (fit residual **1.49/2.32** against
**0.007/0.012** for the clean rows) rather than averaged in; the clean rows reproduce the
spectral gap to **0.3% and 0.0%**.

**TWO FAILURES FOUND WHILE FINISHING THE LEG, WRITTEN UP RATHER THAN PATCHED AWAY.**
(a) **EVERY off-branch run NaN'd, and the NaN reached a PUBLISHED FIGURE LEGEND** reading
`alpha_1 = nan`, three times, in a panel that had already been looked at. `_implicit_step` has
a stagnation stop that RETURNS the unconverged iterate; nothing checked. Finiteness alone is
NOT the fix either — with a partial repair the same run stayed finite and ended at
**mu = -1.6e24**. The working discriminator is the implicit solve's own residual over its
floor (**~6e2 healthy, 1e13 failed**), and `integrate` now reports `converged` from it.
(b) **THE CAUSE: "small" in the wrong norm.** The perturbation was scaled to max|v_k| = 1 —
small in COEFFICIENTS. But the gauge (N') carries b -> (Lambda^p Om)_X(0), and Lambda^p weights
mode k by ~k^p with one more power from d/dX at the origin, so **|lam.v|/|lam.b| = 3.6e8**:
eps=1e-3 was a **3.6e5 RELATIVE** perturbation of the quantity the flow DIVIDES BY. alpha came
back **11713 instead of 3.037 AT tau=0**, before a single step. Same k^p amplification as
Route-H's H4 — one mechanism, two legs, two symptoms.
**AND THE FIX PRODUCED AN AWKWARD SENTENCE THAT IS KEPT:** normalized in the binding
functional, eps=0.05 is a **5e-11 relative change in the PROFILE**. So the off-branch test is a
strong test of the GAUGE-SENSITIVE direction and a **WEAK test of profile-scale robustness —
it is NOT a basin measurement** and must not be cited as one. I7's twin trajectories are the
profile-scale test. A separate Jacobian bug was fixed on the way (the gauge projection was not
differentiated, on the true-on-branch/false-off-branch grounds that it "is analytically the
zero map"); it changes no on-branch number, verified against all 10 pre-existing gates.

**LESSONS BANKED (61)-(66).** (61) a number read off a trajectory needs a REGIME bound, not
just a fit window. (62) difference against a TWIN trajectory to measure a perturbation off an
inexact fixed point. (63) when a truncated operator becomes stable under a perturbation, the
crossover's K-SCALING is the artifact test. (64) the dominant systematic CHANGES between legs
— here the window contributes 2e-5 and K contributes 1e-3, the reverse of §27. (65) **a refused
computation must be refused in the DATA STRUCTURE, not just the prose** — and finiteness is not
the predicate. (66) **"small" is meaningless until you say IN WHICH NORM, and the binding norm
is set by the OPERATOR, not the coefficient vector** — then report BOTH, because the corrected
perturbation may mean less than the original appeared to.

HONEST CEILING unchanged: plain float64, nothing interval-enclosed, nothing rigorous, no link
of the chain moved, s=3/2 is HYPERviscosity. **"Linearly attracting in this norm at this
truncation" is NOT "an attractor"** — the continuum operator's essential spectrum for mu>0 is
not computed here. Clay odds ~0.05%.


## §A — ADVECTION SCOPE (scoping note, no figure): the eleven-leg bound programme is a=0-ONLY.

Not a numbered Route-D leg — a scoping check that belongs with them. solver/advection_scope.py
+ test_advection_scope.py 6/6. TECHNICAL/BLOG_P2_ADVECTION_SCOPE.md. Plain float64.

**THE QUESTION NOBODY ASKED FOR ELEVEN LEGS.** Every Route-D leg worked at the a=0 anchor,
because that is where the known-answer gate lives — and a=0 is EXACTLY the value at which the
advection term −a U Ω_X is ABSENT. The space was chosen, tuned, priced and optimised on the one
member of the family where the term it must carry does not exist.

  A1 **U IS LOG-DIVERGENT.** v3 §S6's far-field law H(Ω)→(∫Ω)/(πX) integrates to
     U(X)→(M/π)log X, M=∫Ω. No cancellation available: M≠0 for every profile in the family (the
     anchor itself has ∫−1/(1+X²)=−π). Measured vs independently integrated windowed mass:
     −0.9970/−0.9969, −0.7544/−0.7540, −0.6862/−0.6870 at a=0/0.3/0.5. **SUBTLETY: dU/dlogX =
     X·H(Ω) is an IDENTITY; the content is that it tends to M/π, so the predictor is the mass over
     the FIT WINDOW, not the truncated domain — the coarse outermost decade moves the full-domain
     mass 15% at a=0.5 while the windowed one agrees to 0.3%.**
  A2 **THE OPERATOR LEAVES THE SPACE.** In the two-scale codomain (grading α+1): the stretch piece
     (VHh)Ω_X ~ X^{α−2}log X DECAYS for α<2 (harmless); the transport piece U h_X ~
     (a|M|α/π)log X DIVERGES for every a≠0. Measured +0.317 vs predicted +0.318 at a=0.3.
     **⇒ DF does not map domain→codomain for any a≠0, and Y₀ is infinite there too.**
  A3 **WHICH HALF IS REAL — reproducibility, NOT magnitude.** The stretch piece carries Ω_X, whose
     far field for a≠0 is at the noise floor. Grid-spread: transport 0.4%/2.6% vs stretch
     **5%/99%**. Only the reproducible half is quoted, and the gate enforces it.
  A4 **THE FIX IS A GRADING THE PROJECT ALREADY HAS.** The ONE-scale residual balances against
     c_l X Ω_X ~ X^{−α}, so its codomain grading is α — one power WEAKER, exactly what the log
     needs (X^α·(log X)X^{−α−1}=(log X)/X→0). Same profile/h/grid: rate +0.317→−0.010 and
     +0.480→−0.016; at X=1e4, 3.11→3.1e-4 and 4.79→4.8e-4. **So: not "a≠0 is out of reach" but
     "a≠0 needs the ONE-SCALE formulation".**
  A5 **THE CROSSING, AND BEING WRONG ABOUT IT USEFULLY.** c+aU changes sign at X*=7.16 (a=0.3) /
     3.10 (a=0.5), ~1% stable over three grids, none at a=0. Written here first as a STAGNATION
     POINT; v12/v13's solver/finite_support.py reads it better as the **EDGE OF SUPPORT X_c**
     (profile identically zero beyond, algebraic zero of order 1/a) — and that reading explains
     what mine did not: the profile collapses to ~1e-9 by X~10 while X*=7.16, i.e. there is no
     tail out there, only dust past the end. Gates depend only on the reproducible half, so they
     survive the reinterpretation.

CLAY: moves NO link of the chain. It narrows an L1 sub-programme and names the repair — a COST
finding, whose value is that it landed before three more bound-sharpening legs were built on the
assumption that the space works.


## §B — ROUTE-G OPS: the orphaned G2, and G2 at 2.6x (no science content, but do not relearn it)

**THE LOSS AND THE RECOVERY.** G2 had been run to its own `--out` file so it could go in
parallel with G3/G4 — that worked — but **nothing ever merged it back**, and
p2_route_g_v1_evidence.py reads only the main artifact. A 55-minute stage sat in a sibling
file while fig36 silently skipped its panel B. Shared stages were byte-identical, so the
merge was safe and **no re-run was needed**. Fixed: `--merge` folds siblings in and REFUSES
when a stage exists in both and differs, so a `--quick` run cannot overwrite a real one.
**GENERAL FORM: a mechanism that SPLITS work needs the one that PUTS IT BACK, or the split
silently becomes a loss.**

**G2 IS NOW ~16 MIN, NOT ~41, AND MOVES NO NUMBER.** (i) the steps ladder is a PREFIX
ladder → one chained trajectory read at each rung, 8100 steps → 4000 (867s → 398s); valid
because renorm=True re-pins the same frozen origin slopes on resumption and dt is
state-derived each step — **verified at 1.3e-14, not assumed**. (ii) the resolution ladder
is embarrassingly parallel and each relaxation is SINGLE-threaded (measured 101% CPU), so
four rungs cost the longest not the sum (1619s → 543s); results reassemble in LADDER order,
not completion order. Verified vs the committed artifact: **89 numeric fields, worst
3.1e-12**, that only in two residuals from accumulation order; beta_mean identical to 12
digits. `test_route_g_perf.py` 4/4. `ROUTE_G_SERIAL=1` forces serial; `ROUTE_G_DATA`
redirects the merge gate at a temp dir so the test cannot clobber writeup/data.
**THIS BOX HAS 4 CORES, NOT 8 — `OMP_NUM_THREADS=8` is pinned project-wide and misleads.**


## §31 — ROUTE-J v1 DONE (2026-08-04): THE PRIMARY-SOURCE PASS. EGRESS OPENED AFTER SIX
## LEGS; ALL 14 PAPERS PULLED; TIER 1 READ. SEVEN STANDING CLAIMS PRE-EMPTED, ONE PARTIAL,
## TWO STILL UNSEARCHED — AND ONE RESULT ARRIVES *FROM* THE LITERATURE.

solver/literature_gates.py + test_literature_gates.py **9/9**;
experiments/p2_route_j_v1_literature.py → writeup/data/p2_route_j_v1_literature.json →
**fig39**. BLOG/TECHNICAL_P2_ROUTEJ_V1.md. LITERATURE_CHECK.md **sixth pass**.
Deterministic (~5 s). **It moves NO link of the chain. NO new science.**

**WHY THIS LEG, AND WHY IT IS CODE AND NOT PROSE.** Five literature passes were written
while `Papers/` stayed empty. This session `curl https://arxiv.org/abs/2207.07548` returned
**200** for the first time and `bash Papers/fetch.sh` pulled **14/14 on the first attempt**.
The deliverable is deliberately NOT a paragraph saying "we checked" — that decays exactly
the way five search-level passes decayed. It is a module of **executable gates**: each one
re-derives a published number from the published equations and compares it to ours.

**THE EXPONENT DICTIONARY GOES FIRST, and it is gate 1 for a reason.** ALS/XU write
`omega ~ tau^{-beta} f(x/tau^{c_l})`, so **their c_l is our beta** and **our alpha = 1/c_l**;
their `Lambda^sigma` is our `(-Delta)^s` with **sigma = 2s**. Hence `s_c(ours) = s*(XU)/2`.
**Get this wrong and every verdict in the leg inverts while still passing its own test.**

**(J-1) ROUTE-F's HEADLINE IS PRE-EMPTED, AND NOT BY THE PAPER THE FIFTH PASS NAMED.** The
fifth pass called arXiv:2207.07548 "the paper most likely to pre-empt Route-F" and said to
read it first. **Wrong.** ALS §8 explicitly leaves the critical-sigma question OPEN
("whether sigma = 1 is the optimal lower bound ... left for future work"). The relation is
**arXiv:2607.19762 §6.1 eq (6.3), s*(a) = 1/c_l(a)** (Xu), from the same rescaling argument,
**posted 22 Jul 2026 — ELEVEN DAYS before Route-F v1**. Our F6 map vs their Table 1: worst
row **3.1e-3**, mean **1.2e-3**, exact at a=0 and a=1/2. What survives is narrow and should
be said narrowly: **F3's cross-check** (steady compactified solve vs time-dependent periodic
simulation, no shared grid/basis/constant) is an independent dynamical validation of THEIR
formula — Xu state their branch's only quantitative validation is the a_c endpoint. **A
service, not a result.**

**(J-2) ROUTE-H's (E) IS ALS §5.3 eqs (57)-(58), VERIFIED.** Parameter map
`omega_{-1}(0) = -(1+mu_0) kappa`, `v_c(0) = kappa T`, `kappa = nu/mu_0`. Worst relative
difference **6.5e-15** over 3 parameter sets x 4 times; ALS's blow-up-time formula (59)
returns our T with absolute error **0.0**; their evolution law `dv_c/dt = omega_{-1}(0)+nu`
reduces to `-kappa`, which is (E)'s own. Route-H declined to claim it — right call, now
settled. **alpha_1 = 0 at a=0 is likewise confirmed-and-known**: ALS's form (61) carries nu
INSIDE the profile at fixed exponents, i.e. the line of viscous self-similar blow-ups we
measured. **alpha_1 = +0.133683 at a=1/2 is NOT in Tier 1** (criticality there is sigma=3,
in neither paper) — but it is UNSEARCHED, not novel.

**(J-3) alpha(1/2) = 3 IS EXACT AND KNOWN — AND IT CLOSES §26's OWN OPEN QUESTION.**
Integrating ALS (49)-(50) cold (no shared grid, basis or code): **c_l = 0.3333076 vs 1/3,
rel 7.7e-5**, with **Omega ~ v_c^{-2.000144}** vs the exact -2. §26 recorded that "what stays
UNEXPLAINED is why alpha=3 lands on a round rational while alpha=5 does not". **ALS §1
answers it: exact pole-dynamics solutions exist at a=0 and a=1/2 and, per Lushnikov et al.,
NOWHERE ELSE.** The alpha=5 point at a=0.5821792673 is a property of **our instrument**
(Lambda^5 is a finite matrix there), not of the problem.

**(J-4) THE RE-CLASSIFICATION WITH THE LARGEST FORWARD CONSEQUENCE — XU PROPOSITION 2, THE
REALIZATION DICHOTOMY. READ THIS ONE BEFORE TOUCHING ROUTE-I.** The essential-spectrum
continuum §26 measured is the faithful spectrum of the **maximal L^2 realization**; on the
**origin-H^2** realization the open strip is empty apart from {0,1}, the whole non-symmetry
family being `u_lambda(y) = y^{1-lambda}/(y+i/2)^2` — L^2 but with `u'' not in L^2` at the
origin. Xu say in as many words that the smear grids **WITHOUT AN ORIGIN CONDITION** place
inside the strip is that realization's spectrum. **OUR DISCRETIZATION HAS NO ORIGIN
CONDITION.** So "the non-symmetry spectrum is CONTINUOUS" is a statement about which
operator we discretized, not about the operator. The DSS verdict survives (nothing to
bifurcate in either realization, so the lane stays shut on better evidence) — **but §30's
"141 of 144 unstable directions at mu=0" is counted in the loose realization and MUST SAY
SO. Re-running I5 with an origin condition is the top-ranked correction item.** Note what
it does NOT touch: the mu>0 half of the inversion is about a DISCRETE negative ladder, and
a discrete ladder is not realization-smear.

**(J-5) THE ONE RESULT ARRIVING FROM THE LITERATURE: WHAT LIES ABOVE s_c.** §27/§29/§30 all
stop at criticality; Route-F's sentence "the scaling says which term dominates" had no
second half. ALS §5.1 (Schochet, corrected) has it. Term by term with
`omega ~ tau^{-beta} f(x/tau^{c_l})`: `omega_t ~ tau^{-beta-1}`, `omega H omega ~
tau^{-2beta}`, `nu Lambda^sigma omega ~ tau^{-beta - sigma c_l}`. **SUBcritically omega_t
balances stretching, forcing beta=1. SUPERcritically DISSIPATION balances stretching,
beta = sigma c_l, and omega_t is SUBDOMINANT.** Schochet is the witness (sigma=2, c_l=1 =>
beta=2, matching ALS (45)). **MEASURED, not quoted:** spread of `tau^beta omega` across a
tau-ladder is **0.0202 at beta=2 vs 0.990 at beta=1 (49x)**, and — the check that makes it a
measurement rather than a four-way fit — the beta=2 residual **FALLS 0.0202 -> 0.0060 ->
0.00187** on deeper sub-ladders, which is ALS's stated O(tau^{-1}) correction behaving as
stated. **THE MECHANISM IS THE PART TO CARRY: the tau^{-2} is carried by a DOUBLE POLE with
residue B = -12 i nu — proportional to nu, hence ABSENT inviscidly. Above criticality the
blow-up is not the inviscid one surviving viscosity; it is a DIFFERENT singularity that
viscosity itself creates.** No leg of this project could have seen that: all three are built
on beta=1.

**(J-6) A 38-YEAR-OLD TYPO, SETTLED FROM OUR SIDE.** ALS §5.1 correct Schochet (CPAM 1986)'s
constant to `K± = 24(3±sqrt6)` from the printed `12(6±sqrt6)`. Substituting both into the
complex Burgers equation with ANALYTIC derivatives (no differencing): corrected **5.24e-16 /
2.85e-16**, printed **2.40e-2 / 8.36e-2** — **13.66 decades**. ALS are right. Schochet CPAM
1986 is still unobtainable (publisher PDF) but its content is now pinned through ALS, **and
the constant one would have copied from it is the wrong one.**

**(J-7) FINITE SUPPORT IS PARTIAL, NOT PRE-EMPTED.** HTW (arXiv:2209.08232) Prop 2.3 proves
compact support for the **De Gregorio model, a=1**, where non-degeneracy forces c_l = c_omega
— same mechanism as ours (profile locally proportional to u + c_omega x; support ends where
that vanishes). **NOT in HTW:** the a-dependence across a in (0,1/2), the algebraic order 1/a
of the zero, and the certification-space consequence we actually used it for.

**(J-8) ON a_c WE ARE THE WORST OF THREE SOURCES.** Published (LSS) **0.6890665**; Xu's
recompute **0.6888 (0.04%)**; ours **0.693493 (0.64%)**. Quote theirs. There is a gate
asserting exactly this, which FAILS if we ever become the better source — at which point the
right response is to say so, not delete the gate.

**NEW BANKED LESSONS (67)-(70).**
**(67) GATE THE QUANTITY THE MEASUREMENT DIVIDES BY, not the quantity it is about.** J3's
first refusal predicate was `tau > 1e3 eps max|S|`. It passed and read **c_l = 0.222** at its
deepest "resolved" rung while reading 0.33333 in the middle. The local exponent is a
DIFFERENCE QUOTIENT, so what must survive is **d tau**, not tau — and tau at the bad rungs is
1e-11, enormous against underflow, so **no threshold on tau could ever have caught it**. This
is lesson (57) one level down.
**(68) A LITERATURE CHECK THAT IS NOT EXECUTABLE DECAYS AT THE RATE OF MEMORY.** Five prose
passes produced zero durable facts; nine gates produced twelve durable verdicts in 5 s of
runtime. If a claim is worth checking against a paper it is worth checking IN CODE.
**(69) WHEN A PAPER PRE-EMPTS YOU, THE VALUABLE PART IS USUALLY THE PART YOU DID NOT ASK
ABOUT.** Reading ALS to check s_c returned nothing about s_c and everything about what lies
above it — the one inbound result of the pass. The claim under audit was the least
informative thing in the paper.
**(70) A SPECTRUM IS NOT A PROPERTY OF AN OPERATOR UNTIL YOU NAME THE REALIZATION.** §26 and
§30 both measured "the" spectrum of a discretization with no origin condition and reported it
as the operator's. Xu's Prop 2 shows that choice moves a whole continuum in and out. **Before
reporting any spectrum, state the domain condition at the singular point.**

**WHAT THIS DOES NOT CHANGE:** any number in any committed artifact. Nothing was found to be
WRONG. What changed is who found it first.

**STILL UNSEARCHED AT PRIMARY SOURCE, and it is the part that matters:** Tier 2
(2302.12877, 2312.01702, 1908.09385) is fetched and text-extracted but NOT read closely.
Those gate the **Route-D methodological claims — still the only claims in this project with a
real chance of being new.** After this pass "unchecked" means unchecked, not "probably fine".


## §32 — ROUTE-K v1 DONE (2026-08-04): THE L1->L2 CERTIFICATION PORT, STEP ONE. THE
## KILL-SWITCH FIRES AT Y_0: THERE IS NO FIXED PROFILE TO TAKE A DEFECT OF, AND NO
## APPROXIMATE INVERSE TO BOUND. RANKED ITEM (3), DEFERRED SIX TIMES, ATTEMPTED.

solver/port_certification.py + test_port_certification.py **6/6**;
experiments/p2_route_k_v1_port.py → writeup/data/p2_route_k_v1_port.json → **fig40**.
BLOG/TECHNICAL_P2_ROUTEK_V1.md. Deterministic (~9 min). **It moves NO link of the chain --
and a BLOCKED link is not a moved link.**

**THE CHAIN AND WHERE IT BREAKS.** A radii-polynomial argument needs (i) a fixed profile x*
with F(x*)=0; (ii) Y_0 >= ||A F(x*)||; (iii) A ~ DF^{-1} with Z_1 = ||I - A DF|| < 1;
(iv) the quadratic having a root. **(i) BLOCKED, (ii) UNDEFINED, (iii) NO A, (iv) not
reached.** `radii_polynomial_status(None, None)` returns BLOCKED_AT_STEP_ONE and is GATED to
carry **no fabricated Y_0 or Z_1** -- substituting a plausible bound would turn "there is
nothing to bound" into "the bound is too big", which is weaker and false.

**(K-1) THE RELAXATION HAS NO FIXED POINT. IT LIMIT-CYCLES.** n_r=200, n_b=48, r_max=1e5:
||F||_inf = **0.9757 -> 0.2060 -> 0.0257 -> 0.2290** at 500/1500/3000/5000 steps, i.e. down
38x then UP 9x, with c_omega swinging **-1.0145 to -1.2444** and c_l/c_omega swinging
**-3.017 to -2.459**, STRADDLING the published -2.9206 without settling on it. 3000 steps is
where every previous run stopped, and it is the bottom of a cycle, not a fixed point.

**(K-2) AND IT DIVERGES UNDER REFINEMENT -- IN OUR OWN COMMITTED DATA, TWO LEGS OLD.**
Route-G's resolution ladder (writeup/data/p2_route_g_v1_g2.json, r_max=1e5): steady residual
**1.671e-2 -> 7.708e-2 -> 2.667e-1** at n_r = 300/450/600. **Refining 2x makes the residual
16x WORSE.** That column has been in the repository for two legs and nobody asked which way
it was going.

**(K-3) THE UNCOMFORTABLE PAIRING, AND THE LESSON IN IT: c_omega DOES NOT NOTICE.** Across
that same ladder c_omega holds to **0.77%**. The modulation (2.11) is a LOCAL read at the
origin and the residual that grows lives elsewhere, so the read stays stable while the object
falls apart. **"Resolution-stable" is not "converged".** Consequence Route-G must carry:
its **beta = 2.98 +- 0.02 against the published 2.9206 is 2.1% out -- 2.5 spread-widths --
and that gap now has a cause.** Correction banner added to TECHNICAL_P2_ROUTEG_V1.md.

**(K-4) WHERE THE DEFECT LIVES: THE WALL.** Argmax of each field's residual tracked in
(r, beta) across the ladder. Early transients sit mid-domain (r~1e2) and at the outer Robin
edge (r~7e4); once they clear, **all three fields put their max at beta = 0.032, the first
interior angular node -- the WALL** -- at moderate r (2-14). Not the corner, not the far
field. That is where Chen-Hou needed a weighted L^inf + C^{1/2} pairing.

**(K-5) DF HAS NO COMPUTABLE APPROXIMATE INVERSE, AND THE LADDER IS FLAT.** Matrix-free
Krylov on DF x = -F, reported as a LADDER in the Krylov dimension because the SHAPE is the
measurement. At the best point of the cycle: **0.6946 / 0.6927 / 0.6908 / 0.6853 / 0.6623**
at m = 10/20/40/80/160. **16x the work buys 5%.** A merely ill-conditioned operator BENDS
DOWN once GMRES captures the extreme eigenvalues -- the planted cond~1e8 control reaches
**0.086**. Flat in the Krylov dimension is the signature of a **CONTINUUM in the spectrum**,
which is Route-E's essential spectrum again and is exactly what §31's lesson (70) says to
name the realization of: **our log-polar grid imposes no condition at the singular corner.**

**(K-6) THE INSTRUMENT IS GATED FIRST, because "the solve stalled" is what a broken solver
says.** Our GMRES: **7.6e-11 in 19 iterations** on a well-conditioned dense system, reported
residual agreeing with the true one; **0.086 after 200** on a planted cond~1e8 system (the
yardstick). The finite-difference Jv: **||Jv|| = 65.140, spread 3.5e-6 across h/||z|| =
1e-4..1e-9**, best inter-rung drift **6.3e-8**. Neither is the noise floor.

**(K-7) THE ONE PRINCIPLED REPAIR, TRIED: IT HALVES THE STALL AND DOES NOT REMOVE IT.** At
large r the transport speed s_rho -> c_l, so the leading operator is -c_l d_rho + (diagonal
damping); upwinded outward it is **LOWER BIDIAGONAL per angular line, exactly invertible in
O(N)** (gated: apply it to its own solve, recover the rhs to **3.9e-16**). Same split
Chen-Hou describe in their own abstract. **0.6623 -> 0.3596 (1.84x) at the best seed, and
the curve stays FLAT.** So the dilation continuum is a real, IDENTIFIED, removable part of
the obstruction -- and a SECOND obstruction of comparable size remains. Candidates: the
nonlocal Biot-Savart velocity, and the wall (where K-4 puts the defect).

**(K-8) THE SEED-DEPENDENCE IS THE SHARPEST FORM OF THE FINDING.** Everything above is "at
the best point of the cycle" and had to be. At the WORST point (||F||_2 = 11.11 vs 0.807) the
unpreconditioned stall reads **0.2450 not 0.6623 (a 2.7x spread)** and the preconditioner
buys **1.03x not 1.84x**. Neither is THE answer. **Z_1 here is not large and is not small;
it is not about anything.** Quoting one stall level was the natural way to write the section
and would have hidden exactly the fact that makes it decisive.

**NEW BANKED LESSONS (71)-(73).**
**(71) "RESOLUTION-STABLE" IS NOT "CONVERGED", AND A LOCAL READ CAN BE STABLE ON AN OBJECT
THAT IS DIVERGING.** Route-G's c_omega holds to 0.77% across a ladder whose residual grows
16x. **Check the residual column's DIRECTION, not just its size** -- and check it on the
ladder you already committed, which is where this one was hiding for two legs.
**(72) REPORT THE SHAPE OF A CONVERGENCE LADDER, NOT ITS ENDPOINT.** "GMRES got to 0.66" is
compatible with both "hard but tractable" and "impossible"; **0.6946 at m=10 and 0.6623 at
m=160** distinguishes them, because flat means continuum and bending means conditioning.
Pair it with a PLANTED ill-conditioned control so "flat" has a yardstick.
**(73) WHEN A QUANTITY HAS NO REFERENT, SAY SO INSTEAD OF BOUNDING IT.** Y_0 here is not
large, it is undefined; Z_1 is not large, it is seed-dependent by 2.7x. The code path that
would have produced a number was deliberately not written, and the kill-switch is gated to
refuse it.

**WHAT MUST BE BUILT NEXT, IN ORDER, AND EACH IS A LEG:** (1) a preconditioner that also
covers the nonlocal Biot-Savart velocity and the wall -- Chen-Hou's finite-rank correction is
the model and Papers/2210.07191.pdf sec.7 is the section; (2) a profile from a CONVERGED
Newton solve, which is DOWNSTREAM of (1) (a prototype JFNK reduced ||F||_2 from 0.807 to
0.549 in fifteen Newton steps and then flatlined, with the linear solve returning relative
residual 1.00); (3) only then the function space, Y_0 in it, and Z_1.


## §33 — ROUTE-L v1 DONE (2026-08-04): THE 2D PRECONDITIONER. BOTH OF §32's NAMED SUSPECTS
## ARE CLEARED BY ABLATION, THE REAL TERM IS THE ANGULAR TRANSPORT, AND AN O(N) EXACT SWEEP
## TAKES THE KRYLOV STALL 0.6623 (FLAT) -> 3.3e-6. STEP (iii) IS UNBLOCKED.

solver/port_certification.py (Route-L additions) + test_port_certification.py **10/10**;
experiments/p2_route_l_v1_precond.py → writeup/data/p2_route_l_v1_precond.json → **fig41**.
BLOG/TECHNICAL_P2_ROUTEL_V1.md. Deterministic (~13 min). **No link of the L1->L4 chain
moved** -- one rung of the SCAFFOLDING opened, which is not the same thing.

**(L-1) BOTH OF §32's CANDIDATES ARE WRONG, AND THE ABLATION SAYS SO CLEANLY.** Six
ablations, each with its own Krylov ladder, ranked by GAIN not endpoint (lesson 72). Gate:
the un-ablated variant reproduces solver.rhs to **0.0**.

    pure dilation, no angular   0.7518 -> 0.1608   gain 4.68   BENDS
    angular transport OFF       0.7857 -> 0.3712   gain 2.12   BENDS
    velocity in s_rho OFF       0.6111 -> 0.3599   gain 1.70   flat
    reaction terms OFF          0.7552 -> 0.5817   gain 1.30   flat
    velocity feedback OFF       0.8456 -> 0.7582   gain 1.11   flat, WORSE THAN FULL
    full                        0.6946 -> 0.6623   gain 1.05   flat

**THE NONLOCAL BIOT-SAVART TERM IS NOT THE OBSTRUCTION -- REMOVING IT MAKES THE STALL
WORSE** (0.6623 -> 0.7582). It is mildly HELPING the Krylov solve. It was the first
candidate §32 named.

**(L-2) THE WALL IS NOT IT EITHER, AND THIS ONE IS A DIRECT MEASUREMENT.** Energy of the
STALLED Krylov residual in the first 3 of 48 angular nodes (proportional share **0.0625**):
**omega 0.0685 (1.10x), eta 0.0794 (1.27x), xi 0.2745 (4.39x)**. omega and eta are FLAT
across the domain -- distributed, which is what a continuum looks like and is not what a
boundary layer looks like. **§32 conflated two different defects: the RELAXATION's, which
IS at the wall (§32 K-4, correct), and the LINEAR SOLVE's, which is not.**

**(L-3) IT IS THE ANGULAR TRANSPORT, and the clincher is a combination.** Angular transport
OFF **plus** §32's radial preconditioner runs to **MACHINE ZERO** (0.0401 -> 0.0171 ->
0.0006 -> 0.0 -> 0.0). So the TRANSPORT operator carries the ENTIRE obstruction, in two
pieces, and nothing else in the equation contributes -- not the nonlinearity, not the
nonlocal term, not the reactions, not the wall.

**(L-4) THE WRONG FIX, KEPT BECAUSE IT IS LOAD-BEARING: ADI IS CATASTROPHIC.** Composing an
exact radial solve with an exact angular solve gives **0.9960**, far WORSE than doing
nothing (0.6623). **The operator does not split**, and the splitting error exceeds the thing
being fixed. This is what forces the correct construction rather than merely permitting it.

**(L-5) THE RIGHT FIX FOLLOWS FROM A MEASURED STRUCTURAL FACT.** The radial upwinding is
**OUTWARD EVERYWHERE on this profile -- measured s_rho in [0.390, 5.732]**, strictly
positive, reported as a magnitude so a marginal case would be visible. That makes the
COUPLED transport operator **block lower bidiagonal in the radial index with TRIDIAGONAL
diagonal blocks**:

    [(c - s_rho/drho) I - s_beta d_beta] f_i = rhs_i - (s_rho/drho) f_{i-1}

so **ONE outward Thomas sweep inverts it EXACTLY, O(N), with NO splitting error -- because
there is no split.** Gated: apply the full transport operator to its own sweep, recover the
rhs to **9.5e-16**.

    none                        0.6946 / 0.6908 / 0.6623            flat, gain 1.05
    radial only (§32)           0.4463 / 0.4215 / 0.3593            flat
    ADI composition             0.99999 / 0.99852 / 0.99604         flat, worse than none
    FULL TRANSPORT LINE SWEEP   0.1830 / 0.1313 / 0.0188 ; 2.0e-4 at m=240, 3.3e-6 at m=320

**The same stall classifier, on the same data structure, returns BENDING (gain 9.72).
A IS CONSTRUCTIBLE. STEP (iii) IS UNBLOCKED** -- first time in 44 legs a blocked link opened.

**(L-6) NEWTON STILL FAILS, AND FAILS DIFFERENTLY -- WHICH IS THE FINDING.** The linear
solves now SUCCEED (**GMRES rel 2.5e-3 in 200 iterations, against 1.00 before**) and Newton
still creeps: ||F||_2 **0.8069 -> 0.7378 over eleven steps (factor 1.09)** with the line
search accepting only **lambda = 1/32 then 1/64**. A full step rejected while the linear
algebra is accurate is NOT a spectral problem -- it is a **NEAR-NULL DIRECTION in DF**.

**(L-7) THE OBVIOUS EXPLANATION WAS TESTED AND IS REFUTED. DO NOT RE-TRY IT.** `renorm=True`
re-pins omega_x(0) and eta_x(0) after every relaxation step and F carries no such
constraint, so the SCALING GAUGE was the candidate. Projecting onto it inside Newton makes
things **strictly worse**: at iteration 0 the line search accepts **NO step at all** (lambda
down to 1/1024, still rejected) and ||F||_2 does not move. **The near-null direction is not
the scaling gauge, and it is recorded as UNIDENTIFIED.**

**NEW BANKED LESSONS (74)-(76).**
**(74) TEST ALL THE SUSPECTS AT ONCE; A BATTERY COSTS ABOUT WHAT THE GUESSES COST.** §32
named two candidates and both were wrong -- and they were named because they are the
INTERESTING parts of the equation (nonlocality, the boundary). The culprit was the boring
term that moves material sideways. Building the six-way battery took about as long as
writing the two guesses down.
**(75) TWO DEFECTS IN THE SAME PROBLEM ARE NOT THE SAME DEFECT.** §32 measured the
RELAXATION's residual at the wall and inferred the LINEAR SOLVE's would be there too. It is
not (1.10x proportional vs 4.39x for xi alone). Localize each one separately.
**(76) A NEGATIVE CONSTRUCTION IS WORTH KEEPING IN THE ARTIFACT.** ADI at 0.996 -- worse
than doing nothing -- is what ruled out the whole splitting family and forced the sweep. A
writeup that only reports what worked cannot be used to avoid re-trying what did not.

**WHAT MUST BE BUILT NEXT, IN ORDER:** (1) **IDENTIFY the near-null direction of the
PRECONDITIONED Jacobian** -- cheap now, because M^-1 exists: a few inverse-iteration or
Lanczos steps through M^-1 DF. The gauge is RULED OUT; the live candidates are the
c_l/c_omega modulation's implicit dependence (which makes F an implicitly-defined map, not
an explicit one) and translation along the profile branch. (2) a **BORDERED system** once
(1) names it -- append the constraint that pins the direction, rather than projecting after
the fact, which is exactly what failed in (L-7). (3) only then the profile, the function
space, Y_0 and Z_1.

## §34 — ROUTE-M v1 DONE (2026-08-04): TARGET SELECTION. THE PORT WAS AIMED AT A CERTIFIED
## OBJECT FOR TWENTY LEGS, AND THE UNCERTIFIED ONE'S SOLVER WAS ALREADY IN THE REPOSITORY.

Banked record: `writeup/4_p2_lottery/TECHNICAL_P2_ROUTEM_V1.md` + `BLOG_P2_ROUTEM_V1.md` +
**fig42** (rebuilds from committed `writeup/data/p2_route_m_v1_targets.json` via
`.venv/bin/python writeup/4_p2_lottery/p2_route_m_v1_evidence.py`).
Code: `solver/target_selection.py`, `test_target_selection.py` **9/9**; `capabilities.py`,
`test_capabilities.py` **5/5**; `line_hilbert.slope_matrix` + its gate in
`test_line_hilbert.py`. Harness: `experiments/p2_route_m_v1_targets.py`.

**THE QUESTION, AND WHY NOBODY HAD ASKED IT.** `CLAY_ROADMAP.md` §2 has said since
2026-07-23 that the realistic prize is *a novel Tier-3 result on a model where blow-up is
provable*. The port has been aimed at Chen–Hou's 2D Boussinesq profile since Spike 1.
**Chen–Hou certified that profile themselves** (arXiv:2210.07191 Part I + Part II, rigorous
numerics). Every session had a concrete blocked step in front of it — the relaxation
cycles, the Krylov ladder is flat, Newton creeps — and "should this be the target" was never
in front of anything, so it never got picked up. Route-J (§31) is the same lesson from the
other side: reading the literature to check your ANSWERS is half of it; reading it to check
your QUESTION is the other half.

**(M-1) THE LEDGER. SIX OBJECTS, THREE QUESTIONS EACH, RANKED BY CONTRIBUTION.** Q1 is *is
there a proof of THIS profile* — not "is blow-up known" — and **an analytic proof counts
harder than a computer-assisted one**, because an object proved by hand does not become more
true when a computer re-proves it. Q2 is the unknown count `fields × n^dim + modulation`,
exact arithmetic, ratioed against **the one object where a proof of this kind is known to
have been completed**. Q3 is one sentence a specialist would accept. Ranking is Q3 first, Q2
last, and `test_target_selection.py` **fails if the uncertified ranking is ever in cost
order** — the cheapest object (602 unknowns) is deliberately rank 2.

**(M-2) GATE: YES. THE NAMED TARGET IS `HL_S2_nonsymmetric`.** Chen–Huang–Li
arXiv:2604.01868 §2.5/§4: the **non-symmetric positive regular self-similar profile of the
1D Hou–Luo model**, reported April 2026 as "a previously unreported blowup phenomenon",
numerical only, **1.11e−3 of the certified object's unknown count**. Their limiting
constants `(c_l, c_ω, c_r, c_l/c_ω) ≈ (1.0636, −0.4235, 0.0765, −2.5114)`; Chen–Hou–Huang's
symmetric branch sits at −2.9987, so this is a **different contraction rate, not a
re-parametrization**. Behind it: gCLM one-scale from degenerate data `a>0` (arXiv:2603.25104
§4, with `c_l` changing sign at `a ≈ 0.2329`); the same phenomenon in 2D (§6.2); and the
stability of the singular steady state (their Conjecture 2.4 — blocked on a **function
space**, because the profile is unbounded and only in `L^p` for `p<2`).

**WHY IT IS RANK 1 AND NOT THE CHEAPEST ONE.** In Chen–Huang–Li's own words, in every
existing proof of this kind *"the origin always acts as the source of stability"*. This
profile has **no symmetry point**, so the translation degree of freedom must be carried by
the certificate itself — their (2.9)/(4.1) adds a third modulation constant `c_r` for
exactly that. A first certificate for a profile with nothing anchoring it is a
**methodological** first. It is also the shape leg 44 concluded the port needs: *border the
system, do not project*.

**(M-3) THE EXCLUSION LIST IS THE LOAD-BEARING HALF, AND IT GREW.** Seven objects proved,
**four of them analytically**:
* arXiv:2305.05895 (Huang–Qin–Wang–Wei) proves **the entire smooth gCLM branch for all
  `a ≤ 1`** by hand, with regularity, monotonicity and decay rates — **the branch Routes D,
  E and F spent a dozen legs measuring.**
* arXiv:2308.01528 proves the Hou–Luo odd non-degenerate profile analytically, **after** the
  Chen–Hou–Huang CAP of the same object.
* arXiv:1908.09385 (J. Chen) — checked for computer assistance and there is **none**; it is
  a perturbative analytic argument around the exact `a = 1/2` solution. An exclusion, not a
  CAP precedent.

**(M-4) "WITHIN REACH" IS NOW A NUMBER: the `Y₀` BUDGET.** The radii polynomial
`½Z₂r² − (1−Z₁)r + Y₀ < 0` has a root iff **`Y₀ ≤ (1−Z₁)²/(2Z₂)`**. `Z₁, Z₂` are properties
of the operator and the space; `Y₀` is a property of how well the profile is resolved. Reach
= can the truncation be pushed until `Y₀` falls under that budget. Gated against a
**completed** certificate: Cadiot–Lessard–Nave arXiv:2302.12877 Thm 6.6 publish
`Y₀ ≤ 2.26e−14, r₀ = 2.27e−14`; our algebra returns their `r₀` at **relative error 0.0**,
implied `Z₁ = 4.41e−3`. The boundary is checked by **bracketing** (feasible at `0.999999999×`
budget, infeasible at `1.000000001×`) on four `(Z₁,Z₂)` pairs, because a strict inequality
tested at its own boundary is a coin flip in floating point.

**AND WHAT CLN DOES NOT CLOSE:** they work in **Hilbert/Fourier `H^l` spaces**, not weighted
`ℓ¹`. Route-D's weighted-`ℓ¹` no-go and discrete-ball trap are **narrowed, not closed** —
still UNSEARCHED at primary source, and still the only claims with a real chance of being
new.

**(M-5) THE 3D NAVIER–STOKES CLAIM, AUDITED RATHER THAN ASSUMED (lesson 76).**
arXiv:2604.09949 claims finite-time singularity for 3D NS on `T³` by computer-assisted
Newton–Kantorovich. That is Q1 for the most consequential object on the list, so it was
checked. Its constants `δ = 8.421739e−12, M = 482.6, K = 1.1e4` close `2δMK = 8.9e−5` as
printed; Kantorovich's hypothesis with `β = M, η ≤ Mδ` is `M²Kδ ≤ ½`, i.e. **one factor of
`M` larger**, and `2M²Kδ = 4.3e−2` **also closes**, with 23× margin. Its `K` reproduces from
its own stated factor product to 2.2e−4. **THE ARITHMETIC IS NOT WHERE IT FAILS, and the
audit says so** — a check that reported "fails" here would be reporting the wrong thing.
The two reasons it cannot be used stand on their own and are on the face of the document:
**(i)** no verification package is released (its appendix F: the package "is intended to
contain" its contents; appendix E: source files "expired during the session"); **(ii)** its
Thm 12.1 reconstructs the exactly-**backward** self-similar solution excluded by
Nečas–Růžička–Šverák and Tsai under the decay its own analytic weight implies — and its
reference list cites Jia–Šverák on **forward** self-similar solutions, which exist, and
neither non-existence result. Recorded as `CLAIMED_UNUSABLE`: not certified, not open.

**(M-6) THE MEASUREMENT: IS THE NAMED TARGET REACHABLE ON OUR OWN CODE?**

**⏳ PENDING — THE MEASUREMENT IS STILL RUNNING AS OF THIS COMMIT.**
The refinement ladder for the named target (`experiments/p2_route_m_v1_targets.py`, M3)
is deterministic and in flight; `writeup/data/p2_route_m_v1_targets.json` and **fig42**
land with it, and this section is filled from that JSON and not from memory. **Nothing
above depends on it:** M1 (the ledger), M2 (the budget algebra and the 3D-NS audit) and
the gate verdict are complete and gated by `test_target_selection.py` 9/9. What M3 adds
is the *measured* half of question (2) — whether the object our code converges to holds
up as the grid is refined with the dissipation taken to zero, read as the ladder's
DIRECTION (lesson 72) and paired with the same reading of Route-K's committed 2D ladder,
where it went the other way (`1.671e−2 → 7.708e−2 → 2.667e−1` at `n_r = 300/450/600`:
**2× finer, 16× worse**).

**(M-7) THE SECOND FINDING IS ABOUT US, AND IT IS THE SAME SHAPE AS THE FIRST.**
`solver/hl_rescaled.py::RescaledHLScenario2` — Chen–Huang–Li's three-constant bordered
formulation, gauge gated to **4.4e-16**, contraction ratio reproduced to ~1% — was built on
**2026-07-26** (§8), described in these notes as "the validated brick", and then left. Nine
legs later the port was aimed at a certified object while the solver for an uncertified one
sat unused in the same folder. It was found this leg **by grepping for an arXiv number**.

`plan_of_record.py` answers *what is next*; these notes answer *what happened*; **nothing
answered *what do we have*.** So this leg shipped `capabilities.py`: 35 solver modules, each
with the object it holds, what it computes, **the strongest known-answer gate it passes with
the magnitude**, and its test file — plus `test_capabilities.py`, which fails if a solver
module has no entry, an entry points at a file that does not exist, or a `validated` field
is too thin to say what was checked. **That last gate rejected fourteen of our own entries
on its first run** ("against dense norms" — a sentence that sounds like validation and
contains no claim); each is now a magnitude or an explicit *no independent published known
answer*.

**(M-8) A 10× SPEEDUP, FOUND BY PROFILING RATHER THAN BY GUESSING.** 81% of a Scenario-2
step (3.4 s of 4.2 s over forty steps at n=801) was inside `natural_spline_slopes` — two
Thomas sweeps as **Python loops**, re-executed nine times per step with coefficients that
depend only on the grid. `line_hilbert.slope_matrix` assembles the operator once per grid
and applies it as a gemv: **43 ms → 4.2 ms per step at n=801**, gated to 2.7e-13 against the
sweeps it replaces. This is what made the M6 refinement ladder affordable in one leg.

**NEW BANKED LESSONS (77)-(78).**
**(77) CHECK THE LITERATURE AGAINST YOUR QUESTION, NOT ONLY AGAINST YOUR ANSWERS.** Route-J
read the papers to see who had pre-empted our results and deleted seven claims. Nobody read
them to ask whether the thing we were building was wanted. Twenty legs of certification
machinery were aimed at a theorem published in 2022. **The target of a programme is a
literature question, and it expires like any other.**
**(78) AN INVENTORY IS A CHECK, SO IT DECAYS AT THE RATE OF MEMORY TOO (68, one level
down).** Thirty-five solver modules is past what fits in a session's head, and the failure
mode is not confusion — it is silently rebuilding, or silently not using, something already
validated. The fix is the same as for the plan and for the literature: **make it code, and
make it fail.**

**WHAT MUST BE BUILT NEXT, IN ORDER:** (1) the **bordered** residual for CHL (4.1) with all
three constants as unknowns — bordered from the start, NOT projected, which is what failed
in leg 44 (L-7); (2) a converged profile checked against the normalization-INDEPENDENT
`c_l/c_ω = −2.5114` (the absolute triple is normalization-dependent and ours will not match
it — §8 documented that already); (3) then `Y₀`, `Z₁`, `Z₂` against the budget.

**NOVELTY: nothing claimed.** Naming an object as uncertified is a statement about the
literature in `Papers/MANIFEST.md`, read for this leg. No `Y₀`, `Z₁` or `Z₂` was computed
for any candidate. No link of the L1→L4 chain moved; Clay stays ~0.05%.


## §35 — ROUTE-PORT v1 DONE (2026-08-04): THE BORDERED SYSTEM ON THE UNCERTIFIED OBJECT.
## THE RADII POLYNOMIAL CLOSES IN FLOAT AT EVERY RUNG -- AND THE BALL IS 1.55e+08x TOO
## SMALL TO CONTAIN THE OBJECT. THE SECOND CLAUSE WAS PRE-COMMITTED.

solver/bordered_hl.py + test_bordered_hl.py **10/10**;
experiments/p2_route_port_v1_bordered.py -> writeup/data/p2_route_port_v1_bordered.json.
BLOG/TECHNICAL_P2_ROUTEPORT_V1.md. Deterministic (**16.7 s**). Plan stage PORT -> DONE.
**No link of the L1->L4 chain moved.**

**TARGET (Route-M's, sec 34): `HL_S2_nonsymmetric`** -- the strictly positive, regular,
NON-SYMMETRIC self-similar profile of the 1D Hou-Luo model, CHL arXiv:2604.01868 sec 2.5 /
sec 4, reported April 2026 as a "previously unreported blowup phenomenon", **NUMERICAL ONLY,
no proof of any kind.**

**(P-1) BORDERED FROM THE START, AND THE BORDERS ARE LOAD-BEARING.** The steady form of CHL
(4.1) carries THREE continuous gauge freedoms -- amplitude, dilation, **translation** (the
last is why three and not two: a non-symmetric profile has no symmetry point to pin it) -- so
the system is 2n equations against 2n+3 unknowns. CHL's (4.2) supplies exactly three BORDER
ROWS pinning Omega(0), Omega_X(0), V(0). **This shape is a direct consequence of sec 33's
(L-7)**: on the 2D object we solved then projected, and Newton accepted no step at all.
**Ablation: drop the borders and it does NOT converge -- residual 1.42e-2 after 60 iterations
against 1e-14 in 4 with them.**

**(P-2) NEWTON CONVERGES WHERE THE RELAXATION FLOORS, AND THE FAR FIELD IS WHY.**
n = 201/301/501/801/1201 -> residual **5.66e-15 / 7.61e-15 / 1.25e-14 / 3.12e-14 / 3.52e-14**,
16 iterations cold then 4 on continuation. `RescaledHLScenario2` time-steps the SAME equations
with the SAME origin gauge and **floors at ~1e-2** (its own leg said so in advance). The
steady equation forces an ALGEBRAIC tail **Omega ~ |X|^(c_om/c_l) ~ |X|^-0.394**, and a
relaxation from compactly-decaying data must TRANSPORT that tail out to |X| ~ 745. **Newton
does not transport; it solves.** That is the whole reason a defect Y_0 exists here and did
not in sec 32.

**(P-3) THE 1.17% RATIO GAP IS REACH, NOT RESOLUTION -- AND IT EXTRAPOLATES.** The ratio is
resolution-converged to the 4th decimal (-2.541222 -> -2.540746 over n=201..1201) and still
1.17% from CHL's -2.5114. Reach/stretch/datum were ablated TOGETHER before naming a suspect
(lesson 74) and reach is the mover: rho_max = 6/7/8/9 -> X_max = 100.9/274.2/745.2/2025.8 ->
ratio **-2.583087 / -2.557642 / -2.541222 / -2.530473**. Power law in X_max with slope
**-0.437** (consistent with the tail exponent -0.394), extrapolating to **-2.511926 vs CHL's
-2.5114, rel err 2.09e-04**; two independent windows agree to **0.93%**.

**(P-4) THE CERTIFICATE CLOSES -- AND THE SPACE IS WHAT CLOSES IT.** Weighted sup norm,
A = DF^-1 in float64. Y_0/budget, tuned vs naive, at n = 201/401/801:
**1.95e-04 / 6.36e-04 / 2.40e-04 (all feasible)** against **1.0125 / 3.3193 / 1.2578 (none
feasible)**. The two differ in ONE CONSTANT -- the weight's length scale w_l, 0.01*X_max
against X_max -- and it is worth **5186 / 5222 / 5236x**. **Closure is a property of the
SPACE, not of the object.** Found before stage B was scheduled; it is the empirical case for
stage B and it was not gone looking for.

**(P-5) AND THE WEIGHT HAS A WALL THE EQUATION BUILT.** p* = 0.39 is NOT tuned: the profile's
own tail is |X|^-0.394, so a weight (1+X^2)^(p/2) with **p > 0.394 makes the TRUE profile's
norm infinite**. Any stage-B search over this space is searching a box with one wall already
set by the object.

**(P-6) THE CEILING, PRE-COMMITTED AS CLAUSE P6b BEFORE THE CERTIFICATE WAS COMPUTED.**
*How far is the truncated object from the less-truncated one, in the certificate's OWN norm?*

    ||z(X_max=745) - z(X_max=2026)|| = 1.831e-01   (worst block: Omega)
    the float ball                   : r in [2.97e-12, 1.18e-09]
    ratio                            : 1.548e+08

**THE CERTIFICATE CLOSES AROUND THE TRUNCATED OBJECT. THE TRUE OBJECT IS EIGHT ORDERS OF
MAGNITUDE OUTSIDE THE BALL.** "The polynomial closes" and "the ball does not contain the
thing we care about" are both true at once, and **reporting only the first is the exact
failure mode WIN_CONDITION.md exists to prevent.**

**WHAT THIS IS NOT.** A float REHEARSAL, not a proof -- A is DF^-1 in float64, so Z_1
measures the CONDITIONING of the discretized problem rather than bounding an operator norm on
a function space; nothing is interval-enclosed (the boundary Route-D v16 drew). Not a
certification of CHL's object: it is a certification-shaped computation about a
finite-dimensional TRUNCATION of it, with the distance to the real thing measured and
reported as too large. **Not a link of the chain.**

**WHAT IT DOES ESTABLISH:** the machinery runs END TO END on an uncertified object for the
first time -- Newton converges, the defect exists, the bounds assemble, the polynomial closes
-- and the two things between here and a real result are now **named and quantified**:
interval arithmetic, and the truncation budget (1.55e+08x).

**NEW BANKED LESSONS (77)-(79).**
**(77) PRE-COMMIT A CLAUSE THAT ASKS WHETHER YOU CERTIFIED THE RIGHT OBJECT, not just whether
the certificate closed.** P6b was written before the certificate was computed and it is the
whole result. Without it this leg ships a headline that is true clause by clause and
misleading overall.
**(78) A GAUGE FREEDOM IS AN UNKNOWN, NOT A POST-PROCESSING STEP.** sec 33 solved then
projected and Newton took no step; here the same three freedoms are unknowns of the same
Newton system and it converges in 4. **Count the continuous symmetries FIRST and border the
system by that count** -- a non-symmetric object has one more than a symmetric one.
**(79) WHEN A METHOD FLOORS, ASK WHAT IT HAS TO TRANSPORT.** The relaxation floors at 1e-2
because an algebraic far-field tail must be carried out to |X| ~ 745; Newton solves for it
instead. The floor was a property of the METHOD's information flow, not of the problem.

**NEXT (plan_of_record.py): stage C-PILOT** -- evolve the Lyapunov weight on a known-answer
object, with the six-property viability gate re-run ON THE NEW FITNESS before any GA compute.
(P-4)'s 5236x and (P-5)'s wall are the search space's motivation and its one hard boundary.
