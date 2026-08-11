# Where a certificate for this operator can live, and where it cannot: the space axis, mapped and closed

**Route PUB2, leg 186, v1. DRAFT — for the user's review. This leg's landing does not approve
it.**

> **This is the SECOND of two publication-scoping drafts, and it is a different document from
> the first.** [`TECHNICAL_P2_PUB1_V1.md`](TECHNICAL_P2_PUB1_V1.md) (leg 179) asks *why the
> method failed* in weighted `ℓ¹` — four separable causes, of which the `A₂₁` inequality is
> one. **This note asks a different question: given that it failed there, where else could a
> certificate for this operator possibly live?** The two notes share exactly one table (leg
> 127's `σ_min` ladder), which PUB1 uses as the proof of a theorem and this note uses as the
> measurement of one endpoint of an axis. They are not to be merged without a deliberate
> editorial decision.

**Status.** Assembled entirely from banked results; **nothing in it is new to the world**, and
its only contribution is arrangement. Every number is quoted from the JSON of the leg that
produced it — the provenance audit is [`writeup/novelty/leg_186.md`](../novelty/leg_186.md),
which lists each number against the file and key it was read from.

**What this note is not.** It is not a certificate, not a theorem about the Navier–Stokes
equations, and not a claim that any link of this project's `L1 → L4` chain has moved. None has,
in 275 legs (count current as of leg 276). The object throughout is the `a = 0` Constantin–Lax–Majda (CLM) steady
linearisation — an already-solved, already-published model — and every magnitude below bounds
the difficulty of the real target **from below, not above**.

**The sentence this note may not contain, and does not.** *"Xu proves the operator invertible,
therefore a certificate is possible."* That phrase was banned by the leg that read Xu at
primary source, for the reason given in §3.3, and the ban is inherited here.

---

## 0. The question, and why three results answer it and not one

A radii-polynomial / Newton–Kantorovich certificate is not built on an operator. It is built on
an operator **in a space**. Seven successive legs of this project failed to close such a
certificate for a 1D fluid transport model, and PUB1 anatomises the failure. This note asks the
question that survives the anatomy: **the failure happened in one space — is the space the
problem, and is there a better one?**

That question has an axis, and the axis now has four points on it, all measured, all banked:

| § | space | result | kind |
|---|---|---|---|
| 2 | weighted `ℓ¹` of Fourier coefficients, `w_k = (1+k)^s`, `s < 1` | `Z₁ ≥ 1` for **every** bounded approximate inverse | **theorem** (leg 127) |
| 3 | origin-`H²` on the line (Xu's realization) | structurally viable formulation — **capped at `a = 0` exactness**, with nothing transferring to the real target | scoping YES, **escalated not built** (leg 163) |
| 3.5 | origin-`H²`, **built** rather than scoped | the formulation closes as a formulation (`σ_min = 0.0908`, a monotone-decreasing ladder flat to **0.139 %** over a 16-fold truncation range — evidence of a positive limit, not a proved floor) **and** the block-diagonal `A` still fails leg 54's `Z₁` battery at best **140.72** where `< 1` is needed | construction gate **YES on both conjuncts, with one magnitude that says NO** (leg 176) |
| 4 | anything between them | no scale avoids both obstructions; the window has width **exactly zero** | scoping **NO** (leg 182) |

> **The convention note. The `σ_min` digits printed in this note are convention-relative; the
> property they are used for is not.** Recorded by leg 249 §10 (W5) and carried into
> [`p2_route_h2c_v1_construction_correction_leg268.json`](../data/p2_route_h2c_v1_construction_correction_leg268.json)
> as `convention_caveat_recorded_by_249`: the `X ⊕ ℂ` Gram puts unit weight on the border
> amplitude while the `X` block carries the bare Laguerre normalization (no `2π`, no half-line
> `½`). That is a **choice**. Sweeping that weight over `10⁻² … 10²` moves `σ_min` across
> **0.01086 … 0.13580 — a factor of 12.5** — and adopting Xu's own `y`-space normalization for
> the `X` block (i.e. carrying the `2π`) gives **0.0420** instead of **0.0908**.
> **[CORRECTED 2026-08-11, leg 280, per leg 277's verified finding.]** `0.0420` is Xu's
> Definition 4.1 *equivalent* full-line norm (`κ = 2π`); Definition 4.1's own *displayed*
> half-line definition (4.2) carries `π`, not `2π`, and gives **`0.057643`** instead
> (`‖R‖_X = 17.348`, not `23.792`) — **`1.37×` larger than `0.0420`**. Both are Xu-normalization
> readings; which one "Xu's own normalization" means was previously unresolved and is now named.
> **In the same
> breath, because it is what keeps this from touching any conclusion below:** the property leg
> 176's gate turns on — `σ_min` **bounded away from zero uniformly in the truncation** — **is
> invariant** under that weight, since a positive weight cannot send a positive limit to zero;
> and the only thing §§3–5 ever argue from is the *contrast in ladder behaviour* (flattens
> here, decays like `M^{−(1−s)}` there), which is likewise convention-invariant. Leg 249's own
> sentence was *"the digits are not invariant, and PUB2 quotes the digits without the
> convention."* **This note now quotes the convention**, and every later printing of `0.0908` /
> `0.090804` — in §3.2, §3.5, §4.5, §5(3) and §7 — points back to this paragraph rather than
> repeating it.

Read separately these are three leg reports. Read together they are one statement, and §5 is
that statement. The order below is the order a practitioner meets the decisions in: pick the
space, discover it is dead, look for a better one, ask whether anything in between helps.

**The fourth point was commissioned, and it has since landed.** A construction leg on the
origin-`H²` formulation (leg 176) was authorised and in flight at the time this note was
drafted; it had then committed **only its novelty pass** — no runner, no data, no gate answer —
and nothing was attributed to it or predicted for it. **It has now landed (`bb0f184`)**, and its
outcome is folded in at **§3.5** as the fourth data point, quoted from its own report. §3.4
preserves, unaltered, what was quotable at drafting; §3.5 is an addition on top of it, not a
rewrite of it.

**Two limits on that fold-in, stated here rather than discovered later.** (1) §§5–6 below were
written when the axis had three points and are **left as drafted**; they are the three-result
synthesis, and §3.5 says explicitly which of their sentences leg 176 makes more precise and
which it leaves standing. (2) The verification leg originally commissioned against leg 176
(leg 192) committed **only its own pre-registered novelty / prior-art pass** — no verification
runner, no re-derivation, no verdict — but **the independent re-derivation has since been done
and has reported**: leg 249 re-derived leg 176's construction in **exact rational arithmetic**
(its journal, novelty log and `p2_route_h2cv_v1_postconstruction.json` are **on `main`**, and
byte-identical to the originating branch `leg/249-h2cv2-v2` at `e9db984`, which is not itself an
ancestor of `main`), confirming both conjuncts and correcting two banked
values below the digits quoted here; a subsequent review pass re-pulled leg 249's figures from
that branch and matched them character for character. **Leg 176's numbers are therefore carried
here as leg 176's float64 measurements, with leg 249's exact tier as the independent check on
them** — the corrections are recorded at §3.5 and in
[`writeup/data/p2_route_h2c_v1_construction_correction_leg268.json`](../data/p2_route_h2c_v1_construction_correction_leg268.json).

---

## 1. Naming the axis honestly first, because the obvious framing is wrong

It is natural to picture `ℓ¹_w` and origin-`H²` as two points on one scale, with an
interpolation family running between them. **They are not.** The two spaces differ in **three
independent coordinates**, and this was the first finding of the leg that went looking for the
interpolant:

| | `ℓ¹_w` (§2) | origin-`H²` (§3) |
|---|---|---|
| domain | periodic circle, Fourier-coefficient truncation | the line `ℝ` |
| index | `ℓ¹` on the coefficient side (`p = 1`) | `L²` (`p = 2`) |
| side condition | algebraic weight `w_k = (1+k)^s` | origin regularity (`φ″ ∈ L²` at 0) |

So "interpolate between them" is not one move; it is at least two, and the third coordinate is
not a space parameter at all. §4 checks the two that *can* be interpolated, separately, and
finds them separately dead. A note that reported "no interpolant works" without saying this
would be reporting a confusion rather than a result, and this is stated first for that reason.

---

## 2. Endpoint one: weighted `ℓ¹`, where the operator is not bounded below

**The result.** In `ℓ¹_w` with `w_k = (1+k)^s` and `s < 1`, for the assembled bordered `a = 0`
CLM steady linearisation `L` at `μ = 0`, **every** bounded operator `A` on the space — with all
four blocks arbitrary, including `A₂₁` — satisfies

```
Z₁ = ‖I − A L‖_w  ≥  1.
```

Quantitatively at truncation `M`: `Z₁ ≥ 1 − ‖A‖_w · σ_min(L_M)` with
`σ_min(L_M) = c_s M^{−(1−s)} → 0`.

**The two ingredients, and only one is this project's.** The inequality
`Z₁ ≥ 1 − ‖A‖ σ_min(L)` follows from `‖x‖ ≤ ‖(I−AL)x‖ + ‖A‖‖Lx‖` and is the
contrapositive-with-remainder of the `Z₁ < 1 ⟹ invertible` hypothesis every radii-polynomial
paper states. **It is folklore and it is not claimed here.** What is this project's is the
other half: that `σ_min(L) = 0` on this operator in this space at every `s < 1`.

**The measurement.** `σ_min ∼ M^{−p}` fitted over `M − K = 128 … 2048` at `K = 4`:

| `s` | 0.0 | 0.3 | 0.7 | 1.0 | 1.5 |
|---|---|---|---|---|---|
| fitted `p` | **0.9925** | **0.6985** | **0.3202** | 0.0788 | 0.5000 |
| predicted `1 − s` | 1.00 | 0.70 | 0.30 | 0.00 | — (different mechanism) |

Max deviation from `1 − s` over all `s < 1` and all `K ∈ {2, 4, 8}`: **0.0219**. Relative
spread of `σ_min` across `K` for `s < 1`: **0.29 %** — so the divergence is a property of the
**tail**, not of where the finite/tail split is placed, which is why no choice of split escapes
it. (At `s = 1.5` that spread is **2.14**, because there the obstruction is the *cokernel*
entering the dual, a second and separate mechanism, reported separately rather than folded in.)

**The witness is constructed, not found.** An explicit sequence `v_M = (z_M ; h^{(M)})` built
from the tail block's analytic kernel matches the numerically-optimal direction to a ratio of
**1.0000000000045** and a cosine of **0.9999999999999998**, with `z_K = 0.0` exactly and the
entire residual of `Lv` carried by **one row** — the truncation edge.

**The bound is attained, so nothing leaks.** At `A = L⁻¹` the inequality is an equality: max
slack **1.2366e−08**. Across the previously banked shape battery it holds **196 / 196** with
minimum slack **7.7343e−10**.

**Two controls that can report the other answer.** (i) Switch on dissipation: `σ_min`
*saturates*, fitted exponent `≤ 2.63e−03` in absolute value at every `μ > 0`, against
**0.6985** at `μ = 0` in the same code path. (ii) A truncation-artifact audit — zero-pad the
`M`-optimal direction into `2M` and `4M` — degrades by at most **1.3543×**, bounded, not a
return to `O(1)`.

**The repair that was the whole point of the assembled object does nothing.** Bordering with
the far-field amplitude changes `σ_min` by **5.7e−15 relative** at `μ = 0`. The mechanism is
*not* that the singular sequence has no far-field-amplitude component — that component is
**6.5–6.8 % of `‖v‖₁` and growing with `M`**. It is that its coupling column is supported on a
**single row**, the truncation edge, so bordering has nowhere else to reach. (The same two code
arms differ by **6.1e−02** at `μ = 0.1`, so the comparison is live in both directions.)

**The consequence, as a magnitude.** Any `A` reaching `Z₁ ≤ 1 − δ` needs
`‖A‖_w ≥ δ/σ_min(L_M) ∼ δ·M^{1−s}`; the measured floor grows **1.99×** per doubling of `M` at
`s = 0` and **1.62×** at `s = 0.3`, i.e. exactly `2^{1−s}`. At any *fixed* `M` the floor is
finite, so a finite-`M` counterexample is not excluded — one is already banked, and was ruled
inadmissible for exactly that reason. What is excluded is a **single bounded `A` working
uniformly in `M`**, which is the only sense the method has.

> **The scope line, which is load-bearing.** This is a statement about the `ℓ¹_w` realization
> at `s < 1` and about nothing else. **No sentence here says the operator has no bounded
> approximate inverse** — §3 is the reason it may not.

---

## 3. Endpoint two: origin-`H²`, viable in form, capped in value

### 3.1 What was checked, and what passed

The published fact this endpoint rests on is not this project's: Xu
([arXiv:2607.19762](https://arxiv.org/abs/2607.19762)) proves the **same** `a = 0` CLM
linearisation is **invertible on origin-`H²`** after the standard modulation, with a spectral
gap of `1/2`. The question a scoping leg could actually answer is narrower and structural:
*does that realization supply a split, a shape for the approximate inverse, and freedom from
§2's obstruction?*

**All three, yes**, each re-derived from primary source rather than cited:

| conjunct | what supplies it | check |
|---|---|---|
| a **split** | Xu's Hardy block-diagonalisation `L₀ = L₀⁺ ⊕ L₀⁻`, the two blocks intertwined by conjugation and **not coupled** | block coupling **exactly zero**, against `K/2` for every split in `ℓ¹_w` |
| a **shape** for `A` | Xu's explicit resolvent kernel: a generalized Hardy–Mellin operator of **exact** norm `1/α` plus a **rank-two** correction whose only poles are the two symmetry eigenvalues | Mellin symbol norm re-derived, max relative error **0.0**; the closed-form lower witness reaches **99.80–99.99 %** of the bound over `α = 0.05 … 1.5` |
| **no §2-class obstruction** | — | `σ_min` does not decay with the truncation the way §2's does — a monotone-decreasing ladder that **flattens** (§3.5), not a proved floor; §3.5 states that limitation in full |

The supporting identities, re-derived numerically with every derivative analytic (three
independent quadratures, no finite differences): the resolvent identity holds to a worst
relative residual of **2.807e−14** over 18 (datum, `z`) combinations including complex `z`; the
two symmetry modes `L₀⁺(b⁻²) = b⁻²` and `L₀⁺(y b⁻²) = 0` hold to **1.790e−15** and
**5.266e−16**, and both also hold exactly by hand.

**The bordered formulation is explicit, not gestured at.** At `z = 0` the only singular object
in the kernel is a **rank-one functional** of the data, so

```
    [ L₀⁺   m ] [ u ]   [ f ]        m(y) = y b(y)⁻²          (the z = 0 null mode)
    [ ℓ     0 ] [ κ ] = [ 0 ]        ℓ(f)  = i f(0) − f′(0)/4  (the only z = 0 pole)
```

— one border column and one matching row per Hardy block, rank two on the real odd space. That
is the **same shape** the `ℓ¹_w` assembly already used. Bordered-solve residuals are
`≤ 2.221e−14`; `ℓ(f)` after projection onto the solvability subspace is **exactly 0.0** in all
three test data.

### 3.2 The contrast with §2, as magnitudes

| | `ℓ¹_w` (§2) | origin-`H²` (§3) |
|---|---|---|
| `σ_min` | → 0 like `M^{−(1−s)}`; **0.9925 / 0.6985 / 0.3202** at `s = 0 / 0.3 / 0.7` | does **not** decay that way: measured **0.0908** (leg 176, §3.5) on a monotone-decreasing ladder that **flattens** to **0.139 %** over a 16-fold truncation range — evidence of a positive limit, **not a proved floor** (§3.5 states that limitation in full). Leg 163's three data `‖u‖_X/‖f‖_X` = 1.3993 / 1.2680 / 1.3769 give only `σ_min ≤ 0.71465` — an **upper** bound, see the note below |
| truncation dependence | none available — `σ_min` has no truncation-independent value at all: it decays like `M^{−(1−s)}` | the ladder **flattens** instead of decaying (0.139 % over a 16-fold truncation range, §3.5) — which is **not** a truncation-independent value and is not offered as one. Separately, and on a *different* sweep, the bordered-solve ratio moves by **1.444e−04** across four added decades of **quadrature window** (`n_quad` 600→1400, window `1e−4…1e+4` → `1e−6…1e+6`); a window spread is not evidence about truncation |
| consequence for `Z₁` | `Z₁ ≥ 1` for **every** bounded `A` | no such floor; the exact inverse is in closed form |
| what bordering does | **nothing** — bordered and unbordered `σ_min` agree to **5.7e−15** | **everything** — the residue at `z = 0` *is* the border column |
| block coupling of the split | `K/2` for every choice | **exactly zero** by construction |

*(**Convention.** The `0.0908` in this table, and every `σ_min` digit below it in this note, is
convention-relative by a factor of **12.5** — §0's convention note states the sweep and Xu's own
`0.0420`. What this table is here for is its *truncation-dependence* row — decays there, flattens
here — and that contrast is convention-invariant.)*

*(**Provenance of the two numbers, and why they were never in conflict.** `0.71465` is the
five-decimal rounding of leg 163's own banked `implied_sigma_min_lower_witness =
0.7146549471256172`, which is the reciprocal of its largest sampled ratio in full precision
(`1/1.39927667753796`). No intermediate rounding of the ratio enters: the chain is one step, not
two. `0.71465` is the display form; the witness bound itself is `σ_min ≤ 0.71465495`, from which
the five-decimal figure differs by `4.9e−06` — far below any digit this note uses it at, but
recorded here so the printed form is not mistaken for the bound itself. Its producing leg wrote it as a
**lower** witness `σ_min ≥ 0.7147`; that
inequality is **inverted**. With `f = L u`, each datum gives `‖f‖_X/‖u‖_X = 1/r ≥ σ_min`, so a
finite family of sampled ratios bounds the infimum **only from above** — a sample can miss the
worst direction and here it did, by a lot: leg 163's best ratio reached **12.71 %** of the true
`‖R‖_X = 11.0127`, and leg 176's own four-datum re-run of the same construction reached only
**7.88 %** of it. Once the sign is read correctly the two legs agree: `0.0908 ≤ 0.71465`. Under the
erroneous `≥` reading they would not even be self-consistent, since the reciprocal of leg 176's
re-run family is `1.1519`, which cannot also be a lower bound on the same quantity. **`0.0908` is
the figure used throughout §3–§5; `0.71465` is retained here only as the (true, and very loose)
upper bound leg 163's data actually establish.** See §3.5.)*

### 3.3 The ceiling, stated at full strength — this is the half that matters

The scoping gate answered **YES**, and the leg that answered it **escalated rather than
built**, `main` untouched. Its own summary of the split was *"a genuine yes/no split, not a
clean win."* The five-item obstruction census is reproduced here with its own severity
gradings intact, because the third item is what closes the value of the YES:

- **O1 — the `α^{−3/2}` resolvent blow-up.** Not a §2-class obstruction. Engaged only as
  `Re z → −½`. The certificate sits at `z = 0`, `α = ½`, where `α^{−3/2} = 2.8284`.
  **No severity for a static certificate.**
- **O2 — non-normality: the gap is not a decay rate in the `X` norm.** Not a §2-class
  obstruction. **No severity for a static invertibility certificate; HIGH severity
  downstream.** Xu bounds his own result in his own abstract: the closed-form decay is obtained
  *"on a weighted space of the conjugated variable reached from `X` by a bounded transfer map;
  we keep the two separate, since `L₀` is non-normal and a spectral gap does not by itself give
  a decay rate in the `X` norm."* So an origin-`H²` certificate would certify
  **invertibility**, not **nonlinear stability** — and nonlinear stability is what the chain's
  first link needs. **This is why "invertible there, therefore a certificate is possible" is a
  forbidden sentence, not a shortcut.**
- **O3 — `a = 0` exactness dependence. FATAL for transfer**, and that grading is the producing
  leg's own word, not a paraphrase. Every usable object in §3.1 is a consequence of the profile
  being the *exact* `a = 0` CLM profile `Ω(y) = −y/(y² + ¼)`: the single-simple-pole identity
  `H(Ω) − iΩ = i/(y + i/2)`, the collapse of the nonlocal linearisation to a scalar first-order
  ODE on each Hardy block, the closed-form kernel, the exact Mellin norm `1/α`. For `a > 0` Xu
  proves only a conditional two-line inclusion under a hypothesis — no resolvent, no
  invertibility, no gap. This project's nominal target is not a CLM profile and inherits none
  of it. **The corollary, in the census's own words: *a certificate at `a = 0` in origin-`H²`
  would certify an object Xu already inverts in closed form.***
- **O4 — realization coupling for `a > 0`.** Xu §4.6: *"One cannot use the `H²` metric to empty
  the strip and the `L²` metric to close the origin channel."* The origin-regularity index and
  the positions of the essential lines are **coupled**; a stronger realization shifts the
  origin line off instead. At `a = 0` the two lines coincide, which is why the picture is clean
  there and only there. (§4 shows this is also what kills one half of the interpolation
  question.)
- **O5 — the §2 obstruction itself: checked for, and it does not recur.** The contrast table of
  §3.2 is that check.

**So the honest form of endpoint two is a conjunction, and both halves must travel together.**
The formulation is structurally viable — split, shape and bordered rows all explicit, verified
against Xu at worst residual **2.8e−14**. And it is capped at `a = 0` exactness, where what it
would certify is already known in closed form, with no transfer to the real target. Quoting
either half alone misrepresents the result.

### 3.4 One finding from that leg that is not about certificates at all

The sharpest in-repo consequence is a realization-discipline finding. On the maximal `L²`
realization, **every point of the open strip `−½ < Re λ < 3/2` is a genuine eigenvalue** (Xu
§4.6, with an explicit odd eigenfunction, confirmed numerically against the full nonlocal
operator) — so there is no `L²` spectral gap at all. The one feature separating those modes
from the physical ones is the second derivative at the origin: requiring `φ″ ∈ L²` near zero is
the whole difference. **Every numerical object this repository owns for this operator sits in
the realization *without* the gap** — its own capability ledger already recorded that its grid
imposes no origin condition. That is actionable independently of whether any certificate is
ever built, and it is the transferable thing here: **the realization discipline, not the
certificate.**

**On the commissioned construction leg (leg 176): as drafted, it had not landed.** *(It has
since landed; this paragraph is kept exactly as written, and the outcome is at §3.5.)* At
drafting it had
committed only its novelty pass. Two things from that pass are quotable, both pre-registrations
rather than results: (a) if it lands, the only thing it could claim as new is the **discrete
realization** — Xu's own numerics use compactified-grid Newton continuation, log-Mellin
discretization and FFT grids, with no Laguerre basis, no matrix representation and no
finite-section truncation — *"a claim about the method, not the theorem; the result is Xu's"*;
(b) Xu's three recorded gaps toward a computer-assisted proof (uniform large-imaginary-part
bound, trace-ideal membership, quadrature-error bounds in trace norm) sit in a different strand
of his paper and *"this leg closes none of the three."* That pass also states that leg 163's O3
is **confirmed rather than weakened** by it. **No outcome is attributed or predicted.**

### 3.5 The fourth data point: the construction leg landed, and its answer has two halves

Leg 176 built the formulation §3.1 scoped. **Its own gate headline, verbatim: "YES on both
conjuncts — with one magnitude that says NO and is reported in the same breath."** Both halves
are reproduced here at the strength leg 176 states them, and neither is quotable without the
other. Float64 throughout, nothing interval-enclosed; 42 evidence checks, 0 failing.

**The YES, half one — Xu's closed form reproduces.** Xu eq. (4.23) at `z = 0`, bordered, checked
pointwise against Xu's own ODE in `y`-space (a check that never mentions the discrete
realization): max relative residual **4.767e−15**, worst over six independent data **5.135e−15**,
against leg 163's established **2.8e−14** class. Every derivative analytic; no finite differences.

**The YES, half two — it closes on leg 163's own diagnostic.** `σ_min` of the bordered operator
in the `X` metric, on a **domain-only** truncation (range untruncated), which gives an upper
bound closing down onto `σ_min` rather than a Galerkin section:

| `N` | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 |
|---|---|---|---|---|---|---|---|---|
| `σ_min` | 0.0927566 | 0.0911590 | 0.0909310 | 0.0908878 | 0.0908506 | 0.0908234 | **0.090804** | *0.0909363* |

*(The `N = 512` cell is quoted to the six figures the computation supports. Leg 176 banked
`0.09080465147034879` there; an independent exact-rational re-derivation (leg 249, whose
artifacts are on `main`; originating branch `leg/249-h2cv2-v2` at `e9db984`) **proves** that value wrong from the 7th significant figure —
the pencil `AᵀG_cA − λG_d` is not positive definite at that `λ`, so `σ_min` is strictly below it
— and certifies `σ_min ∈ (0.090804094, 0.090804194)`. The cause is the whitening leg 176 uses,
whose error grows with the Gram's condition number; a Cholesky whitening of the same matrices
agrees with the exact tier at every rung, and under it the ladder is monotone decreasing through
`N = 2048`, so the `N = 1024` rise below is a property of leg 176's whitening rather than of the
Gram — the reliable window is **wider** than leg 176 claimed, not narrower. Full record:
[`writeup/data/p2_route_h2c_v1_construction_correction_leg268.json`](../data/p2_route_h2c_v1_construction_correction_leg268.json).)*

*(Every digit in that ladder, and the headline below it, is stated in the `X ⊕ ℂ` weight
convention of §0's convention note — a factor of **12.5** of freedom in the digits, none in the
flatten-versus-decay behaviour they are read for.)*

**`σ_min = 0.0908`, `‖R‖_X = 11.0127`**, monotone decreasing through `N = 512`, varying by
**0.139 % over a 16-fold truncation range**. The `N = 1024` row rises instead of falling; leg 176
attributes that to the float floor of an `X` Gram whose entries reach ~1e12 and reports it as the
reason the reliable window stops at 512 — **that attributed cause is superseded by the footnote
above**, which carries leg 249's finding that the rise is a property of leg 176's `eigh`
whitening rather than of the Gram, and that under Cholesky whitening the ladder is monotone
through `N = 2048`. Leg 176's sentence is quoted here as leg 176's; the operative explanation is
leg 249's, and the reliable window is wider than leg 176 claimed rather than narrower. In leg
176's own words the ladder is **"float64 evidence of a
positive limit, not a proof of one."** *(That quoted sentence is the last sentence of leg 176's
`C1_bordered_sigma_min_X.reading` field. Its opening clause — "bounded away from zero and
truncation-independent" — is **superseded** and is deliberately not quoted here; the governing
instruction is A1 of
[`p2_route_h2c_v1_construction_annotation_leg274.json`](../data/p2_route_h2c_v1_construction_annotation_leg274.json),
which requires any quotation of that field to carry the corrected framing or cite the annotation
beside it. This is the citation.)* The tail block closes too, and it earns exactly that same
reading and no stronger one: `‖T⁻¹‖_X` **rises monotonically** across the ladder
(`3.994032 → 4.012071 → 4.021340 → 4.026241 → 4.028864` at `N = 64 … 1024`, **0.865 %** in
relative terms) with its own **increments** shrinking geometrically (`1.804e−2 → 9.269e−3 →
4.901e−3 → 2.623e−3`, ratios `0.514 / 0.529 / 0.535`) — equivalently, the reciprocal tail
`σ_min = 1/‖T⁻¹‖_X` **falls** with decrements `1.126e−3 → 5.745e−4 → 3.027e−4 → 1.617e−4`,
ratios `0.510 / 0.527 / 0.534`, which are the smaller (`≈16×`) set and belong to `σ_min`, not to
`‖T⁻¹‖_X` — float64 evidence of a **finite limit near 4.032**,
not a proof of one, and **not** a truncation-independent value. Earlier drafts of this note
quoted `4.026, truncation-independent`; that is the value at one rung of a sequence still
climbing at `N = 1024`, and it understates the limit by **0.14 %**. What survives untouched is
the comparison the number is here for: this sequence **converges**, where in `ℓ¹_w` (legs 51/53)
the tail inverse norm **diverged** with `M`. (At `N = 512` leg 249's exact arithmetic certifies
`‖T⁻¹‖_X ∈ [4.02623993, 4.02624155]`; leg 176's banked `4.02614534796022` lies **outside** that
bracket by `6.0e−5` relative, same whitening mechanism as above and recorded in the same
correction artifact. Leg 176's own JSON `reading` field already read `4.03`.)
And the two controls report the other answer: unbordered `σ_min` collapses to the float floor
(1.55e−15 → 6.97e−14), and the loose `L²` realization decays like `N^{−1.49}` with **no gap at
all** — so the origin condition is now a measured magnitude rather than a citation.

**The NO, in leg 54's own shape, and it is the same magnitude class this note's §2 reports.**
With `A = blockdiag(finite bordered inverse, tail inverse)` and `Z₁ = ‖I − A𝕃‖_X`:

| `K` \ `M` | 64 | 128 | 256 |
|---|---|---|---|
| 2 | **140.72** | 182.23 | 244.15 |
| 4 | 697.95 | 934.14 | 1277.86 |
| 8 | 2747.04 | 3671.58 | 5026.73 |
| 16 | 10516.43 | 13621.66 | 18417.50 |
| 32 | 43253.75 | 50728.94 | 66043.98 |

**Best cell 140.72 where `< 1` is needed; growth `~K²`.** So in leg 54's shape the `X`
realization fails too — **but, in leg 176's own reading, for a different reason than `ℓ¹_w` did.**
There, leg 127 showed the operator itself had no truncation-independent `σ_min` — a **theorem**,
`σ_min(L_M) = c_s M^{−(1−s)} → 0` — so `Z₁ ≥ 1` for *every* bounded `A`. Here that mechanism is
**measured absent** rather than proved absent: the ladder flattens instead of decaying (§3.5),
float64 evidence of a positive limit and **not** a proved truncation-independent value. On that
reading — the strongest the data support — **the failure is of the block-diagonal
shape of `A`, not of the operator and not of the space.** Leg 176 calls that distinction its most
useful output and the reason both numbers are reported with neither standing for the other.
**This note adopts that framing and adds nothing to it**: no claim is made here that some
*other*, non-block-diagonal `A` closes it — that was not tested, by leg 176 or by anyone.

**One correction this construction makes to §3.2's, §4.5's and §5(3)'s witness — now applied at
all three sites, and it turns out to be a sign, not a magnitude.** Earlier drafts quoted
`σ_min ≥ 0.71465` in §3.2, §4.5 and §5(3). That is **leg 163's three-datum witness**, and leg 176
states plainly that it was **optimistic by 7.9×**
**[FLAGGED 2026-08-11, leg 280, per leg 281's finding E6: this factor is convention-relative,
ranging `5.265 … 656.95` over the same weight sweep §0 names, a `124.8×` swing — the factor
`7.9×` holds only in the repo's own fixed weight convention]**: *"That is a witness, not a bound. The measured
value is 0.0908."* Reproducing leg 163's own quantity from the closed form gives 0.8681539 over four
data while the operator norm is 11.0 — i.e. **random low-mode data does not find the worst
direction.** Tracing it further: `0.71465` is the five-decimal rounding of leg 163's banked
`implied_sigma_min_lower_witness = 0.7146549471256172` (§3.2 records the same provenance, in one
step and with the `4.9e−06` display offset named), the reciprocal in full precision of leg 163's own
largest sampled ratio `1.39927667753796`, and since each datum gives `‖f‖_X/‖u‖_X = 1/r ≥ σ_min`, a finite family of
such ratios bounds `σ_min` **only from above**. So leg 163's data support `σ_min ≤ 0.71465`, the
`≥` was inverted, and **the two legs never actually disagreed** — `0.0908 ≤ 0.71465`. All three
call-sites now carry `0.0908` as the measured figure, with `0.71465` retained only in §3.2 with
its correct direction and its provenance named.

*What the correction does and does not change.* It changes no conclusion in §3–§5. But it does
sharpen how one property may be stated. The `≥` sign was carrying the claim "**bounded away from
zero**", i.e. a lower bound — and **neither leg proves one**: leg 176's own domain-only truncation
is, in its words, *"an upper bound closing down onto `σ_min`"*, and its ladder is *"float64
evidence of a positive limit, not a proof of one."* What is established is a monotone-decreasing
ladder that **flattens** (0.0908878 → 0.090804 over `N = 64 … 512`, **0.0920 %**; 0.139 % over the
full 16-fold range) together with two controls that report the other answer — against `ℓ¹_w`, where
the analogous ladder **decays** like `M^{−(1−s)}`. That contrast is a contrast of ladder behaviour
in both spaces, which is all §3–§5 ever use it for, and it survives the correction intact. What
does not survive, and is not written anywhere in this note, is any claim to a *proved* floor.
Nor — per §0's convention note — any claim that the digit `0.0908` is
convention-independent: it moves by a factor of **12.5** under the border weight and
becomes `0.0420` in Xu's own `y`-space normalization (`0.057643` under Definition 4.1's own
displayed norm — §0), quoted here in one fixed convention.
**[CORRECTED 2026-08-11, leg 280, per leg 281's finding E5/E4: `0.71465`, by contrast, IS
convention-free, to `1.87e−16` — it is `1/max(‖u‖_X/‖f‖_X)` over a finite family, a ratio of
X-norms with no border coordinate, so the weight cancels between numerator and denominator. The
convention-dependence claim above applies to `0.0908` only, not to `0.71465`.]** The flatten-versus-decay contrast just described is what survives that freedom, and
it is the only thing §3–§5 use.

**What this does and does not change in §3.3's ceiling — nothing is lifted.** Leg 176 restates
O3 itself: `a = 0` only, and what is certified is **"an object Xu already inverts in closed
form."** It closes **none** of Xu's three recorded gaps toward a computer-assisted proof
(uniform large-imaginary-part bound, trace-ideal membership, quadrature-error bounds in trace
norm), forms **no `Y₀` and no `Z₂`**, is float64 with nothing interval-enclosed, and moves **no
link of the `L1 → L4` chain**. Its own summary of what it is: **"the first constructed (not
merely scoped) certificate outside the `ℓ¹_w` lane this repository has built, and a new exact
discrete realization of Xu's operator. Infrastructure, not a theorem."** The claim grade of this
fourth point is therefore **construction, gate YES with a reported NO magnitude** — strictly
weaker than §2's theorem and not to be levelled with it; and §3.3's *"escalated rather than
built"* now describes leg 163 specifically, not the state of the axis.

**Completing §0's promise: the two sentences in §§5–6 leg 176 bears on, named rather than left
to inference.** (i) §5's opening *"Separately they are: a theorem, an escalated scoping YES, and
a scoping NO"* counts the three points the synthesis was written from; with leg 176 the axis has
**four**, as §0's own table already shows, and the fourth is the construction grade just stated.
That sentence is **left standing as the three-result synthesis it is**, not silently upgraded.
(ii) §6's claim table likewise has three rows and no leg-176 row; the grade that row would carry
is the one in the preceding paragraph — **construction, gate YES with a reported NO magnitude**,
strictly below §2's theorem grade and strictly below nothing else. Both are drafting-time scope,
now disclosed here rather than discovered by a reader.

---

## 4. The segment between them is empty

Given a dead endpoint and a capped endpoint, the natural next move is to look for something in
between. It was looked for. **There is nothing there**, and the two halves of the search fail
for two *different* reasons.

### 4.1 MOVE A — the coefficient scale. The `ℓ¹_w` obstruction does not weaken at all.

Hold the domain and the realization; vary the index across `ℓ^p_w`, `1 ≤ p ≤ 2` — the
Fourier–Lebesgue / Besov-coefficient scale, which contains `ℓ¹_w` at `p = 1`. **Measured.**

**First, the instrument was calibrated against the banked endpoint.** Local slopes of §2's
exponent converge monotonically *from above*, so the endpoint of a ladder is not the answer;
the Aitken limits are **1.0000 / 0.7002 / 0.3090** at `s = 0 / 0.3 / 0.7`, deviating from
`1 − s` by at most **0.00905**. A negative control on the same code path — the `μ = 0` kernel
fed to the dissipative operator at `μ = 1` — returns **−0.2904**, i.e. the ratio *grows*, so
the `μ = 0` decay is a property of the operator and not of the arithmetic. (This is explicitly
*not* the same control as §2's own `μ > 0` saturation check, and is not conflated with it.)

**Then the mechanism, which is the whole of the check.** Because the kernel solves the tail
recursion exactly, its image vanishes in every row but the truncation edge: the single-row
share of the residual norm is **0.9999999999998843**, with **1** row above `1e−12` relative.
The negative control that could have failed — the same counter fed a perturbed direction —
reports **4088** rows, so "one row" is a property of the witness and not a tautology of the
code.

**And a one-entry vector has the same norm in every `ℓ^p`.** At fixed `(K, M, s)`:

| | `p=1.0` | `p=1.25` | `p=1.5` | `p=1.75` | `p=2.0` |
|---|---|---|---|---|---|
| numerator `‖Th‖_{ℓ^p_w}` | 0.09328169670293 | 0.09328169670293 | 0.09328169670293 | 0.09328169670293 | 0.09328169670293 |
| denominator `‖h‖_{ℓ^p_w}` | 11.7877 | 5.9580 | 4.1585 | 3.3600 | 2.9304 |

Numerator relative spread across `p`: **5.653e−14**. Denominator relative spread: **1.5707**,
i.e. **157 %**. *Moving along the interpolation scale changes the quantity the proof divides by
by 157 %, and the quantity it divides by 6e−12 %.* The index cannot reach the numerator,
because the numerator is one entry.

Swept over the whole grid, the exponent tracks `1 − s` and is `p`-blind where it is `O(1)`:

| | `s=0.0` | `s=0.3` | `s=0.7` | `s=0.9` | `s=1.0` | `s=1.2` | `s=1.4` |
|---|---|---|---|---|---|---|---|
| `p = 1.0` | 1.0000 | 0.7002 | 0.3090 | 0.1436 | 0.0836 | 0.0202 | 0.0038 |
| `p = 2.0` | 1.0000 | 0.7000 | 0.3000 | 0.1000 | 0.0000 | −0.1996 | −0.3898 |
| predicted `1 − s` | 1.00 | 0.70 | 0.30 | 0.10 | 0.00 | −0.20 | −0.40 |

Max deviation from `1 − s` for `s ≤ 0.7`: **0.00905**. Max spread across `p` at fixed
`s ≤ 0.7`: **0.00904**. **Rows where `p > 1` rescues an exponent that is dead at `p = 1`: 0.**
The technique weakens only as `s → 1`, and `s` was already available at `p = 1` and already
swept there. (The `p`-spread grows with `s` — 0.0000 at `s = 0`, 0.0836 at `s = 1.0`, 0.3936 at
`s = 1.4` — but that is the Aitken limit becoming ill-conditioned exactly where the exponent it
extrapolates passes through zero, which is why the conclusion rests on the `s ≤ 0.7` block. It
is reported rather than trimmed.)

### 4.2 The invariant: the two-parameter scale is a one-parameter picture

Three membership thresholds decide the whole scale, and with the kernel decaying like `m^{−2}`
(measured **−2.00236**), the cokernel functional growing like `m^{+1}` (measured **+1.00118**),
and the target's coefficients like `k^{−(1+α)}` with `α = 0.39735311167782`:

| | condition | in terms of `σ := s + 1/p` |
|---|---|---|
| kernel **in** the space | `p(2−s) > 1` | `σ < 2` |
| cokernel **bounded** on it | `q(s−1) > 1` | `σ > 2` |
| target **in** the space | `p(1+α−s) > 1` | `σ < 1+α` |

**All three depend on the single combination `σ = s + 1/p`** — the Sobolev/Besov scaling index,
which is precisely the invariant of interpolation. Measured as growth exponents of partial-sum
norms rather than as convergent/divergent booleans, over 45 `(p, s)` points × 3 quantities:
**114** quantities scored, **21** in the marginal band `|σ − threshold| ≤ 0.15` (excluded from
scoring, and reported rather than hidden, because at a threshold the true behaviour is
logarithmic and a power-law fit correctly reads a small spurious exponent); worst deviation
from the `σ`-prediction outside the band **0.01605**; mismatches above 0.02 outside the band
**0**. The marginal band's log behaviour is demonstrated rather than asserted: at `p=1, s=1`
(`σ = 2`) the partial sums add a *constant* per decade over `N = 10³…10⁶`, max/min increment
ratio **1.01114**. And the single row nearest the band edge was chased rather than tolerated:
its deviation falls monotonically **0.02955 → 0.02167 → 0.01605 → 0.01213** along a truncation
ladder, so it is the partial sum's truncation and not a failure of the prediction.

### 4.3 The window's width is exactly zero, and the target is outside it anyway

The kernel leaves the space at `σ ≥ 2`; the cokernel enters the dual at `σ ≤ 2`. **The only
`σ` at which neither obstruction is present is `σ = 2` exactly — a single point, at every `p`.**
At `p = 1` that is `s = 1`, which is exactly the exponent this project's own ban list already
calls "the ONE exponent at which bordering cannot help." The interpolation scale does not widen
that point; it **translates** it.

And at that point the target is out of the space, by the same margin everywhere:

| | `p=1` | `p=1.25` | `p=1.5` | `p=1.75` | `p=2` | `p=3` | `p=10` | `p=∞` |
|---|---|---|---|---|---|---|---|---|
| `s` at the crossing | 1.0000 | 1.2000 | 1.3333 | 1.4286 | 1.5000 | 1.6667 | 1.9000 | 2.0000 |
| `s` ceiling for the target | 0.3974 | 0.5974 | 0.7307 | 0.8259 | 0.8974 | 1.0640 | 1.2974 | 1.3974 |
| **margin** | **−0.602647** | **−0.602647** | **−0.602647** | **−0.602647** | **−0.602647** | **−0.602647** | **−0.602647** | **−0.602647** |

**Both walls translate by exactly `−1/p`, so the gap between them is an invariant of the whole
scale**, equal to `α − 1 = −0.602647` exponent units. Cross-checked against the directly
measured `p = 1` margin banked earlier by a different leg — **−0.6062554687114012** against
this asymptotic prediction of **−0.602647**, difference **0.003609**, agreeing to **0.6 %**
(the first is a measured norm, the second an exponent-level asymptote). This is the
`p`-independent generalisation of an earlier leg's own sentence: *"the class where the operator
is least bad is the class where the target has infinite norm."* It holds on the whole scale,
with the same 0.60-exponent-unit gap.

### 4.4 MOVE B — the origin-regularity index. No scale can even ask the question.

The other interpolation is the Sobolev index between `L²` and `H²` on the line. It fails, and
for a reason of a different kind. **This half was not re-measured**; it is read out of endpoint
two's own census, and that attribution is part of the result, not a footnote.

**What forces `a = 0` exactness is the single-simple-pole identity `H(Ω) − iΩ = i/(y + i/2)`,
and that is an equation satisfied by the PROFILE.** It contains no norm, no weight and no
index. Every space — interpolated or not, on the line or on the circle — inherits it if and
only if the profile is the exact `a = 0` one. **No choice of scale can supply it, and none can
remove it.** So check (b) is not a question an interpolation scale is *able* to answer, which
is a stronger and more honest statement than "the candidate scales fail it."

And the one interpolation that could even be attempted is ruled out in Xu's own text, quoted
above as O4: *"One cannot use the `H²` metric to empty the strip and the `L²` metric to close
the origin channel."* On the maximal `L²` realization there is no spectral gap at all; a
stronger realization shifts the origin line off; **an intermediate index gets neither.** This
sentence was named as the candidate obstruction in the leg's novelty pass **before** the check
was run, so the NO is not a discovery its own construction conveniently arrived at.

### 4.5 The scale-by-scale answer, and one reason that is explicitly *not* the reason

| candidate scale | (a) no `ℓ¹_w`-class floor | (b) no `a=0` requirement |
|---|---|---|
| `ℓ^p_w` / Fourier–Lebesgue, `1 < p < 2` | **FAILS** — exponent tracks `1−s`, `p`-blind to 0.00904; numerator spread 5.7e−14 | not reached — O3 applies unchanged |
| Besov `B^s_{p,q}` coefficient realization | **FAILS** — same `σ = s + 1/p` invariant; `q` refines only the `σ = 2` line, measure zero, where the target's margin is −0.6026 | not reached — O3 applies |
| weighted Sobolev `H^s_w` on the circle (`p = 2`) | **FAILS** — it is the `p = 2` row above: exponent `1−s` exactly | not reached — O3 applies |
| origin-regularity index between `L²` and `H²` on the line | not reached | **FAILS** — O4, in Xu's own text |
| origin-`H²` itself (the endpoint) | passes — `σ_min` measured at **0.0908** (§3.5), not the `0.71465` of earlier drafts, which was only an upper bound | **FAILS** — O3, fatally |

**Every scale fails at least one check, and no scale passes both.** (The `0.0908` and `0.71465`
in the last row are convention-relative digits — §0's convention note; the FAILS/passes verdicts
in the table are not, since each rests on a decay exponent or on O3/O4.)

**One constraint that is emphatically not the reason, recorded so it cannot later be mistaken
for it.** The CAP literature is bimodal — weighted `ℓ¹` **or** Hilbert `H^l`, nothing between —
because `ℓ¹_ν` is a Banach algebra under convolution (which is what the quadratic constant
needs) and `ℓ^p` is **not** an algebra for `p > 1`. On the `ℓ^p_w` scale the algebra property is
recovered whenever the weight embeds the space in `ℓ¹`, i.e. `σ > 1` — which holds throughout
the region of interest, since the crossing is at `σ = 2`. **So the Banach-algebra constraint
does not bind here.** The reasons are the ones in §4.1–§4.4.

---

## 5. What the three results say together

**Separately** they are: a theorem, an escalated scoping YES, and a scoping NO.

**Together** they are one statement about where a certificate for this operator can live, and it
has four parts:

1. **The obstruction that consumed roughly seventy legs of this project is a property of the
   certificate's SPACE, not of the operator.** The same `a = 0` CLM linearisation is not
   bounded below in `ℓ¹_w` at any `s < 1` (§2, proved) and is invertible with an explicit
   closed-form inverse on origin-`H²` (§3, published by Xu, re-derived here at worst residual
   2.8e−14). Those two facts do not conflict; they separate two realizations of one operator.
   **The organising concept — that an obstruction can belong to the realization rather than to
   the operator — is itself published and named on this exact operator, and is used here, not
   claimed.**

2. **The `ℓ¹_w` endpoint is dead for a reason that is structural and not tunable.** It is not
   the weight (the exponent is `1 − s` at every `s < 1`, with 0.29 % spread across the split),
   not the split (the tail owns the divergence), not the shape of `A` (the argument never
   decomposes `A`), and not the bordering repair (5.7e−15). The method needs weighted `ℓ¹` of
   Fourier coefficients to control its tail, and in that space this operator is not bounded
   below at all.

3. **The origin-`H²` endpoint is structurally viable and simultaneously worthless for the real
   target, and both halves are load-bearing.** Split, shape and bordered rows are explicit and
   verified; `σ_min` measured at **0.0908** (§3.5; the `0.71465` of earlier drafts was an upper
   bound from three data, not a floor) on a ladder that **flattens** rather than decaying —
   0.139 % over a 16-fold truncation range, with a quadrature-window spread of 1.44e−04, and no
   proved floor anywhere in it; the `ℓ¹_w` obstruction does
   not recur. And every one of those objects is a consequence of `a = 0` exactness (O3, FATAL
   for transfer), the operator is non-normal so invertibility is not stability (O2, HIGH
   downstream), and what a certificate there would certify is a closed form its author already
   wrote down. (The `0.0908` in this paragraph is a convention-relative digit — §0's convention
   note, a factor of 12.5 — while the flattens-rather-than-decays statement it appears in is
   not.) **The right-sized claim is: the space axis has a live point, and the live point
   is at the wrong object.**

4. **And there is nothing between the two endpoints.** Not because the candidates were tried
   and found wanting one by one, but for two structural reasons: on the coefficient side the
   entire two-parameter family collapses to the one parameter `σ = s + 1/p` that legs 51/55/127
   had already swept, and the window where both obstructions vanish is a **single point** whose
   distance from the target's own ceiling is the `p`-invariant **−0.602647**; on the
   origin-regularity side the requirement that kills transfer is an identity about the
   **profile**, which no space can supply or remove.

**So the space axis is mapped and closed.** Everything left is off it: a different object (the
`a > 0` profiles, where none of Xu's machinery applies), a different question (nonlinear
stability rather than invertibility, which O2 says needs more than a gap), or a different
discipline (enforce the origin condition in the discretization — the one genuinely transferable
item, per §3.4).

---

## 6. What is claimable, and what is not

The three results sit at three different grades and **must not be levelled**:

| result | grade | what may be claimed |
|---|---|---|
| §2 `Z₁ ≥ 1` on `ℓ¹_w` | **theorem** | `Z₁ ≥ 1` for every bounded `A`, on the `ℓ¹_w` realization at `s < 1`, on this operator. **Not** about the operator; **not** about the method in general. The inequality it rests on is folklore and is not claimed. |
| §3 origin-`H²` viability | **scoping, escalated not built** | that a formulation with an explicit split, shape and bordered rows exists and reproduces Xu at 2.8e−14, **stated only together with O3 (fatal for transfer) and O2 (invertibility is not stability)**. **Never** "a certificate exists there", and never "Xu proves it invertible, therefore a certificate is possible." |
| §4 no interpolant | **scoping negative over a named family** | that every scale considered fails at least one of two named checks, with the `σ`-invariant as the mechanism for one half and a profile identity for the other. **Not** "no space works" — the family is `ℓ^p_w` / Besov-coefficient / weighted-Sobolev-on-the-circle / origin-regularity-index, and it is named. |

**Four things this note must never be read as saying.** (1) That the operator has no bounded
approximate inverse — it is invertible on origin-`H²`, published. (2) That the
Newton–Kantorovich or radii-polynomial method is obstructed in general. (3) That origin-`H²`
offers a route to anything this project needs — O3 says the opposite, and §3.3 leads with it.
(4) That any of this bears on the target problem. The object is the `a = 0` CLM linearisation,
whose first certificate constant is exactly zero for a degenerate reason (the anchor *is* one
basis mode), so every magnitude here bounds the real target's difficulty **from below**.

---

## 7. Ceiling

The object throughout is the `a = 0` CLM steady linearisation. **No dynamics were run.**
Nothing is claimed about this project's nominal target profile beyond its banked coefficient
exponent `α = 0.39735311167782`. **Every `σ_min` digit in this note is stated in one fixed
weight convention and is relative to it by a factor of 12.5** — §0's convention note gives the
sweep (`0.01086 … 0.13580`) and Xu's own `y`-space figure (`0.0420` rather than `0.0908`
under Xu's *equivalent* full-line norm; **`0.057643` under Definition 4.1's own displayed
half-line norm — see §0, corrected 2026-08-11 per leg 277**); what
is invariant under that freedom, and what §§3–5 argue from, is the ladder's *behaviour*, not its
digits. Every number is float64 at a stated truncation; **nothing here
is interval-enclosed or rigorous** in the computer-assisted-proof sense, including §2, whose
*proof* is exact but whose *verifying measurements* are floating-point. §3 built no certificate
and formed no certificate constant. §4's `σ`-threshold algebra is asymptotic at the exponent
level and agrees with the directly measured `p = 1` margin to 0.6 %, not exactly; its MOVE-B
half is read from §3's census rather than independently re-derived, and the leg that wrote it
states plainly that it did not re-read Xu at primary source. The commissioned origin-`H²`
construction leg had **not landed** at drafting and nothing in §§1–4.5 or §§5–6 is attributed to
it; it has since landed and is folded in at **§3.5 only**, where it is float64 with nothing
interval-enclosed, forms no `Y₀` and no `Z₂`, and is carried as that **leg's own float64
measurements**. The independent check on them **has since reported**: the originally commissioned
verification leg (leg 192) committed only a novelty pass, but leg 249 re-derived the construction
in exact rational arithmetic, confirmed both conjuncts, and corrected two banked values below the
digits quoted here (§0, §3.5); a later review pass re-pulled those figures from leg 249's own
branch and matched them exactly, and those three artifacts are now **on `main`**, byte-identical
to that branch. That check is exact where leg 176 is float64, and it does not
convert any ladder here into a proved bound. **No link of the `L1 → L4` chain moved.** None has moved in 275 legs (count current as of leg 276). Clay odds remain ~0.05 %.

**This draft is for the user's review. Its landing records that the bundle reproduces from its
sources; it does not approve the bundle for publication. It is one of two such drafts — see
[`TECHNICAL_P2_PUB1_V1.md`](TECHNICAL_P2_PUB1_V1.md) for the other, which answers a different
question.**
