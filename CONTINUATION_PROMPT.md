# Continuation prompt (copy into a fresh session)

*Written 2026-07-24 at the end of the session that concluded Phase 1's writeup and
opened Phase 2 (the dynamic-rescaling numerics upgrade). Everything below is banked +
pushed to origin/main. Paste this whole block to resume.*

---

Continue the Navier–Stokes blow-up search project in this directory
(/home/andy/projects/Unsolved). The goal is a genuine, honest attempt at the Clay
Millennium problem via evolutionary search over initial conditions — while never
fooling ourselves with a numerical artifact. WIN_CONDITION.md is the anti-self-
deception contract: only Tier 3 (rigorous proof) solves it; Tier 1 (candidate) and
Tier 2 (resolution-confirmed) are progress. Preserve that honesty — do not oversell.
Raise genuine scope decisions for review with a short options menu rather than
deciding unilaterally.

USER'S STANDING STEER (honor it):
- Recalibrated ambition: the realistic prize is novel toy-model singularity research
  + a tiny (~0.05%) Clay "lottery ticket," NOT a Clay solve. Keep the lottery ticket
  as the true focus; when something does NOT contribute to it, say so and be willing
  to pivot.
- Produce blog posts + scientific-community-useful writeups WITH ATTACHED DATA
  (writeup/ + committed writeup/data/*.json). A deliverable, not optional.
- Our code is competent grad-student-grade infra but was UNIFORM-GRID ONLY — a tier
  below the field's frontier (Hou–Luo/Chen–Hou/Elgindi/Buckmaster–Gómez-Serrano use
  adaptive/self-similar-rescaled numerics + construct self-similar profiles). Phase 2
  is closing exactly that gap.

TERMINOLOGY GUARD (do not drop): the dynamic-rescaling / AMR **numerics** upgrade is a
solver upgrade to **Route A**. It is NOT roadmap "Route D" (the later Tier-3 computer-
assisted-proof leg, which only exists after a Tier-2 candidate).

ORIENTATION (read in this order): PROJECT.md, WIN_CONDITION.md, CLAY_ROADMAP.md,
PHASE1_PLAN.md. Phase 1 result (concluded, honest negative): writeup/
NEGATIVE_RESULT_TWO_CURRENCIES.md (the standalone note), PHASE1_GATE4_REFORM_RESULTS.md.
**Phase 2 (current)**: PHASE2_NUMERICS_PLAN.md (the decision), PHASE2_SPIKE0_NOTES.md
(THE ACTIVE WORKING DOC — exact scheme + Appendix C build recipe + findings),
writeup/TECHNICAL_PHASE2_RESCALING.md, writeup/BLOG_PHASE2_RESCALING.md. Then
experiments/JOURNAL.md (newest first) and LOGGING.md.

STATE (all banked + pushed; origin/main at the Phase-2 writeup commit):
- Phase 1 (2D Boussinesq uniform-grid fitness search) is CONCLUDED with a decisive
  honest negative: two currencies (ν_crit, g_frac) both fail a pre-committed cheat-
  audited gate via the same free-split ω₀→0 wall; root cause = on a uniform grid the
  singular structure forms below grid scale. Packaged standalone in
  writeup/NEGATIVE_RESULT_TWO_CURRENCIES.md.
- Phase 2 DECISION (with the user): build dynamic self-similar rescaling (reuses the
  validated solver, resolves the singular region, on-ramp to profile construction),
  reject AMR. Honest catch banked: the field's real novelty frontier is P2 direct
  profile construction of UNSTABLE profiles, not evolve-ICs search — so P1 rescaling
  is the shared substrate; re-decide "evolve ICs vs hunt profiles" at a gate AFTER
  Spike 1.
- Spike 0 (dynamic rescaling in 1D on gCLM, validated against a KNOWN answer before
  the 2D port) is SCOPED + DE-RISKED but the SOLVER IS NOT BUILT. Reconnaissance banked
  (PHASE2_SPIKE0_NOTES.md): exact scheme grounded in Huang–Tong–Wang arXiv:2603.25104;
  three false starts each a finding (pointwise-derivative normalization = noise
  amplifier; periodic grid converges to the WRONG profile since periodic H ≠ line H for
  the ~1/X tail; uniform whole-line grid is CFL-strangled by the −c_l X Ω_X dilation);
  and the full Appendix-C recipe.

KNOWN-ANSWER TARGET (CLM, a=0): data ω₀=−sin x → blow-up at x=0, T*=2, exact profile
Ω̄₀(X)=−4X/(1+4X²), HΩ̄₀=2/(1+4X²), c_ω→−1, c_l=1. Rescaled eqn (a=0):
Ω_τ=(c_ω+HΩ)Ω − c_l X Ω_X, normalization c_l=1, c_ω=1−HΩ(0).

THE IMMEDIATE NEXT STEP (agreed, not yet done): begin the Spike-0 build, in dependency
order (each a clean testable milestone):
 1. solver/line_hilbert.py + test_line_hilbert.py — the Appendix-C.1 spline-analytic
    LINE Hilbert transform on a non-uniform grid (C¹₀ cubic-spline basis; analytic
    H(P_i),H(Q_i) with closed-form A,B,C,D + Mathematica minimax series near s=0).
    THE CRUX. Unit-test to the paper's accuracy against −4X/(1+4X²) ↔ 2/(1+4X²).
    IMPORTANT: pdftotext mangles the A,B,C,D fraction formulas — re-read the exact
    formula region of the PDF (arxiv.org/pdf/2603.25104, Appendix C, ~p.49–52) when
    transcribing; do not trust the mangled text.
 2. the stretched cosh/sinh grid X(ρ)=X_m(1−cosh ρ)+√(c+X_m²) sinh ρ (dX~X·Δρ makes
    the dilation CFL ~Δρ, independent of M) + WENO5 advection + SSPRK(10,4) time
    integration of the rescaled equation, evolving f=Ω/Xᵏ (k=1 for non-degenerate CLM).
 3. test_gclm_rescaled.py — pre-committed CLM success predicate: Ω→Ω̄₀ (shape err<tol),
    c_ω→−1, reconstructed T*→2, all resolution-stable. For a POC: fixed stretched mesh
    (no AMR), M~10²–10³, ~1% accuracy (not machine precision).
Then Spike 1: port the machinery to solver/boussinesq.py (Hou–Luo geometry), reproduce
the published Chen–Hou 2D-Boussinesq self-similar profile as the validation gate.

ENVIRONMENT & WORKFLOW: .venv/bin/python (numpy + matplotlib). 8 workers is the tested
ceiling (OMP_NUM_THREADS=1 pinned). No pytest; run each suite as `python test_X.py`.
Before ANY logged experimental run, verify the 11 pre-run suites pass and COMMIT (the
dirty-tree guard refuses uncommitted .py; gitignored experiments/*.jsonl + *.out are
fine). NOTE: solver development + unit tests (test_line_hilbert.py etc.) are not
"logged gate runs" — the 11-suite gate is for logged experiments feeding the writeup;
still add each new solver test to the suite set as it lands. Multiprocessing dispatchers
MUST be module-level. One JOURNAL.md entry per experiment. Curated writeup evidence
rebuilds via writeup/curate_evidence.py + build_figures.py. Push to origin only when the
user asks. OPS: never `while pgrep -f script.py` (self-match hang) — wait on the exact
PID; and foreground `sleep` is blocked (use background runs / the Monitor tool).

DISCIPLINE LESSONS BANKED THIS PHASE (do not relearn):
- Ground the scheme in the paper; do NOT trial-and-error a known numerical method.
  Every time we reinvented a piece of dynamic rescaling, it was wrong (3 false starts).
- A stable-looking run can converge to a CONFIDENTLY WRONG number (the periodic-H
  profile). Validate against a known answer before trusting anything.
- The uniform grid is the wrong tool for self-similar blow-up (both the fitness search
  AND the rescaled solver): below-grid structure for the search, CFL-strangled dilation
  for the solver. The stretched non-uniform grid is the enabler; it forces the
  non-FFT (spline-analytic) line Hilbert transform.

HONEST FRAMING TO PRESERVE: 2D Boussinesq is a toy model, not 3D NS. Even a flawless
rescaling solver reproduces a PROVEN result (Chen–Hou 2022, 2D-Boussinesq boundary
blow-up) across "Wall C" (2D Boussinesq ≠ 3D NS) — validates machinery, not novel, not
a proof. Overall Clay odds ~0.05%. The lottery ticket lives on the far side of this
solver, and (per the banked catch) probably in profile construction more than in
GA-over-ICs. Keep saying the honest version out loud.
