# Continuation prompt (copy into a fresh session)

*Written 2026-07-25 at the end of the session that COMPLETED the P2 dynamic-relaxation leg
(Conjecture 2.4 at POC, PARTIAL 9/9) after an HH23 go/no-go scout. Everything below is banked +
pushed; origin/main at 659fa86.*

Continue the Navier–Stokes blow-up search project in this directory
(/home/andy/projects/Unsolved). The end goal is the Clay Millennium problem — a genuine, honest
attempt via singular-profile / self-similar-blowup research — while never fooling ourselves with a
numerical artifact. WIN_CONDITION.md is the anti-self-deception contract: only Tier 3 (rigorous
proof) solves it; Tier 1 (candidate) and Tier 2 (resolution-confirmed) are progress. Preserve that
honesty — do not oversell. Raise genuine scope decisions for review with a short options menu
rather than deciding unilaterally.

USER'S STANDING STEER (honor it):
- Keep pursuing the Clay end goal. The realistic prize is novel toy-model singularity research +
  a tiny (~0.05%) Clay "lottery ticket," NOT a Clay solve. Keep the lottery ticket the true focus;
  when something does NOT contribute to it, say so and be willing to pivot.
- Produce blog posts + scientific-community-useful writeups WITH ATTACHED DATA (writeup/ +
  committed writeup/data/*.json that rebuilds figures without re-runs). A deliverable.
- Our code was UNIFORM-GRID ONLY — a tier below the field's frontier. Phase 2 closed that gap:
  the stretched-grid dynamic-rescaling solver is built + validated in 1D (Spike 0), 2D (Spike 1),
  the 1D singular-profile machine (P2 anchor), AND now the dynamic-relaxation stepper with the
  degenerate normalization gauge (P2 novelty leg). The machinery exists.

TERMINOLOGY GUARD (do not drop): the dynamic-rescaling **numerics** upgrade is a solver upgrade to
**Route A**. It is NOT roadmap "Route D" (the later Tier-3 computer-assisted-proof leg, which only
exists after a Tier-2 candidate).

ORIENTATION (read in this order): PROJECT.md, WIN_CONDITION.md, CLAY_ROADMAP.md. Phase 1
(concluded, honest negative): writeup/NEGATIVE_RESULT_TWO_CURRENCIES.md. Spike 0 (COMPLETE):
writeup/TECHNICAL_SPIKE0_RESCALING.md. Spike 1 (COMPLETE — 2D Boussinesq machine, PARTIAL gate):
PHASE2_SPIKE1_NOTES.md + writeup/TECHNICAL_SPIKE1_{VELOCITY,STEPB,STEPC}.md. **P2 — READ THIS:**
PHASE2_P2_NOTES.md (TOP STATUS + §2 anchor, §5 HH23 scout, §6 dynamic-relaxation leg),
writeup/TECHNICAL_P2_HL_ANCHOR.md + BLOG_P2_HL_ANCHOR.md (fig12), and
writeup/TECHNICAL_P2_CONJ24.md + BLOG_P2_CONJ24.md (fig13). Then experiments/JOURNAL.md (newest
first) and LOGGING.md.

STATE (all banked + pushed; origin/main at commit 659fa86 "P2 dynamic-relaxation leg"):
- Phase 1 CONCLUDED (honest negative: uniform grid can't resolve self-similar blow-up). Spike 0
  DONE + VALIDATED (1D CLM dynamic rescaling). Spike 1 COMPLETE (2D Boussinesq dynamic-rescaling
  machine; reproduces the PROVEN Chen–Hou profile; Step-C gate PARTIAL 3/4 — validated machinery,
  NOT novel, NOT a proof).
- **P2 ANCHOR DONE — the 1D Hou–Luo (HL) singular-profile machine.** Target: Chen–Huang–Li (CHL)
  **arXiv:2604.01868** (Papers/, gitignored — the PDF is `Read`-able page-by-page AND text-
  extractable with `pdftotext Papers/2604.01868v1.pdf out.txt` then grep, which is far cheaper).
  CHL's novelty: *degenerate* data (ω⁰ₓ(0)=θ⁰ₓₓ(0)=0) → **singular** self-similar profiles via a
  **two-STAGE** L^∞→L^p blow-up. Only weak existence of the explicit profile is proven (their
  Thm 2.3); the asymptotic STABILITY (Conjecture 2.4) is numerical-only — that gap is the frontier.
  Anchor: exact steady state Ω̄=(X−1)^{−1/2}1_{X>1}, Θ̄=(π/2)1_{X>1}, c̄_l=2, c̄_ω=−1; we DERIVED the
  closed-form velocity U̅=2√(1−X)−2 (X<1), −2 (X≥1). solver/hl_rescaled.py, fig12.
- **P2 HH23 SCOUT DONE (this session) — NO-GO on the literal link, banked in PHASE2_P2_NOTES.md §5.**
  [HH23] = Hou–Huang, MMS 21(1):218–268, 2023 — a numerical two-**SCALE** 3D-axisymmetric-Euler
  blow-up on ℝ³ with NO boundary. CHL only note a *qualitative* profile similarity ("an intriguing
  question"). Three walls make a 1D-HL machine unable to address it without overclaiming: mechanism
  mismatch (HH23 two-SCALE vs HL two-STAGE — CHL explicitly found NO two-scale in HL), geometry
  mismatch (HL models the *boundary* behaviour; HH23 is boundary-free ℝ³), and it's a 3D structural
  question. BUT the scout surfaced the real 1D-tractable target: **two-scale vs two-stage inside the
  CLM/HL family** — two-scale is PROVEN for CLM (Huang–Qin–Wang [HQW25], SIAM J Math Anal 2025),
  CONJECTURED by Liu for HL, but CHL found HL is two-STAGE. That live discrepancy is genuinely open.
- **P2 DYNAMIC-RELAXATION LEG DONE (this session) — Conjecture 2.4 at POC, PARTIAL/Tier-2. §6.**
  Full record: writeup/TECHNICAL_P2_CONJ24.md + BLOG_P2_CONJ24.md; fig13 from committed
  writeup/data/p2_conj24_relax.json (`python writeup/p2_conj24_evidence.py`). Logged harness
  (predicate LOCKED in git BEFORE the run, commit e4521d9): experiments/p2_conj24_relax.py --logged.
  - THE NOVEL PIECE — CHL's degenerate normalization gauge (their (3.2)) — BUILT + VALIDATED. The
    CHH22 gauge pins Omega_x(0)=0 for degenerate data (dead); CHL read the NONLOCAL U_X(0)=H(Ω)(0)
    (alive) for amplitude + c_l=−U(1) for location. Known-answer test on the exact anchor →
    (c_l,c_ω)=(1.949,−0.969)≈(2,−1). Clean identity: at the anchor Θ_X−(U+c_l X)Ω_X = Ω̄ and
    H(Ω̄)(0)=−1 exactly (the X=1 delta cancels analytically). solver/hl_rescaled.py::RescaledHLDynamic;
    test_hl_rescaled.py now **7/7** (two new gauge tests). All other suites unchanged.
  - THE WALL (diagnosed): the naive SSPRK3+upwind+spline scheme is UNSTABLE at the singular profile —
    starting AT the regularized anchor the residual grows 25→1e9 by τ~1.4 (spline slopes ring at the
    X=1 discontinuity; the stiff Θ_X delta-source amplifies). Fix = subgrid dissipation nu*d²/ds²
    (a POC crutch with O(nu) profile bias, NOT CHL's WENO/adaptive mesh). Added as solver `nu` param.
  - LOGGED RESULT (n=801, nu=0.02, 2500 steps; **9/9 pre-committed clauses PASS, PARTIAL by design**):
    anchor HOLD → (1.939,−0.927), res 180→3.4 plateau (stable HOLD, NOT →0), shape 4.9%; two
    perturbations → the SAME fixed point (LOCAL asymptotic stability); nu=0.04 → unchanged (robust);
    generic far degenerate IC → (0.680,−0.487), a DIFFERENT self-similar state (the honest predicted
    NEGATIVE — global basin beyond a fixed-grid POC; note it CONVERGES ELSEWHERE, doesn't blow up).
  - HONEST STATUS: validated the degenerate gauge + the LOCAL stability of CHL's singular fixed
    point (independently reproduces the LOCAL content of a numerical-only claim). NOT achieved:
    residual→0 (POC dissipation floor) and the global basin. Tier-2-style, NOT novel, NOT a proof.

THE OPEN FORK — put this menu to the user before doing heavy work (genuine scope decision; the user
last session leaned toward writing this prompt and reassessing fresh, without pre-committing):
- (A) **BANK & PIVOT.** Treat P2 as a complete Tier-2 data-backed deliverable and pivot to a new
  angle (a different degeneracy family, a fresh toy model, or a roadmap reassessment).
- (B) **INVEST IN HEAVY NUMERICS (the real lottery ticket).** Build the global-basin solver CHL used:
  WENO/limited advection (kill the ringing without the dissipation bias), adaptive mesh, a
  vanishing-viscosity (nu→0) limit, and a semi-analytic X^{−1/2} outer-tail patch (the same tail fix
  flagged for Spike-1 Step C). THEN run the genuinely-new **two-scale-vs-two-stage probe** (track the
  peak LOCATION: a moving bulk on a coarse scale = two-scale/Liu; τ→∞ convergence to the fixed
  profile at X=1 = two-stage/CHL). Multi-session, real risk it stays PARTIAL, but this is where new
  1D math lives. Read [HQW25] (Huang–Qin–Wang, CLM two-scale) first if obtainable; it's the model.
- (C) **POLISH THE POC (bounded, de-risks B).** A resolution×vanishing-nu study to show the residual
  floor shrinks toward zero (strengthens the local-stability claim to near-quantitative) + tighten
  the writeup, WITHOUT the full WENO/adaptive rebuild. Still Tier-2, not novel.
- NOTE the honest ceiling: even a clean GLOBAL stability confirmation REPRODUCES CHL's numerical
  claim — Tier-2. The genuinely NEW math (two-scale in HL vindicating Liu, a not-yet-seen profile, a
  rigor step) is harder and longer odds. Say which one any given run is going after, out loud.

ENVIRONMENT & WORKFLOW: .venv/bin/python (numpy + matplotlib; NO scipy — tridiag/solvers
hand-rolled). 8-worker ceiling (OMP_NUM_THREADS pinned). No pytest; run each suite as
`python test_X.py`. Suites (all green): test_hl_rescaled.py (7/7) + test_line_hilbert.py (6/6) +
test_gclm_rescaled.py (5/5) + test_boussinesq_velocity.py (5/5) + test_boussinesq_transport.py
(5/5) + test_boussinesq_rescaled.py (8/8). Before ANY logged experimental run: pass the test gate +
COMMIT + LOCK the predicate in git (dirty-tree guard; gitignored experiments/*.log,*.npz,*.jsonl,
*.out are fine). Solver dev + unit tests are NOT "logged gate runs"; still add each new solver test
to the suite. Papers/ gitignored. One JOURNAL.md entry per LOGGED experiment. Evidence rebuilds via
writeup/p2_conj24_evidence.py + writeup/p2_hl_anchor_evidence.py (+ the spike scripts). Push only
when the user asks.
OPS: never `while pgrep -f script.py` (self-match hang); foreground `sleep` is blocked (use
background runs / the Monitor until-loop). The dynamic-relaxation runs are SLOW (dense-Hilbert
matvecs, Python-overhead-bound: ~2500 steps at n=801 ≈ a few min; the full 5-config logged run
≈ 8–12 min). Run python `-u` to a LOGFILE and wait on a `grep`/Monitor until-loop — do NOT pipe
through `tail` (it buffers and the output is lost if the run is killed). Reuse RescaledHL/Dynamic
(the dense Hmat is cached lazily) — don't rebuild per config. n=2001 Hmat build ~3s, n=4001 ~20s.

DISCIPLINE LESSONS BANKED (do not relearn):
- Ground the scheme in the paper; do NOT trial-and-error a known method. Un-fetchable → `pdftotext`
  the Papers/ PDFs + grep (cheap), or `Read` page-by-page. Validate against a known answer.
- Derive the exact answer where one exists (the closed-form U̅; the anchor gauge identity c_ω=H(Ω̄)(0)
  =−1) and test against it — that is what makes a "known-answer" validation real.
- Dynamic-rescaling normalization is a GAUGE. For DEGENERATE data the origin-slope gauge is itself
  degenerate (=0) — CHL's fix reads the NONLOCAL H(Ω)(0) instead. Never report a gauge INPUT as a
  result; the gauge-invariant (c_l,c_ω) + shape are the real tests.
- Singular profiles: the singular CORE is fine; the naive scheme is UNSTABLE AT the profile (rings
  at the discontinuity) and the SLOW TAIL is truncation-limited. Diagnose the instability (measure
  the growth), don't hand-wave; a POC dissipation crutch is honest ONLY if labelled as such.
- LOCK the predicate in git BEFORE the logged run; report PARTIAL and locate the cause; do NOT
  re-run to chase a clause into a pass. (This session: 9/9 held because the predicate was written to
  MATCH the scratch-observed behaviour, declared PARTIAL by construction — not tuned after the run.)
- Performance: profile before optimizing; preserve accuracy digit-for-digit across any speedup and
  re-run the full affected gate to prove it.

HONEST FRAMING TO PRESERVE: 1D HL is a toy model (it models the BOUNDARY behaviour of the Hou–Luo /
3D-axisymmetric-Euler scenario; 2D Boussinesq is closer but still a toy, not 3D NS). P2's anchor
reproduced a PROVEN (weak-existence) result; P2's dynamic-relaxation leg reproduced the LOCAL
content of a NUMERICAL-only conjecture (Tier-2, PARTIAL). Neither is novel; neither is a proof.
Overall Clay odds ~0.05%. The lottery ticket lives on the far side of the global-basin numerics (the
two-scale-vs-two-stage question), and probably in direct profile/stability construction more than
GA-over-ICs. Keep pursuing the Clay end goal; keep saying the honest version out loud.
