# blowup-search

An honest, long-shot attempt at the **Navier–Stokes Existence and Smoothness**
Millennium Prize Problem — and, along the way, a set of reusable machinery for
anyone doing computer-assisted singularity research.

The project searches for **finite-time blow-up** in fluid models: first with
evolutionary (quality-diversity) search over initial data, and now with
**computer-assisted certification** of self-similar blow-up profiles. Every
claim in the repository is tiered, gated, and rebuildable from committed data.

> **Status, stated plainly.** 52 legs in, nothing here resolves the Clay
> problem, and the recorded probability that it ever will is **~0.05%**. The
> realistic prize is a *novel Tier-3 (rigorously certified) result on a model
> where blow-up is provable*. That is the target of record. See
> [The honest ceiling](#the-honest-ceiling).

---

## Contents

- [What the problem is, and which direction we attack](#what-the-problem-is-and-which-direction-we-attack)
- [The win condition (three tiers)](#the-win-condition-three-tiers)
- [The honest ceiling](#the-honest-ceiling)
- [Where the project is right now](#where-the-project-is-right-now)
- [Quick start](#quick-start)
- [Repository map](#repository-map)
- [What has been banked](#what-has-been-banked)
- [Reusable contributions](#reusable-contributions-what-to-steal-from-this-repo)
- [Working rules](#working-rules-if-you-contribute)
- [Reading order](#reading-order)

---

## What the problem is, and which direction we attack

The Clay problem asks us to either **(a)** prove smooth, finite-energy initial
data always yields a globally smooth solution of the 3D incompressible
Navier–Stokes equations, or **(b)** disprove it by exhibiting data whose
solution loses smoothness in finite time.

**This project pursues (b).** Direction (a) is a universal claim over an
infinite-dimensional space — nothing can be *searched* into existence. Direction
(b) is existential: one counterexample suffices, which is the kind of target a
fitness-driven search, and then a computer-assisted proof, can actually climb
toward. Rationale for choosing Navier–Stokes over the other five open
Millennium problems is in
[millennium_prize_problems.md](millennium_prize_problems.md); the original
framing is in [PROJECT.md](PROJECT.md).

The precedent is real: Hou, Luo and collaborators found near-singular 3D Euler
solutions numerically; Chen–Hou, Elgindi, Buckmaster–Gómez-Serrano and others
have since turned numerical candidates into **rigorous computer-assisted
proofs** for related equations. Steps (b) splits into: find a candidate profile,
then certify it.

## The win condition (three tiers)

The easiest way for a project like this to fool itself is to confuse "the
simulation looks like it is blowing up" with "we have solved the problem".
[WIN_CONDITION.md](WIN_CONDITION.md) defines three tiers, and only the third
counts:

| Tier | Name | What it takes | What it means |
|---|---|---|---|
| **1** | Candidate | `1/‖ω(t)‖_∞` fits a line with negative slope, forward zero-crossing `T*`, `R² ≥ 0.98` (the Beale–Kato–Majda proxy) | Cheap to produce by accident. A candidate, nothing more. |
| **2** | Numerically confirmed | Resolution study at ≥3 grids; `T*` stabilizes within 2%; self-similar profile consistent across resolutions | Strong evidence. **Still not a proof.** |
| **3** | Rigorously proven | Interval arithmetic / validated numerics certifying a *true* solution near the numerical profile | The only tier that answers anything. |

Two rules follow, and they are enforced rather than remembered:

- A Tier-1 candidate is **never** reported as more than a candidate, and Tier 2
  is **never** called a proof.
- **"No blow-up found" is not evidence of regularity.** A failed search over an
  infinite-dimensional space says nothing about a universally quantified claim.

`win_condition.py` implements Tiers 1–2 as executable diagnostics;
`test_win_condition.py` proves they detect a known analytic blow-up and reject
non-blow-up behaviour.

## The honest ceiling

Two structural walls cap the whole programme. They are about the problem, not
about effort ([CLAY_ROADMAP.md](CLAY_ROADMAP.md) §2):

- **Wall 1 — a search can only argue *for* blow-up, never for regularity.** If
  3D Navier–Stokes is globally smooth (which many experts lean toward),
  direction (b) is empty and this approach has probability ~0 by construction.
- **Wall 2 — provable ≠ where Clay lives.** Today's rigorous-proof technology
  (validated/interval numerics) works on 1D/2D models simple enough for interval
  arithmetic. 3D Navier–Stokes is far out of its reach, so a Tier-3 result is
  attainable *only* on toy models — which are not Clay.

Consequently the stated prize is a **novel Tier-3 result on a model where
blow-up is provable**, as a genuine contribution and a stepping stone. No
output of this repository is ever summarized as movement toward Clay unless a
link of the chain actually moved — which has not happened in 52 legs.

## Where the project is right now

The plan is **machine-readable and drift-checked**, not prose to be
reinterpreted each session:

```bash
.venv/bin/python plan_of_record.py     # current stage, its pre-committed gate, live bans
```

The committed sequence (adopted 2026-08-04) turned the search around: instead of
evolving *the solution*, evolve **the certificate** — the function space, the
operator split, the weights and constants that a computer-assisted proof
currently picks by human taste. Those choices are low-dimensional, gradient-free,
wildly non-convex, and — crucially — have a **rigorous scalar fitness** (does
the radii polynomial close, and with what margin?) that an under-resolved run
cannot fake.

| Stage | What it is | State |
|---|---|---|
| `M` | Target selection — certify *what*, that isn't already done? | ✅ done |
| `PORT` | Certification port, re-aimed at the 1D Hou–Luo non-symmetric profile, as a bordered system | ✅ done |
| `V` | Viscous survival of the margin as `μ → criticality` | ✅ closed by its own gate |
| `C-PILOT` | Evolve the Lyapunov weight on a known-answer object | ✅ gate answered **NO**; the GA was *not* run |
| `L1` | Certify the target for real: interval arithmetic + analytic far-field enclosure | ✅ done |
| `T` | The tail lemma — border the certificate with the far field transport cannot invert | ✅ done |
| **`TC`** | **Assemble the bordered certificate: the far-field amplitude gets its own column, `Y₀`, and matching condition** | ⏳ **next** |
| `B` | Evolve the certificate — space, operator split, constants | ⛔ blocked (C-PILOT's gate said NO) |

Every stage carries a **pre-committed gate naming both outcomes** before it is
run, so the leg's job is to find out which one happened — not to decide
afterwards what counts as success. Bans (e.g. *no GA compute on an unvalidated
fitness*) are machine-readable and lift only by the condition they name.

## Quick start

Python 3.11+, NumPy 2, and (for figures only) Matplotlib. No SciPy — no adaptive
ODE integrators are used.

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt

.venv/bin/python plan_of_record.py            # what is next, and what is banned
.venv/bin/python capabilities.py              # what already exists (40 modules)
.venv/bin/python capabilities.py hou-luo      # substring search over every field
```

**Before building anything, grep `capabilities.py` for the mathematical object.**
Route-M came ten minutes from rebuilding a validated Scenario-2 integrator that
had been in `solver/` for a week; the index exists so that cannot recur, and
`test_capabilities.py` fails if it drifts from the tree.

Tests are **self-running scripts, not pytest** — 50 of them at the repo root:

```bash
.venv/bin/python test_plan_of_record.py       # the plan/prompt/roadmap drift detector
.venv/bin/python test_capabilities.py         # the capability index vs. the tree
.venv/bin/python test_win_condition.py        # the blow-up diagnostics
for t in test_*.py; do .venv/bin/python "$t" >/dev/null || echo "FAIL $t"; done

scripts/merge_gate.sh origin/main             # the executable merge criterion
```

Figures and evidence rebuild from committed JSON, with **no solver, sweep or GA
re-run**:

```bash
.venv/bin/python writeup/build_figures.py                          # figs 1–7 from writeup/data/
.venv/bin/python writeup/4_p2_lottery/p2_route_t_v1_evidence.py    # one leg's figure + claims
```

## Repository map

| Path | What lives there |
|---|---|
| [`writeup/`](writeup/) | **The banked, self-contained results** — 4 arcs, 47 figures, 57 curated data files. Start at [`writeup/README.md`](writeup/README.md) or the machine-checkable [`writeup/INDEX.md`](writeup/INDEX.md). |
| [`solver/`](solver/) | 41 validated numerical modules: gCLM/CLM, 1D Hou–Luo, 2D Boussinesq, Hilbert transforms, interval arithmetic, spectral & Newton–Kantorovich certificates. |
| [`ga/`](ga/) | The quality-diversity search: genome, operators, fitness, MAP-Elites evolution, logbook, resolution study. |
| [`experiments/`](experiments/) | One runner per leg (35 `p2_*` scripts) plus [`experiments/JOURNAL.md`](experiments/JOURNAL.md). |
| `test_*.py` (root) | 50 self-running test scripts, one per module. |
| [`plan_of_record.py`](plan_of_record.py) | The plan, machine-readable: sequence, gates, bans. |
| [`capabilities.py`](capabilities.py) | What already exists, and the strongest known-answer gate each module passes. |
| [`win_condition.py`](win_condition.py) | Tier-1/2 blow-up diagnostics. |
| [`CLAY_ROADMAP.md`](CLAY_ROADMAP.md) | Strategy: the two walls, routes A–D, go/no-go criteria. |
| [`ORCHESTRATION.md`](ORCHESTRATION.md) · [`ORCHESTRATOR_PROMPT.md`](ORCHESTRATOR_PROMPT.md) | The multi-agent day contract and the paste-able prompt that drives it. |
| [`CONTINUATION_PROMPT.md`](CONTINUATION_PROMPT.md) | Session hand-off: what the last leg settled and what not to re-derive. |
| [`LITERATURE_CHECK.md`](LITERATURE_CHECK.md) | Append-only novelty passes, with the queries run. |
| [`PHASE2_P2_NOTES.md`](PHASE2_P2_NOTES.md) | The long working notes, including ~90 numbered banked lessons. |
| [`scripts/`](scripts/) | `merge_gate.sh` (executable merge criterion), `fetch_papers.sh`, `cloud_setup.sh`. |

## What has been banked

Chronologically, in four arcs — negative results included, because they are the
majority and they are the load-bearing ones:

1. **Arc 1 — 1D gCLM pipeline.** A validated solver, a quality-diversity GA that
   beats budget-matched random search on a verified viscous-blow-up fitness
   (3/3 seeds), 18/18 **Tier-2 resolution-confirmed** candidates, and a
   reproducible shape→viscosity-resistance map. Honest read: these are the
   *generic* (α = 1) CLM singularity surviving advection — a validated pipeline,
   not a novel blow-up.
2. **Non-genericity screen (the pivot).** A 240-run gate showed the GA's edge
   and the novel α ≠ 1 target are **disjoint** on gCLM: non-genericity appears
   only near `a = 1` and only as a grid artifact. Rough C^{1,α} data at
   N ∈ {1024, 2048, 4096} rails too. The cheap 1D route to novelty is closed —
   and the model is now formally banned as exhausted.
3. **Arc 2/3 — 2D Boussinesq and the numerics upgrade.** A ν_crit gate that
   *passed and shouldn't have*, then rebuilt to fail correctly; the two-currency
   negative result (a uniform grid cannot resolve self-similar blow-up) that
   closed the lane; and the replacement — a dynamic-rescaling solver validated
   against a closed-form CLM answer.
4. **Arc 4 — the certification legs (`4_p2_lottery/`).** Interval-arithmetic
   Newton–Kantorovich tooling; sixteen Route-D legs establishing what the naive
   certificate cannot close and *why*; critical-dissipation exponents; a first
   integral for the two-scale profile equation; target selection naming an
   **uncertified** object from the literature; a certificate that closes around
   the *truncated* object (and the measurement showing more reach makes that
   worse); and the tail lemma, where bordering restores a bounded tail exactly
   in the weight classes the Fredholm structure predicted in advance.

Each leg ships as a **quartet**: a runner, curated JSON, a `BLOG_*` + `TECHNICAL_*`
pair, and a registered figure. A result that exists only in a PR body or a
terminal scroll does not exist.

## Reusable contributions (what to steal from this repo)

Most of this is model-agnostic and outlives whatever happens to the Clay attempt:

- **A tiered win condition with executable diagnostics** — the candidate /
  numerically-confirmed / rigorously-proven ladder, plus the standing rule that
  a failed search is not evidence of regularity.
  ([`WIN_CONDITION.md`](WIN_CONDITION.md), [`win_condition.py`](win_condition.py))
- **The six-property viability gate.** Never run an expensive search on a
  fitness axis that hasn't passed a resolution-aware viability screen. This
  repository has three separate records of what it costs to skip it, and one
  gate that passed when it shouldn't have — the reform of it is written up.
- **Pre-committed gates.** Write both outcomes down *before* the run; the leg
  only discovers which happened. Combined with `plan_of_record.py`'s bans, this
  is a practical defence against the post-hoc redefinition of success.
- **A drift detector for plans.** [`test_plan_of_record.py`](test_plan_of_record.py)
  fails the build if the plan, the hand-off prompt and the roadmap stop agreeing.
  A check that is not executable decays at the rate of memory.
- **A capability index.** [`capabilities.py`](capabilities.py) records, per
  module, what mathematical object it holds and *the strongest known-answer
  gate it passes, with the magnitude* — the field that stops a module being
  trusted further than it was tested.
- **Evidence that rebuilds without re-running anything.** Curated JSON +
  `*_evidence.py` per leg means every number in prose is checkable in seconds
  from a fresh clone.
- **Negative results written up with the same care as positives**, including
  standalone citable notes (e.g. the two-currency uniform-grid result) and
  novelty passes that pre-empt construction — one route was closed *before* it
  was built, on finding it had been done in 2024.
- **Validated numerical modules** with published-value gates: 1D Hou–Luo
  dynamic-rescaling (including the three-constant origin-pinned gauge), the
  gCLM `a`-family, whole-line Hilbert transforms on non-uniform grids, 2D
  Boussinesq Biot–Savart, fractional dissipation, interval arithmetic and
  Newton–Kantorovich certificate machinery.
- **A multi-agent operating contract** ([`ORCHESTRATION.md`](ORCHESTRATION.md)):
  six lanes with disjoint file ownership, a verifier that re-measures the
  previous leg's headline before anyone builds on it, an executable merge gate,
  and a short list of things that are *never* merged without a human.

## Working rules (if you contribute)

1. `plan_of_record.py` is the plan. Run it first; bans lift only by the
   condition they name.
2. Grep `capabilities.py` for the object before writing a solver.
3. One leg at a time on the critical path, with its gate pre-committed.
4. Report magnitudes, not booleans; name the realization; run a novelty pass
   before construction; include negative controls that can actually fail.
5. Ship the quartet — runner, curated data, BLOG + TECHNICAL, registered figure
   — including for negative results.
6. `scripts/merge_gate.sh origin/main` must print `MERGE GATE: PASS`.
7. Never describe an output as movement toward Clay unless a link of the chain
   actually moved.

## Reading order

1. [`writeup/1_gclm_1d/SUMMARY.md`](writeup/1_gclm_1d/SUMMARY.md) — one page on
   what the completed 1D pipeline actually established.
2. [`WIN_CONDITION.md`](WIN_CONDITION.md) — how we would know if we had won.
3. [`CLAY_ROADMAP.md`](CLAY_ROADMAP.md) — the walls, the routes, and §7's
   re-framing (evolve the certificate, not the solution).
4. [`writeup/INDEX.md`](writeup/INDEX.md) — one line per leg, with links to
   every artifact and an explicit list of the gaps.
5. [`CONTINUATION_PROMPT.md`](CONTINUATION_PROMPT.md) — the current front line.

## Licence

No licence file is present; all rights reserved by the repository owner unless
one is added.
