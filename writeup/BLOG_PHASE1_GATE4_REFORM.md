# The gate we built to fail

*What happened when we cashed in the rank check and ran the honest gate. Sequel to
[BLOG_PHASE1_GSUSTAINED.md](BLOG_PHASE1_GSUSTAINED.md); all numbers below are built
from committed evidence in
[`data/phase1_gate4_reform.json`](data/phase1_gate4_reform.json), full record in
[`../PHASE1_GATE4_REFORM_RESULTS.md`](../PHASE1_GATE4_REFORM_RESULTS.md).*

The last post ended on a cautious win. We had a fitness function for ranking
candidate blow-up shapes — `g_frac`, an inviscid growth **rate** — and although its
*magnitude* was hopelessly on the resolution wall, its **rank order** was stable:
Spearman +0.90 from N=128 to 256. We ran one more expensive check, 256→512, and the
rank held again: **+0.905**. A rank-based fitness looked viable.

So we did the honest thing, and it is worth being explicit about what "honest"
meant here, because it is the whole point of the post.

## Pre-committing a gate you expect might fail

We had been burned before. The *previous* currency, `ν_crit`, printed a clean
**6/6 PASS** on its pre-committed viability gate — and it was a **false pass**. The
gate had tested the wrong cheat. The real degeneracy (the fitness secretly tracking
`1/ω₀²`) was caught only afterward, by a substantive correlation the predicate
hadn't thought to include.

The lesson we banked: *a pre-committed predicate is necessary but not sufficient.*
So this time we promoted the substantive anti-cheat audits — correlate the winner
against the dumbest cheats — from post-hoc diagnostics into **first-class gate
conditions**. If the winning shape is secretly the ω₀→0 corner, or if the fitness
is really just a proxy for some trivial scalar, the gate must **fail by
construction**, not pass and let us discover it later during an expensive search.

We wrote the six-property predicate down, had it reviewed, and froze it *before*
running. One condition in particular — "the fitness must carry ω-geometry signal
*beyond* the buoyancy split" — we flagged in the frozen doc as **likely to fail**,
because a probe had hinted the relevant partial correlation was only +0.09 against
our +0.15 bar. We ran it anyway. A gate that cannot fail is theatre.

## It failed. 4 out of 6.

Here is the scorecard on the 40-shape roster (three resolutions, plus an 18-shape
controlled split-sweep):

| property | result |
|---|---|
| 1. discriminating | PASS |
| 2. direction + control censored | PASS |
| 3. well-posed (window-robust +0.989) | PASS |
| 4. **rank-resolution-stable** | **FAIL** |
| 5. wide band | PASS |
| 6. **non-trivial optimum, split-controlled** | **FAIL** |

The rank *was* stable (property 4's Spearman part passed: +0.889, +0.926). It failed
for a different, sharper reason, and property 6 failed hard. Both failures say the
same thing.

## The ghost came back

The de-risk that made us optimistic had fixed the buoyancy **split** at 0.5 — equal
vorticity and temperature energy. That pins the scale of `ω₀`. It was a controlled
experiment, and in a controlled experiment `g_frac` behaved.

But the actual search does not fix the split. It is free to vary it — and freeing
it is exactly the knob the old `ν_crit` cheat used. More temperature energy → more
buoyancy forcing → faster vorticity growth, *and* a smaller `ω₀`. On the free-split
roster, look at who wins ([data](data/phase1_gate4_reform.json)):

| rank | shape | g_frac | centroid | **split** |
|------|-------|--------|----------|-----------|
| 1 | rand_18 | +1.635 | 1.56 | **0.99** |
| 2 | rand_06 | +1.631 | 2.84 | **0.99** |
| 3 | rand_01 | +1.561 | 1.59 | **0.95** |
| 4 | rand_17 | +1.521 | 2.19 | **0.93** |
| 5 | rand_07 | +1.291 | 1.62 | **0.99** |

The entire top five is the split → 1 corner. `ω₀ → 0`. It is the *same degeneracy*
that killed `ν_crit`, arriving by a different road: `ν_crit` rewarded it through a
small denominator, `g_frac` rewards it because dumping energy into buoyancy really
does make the (vanishing) vorticity grow fastest *in rate*. The correlation
ρ(g_frac, log|ω₀|) = **−0.66**.

Here is the subtle part, and the reason the gate earned its keep. We *also* ran the
controlled split-sweep — fix a shape's geometry, vary only its split — and it
showed a well-behaved **interior** optimum every time (peaks at split 0.3–0.7, no
rail). By that test alone, "the split is not a trivial rail" **passes**. The de-risk
had run essentially that test and concluded the split preference was honest physics.

It was honest physics *and* a rail. Both. At fixed geometry the best split is
interior; but on a free roster where geometry *also* varies, a high-split shape with
the right geometry beats every interior-optimum structured shape. The controlled
experiment could not see it. Only interrogating the **actual free-search winner**
could. (Banked lesson, reasserted for the third time: a controlled sub-test passing
is not the winner being honest.)

## And it's mostly a stopwatch

Two more of property 6's conditions failed, and they matter for anyone thinking of
reusing this currency:

- **Beyond split, it barely ranks geometry.** Partial ρ(g_frac, centroid | split) =
  **+0.11**. Control for the split and the fitness stops distinguishing one
  vorticity *shape* from another. It is close to a split-meter. (This was the
  condition we'd flagged as likely-to-fail. It failed.)

- **It's largely a formation-time proxy.** Partial ρ(g_frac, centroid | t_res) =
  **−0.39**. `t_res` is just *when* the shape first generates small scales. Control
  for that, and the structure signal doesn't merely vanish — it reverses. `g_frac`
  is, to a large degree, a re-encoding of "how soon does this shape hit the grid
  limit." So binning the archive on split wouldn't even rescue it; it's a stopwatch
  as much as it's a split-meter.

## The other failure: some "growers" were never growing

Property 4 failed a second axis the rank-check never tested. The rank of `g_frac` is
resolution-stable — but the **binary classification** "is this shape blowing up" is
not. Seven of 37 shapes trip the small-scale guard at N=128, look like growers, and
then **saturate** once the grid resolves them:

```
advlo_s20:  t_res  2.91 → 3.56 → 4.00   (N = 128, 256, 512)
```

That is a textbook under-resolution false-positive — the exact artifact the whole
project exists to not be fooled by. A rank can be stable while ~19% of what it's
ranking is grid noise.

## Two currencies, one wall — and what it's actually telling us

Step back. We have now taken two independent fitness currencies — a
viscosity-resistance (`ν_crit`) and an inviscid growth-rate (`g_frac`) — through a
pre-committed, cheat-audited viability gate. Both **fail**, and both fail through the
**same root degeneracy**: on a free genome the "most singular" optimum is the ω₀→0
corner, not blow-up structure. `g_frac` throws in a bonus problem (it's half a
stopwatch).

The deeper reading is a statement about the *grid*, not the currency. On a uniform
mesh, the genuine singular structure forms **below grid scale**. Everything a scalar
fitness can read off the trusted, pre-artifact window is therefore dominated by the
degrees of freedom that *are* resolved — overall amplitude, buoyancy split,
formation time — none of which is the thing we're hunting. You can audit away one
proxy and the signal just re-expresses itself through the next. Two currencies was
enough to see the pattern.

So we are not going to reach for a third uniform-grid currency. That would be
pushing harder against a wall, and this project's one firm rule is that a wall is a
finding, not a motivation. The honest path to a fitness that tracks real structure —
and, not coincidentally, the only path to *confirming* any candidate singularity —
is to stop using a uniform grid: **adaptive mesh refinement / self-similar
rescaling**, so the fitness is measured on resolved structure instead of on the
grid's own breakdown.

That's the next decision. As always, the honest framing stands: this is a result
about search *machinery* in a 2D toy model, not about Navier–Stokes, and not a
blow-up. But knowing precisely *why* two reasonable fitness functions both fail —
and having a pre-committed gate rigorous enough to prove it rather than guess it — is
the kind of negative result the field actually needs. If you're going to evolve
initial conditions toward a singularity, here is a wall you'll hit, and here is how
to know you've hit it.
