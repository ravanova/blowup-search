# I had the sign wrong

*Route-D v13 of a Navier–Stokes blow-up search. A correction to the previous leg,
and a better answer. Not a certificate, not rigorous, not a Clay result.*

---

The previous leg found something real: the candidate profile, for any nonzero
advection, does not have a decaying tail — it **ends**, at a finite radius, with an
algebraic zero whose order is one over the advection parameter. And it measured
that the operator the whole certification argument is built around does not
converge as the grid refines: flat at the exactly-solvable anchor, growing like a
power of the grid size at the profile we actually care about.

Then it explained why, and the explanation was wrong.

I wrote that linearizing about a profile with a zero of order `p` produces a mode
blowing up like `(X_c − X)^{−p}`, which is in no reasonable norm. It doesn't. The
mode at the critical radius goes like `(X_c − X)^{+p}` — it *vanishes* there. I
dropped a sign converting a derivative in `X` into a derivative in the distance to
the boundary, and the resulting sentence read plausibly enough that it went into
the writeup, the notes and the continuation prompt.

Measured, the exponent is `+5.28, +4.21, +3.51, +3.01, +2.65, +2.14` across the
parameter range, against a prediction of `+5, +4, +3.33, +2.86, +2.5, +2`. Not
merely the wrong size — the wrong sign.

So the divergence needed a different explanation, and the one it has is worse.

## The wall is not at the critical radius. It is past it.

Outside the profile's support the linearized equation is the same, with the same
exponent, but now it runs the other way. For large `X` the velocity's logarithm
takes over and the homogeneous solution behaves like

```
h ~ ( log(X / X_c) )^{1/a}
```

which **grows**. The space the argument works in is a decay class: perturbations
must fall off like a fixed power of `X`. A slowly growing mode is not in it, and
the amplitude multiplying it is not free — it is whatever the solve inside the
support hands over. So the inverse generically produces something outside its own
target space. One scalar condition's worth of obstruction, sitting at infinity.

That is worse than a singularity at the critical radius, because a singularity is
a resolution problem and this is not. No grid fixes it.

Measured, against a prediction with no fitted constant in it:

| a | 0.20 | 0.25 | 0.30 | 0.35 | 0.40 |
|---|---|---|---|---|---|
| measured exponent | 4.9988 | 3.9980 | 3.3307 | 2.8536 | 2.4855 |
| predicted `1/a` | 5.0000 | 4.0000 | 3.3333 | 2.8571 | 2.5000 |

— from an instrument that has nothing to do with the matrix whose norm was
diverging: integrate the linearized equation outward on the profile's own
coefficients and watch.

The same number `1/a` now appears three times in this problem: the order of the
profile's zero, the exponent of the vanishing mode at the critical radius, and the
power of the logarithm by which the outer mode grows. All three fall out of one
leading balance.

## Checking rather than trusting

Two habits earned their keep, and both were cheap.

**The row that didn't fit.** At `a = 0.5` the measurement came back at 0.054
against a prediction of 2. That is the kind of outlier one is tempted to drop with
a footnote. Refining the grid: 0.054 → 1.84 → 1.70, while the neighbouring
parameter value sits at 2.4855 → 2.5035 → 2.5014, converged to four digits. The
previous leg had already reported that the profile stops being a converged object
right about there. The outlier is the instrument, and knowing that is worth more
than the data point.

**Attribution, not argument.** "The divergence comes from the far field" is a
story until you make the far field stop moving. The grid's outer radius grows with
its size, so I recomputed the operator norm with the domain restricted to a fixed
radius:

| growth with grid size | rows out to 20 | to 50 | to 200 | all |
|---|---|---|---|---|
| a = 0 (control) | flat | flat | flat | flat |
| a = 0.2 | `J^0.31` | `J^0.54` | `J^1.06` | `J^2.86` |

Monotone in the cutoff, and nearly gone when the far field is excluded. Meanwhile
87–97% of the extremal row's weight comes from within 10% of the critical radius.
So the perturbation is *sourced* at the turning point and *does its damage* out in
the tail — exactly what a growing mode excited at the boundary does.

(There is a residual growth even at a fixed radius, `J^0.3` to `J^0.5`. It is
small next to the rest and this leg does not explain it. Saying so is cheaper than
finding out later that I'd rounded it to zero.)

## The repair I recommended last time doesn't work either

The obvious fix for a missing range direction is to add an unknown that supplies
it, and the obvious candidate was the wave speed, which the argument's gauge
freezes. It cannot work, for a reason already written down twice in this project's
own notes: the speed is tied to a *symmetry* of the problem, and a symmetry
direction adds kernel, not range.

I measured it anyway. The square bordered system at the anchor has a condition
number of `4e18` — singular to machine precision. The overdetermined version's
norm grows with the grid even at the anchor, where the plain system is flat.

## What is actually left

The real repair is not a bordering trick, and the diagnosis sharpened it. It is:
**take the far field out of the domain**. Pose the problem on the finite interval
up to the critical radius, with that radius as an unknown, and let perturbations
live only there. The growing mode then has nowhere to grow. This is consistent —
outside the support the residual vanishes identically, because every term in it
carries a factor of the profile or its derivative — and it makes eleven legs of
tail bounds, decay gradings and far-field resonances unnecessary rather than
wrong.

It is still untested, and the test is unchanged: build it at one parameter value,
refine the grid, watch the operator norm. Flat and the framing is repaired.
Divergent and it needs replacing, at which point the honest move is to write up
the arc and spend the remaining effort elsewhere.

---

*Everything here is plain float64. Nothing is interval-enclosed and nothing is
rigorous; this is scouting for a computer-assisted certification on a
one-dimensional toy model, which is not the Clay problem and would not be mistaken
for it. The previous leg's writeups have been corrected in place with the change
marked, rather than quietly edited.*
