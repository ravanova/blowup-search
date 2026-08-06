# Phase-2 P2 — Is the survival boundary of the a>0 two-scale traveling wave genuine or genome-limited? An a_p(K) convergence map

> **SCOPE OF THE WORD "TWO-SCALE" IN THIS NOTE (corrected, leg 180).** Everything measured
> here lives at **`a > 0`**, on the sampled grid `a ∈ {0, 0.3, 0.4, 0.45, 0.5, 0.55, 0.6,
> 0.65, 0.7, 0.8, 0.9, 1.0}`. "Two-scale" names the **residual/ansatz** `R₂ = Ω H(Ω) −
> c_tw Ω_X − a U Ω_X` and its `a = 0` anchor — HQW25's exact CLM traveling wave `Ω₂ =
> −1/(1+X²)` — and nothing more. It is **not** a claim that the published two-scale
> self-similar blowup *scenario* extends to `a > 0`: Huang–Tong–Wang (`arXiv:2603.25104`,
> full text read at leg 112) scope that scenario to **`a ≤ 0`**, and report *one-scale*
> self-similar blowups for `a > 0` — a statement about which scenario **degenerate initial
> data** produce. The object measured below is a different one and is published in its own
> right: the same paper's Theorem 2.7 gives a traveling wave for every `a ∈ (−∞, 1)`, and
> Theorem 7.10(3) makes it compactly supported for `0 < a < 1`. So `a*` is the boundary at
> which the **`a > 0` continuation of the `a = 0` two-scale traveling wave** stops fitting
> the two-scale residual to `10⁻²` — a property of this continuation, not of the two-scale
> scenario.

**Status: a novel toy-model result (Tier-1/2), NOT a Clay solve.** This note
*sharpens* the prior leg ([TECHNICAL_P2_TWO_SCALE.md](TECHNICAL_P2_TWO_SCALE.md)),
whose one honest failure (T4) was that the two-scale survival window `a_p ≈ 0.40`
was measured with a *fixed* even K=2 genome and a richer genome beat it. Because a
GA gives only an **upper bound** on the true minimal residual, `a_p(K)` can only
*rise* with genome richness K. The open question this leg answers:

> Does `a_p(K)` **saturate** as K grows (→ a genuine survival boundary `a* > 0` where the
> `a > 0` continuation of HQW25's proven `a = 0` two-scale traveling wave really stops
> fitting the two-scale residual under advection), or keep
> **marching out** with K (→ no sharp boundary is resolvable — an honest
> INCONCLUSIVE that would point straight to a rigorous / adaptive step)?

**Answer: it saturates.** `a_p(K) = 0.40 → 0.50 → 0.50`, and at the boundary the
residual floor is GA-converged, genome-converged, and basis-independent. The
boundary is **`a* ≈ 0.5–0.55`**, i.e. **strictly inside `a > 0`**, with a soft
`~10⁻²` floor — genuine, not an artifact of a too-simple profile family.

Rebuild the figure from committed data (no GA re-run):
`python writeup/4_p2_lottery/p2_two_scale_kladder_evidence.py` →
`writeup/figures/fig18_two_scale_kladder.png` (reads
`writeup/data/p2_two_scale_kladder.json`; regenerate the data with
`python experiments/p2_two_scale_kladder.py --logged`).

Code: `solver/gclm_family.py` (+ new cross-check basis `even_lorentz_sq`),
`solver/ga_search.py`; harness `experiments/p2_two_scale_kladder.py`; tests
`test_gclm_family.py` (12/12; full suite 7 files green).

---

## 1. Setup: the same residual, a K-ladder of genomes

The object is unchanged from the prior leg — the two-scale (traveling-wave)
rescaled residual of the gCLM `a`-family, with the scale-invariant fitness:

    R₂(Ω) = Ω H(Ω) − c_tw Ω_X − a U Ω_X,   U = ∫₀ˣ H(Ω) dX',   c_tw = least-sq speed,
    relres(Ω) = ‖R₂(Ω)‖ / ‖Ω H(Ω)‖.

What changes is the search space. We minimise `relres` over the **even Lorentzian**
genome `Ω = Σₖ Aₖ/(1+Bₖ X²)` at a *ladder* of K = 2, 3, 4 poles (and K=6 as a
spot-check), and read off, per K,

    a_p(K) = largest a > 0 with the converged floor(a; K) < 10⁻².

Since the K-pole family contains the (K−1)-pole family, `floor(a; K)` is
non-increasing in K and `a_p(K)` non-decreasing — the whole point.

## 2. The confounder that is the entire ballgame: GA convergence

`a_p(K)` is only meaningful if `floor(a; K)` is the **true genome optimum**, not a
figure the GA failed to reach. Near the transition it is *not*, at the old budget:

- **GA-convergence probe** (`--converge`): at **a = 0.6, K = 4**, doubling the base
  budget cut the floor **45 %** (`3.49×10⁻² → 1.91×10⁻²`). A naive `a_p(K)` map at
  the base budget would have measured GA *effort*, not genome richness.

So before locking anything we ran a **scratch plateau probe** — a=0.55 and 0.60,
K∈{4,6}, budgets 1× → ~8× (`pop×gen×seeds` from `80×130×6` to `250×350×10`):

| a | K=4: 1× → 3× → 8× budget | K=6: 1× → 3× → 8× |
|---|---|---|
| 0.55 | 1.15e-2 → 1.08e-2 → **1.03e-2** | 1.31e-2 → 1.23e-2 → **1.09e-2** |
| 0.60 | 2.26e-2 → 1.78e-2 → **1.84e-2** | 2.63e-2 → 2.32e-2 → **1.74e-2** |

The floor **plateaus**: at the converged budget K=4 and K=6 agree and stop
dropping. This (a) told us the boundary is real, and (b) fixed the **logged budget
at `pop=150, gen=250, 8 seeds`** (matches the ~8× column), with an **in-JSON**
budget spot-check (re-run K=4 at ~1.7×) and K=6 genome spot-check so the plateau is
reproducible from committed data, not just scratch.

## 3. The cross-check basis (rules out Lorentzian-family bias)

A saturating `a_p` could, in principle, be a limitation of the *Lorentzian family*
rather than of the equation. So we added a genuinely different even basis,
`even_lorentz_sq` = `Σₖ Aₖ/(1+Bₖ X²)²` (sharper peak, `X⁻⁴` tails), and use the
6-DOF mix (1 Lorentzian + 2 squared poles) against even K=3 (also 6-DOF). Its unit
test (`test_even_lorentz_sq_crosscheck_basis`) pins the two properties that make it
an honest control: a **single squared pole is NOT an a=0 traveling-wave null**
(`relres = 0.11`, i.e. genuinely new shape space), yet the mix still **contains the
exact anchor** (Lorentzian + zero-squared → `relres = 1.3×10⁻⁸`), so the a=0
known-answer gate still passes on it.

## 4. The logged sweep and the locked predicate

**Config (locked, commit `44a507c`):** `a ∈ {0, 0.3, 0.4, 0.45, 0.5, 0.55, 0.6,
0.65, 0.7, 0.8, 0.9, 1.0}` (dense near the edge); n=801; even genome K=2,3,4;
converged budget `150×250×8`; K=6 + mixed-basis + ~1.7× budget spot-checks at
`a ∈ {0.5, 0.55, 0.6}`. Predicate T1–T7, verdict **descriptive**, no clause-chasing.
**Result: 7/7.**

| # | Clause | Outcome |
|---|--------|---------|
| **T1** | a=0 all K `floor < 1e-4` (known answer) | **PASS** (5.5e-8) |
| **T2** | K=2 *understates*: `a_p(K≥3) > a_p(K=2)` | **PASS** (0.50 > 0.40) |
| **T3** | boundary *saturates*: `a_p(4) ≤ a_p(3) + 1 grid step` | **PASS** (0.50 ≤ 0.55) |
| **T4** | floor *converged* at boundary (K6 ≥ 0.7·K4 **and** 1.7×-budget within 25 %) | **PASS** |
| **T5** | far-end robust: converged K4 floor `> 5e-2` at a=1 | **PASS** (1.28e-1) |
| **T6** | resolution guard: min verdict width `> 8` pts | **PASS** (35 pts) |
| **T7** | basis-independent: mixed within 3× of even K=3 at boundary | **PASS** |

## 5. The map (Fig18)

The full floor table (scale-invariant `relres`, converged budget):

| a | K=2 | K=3 | K=4 | K=6 | mixed | K4 @1.7× |
|---|-----|-----|-----|-----|-------|----------|
| 0.00 | 5.5e-8 | 5.6e-8 | 6.0e-8 | | | |
| 0.30 | 1.4e-3 | 1.3e-3 | 1.3e-3 | | | |
| 0.40 | 5.5e-3 | 1.4e-3 | 1.4e-3 | | | |
| 0.45 | **1.2e-2** | 2.5e-3 | 2.7e-3 | | | |
| 0.50 | 2.1e-2 | 5.5e-3 | 5.2e-3 | 5.5e-3 | 4.0e-3 | |
| 0.55 | 3.1e-2 | **1.2e-2** | **1.1e-2** | 1.2e-2 | 8.3e-3 | 1.0e-2 |
| 0.60 | 4.2e-2 | 1.9e-2 | 1.8e-2 | 2.3e-2 | 1.7e-2 | 1.8e-2 |
| 0.65 | 5.5e-2 | 3.7e-2 | 2.8e-2 | | | |
| 0.70 | 6.9e-2 | 4.9e-2 | 4.1e-2 | | | |
| 0.80 | 1.0e-1 | 7.8e-2 | 7.0e-2 | | | |
| 0.90 | 1.4e-1 | 1.0e-1 | 1.1e-1 | | | |
| 1.00 | 1.8e-1 | 1.3e-1 | 1.3e-1 | | | |

Reading it (Fig18 Panels A–C):

- **K=2 understates the boundary.** Its floor crosses `10⁻²` already at a≈0.45
  (`a_p(K2)=0.40`); K=3 and K=4 keep the floor below `10⁻²` out to a=0.50
  (`a_p=0.50`). This is precisely the prior leg's T4 fail, now quantified.
- **`a_p(K)` saturates.** `0.40 → 0.50 → 0.50`: the jump is K=2→K=3, then K=4 adds
  nothing, and **K=6 does not beat K=4** anywhere at the boundary (a=0.55:
  K6=1.2e-2 ≥ K4=1.1e-2). The boundary does **not** march out with richer genome.
- **The boundary is GA-converged.** At a=0.55 the K=4 floor is `1.08×10⁻²` and at
  ~1.7× budget `1.03×10⁻²` (< 5 % change); at a=0.60, `1.78×10⁻²` vs `1.84×10⁻²`.
- **It is basis-independent.** The different-basis (Lorentzian+squared) floor tracks
  even K=3 to within a small factor at every boundary point (a=0.55: 8.3e-3 vs
  1.2e-2; a=0.60: 1.7e-2 vs 1.9e-2).
- **The far (De Gregorio) end is robust** to both K and budget: the converged K=4
  floor still rises to `1.28×10⁻¹` at a=1 — confirming across the whole ladder the
  one sub-claim the prior leg already found robust.
- **Resolution is not the story.** The selected half-max width in every verdict
  point is `≥ 35` grid pts (Panel D), far above the 8-pt guard — no collapsing fine
  inner scale is being mis-resolved.

## 6. The honest nuance we did NOT bury

`a*` is **not a razor edge.** Right at a=0.55 the converged floors *straddle* the
`10⁻²` line: even K3/K4 sit just above (≈1.1×10⁻²) while the mixed basis dips just
under (8.3×10⁻³). That is exactly what a threshold crossing of a smoothly-rising,
slightly basis-sensitive floor looks like. So the defensible statement is:

> **On `a > 0`, the continuation of HQW25's exact `a = 0` two-scale traveling wave
> persists (converged `relres < 10⁻²`) to `a ≈ 0.5`, and its residual floor crosses
> the `10⁻²` threshold in the band `a ≈ 0.5–0.55`, where the floor is
> GA-/genome-converged and basis-independent — a genuine, resolvable boundary, not a
> genome artifact.** It is a soft crossing of a rising floor, not a sharp collapse at
> a single `a*`, and it is a statement about this `a > 0` continuation only — not about
> the published two-scale *scenario*, which `arXiv:2603.25104` scopes to `a ≤ 0`.

## 7. Scope: what this is and isn't

This closes the prior leg's T4 caveat: the survival boundary is genuine and
saturates near `a ≈ 0.5–0.55`, and the map is now a *converged* upper-bound curve
with explicit GA-, genome-, and basis-convergence controls. But the ceiling is
unchanged:

- the whole map is measured on **`a > 0`** and says nothing about `a ≤ 0`, which is
  where `arXiv:2603.25104` places the two-scale self-similar blowup *scenario*; the
  boundary is a property of the `a > 0` traveling-wave continuation this note built,
  and reading it as a boundary of that scenario would be a domain error (see the
  scope box at the top);
- a GA minimising a residual **proves nothing** — Tier-1/2 evidence, not a proof;
- `floor(a; K)` is still an upper bound (we have shown it is *converged* at the
  boundary, not that it is the true infimum over *all* profiles);
- the value toward the roadmap is a **sharper, better-justified Route-D guess**: the
  a=0 exact profile and the near-boundary (`a ≈ 0.5`) converged profiles, plus the
  reusable `residual_two_scale` object, are what a rigorous interval-Newton /
  Newton–Kantorovich step would try to certify.

**Next (chosen): Route D** — the first rung that is genuinely "novel maths": can a
*certifiable* fixed-point statement even be set up for `residual_two_scale`
(bounding the inverse, defect, Lipschitz constant), gated against the a=0 exact
anchor? Scoped honestly as an open question, not a promised certificate. Clay odds
unchanged (**~0.05 %**).
