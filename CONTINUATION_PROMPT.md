# Continuation prompt (copy into a fresh session)

*Written 2026-07-31 (updated after Route-D v9). **NEWEST LEG FIRST — Route-D v9, the
SHARPNESS leg — is a NEGATIVE WITH A MECHANISM, and the mechanism is the most useful thing
in it.** v8 left Z₂ complete and seven of ten constants bounded, so the question changed
from COVERAGE to SHARPNESS (budget ~ 1/(‖A‖C_Q); ‖A‖'s bracket ~70× wide). The target was
obvious: v7's closure is dominated by its own feedback and the feedback is v6's crude
|H(h)| bound. **Rebuilt it on the exact folded kernel K = 2sinθ/(cosφ−cosθ)**, whose p.v.
over (0,π) is EXACTLY ZERO (it is the conjugate of the constant function) so the
singularity needs **one global subtraction** instead of v6's band + matching scale +
remainder — sharper at every X (ratio 0.09–0.99) and **nearly ATTAINED** (0.97 on the
anchor). Also found that the **PAYER RULE** (which part of the norm pays at each point) is
a FREE PARAMETER with an interior optimum, and that the neutral choice — compare at S=T=1,
v8's default — is **WORSE than the crude bound it replaces**: *tune the rule to the T/S
ratio of the ANSWER, not to 1.* Result: **‖A‖ 69.15 → 47.05 (−32%)**, the largest single
gain since the closure was built. **AND THE BUDGET DID NOT MOVE: 2.39e-4 → 2.40e-4.** Why:
the closure is T ≤ C(γ)(P/2)^γ(2S)^{1−γ} and the |H| bound enters **only through P**, so at
the map's optimum (γ=0.15) a 30% better P moves T by 4% — gain by point 32%/11%/3%/**0%**.
Worse, the optimum sits at small γ **because** that is where ‖A‖ barely depends on this
input; the optimiser had already walked to the corner where the improvement cannot matter.
**THE ELASTICITY TABLE (one minute, and it should have come first): d log‖A‖/d log C_sup =
+1.00 at the operating point vs d log‖A‖/d log|H| = +0.11. The last TWO legs both worked on
inputs with elasticity ≤ 0.5 and both moved the budget by ≤ 7% — that is the table read
backwards, and neither leg computed it beforehand.** Everything below is banked + pushed on
`main`. **The next brick is decided by that table, not by intuition — and there is an
argument for doing (2) before (1): (1) C_sup, the two-point dual, the only elasticity-1
input left (~2× available); (2) a REAL LOWER BOUND on ‖A‖, because without one no bracket
in this project can be attributed at all.** Read the "IS THIS STILL THE RIGHT LANE?" box.*

*Before v9, in the same session: **Route-D v8** priced the LAST unbounded constant in
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

THE LEVEL / RIGOR LADDER (the user's framing, honor it): Level-0 = reproduce known
results. Level-1 = a novel numerical map (where ALL gCLM work through fig18 sits).
Level-2 = a rigorous computer-assisted statement (interval / Newton–Kantorovich
certification) = the FIRST rung that is genuinely "novel maths" — **Route-D
v1–v9 (fig19–fig27) are tooling + scoping/negative results + partial upper bounds on the
way there, NOT certificates.**
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
v2, §12–§17 ROUTE-D v3–v8, **§18 ROUTE-D v9 = newest**).
Per-leg writeups + figs under writeup/4_p2_lottery/: TECHNICAL/BLOG_P2_{HL_ANCHOR(fig12),
CONJ24(fig13),SCENARIO2(fig14/15),GA_FRAMEWORK(fig16),TWO_SCALE(fig17),KLADDER(fig18),
ROUTED(fig19),ROUTED_DRESS(fig20),ROUTED_SPACES(fig21),ROUTED_V4(fig22),ROUTED_V5(fig23),
ROUTED_V6(fig24),ROUTED_V7(fig25),ROUTED_V8(fig26),**ROUTED_V9(fig27)**}.md. Then experiments/JOURNAL.md (newest first) and LOGGING.md.

STATE (all banked + pushed to main):
- Phase 1 CONCLUDED. Spike 0/1 DONE. P2 anchor (§2), §6 degenerate-gauge, §7 reframe,
  §8 B1 (Scenario-2), §9 GA framework, §9-cont two-scale a-sweep (5/6), §9-cont2
  a_p(K) convergence map (7/7), §10 Route-D v1, §11 Route-D v2, §12 Route-D v3,
  §13 Route-D v4, §14 Route-D v5, §15 Route-D v6, §16 Route-D v7, §17 Route-D v8,
  §18 Route-D v9 — all DONE + banked.
- The gCLM two-scale survival boundary is GENUINE (a\*≈0.5–0.55, a SOFT crossing),
  not genome-limited (§9-cont2 earned this via GA-/genome-/basis-convergence).

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

**IS THIS STILL THE RIGHT LANE? (v9 gives the sharpest read yet, and it is mixed.)** The
budget has now been flat for three legs — 2.58e-4 → 2.39e-4 → 2.40e-4 — through one leg that
completed the coverage (v8) and one that sharpened the estimate everyone assumed was the
bottleneck (v9). Neither moved it. GOOD: nothing has gone WRONG either; the three
order-of-magnitude losses stopped at v7 and the structure is stable (same optimum, same
ledger, seven of ten bounded, Z₂ complete). BAD: 2.4e-4 is still ~40× below the GA residual
floor, and v9 shows the obvious sharpening targets have small elasticity — the budget is
governed by **C_sup**, which nobody has touched since v6, and by the interpolation
inequality's structure. **THE MOST IMPORTANT THING v9 SAYS: we cannot currently tell a lossy
bound from a large truth.** Every bracket quoted in this project has a LOWER end that is a
maximum over a handful of sign patterns, which is nearly meaningless, and v9 got a 19×
phantom gain out of exactly that confusion. Until there is a real lower bound, "the bound is
47× too big" and "the operator really is that large" are indistinguishable — and they imply
opposite decisions about the lane. Two respectable calls: (i) do the lower-bound leg, THEN
decide with information; (ii) stop the estimate grind here, write the whole P2 arc up as one
coherent community piece (the strongest artifact this project has), and spend the remaining
swing on the coupled-system HL two-stage question. **(i) is cheap and makes (ii) better
informed; that is the recommendation.**

THE RECOMMENDED NEXT BRICKS IF CONTINUING, in the order v9's elasticity table implies:
  (1) **A REAL LOWER BOUND on ‖A‖ — do this FIRST.** The induced norm between polyhedral
      norms is an LP; there is no scipy, but the ball's structure is simple enough for a
      hand-rolled simplex or a projected-gradient ascent over the codomain ball, and even a
      good ADVERSARY construction (v4's square-wave family did this for the quadratic) would
      beat sign patterns by a lot. Deliverable: a bracket whose WIDTH means something. This
      is what tells you whether (2) is worth doing, and whether the whole lane is.
  (2) **C_sup, the two-point dual on the sup part** — the only input left with elasticity ≈ 1,
      untouched since v6, ~2× plausibly available. Handles: the dual currently minimises over
      a SUBSET of reference indices m₀ (valid but lossy); and it inherits v6's crude |H|
      bound nowhere — it is pure duality, so the slack is in the two-point inequality itself.
  (3) The core↔far cutoff commutator [H, φ] — the last structural piece of Z₁.
  (4) The change of ansatz h=(1+X²)^{−α/2}p(θ) (v7 V6).
  (5) The core discretization error (v4 W6).
ONLY when Y₀, Z₀, Z₁, Z₂ are ALL real upper bounds should the float radii polynomial be
assembled, and the same stopping rule applies: **if it does not close in float with margin,
STOP, do not harden.** solver/interval.py has existed since v1 and has still never been
pointed at any of this — correctly, because nothing has closed in float.

SUPERSEDED (kept for the record) — the v9 spec, which this session executed: **"SHARPEN ‖A‖
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
`python test_X.py`. Suites (all 16 green): test_interval.py (5/5) + test_nk_fourier.py
(6/6) + test_decay_grading.py (7/7) + test_decay_collocation.py (6/6) +
test_holder_norms.py (6/6) + test_nk_bounds.py (6/6) + test_nk_seminorm.py (6/6) +
test_nk_hilbert_holder.py (6/6) + **test_nk_hilbert_pointwise.py (6/6, NEW)** +
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
probes get a clearly-labelled non-logged entry too, as §10–§18 did).

**WRITEUP STRUCTURE:** evidence rebuilds (each reads committed writeup/data/\*.json):
writeup/4_p2_lottery/{p2_route_d_v9_evidence.py(fig27), p2_route_d_v8_evidence.py(fig26),
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
a (α,γ) cell costs 4 ρ-values, and the map is 64 cells; test_nk_hilbert_pointwise ~6 min**).**
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
calculation and it should be redone at the end of every leg. **NEW from §18 — the two that
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

HONEST CEILING (say it out loud): Route-D v3–v9 are validated tooling + a no-go theorem, a
confirmed price, a second structural requirement, a space that meets every requirement
identified so far, upper bounds for seven of ten constants (a COMPLETE Z₂ and the whole of
‖A‖), one disqualified method, a budget that lost two orders of magnitude to honesty and has
been flat for three legs, and — as of v9 — an explicit admission that we cannot yet tell a
lossy bound from a large truth; they do NOT climb the rigor ladder. Everything in it is plain
float64: nothing is interval-enclosed, nothing is rigorous. Even the eventual success it
scouts is a computer-assisted TOY-MODEL certification (Chen–Hou / Gómez-Serrano genre),
NOT a Clay solve. 1D HL is a toy model (boundary behaviour of Hou–Luo /
3D-axisymmetric-Euler). Overall Clay odds ~0.05%. Keep pursuing the Clay end goal; keep
saying the honest version out loud.
