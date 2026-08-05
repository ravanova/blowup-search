# The gate that passed — and shouldn't have

*A technical blog post on a search that caught itself almost cheating. Sequel to
[BLOG_PHASE1.md](BLOG_PHASE1.md); all numbers below are built from committed
evidence in [`data/phase1_gate4.json`](../data/phase1_gate4.json), with the full
record in [`../../PHASE1_GATE4_RESULTS.md`](../../PHASE1_GATE4_RESULTS.md).*

The previous post ended on a promise. We had a fitness function for a 2D
Boussinesq blow-up search — `ν_crit`, the critical viscosity that just barely
suppresses a shape's vorticity growth — chosen by experiment on labeled
ground-truth data. But we flagged one open danger, quoting the 1D version of this
project:

> the analogous `ν_crit` fitness passed every check except one: its optimum
> collapsed to a degenerate "pile all your energy into the lowest mode" cheat, and
> that killed the whole axis. It may happen again here. If it does, that's a
> finding, and we'll say so.

It happened. This post is us saying so — and the way it happened is a better
story than a clean failure, because the fitness **passed our pre-committed test**
and was wrong anyway.

## The setup: a gate you write before you look

The discipline this project runs on is: decide what "success" means, in code,
*before* you run the expensive experiment — so you can't rationalize a bad result
into a good one afterward. For the fitness we froze a six-property gate (the
inheritance from the 1D project) and committed it to git before a single
production run:

1. **Nonzero** — shapes have a nonzero critical viscosity (the landscape isn't dead-flat).
2. **Finite** — blow-up doesn't survive arbitrarily large viscosity.
3. **Monotone** — more viscosity never *helps* blow-up.
4. **Resolution-stable** — the value doesn't move when you refine the grid.
5. **Wide band** — different shapes get meaningfully different values.
6. **Non-trivial optimum** — the *best* shape is a real structure, not a degenerate cheat.

Property 6 is the one that killed the 1D axis. So the roster of 40 test shapes
was built specifically to *attack* it: alongside random and structured shapes, we
included six deliberate "trivial cheat" shapes — vorticity piled into the lowest
Fourier mode — to see whether they would win.

We ran it: 40 shapes at grid size N=256, then again at N=512 to check resolution
stability. And the frozen predicate returned:

| Property | Verdict |
|---|---|
| 1. nonzero | PASS (31/36 growers) |
| 2. finite | PASS (0 censored high) |
| 3. monotone | PASS (0 violations / 35 bisections) |
| 4. resolution-stable | PASS (max \|Δν_crit\| = **0.0025**, ½·tol, across 32 shape-pairs) |
| 5. wide band | PASS (spread = **287×** the tolerance) |
| 6. non-trivial optimum | PASS (winner a *structured* shape, centroid 2.66; ρ(ν_crit, centroid) = −0.15) |

**Six for six.** Property 6 in particular looked clean: the winning shape was not
one of our planted low-mode cheats, and `ν_crit` showed essentially no correlation
(−0.15) with spectral centroid — the "concentrate at low frequency" axis that had
been the cheat in 1D. By the letter of the pre-committed gate, we should have
proceeded to the full genetic-algorithm campaign.

## The question that broke it

The gate passed. But a gate is only as good as the failure modes its author
imagined, and this one was written to catch the *1D* cheat (low-mode
concentration). So before trusting it, we asked a blunter question: **is the
winner winning for a real reason, or for a stupid one we didn't think to test?**

`ν_crit` is defined through an *amplification ratio*: how much viscosity it takes
to keep `max|ω|(t) / max|ω(0)|` — the vorticity's growth relative to its starting
value — below a threshold. That denominator, `max|ω(0)|`, is the shape's initial
vorticity amplitude. And in the 2D genome, a shape can freely trade energy between
its vorticity field and its buoyancy (temperature) field. So a shape can make its
*initial vorticity tiny* while parking energy in buoyancy — and then any growth at
all looks like enormous amplification, purely because the denominator is small.

One correlation settles it. Across the 36 uncensored shapes:

> **ρ(ν_crit, log max|ω₀|) = −0.90.**

Three-quarters of the variance in our fitness (R² = 0.755, with a slope of −2.11 —
a textbook dissipation-scaling law, ν_crit ∝ |ω₀|⁻²) is explained by *nothing but
the initial vorticity amplitude*. The fitness was measuring 1/ω₀, not blow-up.

The smoking gun is clearest in shapes that reach the **same absolute vorticity**
but get wildly different scores:

| shape | initial \|ω₀\| | absolute peak \|ω\| reached | ν_crit |
|---|---|---|---|
| `rand_15` | 0.122 | 8.4 | **1.437** |
| `rand_05` | 2.066 | 7.7 | **0.007** |

Both grow to essentially the same absolute vorticity (~8). One scores **197×**
higher than the other — entirely because it *started* smaller. Worse, the ranking
can invert against genuine growth:

| shape | absolute peak \|ω\| reached | ν_crit |
|---|---|---|
| `rand_24` | **14.5** | 0.043 |
| `rand_18` | 13.5 | **1.326** |

`rand_24` grows *more* in absolute terms, yet ranks **31× lower**. A fitness that
ranks the bigger grower below the smaller one is not measuring blow-up propensity.
This is the same disease as the 1D collapse — a trivial optimum — wearing a
costume the pre-committed predicate never checked for. (The undamped buoyancy
field makes it worse: with no thermal diffusion, buoyancy keeps re-forcing
vorticity no matter how much viscosity you apply, so the "hide energy in buoyancy"
shapes rail to the top of the viscosity axis.)

**The lesson worth keeping:** pre-committing your success criterion is necessary
but *not sufficient*. A frozen gate can still have a blind spot — and the only
defense is to interrogate the winner against the dumbest possible explanation,
even (especially) after the gate says PASS.

## Trying to save it — twice — and failing honestly

A degeneracy in the *denominator* sounds fixable. We tried, cheaply, before
concluding anything.

**Fix 1 — remove the knob.** Force every shape to split its energy 50/50 between
vorticity and buoyancy, so the initial amplitude can't be driven to zero. The
amplitude correlation dropped from −0.90 to −0.44 — but did **not** vanish (shape
still affects the peak), the winner was **still a trivial low-mode shape**, and a
new correlation surfaced: ρ(ν_crit, centroid) = **−0.21**. Higher-frequency (more
structured) shapes were now *less* viscosity-resistant — because higher
frequencies dissipate faster. That is the νk² dissipation-scaling wall, the exact
thing that fundamentally sank the 1D axis, reasserting itself.

**Fix 2 — divide out the dissipation.** The 1D notes suggested a "normalized
resistance," `ν_crit · centroid²`, to measure resistance *beyond* the dissipation
scaling. It does make a structured shape win — but tautologically: the centroid²
multiplier spans a 9× range and simply dominates the product. The tell is that a
shape with *higher* raw `ν_crit` ranks *below* one with lower `ν_crit` purely
because its centroid is smaller. That doesn't surface real resistance; it just
relocates the trivial optimum to the opposite (high-frequency) corner.

Conclusion: the `ν_crit` property-6 failure is **fundamental, not a bug**. Any
fitness built on *viscosity resistance* inherits the dissipation-scaling wall,
because it is a measure about viscosity. On this model, that axis is dead — the
1D result, reconfirmed in 2D.

## One idea that isn't dead yet

There's a way out of the wall, and it falls straight out of the diagnosis. The
problem was two-fold: an *amplification ratio* (gameable by shrinking the
denominator) and a *viscosity* measure (organized by dissipation scaling). Change
both:

- Measure **inviscidly** (viscosity off) — no νk² term, so no dissipation-scaling triviality.
- Measure a growth **rate** (a log-derivative over a mid-run window), not a ratio
  against the initial value — so it doesn't divide by ω₀ and can't be gamed by
  shrinking it.

The candidate: **inviscid sustained growth rate** — the log-growth rate of
`max|ω|` over the *late* part of the trustworthy window (late, to reward shapes
that keep accelerating toward a singularity over shapes that spurt early and
saturate). A cheap probe — one solve per shape, no bisection — clears the exact
bars `ν_crit` failed:

| test | `ν_crit` (failed) | `g_sustained` (probe) |
|---|---|---|
| direction on labeled ICs (sharp > mild > control) | mis-ranked | **+0.79 > +0.42 > 0.0** ✓ |
| independence from ω₀ | ρ = **−0.90** | ρ = **+0.24** (cheat gone) |
| structure signal (ρ with centroid) | **−0.21** (wall) | **+0.38** (flipped: structure rewarded) |

The correlation that was the wall (−0.21) flips positive (+0.38). The amplitude
cheat (−0.90) is gone (+0.24). And it correctly orders the three labeled
ground-truth shapes whose answers we already know.

We are **not** declaring victory. This is a probe — necessary, not sufficient —
with two honest open flags: its resolution-stability is only *modest* so far (the
sharp reference drifts ~16% between N=128 and N=256, because the measurement
window moves with the grid; a fixed window should tighten it), and it hasn't been
tested with the energy split left free (where it will legitimately reward
buoyancy, which could hide its *own* trivial optimum). Both need the same
full six-property scrutiny `ν_crit` just failed. That's the next experiment.

## What we have, and what we still don't

We have a **finding**: viscosity-resistance is not a viable blow-up fitness on
this model — killed by the same dissipation wall as in 1D, via a cheat that
slipped past a pre-committed gate until we interrogated the winner directly. We
have a **methodology data point**: a frozen predicate is a floor, not a ceiling.
And we have a **lead**: an inviscid growth-rate currency that, in a cheap probe,
escapes the wall.

We do **not** have a 2D blow-up candidate, a validated fitness, or any reason to
revise the odds. Those remain capped by the two walls no cleverness removes: a
search can only ever argue *for* blow-up, and provable blow-up lives only in toy
models, not in 3D Navier–Stokes. What this episode shows is the machinery of not
lying to yourself — running the cheap diagnostic that turns a satisfying PASS into
an honest FAIL, and writing it down either way.

*Reproducibility: the gate is [`../../phase1_gate4.py`](../../phase1_gate4.py) with the
frozen predicate in [`../../analyze_phase1_gate4.py`](../../analyze_phase1_gate4.py);
the two probes are [`../../phase1_gate4_probe.py`](../../phase1_gate4_probe.py) and
[`../../phase1_currency_probe.py`](../../phase1_currency_probe.py). Every number here is
in the committed [`data/phase1_gate4.json`](../data/phase1_gate4.json) (rebuilt by
[`curate_evidence.py`](../curate_evidence.py)), with narrative in
[`../../PHASE1_GATE4_RESULTS.md`](../../PHASE1_GATE4_RESULTS.md).*
