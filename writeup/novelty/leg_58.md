# Leg 58 — Route-NG novelty pass (NG-0, run and committed BEFORE construction)

**Date:** 2026-08-06. **Slot:** LEG-A (critical path, stage `NG`). **Branch:** `leg/ng-v1`.
**Verdict: `PROCEED_NARROW`.** Cadiot arXiv:2505.03091 is resolved against *this* no-go from
the full text and it does **not** contain it — its standing hypothesis is that the linear part
is a **Fourier multiplier with a symbol bounded away from zero**, which is the exact hypothesis
this operator fails. Nothing found states an obstruction/lower-bound result for the approximate
inverse in a radii-polynomial certificate. What may be claimed is narrow and is written into
`NG-1`'s scope line: the *class* of the failure is not novel as an observation (leg 57 already
established the dominance hypothesis is folklore-in-print, and Cadiot restates it), so the only
thing this leg may claim is **the inequality and the class it holds on**, not the observation.

Per `writeup/novelty/README.md` and the standing rule since leg 53: **links, not counts.** Every
query string below is verbatim; every returned link I judged on-topic is listed. Where a search
returned nothing on-topic I say so instead of reporting a number.

---

## The two claims under test

* **(N1) THE SCOPE QUESTION THE PLAN NAMES.** Does Cadiot arXiv:2505.03091's construction cover
  an operator whose unbounded part is **off-diagonal** (a shift) with a **singular tail block**
  (zero diagonal, non-decaying bordered tail inverse) — i.e. does it already contain this no-go,
  or a positive result that contradicts it?
* **(N2) THE OBSTRUCTION QUESTION THIS LEG ACTUALLY ADDS.** Is there, in print, a **lower bound
  on `‖I − AL‖`** — a statement that *no* approximate inverse in some named class can make the
  radii-polynomial `Z₁` less than one — for an operator whose tail block has a kernel? This is
  the shape of `NG-1`/`NG-2`'s proposition and is a different question from N1.

Leg 62 (Route-CP) is settling N1 independently and from the full PDF; this pass is run
regardless, per the `NG-0`-first rule, and its N1 finding is recorded here as **this leg's own**
so that the two can be cross-checked rather than folded together. **If leg 62's full-PDF pass
disagrees with the reading below, leg 62's reading governs** — it reads at greater depth by
assignment, and `NG`'s claim is capped by it either way.

---

## Queries, verbatim, with the links returned

### Q1 — the paper itself, primary source
`https://arxiv.org/abs/2505.03091` (abstract page), then the **full text**
`https://arxiv.org/html/2505.03091`

- https://arxiv.org/abs/2505.03091 — Matthieu Cadiot (McGill), *"Stability analysis for
  localized solutions in PDEs and nonlocal equations on ℝ^m"*, submitted 6 May 2025.
- https://arxiv.org/html/2505.03091 — full text, the version actually read for the hypotheses
  below.

**Located hypotheses, recorded as read from the full text (N1):**

> "𝕃 is the linear part of 𝔽 and 𝔾 is the nonlinear counterpart… 𝕃 is a **Fourier multiplier
> operator**, that is it is given by its symbol `l : ℝ^m → ℂ` as `ℱ(𝕃u)(ξ) = l(ξ) ℱ(u)(ξ)`"

> "assume that there exists `l_min > 0` such that **`|l(ξ)| ≥ l_min` for all `ξ ∈ ℝ^m`** and
> `lim_{|ξ|₂ → +∞} |l(ξ)| = +∞`"

> "the operator 𝕃 becomes an **infinite diagonal matrix** `L_q` with entries `(l(n/2q))_{n∈ℤ^m}`
> on the diagonal"

**Reading.** All three are the multiplier hypothesis, stated three ways: diagonal in the
spectral basis, symbol bounded **below** away from zero, symbol growing at infinity. The
operator this leg treats has a tail block whose **diagonal is exactly zero** (banked in
`capabilities.py` for `solver/spectral_certificate.py`) and whose unbounded part is a **shift**,
so it satisfies none of the three. **N1 answer: NO** — Cadiot does not cover this case, and
carries no positive result that contradicts the no-go. What Cadiot *does* do, and what keeps the
ban on re-claiming leg 51's methodological finding at full strength standing, is state the
dominance hypothesis explicitly and in print — which is why `NG` may not claim the *observation*
as new, only the inequality.

### Q2
`Cadiot arXiv:2505.03091 computer-assisted proof approximate inverse`

- https://arxiv.org/abs/2505.03091 — the paper (as above).
- https://arxiv.org/list/math.AP/2025-05?skip=25&show=500 — listing page, no content.
- https://arxiv.org/pdf/2411.18361 — Validated matrix-multiplication transform for orthogonal
  polynomials. **On-topic, and already banked at leg 54**: states the block-diagonal convention
  `A = A^N + π^∞` and justifies it by `DF` being a *compact perturbation of the identity*.
  Another statement of the same hypothesis; still not this case.
- https://arxiv.org/abs/2605.07500, https://arxiv.org/html/2605.07500 — Shimizu–Morioka
  heteroclinic CAP case study. Multiplier/ODE setting; not on-topic for N1 or N2.
- https://arxiv.org/html/2509.16693 — suspension-bridge travelling waves on an infinite strip,
  existence **and orbital stability**. Same Cadiot-family machinery, same multiplier hypothesis.
- https://arxiv.org/pdf/1203.3766, https://arxiv.org/abs/1605.09503 — off-topic (Choptuik
  spacetime; a statistics inverse problem). Listed for auditability.

### Q3
`no-go obstruction radii polynomial certificate lower bound Z1 approximate inverse cannot close singular tail block`

Returned complexity-theory "certificate complexity" papers (https://arxiv.org/abs/1402.5078 and
similar), a low-degree-polynomial workshop report, and unrelated numerics. **Nothing on-topic
for N2.** The collision is lexical: "certificate" and "lower bound" mean something else in that
literature.

### Q4
`Newton-Kantorovich validated numerics negative result approximate inverse necessarily fails operator with nontrivial kernel in tail`

- https://arxiv.org/pdf/2507.16798 — heteroclinic loops to homoclinic snaking, rigorous forcing
  through CAPs. Uses the standard construction; no obstruction statement.
- https://arxiv.org/pdf/1910.00759 — Nakao-school "new formulation for the numerical proof of
  the existence of solutions to elliptic problems". **The nearest genre**: it reformulates to
  *avoid* a badly-conditioned linearisation, i.e. it is a repair, not an obstruction, and the
  operator is elliptic (multiplier-like) throughout.
- Remaining returns (Kantorovich kernel neural operators, sampling-Kantorovich saturation,
  inverse source problems) are name collisions on "Kantorovich". **Nothing on-topic for N2.**

### Q5
`"radii polynomial" OR "Newton-Kantorovich" computer-assisted proof obstruction theorem "no approximate inverse" lower bound contraction constant`

- https://arxiv.org/pdf/2604.08715 — 1D Thomas model localized patterns.
- https://arxiv.org/pdf/2404.08529 — 2D Gray–Scott localized stationary patterns.
- https://arxiv.org/pdf/2509.17099 — 1D activator–inhibitor localized patterns and saddle nodes.
- https://arxiv.org/pdf/2405.12446 — transverse heteroclinics by the parameterization method.
- https://arxiv.org/html/2608.01579 — computer-assisted **counterexample** to the planar Pompeiu
  and Schiffer conjectures. On-topic *as genre* (a CAP used to prove a negative), but the
  negative is about the PDE's spectrum, not about the certificate machinery's own reach.
- https://www.math.mcgill.ca/jplessard/Publications_files/piecewise_smooth.pdf — rigorous
  numerics for piecewise-smooth systems.

Every one of these **uses** an approximate inverse and reports the `Z₁` it achieved. **None
states a lower bound on `Z₁`, and none names a class of `A` over which closure is impossible.**
Nothing on-topic for N2.

### Q6
`preconditioner lower bound "I - AL" cannot be less than one singular block Schur complement kernel far-field rank-one correction`

- https://arxiv.org/abs/2002.00917, https://www-users.cse.umn.edu/~saad/PDF/ys-2021-02.pdf —
  power Schur-complement low-rank correction preconditioners.
- https://www-users.cse.umn.edu/~saad/PDF/ys-2017-02.pdf, https://arxiv.org/pdf/1505.04341,
  https://arxiv.org/pdf/2205.03224 — hierarchical / algebraic-domain-decomposition low-rank
  Schur preconditioners.
- https://arxiv.org/pdf/2111.13483 — near-field Schur complement preconditioner for EFIE.
- https://arxiv.org/pdf/2409.16477 — inexact block preconditioning for weak-Galerkin Stokes.

**On-topic as prior art for the *shapes*, not for the obstruction.** This is the numerical-linear-
algebra literature the shape battery draws on, and it confirms leg 54's `MM0` reading: block
Gauss–Seidel, Schur complement and low-rank/rank-one correction are **textbook preconditioning**.
Nothing in it is claimed as new here. What none of them do is the thing `NG-2` needs: derive a
**lower** bound on `‖I − AL‖` valid over a named class of `A` when the (2,2) block is singular.
Their low-rank corrections are all *repairs* (Sherman–Morrison–Woodbury), offered without a
statement of when the repair provably cannot work.

### Q7
`computer-assisted proof self-similar blowup De Gregorio CLM linearization approximate inverse bordered far field 2026`

- https://users.cms.caltech.edu/~hou/papers/DG_CPAM.pdf and
  https://arxiv.org/pdf/1905.06387 — Chen–Hou–Huang, De Gregorio blowup. Already banked.
- https://arxiv.org/pdf/2209.08232 — self-similar finite-time blowups of De Gregorio on the line.
- https://arxiv.org/html/2603.25104 — **generalized CLM self-similar blowups with singular
  profiles**, theoretical and numerical. Closest to the substrate; it is a *positive* study of
  profiles, not a certificate-machinery statement, and it does not construct an `ℓ¹`-Fourier
  approximate inverse for the `a = 0` linearisation.
- https://par.nsf.gov/servlets/purl/10434681 — asymptotic self-similar profile, 3D axisymmetric
  Euler.

None reports an approximate inverse for the `a = 0` CLM linearisation in a weighted `ℓ¹`
coefficient basis, and none reports a bordered far-field column. Nothing on-topic for N2.

---

## What this pass settles, and what it forbids

**Settled (N1).** Cadiot arXiv:2505.03091's hypotheses are located and recorded verbatim above:
Fourier multiplier, `|l(ξ)| ≥ l_min > 0`, `|l| → ∞`, tail an infinite diagonal matrix. The
operator here fails all three. **Cadiot does not contain this no-go and does not contradict it.**

**Settled (N2).** No located statement, in six independent query framings across the CAP
literature and the preconditioning literature, gives a **lower** bound on the radii-polynomial
`Z₁` over a class of approximate inverses. The genre is uniformly constructive: papers report the
`Z₁` they achieved, never a `Z₁` no admissible `A` can beat.

**Forbidden by this pass, and carried into `NG-1`'s scope line.**

1. **The observation is not novel and may not be claimed.** "The tail estimate presumes an
   asymptotically diagonal / dominant derivative" is in print — leg 57 established it, Cadiot
   restates it, arXiv:2411.18361 restates it again with a compactness justification. `NG` claims
   **only** the inequality and the class it holds on.
2. **The shapes are not novel.** Block Gauss–Seidel, Schur complement, rank-one/low-rank lift are
   textbook (Q6). Only their measurement in the `Z₁` slot is this repository's.
3. **No claim may be made about `HL_S2_nonsymmetric` or about any link of the L1→L4 chain.**
   The measured object is the `a = 0` CLM linearisation, whose `Y₀` is exactly zero for the
   degenerate reason banked since leg 51.
4. **Novelty is claimed against Cadiot and no further** — and if leg 62's full-PDF pass reads
   Cadiot differently, that reading caps this one.
