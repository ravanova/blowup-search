# The blow-up that collapses too fast

*Route-G v1 — porting the viscosity question from the 1D toy to the 2D system it is a model
of, and finding out the toy is on the other side of the line.*

Last leg I measured, in a 1D model, the dissipation strength at which a blow-up stops beating
viscosity. The answer came out as `s_c = α/2`, with `α` the far-field decay exponent of the
self-similar profile — a clean number, cross-checked against an unrelated computation, and I
was pleased with it.

This leg took the same question to the 2D system. Two things happened. The formula turned out
to be written in the wrong variable, and once it was rewritten it said something about the
whole programme that I had not expected.

---

## The formula was a coordinate choice

Here is the argument, and it is three lines. A self-similar blow-up has an amplitude and a
length scale:

```
ω ~ (T−t)^{−1},        L ~ (T−t)^β.
```

The amplitude exponent isn't a choice — `ω_t ~ ω²` forces it. Compare the dissipation
`ν ω / L^{2s}` against the driving term `~ ω²`:

```
dissipation / driving  ~  ν (T−t)^{1 − 2sβ}
```

and the blow-up wins exactly when the exponent is positive:

```
s_c = 1/(2β).
```

That is the whole law. `α/2` was this formula written in gCLM's own gauge, where the rescaling
happens to pin one constant to 1. In 2D that constant is `3.006`, and `α/2` is simply wrong
there while `1/(2β)` is unchanged. I had a coordinate choice sitting where a law was supposed
to be, and only a change of model made it visible.

The two exponents are the same fact, incidentally, which is the part I like. Ask that the
blow-up not disturb the solution far away from it — the outer flow shouldn't know a singularity
is forming — and you get `α = −1/β` directly. "The profile decays like `r^α` far out" and "the
structure collapses like `(T−t)^β`" are one statement in two variables.

---

## Navier–Stokes is the line

Now put Navier–Stokes into it. NS's length scale goes like `(T−t)^{1/2}` — that is dimensional
analysis, not a modelling assumption, and it is not adjustable. So `β = 1/2`, and

```
s_c = 1/(2 · 1/2) = 1 — the ordinary Laplacian, exactly.
```

Navier–Stokes sits precisely on its own critical line. This is a familiar fact wearing a new
outfit, but the outfit is useful: it says `β = 1/2` is *the* line, and every blow-up scenario
can be scored by which side of it it lands on.

And here is the part that reads backwards until you stare at it. `s_c = 1/(2β)` is **decreasing**
in `β`. A blow-up that collapses **faster** is **easier** for viscosity to kill.

I had to check that twice. The intuition — a more violent singularity should overwhelm
viscosity — is wrong, and it is wrong for a specific reason. The violence in the *amplitude*
is fixed: everything in this class blows up like `(T−t)^{−1}`. All the freedom is in how small
the structure has to become to get there. A structure that reaches the same amplitude on a
*larger* length scale is the one viscosity cannot reach, because viscosity is a derivative
count and derivatives are what small scales are made of.

So beating ordinary viscosity requires `β < 1/2`: a blow-up that collapses **more slowly** than
the Navier–Stokes rate.

---

## Where the proven 2D blow-up actually sits

The Chen–Hou boundary blow-up for 2D Boussinesq is the real thing: a proven, computer-assisted
singularity in the Hou–Luo geometry, and the object this project's 1D model is a caricature of.
Its rescaling constants are published, and `β = −c_l/c_ω` reads straight off them:

```
β = 2.92,     s_c = 0.171.
```

Nearly six times the Navier–Stokes collapse rate — on the losing side of the line by a wide
margin. At the ordinary Laplacian its relevance exponent is `1 − 2β = −4.84`, meaning the ratio
of dissipation to driving doesn't creep up as the singularity forms, it *explodes*.

That is not a criticism of Chen–Hou. Their theorem is about Euler and about a system with no
viscosity in it, and it is a genuine landmark. It is a statement about the **distance between
the toy and the target**, and it is the first number this project has that measures that
distance on the 2D object rather than by analogy.

I did not want to take it on the paper's word, so I re-measured it with the machine Spike 1
built a month ago: relax the dynamically-rescaled 2D Boussinesq system to its steady profile and
read `β = −c_l/c_ω` off the modulation constants.

It came out at **2.981**, against the published 2.921. Two percent off — and that is worse than
it should be, so I went and found out why.

The machine computes `c_ω`. It does *not* compute `c_l`: the normalization **pins** `c_l`, and
you set it. It is supposed to be `3.00650`. Its discrete readout is `3.0637` — a 1.9% quadrature
bias in the origin-slope operator. And `β = −c_l/c_ω` inherits that in full. Meanwhile `c_ω`,
the number the machine actually produces, lands at `−1.0276` against `−1.02943`: **0.18%**.

So the honest version has two numbers in it. As read, `β = 2.981` (2.1% off). Holding `c_l` to
the value the gauge is *set* to, `β = 2.926 ± 0.011` and `s_c = 0.1709` — 0.18% from published.
Both go in the writeup, because the correction is a choice about the gauge, and hiding a named
1.9% systematic behind a better-looking number is precisely what this project's discipline
exists to stop.

Resolution-stable, too: doubling the radial resolution and extending the domain tenfold moves
`β` by 0.025.

---

## The measurement I could not make

The obvious thing to do was repeat exactly what worked in 1D: run the time-dependent system
with fractional dissipation, track `D/N` at the peak, fit `(T−t)^p`, and read the exponent.

It does not port, and the reason is worth recording because it is not subtle and I did not
anticipate it.

The 2D run does everything right except last long enough. Starting from a grower that an
earlier Phase-1 experiment had already labelled as blowing up, the amplitude grows about 90×
before the spectral resolution guard fires, and its amplitude exponent is `−1.12` — it *is* in
the regime the prediction is about. But that window spans **0.77 decades of `(T−t)`**, where
the 1D leg had nearly four. Fit `β` on the early, middle and late thirds of it and you get
`1.67`, `2.06`, `1.08`. That is not a measurement with error bars; it is a measurement of the
window.

So the code refuses. `collapse_window_report` returns `measurable = False` and the two numbers
that make the call, and no `β` comes out. I'd rather have that than a plausible-looking number
with a factor-of-two systematic hiding inside it.

The interesting part is the exchange rate, which I worked out instead of guessing. Decades of
`(T−t)` are bought with resolution, and the price is set by `β` itself: resolving `L` a factor
`R` smaller buys `R^{1/β}` in time-to-singularity, so **one extra decade costs `10^β` in linear
resolution**. The refused fit still brackets `β` between 1 and 2, and Chen–Hou's object sits at
2.92, so one decade costs somewhere between 10× and 832× per direction — in 2D, between a
hundred and seven hundred thousand times the grid points. Going from 0.77 decades to a usable
2.5 costs roughly 1300× per direction at the low end of that bracket.

(Refusing to quote a value is not the same as learning nothing: the pricing only needs the
bracket, and the bracket is solid.)

That is not a grid anyone buys. It is a fairly complete explanation of why this whole subfield
runs on dynamic rescaling.

The repair isn't more grid. It is a different instrument — and dynamic rescaling is exactly
that instrument, which is why the number in the previous section exists at all. In the rescaled
frame the collapse exponent is a *modulation constant*, computed from origin slopes at every
step. No fit, no window, no singular-time estimate. The measurement that the direct route
cannot make, the rescaled route makes without trying.

---

## The uncomfortable part

The 1D model has `β` on a dial: `β(a) = 1/α(a)`, and Route-E measured `α(a)` across the family.
Over the range this project has worked in — `a` from 0 to 0.5 — `β` runs from 1.00 down to 0.33,
crossing the Navier–Stokes line `β = 1/2` at `a ≈ 0.383`.

The 2D object it is supposed to model sits at `β = 2.92`.

That is not in the range. It is not close to the range. **PLACEHOLDER-E**

I want to be careful about what this does and does not mean. It does *not* mean the 1D model is
a bad model — gCLM was never claimed to reproduce the 2D collapse rate, and it is a model of the
*boundary mechanism*, not of the exponents. What it does mean is that a specific and tempting
inference is unavailable: **"we tuned the toy to where it beats ordinary viscosity" is not a
statement about the 2D scenario**, because the toy's `β` and the target's `β` are on opposite
sides of the line and a factor of six apart. Nobody had claimed otherwise in writing. But the
map in the previous leg made `a ≳ 0.383` look like a destination, and this leg is what says
where that destination is relative to the thing we care about.

---

## What this was worth

No link of the chain moved. No certificate was produced. What the leg bought:

- the law in a form that survives a change of model, with the gauge-dependence of the old form
  identified and gated;
- the observation that faster collapse *loses* — a sign I would have got wrong if asked to guess;
- a number for the 2D object, measured twice (published constants, and our own machine);
- an honest negative on the direct method, with the cost of repairing it priced;
- and a calibration between the toy and its target that says the two are further apart, in the
  one respect this question cares about, than the family map suggested.

Clay odds unchanged at ~0.05%. This is orientation, not evidence about Navier–Stokes. But it is
orientation on the right object for the first time.
