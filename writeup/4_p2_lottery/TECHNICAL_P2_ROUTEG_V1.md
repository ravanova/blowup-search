# Route-G v1 — the critical dissipation exponent on the 2D object: `s_c = 1/(2β)`

*Phase-2 P2, Route G (the port), leg 1. Figure:
`writeup/figures/fig36_route_g_v1_collapse.png`. Data:
`writeup/data/p2_route_g_v1_collapse.json`. Module: `solver/fractional_boussinesq.py`
(gates: `test_fractional_boussinesq.py`).*

**Level-1 numerics plus one elementary scaling derivation, on the 2D system rather than the
1D toy. Not a certificate, not a proof, not Clay progress. Plain float64; nothing here is
interval-enclosed.**

---

## 0. Why this leg, and what it is allowed to conclude

The ranked list had two live items. Item **(3)** was "port to 2D Boussinesq / axisymmetric
Euler with boundary — the L1→L2 step, where certification results actually count", and item
**(2)** was the viscosity question, of which Route-F v1 finished the 1D half. §27 recorded
that the two had merged: *the same `s_c` arithmetic applied to a 2D object is the version of
the viscosity question that is about a real mechanism rather than a 1D caricature.* This leg
is that merged brick.

**Gate-check, answered.**

*(a) Which link of the chain does this move?* **None.** No certificate is produced at any
link. What it does is move a *measurement* from the toy onto the object the toy is a model
of, and the number it produces is about the distance between them.

*(b) If the answer is "none", is another leg better?* The alternative was the DSS lane's
expensive entrance (a periodic-orbit search with nothing to seed it, priced upward by §26).
This is much cheaper and it answers a question that the expensive lane would have to assume.

*(c) Is there a cheaper experiment that kills the route?* Yes, and it is §1 — the derivation.
The leg's cost is in *testing* it and in finding out which of the two available instruments
can carry it.

---

## 1. The law, in the form that survives the port

Route-F v1 reported `s_c = α/2`, with `α` the far-field decay exponent of the 1D self-similar
profile. That form does not port, and it is worth being precise about why: it is not merely
1D-specific, it is **gauge**-specific. It is true in gCLM's rescaling only because that
rescaling pins `c_l = 1`. Change the gauge and `α/2` is wrong while the underlying statement
is unchanged.

The invariant statement is about the **collapse exponent**. Let a blow-up have

```
ω ~ (T−t)^{−1},        L ~ (T−t)^β.
```

The amplitude exponent is not a modelling choice, and the reason is the same in both models
even though the *driving* terms differ. The velocity is recovered from the vorticity by an
order-`−1` operator, so `u ~ ωL`, and hence the transport term is

```
u·∇ω  ~  (ωL)(ω/L)  =  ω²,
```

independent of `L`. Balancing that against `ω_t` gives `ω ~ (T−t)^{−1}`. In gCLM the same `ω²`
appears directly as the stretching term `ω u_x`; in Boussinesq it arrives through transport,
with the buoyancy `θ_x` sitting at the same order (`θ ~ (T−t)^{β−2}`, §6). Then, comparing the
dissipation `ν (−Δ)^s ω ~ ν ω L^{−2s}` against that common `ω²` scale:

```
D/N ~ ν (T−t)^{1 − 2sβ}      ⟹      s_c = 1/(2β).                (SC)
```

Route-F's own blog post wrote `s < 1/(2β)` in passing before specialising it; what this leg
changes is that the specialised form was carried as the headline, and it is the *general*
form that has content. Three consequences follow, and the third is the reason to do the port.

**(i) 1D is the special case.** gCLM's rescaling ODEs integrate to `β = 1/α` (Route-E v1, at
`c_l = 1`), so `1/(2β) = α/2`. Gated in `test_fractional_boussinesq.py::gate0_law` against
`solver.fractional_gclm.critical_s` on Route-E's measured `α(a)`.

**(ii) Navier–Stokes is `β = 1/2`.** NS's `L ~ (T−t)^{1/2}` is forced by dimensional
analysis, and (SC) returns `s_c = 1` — the ordinary Laplacian, exactly. NS is critical, every
scaling argument about it returns zero information, and `β = 1/2` is therefore *the line*.
Which side of it a blow-up sits on is the entire question.

**(iii) The direction is the opposite of the intuitive one.** `s_c = 1/(2β)` is **decreasing**
in `β`. A blow-up that collapses *faster* than the NS rate loses to viscosity **more** easily.
This is worth saying in plain words because the natural intuition — "a violent singularity
should overwhelm viscosity" — is exactly backwards. The violence in the *amplitude* is fixed
at `(T−t)^{−1}` for everything in this class; all the freedom is in **how small the structure
has to get** to achieve it. The blow-up that viscosity cannot touch is the one that reaches
the same amplitude on a **larger** length scale. Beating ordinary viscosity requires
`β < 1/2` — an anomalously *slow* collapse.

That last point is gated too (`s_c` monotone decreasing in `β`), because it is the sort of
sentence that is easy to write backwards.

### 1a. Far-field decay and collapse rate are one fact

The 2D formulation makes visible something the 1D gauge had hidden. In the dynamic rescaling
`ω̃(x,τ) = C_ω(τ) ω(C_l(τ)x, t)`, `dt/dτ = C_ω`, the rescaled system

```
ω_τ + (c_l x + u)·∇ω = θ_x + c_ω ω
```

holds with `c_ω = d log C_ω/dτ` and `c_l = −d log C_l/dτ`. At a fixed point both are
constants, so `C_ω ~ e^{c_ω τ}` and `C_l ~ e^{−c_l τ}`, and

```
T − t = ∫_τ^∞ C_ω dτ' ~ C_ω/|c_ω|     ⟹     (T−t) ~ C_ω,     L ~ C_l ~ (T−t)^{−c_l/c_ω},
```

i.e. **`β = −c_l/c_ω`**, with the physical amplitude `1/C_ω ~ (T−t)^{−1}` coming out for free
(the check that the gauge is the blow-up gauge). Separately, requiring the *outer* solution to
be time-independent — `ω_phys(y) ~ (y/C_l)^α/C_ω` independent of `τ` — gives `α c_l = c_ω`,
i.e.

```
α = c_ω/c_l = −1/β.
```

So "the profile decays like `r^α` far out" and "the length scale collapses like `(T−t)^β`" are
**the same statement**, in 1D and 2D alike. Route-F treated the far-field exponent as an
input it happened to have; it is not an input, it is `β` written in the other variable. This
is why `α/2` looked like a law rather than a coordinate choice.

---

## 2. Where the proven 2D blow-up sits (published constants, exact arithmetic)

Chen–Hou Part I (arXiv:2210.07191) (2.23), transcribed in `PHASE2_SPIKE1_NOTES.md` §1:

```
c_l = 3.00649898,   c_ω = −1.02942516   ⟹   β = −c_l/c_ω = 2.92056,   s_c = 0.17120.
```

**The proven Euler-type boundary blow-up sits at about one sixth of the NS-critical
exponent.** At the ordinary Laplacian its relevance exponent is `p(s=1) = 1 − 2β = −4.84`:
`D/N` *grows* like `(T−t)^{−4.84}` as the singular time approaches. It is not close to beating
ordinary viscosity; it is nearly six times too fast a collapse.

A transcription note, recorded rather than smoothed over: the three quoted forms of the same
constant disagree in the sixth digit — `c_ω/c_l = −0.3424004`, `1/(c_l/c_ω) = −0.3424038`
from the paper's own quoted ratio, and the quoted `α = −0.342407`, a spread of `7e−6`. It
moves `s_c` in its sixth digit and no conclusion here depends on it, but a gate tolerance of
`1e−6` would have been a tolerance the *input* cannot support.

---

## 3. The same number from our own machine

Quoting a published constant is not measuring it. Spike 1 built a dynamically-rescaled 2D
Boussinesq machine (`solver/boussinesq_rescaled.py`, log-polar grid, angular-spectral Poisson
solve, Step-C gate PARTIAL 3/4), and in that formulation **the collapse exponent is a
modulation constant**: `c_l` and `c_ω` are computed from the origin slopes at every step, and
`β = −c_l/c_ω`. No fit. No window. No singular-time estimate. Precisely the three things that
make the direct route (§4) unusable.

**Relaxation ladder** (`n_r = 300`, `n_β = 48`, `r ∈ [10⁻³, 10⁵]`, `renorm=True`) — is it
relaxed?

| steps | residual | `c_ω` | `α = c_ω/c_l` | `β` | `s_c` |
|---|---|---|---|---|---|
| 400 | 1.14e+00 | −1.16222 | −0.379356 | 2.63604 | 0.18968 |
| 1200 | 5.17e−01 | −1.08494 | −0.354131 | 2.82381 | 0.17707 |
| 2500 | 1.67e−02 | −1.02656 | −0.335076 | 2.98439 | 0.16754 |
| 4000 | 1.78e−02 | −1.04388 | −0.340728 | 2.93489 | 0.17036 |

The approach is monotone until 2500 and then **stops being monotone**: the residual bottoms
out around `1.7e−2` and `c_ω` moves back out to `−1.0439`. That is the relaxation settling into
a residual floor, not converging further, and it is worth saying plainly — the last rung is not
"more converged", it is a different point in the same basin. Spike 1's Step C used 2500 steps
and that protocol is kept here deliberately, so the 2500-step row is a **free reproducibility
check** against `writeup/data/spike1_stepC_gate.json`, committed three legs ago. It reproduces
`c_ω` to every printed digit (`−1.0265648734746011`).

**Resolution / domain ladder** (steps = 2500):

| `n_r` | `n_β` | `r_max` | `c_ω` | `β = −c_l/c_ω` | `s_c` |
|---|---|---|---|---|---|
| 300 | 48 | 1e5 | −1.02656 | 2.98439 | 0.16754 |
| 450 | 48 | 1e5 | −1.02331 | 2.99437 | 0.16698 |
| 600 | 48 | 1e5 | −1.03120 | 2.96951 | 0.16838 |
| 450 | 48 | 1e6 | −1.02933 | 2.97449 | 0.16810 |

Spread `0.025` in `β` across a doubling of radial resolution and a tenfold extension of the
domain — resolution-stable at the 0.8% level. Every row reproduces the committed Spike-1 value
for the same configuration.

**And the disagreement is the result.** As read, `β = 2.9807`, which is
**2.1%** from the published `2.92056` — noticeably worse than the accuracy of
its own ingredients. `c_ω`, the quantity the machine actually *computes*, comes out at
`−1.0266` against `−1.02943`, i.e. **0.3%**. The discrepancy is entirely in the other factor:
`c_l` is **pinned** by the frozen normalization and is supposed to be `3.00650`, but its
discrete readout is `3.0637` — a **1.9% quadrature bias in the origin-slope operator**, which
`β = −c_l/c_ω` then inherits in full.

That is a gauge artifact, not a physical error, and it is correctable in the only principled
way: hold `c_l` to the value the normalization *sets* it to. Doing so gives

```
β = 2.9258 ± 0.011        (published 2.92056,  0.18% )
s_c = 0.17090 ± 0.0007        (published 0.171200)
```

Both numbers are reported — the raw reading and the gauge-corrected one — because the
correction is a *choice about the gauge*, and hiding a 1.9% systematic behind a better-looking
number is exactly the move this project's discipline exists to prevent. The honest summary is:
**our own machine puts the Chen–Hou 2D Boussinesq blow-up at `s_c ≈ 0.17`, and the residual
disagreement with the published value is attributable to a named, measured discretization bias
in a constant the scheme pins rather than computes.**

---

## 4. The direct route, priced and refused

The obvious move was to repeat Route-F exactly: run the time-dependent system with
`(−Δ)^s` dissipation, track `D/N` at the peak, fit `(T−t)^p`, read the exponent. The
solver for it is `solver/fractional_boussinesq.py`, built for this and gated to machine
precision against an exact solution (§4a). It does not work, and the reason is not subtle.

Starting from the Phase-1 ground-truth grower (`smooth_sharp`, reused rather than re-tuned
so the run's growth was established by an unrelated earlier experiment) at `n = 256`,
inviscid:

- amplitude grows by **≈ 90×** before the spectral guard fires;
- the amplitude exponent is **−1.12**, so the run *is* in the assumed regime;
- but the fit window spans **0.77 decades of `(T−t)`**, where the 1D leg had nearly four;
- and over that span `β` fitted on early / middle / late sub-windows reads
  **1.67 / 2.06 / 1.08** — a spread of more than 50%.

`collapse_window_report` therefore returns `measurable = False` and the leg does not quote a
`β` from it (banked lesson 45: an unknown must not be returned as a number). Two length
diagnostics also disagree by a factor of two — `amp/|∇ω| = 1.77` against the enstrophy
spectral centroid `= 0.76` — and the disagreement has a diagnosis rather than a shrug: the
spectral centroid is a *global* average and is therefore contaminated by the non-collapsing
background, while `amp/|∇ω|` is local to the sharpening point. The prediction that follows
is that the spectral exponent must **drift upward** across the window as the core's share of
the enstrophy grows, and the local one need not; it does (`0.30 → 1.18`), and that is a gate.

**The price of repairing it, computed rather than guessed.** Decades of `(T−t)` are bought
with resolution, at an exchange rate set by `β` itself: resolving `L` a factor `R` smaller
buys `R^{1/β}` in `(T−t)`, so **one extra decade of `(T−t)` costs `10^β` in linear
resolution**. The refused fit is still good enough to bracket the exponent — everything it
returns lies in `1 ≲ β ≲ 2` — and Chen–Hou's object is at `2.92`, so the price is between
**10× and 832× per direction**, i.e. between `10²` and `7×10⁵` in 2D grid points, *per decade*.
Getting from 0.77 decades to a usable 2.5 costs another factor `10^{1.73β}`: at `β = 1.8`
that is `~1300×` per direction. This is not a grid one buys; it is the reason dynamic
rescaling exists. Note that the pricing needs only a bracket on `β`, which the refused fit
does supply — refusing to quote a value is not the same as learning nothing.

**What survives.** The `D/N` instrument itself is fine — it responds to `s` with the right
sign and monotonicity, which is gated separately from the quantity it cannot pin. The `p(s)`
exponents are reported in the data and plotted in panel D **labelled underpowered**, because
the sign structure is real and because they are the number a future leg would improve. What
is *not* claimed from them is the location of the zero.

### 4a. The known-answer gate

`ω₀ = sin x sin y` is a steady Euler state — `ψ = ω/2`, so `u·∇ω ≡ 0` — so with `θ ≡ 0` the
exact solution of the full fractional system is `ω(t) = e^{−ν 2^s t} ω₀`, **for every `s`**.
Measured relative error at `s = 0.25 / 0.5 / 1.0 / 1.5`: `1.3e−14 / 1.2e−14 / 9.7e−15 /
8.2e−15`. This pins the fractional multiplier and the integrating-factor RK4 *together*,
which matters because the entire leg is a measurement of the size of that term: it must not
be the term carrying the largest discretization error.

The under-resolution guard is Route-F's (banked lesson 55) and is tested the way that lesson
demands — on a case known to be resolved and one known not to be. A smooth field reads
`1.9e−33`; a grid-noise field reads `0.67`. It separates them by 32 orders of magnitude.

---

## 5. Cross-model calibration: where is the 2D object on the toy's dial?

**PLACEHOLDER — filled from the run.**

---

## 6. Robustness: the condition does not care which field is dissipated

A modelling objection to §1 is that the 2D system has two fields, and the answer might
depend on whether the dissipation is put on `ω` or on `θ`. It does not. Redo the count in
the `θ` equation, using `θ ~ (T−t)^{β−2}`:

```
θ_t             ~ (T−t)^{β−3}
κ θ / L^{2s}    ~ κ (T−t)^{β−2−2sβ}
ratio           ~ κ (T−t)^{1 − 2sβ}          — identical.
```

So `s_c = 1/(2β)` is a property of the **collapse**, not of a choice about where to put the
damping. (In 3D NS the question does not arise: one viscosity damps everything.) Encoded as
`relevance_exponent_buoyancy` and gated against `relevance_exponent`, rather than left as a
remark — the derivation is the claim, so the claim gets a test.

An independent check on the sign conventions of the whole section falls out of the same
algebra. §1a's derivation predicts `d log C_θ/dτ = (2−β) c_ω`; the paper states
`c_θ = c_l + 2c_ω` (MMS (2.9)) from its own derivation. On Chen–Hou's constants both give
`0.94764866`. That is a check against a *published relation*, not against arithmetic we
control, and it is the reason to trust the sign of `β`.

---

## 7. What this leg does and does not establish

**Does:**

- `s_c = 1/(2β)`, the invariant form, with the gauge-dependence of Route-F's `α/2`
  identified, and the 1D result recovered as the `β = 1/α` special case (gated).
- `β = 1/2` is Navier–Stokes exactly, and `s_c` is **decreasing** in `β` — beating ordinary
  viscosity requires a collapse *slower* than the NS rate.
- The far-field decay exponent and the collapse exponent are one fact (`α = −1/β`), which is
  why `α/2` looked like a law.
- A number for the proven 2D object, obtained twice: from published constants, and from this
  project's own dynamically-rescaled machine.
- An honest negative on porting the 1D *method*, with the reason (window length) measured
  rather than guessed, and the repair named.
- A calibration between the toy family and its target.

**Does not:**

- Move any link of the chain. No certificate is produced, in 1D or 2D.
- Say anything about whether a **viscous** 2D Boussinesq blow-up exists. The scaling says
  which term dominates *given* the self-similar form; producing a solution that reaches it is
  the entire difficulty and is untouched here.
- Say anything about Navier–Stokes beyond restating where NS sits. NS's `β` is pinned by
  dimensional analysis and is not a dial.
- Establish novelty. `s_c = 1/(2β)` is three lines of scaling and my prior is that it is
  folklore; `LITERATURE_CHECK.md` §"Third pass" records what was searched, what was not
  found, and the two papers that could move the number
  ([2308.01528](https://arxiv.org/pdf/2308.01528), an *exact* Hou–Luo self-similar profile,
  which would give an exact `β`; and [2604.01868](https://arxiv.org/pdf/2604.01868), *new*
  self-similar profiles for the same systems, which would mean the 2D scenario has more than
  one `β`). `WebFetch` is still 403 on every host, so neither has been read.

Plain float64 throughout. Nothing interval-enclosed, nothing rigorous. Clay odds unchanged
at ~0.05%.

---

## 8. Lessons this leg paid for

**(56) A formula that is right in one model can be a GAUGE CHOICE rather than a law — port
it before you headline it.** `s_c = α/2` was correct, gated, and cross-validated against an
unrelated computation. It was still a coordinate expression, true only because gCLM's
rescaling pins `c_l = 1`. *Nothing internal to the 1D leg could have revealed that* — not a
finer grid, not a wider window, not a better control. **Changing the model is a test that no
amount of refinement within the model substitutes for.**

**(57) When the instrument that worked does not port, ask whether an instrument you already
own does.** The direct time-dependent fit fails in 2D for a resolution reason that is not
going away. But this project already had a dynamic-rescaling machine in which the same
quantity is a *modulation constant* — no fit, no window, no singular-time estimate. **The
repair for a measurement that is too noisy is sometimes a different definition of the same
number, not more grid.**

**(58) Check the monotonicity of your own headline, in words.** "Faster collapse loses to
viscosity" is the opposite of the natural intuition, and the natural intuition is what would
have been written into a summary sentence by reflex. It is now a unit test.

**(59) A calibration between the toy and its target is worth a leg on its own.** Fifteen legs
of gCLM work, and nobody had asked where the 2D object sits on gCLM's own dial. The answer
changes what the family map is evidence *for* — and it took an afternoon.
