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

---

# Full-text pass — the gate

> **Gate.** "Does any primary source (the two unread Tier-2 papers, or anything they cite
> forward) already publish the weighted-ell-1 no-go or the discrete-ball trap for this operator
> class, or an equivalent statement under different notation?"

**Answer: NO**, for both claims, after reading four papers at full text. The bookkeeping in
`capabilities.py` line 179 and `PHASE2_P2_NOTES.md` §M-4 is **confirmed, not corrected** — and
it is now confirmed at a strictly higher standard than "fetched but not read". No correction to
`solver/holder_norms.py` is required by this leg.

## Papers read at full text, and what each was searched for

`bash Papers/fetch.sh 2312.01702 1908.09385 2607.15256 2005.14027` — egress worked first
attempt (arxiv.org HTTP 200); all four extracted with `pdftotext -layout`.

### 1. arXiv:2312.01702 — Pikeroen, Barral, Costa, Campolina, Mailybaev, Dubrulle, *Tracking complex singularities of fluids on log-lattices* (v1, 4 Dec 2023; Nonlinearity 37 (2024), DOI 10.1088/1361-6544/ad7661)

**Read:** §2.1 Definitions and notations, §2.2 Global quantities, §2.3 Regularity, §2.4
Singularity strip method, §2.5 Numerical methods, §3.1–3.4 (1D Burgers), §4.1–4.5 (3D
Euler/NS), §5.1–5.3 Discussion, and the full reference list (28 items).

**Neither claim is present, and the paper has no machinery that could carry either.**
Magnitudes rather than a boolean: the extracted text contains **0 occurrences of "weight"**,
**0 of "Banach"**, **0 of "computer-assist"**, **0 of "validated"**, and its only uses of
"rigorous" are disclaimers that rigour is *absent* — §2 line 242: *"we have presently no
rigorous statements about the dyadic model for the parameter …"*, and §3: *"Despite the absence
of rigorous proofs, it is …"*. The method is the **singularity strip method**: fit `δ` from the
slope of `log E(k)`, with §2.4's criterion
`û_k ∼ k^{−d−ξ} e^{ika} e^{−δk}` ⇒ `E(k) ∼ e^{−2δk}`, integrated by explicit RK4 with a
viscous-splitting factor `e^{−νk^{2γ}} dt` (§2.5). There is no norm, no operator bound, no
approximate inverse and no duality argument anywhere in the paper. It is a numerical-physics
scaling study.

**What it *does* have, recorded so the resemblance is not mistaken for prior art later:** it is
the source of the "measure the exponent, not the threshold" discipline that
`LITERATURE_CHECK.md` correctly flags as a possible pre-emption of the *`μ`-as-a-coordinate*
observation (a different candidate, not this leg's). Its critical-dissipation section (§3.4,
§4.5) works at `γ = 1/3` — the log-lattice analogue of a critical exponent, and unrelated to
`ℓ¹` weights.

### 2. arXiv:2005.14027 — Campolina & Mailybaev, *Fluid dynamics on logarithmic lattices*, Nonlinearity **34** (2021) 4684–4715 (the framework paper 2312.01702 rests on; read because it is the only forward-cited place a weighted sequence-space "conservation law" could live)

**Read:** the function-space section (eq. (37)–(38), (40)), the local-existence argument
(eq. (45)–(46), (50)), the blow-up criterion, and Appendix B (Lemma 15, eq. (78)).

**The space is weighted `ℓ²`, not weighted `ℓ¹`, and the structural result runs the opposite
way to our no-go.** Verbatim, eq. (37):

> `‖u‖_{h^m} = ‖D^m u‖_{ℓ²} = ( Σ |k|^{2m} |u(k)|² )^{1/2} < ∞`

with `V^m = {u ∈ h^m | ∇·u = 0}` (eq. (38)) "endowed with the `h^m` norm", i.e. a **Hilbert**
grading exactly as CLN's `H^l` is — the same reason §M-4 gives for CLN not closing the claim
applies verbatim here. Their key structural statement is:

> "Operator `B` is a bounded bilinear operator in `h^m` – see the proof in Appendix B."

with the product estimate (eq. (54)/(78))
`‖f ∗ g‖_{h^m} ≤ C(‖f‖_{h^m}‖g‖_{ℓ^∞} + ‖Df‖_{ℓ^∞}‖g‖_{h^{m−1}})`.
That is a **positive** algebra estimate — the convective term is *bounded* because interactions
on a log-lattice are local — which is the structural opposite of C1's claim that no weighted
pair can simultaneously carry smoothness and far-field decay. The log-lattice sidesteps the
far-field question entirely: the lattice is a geometric sequence in `k`, so there is no
unbounded physical-space transport tail to invert.

### 3. arXiv:1908.09385 — J. Chen, *Singularity formation and global well-posedness for the generalized Constantin–Lax–Majda equation with dissipation* (v1, 25 Aug 2019)

**Read:** §1 (Theorems 1.1–1.5, Remarks 1.2–1.7), §2.1–2.4 in full (dynamic rescaling,
normalization (2.11), the weights (2.12), the weighted `L²` linear estimate (2.13)–(2.19), the
weighted `H⁴` estimate), §2.5–§2.6 (nonlinear stability, Remarks 2.1–2.2), the global
well-posedness sections, and Appendix A (Hardy inequalities, Remark A.7). This paper had
previously been read **for computer assistance only** (leg 45), never for C1/C2.

**Neither claim is present.** The paper is a perturbative analytic argument, and its weights are
**continuum, physical-space energy weights**, not sequence-space gradings. Verbatim, (2.12):

> `ϕ = (x² + b²)³ / (2bx⁴) = −(1/ω̄) (x² + b²)/x³ ,  ψ = (x² + b²)³/(2b) = −x(x² + b²)/ω̄`
>
> "and will perform weighted `L²` and weighted `H⁴` estimates to establish the nonlinear
> stability. … In the following discussion, we assume `ω ∈ L²(ϕ) ∩ H⁴(ψ)`."

**The genuine near-miss, stated precisely because it is the closest this paper gets.** Chen's
two weights differ by exactly `x⁻⁴`: `ϕ = ψ/x⁴`, with the **singular** weight on the *low*-order
(`L²`) estimate and the **less singular** weight on the *high*-order (`H⁴`) estimate — a
**two-grading structure with a fixed grading offset**, which is the same *shape* as C1's "the
two requirements are separated by exactly one grading power". Two reasons it is not C1, and both
are decisive:

1. **The offset is chosen, not obstructed.** Chen picks `ϕ`, `ψ` so the singular part of the
   weight is cancelled by the profile (§2.3: *"For `D`, we separate the singular and less
   singular part of the weight `ϕ` defined in (2.12)"*, then integrates by parts using
   `ω = O(|x|³), ω_x = O(|x|²)`). The offset is a working device; nothing is said to be
   impossible, and no statement is made about the *class* of admissible weights.
2. **The space is `L²(ϕ) ∩ H⁴(ψ)`, a Hilbert pair on the line.** There is no `ℓ¹`, no Wiener
   algebra, no Fourier-coefficient grading: the extracted text has **3 occurrences of "Fourier"**
   in the entire paper (a Littlewood–Paley cutoff in Appendix A and one reference title) and
   **0 of "Wiener" or "Besov"**. There is also **no computer assistance** — which re-confirms
   leg 45's finding from the same text.

**On C2: absent, and structurally so** — the paper never discretizes, so there is no discrete
ball to take a dual over.

### 4. arXiv:2607.15256 — Chen & Hou, *Analytic finite-rank corrections for singularly weighted estimates in a computer-assisted proof of 3D Euler singularity* (16 Jul 2026) — **the one forward citation that could have answered the gate YES**

This paper cites 1908.09385 and is, by title and subject, the closest published object to C1
that exists: a **methodological** CAP paper whose entire content is an obstruction encountered by
**singularly weighted** norms. It was read at full text (abstract, §1.1 strategy, §1.2–1.3
weighted estimates and finite-rank perturbation, §1.4 "The need for analytic low rank
corrections", §2.1, §4, §5 Step 2).

**It publishes a weight obstruction — but a different one, in a different space, with the
opposite resolution.** Verbatim, from the abstract:

> "One effective approach to establishing stability of perturbations around a numerically
> constructed profile is to perform weighted energy estimates with singular weights near the
> singularity. However, the weighted norms require exact local vanishing conditions that are
> not automatically preserved by the equations nor the numerical construction."

and §1.4:

> "the singular weights are effectively of order `|x|^{−3}` near the origin. To employ the
> singularly weighted energy estimates, the perturbation must vanish cubically near the origin
> `f(x) = O(|x|³)`, near `x = 0` … However, the natural odd/even symmetry class of the
> perturbation and the equations preserves only quadratic vanishing order."

That is a **local vanishing-order** obstruction at the singularity, in weighted `L^∞`/`C^{1/2}`
energy spaces, and it is **resolved** — by analytic low-rank corrections that upgrade the
vanishing order from `O(|x|²)` to exact `O(|x|³)`. C1 is a **far-field decay vs. smoothness**
obstruction, in a weighted `ℓ¹` sequence space, asserted as a **no-go over a whole class of
weights**. Different end of the domain, different space, different logical form.

**The paper's own two-sided weight tension, quoted because it is the nearest published cousin of
C1's mechanism and a future write-up should cite it rather than pretend nothing like it is in
print** (§1.2, around (1.17)–(1.18)):

> "Since the energy must be finite and `η(x,0) ≠ 0`, one cannot choose `β ≥ 1`. If `(1 − β)` is
> not small, since `a₂` is much larger than `a₁, a₃`, the term `a₂(1−β)/2` arising from the
> `y`-advection in (1.17) contributes a large positive growth term. On the other hand, if
> `(1 − β)` is small, the estimate of the nonlocal term `u_x` in (2.2) contributes a large
> constant `(1 − β)^{−1/2}` … As a result, one needs to take a very singular weight `x^{−α}y^{−β}`
> or `|(x,y)|^{−α} y^{−β}` with large `α` to extract the desired damping effect."

So: a single weight exponent squeezed from both sides — finite energy above, nonlocal-term
constant blowing up as the exponent approaches the ceiling. **That is a published instance of
the *genre* C1 belongs to, in weighted `L²`.** What it is not, and what keeps C1 unsearched: it
is a **quantitative trade-off resolved by a choice** (take `α` large), not a statement that no
admissible pair exists; the competing requirements are *damping vs. finite energy*, not
*smoothness vs. far-field decay*; and the separation is not claimed to be conserved under the
certificate's operations.

**Also relevant to C2, and the one place any paper in this sweep touches the trap's moral**
(§1.4):

> "The key point is that the numerical step only determines coefficients in explicit basis
> representations. Once these coefficients are fixed, they determine functions defined on the
> entire domain, rather than merely numerical values on grid points. The subsequent low-rank
> corrections are performed analytically on the resulting globally defined functions, using
> their Taylor expansions near the origin. Hence the improved vanishing order is an exact
> analytic property of the corrected function."

This is the same *hygiene* C2 argues for — a grid-node object is not a continuum object, so
never let a rigorous step depend on node values alone — stated as working practice by
practitioners. It is **not** C2: they never compute an induced norm by duality over a
discretized unit ball, they report no extremizer inflation, and they do not state the failure
mode as a general fact about discretized balls. C2's specific claim (the dual extremizer over a
discrete Hölder ball is a grid-scale sign pattern, and its continuum norm inflates with the grid
size) appears in no paper found by this sweep.

---

## What the answer is, and what it costs

**NO on both claims, and the honest form of that is narrow.** What has now been checked at
full-text depth, and by whom:

| claim | 2302.12877 (CLN) | 2312.01702 | 1908.09385 | 2607.15256 (fwd) | 2005.14027 (fwd) |
|---|---|---|---|---|---|
| C1 weighted-`ℓ¹` no-go | narrowed, `H^l` not `ℓ¹` (leg 45, §M-4) | absent; no norms at all | absent; weights are `L²(ϕ)∩H⁴(ψ)` on the line | **nearest cousin**: weighted-`L²` two-sided tension (1.17)–(1.18), resolved not obstructed | absent; `h^m` is weighted `ℓ²`, and the bilinear term is *bounded* |
| C2 discrete-ball trap | not addressed | absent; no rigorous norms | absent; no discretization | moral present as practice (§1.4 basis-vs-grid-values), claim absent | absent |

**Where a counterexample would still be allowed to live, and this leg does not claim otherwise.**
The sampling-discretization literature (Q3/Q4) contains the ambient mathematics behind C2, and
this leg did not read Kosov–Temlyakov at full text — it read enough to classify the subject.
Anyone writing up C2 should cite that literature as background and should *not* claim C2 is
unrelated to it. For C1, the untested direction is the validated-numerics corpus that uses
`ℓ¹`-Wiener norms with geometric weights `ν > 1` (Q1's CAP hits): that regime **avoids** the
algebraic-decay setting where C1 bites, which is why nobody has had to state C1 — an
explanation, not a search result.

**Bookkeeping consequence.** `capabilities.py` line 179 ("UNSEARCHED at primary source") and
`PHASE2_P2_NOTES.md` §M-4 stay as written for C1 and C2 as *claims*, but the word "UNSEARCHED"
is now wrong in a favourable direction: after this leg the correct word is **SEARCHED AT PRIMARY
SOURCE AND NOT FOUND**, over five papers. Both files are outside this leg's territory and are
integration-owned; this is handed to the orchestrator as a wording correction, not edited here.
`solver/holder_norms.py` needs **no** change under the gate's no-branch — its docstring makes no
novelty claim; the novelty wording lives in `capabilities.py`.
