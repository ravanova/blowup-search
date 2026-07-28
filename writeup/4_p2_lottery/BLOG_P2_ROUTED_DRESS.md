# The proof didn't close. Here's exactly what stopped it — and where it hides.

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. The
[previous post](BLOG_P2_ROUTED.md) built the machinery for turning a very good
guess into something a computer could certify, and ended with one gating question:
does the certification actually close? This post runs that test. It doesn't close.
This is the write-up of a negative result — the useful kind, where you learn where
the wall is, why it's there, and what's on the other side of it. Still a toy model.
Still not a breakthrough.*

## The cheapest possible version of the experiment

The last post set up a **Newton–Kantorovich** certificate: you have an approximate
solution, and you want a theorem saying a *true* solution exists nearby. The
theorem needs four numbers.

- `Y₀` — how far your candidate is from solving the equation (the **defect**).
- `Z₀`, `Z₁` — how well you can invert the linearized equation (the **contraction**).
- `Z₂` — how curved the equation is (the **quadratic** term).

Feed them into one polynomial, `p(r) = Z₂r² − (1 − Z₀ − Z₁)r + Y₀`. If it has a
positive root, you get a **ball of radius r around your candidate containing
exactly one true solution**. That's the certificate. And there's a hard gate before
anything else matters: you need

    Z₀ + Z₁ < 1.

If that fails, the polynomial has no positive root and the whole apparatus is dead
on arrival, no matter how good your candidate is.

Doing all this with *guaranteed* arithmetic — intervals, provable rounding — is a
lot of work. So we did the sane thing first: computed all four numbers in ordinary
floating point, across a ladder of truncations from 4 modes up to 256. A **dress
rehearsal**. If the ball closes with room to spare, harden everything with
intervals. If it doesn't, you've saved yourself weeks and learned something.

It didn't close. Not at 4 modes, not at 256, not anywhere in between.

## The number that should have been a warning

Here's the quantity that decided it: `‖A‖`, the size of the inverse of the
linearized operator.

| modes `N` | `‖A‖` |
|---|---|
| 4 | 5.0 |
| 16 | 14.0 |
| 64 | 50.9 |
| 256 | 198.7 |

That's not converging to anything. It's growing — very close to linearly,
`N^0.97`. And a growing `‖A‖` is fatal, because the curvature constant is
`Z₂ = 2‖A‖`: the more modes you add, the *worse* the certificate gets.

The really unforgiving number is the **certification budget** — the largest defect
these bounds could tolerate and still close:

    Y₀_max = (1 − Z₀ − Z₁)² / (4 Z₂)

It is **exactly zero at every truncation**. Not small. Zero. There's no gap to
close by working harder, because there's no gap.

The best profile our genetic algorithm found near the interesting parameter value
has a residual of about `10⁻²`. We had been quietly worried that this was too big
to certify. That worry turns out to have been beside the point. The apparatus can't
certify a defect of `10⁻²`, but it also can't certify a defect of **zero** — and
the anchor we tested has a defect of exactly zero, because it's an exact solution
known in closed form. The failure isn't about accuracy at all.

## Ruling out the prime suspect

We'd flagged two things that could go wrong. The one we'd called "the crux" was the
**gauge** — the bookkeeping that removes the problem's built-in symmetries. This
equation has a two-parameter family of solutions (you can scale the profile and you
can stretch it), so the linearized operator is automatically singular until you pin
those down. Get that wrong and everything downstream is meaningless.

So we tried three completely different ways of pinning it down. All three give the
same growth, `N^0.97`, right on top of each other. The gauge is fine. Whatever is
breaking this, it isn't that.

## The actual culprit, caught in the act

The other suspect was a footnote. To turn an infinite line into something a
computer can handle, we compactify it: `X = tan(θ/2)` wraps the whole real line
onto a circle, with `X = ±∞` landing at `θ = ±π`. It's a standard trick and it made
everything else beautiful — the Hilbert transform becomes trivially diagonal, the
linearized operator becomes tridiagonal.

But the transport term picks up a factor:

    ∂/∂X  =  (1 + cos θ) · ∂/∂θ

and `1 + cos θ` **vanishes at `θ = ±π`**. Exactly where infinity lives. We noted it,
flagged it as a thing to check, and moved on.

So we ran the cleanest test we could think of: rebuild the entire ladder with that
factor replaced by `1`. Change nothing else. It's not a physical equation any more —
it's a control, removing exactly one feature.

| modes `N` | true operator | `1 + cos θ` → `1` |
|---|---|---|
| 4 | 5.0 | 4.0 |
| 64 | 50.9 | 4.0 |
| 256 | 198.7 | 4.0 |

Flat. Perfectly flat, at 4.0, all the way out. The growth doesn't shrink — it
disappears. That's about as clean as causal attribution gets in numerical work: the
footnote was the whole story.

There's an algebraic version of the same fact that's almost prettier. The far field
of the operator is multiplication by the symbol `1 + cos φ`. Its total size is
exactly **twice** its diagonal part — precisely because it touches zero at `φ = π`.
That factor of two is what puts `Z₁` exactly at `1` instead of comfortably below
it: not a near miss, a dead heat. We checked whether re-weighting the space could
tip it. It can't, and we can prove it can't: the required condition forces a
recursion whose roots sit exactly on the unit circle, so any weight satisfying it
oscillates and goes negative. Marginal, permanently, by construction.

## What's on the other side of the wall

Here's the part that makes this worth writing up rather than filing away.

Ask what the operator does out at large `X`. It's essentially

    −c · h′(X) − h(X)/X  =  g(X),

a first-order ODE you can just solve: `h(X) = 2X⁻² ∫ s² g(s) ds`. Do the
bookkeeping and it says the inverse **amplifies by one power of `X`** — feed it
something that decays like `1/X²`, get back something that decays like `1/X`. The
inverse loses exactly one power of decay.

That's a prediction with a number attached, and the compactification converts it
into one we can check directly: mode `m` resolves the scale `X ~ m`, so the
amplification of mode `m` should grow like `m`. Measured:

    ‖A e_m‖  =  1.97 · m

Slope 2, to within 2%. The unbounded inverse and the linear growth in the table
above are the same fact, and now it's an explained fact rather than an
observed one.

And an explained obstruction tells you what to do. If the inverse loses exactly one
power, then stop asking it to map a space to *itself* and ask it to map between two
spaces one power apart. Re-measure with the target space weighted by that one
power:

    ‖A‖  =  3.000,  3.000,  3.000,  3.000, …    (N = 8, 16, … 384)

Constant. Not "roughly constant" — 3.000 at every truncation we tried. The operator
was invertible the whole time. We were measuring it in the wrong space.

## Where this leaves things, honestly

Nothing here is a proof of anything. All of it is ordinary floating point — we
deliberately didn't spend the effort on guaranteed arithmetic, and running the
rehearsal first is exactly what saved that effort.

What the leg produced:

- The naive version of the certification **cannot work** — not at any truncation,
  not with any of the gauges, not with any weighting. That's a structural
  statement, not a "we didn't try hard enough."
- The blocker is the far field at `X = ∞`, established by ablation rather than
  suspicion. The suspect we'd been most worried about, the gauge, is cleared.
- The repair is identified and measured: an asymmetric pair of spaces one decay
  power apart, in which the relevant constant is `3.000` flat.

That last point is a *specification for the next attempt*, not a promise it will
work. Two things still have to be redone in the new setting, and neither is free:
the quadratic term has to be shown to land in the right space, and the far-field
inverse has to be made rigorous rather than asymptotic. This is the familiar
"compact core plus explicit far field" structure that computer-assisted proofs in
this area end up needing. The honest reading is that we've arrived at the point
where that structure becomes necessary — and, unusually, we know precisely why.

We also found a small bug in the previous post's code while doing this: one
coefficient in the closed-form operator was wrong by a factor of two, in a column
the old cross-check never touched. Two independently written versions now agree
exactly. It didn't change any conclusion, but it's the sort of thing that only
surfaces when you build the same object twice — which is a decent argument for
building things twice.

Still a 1D toy model of the boundary behaviour of a 3D problem. Still nowhere near
Clay. The odds on that haven't moved: about 0.05%. What moved is that one plausible
route is now closed with a reason, and its replacement has an address.
