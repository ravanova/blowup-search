# Reading this repository

This repo has its own vocabulary and its own rules about what counts as a result.
Both exist to stop it fooling itself, and both make it hard to read cold. This page
is the key. Ten minutes here will save you an hour of confusion.

---

## What this is, in three sentences

A long-shot attempt at the **Navier–Stokes existence and smoothness** Millennium
Prize problem, run almost entirely by AI agents under a written contract. It did
not solve it — and in September 2026 the statement it was aiming at was claimed by
someone else, so the project turned to **independently checking that claim** instead.
Everything here is tiered, gated, and rebuildable from committed data, and the
project's own honest odds of ever solving the problem are recorded throughout as
**~0.05%**.

## The one rule that governs everything

Three tiers, and **only the third answers anything**:

| Tier | What it takes | What it means |
|---|---|---|
| **1 — Candidate** | one run shows the blow-up signal (`1/‖ω(t)‖_∞` fits a line, forward zero-crossing, `R² ≥ 0.98`) | cheap to produce by accident |
| **2 — Numerically confirmed** | resolution study at ≥3 grids, `T*` stable within 2% | strong evidence — **still not a proof** |
| **3 — Rigorously proven** | validated/interval numerics certifying a true solution | the only tier that resolves anything |

**Tier 2 is never called a proof.** If you find a sentence in this repository that
seems to break that rule, it is a bug — please report it.

The mirror rule: *"no blow-up found" is not evidence of regularity.* A failed search
over an infinite-dimensional space says nothing about a universally quantified claim.

## Where to start

1. **[`writeup/6_reproduction/BLOG_REPRODUCTION.md`](writeup/6_reproduction/BLOG_REPRODUCTION.md)**
   — what we can actually say about the 2026 Navier–Stokes claim, having read all
   166 pages and run the Lean.
2. **[`writeup/5_outpaced/BLOG_OUTPACED.md`](writeup/5_outpaced/BLOG_OUTPACED.md)**
   — the conclusion of the search programme itself, including the part where this
   project identified the winning idea six weeks early and priced it away in a
   subordinate clause.
3. **[`writeup/README.md`](writeup/README.md)** — the full index, arcs 1–7, in the
   order they happened. Arc 7 is **open**; its own writeup does not exist yet, so
   its units are indexed in [`writeup/INDEX.md`](writeup/INDEX.md) instead.
4. **[`WIN_CONDITION.md`](WIN_CONDITION.md)** — the tiers above, in full.

Everything else is working surface. **[`STATE.md`](STATE.md)** is the live board and
is written for the agent that reads it next, not for you.

## Vocabulary

| term | meaning |
|---|---|
| **leg** | one unit of work, numbered sequentially (leg 1 … leg 437+). The atom of the record. Every commit names its leg. |
| **wave** | a batch of 2–5 legs dispatched in parallel, then integrated together |
| **arc** | a phase of the project with its own writeup folder (`writeup/1_gclm_1d/` … `writeup/6_reproduction/`) |
| **lane** | a line of attack (T = torus, V = viscous, L = last obligations, R = reformulation) |
| **gate** | a question written down **before** the work, in the exact wording it must be answered in |
| **pre-registration** | the gate plus its tolerances, committed and pushed before the run that answers it. This is why a "NO" here is trustworthy: the target could not move after the number arrived. |
| **banked** | committed to the record. **A banked datum is never edited** — corrections are recorded beside it, never over it. That is why you will see struck-through text left in place. |
| **planted control** | a deliberate corruption inserted to check the instrument notices. A control that "did not fire as planted" is reported as a defect, not hidden. |
| **adversary** | an agent whose job is to fake a result. If it can reproduce your signal from a deliberately wrong run, **your signal is not evidence** — whatever your gate said. |
| **quartet** | the four things every finding must ship with: a runner, curated JSON, a BLOG + TECHNICAL pair, and a figure. A result that exists only in a chat log does not exist. |
| **`UNVERIFIED` / `VERIFIED`** | *Verification is a fresh session or it is not verification.* A result is `VERIFIED` only if an agent with **no memory of how it was produced** reproduced it from banked data. Self-checking is `UNVERIFIED` and says so. Most of this repo is `UNVERIFIED`. |
| **`W1`–`W7`** | the seven named walls between here and an answer, in [`WALLS.md`](WALLS.md). `W4` (finite energy / localisation) is the hard one. |
| **`L1 → L4`** | the chain of links that would have to move for this project to be nearer a Clay answer. **It has never moved, in 400+ legs.** No output is described as progress toward Clay unless a link actually moves. |
| **core-h** | CPU-hours of attempt compute |
| **escalation** | a question only the human operator may answer. An agent that both raises and rules an escalation has defeated the mechanism. |

## What this repository claims, and what it does not

**Claims:**

- A 1D pipeline at **Tier 2** — and states plainly that it is the known CLM
  singularity surviving advection, not a novel result.
- A full independent read of the 2026 manuscript: all 166 pages, twice, 79 of 79
  statements ledgered, a 58-node proof spine re-derived.
- That on one pinned commit, in **three environments**, the two exported Lean
  theorems were accepted by the Lean 4 kernel depending on no axioms beyond
  `propext`, `Classical.choice` and `Quot.sound` (arc 7, leg 437) — and that this
  is still **`UNVERIFIED`**, because a second machine is not a second agent.

**Does not claim:**

- That the Navier–Stokes problem is solved, by us or by anyone. The Clay prize has
  four conditions and none is met.
- That the 2026 manuscript is **correct**. Nothing measured here contradicts it;
  nothing measured here proves it.
- That the Lean kernel check settles the manuscript's Theorem 1.1. The Lean
  statement is Fefferman's alternatives (C)/(D) — **strictly weaker** than the
  paper's theorem, with five existence clauses absent. Two further limits are banked
  with the result and neither is softened: mathlib's oleans were **replayed from the
  official cache, not rebuilt from source**, and all three runs were directed by one
  role from one brief, so the check stays **`UNVERIFIED` until a blind agent
  reproduces it** from the banked artefacts.
- Any position whatsoever on the priority dispute around that manuscript.

If you are about to quote something from here, quote its status with it. A number
without its tier and verification label is a misquotation.

### Worker files are not findings

Most of `writeup/data/` is raw artefacts written by individual agents, in agent
shorthand, *during* a wave — intermediate measurements, notes to the integrator, and
observations recorded at whatever confidence the agent had at the time. They are
committed unedited on purpose, because that is what makes the integration auditable.

**A phrase in a worker file is not a finding of this repository until an integration
leg has ruled on it.** The adjudicated reading always lives in that arc's
`TECHNICAL_*.md`, under its pre-committed gate wording, with the caveats attached.

This matters most where a worker is measuring somebody else's construction inside
*our* parameter regime. A line like *"(7.9) fails"* or *"no computable `q` is in the
paper's regime"* in `writeup/data/arc6/wave4/` is an exact statement about **our
instantiation at the `λ` we pinned** — not a claim about the source material. The
arc's technical note says so directly: the construction does not close at any `λ` a
grid can reach, **and the paper never said it would**. Quoting the worker line
without that frame inverts its meaning.

## Checking a claim yourself

Every number in the prose lives in a JSON under `writeup/data/`, and each arc ships
a script that rebuilds those numbers and **exits non-zero if the prose has drifted
from the data**:

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python writeup/5_outpaced/outpaced_evidence.py
.venv/bin/python writeup/6_reproduction/reproduction_evidence.py
```

Third-party PDFs are not committed. `bash Papers/fetch.sh` re-pulls them by name
and verifies each sha256.

## How this was made

Written almost entirely by AI agents (Claude, various models), directed by one human
operator, under the contract in [`ORCHESTRATION.md`](ORCHESTRATION.md). Commits name
the authoring model; most link the session that produced them.

That is worth knowing before you weigh anything here. The verification discipline
above — pre-registered gates, planted controls, blind verifiers, adversaries, the
refusal to call self-checked work verified — exists specifically because the work
was done this way. Where it failed, the failures are recorded in
[`writeup/CORRECTIONS.md`](writeup/CORRECTIONS.md), which currently runs to 68
numbered entries, many of them corrections to the agents' own earlier claims.

Reuse terms, and what in here is not ours: [`NOTICE.md`](NOTICE.md).
