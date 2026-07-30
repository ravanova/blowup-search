# Two legs, two half-answers, and the shape of the thing we actually need

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. The
[previous post](BLOG_P2_ROUTED_SPACES.md) proved that a whole category of function
spaces can't carry the proof we're building, and pointed at a replacement — priced
using a simplified model of the equation's far field. This post tests that price
against the real thing. The price is right. But the same test found the replacement
is only half a space. Still a toy model. Still not a breakthrough.*

## The bet being checked

Last time ended with a recommendation and a number. The recommendation: stop
measuring functions by their Fourier coefficients and start measuring them by how
fast they **decay** at spatial infinity. The number: if you do that, the hardest
quantity in the certification arithmetic comes out around **13**, minimized when you
work with profiles decaying like `X^{-3/2}`.

Both came from a *model*. To get the far-field behaviour we threw away the
equation's nonlocal term (a Hilbert transform), threw away the compact middle of
the domain, and threw away the two gauge conditions — leaving a one-line ODE we
could solve exactly. Very clean. Also very easy to be wrong about: the obvious
failure mode is that the part we threw away contributes something the model can't
see.

So this leg rebuilt the whole thing without the simplifications.

## A third opinion

There's a habit in this project that keeps paying: **build the same object twice**.
It's how a sign error surfaced two legs ago. This time it's a third build.

Versions 1 through 3 all represented functions by their Fourier coefficients. That
representation *can't* express decay — a single Fourier mode doesn't decay at all
— which was the whole punchline last time. So this build is nodal: sample the
function on a grid that stretches out to `X ≈ 2500`, and measure it with weighted
sup norms that see decay directly. No shared code path with the earlier versions,
and the two builds agree to 13 decimal places on everything they both compute.

First result: the earlier findings reproduce.

| grid points | ungraded norm | decay-graded norm |
|---|---|---|
| 125 | 11.9 | 3.79 |
| 500 | 14.6 | 3.97 |
| 2000 | 17.4 | **4.07** |

Ungraded: still climbing, +1.37 every time the grid doubles, no sign of stopping.
Graded: settling down, increments halving. Two legs' worth of conclusions, confirmed
from scratch.

(A detail worth a footnote: in the old coefficient setting the bad case diverged
*linearly*; here it diverges only *logarithmically*. Same verdict, much gentler
slope. Switching to sup norms was already half the fix; the decay grading is the
other half.)

## The price is right

Now the actual question. The model said the key quantity should behave like
`2/|α−2|`, where `α` is the decay rate you're working in. Against the full operator:

| `α` | 1.2 | **1.4** | 1.5 | 1.6 | 1.7 |
|---|---|---|---|---|---|
| full operator | 3.81 | **3.54** | 4.07 | 5.06 | 6.58 |
| the model's prediction | 2.50 | 3.33 | 4.00 | 5.00 | 6.67 |

In the window that matters — around `α = 1.5`, where last leg's optimum landed —
the model is within **6%**, and within 2% over part of it. Everything we threw away
was worth almost nothing. The final number comes out at **13.4**, against the
model's predicted 13.3.

That's a good outcome, and not a foregone one. It means the cheap analysis was load-bearing.

There's also a bonus. Look at the full-operator row again: it has a **minimum**, at
`α ≈ 1.4`. The far-field cost climbs as you approach `α = 2` (there's a resonance
there — it's the profile's own decay rate). The core cost climbs as you approach
`α = 1`. Last leg found an interior optimum from two constants pulling opposite
ways; the same shape now shows up in a completely different quantity, driven by a
completely different pair of mechanisms, and lands in the same place. When two
independent arguments put the answer at 1.4–1.5, that's worth trusting.

## And then the other shoe

The certification needs two things from a pair of spaces. One is that you can
invert the linearized equation — that's everything above, and it now works. The
other is that the equation's **nonlinear** term is under control.

The nonlinear term is `h · H(h)`, and there's a classical fact standing right in
front of it: **the Hilbert transform is unbounded on the space of bounded
functions.** Take a bounded function with a jump; its Hilbert transform has a
logarithmic blow-up at the jump. No amount of decay weighting escapes that, because
the blow-up happens at a perfectly ordinary interior point where the weights are
just numbers of order one.

So the decay-graded space, which fixes the inverse, does not control the
nonlinearity. Measured with the textbook adversary — the partial sums of a square
wave, which stay bounded while their conjugates grow like `log m`:

| degree | 4 | 16 | 64 | 256 | 512 |
|---|---|---|---|---|---|
| the constant | 0.74 | 1.26 | 1.81 | 2.40 | **2.73** |

Up and up, +0.41 per e-fold. Unbounded.

### The mistake I made, which is the interesting part

The first version of this test didn't use the square wave. It used **random**
perturbations of increasing complexity — a reasonable-looking way to search a
function space. Those numbers came out like this:

| degree | 4 | 16 | 64 | 256 | 512 |
|---|---|---|---|---|---|
| random sampling | 1.40 | 1.08 | 0.87 | 0.84 | 0.84 |

They go **down**. Random sampling reported the nonlinear term as comfortably
bounded, converging nicely, no problem here. It was wrong, and it was wrong in the
most dangerous direction: it agreed with what I wanted to be true.

The bad direction is a measure-zero cusp in the space. You do not stumble onto it.
You have to know it's there and go build it.

This is the same lesson this project keeps relearning in new costumes: two legs ago
it was "a divergence is a suspicion, a divergence that vanishes when you remove one
feature is an attribution." Here it's: sampling can refute a proposed bound, and it
can give you a lower bound. It can never establish boundedness, and it certainly
can't reveal unboundedness. For that you need the construction.

## The shape of the thing we need

Put the two legs side by side.

> **Last leg:** a weight on Fourier coefficients measures *smoothness*. We needed
> *decay*.
>
> **This leg:** a weighted sup norm measures *decay*. We also need *smoothness*.

Two attempts, two one-parameter families of spaces, each one missing exactly what
the other has. The far-field transport term demands a decay grading; the Hilbert
transform demands a smoothness scale. The space this proof needs has to carry
**both at once**, and neither family does.

That's not a defeat — it's the first time in four legs that the requirement has been
stated completely. The natural candidates are known (weighted Hölder spaces, where
the Hilbert transform *is* bounded, carrying a decay weight). And the rule that has
now paid for itself twice applies again: settle it on paper before writing any more
solver.

## The scoreboard, unchanged

The best conceivable certification budget from these numbers is about `2×10⁻²`. It's
a *ceiling*: it assumes one whole term is zero (it isn't — it's measured shrinking
like `J^{-2.4}`, but it isn't bounded), and it prices the decay half of the space
without the smoothness half. The interesting case has an error floor of about `10⁻²`.

Thin. Thinner than last leg's number, because last leg's number was itself a ceiling.

Everything here is ordinary floating point. Nothing is certified. This is still a
one-dimensional toy model of the boundary behaviour of a three-dimensional problem,
and even complete success would be a computer-assisted result about a profile we can
already write down in closed form. The odds on the actual Millennium problem remain
about 0.05%.

What four legs of this have bought is a map: the naive space is a cliff, the obvious
detour is a cliff, the replacement is real but only half-built, and we now know
exactly what the other half has to do.

---

*Figure: `writeup/figures/fig22_p2_route_d_v4_graded.png`. Data:
`writeup/data/p2_route_d_v4_graded.json`. Technical version with the gates and the
full tables: [TECHNICAL_P2_ROUTED_V4.md](TECHNICAL_P2_ROUTED_V4.md).*
