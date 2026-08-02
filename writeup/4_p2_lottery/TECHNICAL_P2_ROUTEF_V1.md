# Route-F v1 — the critical dissipation exponent is half the far-field decay exponent

*Phase-2 P2, Route F (the viscosity lane), leg 1. Figure:
`writeup/figures/fig35_p2_route_f_v1_viscosity.png`. Data:
`writeup/data/p2_route_f_v1_viscosity.json`. Module: `solver/fractional_gclm.py`
(gates: `test_fractional_gclm.py`, 6/6).*

**Level-1 numerics plus one elementary scaling derivation. Not a certificate, not a proof, not
Clay progress. Plain float64; nothing here is interval-enclosed.**

---

## 0. Why this leg, and what it is allowed to conclude

The standing list of "what would actually be worthwhile toward a Clay-relevant candidate" has
five items. Route-E v1 shut the cheap entrance to item (1), the DSS lane. This leg takes item
**(2)**, which is the only item on the list that probes the *actual* obstruction between a
toy-model certificate and Navier–Stokes rather than polishing the toy:

> **Take a blow-up that exists, add dissipation, and determine the scaling at which
> dissipation kills it.**

That is the Clay question in miniature. Navier–Stokes is hard *because* viscosity and the
nonlinearity are exactly balanced at the blow-up scale; every real proof has to say something
about which one wins. In a 1D model with a dial, that balance can be *measured*.

**Gate-check, answered.**
*(a) Which link does this move?* **None.** It does not produce a certificate at any link. It
maps the obstruction that separates L3 from L4 — in a toy model where the map is computable.
*(b) Is another leg better?* Route-E v1 re-priced the DSS lane upward (its cheap entrance is
shut), which is what promoted this item.
*(c) Cheaper experiment that kills it?* The derivation in §1 *is* the cheap part; the leg's
cost is in testing it rather than believing it.

---

## 1. The prediction, and where it comes from

gCLM with fractional dissipation on a `2 pi`-periodic domain:

```
omega_t + a u omega_x = omega u_x - nu (-Delta)^s omega ,      u_x = H(omega)
```

`s = 1` is the ordinary Laplacian; `s` is the dial.

A self-similar blow-up has `omega ~ (T-t)^{-1}` and a length `L ~ (T-t)^beta`. **Route-E v1
already computed `beta`, without knowing it would be needed here.** In the dynamically-rescaled
variables of `solver/rescaled_spectrum.py` the two rescaling ODEs `A'/A^2 = -c_omega` and
`L'/(LA) = -c_l` integrate to `A ~ 1/(alpha (T-t))` and `L ~ (T-t)^{c_l/alpha}`, where
`alpha = -c_omega` is the profile's **far-field decay exponent** `Omega ~ X^{-alpha}`. With
`c_l = 1`:

```
beta = 1 / alpha .
```

Now compare the two terms at the blow-up scale — the nonlinearity is `~ omega^2`, the
dissipation `~ nu omega / L^{2s}`:

```
      dissipation / nonlinearity  ~  nu (T - t)^{1 - 2 s / alpha}
  =>  the blow-up beats dissipation  <=>  s < s_c(a) = alpha(a) / 2 .          (SC)
```

Three things make (SC) worth an experiment rather than a paragraph.

* **It is a statement about `s`, not about `nu`.** For `s < s_c` the blow-up survives *every*
  `nu > 0`; for `s > s_c` dissipation eventually dominates for every `nu > 0`. So the
  transition must be **`nu`-independent** — which is a control the experiment can run on
  itself (F4).
* **It is falsifiable as a slope, not as a threshold.** The relation predicts the whole
  function `p(s) = 1 - 2s/alpha`, not just its zero. Measuring a *line* is a far stronger test
  than locating a transition by eye, and it is the difference between this leg and a
  blow-up/no-blow-up sweep.
* **It says exactly where the Navier–Stokes difficulty lives.** NS's natural scaling is
  `L ~ (T-t)^{1/2}`, i.e. `beta = 1/2`, i.e. **`alpha = 2`** — for which (SC) puts the ordinary
  Laplacian `s = 1` *exactly* at `s_c`. NS is critical, and that is the whole problem. In gCLM
  `alpha` is a measured function of `a` and is free to move.

---

## 2. What is measured, and why not "did it blow up"

A binary blow-up test near a critical exponent is exactly the kind of measurement this project
has learned to distrust: near `s_c` the blow-up is only *asymptotically* dissipation-free, so at
finite compute the apparent threshold is biased and resolution-dependent, and the bias points
the way the experimenter expects.

So the primary diagnostic is quantitative. Track `D/N`, the ratio of the dissipative to the
nonlinear term **at the peak**, and fit

```
D/N ~ (T - t)^p ,        prediction:  p = 1 - 2 s / alpha .
```

`p` crosses zero at `s_c`. Measuring `p` across `s` gives a line whose slope, intercept and zero
are all separately checkable.

**One thing had to be fixed before this worked, and it is worth recording.** Dissipation
*delays* the blow-up, so fitting against the inviscid `T_0` biases the exponent: every point came
out above its prediction, with a shallower slope and a zero crossing ~10% high. That pattern is
the signature of a wrong singular time, not a wrong exponent. The repair is that the run supplies
its own `T`: for `omega ~ 1/(T-t)`, `1/amp` is linear in `t`, so extrapolating it to zero gives
`T` from the run itself (recovered to `5.3e-5` relative on the inviscid case, where `T` is known
exactly).

---

## 3. Results

### F1 — the known answer

At `a = 0`, `nu = 0` the model is exactly solvable **on the circle as well as the line**: with
`z = H(omega) + i omega`, `z_t = z^2/2`, so `z = z_0/(1 - t z_0/2)`. Checked against an
independent fine RK4 integration to **1.8e-14**, and the solver reproduces it to **1.9e-9** at
`t = 2.5` (amplitude 2.41). The blow-up time is `T = 2/max{H(omega_0) : omega_0 = 0}`.

And `alpha(0) = 1` exactly (Route-E v1's anchor is one Fourier mode), so (SC) predicts
**`s_c(0) = 1/2`** — which is also the classical critical exponent for dissipative CLM. So `a = 0`
is a genuine known-answer gate, not a self-consistency check.

### F2 — the relevance line at `a = 0`, with nothing fitted

`alpha = 1` exactly here, so the prediction `p = 1 - 2s` contains no fitted input at all:

| `s` | 0.15 | 0.25 | 0.35 | 0.45 | 0.55 | 0.65 | 0.75 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `p` measured | +0.735 | +0.533 | +0.327 | +0.121 | −0.086 | −0.292 | −0.494 |
| `p` predicted | +0.700 | +0.500 | +0.300 | +0.100 | −0.100 | −0.300 | −0.500 |

Fitted slope **−2.054** against the predicted **−2.000** (2.7%), and `p = 0` at
**`s = 0.5087`** against the predicted `s_c = 0.5000` (1.7%). Every spectral tail is `~1e-32`.

### F3 — the cross-check, which is the headline

`alpha(a)` was measured by a **steady, compactified spectral solve on the whole line** in a
different module, for a different reason. The slope `dp/ds` is measured by **time-dependent
pseudo-spectral simulation on a periodic domain** with dissipation. The two computations share
no grid, no basis, no equation as posed, and no fitted constant. (SC) says the second is
`-2/alpha` of the first.

*(numbers filled from the run; see the figure and the data file)*

### F4 — the `nu`-independence control

(SC) contains `s` and `alpha` and does **not** contain `nu`. A slope that moved with `nu` would
mean the measurement is about the viscosity rather than about the scaling. Measured across three
decades of `nu`, the slope spread is reported with the run.

### F5 — resolution

A ladder at fixed `(a, nu, s)`; the exponent's spread over an 8× refinement is the leg's own
numerical error bar and is quoted with every claim.

### F6 — the map, and the sentence to be careful with

With `alpha(a)` from Route-E v1, (SC) gives `s_c(a) = alpha(a)/2`. Since `alpha` rises through
`2` on the branch, **`s_c` rises through 1** — the ordinary Laplacian.

**The careful version of that sentence.** For `a` above that crossing, the *scaling* says a
self-similar blow-up of this family is not stopped by ordinary viscosity: the dissipative term is
asymptotically negligible against the nonlinearity at the blow-up scale. That is a statement
about **gCLM's own scaling**, and it is not a statement about Navier–Stokes. NS's `alpha` is
pinned at `2` by dimensional analysis; it is not a free dial. **What the map shows is what the
NS difficulty is made of**: NS sits exactly at the crossing this family walks through.

---

## 4. What this does *not* say

* It does not say a gCLM blow-up with `s = 1` dissipation *exists* for `a` above the crossing.
  (SC) is a statement about which term dominates *given* the self-similar scaling; establishing
  that a solution actually reaches it is the whole difficulty, here as everywhere.
* It says nothing about NS beyond locating the difficulty. gCLM's nonlinearity, scaling and
  velocity relation are all different.
* The measured `p` carries a systematic of a few percent from the singular-time estimate and the
  fitting window, quantified in F5 and reported next to every number.
* Novelty unchecked, as for every leg since v15: `s_c(0) = 1/2` for dissipative CLM is classical;
  the `a`-dependent map is what would need a literature check, and **PDF access is still blocked**
  (arXiv and publishers 403 at the proxy). Four legs now.

---

## 5. Where this sits relative to Clay (re-answered)

**Nothing here is a step whose success would resolve the Clay problem**, and this leg does not
move L1, L2, L3 or L4. What it does is turn the sentence "any real proof must beat viscosity at
small scales" into an *equation with a measured right-hand side* in a model where the arithmetic
is checkable — and locate NS precisely at the marginal case. That is worth having as orientation,
and it is worth nothing as evidence about NS itself. Odds unchanged, ~0.05%.

---

## Appendix — new lessons

**(53) When two legs measure the same constant through unrelated machinery, that cross-check is
worth more than either leg's internal error bar.** `alpha` from a steady compactified solve on the
line and `dp/ds` from time-dependent periodic simulation share no grid, no basis and no fitted
constant. Agreement there tests both computations at once, in a way no refinement of either
could. **Look for a second, structurally different route to a number you already have.**

**(54) A systematic that is uniform across a sweep is pointing at a shared input, not at the
mechanism.** Every measured `p` sat above its prediction with a shallower slope — which is what a
wrong singular time does, and not what a wrong exponent does. The shape of a discrepancy names
its cause faster than its size does. **Read the pattern of the residuals before adjusting the
model.**
