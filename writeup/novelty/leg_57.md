# Leg 57 — Route-XS novelty pass (run BEFORE construction)

**Date:** 2026-08-05. **Agent:** LEG-D. **Branch:** `leg/xs-v1`.
**Verdict: `PROCEED_AS_BOOKKEEPING`.** See "What this pass actually settles" at the bottom —
the observation being classified is *folklore stated in print*, so this leg may not claim it as
a finding. What is not in print is the **classification as an executable ledger**, and that is a
bookkeeping artifact, not a result.

Per `writeup/novelty/README.md` and lesson from leg 53: **links, not counts.** Every query
string below is verbatim and every link returned that I judged on-topic is listed. Where a
search returned nothing on-topic I say so rather than reporting a number.

---

## The claim under test

> A certification method has a SHAPE, and the shape is a property of the operator: the standard
> radii-polynomial / Newton–Kantorovich tail estimate closes because the **unbounded part of the
> linearised operator is a multiplier** (diagonal in the spectral basis, so cutting an entry of
> size `Λ_M` leaves a tail inverse of size `1/Λ_M`, which decays). When the unbounded part is
> instead **off-diagonal (a shift)**, the bordered tail inverse is a **constant**, not `1/Λ_M`,
> and the estimate has nothing to decay with.

Two separable questions, and this pass keeps them separate because leg 51 lost a claim by not
doing so:

* **(N1)** Is the *observation* — that the standard tail estimate presumes an asymptotically
  diagonal / diagonally dominant Fréchet derivative — already in print?
* **(N2)** Is the *classification of the published CAP corpus by that shape*, as an executable
  predicate with located statements, already in print?

---

## Queries, verbatim, with the links returned

### Q1
`radii polynomial computer-assisted proof tail estimate unbounded part multiplier diagonal approximate inverse`

- https://arxiv.org/abs/2605.07500 — Shimizu–Morioka heteroclinic CAP case study
- https://www.sciencedirect.com/science/article/abs/pii/S1007570422000260 — CAPs for nonlinear diffusion problems
- https://www.researchgate.net/publication/274384127 — "Rigorous numerics for analytic solutions of DEs: the radii polynomial approach"
- https://arxiv.org/pdf/1704.03128 — polynomial interpolation / a priori bootstrap for CAPs in nonlinear ODEs
- https://link.springer.com/article/10.1007/s00332-016-9298-5 — (un)stable manifolds with validated error bounds
- https://arxiv.org/pdf/2404.08529 — 2D Gray–Scott localized stationary patterns
- https://arxiv.org/pdf/2604.08715 — 1D Thomas model localized patterns
- https://arxiv.org/pdf/2509.17099 — 1D activator–inhibitor localized patterns and saddle nodes

**On-topic for N1:** none states the shape hypothesis as a hypothesis; all four pattern papers
*use* a diagonal-tail construction without remarking on it. **On-topic for N2:** none.

### Q2
`computer-assisted proof off-diagonal unbounded operator tail block approximate inverse does not decay`

- https://www.researchgate.net/publication/388080912 — inverse-closedness of operator-valued matrices with polynomial off-diagonal decay
- https://arxiv.org/pdf/2507.21457 — Green's function estimates for long-range quasi-periodic operators on Z^d
- https://arxiv.org/pdf/2303.06243 — invertibility of matrix operators of infinite order with exponential off-diagonal decay
- https://link.springer.com/article/10.1007/s00365-010-9101-z — noncommutative approximation: inverse-closed subalgebras and off-diagonal decay
- http://www.cs.emory.edu/~benzi/Web_papers/bmt.pdf — sparse approximate inverse preconditioner
- https://arxiv.org/pdf/2604.22568 — truncations of hierarchical equations of motion

**Assessment.** This is the closest the search index gets, and it is a **different subject**.
The Jaffard / Baskakov inverse-closedness literature asks when an operator with off-diagonal
*decay* has an inverse with the same decay — it presumes decay away from the diagonal and
concludes decay. Our shift operator has no decay away from the diagonal to presume: its
unbounded entries **are** the off-diagonal ones. Not prior art; recorded so a later pass does
not have to rediscover that it is not.

### Q3
`survey classification computer-assisted proofs PDE which operators admit tail estimates asymptotic diagonal dominance requirement`

- https://link.springer.com/article/10.1007/s40324-019-00186-x — Gómez-Serrano, *Computer-assisted proofs in PDE: a survey*, SeMA (2019); preprint https://ui.adsabs.harvard.edu/abs/2018arXiv181000745G
- https://arxiv.org/pdf/2505.03091 — Cadiot, *Stability analysis for localized solutions in PDEs and nonlocal equations on R^m*
- https://arxiv.org/pdf/2403.10450 — planar Swift–Hohenberg non-radial localized patterns
- https://arxiv.org/pdf/2409.20457 — validated renormalization fixed points via Chebyshev series
- https://arxiv.org/pdf/2105.06895 — validated spectral stability via conjugate points
- https://arxiv.org/pdf/2101.01491 — shear-induced chaos CAP
- https://www.researchgate.net/publication/312890988 — CAPs for radially symmetric solutions of PDEs

**This is the hit for N1, and it settles N1 against us.** See below.

### Q4
`Cadiot Lessard Nave computer-assisted proof unbounded domain Fourier approximate inverse dominant part`

- https://arxiv.org/abs/2302.12877 and https://arxiv.org/pdf/2302.12877 — CLN, *Rigorous computation of solutions of semi-linear PDEs on unbounded domains via spectral methods*
- https://doi.org/10.1137/23M1607507 — the SIADS published version of the same
- https://arxiv.org/html/2403.10450 — planar Swift–Hohenberg
- https://arxiv.org/html/2502.20644 — rigorous integration of parabolic PDEs via Fourier–Chebyshev
- https://epubs.siam.org/doi/abs/10.1137/25M1798204 — proving symmetry of localized solutions, dihedral patterns

Confirms the primary source this leg must read at full text rather than abstract, and confirms
`solver/target_selection.py` is already citing the right paper for the Kawahara `r₀`.

### Q5
`computer-assisted proof self-similar blowup transport advection operator no diagonal dominance rigorous numerics difficulty`

- https://arxiv.org/pdf/2308.01528 — exact self-similar blowup of Hou–Luo with smooth profiles
- https://arxiv.org/html/2305.05895 — self-similar blowups of the generalized CLM model
- https://arxiv.org/pdf/2106.05422 — asymptotically self-similar blowup of the Hou–Luo model
- https://arxiv.org/pdf/2605.15149 — asymptotically self-similar blowup for 3D incompressible …
- https://www.researchgate.net/publication/387758591 — Chen–Hou Part II: Rigorous Numerics
- https://arxiv.org/pdf/2604.01868 — novel self-similar blowups, 1D Hou–Luo / 2D Boussinesq
- https://www.researchgate.net/publication/351671065 — stable self-similar blow-up for nonlocal transport equations

**The relevant negative.** These are exactly the papers that certify *transport* problems, i.e.
the place a counterexample to the dichotomy would live if one existed. None of them is described
as an `ℓ¹`-Fourier radii-polynomial certificate; the search surfaces no paper claiming a
radii-polynomial tail estimate for an off-diagonal unbounded part. **Whether that is because
none exists or because none says so in its abstract is exactly what the full-text pass of this
leg has to settle** — which is the whole point of the gate, and the reason leg 53's
abstract-only reading of BDL was withdrawn.

### Q6
`"diagonally dominant" tail computer-assisted proof failure advection term first-order derivative unbounded operator not dominant`

- https://arxiv.org/pdf/1703.01022 — Ohta–Kawasaki heteroclinic connections CAP
- https://arxiv.org/pdf/2409.20457 — validated renormalization fixed points
- https://arxiv.org/pdf/2101.01491 — shear-induced chaos CAP
- https://www.researchgate.net/publication/2706323 — diagonal dominance / positive definiteness of upwind approximations for advection–diffusion
- https://en.wikipedia.org/wiki/Diagonally_dominant_matrix, https://en.wikipedia.org/wiki/Computer-assisted_proof
- https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2026.89 — asymmetric diagonally dominant linear systems

**Nothing on-topic.** The one advection hit is about upwind *discretisation* matrices losing
diagonal dominance, which is a finite-difference stencil question, not a certificate-tail
question. Recorded so the resemblance does not get mistaken for prior art later.

---

## What this pass actually settles

**N1 — the observation is IN PRINT, and this leg must not claim it.** Cadiot,
arXiv:2505.03091, states both halves explicitly and in the same paper:

* §2 (construction of the periodic counterpart, around eq. for `F_q`): *"the operator `L`
  becomes an infinite diagonal matrix `L_q` with entries `l(n/2q)` on the diagonal."*
  That **is** the multiplier half of the dichotomy, written down as the reason the construction
  works.
* §3 (opening paragraph, "Spectrum of `DF(U₀)` using Gershgorin disks"): *"By construction `D`
  is supposed to be diagonally dominant, which hints to the Gershgorin theorem."*
  That is the dominance hypothesis, named as a hypothesis, by the author of CLN.

This is consistent with, and strictly sharpens, the standing ban recorded at leg 51/53: the
general observation is a re-derivation of published practice. **Route-XS therefore starts from
the position that it is classifying known practice, not discovering it.** The leg's prose must
say that, and its ledger entries must carry these two links.

**N2 — the classification is NOT in print, and it is not a result either.** No search returned
a paper that enumerates published radii-polynomial certificates and classifies each by the shape
of its unbounded part. But absence of a bookkeeping artifact is not novelty of a finding: what
this leg can honestly ship is an **executable ledger** that makes an existing folk fact
auditable and re-runnable (lesson 68), and an answer to the gate's actual question — *is there a
published counterexample?* — which no search can answer and only the full texts can.

**The flag this pass does NOT clear.** Leg 52's search-index flag (arXiv:2604.01868 not
resurfacing on topical queries) — Q5 above returned 2604.01868, but Q5 is a *different* query
from leg 52's, so this is **not** a clearance and I am not claiming one. Leg 53 was withdrawn
for exactly this move. The flag stands.

**What no search can do here, and what replaces it.** Every query above is search-level
evidence, which this project has ruled insufficient five times. The gate is answered from the
**full texts** of BDL arXiv:1503.06315, CLN arXiv:2302.12877, Chen–Hou arXiv:2210.07191 +
arXiv:2305.05660, and Dåhne–Figueras arXiv:2410.05480 — each classification traced to a located
statement, never to an abstract page.
