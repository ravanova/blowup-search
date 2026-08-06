# Four things we learned by failing to build a proof

**Draft, for review. Nothing here is new to the world — the contribution is arrangement.**
Technical version with every number and its source:
[`TECHNICAL_P2_PUB1_V1.md`](TECHNICAL_P2_PUB1_V1.md).

---

We spent seven successive work-legs trying to build a computer-assisted proof — a *certificate*
— for a one-dimensional fluid model. We did not build one. This is about what was left over,
because the leftovers turned out to be more portable than the attempt.

A certificate of this kind needs four constants, and one of them, `Z₁`, has to come out below
1. Ours did not. The useful part is that we now know **four separate reasons why**, each one
attached to a different decision a practitioner has to make. Three of the four are about
*method* rather than about our particular equation, which is why they are worth writing down at
all.

---

## 1. You cannot pick a space that does both jobs

The first decision is which function space to work in. Ours was a weighted sequence space:
you pick an exponent, and the weight decides how much you care about high-frequency
coefficients.

The certificate needs two things of that weight, and it turns out they pull in opposite
directions **by exactly one power** — and the gap is *conserved*. We measured the two growth
exponents across the whole family of weights. Their sum is at least 1 everywhere, and exactly
1 across the whole interesting range. The measured minimum over the entire family is **0.98**.
A certificate needs the sum to be 0. There is no weight that works, and the choice of weight
only decides which of the two requirements pays the bill.

The reason is a category error that is easy to make: a diagonal weight on Fourier coefficients
measures **smoothness**, and what the far field of this operator needs is **decay**. Those are
not the same thing. A single mode `cos kθ` equals `±1` at the far edge — it does not decay
*at all*, for any `k`, and no diagonal weight can see that.

**The control is what makes this an attribution rather than a hunch.** Our operator has a
degenerate factor that vanishes to second order at one point. Delete it — change nothing else —
and the exponent sum drops from 0.98 to **exactly 0.00**, the two requirements overlap on a
full unit strip, and the same machinery has an admissible space immediately. So the obstruction
belongs to *this operator's far-field degeneracy*, not to the method and not to the choice of
sequence space.

*Searched for in the literature at full-text depth and not found. The nearest published cousin
is a Chen–Hou paper with a weight tension of the same genre in a different space — and theirs
is resolved by a choice, where ours is a no-go over a whole class. Any write-up has to cite it
and say what differs.*

---

## 2. The trap: a bound that is true and useless

The second decision is how to actually compute an operator norm. The textbook move is duality:
maximize over the unit ball. On a computer you maximize over the *discretized* unit ball.

**That is unsound, and it fails silently.** A discrete Hölder seminorm only looks at grid
nodes. So the maximizer that duality hands you is a sawtooth — a sign pattern that alternates
between adjacent nodes. On the grid it looks perfectly well-behaved. Interpolate it back to the
continuum and its norm is enormous.

We measured the inflation:

| grid points | inflation of the dual maximizer | a smooth function, same code path |
|---|---|---|
| 125 | **×2 994** | ×1.027 |
| 250 | **×12 233** | ×1.027 |
| 500 | **×49 699** | ×1.027 |

It grows like the **square** of the grid size. This is not a constant-factor nuisance you can
absorb — refining the grid makes it *worse*. Meanwhile the smooth control stays flat at 1.027,
so the failure is in the maximizer, not in the norm evaluation.

The rule that comes out of it: never let a rigorous step depend on values at grid points alone.
A coefficient expansion determines a function everywhere; a table of node values does not.

*Also searched and not found — though the surrounding mathematics is published (there is a
whole literature on when a norm sampled at finitely many points controls the continuum norm,
and its headline is that this degrades as smoothness drops). So this is a concrete instance of
a known phenomenon, and should be presented as one.*

---

## 3. A genuine theorem, and a warning about which version to quote

The third decision is the shape of the approximate inverse — the matrix `A` you multiply by to
make `I − AL` small.

**There is no such `A`.** For this operator, in this space, `Z₁ ≥ 1` for **every bounded
choice**. That is a theorem, not a battery of failed attempts.

The argument has two halves and only one is ours. The first is folklore that every paper in
this area states in one form or another: if `A` is bounded, then `Z₁` can only get below 1 by
borrowing against the smallest singular value of `L`. The second half is the content: we showed
that smallest singular value **goes to zero** for this operator in this space, and we did it
with an *explicit* sequence written down by hand rather than found by a search. It reproduces
the numerical optimum to twelve digits, and its entire residual sits in **one row**.

**And here is the warning.** We banked this result twice. The first version proved it only for
approximate inverses with one block set to zero. The second version proved it for **all** of
them, by a different and simpler argument. **The second supersedes the first**, and anyone
citing the first is citing a weaker theorem than we actually hold. The older version is kept in
the technical note because its sharpness control is still the best one — it varies the
dissipation, and shows that adding a little makes the whole obstruction disappear, so the
hypothesis is doing real work.

**The scope line matters more than the theorem.** While we were working, a paper appeared
proving that the *same operator*, in a *different* space, is perfectly invertible with a
spectral gap. So this is a statement about **our realization**, never about the operator. We do
not say, and may not say, that this operator has no bounded approximate inverse.

---

## 4. Knowing when to stop

The last decision is when to quit. Our plan had one stage left: *search* over spaces, splits
and constants for a certificate the hand-tuning had missed.

Instead of running the search, we enumerated it. **1,686 configurations; 1,686 already covered
by something we had banked; zero uncovered.**

More interesting than the coverage is the accounting. Measured in decades of `log₁₀ Z₁`, from
where hand-tuning started to where a certificate closes:

- required: **1.019** decades
- delivered by all our tuning: **0.067** — about **6.6%**
- headroom we never searched: **0.171** — about **16.8%**
- owned by **structure**: **0.781** — about **76.6%**

So there genuinely was unexplored space: tuning had reached only 28% of its own ceiling. It
would not have mattered. A *perfect* search still lands at `Z₁ ≥ 6.04`, six times short. And on
the class where we have a theorem, the searchable headroom is exactly **zero**.

**One thing we are careful not to say.** Automated certificate synthesis is published as *sound
but not complete*: a search that fails tells you nothing about the model. So the claim is that
we exhausted **our own declared enumeration**, and never that no certificate exists.

---

## 5. Two loose ends we are not tidying up

**A literature check that moved two numbers in opposite directions.** We had been carrying two
constants attributed to a 2020 paper, neither ever checked against it. Reading it settles both.
The scaling exponent is *more* firmly the literature's than we had recorded — it is an exact
closed-form solution, on the page three separate ways, and we re-derived its residual to
`8e−16`. But the *count of independent sources* was inflated: the three citations we had been
treating as independent confirmations share three authors and one ancestor. The other constant,
a critical parameter value, is genuinely that paper's — but it comes from **numerics that stop
converging right at the value in question**, with the authors' own stated accuracy being "at
least 5 digits." It should be quoted as that, not as the seventeen digits that get printed.

**A corner our audit does not cover, and we do not know what it means.** Later work found a
setting — a compactly supported profile in a global Chebyshev basis — where `Z₁` comes out
**below 1**: 0.27 and 0.087 at one parameter value, 0.74 and 0.23 at another. That looks like a
counterexample to §3, and it is not: §3's theorem needs the operator's tail to have a kernel,
and in this setting it demonstrably does not, so the theorem simply does not reach here.

But it *does* sit outside the enumeration of §4 — and here is the honest problem. The audit of
§4 was performed on a different object, one that **has no compact support at all**, so this
corner does not exist there. "The audit's completeness claim is reversed" and "the audit's
completeness claim was always scoped to an object where this corner is empty" are **both fair
readings of the same measurements**. That has not been resolved, and this note does not resolve
it. It also comes with a caveat we will not bury: the sub-1 values hold at **two of four**
choices of a gauge, not all four, and this is one constant of four, not a certificate.

We are stating it as it landed, unsoftened and unstrengthened, because that ambiguity is
exactly the kind of thing that gets quietly rounded off between a lab notebook and a paper.

---

## What this is not

It is not a certificate, not a theorem about Navier–Stokes, and not progress on the hard
problem. The object throughout is an already-solved, already-published toy model, and every
number bounds the real difficulty **from below**. Our 1D/2D restriction, incidentally, is not a
self-imposed limitation — as far as we can find, no published work machine-certifies a
singularity for anything with three spatial variables. (The usual way of saying that is wrong,
though: validated numerics *has* certified genuinely 3D objects. What it has not certified is a
3D **singularity**.)

Three of the four results here are about method. That is the reason to write them down: the
next person to reach for a weighted sequence space, or a dual norm over a discrete ball, or a
block-triangular approximate inverse, should not have to spend six legs finding out.
