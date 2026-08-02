# The number that says why Navier–Stokes is hard

*Route-F v1 — the critical dissipation exponent, and a cross-check between two computations
that share nothing.*

Here is the sentence everyone writes about the Navier–Stokes problem, and almost nobody makes
quantitative:

> *any real proof has to beat viscosity at small scales.*

It is true, and as stated it is useless. So this leg turns it into an equation with a measured
right-hand side, in a model where the arithmetic is checkable.

---

## The dial

Take gCLM — a 1D caricature of the vorticity equation with an advection dial `a` — and give it
adjustable dissipation:

```
ω_t + a u ω_x = ω u_x − ν (−Δ)^s ω ,       u_x = H(ω)
```

`s = 1` is ordinary viscosity. `s` is the knob. The question is where, as `s` rises, dissipation
stops losing.

The scaling argument is three lines and it is worth doing slowly, because the answer turns out to
be something I had already measured for an unrelated reason.

A self-similar blow-up has amplitude `ω ~ (T−t)^{−1}` and a length scale `L ~ (T−t)^β`. The
nonlinearity is `~ ω²`. The dissipation is `~ ν ω / L^{2s}`. So

```
dissipation / nonlinearity  ~  ν (T − t)^{1 − 2sβ}
```

and the blow-up wins exactly when `1 − 2sβ > 0`, i.e. `s < 1/(2β)`.

Now, `β`. In the previous leg I built a dynamically-rescaled solver to ask a completely
different question (whether a periodic orbit could bifurcate off the self-similar profile — it
can't). Its by-product was `α`, the profile's **far-field decay exponent**: `Ω ~ X^{−α}`. And the
rescaling ODEs give `β = 1/α`. So:

```
s_c(a) = α(a) / 2
```

**The critical dissipation exponent is half the far-field decay exponent.** The rate at which
the profile decays *in space* determines whether the blow-up beats viscosity *in time*.

---

## Why this is the Navier–Stokes sentence

Navier–Stokes has a natural scaling: `L ~ (T−t)^{1/2}`, i.e. `β = 1/2`, i.e. `α = 2`. Put that
in:

```
s_c = 1 .
```

**Exactly the ordinary Laplacian.** Navier–Stokes sits precisely on the line where neither term
wins — which is not a coincidence and is not bad luck; it is what "critical" means, and it is why
the problem is hard. Every scaling argument you can make about NS returns exactly zero
information, because the two sides balance identically.

In gCLM, by contrast, `α` is a *measured function of a dial*. It runs from 1 upward. So the
family walks through the point where NS is stuck, and you can watch what happens on both sides.
That is the whole value of the toy: not that it blows up, but that it is *off-critical in a
controlled way*.

---

## Measuring an exponent instead of a threshold

The obvious experiment — sweep `s`, see where blow-up stops — is exactly the experiment this
project has learned not to run. Near a critical exponent the blow-up is only *asymptotically*
dissipation-free, so at finite compute the apparent threshold is biased, resolution-dependent,
and biased *in the direction you expect*. That is three ways to fool yourself in one measurement.

So instead: track `D/N`, the ratio of the dissipative to the nonlinear term at the peak, and fit

```
D/N ~ (T − t)^p ,     prediction:  p = 1 − 2s/α
```

This predicts a whole **line**, not a threshold. Its slope, its intercept and its zero crossing
are separately checkable, and the zero crossing *is* `s_c`. Measuring a line is a far stronger
test than locating a transition by eye.

**One thing had to be fixed first.** Dissipation *delays* the blow-up, so fitting against the
inviscid singular time `T₀` biases everything: every point came out above its prediction, with a
shallower slope and a zero crossing ~10% high. That pattern — a *uniform* offset with a slope
error — is the signature of a wrong singular time, not a wrong exponent. The fix is that each run
supplies its own `T`: for `ω ~ 1/(T−t)`, `1/amp` is linear in `t`, so extrapolate it to zero. On
the inviscid case, where `T` is known exactly, that recovers it to `3e−5`.

---

## The result, at the point where nothing is fitted

At `a = 0` the model is exactly solvable — `z = z₀/(1 − t z₀/2)` with `z = H(ω) + iω`, which
holds on the circle too (checked against an independent RK4 to `2e−14`). And `α = 1` *exactly*:
the self-similar profile is a single Fourier mode. So the prediction `p = 1 − 2s` has **no fitted
input at all.**

| `s` | 0.15 | 0.25 | 0.35 | 0.45 | 0.55 | 0.65 | 0.75 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| measured | +0.733 | +0.523 | +0.318 | +0.109 | −0.100 | −0.309 | −0.503 |
| predicted | +0.700 | +0.500 | +0.300 | +0.100 | −0.100 | −0.300 | −0.500 |

Slope `−2.068` against `−2`; zero crossing at `s = 0.5033` against `1/2`. And `s_c(0) = 1/2` is
the classical critical exponent for dissipative CLM, so this is a known-answer gate rather than a
self-consistency check.

### The honest error bar

The dominant systematic is the fit window, and it is swept rather than chosen — because `p` is an
*asymptotic* statement, an early window hasn't got there and a late one is noise:

| window | 0.20–0.80 | 0.30–0.92 | 0.40–0.94 | 0.50–0.95 | 0.60–0.98 |
| --- | --- | --- | --- | --- | --- |
| slope | −1.896 | −2.043 | −2.068 | −2.074 | −2.001 |
| zero | 0.568 | 0.518 | 0.503 | 0.498 | 0.478 |

> **slope = −2.02 ± 0.09** (predicted −2)  ·  **`s_c` = 0.51 ± 0.05** (predicted 0.500)

Individual exponents move by ±0.07 across windows, approaching the prediction *monotonically from
above* — which is what entering an asymptotic regime looks like. The slope is much steadier,
because every `s` shares the window and the bias cancels in the difference. That is why the
claims here are about the slope and the zero, not about any single number.

---

## The part I actually like

`α` was measured by a **steady spectral solve, compactified, on the whole line**, in a different
module, for a different question. The slope `dp/ds` is measured by **time-dependent
pseudo-spectral simulation on a periodic domain with dissipation**. These two computations share
no grid, no basis, no formulation, and no fitted constant. The scaling relation says the second
should be `−2/α` of the first.

| `a` | 0.0 | 0.2 | 0.3 | 0.4 |
| --- | --- | --- | --- | --- |
| `α` (steady, on the line) | 1.0000 | 1.3345 | 1.6172 | 2.0795 |
| `−dp/ds` (time-dependent, periodic) | 2.084 | 1.519 | 1.256 | 0.978 |
| ratio to `2/α` | 1.042 | 1.014 | 1.016 | 1.017 |

**The ratio is 1.022 ± 0.014 while `α` itself doubles.** A uniform 2% bias, not an `a`-dependent
failure — the *shape* of the relation is confirmed to sub-percent by an instrument that knows
nothing about the one that produced `α`.

That is worth more than either leg's internal error bar. Refining one computation can't test the
other; agreement across two unrelated ones tests both.

---

## The map, and the sentence to be careful with

Putting the measured `α(a)` into `s_c = α/2`:

| `a` | 0.0 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 |
| --- | --- | --- | --- | --- | --- | --- |
| `s_c` | 0.500 | 0.571 | 0.667 | 0.809 | **1.040** | **1.500** |

`s_c` crosses **1** — the ordinary Laplacian — at `a ≈ 0.383`. Above that, the scaling says the
blow-up beats ordinary viscosity.

Now the careful version, because this is the sentence that would be misquoted.

It is a statement about **gCLM's own scaling**, and it is **not** a statement about
Navier–Stokes. It does not say that a viscous gCLM blow-up *exists* above `a ≈ 0.383` — the
scaling says which term dominates *given* the self-similar form; showing a solution actually
reaches it is the entire difficulty, here as everywhere. And NS's `α` is not a dial: it is pinned
at 2 by dimensional analysis, which is precisely why NS gets no free information from this kind
of argument.

What the map is genuinely good for is **orientation**: it shows what the NS difficulty is *made
of*, by exhibiting a family that walks through it. NS is the marginal member of a family whose
non-marginal members are computable.

---

## What it cost

One module, one experiment, six gates, and three attempts at the resolution guard before I had an
honest one. (Energy above ⅔ of `k_max` reads exactly `0.0` at some grid sizes, because the
dealiasing already zeroed that band — a guard that is zero by construction reads as "perfectly
resolved". Energy above `n/6` reads `0.37` for every run, resolved or not, because a
near-singular spectrum genuinely is fat. What discriminates is the amplitude *at the cutoff*
relative to the peak: `1.0` at `n = 1024`, `1.4e−2` at `n = 4096`, `2.0e−4` at `n = 8192`. Now
the run refuses rather than returning a number off an unresolved state.)

And the standing honesty, unchanged: **none of this is Clay progress.** It moves no link of the
chain. It does not certify anything. What it does is take one sentence that everybody writes
about why the problem is hard, and give it a measured right-hand side in a place where the
measurement is possible. Odds unchanged, ~0.05%.

The lesson I'll carry: **look for a second, structurally different route to a number you already
have.** `α` had been sitting in the previous leg's data file as a by-product. Used once, it was a
curiosity. Used twice, by two instruments with nothing in common, it became a check on both.
