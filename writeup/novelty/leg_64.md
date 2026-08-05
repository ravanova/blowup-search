# Leg 64 — Route-A12 v1: novelty / literature pass

**Leg 64, Route-A12 v1. Date of pass: 2026-08-05.** Pure literature leg — no computation, no
gCLM measurement (the standing ban is respected: this leg searches literature *about* an
already-computed number and runs nothing).

**The question, as posed in the leg's gate, verbatim:**

> Does any primary source publish `alpha_1` at `a = 1/2` (or the `sigma = 3` criticality
> statement it comes from) for this model?

**Answer: the disjunction splits, and the two halves get opposite answers.**

* **`sigma = 3` criticality at `a = 1/2` — YES, PUBLISHED, and in TIER 1.** Xu
  (arXiv:2607.19762) §6.1 eq (6.3) + **Table 1 row `a = 0.5`** + **Figure 3** state
  `s*(1/2) = 3` **exactly**, in as many words. The standing repository claim that criticality
  at `a = 1/2` is "in neither ALS nor XU" is **wrong about XU** and must be corrected.
* **`alpha_1` at `a = 1/2` — NO, not published anywhere located.** Searched beyond Tier 1
  and Tier 2 across the full arXiv `Constantin-Lax-Majda` corpus (100-result API enumeration)
  plus the four dissipative primary sources read in full text. The dissipative-gCLM exact-
  solution corpus is `(a,sigma) ∈ {(0,0), (0,1), (0,2), (1/2,1)}` on the line and
  `{(0,0), (0,1), (1/2,0), (1/2,1)}` periodic. **`sigma = 3` carries no exact solution, no
  numerical study, and no marginal-case expansion in any source located.**

---

## 1. The query log — links, not counts

Every query string below was issued verbatim on **2026-08-05**. Links are the returned items
that were actually opened or otherwise judged relevant; the rest were off-topic (the
`"0.133683"` query in particular returned only condensed-matter critical-exponent papers).

### Web searches

| # | query string (verbatim) | relevant links returned |
|---|---|---|
| Q1 | `generalized Constantin-Lax-Majda equation critical fractional dissipation exponent a=1/2 sigma=3` | https://arxiv.org/abs/1908.09385 · https://arxiv.org/abs/2207.07548 · https://arxiv.org/pdf/2411.01891 · https://iopscience.iop.org/article/10.1088/1361-6544/ad140c · https://researchwith.njit.edu/en/publications/global-existence-and-singularity-formation-for-the-generalized-co/ |
| Q2 | `gCLM marginal critical dissipation self-similar exponent derivative with respect to viscosity mu_tau = -alpha_1 mu^2 algebraic decay` | https://arxiv.org/html/2607.19762v1 · https://arxiv.org/pdf/1908.09385 — **no hit on the marginal expansion**; remaining results were unrelated (plasma viscosity, Leray equations, Markov chains) |
| Q3 | `Constantin-Lax-Majda a=1/2 dissipation Lambda^3 critical self-similar blowup persistence` | https://arxiv.org/abs/1908.09385 · https://arxiv.org/pdf/2411.01891 · https://arxiv.org/abs/2607.19762 · https://arxiv.org/pdf/2401.14615 |
| Q4 | `"generalized Constantin-Lax-Majda" dissipation marginal case rescaled viscosity parameter dynamical system fixed point second order coefficient` | https://arxiv.org/pdf/2506.02800 · https://www.researchgate.net/publication/326959516_Unimodal_solutions_of_the_generalized_Constantin-Lax-Majda_equation_with_viscosity · https://arxiv.org/pdf/2207.07548 — the only "marginal" hit is **ALS's `sigma = 0`**, an unrelated use of the word (see §4) |
| Q5 | `arXiv generalized Constantin-Lax-Majda equation fractional dissipation 2025 2026 self-similar profile viscosity dependence exponent` | https://arxiv.org/html/2607.19762v1 · https://arxiv.org/html/2603.25104 · https://arxiv.org/pdf/2401.14615 · https://arxiv.org/abs/1908.09385 |
| Q6 | `"0.133683" OR "critical dissipation" gCLM "a = 1/2" sigma = 3 marginal exponent alpha_1` | **nothing in the model's literature.** All ten returns were condensed-matter/statistical-mechanics critical-exponent papers (e.g. https://arxiv.org/pdf/1602.08187, https://arxiv.org/pdf/2310.11525). The one fluid-adjacent return was https://arxiv.org/pdf/2312.01702 (log-lattice singularity tracking, already Tier 2 here). |
| Q7 | `Sakajo generalized viscosity Constantin-Lax-Majda arbitrary derivative order blow-up small viscosity global solutions` | https://www.ms.u-tokyo.ac.jp/journal/abstract/jms100107.html (Sakajo, *J. Math. Sci. Univ. Tokyo* **10** (2003) 187–207) · https://ui.adsabs.harvard.edu/abs/2003Nonli..16.1319S/abstract (Sakajo, *Nonlinearity* **16** (2003) 1319–1328) · https://www.math.kyoto-u.ac.jp/~sakajo/research/CLM/CLM.html |

### Corpus enumeration (not a ranked search)

| # | query | result |
|---|---|---|
| Q8 | arXiv API, `https://export.arxiv.org/api/query?search_query=all:"Constantin-Lax-Majda"&start=0&max_results=100` | 50,349 bytes of Atom, enumerated by title. The **dissipative-gCLM subset is four papers**: `1908.09385` (J. Chen), `2207.07548` (ALS), `2411.01891` (Silantyev–Lushnikov–Siegel–Ambrose, periodic), `2607.19762` (Xu). Everything else in the corpus is inviscid gCLM/De Gregorio (`2401.14615`, `2305.05895`, `2603.25104`, `2506.02800`, `2603.06182`, `1811.09754`, `1710.02737`, `1707.05205`, `2010.01201`), or geometric/right-invariant-metric work on the same operator (`1202.5122`, `1504.08029`, `1105.0327`, `2504.14346`), or 3D-Euler/Boussinesq papers that merely cite CLM (`0803.1784`, `2604.01244`, `2603.26715`, …). |

### Full-text retrieval and grep (the part that decides the gate)

Four PDFs fetched with `bash Papers/fetch.sh 2607.19762 2207.07548 2010.01201 1908.09385`
(all four on the first attempt), text-extracted with `pdftotext -layout`, and grepped. **These
are primary-source reads, not abstract reads.** Line numbers below are into the extracted text
and are given so the reads are reproducible.

| source | what was grepped | what came back |
|---|---|---|
| `2607.19762` (Xu) | `s\*`, `Table 1`, `critical`, `marginal`, `Appendix A` | §6 at L1751; §6.1 at L1760; eq (6.3) at L1769; **the `s*(1/2) = 3` sentence at L1794–1797**; Figure 3 caption L1818–1829; **Table 1 at L230–247**, row `a = 0.5` |
| `2207.07548` (ALS) | `a = 1/2`, `σ = 3`, `(61)`, section headings | §5.1 `a=0,σ=2` (L1044) · §5.2 `a=1/2,σ=1` (L1178) · §5.3 `a=0,σ=1` (L1298, eq (61) at L1385) · §5.4 `a=0,σ=0` (L1561). **No `σ = 3` anywhere.** |
| `2010.01201` (LSS) | `viscos`, `dissipat`, `Lambda^`, `nu` | **one hit, and it is a bibliography entry** (L2236, the citation to ALS's *Nonlinearity* 33 (2020) paper). LSS is an **inviscid** paper. It cannot contain `alpha_1`. |
| `1908.09385` (J. Chen) | `a = 1/2`, `critical`, `self-similar exponent`, `s = 3` | Chen's "critical dissipation" is **a different notion** — see §4. His `a = 1/2` self-similar ansatz is at L195–222 and is **inviscid** (`ν = 0`, stated in the line). |

---

## 2. The `sigma = 3` half — PUBLISHED, in Tier 1, verbatim

**Xu, arXiv:2607.19762, §6.1, immediately after eq (6.3)** (extracted-text L1794–1797), verbatim:

> "The branch value is tested at `a = 1/2`, where `s∗ = 3` exactly (`cl(1/2) = 1/3` by the
> exact solution of [20]; also [4, Thm. 2]) and J. Chen [20] proved blow-up at `s = 2 < 3`
> (subcritical), consistent with persistence."

**Xu Table 1** (paper page 4; extracted-text L230–247), the row that matters, verbatim:

> ` 0.5   0.3333   0.833   3.000   J. Chen [20]: blow-up at s = 2 < 3 (subcritical)`

with the table caption stating "`cl(1/2) = 1/3` is exact ([20]; also [4, Thm. 2])". **Xu
Figure 3** is annotated in the plot itself: "`s * (1/2) = 3 (exact)`".

Xu's `[20]` is **J. Chen 2020, *Nonlinearity* 33 2502–2532 (arXiv:1908.09385)**; `[4]` is
**Lushnikov–Silantyev–Siegel 2021, *J. Nonlinear Sci.* 31 art. 82 (arXiv:2010.01201)**.

**The exponent dictionary check, because this is exactly where a verdict inverts.**
`LITERATURE_CHECK.md` records it: ALS/XU write `ω ~ τ^{-β} f(x/τ^{c_l})`, their `Λ^σ` is our
`(-Δ)^s` with `σ = 2s`, and our `α = 1/c_l`, so `s_c(ours) = α/2 = s*(XU)/2`. At `a = 1/2`:
their `c_l = 1/3` → their `s* = 3` → our `σ_c = 2s_c = 3`, our `s_c = 3/2`. **Xu's `s*(1/2) = 3`
and our "criticality at `a = 1/2` is `σ = 3`" are the same statement, digit for digit, and
theirs is exact where ours is a numerical branch value.** Precision available for comparison:
`3` exactly, both sides; the underlying `c_l(1/2) = 1/3` is exact in the literature ([20],
[4, Thm. 2]), Xu's own recompute prints `0.3333` (Table 1), and this repository's cold
integration of ALS (49)–(50) printed `0.3333076`, **rel 7.7e-5** (`PHASE2_P2_NOTES.md` J-3).

**This half of the gate answers YES**, and it lands one rung earlier than the leg expected —
not in a Tier-2 or Lushnikov-adjacent source, but in a Tier-1 paper the repository had already
read for a *different* claim.

## 3. The `alpha_1` half — NOT PUBLISHED in anything located

`alpha_1 := dα/dμ` at the marginal fixed point is defined in `solver/critical_dissipation.py`
by promoting the rescaled dissipation coefficient `μ(τ) := ν/(A L^{2s})` to a dynamical
variable, giving the autonomous pair `(Ω, μ)` with `μ_τ = (2s − α[Ω,μ]) μ`; at `2s = α_0` the
linear term vanishes and `μ_τ = −α_1 μ² + O(μ³)`. **It is a second-order coefficient of the
marginal-case flow, not a criticality threshold** — the threshold is `s*`, which Xu publishes;
`alpha_1` is what decides the case `s = s*` that Xu explicitly declines to decide.

Xu says so himself, in the same subsection (§6.1, L1777–1781), verbatim:

> "That the inviscid profile then persists as the attractor is the program of Section 8, not
> established here (the required weighted dissipation-form bound, nonlinear estimate, and
> modulation closure are open, Appendix A); and `s*` is not the sharp critical dissipation
> curve separating blow-up from global regularity, which for this family remains unknown."

and

> "The case `s = s∗` is marginal (`γ = 0`) and `s > s∗` is relevant (the open supercritical
> regime)."

Xu's Appendix A ("The exact linear semigroup at `a = 0`", L1984) is at `a = 0` only, and Xu
states (L359) that the semigroup theorems "all live at `a = 0`". **So the one paper that
publishes the `σ = 3` threshold at `a = 1/2` states in the same breath that the marginal case
there is open and that its own machinery does not reach `a = 1/2`.**

**What the rest of the corpus does at `a = 1/2` with dissipation, exhaustively:**

| source | `a = 1/2` content | `σ` covered | reaches `σ = 3`? |
|---|---|---|---|
| ALS `2207.07548` §5.2 | exact pole-dynamics solution, real line | `σ = 1` | **no** |
| ALS `2207.07548` §5.1/§5.3/§5.4 | `a = 0` only | `σ = 2, 1, 0` | **no** |
| SLSA `2411.01891` | exact **periodic** pole dynamics | `σ = 0, 1` (abstract, verbatim: "new periodic solutions for `a = 0` and `1/2` and `σ = 0` and `1`") | **no** |
| J. Chen `1908.09385` | nonlinear-stability blow-up proof | `γ = 2` (Xu: "`s = 2 < 3`, subcritical") | **no** |
| Xu `2607.19762` | `s*(1/2) = 3`, the threshold itself | threshold only; dynamics `a = 0` | **states it, does not analyze it** |
| LSS `2010.01201` | inviscid branch, `a_c = 0.6890665` | none (inviscid) | **no** |
| Sakajo *Nonlinearity* **16** 1319 / *JMSUT* **10** 187 | `a = 0` | arbitrary derivative order, but **thresholds in `ν`**, not exponent derivatives | **no** |

**Nothing in the located literature computes, estimates, or names a number of the type
`dα/dμ` for this model, at `a = 1/2` or at any other `a`.** The nearest published object in
kind is ALS §5.3 eq (61) at `a = 0`: a self-similar form carrying `ν` **inside** the profile at
fixed exponents `c_l = β = 1`, i.e. a one-parameter family of viscous self-similar blow-ups —
which is exactly the statement `alpha_1 = 0` at `a = 0`, and which this repository already
records as confirmed-and-known. **That precedent is what makes the `a = 1/2` gap conspicuous
rather than obscure: the analogous object one rung up the branch has never been written down,
because `σ = 3` has no exact solution to write it down from.**

## 4. Two traps that would each have produced a wrong verdict

**Trap 1 — "critical dissipation" means two different things at `a = 1/2`, and they differ by
a whole unit of `σ`.** J. Chen (`1908.09385` §1.2, L84–96) defines criticality by **norm
scaling**: `‖ω(t,·)‖_{L^{|a|^{-1}}}` is the conserved-in-scaling norm, so `Λ^γ` with
`γ = |a|^{-1}` is *his* critical dissipation. At `a = 1/2` that is **`γ = 2`**. The
scaling-relevance criticality of the *self-similar profile* — the one this repository's
`alpha_1` sits at — is **`σ = 3`**. A search that reads Chen's "we prove global
well-posedness with critical dissipation" as covering the point in question would wrongly
close the gate; Chen's `s = 2` result is, in Xu's own classification, **subcritical**.

**Trap 2 — ALS's "marginal dissipation" is `σ = 0`, not the marginal case.** ALS's
introduction (L~213) calls `σ = 0` "'marginal' dissipation" (it arises in a 1D Oldroyd-B
stress model). That is a wholly unrelated use of the word: it is the *bottom* of the `σ`
range, not the point `σ = σ_c`. Query Q4's only "marginal" hit in the dissipative corpus is
this one, and it is a false friend.

## 5. What this pass changes in the repository's own records

Reported for the orchestrator to apply — **this leg does not edit either file**, both being
outside its territory.

**(A) `capabilities.py` line 80, `solver/critical_dissipation.py`'s entry.** Current text:

> `"validated": "alpha_1 = 0 at a=0 == ALS eq (61); a=1/2 is UNSEARCHED at primary source"`

The first clause is **correct and stays** (ALS `2207.07548` §5.3 eq (61), extracted-text
L1385, is the `a = 0, σ = 1` self-similar form with `ν` inside the profile at `c_l = β = 1`).
The second clause is **stale in both directions** and should become, e.g.:

> `"validated": "alpha_1 = 0 at a=0 == ALS eq (61); criticality sigma=3 at a=1/2 IS published (XU arXiv:2607.19762 sec 6.1 + Table 1 row a=0.5 + Fig 3, 's*(1/2)=3 exactly'); alpha_1 = +0.133683 there is SEARCHED-NOT-FOUND (leg 64), i.e. measured, not independently validated"`

**(B) `LITERATURE_CHECK.md` row `α₁ = +0.133683 at a = 1/2 | Route-H v1 | not in Tier 1 |
unsearched`.** Two corrections: the source column's "not in Tier 1" is **wrong for the
`σ = 3` half** (Xu is Tier 1 and publishes it), and the verdict column should move from
`unsearched` to **`searched — not found`** for the `alpha_1` half.

**(C) `PHASE2_P2_NOTES.md` J-2's parenthetical**, verbatim: "(criticality there is sigma=3,
in neither ALS nor XU)". **The clause is false about XU.** It is true about ALS. The sentence
it supports — that `alpha_1` itself is not in Tier 1 — survives intact; only the reason given
for it is wrong, and the corrected reason is stronger: Xu publishes the threshold and
explicitly leaves the marginal case at it open.

## 6. The honest label for the number

`alpha_1 = +0.133683` at `a = 1/2` is now **searched and not found**, which is a different and
better-supported statement than "unsearched" — and it is still **not** "novel". The precise
status, and the words worth using:

**Measured, not independently validated.** One instrument, one basis, one convergence study:
`K = 96/144/192/240` gives `0.132770 / 0.133470 / 0.133628 / 0.133683`, a spread of
**9.1e-4** across the ladder and **5.5e-5** between the last two rungs — a self-consistency
measure at float64, with no interval enclosure, no second discretization, and **no external
number to check against, because none exists**. The sign is the load-bearing part
(`alpha_1 > 0` ⇒ `μ` decays like `1/(alpha_1 τ)`, algebraically, so the critical viscous
solution relaxes onto the inviscid profile), and the sign is stable across every rung of the
ladder with margin `0.1328` to `0.1337` — about **2400×** the last-rung spread away from zero,
which is the magnitude that matters, not the digit count.
