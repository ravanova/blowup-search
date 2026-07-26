# Two currencies, one wall

*A technical blog post on what happened when we cashed in the escape hatch from the
last one. Sequel to [BLOG_PHASE1_GATE4.md](BLOG_PHASE1_GATE4.md); all numbers below
are built from committed evidence in
[`data/phase1_gsustained.json`](../data/phase1_gsustained.json), with the full record
in [`../PHASE1_GSUSTAINED_RESULTS.md`](../../PHASE1_GSUSTAINED_RESULTS.md).*

The last post ended with a fitness function dead on the table and a promise. We had
been ranking candidate blow-up shapes by `ν_crit` — the critical viscosity a
shape's vorticity growth just survives — and it had failed its own pre-committed
gate: the "best" shapes weren't the ones that grew, they were the ones that started
from a tiny initial vorticity `ω₀`, because `ν_crit` secretly tracks `1/ω₀²`. A
small-denominator cheat. We killed it.

But we thought we saw an escape hatch, and we said we'd try it:

> An **inviscid growth-rate currency** escapes both cheats: measure at `ν=0` (no
> viscosity term, so no dissipation wall) and as a growth *rate* over a mid-run
> window (a log-derivative, so it never divides by `ω₀`).

This post is what happened when we cashed it in. Short version: the escape hatch is
real, but it opens onto a narrower room than we hoped — and on the way in we nearly
got robbed by the exact same pickpocket.

## The refinement that was supposed to work

The inviscid rate had passed a quick probe but carried one flagged weakness:
*resolution-stability was only modest.* Its growth window was **fractional** —
`[0.5·t_res, t_res]`, half-way to the end of the trusted window to the end — and
that endpoint `t_res` moves as you refine the grid. So the window shifted with `N`,
and the fitness drifted with it.

The obvious fix, the one we committed to trying: use a **fixed** window in absolute
time, like the ultra-stable growth rate our resolution spike had already measured
(it converged to four decimals). Pin the window, kill the drift.

It doesn't work, and *why* it doesn't work is the whole story.

Watch what the blow-up shape actually does. Here is `log max|ω|` for `smooth_sharp`
— the labeled shape that genuinely blows up — sampled across its trusted window:

```
t:       0.5   1.0   1.5   2.0   2.25  2.5   (t_res≈2.74 at N=256)
log|ω|: +0.11 +0.75 +1.11 +1.39 +1.56 +1.80
```

It grows fast, then *decelerates* through the middle (the per-step increments
shrink), and then — right at the edge of where the grid can still resolve it —
**re-accelerates**. That final upturn is the signature of the approaching
singularity. It is the thing we actually want to measure.

And it is exactly the part of the curve that the grid keeps taking away from us. As
`N` grows, `tail_guard` (the instrument that stops the solve when enstrophy piles up
at grid scale) lets the trusted window extend a little further into the
acceleration: `t_res` goes 2.46 → 2.74 → 2.98 at N = 128 → 256 → 512. So any window
that *reaches* the acceleration captures more of it at higher resolution, and the
measured rate climbs and climbs:

| initial condition | `g_frac` @128 | @256 | @512 | verdict |
|---|---|---|---|---|
| **smooth_sharp** (blows up) | +0.663 | +0.793 | **+0.968** | never converges |
| smooth_mild (saturates) | +0.421 | +0.421 | +0.421 | flat (stays fully resolved) |
| euler_control (flat) | 0.000 | 0.000 | 0.000 | flat |

A fixed window *stable* enough not to drift has to sit earlier, in the boring
region — and there the saturating shape has the *higher* rate (our spike measured
`g(mild)=1.24 > g(sharp)=0.61`). So you get to pick exactly one: a rate that's
stable, or a rate that knows which shape blows up. Not both.

This is not a bug in the window. It is the resolution wall from three posts ago,
wearing a different hat. Our spike had already found that the blow-up *exponent*
never resolution-converges on a uniform grid — Luo & Hou needed adaptive mesh
refinement to ~10¹² effective resolution to see the real thing. The growth *rate*
is the same quantity in disguise. **`ν_crit` died on the viscosity wall; the
inviscid rate dies on the resolution wall. Two different currencies, the same wall.**

## The twist: the ranking doesn't care

Here is where it would have been easy to write the obituary and stop. But a search
doesn't need the fitness *number* to be right. It needs the fitness to *rank shapes
correctly*, and to keep ranking them the same way as you refine the grid. The
absolute values can drift all they like, as long as the order they put shapes in
holds still.

So we asked a different question. Take the 20-shape roster, score every shape at
`N=128` and again at `N=256`, and measure whether the two *rankings* agree
(Spearman's rank correlation). The magnitude is on the wall — but is the order?

For `g_frac`, the answer is **+0.90**. The rankings barely move. That's a genuinely
different — and more hopeful — result than "the magnitude diverges."

## …but the pickpocket came back

Before believing that, we ran a second candidate: `accel_ratio`, the ratio of the
late-window rate to the early-window rate. It's a natural "is it accelerating?"
score, and its rank-stability was even *better*: **+0.95**.

We have been burned by exactly this before, so we ran the audit we should have run
on `ν_crit` the first time: **interrogate the winner against the dumbest possible
cheat.** And there it was.

`accel_ratio`'s top-ranked shape, `rand_08`, is not a blow-up shape at all — it runs
the *entire* simulation without ever under-resolving (a shape approaching a
singularity gets cut off early; this one never does). It wins because it's a
*ratio*, and its early-window rate is tiny (0.13), so dividing by it inflates the
score. A small-denominator cheat. The *same* cheat as `ν_crit`'s `1/ω₀`, in a fresh
costume. The correlation that gives it away: ρ(`accel_ratio`, early_rate) = **−0.66**
— the score is organized by having a small denominator, not by blowing up. Its
gorgeous +0.95 rank-stability was real and completely worthless, because it was
stably ranking shapes *by the cheat*.

`g_frac` is a *rate*, not a ratio — nothing to divide by — and it passes the audit
clean:

| audit (N=256) | `accel_ratio` (cheat) | **`g_frac`** (survives) |
|---|---|---|
| winner actually a blow-up shape? | no (never under-resolves) | **yes** |
| top-5 that approach a singularity | 3/5 | **5/5** |
| ρ(·, log\|ω₀\|) — the ω₀ cheat | +0.10 | **+0.17** (≈0) |
| ρ(·, early_rate) — small-denominator cheat | **−0.66** | +0.27 (weak) |
| ρ(·, centroid) — rewards structure? | −0.06 (flat) | **+0.31** (yes) |

The lesson from the Gate-4 post was "a frozen predicate is a floor, not a ceiling."
The lesson here is its twin: **a rank-stable winner is a floor, not a ceiling
either.** Stability of a metric tells you nothing about *what* it's stable at. You
still have to look.

## The last trap we checked: does it just want buoyancy?

One more way `g_frac` could be secretly trivial. The genome splits its energy
between vorticity `ω` and a buoyancy field `θ`; the `split` is how much goes to `θ`.
More buoyancy plausibly means faster growth — so maybe `g_frac`'s "optimum" is just
"pour everything into `θ`," a degenerate corner, with `ω₀→0` sneaking the
small-denominator cheat back in through the side door.

Two checks say no. First, hold a shape's *structure* fixed and sweep only the split:
the growth rate peaks in the **interior** (around split 0.3–0.5) and *falls* toward
all-buoyancy. No rail. The physics genuinely wants a balance of vorticity and
buoyancy — which is correct; that coupling is what drives the Boussinesq
singularity. Second, on random shapes `g_frac` *does* correlate with split (+0.73),
but split and `ω₀` are mechanically tangled (more `θ` means less `ω`). Untangle them
with a partial correlation and the verdict is clean:

- partial ρ(`g_frac`, log\|ω₀\| **given** split) = **+0.04** — control for split and
  the `ω₀` dependence *vanishes*. The cheat that killed `ν_crit` is genuinely absent.
- partial ρ(`g_frac`, split **given** log\|ω₀\|) = **+0.41** — the buoyancy
  preference is real physics, not the `ω₀` artifact.

The one honest caveat that leaves: buoyancy (`split`) dominates the ranking more
than vorticity *geometry* does. That's not a cheat, but it means the eventual
shape→growth map would mostly be a map of buoyancy strength, with geometry a quieter
second voice — something a full gate has to account for, not wave away.

## Where this leaves us

Add it up honestly. We went looking for a resolution-stable, cheat-free fitness for
a 2D Boussinesq blow-up search. We found that **no growth-rate *magnitude* can be
that** on a uniform grid — the signal we want lives in the part of the flow the grid
erases. But we also found that a **rank-based** `g_frac` is direction-correct,
free of every cheat we know how to test for, rewards structure, survives a free
buoyancy split — and holds its ranking steady from `N=128` to `256`.

That is a real result, and a narrow one. It is contingent on a single test we have
not yet run: does the *ranking* still hold from `N=256` to `512`, or is even the
order eventually on the wall? That test is expensive (it means resolving the whole
roster at the finest grid), so we've stopped here, banked everything, and paused for
review before spending it. If the ranking holds, there's a search worth running —
scored by a fitness we had to demote from a number to an order. If it doesn't, then
the wall wins completely, and that's the finding.

Either way, the through-line of this whole phase is now unmistakable. Every honest
attempt to *measure* the singularity on a uniform grid — critical viscosity, growth
magnitude — runs into the same fact: **the singularity forms below the grid scale,
and the grid keeps its secret.** You can rank the shapes that are *heading* there.
You cannot, on this hardware, watch one arrive. And a search can only ever argue
*for* blow-up; it can't prove it. We keep saying that, because it keeps being true,
and because the day we forget it is the day one of these pretty, stable, cheating
numbers talks us into believing we've solved a problem we haven't.
