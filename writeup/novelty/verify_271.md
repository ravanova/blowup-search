# verify_271 — independent review of leg 271 (Route-PUB2R2), third iteration on PUB2

**Verdict: the truncation-independence defect family is genuinely CLOSED. 0 surviving sites.**
Leg 271's clauses (a)–(d) all hold under an independent sweep that did not reuse its 12 patterns.
**One residue found, in a different and lesser class** (a subject-attachment slip on a set of
correct numbers, inherited from leg 249 via leg 268, §5 below) — reported precisely, graded as
**not** a fourth iteration of the same defect.

Branch `verify/271-pub2r2-review`, cut from `origin/main` at `c2e9beb`. Leg 271 = `504438f`.
`plan_of_record.py` runs clean; stage **P0** is NEXT. Nothing computed; nothing edited outside
this file.

---

## 1. Independent sweep — my own strategy, not a re-run of leg 271's

Both documents were **read end to end** (TECHNICAL 649 lines post-edit, BLOG 214), then swept with
an independently chosen pattern set aimed at the *property* rather than the wording, including
phrasings leg 271's patterns 1–10 do not anticipate (`plateau`, `stable`, `no longer`,
`same value`, `converge`, `asymptot`, `does not (decay|collapse|drift|go|move|depend|change)`,
`stays put`, `bounded (away|below)`).

| what | count | assessment |
|---|---|---|
| `independen` hits, TECHNICAL \| BLOG | 15 \| 5 | **0 assert independence.** 6 are negations (T L334/335/359/362, B L68/113), 8 are a different subject (three independent coordinates/quadratures, independent data, `p`-independent, independently re-derived), 6 concern leg 249's independent check, 1 is the **true** `ℓ¹_w` statement (T L207 left cell, leg 127's theorem) |
| `floor` hits | 12 \| 3 | **0 assert a proved floor.** 5 are `ℓ¹_w`'s own `‖A‖_w` floor (§2 L152/153, §4.5 L534/540), 2 are the arithmetic/float floor of a control, the rest carry "not a proved floor" / "evidence of a floor and not a proof of one" |
| `flatten`/`settle`/`stays put`/`converge` | 9 \| 5 | every one is either quantified in the same clause or hedged within the same paragraph block |
| `theorem`/`proved`/`proof` | 24 \| 4 | **the grade split is intact everywhere** — see §4 |

**No site in either document asserts that `σ_min` or `‖T⁻¹‖_X` has a value independent of
truncation, window or `N`.** Confirmed by reading, not by counting.

### 1b. One angle leg 271 did not take, and it comes out clean

Leg 271's scope was the two PUB2 files. The claim family could have leaked into sibling **live**
documents. Swept `writeup/**` for `truncation.independen|independent of the truncation|4.026|
0.0908|0.71465|bounded away from zero`:

- `TECHNICAL_P2_PUB1_V1.md`, `PUB3`, `ROUTENGX` (technical + blog), `ROUTET`: **0 hits**.
- All remaining repo-wide hits are in `writeup/novelty/` and `experiments/journal/` — historical
  leg records (legs 177, 238, 249, 250, 268, 271 and `verify_250`/`verify_268`), which correctly
  preserve what was written at the time and must not be rewritten.

So the two-file scope was **adequate**, verified rather than assumed.

---

## 2. Spot-check of the repaired sites against leg 249 / leg 176 at source

Recomputed from the banked JSON and leg 249's own ladder, not from the prose.

| figure as printed | independent check | verdict |
|---|---|---|
| `0.139 %` over a 16-fold truncation range (T L46/181/206/207/582, B L92) | `C1_bordered_sigma_min_X.relative_spread` = **0.0013899483438452888** over `reliable_window` = `[32,64,128,256,512]`, a **16-fold** range | **exact match**, including the "16-fold" |
| `σ_min` ladder `0.0927566 … 0.090804` | matches JSON `ladder` at every rung to the six figures printed | ✅ |
| `0.090804` at `N = 512` | inside leg 249's certified enclosure `(0.090804094, 0.090804194)` | ✅ correctly reduced to supported figures |
| `‖T⁻¹‖_X` `3.994032 → 4.028864`, **0.865 %** | leg 249 journal L218/L232; `(4.028864−3.994032)/4.028864 = 0.8646 %` | ✅ (relative to the last rung, leg 249's own convention) |
| understates the limit by `0.14 %` | `(4.0318−4.026241)/4.0318 = 0.1379 %` | ✅ |
| `140.72`, growth `~K²` | **byte-untouched by `504438f`** — absent from every hunk | ✅ as claimed |
| `0.0920 %` over `N = 64…512` (T L388) | **0.0922 %** from the six-figure values printed in the same clause; **0.0915 %** at full JSON precision | consistent as printed; a rounding-propagation nit of 0.8 % relative, below the figure's own precision |

The three repaired sites I checked hardest — T L206/207 (§3.2's two rows), T L359–364 (§3.5) and
B L98–104 — all match leg 268's already-established framing in **strength as well as wording**
("not a proved floor", "evidence of a positive limit, not a proof of one"). Nothing is
overstated; nothing is understated to the point of losing the converges-vs-diverges contrast the
argument actually uses.

---

## 3. The nine deliberately-untouched sites — independently assessed

I re-read each against journal §4's stated reason and judged it afresh.

| site | leg 271's reason | my assessment |
|---|---|---|
| B L91 "stays put here — `0.0908`, moving by 0.139 %" | quantified in place; paragraph closes on the hedge | **agree, leave.** The magnitude is in the same clause |
| T L208 "no such floor" (§3.2 `Z₁` row) | a different quantity/direction | **agree, leave.** The row is *consequence for `Z₁`*; the right cell rests on Xu's **published** closed-form inverse, not on the ladder |
| T L534/L540 "(a) no `ℓ¹_w`-class floor" / "passes" (§4.5) | a floor on `‖A‖_w` | **agree, leave** — §2 L152 defines "the floor" as exactly the growing floor on `‖A‖_w`, so the column header is self-consistent with the document's own usage. *Softest surviving cell:* "passes" is unhedged, but it says "measured" and cross-refs §3.5, where the limitation is stated in full. Not a defect; a candidate polish if PUB2 is ever re-opened |
| T L156 "uniformly in `M`" | inside §2, correct | **agree, leave** |
| T L281–292 (§3.4 leg-176 status para) | time-stamped, marked "kept exactly as written", outcome pointer to §3.5 | **agree, leave.** It is about the *construction* leg, not the verification leg |
| B L146/L181, T L453/466/494/528/584/604 "invariant" | the `σ = s + 1/p` sense | **agree, leave.** Different object |
| T L46, L181, L319–335, L376–383, L568–573 | leg 268's own corrected text, the template | **agree, leave** — verified byte-untouched by `504438f` |

**None of the nine should have been touched.** One reason I initially suspected was mis-stated
(the `‖A‖_w` characterisation of §4.5) turns out to be correct against §2's own definition, and I
withdraw the objection.

---

## 4. The leg-127-theorem vs leg-176-float64-ladder distinction — checked at every site

This is the mathematically load-bearing point, so I traced the contrast through **all nine** places
it appears rather than the two leg 271 edited.

| site | `ℓ¹_w` side | origin-`H²` side | conflated? |
|---|---|---|---|
| T §0 table L44/L46 | kind = **theorem** (leg 127) | kind = **construction gate YES**, "not a proved floor" | no |
| T §3.1 L181 | — | "not a proved floor; §3.5 states that limitation in full" | no |
| T §3.2 L206/207 | `→ 0 like M^{−(1−s)}` | "flattens … evidence of a positive limit, **not a proved floor**" | no |
| T §3.5 L359–364 | "a **theorem**, `σ_min(L_M) = c_s M^{−(1−s)} → 0`" | "**measured absent** rather than proved absent" | no |
| T §3.5 L385–392 | — | "**neither leg proves one** … not written anywhere in this note" | no |
| T §5(1) L561–568 | "§2, **proved**" | "**published by Xu**, re-derived here at 2.8e−14" — rests on Xu's theorem, **not** on the ladder | no, and correctly so |
| T §5(3) L577–587 | — | "**measured** at 0.0908 … no **proved** floor anywhere in it" | no |
| T §6 table L611/612 | grade **theorem** | grade **scoping, escalated not built** | no |
| B L101–104 | "that is a **theorem**, not a measurement" | "evidence of a floor and **not a proof of one**" | no |

The distinction is preserved **accurately and uniformly**. Two things I checked specifically:

1. The word "theorem" never attaches to the origin-`H²` ladder. Its only uses are §2/leg 127,
   Xu's published invertibility, and explicit negations ("Infrastructure, not a theorem").
2. §5(1) is the one place both sides are stated at full strength — and it is **legitimate**,
   because the right-hand side there is Xu's *published* invertibility, not the measured ladder.
   That is exactly the site where a careless repair would have over-hedged. It did not.

The inference leg 271 preserved — *leg 127's mechanism is absent here, therefore the `Z₁` failure
is attributable to the block-diagonal shape of `A`* — is carried with the qualifier "on that
reading, the strongest the data support" at both T L362–364 and B L104, and is fenced at T
L366–367 against the stronger claim that some other `A` closes it. **I agree the escalation clause
did not need to fire.** The judgement is wording, not argument, and it is recorded in journal §5
so it can be disputed — which is the right disposal.

---

## 5. The one residue — correct numbers attached to the wrong quantity (NOT the hunted defect)

**TECHNICAL §3.5, L330–333:**

> `‖T⁻¹‖_X` **rises monotonically** across the ladder
> (`3.994032 → 4.012071 → 4.021340 → 4.026241 → 4.028864` at `N = 64 … 1024`, **0.865 %** in
> relative terms) with **decrements** shrinking geometrically (`1.126e−3 → 5.745e−4 → 3.027e−4 →
> 1.617e−4`, ratios `0.510 / 0.527 / 0.534`)

The four quoted numbers are **not** differences of the ladder printed beside them. Recomputed:

| quantity | successive differences |
|---|---|
| `‖T⁻¹‖_X` as printed (rises, so it has **increments**) | `1.804e−2 → 9.269e−3 → 4.901e−3 → 2.623e−3` |
| `σ_min = 1/‖T⁻¹‖_X` (falls, so it has **decrements**) | `1.126e−3 → 5.745e−4 → 3.027e−4 → 1.617e−4`, ratios `0.510 / 0.527 / 0.534` |

The quoted figures reproduce the **reciprocal's** decrements to every digit quoted, ratios
included. So the data are right and the word "decrements" is right — they are simply attached to
`‖T⁻¹‖_X`, which rises, rather than to the `σ_min` they were computed from. A reader recomputing
from the ladder in the same sentence lands **16× away**.

- **Provenance:** leg 249 journal L233–234, copied verbatim into PUB2 by leg 268 (`3f6d5d0`).
  Leg 271 left it untouched and did not list it among its nine.
- **Class:** subject-attachment/prose slip. It asserts **no** independence, overstates **no**
  strength, and the geometric-ratio evidence for "converges" is unaffected either way.
- **Grading:** this is **not** a fourth iteration of the truncation-independence defect. That
  family is closed. I flag it because it sits inside the `‖T⁻¹‖` sentence legs 268 and 271 were
  both working on, and because PUB2 is submission-track — a referee recomputing the sentence
  would stop on it.
- **Fix, if wanted:** one word plus one clause — either say "with the corresponding `σ_min`
  decrements shrinking geometrically", or quote `‖T⁻¹‖`'s own increments
  `1.804e−2 → 9.269e−3 → 4.901e−3 → 2.623e−3` (ratios `0.514 / 0.529 / 0.535`, the same
  conclusion). **Not done here** — this is a read-only verification leg.

---

## 6. Protected artifacts and territory — diffed directly

`git show 504438f --name-only` returns **exactly 4 paths**:

```
experiments/journal/leg_271.md
writeup/4_p2_lottery/BLOG_P2_PUB2_V1.md
writeup/4_p2_lottery/TECHNICAL_P2_PUB2_V1.md
writeup/novelty/leg_271.md
```

Matching the declared territory exactly. Consequently, and confirmed by direct diff:

| artifact | bytes changed by `504438f` |
|---|---|
| `writeup/data/p2_route_h2c_v1_construction.json` (leg 176's banked JSON) | **0** |
| `writeup/data/p2_route_h2c_v1_construction_correction_leg268.json` (leg 268's companion) | **0** |
| `writeup/novelty/verify_268.md` | **0** |
| the five shared ledgers | **0** — none appears in the commit |

Clause (c) holds as stated.

### 6b. Root cause, observed in passing

Leg 176's banked JSON `C1_bordered_sigma_min_X.reading` **still reads**:

> "BOUNDED AWAY FROM ZERO and truncation-independent. … This is float64 EVIDENCE of a positive
> limit, not a proof of one"

The banked artifact is correctly immutable and correctly left alone (the correction lives in leg
268's companion artifact). But it is the **upstream source** of the phrase that legs 250, 268 and
271 each had to chase out of the prose — the JSON's own first sentence contradicts its own last
sentence. Any future document quoting this key will regenerate the defect. Worth a pointer from
the companion artifact, or a note in the corrections register, rather than a fourth prose sweep.

---

## 7. Verdict

- **Clause (a) — exhaustive search, 0 surviving sites:** confirmed by an independent sweep with a
  different pattern set plus a full read of both documents. **I found nothing left in this family.**
  Extended beyond leg 271's scope to all sibling live documents: also clean.
- **Clause (b) — TECHNICAL §0/§7 agree with the BLOG ceiling and the record:** confirmed. The
  leg-192-vs-leg-249 distinction is preserved at both sites; BLOG L109's "the independent
  re-derivation we commissioned" checks out against leg 249's own self-description
  ("**Role: VERIFIER** … the independent verification of leg 176").
- **Clause (c) — protected artifacts 0 bytes:** confirmed by direct diff.
- **Clause (d) — escalation correctly not fired:** agreed, on the merits. The theorem/ladder
  asymmetry is handled accurately at all nine sites where the contrast appears.
- **Territory:** exactly the four declared paths.
- **Nine left-alone sites:** all nine correctly left alone.
- **One residue, lesser class:** §5 above.

**This is not a fourth iteration of the defect.** Leg 271's change of instrument — searching the
claim rather than a string — worked, and is the reason this pass found nothing in the family.

Ceiling: no computation run, no solver touched, no number introduced, no ban engaged, no route
promoted, no link of the `L1 → L4` chain moved. Clay odds remain ~0.05 %. PUB2 remains a draft;
this pass does not approve it for submission.
