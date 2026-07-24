# Phase 1 Gate 4 — six-property viability gate results

*Route A Phase 1, the NON-NEGOTIABLE viability gate on the fitness before any GA
campaign (2026-07-24). Pre-committed predicate + roster in `phase1_gate4.py` /
`analyze_phase1_gate4.py` (commit `5957155`, before the run). This records what
came back, the substantive re-analysis, and two follow-up probes. STOPPED for
review; forward path (a full Gate 4 on a new currency) not yet started.*

## Verdict

**The `ν_crit`-analog fitness FAILS property 6 (non-trivial optimum) — the same
wall that killed 1D gCLM.** The frozen predicate prints 6/6 PASS, but that is a
**false pass**: the predicate tested the *1D* failure mode (low-mode
concentration → spectral centroid) and had a blind spot for the actual 2D
degeneracy. Substantively, `ν_crit` is ~75% explained by the initial vorticity
amplitude `max|ω₀|` — a trivial small-denominator cheat, not blow-up structure.

A follow-up **currency probe is promising**: an *inviscid sustained growth-rate*
fitness (`g_sustained`) escapes both the ω₀ cheat and the dissipation-scaling
wall in a cheap probe. That is a probe, **necessary-not-sufficient** — a full
Gate 4 on it is the open forward decision, not a result.

## Gate 4 as run (ν_crit, 40 shapes × N=256 cold + N=512 warm)

40-shape roster designed to *test* property 6: 3 controls (Euler censor-low
anchor + sharp/mild benchmarks), 6 trivial-cheat shapes (ω pure `(1,1)`, minimum
centroid — the 2D analog of the k=1 concentration that killed gCLM), 3 structured
high-centroid, 28 random spanning centroid×anisotropy×split. Full roster at N=256
(cold) then N=512 (warm-started from each N=256 `ν_crit`, probes skipped) — the
warm-start + 8 workers brought the naive ~21 h down to what ran in practice.
Stopped at 36/40 N=512 (the last 4 are moot — see below). 36 uncensored growers,
4 censored low (`ctrl_euler`, `triv_lowsplit`, `rand_14`, `rand_16`).

**Frozen predicate: 6/6 PASS** — nonzero (31/36 > 2·tol), finite (0 censored
high), monotone (0 probe violations / 35 bisections), resolution-stable (max
|Δν_crit| = 0.0025 ≈ ½·tol across all 36 shapes measured at both N — a genuinely
clean pass), wide band (287·tol), and property 6 "PASS" (winner `rand_15`,
centroid 2.66, ρ(ν_crit, centroid) = −0.15).

## Why that 6/6 is a false pass (the substantive property-6 failure)

The predicate anticipated gCLM's failure mode — an optimum collapsing to low-mode
concentration — and tested spectral centroid, which looked innocent (ρ = −0.15).
It never tested the degeneracy that actually governs this landscape: the smooth
genome's **free ω/θ split lets the "optimum" drive `max|ω₀|` → 0**, trivially
inflating `amp = max|ω|/max|ω₀|`, while the undamped θ reservoir (κ=0) re-forces ω
regardless of viscosity, railing `ν_crit` high for a reason unrelated to blow-up
structure. Four convergent tests (N=256 data, all 36 growers):

1. **ρ(ν_crit, log max|ω₀|) = −0.90**, ρ(ν_crit, log abs-peak-|ω|) = only +0.37.
   `ν_crit` tracks 1/ω₀, not the absolute vorticity reached.
2. **log(ν_crit) ~ log|ω₀|: R² = 0.755, slope −2.11** — three-quarters of the
   variance is just ω₀, with a textbook dissipation-scaling exponent (ν_crit ∝
   |ω₀|⁻²).
3. **Same absolute growth, wildly different ν_crit:** `rand_15` (ω₀=0.12) reaches
   |ω|=8.4 → ν_crit=1.437; `rand_05` (ω₀=2.07) reaches |ω|=7.7 → ν_crit=0.007 — a
   **197× gap** for essentially equal absolute growth. Worse, `rand_24` reaches a
   *higher* peak (14.5) than `rand_18` (13.5) yet ranks **31× lower** — the metric
   is inverted relative to genuine propensity.
4. Dividing ν_crit by ω₀² collapses the 287·tol band to ≈55×.

**Methodological lesson:** a pre-committed predicate can still have a blind spot;
pre-committing it is necessary but not sufficient — the substantive diagnostic
(here, correlating the fitness against ω₀) is what caught the false pass. The last
4 N=512 runs were skipped because property 6 is decided entirely by N=256, and
property 4 (the only thing they add) already passes cleanly on 36 shapes.

## Probe 1 — does fixing the split rescue it? (`phase1_gate4_probe.py`, N=128, split=0.5)

Fixing ω/θ split = 0.5 pins ω₀'s scale so it cannot be driven to zero. Result:
**no rescue.**
- ρ(ν_crit, log|ω₀|) drops −0.90 → **−0.44** but persists (shape-dependent peak).
- Winner is **still trivial** (`triv_sharpth`, ω pure `(1,1)`, centroid 1.41).
- ρ(ν_crit, centroid) = **−0.21**: higher-k structure is *less* resistant (it
  dissipates faster) — the νk² dissipation-scaling wall, reasserting.

## Probe 1b — normalized resistance (the 1D rescue), from the same data

STAGE_2_5 flagged `ν_crit · k_centroid²` ("resistance beyond the dissipation
scaling"). Here `ν_crit · centroid²` makes the winner structured (`struct_33`,
centroid 4.24, ρ = +0.85) — but **tautologically**: the centroid² multiplier
(2→18, 9×) dominates the product. The tell: `struct_high` has *higher* raw ν_crit
(0.089) than `struct_33` (0.072) yet ranks below it purely on centroid². This just
relocates the trivial optimum to the high-frequency corner — exactly STAGE_2_5's
finding ("the cap does not remove the trivial optimum, it just moves it").
**Conclusion: the ν_crit property-6 failure is fundamental, not a fixable bug** —
the gCLM νk²-dissipation wall, reconfirmed for viscosity-resistance fitness on 2D
Boussinesq smooth data.

## Probe 2 — one more currency: inviscid sustained growth rate (`phase1_currency_probe.py`)

`ν_crit` was doomed *because it is a measure about viscosity*. Two changes escape
both cheats at once: measure **inviscid** (ν=0 → no νk² term → no dissipation
triviality) and use a growth **rate** over a mid-run window (a log-derivative →
does not divide by ω₀). Currency:
`g_sustained = [log max|ω|(t_res) − log max|ω|(0.5·t_res)] / (0.5·t_res)` inside
the tail_guard-trusted window. Cheap: one ν=0 solve per shape, no bisection.

It **clears the exact bars ν_crit failed** (a probe, not a gate):
- **Direction** (labeled ICs, N=256): sharp **+0.79** > mild **+0.42** > control
  **0.0** ✓ (the raw growth rate never ordered these correctly).
- **ω₀-independence:** ρ(g_sustained, log|ω₀|) = **+0.24** (ν_crit was −0.90) — the
  amp-denominator cheat is gone.
- **Non-trivial optimum** (split-fixed roster): winner `rand_01` (centroid 1.59,
  **not** a trivial `(1,1)` shape); ρ(g_sustained, centroid) = **+0.38** — the
  correlation *flipped sign* from ν_crit's −0.21, so structure is now weakly
  *rewarded* rather than penalized.

**Honest caveats (why this is promising, not proven):**
- **Resolution-stability is only modest:** sharp drifts 0.663 → 0.793 (≈16%) from
  N=128→256 because the *fractional* window moves with t_res. A **fixed-absolute
  window** (like the spike's ultra-stable g) should tighten this — an open
  refinement, not yet a pass.
- **Free-split behavior untested:** the probe fixed split=0.5 to isolate
  structure. With free split, g_sustained will likely correlate with split (more
  θ → more buoyancy forcing → faster growth). That is *real physics*, not the ω₀
  artifact — but it could still create a trivial max-split optimum and needs the
  same property-6 scrutiny.
- Probe-scale (20 shapes, N=128); the full six-property gate, reformulated for a
  growth-rate currency, has not run.

## Consequence / open decision

Per the pre-committed directive, the `ν_crit` result is a **finding, not a
push-harder signal**: viscosity-resistance on this genome has a trivial
(amplitude + dissipation-scaling) optimum. But the currency probe shows the
failure is specific to *viscosity-resistance*, not to the whole search premise —
an inviscid growth-rate currency escapes the wall. The open forward decision
(for review) is whether to promote `g_sustained` to a full Gate 4 with the two
refinements (fixed-absolute window + free-split property-6 check).

## Honest framing (unchanged)

2D Boussinesq is a toy model, not 3D Navier–Stokes; a viable fitness axis is
machinery for a search, not a blow-up. Even a full Gate-4 pass would yield only a
resolution-stable shape→growth QD map with Tier-1 candidates — uniform-grid Tier-2
of the true Hou–Luo singularity remains out of reach (Route D). Overall Clay odds
stay ~0.05%.
