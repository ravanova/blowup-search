# VERIFY 256 — post-landing review of Route-P1B (leg 256, commits `f7b9ee4` + `5916b03` + `68c74de`)

**Verdict: CONFIRMED, no gap.** Every load-bearing claim was re-derived or re-observed from a
source independent of leg 256's own runner. The most consequential claim — the Z1/Z2
discrepancy, the "commented-out bound" and the "stale `delta_lo` multiplier" — is **fully
independently confirmed**: their verification package was cloned at the pinned commit and read
directly, and the sup-bound families were recomputed from scratch from their released `ubar`.

This is a re-dispatch; the prior verifier for this leg died mid-review in the usage-limit
outage with nothing salvageable. This review was run fresh from `origin/main`.

**One cosmetic defect** is recorded in §7 — a single mistyped digit in the pre-committed
novelty file. It changes no gate, no verdict, and no banked number; the journal and the banked
JSON both carry the correct value.

---

## 0. What was independently re-derived vs. only cross-checked

Stated up front, per lesson 90 — the review is worth exactly what it re-derived, not what it
read.

| claim | status |
|---|---|
| the paper's md5, line count, Theorem 42, its 5 constants, `1e-3`, Corollary 21, Remarks 40/41, eq. (54), the `Z2`/`Z3` formulas | **re-derived** — PDF re-extracted here, every statement read at source |
| `P(1e-3) < 0` at their **published** constants, the `1.0114×` margin, `δ̄` recompute, `Q(δ̄)` | **re-derived** — my own arithmetic, from the paper's printed numbers only |
| the stale `1.17163` multiplier, `P(δ̲) > 0`, required `1.22200`, the `Y ≤ 6.3615e−04` threshold | **re-derived** — cell 35 read in the cloned package; arithmetic redone here |
| the commented-out `sup∂ₓψ̂` bound in cell 15 | **re-observed** — read verbatim in the cloned package at the pinned commit |
| `sup ū` / `sup ∂ū` for all four sup-bound families, and the whole `Z2` column of §5's table | **re-derived** — recomputed from their released `ubar` with my own code, no leg-256 module used |
| the eigenvalue convention `λ_m = ½+m` | **re-derived** — my own from-scratch basis, finite differences against the operator |
| `Z1`'s column of §5's table (`0.969` to Remark 41) | **cross-checked only** — `Z1` is a 2×2 spectral norm of quantities that need the quadrature; not backsolvable from printed numbers alone |
| `Y`, `Z3`, `‖LAL⁻¹‖`, `ū` agreement, the ladder, the poisoning | **cross-checked** — the module's own gates re-run here, plus a full independent re-run of the pipeline (§6) |

---

## 1. The source, re-pinned here

`Papers/2404.04054.pdf` re-hashed in this session:

* PDF `md5 = ff7a34b776bfe5edf97397e5eabdbb7a` — **matches leg 256's pin exactly**.
* `pdftotext -layout` output `md5 = 4e7f064859e924244ad19b5bb0888a67`, **2060 lines** —
  **matches leg 256's pin exactly**, byte for byte.

(Note for the ledger: verify 255 used a *different* extraction of the same PDF — 3448 lines,
md5 `944e134c…` — because it did not pass `-layout`. Same document, different line numbers.
Leg 256's pin is the `-layout` one and it reproduces here exactly.)

**Theorem 42** sits at line 1850 and its constants at lines 1858–1862. Read at source:

> *"Theorem 42. Let ū : R+ → R be the function represented on the interval [0, 4] in Fig 7 and
> whose description in terms of "Fourier" coefficients in {ψ̂m}ⁿ_{m=0} is available at [18],
> then there exists a positive solution u⋆ ∈ H to Eq. (54) such that ‖u⋆ − ū‖_{H²(µ)} ≤ 10⁻³."*

with `Y = 0.00075636391`, `Z1 = 0.065135932`, `Z2 = 343.3917`, `Z3 = 556.478`,
`δ̄ = 0.00271646316`.

**Leg 256's transcription of all five constants and of the `10⁻³` enclosure radius is exact.**
Theorem 42 is also correctly identified as the only §6 result carrying a genuine `∇u` term, and
it is the result Remark 40 (line 1686) attaches to. Remark 40 and Remark 41 (line 1831) were
read verbatim and leg 256 quotes both accurately, including rendering Remark 41's `1/√e` as
`e^{−1/2}`.

**Corollary 21** (line 669) reads, at source, `P(δ) = Y − δ + Σ_{k=1..p} (Z_k/k!)δ^k`,
`Q(δ) = −1 + Σ (Z_k/(k−1)!)δ^{k−1}`, and concludes uniqueness of the fixed point in `B̄(ū,δ)`
**for all `δ ∈ (δ_, δ̄)`** with `δ_` the smallest positive root of `P` and `δ̄` the positive
root of `Q`. At `p = 3` this is exactly leg 256's
`P(δ) = Y − δ + Z₁δ + Z₂δ²/2 + Z₃δ³/6`, `Q(δ) = −1 + Z₁ + Z₂δ + Z₃δ²/2`. **Correct**, and
Reading A's shape (`δ_min < 1e−3 < δ̄`) is the right reading of the corollary's open interval.

The `Z2`/`Z3` formulas (line 1723–1724) read at source:
`Z₂ = 2^{15/4}‖LAL⁻¹‖(√2‖ū‖_∞ + ‖∂_xū‖_∞)`, `Z₃ = 96‖LAL⁻¹‖`. **This is what makes leg 256's
§8 back-solves legitimate**, and I redid them: `Z₃/96 = 5.796645833333333` and
`Z₂/(2^{15/4}·5.7966458) = 4.403018838547579`, both matching the leg's banked values.

## 2. The attribution rule, re-derived from the paper's own numbers

Computed here from the **published** `Y, Z1, Z2, Z3` alone — no leg-256 code:

| quantity | my value | leg 256's banked value |
|---|---|---|
| `P(10⁻³)` | `−6.7115616666667e−06` | `−6.711561666666692e−06` |
| smallest positive root of `P` | `9.886846932845e−04` | `9.886846932845356e−04` |
| `10⁻³ / δ_` (**the margin**) | **`1.0114448082309`** | `1.0114448082308967` |
| `δ̄` recomputed from printed `Z1,Z2,Z3` | `0.0027164631369049` | `0.0027164631369048634` |
| rel. err vs printed `δ̄` | `8.501914e−09` | `8.501914e−09` |
| `Q(δ̄)` | `1.2978333686e−14` | `1.2978333685520482e−14` |
| `δ̄ / 10⁻³` | `2.7164631369` | `2.7164631369048635` |

**The attribution rule was followed correctly.** Leg 256 pre-committed (novelty §6) that a
finding is "theirs" — and escalates — *only* if their published constants, at face value, fail
their own Corollary 21. They do not: `P(10⁻³) < 0` and `10⁻³` lies strictly inside
`(9.886847e−04, 2.716463e−03)`. **The margin claim `1.0114×` is independently confirmed to 13
significant figures.** Not escalating is the correct call under the rule as written.

The margin is genuinely thin — the claimed enclosure clears their own polynomial's smallest
root by 1.1% — and leg 256 says so in those words. That is an honest report of a tight but
valid certificate, not a defect.

## 3. Their released package — cloned, at the pinned commit

Network egress was available. `github.com/Huggzz/Hermite-Laguerre_proofs` cloned fresh here;
**commit `7acaac71c84147d745cc959fbd97b548dc12372c` exists and is the HEAD of `main`**, and
`Burger/` contains exactly `proof.ipynb`, `quadrature.jl`, `ubar` as leg 256 recorded.

### 3a. The stale `delta_lo` multiplier — CONFIRMED verbatim

`proof.ipynb` **cell 35**, read directly at the pinned commit:

```julia
δ̲ = Y/(interval(1)-Z₁)*(interval(1.17163))
if sup(P(δ̲))<0
    println("δ̲ is validated")
end
```

This is exactly leg 256's characterisation, in exactly the cell it names. Evaluated here at the
published constants: `δ̲ = 9.479224608227e−04`, `P(δ̲) = +2.4542766431e−05 > 0`, and the
multiplier that *would* validate is `1.2220120264` — short by `1.0430×`. Solving for the `Y` at
which `1.17163` validates gives `6.3615416825e−04`, i.e. `1.1890×` below the published `Y`, so
print-rounding does not explain it. **All four figures reproduce leg 256's banked values.**

Cell 34's `P` is `Z₃/6 δ³ + Z₂/2 δ² − (1−Z₁)δ + Y` — algebraically identical to Corollary 21's,
so the multiplier is being tested against the right polynomial. The staleness is real.

### 3b. The commented-out `sup∂ₓψ̂` bound — CONFIRMED verbatim

`proof.ipynb` **cell 15**, read directly:

```julia
ψ̂₀ = interval.(Float64, sqrt.([...]));
# sup∂ₓψ̂ = (supψ̂ + 2*sqrt.(1 .- 0.5 ./interval.(1:n+1)).*supψ̂)./sqrt(interval(2)*exp(interval(1)));
```

The live `sup∂ₓψ̂` is defined separately in cell 17. So there are indeed **two** `∂ₓψ̂` bounds in
the released notebook, one of them commented out, exactly as leg 256 reports. (It is stale in a
second way too: the commented line references `supψ̂`, which is not defined until the *next*
cell.)

### 3c. The sup-bound families — RE-DERIVED from their `ubar`, from scratch

Their `ubar` is a Julia `Serialization` of 1501 `Float64`s; the file is 12024 bytes = 16 + 1501·8
and `a[0] = 1.5850701039153166`, confirming leg 256's defensive layout read. I implemented cells
15/16/17 and Remark 41 myself in log space and contracted against `|ū|`:

| bound family | my `sup ū` | leg 256 | my `sup ∂ū` | leg 256 | my `√2 supū+sup∂ū` / published `4.4030188` | leg 256's `Z₂`/published |
|---|---|---|---|---|---|---|
| cells 16/17 **as released** | `1.66592` | `1.6659` | `1.18934` | `1.1893` | **`0.80520`** | **`0.8052`** |
| cell 16 + **commented-out** cell 15 | `1.66592` | `1.6659` | `1.81970` | `1.8197` | **`0.94836`** | **`0.9484`** |
| **Remark 41** (the paper's own, sharper) | `1.34036` | `1.3404` | `1.11055` | `1.1105` | **`0.68274`** | **`0.6827`** |
| Remark 41 `ψ̂` + code `∂ψ̂` | `1.34036` | `1.3404` | `1.18934` | `1.1893` | **`0.70063`** | **`0.7006`** |

**Every figure reproduces to the printed digits, from my own code, using only their released
artifacts.** Because `Z₂ = 2^{15/4}‖LAL⁻¹‖·(√2‖ū‖_∞+‖∂_xū‖_∞)` and `‖LAL⁻¹‖` reproduces to
their print granularity, the last column *is* the `Z₂` ratio — so **the claim "their `Z₂`
matches a bound that is commented out in their released notebook, to `0.948`" is independently
established**, not merely restated.

I also confirm the looseness figures: cell 16's bound has `max_m = 12.3565` (attained at
`m = 1500`) against `π^{−1/4} = 0.751126` at `m = 0` — leg 256 reports `12.357` and
`0.75113`. The `136.3×` and `47.0×` overshoot ratios are bound-over-*measured*-sup and need the
module's basis evaluation, so those two I cross-checked rather than re-derived; they are
consistent in order of magnitude with the analytic decay.

**Where the `Z1` claim stands.** `Z1` is the spectral norm of the 2×2 `[[Z̄11,Z̄12],[Z̄21,Z̄22]]`,
and `Z̄11`, `Z̄12`, `Z̄21` all require the product quadratures — so unlike `Z2` it cannot be
backsolved from printed numbers. The claim that their `Z1` matches Remark 41's sharp bound to
`0.969` is therefore **cross-checked against the leg's own pipeline (which I re-ran), not
independently re-derived**. It is the one number in §5's table I could not reach from outside.
This does not weaken the leg's conclusion, which rests on the *joint* statement that no single
family reproduces both — and the `Z2` half of that is now established from outside.

### 3d. The implementation is a faithful port, cell for cell

I read their notebook cells 4, 5, 12, 26, 27, 30, 31, 32 and compared to
`solver/bc_weighted_sobolev.py::bounds`:

* cell 12's `Y = sqrt(H2(Aₙ*PFū) + (L6(ū) − L2(V̄4'*((V̄4ū)².*(DV̄4ū)))))` ≡ module ll. 739–744.
* cell 26's `Z²²` ≡ module l. 775, term for term.
* cell 27's `Z₁ = op_norm([Z¹¹ Z¹²; Z²¹ Z²²])` ≡ module ll. 778–779 (their 2×2 `op_norm` is the
  closed-form exact spectral norm, so `np.linalg.norm(B,2)` is equivalent).
* cell 30's `op_n = max(op_norm(𝔏Aₙ𝔏⁻¹), 1)` ≡ module l. 782, and the module deliberately
  reproduces their **loose** `sqrt(‖A‖₁‖A‖_∞)` operator-norm bound rather than the true spectral
  norm — correct, since that is what their `Z2`/`Z3` are built from.
* cells 31/32's `Z₂`, `Z₃` ≡ module ll. 783–784.

## 4. The eigenvalue convention — re-derived independently

This repository's history of sign/convention bugs makes this the right thing to spot-check, and
I did it without touching leg 256's module. I built `ψ_m(x) = L_m^{(−1/2)}(x²/4)e^{−x²/4}` from
the plain Laguerre recurrence and applied `L = −∂_xx − (x/2)∂_x` by central differences at five
abscissae:

| `m` | measured `Lψ_m/ψ_m` | `½+m` | `½+2m` |
|---|---|---|---|
| 0 | `0.5000000` | 0.5 | 0.5 |
| 1 | `1.5000000` | 1.5 | 2.5 |
| 2 | `2.5000000` | 2.5 | 4.5 |
| 3 | `3.5000000` | 3.5 | 6.5 |
| 5 | `5.5000000` | 5.5 | 10.5 |
| 8 | `8.5000000` | 8.5 | 16.5 |

**`λ_m = ½ + m`. The `½+2m` convention is refuted at every `m ≥ 1`.** Leg 256's gate settles it
the same way and reaches the same answer.

Three further independent confirmations of the same convention:

* The paper's **Notation 28** (line 954) states it outright: *"let `λ_m = d/2 + m` so that
  `Lψ̂_m = λ_m ψ̂_m`"*, with `d = 1`.
* **Corollary 9** (line 355) gives `Lψ_n = (d/2 + n)ψ_n` for `ψ_n(r) = L_n^{(α)}(r²/4)e^{−r²/4}`
  — index `n` is the *Laguerre* index, not the Hermite degree `2n`. This is exactly the ambiguity
  the gate exists to kill, and the module resolves it correctly.
* Their own `proof.ipynb` cell 4: `𝔏 = Diagonal(interval.(collect(0:n)) .+ λ₀)` with
  `λ₀ = interval(d//2) = 1/2`, and `λₘ = interval(d//2+n+1)`. Same convention, from their code.

Note the paper's eq. (11) is *not* in conflict once read carefully: `LΨ_β = ((d+|β|)/2)Ψ_β` at
`d = 1`, `|β| = 2m` also gives `½ + m`. The trap is the Corollary 9 / Hermite-degree confusion,
and that is the one the gate actually disarms.

## 5. Territory, ban discipline, claim discipline

**Territory — clean.** `git diff --name-only f7b9ee4^ 68c74de` returns exactly seven paths and
nothing else:

```
capabilities.py
experiments/journal/leg_256.md
experiments/p2_route_p1b_v1_bcrepro.py
solver/bc_weighted_sobolev.py
test_bc_weighted_sobolev.py
writeup/data/p2_route_p1b_v1_bcrepro.json
writeup/novelty/leg_256.md
```

**No other solver module is touched.** `capabilities.py` is a **single appended row** — the diff
adds 26 lines and removes zero, and no existing entry is modified. None of the five shared
ledgers is edited; leg 256 flags the pointers it wants rather than writing them, which is the
correct posture.

**Ban discipline — genuinely honoured, checked at the implementation and not just the prose.**
The operative ban is the re-posed 2026-08-06 one, and leg 256 quotes it accurately (abbreviating
only the origin-H² parenthetical, with no change of meaning). `solver/bc_weighted_sobolev.py`
imports **`math` and `numpy` and nothing else** — no `solver/interval.py`, no
`solver/nk_bounds.py`, and crucially no `solver/origin_h2_certificate.py`, the one module the
novelty pass identified as belonging to a dead realization. The space really is
`H²(µ)` with the Hilbert norm `‖Lu‖_{L²(µ)}`, the basis really is the half-Hermite/Laguerre
family on the unbounded domain, and the tail really is controlled by `L`'s spectral gap. None of
the three dead realizations is contacted in code or in method.

The novelty pass does call this "the namable fourth space" — the exact phrase in the ban's lift
condition — but it immediately and repeatedly states that **it does not lift the ban and does
not claim to**, and defers the distinctness argument to leg 257 as the scoping leg the lift
condition requires. That is a *nomination*, not a lift, and it is the correct discipline. The
same disclaimer appears in the journal (§1, §9) and in the module's own docstring (l. 39).

**Claim discipline — clean.** Grepping leg 256's own files for `L1`/`L4`/`Clay`/`odds`/`lift`
returns only the three "does not lift the ban" disclaimers. **No claim of L1→L4 movement, no
statement about Clay odds, no ban lifted, and no construction on any Phase-1 target.** Journal
§9 explicitly declines to upgrade Remark 40's "in principle" and states that reproducing a **1D**
result is not evidence for `d = 2,3`. The float64-not-interval ceiling is stated in §2 *before*
any constant and repeated in §8 and in the `capabilities.py` row.

## 6. The pipeline re-run here

`test_bc_weighted_sobolev.py`: **all 8 gates pass** in this worktree. The convention gate prints
`L psi_m = (1/2+m) psi_m for m=0..8, rel residual < 2e-6` and `the 1/2+2m convention is refuted
by the same measurement` — same conclusion my own independent computation reached. Gate 5
reproduces `δ̄` to `8.50e−09` and reports `their enclosure 1e-3 lies in [9.886847e-04,
2.716463e-03]`, matching my hand computation exactly.

`experiments/p2_route_p1b_v1_bcrepro.py` was then re-run in full here (637s, vs the banked
666s), and the regenerated JSON was diffed field-by-field against the banked one. **Every
substantive field is bit-identical** — the only differences are the 11 wall-clock timing fields
and four `NaN` entries that differ only because `NaN != NaN`. Worst relative drift across all
numeric fields: **`0.0`**. The pipeline is deterministic and the banked data is exactly what the
code produces.

The headline reproduces: certified interval `[9.687639e−04, 3.297630e−03]`,
`P(10⁻³) = −2.0065e−05`, Reading A `True`, Reading B `True`, ratios
`Y 1.0001 / Z1 1.3078 / Z2 0.8052 / Z3 1.0000 / δ̄ 1.2139`. The quadrature gates reproduce
`1.287e−09`, `8.605e−10`, `1.604e−09`. The ladder confirms the `n ≈ 800` claim directly —
`closes=False` at `n = 100, 200, 400` and `closes=True` at `n = 800, 1500` — so **Breden–Chu's
`n = 1500` is necessary, not conservative**, exactly as the journal reports. The poisoning
ablation reproduces `1.00× / 1.00× / 74.38×` on the total `Y` with the certificate ceasing to
close at the `1e−03` displacement.

I note this re-run is the *weakest* evidence in this review (lesson 90 — re-running the same
script and agreeing with it is a determinism check, not an independent one). It is reported as
such. The independent work is §§1–4.

## 7. The one defect found — cosmetic, recorded for completeness

`writeup/novelty/leg_256.md` §8 (l. 214) reads:

> *"…with `10⁻³` exceeding the smallest root by `1.1145×` and below `δ̄` by `2.716×`."*

The correct value is **`1.0114×`** (`1e−3 / 9.886847e−04 = 1.0114448`), as I computed
independently in §2. `1.1145` appears to be `1.011445` with the leading zero dropped.

**This is a single mistyped digit in a pre-committed file and nothing depends on it.** The
journal (§6) states `1.0114×` correctly, the banked JSON stores
`their_enclosure_over_their_delta_min = 1.0114448082308967` correctly, and the executable gate
asserts on the interval rather than on the ratio. No gate, verdict, escalation decision or banked
number is affected. It is **not** a gap, and per the standing rule I have **not** repaired it —
it is recorded here so the correct figure is the one that propagates.

A second, smaller wording note for the record: the journal's §3 table row *"our residual
`‖L F(ū)‖` on **their** `ū` | 3.438e−10"* is correctly labelled as **our** measurement on their
`ū`. It is not a figure Breden–Chu publish, and the journal does not claim it is. (Any downstream
paraphrase of the form "their own reported 3.4e−10" would be a misreading of leg 256, not a
defect in it.)

## 8. Verdict

**CONFIRMED. Gate YES on both pre-committed readings stands, the non-escalation is correct, and
the Z1/Z2 finding is real and independently established.**

Specifically:

1. The paper pin, Theorem 42, its five constants, the `10⁻³` radius, Corollary 21, Remarks 40/41
   and the `Z2`/`Z3` formulas are all transcribed **exactly**; re-read at source here.
2. `P(10⁻³) < 0` at their published constants and the **`1.0114×` margin** are re-derived
   independently to 13 significant figures. The pre-committed attribution rule was followed and
   **not escalating is correct**.
3. The verification package was **cloned at commit `7acaac71`**. The commented-out `sup∂ₓψ̂`
   bound (cell 15) and the stale `1.17163` `delta_lo` multiplier (cell 35) both **exist verbatim**
   as described. The sup-bound families and the entire `Z₂` column of §5's table were
   **recomputed from scratch** from their released `ubar` and reproduce to the printed digits.
   The `Z₁` column is the one figure I could only cross-check.
4. The eigenvalue convention `λ_m = ½+m` is **independently re-derived** by finite differences
   against the operator, and confirmed three further ways (Notation 28, Corollary 9, their cell 4).
5. Territory is exactly the seven granted files; `capabilities.py` is append-only; no other
   solver module and no shared ledger is touched.
6. The stage-V ban is honoured in the implementation, not just the prose — the module imports
   `math` and `numpy` only and contacts none of the three dead realizations. The "fourth space"
   is **nominated, not claimed**; leg 257 remains the scoping leg the lift condition requires.
7. No L1→L4 claim, Clay odds untouched, no ban lifted, no Phase-1 construction attempted.

The one defect is a single mistyped digit in the pre-committed novelty file (§7 above), carrying
no consequence. It was not repaired.
