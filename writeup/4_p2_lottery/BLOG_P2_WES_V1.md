# The window wasn't zero-width. The trial space was.

*Route-WES v1, leg 178. Technical companion: `TECHNICAL_P2_WES_V1.md`. Data:
`writeup/data/p2_route_wes_v1_space.json`. Runner:
`experiments/p2_route_wes_v1_space.py`. Figure: `fig66`.*

*Gate answer: **YES** — under the user's ruling of 2026-08-07, which broke a tie this leg
deliberately refused to break itself. That story is the second half of this post.*

## The thing leg 111 found, and the one knob it never turned

Sixty-seven legs ago this project built a weighted-energy instrument for the `a = 0` CLM
linearisation — the friendliest object in the repository — and asked it a simple question. You
want the operator to be damped at the origin, and for that you need the weight to be singular
enough: exponent `γ > 3`. You also need your trial functions to actually live in the weighted
space, and for that you need the weight to be *tame* enough: `γ < 3`.

Same number. The window where both hold has **width zero**, closing exactly at `γ = 3`. Every
admissible weight in leg 111's seven-member family came back with a negative gap converging to
`−(3 − γ)/2`.

That is a real obstruction, and it looks like a fact about the operator. But leg 111 swept
exactly one axis — the weight — and held the other one fixed. Its trial space was
`span{sin kθ}`, whose functions vanish at the origin to order `p = 1`. The membership threshold
is not `3` in general; it is `2p + 1`. At `p = 1` that is `3`, which is the same number as the
damping threshold, which is why the window closed.

**Change `p` and the two thresholds stop coinciding.** This leg turned that knob.

## Constrain the trial space at the origin — someone else's idea, and we say so

The move is not ours and cannot be claimed at any strength. Elgindi, Ghoul and Masmoudi
([arXiv:1906.05811](https://arxiv.org/abs/1906.05811), Prop. 2.1) prove a coercivity estimate for
this operator family on functions that are odd with `f′(0) = Hf(0) = 0`, in the weighted space
`∫|f|²φ` with `φ = (1 + y²)²/y⁴`, and their conclusion is a gap of `1/2`. At `a = 0`, by their
own §1, the object *is* CLM. **The trial space is theirs, the weight is theirs, and the `−1/2` is
theirs.** Reproducing a published theorem numerically is not a new theorem.

What is unpublished — and all this leg reports — is the **measurement**: leg 111's own gate,
re-asked on this repository's own operator and quadrature, on a trial space whose vanishing order
is not `1`.

Four classes were named in a novelty log committed **before the module was touched and before a
single number existed**:

| class | constraint | measured vanishing order | admissible `γ` |
|---|---|---|---|
| `T0_unconstrained` | none | **`0.99999993`** | `< 3` — leg 111's own |
| `T1_dprime` | `Σ k c_k = 0` | **`2.9999999`** | `< 7` |
| `T2_egm` | that **and** `Σ_{k odd} c_k = 0` | **`2.9999997`** | `< 7` |
| `T3_hilbert_only` | `Σ_{k odd} c_k = 0` | **`0.9999991`** | `< 3` |

The orders are *measured* by log-log slope, not asserted. `T3` is the falsification control, and
it is why this isn't a tautology: it deletes a direction from the trial space exactly as `T1` and
`T2` do, but it doesn't change the vanishing order — so if the window opened for `T3` too, the
instrument would be measuring "I removed some directions" rather than "the space changed," and
the whole result gets withdrawn instead of shipped.

## Two things fell out before the main answer

**One: EGM's published weight is a member leg 111's own family excluded.** Transport
`(1 + X²)²/X⁴` through `X = tan(θ/2)` and it is leg 111's family `B` at `γ = 4`, exactly — the
pointwise ratio is the constant `32` to a relative spread of **`2.0e−15`**. Leg 111's family `B`
stopped at `γ = 2` and its family `A` at `γ = 4`. **The published weight was one slot past the
end of the ladder.** This is a statement about an enumeration, not a new weight class, and it was
predicted in writing before it was measured so the run had a chance to refute it.

**Two: that weight is the one that makes the damping constant.** For EGM's weight the damping
factor `D_φ` is identically `−1/2` in `θ`, to `4.441e−16`. For Chen–Hou's `γ = 4` it swings by
`1.0`. That is the arithmetic reason EGM's constant is `−1/2` rather than something near it.

## The answer

On `T2_egm` — the class carrying **both** EGM hypotheses — with EGM's own weight, at
`n = 32, 64, 128, 256`:

`+0.500000  +0.500000  +0.500000  +0.499999667`

Positive. Grid-stable: the last two relative refinement steps are **`5.890e−07`** and
**`7.409e−08`**. Admissible on the constrained space with ratio **`1.000000`** where leg 111
banked **`1.677722e+07`** (divergent) on the unconstrained one. Exponent margin **`+3.0`**. Under
Xu's published ceiling of `0.5`, and the local half of the form supplies **`+0.499999667`** while
the nonlocal Hilbert half supplies **`−1.4e−14`**.

Side by side:

| | leg 111 (`p = 1`) | leg 178 (`p = 3`, `T2_egm`) |
|---|---|---|
| window vs `γ > 3` | `(3, 3)` — **width 0.0** | `(3, 7)` — **width 4.0** |
| admissibility ratio at `γ = 4` | **`1.677722e+07`** divergent | **`1.000000`** convergent |
| exponent margin at `γ = 4` | **`−1.0`** | **`+3.0`** |
| best admissible gap | **`−0.4999241`** | **`+0.499999667`** |

**Leg 111's zero-width window is a property of leg 111's trial space, not of the operator.** The
controls agree: the falsification control `T3` passes **0** rows at `γ > 3`, and the reproduction
control reproduces leg 111's four banked values to `1.7e−07`.

## The part where the leg refused to answer its own question

Here is what makes this leg worth reading twice.

Its own pre-committed pass predicate had five clauses, and on the winning row it scored **four
out of five**. The one that failed was clause 3 — sweep the quadrature grading depth over
`{12, 24, 48, 96}` and demand the answer barely moves — and it failed only at the deepest depth,
`n_grade = 96`, where the gap reads `−230.7`.

The leg knew exactly why. At depth 96 the innermost quadrature panel sits at `θ ~ 3e−31`, and the
order-`θ³` cancellation that *defines* the constrained space is smaller than float64 can
represent there. The runner had built its own contamination diagnostic for precisely this, and it
reads:

| `n_grade` | 12 | 24 | 48 | **96** |
|---|---|---|---|---|
| contamination | `2.5e−21` | `1.0e−17` | `1.7e−10` | **`3.1e+03`** |

At depth 96 the roundoff floor exceeds the signal by **three thousand times**. Over the three
depths where contamination is below `1`, the spread is **`2.2839e−07`** — inside clause 3's own
`1e−3` tolerance by a factor of **`4.4e+03`**.

So: the gate's literal wording answered **YES**. The leg's own stricter predicate answered
**NO — 0 of 44 rows**, on one clause, at one depth, for a reason the leg could demonstrate was
about the arithmetic and not about the mathematics.

**And the leg did not resolve that itself.** It wrote:

> *I am not permitted to resolve this by relaxing my own pre-committed clause after seeing the
> answer, and I have not.*

It also would not write the NO branch's prose — *"the coincidence persists"* — because its own
measurements show it doesn't. So it did the only thing safe under both readings: took the YES
branch's **action** (escalate, don't build, don't land), pushed a branch, and parked.

**The tie was broken on 2026-08-07, by the user, not by the leg.** The ruling: the gate's literal
wording governs, the answer is **YES**, and clause 3 is **scoped rather than overruled** — it is
only ever evaluated at depths where the runner's own diagnostic says the number means something.
In the ruling's words, this is *"not relaxing a pre-registration after seeing the answer; it is
declining to read a number the leg's own diagnostic declares meaningless."*

That distinction is the whole point, and it is why the leg's refusal is preserved in the record
rather than deleted now that there's an answer. A leg that relaxes its own clause after seeing
the result has no clause. A user who scopes it, on the record, with the reasoning written down,
has made a decision that can be argued with later.

## What this does *not* mean, at some length

The ruling came with a bound attached, and it matters more than the number does.

**No weighted-energy lane opens.** Not "next", not "promising", not ranked. In the user's words:
***"Not dead" is not "open."***

The reasons are all things this leg said about itself first:

- **A gap on a constrained trial space is not a certificate.** EGM *buy* the origin conditions
  with two free modulation parameters. This leg prices nothing and proposes nothing.
- **The `+0.499999667` is EGM's `−1/2`, reproduced.** Our own novelty pass says it in as many
  words: *"The `−1/2` is theirs. Reproducing it numerically is not a new theorem."*
- **The object is the `a = 0` CLM linearisation** — one mode, analytic, the friendliest thing in
  this repository, and the one whose `Y₀` is exactly zero for a degenerate reason that is
  separately banned. A gap here bounds the real target's difficulty **from below, never above**.
- Plain float64 throughout. Nothing interval-enclosed. No stage claimed, no ban lifted, no link
  of the `L1 → L4` chain moved. Clay stays at **`~0.05%`**.

What this leg is: a **method fact**. The threshold coincidence that closed the window was an
artifact of holding one axis fixed, and now that is measured rather than assumed. That's a real
thing to know, and it is not a route.

## One more instrument finding, because it changed the answer by 21%

The first assembled run of this leg was **wrong**, and the check that caught it was built for a
different purpose.

At `γ > 3` the *unconstrained* Gram's own entries diverge — by `1.677722e+07` per grading
refinement. If you assemble that Gram and *then* project onto the constrained subspace, you are
computing a cancellation between divergent numbers, and an SVD null-space basis satisfies its own
constraint only to `1.73e−14`. Divergence amplifies that leak. Measured cost at `γ = 4` on
`T2_egm`: gap `+0.396742` instead of `+0.500000` — an error of **`1.033e−01` on a quantity whose
value is `0.5`**, understating it by 21%.

The fix is an integer-coefficient basis whose constraint residual is **exactly `0.0`** in
float64, contracted against the basis functions pointwise *before* any weight is applied. And the
proof it didn't quietly become a different computation: on the unconstrained class the new
machinery is **bit-identical** to leg 111's own function, `0.00e+00` difference.

Two separate instrument failures in one leg — the assemble-then-project artifact, and the depth-96
roundoff floor — both caught by diagnostics the leg built for itself, and both reported as
magnitudes rather than swept up. That is the part worth keeping.
