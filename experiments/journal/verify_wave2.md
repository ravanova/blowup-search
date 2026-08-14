# V-W2 — the wave-2 verifier (branch `verify/wave2`)

No figure. No leg number. A dispatched verification worker with no memory of how `T4`, `T6`
or `T5` were built, re-deriving their claims from the banked JSON and the landed evidence
scripts alone.

**§§0–2 of this file were committed BEFORE any number was computed.** §3 onward is the
re-derivation and was written after.

---

## §0 — THE GATE, verbatim, as committed to `main` before this unit existed

> Re-deriving **from the banked JSON and the landed evidence scripts alone**, does each of the following reproduce **exactly**?
>
> **(1) `T4`'s 2D-lift finding** about `arXiv:1902.00384`: `N_x3 = 0` in Table 1 and in `Nrec`; decoded coefficient arrays of **extent 1** in `x₃`; `max|u⁽³⁾| = max|ω⁽¹⁾| = max|ω⁽²⁾| = 0.0` **exactly** while `max|ω⁽³⁾| = 1.6351 / 1.5274`; `setup = '2D'`.
>
> **(2) `T4`'s first conjunct and its negative control:** criterion (4.32) verified on both rows, `r_min`/`r_max` relative deviations down to **`5.6e-15`**, both `r_sol^Ω` exact, an independent norm check at **`δ = 5.3e-06`** against a **`1e-3`** threshold; and the apparatus finding with its control — term counts *approximate inverse* **×7**, *Newton-Kantorovich* **×4**, *interval arithmetic* **×5**, INTLAB **×2**, against **all six** closure terms (*self-consistent*, *a priori bounds*, *isolating*, *trapping region*, *logarithmic norm*, *dynamical closure*) at **zero**, and Zgliczyński appearing only as bibliography item **[48]**.
>
> **(3) `T6`'s table:** **7/7** full texts read, **2 UNDERCUT / 4 strengthen / 1 confirm**, **0** `UNREACHABLE`, **0** `THROTTLED`; and **UNDERCUT 2** — `arXiv:2409.09234` carries **no-slip walls, not periodicity**, so leg 348's `domain_census` **over-counts by one**.
>
> **(4) `T5`'s sweep:** corpus **1428** tracked `*.md`+`*.py` / **417,476** lines with `DIRECTION.md` excluded by name **and the exclusion asserted executably**; **7 refusals, APPARATUS 5 / REALIZATION 2**; **exactly 2** re-openable under ruling C1 (leg 348's Galerkin-plus-tail build, and leg 315's `O1`); and **leg 257 NOT re-openable** — its apparatus is the Corollary-21 radii polynomial in a fourth **space**.
>
> **yes →** each reproduces; say so per item, **with the number you got**.
> **no →** name the item, the number you got, the number claimed, and the **file and line** the discrepancy is in. **A DISCREPANCY IS THE DELIVERABLE, NOT A FAILURE OF THE UNIT.**
>
> **AND ONE OBLIGATION FOLDED IN, found by the wave-1 verifier and owed since 2026-08-13:** **`T1` / leg 391 banked NO machine record** — no JSON, no evidence script — so its gate answer checks out against **prose only**. **Bank the packet's three questions and the fact that it ruled NONE of them, with an evidence script that EXITS NON-ZERO on disagreement with `writeup/escalations/ESCALATION_BAN_WORDING_2026-08-13.md`.**

## §1 — THE PRE-COMMITTED READING, verbatim

> **(a) AGREEMENT IS THE EXPECTED OUTCOME AND IS WORTH LITTLE ON ITS OWN.** Parts of (1)–(3) were re-derived once at landing. **Your value is concentrated wherever a number was transcribed rather than measured** — find those.
> **(b) A DISAGREEMENT IS BANKED AS A DISAGREEMENT AND IS NOT RECONCILED BY YOU.** Report both numbers and **stop**. Deciding which is right is the Conductor's job, and doing it inside the verifier destroys the independence you exist for.
> **(c) A CLAIM THE JSON CANNOT SUPPORT IS `UNVERIFIABLE`, NOT `no`** — and that is a finding about **banking discipline**, which lesson 68 says decays at the rate of memory. It is exactly how `T1`'s missing record was found.
> **(d) THE FORBIDDEN-READ LIST ABOVE IS BINDING.** That narrowness **is** the unit. State in your journal that you honoured it, and name anything you were unable to check because of it.
> **(e) THE FILENAME TRAP, NAMED IN ADVANCE BECAUSE THE RECORD ALREADY WARNS ABOUT IT:** `writeup/data/p2_route_p2t1_v1.json` is **leg 302, route P2T1 — unrelated to `T1`**. **Do not match on filename substrings.** Scan the `leg` / `route` / `unit` **fields** of every banked JSON, and report your scan as a field-scoped census with its coverage.
> **(f) BANKING `T1`'s RECORD DOES NOT RE-OPEN `T1`'s GATE ANSWER** and is not evidence for or against it. The record states what the packet **asked** and that it **ruled none of the three questions**. Nothing more.
> **(g) CEILING.** Verification moves no `L1 → L4` link. **Tier 2; Clay ~0.05%**, and your write-up says so in its own words.

## §2 — DERIVATION PATHS, FIXED IN ADVANCE

Fixed before any number existed. Where a path turns out to be impossible, the outcome is
`UNVERIFIABLE` / `UNREACHABLE` / `UNDER-RESOURCED`, never a `no` (reading (c), §3d).

### §2.1 Item (1) — `T4`'s 2D lift
Source: `writeup/data/p2_route_t4_v1.json`. For `lab ∈ {p1, p2}`:

| claim | field I will read | my computation |
|---|---|---|
| `N_x3 = 0` in Table 1 | `rows[lab].table1_row.Nx3` | `== 0` |
| `N_x3 = 0` in `Nrec` | `rows[lab].solshape_Nrec[2]` | `== 0` |
| and in the control | `controls.C_3D.p1_Nx3`, `.p2_Nx3` | `== 0` |
| extent 1 in `x₃` | `rows[lab].dimensionality.x3_mode_extent`, and axis 2 of `omega_shape`, `u_shape`, `p_shape` | all `== 1` |
| `max|u⁽³⁾|`, `max|ω⁽¹⁾|`, `max|ω⁽²⁾|` | `dimensionality.max_abs_u3`, `.max_abs_omega1`, `.max_abs_omega2` | `== 0.0` under `float.__eq__`, and `repr` is `0.0` (not `-0.0`, not `1e-320`) |
| `max|ω⁽³⁾| = 1.6351 / 1.5274` | `dimensionality.max_abs_omega3` | round to 4 d.p. and compare to `1.6351` (p1) / `1.5274` (p2) |
| `setup = '2D'` | `dimensionality.setup_field_in_authors_output` | `== "2D"` |

**Independent (non-transcription) leg, pre-registered:** the numbers above are decoded from
`Papers/ns_code/.../saveddata/*.mat`, which are **not tracked in the repo**. I will attempt
to re-fetch `https://www.math.vu.nl/~janbouwe/code/navierstokes/navierstokes-code.zip`
(reading published material is authorised; contacting nobody), verify its `sha256` against
`target_paper.code_zip_sha256`, and **re-decode `max|u⁽³⁾|`, `max|ω⁽ⁱ⁾|`, the array shapes
and the `setup` field myself with `scipy.io.loadmat`.** If the fetch fails I bank
`UNREACHABLE` for the independent leg and state explicitly that the JSON-level check is a
**transcription check, not a measurement**.

### §2.2 Item (2) — the first conjunct and the negative control
Source: same JSON, plus `experiments/p2_route_t4_v1_evidence.py` for the threshold constant.

1. **Criterion (4.32), recomputed by me, not read.** From `rows[lab].published_bounds`
   (`Y0, Z0, Z1, Z2`) I compute `Z0+Z1 < 1` and `2·Y0·Z2 < (1−Z0−Z1)²` myself, and compare
   my booleans with `paper_criterion_4_32.criterion_met`.
2. **`r_min` / `r_max`, recomputed by me from the radii polynomial**
   `p(r) = Z2·r² − (1−Z0−Z1)·r + Y0`, roots `r± = [(1−Z0−Z1) ∓ √Δ] / (2·Z2)`,
   `Δ = (1−Z0−Z1)² − 4·Y0·Z2`. Relative deviation
   `|r_mine − r_published| / |r_published|` against `rows[lab].r_{min,max}.published`, and
   separately I recompute `rel_dev` from the banked `reproduced` vs `published` pair. The
   gate's `5.6e-15` is read as **the smallest non-zero relative deviation over the four
   `r_min`/`r_max` cells**; I report all four.
3. **`r_sol^Ω` exact:** `rows[lab].r_sol_Omega.rel_dev_vs_printed == 0.0` for both, and
   `reproduced == printed_in_paper` as floats.
4. **Norm check `δ`:** `rows.p2.norm_u_X` — I recompute
   `|computed_from_published_data − implied_by_printed_radii| / implied_by_printed_radii`
   and compare with the banked `rel_dev`; round to 2 s.f. and compare to `5.3e-06`. The
   `1e-3` threshold is read from `V4_REPRODUCED` in `experiments/p2_route_t4_v1_evidence.py`
   (module-level constant, pre-committed there) — I assert it is literally `1e-3`.
5. **Term counts:** `controls.C_plus.term_counts` for `approximate inverse` (7),
   `newton-kantorovich` (4), `interval arithmetic` (5), `intlab` (2);
   `controls.C_minus.term_counts` for all six closure terms `== 0`; and
   `controls.C_minus.zgliczynski_mentions` — I assert exactly one entry and that it starts
   with the bibliography marker `[48]`, plus `zgliczynski_only_in_bibliography is True`.
   **Independent leg:** re-fetch `https://arxiv.org/pdf/1902.00384`, check `sha256` against
   `target_paper.pdf_sha256`, and **re-run the term counts myself** over `pdftotext -layout`
   output using the counting convention I can read off
   `experiments/p2_route_t4_v1.py`. Same `UNREACHABLE` rule as §2.1.

### §2.3 Item (3) — `T6`'s table
Source: `writeup/data/p2_route_t6_v1.json`.
- **7/7 full texts:** recount `len(fulltexts)` and `sum(1 for f in fulltexts if f.status == "MEASURED")` myself; cross-check `summary_fetch.n_fulltext_MEASURED`, `.n_fulltext_UNREACHABLE == 0`, `.n_fulltext_THROTTLED == 0`. Also assert every `fulltexts[i].is_pdf_magic` and `chars_extracted > 0` (a "read" that extracted nothing is not a read).
- **2 UNDERCUT / 4 strengthen / 1 confirm:** recount from `verdicts[*].verdict` with
  `collections.Counter` and compare against `verdict_counts`. Assert the three counts sum to 7 and that no verdict string falls outside the four names in `verdict_rules`.
- **UNDERCUT 2:** locate the `verdicts` entry with `id == "2409.09234"`; assert
  `verdict == "UNDERCUT"`; read its `deciding_sentence` / `u_codes` / `locator` and assert
  the deciding sentence contains a no-slip-wall statement and **not** periodicity.
- **"leg 348's `domain_census` over-counts by one":** open `writeup/data/p2_route_pocp_v1.json`
  (leg 348's own banked record — a `writeup/data/*.json`, permitted), locate its
  `domain_census`, and check arithmetic: the periodic count minus one. I also verify the
  `leg348_lock` hashes in `writeup/data/p2_route_t6_v1_leg348_lock.json` against the live
  files, since the over-count claim is only meaningful against the locked leg-348 record.
- **Independent leg:** the extracted texts (`Papers/t6_text/*.txt`) are not tracked. I will
  attempt to re-fetch `arXiv:2409.09234`'s full text and re-locate the deciding sentence
  myself. Failure ⇒ `UNREACHABLE` for the independent leg, transcription-level for the rest.

### §2.4 Item (4) — `T5`'s sweep
Source: `writeup/data/p2_route_t5_v1.json` + `experiments/p2_route_t5_sweep.py`.
- **Corpus:** re-enumerate **myself**, not by re-running the sweep: `git ls-files` at the
  commit that landed `writeup/data/p2_route_t5_v1.json` (found with `git log -1 --` on that
  path), filtered to `*.md` and `*.py`, minus the four `excluded_by_name` entries; count
  files and total lines. Compare with `corpus.files_enumerated` (1428) and `corpus.lines`
  (417476). I will report **both** the count at the landing commit and at `origin/main` HEAD
  if they differ, and will not treat later drift as a discrepancy.
- **`DIRECTION.md` excluded by name AND asserted executably:** assert
  `"DIRECTION.md" in corpus.excluded_by_name`, `corpus.DIRECTION_md_excluded is True`, and
  the control `controls["N-B"].direction_md_in_corpus is False`; and separately **grep the
  landed sweep/evidence script for an executable assertion** that fails when `DIRECTION.md`
  enters the corpus (an assert / check whose falsity changes an exit code). If only a
  comment or a printed line exists, that half is a **`no`**.
- **Tally:** recount from `findings[*].classification` — `APPARATUS` and `REALIZATION` —
  and `len(findings)`; compare with `tally.refusals` (7) / `apparatus_based` (5) /
  `realization_based` (2). Recount `[f.id for f in findings if f.reopenable]` and compare
  with `tally.reopenable_under_C1` (`["F1","F2"]`), asserting `len == 2`.
- **The two re-openables are the right two:** `F1` must be leg **348** and its
  `what_was_refused` must name the Galerkin-plus-tail dynamical closure; `F2` must be leg
  **315** and must name `O1`.
- **Leg 257 NOT re-openable:** find the finding with `leg == 257`; assert
  `reopenable is False`; assert its `why` / `c1_scope_test` names **Corollary 21**, a
  **radii polynomial**, and a **fourth space** (the gate's emphasis: *space*, not *time* /
  *scale* / *norm*). Verify the quote at its recorded `file:line` in the live tree.

### §2.5 The folded-in `T1` obligation
- Read `writeup/escalations/ESCALATION_BAN_WORDING_2026-08-13.md` in full.
- Bank, in `writeup/data/p2_route_t1_packet_v1.json`: the **three questions verbatim**, the
  fact that the packet **ruled none of the three**, the doc's `sha256`, and — per reading
  (f) — an explicit `does_not_reopen_t1_gate_answer: true` marker with no gate verdict.
- `experiments/p2_route_t1_packet_evidence.py` **re-reads the escalation document** and
  asserts (i) each banked question occurs **verbatim** in it, (ii) the banked count of
  ruled questions is `0` and no ruling/decision marker for any of the three appears in the
  doc, (iii) the doc `sha256` matches. Any failure ⇒ **exit 1**. I will mutation-test it by
  corrupting one banked question and showing exit code 1.

### §2.6 The field-scoped census (reading (e))
Scan **every** `writeup/data/*.json`; for each, read the top-level fields `leg`, `route`,
`unit` (and only those — no filename matching). Report: total files, how many carry each
field (coverage), the rows whose `unit` is in `{T1,T4,T5,T6}`, the rows whose `leg` is in
`{391,393,394,395}`, and explicitly what `p2_route_p2t1_v1.json`'s own fields say.

### §2.7 My own gate
`experiments/p2_verify_wave2_evidence.py` re-runs every check above from the banked JSON and
**exits non-zero** on any failure (lesson 68). `scripts/merge_gate.sh origin/main` must PASS.

### §2.8 Forbidden reads
I have not opened and will not open `STATE.md`, `WALLS.md`, `OPTIONS.md`, `DIRECTION.md`,
`CLAY_ROADMAP.md`, `reports/ORCH_STATE.md`, any wave-2 brief, or the reasoning sections of
`experiments/journal/leg_393.md`, `leg_394.md`, `leg_395.md`. Journal reads, if any, are
locator-only and are declared in §5.
