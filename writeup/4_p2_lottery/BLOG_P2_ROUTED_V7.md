# The number that wouldn't stop growing, and the equation nobody had asked

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. Last
post we produced the project's first genuine upper bounds — and discovered that
the obvious way to compute one produces a confident, reproducible, completely
fictional answer. This post is about the piece that was left over: a number that
grew with resolution in three separate computations, and turned out to be growing
for a reason that had nothing to do with any of the things we suspected. Still a
toy model. Still not a breakthrough.*

## The leftover

The certificate we're chasing needs about eight constants, all of them upper
bounds. After the last leg, five were bounded and three were open. The one we
called sharpest was the *smoothness half* of the inverse operator's norm.

Our norm has two parts. One measures size — how big is the function, allowing for
the fact that it should decay far away. The other measures smoothness — how much
can it change between two nearby points, relative to how close they are. The size
half we had bounded, and the bound was beautifully flat: 5.53 at resolution
J = 125, 5.63 at J = 1600, essentially the same number over a thirteen-fold range.

The smoothness half grew. Not dramatically — like `J^0.5` — but steadily, and it
grew in every version we tried. And a bound that grows with resolution is not a
bound; it's an admission that you haven't understood something.

We had a theory about why. The previous leg had found a trap: computing these
things by duality over the grid's unit ball is unsound, because the grid's ball
contains monsters that the real ball doesn't. We assumed the leftover growth was
more of the same, and the plan we wrote down for this leg said so: restrict to a
subspace where the grid is faithful, measure how faithful, done.

That plan was wrong, and finding out how it was wrong is the useful part.

## Asking where the growth lives

Before building anything, we did the cheap thing: we asked *which pairs of points*
were responsible.

The smoothness measure is a maximum over pairs. So take the same computation, throw
away all pairs closer together than some fixed distance, and see what's left.

| pairs included | J = 125 | J = 250 | J = 500 | growth |
|---|---|---|---|---|
| all | 17.2 | 24.2 | 34.2 | `J^+0.49` |
| separated by ≥ 0.05 | 9.1 | 9.6 | 9.8 | `J^+0.05` |
| separated by ≥ 0.1 | 6.9 | 7.1 | 7.1 | `J^+0.02` |

All of it. Every bit of the growth lives on pairs the grid barely separates —
neighbouring points. Exclude a *fixed* distance (fixed in the continuum, so it
covers more and more grid points as J rises) and the same computation is flat.

That kills the plan. Faithfulness of the ball has nothing to do with it: the
monsters the previous leg found live everywhere, not specifically next door. What
this table says is much more specific, and in hindsight obvious.

## Two rows of an inverse

The quantity being computed is, for each pair of nearby points, *how differently
can the inverse operator respond at those two points*. And it was being computed by
bounding the response at each point separately and adding.

For two points right next to each other, that is a terrible way to ask the
question. Adjacent rows of an inverse matrix are *almost the same row*. Their
difference is small because of a cancellation — and pricing them independently
throws the cancellation away, then divides by the tiny distance between the points.
That's the `J^0.5`. It's not the operator. It's arithmetic that has forgotten what
the operator is.

You cannot fix that by being cleverer about the ball. The cancellation isn't a
property of the ball; it's a property of the **equation**.

## Using the equation

Here is the whole idea, and it takes one line. The equation we're inverting is

    (something)·h  −  c·h′  =  g

— a differential equation. Which means it can be *solved for the derivative*:

    c·h′  =  −g  −  (the other terms, all involving h itself)

Every term on the right is something we already control. `g` is the input, and its
size is exactly what the norm on the right-hand side measures. The terms involving
`h` are controlled by the size half of the norm — the half we'd already bounded.
And one of them is the Hilbert transform of `h`, which the previous leg had already
learned to bound.

So the derivative of the solution is bounded. And once you know a function's size
*and* its derivative, its smoothness is free: a function that is at most `S` big and
changes at most `P` fast cannot vary much between nearby points. The classical
inequality is

    smoothness ≤ C(γ) · (P/2)^γ · (2S)^(1−γ)

with `C(1/2) = 2` exactly. There is no J anywhere in it. There is no grid anywhere
in it. The cancellation we were throwing away is exactly the derivative, and the
derivative is what the equation hands you for free.

There is one twist, which is that the Hilbert transform term depends on the
smoothness we're trying to bound — so the inequality feeds back into itself. That
sounds like trouble, and for a moment we expected a smallness condition to check.
It isn't: the feedback is *linear* in the unknown while the interpolation gain is
*sublinear* (that `γ` exponent, less than one), so the fixed point always exists, no
matter how big the constants are. The one place it would fail is `γ = 1`, the
Lipschitz endpoint — which is the third independent reason this framework can't use
Lipschitz, alongside the two we already knew.

## The number

Bounded, at last:

| resolution J | 125 | 250 | 500 | 800 | 1600 |
|---|---|---|---|---|---|
| smoothness half (new bound) | 63.6 | 63.6 | 63.5 | 63.8 | 64.7 |
| old bound on the same thing | 17.2 | 24.2 | 34.2 | — | — |

Flat. (The residual drift is inherited entirely from the size half, which drifts by
2% over the whole range.) The full operator norm is now bounded — **‖A‖ ≤ 69** at
our reference setting — for the first time in seven legs.

Now the honest part. The best *lower* bound we can find for the same quantity is
0.85. So the bracket is 0.85 ≤ (smoothness half) ≤ 63.6, which is a factor of 75
wide. The bound is real, it's uniform, it's the first of its kind here — and it is
not sharp. Two of those three facts matter.

## What it costs

The previous leg's budget used a stand-in for `‖A‖`: the far-field model's inverse
norm, about 2.5. The real bound is 41–44 at the relevant settings — a factor of
10–20 larger. Substituting the honest number:

- the conditional budget drops from `2.8e-3` to `2.0e-4`, an order of magnitude;
- the radius at which the far field has to take over moves from ~100 out to
  2 000–30 000.

The second of those is survivable — the collocation grid we already use reaches
that far. The first is not nothing: the budget is now firmly *below* the residual
floor our search reaches (~`1e-2`), where before it was the same order.

This is the second leg running where making a constant honest cost the budget an
order of magnitude. That pattern deserves saying out loud: **the approach doesn't
just need the constants bounded, it needs them roughly sharp.** Three of the four
we've bounded so far are lossy by an order of magnitude or more, and the losses
multiply.

There is one piece of good news buried in the map. With upper bounds now available
for both parts of `‖A‖` *and* the curvature term, we can finally plot the thing the
budget actually cares about against both tuning knobs — and it has an interior
minimum, at decay grading 1.4 and smoothness grading 0.15. `‖A‖` on its own would
run off to zero smoothness (a weaker norm is always easier to bound); the objective
doesn't, because the quadratic term pays for exactly that weakness. It's the first
interior optimum in this project computed entirely out of upper bounds rather than
out of maxima over test families — which is to say the first one that means what it
appears to mean.

## And a thing we should have noticed six legs ago

While checking the chain we tripped over something uncomfortable.

Our functions live on a grid in a compactified variable, where infinity sits at one
end. A list of values on that grid stands for a trigonometric polynomial. The norm
weights values by how far out they are — heavily, since the whole point is to
measure decay.

A trigonometric polynomial does not decay. At the very end of the interval, where
the weight blows up, it just... doesn't go to zero. So the weighted norm of the
function our grid values represent is **infinite**. At every resolution. It has been
infinite in every leg of this project.

The reason nobody noticed is that the grid stops half a step short of the endpoint,
so every number we ever computed was finite. Here it is at the last grid node versus
a hair further out, same function:

| J | at the last node | at the very end |
|---|---|---|
| 200 | 8.4e-3 | 1.1e+3 |
| 800 | 1.5e-3 | 1.7e+1 |
| 1600 | 6.0e-4 | 2.1e+0 |

It is a *soft* failure — the offending value falls like `J^-3`, so the discretization
is converging to something that does live in the space. But it is not a small
correction to fix; it's a change of representation. The repair is clear enough:
build the decay into the ansatz — write the unknown as (decay profile) × (polynomial)
instead of just (polynomial) — so that the weighted norm becomes an ordinary norm on
the polynomial. Nothing here does that yet.

Two legs ago the lesson was *check that your instrument can measure the thing you're
asking about*. Last leg it was *check that the set you optimised over is the set you
meant*. This one is: **check that the objects your discretization produces are
actually in the space you're working in.** Same failure, three costumes.

## Where this leaves it

- The domain seminorm part of `‖A‖` is bounded, J-free, and analytic. Six of ten
  constants now have upper bounds.
- The route the previous leg recommended was the wrong one, for a reason we could
  have found in ten minutes with a table — and did, this time, before building
  anything.
- Pricing the honest `‖A‖` costs the budget an order of magnitude and puts it below
  our own residual floor.
- The discretization does not live in the space it's being measured in. New item on
  the ledger, and the most structural one there.

Still a toy model of a toy model. Still float arithmetic, nothing interval-enclosed,
nothing rigorous. The Clay odds are unchanged at roughly 0.05%, and the honest best
case for this whole line remains "certifies a traveling wave we already know in
closed form." What changed this leg is that the list of things standing between here
and that best case got one shorter and one longer at the same time.

*Data and figure: `writeup/data/p2_route_d_v7_seminorm.json`, `fig25`. Technical
version with the full derivation:
[`TECHNICAL_P2_ROUTED_V7.md`](TECHNICAL_P2_ROUTED_V7.md).*
