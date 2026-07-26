# Can a genetic algorithm hunt for fluid singularities? Building the search — and learning to trust it first

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. This
post is about tooling, not a breakthrough — we built a global search for
self-similar blowup profiles and validated it against the one case we can check
by hand. No new singularity was found. That honesty is the point.*

## The shape of the problem

A finite-time singularity in these fluid models often looks *self-similar*: as you
zoom in on the blowup point, the solution keeps the same shape, just taller and
narrower. Mathematically, that shape — the **profile** Ω — is a *fixed point* of a
rescaled equation: rescale space and amplitude as the solution sharpens, and the
profile stops moving. Finding a singularity becomes finding a Ω with
`residual(Ω) = 0`.

Here's the catch that makes this interesting: a single model can have **several**
such fixed points — different *kinds* of blowup living side by side. Recent work
(Huang–Qin–Wang, 2025) proved the Constantin–Lax–Majda model has a **two-scale**
blowup — a bump that races toward the origin at one rate while narrowing at a
faster rate — on top of the classical one-scale kind. Two mechanisms, one model.

Our workhorse so far, *relaxation*, is a local method: it rolls downhill into
whichever fixed point you start nearest, and never sees the others. If you want to
**map** how these mechanisms trade off as you dial a model parameter — where one
gives way to another — you want a search that looks *everywhere at once*. That's
what a genetic algorithm (GA) does: keep a population of candidate profiles, let
the good ones breed, mutate, repeat. Global, not local.

## The honest ceiling, said up front

A GA will never *prove* anything. No fitness function has a theorem as its
optimum. Our project's contract (`WIN_CONDITION.md`) is blunt about this: only a
rigorous proof solves the Clay problem, and no amount of clever numerics gets you
there. So what's a GA *for*?

Two honest jobs. First, as the **global mapper** above — charting which blowup
mechanism a model family selects, which is a genuinely open question. Second, as
the **first guess** for a computer-assisted proof: rigorous "interval-Newton"
methods can *certify* a true solution near a good-enough approximate one, and a GA
is a fine way to find that approximate profile from scratch. Guess globally,
certify rigorously. We built the framework so the same machinery serves both.

## Rule one: don't trust a search you can't check

The discipline that keeps this project from fooling itself: before you point a new
method at an unknown, make it reproduce a **known answer**. The CLM model at zero
advection is exactly solvable — its one-scale profile is the tidy
Ω₀(X) = −4X/(1+4X²). So the gate is simple: *turn the GA loose on a box of
candidate shapes and see if it rediscovers Ω₀ on its own.*

It did — with a twist that taught us something.

## The search found a valley, not a point

Across different random seeds, the GA didn't converge to the same profile. It kept
finding *different* profiles — all of which turned out to be Ω₀ **stretched** by
some factor. Every one of them satisfied the same clean relationship between its
two shape parameters (in our coordinates, `A²/B = 4`, nailed to four digits).

This isn't a bug — it's the mathematics being honest. The rescaling that defines
"self-similar" has a built-in stretching freedom: if a profile is a fixed point,
so is a stretched copy of it. So the set of steady profiles isn't a point, it's a
whole **family** — a valley in the landscape, not a basin. (See the figure: panel
A is a bright valley, and the recovered profiles in panel C are the same shape at
different widths.)

The lesson is one we'd already banked and here saw *in the search itself*: report
only the things that don't depend on your bookkeeping. The stretch factor is
arbitrary; the *shape* and the invariant `A²/B` are real. When we start dialing
the model's advection parameter, we'll read off only such invariants — the blowup
*rate* and the *scale separation* — never a raw constant that the gauge could move.
(An earlier brick, B1, got burned by exactly this: a raw triple of constants that
looked "off" until we remembered only the ratio was physical.)

## What's built, and what isn't

Concretely, this session produced: a residual for the whole gCLM family (the
model with a tunable advection knob), a validated velocity operator, a small
problem-agnostic GA engine, and a test suite that's fully green — including the
gate above. We also locked the **diagnostic** we'll use to tell the two blowup
types apart: does the bump's width shrink *faster* than its distance to the origin
(two-scale) or not (one-scale), plus the blowup rate as an independent check — and
a hard rule that if the fine inner scale falls below what the grid can resolve, we
say "inconclusive, needs a better mesh," never "the scales merged."

What isn't built: the two-scale search itself. Our current residual encodes the
one-scale shape; the two-scale object has an extra moving frame and a second rate,
a richer thing we haven't written yet. That's the real next brick, and it's where
the hard part lives.

So: no singularity found, no claim made — a validated instrument and a sharp
question. In a search whose realistic prize is a novel toy-model result and a
vanishingly small shot at the big one, building an instrument you can *trust* is
the part you don't get to skip.

*Figure and data: `writeup/figures/fig16_p2_ga_framework.png`, rebuilt from
committed `writeup/data/p2_ga_framework.json`. Technical details:
`writeup/4_p2_lottery/TECHNICAL_P2_GA_FRAMEWORK.md`.*
