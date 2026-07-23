# Two experiments before the search: de-risking a 2D blow-up hunt

*A follow-up to ["Can you evolve a Navier–Stokes singularity?"](BLOG.md) — this
time in 2D, and this time about the cheap experiments you run **before** you let
the search loose, so you don't spend weeks optimizing the wrong thing or, worse,
optimizing a numerical artifact.*

In the first post we evolved initial conditions toward finite-time blow-up in a
1D toy model (the generalized Constantin–Lax–Majda equation), with one obsession:
never mistake "my simulation looks like it's blowing up" for "I found a
singularity." That project ended with a validated pipeline, resolution-confirmed
(Tier-2) blow-ups, and an honest negative result — the 1D models we could search
only ever produced the *generic*, already-known singularity, never a novel one.

So we moved up: **2D Boussinesq**, in the Hou–Luo symmetry-wall geometry. This is
still a toy model — it is not 3D Navier–Stokes — but it is a much better toy. It
has a **proven** finite-time singularity (Chen–Hou, 2022) and a gold-standard
numerical benchmark (Luo–Hou, 2014). If a search-plus-honesty methodology is ever
going to matter, it should earn its keep here first.

This post is not about a blow-up we found. **We have not run the search yet.**
It is about the two cheap experiments we ran first — and why running them first
was the whole point.

## The trap moves, but it doesn't leave

In 1D the fatal trap was rewarding the GA for "biggest blow-up signal," which
just evolves initial conditions that best exploit your grid's resolution limit. A
coarse grid manufactures fake infinities, and on a single run they are
*indistinguishable* from real ones.

In 2D the trap gets worse, because the real Hou–Luo singularity is a corner
collapse so violent that Luo and Hou needed adaptive mesh refinement down to an
effective ~10¹² grid to track it. On any uniform grid we can afford, the
vorticity sharpens below grid scale long before the singular time. So the first
question isn't "can we find blow-up?" It's the more uncomfortable one:

> **On a uniform grid, is there *anything* about this problem we can measure
> honestly — a signal that doesn't move when we refine the grid?**

If the answer is no, the entire search is dead on arrival, and it's much cheaper
to learn that in an afternoon than after a three-week GA campaign.

### Experiment 1: the resolution wall, quantified

We built a "trust instrument" into the solver first. The right signal that a
spectral simulation has run out of resolution is not conservation drift — that
can stay at 10⁻⁶ while the small scales quietly turn to garbage — but **enstrophy
piling up at the grid scale**. When too much of the energy sits in the highest
retained Fourier modes, the solver stops and refuses to report anything past that
point. Everything downstream only ever reads the *trusted* window.

Then we took two smooth growing initial conditions and ran them at N = 128, 256,
512, 1024, watching two numbers (figure
[`fig6`](figures/fig6_phase1_spike.png)):

- A **fixed-window growth rate** `g` — how fast the vorticity grows over a time
  window that sits inside every resolution's trusted range.
- The **fitted blow-up exponent** α and singular time `T*` — the actual
  "is this a singularity and when" numbers.

The result was a clean, honest split:

- **`g` converges.** As we refine the grid, `g` settles to a fixed value
  (0.609 for the sharper IC, agreeing to better than 0.01% between the two finest
  grids). A resolution-stable signal exists. **The search is viable.**
- **α and `T*` rail.** The fitted exponent lurches 2.45 → 0.70 → 0.90 → 1.20 and
  `T*` never stabilizes. The grid never reaches the singular time, so the
  singularity's *own parameters* are not resolution-converged.

That second half is a real limit, stated plainly: **uniform-grid Tier-2
confirmation of the true Hou–Luo singularity is out of reach.** (Rough, merely
Hölder-continuous initial data was worse — under-resolved from `t ≈ 0`, no usable
window at all — so we dropped that axis.) This isn't a failure; it's a
recalibration. The reachable near-term prize is a resolution-stable **map from
initial-condition shape to growth**, with Tier-1 *candidates* — and Tier-2/Tier-3
confirmation explicitly handed off to adaptive-mesh or validated-numerics tools
(and, realistically, a domain expert). Knowing that *before* building the search
is worth an enormous amount.

### Experiment 2: choosing the fitness on labeled ground truth

Experiment 1 said a resolution-stable growth signal exists. But there was a
subtlety hiding in the data, and it is the kind of subtlety that quietly wrecks
these projects:

- The **sharp** IC blows up (vorticity amplifies 100×) but has the *lower* early
  growth rate, `g = 0.61`.
- The **mild** IC saturates — it never blows up, amplifying only ~5× — but has
  the *higher* early growth rate, `g = 1.24`.

So the resolution-stable quantity, `g`, orders these two examples **backwards**.
It rewards transient early speed, not the propensity to actually blow up. If we
had naively made `g` the fitness, the GA would have spent weeks climbing toward
flashy early-growers that fizzle.

Here's the move we're most happy about. Those two ICs are **labeled ground
truth**: we know one blows up and one doesn't. That's exactly what you need to
*test a fitness function before you trust it*. So we wrote a small, pre-committed
screen: measure each candidate fitness axis on {sharp (blows up), mild
(saturates), a flat non-grower}, and demand two things — the axis must order them
by true blow-up propensity (`sharp > mild > control`), and it must not move when
we refine the grid.

Three axes went in (figure [`fig7`](figures/fig7_phase1_axis_screen.png)):

1. **Raw growth rate `g`** — fails, backwards, exactly as predicted. (This is the
   built-in sanity check: the screen *should* reproduce the known-wrong answer,
   and it does.)
2. **A "persistence" proxy** (is the growth accelerating?) — fails, but
   interestingly: it ranks the hard-saturating shape *below* the flat
   non-grower, because a strong decelerator looks worse than nothing at all.
3. **A ν_crit-analog** — *how much viscosity does it take to kill the growth?* —
   passes cleanly. The shape that really blows up needs far more viscosity to
   suppress (ν_crit ≈ 0.65) than the one that saturates (≈ 0.05) or the
   non-grower (0). And the value is **identical to four decimal places** at
   N = 256 and 512 — the amplification threshold is set by the physics, not the
   grid.

"How much dissipation does it take to stop this?" is a genuine measure of
blow-up *propensity*, not transient speed — which is why it separates the two
labeled cases the way the raw rate cannot.

#### The bug the screen caught before we trusted it

We almost shipped a broken version of ν_crit. Our first definition was "the
viscosity at which the *windowed growth rate* crosses zero." A quick smoke run on
the labeled pair exposed it: the mild IC, run with heavy viscosity, **decayed to
half its initial vorticity** — and *still* registered a positive windowed slope,
because the slope caught a transient bump inside the window. A net-decaying flow
scored as "growing." We switched the criterion to net amplification (the
project's actual blow-up currency), which can't be fooled that way.

The point isn't the specific bug. It's that the labeled ground truth made the
wrong answer *visible* — the screen caught its own design flaw before a single
minute of real search compute. That is the entire value proposition of running
cheap, pre-committed experiments first.

## What we have, and what we very deliberately don't

To be clear about the ledger, because the temptation to oversell is exactly the
thing this project exists to resist:

- We have a **validated 2D solver** whose Hou–Luo no-flow wall is a genuine
  invariant of the discrete dynamics, not something we paint on each step.
- We have a **quantified resolution wall**: the search is viable on a uniform
  grid, but confirming the true singularity there is not.
- We have a **fitness function chosen by experiment**, not by taste, and
  stress-tested on cases with known answers.

We do **not** have a 2D blow-up candidate. The screen we ran is *necessary, not
sufficient*: it only checked two properties on three hand-picked ICs. The real
gate is still ahead — a six-property viability test of ν_crit across dozens of
evolved shapes, and in particular whether its optimum is *non-trivial*. In the 1D
project, the analogous ν_crit fitness passed every check except that one: its
optimum collapsed to a degenerate "pile all your energy into the lowest mode"
cheat, and that killed the whole axis. It may happen again here. If it does,
that's a finding, and we'll say so.

The overall odds of this program actually resolving the Clay problem remain very
low — capped by two walls that no amount of cleverness removes: a search can only
ever argue *for* blow-up, and provable blow-up lives only in simple models, not
in 3D Navier–Stokes. What we're building is a methodology that refuses to lie to
itself on the way there. Two cheap experiments, run before the expensive one,
are what that discipline looks like in practice.

*Numbers and figures here are built from the committed evidence in
[`data/`](data/) via [`build_figures.py`](build_figures.py); see
[README.md](README.md) for the full evidence map, and
[`../PHASE1_AXIS_SCREEN_RESULTS.md`](../PHASE1_AXIS_SCREEN_RESULTS.md) /
[`../PHASE1_SPIKE_RESULTS.md`](../PHASE1_SPIKE_RESULTS.md) for the pre-committed
gates.*
