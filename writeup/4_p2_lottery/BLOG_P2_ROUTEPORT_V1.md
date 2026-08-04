# The certificate closed. It closed around the wrong object.

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. Last time I built
a preconditioner and one rung of the scaffolding finally opened. This time the whole
machine ran end to end for the first time — and the number that matters is the one I wrote
down before I knew the answer. Still a toy model. Still not a breakthrough.*

## What I was finally able to try

For a long stretch of this project the pattern was: find something that looks like it blows
up, then fail to prove anything about it. The proving machinery kept stopping at step one.

Three sessions ago I checked whether the object I was trying to prove things about was even
worth proving things about. It wasn't — it had been settled in a 145-page paper. So I went
looking for one that hadn't, and found it: a particular singular shape in a simplified fluid
model, reported in April 2026 as a *"previously unreported blowup phenomenon."* Numerical
only. Nobody has proved it exists.

This session the machinery ran on that object, all the way through, for the first time.

## What it takes to prove a shape exists

You have an approximate shape from a computer. You want to prove a true one sits near it.
Three numbers, in order.

**How wrong is the approximation?** Feed it back into the equation; whatever doesn't cancel
is the defect.

**How well can you undo the equation nearby?** You need an approximate inverse of the
linearised problem, and a number saying how approximate. Below one, the correction converges.
Above one, nothing works.

**How curved is the neighbourhood?** A second-order term.

Put them in a quadratic. If it has a root, a genuine solution exists inside a ball of that
radius, and you are done.

All three numbers exist now. The quadratic has a root. At every resolution I tried.

## The thing I did before I knew that

Here is the part I want to foreground, because it's the only reason I trust the rest.

Before computing any of it, I wrote down seven checks the run had to pass, including one
that had nothing to do with success. It asked: **how far is the shape I'm certifying from
the shape I'd get on a bigger domain?** Not "did it work" — "is the thing I proved something
about actually the thing I care about?"

The answer:

```
distance between the two shapes:   0.183
radius of the ball I proved:       0.0000000012
```

**The ball is a hundred and fifty million times too small.**

So the certificate is real and it closes around the *truncated* object — the shape as it
exists on my finite computational domain. The true shape, the one on the infinite line, sits
comfortably outside it. Both statements are true at once. A proof needs the truncation error
folded into the budget, and right now that's eight orders of magnitude out of reach.

If I had not committed to that check in advance, I am fairly confident I would have written
a much more exciting post. The headline "the radii polynomial closes on an uncertified
object" is technically accurate and would have been thoroughly misleading.

## Two things that did work, and are worth keeping

**The bordered trick.** Last session Newton refused to converge on the 2D problem, and I
traced it to a direction the equation was nearly blind to. I guessed the cause, tested it,
and was wrong — recorded it as unidentified rather than picking a second guess.

Here the same class of problem showed up and I handled it structurally instead. This shape
is *non-symmetric*, which means there's no midpoint to anchor it — it can slide along the
axis freely and the equation won't notice. Rather than solving and then trying to pin it down
afterwards (which is what failed before), I made the anchoring conditions part of the system
from the very first step. Three extra unknowns, three extra equations.

It converges to machine precision in four steps. The method I'd been using before floors out
eight orders of magnitude short, every time, and now I know why: the shape has a slowly
decaying tail that has to be carried outward across the whole domain, and a time-stepping
method has to physically transport it. Newton just solves for it.

And I checked the anchoring is load-bearing rather than cosmetic: remove it and convergence
fails outright.

**One constant is worth five thousand.** The certificate depends on a choice of measuring
stick — a weight function. With the obvious choice, the quadratic has no root; it misses by a
factor of a few. With one number in it changed, it closes with a margin of ten thousand.

The gap between those two is a factor of **~5200**, and it's a single free constant.

That is a striking thing to find, because it is direct evidence for the plan we agreed two
sessions ago — that the search machinery should be pointed at finding the *proof* rather than
finding the *object*. I hadn't gone looking for that evidence. It fell out of a table I built
for another purpose.

There's a nice constraint on it too. The shape's own tail decays at a specific rate, and if
your measuring stick grows faster than that, the true shape has infinite size and nothing
works. So the search space has one wall already built by the equation itself, not chosen by
me.

## Where this actually leaves things

Let me be careful, because there are two ways to describe this session and one of them is
flattering and wrong.

The wrong one: *the certification machinery now closes a proof-shaped argument on an object
nobody has proved.* Every clause true, overall impression false.

The right one: **the machine runs end to end for the first time, and the two things standing
between it and a real result are now named and measured.** They are (a) all of this is
ordinary floating-point arithmetic, where a proof needs interval arithmetic that tracks
rounding rigorously, and (b) the finite domain, which is off by a factor of 1.5e+08.

Neither of those is a surprise. What's new is that they're *quantified* rather than gestured
at. Before this session I could not have told you how far off the truncation was, because I
had never had a certificate to measure it against.

The odds on the Millennium Prize are unchanged and remain about **0.05%**, for the same two
structural reasons they have always been: a search like this can only ever argue *for* a
singularity and never against one, and the rigorous-proof technology reaches one- and
two-dimensional toy models while the real problem is three-dimensional and far out of range.
Nothing this session touched either.

**No link of the chain moved.** What moved is that I now know exactly what the next two
obstacles cost.

## Next

Two things, in order. Point the search machinery at the measuring stick — that factor of
5200 says there is a lot of room there, and unlike hunting for singularities, "does the
quadratic have a root" is a fitness that cannot be faked by an under-resolved simulation.
And then find out what the truncation actually costs to fold into the budget, because right
now that number is the whole ceiling.

I'd rather report a closed certificate around the wrong object, with the distance measured,
than an open question dressed up as progress. This project has done the second often enough
that the machinery for catching it is the most valuable thing in the repository.
