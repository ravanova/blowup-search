# Leg 62 — Route-CP novelty pass (run BEFORE construction)

**Date:** 2026-08-06. **Agent:** LEG-B. **Branch:** `leg/cp-v1`.
**Verdict: `PROCEED_AS_BOOKKEEPING`.** This leg settles the *scope of somebody else's paper*.
It claims **no mathematical novelty of its own** and must not be written up as a result. What it
produces is a located, executable scope record — the kind of artifact that does not decay at the
rate of memory (lesson 68) — plus one magnitude measured against the paper's own example.

Per `writeup/novelty/README.md`: **links, not counts.** Every query string below is verbatim,
every link returned that I judged on-topic is listed, and where a search returned nothing
on-topic I say so instead of reporting a number.

---

## What is under test

Leg 57 flagged Cadiot arXiv:2505.03091 as independently stating the dominance-hypothesis
observation, and the standing ban ("re-claiming leg 51's methodological finding at full
strength") now rests entirely on that flag, with the lift condition written into
`plan_of_record.py` verbatim:

> *lifted by: never — unless a pass resolves whether Cadiot's construction covers a zero
> diagonal, which is now the live open question, not BDL's*

So this pass is not asking "is our observation new?" — leg 57 already answered that (it is
folklore in print, `PROCEED_AS_BOOKKEEPING`). It asks the two questions that the ban's lift
condition actually turns on:

* **(N1)** Does Cadiot arXiv:2505.03091, **at full text**, cover an operator whose unbounded
  part is **off-diagonal** with a **non-decaying tail inverse** — i.e. does it already contain
  leg 58's no-go, or a positive result contradicting it?
* **(N2)** Does anything **Cadiot cites forward into this case** — the papers building on
  2505.03091's framework — relax the hypothesis in that direction?

**This is NOT leg 58's question.** Leg 58 (`leg/ng-v1`, running in parallel) asks whether the
no-go admits a *proof* for a class of `A` larger than block-diagonal. This leg asks only what
Cadiot's paper *covers*, settled from the PDF, and its answer caps leg 58's claim strength
without gating leg 58's work. Nothing below depends on leg 58's result.

---

## Primary source, fetched not searched

`bash Papers/fetch.sh 2505.03091` — egress probe HTTP 200, fetched on the first attempt,
1004 KB, 30 pages, extracted with `pypdf` (`pdftotext` is not installed in this container;
`solver/viscous_novelty.py` already depends on `pypdf`, so this is the repo's own second
extraction path, not a new one).

* https://arxiv.org/abs/2505.03091 — Cadiot, *Stability analysis for localized solutions in PDEs
  and nonlocal equations on `R^m`*, 6 May 2025.

The located statements are transcribed into `solver/certificate_shapes.py`'s `SHAPE_LEDGER`
under tag `CADIOT_STAB`, each with its section number and the sentence verbatim, so the next
pass can check the quote rather than trust it. **Read those, not this summary.**

---

## Queries, verbatim, with the links returned

### Q1
`radii polynomial approach approximate inverse unbounded off-diagonal linear part vanishing diagonal computer-assisted proof`

- https://link.springer.com/article/10.1007/s00332-016-9298-5 — (un)stable manifolds with validated error bounds
- https://arxiv.org/pdf/2404.08529 — 2D Gray–Scott, localized stationary patterns (Cadiot–Blanco)
- https://www.researchgate.net/publication/274384127 — "Rigorous numerics for analytic solutions of DEs: the radii polynomial approach"
- https://arxiv.org/pdf/2605.07500 — Shimizu–Morioka heteroclinic CAP case study
- https://arxiv.org/pdf/2509.17099 — 1D activator–inhibitor localized patterns and saddle nodes
- https://arxiv.org/pdf/2604.08715 — 1D Thomas model localized patterns
- https://arxiv.org/pdf/2605.03920 — **Linear instability of a Burgers–Hilbert traveling wave**
- https://arxiv.org/pdf/1702.07412 — homoclinic continuation, suspension bridge equation
- https://arxiv.org/pdf/2004.14830 — validated stable manifolds for parabolic PDEs
- https://www.math.mcgill.ca/jplessard/ODEs_files/final_draft.pdf — radii polynomial approach (Lessard)

**On-topic for N1:** none — this query returns the multiplier-shaped corpus again, which is the
same corpus leg 57 already classified. **One new candidate surfaced for the ledger:**
arXiv:2605.03920 (Burgers–Hilbert), read at full text below because its unbounded part *is* a
transport term.

### Q2
`Cadiot "Stability analysis for localized solutions" arXiv 2505.03091 citations`

- https://arxiv.org/abs/2505.03091 — the paper itself
- https://arxiv.org/pdf/2509.17099 — Blanco, Cadiot, Fassler, *Proving the existence of localized
  patterns and saddle node bifurcations in 1D activator-inhibitor type models* — **cites
  2505.03091 as [19]** (confirmed in its bibliography, not inferred from the search snippet)
- https://arxiv.org/pdf/2509.16693 — van der Aalst, Cadiot, *Existence proofs of traveling wave
  solutions on an infinite strip for the suspension bridge equation and proof of orbital
  stability* — **cites 2505.03091 as [4]** (likewise confirmed in the bibliography)
- https://arxiv.org/list/math.AP/2025-05 — arXiv listing, not a citation
- https://arxiv.org/abs/2504.20880 — off-topic

**On-topic for N2:** the two Cadiot-coauthored papers. Both fetched and read at full text (below).

### Q3
`computer-assisted proof "zero diagonal" OR "vanishing diagonal" infinite matrix approximate inverse tail estimate transport operator self-similar blowup`

- https://par.nsf.gov/servlets/purl/10284939 — Elgindi–Jeong, stable self-similar blow-up for nonlocal transport equations
- https://www.researchgate.net/publication/333773639 — same, preprint record
- https://www.researchgate.net/publication/393102788 — Chen–Hou, 3D Euler with smooth data and boundary
- https://arxiv.org/html/2308.01528v3 — exact self-similar finite-time blowup of the Hou–Luo model

**On-topic:** none for the *method* question. Every hit is a blow-up-construction paper; none
forms an infinite tail estimate against an off-diagonal unbounded part. The Chen–Hou row already
in `SHAPE_LEDGER` covers this family and records *why* (they extract damping from the advection
instead of inverting it). **Nothing published on the zero-diagonal tail estimate was found.**

### Q4
`Farid Lancaster "diagonally dominant infinite matrices" Gershgorin generalization hypotheses zero diagonal`

- https://resolve.cambridge.org/core/journals/proceedings-of-the-royal-society-of-edinburgh-section-a-mathematics/article/spectral-properties-of-diagonally-dominant-infinite-matrices-part-i/5173389FF4863FD6FCADB6C21271C2FD — Farid–Lancaster Part I
- https://www.sciencedirect.com/science/article/pii/S002437951100365X — notes on matrices with diagonally dominant properties
- https://www.researchgate.net/publication/38347239 — block diagonally dominant matrices and Gershgorin generalizations
- https://en.wikipedia.org/wiki/Diagonally_dominant_matrix — background only
- https://www.sciencedirect.com/science/article/pii/S0024379521002950 — generalized diagonal dominance and D-stability

**On-topic, with a scope note.** Farid–Lancaster (1991) Part II is Cadiot's reference [24], the
engine behind his generalized Gershgorin theorem. It is paywalled (Elsevier, LAA 143:7–17) and
**was not obtained**. It did not need to be: the three hypotheses Cadiot's Lemma 3.2 verifies
before invoking it are reproduced *in his own proof*, verbatim, and the load-bearing one is the
shifted diagonal-dominance inequality quoted in the ledger. That is a located statement in a
source we do hold. **Recorded as not-obtained rather than glossed** — leg 53's failure mode was
presenting a source it had not read as if it had.

---

## The two forward citations, read at full text

Both were fetched (`curl` from arxiv.org, HTTP 200) and extracted with `pypdf`. Neither relaxes
the hypothesis; **both restate it, and one of them closes the systems loophole explicitly.**

* **arXiv:2509.17099** (Blanco–Cadiot–Fassler, 51 pp.) — its **Assumption 1** reads, verbatim:
  *"Given `l` as in (5), assume there exists `sigma_0 > 0` such that `|det(l(xi))| >= sigma_0`
  for all `xi` in `R`. That is, `det(l(xi))` is bounded away uniformly from 0."* This is the
  **systems** form of Cadiot's Assumption 1, and it is the one that matters here: a *system* is
  the only route by which an off-diagonal entry enters this framework at all, and the systems
  hypothesis is a **non-vanishing determinant of the matrix symbol**. Their Lemma 2.1 then gives
  explicit parameter inequalities under which `l` is invertible — i.e. the hypothesis is
  something they must *check*, not something they can drop.
* **arXiv:2509.16693** (van der Aalst–Cadiot, 31 pp.) — establishes an explicit positive lower
  bound on its own symbol (`l(xi_1, xi_2) >= (2 pi xi_2)^2 c^2 + 1 - c^4/4`, or
  `(2 pi xi_2)^4 + 1`, by cases). Same hypothesis, discharged by direct computation.

**Neither is a counterexample, and neither is a near miss.** The forward closure of 2505.03091
into this case tightens the requirement rather than loosening it.

## One independent candidate, read and classified

**arXiv:2605.03920** (Castro, Gómez-Serrano, Pascual-Caballo, *Linear instability of a
Burgers–Hilbert traveling wave*, 104 pp.) surfaced in Q1 and is the strongest off-diagonal
candidate the search produced: the Burgers–Hilbert linearization's unbounded part **is** a
transport term. It is **not** a counterexample, and it does **not** cite 2505.03091 (its only
Cadiot reference is the Whitham paper, [16]). Its own method section places radii polynomials in
the work of *others* ("In a broader context ... the reduction of the proof of existence to a
fixed-point argument has also been particularly successful in the context of radii polynomials,
developed in [7, 34, 45] and later used in [6, 19]") and proceeds by Fuchsian ODE theory,
reducing to a **finite-dimensional** system solved in interval arithmetic. It is the Chen–Hou
pattern again — the shift case certified by *abandoning* the tail estimate rather than repairing
it — on the torus rather than the line. Entered in `SHAPE_LEDGER` as `BH` for exactly that
reason: **a second, independent instance of the confirmation, from a different community.**

---

## What this pass settles, and what it forbids

**Settles (N1):** No. Cadiot's Assumption 1 requires `|l(xi)| >= l_min > 0` **and**
`|l(xi)| -> +infinity`; his `L` is a Fourier multiplier, hence diagonal by construction; and his
Lemma 3.1 / Lemma 3.2 proofs *use* both halves. The off-diagonal, non-decaying-tail-inverse case
is outside the paper on three independent clauses, not one.

**Settles (N2):** No. Both forward citations restate the hypothesis, and the systems version is
`|det(l)| >= sigma_0 > 0`.

**Forbids.** This leg may bank the located hypotheses as an executable ledger entry and nothing
else. In particular it may **not**:

* claim any mathematical novelty — the observation is folklore in print (leg 57's finding, which
  stands unchanged);
* be read as evidence *for* leg 58's proposition — a gap in one paper is not a theorem, and leg
  58's own gate is a separate question this leg does not touch;
* be read as lifting the "re-claiming leg 51's finding at full strength" ban. That ban's lift
  condition names the *question*, and answering it does not by itself discharge the ban — leg 57
  recommended keeping the ban and this pass supplies no reason to reverse that. The correct
  bookkeeping change is a **narrowing annotation**, integration-owned, not a lift claimed here.
