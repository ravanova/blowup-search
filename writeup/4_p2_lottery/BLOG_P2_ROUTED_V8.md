# The last unpriced constant — and the bad trend that stopped

*Route-D v8 of a Navier–Stokes blow-up search. Level-1 tooling plus upper
bounds. Not a certificate, not rigorous, not a Clay result.*

---

Three legs in a row, this project got the same bad news in the same shape.

Each time, we replaced a quantity we had *measured* with a quantity we had
*bounded* — the honest thing to do, since a certificate needs upper bounds and a
maximum over a handful of test functions is a lower bound. And each time, the
"certification budget" — how big the residual of a candidate profile is allowed
to be before the argument stops closing — dropped by a factor of ten.

```
v5   7.6e-2      (everything measured; one term not priced at all)
v6   1.18e-2     (that term priced)
v7   2.58e-4     (the operator norm made honest)
```

By the end of v7 the conclusion wrote itself: *it is not enough for the constants
to be bounded, they have to be roughly sharp.* Three of the four bounded so far
were lossy by an order of magnitude or more, the losses multiply, and three
constants were still unpriced. Two more legs like that and the budget is gone.

This leg priced one of them. It cost **7%**.

---

## The thing that was missing

The certificate needs a bound on the nonlinear term — for this equation the
product `h·H(h)`, where `H` is the Hilbert transform. Since v5 the space has
measured two things about a function: **how fast it decays** and **how smooth it
is** (a Hölder seminorm, exponent γ). So bounding the product means bounding
both, for both factors.

Three of those four pieces were done by v6 and v7. The fourth — *how smooth is
`H(h)`, in the weighted sense* — had never been bounded at all. v7 said so
explicitly, and predicted where it would hurt: at small γ, i.e. exactly where
v7's own optimum sat. It called that optimum's location "provisional" for that
reason.

## The first surprise: the weight is wrong, and it has to be

The obvious guess is that `H(h)` should be measured with the same decay weight as
`h`. It should not, and the reason is worth keeping.

`H` does not inherit decay. However fast `h` falls off, `H(h)` falls off like
`1/X` and no faster — the far field only sees the total mass of `h`. So the right
weight for `H(h)`'s seminorm is fixed at `1 − γ`, independent of how fast the
functions in the space decay. Asking for the weight the domain uses would have
produced an infinite constant, with nothing to point at.

This is the third time in the Route-D series that a weight exponent has been the
whole difficulty, and the third time the correct one was forced rather than
chosen.

## The estimate, and a mistake worth publishing

The bound itself is the classical proof that the Hilbert transform is bounded on
Hölder spaces, done carefully enough to produce a number instead of a `C`: split
the integral into a near region around the two points and a far region, charge
the near part to the smoothness of `h`, charge the far part to its decay, and
keep every constant.

Two implementation notes, because both cost time.

**Never let the regime of your argument become the regime of your code.** The
scaling argument that shows the bound is finite needs the two points to be close
together relative to their distance from the far-field endpoint. The *estimate*
needs no such thing — only that the near region fits on the circle. The first
version imposed the argument's condition on the code, which forced a much cruder
fallback for the pairs just outside it, and the reported constant came out
**twelve times too large**. Every one of those pairs was the fallback, not the
estimate.

**Build the object twice.** The estimate is a majorant of a three-piece
decomposition. A majorant of a *wrong* decomposition is still a valid inequality
about something — it just isn't about your problem, and no amount of testing "is
the bound bigger than the measured value" will notice. So the decomposition was
built a second time with the true integrand and compared against the answer known
in closed form. Agreement to 6 decimal places, after it caught two sign errors —
one of which was also wrong in the module's own documentation, where it had been
sitting looking correct.

## The second surprise: v7's prediction was backwards

With the constant in hand, the natural check is v7's prediction: the missing term
should punish small γ, so the optimum should move to larger γ.

It doesn't move. The complete `Z₂` map — the first in this project in which every
constant is an upper bound and *nothing is omitted* — has its minimum at exactly
the same place v7's incomplete map did, `(α, γ) = (1.4, 0.15)`, with `Z₂` rising
from 242 to 261.

The reason is a little embarrassing and completely mundane: the term v6 *had*
already bounded contains the same `1/γ` divergence as the new one, coming from
the same near-field integral. Nothing new blows up at small γ. Measured as a
ratio, the correction is 0.1% at γ = 0.05 and 28% at γ = 0.9 — worst at the
*opposite* end from the prediction.

So the budget moves 2.58e-4 → 2.39e-4, and the sequence reads:

```
v5   7.6e-2
v6   1.18e-2      (x 1/6)
v7   2.58e-4      (x 1/46)
v8   2.39e-4      (x 0.93)
```

## What this does and does not change

It does **not** make the certificate close. 2.4e-4 is still about forty times
below the residual floor our search actually achieves, three constants remain
unpriced, and the new bound is itself about four times lossier than the true
constant appears to be. Nothing here is rigorous — it is all ordinary
floating-point arithmetic, and even the eventual success this scouts would be a
computer-assisted result about a *toy model*, not the Millennium problem.

What it changes is one specific piece of pessimism. After v7 the honest reading
was that every remaining honesty step would cost an order of magnitude, and the
approach would die of a thousand cuts. That reading was based on three data
points that all had the same cause — quantities that had never been bounded at
all. This one had never been bounded either, and it cost almost nothing.

That is not evidence the remaining three are cheap. It is evidence that "each
step costs an order" was a pattern in the data rather than a law about the
method, which is a distinction worth about one more leg of effort.

---

**Data + code:** everything in this post rebuilds from
`writeup/data/p2_route_d_v8_quadratic.json` via
`writeup/4_p2_lottery/p2_route_d_v8_evidence.py` (figure `fig26`), with the
estimate in `solver/hilbert_holder.py` and its six gates in
`test_nk_hilbert_holder.py`. The technical companion is
`TECHNICAL_P2_ROUTED_V8.md`.

**Honest ceiling, again:** Level-1 tooling plus upper bounds. Nothing
interval-enclosed, nothing rigorous, no certificate. Overall odds on the
Millennium problem from this line: ~0.05%.
