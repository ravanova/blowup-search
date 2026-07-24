# Experiment Journal

Hand-written context per experiment (see LOGGING.md — the structured logs
answer "what happened"; this records *why* and what a human noticed).

## Spike 0 — the crux is BUILT: line Hilbert transform on a stretched grid PASSES against the known answer — 2026-07-24

Full record: PHASE2_SPIKE0_NOTES.md ("BUILT" section). Code: `solver/line_hilbert.py`,
`test_line_hilbert.py` (run `python test_line_hilbert.py`; 6/6 pass). NOT a logged gate
run — solver development against a closed-form known answer.

The hardest, most-de-risking component of Spike 0 now works. The whole-line Hilbert
transform on a non-uniform sinh-stretched grid maps `−4X/(1+4X²) → 2/(1+4X²)` (the exact
CLM self-similar pair) to **relative error 1.6e-4**, POC target was 1%, with clean
monotone convergence (2.35e-3 → 5.22e-4 → 1.16e-4) under whole-line refinement.

What a human would want to know:

- **This was THE crux** (per the recon notes and the standing steer): the stretched grid
  forces a NON-FFT Hilbert transform, and that spline-analytic transform was the one piece
  the periodic solver couldn't provide. It's now validated in isolation with a hard
  pass/fail against an answer we know exactly. The rest of Spike 0 (the time-stepper) is
  comparatively standard.

- **I derived the A,B basis-Hilbert formulas instead of transcribing the paper's minimax.**
  The recipe warned pdftotext mangles Appendix C's 23-term coefficient lists. Rather than
  hand-copy them, I substituted the Taylor split `ln|1−s| = L(s) − s − s²/2 − s³/3`
  (`L = −Σ_{n≥4}sⁿ/n`) into the exact closed forms; the cancellation cancels *analytically*.
  This reproduced the paper's minimax structure (exactly for B; the OCR's orphaned leading
  `−` confirmed the A sign) and is verified by branch-continuity at |s|=0.5 and against the
  raw closed form. **The minimax transcription the recipe flagged as risky is unneeded.**

- **Honest scope:** this validates machinery against a *proven* toy result, not novelty.
  The dominant error is ~1/M tail truncation (the profile's 1/X decay), expected and fine
  at POC level. No scipy in the venv, so the natural cubic spline slopes are hand-rolled
  (Thomas). `line_hilbert_matrix(x)` gives a reusable dense operator for the time-stepper.

- **Next increment:** `solver/gclm_rescaled.py` — the stretched-grid time-stepper (evolve
  f=Ω/X, k=1; c_ω=1−HΩ(0), c_l=1) + `test_gclm_rescaled.py` (steady residual at Ω̄₀, then
  convergence from perturbed odd data → c_ω→−1, T*→2, resolution-stable). The log-kernel
  velocity U (C.1 C,D elements) is a≠0-only, so deferrable for the CLM POC.

## Spike 0 reconnaissance (dynamic rescaling on 1D gCLM) — 2026-07-24 — scheme grounded on exact known answer; uniform-grid CFL dead-end; Appendix C recipe in hand; solver NOT yet built

Full record: PHASE2_SPIKE0_NOTES.md. Scratch code: phase2_spike0_probe.py (periodic,
kept as a negative example). Commits d39a504, 3242158, 9ed940f. This is NOT a logged
gate run — it is solver-development reconnaissance (cheap probes before the real build),
in the project's "learn before you build" spirit.

Goal: implement dynamic (self-similar) rescaling on the 1D gCLM solver and validate it
recovers a *known* self-similar blow-up before porting to 2D Boussinesq (Spike 1).

What a human would want to know:

- **The known-answer target is CLM (a=0):** data w0=−sin x → blow-up at x=0, T*=2,
  exact self-similar profile Ω̄₀(X)=−4X/(1+4X²), H(Ω̄₀)=2/(1+4X²), c_ω→−1. I first
  derived the rescaled equation + this profile by hand; later confirmed *identical* to
  Huang–Tong–Wang arXiv:2603.25104 (the exact gCLM dynamic-rescaling paper).

- **Three false starts, each a finding** (probes v1→v4, phase2_spike0_probe.py):
  (1) pointwise high-derivative normalization (pin Ω_yyy(0)) is a NOISE amplifier —
  the (ik)³ multiplier makes Ω_yyy(0) read ~1000 vs the analytic 1; use integral
  modulation. (2) A periodic pseudo-spectral run is *stable but converges to the WRONG
  profile* (fitted B≈−1, not the CLM value 4) — because the true profile is a whole-line
  ~1/X function needing the LINE Hilbert transform, and periodic H ≠ line H for slow
  tails. My earlier "periodicity is fine" read was an artifact of the wrong (periodic) H.
  (3) On a large *uniform* whole-line grid the line-H works (~1/M truncation err) but the
  −c_l X Ω_X dilation NaNs — diagnosed as a **CFL limit** (advection speed is X up to M,
  so dt < dX/M ≈ 1e-4; a spectral filter did not help). Uniform grid = wrong tool.

- **Grounding closed all gaps (the session's repeated lesson: read the paper, don't
  trial-and-error).** arXiv:2603.25104 gives: rescaled eqn Ω_τ=(c_ω+HΩ)Ω−c_l X Ω_X;
  a=0 normalization c_l=1, c_ω=1−HΩ(0) (value-based, robust). Appendix C gives the
  discretization: **C.1** line Hilbert transform via C¹₀ cubic-spline basis with analytic
  H(P_i),H(Q_i) (closed-form A,B,C,D + minimax series) — works on a NON-uniform grid where
  FFT cannot; **stretched cosh/sinh grid** X(ρ) with dX~X·Δρ so the dilation CFL ~ Δρ is
  independent of M (this cures the uniform-grid death); **C.2** WENO5 advection +
  SSPRK(10,4), evolve f=Ω/Xᵏ, converge ‖f_τ‖<1e-8. Full recipe banked in the notes.

- **Honest status:** Spike 0 is de-risked and fully specified but the solver is NOT built.
  Next increment: solver/line_hilbert.py + test vs the −4X/(1+4X²)↔2/(1+4X²) pair
  (the crux, self-contained, hard pass/fail). Confirmed a genuine multi-day build.

## Phase 2 route decision — 2026-07-24 — Phase 1 fitness search concluded; numerics upgrade (dynamic rescaling) chosen over AMR; NOT roadmap "Route D"

Full record: PHASE2_NUMERICS_PLAN.md. Commit e7e0e3b. Decision made WITH the user via a
reviewed options menu (per the standing "raise genuine scope decisions" steer).

Context: the uniform-grid fitness search concluded with a decisive negative (two
currencies — ν_crit, g_frac — both fail the honest gate via the same free-split ω₀→0
wall; root cause: on a uniform grid the singular structure forms below grid scale).
Standalone packaging of that negative: writeup/NEGATIVE_RESULT_TWO_CURRENCIES.md
(commit 9cd2b21) — the Option-C deliverable this session.

What a human would want to know:

- **The forward move is a numerics upgrade, not another fitness.** Researched the field
  (Chen–Hou; Wang–Lai–Gómez-Serrano–Buckmaster; the 2025–26 unstable-profile frontier).
  Three paradigms: (P1) dynamic self-similar rescaling — time-integrate in a rescaled frame
  so the blow-up is a steady profile on a fixed grid; (P2) direct profile construction
  (Newton/PINN) — the current novelty frontier; (P3) AMR. **Chose P1**, reject P3: P1
  reuses the validated solver, dissolves the below-grid-scale wall (fitness on RESOLVED
  structure), and its late-time state IS a self-similar profile (the on-ramp to P2).

- **Terminology guard banked:** the AMR / self-similar-rescaling upgrade is a Route-A
  *numerics* upgrade, NOT roadmap "Route D" (the later Tier-3 computer-assisted-proof leg).
  Fixed this mislabel in writeup SUMMARY.md + README.md.

- **Honest catch surfaced (matters for the lottery ticket):** the literature's real novelty
  frontier is P2 profile construction of UNSTABLE profiles, not evolve-ICs search. P1 mainly
  finds the *stable* CLM/Boussinesq blow-up (which Chen–Hou already proved). So P1 is framed
  as the shared substrate + on-ramp; A-vs-B (evolve-ICs vs profile-hunting) is a gate to
  re-decide AFTER Spike 1, with a working rescaling solver in hand. User approved: do Option-C
  writeup first (done), then build Spike 0.

## Reformulated Gate 4 (g_frac) — 2026-07-24 — FAIL 4/6: free-split rails to ω₀→0, split-dominated + t_res proxy

Full results: PHASE1_GATE4_REFORM_RESULTS.md. Frozen predicate:
PHASE1_GATE4_REFORMULATED_PREDICATE.md. Scripts: phase1_gate4_reform.py +
analyze_phase1_gate4_reform.py (commit 13d888f, pre-run). Data:
experiments/phase1_gate4_reform.jsonl → writeup/data/phase1_gate4_reform.json.
The user reviewed + signed off the frozen predicate (3 improvements folded in:
rank-stability across 128→256→512, split-dominance promoted to gate condition 6g,
t_res-proxy check 6h; plus winner-not-at-split-rail 6b′ from designing the
adversarial roster). 138 solves (40 shapes × {128,256,512} + 18-shape split-sweep).

What a human would want to know:

- **The gate did its job and returned a decisive negative.** g_frac passes 1,2,3,5
  (discriminating, direction-correct, well-posed/window-robust +0.989, wide band)
  and its RANK is resolution-stable (+0.889, +0.926 — the de-risk result holds).
  But property 6 fails hard on FREE split.

- **The ω₀ cheat returns exactly as it killed ν_crit.** The de-risk fixed split=0.5
  (pinning ω₀). Free split lets the optimum drive ω→0 for max buoyancy forcing: the
  TOP-5 shapes at N=512 are all split 0.93–0.99, winner rand_18 split=0.99
  centroid=1.56. ρ(g,log|ω₀|)=−0.66. The controlled split-sweep STILL showed
  interior optima (property 6f passed) — but the free-roster WINNER rails anyway,
  because at free structure a high-split shape beats the interior-optimum structured
  ones. The sweep couldn't see it; the winner interrogation did. (Banked lesson
  reasserted: a controlled sub-test passing ≠ the winner being honest.)

- **6g confirmed the split-dominance finding as a gate condition:** partial
  ρ(g,centroid|split)=+0.11 < 0.15 — once split is controlled, g_frac barely ranks
  ω-geometry. And 6h: partial ρ(g,centroid|t_res)=−0.39 — g_frac is largely a
  formation-time proxy. Binning on split alone would NOT rescue it (it's also a
  t_res proxy).

- **Property 4's second axis (new here) also failed:** grower/non-grower
  CLASSIFICATION is not resolution-stable — 7/37 shapes are coarse-grid
  false-growers (t_res climbs to 4.0 as N grows; e.g. advlo_s20 2.91→3.56→4.00),
  textbook under-resolution false-positives. Rank-stable ≠ classification-stable.

- **Strategic read (the user's Clay-lottery focus):** TWO currencies now hit the
  same uniform-grid wall (ω₀→0 degeneracy); g_frac adds a t_res-proxy problem. A
  THIRD uniform-grid scalar currency is the weeds. Genuine structure lives below
  grid scale → the honest path to a structure-tracking fitness AND to Tier-2 is
  Route D (AMR / self-similar rescaling). Teed up as the next-session decision.

## g_sustained 256→512 rank check — 2026-07-24 — the rank SURVIVES the wall (Spearman +0.905), cheat audit clean at N=512

Full results: PHASE1_GSUSTAINED_RESULTS.md (Consequence section — the de-risk this
resolves). Script: phase1_gsustained_rankcheck.py (commit 19d51c0). Data:
experiments/phase1_gsustained_rankcheck.jsonl. This is the ONE expensive leg the
staged probe paused on: does g_frac's *ranking* hold at higher N, or is even the
rank on the uniform-grid wall? The user green-lit running it (over accepting the
negative now / pivoting to Route D).

What a human would want to know:

- **The rank holds across a doubling.** Spearman(rank@256, rank@512) = **+0.905**
  (precommitted bar > 0.85; 20/20 shapes finite). Essentially identical to the
  +0.90 at 128↔256 — the ordering did NOT degrade with resolution. The rank is not
  on the wall even though the magnitude is (g_frac@512 > g_frac@256 for every
  grower, e.g. struct_diag 0.33→0.74; the wall is real, only the order is stable).

- **Cheat audit re-run AT N=512 is clean** (not carried over from 256 — the banked
  lesson is that a rank can be stable AND cheat-organized): winner rand_01 is a
  genuine grower (t_res 2.95), top-5 all growers (5/5), ρ(g,log|ω₀|)=+0.21 (no ω₀
  cheat), ρ(g,centroid)=+0.31 (structure), ρ(g,t_res)=−0.70. Consistent with the
  256 audit.

- **The known-cheat control did its job.** accel_ratio was also rank-stable
  (+0.853) but winner rand_08 is a non-grower and ρ(accel_ratio,early_rate)=−0.58 —
  the small-denominator cheat, correctly separated from g_frac. The audit
  discriminates honest-vs-cheat even when both are rank-stable.

- **Ops note (a mistake, banked as a lesson, not a science problem):** the run
  finished cleanly but my monitoring hid it for ~10 min. A `while pgrep -f
  'script.py'` waiter matched *itself* (its own argv contains the string) so it
  never exited/notified; track.py's `py or raw` fallback then counted the leftover
  bash wrappers as a live producer and kept printing RUNNING. Fixed both
  (track.py commits aa402da, 81d592f): never wait on a pgrep pattern that matches
  the waiter, and never fall back to non-python matches when checking a python
  producer's liveness. The science/data were unaffected — all 40 solves present.

- **Verdict → forward.** Outcome (1): the g_frac rank-based currency survives the
  de-risk. Next is the reformulated 40-shape Gate 4 (property-4 ⇒ RANK-stable,
  property-6 ⇒ evaluated controlling for split). Paused at a checkpoint to review
  the reformulated predicate wording before spending the gate — reformulating an
  anti-self-deception predicate is exactly the step not to do unilaterally.

## g_sustained staged probe — 2026-07-24 — fixed-window magnitude fails (same wall); rank-based g_frac survives

Full results: PHASE1_GSUSTAINED_RESULTS.md. Data:
experiments/phase1_gsustained_probe.jsonl → writeup/data/phase1_gsustained.json.
This is the STAGED, cheap-first probe of the two Gate-4 forward refinements
(fixed-absolute window; free-split property-6), run before any 40-shape gate. The
user picked "continue staged (cheap caveat first)" at each fork, and the probing
kept paying off — it caught a second cheat and reframed the whole deliverable.

What a human would want to know:

- **The fixed-window refinement fails, and the reason is structural.** I measured
  the labeled ICs at N=128/256/512 and *looked at the trajectory* (window_diag
  scratchpad probes) before trusting any window. smooth_sharp re-accelerates right
  at the edge of its trusted window, and tail_guard pushes that edge out with N
  (t_res 2.46→2.74→2.98), so g_frac climbs 0.663→0.793→0.968 and never converges.
  Any window stable enough to avoid the drift sits in the earlier region where the
  spike already showed mild>sharp. You get stable OR blow-up-predictive, not both.
  This is spike finding #3 (near-singularity rate never resolution-converges on a
  uniform grid) reasserting — the SAME wall as ν_crit, on the growth-rate axis.
  Two currencies, one wall.

- **The rank order is what survives.** For a QD map only the ranking must be
  N-stable (bins are on resolution-stable descriptors). Spearman(rank@128,
  rank@256) = +0.90 for g_frac — the magnitude is on the wall but the order holds.

- **A second cheat, caught by the same reflex.** accel_ratio (late/early rate) was
  MORE rank-stable (+0.95) but is a small-denominator cheat: its winner rand_08
  never under-resolves (a non-grower), it mis-ranks the labeled ground truth
  (rand_08 +3.6 > sharp +1.4), and ρ(accel_ratio, early_rate) = −0.66. Its
  stability was real and worthless — it was stably ranking by the cheat. The
  banked lesson repeated: a rank-stable winner is a floor, not a ceiling; always
  interrogate against the dumbest cheat. g_frac passes the same audit clean
  (winner a grower, top-5 all under-resolve, ρ(g,log|ω₀|)=+0.17, ρ(g,centroid)=+0.31).

- **Caveat 2 (free split) is favorable.** No trivial max-split rail: a controlled
  split-sweep at fixed structure has an INTERIOR optimum (~0.3–0.5). The free-roster
  ρ(g,split)=+0.73 looked worrying but split↔ω₀ are mechanically entangled
  (ρ=−0.92); partial ρ(g,log|ω₀| | split)=+0.04 proves the ω₀ cheat is ABSENT and
  partial ρ(g,split | log|ω₀|)=+0.41 shows the split preference is genuine buoyancy
  physics. Honest caveat: split (logged, not binned) dominates ω-geometry.

- **Discipline notes.** Ran the 11-suite set (11/11) and committed the probe
  script (c1cf817) before the logged run; the run reproduced every scratchpad
  number exactly. STOPPED for review at the one remaining, expensive de-risk:
  256→512 RANK stability. If the rank holds → full reformulated (rank-based) Gate 4
  with property 6 evaluated controlling for split; if not → accept the negative.

## Gate 4 — 2026-07-24 — ν_crit FAILS property 6; inviscid growth-rate currency promising

Full results: PHASE1_GATE4_RESULTS.md. The headline: the pre-committed six-property
predicate printed 6/6 PASS, but that was a **false pass** — and catching it is the
whole point of the substantive re-analysis.

The frozen predicate (committed `5957155` before the run) anticipated the *1D*
property-6 failure mode (optimum → low-mode concentration) and tested spectral
centroid, which came back innocent (ρ=−0.15). But the real 2D degeneracy is
different: the smooth genome's free ω/θ split lets the "optimum" drive max|ω₀|→0,
trivially inflating amp=max|ω|/max|ω₀| (with κ=0 the undamped θ re-forces ω past
any viscosity). Diagnostic that caught it: **ρ(ν_crit, log|ω₀|) = −0.90**, slope
−2.11, R²=0.755 — ν_crit is 75% just the initial amplitude. Smoking gun: two
shapes reaching the SAME absolute vorticity get a 197× ν_crit gap from ω₀ alone,
and rand_24 grows MORE absolutely than rand_18 yet ranks 31× lower (the metric is
inverted vs propensity). A human asked exactly the right question — "be sure it's
actually a failure" — which forced the confirming analysis rather than trusting
the predicate's letter.

Then the disciplined ladder (each cheap, each decided on data): (1) fix the split
→ doesn't rescue (ρ(ν,log|ω₀|) −0.90→−0.44 persists; winner still trivial;
ρ(ν,centroid)=−0.21, the νk² dissipation wall reasserting). (2) normalized
resistance ν_crit·centroid² → only TAUTOLOGICALLY relocates the trivial optimum
(the centroid² multiplier dominates; struct_high has higher raw ν_crit but ranks
below struct_33 on centroid² alone) — exactly STAGE_2_5's "moves the trivial
optimum, doesn't remove it." So the ν_crit failure is the gCLM dissipation wall
reconfirmed, fundamental not fixable.

(3) One more currency (user decision): inviscid **sustained growth rate**
g_sustained escapes both cheats — inviscid (no νk² wall) + a rate not a ratio (no
ω₀ denominator). Probe clears the exact bars ν_crit failed: direction sharp
+0.79>mild +0.42>control 0.0; ρ(g,log|ω₀|)=+0.24 (cheat gone); ρ(g,centroid)=+0.38
(FLIPPED from ν_crit's −0.21 — structure rewarded). Necessary-not-sufficient
caveats: resolution-stability only modest (sharp 0.66→0.79, fractional window
drifts with t_res — fix with a fixed-absolute window); free-split untested (g
likely tracks split — real physics but a possible max-split triviality). A human
chose to DOCUMENT + pause before any further compute — banking the whole arc
before deciding the g_sustained Gate-4 path.

Compute note: the N=512 warm-start + 8 workers worked, but N=512 solves were
memory-bandwidth-bound (~12 min each under 8 concurrent FFT workers, ~3× a lone
solve). Stopped at 36/40 N=512 — property 6 is decided by N=256, and property 4
(the only thing the last 4 add) already passed on 36 shapes (all |Δν|≤½·tol).

## Gate 3 — 2026-07-24 — smooth 2D genome + ν_crit-analog fitness (built, no logged run yet)

Built the Gate-3 machinery: a smooth Hou–Luo-subspace genome
(`ga/genome2d_smooth.py`), the ν_crit-analog fitness wired through
`solve_boussinesq` (`ga/fitness2d.py`), and `test_genome_2d.py` (12/12; full
11-suite gate green). No logged experiment — Gate 3 is infrastructure; the first
logged 2D-genome run is Gate 4.

Genome design: ω = Σ a_jk sin(jx)sin(ky) (odd-x/odd-y, K=4), θ = Σ b_jk
cos(jx)sin(ky) (even-x/odd-y, j=0..K incl. the x-constant Luo–Hou modes). One
JOINT energy normalization pins total field energy at 2·ENERGY_BUDGET_2D, so the
overall-amplitude cheat (scale both fields up → needs more ν to kill; the 2D
analog of the 1D w→λw cheat) is removed, while the ω/θ energy RATIO (buoyancy
strength) stays free and is read off as the `split` descriptor. Confirmed
physically: because ν_crit is the fitness, a free overall amplitude WOULD be a
cheat (bigger fields need more viscosity) — fixing the budget is necessary, not
cosmetic.

MAP-Elites descriptor decision (raised with the user, then de-risked with a cheap
check before deciding). Candidates: anisotropy, spectral centroid, ω–θ alignment,
ω/θ split. A pure-genome probe (4000 random parity genomes, NO solver, seconds)
found: all four are mutually orthogonal (max |Pearson r| = 0.012 — none redundant,
unlike the 1D centroid/energy_top_k pair) and every pairing fills a 12×8 archive
at ≥0.83 coverage. So the cheaply-checkable failure modes are ABSENT for all
candidates — no empirical winner. The real differentiator (fitness-correlation →
archive collapse) is NOT cheaply measurable but comes free from Gate 4, so the
insurance move is: **bin on anisotropy × centroid, LOG all four raw** → binning
becomes a post-hoc, zero-re-run choice Gate 4's ν_crit data can overrule.
Rationale for the pair: both pure-geometry (unlikely to BE the fitness, keeping
cells populated), and the property-6 low-mode-collapse trap lands legibly on the
centroid axis. User approved.

Discipline notes: (1) the fitness reuses `ga.fitness.bisect_critical` with the v3
amplification-only predicate (amp≥2×, monotone in ν; an in-window slope is not —
the axis-screen smoke proved it), and its monotone-probes are exactly the Gate-4
property-6 instrument. (2) tail_guard makes the fitness read only the resolved
window. (3) The test suite's anti-self-deception anchor: a non-buoyant (2D Euler)
control conserves max|ω| → amp≈1 < 2× → ν_crit censored low (=0), confirming the
axis responds to the buoyancy mechanism, not merely to carrying a vortex.

## phase1_axis_screen (9033e6f) — 2026-07-23 — route fitness on ν_crit-analog

Why run BEFORE picking a fitness axis: the spike proved a resolution-stable
growth signal exists but flagged the confound — the windowed rate g is stable yet
NOT blow-up-predictive (smooth_mild has higher g yet saturates; smooth_sharp
lower g yet blows up). Rather than pick the axis on priors, a human asked the
right question: use the spike's two LABELED ground-truth ICs as a cheap
discriminator. Sharp BLOWS UP, mild SATURATES — so the routing question is simply
which candidate axis orders sharp>mild>control (propensity) AND is
resolution-stable. Necessary-not-sufficient screen (~an hour), not the gate.

Three axes at N=256,512 on {smooth_sharp, smooth_mild, euler_control}: (1)
ν_crit-analog = viscosity at which net resolved amplification crosses 2× (κ=0,
confirmed with the user; amplification is the blow-up currency, same predicate as
ga.fitness v3); (2) persistence = growth acceleration over the resolved window
(free from the ν=0 run); (3) g_baseline as the known-wrong-direction sanity axis.

The smoke (N=128) earned its keep BEFORE the committed run: the first ν_crit used
a windowed-slope zero-crossing, and smoke exposed it as contaminated — a
net-DECAYING mild run (amp=0.5) still showed a positive in-window slope, censoring
it in the wrong direction. Switched to the amplification boundary (monotone in ν,
cannot be fooled). A human-style discipline point: the screen caught its own
design bug because the labeled truth made the wrong answer visible.

Verdict (pre-committed gate): ν_crit is the SOLE survivor. Direction sharp
0.6519 ≫ mild 0.0483 > control 0.0000, and — the headline — ν_crit is IDENTICAL
to four decimals at N=128/256/512 (the amp-crossing ν is set by the dynamics, not
the grid). persistence FAILS on direction (the hard-saturating mild, persist
−2.69, sits BELOW the flat control ≈0 — it cannot rank a strong decelerator
against a non-grower; NOT a stability failure, correcting an earlier eyeball).
g_baseline reproduces the spike's mild>sharp (the built-in sanity check that the
discriminator is trustworthy). N=512 growers were ~32 min each (a single N=512
solve to t_max=4 is ~4 min × ~12 bisection runs); euler_control censored low in 1
run.

Honest scope: this settles ROUTING only. It clears the direction +
resolution-stability legs on 3 ICs; it does NOT clear the full six-property Gate
4. The big remaining risk is property 6 (non-trivial optimum) — the exact
property that killed gCLM's ν_crit (trivial k=1 collapse, STAGE_2_5). The Hou–Luo
singularity being robust smooth-data (not non-generic) is the REASON to expect
property 6 to fare better, but that's a hypothesis Gate 4 tests, not a result.
Next: Gate 3 genome wiring ν_crit(amp≥2×, κ=0, tail_guard window), then the
non-negotiable Gate 4. Full write-up: PHASE1_AXIS_SCREEN_RESULTS.md.

## phase1_resolution_spike (4741cda) — 2026-07-23 — de-risk: STABLE

Why run BEFORE the Gate 3 genome (a reorder, confirmed with the user): the
dominant risk to a Tier-2 result in 2D Boussinesq is not physics but RESOLUTION.
Unlike 1D gCLM (fully resolved at N≤4096), the Hou–Luo singularity is a corner
collapse Luo–Hou needed AMR (~1e12 effective) to track; on a uniform grid the
vorticity sharpens below grid scale before T*. So a cheap probe (hours) answers
"is there a resolution-stable fitness signal at feasible N?" before weeks of
genome/GA — exactly the Stages 2.5/3.5/3.6 de-risk-before-compute discipline.

Instrument added first (`solver` tail_guard): stop "under_resolved" when
enstrophy piles near the 2/3 dealias cut. A human noticed the key trap in
calibration: conservation drift stays ~1e-6 even when small scales are garbage
(∫w and energy-balance are robust to under-resolution), so drift is the WRONG
trust signal; the spectral tail is the right one. The solver now refuses to
report dynamics past that point.

Verdict STABLE (pre-committed gate in analyze_phase1_spike.py; full write-up
PHASE1_SPIKE_RESULTS.md). The fixed-window log-growth-rate g CONVERGES across
N=128→1024: smooth_sharp g→0.609 (finest-two 0.01%), smooth_mild g→1.239
(0.000%). Four findings: (1) resolution-stable growth fitness exists → search
viable; (2) the resolved window EXTENDS with N (amp_res 29→101×), so amp_res is
NOT a stable fitness but g is; (3) the blow-up EXPONENT/T* rails (a 2.45→1.20)
— uniform-grid Tier-2 confirmation of the true singularity is out of reach, the
resolution wall quantified; (4) rough C^{0,h} data is under-resolved from t≈0
(t_res 0.03–0.07 at all N) — the rough-data axis is resolution-starved on
uniform grids.

A gate-logic bug worth recording (fixed transparently, not post-hoc softening):
the first cut used STRICT per-step monotonicity for "converging", which gave a
false RAILS on g-sequences agreeing to <0.01% because of rounding-level (1e-4)
wobble. Replaced with "every successive relative change ≤ the pre-committed 10%
tolerance" — the honest reading of "settles across resolution", stronger than a
finest-two check and immune to rounding noise. The 10% threshold itself was
never moved (it passes by ~1000×).

Consequence (recalibrated, honest): PROCEED to Gate 3/4 on SMOOTH data with a
resolution-stable growth-based fitness (a ν_crit-analog is the prime candidate,
NOT amp_res); the near-term deliverable is a shape→growth QD map with Tier-1
candidates, NOT Tier-2-confirmed singularities (those need AMR / Route D). Gate 4
must still resolve which resolution-stable axis actually tracks blow-up
PROPENSITY — note smooth_mild has higher early g yet saturates, smooth_sharp
lower g yet blows up. Drop (or explicitly scope out) the rough-data axis.

## DECISION RECORD + boussinesq Gate 1a — 2026-07-23 — Route A Phase 1 begins

Post-Stage-3.6 review settled the scope: **commit to Route A Phase 1** (the
multi-week 2D-solver build), and — within Boussinesq — build around the
**Hou–Luo symmetry-wall geometry** (both decisions confirmed with the user). Why
Hou–Luo over the Elgindi-type C^{1,α} no-boundary variant: it is the setting of
the *computer-assisted proof* (Chen–Hou 2022) → best Tier-3/Route-D handoff; it
has a gold-standard numerical benchmark (Luo–Hou 2014) to validate against; and
its smooth-data singularity is robust, so the fitness is far less likely to rail
the viability gate than gCLM's non-generic axis did. The rough-data genome still
enters later as a C^{1,α} boundary-data variant. Full plan: PHASE1_PLAN.md.

**Gate 1a (doubly-periodic solver core) — PASS.** `solver/boussinesq.py`: full
fft2 pseudo-spectral 2D Boussinesq (w_t + u·∇w = th_x + νΔw; th transported;
Biot–Savart Δψ=w), RK4 + exact integrating-factor viscosity, 2/3 dealiasing,
advective CFL — the gCLM method lifted to 2D verbatim, same `SolverResult`
contract plus theta_final. Viscosity/thermal-diffusivity and the artifact guards
(∫w, ∫th conservation; kinetic-energy balance d/dt½∫|u|² = ∫vθ − ν∫w²) are
first-class from line one.

Validated by an exact analytic ladder (`test_solver_boussinesq.py`, 6/6), each
isolating one unknown: biot_savart 3.9e-16, rhs_terms (advection assembly +
buoyancy th_x vs hand-computed analytic RHS) 9.3e-15, scalar_transport (frozen-u
exact translate) 5.4e-11, viscous_decay 3.0e-15, taylor_green (w=e^{−2νt}sinx
siny exact solution — advection self-cancels) 5.3e-15, conservation 1.2e-16.
Everything at or near machine precision; the RK4-time-integration checks
(transport 5e-11, Taylor–Green 5e-15) confirm the coupled dynamics too. What a
human noticed: the Taylor–Green check is the strong one — it forces the
advection term and the Biot–Savart velocity to cancel exactly at machine scale,
which a sign error or a mis-indexed kx/ky mesh would not survive.

**Gate 1b (Hou–Luo symmetry-wall) — correctness PASS.** The no-flow wall is
imposed by parity (w odd-x/odd-y, th even-x/odd-y) rather than a Chebyshev
boundary: Biot–Savart then gives v even-x/odd-y (vanishes on y=0,π) and u
odd-x/even-y (vanishes on x=0,π), an effective [0,π]² box with the singular
corner at the origin. `test_boussinesq_wall.py`, 4/4: wall_bc 8.2e-17 (v,u zero
on the walls/axes at machine scale); **parity_preserved 9.0e-15 — the crucial
one: with NO projection, symmetric data stays in the subspace to roundoff, so
the wall is a genuine invariant of the discretised dynamics, not enforced by
fiat**; parity_enforced 3.7e-16; buoyancy_amplifies — a Luo–Hou-type IC (seed
vorticity + sharp buoyancy gradient) amplifies max|ω| 30.6× while holding parity
at machine scale and drift at 2.6e-6. The `symmetry="houluo"` solver option
projects each step so long runs stay exactly on the wall; the guard proves the
projection is only cleaning float-level leakage, not doing real work.

What is deliberately NOT claimed yet: the quantitative Luo–Hou growth curve /
finite-T\* singularity. Uniform-grid spectral resolution cannot reach the ~10⁷
amplitude Luo–Hou got with adaptive meshing, so matching their curve is a
separate resolution-limited study, and "how faithfully to chase it" is a
judgment call flagged for review rather than decided here. The two Boussinesq
suites (test_solver_boussinesq, test_boussinesq_wall) join the required pre-run
set for Phase 1.

**Gate 2 (port the Phase-0 method) — PASS.** Two pieces, each validated before
trust. (a) The 2D rough-data representation (`ga/genome2d.py`): the separable
Holder product w_h = P_h(x)P_h(y) with P_h = sign(sin)|sin|^h — automatically
odd-x/odd-y (the vorticity parity), plus the even-x/odd-y density partner
th_h = |sin x|^h P_h(y). Its slice at y=π/2 is exactly the 1D P_h, so the
Phase-0 regularity certificate transfers verbatim: `test_genome_rough_2d.py` 7/7
— corner Holder exponent recovers h, h=1 is exactly sin x sin y, the cusp x-slope
diverges at the N^{1-h} rate (C^{0,h}-not-C^1), tail energy monotone in h, and
the realized fields sit in the right parity subspace, energy-normalized. (b) The
fine-N exponent measurement is the SAME model-agnostic estimate_blowup_time; only
its wiring to the 2D solver is new, so it is validated on known-answer controls
(`test_phase1_measurement.py` 3/3): a synthetic (T*-t)^-a series is inverted back
to (a, T*) exactly (a=1.0/1.5/2.5, R²=1.0), and — the important one — 2D Euler
(buoyancy off, globally regular, ||w||_inf conserved) is fed through the whole
pipeline and must NOT reach Tier-2. It doesn't: ||w||_inf growth is 1.4%→0.4% as
N goes 128→192 (shrinking, as the theorem says), and the per-resolution T*/alpha
rail to OPPOSITE grid edges (T*=58,a=0.30 vs T*=12103,a=3.00, the finer with
negative held-out R²), so the convergence gate rejects it decisively. A single
coarse run's held-out R²=0.984 would have flagged a spurious candidate — exactly
why resolution-convergence, not single-run candidacy, is the real gate. What a
human noticed: the negative control is the sharp one — it proves the pipeline
cannot manufacture a Tier-2 blow-up from a flow we KNOW is regular, which is the
whole anti-self-deception contract, now demonstrated in 2D.

The four Phase-1 suites are solver-heavy (~30–60s each); the full 10-suite gate
needs a longer timeout than the 1D-only set. Next (STOP for review first): Gate
3 — the 2D genome data structure + MAP-Elites reuse, then the NON-NEGOTIABLE
Gate 4 viability gate before any GA compute.

## DECISION RECORD (not an experiment) — 2026-07-23 — Route A, Phase 0 is next

Post-Stage-3.5 review with the user settled the forward path. Decision: pursue
Clay via [CLAY_ROADMAP.md](../CLAY_ROADMAP.md) **Route A** (switch to a model
where non-generic blow-up is provable — 2D Boussinesq / C^{1,α} De Gregorio),
and fold the former "Route C" (cheap rough-data + fine-N gCLM probe) into it as
**Phase 0** rather than running it as a parallel detour.

Why Phase 0 first, not a leap to the 2D solver: two unknowns (a new solver AND a
new non-generic-exponent measurement) must not be debugged simultaneously — on a
weird rough-data blow-up you couldn't tell solver bug from measurement bug.
Build/validate the *measurement* on the 1D substrate where the answers are known
(CLM analytic T*, De Gregorio literature), then port a trusted method to 2D.
Phase 0's real value is the transferable method + rough-data genome + an honest
"is gCLM exhausted?" check — NOT a gCLM science result (Stage 3.5 makes a
converged non-generic exponent unlikely). What transfers to Phase 1 is the
method and the representation *principle*, not the 1D genome code; a Phase-0
negative is informative, not a kill-signal (Boussinesq is a different
mechanism). Hard 2-day time-box + pre-committed converge/rail gate so it can't
become open-ended 1D tinkering. Concrete spec: PLAN.md Stage 3.6.

## stage3_6_sweep (95ef09f) — 2026-07-23 — Route A Phase 0: RAILS (expected)

Why configured this way: the execution of the decision record above. Two
deliverables + one gated verdict, on the validated 1D solver. (1) A genuine
C^{1,α} rough-data genome mode — `holder_profile(h) = sign(sin x)|sin x|^h`,
an odd C^{0,h} vorticity with a *localized* Hölder cusp, unlike the delocalized
random-phase field the k^{-p} envelope reaches. Chose the real-space local
Hölder exponent as the regularity certificate (test_genome_rough.py) because
the spectral-decay rate is contaminated by the second cusp at x=π and
finite-k roundoff, whereas |f(x)|∼x^h near 0 is exact and definitional; also
pinned the C^{0,h}-not-C^1 signature (max|f′|∼N^{1-h} diverges). (2) A fine-N
exponent probe at N∈{1024,2048,4096} over h∈{0.2..1.0} × a∈{0.7,0.9,0.95,1.0}.
Added a=0.7 as a **methodological control** (not in the original spec's a-list
but demanded by "validate the measurement where the answer is known"): Stage
3.5 says a=0.7 must read generic α≈1 stably, so if the fine-N fit doesn't
recover that, the probe is inconclusive rather than a verdict. Frozen at the
Stage 3.5 config (t_max=24, amp=1e3, tail 0.15) except resolutions; max_steps
200k so De Gregorio non-blow-up runs bail (~700s each at N=4096) instead of
hanging. Pre-committed gate in analyze_stage3_6.py, not softened after seeing
data.

What a human noticed skimming the results (experiments/stage3_6_sweep.jsonl,
72 rows; full write-up STAGE_3_6_RESULTS.md):

- The control worked *perfectly*: a=0.7 is α∈{1.00–1.10} across a 4× grid
  range for every h, 18/18 usable. That's what lets the near-a=1 negative be
  believed. Mild honest wrinkle: the roughest shapes (h=0.20/0.35) tick from
  1.00 to 1.05–1.10 only at N=4096 — a small finite-N wobble, but still
  generic, never railing.
- Rough data DID revive blow-up *occurrence* — a=0.9 went 18/18 usable fits
  (vs Stage 3.5's 20/40 usable + 15 flips at N∈{256,512}). For a moment that
  looked like progress. But the exponent still scatters non-monotonically
  across resolution (median cross-N span 0.65, max 1.95; e.g. h=0.50:
  2.60→0.65→1.20). Occurrence improved; convergence did not.
- a=0.95 rails outright — h=0.20 goes 0.30→0.85→3.00, spanning the whole fit
  grid across resolution, and 4/18 flip well-definedness. a=1.0 (De Gregorio
  proper) is stone dead: 0/18 blow up even for C^{0,0.2} data (slow runs hit
  the 200k step cap). Not evidence of regularity (WIN_CONDITION.md) — just no
  searchable signal.
- Key reassurance the rail is real, not slop: max conservation_drift over all
  72 runs is 1.9e-4, well under the 1e-3 guard, and every counted fit clears
  R²≥0.9. The runs are well-resolved and individually clean; the exponent
  simply has no resolution-stable limit. Going N=256/512 → 1024/2048/4096 did
  not shrink the scatter (max span 2.70 vs Stage 3.5's 2.7). Refinement
  doesn't help — the strongest cheap evidence that gCLM's non-generic exponent
  is a grid-scale feature, not physics.
- Net: the cheap 1D route to a novel non-generic result is closed for smooth
  AND rough data. But the two deliverables (rough-data representation +
  validated fine-N method) transfer to Phase 1 exactly as scoped. STOP for
  review per the gate before any 2D solver work.

## nongenericity_sweep (7b… post-Stage-3) — 2026-07-23 — NO VIABLE AXIS

Why configured this way: review question after Stage 3 — the GA edge is at
a=0.7 but every confirmed blow-up there is generic (α=1.000), whereas the novel
Tier-3-provable target is non-generic (α≠1) near a=1 with rough data. Sweep
measured |α−1| inviscid across a∈{0.7,0.9,1.0} to see if the edge regime and
the novel regime overlap, before spending any GA compute. Amp raised 100→1e3
so α is fittable (100× gave R²=−1.7 garbage in the marginal regime in the
pre-build probe); max_steps capped at 300k so no-blow-up/near-critical runs
bail instead of burning t_max. p-regime question folded into the analysis via
the 20 init-prior draws' native envelope_p (they already span [0.02, 3.30]).

What a human noticed skimming the results:

- The answer is a clean "disjoint," and sharper than expected. At a=0.7 α is
  pinned at 1.00 for ALL 37 blow-ups including the p=0.02 (nearly white) draw —
  Spearman(|α−1|, p) = −0.07, i.e. roughness does nothing to the exponent
  there. Whatever the GA evolves at a=0.7, it's generic CLM. Independently
  re-confirms Stage 3's α=1.000 across the whole roster, not just the elites.
- a=0.9 is the tell: non-genericity DOES appear (α up to 3.0) but it's pure
  grid artifact — 15/40 well-def flips, and the biggest |α−1| shapes rail to
  α=3.0 at N=256 then collapse to 0.30–0.60 at N=512 (max Δα=2.7). This is
  literally the Stage 1.5 a_crit "near-critical advection collapse scale"
  instability, now on the exponent. Wrote it up as such.
- a=1.0: 0/40 blow up (34–35 clean no_blowup, rest stiff step-cap). Dead axis,
  as Stage 2.6 already found for smooth data — restated with the WIN_CONDITION
  non-goal caveat (absence of signal ≠ regularity).
- Net: the gate earned its keep — 240 runs / ~2 min killed a GA campaign that
  would have been optimizing resolution noise. The three forward options
  (rough+fine-N; switch to 2D Boussinesq; bank the 1D pipeline) go to review;
  NONGENERICITY_RESULTS.md records them.

## stage3-resolution-20260723T082807 (57b4a88) — 2026-07-23 — TIER 2: 18/18 CONFIRMED

Why configured this way: studied the top-3 elites per acceptance seed (9
genomes, spread across 9 MAP-Elites cells, all 3 seeds) rather than only the
single best, so a promotion means the evolved *shape family* confirms, not one
lineage. Two operating points per elite because fitness is a ν_crit bisection
but a resolution study is one trajectory: ν=0 (cleanest, gates promotion — the
sharpest test of the C^∞-may-not-blow-up regularity caveat) and ν=0.5·ν_crit
(inside the band; confirms the viscosity-resistant blow-up itself refines). Ran
each elite's *own* frozen config.json, not a shared default — the study must
mirror the exact fitness config each elite was produced under. Amplification
raised 100×→10⁴×: at a fixed 100× stop every resolution halts at the same
physical state, making T\* agreement almost tautological; 4 decades of growth
actually stresses the extrapolation.

What a human noticed skimming the results:

- The convergence is almost too clean. Inviscid 512→1024 relative T\* diff
  maxes at 3.5e-6 against a 2e-2 gate (~5000× margin); the top elite gives
  *bit-identical* T\*=2.17320 at N=1024 and N=2048. That is the signature of a
  singularity already fully resolved at N=256, i.e. NOT forming at
  ever-smaller scales — the direct refutation of the resolution-artifact worry
  for these shapes.
- Every single confirmed blow-up fits α=1.000 exactly. This is the *generic
  CLM* exponent, not a De Gregorio non-generic one — so honestly these are the
  CLM singularity surviving a=0.7 advection, consistent with (not beyond) the
  literature. Wrote this into STAGE_3_RESULTS.md so the pipeline-validation win
  isn't mis-sold as a new singularity. The novelty stays the QD map.
- Conservation drift *shrinks* monotonically with N (6.7e-5 → 1.0e-6 as
  256→2048), the opposite of an under-resolved run. The artifact guard (1e-3)
  never engaged; it is there for the axes we haven't confirmed yet.
- Cost was trivial (~4s/run at N=1024, 18 studies × 3 N in well under a
  minute at 10 workers) — the expensive part of this project was always the
  bisection-heavy GA, not the confirmation.
- Literal PLAN wording says "De Gregorio genome"; our axis is a=0.7, and a=1 is
  a dead axis for smooth odd data. Flagged the gap explicitly rather than
  quietly reinterpreting the criterion.

## stage2_6-seed1/2/3 (a10d6b2) — 2026-07-22/23 — FINAL: ACCEPTANCE PASS 3/3

**Final verdict (analyze_stage2.py): STAGE 2 ACCEPTANCE MET.** GA vs
random at matched budget: 0.1624/0.1591 (+3.3 tol), 0.1631/0.1585
(+4.6 tol), 0.1629/0.1597 (+3.2 tol); domination over the final half of
the budget on all seeds; GA above the literature best (0.1585) on all
seeds, random on none. QD replay (secondary): random still covers more
cells (74–79% vs 50–56%); GA wins QD-score on seed 3 only — peak search
and map-building remain different objectives (tuning lever: exploration
pressure). Cross-seed archives: Jaccard 0.62–0.72, |Δfitness| 0.005–0.011
on shared cells. Health: censoring 5/3/8, non-monotone 0/5/2 (excluded
from archives by rule), lit control reproduced the sweep within 1 tol on
every seed. Full write-up: STAGE_2_6_RESULTS.md. Next: Stage 3 resolution
study on the elites (pending review).

The interim seed-1 analysis below is preserved as written mid-protocol:

Why configured this way: the Stage 2 acceptance protocol rerun on the
axis Stage 2.6's gate verified — nu_crit under the v3 amplification-only
oracle at a=0.7, t_max=24, bisection [0, 0.3] tol 1e-3 (config-only
changes at commit a10d6b2). 3 seeds, pop 24 × 25 gens, budget-matched
interleaved baseline_random, literature control re-sampled at run start.

**Seed 1 interim analysis (written mid-protocol so a crash cannot lose
it; final 3-seed verdict pends in STAGE_2_6_RESULTS.md):**

- Shakedown clean: literature control best 0.15849 vs sweep's structured
  best 0.15820 (within 1 tol). ~170s/generation at 10 workers.
- **First-ever GA-vs-random separation in this project.** Random init
  ceiling (gen 0, 24 draws): 0.14736. Final GA best: 0.16236 at gen 21.
  Interleaved random baseline plateaued at 0.15908 (~600 draws). GA
  finished ~+3.3 tol above random and above the best literature profile
  (0.15849) — margin modest but structurally meaningful: the GA climbed
  where random stalled.
- **Operator attribution (the "do we need better breeding?" question,
  answered from the event stream):** after gen 0, ALL eleven best-so-far
  improvements came from variation — 6 mutation, 5 crossover, 0 from
  later random draws — a monotone climb 0.147 → 0.150 → 0.153 → 0.155 →
  0.158 → 0.160 (gens 1–9) then 0.161 → 0.162 (gens 12–21). Archive
  insertions: 96 mutation / 86 crossover / 21 init. Both operators
  productive for both peak fitness and map-building. Verdict: breeding is
  effective; no operator changes warranted, and none permitted mid-protocol
  (frozen acceptance config; changes would restart all 3 seeds).
- **Post-verdict tuning leads, if wanted (from this seed's data, to be
  re-checked against all 3):** (1) improvements still arriving at gen 21
  while mutation scale has decayed 0.3 → ~0.05 — a scale floor or longer
  run plausibly buys more; 25 gens may truncate the climb. (2) Archive
  coverage plateaus at 0.500 from gen ~17 (QD still creeping) —
  exploration pressure (novelty bonus / empty-cell-directed emission) is
  the standard lever if the map deliverable needs more coverage.
  (3) No evidence the genotype (sine coeffs + envelope p) is the
  bottleneck — the winning shapes are low-k mixtures it represents
  directly.

## stage2_5_sweep A + B (A: f3dc522, B: a005ef8) — 2026-07-22

Why configured this way: PLAN.md Stage 2.5's answer to the Stage 2
verdict — before any GA rerun, gate a redesigned fitness axis on the
six-property checklist, with the non-trivial-optimum property measured
against the GA's ACTUAL init prior (20 draws with the Stage 2 config's
N=32, p ∈ [0, 3.5]) alongside the 20 Stage 1.5 shapes. Candidate A:
ν_crit at a ∈ {0.4, 0.7, 1.0} (largest passing a wins). Candidate B
(fallback): ν_crit at a=0 under a k≤2 ≤ 50% energy cap enforced at
normalization. Same frozen v2 oracle and tol 1e-3 as Stage 2; a range
ladder [0,0.1]→[0,0.4]→[0,1.0] because moderate advection turned out to
RAISE ν_crit ~3× (unexpected and interesting on its own).

**Verdict: no viable axis — every candidate fails, each differently, and
the pattern is the finding** (full numbers: STAGE_2_5_RESULTS.md):

- a=1.0 (De Gregorio): dead axis. 35/40 censored low at ν=0. The k=1
  refuge dies at the equilibrium, but so does essentially all smooth-data
  blow-up within the horizon — only rough low-k1 prior draws survive, at
  ν_crit ≈ tol/2. The literature's smooth-data regularity expectation,
  watched in real data.
- a=0.7: the only landscape with a genuinely structured top (prior-vs-
  structured gap 21·tol) — but it fails monotonicity, and the audit shows
  why: 100% of its boundary decisions are fit-decided (slow α≈0.3 growth,
  T* extrapolated just inside the 1.5·t_max cap), vs 19/19
  amplification-decided at a=0. One shape's classification flickers
  non-monotonically as fit quality dips and recovers across a marginal
  band (island at ν ∈ [0.026, 0.031], R² up to 0.997). The critical value
  at a>0 measures "where a marginal extrapolation crosses the horizon
  cap" — resolution-exact but semantically soft.
- a=0.4: Stage 2's disease softened but present — gap 7·tol,
  ρ(ν_crit, k1frac) = 0.79; prior sampling reaches the top region.
- Candidate B: PLAN.md's own stated risk realized verbatim. Seven-way tie
  at the top, every one at EXACTLY the 0.5 cap boundary; best prior draw
  EQUALS best structured (gap 0.0); ρ(k1) = 0.91. The cap relocates the
  trivial optimum; it does not remove it.

What a human should take away: ν_crit on gCLM at fixed horizon is, in
every variant tried, a thin wrapper around the νk² dissipation scaling —
a spectral-concentration quantity the init prior samples directly. No GA
can beat random on it, and the six-property gate now proves that for ~40
bisections (~10 min) instead of ~3 GA-seed-days. Stage 2 acceptance rerun
deliberately NOT executed. Paths forward (oracle v3 + a=0.7; rate-based
fitness; ν_crit normalized by the shape's own k²; or accept the negative
result and re-scope) are redesign-level and go to review.

## stage2-seed1 / seed2 / seed3 (d47b579) — 2026-07-22

Why configured this way: the Stage 2 acceptance runs — 3 independent seeds,
pop 24 × 25 generations = 600 GA evals each, budget-matched interleaved
baseline_random (612 with the literature control), frozen fitness config
(nu_crit at a=0, N=256, t_max=12, bisection [0, 0.1] tol 1e-3, v2 oracle).
~12,200 solver runs / ~64 min per seed at 10 workers.

**Verdict: acceptance NOT MET, decisively and in triplicate — and the
reason is a finding, not a bug.** The nu_crit landscape at a=0 has a
trivially-located global optimum: pile energy into k=1. Numbers:

- Best-so-far: GA 0.0543 / 0.0543 / 0.0545 vs random 0.0543 / 0.0543 /
  0.0543. Margin 0, 0, and 0.2× tolerance. Both sides hit the ceiling
  within ~12 evaluations (order-statistics of the init prior, not search).
- All three seeds' best genomes are >= 99.5% k=1 energy with a few % of
  one low harmonic (k=2..4). Two of three were raw init draws; seed 3's
  crossover polish bought +0.0002 (~0.2 tol). This is the nu*k^2 scaling
  argument, rediscovered empirically: lowest mode survives viscosity best.
  PLAN.md's "frequency-space cheating" guardrail worry turns out to be the
  honest global optimum of this axis, not a cheat.
- Sharper: random *dominates the GA on map-building too* — replaying both
  event streams through identical archive-insertion rules, random reaches
  74–79% coverage / QD 2.6–2.7 vs the GA's 46–58% / 2.0–2.2 at the same
  budget. Fitness-driven tournament selection concentrates parents on a
  flat plateau; exploration is all cost, no signal. On a saturated
  landscape MAP-Elites' selection pressure is strictly worse than prior
  sampling for the map deliverable.
- The pipeline itself behaved to spec: 0/1800 GA+random evals censored
  (bump(κ=5) control aside), 6 non-monotone flags in 3,672 evals, ~6%
  bracket-expansion rate, warm starts saving ~2 runs/eval, zero cache
  hits (expected: MAP-Elites never re-evaluates elites).
- The map interior is real but partially confounded: median nu_crit falls
  smoothly with oscillation count (0.054 at 2 sign changes → 0.028 at 20)
  and with tail roughness — but per-bin maxima sit at ~0.054 nearly
  everywhere because the two archive descriptors don't pin k=1 dominance
  (a 99%-k=1 genome can carry any tail slope in its negligible tail).
  Cross-seed final archives: Jaccard 0.61–0.69, mean |Δfitness| on shared
  cells ≈ 0.0064 (~6 tol) — moderate convergence, consistent with sparse
  per-cell sampling.

Lesson recorded for any future fitness axis: Stage 1.5's viability
properties (nonzero, finite, monotone, resolution-stable, wide band) are
necessary but NOT sufficient — they never asked *where the optimum lives*.
Add a sixth check: the optimum must not be reachable by trivial sampling
of the init prior (e.g. require the best of ~20 random draws to sit well
below the best hand-constructed shape).

Redesign options for a non-degenerate axis (review decision, in rough
order of preference): (1) bandwidth-constrained nu_crit — cap the k=1 (or
top-k) energy fraction, or pin the spectral centroid, so resistance must
come from structure; (2) move to a > 0 (De Gregorio side) where advection
fights growth and low-k concentration stops being free — requires the
resolution-convergent oracle Stage 1.5 says the a-axis needs; (3) score
QD/map metrics directly rather than scalar best-so-far.

## stage2-shakedown (d47b579) — 2026-07-22

Why configured this way: first end-to-end run of the Stage 2 GA harness —
deliberately tiny (pop 6, 3 generations, seed 999) to shake out the
pipeline before the real 3-seed acceptance runs, per PLAN.md. Full frozen
fitness config (N=256, t_max=12, bisection [0, 0.1] tol 1e-3, v2 oracle).

What a human noticed skimming the results:

- The literature positive control lands where Stage 1.5 put it: sin(x)
  0.0535 (vs 0.0527 at the coarser Stage 1.5 tolerance), sin(2x) 0.0137
  exactly, and bump(κ=5) censored "low" — the beyond-horizon control
  behaves inside the GA harness too.
- Warm-started child evaluations took a median 9 solver runs vs 11 cold,
  with 0 bracket expansions in 12 — the ±0.01 margin is, if anything,
  generous; leaving it.
- Median 15.3s per evaluation, ~2× the Stage 1.5 per-bisection cost:
  the [0, 0.1] range concentrates bisection samples near the critical
  value, where no-blow-up runs burn the whole t_max. Real-run sizing
  (~25 min/seed at 10 workers) accounts for it.
- A random init genome (0.0543) edged out sin(x) immediately — the
  landscape above 0.053 is reachable, but the random baseline found it
  too. Whether the GA can *separate* from the baseline is exactly what
  the 3-seed acceptance runs measure.

## stage1_5_sweep (v1: 5c6dfc2, v2: b05b9bf) — 2026-07-22

Why configured this way: t_max=12 chosen after computing analytic CLM T*
for all 20 normalized ICs (live shapes span 1.0–6.5; bump(κ=5) at 15.9 kept
deliberately as a beyond-horizon censoring control). ν bisected at a=0 to
isolate viscosity in the proven-blow-up regime; a bisected at ν=0. One
energy scale (E of sin(x)) across all shapes so critical values compare
shape, not amplitude.

What a human noticed skimming the results:

- The ν axis is astonishingly clean: all 80 v1-vs-v2 and 256-vs-512
  ν-bisections take *identical* decision paths. The sin(2x) value landing at
  ν_crit(sin)/4 (νk² scaling) was not designed in — good sign the number is
  physical.
- The v1 a-axis anomalies (censored-high at N=512 only, for two shapes) all
  traced to one predicate flaw: accepting held-out-R²≈0.9 fits whose
  extrapolated T* was 6–11× beyond the horizon. Capping T* at 1.5·t_max
  (v2) fixed every one; tail(p=1)'s 2× resolution drift survived the fix
  and is the real, physical reason a_crit was rejected.
- 14% of amplification-stopped runs had tail fits below the R² floor
  (bursty near-critical growth) — the amplification-first predicate rule
  mattered in practice, not just in principle.
- Energy-balance residuals up to 0.5 on ν-axis blow-up runs looked alarming
  but are endgame dt-integration error: halving dt halves them and moves
  ν_crit by exactly zero (3-shape spot-check at N=512).
