# Route-MM v1 — the shape of the approximate inverse, spent

**Stage `MM`, leg 54. Gate answer: NO.** Data: `writeup/data/p2_route_mm_v1_shape.json`.
Runner: `experiments/p2_route_mm_v1_shape.py`. Figure: `fig49_route_mm_v1_shape.png`,
rebuilt from the curated JSON alone by `experiments/p2_route_mm_v1_shape_evidence.py`.

> **Gate, in its pre-committed wording.** *Does an approximate inverse that is NOT block
> diagonal bring the assembled `Z₁` below 1, on the `a = 0` CLM object, in a class with
> `s < 0.394`?* — **NO.** The no-branch fires: **stop building `ℓ¹`-Fourier
> radii-polynomial certificates for inviscid self-similar transport.** This is `T`'s own
> no-branch. Do not re-enter by tuning `s`, the weight family, the split, or the border.

---

## 0. What was left, and why it was the last thing

Leg 53 put the four terms of the bordered certificate into one radii polynomial. It did not
close: with the block-diagonal approximate inverse the method requires,
`A = Γ⁻¹ ⊕ A_tail`, the coupling sub-block `Z₁[Γ←tail]` came out **43.15** at the best
split in the whole admissible sweep, against the **1** it must be under. Four of the five
degrees of freedom were then measured and banned — the weight exponent `s`, the weight
family, the split `K`, the border direction. **The fifth is the shape of `A`**, and the
block-diagonal shape is exactly what makes the coupling a term at all.

The novelty pass (`writeup/novelty/leg_54.md`, run and committed before any construction)
found the statement that makes this a real question rather than a complaint.
**arXiv:2411.18361** gives the convention explicitly: for `DF` a *compact perturbation of
the identity*, take `A = A^N + π^∞` — invert the Galerkin projection numerically and **let
the tail act as the identity**. So block-diagonal is the field's convention, not this
project's misreading of it, **and the hypothesis that buys it is precisely the one this
operator fails** (leg 51: the unbounded part is a shift, not a multiplier). Verdict
`PROCEED_NARROW`; nothing is banked as novel, since block Gauss–Seidel and Schur-complement
preconditioning are textbook (`10.1007/BF01385611`).

---

## 1. MM-1 — the mismatch as an inequality, and it is an equality

For any `A` written in blocks against the finite/tail split,

```
(I - A L)_{tail,Γ}  =  -(A21 G + A22 C),        C := L_{tail,Γ}
```

With `A21 = 0` and `A22 = A_tail` this is exactly `-A_tail C`, whose `(K+1)`-th row carries
the entry `1 - K/2` from mode `K`. Hence

```
Z₁  ≥  |1 - K/2| · (w_{K+1}/w_K) · ‖A_tail e_{K+1}‖_w / w_{K+1}
```

for **every** finite block — the sub-block contains no `Γ⁻¹`. Measured against the runner's
own data it is **not merely a bound but an equality**: the `(K+1)`-th column is the
maximising column, and `measured / RHS = 1.0000` at every `K` in both classes (max
deviation `MM1_max_ratio_deviation_from_one`). That is a strengthening worth having, and
VER-A found it independently.

**Its reach is limited, and the directive overstated it.** The prefactor `|1 − K/2|`
vanishes at `K = 2` and is small below `K = 6`:

| `K` | 2 | 4 | 6 | 8 | 16 | 32 | 64 |
|---|---|---|---|---|---|---|---|
| RHS, flat `s = 0` | 0.00000 | 0.99611 | 1.98835 | 2.97674 | 6.89231 | 14.54545 | 29.17647 |
| RHS, algebraic `s = 0.3` | 0.00000 | 1.38731 | 2.76244 | 4.12384 | 9.44094 | 19.55753 | 38.18210 |

**So MM-1 does not establish "no block-diagonal `A` can work for this operator".** It
establishes it for `K ≥ 6` (flat) and `K ≥ 4` (algebraic). Leg 53's sweep started at
`K = 4` and hid this; VER-A flagged it as GAP 1. The scope is stated with the restriction
attached, and the corner is closed separately, twice over — by §2 and by §4.

*Second factor.* `CONTINUATION_PROMPT.md` quotes the measured range as `0.94 … 1.33`. That
figure is not traceable to leg 53's shipped JSON. VER-A re-measured `0.9412 … 1.3873` over
`K = 4…64`; this leg quotes its own measured range from `MM1_second_factor_range`.

---

## 2. MM-1b — every odd split has a singular finite block

Sweeping `K = 3` to probe VER-A's hole raised `LinAlgError: Singular matrix`. Chasing it
rather than working around it:

**Every odd split is exactly singular**, in both classes, under both gauges, with and
without the far-field column. The smallest singular value of the augmented finite block is
at most `MM1b_max_smallest_sv_at_odd_K` at every odd `K ∈ {3,5,7,9,11}` and at least
`MM1b_min_smallest_sv_at_even_K` at every even `K ∈ {2,4,6,8}` — and without the far-field
column at `K = 3` it is **exactly `0.0`**, not merely small.

The reason is structural rather than numerical. The far-field kernel `ĥ` is supported on
**one parity chain** (modes `K+1, K+3, …`), and the linearisation couples mode `k` only to
`k ± 1`. At odd `K` the mode-`K` residual row therefore acquires **no entry on any of
`b_1…b_K` or `δc_ω`** and is carried entirely by the amplitude column.

**Consequence.** The split must be **even**, so the corner MM-1 leaves open is not
`{2, 3, 4}` but `{2}` in both classes plus `{4}` in the flat class alone — and §4's floor
covers both. *This removes candidate splits; it does not select one, so it is not the banned
re-entry by tuning `K`.* The fact is gated in `test_spectral_certificate.py` rather than
left in the runner, because it is a property of the operator.

---

## 3. MM-2 — the shape battery

Seven shapes of `A`, all on leg 53's assembled object, all measured as the **true column-max
of `I − A L` over the whole space** rather than as a sum of sub-block norms.

| shape | `A` | admissible |
|---|---|---|
| `block_diag` | `Γ⁻¹ ⊕ A_tail` — leg 53's baseline | yes |
| `gs_lower` | exact inverse of `[[G,0],[C,T]]` — block GS, `Γ` swept first | yes |
| `gs_upper` | exact inverse of `[[G,B],[0,T]]` — block GS, tail swept first | yes |
| `schur` | Schur complement of the coupling, `A_tail` for the tail solve | yes |
| `ff_lift` | block-diagonal plus a rank-one lift of the far field into the tail | yes |
| `oracle_pinv` | `A₁₂ = −A₁₁ B T⁺` — bounds what the best possible `A₁₂` could do | **no** |
| `exact_inv` | `A = (L_M)⁻¹` | **no** |

**`gs_lower` is worth exactly nothing, and the algebra says so before the run does.** For
`Λ = [[G,0],[C,T]]`,

```
I - Λ⁻¹L  =  [[0, -G⁻¹B], [0, T⁻¹CG⁻¹B]]
```

whose `(Γ,tail)` block is `−Γ⁻¹B` — **identical to the block-diagonal one**. Measured:
identical to five digits. That was a prediction that could have come out otherwise.

**`gs_upper` and `schur` do help, and the help is real but far too small.** The best
admissible shape anywhere in the sweep is recorded in `MM2_best_admissible`; the
block-diagonal baseline at its own best in `MM2_block_diagonal_baseline`; the ratio in
`MM2_improvement_over_block_diagonal`. Spending the last free choice buys a factor of
**~1.4** where a factor of **~45** was needed.

**Instrument check (lesson 85).** `block_diag` reproduces leg 53's sub-blocks exactly —
`Z₁[Γ←tail] = 43.151291`, `Z₁[tail←Γ] = 1.387315` — recorded in
`MM2_instrument_check_vs_leg53`.

### 3.1 A correction to leg 53, made in place

**The tail–tail sub-block was understated.** Leg 53 compared `A_tail` against the *bordered*
matrix it actually inverts and reported `6.0e−13`. But the assembled operator's tail–tail
block is the **bare** scaled tail `T`, which is singular; the `(u,v)` bordering is part of
the construction of `A`, not part of `L`. Charged correctly, `‖I − A_tail T‖ ≈ 2.2`.

This makes the block-diagonal baseline **worse, not better**, so leg 53's NO is unaffected.
It is recorded because it is the term `ff_lift` then removes, and it had to be visible
before that move made sense.

---

## 4. MM-4 — the floor no shape can cross

This is the part that generalises beyond the seven shapes tried. For a **completely general**
`A = [[A₁₁,A₁₂],[A₂₁,A₂₂]]`,

```
(I - A L)_{Γ,tail}  =  -(A₁₁ B + A₁₂ T)
```

The tail operator `T` is **singular** — its kernel is exactly the far-field direction `ĥ`
that leg 52 bordered. Applying that block to `ĥ`:

```
(I - A L)_{Γ,tail} ĥ  =  -A₁₁ B ĥ
```

**`A₁₂` has dropped out of the algebra.** The size of the coupling along the one direction
that matters is a property of `A₁₁` alone, and no choice of off-diagonal block can touch it.
The floor `‖Γ⁻¹ (L ĥ)‖_w / ‖ĥ‖_w` is tabulated in `MM4_floor` for every `K` including 2; its
smallest value over every class and split is `MM4_min_floor`, **an order of magnitude above
the 1 it must be under, at the most favourable split that exists.**

### 4.1 The identity's own caveat, measured rather than asserted

`ĥ` spans `ker T` for the **infinite** tail operator. On the **truncated** operator actually
computed, `T ĥ` is *not* exactly zero, and the writeup would be dishonest to claim otherwise —
a first draft of the gate in `test_spectral_certificate.py` asserted `‖T ĥ‖/‖ĥ‖ < 1e−12` and
**failed at `0.242`**, which is how this got measured properly.

What the defect actually is (`MM4b_kernel_truncation_defect`):

* it is supported on the **last mode alone**, at every `K` and `M` tried
  (`MM4b_defect_is_edge_only`) — a boundary effect of the truncation, not a failure of the
  kernel;
* its relative `ℓ¹` size **halves per doubling of `M`** (`MM4b_defect_halves_per_doubling`),
  i.e. it is `O(M⁻¹) → 0`;
* at the `M` used throughout this leg it is at most
  `MM4b_max_relative_defect_at_M_extra_1024` in relative terms, against a floor of `5.04`
  and above.

So the floor is a statement about the **infinite** operator which the computed one tracks to
a few percent — **not an exact algebraic zero being read off a float**, which is the failure
mode lesson 86 warns about. A couple of percent of slack, against a quantity that would have
to fall by a factor of five, does not move the conclusion. The gate now pins the *shape of the ladder* (edge-only,
`M⁻¹`) rather than an exact zero the truncation does not deliver.

`A₁₁` is not entirely free (`A₁₁G + A₁₂C = I`), so the freedom is **ablated rather than
assumed away**: recomputing the floor with the Schur complement's `A₁₁` changes it by at
most `MM4_max_A11_freedom_effect` in relative terms. The freedom is measured, and it is not
where the answer lives.

**Dually — and this is why the shape had to be non-block-diagonal at all —**

```
(I - A L)_{tail,tail} ĥ  =  ĥ - A₂₁ B ĥ
```

so the only way to control the tail on its own kernel is a **non-zero `A₂₁`**: the approximate
inverse must lift the far-field column back into the tail. `ff_lift` builds exactly that
rank-one lift (with `u` swept over four functionals, the best reported — the conservative
choice for a negative result). It **does** fix the tail–tail block, and it is swamped,
because by the identity above it cannot touch `(Γ,tail)`.

---

## 5. MM-3 — the admissibility audit, which is the actual experiment

**The gate as literally worded is trivially YES**: take `A = (L_M)⁻¹` and `‖I − A L_M‖`
drops to float noise (`~1e−9` in the battery). That number is a statement about
`numpy.linalg.inv`, not about the operator — lesson 86. What makes the gate a real question
is **admissibility**: an admissible `A` is finite rank plus an *explicit* operator on the
modes beyond it, because the tail is infinite and `Γ⁻¹` of an infinite block does not exist.

So the audit builds `A` at truncation `M_A`, extends it over modes `M_A+1 … M_L` by the only
explicit operator available (the bordered tail inverse of *that* sub-tail), and evaluates it
against `L` at `M_L > M_A`. Results in `MM3_admissibility_audit`:

* it does not merely fail to help — it is **orders of magnitude worse** than the
  block-diagonal baseline (`MM3_min_Z1_over_audit`);
* it **degrades as `M_A` grows** (`MM3_growth_per_doubling_of_M_A_*`);
* it is **essentially independent of `M_L`** — the `M_L = 1024` and `2048` rows agree to five
  digits.

That last pair is the tell. The cost does not live out in the tail; it lives at the **seam**
where the finite-rank part of `A` meets the explicit tail operator. **The exact inverse is
not a shape of `A`; it is the truncation.**

---

## 6. Controls

**MM-5, positive, and it can report the other answer.** Same code path with `Λ¹` dissipation,
unbordered tail, no far-field unknown — a dissipative tail has no kernel, so it needs no
far-field unknown, and bordering an already-invertible tail with its near-null pair is the
wrong operator. Run through **every** shape, not just the baseline. It reaches `Z₁ < 1`
(`MM5_control_can_report_below_one`, `MM5_min_mu_with_Z1_below_one`,
`MM5_shapes_that_reach_below_one`). The instrument can say yes; on this operator it does not.

**MM-5b, negative, and one of them did not behave.** The border direction is wired through
the amplitude column, so a wrong direction changes `Γ` itself and the control *can* fail
(lesson 90). It does, for `block_diag` and `gs_upper`: the second singular pair makes the
augmented block essentially singular and a random direction is orders of magnitude worse.

**It does not discriminate for the Schur shape.** With a random border, `schur`'s `Z₁` comes
out **smaller** than with the analytic border, across all six seeds tried
(`MM5b_shapes_where_a_wrong_border_is_BETTER`). The mechanism is visible in the numbers:
`S = G − B A_tail C` partly undoes whatever the border did to `Γ`, so the Schur shape is far
less border-sensitive than the block-diagonal one. That is a property of the shape, not a bug.

Two consequences, both stated rather than buried:

1. the border-direction control **licenses the negative result for `block_diag` and
   `gs_upper` but not for `schur`**, where the negative rests instead on the `μ`-dial
   positive control and on §4's floor;
2. the smallest `Z₁` anywhere in that table (`MM5b_min_Z1_over_every_border_and_shape`) is
   still well above 1, and chasing it would mean **tuning the border direction — banned**,
   and measured dead in leg 53.

---

## 7. The polynomial, and the ceiling

`MM6_polynomial` carries `Y₀`, `Z₁`, `Z₂` and the root for the best admissible shape at each
split. **No row has a positive interval**; `r_max = 0` throughout.

**The ceiling, pre-committed and unchanged.** This is the `a = 0` CLM object. `Y₀` is
**exactly zero** because the anchor **is** one basis mode — the degenerate reason banked as a
ban since leg 51 — so the polynomial's root `r = 0` is available for free and certifies
nothing. The reportable quantity is whether the inequality holds on a **positive** interval,
which needs `Z₁ < 1`, and it does not. **Nothing is claimed about `HL_S2_nonsymmetric`:** on
the gate's own terms that object is reached only if the polynomial closes here.

VER-A additionally records that `Y₀ = 0` is a hardcoded literal rather than an evaluated
float — so no float noise is being read as an exact zero — and that its justification checks
out independently in exact rational arithmetic.

---

## 8. What this establishes, and what it does not

**Establishes.** On the `a = 0` CLM object, in both admissible classes, under both gauges, at
every admissible (even) split from `K = 2` to `64`: **no shape of the approximate inverse
brings the assembled `Z₁` below 1.** The three natural non-block-diagonal shapes buy ~1.4×
where ~45× is needed; the unrestricted optimum is inadmissible and, made admissible, is
orders of magnitude worse; and underneath all of them sits a floor that is **independent of
the off-diagonal block of `A` by an algebraic identity**, not by exhaustion of cases.

**Does not establish.** That no *finite block* of any kind can close this. §4's floor is
shape-independent but **not** finite-block-independent — it contains `A₁₁`. MM-1 is
finite-block-independent but only bites for `K ≥ 6` / `K ≥ 4`. Neither argument alone is
universal, and this leg does not combine them into a claim that they do not support.

**And the honest ceiling.** No link of the `L1→L4` chain moved. Clay odds unchanged at
~0.05%. What closed here is a **method**, on a **toy object**: the `ℓ¹`-Fourier
radii-polynomial certificate is the wrong shape for an operator whose unbounded part is a
shift, and three legs of increasingly careful work now say so from three directions — leg 51
(the method wants a multiplier), leg 52 (bordering repairs invertibility, not size), leg 53
(the seam is the term that runs out), and this leg (and the seam cannot be moved by choosing
`A` differently).
