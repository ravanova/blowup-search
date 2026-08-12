# Route-COBV v1 — `CLAY_OBLIGATIONS.md` checked clause by clause against its own sources

**Leg 384.** Verification class. **CEILING: TIER 2.** No link of the `L1 → L4` chain moved;
`CLAY_OBLIGATIONS.md` §6's two no-method obligations stay **OPEN**; **Clay stays ~0.05%.**

- Runner: `experiments/p2_route_cobv_v1.py`
- Curated data: `writeup/data/p2_route_cobv_v1.json` (`self_hash` `c52d812f…`)
- Evidence / figure: `experiments/p2_route_cobv_v1_evidence.py` → **fig105**
  (`writeup/figures/fig105_route_cobv_v1.png`), rebuilt from the JSON alone
- Document under audit: `CLAY_OBLIGATIONS.md`, sha256
  `f47a73ac27903d79f63435ba8f4726245059e0c09f931e15cb9c0ed7a2923bde` — **read only, never
  edited by this leg**
- Landed edit under test: `a962e4a` (merged in `d65419c`)
- Source of truth for item (i): `writeup/data/p2_route_cloc_v1.json` (leg 381, `7aecf78`) —
  **read, never written**

---

## 1. The pre-committed gate, and its answer

> **Does every checked clause either verify against its primary source / landed record, or get
> reported with the exact discrepancy verbatim?**
> **yes** → The obligations document graduates from DRAFT-UNVERIFIED clause by clause, on
> integration's edit.
> **no** → A source is unreachable: bank the refusal as a refusal; an unverifiable clause is
> recorded as exactly that.

**The gate answers YES.** 23 checks ran; **17 MATCH, 6 MISMATCH, 0 UNVERIFIED**; the
`unverifiable_clauses` list is empty. The Clay Institute's rules were reachable — **HTTP 200**
on both the rules page (79 319 bytes, sha256 `0a6f68d5…`) and the 2018-revision PDF
(43 263 bytes, sha256 `9b5003745c0ae7268dc7769f83e1c61eaca674f28631f1df2cd8400976640b2a`) —
so the `no` branch never engaged and **no refusal needed banking**.

## 2. The instrument control: proving the counts are measurements

A leg this cycle found a fabricated zero in its own instrument — a variable initialised to
`0.0` and never written. A mismatch count has exactly that failure shape, so **every one of
the 23 checks carries its own targeted plant, by name**, and the plants run in **both**
directions:

- a **MATCH** is only reported for a check whose **corrupt-plant** made it read MISMATCH;
- a **MISMATCH** is only reported for a check whose **repair-plant** made it read MATCH.

**23 controls run, 23 fired, 0 failed.** Three plants did *not* fire on the first attempt and
each exposed a real defect in the checker rather than in the document — I10's plant failed
because the banked rows step **2** decades, not 1, so the naive first difference was double the
per-decade increment and the "cube of" branch could never trigger; that repair turned I10 from
a false MATCH into a genuine finding. The other two (I5, III2) failed because a raw
`str.replace` could not cross a markdown line wrap and a PDF non-breaking space respectively.
A green light that could not go red was, in each case, the bug.

Two normalisation facts made the mechanical read possible at all: `pdftotext -layout` emits
**U+00A0 between every word** of the rules PDF, and the document's clauses wrap across
markdown `>` blockquote markers, so `norm()` strips both before matching.

## 3. Item (i) — the landed block against leg 381's `check_D` verdicts

15 checks (I1–I15). **12 MATCH, 3 MISMATCH.** Confirmed mechanically: the excision of
`with f ≡ 0` (**0 occurrences** remain in the target paragraph); the 4 CONFIRMED / 1 CORRECTED
/ 1 REFUTED counts, **recomputed from the JSON's six ledger rows and equal to the document's
stated counts**; the (b)→**(C)** labelling fix; the not-a-shortcut clause; §4's
`VERIFIED AS A SPECIFICATION — leg 381 (7aecf78), gate YES` header with its three numbered
amendments; the §4-stays-OPEN-until-DTOL rule; §7 marked `STILL UNCHECKED`; §8 ask #1 recorded
`SATISFIED`; and (D) named-but-not-authorised.

**Out of scope, recorded as such, not as verified:** the DTOL numbers in §4 amendment 1
(`0.8686`, `3.35`, `0.434`) and §8 ask #1's SATISFIED ruling are **not present in
`p2_route_cloc_v1.json`**. They lie outside this leg's declared comparison source and are
banked as *unchecked here*.

### I8 — the quoted verification tolerance is the single best row

The document (line 128): *"repaired it with the truncated law … **verified to `2.6e-5`**"*.
`2.6e-5` is the `abs_error` of the **α = 0.8 row alone** (`2.577133230399764e-05`). The JSON's
own `max_abs_error` over its four banked rows is **`0.0256893924479335`** at α = 1.4 — larger
by a factor **988.05**. At **α = 1**, which is the exponent §4 is actually about, the error is
**`0.000264923221459137`**. Panel B of fig105 draws all four rows against both lines.

### I10 — `326.875 per decade` is the increment of the cube, not of the norm

The document (line 158): *"the critical `L³` tail grows **326.875 per decade of window,
constant to 7.4e-10**"*. The JSON's own reading says *"the **cube of** the critical-norm tail
grows by a constant amount per decade"*. `326.87521405120924` is the per-decade increment of
`tail_L3_cubed` (`653.7456, 1307.496, 1961.2465, 2614.9969, 3268.7473`); the **L³ norm itself**
runs `8.679 → 14.841` across the same five banked rows. The three words *"the cube of"* were
dropped in transcription. **The document's qualitative conclusion is unaffected** — the tail is
still log-divergent and still never small — but the number as printed is not the number of the
quantity it is attached to. Panel C.

### I15 — reverse direction: a JSON verdict the document does not carry

Running the comparison the other way (every JSON ledger row → is it reflected in the document?)
found one. On the reviewer's clause *"decaying faster than any polynomial"*, leg 381 banked
**`CONFIRMED AND STRENGTHENED`**: Fefferman's condition **(4)** bounds *every derivative*,
`|∂ₓ^α u°(x)| ≤ C_{αK}(1+|x|)^{−K}` for **any** α and K, and the JSON says in terms that the
reviewer's phrase *understates* it. The landed document says only that decay *"stands as
stated"*, folding a strengthening into a plain confirmation.

## 4. Item (ii) — §2's four screen rows, machine-read

All four **MATCH**. Nothing here was transcribed: `solver/dssp_screen.py` was **imported and
executed** read-only, and the cited legs' JSONs were parsed.

| Row | Verified by |
|---|---|
| NRS 1996 / Tsai (T1/T2) | `classify_ss_ansatz` executed on measured λ = 1.7 → `ansatz=DSS`, `satisfies_theorem_ansatz=False`; `_ledger_nrs_tsai_three_way` executed → **`NOT-REACHED-BY-ANSATZ`**; leg 341's `p2_route_algw_v1.json` carries the claim verbatim |
| Chae–Wolf / Pineau–Vicol | leg 330's `value_lambda_ceiling` = `1.6487212707001282`, equal to `exp(1/2)` to 1e-15 and to the document's `1.6487`; `ledger_pineau_vicol` executed at λ = 1.7 → *"OUTSIDE Pineau–Vicol's lambda window — theorem silent"* |
| Chae–Tsai (Euler-only) | leg 326's `p2_route_ctrx_v1.json`: **4** theorems read, `equation_1_6_is` records the Euler transform with no Laplacian; `ledger_chae_tsai` executed → branch `(ii)`, `FAILS_HYPOTHESIS` |
| Jiu–Wang–Wei (Morrey) | leg 368's classification **`WIDENS`**; leg 370's planted widen-then-close control reproduces `EXCLUDED-BY-MORREY`; `ledger_morrey` executed on the DSS object → `NOT-REACHED-BY-ANSATZ` |

**Provenance finding on row 1 (recorded on a MATCHing check, not a mismatch).** The row cites
*"legs 253, 341"*. Leg 341's record carries the claim verbatim. **No `writeup/data/*.json`
declares leg 253**, so that half of the citation has no machine-readable landed record; the
operative encoding is `solver/dssp_screen.py` (legs 357/359/362).

## 5. Item (iii) — §7 against the Clay Institute's published rules

Four checks, **1 MATCH, 3 MISMATCH**. The two-year clause (III2) is correct: the rules require
*"at least two (2) years have elapsed since publication of the Proposed Solution in a Qualifying
Outlet"*.

- **III1 — "refereed *journal*" is narrower than the rules.** Section 6(a)(i) says *"a refereed
  mathematics **publication** of worldwide repute meeting the conditions in Section 6(e)"*, and
  Section 6(a)(ii) gives a **second qualifying route** the document does not mention: *"a
  publication meeting a relaxed set of conditions approved by the BOD following a recommendation
  from the SAB"*. Section 6(e) lists four characteristics whose absence disqualifies an outlet,
  including *"inclusion in the list of publications maintained by MathSciNet"*.
- **III3 — two load-bearing words dropped.** The rules (Section 4(c), repeated at 7(a)(i)) say
  *"general acceptance in the **global** mathematics community, as determined in the **sole
  discretion of CMI**"*. Acceptance is not a community fact the repository could observe; it is
  a CMI determination. Section 7(a)(i)(4) enumerates what CMI may consider.
- **III4 — §7 lists three conditions; the rules impose four.** Missing is Section **4(d)**:
  *"the Proposed Solution has satisfactorily answered the questions raised by the Problem's
  official description, as determined in the sole discretion of CMI"*, sharpened by 5(d). Also
  absent, and of planning relevance: **5(e)** *"CMI will not accept Proposed Solutions submitted
  directly to CMI"*; and — directly relevant to route 4 — **5(b)**, which states that for the
  Navier–Stokes Problem *"a resolution in either direction will be evaluated by the standard
  evaluation procedure set forth in Section 7"*, so **the breakdown direction this repository
  pursues is explicitly in scope**.

## 6. Proposed corrections, routed to integration

**This leg is a verifier: it reports gaps and repairs none.** `CLAY_OBLIGATIONS.md` was not
edited. The exact text below is proposed for integration to land; line numbers are against the
audited sha256.

**(a) I8 — line 128.** Replace
`repaired it with the truncated law ... verified to `2.6e-5`.` with:

> repaired it with the truncated law `E_ρ(t) ≍ ρ^{3−2α}(T*−t)^{α−1}`, verified across four
> exponents to a worst-case absolute error of `2.57e-2` (at `α = 1.4`); at `α = 1` — the
> exponent §4 is about — the error is `2.65e-4`.

**(b) I10 — lines 158–159.** Replace
`the critical `L³` tail grows **326.875 per decade of window, constant to 7.4e-10**` with:

> the **cube** of the critical `L³` tail grows **326.875 per decade of window, constant to
> 7.4e-10** — the norm itself running `8.679 → 14.841` across the banked 2→10 decades

**(c) I15 — lines 38–40.** Replace the CONFIRMED bullet with:

> - **CONFIRMED, verbatim:** *bounded energy* is Fefferman's condition **(7)**, and it is the
>   condition §4 and §5 are about. Smoothness and divergence-free stand as stated.
>   **Decay is confirmed and strengthened:** condition **(4)** bounds *every derivative*,
>   `|∂ₓ^α u°(x)| ≤ C_{αK}(1+|x|)^{−K}` for **any** `α` and `K`, so "faster-than-polynomial
>   decay" understates what the statement requires.

**(d) II1 — line 86.** Replace `λ ≫ 1` is outside the hypothesis (legs 253, 341).` with:

> `λ ≫ 1` is outside the hypothesis (leg 341's landed record; encoded operatively in
>   `solver/dssp_screen.py` by legs 357/359/362 — leg 253 is cited from narrative only and has
>   no landed JSON).

**(e) III1/III3/III4 — replace §7's opening paragraph and its STILL UNCHECKED blockquote
(lines 209–216) with:**

> The Millennium Prize rules (CMI, 2018 revision) impose **four** conditions in their Section 4,
> not three:
>
> 1. **Publication in a qualifying outlet** — Section 6(a)(i), *"a refereed mathematics
>    **publication** of worldwide repute meeting the conditions in Section 6(e)"*; Section
>    6(a)(ii) admits a second route, *"a publication meeting a relaxed set of conditions
>    approved by the BOD following a recommendation from the SAB"*. Section 6(e)'s conditions
>    include *"inclusion in the list of publications maintained by MathSciNet"*.
> 2. **At least two (2) years** elapsed since publication in a qualifying outlet.
> 3. **General acceptance in the global mathematics community, as determined in the sole
>    discretion of CMI** — Section 4(c). It is a CMI determination, not a community fact;
>    Section 7(a)(i)(4) enumerates what CMI may consider.
> 4. **The Proposed Solution has satisfactorily answered the questions raised by the Problem's
>    official description, as determined in the sole discretion of CMI** — Section 4(d),
>    sharpened by Section 5(d).
>
> Two further facts of planning relevance: Section 5(e) — *"CMI will not accept Proposed
> Solutions submitted directly to CMI"*; and Section 5(b) — for the Navier–Stokes Problem
> *"a resolution in either direction will be evaluated by the standard evaluation procedure set
> forth in Section 7"*, so the breakdown direction this repository pursues is explicitly in
> scope. These are listed so that "the obligations are discharged" is never read as "the problem
> is solved", and because the two-year clock is a planning fact.
>
> > **CHECKED AGAINST THE PUBLISHED RULES — leg 384, HTTP 200**
> > (`millennium_prize_rules_0.pdf`, sha256 `9b500374…`). §7's own "check before relying on it"
> > is discharged.

## 7. What can graduate from DRAFT-UNVERIFIED

On the gate's yes branch, **clause by clause, on integration's edit**: every item (i) clause
except the three named above; all four of §2's screen rows (row 1 with the citation note); and
§7's three prize-rules clauses once (e) lands. The document's **STATUS: DRAFT, UNVERIFIED**
header is integration's to change, not this leg's.

## 8. What this leg did not do

No outreach of any kind. No edit to `CLAY_OBLIGATIONS.md`, to `p2_route_cloc_v1.json`, or to
any solver module. No repair of any discrepancy. No claim of movement toward Clay: **no link of
`L1 → L4` moved, §6's two no-method obligations remain OPEN, and Clay stays ~0.05%.**
