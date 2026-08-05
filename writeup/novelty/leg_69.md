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

---
---

# TECHNICAL NOTE — Route-IA v1: the shared interval core fails in the subnormal range

*This section is the leg's required technical note. It is carried here rather than in a separate
`writeup/4_p2_lottery/TECHNICAL_P2_ROUTEIA_V1.md` because the leg's declared file territory does
not include that path; the quartet permits either location. **The orchestrator should promote it
to a standalone TECHNICAL document if it wants leg 58 and leg 61 to cite it directly.***

## Gate, verbatim, and the answer

> "Under a harder adversarial corpus (larger matrices matched to the certificate's own K range,
> near-singular conditioning matched to the tail block's near-zero diagonal, and subnormal-range
> inputs), does the rigorous bound still provably dominate the exact rational value on every
> sampled case — zero false negatives?"

**NO — 62 false negatives in 14,036 sampled cases.** All 62 lie in the subnormal-input family.
The normal-range families, which are the ones matched to the certificate's actual sizes and
conditioning, returned **0 false negatives in 12,356 cases**.

Per the gate's `no` branch this is reported as a stop-the-line finding, `solver/interval.py` was
**not** modified under this leg's authority, and this branch is **not** merged to `main`.

## Method

Ground truth is exact. Every input is exact float64 data, so `fractions.Fraction` reproduces the
real answer of each sum, dot product and matvec with no error whatsoever; containment is decided
by exact rational comparison, never numerically. Catastrophic cancellation is manufactured
without leaving exact data: the head/tail `(h, l)` of a row's exact rational dot product are
themselves exact floats, so appending columns `(-h, -l)` against unit entries drives the exact
answer to ~1e-32 *relative* to the row's absolute mass while every stored number stays exactly
representable.

Reported magnitudes, per case:

* **relative slack** `min(x − lo, hi − x) / (hi − lo)` — 0.5 is dead centre, 0 is touching an
  endpoint, negative is a false negative;
* **absolute escape** `|x − nearest endpoint| / η`, with `η = 2^-1074` the smallest positive
  subnormal (Rump's underflow unit).

The absolute escape is the number that decides severity: it says whether the defect is
*relative* — which would scale into the certificate's own regime — or *absolute*, which cannot.

## Results

| family | cases | false negatives | worst relative slack | worst escape |
|---|---|---|---|---|
| `elementary_ops` (+, −, ×, ÷, reciprocal; 1e-320…1e300) | 6772 | 0 | +5.06e-20 | — |
| `isum_cancellation` (m = 32…258) | 240 | 0 | +0.4931 | — |
| `matvec_point_and_box` (n×m to 8×260, box corners) | 720 | 0 | +1.74e-12 | — |
| `dot2_normal_range` (m = 32…258, scales 1e-100…1e100) | 720 | 0 | +0.4991 | — |
| `tail_block_conditioning` (LIVE operator, K = 16…128) | 3904 | 0 | +0.4764 | — |
| **`dot2_subnormal_range`** (scales 1e-120…1e-185) | 840 | **43** | **−0.8223** | **6.58 η** |
| **`matvec_subnormal_range`** (same band) | 840 | **19** | **−0.9756** | **3.90 η** |

Zero of the 12,356 normal-range cases so much as *touched* an endpoint — every one is a strict
enclosure. The 416 cases carrying an unbounded endpoint are elementary divisions across the
subnormal boundary (a reciprocal of a subnormal overflows to `inf`); they are counted separately
and are vacuously true, so they neither flatter nor damage the slack statistic.

### Finding 1 — the subnormal band, and it is a BAND, not a tail

The failure onset is sharp and, crucially, **bounded on both sides**:

| input scale | 1e-140 | 1e-145 | **1e-150** | **1e-155** | **1e-160** | 1e-165 | 1e-170 |
|---|---|---|---|---|---|---|---|
| false negatives / 60 | 0 | 0 | **15** | **21** | **7** | 0 | 0 |

The band is where the *products* `M_ij v_j` straddle the normal/subnormal boundary (min normal
2.2e-308, η = 4.9e-324). Above it the arithmetic is normal and both bounds hold. Below it
everything flushes to zero and the module's one-ulp outward push happens to cover, so containment
returns — by luck, not by argument.

**Mechanism.** The ORO bound `dot2_matvec` implements, `u|x·y| + γ_m²|x|·|y|`, is purely
*relative*: with `|x|·|y| ~ 1e-300`, the term `γ_m²|x|·|y| ~ 1e-28 × 1e-300 = 1e-328` is itself
below η and rounds to zero, while the residual accumulation `s = s + (q + r)` is by then rounding
in the subnormal range where the error is *absolute*, a few η. The classic `γ_m` bound behind
the uncompensated `matvec` fails for the same reason — which is why `matvec` fails too, and this
is **not** a defect confined to the compensated path. This is exactly the gap Rump's
underflow-aware restatement (BIT Numer. Math. 2012, https://www.tuhh.de/ti3/paper/rump/Ru11.pdf)
closes by carrying an explicit η term; Q3 of the novelty pass above located it *before*
construction, and the measurement then confirmed it at the predicted place.

**Worst observed case**, reproduced verbatim from the data file (`scale = 1e-155`):
enclosure `[3.5e-323, 7.4e-323]`, exact rational value below `1e-323` — the enclosure is
*strictly positive* and the answer is essentially zero. Escape 6.58 η = 3.25e-323.

**Why this does not reach legs 58 and 61.** The escape is *absolute*, capped at ~6.6 η ≈ 3e-323,
and no measured case exceeded 7 η. The live operator both legs feed to `dot2_matvec` —
`spectral_certificate.bordered_linearization(K)` — has nonzero entries spanning **0.5 to 128**
at every K in 16…128. That is **≈140 decades above the failure band**. For the defect to touch a
certificate number, the operator entries would have to fall by 150 orders of magnitude.

### Finding 2 — a silent NaN at the other end (not a containment miss)

`_two_product` multiplies by Dekker's splitting constant `2^27 + 1` *before* splitting, so it
overflows for large operands. Measured threshold: the error term stops being finite at
**|a| ≥ 2^997 = 1.34e300**. `dot2_matvec` then returns `[nan, nan]` and **raises nothing** — the
`Interval` constructor's `np.any(lo > hi)` guard is vacuously satisfied by NaN, so an
unusable enclosure propagates silently. Operationally this is the more dangerous of the two
defects, because a false negative at least *is* a value one can test, whereas a NaN enclosure
passes every `lo <= x <= hi` check written with comparison operators. The live operators sit
**≈298 decades below** this wall.

## What is and is not claimed

* **Claimed, and measured:** in the regime the certificate stack actually occupies — accumulation
  lengths 32 to 260, the live zero-diagonal bordered linearization at K up to 128, input scales
  1e-100 to 1e100, rows cancelled to ~1e-32 relative — the interval core returned **0 false
  negatives in 12,356 exact-rational checks**, with worst-case relative slack `+5.06e-20` and no
  case touching an endpoint. This is a genuinely stronger, size-matched validation footprint than
  the 6×4 corpus that `capabilities.py`'s "validated" line rests on.
* **Claimed, and measured:** two soundness defects exist outside that regime, characterized above
  with their exact thresholds and escape magnitudes.
* **NOT claimed:** any novelty. Both defects are documented hypotheses of the published
  algorithms (see Q2 and Q3 above), not discoveries. What is new is only that *this repository's
  implementation does not enforce them, and nothing in the repository said so.*
* **NOT claimed:** that legs 58 or 61 produced a wrong number. Nothing here shows that. The
  measured 140-decade separation is evidence they did not — but that is an argument from measured
  operator magnitudes, and it holds only for operators whose entries stay O(1).

## Recommended disposition (for the orchestrator, not executed here)

1. `capabilities.py`'s "validated" line for `solver/interval.py` should be **narrowed** to state
   the range of validity, e.g. *"containment holds on adversarial cases at accumulation lengths
   up to 260 and entry magnitudes in [1e-100, 1e100]; UNSOUND in the subnormal band and silently
   NaN above 2^997"*. That edit is outside this leg's territory and was not made.
2. The repair, when a leg is authorised to make it, is small and standard: add Rump's absolute η
   term to `_gamma`-based radii in `isum`/`matvec`/`dot2_matvec`, and guard `_two_product`
   against the splitting overflow (or raise instead of returning NaN).
3. `test_interval_stress.py` pins both defects as **characterization tests that currently pass**.
   When the repair lands they will start failing, which is the intended signal to flip them into
   soundness assertions. They must not be weakened to make a repair look unnecessary.
