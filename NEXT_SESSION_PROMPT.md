# Continuation prompt (paste into a new Claude Code session)

*Copy everything in the fenced block below as the first message of a fresh
session in this repo. It orients the model and points it at the decided next
action (Stage 3.6 / Route A Phase 0).*

```
Continue the Navier–Stokes blow-up search project in this directory
(/home/andy/projects/Unsolved). The goal is a genuine, honest attempt at the
Clay Millennium problem via evolutionary search over initial conditions — while
never fooling ourselves with a numerical artifact. WIN_CONDITION.md is the
anti-self-deception contract: only Tier 3 (a rigorous proof) solves it; Tier 1
(candidate) and Tier 2 (resolution-confirmed) are progress. Preserve that
honesty in all framing — do not oversell.

Orientation (read in this order): PROJECT.md, WIN_CONDITION.md, CLAY_ROADMAP.md,
writeup/SUMMARY.md, PLAN.md (esp. Stage 3.5 and the new Stage 3.6),
NONGENERICITY_RESULTS.md, LOGGING.md. Then skim writeup/TECHNICAL_WRITEUP.md.

State of the work (all banked, reproducible, pushed to the private repo
github.com/ravanova/blowup-search):
- DONE — Stage 1 (validated pseudo-spectral gCLM solver), Stage 1.5 (fitness
  viability: nu_crit chosen), Stage 2/2.5/2.6 (GA harness; after two failed
  fitness axes, acceptance MET on nu_crit at a=0.7 — GA beats budget-matched
  random 3/3 seeds), Stage 3 (resolution study: 18/18 elites → Tier-2
  NUMERICALLY_CONFIRMED, but all generic alpha=1.000 — the CLM singularity
  surviving advection, NOT a novel De Gregorio-type blow-up).
- DONE — Stage 3.5 (non-genericity de-risking): the GA edge (a=0.7, generic,
  resolution-stable) and the novel non-generic (alpha!=1) target are DISJOINT on
  gCLM — non-genericity appears only near a=1 and only as a resolution artifact
  (15/40 well-def flips, alpha railing 3.0<->0.3). A gCLM non-genericity GA would
  optimize grid noise. See NONGENERICITY_RESULTS.md.

Decision (see the JOURNAL decision record + CLAY_ROADMAP.md): pursue Clay via
Route A (switch to a model where non-generic blow-up is PROVABLE — 2D Boussinesq
/ C^{1,alpha} De Gregorio), and do its Phase 0 first on the existing 1D solver.
Never debug a new solver and a new measurement at once: validate the measurement
on the substrate with known answers, then port it.

YOUR TASK — execute PLAN.md Stage 3.6 (Route A, Phase 0), then STOP for review.
Concretely, unless a fresh read changes your mind:
1. Add a genuine C^{1,alpha} rough-data genome mode to the genome
   representation (the k^{-p} envelope in ga/genome.py is only the seed; it
   reaches smooth/decaying shapes, not true limited-regularity Hölder profiles).
   Unit-test the intended regularity.
2. Build a fine-N non-generic-exponent measurement: extend nongenericity_sweep.py
   (or a sibling) to run rough-data shapes near a=1 at N in {1024, 2048, 4096},
   reusing win_condition + the conservation-drift guard, and report whether the
   fitted exponent alpha (or a self-similar-profile quality score) CONVERGES with
   resolution or RAILS at grid scale (the Stage 3.5 failure mode).
3. Apply the pre-committed gate (do NOT soften it mid-run):
   - alpha converges at N=2048/4096 -> surprise; gCLM not exhausted; a novel 1D
     candidate may be reachable -> STOP and re-plan before any 2D solver.
   - alpha still rails (expected) -> gCLM confirmed exhausted; the deliverable is
     the validated method + rough-data genome to carry into Phase 1 (2D
     Boussinesq). A Phase-0 negative is informative, NOT a kill-signal for
     Phase 1 (Boussinesq is a different mechanism).
   Hard ~2-day-equivalent time-box; no "try a few more shapes" third branch.
4. Write STAGE_3_6_RESULTS.md + a JOURNAL entry; update PLAN.md's Stage 3.6
   banner and PROJECT.md's index; commit; STOP for review.

Environment & workflow: .venv/bin/python (numpy + matplotlib installed), 12
cores — use ~10 workers, OMP_NUM_THREADS=1 pinned. No pytest; run each suite as
`python test_X.py`. Before ANY logged run, verify all five suites pass
(test_win_condition.py, test_solver_clm.py, test_logbook.py, test_ga.py,
test_resolution_study.py) and COMMIT — the dirty-tree guard refuses uncommitted
code by design (untracked non-.py files are fine). One JOURNAL.md entry per
experiment_id. Sweeps write to gitignored experiments/*.jsonl and do their own
dirty check. Push to origin (ravanova/blowup-search) when the user asks.

Honest framing to preserve: these are 1D toy models, not 3D Navier–Stokes;
Tier 2 is not a proof; the novel target is a resolution-STABLE non-generic
blow-up (which Stage 3.5 says gCLM likely can't provide — hence the planned
model switch). Overall probability of solving Clay stays very low (~0.05%,
capped by two structural walls: a search can only argue FOR blow-up, and
provable blow-up lives only in simple models, not 3D NS). The reachable win is a
novel Tier-2 (and, with an expert collaborator, Tier-3) candidate in a provable
model. If a step surfaces a genuine scope decision, raise it for review rather
than deciding unilaterally.
```
