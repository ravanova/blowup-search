# Win Condition

We need to recognize the difference between "the simulation looks like it's
blowing up" and "we have actually solved the problem." These are very
different claims, and conflating them is the single easiest way for a
computational search project like this to fool itself. So the win condition
is defined in three tiers. **Only Tier 3 counts as solving the problem.**
Tiers 1–2 are progress markers.

## Background: the criterion we're chasing

The **Beale–Kato–Majda (1984) theorem** gives the exact condition for
blow-up: a smooth solution on `[0, T)` fails to extend smoothly past `T` if
and only if

```
∫₀ᵀ ||ω(t)||_∞ dt = ∞
```

where `ω = curl(u)` is the vorticity. In practice you can't numerically
integrate to a divergent value, so the standard proxy (used by Hou, Luo, and
others) is to track `M(t) = ||ω(t)||_∞` and plot its reciprocal `1/M(t)`. If
the solution is heading toward a genuine finite-time singularity, `1/M(t)`
should approach zero at some finite time `T*`, often close to linearly. This
reciprocal-vorticity extrapolation is what our Tier 1 check implements.

## Tier 1 — Candidate

A single simulation run produces a credible blow-up signal:

- Fit `1/M(t)` as a line over the tail of the run.
- The fit must have a **negative slope** (vorticity is genuinely growing, not
  flat or decaying).
- The extrapolated zero-crossing `T*` must lie **ahead of** the simulated
  time range (a forward prediction, not something already passed).
- The fit quality (`R²`) must clear a high threshold (default 0.98) — a sloppy
  fit is not a signal, it's noise.

This is what the GA's fitness function optimizes for during evolution. A
genome that clears this bar becomes a **candidate**, nothing more.

## Tier 2 — Numerically confirmed

A raw candidate is cheap to produce accidentally — under-resolved
simulations routinely look like they're blowing up when they're actually just
hitting the limits of the grid (a numerical artifact, not real physics). To
rule that out:

- **Resolution convergence study**: rerun the candidate at increasing spatial
  and temporal resolution (at least 3 resolution levels). The estimated `T*`
  must stabilize — differences between successive resolutions should shrink,
  and the finest two estimates must agree within a tight relative tolerance
  (default 2%). If `T*` keeps drifting as you refine the grid, it's an
  artifact, not a singularity.
- **Self-similar profile check** (qualitative, not yet automated): near
  `(x*, T*)` the rescaled solution should approach a consistent self-similar
  profile with stable scaling exponents across resolutions, consistent with
  the blow-up ansatz used in Luo–Hou (2014) and related work.

Passing Tier 2 is strong numerical evidence of a genuine singularity. It is
still **not a proof** — floating-point simulation cannot certify behavior at
an actual singular point.

## Tier 3 — Rigorously proven (the actual win condition)

Convert the Tier-2 numerical candidate into a **computer-assisted proof**:
rigorous interval arithmetic / validated numerics establishing that a true
(exact, not floating-point-approximate) solution exists in a neighborhood of
the numerical profile and genuinely reaches a singularity in finite time.
This is the same style of argument Buckmaster, Gómez-Serrano, and others have
carried out for related equations (Boussinesq, De Gregorio, etc.).

**Only Tier 3 is an actual answer to the Clay Millennium Problem.** This tier
cannot be automated by the GA or by floating-point simulation — it requires a
separate, dedicated rigorous-numerics pipeline built around whatever specific
candidate clears Tier 2. That pipeline is out of scope until we have a Tier-2
candidate to feed it.

## Explicit non-goal: proving the positive direction

If the evolutionary search runs for a long time and never finds a Tier-1
candidate, **that is not evidence of global regularity.** Failure to find a
counterexample after finite search says nothing about a universally
quantified claim over an infinite-dimensional space of initial data. We will
not treat "the GA didn't find blow-up" as a result — only a genuine Tier 3
proof, in either direction, counts.
