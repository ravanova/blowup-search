# Leg 57 — VERIFY pass on Route-XS v1 (`leg/xs-v1`, HEAD `04c20eb`)

**Agent:** VER-D. **Branch:** `verify/xs-v1-review`. **Date:** 2026-08-05.
**Verdict: SIGN OFF — merge `leg/xs-v1` as-is.** One minor citation defect (G1), which is a
mislabelled section number, not a wrong or invented statement. No claim in the PR depends on it.

This pass re-derived the numbers from scratch and read the source PDFs. It did not re-read
leg 57's prose and nod.

---

## 1. Territory discipline — CONFIRMED

`git diff --stat main leg/xs-v1` is exactly the 12 declared files, **+2440 / −0**. There is not
one deletion anywhere in the diff.

`git diff main -- capabilities.py` is strictly additive: a single 26-line block inserted between
the `literature_gates` and `bordered_hl` records. No existing entry is reordered, reworded or
removed. `writeup/build_figures.py` is a one-line append to `P2_EVIDENCE`.

## 2. The measured numbers — INDEPENDENTLY RE-DERIVED, BIT-FOR-BIT

The headline correction revises a number banked by legs 52–53, so I did not call leg 57's code.
I rebuilt the tail block, both null-vector recursions, and the bordered inverse from the stated
definition in a standalone script that imports nothing from `solver/`
(`(T h)_m = (1 − (m−1)/2) h_{m−1} + ((m+1)/2) h_{m+1}`, zero diagonal; flat weight ⇒ max column
abs-sum). Every value agrees to all printed digits:

| quantity | leg 57 / JSON | my independent value |
|---|---|---|
| bordered `‖B⁻¹‖`, K = 4, M = 1024 | 2.190835328396217 | 2.190835328 |
| bordered, K = 128 | 11.527648395372571 | 11.527648395 |
| K-exponent (last 4 rungs) | +0.4371818703216551 | +0.437181870 |
| ratio last/first | 5.261759405628761 | 5.261759406 |
| unbordered M-exponent, µ = 0 | +1.0209414058885984 | +1.020941406 |
| bordered M-exponent, µ = 0 | +0.023072261886396335 | +0.023072262 |
| µ = 0.25 K-exponent | −0.8487376848506958 | −0.848737685 |
| µ = 0.5 / 1.0 / 2.0 / 4.0 | −0.886 / −0.915 / −0.933 / −0.946 | −0.886379 / −0.915317 / −0.932695 / −0.945898 |

Intermediate rungs match too (3.233963781, 4.652886535, 6.530033796, 8.890152593; the M-ladders
17.14 / 35.43 / 72.00 / 145.14 / 291.43 unbordered and 3.0414 → 3.2496 bordered).

**The correction to legs 52–53 is real and it is leg 57's direction, not the reverse.** The
bordered tail inverse is not a constant: it rises monotonically 2.191 → 11.528 over K = 4…128 at
exponent +0.437, i.e. the standing "2.19 … 10.32" is the bottom of a rising ladder. The blog's
"one curve up, five curves down" is exactly what the dial produces.

Every quoted figure in BLOG and TECHNICAL that I could trace resolves to the curated JSON at the
stated precision, including the `WRONG_OPERATOR_CONTROL` values (1.06e+03, 2.06e+04, 8.26e+04)
which are correctly fenced as a construction that must never be quoted as a comparison.

## 3. The executable ledger — 15/15 CONFIRMED, and the gates are not proxies

`.venv/bin/python test_certificate_shapes.py` → **ALL GATES PASS (221 s), exit 0**, 15 named
gates. I read the implementations of tests 1, 4, 5, 7, 8, 11.

* `is_counterexample` is the literal three-clause conjunction the prose states — no weaker proxy.
* Test 5 is a genuine live-gate control (lesson 90): admitting the fictitious row flips the same
  predicate to `yes` with `counterexamples == ["SYNTHETIC_CONTROL"]`.
* Test 11 asserts both halves as magnitudes (`|M-exponent| < 0.1` **and** `K-exponent > 0.3`
  **and** `vals[-1] > 4·vals[0]`), not a boolean.
* Test 8 pins `CH.tail_inverse_decays is None` rather than `False` — the right distinction, since
  there is no tail inverse to speak of.

One structural note, not a defect: `unlocated_rows()` guards only against the *string* "abstract"
appearing in `where`. It cannot detect a **wrong section number**, which is precisely defect G1
below. The guard is necessary but not sufficient; the `url` field is what makes G1 findable.

## 4. The located statements — 10 of 11 CHECKED AGAINST THE SOURCE PDFs

I pulled the full texts (BDL 1503.06315, CLN 2302.12877, Chen–Hou I 2210.07191, Cadiot
2505.03091) and extracted them myself.

**BDL — 4/4 confirmed.**
* Intro/conclusion quote is **verbatim exact**, reference list included: *"In [3, 4, 6, 7, 9, 5],
  the nonlinear equations under study have asymptotically diagonal or block-diagonal dominant
  linear part, which helps a lot in the computation of approximate inverses. In contrast, the
  present work considers problems with tridiagonal dominant linear part. To the best of our
  knowledge, this is the first attempt to compute rigorously solutions of such problems."*
* Assumption (4): the paper reads *"Assume that there exist real numbers `s_L > 0`, `0 < C₁ ≤ C₂`
  and an integer `k₀`"* with the display giving `… ≤ C₂ and ∀ k ≥ k₀, C₁ ≤ |µ_k|/ω_k^{s_L}`.
  **Leg 57's `[RECONSTRUCTED]` flag is honest and accurate** — `pdftotext` really does emit that
  display with the fractions stacked and out of order, exactly as its transcription note
  describes. The load-bearing clause (a strictly positive lower bound on the **diagonal** `µ_k` at
  the growth rate `s_L`) is unambiguous in the extraction.
* Assumption (5): *"Assume further the existence of `δ ∈ (0, 1/2)` and `k₀ ≥ 0` such that
  `∀ k ≥ k₀, |λ_k/µ_k|, |β_k/µ_k| ≤ δ`."* Confirmed.
* Proposition 2.3: *"Assume that `m ≥ k₀` and `δ < ½`. Then `A` maps `Ω^s` into `Ω^{s+s_L}`."*
  **Verbatim exact.**

**CLN — 2/2 confirmed verbatim**, Assumption 2.1 and the §1 literature-review passage
(*"exploit the fact that the Fréchet derivatives are (asymptotically) diagonally dominant … a
tail operator (which is diagonal) which acts on the tail of the sequence"*). Both correctly
located; the ellipsis in leg 57's quote is honest.

**Chen–Hou — 2/2 confirmed verbatim**, and the negative claim verified independently: the strings
`radii polynomial`, `Kantorovi`, `approximate inverse`, `contraction mapping` return **0 hits** in
Part I. §2.7 is confirmed to be titled exactly *"The local parts and functional spaces"* and the
quote is exact. See G2 for the §2.6 label.

**Cadiot 2505.03091 — 2/2 present verbatim**, but see G1 for the location of the first.

## 5. The BDL zero-diagonal question — CLOSED, AS CLAIMED

The ban's lift condition ("unless a pass resolves whether BDL's construction covers a zero
diagonal") **is now factually resolved, and resolved negatively.** From the source:

* Assumption (4) requires `0 < C₁ ≤ |µ_k|/ω_k^{s_L}` for all `k ≥ k₀`. A zero diagonal violates
  this outright; `C₁` is explicitly strictly positive.
* Assumption (5) puts `µ_k` in a denominator, so at zero diagonal `δ` is not merely large, it is
  undefined — which is what `bdl_delta(0) = inf` encodes.
* Their future-work list asks to relax the **symmetry** in (5) and to extend to
  **block-tridiagonal** structures. I read the full closing section: **a vanishing diagonal is not
  on that list.** Leg 57's note is accurate.

I also confirmed the `NOT_BLOCK_DIAGONAL` classification structurally rather than by label: BDL
factor the tail as `T = L_I U_I` and their `A` (eq. 21) couples the finite block to the tail —
`x_F = K⁻¹ y_F − β_{m−1} U_I⁻¹ L_I⁻¹ r₀ y_I (K⁻¹)_{c_{m−1}}`. The finite block genuinely sees the
tail data. So BDL is a real published precedent for MM's move, and its price is on the label.

## 6. The ban recommendation — SOUND, verified from the papers not from leg 57's prose

Leg 57 recommends **not** lifting the ban even though its stated condition is met, because
Cadiot pre-empts the claim independently. I checked this from the sources, and it holds — in fact
it holds on two independent legs:

* Cadiot §3 opening, **verbatim and correctly located**: *"By construction `D` is supposed to be
  diagonally dominant, which hints to the Gershgorin theorem."*
* CLN §1, verbatim: the Fréchet derivative being asymptotically diagonally dominant is named as
  the *main ingredient*, with the tail operator explicitly *"(which is diagonal)"*.

So the observation is in print independently of BDL, and lifting the ban on the strength of the
BDL resolution alone would re-open a claim that a different paper already occupies. **Concur:
do not lift.** One nuance worth recording: Cadiot's §3 sentence sits in a Gershgorin
spectral-enclosure context rather than a radii-polynomial tail estimate, so the single most
on-point statement of the multiplier half is actually the **CLN §1** passage. The conclusion is
unchanged; the CLN citation is the stronger one to lean on.

---

## 7. Gaps

**G1 — MINOR, CITATION DEFECT, THE ONLY REAL FINDING OF THIS PASS.**
The Cadiot sentence *"the operator `L` becomes an infinite diagonal matrix `L_q` with entries
`l(n/2q)` on the diagonal"* is attributed to **§2 ("section 2 (periodic counterpart)")**. It is
not in §2. It is in **§1.2, the Introduction** — in the paragraph beginning *"More precisely,
given `q > 0`, (1) has a Fourier coefficients counterpart…"*, which itself forward-refers
(*"which we expose in Section 3"*). I checked this hard rather than by eye: **Cadiot's §2
("Presentation of the problem", through §2.3) contains zero occurrences of the string
"diagonal".**

The sentence is real, verbatim as quoted, and in the full text — so this is *not* a repeat of leg
53's abstract-citation failure, and the "folklore in print" conclusion is untouched (it is
independently carried by the correctly-located §3 quote and by CLN §1). But this leg's entire
premise is that a located statement can be checked, and a wrong section number is the one error
its own guard cannot catch. The label appears in four places: `writeup/novelty/leg_57.md`,
`solver/certificate_shapes.py`'s docstring, `TECHNICAL …§0`, and the JSON's
`XS0_novelty.prior_statement_of_the_dichotomy.where_multiplier_half`. Recommended follow-up:
change "section 2" to "section 1.2 (Introduction)" in those four places. **Not a merge blocker.**

**G2 — MINOR, COULD NOT BE PINNED EITHER WAY.**
Chen–Hou's advection inequality (*"`c̄_l x + ū(x,y) ≥ c₁x`, `c₁ ≈ 0.47`"*) is quoted verbatim and
is certainly in Part I, but it is a run-in header paragraph and `pdftotext` reflows the region
(a fragment of §2.6.1's closing sentence appears duplicated near §2.4/2.5). Attribution to §2.6
*"Main terms of the system"* is consistent with the surrounding structure and nothing contradicts
it; I simply cannot confirm the digit from a flat extraction. Flagging for completeness, not as a
defect.

**G3 — NOT CHECKED.** The single DF (2410.05480) located statement is the one of the eleven I did
not pull. It is the lowest-stakes row — classified `NO_UNBOUNDED_PART` / `FINITE_JACOBIAN` and
explicitly admitted "to record that it is silent, not to be counted on either side" — and that
paper was already re-derived at leg 48.

**G4 — SCOPE NOTE.** The string-absence claim is stated for *both* Chen–Hou parts. I verified it
for **Part I only** (0/4 hits). Part II (2305.05660) was not independently searched.

**No unresolved gap bears on the gate answer, the headline correction, the ledger
classifications, or the ban recommendation.**

## 8. Sign-off

**Merge `leg/xs-v1` as-is.** The gate answer NO is earned, the ledger is genuinely executable
with a live control, the numbers reproduce exactly from an independent construction, the two
"honest demotions" are real demotions and not decorated wins, and the BDL zero-diagonal question
is properly closed against the repo's own hoped-for direction. G1 is worth a one-line correction
on a later pass; it changes no claim.
