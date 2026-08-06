# The wall was the room, not the wall

**Draft, for review. Nothing here is new to the world — the contribution is arrangement.**
Technical version, with every number and the file it was read from:
[`TECHNICAL_P2_PUB2_V1.md`](TECHNICAL_P2_PUB2_V1.md).

> **This is the second of two drafts, and it is a different piece from the first.**
> [`BLOG_P2_PUB1_V1.md`](BLOG_P2_PUB1_V1.md) is about *why our proof attempt failed*. This one
> is about *where else it could have been attempted* — a question we could only ask once we
> knew the failure was real.

---

We spent about seventy work-legs failing to build a computer-assisted proof for a
one-dimensional fluid model. The companion piece anatomises the failure into four causes. This
one is about the question that outlived the anatomy, and about the fact that we can now answer
it.

A proof of this kind is never built on an equation. It is built on an equation **in a space** —
a choice of how you measure the size of a function. That choice is usually treated as a
technical preliminary. It turned out to be the whole thing.

---

## The obstruction was in the room, not in the operator

Our space was a weighted sequence space: take a function's Fourier coefficients, weight the
high-frequency ones by a power, add up the absolute values. It is the standard choice in this
corner of validated numerics, for a good reason — it is the space in which you can control an
infinite tail.

In that space we proved a hard negative. The key constant of the method has to come out below
1, and **it cannot**: for *every* bounded choice of approximate inverse, without exception, it
is at least 1. The reason is that our operator is not bounded below in that space at all. Its
smallest singular value falls to zero as you refine, like `M^{−(1−s)}`, and we have the
explicit sequence that drives it there — constructed rather than found, matching the
numerically optimal direction to eleven decimal places.

We checked the obvious escapes, and they are all closed. It is not the weight: the exponent is
`1 − s` at every admissible `s`. It is not where you split the operator: the answer moves by
0.29 % across every split we tried, because the divergence lives in the tail. It is not the
shape of the approximate inverse: the argument never even looks at its shape. And it is not the
repair we spent a leg building — bordering the system with an extra unknown changes the
answer by **six parts in a thousand trillion** (`5.7e−15`, relative).

**And then the same operator turned out to be invertible somewhere else.** A 2026 paper by Jie
Xu proves that our exact object — same operator, same parameter — is invertible on a *Hilbert*
space of functions on the line, with an explicit closed-form inverse and a spectral gap, once
you require a certain regularity condition at the origin.

Both things are true. They do not conflict. They separate two **realizations** of one operator.
That is the finding: **the wall we had been hitting for seventy legs belongs to the room, not
to the operator.** (The idea that an obstruction can belong to a realization rather than to an
operator is not ours — it is published, and named on this exact operator. We use it; we do not
claim it.)

---

## So we went and looked at the other room

Structurally, it is a good room. We re-derived Xu's machinery from the paper rather than citing
it, and everything a proof needs is there: the operator splits into two uncoupled halves, the
inverse has an explicit shape with an *exact* norm, and the one singular direction is rank one,
so the same bordering trick we used before fits perfectly. The residuals across those checks
are around `1e−14`. The quantity that collapsed in the sequence space is here bounded away from
zero and, crucially, **independent of the truncation** — it moves by `1.4e−04` when we widen
the computational window by four decades.

**And it is worth nothing for our actual problem.** This is the part that has to be said in the
same breath, and it is why the leg that found it escalated instead of building anything.

Every single one of those beautiful objects — the splitting, the closed-form inverse, the exact
norm — exists because the profile is the *exact* solution at one special parameter value. There
is an identity that makes it all work, and that identity is a statement about the **profile**,
not about the space. Move off that parameter and Xu proves only a conditional statement: no
inverse, no gap. Our real target is not that profile and inherits none of it.

So the honest summary of the good room is a sentence with two halves, and quoting either half
alone is a misrepresentation: **a certificate there is structurally buildable, and what it
would certify is a closed form its author has already written down.**

There is a second catch worth naming, because it will matter to anyone tempted by this route:
the operator is *non-normal*, and Xu says so in his own abstract — a spectral gap does not by
itself give a decay rate in the norm you care about. A proof in that room would certify
**invertibility**, not **stability**. Stability is what the next step of our chain actually
needs.

---

## Is there anywhere in between?

That is the obvious next thought: two rooms, one dead and one useless — what about the corridor?

The first thing we found is that **the two rooms are not on one corridor.** They differ in
three independent ways at once: one lives on a circle and one on the line; one is an `ℓ¹`-type
sum and one an `L²`-type integral; one is controlled by a weight and one by a condition at the
origin. "Interpolate between them" is not one move. Saying this precisely matters, because a
report that said "no interpolant works" without noticing it would be reporting a confusion.

So we checked the two moves that *can* be made, separately. Both are dead, and — this is the
interesting part — **they are dead for two completely different kinds of reason.**

**The coefficient move dies from an invariant.** Slide the index from `ℓ¹` toward `ℓ²` and our
negative proof does not weaken at all. The reason is almost embarrassingly concrete: the
quantity the proof divides by is supported on **exactly one entry** of a vector, and a
one-entry vector has the *same* norm in every `ℓ^p`. We measured it — moving along the scale
changes the denominator by 157 % and the numerator by six parts in a hundred trillion
(`5.7e−14`, relative).
The proof's exponent is blind to the index to within 0.009, and the number of places where
moving off `ℓ¹` rescues a case that was dead at `ℓ¹` is **zero**.

Better: the whole two-parameter family collapses into **one** parameter, `σ = s + 1/p` — which
is exactly the quantity interpolation preserves. In that variable, the two-dimensional search
we were contemplating is the one-dimensional picture we had already swept years of legs ago.
The window where both obstructions are absent turns out to be a **single point**, at every
index; and at that point the object we want to certify is outside the space by a margin of
`−0.6026` — **the same number at every index**, because both walls move by exactly the same
amount. Interpolation moves the picture. It changes nothing in it.

**The origin-regularity move dies from something that isn't a space question at all.** What
forces the special-parameter restriction is that identity about the profile. It contains no
norm, no weight, no index. Every space inherits it if and only if the profile is the exact one.
**No choice of space can supply it, and none can remove it.** That is a stronger statement than
"the candidates failed," and it is the honest one. And the one interpolation you could even
attempt — sliding the regularity index — is ruled out by Xu himself, in a sentence we named as
the likely obstruction *before* we ran the check: you cannot use the strong metric to clear the
spectrum and the weak one to close the origin channel; the two are coupled.

---

## What this adds up to

The space axis is now mapped, and it is closed.

- **The room we were in is dead**, and provably so — not by tuning, but structurally.
- **The room next door is live and holds the wrong object.** Buildable, verified, and it would
  certify something already known in closed form, for a parameter value we do not care about.
- **There is no corridor.** One half of the gap collapses to a single invariant we had already
  swept; the other half is not a question a space can answer.

The one thing that *does* transfer is not a certificate — it is a discipline. Xu's gap only
exists in the realization that enforces a condition at the origin. Every numerical object we
own for this operator sits in the realization **without** that condition, and our own capability
ledger had already recorded that fact without anyone drawing the consequence. That is
actionable whether or not a certificate is ever built.

---

## The usual caveats, which are not decoration

Our object is a well-studied one-dimensional model at a special parameter — already solved,
already published. Nothing here is a statement about the Navier–Stokes equations, and no link
of our chain to that problem has moved; none has moved in 185 legs. Every number above is
ordinary floating point at a stated truncation — **none of this is interval-enclosed or
rigorous** in the computer-assisted-proof sense, including the part we call a theorem, whose
proof is exact but whose confirming measurements are not. We did not build a certificate in the
second room; a leg to try was authorised and had not reported when this was written, and
nothing here depends on or predicts what it will find.

And one framing we are careful never to use, because it is the tempting and wrong one: *"the
operator is invertible there, therefore a proof is possible."* It is not a shortcut. It is a
different claim, and the paper that proves the invertibility declines to make it.
