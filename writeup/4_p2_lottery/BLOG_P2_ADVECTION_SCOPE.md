# We tuned the space on the one case where the hard term vanishes

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. Eleven
posts of this series have been about building a function space precise enough to
certify a solution in — choosing its two parameters, pricing them, bounding the
constants. This post is about a question nobody thought to ask for eleven legs, and
the answer took an afternoon. Still a toy model. Still not a breakthrough.*

## The shape of the mistake

The equation has a knob, `a`, controlling how strongly the fluid advects itself. At
`a = 0` there's an exact solution written down in closed form — which is why every
piece of machinery got built and tested there. You want a known answer to gate
against; that's good practice, and this project has a banked lesson insisting on it.

But `a = 0` is exactly the value at which the advection term **disappears from the
equation**.

So eleven legs chose a space, tuned its two parameters, priced its constants and
optimised its budget — on the one member of the family where the term that space
would eventually have to carry does not exist. Nobody checked whether it could carry
that term at all.

It can't.

## The velocity doesn't converge

The quantity that does the advecting is `U(X) = ∫₀ˣ H(Ω)`, an integral of the
profile's Hilbert transform out to radius `X`. We already knew, from three legs
back, that `H(Ω)` decays like `(∫Ω)/(πX)` far out.

Integrate that and you get a logarithm. `U` doesn't settle down — it grows like
`log X`, forever, at a rate set by the profile's total mass:

| `a` | measured growth rate | mass/π |
|---|---|---|
| 0.0 | −0.9970 | −0.9969 |
| 0.3 | −0.7544 | −0.7540 |
| 0.5 | −0.6862 | −0.6870 |

Four significant figures, and there's no escape hatch: the rate is proportional to
the profile's mass, and the mass isn't zero for anything in this family. The `a = 0`
anchor itself integrates to exactly `−π`.

The consequence is immediate. The space is defined by how fast things decay. Feed a
function from that space through the linearised operator, and the advection term
comes back multiplied by a logarithm — so the output isn't in the space the operator
is supposed to land in. Not for any `a ≠ 0`. Measured growth rate `+0.317` where the
prediction says `+0.318`, and identically zero at `a = 0`, which is the control that
makes it the advection term and nothing else.

**Eleven legs of bounds are `a = 0`-only.** That sentence had never been written down.

## Half of that measurement was noise, and it took a specific test to notice

There are two advection pieces, and my first instinct was to report both. One of
them carries `Ω_X` — the profile's slope — and for `a ≠ 0` the profile has collapsed
to the numerical noise floor by about `X = 10`. Fitting a growth rate out there
measures amplified noise dressed up as a trend.

Magnitude can't tell you which is which; both look like numbers. What separates them
is whether they **reproduce when you refine the grid**:

| `a` | transport piece | stretch piece |
|---|---|---|
| 0.3 | 0.4% | 5% |
| 0.5 | **2.6%** | **99%** |

The transport piece is built from `U`, which is set by the profile's *core* — the
part that's actually resolved — and from an analytic test function. It repeats. The
stretch piece changes by 99% when you refine. Only the first one is a result, and
the test now enforces that rather than trusting me to remember.

## The fix was already in the building

Here's what saves this from being purely a cost.

There are two ways to write the equation for a collapsing profile. The one this
project has been using — the "two-scale" traveling-wave form — balances the
stretching term against `c Ω_X`, and that balance is what fixes the space's decay
grading at `α+1`. The other, older form — the self-similar one — balances against
`c_l X Ω_X` instead. That extra factor of `X` means its natural grading is `α`.

One power weaker. And one power is exactly what a logarithm needs to be absorbed:
`X^α · (log X)·X^{−α−1} = (log X)/X → 0`.

Same profile, same test function, same grid, just the two gradings side by side:

| `a` | two-scale | one-scale | at `X = 10⁴` |
|---|---|---|---|
| 0.3 | **+0.317** (grows) | **−0.010** (decays) | 3.11 → 0.00031 |
| 0.5 | **+0.480** (grows) | **−0.016** (decays) | 4.79 → 0.00048 |

So the finding isn't "`a ≠ 0` is unreachable." It's "`a ≠ 0` needs the self-similar
formulation" — which this project has had a validated solver for since early on.

## A crossing, and being wrong about it in a useful way

Chasing this, I found that the effective speed `c + aU(X)` changes sign at a
specific radius — 7.16 at `a = 0.3`, 3.10 at `a = 0.5`, stable to about 1% across
three different grids. I wrote it up as a *stagnation point*: the far field of the
"traveling wave" moving opposite to its core. Striking, if true.

A parallel line of work had already read the same crossing better. It isn't a
stagnation point. It's the **edge of the profile** — beyond that radius the solution
is simply zero, with a specific algebraic order of vanishing.

That reading is better because it explains something mine didn't: why the profile
collapses to `10⁻⁹` by `X ~ 10` when the crossing sits at 7.16. There is no far-field
tail out there to have a sign. There's numerical dust past the end of the function.

I kept my gates written so they depend only on the part that reproduces, which is
why they survive the reinterpretation unchanged. That was luck as much as design,
but it's the kind of luck that a habit produces.

## What it costs and what it's worth

This moves nothing toward Clay. It narrows the scope of one sub-programme and names
the repair. Work that looked general turned out to be specific.

The value is in *when* it was found. Three more legs of bound-sharpening were queued,
all of which would have been built on the assumption that the space works — and all
of which would have had to be redone. The check took an afternoon because the
question was cheap once someone asked it.

The uncomfortable general version: the practice that caused this is the same one that
keeps the project honest. Gate everything against a known answer. It's right. But a
known answer is a *special* case, and the thing that makes it tractable is often
exactly the thing that makes it unrepresentative. Worth asking, next time, what the
gate case is missing.
