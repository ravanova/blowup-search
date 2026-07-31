# Route-D v7 — the domain seminorm part of ‖A‖, closed by a derivative gain

**Status: Level-1 tooling + upper bounds. NOT a certificate, NOT rigorous, NOT a
Clay result.** Plain float64 throughout: analytic estimates with numerically
evaluated constants, gated against independent measurements. Nothing here is
interval-enclosed.

**Figure:** `fig25` (`writeup/figures/fig25_route_d_v7_seminorm.png`)
**Data:** `writeup/data/p2_route_d_v7_seminorm.json`
**Code:** `solver/nk_seminorm.py` (+ `test_nk_seminorm.py`, 6/6),
`experiments/p2_route_d_v7_seminorm.py`,
`writeup/4_p2_lottery/p2_route_d_v7_evidence.py`

---

## 0. What this leg was for

v6 (`TECHNICAL_P2_ROUTED_V6.md`) moved three of eight Newton–Kantorovich constants
from MEASURED to BOUNDED and named three gaps, calling the first the sharpest:

> **the domain-SEMINORM part of ‖A‖.** The continuum argument says it is finite
> (the inverse gains a WHOLE derivative …); three computations all came back lossy
> at J^γ because they were still pricing B1's fake direction. Two candidate
> routes: (a) restrict to a BAND-LIMITED subspace where the discrete norm IS
> faithful, with a quantified faithfulness factor; (b) bound the seminorm through
> the C^{1,γ} gain analytically rather than by duality. **Do (a) first.**

This leg did **(b)**, because a ten-minute diagnostic (§1) showed (a) was aimed at
the wrong mechanism. That diagnostic is the leg's first result, and the general
lesson it carries is worth more than the specific one: *v6's own recommendation was
built on an analogy to v6's own headline finding, and the analogy was false.*

Notation is v5's throughout: `X = tan(θ/2)`, `w_β(θ) = (1+X²)^{β/2} = sec^β(θ/2)`,

```
‖h‖_{α,γ} = S + T ,   S = sup_θ w_α |h| ,
T = sup_{θ₁≠θ₂} min(w_{α−γ}(θ₁), w_{α−γ}(θ₂)) |h(θ₁)−h(θ₂)| / |θ₁−θ₂|^γ
```

with the seminorm weight `α−γ` forced by the conformal change of variables (v5
§2). The codomain `Y` is the same with `α → α+1`. The operator is the gauged
inverse `A = M⁻¹`, `M = [gauge row ; DF rows 1..]`, at the anchor `Ω = −1/(1+X²)`,
`c = 1/2` — the same object v5 and v6 measured.

---

## 1. V1 — where the J^γ actually lives

v6's bound on the seminorm part is

```
max_{j≠k}  p_jk ‖A_j· − A_k·‖_{Y*} ,      p_jk = min(w_{α−γ}) / |Δθ|^γ ,
```

with `‖·‖_{Y*}` the two-point dual. Compute exactly that, but restricted to pairs
with `|Δθ| ≥ Δ` for a **fixed** Δ (fixed in θ, so it covers more grid points as J
grows):

| pairs | J=125 | J=250 | J=500 | growth |
|---|---|---|---|---|
| all | 17.216 | 24.224 | 34.167 | **J^+0.494** |
| \|Δθ\| ≥ 0.02 | 17.216 | 12.621 | 13.323 | J^−0.185 |
| \|Δθ\| ≥ 0.05 | 9.085 | 9.560 | 9.779 | J^+0.053 |
| \|Δθ\| ≥ 0.1 | 6.948 | 7.078 | 7.122 | **J^+0.018** |

γ = 0.5, and the unrestricted exponent is 0.494. **All of the growth sits on the
near diagonal.** (The Δ = 0.02 row is non-monotone because at J = 125 the grid
spacing π/125 = 0.025 already exceeds 0.02, so the restriction is vacuous there —
the row is the crossover, not a trend.)

That disqualifies route (a) as a *fix*, and the reason is structural rather than
numerical. A faithfulness defect of the ball is a statement about which directions
are admissible; it does not know or care whether the two domain indices being
compared are adjacent. The J^γ does. So it is not that defect.

What it is: `‖A_j· − A_k·‖_{Y*}` was being bounded by pricing each row separately.
For adjacent `j, k` that discards the near-cancellation of neighbouring rows of an
inverse and then divides by `|Δθ|^γ ~ (π/J)^γ`. The growth is exactly that
division. **No refinement of the dual functional recovers a cancellation the dual
functional cannot see, because the cancellation is a property of the equation, not
of the rows.**

---

## 2. The derivative gain — the estimate itself

### 2.1 Solve for the derivative

At the anchor, `H(Ω) = −X/(1+X²)`, so `DF h = h H(Ω) + Ω H(h) − c h_X` reads

```
DF = −diag( X/(1+X²) ) − diag( 1/(1+X²) ) H − c d/dX          (gate 4: 1.9e-16)
```

and `DF h = g` rearranges **exactly** to

```
c h_X = −g − h X/(1+X²) − H(h)/(1+X²)                                     (P)
```

Define `P = sup_θ (1+X²)^{(α+1)/2} |h_X|`. Weighting (P):

* `g`-term: `(1+X²)^{(α+1)/2}|g| ≤ ‖g‖_Y` — the codomain sup weight, exactly;
* `h`-term: `X (1+X²)^{(α−1)/2}|h| ≤ S`, since `X(1+X²)^{−1/2} ≤ 1`;
* `H(h)`-term: `(1+X²)^{(α−1)/2}|H(h)|`, bounded in §2.3.

so

```
P ≤ (1/c) [ ‖g‖_Y + S + sup_X (1+X²)^{(α−1)/2} ( a_sup(X) S + a_semi(X) T ) ]   (D)
```

### 2.2 Size + derivative ⇒ smoothness, with the weights cancelling exactly

Take a pair `θ₁ < θ₂` (so `|X₁| < |X₂|`, and `min(w_{α−γ})` is at `θ₁`), and split
on the scale `δ(θ₁) = κ (1+X₁²)^{−1/2}` — a fixed multiple of the **local X-scale**,
expressed as a θ-length.

**Separated pairs** (`|Δθ| > δ`). Use the sup part at each point; `w_α` increases
in `|X|`, so `|h(θ₁)| + |h(θ₂)| ≤ 2S/w_α(θ₁)` and the pair contributes at most

```
2 S w_{α−γ}(θ₁) / ( w_α(θ₁) δ(θ₁)^γ ) = 2 S (1+X₁²)^{−γ/2} / δ^γ = 2 S κ^{−γ} .
```

**Near pairs** (`|Δθ| ≤ δ`). Use the derivative: `|Δh| ≤ |Δθ| max|h_θ|` with
`h_θ = (1+X²) h_X / 2`, so `|h_θ| ≤ w_{1−α} P / 2`, which for **α ≥ 1** is largest
at the smaller `|X|`, i.e. at `θ₁`. The pair contributes at most

```
(1/2) P w_{α−γ}(θ₁) w_{1−α}(θ₁) δ(θ₁)^{1−γ} = (1/2) P w_{1−γ}(θ₁) δ^{1−γ}
                                             = (1/2) P κ^{1−γ} .
```

Both halves are **scale-invariant** — the weights cancel identically at every
scale, which is the compactification doing the far-field bookkeeping for free, the
same free lunch v5 found for the seminorm itself. Hence, minimising over the free
parameter κ,

```
T ≤ min_κ [ (1/2) κ^{1−γ} P + 2 S κ^{−γ} ] = C(γ) (P/2)^γ (2S)^{1−γ} ,
C(γ) = (1−γ)^{γ−1} γ^{−γ} ,   C(1/2) = 2 ,   κ* = 4γS/((1−γ)P) .            (I)
```

There is **no J in (I)**, and no grid.

*Hypothesis:* α ≥ 1 (used once, for the monotonicity of `w_{1−α}`). Every α this
project uses lies in [1.1, 1.8]; `seminorm_closure` refuses α < 1 rather than
silently extending.

*Gate 2:* (I) verified directly on 32 profiles (smooth, oscillatory `cos kθ · f_α`
up to k = 80, localized bumps, square-wave partial sums) at four (α,γ) including
the endpoint α = 1: **worst measured ratio T/bound = 0.461**.

### 2.3 The split Hilbert bound — free sharpening

v6's `hilbert_farfield_bound` charges `|H(h)(X)|` to the **total** norm. Its
derivation already separates the two payers: on the p.v. band `[X/2, 3X/2]` the
increment of `h` is paid by the seminorm and the increment of the even kernel by
the decay envelope, and the rest of the line is paid by the envelope. Keeping them
apart costs nothing:

```
|H(h)(X)| ≤ a_sup(X) S + a_semi(X) T ,    a_sup + a_semi = v6's bound   (2.1e-16)
```

Weighted sups at the reference (α,γ) = (1.5, 0.5):
`sup_X (1+X²)^{(α−1)/2} a_sup = 1.031`, `… a_semi = 1.277`, against v6's combined
1.928. Worth **~30%** on the final closure (T ≤ 93.5 unsplit vs 63.6 split), and
up to **4.3× sharper pointwise** on elements whose norm is not evenly divided.

*Gate 1* also checks domination against measurements — and caught something worth
recording. v6's validation family included **raw nodal sign patterns** aligned with
a row of `H`. Those are not elements of the class: their interpolants do not decay
(that is v6's own B1), so the far-field envelope `|h(y)| ≤ S (1+y²)^{−α/2}` on which
every one of these bounds rests simply fails for them. v6's total-norm bound had
enough slack to absorb the violation; the sharper split does not. The gate
low-passes the aligned adversary to degree J/8, which keeps the alignment and puts
the element back in the space.

### 2.4 The closure, and why it never fails

(D) and (I) together read `T ≤ F(T)` with `F` concave, increasing, `F(0) > 0`.
`F(T) − T` is then concave and positive at 0, so it changes sign exactly once:
**there is exactly one fixed point `T*`, and `{T : T ≤ F(T)} = [0, T*]`.** Any a
priori finite `T` obeying the inequality therefore satisfies `T ≤ T*`.
`seminorm_closure` returns `T*` by monotone iteration from 0.

And `T*` always exists, for a reason worth stating: the feedback is **linear** in
`T` (it enters through `|H(h)|`) while the interpolation gain is **sublinear**,
`F ~ T^γ`. So for every γ < 1 the closure holds regardless of the size of the
constants — no smallness condition, no contraction to lose. Only γ = 1 (Lipschitz)
turns this into a genuine contraction condition. That is a **third independent
reason** γ = 1 is excluded, alongside v5 U2 (the Hölder–Hilbert constant blows up
at both ends) and the classical unboundedness of `H` on Lipschitz functions.

*Gate 5:* `T = F(T)` to 1e-9, local slope 0.445 < 1, monotone in `C_sup`, closes
for `C_sup` up to 5e3, and `F(2T)/F(T) = 1.414 = 2^γ` confirming sublinearity.

---

## 3. V3 — the number

`C_sup` is v6's two-point dual on the sup part (which saturates); everything else
is (I) + (D).

| J | C_sup (UB) | **T (UB, new)** | **‖A‖ (UB)** | v6 dual on T | family LB on T |
|---|---|---|---|---|---|
| 125 | 5.5360 | **63.613** | **69.149** | 17.216 | 0.8207 |
| 250 | 5.5313 | 63.560 | 69.091 | 24.224 | 0.8322 |
| 500 | 5.5282 | 63.525 | 69.053 | 34.167 | 0.8420 |
| 800 | 5.5543 | 63.822 | 69.376 | — | 0.8475 |
| 1600 | 5.6311 | 64.695 | 70.326 | — | 0.8540 |

`‖A‖_upper ~ J^{+0.0059}` — and the residual drift is inherited *entirely* from
`C_sup`; the closure contains no J at all. **This is the first uniform upper bound
on the whole of ‖A‖ in seven legs.**

Honest reading of the same table: the best lower bound available (the exact
seminorm extremizer directions, without an LP) is 0.85, so the bracket is

```
0.85  ≤  seminorm part of ‖A‖  ≤  63.6          (a factor ~75 wide)
```

The bound is real, uniform and analytic. It is **not sharp**, and §5 is about what
that costs.

---

## 4. V4 — the (α, γ) map, made of upper bounds

At J = 800, sweeping α ∈ [1.1, 1.8] and γ ∈ [0.05, 0.8] (deliberately past where
the answer was expected — banked lesson 8):

`‖A‖` upper bound:

| α \ γ | 0.05 | 0.1 | 0.15 | 0.25 | 0.35 | 0.5 | 0.65 | 0.8 |
|---|---|---|---|---|---|---|---|---|
| 1.2 | 15.0 | 18.5 | 22.2 | 31.2 | 43.0 | 69.4 | 115.6 | 213.3 |
| 1.4 | **14.0** | 17.2 | 20.8 | 29.5 | 41.3 | 68.8 | 122.2 | 265.0 |
| 1.6 | 19.3 | 23.4 | 27.9 | 38.7 | 53.3 | 88.2 | 160.5 | 401.7 |
| 1.8 | 34.7 | 42.2 | 50.4 | 70.3 | 97.8 | 165.9 | 324.0 | 979.7 |

`Z₂ = 2‖A‖C_Q` (the quantity the radii polynomial sees):

| α \ γ | 0.05 | 0.1 | 0.15 | 0.25 | 0.35 | 0.5 | 0.65 | 0.8 |
|---|---|---|---|---|---|---|---|---|
| 1.2 | 467.7 | 330.7 | 301.6 | 321.1 | 387.7 | 570.1 | 921.5 | 1698 |
| 1.4 | 379.7 | 267.0 | **242.4** | 255.0 | 308.5 | 462.7 | 788.7 | 1697 |
| 1.6 | 479.7 | 328.9 | 292.0 | 297.4 | 352.3 | 519.8 | 900.2 | 2219 |
| 1.8 | 803.3 | 547.1 | 487.4 | 497.8 | 587.7 | 876.5 | 1630 | 4857 |

**`‖A‖` alone falls monotonically as γ → 0** — a weaker domain norm is easier to
bound — so optimizing it alone would run straight off the edge of the grid (its
argmin is at γ = 0.05, the boundary). `Z₂` **bowls in both knobs**, with an
interior optimum at **(α, γ) = (1.4, 0.15), Z₂ ≤ 242.4**: the quadratic pays for
exactly the weakness that makes `‖A‖` cheap.

This is the **first interior optimum in this project computed entirely from upper
bounds**. v5's joint optimum was a maximum over test families (lower bounds) and
v6 killed it; this one is made of the right side of the inequality throughout.

Caveat that must travel with it: `Z₂` here still omits the **codomain seminorm part
of C_Q**, which is unbounded — and that omission is worst exactly where γ is
smallest. So the location (1.4, 0.15) is provisional in the same way v5's was, for
a different reason.

---

## 5. V5 — what the honest ‖A‖ costs

v6's conditional budget substituted the far-field inverse norm `2/(2−α) ≈ 2.5` for
`‖A‖`, justified by v4 W2 (the far-field law predicts the full gauged `‖A‖` **in
sup norms** to 6%). In the Hölder norm the real bound is 10–20× larger. At γ = 0.35,
requiring `Z₁ = ‖A‖ · (far-field modelling error) ≤ 0.5`:

| α | ‖A‖ UB | v6 proxy | ratio | X₀ needed | J implied | Y₀max (honest) | Y₀max (v6 proxy) |
|---|---|---|---|---|---|---|---|
| 1.1 | 44.27 | 2.22 | 19.9 | 2e3 | 1e3 | 1.12e-4 | 2.23e-3 |
| 1.2 | 43.03 | 2.50 | 17.2 | 2e3 | 1e3 | 1.61e-4 | 2.78e-3 |
| 1.3 | 42.03 | 2.86 | 14.7 | 3e3 | 2e3 | 1.83e-4 | 2.70e-3 |
| 1.4 | 41.29 | 3.33 | 12.4 | 6e3 | 4e3 | 2.02e-4 | 2.51e-3 |
| 1.5 | 42.74 | 4.00 | 10.7 | 3e4 | 2e4 | 2.09e-4 | 2.23e-3 |

Two readings, both true:

**Survivable.** The matching radius the honest `‖A‖` forces — `X₀ ~ 2e3–6e3` for
α ≤ 1.4, implying `J ~ πX₀/4 ~ 1e3–4e3` — is *inside* what the existing dense
collocation reaches. (α = 1.5 wants 3e4, i.e. J ~ 2e4, which is not: dense J×J at
2e4 is 3.2e9 entries.) So the honest bound does not, by itself, put the far-field
split out of computational reach.

**Expensive.** The conditional budget drops an order of magnitude, from 2.8e-3 to
2.0e-4 — from the same order as the GA residual floor (~1e-2) to a factor ~50
below it. And this is the **second consecutive leg** in which replacing a lower
bound by an upper bound cost the budget an order of magnitude (v6 B5 did the same
to v5's optimum when Z₁ was first priced).

That pattern is the leg's most important negative: **the approach does not merely
need the constants bounded, it needs them roughly sharp.** Three of the four we
have bounded are lossy by an order of magnitude or more, and the losses multiply
inside `Z₂` and `Z₁`.

---

## 6. V6 — the interpolant is not in the space

Checking the chain surfaced a defect older than this leg.

A nodal vector on the midpoint grid stands for an even **trigonometric polynomial**
in θ. A trigonometric polynomial does not vanish at θ = π. The decay weight
`w_α(θ) = sec^α(θ/2)` diverges there. Therefore

> **`sup_θ w_α |h|` is INFINITE for the interpolant, at every J.**

Every discrete norm in Route-D v1…v7 is finite only because the midpoint grid stops
half a step short of π. Measured on `h = A e_{J/2}`:

| J | h(π) | w\|h\| at the last node | w\|h\| at θ = π − 1e-6 |
|---|---|---|---|
| 200 | 3.85e-7 | 8.40e-3 | 1.09e+3 |
| 400 | 4.75e-8 | 3.60e-3 | 1.34e+2 |
| 800 | 5.90e-9 | 1.49e-3 | 1.67e+1 |
| 1600 | 7.35e-10 | 6.04e-4 | 2.08e+0 |

`h(π) ~ J^{−3.01}`: the failure is **soft**, and the discretization is converging to
something that does live in the space. But it is not a small correction — it is a
change of representation. The repair is explicit:

> write `h = (1+X²)^{−α/2} p(θ)` with `p` a trigonometric polynomial, so that the
> weighted sup norm becomes the plain sup norm of `p` and the weighted seminorm a
> mildly weighted θ-seminorm of `p`.

Note the derivative-gain closure of §2 is **immune**: it is a continuum statement
about the true solution of `DF h = g`, which does decay. The defect is in the
*hypothesis* `S ≤ C_sup`, which is currently supported by grid measurements.

---

## 7. Ledger after v7

| constant | status | note |
|---|---|---|
| Y₀ (at the a=0 anchor) | **EXACT** | the anchor is an exact zero |
| Z₀ | **BOUNDED** | finite-block rounding (~1e-11) |
| Z₁ far-field modelling error | **BOUNDED** (v6) | closed form, `X₀^{α−2}` |
| Z₁ core↔far-field coupling | OPEN | smooth cutoff + `[H, φ]` commutator |
| Z₁ core discretization | MEASURED ONLY | v4 W6: `J^{−2.1..−2.6}` |
| ‖A‖ domain SUP part | **BOUNDED** (v6) | two-point dual, uniform in J |
| **‖A‖ domain SEMINORM part** | **BOUNDED (NEW)** | derivative-gain closure, J-free |
| C_Q sup part | **BOUNDED** (v6) | same `|H(h)|` bound |
| C_Q codomain SEMINORM part | OPEN | needs weighted Hölder boundedness of `H` |
| discrete ↔ continuum transfer | **OPEN (NEW)** | §6: a change of ansatz |

Six of ten bounded. Two of the four open items are new names for things that were
previously invisible rather than new problems.

---

## 8. Reproduce

```
.venv/bin/python test_nk_seminorm.py                          # 6/6, ~3 min
.venv/bin/python experiments/p2_route_d_v7_seminorm.py        # ~15 min -> JSON
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v7_evidence.py   # fig25 from JSON
```

Deterministic: no GA, no seeds, no predicate lock (the project's logged-run
discipline applies to stochastic Tier-1/2 runs; this is a tooling probe, entered in
`experiments/JOURNAL.md` as a clearly-labelled non-logged entry).

---

## 9. Honest ceiling

v7 bounds one more constant and re-prices the budget with it. It does **not** climb
the rigor ladder: everything is float64, nothing is interval-enclosed, and there is
still no certificate. The eventual success this line scouts is a computer-assisted
**toy-model** certification (Chen–Hou / Gómez-Serrano genre), not a Clay solve; 1D
HL is a toy model of the boundary behaviour of Hou–Luo / 3D axisymmetric Euler.
Overall Clay odds remain ~0.05%. The honest best case for the whole Route-D leg is
still "certifies the a = 0 traveling wave", which is already known in closed form.
