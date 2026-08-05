# Leg 62 — Route-CP: the Cadiot pre-emption, settled from the full text

**Agent:** LEG-B. **Branch:** `leg/cp-v1`. **Date:** 2026-08-05/06. **Difficulty:**
standard. **Claim-bearing:** yes (literature classification).

## Gate

> Does Cadiot arXiv:2505.03091's construction cover an operator whose unbounded part is
> off-diagonal with a non-decaying tail inverse — i.e. does it already contain leg 58's
> no-go, or a positive result that contradicts it?

**ANSWERED: NO.** `no ->` branch taken: the gap leg 57's ledger measured is confirmed at
full-text depth for the one paper most likely to close it. NG may claim novelty against
this paper and no further.

## Order of work (the protocol, and it was followed in this order)

1. `plan_of_record.py` read; every ban noted. The one that binds this leg is the
   re-claiming ban whose lift condition is *literally this gate*: "unless a pass resolves
   whether Cadiot's construction covers a zero diagonal, which is now the live open
   question, not BDL's".
2. `capabilities.py` grepped before building — it already indexes
   `solver/certificate_shapes.py` (leg 57's SHAPE_LEDGER) and
   `solver/literature_gates.py`. Both were EXTENDED, not rebuilt.
3. **Novelty pass written and committed BEFORE construction** (`8ab84fa`), six verbatim
   queries with links, not counts.
4. Full texts fetched (`Papers/fetch.sh`) and read: 2505.03091, 2504.05066, 2404.08529,
   2302.12877.
5. Ledger, re-derivations, tests, runner, figure, writeups.

## What was actually read, and how deep

| paper | role | depth |
|---|---|---|
| arXiv:2505.03091 (Cadiot) | the paper under test | FULL TEXT |
| arXiv:2504.05066 (Breden–Payan–Reisch–Tang) | Cadiot's [15], most general Gershgorin located | FULL TEXT |
| arXiv:2404.08529 (Cadiot–Blanco) | Cadiot's [20], the systems extension | FULL TEXT |
| arXiv:2302.12877 (CLN) | Cadiot's [21], the framework; Assumption 2.1 re-read | FULL TEXT |
| FL91, LAA 143:7–17 (1991) | Cadiot's [24], the Gershgorin theorem invoked | **SECOND HAND** — paywalled, no arXiv copy |

19 located statements, none from an abstract. FL91's row is flagged `SECOND_HAND`,
carries `rho = None`, and is **refused** by `cp_gate_answer` rather than counted either
way. Leg 53's correction applied as code.

## The answer, in one paragraph

Cadiot's Assumption 1 requires the unbounded part to be a **Fourier multiplier**
(`F(Lu)(ξ) = l(ξ)F(u)(ξ)`, eq. 2) with `|l(ξ)| ≥ l_min > 0` and `|l| → ∞`. Diagonality is
not ambient: the proof of Lemma 3.3 turns on *"since `L` is diagonal, `L π_N = π_N L
π_N`"*, which is the step that removes the unbounded part from the off-diagonal
Gershgorin radii. And `DG(ũ)` is assumed relatively compact w.r.t. `L` (Lemma 2.2). Three
independent exclusions, all hypotheses rather than gaps. The near miss — §5.2's Whitham
equation, the one carrying `u ∂_x u` — disposes of the transport before it reaches the
linear part: the traveling-wave reduction divides out `∂_x` and leaves `G(u) = u²` with a
bounded derivative.

## The finding that was not asked for, and it caps NG's WORDING

BRT arXiv:2504.05066 §2.1 removes the nonzero-diagonal hypothesis from the classical
infinite-matrix Gershgorin theorem: *"some of the assumptions of [FL91, Theorem 2.1] are
needlessly restrictive (for instance, all the diagonal elements of `L` have to be
nonzero)"*. Their Theorem 2.6 needs only a Schauder basis, property (2.2), and a compact
resolvent.

**So a no-go phrased as "the published machinery requires a nonzero diagonal" is FALSE.**
It costs NG nothing in substance — the generalised theorem applies to a zero diagonal and
returns disks of infinite radius, i.e. it is vacuous, not violated (their Definition 2.5:
*"its radius `r_i(L)` can be infinite"*). But NG must phrase the no-go **quantitatively**,
as an ordering of growth rates, which is BRT Lemma 2.10's own requirement `p − q₁ < 2/n`.

Relayed to the orchestrator for NG mid-leg rather than at the end, because NG is heavy and
was still building.

## The axis, and why it is `ρ` and not the exponent difference

`ρ = limsup_k (off-diagonal row sum) / |diagonal|`, needed `< 1` by every located source.
Chosen over `γ_D − γ_R` because **BDL separates them**: BDL has equal exponents and is
still admissible, on the constant `ρ ≤ 2δ < 1`. A classification by exponent alone would
put BDL on the wrong side. Ours: `γ_D = 0`, `γ_R = 1`, `ρ = ∞`.

## Magnitudes

- Gate: **no**, over **3** full-text literature rows, **1** refused (FL91).
- Cadiot Assumption 1 re-derived at his own parameters: SH `l_min` **0.3200** (= `µ`),
  growth exponent **4.0000**; Whitham `l_min` **0.2000** (= `1 − c`), growth exponent
  **0.5017**; Gray–Scott `σ₀` **10.000** (= `λ₂`).
- The one off-diagonal entry in the whole Cadiot corpus (Gray–Scott, `λ₁=19, λ₂=10`):
  **189, a constant**, against a diagonal growing like `|2πξ|²`. Crossover at
  `ξ* = 2.1293`; `ρ` decays with exponent **−1.9967**; `ρ` at 100× the crossover is
  **1.06e−04**. Ours is `+∞` at every index.
- BRT's diagonal weight against a nearest-neighbour shift: damps by **at most 4.88e−04**
  at index 8192, over `p ∈ {0, 0.5, 1, 2, 4}`.
- The same weight on BRT's own operator reproduces their published exponent `p − q₁` to
  **≤ 2.4e−15** at three parameter pairs.

## What surprised me

Two things.

**One.** The strongest exclusion was not an absence. I expected to report "the paper
never discusses this case". What is actually true is better: the case is excluded by the
paper's *defining hypothesis*, and the diagonality is used inside a proof step (Lemma
3.3) whose failure is precisely NG's mechanism. A gap can be filled by a revision; a
defining hypothesis cannot be, without becoming a different paper.

**Two, and this is the one worth carrying.** Legs 51–53 measured "the coupling entry is
`K/2` for EVERY `s`" and banked it as a mechanism that was *measured, not argued*. BRT's
Definition 2.8 repairs infinite Gershgorin radii with a diagonal weight `f(i) = max(1,
i^p)` — **the same family**. Conjugation maps `(i,j) → (f(i)/f(j)) M_{i,j}`, and for a
nearest-neighbour coupling `f(i)/f(i+1) = (i/(i+1))^p → 1` for every `p`. The sweep did
not fail because the sweep was unlucky; it failed because a diagonal weight is
asymptotically flat a bounded distance from the diagonal, which is exactly where a shift
lives. **A repository measurement acquired a one-line proof from a paper that was fetched
to check something else.**

## What I did NOT do

- Did not read FL91 (paywalled). The row says so and the gate refuses it.
- Did not re-run leg 57's operator dial — `p2_route_xs_v1_shapes.py` owns that; leg 57's
  `SHAPE_LEDGER` and its 15 gates were left untouched, and `CP_LEDGER` is a separate
  ledger with its own gate.
- Did not touch the five shared ledgers, `plan_of_record.py`,
  `CONTINUATION_PROMPT.md`, or `PHASE2_P2_NOTES.md`.
- Did not write a BLOG. Optional for a pure literature leg; the narrative is one
  paragraph ("surprise two" above) and it lives in the TECHNICAL §6 where it is load
  bearing, rather than being padded into a second document.

## Territory

`solver/certificate_shapes.py`, `test_certificate_shapes.py`,
`solver/literature_gates.py`, `test_literature_gates.py`,
`experiments/p2_route_cp_v1_cadiot.py`,
`writeup/4_p2_lottery/TECHNICAL_P2_ROUTECP_V1.md`,
`writeup/data/p2_route_cp_v1_cadiot.json`,
`writeup/figures/fig56_route_cp_v1_cadiot.png`, `writeup/novelty/leg_62.md`,
`experiments/journal/leg_62.md`, plus the **append-only** one-line fig56 registration in
`writeup/build_figures.py` (DIRECTION.md declares that file append-only across the four
legs of this cycle).
