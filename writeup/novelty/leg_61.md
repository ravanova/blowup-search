# Leg 61 — Route-KA novelty pass (run BEFORE construction)

**Date:** 2026-08-05. **Agent:** LEG-E. **Branch:** `leg/ka-v1`.
**Verdict: `PROCEED_AS_INTERNAL_AUDIT`.** This leg may claim **nothing** about the Kawahara
equation, about solitons, or about certification methodology. The Kawahara soliton is proved
(Cadiot–Lessard–Nave, arXiv:2302.12877 Thm 6.6, SIADS 10.1137/23M1607507), the proof is
published, and its verification package is released. The only claimable object here is a
statement about **this repository's own pipeline**: whether `solver/interval_certificate.py`,
pointed at a problem whose answer is in print, lands inside the published window. That is a
self-audit, not a result about mathematics.

Per `writeup/novelty/README.md` and the standing convention: **links, not counts.** Every query
string below is verbatim; every returned link I judged on-topic is listed; where nothing came
back on-topic I say so instead of quoting a number.

---

## The two things that could conceivably be novel, kept separate

* **(N1)** The *object* — existence of a Kawahara soliton, with a certified radius.
  **Already in print, and not remotely open.** No claim available.
* **(N2)** The *act* — an independent re-derivation of another group's published certified
  radius by a differently-constructed pipeline, in a **different norm** (weighted `ℓ^∞`
  rather than the Hilbert `H^l` CLN use), reported as a cross-norm magnitude.
  **Not found in print as a described practice**, but this pass judges that a **methodological
  non-finding, not a gap**: cross-validating one's own code against a published answer is
  ordinary hygiene that nobody writes a paper about. Claiming it as novelty would be exactly
  the failure mode leg 51 was docked for.

---

## Queries, verbatim, with the links returned

### Q1
`independent reproduction Cadiot Lessard Nave Kawahara soliton computer-assisted proof radius replication`

- https://arxiv.org/abs/2302.12877 — CLN, the source itself
- https://doi.org/10.1137/23M1607507 — the SIADS version of the same
- https://arxiv.org/pdf/2503.04701 — Computer-assisted proofs of gap solitons in BECs (same
  machinery, different object; cites CLN, does not re-derive their radius)
- https://arxiv.org/pdf/2509.17099 — localized patterns / saddle-node CAPs in 1D
  activator–inhibitor models (same machinery, different object)
- https://link.springer.com/article/10.1007/s00332-026-10242-2 — JNLS version of the BEC work

**Nothing on-topic** for an *independent reproduction* of CLN's Kawahara radius by a second
group or a second code base. The follow-on literature reuses the method; it does not re-run the
example.

### Q2
`weighted ell^infinity sup norm radii polynomial reproduce published Hilbert space H^l certified radius cross-norm comparison`

**Nothing on-topic.** Every returned link was about the *numerical radius* of a Hilbert-space
operator (a different object with a colliding name) or about certified robustness in machine
learning:
- https://arxiv.org/abs/2111.14222 — weighted Hilbert–Schmidt numerical radius
- https://www.sciencedirect.com/science/article/abs/pii/S0024379522003834 — weighted numerical radii
- https://arxiv.org/pdf/2207.02152, https://arxiv.org/pdf/2002.08118 — randomized smoothing (ML)

The name collision is itself worth recording: searching for "certified radius" in the
`ℓ^∞`-vs-`H^l` sense is polluted by two unrelated literatures, so absence of hits here is weak
evidence and is not used as such.

### Q3
`benchmark suite validating computer-assisted proof software against another group's published certified radius rigorous numerics cross-validation`

- https://vncap.org/ — Validated Numerics for CAP, the community hub
- http://capd.ii.uj.edu.pl/ and https://arxiv.org/pdf/2010.07097 — CAPD::DynSys toolbox
- https://github.com/juliaintervals/intervalarithmetic.jl — the interval layer CLN themselves use
- https://www.reliable-computing.org/intsoft.html — interval software index

**No standing cross-validation benchmark suite for CAP frameworks was found.** The closest
returned item is a *performance* comparison (HomotopyContinuation.jl vs Macaulay2), not a
published-radius reproduction. So the practice this leg performs is not standardized anywhere I
can locate — which is a reason to do it, not a reason to claim it.

### Q4
`Kawahara equation soliton rigorous numerics Y0 Z1 Z2 bounds reproduced ProofKawahara.jl`

- https://doi.org/10.1137/23M1607507 — CLN again
- https://arxiv.org/pdf/2503.04701 — BEC gap solitons, same `Y0/Z1/Z2` shape
- the remaining hits were analytical/numerical Kawahara papers (tanh-expansion exact solutions,
  well-posedness, control theory) with no rigorous-numerics content

**Nothing on-topic** for a third-party recomputation of CLN's constants.

---

## What this pass did NOT do by search, and did by fetch instead

The decisive fact for this leg is not in any search result. `Papers/fetch.sh 2302.12877`
retrieved the paper, and the code repository named in its reference [15] is live and complete:

- https://github.com/matthieucadiot/ProofKawahara.jl — `ProofKawahara.jl`, 23,948 bytes, plus
  README and LICENSE.

Reading it fixes the truncation the paper never prints, which is what makes the pre-committed
window meaningful: **`N = 250` cosine modes (0..250), half-domain `d = 50`, Bond number
`T = 0.35`, wave speed `c = 0.9`.** The paper prints only the constants
(`‖DF_e(u_0)^{-1}‖_{2,l} ≤ 4.4`, `Y_0 ≤ 2.26e-14`) and the conclusion (`r_0 = 2.27e-14`,
uniqueness in `B_{0.015}`).

**This is worth recording against the ledger.** `LITERATURE_CHECK.md`'s seventh pass records
arXiv:2604.09949 as unusable partly because *no verification package is released*. CLN are the
opposite case, and the contrast is the reason this leg is runnable at all: the window can be
pre-committed at the published truncation because the truncation is published, in code, even
though it is absent from the paper.

---

## The window, pre-committed here, before any construction (lesson 84)

Stated now so it cannot be moved later. CLN certify in `H^l` on `ℝ`; this repository's pipeline
certifies in a weighted `ℓ^∞` norm on cosine coefficients. The radii are therefore **not the
same number**, and the comparison is only honest with a stated, rigorous conversion:

* for a coefficient vector supported on `|n| ≤ N`, `‖a‖_{ℓ²_l} ≤ √(2N+1) ‖a‖_{ℓ^∞_l}`;
* CLN's Thm 6.6 also gives the coefficient-space statement `Ũ ∈ B_{r_0/√|Ω_0|}(U_0) ⊂ X^l_e`,
  so the function-space radius is `√|Ω_0| = √100 = 10` times the coefficient-space one.

So our `r_min` converts **upward** into CLN's norm by the factor `√(2N+1)·√|Ω_0| = √501·10 ≈
223.8`, and the pre-committed window on the converted radius `r*` is

> **`r* ∈ [2.27e-14, 1.5e-2]`** — at or above CLN's existence radius `r_0`, and at or below
> their uniqueness radius.

Both ends are load-bearing and neither is decoration:

* **upper end.** A converted radius above `0.015` means the certificate cannot even reach inside
  the ball where CLN prove uniqueness — the pipeline would be closing on something it cannot
  identify with their soliton.
* **lower end.** Our pipeline bounds strictly **fewer** error terms than CLN's: it certifies the
  finite Galerkin system and does *not* carry the Fourier tail `n > N` or the unbounded-domain
  correction, both of which CLN include. A converted radius *below* `r_0` is therefore evidence
  of **over-optimism**, not of a sharper proof, and would be reported as such.

Magnitudes, not booleans: the log10 distance to each end is reported whatever the outcome.
