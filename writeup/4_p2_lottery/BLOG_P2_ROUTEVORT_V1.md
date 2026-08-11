# The wall was made of pressure

*Route-VORT (leg 332). Technical sibling:
[TECHNICAL_P2_ROUTEVORT_V1.md](TECHNICAL_P2_ROUTEVORT_V1.md). Figure: `fig86`.
Data: `writeup/data/p2_route_vort_v1.json`.*

Two legs ago this project hit a wall that looked permanent.

The setting was a weighted function space — Breden and Chu's `H²(μ)`, where every
function is required to decay like a Gaussian, and the "norm" you measure things
in multiplies them by `e^{|x|²/4}` before integrating. That weight grows
ferociously. At a radius of 80 it is `e^{1600}`, a number with seven hundred
digits. Anything you want to put in this space has to decay fast enough to beat
it.

Leg 257 found a witness — a perfectly nice, perfectly Gaussian, perfectly
divergence-free swirl of fluid — pushed it through the Navier-Stokes
nonlinearity, and discovered that what came out **did not decay like a Gaussian
at all**. It decayed like `1/r⁴`. Algebraically. Which against `e^{r²/4}` is no
decay whatsoever. The integral is infinite.

Worse, leg 257 showed the coefficient of that `1/r⁴` tail could never be made to
vanish, because the coefficient *is the kinetic energy of the witness*. You can't
have a nonzero fluid with zero energy. So the tail is there for every nonzero
field in the space, and the whole approach is dead on arrival.

That's a clean, brutal, and — as this leg confirms to twelve decimal places —
entirely correct piece of mathematics.

## Where the tail actually came from

Here's the part that turns out to matter.

Navier-Stokes has a pressure in it. Pressure is a nuisance: it isn't an
independent thing you get to choose, it's whatever it has to be to keep the fluid
incompressible. The standard way to handle this is the **Leray projector**, which
takes your nonlinear term `F` and subtracts off a gradient:

```
P[F] = F − ∇v
```

where `v` is the pressure, solving `Δv = div F`. And `v` is where the trouble
lives. `F` itself is Gaussian — it decays beautifully. But `v` is the solution of
a Poisson equation, and Poisson equations are *nonlocal*: a compact blob of
source produces a potential that reaches all the way to infinity, falling off
like a power of `r`. Leg 257's `1/r⁴` tail is `∇v`, and only `∇v`.

So the obstruction is real, but it is made **entirely of pressure**.

## The move

Fluid dynamicists have known for two centuries how to get rid of the pressure:
take the curl. Work with the *vorticity* `ω = curl u` instead of the velocity.
The pressure is a gradient, and the curl of a gradient is zero, so it vanishes
from the equations before you ever have to think about it.

If leg 257's obstruction lives in the pressure gradient, and the vorticity
formulation deletes the pressure gradient, then the obstruction should
evaporate — for the most elementary reason in vector calculus:

```
curl(∇v) ≡ 0
```

That's the whole idea, and it is not subtle. Which is exactly why it deserved
checking rather than believing. Cheap arguments that give you the answer you were
hoping for are the ones that turn out to be wrong.

## The catch, and why it's the whole leg

There's a reason nobody had simply declared victory here. Going to vorticity
doesn't make the nonlocality go away — it **relocates** it. The vorticity
equation still contains the velocity `u`, and you now have to *reconstruct* `u`
from `ω` via the **Biot-Savart law**, which is every bit as nonlocal as the
Poisson equation was. Leg 257's own notes flagged this: *"Biot-Savart is nonlocal
with the same algebraic tail, so the obstruction moves rather than lifts."*

And that flag is half right. This leg measured the reconstructed velocity, and it
does decay algebraically, like `1/r³`. Against the Gaussian weight, that means
the reconstructed velocity is **flatly outside the space**. Its weighted density
at radius 80 comes out to `10^686`. It is not even close to belonging.

So we have a genuinely awkward situation: the vorticity is in the space, the
velocity is emphatically not, and the equation involves both.

Does the obstruction survive?

## No. And here is why not.

The difference is one word: **alone**.

In the velocity formulation, the projector's output `∇v` sits in the equation by
itself. Nothing multiplies it. Its `1/r⁴` tail meets `e^{r²/4}` in a fair fight
and wins, and the integral diverges.

In the vorticity formulation, the nonlinear term is `(u·∇)ω − (ω·∇)u`. Look at
it. **Every single term contains an `ω` or a `∇ω`** — and `ω` is the thing that
lives in the space, the thing that carries the Gaussian. The badly-behaved
velocity `u` never appears on its own. It only ever appears *multiplied by
something that decays like `e^{−r²}`*.

And `u`, though it is not in the space, is perfectly **bounded** — it maxes out
at about `0.67`. Bounded is all you need, when the thing next to it is a
Gaussian. So the product decays like a Gaussian, and the Gaussian crushes the
weight, and the integral converges.

That's it. That's the mechanism. The nonlocal object is still there and is still
badly behaved; it has simply been demoted from a term in its own right to a
*coefficient*, and coefficients only need to be bounded.

## What the numbers say

The same norm, the same code, the same quadrature — five different fields fed
through it, with nothing varying but the field. Reading off the weighted density
at radius 80, in powers of ten:

| what | at r = 80 | |
|---|---|---|
| velocity formulation, projected | `10^+682` | out of the space |
| the reconstructed velocity itself | `10^+686` | out of the space |
| velocity formulation, *unprojected* | `10^−10415` | in the space |
| vorticity formulation, witness A | `10^−10411` | in the space |
| vorticity formulation, reconstructed velocity | `10^−4864` | in the space |

Eleven thousand orders of magnitude, in opposite directions, from one code path.
Note the third row especially: the *unprojected* velocity nonlinearity is fine
too. It really is the projector, and nothing else, that does the damage.

And instead of a divergence, the vorticity side has an actual finite number, with
an actual bound behind it:

```
‖nonlinearity‖ ≤ ‖∇u‖_∞ · ‖ω‖ + ‖u‖_∞ · ‖∇ω‖ = 0.731
```

with the true value `0.101`. The bound holds, and it isn't vacuous.

## Confirming the thing we were disagreeing with

A refutation is worth nothing if you can't first reproduce what you're refuting.
So this leg rebuilt leg 257's calculation from scratch by a completely different
method — leg 257 ground through a 216,000-point three-dimensional grid; this leg
solved it in closed form using spherical harmonics, sharing no code at all.

The two agree to about **twelve digits**. And the closed-form route does one
thing the grid couldn't: it proves the coefficient identity exactly rather than
by fitting. The tail coefficient is `0.313328534329601`, and `T/4π` — the energy
over `4π` — is `0.3133285343288751`. They match to two parts in a trillion.

Leg 257 was right. The coefficient really is the energy. It really can't vanish.
It just happens to be sitting entirely inside the one term that taking a curl
annihilates.

## The bill

It would be dishonest to stop here, so: this escape route is real, and it is not
free.

That reconstructed velocity decays like `1/r³`. Work out what that means and you
find `u` is in `L³` — its cube is integrable over all of space, with the norm
coming out to `0.731`. And `u ∈ L³` is *precisely* the hypothesis of a
well-known theorem of Nečas–Růžička–Šverák and Tsai, which says that a
backward-self-similar solution of 3D Navier-Stokes satisfying it must be
**identically zero**.

So the vorticity formulation buys you admission to the space and immediately
hands you over to a different wall, one that was already standing behind the
first one. The obstruction we were asked about does not carry over. A different
obstruction is waiting.

That is still progress, and of a specific kind: we now know that the wall leg 257
hit was a property of *how the problem was written down*, not of the problem. But
the honest headline isn't "the road is open." It's "we've correctly identified
which wall we're actually facing."

## Two errors worth admitting

Both mistakes in this leg were caught by tests written before the answer was
known, not by anyone reading the code.

The first: the sign of the vorticity nonlinearity was backwards. The check
reported a residual of `2.895` — which is not a small error, it's *twice the
term*, the unmistakable signature of a flipped sign. If that check hadn't
existed, the leg would have produced converged, plausible, wrong numbers.

The second was subtler and is a nice illustration of why this space is hard to
compute in at all. At radius 80, a Gaussian field is `e^{−12800}`, which
underflows to exactly zero in double precision. The weight is `e^{1600}`, which
overflows to infinity. **The product is a perfectly ordinary finite number, and
neither factor can be represented at all.** The first version of the code
dutifully reported the convergent arms as `−infinity` — a floor, not a
measurement — which would have made the two sides look symmetric when they are
about as asymmetric as two things can be. The fix was to carry the Gaussian in
the exponent and never form it, and the table above is the result.

The wall was made of pressure. Take the curl, and it isn't there. There is,
unfortunately, another wall.
