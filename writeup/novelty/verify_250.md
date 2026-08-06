# VERIFY 250 — post-landing review of Route-PUB2FIX (leg 250, commit `71cde44`)

**Verdict: CONFIRMED, no gap.** Leg 250's central claim — that the leg-163/leg-176 `σ_min`
conflict was an **inverted inequality sign**, not a wrong magnitude — is correct, and correct for
the reason leg 250 gives. Three sub-threshold prose imprecisions are recorded below as DOCS nits
(magnitudes given); none of them changes a number, a direction, or a conclusion. One genuine
residue **outside** PUB2FIX's declared territory is confirmed as real and is recommended as a
DOCS/rework item.

Reviewed independently: arithmetic re-derived from `Decimal`, provenance traced to the banked JSON
and the producing source file, bound direction re-derived from the definition of the G4 quantity
rather than from leg 250's prose. No leg-250 script was re-run (lesson 90).

---

## 1. Arithmetic and provenance of `1.3993` — CONFIRMED, with one wording nit

Re-derived at 30-digit precision:

```
1/1.3993   = 0.714643035803616093761166297434
0.71465 - 1/1.3993 = 6.964e-06   (relative 9.75e-06)
1/0.71465  = 1.39928636...
```

So `0.71465` is **not** exactly `1/1.3993`: round-to-nearest at five decimals gives `0.71464`. The
gap is `7.0e-06` absolute, `9.7e-06` relative — consistent with a **round-up** at the fifth
decimal, which is exactly what leg 250's §3.2 provenance note discloses in the same breath
(*"rounded up in the fifth decimal (`1/1.3993 = 0.7146430`)"*). The disclosure makes the reader
whole, so this is not a defect at §3.2.

**Provenance of `1.3993` — genuine, not invented for this leg.** It is banked as
`C6_closed_form_ratio.leg163_G4_values = [1.3993, 1.2680, 1.3769]` in
`writeup/data/p2_route_h2c_v1_construction.json`, carried from
`experiments/p2_route_h2c_v1_construction.py:323`, and the same three values appear in leg 176's
own journal (`experiments/journal/leg_176.md:165`). `max(1.3993, 1.2680, 1.3769) = 1.3993` —
confirmed largest. The banked record also carries leg 163's own claimed direction verbatim:
`leg163_inferred_sigma_min_witness = 0.7147` with `leg163_witness_optimistic_by = 7.870742…`. So
leg 163 did claim `≥`, and leg 250 is not attacking a straw reading.

## 2. The bound direction — INDEPENDENTLY RE-DERIVED, leg 250 is right

The G4 quantity is defined in `solver/origin_h2_certificate.py:484` and computed by
`resolvent_ratio()` in `experiments/p2_route_h2c_v1_construction.py` as `r = ‖u‖_X / ‖f‖_X` for
Xu's exact solution `u` of `L u = f`, normalized by `ℓ(u) = 0`. Therefore:

- `σ_min = inf_{v ≠ 0} ‖L v‖_X / ‖v‖_X`, so `1/σ_min = sup_v ‖v‖_X / ‖L v‖_X`.
- Each sampled datum gives `r_i ≤ 1/σ_min`, i.e. `σ_min ≤ 1/r_i`.
- Over a finite family the tightest statement is `σ_min ≤ min_i (1/r_i) = 1/max_i r_i = 1/1.3993`.

**A finite sample can only bound `σ_min` from ABOVE. There is no missing case.** A single vector
supplies one Rayleigh quotient, which is an *upper* bound on an infimum; lower-bounding an infimum
requires a statement over *all* `v` (an exhaustive/covering argument), which no sampling leg
performed. Leg 163's `σ_min ≥ 0.7147` is the inverted reading, exactly as leg 250 says.

Verified numerically: `1/max r = 0.7146430`, `1/min r = 0.7886435`. Note leg 163 used `1/max r`,
which is the correct *upper*-bound extremum and the **wrong** extremum for the `≥` reading it
wrote — internal evidence that the sign, not the sampling, was the error.

**Leg 250's "decisive check" holds, though its one-line phrasing is elliptical.** Leg 250 writes
that under the `≥` reading, leg 176's re-run reciprocal `1.1519` "cannot also be a lower bound".
Two lower bounds are not by themselves contradictory. The real contradiction, which the banked
data do supply: leg 163's own datum `r = 1.3993` exhibits a concrete vector with Rayleigh quotient
`1/1.3993 = 0.7146`, which directly refutes `σ_min ≥ 1.1519`. Verified:
`1/max(over_seeds) = 1/0.868153885807814 = 1.1518695`. The check is sound; only the intermediate
step is left implicit in the prose. **DOCS nit 1.**

## 3. The five edited sites — ALL SAY WHAT LEG 250 CLAIMS, cross-checked against the JSON

Every magnitude below re-derived from `writeup/data/p2_route_h2c_v1_construction.json`, not from
leg 250's prose.

| site | line | now reads | cross-check |
|---|---|---|---|
| §3.2 table row | 200 | `σ_min` "does **not** go to 0: measured **0.0908**", leg 163's three data "give only `σ_min ≤ 0.71465` — an **upper** bound" | `sigma_min_at_512 = 0.09080465147034879` → `0.0908` ✓; direction ✓ |
| §3.2 provenance note | 206–216 | full provenance, sign inversion, `12.71 %` / `7.88 %`, `0.0908 ≤ 0.71465` | `1.3993/11.0127 = 12.706 %` → 12.71 % ✓; `0.868154/11.0127 = 7.883 %` → 7.88 % ✓; `‖R‖_X = 11.012651706796523` ✓ |
| §3.5 conflict note | 335–358 | correction "applied at all three sites", sign not magnitude, plus the new *no proved floor* paragraph | ladder `0.09088780 → 0.09080465` over `N = 64…512` = **0.09149 %** → stated `0.0915 %` ✓; `relative_spread = 0.0013899` = **0.139 %** over the 16-fold reliable window `32…512` ✓ |
| §4.5 scale table | 508 | "measured at **0.0908** (§3.5), not the `0.71465` of earlier drafts, which was only an upper bound" | ✓ |
| §5(3) | 545–547 | "`σ_min` measured at **0.0908** … the `0.71465` of earlier drafts was an upper bound from three data, not a floor" | ✓ |
| BLOG companion ¶ | 103–112 | sign-not-magnitude, "no *bigger* than 0.71465, never that it is no smaller", and "evidence of a positive limit, not a proof of one" | matches JSON `reading` field verbatim in substance ✓ |

The retained `σ_min ≤ 0.71465` is **true** (the sharp sampled bound is `0.7146430 < 0.71465`), so
retaining the rounded-up figure with the corrected sign states something weaker than the data
support — safe, not overclaimed.

The new "no proved floor" paragraph is faithful to the source: the JSON's own `C1` reading says
*"This is float64 EVIDENCE of a positive limit, not a proof of one"*, which leg 250 quotes
accurately. Grep confirms **zero** surviving instances of `σ_min ≥ 0.71465` anywhere in either
document.

**DOCS nit 2.** §3.5 line 344 says "`0.71465` is exactly `1/1.3993`" *without* the round-up
disclosure that §3.2 line 207 carries. Overstatement magnitude `7.0e-06`; a reader who reaches
§3.5 first is told "exactly" for a number that is not exact.

**DOCS nit 3.** §3.5 line 347–348 says `0.71465` is "retained only in §3.2". The numeral in fact
also appears at §4.5 (line 508) and §5(3) (line 547), in both cases as a named *superseded* value
rather than a live bound. The substance is right (only §3.2 retains it as an operative bound); the
self-description is loose.

## 4. The flagged residue — CONFIRMED outside declared territory, and a REAL inconsistency

`TECHNICAL_P2_PUB2_V1.md:175` (§3.1, "What was checked, and what passed") — the numberless check
row:

> | **no §2-class obstruction** | — | `σ_min` bounded away from zero and truncation-independent (below) |

This is in **§3.1**, not one of the three sites (§3.2, §4.5, §5(3)) PUB2FIX's gate required.
Confirmed outside declared territory; leg 250 was right to flag rather than edit it.

It is a **real inconsistency worth a DOCS/rework item**, and slightly sharper than leg 250's own
framing of it. The row sits in the "check" column of a table introduced as *"each re-derived from
primary source"* — i.e. it presents "bounded away from zero" as a **verified conjunct**. §3.5 now
says in terms that *"neither leg proves one"* and that *"what does not survive … is any claim to a
proved floor"*. §3.1 therefore asserts as checked precisely the thing §3.5 now withdraws. The
suggested repair is one clause (e.g. "`σ_min` does not decay with truncation — measured 0.0908,
flat to 0.139 % — where §2's decays"), but it is a **rework leg's** call, not this verifier's.

No other residue found: the blog's earlier paragraph (line 88) says only that the quantity "stays
put — `0.0908`, moving by 0.139 % across a sixteen-fold change in truncation", which is
descriptive of the ladder and asserts no floor.

## 5. Territory — CONFIRMED CLEAN

`git diff --stat 06e96d2 71cde44` touches exactly four files, all declared:

```
experiments/journal/leg_250.md                92 +
writeup/4_p2_lottery/BLOG_P2_PUB2_V1.md       10 +-
writeup/4_p2_lottery/TECHNICAL_P2_PUB2_V1.md  55 +-
writeup/novelty/leg_250.md                   106 +
```

None of the five shared ledgers touched. No code, no banked JSON, no `plan_of_record.py`.

---

## Bottom line

Leg 250's determination survives an independent re-derivation on all four load-bearing points:
the reciprocal (`0.7146430`, disclosed as rounded up), the provenance of `1.3993` (genuinely leg
163's largest sampled ratio, banked), the bound direction (sampling bounds an infimum only from
above — no case missing, and leg 163's choice of `1/max r` is itself internal evidence of a sign
error), and the five edited sites (all five say what is claimed, and every magnitude — 0.0908,
12.71 %, 7.88 %, 0.0915 %, 0.139 %, 11.0127 — reproduces from the banked JSON to the stated
precision). **No repair needed.** Three prose nits (`7.0e-06` overstatement of "exactly" at §3.5,
an elliptical self-consistency step, one loose "only in §3.2") and one confirmed out-of-territory
residue at §3.1 are handed to the Decision Maker as an optional DOCS item.
