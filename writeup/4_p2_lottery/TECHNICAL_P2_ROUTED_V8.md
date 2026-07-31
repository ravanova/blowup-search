# Route-D v8 — the codomain seminorm part of `C_Q`, and the first complete `Z₂`

**Status: Level-1 tooling + upper bounds. NOT a certificate, NOT rigorous, NOT a
Clay result.** Plain float64: analytic majorants with numerically evaluated
constants, gated against an exact second build and against measurements. Nothing
here is interval-enclosed.

**Figure:** `fig26` (`writeup/figures/fig26_route_d_v8_quadratic.png`)
**Data:** `writeup/data/p2_route_d_v8_quadratic.json`
**Code:** `solver/hilbert_holder.py` (+ `test_nk_hilbert_holder.py`, 6/6),
`experiments/p2_route_d_v8_quadratic.py`,
`writeup/4_p2_lottery/p2_route_d_v8_evidence.py`

---

## 0. What this leg was for

v7 closed the domain seminorm part of `‖A‖` and produced the project's first
`(α, γ)` map made entirely of upper bounds — with one term still missing, and it
said so:

> Caveat that must travel with it: `Z₂` here still omits the codomain SEMINORM
> part of `C_Q`, which is unbounded — and that omission is worst exactly where γ
> is smallest. So the location (1.4, 0.15) is provisional.

This leg bounds that term. The headline is not the bound: it is that after
**three consecutive legs in which replacing a lower bound by the honest upper
bound cost the conditional budget an order of magnitude**, this one costs **7%**
— and v7's provisional optimum survives unmoved, for a reason v7 got backwards.

Notation is v5's: `X = tan(θ/2)`, `w_β = sec^β(θ/2) = (1+X²)^{β/2}`, domain
`‖h‖_{α,γ} = S + T` with `S = sup w_α|h|` and `T` the `w_{α−γ}`-weighted θ-Hölder
seminorm; codomain the same with `α → α+1`. All pairs live in `θ ∈ (0, π)`,
because `h` is even and that is where the project's norms are defined
(`solver/decay_collocation.grid`).

---

## 1. What actually has to be bounded — and with which weight

With `Q(h) = h·H(h)` and `ψ = H(h)`, expand the product's increment about the
**inner** point of the pair (`θ_i` = the one with smaller `|θ|`, where `min(w)`
sits):

```
w_{α+1−γ}(θ_i) |Q(θ₁) − Q(θ₂)| / d^γ
    ≤ S · { w_{1−γ}(θ_i) |Δψ| / d^γ }   +   T · w_1(θ_i) B(θ_o)
```

using `|h| ≤ S/w_α` and `|Δh| ≤ T d^γ / w_{α−γ}`. Two things fall out and both
matter:

* **The second term needs no new work.** `w` increases in `|θ|`, so
  `w_1(θ_i) ≤ w_1(θ_o)` and `w_1(θ_i) B(θ_o) ≤ sup_θ w_1 B` — which is exactly
  v6's `C_Q` sup-part quantity.
* **The first term needs the weighted Hölder seminorm of `ψ` with weight
  `1 − γ`, not `α − γ`.** `H` does not inherit `h`'s decay: for even `h` with
  nonzero mass, `H(h)(X) → (∫h)/(πX)` however fast `h` decays, so `ψ`'s decay
  grading is **1** and its seminorm weight is `1 − γ` by the same rule that gave
  the domain `α − γ`. Asking for `α − γ` here would be asking for something
  false — and would have produced an infinite constant with no explanation.

So the object of the leg is

```
T_ψ = sup_{θ₁≠θ₂} min(w_{1−γ}) |ψ(θ₁) − ψ(θ₂)| / |Δθ|^γ  ≤  b_sup S + b_semi T .
```

---

## 2. The estimate

Work relative to `θ₁`: put `φ = θ₁ + t`, `θ₂ = θ₁ + σ`, `d = |σ|`. **In `t`
nothing wraps**, which is the whole reason for the change of variable: in
absolute `θ` the pair (`θ` near `π`, `φ` near `−π`) is a pair of *neighbours* on
the circle, so a near region defined as an interval of the line would leave a
kernel singularity sitting in the "far" region.

Using `p.v.∫cot = 0` on the circle, `ψ(θ) = (1/2π) p.v.∫[h(φ) − h(θ)]
cot((θ−φ)/2) dφ`, and with `N = [min(0,σ) − p·d, max(0,σ) + p·d]`:

```
ψ(θ₁) − ψ(θ₂) = (1/2π) [ E_N + E_F + G ]
E_N = ∫_N [h−h(θ₁)] cot(−t/2) dt − ∫_N [h−h(θ₂)] cot((σ−t)/2) dt
E_F = ∫_F [h−h(θ₁)] [cot(−t/2) − cot((σ−t)/2)] dt
G   = [h(θ₂) − h(θ₁)] ∫_F cot((σ−t)/2) dt
```

Each piece gets an explicit majorant:

* increments of `h` by whichever norm part is cheaper **at that point**,
  `|h(φ) − h(ref)| ≤ min( T |Δ|^γ cos^{α−γ}(θ_near/2), S[cos^α(φ/2) +
  cos^α(ref/2)] )` with **folded** distances `Δ = ||φ| − |ref||` (the norm lives
  on `(0,π)` and `h` is even, so a pair straddling `θ = 0` has increment zero and
  the seminorm knows it). The choice is made by a rule depending only on
  `(φ, ref, α, γ)`, never on `S` or `T` — which is what keeps the result a
  genuine **linear** bound in `(S, T)` rather than a concave envelope;
* the kernels **exactly**, with the far difference in the stable form
  `cot(t/2) + cot((σ−t)/2) = sin(σ/2)/(sin(t/2) sin((σ−t)/2))`, which preserves
  the `O(d)` cancellation that makes `E_F` small;
* `G` in closed form: `∫_F cot((σ−t)/2) dt = −p.v.∫_N = 2 log|sin((σ−n₁)/2) /
  sin((σ−n₂)/2)| → 2 log(3/2)` for `p = 2`.

**The padding is a parameter, not a constant, and that mattered.** The
decomposition only needs `N` to cover the circle at most once, i.e.
`(1+p)d ≤ π`. A first draft restricted the estimate to `d ≤ (π−θ_i)/6` — which is
what the *scaling argument* needs — and the sweep then returned a constant a
factor **12 too large**, entirely from pairs just outside that cutoff where the
crude pointwise route had to take over. Shrinking `p` for wide pairs instead of
abandoning the estimate fixed it. *Do not let the regime of an argument become
the regime of the code.*

For pairs too wide even for that (`d > 2.6`), and only those, the **pointwise**
route is used: `|Δψ| ≤ |ψ(θ₁)| + |ψ(θ₂)|` with v7's split pointwise bound.

---

## 3. X1 — the estimate, its convergences, and what it is worth

At the reference `(α, γ) = (1.5, 0.5)`:

```
T_ψ  ≤  1.1936 · S  +  4.9410 · T
```

| pairs swept | `b_sup` | `b_semi` |
|---|---|---|
| 24×14 | 1.19318 | 4.940975 |
| 40×22 | 1.19356 | 4.940974 |
| 64×34 | 1.19368 | 4.940952 |
| 96×52 | **1.19369** | **4.940973** |

Flat to `4e-6` over a 4× refinement in each direction, and the per-pair
quadrature is flat to `4e-4` over 150 → 2400 points. **This refinement is a gate,
not a nicety**: the pair supremum is a *grid* supremum, which can only
UNDER-report — the mirror image of v6's discrete-ball trap, where a set that was
too big over-reported.

**Gate: the decomposition, built twice.** A majorant of a *wrong* decomposition
is still an inequality about something, and no domination test would notice. So
`E_N + E_F + G` is evaluated a second time with the **true** increments and
compared against the exact conjugate (`cos kθ → sin kθ`): agreement to
**5.6e-6** (quadrature-limited) over 7 pairs × 3 profiles. It caught two sign
errors, one of them in a kernel identity that was also wrong in the module
docstring.

**Ablation: the estimate is the result.** With only the pointwise route — all
v6 and v7 had for this quantity — the same sweep returns `b_sup + b_semi =
1452` instead of `6.13`: **237× worse**. And the per-pair *rule* matters: taking
whichever route has the smaller coefficient **sum** inflates `b_sup` from 1.19 to
2.61, because at a near-tie it trades a large `u_sup` for a marginal gain in the
sum. The route choice must be a single rule applied to both coefficients; mixing
"the route that minimizes `b_sup`" with "the route that minimizes `b_semi`" is
not itself a bound.

---

## 4. X2 — the bracket

Measured against the family (anchor shape, `cos kθ · f_α` up to `k = 256`,
square-wave partial sums, core and far-field bumps) at four `(α, γ)`:

| (α, γ) | worst measured / bound | worst profile |
|---|---|---|
| (1.5, 0.50) | 0.239 | `bump_core` |
| (1.2, 0.25) | 0.227 | `f_alpha` |
| (1.4, 0.35) | 0.222 | `f_alpha` |
| (1.4, 0.65) | 0.246 | `bump_core` |

Valid everywhere, and **~4× lossy** on the directions the family contains. Same
order of slack as v7's closure. Per v7's own conclusion — the constants must be
roughly *sharp*, not merely bounded — that slack is now the main quantity of
interest, not the bound.

---

## 5. X3 — the γ structure, and where v7's prediction went wrong

Both endpoint divergences are present and visible: `b_semi` = 18.6 at γ=0.05
(near region, `∫|t|^{γ−1} ~ 1/γ`), falling to 4.94 at γ=0.5, rising again to
7.16 at γ=0.9 (far region, `∫d|t|^{γ−2} ~ 1/(1−γ)`). So the complete `C_Q` bowls,
with an interior minimum **3.330 at γ = 0.65**.

But v7 predicted the *omission* would be worst where γ is smallest, and it is
the **opposite**:

| γ | 0.05 | 0.15 | 0.35 | 0.5 | 0.65 | 0.9 |
|---|---|---|---|---|---|---|
| `C_Q` complete | 12.98 | 5.96 | 3.80 | 3.43 | 3.33 | 3.82 |
| `C_Q` sup-only (v6/v7) | 12.96 | 5.51 | 3.50 | 3.13 | 2.99 | 2.99 |
| ratio | **1.001** | 1.082 | 1.086 | 1.094 | 1.112 | **1.276** |

The reason is simple once seen: **v6's sup-only `C_Q` already carried the same
`1/γ` near-region divergence**, through the seminorm-paid half of its own
`|H(h)|` bound. Nothing *new* blows up at small γ. The ratio is flat there and
grows toward the Lipschitz end instead.

---

## 6. X4 — the first complete `Z₂` map

`Z₂ = 2‖A‖C_Q` at `J = 800`, with `‖A‖` = v6's sup-part dual + v7's closure and
`C_Q` = v6's sup part (split by payer) + this leg's seminorm part. **Every
constant is an upper bound and nothing is omitted — the first `Z₂` in this
project of which that is true.**

| α \ γ | 0.05 | 0.1 | 0.15 | 0.25 | 0.35 | 0.5 | 0.65 | 0.8 |
|---|---|---|---|---|---|---|---|---|
| 1.2 | 456 | 350 | 337 | 392 | 512 | 795 | 1276 | 2294 |
| 1.4 | 378 | 282 | **261** | 279 | 341 | 518 | 894 | 2001 |
| 1.6 | 484 | 354 | 319 | 325 | 382 | 566 | 1003 | 2638 |
| 1.8 | 826 | 605 | 544 | 550 | 645 | 973 | 1850 | 5901 |

**Optimum: (α, γ) = (1.4, 0.15), `Z₂ ≤ 261.1`** — the same location v7's
incomplete map reported (`Z₂ ≤ 242.4`), 7.7% higher. v7 called that location
provisional *because of this omission*; the omission is now priced and the
location holds.

---

## 7. X5 — the budget, and the trend that does not continue

At the optimum, requiring `Z₁ ≤ 0.5` from the far-field modelling error:
`X₀ = 3.2e3`, implying `J ~ 2.5e3` and a `6.2e6`-entry dense core — inside what
the existing collocation reaches.

| leg | `Y₀^max` | what changed |
|---|---|---|
| v5 | 7.6e-2 | family-restricted maxima (LOWER bounds) throughout; `Z₁` unpriced |
| v6 | 1.18e-2 | `Z₁` far-field priced for the first time |
| v7 | 2.58e-4 | the honest `‖A‖` (sup part + seminorm closure) |
| **v8** | **2.39e-4** | `C_Q` complete; every constant in `Z₂` an upper bound |

(v7's own writeup quoted 2.0e-4, its value at the single row γ = 0.35; 2.58e-4 is
v7's map priced over the same sweep as v8, which is the like-for-like number.)

**Three order-of-magnitude losses, then one of 7%.** The pattern v7 flagged as
its most important negative — *every time a lower bound is replaced by an upper
bound, the budget loses an order* — **does not continue through this leg.** Two
reasons, both stated above: the old term already carried the new one's worst
divergence, and v7's split-by-payer sharpening of `|H(h)|` recovers most of what
the new term costs.

That is a real update on the lane question, in the *good* direction, and it is
worth being precise about how much: it does not make the budget large (2.4e-4 is
still ~40× below the GA residual floor), it removes one specific reason to expect
the remaining three ledger items to be catastrophic.

---

## 8. X6 — ledger after v8

| constant | status | note |
|---|---|---|
| Y₀ (at the a=0 anchor) | **EXACT** | the anchor is an exact zero |
| Z₀ | **BOUNDED** | finite-block rounding (~1e-11) |
| Z₁ far-field modelling error | **BOUNDED** (v6) | closed form, `X₀^{α−2}` |
| Z₁ core↔far-field coupling | OPEN | smooth cutoff + `[H, φ]` commutator |
| Z₁ core discretization | MEASURED ONLY | v4 W6: `J^{−2.1..−2.6}` |
| ‖A‖ domain SUP part | **BOUNDED** (v6) | two-point dual, uniform in J |
| ‖A‖ domain SEMINORM part | **BOUNDED** (v7) | derivative-gain closure, J-free |
| C_Q sup part | **BOUNDED** (v6, sharpened v7/v8) | split by payer |
| **C_Q codomain SEMINORM part** | **BOUNDED (NEW)** | weight `1−γ`; grid-swept majorant |
| discrete ↔ continuum transfer | OPEN (v7) | a change of ansatz |

**Seven of ten bounded.** The three that remain are all `Z₁`-side or
representational; `Z₂` is complete.

---

## 9. Reproduce

```
.venv/bin/python test_nk_hilbert_holder.py                        # 6/6, ~4 min
.venv/bin/python experiments/p2_route_d_v8_quadratic.py           # ~12 min -> JSON
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v8_evidence.py   # fig26 from JSON
```

Deterministic: no GA, no seeds, no predicate lock (the logged-run discipline
applies to stochastic Tier-1/2 runs; this is a tooling probe, entered in
`experiments/JOURNAL.md` as a clearly-labelled non-logged entry).

---

## 10. Honest ceiling

v8 bounds the last unpriced constant in `Z₂` and re-prices the budget with it. It
does **not** climb the rigor ladder: everything is float64, nothing is
interval-enclosed, and there is still no certificate — three ledger items remain
open, all on the `Z₁` side, and the bound itself is ~4× lossy. The eventual
success this line scouts is a computer-assisted **toy-model** certification
(Chen–Hou / Gómez-Serrano genre), not a Clay solve; 1D HL is a toy model of the
boundary behaviour of Hou–Luo / 3D axisymmetric Euler. Overall Clay odds remain
~0.05%. The honest best case for the whole Route-D leg is still "certifies the
a = 0 traveling wave", which is already known in closed form.
