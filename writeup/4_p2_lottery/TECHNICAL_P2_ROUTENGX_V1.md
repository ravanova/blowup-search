# Route-NGX v1 — the general class `A₂₁ ≠ 0`, decided: `Z₁ ≥ 1` for every bounded `A`

**Leg 127 (exploration, reserve). Gate answer: YES, (i).** Data:
`writeup/data/p2_route_ngx_v1_general.json`. Runner:
`experiments/p2_route_ngx_v1_general.py`. Figure: `fig63_route_ngx_v1_general.png`, rebuilt
from the curated JSON alone by `experiments/p2_route_ngx_v1_general_evidence.py`. Novelty
pass: `writeup/novelty/leg_127.md`, run and committed **before** any construction. Module
additions are append-only in `solver/spectral_certificate.py`; gates 32–37 in
`test_spectral_certificate.py` (37/37 pass).

> **Gate, in its pre-committed wording.** *Can the no-go be DECIDED on the full bounded class
> — either (i) a proof that `Z₁ ≥ 1` for every bounded `A` (`A₂₁` free) at some `s < 1`, with
> hypotheses containing the `a = 0` CLM linearization, or (ii) an explicit admissible `A` with
> `A₂₁ ≠ 0` and measured `Z₁ < 1`, grid-stable over ≥ 3 resolutions?* — **YES, (i).** The
> yes-(i) branch fires: *the theorem reaches its sharp form. Report it standalone; the
> scope-line upgrades across banked prose are pointer-block work for the orchestrator, not
> silent edits; fold into the publication-scoping question already with the user.*

> **THE SCOPE LINE IS LOAD-BEARING AND IT IS NEW.**
> [arXiv:2607.19762](https://arxiv.org/abs/2607.19762) (Xu, 2026), which post-dates leg 58's
> novelty pass, proves the **same** `a = 0` CLM linearisation is **invertible on origin-`H²`**
> after the standard modulation, with a spectral gap of `1/2`. Everything below is therefore a
> statement about the **`ℓ¹_w` realization at `s < 1`** and about nothing else. No sentence in
> this leg says the operator "has no bounded approximate inverse".

---

## 0. What was open

Leg 58 proved `Z₁ ≥ 1` on the class `A₂₁ = 0` by evaluating `I − A L` on `x = (0; h)`, where
`h` is the tail block's far-field kernel (`T h = 0`, `h_m ∼ m⁻²`, hence `h ∈ ℓ¹_w` iff
`s < 1`). Then

```
(I − A L)(0; h) = ( −(A₁₁B + A₁₂T)h ;  h − A₂₁Bh − A₂₂Th )
```

and `T h = 0` kills the `A₁₂` and `A₂₂` terms, leaving `‖A₁₁Bh‖ + ‖h‖ ≥ ‖h‖`. The argument
stops at `A₂₁ ≠ 0` because `h − A₂₁Bh` becomes cancellable. For that class the repository had
leg 54's battery only: seven shapes, best admissible `Z₁ = 8.9591` against a block-diagonal
baseline of `10.4584`, and MM4c's rank-one construction driving the `ĥ`-column floor to
`≈ 10⁻¹⁶` at a total `Z₁` of `5.66 × 10⁵`.

## 1. The pre-registered argument, carried out, and refuted (lesson 76)

`DIRECTION.md` pre-registered a **two-direction** argument: pair `x = (0; h)` with the
finite-block directions `A₂₁` populates. Carried out, it reads as follows. For `x = (z; 0)`
with `z_K = 0` the coupling `C z` vanishes (`C` is rank one and sees only `z_K`), so the
tail-row component of `(I − A L)x` is exactly `−A₂₁ L₁₁ z`, uncancellable. Writing
`‖h − A₂₁Bh‖ = θ‖h‖` and optimising over `θ` gives

```
Z₁  ≥  max( θ , (1−θ)/η )  ≥  1/(1+η),        η = ‖G⁻¹Bh‖_w / ‖h‖_w.
```

Measured at `K = 4`, `s = 0.3` (JSON `NGX3_explicit_sequence`, `finite_correction_norm`,
against a unit-normalised `h`): `η = 14.45 → 13.66` across `M − K = 128 … 2048`, i.e. it
converges to `≈ 13.7` rather than decaying. The bound is therefore `Z₁ ≥ 0.068`, which is
vacuous. **The pre-registered route does not close, and it is recorded here rather than
deleted.**

## 2. The argument that does close, and it has no blocks in it

For every `x`, `‖x‖_w ≤ ‖(I − A L)x‖_w + ‖A‖_w‖Lx‖_w`. Dividing by `‖x‖_w` and minimising:

> **(T1)** For every bounded `A`: `Z₁ ≥ 1 − ‖A‖_w · σ_min(L)`, where
> `σ_min(L) := inf_{x≠0} ‖Lx‖_w/‖x‖_w = 1/‖L⁻¹‖_w`.

`A` is never decomposed, so `A₂₁` never appears and there is no corner in which the argument
can stop. **(T1) is folklore and is NOT claimed** — it is the contrapositive-with-remainder of
the `Z₁ < 1 ⟹ invertible` hypothesis stated in arXiv:1503.06315, arXiv:2505.03091 and
arXiv:2411.18361. The novelty pass established this before construction and forbade the claim.
What this leg contributes is which side of (T1) the operator's `ℓ¹_w` realization falls on.

**(T1) is sharp, not lossy.** Taking `A = L⁻¹` gives `Z₁ = 0` and `‖A‖_w = 1/σ_min` exactly,
so the right-hand side is `0` and the slack is `0`. Measured over the exact-inverse checks:
max slack `1.24 × 10⁻⁸` (`NGX1_max_slack_at_the_exact_inverse`). A bound that is attained does
not leak, which is why the conclusion below carries no hidden constant.

## 3. The operator is not bounded below in `ℓ¹_w` at `s < 1`

`σ_min(L)` for the assembled bordered object (leg 53's assembly, leg 54's single-matrix form),
fitted as `σ_min ∼ M^{−p}` over `M − K = 128 … 2048`:

| `s` | class | fitted `p` (`K = 4`) | predicted `1 − s` |
|---|---|---|---|
| 0.0 | flat | **0.9925** | 1.00 |
| 0.3 | algebraic | **0.6985** | 0.70 |
| 0.7 | algebraic | **0.3202** | 0.30 |
| 1.0 | algebraic | 0.0788 | 0.00 |
| 1.5 | algebraic | 0.5000 | — (different mechanism, §6) |

Max deviation from `1 − s` over all `s < 1` and all `K ∈ {2, 4, 8}`: **0.0219**. The relative
spread of `σ_min` across `K` at the top of the ladder is **0.29%** for `s < 1`: the divergence
is a property of the **tail**, not of where the split is placed, which is why no choice of
finite block escapes it.

### 3.1 The sequence is constructed, not found (lesson 86)

`explicit_far_field_direction` builds `v_M = (z_M ; h^{(M)})` with `h^{(M)}` the analytic tail
kernel and `G z_M = −B h^{(M)}`. Measured against the numerically-optimal direction from
`l1_bounded_below_constant`:

- ratio to the numerical optimum: **1.0000000000045** (max over the ladder);
- cosine with the numerical optimum: **0.9999999999999998**;
- finite-block residual of `L v`: at most `1.22 × 10⁻¹⁴` over every class and `M` (float zero);
- **`z_K = 0.0` exactly**, by the parity of the kernel recursion — this switches off the sole
  finite-to-tail coupling entry `(1 − K/2)`;
- rows carrying the residual of `L v`: **1**, the truncation edge `m = M`.

The rate then follows analytically: the edge row has size `|1 − M/2|·|h_M|·w_M ∼ M^{s−1}`
(gate 35 measures the exponent as `−0.6942` against a predicted `−0.70`), while
`‖v_M‖_w` is bounded because `Σ m^{s−2}` converges for `s < 1` (gate 34: the norm rises 5.4%
over an 8× range of `M` with shrinking increments, against a 2.83× growth at `s = 1.5` on the
identical vector).

### 3.2 It is not a truncation artifact (leg 58's NG2c, re-aimed)

The referee objection: *the near-null vector is an artifact of stopping at `M`.* Test: zero-pad
the `M`-optimal direction into truncations `2M` and `4M` and re-measure. Max degradation over
the audit: **1.3543×** — bounded, not a return to `O(1)` — and the embedded ratios continue
falling along the ladder at the same rate.

## 4. The theorem

> **Theorem NGX.** Let `X = ℓ¹_w` with `w_k = (1+k)^s`, `s < 1`, and let `L` be the assembled
> bordered `a = 0` CLM steady linearisation in the compactified odd-sine coefficient basis,
> split at mode `K`, with `μ = 0`. Let `A` be any **bounded** operator on `X` — admissible in
> leg 54's MM3 sense, i.e. the truncation of one fixed bounded operator, so that `‖A‖_w` is
> uniform in `M` — with `A₂₁` **completely free** and `A₁₁, A₁₂, A₂₂` arbitrary. Then
>
> ```
> Z₁ = ‖I − A L‖_w  ≥  1.
> ```
>
> Quantitatively at truncation `M`: `Z₁ ≥ 1 − ‖A‖_w · σ_min(L_M)` with
> `σ_min(L_M) = c_s M^{−(1−s)} → 0`.
>
> *Proof.* (1) (T1), folklore. (2) `σ_min(L) = 0`, witnessed by the explicit sequence of §3.1.
> ∎

This **supersedes** leg 58's `A₂₁ = 0` theorem (that class is the special case `A₂₁ = 0`) and
**retires** leg 54's *"measured, not proved"* scope line for this operator in this space.

## 5. The consequence, as a magnitude (NGX6)

Any `A` reaching `Z₁ ≤ 1 − δ` needs `‖A‖_w ≥ δ/σ_min(L_M) ∼ δ·M^{1−s}`. Measured floors at
`s = 0.3`, target `Z₁ = 0.99`: **1.555 → 10.778** across `M − K = 128 … 2048`; growth per
doubling **1.99×** (flat) and **1.62×** (`s = 0.3`), i.e. exactly `2^{1−s}`.

**The honest reading.** At any *fixed* `M` the floor is finite and modest, so a finite-`M`
counterexample is **not** excluded — and leg 54 already exhibited one, `exact_inv`, whose
`‖A‖_w` equals `1/σ_min` to the printed digits (`662.58` at `M − K = 1024`, `s = 0.3`). That
is precisely why MM3 ruled it inadmissible. What Theorem NGX excludes is a **single bounded
`A` working uniformly in `M`**, which is the only sense the radii-polynomial method has.

Cross-check against leg 54's banked battery: **196/196** rows satisfy (T1); minimum slack
`7.73 × 10⁻¹⁰`, attained at `exact_inv` (`K = 64`, `s = 0.3`), where the bound is tight.

## 6. Controls, both able to report the other answer (lesson 90)

**Positive control, `μ > 0`.** Dissipation gives the tail a diagonal and destroys the kernel.
`σ_min` then **saturates**: fitted exponent `≤ 2.62 × 10⁻³` in absolute value across every
`μ > 0` and both arms, against **0.6985** at `μ = 0` in the same code path.

**Second control, the `s`-scan.** The exponent must vanish at `s = 1`, where the kernel leaves
`ℓ¹_w`. It does (`0.079`, consistent with a logarithm rather than a power). At `s = 1.5`
`σ_min` diverges **again**, at exponent `0.500` — but that is the **cokernel** side of
`fredholm_sides` (the dual functional entering the space), a *different* mechanism, and it is
reported separately rather than folded in (lesson 75). Note also that the `K`-spread jumps from
0.29% (`s < 1`) to **2.14** at `s = 1.5`: the second obstruction lives at the split, the first
does not. Two mechanisms, two `K`-sensitivities.

**A coincidence that had to be interrogated.** At `μ = 0` the bordered and unbordered objects
give `σ_min` identical to `5.7 × 10⁻¹⁵` relative. Lesson 90 says identical numbers are a bug
until proven otherwise, so the same two arms were compared at `μ = 0.1`, where they differ by
`6.1 × 10⁻²` relative — the code path does distinguish them. The `μ = 0` coincidence is
therefore a **finding**: the singular sequence has exactly zero far-field-amplitude component,
so bordering with that amplitude — leg 52's repair, the entire purpose of the assembled object
— does not move the obstruction at all. This independently re-answers NG2c's split-placement
objection in the general class: **the wall is not where the far-field unknown is put.**

## 7. What this is a statement about — and what it is not

Xu (arXiv:2607.19762) proves this operator is invertible on origin-`H²` after modulation, with
a spectral gap of `1/2`; our gauge row performs exactly that modulation (the dilation zero mode
is exactly `e₂`, gated). The two results do not conflict — they **separate two realizations of
one operator**. The content of Theorem NGX is therefore:

> The obstruction is a property of the **certificate's space**, not of the `a = 0` CLM
> linearisation. The radii-polynomial method needs weighted `ℓ¹` of Fourier coefficients in
> order to control its tail; in that space, at every `s < 1`, this operator is not bounded
> below, and no bounded approximate inverse exists at all — let alone a good one.

And the space is squeezed from both sides: at `s < 1` the kernel is in the space; at `s ≥ 1`
the cokernel functional is in the dual; and `s = 1`, the one exponent where `σ_min` does not
vanish, is exactly where the target object has infinite `ℓ¹_w` norm (leg 51's finding, leg 55's
measurement) and where leg 52 measured the bordering repair failing.

## 8. Ceiling (pre-committed, NGX7)

The object is the `a = 0` CLM linearisation. `Y₀` is **exactly zero** because the anchor *is*
one basis mode, so the radii polynomial's root `r = 0` is available for a degenerate reason and
certifies nothing. **No dynamics were run.** Nothing is claimed about `HL_S2_nonsymmetric`;
**no link of the `L1 → L4` chain moved**, here or in 127 legs. A wall measured on this object
bounds the real target's difficulty **from below**, not from above. Nothing here lifts any ban
in `plan_of_record.py`, and Xu's own route to a computer-assisted proof (large-imaginary-part
resolvent bounds, trace-ideal membership, quadrature error in trace norm) is a different method
from this lane and is not a lift condition for any of them.
