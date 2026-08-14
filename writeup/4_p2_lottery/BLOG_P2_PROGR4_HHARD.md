# We stopped blaming the search and pointed the instrument at the flow itself (PROG-R4, unit E)

For several runs now this project has been failing to find eight specific published orbits in a
turbulent flow, and each time the post-mortem has come back with the same shape of answer: *the
starting guesses weren't good enough.* First the pool was too shallow. Then it was filtered on the
wrong property. Then it was [stratified properly](BLOG_P2_PROGR4_SHIFT_STRATA.md) and the count was
still zero.

At some point that stops being a diagnosis and starts being a habit. There are two very different
things it could mean:

- **"supply"** — we failed because the guesses we handed the solver were bad, or
- **"hard"** — we failed because these particular orbits are hard *in our version of the flow*,
  no matter how good the guesses are.

Every run so far has been unable to tell those apart, because every run drew its guesses from the
same mine. This unit was built to separate them, by doing the one thing none of the previous runs
could do: **take the published numbers and start the solver right at them.**

## The thing you have to be honest about first

A published table row gives you a **period** and a **shift**. It does not give you a flow field.

That sounds pedantic and it is the whole ballgame. You cannot "start at the published orbit"
because nobody published the orbit — they published two numbers describing it. What you can do is
take a field out of your own simulation, pin the period and the shift to the published values, and
hand *that* to the solver. It is the strongest starting guess available and it is **not** the
published orbit, and this unit committed in advance to never blurring the two.

Sixteen of those seeds, eight published rows, two ways of picking the field for each. Written down
before anything ran, along with the four possible outcomes and what each would mean.

## What happened

**Two of the sixteen converged. Neither converged to the orbit it was aimed at.**

| aimed at | period | shift | landed at | period | shift |
|---|---|---|---|---|---|
| UPO35 | 18.912 | 0.707 | | **22.036** | **0.135** |
| UPO9 | 14.776 | 0.295 | | **16.537** | **0.099** |

To count as a recovery, both numbers had to land within 0.05. They missed by 3.1 and 1.8 on the
period, and 0.57 and 0.39 on the shift. These are real, fully converged solutions of our flow —
residuals of one part in a billion and better — they are just not the ones we were aiming at.

And look where they landed. Both at a shift near 0.1, from seeds pinned at 0.707 and 0.295.

That is the same destination the last two runs kept arriving at, and this time the solver was
*started at the published values themselves.* The pull isn't coming from the menu of starting
guesses. It survives having the menu removed.

The closest anything got to a named orbit was a run at UPO35 that finished with the period off by
0.036 — inside tolerance — and the shift off by 0.085, just outside. It is tempting to call that a
near miss. It isn't: that attempt **stalled**, with a residual of about ten. Being near a published
orbit in the two numbers and being a solution of our flow turn out to be different things.

## Three smaller findings, all slightly uncomfortable

**The better-looking seeds did worse.** One of the two ways of choosing a field explicitly matches
the published shift; the other just picks the best-scoring candidate and ignores the published
numbers entirely. The shift-matched arm started closer in **eight rows out of eight** — and
finished further away in almost all of them. Both convergences came from the arm that wasn't trying
to match.

**Starting at the published numbers gave us a *worse* starting point than our own mining does.**
Our mined guesses start with an error around 14–19; these started at 20–55. That's not a knock on
the published values. It is the direct price of the fact that the row doesn't come with a field.

**Nothing ran out of iterations.** All fourteen non-convergences stopped because a pre-registered
rule detected that they had stopped descending, at 20–31 steps out of 52 available. So "buy more
Newton steps" is not the missing ingredient, whatever else is.

## Does this mean the orbits aren't there?

**No, and the report says so in about six places.**

It means something narrower and, honestly, more interesting. A previous attempt at these same rows
— smaller simulation, cruder solver — failed all five of its tries by *refusing to move at all*,
stuck at residuals of 22 to 29. This run, with a much bigger simulation and a proper trust-region
solver, got residuals of **0.8 to 10**, from *worse* starting points, and converged twice. It went
substantially further into the problem.

And it recovered nothing.

That is the first evidence in this programme pointing at the **flow we're simulating** rather than
the **budget we're spending**. Our version — a 24 × 24 grid, a first-order-in-time splitting — may
simply not host these orbits in a form our solver can reach, and no amount of better guessing fixes
that. The published orbits live in the authors' discretisation, not ours.

Which is a claim we can only make weakly, because sixteen attempts is sixteen attempts. The honest
version of the question needs ten independent fields per row (~91 core-hours) or a resolution lift
to a 48 × 48 grid (~730 core-hours, plus a simulation we haven't run). Both are priced in the
report and neither was bought. **Zero out of sixteen is a result about our flow at our budget, and
it is not an answer about the published orbits.** The gate about those stays open and
under-resourced, exactly where it was.

## The part that makes the zero mean anything

A null from a broken instrument is worthless, so three controls were planted.

One had to succeed: a solution we can write down in closed form, nudged off itself. It converged.
One had to fail: the same period and shift with the flow field scrambled. It failed. And one had to
prove the *matching rule* still works — take an orbit a previous run genuinely found, perturb it,
and see whether this unit's own machinery says "recovered". It did, to seven decimal places.

That last one is the important one. The rule that returned zero recoveries is demonstrably capable
of returning a recovery. The zero is a measurement, not a bug.

Two other diagnostics ran alongside, each also with controls that had to fire in both directions,
and one of them is worth flagging because it *didn't* say what would have been convenient. The
solver's trust region binds on 29 accepted steps out of 30, and 98% of the drift toward low shift
happens on those constrained steps — which looks damning until you check whether constrained steps
actually drift *faster*. They don't; the difference is indistinguishable from noise (p = 0.93). So
the tempting story — "the trust region is dragging us downhill" — was available, was tested, and
was declined.

## What it costs to say this

The unit was budgeted at about an hour of compute. It took nine, and the reason is worth recording:
the cost model was calibrated on bad guesses, which fail fast and cheap. **A plausible guess is
expensive precisely because it doesn't fail quickly.** Something to remember the next time
somebody prices a search off the telemetry of a search that wasn't working.

The host also killed the run twice mid-flight. The second kill cost nothing, because after the
first one every attempt started checkpointing itself.

And none of this moves the Millennium problem this repository is ultimately aimed at. Those odds
stay where they have been, around 0.05%. What changed is a diagnosis: for three runs we have been
blaming the search, and the search just got handed the best starting guesses it will ever get and
went somewhere else anyway.

---

*Produced and checked in a single session with no independent reviewer, and therefore labelled
UNVERIFIED under this project's own rules. Verification is a fresh pair of eyes or it is not
verification.*
