# TECHNICAL — Route-CLOC (leg 381): verifying `CLAY_OBLIGATIONS.md` §4

**Gate answer, in the gate's own wording: YES** — "the reviewer's arithmetic survives (i) with the
DSS modulation handled, AND (ii) confirms the bounded-energy reading against the primary text" —
**with one refuted side-clause, one labelling correction, and one repaired derivation step**, all
routed to integration verbatim in §6 below.

**Ceiling: Tier 2. No link of the `L1 → L4` chain moved. Clay stays ~0.05%.** Verifying an
obligation is not such a link. This leg builds no certificate, no enclosure, and attempts no
localisation.

* Runner: `experiments/p2_route_cloc_v1.py` (self-tests: **ALL PASS**)
* Figure: **`fig104`** — `writeup/figures/fig104_route_cloc_v1.png`, rebuilt by
  `experiments/p2_route_cloc_v1_evidence.py` from the curated JSON alone (nothing recomputed),
  registered in `writeup/build_figures.py`. Added by a later DOCS-lane pass that closes this
  leg's missing-figure audit finding; it plots this leg's banked numbers and changes none of
  them. **Caption:** *fig104 — Route-CLOC (leg 381). Panel A, the cutoff bill at the banked
  Type-I exponent `α = 1`: the nonlinear residual (`ρ^{−1.4993}`), the viscous residual
  (`ρ^{−1.4999}` — identical scaling to the nonlinear one at exactly `α = 1`), the divergence
  defect (`ρ^{−0.4996}`) and the pressure perturbation at the origin (`ρ^{−1.9997}`) all shrink
  with the cutoff radius over `ρ = 10 … 1000`, while the critical `L³` tail stays flat
  (`13.1764 → 13.1773`, exponent `1.28e−05`). Panel B, the term that never gets cheap: the cube
  of the discarded `L³` tail grows by a constant **326.875 per decade** of window, constant to
  `7.4e−10` across four increments — log-divergent, so no cutoff radius makes it small. Panel C,
  the DSS exponent equals the SS exponent: `0.499999942` vs `0.500000000`, ratio `0.9999998844`
  (no factor), while dropping the log-periodic modulation — which swings `G` by `2.99×` within
  one period — biases the fit to `0.4876`, `2.47 %` off. This is a **Tier-2-ceiling verification
  result: no `L1 → L4` link moved, Clay stays ~0.05 %.* Panel C shows the banked scalars: the
  per-sample energy series `E(s)` and the factor `G(s)` are not in the curated JSON, so no
  fit-through-data overlay is drawn.
* Curated data: `writeup/data/p2_route_cloc_v1.json` — every number below is in it
* Novelty pass: `writeup/novelty/leg_381.md`, committed before the runner existed
* Journal: `experiments/journal/leg_381.md`

---

## 1. What was verified, and what "handled rather than dropped" cost

### 1.1 The derivation, independent of the reviewer's

Similarity variables at blow-up time `T*`, standard normalisation:

```
y = x / sqrt(T*-t),   s = -log(T*-t),   u(x,t) = (T*-t)^{-1/2} U(y,s)
```

The NS scaling symmetry `u ↦ Λ u(Λx, T* − Λ²(T*−t))` acts in `(y,s)` as the shift `s ↦ s + 2 log Λ`.
A `λ`-DSS solution is invariant at the single value `Λ = λ`, hence

```
DSS  ⟺  U(y, s + 2 log λ) = U(y, s)          [leg 260's framing, reproduced not assumed]
```

with exact self-similarity the degenerate case `∂_s U = 0`. Then

```
E(t) = ∫_{ℝ³}|u|²dx = (T*−t)^{−1}·(T*−t)^{3/2}·∫|U(y,s)|²dy = (T*−t)^{1/2} G(s),
G(s) := ∫|U(·,s)|²dy,   G(s + 2 log λ) = G(s).
```

**Structural reason no exponent can shift.** The DSS group `λ^ℤ` is a *subgroup* of the same
one-parameter scaling group that fixes the SS exponents. Restricting `ℝ_{>0}` to `λ^ℤ` cannot change
an exponent; it can only replace the *constant* `∫|U|²dy` by a *periodic function* of `s`. So the
`(T*−t)^{1/2}` is not an artefact of exact self-similarity, and the modulation enters as a bounded
positive prefactor oscillating in `[min G, max G]` — which means `E(t)(T*−t)^{−1/2}` has **no limit**
as `t → T*` unless `G` is constant.

### 1.2 The numerical falsifier

An explicitly-constructed synthetic field that is **exactly `λ`-DSS** and **exactly
divergence-free**, poloidal, non-axisymmetric (two orthogonal axes), with tunable algebraic decay
`α` and a strong prescribed log-periodic modulation:

```
P[ψ](y) = curl curl (ψ(r) e) = (ψ'' − ψ'/r)(ŷ·e) ŷ − (ψ'' + ψ'/r) e
U(y,s)  = m₁(s) P[ψ_α](y; c) + m₂(s) P[ψ_α](y; d),   c·d = 0,   ψ_α(r) = (1+r²)^{(2−α)/2}
```

| what it is checked to be | measured | tolerance |
|---|---|---|
| exactly `λ`-DSS: `u(x,t) = λ u(λx, T*−λ²(T*−t))`, `λ = 1.7` | max rel error **1.14e-15** | 1e-12 |
| exactly divergence-free (4th-order FD) | max rel **8.87e-12** | 1e-6 |
| the change of variables itself, checked in **physical** `x`-space against the similarity-variable prediction (different integral, different grid, different variable) | max rel disagreement **4.19e-15** | 1e-8 |

This field is **not** the route-4 candidate and is not claimed to be. Its only job is to catch an
algebra error in the derivation.

### 1.3 The exponent, and what dropping the modulation costs

| fit | exponent | note |
|---|---|---|
| exact SS (`∂_s U = 0`) | **0.500000000000** | pure power law, max rel residual **8.9e-16** |
| genuine DSS, **modulation handled** (log-periodic factor in the design matrix, period `2 log λ`) | **0.499999942** | max log-residual **1.58e-5** |
| genuine DSS, **modulation dropped** (naive OLS of `log E` on `log(T*−t)`) | **0.487628262** | **biased by 2.47 %** |

**THE FACTOR: `DSS exponent / SS exponent = 0.9999998844`, i.e. 1 to 1.2e-7. There is no factor.**
The DSS exponent is the SS exponent.

What the modulation actually does, measured on the same object:

* relative oscillation amplitude of `G` over one period: **2.99** (a 299 % swing) — so this is not a
  small perturbation of the SS case, and it still moves no exponent;
* best-fit period of the residual: **1.0574** in `s`, against `2 log λ = 1.0613` — **0.36 %**, i.e.
  the residual is the log-periodicity and nothing else;
* the naive fit's **2.47 % bias** is the price of dropping it. It is a *windowing artefact*, not an
  exponent — which is exactly the error a careless reader of the reviewer's one-line arithmetic
  would make, and exactly why the gate asked for the modulation to be handled.

### 1.4 The one step of the reviewer's arithmetic that is NOT valid as written

> "`∫|u|²dx` at time `t` scales as `(T*−t)^{1/2}∫|U|²dy`, so bounded energy requires `U ∈ L²(ℝ³)`."

In the case of interest — leg 260's banked object, where `U ∉ L²` — **both sides are `+∞`**, and an
identity between infinities cannot carry a conditional. The step needs replacing, not deleting. The
**truncated** law is finite for every `α` and every `ρ`, and reduces to the reviewer's statement
whenever both sides are finite:

```
E_ρ(t) = ∫_{|x|≤ρ}|u|²dx = (T*−t)^{1/2} ∫_{|y| ≤ ρ/√(T*−t)}|U|²dy
       ≍ [K(s)/(3−2α)] · ρ^{3−2α} · (T*−t)^{α−1}          (α < 3/2)
```

verified against quadrature:

| `α` | fixed-ball energy exponent, measured | predicted `α−1` | error |
|---|---|---|---|
| 0.80 | −0.20000 | −0.2 | 2.6e-5 |
| **1.00** | **−0.00026** | **0.0** | 2.6e-4 |
| 1.20 | +0.19710 | +0.2 | 2.9e-3 |
| 1.40 | +0.37430 | +0.4 | 2.6e-2 (finite-`R` effect near the `3/2` threshold, expected) |

**Same conclusion as the reviewer's, reached by a derivation that is valid in the case that
matters.** §4's conclusion stands; §4's *proof* needed this repair.

---

## 2. Where leg 260's banked object sits, in numbers

Leg 260 banked, from Chae–Wolf `arXiv:1610.09464` Thm 1.1 read in full by leg 253: every `λ`-DSS
solution is Type-I, `|U(y)| ≤ C/(1+|y|)`, i.e. **`α = 1`**.

| threshold | requires | banked value | verdict |
|---|---|---|---|
| `U ∈ L²(ℝ³)` (the Clay energy condition, via §1.1) | `α > 3/2` | `α = 1` | **short by Δα = 1/2; the certified exponent would have to be 1.5× the a-priori one** |
| critical `L³` tail finite | `α > 1` | `α = 1` | **fails, logarithmically** |
| fixed-ball energy decays as `t → T*` | `α > 1` | `α = 1` | **exactly critical: time-independent** |

Two magnitudes worth carrying:

* **The `L²` divergence is linear.** Shell integral ratio `∫_{10³<|y|<10⁶} / ∫_{1<|y|<10³} = 1000.32`
  — three decades of window give three decades of mass, reproducing leg 260's own "diverges
  linearly" independently and on a different (poloidal, non-axisymmetric) field.
* **`α = 1` is exactly the critical case for the *local* picture.** The fixed-ball energy exponent is
  `−0.00026` against a predicted `0`. So the total energy's divergence is a **pure far-field
  statement**, not a concentration statement: the energy inside any fixed physical ball is bounded
  and essentially constant right up to `T*`.

---

## 3. Step (iii): what the admissible-cutoff analysis would consume, as magnitudes

**This leg attempts no localisation.** Cutting off changes the equation's solution, so the obligation
is *transferred to §5's persistence question*, not discharged. What follows is the bill, not an
attempt to pay it.

### 3.1 Input 1 — the certified decay exponent

Built by **leg 382 (slot C, Route-DEXC)**, not by this leg, and this leg does not depend on its
landing: every magnitude below is a function of `α`. What the cutoff analysis needs is a **two-sided
enclosure `[α_lo, α_hi]`**, and **every bound below depends only on `α_lo`**. The thresholds that
change the answer are `α_lo > 1` (fixed-ball energy decays; critical `L³` tail finite) and
`α_lo > 3/2` (global `L²`). Currently available: `α = 1` a priori (Type-I), plus a *fitted*
per-candidate exponent from `solver/dssp_screen.py::fitted_far_field_decay_exponent` — and
`CLAY_OBLIGATIONS` §8 bullet 2 is right that fitted is not sufficient.

**Added after rebase (leg 382 landed while this leg ran; conclusions unchanged, pointer recorded).**
Leg 382's instrument certifies the *exact* power-law exponent set and therefore answers **EMPTY on
every real input** — no real profile is an exact power law — so it carries a tolerance `δ` and
returns a certified enclosure of **width ≈ 0.8686·δ (half-width ≈ 0.434·δ)**. Composing that with
the thresholds above gives the requirement this leg's magnitudes actually impose on slot C's
instrument: the usable quantity is `α_lo = α_centre − 0.434·δ`, so **`δ` must satisfy
`δ < (α_centre − 1)/0.434` for the fixed-ball-energy and critical-`L³` thresholds, and
`δ < (α_centre − 3/2)/0.434` for global `L²`** — while `δ` must simultaneously exceed the profile's
own departure from an exact power law on the window (leg 382 measured critical tolerances `δ*` of
`0.0697`, `0.3157`, `3.3529` on its three controls). Whether those two demands on `δ` are
simultaneously satisfiable for the real candidate is **not** settled by either leg, and is named
here as the composed open question rather than assumed away.

### 3.2 Input 2 — the perturbation size as a function of cutoff radius `ρ`

Cutoff `χ_ρ`: 1 on `|x| ≤ ρ`, 0 on `|x| ≥ 2ρ`, quintic transition. All exponents below are
**measured** on the synthetic field and agree with the closed forms to ≤ 0.1 %:

| quantity | closed form | measured exponent at `α = 1` | predicted |
|---|---|---|---|
| discarded tail, `L²` | `C ρ^{3/2−α}` | **+0.5000** | +0.5 (**divergent**) |
| discarded tail, `L³` (critical) | `C ρ^{1−α}` | **0.0000** | 0.0 (**log-divergent**) |
| discarded tail, sup at `ρ` | `C ρ^{−α}` | **−0.9991** | −1.0 |
| divergence defect `‖∇χ·u‖_{L²}` (Bogovskii source) | `C ρ^{1/2−α}` | **−0.4996** | −0.5 |
| Bogovskii corrector, `L²` scale | `C ρ^{3/2−α}` | **+0.5004** | +0.5 |
| nonlinear cutoff residual `‖(u·∇χ)u‖_{L²}` | `C² ρ^{1/2−2α}` | **−1.4993** | −1.5 |
| viscous cutoff residual `‖ν(2∇χ·∇u + (Δχ)u)‖_{L²}` | `ν C ρ^{−α−1/2}` | **−1.4999** | −1.5 |
| pressure perturbation at the origin | `C² ρ^{−2α}` | **−1.9997** | −2.0 |

Absolute sizes at `α = 1` (`ν = 1`, `C` the synthetic field's own amplitude), so the decay is
visible as numbers and not only as slopes:

| `ρ` | nonlinear residual `L²` | viscous residual `L²` | divergence defect `L²` | pressure pert. at origin |
|---|---|---|---|---|
| 10 | 4.19e-1 | 1.02e+0 | 2.39e+0 | 7.19e-2 |
| 100 | 1.33e-2 | 3.22e-2 | 7.58e-1 | 7.21e-4 |
| 1000 | 4.21e-4 | 1.02e-3 | 2.40e-1 | 7.21e-6 |

Three readings, each a magnitude:

1. **At exactly the Type-I exponent the nonlinear and viscous cutoff residuals scale identically**,
   both `ρ^{-3/2}` (`1/2 − 2α = −α − 1/2` ⟺ `α = 1`). For `α > 1` the nonlinear one is the smaller.
   So at the banked exponent there is no regime in which one of the two can be neglected.
2. **The pressure non-locality is not the obstruction.** `|δp(0)| ≍ C²ρ^{−2α}`, to be compared with
   the profile's own pressure scale `(T*−t)^{−1}`: the ratio is `ρ^{−2α}(T*−t) → 0`. Cutting off far
   away does perturb the pressure everywhere, including at the singular point, but by a relatively
   vanishing amount.
3. **What does *not* go away is the tail's size in critical norms.** Shown, not asserted: the cube of
   the `L³` tail grows by a **constant 326.875 per decade** of window (spread across five window
   widths: **7.4e-10** relative). At `α = 1` the discarded far field is not small in `L³` no matter
   how far out the cutoff is placed.

### 3.3 What this does *not* discharge

The residuals do go to zero with `ρ`. **Smallness of a residual is not persistence of a blow-up.**
What must be shown is that the localised solution *still loses smoothness at a finite time*, over a
time interval of length `~T*`, with the cutoff sitting at similarity radius `ρ/√(T*−t) → ∞`. That is
`CLAY_OBLIGATIONS` §5, classified there as **NO KNOWN METHOD, AND THE HARDEST ITEM**, and this leg
does not attempt it. §4's own sentence — "cutting off changes the equation's solution, so this
obligation is not discharged by the cutoff — it is transferred to §5" — is **verified as correct**,
and the magnitudes above are what §5 would be handed.

---

## 4. Step (ii): the official Clay statement, read directly

Source: Charles L. Fefferman, *Existence and smoothness of the Navier–Stokes equation*, the official
Clay Mathematics Institute problem description,
`https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf` (TeX creation date
2006-08-04, last modified 2013-02-05). Fetched by this leg and its text layer extracted; this
repository had **never previously cited the problem statement itself** (novelty pass §1).

Verbatim, the conditions `CLAY_OBLIGATIONS` §4 and §5 depend on:

```
(4)  |∂ᵅ_x u°(x)| ≤ C_{αK}(1+|x|)^{-K}         on ℝⁿ, for any α and K
(5)  |∂ᵅ_x ∂ᵐ_t f(x,t)| ≤ C_{αmK}(1+|x|+t)^{-K} on ℝⁿ × [0,∞), for any α, m, K
(6)  p, u ∈ C^∞(ℝⁿ × [0,∞))
(7)  ∫_{ℝⁿ}|u(x,t)|² dx < C  for all t ≥ 0   (bounded energy)

(C) Breakdown of Navier–Stokes solutions on ℝ³.  Take ν > 0 and n = 3.  Then there exist a
    smooth, divergence-free vector field u°(x) on ℝ³ and a smooth f(x,t) on ℝ³ × [0,∞),
    satisfying (4), (5), for which there exist no solutions (p,u) of (1),(2),(3),(6),(7)
    on ℝ³ × [0,∞).
```

Clause-by-clause verdict on the reviewer's load-bearing paragraph (4 confirmed, 1 corrected,
1 refuted):

| reviewer's clause | verdict | primary text |
|---|---|---|
| "direction (b) — exhibit a breakdown" | **CORRECTED (labelling)** | the breakdown statement on `ℝ³` is **(C)**; **(D)** is the torus breakdown; **(B)** is *existence* on `ℝ³/ℤ³`, not a breakdown statement at all |
| data "smooth" | **CONFIRMED** | (C), verbatim |
| data "divergence-free" | **CONFIRMED** | (C), verbatim |
| data "decaying faster than any polynomial" | **CONFIRMED AND STRENGTHENED** | (4) binds **every derivative** `∂ᵅ_x`, not the field alone. A compactly-supported cutoff supplies this trivially, so this clause is **not** the binding difficulty |
| "with `f ≡ 0`" | **REFUTED** | (C) permits "a smooth `f(x,t)` … satisfying (4),(5)". "Take `f(x,t)` to be identically zero" appears in **(A)** and **(B)** — the two *existence* statements — and in **neither** breakdown statement |
| "no smooth solution for all time with bounded energy" | **CONFIRMED** | (C) rules out solutions of (1),(2),(3),**(6)**,**(7)**, with (7) the bounded-energy condition verbatim, uniform in `t` with a single constant `C` |

**§4's premise — that the Clay statement requires bounded energy — is verified against the primary
text, as numbered condition (7).**

### 4.1 The refuted clause is a real relaxation, and it is NOT a shortcut

`(C)` permitting a forcing genuinely weakens the obligation: a breakdown candidate may carry an `f`,
provided it is smooth and satisfies (5). It does **not** follow that the cutoff residual can be
absorbed into `f` and §4 declared discharged. To do that one would *define* `f` as the residual of
the truncated field; but (C) requires `f` to be smooth on `ℝ³ × [0,∞)` and to satisfy (5) *while*
requiring that **no** smooth bounded-energy solution exists on `[0,∞)`. So `f` must be specified past
`T*`, where the candidate field does not exist, and cutting `f` off in time before `T*` removes
exactly the forcing that was making the field a solution. **The relaxation should be recorded; it
discharges nothing.**

### 4.2 One option named, with its cost, and no leg authorised by it

Statement **(D)** — breakdown on `ℝ³/ℤ³` — carries **no decay condition and no bounded-energy
condition**: its acceptance conditions are (10) periodicity and (11) smoothness only. A torus target
would make `CLAY_OBLIGATIONS` §4 **vacuous by construction**. This is recorded as an option with its
own cost, **not a recommendation**: the route-4 object is a DSS profile on `ℝ³` and is not periodic,
and re-targeting would re-open §2's rigidity screen from scratch — §2 being, per the obligations
document, "the programme's strongest position". **No leg is authorised by this note.** It is
integration's and the user's call whether it is worth a scoping question.

---

## 5. Ceiling, and what this is not

* **Tier 2.** Verifying an obligation is not a link of the `L1 → L4` chain. **Clay stays ~0.05 %.**
* The numerics are **float64 quadrature of a synthetic field**. Nothing here is interval-certified,
  and nothing here measures the *real* candidate's `α`. A synthetic field can confirm an identity and
  can refute one; it cannot certify the object's decay.
* The `α = 1` used throughout as "the banked value" is the **a-priori Type-I bound** (an upper bound
  on `|U|`, hence a *lower* bound on the decay rate), not a measurement of the candidate. If the real
  profile decays faster, every magnitude in §3 improves in the direction shown, and the thresholds in
  §2 say exactly how much faster it would have to be.

## 6. Routed to integration, verbatim

`CLAY_OBLIGATIONS.md` is integration's to amend; this leg edits no obligations file. The requested
edits:

1. **§4 is verified as a specification.** The `(T*−t)^{1/2}` survives an independent derivation for
   genuine DSS with the modulation handled; the DSS exponent equals the SS exponent exactly (ratio
   `1` to `1.2e-7`); the localisation problem is confirmed load-bearing; its inputs are named in §3
   above. The DRAFT-UNVERIFIED header may be updated **for §4 only** — §1, §2, §3, §5, §6, §7 were
   not verified by this leg.
2. **§4's derivation needs one repair.** Replace "`∫|u|²dx` at time `t` scales as
   `(T*−t)^{1/2}∫|U|²dy`, so bounded energy requires `U ∈ L²`" with the truncated law
   `E_ρ(t) ≍ ρ^{3−2α}(T*−t)^{α−1}`, because in the case of interest both sides of the original are
   `+∞`. **Conclusion unchanged; derivation now valid.**
3. **The target paragraph's "with `f ≡ 0`" is REFUTED** and should be struck: statement (C) permits a
   smooth forcing satisfying (4),(5). Add the note in §4.1 above so the relaxation is not misread as
   a shortcut.
4. **The labelling should read (C)**, not "direction (b)".
5. **Add, in §4, that (4) binds every derivative of the data**, and that a compactly-supported cutoff
   satisfies it trivially — so the decay-of-data clause is not the binding difficulty; bounded energy
   is.
6. **§7 was not checked** (the Millennium Prize rules: refereed journal, two-year wait, general
   acceptance). Its own text already says "check against the Clay Institute's own published rules
   before relying on it", and that instruction still stands — this leg read the *problem statement*,
   not the *prize rules*. Left to a successor.
