# Continuation prompt (copy into a fresh session)

*Written 2026-07-30 (updated after Route-D v6). Earlier in the session: ran
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
fiction. Pricing Z₁ for the first time **KILLS v5's joint optimum**. Everything below
is banked + pushed on `main`. **The scoping phase of Route D is DONE; v6 started the
estimates phase and left exactly three named gaps.** The recommended next thing is
**the domain-seminorm part of ‖A‖ (Route-D v7)** — but read the "IS THIS STILL THE
RIGHT LANE?" box.*

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
certification) = the FIRST rung that is genuinely "novel maths" — **Route-D v1
(fig19), v2 (fig20), v3 (fig21), v4 (fig22), v5 (fig23) and v6 (fig24) are tooling +
scoping/negative results + partial upper bounds on the way there, NOT certificates.**
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
v2, §12 ROUTE-D v3, §13 ROUTE-D v4, §14 ROUTE-D v5, **§15 ROUTE-D v6 = newest**).
Per-leg writeups + figs under writeup/4_p2_lottery/: TECHNICAL/BLOG_P2_{HL_ANCHOR(fig12),
CONJ24(fig13),SCENARIO2(fig14/15),GA_FRAMEWORK(fig16),TWO_SCALE(fig17),KLADDER(fig18),
ROUTED(fig19),ROUTED_DRESS(fig20),ROUTED_SPACES(fig21),ROUTED_V4(fig22),ROUTED_V5(fig23),
**ROUTED_V6(fig24)**}.md. Then experiments/JOURNAL.md (newest first) and LOGGING.md.

STATE (all banked + pushed to main):
- Phase 1 CONCLUDED. Spike 0/1 DONE. P2 anchor (§2), §6 degenerate-gauge, §7 reframe,
  §8 B1 (Scenario-2), §9 GA framework, §9-cont two-scale a-sweep (5/6), §9-cont2
  a_p(K) convergence map (7/7), §10 Route-D v1, §11 Route-D v2, §12 Route-D v3,
  §13 Route-D v4, §14 Route-D v5, §15 Route-D v6 — all DONE + banked.
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

**IS THIS STILL THE RIGHT LANE? (raise with the user if the odds matter to a decision.)**
v6 changed the picture in both directions and both should be said. GOOD: three of eight
constants are now genuinely BOUNDED rather than measured, and the conditional budget
(1.18e-2) is the same ORDER as the a≈0.5 GA residual floor (~1e-2) — so the target is no
longer out of reach by orders of magnitude, which it appeared to be after v2. BAD: v6 also
showed that v5's headline optimum was an artifact of not pricing Z₁, and that one whole
class of computation we might have trusted (discrete-ball duality) is unsound — so the
remaining three constants may hold more surprises of the same kind, and the budget is
still CONDITIONAL and OPTIMISTIC. The honest best case for the whole Route-D leg remains
"certifies the a=0 traveling wave", which is already known in closed form; a≠0 stays a
hope, not a plan. The next three bricks are ESTIMATES — narrower, more technical, and less
likely to produce a surprising story than the scoping legs did. Worth checking the user
still wants that before committing.

THE RECOMMENDED NEXT BRICK — **Route-D v7: the three open ledger items, in order of
sharpness.** The scoping phase is over; these are ESTIMATES, and each is now named
precisely enough to attack alone.
  (1) **The domain-SEMINORM part of ‖A‖ — the sharpest.** The continuum argument says it
      is finite (the inverse gains a WHOLE derivative: h_X = −(g + H(h) + X h)/c, so
      g ∈ C^{0,γ} puts h ∈ C^{1,γ}, more smoothness than the norm asks for); three
      computations all came back lossy at J^γ because they were still pricing B1's fake
      direction. Two candidate routes: (a) restrict to a BAND-LIMITED subspace where the
      discrete norm IS faithful, with a quantified faithfulness factor (v6's `refine` +
      `discrete_ball_inflation` already measure that factor — a smooth element of the
      class is faithful to 3%); (b) bound the seminorm through the C^{1,γ} gain
      analytically rather than by duality. Do (a) first — it is cheap and reuses v6 tooling.
  (2) **The core↔far-field coupling of Z₁.** A sharp split at X₀ has a 1/(X−X₀) seam
      because H is NONLOCAL, so it needs a smooth cutoff φ and a commutator estimate for
      [H, φ] (φ′ ~ 1/X₀, so the terms are O(1/X₀) — the scale is right, the estimate is
      the work). This is the standard "compact core + explicit far field" machinery.
  (3) **The core discretization error** (v4 W6 measured J^−2.1..−2.6, never bounded) —
      a statement about band-limited approximation of the true decay class.
ONLY when Y₀, Z₀, Z₁, Z₂ are ALL real upper bounds should the float radii polynomial be
assembled, and the same stopping rule applies: **if it does not close in float with
margin, STOP, do not harden.** solver/interval.py has existed since v1 and has still never
been pointed at any of this — correctly, because nothing has closed in float.

SUPERSEDED (kept for the record) — the v6 spec, which this session executed:
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
`python test_X.py`. Suites (all 13 green): test_interval.py (5/5) + test_nk_fourier.py
(6/6) + test_decay_grading.py (7/7) + test_decay_collocation.py (6/6) +
test_holder_norms.py (6/6) + **test_nk_bounds.py (6/6, NEW)** + test_gclm_family.py (12/12) +
test_hl_rescaled.py (9/9) + test_line_hilbert.py (6/6) + test_gclm_rescaled.py (5/5) +
test_boussinesq_{velocity,transport,rescaled}.py (5/5,5/5,8/8). Scripts under
experiments/ need the `sys.path.insert(0, dirname(dirname(abspath(__file__))))`
bootstrap. Before ANY logged experimental run: pass the test gate + COMMIT + LOCK the
predicate in git (dirty-tree guard; gitignored experiments/\*.{log,npz,jsonl,out} fine).
Solver dev + unit tests + DETERMINISTIC scoping probes are NOT "logged gate runs" (all
three Route-D probes are deterministic — no predicate lock needed); still add each new
solver test to the suite. Papers/ gitignored ([HQW25]=arXiv:2401.14615 →
Papers/hqw25.txt). One JOURNAL.md entry per logged experiment (deterministic tooling
probes get a clearly-labelled non-logged entry too, as §10–§15 did).

**WRITEUP STRUCTURE:** evidence rebuilds (each reads committed writeup/data/\*.json):
writeup/4_p2_lottery/{p2_route_d_v6_evidence.py(fig24), p2_route_d_v5_evidence.py(fig23),
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
cheap).** Run `python -u` to a
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
the origin AND sharp. Free accuracy, easy to leave on the table.

HONEST CEILING (say it out loud): Route-D v3+v4+v5+v6 are validated tooling + a no-go
theorem, a confirmed price, a second structural requirement, a space that meets every
requirement identified so far, and now upper bounds for three of the eight constants plus
one disqualified method; they do NOT climb the rigor ladder. Everything in it is plain
float64: nothing is interval-enclosed, nothing is rigorous. Even the eventual success it
scouts is a computer-assisted TOY-MODEL certification (Chen–Hou / Gómez-Serrano genre),
NOT a Clay solve. 1D HL is a toy model (boundary behaviour of Hou–Luo /
3D-axisymmetric-Euler). Overall Clay odds ~0.05%. Keep pursuing the Clay end goal; keep
saying the honest version out loud.
