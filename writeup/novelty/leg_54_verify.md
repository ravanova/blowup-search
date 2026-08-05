# Leg 54 — VER-A: independent re-measurement of leg 53's headline, before MM builds on it

**Role.** VER-A, paired to leg 54 (Route-MM). This is lesson 85 applied: re-measure your own
headline before building a stage on it. I report gaps; I do not repair them, and I have not
touched leg 53's or leg 54's owned files.

**Artifacts.** `experiments/p2_route_mm_v1_headline_verify.py` (this pass's own runner, which
rebuilds the augmented block, the amplitude column and every sub-block norm from
`solver/spectral_certificate.py` primitives rather than importing leg 53's runner) and
`writeup/data/leg_54_verify_headline.json`.

---

## 0. Mechanical reproduction

`experiments/p2_route_tc_v1_assemble.py` re-run unmodified. Its output is **bit-for-bit
identical** to the committed `writeup/data/p2_route_tc_v1_assemble.json` — the only differing
field is `elapsed_s`. The JSON was restored with `git checkout` after the run.

---

## 1. What I independently CONFIRM, and to what precision

| headline | leg 53 | this pass | verdict |
|---|---|---|---|
| `Z₁[Γ←tail]` min over TC-8 ablation | 20.47 | 20.473399995961532 | confirmed, exact |
| `Z₁[Γ←tail]` at best split in sweep | 43.15 | 43.15129110858924 | confirmed, exact |
| `Z₁[tail←Γ]` min over the sweep `K = 4..64` | 0.9961 | 0.9961089494163415 | confirmed, exact |
| assembled `Z₁` at its minimum | 44.54 | 44.53860580010511 | confirmed, exact |
| positive control, assembled `Z₁` at `μ = 2` | 0.9156 | 0.9156 | confirmed |
| `‖Γ⁻¹‖` augmented | exactly `2(K²−1)` | rel. err ≤ 5.6e−16, `K = 4…64` | confirmed |
| `‖Γ⁻¹‖` dropping the amplitude column | exactly `4(K−1)` | **exact in rational arithmetic** | confirmed |

### 1.1 The two closed forms, re-derived rather than re-read

I rebuilt the augmented block myself and did not consult leg 53's derivation for the
attribution. Both closed forms hold to machine precision at `K = 4, 6, 8, 12, 16, 24, 32, 48,
64`, and the unaugmented one, `4(K−1)`, is **exact in `Fraction` arithmetic** (12, 28, 60, 124
at `K = 4, 8, 16, 32`) — so "exactly" is not a float coincidence, which is what lesson 86 asks.

**The attribution is right this time.** I computed which column of `Γ⁻¹` attains the norm:

* augmented → **column `K+1`, the amplitude column**, at every `K`. Its value *is* `2(K²−1)`;
  the mode-`K` column sits at `4(K−1)` beside it, unchanged.
* unaugmented → **column `K−1`, the mode-`K` residual row**, value `4(K−1)`.

So leg 53's *corrected* mechanism — the `K²` is created by the augmentation, and the coupling
contributes a factor `2` rather than `K/2` — is independently confirmed. The `K²` does **not**
come from the finite block's own back-recursion; the block without the amplitude column is
strictly linear in `K`.

### 1.2 The positive control is a real control in the dial that matters

The `μ` ladder is monotone and crosses 1 between `μ = 1` and `μ = 2`:

```
mu     0      0.05   0.1    0.25   0.5    1.0    2.0     4.0     8.0
Z1   556.0  201.6   98.7   13.68  3.616  1.636  0.9156  0.6348  0.5188   (algebraic s=0.3)
```

It can plainly report the other answer, and it does. Leg 53's **negative** control (the border
direction) is also genuinely wired now — I reproduce `Z₁[Γ←tail]` = 546.57 / 546.37 / 2.099e16
/ 6907.8 across the four border directions, i.e. four *different* numbers, so the lesson-90
repair took. (My own first draft of this verifier reintroduced exactly that bug by failing to
thread the amplitude direction into `Γ`; it is fixed, and the fix is commented in the script as
a warning.)

---

## 2. Gaps — things leg 54 should not consume as written

### GAP 1 (material). MM-1's inequality is vacuous at small `K`, and leg 53's sweep started at `K = 4`

The good news first: MM-1 is **stronger** than the directive claims. I measure

```
Z₁[tail←Γ]  =  |1 − K/2| · (w_{K+1}/w_K) · ‖A_tail e_{K+1}‖_w / w_{K+1}
```

as an **equality**, not merely a lower bound, at every `K ≥ 3` in both admissible classes — the
`b_K` column is exactly the argmax column of that sub-block. Leg 54 can use the equality.

The problem is the prefactor. `|1 − K/2|` vanishes at `K = 2` and is small below `K = 5`:

| `K` | 2 | 3 | 4 | 5 | 6 | 8 | 16 | 32 | 64 |
|---|---|---|---|---|---|---|---|---|---|
| `|1 − K/2|` | **0** | 0.5 | 1.0 | 1.5 | 2.0 | 3.0 | 7.0 | 15.0 | 31.0 |
| RHS, flat `s = 0` | 0.0000 | 0.4985 | **0.9961** | 1.4927 | 1.9883 | 2.9767 | 6.8923 | 14.5455 | 29.1765 |
| RHS, algebraic `s = 0.3` | 0.0000 | 0.6949 | 1.3873 | 2.0766 | 2.7624 | 4.1238 | 9.4409 | 19.5575 | 38.1821 |

**MM-1's RHS exceeds 1 only for `K ≥ 5` (flat) and `K ≥ 4` (algebraic).** At `K = 2` it is
identically zero and the statement is empty. Nothing in the code makes `K = 2, 3` inadmissible
— I ran them and they are fine — so the directive's reading of MM-1 as *"a statement that no
block-diagonal `A` can work for this operator"* **is not established as written**: it leaves
`K ∈ {2, 3, 4}` open.

This is not cosmetic. Closure at `K ≤ 4` is still blocked in practice, but only by
`Z₁[Γ←tail]` (59.0 at `K = 4` flat, 43.15 at `K = 4` algebraic) — which is precisely the
sub-block that **contains `Γ⁻¹`**, and which MM-1 exists in order not to depend on. The
finite-block-independent argument therefore has a genuine hole at small `K`.

Two repairs are available and both are leg 54's call: state MM-1 with the `K ≥ 5` restriction
and close `K ∈ {2,3,4}` by a separate finite exhaustive argument, or find a second
finite-block-independent column carrying no `|1 − K/2|` prefactor.

### GAP 2 (minor, numeric). The second factor's range is 0.94 … **1.39**, not 0.94 … 1.33

The directive quotes the measured second factor as **0.94 … 1.33**. I measure

* **0.9412 … 1.3873** over leg 53's own sweep (`K = 4…64`, both classes),
* **0.9412 … 1.3913** over `K = 2…64`.

The maximum sits at `K = 4`, `s = 0.3`. The quantity is also not present anywhere in leg 53's
shipped JSON, so the quoted `1.33` is not traceable to the artifact. The error is conservative
(a larger second factor makes MM-1's RHS larger), but if leg 54 quotes the range it should
quote **0.94 … 1.39**.

### GAP 3 (scope). The closed forms are a flat-class, null-gauge statement

`2(K²−1)` and `4(K−1)` are exact **only** in the flat class with the pinned-`e₂` gauge. Off
that corner:

| | `K = 4` | `K = 16` | `K = 64` |
|---|---|---|---|
| flat, null (÷ `2(K²−1)`) | 1.0000 | 1.0000 | 1.0000 |
| flat, dilation | 1.7755 | 1.7769 | 1.7826 |
| algebraic `s = 0.3`, null | 0.7559 | 0.5437 | 0.3682 |
| algebraic `s = 0.3`, dilation | 1.3858 | 0.9976 | 0.6778 |

The dilation gauge is a clean `≈ 1.78×` factor, so `K²` survives there. In the algebraic class
the ratio drifts downward — the growth is closer to `K^1.8` than `K²`. The tidy closed form is
real but it is one cell of a four-cell table, and the directive states it unqualified.

### GAP 4 (executability, not arithmetic). `Y₀ = 0` is a literal, not a measurement

`Y₀` is never evaluated. It is the literal `0.0` in `solver/spectral_certificate.py`'s
`rigorous_finite_block`, and the literal `0.0` again at the polynomial in TC-2; TC-3's
`matching_row_residual_at_anchor` is likewise a hardcoded `0.0`. So there is **no float noise
being read as an exact zero** — lesson 86 is not violated, because no float is involved.

I checked the justification independently and **it holds**: `clm_residual_exact(K=8)` returns
all-zero in exact rational arithmetic (18 of 18 entries), and the anchor's tail coefficients on
modes `K+1…M` are identically zero, which is why the matching row's residual is zero for the
same structural reason. The banked degenerate reason — the anchor **is** one basis mode — is
correct.

What is missing is lesson 68: the identity is asserted at the point of use rather than checked
there, so nothing in the runner would notice if the anchor ever changed. This is a
one-line-assert gap, not a wrong number, and I flag it only because leg 54 consumes `Y₀ = 0`
as an input.

### GAP 5 (framing). "Minimum over the sweep" is right; "minimum" is not

`Z₁[tail←Γ] = 0.9961` is confirmed as the minimum over **leg 53's sweep** (`K = 4…64`, both
classes, both gauges) — and it is not a single favourable point: I reproduced the whole ladder
at `K = 2, 3, 4, 5, 6, 8, 12, 16, 24, 32, 48, 64` and the value is monotone in `K` and
identical under both gauges (correct, since neither `L_{tail←Γ}` nor `A_tail` sees the gauge
row). But extending below the sweep gives **0.4985 at `K = 3`** and **0.0006 at `K = 2`**. Any
sentence of the form "its minimum is 0.9961" needs the `K ≥ 4` qualifier. This is the same
underlying fact as GAP 1.

### Note on the positive control's one dial

At `μ > 0` the runner hard-wires `border=None` and `far_field=False`, so the border direction
cannot reach the positive control at all — it is border-independent *by construction*. That is
defensible on its own terms (a dissipative tail has no kernel, so it needs no far-field
unknown, and leg 53's writeup says so explicitly). But it means the `μ > 0` path differs from
the `μ = 0` path in **three** ways at once — dissipation, border, far-field column — so the
control certifies that *the instrument* can say yes, not that the mechanism was ablated. It is
not a lesson-90 tautology, because `μ` is a real dial and the answer moves across it; I record
it as a scope note rather than a gap.

---

## 3. Bottom line for leg 54

Four of the five headline numbers are confirmed to full printed precision and both closed forms
are confirmed exactly, one of them in rational arithmetic. The mechanism attribution leg 53's
own verifier corrected — `K²` from the augmentation, factor `2` not `K/2` — is independently
confirmed by column attribution.

**The one thing leg 54 must not consume as written is MM-1's claim to cover every block-diagonal
`A`.** It covers `K ≥ 5`. The inequality is an equality there, which is a strengthening worth
having; the small-`K` corner needs its own argument.
