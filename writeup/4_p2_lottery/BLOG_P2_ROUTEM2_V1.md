# We asked the failure what it could handle — and it named something

*Route-M2 v1, leg 63. Gate: YES. Nothing was promoted; the branch is parked for a
human decision. Data: `writeup/data/p2_route_m2_v1_targets.json`.*

---

Seven legs ago this project aimed a certification method at a specific object: the
non-symmetric self-similar profile of the 1D Hou–Luo model, a blow-up nobody has proved. Six
legs later the attempt was dead. The interesting part was *how* it died. Not on the object —
leg 55 measured the object and found it perfectly admissible. It died on a property of the
**operator**, and that property turned out to be sharp enough to write down:

> The standard tail estimate works when the unbounded part of the linearization is a
> **multiplier** — a diagonal. Cut the problem off at mode `K`, and what's left has an inverse
> that *shrinks* like `1/K`. Our operator's unbounded part is a **shift** — it lives off the
> diagonal — and the leftover inverse is a **constant that grows**. There is nothing to make
> the error small with.

That is a diagnosis, and a diagnosis you can compute is a **screen**. This leg turned it into
one and pointed it back at the question of what to attempt at all.

## The dial

The screen needs a knob that separates *models*, not just settings. Dissipation supplies one:
add `−ν k^γ` to the diagonal, where `γ` is the **order** of the dissipation — `γ = 2` is
ordinary viscosity, `γ = 0` is none at all — and ask, for each `γ`, whether the leftover
inverse shrinks or grows as you cut further out.

Two disciplines before any number was allowed to count. The new dial had to reproduce the old
one exactly where they overlap (it does: **zero difference, entry for entry**), and the fast
tridiagonal shortcut had to agree with the slow, honest dense computation (it does, to **3
parts in 10¹⁵**). This repository has lost a claim before by comparing numbers from an operator
that had quietly changed underneath them.

## The guess that died

The obvious prediction: the crossover sits at `γ = 1`, because the transport term's
off-diagonal entries grow like `k/2`, so the diagonal has to out-grow them to win.

Wrong, and not narrowly. The measured crossover is **0.402** at one dissipation strength,
**0.824** at a hundredth of it, and **0.012** at ten times it. A diagonal that is pointwise
*much smaller* than the off-diagonal still breaks the recursion that makes the inverse grow.
The same thing happened to leg 57's prediction on the previous dial, for the same reason: the
threshold you get from comparing entry sizes is not the threshold the operator actually has.

That the crossover moves so much with strength is itself a caveat, and it is written into the
result rather than around it: every candidate is re-screened across two decades of strength,
and the conclusion leans on the one that doesn't flip.

## The ledger, and the uncomfortable symmetry in it

Run every uncertified target this project has ever ranked through the screen, and the four
inviscid ones come back with the **identical** number: `+0.4372`, the wrong sign, the same
wrong sign, by the same amount. That is not a bug — it is the diagnosis restated. The shape is
a property of the operator, so every target in the inviscid family fails the screen for
precisely the same reason. Including the one the project spent seven legs on.

Then the two dissipative rows come back the other way, and the top one clears it by a whole
power: **−2.0270**.

## Which leaves the question the gate was written to ask

*Is there an uncertified target, on a model where blow-up is provable, that this method is
actually shaped for?*

**Yes — one.** The generalized Constantin–Lax–Majda model with ordinary viscosity. Chen
(arXiv:1908.09385) **proves** finite-time self-similar blow-up there, analytically, for a
parameter close to `1/2` with the full Laplacian. No computer-assisted certificate exists for
*any* dissipative self-similar profile — every certificate in this family is inviscid. And its
tail block needs none of the apparatus that legs 52–54 built and then watched fail: no border
row, no border column, no matching condition, no block coupling to lose.

## And the reason nothing was promoted

Every candidate that passes the screen is **dissipative** — and this project has a standing ban
on re-opening the dissipation question, whose lift condition names a link in the chain that is
now measured dead.

So the screen's answer and the plan's rules point in opposite directions, and that is a
genuine fork, not a technicality. Either the ban is about a *different question* than the one
this ledger raises, or it binds and the honest reading is that every reachable target is
shift-shaped and the method is finished for this project's whole target class — which would be
a materially stronger negative result than the one leg 58 is writing.

Deciding that is not a measurement, so this leg didn't make it. The branch is parked with the
ledger, the evidence, and the constraint attached to the verdict where a summary can't lose it.

**What this is not:** not a proof, not a certificate, not float-free — no intervals were used.
Not a claim that a certificate would close on the winning row; that needs a different number
entirely. Not full-text literature work: the blow-up result was read from an abstract, which is
recorded on the row as a debt the next pass has to pay. And not movement on the Clay problem,
whose odds here remain about 0.05%.

What it is: the first time this project's failure has been used as an instrument instead of an
epitaph — and the instrument found something.
