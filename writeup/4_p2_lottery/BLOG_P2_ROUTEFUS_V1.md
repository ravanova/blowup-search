# The assumption nobody can check by computing harder

*Leg 314 / Route-FUS. Figure `fig77`. Technical companion:
`TECHNICAL_P2_ROUTEFUS_V1.md`. Scoping only — nothing was built.*

---

There is a sentence on page 19 of `arXiv:2509.14185` that decides whether a whole programme
can ever become a proof:

> *"For a computer-assisted proof to be feasible, it is **desirable** that the spectrum in the
> right-half µ-plane consists of a **finite number** of eigenvalues."*

"Desirable." Not proved, not checked — hoped for, and then used.

That paper found unstable self-similar blow-up profiles for several fluid models using neural
networks, to impressive precision. A follow-up 72 days later pushed the precision to round-off.
Leg 175 of this project read both at full text and banked the important observation: **the
precision fix does not touch this sentence.** You cannot compute your way out of it. We checked
that again this pass on a fresh instrument — the follow-up's abstract never mentions unstable
spectra or eigenvalues at all.

So we asked the obvious next question. Is this condition provable, checkable, or open?

The answer turned out to be more interesting than any of the three.

## The condition isn't a question yet

Here is the thing about "the spectrum has finitely many points in the right half-plane." It
sounds like a fact about the profile. It isn't. It's a fact about the profile **and the space
you put it in** — and if you don't say which space, you haven't asked anything.

This isn't our clever observation. It's a theorem, in a paper this project already had on its
shelf. Jie Xu's *Spectral picture of self-similar collapse in the Constantin–Lax–Majda equation*
takes one specific profile — the simplest interesting one in this whole family — and shows that
the answer flips depending on the realization:

* In one realization (**maximal `L²`**), you see what Xu calls an **"in-strip smear"** — a
  blurred band, not a finite set of points.
* In another (**origin-`H²`**, which imposes a condition where the profile is singular), the
  smear **disappears**. The essential spectrum collapses onto a single vertical line at
  `Re λ = −½`, and the point spectrum over the entire complex plane is exactly **two points**,
  `{0, 1}` — and both are symmetry artefacts, not real instabilities.

Same equation. Same profile. Finite or smeared, depending on a choice nobody wrote down.

## We can show you the smear

This project has, sitting in its own data directory from an earlier leg, exactly the
measurement that makes the smear concrete — on a related 1D model, in a discretization that a
previous leg had already audited *from the source code* and confirmed to be the maximal-`L²`
side of Xu's dichotomy.

Count the unstable directions as you refine the grid:

| grid size `K` | unstable directions |
|---|---|
| 48 | 45 |
| 96 | 93 |
| 144 | 141 |

That's `K − 3`. Exactly. The fitted slope is `1.000000` with **zero** residual.

**The number of instabilities is just the number of grid points.** Refine the grid, get more
instabilities, forever. Meanwhile the fastest growth rate barely moves — flat to within
`0.75%` — while the frequencies it lives at march off toward infinity in lockstep with the
grid. That isn't a finite set of modes being resolved better. It's a **curve** running off to
infinite frequency, and the grid is just deciding how much of it you get to see.

### Two things we made ourselves check

`K − 3` is *far* too tidy. This project has a standing rule about suspiciously round answers:
find out what produced them before quoting them. So: the matrix is `K × K`, the code removes
one eigenvalue by hand (a known exact symmetry mode), and two more sit at or below zero.
`1 + 2 = 3`. Bookkeeping, fully accounted — and we explicitly **do not** bank the "3" as a fact
about the operator. The real content is the **slope**.

The second objection is sharper: maybe a badly-resolved profile just *manufactures* fake
instabilities. Good objection. It runs the wrong way. Across that same ladder the profile's own
residual improves by **more than ten orders of magnitude** — and the count goes **up**. Better
resolution buys *more* instability. A numerical artefact would evaporate. This one thickens.

And the control: what would have to change for the counting code to say "finite"? Only one
thing — switch on viscosity. Do that, and the same code, same grid, same profile reports
**zero** unstable directions at every `K`. The instrument can say finite. It says divergent here
because the operator is different, not because the code can't count.

## Why you can't compute the answer

Now the part that decides the classification.

Every rigorous computational method for this counts eigenvalues **inside a box**. That's what
validated numerics does: draw a bounded region, enclose what's in it, certify the total.

But the finiteness condition is a claim about **infinite imaginary part**. Eigenvalues are
allowed to pile up out at infinite frequency, and ruling that out is not counting — it's an
*estimate*, a bound on how the operator behaves at high frequency. No box, however large, and no
amount of certified arithmetic, sees the place where the condition actually lives.

The literature agrees, and the clearest evidence is a paper that does the job properly. Guo,
Hadžić, Jang and Schrecker's 149-page proof of nonlinear stability for the Larson–Penston
collapse handles the spectrum by splitting it: an energy method at **low and high frequency**,
and **computer assistance only in the middle**. The computer gets a compact box —
`Re λ ∈ [0,1]`, `|Im λ| ≤ 8`, a range this project had already recorded. The unbounded tail is
handled by a **theorem**: maximal dissipativity of the operator on backward light cones.

The sharpest illustration is a paper that *does* certify an unstable count. Barker and Zumbrun
enclose eigenvalues rigorously, in interval arithmetic, using a winding number around a region
`B(0,R) ∩ {Re λ ≥ 0}`. Look at where the radius comes from: `R = (√γ + ½)²`, **derived on
paper**, proved to contain every possible unstable eigenvalue. The computer works inside the
disc. The disc itself is a theorem. That is the shape of every honest certified count, and it is
precisely the half nobody has for the four models here.

Two more corroborations from unrelated corners. Gallay and Wayne, working in weighted spaces,
have the essential spectrum sitting at `Re λ ≤ −(m−1)/2` — you buy finiteness by *raising the
weight*, which is to say by changing the space, exactly the realization-dependence above. And
Chen and Hou's computer-assisted 3D Euler proof simply **sidesteps** the condition: it runs on
energy estimates with a finite-codimension argument rather than on any enumeration of unstable
modes. When an existing computer-assisted blow-up proof routes *around* your assumption, that
tells you something about its price.

That structural step has three names in three literatures — maximal dissipativity
(Buckmaster–Cao-Labora–Gómez-Serrano), a Hardy–Mellin resolvent bound (Xu), Weyl's theorem plus
a high-frequency estimate (the classical version, and the 2007–2010 wave-map papers). It is the
same step every time, **and it is not available for any of the four models in question.**

## The verdict

**Open** — with the obstruction named, in two parts:

1. **The condition isn't realization-invariant, and no realization is named.** As written, it
   has no truth value to prove, disprove *or check*.
2. **Once you fix one, what's left is a high-frequency resolvent bound on an unbounded region.**
   That's a theorem, not a computation.

The one-line version, which is the thing we'd most like to survive this write-up:

> **For this condition, numerics is a refuter, not a verifier.**

A grid ladder can *kill* finiteness — it does, above. A certified count can tell you what's
inside a box. Neither can ever *establish* the thing the proof needs. Anyone who builds the
certified count and reports "condition checked" will have measured something true and answered a
different question.

## What this is not

It is not progress on Navier–Stokes. **No link of this project's chain moved. The odds on the
Clay problem stay ~0.05%, unchanged.** Classifying an assumption is not discharging it — if
anything we've made the assumption *harder to state* than it was on page 19, by showing it's
under-specified.

And the honest boundary: the diverging count above is measured in **one realization of one 1D
model**. It is not a claim about the four models the original paper studied. It demonstrates the
missing step **can** fail. Whether it does fail for those four is exactly the open question — and
now at least it's the *well-posed* open question, which it wasn't before.

*Nothing was built. The construction, if anyone wants it, is named in the technical companion
§7 — including which half of it this repository could actually do, and which half nobody can.*
