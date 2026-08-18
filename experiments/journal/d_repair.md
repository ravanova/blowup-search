# D-REPAIR — wave 5, infrastructure unit, branch `repair/wave3-defects`

Repairs exactly the defects `V-W3` located (`experiments/journal/verify_wave3.md` §4, **D2–D6**)
and the four Conductor debts held open until `V-W3` returned, then answers — mechanically, with the
check left behind as an executable script — whether `writeup/build_figures.py` self-checks every
figure the record cites.

**This unit moves nothing toward Clay.** Repairing infrastructure does not move an `L1→L4` link and
is not progress. Ceiling: **TIER 0, infrastructure**. `L1→L4` links moved: **0**. Clay: **unchanged**.

---

## §0 — THE GATE AS GIVEN (committed before anything was touched)

`writeup/waves/WAVE5_PLAN.md` @ `1e49a00`, section `## D-REPAIR — infrastructure`, verbatim:

> Repair EXACTLY the defects `V-W3` located and no others (`experiments/journal/verify_wave3.md`
> §4, D2-D6), plus the four Conductor debts held open until `V-W3` returned so as not to destroy a
> live measurement: register `fig107` AND `p2_route_t6_v1_evidence.py` in `P2_EVIDENCE` in
> `writeup/build_figures.py`; add `writeup/INDEX.md` rows for `E` and `V-W2`; reconcile
> `INDEX.md`'s stale in-flight figure allocation table. Then answer, MECHANICALLY and with the
> check left behind as an executable script: DOES `build_figures.py` SELF-CHECK EVERY FIGURE THE
> RECORD CITES — YES OR NO, WITH THE ENUMERATION?

### Pre-committed readings — binding

**(a) REPAIR ONLY WHAT IS LISTED.** Anything else found is REPORTED, NOT REPAIRED — a new defect is
a new unit. It goes in §8 as a flag to the Conductor and is applied nowhere.
**(b) NO BANKED ARTEFACT MAY BE REWRITTEN TO MATCH A LATER FINDING.**
`writeup/data/p2_route_vbs_v1_scoping.json::the_empty_cell.meaning` is measured FALSE and is
EXPLICITLY OUT OF SCOPE — question (Q3) of an open user escalation
(`writeup/escalations/ESCALATION_W3_WORDING_2026-08-18.md`). **NOT TOUCHED.**
**(c)** If a listed defect turns out NOT TO EXIST, say so plainly — that is a finding about the
verifier and is worth more than a silent no-op.
**(d)** `bash scripts/merge_gate.sh origin/main` must print `MERGE GATE: PASS`.
**(e) Lesson 68:** a check that is not executable decays. Leave the check RUNNABLE, and RUN it.

D1 is **out of scope**: already corrected by the Conductor in `STATE.md` and `OPTIONS.md`, which are
the Conductor's files and were not opened for writing by this unit. Nor were `WALLS.md`,
`ORCHESTRATION.md` or `reports/`.

---

## §1 — METHOD

1. **The check was written and committed BEFORE any repair** (`b3be9ac`), so its pre-repair output is
   in the record and the repairs cannot be tuned to it after the fact.
2. **`V-W3`'s `fig107` measurement was reproduced independently before anything changed**:
   `P2_EVIDENCE` held **36** entries with ids `[48…82, 99–106, 108, 109, 110]`; **107 is the only gap
   in 99–110**; `fig107` appeared in **0 string tokens** and **2 comment tokens**; the drawing script
   and the `.png` both exist and `INDEX.md` cites the figure. Confirmed, exactly as `V-W3` recorded.
3. **One commit per defect, with the defect id in the message.** Wave 3 lost three units of four to a
   host process exit and only committed work survived. Commits on this branch, in order:

   | commit | what it discharged |
   |---|---|
   | `b3be9ac` | the executable check + its pre-repair baseline (lesson 68), **before** any repair |
   | `994758d` | **D6** + debts 1a and 1b (`fig107`, `p2_route_t6_v1_evidence.py`) |
   | `401e657` | **D3**, *superseded by `f70a21e`* — its arithmetic reproduced `V-W3`'s convention mix |
   | `f70a21e` | **D4**, and **D3**'s arithmetic corrected; says in its own message that it supersedes `401e657` |
   | `dbd9d83` | **D5** |
   | `c8223dd` | debts 2 and 3 (`INDEX.md` rows for `E` and `V-W2`; the allocation table reconciled) |

4. **Corrections are marked, never hidden** (`writeup/CORRECTIONS.md`). Every repair to a *banked
   journal* is a `>` blockquote **beside** the standing original wording. **No banked line was
   edited to agree with a later finding**, and no banked JSON was written to at all.
5. `.venv/bin/python` throughout.

---

## §2 — PER DEFECT

### D2 — "the stated derivation of `0.57` does not evaluate to `0.57`". **DOES NOT EXIST ANY MORE.**

*Located at* `STATE.md:179` and `OPTIONS.md:73`. Reading (c) applies, plainly:

**The defect is not there.** The Conductor's D1 correction removed the `(5.687 + 0.806)/16`
derivation from both located sites; there is no surviving text at either location that states a
derivation of `0.57`. The two files are also the Conductor's and off-limits to this unit for
writing, so even had the text survived, the repair would have been a report.

**Nothing was changed for D2.** This is a finding about the *ordering* of the wave, not about the
verifier's accuracy: `V-W3` measured D2 correctly at the time it measured it, and the Conductor's
D1 fix then dissolved D2 as a side effect. A defect list is a **measurement with a timestamp**, and
this one aged out between landing and repair.

### D3 — "the structural explanation for the overrun is contradicted by both ledgers". **REAL. Repaired — and `V-W3`'s SIZE AND DIRECTION are wrong.**

*Located at* `experiments/journal/prog_r4_e.md:394-397` and `:474-476`.

`V-W3` recorded "E used **2.3% fewer** epochs per attempt". That compares **`E`'s `n_iters`
convention** (343/16 = 21.4375) against **U5's ledger-row convention** (2195/100 = 21.95). Like for
like, in a single convention, the sign flips:

| basis | U5 | `E` | `E`/U5 |
|---|---|---|---|
| epochs/attempt, `n_iters` convention | 21.04 | 21.4375 | **1.0189** (+1.9%) |
| epochs/attempt, ledger-row convention | 21.95 | 22.3125 | **1.0165** (+1.7%) |
| core-seconds/attempt | — | — | **0.9958** |
| realised s/epoch | — | 95.389 | **1.0041** vs the banked 95 s model |

So `E` used **slightly more** epochs per attempt, not fewer, and still cost marginally **less** per
attempt in core-seconds, because its realised seconds-per-epoch is within **0.41%** of the
commissioned 95 s model. **D3's conclusion survives and is strengthened**: the structural
explanation for an "overrun" is contradicted by both ledgers in either convention. Only its number
is wrong.

*Repair:* two `>` correction blocks in `experiments/journal/prog_r4_e.md`, one after the §10
"commissioned model was ~0.0713" paragraph and one after §12(d), each carrying the like-for-like
table above. The §10 block also contains "**A finding about the verifier, reported not ruled**" —
D3's size and sign — and a "**NOT repaired here, and deliberately**" note recording that the `~8×`
residue at `writeup/4_p2_lottery/TECHNICAL_P2_PROGR4_HHARD.md:212` is **D1**, out of scope, flagged
and not fixed. The original wording stands untouched above both blocks.

### D4 — "`prog_r4_u5.md`'s epoch count disagrees with its own ledger". **REAL AS A DISCREPANCY, BUT IT IS A CONVENTION, AND IT RECONCILES EXACTLY.**

*Located at* `experiments/journal/prog_r4_u5.md:405` — "2,104 epochs / 100 attempts" against a
ledger holding **2195**.

The difference is **91 rows and it has zero residue**. The rule, attempt by attempt: a **converged**
attempt has `len(ledger) == n_iters`; a **non-converged** attempt has `len(ledger) == n_iters + 1`,
the extra row being the final evaluated-but-not-accepted state. U5 had **9** converged attempts of
100, so `2195 − 2104 = 91 = 100 − 9`. `E` reproduces the same rule: `357 − 343 = 14 = 16 − 2`.

**`:405` was therefore NOT changed to 2195.** Doing so would have (i) contradicted U5's own banked
JSON and (ii) **broken three landed executable checks that assert 2104** —
`experiments/p2_prog_r4_m3_evidence.py:212` and `:222`,
`experiments/p2_prog_r4_r0r1_evidence.py:238`, and
`experiments/programme_r4/r1_flatness.py:173`.

*Repair:* a `>` correction block after the "Cost basis, measured this run, not estimated" paragraph
at `:405`, stating explicitly that the line is **not** changed, giving the two-convention table and
the exact rule, and citing the three checks by file and line so the next reader cannot re-open this
by grep.

### D5 — "`E`'s two cost figures do not reconcile and the artefact cannot close the gap". **THE GAP IS REAL. THE "CANNOT" IS NOT — IT RECONCILES, FROM THE BANKED RECORD ALONE.**

*Located at* `writeup/data/p2_prog_r4_e_v1.json`: `diagnostic_3.resourcing.core_hours` = **5.687**
against `sum(attempts[].wall_seconds)` = **9.0884** core-hours over the same 16 rows.

Two independent facts close it, and both are already in the banked JSON:

1. **`core_hours` is pool OCCUPANCY, not CPU consumed.**
   `wall_seconds × workers / 3600 = 2047.4409 × 10 / 3600 = 5.6873` — the banked figure to four
   decimals. Occupancy counts idle workers; the sum of attempt walls counts only CPU.
2. **The relaunch subset IS recoverable**, by a bound the record cannot violate: **no attempt can
   outlast the window that contains it.** `resourcing.wall_seconds` = 2047.4409 s matches attempt
   11's own wall (2047.4169 s) to **0.024 s** (1.2e-5 relative), so attempt 11 is the window's
   longest member. The **8** attempts with wall > 2047.4409 s — `{0,1,2,3,4,6,7,8}` — therefore
   **cannot** have been in the relaunch. That leaves `{5,9,10,11,12,13,14,15}`, and it is exactly
   the 8 attempts §12(e) independently says were reused from checkpoint.

| | core-seconds | core-hours |
|---|---|---|
| relaunched 8, CPU consumed | 12,601.38 | **3.5004** |
| inherited 8, CPU consumed | 20,116.96 | **5.5880** |
| all 16, CPU consumed | 32,718.33 | **9.0884** |
| relaunch window, pool occupancy (= banked `core_hours`) | 20,474.41 | **5.6873** |

The relaunch window was **61.5% busy, 38.5% idle**. The 3.4011 core-hour gap (37.4% of the larger,
matching `V-W3`'s size exactly) is **5.588 h omitted** plus **2.187 h of idle added**.

**What this unit cost, stated once: 9.0884 core-hours of attempt CPU plus 0.8057 h of planted
controls.**

*Repair:* a `>` correction block in `experiments/journal/prog_r4_e.md` after "What was actually
spent", carrying the recovery, the four-row table, the single cost statement, and a note that
**D5's size holds and D5's ceiling does not** — `V-W3` recorded "not recoverable from the record",
and it is recoverable. The banked JSON was **not** modified: reading (b).

### D6 — "`fig107` is not registered in `P2_EVIDENCE`". **REAL. REPAIRED.**

*Located at* `writeup/build_figures.py`. Reproduced independently before repair (§1.2).

*Repair:* `writeup/figures/fig107_prog_r4_m3_shift_strata.py` added to `P2_EVIDENCE`. It redraws
from `writeup/data/p2_prog_r4_m3_v1.json` (plus `p2_prog_r4_g1_v1.json`, read-only, for the U3
baseline) alone and carries **16 self-checks**. After the repair `fig107` appears in both `REBUILT`
and `SELF-CHECKED`. A documented **ENTRY FORMS** comment block was added above the list, because the
list now carries three shapes.

---

## §3 — THE FOUR HELD DEBTS

| # | debt | state |
|---|---|---|
| 1a | register `fig107` in `P2_EVIDENCE` | **DISCHARGED** (`994758d`) — this is D6 |
| 1b | register `p2_route_t6_v1_evidence.py` in `P2_EVIDENCE` | **DISCHARGED** (`994758d`), with a new entry form; see below |
| 2 | `writeup/INDEX.md` rows for `E` and `V-W2` | **DISCHARGED** (`c8223dd`) |
| 3 | reconcile `INDEX.md`'s stale in-flight figure allocation table | **DISCHARGED** (`c8223dd`) |

**1b needed a new entry form, and the reason matters.** `experiments/p2_route_t6_v1_evidence.py`
exits non-zero without **seven full-text PDFs that are gitignored**, and those seven are absent from
this worktree *and* from the main checkout. Registering it naively would have made the rebuild abort
on any clean checkout — a repair that breaks the thing it repairs. `P2_EVIDENCE` now accepts a third
form, `(path, args, required_inputs)`; when a required input is absent the runner **prints
`SKIP … (N required input(s) absent, gitignored: …)`, counts it, and lists every skipped entry in a
block at the end**. It is never silently passed and it never aborts the rebuild. It is registered as
a **verification**, with no figure — `V-W2` established that a registered "none" is a legitimate §6
quartet entry.

**Debt 2.** Two Arc-4 rows. `E` (leg 380, wave 1): full quartet, `fig109`, landed `d0d72b1`,
**VERIFIED by `V-W3`**, and the row says in its own text that it was **withheld until `V-W3`
returned**; ceiling TIER 2, no `L1→L4` link moved. `V-W2` (wave 3): a verification lane, so B/T is
**n/a** and the figure cell is **none** — a verification produces no curve; landed `594ff89`, the
one unit of four that survived wave 3's host process exit.

**Debt 3.** The allocation table is reconciled **against the files, not re-adjudicated**. Every
`State` cell is now a mechanical fact — `git ls-files writeup/figures/` and `ast`-parsed membership
of `P2_EVIDENCE`. Six of seven rows were stale:

| figure | leg | was | is |
|---|---|---|---|
| `fig72` | 320 MTSC | reserved, no files on main | **`.png` tracked**, no script, unregistered |
| `fig75` | 301 FSB | reserved, no files on main | unchanged — genuinely still reserved |
| `fig76` | 313 SDSS | reserved, no files on main | **`.png` tracked AND registered in `P2_EVIDENCE`** |
| `fig78` | 326 CTRX | leg live | nothing on main; **no leg is live** |
| `fig81` | 329 EGMF | leg live | `.png` + `evidence.py` tracked, **unregistered** |
| `fig83` | 306 SSE | leg live | nothing on main |
| `fig84` | 318 DECR | leg live | `.png` + BLOG/TECHNICAL, no script |

Where the landed table and the files disagree, **both are shown and neither is overruled** — that is
the Conductor's to rule, and it is §8 below. The table is marked **closed to new allocations** (under
CONDUCTOR mode, allocation is stated at dispatch and tracked in `reports/ORCH_STATE.md`), and
"`fig85` is the next free number" is struck and corrected to **`fig111`** — `.png` files exist
through `fig110`.

Two statements that **this unit's own D6 repair made false** were corrected in place rather than
deleted: the note "`fig107`'s registration gap is deliberately unfixed while `V-W3` measures it",
and the T6 row's "script exists, NOT registered … do not 'helpfully' register it". Both were
conditional on `V-W3` being in flight. `V-W3` has returned (`2b8755e`); the condition is spent. The
gate names both registrations explicitly, so this is the commission, not an initiative.

---

## §4 — THE GATE ANSWER

> **DOES `build_figures.py` SELF-CHECK EVERY FIGURE THE RECORD CITES?**

# NO.

Twice over, and the two answers are different sizes.

```
P2_EVIDENCE entries registered  : 38        (was 36 before this unit)
  registered but file missing   : 0
figure ids CITED in the record  : 110
figure ids REBUILT              : 45
figure ids SELF-CHECKED         : 22
.png files in writeup/figures   : 97

ANSWER, rebuild coverage    (CITED subset of REBUILT)     : NO  (66 uncovered)
ANSWER, self-check coverage (CITED subset of SELF-CHECKED): NO  (88 uncovered)
```

**REBUILT** (45) — a `.png` whose filename appears in a file `build_figures.py` actually executes:
`1 2 3 4 5 6 7 48 49 50 51 52 55 56 58 59 60 61 64 65 66 67 68 69 70 71 73 74 76 77 79 80 82 99 100
101 102 103 104 105 106 107 108 109 110`

**SELF-CHECKED** (22) — of those, the ones whose script carries an executable assertion:
`58 61 66 69 73 74 76 77 79 80 99 100 101 102 103 104 105 106 107 108 109 110`

The gap is partitioned, so that the answer is not one undifferentiated number:

**[A] CITED, the `.png` EXISTS, NOT REBUILT — 52.** *A figure the record shows a reader that
`build_figures.py` cannot reproduce.* This is the serious bucket.
`8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41
42 43 44 45 46 47 63 72 81 84 85 86 89 91 92 94 96 97`

**[B] CITED, NO `.png`, NOT REBUILT — 14.** Reserved/allocated/parked numbers; no artefact exists to
rebuild, so these are not defects.
`53 54 57 62 75 78 83 87 88 90 93 95 98 111`

**[C] REBUILT but never cited — 1:** `65`.

**[D] REBUILT with no assertion anywhere in the script — 23.** It runs; it does not check itself.
`1 2 3 4 5 6 7 48 49 50 51 52 55 56 59 60 64 65 67 68 70 71 82`

**What this unit changed in that answer, and it is small:** `fig107` moved from uncovered into both
`REBUILT` and `SELF-CHECKED`; entries went 36 → 38; `REBUILT` 44 → 45; `SELF-CHECKED` 21 → 22;
bucket [A] 53 → 52. **The answer was NO before the repair and it is NO after it.** One list entry
was the whole of D6, and D6 was one figure out of 66.

**`fig111` is in [B] because of this unit's own `INDEX.md` edit** — the checker counts "`fig111` is
the next free number" as a citation. That is the honest behaviour of a token scan and [B] is exactly
the bucket for reserved numbers; recorded here so no later reader treats it as a discovery.

---

## §5 — THE EXECUTABLE CHECK (lesson 68)

**`writeup/check_figure_coverage.py`** — run it:

```
.venv/bin/python writeup/check_figure_coverage.py
```

It exits **0** only if `CITED ⊆ REBUILT` **and** `CITED ⊆ SELF-CHECKED`. It currently exits **1**,
and it printed the §4 block above when run at the end of this unit.

How it avoids the exact hiding place `fig107` used:

* `P2_EVIDENCE` is read with `ast.parse` + `ast.literal_eval`, **never grep**. `fig107` appeared in
  the file in 2 comments and 0 string literals; a grep-based checker would have called it registered.
* **REBUILT** = figure ids whose `.png` filename appears in a file `build_figures.py` actually
  executes — not "a script exists somewhere".
* **SELF-CHECKED** narrows that to scripts carrying an executable assertion
  (`assert`, `raise`, `sys.exit(≥1)`, `SystemExit(≥1)`).
* **CITED** = a scan of `writeup/**/*.md` plus root `*.md`, with ranges (`figs 20–24`, `fig14/15`)
  expanded, so a figure cited only inside a range cannot slip through.

Its pre-repair baseline is committed at `b3be9ac`, before any repair touched anything.

---

## §6 — MERGE GATE

`bash scripts/merge_gate.sh origin/main` → **`MERGE GATE: PASS`**.

---

## §7 — WHAT THIS IS NOT

Nothing in this unit is movement toward Clay. No `L1→L4` link moved; no theorem, bound, or numerical
finding was established, extended or weakened. Two banked *findings* were sharpened as a side effect
of repairing the journals that carry them (D5's cost reconciliation, D3's sign), and both are
bookkeeping about a completed experiment, not new physics or new mathematics. The rebuild path is
one figure less blind than it was. That is all.

---

## §8 — FOUND AND DELIBERATELY **NOT** REPAIRED — flags to the Conductor

Reading (a): a new defect is a new unit. Every item below is applied **nowhere**.

1. **The answer to this unit's own gate is NO by 66 figures, and only one of them was in scope.**
   Bucket [A] — 52 figures the record shows a reader that `build_figures.py` cannot reproduce —
   is the real finding of this unit and it is far larger than the defect list that led to it.
   `fig8`–`fig47` is a contiguous block of 40, which suggests an era of the project that predates
   the registration convention rather than 40 separate lapses. **Sizing and repairing that is a
   unit, or a wave.**
2. **23 registered scripts run without a single assertion** (bucket [D]). They redraw; they verify
   nothing. Lesson 68 applies to them exactly as it applied to `fig107`.
3. **`fig81`'s evidence script is tracked on `main` and is not registered in `P2_EVIDENCE`** —
   `writeup/figures/fig81_route_egmf_v1_evidence.py`. This is *the same defect as D6*, at a
   different figure, found while reconciling the allocation table. **It is not D6 and it was not
   repaired.** It is one list entry away from being fixed, and that entry is not mine to add.
4. **Four legs have figures and/or BLOG+TECHNICAL pairs on `main` but no row in `INDEX.md`'s landed
   table** — 326 (CTRX, `fig78`: nothing on main at all), 329 (EGMF, `fig81`), 306 (SSE, `fig83`:
   nothing on main), 318 (DECR, `fig84`). Whether those landed, and under what caveat, is a
   Conductor ruling, not a bookkeeping fix. The allocation table now records the file facts and
   overrules nothing.
5. **`fig72` and `fig76` are recorded `PARKED, NOT MERGED` in the landed table while their `.png`
   files are tracked on `main`, and `fig76`'s evidence script is registered and runs.** Two
   registers disagree about whether the same work merged. Not ruled here.
6. **`fig65` is rebuilt and self-checked but is cited nowhere in the record** (bucket [C]). Harmless,
   but it means a figure is being maintained for no reader.
7. **D1's `~8×` residue survives outside the Conductor's files**, at
   `writeup/4_p2_lottery/TECHNICAL_P2_PROGR4_HHARD.md:212`. D1 is out of this unit's scope by the
   gate. **Flagged, not fixed** — and it is flagged in `prog_r4_e.md`'s D3 correction block too, so
   it cannot be lost.
8. **`V-W3`'s D3 is wrong in size and direction** (§2, D3) and its D5 ceiling is wrong (§2, D5:
   "not recoverable from the record" — it is recoverable). Both are findings **about the verifier**.
   D3's and D5's conclusions both survive; only their numbers and their ceiling do not. Reported,
   not ruled: whether a verifier's landed §4 should carry a correction block is the Conductor's.
9. **D2 aged out between measurement and repair** (§2). A defect list is a measurement with a
   timestamp. If wave-N verifiers are to be repaired by wave-N+1 units, a defect that a *different*
   repair dissolves in the interval will keep happening, and the second unit will keep spending its
   time discovering the absence. Worth a convention.
10. **`writeup/data/p2_route_vbs_v1_scoping.json::the_empty_cell.meaning` was NOT TOUCHED.** It is
    measured FALSE, it is question (Q3) of the open user escalation
    `writeup/escalations/ESCALATION_W3_WORDING_2026-08-18.md`, and reading (b) is absolute: a banked
    artefact is never rewritten to match a later finding. Recorded here to make the non-action
    auditable.
11. **`writeup/build_figures.py` aborts in a clean worktree** at `p2_route_cadx_v1_scope.py`, which
    needs `Papers/2505.03091.pdf` — present in the main checkout, absent here, and gitignored. It is
    the only *pre-existing* registered entry with a `Papers/` dependency. It could take the new
    `(path, args, required_inputs)` form and SKIP loudly instead of aborting. **Not applied** — it is
    not a listed defect, and changing an entry that currently runs green in the main checkout is a
    behaviour change I was not commissioned to make.
