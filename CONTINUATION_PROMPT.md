# Continuation prompt (copy into a fresh session)

*Written 2026-07-24 at the end of the session that GROUNDED Phase-2 Spike 1 (the 2D
Boussinesq dynamic-rescaling port) in the source papers and BUILT + validated its crux
piece, Step A (the 2D velocity operator on a stretched grid), against a manufactured known
answer — packaged as a writeup. Everything below is banked + pushed to origin/main. Paste
the block to resume.*

Continue the Navier–Stokes blow-up search project in this directory
(/home/andy/projects/Unsolved). The goal is a genuine, honest attempt at the Clay
Millennium problem via evolutionary search over initial conditions — while never fooling
ourselves with a numerical artifact. WIN_CONDITION.md is the anti-self-deception contract:
only Tier 3 (rigorous proof) solves it; Tier 1 (candidate) and Tier 2 (resolution-
confirmed) are progress. Preserve that honesty — do not oversell. Raise genuine scope
decisions for review with a short options menu rather than deciding unilaterally.

USER'S STANDING STEER (honor it):
- Recalibrated ambition: the realistic prize is novel toy-model singularity research + a
  tiny (~0.05%) Clay "lottery ticket," NOT a Clay solve. Keep the lottery ticket the true
  focus; when something does NOT contribute to it, say so and be willing to pivot.
- Produce blog posts + scientific-community-useful writeups WITH ATTACHED DATA (writeup/ +
  committed writeup/data/*.json that rebuilds figures without re-runs). A deliverable.
- Our code was UNIFORM-GRID ONLY — a tier below the field's frontier. Phase 2 is closing
  that gap; the stretched-grid rescaling solver is built in 1D (Spike 0) and the 2D port
  (Spike 1) is now in progress — its crux velocity operator is built + validated.

TERMINOLOGY GUARD (do not drop): the dynamic-rescaling **numerics** upgrade is a solver
upgrade to **Route A**. It is NOT roadmap "Route D" (the later Tier-3 computer-assisted-
proof leg, which only exists after a Tier-2 candidate).

ORIENTATION (read in this order): PROJECT.md, WIN_CONDITION.md, CLAY_ROADMAP.md. Phase 1
result (concluded, honest negative): writeup/NEGATIVE_RESULT_TWO_CURRENCIES.md. Phase 2
Spike 0 (COMPLETE): writeup/TECHNICAL_SPIKE0_RESCALING.md, writeup/BLOG_SPIKE0_RESCALING.md,
PHASE2_SPIKE0_NOTES.md. **Phase 2 Spike 1 (IN PROGRESS — the current frontier):**
PHASE2_SPIKE1_NOTES.md (the working doc — read its top status + §1–3),
writeup/TECHNICAL_SPIKE1_VELOCITY.md (Step A, built+validated),
writeup/BLOG_SPIKE1_STEPA.md. Decision/derivation record: PHASE2_NUMERICS_PLAN.md,
writeup/TECHNICAL_PHASE2_RESCALING.md. Then experiments/JOURNAL.md (newest first) and
LOGGING.md.

STATE (all banked + pushed; origin/main at the Spike-1 Step-A writeup commit):
- Phase 1 (2D Boussinesq uniform-grid fitness search) CONCLUDED with a decisive honest
  negative: two currencies both fail a pre-committed cheat-audited gate via the same
  free-split ω₀→0 wall; root cause = on a uniform grid the singular structure forms below
  grid scale. Standalone: writeup/NEGATIVE_RESULT_TWO_CURRENCIES.md.
- Phase 2 DECISION (with user): build dynamic self-similar rescaling (P1), reject AMR.
  Honest catch: the field's real novelty frontier is P2 direct construction of UNSTABLE/
  singular profiles, not evolve-ICs search — so P1 rescaling is the shared substrate;
  re-decide "evolve ICs vs hunt profiles" at a gate AFTER Spike 1.
- Spike 0 DONE + VALIDATED: 1D CLM dynamic rescaling recovers Ω̄₀=−4X/(1+4X²), c_ω→−1,
  shape err ~2e-6, resolution-stable. solver/line_hilbert.py, solver/gclm_rescaled.py;
  tests test_line_hilbert.py (6/6), test_gclm_rescaled.py (5/5). Headline: one-scale
  rescaling is stable/attracting for CLM (overturned the recon two-scale fear).
- **Spike 1 Step A DONE + VALIDATED (this session).** The user chose Spike 1 (2D Boussinesq
  port), DE-RISKED variant: build+validate the highest-risk piece — the 2D velocity operator
  `u = ∇^⊥(−Δ)⁻¹ω` — standalone against a known answer before the full solver.
  - GROUNDED in the source (Papers/ — gitignored; user downloaded, `Read` handles PDFs
    page-by-page since WebFetch hit a size limit). Chen–Hou Part I arXiv:2210.07191
    §2/§7 + MMS-Numerics-2025 (2305.05660) §2. Physical (2.3)–(2.5): ω_t+u·∇ω=θ_x,
    θ_t+u·∇θ=0, −Δφ=ω, u=−φ_y, v=φ_x, φ=0 on wall y=0; ω odd-x, θ even-x → first-quadrant
    Hou–Luo geometry. One-scale rescaling (2.10): ω_τ+(c_l x+u)·∇ω=θ_x+c_ω ω,
    θ_τ+(c_l x+u)·∇θ=c_θ θ, c_θ=c_l+2c_ω; modulation (2.11): c_l=2θ_xx(0)/ω_x(0),
    c_ω=½c_l+u_x(0). Far-field ω~r^α, α=c_ω/c_l≈−1/3; **gate target c_l/c_ω≈−2.92,
    c_ω<0**. NOTE: the "two-scale" worry was from Chen–Hou's earlier C^{1,α} paper, NOT
    this smooth-data profile — it is ONE-SCALE.
  - BUILT: solver/boussinesq_velocity.py. On a log-radial (r=e^ρ) × angular-sine (sin(2nβ),
    DST-I) quarter-plane grid, the polar Laplacian's 1/r,1/r² terms CANCEL and −Δφ=ω
    decouples per mode into a constant-coeff tridiagonal ODE φ_n''(ρ)−(2n)²φ_n=−r²ω_n
    (Thomas solve, no scipy sparse). r^{±2n} homogeneous tails = origin-regularity +
    far-field decay (the r^{−1/3} lever, POC-level). u_x(0) read cleanly by extrapolating
    the n=1 coefficient φ₁/r² → r=0 (dodges the 1D-recon high-derivative noise trap).
  - VALIDATED vs a manufactured known answer (test_boussinesq_velocity.py, 5/5): recover
    u,v to rel L∞ ~6e-5, radial convergence order 2.00, u_x(0)=−2.0008 (target −2, tol
    1e-3). Evidence: writeup/figures/fig9_spike1_stepA_velocity.png + committed data
    (rebuild: python writeup/spike1_stepA_evidence.py).
  - HONEST POC SCOPE (explicit, flagged to user): Chen–Hou's full apparatus (B-spline FEM
    Poisson, adaptive mesh to 10¹⁵, semi-analytic far-field split, 10⁻⁷ residual, INTLAB
    interval bounds) is months-scale and mostly for the PROOF. Plan pre-committed Spike 1
    to qualitative fidelity, so Step A uses a tractable VALIDATED Poisson solve (legit — an
    elliptic solve is textbook, unlike the exotic 1D line Hilbert) with the same math.

THE OPEN WORK (Spike 1 continues; each step validated before trusting it):
- **Step B — the rescaled solver.** Wire the velocity operator into the rescaled system
  (2.10): transport (c_l x + u)·∇ (upwind/WENO-lite on the stretched grid, per Spike 0),
  buoyancy θ_x, reaction c_ω ω / c_θ θ; modulation ODEs (2.11) from the origin slopes;
  SSPRK time-stepping in τ. Introduces the ζ=θ/x substitution (θ vanishes quadratically —
  the paper evolves ζ). Build incrementally with piece-tests (transport-only translation,
  buoyancy, then modulation).
- **Step C — the Spike-1 gate.** Relax perturbed data to the steady profile; check shape +
  α≈−1/3 / c_l/c_ω≈−2.92, resolution-stable. Pre-committed predicate written before the
  logged run.
- **Post-Spike-1 gated decisions (deferred, per the plan):** (i) stable-vs-singular target
  — the user raised this fork; deferred here because both share Steps A–B and the working
  machine can then probe both cheaply (singular target = Chen–Huang–Li arXiv:2604.01868,
  the De-Huang-group extension in Papers/); (ii) evolve-ICs vs hunt-profiles [P2].

ENVIRONMENT & WORKFLOW: .venv/bin/python (numpy + matplotlib; NO scipy — spline/tridiag
solvers hand-rolled). 8-worker ceiling (OMP_NUM_THREADS pinned). No pytest; run each suite
as `python test_X.py`. Solver tests test_line_hilbert.py (6/6) + test_gclm_rescaled.py
(5/5) + test_boussinesq_velocity.py (5/5) are ~1–2 min total. Before ANY logged
experimental run, verify the pre-run test gate passes and COMMIT (dirty-tree guard refuses
uncommitted .py; gitignored experiments/*.jsonl + *.out fine). Solver dev + unit tests are
NOT "logged gate runs"; still add each new solver test to the suite as it lands. Papers/ is
gitignored (copyrighted PDFs). Multiprocessing dispatchers MUST be module-level. One
JOURNAL.md entry per experiment. Writeup evidence rebuilds via writeup/build_figures.py
(Phase-1) + writeup/spike0_rescaling_evidence.py (Spike 0) + writeup/spike1_stepA_evidence.py
(Spike 1 Step A) + writeup/curate_evidence.py. Push to origin only when the user asks. OPS:
never `while pgrep -f script.py` (self-match hang); foreground `sleep` is blocked (use
background runs / the Monitor tool).

DISCIPLINE LESSONS BANKED (do not relearn):
- Ground the scheme in the paper; do NOT trial-and-error a known numerical method. When the
  paper's text is OCR-mangled or un-fetchable, DERIVE/validate analytically against a known
  answer (the 1D A,B coefficients; the 2D log-grid decoupling). WebFetch cannot ingest the
  big papers — read the PDFs in Papers/ with `Read` (page ranges).
- A stable-looking run can converge to a CONFIDENTLY WRONG number. Validate against a known
  answer before trusting anything (manufactured solutions for the 2D operators).
- The uniform grid is the wrong tool for self-similar blow-up; the stretched non-uniform
  grid is the enabler and forces non-FFT operators (1D line Hilbert; 2D Poisson-on-log-grid).
- High-order pointwise ORIGIN reads are noise amplifiers; prefer integral / mode-localized
  reads (u_x(0) via the n=1 coefficient extrapolated to r=0).

HONEST FRAMING TO PRESERVE: 2D Boussinesq is a toy model, not 3D NS. A flawless Spike-1
solver reproduces a PROVEN result (Chen–Hou 2022) across "Wall C" (2D Boussinesq ≠ 3D NS) —
validates machinery, not novel, not a proof. Overall Clay odds ~0.05%. The lottery ticket
lives on the far side of this solver, and (per the banked catch) probably in profile
construction (P2) more than in GA-over-ICs. Keep saying the honest version out loud.
