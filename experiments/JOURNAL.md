# Experiment Journal

Hand-written context per experiment (see LOGGING.md — the structured logs
answer "what happened"; this records *why* and what a human noticed).

## Phase-2 P2 — TWO-SCALE a_p(K) CONVERGENCE map — LOGGED (7/7) — 2026-07-26

**LOGGED gate run** (predicate T1–T7 LOCKED in git before the run, commit 44a507c).
Data: committed `writeup/data/p2_two_scale_kladder.json`; harness
`experiments/p2_two_scale_kladder.py --logged`; writeups TECHNICAL/BLOG_P2_KLADDER
+ fig18 (rebuilds from JSON via `writeup/p2_two_scale_kladder_evidence.py`);
PHASE2_P2_NOTES.md §9-cont2. Verdict **7/7 clauses hold** — a NOVEL toy-model
characterization (Tier-1/2), NOT a proof, NOT a Clay solve. This SHARPENS the prior
leg's T4 FAIL (the honest one): it turns the "genome-relative soft boundary" caveat
into a converged, resolvable answer.

What a human would want to know:

- **The question (from the prior leg's T4 fail).** The two-scale a-sweep found the
  exact a=0 traveling wave persists (relres<1e-2) only to a_p≈0.40 for a FIXED even
  K=2 genome — but T4 FAILED: a richer K=3 genome cut the a=0.5 floor 4×, below the
  1e-2 line. The GA gives only an UPPER BOUND, so a_p(K) can only rise with K. Open
  question the user chose to sharpen: does a_p(K) **saturate** (→ a genuine survival
  boundary a\*) or **keep marching out** with K (→ INCONCLUSIVE, genome-limited)?

- **The confounder the scout caught (this is the whole ballgame).** At the base
  budget the higher-K floors are **search-limited, not converged**: a GA-convergence
  probe showed the a=0.6 K=4 floor drop **45%** when the budget was doubled. A naive
  a_p(K) map at the old budget would have reflected GA effort, not genome richness.
  A scratch plateau probe (a=0.55/0.60, K=4/6, budgets 1×→8×) settled it: the floor
  **PLATEAUS** — a=0.55→~1.0e-2 and a=0.60→~1.8e-2, stable under ~8× budget AND not
  improved at K=6. That fixed the logged budget at pop150/gen250/8-seeds (converged)
  and put an IN-JSON budget spot-check (~1.7×) + a K=6 genome spot-check in the run
  so the plateau is reproducible from committed data, not just scratch.

- **Result (7/7).** a_p(K) = **0.40 → 0.50 → 0.50** — it rises off the K=2 value
  then **SATURATES**. Boundary a\* ≈ 0.55 (smallest a where the converged K=4 floor
  first exceeds 1e-2: K4(0.55)=1.08e-2). At the boundary the floor is **GA-converged**
  (K4 1.7×-budget 1.03e-2 vs 1.08e-2, <5%) and **genome-converged** (K6 1.23e-2 does
  NOT beat K4 1.08e-2), and **basis-independent** (a different even basis, Lorentzian
  + squared-pole `even_lorentz_sq`, gives 8.3e-3, within 3× of even K3). Resolution
  fine (min verdict width 35 grid pts ≫ 8). Far-end (De Gregorio) robust: K4 floor
  rises to 1.28e-1 at a=1.0 — survives richer genome + budget (this was the prior
  leg's ONE robust T4 sub-claim, now confirmed across the whole K-ladder).

- **The honest nuance I did NOT bury.** a\* is not a razor edge. Right at a=0.55 the
  converged floors straddle the 1e-2 line: even K3/K4 sit just above (≈1.1e-2) while
  the mixed basis dips just under (8.3e-3). That is exactly what a threshold crossing
  looks like — the boundary is a\* ≈ 0.5–0.55 with a soft ~1e-2 floor, not a sharp
  wall. Reported as such; the SCIENCE claim is "saturates near 0.5–0.55, genuine, not
  genome-limited," not "dies exactly at 0.55."

- **Bug/discipline notes.** New solver basis `even_lorentz_sq` (X^-4 poles) added +
  unit-tested as the basis-independence cross-check: gated to be genuinely DIFFERENT
  (a single squared pole is NOT an a=0 traveling-wave null, relres=0.11) yet to still
  CONTAIN the exact anchor (Lorentzian+zero-squared mix → 1.3e-8), so T1 holds on it.
  test_gclm_family 12/12; full suite 7 files green. Observed the plateau in scratch
  BEFORE locking the predicate (grounded the budget + thresholds). Did NOT re-run to
  move any clause.

- **Where this sits + next.** This is a Level-1 result (a novel *numerical* map), now
  clean and convergence-guarded — it does NOT move up the rigor ladder, it makes the
  Route-D **guess** sharper and better-justified (a\*≈0.5–0.55 boundary + the a=0
  exact + near-boundary profiles). **User confirmed Route D is the next brick**: an
  interval-Newton / Newton–Kantorovich certification on those profiles — the first
  rung that is genuinely "novel maths" (Level-2). Clay odds unchanged (~0.05%).

## Phase-2 P2 — TWO-SCALE-under-advection a-sweep — LOGGED (5/6, PARTIAL) — 2026-07-26

**LOGGED gate run** (predicate T1–T6 LOCKED in git before the run, commit 6fc1ff0).
Data: committed `writeup/data/p2_two_scale_sweep.json`; harness
`experiments/p2_two_scale_sweep.py --logged`; writeups TECHNICAL/BLOG_P2_TWO_SCALE
+ fig17 (rebuilds from JSON via `writeup/p2_two_scale_sweep_evidence.py`);
PHASE2_P2_NOTES.md §9. Verdict **5/6 clauses, PARTIAL by construction** — a NOVEL
toy-model result (Tier-1/2), NOT a proof, NOT a Clay solve.

What a human would want to know:

- **The question.** HQW25 (arXiv:2401.14615) proves CLM (a=0) has an EXACT two-scale
  self-similar blowup whose profile is a TRAVELING WAVE Ω₂=−1/(1+X²). Does that
  mechanism survive gCLM advection as `a` grows (a=0 CLM → a=1 De Gregorio)? Nobody
  had mapped it. This is the novelty swing the user chose.

- **What we built + derived.** The two-scale residual R₂=ΩHΩ − c_tw Ω_X − a U Ω_X:
  carried HQW25's moving-frame ansatz to its leading (T−t)^{−3} order → a PURE
  TRAVELING WAVE (the dilation −c_l XΩ_X and amplitude c_ω Ω terms are subleading and
  DROP). Structurally a TRANSLATION, not a dilation. a=0 known-answer gate: Ω₂ nulls
  R₂ to 1.5e-9, gauge speed c_tw=0.5000000; EVERY even_lorentz A/(1+BX²) is an exact
  a=0 TW with c_tw=−A/(2√B) → the a=0 set is a 2-parameter scaling valley.

- **The GA-cheats bug we caught pre-lock.** Plain RMS ‖R₂‖ is NOT scale-invariant —
  a GA drives amplitude→0 (c_tw→0), a trivial null. Switched to the scale-invariant
  relres=‖R₂‖/‖ΩHΩ‖ (fraction of stretching unaccounted). The scratch literally
  showed the pathology first; fixing it is why the result is trustworthy.

- **Pre-lock robustness scout (grounds the thresholds).** The floor curve is INVARIANT
  across n=601/801/1201 and rho_max=8/10 (physical, not a tail artifact) and
  GA-converged (2.5× budget barely moves it). Config locked n=801, 6 seeds.

- **Result (5/6).** T1 known-answer PASS (5.8e-8). T2 persistence PASS: relres<1e-2
  out to a_p=0.40 (deformed-but-present traveling profile). T3 monotone-degradation
  PASS: floor rises to 1.8e-1 at a=1. T5 symmetry PASS: odd-fraction<0.013 throughout
  (mixed genome free to skew, STAYS EVEN). T6 resolution-guard PASS (min 49 pts).
  **T4 FAIL (the honest headline):** at a=0.5 a richer even K=3 ansatz cuts the floor
  4× (2.45e-2→5.6e-3), so the mid-range floor is partly GENOME-LIMITED — the K=2 map
  is a genome-relative UPPER BOUND, the survival boundary is NOT sharply pinned. This
  is exactly the pre-committed INCONCLUSIVE branch, reported not hidden. BUT at a=1
  K=3 does NOT rescue (1.83e-1→1.43e-1) → the De Gregorio-end degradation is robust.

- **Honest picture.** No sharp collapse: the two-scale traveling wave DEFORMS SMOOTHLY,
  persists well for small a, degrades toward De Gregorio, stays even, and advection
  SELECTS a scale (lifts the a=0 valley). Endpoints robust; middle genome-relative.

- **Discipline held.** Did NOT re-run to chase T4 into a pass. The T4 fail is the
  machine catching its own limitation — the right outcome. Next: richer/spectral
  genome to sharpen a_p (or a Route-D interval-Newton on these guesses); separately,
  the coupled-system HL two-stage leg. Clay odds unchanged (~0.05%).

## Phase-2 P2 — GA GLOBAL-SEARCH FRAMEWORK (BUILD/scout, NOT a logged gate run) — 2026-07-26

**Infrastructure build + a=0 known-answer validation. No logged experimental run; no science claim.**
Banked record: PHASE2_P2_NOTES.md §9 + writeup/TECHNICAL_P2_GA_FRAMEWORK.md + BLOG_P2_GA_FRAMEWORK.md
+ fig16 (rebuilds from committed writeup/data/p2_ga_framework.json). Code: solver/gclm_family.py,
solver/ga_search.py; tests test_gclm_family.py (6/6; full suite 7/7).

What a human would want to know:

- **What the user asked for.** Pursue the gCLM two-scale↔two-stage transition (the novelty swing),
  and do it VIA a genetic algorithm (their idea), built to also serve Route D. Then: gCLM axis first,
  bridge to HL later.

- **What we built.** A GLOBAL search for self-similar profiles: the gCLM `a`-family rescaled residual
  R = (c_ω+HΩ)Ω − c_l XΩ_X − a U Ω_X (solver/gclm_family.py, velocity U=∫₀ˣHΩ cached) + a generic,
  problem-agnostic real-coded GA (solver/ga_search.py). Deliberately separate from the relaxation
  solvers so the SAME residual object is reusable by a future Route-D interval-Newton certification.

- **Why a GA (honest, said to the user).** Relaxation is LOCAL — it finds the attractor you seed near.
  A family can have MULTIPLE fixed points (different blowup mechanisms); a GLOBAL search maps the set +
  bifurcations = the open two-scale↔two-stage question. A GA proves nothing (Tier-1/2); its roles are
  the global mapper + the "guess" stage for Route D.

- **Fetched the missing anchor.** [HQW25] = arXiv:2401.14615 (Huang–Qin–Wang) downloaded to Papers/.
  Gives the EXACT a=0 two-scale profile Ω₂ (an even Lorentzian bump, c_ω=−3/2). Also corrected the
  framing: HQW25 two-scale = CLM (a=0, scalar gCLM); CHL two-stage = HL coupled system (different
  axis). Well-posed gCLM question: does the a=0 two-scale survive advection as `a` grows?

- **a=0 gate PASSES.** Exact Ω₀ nulls the residual to 2.2e-7; the GA recovers the exact steady set — as
  a 1-parameter DILATION family (gauge is dilation-invariant), so only the invariant A²/B=4.000 is a
  "match". The banked "report gauge-invariants only" lesson literally showed up as a valley (not a
  basin) in the GA landscape (Fig16A). Nice confirmation the discipline is right.

- **Diagnostic LOCKED (pre-run):** D1 scale-separation L_wid/L_loc→0 (slope c_l/c_s=2) ⟺ two-scale;
  D2 invariant c_l/c_ω=−2/3 vs −1; resolution guard → INCONCLUSIVE below ~8 grid pts, never "merged".

- **Honest stop.** The residual is ONE-scale; HQW25's two-scale ansatz (moving frame + c_s) is NOT yet
  built, so Ω₂ isn't a residual-null here yet. That two-scale residual + its Ω₂ gate is the next brick,
  THEN a locked predicate + the logged a-sweep. Validated tooling, not the ticket. Clay odds ~0.05%.

## Phase-2 P2 — B1 LOGGED: CHL Scenario 2 reproduced via the modified rescaling (4.1)/(4.2) — 2026-07-26

**LOGGED gate run** (predicate LOCKED in git before the run, commit b5294ff). Data:
committed `writeup/data/p2_scenario2_relax.json`; harness `experiments/p2_scenario2_relax.py --logged`;
full write-up `PHASE2_P2_NOTES.md` §8. Verdict **5/5 PARTIAL by construction** — Tier-2, NOT novel,
NOT a proof.

What a human would want to know:

- **What we built.** `RescaledHLScenario2` (solver/hl_rescaled.py) = CHL's modified formulation
  (4.1) (spatial-shift DOF `c_r`, evolve `V:=Θ_X`) with the origin-pinned 3-constant normalization
  (4.2): a hand-rolled 3×3 solve each step (`_solve_3x3`, no scipy) for `(c_l,c_ω,c_r)` that pins
  `∂_τΩ(0)=∂_τΩ_X(0)=∂_τV(0)=0`. Origin-clustered grid with X=0 a node. Tests 9/9 — the new gauge
  nulls those three origin time-derivatives to 4.4e-16 (known-answer).

- **Why B1 was the right brick (the user's steer: only if it helps the real direction).** The §6/§7
  degenerate gauge pins stagnation at X=1 and (measured, §7) can't HOLD a profile peaked away from
  X=1. CHL's origin-pinned (4.2) gauge can — and it's exactly the machinery a future gCLM
  two-scale↔two-stage sweep needs to hold regular profiles. B1 = "the gCLM-ready gauge, VALIDATED",
  not a trophy. Said out loud in §8 + to the user.

- **Result.** Two distinct non-symmetric positive ICs both relax to the amplitude-INVARIANT
  contraction exponent `c_l/c_ω = −2.533 / −2.535` (CHL Fig 4.2: −2.5114, ~0.9%) — a genuine
  IC-independent attractor to a regular strictly-positive profile (min Ω>0, smoothness 0.73 vs ≈1061
  for the singular anchor). Residual falls 15→2.2e-2 (≈680×).

- **The honest ceiling (S5, a PASS because it's the predicted boundary).** The residual FLOORS at
  ~2e-2 (does NOT reach CHL's 1e-6 — fixed grid vs their adaptive mesh) and the ABSOLUTE triple
  drifts to (1.59,−0.63,0.21), off CHL's raw (1.0636,−0.4235,0.0765) — the absolute constants are
  IC-normalization-dependent; only the ratio + shape are gauge-invariant. Adaptive dt (recompute CFL
  as the initial c_l=13 transient decays) was needed to reach τ≈42 in 14k steps.

- **Where this leaves us.** BOTH CHL scenarios now reproduced (§2 singular Stage-2 anchor + §8
  regular Scenario-2 exponent). Tier-2 consolidation. The lottery ticket still lives elsewhere: the
  gCLM two-scale↔two-stage transition (now has the validated origin-pinned gauge to build on) or a
  rigor step on Conjecture 2.4.

## Phase-2 P2 — SCOUT (non-logged): the "generic" state is CHL's regular Stage-1 profile; B1/B2 scoped — 2026-07-25

**NOT a logged gate run** — an exploratory characterization + literature scout, no pre-committed
predicate, no new solver code (used `RescaledHLDynamic` as-is). Recorded here because it upgrades the
prior entry's main caveat and decided the fork direction. Evidence:
`writeup/p2_regular_profile_evidence.py` → `fig14` from committed `writeup/data/p2_regular_profile.json`
(+ `..._traj.json`). Full write-up: `PHASE2_P2_NOTES.md` §7, `TECHNICAL_P2_CONJ24.md` §7.

What a human would want to know:

- **The reframe.** CHL's rescaled HL system has TWO fixed points: the singular Stage-2 anchor
  `(2,-1)` AND a regular, strictly-positive Stage-1 profile (their Scenario 2, §4). The prior logged
  run's "generic degenerate IC → a DIFFERENT state (0.680,-0.487), honest predicted NEGATIVE" is
  **not** a POC artifact — characterizing that final field shows it is smooth (`max|Ω_X|/peak≈0.3`
  vs `≈1061` for the singular anchor), single-signed, peaked at `X≈0.35` away from `X=1`. That is
  qualitatively CHL's Stage-1 regular profile. Our machinery reaches BOTH CHL attractors.

- **Why it matters / the honest guards.** This is a QUALITATIVE match (regular, +ve, peak off `X=1`),
  reached with the STANDARD `(2.4)`+degenerate gauge — NOT CHL's modified Scenario-2 formulation
  `(2.9)/(4.1)`. So NOT a proven identity; constants differ under the different normalization (ours
  `c_l≈0.5, c_ω≈−0.45`; theirs `(c_l,c_ω,c_r)=(1.0636,−0.4235,0.0765)`). Not novel, not a proof.

- **The B1/B2 scout (8000-step trajectory).** Under our gauge the generic trajectory TRANSITS the
  CHL-S2 neighborhood (`c_l≈1.06` near step 1200 — nearly the published value) but CANNOT hold it,
  then wanders in the low-`c_l` regular regime and NEVER approaches `c_l=2`. Diagnosis: our gauge
  pins `c_l=−U(1)` (stagnation at `X=1`), a mismatch for a profile peaked at `X≈0.35`; CHL's `(4.2)`
  pins at the ORIGIN. Decision: **B1 (implement `(4.1)/(4.2)`) is the recommended next brick** —
  cheap (`+c_r` in transport, a 3×3 gauge solve), with a clean KNOWN-ANSWER `(1.0636,−0.4235,0.0765)`
  we already fly within `~0.005` of. **B2 (the Stage-1→Stage-2 transition) is NOT reachable on a
  fixed grid** and mostly re-confirms CHL — wrong brick now. Lottery ticket still lives elsewhere
  (gCLM-family two-scale↔two-stage transition; or a rigor step).

## Phase-2 P2 — dynamic relaxation: Conjecture 2.4 (CHL) at POC, LOCAL attractor confirmed — 2026-07-25

Full record: writeup/TECHNICAL_P2_CONJ24.md + BLOG_P2_CONJ24.md; evidence fig13 from committed
writeup/data/p2_conj24_relax.json (`python writeup/p2_conj24_evidence.py`). Logged harness
experiments/p2_conj24_relax.py --logged (predicate LOGGED to git before the run). Machinery
solver/hl_rescaled.py::RescaledHLDynamic + test_hl_rescaled.py (7/7). This IS a logged gate run.

**Verdict: PARTIAL (by construction) — 9/9 pre-committed clauses hold.** The first genuine swing
of the lottery-ticket leg. It reproduces the LOCAL content of a numerical-only conjecture — Tier-2
independent confirmation, NOT novel, NOT a proof.

The chosen path this session (with the user): *scout HH23 first, then build+validate the stepper,
then reassess.* The HH23 scout (JOURNAL not needed — it's a read, banked in PHASE2_P2_NOTES.md §5)
returned NO-GO on the literal 3D link (mechanism + geometry mismatch; would overclaim) but surfaced
the real 1D-tractable question (two-scale vs two-stage). Then this run.

What a human would want to know:

- **The novel piece is the degenerate GAUGE, and it works.** CHH22 pins the origin slope
  Omega_x(0), which is exactly 0 for degenerate data. CHL (their (3.2)) instead read the NONLOCAL
  U_X(0)=H(Omega)(0) (nonzero even when the slope vanishes) + pin c_l=-U(1). Implemented and
  validated as a KNOWN-ANSWER test on the proven Thm-2.3 anchor: (c_l,c_omega)=(1.949,-0.969)≈(2,-1).
  A clean identity makes it a real test: at the anchor Theta_X-(U+c_l X)Omega_X = Omega_bar and
  H(Omega_bar)(0)=-1 exactly (the delta at X=1 cancels analytically).

- **Hit a real numerical wall and diagnosed it (didn't hand-wave).** The naive SSPRK3+upwind+spline
  scheme is UNSTABLE at the singular profile: starting AT the regularized anchor the residual grows
  25→3e3→1e9 and blows up by tau~1.4. Cause: non-dissipative spline slopes ring at the X=1
  discontinuity; the stiff Theta_X delta-source amplifies it. Same class of difficulty that drove
  CHL to adaptive mesh + WENO. Fix = subgrid dissipation nu*d²/ds² — a POC crutch (O(nu) bias), NOT
  their industrial solution, but enough to ask the question.

- **Locked the predicate BEFORE the logged run; 9/9 held; did NOT tune to pass.** Gauge-invariant
  only, declared PARTIAL by construction. Result (n=801, nu=0.02, 2500 steps):
  - anchor HOLD → (1.939,-0.927), residual 180→3.4 plateau (a stable hold, explicitly NOT →0),
    shape rel-L2 4.9%.
  - two perturbations → the SAME fixed point (within 0.06 in both constants), residual drop >5×:
    the LOCAL asymptotic stability CHL only asserted.
  - nu=0.04 → (1.936,-0.925), unchanged: the fixed point is robust to the stabilizer, not a
    nu-artifact; the residual floor scales with nu (controllable, not a wall).
  - generic far degenerate IC → (0.680,-0.487): it relaxes to a DIFFERENT self-similar state (low
    residual, wrong constants, 29% shape). The honest predicted NEGATIVE — the GLOBAL basin is
    beyond a fixed-grid POC. (Note the nuance: generic data doesn't blow up, it converges ELSEWHERE.)

- **NOT achieved (on purpose, stated out loud):** residual→0 (POC dissipation floor) and the global
  basin. Both need WENO/adaptive mesh + vanishing-viscosity + a semi-analytic X^{-1/2} outer patch
  (the same tail fix flagged for Spike-1 Step C). The genuinely-new leg (two-scale vs two-stage,
  §5) needs exactly those global-basin numerics — hence the reassessment point.

## Phase-2 P2 — the 1D Hou–Luo singular-profile machine, validated against an exact solution — 2026-07-25

Full record: writeup/TECHNICAL_P2_HL_ANCHOR.md + BLOG_P2_HL_ANCHOR.md; evidence fig12 from
committed writeup/data/p2_hl_anchor.json (`python writeup/p2_hl_anchor_evidence.py`). Working
doc PHASE2_P2_NOTES.md. Code solver/hl_rescaled.py + test_hl_rescaled.py (5/5). This is solver
dev + unit validation, NOT a logged gate run.

**What this is: VALIDATION of a proven result — machinery, not novelty, not a proof.** After
Spike 1 we scoped P2 = the actual novelty frontier, and decided (with the user, from evidence)
to attack the **1D Hou–Luo model** singular-profile scenario of Chen–Huang–Li (arXiv:2604.01868),
NOT 2D Boussinesq.

What a human would want to know:

- **Scouted before committing.** Read CHL page-by-page: the novel thing is *degenerate* data
  → *singular* self-similar profiles (two-stage L^∞→L^p), and only *weak existence* of one
  explicit profile is proven — the asymptotic *stability* is numerical-only. That gap is the
  frontier. Chose 1D over 2D because the novelty lives there first, it reuses line_hilbert +
  gCLM rescaling, and 2D would compound the Step-C tail problem.

- **A feasibility probe made the decision on evidence, not vibes.** Fed the singular profile
  Ω̄=(X−1)^{−1/2} to our line-Hilbert operator and compared to the exact H I derived. The
  operator SURVIVES: the singular core is representable to a few % and improving; the only real
  error is the slow X^{−1/2} tail, and it is TRUNCATION-limited (falls with domain reach M,
  immune to node clustering — measured, not asserted). Not a wall; the known outer-patch gap.

- **Derived a closed-form velocity for their profile.** From the classical Hilbert pair
  H(x₊^{−1/2})=−(−x)₊^{−1/2}: H(Ω̄)=−(1−X)^{−1/2}1_{X<1}, U̅=2√(1−X)−2 (X<1), −2 (X≥1). Three
  independent checks line up (U̅(0)=0; U̅(1⁻)=−2 = strong steady form; c̄_l+2c̄_ω=0 exactly). A
  small self-contained by-product the paper didn't spell out — and the known answer that makes
  the validation a real known-answer test (the Spike-0 discipline).

- **Five known-answer checks pass** (test_hl_rescaled.py): velocity operator vs arctan(2X)
  1.1e−5; full pipeline 1.8e−3; velocity on the singular anchor → U̅ converging at the ½-order
  the √-singularity predicts; steady residual of the exact profile 6.2e−3 converging; Θ
  consistency exactly 0.

- **Performance (the user asked).** Bottleneck was the shared line_hilbert.py build, not P2 code:
  batched Thomas slope solve (_slope_matrix 6.15s→0.29s, 21×), Horner+shared+shortened L(s)
  series (n=4001 build 65s→19.7s, 3.3×), lazy Hilbert matrix. HL suite >120s→3.9s. Accuracy
  IDENTICAL — line_hilbert 6/6, gclm 5/5, hl 5/5 all green (verified the operator change didn't
  move a single error digit).

- **NOT done (on purpose):** the dynamic relaxation + degenerate normalization — the actual
  novelty swing (does generic degenerate data converge to the singular profile?). That is a
  logged run with a pre-locked predicate; paused here at the user's request to bank the anchor.

## Spike 1 Step C — relax to the Chen–Hou profile (the gate): PARTIAL, honestly reported — 2026-07-25

Full record: writeup/TECHNICAL_SPIKE1_STEPC.md + BLOG_SPIKE1_STEPC.md; evidence fig11 from
committed writeup/data/spike1_stepC_gate.json (`python writeup/spike1_stepC_evidence.py`).
Harness experiments/spike1_stepC_gate.py (predicate LOGGED to git before the run, commit
eabb418). This IS the logged gate run.

**Verdict: PARTIAL — 3 of 4 pre-committed checks pass, the far-field exponent check FAILS. Does
NOT pass the gate. Goalposts NOT moved.**

What a human would want to know:

- **The pre-committed predicate did its job.** We locked the pass/fail bar (alpha within 5%,
  far-field exponent within 10%, anisotropy <0.23, resolution-stable) in git *before* the run.
  It came back PARTIAL and we report PARTIAL — the whole point of WIN_CONDITION.

- **Found a bug, diagnosed it properly, fixed it.** First runs drifted: gauge-invariant alpha
  settled right (~-0.35) but c_l,c_om drifted individually and the run destabilized (~step 8000).
  Rather than hand-wave, we MEASURED the drift rate vs grid (experiments/diagnose_stepC_drift.py):
  it ~halves under n_r refinement and worsens as r_min shrinks -> a NEAR-ORIGIN TRUNCATION
  artifact, not a broken method. Fix: renorm=True re-pins omega_x(0),eta_x(0) each step (discrete
  enforcement of the paper's (2.12)); drift arrested, run stable. Standard dynamic-rescaling move,
  rediscovered by watching what breaks without it. test_renorm_pins_gauge added.

- **The good half (checks 1,3,4 PASS).** c_omega matches Chen–Hou to <0.5% across all configs
  (-1.026..-1.031 vs -1.0294) — and c_omega is the REAL result (it evolves via u_x(0) to the
  profile value while c_l is pinned to the gauge). alpha ~ -0.335 (2%), resolution-stable.
  Anisotropy ~0.026 << 0.23 — the profile's strong x/y anisotropy (2.24) reproduced.

- **The failing half (check 2 FAIL), stated straight.** The directly-fitted far-field exponent
  is ~-0.31 (7-13% off -0.342) and moves the WRONG way with n_r. Honest causes: (i) a PROTOCOL
  confound — fixed 2500 steps means higher-n_r runs reach smaller tau (under-relaxed; the slow
  r^{-1/3} tail forms last); (ii) POC limits — domain 1e5-1e6 vs the paper's 1e15, outer BC
  steepens the tail, no semi-analytic r^alpha split, 2nd-3rd order vs 6th-8th B-splines. A clean
  tail match needs the paper's apparatus. Did NOT re-run longer to chase a pass (that would be
  goalpost-moving); flagged fixed-tau protocol as future work.

- **Honest framing.** Even a clean pass reproduces a PROVEN result (Chen–Hou 2022) on a toy model
  across Wall C — validates machinery, NOT novel, NOT a proof. Clay ~0.05%. This is Tier-1/2: the
  machine captures the profile's core (invariants + anisotropy) with its POC limits located.

- **Next (the actual lottery ticket, P2).** Spike 1 has validated the stretched-grid dynamic-
  rescaling machinery end-to-end. The interesting move is to point it at a profile NOT already in
  a theorem (stable-vs-singular target: Chen–Huang–Li arXiv:2604.01868 in Papers/; or 3D-axisym).
  Deferred post-Spike-1 forks now actionable with the working machine.

## Spike 1 Step B — rescaled 2D Boussinesq RHS + modulation + SSPRK3, ASSEMBLED & VALIDATED — 2026-07-24

Full record: PHASE2_SPIKE1_NOTES.md §3 ("STEP B COMPLETE"). Code: `solver/boussinesq_rescaled.py`.
Suites: `test_boussinesq_transport.py` (5/5) + `test_boussinesq_rescaled.py` (7/7). NOT a logged
gate run — solver development validated piece-by-piece against manufactured known answers. The
scientific gate (does the steady state = the Chen–Hou profile?) is Step C, still to run.

What a human would want to know:

- **Grounded, then a fork the user made me EARN with data.** Transcribed the exact rescaled
  system (2.10)/(2.28), normalization (2.11)/(2.12), and — the payoff of re-reading Part I —
  the *precise* gate constants (2.23): c̄_l≈3.006499, c̄_ω≈−1.029425, ū_x(0)≈−2.532674, ratio
  ≈−2.92056, α≈−0.3424 (sharper than the round −2.92/−1/3 I'd been carrying). Also learned the
  paper evolves the *derivatives* (ω, η=θ_x, ξ=θ_y), not primitive (ω,θ).

- **The formulation decision, settled empirically (user asked "are there tests?").**
  `experiments/spike1_stepB_decide_formulation.py`: reading θ_xx(0) off primitive θ is an r²-curvature of two
  even modes, and the cos2β mode carries only (θ_xx−θ_yy) — contaminated by θ_yy. Measured **~2×
  worse and ~2× more noise-sensitive** than reading θ_xx(0)=η_x(0) as a clean *linear r-slope* of
  η's single odd cosβ mode. Ruled out primitive-θ. User chose the **full 3-field (ω,η,ξ)** (keep
  the v_x·ξ coupling) so the fixed point is *exactly* the Chen–Hou profile — a faithful gate.

- **The angular bases finally pinned down.** The sine basis was ONLY for φ (zero on both walls).
  The transported fields: ω,η odd-in-x → {cosβ,cos3β,…} (zero at axis, free at wall); θ,ξ
  even-in-x → {1,cos2β,…}. Transport uses β finite differences (basis-agnostic), so it didn't
  care; the origin reads and parities do.

- **The elegant confirmation.** c_l = 2η_x(0)/ω_x(0) is a RATIO of two same-basis slope reads, so
  the projection's quadrature bias **cancels**: c_l recovered to ~3e-16 in the test even though
  each slope alone carries ~2e-5. The thing the whole scheme's stability hinges on is the
  best-conditioned quantity in it.

- **Built de-risked, crux-first (Step-A discipline).** Piece 1 transport kernel (2D upwind on the
  curved log grid, the Spike-0 3rd-order Shu stencil generalized): manufactured rel err ~9.5e-6,
  order ~2.98, rigid-rotation→0 exact, far-field CFL cure carries to 2D. Pieces 2–4: grad_xy
  (order ~1.97), origin reads, modulation, then the coupled SSPRK3 integrator — RHS wiring locked
  by a term-by-term re-assembly test, and the whole machine steps stably (finite c_l,c_ω).

- **Honest status.** This is the MACHINE, validated to run. It is NOT yet shown to reproduce the
  profile — the smoke-test c_l≈1.06 is an arbitrary-blob transient, not a relaxation. And per the
  standing steer, even a flawless Step C reproduces a PROVEN result across Wall C: validates
  machinery, not novel, not a proof. Clay odds ~0.05%; the lottery ticket is post-Spike-1.

- **Next: Step C (the gate, a LOGGED run).** Needs (i) an initial guess in the profile's basin
  and (ii) a pre-committed pass/fail predicate (c_l,c_ω,ratio,α + shape, resolution-stable) fixed
  BEFORE the run. Both are genuine decisions — check in with the user first. Watch the r_min
  inflow inner-BC for domain/resolution sensitivity (flagged, not yet stressed).

## Spike 1 Step A — 2D Boussinesq velocity operator on a stretched grid, VALIDATED — 2026-07-24

Full record: PHASE2_SPIKE1_NOTES.md; technical writeup/TECHNICAL_SPIKE1_VELOCITY.md; blog
writeup/BLOG_SPIKE1_STEPA.md. Code: `solver/boussinesq_velocity.py`,
`test_boussinesq_velocity.py` (5/5 pass). NOT a logged gate run — solver development
validated against a manufactured known answer. Evidence figure fig9 + committed data
rebuild: `python writeup/spike1_stepA_evidence.py`.

User chose Spike 1 (2D Boussinesq port), **de-risked variant**: build + validate the
highest-risk new piece (the 2D velocity operator `u = ∇^⊥(−Δ)⁻¹ω`) standalone before
wiring the full rescaled solver. Step A is that piece — the 2D analogue of Spike-0's
non-FFT line Hilbert (on the uniform grid it's a trivial FFT; the real profile's slow
`r^{−1/3}` tail forces a stretched grid where FFT can't go).

What a human would want to know:

- **Grounded first, not reinvented.** Pulled Chen–Hou Part I (arXiv:2210.07191) + the MMS
  rigorous-numerics paper (2305.05660) into `Papers/` (gitignored) and transcribed the
  formulation exactly: physical (2.3)–(2.5), one-scale dynamic rescaling (2.10), modulation
  (2.11), half-plane Poisson velocity with `φ=0` on the wall, far-field `ω~r^α`,
  `α=c_ω/c_l≈−1/3`, gate target `c_l/c_ω≈−2.92`. WebFetch couldn't ingest the papers (size
  limit) — the user downloaded the PDFs; `Read` handles them page-by-page.

- **Correction banked:** the "two-scale rescaling" worry in the planning notes was from
  Chen–Hou's *earlier C^{1,α}-boundary* paper, NOT this smooth-data profile, which is
  **one-scale**. So Spike-0's one-scale-is-attracting headline is the relevant precedent.

- **The elegant win.** On a **log-radial** grid (`r=e^ρ`) with the Dirichlet **angular
  sine** basis `sin(2nβ)`, the polar Laplacian's `1/r`, `1/r²` terms cancel and `−Δφ=ω`
  decouples per mode into a constant-coefficient tridiagonal ODE
  `φ_n''(ρ) − (2n)²φ_n = −r²ω_n` — one Thomas solve per mode, no scipy sparse. The
  `r^{±2n}` homogeneous tails carry origin-regularity + far-field decay (the `r^{−1/3}`
  lever at POC level).

- **Validation (manufactured known answer, the house rule).** `φ*=r²e^{−r}sin2β +
  r⁴e^{−r}sin4β` → recover `u,v` to rel L∞ **~6e-5**, radial convergence order **2.00**
  (clean log-log line, not a lucky grid), and the modulation origin read **`u_x(0)=−2.0008`**
  vs −2 (that steering signal was a noise-amplifier in 1D recon; the angular-mode structure
  makes it clean here).

- **Honest POC scope (stated explicitly, flagged to user).** Chen–Hou's full apparatus
  (6th–8th-order B-spline FEM Poisson, adaptive mesh to `10¹⁵`, semi-analytic far-field
  split, `10⁻⁷` residual, INTLAB interval bounds) is months-scale and mostly built for the
  *proof*. The plan pre-committed Spike 1 to qualitative fidelity, so Step A uses a
  tractable **validated** Poisson solve (legitimate: an elliptic solve is textbook, unlike
  the exotic 1D line Hilbert) with the same mathematics. Reproduces a proven result across
  Wall C — validates machinery, NOT novel, NOT a proof.

- **Next:** Step B (rescaled RHS `(c_l x+u)·∇` + buoyancy `θ_x` + modulation, SSPRK in τ,
  with the `ζ=θ/x` substitution), then Step C (relax to the Chen–Hou profile — the gate).
  The stable-vs-singular target fork the user raised stays deferred to the post-Spike-1
  gate, when the working machine can probe both.

## Spike 0 COMPLETE — dynamic rescaling POC recovers the CLM profile + rate against the known answer — 2026-07-24

Full record: PHASE2_SPIKE0_NOTES.md ("SPIKE 0 COMPLETE" section). Code:
`solver/gclm_rescaled.py`, `test_gclm_rescaled.py` (5/5 pass, ~48s). NOT a logged gate
run — solver development validated against a closed-form known answer.

The dynamic self-similar rescaling technique is validated end-to-end in 1D. On a
sinh-stretched whole-line grid, CLM (a=0) dynamic rescaling recovers the exact profile
Ω̄₀=−4X/(1+4X²) to shape error ~2e-6 with the exact self-similar rate c_ω→−1, and it is
resolution-stable. This de-risks the whole method before the 2D port (Spike 1).

What a human would want to know:

- **The headline finding overturns recon finding-3.** The recon feared one-scale
  rescaling was unstable (the profile overshot and blew up in the rescaled frame → the
  Chen–Hou two-scale motivation). That instability was an **artifact of the wrong
  (periodic) Hilbert transform + integral modulation**, NOT fundamental. With the correct
  LINE Hilbert transform and value-based normalization (c_ω=1−HΩ(0), c_l≡1), Ω̄₀ is a
  clean **attractor**: two different perturbed odd ICs (Gaussian, narrower Lorentzian)
  both relax to it. One-scale suffices for CLM. (Whether Boussinesq/De Gregorio re-needs
  two-scale is a Spike-1 question — different mechanism.)

- **The scheme, reduced for CLM:** evolve f=Ω/X in the computational coordinate ρ
  (X=c·sinh ρ); the dilation becomes tanh(ρ)·f_ρ (speed ≤1 → CFL ~ Δρ independent of the
  reach M — the uniform-grid CFL death is cured). 3rd-order upwind (smooth profile → the
  paper's nonlinear WENO limiter is overkill at POC; outflow at both ends means upwind
  stencils reach inward, no ghosts) + SSPRK3. The origin slope f(0)=−4 is frozen to
  machine precision by the scheme itself (advection speed and source both vanish at ρ=0).

- **Honest scope, stated plainly:** this reproduces a *proven closed-form* toy result
  across Wall C — it validates machinery, it is NOT novel and NOT a proof. I deliberately
  did NOT claim the physical T*=2 from the whole-line run: T* belongs to the global
  periodic solve (already covered by test_solver_clm.py); a whole-line rescaling's initial
  amplitude is a free gauge, so its correct analogue is the *rate* c_ω→−1 (⟺ ω~(T−t)⁻¹),
  which it nails. The log-kernel velocity U was correctly deferred (CLM doesn't use it).

- **Gate reached (each spike STOPS for review, per PHASE2_NUMERICS_PLAN.md).** Technique
  de-risked in 1D. Forward decision = Spike 1 (2D Boussinesq port, the real multi-week
  lift) vs. first exercising a≠0 / De-Gregorio singular-profile targets in 1D (which need
  the deferred velocity U + AMR). Raised to the user as a scope decision.

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
