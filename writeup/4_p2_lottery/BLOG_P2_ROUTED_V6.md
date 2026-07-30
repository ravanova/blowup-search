# The measurement that was measuring itself

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. Five
posts ago we started trying to turn a good numerical guess into something a
computer could certify. Along the way we've built the right space, priced it, and
found the two structural requirements it has to satisfy. This post is about
finally putting **upper** bounds on the numbers — and discovering that the obvious
way to compute one produces a confident, reproducible, completely fictional
answer. Still a toy model. Still not a breakthrough.*

## Five legs of measuring the wrong side of the inequality

Here's an embarrassing thing that took five legs to notice properly.

The certificate we're chasing needs four constants — the defect, two contraction
terms, and a curvature term. Feed them to one polynomial; if it has a positive
root, a true solution provably exists near your guess. Every constant has to be an
**upper** bound. That's the whole point: you're claiming *the error is no bigger
than this*.

What we had been computing was the maximum over a list of test functions. That's a
**lower** bound. It says *the error is at least this*. Perfectly good for
diagnosis — it's how we found the space, how we priced it, how we discovered the
quadratic term was unbounded in the wrong norm — and useless for a certificate.
The budget we'd been quoting was an upper bound built out of lower bounds, which
is not a number that means anything.

So this leg went after the real thing.

## The obvious method, and why it lies

To turn a max-over-a-test-family into a genuine bound, you use duality. Instead of
asking "how big does this get over the functions I thought to try," you ask "how
big *could* it get over everything in the unit ball," and for these norms that
question has a closed-form answer. On a grid it's a short computation: find the
worst direction, read off the number.

We ran it. It said the operator was unbounded — the number grew steadily with
resolution, `J^0.5`, clean as anything, and it kept growing through every variant
we tried. Three different ways of setting it up, every choice of the gauge
condition, same answer.

That would have been a significant negative result. It's also wrong.

Here's the problem. Our norm measures smoothness by comparing the function's
values at pairs of **grid points**. Duality goes looking for the worst possible
function — and what it finds is a spiky thing that flips sign from one grid point
to the next. Measured at the grid points, that looks tame. But a list of numbers
at grid points stands for an actual *function*, the one that interpolates them,
and that function is thrashing wildly in the gaps the grid never looks at.

We can measure exactly how wildly, by evaluating the same function on a grid six
times finer:

| grid points `J` | how much bigger its *true* norm is |
|---|---|
| 125 | 3,000× |
| 250 | 12,000× |
| 500 | 50,000× |

Growing like `J²`. A smooth function of the same type, run through the identical
test, comes back faithful to 3%.

So the "worst direction in the unit ball" was not in the unit ball. It wasn't
within four orders of magnitude of the unit ball. The unboundedness we measured
was a property of our ruler.

## The same mistake, from the other side

The uncomfortable part is that we already had a lesson banked about this, and it
pointed the other way.

Two legs ago we tested whether a certain quantity was bounded by trying random
functions of increasing complexity. They gave smaller and smaller answers, and we
nearly wrote down that everything was fine. It wasn't: the bad direction was a
specific textbook construction that random search will essentially never find. The
lesson we wrote down was **build the adversary** — don't sample, construct.

This leg is that lesson in a mirror. There, the set of directions we searched was
too *small*, and we missed a real problem. Here, the set was too *big* — it
included things that aren't functions in our space at all — and we found a fake
one. Sampling under-reports; a sloppy ball over-reports. Neither is telling you
about the operator. Both are telling you about the instrument.

That's a more useful lesson than either one alone, and it's worth stating plainly:
**before you trust a number about an operator, check that the set you optimized
over is the set you meant.**

## What actually survives

The fix is to stop asking the grid what's in the ball, and only use facts that are
true of the real, continuous ball. Two of them are enough:

- a function in the unit ball can't be bigger than the weight allows at any point;
- it can't change faster than the smoothness weight allows between any two points.

Both hold for the true norm, so any bound built from them is honest, whatever the
grid is doing. Applying them gives a computable estimate, and for the first part
of the constant it does something we've never seen in this project:

    J = 125    250    500   1000   1600
        5.536  5.531  5.528 5.580  5.631

It **stops**. A thirteen-fold increase in resolution moves it by 1.7%. That is the
first genuine, resolution-independent upper bound on any piece of this
certificate, and it sits about a factor of two above the lower bound we'd been
quoting — so for the first time we have the number *bracketed* rather than
approached from one side.

The second part of the constant is still not bounded. The estimate for it is
honest but too generous, and it's generous in exactly the way §1 explains: it's
still paying for that spiky direction. We know from the equation itself that it
ought to be finite — the inverse of this operator gains a whole derivative, which
is more smoothness than the norm asks for — but knowing and computing are
different, and this is now the sharpest open question in the whole programme.

## The piece of `Z₁` that came out clean

The other half of the leg went better.

`Z₁` is the term that measures how much your simplified model of the operator
differs from the real one. It has never been bounded here, in six legs. Out in the
far field we model the operator by a simple ODE whose inverse we know exactly; the
question is what we threw away doing that.

The answer turns out to be a two-line identity — the difference between the real
operator and the model is exactly

    h / (X(1+X²))  −  H(h)/(1+X²)

and nothing else. Checked against the full operator, it agrees to sixteen decimal
places. The first term is trivial to bound. The second needs to know how big the
Hilbert transform of an *arbitrary* unit-ball function can be far from the origin —
which is precisely the quantity that broke the previous leg, and precisely what the
smoothness part of the norm was introduced to pay for. Splitting the integral at
half-scale, the singular half gets charged to the smoothness and the rest to the
decay, and the whole thing closes.

One detail was worth the time it cost: doing this with the textbook one-sided
kernel gives a bound that blows up near the origin, where the true answer is
exactly zero by symmetry. Writing the kernel in its even form instead — the
functions here are all even — fixes that *and* recovers the sharp constant far
away (1.681 against a true 1.669). Symmetry you already know about is free
accuracy; it's just easy to leave on the table.

The resulting bound holds against every adversary we could build, with 1.1–3.0×
headroom, and it falls off at exactly the predicted rate as the far-field cut
moves out, across the whole range of the space's parameter.

## And then it moves the answer

Here's the payoff. The previous leg found a best setting for the space's two
parameters, and reported a budget about four times better than the one before it.
That optimization did not include `Z₁`, because nobody could compute `Z₁`.

Now we can, at least partly. And at the previous leg's optimum, `Z₁` comes out
between **2.3 and 4.3** — against a requirement of *less than 1*. Not close. That
setting doesn't work at any far-field cut we tested, and the reason is structural:
the term we just bounded dies off slowly there, so buying the same margin would
mean pushing the far field a hundred thousand times further out, while the other
constant is simultaneously running away toward a resonance.

Move to the other end of the range and everything relaxes. The best setting is now
roughly `α ≈ 1.2`, and the budget there is about `1.2 × 10⁻²`.

That number deserves one careful sentence, because it's tempting. The residual of
the best profile we've found at the interesting parameter value is also about
`10⁻²`. Those being the same order of magnitude is **not** a claim that we could
certify it. The budget is conditional — it prices one piece of `Z₁` and omits
three constants entirely, and every omission makes it look better than it is. What
changed is narrower and duller than it sounds: the target is no longer out of
reach by orders of magnitude. That's a different sentence from "we can reach it."

## Where this leaves things

Of the eight quantities a certificate needs here, three moved this leg from
*measured* to *bounded*. Three are still open, and they now have names and
addresses rather than being a vague "and then we'd need estimates":

- the smoothness part of the inverse's norm (the estimate is too generous, and we
  know why);
- the coupling between the compact core and the far field (a sharp cut has a seam
  where the nonlocal operator sees across it; needs a smooth cutoff);
- the discretization error of the core (measured two legs ago, never bounded).

None of this is rigorous. It's all ordinary floating point — analytic bounds with
numerically evaluated constants, checked against measurements. The
interval-arithmetic engine we built six legs ago still hasn't been pointed at any
of it, which is correct, because nothing has closed yet.

Still a 1D toy model of the boundary behaviour of a 3D problem. Still nowhere near
Clay; the odds there haven't moved, about 0.05%. What moved is that one of the
numbers is now bracketed instead of guessed, one candidate optimum is dead, and
one method has been disqualified before it could be believed.
