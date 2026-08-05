# Leg 64 — Route-A12 v1: is `alpha_1` at `a = 1/2` unsearched, or just unlooked-at?

**Branch** `leg/a12-v1`. **Exploration leg**, light, pure literature — claim-bearing
(literature classification). **No computation, no gCLM measurement.**
**Gate: SPLIT — YES on the `sigma = 3` half, NO on the `alpha_1` half.**

---

## Order of work (the discipline, as executed)

1. `plan_of_record.py` — read. `NG` is `NEXT`. The ban that binds this leg hardest is
   **"another gCLM measurement leg (lifted by: never)"**: this leg runs nothing, quotes
   Route-H v1's ladder, and touches no solver. Also noted and honoured: **"building a
   solver without grepping `capabilities.py` for the object first"** — `capabilities.py`
   was grepped first, and it is the source of this leg's entire premise (line 80).
2. **`DIRECTION.md` has no leg-64 entry.** The file's status block is still the cycle of
   2026-08-05, last leg number **57**, queue items renumbered 59/60/61. **Flagged for the
   orchestrator**, same finding leg 57 flagged: the DM's queue is behind the dispatch. The
   thesis and the verbatim gate came from the dispatch prompt instead.
3. **Novelty pass FIRST**, committed before the write-up
   (`writeup/novelty/leg_64.md`, commit `fc33b3e`). **Nine queries, links not counts**,
   per `writeup/novelty/README.md`'s post-leg-53 rule.
4. Full-text pass on four PDFs, then the query-log script, the curated JSON, this journal.
   No figure — pure literature leg, nothing numeric to plot.

## What the leg was asked, and the one-sentence answer

> "Does any primary source publish `alpha_1` at `a=1/2` (or the `sigma=3` criticality
> statement it comes from) for this model?"

**The disjunction had two halves and they answer opposite ways.** The `sigma = 3`
criticality at `a = 1/2` is **published, exactly, in a Tier-1 paper this repository had
already read for something else** — Xu `arXiv:2607.19762` §6.1, Table 1 row `a = 0.5`,
Figure 3 — and `alpha_1` itself is **searched and not found** anywhere in the model's
literature.

## The part that was a surprise

The leg was dispatched to search *beyond* Tier 1, on the strength of `PHASE2_P2_NOTES.md`
J-2's parenthetical "criticality there is `sigma = 3`, in neither ALS nor XU". **That
parenthetical is false about XU.** Xu §6.1 says, verbatim,

> "The branch value is tested at `a = 1/2`, where `s∗ = 3` exactly (`cl(1/2) = 1/3` by the
> exact solution of [20]; also [4, Thm. 2]) and J. Chen [20] proved blow-up at `s = 2 < 3`
> (subcritical), consistent with persistence."

and his Figure 3 is annotated **in the plot** with `s * (1/2) = 3 (exact)`. Under the
repository's own exponent dictionary (`their Λ^σ` = `our (-Δ)^s` with `σ = 2s`), Xu's
`s*(1/2) = 3` **is** our `σ_c = 3`, digit for digit — and his is exact where ours is a
numerical branch value. **The search that answers the gate's first half never needed to
leave Tier 1; it needed to read one more row of a table the repository had already cited
for `a_c`.**

That is a lesson-shaped event: a claim was carried for a whole J-pass on the strength of a
paper being classified by *what it was read for*, not by what it contains.

## The part that held

`alpha_1 = dα/dμ` at the marginal fixed point is **not published**, and the reason is
structural rather than an artifact of how hard anyone looked. The dissipative-gCLM
exact-solution corpus is, exhaustively,

    real line   (a, σ) ∈ {(0,0), (0,1), (0,2), (1/2,1)}      ALS §5.1–§5.4
    periodic    (a, σ) ∈ {(0,0), (0,1), (1/2,0), (1/2,1)}    SLSA arXiv:2411.01891

and **`σ = 3` is in neither list.** `alpha_1` at `a = 1/2` is a coefficient of the marginal
flow *at* `σ = 3`, so there is no exact solution in the literature to read it off from.
Xu, in the same subsection that publishes the threshold, says the case `s = s*` is
**marginal** and that persistence there "is the program of Section 8, not established
here"; his Appendix A machinery is at `a = 0` only.

Breadth actually covered, so "not found" means something: a 100-result arXiv API
enumeration of the whole `Constantin-Lax-Majda` corpus (the dissipative subset is exactly
four papers), full-text greps of all four, seven web searches including one on the digits
`0.133683`, and Sakajo's two 2003 papers (Xu's refs [18]/[19] — `a = 0`, and thresholds
**in** `ν` rather than a derivative **of the exponent with respect to** `ν`).

## Two traps, either of which would have closed the gate wrongly

**T1 — "critical dissipation" means two different things at `a = 1/2`, differing by a whole
unit of `σ`.** J. Chen (`1908.09385` §1.2) defines criticality by **norm scaling**:
`Λ^γ` with `γ = |a|^{-1}`, which at `a = 1/2` is **`γ = 2`**. The scaling-relevance
criticality of the self-similar profile is **`σ = 3`**. Chen's theorem is, in Xu's own
classification, **subcritical**. Reading "global well-posedness with critical dissipation"
as covering our point would have produced a false YES.

**T2 — ALS's "'marginal' dissipation" is `σ = 0`**, from a 1D Oldroyd-B stress model. It is
the bottom of the `σ` range, not `σ = σ_c`. It is the only "marginal" hit in the
dissipative corpus, and it is a false friend.

## The magnitudes

| quantity | value |
|---|---|
| our `alpha_1` at `a = 1/2`, `K = 240` | **+0.133683** |
| ladder `K = 96/144/192/240` | 0.132770 / 0.133470 / 0.133628 / **0.133683** |
| full-ladder spread | **9.13e-4** |
| last-two-rung spread | **5.50e-5** |
| distance of the value from zero, in last-rung spreads | **2431×** |
| Xu `s*(1/2)` | **3**, exact |
| our `σ_c` at `a = 1/2` | **3**, exact (from `α(1/2) = 3`) |
| `c_l(1/2)`: exact / Xu Table 1 / this repo's cold ALS (49)–(50) integration | 1/3 / 0.3333 / **0.3333076** (rel **7.7e-5**) |
| dissipative gCLM papers in the whole arXiv CLM corpus | **4** |
| queries logged | **9** |

**The sign is the load-bearing digit, not the sixth decimal.** `alpha_1 > 0` means `μ`
decays like `1/(alpha_1 τ)` — algebraically, the linear term being gone — so the critical
viscous solution relaxes onto the inviscid profile. The sign holds across every rung with
`2431×` the last-rung spread of margin.

## What this leg reports rather than edits

`capabilities.py`, `LITERATURE_CHECK.md` and `PHASE2_P2_NOTES.md` are all outside this
leg's territory, and the dispatch is explicit that `solver/critical_dissipation.py` must
not be edited under any gate outcome. **Three corrections are reported for the
orchestrator**, stated precisely in `writeup/novelty/leg_64.md` §5 and machine-readable in
`writeup/data/p2_route_a12_v1_alpha_lit.json` under `reported_corrections`:

1. **`capabilities.py` line 80** — the clause `"a=1/2 is UNSEARCHED at primary source"` is
   stale in both directions and should name Xu for the `σ = 3` half and
   *searched-not-found* for `alpha_1`. The clause `"alpha_1 = 0 at a=0 == ALS eq (61)"` is
   **confirmed** (ALS §5.3 eq (61) is the `a=0, σ=1` self-similar form carrying `ν` inside
   the profile at `c_l = β = 1`) and stays.
2. **`LITERATURE_CHECK.md`** — the row's source column "not in Tier 1" is wrong for the
   criticality statement; the verdict moves `unsearched → searched, not found`.
3. **`PHASE2_P2_NOTES.md` J-2** — the parenthetical is false about XU. Its conclusion
   survives; the corrected reason is stronger than the wrong one.

`solver/critical_dissipation.py` itself **needs no correction**: its module docstring
states the marginal-case reduction and the sign criterion, and nothing in it asserts
novelty. The stale annotation lives in `capabilities.py`, not in the solver.

## The honest label, which is the leg's actual deliverable

`alpha_1 = +0.133683` at `a = 1/2` is **measured, not independently validated**: one
instrument, one basis, one convergence ladder, float64, no interval enclosure, and — now
established rather than assumed — **no external number to check it against, because none
exists.** That is a smaller claim than "novel" and a better-supported one than
"unsearched", and it is the claim the repository should carry.

## Files

* `experiments/p2_route_a12_v1_alpha_lit.py` — the query log, source locations
  (paper section + extracted-text line), verbatim quotations, emitter.
* `writeup/data/p2_route_a12_v1_alpha_lit.json` — curated data; every number and citation
  in the prose above is in it.
* `writeup/novelty/leg_64.md` — novelty log **and** this leg's technical note.
* No figure (pure literature leg).
