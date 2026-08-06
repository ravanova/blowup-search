# Leg 91 — Route-FGA novelty pass (run BEFORE construction)

**Date:** 2026-08-05/06. **Agent:** LEG-G. **Branch:** `leg/fga-v1`.

**Verdict: `PROCEED_AS_AUDIT`.** This leg builds no new mathematics and claims no novel
mechanism. It is an adversarial robustness audit of `solver/fractional_gclm.py`'s
critical-exponent path under malformed dissipation inputs. Everything it can find is either
(a) a defect in *our* code, or (b) a confirmation of a documented numerical hazard. Neither is
a discovery, and nothing below is claimed as one.

**It does not reopen, contest, re-measure, or re-derive the `s_c = alpha/2` finding.** That
result is validated against XU eq (6.3) row by row and is marked PRE-EMPTED under Route-J; it is
settled physics and this leg treats it as fixed background. The distinction this leg holds to,
stated once and then obeyed throughout: *the physics claim `s_c = alpha/2` is settled; what has
never been checked is whether the code that computes and measures `s_c` refuses malformed input.*
Every number this leg reports is a statement about **code behaviour under invalid input**, never
about the value of `s_c` for any physically admissible `s`. No adversarial run's output is ever
quoted as a physics measurement.

Per `writeup/novelty/README.md`: **links, not counts.** Query strings verbatim; every on-topic
link listed.

---

## What is being checked for prior art

* **(N1)** Is there a *published admissible range* for the dissipation exponent in the dissipative
  gCLM family — i.e. does the literature itself pin down what "invalid `s`" means, so the battery
  tests against a documented boundary rather than an invented one?
* **(N2)** What is `(-Delta)^s` for **`s < 0`** mathematically? If it is a well-defined operator,
  negative `s` is merely off-topic input; if it is *ill-defined*, then a code that accepts it
  silently is masking a real singularity, and the audit has a sharper target.
* **(N3)** Is "adversarial battery against a numerical module, checking that invalid input is
  propagated or flagged rather than silently absorbed" an established *method*?
* **(N4)** Is silent absorption of an invalid parameter — as opposed to NaN propagation — a
  documented failure mode with a name?

---

## Queries, verbatim, with the links returned

### Q1
`dissipative Constantin-Lax-Majda generalized CLM fractional dissipation admissible exponent range critical exponent alpha/2`

- https://arxiv.org/pdf/1908.09385 — Lushnikov–Silantyev–Siegel (and successors), *Singularity
  Formation and Global Well-Posedness for the Generalized Constantin–Lax–Majda Equation with
  Dissipation*.
- https://arxiv.org/abs/2207.07548 and https://arxiv.org/pdf/2207.07548 — *Global existence and
  singularity formation for the gCLM equation with dissipation: the real line vs. periodic
  domains*.
- https://arxiv.org/pdf/2411.01891 — *Exact periodic solutions of the generalized
  Constantin–Lax–Majda equation*.
- https://arxiv.org/html/2607.19762v1 — Xu, *The spectral picture of self-similar collapse in the
  Constantin–Lax–Majda equation* — the same XU the `s_c` row-by-row validation is against.
- https://arxiv.org/pdf/2506.02800 — *Stability and Instability on the De Gregorio Modification*.
- https://www.researchgate.net/publication/326959516_Unimodal_solutions_of_the_generalized_Constantin-Lax-Majda_equation_with_viscosity

**On-topic finding for (N1), and it fixes the battery's boundary.** The literature parametrises
the dissipation as `-Lambda^sigma` with `Lambda^sigma-hat = |k|^sigma`, i.e. **`sigma = 2s` in
this module's variables**. The studied range is `sigma >= 0` throughout: global-in-time existence
on the circle is proved *"for `sigma >= 1` for all real values of the advection parameter `a`"*
for small data, and the **lowest** exponent anyone treats is `sigma = 0`, described as the
*"marginal"* dissipation and given a physical reading (stress evolution in an Oldroyd-B fluid).
So the published admissible floor is `sigma = 0`, i.e. **`s = 0`**, and **`s < 0` is outside every
range the dissipative-CLM literature considers.** That is the boundary the battery tests against;
it is read off the literature, not invented here. The literature imposes no *upper* bound on
`sigma`, so the only upper wall is the code's own float64 wall on `|k|^{2s}` — which this leg
therefore measures rather than assumes.

### Q2
`"(-\Delta)^s" negative s Riesz potential smoothing operator not fractional Laplacian admissible range s in (0,1)`

- https://www.ams.org/journals/proc/1998-126-08/S0002-9939-98-04325-1/S0002-9939-98-04325-1.pdf —
  *Spectral properties of the operator of Riesz potential type*.
- http://ssamko.com/dpapers/files/New_Approach_FCAA.pdf — Samko, *A new approach to the inversion
  of the Riesz potential*.
- https://projecteuclid.org/journals/communications-in-mathematical-analysis/volume-14/issue-1/Optimal-Regularity-Properties-of-the-Riesz-Potential-Operator/cma/1364216234.full
- https://arxiv.org/pdf/0907.3321 — *Riesz's and Bessel's Operators in Bilateral Grand Lebesgue
  Spaces*.
- https://arxiv.org/pdf/2012.08841 — *Lower bound of Schrödinger operators on Riemannian
  manifolds* (carries the `I_s = Delta^{-s/2}, s > 0` convention).
- https://arxiv.org/pdf/1811.06399, https://arxiv.org/pdf/2511.13461, https://arxiv.org/pdf/2105.04926,
  https://cvgmt.sns.it/media/doc/paper/2447/gI_1.cvgmt.pdf — adjacent Riesz-potential regularity
  results, none on the negative-exponent-as-input question.

**On-topic finding for (N2), and it is the sharpest result of this pass.** For a negative
exponent the multiplier `|xi|^sigma` is not a benign object: *"since `|xi|^sigma` has a
singularity at `xi = 0` when `sigma < 0`, the Riesz potential operator is not well defined on
Schwartz space when the parameter is negative, and `|xi|^sigma` is not a tempered distribution
for `sigma <= -d`."* The obstruction to `sigma < 0` is **exactly the `k = 0` mode**. That is
directly relevant to what the module does: `solver/fractional_gclm.py` builds
`visc = |k|^{2s}` and then, on the **very next line**, executes `visc[0] = 0.0` with the comment
*"the mean is not dissipated"*. For `s > 0` that line is a harmless no-op-in-spirit (`0^{2s} = 0`
already). For `s < 0` it is the line that **overwrites the `inf` which is the mathematical
signal that the operator is ill-defined**. The audit therefore has a precise, literature-anchored
target: does the singularity-masking at `k = 0` let an ill-defined negative-exponent operator run
to completion and emit a finite, plausible-looking number? This is a hypothesis about *our* code
that the published Riesz theory makes worth testing — not a new result about Riesz potentials.

### Q3
`fractional Laplacian negative exponent input validation spectral solver silent unphysical operator numerical software defect`

- https://www.sciencedirect.com/science/article/abs/pii/S0010465520303416 — open-source parallel
  spectral fractional Laplacian code (3D complex geometry).
- https://arxiv.org/pdf/1812.08325 — *Spectral Method for the Fractional Laplacian in 2D and 3D*.
- https://www.math.purdue.edu/~shen7/pub/CheS20b.pdf — Chen–Shen, efficient spectral method.
- https://arxiv.org/pdf/2010.06509, https://arxiv.org/pdf/2409.17388, https://arxiv.org/pdf/1911.11906,
  https://arxiv.org/html/2311.07814, https://arxiv.org/pdf/1709.01639, https://arxiv.org/pdf/1708.03912,
  https://arxiv.org/pdf/1311.7691, https://par.nsf.gov/servlets/purl/10171470 — the spectral /
  FEM / finite-difference fractional-Laplacian solver corpus.
- https://onlinelibrary.wiley.com/doi/10.1155/2023/9014456 and https://www.hindawi.com/journals/jfs/2023/9014456/
  — *Critical Fractional p-Laplacian System with Negative Exponents* (negative exponent in the
  **nonlinearity**, not in the operator — not the same object).
- https://arxiv.org/html/2509.24454 — nonexistence in the supercritical / negative-exponent case.
- https://en.wikipedia.org/wiki/Improper_input_validation — CWE-20 framing.

**On-topic finding.** The fractional-Laplacian solver corpus is large and none of it documents an
input-validation defect of this shape; no published solver paper reports "we accepted `s < 0` and
returned a plausible number". The absence is expected — such papers report methods, not their
own defects — and is recorded so that **no claim of novelty attaches to finding one here**. The
one paper with "negative exponents" in the title puts them in the *nonlinearity*, a different
object. Nothing found pre-empts or duplicates this leg, and nothing found makes it a discovery:
whatever it finds is a bug in this repository's own file.

### Q4
`scientific computing silent failure invalid parameter propagation NaN plausible result numerical library robustness audit`

- https://arxiv.org/abs/2110.15804 — *Doubt and Redundancy Kill Soft Errors — Towards Detection and
  Correction of Silent Data Corruption in Task-based Numerical Software*.
- https://arxiv.org/abs/1312.2674 and https://arxiv.org/pdf/1312.2674 — *Silent error detection in
  numerical time-stepping schemes*.
- https://arxiv.org/abs/2203.08989 — *Detecting silent data corruptions in the wild*.
- https://arxiv.org/pdf/2507.23186 — *NaN-Propagation: A Novel Method for Sparsity Detection in
  Black-Box Computational Functions*.
- https://www.cs.purdue.edu/homes/lintan/publications/grist-icse21.pdf — Yan et al., *Exposing
  Numerical Bugs in Deep Learning via Gradient Back-Propagation* (ICSE'21).
- https://arxiv.org/html/2605.30353 — *Physics Is All You Need? A Case Study in
  Physicist-Supervised AI Development of Scientific Software*.
- https://en.wikipedia.org/wiki/Robustness_(computer_science)
- https://semiengineering.com/why-silent-data-errors-are-so-hard-to-find/,
  https://www.rustcodeweb.com/2025/04/numpy-managing-warnings-and-errors.html — background.

**On-topic finding for (N3) and (N4), and it supplies the leg's vocabulary.** The method is
established: *"silent errors are errors in application state that have escaped low-level error
detection"*, and the recommended discipline is exactly this leg's gate — *"ignoring warnings may
lead to silent propagation of invalid results (e.g. inf, nan)"*, so a module must either
propagate the invalid value or refuse. The NaN-Propagation paper names the precise failure mode
the gate's yes-branch describes: *"a more serious false-negative failure mode can occur if the
program actively overwrites NaN outputs without raising an error"* — the paper adds that this
overwriting *"is quite rare in engineering analysis code today"*, which is what makes it worth
testing for rather than assuming. Two further items shape the battery: the same corpus warns
that *"overly aggressive propagation of NaN values"* is itself a false-positive mode, so the
battery must record **which** invalid inputs propagate correctly (a pass) and not only which do
not; and the physicist-supervised-software case study independently reaches this leg's design
rule — *"testing at diverse parameter points beyond calibration ... and an explicit rule against
unphysical numerical patches proved critical for catching what standard oracle tests missed"* —
which is precisely the gap here, since `test_fractional_gclm.py`'s six gates test only
physically admissible `s`.

---

## What this pass changed about the leg, before construction

1. **It set the invalid-input boundary from the literature, not by invention** (N1): the
   dissipative-gCLM corpus works at `sigma = 2s >= 0`, floor `sigma = 0`. So `s < 0` is the
   literature-backed "invalid" case, and there is **no published upper bound** — meaning the upper
   wall must be *measured* as a property of the code (the float64 overflow of `|k|^{2s}`), not
   asserted as physics. The battery is split accordingly.
2. **It gave the battery an exact target line** (N2): `visc[0] = 0.0`, one line after
   `visc = |k|^{2s}`. Published Riesz theory says `k = 0` is precisely where a negative exponent
   is ill-defined, so that line is the candidate masking step. The battery instruments it
   directly, including the monotonicity of `visc` in `|k|` — the substantive corruption, which
   emits no warning at all.
3. **It required the battery to record passes as loudly as failures** (N4): inputs that correctly
   propagate NaN are part of the result, so the report is a *map* of the module's behaviour, not
   a bug list.
4. **It pre-empts every novelty claim.** Nothing this leg can find is new mathematics. A defect
   would be a defect in our code against a boundary already in print; a clean result is a
   confirmation of robustness. The leg claims **no** novelty, and it makes **no** statement about
   the value of `s_c`, which remains PRE-EMPTED and settled.
