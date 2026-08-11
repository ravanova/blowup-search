# Route-DWM v1 — a per-constant width ledger of BCG's r-dominance argument (leg 305)

**Gate answer: YES.** The re-derivation reproduces both window endpoints through an independent
code path and yields a per-constant width ledger naming the costliest constant.

**Data:** `writeup/data/p2_route_dwm_v1.json`. **Runner:** `experiments/p2_route_dwm_v1.py`.
**Figure:** fig82, `writeup/figures/fig82_route_dwm_v1_ledger.png`.
**Source:** Buckmaster, Cao-Labora, Gómez-Serrano, [arXiv:2208.09445](https://arxiv.org/abs/2208.09445),
*Smooth imploding solutions for 3D compressible fluids*, Forum of Math. Pi **13** e6 (2025);
e-print tarball md5 `45ea63c45a1a199ecfb4dc4a15431600`, file `RadialImplosion31_FinalArxiv.tex`.
Every `l.NNN` below is a line number in that file.

---

## 1. What was open

Leg 266 (verified and corrected by leg 300) fixed the certificate obligation at the stability
step with `F_dis` retained and `r` **outside** the dominance window `(1.1666667, 1.1909830)` —
a window `6.854×` narrower than the target window `(1, 7/6]`, closed form `(7+3√5)/2`. Nobody
knew whether that width is **sharp** for BCG's argument or an artifact of one generous
intermediate constant. This leg re-derives the window tracking every intermediate constant and
measures which constant costs the most width.

Leg 240 had already banked the endpoints, the width, the `δ_dis` margin and the γ-ceiling.
Those are used here as an **internal reference to be reproduced through a different code path**,
never re-claimed as this leg's findings.

## 2. The independent path (pre-registered before measuring)

A reproduction through the same formula is not a reproduction. Both endpoints are re-derived
from **different displayed equations** than legs 240 and 300 used.

| endpoint | legs 240/300 | **leg 305** |
|---|---|---|
| upper `r*` | BCG's closed form `\eqref{eq:rstar}` (l.352–358), evaluated | the **root** of the upstream Jacobian quantity `D_{Z,1}(r,γ) = −4 + (1+γ)(r−1)/(γ−1) + R₂ = 0` from `\eqref{eq:k_asquotientDZ1}` (l.600) — the quantity whose vanishing is what *causes* `k → ∞` (Lemma `\ref{lemma:k}`, l.579–583, proof l.605), with `R₂` from `\eqref{eq:def_R2}` (l.547–551) and `R₁` from `\eqref{eq:R1}` (l.526–528) |
| lower `2γ/(γ+1)` | CGSS (1.8) | the prefactor exponent read off BCG's **own displayed PDE** `\eqref{eq:main}` (l.483), `e^{(2−r+(1/α)(1−r))s}`, whose sign condition is `\eqref{eq:delta:dis}` (l.489–491), **solved** rather than quoted |
| arithmetic | IEEE double | 60-digit `decimal` throughout; float appears only as a deliberately contrasted control |

`\eqref{eq:rstar}` is evaluated in exactly one place — check T4 — purely as the cross-check
target. Nothing else consumes it.

## 3. Reproduction: every gate-triggering tolerance passes

| check | measured | tolerance | verdict |
|---|---|---|---|
| T1 lower endpoint vs leg 240's `1.1666667` | dev `3.333e-8` | `≤ 5e-8` | **pass** |
| T1 upper endpoint vs leg 240's `1.1909830` | dev `5.625e-9` | `≤ 5e-8` | **pass** |
| T2 γ-ceiling vs leg 240's `2.154700538379` | dev `2.515e-13` | `≤ 5e-13` | **pass** |
| T3 closed forms (`r*=(7−√5)/4`, `r_dis=7/6`, ratio `(7+3√5)/2`, width `(7−3√5)/12`) | dev `0`, `1e-59`, `3.37e-57`, `0` | `≤ 1e-40` | **pass** |
| T4 root-solve vs `\eqref{eq:rstar}` over 12 γ, both branches | max dev **exactly `0`** | `≤ 1e-40` | **pass** |

Measured window, 60 digits:

```
lower  1.16666666666666666666666666666666666666666666666666666666666
upper  1.19098300562505257589770658281718094113984541009711856893228
width  0.02431633895838590923103991615051427447317874343045190226562
ratio  6.85410196624968454461376050309691435316092753941728858640298
γ-ceil 2.15470053837925152901829756100391491129520350254025375203704
```

The ratio is `(7+3√5)/2`, agreeing with leg 300's re-derivation. It is **not** `6.855`; that
transcribed digit is not used anywhere in this leg's artifacts.

The γ-ceiling deserves a note. Solving `r*(γ) = 2γ/(γ+1)` requires `r*` on **both** of BCG's
branches, and the root-solve selects the branch by measurement rather than by reading
`\eqref{eq:rstar}`: for `1 < γ < 5/3`, `D_{Z,1}` reaches zero only *at* the realness edge, while
for `γ ≥ 5/3` it crosses zero strictly inside the domain. That this branch structure falls out
of the root-solve, and that T4 then agrees with the two-branch closed form to **exactly zero**
over 12 γ values, is the strongest single piece of evidence that the transcription of `R₁`,
`R₂` and `D_{Z,1}` is faithful.

### The `r=1` conditioning trap, reproduced and diagnosed

BCG state at l.603 that `R₂ = 0` at `r = 1`, hence `k(1) = 1`. The radicand is a sum of terms
of magnitude up to `24.528` cancelling to exactly zero, so in IEEE double it evaluates to
`1.2212453270876722e-14` of rounding dust and the square root costs half the digits:

* float: `|k(1) − 1| = 1.381374710174299e-07`, failing a `1e-9` tolerance — reproducing leg
  302's measured `1.29e-07` to within the difference in probe arithmetic;
* 60-digit: `R₂` radicand at `r=1` is `0.000` **exactly**, and `|k(1) − 1| = 0` exactly.

This was **pre-registered as an expected float failure** and it decides nothing: the float
number is emitted under `conditioning_trap`, labelled diagnostic, and is not an input to any
verdict. A conditioning artifact reported as a sharpness finding would have been this leg's
serious failure mode; it was diagnosed before it was believed.

## 4. The ledger

Eleven named constants, each appearing in a displayed BCG equation, each perturbed one at a
time multiplicatively with everything else held fixed, and the window recomputed at `γ = 7/5`.
`move_to_close` is the relative change in that one constant for which the dominance window
becomes as wide as the target window `1/6` — i.e. the deficit falls to `1×`.

| constant | BCG value | locator | `dW/dln c` | % of window per 1% | `move_to_close` | class |
|---|---|---|---|---|---|---|
| **C1 `c_lap`** | **2** | `\eqref{eq:main}` l.483 | **−0.333333** | **−13.708** | **−42.705%** | EXACT_IDENTITY |
| C2 `c_r` | 1 | l.483 | +0.194444 | +7.983 | +83.383% | EXACT_IDENTITY |
| C3 `c_dens` | 1 | l.483 | +0.138889 | +5.665 | +702.492% | EXACT_IDENTITY |
| C4 `α = (γ−1)/2` | 0.2 | l.483 | −0.138889 | −5.702 | −87.539% | EXACT_IDENTITY |
| C5 `c₄` | −4 | l.600 | — | — | unreachable | EXACT_IDENTITY |
| C6 `c_lin=(1+γ)/(γ−1)` | 6 | l.600 | — | — | unreachable | EXACT_IDENTITY |
| C7 `R₂` scale | 1 | l.547–551 | — | — | unreachable | EXACT_IDENTITY |
| C8 `a₂` | −2.432 | l.548–550 | — | — | unreachable | EXACT_IDENTITY |
| C9 `a₁` | 9.472 | l.548–550 | — | — | unreachable | EXACT_IDENTITY |
| C10 `a₀` | −6.528 | l.548–550 | — | — | unreachable | EXACT_IDENTITY |
| C11 `R₁`-coupled group | `grp(r)` | l.548–550 | — | — | unreachable | EXACT_IDENTITY |

**Costliest constant (pre-registered rule: smallest `|move_to_close|`): `C1_c_lap`, the
Laplacian's own scaling weight, at −42.705%.**

### Why `c_lap` is the costliest, and why it is not generous

Naming the constant is not the realization; naming *why* it is the one is. At `γ = 7/5` the
lower endpoint is the root of `2 − r + (1/α)(1−r)`, and `c_lap = 2` is the `2` in that
expression. It is not an estimate, a Sobolev constant, or a bookkeeping convenience. It is the
number of spatial derivatives in `νΔ`, entering through the parabolic scaling of the
Laplacian under BCG's self-similar change of variables. Its width elasticity is `−13.708%` of
the window per `1%` move, precisely because it is the additive constant term of the exponent
rather than a coefficient of `r`.

**[CORRECTED 2026-08-12, leg 336, measured against this leg's own ledger JSON
(`writeup/data/p2_route_dwm_v1.json`, `ledger[]`, field `M2_pct_of_window_per_1pct`).]** The
sentence originally read *"Its width elasticity is the largest of any constant — `−13.708%` of
the window per `1%` move"*. That is **false on the ledger's own metric**: `C9_a1`'s elasticity is
`M2_pct_of_window_per_1pct = −31.058%`, `2.27×` larger in magnitude than `C1`'s `−13.708%`. The
table above prints `—` for `C5`–`C11` because their *reachable* `move_to_close` is undefined
(their far side is capped) — but the JSON still computes a one-sided `M2` elasticity for every
row from whichever perturbation direction is non-flat, and on that column `C1` is not the
largest; `C9_a1` is (`|−31.058|`), ahead of `C1` (`|−13.708|`), `C8_a2`'s and `C10_a0`'s and
`C6_c_lin`'s and `C5_c4`'s and `C7_R2scale`'s rows (all smaller in magnitude). `C1_c_lap` remains
the costliest constant **only under the pre-registered rule stated above (smallest
`|move_to_close|`), which is a narrower and different metric than elasticity** — see §6 for
whether the SHARP verdict depends on either claim.

Its `move_to_close` has a closed form, and the runner's bisected value agrees with it to `1e-40`:

```
c_lap*  = (9 − 3√5)/2 = 1.14589803375031545538623949690308564683907246058271141359365
s*      = (9 − 3√5)/4 = 0.572949016875157727693119748451542823419536230291355706796825
```

Since `c_lap = 2s` for the operator `ν(−Δ)^s`, closing the deficit by moving this constant means
replacing `νΔ` with **hypodissipation** `ν(−Δ)^s` at `s = 0.5729…`, below the `s = 1` of the
actual Navier–Stokes viscosity and indeed below `s = 1/2`. **That is a different PDE, not a
sharper proof of the same one.** This is what "sharp" means here in operational terms.

### The upper endpoint cannot be moved at all, and that is a measurement

Seven of the eleven constants — every constant living in `D_{Z,1}` or `R₂` — report
`unreachable`, and the reason is structural rather than numerical. At `γ = 7/5`:

```
R₁ radicand at r*        = 3E-59          (i.e. zero)
R₁ radicand roots        = 1.19098300562505257589770658281718094113984541009711856893228
                           2.30901699437494742410229341718281905886015458990288143106773
D_{Z,1} at realness edge = −1.639E-30     (i.e. zero)
```

`r*` is **exactly the smaller root of BCG's `R₁` radicand** — that is, exactly the point where
`P_s` and `P̄_s` merge, a saddle-node of the phase portrait. It is not an estimate of a
threshold; it is a discriminant. Consequently the upper endpoint is pinned: perturbing any
`D_{Z,1}`/`R₂` constant can push `D_{Z,1}`'s zero *below* the edge, lowering `r*`, but can never
push it above, because `R₁` ceases to be real there and `P_s` ceases to exist. **`r*` sits at a
maximum of every one of these seven one-parameter families.**

The measurement that establishes this, rather than asserting it, is the response exponent. The
runner perturbs by `ε = 1e-5` and `1e-6` and fits `|ΔW| ∼ ε^p`:

* six of the seven capped rows (`C5`–`C10`): `p = 1.996…–1.9996`, i.e. **`p = 2`** — a
  *stationary* maximum, not a kink;
* the four uncapped rows: `p = 0.9999…–1.0`, i.e. `p = 1`, as an ordinary derivative should be.

**[CORRECTED 2026-08-12, leg 336, measured against `ledger[]` fields `scaling_exponent_up` /
`scaling_exponent_dn` in `writeup/data/p2_route_dwm_v1.json`.]** The bullet originally read *"all
seven capped rows"*. `C11_aR1` is capped (`capped_r_star_at_a_maximum: true`) but reports
`scaling_exponent_up = scaling_exponent_dn = "flat"` — **neither** side shows the `p ≈ 2`
response; both are identically flat. `C11_aR1` is not a seventh instance of the `p = 2`
phenomenon; see the T6 correction below for the adjudication (inert-by-construction, not missing
data).

`p = 2` is forced by the geometry: `D_{Z,1}` meets zero at the edge with a **vertical** tangent,
because `R₁ ∼ √(edge − r)` there, so an `O(ε)` perturbation of any constant inside `D_{Z,1}`
moves the endpoint only by `O(ε²)`. `C11_aR1`'s row multiplies `R₁` itself, which **is** the
quantity that vanishes at `r*` (`R₁_radicand_at_r_star ≈ 0`, `structural_findings` in the JSON);
its term is `R₁ × (polynomial)`, and `R₁ = 0` at the evaluation point regardless of how the
polynomial factor is perturbed, so the row measures a derivative of a term that is identically
zero at `r*` — a different, degenerate case from the six genuine `p = 2` rows, not a data gap.

### A pre-registered tolerance that failed, reported rather than smoothed

Tolerance **T6** (elasticity linearity: the central-difference `dW/dln c` at `ε = 1e-5` versus
`ε = 1e-6`, relative deviation `≤ 1e-4`) **FAILS**, and it is reported as failing. T6 was
pre-registered as a non-gate-triggering diagnostic, and the diagnosis is exact: for six of the
seven capped rows, the central difference is itself `O(ε)` because one side is flat and the
other is quadratic, so halving `ε` halves it and the relative deviation is exactly `0.9`.
Measured: `0.8991`–`0.8999` for those six. An additional check declared as additional, **T6b**,
applies the same test to the four uncapped rows and passes at `~9e-15`.

**[CORRECTED 2026-08-12, leg 336, measured against `ledger[]` field `M1_linearity_rel_dev` in
`writeup/data/p2_route_dwm_v1.json`.]** The passage originally read *"for the seven capped rows
… Measured: `0.8991`–`0.8999` for all seven"*. `C11_aR1`'s `M1_linearity_rel_dev` is `0E-54` —
exactly zero, not `≈0.899` — because both its one-sided derivatives (`M1_one_sided_up`,
`M1_one_sided_dn`) are themselves exactly `0`, not merely small. **Adjudication: this is
inert-by-construction, not missing or broken data.** `C11_aR1`'s row is `R₁ × (9(γ−2)γ +
((2−3γ)γ+5)r + 5)`, and `R₁ = 0` at `r = r*` by the structural finding above (`R₁` radicand
`≈ 3E-59`, i.e. `R₁` itself vanishes there — this is the same fact that *defines* `r*` as the
saddle-node). Perturbing the polynomial factor by `±ε` multiplies a zero by `(1±ε)`, which stays
exactly zero to the runner's precision; there is no missing measurement, no broken perturbation,
and no undetected response — the term genuinely contributes nothing to `dW` at `r*`, unlike the
other six capped rows, whose one-sided derivatives are small but nonzero (Lesson 90 tell: `C11`
is a control that structurally cannot come out differently, which is exactly why it does not
belong to the "seven" count).

So T6's failure is not an arithmetic defect. It is the numerical signature of BCG's constants
sitting at a stationary maximum of `r*` — the same finding as the previous subsection, arriving
independently through a tolerance that was written down before the measurement.

## 5. The discrete sub-ledger

BCG's admissible speeds are not an interval. Lemma `\ref{lemma:k}` (l.583) makes
`k : [1, r*) → [1, ∞)` a bijection and the profiles live at `r_n := k⁻¹(n)` for **odd** `n ≥ 3`
(l.367–369). So the width deficit also has a counting form:

```
k(7/6) = 16.3479210516613384873990168461313841556225924879068376948995
```

**16 admissible speeds fall at or below the dominance threshold, 7 of them odd
(`n = 3,5,7,9,11,13,15`). BCG's Euler profiles at those seven speeds have no
Navier–Stokes counterpart under the dominance argument; the first odd speed that survives is
`n = 17`.** The continuum deficit `6.854×` and the discrete deficit "the first seven odd
profiles" are two readings of the same gap.

## 6. Verdict: sharp, on the pre-registered rule

The rule, fixed before measuring: **SLACK** iff at least one constant is classified `ESTIMATE`
*and* its `move_to_close` is within a factor 2 of unity. Otherwise **SHARP FOR BCG'S ARGUMENT
AS STATED**.

**All eleven constants classify as `EXACT_IDENTITY`.** Not one is an estimate, a Sobolev or
interpolation constant, or a numerically-tuned bound; each is a derivative count, an ideal-gas
exponent, a polynomial coefficient in a discriminant, or an algebraic combination of `γ`. There
is therefore no constant that a sharper argument could sharpen. The verdict is
**SHARP_FOR_BCG_ARGUMENT_AS_STATED**, and the named realization (lesson 91) is:

> The `6.854×` deficit is not the price of a generous estimate. It is the distance between two
> *exact* thresholds — a **derivative count** (`c_lap = 2`, the order of the Laplacian) and a
> **discriminant** (`r*`, the merge point of `P_s` and `P̄_s`). Both endpoints are rigid. Closing
> the deficit by moving the costliest constant means changing the operator to
> `ν(−Δ)^{0.5729…}`, i.e. solving a different equation.

**What this does and does not say.** It says the deficit cannot be reduced by sharpening any
constant *in this argument*. It does **not** say the deficit is irreducible: a different
argument — one that does not route the viscous term through pointwise domination by the
self-similar profile at all — is untouched by this ledger. Measuring the shape of an obligation
is not discharging it.

**[ADDED 2026-08-12, leg 336.]** The verdict above depends only on the `M4_class` field of all
eleven rows (`EXACT_IDENTITY`, unanimous) and on `move_to_close`. **Neither correction in §4
touches either input.** The elasticity correction (`C9_a1` at `−31.058%`, not `C1` at `−13.708%`,
is the largest-magnitude `M2_pct_of_window_per_1pct`) does not change any row's `M4_class`, and
`C1_c_lap` is unaffected as *costliest-by-`move_to_close`* because that metric was never
elasticity to begin with. The `C11_aR1` all-zero-row adjudication (inert-by-construction, not
missing data) removes one row from the "seven capped `p ≈ 2` / T6 `≈0.899`" count but changes no
row's `M4_class` and adds no `ESTIMATE`. **The SHARP verdict is UNMOVED by both corrections.**

## 7. Relation to leg 315 (Route-TMS)

Leg 315 landed the complementary question. It asked *what machinery could close this gap* and
identified the sonic-crossing `r`-tube of BCG's autonomous `(W,Z)` self-similar Euler ODE flow
as reachable by Taylor-model stepping but not by this repository's Newton–Kantorovich
apparatus, recording the same shortfall `6.8541019662496845446`. This leg asks *which constant
makes the gap that wide*. The two answers compose: **the costliest constant named here,
`c_lap = 2`, is the thing leg 315's proposed enclosure would have to beat** — and since `c_lap`
is a derivative count rather than an estimate, an enclosure cannot beat it by being tighter; it
would have to certify the domination on a region where `δ_dis < 0`, by a different mechanism.

Leg 315 also found the cost blocker, which matters for reading this leg's verdict: Zgliczyński's
ODE→PDE bridge assumes **dissipativity**, while BCG's rescaled system is **quasilinear
hyperbolic**. So even had this ledger come out *slack*, "slack" would not have meant
"reachable". It came out sharp, which if anything strengthens that reading.

## 8. Walls

**Wall 1 and Wall 2 stand.** Measuring the shape of an obligation is not discharging it; no
link of the L1→L4 chain moves. The object is 3D **compressible** Navier–Stokes (BCG, `γ = 7/5`),
which the source leg itself flagged as **not** the incompressible system the Clay problem asks
about. **Clay odds ~0.05%, unchanged.**
