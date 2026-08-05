# Route-TC v1 — assembling the bordered certificate: the four terms in one polynomial, and the term that ran out is the one that did not exist before

*Leg 53. Runner `experiments/p2_route_tc_v1_assemble.py` → `writeup/data/p2_route_tc_v1_assemble.json`
→ **fig48** (`writeup/4_p2_lottery/p2_route_tc_v1_evidence.py`, rebuilds from committed data
with no recomputation). Deterministic. Stage `TC` of `plan_of_record.py`, 8 pre-committed
clauses.*

---

## 0. The gate, and its literal answer

> **GATE (pre-committed).** With the far-field amplitude carried as a real unknown through
> all four terms, does the radii polynomial close — on the `a = 0` CLM object, in a class
> with `s < 0.394`?

**NO.**

> **CORRECTED AFTER VERIFIER'S REVIEW (PR #5, `writeup/4_p2_lottery/VERIFY_LEG52_HEADLINE.md` Part B).**
> The gate answer and every measured number below stand and were independently confirmed.
> Three things in the first version of this document did not: the **scope** of the failure
> (§0 and §2), the **stated mechanism** (§2), and the status of TC-5b's headline control
> (§5). All three are corrected here, and §5b adds a normalisation ablation the first
> version should have run. Part C of the same review withdrew this leg's resurfacing
> clearance; see §6.

**TERM THAT RAN OUT: `Z₁`, and specifically its two BLOCK-COUPLING sub-blocks** — the pieces
of `I − A L` that connect the finite block to the bordered tail. They did not exist as
quantities before this leg, because before this leg the two blocks had never been in the same
object. Neither the tail constant (leg 52) nor `Y₀` nor `Z₂` is what failed.

**SCOPE, STATED EXACTLY.** What this establishes is that the **block-diagonal** approximate
inverse the standard method requires cannot close this certificate — at `s = 0` and
`s = 0.3`, under both gauges, at every split `K = 4 … 64`, and under all six normalisations
of the augmented block ablated in §5b. What it does **not** establish is that *no* finite
block can. The genuinely finite-block-independent sub-block is `Z₁[tail←Γ]`, and its minimum
over the whole sweep is **0.9961 — below 1.** That is precisely why the plan's next stage
(`MM`: an approximate inverse that is *not* block diagonal) is a real question and not a
formality.

---

## 1. What was assembled (TC-1)

The object is leg 51's: the `a = 0` CLM fixed point `Ω₀ = −sin θ`, `c_ω = −1`, `c_l = 1`, in
the compactified odd-sine basis where `H`, `X d/dX` and `d/dX` are exact. **No new basis** —
leg 51 chose it and leg 52 measured the tail in it.

The linearisation's column `k` is, exactly,

```
row k+1 :  1 − k/2        row k−1 :  k/2        row 1 : −(−1)^k
```

so its diagonal is exactly zero for `k ≥ 2` and its unbounded part is **off-diagonal**.

**The far-field direction.** `ĥ` is leg 52's `tail_right_null`: `h_{K+1} = 1`, propagated by
the homogeneous two-term recursion, supported on modes `K+1, K+3, …`, decaying like
`m^{−2.00}`. Extending it by zero onto modes `1 … K` and applying the exact linearisation
gives the far-field amplitude's **column in the finite block** — computed, not fitted:

| `K` | row `K` entry `(K+1)/2` | row 1 entry `Σ_{m>K} −(−1)^m h_m` | gauge row `Σ_{m>K} m h_m` | `‖ĥ‖_{ℓ¹}` |
|---|---|---|---|---|
| 4 | +2.500 | +2.493 | +46.53 | 2.493 |
| 8 | +4.500 | +4.469 | +161.94 | 4.469 |
| 16 | +8.500 | +8.377 | +548.91 | 8.377 |
| 32 | +16.500 | +16.015 | +1820.41 | 16.015 |
| 64 | +32.500 | +30.616 | +5862.15 | 30.616 |

(`M = K + 1024` throughout this table.)

Two entries, both explicit: the amplitude reaches mode `K` through the operator's own
sub-diagonal with weight `(K+1)/2`, and mode 1 through the rank-one `H Ω` term with weight
`≈ K/2`. **The far-field amplitude is not a weakly coupled bookkeeping variable — it feeds
back into the finite block with a strength that grows linearly in the split.**

**The matching row.** `a` is defined as the amplitude of `ĥ` in the tail; the matching row
states that, and its content *as an equation* is a coupling to the tail remainder. That is
itself a finding and it is recorded as one: **the far-field amplitude is fixed by the tail,
not by the finite block**, so the matching condition contributes to `Z₁`'s coupling blocks
rather than sitting inside the finite matrix.

**The gauge.** Two are run, because if the answer turned on the gauge that would be the
finding.

* `dilation` — leg 51's `Σ_k k b_k`;
* `null` — pin the exact dilation zero mode instead. That mode is **exactly `e₂`**: `X d/dX`
  applied to `−sin θ` is `−(1/2) sin 2θ`, and `‖L e₂‖_∞ = 0.00e+00` in float — checked, not
  asserted.

The answer does **not** turn on the gauge (both fail), but the dilation gauge is separately
inadmissible — see §4.

---

## 2. `Z₁` decomposed by sub-block (TC-4)

The radii-polynomial method needs an approximate inverse of the shape
`A = Γ⁻¹ ⊕ A_tail` (block diagonal: a computed finite inverse, an explicit tail estimate).
`Γ` is the augmented finite block above; `A_tail` is leg 52's bordered tail inverse. The four
sub-blocks of `I − A L` are then separate, computable objects, and **a sub-block's norm is a
lower bound on `Z₁`** for that `A`.

All values in the weighted `ℓ¹` operator norm `‖M‖_w = max_j (1/w_j) Σ_i w_i |M_ij|`, with
`w_k = 1` (flat) or `(1+k)^s`. `M = K + 1024`. Border = analytic (leg 52's far-field pair).

**Flat, `s = 0`, `null` gauge:**

| `K` | `‖Γ⁻¹‖` | `‖A_tail‖` | `Z₁[ΓΓ]` | `Z₁[tail←Γ]` | `Z₁[Γ←tail]` | `Z₁[tail tail]` |
|---|---|---|---|---|---|---|
| 4 | 30.0 | 2.191 | 3.5e−16 | **0.996** | **59.0** | 1.2e−12 |
| 8 | 126 | 3.234 | 3.2e−15 | **2.977** | **251** | 1.2e−11 |
| 16 | 510 | 4.654 | 6.2e−14 | **6.892** | **1019** | 4.9e−12 |
| 32 | 2.05e+03 | 6.539 | 3.4e−13 | **14.545** | **4091** | 9.6e−13 |
| 64 | 8.19e+03 | 8.936 | 1.8e−12 | **29.176** | **1.638e+04** | 2.5e−13 |

**Algebraic `s = 0.3`, `null` gauge:**

| `K` | `‖Γ⁻¹‖` | `‖A_tail‖` | `Z₁[ΓΓ]` | `Z₁[tail←Γ]` | `Z₁[Γ←tail]` | `Z₁[tail tail]` |
|---|---|---|---|---|---|---|
| 4 | 22.7 | 2.604 | 7.7e−16 | **1.387** | **43.15** | 6.0e−13 |
| 8 | 81.7 | 3.918 | 2.8e−15 | **4.124** | **159.4** | 2.6e−12 |
| 16 | 277 | 5.619 | 2.5e−14 | **9.441** | **546.6** | 1.7e−12 |
| 32 | 919 | 7.759 | 1.6e−13 | **19.558** | **1822** | 4.6e−13 |
| 64 | 3.02e+03 | 10.318 | 6.4e−13 | **38.182** | **6000** | 1.7e−13 |

The `dilation`-gauge rows are worse throughout — `Z₁[Γ←tail]` larger by a factor **1.52 to
8.73** (worst at `K = 4`, flat) — and are in the JSON.

**Read the two diagonal blocks first.** `Z₁[ΓΓ]` is the float inverse's own defect,
`10⁻¹⁶ … 10⁻¹²`. `Z₁[tail tail]` is `10⁻¹³ … 10⁻¹¹` — **but that number cannot report what it
looks like it reports**: with a border on, `A_tail` is inverted from the bordered matrix
itself, so `A_tail · B_tail = I` identically and the quantity measures float round-off, not
the tail's truncation defect at `M`. It only makes the NO stronger, so nothing turns on it;
it should not be read as "the tail–tail block is fine". *(Also: `Z1_total` sums all four
sub-blocks, whereas the norm the block system actually induces is
`max(z_GG + z_tG, z_Gt + z_tt)`. The reported `Z₁` is therefore a slight over-estimate —
44.539 against 43.151 at the best row. Conservative; changes nothing.)* Leg 52's bordered
tail constant
appears here as `‖A_tail‖ = 2.19 … 10.3` and behaves exactly as leg 52 reported.

**The two off-diagonal blocks are the whole result.**

`Z₁[tail←Γ] = ‖A_tail L_{tail,Γ}‖`. `L_{tail,Γ}` has a single structural entry: mode `K`
feeds residual mode `K+1` with coefficient `1 − K/2`. **This block does not involve `Γ⁻¹` at
all**, so it is a lower bound on `Z₁` for *every* choice of finite block, however clever.
Its value is `≈ (K/2 − 1) · ‖A_tail e_{K+1}‖_w / w_K`, the second factor is `O(1)` because
leg 52's bordered tail inverse is a **constant** rather than a decaying multiplier, and so it
grows **exactly ×2 per doubling of `K`** (0.996, 2.977, 6.892, 14.545, 29.176). **But its
minimum over the whole sweep is 0.9961, which is below 1** — so this term alone does not
forbid closure, and the structural claim has to be stated as what it is: the *rate* is
structural, the *failure at the best split* is not from this term.

`Z₁[Γ←tail] = ‖Γ⁻¹ L_{Γ,tail}‖` — **this is the term that actually exceeds 1 everywhere, and
it does involve `Γ⁻¹`.** Measured across every row of the sweep,

```
Z1[Gamma<-tail] / ||Gamma^-1||  =  1.9667, 1.9921, 1.9980, 1.9995, 1.9999   (flat)
                                   1.9028, 1.9503, 1.9712, 1.9826, 1.9896   (s = 0.3)
```

so under the shipped normalisation `Z₁[Γ←tail] = 2‖Γ⁻¹‖` and **the whole `K`-dependence lives
in `‖Γ⁻¹‖`, not in the coupling entry.** The coupling contributes a factor **2**, and its
dominant column is the **rank-one row-1 term** — `−(−1)^m` into residual mode 1, weight 1 from
*every* tail mode — not the `(K+1)/2` sub-diagonal.

**And `‖Γ⁻¹‖` grows like `K²`, not `K` — and the `K²` is created by this leg's own
augmentation.** For the augmented block it is **exactly `2(K² − 1)`** (30, 126, 510, 2046,
8190 at `K = 4 … 64`, `×4.00` per doubling); re-running the *same* code path with
`far_field=False` — the same block without the amplitude column and matching row — gives
**exactly `4(K − 1)`** (12, 28, 60, 124, 252, `×2.02`). The inflation is the weight pairing:
the amplitude column carries `W_a = ‖ĥ‖_w ≈ K/2` while the matching row carries
`ρ = w_{K+1}`, so in weighted coordinates the matching equation has coefficient `≈ 2/K` — a
deliberately weak equation, and inverting it costs a factor `K`. **That is a normalisation
choice, and §5b ablates it.**

*(The first version of this document cited leg 51's `A_norm` 165 → 359 → 769 → 1633 as
"`‖Γ⁻¹‖` grows like `K`". That is a different matrix — leg 51's* unaugmented *finite block —
and at `K = 64` the two differ by 23×. The citation was wrong and so was the exponent.)*

**The structural fact, which survives all of the above.** The standard radii-polynomial tail
estimate works because the unbounded part of the operator is a *multiplier*: the split cuts
through an entry of size `Λ_M`, and the tail inverse is `1/Λ_M`, so the product is `O(1)` and
can be made small. Here the unbounded part is **off-diagonal**, so any split cuts through an
entry of size `K/2` — and bordering, which fixed the tail block's *invertibility*, does
nothing to the *size* of the tail inverse: it returns a constant, not `1/K`. **Constant times
`K/2` diverges**, and that is exactly the `×2`-per-doubling growth measured in `Z₁[tail←Γ]`,
reaching 38.2 by `K = 64`. What that argument does **not** deliver on its own is failure at
the *smallest* split, where `Z₁[tail←Γ] = 0.9961`; the failure there comes from
`Z₁[Γ←tail] = 2‖Γ⁻¹‖`, which §5b shows is not a normalisation artifact either.

This is banked lesson 75 in action: two defects in the same problem are not the same defect.
Leg 51 found the tail block non-invertible; leg 52 fixed that; the coupling is a different
defect and it survives the fix.

---

## 3. The four terms in one polynomial (TC-2)

`Y₀ = 0` **exactly**, in every class and at every split, including the new matching row. The
matching row's residual at the anchor is exactly `0.0`, and the reason is the same degeneracy
that gives leg 51's `Y₀ = 0`: the `a = 0` CLM anchor **is** one basis mode, its tail is
identically zero, so the far-field amplitude it implies is exactly zero and the matching
condition is satisfied with nothing left over.

With `Y₀ = 0` the polynomial `Z₂ r² − (1 − Z₁) r + Y₀ ≤ 0` **always has the root `r = 0`**.
That root certifies nothing — it is the statement that an exact anchor is exact. The
reportable quantity is whether the inequality holds on a **positive interval**, which needs
`Z₁ < 1`. It does not, anywhere.

Assembled, with the bounded gauge:

| class | `K` | `Y₀` | `Z₁` (assembled) | `Z₂` | tail const | positive interval | `r_max` |
|---|---|---|---|---|---|---|---|
| flat | 4 | 0 | 59.996 | 180 | 2.191 | **no** | 0 |
| flat | 16 | 0 | 1025.9 | 3060 | 4.654 | **no** | 0 |
| flat | 64 | 0 | 16408 | 49140 | 8.936 | **no** | 0 |
| `s = 0.3` | **4** | 0 | **44.539** | **119.02** | 2.604 | **no** | 0 |
| `s = 0.3` | 16 | 0 | 556.01 | 1455.3 | 5.619 | **no** | 0 |
| `s = 0.3` | 64 | 0 | 6038.2 | 15829 | 10.318 | **no** | 0 |

The full ten rows are in `TC2_polynomial`, each also carrying the rigorous finite-block `Z₁`,
the two coupling blocks, `‖A‖`, the Banach-algebra quadratic bound `Q` with `Z₂ = 2‖A‖·Q`,
the discriminant and both roots.

**And the counterfactual is in the same row**, because it is the number that would have been
reported if the terms had never been assembled: `poly_leg51_only` repeats the polynomial with
leg 51's finite-block `Z₁` and `‖A‖` alone. **That one has a positive interval in every row** —
`r_max = 2.142e−02` at `s = 0.3`, `K = 4`, down to `4.642e−04` at flat `K = 64`. **The
difference between those two columns is exactly the content of this leg:** three terms of
four close comfortably, and the fourth is the one that only exists once they are assembled.

---

## 4. The border's own defect (TC-3)

Three magnitudes, and what each dominates.

**(a) The matching row's residual at the anchor: exactly `0.0`.** It dominates nothing. It is
zero for a degenerate reason (§3) and it is reported so that a later leg on a real profile
knows the quantity exists and where it enters.

**(b) The asymptotic expansion's own truncation defect.** `‖(L ĥ)|_{tail rows}‖_w / ‖ĥ‖_w`,
i.e. how far the far-field mode is from being annihilated once its recursion is cut at `M`.
At `K = 64`, `M = K + 1024`: **6.15e−02** (flat), **1.10e−01** (`s = 0.3`). It falls with the truncation:
fitted exponent **−1.0000** (flat) and **−0.7794** (`s = 0.3`) in `M` — ladder and fits in
the JSON. It is a genuine defect of the
border, it is `10⁻¹`–`10⁻²`, and it dominates `Y₀` (which is zero) and nothing else: it is
two to three orders below the coupling blocks.

**(c) The gauge row's entry on the far-field column — and this one does not exist.**
`Σ_{m>K} m h_m` with `h_m ~ C m^{−2}` is a harmonic sum. Measured at `K = 64`:

```
M − K =   256     512    1024    2048
        3347.4  4556.6  5862.2  7222.1        →  +1865 per e-fold in M
```

**Logarithmically divergent.** The underlying statement is not numerical: the dilation gauge
`Σ_k k b_k` has dual norm `max_k k / w_k` on `ℓ¹_w`, which is **infinite for every `s < 1`** —
i.e. for every class in which the target profile has finite norm. **The far-field column has
an entry that does not exist**, and it was invisible until the amplitude had a column at all.

What it dominates: it makes `‖Γ‖` itself unbounded under the natural gauge, hence `‖A‖` and
hence `Z₂`. The repair is available and is not a tuning of `s`: pin the exact null direction
`e₂` instead (a bounded functional of norm `1/w₂`). Both gauges are run above, and with the
bounded gauge `‖Γ⁻¹‖` improves by 1.78–1.84× and `Z₁[Γ←tail]` by 1.52–8.73× — **and the gate still answers NO**,
which is why the gauge is reported as a defect of the assembly rather than as the cause of
the failure.

---

## 5. Controls

**Positive control (TC-5).** Same code path with `Λ¹` dissipation (`−μk` on the diagonal),
turning the unbounded part from a shift into a multiplier. The control uses the **unbordered**
tail inverse and **drops the far-field column**, because a dissipative tail has no kernel and
needs no amplitude unknown — bordering it with one would charge the control a defect the
dissipative problem does not have. Values are in `TC5_positive_control`.

The instrument reports the other answer (`K = 16`, `M = K + 1024`):

| `μ` | class | `‖A_tail‖` | `Z₁[tail←Γ]` | `Z₁[Γ←tail]` | assembled `Z₁` |
|---|---|---|---|---|---|
| 0 | `s = 0.3` | 5.619 | 9.441 | 546.6 | 556.0 |
| 0.1 | `s = 0.3` | 0.6556 | 4.668 | 94.05 | 98.72 |
| 0.5 | `s = 0.3` | 0.1734 | 1.179 | 2.438 | 3.616 |
| 1.0 | `s = 0.3` | 0.08528 | 0.5506 | 1.086 | 1.636 |
| **2.0** | `s = 0.3` | 0.03801 | 0.2493 | 0.6663 | **0.9156** |
| 4.0 | `s = 0.3` | 0.01687 | 0.1154 | 0.5195 | 0.6348 |

The coupling blocks fall like `1/μ`, exactly as the mechanism predicts, and the assembled
`Z₁` crosses **below 1 at `μ = 2`**. **A method that
reported "does not close" for everything would not be measuring; this one reports closure as
soon as the operator has a diagonal.**

**Negative controls (TC-5b) — rewired so they can fail.** The first version of this leg
computed the coupling from `Γ⁻¹` and `L_{Γ,tail}`, **neither of which references the border**,
and then reported "`Z₁[Γ←tail]` is 546.57 for all four borders" as the sharpest form of the
result. VERIFIER was right that this is a **tautology of the code, not a measurement**. The
border direction is now wired through the **amplitude column** as well — the extra column is
`L` applied to whichever direction the border names — so a wrong amplitude direction changes
`Γ` itself and the control genuinely can come out differently. At `K = 16`, `s = 0.3`:

| border | `‖A_tail‖` | `‖Γ⁻¹‖` | `Z₁[tail←Γ]` | `Z₁[Γ←tail]` |
|---|---|---|---|---|
| **analytic** (the far-field mode) | **5.619** | **277.28** | **9.441** | **546.57** |
| svd (the best 1-d choice that exists) | 5.588 | 277.08 | 9.441 | 546.37 |
| second singular pair (wrong direction) | 26.76 | **2.099e+16** | 13.37 | **2.099e+16** |
| random | 338.9 | 6638.5 | 19.65 | 6907.8 |

**analytic / SVD = 1.0004** — the border a proof can write down matches the most favourable
one-dimensional choice that exists, reproducing leg 52's T-2 result one level up. The two
deliberately wrong directions are **worse by 12.6× (random) and 3.84e+13× (second)**; the
second singular pair is not the kernel, so using it as the amplitude direction makes the
augmented block essentially singular. **The controls can fail, and they do.**

What remains true, and is now stated as a structural observation rather than as a control:
`L_{Γ,tail}` and `L_{tail,Γ}` are pieces of the *operator*, so **the coupling exists whatever
direction the amplitude column carries** — the border chooses how badly it is conditioned,
not whether it is there.

**(TC-8) NORMALISATION ABLATION — because `‖Γ⁻¹‖`'s `K²` is a choice, not a fact.** §2 shows
the augmentation inflates `‖Γ⁻¹‖` from `4(K−1)` to `2(K²−1)` through the weight pairing
between the amplitude column (`W_a`) and the matching row (`ρ`). Five conventions for that
pair, plus the un-augmented block as the lower envelope, `null` gauge:

| convention | `(W_a, ρ)` | flat `K=4` `Z₁[Γ←tail]` | `s=0.3` `K=4` | `s=0.3` `K=16` |
|---|---|---|---|---|
| **shipped** | `(‖ĥ‖_w, w_{K+1})` | 59.00 | **43.15** | 546.6 |
| unit_column | `(1, w_{K+1})` | 57.51 | 40.66 | 535.9 |
| unit_row | `(‖ĥ‖_w, 1)` | 59.00 | 43.15 | 546.6 |
| unit_both | `(1, 1)` | 57.51 | 40.66 | 535.9 |
| row_like_col | `(‖ĥ‖_w, ‖ĥ‖_w)` | 59.00 | 43.15 | 546.6 |
| **no_amplitude** (lower envelope) | — | 29.00 | **20.47** | 269.3 |

**The smallest `Z₁` lower bound over every normalisation tried is 20.47** — one to two orders
above 1, and still growing in `K`. Note also that `row_like_col` drops `‖Γ⁻¹‖` from 22.68 to
8.90 at `s = 0.3, K = 4` while leaving `Z₁[Γ←tail]` at 43.15 unchanged: **`Z₁[Γ←tail] = 2‖Γ⁻¹‖`
is a fact about the shipped convention, not an identity.** The gate answer survives the
renormalisation that the corrected mechanism invites.

**Split-point sweep (TC-6).** `K = 4 … 64`. The fair question was never whether the largest
split works; it was whether **any** split works. None does, and the trend is monotone in the
wrong direction.

---

## 6. Novelty (TC-0), run before the construction

Verdict **`PROCEED_NARROW`**, six queries, four ledger entries, all committed in the runner
and in `LITERATURE_CHECK.md`.

* **`arXiv:1503.06315` (Breden–Desvillettes–Lessard, DCDS-A 35(10) 4765–4789).** Leg 52 left
  open whether their construction reaches a tridiagonal operator with an exactly zero
  diagonal. This pass fetched the publisher's abstract page: the stated hypothesis is a
  tridiagonal **dominant** linear part. Our tail does not satisfy it. **That was evidence, not
  proof** — a reading of an abstract, not the full text — and it has since been **superseded**:
  LIT's ninth pass extracted the PDF and settled the question outright (assumption (4) needs
  `C1 ≤ μ_k/ω_k^{s_L} ≤ C2` with `C1 > 0`, assumption (5)'s ratios are undefined at `μ_k = 0`,
  the LU construction divides by `μ_k`, and a vanishing diagonal is not on their own
  future-work list). **Read LIT's item 2, not this entry.** The general observation remains a
  re-derivation, exactly as leg 52 recorded it.
* **`arXiv:2604.01868` (Bojin Chen, De Huang, Xiangyuan Li, April 2026). CLEARANCE
  WITHDRAWN — THE FLAG STANDS.** This pass originally reported leg 52's search-index flag as
  cleared, because query 4 returned a summary naming the paper's title and authors correctly.
  VERIFIER adjudicated that against LIT's ninth pass and **LIT wins.** Query 4 prepends the
  literal arXiv ID, so it tests retrieval *by ID* — which was never in dispute — and not the
  **topical recall without an identifier** the flag was actually raised against. LIT re-ran
  leg 52's query **verbatim** and reproduced the null result, and enumerated the links
  returned by an ID-bearing query: all other papers, with the correct title appearing only in
  the prose summary, i.e. the model answering from its own knowledge rather than from a
  surfaced link. This pass logged **counts, not links**, so its clearance could not be audited
  against its own record. *The accurate statement: fetching by ID has always worked; topical
  recall still fails; the flag stands.*
* **`arXiv:2406.16597` / CPA (2026), self-similar blowup for cubic NLS.** Bordering a
  certificate to kill a symmetry-induced kernel is standard, and **no novelty is claimed for
  the move.** What is measured here is what happens when the kernel is the far field of an
  unbounded *off-diagonal* operator, so the border acquires a coupling term.
* **SIADS `doi:10.1137/23M1607507`, semilinear PDEs on unbounded domains via spectral
  methods.** Semilinear: the unbounded part is a multiplier, so the standard tail estimate
  applies. Confirms leg 51's reading of the field's shape; supplies no construction for an
  unbounded off-diagonal part.

---

## 7. Ceiling (TC-7), pre-committed before the numbers existed

Measured on the `a = 0` CLM fixed point: one mode, analytic, in every weight class
considered.

`Y₀` is exactly zero there — **including the new matching row** — because the anchor *is* one
basis mode and therefore has no far field at all. The polynomial's root `r = 0` is available
for a degenerate reason and certifies nothing; the reportable quantity is the positive
interval, and there is none.

**Nothing is claimed about `HL_S2_nonsymmetric`.** On the gate's own terms that run happens
only if the polynomial closes here, and it did not. A wall measured on the easiest available
object bounds the difficulty for the real target **from below, not from above**.

**No link of the L1→L4 chain moved. Clay unchanged at ~0.05%.**

---

## 8. Reproduce

```
.venv/bin/python -u experiments/p2_route_tc_v1_assemble.py     # regenerate the JSON
.venv/bin/python writeup/4_p2_lottery/p2_route_tc_v1_evidence.py   # rebuild fig48 only
```

Every number quoted above is present in `writeup/data/p2_route_tc_v1_assemble.json`.
