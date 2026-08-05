# Leg 54 — Route-MM v1: THE MISMATCH. Journal.

**Branch** `leg/mm-v1`. **Stage** `MM` (critical path). **Gate answer: NO.**

## Order of work, and it mattered

1. `plan_of_record.py`, `CONTINUATION_PROMPT.md` DIRECTIVE 1, `DIRECTION.md` §54.
2. **MM-3 novelty pass FIRST**, committed as `writeup/novelty/leg_54.md` *before*
   `p2_route_mm_v1_shape.py` existed (commit `8e7a36b`). Links, not counts.
3. `capabilities.py` grepped for the object before building — `solver/spectral_certificate.py`
   entry names the assembled state and its ceiling.
4. Construction, controls, gate.

## What the novelty pass changed about the claim

It found the thing that makes MM-1 a real statement rather than a complaint:
**arXiv:2411.18361 states the block-diagonal convention explicitly** — for `DF` a *compact
perturbation of the identity*, take `A = A^N + π^∞`, i.e. let the tail act as the identity.
So the block-diagonal shape is the convention, not this project's misreading of it, **and
the hypothesis that buys it is exactly the one this operator fails** (leg 51: the unbounded
part is a shift, not a multiplier). Block Gauss–Seidel vs Schur-complement preconditioning
is textbook (Numer. Math. `10.1007/BF01385611`); nothing is banked as novel.

## VER-A's verification, and the two things it forced

VER-A re-derived leg 53's headline independently and confirmed **all** of it to full printed
precision, including both closed forms (`4(K−1)` exact in rational arithmetic). Two
corrections were adopted rather than argued with:

* **GAP 1 — MM-1 does not reach small `K`.** The prefactor `|1 − K/2|` is exactly 0 at
  `K = 2`, so the RHS clears 1 only from `K ≥ 5` (flat) / `K ≥ 4` (algebraic). Leg 53's
  sweep started at `K = 4` and hid it. **MM-1 as the directive states it — "no
  block-diagonal `A` can work for this operator" — is not established.** It is stated here
  with its `K` restriction attached.
* **GAP 2 — the second factor is 0.94 … 1.39, not the 0.94 … 1.33** that
  `CONTINUATION_PROMPT.md` quotes and that is not traceable to leg 53's JSON. This leg
  quotes its own measured range.

## The finding that closed VER-A's hole, and it was an accident

Sweeping `K = 3` to check the hole **crashed on a singular matrix**. Chasing that instead of
working around it: **every odd split has an exactly singular augmented finite block** — in
both classes, under both gauges, with and without the far-field column (smallest singular
value `0.0` at `K = 3` without the column). The reason is structural: `ĥ` lives on one
parity chain (`K+1, K+3, …`) and the linearisation couples `k` only to `k ± 1`, so at odd
`K` the mode-`K` residual row picks up no entry on any of `b_1…b_K` or `δc_ω` and is carried
entirely by the amplitude column.

So **the split must be even**, and VER-A's open corner `{2, 3, 4}` collapses to `{2}` in both
classes plus `{4}` in the flat class — both of which MM-4's floor covers. *This removes
candidate splits; it does not choose one, so it is not the banned re-entry by tuning `K`.*

## The main result

Seven shapes of `A`, all measured as the **true column-max of `I − A L`** over the whole
space rather than as leg 53's sum of sub-block norms. Ordered by what they establish:

* **block Gauss–Seidel with `Γ` swept first is worth exactly nothing** — and the algebra
  says so before the run does: `I − Λ⁻¹L` has `(Γ,tail)` block `−Γ⁻¹B`, *identical* to the
  block-diagonal one. Measured: identical to 5 digits. A prediction that could have failed.
* **tail-first Gauss–Seidel and the Schur complement do help**, and the help is real.
* **The exact inverse of the truncated operator reads `~1e−9`, and that number is a
  tautology** (lesson 86). MM-3 makes it admissible — finite rank to `M_A`, then the only
  explicit operator available — and it becomes `1e4`, *worse than the baseline by two
  orders*, growing with `M_A` while being independent of `M_L` to five digits. The cost is
  at the **seam**, which is the same mismatch one level up.
* **MM-4 is the part that generalises.** `(I − AL)_{Γ,tail} = −(A11 B + A12 T)`, and `T` is
  **singular** on exactly the far-field direction the certificate borders, so applied to
  `ĥ` it collapses to `−A11 B ĥ` and **`A12` drops out of the algebra**. That floor is
  shape-independent. Dually `(I − AL)_{tail,tail} ĥ = ĥ − A21 B ĥ`, which is *why* the shape
  must be non-block-diagonal — and `ff_lift` builds exactly that rank-one lift, fixes the
  tail-tail block, and is swamped because it cannot touch `(Γ,tail)`.

## Corrections made to leg 53, in place

**The tail–tail sub-block was understated.** Leg 53 measured `‖I − A_tail B_bordered‖`
against the matrix `A_tail` actually inverts and got `6.0e−13`. But the assembled operator's
tail–tail block is the **bare** scaled tail `T`, which is singular; the bordering is part of
the construction of `A`, not part of `L`. Charged correctly it is ≈ 2.2, not `6.0e−13`.
**This makes leg 53's baseline worse, not better**, so its NO is unaffected — but it is the
term `ff_lift` then removes, and it had to be visible before that move made sense.

## The control that did not do what it was supposed to

**The border-direction negative control does not discriminate for the Schur shape.** With a
random border, Schur's `Z₁` comes out *smaller* than with the analytic border, across all six
seeds tried. The mechanism is visible: `S = G − B A_tail C` partly undoes whatever the border
did to `Γ`, so the Schur shape is much less border-sensitive than the block-diagonal one —
a property of the shape, not a bug. Reported, not buried. Consequences: the border control
licenses the negative for `block_diag` and `gs_upper` but **not** for `schur`, where the
negative rests on the `μ`-dial positive control and on MM-4's floor instead. The smallest
`Z₁` anywhere in that table is still far above 1, and chasing it would mean tuning the
border, which is **banned**.

## What I did not do

* Did not tune `s`, the weight family, the split, or the border — all banned, all measured
  dead in leg 53.
* Did not claim anything about `HL_S2_nonsymmetric`. `Y₀ = 0` here for the banked degenerate
  reason (the anchor **is** one basis mode), and on the gate's own terms that object is
  reached only if the polynomial closes here.
* Did not edit `plan_of_record.py`, `CONTINUATION_PROMPT.md`, `PHASE2_P2_NOTES.md`,
  `experiments/JOURNAL.md` or `LITERATURE_CHECK.md`.

## Lessons this leg would add

* **A degeneracy that crashes your sweep is data.** The odd-`K` singularity arrived as a
  `LinAlgError` while checking someone else's flagged hole, and it closed most of that hole.
  Working around the crash would have lost it.
* **When the optimum of a free choice is a tautology, the audit IS the experiment.** The
  gate as literally worded ("does a non-block-diagonal `A` bring `Z₁` below 1") is trivially
  yes — take `A = L⁻¹`. What makes it a real question is admissibility, and that had to be
  measured rather than asserted.
