# Both halves, finally in one room

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. The
[last two posts](BLOG_P2_ROUTED_V4.md) each found half of one requirement and
couldn't satisfy it: one kind of measurement sees decay but not smoothness, the
other sees smoothness but not decay. This post builds the thing that sees both. It
works. Still a toy model. Still not a breakthrough.*

## The shape of the problem, restated

We're trying to turn a very good numerical guess into a computer-checkable proof.
The machinery needs a pair of "spaces" — precise ways of measuring how big a
function is — and it needs *every* quantity in the certification arithmetic to come
out finite in that pair.

Three legs in, we knew exactly what the space had to do, because two different
attempts had each failed for exactly one reason:

- Measure functions by their **Fourier coefficients**, and you're measuring
  smoothness. The equation's transport term, which lives at spatial infinity,
  demands decay. That failure was total — an entire category of spaces, ruled out
  by a conservation law.
- Measure by a **weighted maximum**, and you're measuring decay. That fixed the
  transport term beautifully. But the equation also has a Hilbert transform in it,
  and the Hilbert transform is famously unbounded on bounded functions — take
  something bounded with a jump and its transform blows up logarithmically.

Two one-parameter families, each missing exactly what the other had. So: build one
that carries both.

## The candidate, and a mistake it caught

The classical place where the Hilbert transform *is* well behaved is Hölder space —
functions with a quantified modulus of continuity. So the candidate is a norm with
two knobs: a decay weight `α`, and a smoothness exponent `γ`.

Writing it down took one attempt more than expected. There's a change of variables
in this project that maps the infinite line onto a finite interval, and the natural
far-field smoothness measure has to be translated through it. I did the translation,
got a clean-looking formula, and wrote a numerical check for it.

The check failed. Not by a rounding error — by a whole exponent. The correct
translation eats a factor of `γ` that I'd left in, and with the wrong version, *the
very profile we're trying to certify has infinite norm*. The space wouldn't have
contained the object it was built for.

That's the second time in three legs that a cheap consistency check has caught an
algebra slip before it reached a conclusion. It is, at this point, the single
highest-return habit in the project.

The corrected version has a nice payoff: after the translation, the elaborate
far-field smoothness measure becomes a completely ordinary one on the compactified
interval, with a single weight. The change of variables does the hard bookkeeping
for free. That's the only reason this leg was cheap enough to run.

## The adversary, defused

Last post's obstruction was a specific function: the partial sums of a square wave,
which stay bounded while their Hilbert transforms grow like `log m`. Feed it to
both norms:

| degree | 8 | 32 | 128 | 512 | |
|---|---|---|---|---|---|
| **maximum norm** (last leg) | 1.80 | 2.56 | 3.31 | 4.07 | **grows** |
| Hölder, `γ = 0.35` | 1.04 | 1.02 | 1.01 | 1.00 | **flat** |
| Hölder, `γ = 0.5` | 1.02 | 0.98 | 0.92 | 0.85 | **falls** |

The maximum-norm ratio grows at every setting of the decay weight — it doesn't care
about decay at all, which was precisely the diagnosis. In the Hölder norm the
adversary is neutralised, because it now pays for its own oscillation: a wiggly
function has a large Hölder norm, and that sits in the denominator.

It fails at very small `γ`, which it must — `γ → 0` *is* the maximum norm, so the
problem has to come back, and it does, right on schedule.

## Two knobs, two sweet spots

Here's the part I didn't expect.

Measure how much the Hilbert transform can amplify a Hölder norm, as a function of
`γ`:

| `γ` | 0.15 | 0.25 | **0.35** | 0.5 | 0.65 | 0.85 |
|---|---|---|---|---|---|---|
| amplification | 1.60 | 1.21 | **1.12** | 1.13 | 1.18 | 1.29 |

A bowl. Both ends rise, for different reasons: at `γ → 0` you're back to the
maximum norm where the transform is unbounded; at `γ → 1` you're at Lipschitz,
where it fails again. There's a best choice in the middle.

And last leg found the *same shape* in the other knob: the decay exponent `α` has
its own interior optimum near 1.4, because the far-field cost rises one way and the
core cost rises the other.

> Two knobs. Two interior optima. Four unrelated mechanisms producing them. The
> space this proof needs has a finite, non-degenerate best configuration in both
> parameters — which is the most encouraging structural fact five legs have turned
> up.

## One thing still creeps

Not everything settled. A coarse scan and a focused one disagreed about whether a
key quantity converges, which is always worth chasing down. The culprit turned out
to be a single direction.

Feed the machinery an error that decays *exactly* at the critical rate the codomain
is defined by, versus one that decays even slightly faster:

| margin `δ` | J=125 | 250 | 500 | 1000 | 2000 |
|---|---|---|---|---|---|
| **0 (exactly critical)** | 1.956 | 2.223 | 2.471 | 2.691 | **2.879** |
| 0.10 | 1.778 | 1.778 | 1.777 | 1.777 | **1.777** |
| 0.50 | 1.711 | 1.711 | 1.711 | 1.711 | **1.711** |

Any margin at all, and the number is flat to four significant figures across a
sixteenfold refinement. Zero margin, and it creeps upward — a logarithm.

This is not a new problem. Two legs ago we found exactly this at a different
exponent: the far-field equation produces a *logarithm* precisely at one critical
rate and a clean answer everywhere else. The fix then was to step slightly off the
critical value, and the fix now is the same — require the error to decay strictly
faster than the critical rate.

The difference is the price. Last time, stepping off cost a factor of `2/ε` and
forced a whole optimisation. This time it costs *nothing* — the numbers get
slightly **better** as you step further off. The reason is which side of the ledger
the step lands on: tightening a requirement on the *error* makes the machinery's
job easier, while loosening the class of *solutions* made it harder.

## Where that leaves the arithmetic

The key constant comes out around **3.3**, against **13.4** in the previous setting.
The best tolerable error is about `8×10⁻²` instead of `2×10⁻²`. Roughly a fourfold
improvement.

And now the honest part, which is longer than the good news.

That `8×10⁻²` is a ceiling on a ceiling. The operator sizes here are measured over a
*family* of test functions rather than computed exactly — the exact computation is a
linear program, and this project deliberately has no linear-programming library —
so they're lower bounds, which makes the final figure an over-estimate. One whole
term in the arithmetic has still never been bounded by anything, in five legs. The
best configuration sits at the edge of the range I swept, in a row that showed signs
of not having converged. And the case we actually care about — the one where the
answer isn't already known in closed form — has an error floor of about `10⁻²`,
which is uncomfortably close to a ceiling that hasn't yet paid its debts.

## Five legs in

What Route D has produced so far: a rigorous interval-arithmetic core (still
unused, correctly — nothing has closed in floating point yet), an exact operator
representation, a structural negative with a mechanism behind it, a no-go theorem
for an entire category of spaces, a confirmed price for the far field, and now a
space in which every requirement identified so far is simultaneously satisfiable.

That's a genuine map of the terrain. It is not a proof of anything, and it's worth
saying plainly that the gap between "we know which space to use" and "we have a
certificate" is still most of the distance.

This remains a one-dimensional toy model of the boundary behaviour of a
three-dimensional problem, everything is ordinary floating-point arithmetic, and
even total success would be a computer-assisted result about a profile we can
already write down. The odds on the actual Millennium problem are about 0.05%, and
nothing here moved them.

But five posts ago we didn't know what the space had to do. Now we do, and we have
one. That's the kind of progress this sort of project is actually made of.

---

*Figure: `writeup/figures/fig23_p2_route_d_v5_holder.png`. Data:
`writeup/data/p2_route_d_v5_holder.json`. Technical version with the derivations,
gates and full tables: [TECHNICAL_P2_ROUTED_V5.md](TECHNICAL_P2_ROUTED_V5.md).*
