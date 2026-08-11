# You can't enclose something that isn't there

*Route-DECR (leg 318). Technical sibling: [TECHNICAL_P2_ROUTEDECR_V1.md](TECHNICAL_P2_ROUTEDECR_V1.md).
Figure: `fig84`. Data: `writeup/data/p2_route_decr_v1.json`.*

---

There is a move that appears over and over in computer-assisted blow-up proofs for fluids, and
until now this project had recorded it as a limitation. You want to prove that a solution of
the Navier–Stokes equations blows up. You cannot handle the viscous term directly, so you
prove the theorem for the *inviscid* equations instead — Euler, where the same singularity
mechanism lives — and then you argue that the viscosity you dropped is small enough not to
matter. The computer certifies the inviscid profile. The viscosity is handled with a
pen-and-paper inequality afterwards.

An earlier leg of this project gave the two options names. **ENCLOSED** is when the viscosity
sits inside the thing the computer certifies. **DOMINATED** is when it doesn't — when the
certified object is the viscosity-free system and the viscosity is admitted afterwards as a
decaying error. Leg 240 then read the entire subsequent published output of the author group
that produced the flagship compressible result, at full text, and measured that nobody had
upgraded DOMINATED to ENCLOSED. Nobody had even tried.

That is the sort of finding that invites a lazy explanation: *it's hard, and people are busy.*
This leg asked whether there is a better one. And there is.

## The one-line version

**You cannot enclose an object that does not exist.**

Here is why that is not a slogan. When you look for a self-similar blow-up, you rewrite the
equation in rescaled coordinates so that the singularity becomes a *steady state* — a thing
that just sits there and doesn't change. That steady state is the "profile", and it is what the
computer certifies.

Now put the viscous term into those rescaled coordinates. It does not sit still. It comes with
a factor that decays like `e^{−δ s}`, where `s` is the rescaled time and `δ` is a number you
can compute from the scaling exponents alone. And a steady state, by definition, cannot contain
a term that is still changing. So if `δ > 0`, the viscous term is **absent from every profile
there is**. The only profiles that exist are the viscosity-free ones.

There is nothing to enclose. Not "nothing anyone has managed to enclose" — nothing there.

If `δ = 0` exactly, the viscous term stops decaying, it sits still like everything else, and
now there genuinely is a viscosity-dependent profile to certify. That is the case Dähne and
Figueras are in for the complex Ginzburg–Landau equation, and it is why they can dial the
dissipation up from zero and follow the certified branch. If `δ < 0`, the viscosity grows
instead, overwhelms the nonlinearity, and there is no blow-up at all.

So the criterion is: **enclosure is criticality.** DOMINATED is not a weakness of anyone's
method. It is the visible signature of a viscous term that is *subcritical* for the scaling
you chose.

## The part that made this worth a leg

You could stop there and call it a tidy reframing. What makes it sharp is where the boundary
falls in the one case this project cares most about.

The compressible implosion theorem works on a window of scaling exponents. Leg 240 banked that
window: at the standard air-like value of the adiabatic exponent it is the open interval from
`1.1666667` to `1.1909830` — a window `0.0243163` wide, which is not much room.

Compute where `δ = 0` — the one exponent at which enclosure becomes possible at all — and it
lands on `r = 2γ/(γ+1)`. That is **exactly the lower endpoint of the window**. Not close to it.
The same number, to `0.0`, at both of the values the bank records, and identically zero in exact
arithmetic across forty-five more.

So the picture is this. Domination owns the open window. Enclosure could only ever live at the
single point the window leaves out — and it is left out *precisely because* that is where the
decay rate of the domination argument hits zero. The two treatments are complementary. They
share exactly one point, and neither of them occupies it.

And at that one point, two further things go wrong, both of which we can name. The
viscosity-free profile equation is *first order*; putting the Laplacian back makes it *second
order*, so the viscous profile is not a small deformation of the inviscid one — it is a
different problem that would have to be certified from scratch. And separately, leg 315 found
that the only known machinery for turning a certified ODE into a certified PDE statement
assumes the equation is *dissipative*, while this one is *hyperbolic*.

The enclosure window has measure zero, and the cheap way in is blocked. Nobody failed here for
want of effort.

## A prediction we could have lost

A criterion that only explains things you already knew is worthless. So the leg extended it
out of sample.

Suppose the viscosity is not constant but depends on the density, as `ρ^θ`. Redo the exponent
bookkeeping — this is a derivation, not a quotation — and you get a threshold: below a certain
power `θ`, the viscosity is subcritical and the implosion still happens; at `θ = 1`, the
shallow-water case, the viscosity is *supercritical* and the mechanism must die.

The literature pass for this leg had turned up two papers, both new to this project's records,
both by a group with no computer anywhere in their argument. One proves that implosions do
occur below a threshold in exactly that power, a threshold depending on the adiabatic exponent.
The other proves that at `θ = 1` solutions are globally regular and **cannot implode at all**.

The sign test was run before those theorems were consulted for their direction. Had it come out
the other way, the criterion would have been killed by a published theorem it did not choose.
It came out right. The *numerical value* of the threshold is still unchecked — we read an
abstract, not a paper — and that is written down as a named, one-leg test that could still kill
this.

## The test that nearly killed it, and shouldn't have

The central identity — that the enclosure exponent is the window's excluded endpoint — was
first checked in ordinary floating-point arithmetic. It failed. The residual came out at
`5.3e-15` against a tolerance of `1e-15`, and the leg's own test declared its own headline
false.

It wasn't false. The two quantities being compared are each about `1` and cancel exactly, so
`5.3e-15` is roughly twenty-five units in the last place of the things that cancelled — the
standard price of catastrophic cancellation, and no evidence whatever about the identity. This
project has been bitten by precisely this before, and the lesson from that occasion was not "use
a looser tolerance". It was "fix the instrument". So the test now runs in exact rational
arithmetic, where the residual is `0` — not "0.000000", actually zero — and the floating-point
number is kept alongside as a diagnosis rather than a measurement.

Loosening the tolerance to `1e-14` would have passed the test for the wrong reason and left it
unable to detect a real error of that size.

## What this does not do

It does not open anything. That was written into the leg's brief before the work started: even
if the criterion existed, it would not become a line of attack. And the mathematics agrees —
the criterion's only positive statement is that enclosure is possible on a set of measure zero,
at a point where both of the routes in are blocked. There is nothing there to build.

It also says something unwelcome about this project's actual target. For the *incompressible*
Navier–Stokes equations — the Clay problem — the viscous term is scaling-critical automatically.
The criterion is satisfied. Enclosure was never the obstruction there. The obstruction is a
non-existence theorem: Nečas–Růžička–Šverák and Tsai proved the profile you would want to
certify isn't there either, for a completely different reason. Trading the compressible object
for the incompressible one trades a measure-zero window for a theorem that closes the door. That
is a worse position, and the criterion is what makes the two comparable at all.

No link of the chain from a certified profile to a Clay proof moved. The odds stay where they
have been for fifty-three legs: about 0.05%. What moved is a small amount of clarity about why
one particular door has never opened — it turns out there was never a room behind it.
