# Leg 63 — Route-M2 novelty pass (run BEFORE construction)

**Date:** 2026-08-05. **Agent:** LEG-C. **Branch:** `leg/m2-v1`.
**Verdict: `PROCEED_AS_SCOPING`.** The screen itself is bookkeeping and is not claimed (leg 57
already settled that the multiplier/shift dichotomy is folklore in print). What this pass had to
settle is a *factual* question the gate turns on, not a novelty question about our own method:
**is there a model with PROVED finite-time blow-up whose dissipation is strong enough to put the
linearization's unbounded part on the multiplier side?** The answer located below is **yes**, and
it changes the leg's expected outcome from "confirm exhaustion" to "escalate".

Per `writeup/novelty/README.md` and the ban banked from leg 53: **links, not counts.** Every query
string is verbatim; every returned link I judged on-topic is listed; where nothing on-topic came
back I say so instead of quoting a number. Everything below the fold is **TRANSCRIBED** from
abstracts and search summaries, not verified from full text, *except* the two items marked
FULL-TEXT/ABSTRACT-VERBATIM.

---

## The three questions

* **(N1)** Is *screening candidate CAP targets by the shape of the linearization's unbounded part*
  (multiplier vs shift) already in print as a selection criterion?
* **(N2)** Which models have **proved** finite-time blow-up **with dissipation**, and at what
  dissipation exponent? This is the question that decides the gate, because the exponent is
  exactly the coordinate the predicate is measured against.
* **(N3)** Has anyone already produced a **computer-assisted certificate** for a self-similar
  profile of a *dissipative* 1D transport model? If yes, the candidate is certified and drops out.

---

## Queries, verbatim, with the links returned

### Q1
`finite time blow-up proof one dimensional model Hilbert transform fractional dissipation exponent alpha Cordoba Cordoba Fontelos`

- https://arxiv.org/pdf/1009.0540 — Kiselev, *Regularity and blow up for active scalars*
- https://doi.org/10.1137/100794924 — Li–Rodrigo, *On a one-dimensional nonlocal flux with fractional dissipation*, SIAM J. Math. Anal.
- https://arxiv.org/pdf/1508.00550 — *One-dimensional model equations for hyperbolic fluid flow* (survey)
- https://arxiv.org/pdf/1408.1056 — *On a transport equation with nonlocal drift*
- https://arxiv.org/pdf/2405.16364 — multi-dimensional transport equation with nonlocal velocity and fractional dissipation
- https://arxiv.org/pdf/2205.15310 — blow-up of a non-local transport equation on compact manifolds
- https://arxiv.org/pdf/2403.06449 — blowup for a nonlocal multi-dimensional transport equation
- https://arxiv.org/pdf/2511.04660 — finite-time blow-up for a multi-dimensional model

**On-topic for N2, and this is the CCF line.** Dissipative CCF `θ_t = (Hθ)θ_x − Λ^{2α}θ` has
proved blow-up only for **small** exponents (the located range in these summaries is `α < 1/4`,
extended in parts of the literature toward `1/2`). Recorded because it is the *negative* half of
the answer: the most-cited dissipative blow-up proof sits far on the **shift** side.

### Q2
`proven finite time singularity fluid model with fractional dissipation exponent greater than one supercritical blow-up open problem`

- https://www.emergentmind.com/open-problems/ccf-fractional-dissipation-singularity-formation-12-to-1 — states the CCF range `α ∈ [1/2, 1]` as a **longstanding open problem**
- https://arxiv.org/pdf/1009.0540 — Kiselev survey, same
- https://arxiv.org/pdf/2104.10759 — fractional Burgers: blow-up for `0 < α < 1/2`, global for `α ≥ 1/2`
- https://link.springer.com/article/10.1007/s00220-008-0669-0 — aggregation equation with fractional dissipation
- https://www.researchgate.net/publication/251288116 — generalized SQG finite-time singularities

**Assessment.** For the *nonlocal-flux* family (CCF, fractional Burgers), the proved-blow-up
ceiling is `1/2` and the region above it is explicitly open. If the ledger contained only that
family, the gate would answer NO on an exponent gap of a factor ≈ 2 — which is the outcome the
leg was dispatched expecting.

### Q3
`De Gregorio Constantin-Lax-Majda fractional dissipation global regularity threshold alpha 1/2 blow up proof`

- **https://arxiv.org/abs/1908.09385** — Chen, *Singularity formation and global well-posedness for
  the generalized Constantin–Lax–Majda equation with dissipation* — **the decisive hit, see below**
- https://arxiv.org/pdf/2506.02800 — stability/instability of the De Gregorio modification
- https://arxiv.org/pdf/2305.05895 — self-similar blowups with smooth profiles of gCLM (inviscid)
- https://arxiv.org/pdf/2411.01891 — exact periodic solutions of gCLM
- https://www.researchgate.net/publication/326959516 — *Unimodal solutions of the gCLM equation
  with viscosity* (Lushnikov–Silantyev–Siegel) — **numerical**, viscous, no certificate
- https://intlpress.com/site/pub/files/_fulltext/journals/cms/2011/0009/0003/CMS-2011-0009-0003-a012.pdf — gCLM, earlier

### Q4 (N3)
`interval arithmetic computer-assisted proof viscous self-similar blowup profile generalized Constantin-Lax-Majda dissipation Lambda^2 certified`

- https://arxiv.org/html/2607.19762 — spectral picture of self-similar collapse in CLM
- https://arxiv.org/html/2603.25104 — gCLM singular profiles, theoretical + numerical (already in the ledger, inviscid)
- https://arxiv.org/pdf/2308.01528 — exact self-similar blowup of Hou–Luo with smooth profiles (inviscid, analytic)
- https://arxiv.org/pdf/2605.15149 — asymptotically self-similar blowup for 3D Euler, `C^{1,1/3−}` (inviscid)
- https://arxiv.org/abs/1908.09385 — as above

**On-topic for N3: nothing.** Every located computer-assisted certificate in this family
(Chen–Hou–Huang for inviscid De Gregorio/gCLM; Chen–Hou for 2D Boussinesq) is **inviscid**. No
interval-arithmetic certificate of a *dissipative* self-similar profile was located. The
dissipative blow-up proofs that exist are **analytic**, not computer-assisted. That is the gap
this leg's ledger is pointing at, and it is the reason the candidate below counts as uncertified.

### Q5 (N1)
`choosing targets for computer-assisted proofs criterion diagonal dominance linearization spectral basis which problems are amenable`

- https://epubs.siam.org/doi/10.1137/23M1607507 — rigorous computation for semilinear PDEs on unbounded domains via spectral methods
- https://arxiv.org/pdf/2403.18718 — Whitham solitary waves, constructive proofs
- https://arxiv.org/pdf/2509.17099 — 1D activator–inhibitor localized patterns
- https://arxiv.org/pdf/1601.00307 — Fourier–Taylor parameterization of unstable manifolds
- https://arxiv.org/pdf/2507.09021 — pseudospectral rigorous estimation of transfer-operator resonances
- https://dl.acm.org/doi/10.1007/s10444-014-9349-0 — eigenvalue localization via diagonal dominance
- https://arxiv.org/pdf/1908.09598 — geometric features of spectra of linear operators

**On-topic for N1: none as a selection criterion.** The corpus *uses* "a finite matrix plus a
diagonal tail which can be controlled theoretically" as standard practice, and one summary notes
"there are approaches when the tail is not diagonally dominant" — i.e. the property is treated as
a construction detail, never as a stated screen for choosing what to attempt. Combined with leg
57's located Cadiot statements (arXiv:2505.03091 §2 and §3), the position is unchanged from leg
57: **the dichotomy is folklore, so this leg claims no novelty for the screen.** Using it as a
target-selection column is bookkeeping.

---

## The one item read at ABSTRACT-VERBATIM depth, because the gate turns on it

**Chen, arXiv:1908.09385**, abstract, fetched and quoted verbatim (truncated as returned):

> "We study a generalization due to De Gregorio and Wunsch of the Constantin-Lax-Majda equation
> (gCLM) on the real line ... We use the method in [chen2019finite] to prove finite time
> self-similar blowup for `a` close to `1/2` and `γ = 2`"

with `Λ^γ = (−∂_xx)^{γ/2}` the dissipation. Three things follow, and each is load-bearing:

1. **`γ = 2` is the full Laplacian.** In the spectral basis the unbounded part of the linearization
   is then `−ν k²` on the **diagonal**, against a transport off-diagonal of size `~ k/2`. That is
   the multiplier side of the predicate by a whole power of `k`, not marginally.
2. **The blow-up is PROVED, and proved analytically** (nonlinear stability of an approximate
   self-similar profile), not computer-assisted. So the model satisfies the prize's wording
   ("a model where blow-up is provable") while the *profile* remains uncertified in the
   interval-arithmetic sense this repository means by `certified`.
3. **The proof is local in `a`** ("close to `1/2`"). Everything off that neighbourhood — including
   the viscous unimodal profiles of Lushnikov–Silantyev–Siegel — is numerical. That is where an
   uncertified target on a blow-up-provable model actually lives.

**Not verified from full text.** The `a`-neighbourhood is not quantified in the abstract, the
`ν`-dependence is not stated there, and the global-well-posedness side (`a ≤ −1`, critical and
supercritical dissipation) is transcribed from the same abstract. A promotion decision must read
the PDF; a **scoping ledger row** may carry it with this provenance and the caveat attached, and
that is exactly what this leg builds. Flagged as the first thing a promotion leg must discharge.

---

## What this pass settles

* **N1 — no claim.** The screen is folklore-adjacent bookkeeping; leg 57's ban stands and this leg
  inherits it. Nothing in the writeups may present the multiplier/shift screen as a finding.
* **N2 — the gate's factual premise holds.** There is at least one model with **proved** finite-time
  blow-up whose dissipation exponent (`γ = 2`) is unambiguously multiplier-shaped. The CCF /
  fractional-Burgers line, by contrast, tops out at `1/2` with `[1/2, 1]` open — so the answer is
  **family-dependent**, which means the ledger must carry the exponent per row and not a global verdict.
* **N3 — the candidate is uncertified.** No computer-assisted certificate of a dissipative
  self-similar profile was located in this family.

**Consequence for the leg, recorded before construction:** the gate is likely to answer **YES**,
which is escalation #1 — ranked ledger, predicate column, evidence, **promote nothing**, push the
branch only. And the honest constraint travels with it: the candidate is dissipative, so stage V's
ban governs whether it may ever be promoted, and that ban's lift condition names `L1`, which is
measured dead. Surfacing that as a user call is this leg's job; making the call is not.
