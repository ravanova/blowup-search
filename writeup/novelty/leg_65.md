# Leg 65 — Route-L1G novelty pass (run BEFORE the writeup)

**Date:** 2026-08-05. **Agent:** LEG-H. **Branch:** `leg/l1g-v1`. **Claim-bearing,
literature-only leg** — no computation, no new bound, and it does not touch the Route-D
bound-sharpening ban.

Per `writeup/novelty/README.md` and the lesson from leg 53: **links, not counts.** Every query
string below is verbatim; every link a query returned that I judged on-topic is listed, and
where a query returned nothing on-topic I say so instead of reporting a number.

**`DIRECTION.md` has no leg-65 entry.** Its status block still closes the 2026-08-05 cycle at
leg 57 and its queue runs to 63. The thesis and the verbatim gate came from the dispatch prompt.
Flagged for the orchestrator, not worked around.

---

## The two claims under test, stated as this repository states them

**(C1) The weighted-`ℓ¹` no-go (Route-D v3).** From
`writeup/4_p2_lottery/TECHNICAL_P2_ROUTED_SPACES.md`, as summarised verbatim in
`solver/holder_norms.py`'s module docstring:

> "a diagonal weight on Fourier coefficients measures SMOOTHNESS, and the far-field transport
> needs DECAY. No weighted-ell^1 pair can carry the certificate."

and in `LITERATURE_CHECK.md`'s candidate table:

> "The weighted-`ℓ¹` conservation law / no-go (v3) — the two NK requirements are separated by
> exactly one grading power, and the separation is conserved."

**(C2) The discrete-ball trap (Route-D v6, measurement B1).** From
`experiments/p2_route_d_v6_bounds.py`'s header:

> "Computing an induced norm by duality over the DISCRETE unit ball is unsound: a discrete
> Holder seminorm only inspects grid nodes, so the extremizer duality selects is a grid-scale
> sign pattern whose interpolant has an enormous continuum norm."

**Prior bookkeeping this pass is auditing.** `capabilities.py` line 179 says the weighted-`ℓ¹`
no-go "is derived here and is UNSEARCHED at primary source"; `PHASE2_P2_NOTES.md` §M-4 says CLN
arXiv:2302.12877 works in Hilbert/Fourier `H^l` spaces, so it **narrows but does not close**
either claim, and both are "still UNSEARCHED at primary source, and still the only claims with a
real chance of being new."

---

## Queries, verbatim, with the links returned

### Q1
`weighted ell^1 Fourier norm cannot simultaneously control smoothness and decay computer-assisted proof no-go`

- https://arxiv.org/pdf/2203.02404 — a posteriori validation of generalized polynomial chaos expansions
- https://arxiv.org/html/2603.02021 — `ℓ¹` mapping properties, smoothness and decay for SU(2)-valued nonlinear Fourier transform
- https://arxiv.org/pdf/1601.00307 — Fourier–Taylor parameterization of unstable manifolds for parabolic PDEs
- https://arxiv.org/pdf/2303.03518 — computer-assisted validation of a periodic orbit in the Brusselator
- https://www.sciencedirect.com/science/article/pii/S1063520315000196 and https://arxiv.org/pdf/1308.0759 — interpolation via weighted `ℓ¹` minimization
- https://arxiv.org/pdf/1503.02352 — infinite-dimensional `ℓ¹` minimization and function approximation from pointwise data

**On-topic for C1: none.** The `ℓ¹` hits are compressed-sensing/approximation-theory weighted
`ℓ¹`, a different object from a weighted `ℓ¹` sequence space carrying a radii-polynomial
certificate. The CAP hits (2203.02404, 1601.00307, 2303.03518) all *use* a weighted `ℓ¹`/`ℓ¹`
Wiener-algebra norm with geometric weights `ν > 1` and none remarks on a smoothness/decay
obstruction — which is the same pattern the second pass recorded ("standard work uses `ν>1`
geometric weights, which avoids the regime").

### Q2
`induced operator norm by duality over discretized unit ball unsound extremizer grid-scale sign pattern Holder seminorm validated numerics`

- https://njohnston.ca/2016/01/how-to-compute-hard-to-compute-matrix-norms/ — computing hard matrix norms
- https://www.sciencedirect.com/science/article/pii/S0024379520300197 — seminorm and numerical-radius inequalities in semi-Hilbertian spaces
- https://arxiv.org/pdf/2503.19190 — learning polyhedral norms and convex regularizers
- https://projecteuclid.org/journals/illinois-journal-of-mathematics/volume-32/issue-4/... — duality in spaces of operators and smooth norms

**Nothing on-topic for C2.** Only the generic fact that a norm is a sup over the dual ball —
which is the *premise* of the trap, not the trap.

### Q3
`rigorous numerics dual norm computed over finite-dimensional discretization underestimates continuum operator norm interpolant Holder seminorm pitfall`

- https://arxiv.org/pdf/2305.05660 — Chen–Hou, stable nearly self-similar blowup of 2D Boussinesq / 3D Euler II: rigorous numerics
- https://arxiv.org/abs/2502.09984 — verified error bounds for singular values of structured matrices, for CAPs
- https://arxiv.org/pdf/1812.08100 and https://arxiv.org/pdf/2203.07126 — Kosov–Temlyakov, sampling discretization error for function classes / for classes with small smoothness
- https://link.springer.com/article/10.1007/s00365-021-09539-0 — sampling discretization of integral norms
- https://arxiv.org/pdf/2312.05670 — bounds for the sampling discretization error

**The nearest published relative of C2, and it is a different subject — recorded so a later
pass does not have to rediscover that.** The sampling-discretization literature
(Temlyakov and co-authors) asks exactly when a norm evaluated at finitely many nodes is
comparable to the continuum norm, and its headline is that this **degrades as the smoothness of
the class drops**. That is the ambient reason C2 is true, but none of these papers is about a
*dual/extremizer* computation inside a certificate, none is about a Hölder seminorm on a graded
grid, and none reports an inflation factor. It is background mathematics for the trap, not a
publication of it.

### Q4
`Temlyakov sampling discretization of norms fails for function classes without smoothness discrete norm does not control continuum norm survey`

- https://arxiv.org/abs/2203.07126 — sampling discretization error of integral norms for classes with small smoothness
- https://link.springer.com/article/10.1007/s00365-021-09539-0 — sampling discretization of integral norms
- https://link.springer.com/article/10.1134/S0001434625030265 — sampling recovery on function classes with a structural condition

Confirms Q3's reading and nothing more.

### Q5
`Campolina Mailybaev "Fluid dynamics on logarithmic lattices" Nonlinearity 2021 arXiv function spaces norms conservation laws`

- https://iopscience.iop.org/article/10.1088/1361-6544/abef73 and https://arxiv.org/pdf/2005.14027 — Campolina–Mailybaev, *Fluid dynamics on logarithmic lattices*, Nonlinearity **34** (2021) 4684–4715
- https://iopscience.iop.org/article/10.1088/1361-6544/ad7661 — the published version of arXiv:2312.01702

The **forward-cited framework paper** for Tier-2 `2312.01702`, and the one place a "weighted
sequence-space conservation law" could plausibly live. Read at full text below.

### Q6 — forward-citation sweep, not a text query
`https://api.semanticscholar.org/graph/v1/paper/arXiv:2312.01702/citations` and
`.../arXiv:1908.09385/citations`

- Citing `2312.01702` (8 papers, all turbulence physics): 2607.18788, 2607.06062, 2508.10659,
  2508.05686, 2507.03196, 2502.19005, 2405.04112, and one un-indexed BEC paper.
- Citing `1908.09385` (31 papers): the gCLM/De Gregorio/Hou–Luo blowup corpus — 1905.06387,
  2010.01201, 2010.12700, 2106.05422, 2107.04777, 2206.01296, 2207.07548, 2209.08232,
  2305.05895, 2308.01528, 2401.14615, 2411.01891, 2503.06383, 2506.02800, Chen–Hou Part II,
  and **https://arxiv.org/abs/2607.15256 — Chen–Hou, _Analytic finite-rank corrections for
  singularly weighted estimates in a computer-assisted proof of 3D Euler singularity_ (16 Jul
  2026)**.

**2607.15256 is the one live candidate the sweep produced** — a 2026 methodological CAP paper
whose entire subject is an obstruction to weighted norms. It was fetched and read at full text;
see below.

---

## What this pass settles before the full-text read

**Verdict: `PROCEED`.** No search-level hit publishes either claim. That is worth exactly what
this project has said search-level evidence is worth five times — nothing — so the gate is
answered from full texts, below, and never from an abstract page.

