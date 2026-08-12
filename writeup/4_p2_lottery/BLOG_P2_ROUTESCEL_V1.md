# The certificate that has to say what it is assuming

*Route-SCEL, leg 385. Companion: `TECHNICAL_P2_ROUTESCEL_V1.md`. Data:
`writeup/data/p2_route_scel_v1.json`. Figure: fig103.*

Last leg built an instrument that certifies how fast a field decays far from the origin —
not fits it, certifies it, with an error bar you could put in a proof. Then it wrote down,
in its own docstring, the reason nobody could use it yet:

> "if the caller has only pointwise samples, it must first convert them using a certified
> modulus of continuity, or a monotonicity hypothesis, and must state which."

That is the whole problem in one sentence. The instrument wants to know what the profile does
at **every** radius on a window. What any actual computation produces is a **list of
numbers** at a **finite list of radii**. Between two samples, the function can do anything.
And "anything" is not a figure of speech: from finitely many point evaluations alone, with no
assumption about the function, *every* interval containing the sampled values is consistent
with the data. There is no honest default. A converter that quietly produced "something"
would be inventing, not computing.

So this leg built the converter with the refusal built in first.

## Two hypotheses, and the machine refuses without one

You can bridge the gaps between samples in exactly two elementary ways, and the module offers
both — as **declarations the caller makes**, recorded in the output row.

**Monotonicity.** Say the profile only goes down. Then between two samples it is trapped
between them, and the sample pair *is* the enclosure. Nothing is added, nothing is lost.

**A modulus of continuity.** Say the profile can't change faster than some stated rate.
Then every point of a cell is close to a sample, and the enclosure is the sample values
inflated by that rate.

Hand the module samples and **no** declaration and it returns `INCAPACITY` — a refusal, with
a reason, and it never calls the certifying routine at all. There is no code path that
produces a decay exponent without a named hypothesis stapled to it.

## The good news: monotonicity is free

Feed the adapter a sampled power law with monotonicity declared, and the certified exponent
that comes out the far end is `7.438494264988549e-15` wide.

Leg 382's number, computed on the same window from exact analytic interval evaluation rather
than from samples, was `7.438494264988549e-15`.

Not "the same to within". The same number, bit for bit, at every exponent tried
(`p = 1, 2, 2.5, 3`), with the true exponent inside every interval. The reason is pleasant:
a monotone function's extremes on a cell sit at the cell's endpoints, which are exactly the
points you sampled, so the conversion loses nothing at all. **Under this hypothesis, a
sampled profile is as good as an analytic one.**

## The bad news, predicted in writing before it was measured

The modulus path is *sound* — it contains the truth, always — but it is **not tight, and
cannot be made tight**. Its width is set by how much the profile is allowed to move between
samples, so it falls like `1/N`: `2.10e-3` at a thousand samples, measured slope `−1.007`.
To reach the monotone path's `7.4e-15` you would need about **10¹⁴ samples**.

This was written into the pre-registration, with the number `2.0e-3`, before the module
existed. The measurement came back `2.10e-3`. So the honest headline is not "the adapter
works" — it is:

> **Monotonicity buys you leg 382's instrument at full precision. A modulus buys you a
> sound but far coarser statement, and no amount of sampling closes that gap.**

There is a second, sharper warning inside the modulus path. State your modulus in the
obvious way — "the profile changes by at most `L` per unit radius" — on a window spanning
three decades, and it dies: the allowed wobble grows with radius while the profile shrinks,
so past `r ≈ 208` the certified lower bound goes **negative** (341 of 1000 cells), and the
downstream instrument correctly answers `INCAPACITY` rather than a number. The fix is to
state the modulus in log–log coordinates instead, which the module supports. Panel C of
fig103 is that curve falling off the cliff.

## The uncomfortable part, which is the point

Here is a profile that agrees with a clean power law at **every single sample**, and wiggles
by 5% in between. Declare monotonicity. The adapter accepts it — it *has* to, the samples are
bit-identical to the honest case — and hands you a certificate of width `7.44e-15`.

That certificate is **false about the true profile**, which escapes its claimed enclosure in
all 1000 cells, by up to 5.1%.

Nothing is broken. The certificate is valid *under the declared hypothesis*, and the
hypothesis is false. That is what a conditional statement is. And it is why the module writes
the condition into the row: the two certificates — the true one and the false one — are
**numerically indistinguishable**, and the only thing that separates them is the field that
says what was assumed. A certificate whose conditionality is invisible is worse than no
certificate, because it invites you to use it as though it were unconditional.

The same trap exists on the modulus side: a profile whose *sample-to-sample* steps obey your
stated rate perfectly, while its *between-sample* excursions do not. Accepted, and wrong by
`4.8e-2` in `log f`.

Where the violation *is* visible in the samples — a sample that goes the wrong way, a jump
that breaks the stated rate by a factor of 20 — the adapter refuses and names the offending
cell. Those checks are necessary conditions, never sufficient, and the module says so.

## What we got wrong

The pre-registration predicted that the sneaky wiggle would be caught by re-sampling on a
half-shifted grid. **It isn't**, and that prediction is recorded as refuted rather than
quietly edited. The reason is embarrassingly simple: the wiggle has period exactly one cell,
so shifting the grid by any fixed fraction multiplies *every* sample by the same constant —
and a constant multiple of a decreasing sequence is still decreasing. A follow-up probe
(clearly labelled as after-the-fact) found the correct statement: detection is a
**commensurability** phenomenon, and a violating profile can hide from any *fixed* grid.
Which strengthens the leg's conclusion rather than weakening it. The hypothesis is doing the
work. The sampling never was.

## What this does and does not buy

Real sampled profiles are now admissible input to the §4 instrument — **conditional on a
named hypothesis**, with the name attached to the number.

It does not produce a profile. No profile of the target object exists in this repository, and
every input here is a planted analytic known. The first real consumer remains whatever future
unit produces a profile, and this leg claims nothing about one. The admissible-cutoff half of
the obligation is untouched. Ceiling Tier 2. Clay odds unmoved at ~0.05%.
