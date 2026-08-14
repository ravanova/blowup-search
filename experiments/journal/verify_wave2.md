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

---

# §3 — WHAT I GOT

*Everything below was written after the numbers existed. §§0–2 were committed at `e93ec51`,
before the first computation.*

## §3.0 How I checked, and why it is not a re-run

The brief forbids reporting the units' own exit codes as verification. I did not run
`p2_route_t4_v1_evidence.py`, `p2_route_t5_sweep.py` or `p2_route_t6_v1.py` as the check. Instead:

* **The primary artefacts were re-fetched and re-measured.** `Papers/` is untracked and was
  **empty** in this worktree, so nothing in items (1)–(3) could be measured from disk. I re-fetched
  all three from their published endpoints (read-only; **no author, group, maintainer or list was
  contacted**) and every digest matched the banked one **exactly**:

  | artefact | HTTP | my sha256 | banked sha256 |
  |---|---|---|---|
  | `arxiv.org/pdf/1902.00384` | 200 | `97e81647e108b8d7…` | `97e81647e108b8d7…` ✔ |
  | VU `navierstokes-code.zip` | 200 | `edf64bc0cf099ed6…` | `edf64bc0cf099ed6…` ✔ |
  | `arxiv.org/pdf/2409.09234` | 200 | `7a3c8ac94b0af865…` | `7a3c8ac94b0af865…` ✔ |

  **This is the part of the run that was worth doing.** Reading (a) said my value is concentrated
  where a number was *transcribed* rather than *measured*; with the artefacts back on disk, items (1)
  and (2) stop being transcription checks and become measurements.
* The `.mat` arrays were decoded from scratch with `scipy.io.loadmat` — variable names discovered by
  inspecting the files, not by reading the unit's decoder.
* The radii were recomputed from the **paper's own (4.33)/(4.34)**, which I read off the re-fetched
  PDF, applied to the authors' published `Y0, Z0, Z1, Z2`.
* Every tally was recounted with `collections.Counter` from the raw `findings` / `verdicts` /
  `fulltexts` lists — never read off a `*_counts` field.
* `T5`'s corpus was re-enumerated with `git ls-tree` + `git cat-file` at the commit that landed the
  artefact — not by calling the sweep's `enumerate_corpus()`.
* The term counts were recounted with a normaliser I wrote before reading theirs.

**One thing I could only check by reading the landed script, and I label it as such:** the `1e-3`
threshold behind the norm check is a module constant of `experiments/p2_route_t4_v1_evidence.py`
(`V4_REPRODUCED = 1e-3`, line 25). There is no independent source for it; my check asserts the
constant is literally `1e-3` and that the measured `δ` is under it.

## §3.1 ITEM (1) — `T4`'s 2D lift — **YES, reproduces exactly**

Measured by me from `dataorbit{1,2}.mat` / `extraorbit{1,2}.mat` inside the re-fetched package, and
from Table 1 of the re-fetched PDF (`pdftotext -layout`, p.46).

| claim | **the number I got** | claimed | |
|---|---|---|---|
| `N_x3` in Table 1, p1 / p2 | **0 / 0** (read by me from the PDF table) | 0 / 0 | ✔ |
| `N_x3` in `Nrec`, p1 / p2 | **`[17,17,0,11]` / `[21,21,0,16]`** | third entry 0 | ✔ |
| `x₃` extent, `ω` / `u` / `p` | **1 / 1 / 1** on both rows | 1 | ✔ |
| `max\|u⁽³⁾\|` p1, p2 | **`0.0`, `0.0`** (zero non-zero entries) | `0.0` exactly | ✔ |
| `max\|ω⁽¹⁾\|`, `max\|ω⁽²⁾\|` | **`0.0`** on all four | `0.0` exactly | ✔ |
| `max\|ω⁽³⁾\|` p1 | **`1.6351073366158`** → `1.6351` | `1.6351` | ✔ |
| `max\|ω⁽³⁾\|` p2 | **`1.5274264613264072`** → `1.5274` | `1.5274` | ✔ |
| `setup` | **`'2D'`** on both | `'2D'` | ✔ |

My independent decode is **bitwise identical** to the banked row on every one of those fields —
including `Ω̄` (`1.652446122134822` / `1.527206870217959`), the shapes, and `Nrec`. The zeros are
structure, not an empty array: `max|ω⁽³⁾|` is non-zero on both rows.

**Nothing transcribed survived unchecked here.** `table1_row` is the one thing the runner marks in a
comment as *"transcribed from the PDF"* (`experiments/p2_route_t4_v1.py:203`) — I re-read the table
myself and every cell of both rows agrees, including the RAM/CPU columns (`10 GB / 6 d`,
`110 GB / 95 d`).

## §3.2 ITEM (2) — the first conjunct and the negative control — **YES, reproduces exactly**

### The paper's criterion (4.32), recomputed

The re-fetched PDF states (4.32) as `Z0+Z1 < 1` **and** `2·Y0·Z2 < (1−(Z0+Z1))²`, with (4.33)/(4.34)
giving `r_min = [1−(Z0+Z1) − √((1−(Z0+Z1))² − 2·Y0·Z2)] / Z2` and **`r_max = [1−(Z0+Z1)] / Z2`**.

**`r_max` is the validity bound, not the larger root.** My §2.2 pre-registered the textbook
`Z2·r² − (1−Z0−Z1)·r + Y0` and its larger root. **That was my error, and I record it as mine, not the
record's** — under it, `p1`'s discriminant goes negative and `r_max` misses by 70 %. Under the
paper's own (4.33)/(4.34) everything reproduces bit-for-bit. Reading (a) warned that agreement is
cheap; this is the one place where a wrong convention would have manufactured a false discrepancy,
and the fix came from the paper, not from the banked file.

| | **my number** | banked | claimed |
|---|---|---|---|
| p1 `Z0+Z1` | **0.9730669503350271** < 1 | same | (4.32) met ✔ |
| p1 `2·Y0·Z2` vs `(1−Z0−Z1)²` | **3.737652e-04 < 7.253892e-04** | same | ✔ |
| p2 `Z0+Z1` | **0.9728800000004357** < 1 | same | ✔ |
| p2 `2·Y0·Z2` vs `(1−Z0−Z1)²` | **1.483107e-05 < 7.354944e-04** | same | ✔ |
| p1 `r_min` rel dev | **2.434836e-10** | 2.434836e-10 | ✔ |
| p1 `r_max` rel dev | **0.0 (exact)** | 0.0 | ✔ |
| p2 `r_min` rel dev | **8.334722e-13** | 8.334722e-13 | ✔ |
| p2 `r_max` rel dev | **5.618065e-15** | 5.618065e-15 | **5.6e-15** ✔ |
| p1, p2 `r_sol^Ω` | **`2.6314e-05`, `2.2491e-06`, rel dev `0.0`** | exact | both exact ✔ |
| norm check `δ` | **5.2748360312e-06** → `5.3e-06` | 5.2748e-06 | **5.3e-06** ✔ |
| threshold | **`V4_REPRODUCED = 1e-3`**, `p2_route_t4_v1_evidence.py:25` | — | **1e-3** ✔ |

My roots are **bitwise identical** to the banked `reproduced` values on all four cells. The gate's
`5.6e-15` reads as *the smallest non-zero deviation of the four*, and that is what it is.

### The apparatus finding and its negative control

Recounted by me over the re-fetched PDF with my own normaliser:

| term | **my count** | banked | claimed |
|---|---|---|---|
| *approximate inverse* | **7** | 7 | 7 ✔ |
| *Newton-Kantorovich* | **4** | 4 | 4 ✔ |
| *interval arithmetic* | **5** | 5 | 5 ✔ |
| *INTLAB* | **2** | 2 | 2 ✔ |
| *self-consistent* | **0** | 0 | 0 ✔ |
| *a priori bounds* | **0** | 0 | 0 ✔ |
| *isolating* | **0** | 0 | 0 ✔ |
| *trapping region* | **0** | 0 | 0 ✔ |
| *logarithmic norm* | **0** | 0 | 0 ✔ |
| *dynamical closure* | **0** | 0 | 0 ✔ |

All six load-bearing verbatim quotes (three apparatus, three 2D) relocated by me in the re-fetched
text. **Zgliczyński: exactly one occurrence of the name in the whole document, and it is bibliography
item `[48]`.**

**Two nuances, banked because they refine a number rather than contradict it:**

1. ***approximate inverse* = 7 is normalisation-sensitive.** Without de-hyphenating a line-break the
   count is **6**. Both the landed runner and my independently written normaliser de-hyphenate, so 7
   stands; the other three C+ counts are insensitive. Anyone re-deriving with a naïve counter will
   get 6 and should not read that as a discrepancy.
2. **The *reference* `[48]` is cited once in the body**, at *"Shivashinsky PDE [1, 9, 10, 48]"* — as
   prior work on Kuramoto–Sivashinsky, never as this paper's method. The *name* appears only in the
   bibliography, which is what the claim says.

## §3.3 ITEM (3) — `T6`'s table — **YES on every count; one wording nuance, unreconciled**

| claim | **my recount** | banked | |
|---|---|---|---|
| full texts read | **7/7 `MEASURED`** | 7 | ✔ |
| verdicts | **2 `UNDERCUT` / 4 strengthen / 1 confirm** | same | ✔ |
| `UNREACHABLE` | **0** | 0 | ✔ |
| `THROTTLED` | **0** | 0 | ✔ |

Recounted with `Counter` from the raw lists, not read off `verdict_counts`; they sum to 7 and use no
verdict outside the pre-registered vocabulary. Every full text carries PDF magic and extracted a
non-empty text (min 30 592 chars) — a "read" that extracted nothing would not have counted.

**UNDERCUT 2 = `arXiv:2409.09234`.** I re-fetched it (sha256 `7a3c8ac9…`, matching), relocated the
banked deciding sentence and both supporting quotes **verbatim**, and read the boundary conditions
myself at sec 2, p.4:

> *"The boundary conditions at the inner and outer cylinder walls 𝑟 = 𝑟ᵢ and 𝑟 = 𝑟ₒ are
> v = 𝑅ᵢ𝜽̂ and v = 𝑅ₒ𝜽̂. Periodicity is enforced to the rest of boundaries of the parallelogram
> domain."*

So the domain is **not** a periodic cell: rotating-wall Dirichlet conditions radially, periodicity
only in the remaining directions. I also measured that the paper contains **zero** occurrences of
*interval arithmetic*, *Newton-Kantorovich*, *Galerkin*, *computer-assisted*, *INTLAB*,
*self-consistent*, *a priori bounds* and *trapping region*.

**The over-count arithmetic reproduces:** `p2_route_pocp_v1.json.domain_census.compact_or_periodic_domain`
lists **6** entries, one of which is `"arXiv:2409.09234 (minimal periodic domain)"`. **6 − 1 = 5.**
Leg 348's record is still exactly as `T6` locked it — both lock hashes re-verified live
(`ef1df364…`, `639e600b…`).

### The nuance, reported and NOT reconciled (reading (b))

**The gate and the banked record give different *grounds* for the same over-count.**

* **The gate's wording:** *"`arXiv:2409.09234` carries no-slip walls, not periodicity, **so** leg
  348's `domain_census` over-counts by one."*
* **The record's own wording** (`p2_route_t6_v1.json`, the `2409.09234` verdict's
  `leg348_classification_status`): the ground is that the paper *"CLOSES NO TAIL-DOMINATION ESTIMATE
  AND IS NOT AN INSTANCE OF THAT TECHNOLOGY AT ALL. The census over-counts by one."* The
  wall/periodicity point is filed as `u_code` **U1**, and the record labels it **"secondary"**.

Both facts are in the record and **both reproduce independently**. What differs is which one carries
the *"so"*. A second, smaller one: **the paper never uses the phrase "no-slip"** (0 occurrences) —
`v = 𝑅ᵢ𝜽̂` at a rotating wall *is* the no-slip condition, but the phrase is the record's, not the
paper's. **I report both readings and stop. Deciding which grounding is the operative one is the
Conductor's job, not mine.**

## §3.4 ITEM (4) — `T5`'s sweep — **YES, reproduces exactly at the landing commit**

**Corpus, re-enumerated by me with `git ls-tree` + `git cat-file` at `3cab83e` (the commit that
landed `writeup/data/p2_route_t5_v1.json`), minus the four `excluded_by_name` entries:**

| | **my number** | banked | claimed |
|---|---|---|---|
| files | **1428** | 1428 | 1428 ✔ |
| lines | **417 476** | 417 476 | 417,476 ✔ |
| bytes | **23 547 210** | 23 547 210 | — ✔ |
| `DIRECTION.md` in corpus | **False** | False | excluded ✔ |

**Corpus drift, recorded so nobody re-derives at HEAD and reports a false discrepancy:** at
`origin/main` the same enumeration gives **1440 files / 421 528 lines**. That is later legs' files,
not a disagreement. The number is a function of the tree, and the tree has moved.

**"and the exclusion asserted executably" — YES.** `experiments/p2_route_t5_sweep.py` carries, at
`:380–381`, `if "DIRECTION.md" in corpus: fail.append("N-B: DIRECTION.md is in the corpus -- S3e
VIOLATED")`, and `main()` ends `if fail: … return 1`. A non-empty `fail` list is a non-zero exit, so
the exclusion is gated by **exit code**, not by a printed line or a promise in prose. The control
`N-B` additionally re-derives the enumeration and compares it set-wise. This half of the claim is the
one most easily satisfied by a comment instead of an assertion; it is satisfied by an assertion.

**Tally, recounted from `findings` with `Counter`:**

| | **my recount** | banked | claimed |
|---|---|---|---|
| refusals | **7** | 7 | 7 ✔ |
| `APPARATUS` | **5** | 5 | 5 ✔ |
| `REALIZATION` | **2** | 2 | 2 ✔ |
| re-openable under C1 | **`['F1','F2']` — exactly 2** | `['F1','F2']` | exactly 2 ✔ |

No `REALIZATION`-based refusal is marked re-openable, and the classification vocabulary is exactly
`{APPARATUS, REALIZATION}`.

**The two re-openables are the two the gate names:**

* **`F1` = leg 348**, `what_was_refused` = *"Proposing the build for a periodic-orbit /
  **Galerkin-plus-tail DYNAMICAL closure** on the T³ object class."* ✔
* **`F2` = leg 315**, `what_was_refused` = *"Dispatching the build leg for **`O1`** — sonic-point-
  desingularized Taylor-model stepping in the similarity parameter."* ✔

**Leg 257 is NOT re-openable, and for the reason the gate states.** `F3`, leg 257, route P1C,
`reopenable = false`. Its `c1_scope_test` reads: *"The apparatus IS radii-polynomial:
`capabilities.py:518-522` records the module as carrying '… plus **Corollary 21's radii
polynomial**' … **A fourth SPACE is not a fourth APPARATUS.** C1 does not reach it."* I relocated the
`capabilities.py` quote live — *"section 6's bounds Y, Zbar11/12/21/22, Z1, Z2, Z3 plus Corollary
21's radii polynomial"* is still there. ✔

**All seven deciding sentences still sit at their recorded `file:line`** in the live tree
(`leg_348.md:122`, `leg_315.md:150`, `JOURNAL.md:3696`, `leg_262.md:150`, `leg_273.md:257`,
`leg_341.md:122`, `leg_315.md:51`) — under the whitespace-normalised 7-line-window rule the sweep
itself uses. My first pass used strict whitespace and reported 0/7; that was **my** comparison being
wrong, and is recorded here so the correction is visible rather than silent.

## §3.5 The field-scoped census (reading (e)) — the filename trap, avoided

Scanned **every** `writeup/data/*.json` on the top-level **fields** `leg` / `route` / `unit` only.
Never on a filename substring.

| | |
|---|---|
| files found / parsed | **306 / 306 — 100 % coverage, none unparseable** |
| top-level `leg` present | **229 / 306 (75.3 %)** |
| top-level `route` present | **225 / 306** |
| top-level `unit` present | **9 / 306** |
| rows with `unit ∈ {T4,T5,T6}` | `p2_route_t4_v1.json` (leg 393), `p2_route_t5_v1.json` (leg 395), `p2_route_t6_v1.json` (leg 394) |
| rows with `leg ∈ {391,393,394,395}` | **only 393, 394, 395 — leg 391 is absent** |
| **`p2_route_p2t1_v1.json`** | **`leg = 302`, `route = "P2T1"`, `unit = null`** — the trap, named in advance, avoided |

*(Counts are taken after V-W2 added its own two files; before them the totals were 304/304, `leg`
229, `route` 225, `unit` 8.)*

**`T1` / leg 391 banked nothing**, confirmed independently by field scan at full coverage. The wave-1
verifier's finding stands. My repair record deliberately carries **no** top-level `leg`/`unit` — it
is a record banked *by* V-W2 *about* leg 391, not leg 391's own, and nests that under `banks_for`, so
the census statement stays true after the repair.

## §3.6 The folded-in obligation — `T1` / leg 391's missing record — **DISCHARGED**

Banked: `writeup/data/p2_route_t1_packet_v1.json`, checked by
`experiments/p2_route_t1_packet_evidence.py` (**31/31, exit 0**).

The record states, **verbatim from
`writeup/escalations/ESCALATION_BAN_WORDING_2026-08-13.md` (sha256 `e73eeca8e49c443b…`, 478 lines)**:

* **the packet's three ban-wording questions** —
  **(a)** Cadiot: the lift clause's literal reading vs its evident purpose;
  **(b)** Stage V's *"needs L1 first"* — a lift condition unliftable as written;
  **(c)** the apparatus question — does the ℓ¹-Fourier/radii-polynomial ban reach a Zgliczyński-style
  Galerkin-plus-tail **dynamical** closure? — each with its *pending since* and *what it blocks*;
* the fourth item **(d)** (the outreach hold), banked **separately** because the document itself says
  it is *"Not a ban-wording question"*;
* **that it ruled NONE of them**: `questions_ruled = 0` of 3, backed by the document's own
  *"**This packet rules nothing.**"* and *"**It ruled none of (a), (b), (c).**"*

The script asserts each question occurs **verbatim** in the document, re-hashes the document, and
independently regex-scans for any endorsement verb attached to the packet (none). **Per reading (f),
the record carries no gate verdict and is explicitly marked `does_not_reopen_t1_gate_answer: true`.**
It says what the packet **asked** and that it **ruled none**. Nothing more.

**Mutation-tested, as required:**

| mutation | result |
|---|---|
| baseline | **exit 0** |
| corrupt question (c)'s verbatim text (`dynamical` → `DYNAMICAL`) | **exit 1**, `FAIL question (c) occurs VERBATIM…` |
| set `questions_ruled = 1` | **exit 1**, `FAIL banked count of questions RULED is zero` |
| bank only two questions | **exit 1**, `FAIL exactly THREE ban-wording questions are banked` |
| restored | **exit 0** |

My own gate, `experiments/p2_verify_wave2_evidence.py`, is **100/100 checks OK, exit 0**, with 2
checks reported `skip` (see §4.2) and was mutation-tested the same way: corrupting my banked
`max|ω⁽³⁾|` for p1 gives **exit 1**.

# §4 — VERDICTS, AND WHAT I COULD NOT CHECK

| item | verdict | the number that decides it |
|---|---|---|
| **(1)** `T4`'s 2D lift | **YES — reproduces exactly** | `max\|u⁽³⁾\| = max\|ω⁽¹⁾\| = max\|ω⁽²⁾\| = 0.0`, `max\|ω⁽³⁾\| = 1.6351 / 1.5274`, `N_x3 = 0`, extent 1, `setup='2D'` — all **bitwise identical** to a fresh decode of the re-fetched package |
| **(2)** first conjunct + control | **YES — reproduces exactly** | `5.618065e-15` smallest non-zero; `δ = 5.2748e-06 < 1e-3`; 7 / 4 / 5 / 2 and six zeros; `[48]` |
| **(3)** `T6`'s table | **YES on every count** | 7/7, 2/4/1, 0, 0; `6 − 1 = 5` — **plus one wording nuance banked unreconciled** |
| **(4)** `T5`'s sweep | **YES — reproduces exactly at `3cab83e`** | 1428 / 417 476; 7, 5, 2; exactly 2; leg 257 not re-openable |
| folded-in `T1` obligation | **DISCHARGED** | 3 questions, 0 ruled; evidence script exit-code gated and mutation-tested |

## §4.1 Unreconciled — reported, not decided

**One.** Item (3): the gate grounds the `domain_census` over-count in the **no-slip walls**; the
banked record grounds it in the paper **not being an instance of the certification technology at
all**, and files the wall point as a *secondary* `u_code`. Both facts reproduce independently. Which
grounding is operative is **the Conductor's call, not mine** (reading (b)). See §3.3.

## §4.2 `UNVERIFIABLE` / not checkable by this unit

* **`corpus.DIRECTION_md_windows_forgone = 143`** (`p2_route_t5_v1.json`). Checking it requires
  reading `DIRECTION.md`, which is on my forbidden-read list. **`UNVERIFIABLE BY THIS UNIT`** — not a
  `no`, and not in the gate.
* **Every "why".** The reasoning behind any wave-2 number is in files I may not open. I checked
  *what* the numbers are and *whether they re-derive*; I did not and cannot check *whether the
  reasoning that produced them was sound*. That is the trade the unit is for.
* **Two live re-measurements are `skip`, not `pass`, in my evidence script.** `Papers/` is untracked,
  so a fresh clone cannot re-decode the `.mat` files or re-count the PDF. My script reports those two
  as `skip` with the banked sha256 rather than silently passing them. The measurement itself is
  banked in `p2_verify_wave2_v1.json` under `independent_artefacts_refetched`, digests included.

## §4.3 Two errors of mine, recorded because a verifier that hides its own misses is worthless

1. **The pre-registered radii formula (§2.2) was wrong.** I fixed the convention from the paper's own
   (4.33)/(4.34), not from the banked file, and then everything reproduced bit-for-bit. Had I
   reported the pre-registered version, I would have banked a 70 % false discrepancy on `r_max`.
2. **My first quote-location pass used strict whitespace and reported 0/7 for `T5`'s findings.** The
   sweep's own rule — and the correct one — normalises whitespace over a 7-line window. All 7 verify.

## §4.4 Forbidden reads — honoured

I did **not** open `STATE.md`, `WALLS.md`, `OPTIONS.md`, `DIRECTION.md`, `CLAY_ROADMAP.md`,
`reports/ORCH_STATE.md`, any wave-2 brief, or **any part** of `experiments/journal/leg_393.md`,
`leg_394.md` or `leg_395.md` — not even for locators; I never needed one, because every discrepancy
candidate resolved inside the JSON or the primary sources.

Journal files I *did* open, locator-only, to confirm a banked quote sits at its recorded line:
`experiments/journal/leg_348.md`, `leg_315.md`, `leg_273.md`, `leg_341.md`, `experiments/JOURNAL.md`,
`writeup/novelty/leg_262.md`. None is a wave-2 journal.

## §4.5 Outreach

**Read-only.** Three HTTP GETs against published-document endpoints (`arxiv.org` ×2,
`math.vu.nl` ×1), all HTTP 200, all digest-matched. **No author, group, maintainer or mailing list
was contacted**; that remains HELD by the user. No source was throttled and none was unobtainable, so
no `THROTTLED` and no `UNREACHABLE` is banked — and no zero was banked in place of either.

# §5 — TERRITORY, CEILING

## §5.1 What I wrote

`experiments/journal/verify_wave2.md`, `writeup/data/p2_verify_wave2_v1.json`,
`experiments/p2_verify_wave2_evidence.py`, and — for the folded-in obligation only —
`writeup/data/p2_route_t1_packet_v1.json` and `experiments/p2_route_t1_packet_evidence.py`.

**No source, no figure, no Conductor-owned file. I edited no wave-2 artefact** — not one byte of
`p2_route_t4_v1.json`, `p2_route_t5_v1.json`, `p2_route_t6_v1.json`,
`p2_route_t6_v1_leg348_lock.json` or their scripts. The one thing I found that differs is written
down as a finding in §3.3, not fixed in place.

*(One environment side effect, gitignored and outside the repo's tracked surface: `scipy` was
installed into the shared `.venv`, because reading the authors' `.mat` files needs it and it was
missing. No tracked file changed.)*

## §5.2 Ceiling

**TIER 2. Clay ~0.05 %, unchanged.**

This unit moved **no** link of the `L1 → L4` chain, and could not have. Re-deriving four banked
findings and repairing one missing record changes what the repository can be **trusted to have
measured** — it does not change what the repository has **proved**. A verifier that agreed with
everything would have been worth little (reading (a)); this one agreed with everything in the gate
and found, on top of that, a divergence between the gate's stated ground for an over-count and the
record's, a normalisation sensitivity in a term count, and the confirmation by field-scoped scan that
`T1` really did bank nothing. None of that is progress toward Clay in either direction.
