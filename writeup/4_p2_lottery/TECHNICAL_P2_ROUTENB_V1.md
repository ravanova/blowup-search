# Route-NB v1 — TECHNICAL: the compactified-basis coefficient decay of `HL_S2_nonsymmetric`

**Leg 55. Exploration route.** Runner `experiments/p2_route_nb_v1_targetnorm.py`; module
`solver/target_norm.py`; gates `test_target_norm.py` (23/23); curated data
`writeup/data/p2_route_nb_v1_targetnorm.json`; figure
`writeup/figures/fig50_route_nb_v1_targetnorm.png`; novelty log `writeup/novelty/leg_55.md`.
**Every number in this document is a field of the JSON, with one declared exception: the
`n = 3201` convergence confirmation in §4.1 (and the `6.3e-14` residual it reports) is a
separate run, not part of the curated payload, and is labelled as such at both mentions.**

---

## 0. The gate, in its pre-committed wording

> **Gate.** Do `HL_S2_nonsymmetric`'s compactified-basis coefficients decay fast enough
> that `‖·‖_{ℓ¹_w}` is finite for at least one admissible `s < 0.394`, with the exponent
> stable across the resolution ladder?

**Answered: `yes`.** `p = 1.3937` at the headline domain (`1.3963` at the largest domain),
finite at `s = 0`, `s = 0.3` and — marginally — `s = 0.39`; resolution drift `3.8e-04`.

§7 states what the yes-branch does and does not license, because the gate's yes-branch and
the ban clause's literal text are not about the same `s`.

---

## 1. The object and the basis

`HL_S2_nonsymmetric` is `solver/bordered_hl.py`'s bordered steady system for the 1D Hou–Luo
model (Chen–Huang–Li arXiv:2604.01868 §2.5/§4), solved by damped Newton on the
origin-clustered grid `X = c sinh ρ`, `c = 0.5`. Every solve in the curated JSON converges to
`≤ 2.3e-14` (the separate `n = 3201` confirmation of §4.1, which is not a JSON field, reaches
`6.3e-14`). The unknowns are `Ω`, `V = Θ_X` and three gauge constants `(c_l, c_ω, c_r)`.

`solver/spectral_certificate.py` compactifies with the tangent half-angle map
`X = tan(θ/2)`, in which the three operators of the `a = 0` CLM problem are exact. Its own
profiles are odd, so it uses an odd sine series. **The target is non-symmetric**, so
Route-NB uses the full circle:

    h(θ) := Ω(tan(θ/2)),   θ ∈ (−π, π),   h(θ) = Σ_{k∈ℤ} c_k e^{ikθ},  c_{−k} = conj(c_k)

with coefficient magnitude in the **complex-exponential convention**

    |ĥ_k| := |c_k| + |c_{−k}| = 2|c_k|,   k ≥ 1.

**Gate 2** of `test_target_norm.py` checks that `theta_of_X` is the *same* half-angle
convention as `spectral_certificate.moebius_power`, to `1.3e-15`, so the projection lands in
the certificate's basis and not a neighbouring one.

**Convention independence.** The real-basis alternative `|a_k| + |b_k|` satisfies
`2|c_k| ≤ |a_k| + |b_k| ≤ 2√2 |c_k|`; gate 6 verifies the bracket. A change of convention is
worth at most `√2` in the norm and **nothing** in the exponent.

### 1.1 Why the exponent is a statement about one point of the circle

`X → ±∞` is `θ → ±π`, a single point, near which `X ≈ 2/(π−θ)`. A far field
`Ω ~ A_± |X|^{−α}` becomes

    h(θ) ~ A_± ((π−θ)/2)^α,

a branch point of order `α`. Elsewhere the profile is smooth and contributes
super-algebraically. Hence the prediction `p = 1 + α`, already asserted (not measured) by
`spectral_certificate.coefficient_decay_exponent`. Non-symmetry only makes `A_+ ≠ A_−`; it
does not change `p`.

### 1.2 The norm

    ‖h‖_w = Σ_{k≥1} w_k |ĥ_k|,   w_k = (1+k)^s (algebraic) or 1 (flat)

using `spectral_certificate.weight_vector`. Gate 7 confirms the flat class **is** the
algebraic class at `s = 0`, entry for entry. For `|ĥ_k| ~ C k^{−p}`:

    ‖h‖_w < ∞  ⟺  p − s > 1.

---

## 2. The instrument, and its two failures

### 2.1 Pipeline

`compactify` interpolates the grid-borne profile in **`ρ`** (the variable the data are
uniform in; interpolating in `X` would put a 745-to-0.04 spacing ratio inside one stencil)
onto a **staggered** uniform `θ` grid of size `M`, then FFTs. The stagger
`θ_j = −π + 2π(j+½)/M` matters: `θ = ±π` is simultaneously the one point where `X` is
infinite and the point the exponent comes from, so a grid landing on it cannot be evaluated.
The half-cell shift is a pure phase and does not touch any `|c_k|`.

Interpolation is local barycentric Lagrange of order `L` on the uniform `ρ` grid (no scipy
in this project by design). Gates 4–5 check exactness on polynomials **and** that the order
knob is really wired — order 2 errs `9.3e-05` where order 12 errs `3.3e-16`, a ratio of
`2.8e+11`. An ablation on a dead knob proves nothing.

### 2.2 `fit_exponent` was wrong twice, and both times it returned a plausible number

Both failures were caught by a **control**, not by a test. Both are now regression gates
(14, 15).

**Failure 1 — log-averaging.** The first version binned `log|ĥ_k|` logarithmically and fitted
the bin means of the logs. Negative control 1, `Ω = 1/(1+|X|)`, obeys the identity
`h(θ) + h(π−θ) = 1`, which **annihilates every even mode**; the FFT returns `~1e-18` there.
Taking logs of those gave `p = −0.06` for a spectrum whose `k²|ĥ_k|` is flat to three digits
to 2.3% over `k = 9 … 129` (0.6222 → 0.6355 → 0.6365) and to three digits from `k = 33`
on. A `> 0` filter does not catch
`1e-18`.

**Failure 2 — sparse bins.** Switching to a **linear** mean within log bins fixed the
arithmetic but not the failure: one equal-width log bin at the bottom of the band caught a
*single* annihilated mode (`k = 10`, value `9.8e-19`), whose log is `−41` against a trend of
`−12`, and it captured the whole least squares. Result `p = −0.25`.

**Failure 3, avoided.** Equal-**count** bins cure the population problem but have `k`-widths
that grow along the band, so the convexity offset between a bin's linear mean and its value
at the bin's geometric-mean `k` drifts — biasing the fitted exponent by up to `+0.06` on the
calibration family.

**The shipped fitter** uses log-spaced bins **merged** until each holds ≥ 8 modes, with a
**linear** mean inside each bin. Log spacing makes every bin span the same *ratio* of `k`, so
the convexity offset is identical in every bin and moves the prefactor rather than the
slope; the merge makes an annihilated sub-sequence a factor-of-two effect on the prefactor
and none at all on the slope. The linear mean is also the physically right object: the norm
under study **sums** coefficients, so what decides finiteness is the mass in a bin, not its
geometric mean.

### 2.3 Calibration — the instrument's error bar, at the transform size actually used

`calibration_family(X, α) = (1+X²)^{−α/2}` has far field exactly `|X|^{−α}` and equals
`|cos(θ/2)|^α` exactly, so `p = 1 + α` for every `α`. Sweeping `α` and asking the fitter to
recover an exponent it was never told, **at `M = M_PRIMARY = 16384`, the transform size every
target measurement in this leg uses**:

| `α` | `p` measured | `p − (1+α)` |
|---|---|---|
| 0.1000 | 1.10752 | +0.00752 |
| 0.2000 | 1.20571 | +0.00571 |
| **0.3935** | **1.39739** | **+0.00389** |
| 0.6000 | 1.60335 | +0.00335 |
| 1.0000 | 2.00405 | +0.00405 |
| 1.5000 | 2.50612 | +0.00612 |

**Systematic at the target's own `α`: `+0.0039`. Worst over the sweep: `0.0075`.** The bias is
**positive** — the fitter over-estimates `p` — so a bias-corrected exponent is *lower*:
`1.3937 − 0.0039 = 1.3898`. All exponents below are quoted against this.

#### 2.3.1 And the systematic is a property of `(M, band)`, not of the fitter alone

**This was wrong in the first version of this document and was caught by VER-B's review.** The
calibration was originally run at `M = 65536` while every target measurement runs at
`M = 16384`, and the finer grid's systematic (`+0.0022`) was quoted against the coarser grid's
answer. It is `1.8×` too small:

| `M` | systematic at target `α` | worst over sweep |
|---|---|---|
| 4 096 | +0.01613 | 0.03132 |
| 8 192 | +0.00722 | 0.01492 |
| **16 384 (headline)** | **+0.00389** | **0.00752** |
| 32 768 | +0.00263 | 0.00611 |
| 65 536 | +0.00215 | 0.00610 |

The mistake was not arbitrary and that is what makes it worth recording: at `M = 65536` the
finest `θ` cell reaches `|X| = 2M/π = 4.17e+04`, **past the headline domain's `X_max`**, so
that grid could not have been used on the target without extrapolating. The calibration family
is analytic and has no such limit — which is exactly why calibrating it on a finer grid than
the target was measured on **flatters the instrument**. The control battery (§3) is now run at
`M_PRIMARY` throughout for the same reason.

---

## 3. The controls

| control | what it is | expected | measured |
|---|---|---|---|
| **positive** | `a = 0` CLM anchor `Ω₀ = −sin θ = −2X/(1+X²)`, exactly one mode | `\|ĥ₁\| = 1`, `p = ∞` | `\|ĥ₁\|−1 = 3.4e-15`, `max_{k≥2} = 1.7e-12` |
| **negative 1** | `1/(1+\|X\|)`: far field `\|X\|^{−1}`, kink at `θ = π` | `p = 2` (the `s = 1` threshold) | **1.9888** |
| **negative 2** | `2 arctan(X)/π = θ/π`: sawtooth, `α = 0`, jump | `p = 1` (the flat threshold) | **1.0008** |

**Positive-control window, pre-registered (lesson 84):** `| |ĥ₁| − 1 | < 1e-10` **and**
`max_{k≥2} |ĥ_k| < 1e-08`. Passed at `n = 201, 401, 801` (`4.4e-11 → 1.8e-13 → 3.4e-15`).
**It can fail:** a wrong half-angle convention, a sign error in `theta_of_X`, or an
off-by-one in the FFT phase each smear a single mode across all `k`.

**Negative control 2 also has exact coefficient VALUES**, `|ĥ_k| = 2/(πk)`, matched to
`1.0e-04` relative over `k ≤ 512`, and cross-checked against the repository's own
`spectral_certificate.sawtooth_coefficients` (gate 10). It is simultaneously the instrument's
hardest calibration: a jump is the worst non-smoothness on the circle, so it brackets the
target's `α`-cusp **from the bad side**, while the positive control brackets it from the
good side.

---

## 4. The two ladders

### 4.1 Resolution — flat

At the shipped domain `ρ_max = 8` (`X_max = 745.2`), `M = 16384`, band `k ∈ [32, 256]`:

| `n` | Newton residual | `p` | `R²` | noise floor | `α = −c_ω/c_l` |
|---|---|---|---|---|---|
| 201 | 7.4e-15 | 1.36887 | 0.999996 | 2.49e-06 | 0.39351 |
| 401 | 1.5e-14 | 1.36912 | 0.999996 | 2.50e-06 | 0.39356 |
| 801 | 2.3e-14 | 1.36925 | 0.999996 | 2.49e-06 | 0.39358 |

**Drift `3.77e-04`**, an order of magnitude under the fitter's own systematic (`+0.0039`,
§2.3). Separately confirmed at `ρ_max = 12`: `p = 1.3937 → 1.3938` across `n = 401 → 3201`
(*a separate run, not a JSON field*). The measurement is **not** resolution-limited.

### 4.2 Domain — the ladder that moves, and then stops

`n = 801`, `ρ_max = 8 → 14`:

| `ρ_max` | `X_max` | `p` | `p − 1` | physical tail exp. (outer) | `α` | `(p−1) − α` |
|---|---|---|---|---|---|---|
| 8 | 745.2 | 1.36925 | 0.36925 | −0.36093 | 0.39358 | **−0.02433** |
| 10 | 5 506.6 | 1.38761 | 0.38761 | −0.37954 | 0.39625 | **−0.00864** |
| 12 | 40 688.7 | 1.39374 | 0.39374 | −0.38935 | 0.39735 | **−0.00361** |
| 14 | 300 651.1 | 1.39631 | 0.39631 | −0.39410 | 0.39782 | **−0.00151** |

Three independent measurements — a Fourier fit on the circle, a log-log fit in physical
space (`bordered_hl.tail_exponent`), and a ratio of two Newton unknowns — converge together.
**The `k^{−1−α}` law is confirmed to `1.5e-03`**, and the shortfall at the shipped domain is
the profile not yet having reached its asymptotic tail at `X = 745`.

**This is a diagnostic, not a repair.** The live ban against *closing the truncation gap by
extending the domain* concerns the certificate's truncation gap, which leg 47 measured to get
**worse** with reach (`+0.47` decades per unit `ρ`). Nothing here repairs that gap; the two
quantities are different and both statements hold — the exponent improves with reach while
the certificate's gap worsens.

**Where the ladder stops, and why.** Gate 1 measures the float round-trip
`X → θ → X`: `4.0e-12` relative at `X = 4.1e+04`, `2.9e-11` at `X = 3.0e+05`. At
`X = 3.0e+05` the image `θ` sits `6.7e-06` from `π` and float64 `tan`/`arctan` lose about
five digits. That, not the physics, is what bounds the ladder.

---

## 5. Ablations

Base for §5.1–§5.3: `n = 801`, `ρ_max = 12`, `X_max = 4.07e+04`, `α = 0.39735`.

### 5.1 The far-field closure — it DECIDES at the shipped domain

| `ρ_max` | `X_max` | closure | `p` | `θ`-points outside grid | fires? |
|---|---|---|---|---|---|
| 8 | 745 | power (the equation's own tail) | **1.36925** | 14 | yes |
| 8 | 745 | clamp (injects `α = 0`) | **1.42279** | 14 | yes |
| 8 | 745 | zero (injects a jump) | **1.23295** | 14 | yes |
| 12 | 40 689 | power | 1.39374 | **0** | no |
| 12 | 40 689 | clamp | 1.39374 | **0** | no |
| 12 | 40 689 | zero | 1.39374 | **0** | no |

**Spread where it fires: `0.190`** — on a quantity whose meaning is its third decimal. The
finest `θ` cell of an `M`-point staggered grid sits `π/M` from the branch point, i.e. it
reaches `|X| = 2M/π = 1.043e+04` at `M = 16384`. A domain shorter than that **must** be
extrapolated (`X_max = 745`: 14 sample points outside); a longer one never is.

At `ρ_max = 12` all three rows are **byte-identical**, and that is *not* evidence the closure
does not matter — it is evidence the closure is never consulted. Per lesson 90, identical
numbers are reported with the reason they are identical (`n_theta_points_outside_grid = 0`)
rather than quoted as a null result. **The headline is measured where no closure is
consulted.** Gates 17–19 pin all of this, including that `far_field="none"` leaves NaN and
the transform refuses it rather than inventing data.

### 5.2 Interpolation order — a real null, shown to be real

| order | `p` (`ρ_max = 12`) | interpolant movement vs order 12 (relative) |
|---|---|---|
| 2 | 1.393710 | 8.67e-05 |
| 3 | 1.393745 | 3.02e-06 |
| 4 | 1.393744 | 1.50e-07 |
| 8 | 1.393745 | 1.50e-09 |

`p` is identical to five digits — again the lesson-90 tell. So the **movement of the
interpolant itself** is reported beside it: order 2 shifts `h` by `8.7e-05` relative and
shifts `p` by `3.5e-05`. The knob is wired (gate 5) and the profile is resolved. That is a
real null.

*Spreads are taken **within** a domain: the two `ρ_max` values sit at genuinely different
exponents, so a spread across both would report the domain ladder and mislabel it
interpolation sensitivity.*

### 5.3 Transform size and fit band

| `M` | `p` | | band | `p` |
|---|---|---|---|---|
| 4096 | 1.39912 | | [16, 128] | 1.40030 |
| 8192 | 1.39530 | | [32, 256] | 1.39374 |
| 16384 | 1.39374 | | [64, 512] | 1.39349 |
| 32768 | 1.39314 | | [32, 1024] | 1.39509 |

Spreads **`0.0060`** and **`0.0068`** — comparable to the calibration systematic and an order
of magnitude below the quantity being decided.

---

## 6. The norms

At `n = 801`, `ρ_max = 12`, `p = 1.39374`, `C = 0.48560`, `α = 0.39735`. Partial sums
`S_N = Σ_{k≤N} (1+k)^s |ĥ_k|`; the tail is the integral bound
`2^s C N^{−(p−s−1)} / (p−s−1)`.

| `s` | admissible (`s < α`) | margin `p−1−s` | `S_4096` | tail bound | `‖·‖` upper bound |
|---|---|---|---|---|---|
| **0.00** | yes | **+0.39374** | 1.5122 | 0.0466 | **1.5588** |
| **0.30** | yes | **+0.09374** | 3.3290 | 2.9241 | **6.2531** |
| 0.39 | yes | +0.00374 | 4.5764 | 164.72 | **NOT RESOLVED** (see below) |
| **1.00** | **no** | **−0.60626** | 123.12 | — | **DIVERGENT** |

At `s = 1` the entry is **not** a large number. `analytic_tail` returns
`finite: false, bound: null, reason: "p − s ≤ 1: the weighted sum diverges; the tail has no
value"` — when a quantity has no referent, say so instead of bounding it (lesson 73; gate 21).
Where it is finite the bound is verified to dominate the true summed remainder (gate 22).

**`s = 0.39` is NOT RESOLVED, and the first version of this document got that wrong.** Its
margin is `+0.00374` against a systematic of `+0.00389` at the headline's own `M` — a ratio of
**`0.96×`, i.e. the margin does not clear the instrument's own error bar.** The bias is
*positive*, so the bias-corrected margin is `+0.00374 − 0.00389 = −0.00015`: **negative**.

The first version quoted this row as finite on the strength of a `1.7×` ratio against the
`M = 65536` systematic `+0.0022` (§2.3.1) — erring **unsafe**, in the one direction that
matters. It is now reported as **not resolved**: the measurement cannot distinguish this class
from the divergent side, and `admissible_classes_with_finite_norm` in the JSON contains only
`[0.0, 0.3]`, with `0.39` listed separately under `admissible_classes_not_resolved`.

Two things do point the right way and neither is sufficient: the domain ladder had not
converged at this domain (`(p−1) − α` is still `−0.0036`), and against the largest-domain
`α = 0.39782` the margin would be `+0.0078`. **The gate does not need this row** — `s = 0` and
`s = 0.3` carry it with margins `100×` and `24×` the systematic.

### 6.1 The second unknown

| unknown | predicted far field | `p` measured | physical tail exp. | `s_max` |
|---|---|---|---|---|
| `Ω` | `\|X\|^{−α}`, `α = 0.397` | **1.39374** | −0.38935 | 0.394 |
| `V` | `\|X\|^{−2α}`, `2α = 0.795` | **1.83677** | −0.80351 | 0.837 |

`V` decays roughly twice as fast, as the steady equation forces. **`Ω` is binding** and the
gate is decided on `Ω` alone.

### 6.2 The window, both sides now measured

`spectral_certificate.weight_window(α = 0.39735, s_operator = 1.0)`:

    s_max_object = 0.39735     s_operator = 1.000     gap = +0.60265     empty = True

---

## 7. What the gate answer licenses, and what it does not

**The gate answers `yes` on its own wording.** The target's `ℓ¹_w` norm is finite for
admissible `s < 0.394` — `s = 0` (margin `+0.394`) and `s = 0.3` (margin `+0.094`) — with a
resolution drift of `3.8e-04`.

**The gate's yes-branch says the ban clause is "factually wrong". That overstates it, and
the overstatement should not be propagated.** The clause reads:

> *does not have finite norm **in the class where the operator is least bad***

The class where the operator is least bad is `s = 1` (leg 51's divergence-curve minimum).
**At `s = 1` the norm does diverge**, margin `−0.606`. So the clause, read literally, is
**correct**.

**Leg 51 said so itself, and it is the strongest support for this reading.**
`writeup/4_p2_lottery/TECHNICAL_P2_ROUTEL1_V2.md` §9 already states, in the same breath as its
window measurement:

> *"The class where the operator is least bad is the class where the target has infinite norm,
> and vice versa."*

That is precisely the clause's content, written by the leg that raised it. The clause was never
a claim that the target is outside *every* class — it is a claim about the *coincidence* of the
two classes, and this leg's measurement **confirms** it rather than refuting it.

What this leg establishes is therefore narrower and more useful than "the ban is wrong":

1. The **object side** of the window is now a measurement (`s_max = 0.397 ± 0.008`) where it
   was previously a docstring derivation applied to an assumed `α`.
2. The `k^{−1−α}` correspondence is **confirmed**, to `1.5e-03`, on the real target.
3. The window is **empty by `+0.603` in exponent units**, with both sides measured — which
   **confirms leg 51's published `0.606`** (`TECHNICAL_P2_ROUTEL1_V2.md` §9: *"The window is
   empty by 0.606 in exponent units"*) rather than adding a new quantity. The delta is that
   leg 51's object side was derived from an assumed `α` and this one is measured.
4. **The target is comfortably inside the space at `s = 0` and `s = 0.3`** — the classes legs
   52 and 53 actually used. So "the target was never in the space" is **not** an available
   explanation for those legs' failures. Leg 53's block coupling (`Z₁ = 43.15` at its best
   split) stands as the operative reason, untouched by this leg.

**Escalation.** Whether the clause's *text* needs narrowing is the Decision Maker's call, not
this leg's. It is flagged in the PR body. **No ban was edited here.**

**Not claimed:** that any certificate closes; anything about `MM`'s gate; that
`k^{−1−α}` or the value of `α` is novel (see `writeup/novelty/leg_55.md` Q1/Q4 — the
correspondence is classical, and arXiv:2308.01528 is the analytic prior art on far-field
decay rates for Hou–Luo profiles). **No link of the L1→L4 chain moved. Clay ~0.05%.**

---

## 8. Reproduction

    .venv/bin/python experiments/p2_route_nb_v1_targetnorm.py                       # ~4 min
    .venv/bin/python experiments/p2_route_nb_v1_targetnorm_evidence.py             # fig50
    .venv/bin/python test_target_norm.py                                            # 23 gates

`solver/spectral_certificate.py` and `solver/bordered_hl.py` are imported **read-only**;
neither has a diff in this leg.
