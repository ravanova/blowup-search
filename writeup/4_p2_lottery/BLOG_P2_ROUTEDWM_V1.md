# The gap is not padding — it's the distance between a derivative count and a discriminant

*Leg 305 (Route-DWM). Figure: fig82. Data: `writeup/data/p2_route_dwm_v1.json`.
Technical companion: `TECHNICAL_P2_ROUTEDWM_V1.md`.*

## The setup

There is a proof — Buckmaster, Cao-Labora and Gómez-Serrano's
[2208.09445](https://arxiv.org/abs/2208.09445) — that builds smooth imploding solutions for 3D
**compressible** fluids. To carry the construction from Euler across to Navier–Stokes, it has
to show the viscous term is *dominated* by the profile it has just built. That domination only
works for a band of self-similar speeds `r`, and at `γ = 7/5` the band is

```
certified band   (1.1666667, 1.1909830)     width 0.0243
band you'd want  (1, 1.1666667]             width 0.1667
```

The band you want is **6.854×** wider than the band you get. An earlier leg here pinned that
number down (it is exactly `(7+3√5)/2`, and a transcribed `6.855` that had spread through the
repo was caught and corrected). But nobody knew what kind of number it was.

That distinction matters more than it sounds. A `6.854×` shortfall could be one of two very
different things:

1. **Padding.** Somewhere in the derivation sits a generous constant — a Sobolev constant taken
   at its textbook value, a factor of 2 kept for convenience. Sharpen it and the band widens.
   Gaps like this close all the time.
2. **Structure.** The two endpoints are exact, and the distance between them is a fact about the
   equation rather than about the argument.

You cannot tell which by looking at the number. You have to take the derivation apart.

## What we did

We re-derived both endpoints from scratch, deliberately through **different equations** than the
earlier leg used — the earlier one evaluated the paper's closed-form answer; we root-solved the
upstream quantity five pages later whose vanishing is what *produces* that answer. Then we
exposed all eleven intermediate constants as knobs, turned each one at a time, and measured how
much the band widened.

Everything in 60-digit arithmetic, for a specific reason. This corner of the paper contains a
nasty trap: one expression is a sum of terms as large as `24.5` that cancels to *exactly* zero
at `r = 1`. In ordinary double precision that zero shows up as `1.2e-14` of rounding dust, and
taking its square root throws away half the remaining digits. A previous leg hit this and
correctly diagnosed it as broken arithmetic rather than a broken paper. We reproduced the trap
on purpose — our float path is off by `1.4e-07` where it should be exact — kept the number
clearly labelled as a diagnostic, and let nothing depend on it.

Before measuring anything we wrote down, in a commit of its own, the tolerances, the known
answers we had to reproduce, and the rule that would decide "sharp" versus "slack". That is the
only way the answer could genuinely have come out either way.

## What came back

**The endpoints reproduced.** Independently, to within `3.3e-8` and `5.6e-9` of the previously
banked values, and against the paper's closed form to **exactly zero** across twelve values of
`γ` spanning both of its branches. The transcription is faithful.

**Every one of the eleven constants is an exact identity.** Not one is an estimate. They are
derivative counts, the ideal-gas exponent, and polynomial coefficients of a discriminant. There
is no padding to squeeze, because there is nothing in the derivation that was ever a choice.

**The costliest constant is the `2` in the Laplacian.** It is the single most sensitive knob —
each 1% you move it changes the band by 13.7% — and it needs the smallest move to close the gap:
**−42.7%**, from `2` down to `1.145898`, which is exactly `(9 − 3√5)/2`.

And that is the punchline, because `2` is *the number of spatial derivatives in `Δ`*. Moving it
to `1.145898` means replacing viscosity `νΔ` with **hypodissipation** `ν(−Δ)^s` at
`s = 0.5729…` — less than half a Laplacian. You have not found a sharper proof. You have changed
the equation.

**The other endpoint cannot be moved at all.** All seven constants in the upper-endpoint
machinery came back *unreachable*, and the reason turned out to be geometric: `r*` is exactly
where two points of the phase portrait collide and stop existing. It is a discriminant, not an
estimate of a threshold. You can push the upper endpoint down; nothing pushes it up. We measured
this rather than assumed it — perturb by `ε` and the endpoint moves by `ε²`, the signature of
sitting exactly at a stationary maximum, and it came out at `p = 2.00` on all seven.

There is also a counting version of the same gap. The paper's admissible speeds are not a
continuum — they are a discrete list `r₃, r₅, r₇, …`. Sixteen of them fall below the dominance
threshold, seven of those odd. **The first seven odd profiles the Euler theorem produces have no
Navier–Stokes counterpart under this argument.** The first one that survives is the seventeenth.

## One tolerance failed, and we kept it

We had pre-registered a linearity check that we expected to pass. It failed. It would have been
easy to quietly restrict it to the constants where it worked.

Instead we chased it, and it turned out to be the finding arriving a second time by a different
route. When a quantity sits at a stationary maximum, its two-sided derivative is proportional to
your step size, so halving the step halves the answer and the "relative deviation" is exactly
`0.9`. We measured `0.899` on all seven affected constants. The failing tolerance was reporting
the flatness we had just discovered. We left it recorded as failed, added a separate check
*declared as separate*, and wrote down why.

## What this does and does not mean

**It does not** mean imploding compressible Navier–Stokes solutions only exist in the narrow
band. It means *this argument* only reaches the narrow band, and no amount of sharpening its
constants will change that — because it has no constants to sharpen.

**It does** tell you the shape of what any replacement has to beat. A companion leg (315) asked
the complementary question — what machinery could certify the domination beyond the endpoint —
and found a candidate along with a real obstruction: the standard ODE-to-PDE bridge assumes
dissipativity, and this system is quasilinear hyperbolic. Read together: the gap will not close
by tightening an estimate, because there is no estimate in it; it would have to close by
certifying domination through a genuinely different mechanism, in a regime where the current
one provably does not apply.

**Standing caveats, unchanged.** Measuring the shape of an obligation is not discharging it —
nothing about the main chain of this project moves. And this is 3D **compressible**
Navier–Stokes, which is **not** the incompressible system the Clay problem asks about.
Clay odds ~0.05%, unchanged.
