# Leg 62 — Route-CP novelty pass (run BEFORE construction)

**Date:** 2026-08-05. **Agent:** LEG-B. **Branch:** `leg/cp-v1`.
**Verdict: `PROCEED_AS_LEDGER_EXTENSION`.** This leg classifies literature; it does not
claim a mathematical finding. What it ships is an *executable ledger entry* with located
verbatim hypotheses, in the discipline `solver/literature_gates.py` set and
`solver/certificate_shapes.py` continued.

Per `writeup/novelty/README.md` and the standing lesson from leg 53: **links, not
counts.** Every query string below is verbatim, and every link I judged on-topic is
listed. Where a search returned nothing on-topic I say so rather than reporting a number.

**The standing constraint this pass inherits.** Leg 57's pass already settled that the
*observation* (a radii-polynomial tail estimate presumes an asymptotically diagonal
Fréchet derivative) is **folklore in print**, and Cadiot arXiv:2505.03091 is where it is
in print. Nothing below re-opens that. This pass is scoped to the *different* question
leg 57 explicitly did not answer.

---

## The claim under test

Not leg 51's methodological observation. **Leg 58's (NG's) hypothesis**, which is
narrower and load-bearing:

> There is no published construction covering an operator whose **unbounded part is
> off-diagonal** (a shift — the diagonal is not merely small, it is zero) **and whose
> tail inverse is therefore a non-decaying constant** rather than `1/Λ_M`.

The single largest novelty risk to that is Cadiot arXiv:2505.03091, because it is the
one paper in the corpus that (a) is by the author of the framework we are closest to,
(b) states the dominance hypothesis *as a hypothesis*, and (c) postdates every other
row of the ledger. Leg 57 flagged it and read two sentences of it. **This pass reads it
whole, and reads what it cites forward into this case.**

---

## Queries, verbatim, with the links returned

### Q1
`Cadiot "Stability analysis for localized solutions" PDEs nonlocal equations R^m computer-assisted`

- https://arxiv.org/pdf/2505.03091 — the target paper, full PDF
- https://arxiv.org/abs/2505.03091 , https://arxiv.org/html/2505.03091
- https://arxiv.org/html/2509.10375 — proving symmetry of localized solutions, dihedral
  patterns in the planar Swift–Hohenberg PDE
- https://arxiv.org/pdf/2509.16693 — traveling waves on an infinite strip for the
  suspension bridge equation, and orbital stability
- https://www.researchgate.net/profile/Matthieu_Cadiot2

**Use.** Located the PDF. The two follow-ons (2509.10375, 2509.16693) are the same
framework applied to further constant-coefficient problems; neither is on-topic for an
off-diagonal unbounded part. **The paper was then fetched and read at full text
(`Papers/fetch.sh 2505.03091`), which is what actually answers the gate — every
classification below is traced to a located statement, never to this search.**

### Q2
`Breden Payan Reisch Tang Turing instability nonlocal heterogeneous reaction-diffusion computer-assisted proof arXiv 2025 generalized Gershgorin`

- https://arxiv.org/abs/2504.05066 (PDF: https://export.arxiv.org/pdf/2504.05066) —
  Breden, Payan, Reisch, Tang, *Turing instability for nonlocal heterogeneous
  reaction-diffusion systems: a computer-assisted proof approach*
- https://arxiv.org/pdf/1704.03827 — Breden–Castelli, triangular cross-diffusion CAP
- https://imsc.uni-graz.at/btang/Publications.html

**On-topic, and it is the most dangerous citation in the whole pass.** This is Cadiot's
reference [15], the one he describes as deriving a generalized Gershgorin theorem "under
very broad assumptions ... whenever a linear operator is expressed on an adequate
Schauder basis". It is also the only paper located anywhere in this project that
**explicitly removes the nonzero-diagonal hypothesis** from the infinite-matrix
Gershgorin theorem. Fetched and read at full text. See "What this pass settles".

### Q3
`Farid Lancaster "Spectral properties of diagonally dominant infinite matrices" II Linear Algebra Appl 143 1991 hypotheses theorem`

- https://resolve.cambridge.org/core/journals/proceedings-of-the-royal-society-of-edinburgh-section-a-mathematics/article/spectral-properties-of-diagonally-dominant-infinite-matrices-part-i/5173389FF4863FD6FCADB6C21271C2FD — Part I
- https://ftp.math.utah.edu/pub/tex/bib/toc/linala1990.html — LAA vol. 143 table of contents, confirming Part II pp. 7–17 (1991)
- https://arxiv.org/pdf/2104.13204 — generalized diagonally dominant matrices, eigenvalue inclusion regions
- https://en.wikipedia.org/wiki/Diagonally_dominant_matrix

**On-topic; primary text not reachable (paywalled, no arXiv copy).** This is Cadiot's
reference [24] — the theorem his Lemma 3.2 actually invokes. Search level establishes
only that it concerns *diagonally dominant, unbounded, infinite matrix operators on
`ℓ^p`*. **I did not read it, and I do not classify from that.** Its hypotheses are
instead recorded from a source that states them and that I did read at full text —
Breden et al. arXiv:2504.05066 §2.1, which quotes and criticises them. That secondary
route is flagged as such in the ledger rather than presented as a primary reading.

### Q4
`Cadiot Blanco "2D Gray-Scott system" constructive proofs existence localized stationary patterns arXiv`

- https://arxiv.org/abs/2404.08529 (PDF: https://arxiv.org/pdf/2404.08529) —
  Cadiot & Blanco, *The 2D Gray–Scott system of equations*
- https://iopscience.iop.org/article/10.1088/1361-6544/adbcf0 — the Nonlinearity version
- https://arxiv.org/pdf/2509.17099 — localized patterns and saddle nodes, 1D activator–inhibitor

**On-topic.** This is Cadiot's reference [20], the **systems** extension — the only
route by which the framework acquires a genuinely matrix-valued symbol, i.e. the only
place an off-diagonal entry can appear in the *linear* part at all. Fetched and read at
full text for its Assumption 1.

### Q5
`computer-assisted proof Gershgorin zero diagonal unbounded off-diagonal variable coefficient transport operator Fourier tail estimate does not decay`

- https://arxiv.org/pdf/2302.12877 — CLN (already in the ledger)
- https://arxiv.org/pdf/2505.03091 — the target paper (already in the ledger)
- https://arxiv.org/pdf/2509.17099 — 1D activator–inhibitor localized patterns
- https://arxiv.org/html/2509.16693 — suspension bridge traveling waves
- https://arxiv.org/pdf/2507.09021 — pseudospectral rigorous estimation of transfer-operator resonances
- https://arxiv.org/pdf/1605.07239 — optimizing Gershgorin for symmetric matrices
- https://aalexan3.math.ncsu.edu/articles/gershgorin-report.pdf , http://buzzard.ups.edu/courses/2007spring/projects/brakkenthal-paper.pdf — expository Gershgorin notes

**Nothing on-topic that is not already in the ledger.** The query is deliberately
phrased in the exact terms of NG's hypothesis and it returns the ledger's own rows. The
one unfamiliar hit, 2507.09021, is a transfer-operator resonance paper — a
pseudospectral enclosure of a *compact-ish* operator's resonances, no unbounded
off-diagonal part. Recorded so a later pass does not re-chase it.

### Q6
`radii polynomial approach linearization unbounded part not a Fourier multiplier variable coefficient advection approximate inverse tail 2026`

- https://arxiv.org/html/2512.12019 — robust series linearization of nonlinear advection–diffusion equations
- https://arxiv.org/html/2502.18317v1 — polynomial approximation to the inverse of a large matrix
- https://link.springer.com/article/10.1007/s10208-024-09671-w — infinite-dimensional banded matrix factorizations
- https://arxiv.org/pdf/2410.11467 — `L^∞` stability for wave propagation, Fourier multipliers

**Nothing on-topic.** 2512.12019 is a formal series construction, not a certificate;
2502.18317 and the FoCM banded-factorization paper are numerical linear algebra without
an unbounded part. Recorded because the *resemblance* of "banded infinite matrix
factorization" to BDL's LU tail is the kind of thing that gets mistaken for prior art;
it is not — it presumes bandedness with a controlled diagonal, same as everything else.

---

## What this pass settles

**The gate is answered NO, and it is answered from full text, not from search.** Cadiot
arXiv:2505.03091 does **not** cover an operator whose unbounded part is off-diagonal
with a non-decaying tail inverse, and contains no positive result contradicting NG. The
exclusion is not incidental — it is the paper's defining hypothesis, stated three ways:

* **Assumption 1** requires the unbounded part to be a **Fourier multiplier**, i.e.
  exactly diagonal in the Fourier basis, *and* bounded below: `|l(ξ) ≥ l_min > 0`.
* The unbounded part's diagonality is **load-bearing in a proof**, not just an ambient
  convenience: Lemma 3.3's proof turns on "since `L` is diagonal, we have `Lπ_N = π_N L
  π_N`", which is what removes `L` from the off-diagonal Gershgorin radii and leaves
  only the bounded `DG(U_0)` there.
* The rest of the operator is assumed **relatively compact with respect to `L`**. A
  transport term of the same order as the unbounded part is not.

The verbatim quotes, with section numbers, go into `solver/certificate_shapes.py`'s
ledger, which is the artifact — not this file.

**The one thing this pass found that CAPS NG in a direction NG will not expect.**
Breden–Payan–Reisch–Tang arXiv:2504.05066 §2.1 states, of the classical infinite-matrix
Gershgorin theorem [FL91]: *"some of the assumptions of [FL91, Theorem 2.1] are
needlessly restrictive (for instance, all the diagonal elements of `L` have to be
nonzero)"* — and their replacement Theorem 2.6 drops that hypothesis entirely, requiring
only a Schauder basis, a sup-attaining property, and a compact resolvent. **So a no-go
phrased as "the published Gershgorin machinery requires a nonzero diagonal" is FALSE
against a 2025 paper.** The abstract theorem applies to a zero diagonal; it simply
returns disks of infinite radius and says nothing. NG's proposition must be phrased
*quantitatively* — about the ordering of growth rates — not as a structural
prohibition. This is a real constraint on NG's wording and it is reported to NG directly.

**What is left genuinely open, and therefore claimable by NG against this paper.** No
located source covers the case where the off-diagonal row-sum growth rate **exceeds**
the diagonal growth rate. Every construction read here requires the opposite ordering,
and Breden et al. make the requirement explicit and quantitative (`p − q_1 < 2/n`).
Our object sits on the wrong side of that inequality by a full order. That is the gap,
and it is now confirmed at full-text depth for the paper most likely to have closed it.

**What no search can do here, and what replaced it.** Every query above is search-level
evidence, which this project has ruled insufficient six times. The gate was answered
from the **full texts** of arXiv:2505.03091, arXiv:2504.05066, arXiv:2404.08529 and
arXiv:2302.12877, each fetched via `Papers/fetch.sh` and each classification traced to a
located statement. FL91 is the one link in the chain read only at second hand, and the
ledger says so on its own row rather than burying it.
