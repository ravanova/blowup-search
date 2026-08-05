# Route-T v1 — bordering restores a bounded tail, and it works where the failure curve was *worst*

*Phase 2 / P2, leg 52. Code: `solver/spectral_certificate.py` (+5 functions),
`test_spectral_certificate.py`, `experiments/p2_route_t_v1_border.py` →
`writeup/data/p2_route_t_v1_border.json` → **fig47**. Working notes: `PHASE2_P2_NOTES.md`
§41. Plan stage `T` (`plan_of_record.py`). 154 s, 6/6 pre-committed clauses.*

**Leg 51 measured a window that was empty by 0.606 in exponent units and answered `L1`'s
gate NO. One border row and one border column close it: the bordered tail inverse saturates
at `s = 0` (9.44) and `s = 0.3` (11.37), both inside the band where the target profile has
finite norm. The border a proof can write down achieves the optimum to three digits. It is
still not a certificate, for a reason pre-committed before any number existed. No chain link
moved; Clay unchanged at ~0.05%.**

---

## 0. What was open

Leg 51 rebuilt the certificate in Route-E's compactified basis and got three of four terms:
the operator gap vanished, `Y₀` was **exactly zero** in rational arithmetic, `Z₁` and `Z₂`
were rigorous and finite. The fourth term — the neglected-mode tail — had no bound in any
weight class tried, because the unbounded part of an inviscid self-similar linearisation is
the dilation **shift**, not a multiplier: **the tail operator's diagonal is exactly zero.**

But leg 51 also localised the failure further than "the space is wrong". The operator is
**not injective**, and its kernel is one explicit mode — `h_m ~ m^{−2.007}`, the `|X|^{−1}`
far field. A non-invertibility caused by a **finite-dimensional kernel** is the textbook
case for **bordering**, which is the same move that made Route-PORT's finite block work
(three gauge freedoms → three border rows). This leg measures that repair before anything is
built on it.

## 1. T-0 — the novelty pass, first, and it narrowed the claim

Five queries, three ledger entries, **committed in the driver** so the search is auditable
rather than remembered (leg 42's failure mode was an unrecorded search). Verdict
`PROCEED_NARROW`.

The one that matters: **Breden–Desvillettes–Lessard, arXiv:1503.06315**, *"Rigorous numerics
for nonlinear operators with tridiagonal dominant linear part."* They state leg 51's problem
in nearly leg 51's words — the derivative "does not have an asymptotically diagonal dominant
structure", so the approximate inverse is not straightforward — and supply a construction for
`A` in that setting.

**So the general observation is not new**, and leg 51's methodological claim drops to a
re-derivation of something the field knows. What their paper does not obviously cover: our
tail is tridiagonal and **not dominant** — diagonal exactly zero — and is **Fredholm with a
kernel**. Whether their construction reaches that case **was not resolved in this pass** (the
PDF did not extract), and it is recorded as an open question rather than as a gap.

Leg 51's *prediction about the shape of the field* survives the pass — the certified
self-similar blow-ups using `ℓ¹`-Fourier machinery are dissipative (Dahne–Figueras, CGL),
while the certified inviscid ones (Chen–Hou, arXiv:2210.07191 / 2305.05660) used weighted
energy estimates over 145 pages instead. That is a consistency check, not evidence.

*Flagged:* the query naming `arXiv:2604.01868` (Chen–Huang–Li, the April 2026 source of this
project's target) **did not resurface it** — only 2021–2023 Hou–Luo work returned. A
statement about the search index, not about the paper; the repo's seventh-pass record stands
and a later leg should re-check.

## 2. T-5 — which side of `s = 1` the obstruction is on, stated *before* the ladders

In `w_k = (1 + k)^s`, measured on modes `65 … 3136`:

```
kernel      h_m ~ m^(-2.0024)    ->  IN the space         iff  s < 1
cokernel    u_m ~ m^(+1.0012)    ->  functional BOUNDED   iff  s >= 1
```

Bordering supplies a missing range direction and annihilates a kernel. It cannot repair a
cokernel functional that is not in the dual. **Therefore bordering must help below `s = 1`
and must not help at or above it** — written down before the ladders ran, and it is the
prediction the rest of the leg tests.

**And it re-reads leg 51's U-curve.** That curve's minimum was at `s = 1.00`, which leg 51
recorded as the least-bad class. It is in fact the exact exponent at which the operator is
marginally **both** failure modes at once — the kernel leaving the space precisely as the
cokernel functional enters the dual. The most promising-looking point on the curve was the
one point the repair could not reach.

## 3. T-1 — the ladders

`K = 64` retained modes; tail on `65 … M` for `M ∈ {320, 576, 1088, 2112, 3136}`; weighted
`ℓ¹` operator norm of the inverse of

```
B  =  [[ T , u ],
       [ vᵀ, 0 ]]
```

`v` pinning the kernel (one extra equation), `u` supplying the missing range direction (one
extra unknown), both normalised so the number is not an artifact of their scale.

| class | admissible? | unbordered | **bordered (analytic)** | shape |
|---|---|---|---|---|
| flat `s = 0` | **yes** | 4.06 → 48.76 (`M^{+1.085}`) | **7.46 → 9.44** (`M^{+0.100}`) | **SATURATES** |
| algebraic `s = 0.3` | **yes** | 3.03 → 20.67 (`M^{+0.837}`) | **8.09 → 11.37** (`M^{+0.147}`) | **SATURATES** |
| algebraic `s = 0.394` | boundary | 2.77 → 16.04 (`M^{+0.765}`) | **8.30 → 12.16** (`M^{+0.165}`) | **SATURATES** |
| algebraic `s = 1.0` | no | 1.64 → 3.94 (`M^{+0.379}`) | 9.89 → 20.51 (`M^{+0.319}`) | still growing |
| algebraic `s = 1.5` | no | 2.41 → 11.54 (`M^{+0.681}`) | 11.44 → 31.81 (`M^{+0.448}`) | still growing |

*Admissible* = the target `Ω ~ |X|^{−α}`, `α = 0.394`, has finite norm in the class, i.e.
`s < α`. `s = 0.394` is the excluded boundary, reported because it saturates anyway.

**The ordering inverts.** Unbordered, `s = 1` was the best class and `s = 0` the worst.
Bordered, `s = 0` and `s = 0.3` are bounded and `s = 1` is not. Exactly T-5's prediction,
and the opposite of what optimising leg 51's curve would have suggested.

**Reported as a shape, not an endpoint (lesson 72).** Flat increments
`0.864 → 0.616 → 0.369 → 0.133`; `s = 0.3`, `1.212 → 1.019 → 0.738 → 0.314` — falling, with
the fitted exponent down an order of magnitude (`1.085 → 0.100`). At `s = 1` the increments
*rise* across the ladder (`2.44 → 2.92 → 3.25`), which is what a slow divergence looks like
and what a slow saturation does not.

### 3.1 The window is no longer empty — this is the result

```
leg 51:  object needs s < 0.394   |   operator wants s ~ 1   |   gap 0.606, curve never zero
leg 52:  object needs s < 0.394   |   operator BOUNDED at s = 0 and s = 0.3
```

The two sides overlap. Leg 51's NO was a statement about the **standard construction**, not
about the object — which is the branch `L1`'s own gate named in advance and did not get to
take.

### 3.2 The kernel is one-dimensional, measured

`σ_min` falls `2.71e−01 → 8.54e−03` (flat class) while `σ_2` stays bounded away,
`2.092 → 1.652`. One singular value goes to zero and the next does not, independently
confirming the analytic claim that the block's first row — which involves the mode `K` lying
outside it — kills one of the two parity chains.

## 4. T-2 — the border a certificate can actually write down

The SVD pair is the most favourable one-dimensional bordering that exists; the analytic
far-field mode and its adjoint are what a proof would use. Ratio at the top rung:

```
flat 1.000    s=0.3 1.007    s=0.394 1.012    |    s=1 1.130    s=1.5 1.383
```

**In the admissible classes the explicit mode achieves the optimum to three digits.** That
is the clause that makes the repair usable rather than an SVD artifact — a certificate
cannot border with a singular vector it computed numerically.

## 5. T-4 — the alignment is the physics, and it fails with the repair

`|cos|` between the optimal border direction and the analytic far-field mode, top rung:

| class | flat | `s = 0.3` | `0.394` | `s = 1` | `s = 1.5` |
|---|---|---|---|---|---|
| alignment | **1.00000** | **0.99996** | 0.99991 | 0.99300 | **0.90209** |

At `s = 1.5` it is also *flat in `M`* (0.90378 → 0.90209), i.e. not converging to the far
field at all. **Alignment and usefulness degrade together** — the story predicts that and a
coincidence would not. The repair is therefore not "border by something": it is **add the
far-field amplitude as an unknown.**

## 6. T-3 — the negative controls

| border | flat class, `M = 320 → 3136` | saturates? |
|---|---|---|
| analytic | 7.46 → **9.44** | **yes** |
| SVD (optimal) | 7.46 → **9.44** | **yes** |
| second singular pair | 13.04 → **48.76** | no |
| random pair | 1584, 324, 379, 537, **668** | no |

The second-pair control lands on **48.76 — exactly the unbordered value** at the top rung.
Bordering in the wrong direction is asymptotically worth nothing at all. The random control's
first rung is an outlier of the draw; from the second onward it rises monotonically, ending
70× the analytic border. Neither saturates in any of the five classes, which is what makes
"bordering fixes it" a measurement.

## 7. The ceiling — pre-committed as clause T-6, before any number existed

**A bounded bordered tail is not a certificate.** What is measured here is the weighted `ℓ¹`
operator norm of the inverse of *the tail block plus one border row and one border column*,
as the number of retained modes grows.

In a certificate that border is a **new unknown** — the far-field amplitude — and it needs

* its own **column in the finite block**,
* its own contribution to **`Y₀`**,
* and a **matching condition** between the spectral tail and the asymptotic expansion.

**None of that is written here.**

And the object is still the **`a = 0` CLM linearisation**: one mode, analytic, in every class
considered. Leg 51 was careful that a *wall* there bounds the difficulty for
`HL_S2_nonsymmetric` from below rather than above. The same asymmetry applies to a *success*:
this bounds it from below too. **Nothing is claimed about `HL_S2_nonsymmetric`.**

The constant is also not small — 9.44 and 11.37, against a `Z₂` of 79.5 from leg 51. Whether
the assembled polynomial closes with those numbers is a different question from whether the
term is finite, and only the second was asked here.

## 8. What moved and what did not

**Moved:** the `ℓ¹`-Fourier route to a certified `L1` was closed by leg 51 and is open again,
with a named repair, a mechanism, a measured constant, and a prediction that was made before
the measurement and held.

**Did not move:** `L1` is still uncertified, the target object has still never been touched by
this machinery, `L2` and `L3` are still Chen–Hou's, `L4` is still out of reach by Wall 2.
**No link of the L1→L4 chain moved. Clay odds unchanged at ~0.05%.**

## 9. Reproduce

```bash
.venv/bin/python -u experiments/p2_route_t_v1_border.py   # 154 s
.venv/bin/python writeup/4_p2_lottery/p2_route_t_v1_evidence.py   # fig47
.venv/bin/python test_spectral_certificate.py
```

Pre-committed clauses: **6/6** — `T0` novelty pass first and it can only narrow,
`T1` the gate on admissible classes, `T2` analytic against optimal, `T3` two negative
controls diverge, `T4` alignment reported at every rung, `T5` the Fredholm side stated before
the ladders, `T6` the ceiling written before the numbers.
