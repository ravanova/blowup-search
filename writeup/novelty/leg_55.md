# Leg 55 — Route-NB novelty pass (NB-0)

**Run BEFORE any construction**, per `CONTINUATION_PROMPT.md` Directive 3 and the standing
process rule. **Links, not counts** — leg 53's pass logged counts, could not be audited, and its
clearance was withdrawn. Every query below is written out, and every hit that mattered is a link.

**Date:** 2026-08-05. **Tool:** WebSearch (US index), six queries.

**Verdict: `PROCEED`.** The specific question — *what is the measured decay exponent of
`HL_S2_nonsymmetric`'s coefficients in the `X = tan(θ/2)` compactified basis, and does it put the
profile inside a weighted `ℓ¹` ball* — is not answered anywhere I can find. What *is* published is
the analytic far-field exponent (adjacent, and it is the input to the prediction I test), and the
weighted-`ℓ¹` machinery (adjacent, and it always assumes the analytic/geometric case). Nobody
joins them for this object. **Nothing is banked as a novel result by this pass** — a PROCEED is
permission to measure, not a claim.

---

## The queries, verbatim

### Q1 — "Fourier coefficient decay rate of self-similar blowup profile Hou-Luo De Gregorio computer-assisted proof weighted ell^1"

Hits that mattered:

- **arXiv:2308.01528**, *Exact self-similar finite-time blowup of the Hou–Luo model with smooth
  profiles* — <https://arxiv.org/abs/2308.01528> (published: *Comm. Math. Phys.*,
  <https://link.springer.com/article/10.1007/s00220-025-05429-9>). **This is the closest prior
  art on the object side.** It gives *rigorous estimates on the algebraic decay rates of the
  profiles in the far field*, by a purely analytic fixed-point method. That is the exponent `α`
  — the **input** to the coefficient-decay prediction — in **physical space**. It does not
  expand the profile in any basis and does not ask about `ℓ¹` membership.
- **arXiv:2106.05422**, *Asymptotically self-similar blowup of the Hou-Luo model for the 3D Euler
  equations* — <https://arxiv.org/abs/2106.05422> (Annals PDE:
  <https://link.springer.com/article/10.1007/s40818-022-00140-7>; author copy:
  <https://users.cms.caltech.edu/~hou/papers/HL-Annals-PDE-202.pdf>). The computer-assisted proof
  this project's target is *not* covered by. Weighted **`L²`/`H^k` energy** spaces, not `ℓ¹`.
- **arXiv:2604.01868** — *Novel Self-similar Finite-time Blowups with Singular Profiles of the 1D
  Hou-Luo Model and the 2D Boussinesq Equations* — <https://arxiv.org/pdf/2604.01868>. **Our
  target's source** (Chen–Huang–Li, sec 2.5/4). Numerical only. *Note: this hit resurfacing here
  does **not** clear leg 52's search-index flag — that flag was raised against a **different**,
  specific topical query, LIT reproduced its null result verbatim in its ninth pass, and leg 53's
  clearance was withdrawn. This is a different query and settles nothing about the flag.*
- **arXiv:2305.05895** — gCLM smooth self-similar blowups — <https://arxiv.org/html/2305.05895>.
- **arXiv:2603.25104** — gCLM *singular*-profile self-similar blowups —
  <https://arxiv.org/html/2603.25104>. Singular profiles, physical space.

### Q2 — "radii polynomial computer-assisted proof non-analytic profile algebraic far-field decay weighted ell^1 Fourier space unbounded domain compactification"

- **arXiv:2302.12877**, *Rigorous computation of solutions of semi-linear PDEs on unbounded
  domains via spectral methods* — <https://arxiv.org/pdf/2302.12877>. **The methodological
  nearest neighbour** (already in this repo's ledger for `solver/decay_grading.py`). Sobolev +
  Fourier on `ℝ^m`. It handles unbounded domains, but not by measuring whether a *given* profile's
  coefficients land in the ball.
- Lessard et al., *Automatic differentiation for Fourier series and the radii polynomial
  approach*, Physica D 334 (2016) —
  <https://www.sciencedirect.com/science/article/abs/pii/S0167278916000294>. Standard `ℓ¹_ν`.
- <https://arxiv.org/pdf/2403.10450> (Swift–Hohenberg localized patterns),
  <https://arxiv.org/pdf/2505.03091> (localized solutions on `ℝ^m`),
  <https://arxiv.org/pdf/1912.03836> (Cauchy–Kovalevskaya).
  **Every one of these assumes `ν > 1`, i.e. geometric weights, i.e. an analytic profile.** The
  recurring sentence across the corpus — *"when ν > 1 the coefficients decay at least
  geometrically, which means the associated function has analytic regularity"* — is exactly the
  hypothesis our target is suspected to violate, and none of these papers treats what happens
  when it does.

### Q3 — "algebraic decay exponent far field Hou-Luo self-similar profile omega ~ |x|^-alpha 0.394 rigorous estimate"

Re-surfaced **arXiv:2308.01528** and **arXiv:2106.05422**. **The specific value `α = 0.394` for
`HL_S2_nonsymmetric` is not found in any published source by this query** — in this repository it
is `c_ω/c_l` read off the solved bordered system, not a transcribed constant. Recorded as
**unchecked against primary source**, not as a gap and not as novel.

### Q4 — "Fourier sine coefficients decay k^{-1-alpha} algebraically decaying function Mobius transform x=tan(theta/2) compactification"

The `|t|^α` branch-point → `k^{-1-α}` correspondence is **classical** and I claim nothing about
it. The nearest explicit statement found:

- <https://arxiv.org/pdf/2006.05282> (Wiener–Hopf difference equations, semi-cardinal
  interpolation): *if a function decays algebraically with power α, the Fourier coefficients of
  the Wiener–Hopf factor decay with the same power* — the same mechanism, different setting.
- <https://arxiv.org/pdf/1805.02445> (Fourier decay of Hölder-continuous functions).

**No hit couples this to the tangent half-angle map as a compactification for a blowup profile.**
That coupling is what `solver/spectral_certificate.py::coefficient_decay_exponent` already
*asserts* (as a derivation, in a docstring). **This leg's contribution is that it is MEASURED on
the real target rather than asserted** — a small thing, and it is stated as a small thing.

### Q5 — "computer-assisted proof function space incompatible with solution regularity profile not in weighted ell^1 space certification failure"

**Nothing.** No paper found that treats "the solution is not in the certification space" as a
diagnosable, measurable failure mode rather than as an unstated hypothesis. Closest:
<https://arxiv.org/pdf/2103.12390> (saddle-type blow-up, validation failing from error
propagation — a *different* failure mode: the integrator, not the space).
**This is the gap this leg sits in.** It is a modest gap: the measurement is elementary once
posed. It is posed here because a live ban asserts its answer without it.

### Q6 — "Chen Hou Huang De Gregorio blowup profile Holder continuous not smooth at origin regularity 1/alpha function space choice"

- <https://arxiv.org/pdf/1905.06387> (Chen–Hou–Huang, De Gregorio finite-time blowup; CPA:
  <https://onlinelibrary.wiley.com/doi/abs/10.1002/cpa.21991>) — Hölder-continuous *initial data*
  with compact support. **Regularity of the initial data, not coefficient decay of the profile.**
- <https://jiajiechen94.github.io/research> — surveyed for anything closer; nothing.

---

## What this pass does and does not license

**Licenses:** measuring `|ĥ_k|` for `HL_S2_nonsymmetric` in the compactified basis and reporting
the fitted exponent with its resolution drift.

**Does not license:** claiming the `k^{-1-α}` correspondence as new (it is classical, Q4);
claiming `α` itself as new (arXiv:2308.01528 is the analytic prior art, Q1); claiming anything
about whether the certificate closes (that is `MM`'s gate, not this leg's); and it does not clear
or touch leg 52's standing search-index flag.

**Standing flag, untouched:** `arXiv:2604.01868` not resurfacing on leg 52's verbatim topical
query. **STANDS.** Q1 above is not that query.
