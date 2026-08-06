# Route-M2P v1 — Chen's γ=2 gCLM candidate: the full text, the constants, and the first Y₀

**Leg 125. Branch `leg/m2p-v1`. 2026-08-06.** Data: `writeup/data/p2_route_m2p_v1_promotion.json`.
Figure: `writeup/figures/fig61_route_m2p_v1_promotion.png`. Module: `solver/dissipative_profile.py`
(new), tests `test_dissipative_profile.py`. Driver: `experiments/p2_route_m2p_v1_promotion.py`.

**Stage claimed: none.** `NG` stays `NEXT`. **Clay: unmoved, ~0.05%.** This is not movement on
L1→L4 and was never going to be, whichever way the gate answered.

---

## 0. What was owed

Leg 63 (Route-M2) screened every certification target this repository has ranked and found
**one** that passes its multiplier/shift screen: gCLM with full Laplacian dissipation, γ=2,
tail-inverse K-exponent −2.0270, with blow-up **proved analytically** by J. Chen,
arXiv:1908.09385. It read the abstract only, and said so, leaving three debts:

1. read the full text (the `a`-neighbourhood unquantified, the ν-dependence unstated);
2. transcribe the profile's constants with provenance;
3. measure the first `Y₀` against the radii-polynomial budget.

This leg discharges those three. The novelty pass ran and was committed **first** (`5add939`,
`writeup/novelty/leg_125.md`) — 7 queries, 2 full fetches, and the same conclusion leg 63
reached at one level more depth: **no computer-assisted certificate of any dissipative
self-similar profile of a 1D fluid transport model exists.** The one real
CAP-under-dissipation precedent, Dähne–Figueras arXiv:2410.05480, is a CGL/NLS ODE continued
in the dissipation parameter — it pre-empted stage V's *question* and does not touch this
*object*.

---

## 1. The full-text read, which changes the object

### 1.1 The theorem, located and quoted

**Theorem 1.1, p.3** (arXiv v1 pagination), verbatim:

> "Consider (1.1) with `L ω = -∂_xx ω`. There exists `δ > 0` such that for
> `a ∈ (1/2 - δ, 1/2 + δ)`, `0 ≤ ν ≤ 1`, (2.1) develops a self-similar singularity in finite
> time for some `C_c^∞` initial data."

The headline survives: γ=2 blow-up is proved, `ν` up to 1.

### 1.2 The profile at γ=2 is the *inviscid* profile

§2 opens (p.4): *"Firstly, we study the inviscid problem, i.e. ν = 0."* Its eq **(2.2)**:

> `Ω = -2bx/(x²+b²)²`,  `U_x = (b²-x²)/(b²+x²)²`,  `U = x/(b²+x²)`,
> `c_l = 1/3`,  `c_ω = -1`,  where `b = √(3/8)`

and immediately after the verification, the sentence this whole leg turns on (p.4):

> "In this self-similar blowup, the spatial blowup scaling is `c_l = 1/3`, if we add the
> diffusion term, such term is asymptotically small compared to the nonlinear term in the
> equation of the self-similar variables. In our later analysis, we will treat the diffusion
> term as a small perturbation to the nonlinear part, especially the vortex stretch term
> `u_x ω`."

**Everywhere `ν` appears in Chen's argument it appears as the time-dependent `ν(t)`** — in the
approximate steady state (2.8), in the error term (2.10) `F(ω̄,t) = −(a−½)(ū − ū_x(0)x)ω̄_x +
ν(t)ω̄_xx`, and in the normalisation (2.11) `c_ω(t) = −u_x(0) − ν(t)ω_xxx(t,0)/ω̄_x(0)` — and
`ν(t) → 0`. The two that fix the steady object are on p.5:

* **(2.7)** `ν(t) = exp(∫₀ᵗ (c_ω(s) + 2c_l(s)) ds) C_l(0)^{-2} C_ω(0) ν`. At Chen's own
  constants the exponent is `-1 + 2/3 = -1/3 < 0`, so **`ν(t) → 0` exponentially** in the
  rescaled time.
* **(2.8)** `c̄_ω(t) = -1 - ν(t) ω̄_xxx(0)/ω̄_x(0)`, a correction that vanishes with `ν(t)`.
  Its constant is exactly `-12/b² = -32` (derived and tested), so `c̄_ω(t) = -1 + 32 ν(t)`.

The approximate steady state (2.8) **is** the inviscid profile (2.2), with
`c̄_l = 1/3 - (a - 1/2) ū_x(0)` and `ū_x(0) = 1/b² = 8/3`.

**Therefore: there is no ν-dependent steady profile in this paper to certify.** The thing leg
63 ranked first — "a dissipative self-similar profile with a proved blow-up behind it" — does
not exist as a distinct object at γ=2.

### 1.3 The γ tension, resolved — including a correction to this repository

A prior verifier's leg-64 review flagged a tension between Chen's criticality formula and the
abstract's "a close to 1/2 and γ=2". Resolved from the source:

1. **The formula is `γ = |a| - 1`, not `γ = |a|^{-1}`** (p.2, §1.2, verbatim: *"…which makes
   `Λ^γ` with `γ = |a| - 1` the critical dissipation with respect to the natural scaling of
   the equation."*). **The `|a|^{-1}` form carried in this repository is a transcription
   slip**, corrected here.
2. It holds **only for `a ≤ -1`**, where the a-priori `L^{|a|}` estimate exists. At `a = 1/2`
   it does not apply. There, `L¹` conservation makes **`γ = 1`** critical (p.2, §1.2).
3. So γ=2 at a=1/2 is *stronger* than critical — the regime where one naively expects global
   existence — and blow-up happens anyway. **The reason is the scaling, not the criticality:**
   diffusion-balanced scaling at γ=2 needs `c_l = 1/γ = 1/2`, and Chen's `c_l = 1/3 < 1/2`, so
   diffusion is asymptotically subdominant. There is no contradiction with Theorem 1.3's
   global well-posedness either: 1.3 covers Classes 1 and 2, Chen's blow-up data is Class 3,
   and Remark 1.4 states *"(1.4) is sharp due to the blowup result in Theorem 1.1."*

**`δ` is unquantified in the source.** Theorem 1.1 asserts "There exists `δ > 0`" and no
numerical value appears anywhere in the paper. This is now *known-absent*, not unread. Any
certificate attempt must supply its own `δ`.

### 1.4 Independent corroboration (unplanned)

Lushnikov–Silantyev–Siegel arXiv:2207.07548 was fetched and read at the same depth. Their
exact real-line solution list is: `a=1/2, σ=1`; `a=0, σ=1`; `a=0, σ=0`; plus a corrected
revisit of Schochet's `a=0, σ=2`. **There is no `a=1/2, σ=2` exact solution.** Their
`a=1/2, σ=1` solution (eq (55)) is described as *"an exact solution of the inviscid problem
ν = 0"*, with the same `α=1/3, β=1` double-pole shape as Chen's (2.2). Two independent
sources agree: at `a = 1/2`, the blow-up profile is the inviscid one regardless of the
dissipation.

Their §2 also records, verbatim, *"By rescaling each of t and ω̃, we can eliminate ν from the
problem. We therefore set ν = 1 without loss of generality"* — so a ν-continuation here is not
merely banned by stage V, it is **vacuous**.

---

## 2. The construction

`solver/dissipative_profile.py`. `capabilities.py` was grepped first (standing ban); the
nearest entries — `fractional_gclm.py` (Λ^s relevance thresholds), `critical_dissipation.py`
(criticality, not γ=2), `gclm_family.py` (the *inviscid* rescaled residual) — hold no
dissipative steady profile, which is why this is a new module.

Sinh grid `X = c sinh ρ` on `|X| ≤ 745`, dense spline Hilbert matrix (`solver/line_hilbert.py`),
4th-order `d/dρ` **as a matrix** (an exact Jacobian is needed, not just an action), and a
**4th-order cumulative velocity integral** — cumulative trapezoid in `X` is 2nd order and was
measured to be the accuracy bottleneck, holding the known-answer residual to order 2.00 while
the Hilbert transform and derivative both delivered 4.

### 2.1 The two objects

* **Object A — Chen's object as posed** (`ν = 0`):
  `F = (c_ω + U_X)Ω − (c_l X + a U)Ω_X`. At `a=1/2` the exact closed form (2.2) solves it.
* **Object B — the profile that would have to exist** for leg 63's reading to hold:
  `F = (c_ω + U_X)Ω − (c_l X + a U)Ω_X + ν Ω_XX`, with the **diffusive-invariance constraint
  `c_ω + 2c_l = 0`** forced by (2.7) — the condition for `ν(t)` to be constant, i.e. for a
  genuine dissipative steady state. Chen's own exponents give `−1/3`, which is the steady-side
  restatement of "the diffusion term is asymptotically small".

### 2.2 Two instrument faults, caught by controls rather than by inspection

Both are now pinned as regressions in `test_dissipative_profile.py` (25 checks, all passing).

**(a) The unbordered residual is exactly singular.** The equation carries two one-parameter
gauge symmetries: **dilation** `Ω(X) → Ω(μX)` at fixed `(c_l, c_ω)` — for Chen's family this
is exactly `Ω_b → μ^{-2}Ω_{b/μ}`, generator `X Ω_X` — and **amplitude**
`(Ω, c_l, c_ω) → λ(Ω, c_l, c_ω)`, the gauge `gclm_family.py`'s docstring already warns about.
The first version of this module inverted the singular block and reported `‖A‖ ~ 1e8–1e11`
with **`Y₀ = 0.179, 0.190, 0.148` at `n = 201/401/801` — independent of resolution**. A `Y₀` that does not fall when the residual
falls four orders is not a finding about the equation; it is an inverse that is not one.

**(b) The obvious border row is a tautology.** `U_X(0) = 8/3` looks like the natural
normalisation — it is Chen's `ū_x(0)`. It is **invariant along the dilation family**
(`μ^{-2}·(b/μ)^{-2} = 1/b²` identically), so bordering with it pins nothing. Measured at
`n = 401`: bordered `cond = 1.233e+07` against unbordered `σ_max/σ_min = 1.225e+07` — the
border bought a factor **0.99**. This is banked lesson 53/TC-5b exactly ("four identical
numbers should have read as a bug"). The border is now `Ω_X(0) = −2/b³ = −8.709296863`, which
*does* vary along the family (`→ μ Ω_X(0)`); `cond` fell to **4.74e+03** at `n=201`. The
tautology is kept in the module as a reported diagnostic and as a named regression test.

**(c)** A smaller one: a sup-norm line search rejected every full Newton step (ladder
`2.948e-04 → 2.912e-04` over five steps, reported "stalled") while the same steps undamped
reached `1.4e-12` in five and the float floor in six. Moved to a 2-norm criterion.

### 2.3 The known-answer gate

Chen's closed form against the discrete residual:

| `n` | 201 | 401 | 801 | 1601 |
|---|---|---|---|---|
| residual sup | 2.948e-04 | 1.912e-05 | 1.197e-06 | 7.633e-08 |

**Observed order 3.95, 4.00, 3.97.** `ū_x(0)` converges to `8/3` with relative error
`3.90e-06 → 1.00e-09`. This is the only place in the leg where the answer is known
independently of the solver, so it is what licenses every other number here.

---

## 3. The measurements

Convention re-read from `solver/weight_search.py::certificate_constants` rather than
transferred: `A = inv(J)`, `Y₀ = max(w|A F|)`, `Z₁ = max(w(|I − AJ|·1/w))`, `Z₂ = 2‖A‖_w B`,
weighted sup norm `w = (1+X²)^{s/2}` with border weight `w_c = 1`. Budget from
`solver/target_selection.py::y0_budget`, `(1−Z₁)²/(2Z₂)`. `F` is **exactly degree 2**, so the
Newton–Kantorovich remainder is exact and `B` is bounded term by term (tested: the remainder
scales ×4.000000 when the step doubles).

### 3.1 Object A — `a = 1/2`, `s = 0`

| `n` | Newton | residual | `c_l` (exact `1/3`) | `cond(J)` | `‖A‖` | `Y₀` | budget | `Y₀/budget` |
|---|---|---|---|---|---|---|---|---|
| 201 | ok, 3 steps | 3.553e-15 | 0.3336621749 | 4.74e+03 | 2.294e+02 | 1.6916e-14 | 1.466e-07 | **1.154e-07** |
| 401 | ok, 3 steps | 4.441e-15 | 0.3333773794 | 3.38e+04 | 7.456e+02 | 4.1955e-14 | 2.178e-08 | **1.926e-06** |
| 801 | ok, 3 steps | 1.008e-14 | 0.3333403924 | 2.42e+05 | 2.446e+03 | 1.8994e-13 | 3.275e-09 | **5.800e-05** |

`s = 1`: `Y₀/budget` = `1.325e-09`, `2.604e-08`, `8.889e-07`. **Under budget at every tested
resolution and both weights, by 4 to 9 decades.** `c_l` is recovered to `3.3e-04`, `4.4e-05`,
`7.1e-06` — converging on Chen's `1/3` as an independent second known answer.

### 3.2 Object B — the dissipative steady state, `ν = 1` FIXED

| `n` | Newton | residual | `c_l` | `c_ω` | rel. dist. to Chen | `Y₀` | `Y₀/budget` |
|---|---|---|---|---|---|---|---|
| 201 | **stalled** | 3.751e+00 | −12.5713 | 25.1426 | 5.794e-01 | 2.1013e+00 | 7.251e+10 |
| 401 | **stalled** | 2.652e+00 | −10.6740 | 21.3479 | 4.917e-01 | 4.5694e+00 | 5.480e+12 |
| 801 | **stalled** | 2.649e+00 | −10.6889 | 21.3777 | 4.926e-01 | 4.5320e+00 | 1.773e+14 |

Seeded from Chen's own profile — the most favourable start available — Newton runs away:
`c_l` to `≈ −10.7`, the iterate about half a profile-amplitude away, residual `O(1)` and flat
under refinement. **There is no dissipative steady state near Chen's profile to be under
budget of.** This is the numerical statement of the same fact §1.2 quotes from the text.

### 3.3 The `a`-neighbourhood — where the information actually is

At `a = 1/2` the profile is a closed form, so a `Y₀` there certifies an object one can already
write down. Off `a = 1/2` there is no closed form. (`a` is the **advection** parameter;
varying it is not varying a dissipation parameter, so the stage-V tripwire is untouched.)
At `n = 801`, `s = 0`:

| `a` | Newton | `c_l` | rel. dist. to Chen's closed form | `Y₀` | `Y₀/budget` |
|---|---|---|---|---|---|
| 0.40 | ok, 5 steps | 0.48095187 | 1.55e-01 | 3.6875e-13 | 7.819e-05 |
| 0.45 | ok, 5 steps | 0.40873853 | 8.30e-02 | 2.9377e-13 | 7.513e-05 |
| 0.48 | ok, 4 steps | 0.36393393 | 3.46e-02 | 3.6643e-13 | 1.044e-04 |
| **0.50** | ok, 3 steps | 0.33334039 | 1.79e-05 | 1.8994e-13 | 5.800e-05 |
| 0.55 | ok, 5 steps | 0.25385548 | 9.58e-02 | 5.9231e-13 | 2.200e-04 |
| 0.60 | ok, 5 steps | 0.16909737 | 2.06e-01 | 7.2041e-13 | 3.324e-04 |

Newton converges on **every** row, to genuinely different profiles — 20.6% away from Chen's
closed form at `a = 0.60`, with `c_l` moving monotonically from `0.481` to `0.169` across the
band — and `Y₀` stays about **4 decades under budget throughout**.

The `c_l` column is worth reading against Chen's own eq (2.8), which supplies the
**linearised** prediction `c̄_l = 1/3 − (a − 1/2)·ū_x(0) = 1/3 − (a − 1/2)·(8/3)`. It is
exact at `a = 1/2` (predicted `0.333333` vs measured `0.333340`, agreeing to `7e-06`) and
departs steadily off it:

| `a` | 0.40 | 0.45 | 0.48 | 0.50 | 0.55 | 0.60 |
|---|---|---|---|---|---|---|
| Chen (2.8) linearised `c̄_l` | 0.600000 | 0.466667 | 0.386667 | 0.333333 | 0.200000 | 0.066667 |
| measured `c_l` (n=801) | 0.480952 | 0.408739 | 0.363934 | 0.333340 | 0.253855 | 0.169097 |
| absolute departure | 0.1190 | 0.0579 | 0.0227 | 0.0000 | 0.0539 | 0.1024 |

That is what an approximate steady state *should* look like: it is Chen's own construction,
accurate to first order in `(a − 1/2)` by design, and the nonlinear solve measures how fast
the approximation degrades. It also gives a first quantitative handle on the `δ` the paper
leaves unquantified — though the handle is on the *linearisation's* accuracy, which is not the
same thing as the theorem's `δ`, and this leg does not claim otherwise.

**These appear to be the first measured `Y₀` values for gCLM self-similar profiles off
`a = 1/2`, in or out of the searched literature.** This is the part of the leg with real
novel content, and it is narrower than "the dissipative candidate" by a long way.

### 3.4 Leg 53's μ=2 positive control, re-read rather than transferred

`Z₁ = 0.9156 at μ = 2` **does not transfer**, on two independent counts:

1. **`μ` is a coefficient, not an exponent.** `solver/spectral_certificate.py` line 74:
   *"POSITIVE CONTROL: add `-mu k` to the diagonal (fractional dissipation `Lambda^1`…)"*,
   and lines 257/371 subtract `mu * k`. The control is **γ = 1 with coefficient 2**, not γ=2.
2. **Different object.** It was measured on the `a = 0` CLM linearisation in the compactified
   coefficient basis at `K = 16`, `s = 0.3`, unbordered tail — an anchor whose `Y₀` is exactly
   0 for the banned degenerate reason. Neither the operator, the basis, nor the anchor is
   this leg's.

What survives is the methodological point it was built for and which this leg does rely on: a
dissipative multiplier *can* pull an assembled `Z₁` below 1, so a `Z₁` above 1 is a
measurement and not a broken instrument. That is a claim about the instrument, not a constant
to reuse.

---

## 4. The gate

> **"With Chen's theorem located and constants transcribed from the FULL TEXT, and the profile
> constructed at two or more resolutions, does Y_0 come in under the radii-polynomial budget
> at any tested resolution?"**

**YES.** Object A is under budget at every tested resolution (201/401/801) and both weight
classes (`s = 0, 1`), by 4 to 9 decades; best `Y₀/budget = 1.325e-09`. Per the pre-committed
yes-branch: magnitudes banked above, **no certificate built under this leg's authority**,
branch pushed and **not merged**, escalated to the user.

### 4.1 How the YES must be read

The yes-branch fires, but the full-text read changed what it fires *on*, and this is the part
that matters for the escalation decision:

* **The object that clears the budget is Chen's INVISCID closed-form profile.** The property
  that made this candidate uniquely attractive to leg 63 — *dissipative*, hence novel against
  an empty CAP literature — **does not survive §1.2**.
* A certificate here would be a certificate of an **inviscid gCLM profile at `a ≈ 1/2`**. This
  repository's own exclusion list already records that the entire smooth gCLM branch for
  `a ≤ 1` is analytic (HQWW arXiv:2305.05895 / 2308.01528, `Papers/MANIFEST.md`), which is why
  such targets were excluded in the first place.
* At `a = 1/2` exactly, the target has a **closed form** — certifying it is certifying
  something already written down.
* **The genuinely novel remainder is narrower and real:** the `a ≠ 1/2` profiles (§3.3), which
  have no closed form, are not in the searched literature, and for which this leg reports the
  first measured `Y₀`. That, and not "the dissipative candidate", is what a certificate-attempt
  leg would actually be aiming at.

The gate's own no-branch clauses were checked and **not** triggered: there *is* an explicit
profile at γ=2 (it is just inviscid), and the `a`-neighbourhood does *not* exclude every usable
case (`a = 1/2` is interior to it, and `a = 0.45–0.48` converge). So this is a YES, reported
with the qualification rather than downgraded by it.

---

## 5. Ceiling, pre-committed and non-negotiable

* **Not movement on L1→L4. Not Clay progress. Clay stays ~0.05%.** Only the novel-output
  sub-goal was ever in play.
* Every constant here is the **truncated discrete** system on `|X| ≤ 745`, in **float**, with
  `A = inv(J)` an exact float inverse. The far-field tail beyond the grid is **not bounded**,
  and `Z₁` is float conditioning rather than a rigorous bound. `Y₀` under budget is a
  **necessary** condition for a certificate, never sufficient — the same ceiling
  `solver/interval_certificate.py` carries for L1 step one.
* The `|X|^{-1}` far field that the transport operator cannot invert (legs 51–53) has **not**
  been dealt with here. It is the reason `cond` grows ~7× per doubling and it would have to be
  bordered, as in leg 52, before any interval-arithmetic pass.
* **Tripwire: not crossed.** `ν` is a fixed constant everywhere; no dissipation parameter was
  floated against any certificate's margin; there is no certificate here whose margin could be
  floated. `no_dynamics_run: true` — no gCLM time evolution was run, so the "another gCLM
  measurement leg" ban is untouched.
