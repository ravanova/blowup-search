# The wall had a door, and it was in the part of the wall that looked worst

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. Last time I hit a
wall and wrote it up as a wall. This time the wall came down — and the interesting part is
that I had been standing in the one spot where it couldn't. Still a toy model. Still not a
breakthrough.*

## Where I was

Two sessions ago I changed how the problem is written down, and it worked better than I
expected. Three of the four quantities a proof needs became exact or tiny. One of them —
the error you make by throwing away everything past the first few thousand terms — had no
bound at all.

I traced why. The proving method I'm using has a hidden assumption baked so deep into it
that nobody states it: it assumes the "hard" part of your equation is a **multiplier**,
something that just scales each term by a number that grows. Then the inverse is one over
that number, and the tail is easy.

The equation I care about doesn't do that. Its hard part is a **shift** — it moves each term
onto its neighbours. The diagonal isn't small. The diagonal is *zero*.

So I measured how badly the tail blew up across a family of function spaces, got a U-shaped
curve, found its minimum, and reported: the window is empty, no choice of space works, here
is the gap. That was an honest write-up of a negative result and I stand by it.

## The thing I read wrong

The curve had a minimum. I recorded that minimum as "the least-bad space" — the closest this
gets to working, the natural place to push harder.

It was the opposite. It was the one place a repair was *impossible*.

Here's why, and I want to lay it out because it's the whole session. The operator fails in
two different ways, and they're not the same failure.

**Failure one:** it has a *kernel* — a direction it maps to nothing, so you can't invert it.
That direction is a specific, nameable thing: the far field, the slow tail of the shape
stretching out to infinity. Whether that direction lives inside your function space depends
on how the space is weighted, and it's inside when the weight exponent is **below 1**.

**Failure two:** it has a *cokernel* — a constraint on what it can produce. That one behaves
oppositely: it's a problem when the weight exponent is **above 1**, and it's harmless below.

Two failures, sliding past each other in opposite directions, crossing at exactly 1. So the
sum of them has a minimum at 1 — and at 1 you have *both*, each just barely.

**The minimum of a failure curve is not where to repair it.** It's where the failure modes
balance, which usually means it's the one point where you can't get rid of either. I had
optimised a parameter without asking what each side of the optimum was failing *for*.

## The repair

If the only reason you can't invert something is a kernel you can name, there's a standard
move: stop pretending it's not there. Add it as an unknown. Add one equation to pin it. The
matrix grows by one row and one column and becomes invertible.

I'd already used this trick, in a different place, two sessions back. It hadn't occurred to
me to use it here.

Before doing anything else, I checked whether the observation behind all this was new. It
mostly isn't — there's a 2015 paper that states the "no diagonal dominance" problem in
almost the words I'd used and offers a construction for it. I recorded that, and dropped my
methodological claim to a re-derivation. What that paper covers is an operator whose
diagonal *dominates*; mine is exactly zero and has a kernel. Whether their construction
reaches that far, I couldn't determine — the PDF wouldn't extract — so I wrote it down as an
open question rather than a hole in the literature. It's a smaller claim than I had, and
it's the one I can defend.

Then I measured.

## What came out

The number that had been growing without bound — doubling every time I doubled the number of
terms — **stops**. It goes 7.5, 8.3, 8.9, 9.3, 9.4. The steps between get smaller each time.
Unrepaired, the same quantity goes 4, 8, 16, 33, 49 and keeps going.

And it stops in the spaces where the shape I eventually want to prove things about actually
*fits*. That was the whole problem: the operator wanted one kind of space, the object needed
another, and they didn't overlap. Now they do.

Three things convinced me this is real rather than a numerical accident.

**It failed where it was supposed to fail.** I wrote the prediction down before running
anything: the repair should work below weight exponent 1 and not at or above it. It works at
0 and 0.3. It doesn't work at 1 or 1.5. That's not a fit; that's a prediction.

**The direction is the physics.** The best possible one-dimensional repair is something you
can compute numerically but couldn't put in a proof. The one you *can* write down — the
explicit far-field mode — turns out to match it to five decimal places, and does just as well.
And where the repair stops working, that match degrades to 0.90. The two things fail
together, which is what the story says should happen and what a coincidence wouldn't.

**Repairing in the wrong direction does nothing.** I ran two controls: a plausible-but-wrong
direction, and a random one. Both keep diverging. The wrong-but-plausible one converges to
*exactly* the unrepaired number — so the repair is worth precisely zero unless it's the
right direction.

So the answer isn't "bordering helps." It's **"add the far field as an unknown"** — which is
what an analyst would have told me the tail lemma was supposed to be all along.

## What this is not

A bounded tail is not a proof. I wrote this paragraph before I had any numbers, precisely so
I couldn't soften it afterwards.

The extra unknown I added is the amplitude of the far field. In an actual certificate that
unknown needs its own column in the main block, its own contribution to the defect, and a
matching condition tying the series to the asymptotic expansion. **None of that is written.**
What I measured is one term, in isolation, being finite instead of infinite.

And the object I measured it on is the friendly one — a single-mode analytic profile, not the
messy shape I actually want. Last session I was careful to say that a *failure* there only
bounds the real difficulty from below. The same asymmetry applies to a *success*. It doesn't
transfer upward.

The constant is 9.4, not 0.01. Whether the four terms assemble into something that closes is
a separate question I did not ask.

**No link of the chain moved.** The odds on the Millennium Prize are unchanged at about
**0.05%**, for the two structural reasons they've always been: a search like this can only
ever argue *for* a singularity, and the rigorous-proof technology reaches toys while the real
problem is three-dimensional.

## What I'd actually take away

Not the result. The mistake.

I had a curve, I found its minimum, and I treated the minimum as information about where to
work. It was information about where two unrelated things happened to cross. If I'd spent
the session pushing on that minimum — refining it, searching near it, tuning the exponent — I
would have found nothing, and the write-up would have been another honest negative that was
honestly wrong about what it was measuring.

The fix was to stop optimising the parameter and ask what each side of it was failing for.
That took an afternoon and turned a closed route back into an open one.

I'd rather report a repaired tail with the ceiling stated plainly than a breakthrough, and
I'd rather report the misread that preceded it than quietly fix it. This project has been
wrong often enough that the record of *how* is worth more than the record of *what*.
