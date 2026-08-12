# Route-SCEL v1 — samples → certified cell enclosures, under a named hypothesis

**Leg 385, slot C, construction, difficulty HEAVY. Gate: YES.**
Module: `solver/dssp_decay_samples.py`. Tests: `test_dssp_decay_samples.py`, 17/17.
Runner: `experiments/p2_route_scel_v1.py` (8.1 s). Data:
`writeup/data/p2_route_scel_v1.json`. Figure: **fig103**.
Novelty pass `00d8e4e`, pre-registration `353cbf1` — both committed before construction.
Reads `solver/dssp_decay_enclosure.py` (leg 382, `104f5b3`) and **edits it nowhere**.
Companion: `BLOG_P2_ROUTESCEL_V1.md`.

**Ceiling: TIER 2.** `CLAY_OBLIGATIONS.md` §6 items 1 and 2 stay **OPEN**; item 1's
admissible-cutoff half is **entirely untouched** by this leg. No `L1 → L4` link moved.
Clay ~0.05%.

---

## 1. The gap this closes, in leg 382's own words

`solver/dssp_decay_enclosure.py:354`:

> "Supplying those is the caller's obligation and this routine cannot check it — if the caller
> has only pointwise samples, it must first convert them using a certified modulus of
> continuity, or a monotonicity hypothesis, and must state which."

`certified_decay_from_cell_enclosures(r_lo, r_hi, f_lo, f_hi, ...)` requires
`f_lo[i] ≤ f(r) ≤ f_hi[i]` for **every** `r` in cell `i`. Any profile-producing unit holds
point samples. The converter did not exist anywhere in the tracked tree (novelty pass §1:
six `modulus of continuity` hits, none an implementation; zero sample→enclosure routines in
`solver/`).

**The negative fact that forces the design.** From finitely many point evaluations alone,
with no regularity hypothesis, no non-trivial enclosure is derivable. So the module's first
behaviour is a refusal, not a computation.

## 2. The two paths

Let `t = log r`, `g = log f`, cells `[r_i, r_{i+1}]` with both endpoints sampled as certified
intervals `[f_lo_i, f_hi_i]`.

**PATH A — MONOTONE.** Caller declares `f` non-increasing (or non-decreasing) on the window.
Extremes on a cell are attained at its endpoints, so `f(r) ∈ [f_lo_{i+1}, f_hi_i]`. Exact:
**no slack is added beyond the caller's own sample error bars.**

**PATH B — MODULUS.** Caller declares `ω(h) = L·h^α`, `α ∈ {1/2, 1}`, in one of two kinds:

| kind | statement | cell enclosure |
|---|---|---|
| `absolute` | `\|f(r) − f(s)\| ≤ ω(\|r − s\|)` | `[min − ω(h/2), max + ω(h/2)]` |
| `loglog` | `\|g(t) − g(s)\| ≤ ω(\|t − s\|)` | `[min·e^{−ω(Δt/2)}, max·e^{+ω(Δt/2)}]` |

`h/2` because every point of a cell is within half its width of one endpoint.

`L` may be a scalar or a per-sample array (cell `i` uses `max(L_i, L_{i+1})`).

**No `iexp` in the substrate.** `solver/interval.py` has `ilog` and no exponential, and leg
382 deliberately declined to add a transcendental whose remainder it would have to prove. The
`loglog` kind is therefore closed with two elementary bounds using only `+ − × ÷`:

```
e^{-x} >= 1 - x         (x >= 0)
e^{ x} <= 1/(1 - x)     (0 <= x < 1),   since 1/(1-x) = Σ xⁿ >= Σ xⁿ/n! = eˣ
```

applied outward. At `ω ≈ 2.4e-3` the overestimate is `O(ω²) ≈ 5e-6` relative — measured as
`max_relative_inflation = 2.4235738569e-3` against `ω = 2.4177143477e-3`, a 0.24% excess over
the exact exponential. Inputs with `ω(Δt/2) ≥ 1` are **refused**, not approximated.

**Both may be declared**, in which case the enclosures are intersected and the row records
`MONOTONE+MODULUS`.

## 3. Refusal is a first-class output, and the conditionality is in the row

`samples_to_cells` returns `INCAPACITY` — never a guess — for: no hypothesis; a hypothesis
the samples themselves contradict; non-increasing radii; any `r ≤ 1`; a non-positive sample
bound; `f_hi < f_lo`; fewer than two samples; a bare number in place of a `Modulus`; `α`
outside `{1/2, 1}`; `ω(Δt/2) ≥ 1` in the `loglog` kind; and mutually inconsistent
declarations. `certified_decay_from_samples` **never calls leg 382's routine** on a refusal
(`enclosure_called: false`, `p_lo: null`): *there is no code path producing a decay exponent
without a named hypothesis attached to it.*

Every accepted row carries `hypothesis`, `hypothesis_detail`, `sample_exactness`
(`enclosed` vs `declared-exact`) and a `conditional_on` sentence, merged into leg 382's own
output dict. §6 below is why that is not decoration.

**Necessary conditions, never sufficient.** A declared hypothesis implies checkable facts
about the samples (monotone increments; `|Δ| ≤ ω(h)`). Violations that are *certain after
outward rounding* refuse and name the cell. Passing proves nothing — §6.

## 4. PATH A reproduces leg 382 bit-identically

Window `[10, 1000]`, `N = 1000` cells, bracket `[0,12]` — leg 382's configuration, unmoved.
Samples are certified enclosures produced by leg 382's own interval generator at point radii
(a float64 evaluation of the planted formula is *not* its exact value, and laundering that
away is the leak this module exists to plug).

| row | profile | truth | width from SAMPLES | leg 382's banked width | difference |
|---|---|---|---|---|---|
| K1 | `3.0 r^-1` | 1.0 | `7.438494264988549e-15` | `7.438494264988549e-15` | **0.0** |
| K2 | `1.0 r^-2` | 2.0 | `1.5987211554602254e-14` | `1.5987211554602254e-14` | **0.0** |
| K3 | `0.25 r^-5/2` | 2.5 | `1.9984014443252818e-14` | `1.9984014443252818e-14` | **0.0** |
| K4 | `7.0 r^-3` | 3.0 | `1.554312234475219e-14` | `1.554312234475219e-14` | **0.0** |

Every difference is **exactly zero**, not "within tolerance", and the truth is inside every
interval (K1: `p ∈ [0.9999999999999963, 1.0000000000000038]`). The baselines are
**re-computed in this run** by calling `certified_decay_interval` — never transcribed.

**Mechanism**, and it is the same one leg 382 measured when its own width prediction failed
(its §12a): for a monotone profile the cell enclosure's endpoints coincide with the pointwise
values at the cell edges. Those edges are exactly the sample points. **The conversion loses
nothing.** Prediction **P1 CONFIRMED**, in the strongest available form.

## 5. PATH B is sound, and cannot be made tight — predicted before it was measured

`f = 3 r^-1`, true log-log Lipschitz constant `1.0`, declared `ω(h) = 1.05·h` (`loglog`) — a
true, slightly conservative statement.

* Verdict `INTERVAL`, `p ∈ [0.9989466218941611, 1.0010512713496271]`, truth inside.
* **Width `2.1046494554660677e-3`** — pre-registered prediction `≈2.0e-3`, band `[7e-4, 6e-3]`.
  **P2 CONFIRMED.**
* Ratio to PATH A: **`2.829e11`**.

| `N` | PATH A width | PATH B width |
|---|---|---|
| 100 | `7.66053886991358e-15` | `2.1474946052902677e-2` |
| 250 | `7.66053886991358e-15` | `8.474917198654897e-3` |
| 1000 | `7.438494264988549e-15` | `2.1046494554660677e-3` |
| 2000 | `7.438494264988549e-15` | `1.051161005387713e-3` |

Log-log slopes: **PATH A `−0.0118`** (rounding floor; leg 382 measured `−0.0295` on its own
ladder), **PATH B `−1.0068`**. **P3 CONFIRMED.** Extrapolating, PATH B reaches PATH A's
`7.44e-15` at **`N ≈ 2.83e14`** samples.

> **The modulus path cannot reproduce leg 382's exact-power widths at any feasible sampling
> density.** It is *sound*, never *tight*. This was written into the pre-registration (P2, P3)
> before the module existed; it is not a post-hoc rationalisation of a disappointing number.

### 5a. A globally stated `absolute` modulus is useless on a multi-decade window

Same profile, declared `ω(h) = 0.03·h` where `0.03 = p·C·R₀^{−p−1}` is the **true** global
Lipschitz constant on `[10, 1000]`.

* First cell whose lower enclosure is non-positive: **`r = 207.97`** (pre-registered `≈208`,
  band `[100, 420]`).
* Cells affected: **341** of 1000 (pre-registered `≥250`).
* Downstream verdict: **`INCAPACITY`** — *"profile enclosure touches or crosses zero; log is
  undefined"* — not a number. **P4 CONFIRMED** on all three components.

Mechanism: on a geometric grid `h ∝ r`, so `ω(h/2)` **grows** with `r` while `f` decays; the
additive inflation overtakes the profile. The `loglog` kind, or per-sample local constants,
are what such a window admits. Panel C of fig103.

### 5b. Declaring both

`MONOTONE + loglog ω` gives width `7.438494264988549e-15`, difference from PATH A **exactly
0.0**. The intersection is dominated by the tighter statement. **P12 CONFIRMED.**

## 6. The controls — all five fired, none widened

| id | planted violation | expected | outcome | magnitude |
|---|---|---|---|---|
| X1 | **no hypothesis** | refusal | `INCAPACITY`, `enclosure_called: false` | no exponent exists |
| X2 | monotonicity broken **visibly** (one sample +5%) | refusal | `INCAPACITY`, cell **499** | violation `+1.3615e-3` |
| X3 | monotonicity broken **secretly** (node-aligned wiggle `A = 0.05`) | containment failure | **accepted**, then caught | **`+5.1420e-2`** relative, **1000/1000 cells** |
| X4 | modulus understated **detectably** (`L = 0.1`, truth `2.0`) | refusal | `INCAPACITY` | ratio **`19.99999999994`** |
| X5 | modulus understated **undetectably** | containment failure | **accepted**, then caught | **`+4.7721e-2`** in `log f` |

**P5–P9 all CONFIRMED.** No threshold, amplitude, window or modulus was touched to make a
control pass (the leg-361 rule).

### 6a. X3 is the leg's argument, stated precisely

The planted truth is `f(r) = 3r^{-1}(1 + A·sin(2π(t − t₀)/Δt))` with `Δt` **exactly** the grid
spacing in `t`, so the sine vanishes at every node: **the samples are bit-identical to K1's.**
The adapter accepts — it *provably cannot* do otherwise — and the pipeline returns

* verdict `INTERVAL`, width **`7.438494264988549e-15`**, containing `p = 1`,

which is **numerically indistinguishable from K1's true certificate** and is **false about the
true profile**, which leaves the claimed enclosure in **all 1000 cells** by up to 5.14%.

Nothing is broken. The certificate is valid *under the declared hypothesis*; the hypothesis is
false. The only thing separating the true certificate from the false one is the row's
`hypothesis` / `conditional_on` field. **That is why conditionality is recorded, and it is the
one design decision in this module that is not a matter of taste.**

X5 is the same trap on the modulus side: node-to-node increments satisfy `L = 1.05` exactly
(`|Δg| = Δt ≤ 1.05Δt`) while the within-cell excursion `0.05` dwarfs the inflation
`2.4177e-3`.

## 7. Where the pre-registration was WRONG — recorded, not amended

### P11: REFUTED

Part I §5 predicted that X3's true profile, re-sampled on the **half-cell-shifted** grid,
would be visibly non-monotone and refused. **It is not**: the adapter returns `CELLS`. The
quarter-shifted grid also returns `CELLS`.

**Mechanism.** The wiggle has period exactly one cell in `t`, so a *uniform* shift by `s`
cells multiplies **every** sample by the same constant `(1 + A·sin(2πs))`. A constant multiple
of a monotone sequence is monotone, and its log-increments are unchanged, so **both** necessary
conditions pass at every uniform shift; the half-shift is doubly invisible because
`sin(π) = 0`. The pre-registration's reasoning was wrong about *which* grids can see the
wiggle. The prediction stays on the record as wrong.

### The correct statement, located post-hoc and labelled as such

**NOT PRE-REGISTERED. Decides nothing about the gate**, which is answered by X1–X5.
Re-sampling the same true profile at other densities:

| `N` | `Δt′/Δt₀` | verdict | worst monotone violation |
|---|---|---|---|
| 500 | 2.000 | `CELLS` | `−2.776e-5` |
| 997 | 1.003 | `CELLS` | `−1.104e-5` |
| 1001 | 0.999 | `CELLS` | `−1.478e-5` |
| 1010 | 0.990 | `CELLS` | `−5.469e-6` |
| **1100** | 0.909 | **`INCAPACITY`** | **`+7.032e-3`** |
| **1500** | 0.667 | **`INCAPACITY`** | **`+2.494e-2`** |
| 2000 | 0.500 | `CELLS` | `−6.916e-6` |

Detection is a **commensurability** phenomenon: ratios near an integer (500, 1000, 2000) or
near 1 (997, 1001, 1010 — the phase drifts too slowly) see nothing. **A hypothesis-violating
profile can hide from any fixed grid**, which strengthens the leg's conclusion rather than
weakening it: the hypothesis is doing the work, and the sampling never was.

## 8. Anti-tautology

1. **The containment audit can report CLEAN, and does** — worst signed relative excess
   `−1.7067e-16` (S1), `−2.4177e-3` (S2), `−2.3079e-3` (S3), all strictly negative. **P10 CONFIRMED.**
   An audit that always fires would prove nothing.
2. No row returns the full search bracket.
3. The refusals are not universal: S1–S4 are accepted by the same code path that refuses
   X1, X2, X4.
4. Every accepted row carries a hypothesis.
5. Every leg-382 comparison number is re-computed in this run, not transcribed.

**Ledger: 11 of 12 pre-registered predictions CONFIRMED, P11 REFUTED and recorded as
refuted.**

## 9. The gate, answered in its own wording

> "Does the adapter convert a planted sampled profile with a stated true hypothesis into cell
> enclosures whose certification reproduces 382's exact-power result within its measured
> widths, AND does a planted hypothesis-VIOLATING input (samples secretly non-monotone /
> modulus understated) fire the refusal or a containment failure — controls able to fail,
> neither widened?"

**YES**, with the conjuncts stated separately because they are not equally strong:

* **First conjunct — YES, via PATH A only.** Monotonicity reproduces leg 382's four banked
  exact-power widths with difference **exactly 0.0**, truth inside every interval. **PATH B
  does not and cannot** (`2.10e-3` at `N = 1000`, slope `−1.0068`, `N ≈ 2.8e14` needed) — a
  measured limitation, predicted in advance, and this leg does **not** claim a YES for both
  paths.
* **Second conjunct — YES.** X1, X2, X4 fire refusals; X3 and X5 are accepted (as they must
  be) and fire containment failures of `+5.142e-2` relative and `+4.772e-2` in `log f`.
  Nothing was widened; P11 failed and is recorded as failed.

**Which hypothesis each result is conditional on:** the reproduction rows and S4 on
**declared monotonicity** (never verified); S2, S3, X5 on a **caller-certified modulus**.
No row here is unconditional, and every row says so in its own `conditional_on` field.

## 10. Carried forward, unchanged by the YES

* **`CLAY_OBLIGATIONS.md` §6 items 1 and 2 stay OPEN.** Item 1's admissible-cutoff half is
  entirely untouched; this leg supplies the *input contract* of the certified-exponent third.
* **No profile exists.** Every input is a planted analytic known. The first real consumer
  remains whatever future unit produces a profile, and **this leg claims nothing about one**.
* **Disclosed hole, inherited and only partly discharged.** `export.arxiv.org` returned
  HTTP 429 to this leg exactly as it did to leg 382; the arXiv half of that leg's prior-art
  hole is **still open**. Crossref was reachable and searched weakly (novelty pass §3).
  No mathematical novelty is claimed, so only a citation could change.
* **Left to a successor:** leg 382's `rel_tolerance` δ mode and this adapter have **not** been
  composed — the δ a caller owes and the `ω` a caller owes are two separate statements of
  the same thing (accuracy), and whether they should be one input is unexamined here.
  A per-cell (rather than global) `δ` does not exist in leg 382's routine and would be its
  owner's change, not this leg's.
* No `L1 → L4` link moved. Ceiling TIER 2. Clay ~0.05%.
