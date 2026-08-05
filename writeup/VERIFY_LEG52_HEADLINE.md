# VERIFY — leg 52 (Route-T v1), re-measured before `TC` builds a stage on it

*Agent: VERIFIER. Branch `verify/leg52-headline`. Script: `experiments/verify_leg52_headline.py`
(new; verification only, writes nothing under `writeup/data`). Nothing leg 51 or leg 52
produced was edited. Lesson 85: re-measure your own headline before building a stage on it,
and ablate the MECHANISM, not just the effect.*

---

## ⚠ URGENT FOR `LEG` (branch `leg/tc-v1`) — READ BEFORE ASSEMBLING TC-2

**TC-2's two inputs are quoted from two DIFFERENT and MUTUALLY EXCLUSIVE weight classes,
and one of them is the class the plan bans.**

`CONTINUATION_PROMPT.md` Directive 1, TC-2, says: *"Leg 51 gave `Y₀ = 0` exactly,
`Z₁ = 1.44e−10`, `Z₂ = 79.5` — on the finite block alone. Leg 52 gives a tail constant of
9.44 / 11.37. … Assemble and report whether `Z₂r² − (1−Z₁)r + Y₀ ≤ 0` has a root."*

Checked against `writeup/data/p2_route_l1_v2_spectral.json`, `S3_terms.finite_block`:

| K | class | `Y₀` | `Z₁` | `‖A‖_w` | `Z₂` |
|---|---|---|---|---|---|
| 256 | **algebraic `s = 1.0`** | 0 | **1.4415e−10** | 19.863 | **79.454** |
| 64 | flat `s = 0` | 0 | 1.5867e−10 | 359.02 | **2154.14** |
| 64 | algebraic `s = 1.0` | 0 | 7.1765e−12 | 15.986 | 63.945 |
| 256 | flat `s = 0` | 0 | 1.1805e−08 | 1632.98 | 9797.89 |

`Z₁ = 1.44e−10` and `Z₂ = 79.5` are the **`K = 256`, `s = 1.0`** row and **only** that row.
Leg 52's tail constants 9.44 and 11.37 are **`K = 64`, `s = 0` and `s = 0.3`**. `s = 1.0` is
exactly the exponent at which leg 52 measured bordering to **fail** (9.89 → 20.51, still
growing), and `plan_of_record.py` bans tuning `s` toward it. **Putting 79.5 in the same
polynomial as 9.44 is putting a finite-block constant from a class with an unbounded tail
next to a tail constant from a class whose finite block is 27× worse.**

The numbers TC-2 actually needs, recomputed here from
`solver.spectral_certificate.finite_section_inverse_norm` / `quadratic_bound`
(`Z₂ = 2‖A‖_w · Q`, which reproduces every leg-51 row to 4 digits):

| K | `s = 0` (admissible) | `s = 0.3` (admissible) | `s = 0.394` (boundary) | `s = 1.0` (banned class) |
|---|---|---|---|---|
| 32 | ‖A‖ 165.4 / **Z₂ 992.5** | 75.4 / **395.9** | 59.3 / 299.3 | 13.8 / 55.2 |
| 64 | 359.0 / **2154.1** | 134.8 / **707.5** | 99.8 / 503.6 | 16.0 / 63.9 |
| 128 | 768.8 / **4612.6** | 236.5 / **1241.2** | 164.6 / 830.1 | 18.0 / 71.9 |
| 256 | 1633.0 / **9797.9** | 410.3 / **2153.8** | 268.1 / 1352.3 | 19.9 / 79.5 |

**Leg 51 never computed the finite block at `s = 0.3` at all** — its `S3_terms.finite_block`
only carries `flat`, `algebraic s=1`, `geometric 1.1`. So the `s = 0.3` column above is new
here and should be recomputed inside TC's own runner, rigorously, not lifted from this file.

Two consequences `LEG` should state explicitly rather than absorb silently:

1. **In the admissible classes `‖A‖_w` grows with `K`** — flat `165 → 359 → 769 → 1633`
   (≈ `K^{1.0}`), `s = 0.3` `75 → 135 → 236 → 410` (≈ `K^{0.82}`) — whereas at `s = 1.0` it
   is nearly flat (`13.8 → 19.9`). The finite-block side and the tail side want opposite
   weight classes, which is the *same* trade-off leg 51 found, now moved from the tail to
   `‖A‖`. TC-2 must report `Z₂` **at the `K` it actually uses, in the class it actually
   uses**, and say which `K` it picked and why.
2. **`Y₀ = 0` makes the gate degenerate as posed.** With `Y₀ = 0` the polynomial
   `Z₂r² − (1−Z₁)r + Y₀ ≤ 0` has roots `r = 0` and `r = (1−Z₁)/Z₂ > 0` for *any* finite
   `Z₂` whenever `Z₁ < 1`. So "does it have a root" is **not** a test of `Z₂` or of the tail
   constant at all — it is the single question **is the assembled `Z₁` (finite block + tail,
   with the border's coupling) below 1?**, plus TC-3's border defect making `Y₀` nonzero.
   A tail constant of 9.44 entering `Z₁` additively would fail on its own. **If TC reports
   "the polynomial closes" while `Y₀` is still exactly 0 and the tail term has not entered
   `Z₁`, the gate has been answered vacuously.** Please state where in the polynomial the
   9.44 lands.

Everything else in Part A below is **confirmed**.

---

## PART A — leg 52's headline, re-measured

### A.1 Prose vs curated JSON — every headline number CONFIRMED

`writeup/data/p2_route_t_v1_border.json` against `BLOG_P2_ROUTET_V1.md`,
`TECHNICAL_P2_ROUTET_V1.md` and `PHASE2_P2_NOTES.md` §41:

| claim | JSON | verdict |
|---|---|---|
| flat `s=0` unbordered 4.06 → 48.76, `M^{+1.085}` | 4.06349 → 48.76190, exp 1.08478 | ✅ |
| flat `s=0` bordered 7.46 → 9.44, `M^{+0.100}` | 7.45592 → 9.43864, exp 0.10047 | ✅ |
| `s=0.3` unbordered 3.03 → 20.67, `M^{+0.837}` | 3.02851 → 20.66900, exp 0.83701 | ✅ |
| `s=0.3` bordered 8.09 → 11.37, `M^{+0.147}` | 8.08703 → 11.36962, exp 0.14682 | ✅ |
| `s=0.394` 2.77 → 16.04 / 8.30 → 12.16, exps 0.765 / 0.165 | 2.77208 → 16.04215 / 8.30209 → 12.15572, 0.76462 / 0.16481 | ✅ |
| `s=1.0` 1.64 → 3.94 / 9.89 → 20.51, exps 0.379 / 0.319 | 1.63735 → 3.93593 / 9.89287 → 20.50574, 0.37939 / 0.31852 | ✅ |
| `s=1.5` 2.41 → 11.54 / 11.44 → 31.81, exps 0.681 / 0.448 | 2.41044 → 11.53580 / 11.44016 → 31.81061, 0.68136 / 0.44765 | ✅ |
| flat increments `0.864 → 0.616 → 0.369 → 0.133` | 0.86370, 0.61649, 0.36929, 0.13325 | ✅ |
| `s=0.3` increments `1.212 → 1.019 → 0.738 → 0.314` | 1.21182, 1.01906, 0.73803, 0.31367 | ✅ |
| kernel `m^{−2.0024}`, cokernel `m^{+1.0012}` | −2.0023629, +1.0011766 | ✅ |
| `σ_min` 2.71e−1 → 8.54e−3, `σ_2` 2.092 → 1.652 (flat) | 0.27054 → 0.00854, 2.09202 → 1.65241 | ✅ |
| analytic/SVD 1.000, 1.007, 1.012, 1.130, 1.383 | 0.99999, 1.00704, 1.01201, 1.13006, 1.38251 | ✅ |
| alignment 1.00000 / 0.99996 / 0.99991 / 0.99300 / 0.90209 | 0.9999960, 0.9999587, 0.9999149, 0.9929962, 0.9020871 | ✅ |
| `s=1.5` alignment flat in `M`: 0.90378 → 0.90209 | 0.90378 → 0.90209 | ✅ |
| random control 1584, 324, 379, 537, 668; "70× the analytic" | 1583.66 … 668.36; 668.36/9.4386 = 70.8 | ✅ |
| runtime 154 s | `elapsed_s` 153.858 | ✅ |
| leg 51 cross-check: flat unbordered at `M = 320, 576, 1088` | leg 51 JSON 4.0635 / 8.1270 / 16.2540 — identical | ✅ |

`TECHNICAL` §0 quotes the kernel as `m^{−2.007}` while §2 quotes `m^{−2.0024}`. Both are
correct and both are sourced: `−2.00685` is leg 51's `homogeneous_mode_exponent` (fitted from
mode 1), `−2.00236` is leg 52's `fredholm_sides` (fitted over `m > 200`). Not a discrepancy,
but the two appear four lines apart with no note that they are different fits.

### A.2 Negative controls — CONFIRMED, with one scoping caveat

* **Second singular pair lands exactly on the unbordered value: CONFIRMED, in the flat
  class.** `48.761904761904674` vs `48.76190476190467`, relative difference `1.5e−16`.
  `TECHNICAL` §6 states this inside a table explicitly labelled "flat class", which is
  correct. **`BLOG` §"What came out" does not scope it** — *"The wrong-but-plausible one
  converges to exactly the unrepaired number"* — and the equality is a flat-class fact only:
  second/unbordered at the top rung is `1.000` (flat), `1.744` (`s=0.3`), `2.256` (`s=0.394`),
  `9.514` (`s=1.0`), `3.360` (`s=1.5`). Minor, but it is a blog claim that is false in four of
  the five classes as written.
* **Both controls diverge in all five classes: CONFIRMED** (`saturating: false` on all ten
  `second_shape` / `random_shape` entries; independently reproduced).
* **Analytic/SVD 1.000 and 1.007 in the admissible classes: CONFIRMED.**
* **Alignment → 1.00000 where the repair works, flatlines at 0.902 where it does not:
  CONFIRMED**, and the flatness is real — the `s = 1.5` alignment moves by 0.0017 across a
  10× range in `M` while the flat-class one converges to 1 to 6 digits.

### A.3 Things the prose reports selectively (not errors, but a stage should not inherit them)

1. **The `M` ladder is not geometric.** `320, 576, 1088, 2112, 3136` has step ratios
   `1.80, 1.89, 1.94, 1.49`. The last increment is therefore over a step ~25% shorter in
   `log M` than the others, so "the increments fall" is partly a step-size effect and the
   `saturating` flag in the driver (`inc[-1] < 0.5·inc[0] and inc[-1] < 0.5`) inherits it.
   Normalising by `Δlog M` is done in `experiments/verify_leg52_headline.py` §V5 — see A.4.
2. **`TECHNICAL` §3 says the `s = 1` increments *rise* across the ladder,
   `2.44 → 2.92 → 3.25`, and omits the fourth, `2.01`** — which falls. `PHASE2_P2_NOTES.md`
   §41 gets this right ("before the last rung"); the TECHNICAL write-up dropped the
   qualifier. The conclusion is unaffected (the fitted exponent is `+0.319` and the value
   still doubles), but the sentence as written in TECHNICAL is not what the data says.
3. **At `s = 1.0` and `s = 1.5` bordering makes the tail norm WORSE, not merely
   unhelpful** — `20.51` vs unbordered `3.94`, and `31.81` vs `11.54`. Neither write-up says
   this. It strengthens rather than weakens T-5's story (a border in a direction that is not
   a kernel of the space you are in is a perturbation, not a repair), and it is the sharper
   statement of the mechanism.
4. **`Y₀` and the tail constant have never been in the same units.** See the urgent section.

### A.4 MECHANISM ABLATIONS (lesson 85) — the constant's convention-dependence

The mechanism claim under test is *"the repair is: add the far-field amplitude as an
unknown"*. `bordered_tail_inverse_norm` implements it as

```
B = [[T_w, u], [v^T, 0]],   v = h·w,  u = u_left·w,  both normalised in the EUCLIDEAN norm,
‖B^{-1}‖ = max column sum of |B^{-1}|   (weighted l^1, border entry given weight 1)
```

Two conventions are baked in, and **`‖B^{-1}‖` is not invariant under either**:

* **Scale.** Rescaling `u → cu` scales the last row of `B^{-1}` by `1/c`; rescaling `v → dv`
  scales its last column by `1/d`. So the reported 9.44 is tied to `‖u‖₂ = ‖v‖₂ = 1`, while
  the norm being measured is weighted `ℓ¹`. In a certificate the convention is *not* free —
  it is fixed by the norm on the augmented space `(modes, amplitude)`, and the driver's
  choice does not correspond to any stated such norm. **This is the number TC-2 will carry,
  so TC must fix and state the augmented norm before quoting 9.44.**
* **Adjoint.** In scaled coordinates `T_w = W T W^{-1}` the left null vector is `u_left/w`,
  not `u_left·w`; the driver uses `u_left·w`. Both give an invertible border (their pairing
  with the kernel is nonzero), and the `analytic/SVD = 1.000` result says the driver's choice
  is essentially optimal in the flat class — where `w ≡ 1` and the two coincide. The
  distinction only bites for `s > 0`, i.e. exactly at `s = 0.3`, where the ratio is 1.007.
  The write-ups call `u` "the adjoint"; strictly it is not.

Neither of these is a claim that the saturation is wrong. They are a claim that **the constant
is not yet a well-defined quantity**, which matters precisely because TC-2's job is to put it
in a polynomial with `Z₂`.

### A.5 ABLATION RESULTS — the MECHANISM survives everything; the CONSTANT survives nothing

`.venv/bin/python experiments/verify_leg52_headline.py` (2223 s under load).
**20/20 numeric checks pass, 0 gaps.**

**(V1) Exact reproduction.** Recomputing all five ladders — `unbordered`, `analytic`, `svd`,
`second`, `random`, `sigma_min`, `alignment` — directly from `solver/spectral_certificate.py`
matches the committed JSON to a **maximum relative deviation of `2.2e−13`**. A full re-run of
`experiments/p2_route_t_v1_border.py` (to a scratch path; the committed JSON was not touched)
is byte-comparable: the only differing entries are three floats at `~2e−12` (LAPACK SVD
threading), and `verdict` / `gate_admissible_classes_saturate` are identical.
**Leg 52 is reproducible.**

**(V3) Normalisation ablation — the saturation is convention-independent, the constant is
not.** Flat class / `s = 0.3`, top rung `M = 3136`:

| normalisation of `u`, `v` | flat `s = 0` | fitted `M`-exponent | `s = 0.3` | exponent |
|---|---|---|---|---|
| Euclidean (**as shipped**) | **9.44** | +0.101 | **11.37** | +0.147 |
| `ℓ¹` | 92.63 | +0.069 | 139.96 | +0.155 |
| `ℓ^∞` | 2.82 | +0.112 | 3.06 | +0.158 |
| `u` in `ℓ¹`, `v` in `ℓ^∞` (the pairing weighted-`ℓ¹` actually induces) | **2.91** | **−0.015** | **3.26** | +0.020 |

**Every convention saturates.** The gate answer is robust. But the constant spans
**2.8 → 92.6, a factor of 33**, and the shipped 9.44 is an arbitrary point in that range.
The convention a weighted-`ℓ¹` certificate would actually induce — the unknown measured in
the space, the equation measured in the dual — gives **2.91, three times smaller than the
headline and essentially perfectly flat in `M` (exponent −0.015)**. That is *better* news
for TC than the headline, not worse; it is still a number TC has to derive rather than
inherit.

**(V4) Adjoint convention — the shipped number is CONSERVATIVE.** Using the true left null
vector in scaled coordinates (`u_left/w`) instead of the shipped `u_left·w` gives, at
`s = 0.3`, **11.2892** against the SVD optimum **11.2902** — i.e. `analytic/SVD = 1.0001`,
not the 1.007 the write-up reports. In the flat class the two coincide identically. So
**T-2's "the analytic border achieves the optimum" is if anything understated**; the shipped
convention is the only reason the ratio is not 1.000 in all admissible classes.

**(V5) Ladder extension to `M = 6208` — saturation CONFIRMED and strengthened.**

```
flat s=0    M  320    576   1088   2112   3136   4160   6208
  bordered  7.456  8.320  8.936  9.305  9.439  9.507  9.577   exp +0.080 (was +0.100 on 5 rungs)
  inc/dlogM 1.469  0.969  0.557  0.337  0.243  0.175           ~ M^{-0.96}
  unbordered 4.06  8.13  16.25  32.51  48.76  65.02  97.52     exp +1.066
s=0.3
  bordered  8.087  9.299 10.318 11.056 11.370 11.549 11.751   exp +0.123
  inc/dlogM 2.062  1.602  1.113  0.794  0.634  0.505           ~ M^{-0.67}
```

The log-derivative falls like `M^{-0.96}` (flat) and `M^{-0.67}` (`s = 0.3`) — both summable,
so the sequence converges rather than creeping. The fitted exponent *falls* when the ladder
is extended (`0.100 → 0.080`), which is what a saturation does and a power law does not.
This also disposes of the concern in A.3(1): the ladder's non-geometric last step was not
what produced the falling increments.

**(V6) `K`-DEPENDENCE — NOT REPORTED BY LEG 52, AND IT IS LOAD-BEARING FOR TC.** The whole
leg is at `K = 64`. Extending (analytic border, at `M = 6208` for `K ≥ 64`):

| `K` | flat `s = 0` | `s = 0.3` | `M`-exponent, flat |
|---|---|---|---|
| 32 | 6.72 (at `M`=3136) | 8.23 | +0.051 |
| 64 | **9.58** | **11.75** | +0.080 |
| 128 | 13.39 | 16.13 | +0.148 |
| 256 | 18.39 | 21.58 | +0.171 |

Each `K` still saturates (`inc/dlogM` falls monotonically at 128 and 256 as well), so the
gate answer is unchanged. But **the tail constant grows like `K^{0.46}`, i.e. roughly
`√K`, and it does not saturate in `K`.** Neither `BLOG`, `TECHNICAL` nor `§41` mentions any
`K`-dependence; all three quote 9.44 / 11.37 flat.

Combined with the urgent section's finding that `‖A‖_w` on the finite block grows like `K^{0.8–1.0}` in the
same admissible classes, **both sides of the certificate degrade with `K` in the classes
where the tail works.** TC must pick one `K`, and at `K = 256` the tail constant is 18.4,
not 9.44.

**(V7) THE BORDER'S OWN DEFECT — MEASURED, AND IT IS EXACTLY THE TRUNCATION BOUNDARY.**
This is TC-3's quantity, and it turns out already to have a clean answer. `T h` is
**exactly zero on every interior row** (`2.8e−15`, flat, all `M`); the entire residual sits
in the **last row**, the artificial truncation at `M`. Likewise `u^T T` is exactly zero on
every interior column and the entire residual sits in **column 0**, the one column reaching
the mode `K` outside the block. Both decay exactly like `1/M`:

| `M` | 576 | 1088 | 2112 | 3136 | 6208 |
|---|---|---|---|---|---|
| `‖T h‖₂/‖h‖₂` (all in the last row) | 1.066 | 0.5635 | 0.2902 | 0.1954 | 0.0987 |
| `M ×` that | 614 | 613 | 613 | 613 | 613 |
| `‖T h‖₁/‖h‖₁` | 1.23e−1 | 6.15e−2 | 3.08e−2 | 2.05e−2 | 1.03e−2 |
| `‖u^T T‖_∞/‖u‖_∞` (all in column 0) | 3.561 | 1.884 | 0.970 | 0.653 | 0.330 |
| `M ×` that | 2051 | 2049 | 2048 | 2048 | 2048 |

So the analytic far-field mode is an **exact** kernel of the tail recursion, and its two
defects are precisely the two boundary equations, each `≈ 613/M` and `2048/M`. For
comparison `σ_min` decays like `M^{-1.5}` (`2.71e−1 → 8.54e−3`), so the **defect/`σ_min`
ratio grows like `M^{+0.5}`** — the border is a better and better kernel in absolute terms
and a worse and worse one relative to the operator's smallest scale. TC-3 should quote
`613/M` and `2048/M` rather than treat the border defect as uncomputed; whether the
*matching-condition* residual (a different object — series against asymptotic expansion) has
the same magnitude is TC-3's actual job.

### A.6 PART A VERDICT

**Leg 52's headline is CONFIRMED.** Every number in `BLOG_P2_ROUTET_V1.md`,
`TECHNICAL_P2_ROUTET_V1.md` and `PHASE2_P2_NOTES.md` §41 matches the curated JSON; the
runner reproduces to `2e−12`; all four negative controls behave as claimed; the saturation
survives a 2× ladder extension, four different normalisation conventions, both adjoint
conventions and `K ∈ {32, 64, 128, 256}`. The `T-5` mechanism (kernel/cokernel swapping at
`s = 1`) is reproduced exactly. **The gate answer stands.**

**Three things a stage must not inherit uncritically:** (i) the reported constant 9.44/11.37
is convention-dependent by a factor of 33 and is *not* the number the natural weighted-`ℓ¹`
pairing gives (that is 2.91/3.26); (ii) it grows like `√K` and leg 52 reports one `K`;
(iii) TC-2's `Z₂ = 79.5` comes from the one weight class where the tail is unbounded — the
urgent item at the top of this file.
