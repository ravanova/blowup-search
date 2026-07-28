# Phase-2 P2 — Route D v2: the float dress rehearsal, and why the naive Newton–Kantorovich does not close

**Status: Level-1 *tooling* + a **structural negative** with a constructive
repair — NOT a certificate.** This is the brick
[TECHNICAL_P2_ROUTED.md](TECHNICAL_P2_ROUTED.md) §8 named as next: compute the
radii-polynomial bounds `Y₀, Z₀, Z₁, Z₂` for the gCLM two-scale traveling wave at
the exact `a=0` anchor, in plain floating point, across a truncation ladder, and
see whether the certification ball closes *before* spending effort on interval
hardening.

**It does not close — and the measurements say it cannot, at any truncation,
under any gauge, and with no positive weight able to repair it.** The obstruction
is located precisely and confirmed causally: the transport term
`c (1 + cos θ) ∂_θ` **degenerates at `θ = ±π`**, i.e. at `X = ∞`. The same
measurements then specify the fix: the linearized inverse loses **exactly one
power of spatial decay**, and becomes *uniformly bounded* the moment the codomain
is graded by that one power. Clay odds unchanged (~0.05%).

Rebuild the figure from committed data (no re-derivation):
`python writeup/4_p2_lottery/p2_route_d_dress_evidence.py` →
`writeup/figures/fig20_p2_route_d_dress.png` (reads
`writeup/data/p2_route_d_dress.json`; regenerate the data — deterministic, a few
seconds — with `python experiments/p2_route_d_dress.py`).

Code: `solver/nk_fourier.py` (the exact Fourier-basis operator) +
`test_nk_fourier.py` (6/6). Full suite now **9 files green**.

---

## 0. What was being tested, and why it is worth reporting

Route-D v1 established the framing: gauge the two scaling symmetries, work in the
compactified Fourier basis where the line Hilbert transform becomes the circular
conjugate, and exploit that the linearization `DF` is tridiagonal. It ended with
one gating question — *do the radii-polynomial bounds close?* — and the honest
warning that they might not.

A negative here is not a wasted brick. "The certification ball does not close, and
here is exactly which structural feature blocks it, confirmed by a controlled
ablation, together with the space in which it *would* close" is a more useful
statement than a certificate of a solution that was already known in closed form.
The a=0 anchor `Ω₂ = −1/(1+X²)` is an exact traveling wave; certifying it proves
nothing new. Its value was always as a **rehearsal**: the machinery you build
there is the machinery you would carry to `a ≠ 0`, where the answer is unknown.
This leg reports what the rehearsal found.

## 1. The exact Fourier operator (`solver/nk_fourier.py`)

Route-D v1 verified the change of variable numerically (~10⁻⁷ on endpoint-vanishing
combinations). It is in fact exact and unconditional. With `X = tan(θ/2)`,

    e^{iθ} = (1 + iX)/(1 − iX)

is holomorphic in the upper half `X`-plane (its only pole is `X = −i`) and tends
to `−1` at infinity, so `G_k := e^{ikθ} − (−1)^k` lies in the Hardy space and
decays; `H(Re G) = Im G` then gives, **for every `k ≥ 0`, with no decay
assumption**,

    H(cos kθ) = sin kθ,        H(1) = 0.                                   (H)
    f_X = (1 + cos θ) f_θ.                                                 (D)

So for `Ω = Σ_{k≥0} a_k cos kθ` the residual `F(Ω,c) = Ω H(Ω) − c Ω_X` is odd and
its sine coefficients are closed-form polynomials in `a`:

    Ω H(Ω)   = ½ Σ_{k≥0} Σ_{j≥1} a_k a_j [ sin((j+k)θ) + sin((j−k)θ) ]
    −c Ω_X   = c Σ_{k≥1} k a_k [ sin kθ + ½ sin((k+1)θ) + ½ sin((k−1)θ) ]

with `sin(−m) = −sin m` folded and `sin 0 = 0` dropped. No grid, no quadrature.
The anchor is `a = (−½, −½, 0, …)`, `c = ½`, and the two terms cancel **exactly**
(`sinθ/4 + sin2θ/8` each): `residual` returns identically zero at every truncation
— a much sharper gate than the grid's `10⁻⁹`.

**Validation** (`test_nk_fourier.py`, 6/6) uses three independent oracles: the
exact anchor; central finite differences of the residual (Jacobian agrees to
1.4×10⁻¹⁰); and the banked **grid** residual on the sinh grid with the dense
line-Hilbert matrix (agrees to 1.6×10⁻⁴ relative, discretization-limited). The
two exact symmetry tangents are annihilated to `0.0`.

> **A bug this caught.** The v1 probe's closed-form band had an unfolded
> `sin(−θ)` in its `k = 0` column (`−1/4` instead of `−1/2`); its grid
> cross-check only ran `k ≥ 1`, so it never exercised the folding case. Fixed in
> `experiments/p2_route_d_probe.py`; the two independently-written closed forms
> now agree to `0.0`, and the reported grid cross-check (3.9×10⁻²) is unchanged,
> since that residual is the `θ = ±π` endpoint correction, not this entry.

## 2. The gauged square system

Following v1 §Q2: fix the speed `c = ½` and impose one scalar normalization.
Unknowns `a_0 … a_N` (`N+1`); equations = the normalization row plus sine modes
`1 … N`. The two exact kernel directions of the un-gauged `[DF | ∂F/∂c]` are the
scaling-valley tangents, now available in closed form by differentiating
`A/(1+BX²)` (speed `−A/(2√B)`) at `(A,B) = (−1,1)`:

| symmetry | profile direction | `δc` |
|---|---|---|
| amplitude | `(½, ½, 0, …)` = `(1+cosθ)/2` | `−½` |
| dilation | `(⅛, 0, −⅛, 0, …)` = `sin²θ/4` | `−¼` |

With `c` fixed the surviving kernel is the combination with zero `δc`, which is
`w = −¼ cos θ (1 + cos θ) = (−⅛, −¼, −⅛, 0, …)`. All three normalizations tested
(`Σa_k = −1`, `a_0 = −½`, `a_1 = −½`) are non-degenerate on `w`, so each isolates
the zero. This is the analytic version of v1's singular-value count.

## 3. D1 — the ladder: the inverse is unbounded (fig20-A)

| `N` | `σ_min` | cond | `‖A_N‖_{ℓ¹}` | `Z₀` | `Z₁` | `Y₀^max` | closes |
|---|---|---|---|---|---|---|---|
| 4 | 2.6×10⁻¹ | 1.1×10¹ | 5.00 | 1.0×10⁻¹⁵ | 5.99 | 0 | no |
| 16 | 8.8×10⁻² | 1.4×10² | 14.00 | 1.3×10⁻¹⁴ | 18.00 | 0 | no |
| 64 | 2.4×10⁻² | 2.4×10³ | 50.89 | 7.4×10⁻¹³ | 66.00 | 0 | no |
| 256 | 6.1×10⁻³ | 4.0×10⁴ | 198.69 | 2.9×10⁻¹¹ | 258.00 | 0 | no |

Fitted over the upper half of the ladder:

    ‖A_N‖_{ℓ¹} ~ N^0.97,   σ_min ~ N^−0.98,   cond ~ N^2.03.

The norm of the finite-section inverse **grows linearly with the truncation**. In
the unweighted Fourier (Wiener `ℓ¹`) space the linearized operator is therefore
not boundedly invertible, and *no* truncation can certify: `Z₂ = 2‖A‖` diverges
while the contraction budget `1 − Z₀ − Z₁` is already negative.

`Y₀` itself is `0.0` at every `N` — the anchor is an exact zero and a degree-1
trig polynomial, so both the finite defect and the convolution tail vanish
identically. The informative quantity is therefore the **certification budget**

    Y₀^max = (1 − Z₀ − Z₁)² / (4 Z₂),

the largest defect these bounds could tolerate. It is **identically zero at every
`N`**. For comparison, the residual floor of the best GA profile at `a ≈ 0.5`
(the boundary this programme actually cares about) is `~10⁻²`
([TECHNICAL_P2_KLADDER.md](TECHNICAL_P2_KLADDER.md)). There is no gap to close;
there is no budget at all.

## 4. D3 — the gauge is exonerated

Sub-task **G** (v1 §7) was flagged as "the crux": get the gauge/Fredholm
bookkeeping wrong and `Z₀` is meaningless. All three normalizations give
`‖A_N‖ ~ N^0.97` — the three ladders lie on top of each other (fig20-A, open
markers). **G is not what blocks closure.** It still has to be got right for a
working certificate, but it is no longer a suspect for this failure.

## 5. D4 — causal isolation: it is the far-field degeneracy (fig20-B)

The suspect was sub-task **R**, the `θ = ±π` (Cayley) endpoint. Test it by
ablation: rebuild the identical ladder with the transport factor `(1 + cos θ)`
replaced by `1` — so the transport term is `−c h_θ` instead of `−c (1+cos θ) h_θ`
— and change nothing else (both Hilbert/product terms untouched). This surrogate
is not a physical operator; it removes exactly one feature.

    true operator:       ‖A_N‖_{ℓ¹} ~ N^0.97,  reaching 198.7 at N = 256
    surrogate:           ‖A_N‖_{ℓ¹} ~ N^0.00,  FLAT at exactly 4.0

The growth vanishes completely. The vanishing of the transport symbol at
`θ = ±π` is not a suspect but **the cause**. Sub-task **R** is promoted from
footnote to blocker.

## 6. D2/D5 — why the far field is exactly marginal, and why no weight fixes it (fig20-C)

Two independent mechanisms both fail, and both fail *at exactly the boundary*.

**(a) Truncation coupling.** Column `N+1` of `DF` feeds row `N` with the
sub-diagonal weight `c(N+1)/2`. Propagating it through `A_N` gives, exactly,

    Z₁ ≥ ‖A_N (A† − DF)‖ ≥ N + 1                (measured: 5, 17, 65, 257 at N = 4, 16, 64, 256)

— the finite section is coupled to the modes it discards *more* strongly the
larger it gets. Bigger `N` is strictly worse. Even the fiction in which the far
field is ignored entirely does not close at any `N`.

**(b) Far-field column weight.** The far-field columns of `DF` are exactly
tridiagonal, `(sub, diag, sup) = (ck/2, ck − ½, ck/2 − ½)`. With the standard
diagonal tail model `A_tail = diag(1/Λ_m)`, the discarded off-diagonal
contributes a `Z₁` column weight `z(k)`. Two natural choices of `Λ` bracket it:

| `k` | `Λ_m = c m` | `Λ_m = c m − ½` (true diagonal) |
|---|---|---|
| 10 | 0.91919 | 1.02500 |
| 100 | 0.99020 | 1.00020 |
| 3000 | 0.99967 | 1.00000 |

**Both tend to 1, from opposite sides, at rate `O(1/k)`, independent of `c`.** So
`sup_{k>N} z(k) = 1` for every `N`: the marginality is not an artifact of the tail
model. The reason is structural — the transport term is multiplication by the
symbol `1 + cos φ`, whose `ℓ¹` norm is `2`, exactly twice its own mean, *because
it vanishes at `φ = π`*.

**No weight repairs it.** In a weighted `ℓ¹` with domain weight `w`, the column
weight becomes `z_w(k) ≈ (u_{k−1} + u_{k+1}) / (2 u_k)` with `u_k := w_k / k`.
Demanding `z_w ≤ 1 − δ` for all large `k` forces
`u_{k+1} ≤ 2(1−δ) u_k − u_{k−1}`, whose characteristic roots
`(1−δ) ± i√(1−(1−δ)²)` lie **on the unit circle** with argument `arccos(1−δ) > 0`;
every solution oscillates, so any positive sequence obeying it changes sign in
finitely many steps. **No positive weight achieves a uniform `Z₁ < 1`.** The best
possible is `u` affine (`w_k = k(α + βk)`), which gives `z_w ≡ 1` exactly. The
numerics agree: over `k ∈ [5, 2000]`, `w = k^0.5 → 1.0155`, `w = 1.05^k → 1.0327`,
`w = k → 1.000000`, `w = k(1+k) → 1.000000`, `w = k^1.5 → 0.99999997` — the last
one dips below only because the window is finite; the theory says its supremum
over all `k` is exactly `1`, so no fixed margin `δ > 0` exists.

Sharpening the tail model beyond a diagonal does not escape this: taking
`A_tail` to be the exact far-field inverse zeroes that `Z₁` block but moves the
divergence into `‖A‖`, which §3 already measures as unbounded. It is one fact
wearing two hats.

## 7. D6 — the repair: the inverse loses exactly one power of decay (fig20-D)

The far field of the linearization is, at large `X`
(`H(Ω₂) ~ −1/X`, `Ω₂ ~ −1/X²`):

    DF[h] ≈ −c h_X − h/X = g.

With `c = ½` the integrating factor is `X²`, so `(X² h)' = −2X² g` and

    h(X) = 2 X^{−2} ∫_X^∞ s² g(s) ds.

For oscillatory `g` of unit amplitude this gives `h ~ X`: **the inverse amplifies
by one power of `X`, i.e. it loses one power of decay.** Under `X = tan(θ/2)` a
Fourier mode `m` resolves the scale `X ~ m`, so the prediction is
`‖A e_m‖_{ℓ¹} ∝ m`. Measured at `N = 256`:

    ||A e_m||_1  =  1.97 m       (fit on the interior window m <= N/8)

— slope `2` to within 2%. (The profile rolls over as `m → N`; that is the
finite-section edge, where `‖A e_N‖_{ℓ¹} = 4` exactly at every `N`, not the
asymptotics.) The `N^0.97` growth of `‖A_N‖` in §3 is the same fact: the worst
column is the largest available mode.

So the operator *is* invertible — just not from a space to itself. Grade the
codomain by one mode power (`v_m = m` on sine mode `m`, `1` on the gauge row) and
re-measure:

| pairing | `‖A‖` at `N = 256` | growth |
|---|---|---|
| **graded codomain → plain `ℓ¹` domain** | **3.0000** | **`N^0.00` — flat** |
| plain `ℓ¹` codomain → graded domain | 1.98×10⁴ | `N^1.94` |
| graded → graded | 130.0 | `N^0.95` |

`‖A‖ = 3.000`, constant from `N = 8` to `N = 384`. **That is the functional
setting a working certificate must use: an asymmetric pair of spaces separated by
exactly one power of spatial decay.**

## 8. What this means for Route D, said plainly

- The naive uniform-Fourier radii-polynomial NK **does not close at the `a = 0`
  anchor**, and the failure is structural rather than numerical: it survives every
  truncation, every gauge, and every weight.
- The blocker is **R** (the `θ = ±π` far field), demonstrated by ablation, not
  **G** (the gauge), which is exonerated. That reorders v1's open-risk list.
- The certification budget `Y₀^max` is **identically zero**, so the pessimistic
  forecast in v1 §7 — that an `a ≈ 0.5` certificate would fail because `Y₀` jumps
  to `~10⁻²` — was, if anything, too optimistic. The programme does not fail at
  `a ≠ 0` for lack of accuracy; it fails at `a = 0` for lack of a space.
- The repair is identified and numerically validated: an asymmetric,
  decay-graded pair of spaces, in which `‖A‖ = 3.000` uniformly.

**Next brick (specification, not a promise).** Rebuild the bounds in the graded
pair: domain `ℓ¹` cosine coefficients, codomain graded by one mode power, with
the far-field block handled by the *exact* ODE inverse above rather than a
diagonal model. Two things must then be re-derived, and neither is free: the
quadratic term `D²F[h,h] = 2 h H(h)` must be shown to land in the graded codomain
(the Wiener algebra bound gives `ℓ¹`, not the graded space, so the domain norm
likely has to move too), and the far-field inverse must be enclosed rigorously.
This is the standard "compact core + explicit far field" two-region structure of
the Chen–Hou / Gómez-Serrano genre; the honest reading of this leg is that the
project has arrived at the point where that structure becomes necessary, and now
knows exactly why.

**Ceiling.** Everything here is plain `float64`. Nothing in this note is
interval-enclosed and nothing is claimed as rigorous — that was the whole point of
running the rehearsal first, and it saved the interval hardening of a set of
bounds that could never have closed. This leg does not climb the rigor ladder. Even
the success it is scouting would be a computer-assisted *toy-model* certification,
not a Clay solve. Overall Clay odds unchanged (~0.05%).
