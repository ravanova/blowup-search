# VERIFY 268 — independent review of Route-PUB2R (leg 268, `3f6d5d0`)

**Verdict: NOT a clean confirmation.** Five of leg 268's six checkable claims hold exactly as
stated and at full precision. Its **clause-4 claim — "the escalation clause did not fire" — does
not hold as a claim about PUB2**, because the check behind it keyed on the literal string
`4.026` rather than on the property. **Three untouched sites assert truncation-independence**,
two of which now directly contradict sentences leg 268 itself wrote into the same two files.
This is a wording/consistency finding on a submission-track document, not a numerical error:
every number leg 268 printed is supported. Nothing was repaired here.

---

## 1. What checks out, at full strength

### 1.1 Leg 176's banked JSON is untouched — 0 bytes

`writeup/data/p2_route_h2c_v1_construction.json` has blob hash `ecf8e685d33d7879fd52b1486ef6406f387aca4a`
at **both** `3f6d5d0^` and `3f6d5d0`; `git diff` on that path across the leg is **0 bytes**;
size **12892 bytes**. Stronger than claimed: `git log` on that path returns **exactly one
commit ever** — `bb0f184` (leg 176). It has never been rewritten by anyone.

### 1.2 The correction artifact transcribes leg 249 exactly

Both certified figures were pulled independently from `leg/249-h2cv2-v2`
(`git ls-remote` confirms the head is `e9db984b809da0feff7ce148ae8e7d839daba05a`, the exact
commit the artifact cites) and match character for character, not rounded or paraphrased:

| quantity | leg 249 (`experiments/journal/leg_249.md` L200 / L222) | leg 268's artifact | |
|---|---|---|---|
| `σ_min` enclosure | `(0.090804094, 0.090804194)`, open | `[0.090804094, 0.090804194]` + `certified_enclosure_is_open_interval: true` | ✅ |
| `‖T⁻¹‖_X` bracket | `[4.026239930769523, 4.026241551830974]` | identical, all 16 digits | ✅ |

Twelve further transcriptions were checked against leg 249's own banked
`writeup/data/p2_route_h2cv_v1_postconstruction.json` on that branch and all match to every
digit: `0.09080414383680567` (Cholesky at N=512), `4.026240741300086` (independent tail inverse
norm), `0.24837652731703622` (banked tail `σ_min`), `0.24803101644034442` (extrapolated limit),
`5.08e−07`, the error ladder `8.3e−13 → 3.8e−10`, `7.1×`, `6.74e−16`, `N = 2048`, the decrement
ratios `0.510 / 0.527 / 0.534`.

### 1.3 The printed magnitudes are recomputable and honest

Recomputed from the ladders, not taken on trust:

| printed | independently computed | note |
|---|---|---|
| `0.865 %` rise, `N = 64…1024` | `(4.028864−3.994032)/4.028864 = 0.8646 %` | relative to the last rung, matching leg 249's own convention |
| understates limit by `0.14 %` | `(4.0318−4.026241)/4.0318 = 0.1379 %` | ✅ |
| `0.139 %` over the 16-fold range | `(0.0909310−0.090804)/0.0909310 = 0.1397 %`; banked `relative_spread = 1.3899e−03` | ✅ |
| `0.0920 %` over `N = 64…512` | `0.0920 %` against the certified `0.09080414`; `0.0922 %` against the printed `0.090804` | see nit E |
| "finite limit near `4.032`" | leg 249's `4.0318` | correct rounding, not a tightening |

The `N = 512` cell drop `0.0908047 → 0.090804` correctly retreats to the six figures leg 249
says are supported, and the new footnote states the *proof* (pencil not positive definite at
that `λ`) rather than a re-measurement, which is the right strength.

### 1.4 Leg 176's gate answer and `capabilities.py`

`experiments/journal/leg_176.md` and `writeup/novelty/leg_176.md` are both last-touched by
`bb0f184` — untouched by leg 268 as claimed. `capabilities.py`'s single relevant row
(`solver/origin_h2_certificate.py`, "Route-H2C, leg 176", L91–L100) names the
`range-untruncated sigma_min diagnostic` as a capability but **records no numeric value at all**
— neither of the two proved-wrong figures appears there, so there is nothing to correct.
Repo-wide, `4.02614534796022` and `0.09080465147034879` occur in exactly the banked JSON, the
new correction artifact, and leg 268's own journal.

### 1.5 Territory

Diff `3f6d5d0^..3f6d5d0` is exactly the five declared files, 330 insertions / 11 deletions,
nothing else.

---

## 2. The gap: clause 4 was tested on a string, not on the property

Leg 268's clause-4 evidence is that `4.026` occurs at exactly one site. That is true. But
truncation-independence is asserted at **three further sites that never mention `4.026`**, and
leg 268's own edits now contradict two of them.

### A. `BLOG_P2_PUB2_V1.md` L65–67 — a direct self-contradiction, 42 lines apart

> "The quantity that collapsed in the sequence space is here bounded away from zero and,
> **crucially, independent of the truncation** — it moves by `1.4e−04` when we widen the
> computational window by four decades."

Leg 268's own new text at L108 of the same file:

> "one descriptor we had attached to the tail piece — that its value is *independent* of the
> truncation — is simply false."

Two further defects in that one sentence: the word "crucially" makes it load-bearing rather
than incidental, and the justification is a **computational-window** spread offered as evidence
of **truncation** independence — which is precisely the conflation leg 268 diagnosed for the
same number (`1.44e−04`) at TECHNICAL §5(3) and fixed **there only**. Mitigating: L65 sits in
the pre-construction drafting layer (L82 opens "Since this was drafted, we went and built it"),
and the post-build paragraph at L88–89 is honest. But the sentence is not marked superseded, and
leg 268 edited L104 of the same document.

### B. `TECHNICAL_P2_PUB2_V1.md` L201 — §3.2's contrast table, row "truncation dependence"

| | `ℓ¹_w` (§2) | origin-`H²` (§3) |
|---|---|---|
| truncation dependence | none available — `σ_min` has no truncation-independent value at all | ratio spread **1.444e−04** across four added decades of window (`n_quad` 600→1400, window `1e−4…1e+4` → `1e−6…1e+6`) |

The row label says *truncation*; the cell contents are a *quadrature window* sweep. Read against
its own left-hand cell the row asserts that origin-`H²` **does** have a truncation-independent
`σ_min`, at the `1e−4` level — an order of magnitude tighter than the ladder's own measured
relative spread of `1.39e−03`, and the claim §3.5 now withdraws. Leg 268's correction artifact
records "section 3.2 provenance note: unchanged (it already disclosed the round-up)" — §3.2 was
inspected for the 259 round-up nit only, and this row was not seen.

### C. `TECHNICAL_P2_PUB2_V1.md` L353–354 — the load-bearing one

> "There, leg 127 showed the operator itself had no truncation-independent `σ_min`, so `Z₁ ≥ 1`
> for *every* bounded `A`. **Here the operator does have one**, so the failure is of the
> block-diagonal shape of `A`, not of the operator and not of the space."

This carries what leg 176 calls "its most useful output" and propagates into §5(1) and §6. It
states a truncation-independent `σ_min` as a fact, 30 lines before leg 268's own retained
sentence at L383:

> "What does not survive, and **is not written anywhere in this note**, is any claim to a
> *proved* floor."

L383 is now literally false because of L354. This is the **same defect class leg 268 did fix**
at §3.1's conjunct-table cell ("no longer presents a floor 3.5 withdraws") — applied there and
not here. In fairness on substance: leg 249's own summary endorses leg 176's conclusion that
"`σ_min` is bounded away from zero uniformly in the truncation", and leg 249's `truncation-independent`
verdict is aimed at the *tail* `‖T⁻¹‖_X`, not at `σ_min`. So this is an overstatement and an
internal contradiction, not a demonstrated falsehood.

### D. `TECHNICAL_P2_PUB2_V1.md` L629–631 — the two ceilings now disagree

The technical §7 still reads "carried as a **single leg's own measurements** — its commissioned
verification leg has committed only a novelty pass and **has returned no verdict**", while the
blog's ceiling was edited by leg 268 to "The independent check has since reported: it confirms
both halves by exact-rational re-derivation". Whatever the right resolution (leg 249 is not
formally leg 192), the two companion documents now state opposite things about the same fact.

### E. Nit — the provenance of `1.44e−04`

Leg 268 relabels it "quadrature-window spread". Traced: it is
`G4…resolution_ladder_spread = 0.000144433514507325` in leg 163's
`p2_route_h2s_v1_scoping.json` (parked), i.e. the spread of leg 163's **three-datum**
bordered-solve ratio across a quadrature-resolution ladder. The relabel is a real improvement
over "truncation-independent to 1.44e−04". But the new §5(3) sentence attaches leg 163's
three-datum quantity to **leg 176's `σ_min` ladder** ("…and no proved floor anywhere in it"),
which is a cross-leg attachment. Note also that leg 176's own banked
`spread_over_reliable_window` is `1.2639e−04`, a different number for a different thing.

### F. Nit — `0.0920 %` at L379

Computed against the certified `0.09080414`, not against the `0.090804` printed two lines
earlier in the same sentence, which gives `0.0922 %`. Defensible (it is closer to the truth) but
the sentence quotes `0.090804` as its own input.

---

## 3. Recommendation

A rework leg owning PUB2's territory should fix A, B, C and D. A and C are the ones that
matter: each contradicts a sentence in leg 268's own corrected text, in a document headed for
submission. Nothing in §2's list requires re-running any computation — leg 249's data already
support every replacement, and leg 268's correction artifact is a correct and complete carrier
for them.

**Ceiling.** This pass verified transcription, arithmetic, territory and internal consistency.
It re-derived nothing about the operator, ran no solver, and moved no link of the `L1 → L4`
chain. Clay odds unchanged at ~0.05 %. No ban lifted, no GA compute.
