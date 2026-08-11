# TECHNICAL — P2 Route-TMS v1: validated integration and Taylor models, scoped

**Leg 315.** Branch `leg/315-tms-v1`. Runner `experiments/p2_route_tms_v1_scoping.py`
(runtime 1.9 s). Curated data `writeup/data/p2_route_tms_v1.json`. Figure
`fig79_route_tms_v1_reach.png`. Novelty pass `writeup/novelty/leg_315.md` (committed first).
Journal, with the integration notes, `experiments/journal/leg_315.md`.

> **SCOPING ONLY. NOTHING IS BUILT.** No solver module was written or edited. No ban was
> lifted, narrowed, or argued against. `requirements.txt` was not touched. **Naming a
> reachable object is not reaching it** — Walls 1 and 2 stand, no link of the L1→L4 chain
> moved, and Clay odds remain **~0.05%**, unchanged.

---

## 1. The gate, in its pre-committed and immutable wording

> **Does the scoping name at least one concrete object currently unreachable by the
> radii-polynomial/NK apparatus that Taylor-model arithmetic reaches, with the reaching
> mechanism stated and its build cost classed?**

**Answer: YES.** Two objects are named — `O1` and `O2` — each with a named reaching
mechanism and an evidence-backed cost class. A third, `O3`, is named as reached by
**neither**, so that the YES is not read as larger than it is.

---

## 2. What the thesis got right, and the part of it that is false

The dispatched thesis says `requirements.txt`'s "no adaptive ODE integrators are used" is a
**policy, not a finding**. That is confirmed: the line is a project decision, and it is
recorded nowhere as the output of a measurement.

But the naive form of the surrounding argument — *radii-polynomial/NK cannot reach
time-dependent objects, Taylor models can* — is **false**, and this document does not make
it. The novelty pass located **van den Berg, Breden & Sheombarsing, arXiv:2305.08221,
*Validated integration of semilinear parabolic PDEs*** (2023): rigorous **time** integration
by Fourier-space variation-of-constants, Chebyshev in time, domain decomposition, and a
**Newton–Kantorovich** argument, applied to Fisher, Swift–Hohenberg, Ohta–Kawasaki and
Kuramoto–Sivashinsky. NK does time. That result is carried in the reach matrix as control
`C2` precisely so the matrix can, and does, report against its own author's thesis.

So the reach argument must turn on something sharper. It does, and §4 states what.

---

## 3. The target, and the verifier's finding it rests on

The object is leg 251's Phase-1 candidate: **BCG** — Buckmaster, Cao-Labora,
Gómez-Serrano, *Smooth imploding solutions for 3D compressible fluids*, `arXiv:2208.09445`,
Forum of Mathematics Pi **13** (2025) e6 — at the diatomic value **γ = 7/5**.

The leg-251 verifier's finding, in `writeup/novelty/verify_251.md` §C, is the hinge:

> **At BCG's scaling there is no self-similar profile system of the dissipative equation.**
> […] the self-similar reduction — **the autonomous `(W, Z)` ODE system** that Thms 1.1/1.2
> solve — **is the Euler system**. […] Dissipation […] enters the **dynamically rescaled**
> system as a forcing term, `F_dis` […] **non-autonomous and exponentially decaying in
> self-similar time**: the bounds […] all carry an explicit `e^{−δ_dis s₀}` prefactor.
> […] The gap […] is in the **stability step**: the `r`-restriction that lets the profile
> *dominate* `F_dis`.

and its re-posing:

> **Before Phase 1 is authorized, obligation 1 should be re-posed** as: a rigorous enclosure
> of the *linear/nonlinear stability step with the dissipative forcing retained*, at a
> similarity exponent outside BCG's dominance regime.

**The gap is therefore NOT a profile enclosure.** Every object below is stated against that
re-posed obligation, not against the retracted one.

### 3a. The measured numbers, carried forward and not re-derived

Repo-internal, from leg 266, **corrected by leg 300** (`experiments/journal/leg_300.md:40-51`;
leg 266's `6.855` was a slipped digit) and propagated repo-wide by leg 319:

| quantity | value |
|---|---|
| dominance window, lower endpoint | `1.1666667` (= 7/6) |
| dominance window, upper endpoint | `1.1909830` |
| window width **certified** by BCG's dominance argument | `0.0243163` |
| window width **available** to the target | `0.1666667` (= 1/6) |
| shortfall ratio | `6.8541019662496845446` = `(7 + 3√5)/2` |

This leg re-derives none of these. It uses them only to say **where** the named object aims:
at `r` beyond `1.1909830`.

---

## 4. `O1` — the named object, and its named reaching mechanism

> **`O1`, the sonic-crossing `r`-tube.** A rigorous enclosure of BCG's autonomous `(W, Z)`
> self-similar **Euler** ODE flow **through the sonic point**, carried as a Taylor model
> polynomial in the similarity exponent `r` over an `r`-**interval** at γ = 7/5, whose output
> is the profile-vs-`F_dis` domination margin as a certified function of `r` extending across
> and beyond the dominance-window upper endpoint `r = 1.1909830`.

### 4a. Why the NK apparatus does not reach it — with the realization named (lesson 91)

"Measured dead" with no realization named is not an admissible negative. The negative here
holds in **three named realizations**, all of them this repository's own:

1. the **`ℓ¹_w` coefficient basis** — leg 54: best `Z₁` improvement `1.167×` where `>8×` was
   needed;
2. the **sup-norm collocation basis** — leg 56: `(H,D)` consistency defect over budget by
   `1.85e7×` (derivative) and `2.04e11×` (Hilbert);
3. **origin-`H²` capped at `a = 0`**, with no transfer to the real target — legs 163/176.

The structural reason, stated so it can be checked rather than believed: a radii-polynomial
certificate is a **zero-finder**. It requires a fixed function space, a numerical candidate,
and an approximate inverse of the linearization **in that space**. The `(W, Z)` trajectory
must pass through the **sonic point** — a degeneracy of the vector field — where a
**global-basis** linearization is not boundedly invertible. And this repository's standing,
re-posed ban forecloses proposing a **fourth** space/basis without its own scoping leg. So the
NK route here is closed by **this repository's own law**, not merely by difficulty.

This is lesson 87 in its own terms: *a certification method has a SHAPE, and the shape is a
property of the operator*. NK's shape is a **zero**; what is wanted is a **flow map**.

### 4b. The reaching mechanism, named in three parts

> **SONIC-POINT-DESINGULARIZED TAYLOR-MODEL STEPPING IN THE SIMILARITY PARAMETER.**

1. **The object is a finite-dimensional autonomous ODE** — the verifier's own words, "the
   autonomous `(W, Z)` ODE system that Thms 1.1/1.2 solve". A validated IVP integrator
   encloses the **flow map**, and therefore **requires no function space at all**. That is
   the first load-bearing half of the reach.
2. **The sonic degeneracy is crossed** by quasi-homogeneous desingularization plus local
   analytic continuation. This technique is **already recorded in this repository**, at
   `writeup/data/p2_route_w2l_v1_lit.json:180`, verbatim: *"quasi-homogeneous compactification
   plus rigorous integration in interval arithmetic"*. That is the second load-bearing half.
3. **Wrapping control** by Lohner-QR, mean-value form and shrink-wrapping (Berz–Makino).
   Without it, naive interval stepping cannot cross an interval of useful length. **This is
   the part that is Taylor-model arithmetic proper rather than merely interval arithmetic, and
   it is exactly what `solver/interval.py` cannot supply.**

Carrying `r` as a symbolic Taylor variable then certifies an `r`-**interval** in one
integration rather than one `r` per run.

### 4c. One claim explicitly NOT made

The parameter-interval property in 4b is a **convenience, not a load-bearing distinction**.
Radii-polynomial certificates are routinely run with interval parameters for branch
continuation, so "Taylor models sweep `r` and NK does not" would be **false**, and is not
claimed. The reach rests on 4b(1) and 4b(2) only.

---

## 5. Cost classing — what each estimate rests on

The useful part of this leg is the distinction between *an existing library*, *a hand-roll of
the kind leg 256 was forced into*, and *a genuine research problem*.

### 5a. `O1`: **class C** — a genuine research problem, with a class-B implementable core

**Not class A.** No maintained, pip-installable, **Python** Taylor-model ODE integrator was
located. `python-flint` **0.9.0** (PyPI, released **2026-07-03**, SPDX
`MIT AND LGPL-3.0-or-later`, FLINT/Arb themselves LGPL v2.1+, requires only Python ≥ 3.10,
**does not require scipy**) supplies `arb`/`acb` rigorous balls and `arb_series` — but **no
Taylor-model IVP integrator**. The field's implementations are out-of-language: CAPD (C++,
`arXiv:2010.07097`), VNODE-LP (C++, unmaintained), Flow\* (C++), COSY Infinity (restricted
licence), TaylorModels.jl (Julia). TERA (`arXiv:2607.01189`, 2026) *is* Python, but is
control-systems reachability, brand-new, and unvalidated for a fluid profile.

**The class-B core.** A Taylor-model type over `solver/interval.py`'s existing outward-rounded
`Interval`, plus a Lohner-QR wrapping layer, is a hand-roll of exactly the kind leg 256 was
forced into. Leg 256's own words (`experiments/journal/leg_256.md:69-77`): *"with no scipy
there is no Gauss–Laguerre rule to call, so nodes come from Sturm bisection on the Jacobi
matrix […] followed by Newton on the scaled recurrence."* That was **one leg for a static
quadrature rule**; a validated IVP integrator with wrapping control is strictly larger — so
**≥ 1 leg and plausibly several**.

**Why C and not B — the research obstacle is not the integrator.** `O1` is only the first
rung. The verifier's re-posed obligation is the **stability step with `F_dis` retained** over
`s ∈ [s₀, ∞)`: a **non-autonomous PDE trapping argument**, not an ODE. The standard bridge
from a validated ODE integrator to a validated PDE enclosure is Zgliczyński's
**self-consistent a-priori bounds** (`math/0005247`, Zgliczyński–Mischaikow, 2000), whose
hypotheses are **dissipative/parabolic**. BCG's rescaled system is **quasilinear hyperbolic**,
with dissipation entering as an exponentially decaying **forcing** (`e^{−δ_dis s₀}`) rather
than as a smoothing principal part. **That mismatch is the research problem, and naming it is
this leg's most useful output.**

### 5b. `O2`: **class A / B split**

> **`O2`.** Rigorous enclosure of the degree-**4503** Gauss–Laguerre nodes and weights, and of
> the resulting quadrature, that leg 256 had to hand-roll in float64 — i.e. closing leg 256's
> own recorded ceiling.

`capabilities.py:496-498` records that ceiling verbatim: *"CEILING: float64, NOT interval
arithmetic — this reproduces their CONSTANTS, not their proof."* Breden–Chu prove their
Theorem 42 in interval arithmetic over **16384-bit** BigFloat; leg 256 could not, and said so.

**Reaching mechanism**: arbitrary-precision **ball arithmetic** with rigorous special-function
and root enclosures. This is the **validated-integration half of the route name, not the
Taylor-model half**, and is labelled as such rather than smuggled in. Arb's exponent range
makes leg 256's `e^{−1.8e4} × 1e1220` product representable **directly**, removing the
per-node log-renormalization scaffolding leg 256 was forced to build.

**Class A** for the arithmetic substrate, with licence and version pinned as above — and note
it does not even engage the "no adaptive ODE integrators" policy line, which is about scipy
and about ODE integration, neither of which this is. **Class B** for the quadrature layer:
it is **not confirmed** that rigorous quadrature (`acb_calc_integrate`) is exposed through the
Python bindings — the API page reached documents v0.3.0 and lists no `.integral()` method.
That is recorded as **under-evidenced**, not assumed either way.

**Territory**: leg 312 (Route-APIA) already owns the arbitrary-precision interval build
(`solver/interval_mp.py`). `O2` is a **consumer** of APIA, not a new build leg.

### 5c. `O3`: reached by neither, and deliberately not costed

> **`O3`.** Forward invariance (a trapping region) for the dynamically rescaled
> compressible-NS perturbation system with `F_dis` **retained**, over the **semi-infinite**
> self-similar time interval `s ∈ [s₀, ∞)`, at `r` outside the dominance window.

This is the verifier's re-posed obligation **in full**, and **no mechanism is claimed for it**.
Costing an object that neither apparatus reaches would be vibes, which the spec forbids.
Whether any computer-assisted work has ever enclosed a non-autonomous forcing-domination /
trap-region argument of this **shape**, in any field, is the explicit territory of **leg 267
(Route-FDL)**. This leg does **not** pre-empt or predict FDL's answer, and does **not** claim
the precedent is absent.

---

## 6. The reach matrix, and why it is not a tautology (lesson 90)

A matrix whose every row said "Taylor models win" would be a restatement of the author's
intent. So the matrix carries **two controls that come out the other way**, and the runner
**asserts it in code** — `_check_matrix_is_not_a_tautology` fails the run if no row is NK-only,
or if no row is "neither". It is wired to the same field the headline reads, so it cannot pass
vacuously.

| row | NK reaches? | TM reaches? |
|---|---|---|
| `O1` sonic-crossing `r`-tube | no (3 named realizations) | **yes** |
| `O2` rigorous degree-4503 Gauss–Laguerre enclosure | no (out of category) | **yes** |
| `O3` semi-infinite trapping with `F_dis` retained | no | **no** |
| `C1` **control** — stationary zero of `F(u)=0` with an approximate inverse | **yes** | no |
| `C2` **control** — validated parabolic time-integration, `arXiv:2305.08221` | **yes** | no |

`C1` is this repository's own bordered certificate machinery
(`capabilities.py:238-243, :333-337, :359-360`) — Taylor models have no notion of an
infinite-dimensional zero-finding problem and **lose that row**. `C2` is scored off an
**external** paper that directly contradicts the naive form of this leg's thesis, so it could
not have come out the author's way by construction.

---

## 7. Instrument controls, including one instrument found broken

**The arXiv search UI returns zero for ANY query containing two quoted phrases ANDed.**
`"Taylor models"` alone returns **84** results; `"validated integration"` alone returns **20**;
every two-phrase conjunction returns **0**. Six all-zero queries were therefore treated as a
**broken instrument and discarded, not banked**. `pypi.org/search` was likewise blocked by a
"Client Challenge" page and discarded; individual project pages load and were used instead.

Three controls passed: the positive control (`arXiv:2505.03091`, Cadiot, fetched and matching
the in-repo record), the negative control (a fabricated arXiv path returning HTTP 404), and a
**spelling-variant** control — `"Navier--Stokes"` with the LaTeX double hyphen returned exactly
this repository's own recorded negative-control citation, `arXiv:2604.09949`. Full log and
eleven banked links in `writeup/novelty/leg_315.md`.

---

## 8. `capabilities.py`, grepped as the standing ban requires

Terms `Taylor model`, `validated integration`, `rigorous integration`, `interval ODE`, `CAPD`,
`Lohner`, `COSY`, `VNODE`, `flow map`, `wrapping`: **one hit**, `capabilities.py:98`
("exact-Taylor inner integrals" inside Xu's resolvent — an exact Taylor **expansion**,
unrelated to Taylor-**model** arithmetic). Every other term returns **zero**. What is
registered nearby is `solver/interval.py`, *"rigorous interval arithmetic … hand-rolled
outward-rounded intervals; no scipy, no mpmath"* — **scalar arithmetic, no integrator**. The
absence is corroborated verbatim in-repo by leg 285's spec,
`experiments/p2_route_p2s_v1_spec.py:493`: `existing="solver/interval.py supplies the
arithmetic but no validated integrator"`.

---

## 9. What this leg does not do

It does not build. It does not edit `requirements.txt` — the policy observation is routed as
an **integration note** in `experiments/journal/leg_315.md`, per the spec's own instruction,
and it is worth stating that on this leg's evidence **the policy is not the binding
constraint**: the tooling that would matter (`python-flint`/Arb) is not scipy, and the
Taylor-model IVP integrators are not Python at all. It lifts no ban; the one adjacent ban —
the re-posed radii-polynomial ban — is recorded as **disjoint in subject matter** (a
Taylor-model flow enclosure proposes **no** function space, so it is not the "fourth
space/basis" the lift clause contemplates) and that reading is **routed to the user, not
decided here**.

**No link of the L1→L4 chain moved. Clay odds remain ~0.05%.**
