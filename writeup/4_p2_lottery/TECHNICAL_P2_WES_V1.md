# TECHNICAL — Route-WES v1 (leg 178): the zero-width window is a property of the TRIAL SPACE, and the gate answers YES under the user's 2026-08-07 ruling

Runner `experiments/p2_route_wes_v1_space.py`; evidence
`experiments/p2_route_wes_v1_space_evidence.py`; data
`writeup/data/p2_route_wes_v1_space.json`; figure
`writeup/figures/fig66_route_wes_v1_space.png` (`fig66`); module
`solver/energy_coercivity.py` (append-only, leg 111's functions untouched); novelty pass
`writeup/novelty/leg_178.md` (committed at `0ed6bde`, **before** the module was appended to and
before any number existed); journal `experiments/journal/leg_178.md`.
Every number below is in the JSON and is re-derived from it by the evidence script.

**Nothing is claimed that is not a measurement.** The construction (a singular-weight energy
estimate on a trial space constrained at the origin), the weight, and the constant `−1/2` are
Elgindi–Ghoul–Masmoudi's, [arXiv:1906.05811](https://arxiv.org/abs/1906.05811) Prop. 2.1; the
realization dichotomy and the ceiling `1/2` are Xu's,
[arXiv:2607.19762](https://arxiv.org/abs/2607.19762) §3.1 Prop. 2. This leg contributes the
*number on this repository's instrument*, and its novelty pass says so in advance and in as many
words: *"The `−1/2` is theirs. Reproducing it numerically is not a new theorem."*

---

## 0. The gate, its answer, and who decided it

> "For at least one pre-named alternative weighted-energy construction (different from leg
> 111's), is the measured coercivity gap positive and grid-stable across two refinements,
> outside the `γ > 3`-needs / `γ < 3`-exists coincidence?"
>
> **yes** → The zero-width window is a construction artifact, not an operator fact — a genuine
> third-realization revival. ESCALATE to the user; do not build further under this leg's own
> authority.
> **no** → The coincidence persists under a second, independently-chosen construction. Bank it.

| reading | answer |
|---|---|
| the gate's **literal wording** | **YES** |
| the leg's own §7 **five-clause predicate, unscoped** | **NO — 0 of 44 rows** |
| **the gate as ruled, 2026-08-07** | **YES** |

The two readings disagreed and **the leg refused to break its own tie**, taking the YES branch's
*action* (escalate, do not build, do not land) as the one safe under both readings. **The tie was
broken by the user on 2026-08-07, not by this leg** — §7 below carries the ruling verbatim and
the arithmetic it rests on. The leg's refusal is preserved in `experiments/journal/leg_178.md`
rather than deleted.

The JSON's `gate_answer.answer` field still reads **`"NO"`**, deliberately: it is the predicate
as the runner computed it, unscoped. The ruling scopes how clause 3 is *read*; it does not
rewrite what was measured. **The prose is the authority on the gate answer; the JSON is the
authority on the numbers.**

---

## 1. The object, and the arithmetic that made the window close

`solver/energy_coercivity.py` (leg 111, Route-WE) carries the weighted-`L²` coercivity form of
the **`a = 0` CLM linearisation** — the same operator the other two `L1` realizations died on;
its coefficient matrix is exactly equal (`0.0`) to
`spectral_certificate.bordered_linearization`'s interior block. The gap is
`−sup ⟨L h, h⟩_φ / ‖h‖²_φ`, solved as a generalized symmetric eigenproblem with explicit
whitening, and the damping factor is closed-form
`D_φ = (3/2) cos θ + (1/2) sin θ (log φ)′`.

Two thresholds govern, and leg 111 met them at the same place:

- **damping** at the origin requires `γ > 3`;
- **membership** of the trial functions in `L²_φ` requires `γ < 2p + 1`, with `p` the vanishing
  order at `θ = 0`.

Leg 111 held the trial space at `span{sin kθ}`, where `p = 1`, so `2p + 1 = 3` — *the same
number*. Window `(3, 3)`, **width `0.0`**, and every admissible member had a negative gap
converging to `−(3 − γ)/2`.

**Leg 111 swept the weight and held the space fixed. This leg moves the space.** Its runner
never edits leg 111's functions — control C1 below is the receipt.

---

## 2. Axis 1, the trial space: pre-named, and the vanishing order MEASURED

All four classes are subspaces of `span{sin kθ : k = 1..N}`, cut out by functionals that are
exact in closed form in this basis, since `(sin kθ)′(0) = k` and `H(sin kθ)(0) = −1 + (−1)ᵏ`:

| class | constraint on `c` | `h′(0)` | `H h(0)` | measured `p` (log-log slope) | declared `p` | admissible `γ` |
|---|---|---|---|---|---|---|
| `T0_unconstrained` | none | `1.0` | `−2.0` | **`0.9999999283`** | 1 | `< 3` |
| `T1_dprime` | `Σ k c_k = 0` | `0.0` | `−4.0` | **`2.9999998932`** | 3 | `< 7` |
| `T2_egm` | that **and** `Σ_{k odd} c_k = 0` | `0.0` | `0.0` | **`2.9999997484`** | 3 | `< 7` |
| `T3_hilbert_only` | `Σ_{k odd} c_k = 0` | `−2.0` | `0.0` | **`0.9999990684`** | 1 | `< 3` |

The order is measured from each class's probe over `θ ∈ {1e−2, 1e−3, 1e−4}`, not asserted.
`T2_egm` is the class carrying **both** EGM hypotheses; `T1_dprime` carries only `f′(0) = 0`.

**Odd trigonometric polynomials vanish to odd order only**, so leg 165's exponent-counted
`p = 2` (window width `2.0`) is unattainable here; `T1`/`T2` land at `p = 3` and the window is
`(3, 7)`, **width `4.0`**. This was registered in the novelty log before the run so it could not
be presented afterwards as a strengthening.

---

## 3. Axis 2, the weight: eleven members, and P0's exact identity

Family `A` (`φ = (2 sin(θ/2))^{−γ}`) at `γ ∈ {0, 2, 3, 4, 5, 6, 7}`; family `B`
(`φ = (2 sin(θ/2))^{−γ} (2 cos(θ/2))^{−2}`) at `γ ∈ {0, 2, 4}`; and `E_egm`, EGM's own
`(1 + X²)²/X⁴` transported through `X = tan(θ/2)`, `dX = ((1 + X²)/2) dθ`, evaluated from its
own closed form and **not** from family `B`'s.

**P0 — predicted before the run, and it held.** `φ^E / φ^{B4}` is the constant `32`:

| quantity | value |
|---|---|
| `ratio_min` | `31.99999999999997` |
| `ratio_max` | `32.000000000000036` |
| relative spread | **`1.9984e−15`** |
| `|ratio − 32|` | **`3.5527e−14`** |
| quadrature points | `2024` |

**EGM's published weight IS leg 111's family `B` at `γ = 4`** — the one member leg 111's
seven-weight enumeration excluded (`B` stopped at `γ = 2`, `A` at `γ = 4`). That is a statement
about an enumeration, not a new weight class, and the novelty pass pre-registered it as a
prediction *"so the run can refute it."*

**And it is the weight that makes the damping constant.** `D_φ ≡ −1/2` identically in `θ`, max
deviation **`2.220e−16`** (`B4_egm`) and **`4.441e−16`** (`E_egm`), against **`1.000e+00`** for
`A4_chen_hou`. That is the arithmetic reason EGM's constant is exactly `−1/2`.

---

## 4. The instrument finding: assemble-then-project is INVALID here, by `1.033e−01` on a quantity whose value is `0.5`

At `γ > 3` the *unconstrained* Gram's own entries are divergent
(`∫ sin jθ sin kθ θ^{−γ} ~ jk ∫ θ^{2−γ}`), growing by `1.677722e+07` per grading refinement.
Restricting **after** assembly computes the constrained form as a cancellation between divergent
numbers, and an SVD null-space basis satisfies its constraint only to `~1e−14`, a leak that
divergence then amplifies. Measured at `γ = 4`:

| | `T1_dprime` | `T2_egm` |
|---|---|---|
| constraint residual, exact basis | **`0.0`** | **`0.0`** |
| constraint residual, SVD basis | `1.4211e−14` | `1.7319e−14` |
| gap, assemble-then-project | `−5.7672900593` | `+0.3967415295` |
| gap, exact basis | `−5.7783387134` | **`+0.4999999999786626`** |
| absolute difference | `1.1049e−02` | **`1.0326e−01`** |

**The artifact understates the `T2` gap by 21%.** The repair is an integer-coefficient basis
whose constraint residual is *exactly* zero in float64 — `v_j = (j+1)e_j − j e_{j+1}` for `T1`,
`w_m = u_{m+1}v_m − u_m v_{m+1}` for `T2` — contracted against the basis functions **pointwise**
before any weight is applied, so the cancellation happens at scale `ε·K·θ` rather than at the
scale of a divergent integral. Lesson 86, caught by an instrument built for a different purpose.
**Every gate-answering number in this document is from the exactly-constrained basis.**

---

## 5. The measurements

### 5.1 `T2_egm`, the EGM class — gap ladder at `n = 32, 64, 128, 256`, `μ = 0` exactly

| weight | `γ` | ladder | reading |
|---|---|---|---|
| `A2` | 2 | `−0.481895 −0.495329 −0.498814 −0.499701` | negative — below the damping threshold |
| `A3` | 3 | `+0.013421 +0.004064 +0.001210 +0.000355` | **collapsing**, last relative step `0.707` |
| `A4_chen_hou` | 4 | `+0.502412 +0.500603 +0.500151 +0.500038` | positive, grid-stable; **fails the ceiling clause by `3.765e−05`** |
| `A5` | 5 | `+0.869083 +0.868438 +0.904082 +0.894630` | **above Xu's ceiling `0.5`** — instrument, contamination `4.0e−07` |
| `A6` | 6 | `−11.2 … −78356.4` | contaminated, `1.2e+05` |
| `A7` | 7 | `−1994.8 … −94793.5` | contaminated, `3.2e+15` |
| `B4_egm` | 4 | `+0.500000 +0.500000 +0.500000 +0.499993` | contamination `4.13e−17` |
| **`E_egm`** | 4 | **`+0.500000 +0.500000 +0.500000 +0.499999667`** | contamination **`4.126e−17`** — **the gate-answering row** |

`A4` approaching `0.5` **from above** is not a defect: a Galerkin Rayleigh quotient over nested
subspaces is an upper bound on the limit, so it must. The pre-committed ceiling clause
(`gap ≤ 0.5 + 1e−9`) is strict enough to fail it by `3.765e−05`; `B4`/`E` pass it exactly because
their `D_φ` is constant. **`A5`'s `+0.894630` exceeding the published ceiling is the known-answer
window (lesson 84) firing as designed**, and the contamination diagnostic flags it ten orders of
magnitude above the clean rows — the two instruments agree on which rows are trustworthy.

### 5.2 The gate-answering row, in full

`T2_egm | E_egm`, `γ = 4`, `μ = 0`:

| quantity | value | clause |
|---|---|---|
| gap at `n = 256` | **`+0.49999966748322944`** | 1 positive — **PASS** |
| relative steps, last two refinements | **`5.8904e−07`**, **`7.4090e−08`** (tol `5e−2`) | 2 grid-stable — **PASS** |
| quadrature spread, contamination `< 1` depths | **`2.2839e−07`** (tol `1e−3`) | 3 quadrature-stable — **PASS as ruled** |
| quadrature spread, all four depths | `4.0349e+00` | 3 unscoped — fail |
| admissibility ratio | **`1.000000`** (tol `1e−6` of `1`) | 4 admissible — **PASS** |
| exponent margin `2p + 1 − γ` | **`+3.0`** | 4 — **PASS** |
| ceiling | `0.49999967 ≤ 0.5 + 1e−9` | 5 under ceiling — **PASS** |
| local half of the form | `+0.49999966748322916` | — |
| nonlocal Hilbert half | **`−1.3966e−14`** | — |
| integration-by-parts residual | `1.4482e−14` | — |
| contamination at `n = 256` | `4.1260e−17` | — |
| `cond(G)` at `n = 256` | `2.5542e+11` | — |

### 5.3 Against leg 111, the same instrument, one axis moved

| | leg 111 (`T0`, `p = 1`) | leg 178 (`T2_egm`, `p = 3`) |
|---|---|---|
| window vs `γ > 3` | `(3, 3)` — **width `0.0`** | `(3, 7)` — **width `4.0`** |
| admissibility ratio per refinement at `γ = 4` | **`1.677722e+07`** divergent | **`1.000000`** convergent |
| exponent margin at `γ = 4` | **`−1.0`** | **`+3.0`** |
| largest admissible gap | **`−0.4999241`** | **`+0.499999667`** |

**The coincidence does not persist.** It was a property of `p = 1`, not of the operator.

### 5.4 The other three classes

- **`T1_dprime`** — every gap `≤ −1` (`E_egm`: `−5.778 −8.160 −11.500 −16.205`). **Required**:
  its point-mode intersection has **dimension 1**, so Xu's published eigenvalue `1` lives in the
  trial space and forces `gap ≤ −1`. An internal consistency check, not a defect.
- **`T2_egm`** — point-mode intersection **dimension 0** (singular values `3.2361`, `1.2361`):
  the two origin constraints annihilate `span{sin θ, sin 2θ}` exactly, so **the origin
  constraints ARE the modulation** and `modulate=True`/`False` must agree. This is **this leg's
  own arithmetic** (prediction P5) — the run-time fetch of Xu confirmed §3.2 attributes mode
  removal to *centering*, a different mechanism, and does **not** state this.
- **`T3_hilbert_only`**, the falsification control — inadmissible at every `γ > 3` (ratio
  `1.677722e+07`, margin `−1.0`), **`0` passing rows**. A class that removes a direction without
  changing the vanishing order does not open the window, so the instrument is measuring the
  *space*, not dimension reduction.

---

## 6. Controls, all four, with magnitudes

- **C1 (reproduction).** Leg 111's four banked `n = 256` gaps reproduce through the untouched
  path: `A0 −1.499886` → `−1.4998861652` (`1.652e−07`), `A2 −0.499924` → `−0.4999241101`
  (`1.101e−07`), `B0 −1.499924` → `−1.4999241101` (`1.101e−07`), `B2 −0.499962` →
  `−0.4999620551` (`5.506e−08`); tolerance `1e−5`. **PASS.** On `T0_unconstrained` the appended
  machinery is **bit-identical** to leg 111's own function — `0.00e+00` at `n = 16` and `n = 32`
  on `A0` and `A2`. Had this moved, the append was not append-only in effect and the whole run is
  void.
- **C2 (the predicate must be able to say NO).** `T3_hilbert_only` passes `0` rows at `γ > 3`,
  and fails on the **admissibility** clause specifically, as predicted (P4). **PASS.** Had it
  passed, this leg's result is *withdrawn, not shipped*.
- **C3 (positive control, lesson 90).** Leg 111's `Λ¹` dissipation re-run through the **appended
  constrained** path, `μ: 0 → 2`, flat weight: `T0` `−5.51616 → −1.89349 → −0.87236 → −0.13831 →
  +0.49674`; `T2` `−2.85389 → −0.03295 → +1.12444 → +2.04484 → +2.87951`. Both sign-flipping and
  monotone. **PASS.**
- **C4 (no borrowing across objects).** `μ > 0` is a **different operator**, not a different
  realization. **No `μ > 0` row answers this gate**; every gate-answering row is at `μ = 0`
  exactly, and the `μ > 0` block sits in its own JSON section so the distinction is visible
  rather than assumed.

**P6, the prediction made to be negative, and it was better than predicted.** The gap does not
grow without bound toward `γ = 7`: it **degrades into contamination** instead
(`A5 +0.894630` at contamination `4.0e−07`, `A6 −78356.36` at `1.2e+05`, `A7 −94793.53` at
`3.2e+15`, and `A7` is flatly inadmissible). That is a stronger statement than the saturation
predicted, and is reported as such rather than as a confirmation.

**A lesson-90 flag on this leg's own output.** `T0_unconstrained` returns **identical** ladders
at `γ = 5, 6, 7` (`−0.044755 −0.022898 −0.011583 −0.005825`). Three different weights cannot
legitimately give one number: that computation has **no content** — the whitening has dropped
essentially everything — and those rows are already excluded by the admissibility clause (margins
`−2`, `−3`, `−4`). Recorded rather than passed over, because four identical numbers are exactly
what leg 53 mistook for a finding.

---

## 7. Clause 3, the disagreement, and the ruling that scoped it

### 7.1 The disagreement, as measured

Every decisive row failed on **exactly one** of the five clauses — **clause 3, quadrature-depth
stability** — and only at the deepest pre-committed grading depth, `n_grade = 96`. From
`quadrature_stability["T2_egm|E_egm"]`:

| `n_grade` | 12 | 24 | 48 | **96** |
|---|---|---|---|---|
| gap | `+0.4999998187` | `+0.4999997045` | `+0.4999997527` | **`−230.7108028`** |
| contamination | `2.518e−21` | `1.031e−17` | `1.730e−10` | **`3.066e+03`** |

At `n_grade = 96` the innermost quadrature panel sits at `θ ~ 3e−31`, where the order-`θ³`
cancellation that **defines** the constrained space is below float64's ability to represent it.
The `contamination` diagnostic — the weighted energy of a bound on the pointwise cancellation
error, divided by the weighted energy of the basis function — reads **`3.066e+03`** there: the
roundoff floor exceeds the signal by three thousand times.

The failure is **the instrument stopping, not the mathematics moving.** The four depths split
across `24` orders of magnitude of contamination, with no depth remotely near the value `1`.

### 7.2 The ruling — the user's, dated 2026-08-07

> **RULING 1 — the gate's LITERAL wording governs. The answer is YES.** Clause 3 of the leg's
> own five-clause predicate is **scoped, not overruled**: it is only ever evaluated at grading
> depths where the runner's own contamination diagnostic is below 1.
>
> The reasoning, so it is on the record and not re-litigated: clause 3 did not detect instability
> in the mathematics. It detected that the instrument stops working at `n_grade = 96`, where the
> innermost panel sits at `θ ~ 3e−31` and contamination reads `3.1e+03` — the roundoff floor
> exceeding the signal by three thousand times. Over the three depths where contamination is
> below 1 the spread is `2.2839e−07`. This is not relaxing a pre-registration after seeing the
> answer; it is declining to read a number the leg's own diagnostic declares meaningless, which
> is lesson 86 and which leg 178 itself cites. The leg was right to refuse to make this call
> unilaterally, and right to take the YES branch's action (escalate, do not build, do not land)
> as the one safe under both readings.

**Clause 3 as it now reads:** *at fixed `n = 128`, sweeping the grading depth
`n_grade ∈ {12, 24, 48, 96}` gives relative spread `≤ 1e−3`* — verbatim as §7 of the novelty log
wrote it — **with one scope attached: evaluated only at depths whose contamination diagnostic is
`< 1`.**

| | spread | vs tolerance `1e−3` |
|---|---|---|
| three read depths (`12, 24, 48`) | **`2.2839e−07`** | passes by **`4.379e+03`** |
| all four depths | `4.0349e+00` | fails by `4.035e+03` |

**This was not the leg's call and is not credited to it.** The leg wrote: *"I am not permitted to
resolve this by relaxing my own pre-committed clause after seeing the answer, and I have not."*
It also declined to write the NO branch's prose — *"the coincidence persists under a second,
independently-chosen construction"* — because §5.3's magnitudes falsify it. It escalated. The
record of that refusal is preserved deliberately.

**The pre-committed ladder `{12, 24, 48, 96}` is NOT changed.** The ruling scopes how a depth is
*read*, not which depths are run, so depth 96 keeps reporting its diagnostic rather than being
deleted from future sweeps on this module.

---

## 8. What does NOT follow — the bounding ruling, same date

> The goal is now a full Clay solve… EGM buy the origin conditions with two free modulation
> parameters, so a gap on a constrained trial space is not a certificate; the `+0.499999667` is
> EGM's published `−1/2` reproduced numerically and leg 178 says so in as many words; and the
> object is the `a = 0` CLM linearisation, whose `Y₀` is exactly zero for the banned degenerate
> reason. **Do NOT open a weighted-energy lane. "Not dead" is not "open."**

Explicitly, and none of this is loosened by the YES:

- **No weighted-energy lane opens.** Not ranked, not proposed, not priced. This is a **method
  fact about a constrained trial space**.
- **A gap on a constrained trial space is not a certificate.** EGM *buy* `f′(0) = Hf(0) = 0` with
  two free modulation parameters (leg 165's caveat, carried verbatim).
- **The `+0.499999667` is EGM's `−1/2`, reproduced on this instrument.** Not a new theorem.
- **Clause S7 binds.** The object is the `a = 0` CLM linearisation — one mode, analytic, the
  friendliest object in this repository, and the one whose `Y₀` is exactly zero for a separately
  banned degenerate reason. A gap measured here bounds `HL_S2_nonsymmetric`'s difficulty **from
  below, never above**.
- **`B`'s space axis is not re-opened.** That clause concerns the `ℓ¹_w` **coefficient** space of
  the radii-polynomial machinery, which shares **zero quantities** with this weighted-`L²` energy
  form: no `Y₀`, `Z₀`, `Z₁`, `Z₂`, no approximate inverse `A`, no `A_K ⊕ A_tail` split, no
  border, no `ℓ¹_w` norm.
- **No stage claimed, no ban lifted, no link of the `L1 → L4` chain moved.** Clay stays at
  **`~0.05%`**.
- Plain float64 throughout; **nothing interval-enclosed**.

`capabilities.py`'s leg-111 entry is left exactly as leg 111 wrote it. Its scope line —
*"the window has ZERO width ON THIS UNCONSTRAINED ODD-SINE TRIAL SPACE (p = 1 vanishing order)"* —
is accurate as written and this leg's `T2_egm` is a **different**, constrained, `p = 3` space that
does not contradict it. Re-scoping that entry was raised by the leg as an open question and was
**not** decided by the 2026-08-07 ruling, which decided the gate reading only.
