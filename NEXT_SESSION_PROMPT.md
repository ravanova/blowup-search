# Continuation prompt (paste into a new Claude Code session)

*Copy everything in the fenced block below as the first message of a fresh
session in this repo. It orients the model and points it at the decided next
action (Route A, Phase 1 — a 2D Boussinesq model switch, which is a scope
decision to confirm with the user before building).*

```
Continue the Navier–Stokes blow-up search project in this directory
(/home/andy/projects/Unsolved). The goal is a genuine, honest attempt at the
Clay Millennium problem via evolutionary search over initial conditions — while
never fooling ourselves with a numerical artifact. WIN_CONDITION.md is the
anti-self-deception contract: only Tier 3 (a rigorous proof) solves it; Tier 1
(candidate) and Tier 2 (resolution-confirmed) are progress. Preserve that
honesty in all framing — do not oversell.

Orientation (read in this order): PROJECT.md, WIN_CONDITION.md, CLAY_ROADMAP.md
(esp. Route A, Phase 1), writeup/SUMMARY.md, PLAN.md (esp. the Stage 3.6 banner
and Stage 4), STAGE_3_6_RESULTS.md, NONGENERICITY_RESULTS.md, LOGGING.md. Then
skim writeup/TECHNICAL_WRITEUP.md (now includes §8, the Stage 3.6 result).

State of the work (all banked and reproducible; confirm the latest commits are
pushed to the private repo github.com/ravanova/blowup-search — the Stage 3.6
commits 95ef09f / f7d2976 / d4a7061 may be local-only):
- DONE — Stages 1–3: validated 1D pseudo-spectral gCLM solver; fitness-viability
  de-risking; QD (MAP-Elites) GA that beats budget-matched random 3/3 seeds on
  nu_crit at a=0.7; resolution study promoting 18/18 elites to Tier-2
  NUMERICALLY_CONFIRMED — but all generic (alpha=1.000, the CLM singularity
  surviving advection), NOT a novel De Gregorio-type blow-up.
- DONE — Stage 3.5 (non-genericity de-risking): the GA edge (a=0.7, generic,
  resolution-stable) and the novel non-generic (alpha!=1) target are DISJOINT on
  gCLM; non-genericity appears only near a=1 and only as a resolution artifact.
- DONE — Stage 3.6 (Route A, Phase 0: rough-data spike): built a genuine
  C^{1,alpha} rough-data genome mode (ga/genome.py holder_profile =
  sign(sin x)|sin x|^h, an odd C^{0,h} localized Hölder cusp; regularity
  unit-tested in test_genome_rough.py, 7/7) and a fine-N exponent measurement
  (stage3_6_sweep.py at N in {1024,2048,4096}; pre-committed gate
  analyze_stage3_6.py; live viewer stage3_6_progress.py). VERDICT: RAILS, the
  expected branch. The a=0.7 control validated the fine-N measurement (generic
  alpha~1, stable, 18/18 usable); near a=1 nothing converges — a=0.9 scatters
  (max cross-N span 1.95), a=0.95 rails (0.30<->3.00) and flips, a=1.0 is a dead
  axis (0/18 even for C^{0,0.2} data, which per WIN_CONDITION.md is NOT evidence
  of regularity). Max conservation_drift 1.9e-4 << the 1e-3 guard, so the rail is
  a genuine grid-scale property, not under-resolution. Full writeup
  STAGE_3_6_RESULTS.md; banked into writeup/ (fig5, data/stage3_6_rough.json).

Decision now settled by Stage 3.6: the cheap 1D route to a *novel*, non-generic
(Tier-3-provable) result is closed for smooth AND rough data. Per the
pre-committed gate and CLAY_ROADMAP.md, the pursuit continues via Route A,
Phase 1 — switch to a model where non-generic blow-up is actually provable (2D
Boussinesq, the "poor man's 3D Euler" in the Hou–Luo geometry; or a
rough-data-capable De Gregorio solver). A Phase-0 negative is informative, NOT a
kill-signal for Phase 1: Boussinesq blow-up is a different mechanism, and it is
where the literature's provable non-generic blow-ups (Elgindi–Jeong, Chen–Hou,
Buckmaster–Gómez-Serrano) live.

FIRST — this is a genuine scope escalation, so raise it for review before
building; do not start the solver unilaterally. Phase 1 is materially heavier
than anything so far (a new 2D spectral solver + a 2D genome — weeks, not the
~2-day Phase-0 spike), and the 1D pipeline + writeup is already a complete,
banked, defensible deliverable. Put the choice to the user explicitly:
  (a) commit to Route A Phase 1 (2D Boussinesq) — the only route with a shot at a
      novel Tier-2/Tier-3 result, but a multi-week build; or
  (b) treat the banked 1D pipeline + writeup as the terminal deliverable and stop.
Get an explicit decision. If (b): nothing more to build — help package / push /
present. If (a): proceed to the plan below.

YOUR TASK IF PHASE 1 IS APPROVED — build with the same "two unknowns never
debugged at once" discipline Phase 0 used, and STOP for review at each gate:
1. Stand up a 2D Boussinesq (or rough De Gregorio) spectral solver, validated
   FIRST against a known result (a published Boussinesq near-singular profile or
   an analytic/benchmark case) before it is ever trusted — the analog of Stage 1's
   CLM/diffusion/advection acceptance checks. Keep viscosity and the artifact
   guards (conservation / energy-balance drift) first-class from the start,
   exactly as solver/gclm.py does.
2. Port the transferable Phase-0 method: the rough-data representation principle
   (a 2D analog of holder_profile — genuine C^{1,alpha} data, unit-tested for its
   regularity) and the fine-N exponent / self-similar-quality measurement
   (validated on a known-answer control first, as the a=0.7 control did in 3.6).
3. Build a 2D genome data structure applying the rough-data principle. Reuse the
   WHOLE existing harness conceptually — MAP-Elites, budget-matched acceptance,
   the six-property viability gate, the win-condition tiers, the resolution study,
   single-writer logging (ga/*, win_condition.py, LOGGING.md).
4. NON-NEGOTIABLE GATE before any GA compute: re-run the six-property viability
   gate on the new Boussinesq fitness (Stages 2.5 / 3.5 / 3.6 are why). Commit to
   a full GA campaign ONLY if it passes all six. If it fails like gCLM's
   non-genericity axis did, STOP — do not run the GA; that is a finding, not a
   push-harder signal.
5. On a Tier-2 novel candidate in the provable model: open Route D
   (validated-numerics / a domain-expert collaboration) — the actual proof leg,
   out of scope for the search machinery.

Environment & workflow: .venv/bin/python (numpy + matplotlib installed), 12
cores — use ~10 workers, OMP_NUM_THREADS=1 pinned. No pytest; run each suite as
`python test_X.py`. Before ANY logged run, verify all SIX suites pass
(test_win_condition.py, test_solver_clm.py, test_logbook.py, test_ga.py,
test_resolution_study.py, test_genome_rough.py) and COMMIT — the dirty-tree
guard refuses uncommitted code by design (untracked non-.py files are fine). One
JOURNAL.md entry (experiments/JOURNAL.md) per experiment_id. Sweeps write to
gitignored experiments/*.jsonl and do their own dirty check. Curated writeup
evidence rebuilds via writeup/curate_evidence.py + writeup/build_figures.py
(committed data only; no re-runs). Push to origin (ravanova/blowup-search) when
the user asks.

Honest framing to preserve: these are toy models (1D so far; 2D Boussinesq next),
not 3D Navier–Stokes; Tier 2 is not a proof; the novel target is a
resolution-STABLE non-generic blow-up, which gCLM cannot provide (Stages
3.5–3.6) — hence the model switch. Overall probability of solving Clay stays very
low (~0.05%), capped by two structural walls: a search can only argue FOR
blow-up, and provable blow-up lives only in simple models, not 3D NS. The
reachable win is a novel Tier-2 (and, with an expert collaborator, Tier-3)
candidate in a provable model. If a step surfaces a genuine scope decision, raise
it for review rather than deciding unilaterally.
```
