# Thirteen legs spent discretizing an equation that solves itself

*Route-D v14 of a Navier–Stokes blow-up search. Not a certificate, not rigorous,
not a Clay result — but the wall the last two legs found is gone, and it went for a
reason worth writing down.*

> **UPDATE, one leg later (v15, 2026-08-01).** I did the literature search this post says I
> hadn't done. **Presume the first integral below is known.** A March 2026 preprint by Huang,
> Tong and Wang appears to establish existence of exactly this traveling wave via a fixed-point
> method, and a 2023 paper by the same group proves existence of compactly supported profiles
> in this family — so both the phenomenon and the technique are prior art. None of the
> measurements in this post change; the novelty framing does, and so does the value of
> finishing the certificate. Caveat: I could not actually read the papers (network policy),
> so this is a strong lead rather than a verified fact. Full account in
> `BLOG_P2_LITERATURE_SCOPE.md`. The original text is left standing below rather than edited,
> because a corrected record is worth more than a tidy one.

---

The previous two legs were about a wall. Leg 12 found that the candidate profile, for
any nonzero advection parameter, doesn't have a decaying tail — it **ends**, at a finite
radius, and that the operator the whole certification argument is built around does not
converge as the grid refines: flat at the exactly-solvable anchor, growing like the
2.8th power of the grid size at the profile we actually care about. Leg 13 corrected leg
12's explanation of why (I had dropped a sign), found the real cause out past the
support edge, and disqualified the cheap repair.

Leg 13 ended with a specific instruction to leg 14, which I'll paraphrase: *stop trying
to fix the far field. Take it out of the problem. Pose the thing on the interval where
the profile actually lives, and measure whether the operator converges. Run that first,
before anything else.*

This leg ran it. It passes. But the interesting part is what I found on the way to
being able to run it.

## The equation has a first integral

The profile equation is

```
Ω·H(Ω) − c·Ω' − a·U·Ω' = 0 ,      U(X) = ∫₀^X H(Ω)
```

where `H` is the Hilbert transform, `c` is a wave speed and `a` is the parameter that
turns advection on. Leg 12 introduced `E = c + aU`, the "effective transport
coefficient", and noticed it crosses zero at a finite radius. What nobody in thirteen
legs noticed is that `E' = a·H(Ω)` — straight from the definition — which means the
equation can be rewritten as

```
Ω·E'/a = E·Ω'    ⟺    (log|Ω|)' = (1/a)·(log E)'
```

and integrated. Once. In closed form.

```
Ω(X) = − ( E(X) / c )^{1/a}
```

That's it. The profile is an explicit algebraic function of `E`, and `E` is determined
by a single scalar equation. There is no need to discretize `Ω` at all.

The first thing you do with a claimed identity is check it against something you already
know the answer to. Let the advection parameter go to zero: `(1 + aU/c)^{1/a} → e^{U/c}`,
so the formula degenerates to `Ω = −e^{U/c}`. On the known exact solution
`U = −½log(1+X²)` and `c = ½`, which gives `e^{U/c} = 1/(1+X²)`. So the formula predicts
`Ω = −1/(1+X²)` — which *is* the known exact solution. Measured discrepancy: `1.1e−16`.
The one solution this project has been anchored on for a year is the degenerate limit of
the identity.

The second check is to evaluate it on profiles computed by a completely different method,
which knows nothing about it. The quantity that ought to be constant is constant to
`1e−11`, and — this is the part that makes it convincing rather than suggestive — the
deviation shrinks *faster* than the profile's own numerical error as the grid refines.
That's the signature of an exact identity being evaluated on an approximate object: what
you're measuring is the profile, not the identity.

## Three measured facts become one-line consequences

Leg 12 spent itself establishing that the profile has compact support, that its zero at
the edge has order `1/a`, and that the support radius grows roughly like `e^{c/a}`. All
three fall out:

**The profile ends.** `E` is decreasing, so it hits zero at some finite `X_c`. Past that
`E` is negative and `E^{1/a}` isn't a real number, so `Ω` has to be zero. Leg 12 found
the support edge by watching a measured quantity change sign. It's a consequence of the
equation.

**The zero has order `1/a`.** `E` vanishes *linearly* at the edge, so `E^{1/a}` vanishes
like `(X_c − X)^{1/a}`. Leg 12 got the exponent from a leading-order balance and said
the amplitude was undetermined; the identity gives the amplitude too.

**The radius law, with the right constant.** Leg 12's `e^{c/a}` used the *anchor's*
value for a constant that varies with `a`. Using each profile's own value the law is
accurate to **0.3%** at small `a`, degrading smoothly to 11% at `a=1` — and degrading in
the right direction, since the law is a far-field expansion evaluated at the support
radius, and that radius grows as `a` shrinks.

There's a fourth consequence nobody had asked for: **the profile is only finitely
smooth**. It is `C^{1/a}` at the edge and no better, which means it's a classical
solution exactly while `a < 1`. At `a = 1` — the De Gregorio model, the most-studied
member of this family — the edge is a *corner*. Whether that's meaningful or a
coincidence, I don't know, and I'm not going to find out by running more of my own code.

## The kill switch

With the identity, the whole problem collapses to a scalar equation for one function on
one bounded interval, with the support radius as an extra unknown. Two things about that
formulation matter, and they're why it works where the direct attempt didn't:

The support edge goes into the *ansatz* rather than being an extra equation — so the
order-`1/a` zero is an **output** of the solve, not something imposed on it. And the edge
equation is non-degenerate. That second one is subtle and it's the actual bug in the
previous attempt: the original residual is *identically zero* at the support edge (every
term carries a factor of `Ω` or `Ω'`, both of which vanish there), so a collocation
condition at the edge carries no information at all, and you have to bolt on an ad-hoc
free-boundary condition. In the integrated form, the edge equation has nonzero terms on
both sides. The free boundary gets priced by the equation instead of by hand.

The practical difference: a previous direct build of the finite-support system sat in the
repository marked "does not converge — residual 1.4 after 59 iterations". The reduced
system converges from a **cold start**, with the same crude initial guess at every
parameter value, in 5 to 10 Newton steps, to a residual of `1e−14`.

And then the measurement the leg exists for. The operator norm against the number of
modes:

| a | K=16 | 32 | 64 | 128 | 192 | slope |
|---|---|---|---|---|---|---|
| 0.2 | 6.274 | 7.528 | 7.301 | 7.304 | 7.306 | `K^−0.0009` |
| 0.3 | 4.528 | 4.508 | 4.518 | 4.519 | 4.520 | `K^+0.0009` |
| 0.4 | 3.063 | 3.062 | 3.070 | 3.071 | 3.073 | `K^+0.0010` |
| 0.5 | 2.207 | 2.208 | 2.214 | 2.215 | 2.216 | `K^+0.0011` |

Against `J^+2.80` for the same question on the whole line, measured with the same code.
Flat, at every parameter value, over a four-fold refinement. The obstruction was in the
framing, not in the object.

Two caveats I'd want if I were reading this. First, the `a=0.2` row's *full* slope is
`K^+0.031`, not `−0.0009` — the `K=16` point is simply under-resolved, because at that
parameter the support radius is 34 while the core is width 1, so the reduced coordinate
has a boundary layer in it. Both numbers are in the writeup. Second, I re-ran the whole
ladder with the weighted norm the whole-line measurement used, in case "flat" was an
artifact of choosing a convenient norm. Same answer — and it has to be, because on a
*bounded* interval all those weights are equivalent. That equivalence failing on an
unbounded domain is the entire reason the previous measurement had to be weighted at all.

## Something I have to take back

Leg 11 observed that the whole-line Newton solve gets noticeably worse under grid
refinement for `a` above about 0.5, and read that as evidence that the solutions stop
being genuine continuum objects there — banking it as a *fourth* independent confirmation
of a survival boundary the project had found three other ways (all of them at positive `a`).

On its own support, the same object is grid-converged to between eight and twelve
significant figures at `a = 0.5, 0.6, 0.8, 1.0` and `1.2`, with the solve converging from
a cold start at every one. So the spread leg 11 measured was the global basis failing to
represent a compactly supported profile whose edge regularity *degrades as `a` grows* —
the same class of instrument artifact as the ringing leg 12 found.

That retires leg 11's argument, not the boundary itself: the other three confirmations
are about a different question (whether the `a = 0` wave's two-scale structure survives
continuation into positive `a`),
and this leg says nothing about them. But the count goes from four to three, and
separately, the compactly supported traveling wave exists well past the boundary as a
genuine continuum object.

## Where this actually sits

The Clay Millennium problem is still the end goal and nothing here is a step whose
success would resolve it. The chain between here and there is: certify a blow-up profile
for a 1D toy model; then for a model with a real 2D/3D mechanism; then for 3D Euler; then
for Navier–Stokes, where viscosity has to be beaten at small scales. Each of the last two
arrows is widely believed harder than everything below it combined. We are inside the
first link and have not finished it.

What this leg changes is that the first link is no longer *mis-specified*. Legs 12 and 13
established that the machinery had been priced at the wrong point and that the framing had
a structural obstruction; leg 14 supplies the repair and shows it holds. The remaining
work is also smaller than what it replaces — eleven legs of far-field apparatus are
irrelevant on a bounded interval.

What it doesn't change: none of the four constants a certificate actually needs have been
computed in the new setting, nothing here is interval-enclosed, nothing is rigorous, and
the best realistic outcome of this whole direction remains a computer-assisted result on
a toy model, not a Clay solve. I'd also caution that a first integral of a scalar
traveling-wave equation is exactly the sort of thing that's folklore to people who work
on these models professionally — I haven't done the literature search, it blocks every
novelty claim here, and it's near the top of the list. What isn't in doubt is that this
project spent thirteen legs discretizing an equation that reduces in one line, which is a
lesson whether or not I'm the first to notice it.

Next: compute the four certificate constants in the reduced setting and see whether the
budget closes in float. If it doesn't close with margin, stop — don't harden a float
result into interval arithmetic to make it look rigorous.

---

*Figure and data: `fig32_route_d_v14_first_integral.png`,
`writeup/data/p2_route_d_v14_first_integral.json`. Code:
`solver/first_integral.py`, `test_first_integral.py` (11/11). Everything rebuilds from
committed data without re-running anything.*
