# Continuation prompt (copy into a fresh session)

*Written 2026-07-30 (updated after Route-D v4) at the end of the session that ran
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
does NOT control the quadratic because H is unbounded on L^∞. Everything below is
banked + pushed on `main`. The recommended next thing is **the two-grading space
question (Route-D v5), settled ON PAPER first** — but read the "IS THIS STILL THE
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
(fig19), v2 (fig20), v3 (fig21) and v4 (fig22) are tooling + scoping/negative results
on the way there, NOT certificates.** Level-3 = Clay.

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
v2, §12 ROUTE-D v3, **§13 ROUTE-D v4 = newest**). Per-leg writeups + figs under
writeup/4_p2_lottery/: TECHNICAL/BLOG_P2_{HL_ANCHOR(fig12),CONJ24(fig13),
SCENARIO2(fig14/15),GA_FRAMEWORK(fig16),TWO_SCALE(fig17),KLADDER(fig18),ROUTED(fig19),
ROUTED_DRESS(fig20),ROUTED_SPACES(fig21),**ROUTED_V4(fig22)**}.md. Then experiments/JOURNAL.md (newest first) and LOGGING.md.

STATE (all banked + pushed to main):
- Phase 1 CONCLUDED. Spike 0/1 DONE. P2 anchor (§2), §6 degenerate-gauge, §7 reframe,
  §8 B1 (Scenario-2), §9 GA framework, §9-cont two-scale a-sweep (5/6), §9-cont2
  a_p(K) convergence map (7/7), §10 Route-D v1, §11 Route-D v2, §12 Route-D v3,
  §13 Route-D v4 — all DONE + banked.
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

**IS THIS STILL THE RIGHT LANE? (raise with the user if the odds matter to a decision.)**
v3+v4 are legitimate publishable bricks and they genuinely sharpened the target, but the
number is sobering and v4 made it worse, not better: the budget CEILING is 1.9e-2, and it
is a ceiling (Z₁=0 assumed, smoothness component unpriced), against an a≠0 residual floor
of ~1e-2. The honest best case for the whole Route-D leg remains "certifies the a=0
traveling wave", which is already known in closed form. Do not assume the lane; put a menu
if a big build is next.

THE RECOMMENDED NEXT BRICK — **Route-D v5: the TWO-GRADING space, ON PAPER FIRST.**
v4 showed the space needs a decay grading AND a smoothness scale. Settle whether a
consistent pair exists BEFORE writing any solver — that rule has now paid for itself
twice (§12 saved a two-region build, §13 would have been avoidable had the L^∞
unboundedness of H been checked first). Concretely: (i) the natural candidate is a
weighted-Hölder pair, |h|·(1+X²)^{α/2} in C^{0,γ} with codomain (1+X²)^{(α+1)/2} in
C^{0,γ} — H IS bounded on C^{0,γ} (constant ~1/(γ(1−γ)), so γ has its own interior
optimum, exactly like α), and Hölder is an algebra so the quadratic is fine; the thing to
check is whether the far-field ODE inverse still gains what it must in the Hölder scale,
and how the two optima (α, γ) interact. (ii) Do the v3-style conservation-law analysis in
the (α, γ) plane: is there a non-empty admissible region, and what is the best Z₂ in it?
(iii) ONLY if that closes on paper, extend solver/decay_collocation.py to Hölder norms
(discrete Hölder seminorms over node pairs are computable) and re-run W1–W4. The same
stopping rule applies: if the float rehearsal does not close with margin, STOP.

Alternative lanes (put these in the menu): (a) the separate coupled-system HL two-stage
leg (whether an HL-type two-stage appears at any scalar gCLM member or genuinely needs
the coupled (ω,θ) system) — the biggest genuinely-novel swing left; (b) extend the
a_p(K) map to the odd/one-scale channel (lower value — refines a Level-1 map); (c) write
up the whole P2 arc as a single coherent community piece (the 1D gCLM two-scale story +
the three-part Route-D negative) rather than building further.

ENVIRONMENT & WORKFLOW: .venv/bin/python (numpy + matplotlib; NO scipy —
tridiag/solvers/3×3/GA/Hilbert/interval-arith/Fourier-operator/decay-grading/collocation
all hand-rolled). 8-worker ceiling (OMP_NUM_THREADS=8 pinned). No pytest; run each suite as
`python test_X.py`. Suites (all 11 green): test_interval.py (5/5) + test_nk_fourier.py
(6/6) + test_decay_grading.py (7/7) + **test_decay_collocation.py (6/6, NEW)** +
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
probes get a clearly-labelled non-logged entry too, as §10–§13 did).

**WRITEUP STRUCTURE:** evidence rebuilds (each reads committed writeup/data/\*.json):
writeup/4_p2_lottery/{p2_route_d_v4_evidence.py(fig22), p2_route_d_v3_evidence.py(fig21),
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
matrices are J² and 40000 would be 12 GB).** Run `python -u` to a
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

HONEST CEILING (say it out loud): Route-D v3+v4 are validated tooling + a no-go theorem,
a confirmed price, and a second structural requirement; they do NOT climb the rigor
ladder. Everything in it is plain
float64: nothing is interval-enclosed, nothing is rigorous. Even the eventual success it
scouts is a computer-assisted TOY-MODEL certification (Chen–Hou / Gómez-Serrano genre),
NOT a Clay solve. 1D HL is a toy model (boundary behaviour of Hou–Luo /
3D-axisymmetric-Euler). Overall Clay odds ~0.05%. Keep pursuing the Clay end goal; keep
saying the honest version out loud.
