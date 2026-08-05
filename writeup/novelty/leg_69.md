# Leg 69 — Route-IA novelty pass (run BEFORE construction)

**Date:** 2026-08-05. **Agent:** LEG-G. **Branch:** `leg/ia-v1`.
**Verdict: `PROCEED_AS_AUDIT`.** This leg builds no new mathematics and claims no novel
mechanism. It stress-tests `solver/interval.py` — the shared primitive under legs 58 and 61 —
against exact rational ground truth. The pass below exists to establish, *before* construction,
which failure modes are **already documented in print**, so that anything this leg finds is
reported as *"a known floating-point hazard, present in our code"* and never as a discovery.

Per `writeup/novelty/README.md` and the lesson from leg 53: **links, not counts.** Every query
string below is verbatim, and every link returned that I judged on-topic is listed. Where a
search returned nothing on-topic I say so rather than reporting a number.

---

## What is being checked for prior art

The module under test rests on three imported results. The pass asks, for each, **what
hypotheses the published statement carries** — because a hypothesis the code does not enforce is
exactly where a soundness gap would live.

* **(N1)** Ogita–Rump–Oishi `Dot2`: the bound `|res − x·y| ≤ u|x·y| + γ_m² |x|·|y|`, which
  `dot2_matvec` implements verbatim. **Under what assumption on underflow/overflow is it
  stated?**
* **(N2)** Dekker's `TwoProduct` (the `_two_product` splitting): is its *error-free* property
  known to fail in the subnormal range?
* **(N3)** The classic `γ_m = mu/(1−mu)` accumulation bound used by `isum`/`matvec`: is the
  standard form valid under underflow, or does the underflow-safe form carry an extra absolute
  term?
* **(N4)** Is "simulate directed rounding with one `nextafter` push" a recognised, sound
  discipline, and is it known to interact badly with subnormals?
* **(N5)** Is there an established practice of validating an interval library against exact
  rational / higher-precision ground truth on an adversarial corpus — i.e. is the *method* of
  this leg standard?

---

## Queries, verbatim, with the links returned

### Q1
`Ogita Rump Oishi accurate sum and dot product error bound underflow assumption TwoProduct`

- https://www.tuhh.de/ti3/paper/rump/OgRuOi05.pdf — Ogita–Rump–Oishi, *Accurate Sum and Dot
  Product*, SIAM J. Sci. Comput. 26(6):1955–1988, 2005. The source of the `Dot2` bound the module
  implements.
- https://ogilab.w.waseda.jp/ogita/math/doc/2005_OgRuOi.pdf — author-hosted copy of the same.
- https://epubs.siam.org/doi/10.1137/030601818 — publisher record.
- https://epubs.siam.org/doi/10.1137/070679946 — Castaldo–Whaley–Chronopoulos, superblock dot
  product; a different accuracy family, listed because it shares the error-bound framing.
- https://www.mdpi.com/2227-7390/13/2/270 — ARMv8 implementation of the same algorithms.

**On-topic finding for (N1).** The paper's standing assumption is *no overflow*, with underflow
**permitted for the summation transformation** (`TwoSum` is exact under underflow because
floating-point addition/subtraction is). That permission does **not** extend to `TwoProduct`.
I could not extract verbatim theorem text from the PDF (the fetch returned an unreadable encoded
stream), so this is recorded as **located but not verbatim-verified** — flagged as such below.

### Q2
`Dekker TwoProduct error-free transformation fails underflow subnormal exactness condition`

- https://arxiv.org/pdf/2602.19452 — *Dekker's floating point number system and compensated
  summation algorithms*; treats subnormals explicitly and notes that earlier work commonly
  neglects them.
- https://arxiv.org/pdf/1808.10387 — compensated de Casteljau in K-fold precision; states that
  error-free transformations do not apply outside the normal range and do not attempt to handle
  overflow/underflow.
- https://www.tuhh.de/ti3/paper/rump/Ru06d.pdf — Rump, *Error bounds for extremely
  ill-conditioned problems*.
- https://arxiv.org/pdf/cs/0610122 — Graillat–Langlois–Louvet, faithful polynomial evaluation
  with compensated Horner; same EFT toolkit, same normal-range premise.
- https://arxiv.org/pdf/1603.00491 — *Wanted: Floating-Point Add Round-off Error instruction*.
- https://arxiv.org/pdf/2604.06258, https://arxiv.org/pdf/2602.15965 — adjacent, retained for
  the record.

**On-topic finding for (N2).** The failure of `TwoProduct`'s exactness once the product enters
the subnormal range is **explicitly in print** and is treated as a known limitation of the EFT
toolkit, not as a subtlety. Anything this leg measures there is a *confirmation*, not a finding.

### Q3
`Rump error estimation floating-point summation dot product underflow verified rigorous bound eta term`

- https://www.tuhh.de/ti3/paper/rump/Ru11.pdf — Rump, *Error estimation of floating-point
  summation and dot product*, BIT Numer. Math., 2012.
- https://link.springer.com/article/10.1007/s10543-011-0342-4 — publisher record for the same.
- https://link.springer.com/article/10.1007/s00211-023-01370-y and
  https://arxiv.org/pdf/2203.15928 — Higham/Ipsen-school precision-aware deterministic and
  probabilistic summation bounds.
- https://www.researchgate.net/publication/228568591_Error-free_transformations_in_real_and_complex_floating_point_arithmetic — Graillat et al.

**On-topic finding for (N3), and the sharpest one in this pass.** Rump's BIT paper is exactly
the underflow-aware restatement: it introduces the **underflow unit η** (smallest positive
subnormal, `2^-1074` in binary64) alongside `u`, and its bounds are asserted to hold **in the
presence of underflow** *because* they carry an η term. The standard `γ_m`-only form the module
uses carries no such term. So the literature's own underflow-safe bound is strictly larger than
the one implemented here, and the difference is an **absolute** term that no relative bound and
no one-ulp push can recover once the terms are small enough. This is the precise shape of the
hole the construction will probe.

### Q4
`interval arithmetic outward rounding nextafter one ulp simulated directed rounding soundness subnormal`

- https://www.sciencedirect.com/science/article/pii/S0010448597000869 and
  https://www.researchgate.net/publication/222474683_Efficient_and_reliable_methods_for_rounded-interval_arithmetic — Hu et al., efficient and reliable rounded-interval arithmetic; the
  standard reference for the "widen each endpoint by one ulp" discipline the module uses.
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8005885 — patent, encoded
  rounding control to emulate directed rounding.
- Modal-interval-processor patents (7949700, 8849881, 9588736) — returned, off-topic for
  soundness, listed for completeness.

**On-topic finding for (N4).** The one-ulp-outward discipline is standard and sound *as a cover
for the ≤0.5 ulp rounding of a single correctly-rounded operation*. Nothing returned claims it
covers an **accumulated** error, and nothing claims it covers underflow. Consistent with the
module's own docstring, which is careful about exactly this.

### Q5
`testing validating interval arithmetic library soundness adversarial test corpus exact rational ground truth computer-assisted proof`

- https://arxiv.org/pdf/2307.06953 — *A framework to test interval arithmetic libraries and their
  IEEE 1788-2015 compliance*.
- https://arxiv.org/pdf/2205.11837 — *Testing interval arithmetic libraries, including their
  IEEE-1788 compliance*; notes that despite the 2015 standard, little attention has gone to how
  such testing should be done, and releases a JSON corpus of hard-to-round cases.
- https://arxiv.org/pdf/2003.10623 — *Computer-Assisted Verification of Four Interval Arithmetic
  Operators* (Why3 + back-end provers; validity, soundness, tightness).
- https://arxiv.org/pdf/2107.05784 — an interval arithmetic for robust error estimation.
- https://en.wikipedia.org/wiki/INTLAB — the reference implementation this module deliberately
  does not depend on.

**On-topic finding for (N5).** The *method* of this leg — an adversarial corpus checked against
exact ground truth, emitted as machine-readable data — is standard practice with published
precedent. It is not novel and this leg will not present it as such. The published corpora are
element-wise operator corpora; none of them is size- or conditioning-matched to a *particular*
certificate stack, which is the only sense in which this leg's artifact is specific.

---

## What this pass actually settles

1. **No novelty is available to this leg and none will be claimed.** Every mechanism that could
   break `solver/interval.py` at the subnormal end is in print, in some cases as an explicit
   stated limitation of the algorithm the module implements.
2. **It sharpens the construction.** Q3 turns a vague "test subnormals" instruction into a
   specific predicted defect with a named missing term (Rump's η). The corpus will be built to
   separate a **normal-range** verdict from an **underflow-range** verdict, because the two have
   completely different standing: a normal-range miss would be a defect with no literature
   excuse, whereas an underflow-range miss is a documented hypothesis the code does not enforce.
3. **One item is located but not verbatim-verified** and is recorded rather than papered over
   (leg 56's `ilog` gap set the precedent): the exact hypothesis text of ORO's `Dot2` theorem was
   not extracted, only its assumption structure from secondary summaries. The leg does not rest
   any conclusion on the verbatim wording — the measurement against exact rationals is
   self-contained and needs no appeal to the paper.
