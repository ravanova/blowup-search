# Leg 87 — Route-IVB novelty pass (run BEFORE construction)

**Date:** 2026-08-05/06. **Agent:** LEG-G. **Branch:** `leg/ivb-v1`.

**Verdict: `PROCEED_AS_AUDIT`.** This leg builds no new mathematics and claims no novel
mechanism. It is an *independent* post-repair regression check of `solver/interval.py` — the
shared interval primitive under legs 58 and 61 — re-running leg 69's original adversarial corpus
against the repaired module and adding a fresh battery. Everything it can find is either
(a) a defect in *our* code, or (b) a confirmation of a documented floating-point hazard. Neither
is a discovery, and nothing below is claimed as one.

Per `writeup/novelty/README.md`: **links, not counts.** Query strings verbatim; every on-topic
link listed.

---

## What is being checked for prior art

Leg 69's pass established that both defects it found are documented limitations of Dekker's and
ORO's algorithms. That much is settled and is not re-litigated here. This pass asks the *next*
question, which is the one a post-repair check actually needs answered:

* **(N1)** The repair's central invented quantity is the **sizing of the absolute η term** —
  `_ETA_TERMS_PLAIN = 2.0` and `_ETA_TERMS_DOT2 = 8.0` per accumulated term. Is there a
  **published bound with an explicit η coefficient** to check those two constants against?
  Leg 69's pass located Rump BIT 2012 but recorded the theorem text as *"located but not
  verbatim-verified"* (its PDF fetch returned an encoded stream). Closing that gap is this
  pass's job.
* **(N2)** Is the subnormal failure correctly *attributed*? Leg 69 and the repair both describe
  it as "Dekker's TwoProduct is error-free only in the normal range". Is the **splitting** what
  fails under underflow, or something else?
* **(N3)** The Dekker overflow wall: is `2^997` and the *remedy* for it in print, and is
  "raise" the published remedy?
* **(N4)** The NaN repair widens a NaN endpoint to `[-inf, +inf]`. What does the **interval
  arithmetic standard** prescribe for an out-of-domain / invalid result?
* **(N5)** Is "conformance/adversarial corpus for an interval library, checked against exact
  ground truth" an established method — i.e. is this leg's *method* standard?

---

## Queries, verbatim, with the links returned

### Q1
`Rump 2012 BIT error estimation floating-point summation dot product underflow eta term constant 5 eta TwoProduct`

- https://www.tuhh.de/ti3/paper/rump/Ru11.pdf — Rump, *Error estimation of floating-point
  summation and dot product*, BIT Numer. Math. 52:201–220, 2012. **Fetched and read as text this
  time** (`pdftotext`), unlike leg 69's attempt.
- https://link.springer.com/article/10.1007/s10543-011-0342-4 — publisher record for the same.
- https://www.researchgate.net/publication/227009772_Error_estimation_of_floating-point_summation_and_dot_product — mirror.
- https://link.springer.com/article/10.1007/s00211-023-01370-y — precision-aware deterministic and
  probabilistic summation bounds (Higham/Ipsen school); adjacent, does not carry the η term in the
  form needed here.
- https://epubs.siam.org/doi/abs/10.1137/120894488 — Jeannerod–Rump, *Improved Error Bounds for
  Inner Products*; sharpens the *relative* constant, not the absolute one.
- https://www.cambridge.org/core/journals/acta-numerica/article/floatingpoint-arithmetic/287C4D5F6D4A43FBEEB1ABED2A405AAF — Boldo–Jeannerod–Melquiond–Muller, Acta Numerica survey.

**On-topic finding for (N1) — the sharpest result of this pass, and it is now VERBATIM.**
Rump §2 fixes the notation this repository already uses: *"The relative rounding error unit … is
denoted by u, and the underflow unit by eta, that is the smallest positive (subnormal)
floating-point number. For IEEE 754 double precision (binary64) we have u = 2−53 and eta =
2−1074."* Theorem 4.3 then states, for the recursive dot product of `x, y ∈ F^n` with
`(n+2)u ≤ 1`:

> `| s̃n − xᵀy | < (n + 2)u · ufp(S̃n) + n·eta/2 < (n + 2)u · ufp(S̃n) + realmin`

So the published absolute underflow coefficient for the **plain** dot product is **n·η/2, i.e.
0.5 η per accumulated term.** `solver/interval.py` carries **2.0 η per term** on the plain path —
a **4× margin over the published constant**, not an under-estimate. Remark 6 is the licence for
the term existing at all: *"It is not possible to avoid some additive term covering underflow in
(4.2) since all |xi yi| may be so small that s̃n = S̃n = 0 but xᵀy ≠ 0."* That is leg 69's
subnormal defect stated in print, four years before it was measured here.

Two further points that shape the battery rather than the write-up. Remark 7 — *"Floating-point
operations with quantities in the underflow range (such as n·eta/2) are often very time consuming,
so that for computational purposes the underflow terms are better estimated by realmin"* — is why
a published-quality implementation may look *different* from ours without being *sounder*; ours
uses the tight n·η form, which is the one that must be checked empirically. And Rump's bound is
for the **plain** recursion; it does **not** cover the compensated (Dot2) path, whose η
coefficient of **8.0** therefore has **no published bound behind it at all** and rests on ORO
2005's `a·b = p + e + 5η·θ` remark plus the repair's own margin argument. **That constant is the
one unbacked number in the repair, and the fresh battery is aimed squarely at it.**

### Q2
`Dekker splitting overflow 2^996 threshold scaling remedy TwoProduct veltkamp split spurious overflow`

- https://members.loria.fr/PZimmermann/papers/split.pdf — Jeannerod–Muller–Zimmermann, *On various
  ways to split a floating-point number* (ARITH). **Fetched and read as text.**
- https://perso.ens-lyon.fr/jean-michel.muller/slides-split.pdf — the talk version.
- https://link.springer.com/chapter/10.1007/11814771_6 and
  https://www.semanticscholar.org/paper/Pitfalls-of-a-Full-Floating-Point-Proof:-Example-on-Boldo/028bf82e3f806159f92e378f52c8cb1ea0cc1721
  — Boldo, *Pitfalls of a Full Floating-Point Proof: … Veltkamp/Dekker Algorithms*.
- https://www.academia.edu/82573915/Alternative_Split_Functions_and_Dekker_s_Product — alternative
  split functions.
- https://carolomeetsbarolo.wordpress.com/2012/02/13/the-veltkamp-dekker-route-to-extended-precision/ — expository.

**On-topic finding for (N2), and it CORRECTS a phrase both leg 69 and the repair comment use.**
Jeannerod–Muller–Zimmermann on Veltkamp's splitting: *"Note that the algorithm works correctly
even in the presence of underflows (due to the special shape of C and since underflowing additions
are exact …)."* The **splitting is underflow-safe**. What fails in the subnormal range is not the
split but the **product** `p = fl(a·b)`, whose rounding error stops being representable once
`a·b` itself is subnormal — so `a·b = p + err` ceases to be exact. The repair's η term is
therefore in the right place (an absolute term on the accumulation) for a reason slightly
different from the one its comment gives. This is a **documentation nuance, not a soundness
issue**, and is recorded as such; it is *not* grounds to touch `solver/interval.py`, which this
leg may not edit under any outcome.

**On-topic finding for (N3).** Same paper: *"If |x| is large, then an overflow can occur in the
first line of both Algorithms 3 and 5."* And Boldo's result, quoted there: *"if Cx does not
overflow, then no other operation will overflow"* — which is exactly why guarding the **first**
multiplication (`_SPLIT * a`) is the right and sufficient guard point, and why the wall sits at
`2^997` (the largest `e` with `(2^27+1)·2^e` finite). The published **remedy** is *scaling*
(*"it suffices for instance to replace φ by …"*), **not** raising. The repair chose to raise.
That is a legitimate, conservative scope decision for a module that must never return an
unsound enclosure — refusing to answer is sound; scaling would be *better*, and is a possible
future bench item, not a defect. No claim of novelty attaches either way.

### Q3
`IEEE 1788-2015 interval arithmetic NaN endpoint NaI entire interval decoration fail closed`

- https://inria.hal.science/hal-01559955/document and
  https://link.springer.com/chapter/10.1007/978-3-319-63501-9_2 — Revol, *Introduction to the
  IEEE 1788-2015 Standard for Interval Arithmetic*.
- https://standards.ieee.org/ieee/1788/4431/ — the standard itself.
- https://onlinelibrary.wiley.com/doi/10.1002/cpe.7856?af=R — Benet et al., *A framework to test
  interval arithmetic libraries and their IEEE 1788-2015 compliance*, CCPE 2024.

**On-topic finding for (N4).** IEEE 1788-2015's set-based flavor *"chose to return results even
when encountering out-of-domain values (instead of returning invalid values similar to NaN),
while providing users with a means to check whether the computation encountered such values"* —
the **decoration** (`com, dac, def, trv, ill`). The repair's "widen a NaN endpoint to
`[-inf, +inf]`" is the *return-a-valid-result* half of the standard's answer and is sound. It
does **not** carry the other half: a widened-from-NaN interval is indistinguishable from a
genuinely computed entire interval, i.e. the `trv`/`ill` decoration is lost. **Recorded as a
scope limitation of the repair, measurable and worth measuring** (the battery includes a case
that exercises it), not as a soundness defect and not as a licence to edit the module.

### Q4
`regression test suite verified computing library after soundness bug fix independent re-verification adversarial corpus`

- https://onlinelibrary.wiley.com/doi/10.1002/cpe.7856?af=R — Benet et al. (again): the standard
  *method* — a conformance/adversarial test corpus for interval libraries — is established
  practice.
- https://arxiv.org/pdf/2305.06970 — automated regression test for scientific computing libraries
  (SPHinXsys).
- https://arxiv.org/html/2605.22368v1 — VeriScale, adversarial test-suite scaling.
- https://arxiv.org/pdf/2601.16239 — combining tests and proofs.
- https://arxiv.org/html/2511.16004 — InfCode, adversarial refinement of tests and patches.
- Nothing on-topic for `solver/interval.py` specifically, which is unsurprising: it is this
  repository's own module.

**On-topic finding for (N5).** The method is standard and is claimed as such. The one piece of
methodology worth naming explicitly, because it is what makes this leg *independent* rather than
a re-run: the repair agent's own report rests on "18 gates bit-identical pre/post". This leg
reconstructs a **pre-repair module in memory** from the current source (η constants zeroed, the
overflow raise and the NaN widening neutered) and diffs **endpoint bit patterns** against the
repaired module on live-range data — re-deriving the inertness claim from the source itself
rather than accepting the report. That is a differential-testing pattern, also standard
(Benet et al. use VM-differential conformance for the same purpose).

---

## What this pass changed about the leg, before construction

1. **It gave the battery a target.** N1 says the plain-path constant `2.0 η/term` has a published
   bound behind it (Rump's `0.5 η/term`, 4× margin) and the compensated-path constant
   `8.0 η/term` **does not**. So the fresh battery is not a generic widening of leg 69's scales —
   it is aimed at *empirically bounding the true absolute error of `dot2_matvec` in the subnormal
   band*, in units of η per term, and comparing it to 8.
2. **It told the leg where the attribution is loose** (N2): the split is underflow-safe, the
   product is not. Recorded, not patched.
3. **It named a real, published scope limitation of the repair** (N3 scaling vs raising, N4 lost
   decoration) so that neither gets mistaken for a defect nor silently omitted.
4. **It pre-empts every novelty claim.** Nothing this leg can find is new mathematics. A defect
   would be a defect in our code against bounds already in print; a clean result is a
   confirmation. The leg claims **no** novelty.
