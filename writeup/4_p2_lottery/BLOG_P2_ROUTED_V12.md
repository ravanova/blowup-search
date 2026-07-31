# The profile ends

*Route-D v12 of a Navier–Stokes blow-up search. Level-1 tooling plus a structural
finding. Not a certificate, not rigorous, not a Clay result.*

---

The previous leg drove the candidate profile's residual down twelve orders of
magnitude and handed over a single instruction: *you measured that in the wrong
coordinates*. All the machinery that decides whether the argument closes — the
operator norms, the constants, the budget — is written in a different, compactified
discretization. Carry the profile across and measure the defect there.

I carried it across. The measurement took about an hour. Then it took the rest of
the leg to understand what it was saying, and the answer was not about the
defect.

## The thing about a Newton solve

A Newton solve drives the residual to zero *at the grid points*. The certificate
does not care about grid points. It cares about the residual of the underlying
function, everywhere — and those are different, for a reason that is structural
rather than sloppy. The nonlinear term is a product of two polynomials of degree
`J`, so it has degree `2J`, and collocation pins down only `J` conditions on it.
The rest is invisible to the solve by construction. That leftover is exactly what
the argument's first constant is made of.

So: rows the solver enforces, 1e-13 at every parameter value. The one row the
gauge condition displaces, at the same moment, in the same solution: **1e-13 at
`a = 0`, and 9e-3 at `a = 0.5`.** Ten orders apart. Zero at the nodes is not zero
as a function, and here it is not even close.

Fine — that is a known kind of problem, and it usually gets better as you refine
the grid. It did not. At one parameter value the defect sat flat across a
sixteen-fold refinement. And in every single case, the worst point was the
outermost point of the domain.

That last detail is the tell.

## The velocity has a logarithm in it

Here is the equation's far field, in one line. The profile is transported at a
speed which is *not* the constant `c` in the equation, but

```
E(X) = c + a·U(X)
```

where `U` is the velocity the profile induces on itself. And `U` is an integral
of a Hilbert transform, so it carries a logarithm: for large `X`,
`U ≈ (∫Ω/π)·log X`, and the integral of the profile is negative.

So `E` decreases without bound. **At some finite radius it hits zero.**

At the anchor point of the whole programme — the exactly-solvable case `a = 0` —
this cannot happen, because `E ≡ c` is constant. That case has a clean power-law
tail, `X⁻²`, and eleven legs of analysis were built on it: a graded space that
measures how fast things decay, a resonance at exponent 2, tail bounds, far-field
solution operators. All correct, all about that tail.

Turn `a` on and the tail is gone. Past the critical radius the transport reverses,
and the profile does not decay out there — **it ends**. Approaching the radius
from inside, the balance forces

```
Ω ~ (X_c − X)^{1/a}
```

an algebraic zero whose order is one over the advection parameter, with no fitted
constant anywhere in the derivation. Beyond it, zero solves the equation exactly.

Measured, in two completely independent discretizations, at five parameter
values: the critical radius agrees to **0.1% or better** (once the grid resolves
it at all), and the zero's order tracks `1/a` to 7–9% — the residual gap being
what a leading-order fit over a finite window should show.

The `a = 0` anchor everything was built on is the degenerate case where that
radius sits at infinity.

## Why the defect measurement was misbehaving

Because a function that is identically zero outside a finite radius, represented
in a *global* spectral basis, leaves ringing where it should be flat — and the
norm the certificate uses weights the far field by a large positive power of `X`,
which multiplies precisely that ringing. The measurement was not failing. It was
reporting, accurately, that the object and the space are mismatched.

## The number that looked like good news

At one parameter value the defect does converge, and at the finest grid it lands
**7.7× under the budget** — the first time in this project that side of the
inequality has come in under target at nonzero advection.

It is not good news, and the reason is worth stating plainly, because it is the
kind of error that is easy to publish by accident. Every constant in that budget
was computed by linearizing at the `a = 0` anchor. The certificate linearizes at
the profile it certifies. So I measured the operator norm at the *actual*
profiles:

| a | 0 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 |
|---|---|---|---|---|---|---|
| ‖A‖ | 3.5 | 3.9 | 2,100 | 76,000 | 500,000 | 16,000,000 |

That is not the matrix going bad — the plain condition number barely moves across
that row. And one grid size cannot distinguish "large operator" from "bad grid",
so I refined:

| ‖A‖ | J=200 | J=400 | J=800 |
|---|---|---|---|
| a = 0 | 3.551 | 3.542 | 3.537 |
| a = 0.2 | 292 | 2,100 | 15,300 |

**At the anchor it is flat to three decimals. At the real profile it grows like a
power of the grid size.** The approximate inverse that the entire argument is
built around does not exist in the limit.

There is a mechanism, and in hindsight it is forced: linearizing about a solution
with a zero of order `p` produces a mode that blows up like `(X_c − X)^{−p}`,
which belongs to no sup norm at all. The operator at the real profile has a
genuine singular direction at the critical radius, and the numbers above are
measuring how much of it each grid can resolve. The "good" value at `a = 0.1` is
the grid failing to see the problem.

Correct the budget for the real operator norm and the near-miss becomes a miss by
three orders of magnitude. Both sides of the inequality move the wrong way, by
the same mechanism.

## The boundary, and a coincidence that did not survive

This project has confirmed four separate times that the two-scale structure stops
existing somewhere around `a ≈ 0.5`, and has never had a mechanism for it. Two
were available here. The critical radius shrinks steadily as `a` grows — at
`a = 0.5` it is down to about three times the profile's own width — which is a
geometric story: eventually there is no room for two scales. And the zero's order
is `1/a`, which passes through the integer 2 at exactly `a = 1/2`, where the
relevant transform grows a logarithm; that would be a sharp arithmetic story
landing exactly on the observed boundary.

The arithmetic story predicts trouble at `a = 1/3` too, where the order is 3.
There is none: that point sits smoothly between its neighbours in every
measurement. So the coincidence is a coincidence, and what is left is the
geometric trend — smooth, with nothing special happening at 0.5.

Which is annoying, and also exactly what the earlier work said: that crossing is
*soft*. The leg explains where the outer scale comes from and why it collapses.
It does not predict the boundary.

## Where this leaves the programme

Honestly? It re-specifies the target, and I would rather find that by measurement
than after an attempt to make anything rigorous.

The upside is that the repair is *cheaper* than what it replaces. If the profile
is exactly zero beyond a finite radius, a certificate can work on a **finite
interval**, with the radius itself as an unknown — and the far field, which has
absorbed eleven legs of tail bounds, resonances and graded norms, disappears,
because there is nothing out there. The price is the singularity at the boundary,
and the standard reason to think that price is refundable is that the singular
mode is precisely the derivative of the solution family with respect to the
boundary position: adding a free boundary as an unknown is the usual way an
apparent singularity of a linearization stops being one.

That is untested. It is the next leg, and it comes with its own kill switch: do
the free-boundary version at one parameter value and watch the operator norm as
the grid refines. If the singular direction is not absorbed, the framing needs
replacing rather than repairing.

---

*Everything here is plain float64. Nothing is interval-enclosed and nothing is
rigorous; this is scouting for a computer-assisted certification on a
one-dimensional toy model, which is not the Clay problem and would not be
mistaken for it. Code, data and the figure are in the repository; the figure
rebuilds from committed data without re-running anything.*
