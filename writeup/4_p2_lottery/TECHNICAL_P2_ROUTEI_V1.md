# Route-I v1 — the marginal flow, driven

*Phase 2 / P2, leg 41. Figure: `writeup/figures/fig38_route_i_v1_driven.png`.
Code: `solver/marginal_flow.py`, `test_marginal_flow.py` (11/11),
`experiments/p2_route_i_v1_driven.py` → `writeup/data/p2_route_i_v1_driven.json`.
Working notes: `PHASE2_P2_NOTES.md` §30.*

**Level-1 numerics plus one exact-solution gate. NOT a certificate, nothing
interval-enclosed, no link of the L1→L4 chain moved. Clay odds unchanged at ~0.05%.**

---

> ## ⚠️ THE `μ = 0` STABILITY COUNT NEEDS ITS REALIZATION NAMED
> *(added 2026-08-04, Route-J v1 primary-source pass — **this is a live correction, not a
> retraction**)*
>
> This leg's headline is that the **inviscid** rescaled fixed point at `a = 1/2` has
> **141 of 144 unstable directions**, read as "§26's essential spectrum as a count".
> **arXiv:2607.19762 Proposition 2** (Xu, realization dichotomy) shows that what that
> count is counting is realization-dependent: the essential-spectrum smear which grids
> **without an origin condition** place inside the strip is the faithful spectrum of the
> **maximal `L²` realization**, and the **origin-`H²`** realization has none of it.
> **Our discretization has no origin condition — the loose realization is the one we
> measured.**
>
> This does **not** make the measurement wrong, and it does **not** by itself touch the
> `μ > 0` half of the inversion (dissipation collapsing the spectrum onto a *discrete*
> negative ladder is not realization-smear). It does mean the `μ = 0` count is quoted in a
> realization nobody would choose deliberately. **The count must be stated with the
> realization named, and the honest next step is to re-run I5 with an origin condition and
> report what the count is there.** That is the top-ranked correction item for the next leg.
>
> Route-I also inherits Route-F's pre-emption in full: `λ_μ = 2s - α₀` is Route-F's `s_c`
> in spectral clothing, and `s_c = α/2` is **Xu §6.1 eq (6.3)**, posted eleven days before
> Route-F. See `TECHNICAL_P2_ROUTEJ_V1.md` and `LITERATURE_CHECK.md` sixth pass.

---

## 0. What this leg is, in one paragraph

Route-H v1 (§29) wrote down the augmented flow — the rescaled gCLM equation with the
dissipation coefficient `mu = nu/(A L^{2s})` promoted to a dynamical variable — and then
read it *statically*: Newton at frozen `mu`, `alpha(mu)` off the resulting branch, and
the dynamics inferred from the shape of that curve. Two numbers came out of that reading
and **neither was ever integrated**. This leg integrates the coupled system as an
initial-value problem and measures both from a trajectory. It also answers the piece of
ranked item (2) that §27 and §28 left open — *the scaling says which term dominates given
the self-similar form; does a viscous solution actually reach that form?* — and the
answer turns out to be more interesting than the arithmetic that motivated it.

The equations, unchanged from §29:

```
Omega_tau = (c_omega + H Omega) Omega - X Omega_X - a U Omega_X - mu Lambda^{2s} Omega   (F_mu)
mu_tau    = (2 s - alpha[Omega, mu]) mu ,      alpha = -c_omega                          (M)
```

with `c_omega = 1 + (a-1) H(Omega)(0) + mu (Lambda^{2s}Omega)_X(0)/Omega_X(0)`, in
Route-E's compactified odd-sine basis (`X = tan(theta/2)`), where `H`, the dilation
operator, the velocity and `Lambda^p` for integer `p` are all exact and quadrature-free.

---

## 1. The headline: the stability inversion

At `a = 1/2` the linearization of the **inviscid** rescaled flow about its self-similar
fixed point is violently unstable. Counting eigenvalues of `S^{-1} dR/db` with
`Re > 1e-6`, excluding the exact dilation mode:

| K | unstable directions at `mu = 0` | max Re |
|---|---|---|
| 48 | 45 of 48 | +4.524 |
| 96 | 93 of 96 | +4.546 |
| 144 | 141 of 144 | +4.558 |

This is §26's essential spectrum `[-2, +5]`, seen as a count. A fixed point with a
141-dimensional unstable manifold is not an attractor and nothing generic reaches it.

**Any `mu > 0` removes all of it.** The spectrum becomes a discrete negative ladder —
`0` (the exact dilation mode), then approximately `-1`, then `-4.7`, and downward — and
the gap between the neutral mode and the next one is insensitive to `mu` across four
decades. That is the dynamical statement the scaling legs could not make: at criticality
the viscous self-similar profile *is* linearly attracting, and its inviscid limit is not.

### 1.1 Why this is not the artifact it looks like

Adding a large negative-definite operator to a matrix pushes its eigenvalues left, so
"`mu > 0` stabilizes the truncated generator" is exactly the sort of claim that is an
artifact of truncation. The crossover settles it. Dissipation damps mode `k` at rate
`mu k^p`, so it beats a growth rate `g` once

```
mu K^p  >~  g ,     i.e.   mu*(K) ~ g / K^p ,     g = max Re of the inviscid generator.   (C)
```

Measured, with `g = 4.55`:

| K | crossover bracketed in | (C) predicts |
|---|---|---|
| 48 | `[1e-5, 1e-4]` | `4.1e-5` |
| 96 | `[1e-6, 1e-5]` | `5.1e-6` |
| 144 | `[1e-6, 1e-5]` | `1.5e-6` |

`mu*` falls with `K`. So **at any fixed `mu > 0` a fine enough grid sees zero unstable
directions, and at any fixed `K` a small enough `mu` sees ~`K` of them: the two limits do
not commute.** An artifact would need `mu*` to be independent of `K` or to grow with it.

**How much of that the ladder actually resolves, stated plainly.** The `mu` grid is
decade-spaced, so the bracket has one-decade resolution. `48 -> 96` moves it by a full
decade (measured **x10**, (C) predicts **x8**) — that step carries the claim. `96 -> 144`
predicts only **x3**, which is *below* the ladder's resolution, and the bracket duly does
not move (**x1.0**). That is consistent with (C) and is **not** independent evidence for
it; reading the flat step as confirmation would be reading the grid. A sharper test needs
a finer `mu` ladder, and it is the obvious next thing to spend time on if this claim ever
has to carry weight.
(C) is also the resolution guard every trajectory here is run against — for the leg's
main trajectory, `mu >= 0.02` at `K = 96` needs `K > 6.1`, a margin of about 16x.

### 1.2 Where the instability lives — and why it is the DSS band

The leading inviscid eigenvalue at `K = 96` is **`+4.5455 + 430.35i`**. The unstable
spectrum is not a set of slowly growing modes; it is a curve on which `Re` *increases*
with `|Im|`:

| max Re restricted to | `|Im| <= 2` | `<= 5` | `<= 10` | `<= 30` | `<= 100` | all |
|---|---|---|---|---|---|---|
| K = 96 | +0.313 | +0.718 | +1.004 | +2.252 | +3.365 | +4.546 |
| K = 144 | +0.119 | +0.309 | +0.745 | +1.770 | +2.990 | +4.558 |

and `max|Im|` grows with `K` (430 at `K = 96`, 661 at `K = 144`). These are exactly
Route-E's continuum modes `exp(i y (tau - log X))` — the log-periodic directions. **So
the directions that grow fastest in the inviscid rescaled flow are precisely the ones a
discretely self-similar solution is built out of, and dissipation is what removes them.**
That is a sharper statement than §26's ("a continuum has no eigenvalue to move") and
§29's ("dissipation discretizes the continuum, and nothing crosses"): the continuum is
not merely unable to bifurcate, it is the *unstable* part, and `mu` deletes it rather
than damping it — at `mu = 0.05` the whole band is gone, max Re `= -1e-13`.

Two consequences worth carrying:

* the DSS lane's obstruction is now **doubly** stated. A DSS solution needs the
  log-periodic structure; in the inviscid problem that structure is continuous spectrum
  (§26) *and* it is where all the growth is (here); in the viscous problem it is absent
  entirely. The lane is not closed, but nothing in three legs has produced a mechanism
  by which it opens.
* **any time integrator caps the `|Im|` it can resolve at ~`pi/dt`**, so a nonlinear
  growth rate measured from a generic kick is a *lower bound* on max Re, not a
  measurement of it. Stated below rather than discovered later.

---

## 2. Route-F's critical exponent, measured as a growth rate

`lambda_mu = 2s - alpha_0` is the growth rate of `mu` at the inviscid fixed point — the
spectral form of Route-F's `s_c`. Integrating (M) from `mu_0 = 2e-3` and fitting
`d(log mu)/d tau` in the linear regime, at `a = 1/2` where `alpha_0 = 3` exactly:

| p (= 2s) | s | predicted `2s - alpha_0` | measured | seed residual | `Lambda^p` truncation | |
|---|---|---|---|---|---|---|
| 1 | 0.5 | −2.0000 | **−2.00141** | 3.2e−8 | 2.8e−7 | kept |
| 2 | 1.0 | −1.0000 | **−1.00042** | 9.4e−7 | 3.4e−3 | kept |
| 3 | 1.5 | 0.0000 | **−0.00026** | 2.3e−8 | 1.1e−2 | kept |
| 4 | 2.0 | +1.0000 | **+1.00030** | 1.1e−9 | 1.3e−1 | kept |
| 5 | 2.5 | +2.0000 | (+2.00699) | 9.4e−10 | **1.77** | **REFUSED** |

Fitted as a line in `s` **over the four kept rows**: **slope +2.0011** against a
predicted +2, **zero at `s = 1.50009`** against a predicted 1.5, worst kept error
**1.4e−3**. Two signs, three non-marginal points, and the marginal one returning
`−2.6e−4`.

This is not a re-derivation of §27. Route-F fitted a power law to `D/N` along a
time-dependent *periodic pseudo-spectral* trajectory and read `s_c` off where the
exponent crossed zero; this fits an exponential growth rate of a different variable in a
*compactified steady-basis* integration on the line. No shared grid, basis, formulation
or fitted constant. The prediction `2s - alpha_0` uses `alpha_0 = 3`, a number this
computation never sees.

**Three refusals, and they are the honest part of this section.** The rung gate asks two
separate questions — is the *profile* resolved (seed residual < 1e−5) and is the
*operator* accurate (`Lambda^p` truncation < 1) — and a rung has to pass both.

* **`p = 5` at `a = 1/2` is refused on the operator**, truncation **1.77**: the discarded
  coefficients exceed the kept ones. Its number, `+2.00699`, would have looked like the
  *best* confirmation in the table — it is the largest `|lambda_mu|` and lands within
  0.35% — which is exactly why the gate is on the operator and not on the agreement.
  This is Route-H's H4 finding recurring: `Lambda^p` amplifies mode `k` by `~k^p`, so the
  same `K` that is ample at `p = 3` is not at `p = 5`.
* **All three `a = 0.3` rungs are refused on the profile.** Off the resonances `alpha_0`
  is not an integer, the compactified basis converges algebraically rather than
  spectrally, and the seed residual is 6e−4 to 4e−3 at the same `K` — two to five orders
  worse than the 1e−9..1e−8 at `a = 1/2`. **So this leg has no off-resonance control**,
  and the two rungs that came closest (`p = 1`: −0.64493 against −0.6172; `p = 2`:
  +0.37352 against +0.3828, both ~4% out) are reported as refused rather than quoted as
  a weak confirmation. `p = 3` there returns **−3.39** against a prediction of **+1.38**
  — wrong sign, wrong magnitude — which is what an unresolved profile is worth.

The `a = 0.3` refusals matter for what the leg is allowed to claim: the growth-rate law
is confirmed **at one value of `a`**, the resonance where the basis is spectral. Whether
it holds off the resonances is untested here, and the earlier draft of this section
quoted the `a = 0.3` numbers as a passing control — they are not.


---

## 3. The tar pit, driven

At criticality (`a = 1/2`, `p = 3`) the linear term in (M) vanishes and `mu_tau =
-alpha_1 mu^2`. Route-H got `alpha_1` by extrapolating secants of `alpha(mu)` on the
frozen-`mu` Newton branch. Here it is the slope of `1/mu` along a trajectory — `1/mu` is
linear in `tau` under the quadratic law, which is why the fit lives there.

**At matched K, the two computations agree:**

| K | dynamic (this leg) | static (§29) | apart |
|---|---|---|---|
| 96 | 0.132362 | 0.132770 | 0.31% |
| 144 | 0.133302 | 0.133470 | 0.13% |
| 192 | 0.133491 | 0.133628 | 0.10% |

Both ladders climb toward ≈0.1337 and the gap between them *narrows* with `K`, which is
what two discretizations of the same quantity should do. The verdict is
`relaxes_to_inviscid` from both.

Error budget, and it is a different one from Route-F's:

* **the time step is not the systematic.** BDF2 self-convergence order **1.994** over
  `dt = 1 … 1/8`, spread in `alpha_1` **8.7e-5**, so signal/discretization ≈ **1520**.
  The refusal gate (`> 10`) is cleared by two orders.
* **the fit window is not the systematic either.** Sweeping `mu <= 0.30 … 0.10` moves
  `alpha_1` by ~2e-5. In Route-F the window *was* the dominant systematic; here it is
  negligible and `K` is everything. Worth saying out loud, because the reflex after §27
  is to sweep the window and quote its spread as the error bar — it would understate the
  error here by two orders.
* **the gauge is enforced, and the enforcement does no work.** `sum_k k b_k = -1` is an
  exact invariant of (F_mu) (`c_omega` is *defined* by `R_X(0) = 0`, which is
  `kk . S^{-1}R = 0`). Numerically that identity holds to a relative 3.6e-9 per step,
  which accumulates to a drift of **4.0e-4** over `tau = 60` — 3% of the `alpha - alpha_0`
  signal the leg quotes. The flow therefore subtracts the dilation component roundoff put
  there. Turning the subtraction **off** moves the headline by **0.037%**, and the drift
  goes from `-4.7e-14` to `+4.0e-4`. Both halves are gated: a projection that had to do
  real work would be a bug wearing a fix's clothes.

Over `tau = 0 … 600` from `mu_0 = 0.3`, the integrated `mu(tau)` tracks the closed law
`1/(1/mu_0 + alpha_1 tau)` to within a few percent at worst, and the decay times are the
ones §29 predicted: nine times the `tau` per decade, forever, with `tau` itself
logarithmic in `(T-t)`.

---

## 4. Adiabaticity — the static reading's assumption, measured

Reading `alpha` off a frozen-`mu` branch is only legitimate if the driven trajectory
stays on that branch. It does, and it gets better with time: the relative distance
`||Omega(tau) - Omega*(mu(tau))||_inf` runs **1.2e-4 → ~2e-7** over the long run. It
should tighten — the driving rate is `mu_tau ~ mu^2`, so as `mu` decays the flow is
pulled off the branch ever more slowly while the restoring gap stays at ≈1.

Starting **off** the branch is the stronger version, and it needs a qualification that
the first version of this section did not have.

Perturbing `Omega` by `eps` and letting `mu` run reproduces the on-branch `mu(120) =
0.052067` to **0.000%** and `alpha_1 = 0.132361` to six digits, for `eps` up to `5e-2`.
That agreement is exact-looking because it should be: the spectral gap is `≈ -1`, so
over `tau = 120` a perturbation is suppressed by `e^{-120}`, i.e. below double
precision. It is an independent confirmation of §1's inversion through the nonlinear
flow rather than a separate fact.

**What `eps` measures, and why it is not what it looks like.** The perturbation is
normalized in the functional the gauge (N′) actually reads,
`b -> (Lambda^p Omega)_X(0)`, not in the coefficient sup-norm — and those differ by
**3.6e8** at `a = 1/2, p = 3, K = 96`. `Lambda^p` weights mode `k` by `~k^p` and the
derivative at the origin adds one more power, so that functional's condition number is
`~K^4`. Consequences, both worth stating:

* the *first* version of this measurement normalized in coefficients, which made
  `eps = 1e-3` a `3.6e5` **relative** perturbation of the quantity the flow divides by.
  `alpha` came back as `11713` instead of `3.037` at `tau = 0`, before a single step,
  and every off-branch trajectory overflowed. Every published number in this section
  was `nan`. See §8, lessons (65) and (66);
* correctly normalized, `eps = 5e-2` is a **`5e-11` relative change in the profile**.
  So this is a strong test of the *gauge-sensitive* direction and a **weak** test of
  profile-scale robustness. It is not a basin-of-attraction measurement, and it should
  not be read as one — **§5's twin trajectories are the profile-scale test**, and they
  are the ones to cite for how big a perturbation the viscous fixed point actually
  absorbs.

This is the same `k^p` amplification that Route-H's H4 found making `Lambda^5`
unusable: one mechanism, showing up in two legs as two different symptoms.

---

## 5. The nonlinear control

Eigenvalues of a truncated generator are a claim about a matrix. Twin trajectories —
integrate the kicked and unkicked states side by side and difference them — are a claim
about the flow.

| `mu` | twin-trajectory rate | spectral gap | apart | fit residual | |
|---|---|---|---|---|---|
| 0 | +1.904 | +4.5455 | 58% | **1.49** | lower bound (see below) |
| 1e−3 | −1.812 | −1.0002 | **81%** | **2.32** | not asymptotic |
| 0.05 | **−1.0143** | −1.0114 | **0.3%** | 0.007 | clean |
| 0.2 | **−1.0441** | −1.0437 | **0.0%** | 0.012 | clean |

**The fit residual is what separates the rows, and it separates them by two orders**
(0.007–0.012 against 1.49–2.32). Where a single exponential describes the trajectory,
the twin-trajectory rate reproduces the spectral gap to a fraction of a percent — that
is the control that matters, and it says the linear-stability claim of §1 survives
passage through the nonlinear flow. Where a single exponential does *not* describe the
trajectory, the fitted "rate" is not a rate, and the table says so rather than averaging
it in.

Two rows are quoted as failures on purpose:

* **`mu = 0` is a lower bound, not a measurement.** `dt = 0.01` resolves `|Im| <~ 314`
  and the leading eigenvalue sits at `|Im| = 430`, so no usable time step can realize
  `+4.55`. What the row establishes is only that the kick *grows*, by **4.6e5** in
  `tau = 6`. Any integrator caps the `|Im|` it can see at `~pi/dt`, so a nonlinear rate
  from a generic kick is always a lower bound on max Re — stated in §1.2 before it was
  needed rather than discovered here.
* **`mu = 1e-3` has not reached its asymptotic rate.** The gap is `−1.0002`, but at that
  `mu` the dissipative ladder is barely separated and the kick's projection onto the
  slowest mode is small, so over `tau = 6` the difference is still dominated by faster
  transients — visible directly in fig38 F as the kinked orange curve, and in the fit
  residual of 2.32. It is **not** evidence against §1; it is evidence that this
  instrument needs either a longer run or a larger `mu`, and the two larger-`mu` rows are
  the ones that carry the control.

An earlier draft of this section reported the `mu = 1e-3` row as "≈ −1.0, <1%". It is
81% out. The number was never in the data; the row was written from what the eigenvalue
said it *should* be.

**A measurement that went wrong first, kept because the failure is the lesson.** The
obvious version of this test — integrate the kicked state and watch `|b(tau) - b0|` —
reads the *base state's own motion*, because `b0` is a Newton fixed point with residual
~1e-8 rather than an exact one, and it drifts at a rate comparable to a small kick. Run
that way, `mu = 0.05` and `mu = 0.2` both returned a **growth** rate of **+1.5**, the
opposite of what every eigenvalue says, with no diagnostic complaining. Differencing
against a twin removes the base motion exactly, for the price of one more trajectory.

---

## 6. Where this sits relative to Clay

**It moves no link of the chain.** L1 (a certified profile in 1D) is untouched — nothing
here is interval-enclosed and no budget is closed. What it does is convert the previous
two legs' *inferred* dynamics into *measured* dynamics, and answer the dynamical half of
ranked item (2) in the toy: at criticality a viscous solution does reach the self-similar
form, because that form is linearly attracting once `mu > 0`, and it then cannot leave
because `mu` decays algebraically.

The honest translation to NS is narrow and should be stated as such:

* `s = 3/2` is **hyperviscosity**. It is used because that is where criticality can be
  posed exactly in this basis, not because it resembles NS.
* the relevant structural fact — *the inviscid rescaled fixed point is unstable in a
  continuum of log-periodic directions, and dissipation deletes that continuum* — is the
  kind of statement that ought to be standard in the parabolic-blowup literature. See
  §7.
* "linearly attracting in this norm at this truncation" is not "an attractor". The
  unstable-count statement is about the spectrum of a truncated generator, supported by
  the K-ladder (C) and by a nonlinear trajectory; it is not a theorem about the continuum
  operator, whose essential spectrum for `mu > 0` is not computed here.

---

## 7. Novelty: unchecked, and probably thin

`(M)` itself is at risk through Route-F/H's inheritance — the dissipative-gCLM relevance
exponent is reported in arXiv:1908.09385 / arXiv:2207.07548, and `lambda_mu = 2s -
alpha_0` is that exponent in spectral clothing. See `LITERATURE_CHECK.md`; **arXiv:2207.07548
is still the first paper to read and it now gates four claims.**

The three methodological candidates from this leg are **unsearched** (WebFetch remains
403 on every host including Wikipedia; WebSearch is the only channel):

1. the stability inversion — `mu > 0` removing a continuum of unstable directions of the
   *rescaled* flow, with the non-commuting limits made quantitative by (C);
2. the identification of the fastest-growing inviscid directions with the DSS band;
3. twin-trajectory differencing as the control on a computed spectral gap.

Presume (1) known — it is the sort of thing that follows from the resolvent of a
sectorial operator and someone has certainly written it down for a parabolic blowup
problem. (2) is the one worth a specialist's five minutes.

---

## 8. Lessons banked (61)–(66)

* **(61) A number read off a trajectory needs a regime bound, not just a fit window.**
  At `a = 0.3, p = 3` "the first 40% of the run" gave +11.8 against a prediction of +4.6
  because `mu` had left the linear regime by `tau = 1.2`. The fit must be bounded by the
  *variable*, not only by the *time*.
* **(62) Differencing against a twin trajectory is how you measure a perturbation off an
  inexact fixed point.** A Newton fixed point at residual 1e-8 drifts as fast as a small
  kick, and the naive measurement returned the opposite sign with nothing complaining.
* **(63) When a truncated operator becomes stable under a perturbation, the crossover's
  K-scaling is the artifact test.** `mu*(K) ~ g/K^p` falling with `K` says the limits do
  not commute; an artifact would have `mu*` flat or rising.
* **(64) The dominant systematic changes between legs, and the reflex is to reuse the
  previous leg's.** Route-F's error bar was the fit window; here the window contributes
  2e-5 and `K` contributes 1e-3. Quoting the window spread as the error bar would have
  understated it by two orders.
* **(65) A refused computation must be refused in the DATA STRUCTURE, not just in the
  prose.** Every off-branch run in §4 overflowed; `integrate` returned the state anyway,
  the driver stored `alpha_1 = nan`, and the figure legend rendered *"off-branch
  ε=0.001: α₁ = nan"* — three times, in a published panel. Finiteness alone is not the
  test either: with a partial fix the same run stayed finite and ended at
  `mu = -1.6e24`. The discriminator that works is the implicit solve's own residual over
  its floor (~6e2 healthy, 1e13 failed), and `integrate` now reports `converged` from it.
* **(66) "Small" is meaningless until you say IN WHICH NORM, and the binding norm is
  set by the operator, not by the coefficient vector.** A perturbation at `1e-3` in
  coefficient sup-norm was `3.6e5` in the functional the gauge divides by, because
  `Lambda^p` weights mode `k` by `k^p`. The symptom was total (`alpha = 11713` at
  `tau = 0`); the cause was invisible in the quantity being reported. Normalize in the
  functional that binds, and **report both numbers**, because the corrected perturbation
  turned out to be `5e-11` of the profile — which changes what the measurement is
  entitled to claim.
