# Leg 59 novelty pass — Route-WV: is the weight fitness's admissibility wall 2-D?

Run BEFORE construction (branch `leg/wv-v1`, 2026-08-05). Links, not counts. This
leg's object: the boundary in *weight-parameter space* across which a
Newton–Kantorovich / radii-polynomial argument stops closing because the
approximate inverse stops contracting in that norm (`Z_1 >= 1`) — and whether that
boundary is a half-plane in the single far-field power `p+q` (leg 49/50's model) or
a genuinely two-dimensional region in the two factor powers of
`nu(X) = (1+(X/L)^2)^(p/2) (1+(X/l)^2)^(q/2)`.

## What was searched

Queries run (Aug 2026): admissible region / radii polynomial / two-parameter weight;
algebraic weight + weighted ell^1 + Newton–Kantorovich + tuning the weight exponent;
sweep of the weight parameter nu and where the contraction bound crosses one;
Chen–Hou's own multi-power weight (sec 5.3.3 of arXiv:2210.07191).

## Precedents found, and why none pre-empts

- **Chen–Hou, [arXiv:2210.07191](https://arxiv.org/abs/2210.07191) sec 5.3.3** (and
  Part II, [arXiv:2305.05660](https://arxiv.org/abs/2305.05660)) — the closest source
  in this repository's own library, and already carried in
  `solver/weight_search.py::PRECEDENTS`. They use a weight "consisting of different
  powers", i.e. exactly the two-factor algebraic family this leg models, and they
  choose it BY HAND in a documented order. What they do not publish is the
  *admissible set* of the two powers: no boundary is measured, so there is nothing
  here that says whether it is a half-plane in the sum or a 2-D region.
  Verdict: ADJACENT, and it is the reason no originality is claimed for the weight
  FAMILY.
- **A posteriori validation of generalized polynomial chaos expansions,
  [arXiv:2203.02404](https://arxiv.org/pdf/2203.02404)** — weighted ell^1 with a
  single geometric decay parameter nu, and the usual remark that nu must be picked so
  the bounds close. One parameter, one wall; the question of a 2-D wall does not
  arise. Verdict: ADJACENT.
- **Contraction analysis of nonlinear DAE systems,
  [arXiv:1702.07421](https://arxiv.org/pdf/1702.07421)** — states the general form of
  the problem explicitly (infinitely many admissible weight matrices; which choice
  gives the least conservative bound is the open practical question), but for
  contraction metrics of a DAE flow, not for the norm of a Newton–Kantorovich
  argument, and with no measured boundary. Verdict: ADJACENT — and the most
  honest statement of why this is a search problem at all.
- **Cadiot [arXiv:2505.03091](https://arxiv.org/abs/2505.03091)** — carried in this
  repository's ban list as the live open question about zero-diagonal dominance
  hypotheses. It concerns the operator's structure, not the weight-parameter
  admissible set. Verdict: ADJACENT, unchanged by this leg.
- **[arXiv:2506.18908](https://arxiv.org/pdf/2506.18908)** ("admissible weights",
  left-invariant weights of polynomial growth on groups) — same words, different
  subject: which weights make a Banach algebra, not which weights make a computer
  -assisted contraction close. Verdict: NOT RELEVANT.

## Verdict carried into construction

No source found states the admissible weight-parameter set of a radii-polynomial
argument as a measured region, in any dimension. The claim this leg may make is
therefore narrow and it is a MEASUREMENT, not a theorem: on one known-answer object
(the a=0 CLM linearisation, closed form since CLM 1985) and in FLOAT, how much of the
observed `Z_1 >= 1` failure set a 1-D wall in `p+q` explains versus a 2-D wall in both
factors. Nothing here is claimed about CLM, about Hou–Luo, or about any certificate.

Standing ceiling: this leg re-runs a FROZEN gate. Repairing the wall model is allowed;
moving a threshold is not.
