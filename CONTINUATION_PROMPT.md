# Continuation prompt (copy into a fresh session)

*Written 2026-07-25 at the end of the session that COMPLETED Phase-2 Spike 1 (the 2D
Boussinesq dynamic-rescaling port): built + validated the full rescaled solver (Step B),
then ran the gate (Step C) — diagnosed a relaxation drift, fixed it with gauge
renormalization, and got a PARTIAL result reported straight against a pre-committed
predicate. Everything below is banked + pushed to origin/main. Paste the block to resume.*

Continue the Navier–Stokes blow-up search project in this directory
(/home/andy/projects/Unsolved). The goal is a genuine, honest attempt at the Clay Millennium
problem via evolutionary search over initial conditions — while never fooling ourselves with
a numerical artifact. WIN_CONDITION.md is the anti-self-deception contract: only Tier 3
(rigorous proof) solves it; Tier 1 (candidate) and Tier 2 (resolution-confirmed) are
progress. Preserve that honesty — do not oversell. Raise genuine scope decisions for review
with a short options menu rather than deciding unilaterally.

USER'S STANDING STEER (honor it):
- Recalibrated ambition: the realistic prize is novel toy-model singularity research + a tiny
  (~0.05%) Clay "lottery ticket," NOT a Clay solve. Keep the lottery ticket the true focus;
  when something does NOT contribute to it, say so and be willing to pivot.
- Produce blog posts + scientific-community-useful writeups WITH ATTACHED DATA (writeup/ +
  committed writeup/data/*.json that rebuilds figures without re-runs). A deliverable.
- Our code was UNIFORM-GRID ONLY — a tier below the field's frontier. Phase 2 closed that gap:
  the stretched-grid dynamic-rescaling solver is now built + validated in 1D (Spike 0) AND 2D
  (Spike 1, this frontier). The machinery exists. The lottery ticket is the NEXT thing (P2).

TERMINOLOGY GUARD (do not drop): the dynamic-rescaling **numerics** upgrade is a solver
upgrade to **Route A**. It is NOT roadmap "Route D" (the later Tier-3 computer-assisted-proof
leg, which only exists after a Tier-2 candidate).

ORIENTATION (read in this order): PROJECT.md, WIN_CONDITION.md, CLAY_ROADMAP.md. Phase 1
(concluded, honest negative): writeup/NEGATIVE_RESULT_TWO_CURRENCIES.md. Spike 0 (COMPLETE):
writeup/TECHNICAL_SPIKE0_RESCALING.md. **Spike 1 (COMPLETE — the machinery just finished):**
PHASE2_SPIKE1_NOTES.md (working doc — read top status + §1–3), and the three Step writeups
writeup/TECHNICAL_SPIKE1_VELOCITY.md (A), writeup/TECHNICAL_SPIKE1_STEPB.md (B),
writeup/TECHNICAL_SPIKE1_STEPC.md (C) + their BLOG_SPIKE1_STEP*.md. Then experiments/JOURNAL.md
(newest first) and LOGGING.md.

STATE (all banked + pushed; origin/main at the Spike-1 Step-C writeup commit 51b63b2):
- Phase 1 CONCLUDED with a decisive honest negative (uniform grid can't resolve self-similar
  blow-up: structure forms below grid scale). writeup/NEGATIVE_RESULT_TWO_CURRENCIES.md.
- Spike 0 DONE + VALIDATED: 1D CLM dynamic rescaling recovers Ω̄₀=−4X/(1+4X²), c_ω→−1, shape
  err ~2e-6, resolution-stable. One-scale rescaling is stable/attracting for CLM.
- **Spike 1 COMPLETE (this session) — the 2D Boussinesq dynamic-rescaling machine, end-to-end.**
  Grounded in Chen–Hou Part I (arXiv:2210.07191, in Papers/ — gitignored; `Read` the PDF page-
  by-page, WebFetch can't). Physical (2.3)–(2.5), one-scale rescaling (2.10), modulation (2.11)/
  (2.12); precise gate constants (2.23): c̄_l≈3.006499, c̄_ω≈−1.029425, ū_x(0)≈−2.532674,
  c̄_l/c̄_ω≈−2.92056, α=c̄_ω/c̄_l≈−0.3424.
  - Step A (velocity operator u=∇^⊥(−Δ)⁻¹ω): solver/boussinesq_velocity.py,
    test_boussinesq_velocity.py (5/5). Log-radial × angular-sine grid; −Δφ=ω decouples per mode
    into a tridiagonal ODE. Manufactured rel L∞ ~6e-5, order 2.00, u_x(0)=−2.0008. fig9.
  - Step B (full rescaled solver): solver/boussinesq_rescaled.py, test_boussinesq_transport.py
    (5/5) + test_boussinesq_rescaled.py (8/8). Evolves the 3-field **(ω, η=θ_x, ξ=θ_y)** system
    (2.28) — the variable choice was DECIDED BY EXPERIMENT (the user asked "are there tests?":
    experiments/spike1_stepB_decide_formulation.py showed the η-slope θ_xx(0) read ~2× better +
    noise-robust than primitive-θ). RHS: transport (2D upwind on the log-polar grid, Spike-0 Shu
    stencil generalized; order ~2.98), buoyancy η, reaction (2c_ω∓u_x), modulation, SSPRK3.
    c_l=2η_x(0)/ω_x(0) recovered to ~3e-16 (quadrature bias cancels in the ratio). fig10.
  - Step C (the gate — LOGGED, PARTIAL): experiments/spike1_stepC_gate.py (predicate LOCKED in
    git before the run, commit eabb418). **3 of 4 pre-committed checks PASS, the far-field-
    exponent check FAILS → does NOT pass the gate; goalposts NOT moved.** The initial relaxation
    DRIFTED; diagnosed (experiments/diagnose_stepC_drift.py) as a near-origin truncation artifact
    (halves under n_r, worsens with smaller r_min) — NOT a broken method — and fixed with **gauge
    renormalization** (RescaledBoussinesq.run(renorm=True), discrete enforcement of (2.12);
    test_renorm_pins_gauge). With the fix: c_ω matches Chen–Hou to **<0.5%** (−1.026…−1.031 vs
    −1.0294) across all configs, α≈−0.335 (~2%, resolution-stable), anisotropy ≈0.026 ≪ 0.23
    (2.24). The directly-fitted far-field exponent (≈−0.31) fails, partly a protocol confound
    (fixed steps → higher-n_r under-relaxed) and partly the POC limit (domain 1e5–1e6 vs paper
    1e15, no semi-analytic r^α split, 2nd–3rd order vs 6th–8th B-splines). fig11.
  - HONEST STATUS: the machine captures the profile's *invariants + anisotropic core* but not the
    full r^{−1/3} tail at POC fidelity — exactly where the paper needed its heavy apparatus.
    Tier-1/2: machinery VALIDATED end-to-end (reproduces a PROVEN result across Wall C), NOT
    novel, NOT a proof.

THE OPEN WORK — now the POST-Spike-1 forks, i.e. THE LOTTERY TICKET (genuine scope decisions,
put a short menu to the user; both were deferred to "after Spike 1" and the machine is ready):
- **(P2) hunt an UNSTABLE / not-already-proven profile** — the actual novelty frontier. Candidate
  target: the stable-vs-singular extension Chen–Huang–Li arXiv:2604.01868 (Papers/), or a
  3D-axisymmetric-with-boundary analogue. This is where a Clay lottery ticket could live.
- **evolve-ICs vs hunt-profiles**: re-decide now with the working machine (the banked catch:
  the field's real novelty is direct profile construction, not GA-over-ICs).
- **OPTIONAL Step-C polish (only if it feeds the ticket)**: close the far-field gap with a
  fixed-τ (not fixed-step) relaxation protocol + a semi-analytic r^α outer patch + larger r_max.
  This would upgrade Step C toward a full pass but only reproduces a PROVEN result — low priority
  vs P2 unless the user wants the clean validation.

ENVIRONMENT & WORKFLOW: .venv/bin/python (numpy + matplotlib; NO scipy — tridiag/solvers hand-
rolled). 8-worker ceiling (OMP_NUM_THREADS pinned). No pytest; run each suite as
`python test_X.py`. Spike suites: test_boussinesq_velocity.py (5/5) + test_boussinesq_transport.py
(5/5) + test_boussinesq_rescaled.py (8/8) + test_gclm_rescaled.py (5/5) + test_line_hilbert.py
(6/6). Before ANY logged experimental run: pass the test gate + COMMIT (dirty-tree guard;
gitignored experiments/*.log,*.npz,*.jsonl,*.out are fine). Solver dev + unit tests are NOT
"logged gate runs"; still add each new solver test to the suite. Papers/ gitignored. One
JOURNAL.md entry per experiment. Evidence rebuilds via writeup/spike1_step{A,B,C}_evidence.py
(committed data → figures). Push to origin only when the user asks. OPS: never `while pgrep -f
script.py` (self-match hang); foreground `sleep` is blocked (use background runs / Monitor);
long relaxations buffer — run python `-u` + flush and tail a logfile, or use a background waiter.

DISCIPLINE LESSONS BANKED (do not relearn):
- Ground the scheme in the paper; do NOT trial-and-error a known method. Un-fetchable → `Read`
  the Papers/ PDFs page-by-page; validate against a known answer (manufactured solutions).
- A stable-looking run can converge to / drift toward a CONFIDENTLY WRONG number. Validate, and
  when something drifts, MEASURE the rate vs a parameter to diagnose (truncation refines away;
  a BC leak scales with the boundary) before hand-waving.
- Uniform grid is wrong for self-similar blow-up; stretched grid forces non-FFT operators.
- High-order pointwise ORIGIN reads are noise amplifiers; prefer mode-localized/ratio reads
  (c_l as a ratio has its quadrature bias cancel). Let DATA pick formulation forks.
- Dynamic-rescaling normalization is a GAUGE: c_l is pinned by the initial slopes (an input),
  so the gauge-INVARIANT α + shape are the real tests — never report an input as a result.
- Discrete drift of the frozen origin slopes → enforce (2.12) by RENORMALIZING each step.
- Do NOT re-run to chase a locked predicate into a pass; report PARTIAL and locate the cause.

HONEST FRAMING TO PRESERVE: 2D Boussinesq is a toy model, not 3D NS. Spike 1 reproduced a PROVEN
result (Chen–Hou 2022) across "Wall C" — validates machinery, not novel, not a proof. Overall
Clay odds ~0.05%. The lottery ticket lives on the far side of this solver, and (per the banked
catch) probably in profile construction (P2) more than in GA-over-ICs. Keep saying the honest
version out loud.
