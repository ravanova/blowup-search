# Continuation prompt (copy into a fresh session)

*Written 2026-07-30 at the end of the session that ran **Route-D v3, the space-pair
scoping leg** — the gating check §11 attached to its own repair — and got a
**NO-GO THEOREM for the entire weighted-ℓ¹ category** together with a **constructive
positive half**: the two Newton–Kantorovich requirements are separated by exactly one
grading power and the separation is CONSERVED (measured minimum exponent sum 0.98 over
the whole family; control 0.00); the replacement is a DECAY-graded pair, which
satisfies both, is resonant at the anchor's own decay rate, and has an interior
optimum α\* ≈ 1.44. Everything below is banked + pushed on `main`. The recommended
next thing is **the compact-core block (Route-D v4)** — but read the "IS THIS STILL
THE RIGHT LANE?" box first.*

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
(fig19), v2 (fig20) and v3 (fig21) are tooling + scoping/negative results on the way
there, NOT certificates.** Level-3 = Clay.

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
v2, **§12 ROUTE-D v3 = newest**). Per-leg writeups + figs under writeup/4_p2_lottery/:
TECHNICAL/BLOG_P2_{HL_ANCHOR(fig12),CONJ24(fig13),SCENARIO2(fig14/15),
GA_FRAMEWORK(fig16),TWO_SCALE(fig17),KLADDER(fig18),ROUTED(fig19),ROUTED_DRESS(fig20),
**ROUTED_SPACES(fig21)**}.md. Then experiments/JOURNAL.md (newest first) and LOGGING.md.

STATE (all banked + pushed to main):
- Phase 1 CONCLUDED. Spike 0/1 DONE. P2 anchor (§2), §6 degenerate-gauge, §7 reframe,
  §8 B1 (Scenario-2), §9 GA framework, §9-cont two-scale a-sweep (5/6), §9-cont2
  a_p(K) convergence map (7/7), §10 Route-D v1, §11 Route-D v2, §12 Route-D v3 —
  all DONE + banked.
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

**IS THIS STILL THE RIGHT LANE? (raise with the user if the odds matter to a decision.)**
v3 is a legitimate publishable brick and it genuinely sharpened the target, but the
number it produced is sobering: Z₂≈13 ⇒ budget ~1e-2 BEFORE the compact core, Z₁ and
interval overhead are paid, against an a≠0 residual floor of ~1e-2. The honest best case
for the whole Route-D leg remains "certifies the a=0 traveling wave", which is already
known in closed form. Do not assume the lane; put a menu if a big build is next.

THE RECOMMENDED NEXT BRICK — **Route-D v4: the compact-core block in the decay pair.**
v3 priced the FAR FIELD; nothing yet prices the core. Concretely: (i) fix α=3/2, build
the finite-mode core operator with the decay-graded norms (the core is where the
coefficient picture is still fine — the grading only matters in the tail), and measure
the core's contribution to ‖A‖, Z₀, Z₁; (ii) the matching condition between core and
far field (v3's far-field solve already uses h(X₀)=0, the natural core match) and what
it costs; (iii) only then a full float radii polynomial in the decay pair — the v3
analogue of v2's dress rehearsal, and the same rule applies: if it does not close in
float with margin, STOP, do not harden. Do NOT skip to claiming a certificate.

Alternative lanes (put these in the menu): (a) the separate coupled-system HL two-stage
leg (whether an HL-type two-stage appears at any scalar gCLM member or genuinely needs
the coupled (ω,θ) system) — the biggest genuinely-novel swing left; (b) extend the
a_p(K) map to the odd/one-scale channel (lower value — refines a Level-1 map); (c) write
up the whole P2 arc as a single coherent community piece (the 1D gCLM two-scale story +
the three-part Route-D negative) rather than building further.

ENVIRONMENT & WORKFLOW: .venv/bin/python (numpy + matplotlib; NO scipy —
tridiag/solvers/3×3/GA/Hilbert/interval-arith/Fourier-operator/decay-grading all
hand-rolled). 8-worker ceiling (OMP_NUM_THREADS=8 pinned). No pytest; run each suite as
`python test_X.py`. Suites (all 10 green): test_interval.py (5/5) + test_nk_fourier.py
(6/6) + **test_decay_grading.py (7/7, NEW)** + test_gclm_family.py (12/12) +
test_hl_rescaled.py (9/9) + test_line_hilbert.py (6/6) + test_gclm_rescaled.py (5/5) +
test_boussinesq_{velocity,transport,rescaled}.py (5/5,5/5,8/8). Scripts under
experiments/ need the `sys.path.insert(0, dirname(dirname(abspath(__file__))))`
bootstrap. Before ANY logged experimental run: pass the test gate + COMMIT + LOCK the
predicate in git (dirty-tree guard; gitignored experiments/\*.{log,npz,jsonl,out} fine).
Solver dev + unit tests + DETERMINISTIC scoping probes are NOT "logged gate runs" (all
three Route-D probes are deterministic — no predicate lock needed); still add each new
solver test to the suite. Papers/ gitignored ([HQW25]=arXiv:2401.14615 →
Papers/hqw25.txt). One JOURNAL.md entry per logged experiment (deterministic tooling
probes get a clearly-labelled non-logged entry too, as §10, §11 and §12 did).

**WRITEUP STRUCTURE:** evidence rebuilds (each reads committed writeup/data/\*.json):
writeup/4_p2_lottery/{p2_route_d_v3_evidence.py(fig21), p2_route_d_dress_evidence.py
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
probe ~10 s; v2 dress ladder a few seconds; v3 space sweep ~1 min. Run `python -u` to a
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
and the check that confirmed the whole picture.

HONEST CEILING (say it out loud): Route-D v3 is validated tooling + a no-go theorem with
a constructive replacement; it does NOT climb the rigor ladder. Everything in it is plain
float64: nothing is interval-enclosed, nothing is rigorous. Even the eventual success it
scouts is a computer-assisted TOY-MODEL certification (Chen–Hou / Gómez-Serrano genre),
NOT a Clay solve. 1D HL is a toy model (boundary behaviour of Hou–Luo /
3D-axisymmetric-Euler). Overall Clay odds ~0.05%. Keep pursuing the Clay end goal; keep
saying the honest version out loud.
