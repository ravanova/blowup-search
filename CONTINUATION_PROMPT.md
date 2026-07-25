# Continuation prompt (copy into a fresh session)

*Written 2026-07-25 at the end of the session that BANKED the P2 regular-profile reframe (the
"generic" state is CHL's regular Stage-1 profile, NOT an artifact) and SCOPED the fork toward B1.
Everything below is banked + pushed; origin/main at 7ff371e. The user chose to keep pursuing the
lottery ticket (path B), banked this finding (B3), and asked to scope B1-vs-B2 — done. The
RECOMMENDED next brick is **B1** (implement CHL's modified Scenario-2 formulation (4.1)/(4.2);
cheap, clean known-answer). Put B1 to the user (with the honest ceiling) before building.*

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
PHASE2_P2_NOTES.md (TOP STATUS + §2 anchor, §5 HH23 scout, §6 dynamic-relaxation leg, **§7 the
regular-profile reframe + B1/B2 scout — read this**), writeup/TECHNICAL_P2_HL_ANCHOR.md +
BLOG_P2_HL_ANCHOR.md (fig12), writeup/TECHNICAL_P2_CONJ24.md (§7 addendum) + BLOG_P2_CONJ24.md
(postscript) (fig13, fig14). Then experiments/JOURNAL.md (newest first) and LOGGING.md.

STATE (all banked + pushed; origin/main at commit 7ff371e "P2 regular-profile reframe (scout)"):
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
- **P2 REGULAR-PROFILE REFRAME + B1/B2 SCOUT DONE (this session) — §7. EXPLORATORY (non-logged), no
  new solver code.** Evidence: writeup/p2_regular_profile_evidence.py → fig14 from committed
  writeup/data/p2_regular_profile.json (+ _traj.json). CHL's rescaled HL system has TWO fixed points;
  our degenerate-gauge machinery reaches both. The §6 logged run's "generic → (0.680,−0.487),
  DIFFERENT state, honest NEGATIVE" is NOT a POC artifact — that final field is a REGULAR,
  strictly-positive profile (smooth: max|Ω_X|/peak≈0.3 vs ≈1061 for the singular anchor; peaked at
  X≈0.35 away from X=1), = CHL's Stage-1 / Scenario-2 object (their §4) QUALITATIVELY. So we reach
  the FIRST HALF of CHL's two-stage structure independently. GUARDS: qualitative match only (standard
  (2.4)+degenerate gauge, NOT CHL's modified (4.1)); constants differ under different normalization
  (ours c_l≈0.5,c_ω≈−0.45; theirs (c_l,c_ω,c_r)=(1.0636,−0.4235,0.0765), ratio −2.5114); NOT novel,
  NOT a proof. B1/B2 SCOUT (8000-step generic trajectory, fig14 C): under our gauge the trajectory
  TRANSITS the CHL-S2 neighborhood (c_l≈1.06 near step 1200 — nearly the published value) but CANNOT
  hold it → wanders in the low-c_l regular regime (res floor ~0.12) and NEVER approaches c_l=2.
  Diagnosis: our gauge pins c_l=−U(1) (stagnation at X=1), a mismatch for a profile peaked at X≈0.35;
  CHL's (4.2) pins at the ORIGIN. ⇒ B1 is cheap + well-motivated; B2's transition is unreachable on a
  fixed grid.

THE DECIDED PATH — pursuing the lottery ticket (path B). B3 (bank the reframe) DONE this session.
Put the B1 recommendation to the user (with the honest ceiling) before building:
- (B1) **RECOMMENDED NEXT BRICK — implement CHL's modified Scenario-2 formulation (4.1)/(4.2) and pin
  the regular profile.** SMALL delta on solver/hl_rescaled.py::RescaledHLDynamic, fully grounded in
  CHL §2.5+§4 (already pdftotext-extracted; re-extract: `pdftotext Papers/2604.01868v1.pdf out.txt`,
  grep "(4.1)","(4.2)","Scenario 2"). SPEC:
    * Formulation (4.1): our (2.4) transport (U+c_l X) → **(U+c_l X+c_r)** (one extra constant c_r);
      use V:=Θ_X (better far-field decay): Ω_τ+(U+c_l X+c_r)Ω_X=c_ω Ω+V; V_τ+(U+c_l X+c_r)V_X=
      (2c_ω−U_X)V; U_X=H(Ω), U(0)=0.
    * Normalization (4.2): enforce ∂_τΩ(0)=∂_τΩ_X(0)=∂_τV(0)=0 → a 3×3 LINEAR solve each step for
      (c_l,c_ω,c_r): [Ω_X(0)c_r−Ω(0)c_ω=V(0)]; [V_X(0)c_r−2V(0)c_ω=−U_X(0)V(0)];
      [Ω_XX(0)c_r−Ω_X(0)c_ω+Ω_X(0)c_l=V_X(0)−U_X(0)Ω_X(0)]. (Hand-roll the 3×3; NO scipy.)
    * KNOWN-ANSWER target (their Fig 4.2): (c_l,c_ω,c_r,c_l/c_ω)=(1.0636,−0.4235,0.0765,−2.5114). We
      already fly within ~0.005 of c_l=1.0636 at the transit, so pinning there is very plausible.
    * SUCCESS = converge to a regular strictly-positive profile at those constants + a SHAPE OVERLAY
      confirming our generic-run profile IS this one (CHL Fig 4.3 shows Scenario-1-inner = Scenario-2).
    * Add a new solver class/method + unit tests to test_hl_rescaled.py; then a LOGGED run (lock the
      predicate first). Outcome = "both CHL scenarios reproduced" — clean Tier-2 consolidation.
- (B2) **NOT the right brick now — the Stage-1→Stage-2 transition / two-scale-vs-two-stage probe.**
  The scout showed it is UNREACHABLE on a fixed grid (the generic trajectory heads AWAY from c_l=2);
  it needs the adaptive-mesh rebuild AND even a clean result mostly RE-CONFIRMS CHL's published
  two-stage finding (low novel upside). Defer until after B1.
- HONEST CEILING (say it out loud): B1 REPRODUCES a CHL object → Tier-2, NOT the lottery ticket. The
  genuinely-new math lives elsewhere and is longer odds: (i) the **gCLM-family two-scale↔two-stage
  transition** — where in the parameter 'a' does CLM's PROVEN two-scale (HQW25) give way to HL's
  two-stage (CHL)? Nobody has mapped it; we already have solver/gclm_rescaled.py — this is the most
  promising NEW angle; or (ii) a rigor step on Conjecture 2.4. B1 is the grounded brick that de-risks
  both. Read [HQW25] (Huang–Qin–Wang, CLM two-scale, SIAM J Math Anal 2025) first if obtainable —
  it's the model for the gCLM probe. (Papers/ also holds 2210.07191, 2305.05660, MMS-Numerics-2025.)

ENVIRONMENT & WORKFLOW: .venv/bin/python (numpy + matplotlib; NO scipy — tridiag/solvers
hand-rolled). 8-worker ceiling (OMP_NUM_THREADS pinned). No pytest; run each suite as
`python test_X.py`. Suites (all green): test_hl_rescaled.py (7/7) + test_line_hilbert.py (6/6) +
test_gclm_rescaled.py (5/5) + test_boussinesq_velocity.py (5/5) + test_boussinesq_transport.py
(5/5) + test_boussinesq_rescaled.py (8/8). Before ANY logged experimental run: pass the test gate +
COMMIT + LOCK the predicate in git (dirty-tree guard; gitignored experiments/*.log,*.npz,*.jsonl,
*.out are fine). Solver dev + unit tests are NOT "logged gate runs"; still add each new solver test
to the suite. Papers/ gitignored. One JOURNAL.md entry per LOGGED experiment (scouts may get a
clearly-labelled entry too). Evidence rebuilds via writeup/p2_conj24_evidence.py +
writeup/p2_regular_profile_evidence.py (fig14; --generate re-runs fields, --generate-traj re-runs the
8000-step trajectory) + writeup/p2_hl_anchor_evidence.py (+ the spike scripts). Push only when asked
(the user asked this session).
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
content of a NUMERICAL-only conjecture (Tier-2, PARTIAL); the regular-profile reframe reproduced
CHL's Stage-1 object QUALITATIVELY (Tier-2, not even a proven identity yet — B1 would tighten it).
None is novel; none is a proof. Overall Clay odds ~0.05%. The lottery ticket does NOT live in
reproducing more of CHL (B1/B2 are both Tier-2) — it lives in genuinely-new math: most promisingly
the gCLM-family two-scale↔two-stage transition (uses solver/gclm_rescaled.py), or a rigor step. B1
is the grounded consolidation brick, not the ticket — say so out loud. Keep pursuing the Clay end
goal; keep saying the honest version out loud.
