# Two currencies, one wall

### A pre-committed negative result on scalar fitness for blow-up search on uniform grids, and the anti-self-deception gate that produced it

*A self-contained methods note. It can be read without any other file in this
repository. Every quantitative claim is traceable to a small committed JSON file
in [`data/`](../data/); the pointers are collected in
[§7 Data & reproducibility](#7-data--reproducibility). For the chronological
narrative and the surrounding project, see [SUMMARY.md](../1_gclm_1d/SUMMARY.md).*

---

## Abstract

We attempted to use an evolutionary (quality-diversity) search over initial
conditions to steer a 2D Boussinesq system, in the Hou–Luo symmetry-wall
geometry, toward finite-time singular behaviour. Such a search needs a **scalar
fitness** that rewards "more singular" initial data. We tested two independent,
physically-motivated fitness currencies — a **viscosity-resistance** measure
(`ν_crit`, the critical viscosity a shape's growth survives) and an **inviscid
growth-rate** measure (`g_frac`) — each against a **pre-committed, cheat-audited
viability gate**. Both fail, and both fail through the *same* root degeneracy: on
a free genome the "most singular" optimum is not blow-up structure but the
**vanishing-vorticity corner** (`ω₀ → 0`), reached by dumping the conserved energy
budget into the buoyancy field. `g_frac` fails with a bonus pathology — controlling
for buoyancy split it is largely a *formation-time stopwatch*, not a shape
discriminator.

The unifying diagnosis is about the **grid**, not the currency. On a uniform mesh
the genuine singular structure forms **below grid scale**, so any scalar read off
the trusted, pre-artifact window is dominated by the degrees of freedom that *are*
resolved — overall amplitude, buoyancy split, formation time — none of which is
the target. Audit away one proxy and the signal re-expresses through the next. Two
currencies were enough to establish the pattern; a third uniform-grid scalar is
not indicated. The honest exit is to stop reading a uniform grid's own breakdown
and measure fitness on *resolved* structure — i.e. adaptive mesh refinement or
dynamic self-similar rescaling.

The transferable contributions are two: **(i)** the gate protocol below — a
concrete, reusable recipe for not fooling yourself with a fitness function — and
**(ii)** the negative result itself, which tells anyone planning an
evolve-the-initial-condition search precisely which wall they will hit and how to
recognise it.

**Scope, stated up front and not walked back.** This is a *2D toy model*, not 3D
Navier–Stokes. Finite-time blow-up in 2D Boussinesq boundary geometry was already
*proven* (Chen–Hou, 2022); we neither reprove nor extend it. Nothing here is a
proof, a blow-up, or a claim about the Millennium problem. It is a negative result
about **search machinery**.

---

## 1. Setting

The equations are 2D Boussinesq,

```
ω_t + (u·∇)ω = θ_x + ν Δω
θ_t + (u·∇)θ =          κ Δθ
u = ∇^⊥ ψ,   Δψ = ω
```

on the Hou–Luo geometry, where a no-flow symmetry wall is imposed by parity rather
than by an explicit boundary condition. Our pseudo-spectral solver
(`solver/boussinesq.py`) is validated to machine precision against an analytic
ladder, and the Hou–Luo wall is a *genuine invariant of the discrete dynamics*
(held to `9×10⁻¹⁵` unenforced). None of that is in question here; the solver is
trustworthy on the window where it is trusted.

The search premise is: parametrise a family of smooth, parity-correct initial data
(a truncated Fourier genome under one *joint* energy normalisation, so overall
amplitude is not a free knob), and evolve it with MAP-Elites to maximise a scalar
fitness that should correlate with "closer to singular." The whole difficulty is
choosing that scalar so that its maximiser is *singular structure* and not some
cheaper thing the genome can also do.

A structural fact that governs everything below: the genome's energy normalisation
is **joint** over vorticity `ω` and temperature/buoyancy `θ`. A single scalar, the
**split** `s ∈ (0,1)`, sets the fraction of the fixed energy budget placed in `θ`
versus `ω`. Pushing `s → 1` starves the vorticity: `|ω₀| → 0`. This "split" knob is
the villain of the piece.

---

## 2. The anti-self-deception gate (the transferable protocol)

The reason this project exists is to *not* mistake a numerical or definitional
artifact for a discovery. The mechanism is a viability gate applied to a candidate
fitness **before** any expensive search is pointed at it. The protocol has three
layers, and each was learned by being burned.

**Layer 1 — a pre-committed predicate.** Write the acceptance test down as a fixed
set of properties (discriminating; direction-correct with a censored control;
well-posed / window-robust; resolution-stable; wide dynamic range; a non-trivial
optimum), have it reviewed, and **freeze it in git before running**. A
dirty-tree guard refuses to log a run against an uncommitted predicate. This stops
the classic move of adjusting the bar after seeing the result.

**Layer 2 — cheat audits as first-class gate conditions, not post-hoc
diagnostics.** A pre-committed predicate is *necessary but not sufficient*. Our
first currency taught us this the hard way: `ν_crit` printed a clean **6/6 PASS**
on its frozen gate — and it was a **false pass**. The predicate had simply not
thought to test the actual cheat. So in the reformulated gate, the substantive
anti-cheat correlations were **promoted into the predicate itself**: if the winning
shape is secretly the `ω₀ → 0` corner, or if the fitness is really a proxy for some
trivial scalar (amplitude, split, formation time, a small-denominator ratio), the
gate must **fail by construction**. A gate that *cannot* fail is theatre; we even
flagged one sub-condition in the frozen document as *expected to fail*, and ran it
anyway.

**Layer 3 — interrogate the actual free-search winner, not a controlled slice.**
This is the sharpest and most repeatedly-relearned lesson. A **controlled**
sub-experiment passing is *not* the winner being honest. You can fix a shape's
geometry, sweep only its split, and find a well-behaved interior optimum every
time — concluding "the split is not a trivial rail." And that conclusion is *locally
true and globally false*: on a free roster where geometry *also* varies, a
high-split shape with the right geometry beats every interior-optimum structured
shape. Only correlating the **actual, free, winning genome** against the dumbest
possible cheats reveals it. Three distinct controlled sub-tests passed while the
free-search winner was railed; each time, only winner-interrogation caught it.

> **The one-line version, for reuse:** a frozen predicate is a floor, a
> rank-stable winner is a floor, and a passing controlled sub-test is a floor.
> None is a ceiling. Always correlate the *free-search winner* against
> amplitude, every conserved-budget split, formation time, and small-denominator
> ratios — before you believe the fitness.

---

## 3. Currency 1 — viscosity-resistance (`ν_crit`)

`ν_crit` is the critical viscosity at which a shape's net amplification crosses a
fixed threshold — the 2D analogue of the fitness that *succeeded* in our earlier
1D pipeline. It passed its pre-committed 6/6 gate. Then Layer-2/Layer-3 audits
were applied to the winner and it collapsed:

- The measure is **≈75% explained by the initial vorticity amplitude**:
  `ρ(ν_crit, log|ω₀|) = −0.90`.
- Two shapes at *equal absolute vorticity* differ in `ν_crit` by **197×** — the
  gap is set by the split-driven denominator, not by structure.

`ν_crit` rewards `ω₀ → 0` through a **small-denominator** mechanism: a shape that
barely has any vorticity trivially "survives" viscosity, because there is almost
nothing for viscosity to damp. Fixing the split and a normalised-resistance
transform both fail to rescue it. Per the pre-committed directive, **a wall is a
finding, not a push-harder signal** — so `ν_crit` was retired, not patched.

---

## 4. Currency 2 — inviscid growth-rate (`g_frac`), and the reformulated gate

`g_frac` is a fixed-window inviscid growth **rate**: how fast a shape amplifies
vorticity over a trusted early window, before any grid artifact. It was designed to
sidestep the small-denominator trap — a rate has no viscosity denominator to game —
and an early probe was encouraging. Crucially, its **magnitude** is *not*
resolution-convergent (it climbs with N — sharp shape `0.66 → 0.79 → 0.97` at
N=128/256/512 — because the shape re-accelerates at the moving edge of the trusted
window; this is the uniform-grid wall reasserting), but its **rank order** is
resolution-stable: Spearman `+0.90` at 128↔256, and a dedicated de-risk confirmed
`+0.905` at 256↔512. So the honest reformulation was "resolution-stable must mean
**rank**-stable here," and a rank-based `g_frac` earned a full 40-shape gate.

**The reformulated gate.** Six properties, frozen and reviewed pre-run, with the
anti-cheat audits of §2 promoted to first-class conditions. Property 4 became
*rank-*stability across 128→256→512; property 6 became *non-trivial optimum
controlling for split*, carrying eight explicit sub-conditions (winner is a real
grower, is structured, is not at the split rail, top-5 are growers, no `ω₀` cheat
even partialled on split, structure not penalised, structured gradient beyond
split, and more-than-a-formation-time-proxy).

**Verdict: FAIL 4/6.** ([data](../data/phase1_gate4_reform.json))

| property | result |
|---|---|
| 1. discriminating | PASS |
| 2. direction + censored control | PASS |
| 3. well-posed (window-robust ρ = +0.989) | PASS |
| 4. **rank-resolution-stable** | **FAIL** |
| 5. wide band | PASS |
| 6. **non-trivial optimum, split-controlled** | **FAIL** |

The rank part of property 4 *passed* (`+0.889`, `+0.926`). It failed for a sharper
reason (§4.2). Property 6 failed hard (§4.1).

### 4.1 The ghost came back: free-split rail to `ω₀ → 0`

The de-risk that made us optimistic had **fixed the split at 0.5**. The real search
does not. On a free-split roster, the entire top five is the split → 1 corner:

| rank | shape | g_frac | centroid | **split** | t_res |
|------|-------|--------|----------|-----------|-------|
| 1 | rand_18 | +1.635 | 1.56 | **0.99** | 2.01 |
| 2 | rand_06 | +1.631 | 2.84 | **0.99** | 2.26 |
| 3 | rand_01 | +1.561 | 1.59 | **0.95** | 2.53 |
| 4 | rand_17 | +1.521 | 2.19 | **0.93** | 2.26 |
| 5 | rand_07 | +1.291 | 1.62 | **0.99** | 2.15 |

`ρ(g_frac, log|ω₀|) = −0.66`. This is the *same degeneracy* that killed `ν_crit`,
arriving by a different road: `ν_crit` rewarded `ω₀ → 0` through a small
denominator; `g_frac` rewards it because dumping energy into buoyancy genuinely
makes the (vanishing) vorticity grow fastest *in rate*. It is honest physics **and**
a rail — both at once.

And the controlled split-sweep *passed*: fix geometry, vary split, and the optimum
is interior every time (peaks at split 0.3–0.7). By that test alone "split is not a
rail" passes. It is Layer-3 exactly: the controlled slice is clean, the free winner
is railed, and only winner-interrogation sees it.

### 4.2 It's also largely a stopwatch

Two further property-6 sub-conditions failed, and they matter for anyone tempted to
reuse a growth-rate currency:

- **Beyond split, it barely ranks geometry.** Partial `ρ(g_frac, centroid | split)
  = +0.11` (bar was `+0.15`). Control for the split and the fitness stops
  distinguishing one vorticity *shape* from another — it is close to a split-meter.
  (This is the condition we had flagged as *likely to fail* in the frozen doc.)
- **It's largely a formation-time proxy.** Partial `ρ(g_frac, centroid | t_res) =
  −0.39`. `t_res` is merely *when* a shape first generates small scales. Control for
  it and the structure signal doesn't just vanish, it **reverses**. So even binning
  the archive on split would not rescue `g_frac`: it is a stopwatch as much as a
  split-meter.

### 4.3 And rank-stability is not classification-stability

Property 4's rank was stable, but the *binary* label "is this shape blowing up" was
not. **7 of 37 shapes** trip the small-scale guard at N=128, look like growers,
then **saturate** once the grid resolves them — e.g. `advlo_s20`'s resolution time
climbs `2.91 → 3.56 → 4.00` (the window ceiling) as N = 128 → 256 → 512. That is a
textbook under-resolution false-positive — the exact artifact the project exists to
avoid. A rank can be perfectly stable while ~19% of what it ranks is grid noise.

---

## 5. The unifying diagnosis: below-grid-scale structure and proxy re-expression

Two independent currencies, two independent pre-committed gates, one root failure:
on a free genome the "most singular" optimum is the `ω₀ → 0` corner, not blow-up
structure. The correct reading is a statement about the **grid**, not the currency.

On a uniform mesh, the genuine Hou–Luo singular structure forms **below grid
scale** — the true singularity requires the kind of adaptive refinement Luo–Hou
drove to ~10¹², utterly out of uniform-grid reach. Everything a scalar fitness can
read off the *trusted, pre-artifact* window is therefore dominated by the degrees
of freedom that *are* resolved on that window: overall amplitude, the buoyancy
split, the formation time. None of those is the target. Audit one proxy away and
the fitness re-expresses the same preference through the next resolvable proxy —
amplitude → split → formation time. This is why a *third* uniform-grid scalar
currency is not indicated: it would be pushing harder against the wall the first
two already mapped, and the project's firm rule is that a wall is a finding, not a
motivation.

---

## 6. What follows — and what does not

**The honest exit is a numerics upgrade, not another fitness.** To measure a
fitness on *resolved* structure instead of on the grid's own breakdown, the search
must stop using a uniform grid: **adaptive mesh refinement (AMR) or dynamic
self-similar rescaling**, tracking the forming structure and reading the fitness in
the rescaled frame. This is the field-standard tooling (Luo–Hou, Chen–Hou,
Elgindi, Buckmaster–Gómez-Serrano). It is also the *only* route to Tier-2
resolution-confirmation of the true Hou–Luo singularity within this program.

**A terminology guard, because it is easy to trip.** This upgrade is a **solver
upgrade to Route A** — better *numerics*. It is **not** what the project roadmap
calls **"Route D."** Roadmap Route D is the *Tier-3 validated-numerics /
computer-assisted-proof leg* (with a domain expert), which only exists **after** a
Tier-2 candidate has been produced. AMR-numerics ≠ proof-leg. Do not conflate them.

**What is transferable right now**, independent of whether the AMR upgrade is
built:

1. **The gate protocol of §2** — pre-committed predicate + cheat audits as
   first-class conditions + free-search-winner interrogation. It is model-agnostic
   and is the most portable thing here.
2. **The negative result itself** — anyone building an evolve-the-initial-condition
   search on a conserved-energy genome over a uniform grid will meet this wall. Now
   they know its shape (the conserved-budget split corner), and how to detect it
   (winner-interrogation against amplitude / split / formation time).

**What this is not.** Not a proof. Not a blow-up. Not a statement about 3D
Navier–Stokes. Even a *positive* result in this setting would be toy-model science
across the gap that 2D Boussinesq (already proven to blow up at a boundary) does
not close to the Millennium problem. The realistic value is the machinery result
and the methodology, honestly bounded.

---

## 7. Data & reproducibility

Every quantitative claim above traces to a committed file in [`data/`](../data/); no
raw log or solver re-run is required to check any number.

| claim | file |
|---|---|
| `ν_crit` false 6/6, then `ρ(ν_crit, log|ω₀|) = −0.90`, 197× gap | [`data/phase1_gate4.json`](../data/phase1_gate4.json) |
| `g_frac` magnitude on the wall; rank-stability +0.90 / +0.905; `accel_ratio` near-cheat caught | [`data/phase1_gsustained.json`](../data/phase1_gsustained.json) |
| reformulated gate FAIL 4/6 scorecard; free-split top-6; the eight property-6 sub-conditions; the 7 classification flips | [`data/phase1_gate4_reform.json`](../data/phase1_gate4_reform.json) |
| all headline numbers | [`data/summary_metrics.json`](../data/summary_metrics.json) |

The frozen predicate contract and full per-experiment records live in the repo
root: [`../PHASE1_GATE4_REFORMULATED_PREDICATE.md`](../../PHASE1_GATE4_REFORMULATED_PREDICATE.md)
(the gate, committed pre-run),
[`../PHASE1_GATE4_REFORM_RESULTS.md`](../../PHASE1_GATE4_REFORM_RESULTS.md),
[`../PHASE1_GATE4_RESULTS.md`](../../PHASE1_GATE4_RESULTS.md),
[`../PHASE1_GSUSTAINED_RESULTS.md`](../../PHASE1_GSUSTAINED_RESULTS.md). The
runner/analyzer split that produced the evidence (`phase1_gate4_reform.py` writes
the log; the frozen `analyze_phase1_gate4_reform.py` applies the predicate) is
described there. For the surrounding project and the chronological narrative, start
at [SUMMARY.md](../1_gclm_1d/SUMMARY.md); the per-experiment blog posts are
[BLOG_PHASE1_GATE4.md](BLOG_PHASE1_GATE4.md),
[BLOG_PHASE1_GSUSTAINED.md](BLOG_PHASE1_GSUSTAINED.md), and
[BLOG_PHASE1_GATE4_REFORM.md](BLOG_PHASE1_GATE4_REFORM.md).
