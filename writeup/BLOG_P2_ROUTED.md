# We have a good guess. Can a computer *prove* it's real? First we find out if the question can even be asked.

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. Every
previous post in this series found shapes by search and measured how well they fit.
A search proves nothing — it produces a very good guess. This post is the first
step of a different kind: turning a guess into something a computer could one day
**certify**. It is deliberately not the certification. It is the reconnaissance
that tells us whether the certification is even set up right. Still a toy model.
Still not a breakthrough.*

## The ladder we're climbing

It helps to name the rungs.

- **Level 0** — reproduce a known result. (We did this early.)
- **Level 1** — a *novel numerical map*: a genetic algorithm finds an approximate
  self-similar profile and measures a residual. **Everything banked so far lives
  here.** A GA is a brilliant guesser and an honest one, but it proves *nothing*.
- **Level 2** — a *rigorous, computer-assisted statement*: a mathematical argument,
  every inequality checked by machine with guaranteed arithmetic, that a **true**
  solution exists in an explicit neighbourhood of the guess. This is the first rung
  that is genuinely *new mathematics*.
- **Level 3** — the Clay problem itself.

This post is our first brick on the Level-1 → Level-2 jump. And the honest first
question is **not** "prove the profile is real." It's the humbler one:

> *Can the proof even be set up?* Can we bound the three quantities a certification
> theorem needs — the defect, the inverse of the linearization, and a curvature
> constant — well enough that the argument would close, checked against a case
> where we already know the answer?

If the answer is "no, and here's exactly why," that's a legitimate result too.

## First: arithmetic you can trust

A Level-2 claim is only as honest as its arithmetic. Ordinary floating point
rounds, and a rounding error in the wrong direction can turn a false statement into
a "proof." So the first thing we built is a small **interval-arithmetic** engine:
instead of a number, it carries a *guaranteed* range `[low, high]` around the true
value, and every `+ − × ÷` rounds *outward* so the true answer can never escape the
interval. No libraries — it's a few hundred lines, and we gate it against exact
fraction arithmetic so we know it never lies. `1/3` comes back as a tiny bracket
straddling the true third; the enclosure of a whole vector operation is checked to
contain 64 random samples of its inputs. It's boring, and that's the point.

Then we pointed it at our known-answer case. The two-scale singularity of the CLM
model has a shape we can write down exactly — `−1/(1+X²)`, a smooth bump. Our engine
brackets its "defect" (how far it is from a perfect solution) inside a range whose
*width* is about **ten times smaller** than the defect itself. Translation: the
guaranteed arithmetic is precise enough to carry the first of the three bounds a
certification needs. One prerequisite met, with evidence.

## Then: the thing that makes the naive proof impossible

Here's where it got interesting — and where a careless attempt would have quietly
failed.

Our exact shape is not a lonely solution. Stretch it taller, or wider, and you get
*another* exact solution. There's a whole **two-dimensional family** of them, a
smooth valley of answers rather than a single point at the bottom of a bowl. Every
certification theorem needs to invert the "curvature" of the landscape at the
solution — and at the bottom of a *flat valley* that curvature is singular. You
cannot invert it. A naive attempt doesn't just fail; it fails *silently*, reporting
nonsense.

We measured this directly. The curvature has **two** flat directions — confirmed by
computing that two of its characteristic values are essentially zero. That's the
diagnosis. The cure is standard once you see it: you must "pin down" the valley
before you invert — fix the height and the width by hand, converting the flat valley
into an isolated point. Our measurement told us *exactly how many* pins are needed:
**two**. Not a guess — a count.

## The lucky break

The hard part of any such proof is controlling an operator (here, a nonlocal thing
called the Hilbert transform) across *infinitely many* scales at once. That's
usually where these attempts drown.

We got a genuine structural break. If you bend the infinite line into a circle with
the right change of variables, that fearsome operator becomes the simplest thing in
harmonic analysis: it just turns cosines into sines. We checked this holds to seven
decimal places across a range of test shapes. And in this new picture, our exact
solution isn't a complicated function — it's a **two-term** object, a constant plus
a single cosine.

The payoff cascades. Because the solution is so simple in this basis, the
linearization we need to invert turns out to be **banded** — almost diagonal, a
thin stripe down the middle plus one extra column (see panel D of the figure: the
stripe is unmistakable). Banded operators are exactly the ones these
computer-assisted proofs *can* control, because the part you can't compute directly
— the infinite tail — is tame and shrinks predictably. This is the difference
between "the proof might set up" and "the proof might set up *and close*."

## What we are — and are not — claiming

Let me be as clear as the honesty of this project demands:

- We have **not** certified anything. There is no theorem here.
- We built a trustworthy interval-arithmetic tool and *validated* it.
- We **diagnosed** the obstruction (a 2-D valley of solutions) and **counted** the
  fix (two gauge conditions).
- We found a basis where the central operator is banded, which is what makes a
  certification *plausible* rather than hopeless — and we backed every structural
  claim with a number, not a hand-wave.

The next step is a "dress rehearsal": compute the three certification bounds in
ordinary floating point first, just to see whether the argument would close at our
known-answer point *at all*, before spending the effort to make it rigorous. If it
closes, we harden it with the interval engine. If it doesn't, we'll have learned
precisely which wall it hit — and that, written up honestly, is a publishable
"here's why the obvious approach doesn't work yet."

And the ceiling, stated plainly, because this series always states it: even if this
whole line succeeds, it is a **computer-assisted certification of a toy model** —
the same respected-but-incremental genre as recent work on related equations. It is
not the Clay problem. What's genuinely new is small and specific: the certification
question for this profile now lives in a basis where its hardest operator is banded,
and we can say so with evidence. On a long-shot problem, an honest small step in the
right direction is the whole game.

---

*Figure: `writeup/figures/fig19_p2_route_d.png`. Panel A — the guaranteed
enclosure of the residual, ten times tighter than the defect it brackets. Panel B —
the two flat directions of the valley, and how fixing the wave speed removes one.
Panel C — the line-to-circle diagonalization, accurate to ~10⁻⁷. Panel D — the
banded linearized operator. Everything rebuilds from committed data with*
`python writeup/p2_route_d_evidence.py`. *Companion technical note:*
[TECHNICAL_P2_ROUTED.md](TECHNICAL_P2_ROUTED.md).
