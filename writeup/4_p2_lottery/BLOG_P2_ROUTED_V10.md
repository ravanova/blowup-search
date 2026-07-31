# The number we had been quoting was 50. It is 8.

*Route-D v10 of a Navier–Stokes blow-up search. Level-1 tooling plus bounds. Not
a certificate, not rigorous, not a Clay result.*

---

The previous leg ended with an admission. For ten legs this project has been
quoting brackets — *the operator norm is between 1 and 47* — and using them to
decide what to work on next. And the lower end of every one of those brackets was
computed the same lazy way: take the direction that would be extremal if the
problem were simpler, evaluate, move on.

Those directions are sign patterns: `+1, −1, −1, +1, …` scaled by a weight. They
are exactly right for a sup-norm problem. Our space also measures smoothness, and
a sign pattern is maximally unsmooth, so dividing by its norm throws away almost
everything it gained. The tell, which nobody had looked at until now: **the
baseline gets worse as the grid gets finer.** It was never converging to anything
about the operator. It was measuring how badly a jagged vector is punished.

So the bracket was uninterpretable, and — this is the part that made it urgent —
its two readings imply opposite decisions. If the upper bound is 50× too big,
sharpening it is the whole ballgame. If the operator really is that large, no
amount of sharpening helps and the lane is done. We could not tell.

## Building an adversary that belongs to the space

The fix is to ask what the unit ball actually contains. An element with finite
norm here has to decay at a fixed rate and must not oscillate. So: that decay
times a *slowly varying* shape — powers, low-order cosines, broad bumps swept over
centre and width, smoothed steps, boxes. Every candidate gives a valid lower
bound automatically, so the entire problem is construction rather than proof.

The winner is a **wide bump sitting in the far field** — centred at `X ≈ 90`, half
the domain wide. Nothing oscillatory comes close. And that is where every other
finding in this project has pointed: the far-field degeneracy that killed the
first space, the resonance that set the decay exponent, the matching radius the
budget keeps demanding. The operator's worst direction is a broad far-field
disturbance. Getting the same answer from an unrelated calculation is a small
piece of evidence that the number means something.

A random search launched from that shape improves it by 0.0%. Reported, because a
flat maximum tells you something too.

## The numbers

At the reference point the lower bound goes from 0.94 to 2.88, and the bracket
from 50× to 16×.

But the reference point is not where we work. The budget is evaluated at a
different corner of the parameter space, and has been for three legs. There:

```
2.74  ≤  ‖A‖  ≤  20.94        a factor of 7.7
```

**The bracket that matters was never 50×.** Quoting the wrong point was itself
part of the confusion — a second, quieter version of the same mistake.

## What it decides

Because the lower bound is now real, one can ask a question that was unanswerable
before: *how much is left on the table?* A perfect upper bound — one reaching the
adversary exactly — would multiply the certification budget by the bracket and no
more:

| | |
|---|---|
| budget now | 2.45e-4 |
| if the operator norm were exactly sharp | 1.88e-3 |
| the residual floor our search actually achieves | 1e-2 |

Both readings are true and both matter.

**Better than it looked.** After the honesty legs the budget sat about forty times
below the floor with no idea how much was recoverable. The recoverable part is
7.7×, which lands about **five times short** rather than forty.

**Not enough by itself.** Sharpening the operator norm perfectly does not close
the gap. It would need the nonlinear constant's own slack (about 4×) as well —
and those two together only just reach the floor, with nothing spare for the three
constants still unbounded.

That is a real, quantitative statement about a lane that has been running on
intuition for several legs, and it took one afternoon of building test functions
rather than another estimate.

## The lesson, stated plainly

A bracket is two numbers and both have to be earned. We earned one end six legs
ago and kept quoting the other as though it were free. The cost was not just
imprecision: it was a leg spent sharpening the wrong input, and a phantom "19×
available gain" that survived until someone checked what the lower number
actually was.

If you are going to make decisions from a bracket, build both ends first.

---

**Data + code:** rebuilds from `writeup/data/p2_route_d_v10_lower.json` via
`writeup/4_p2_lottery/p2_route_d_v10_evidence.py` (figure `fig28`), with the
construction in `solver/op_lower.py` and its six gates in `test_op_lower.py`.
Technical companion: `TECHNICAL_P2_ROUTED_V10.md`.

**Honest ceiling:** Level-1 tooling plus bounds. Nothing interval-enclosed,
nothing rigorous, no certificate. Overall odds on the Millennium problem from
this line: ~0.05%.
