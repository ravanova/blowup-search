# The obstruction was about the box, not the object

*Leg 313, Route-SDSS. Gate answer: **NO**. Escalated to the user; nothing lifted.*

---

Fifty-three legs ago, leg 260 closed a door. It had been asked whether a particular expensive
search — a hunt for a discretely self-similar blow-up of 3D Navier–Stokes, framed as a hunt
for a **periodic orbit** of a rescaled flow — was excluded because it was *expensive* or
because it was *impossible*. Leg 260 came back with something better than a price. It found a
reason:

> *the target is not in the search's own state space.*

The profile such a search is looking for has **infinite energy** once you rewrite the problem
in similarity variables. A search that represents finite-energy states can never get near it.
And unlike a price — which the Clay goal's authorisation of heavy engineering simply
dissolves — that is structural. Leg 260 called it out precisely: the entrance's *defining
adjective*, **unseeded**, is incompatible with its object's only function space.

This leg was sent to ask one question. **That argument was made about a search that trawls
blindly. Does it still hold if you seed the search from a candidate somebody already
computed?**

The answer is no. And the reason is a little embarrassing, in the way good corrections usually
are.

## The infinite energy was a fact about the ruler

Leg 260's divergent integral is real. This leg reproduced it — including reproducing leg 260's
own banked number, `2.000035`, on leg 260's own integrand, as a control. The profile really
does have infinite energy **when you measure it in the unweighted `L²` norm on all of space**.

But leg 260 had already answered a *different* question in the same document: *what function
space does this object live in?* Its answer was a **weighted** space — `(1+|y|)^{-s}` with
`s > 1`. This leg measured where that threshold sits, and it sits exactly at `s = 1`: at
`s = 0.9` the norm still diverges, at `s = 1.1` it is finite.

So leg 260's own answer to question (a) already contains a space in which its answer to
question (c) is false. The obstruction and its own solvent were in the same document.

It gets sharper. There is exactly one method in the literature that has actually *operated*
this kind of seeded search on a Navier–Stokes-like object — Hou's dynamic-rescaling programme.
It does not use a finite box at all. It computes *"in a transformed domain on a uniform mesh,
which maps back to a highly adaptive physical mesh"*. Compactify space that way — let
`X = |y|/(1+|y|)`, so that infinity becomes the point `X = 1` — and the troublesome profile
becomes, exactly, the function `1 - X`. A straight line. Its norm is `√(1/3) ≈ 0.577`. There
is nothing infinite anywhere.

**The infinite energy was never a property of the object. It was a property of the ruler leg
260 measured it with.** Naming which ruler is not a technicality here; it is this
repository's own rule (lesson 91), and leg 260's statement did not name one.

Leg 260 gave four reasons. Under seeding, all four go — including the two it itself flagged as
*"the finding"*. One of them dissolves almost comically: reason 3 says *"impose the unknown
and the search is seeded"*. Seeding is the hypothesis. Hou imposes exactly that, and calls it
a *soft far-field cut-off*.

## But something else was hiding underneath

This is where the leg stops being a demolition and starts being useful.

The ban this leg was scoping carries a warning in its own text: the building blocks of these
orbits have **limited regularity**, of the form `X^{1-iy}` — a fractional, oscillating power
sitting at a point. That was recorded as a difficulty of the *model* the repository used to
study this (gCLM), at the *origin*.

Watch what the compactification does to it. The far-field block of the Navier–Stokes object
oscillates like `r^{-1+iκ}`. Push it through `X = |y|/(1+|y|)` and it becomes

    (1 - X)^{1 - iκ}

which is the **same functional form**, letter for letter, now sitting at the far boundary
`X = 1` instead of at the origin.

**The compactification that made the norm finite did not remove the difficulty. It moved it.**
You can put it at zero or you can put it at infinity; you cannot delete it. It is a property
of the entrance, not of where you choose to stand.

And that costs. A smooth function needs **10** Chebyshev modes to be resolved to one part in a
million. This block needs **823** at the mildest oscillation tested, and **14,149** by the time
the frequency reaches 20 — with the cost growing essentially *linearly* in the oscillation
frequency, `n ≈ 791 κ^0.954`. The coefficients die off algebraically, not geometrically. That
is a factor of a thousand-odd in one direction of a three-dimensional problem, and it is the
one number leg 260 could not have quoted, because it had not yet moved the difficulty into a
place where it could be counted.

*(Two honest notes. This leg's first attempt at that measurement was wrong: at a coarser
resolution the worst number moved 30% when refined, meaning it was measuring the array rather
than the object, and a second column saturated outright and has been withdrawn. And two of the
leg's own controls were duds — one was a symmetric function whose odd coefficients vanish for
reasons having nothing to do with smoothness, which is precisely the failure mode this
repository named as lesson 90. All of it is in the technical writeup rather than quietly
fixed.)*

## The seed does not exist yet

There is a second finding, and it is the one that actually constrains what happens next.

A seeded search needs a seed. So: is there a known numerical DSS candidate for 3D
Navier–Stokes to seed from?

No. The literature search found the near miss — Hou's candidate — and it fails the screen
three separate ways: it is **axisymmetric** (which this repository's own screen kills
outright), it is a *generalized* Navier–Stokes with solution-dependent viscosity and an
effective dimension of about **3.188**, and it is a **stationary** profile rather than a
genuinely time-periodic one. Beyond it, nothing: across every query and spelling variant, **no
one has computed a genuinely discretely self-similar blow-up profile for Navier–Stokes
numerically.** The time-periodic computations that do exist are for other equations, and they
lean on an explicit ground state and a compact operator — neither of which Navier–Stokes
offers.

So the seed set for the object that survives the screen is **empty**. That is a real
obstruction, it is not leg 260's, and it is not a price. But it is an *availability* fact, not
an impossibility: two published programmes describe how to *manufacture* such a seed rather
than find one. Manufacturing it is the first item on the bill, not a locked door.

## What this leg did not do

It did not lift anything.

The route's ban stands, in force, unchanged. This leg has no authority over it and did not
touch the file it lives in. What it hands the user is a corrected picture: the reason recorded
for closing the door is scoped to a measuring device nobody has to use, a **different**
obstruction now stands where it stood, and the price has been re-read from the live
repository — where, incidentally, it has gone **up**, not down. Leg 260 estimated a floor of 27
legs of construction and told future legs to re-read rather than cite that number. Fifty-three
legs later, not one new solver module has landed, so the floor is now about **33**.

The ruling is the user's. It always was.

**And the ceiling, stated plainly and unchanged: no link of the chain from a 1D certificate to
the Clay problem moved here. Odds on Clay remain ~0.05%. This leg answered a scoping question,
which is a way of choosing what not to try — never a step toward the prize.**

---

*Figure: `fig76_route_sdss_v1.png`. Data: `writeup/data/p2_route_sdss_v1.json`, 30/30
self-tests. Technical companion: `TECHNICAL_P2_ROUTE_SDSS_V1.md`.*
