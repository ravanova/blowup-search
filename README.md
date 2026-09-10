# blowup-search

An honest, long-shot attempt at the **Navier–Stokes Existence and Smoothness**
Millennium Prize Problem — and, along the way, a set of reusable machinery for
anyone doing computer-assisted singularity research.

The project searches for **finite-time blow-up** in fluid models: first with
evolutionary (quality-diversity) search over initial data, and now with
**computer-assisted certification** of self-similar blow-up profiles. Every
claim in the repository is tiered, gated, and rebuildable from committed data.

> **New here?** Read **[READING_THIS_REPO.md](READING_THIS_REPO.md)** first — the
> vocabulary (legs, waves, gates, `UNVERIFIED`, `L1 → L4`), the three-tier rule that
> governs every claim, and an explicit list of what this repository does and does
> **not** claim. Reuse terms and third-party material: [NOTICE.md](NOTICE.md).

> ## ▶ Where this is now: arc 7 — running the kernel
>
> **2026-09-10, OPEN.** Arc 7's job is narrow, and it is the one thing this repository
> can honestly do about the 2026 claim: **run the Lean kernel to completion on the two
> exported theorems** — because out-refereeing 166 pages is beyond this repository and
> running a kernel is not.
>
> **`K1` (leg 437) is GREEN in three environments** on one pinned commit: `lake build`
> completes (11251 jobs, 0 errors) and `#print axioms` returns
> `[propext, Classical.choice, Quot.sound]` for both exported theorems, with `sorryAx`
> not reachable. **That is not a verification of the manuscript, and this repository
> does not call it one.** The Lean statements are Fefferman's **(C)/(D) — strictly
> weaker than the paper's Theorem 1.1**, five existence clauses absent; mathlib's oleans
> were replayed from the official cache, not rebuilt; and under this repository's own
> rule a second machine is not a second agent, so `K1` stays **`UNVERIFIED`** until a
> blind agent reproduces it from the banked artefacts.
> Record: [`experiments/journal/leg_437.md`](experiments/journal/leg_437.md).
>
> **Still open:** `K2` (the Lean's gaps — five `PARTIAL` statements, four `sorry`, the
> comparator checks) is in flight; `K3` (the construction re-run under a two-route
> evidence rule) and `K4` (the verdict written for outsiders, `writeup/7_confirmation/`)
> have not started. **Until `K4` lands there is no single page here stating what a green
> kernel does and does not establish — the paragraph above is the interim answer.**
>
> ## ▶ Start here: [arc 6 — what we can actually say about the claim](writeup/6_adjudicated/BLOG_ADJUDICATED.md)
>
> **2026-09-09.** On 2026-09-08 a 166-page manuscript and a Lean project claimed
> finite-time blowup for the **forced** 3D Navier–Stokes equations on `ℝ³` —
> **Fefferman's Alternative (C)**, the statement this programme was aiming at.
> **Arc 6 read it at primary**: six gates, six legs, one session, `§3f` SOLO.
>
> **What arc 6 establishes.** The statement is (C), and it **claims (D) too** —
> which arc 5 had recorded as untouched, and which is the only unbroken way this
> repository's own wall `W4` can break. The Lean project's top-level statement
> **is** (C) and (D), and its definitions are **byte-identical to Google
> DeepMind's independent formalisation** of the Clay problem — checked here
> against the upstream source, not against the comment that says so. Its
> 580-module dependency graph is `sorry`-free at source level.
>
> **What arc 6 does NOT establish.** That the proof is correct. ~~Sections 4–9 were
> **not read** and the Lean was **not compiled** — the build is blocked on a host
> this environment's egress policy denies, which is reported and not routed
> around.~~ Nothing here suggests the proof is wrong either.
>
> **STRUCK 2026-09-10 (leg 431), on the user's instruction; recorded, not rewritten.** The
> struck sentence described the first pass (legs 417–422). The second pass under `§3g` read
> **all 166 pages twice** — solo (leg 425) and by five blind shards (leg 428), 79 of 79
> statements both times — and re-derived a 58-node spine (leg 429: 58 `CHECKED`, 0 `GAP`,
> 10 `VERIFIED` by a blind verifier). The Lean was **measured, not compiled to the theorem**
> (leg 431): the cache host *was* reachable this time, the toolchain builds mathlib without
> error, and the main theorem was never reached, so its kernel status is `NOT-ESTABLISHED` —
> and what the kernel would accept is Fefferman's (C)/(D), strictly weaker than Theorem 1.1.
> The outer profile of Lemma 4.8 was instantiated from the paper's schedule (leg 430): its
> constants, exponents and pressure datum reproduce; its closure and cone do not at any
> pre-registered `λ`, and the sweep locates where they do (`λ ≤ 3·10⁻⁴`). Tier 2 throughout.
>
> **And the part that is ours.** The manuscript's residual-absorption mechanism
> was ported onto this repository's own banked object, with every advantage
> granted to it. **`W4` does not break**, and the reason is measured twice — once
> at exactly `−1.500000`, and once as a **logarithm** that a power-law fit reads
> as *bounded*. A logarithm this repository flagged **in advance**, in the
> pre-registration, because it has been fooled by one twice before.
>
> **SECOND PASS (legs 423–434, 2026-09-10, §3g CONDUCTOR ×5) — the verdict, in one paragraph.** Read twice —
> solo and by five blind shards — all 79 statements index and close as the manuscript says (Props 9.5/9.6
> are never cited downstream). Re-derived by four agents and checked blind by a fifth, the 58-node spine
> holds: 480 steps, no `GAP`, **ten nodes `VERIFIED`**. Instantiated from the paper's own schedule, Lemma
> 4.8's profile reproduces its constants, exponents, pressure datum and tail stress (two routes agree to
> `10⁻⁹`); its closure and cone do **not** reproduce at any `λ` a grid reaches — the paper's own asymptotics
> put them at `λ ≲ 3·10⁻⁴`, `√λP_* ≪ 1`, and its outer-edge powers on a collar `δ ≲ 10⁻⁶⁹`. Measured, the
> Lean is `sorry`-free outside its challenge placeholders, source-covers all 79 statements, exports
> Fefferman's (C)/(D) — **strictly weaker than Theorem 1.1** — and, in a build the Conductor completed after the
> agents reported (leg 435), **both exported theorems are accepted by the Lean kernel with axioms
> `[propext, Classical.choice, Quot.sound]`** — ~~one run, one container, unreplayed.~~
>
> **CORRECTED 2026-09-10 (arc 7, legs 436–437); struck, not rewritten.** Leg 435's `#print axioms` ran on a
> build that never **completed** (`CORRECTIONS.md` §72). Arc 7's unit `K1` supplies the completed build and
> repeats it: **GREEN in three environments** on the same pin — 11251 jobs, 0 errors, both theorems on the
> same three axioms, `sorryAx` not reachable in any of them. It stays **`UNVERIFIED`**: mathlib's oleans were
> replayed from the official cache rather than rebuilt, and a second machine is not a second agent
> ([`experiments/journal/leg_437.md`](experiments/journal/leg_437.md)).
>
> *Arc 6's summary continues:*
> Wave 4's adversary faked eleven of twelve pre-registered signals, so they are not evidence. **Nothing
> measured contradicts the manuscript; nothing measured proves it; no wall moved.** Tier 2 throughout.
> [TECHNICAL_REPRODUCTION.md](writeup/6_reproduction/TECHNICAL_REPRODUCTION.md) ·
> [BLOG_REPRODUCTION.md](writeup/6_reproduction/BLOG_REPRODUCTION.md) · fig113, fig114
>
> [BLOG_ADJUDICATED.md](writeup/6_adjudicated/BLOG_ADJUDICATED.md) ·
> [TECHNICAL_ADJUDICATED.md](writeup/6_adjudicated/TECHNICAL_ADJUDICATED.md) ·
> [five curated JSONs](writeup/data/) · fig112
>
> **Every arc-6 gate is `UNVERIFIED`** — §3f rule 1: verification is a fresh
> session or it is not verification, and one session measured all of this and
> wrote its own answers. **No wall moved. No `L1 → L4` link moved. Clay stays
> ~0.05%. Tier 2 is never a proof.**
>
> *Arc 5, the concluding writeup of the search programme itself —
> [BLOG_OUTPACED.md](writeup/5_outpaced/BLOG_OUTPACED.md) ·
> [TECHNICAL_OUTPACED.md](writeup/5_outpaced/TECHNICAL_OUTPACED.md) — is the arc
> before it, and arc 6 corrects two of its readings:
> [`CORRECTIONS.md` §61 and §63](writeup/CORRECTIONS.md).*

> **Status, stated plainly.** ~~146 legs in~~ (**stale — 416 legs at the
> 2026-08-19 stop**), nothing here resolves the Clay
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
link of the chain actually moved — which has not happened in 146 legs.

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
| `TC` | Assemble the bordered certificate: the far-field amplitude gets its own column, `Y₀`, and matching condition | ✅ done |
| `MM` | The mismatch — is a non-block-diagonal approximate inverse a real lane? | ✅ gate answered **NO** |
| `NG` | The no-go, stated as a theorem and checked against the literature | ✅ closed **YES** (leg 58) |
| **`B`** | **Evolve the certificate — space, operator split, constants** | ⛔ closed **NO** (leg 126): full declared search space (1,686 configurations) audited, zero uncovered, best reachable margin 6.04x short. Committed sequence exhausted; next step awaits a user ruling. |

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

To see the pace of the orchestrated run — cumulative numbered legs landed
against the calendar — regenerate the progress chart from git history:

```bash
python3 scripts/legs_over_time.py            # writes reports/legs_over_time.html
open reports/legs_over_time.html             # (or just open it in a browser)

python3 scripts/legs_over_time.py --since 2026-08-01   # widen the x-axis floor
```

It parses `Leg N: ...` commit subjects, so it stays accurate as new legs land;
the output is gitignored rather than committed since it's stale the moment
the next leg merges. The x-axis floor defaults to `auto` — the hour the first
numbered leg landed — so the chart frames the run instead of the flat line
before it; `--since YYYY-MM-DD` widens it for calendar context. **Run it on a
full clone:** the numbering starts at leg 54, and a shallow clone silently
drops the early legs from the chart (`git fetch --unshallow` first).

### Starting an orchestrated run

Paste the **full text** of [`ORCHESTRATOR_PROMPT.md`](ORCHESTRATOR_PROMPT.md) — and nothing
else, no accompanying question — into a fresh Claude Code session on Sonnet 5 in this
repository. It is written as a direct instruction, so the session starts dispatching
immediately. Watch progress in the git-ignored `PROGRESS.md`; stop it with `touch STOP`
(graceful) or `touch STOP-NOW` (hard). Full contract in
[`ORCHESTRATION.md`](ORCHESTRATION.md).

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
| [`ORCHESTRATION.md`](ORCHESTRATION.md) | The multi-agent contract: roster, leg territories, landing policy, how to start a run. |
| [`ORCHESTRATOR_PROMPT.md`](ORCHESTRATOR_PROMPT.md) | **The paste-able prompt** that turns a fresh session into the orchestrator. Pure instruction — no notes about itself. |
| [`DIRECTION.md`](DIRECTION.md) | The Decision Maker's ranked leg queue and live slot assignments. |
| [`CONTINUATION_PROMPT.md`](CONTINUATION_PROMPT.md) | The critical-path leg's directive: what the last leg settled and what not to re-derive. |
| [`LITERATURE_CHECK.md`](LITERATURE_CHECK.md) | Append-only novelty passes, with the queries run. |
| [`PHASE2_P2_NOTES.md`](PHASE2_P2_NOTES.md) | The long working notes, including ~90 numbered banked lessons. |
| [`scripts/`](scripts/) | `merge_gate.sh` (executable merge criterion), `fetch_papers.sh`, `cloud_setup.sh`, `legs_over_time.py` (progress chart). |

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
  four parallel legs with disjoint file territories, a Decision Maker that plans
  every leg, paired verifiers that re-measure headline numbers before anyone
  builds on them, an executable merge gate every landing must pass, and a short
  list of things that are *never* pushed without a human.

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
