# I made the estimate 32% sharper and nothing happened

*Route-D v9 of a Navier–Stokes blow-up search. Level-1 tooling plus upper
bounds. Not a certificate, not rigorous, not a Clay result.*

---

By the previous leg the bookkeeping was nearly done: seven of ten constants in
the certification argument were genuinely bounded, and the nonlinear term's
constant was complete. So the question changed. It was no longer *can we bound
this*, it was *are the bounds any good* — because the certification budget scales
inversely with their product, and one of them, the inverse operator norm, was
bracketed by a factor of seventy.

The obvious target was clear. The bound on that operator is a fixed point that
feeds back on itself through a bound on the Hilbert transform, and at the working
point that feedback supplies 81 of the 93 units going in. The Hilbert bound was
old — it was built two legs earlier out of textbook majorants, each one throwing
away a constant somewhere.

So I rebuilt it properly, and it got much better.

## The rebuild

Folding the integral onto the half-line gives an exact kernel with three
convenient properties. The far-field decay is *in* the kernel rather than
something you have to recover by cancellation. Its principal value integrates to
exactly zero — it is the conjugate of the constant function — which means the
singularity can be handled by one global subtraction instead of the band, the
matching scale and the leftover term the old version needed. And written in the
right variables it is numerically stable out to the far field, which the naive
form is not: near the endpoint two cosines both approach −1 and their difference
has no significant digits left. (The first version produced NaNs. That is what
they were.)

The new bound is sharper than the old at every point I sampled — a factor of
eleven near the origin, about a third through the middle range, converging to
parity far out. On the anchor profile it is within 3% of being attained, which
means it is nearly the *right* answer, not merely a smaller upper bound.

## The part I did not expect

At each point of the integral you can charge the function's variation either to
its smoothness or to its decay. Any fixed rule for choosing gives a valid bound.
The natural rule — take whichever is smaller — is what the previous leg used.

It is the wrong default, and the reason generalises:

> tune the rule to the ratio of the two quantities in the *answer*, not to 1.

In this closure the smoothness term ends up about ten times the size of the
decay term, so a rule that shifts work onto smoothness in order to minimise their
unweighted sum is charging the expensive account. Introducing a knob for that
ratio, the operator norm bowls with an interior optimum — and the neutral rule,
the natural one, comes out *worse than the crude bound it was meant to replace*.
At the optimum: 69.4 → 47.2, a 32% improvement, the largest single gain since the
closure was built.

## And then the budget did not move

2.39e-4 before, 2.40e-4 after.

The reason took one table to find. The closure raises the Hilbert input to the
power γ — the smoothness exponent of the space — and the working point sits at
γ = 0.15. So a 30% improvement in that input moves the answer by 4%. Sweeping
across the parameter plane:

| where | (1.5, 0.50) | (1.4, 0.35) | (1.4, 0.25) | (1.4, 0.15) |
|---|---|---|---|---|
| gain | 32% | 11% | 3% | 0% |

The rightmost column is the operating point. It has been the operating point for
three legs. The gain is real everywhere except where it is spent.

And the operating point sits there for a reason that makes this worse, not
better: small γ is where the operator norm is cheap *because* it barely depends
on the Hilbert input. The optimiser has already walked to the corner of the
parameter space where my improvement cannot matter.

## The measurement that should have come first

The fix for this class of mistake is one table, and it costs about a minute:
scale each input of the closure by a factor and see what comes out.

| input | elasticity at the working point |
|---|---|
| the sup-part dual bound | **+1.00** |
| the Hilbert bound (this leg's work) | **+0.11** |

The operator norm is *proportional* to the first and essentially blind to the
second. The last two legs both worked on inputs with elasticity below 0.5, and
both moved the budget by under 7%. That is not bad luck; it is that table, read
backwards, and neither leg computed it beforehand.

## One trap on the way out

The tempting next step is to ask how much is available from the input that does
matter — substitute a measured value and read off the gain. I did that, and got
a factor of nineteen, and it was wrong: the "measured" value was a lower bound
computed by dividing one part of a quantity by the whole norm of a wildly
oscillatory test vector, which puts it an order of magnitude below anything
plausible. This project has a banked lesson about knowing which side of an
inequality each number is on. Apparently having the lesson written down is not
the same as applying it.

What survives is smaller and honest: elasticity says the sup-part dual is the
input worth attacking; its own known bracket says roughly a factor of two is on
the table there; and the wider gap cannot be attributed at all until someone
builds a decent *lower* bound. That, and not another estimate, is what the next
leg needs.

## Where this leaves things

Better estimate, no better budget. Three order-of-magnitude losses when the
bounds became honest, then three legs of nothing in either direction. The
certification budget is still about forty times below the residual our actual
search achieves, everything is ordinary floating-point arithmetic, nothing is
rigorous, and the eventual success this scouts would be a computer-assisted
result about a toy model rather than the Millennium problem.

The useful output of this leg is not the 32%. It is the elasticity table, which
says the next thing to work on is the one input nobody has touched since it was
first bounded — and says it with numbers instead of intuition.

---

**Data + code:** everything rebuilds from
`writeup/data/p2_route_d_v9_sharpen.json` via
`writeup/4_p2_lottery/p2_route_d_v9_evidence.py` (figure `fig27`), with the
estimate in `solver/hilbert_pointwise.py` and its six gates in
`test_nk_hilbert_pointwise.py`. Technical companion:
`TECHNICAL_P2_ROUTED_V9.md`.

**Honest ceiling:** Level-1 tooling plus upper bounds. Nothing interval-enclosed,
nothing rigorous, no certificate. Overall odds on the Millennium problem from
this line: ~0.05%.
