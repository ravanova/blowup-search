# Route-TN v1 — the `(H, D)` consistency defect of `L1` step one, enclosed

**Leg 56. Exploration route (not critical path). Gate answered NO.**
Runner `experiments/p2_route_tn_v1_consistency.py` · data
`writeup/data/p2_route_tn_v1_consistency.json` · figure
`writeup/figures/fig51_route_tn_v1_consistency.png` (rebuilt by
`experiments/p2_route_tn_v1_consistency_evidence.py`) · novelty log
`writeup/novelty/leg_56.md` · journal `experiments/journal/leg_56.md`.

Every number quoted below is in the curated JSON.

---

## 1. Scope, stated before anything else

`solver/interval_certificate.py` proves a statement about a **finite-dimensional polynomial
system built from the stored float matrices `H`, `D`**. Its docstring names the two gaps
between that and the continuum profile: the consistency of `(H, D)`, and the far field
beyond `X_max`. This leg bounds the **first**, at **fixed reach**.

**This is not "closing the truncation gap by extending the domain"** (banned; leg 47
measured that trend at +0.47 decades per unit ρ, the wrong sign). `X_max = 745.2394128947751`
is identical in every run at every rung. `n` is the only thing that moves. The far-field term
is computed **only** so it can be subtracted from the measurement and reported in a separate
column (discipline 75: two defects in the same problem are not the same defect).

**Nothing below is a claim about `HL_S2_nonsymmetric` being certified, about the far-field
gap, about the coefficient-basis work of legs 51–53, or about any link of the L1→L4 chain.**

## 2. Why the naive quantity has no referent (discipline 73)

There is no `‖H_disc − H‖`. `H_disc : R^n → R^n`; `H` maps functions to functions. The
difference is defined only relative to a **named class**, and its magnitude is a property of
that class as much as of the operator. Reported accordingly as a curve (§7), never as a
scalar impersonating an operator norm.

## 3. The structural fact the leg turns on

`line_hilbert_matrix` is **not a quadrature rule**. Per `solver/line_hilbert.py` (Huang–Tong–
Wang arXiv:2603.25104 App. C.1), it expands the data in the `C¹₀` Hermite basis `{P_i, Q_i}`
with node slopes taken from the natural cubic spline, and applies the **closed-form exact**
Hilbert transform of each basis element. `slope_matrix` returns the derivative of the **same**
interpolant. Writing `Π_n` for that interpolant:

```
H_disc f = H(Π_n f)|_[-M,M]                D_disc f = (Π_n f)'|_nodes
```

so with `e = Π_n f − f`:

| defect | equals | character |
|---|---|---|
| `D_disc f − f'` | `e'` | local; bounded by interpolation theory |
| `H_disc f − H_M f` | `H(e)` on `[−M, M]` | **gated here** |
| `H_M f − H f` | far-field tail | reported, **not** gated |

`H` is unbounded on `L^∞`, so `H(e)` **cannot** be bounded from `‖e‖_sup`. It must be
evaluated against an exact reference. That requirement is what the rest of the machinery
exists to satisfy.

## 4. The test class, and its closed forms

`u = X − b`, two families of identical interior smoothness:

| family | `f` | `H f` | `f'` | value at the cut |
|---|---|---|---|---|
| `odd` | `−u/(u²+a²)` | `a/(u²+a²)` | `(u²−a²)/(u²+a²)²` | `~1/M` |
| `even` | `a/(u²+a²)` | `u/(u²+a²)` | `−2au/(u²+a²)²` | `~a/M²` |

(`a = 1/2, b = 0` in the `odd` family is exactly the CLM pair `test_line_hilbert.py` already
gates against.) Partial fractions of the truncated integral, with
`A = C`, `B` per family and `u₁ = −M−b`, `u₂ = M−b`:

```
π H_M f = (A/2) ln((u₂²+a²)/(u₁²+a²)) + (B/a)(arctan(u₂/a) − arctan(u₁/a)) − C ln|(x−M)/(x+M)|
```

which → `π B/a = π H f` as `M → ∞`, as it must. The **truncation** is formed directly from
the small residual terms rather than as a difference of two nearly equal numbers.

**Endpoint nodes are excluded** (2 of n; 799 interior at n = 801). At `x = ±M` the truncated
transform is log-divergent, `H_disc`'s boundary basis is one-sided and finite, and the two
divergences cancel analytically but not in floating point.

## 5. Rigorous evaluation

New in `solver/interval.py`, because `np.log` / `np.arctan` carry no ULP guarantee this
module may assume:

* `ilog` — exact reduction `x = m·2^e` (`np.frexp`), then `log m = 2 atanh((m−1)/(m+1))` with
  `|z| ≤ 1/3` and a **proved** geometric tail bound, plus a `log 2` enclosure.
* `iatan_small` — alternating Taylor series for `|t| ≤ 1/2`; remainder bounded by the first
  omitted term. Domain guards raise rather than silently extrapolate, and
  `test_interval.py` gates that they fire.
* Both are checked against an **independent 50-digit `decimal` reference**. Max widths:
  `ilog` 3.55e−14, `iatan_small` 1.48e−14.

Discrete operators are applied by the compensated `dot2_matvec` on the midpoint, with the
input enclosure's radius carried through by `|Mat| @ rad`. Both pieces round outward.

## 6. The comparison quantity (discipline 67)

A consistency defect enters as an addition to the residual:
`Y₀ → ‖A(F + δF)‖_w ≤ Y₀ + ‖A‖_w ‖δF‖_w`. So the admissible defect is

```
τ = budget / ‖A‖_w
```

Re-derived here, not quoted (lesson 85). At n = 801: `budget = 3.554656e−10`,
`‖A‖_w = 15417.7` — **both matching leg 46/50's stored values to all printed digits**.
Hence **τ = 2.306e−14**.

`Y₀` itself re-derives as 9.97e−12 against 7.35e−12 stored (Newton landing at a slightly
different converged iterate; both far under budget). `Y₀` does not enter this leg's
comparison, and both values are on panel E rather than being asserted away.

**τ overstates what is admissible** (clause TN-5): it discards every amplification the true
`δF` carries — the profile's own norm, the `S` factor, the velocity operator. A defect that
fails against `τ` fails against the real requirement a fortiori. Only that direction is
claimed.

## 7. Results

`X_max = 745.239` fixed; weighted sup norm with `ν = (1+X²)^{p/2}`, `p = P_STAR = 0.39`.

**The ladder** (`odd`, `a = 1/2`):

| n | `D` defect | order | `H` defect | order | truncation | τ |
|---|---|---|---|---|---|---|
| 201 | 1.1220e−04 | — | 4.7287e−03 | — | 1.9042e−02 | 2.3008e−13 |
| 401 | 6.8724e−06 | 4.03 | 4.7131e−03 | 0.00 | 2.2582e−02 | 3.1728e−14 |
| 801 | 4.2738e−07 | 4.01 | 4.7041e−03 | 0.00 | 2.6260e−02 | 2.3056e−14 |

**Against τ at n = 801:** `D` is **1.854e+07 τ**; `H` is **2.040e+11 τ**; the far-field
truncation is **1.139e+12 τ**.

**The two defects fail differently, and merging them would destroy the result (TN-7):**

* `D` converges at **order 4.01** — the natural-spline order, measured. It is simply far too
  large. Extrapolating at that order, reaching τ needs **n ≈ 52,163** (`N = 104,329`, dense).
* `H` **does not converge**: 1.0052× total over a 4× refinement. Refinement is not a lever.

**The scale curve** (n = 801, `odd`) — the answer to "the defect of what?":
`a` = 0.125 → `D` 1.804e−03; 0.25 → 2.752e−05; 0.5 → 4.274e−07; ≥ 1 → floors at ≈ 7.13e−08.
`H` is flat at 4.704e−03 across the whole range, because for large `|X|` the class member is
`≈ −1/X` regardless of `a`, and `H`'s defect lives there. `D`'s floor is the same far-field
mesh effect (`h ≈ 14.8` at `|X| ≈ 745`, n = 801) taking over from the origin.

## 8. Mechanism, ablated (lessons 85 and 90)

`line_hilbert_matrix` assembles source columns for **interior nodes only** (`x[1:-1]`); the
endpoint `P`-columns are identically zero. The transformed object therefore has
`f(±X_max) = 0` imposed on it.

The ablation dials **only the value at the cut**, by `M/a ≈ 1490`, holding interior
smoothness fixed. Nothing in the code path distinguishes the families.

| n | `H` odd | `H` even | collapse | `D` odd | `D` even | change |
|---|---|---|---|---|---|---|
| 201 | 4.7287e−03 | 3.3289e−06 | **1421×** | 1.1220e−04 | 1.0051e−04 | 1.12× |
| 401 | 4.7131e−03 | 3.1082e−06 | **1516×** | 6.8724e−06 | 6.1942e−06 | 1.11× |
| 801 | 4.7041e−03 | 3.1303e−06 | **1503×** | 4.2738e−07 | 3.8655e−07 | 1.11× |

The collapse matches `M/a = 1490.5` to within 1%, and the same dial moves `D` by 11%. The
control could have come out the other way (both moving, or neither): it did not.

The `even` family's `H` defect is *also* flat in `n` (3.33e−06 → 3.13e−06), so the
non-convergence is a property of the cut and not of the particular family.

## 9. The bound is not its own evaluation error (discipline 86)

This was pre-registered as the leg's central risk. At n = 801, enclosure width / value:

* `D`: **6.34e−08**
* `H`: **1.15e−13**

Both bounds dominate their own evaluation error by seven and thirteen orders. The risk did
not materialise.

The closed-form reference is independently verified: `test_interval_certificate.py` (8)
checks it against a direct principal-value quadrature sharing **no code** with it, over 12
(family, `a`, node) cases — worst absolute disagreement **4.44e−15**. The comparison is
mixed absolute/relative on purpose: the `even` family's truncated transform vanishes
identically at `X = 0` by symmetry, and a pure relative test there divides by a true zero.

## 10. Gates added

`test_interval.py`: `ilog` / `iatan_small` enclose an independent 50-digit reference; the
domain guards fire.

`test_interval_certificate.py` (8)–(12): the reference matches independent quadrature; the
ablation separates; `D` converges at order 4 ± 0.25; **`H` is flat to within 5% over a 4×
refinement** — deliberately falsifiable, so that a future change making `H` converge fails
the gate and forces a re-read; width/value < 1e−4 for both. All 12 gates pass (414 s).

## 11. Gate answer

> **Can the `(H, D)` consistency defect be enclosed by a rigorous bound that is smaller than
> leg 46's `Y₀` budget at n = 801, with a convergence rate measured across n = 201/401/801?**
>
> **NO.**

Reporting the magnitude and the rate, as the no-branch requires: at n = 801 the defect is
**4.704e−03** (Hilbert) and **4.274e−07** (derivative) in the certificate's own weighted sup
norm, against an admissible **τ = 2.306e−14** — exceeding it by **2.04e+11×** and
**1.85e+07×**. The rates across n = 201/401/801 are **order 0.00** for the Hilbert defect
(it does not converge) and **order 4.01** for the derivative defect.

Per the pre-committed no-branch: **the collocation realization cannot carry `L1`, and the
coefficient basis is the only lane left for it. No grid-basis repairs are proposed** — not
the boundary-basis change §8 obviously invites, nor any other.

**The negative does not hinge on the `H` artifact.** With the Hilbert defect deleted
outright, the derivative defect alone still requires n ≈ 52,163 at its measured order 4 —
a dense interval system of dimension 104,329.

## 12. Ceiling

Pre-committed and honoured. Nothing above is a statement about `HL_S2_nonsymmetric` being
certified, about the far-field gap, about the coefficient basis, or about the method's
viability anywhere else. **No link of the L1→L4 chain moved; in 56 legs none has.** Clay
remains ~0.05% behind Walls 1 and 2.

**Novelty: `PROCEED_NARROW`, six queries, nothing banked.** Rigorous error bounds for
spline-based Hilbert transforms inside computer-assisted proofs are established practice in
this exact literature (Chen–Hou–Huang, arXiv:2106.05422 and arXiv:2305.05660). Links, not
counts, in `writeup/novelty/leg_56.md`. Leg 52's search-index flag on arXiv:2604.01868
**stands** — it surfaced inside a broad topical query here, which is recorded as a surfacing
and explicitly **not** as a clearance.
