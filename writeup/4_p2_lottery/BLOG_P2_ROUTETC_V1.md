# I fixed the broken part, and the break moved to the seam

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. Last time the wall
came down. This time I put the pieces together and found out the wall was never the load-bearing
thing. Still a toy model. Still not a breakthrough. Clay odds unchanged at ~0.05%.*

*(Revised after review. The answer below is unchanged and was independently confirmed. Two
things I first got wrong are corrected in place: how much the result proves, and why the
numbers are the size they are. I've left the wrong versions visible rather than quietly
swapping them, because the correction is the more interesting half.)*

## The story so far, in one paragraph

I'm trying to write a computer-checkable proof that a certain equation has a solution that
blows up. The method — it's standard, it's called a radii polynomial — needs four numbers.
Get all four small enough and an inequality closes and you have a theorem. Two sessions ago
three of the four came out exact or tiny and the fourth, the "tail", had no bound at all. Last
session I fixed the tail: added the far field as an extra unknown, and the number that had
been running away to 48 settled down at 9.44.

That was a real fix, and I wrote it up carefully with a warning attached: **a bounded tail is
not a certificate**. The tail was one term of four, measured on its own. The extra unknown I'd
added had no home anywhere else in the problem. This session I gave it one.

## What "giving it a home" actually means

If you introduce a new unknown into one part of a system of equations, it has to appear in the
other parts too. Concretely, three things were missing:

1. **A column.** The new unknown is the amplitude of the far field — how big the tail is out at
   infinity. How does that feed back into the first few hundred coefficients? I had never
   computed it.
2. **A row.** Some equation has to *determine* the amplitude. A matching condition between the
   series I'm computing and the asymptotic shape I'm assuming.
3. **A defect.** Every equation you add has a residual — how badly your approximate answer
   fails it — and residuals feed the term that has to be small.

None of these are hard once you write them down. That's the point of this session: they'd
never been written down.

## The column was not small

Here's the first thing that came out, and it's the whole story in miniature.

The far-field amplitude reaches back into the finite part of the problem through exactly two
entries. Both of them **grow with the size of the finite block.** If I keep 64 coefficients,
the amplitude hits one of them with weight 32.5 and another with weight 30.6. If I keep 4, it's
2.5 and 2.5.

So the extra unknown isn't a small correction sitting off to the side. It's welded to the rest
of the system, and the weld gets heavier the bigger the block.

That's not a bug in my setup. It's what the equation is. The hard part of this equation —
the part that's unbounded — is a **shift**: it moves each coefficient onto its neighbours. So
wherever you cut the problem into "the part I compute" and "the part I estimate", the cut goes
straight through an entry whose size is *half the cut position*.

## And then the seam let go

The proving method wants an approximate inverse built in two independent blocks: a matrix
inverse for the finite part, an explicit formula for the tail. Fine. But then the quantity that
has to be less than 1 splits into four pieces — two for the blocks, two for the **seam** between
them.

The two block pieces are beautiful. `10⁻¹⁶` and `10⁻¹²`. Nothing wrong there.

The two seam pieces, in the best space and at the best cut I tried:

```
                             best case anywhere in the sweep
  seam, tail  ← finite                1.39
  seam, finite ← tail                43.15
```

They need to be under 1. Together. And they get *worse* as the cut moves outward — exactly
doubling for one, exactly quadrupling for the other, per doubling of the cut. I swept cuts from
4 up to 64 coefficients, two function spaces, two ways of removing a symmetry, and six ways of
normalising the extra row and column. **20.47 is the best number that exists anywhere in all of
that** (43.15 in the configuration I actually shipped).

**What that does and doesn't prove — I overstated this the first time.** The 1.39 is the piece
that doesn't depend on how I build the finite matrix, so it's the piece that would be a
statement about *any* attempt. Its best value across the whole sweep is **0.9961 — just under
1.** So it doesn't forbid closure by itself. The 43 is the piece that *does* depend on my
finite matrix. So what I've actually shown is: **the standard two-independent-blocks recipe
can't close this.** Not: nothing can. That distinction is the entire reason the next step is a
real question rather than a formality, and I'd written the plan correctly while writing the
prose wrong.

## Why the numbers are the size they are — and why my first answer was wrong

I originally wrote that the big number is big because "the inverse of the finite block grows
like the cut size, and the seam entry is half the cut size, so the product goes like cut
squared." Clean story. Wrong twice.

The inverse of my finite block doesn't grow like *K*. It grows like **K²** — exactly
`2(K²−1)`, which is a suspiciously tidy formula and should have made me look. And when I ran
the same code with the far-field unknown switched off, it came out as exactly `4(K−1)` —
linear. **The K² is something my own augmentation created**, not something the equation did.
It comes from a weight mismatch: the amplitude column is measured at scale ~K/2 while the
matching row is measured at scale ~1, so in the scaled problem the matching equation carries a
coefficient of about 2/K — a deliberately feeble equation, and inverting a feeble equation
costs you a factor of K.

And the seam entry doesn't contribute K/2 either. It contributes **2**. I checked: the ratio of
the big number to the inverse norm is 1.90–2.00 in every single row. The dominant path isn't
the sub-diagonal entry I'd fingered; it's a rank-one term that hits the *first* coefficient
with weight 1 from every single tail mode.

So I re-ran it with six different normalisations, including simply deleting the amplitude
unknown. Best case anywhere: **20.47.** Still one to two orders too big, still growing. **The
answer survives; my explanation of it didn't.** Given that this leg's whole methodological
point is about naming mechanisms correctly, that's worth more than the answer.

## Why last session's fix didn't help here

This is the bit I want to be precise about, because it's the actual lesson.

In the textbook version of this method, the hard part of your equation is a **multiplier** —
it scales coefficient number *k* by some number that grows, like *k²*. Then the seam entry is
big, size *k*, but the tail's inverse is *one over* that, size 1/*k*, and the product is fine.
The bigness cancels.

My tail's inverse is not 1/*k*. It's a **constant** — 9.44 in last session's ladder, 2.2 to
10.3 at the cuts I used here. That was last session's good news: it used to be unbounded and
now it isn't. But a constant doesn't cancel a *k*. Constant times *k*/2 is *k*/2, and *k*/2
goes to infinity.

So bordering fixed the tail's **invertibility** and did nothing to its **size**, and it's the
size that the seam needs. Two different defects in the same problem, and I'd only fixed one of
them. I keep re-learning that one.

## The thing that doesn't exist

There's a smaller finding I like more than the main one, because it was genuinely invisible
before.

The problem has a symmetry — you can rescale the *x*-axis and get another solution — so I have
to pin it down with an extra equation. The natural one is a weighted sum: `Σ k b_k`. Everyone
uses something like that.

Now that the far field has a column, that column has an entry in the symmetry-pinning row. And
that entry is a sum of *m* times the far-field coefficients, which decay like 1/*m*². Which is
the harmonic series.

```
  keeping    256   512   1024   2048   coefficients
             3347  4557  5862   7222        ... +1865 every time I e-fold
```

It never converges. **The far-field column has an entry that doesn't exist.** In the spaces
where my target profile lives, that symmetry-pinning equation isn't a valid equation at all.

There's a clean fix — pin the symmetry direction directly instead (it turns out to be exactly
one basis vector, checked to zero in floating point), and everything improves, by between 1.5×
and 8.7× depending where you cut. It doesn't rescue the answer: 43 is *after* the fix. But it's
the kind of thing you only find by assembling.

## The honest bookkeeping

The first of my four numbers, `Y₀`, is **exactly zero** — including in the new matching row.
That sounds great and means nothing. It's zero because the exact solution of this toy problem
is a single basis function, so it has no far field at all, so the matching condition is
trivially satisfied. The polynomial has a root at *r* = 0, which is the statement "an exact
answer is exact."

The real question is whether the inequality holds on an interval of positive size, and that
needs the seam number under 1, and it's 43.

## Did I break my own instrument?

Fair question, and it's the one I always try to answer before publishing a negative. If my code
says "doesn't close" for everything, then it isn't measuring anything.

So: add dissipation. One extra term, `−μk`, which turns the shift into a multiplier — the exact
structural property the textbook method assumes. Nothing else changes.

The seam numbers fall like 1/μ, exactly as the mechanism predicts, and by μ = 2 the assembled
number is **0.92** — under 1. The certificate closes. **The instrument can say yes; it just
doesn't say yes about the inviscid problem.** That's what makes this a measurement rather than a
bug report.

I also checked four choices for the far-field direction, including two deliberately wrong ones.
Here I had to fix something: in my first version the big seam number came out *identical* for
all four, which I proudly reported as the cleanest possible statement — and which was actually
just a bug in what I was measuring. That number was computed from two things neither of which
knew which border I'd picked. It couldn't have come out otherwise. **A control that cannot fail
isn't a control.**

So I wired the choice through properly, into the amplitude column itself. Now it can fail, and
it does: the honest writeable-down direction ties the theoretical optimum (ratio 1.0004) and
beats a random direction by 13×, while the plausible-but-wrong direction makes the whole matrix
essentially singular — worse by a factor of 4×10¹³. The controls discriminate. And the true
statement I'd been reaching for survives in weaker form: the seam is part of the *operator*, so
the border choice decides how badly conditioned it is, not whether it's there.

## Where this leaves things

The gate I wrote before running anything said: if the polynomial closes on the toy problem, go
try the real one; if not, report which term ran out and *don't* fix it by fiddling with the
function space.

It didn't close. The term that ran out is the seam, and it's a term that **did not exist as a
quantity until this session**, because before this session the two halves of the problem had
never been in the same object. That's not a disappointment — that's what assembly is for.

And fiddling with the function space can't touch it: the seam entry is `K/2` for every choice of
space I'm allowed. This is the second time in three sessions I've had to write down that the
parameter's optimum isn't where the mechanism lives.

What it does tell me, sharply, is that the standard `ℓ¹`-Fourier radii polynomial and *inviscid
self-similar transport* are structurally mismatched, and not in the place I thought. Not the
tail. The seam. If there's a way through, it needs an approximate inverse that isn't block
diagonal — which is a different piece of machinery, not a tuning of this one.

Still a toy model. Still nothing claimed about the real target. **No link of the chain moved.**
