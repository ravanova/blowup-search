# Leg 69 — Route-IA v1: stress-testing the shared interval core

**Branch** `leg/ia-v1`. **Exploration leg, CLAIM-BEARING** (soundness of shared infrastructure).
**Gate: NO — stop-the-line.** Branch pushed; **not merged to `main`**, per the gate's `no` branch.

---

## Order of work (the discipline, as executed)

1. `plan_of_record.py` — read. `NG` is NEXT. Every live ban noted; the two that bind this leg
   are *no further ℓ¹-Fourier or collocation machinery for this operator before NG's gate
   answers* (this leg builds none — it tests arithmetic that already exists) and *no Route-D
   bound sharpening* (this leg sharpens nothing; it does not touch a bound). Also observed:
   *build nothing without grepping `capabilities.py` first* — done, entry at line 113.
2. `DIRECTION.md` — **has no leg 69 entry.** Grepped for `69`, `leg-69` and `Route-IA`: nothing.
   The thesis and the verbatim gate came from the dispatch prompt instead. **Flagged for the
   orchestrator**, as leg 57 flagged the same absence.
3. **Novelty pass FIRST**, committed before any construction (`writeup/novelty/leg_69.md`),
   five queries, **links not counts**.
4. Then: runner, curated data, stress gates, technical note.

## What the novelty pass changed about the leg

It converted a vague instruction into a prediction. Q3 located Rump's underflow-aware
restatement of the summation/dot-product error bound (BIT 2012), which carries an explicit **η**
term that the classic `γ_m` form does not. That named the *specific missing term* in
`solver/interval.py` before a single case was run, and it told the leg to **split the corpus into
a normal-range verdict and a subnormal-range verdict** — because the two have completely
different standing. A normal-range miss would be a defect with no literature excuse; a
subnormal-range miss is a documented hypothesis of the published algorithm that our code does not
enforce. Without that split the leg would have reported one undifferentiated "NO" and buried the
only number that matters.

It also pre-emptively removed any novelty claim: both defects found are documented limitations of
Dekker's and ORO's algorithms. This leg claims none of them as a discovery.

## What was actually measured

14,036 cases, every one decided against **exact rational** ground truth (`Fraction` on exact
float64 inputs — containment is decided exactly, not numerically). Catastrophic cancellation is
manufactured by appending the double-double head/tail of a row's exact dot product as two extra
exact-float columns, which drives the exact answer to ~1e-32 *relative* to the row's absolute
mass while keeping every stored number exactly representable — that is what keeps the ground
truth exact.

* **Normal range — 12,356 cases, 0 false negatives.** Accumulation lengths 32 to 260 (the
  certificate's own K range, bordered), input scales 1e-100 to 1e100, and the **live**
  zero-diagonal operator `spectral_certificate.bordered_linearization(K)` at K = 16…128. Worst
  relative slack `+5.06e-20`; **no case even touched an endpoint**.
* **Subnormal range — 1,680 cases, 62 false negatives.** Both `dot2_matvec` (43) and the
  uncompensated `matvec` (19) — so this is *not* confined to the compensated path. The failure
  is a **band**, not a tail: 0/60 at 1e-145, then 15/60, 21/60, 7/60 at 1e-150/-155/-160, then
  0/60 again from 1e-165 down. Worst escape **6.58 η = 3.25e-323**, i.e. **absolute**, not
  relative.
* **Second defect, separate mechanism.** Dekker's splitting overflows at **|entry| ≥ 2^997 =
  1.34e300**; `dot2_matvec` then returns `[nan, nan]` and **raises nothing**, because
  `Interval.__init__`'s `np.any(lo > hi)` guard is vacuous on NaN.

## The number that decides severity

The live operators both legs feed to `dot2_matvec` have nonzero entries spanning **0.5 to 128**
at every K in 16…128 — **≈140 decades above the subnormal band and ≈298 decades below the Dekker
wall**. Combined with the escape being *absolute* and capped at ~7 η, that is the measured reason
neither defect can reach a certificate number produced by legs 58 or 61. It is an argument from
measured operator magnitudes, and it holds only while those entries stay O(1).

## What was deliberately NOT done

* `solver/interval.py` was **not** modified, under any reading of the gate. Read-only.
* The branch was **not** merged to `main`.
* `capabilities.py`'s over-broad "validated" line was **not** narrowed — outside territory. The
  recommended replacement text is in the technical note.
* No figure. Audit leg, and the two magnitudes that matter (the onset band and the 140-decade
  separation) are both single numbers that a plot would dilute rather than clarify.

## Lesson offered

The `capabilities.py` "validated" line said *"containment holds on adversarial cases"* with no
range attached, and the corpus behind it topped out at a 6×4 matrix and a 4-term accumulation
while the consumers had grown to 258-term accumulations. **A validation claim without a stated
range of validity is not auditable** — it cannot be falsified, so it silently stops tracking the
code it certifies. Every `validated` entry should carry the regime it was measured in.
