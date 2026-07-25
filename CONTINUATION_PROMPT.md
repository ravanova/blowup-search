# Continuation prompt (copy into a fresh session)

*Written 2026-07-25 at the end of the session that STARTED Phase-2 P2 (the lottery-ticket leg):
scouted Chen–Huang–Li arXiv:2604.01868, decided (with the user, on evidence) to attack the 1D
Hou–Luo singular-profile scenario, and built + validated the singular-profile machine against the
explicit exact Thm-2.3 steady state (5/5 known-answer tests), plus a shared-operator performance
pass. The dynamic-relaxation NOVELTY leg is set up but NOT yet started.*

---

Continue the Navier–Stokes blow-up search project in this directory
(/home/andy/projects/Unsolved). The goal is a genuine, honest attempt at the Clay Millennium
problem via evolutionary search over initial conditions — while never fooling ourselves with a
numerical artifact. WIN_CONDITION.md is the anti-self-deception contract: only Tier 3 (rigorous
proof) solves it; Tier 1 (candidate) and Tier 2 (resolution-confirmed) are progress. Preserve
that honesty — do not oversell. Raise genuine scope decisions for review with a short options
menu rather than deciding unilaterally.

USER'S STANDING STEER (honor it):
- Recalibrated ambition: the realistic prize is novel toy-model singularity research + a tiny
  (~0.05%) Clay "lottery ticket," NOT a Clay solve. Keep the lottery ticket the true focus; when
  something does NOT contribute to it, say so and be willing to pivot.
- Produce blog posts + scientific-community-useful writeups WITH ATTACHED DATA (writeup/ +
  committed writeup/data/*.json that rebuilds figures without re-runs). A deliverable.
- Our code was UNIFORM-GRID ONLY — a tier below the field's frontier. Phase 2 closed that gap:
  the stretched-grid dynamic-rescaling solver is built + validated in 1D (Spike 0), 2D (Spike 1),
  and now the 1D singular-profile machine (P2 anchor). The machinery exists. The lottery ticket
  is the NEXT thing — the P2 novelty leg (dynamic relaxation), NOT yet started.

TERMINOLOGY GUARD (do not drop): the dynamic-rescaling **numerics** upgrade is a solver upgrade
to **Route A**. It is NOT roadmap "Route D" (the later Tier-3 computer-assisted-proof leg, which
only exists after a Tier-2 candidate).

ORIENTATION (read in this order): PROJECT.md, WIN_CONDITION.md, CLAY_ROADMAP.md. Phase 1
(concluded, honest negative): writeup/NEGATIVE_RESULT_TWO_CURRENCIES.md. Spike 0 (COMPLETE):
writeup/TECHNICAL_SPIKE0_RESCALING.md. Spike 1 (COMPLETE — 2D Boussinesq machine, reproduced the
PROVEN Chen–Hou regular profile across "Wall C", gate PARTIAL): PHASE2_SPIKE1_NOTES.md + the three
writeups writeup/TECHNICAL_SPIKE1_{VELOCITY,STEPB,STEPC}.md. **P2 (JUST STARTED — read this):**
PHASE2_P2_NOTES.md (top status + §1–4), writeup/TECHNICAL_P2_HL_ANCHOR.md + BLOG_P2_HL_ANCHOR.md,
fig12. Then experiments/JOURNAL.md (newest first) and LOGGING.md.

STATE (all banked + pushed; origin/main at commit 28bbfc3 "Phase-2 P2 start"):
- Phase 1 CONCLUDED with a decisive honest negative (uniform grid can't resolve self-similar
  blow-up). Spike 0 DONE + VALIDATED (1D CLM dynamic rescaling). Spike 1 COMPLETE (2D Boussinesq
  dynamic-rescaling machine; reproduces the PROVEN Chen–Hou profile; Step-C gate PARTIAL 3/4,
  far-field-exponent check fails at POC fidelity — validated machinery, NOT novel, NOT a proof).
- **P2 VALIDATION ANCHOR DONE (this session) — the 1D Hou–Luo (HL) singular-profile machine.**
  Target: Chen–Huang–Li **arXiv:2604.01868** (Papers/, gitignored — `Read` page-by-page, WebFetch
  can't). Their novelty: *degenerate* data (ω⁰ₓ(0)=θ⁰ₓₓ(0)=0) → **singular** self-similar profiles
  via a **two-stage** L^∞→L^p blow-up. **Only weak existence of the explicit profile is proven
  (their Thm 2.3); the asymptotic STABILITY is numerical-only — that gap is the frontier.**
  - DECISION (with user, from evidence): attack **1D HL, not 2D Boussinesq** — the novelty lives
    there first, it reuses solver/line_hilbert.py (6/6) + gCLM rescaling (5/5), and 2D would
    compound the Step-C tail problem. Feasibility probe: line_hilbert SURVIVES the singular
    profile; only the slow X^{−1/2} tail is truncation-limited (the known outer-patch gap), core
    representable to a few %.
  - Rescaled HL dynamics (their (2.4), fields Ω,Θ, velocity U): Ω_τ+(U+c_l X)Ω_X=c_ω Ω+Θ_X;
    Θ_τ+(U+c_l X)Θ_X=(c_l+2c_ω)Θ; U_X=H(Ω), U(0)=0. Two new pieces vs CLM: U is the *integral*
    of H(Ω) pinned at U(0)=0; and the buoyancy field Θ.
  - Explicit exact anchor (Thm 2.3): Ω̄=(X−1)^{−1/2}1_{X>1}, Θ̄=(π/2)1_{X>1}, c̄_l=2, c̄_ω=−1.
    **Derived closed-form velocity** (classical Hilbert pair H(x₊^{−1/2})): H(Ω̄)=−(1−X)^{−1/2}1_{X<1},
    U̅=2√(1−X)−2 (X<1), −2 (X≥1). Checks: U̅(0)=0; U̅(1⁻)=−2 (strong steady form, Rmk 5.4);
    c̄_l+2c̄_ω=0 exactly (Θ eqn trivial). A small self-contained by-product the paper didn't spell out.
  - solver/hl_rescaled.py + test_hl_rescaled.py (**5/5**): velocity vs arctan(2X) 1.1e−5; pipeline
    1.8e−3; velocity on the singular anchor → U̅ converging at ½-order (the √-singularity of H);
    steady residual 6.2e−3 converging; c̄_l+2c̄_ω consistency exactly 0. fig12.
  - HONEST STATUS: this VALIDATES the singular machinery against a PROVEN (weak-existence) result
    and contributes the closed-form U̅ — but it is NOT novel and NOT a proof (Tier-1/2, same tier
    as Spike 1). The novelty leg is NOT yet started.
- PERFORMANCE (user-requested, this session): fixed the shared line_hilbert.py build bottleneck —
  batched Thomas slope solve (_slope_matrix 6.15s→0.29s, 21×), Horner+shared+shortened L(s) series
  (n=4001 matrix build 65s→19.7s, 3.3×), lazy Hilbert matrix in RescaledHL. HL suite >120s→3.9s.
  Accuracy IDENTICAL (line_hilbert 6/6, gclm 5/5, hl 5/5 — verified no error digit moved).

THE OPEN WORK — THE LOTTERY-TICKET LEG (P2 novelty; genuine scope decision — put a menu to user):
- **THE swing: the dynamic relaxation + degenerate-case normalization.** Build the SSPRK3 time
  stepper for (2.4) with a normalization that works when the origin slopes VANISH (CHH22's
  origin-slope gauge is degenerate for degenerate data — need a higher-order or norm-based gauge;
  see CHL §3 for their choice). **LOCK a predicate in git BEFORE the logged run.** Novelty target:
  does *generic smooth degenerate data* converge to the singular profile (the asymptotic stability
  CHL only asserted numerically)? A resolution-confirmed yes/no is a Tier-2-style contribution.
- Beyond that: unexplored degeneracy orders / profile families; the flagged-open link to Hou–Huang
  two-scale 3D-axisymmetric-Euler (HH23) — CHL call it "an intriguing question."
- The slow X^{−1/2} tail will need a fixed-τ (not fixed-step) protocol + a semi-analytic r^α outer
  patch + larger r_max (same fix flagged for Spike-1 Step-C polish). Bounded, known.
- NOTE the honest ceiling: even a clean stability confirmation REPRODUCES CHL's numerical claim —
  it's a Tier-2-style independent confirmation, useful and shareable, but the genuinely *new* math
  (a not-yet-seen profile, a rigor step, or the HH23 link) is harder and longer odds. Say which
  one any given run is going after, out loud.

ENVIRONMENT & WORKFLOW: .venv/bin/python (numpy + matplotlib; NO scipy — tridiag/solvers
hand-rolled). 8-worker ceiling (OMP_NUM_THREADS pinned). No pytest; run each suite as
`python test_X.py`. Suites: test_hl_rescaled.py (5/5, NEW) + test_line_hilbert.py (6/6) +
test_gclm_rescaled.py (5/5) + test_boussinesq_velocity.py (5/5) + test_boussinesq_transport.py
(5/5) + test_boussinesq_rescaled.py (8/8). Before ANY logged experimental run: pass the test gate
+ COMMIT (dirty-tree guard; gitignored experiments/*.log,*.npz,*.jsonl,*.out are fine). Solver dev
+ unit tests are NOT "logged gate runs"; still add each new solver test to the suite. Papers/
gitignored. One JOURNAL.md entry per experiment. Evidence rebuilds via
writeup/p2_hl_anchor_evidence.py (+ the spike scripts). Push to origin only when the user asks.
OPS: never `while pgrep -f script.py` (self-match hang); foreground `sleep` is blocked (use
background runs / Monitor); long/dense-matrix runs buffer — run python `-u` + flush and tail a
logfile, or use a background waiter/Monitor. Big dense Hilbert builds (n≥4001) take ~20s each even
after the speedups — reuse RescaledHL (Hmat is cached lazily), don't rebuild per config.

DISCIPLINE LESSONS BANKED (do not relearn):
- Ground the scheme in the paper; do NOT trial-and-error a known method. Un-fetchable → `Read` the
  Papers/ PDFs page-by-page; validate against a known answer (manufactured / exact solutions).
- Derive the exact answer where one exists (the closed-form U̅ here) and test against it — that is
  what makes a "known-answer" validation real. A stable-looking run can drift to a CONFIDENTLY
  WRONG number; when something drifts, MEASURE the rate vs a parameter to diagnose (truncation
  refines away; a BC/tail leak scales with the boundary/reach) before hand-waving.
- Singular profiles: the singular CORE is often fine; the SLOW TAIL is the real cost and is
  truncation-limited (semi-analytic outer patch, not brute force). Confirmed by a banded probe.
- Dynamic-rescaling normalization is a GAUGE. For DEGENERATE data the origin-slope gauge is itself
  degenerate — you must pick a higher-order/norm-based normalization. Never report a gauge INPUT as
  a result; the gauge-invariant α + shape are the real tests.
- Do NOT re-run to chase a locked predicate into a pass; report PARTIAL and locate the cause.
- Performance: profile before optimizing (the "obvious" O(N³) matmul was NOT the bottleneck — the
  transcendental L(s) series build was). Preserve accuracy digit-for-digit across any speedup and
  re-run the full affected gate to prove it.

HONEST FRAMING TO PRESERVE: 1D HL is a toy model (it models the boundary behaviour of the Hou–Luo
/ 3D-axisymmetric-Euler scenario; 2D Boussinesq is closer but still a toy, not 3D NS). P2's anchor
reproduced a PROVEN (weak-existence) result — validates machinery, NOT novel, NOT a proof. Overall
Clay odds ~0.05%. The lottery ticket lives on the far side of the dynamic relaxation (the stability
of the singular profile), and probably in direct profile/stability construction more than
GA-over-ICs. Keep saying the honest version out loud.
