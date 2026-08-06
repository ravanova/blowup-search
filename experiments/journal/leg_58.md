# Leg 58 — Route-NG v1: the no-go, stated as a proposition

**Branch** `leg/ng-v1`. **Critical path** (slot LEG-A, stage `NG`). **Figure** `fig55`.
**Gate: YES — and a YES on this gate is an escalation, not a merge.**

> **This leg was interrupted and resumed.** The first agent on `leg/ng-v1` ran and
> committed the novelty pass (`NG-0`) and was then killed by an infrastructure
> interruption before any construction happened. The novelty pass survived on the branch
> and was **not redone** — it is built on, exactly as the resumption directive required.
> Everything below the novelty pass is the resumed agent's.

---

## Order of work (the discipline, as executed)

1. `git fetch origin leg/ng-v1 && git checkout leg/ng-v1` — confirmed the surviving commit
   `b544498` (`NG-0` novelty pass, verdict `PROCEED_NARROW`).
2. `.venv/bin/python plan_of_record.py` — read. `NG` is `NEXT`; every live ban noted. The
   three that bind this leg: *do not repair `B`'s three degrees of freedom* (this leg
   repairs none — it explains why they are dead), *do not build further `ℓ¹`-Fourier
   machinery for this operator before `NG`'s gate answers* (this leg adds four predicate
   functions to an existing module and no new machinery), and *grep `capabilities.py`
   before building anything* (done — `solver/spectral_certificate.py`'s entry already
   carries the tail block, its kernel, the bordered inverse and the ceiling).
3. `CONTINUATION_PROMPT.md` DIRECTIVE 1 in full, `DIRECTION.md`'s leg-58 entry for the file
   territory, `ORCHESTRATION.md` §6 (quartet) and §9f.
4. **Novelty pass: already committed, before any construction** (`writeup/novelty/leg_58.md`).
   Not redone. Its prohibitions were transcribed into the runner's `NG0` clause and into
   the proposition's `what_is_NOT_claimed` list before a single number was produced.
5. Probes → solver predicates → tests → runner → data → figure → writeups.

## What the novelty pass fixed before the construction started

Verdict `PROCEED_NARROW`. Cadiot arXiv:2505.03091 was resolved **from the full text** and
does not contain this no-go: its standing hypothesis is a Fourier multiplier with
`|l(ξ)| ≥ l_min > 0` and `|l| → ∞`, i.e. an infinite **diagonal** tail. This operator's tail
diagonal is **exactly zero** and its unbounded part is a **shift**.

What the pass **forbade**, and what this leg therefore does not claim:

* the **observation** that a tail estimate presumes a dominant diagonal — folklore in
  print (Cadiot §§2–3, arXiv:2411.18361). Leg 51's, and not re-claimed here either.
* the **shapes** — block Gauss–Seidel, Schur complement, rank-one lift are textbook.
* the `m⁻²` kernel decay and the `s < 1` membership threshold — **leg 51's**
  (`fredholm_sides`, and `test_spectral_certificate.py` gate 7 already says *"in `ℓ¹` for
  `s < 1`, so the tail operator is not injective there"*). Re-checked here on the vector
  actually used; **not claimed**.
* anything about `HL_S2_nonsymmetric` or any link of the L1→L4 chain.

Only **the inequality and the class it holds on** were available to claim. That is exactly
what the leg claims and nothing more.

## The finding, and why nobody had it in seven legs

The ingredients were all banked. `fredholm_sides` (leg 51) had the kernel in the space for
`s < 1`; `MM4` (leg 54) had *"`T` is SINGULAR — its kernel is the far field `hhat` — so on
that one direction the term collapses to `-A11 B hhat` and NO CHOICE OF `A12` CAN TOUCH
IT"*, and even its dual half, *"the tail-tail block on the same direction is
`hhat - A21 B hhat`"*. What nobody did was put the two block-rows in the **same column** and
read off the operator norm.

Do that and the proof is three lines. Test `I − AL` on `x = (0; h)`:

```
(I − A L)(0; h) = ( −(A11 B + A12 T) h ;  h − A21 B h − A22 T h )
```

`T h = 0` kills the `A12` term **and** the `A22` term; `A21 = 0` kills the third. So the
column is `(−A11 B h ; h)` and, dividing by `‖x‖_w = ‖h‖_w`,

```
Z1  ≥  1 + ‖A11 B h‖_w / ‖h‖_w  ≥  1     for every A with A21 = 0.
```

`A12` and `A22` never appear — which is precisely why the class is **strictly larger than
block-diagonal**, and precisely why the argument **stops** at `A21 ≠ 0`.

This is **lesson 89 again** ("a term that does not exist until you assemble cannot be
bounded by fixing the terms that do"), in its positive form: the assembly took one leg and
it corrected the reading of the previous four.

## What was hard, and what nearly went wrong

**The kernel's decay is `m⁻²`, not `m⁻¹`.** My first estimate of the recursion gave `m⁻¹`,
which would have put the kernel **outside** `ℓ¹_w` at `s = 0` (log-divergent) and killed the
unconditional form of the theorem — leaving only a quantitative `Z1 ≥ 1 − β ρ` with a
hypothesis on `‖A22‖`. Measuring instead of trusting the estimate is what saved it: the
fitted slope is `−2.0005`, the partial norms settle at `s = 0` and `s = 0.3`, and the
threshold is exactly `s = 1` — which is leg 51's Fredholm crossing, arrived at from the
other side. **A growth rate you cite must be measured on the matrix you actually built.**

**The referee's objection had to be measured, not argued** (`NG2c`). "You chose a split
whose tail block is singular — put the far-field amplitude in the **tail** and it is
invertible." True, and it does not help: the alternative split is the *same operator under a
permutation of one index*, so it was built that way and measured. `T'` is invertible at
every finite `M` and `‖T'⁻¹‖_w` **diverges** with `M` at the fitted rate `M^(1−s)` — the same
exponent, opposite sign, at which the kernel defect `ρ_M` vanishes. The obstruction is
carried by the operator, not by where the amplitude is filed.

**Two conventions for the same control number.** Leg 53 reports `0.9156` for the `μ = 2`
algebraic configuration; leg 54 reports `0.6663`. They are the same configuration measured
two ways — sum of sub-block norms vs true column-max. Both are re-measured here and both
are emitted, because quoting one while the proposition is stated in the other norm is
exactly the cross-leg number error this repository has been burned by twice.

## The sharpness control, and that it can come out the other way

Lesson 90's test — *what would have had to change in the code for this control to report
the other answer?* — is answered by construction here: the control varies `μ`, which changes
the tail operator itself. At `μ = 0` (H2) holds and the theorem forbids `Z1 < 1`; at
`μ = 0.1` the kernel is gone (`σ_min` jumps by more than two orders of magnitude) and by
`μ = 2` the **same two in-class shapes** reach `Z1 < 1`. The hypothesis is necessary, not
decorative.

## Territory and the one file touched outside it

Everything is inside the leg-58 territory declared in `DIRECTION.md`, with one exception
which is the standing convention rather than a deviation: **one appended line** in
`writeup/build_figures.py`'s `P2_EVIDENCE` list, which `DIRECTION.md` requires to stay
**append-only** and which every leg since 53 has appended to in order to register its
figure. No shared ledger was touched: `experiments/JOURNAL.md`, `LITERATURE_CHECK.md`,
`plan_of_record.py`, `CONTINUATION_PROMPT.md` and `PHASE2_P2_NOTES.md` are untouched, and
this file plus `writeup/novelty/leg_58.md` stand in for the first two.

`capabilities.py` was **read and not edited** — it is outside the declared territory, and
leg 54 set the precedent of not editing it from a leg branch. Its
`solver/spectral_certificate.py` entry's `validated` field now understates what the module
carries (it stops at leg 53's assembly); **flagged for the orchestrator** rather than fixed
here.

## The gate, and why it is parked rather than landed

**YES.** The named class is `A_upper = { A = [[A11, A12], [0, A22]] }`; it strictly contains
block-diagonal and contains leg 54's separately-measured `gs_upper`; and its hypotheses are
verified **on** the `a = 0` CLM tail block rather than assumed. Per the pre-committed
branch, a YES is *"the repository has a Tier-3-shaped negative theorem; write it as a
standalone claim with its sharpness control, and **escalate publication scoping to the
user**"* — so this branch is **pushed and parked**, not merged to `main`.

**And the ceiling is unmoved.** The object is still the `a = 0` CLM linearisation, whose
`Y₀` is exactly zero for the degenerate reason banked since leg 51. A wall measured here
bounds the real target's difficulty **from below** and no more. **No link of the L1→L4 chain
moved.** Clay odds remain ~0.05%.
