# Continuation prompt (copy into a fresh session)

*Written 2026-07-26 at the end of the session that COMPLETED B1 (CHL Scenario 2 reproduced via the
modified rescaling (4.1)/(4.2)) and banked + pushed the full writeup. Everything below is banked +
pushed; origin/main at 2cb751c. The user chose to keep pursuing the lottery ticket (path B). B1 was
green-lit ON THE CONDITION that it help the real direction — it does (it delivered the origin-pinned
gauge the gCLM probe needs). The RECOMMENDED next thing is the **gCLM two-scale↔two-stage transition
probe** — the actual novelty swing. Put the plan (and its honest odds) to the user before a logged run.*

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
  when something does NOT contribute to it, say so and be willing to pivot. (The user explicitly
  gate-checks new bricks against "does this help the real direction with more assertiveness or
  accuracy down the line" — answer that honestly BEFORE building.)
- Produce blog posts + scientific-community-useful writeups WITH ATTACHED DATA (writeup/ +
  committed writeup/data/*.json that rebuilds figures without re-runs). A deliverable.
- Our code was UNIFORM-GRID ONLY — a tier below the field's frontier. Phase 2 closed that gap: the
  stretched-grid dynamic-rescaling solver is built + validated in 1D (Spike 0), 2D (Spike 1), the 1D
  singular-profile machine (P2 anchor), the dynamic-relaxation stepper with the degenerate gauge (P2
  §6), AND now the origin-pinned 3-constant gauge for regular profiles (P2 §8 / B1). The machinery exists.

TERMINOLOGY GUARD (do not drop): the dynamic-rescaling **numerics** upgrade is a solver upgrade to
**Route A**. It is NOT roadmap "Route D" (the later Tier-3 computer-assisted-proof leg, which only
exists after a Tier-2 candidate).

ORIENTATION (read in this order): PROJECT.md, WIN_CONDITION.md, CLAY_ROADMAP.md. Phase 1
(concluded, honest negative): writeup/NEGATIVE_RESULT_TWO_CURRENCIES.md. Spike 0 (COMPLETE):
writeup/TECHNICAL_SPIKE0_RESCALING.md. Spike 1 (COMPLETE — 2D Boussinesq machine, PARTIAL gate):
PHASE2_SPIKE1_NOTES.md + writeup/TECHNICAL_SPIKE1_{VELOCITY,STEPB,STEPC}.md. **P2 — READ THIS:**
PHASE2_P2_NOTES.md (TOP STATUS + §2 anchor, §4 the open work, §5 HH23 scout, §6 dynamic-relaxation,
§7 regular-profile reframe, **§8 B1 = Scenario-2 DONE**). Per-leg writeups + figs:
writeup/TECHNICAL_P2_HL_ANCHOR.md (fig12), TECHNICAL_P2_CONJ24.md (fig13), the §7 reframe (fig14),
**TECHNICAL_P2_SCENARIO2.md + BLOG_P2_SCENARIO2.md (fig15)**. Then experiments/JOURNAL.md (newest
first) and LOGGING.md.

STATE (all banked + pushed; origin/main at commit 2cb751c "P2 B1 writeup"):
- Phase 1 CONCLUDED (honest negative). Spike 0 DONE + VALIDATED. Spike 1 COMPLETE (2D Boussinesq
  dynamic-rescaling machine; reproduces the PROVEN Chen–Hou profile; Step-C PARTIAL 3/4).
- Target paper: Chen–Huang–Li (CHL) **arXiv:2604.01868** (Papers/, gitignored; `Read` page-by-page OR
  `pdftotext Papers/2604.01868v1.pdf out.txt` then grep — far cheaper). CHL's novelty: *degenerate*
  data (ω⁰ₓ(0)=θ⁰ₓₓ(0)=0) → **singular** self-similar profiles via a **two-STAGE** L^∞→L^p blowup;
  only weak existence (their Thm 2.3) is proven, the asymptotic stability (Conjecture 2.4) is
  numerical-only.
- **P2 ANCHOR DONE (§2)** — the 1D HL singular-profile machine reproduces CHL's PROVEN Thm-2.3 steady
  state; we DERIVED the closed-form velocity U̅. solver/hl_rescaled.py::RescaledHL, fig12.
- **P2 §6 DYNAMIC-RELAXATION DONE** — Conjecture 2.4 at POC (LOCAL attractor, PARTIAL 9/9). Built +
  validated CHL's DEGENERATE normalization gauge (their (3.2)): reads the nonlocal H(Ω)(0), pins
  c_l=−U(1) at X=1. solver/hl_rescaled.py::RescaledHLDynamic, fig13.
- **P2 §7 REGULAR-PROFILE REFRAME DONE (scout)** — the §6 "generic → different state" is a REGULAR,
  strictly-positive profile = CHL's Scenario-2 object (qualitatively). fig14.
- **P2 §8 / B1 DONE THIS SESSION — CHL Scenario 2 reproduced. Tier-2, PARTIAL, NOT novel, NOT a proof.**
  * BUILT + VALIDATED the **origin-pinned 3-constant gauge** (CHL's modified (4.1)/(4.2)):
    solver/hl_rescaled.py::RescaledHLScenario2 (spatial-shift DOF c_r, evolve V:=Θ_X, origin-clustered
    grid with X=0 a node) + hand-rolled `_solve_3x3` (no scipy) + `scenario2_ic` (non-symmetric
    positive, origin-NONdegenerate — Ω_X(0)≠0 is required, it's the c_l coefficient).
    test_hl_rescaled.py now **9/9**: the (4.2) solve nulls ∂_τ{Ω(0),Ω_X(0),V(0)} to 4.4e-16
    (known-answer), `_solve_3x3` matches numpy to 7e-14.
  * LOGGED run (predicate LOCKED pre-run, commit b5294ff; n=801, nu=0.02, 2 ICs × 14000 steps,
    ADAPTIVE dt → τ≈42; **5/5 PARTIAL by design**): both ICs → invariant exponent c_l/c_ω =
    −2.533/−2.535 (CHL −2.5114, ~0.9%) as a genuine IC-INDEPENDENT ATTRACTOR to a regular
    strictly-positive profile (minΩ>0, smoothness 0.73 vs ≈1061 for the singular anchor, X*=0.82);
    res falls 15→2.2e-2 (~680×) then FLOORS; absolute triple → (1.59,−0.63,0.21), off CHL raw
    (1.0636,−0.4235,0.0765). Harness experiments/p2_scenario2_relax.py; fig15 rebuilds from committed
    writeup/data/p2_scenario2_relax.json via `python writeup/p2_scenario2_evidence.py`.
  * HONEST READ: the amplitude-INVARIANT ratio (physical exponent) + profile SHAPE are reproduced;
    the ABSOLUTE constants are IC-normalization-dependent (the gauge holds origin values at our IC's
    normalization); the residual floors (fixed grid vs CHL's adaptive mesh). BOTH CHL scenarios now
    reproduced (singular Stage-2 anchor + regular Scenario-2 exponent) — a Tier-2 consolidation, not
    the ticket.

THE NEXT THING — the actual novelty swing (put to the user before a logged run):
- **(NEXT) The gCLM-family two-scale↔two-stage TRANSITION probe.** THE most promising NEW angle, and
  the one B1 just de-risked. The generalized CLM (gCLM) model has a parameter `a` interpolating a
  family of 1D Euler surrogates. Two DIFFERENT blowup mechanisms are known at different members:
    * **two-SCALE** (spatial multi-scale; a bulk + a fine inner scale) is **PROVEN** for CLM by
      Huang–Qin–Wang **[HQW25]** (SIAM J Math Anal 2025);
    * **two-STAGE** (temporal; local L^∞ blowup off-origin, then weak continuation to an L^p blowup at
      the origin) is what CHL found for HL.
  NOBODY has mapped where in `a` the transition between these happens. That is genuinely open and
  1D-tractable. We already have solver/gclm_rescaled.py (test_gclm_rescaled.py 5/5) AND, from B1, the
  validated origin-pinned gauge needed to hold the regular profiles a sweep will encounter.
  FIRST STEPS (scope, don't logged-run yet): (1) obtain/READ [HQW25] if possible — it's the model for
  what "two-scale" looks like numerically and gives a known-answer anchor (Papers/ also holds
  2210.07191, 2305.05660, MMS-Numerics-2025 — grep them). (2) Decide the diagnostic that DISTINGUISHES
  two-scale from two-stage on a rescaled trajectory (e.g. presence/absence of a second inner scale;
  the L^∞-vs-L^p timing) — this is the crux and must be defined BEFORE any logged run. (3) Pick the
  `a`-values to sweep (CLM = the proven two-scale end; HL's `a` = the two-stage end; bisect between).
  (4) THEN lock a predicate and run. Expect this to be harder than B1 (no clean closed-form anchor; may
  need the adaptive-mesh rebuild for the fine inner scale) — surface a short options menu first.
- HONEST CEILING (say it out loud): even a clean two-scale↔two-stage map is novel *toy-model* research,
  not a Clay solve; overall Clay odds remain ~0.05%. But UNLIKE B1 (which reproduced a CHL object),
  this would be NEW math — the genuine lottery ticket. The alternative swing is a rigor step on
  Conjecture 2.4 (harder, less tractable on a laptop). Recommend the gCLM probe.
- KNOWN LIMITATION to respect: our dynamic-relaxation runs FLOOR the residual on a fixed grid (~1e-2),
  and the slow X^{−1/2}-type tail is truncation-limited. A two-scale profile has a FINE inner scale
  that a fixed grid may not resolve — be ready to conclude "needs adaptive mesh" honestly rather than
  overclaim, exactly as B1/§6 did. The adaptive-mesh rebuild is the known heavy-numerics next step if
  the fixed grid can't separate the scales.

ENVIRONMENT & WORKFLOW: .venv/bin/python (numpy + matplotlib; NO scipy — tridiag/solvers/3x3
hand-rolled). 8-worker ceiling (OMP_NUM_THREADS=8 pinned). No pytest; run each suite as
`python test_X.py`. Suites (all green): test_hl_rescaled.py (**9/9**) + test_line_hilbert.py (6/6) +
test_gclm_rescaled.py (5/5) + test_boussinesq_velocity.py (5/5) + test_boussinesq_transport.py (5/5) +
test_boussinesq_rescaled.py (8/8). Before ANY logged experimental run: pass the test gate + COMMIT +
LOCK the predicate in git (dirty-tree guard; gitignored experiments/*.log,*.npz,*.jsonl,*.out are
fine). Solver dev + unit tests are NOT "logged gate runs"; still add each new solver test to the
suite. Papers/ gitignored. One JOURNAL.md entry per LOGGED experiment (scouts may get a
clearly-labelled entry too). Evidence rebuilds: writeup/p2_scenario2_evidence.py (fig15),
p2_conj24_evidence.py (fig13), p2_regular_profile_evidence.py (fig14), p2_hl_anchor_evidence.py (fig12)
(+ spike scripts). Push only when asked.
OPS: never `while pgrep -f script.py` (self-match hang); foreground `sleep` is blocked (use background
runs / the Monitor until-loop). The dynamic-relaxation runs are SLOW (dense-Hilbert matvecs,
Python-overhead-bound: ~10 steps/s at n=1601, ~35 steps/s at n=801). USE ADAPTIVE dt (recompute the
CFL every ~200 steps as the initial transient decays — this was the key to reaching large τ in B1;
a fixed dt is throttled by the c_l≈13 startup transient). Run python `-u` to a LOGFILE and wait on a
`grep`/Monitor until-loop — do NOT pipe through `tail`. For a long run the user may want a CLI progress
bar: emit throttled `PROGRESS [bar] pct k/N ... ETA` lines and Monitor them. Reuse the solver instance
(the dense Hmat is cached lazily) — don't rebuild per config.

DISCIPLINE LESSONS BANKED (do not relearn):
- Ground the scheme in the paper; do NOT trial-and-error a known method. Un-fetchable → `pdftotext`
  the Papers/ PDFs + grep, or `Read` page-by-page. Validate against a known answer; DERIVE the exact
  answer where one exists and test against it (the anchor U̅; the (4.2) gauge nulling ∂_τ to 1e-15).
- Dynamic-rescaling normalization is a GAUGE, and it is amplitude/normalization-DEPENDENT. Report only
  the GAUGE-INVARIANTS as results: the ratio c_l/c_ω (the physical self-similar exponent) and the
  profile SHAPE. NEVER report a normalization-dependent absolute constant as a "match" — B1's absolute
  triple was off CHL's raw by design; the ratio was the real result.
- For DEGENERATE (origin-symmetric) data use the §6 gauge (nonlocal H(Ω)(0), pin at X=1); for REGULAR
  NON-SYMMETRIC profiles use the §8 origin-pinned 3-constant gauge (needs Ω_X(0)≠0). Pick the gauge to
  match the profile's symmetry — a mismatch cannot HOLD the profile (§7 measured this).
- Singular/multi-scale profiles: the naive scheme rings at discontinuities and the slow tail is
  truncation-limited; a fixed grid FLOORS the residual. Diagnose the floor (measure it), label any
  dissipation crutch as POC, and CONCLUDE "needs adaptive mesh" honestly rather than overclaim.
- LOCK the predicate in git BEFORE the logged run; write it to MATCH scratch-observed behaviour and
  declare PARTIAL by construction; report PARTIAL and locate the cause; do NOT re-run to chase a clause
  into a pass. (B1: 5/5 held because the predicate was matched to a pre-run scratch that reached τ≈71.)
- Do an exploratory SCRATCH run to find the landing point BEFORE writing the predicate — never lock a
  predicate blind.

HONEST FRAMING TO PRESERVE: 1D HL is a toy model (models the BOUNDARY behaviour of the Hou–Luo /
3D-axisymmetric-Euler scenario; 2D Boussinesq is closer but still a toy, not 3D NS). P2's anchor
reproduced a PROVEN result; the §6 leg reproduced the LOCAL content of a NUMERICAL-only conjecture;
B1/§8 reproduced CHL's Scenario-2 exponent as a genuine attractor (all Tier-2, PARTIAL, none novel,
none a proof). Both CHL scenarios are now reproduced — a clean consolidation, NOT the ticket. The
lottery ticket lives in genuinely-NEW math: the gCLM two-scale↔two-stage transition (uses
solver/gclm_rescaled.py + the B1 origin-pinned gauge) or a rigor step on Conjecture 2.4. Overall Clay
odds ~0.05%. Keep pursuing the Clay end goal; keep saying the honest version out loud.
