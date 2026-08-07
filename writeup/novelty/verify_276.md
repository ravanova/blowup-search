# VERIFY 276 — independent review of Route-PUB2R3 (leg 276, `9b7fc5c`)

**Branch** `verify/276-pub2r3-review`, fresh from `origin/main` at `9b7fc5c`. **Date** 2026-08-07.
Mandated verifier under the standing iteration-correction rule for PUB2. This is the **sixth**
landing on this document (250, 268, 271, 274, 270, 276) and the sixth mandated check.

Nothing was computed, measured or invented here. Every number below was re-derived from a banked
artifact on `main`, or read directly out of the diff.

---

## Verdict in one line

**Leg 276's five declared families all verify — every edit is correct, every loosened bound is the
tightest value its banked source supports, and the math it corrected is right.** One finding:
**the C1 residue leg 276 left standing as unresolvable is in fact partially resolvable from two
banked sources on `main`**, and applying them makes one of the four sites (`BLOG L14`) a plain
error rather than an ambiguity. That is a gap in leg 276's *assessment*, not in its *edits*.

---

## 1. Territory — PASS

`git show --stat 9b7fc5c` is **exactly the 5 declared files** (2 PUB2 docs, `experiments/journal/leg_276.md`,
`writeup/CORRECTIONS.md`, `writeup/novelty/leg_276.md`). 509 insertions, 25 deletions.
None of the five integration-owned ledgers (`plan_of_record.py`, `CONTINUATION_PROMPT.md`,
`experiments/JOURNAL.md`, `PHASE2_P2_NOTES.md`, `LITERATURE_CHECK.md`) was touched.
`CORRECTIONS.md` is **not** on that list — checked against `ORCHESTRATION.md` §5a — so editing it
was in-territory.

## 2. The "116 byte-unchanged" claim — PASS, verified independently, not by re-running leg 276's script

Rather than trust the trace re-run, I tokenized every numeric literal in both files at `9b7fc5c~1`
and `9b7fc5c` and diffed the multisets. **Every token that was lost or decreased in count is one of
leg 276's declared changes, and there are no others:**

| file | tokens removed | accounted for by |
|---|---|---|
| BLOG | `185` | leg-count refresh |
| TECH | `0.009`, `0.0090` | N3, N2 |
| TECH | `2.22e−14`, `2.62e−03` | N4, N1 |
| TECH | `0.868155` | N6 |
| TECH | `0.7146430`, `7.0e−06`, `1.3993` (5→1) | N5, the retired two-step chain |
| TECH | `185` (×2), `512.` | leg-count refresh; punctuation at the reworded §3.5 sentence |

**Zero un-declared printed figures moved.** This is a stronger check than "116/116 byte-identical":
it would also have caught a value silently *added* in the wrong place. The one surviving `1.3993`
is §3.2's table row quoting leg 163's three raw data (`1.3993 / 1.2680 / 1.3769`) — correct to
leave, it is the datum, not the derived chain.

## 3. Family 3 — the `0.71465` provenance — PASS, and leg 276's framing is the more accurate one

Re-derived in `Decimal` at 40 digits and in float64:

* `1/1.39927667753796 = 0.7146549471256172` **exactly in float64** (bit-identical to the banked
  `G4_bordered_reduction_at_zero.implied_sigma_min_lower_witness`). Leg 276's one-step chain is right.
* Rounding that to five decimals gives `0.71465`, a round-**DOWN** of `4.947125617e−06`.
  Leg 276's `4.9e−06` is correct.
* Leg 270's "rounds to `0.71465` with no round-up" is **also** correct — the two claims do not
  conflict. Leg 276's is strictly more informative: it names the direction and the magnitude.
* The *old* text's "round-up of `7.0e−06`" was self-consistent only against the **truncated** ratio
  `1.3993` (`0.71465 − 1/1.3993 = 6.964e−06`). Leg 276 correctly identified that the truncation,
  not the number, was the defect.
* `σ_min ≤ 0.71465495` is a **valid and tight** upper bound: `0.71465495 ≥ 0.7146549471256172`.

**The subtle point leg 276 found and leg 270 missed is real.** Because the witness bounds `σ_min`
from *above*, rounding it **down** to `0.71465` states a bound `4.9e−06` **stronger** than the data
licenses — the same defect class as N1–N4, at a site leg 270 verdicted MATCH. Leg 276's choice to
disclose rather than move the digit (which is byte-protected at six sites) is the right trade.

## 4. Family 2 — the four loosened bounds — PASS, all four are the tightest value the data supports

Each banked value re-read directly from its JSON on `main`, and each new bound re-checked:

| id | banked source (on `main`) | banked value | old bound | new bound | old? | new tightest at that precision? |
|---|---|---|---|---|---|---|
| N1 | `p2_route_ngx_v1_general.json .NGX5_max_abs_exponent_for_mu_positive` | `0.0026247852520269194` | `≤ 2.62e−03` | `≤ 2.63e−03` | **FALSE** | yes |
| N2 | `p2_route_h2i_v1_scoping.json .G3….max_abs_dev_from_1_minus_s_for_s_le_0.7` | `0.009045867213865688` | `0.0090` | `0.00905` | **FALSE** | yes |
| N3 | `p2_route_h2i_v1_scoping.json .G3….max_spread_across_p_for_s_le_0.7` | `0.009036579560100677` | `0.009` | `0.00904` | **FALSE** | yes |
| N4 | `p2_route_h2s_v1_scoping.json .gates.G4….worst_rel_residual` | `2.2201198984667287e-14` | `≤ 2.22e−14` | `≤ 2.221e−14` | **FALSE** (by 1.2e−17) | yes |

**Not arbitrarily loosened** — each new figure is the smallest representable bound at one more
significant digit that the banked value actually satisfies. N2/N3 additionally now agree with §4.1's
own sweep table, so the document states each quantity one way.

## 5. Family 4 — the 23 leg-163 claims post-merge — PASS, 9 spot-checked independently from `main`

Read straight out of `writeup/data/p2_route_h2s_v1_scoping.json` **on `main`** (not from leg 276's table):

| claim | independently read | matches |
|---|---|---|
| `G1_mellin_exact_norm.max_rel_err` | `0.0` | ✓ |
| `G1….rows[*].witness_fraction_of_bound` | `0.9980059800697489 … 0.9999333399992594`, 6 rows | ✓ |
| `G1….rows[*].alpha` | `0.05 … 1.5`, 6 rows | ✓ |
| `G2_resolvent_identity.worst_rel_residual` | `2.8072372914100434e-14` | ✓ |
| `len(G2….rows)` | `18` | ✓ |
| `G3….mode_eigenvalue_1.max_abs_residual` | `1.790180836524724e-15` | ✓ |
| `G4….max_ratio_uX_over_fX` | `1.39927667753796` | ✓ |
| `G4….implied_sigma_min_lower_witness` | `0.7146549471256172` | ✓ |
| `G4….rows[*].ell_after_projection_abs` | `0.0` in **all three** data | ✓ (matches §3.1's "exactly 0.0 in all three test data") |

## 6. Family 1 — the convention disclosure — PASS

`convention` now appears 20× in TECH and 1× in BLOG; `0.0420`, `12.5`, `0.01086`, `0.13580` appear
in both. The three facts the brief required are stated **together** at §0's blockquote and are
pointed back to at §3.2, §3.5 (ladder), §4.5, §5(3), §7 and BLOG's first use — the six clusters
plus the ceiling. The invariance sentence ("a positive weight cannot send a positive limit to
zero") accompanies each. Content re-checked against
`p2_route_h2c_v1_construction_correction_leg268.json .what_is_NOT_corrected.convention_caveat_recorded_by_249`.

## 7. Truncation-independence — PASS, the defect has NOT crept back

Given this took three iterations to close originally, I swept both files for it independently.
**Every** occurrence of the phrase is now a negation or an explicit supersession flag:

* TECH L227 — "is **not** a truncation-independent value and is not offered as one"
* TECH L370 — leg 276's **new** text, flagging leg 176's opening clause "bounded away from zero and
  truncation-independent" as **superseded and deliberately not quoted**, citing A1 of
  `p2_route_h2c_v1_construction_annotation_leg274.json`
* TECH L382–383, L407, L410 — all negations
* BLOG L68 — "it is *not* a value independent of the truncation"

Zero affirmative uses. Leg 276 **strengthened** the guard rather than eroding it: L370 closes the
one remaining route by which a reader could have re-imported the defect via a partial quotation.

## 8. Arguments / conclusions / gate answers — PASS

Read both files in full around every hunk. All 25 deleted lines are numeric corrections or
provenance rewording. Every gate verdict is byte-unchanged: §0's four-point table (`theorem` /
`scoping NO` / `construction YES on both conjuncts with one magnitude that says NO` / `scoping NO`),
§4.5's FAILS/passes column, §5's four parts, `140.72`, `11.0127`, `0.139 %`, `0.0908`, the
`L1 → L4` "none has moved". Two rewrites deserve naming, and both are consistency repairs, not
new conclusions:

* §3.5's body now says leg 176's attributed cause for the `N = 1024` rise is **superseded** by leg
  249's `eigh`-vs-Cholesky finding. That finding was **already banked** in the same paragraph's
  footnote (present pre-276); leg 276 only made the body agree with its own footnote.
* BLOG's "the independent re-derivation we commissioned" → "an independent re-derivation … (it was
  not the verification leg we originally commissioned)". This makes BLOG agree with TECH §0's
  already-present leg-192 statement.

Leg-count refresh `185 → 275 legs (count current as of leg 276)` is consistent across all four sites.

---

## 9. THE FINDING — C1 is partially resolvable, contrary to "no banked source determines it"

Leg 276 left C1 standing and reported it, which was honest, and scoped its claim precisely to *"no
banked source **in leg 276's read-set**"*. That scoped claim is true. But the residue is not
genuinely undetermined, and I found the sources by searching outside that read-set.

**Two independent banked artifacts on `main` anchor the "seven" figure to an explicit leg range:**

* `writeup/4_p2_lottery/BLOG_P2_ROUTECP_V1.md:12` — *"**Seven legs of work (51–57)** had produced a
  negative result about a certification method"*
* `writeup/4_p2_lottery/TECHNICAL_P2_ROUTENG_V1.md:22–24` — *"## 0. What seven legs held… **Legs
  51–57** produced every part of a negative result and assembled none of them"*

Both name the same range. So "seven successive legs failed to close such a certificate" is
**determined**: it is legs 51–57, the certificate-closure attempts.

**Leg 276's own hypothesis is therefore confirmed — and it splits the four sites 2/2, not 4/0:**

| site | text | status under the 51–57 anchor |
|---|---|---|
| TECH L35 | "**Seven** successive legs of this project failed to close such a certificate" | **correct**, anchored at 51–57 |
| TECH L627 | "the obstruction that consumed **roughly seventy** legs" | defensible — the broader *obstruction* span, a different claim; no banked anchor found either way |
| BLOG L52 | "the wall we had been hitting for **seventy** legs" | same broader framing as L627 |
| **BLOG L14** | "We spent about **seventy** work-legs **failing to build a computer-assisted proof for a one-dimensional fluid model**" | **wrong** — see below |

**BLOG L14 is the problem.** It is not the obstruction claim; it is the *certificate-building*
claim, and it is near-verbatim its companion's:

> PUB1 `BLOG_P2_PUB1_V1.md:9` — *"We spent **seven** successive work-legs trying to build a
> computer-assisted proof — a certificate — for a one-dimensional fluid model."*
> PUB2 `BLOG_P2_PUB2_V1.md:14` — *"We spent about **seventy** work-legs failing to build a
> computer-assisted proof for a one-dimensional fluid model."*

Same object, same activity, same sentence shape, **10× different number** — in two documents PUB2
itself presents as a pair ("The companion piece anatomises the failure"). And PUB2's own TECH §0
L35 states that same activity as **seven**. So BLOG L14 contradicts (a) PUB1 at both its sites,
(b) PUB2's own technical note, and (c) the two banked leg-range sources — while TECH L627 and
BLOG L52 remain legitimately a different, broader claim.

**Magnitudes:** 2 of 4 sites resolved as correct-as-written or defensible; **1 of 4 (BLOG L14)
resolves as a plain error**; 1 of 4 (TECH L627) has no banked anchor for `seventy` in either
direction. I have **not** fixed it — per the brief this is reported, not repaired.

The `seventy` figure has **no** banked anchor I could find anywhere in `writeup/`,
`experiments/journal/` or `reports/`; `seven`/51–57 has two. That asymmetry is itself worth
recording.

## 10. Process concern — the seventh iteration

The brief asked that a seventh iteration be flagged as a standing process concern rather than
filed as another work item. **It should be.** §9 makes a seventh landing on this document
necessary — one sentence in BLOG L14, plus a decision on whether TECH L627 / BLOG L52's `seventy`
gets a banked anchor or gets softened.

The concern is not that defects keep being found; it is that **each pass's read-set has been
scoped to the previous pass's findings**. Leg 270 found C1 by reading PUB2 against PUB1. Leg 276
inherited C1 as framed and searched within the read-set that framing implied — and the resolving
sources (`BLOG_P2_ROUTECP_V1`, `TECHNICAL_P2_ROUTENG_V1`) sit one grep outside it, in the same
`writeup/4_p2_lottery/` directory. A seventh pass scoped the same way will have the same blind
spot. **The recommendation is that any seventh pass be scoped by artifact (every file in
`writeup/4_p2_lottery/` that PUB2 shares a claim with) rather than by inherited defect list**, and
that it be the last — with the exit condition stated up front rather than discovered.

---

## Summary of magnitudes

| | |
|---|---|
| declared files in diff | **5 / 5**, zero integration-owned ledgers touched |
| un-declared printed figures moved (independent multiset diff) | **0** |
| family-2 bounds re-checked against banked JSON | **4 / 4** correct, **4 / 4** old bounds genuinely false, **4 / 4** new bounds tightest at that precision |
| family-3 identity re-derived | `1/1.39927667753796 = 0.7146549471256172` **exact in float64**; round-**down** of `4.947e−06`; `≤ 0.71465495` valid |
| leg-163 claims independently re-read from `main` | **9 / 9** reproduce |
| truncation-independence affirmative uses | **0** (5 negations + 1 new supersession guard) |
| gate answers / conclusions changed | **0** |
| **C1 sites resolvable from banked sources outside leg 276's read-set** | **3 of 4** (1 confirmed correct, 1 confirmed **wrong**, 1 defensible); 1 unanchored |
| verdict | families 1–5 **PASS**; **one finding at C1**; seventh iteration **flagged as a process concern** |
