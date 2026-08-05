# Leg 61 — Route-KA v1: a known-answer window for the whole interval pipeline

**Agent:** LEG-E. **Branch:** `leg/ka-v1`. **Date:** 2026-08-05/06.
**Gate answered YES on its literal reading, NO on the stricter pre-committed window, and the
gap between those two answers is measured, not argued.**

Deliverables: runner `experiments/p2_route_ka_v1_kawahara.py` · curated data
`writeup/data/p2_route_ka_v1_kawahara.json` · technical note
`writeup/4_p2_lottery/TECHNICAL_P2_ROUTEKA_V1.md` · executable gate
`test_interval_certificate.py` (14)–(18) · novelty log `writeup/novelty/leg_61.md`.
No figure — audit leg, per the established convention for known-answer legs.

---

## The one-line finding

`solver/interval_certificate.py`, run end to end on CLN's Kawahara problem at CLN's own
truncation, closes its radii polynomial and **certifies existence at every radius in
`[6.77e−15, 2.62e−02]` (H^l), an interval that contains CLN's published `[2.27e−14, 1.5e−02]`
entirely** — so their refereed `r₀` is a certified radius of our polynomial, with 0.53 decades
of margin below and 12.06 above.

## Order of work

1. `plan_of_record.py` read; no ban touches a known-answer interval audit.
2. **Novelty pass first, committed before any construction** (`b241964`). Verdict
   `PROCEED_AS_INTERNAL_AUDIT`: the Kawahara soliton is proved and published, so no claim is
   available to this leg beyond a statement about our own pipeline.
3. `capabilities.py` grepped before building. Nothing in the stack does Fourier-cosine
   convolution or Kawahara; `nk_fourier.py`/`spectral_certificate.py` are the compactified
   `X = tan(θ/2)` basis for the gCLM object, not reusable here. New enclosure class justified.
4. Construction, run, ablations, gates.

## What made the window pre-committable — and it nearly wasn't

CLN's paper prints `T = 0.35`, `c = 0.9`, `‖DF_e(u₀)⁻¹‖_{2,l} ≤ 4.4`, `Y₀ ≤ 2.26e−14`,
`r₀ = 2.27e−14`, uniqueness in `B_{0.015}` — **and not the truncation.** Lesson 84 wants the
window fixed at their truncation, which the paper does not state.

Their reference [15] is a live repository: `github.com/matthieucadiot/ProofKawahara.jl`, fetched
in full. Lines 357–360 give **`N = 250` cosine modes, half-domain `d = 50`**. Worth recording
against the ledger: `LITERATURE_CHECK.md` marks arXiv:2604.09949 unusable partly because *no*
verification package was released. CLN are the opposite case, and that is the only reason this
leg was runnable as specified.

## The sign convention was confirmed before any constant was quoted

Dropping `λ₂` leaves the KdV reduction, whose sech² soliton at these parameters has
`α = −0.2`, `β = √3`. Newton from that seed gives a profile with minimum **−0.181650** at the
origin, `|u(d)| = 4.3e−18`, `|a_N| = 1.6e−22`. CLN's Figure 1 shows a minimum a little above
−0.18. A sign slip in `λ₁, λ₂, λ₃` would have made every downstream number a rigorous bound on
the wrong problem; this is gate (14) so it stays checked.

## The result

`Y₀ = 3.0243e−17`, `Z₁ = 3.059e−13`, `Z₂ = 8.5455e+03`, `‖A‖_w = 2.9834`,
`Y₀/budget = 5.169e−13`. Float Newton residual `1.301e−18`.

* **Reading A (the gate's words, on the certified set): YES.** `r₀ = 2.27e−14` is inside our
  certified interval; our `r_max` also passes their uniqueness ball by 1.75×.
* **Reading B (my stricter pre-committed window, on `r_min` itself): NO, short by 3.35×
  (0.53 decades)** at the lower end of an 11.8-decade window; upper end clear by 12.3 decades.

Both are reported. I did not move the window.

## Two explanations nominated in advance, both killed by measurement

The pre-committed reading of a low `r_min` was **over-optimism**. Two mechanisms would have
made that reading right, and neither survives:

| ablation | needed | delivered | verdict |
|---|---|---|---|
| CLN's trace projection onto `ker T^N_{4,e}` | 3.34× | **1.025×** | not it |
| the discarded mode-`(N,2N]` tail of `u²` | `1.59e−14` | **`1.665e−17`** | 2.98 decades short |

The resolution sweep found the real mechanism. Across `N = 60…300`, `Y₀` **in our own norm is
flat at ≈3.0e−17** — set by the float64 residual, not by resolution — while the converted
`r_min` climbs `3.31e−15 → 7.20e−15`, tracking `√(2N+1)` exactly. **The position of our radius
relative to CLN's is set by the cross-norm conversion factor, not by the arithmetic.**

So the honest statement is not "3.35× over-optimistic". It is: our upper bound sits 3.35× below
their upper bound *after a deliberately pessimistic conversion*, and two upper bounds in that
relation contradict nothing. The bug-hunt branch needs the pipeline to fail where they prove
existence, or to close only above their uniqueness ball. **It does neither.**

## The thing to carry forward, and it is a caveat not a trophy

Because the comparison passes through `√(2N+1)`, **this gate localises the pipeline to a factor
of a few — roughly half a decade. It is not a digit-level check and must never be cited as one.**

That resolution is nonetheless ample for the job it was built for. Leg 56 reports consistency
defects of **1.854e+07×** and **2.040e+11×** from this same pipeline (verified against its own
`TECHNICAL_P2_ROUTETN_V1.md` §171, not taken from the brief). Those sit **7 and 11 decades**
from this gate's resolution, so they clear it with ~6.5 and ~10.5 decades to spare. The leg's
stated worry — that a pipeline which had never met a published answer is a weak place to source
a number that large — is answered in the pipeline's favour, at a resolution that is stated
rather than implied.

## Ledger work I could not do (integration-owned)

`capabilities.py` is outside my territory, so its `solver/interval_certificate.py` entry still
describes only the internal validations. It should gain: *"reproduces CLN's published Kawahara
radius END TO END — their `r₀ = 2.27e−14` is a certified radius of this module's own polynomial
at their truncation (N=250, d=50); gate resolution ~0.5 decades, set by the `√(2N+1)` cross-norm
conversion."* Flagging for integration rather than editing a shared ledger.

## Standing disciplines exercised

* 75 — the two gaps (Fourier tail, unbounded-domain passage) are named as **not** bounded here,
  before the radius is quoted, not after.
* 84 — window pre-committed in the novelty log, in a separate commit, before construction.
* 85/90 — the mechanism ablations could have come out the other way, and did: both failed to
  explain the gap, and that is reported rather than quietly dropped.
* 86 — the conversion factor is checked as an inequality against random vectors (gate 17)
  rather than trusted from the algebra.
