# Route-M2P v1 (leg 125) — Chen's γ=2 dissipative gCLM candidate: full text, constants, first Y₀

**Branch** `leg/125-m2p-v1`. **Module** `solver/dissipative_profile.py` (new, sole owner).
**Tests** `test_dissipative_profile.py`, 20/20. **Runner**
`experiments/p2_route_m2p_v1_promotion.py`. **Data**
`writeup/data/p2_route_m2p_v1_promotion.json`. **Figure** `fig61`.
**`no_dynamics_run: true`** — every solve here is of a *steady* equation. **Claims no stage.**
**Everything is floating point; no number in this document is a certificate.**

---

## 0. What this leg was sent to do

Leg 63's screen produced the only screen-passing candidate in 63+ legs: gCLM with full
Laplacian dissipation (γ=2), `a` near 1/2, blow-up proved analytically by J. Chen,
[arXiv:1908.09385](https://arxiv.org/abs/1908.09385) (*Nonlinearity* **33** (2020) 2502). It did
not read the full text, transcribe the constants, or measure `Y₀`. Three debts, discharged in
that order.

The novelty pass ran and was committed **first** (`writeup/novelty/leg_125.md`, commit
`bb3f356`), five verbatim queries, links not counts. Its two operative findings:

* **No CAP or validated-numerics certificate of any *dissipative* self-similar gCLM profile
  exists in the searched literature.** Every CAP hit returned was inviscid. So a measured `Y₀`
  here is a novel data point regardless of its value.
* **Chen is analytic** — weighted `L²` and weighted `H⁴` energy estimates (§2.3–2.5), no
  interval arithmetic anywhere. This *confirms at full-text depth* `Papers/MANIFEST.md`'s
  2026-08-04 index-depth entry: an exclusion, not a CAP precedent.

---

## 1. The full-text read

### 1.1 Theorem 1.1, verbatim (p.3)

> **Theorem 1.1 (Finite time blow-up for a close to ½).** *Consider (1.1) with Lω = −∂ₓₓω.
> There exists δ > 0 such that for a ∈ (½ − δ, ½ + δ), 0 ≤ ν ≤ 1, (2.1) develops a self-similar
> singularity in finite time for some C_c^∞ initial data.*

### 1.2 The profile, verbatim (eq (2.2), p.4)

Chen studies the **inviscid** problem first. For a = ½ the steady self-similar equation

    (c_l x + a U) Ω_x = (c_ω + U_x) Ω ,   U_x = HΩ ,  a = 1/2

has, in his words, *"the following analytic self-similar solution"*:

| constant | value | provenance |
|---|---|---|
| `Ω(x)` | `−2bx / (x² + b²)²` | eq (2.2), p.4 |
| `U_x(x) = HΩ` | `(b² − x²) / (b² + x²)²` | eq (2.2), p.4 |
| `U(x)` | `x / (b² + x²)` | eq (2.2), p.4 |
| `c_l` | `1/3` | eq (2.2), p.4 |
| `c_ω` | `−1` | eq (2.2), p.4 |
| `b` | `√(3/8)` | eq (2.2), p.4; `b² = 3/8` closes his verification identity |
| `ū_x(0)` | `8/3` (`= 1/b²`) | p.5, *"where we have used ūₓ(0) = 8/3"* |
| weights `φ`, `ψ` | `(x²+b²)³/(2bx⁴)`, `(x²+b²)³/(2b)` | eq (2.12), p.6 |
| `ν(t)` | `exp(∫₀ᵗ [c_ω + 2c_l]) C_l(0)⁻² C_ω(0) ν` | eq (2.7), p.5 |
| decay exponent (exact) | `−1/3` | (2.40), p.11: *"bounded above by −1/3 and a small term"* |
| decay exponent (rigorous) | `≤ −1/4` | (2.43), p.11: `ν(t) ≤ exp(−t/4) ν(0)` |
| `δ`, `ν₀` | **UNQUANTIFIED** | (2.41), p.11 — see §1.4 |

All of these are machine-readable in `chen_constants()` with the provenance string attached to
each, and `test_dissipative_profile.py` checks their internal consistency (`b² = 3/8`,
`1/b² = 8/3`, `2c_l + c_ω = −1/3`).

### 1.3 The sentence that decides the leg (§2.6, p.12, verbatim)

> *"Since ν(t) converges to 0, such profile is the same as the inviscid profile associated
> with a."*

with **Remark 2.1** (p.11): *"(2.43) implies that the diffusion term in (2.6) vanishes as
t → +∞"*, and **§1.5** (p.4): *"In Section 2, we construct the self-similar profile for the
**inviscid** gCLM (1.1) with a = ½."*

**There is no γ = 2 self-similar profile in the paper.** The dissipation is genuinely present
in the equation and genuinely handled by the proof, but it is handled as a *vanishing
perturbation*: Chen states the plan explicitly on p.4 — *"if we add the diffusion term, such
term is asymptotically small compared to the nonlinear term in the equation of the self-similar
variables. In our later analysis, we will treat the diffusion term as a small perturbation."*

### 1.4 The a-neighbourhood is unquantified, as leg 63 suspected

Eq (2.41), p.11 fixes `δ` and `ν₀` only through

    (1 + C₂ + C₃ + C₂C₃ + C₂²)(δ + ν₀) < 1/1000

with `C₂` (from (2.39)) and `C₃` (from (2.40)) **unnamed universal constants**. So the width of
the a-window is not extractable from the paper. Recorded as `None` with the provenance string,
never bounded — lesson 73. Related, and worth stating because it is easy to misread: Theorem
1.1's *"0 ≤ ν ≤ 1"* is **not** a large-viscosity claim. (2.41)–(2.42) reach it by choosing the
initial length scale `C_l(0)` large so that `ν(0) ≤ C_l(0)⁻² ≤ ν₀`; the *rescaled* viscosity is
driven small.

### 1.5 The γ tension leg 64's review surfaced: resolved, and it was never a contradiction

| statement | range of `a` | source |
|---|---|---|
| critical dissipation is `γ = \|a\|⁻¹` | **a ≤ −1** only | §1.2 p.2; Theorem 1.5 |
| critical dissipation is `γ = 1` (from `L¹` conservation) | **a > −1** | §1.2 p.2 |

The two have **disjoint** ranges of `a` and never meet. Neither yields a γ = 2 profile, and
Theorem 1.1 does not need one. There is a third piece that removes the last of the tension: the
blow-up data of Theorem 1.1 is **class 3** (`ω₀` odd, `ω₀ ≤ 0` for `x > 0`; Remark 1.4, p.3),
which is precisely the class in which `L¹` is **not** conserved — Lemma 3.1(b), eq (3.5), gives
only `‖ω(t)‖_{L¹} ≲ exp((1+a)∫uₓ(s,0)ds)‖ω₀‖_{L¹}`. So the `L¹`-based criticality of §1.2 does
not classify the blow-up data at all.

---

## 2. The obstruction, derived

From eq (2.7), the effective viscosity in dynamic-rescaling variables satisfies
`ν̇ = (2c_l + c_ω) ν` (Chen writes this out explicitly on p.12). A **steady** self-similar state
therefore requires `(2c_l + c_ω) ν = 0`: either `ν = 0`, or

    2 c_l + c_ω = 0 .

The steady equation has an exact time-normalisation symmetry
`(Ω, c_l, c_ω) → (κΩ, κc_l, κc_ω)` for every `κ > 0` (verified directly: both sides scale by
`κ²`), under which `2c_l + c_ω` is *covariant*, not invariant. The banked gauge discipline in
`solver/gclm_family.py` — *"c_ω, c_l are a NORMALIZATION gauge, not results"* — applies. The
invariant form is

    **Δ  :=  2 c_l / |c_ω|  −  1**

    Δ = 0  ⟺  c_l/|c_ω| = 1/2, the heat scaling ⟺ a γ=2 profile is admissible
    Δ < 0  ⟺  dissipation vanishes in self-similar variables
    Δ > 0  ⟺  dissipation would dominate

At Chen's eq (2.2): `Δ = 2(1/3)/1 − 1 = −1/3` **exactly**, matching his own (2.40) bound
*"above by −1/3"* derived by an entirely different route. The mechanism in words: the structure
collapses like `(T−t)^{1/3}` while the diffusive length shrinks like `(T−t)^{1/2}`; the
structure is always the larger of the two, so diffusion never resolves it.

**Lesson-90 controls, written before the number was quoted.** `diffusion_consistency` returns
`0.0` **exactly** on the heat pair `(1/2, −1)` and `+1.0` **exactly** at the a=0 CLM anchor
`(1, −1)`. Three distinct values across three known profiles; the functional varies and *can*
report the other answer. Both are permanent tests.

---

## 3. Construction

`solver/dissipative_profile.py`. **Reused, not rebuilt** (standing ban; `capabilities.py`
grepped first): `gclm_family.GCLMResidual` (sinh grid, whole-line Hilbert matrix via
`line_hilbert`, the a-family residual convention), `gclm_rescaled.sinh_grid`,
`nk_bounds.budget`. **Added**, because nothing in the repository had it:

1. **A 4th-order cumulative velocity operator.** The banked trapezoid operator floors the
   residual of the *exact* profile far above the level any `Y₀` would need — lesson 86 ("a
   bound dominated by its own evaluation error is a statement about the code"). At `n = 601`
   the Adams–Moulton panel rule drops the velocity error from **1.4375e−04 to 7.467e−07
   (192.5×)** and the residual sup from **2.4124e−04 to 3.7426e−06 (64.5×)**. Tested against
   the banked operator (`test_high_order_velocity_beats_the_banked_trapezoid_one`).
2. The **dissipative** steady residual `R = (c_ω + HΩ)Ω − c_l XΩ_X − a U Ω_X + ν Ω_XX` and its
   **exact** Jacobian (`R` is exactly quadratic in `Ω`, so `D²F` is a constant bilinear map and
   there is no linearisation error).
3. `diffusion_consistency` / `nu_decay_rate`.
4. The `Y₀` measurement and the exact `Z₂`.

**Gauge fixing.** Two exact symmetries must be quotiented or Newton reports the conditioning of
a gauge: amplitude `(Ω,c_l,c_ω) → (κΩ,κc_l,κc_ω)`, and spatial dilation `Ω(X) → Ω(X/μ)` (same
`c`'s, `ν → μ²ν`). `c_ω = −1` kills the first; `Ω_X(0)` fixed kills the second. **`c_l` is left
free and `HΩ(0)` is never imposed**, so both are genuine outputs. Solved in least-squares form
because the residual of an odd profile is odd and the square system is rank-deficient by
construction.

### 3.1 M2 — known-answer gate: Chen's closed form nulls the residual, and the floor converges

| `n` | residual sup | Hilbert err | velocity err |
|---|---|---|---|
| 601 | 3.743e−06 | 1.09e−07 | 7.47e−07 |
| 801 | 1.187e−06 | 3.42e−08 | 7.37e−07 |
| 1201 | 2.358e−07 | 7.14e−09 | 7.27e−07 |

### 3.2 M3 — Newton reconstruction: Chen's constants come back as *outputs*

Started from a 5% perturbation of the exact profile with `c_l₀ = 0.30`. Newton converges
quadratically (residual history `2.5e−02 → 9.7e−04 → 4.6e−06 → 3.2e−11 → 1.5e−15`).

| `n` | `c_l` (Chen 1/3) | abs err | `HΩ(0)` (Chen 8/3) | shape sup err | `Δ` |
|---|---|---|---|---|---|
| 601 | 0.333334952 | 1.62e−06 | 2.666665062 | 4.18e−06 | −0.333330 |
| 801 | 0.333333846 | 5.13e−07 | 2.666666160 | 1.32e−06 | −0.333332 |
| 1201 | 0.333333435 | 1.02e−07 | 2.666666568 | 2.61e−07 | −0.333333 |

Second-order convergence in all three columns. This is an independent numerical verification of
eq (2.2) and of the reading of the steady equation, including the fact that Chen's printed
advection coefficient is `a = 1/2` multiplying `U` (the layout stacks it as a fraction).

### 3.3 M4 — Δ(a), the central measurement

Every point converged to machine precision (residual RMS 5.91e−16 … 4.64e−15), `n = 401`.

| `a` | `c_l` | `Δ` |
|---|---|---|
| 0.30 | 0.618417 | **+0.236835** |
| 0.35 | 0.550677 | **+0.101354** |
| 0.40 | 0.480958 | −0.038083 |
| 0.45 | 0.408741 | −0.182517 |
| **0.50** | **0.333342** | **−0.333317** |
| 0.55 | 0.253857 | −0.492286 |
| 0.60 | 0.169101 | −0.661798 |
| 0.65 | 0.077533 | −0.844934 |
| 0.70 | −0.022807 | −1.045613 |

**At Chen's a = ½ the measured Δ is −0.333317** against the exact −1/3 = −0.333333 (agreement
1.6e−05), and against the **0** a γ=2 profile would need. **The gap to admissibility at Chen's
own advection value is 1/3.**

**Δ crosses zero**, between a = 0.35 and a = 0.40. Located two independent ways:

* linear interpolation of the sweep: `a* = 0.386344`
* direct solve with `c_l = 1/2` **imposed** and `a` free (M7, ν = 0): `a* = 0.386496`
* agreement **1.5e−04**

### 3.4 M5 — the dissipative branch on Chen's own `a`, searched not assumed

Newton on the full dissipative steady equation at a = ½, `Δ` measured:

| `ν` | `c_l` | `|Δ|` |
|---|---|---|
| 0 | 0.333342 | 0.333317 |
| 1e−04 | 0.332419 | 0.335162 |
| 1e−03 | 0.324531 | 0.350938 |
| 1e−02 | 0.269067 | 0.461866 |
| 1e−01 | 0.081199 | 0.837603 |
| 3e−01 | −0.077224 | 1.154447 |

Monotone increasing: on Chen's branch, adding viscosity moves the profile **away** from
γ=2 admissibility, by up to 3.5× over the tested range. No zero crossing.

### 3.5 M7 — imposing Δ = 0, and why the result is a lead and not a claim

M7 does the converse of M5: it **imposes** `(c_l, c_ω) = (1/2, −1)` — exactly the condition a
γ=2 profile needs — and solves for `(Ω, a)` at each `ν`.

| `ν` | `a` | relative residual | solution scale | non-trivial |
|---|---|---|---|---|
| 0 | +0.3864964 | 1.933e−15 | 3.69e−01 | yes |
| 1e−03 | +0.3794130 | 2.462e−15 | 3.76e−01 | yes |
| 1e−02 | +0.3202336 | 2.706e−15 | 4.61e−01 | yes |
| 1e−01 | +0.2833540 | 1.102e−14 | 7.01e−01 | yes |
| 3e−01 | +0.3820855 | 2.437e−14 | 5.46e−01 | yes |
| 1.0 | −10.0924614 | **5.486e+00** | **2.20e−16** | **no — trivial null** |

**Two controls, and both matter.**

* **The ν = 1 row collapsed to `Ω ≡ 0`.** The trivial null solves the equation *exactly*, so
  its **absolute** residual is zero and it would have been reported as a perfect solve. Only
  the scale-invariant residual `‖R‖ / ‖(c_ω + HΩ)Ω‖` exposes it (5.486, and solution scale
  2.20e−16). This is lesson 90 in its sharpest form and it is why M7 reports a relative
  residual at all.
* **Dilation covariance fails as a check.** `Ω(X) → Ω(X/μ)` maps a solution at `ν` to one at
  `μ²ν` with `a` **unchanged**, so a genuine one-parameter branch must have `a` independent of
  `ν`. Measured `a` ranges over **[0.283354, 0.386496]** — it is not. The direct diagnostic:
  dilating the ν = 1e−02 solution by `μ = √10` and evaluating at ν = 1e−01 gives relative
  residual **5.59e−02**, against an undilated control of **1.707** (a 30.5× improvement, so the
  covariance is *partly* there and the remainder is interpolation error) — but not the ~0 a
  resolved branch would give.

**Diagnosis.** In the odd subspace the system has `(n−1)/2` independent residual rows for
`(n−1)/2 + 1` unknowns: short by one. Newton (minimum-norm least squares) therefore lands on an
arbitrary point of a one-parameter set that depends on the starting guess. **This leg has
therefore NOT established that a γ = 2 profile exists at `a*`.** It is recorded as an open lead
with the failed check attached (lesson 76), and explicitly not as a result.

---

## 4. Y₀ and the budget

### 4.1 Which Y₀ is the honest one (lesson 86, applied in advance)

After Newton the **discrete** defect sits at the Newton floor, `O(1e−15)`. That is a statement
about the code, not about the mathematics, and it is never the headline. The **honest** `Y₀` is
the *consistency* defect — the discrete solution's defect in the *continuous* equation —
proxied at each resolution by the exact profile's residual (§3.1). Both are in the JSON, both
are on fig61(d), and which is which is labelled at both.

### 4.2 Leg 53's μ = 2 positive control, re-read against **this** candidate

Leg 53's dissipative positive control reached `Z₁ = 0.9156181325483919`
(`writeup/data/leg_54_verify_headline.json`, `Z1_total`; independently re-derived by VER-A at
leg 54). It is used here as a **fixed** input — the most favourable `Z₁` this repository has
ever measured — held constant while `Y₀` is measured. **It is not assumed to transfer**: it was
measured on the a=0 CLM linearisation with Λ¹ dissipation, a different operator from Chen's
a=½ Λ² one, and it is quoted here only to make the budget as generous as the banked record
allows. Any honest `Z₁` for *this* operator would be larger and the budget smaller.

### 4.3 The measurement, with `Z₀ = 0` (maximally generous)

`Z₂` is exact for this operator (`F` is exactly quadratic, so `D²F` is a constant bilinear map)
and is assembled as `‖A‖·‖B‖` in the sup norm.

| `n` | `Y₀` (honest) | `Z₂` | budget `Y₀,max` | `Y₀`/budget | closes |
|---|---|---|---|---|---|
| 601 | 3.743e−06 | 3.842e+12 | 4.633e−16 | **8.079e+09** | no |
| 801 | 1.187e−06 | 2.545e+13 | 6.994e−17 | **1.698e+10** | no |
| 1201 | 2.358e−07 | 3.674e+14 | 4.846e−18 | **4.866e+10** | no |

**`Y₀` is over budget at every tested resolution, and the gap WIDENS under refinement** —
6.024× over the ladder — because `Z₂` grows (measured `≈ n^6.59`) far faster than `Y₀` falls
(measured `≈ n^-3.99`, i.e. the expected 4th order).

**What that Z₂ is and is not.** `‖A‖` is the sup norm of the pseudo-inverse of a Jacobian that
is rank-deficient by the two gauge directions, so `Z₂` is substantially an artefact of a
**gauge-unbordered** discretisation rather than a property of the operator. A real certificate
would border those directions — which is exactly what legs 51–53's bordered certificate does,
and exactly where leg 53 found the margin runs out (`Z₁`'s block coupling, entry `K/2`, 43.15).
So the honest reading is: **the candidate does not clear the budget, and the reason it does not
is not the reason the ledger expected.** The magnitude is reported; the mechanism is named as
not fully attributed.

---

## 5. The gate, answered in its pre-committed wording

> *"With Chen's theorem located and constants transcribed from the FULL TEXT, and the profile
> constructed at two or more resolutions, does Y₀ come in under the radii-polynomial budget at
> any tested resolution?"*

**NO.** At every tested resolution (`n = 601, 801, 1201`) `Y₀` exceeds the budget — by
**4.866e+10** at the finest — and the gap widens under refinement.

The no-branch's **second clause fires independently and is the more important of the two**:

> *"If the full text does not support the abstract as read (no explicit profile at γ = 2, or
> the a-neighbourhood excludes every usable case), that lands here too: quote the located text
> verbatim and the candidate leaves the ledger's top slot on literature grounds — which is
> itself the finding."*

It does not support it. **There is no explicit profile at γ = 2**; the located text is quoted
verbatim in §1.3 (*"Since ν(t) converges to 0, such profile is the same as the inviscid profile
associated with a."* — §2.6, p.12). And the a-neighbourhood is **unquantified** (§1.4).

**The candidate is set aside as "identified, measured, not under budget", and it leaves the
ledger's top slot on literature grounds. No retry without new information.**

**Why even a passing `Y₀` would not have helped.** The certificate would have certified the
*inviscid* a = ½ profile, which Chen gives in **closed form** (eq (2.2)) and verifies by hand
on p.4, and which `Papers/MANIFEST.md`'s exclusion list already records as covered analytically
for the entire smooth gCLM branch `a ≤ 1` (HQWW arXiv:2308.01528, arXiv:2305.05895). This is
the **same degeneracy** as the banned leg-51 clause — `Y₀` exactly zero because the a=0 CLM
profile *is* one basis mode — arriving for a **new reason**, and it is flagged here so it
cannot be re-read as progress later.

**Escalation note (report only).** The gate's yes-branch would have escalated a full
certificate-attempt leg to the user. The gate answered **no**, so there is nothing to escalate
on that ground, and no certificate was built under this leg's authority.

**Tripwire, checked and not tripped.** `ν` is floated in M5 and M7 against the **profile
equation's own residual** — Chen's object — never against a certificate's margin, a
`Z`-constant or `r_min`. The one banked certificate constant used (leg 53's `Z₁`) is held
**fixed** while `Y₀` varies, the opposite direction of dependence from the banned one.

---

## 6. Honest ceiling, pre-committed and unchanged

Not movement on `L1→L4`; not Clay. Clay odds stay **~0.05%**. In 125 legs no link of the chain
has moved and this leg does not move one. What is claimed is the sub-goal: no CAP of any
dissipative self-similar profile exists in the searched literature, so the measured `Y₀`, the
measured `Δ(a)` curve and its crossing at `a* = 0.386496` are novel data points — and the
candidate that topped the ledger for sixty legs is now **measured** rather than assumed.

## 7. What a follow-up would have to do (not proposed as a leg, just recorded)

The `a* ≈ 0.3865` corner is unclaimed by Chen and by everything the novelty pass returned. To
turn the lead into a result someone would have to (i) supply the missing equation — a second
normalisation that pins the one-parameter set M7 slides along — and (ii) re-run the dilation
covariance check as a **pass/fail gate**, with `a` required constant in `ν` to the solve
tolerance. Until both hold, there is no branch, only solutions of an under-determined system.
