# Route-E v1 — the rescaled gCLM flow has no eigenvalue available for a Hopf bifurcation

*Phase-2 P2, Route E (the DSS lane), leg 1. Figure: `writeup/figures/fig34_p2_route_e_v1_spectrum.png`.
Data: `writeup/data/p2_route_e_v1_spectrum.json`. Module: `solver/rescaled_spectrum.py`
(gates: `test_rescaled_spectrum.py`, 8/8).*

**Level-1 numerics plus two small exact computations. Not a certificate, not a proof, not
Clay progress. Plain float64 throughout; nothing here is interval-enclosed.**

---

> ## ⛔ NOVELTY RETRACTED, ONE OPEN QUESTION CLOSED, ONE RESULT RE-CLASSIFIED
> *(added 2026-08-04, Route-J v1 primary-source pass)*
>
> **1. The point-spectrum negative is pre-empted.** **arXiv:2607.19762 Theorem 2** (Xu)
> proves the full point spectrum of the CLM linearization on the odd origin-`H²`
> realization is exactly `{0, 1}` — the symmetry modes, no embedded eigenvalues — in our
> own normalization `Ω = -y/(y² + 1/4)`. This leg is **confirmed but not novel**.
>
> **2. THE ESSENTIAL-SPECTRUM CONTINUUM IS RE-CLASSIFIED, and this is the important one.**
> Xu's **Proposition 2 (realization dichotomy)**: the essential-spectrum *smear* that grids
> **without an origin condition** place inside the strip is the faithful spectrum of the
> **maximal `L²` realization**; imposing the single second-derivative condition at the
> origin removes the entire non-symmetry family (explicitly, `u_λ(y) = y^{1-λ}/(y+i/2)²`,
> `L²` but with `u'' ∉ L²` at the origin). **Our discretization has no origin condition, so
> we were rendering the loose realization and did not know there was a choice.** The DSS
> conclusion survives — in the tight realization there is no continuum *and* no complex
> pair, so there is still nothing to bifurcate — but "the non-symmetry spectrum is
> continuous" must be stated as a property of the realization, not of the operator.
>
> **3. `α(1/2) = 3` is exact and known, AND THIS LEG'S OPEN QUESTION IS ANSWERED.** This
> writeup recorded that *"what stays unexplained is why `α = 3` lands on a round rational
> while `α = 5` does not"*. **arXiv:2207.07548 §1** answers it: exact pole-dynamics
> solutions exist at `a = 0` and `a = 1/2` and, per Lushnikov et al., **nowhere else**.
> `c_l(1/2) = 1/3` is exact; verified here to 7.7e-5 by integrating their `a = 1/2` system
> cold. The `α = 5` point at `a = 0.5821792673` is a property of **our instrument** (`Λ⁵`
> is a finite matrix there), not of the problem.
>
> **4. The `α(a)` branch and `a_c` are published.** `a_c` (Lushnikov–Silantyev–Siegel) is
> **0.6890665**; Xu's recompute is 0.6888 (**0.04%**); ours is 0.693493 (**0.64%**). We are
> the least accurate of the three and should quote theirs.
>
> See `TECHNICAL_P2_ROUTEJ_V1.md` and `LITERATURE_CHECK.md` sixth pass.

---

## 0. Why this leg exists, and what it was allowed to conclude

Route D spent sixteen legs on link **L1** of the chain — a certified self-similar blow-up
profile for a 1D toy model. Leg v15 (the literature check) found that L1 is very probably
occupied territory: computer-assisted interval/Newton–Kantorovich certification is routine
for the groups working this family. That did not invalidate a single measurement, but it did
re-price the lane, and it promoted a different item to "the swing":

> **Nečas–Růžička–Šverák (1996), extended by Tsai**: exactly self-similar blow-up for 3D
> Navier–Stokes in the natural scaling class is *ruled out*. Therefore the entire
> "find a self-similar profile and certify it" template cannot be pointed at NS as posed.
> The candidate class that survives is **discretely self-similar (DSS)**.

In dynamic-rescaling variables the translation is exact, and it is why this leg is cheap:

| object | in rescaled variables |
| --- | --- |
| self-similar blow-up | a **fixed point** of the rescaled flow |
| DSS blow-up | a **periodic orbit** of the rescaled flow |

A global search for a periodic orbit is expensive and needs somewhere to start. But one
mechanism would both *produce* a periodic orbit and *tell you where it is*: a **Hopf
bifurcation** off the self-similar branch — a complex-conjugate pair of eigenvalues crossing
the imaginary axis as `a` moves. If such a pair exists the DSS lane opens with a concrete
starting point; if there is no eigenvalue capable of crossing, that route is closed and the
lane has to be entered some other way.

That is a question about a spectrum, and a spectrum is one dense eigenvalue solve.

**Gate-check, answered rather than re-pasted.**
*(a) Which link does this move?* **None.** It does not advance L1→L4. It is lane scoping.
*(b) Is another L1 leg better?* No — v15 re-priced L1 downward and named this as the swing.
*(c) Is there a cheaper experiment that would tell us the route is dead?* **This was it**, which
is why it was worth doing before any DSS search machinery was built.

---

## 1. The flow, and the one modelling choice in it

gCLM on the line: `omega_t + a u omega_x = omega u_x`, `u_x = H(omega)`. Dynamic rescaling
`omega(x,t) = A(t) Omega(X,tau)`, `X = x/L(t)`, `dtau/dt = A` gives

```
Omega_tau = (c_omega + H Omega) Omega - c_l X Omega_X - a U Omega_X ,   U(X) = int_0^X H(Omega) dX'
```

The two gauge functions `(c_omega, c_l)` carry the two scaling freedoms. This leg fixes
`c_l = 1` — **a choice, and it is stated as one** — and determines `c_omega` from the
normalization that freezes the origin slope. Requiring `(Omega_tau)_X(0) = 0` for odd `Omega`
gives, exactly,

```
c_omega[Omega] = 1 + (a - 1) H(Omega)(0) .                                        (N)
```

At `a = 0` this **is** the value-based normalization the project has used since Spike 0
(`solver/gclm_rescaled.py`), so this is the same flow continued in `a` rather than a new
convention. Worth saying out loud: the project's existing residual used `c_omega = 1 − H(Omega)(0)`
at *every* `a`, and that version has **no fixed point at all** for `a != 0` — differentiating the
residual at the origin gives `R_X(0) = -a H(Omega)(0) Omega_X(0) != 0`. (N) is the repair, and
it is forced, not chosen.

With `c_l` fixed, **dilation survives as a symmetry**: `Omega(X) -> Omega(X/mu)` is again a
fixed point, and `H(Omega)(0)` is dilation-invariant so (N) is untouched.

---

## 2. The discretization: the far field costs nothing here

Compactify with `X = tan(theta/2)` and expand the **odd** profile in sines. Three operators
are then exact on the whole line, with no domain truncation and no quadrature:

```
H(sin k theta) = -cos k theta + (-1)^k
X d/dX         = sin(theta) d/d theta          <- the DILATION term is bounded and exact
d/dX           = (1 + cos theta) d/d theta
```

The `(-1)^k` is not decoration: `H^2 = -1` only modulo constants on the line, and that constant
is exactly what makes `H(Omega)` vanish at `X = infinity`.

The velocity is exact too. Writing `N_k(t) := ((-1)^k - cos k t)/(1 + cos t)`, the identity
`2 cos t cos kt = cos(k+1)t + cos(k-1)t` gives

```
N_{k+1} = -2 N_k - N_{k-1} - 2 cos k t ,      N_0 = 0,  N_1 = -1,
```

so **every `N_k` is a trig polynomial** — the `1 + cos t` in the denominator always cancels —
and `U = sum_k b_k int_0^theta N_k` is elementary. There is no quadrature anywhere in the
build. (Gate 2 checks this as a polynomial identity out to `k = 30`, not merely at the anchor.)

**The `a = 0` fixed point is a single mode.** `Omega_0 = -sin theta = -2X/(1+X^2)`, with
`H(Omega_0) = 1 + cos theta = 2/(1+X^2)` and `c_omega = -1`. It nulls the residual to
**1.1e-16** at every `K` tested. Sixteen Route-D legs worked in this same compactified
variable; this is the first time the *self-similar* (dilation) anchor has been written in it,
and it is one Fourier mode.

---

## 3. Two eigenvalues are exact, at every `a`, and they are symmetry

Before computing anything, write down what has to be there. Let `L` be the linearization of
the flow at a fixed point. Then

```
L (X Omega_X) = 0                              (dilation)
L (Omega)     = -Omega + X Omega_X             (amplitude)
```

The first is the dilation symmetry: the orbit is a curve of fixed points, so its generator is
in the kernel. The second follows by substituting the profile equation into `L(Omega)` and
using (N). So `span{Omega, X Omega_X}` is invariant with matrix `[[-1,0],[1,0]]`:

> **lambda = 0 (dilation) and lambda = -1 (amplitude), for every `a`.**

A Jordan-like pair, present at every parameter value, **carrying no dynamical information**.
Any DSS-relevant eigenvalue has to be something else. `structural_pair_defect` measures both
identities rather than trusting them: **3.0e-15 / 3.3e-16** at `a = 0` and **1.3e-10 / 9.1e-15**
at `a = 1/2`, with the `2x2` block itself exact to **6.1e-16**.

**And the same two identities double as a free error bar.** Because `lambda = 0` is exact, its
*computed* deviation measures the error of the whole spectrum at that parameter. At `a = 0.2`
the dilation defect is `8.0e-2` and the filter duly reports the dilation mode at `-0.352`;
at `a = 1/2` the defect is `1.3e-10` and it reports `+8.9e-5`. That single number is what
licenses (and forbids) every quantitative claim below.

---

## 4. At `a = 0` the rest of the spectrum is known in closed form

Set `w = e^{-i theta}` and `Z = H Omega + i Omega`, so the anchor is `Z_0 = 1 + w`. Writing
the `a = 0` linearization in `s = delta Z`:

```
L s = w s - ((w^2 - 1)/2) s_w - s(w=1) (1 + w) .
```

For `s(1) = 0` the homogeneous problem `L s = lambda s` is a first-order ODE and integrates:

```
s_lambda(w) = (w - 1)^{1 - lambda} (w + 1)^{1 + lambda} .
```

The verification is one line — `((w^2-1)/2) s_w = s (w - lambda)`, hence `L s = lambda s` —
and admissibility does the rest: `s -> 0` at `w = -1` (decay at `X = infinity`) needs
`Re lambda > -1`; `s` bounded and vanishing at `w = 1` (i.e. at `X = 0`) needs `Re lambda < 1`.

So the `a = 0` linearization carries a **continuum of eigenvalues filling the strip
`-1 < Re lambda < 1`**, whose eigenfunctions carry a **fractional power** `(w-1)^{1-lambda}`
at the origin. Demanding analyticity there forces `1 - lambda` to be a non-negative integer,
and with `Re lambda > -1` that leaves exactly `lambda = 0` and `lambda = -1` — the two
structural modes and nothing else.

### 4.1 The member worth looking at is `lambda = i y`

Near the origin `w - 1 ~ -2iX`, so

```
s ~ X^{1 - i y}          against the time factor   e^{i y tau}
  =>  exp( i y ( tau - log X ) )
```

— a wave travelling **outward in `log X` at unit speed**, exactly `tau`-periodic with period
`2 pi / y`. **That is the log-periodic structure a DSS solution is made of, and it is present
in this operator, exactly.** It is *continuous* spectrum, not a bound state: it is the dilation
transport carrying a scale-invariant wave to infinity. Nothing there can cross an axis. That
is the mechanism behind this leg's negative rather than a restatement of it, and gate (5b)
checks the identity with a numerical derivative and confirms the period.

---

## 5. The branch: `alpha(a)` is an output, and it runs away

Following the fixed point from the exact anchor by continuation, the far-field decay exponent
is a result, not a parameter: `c_omega Omega = (X + a U_inf) Omega_X` gives

```
Omega ~ X^{-alpha} ,   alpha(a) = -c_omega(a) .
```

Richardson-extrapolated over `K = 64/128/256`:

| `a` | 0 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 |
| --- | --- | --- | --- | --- | --- | --- |
| `alpha` | 1.000000 | 1.141397 | 1.334497 | 1.617244 | 2.079464 | **3.000000** |

`alpha` increases with `a`; following it finely (`K = 192`, `da = 0.005`) the branch is lost at
`a = 0.65` with `alpha = 11.5` at the last good point, and `1/alpha` extrapolates linearly to
zero at **`a_c ~ 0.694`** — the tail becomes infinitely steep and the branch, as posed on the
whole line, ends. This is the self-similar analogue of what Route-D v12/v14 found for the
*traveling-wave* object (which ends at a finite radius `X_c`); different object, so the
agreement is a check rather than a repetition.

**One consequence governs everything numerical here.** A branch point of order `alpha` at
`X = infinity` means the sine coefficients decay *algebraically* — measured residual `K^-2`ish
at `a = 0.3` (`7.8e-2 -> 6.7e-4` over `K = 16..256`). There is exactly one exception on the
branch besides the anchor:

* `a = 0`, `alpha = 1` — exact, one mode;
* **`a = 1/2`, `alpha = 3` — `c_omega = -3.000000000000`, residual `1.4e-14` at `K = 192`**
  (`2.7e-1 -> 4.4e-2 -> 7.0e-5 -> 1.4e-11 -> 1.4e-14` over `K = 16..192`; geometric coefficient
  decay, i.e. analytic).

The `a = 1/2` point was *found*, not assumed: a scan of the fixed-point residual in `a` at fixed
`K` shows a single dip, ten orders deep, exactly there.

### 5.1 The odd-`alpha` rule: hypothesised from two points, tested at a third, and
### nearly discarded on two rungs of a ladder

`Omega ~ (pi - theta)^alpha` near `X = infinity`, so "`alpha` an odd integer makes the profile
smooth there" is the natural reading — and it fits both special points (`alpha = 1` and `3`).
That is a rule inferred from a two-point set with one degree of freedom, so E8b/E8c went and
found the third point: `alpha = 5` occurs at **`a = 0.5821792673`** (secant-solved to `5e-11`).

The `K`-ladder there is the interesting part, because **its first two rungs say the opposite of
its last four**:

| `K` | 96 | 128 | 192 | 256 | 320 | 384 |
| --- | --- | --- | --- | --- | --- | --- |
| `sup|R|` | 3.19e-2 | 1.12e-2 | 7.92e-4 | 2.87e-5 | 9.24e-7 | 2.55e-8 |
| implied order | — | 3.6 | 6.5 | 11.5 | 15.4 | 19.7 |

An order that **rises monotonically** is not an order at all — it is exponential convergence
seen before it has settled. **`alpha = 5` is an analytic resonance too, and the odd-`alpha` rule
holds at all three points.** The `alpha = 5` profile is simply steeper (`Omega ~ X^-5` against
`X^-3`), so it enters its asymptotic regime later; at the `K = 256` of the E8b scan its dip is
only `13x` deep, and by `K = 384` it is four orders.

*This paragraph replaced an earlier version of itself.* On the first two rungs (`3.19e-2 ->
1.12e-2`, order `3.6`) this note said the rule was **false** and that `a = 1/2` was special for
an unidentified reason. Two rungs of a ladder are not a rate — banked lesson (22) applied one
level down — and the correction is marked rather than quietly edited (banked lesson (35)).

What survives as genuinely unexplained is narrower and more specific: **`alpha = 3` lands at
exactly `a = 1/2`**, while `alpha = 5` lands at `0.5821792673`, which is not an evidently
special number. So the rule explains *why* those `a` are analytic; it does not explain why one
of them is a round rational.

**Novelty unchecked** — an exact exponent at `a = 1/2` in this family is precisely what may be
folklore to people who work on gCLM/De Gregorio, and the literature check is still blocked on
PDF access (v15's finding).
A two-parameter rational ansatz `Omega = -c X/(X^2+gamma)^2` reproduces the profile to
**7e-5** relative — the right *shape*, right down to the location and depth of the minimum —
but the profile itself is computed to `2e-14`, so the ansatz is a near miss and **the closed
form was not identified.**

Because of all this, **every quantitative spectral statement below is quoted at `a = 0` or
`a = 1/2`** — the only two points on the branch where the fixed point is analytic. At generic `a` the instrument cannot resolve even the eigenvalues it is known to
have (§3), and no conclusion is drawn there.

---

## 6. The spectrum

### 6.1 What the filter said, and why the first reading of it was wrong

Refining `K = 96 -> 144` and keeping the eigenvalues that move less than `1e-2`:

| `a` | kept |
| --- | --- |
| 0 | `0` (dist 8e-16), `-1` (dist 6e-15) |
| 1/2 | `+8.9e-5` (dist 9e-5), `-1.000005` (dist 5e-6), **`-2.0073` (dist 5.6e-3)** |
| 0.1, 0.2 | two values, but the *dilation* one is reported at `-0.120` / `-0.352` — see §3 |
| 0.3, 0.4, 0.55 | nothing (the fixed point is not resolved well enough) |

The third entry at `a = 1/2` is not symmetry, and the honest first reaction was that the
fixed point has a genuine non-symmetry mode. A `K`-ladder makes it look even better —
`-2.007293 / -2.001677 / -2.000467 / -1.999999` over `K = 96..256`, converging on `-2` exactly.

**It is not a mode. It is the left edge of the essential spectrum.** The two singular endpoints
of the operator fix that spectrum's extent: near `X = infinity` the local operator is
`c_omega + xi d/d xi` with `xi = pi - theta`, and near `X = 0` it is
`(c_omega + H Omega(0)) - theta d/d theta`, so

```
        c_omega + s_min  <=  Re lambda  <=  c_omega + H(Omega)(0) ,
```

and in *this* space `s_min = 1`, because every `sin k theta` vanishes linearly at `theta = pi`.
So the accessible strip is `[c_omega + 1, c_omega + H(Omega)(0)]` — which is `[0, 1]` at
`a = 0` and `[-2, +5]` at `a = 1/2`. Both edges land where predicted: the measured spectrum
spans `[-2.007, +4.55]` at `a = 1/2`, and `c_omega + 1 = -2` **is** the value the "third
eigenvalue" converges to.

The control that settles it costs nothing, because the project already had it: **at `a = 0`
the same edge sits at `0`, and 99% of the discretized spectrum sits on it.** Nobody would call
that an isolated eigenvalue. It is the same object at `a = 1/2`, moved to `-2` because
`c_omega` moved.

### 6.2 The verdict

> **The only grid-converged ISOLATED eigenvalues, at both points where the method can see, are
> `0` and `-1` — the two exact symmetry modes. There is no complex pair anywhere, nothing
> approaching the imaginary axis, and therefore no Hopf bifurcation off the gCLM self-similar
> branch.**

Two things must be said alongside it, and neither weakens it:

* **The flow is not spectrally stable.** Its ESSENTIAL spectrum reaches `c_omega + H(Omega)(0)`,
  which is `+1` at `a = 0` and `+5` at `a = 1/2` — well into the right half plane, complex
  members included (the measured cloud runs to `Im ~ ±150`). Those directions are exactly the
  ones with a fractional power at `X = 0`: a *corner at the origin* grows relative to the
  profile. That is the familiar low-regularity essential instability of self-similar
  linearizations, it is norm-dependent, and — this is the point — **a continuum has no
  eigenvalue to move, so it cannot Hopf-bifurcate.**
* At `a` between the two resonances the instrument is too blunt to say anything, and §3's free
  error bar is how that is known rather than guessed.

### 6.3 The positive control — the part that makes the negative mean something

"Only two survived the filter" is evidence only if the filter would have reported more. The
same filter, on the same operator with a smooth localized potential added:

| potential | converged eigenvalues | max shift from the plain operator |
| --- | --- | --- |
| `V = 3` | `-0.864` | 0.14 |
| `V = 6` | **`+1.083`**, `-0.833` | 1.08 |
| `V = 12` | **`+4.578`**, `-0.814` | 4.58 |

**The instrument can see an isolated unstable eigenvalue, twice over. There is not one.**

### 6.4 What this does *not* say

* Not that gCLM has no DSS solution — only that one is **not born from a Hopf bifurcation off
  the self-similar branch that continues from CLM**. Periodic orbits can exist without a fixed
  point nearby that spawned them, and §4.1 shows the log-periodic directions themselves are
  present (in the continuum).
* Nothing about NS. gCLM's scaling structure is not NS's; the only reason DSS is interesting
  for NS is a theorem about NS.
* The essential spectrum's location is **norm-dependent**, and what is measured is the spectrum
  of a *discretization*, filtered for grid-independence. An eigenvalue embedded in the continuum
  can be missed by any such method. `a = 0`, where the closed form settles it independently, is
  the only place that risk is retired.
* One gauge only (`c_l = 1` plus (N)). Changing the normalization moves the symmetry
  eigenvalues but not the transverse spectrum — standard, but an *argument* here, not a
  measurement.

---

## 7. What this cost, and what it bought

Cost: one module, one experiment, eight gates, and two follow-up measurements the first sweep
forced. Bought:

1. **The cheapest DSS mechanism is closed** for the 1D family, with a positive control behind
   the negative and a *mechanism* (§4.1, §6.1) rather than an absence.
2. **The self-similar branch of gCLM in the compactified variable** — exact one-mode anchor,
   exact velocity operator, Newton continuation.
3. **`alpha(a)`**, the far-field decay exponent map, as an output, with the branch's end.
4. **The odd-`alpha` resonance family** — `alpha = 1` (exact), `alpha = 3` at `a = 1/2` (12
   digits), `alpha = 5` at `a = 0.5821792673` (exponential ladder to `2.5e-8`) — and the
   narrower open question it leaves: why `alpha = 3` lands on a round rational. Novelty
   unchecked; closed form not identified.
5. **Two exact statements about the `a = 0` linearization**: the closed-form continuum
   `(w-1)^{1-lambda}(w+1)^{1+lambda}` on the strip `-1 < Re lambda < 1`, and the
   log-periodic identification of its imaginary members.
6. **The essential-spectrum edge formula** `[c_omega + 1, c_omega + H(Omega)(0)]`, confirmed at
   both exactly-resolved points — which is what turned a spurious "third mode" into a
   measurement.

### Where this sits relative to Clay (re-answered, not re-pasted)

Unchanged, and stated plainly: **nothing here is a step whose success would resolve the Clay
problem.** This leg moves no link of the chain. What it does is stop the project spending
several legs building a DSS search around a mechanism that does not exist in the family where
its tooling lives. The two structural walls are untouched. Odds ~0.05%, unchanged.

The honest summary of the DSS lane after one leg: **the lane is not closed, but the cheap
entrance is.** Entering it now costs a real build — a periodic-orbit search in the rescaled
flow with no fixed point nearby to seed it — and §4.1 says where such an orbit would have to
live (the log-periodic directions, which are continuous spectrum and of limited regularity at
the origin). That is a much bigger commitment than this leg was, and it should be weighed
against the alternatives (the Hou–Luo critical-viscosity map; the L1→L2 port to 2D Boussinesq)
rather than taken by default.

---

## Appendix — new lessons this leg paid for

**(46) A symmetry audit is cheaper than an eigenvalue solve, and it predicts part of the
answer.** Two eigenvalues here were derivable in five lines from the flow's two symmetries.
Doing that *first* meant the numerical spectrum arrived with its expected members already
named, so "only two survived" read immediately as "nothing but symmetry" instead of looking
like a result. **Enumerate the symmetry modes before computing a spectrum; they are the null
result's baseline.**

**(47) A null result needs a planted positive, not just a control.** Banked (2) says ablate to
attribute and (9) says build the adversary; this is the third member. When the finding is
*absence*, show the instrument detecting a *presence* of the same kind. Planting a bound state
and recovering it at `+1.083` and `+4.578` costs three lines, and is the difference between
"there is no unstable eigenvalue" and "we did not find one".

**(48) When you generalize a gauge, re-derive it — do not extend it.** `c_omega = 1 - H(Omega)(0)`
is correct at `a = 0` and was being carried at every `a`. For `a != 0` that flow admits **no
fixed point at all**; one line of algebra at the origin catches it. This is banked (29) —
*a constant is attached to a point, not to a problem* — wearing the gauge's clothes.

**(49) The regularity of the object sets the convergence rate of everything built on it, and it
can vary with the parameter.** Here `alpha(a)` is an output and is an odd integer at exactly
two points on the branch; there the method is spectral and everywhere else second-order, a
ten-order accuracy swing driven by nothing but the parameter. **Find where your object is
smooth and quote your sharp numbers there**, instead of quoting one accuracy for a whole sweep.

**(50) An exactly known eigenvalue is a free error bar on every other one.** The dilation mode
is `0` by symmetry, so its computed value *is* the spectrum's error at that parameter — `0.35`
at `a = 0.2`, `8.9e-5` at `a = 1/2`. That number decided which rows of the sweep were allowed
to carry a conclusion, and it cost nothing to read. **If a symmetry pins one eigenvalue, plot
its deviation next to every claim you make about the others.**

**(52) Two points define a line through anything — and two RUNGS define a convergence rate
through anything.** "`alpha` odd integer => analytic" fitted the only two special points I had,
so the third was located by secant and laddered. Its first two rungs implied order `3.6` and I
wrote the rule off as false; four more rungs showed the order climbing `6.5 -> 11.5 -> 15.4 ->
19.7`, i.e. exponential convergence that had not settled, and the rule was right after all. The
mistake and its repair are the same lesson at two scales: **before a fitted exponent becomes a
claim, add rungs until the exponent stops moving.** A steeper object reaches its asymptotic
regime later, which is exactly when a short ladder is most misleading.

**(51) A convergence filter can be fooled by the EDGE of a continuum, and the fix is a control
point, not a tighter tolerance.** The `-2` at `a = 1/2` converged to six digits under
refinement and was not a mode: it was `c_omega + 1`, the accumulation edge of the essential
spectrum in this space. Tightening the filter would have made it look *better*. What exposed
it was evaluating the same quantity at `a = 0`, where the identical edge carries 99% of the
discretized spectrum and is obviously not an eigenvalue. **Before believing an isolated
eigenvalue, ask where the continuum's edges are — and go and look at the same object somewhere
you already understand it.**
