# We checked our own excuse against the literature. It held — and it wasn't ours.

*Route-XS v1, leg 57. An exploration leg. The gate answered NO, which here is the good
answer. Figure: `fig52_route_xs_v1_shapes.png`.*

---

## The excuse

For three legs we have been telling ourselves a story about why our certificate won't
close.

The method we are using — a radii-polynomial certificate, the standard tool of rigorous
computer-assisted proof — needs to invert an infinite matrix. It cannot, so it splits the
matrix in two: a finite block you invert on the computer, and an infinite **tail** you
bound by hand. The bound on the tail is the whole trick, and it works for a beautiful
reason: in the usual problems, the part of the operator that blows up is a **multiplier**.
In the right basis it is a diagonal matrix with entries marching off to infinity. Cut it at
mode `K` and the tail's inverse is `1/Λ_K` — automatically tiny, and tiny is exactly what
the estimate needs.

Our operator is not like that. The thing that blows up is a **transport term** — the
stretching that makes the singularity in the first place — and in our basis its matrix has
entries of size `~ k/2` sitting *off* the diagonal, with **exactly zero on the diagonal
itself**. There is no `Λ_K` to divide by. So the tail estimate has nothing to work with, and
the certificate stalls.

That story is satisfying. It is also, told that way, **just a story we tell about our own
code.** Three legs of failure and a tidy explanation for it is the exact shape of a
rationalisation. So this leg went and checked it against the published record: not "does
this feel right", but **is there a paper that does the thing we say cannot be done?**

## The check

Four computer-assisted proofs that this project actually cites. For each one, three
questions: is the unbounded part a multiplier or a shift; is the approximate inverse
block-diagonal; and does the tail inverse decay? Every answer traced to a **specific
sentence in the full text** — a section number and the sentence quoted — because the last
time we did this from an abstract, the claim had to be withdrawn.

The result, and the two interesting rows are the ones that *almost* break it:

| | radii-poly? | unbounded part | approx. inverse | tail decays? |
|---|---|---|---|---|
| Cadiot–Lessard–Nave | yes | multiplier | block-diagonal | yes |
| **Breden–Desvillettes–Lessard** | yes | tridiagonal-dominant | **NOT block-diagonal** | yes |
| **Chen–Hou** | **no** | **SHIFT** | none built | — |
| Dåhne–Figueras | no | (finite-dimensional) | finite Jacobian | — |

**Nobody has a counterexample.** But look at *how* the two near-misses miss.

**Breden–Desvillettes–Lessard** build the exact thing our next leg was going to try: an
approximate inverse that is **not** block-diagonal. It is published, it works, and it is
the first of its kind by their own account. And it still needs the diagonal to be there —
their assumption (4) requires it bounded below, and their Proposition 2.3 gets the decay
*from* that. So the move is available and its price is on the label.

**Chen–Hou** is the one that matters. Theirs is the one published computer-assisted proof
whose unbounded part genuinely *is* a transport operator — the same shape as ours. And they
never form a tail estimate at all. The words "radii polynomial", "Newton–Kantorovich" and
"approximate inverse" **do not appear anywhere in either of their two papers.** Instead they
run a weighted energy estimate and *"derive the damping terms … from the local terms,
especially the advection term."*

They take the transport term — the thing we treat as the obstruction — and use it as the
**source** of the estimate.

That is not a counterexample to our story. It is the strongest confirmation of it in the
literature: the one group who certified this shape of operator did it by throwing our method
away.

## The part where we made it a measurement

A table of four papers is still a table someone typed. So the dichotomy was also **dialled
continuously**. Our tail operator has a knob already in the code — add dissipation, `mu·k`,
onto the diagonal — which walks the operator from "shift" (`mu = 0`, diagonal exactly zero)
to "multiplier". Then just measure whether the tail inverse shrinks as you push the cut out:

- **`mu = 0`:** the inverse **grows**, `K^{+0.44}` — from 2.19 at `K = 4` to **11.53** at
  `K = 128`.
- **every `mu > 0`:** it **shrinks**, `K^{-0.85}` to `K^{-0.95}`.

One curve up, five curves down, and the one going up is the only one with no diagonal. It is
panel A of the figure and it is the whole leg in one picture.

This also **corrected our own headline.** Legs 52–53 described the bordered tail inverse as
"a constant (2.19 … 10.32) rather than `1/K`". It is not a constant. **It grows** — 5.3× over
the range we measured. The 2.19 we have been quoting is the *smallest rung of a rising
ladder*, not a bound.

## The part where we were wrong

Breden–Desvillettes–Lessard admit off-diagonal terms up to a ratio `δ < 1/2`. Translated to
our operator that is `mu > 1`, so the natural guess was that things fall apart below
`mu = 1` — a published threshold, showing up in our own numbers. It would have been a lovely
paragraph.

**It's false.** `mu = 0.25` sits four times outside their admissible set and behaves exactly
like the well-conditioned cases. Their `δ < 1/2` is what *their particular construction*
needs; it is not where the operator changes character. The real hinge is cruder and more
absolute: **zero diagonal, or not.**

That guess is in the artifact, labelled REFUTED, with a test pinning it dead. So is a set of
numbers we computed the wrong way — bordering an operator that didn't need it, producing
values like 8.26e+04 that look alarming and mean nothing — kept precisely so the next person
who computes them recognises them instead of publishing them.

## What we actually earned

Less than it sounds, and the novelty pass said so **before** any of this was built.

The dichotomy is **not our observation.** Cadiot writes both halves down in a 2025 paper:
that the operator "becomes an infinite diagonal matrix", and that the tail is "supposed to
be diagonally dominant". We have been re-deriving standard practice and calling it an
insight. The honest version is: **we rediscovered why the method has the shape it has, the
hard way, by running into the wall.**

What is new is only that the classification is now **executable** — a predicate you can run,
that reads a ledger, that answers the question, and that **flips to "yes" when we feed it a
fictitious counterexample**, so we know the "no" is a fact about the literature and not a
bug in the code. A check that isn't executable decays at the speed of memory. This one has
tests.

So the epitaph gets to stand — with a citation instead of a mood behind it. Our negative
result generalises past our own repository. And the next leg, which was going to try a
non-block-diagonal approximate inverse, now knows that this exact move is published, and
knows what its authors needed to make it work.

**No link of the chain moved. It's still ~0.05%.** But the wall we hit is a real wall, other
people have hit it, and one group found a door that isn't the one we've been pushing on.
