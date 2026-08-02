# Continuation prompt (copy into a fresh session)

*Written 2026-08-02 (updated after Route-F v1). **NEWEST LEG FIRST — ROUTE-F v1 GIVES THE
"BEAT VISCOSITY" SENTENCE A MEASURED RIGHT-HAND SIDE: s_c = alpha/2, THE CRITICAL DISSIPATION
EXPONENT IS HALF THE FAR-FIELD DECAY EXPONENT — AND NAVIER-STOKES IS THE MARGINAL MEMBER.**
Ranked item (2), promoted when §26 shut the DSS lane's cheap entrance; **it is the only item on
the list that probes the ACTUAL obstruction between a toy certificate and NS rather than
polishing the toy, and it moves NO link of the chain.** For omega_t + a u omega_x = omega u_x -
nu(-Delta)^s omega: a self-similar blowup has omega ~ (T-t)^-1, L ~ (T-t)^beta, and **§26's
rescaling ODEs give beta = 1/alpha** with alpha the profile's far-field decay exponent, so
D/N ~ nu (T-t)^{1-2s/alpha} and **s_c(a) = alpha(a)/2**. **THE NS READING IS THE POINT: NS's
natural scaling is beta = 1/2 ⇒ alpha = 2 ⇒ s_c = 1 EXACTLY, the ordinary Laplacian. NS is
critical — every scaling argument returns zero information because the two sides balance
identically — while in gCLM alpha is a MEASURED DIAL, so the family WALKS THROUGH the point
where NS is stuck. That is the toy's value: not that it blows up, but that it is off-critical
in a controlled way.** **METHOD: measure an EXPONENT, not a threshold** — a binary blowup sweep
near a critical exponent is biased, resolution-dependent AND biased in the expected direction,
so instead fit **D/N ~ (T-t)^p against p = 1 - 2s/alpha**, a whole LINE whose slope, intercept
and zero are separately checkable. **F2 (a=0, alpha=1 EXACTLY, nothing fitted):** p =
+0.733/+0.523/+0.318/+0.109/-0.100/-0.309/-0.503 at s=0.15..0.75 vs predicted
+0.700/…/-0.500; slope **-2.068** vs -2, zero at **0.5033** vs 0.5000. **F3 THE CROSS-CHECK,
the part worth keeping: alpha from §26's STEADY COMPACTIFIED SOLVE ON THE LINE vs dp/ds from
TIME-DEPENDENT PERIODIC simulation — no shared grid, basis, formulation or fitted constant —
ratio 1.0419/1.0137/1.0157/1.0169 at a=0/0.2/0.3/0.4, i.e. 1.022 +- 0.014 WHILE ALPHA DOUBLES**
(a uniform ~2% bias, not an a-dependent failure). **ERROR BAR = THE FIT WINDOW, SWEPT NOT
CHOSEN: slope -2.02 +- 0.09, s_c 0.51 +- 0.05**; single exponents move +-0.07 and approach the
prediction MONOTONICALLY FROM ABOVE (an asymptotic regime being entered), and the slope is
steadier because every s shares the window so the bias cancels. **THE nu CONTROL PASSES ONLY
WEAKLY AND SAYS SO** (slopes -1.866/-2.051/-2.110 over nu=1e-2..1e-4, spread 0.245) — the
measurement most worth tightening. Resolution contributes ~0.01 (two finest grids differ by
1.2e-2). **F6 THE MAP: s_c = 0.500/0.571/0.667/0.809/1.040/1.500 at a=0…0.5, crossing the
ordinary Laplacian s=1 at a ~ 0.383.** **THE SENTENCE TO BE CAREFUL WITH: above that the SCALING
says the blowup beats ordinary viscosity — arithmetic about GCLM's OWN SCALING, NOT a statement
about NS, and NOT a claim that a viscous gCLM blowup EXISTS there (the scaling says which term
dominates GIVEN the self-similar form; showing a solution reaches it is the whole difficulty).
NS's alpha is pinned at 2 by dimensional analysis and is not a dial. The map is ORIENTATION,
not evidence about NS.** **THE RESOLUTION GUARD TOOK THREE TRIES and two were silently
degenerate** — energy above 2/3 k_max reads EXACTLY 0.0 at some n (the dealiasing already zeroed
that band; a guard that is zero by construction reads as "perfectly resolved"), energy above n/6
reads ~0.37 for EVERY run (a near-singular spectrum is genuinely fat); what works is the
amplitude AT THE CUTOFF vs the peak, and the run now **REFUSES** ("under_resolved") rather than
returning a number. New solver/fractional_gclm.py + test_fractional_gclm.py (6/6; suite **24
files green**); fig35; BLOG/TECHNICAL_P2_ROUTEF_V1.md; PHASE2_P2_NOTES §27. Everything banked +
pushed on `main`. **NEXT: the two remaining ranked items are (3) the L1→L2 port to 2D
Boussinesq / axisymmetric Euler with boundary — where certification results actually count and
Spike 1 already reproduced the Chen-Hou regular profile — and (1) the DSS lane's EXPENSIVE
entrance (a genuine periodic-orbit search with nothing nearby to seed it). (3) is the better
value. Also: the LITERATURE CHECK is now **PARTIALLY UNBLOCKED — see LITERATURE_CHECK.md, and READ IT
BEFORE CLAIMING NOVELTY FOR ANYTHING.** The blocker is an egress ALLOWLIST, not a broken proxy
(`export.arxiv.org` says so verbatim; WebFetch on arxiv.org/abs, arxiv.org/html and alphaxiv all
403) — but **WebSearch works and its backend CAN read those pages**, so a first pass was possible.
**IT CHANGED THE PICTURE: of four checkable claims, TWO look PRE-EMPTED and one is at serious
risk.** (i) the FINITE SUPPORT of v12/v13 — "self-similar profiles of the De Gregorio model must
be compactly supported" (arXiv:2209.08232); (ii) Route-E v1's eigenvalues-are-only-symmetry-modes
— arXiv:2607.19762 (22 Jul 2026, 41 pp) reports the full point spectrum of the CLM profile is
exactly {0,1}, the symmetry modes, IN OUR OWN NORMALIZATION Omega=-y/(y^2+1/4), rigorously (so
Route-E is CONFIRMED but not novel); (iii) **Route-F v1's s_c = alpha/2 may already exist as
"s*(a) = 1/c_l(a)"** — if c_l = 2*beta the two are the SAME statement, and this is THE most
important thing to verify against a primary source; (iv) "Okamoto et al provided numerical
evidence for travelling-wave solutions for ANY a>0", which does not refute a*≈0.5-0.55 (ours is
HQW25's TWO-SCALE inner object, plausibly different) but does mean the claim must say WHICH object
stops existing. ALL OF THAT IS SEARCH-LEVEL AND UNVERIFIED — summarisers blend sources. **THE ASK
FOR THE USER: add `arxiv.org`, `export.arxiv.org`, `api.semanticscholar.org`, `link.springer.com`,
`aimsciences.org` to the environment's egress allowlist.** The three METHODOLOGICAL candidates
(discrete-ball trap; weighted-l1 conservation law; elasticity discipline) are still UNCHECKED and
are the likeliest to be genuinely new, because they are about the METHOD rather than about gCLM.***

*Before Route-F v1: **Route-E v1 opened the DSS lane and shut its cheapest entrance.** **NEWEST LEG FIRST — ROUTE-E v1 OPENS THE DSS
LANE AND SHUTS ITS CHEAPEST ENTRANCE.** v15/v16 named DSS as the swing. Necas-Ruzicka-Sverak
(ext. Tsai) rules out EXACTLY self-similar NS blowup, and in dynamic-rescaling variables
**self-similar = FIXED POINT, DSS = PERIODIC ORBIT**, so the cheapest way a periodic orbit could
exist near this project's objects is a **HOPF bifurcation off the fixed point** — one dense
eigenvalue solve. **VERDICT: at both points where the instrument can see, the only grid-converged
ISOLATED eigenvalues are 0 and -1, THE TWO EXACT SYMMETRY MODES (dilation; amplitude, from
L(Omega) = -Omega + X Omega_X). No complex pair, nothing near the axis, NO HOPF.** Backed by a
**PLANTED POSITIVE CONTROL** (same filter, same operator + a smooth bump ⇒ isolated **+1.083**
at V=6, **+4.578** at V=12), so "only symmetry survives" is a measurement, not a blind spot.
**THE MECHANISM IS BETTER THAN THE VERDICT: at a=0 the linearization is exactly solvable and its
continuum is (w-1)^{1-lambda}(w+1)^{1+lambda} on the strip -1 < Re lambda < 1; the purely
imaginary members are X^{1-iy} e^{iy tau} = exp(iy(tau - log X)), a wave travelling OUTWARD IN
log X, exactly tau-periodic. The log-periodic structure a DSS solution is MADE OF is present —
as CONTINUOUS spectrum. A continuum has no eigenvalue to move.** **SAID ALONGSIDE, NOT BURIED:
the flow is NOT spectrally stable — its ESSENTIAL spectrum fills [c_omega+1, c_omega+H Omega(0)]
= [0,+1] at a=0 and [-2,+5] at a=1/2 (measured [-2.0005,+4.564]), complex members included; those
directions carry a CORNER AT THE ORIGIN, are norm-dependent, and still cannot bifurcate.**
**THE BUILD (worth reusing): compactify X = tan(theta/2), odd sines ⇒ H(sin k th) = -cos k th +
(-1)^k, X d/dX = sin(th) d/dth, d/dX = (1+cos th) d/dth ALL EXACT — the dilation term is bounded
and exact — and the velocity is exact via N_{k+1} = -2N_k - N_{k-1} - 2cos kt (every N_k a trig
polynomial; NO QUADRATURE ANYWHERE). The a=0 self-similar anchor is ONE MODE, Omega = -sin theta,
residual 1.1e-16.** **A GAUGE THE PROJECT HAD BEEN CARRYING IS WRONG FOR a != 0:
c_omega = 1 - H(Omega)(0) admits NO fixed point at all for a != 0 (R_X(0) = -a H(Omega)(0)
Omega_X(0)); the forced repair is c_omega = 1 + (a-1) H(Omega)(0).** BY-PRODUCTS: **alpha(a) =
-c_omega(a)** is an OUTPUT (1.0000/1.1414/1.3345/1.6172/2.0795/3.0000 at a=0..0.5, Richardson),
the branch is lost at a=0.65 with 1/alpha → 0 at **a_c ~ 0.694**; odd-integer alpha ⇒ analytic ⇒
spectral, confirmed at **alpha=1 (a=0), alpha=3 (a=1/2, twelve digits) and alpha=5
(a=0.5821792673)**; **what stays UNEXPLAINED is why alpha=3 lands on a round rational while
alpha=5 does not.** NOVELTY UNCHECKED — **PDF ACCESS IS STILL BLOCKED (arxiv + publishers 403 at
the proxy CONNECT); that is now THREE legs and it is still the cheapest unblocking act.**
**TWO ERRORS CAUGHT INSIDE THE LEG, both banked: (i) the filter kept a "third eigenvalue" at
a=1/2 whose K-ladder converged to -2 in SIX DIGITS — it is the essential spectrum's LEFT EDGE
c_omega+1, exposed by the free control at a=0 where the identical edge carries 99% of the
spectrum (tightening the filter would have made it MORE convincing); (ii) I hypothesised the
odd-alpha rule from two points, found the third, read TWO RUNGS of its ladder as algebraic, wrote
the rule off as false AND COMMITTED THAT — four more rungs gave order 3.6→6.5→11.5→15.4→19.7,
i.e. exponential, and the rule holds. Both corrections are in place and MARKED.** New
solver/rescaled_spectrum.py + test_rescaled_spectrum.py (8/8; suite **23 files green**); fig34;
BLOG/TECHNICAL_P2_ROUTEE_V1.md; PHASE2_P2_NOTES §26. Everything banked + pushed on `main`.
**IT MOVES NO LINK OF THE CHAIN AND IS NOT CLAY PROGRESS — it is lane scoping, and it stops the
project building a DSS search around a mechanism that does not exist here. NEXT: the DSS lane is
NOT closed, its CHEAP entrance is. Entering costs a real periodic-orbit build with nothing nearby
to seed it. WEIGH THAT AGAINST (2) the Hou-Luo CRITICAL-VISCOSITY MAP (well-posed, publishable
either way, directly probes "can a blowup beat viscosity") and (3) the L1→L2 port to 2D
Boussinesq. DO NOT default into the expensive DSS build.***

*Before Route-E v1: **Route-D v16 was the float rehearsal**, framed by v15 as a CAPABILITY BUILD
not a result. **NEWEST LEG FIRST — Route-D v16 IS THE FLOAT
REHEARSAL, framed by v15 as a CAPABILITY BUILD not a result. IT DOES NOT CLOSE, and the reason
is not the far field.** **THE GOOD NUMBER: Y_0 REACHES MACHINE PRECISION** — the defect of the
INTERPOLANT as a function (v12's distinction, which survives the reformulation) runs
**1.5e-2 → 4.0e-5 → 2.0e-10 → 1.5e-12** over K=16..96 at a=0.3, against a NODAL control flat at
1e-14 by construction. (Fits K^-13.0/K^-16.3 are FLOOR-CONTAMINATED — the honest claim is
"faster than the algebraic K^-(2/a+1) and it reaches machine precision", NOT a rate.) For scale:
GA floor ~1e-2 for five legs; v12's anchor-priced budget 2.4e-4. **Z_0 = 1.6e-11** (roundoff, as
it must be). **Z_2 IS INFINITE IN THE SUP SETTING, TWO INDEPENDENT REASONS, NEITHER THE FAR
FIELD:** **(a) H is unbounded on sup ON A BOUNDED INTERVAL** — v4's W3 is a LOCAL fact (about a
jump, not about infinity), so **removing the far field killed the DECAY grading and left the
SMOOTHNESS one completely untouched**; adversary (Chebyshev partial sums of a step, built inside
the real perturbation space de=(1-v^2)ds) grows **1.350→3.040 over K=8..256, linear in log K at
+0.499/e-fold**. **THE INSTRUMENT CHECK THAT MAKES IT TRUSTWORTHY: the NAIVE probe (one high
mode) ALSO "diverges" (0.998/2.935/6.436) and it is ENTIRELY THE QUADRATURE** — under a 4x
refinement the naive row at K=256 collapses 6.436→0.999 while the adversary row is
2.991→3.041. One row moves, one does not; **both are kept in the module and the figure.**
**(b) sup|N''| is finite EXACTLY for a <= 1/2** (N=e^{1/a}, N''=p(p-1)e^{p-2}, e vanishes
LINEARLY at the edge ⇒ need p>=2) — **exactly where Omega loses C^2**. Growth factor over an
8-decade edge-cutoff tightening: **1.00 at a=0.2..0.5; 28.5/466/3.8e4/1.0e6 at
a=0.55/0.6/0.7/0.8**; at a=1/2 the value is p(p-1)=2 EXACTLY. **THREE THINGS (b) IS NOT: not a
statement about the EQUATION (v14 solves the profile grid-converged to a=1.2 — the wave exists,
the NORM fails); NORM-DEPENDENT (a weight (1-v)^{(2-1/a)/2} restores it, at the price of
perturbations vanishing at the edge — lesson 13's trade); and NOT an explanation of a\***. The
coincidence with a*~0.5-0.55 is RECORDED because recording it is how the next person disproves
it — v12's a=1/3 control is the precedent, and **no control has been run here.** **Z_1 IS NOT
COMPUTED AT ALL** (the infinite-dimensional tail = the whole content of a real CAP);
`rehearsal()` returns it as **None, not zero, and REFUSES to return a radii polynomial**.
**THE REPAIR IS MEASURED, NOT ASSUMED:** the same adversary against
||de||_gamma = sup|de| + [de]_gamma gives slopes **+0.066/+0.014/-0.021/-0.049/-0.057/-0.050**
at gamma=0.15/0.25/0.35/0.5/0.65/0.85 — **divergence stops at gamma >~ 0.35, and gamma=0.15
STILL CREEPS**, which is what shows the threshold is real and not an artefact of dividing by any
seminorm. **v5 U1 found the SAME 0.35 on the whole line — a genuine independent check, because
v5's norm ALSO carried a decay grading and this one has none, so the threshold belongs to the
SMOOTHNESS half.** So v5/v7/v8's Holder machinery is the next brick and is NOT wasted: the
compact-interval version has **no decay grading, no resonance, no matching radius X_0, no tail
bound** — v7-v9 with the expensive half deleted. **CORRECTION TO v14: "the cold start converges
at every a" is overstated — at a=0.7 it misses the basin and needs continuation; every other
value in 0.2..1.2 converges cold.** New solver/reduced_certificate.py +
test_reduced_certificate.py (16/16; suite **22 files green**); fig33;
BLOG/TECHNICAL_P2_ROUTED_V16.md. Everything banked + pushed on `main`. **NEXT — UNCHANGED FROM
v15's ranking, and v16 does not disturb it: (1) verify the two load-bearing literature readings
(BLOCKED ON PDF ACCESS — tell the user); (2) the DSS lane as the swing; (3) the Holder version
of the reduced space ONLY as a capability finish, clearly labelled as such.** Do NOT run another
whole-line estimate leg.*

*Before v16, in the same session: **Route-D v15 IS THE
LITERATURE CHECK, and it re-prices fifteen legs. READ THE LIMITATION FIRST: NOT ONE PAPER WAS
READ** — this container's network policy blocks arxiv.org and every publisher domain reached
(WebFetch and curl both 403 at the proxy's CONNECT). Web SEARCH works. So identifiers (titles,
authors, arXiv numbers, DOIs) are reliable and **every technical statement below is a
search-summary paraphrase = a LEAD, not a fact.** Data writeup/data/p2_literature_scope.json
carries an explicit `confidence` and `must_verify` per entry. **WHAT IT FOUND:**
**arXiv:2603.25104 (Huang, Tong, Wang, 2026-03-26)** — abstract-level, the two-scale blowup's
inner profile is governed by a TRAVELING WAVE on the smaller scale and **its existence is
established rigorously via a FIXED-POINT METHOD. That is THIS PROJECT'S OBJECT.** Same
abstract, and this is the **highest-value unverified item in the leg**: the two-scale scenario
is described as the **a <= 0** case with **a > 0 giving ONE-scale** self-similar blowups — and
this project has worked the two-scale object at **a > 0** throughout, so **the question may not
be whether our object is novel but whether it is the RIGHT OBJECT**. **arXiv:2305.05895 (same
group, 2023)** — gCLM self-similar profiles exist for all a <= 1, "either smooth on the whole
real line or **COMPACTLY SUPPORTED** and smooth in the interior of their closed supports", via
the fixed point of an a-dependent nonlinear map R_a with Omega(x) = -x f(x); a=1 compactly
supported. So **v12's "the profile ends" is a known phenomenon and v14's reduction is a known
technique. Okamoto-Sakajo-Wunsch, DCDS 34 (2014) 3155-3170** computed gCLM traveling waves and
their asymptotics for every a>0 — since 2014. **arXiv:2209.08232** — infinitely many compactly
supported self-similar De Gregorio solutions on the line. **AND THE DECISION-RELEVANT ONE:
computer-assisted proofs by interval arithmetic (INTLAB) + Newton-Kantorovich are ROUTINE IN
THIS EXACT FAMILY** (Chen-Hou rigorous numerics; per search summary, one-scale asymptotically
self-similar CLM blowups already certified). **CONSEQUENCE — SAY IT PLAINLY: L1 IS OCCUPIED
TERRITORY.** Finishing the certificate is a **CAPABILITY DEMONSTRATION and a REPRODUCTION**,
which is exactly what standing brick (4) always said it was in a bullet the project had been
ignoring for five legs. **The marginal value of the next Route-D leg dropped, for a reason
external to the work.** WHAT IT DOES NOT DO: does not touch the two structural walls, does not
change the ~0.05% odds, **does not invalidate one measurement in v3-v14 — being second is not
being wrong.** **v14's novelty claim is RETRACTED to "presume the first integral is KNOWN",
corrected IN PLACE in both v14 writeups with the change MARKED.** Also logged deliberately,
flagged **DO NOT USE / DO NOT REPEAT AS A RESULT**: arXiv:2604.09949 (2026-04-10, single
author) claims stable finite-time singularity for 3D NS with a computer-assisted validation —
recorded ONLY so a later session does not rediscover it and lose a day. **NEXT, and the
recommendation CHANGED:** (1) **VERIFY THE TWO LOAD-BEARING READINGS** (the a-sign in
2603.25104; whether its fixed point IS this first integral) — both need a PDF, so **the binding
constraint on the next decision is ACCESS, not compute and not cleverness**; until then treat
the a>0 two-scale object as POSSIBLY THE WRONG OBJECT. (2) **THE DSS LANE BECOMES THE SWING**
(standing item (1); Necas-Ruzicka-Sverak/Tsai force non-self-similarity for NS relevance, a DSS
blowup is a PERIODIC ORBIT of the rescaled flow, and global search is what this project's
tooling is actually good at) — **but the "uncrowded" reading is the WEAKEST inference in the
leg: absence of search hits is not absence of literature, never let it harden.** (3) Finish the
certificate anyway, cheaply, **and stop calling it the result.** No code, no figure, Level-0.*

*Before v15, in the same session: **Route-D v14 FOUND AN
EXACT FIRST INTEGRAL OF THE PROFILE EQUATION, and the kill switch v13 specified PASSES.**
E := c + aU satisfies E_X = a H(Omega) BY DEFINITION — which is the equation's own
nonlinearity — so R = Omega H(Omega) - E Omega_X = 0 is (log|Omega|)_X = (1/a)(log E)_X, and
integrates:*

    **Omega(X) = -( E(X)/c )^{1/a} ,   E = c + aU ,   U_X = H(Omega).**            (FI)

*Thirteen legs discretized an equation that integrates once in closed form. **GATED THREE
WAYS:** (i) the a->0 limit (1+aU/c)^{1/a} -> exp(U/c) IS the exact anchor — on
U = -(1/2)log(1+X^2), c=1/2 it gives Omega = -1/(1+X^2), measured **1.11e-16**, and the
finite-a form approaches it at the predicted O(a) (a^1.011); (ii) on the whole-line
collocation build, which knows nothing about it, the spread of |Omega|/E^{1/a} runs
**5.9e-8 -> 1.0e-11** (a=0.2) and **2.3e-6 -> 5.1e-9** (a=0.3) over J=200..1600 — an order
BELOW the profile's own residual at every J and falling FASTER (x251 vs x126; x20 vs x9),
the signature of an exact identity on an approximate object; (iii) the reconstructed Omega
solves the ORIGINAL R off-node to **1.9e-10**, converging at the U-quadrature's own n^-1.98.
**THREE v12 MEASUREMENTS BECOME ONE-LINERS:** the profile ENDS (E decreases, hits 0 at X_c,
beyond which E^{1/a} is not real — FORCED, not discovered; caveat said out loud: needs
H(Omega)<0 for X>0, true on every solution found, not proved); the zero has order 1/a WITH
the amplitude A = (2s(1)/X_c)^{1/a} (fitted exponents 4.000019/3.333350/2.500014/2.000013/
1.250017 vs 1/a, rel err <=1.4e-5); and the radius law gets its constant. NEW: **Omega is
only C^{1/a} at the edge — classical exactly while a<1, and at a=1 (De Gregorio) the edge is
a CORNER** (observation, needs the literature check, not another leg). **THE REDUCED SYSTEM:**
v=X/X_c, e=E(X_c v)/c, and c e' + a X_c Hpv[e^{1/a}] = 0 with e(0)=1, e(1)=0 — scalar, on a
bounded interval, c a pure scale. Two reasons it converges where solver/finite_support.py
never did: **e(1)=0 goes in the ANSATZ** (e=(1-v^2)s), so the order-1/a zero is an OUTPUT;
and **the edge row is NON-DEGENERATE** (R itself is identically 0 at X_c, so a direct build
must APPEND a free-boundary condition — here the equation prices it). Cold start (s==1,
X_c0=10 at every a), **5-10 Newton steps to ~1e-14, for every a in 0.2..1.2**. X_c/c matches
the whole-line build's own E-crossing to **3.9e-6/4.3e-6/7.3e-5** (v12's two builds: 0.06-0.11%)
and is K-converged to 3.7e-13. **THE KILL SWITCH PASSES: ||A|| = K^-0.0009/+0.0009/+0.0010/
+0.0011 at a=0.2/0.3/0.4/0.5 over K=48..192**, against the control — same code, same decay
grading that produced v12's number — **J^-0.004 (a=0, v12: -0.003) and J^+2.800 (a=0.2,
v12: +2.86)**. TWO HONESTY ITEMS: the a=0.2 FULL-ladder slope is K^+0.0308 (the K=16 point is
under-resolved; X_c/c=34.3 while the core stays O(1), so v carries a layer of width ~1/X_c and
needs K >~ X_c) — both reported; and **the flatness is NOT an unweighted-norm artifact**
(re-run at the alpha=1.4 decay grading: K^-0.0030/+0.0008/+0.0011/+0.0013), which it cannot be,
because on a COMPACT interval those weights are equivalent — worth saying because the
UNWEIGHTED whole-line norm grows J^+0.99 **even at the anchor**, purely from the grid radius
~4J/pi. **ALSO: v11's FOURTH confirmation of a* is RETIRED** (on its own support the same
object is K-converged to 6.3e-13/4.9e-12/2.2e-10/2.3e-9/7.6e-9 at a=0.5/0.6/0.8/1.0/1.2 — v11's
whole-line spread was the global basis failing on a compactly supported profile whose edge
regularity is C^{1/a} and gets WORSE as a grows). **What is retired is v11's ARGUMENT, not
a\*** — the other three confirmations are about the two-scale GA problem, untouched; a* is
confirmed THREE times, and separately the compactly supported traveling wave exists as a
continuum object well past it. New solver/first_integral.py + test_first_integral.py (11/11;
suite **21 files green**); fig32; BLOG/TECHNICAL_P2_ROUTED_V14.md; solver/finite_support.py
marked SUPERSEDED with the structural reason. Everything banked + pushed on `main`.
**NOT CLAIMED: a certificate. Y0/Z0/Z1/Z2 do NOT exist in the reduced space; ||A|| converging
says the approximate inverse EXISTS in the limit, nothing about the budget closing. 4.52 is
NOT "better than 47" — different operator, different space, and the comparable quantity is the
SLOPE (quoting the value would be lesson 28 in a new costume). Novelty UNCHECKED: a first
integral of a scalar traveling-wave equation is exactly what is folklore to people who work on
gCLM/De Gregorio.** ~~NEXT — brick (4), FINISH ONE CERTIFICATE END-TO-END, now cheap.~~ **[v15 RE-PRICED THIS:
the certificate is still cheap and still the right capability, but it is a REPRODUCTION, not
the result. See the v15 paragraph above and the lane box.]** Eleven legs of far-field machinery
(v3 resonance, v6 tail bound, v7-v9 estimates, v10 bracket) are genuinely not needed on a
bounded interval, and the **STOPPING RULE is UNCHANGED: if it does not close in float with
margin, STOP, do not harden.** Read BOTH the
"WHERE THIS SITS RELATIVE TO CLAY" section and the "IS THIS STILL THE RIGHT LANE?" box before
committing to another leg.*

*Before v14, in the same session: **Route-D v13 CORRECTED
v12's mechanism, found the real obstruction, and disqualified the repair v12 recommended.**
v12's measurements stand (the a>0 profile ENDS at X_c ~ e^{c/a} with a zero of order 1/a;
||A|| diverges with J at that profile and is flat at the a=0 anchor). Its EXPLANATION did not.
v12 attributed the divergence to a homogeneous mode ~ (X_c-X)^{-1/a}; **that is a dropped sign
in d/dX -> d/ds. With s = X_c-X the homogeneous equation h_c h - a h_c s h_s = 0 gives
h ~ s^{+1/a}, which VANISHES at X_c, and the inhomogeneous solve is bounded there too. Nothing
is singular at the turning point.** Measured inner exponents +5.28/+4.21/+3.51/+3.01/+2.65/
+2.14 vs +1/a = 5/4/3.33/2.86/2.5/2 — right sign, 5-7% high (the usual finite-window fit bias).
**(v14 makes both exponents exact consequences of the first integral, and v14's repair is the
one v13 named.)**
**THE REAL OBSTRUCTION IS IN THE FAR FIELD, and it is worse: outside X_c the same equation has
the same exponent but now GROWS — h ~ (log(X/X_c))^{1/a} — against a domain space that is a
DECAY class, with the amplitude fixed by matching rather than free. That is a codimension-1
RANGE obstruction of the continuum operator, which NO refinement touches** (a local singularity
would at least have been a resolution problem). Measured with an instrument independent of the
matrix (integrate h_X = (H(Omega)/E)h outward on the profile's exact H(Omega), E, out to 1e8):
q = **4.9988 / 3.9980 / 3.3307 / 2.8536 / 2.4855** vs 1/a = 5 / 4 / 3.3333 / 2.8571 / 2.5 —
**0.02-0.6%, no fitted constant**; quadrature converged to 1.6e-4 over a 16x refinement. The
a=0.5 outlier (q=0.054) refines 0.054 -> 1.84 -> 1.70 over J=400/800/1600 while the a=0.4
control sits at 2.4855 -> 2.5035 -> 2.5014, so **the outlier is the instrument**, exactly as
v12's own rate table predicted. **So 1/a now appears THREE times in three roles: the order of
the profile's zero at X_c, the exponent of the vanishing INNER mode, and the power of the log
by which the OUTER mode grows** — all from one leading balance. **THE DIVERGENCE IS NOW
ATTRIBUTED, not argued:** restrict the DOMAIN sup to a FIXED outer radius (the grid's own
radius ~4J/pi grows with J) and the J-slopes fall +2.86 -> +1.06 -> +0.54 -> +0.31 across
cutoffs inf/200/50/20 at a=0.2, while **the a=0 control is FLAT at every cutoff**; and 69-97%
of the extremal row's mass comes from codomain slots within 10% of X_c — **sourced at the
turning point, damage done in the far field**, which is what a growing mode excited at X_c
does. **NOT attributed (say it): a residual J^+0.3..0.5 at fixed radius.** **THE CHEAP REPAIR
IS DEAD:** v12 recommended bordering with the speed c; dilation Omega(X)->Omega(X/mu), c->mu c
is a SYMMETRY of the zero set at every a, so restoring c adds KERNEL, not range — the square
bordered system at a=0 has **cond 4.4e18, smin 4.4e-17**, and the overdetermined version's norm
grows J^+1.40 **even at the anchor** where the plain system is flat. New solver/turning_point.py
+ test_turning_point.py (6/6); fig31; BLOG/TECHNICAL_P2_ROUTED_V13.md;
**v12's writeups corrected IN PLACE with the change MARKED (banner + struck passages), not
quietly edited.** v13's spec — "REMOVE THE FAR FIELD FROM THE DOMAIN; pose the problem on
[0, X_c] with X_c an unknown and perturbations supported there; run the kill switch FIRST" —
**is what v14 executed, and it was right on every count.** Its predicted verdict ("flat => the
framing is repaired and eleven legs of far-field machinery are simply not needed") is the one
that came back.*

*Before v13, in the same session: **Route-D v12 carried the profile into the basis the bounds
are written in and found that the object the certificate is about is not the object the space
was designed for.** The build was the a-transport term in the compactified theta-basis, whose
only non-local piece, U = INT_0^X H(Omega)dX', has a closed form there (U = SUM_k A_k I_k,
I_k = INT_0^theta sin kt/(1+cos t)dt, exact three-term recursion, longdouble because float64
drifts 1.7e-11 by k=800) — which makes the residual of the INTERPOLANT evaluable anywhere. Two
framings came free: **A IS THE NEWTON MATRIX** (the certificate's gauged system is what Newton
iterates, so Y0 = ||A F|| is the size of the Newton step) and **zero at the nodes is not zero as
a function** (Omega*H(Omega) has degree <2J against J collocation conditions; rows Newton
enforces 1.5e-13 vs 9.1e-3 in the row the gauge displaced, at a=0.5). **THE FINDING: E(X) =
c + aU(X) is the true transport coefficient, U inherits the Hilbert transform's logarithm and
runs to -infinity, so E crosses zero at a finite X_c ~ e^{c/a}; approaching it Omega ~
(X_c-X)^{1/a} with no free constant, and beyond it Omega = 0 solves the equation exactly. The
a=0 anchor — on which eleven legs of decay-graded far-field analysis were built — is the
degenerate X_c = infinity limit** (and the same balance at a=0 gives Omega ~ X^{m/(pi c)} =
X^-2, so the anchor's tail and v3's alpha=2 resonance are the a->0 corner of this picture).
Two independent discretizations agree on the dilation invariant X_c/c to **0.06-0.11%**.
CONSEQUENCE: **||A|| at the real profile DIVERGES with J (J^+2.86 at a=0.2, J^+2.75 at 0.3)
while at the anchor it is FLAT (J^-0.003)**, so the seven "bounded" ledger constants are all
constants for the ANCHOR's linearization; the one number that came in **7.7x UNDER budget**
(a=0.2, J=1600, Y0 <= 3.17e-5 vs 2.45e-4) was priced with the anchor's ||A|| and corrects to
~3 orders OVER. **Both sides move the wrong way, by one mechanism.** The survival boundary got
a candidate mechanism (X_c falls 10.6 -> 3.1 -> 2.1 over a=0.25..0.7 while the core half-width
stays ~1) but **the a=1/3 control killed the sharp arithmetic version** (p=1/a hits the integer
2 at a=1/2, tantalisingly at a*, but a=1/3 with p=3 shows no anomaly), so **v12 does NOT
predict a\***. v12's stated MECHANISM for the divergence was wrong and v13 (above) corrects it;
its MEASUREMENTS all stand.*

*Before v12, in the same session: **Route-D v11 attacked the OTHER SIDE OF THE INEQUALITY** and
retired a number the project had carried as physics for five legs. Every a != 0 profile had come
from a GA over a small genome or from fixed-grid relaxation, and BOTH floor at ~1e-2; a Newton
solve on the full grid reaches relres ~1e-14 at every a up to 0.5 — twelve orders. **The floor
was the SEARCH, not the equation.** Newton also converged at a=0.8 and 1.0, which for an hour
looked like "the survival boundary was a genome artifact all along"; it is not — machine
precision on a DISCRETE system proves nothing by itself, and the grid-refinement table (spread
in c over n=401/801/1601: 8e-4/3e-4/3e-5 at a=0/0.2/0.5 but 3.7e-3/1.3e-2 at a=0.8/1.0) shows
the solutions are continuum objects only up to a ~ 0.5. **So the GA's a*~0.5-0.55 is confirmed a
FOURTH time by a method with no genome, no search budget and no stochasticity** — and sharpened:
below a*, an exact discrete traveling wave EXISTS. v11 read Y0's new binding constraint as
"discretization-limited"; v12 found the discretization was not the problem either.*

*Before v11, in the same session: **Route-D v10 earned the
OTHER END OF THE BRACKET, and it changes what we know about the lane.** v9 ended by
admitting that every bracket this project quotes has a lower end that is a maximum over SIGN
PATTERNS — nearly meaningless — so "the bound is 50× too big" and "the operator really is
that large" could not be told apart while implying opposite decisions. **The tell nobody had
checked in six legs of quoting it: the sign-pattern baseline gets WORSE as J grows (0.973 →
0.921). It was never converging to anything about the operator** — only measuring how badly a
jagged vector is punished by a Hölder seminorm. Replaced by an adversary family the Y-ball
actually contains (**1/v × a slowly varying shape**: powers, low cosines, swept bumps,
smoothed steps, boxes; validity is FREE since any g gives ‖A‖ ≥ ‖Ag‖_X/‖g‖_Y, so the whole
problem is CONSTRUCTION — banked lesson 9 pointed at the operator). Results: reference
bracket **50× → 16×**; and at the **OPERATING point (1.4, 0.15)**, where the budget has been
evaluated for three legs, **2.74 ≤ ‖A‖ ≤ 20.94 — a factor 7.7, not 50** (quoting the
REFERENCE point's bracket was itself a second, quieter version of the same mistake). The
extremizer is a **WIDE FAR-FIELD BUMP** (θ=3.12, X≈93, half the domain wide) — the same place
v2's far-field degeneracy, v3's α=2 resonance and v6's X₀ all point, which is a small
independent check that the number is about the problem and not the discretization. **THE
VERDICT — the first MEASURED CEILING on sharpening in ten legs: a PERFECT upper bound on ‖A‖
would move the budget 2.45e-4 → 1.88e-3 and no further, i.e. ~5× short of the GA residual
floor rather than 40×. Better than it looked, and NOT enough on its own** — closing the gap
also needs C_Q's ~4× (v8 X2), and the two together only just reach the floor with nothing
spare for the three open Z₁ items. Everything below is banked + pushed on `main`. **Next:
C_sup (elasticity ≈1, untouched since v6, now with a measured ceiling on the payoff); read
the "IS THIS STILL THE RIGHT LANE?" box, which v10 makes quantitative for the first time.**

*Before v10, in the same session: **Route-D v9**, the SHARPNESS leg, rebuilt the |H(h)|
bound on the exact folded kernel K = 2sinθ/(cosφ−cosθ) (whose p.v. over (0,π) is exactly zero,
so the singularity needs ONE GLOBAL SUBTRACTION instead of v6's band + matching scale +
remainder): ‖A‖ 69.15 → 47.05 (−32%) at the reference — **and the budget did not move**,
because the closure raises that input to the power γ and the operating point sits at γ=0.15
(gain by point 32%/11%/3%/**0%**). Its real output is the **ELASTICITY TABLE**:
d log‖A‖/d log C_sup = **+1.00** at the operating point vs **+0.11** for the input v9 improved.
It also found the **PAYER RULE** — which part of the norm pays at each point is a free
parameter with an interior optimum, and the neutral choice is WORSE than the crude bound it
replaces: *tune the rule to the T/S ratio of the ANSWER, not to 1*. And before v9: **Route-D v8** priced the LAST unbounded constant in
Z₂, the codomain seminorm part of C_Q (weight **1−γ, NOT α−γ** — H does not inherit h's
decay), giving the first COMPLETE Z₂ map; its optimum stayed at (1.4, 0.15) and the budget
moved only 7% (2.58e-4 → 2.39e-4), ending v7's three-legs-running order-of-magnitude loss.
And before that, **Route-D v7** went after the sharpest of v6's three
open ledger items, the **domain SEMINORM part of ‖A‖**, and **closed it** — not by v6's
recommended route (band-limited subspace + faithfulness factor), which a ten-minute
diagnostic disqualified STRUCTURALLY, but by using the EQUATION: solve `DF h = g` for
`h_X`, split every pair at a fixed multiple of the local X-scale, and the weights cancel
identically at every scale, leaving a bound with **no J and no grid in it**. The feedback
is LINEAR in the seminorm while the interpolation gain is SUBLINEAR, so the closure holds
for ANY constants (no smallness condition), and γ=1 is excluded for a third independent
reason. Result: **the first uniform upper bound on the WHOLE of ‖A‖** (69.1→70.3 over
J=125..1600, J^+0.006) and the first (α,γ) interior optimum built entirely from upper
bounds. Two caveats travel with it: pricing the honest ‖A‖ cost the budget an order of
magnitude (the third such leg — see (iii) above for what v8 did to that trend), and the
interpolant's decay-graded norm is INFINITE at every J (a trig polynomial does not vanish
at θ=π where sec^α diverges) — soft (h(π)~J^−3.01) but a change of ANSATZ.*

*Earlier in the session: ran
**Route-D v3, the space-pair scoping leg** — the gating check §11 attached to its own repair — and got a
**NO-GO THEOREM for the entire weighted-ℓ¹ category** together with a **constructive
positive half**: the two Newton–Kantorovich requirements are separated by exactly one
grading power and the separation is CONSERVED (measured minimum exponent sum 0.98 over
the whole family; control 0.00); the replacement is a DECAY-graded pair, which
satisfies both, is resonant at the anchor's own decay rate, and has an interior
optimum α\* ≈ 1.44 — and then **Route-D v4**, which carried those measurements to the
FULL gauged operator in a third independent discretization and got **one confirmation
and one new structural gap**: v3's far-field pricing survives (within 6%; Z₂ = 13.4 vs
13.3 predicted; a second interior optimum at α ≈ 1.40), but the decay-graded SUP pair
does NOT control the quadratic because H is unbounded on L^∞ — and then **Route-D
v5**, which built the two-grading (decay × smoothness) space those two legs jointly
demanded and found that **it works**: v4's adversary is defused, smoothness has its
own interior optimum, Z₂ falls 13.4 → 3.29, and the one surviving marginal direction
has a nearly-free fix — and then **Route-D v6**, which went after the ESTIMATES and
produced the project's **first genuine UPPER bounds** (three of eight NK constants
move MEASURED→BOUNDED) together with a **methodological negative that matters more
than the bounds**: computing an induced norm by duality over a DISCRETE Hölder ball
is UNSOUND, and the ‖A‖~J^0.5 unboundedness it reported under three routes was
fiction. Pricing Z₁ for the first time **KILLS v5's joint optimum**. **The scoping phase
of Route D is DONE; v6 started the estimates phase and left exactly three named gaps, and
v7 (above) closed the sharpest of them.***

Continue the Navier–Stokes blow-up search project. End goal: the Clay Millennium
problem — a genuine, honest attempt via singular-profile / self-similar-blowup
research — while never fooling ourselves with a numerical artifact. WIN_CONDITION.md
is the anti-self-deception contract: only Tier 3 / Level 3 (rigorous proof) solves it;
Tier 1 (candidate) and Tier 2 (resolution-confirmed) are progress. Preserve that
honesty — do not oversell.

USER'S STANDING STEER (honor it): Keep pursuing the Clay end goal. The realistic prize
is novel toy-model singularity research + a tiny (~0.05%) Clay "lottery ticket," NOT a
Clay solve. Keep the lottery ticket the true focus; when something does NOT contribute
to it, say so and be willing to pivot. Gate-check every new brick against "does this
help the real direction" BEFORE building. Produce blog + community writeups WITH
ATTACHED DATA (writeup/ + committed writeup/data/\*.json that rebuilds figures without
re-runs). **WORKFLOW (current session mode): work autonomously in chunks; at the end of
each chunk write a BLOG + TECHNICAL writeup with data + figure, update this
continuation prompt, and push to `main`; then pick up the next chunk and repeat.**

**WHERE THIS SITS RELATIVE TO CLAY (standing section — the user asked for this to be carried
forward explicitly, and for it to be RE-ANSWERED, not just re-pasted, at the end of every leg).**

YES, the Clay problem is still the end goal, and NO, nothing in Route D is a step whose success
would resolve it. Both halves are true at once and must be stated together. The honest way to
hold them is a CHAIN — write down every link that would have to be forged between here and
Clay, and after each leg say which link it moved:

  L1  a certified (Level-2, computer-assisted) self-similar blow-up profile for the 1D gCLM/HL
      toy model at some a > 0.                     <- WHERE THE WORK IS NOW; NOT YET DONE
      (v12/v13 showed L1 as posed was MIS-SPECIFIED; v14 supplied the repair and it passes its
      own kill switch, so L1 is now merely UNFINISHED rather than mis-specified — the first
      time in three legs that link moved forward instead of being reclassified.)
  L2  the same for a model with a genuine 2D/3D mechanism (2D Boussinesq / axisymmetric Euler
      with boundary) — Chen–Hou territory.         <- already done by others for specific data;
      our contribution there would be a new profile or a new method, not the first result
  L3  a certified blow-up for 3D EULER without boundary or symmetry crutches.   <- open frontier
  L4  the same for 3D NAVIER–STOKES, where viscosity must be beaten at small scales. <- Clay
  These arrows are not increments. L2→L3 and L3→L4 are each widely regarded as harder than
  everything below them combined. **We are inside L1 and have not finished it.**

TWO STRUCTURAL WALLS (CLAY_ROADMAP.md §2 — about the problem, not our effort; no amount of good
work removes them):
  * A search/certification programme can only ever argue FOR blow-up. If 3D NS is globally
    smooth — which many experts lean toward — this direction is empty by construction.
  * The only rigorous-proof technology that exists (validated/interval numerics) works on models
    simple enough for interval arithmetic. 3D NS is far outside its reach. A Tier-3 result is
    attainable ONLY on toy models, and toy models are not Clay.

SO WHAT THIS PROGRAMME IS REALISTICALLY FOR: a novel Tier-3 (Level-2 certified) result on a toy
model where blow-up is provable — a genuine, publishable contribution and a stepping stone —
with Clay as a distal ~0.05% horizon. That is the user's standing steer and it has not changed.
Say the honest version out loud in every writeup; never let a good leg drift into implying that
L1 success is Clay progress in any load-bearing sense.

**WHAT WOULD ACTUALLY BE WORTHWHILE TOWARD A CLAY-RELEVANT CANDIDATE (the user asked this
directly; keep it here and revisit it, do not let it rot).**

Two hard theorems decide the strategy, and neither is negotiable:
  * **Nečas–Růžička–Šverák (1996), extended by Tsai** — EXACTLY self-similar blow-up for 3D
    NS in the natural scaling class is RULED OUT. The whole "find a self-similar profile and
    certify it" template that Route D has been building for twelve legs therefore **cannot be
    pointed at NS as-is**; it works for Euler-type models where the scaling is admissible.
  * **Tao's supercriticality barrier** — at the blow-up scale NS's controlled quantities are
    supercritical, and averaged-NS achieves blow-up within reach of energy-method-only
    arguments. Any real proof must exploit structure that survives averaging.
Together: a Clay-relevant candidate must be **non-self-similar** (discretely self-similar, or
an unstable/non-generic scenario) and must beat viscosity at small scales.

RANKED, with the reasoning, not just the list:
  1. **Discretely self-similar (DSS) profile search.** The live candidate class precisely
     BECAUSE exact self-similarity is excluded. A DSS blow-up is periodic in log-time rather
     than stationary — i.e. a periodic orbit of the rescaled flow — and a GA for global search
     plus Newton for refinement is unusually well suited to finding one. This is the most
     Clay-relevant thing available with the tooling that exists, and it looks uncrowded.
     **ROUTE-E v1 (§26) TOOK THE CHEAP ENTRANCE AND FOUND IT SHUT: no eigenvalue of the
     self-similar fixed point is available for a Hopf bifurcation, so a periodic orbit is not
     going to be handed to us by a bifurcation off the branch we already have. The lane is NOT
     closed — the cheap way in is. Entering now means a genuine periodic-orbit search with
     nothing nearby to seed it, and v1 says where such an orbit would have to live (the
     log-periodic directions, which are CONTINUOUS spectrum and of limited regularity at the
     origin). Price that build honestly before starting it.**
  2. **Map the critical viscosity scaling for the Hou–Luo scenario.** The Clay question in
     miniature: take the Euler blow-up Chen–Hou proved, add viscosity, determine numerically
     the scaling at which ν kills it. Well-posed, directly probes "can a blow-up beat
     viscosity", and produces a publishable answer either way.
     **ROUTE-F v1 (§27) DID THIS IN 1D: s_c = alpha/2, measured with nothing fitted at a=0 and
     cross-checked against an unrelated computation of alpha; NS is the marginal member
     (alpha = 2 ⇒ s_c = 1). The 1D version is DONE. What remains of this item is the 2D/3D
     version, which is the same question on the object of item (3) — so items (2) and (3) have
     merged into one next brick.**
     **ROUTE-G v1 (§28) CLOSED THE SCALING HALF OF THIS ITEM ON THE 2D OBJECT: s_c = 1/(2 beta)
     (the invariant form; alpha/2 was a gauge choice), and the Chen–Hou 2D Boussinesq blow-up
     sits at beta = 2.92 ⇒ s_c = 0.171, SIX TIMES the NS collapse rate and on the LOSING side.
     What remains of item (2) is no longer a scaling question — it is the DYNAMICAL one: does a
     VISCOUS solution actually reach the self-similar form? The scaling says which term
     dominates GIVEN the form; producing a solution that gets there is the whole difficulty and
     is untouched.**
  3. **Port to 2D Boussinesq / axisymmetric Euler with boundary.** The current toy is a 1D
     model of the BOUNDARY behaviour of that system; Spike 1 already reproduced the Chen–Hou
     regular profile, so the solver exists. This is the L1→L2 step, where certification
     results actually count.
     **ROUTE-G v1 (§28) TOOK THE MEASUREMENT HALF AND LEFT THE CERTIFICATION HALF UNTOUCHED.**
     It re-measured beta on the 2D object with our own rescaled machine and priced the direct
     time-dependent route out of reach (one extra decade of (T-t) costs 10^beta in LINEAR
     resolution — 832x per direction at Chen–Hou's beta). **The remaining content of item (3)
     is a CERTIFICATE in 2D, which is Route-D's machinery pointed at the Spike-1 object — and
     that is a large build, not a leg.** Before starting it, note v15: computer-assisted
     certification in this family is ROUTINE for the groups working it.
  4. **Finish ONE certificate end-to-end, on anything — even a=0 where the answer is known.**
     Thirteen legs produced constants and never a closed budget. Every route above needs a
     pipeline that demonstrably closes; this is worth doing for the capability, not the result.
     **v14 PROMOTED THIS TO THE NEXT BRICK:** the reduced (first-integral) system on [0, X_c]
     has a convergent approximate inverse at the a>0 profile itself, the far-field machinery
     that made the old constants expensive is simply absent on a bounded interval, and the
     ansatz problems v12/v13 found are gone. It is now the cheapest item on this list as well
     as the one everything else needs.
  5. **The literature search.** Hours of work, and it currently BLOCKS every novelty claim the
     project might make — **now including v14's first integral, which is exactly the kind of
     thing that is folklore to people who work on gCLM/De Gregorio** — plus the three
     methodological candidates (the discrete-ball trap; the weighted-ℓ¹ conservation law /
     no-go; the elasticity discipline).

RECOMMENDED SEQUENCING **(REVISED BY §27)**: the DSS lane's cheap entrance is shut (§26) and
the 1D critical-viscosity map is DONE (§27). **The best-value next chunk is (3), the L1→L2 port
to 2D Boussinesq / axisymmetric Euler with boundary** — it is where certification results
actually count, Spike 1 already reproduced the Chen-Hou regular profile so the solver exists,
and it now carries item (2) with it: the same s_c = alpha/2 arithmetic applied to a 2D object is
the version of the viscosity question that is about a REAL mechanism rather than a 1D caricature.
The DSS lane's expensive entrance is the alternative. **Previously, and now
superseded:** **(4) FIRST now that it is cheap and the framing is repaired** — it is
decisive in the same way the kill switch was, and it is the capability every other route needs;
(5) alongside it, because it is cheap and it is the only thing standing between this work and a
novelty claim; then (1) as the genuinely Clay-relevant swing with (2) as the well-posed
fallback. **NOT more whole-line Route-D estimate legs** — v14 removed the far field from the
problem, so v3's resonance, v6's tail bound, v7-v9's estimates and v10's bracket are all about
a formulation the project no longer uses.

HONEST FRAMING THAT SURVIVES ALL OF THIS: even (1) succeeding yields a CANDIDATE requiring
proof, not a proof — and the proof technology for 3D NS does not currently exist. That is the
~0.05%, and none of the above changes it. What they change is whether the effort is aimed at
the actual obstruction or at polishing a model that was never going to reach it.

**GATE-CHECK BEFORE EACH NEW BRICK (answer it in the leg's writeup, don't just re-paste it):**
  (a) which link of the chain does this move, and how far?
  (b) if the answer is "none — it makes L1 more rigorous or cheaper", is another L1 leg still
      the best use of the chunk, or is the marginal leg now worth less than switching lanes?
  (c) is there a cheaper experiment that would tell us the whole L1 route is dead?
Route D has now had FOURTEEN legs, which is a lot of L1. v12 changed the question, v13 sharpened
it, and **v14 answered it**: the a>0 profile ends at a finite radius because the equation's own
first integral forces it; posed on that support the approximate inverse CONVERGES (K^~0.001 vs
the whole line's J^+2.80). L1 is no longer "mis-specified"; it is unfinished, and the remaining
work is SMALLER than what it replaces because a bounded interval has no far field to price.
Concrete trigger to reassess, and it is the next brick: **assemble Y₀, Z₀, Z₁, Z₂ in the reduced
space at ONE a and see whether the budget closes in FLOAT with margin.** If it does not, promote
the alternative lanes (the coupled-system HL two-stage leg; writing the whole P2 arc up as a
community piece) from fallback to primary — and do NOT harden a float result that did not close.
Standing caution that v14 does not remove: even a closed float budget is Level-2-shaped work on
a TOY MODEL, and none of it is interval-enclosed yet.

THE LEVEL / RIGOR LADDER (the user's framing, honor it): Level-0 = reproduce known
results. Level-1 = a novel numerical map (where ALL gCLM work through fig18 sits).
Level-2 = a rigorous computer-assisted statement (interval / Newton–Kantorovich
certification) = the FIRST rung that is genuinely "novel maths" — **Route-D
v1–v14 + v16 (fig19–fig33) are tooling + scoping/negative results + partial bounds + one exact
algebraic identity on the way there, NOT certificates; v15 is Level-0 scoping and found that
Level-2 in this family is ROUTINE FOR OTHERS; **Route-E v1 (fig34) is Level-1 numerics plus two
small EXACT computations (the closed-form a=0 continuum, and the two symmetry eigenvalues) — a
lane-scoping NEGATIVE, not a certificate; **Route-F v1 (fig35) is Level-1 numerics plus one
elementary scaling derivation — a measured map, not a certificate***; **Route-G v1 (fig36) is
that map PORTED to 2D: one exact derivation (the invariant law + the far-field/collapse
identity), one re-measurement of a PUBLISHED constant with our own machine (so its measured
half is Level-0 BY CONSTRUCTION — reproducing Chen–Hou, not extending them), and one honest
negative with its repair priced. NOT a certificate; the certification half of the 2D port is
untouched.**
Level-3 = Clay.

TERMINOLOGY GUARD (do not drop): the dynamic-rescaling numerics + the GA framework are
Route-A TOOLING (built to FEED Route D). "Route D" proper is the Tier-3
computer-assisted-proof leg; a successful interval-Newton certification is its first
concrete step. A GA proves nothing (Tier-1/2 only).

ORIENTATION (read in this order): PROJECT.md, WIN_CONDITION.md, CLAY_ROADMAP.md.
writeup/ has arc subfolders (1_gclm_1d, 2_phase1_2d, 3_spikes, 4_p2_lottery; data/ +
figures/ stay central; writeup/README.md is the ordered index). Phase 1 (concluded
negative): writeup/2_phase1_2d/NEGATIVE_RESULT_TWO_CURRENCIES.md. P2 — READ:
PHASE2_P2_NOTES.md (TOP STATUS + §2 anchor, §6 degenerate gauge, §7 reframe, §8 B1,
§9 GA framework, §9-cont TWO-SCALE, §9-cont2 a_p(K) map, §10 ROUTE-D v1, §11 ROUTE-D
v2, §12–§18 ROUTE-D v3–v9, §19 ROUTE-D v10, §20 ROUTE-D v11, §21 ROUTE-D v12,
§22 ROUTE-D v13, §23 ROUTE-D v14,
§24 ROUTE-D v15 (the literature check — READ IT BEFORE CHOOSING A LANE),
§25 ROUTE-D v16,
§26 ROUTE-E v1 (the DSS lane opens),
§27 ROUTE-F v1 (s_c = alpha/2 in 1D),
**§28 ROUTE-G v1 = newest (the PORT: s_c = 1/(2 beta), and where the 2D object sits;
read it before choosing a lane, and note that it RETIRES alpha/2 as a gauge choice)**).
Per-leg writeups + figs under writeup/4_p2_lottery/: TECHNICAL/BLOG_P2_{HL_ANCHOR(fig12),
CONJ24(fig13),SCENARIO2(fig14/15),GA_FRAMEWORK(fig16),TWO_SCALE(fig17),KLADDER(fig18),
ROUTED(fig19),ROUTED_DRESS(fig20),ROUTED_SPACES(fig21),ROUTED_V4(fig22),ROUTED_V5(fig23),
ROUTED_V6(fig24),ROUTED_V7(fig25),ROUTED_V8(fig26),ROUTED_V9(fig27),ROUTED_V10(fig28),ROUTED_V11(fig29),ROUTED_V12(fig30),ROUTED_V13(fig31),ROUTED_V14(fig32),
ROUTED_V16(fig33),ROUTEE_V1(fig34),ROUTEF_V1(fig35),**ROUTEG_V1(fig36)**}.md. Then experiments/JOURNAL.md (newest first) and LOGGING.md.

STATE (all banked + pushed to main):
- Phase 1 CONCLUDED. Spike 0/1 DONE. P2 anchor (§2), §6 degenerate-gauge, §7 reframe,
  §8 B1 (Scenario-2), §9 GA framework, §9-cont two-scale a-sweep (5/6), §9-cont2
  a_p(K) convergence map (7/7), §10 Route-D v1, §11 Route-D v2, §12 Route-D v3,
  §13 Route-D v4, §14 Route-D v5, §15 Route-D v6, §16 Route-D v7, §17 Route-D v8,
  §18 Route-D v9, §19 Route-D v10, §20 Route-D v11, §21 Route-D v12, §22 Route-D v13,
  §23 Route-D v14, §24 Route-D v15 (literature scope), §25 Route-D v16,
  §26 ROUTE-E v1 (the DSS lane's Hopf question, answered NO),
  §27 ROUTE-F v1 (the critical dissipation exponent, s_c = alpha/2 in 1D),
  §28 ROUTE-G v1 (the PORT to 2D Boussinesq: s_c = 1/(2 beta), beta the COLLAPSE exponent;
    NS is beta=1/2 exactly; Chen-Hou 2D sits at beta=2.92 on the LOSING side) — all DONE + banked.
- The gCLM two-scale survival boundary is GENUINE (a\*≈0.5–0.55, a SOFT crossing),
  not genome-limited — earned by §9-cont2's GA-/genome-/basis-convergence, i.e. **THREE
  confirmations, not four: v14 RETIRED v11's grid-refinement argument** (on its own support
  the profile is K-converged to 8–12 digits at a=0.5…1.2; v11's whole-line spread was the
  global basis failing on a compactly supported profile whose edge regularity is C^{1/a}).
  a* is about the two-scale GA problem; **the compactly supported traveling wave itself
  EXISTS as a grid-converged continuum object well past a\***, which is a different question.

**P2 §12 — ROUTE-D v3 DONE + BANKED (this session).** Delivered:
- **solver/decay_grading.py** — the decay-graded layer: the pure-convolution quadratic,
  the sharp weighted-algebra constant, the exact cosine coefficients of
  f_α = (1+X²)^(−α/2) = |cos(θ/2)|^α (stable two-term recursion; no Γ of a negative
  argument), and the far-field solution operator between decay-graded sup norms
  (2nd-order trapezoid in τ=log X, M-matrix ⇒ induced norm in ONE pass).
  **test_decay_grading.py 7/7**, every gate against an independent oracle. Suite now
  **10 files green**.
- **experiments/p2_route_d_v3_spaces.py** (deterministic, NON-logged) →
  writeup/data/p2_route_d_v3_spaces.json → fig21
  (writeup/4_p2_lottery/p2_route_d_v3_evidence.py). Six results:
  * **S1 the identity:** Q(h)=hH(h)=½Σ_m(Σ_{j+k=m}h_jh_k)sin mθ — a PURE convolution
    (Hardy: 2hH(h)=Im[(h+iHh)²]). Independent second build agrees to 3.2e-17.
    ⇒ sharp constant: bounded quadratic ⟺ S=sup v_{j+k}/(u_ju_k)<∞, S/4≤M≤S/2;
    unweighted M=½, **2× sharper than the Wiener constant v2 used**.
  * **S2 the price:** v_m^min(u)=‖Ae_m‖_{ℓ¹_u}; v_m^min/(m u_m) = O(1) (1.3–3.2) for
    s∈[0,2]. Exactly one mode power, weighted domains included.
  * **S3 THE NO-GO + THE CONSERVATION LAW:** k=0 in S gives v_m/u_m ≤ S·u_0 BOUNDED,
    while a bounded inverse needs v_m/u_m ≳ 2m. Measured over u=(1+k)^s, v=(1+m)^t:
    both requirements depend only on g=t−s, and **‖A_N‖~N^(1−g), S_K~K^g — exact
    complements. A certificate needs both exponents 0; the SUM is ≥1 everywhere
    (=1 on 0≤g≤1). Min over the entire family = 0.98.** Region I t≥s+1, region II
    t≤s, strip EMPTY; boundaries pinned grid-independently on the candidate lines.
  * **S4 the control:** (1+cosθ)→1 ⇒ boundary falls from t≥s+1 to t≥s−1 — **TWO
    powers**, exactly the order 1+cosθ vanishes to (healthy transport GAINS one,
    this one LOSES one). Min sum 0.98→0.00, overlap 0/9→9/9.
  * **S5 the resonance (both sides):** ‖L^{-1}‖ = **2/|α−2|** to ≤0.008% over 15 α;
    operator side lim X^{α+1}DF[f_α] = cα−1 to ≤0.3%. The pole at α=2 is BOTH the
    homogeneous far-field solution at c=½ AND the anchor's decay. **v2's "loses one
    power" IS this resonance seen at integer grading.** Window 1<α<2.
  * **S6 the pair that works:** decay-graded X={|h|≲X^−α}, Y={|g|≲X^−α−1}: every term
    lands in Y, **including the quadratic**, because H(h)→(∫h)/(πX) ⇒ hH(h) gains one
    power (verified vs ∫f_α=√πΓ((α−1)/2)/Γ(α/2), <0.1%). Price 2/(2−α) vs (∫f_α)/π ⇒
    **interior optimum α\*≈1.44** (3/2 within 1%), Z₂≈13.3, budget ≈1.9e-2.
    ⇒ certify X^−3/2 profiles with X^−5/2 residuals, NOT the anchor's own X^−2.
- **REFRAME worth keeping:** a diagonal weight measures SMOOTHNESS, not DECAY —
  cos kθ = (−1)^k at θ=π never decays, for any k. Decay lives in the ALTERNATING
  structure of the coefficient sequence. v2's repair was a category error, and the
  conservation law is what that error looks like when measured.


**P2 §13 — ROUTE-D v4 DONE + BANKED (this session, after v3).** Delivered:
- **solver/decay_collocation.py** — nodal spectral collocation on the midpoint θ-grid
  (X = tan(θ/2), far field reaches ~4J/π) with WEIGHTED SUP norms: the THIRD independent
  construction of this operator (v1/v2/v3 were all coefficient-space). H(cos kθ)=sin kθ,
  d/dθ and f_X=(1+cosθ)f_θ are all exact on the band-limited space, so DF is a dense J×J
  matrix with no quadrature. **test_decay_collocation.py 6/6**, gated against
  solver/nk_fourier (agreement 2.6e-13), the exact anchor and both kernel directions.
  Suite now **11 files green**.
- **experiments/p2_route_d_v4_graded.py** (deterministic, NON-logged) →
  writeup/data/p2_route_d_v4_graded.json → fig22. Six results:
  * **W1** the third build reproduces v2's negative + v3's repair: ungraded ‖A‖
    11.9→17.4 over J=125..2000 (+1.37/doubling, ~J^0.13, no sign of stopping), graded
    (α=3/2) 3.79→4.07 (~J^0.017, settling). NOTE: the sup-norm divergence is only
    LOGARITHMIC vs LINEAR (N^0.97) in v2's ℓ¹ — same verdict, gentler slope.
  * **W2 the core is cheap:** on α∈[1.4,1.7] the far-field law 2/|α−2| predicts the FULL
    gauged ‖A‖ to **6%** (2% on [1.5,1.7]). And the full ‖A‖ has its **own interior
    minimum at α≈1.40** — a second, independent argument landing where v3's budget
    optimum did. CAVEAT: the negative "core excess" at α≥1.8 is incomplete J-convergence,
    not a core effect.
  * **W3 THE MISSING HALF:** the decay-graded SUP pair does NOT control the quadratic —
    **H is unbounded on L^∞**. Shown with the conjugate-extremal family (degree-m Fourier
    partial sums of sign(cos θ): bounded ~1.18, ‖H p_m‖ ≥ (2/π)log m at the jump θ=π/2
    where both weights are O(1)): C_Q = 0.74→2.73 over m=4..512, **+0.41 per e-fold**.
  * **W4 the price, confirmed:** Z₂ = 2‖A‖C_Q = 13.6(α=1.4)/**13.4(1.5)** vs v3's
    far-field-only 13.3/13.4; C_Q matches (∫f_α)/π to <2% for α≥1.3. Budget **CEILING**
    1/(4Z₂) ≤ 1.9e-2 — assumes Z₁=0 and prices no smoothness component.
  * **W5 operational:** the gauge must replace a **CORE** collocation equation. Dropping
    rows at X=0.001/0.4/1.0 gives ‖A‖=4.03/4.41/5.70; dropping the OUTERMOST (X=1273)
    gives **1.06e5**. Gauge spread 1.7×, core-row spread 1.4× (modest, as v2 D3 found).
  * **W6 the Z₁-analogue, QUANTIFIED not bounded:** collocation truncation error
    6.6e-3→9.3e-5 (J^−2.08) at α=1.2, →2.6e-5 (J^−2.36) at 1.5, →4.3e-6 (J^−2.64) at 1.8.

**THE UNIFIED STATEMENT (v3 + v4 — carry this forward).** v3: a diagonal weight on
Fourier coefficients measures **smoothness**; we needed **decay**. v4: a weighted sup
norm measures **decay**; we also need **smoothness**. Two legs, two one-parameter
families, each missing exactly what the other has. The far-field transport forces a
decay grading; the Hilbert transform forces a smoothness scale; **the certificate's
space must carry BOTH at once and no one-parameter family does.** Four legs in, this is
the first time the requirement has been stated completely.


**P2 §14 — ROUTE-D v5 DONE + BANKED (this session, after v4).** Delivered:
- **solver/holder_norms.py** — the two-grading space
  ‖h‖_{α,γ} = sup w^(α)|h| + sup_{j≠k} min(w^(α−γ)) |Δh|/|Δθ|^γ, w^(β)=(1+X²)^{β/2}.
  **The seminorm weight is α−γ, NOT α, and it is FORCED** by the exact Jacobian
  dX/dθ=(1+X²)/2 (the γ is eaten by it); with weight α the profile f_α itself has
  INFINITE seminorm — the space would not contain the object the certificate is about.
  **The numerical conformal check caught this** (second time in three legs a cheap
  check has caught an algebra slip). PAYOFF: after the identity the whole weighted
  conformal seminorm is a PLAIN θ-Hölder seminorm with a diagonal weight — the
  compactification does the far-field bookkeeping for free, one O(J²) broadcast, which
  is the only reason the leg was cheap. **test_holder_norms.py 6/6**; suite **12 green**.
- **experiments/p2_route_d_v5_holder.py** (deterministic, NON-logged) →
  writeup/data/p2_route_d_v5_holder.json → fig23. Five results:
  * **U1 THE DEFUSAL:** v4's square-wave adversary — sup ratio ×2.26 over m=8..512 at
    EVERY γ (it does not care about the decay weight, exactly v4's diagnosis); Hölder
    ratio ×0.96 (γ=0.35), **×0.83 (γ=0.5)**, ×0.76 (γ=0.85). Defused for γ ≳ 0.35.
    In a Hölder norm the adversary pays for its own oscillation ([p_m]_γ ~ m^γ).
  * **U2 SMOOTHNESS HAS ITS OWN INTERIOR OPTIMUM:** C_H(γ) BOWLS — 1.60, 1.21, **1.12**,
    1.13, 1.18, 1.20, 1.29 over γ=0.15..0.85 — rising at both ends for DIFFERENT reasons
    (γ→0 is the sup norm where H is unbounded; γ→1 is Lipschitz where it fails again).
    **Same shape as decay** (v4: ‖A‖ bowls at α≈1.4). Two knobs, two interior optima,
    four unrelated mechanisms.
  * **U3c THE ONE MARGINAL DIRECTION:** residual f_{α+1+δ} at α=1.5, γ=0.5 — **δ=0 (the
    codomain's CRITICAL rate) creeps 1.956→2.879 over J=125..2000 (J^+0.14, a LOG), while
    δ=0.1/0.25/0.5/1.0 are FLAT TO 4 S.F. across a 16× range in J.** v3's resonance one
    level down; SAME FIX (keep the residual class OPEN). **This detuning is nearly FREE
    and the constants IMPROVE with δ** — unlike v3's 2/ε — because it TIGHTENS the
    codomain instead of LOOSENING the domain off its own kernel.
  * **U4 the quadratic:** adversary growth ×0.77 (γ=0.35) → ×0.11 (0.85); C_Q ≈ 0.86–1.14.
    v4's sup-pair value was 2.73 at m=512 and still climbing.
  * **U5 the joint optimum** (defused region γ≥0.35): (α,γ)=(1.8,0.35), ‖A‖=2.45,
    C_Q=0.67, **Z₂=3.29** (v4: 13.4), budget ceiling **7.6e-2** (v4: 1.9e-2) — ~4× better.
    FOUR asterisks: (i) ‖A‖ is FAMILY-RESTRICTED, a lower bound (the exact induced norm
    between polyhedral norms is an LP; no scipy) so the ceiling is an upper bound on an
    upper bound; (ii) C_Q likewise; (iii) Z₁ STILL unbounded; (iv) the argmax is at α=1.8,
    the EDGE of the swept grid, in a row with an unconverged-J artifact — the optimum's
    EXISTENCE is solid, its LOCATION is not.

**P2 §15 — ROUTE-D v6 DONE + BANKED (this session, after v5).** Delivered:
- **solver/nk_bounds.py** — the upper-bound layer. **test_nk_bounds.py 6/6**; suite now
  **13 files green**.
- **experiments/p2_route_d_v6_bounds.py** (deterministic, NON-logged) →
  writeup/data/p2_route_d_v6_bounds.json → fig24. Six results:
  * **THE FRAMING PROBLEM v1–v5 ALL SHARED (say it plainly):** every constant reported
    through v5 was a family-restricted maximum = a **LOWER** bound, and Z₁ was never
    bounded at all. A budget assembled from lower bounds is not a quantity a certificate
    can use. v6 fixes part of that and disqualifies the obvious method for the rest.
  * **B1 THE DISCRETE-BALL TRAP (the methodological headline).** Computing an induced
    norm by DUALITY over the DISCRETE unit ball is **UNSOUND**. A discrete Hölder
    seminorm only inspects pairs of GRID NODES, so duality's extremizer is a grid-scale
    sign pattern whose interpolant thrashes between them: continuum/discrete norm ratio
    **3.0e3 (J=125) → 5.0e4 (J=500), ~J^2.03**, vs **1.03** for a smooth control. The
    ‖A‖~J^0.5 it reported under THREE routes and EVERY gauge-row choice is **fiction**.
    Banked lesson (9) in MIRROR IMAGE: a family too SMALL under-reports (v4 missed the
    adversary), a ball too BIG over-reports (v6 invented one). Both are the instrument.
  * **B2 WHAT SURVIVES.** Use only inequalities the CONTINUUM norm implies:
    |g_m| ≤ ‖g‖/v_m and |g_m−g_{m₀}| ≤ ‖g‖/q_{m,m₀} ⇒
    ‖c‖_{Y*} ≤ min_{m₀}[|Σc_m|/v_{m₀} + Σ|c_m|/q_{m,m₀}] (`two_point_dual`; minimising
    over a SUBSET of m₀ stays valid). Domain **SUP part SATURATES: 5.536→5.631 over
    J=125..1600 (J^+0.006)** = the project's FIRST uniform upper bound on any part of
    ‖A‖, bracketing v5's family lower bound (~2.2–2.9) by ~2×. Domain SEMINORM part is
    valid but LOSSY (J^+0.496 = J^γ) — B1 says why (still pricing the fake direction).
  * **B3 EXACT MODELLING IDENTITY.** (DF−L)h = h/(X(1+X²)) − H(h)/(1+X²), where L is
    v3's far-field model −c h_X − h/X. Verified vs collocation to **1.5e-16 relative**.
  * **B4 THE FAR-FIELD Z₁ BOUND = the first bounded piece of Z₁ in six legs.** p.v. split
    at half-scale on the **EVEN kernel K(X,y)=2X/(X²−y²)**: singular half charged to the
    Hölder seminorm, rest to the decay envelope. X-side Hölder envelope
    2^γ(1+X_min²)^{−(α+γ)/2} — **weight α+γ, NOT α−γ** (v5's θ-weight pushed through
    |dθ|≤2|dX|/(1+X_min²)). The EVEN kernel is NOT cosmetic: the two-sided 1/(X−y) split
    DIVERGES as X→0 (truth is 0 by parity) and loses a factor 2 far out; even form is
    finite at 0 and SHARP (X·bound→1.681 vs M_α/π=1.669). Validated on RESOLVED nodes
    (|X|dθ≤1): X₀=20/50/100 → headroom 3.0×/1.7×/1.1×. Decays at the predicted X₀^{α−2}
    for every α. Same bound ⇒ **C_Q ≤ 3.13** at (1.5,0.5) (v5 family LB 0.86–1.14).
  * **B5 PRICING Z₁ KILLS v5's OPTIMUM.** At α=1.8, Z₁^far = **4.32/3.13/2.34** at
    X₀=200/800/3200 — all ≫ 1, no closure at any X₀, and dead STRUCTURALLY (the modelling
    error decays like X₀^{α−2}, so α=1.8 needs the far field 10⁵× further out, while
    ‖A‖=2/(2−α) runs toward the α=2 resonance). **New optimum α≈1.2, conditional budget
    Y₀^max = 1.18e-2.** CAREFUL: the a≈0.5 GA floor is ALSO ~1e-2 — that coincidence is
    **NOT** a claim the boundary profile could be certified. The budget is CONDITIONAL and
    OPTIMISTIC (far-field Z₁ only; far-field ‖A‖ validated by v4 only on α∈[1.4,1.7], NOT
    where the optimum now sits; three constants omitted). Honest reading: the target is no
    longer out of reach by ORDERS OF MAGNITUDE. That is all.
  * **B6 THE LEDGER.** EXACT: Y₀ (anchor). BOUNDED: Z₀; **Z₁ far-field modelling error
    (NEW)**; **‖A‖ domain sup part (NEW)**; **C_Q sup part (NEW)**. OPEN: ‖A‖ domain
    seminorm part; Z₁ core↔far coupling; Z₁ core discretization. **Three of eight moved.**

**P2 §16 — ROUTE-D v7 DONE + BANKED (this session, after v6).** Delivered:
- **solver/nk_seminorm.py** — the derivative-gain closure layer: the split |H(h)| bound
  (`hilbert_split_bound`), the interpolation inequality (`interp_T_bound`, closed-form
  optimal κ), the solved-for-derivative identity (`derivative_bound`) and the fixed-point
  `seminorm_closure` (monotone iteration; REFUSES α<1 rather than silently extending the
  one hypothesis it uses). **test_nk_seminorm.py 6/6**; suite now **14 files green**.
- **experiments/p2_route_d_v7_seminorm.py** (deterministic, NON-logged) →
  writeup/data/p2_route_d_v7_seminorm.json → fig25
  (writeup/4_p2_lottery/p2_route_d_v7_evidence.py). Six results:
  * **V1 WHERE THE J^γ ACTUALLY LIVES — and why v6's own recommendation was wrong.**
    v6's dual on the seminorm part, restricted to pairs with |Δθ| ≥ Δ for FIXED Δ:
    all 17.2→24.2→34.2 (**J^+0.494**); Δ=0.05 → J^+0.053; **Δ=0.1 → J^+0.018**. All the
    growth is on the NEAR DIAGONAL, so route (a) (band-limited subspace + faithfulness
    factor) is disqualified **STRUCTURALLY**: a faithfulness defect of the ball is a
    statement about admissible DIRECTIONS and cannot know whether two domain indices are
    adjacent — the J^γ does. What it is: ‖A_j·−A_k·‖_{Y*} priced ROW BY ROW, throwing away
    the near-cancellation of neighbouring rows of an inverse and then dividing by
    |Δθ|^γ~(π/J)^γ. **No dual functional recovers a cancellation that is a property of the
    EQUATION rather than of the rows.**
  * **V2 the split Hilbert bound (free).** v6 charged |H(h)| to the TOTAL norm; its own
    derivation already separates the payers. |H(h)| ≤ a_sup·S + a_semi·T, sum = v6's bound
    to 2.1e-16; weighted sups 1.031 / 1.277 vs v6's 1.928. **~30% on the closure**
    (T ≤ 93.5 → 63.6), up to 4.3× sharper pointwise.
  * **V3 THE CLOSURE (the estimate).** (P) `c h_X = −g − hX/(1+X²) − H(h)/(1+X²)`, an exact
    rearrangement (gate 1.9e-16) ⇒ a bound (D) on P = sup(1+X²)^{(α+1)/2}|h_X|. Split each
    pair at δ(θ₁)=κ(1+X₁²)^{−1/2} (a fixed multiple of the LOCAL X-scale): separated pairs
    pay 2Sκ^{−γ}, near pairs (1/2)Pκ^{1−γ}, **the weights cancel identically at every
    scale** ⇒ **T ≤ C(γ)(P/2)^γ(2S)^{1−γ}, C(γ)=(1−γ)^{γ−1}γ^{−γ}, C(½)=2 — NO J, NO GRID.**
    Gate: verified on 32 profiles × 4 (α,γ) incl. α=1, worst ratio 0.461. **WHY IT NEVER
    FAILS:** T ≤ F(T) with F concave/increasing/F(0)>0 ⇒ a UNIQUE fixed point and
    {T:T≤F(T)}=[0,T*]; the feedback is LINEAR in T (via |H(h)|), the gain SUBLINEAR (T^γ),
    so **no smallness condition for any γ<1** — and γ=1 becoming a real contraction
    condition is a **THIRD independent exclusion** of the Lipschitz endpoint (with v5 U2 and
    the classical unboundedness of H there). **NUMBER at (1.5,0.5):** T ≤ 63.6,
    **‖A‖ ≤ 69.1→70.3 over J=125..1600 (J^+0.0059, drift inherited ENTIRELY from v6's
    C_sup)** = **the first uniform upper bound on the WHOLE of ‖A‖.** Honest bracket:
    **0.85 ≤ (seminorm part) ≤ 63.6, a factor ~75 wide.**
  * **V4 the (α,γ) map made of UPPER bounds.** ‖A‖ alone falls monotonically as γ→0 (argmin
    at the grid edge γ=0.05 — a weaker domain norm is easier to bound), but **Z₂=2‖A‖C_Q
    BOWLS in both knobs: interior optimum (1.4,0.15), Z₂ ≤ 242.4** — the quadratic pays for
    exactly the weakness that makes ‖A‖ cheap. **First interior optimum in this project made
    entirely of upper bounds.** CAVEAT: still omits the codomain seminorm part of C_Q, which
    is unbounded and whose omission is worst exactly where γ is smallest ⇒ the LOCATION is
    provisional (again).
  * **V5 what the honest ‖A‖ costs.** v6 substituted the far-field 2/(2−α)≈2.5 for ‖A‖
    (validated by v4 W2 — but in SUP norms). In the Hölder norm the real bound is 10–20×
    larger. At γ=0.35, Z₁ ≤ 0.5 needs X₀~2e3 (α=1.2, J~1e3) … 3e4 (α=1.5, J~2e4 = 3.2e9
    dense entries, out of reach). **SURVIVABLE for α ≤ 1.4** (inside the existing dense
    collocation). **EXPENSIVE: budget 2.8e-3 → 2.0e-4**, from the GA floor's order to ~50×
    below it. **SECOND CONSECUTIVE leg where an upper bound cost an order of magnitude** ⇒
    **the constants must be roughly SHARP, not merely bounded** (three of four are lossy by
    ≥1 order, and the losses MULTIPLY inside Z₁, Z₂).
  * **V6 the interpolant is not in the space (a defect older than this leg).** A nodal vector
    on the midpoint grid is an even TRIG POLYNOMIAL in θ; it does not vanish at θ=π where
    w_α=sec^α(θ/2) diverges ⇒ **sup w_α|h| is INFINITE for the interpolant at every J.**
    Every discrete norm in v1…v7 is finite only because the midpoint grid stops half a step
    short of π. Measured on h=Ae_{J/2}: last node 8.4e-3→6.0e-4 over J=200..1600, but at
    θ=π−1e-6 it is 1.09e3→2.08e0; **h(π)~J^−3.01** — SOFT (converging to something that does
    live in the space) but a change of REPRESENTATION. **Repair: h=(1+X²)^{−α/2}p(θ)** with p
    a trig polynomial ⇒ weighted sup becomes a plain sup. The V3 closure is IMMUNE (a
    continuum statement about the true solution, which decays); the defect is in the
    HYPOTHESIS S ≤ C_sup, currently supported by grid measurements.
  * **V7 THE LEDGER.** EXACT: Y₀. BOUNDED: Z₀; Z₁ far-field modelling error (v6); ‖A‖ domain
    SUP part (v6); **‖A‖ domain SEMINORM part (NEW)**; C_Q sup part (v6). OPEN: Z₁ core↔far
    coupling; Z₁ core discretization (measured only); C_Q codomain SEMINORM part;
    **discrete↔continuum transfer (NEW)**. **Six of ten bounded**, and two of the four open
    items are new NAMES for things previously invisible rather than new problems.

**P2 §17 — ROUTE-D v8 DONE + BANKED (this session, after v7).** Delivered:
- **solver/hilbert_holder.py** — the weighted-Hölder-of-H layer: the per-pair increment
  majorant (`increment_pair_bound`), the shrinking near-region padding (`near_padding`),
  the pair sweep (`hilbert_holder_constant`, with an explicit per-pair ROUTE RULE), the
  payer-split C_Q sup part (`cq_sup_split`), the assembled quadratic constant
  (`quadratic_constant_full`, exact max of the quadratic form over the simplex), and
  **`decomposition_exact` — the same decomposition with the TRUE integrands**, which is
  what gates the majorant. **test_nk_hilbert_holder.py 6/6**; suite now **15 files green**.
- **experiments/p2_route_d_v8_quadratic.py** (deterministic, NON-logged) →
  writeup/data/p2_route_d_v8_quadratic.json → fig26
  (writeup/4_p2_lottery/p2_route_d_v8_evidence.py). Six results:
  * **X0 THE WEIGHT (get this right first).** Expanding the product increment about the
    INNER point: w_{α+1−γ}|ΔQ|/d^γ ≤ S·{w_{1−γ}|Δψ|/d^γ} + T·w_1(θ_i)B(θ_o). The second
    term is FREE (w increases in |θ| ⇒ w_1(θ_i)B(θ_o) ≤ sup w_1 B = v6's C_Q sup part).
    The first needs ψ=H(h)'s seminorm **with weight 1−γ, NOT α−γ**: **H does not inherit
    decay.** Third time in the series a weight exponent was the whole difficulty.
  * **X1 THE ESTIMATE + BOTH CONVERGENCES + THE ABLATION.** Work in t=φ−θ₁ so **nothing
    wraps**; N=[min(0,σ)−pd, max(0,σ)+pd]; majorize h's increments by whichever norm part
    is cheaper POINTWISE (rule independent of S,T ⇒ the bound stays LINEAR in (S,T)); keep
    the kernels EXACT (far difference as sin(σ/2)/(sin(t/2)sin((σ−t)/2)) preserves the O(d)
    cancellation); G closed-form (→2log(3/2)). **T_ψ ≤ 1.1936 S + 4.9410 T** at (1.5,0.5),
    flat to **4e-6** over a 4× pair-grid refinement and 4e-4 over 150→2400 quadrature
    points (a GRID sup can only UNDER-report — the mirror of v6's trap — so the refinement
    is a gate). **ABLATION: pointwise-only (all v6/v7 had) gives 1452 vs 6.13 — 237×.**
    Per-pair RULE matters: "smaller coefficient SUM" inflates b_sup 1.19→2.61; the choice
    must be ONE rule applied to both coefficients.
    **THE PADDING BUG:** the first draft restricted the estimate to d ≤ (π−θ_i)/6 — what
    the SCALING ARGUMENT needs — and the sweep came back **12× too large**, entirely from
    pairs just outside, where the crude fallback took over. The DECOMPOSITION only needs
    (1+p)d ≤ π. **Do not let the regime of an ARGUMENT become the regime of the CODE.**
  * **X2 THE SECOND BUILD.** A majorant of a WRONG decomposition is still a valid
    inequality about something, and no domination test notices. E_N+E_F+G rebuilt with the
    TRUE increments vs the exact conjugate (cos kθ→sin kθ): **5.6e-6** over 7 pairs × 3
    profiles. Caught two sign errors, one of them ALSO wrong in the module docstring.
  * **X3 THE BRACKET.** Measured (family ⇒ LOWER) vs bound over 10 profiles at four (α,γ):
    worst ratio **0.222–0.246** — valid, **~4× lossy**, the same order of slack v7 carried.
  * **X4 THE γ STRUCTURE — v7's PREDICTION IS BACKWARDS.** b_semi 18.6 (γ=0.05) → 4.94
    (0.5) → 7.16 (0.9): both endpoint divergences present, C_Q complete BOWLS (min 3.330 at
    γ=0.65). But the RATIO complete/sup-only is **1.001 at γ=0.05, 1.09 at 0.35, 1.28 at
    0.9** — worst at the OPPOSITE end from v7's prediction, because **v6's sup-only C_Q
    already carried the same 1/γ near-region divergence.**
  * **X5 THE FIRST COMPLETE Z₂ MAP.** ‖A‖ = v6 dual + v7 closure; C_Q = v6 sup part (split
    by payer) + v8 seminorm part. **Every constant an upper bound, NOTHING omitted.**
    Optimum **(1.4, 0.15), Z₂ ≤ 261.1** vs v7's incomplete 242.4 at the SAME point ⇒ v7's
    provisional location HOLDS.
  * **X6 THE BUDGET + THE TREND.** At the optimum, Z₁ ≤ 0.5 needs X₀=3.2e3 (J~2.5e3,
    6.2e6 dense entries — in reach). **7.6e-2 → 1.18e-2 → 2.58e-4 → 2.39e-4.** (v7's
    writeup quoted 2.0e-4 = its γ=0.35 row; 2.58e-4 is v7's map over the same sweep, the
    like-for-like number.) Three order-of-magnitude losses, then **7%**.
  * **X7 THE LEDGER.** EXACT: Y₀. BOUNDED: Z₀; Z₁ far-field (v6); ‖A‖ sup (v6); ‖A‖
    seminorm (v7); C_Q sup (v6, sharpened v7/v8); **C_Q codomain seminorm (NEW)**. OPEN:
    Z₁ core↔far coupling; Z₁ core discretization (measured only); discrete↔continuum
    transfer (v7). **Seven of ten; Z₂ COMPLETE.**

**P2 §18 — ROUTE-D v9 DONE + BANKED (this session, after v8).** Delivered:
- **solver/hilbert_pointwise.py** — the pointwise |H(h)| layer on the exact folded kernel:
  `pointwise_bound` (offset-parameterised so sin((φ−θ)/2)=sin(±s/2) is exact — the naive
  cos-difference form NaNs at X≳1e4), `pointwise_curves` (drop-in for v7's `curves=`),
  `weighted_sups`, `sweep_rho` (the payer rule), `measured_pointwise` (the other side of the
  bracket). **test_nk_hilbert_pointwise.py 6/6**; suite now **16 files green**.
- **experiments/p2_route_d_v9_sharpen.py** (deterministic, NON-logged) →
  writeup/data/p2_route_d_v9_sharpen.json → fig27
  (writeup/4_p2_lottery/p2_route_d_v9_evidence.py). Six results:
  * **Y1 THE BOUND.** K_θ(φ) = 2sinθ/(cosφ−cosθ): (i) the far-field decay is IN the kernel
    (sinθ→0); (ii) **p.v.∫_0^π K dφ = 0 exactly** (the conjugate of the constant function;
    antiderivative −2log|sin((φ−θ)/2)/sin((φ+θ)/2)| vanishes at BOTH ends) ⇒ one GLOBAL
    subtraction replaces v6's band + matching scale + remainder, each of which cost a
    constant. Ratio to v6 over 8 decades of X: **0.09/0.26/0.66/0.87/0.65/0.67/0.85/0.95/0.99**.
    Second build vs the exact conjugate: **1.5e-7**. Nearly ATTAINED: 0.97 on the anchor.
  * **Y2 THE PAYER RULE (the transferable lesson).** Any FIXED rule is valid; v8's default
    compared the two routes at S=T=1. **Tune the rule to the T/S ratio of the ANSWER.** With
    ρ: ‖A‖ = 74.7(1)/63.4(2)/53.1(3)/48.4(4.5)/**47.2(6–9)**/50.6(25)/54.0(50) — an INTERIOR
    optimum, and **the neutral ρ=1 (74.7) is WORSE than the crude bound it replaces (69.4)**.
    C_Q wants ρ≈2 instead (it maximises over the simplex, ratio O(1)). Both valid.
  * **Y3 THE NEW ‖A‖:** 69.15 → **47.05** at (1.5,0.5), J-flat (J^+0.0059).
  * **Y4 THE GAIN DOES NOT TRANSFER — the leg's actual result.** Reduction by point:
    **32% (1.5,0.50) / 11% (1.4,0.35) / 3% (1.4,0.25) / 0% (1.4,0.15) / −1% (1.2,0.15)**, and
    **(1.4,0.15) is the map's optimum**, unchanged for three legs. MECHANISM: the |H| bound
    enters the closure T ≤ C(γ)(P/2)^γ(2S)^{1−γ} **only through P**, so at γ=0.15 a 30% better
    P moves T by 4%. And the optimum sits at small γ **because** that is where ‖A‖ barely
    depends on this input — the optimiser had already walked to the corner where the
    improvement cannot matter.
  * **Y5 THE ELASTICITY TABLE.** d log‖A‖/d log C_sup = **+0.98** (reference) / **+1.00**
    (operating); d log‖A‖/d log|H| = +0.46 / **+0.11**. ‖A‖ is PROPORTIONAL to C_sup and at
    the operating point blind to the |H| bound. **The last TWO legs both worked on inputs with
    elasticity ≤ 0.5 and both moved the budget ≤ 7%.**
  * **Y6 THE TRAP (banked lesson 15, missed AGAIN).** Substituting a "measured" C_sup reported
    a **19× available gain — an artifact**: that number was a family lower bound computed by
    dividing the SUP PART of an image by the FULL codomain norm of a sign pattern. Survives:
    ~2× is plausibly available from C_sup (v6 B2's own bracket); the wider bracket (47× vs a
    family LB ~1.0) **cannot be attributed at all** without a decent LOWER bound.
  * **Y7 MAP + BUDGET.** Complete Z₂ map with ρ chosen per cell: optimum **(1.4,0.15),
    Z₂ ≤ 260.7** (v8: 261.1). Budget **7.6e-2 → 1.18e-2 → 2.58e-4 → 2.39e-4 → 2.40e-4**:
    three order-of-magnitude losses, then three legs of nothing in either direction.

**P2 §19 — ROUTE-D v10 DONE + BANKED (this session, after v9).** Delivered:
- **solver/op_lower.py** — the adversary layer: `sign_pattern_lower` (the old baseline, kept
  as the control), `smooth_family` (1/v × slowly varying shapes), `family_lower`, `ascend`
  (random ascent in a smooth cosine basis) and `best_lower`. **test_op_lower.py 6/6**; suite
  **17 files green**.
- **experiments/p2_route_d_v10_lower.py** (deterministic, NON-logged) →
  writeup/data/p2_route_d_v10_lower.json → fig28. Six results:
  * **W0 WHY SIGN PATTERNS FAIL + THE TELL.** g = sign(A_i·)/v is the exact extremizer of the
    SUP-TO-SUP problem; here its Hölder seminorm is enormous, so dividing by the full codomain
    norm discards everything the numerator gained. **THE TELL: the baseline gets WORSE with J
    (0.973 → 0.921 over J=200..800).** Six legs quoted it; nobody plotted it against J.
  * **W1 THE CONSTRUCTION.** Finite codomain norm ⇒ decay ≥ 1/v = cos^{α+1}(θ/2) AND no
    oscillation ⇒ the family is 1/v × slowly varying. **Validity is FREE** (any g bounds below),
    so the whole problem is CONSTRUCTION. Reference (1.5,0.5) J=400: **0.942 → 2.884**, bracket
    **50× → 16×**. Random ascent from the best adds **1.000×** — reported, because a flat
    maximum is information about the problem's shape.
  * **W2 THE BRACKET THAT MATTERS.** At the OPERATING point (1.4,0.15): **2.74 ≤ ‖A‖ ≤ 20.94,
    a factor 7.7.** Quoting the REFERENCE point's bracket was a second, quieter version of the
    same mistake.
  * **W3 THE EXTREMIZER:** a **wide far-field bump** (θ=3.12 ⇒ X≈93, width 0.5), with its
    neighbours next and nothing oscillatory close. Same place as v2's far-field degeneracy,
    v3's resonance, v6's X₀ — an independent check that the number is about the problem.
  * **W4 ACROSS THE MAP:** 10.7×/**8.2×**/14.2×/16.2×/10.8×/10.4× — 8–16× everywhere,
    **tightest at the optimum**, worst where the closure leans hardest on the interpolation
    inequality (large γ).
  * **W5 THE MEASURED CEILING (the point of the leg).** A PERFECT ‖A‖ bound multiplies the
    budget by the bracket and no more: **2.45e-4 → 1.88e-3**, vs the GA floor 1e-2. **~5× short,
    not 40×** — and **not enough alone**: it would also need C_Q's ~4× (v8 X2), and the two
    together only just reach the floor with nothing spare for the three open Z₁ items. Caveats:
    the true norm is somewhere INSIDE the bracket, so 7.7× over-estimates the achievable gain;
    the lower bound is still a finite family; the budget is still CONDITIONAL.

**IS THIS STILL THE RIGHT LANE? (v12 REPLACED THE QUESTION; v14 ANSWERED IT — read this box
before choosing anything.)** Through v10 the box was an arithmetic problem: budget 2.45e-4, GA floor ~1e-2, a
perfect ‖A‖ worth ≤7.7×, C_Q's slack ~4×, three unpriced Z₁ items — i.e. even perfect
sharpening only just reached the floor with no headroom. v11 removed the floor (Newton, twelve
orders). **v12 removed the arithmetic**: the a>0 profile ends at X_c ≈ e^{c/a}, so
  * every constant in that arithmetic was priced at the a=0 ANCHOR, where the object has an
    X^−2 tail and the decay grading makes sense;
  * at the profile the certificate is actually about, **‖A‖ DIVERGES with J (J^+2.86) while the
    anchor's is flat (J^−0.003)** — the approximate inverse does not exist in the limit;
  * the codomain norm's far-field weight amplifies exactly the Gibbs ringing that a global
    spectral basis leaves where a compactly supported profile is zero, so Y₀ measured there is
    large and, at a=0.4, does not converge at all over a 16× refinement.
**v14 ANSWERED IT, and the answer moves the box rather than repeating it.** The repair v12/v13
named is built, gated and run: on [0, X_c] via the first integral, ‖A‖ is FLAT in K (and flat
under the same decay grading, which it must be on a compact interval) against the whole line's
J^+2.80 measured with the same code. So:
  * **"mis-specified" is discharged.** The approximate inverse exists in the continuum limit at
    the a>0 profile the certificate is actually about, which is the thing three legs could not
    say.
  * **the remaining work is SMALLER than what it replaces.** v3's resonance, v6's tail bound,
    v7–v9's estimates and v10's bracket were all about a far field that no longer exists in the
    formulation. Nothing of them carries over, and nothing of them is needed.
  * **the arithmetic is GONE, not fixed.** Do not quote the old budget history (7.6e-2 → …
    → 2.40e-4) as if it applied: every number in it is the anchor's, in a space the project no
    longer uses. There is currently NO budget in the reduced space — not a bad one, none.
**v15 THEN RE-PRICED THE ANSWER — and this is the current state of the box.** The literature
check (done, one hour, §24) says the technique is routine in this family and the object's
existence appears already proved. So the question is no longer "does the lane work" — v14
showed it does — but **"is the lane worth walking when someone else has already walked it".**
**The three calls, re-answered AGAIN:**
  (a) **Finish one certificate end-to-end in the reduced space** (Y₀, Z₀, Z₁, Z₂ at one a, then
      the radii polynomial in float). **Still worth doing, DEMOTED to what it always was: a
      CAPABILITY, not a result.** Cheap now. Do it in a chunk, not a campaign.
  (b) **VERIFY THE TWO LOAD-BEARING READINGS** — the a-sign in arXiv:2603.25104 (is the
      two-scale scenario a ≤ 0 territory?) and whether its fixed point is v14's first integral.
      **Needs a PDF. The binding constraint here is ACCESS, not compute** — flag it to the user
      rather than routing around it. **HIGHEST VALUE PER HOUR IF IT CAN BE DONE AT ALL**,
      because it bears on whether the a>0 two-scale object is the right object.
  (c) **THE DSS LANE — the swing.** Promoted from standing item (1). Discretely self-similar =
      a periodic orbit of the rescaled flow = a global search problem = the one thing this
      project's tooling (GA + Newton) is genuinely good at, and the one class
      Nečas–Růžička–Šverák/Tsai leaves open for NS relevance. **Caveat that must travel with
      it: "uncrowded" rests on not finding search hits, which is the weakest inference in §24.**
**Recommendation: (b) if access allows, then (c) as the swing, with (a) as a one-chunk
capability build whenever it is convenient. Do NOT run another whole-line estimate leg. The
stopping rule is unchanged — if the float budget does not close with margin, say so; never
harden.**

**THE RECOMMENDED NEXT BRICKS — v15 REORDERED THEM. Read this list first:**
  (0a) **VERIFY arXiv:2603.25104 AND arXiv:2305.05895.** The a-sign question (is the two-scale
       scenario a ≤ 0?) and whether their fixed point is v14's first integral. Blocked on PDF
       access in this container — **tell the user it is blocked rather than quietly skipping
       it**; a human or a session with arXiv reachable can settle both in twenty minutes.
  (0b) **THE DSS LANE** (standing worthwhile-item (1)) — the swing, now that L1 is occupied.
  (0c) The certificate below, demoted to a **one-chunk capability build**.
Everything after this line is the v14 ordering, kept because the technical build notes in (1)
are still exactly right for whoever does the capability build:
  (1) **THE WHOLE CERTIFICATE, IN THE REDUCED SPACE, AT ONE a — and stop at the float
      rehearsal.** This is standing item (4) ("finish one certificate end-to-end"), promoted
      because v14 made it cheap. Work at a=0.3 (K=64 is converged to 3.7e-13; a=0.2 needs
      K≳X_c/c=34 for the core layer). The four things, in this order:
        • **Y₀** = ‖A F(x̄)‖ — the defect of the INTERPOLANT of the reduced solution, not of
          the nodal vector. The same distinction that made v12 worth running applies here:
          Newton zeroes the residual at the K nodes, and the certificate asks about the
          function. `ReducedProfile.residual` is already evaluable at arbitrary v, so this is
          a sup over a fine off-node grid, not a new build.
        • **Z₀** = ‖I − A DF‖ — should be ~machine, since A is built from the same DF.
        • **Z₁, Z₂** — and note what is NOT needed: no decay grading, no resonance, no tail
          bound, no matching radius X₀, no Hölder seminorm on an unbounded domain. The
          quadratic term is Hpv[·] of a product on a COMPACT interval, where every weight is
          equivalent to 1. The nonlinearity is e ↦ e^{1/a}, whose derivatives are bounded on
          any interval where e is bounded away from... **except at v=1, where e→0 and
          e^{1/a−1} is unbounded for a>1; for a<1 it vanishes, so a<1 is the good case and
          that had better be stated as a hypothesis rather than discovered.**
        • Then the radii polynomial in FLOAT. **STOPPING RULE, unchanged and load-bearing: if
          it does not close with margin, STOP and report it. Do not harden.**
  (2) **THE STRUCTURE AS A RESULT (partly delivered, worth finishing).** v14 measured the
      radius law with the profile's own (m, U₀) — 0.3% at a=0.2 degrading to 11% at a=1, with
      the error attributed. Still open and cheap: whether the same first integral exists for
      the HL model (the reduction only used E_X = a H(Ω), so the question is whether HL's
      transport coefficient has the same property); and what the C^{1/a} edge regularity —
      a CORNER exactly at De Gregorio, a=1 — means, if anything. **Do the literature check
      before writing either up as novel.**
  (3) **THE LITERATURE SEARCH, promoted.** It now blocks v14's headline as well as the three
      methodological candidates. Cheapest item on the list and the only one that converts any
      of this into a claim.
  (4) Retired by v14, do NOT spend a leg on them: C_sup's two-point dual; the core↔far
      commutator; the ansatz change h=(1+X²)^{−α/2}p(θ); anything else whose subject is the
      far field of a formulation the project no longer uses.
ONLY when Y₀, Z₀, Z₁, Z₂ are ALL real upper bounds AT THE PROFILE BEING CERTIFIED should the
float radii polynomial be assembled, and the same stopping rule applies: **if it does not close
in float with margin, STOP, do not harden.** solver/interval.py has existed since v1 and has
still never been pointed at any of this — correctly, because nothing has closed in float.

SUPERSEDED (kept for the record) — the v14 spec, which this session executed: **"REMOVE THE FAR
FIELD FROM THE DOMAIN. Pose the problem on [0, X_c] with X_c an UNKNOWN and perturbations
supported there. KILL SWITCH, run it FIRST; flat ⇒ the framing is repaired."** Outcome: **right
on every count, including the predicted verdict** — the first spec in this series that was. Two
things it got wrong in a way worth keeping: (i) it prescribed the ANSATZ Ω = (1−y²)^{1/a}q(y),
"the zero order is known exactly, so put it in rather than resolving it" — and the first
integral makes the order an OUTPUT, which is strictly better because nothing has to be known in
advance; (ii) it framed the leg as a BUILD, and the build turned out to be two lines of algebra
that thirteen legs had walked past. Lesson: **a spec that says "discretize X on domain Y" should
first ask whether X integrates.** Also worth keeping: v13 named the repair from a MECHANISM
(a mode that grows in the far field ⇒ remove the far field), and the mechanism was right even
though the repair's implementation was not the one it imagined. A correct diagnosis survives a
wrong prescription.

SUPERSEDED (kept for the record) — the v13 spec: **"the kill
switch: build the free-boundary system and measure ‖A‖ vs J; the singular mode s^{−1/a} is
precisely ∂/∂X_c of the solution family, so the free boundary should absorb it."** Outcome: the
spec's REASON was wrong twice over — there is no s^{−1/a} mode (dropped sign), and the cheap
version of the repair (border with c) is disqualified because dilation is a symmetry. v13
therefore spent itself on diagnosis instead of the build, and the build is still the next
brick — with a better justification (the obstruction is a growing FAR-FIELD mode, so what
matters is that [0,X_c] has no far field, not that X_c is an unknown). **Lesson for writing
the next spec: a spec that carries a MECHANISM should carry the mechanism's own gate. v12's
measurements were gated six ways and its explanatory sentence was gated not at all.**

SUPERSEDED (kept for the record) — the v12 spec, which this session executed: **"carry the
Newton profile into the θ-collocation basis the bounds live in and measure Y₀ THERE (the v11
number is in the Route-A ρ-discretization; they are different objects)."** Outcome: the task was
right and the MOTIVE was too small. The spec expected a number; what the carry-over produced was
a change of subject, because measuring in the right basis is also the first time anyone had
looked at the a>0 profile's far field with an instrument that could see it. Worth remembering:
**"measure X in the right place" specs are cheap and they are how mis-specifications surface —
the reason to run one is not the number it returns.** Also banked: the spec's own framing
("Y₀ is DISCRETIZATION-limited") was wrong in an instructive way — the discretization was fine;
the SPACE was wrong.

SUPERSEDED (kept for the record) — the v10 spec, which this session executed: **"a REAL LOWER
BOUND on ‖A‖ — do this FIRST; without one, no bracket in this project can be attributed."**
Outcome: correct, and cheaper than expected — the construction is a parametric family plus a
ratio, no LP needed, and the ascent that was supposed to be the hard part adds nothing. The
spec's guess that an LP would be required was wrong for a reason worth keeping: **when
validity is free, the problem is construction, not optimisation.**

SUPERSEDED (kept for the record) — the v9 spec: **"SHARPEN ‖A‖
(the highest-value leg available): v7 routes the whole seminorm through one interpolation
inequality with a single global κ, and the measured ratio says that is ~75× lossy."**
Outcome: the sharpening worked (−32% at the reference point) and bought **nothing** at the
operating point, for a reason the spec could have found in one minute with an elasticity
table. The spec's premise — "the ~75× bracket means ~75× is available" — was also wrong, and
wrong in the specific way v9 then re-derived the hard way: **a bracket whose lower end is a
family maximum bounds the available gain from above and says nothing else.** Two lessons for
writing the next spec: price the ELASTICITY before choosing the target, and never read an
available gain off a bracket whose lower end you have not earned.

SUPERSEDED (kept for the record) — the v8 spec: **"the C_Q
codomain seminorm part — weighted Hölder boundedness of H with an explicit constant; it is
the one term that would make the V4 map's optimum LOCATION trustworthy."** Outcome: the
bound worked and the location IS now trustworthy — but the reason the spec gave for
doubting it (the omission is worst at small γ) was **wrong in direction**, and the leg's
real content turned out to be the budget trend, not the location. Worth remembering: a
spec's stated MOTIVE can be wrong while its recommended TASK is still the right one.

SUPERSEDED (kept for the record) — the v7 spec: **"do route
(a) first — restrict to a band-limited subspace where the discrete norm IS faithful, with a
quantified faithfulness factor; keep the analytic C^{1,γ} gain in reserve."** Outcome: route
(a) was aimed at the WRONG MECHANISM and a ten-minute diagnostic (V1) disqualified it;
route (b), the reserve, is what closed the bound. The spec was written by reasoning from the
PREVIOUS leg's headline finding (the discrete-ball trap) by analogy, and the analogy was
false — the J^γ was a near-diagonal pricing artifact, not a ball-faithfulness defect. Worth
remembering when writing the next spec: **the freshest lesson is the most tempting analogy.**

SUPERSEDED (kept for the record) — the v6 spec:
**bound Z₁ from the closed-form far field, and turn the family-restricted operator norms
into genuine upper bounds analytically ("the far field has a closed-form inverse and the
core is finite-dimensional, so an LP is not actually needed").** Outcome: the Z₁ half
worked (§15 B3/B4); the operator-norm half was HALF RIGHT AND HALF A TRAP — an LP is
indeed not needed for the sup part (the two-point dual saturates), but the route it
suggested, duality over the discrete ball, is unsound and the seminorm part is still open.
The prediction "an LP is not actually needed" was right for the wrong reason and wrong for
the rest; worth remembering when writing the next spec.

Alternative lanes (put these in the menu): (a) the separate coupled-system HL two-stage
leg (whether an HL-type two-stage appears at any scalar gCLM member or genuinely needs
the coupled (ω,θ) system) — the biggest genuinely-novel swing left; (b) extend the
a_p(K) map to the odd/one-scale channel (lower value — refines a Level-1 map); (c) write
up the whole P2 arc as a single coherent community piece (the 1D gCLM two-scale story +
the three-part Route-D negative) rather than building further.

ENVIRONMENT & WORKFLOW: .venv/bin/python (numpy + matplotlib; NO scipy —
tridiag/solvers/3×3/GA/Hilbert/interval-arith/Fourier-operator/decay-grading/collocation
all hand-rolled). 8-worker ceiling (OMP_NUM_THREADS=8 pinned). No pytest; run each suite as
`python test_X.py`. Suites (all 22 green): test_interval.py (5/5) + test_nk_fourier.py
(6/6) + test_decay_grading.py (7/7) + test_decay_collocation.py (6/6) +
test_holder_norms.py (6/6) + test_nk_bounds.py (6/6) + test_nk_seminorm.py (6/6) +
test_nk_hilbert_holder.py (6/6) + test_nk_hilbert_pointwise.py (6/6) +
test_op_lower.py (6/6) + test_profile_newton.py (6/6) +
test_collocation_newton.py (6/6, ~3 s) +
test_turning_point.py (6/6, ~13 s) +
test_first_integral.py (11/11, ~90 s) +
**test_reduced_certificate.py (16/16, NEW — ~3 min)** +
test_gclm_family.py (12/12) +
test_hl_rescaled.py (9/9) + test_line_hilbert.py (6/6) + test_gclm_rescaled.py (5/5) +
test_boussinesq_{velocity,transport,rescaled}.py (5/5,5/5,8/8). Scripts under
experiments/ need the `sys.path.insert(0, dirname(dirname(abspath(__file__))))`
bootstrap. Before ANY logged experimental run: pass the test gate + COMMIT + LOCK the
predicate in git (dirty-tree guard; gitignored experiments/\*.{log,npz,jsonl,out} fine).
Solver dev + unit tests + DETERMINISTIC scoping probes are NOT "logged gate runs" (all
three Route-D probes are deterministic — no predicate lock needed); still add each new
solver test to the suite. Papers/ gitignored ([HQW25]=arXiv:2401.14615 →
Papers/hqw25.txt). One JOURNAL.md entry per logged experiment (deterministic tooling
probes get a clearly-labelled non-logged entry too, as §10–§20 did).

**WRITEUP STRUCTURE:** evidence rebuilds (each reads committed writeup/data/\*.json):
writeup/4_p2_lottery/{**p2_route_d_v16_evidence.py(fig33)**, p2_route_d_v14_evidence.py(fig32),
p2_route_d_v13_evidence.py(fig31),
(v15 has NO evidence script and NO figure — no measurement; its data is
writeup/data/p2_literature_scope.json, read directly),
p2_route_d_v12_evidence.py(fig30),
p2_route_d_v11_evidence.py(fig29),
p2_route_d_v10_evidence.py(fig28), p2_route_d_v9_evidence.py(fig27),
p2_route_d_v8_evidence.py(fig26),
p2_route_d_v7_evidence.py(fig25),
p2_route_d_v6_evidence.py(fig24),
p2_route_d_v5_evidence.py(fig23),
p2_route_d_v4_evidence.py(fig22),
p2_route_d_v3_evidence.py(fig21),
p2_route_d_dress_evidence.py
(fig20), p2_route_d_evidence.py(fig19), p2_two_scale_kladder_evidence.py(fig18),
p2_two_scale_sweep_evidence.py(fig17), p2_ga_framework_evidence.py(fig16),
p2_scenario2_evidence.py(fig15), p2_regular_profile_evidence.py(fig14),
p2_conj24_evidence.py(fig13), p2_hl_anchor_evidence.py(fig12)};
writeup/3_spikes/{spike0,spike1_stepA/B/C}\_evidence.py; central
writeup/build_figures.py (figs 1–7). writeup/README.md is the ordered index.

OPS: DISK WATCH — root fs has hit 100% mid-session before; `df -h /` if writes fail with
ENOSPC. Never `pgrep -f script.py` while it self-matches (hang). Foreground `sleep`
blocked (use background runs / Monitor until-loop). The GA at the converged budget
(pop150/gen250/8seeds) ≈ 30–45 s/best_of at n=801; base-budget GA ≈ 1 s. Route-D v1
probe ~10 s; v2 dress ladder a few seconds; v3 space sweep ~1 min; **v4 collocation sweep
~10 min (dense J×J inverses at J up to 2000 — do NOT build a Collocation at J≳5000, the
matrices are J² and 40000 would be 12 GB); v5 Hölder sweep ~10 min (HolderNorm caches a
J×J pair matrix — same J² ceiling); v6 bounds ladder ~10 min (the SEMINORM-part dual is
O(J³) and is capped at J≤1000 for that reason — the sup-part dual is only O(J²) and is
cheap); v7 seminorm ladder ~15 min — the closure itself is O(1); the cost is v6's C_sup
dual at each J plus the (α,γ) map; **v8 quadratic sweep ~12 min — one pair bound is ~1 ms
(three log-graded quadratures), a full (α,γ) point ~2 s, and the map re-uses a cache;
test_nk_hilbert_holder ~4 min; **v9 sharpen sweep ~35 min — one pointwise bound is ~1 ms,
a (α,γ) cell costs 4 ρ-values, and the map is 64 cells; test_nk_hilbert_pointwise ~6 min; **v10 lower-bound sweep ~20 min — the family is ~2000
candidates x a J-sized matvec plus an O(J^2) seminorm each, so it scales like J^2;
test_op_lower ~8 min; **v14 first-integral experiment ~6 min, dominated by the
whole-line CONTROL (dense J=800 Newton + inverse); the reduced solve itself is milliseconds —
a K=192 Newton is 5-10 steps on a 193x193 system, so the a-sweeps are essentially free**).**
Run `python -u` to a
LOGFILE, wait on a Monitor until-loop — do NOT pipe through tail. Reuse solver instances.

DISCIPLINE LESSONS BANKED (do not relearn): Ground the scheme in the paper; DERIVE the
exact answer where one exists and gate against it. Make the fitness/observable
scale-/gauge-invariant or the optimizer games it. Report gauge/genome/budget/basis
invariants and upper-bound caveats, never a sharp claim a fixed genome/budget can't
support (the T4 lesson). Near-transition GA floors are SEARCH-limited at low budget.
Fixed-grid dynamic-relaxation FLOORS the residual (~1e-2). **From §11:** (1) do the
cheap float rehearsal BEFORE hardening; (2) ABLATE to attribute — build the control;
(3) build the same object twice (that is how the k=0 fold bug surfaced); (4) a negative
with a mechanism is a result — chase the mechanism until it predicts a NUMBER, then let
it tell you what to build next. **NEW from §12 — four more that earned their keep:**
(5) **When a leg hands you a repair WITH a condition attached, discharge the condition
FIRST, on paper.** §11 wrote its own gating check and it took an afternoon; skipping it
would have cost a whole two-region solver build. (6) **Look for the conserved
quantity.** "The repair fails" is an anecdote; "the two exponents sum to ≥1 over the
entire family, and the weights only choose which one pays" is a theorem — and it came
from plotting both requirements on one axis. (7) **Check that your instrument can
measure the thing you are asking about.** Diagonal weights measure smoothness; we were
asking about decay. Whole categories of failure are category errors wearing a numerical
costume. (8) **Widen the sweep past where you expect the answer.** The control's
boundary was first reported as t=s because the t-grid started at 0; extending it to
negative t revealed t=s−1, i.e. TWO powers — which is the order the symbol vanishes to
and the check that confirmed the whole picture. **NEW from §13:** (9) **Sampling cannot
establish boundedness, and it cannot reveal unboundedness — BUILD THE ADVERSARY.** The
first version of v4's quadratic test used random perturbations of increasing degree;
they FELL (1.40→0.84) and reported the quadratic as comfortably bounded. The truth
needed the textbook extremal construction (square-wave partial sums), which gives
+0.41 per e-fold. The bad direction is a measure-zero cusp in the ball; you never
stumble onto it, and random search will happily confirm what you want to be true.
(10) **When a cheap model survives contact with the full object, that is a licence —
use it.** v3's far-field law predicted the full operator's inverse norm to 6%. That
makes the far-field analysis a trustworthy instrument for the next leg, and it is worth
saying so explicitly rather than re-deriving everything from scratch each time.
**NEW from §14:** (11) **Write the consistency check for the change of variables, always.**
v5's seminorm weight was wrong by a whole exponent (α instead of α−γ) and the failure mode
was silent-but-fatal: the space would not have contained the profile it was built for. The
numerical conformal check caught it in seconds. Two of the last three legs were saved this
way. (12) **When two measurements of the same thing disagree, the disagreement IS the
result — isolate which input each one is responding to.** v5's coarse sweep said J^0.14,
the focused ladder said saturating; both were right about their own test directions, and
separating them found the critical-rate marginality. (13) **Detuning a requirement on the
RESIDUAL is cheap; detuning the class of SOLUTIONS is expensive.** v3's domain-side
detuning cost 2/ε because it moved the domain off its own kernel; v5's codomain-side
detuning is free and the constants IMPROVE with it. Check which side a marginality lives on
before pricing it. **NEW from §15:** (14) **A too-BIG ball lies exactly as loudly as a
too-SMALL family.** Lesson (9) said to build the adversary because sampling under-reports.
v6 is the mirror: duality over a DISCRETE Hölder ball reported ‖A‖~J^0.5 under three
independent routes and every gauge choice, and it was fiction — the extremizer it picked
was inflated ~J² in the continuum norm. Before trusting any number about an operator, CHECK
THAT THE SET YOU OPTIMISED OVER IS THE SET YOU MEANT (v6's `refine` +
`discrete_ball_inflation` do this in seconds). (15) **Know which SIDE of the inequality you
are on, and write it down.** Five legs reported family-restricted maxima — LOWER bounds —
into a framework that needs UPPER bounds, and the budget quoted throughout was an upper
bound assembled out of lower bounds. Nobody was hiding it (family_op_norm says so in its own
docstring); it just never got carried to the conclusion. (16) **Use the symmetry you already
have.** The |H(h)| bound with the textbook one-sided kernel DIVERGES as X→0, where parity
makes the truth exactly 0, and loses a factor 2 far out. The even-kernel form is finite at
the origin AND sharp. Free accuracy, easy to leave on the table. **NEW from §17:**
(20) **Do not let the regime of an ARGUMENT become the regime of the CODE.** v8's scaling
argument (the one that shows the estimate is finite) needs the two points close together
relative to their distance from the endpoint; the ESTIMATE needs only that the near region
fits on the circle once. The first draft imposed the argument's condition on the code, a far
cruder fallback took over just outside it, and the reported constant came back **12× too
large** — every one of the offending pairs was the fallback, not the estimate. Write down
separately what the derivation assumes and what the formula requires. (21) **When your bound
is a MAJORANT of a decomposition, build the DECOMPOSITION twice — the majorant test cannot
see a wrong decomposition.** "Is the bound bigger than the measured value" passes just as
happily when the identity underneath is wrong by a sign, because a majorant of the wrong
object is still a valid inequality about something. v8's exact rebuild against the
closed-form conjugate caught two sign errors, one of which was also wrong in the module
docstring, where it had been sitting looking correct. This is banked lesson (3) with the
extra clause: build the IDENTITY twice, not just the number. (22) **A trend across legs is a
hypothesis, not a law — price the next point before acting on it.** Three consecutive legs
lost an order of magnitude of budget for the same reason, and the natural conclusion was
that the method dies of a thousand cuts. The fourth point, same cause, cost 7%. Plot the
history (v8 fig26 panel F), but do not retire a lane on three points with a shared cause.
(23) **Once the coverage is nearly complete, SHARPNESS becomes the bigger lever — compute
which.** Bounding the last open constants can buy at most a constant factor each; halving
the ~75× slack in ‖A‖ buys more than all of them together. That comparison is a two-minute
calculation and it should be redone at the end of every leg. **NEW from §19:** (26) **A bracket
is TWO numbers and both have to be earned before any decision comes out of it.** Six legs quoted
a lower bound from sign-pattern directions without once plotting it against J — where it would
have been obvious that it DEGRADES with refinement and was therefore measuring the instrument,
not the operator. The cost was a leg spent sharpening the wrong input and a phantom "19×
available gain". (27) **When validity is FREE, the problem is CONSTRUCTION, not optimisation.**
Any test vector gives a valid lower bound, so no LP, no certificate machinery and no clever
solver was needed — just asking what the unit ball actually contains (a decay rate and no
oscillation) and sweeping shapes. The random ascent that was supposed to be the hard part
improved the answer by 0.0%. (28) **Quote the bracket AT THE OPERATING POINT.** The reference
point (1.5, 0.5) gave 16×; the point where the budget has actually been evaluated for three legs
gave 7.7×. Reporting constants where they were first derived rather than where they are used is
its own quiet error. **NEW from §18 — the two that
would have saved this leg:** (24) **Price the ELASTICITY before choosing the target.** Scaling
each input of a composite bound by a factor and fitting d log(output)/d log(input) costs one
minute. v9 spent a leg sharpening an input whose elasticity at the operating point is +0.11,
and v8 spent one on an input at ≤0.5 — both moved the budget ≤7%, which is the table read
backwards. The input that governs everything (C_sup, elasticity +1.00) has not been touched
since it was first bounded. (25) **Never read an "available gain" off a bracket whose LOWER
end you have not earned.** ‖A‖'s 47–75× bracket has a lower end that is a maximum over a few
sign-pattern directions; it bounds the available gain from ABOVE and says nothing else. v9
tried to convert it into a number by substituting that lower end as an oracle and got a 19×
phantom. Worse, the ambiguity is decision-relevant: "the bound is 47× too big" and "the
operator really is that large" imply opposite conclusions about the whole lane, and we
currently cannot tell them apart. **Build the lower bound; a bracket you cannot interpret is
not a measurement.** **NEW from §16:**
(17) **The freshest lesson is the most tempting analogy — and an analogy is not a
diagnosis.** v6 recommended its own successor's method by reasoning from v6's own headline
(the discrete-ball trap): "the seminorm dual is lossy, and we just learned that discrete
balls are unfaithful, so restrict the ball." A ten-minute measurement showed the loss was on
the NEAR DIAGONAL, which a ball-faithfulness defect cannot produce. **Cost of the check: ten
minutes. Cost of skipping it: a whole leg spent quantifying a faithfulness factor that would
not have moved the number.** Spend the ten minutes localizing a defect before designing
against it. (18) **When a bound is lossy, ask whether you are pricing terms that the EQUATION
relates.** The dual was pricing two adjacent rows of an inverse independently and then
dividing by their tiny separation — throwing away a cancellation that no refinement of a dual
functional can see, because it is a property of the equation, not of the rows. The fix was to
solve the equation for the derivative. Generalization: **duality is the right tool for "how
big can this be"; it is the wrong tool for "how much do these two nearly cancel".**
(19) **Watch the RATE at which honesty costs you — it is a lane decision, not a detail.**
Budget 7.6e-2 (v5, lower bounds) → 1.18e-2 (v6, Z₁ priced) → 2.0e-4 (v7, ‖A‖ priced). Two
consecutive order-of-magnitude losses, both from replacing a lower bound with the honest
upper bound, with three constants still open. The individual numbers are fine; the SEQUENCE
is the result, and it says the approach needs constants that are roughly SHARP, not merely
bounded. **Plot your own budget history across legs — the trend is a cheaper decision
procedure than any single leg's number.**
 **NEW from §21 — the three that
this leg cost:** (29) **A constant is attached to a POINT, not to a problem.** Seven of ten
ledger constants were bounded — all at the a=0 anchor, because that is where the exact solution
is, and nobody ever wrote down that the certificate needs them at the a≠0 PROFILE instead. One
J-ladder at the real profile turned "bounded" into "divergent" (J^+2.86 vs the anchor's
J^−0.003). Before pricing anything, write down the point at which the price is quoted, and
re-run the ladder there. (30) **A number that is under budget is not a result until the budget
was computed for the same object.** v12's a=0.2 defect came in 7.7× under and looked like the
leg's headline for half an hour; the budget it beat was the anchor's. (31) **When a measurement
misbehaves in TWO ways at once, stop measuring and ask what object you are looking at.** The
weighted defect was non-monotone in a AND its arg-max was pinned to the domain edge at every a.
Either alone is a shrug; together they were one fact (the profile ends, and a global spectral
basis rings where it should be flat). The temptation was to fix the measurement.
 **NEW from §22:** (32) **A mechanism is a
claim and needs its own gate.** v12's measurements were gated six ways; the SENTENCE explaining
them ("the mode blows up like s^{−1/a}") was gated not at all, and it was wrong by a sign.
Fitting the exponent a mechanism predicts costs ten minutes and is now a unit test. **If a
writeup asserts an exponent, fit it.** (33) **Attribute a divergence by making the suspected
cause stop moving.** "It is the far field" became a measurement the moment the domain sup was
restricted to a fixed radius — and the same ladder surfaced the part the story does NOT explain
(a residual J^+0.3 at fixed radius), which is in the writeup as unattributed rather than rounded
to zero. (34) **The cheapest disqualification is a symmetry count.** Bordering with c to fix a
RANGE obstruction was dead on paper from a fact recorded twice already in these notes (dilation
is a symmetry ⇒ it supplies KERNEL); measuring it took three minutes and made the paper argument
checkable. (35) **Correct in place, and mark the correction.** v12's writeups keep their wrong
sentences struck through with a banner pointing at v13, because a silently edited record is
worth less than a corrected one. **NEW from §23 — the four that fourteen legs paid for:**
(36) **BEFORE DISCRETIZING, TRY TO INTEGRATE.** Thirteen legs of space design, norm design,
adversary construction and constant-pricing were spent on an equation that integrates once in
closed form, and the integration is two lines. The ingredient had been sitting in these notes
since §21: E was DEFINED there, and its derivative IS the equation's own nonlinearity. Nobody
differentiated the definition. Cost: eleven legs of far-field machinery that a bounded interval
does not need. **Ask what the equation's own quantities satisfy before asking what basis to put
them in.** (37) **A degenerate row is a FORMULATION smell, not a bookkeeping nuisance.** The
direct finite-support build needed a free-boundary condition APPENDED, precisely because the
residual carries no information at the support edge — and it never converged. The formulation
whose edge row is nonzero converges from a cold start in 5-10 steps at every a. **When a build
needs a condition appended, ask what the equation forgot.** (38) **When you change formulations,
RE-MEASURE THE CONTROL WITH THE NEW CODE.** "Flat vs J^+2.8" is only a contrast if both sides
are the same norm; the first draft compared the reduced ladder to an UNWEIGHTED whole-line
ladder, which diverges J^+0.99 at the ANCHOR purely because the grid's outer radius grows with
J. That would have manufactured a result out of a grid parameter. (39) **A repair that works
also RE-OPENS what the broken version banked.** Fixing the formulation retired a banked
confirmation of a* — because the evidence for it was a symptom of the same instrument defect the
repair removed. Re-run the OLD conclusions through the NEW formulation, not only the new
question. **NEW from §24 — the three the literature check cost:**
(40) **CHECK THE LITERATURE BEFORE THE FOURTEENTH LEG, NOT AFTER.** One hour of search
re-priced fifteen legs. Every piece of this project's discipline — gate the mechanism, build
the adversary, price the elasticity, quote the bracket at the operating point — is aimed at not
fooling yourself with your OWN instruments, and **not one of those instruments can tell you
that somebody else finished first.** A project that only ever measures itself against its own
previous leg will walk a long way in a direction that is already occupied. (41) **Record a
negative or dangerous lead WITH its confidence, or it will be re-found and re-believed.** The
extraordinary 3D-NS-singularity preprint is in writeup/data/p2_literature_scope.json flagged
"do not use", precisely so the next session does not independently rediscover it and lose a
day to it. (42) **When the binding constraint is ACCESS rather than compute, say so and name
what would unblock it.** The cheapest decisive act available to this project is now "read one
paper", and it is blocked by a network policy. Surface that to the user; do not silently route
around it and do not substitute more computation for the missing fact. **NEW from §25 — the three v16 paid for:**
(43) **When a repair removes an obstruction, ENUMERATE THE OTHER OBSTRUCTIONS before assuming
they went with it.** v14 removed the far field and an unstated assumption came along for the
ride: that the smoothness requirement went too. It did not and it never could have — H's
unboundedness on sup is about a JUMP, not about infinity. **Ask which of the old requirements
were actually ABOUT the thing you removed.** (44) **Two independent-looking signs of the same
conclusion can be one real fact and one instrument artifact, and they will not feel different.**
The naive single-mode probe and the step adversary both said "divergent"; a 4x quadrature
refinement killed one and left the other untouched. Reaching the right conclusion for a wrong
reason is how a wrong reason survives several legs. **Refine the instrument on EVERY row,
including the ones you agree with.** (45) **A ledger entry that is unknown must be None, never
zero, and the assembly must REFUSE TO RUN.** Returning a budget with Z_1 silently absent would
have produced a closed-looking result off a ledger with a hole in it.
 **NEW from §26 — the seven Route-E v1 paid for:**
(46) **A symmetry audit is cheaper than an eigenvalue solve, and it predicts part of the
answer.** Two of this leg's eigenvalues were derivable in five lines from the flow's symmetries.
Doing that FIRST meant "exactly two survived" read immediately as "nothing but symmetry" instead
of looking like a result. **Enumerate the symmetry modes before computing a spectrum; they are
the null result's baseline.** (47) **A null result needs a PLANTED POSITIVE, not just a
control.** Lesson (2) says ablate to attribute and (9) says build the adversary; this is the
third member. When the finding is ABSENCE, show the instrument detecting a PRESENCE of the same
kind — here, planting a bump and recovering +1.083 and +4.578. (48) **When you generalize a
gauge, RE-DERIVE it — do not extend it.** c_omega = 1 - H(Omega)(0) is correct at a=0 and was
being carried at every a; for a != 0 that flow admits NO fixed point at all, and one line of
algebra at the origin catches it. This is (29) wearing the gauge's clothes. (49) **The
regularity of the object sets the convergence rate of everything built on it, and it can vary
with the PARAMETER.** alpha(a) is an output and is an odd integer at isolated points, where the
method is spectral and everywhere else second-order — a ten-order accuracy swing driven by
nothing but a. **Find where your object is smooth and quote your sharp numbers there.**
(50) **An exactly known eigenvalue is a free error bar on every other one.** The dilation mode is
0 by symmetry, so its COMPUTED value is the spectrum's error at that parameter (0.35 at a=0.2,
8.9e-5 at a=1/2) — and that decided which rows of the sweep could carry a conclusion. **If a
symmetry pins one eigenvalue, plot its deviation next to every claim about the others.**
(51) **A convergence filter can be fooled by the EDGE of a continuum, and the fix is a CONTROL
POINT, not a tighter tolerance.** The "-2" at a=1/2 converged to six digits and was the essential
spectrum's left edge; tightening the filter would have made it look BETTER. What exposed it was
evaluating the same quantity at a=0, where that identical edge carries 99% of the spectrum.
**Before believing an isolated eigenvalue, ask where the continuum's edges are — then go look at
the same object somewhere you already understand it.** (52) **Two points define a line through
anything — and two RUNGS define a convergence rate through anything.** I hypothesised a rule from
the only two special points I had, went and found the third, read two rungs of its ladder as
algebraic, wrote the rule off as false AND COMMITTED THAT; four more rungs gave order
3.6→6.5→11.5→15.4→19.7 (exponential) and the rule held. **Add rungs until the exponent stops
moving** — a steeper object reaches its asymptotic regime later, which is when a short ladder is
most misleading.
 **NEW from §27 — the three Route-F v1 paid for:**
(53) **When two legs measure the same constant through unrelated machinery, that cross-check is
worth more than either leg's internal error bar.** alpha from a steady compactified solve on the
LINE and dp/ds from time-dependent PERIODIC simulation share no grid, basis, formulation or
fitted constant; refining one cannot test the other, and agreement tests both. **Look for a
second, structurally different route to a number you already have** — alpha sat in §26's data
file as a by-product, and using it twice turned a curiosity into a check. (54) **A systematic
that is UNIFORM across a sweep is pointing at a shared input, not at the mechanism.** Every
measured p sat above its prediction with a shallower slope: that is what a wrong SINGULAR TIME
does, not what a wrong exponent does. **Read the pattern of the residuals before adjusting the
model.** (55) **A guard that can return "perfect" by construction is worse than no guard.** Two
of this leg's three resolution-guard definitions were silently degenerate — one identically zero
at half the grid sizes (the dealiasing had already zeroed the band it measured), one identically
fat at all of them (a near-singular spectrum genuinely is broad). **Before trusting a diagnostic,
run it on a case you KNOW is bad and one you know is good, and confirm it separates them.**

 **NEW from §28 — the four Route-G v1 paid for:**
(56) **A FORMULA THAT IS RIGHT IN ONE MODEL CAN BE A GAUGE CHOICE RATHER THAN A LAW — PORT IT
BEFORE YOU HEADLINE IT.** s_c = alpha/2 was correct, gated, and cross-validated against an
unrelated computation, and it was still a coordinate expression, true only because gCLM's
rescaling pins c_l = 1. **Nothing internal to the 1D leg could have revealed that** — not a
finer grid, not a wider window, not a better control, not another decade of (T-t). Changing
the MODEL is a test that no amount of refinement WITHIN the model substitutes for. Every
banked lesson up to here is about not fooling yourself with your own instrument; this one is
about not fooling yourself with your own COORDINATES. (57) **When the instrument that worked
does not port, ask whether an instrument you ALREADY OWN does.** The direct time-dependent fit
fails in 2D for a resolution reason that will not go away — but the project already had a
dynamic-rescaling machine in which the same quantity is a MODULATION CONSTANT, with no fit, no
window and no singular-time estimate anywhere in it. **The repair for a measurement that is too
noisy is sometimes a different DEFINITION of the same number, not more grid.** (58) **Check the
MONOTONICITY of your own headline, in words.** "Faster collapse loses to viscosity" is the
opposite of the natural intuition ("a violent singularity should overwhelm viscosity"), and the
natural intuition is what gets written into a summary sentence by reflex. It is now a unit test.
(59) **A CALIBRATION between the toy and its target is worth a leg on its own.** Fifteen legs of
gCLM work and nobody had asked where the 2D object sits on gCLM's own dial. It took an afternoon
and it changes what the family map is evidence FOR.

HONEST CEILING — **AND FROM ROUTE-G v1: the "beat viscosity" sentence is now on the 2D object,
and its content changed on the way. The law is s_c = 1/(2 beta), NOT alpha/2 — the 1D form was
a GAUGE CHOICE (true only where c_l = 1) and only the port could have caught it. NS is
beta = 1/2 ⇒ s_c = 1 exactly. s_c DECREASES with beta, so beating ordinary viscosity requires
an anomalously SLOW collapse (beta < 1/2), which is the opposite of the natural intuition. The
proven Chen–Hou 2D Boussinesq blow-up is at beta = 2.92, s_c = 0.171 — SIX TIMES the NS
collapse rate, on the losing side by a wide margin. That is ORIENTATION about the distance
between the toy and the target, NOT evidence about NS and NOT a claim that a viscous 2D
blow-up exists. Its measured half REPRODUCES Chen–Hou rather than extending them (Level-0 by
construction), the 1D method does NOT port (under one decade of (T-t) against 1D's four, and
one more decade costs 10^beta in LINEAR resolution), and it moves NO link of the chain. What it
does do that no previous leg did: it CALIBRATES the toy against its target, and the answer is
that gCLM's dial and the 2D object sit on opposite sides of the NS line.** **AND FROM ROUTE-F v1: the "beat viscosity" sentence has a measured
right-hand side in 1D, s_c = alpha/2, confirmed with nothing fitted at a=0 and cross-checked
against an unrelated computation of alpha. It is ORIENTATION, not evidence about NS: NS's alpha
is pinned at 2 by dimensional analysis, gCLM's is a dial, and nothing here says a viscous gCLM
blowup EXISTS above the crossing. It moves no link of the chain.** **AND FROM ROUTE-E v1: the DSS lane's cheapest entrance is SHUT. There is no
eigenvalue of the gCLM self-similar fixed point available for a Hopf bifurcation; the only
isolated grid-converged spectrum is the two exact SYMMETRY modes, and the log-periodic (DSS)
directions are CONTINUOUS spectrum. That is a genuine negative with a mechanism and a planted
positive control behind it — and it moves NO link of the chain. It is not Clay progress; it is
lane scoping that prevents several legs of misdirected build. The flow is also not spectrally
stable (essential spectrum reaching +1 at a=0 and +5 at a=1/2), which is norm-dependent and
still cannot bifurcate.** Route-D v3–v14 are validated tooling + a no-go theorem, a
confirmed price, a second structural requirement, a space that met every requirement identified
up to v11, upper bounds for seven of ten constants (a COMPLETE Z₂ and the whole of ‖A‖) — **all
at the a=0 ANCHOR, and all about a formulation v14 replaced** — one disqualified method, a
budget that lost two orders of magnitude to honesty, a measured bracket, v12/v13's finding that
the object those constants were meant to certify was not in the space they were computed in,
and, as of v14, an exact first integral of the profile equation together with a reduced
formulation on [0, X_c] whose approximate inverse CONVERGES under refinement. **That is real
progress and it is still not a certificate:** no constant of the radii polynomial has been
computed in the reduced space, so there is no budget, closed or otherwise. Everything is plain
float64: nothing is interval-enclosed, nothing is rigorous, and solver/interval.py has still
never been pointed at any of it — correctly, because nothing has closed in float. Even the
eventual success this scouts is a computer-assisted TOY-MODEL certification (Chen–Hou /
Gómez-Serrano genre), NOT a Clay solve. 1D HL is a toy model (boundary behaviour of Hou–Luo /
3D-axisymmetric-Euler). And v14's headline is **novelty-unchecked** — a first integral of a
scalar traveling-wave equation is exactly what may be folklore to people who work on this
family, and the literature search blocks the claim. Overall Clay odds ~0.05%, unchanged by this
leg. **AND, from v15: L1 — the milestone fifteen legs aimed at — is very probably OCCUPIED
TERRITORY. Computer-assisted interval/Newton-Kantorovich certification is routine for the
groups working this family, and the two-scale traveling wave's existence appears to have been
proved analytically in March 2026. Finishing the certificate is a capability demonstration and
a reproduction. That is not a reason to stop; it is a reason to stop calling it the lottery
ticket, and to move the swing to the DSS lane. Every measurement in v3-v14 still stands —
being second is not being wrong.** Keep pursuing the Clay end goal; keep saying the honest
version out loud. **AND from v16: the reduced-space float rehearsal DOES NOT CLOSE.** Y_0 is
finally machine-level (1.5e-12) and Z_0 is roundoff, but Z_2 is infinite in the sup setting for
two reasons that have nothing to do with the far field, and Z_1 — the whole content of a real
computer-assisted proof — has not been computed at all. **There is still no budget in the
reduced space, closed or otherwise, and the code refuses to assemble one.** The repair (a Holder
domain norm, gamma >~ 0.35) is named and measured but not built.
