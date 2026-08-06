# Route-NG v1 — the no-go, stated as a proposition, and the class it is a theorem on

**Stage `NG`, leg 58. Gate answer: YES.** Data: `writeup/data/p2_route_ng_v1_nogo.json`.
Runner: `experiments/p2_route_ng_v1_nogo.py`. Figure: `fig55_route_ng_v1_nogo.png`, rebuilt
from the curated JSON alone by `experiments/p2_route_ng_v1_nogo_evidence.py`. Novelty pass:
`writeup/novelty/leg_58.md`, run and committed **before** any construction.

> **Gate, in its pre-committed wording.** *Does the no-go admit a proof for a named class of
> approximate inverses strictly larger than block-diagonal, with hypotheses that provably
> contain the `a = 0` CLM linearization?* — **YES.** The yes-branch fires: *the repository
> has a Tier-3-shaped negative theorem; write it as a standalone claim with its sharpness
> control, and **escalate publication scoping to the user**.* This branch is therefore
> **parked, not merged**.

> **The claim is narrow on purpose and the scope line is load-bearing.** What is proved is a
> statement about approximate inverses with `A₂₁ = 0`. What is *measured* is everything
> else, and leg 54's battery is the whole of it. **"No `A` we tried" is still not "no `A`",
> and this leg does not pretend otherwise.**

---

## 0. What seven legs held, and what was missing

Legs 51–57 produced every part of a negative result and assembled none of them: a named
mechanism (the unbounded part is **off-diagonal**, a shift, while the standard tail estimate
needs a **multiplier**), an inequality that covers the block-diagonal case (`MM-1`), a
battery over seven shapes of `A` bottoming at `Z₁ = 8.9591` against a block-diagonal
baseline of `10.4584`, a positive control that reports the other answer, and a literature
classification saying the case is unpublished.

What was missing was not more measurement. It was the **write-up as a proposition**, with
the one open mathematical question named honestly — and, if possible, an extension of
`MM-1` past the block-diagonal case.

The extension exists, and it was sitting in the repository in two halves.

---

## 1. The proposition

**Setting.** `L` is the `a = 0` CLM steady linearisation in the compactified odd-sine
coefficient basis, bordered with the far-field amplitude as an extra unknown and its
matching condition as an extra equation (leg 52's repair, leg 53's assembly). It is split at
mode `K` as

```
L = [[G, B],
     [C, T]]
```

with `G` the finite block on modes `1..K` plus the gauge and amplitude auxiliaries, and `T`
the tail block on modes `K+1..M`. The norm is weighted `ℓ¹`, `w_k = (1+k)^s`.

**Hypotheses.**

* **(H1)** the split is the one the radii-polynomial method uses — a finite block carrying
  the auxiliaries, and a tail the certificate must handle by an *explicit* operator rather
  than a numerical inverse;
* **(H2)** the tail block `T` has a kernel **in the space**: `T h = 0` with
  `0 < ‖h‖_w < ∞`;
* **(H3)** `A` is a bounded approximate inverse with `A₂₁ = 0` — its tail rows do not couple
  back to the finite block. `A₁₁`, `A₁₂` and `A₂₂` are otherwise **arbitrary**.

**Conclusion.** For every such `A`,

```
Z₁ = ‖I − A L‖_w  ≥  1 + ‖A₁₁ B h‖_w / ‖h‖_w  ≥  1.
```

The radii polynomial requires `Z₁ < 1`, so **no approximate inverse in the class closes the
certificate — at any split `K`, in any weight class with `s < 1`**.

**Proof.** Test the operator on `x = (0; h)`:

```
(I − A L) x  =  ( −(A₁₁ B + A₁₂ T) h ;  h − A₂₁ B h − A₂₂ T h ).
```

`T h = 0` kills the `A₁₂` term **and** the `A₂₂` term; `A₂₁ = 0` kills the third. So
`(I − A L) x = (−A₁₁ B h ; h)`, whose `ℓ¹_w` norm is `‖A₁₁ B h‖_w + ‖h‖_w`. Divide by
`‖x‖_w = ‖h‖_w`. ∎

`A₁₂` and `A₂₂` never appear. **That is exactly why the class is strictly larger than
block-diagonal, and exactly why the argument stops at `A₂₁ ≠ 0`.**

### 1a. The class, and in what sense it is strictly larger

```
𝒜_upper  =  { A = [[A₁₁, A₁₂], [0, A₂₂]] : A₁₁, A₁₂, A₂₂ bounded }
```

Block-diagonal is the **single point** `A₁₂ = 0`, `A₂₂ = A_tail` inside it. `𝒜_upper` also
contains leg 54's `gs_upper` shape (one step of block Gauss–Seidel, tail swept first,
`A₁₂ = −Γ⁻¹ B A_tail`), which leg 54 measured as a *separate* shape. Of leg 54's seven
shapes, **two are inside the class** (`block_diag`, `gs_upper`) and **five are outside**
(`gs_lower`, `schur`, `ff_lift`, and the two inadmissible ones) — all of which have
`A₂₁ ≠ 0`. Both facts are checked numerically in the runner rather than asserted from the
construction: the in-class shapes measure `‖A₂₁‖ = 0` exactly, and `‖A₁₂‖ > 0` on
`gs_upper`, which is what makes the containment strict.

### 1b. What this adds over `MM-1`

`MM-1` bounds the same sub-block but *through the coupling column*, giving

```
Z₁  ≥  |1 − K/2| · (w_{K+1}/w_K) · ‖A_tail e_{K+1}‖_w / w_{K+1}
```

which is measured to be an exact equality (`1.89e−15`) — but whose `|1 − K/2|` prefactor
**vanishes at `K = 2`**, so its RHS only clears 1 from `K ≥ 6` (flat) / `K ≥ 4` (algebraic),
and which fixes `A₂₂ = A_tail`. The proposition above has **no prefactor, no `K`
restriction, and no constraint on `A₂₂`**. It therefore closes `MM-1`'s small-`K` corner
*within this class* and enlarges the class at the same time.

---

## 2. (H2), measured — and the reporting error it nearly caused

The proof needs the tail kernel to be **in** `ℓ¹_w`. That the kernel decays like `m⁻²`, and
that this puts it in the space exactly when `s < 1`, is **leg 51's** — `fredholm_sides`, and
`test_spectral_certificate.py`'s gate 7 has said *"in `ℓ¹` for `s < 1`, so the tail operator
is not injective there"* since that leg. **It is not claimed here.** What this leg does is
check it on the vector actually used, over a ladder of truncations.

`‖h‖_w` partial sums at `K = 8`, over `M = 256, 1024, 4096, 16384`:

| `s` | partial `‖h‖_w` | last increment ratio `r` | verdict |
|---|---|---|---|
| 0.0 | 4.3765 → 4.4692 → 4.4923 → **4.4981** | **0.2498** | converges |
| 0.3 | 10.9897 → 11.5691 → 11.7877 → **11.8705** | **0.3785** | converges |
| 0.7 | 41.3407 → 48.1501 → 52.6225 → **55.5699** | **0.6590** | converges |
| 1.0 | 122.2190 → 166.1654 → 209.9030 → **253.5886** | **0.9988** | log-divergent |
| 1.5 | 901.6809 → 1916.6042 → 3936.0536 → **7969.7767** | **1.9974** | power-divergent |

**The discriminator is the increment ratio, not the shape of the curve — and this is where
the leg nearly reported the wrong thing.** At `s = 0.7` the partial sum is still visibly
rising at `M = 16384` and a "has it settled?" criterion calls it divergent. It is not: the
increments shrink geometrically by `0.659` per rung, so the series converges (to about
`61.3` by geometric extrapolation), as `Σ m^{−2} m^{0.7} = Σ m^{−1.3}` must. A boolean would
have recorded a false negative on a hypothesis this leg's whole result depends on. **Report
a magnitude, never a boolean** — applied to a convergence test.

At `s = 1` the increments are *constant* (`r = 0.9988`) — logarithmic divergence — and at
`s = 1.5` they *double* (`r = 1.9974`) — power divergence. **So the threshold is exactly
`s = 1`**, which is leg 51's `fredholm_sides` crossing reached from the other side, and
`s = 1` is separately banned already (leg 52: the one exponent at which bordering cannot
help, because the kernel leaves the space at the same moment the cokernel functional enters
the dual).

**Both classes legs 51–54 actually used — `s = 0` and `s = 0.3` — are inside the
hypothesis.** That is what "hypotheses that provably contain the `a = 0` CLM linearization"
means here, and it is why the gate can answer YES.

### 2a. Two realizations, named

On the **infinite** tail the recursion makes `T h = 0` exactly, and the bound is the
unconditional `Z₁ ≥ 1 + floor`. At **finite `M`** the truncation leaves a nonzero edge term,
so the honest finite-`M` statement is

```
Z₁  ≥  1 + floor − ρ_M · (‖A₁₂‖_w + ‖A₂₂‖_w),      ρ_M := ‖T h‖_w / ‖h‖_w.
```

`ρ_M` is a pure truncation artifact — `T h` is zero on every interior row to `3.55e−15` and
nonzero only at the truncation edge, both of which are gated in
`test_spectral_certificate.py` (*"analytic right null vector is a kernel"* and *"the far
field is annihilated except at the truncation edge, and that falls like 1/M"*) — and it
vanishes on the ladder:

| class | `ρ_M` over `M−K = 128 … 2048` | fitted | predicted |
|---|---|---|---|
| flat `s = 0` | 5.469e−02 → 3.418e−03 | `M^(−1.0000)` | `M^(−1.0)` |
| algebraic `s = 0.3` | 9.754e−02 → 1.292e−02 | `M^(−0.7288)` | `M^(−0.7)` |

i.e. `ρ_M ∼ M^{−(1−s)}`, degenerating exactly at `s = 1` again. **The gap between the two
realizations is therefore predicted, not noise**, and §3 holds the measurement to it.

---

## 3. The bound against leg 54's battery

The runner rebuilds leg 54's assembled object unchanged and measures the `ĥ`-column of
`I − A L` for every shape, at `K = 2, 4, 8, 16, 32` in both admissible classes, against
**both** forms of the bound.

**Instrument check first (lesson 85).** At the configuration leg 54 reported its headline on
(algebraic `s = 0.3`, `K = 2`, `M−K = 1024`), this leg re-derives `block_diag` = **10.4584**
and `ff_lift` = **8.9591** — leg 54's baseline and best admissible — to a relative gap of
**7.157e−06**. (That gap is BLAS reduction order, not drift: this runner pins the thread
count precisely so a verifier gets the same digits, and leg 54's run did not.) The battery
being compared against is the same battery.

**The three things that could have gone wrong, and did not:**

1. **The finite-`M` bound is never violated.** Over every in-class measurement the slack
   `column − (1 + floor − ρ_M(‖A₁₂‖+‖A₂₂‖))` is at least **+5.336e−04**.
2. **The measured columns never fall below 1**, which is what the proposition forbids. The
   in-class minimum over the whole sweep is **6.0424** — the corresponding full `Z₁` is
   **9.5660**.
3. **The deviation from the infinite-tail equality is the truncation.** The largest
   `|column − (1 + floor)|` anywhere in the class, divided by the truncation budget
   `ρ_M(‖A₁₂‖+‖A₂₂‖)`, is **0.5047** — under 1, so the entire discrepancy is accounted for
   by the edge term §2a predicts, with nothing left over.

A sample of the columns against the infinite-tail bound `1 + ‖A₁₁ B ĥ‖_w/‖ĥ‖_w`:

| class, `K` | `ρ_M` | `block_diag` column (bound) | `gs_upper` column (bound) |
|---|---|---|---|
| flat, 2 | 9.77e−04 | 8.0073 (8.0078) | 8.0078 (8.0078) |
| flat, 8 | 6.84e−03 | 56.3794 (56.3828) | 56.3831 (56.3828) |
| flat, 32 | 3.03e−02 | 255.4930 (255.5078) | 255.5692 (255.5078) |
| algebraic, 2 | 4.56e−03 | 6.0424 (6.0444) | 6.0427 (6.0444) |
| algebraic, 32 | 6.42e−02 | 86.8226 (86.8497) | 86.8863 (86.8497) |

So the bound is not merely valid, it is **attained** on that column — and the containment is
strict in the direction that matters: over these in-class measurements `‖A₂₁‖ = 0` exactly
while `‖A₁₂‖` reaches **218.97**, so `A₁₂` is genuinely free and genuinely large, and the
bound does not care.

---

## 4. The split-placement audit — the referee's objection, measured

> *"You chose a split whose tail block is singular. Put the far-field amplitude in the
> **tail** instead and the tail block is invertible."*

True, and it does not help. The alternative split is the **same operator under a permutation
of one index** — the amplitude column and its matching row move from the finite block to the
tail — so it is built that way and measured rather than argued.

`T'` is invertible at every finite `M`, and `‖T'⁻¹‖_w` **diverges** with `M`:

| class | `‖T'⁻¹‖_w` over `M−K = 128 … 2048` | fitted | `ρ_M` fitted (§2a) |
|---|---|---|---|
| flat `s = 0` | 18.29 → 292.6 | `M^(+1.0000000000000016)` | `M^(−0.9999999999999832)` |
| algebraic `s = 0.3` | 10.25 → 77.43 | `M^(+0.7287819933069677)` | `M^(−0.7287819933068554)` |

**The same exponent `1 − s`, with the opposite sign, to twelve digits.** Either the tail
block has a kernel (amplitude in the finite block) or its inverse is unbounded (amplitude in
the tail). The obstruction is carried by the **operator**, not by where the amplitude is
filed.

**Scope:** this is a measured ladder over `M−K = 128…2048` at `K = 8` with a fitted exponent.
It is **not** a proof that `‖T'⁻¹‖_w` is unbounded, and the proposition is not stated for
that split.

---

## 5. Where the proof stops, and it is exactly one unit

`A₂₁ ≠ 0` buys back **one unit and nothing else** — the term `h − A₂₁ B h` that hypothesis
(H3) excludes. Comparing the `ĥ`-column of `block_diag` against `ff_lift` (the rank-one
far-field lift) across the whole sweep, the removed amount is **0.9451 … 0.9990**.

On the infinite tail that credit is exactly 1. At finite `M` it falls short, and **the
shortfall is the truncation defect and not something else**: the largest deficit anywhere is
**0.0549**, and across all ten configurations the deficit **never exceeds `ρ_M`**, tracking
it at a ratio of **0.856 … 0.997** while `ρ_M` itself moves over the sweep by a factor of
66 (`9.77e−04` at flat `K = 2` to `6.42e−02` at algebraic `K = 32`). Had the shortfall not
been proportional to `ρ_M`, the mechanism would have been wrong.

The residual `‖A₁₁ B ĥ‖_w/‖ĥ‖_w` survives every admissible lift.

**That is the precise place the proof stops.** Beyond it this repository has:

* leg 54's battery over seven shapes × class × gauge × split, best **admissible**
  `Z₁ = 8.9591` against baseline `10.4584` — a **1.167×** improvement where more than **8×**
  was needed;
* leg 54's `MM4c`, which **refuted** a shape-independent floor by an explicit rank-one
  counter-construction (floor → `~1e−16`), surviving only because the total `Z₁` then hits
  `5.7e+05`.

So the residual term is beatable *in principle*, at a catastrophic cost in the rest of the
operator, and **no proof covers `A₂₁ ≠ 0`**. The general no-go is a **measurement over a
battery** and is described that way everywhere it appears in this repository.

---

## 6. Sharpness — the hypothesis cannot be dropped

Lesson 90's test is *what would have had to change in the code for this control to report
the other answer?* Here the control varies `μ`, which changes the tail operator itself, so
the answer is "the operator, and it does".

With `Λ¹` dissipation the tail acquires a diagonal `−μk`: it becomes a **multiplier**, (H2)
fails outright, and the proposition has no content. Measured at `K = 16`, `M−K = 1024`,
algebraic `s = 0.3`:

| `μ` | `σ_min(T)` | `Z₁` `block_diag` | `Z₁` `gs_upper` |
|---|---|---|---|
| 0.0 | 1.4463e−02 | 549.4506 | 146.2360 |
| 0.1 | 2.0548e+00 | 94.0535 | 78.7174 |
| 0.5 | 9.2174e+00 | 2.4379 | 2.7461 |
| 1.0 | 1.7746e+01 | 1.0858 | 1.0150 |
| 2.0 | 3.4593e+01 | **0.6663** | **0.4026** |
| 4.0 | 6.8360e+01 | 0.5195 | 0.1740 |

Both of these shapes are **inside the proved class**. At `μ = 0` the theorem forbids
`Z₁ < 1` and the measurement agrees at every `K` and in both weight classes; the kernel is
gone by `μ = 0.1` (`σ_min` jumps by more than two orders of magnitude) and by `μ = 2` the
same class is comfortably under 1. **The hypothesis is necessary, not decorative.**

**Cross-leg number hygiene.** Leg 53 reports `0.9156` for the `μ = 2` algebraic
configuration; leg 54 reports `0.6663`. These are the *same configuration measured in two
conventions* — sum of the four sub-block norms versus the true column-max. The proposition
is stated in the operator norm, so `0.6663` is the number that bears on it; both are
re-measured here and both are emitted to the JSON, because quoting one while arguing in the
other is precisely the cross-leg error this repository has been burned by twice.

---

## 7. Scope, and what is not claimed

**PROVED.** The class `A₂₁ = 0` — every block-diagonal and every block-upper-triangular
approximate inverse, with `A₁₂` and `A₂₂` free — at every `K`, for every `s < 1`.

**MEASURED, NOT PROVED.** Every `A` with `A₂₁ ≠ 0`. For those there is leg 54's battery and
nothing else.

**Not claimed, per the novelty pass** (`writeup/novelty/leg_58.md`, `PROCEED_NARROW`):

* the **observation** that a tail estimate presumes a dominant diagonal — folklore in print.
  Cadiot arXiv:2505.03091 §§2–3 states it, arXiv:2411.18361 restates it with a compactness
  justification. Cadiot's own hypotheses were located in the **full text** — a Fourier
  multiplier with `|l(ξ)| ≥ l_min > 0`, `|l| → ∞`, tail an infinite **diagonal** matrix — and
  this operator fails all three, so Cadiot does not contain this no-go and carries no
  positive result contradicting it. **Leg 62 reads the same paper at greater depth by
  assignment, and its reading caps this one.**
* the `m⁻²` kernel decay and the `s < 1` threshold — **leg 51's**.
* the shapes of `A` — textbook preconditioning.
* **anything about `HL_S2_nonsymmetric`, and anything about any link of the L1→L4 chain.**

**The ceiling, pre-committed.** The object is the `a = 0` CLM linearisation, whose `Y₀` is
**exactly zero** because the anchor *is* one basis mode — so the radii polynomial's root
`r = 0` is available for a degenerate reason and certifies nothing. A wall measured here
bounds the real target's difficulty **from below**, and no more. Float64 throughout, no
interval arithmetic: the *proof* is exact linear algebra on an explicitly constructed
kernel, but every *number* in this document is a float measurement.

**No link of the L1→L4 chain moved.** Clay odds remain ~0.05%.
