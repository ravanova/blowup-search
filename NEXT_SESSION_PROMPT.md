# Continuation prompt (paste into a new Claude Code session)

*Copy everything in the fenced block below as the first message of a fresh
session in this repo. It orients the model and points it at the decided next
action (Route A Phase 1, Gate 3 — the 2D genome + MAP-Elites, on smooth data
with a resolution-stable growth-based fitness; then the non-negotiable Gate 4
viability gate).*

```
Continue the Navier–Stokes blow-up search project in this directory
(/home/andy/projects/Unsolved). The goal is a genuine, honest attempt at the
Clay Millennium problem via evolutionary search over initial conditions — while
never fooling ourselves with a numerical artifact. WIN_CONDITION.md is the
anti-self-deception contract: only Tier 3 (a rigorous proof) solves it; Tier 1
(candidate) and Tier 2 (resolution-confirmed) are progress. Preserve that
honesty — do not oversell. When a genuine scope decision arises, raise it for
review rather than deciding unilaterally.

Orientation (read in this order): PROJECT.md, WIN_CONDITION.md, CLAY_ROADMAP.md
(Route A), PHASE1_PLAN.md (the Phase-1 gate contract), PHASE1_SPIKE_RESULTS.md
(the resolution de-risk verdict — READ THIS, it recalibrates the deliverable),
writeup/SUMMARY.md, then experiments/JOURNAL.md (newest entries first) and
LOGGING.md.

State — Route A Phase 1 (2D Boussinesq, Hou–Luo geometry). Both scope decisions
(commit to Phase 1; Hou–Luo symmetry-wall geometry) were confirmed with the user.
All banked + reproducible; commits d4de0dd..3244940 are LOCAL (confirm whether to
push to github.com/ravanova/blowup-search — push only when the user asks):
- DONE Gate 1a — solver/boussinesq.py: doubly-periodic 2D Boussinesq
  pseudo-spectral solver (the gCLM method lifted to 2D: fft2, RK4,
  integrating-factor viscosity, 2/3 dealiasing, advective CFL), same result
  contract + theta_final; nu/kappa + artifact guards first-class. Validated by an
  exact analytic ladder, test_solver_boussinesq.py 6/6 at machine precision
  (Biot–Savart, RHS incl. buoyancy th_x, transport, viscous decay, Taylor–Green,
  conservation).
- DONE Gate 1b — the Hou–Luo no-flow wall via parity (w odd-x/odd-y, th
  even-x/odd-y → v vanishes on the walls), an effective [0,pi]^2 box with the
  singular corner at the origin. test_boussinesq_wall.py 4/4: wall BC 8e-17,
  parity a GENUINE invariant of the dynamics (9e-15 unenforced), buoyancy
  amplifies 30x with parity/conservation intact. solve_boussinesq(symmetry=
  "houluo") holds the wall exactly on long runs.
- DONE Gate 2 — ported the Phase-0 method. ga/genome2d.py: 2D rough-data
  representation (separable Holder product; y=pi/2 slice is exactly the 1D
  profile), test_genome_rough_2d.py 7/7. The fine-N exponent measurement is the
  same model-agnostic win_condition.estimate_blowup_time; validated on controls,
  test_phase1_measurement.py 3/3 (synthetic (T*-t)^-a inverted exactly; 2D Euler
  correctly refused Tier-2 — the anti-self-deception property, in 2D).
- DONE resolution de-risk spike (reordered before Gate 3, to test the DOMINANT
  risk cheaply first). Solver gained tail_guard (stop "under_resolved" when
  enstrophy piles near the dealias cut — the RIGHT under-resolution signal;
  conservation drift stays tiny under-resolution, so it is the WRONG signal).
  phase1_resolution_spike.py + analyze_phase1_spike.py, pre-committed gate.
  VERDICT STABLE (PHASE1_SPIKE_RESULTS.md): the fixed-window log-growth-rate
  fitness g CONVERGES across N=128→1024 for smooth growers (smooth_sharp g→0.609,
  smooth_mild g→1.239) → a resolution-stable SEARCH signal exists.

CRUCIAL recalibration from the spike (do not lose this — it is the honest scope):
1. The blow-up EXPONENT/T* RAILS across N (a 2.45→1.20). A uniform grid never
   reaches T* (Luo–Hou needed AMR to ~1e12). So uniform-grid Tier-2 CONFIRMATION
   of the true Hou–Luo singularity is OUT OF REACH. Near-term Phase-1 deliverable
   is a resolution-stable shape→growth QD map with Tier-1 candidates, NOT
   Tier-2-confirmed singularities. Tier-2/Tier-3 needs AMR or Route D.
2. Rough C^{0,alpha} data is under-resolved from t≈0 (t_res 0.03–0.07 at all N).
   The rough-data genome axis is resolution-STARVED on uniform grids — proceed on
   SMOOTH data; drop or explicitly scope out the rough axis (ga/genome2d.py stays
   but is deprioritised).
3. amp_res grows with N (resolved window extends) so it is NOT a stable fitness;
   the windowed growth rate g IS. But g is resolution-stable yet not automatically
   blow-up-PREDICTIVE (smooth_mild has higher early g yet saturates; smooth_sharp
   lower g yet blows up). A nu_crit-analog (critical viscosity suppressing the
   resolved-window growth) is the prime fitness candidate — resolution-stable AND
   plausibly blow-up-predictive, mirroring the gCLM fitness that worked.

YOUR TASK — Gate 3, then the non-negotiable Gate 4. Same "two unknowns never
debugged at once" discipline; STOP for review at each gate.
1. FIRST raise the fitness-axis decision (nu_crit-analog vs a windowed
   growth-rate vs other), informed by recalibration point 3 — it shapes the whole
   viability gate. Get the user's pick.
2. Gate 3 — a 2D genome over SMOOTH Hou–Luo-subspace fields (parities enforced;
   an energy-budget-normalised Fourier/mode representation, the 2D analog of
   ga/genome.py). Reuse the whole harness conceptually: MAP-Elites, budget-matched
   acceptance, win-condition tiers, resolution study, single-writer logging.
   Wire the chosen fitness through the 2D solver with the tail_guard so the
   fitness only ever reads TRUSTED (resolved) dynamics.
3. Gate 4 — NON-NEGOTIABLE: re-run the six-property viability gate on the new
   Boussinesq fitness BEFORE any GA compute. The spike already cleared the
   dominant resolution-stability property for the growth proxy; Gate 4 must
   confirm the other five, ESPECIALLY that the axis tracks blow-up PROPENSITY
   (not transient early growth). Commit to a full GA campaign only if all six
   pass. If it rails like gCLM's non-genericity axis did, STOP — a finding, not a
   push-harder signal (Stages 2.5/3.5/3.6 are why).
4. On a Tier-1 novel candidate: open Route D (validated-numerics / a domain-expert
   collaboration) for the actual Tier-2/Tier-3 confirmation the uniform grid
   cannot give.

Environment & workflow: .venv/bin/python (numpy + matplotlib), 12 cores — ~8–10
workers, OMP_NUM_THREADS=1 pinned. 2D runs are SLOW (a smooth grower to
under-resolution is seconds at N=256 but ~30–40 min at N=1024 — size compute
accordingly; the tail_guard bounds most runs to seconds). No pytest; run each
suite as `python test_X.py`. The required pre-run suite set is now TEN
(test_win_condition, test_solver_clm, test_logbook, test_ga,
test_resolution_study, test_genome_rough, test_solver_boussinesq,
test_boussinesq_wall, test_genome_rough_2d, test_phase1_measurement); the four
Phase-1/2D suites are solver-heavy, so run the full gate with a longer timeout.
Before ANY logged run verify the suites pass and COMMIT (the dirty-tree guard
refuses uncommitted .py by design; gitignored experiments/*.jsonl + *.out are
fine). One JOURNAL.md entry per experiment. Curated writeup evidence rebuilds via
writeup/curate_evidence.py + build_figures.py (committed data only). Push to
origin only when the user asks. phase1_progress.py gives a CLI progress bar for
sweeps (--watch).

Honest framing to preserve: 2D Boussinesq is still a toy model, not 3D
Navier–Stokes; Tier 2 is not a proof; and per the spike, uniform-grid Tier-2 of
the TRUE Hou–Luo singularity is itself out of reach — the reachable near-term win
is a resolution-stable shape→growth QD map (Tier-1) in a provable-blow-up model,
with Tier-2/Tier-3 gated behind AMR or an expert collaborator (Route D). Overall
probability of solving Clay stays very low (~0.05%), capped by two structural
walls: a search can only argue FOR blow-up, and provable blow-up lives only in
simple models, not 3D NS.
```
