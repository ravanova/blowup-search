# Continuation prompt (copy into a fresh session)

*Written 2026-07-24 at the end of the session that BUILT and validated Phase-2 Spike 0
(dynamic self-similar rescaling in 1D) against the CLM known answer, and packaged it as a
writeup. Everything below is banked + pushed to origin/main. Paste the block to resume.*

*(This is the single canonical resume prompt; the old NEXT_SESSION_PROMPT.md was stale
and was removed.)*

---

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
- Our code was UNIFORM-GRID ONLY — a tier below the field's frontier (Hou–Luo/Chen–Hou/
  Elgindi/Buckmaster–Gómez-Serrano use adaptive/self-similar-rescaled numerics + construct
  self-similar profiles). Phase 2 is closing exactly that gap; the stretched-grid rescaling
  solver is now built in 1D.

TERMINOLOGY GUARD (do not drop): the dynamic-rescaling **numerics** upgrade is a solver
upgrade to **Route A**. It is NOT roadmap "Route D" (the later Tier-3 computer-assisted-
proof leg, which only exists after a Tier-2 candidate).

ORIENTATION (read in this order): PROJECT.md, WIN_CONDITION.md, CLAY_ROADMAP.md. Phase 1
result (concluded, honest negative): writeup/NEGATIVE_RESULT_TWO_CURRENCIES.md. **Phase 2
Spike 0 (JUST COMPLETED — the current frontier)**: writeup/TECHNICAL_SPIKE0_RESCALING.md
(the built+validated result), writeup/BLOG_SPIKE0_RESCALING.md, and PHASE2_SPIKE0_NOTES.md
(the working doc — read its top status + the "SPIKE 0 COMPLETE" section). Decision +
derivation record: PHASE2_NUMERICS_PLAN.md, writeup/TECHNICAL_PHASE2_RESCALING.md. Then
experiments/JOURNAL.md (newest first) and LOGGING.md.

STATE (all banked + pushed; origin/main at the Spike-0 writeup commit):
- Phase 1 (2D Boussinesq uniform-grid fitness search) CONCLUDED with a decisive honest
  negative: two currencies (ν_crit, g_frac) both fail a pre-committed cheat-audited gate
  via the same free-split ω₀→0 wall; root cause = on a uniform grid the singular structure
  forms below grid scale. Standalone: writeup/NEGATIVE_RESULT_TWO_CURRENCIES.md.
- Phase 2 DECISION (with the user): build dynamic self-similar rescaling (P1) — reuses the
  validated solver, resolves the singular region, on-ramp to profile construction — reject
  AMR. Honest catch banked: the field's real novelty frontier is P2 direct profile
  construction of UNSTABLE profiles, not evolve-ICs search — so P1 rescaling is the shared
  substrate; re-decide "evolve ICs vs hunt profiles" at a gate AFTER Spike 1.
- **Spike 0 DONE + VALIDATED (this session).** Dynamic rescaling built in 1D on CLM (a=0)
  and checked against the closed-form answer. Files: solver/line_hilbert.py,
  solver/gclm_rescaled.py; tests test_line_hilbert.py (6/6), test_gclm_rescaled.py (5/5);
  figure writeup/figures/fig8_spike0_rescaling.png (rebuild: python
  writeup/spike0_rescaling_evidence.py). Results:
  - CRUX — the **line** Hilbert transform on a non-uniform (sinh-stretched) grid recovers
    the known pair −4X/(1+4X²) → 2/(1+4X²) to rel err 1.6e-4. The stability-critical A,B
    basis-Hilbert coefficients were DERIVED analytically (ln|1−s| = L(s)−s−s²/2−s³/3,
    L=−Σ_{n≥4}sⁿ/n, cancels the s→0 blowup) — NOT transcribed from the paper's mangled
    minimax, which is therefore unneeded. Node slopes via a hand-rolled natural cubic
    spline (no scipy in the venv). line_hilbert_matrix(x) = a reusable dense operator.
  - SOLVER — reducing for CLM (evolve f=Ω/X, k=1; c_l≡1, c_ω=1−HΩ(0)) in the computational
    coord ρ (X=c·sinh ρ) gives f_τ = −tanh(ρ)f_ρ + (HΩ−HΩ(0))f; the dilation is now bounded
    (speed ≤1) so CFL ~ Δρ independent of reach M (uniform-grid CFL death CURED). 3rd-order
    upwind + SSPRK3. Perturbed odd data (2 different bumps) relaxes onto Ω̄₀: shape err
    ~2e-6, c_ω→−0.999, resolution-stable (c_ω −0.9986→−0.9995 refining). Origin slope
    f(0)=−4 frozen to machine precision by the scheme.
  - HEADLINE FINDING (overturns recon finding-3): one-scale rescaling is STABLE and
    attracting for CLM — the earlier apparent one-scale instability was an artifact of the
    WRONG (periodic) Hilbert transform + integral modulation, not fundamental. (Chen–Hou's
    two-scale need was for Boussinesq/De Gregorio — a different mechanism; may or may not
    recur in Spike 1.)
  - HONEST SCOPE (kept explicit): reproduces a PROVEN closed-form toy result across Wall C
    — validates machinery, NOT novel, NOT a proof. Physical T*=2 deliberately NOT claimed
    from a whole-line run (its initial amplitude is a free gauge; the local analogue is the
    rate c_ω→−1). The log-kernel velocity U (Appendix-C.1 C,D elements) was correctly
    deferred — CLM (a=0) does not use it; it is the first thing a≠0 / the 2D port needs.

KNOWN-ANSWER TARGET (CLM, a=0), for reference: ω₀=−sin x → blow-up at x=0, T*=2, exact
profile Ω̄₀(X)=−4X/(1+4X²), HΩ̄₀=2/(1+4X²), c_ω→−1, c_l=1.

THE DECISION AT THE GATE (Spike 0 stops for review — this is the open fork; the user has
NOT yet chosen; present it as an options menu with a recommendation, do not assume):
- OPTION 1 — Spike 1: port the rescaling machinery to solver/boussinesq.py (2D Boussinesq,
  Hou–Luo geometry) and reproduce the published Chen–Hou self-similar profile as the
  validation gate. THE PLANNED REAL LIFT (multi-week). Needs: the 2D analogue of the line
  Hilbert/Riesz transform + velocity U, the 2D rescaled RHS + modulation, likely one-scale
  → two-scale IF a scaling instability appears (the CLM result says it need not). Reproduces
  a PROVEN profile — validation toward the relevant model, not novelty.
- OPTION 2 — 1D a<0 singular-profile extension (cheaper): add the deferred log-kernel
  velocity U (Appendix-C.1 C,D integral elements) + AMR mesh regeneration near the X=1
  singularity, targeting the a<0 gCLM singular self-similar profiles (arXiv:2603.25104
  §5–6). Richer 1D validation; builds U+AMR machinery that transfers to 2D; still
  reproduces published results.
- (After Spike 1, per the plan: the gated "evolve ICs vs hunt profiles [P2]" decision.)

ENVIRONMENT & WORKFLOW: .venv/bin/python (numpy + matplotlib; NO scipy — spline solvers are
hand-rolled). 8-worker ceiling (OMP_NUM_THREADS pinned). No pytest; run each suite as
`python test_X.py`. The solver tests test_line_hilbert.py (6/6) + test_gclm_rescaled.py
(5/5) are ~1 min total. Before ANY logged experimental run, verify the pre-run test gate
passes and COMMIT (the dirty-tree guard refuses uncommitted .py; gitignored
experiments/*.jsonl + *.out are fine). NOTE: solver development + unit tests are NOT "logged
gate runs"; still add each new solver test to the suite as it lands. Multiprocessing
dispatchers MUST be module-level. One JOURNAL.md entry per experiment. Writeup evidence
rebuilds via writeup/build_figures.py (Phase-1) + writeup/spike0_rescaling_evidence.py
(Spike 0) + writeup/curate_evidence.py. Push to origin only when the user asks. OPS: never
`while pgrep -f script.py` (self-match hang); foreground `sleep` is blocked (use background
runs / the Monitor tool).

DISCIPLINE LESSONS BANKED (do not relearn):
- Ground the scheme in the paper; do NOT trial-and-error a known numerical method. Every
  reinvented piece of dynamic rescaling was wrong (3 false starts in recon). BUT: when the
  paper's text is OCR-mangled, DERIVING the formula analytically and verifying it against a
  known answer beat transcription (the A,B coefficients — see Spike 0).
- A stable-looking run can converge to a CONFIDENTLY WRONG number (the periodic-H profile).
  Validate against a known answer before trusting anything.
- The uniform grid is the wrong tool for self-similar blow-up (below-grid structure for the
  search; CFL-strangled dilation for the solver). The stretched non-uniform grid is the
  enabler and forces the non-FFT (spline-analytic) line Hilbert transform.

HONEST FRAMING TO PRESERVE: 2D Boussinesq is a toy model, not 3D NS. A flawless rescaling
solver reproduces a PROVEN result (Chen–Hou 2022) across "Wall C" (2D Boussinesq ≠ 3D NS) —
validates machinery, not novel, not a proof. Overall Clay odds ~0.05%. The lottery ticket
lives on the far side of this solver, and (per the banked catch) probably in profile
construction (P2) more than in GA-over-ICs. Keep saying the honest version out loud.
