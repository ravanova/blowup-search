# Phase 2 — Numerics Upgrade: method recommendation & spike plan

**Status:** RECOMMENDATION, awaiting sign-off. No solver code written yet.
**Date:** 2026-07-24.
**Context:** Phase 1 (the uniform-grid fitness search) concluded with a decisive,
honestly-documented negative — see
[writeup/2_phase1_2d/NEGATIVE_RESULT_TWO_CURRENCIES.md](writeup/2_phase1_2d/NEGATIVE_RESULT_TWO_CURRENCIES.md).
Root cause: on a uniform grid the genuine singular structure forms **below grid
scale**, so no scalar fitness read off the trusted window can isolate it. The agreed
next move is the numerics upgrade that resolves the singular region. This doc is the
"research first, then recommend" deliverable for choosing *how*.

> **Terminology guard (do not drop):** everything below is a **numerics upgrade to
> Route A**. It is **not** roadmap **"Route D"** — that is the later Tier-3
> computer-assisted-proof leg (interval arithmetic, domain-expert collaboration),
> which only exists *after* a Tier-2 candidate. See
> [CLAY_ROADMAP.md](CLAY_ROADMAP.md#L135).

---

## 1. What the field actually uses (grounded, with sources)

Three distinct numerical paradigms appear in the singularity-formation literature
for exactly our models (Hou–Luo / 2D Boussinesq / 3D axisymmetric Euler):

**(P1) Dynamic (self-similar) rescaling — time-integration in a rescaled frame.**
Evolve the PDE in variables `y = x/λ(τ)`, rescaled amplitude, and rescaled time
`τ = -log(T−t)`, where the scaling factors evolve by **modulation ODEs** chosen to
enforce normalization conditions (e.g. pin the profile amplitude and a derivative at
the origin). A self-similar blow-up becomes a **steady state** of the rescaled
equation, held **resolved on a fixed grid** as physical time approaches `T`. This is
the classical method (originating in NLS: McLaughlin–Papanicolaou–Sulem–Sulem) and
is exactly how Chen–Hou constructed the approximate self-similar profile underlying
their 2022 proof. Chen–Hou needed a **two-scale** variant (a second scaling degree
of freedom, treating the space dimension as continuous) to kill a scaling
instability the one-scale form could not.
[[Chen–Hou II, arXiv:2305.05660]](https://arxiv.org/pdf/2305.05660)
[[Hou, MMS 2025 numerics]](https://users.cms.caltech.edu/~hou/papers/MMS-Numerics-2025.pdf)

**(P2) Direct self-similar profile construction — solve the profile equation
itself.** Substitute the self-similar ansatz `u(x,t) = (T−t)^α f(x/(T−t)^β)` into the
PDE to get a *stationary* nonlinear PDE-eigenvalue problem for the profile `f` and
the scaling exponent `λ` (or `α,β`), and solve it directly (Newton, or a
physics-informed neural network). No time-integration; the singular scale is baked
into the ansatz, so there is no resolution wall at all. This is the current cutting
edge: Wang–Lai–Gómez-Serrano–Buckmaster found the first smooth self-similar 2D
Boussinesq / 3D Euler profiles this way (PRL 2023), explicitly as *"the basis of a
future computer-assisted proof."* The 2025–2026 frontier pushes this to **unstable**
and **singular (unbounded) profiles** to machine precision, aimed directly at
computer-assisted proofs.
[[Wang–Lai–Gómez-Serrano–Buckmaster, PRL 2023, arXiv:2201.06780]](https://arxiv.org/abs/2201.06780)
[[Resolving unstable singularities to machine precision, arXiv:2511.22819]](https://arxiv.org/abs/2511.22819)
[[Novel singular-profile blowups, Hou-Luo + 2D Boussinesq, arXiv:2604.01868]](https://arxiv.org/abs/2604.01868)

**(P3) Adaptive mesh refinement / adaptive moving mesh — resolve the singular region
on a physical-space grid that concentrates points there.** This is what the original
Luo–Hou 2014 discovery used (adaptive moving mesh, ~10¹² amplification). General —
does not assume self-similarity — but heavy engineering, moves off the spectral
solver, and for a structure that *is* (approximately) self-similar it is strictly
more work than (P1) for the same result.

**Reading of the landscape.** The field has essentially *moved past* AMR (P3) toward
self-similar methods (P1/P2) for these specific singularities, precisely because the
blow-up is self-similar and P1/P2 exploit that to resolve it exactly. Notably,
**none of the modern frontier is an evolutionary search over initial conditions** —
it is profile construction (P2), increasingly NN-assisted, targeting novel
(unstable/singular) profiles.

---

## 2. Recommendation

**Build P1 (dynamic self-similar rescaling) as the concrete first step — one-scale
first, add the second scale only if a scaling instability shows up — and reject P3
(AMR).** Rationale:

1. **It reuses the asset we already trust.** Dynamic rescaling is a *change of
   variables plus a few modulation ODEs* bolted onto the existing validated
   pseudo-spectral solver (`solver/boussinesq.py`). AMR would mean a new
   finite-difference/adaptive-grid solver — throwing away the validated code and
   debugging a new discretization at the same time.
2. **It directly dissolves our documented wall.** Fitness would be measured on
   *resolved* self-similar structure (the profile and its exponent `λ`) instead of
   on the grid's own breakdown. That is the exact failure mode
   `NEGATIVE_RESULT_TWO_CURRENCIES.md` diagnosed.
3. **It is the de-risked on-ramp to the real novelty frontier.** The late-time state
   of a dynamic-rescaling run **is** a self-similar profile — the same object P2
   constructs directly. So P1 gives us (a) an honest structure-tracking fitness for
   an evolve-ICs search AND (b) a warm-started profile we can later refine with P2
   (Newton/PINN) if we pivot toward unstable/novel profiles. It keeps both doors
   open; AMR opens neither.
4. **It is field-validated on our exact model.** Chen–Hou's proof profile came from
   this method. We would be adopting the community-standard tool, not inventing one.

**Honest caveat that this research surfaced (matters for the "lottery ticket").** The
literature says the current *highest-novelty, most-Clay-relevant* activity is **P2
profile construction of unstable/singular profiles**, not evolve-ICs search. Dynamic
rescaling (P1) primarily finds the **stable** self-similar blow-up — which for 2D
Boussinesq is the one Chen–Hou already *proved*. So P1 by itself, used only as a
better fitness for an IC search, risks being a well-engineered route to a
already-known answer. The value case for P1 is strongest when it is framed as **the
on-ramp to P2**, not as a permanent commitment to the GA-over-ICs paradigm. This is
the Option-A / Option-B tension from the last decision, now with real information:
the two are not rivals — **P1 is the shared substrate, and P2 is where novelty
lives.** Recommended posture: build P1, and treat "do we then evolve ICs, or pivot
to P2 profile-hunting?" as the *next* gated decision, made with a working rescaling
solver in hand.

---

## 3. Spike-first plan (each spike STOPS for review)

Consistent with the project discipline (build the method on a known-answer substrate
before the expensive port; cf. the Route-C→A/Phase-0 rationale in
[CLAY_ROADMAP.md](CLAY_ROADMAP.md#L124)):

**Spike 0 — 1D dynamic rescaling on gCLM, against a known answer.**
Reuse the *existing* 1D gCLM solver. Implement one-scale dynamic rescaling and verify
it reproduces a **known** self-similar blow-up:
- easiest target: CLM (`a=0`) has a closed-form blow-up — the rescaled solution must
  converge to the known profile and the rate must match analytics;
- richer target: the Hou–Luo/De Gregorio family has *exact self-similar* profiles
  ([arXiv:2308.01528](https://arxiv.org/abs/2308.01528)) — the rescaled steady state
  and exponent `λ` must match.
Success criterion (pre-committed, in the spike's own predicate doc): rescaled
solution reaches a steady profile; recovered `λ` and profile match the known answer
to a stated tolerance; the modulation ODEs hold their normalization. **Cheap** (1D,
existing solver). This de-risks the entire technique before any 2D work. If it
fails, we debug in 1D where the answer is known — never in 2D against an unknown.

**Spike 1 — 2D dynamic rescaling on Boussinesq, reproduce the Chen–Hou profile.**
Port the validated rescaling machinery to `solver/boussinesq.py` in the Hou–Luo
geometry. Success criterion: converge to an approximate self-similar profile
consistent with the published Chen–Hou / Wang–Lai profile (qualitative shape +
exponent in the reported range). This is the real deliverable: a solver that resolves
the true singular structure. **Larger** (2D, new RHS + modulation, likely one-scale
→ two-scale if instability appears). Reproducing a *published* profile is the
validation gate — we are matching a known target, not claiming novelty.

**Then — gated decision (not part of this build):** with a working rescaling solver,
choose the forward use: (i) structure-tracking fitness for an evolve-ICs QD search
[Option A continues], or (ii) pivot to P2 profile construction / unstable-profile
hunting [Option B], warm-started from the P1 profile. Decide then, with data.

---

## 4. Honest scope, risks, and non-claims

- **Still a 2D toy model.** Even a flawless dynamic-rescaling solver reproducing the
  Chen–Hou profile is reproducing a *proven, published* result in a toy model across
  "Wall C" (2D Boussinesq ≠ 3D NS). Reproduction validates our machinery; it is not
  novel and not a proof.
- **Novelty, if any, is downstream and is P2's.** A genuinely new contribution would
  be a *new* self-similar profile (e.g. an unstable branch, or one our
  search-over-ICs surfaced that direct construction had not) — that lives on the far
  side of Spike 1, in the gated P2 decision, and would still need Route D to be
  certified.
- **Technical risks:** (a) scaling instability may force the two-scale formulation
  (Chen–Hou hit exactly this) — Spike 0 will reveal it cheaply in 1D; (b) choosing
  the modulation normalization conditions is fiddly and model-specific; (c) the
  Hou–Luo profile is only *approximately* self-similar, so "converged" needs a
  tolerance, not an equality.
- **Effort:** Spike 0 is days; Spike 1 is the multi-week lift. Both are right-sized
  solver work, not a 3D-Euler-scale program.

---

## 5. Open sub-decisions for sign-off

1. **Method:** adopt P1 (dynamic rescaling), reject P3 (AMR)? [recommended: yes]
2. **Framing:** accept the honest posture that P1 is the *on-ramp*, with A-vs-B
   (evolve-ICs vs profile-construction) re-decided at a gate *after* Spike 1, rather
   than committing now? [recommended: yes]
3. **Spike 0 target:** CLM closed-form first (simplest), then the exact
   Hou–Luo/De Gregorio self-similar profile? [recommended: yes, CLM first]
4. **Scope of this session:** proceed to *implement Spike 0* now, or stop at this
   written plan for review first?

---

## Sources

- Chen & Hou, *Stable nearly self-similar blowup of the 2D Boussinesq and 3D Euler
  equations with smooth data II: Rigorous Numerics*, arXiv:2305.05660.
- Chen & Hou, *Finite time blowup of 2D Boussinesq and 3D Euler equations with
  C^{1,α} velocity and boundary*, arXiv:1910.00173.
- Hou, *Stable Nearly Self-Similar Blowup of the 2D Boussinesq …* (MMS numerics,
  2025), users.cms.caltech.edu/~hou/papers/MMS-Numerics-2025.pdf.
- Wang, Lai, Gómez-Serrano & Buckmaster, *Asymptotic self-similar blow-up profile for
  3D axisymmetric Euler equations using neural networks*, PRL 130 244002 (2023),
  arXiv:2201.06780.
- *Resolving Sharp Gradients of Unstable Singularities to Machine Precision via
  Neural Networks*, arXiv:2511.22819 (2025).
- *Novel Self-similar Finite-time Blowups with Singular Profiles of the 1D Hou-Luo
  Model and the 2D Boussinesq Equations*, arXiv:2604.01868 (2026).
- *Exact self-similar finite-time blowup of the Hou–Luo model with smooth profiles*,
  arXiv:2308.01528.
- *Singularity Formation: Synergy in Theoretical, Numerical and Machine Learning
  Approaches* (survey), arXiv:2604.16842.
