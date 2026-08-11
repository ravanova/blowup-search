# Route-FSB v1 — the fourth space/basis screen (leg 301)

**Status: PARKED. This is escalation.** The gate below answers **YES**, and a yes on this
gate is not a licence — it is a proposal handed to the user. **Nothing is built here. No ban
is lifted here.** The re-posed 2026-08-06 ban on re-attempting the `ℓ¹`-Fourier /
radii-polynomial machinery stands after this file exactly as it stood before it. Its own lift
condition reads:

> *lifted by: never — unless a namable FOURTH space/basis this repository has not yet tried is
> proposed, with its own scoping leg establishing it is not subject to the same
> three-realization death*

Two things are asked for: a **proposal**, and a **scoping leg**. This leg supplies the first
and writes the specification for the second. The second has not been run. Until it is run and
its gate is answered, the ban is not lifted, and this file must not be cited as if it were.

| artifact | path |
|---|---|
| runner | `experiments/p2_route_fsb_v1_screen.py` |
| curated JSON | `writeup/data/p2_route_fsb_v1_screen.json` |
| figure | `writeup/figures/fig67_route_fsb_v1_screen.png` |
| BLOG | `writeup/4_p2_lottery/BLOG_P2_ROUTEFSB_V1.md` |
| novelty pass (committed alone, before construction) | `writeup/novelty/leg_301.md` |
| journal | `experiments/journal/leg_301.md` |

---

## 1. The gate, quoted from `DIRECTION.md` before the work began

> **Gate.** Does the screen produce at least one NAMED fourth space/basis with an explicit
> structural argument (not a hope) that each of the three death mechanisms cannot recur in it?

**Answer: YES**, on one candidate of the fourteen enumerated:

> **The Malmquist–Takenaka / Christov rational orthonormal basis of the line,**
> `φₙ(x) = iⁿ √(2/π) (1+2ix)ⁿ / (1−2ix)^{n+1}`, `n ∈ ℤ`.

A second candidate, the **Olver–Townsend airfoil/ultraspherical pairing** already measured by
parked leg 162, clears two of the three mechanisms and is `UNRESOLVED` on the third for a
reason that is about the *object*, not the basis. It is recorded as the fallback, not the
proposal.

---

## 2. What "the same three-realization death" actually is

The ban names three realizations. This screen refuses to treat "measured dead" as one blur.
Each realization died of a **different, separately measured mechanism**, and a fourth space has
to survive all three, not the worst one.

### M1 — zero diagonal / block coupling (leg 54, sharpened by leg 62)

Realization: **weighted `ℓ¹` of Fourier coefficients, compactified odd-sine basis**
(`solver/spectral_certificate.py`). The unbounded part is the dilation transport
`X d/dX = sin θ ∂_θ`; column `k` has entry `1 − k/2` in row `k+1` and `k/2` in row `k−1`, and
**zero on the diagonal**. Measured: `min_k |diag(tail_block)| = 0.0` exactly.

It is a **shift, not a multiplier** — lesson 87's dichotomy, and the reason the standard tail
estimate has nothing to bite on. Where the unbounded part is a multiplier the split cuts entry
size `Λ_M` and the tail inverse is `1/Λ_M`; here bordering restores the tail's *invertibility*
without touching its *size*, and leg 57 measured that the "constant" bordered tail inverse is
not a constant: **2.191 → 3.234 → 4.653 → 6.530 → 8.890 → 11.528** over `K = 4…128`, a 5.26×
rise, fitted exponent **+0.437**.

Consequences, all measured:

- best admissible `Z₁` = **8.9591** against a block-diagonal baseline of **10.4584** — the last
  free choice of shape buys **1.167×** where about **9×** was needed;
- the finite-block-independent sub-block `Z₁[tail←Γ]` bottoms out at **0.9961**, just under 1,
  which is why the failure is scoped to the shape of `A` and not to the operator;
- `‖Γ⁻¹‖` = exactly `2(K²−1)` with the amplitude column and exactly `4(K−1)` without it — the
  `K²` was created by the augmentation, not by the operator;
- leg 62: the Gershgorin shift `|s|` Cadiot's argument needs **saturates at 0.28723** on his own
  Whitham operator, and on ours runs **63 → 127 → 255 → 511 → 1023** over `M = 128…2048`,
  fitted exponent **+1.0051**. Not "the constant is bad" — the object the proof needs does not
  exist.

**Predicate.** `PASS` iff `lmin > 0` **and** the diagonal grows. These are Cadiot's Assumption 1
clauses `A1_LMIN` and `A1_GROWTH`, and both fail here, the first infinitely.

### M2 — the `(H,D)` consistency defect (leg 56)

Realization: **collocation in a weighted sup norm** on a graded line grid
(`solver/interval_certificate.py`, `solver/line_hilbert.py`). `H` is `line_hilbert_matrix`, `D`
the natural-cubic-spline slope operator. The defect enters the certificate as an addition to the
residual, so the admissible size is `τ = budget/‖A‖_w`; at `n = 801`, budget
`3.554656e−10` and `‖A‖_w = 15417.7` give **`τ = 2.306e−14`**.

Measured: derivative defect **1.854e+07 τ** converging at order **4.01**; Hilbert defect
**2.040e+11 τ** at order **0.00**. Cause, corrected in place by leg 56's own VER-C: it is not
"one interpolation error through two operators" — `line_hilbert_matrix` assembles source columns
for interior nodes only, so it transforms an **endpoint-zeroed** interpolant `Π⁰` while `D` uses
the full natural spline. They are *different discretisations*, and the endpoint artifact is the
whole defect (share **1.00009** at `n = 801`).

**Predicate.** `PASS` iff `H` and `D` act **exactly** on the basis in closed form, so that the
defect is identically zero by construction rather than small and hopefully convergent.

### M3 — `a = 0` exactness and non-transfer (legs 163/176/182; leg 260 for the Gaussian family)

Realization: **origin-`H²` on the line (Xu), Hardy blocks in the Laguerre basis**
(`solver/origin_h2_certificate.py`). This space is *real*: `σ_min = 0.0908`, truncation-stable
to 0.139% over a 16-fold range, and the tail inverse **converges** to `4.026` where `ℓ¹_w`'s
diverged. It still dies, and not on shape: leg 163's census item **O3, marked FATAL for
transfer**, observes that every usable object is a consequence of the identity

> `H(Ω) − iΩ = i/(y + i/2)`

which, in leg 182's words, *"is an equation satisfied by the **profile**. It contains no norm,
no weight, and no index."* `HL_S2_nonsymmetric` is not a CLM profile and inherits none of it.
In leg 54's shape the X realization fails too, best cell `Z₁ = **140.72**` growing like `K²`.

The sibling case is the Gaussian-weighted family (`solver/bc_weighted_sobolev.py`), which is
this repository's *own* previously named "fourth space": ruled out for the NS target by leg 260
because the Leray projector leaves `L²(µ)` (fitted tail exponent **−3.000000**) and the
weight/decay mismatch runs **26.6 → 1.0e5 → 3.9e20 → 1.3e83** across shells.

**Predicate.** `PASS` iff the basis's usable structure is independent of the profile.

---

## 3. The screen: 14 candidates

Verdicts are **computed** by predicates over per-candidate structural fields in
`experiments/p2_route_fsb_v1_screen.py`, not asserted in prose. Full table in the JSON.

| candidate | M1 | M2 | M3 | what kills it (or doesn't) |
|---|---|---|---|---|
| `l1_fourier_compactified` | FAIL | PASS | PASS | realization 1. `lmin = 0.0` exactly |
| `collocation_sup_line` | — | FAIL | PASS | realization 2. `2.040e+11 τ` at order 0.00 |
| `origin_h2_laguerre` | — | PASS | FAIL | realization 3. O3, `a = 0` exactness |
| `weighted_energy_L2` | — | PASS | FAIL | zero-width coercivity window (legs 111/141/178) |
| `weighted_holder_routeD` | FAIL | PASS | PASS | Route-D v3's conservation law, min exponent sum **0.98** |
| `breden_chu_gaussian_H2mu` | PASS | PASS | FAIL | leg 260: shells to **1.3e83** |
| `hermite_ou_eigenbasis` | PASS | PASS | FAIL | **leg 262's own named candidate, killed by leg 260's already-banked measurement** — same Gaussian-weight family |
| `chebyshev_naive_pairing` | FAIL | PASS | PASS | leg 162 realization A: same polynomial family, zero diagonal |
| `chebyshev_airfoil_ultraspherical` | PASS | PASS | **UNRESOLVED** | leg 162 realization B: exact `diag(−n)`, `Z₁ = 0.0874` — on a **different object** |
| **`malmquist_takenaka`** | **PASS** | **PASS** | **PASS** | **survivor** |
| `wavelet_multiresolution` | — | FAIL | PASS | no interval-arithmetic CAP exists in a wavelet basis anywhere; `H` almost-diagonal, not diagonal, and symmetric wavelets vanish on the diagonal by parity |
| `fourier_gevrey` | FAIL | PASS | PASS | **not a fourth basis at all**: realization 1's matrix with a different norm. A zero diagonal is a property of the matrix |
| `ellp_besov_sobolev_interpolants` | FAIL | PASS | PASS | leg 182's `σ = s + 1/p` collapse; window is the single point `σ = 2`, margin **−0.602647** at every `p` |
| `nakao_plum_fem_eigenvalue` | — | — | PASS | a different **technology**, not a basis; `M1` has no referent (lesson 73). Not proposed |

Two rows deserve emphasis because they are the screen doing work no single-candidate leg could
have done:

- **`hermite_ou_eigenbasis`** was named as a fourth-space candidate by **leg 262**, whose `M1`
  argument is correct and survives intact. It dies anyway, on `M3`, to a measurement **leg 260
  had already banked two legs earlier**. The kill was in the repository; nobody had put the
  proposal and the measurement in the same table.
- **`chebyshev_naive_pairing`** vs **`chebyshev_airfoil_ultraspherical`** are the *same
  polynomial family* and land on opposite sides of `M1`. It is the **Petrov–Galerkin pairing**,
  not the family, that decides multiplier-or-shift. Any future proposal that names a "basis"
  without naming its pairing has not named anything.

---

## 4. The survivor, and why each mechanism cannot recur

`φₙ(x) = iⁿ √(2/π) (1+2ix)ⁿ / (1−2ix)^{n+1}`, `n ∈ ℤ`: a complete orthonormal basis of `L²(ℝ)`.
Non-negative indices span the Hardy space `H²` of the upper half plane; negative indices span
its conjugate.

**M1 cannot recur.** Because the basis splits `L²(ℝ)` into the two Hardy spaces, **the Hilbert
transform is exactly diagonal on it** — multiplication by `∓i`, modulus 1. The differentiation
matrix is tridiagonal and skew-Hermitian (Iserles & Webb, DAMTP NA2019/03, eq. 3.3):

```
D[n, n]   = i(2n+1)        D[n, n+1] = n+1        D[n, n-1] = -n
```

Computed from that closed form in the runner, over `n ∈ [−64, 64]`:
**`lmin = 1.0`** (attained at `n = 0, −1`), diagonal growth exponent fitted **0.974588** on
`n = 8…64` and exactly `+1` in closed form (the shortfall is the additive 1 in `2n+1`, not
slower growth). Cadiot's `A1_LMIN` and `A1_GROWTH` **both hold**, where both fail — the first
infinitely — in realization 1. The transcription is self-tested: `D` is verified
skew-Hermitian entrywise, so a misreading of the displayed matrix would have returned `False`.

**M2 cannot recur.** `H` and `D` above are *exact* on the basis: closed-form rational entries,
no interpolant, no grid, no endpoint basis functions to drop. The `(H,D)` consistency defect is
identically zero by construction, which is a different thing from small and convergent. Leg 56's
mechanism has no way in.

**M3 cannot recur.** Completeness and the Hardy splitting are properties of the **basis**, not
of any profile. Nothing in the construction references `Ω`, the CLM identity, or `a = 0`, so
there is nothing for O3 to cap. And the fit to the target's shape is structural rather than
lucky: every basis function obeys the uniform bound

```
|φₙ(x)| = √(2/π) · 1 / √(1 + 4x²)
```

so the basis carries **algebraic decay in its own functions** rather than in a weight. That is
precisely the repair for Route-D v3's diagnosed category error — *"A diagonal weight on Fourier
coefficients measures **smoothness**, not **decay** … asking a weighted-`ℓ¹` pair to express
'loses one power of decay' was a category error"* — and it is why `fourier_gevrey` is in the
table as a `FAIL` rather than as a rival.

---

## 5. Counterweights, stated at full strength

A proposal that only lists its advantages is a hope. Three things are against this one.

**(a) `δ = 1` exactly.** The BDL row-dominance ratio, **computed not quoted**:

```
δ(n) = (|D[n,n-1]| + |D[n,n+1]|) / |D[n,n]| = (|n| + |n+1|) / |2n+1| = 1.0000   for every n ∈ ℤ
```

BDL assumption (5) wants `δ < 1/2`. MT lands, exactly, on the same wall leg 158's odd–even
recast of *our own* operator reached by hand (`δ → 1.0039`). Simple diagonal dominance is
therefore **not** available, and this is the first thing the scoping leg must measure rather
than assume.

It is deliberately **not** scored as a death, for a reason that is in the banked record rather
than in this leg's preferences: **leg 62's test 14 refuted `δ` as the coordinate.** At
`µ = 0.25` the ratio is `δ = 2`, four times outside BDL, and the operator is still boundedly
invertible with `K`-exponent **−0.849**. Leg 62's own words: *the hinge is zero-versus-nonzero
diagonal, and `δ` is not the coordinate for it.* MT is on the non-zero side, with linear growth.
Consistency demands the screen use the coordinate this repository measured, not the hypothesis
it refuted.

**(b) No validated transform to inherit.** The external pass found **no rigorous-numerics or
computer-assisted-proof work in a Malmquist–Takenaka / Christov basis anywhere**. That is the
novelty and it is also the bill: there is no validated MT transform, no published interval
enclosure of the coefficients, no `Y₀` machinery to port. The nearest transferable machinery is
arXiv:2411.18361 (validated orthogonal-polynomial transforms) and arXiv:2302.12877 (CAP on
unbounded domains). Building that is exactly the cost the scoping leg exists to price.

**(c) The nonlinearity is untouched by this screen.** Every mechanism screened here is about the
**linear** operator's shape. MT is a *rational* basis; the quadratic term's coefficient
convolution is not the clean Cauchy product a Fourier basis gives, and its `ℓ¹`-algebra
property is **UNMEASURED** by this leg. It is scoping question S3 below and it is capable of
killing the proposal outright.

---

## 6. Controls

Lesson 90: a control that cannot come out differently is not a control, and identical numbers
are the tell. All four here can come out differently, and two of them do.

| control | purpose | result |
|---|---|---|
| **negative** — this repository's own tail operator, banked closed form `λ_k = 1−(k−1)/2`, `µ_k = 0`, `β_k = (k+1)/2` | the screen must FAIL `M1` on the realization measured dead | `lmin = 0.0` exactly, `δ` infinite, **`M1 = FAIL`** — the opposite answer to MT |
| **positive** — leg 158's synthetic BDL-admissible `µ_k = k`, `λ_k = β_k = 0.2k` | the screen must PASS, and land inside BDL | `lmin = 2.0`, growth exponent `1.0`, `δ = 0.4000`, `bdl_admissible = True`, **`M1 = PASS`** |
| **instrument** — leg 158's odd–even recast, recomputed | does this code reproduce a banked number? | limit **1.00196** against banked **1.0039** (0.19%); **sup 3.0 against banked 1.667 — does not agree** |
| **self-test** — `D` skew-Hermitian | catch a mis-transcription of eq. (3.3) | passes |

The instrument check's disagreement is reported, not tuned. The two quantities differ **by
definition**: leg 158's `δ` is a `2×2` block quantity (`‖D_j⁻¹‖` times the off-block mass),
the recomputation is the elementwise ratio. They must agree asymptotically, where the blocks
decouple, and need not agree at the first few modes, where the border row and the pairing offset
both matter. The agreeing half is the half with content — it is the same wall — and nothing in
the gate depends on the sup.

---

## 7. What this leg did NOT do

- It did not build anything. No `solver/` module is written, edited or imported by the runner.
- It did not compute a `Z₁`, `Y₀`, `Z₀` or `Z₂` for any operator in any space.
- It did not lift the ban, and a `YES` here does not lift it. **Only the lift condition lifts
  it, and the lift condition names a scoping leg that has not been run.**
- It did not measure the nonlinearity, the quadratic term, or any `ℓ¹`-algebra property of the
  MT coefficient space.
- It did not move a link of the `L1 → L4` chain. **Clay odds stay ~0.05%.** Ranking this leg
  high by chain proximity was a choice about what to try; it is not a claim about what happened.

---

## 8. The scoping-leg spec the lift condition requires

Proposed as **Route-MT v1**, to be dispatched only on the user's ruling. Its remit is to
*price* the basis, and it must be able to come back `NO`.

**Object.** `HL_S2_nonsymmetric` (the standing target), and the MT basis of `L²(ℝ)` above with
its Hardy splitting. Not the `a = 0` CLM profile — a scoping leg that reverts to `a = 0` has
reproduced M3 and answers `NO` by construction.

**Pre-committed gate.** *Does the MT basis carry, for the real target, (i) an approximate
inverse whose `Z₁ < 1` at some truncation, with (ii) the truncation-dependence measured over at
least a 4-fold range, and (iii) the quadratic term bounded in the same norm — all three, with
each bound admissible in the sense of lesson 86?*
`yes` → the lift condition is met on evidence and the ban's status returns to the user.
`no` → bank at full strength: the fourth space is measured dead too, with its own named
mechanism, and the ban's lift condition is then **exhausted over the enumerated class** — the
strongest possible closing of this line.

**Stages, in order, each able to stop the leg.**

- **S1 — the linear shape, measured.** Assemble the target's linearization in MT coordinates and
  measure `min |diag|`, its growth exponent, and `σ_min` of the bordered finite block over at
  least `N = 64,128,256,512`. Hypothesis under test: `lmin ≥ 1` survives the *target*, not just
  the differentiation matrix. **Kill condition:** `σ_min → 0` with `N`, i.e. leg 127's verdict
  recurring in a new basis.
- **S2 — dominance, honestly.** Measure `δ` for the target's linearization. It is expected near
  1 and BDL will not apply. Required deliverable: either a Gershgorin-free bound, or the
  measured shift `|s|` as a function of `N` with its fitted exponent — the number that must
  **saturate** (Cadiot's Whitham: 0.28723) and that ran `+1.0051` in realization 1.
- **S3 — the nonlinearity.** Measure whether the MT coefficient space is an algebra under the
  target's quadratic term, or bound the bilinear form's norm directly. **This is the stage most
  likely to kill the leg**, and it must be attempted before any certificate is assembled.
- **S4 — admissibility (lesson 86).** Every bound finite-rank-plus-explicit-tail. Leg 54's
  `exact_inv` tautology (`1e−9` inadmissible → `1e4` admissible, two orders *worse* than
  baseline) is the banked warning.
- **S5 — controls before conclusions.** A known-answer object in the MT basis (leg 61's
  CLN-Kawahara pattern), and a negative control that reports the other answer.

**Costs to declare up front.** No validated MT transform exists; S1–S3 include building and
verifying one. MT coefficient decay for the relevant class is geometric only for
rationally-decaying targets (`ρ = 1 + √2` for `1/(1+x⁴)`-type) and merely algebraic
(`|n|^{−5/4}`, `|n|^{−9/4}`) for `sin x/(1+x²)`-type — so **the decay rate of the target's own
coefficients is itself an S1 measurement**, not an assumption.

**Explicitly out of scope.** Re-running any of the three dead realizations; touching the
Chebyshev corner parked on `origin/leg/162-capg-v1`; any claim about Clay odds.

---

## 9. Provenance

Iserles & Webb, *Orthogonal systems with a skew-symmetric differentiation matrix*, DAMTP
NA2019/03 — eq. (3.3) read from the PDF as text, not paraphrased. Cadiot arXiv:2505.03091 §2/§3
(the dominance hypothesis, named as a hypothesis by its own author); BDL arXiv:1503.06315
assumptions (4)/(5). Olver–Townsend / Slevinsky–Olver arXiv:1507.00596. Internal: legs 54, 56,
57, 62, 127, 158, 162, 163, 176, 182, 245, 255, 257, 260, 262, and Route-D v3's
`TECHNICAL_P2_ROUTED_SPACES.md`. Every internal magnitude in this file is read out of the banked
record; none was re-derived here.
