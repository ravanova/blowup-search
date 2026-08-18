# VERIFY WAVE 3 — unit `V-W3`, wave 4 verifier

Branch `verify/wave3`. Data `writeup/data/p2_verify_wave3_v1.json`.
Re-derivation script: `experiments/verify_wave3_rederive.py`.

---

## §0 — THE GATE AS GIVEN (committed before anything was checked)

Four items, pre-committed. Nothing added, nothing dropped.

**(1) Unit `E` — the H-hard diagnostic (`d0d72b1`).** Re-derive its headline **from
`writeup/data/p2_prog_r4_e_v1.json`, not from prose**. Claim on record: **16 attempts, 2 converged,
0 recovered any named row**, with a positive control passing at `‖R‖ ≈ 1.5e-10` **through E's own
predicate**, and two diagnostics — (i) `PULL_TO_LOW_S`, (ii) `MIXED` with `p = 0.9317`. Does the
artefact support **each**? Name any it does not.

**(2) `E`'s cost.** Record: `E` overran commissioning by ~**8×**: ≈**0.57 h/attempt** (5.687
core-hours + 0.806 h controls, 16 attempts) against a commissioning figure of **0.0713**. Re-derive
both sides. **Is the 8× real, and is `0.0713` the like-for-like comparison** — same thing, same unit?
A bogus overrun is as much a finding as a real one.

**(3) `V-W2` (wave-2 verifier, `594ff89`).** Verify the verifier. (a) Do its **four re-measurements**
land where its journal says? Re-run or re-derive each. (b) Its stated method includes **re-fetching
sources and recording SHA-256**. Does that appear in its artefacts with hashes present and
reproducible — or is it prose only?

**(4) `fig107`.** Record states `fig107` is **absent from the `P2_EVIDENCE` structure in
`writeup/build_figures.py`**. Confirm **mechanically** (grep/parse, not eyeball) and report what is
and is not registered.

### Pre-committed readings — binding

(a) **REPORT, DO NOT REPAIR.** A defect gets a location and a size, not a fix. A verifier that
repairs its own findings has destroyed the measurement. Includes `fig107`: it is **not** registered
by this unit.
(b) **Waves 1 and 3 ONLY, NEVER wave 4.** `V3` (`leg/399-v3-gradeA`) and `L2′` (`leg/397-l2-decay`)
are out of territory — not opened, not graded, not commented on. They land `UNVERIFIED` by design.
(c) A **PASS is a real result and so is a FAIL.** Per item: `CONFIRMED` / `REFUTED` / `PARTIAL` /
`UNREACHABLE`, with the discrepancy quantified when `PARTIAL` or `REFUTED`.
(d) Re-derive from `writeup/data/*.json` and code, **never from prose**. Missing artefact =
`UNREACHABLE` and a named finding; it does **not** become a pass.
(e) Lesson 68: a check is executable or it decays. Runnable re-derivation left under `experiments/`.
(f) `UNREACHABLE` and `THROTTLED` bank as themselves, never as zeros.
(g) **Verification is not movement toward Clay.** No link moves because a number checked out. Clay
odds ~0.05%, unmoved. Tier 2 is never a proof. Scale is not evidence.

---

## §1 — METHOD

**Everything below is recomputed. Nothing below is read off a sentence.** The rule that shaped
every step is pre-committed reading (d): a journal agreeing with itself is not verification, so a
claim was only allowed to pass if it fell out of `writeup/data/*.json`, out of
`experiments/programme_r4/*.json`, out of source **parsed** with `ast`/`tokenize`, out of the git
tree via `ls-tree`/`cat-file`, or out of third-party bytes fetched today.

Where a banked artefact carries a summary field, the summary was **never trusted as the
measurement**. It was checked against a recount of the artefact's own per-row records. That single
discipline is what turned up the one refutation.

**Checkpointing (mandatory above ~1 h).** The §0 gate was committed before any number was computed
(`1d97994`), the executable re-derivation next (`aabc748`, then `3357211` with the PDF leg), then
the data object (`02d2104`), then this journal. Every one of those commits is independently
resumable: `experiments/verify_wave3_rederive.py` recomputes all four items from a clean checkout
in seconds and exits non-zero if any of them stops agreeing, so a successor picking this up after a
host exit needs nothing from this session's memory.

**Lesson 68 — the check is executable.**

```
python3 experiments/verify_wave3_rederive.py
```

Offline core: items (1), (2), (4) in full, and the JSON-and-git-level parts of item (3). Exit 0 iff
every re-derivation agrees. Three additive independent legs, each of which records `UNREACHABLE`
rather than passing or failing when its resource is absent:

```
python3 experiments/verify_wave3_rederive.py --net            # re-fetch + SHA-256 the three sources
python3 experiments/verify_wave3_rederive.py --saveddata DIR  # re-decode the authors' .mat (needs scipy)
python3 experiments/verify_wave3_rederive.py --pdf FILE       # recount T4's C+/C- terms (needs pdftotext)
```

With all three legs on: **180 checks, 0 disagreements.**

**Territory honoured.** `DIRECTION.md` was never opened. Wave 4's units — `V3` on
`leg/399-v3-gradeA` and `L2′` on `leg/397-l2-decay` — were never opened, never graded and never
commented on; by reading (b) they land `UNVERIFIED` and wave 5 carries their verifier. Nothing was
repaired: no defect found below has been fixed, `fig107` least of all. Nothing was merged and
nothing was pushed to `main`. No author group was contacted; the two arXiv PDFs and the VU code zip
were **read**, over anonymous HTTP, and nothing else.

---

## §2 — PER-ITEM VERIFICATION

### §2.1 Item (1) — unit `E`'s headline. **CONFIRMED**, six of six.

Re-derived from `writeup/data/p2_prog_r4_e_v1.json` alone. I did not read `diagnostic_3`'s summary
block and call it a measurement; I recounted the 16 rows of `diagnostic_3.attempts` and then made
the summary answer to the recount.

| claim on record | how I got it | value |
|---|---|---|
| 16 attempts | `len(attempts)` | **16** |
| 2 converged | `reason == 'converged'` recount; cross-checked against the `success` flag | **2** and **2** |
| 0 recovered any named row | `recovered_any_named_orbit` recount; cross-checked `matched_row is None` on all 16 | **0** and **0/16 matched** |
| positive control at `‖R‖ ≈ 1.5e-10` **through E's own predicate** | `controls.R.final_residual`, then `controls.R.harness_predicate_says_recovered` | **1.5243710606417483e-10**, predicate **`true`** |
| diagnostic (i) `PULL_TO_LOW_S` | `diagnostic_1.verdict` | **`PULL_TO_LOW_S`**, `n = 23` |
| diagnostic (ii) `MIXED`, `p = 0.9317` | `diagnostic_2.verdict`, `diagnostic_2.permutation_p` | **`MIXED`**, **0.9316534173291335 → 0.9317** |

The summary block agrees with the recount on every field. Controls `fired_as_planted = true` with
an empty `failures` list.

**Two nuances, banked as nuances and not as defects, because in both cases the artefact carries
both readings and E's own write-up states the second:**

1. **The `1.5e-10` is control `R`'s, not control `P`'s.** `E` ran two positive controls. `P`, the
   planted analytic fixed point, lands at `‖R‖ = 7.75e-09`; `R`, the perturbed converged orbit,
   lands at `1.52e-10` and is the one carrying `harness_predicate_says_recovered = true`. The claim
   says "*a* positive control", which is exact. It would be wrong to write "the".
2. **`PULL_TO_LOW_S` is a statement about the `n = 23` converged subset.** The same statistic over
   all 200 banked attempts returns **`NO_PULL`** (median drift −0.0239, 120/80 negative/positive,
   sign-test `p = 0.00569`). Both are in the artefact under
   `diagnostic_1.secondary_all_200_attempts`, and `TECHNICAL_P2_PROGR4_HHARD.md:92` states the
   secondary in its own words. The headline is a subset statement and must be quoted as one.

### §2.2 Item (2) — `E`'s cost. **REFUTED.** There was no overrun.

This is the finding. The record says `E` overran its commissioning estimate by ~**8×**. Re-derived,
**it did not overrun at all**: like for like it came in **0.4% under**. The 8 is the worker count.

**Side one — what `E` spent.** Summed from `diagnostic_3.attempts[].wall_seconds` and
`[].n_iters`, with `resourcing.core_hours` checked against its own identity:

| quantity | re-derived |
|---|---|
| `resourcing.core_hours` | **5.687335857417849** — and `2047.4409 s × 10 workers / 3600` reproduces it exactly |
| controls | `2900.5545 s` = **0.805709578593572 h** |
| **sum of per-attempt wall over the 16 rows** | **9.08842624425888 core-hours** |
| epochs | **343** (recount of `n_iters` = `resourcing.total_epochs`) |
| realised cost of an epoch | **95.389 s** |

**The record's own stated arithmetic does not produce its own headline.** `(5.687 core-hours +
0.806 h of controls) / 16` = **0.4058** h/attempt. The record calls that quantity `0.57`. It is not.
The `0.57` comes from a different, unquoted number — the sum of per-attempt wall, `9.088` core-hours,
over 16 attempts = **0.56803**. **The stated derivation is off by a factor 1.400.**

**Side two — what `0.0713` measures.** Parsed by regex out of `experiments/journal/prog_r4_u5.md:405`,
which defines it verbatim:

> **Cost basis, measured this run, not estimated.** `0.0713 h wall per attempt at 8 workers`
> (2,104 epochs / 100 attempts, epochs costed at 95 s as required)

`0.0713` is **wall-hours per attempt on 8 concurrent workers**. `0.57` is **core-hours per attempt**.
They are not the same unit. U5 uses `0.0713` consistently as a wall figure everywhere else it appears
(`141 × 0.0713 + 0.68 ≈ 10.7 h`; `≈ 8 h for a fresh 100`), so there is no ambiguity about which it is.

**Like for like, both sides in core-hours per attempt:**

| side | core-hours per attempt |
|---|---|
| U5 commissioning model, `0.0713 wall-h × 8 workers` | **0.5704** |
| `E` measured, `9.08843 / 16` | **0.56803** |
| **ratio** | **0.9958** |

**The claimed `~8×` is reproducible by exactly one operation: dividing a core-hour figure by a
wall-hour figure.** `0.56803 / 0.0713 = 7.967`. That is the worker count, 8, and nothing else.

**The structural explanation offered for the overrun is also not what the ledgers show.** The record
says the model "was calibrated on U5 attempts that stall early, while an attempt planted at a
published `(T, s)` runs 20–31 epochs before the stall rule fires." Measured:

| | epochs/attempt |
|---|---|
| U5, counted from `experiments/programme_r4/u5_m3_ledger.json` | **21.95** (2195 epochs / 100) |
| `E`, counted from its own `n_iters` | **21.44** (343 / 16) |

`E` used **2.3% fewer** epochs per attempt than U5, not more. And `E`'s realised `95.389 s/epoch` is
within **0.4%** of the `95 s` the commissioning model prices an epoch at. **Both factors of the cost
model were accurate.** There is nothing structural to explain because there is nothing to explain.

**Collateral, found on the way:** `prog_r4_u5.md:405` says "2,104 epochs / 100 attempts". Its own
banked ledger holds **2195**, and `E`'s `diagnostic_2.n_epochs` independently reports **2195**.
Size: 91 epochs, **4.3%**.

**What is NOT wrong, and should not be swept up in this.** `E`'s forward pricing table
(`prog_r4_e.md:400` onward) is internally correct: it prices from `9.088/16 = 0.568` core-h/attempt
and converts to wall properly (160 attempts → ~91 core-hours → ~11 h wall at 8 workers). The
**pricing** is sound. Only the **comparison** is defective — and with it the derived instruction at
`OPTIONS.md:72`, "THE COST MODEL UNDER ALL FOUR OPTIONS IS WRONG BY ~8×, MEASURED", which does not
survive. The cost model is right.

**Robustness.** The conclusion does not turn on which of `E`'s two cost figures you take. Using the
banked `5.687 + 0.806` instead gives `0.406` core-h/attempt, a ratio of **0.71** to the commissioning
model — still an under-run, still nowhere near 8×.

### §2.3 Item (3) — verify the verifier (`V-W2`, `594ff89`). **CONFIRMED**, both parts.

**(a) The four re-measurements all land where `V-W2`'s journal says they land.** Each was re-derived
from the **primary** artefact `V-W2` was checking, not from `V-W2`'s own record, and `V-W2`'s column
was then made to answer to mine.

1. **`T4`'s 2D lift.** Both certified rows: `Table 1` `N_x3 = 0`; package `Nrec` `[17,17,0,11]` and
   `[21,21,0,16]`; `x₃` mode extent **1**; `max|u⁽³⁾| = max|ω⁽¹⁾| = max|ω⁽²⁾| = 0.0` under `repr`,
   not merely under `abs(·) < ε`; `max|ω⁽³⁾| = 1.6351073366158` / `1.5274264613264072`;
   `setup = '2D'`. **Independent leg:** I downloaded `navierstokes-code.zip` myself and re-decoded
   `{data,extra}orbit{1,2}.mat` with `scipy.io`. **Every field reproduces bitwise**, including
   `‖u‖_X = 10.070710173304683` and `12.557400068291274`.
2. **`T4`'s first conjunct and its negative control.** Criterion (4.32) recomputed from the four
   published constants `Y0, Z0, Z1, Z2` read out of the authors' own file: `Z0+Z1`, `2·Y0·Z2`,
   `(1−Z0−Z1)²` and the discriminant all reproduce bitwise on both rows, criterion met on both.
   `r_min`/`r_max` recomputed bitwise. The four relative deviations are
   `{p1.r_min 2.435e-10, p1.r_max 0.0, p2.r_min 8.335e-13, p2.r_max 5.618e-15}`, **smallest non-zero
   `5.6e-15`** as claimed. `r_sol^Ω` exact against the printed value on both rows. Norm check
   `δ = 5.2748e-06` against the `V4_REPRODUCED = 1e-3` threshold, which I **parsed out of
   `experiments/p2_route_t4_v1_evidence.py`** rather than took on trust. **Independent leg:** I ran
   `pdftotext -layout` over my own copy of the PDF and recounted with my own normaliser —
   *approximate inverse* **×7**, *Newton-Kantorovich* **×4**, *interval arithmetic* **×5**, *INTLAB*
   **×2**, all six closure terms **0**, and exactly **one** line containing the name Zgliczyński,
   which begins `[48]`.
   *Nuance, pre-registered by `V-W2` before it computed:* "down to `5.6e-15`" is true of one cell in
   four; one cell is exactly `0.0`. `V-W2` reports all four. No defect.
3. **`T6`'s table.** 7 full texts, `n_fulltext_MEASURED = 7`, `UNREACHABLE = 0`, `THROTTLED = 0`.
   Verdicts recounted **from the seven per-paper rows**, not from the banked counter: **4
   strengthen, 2 UNDERCUT, 1 confirm**, and the banked counter agrees. The two UNDERCUTs are
   `1902.00384` and `2409.09234`.
4. **`T5`'s sweep.** I re-enumerated the corpus myself — `git ls-tree -r` at the landing commit of
   `p2_route_t5_v1.json` (`3cab83ed2dc9`), filtered to `*.md`/`*.py`, minus the record's own
   `excluded_by_name` list, then `git cat-file` over every blob to count newlines. **1428 files,
   417476 lines**, exactly as banked. I did not re-run the sweep. 7 findings, **5 APPARATUS / 2
   REALIZATION**, re-openable **`['F1','F2']`**.

**(b) The SHA-256 method is in the artefact, not only in the prose — and it reproduces today.**
`writeup/data/p2_verify_wave2_v1.json` carries a top-level `independent_artefacts_refetched` block
holding, for each of three sources, `url` / `http` / `my_sha256` / `banked_sha256` / `match`. All
three `my_sha256` values are well-formed 64-hex and all three are recorded as matching what they
were checked against. **I re-fetched all three on 2026-08-18 and hashed them myself:**

| source | bytes | SHA-256 | vs `V-W2` |
|---|---|---|---|
| `arxiv.org/pdf/1902.00384` | 874,126 | `97e81647…4a05d29` | **identical** |
| `math.vu.nl/~janbouwe/…/navierstokes-code.zip` | 4,851,078 | `edf64bc0…20c7ac5f` | **identical** |
| `arxiv.org/pdf/2409.09234` | 4,533,748 | `7a3c8ac9…d3d3042b3` | **identical** |

Two of the three are additionally carried by `writeup/data/p2_route_t4_v1.json`, a record `V-W2` did
not write, so its hash column is checkable against something independent of itself. **The method is
real, executable and reproducible; it is not prose.**

### §2.4 Item (4) — `fig107`. **CONFIRMED**, mechanically.

`ast.parse` on `writeup/build_figures.py`, then `ast.literal_eval` of the `P2_EVIDENCE` assignment.
It is a **list of 36 entries** (mostly path strings, two `(path, args)` pairs). The figure an entry
draws is named in its trailing `# figNNN --` comment, not in the path string, so the registered id
set was read off the literal's own source line range rather than off the strings — **36 entries, 36
distinct ids, one each**:

```
48 49 50 51 52 55 56 58 59 60 61 64 65 66 67 68 69 71 73 74
76 77 79 80 82 99 100 101 102 103 104 105 106 108 109 110
```

**`107` is not among them.** Separately, `tokenize` over the whole file finds the text `fig107` in
**0 `STRING` tokens** and **2 `COMMENT` tokens**, at lines **401** and **402** — inside `fig108`'s
and `fig109`'s own entries, each recording that `fig107` was allocated to U5 at dispatch. **The file
records the allocation and never registers the figure.**

The gap is isolated: `fig99` and `fig100`–`fig106` and `fig108`–`fig110` are all registered.
`writeup/figures/fig107_prog_r4_m3_shift_strata.py` and its `.png` both exist on disk and
`writeup/INDEX.md` cites `fig107` in the PROG-R4 U5 row.

**NOT REPAIRED.** Reading (a) is binding and named `fig107` explicitly.

---

## §3 — VERDICTS

| # | item | verdict | size of the discrepancy |
|---|---|---|---|
| **1** | unit `E`'s headline — 16 / 2 / 0, control at `1.5e-10` through E's own predicate, `PULL_TO_LOW_S`, `MIXED` `p=0.9317` | **CONFIRMED** (6/6) | — (two nuances, both already in the artefact) |
| **2** | `E`'s `~8×` cost overrun, `0.57` vs `0.0713` h/attempt | **REFUTED** | claimed **8.0×**, true **1.00×**; the 8 *is* the worker count. Stated derivation separately off by **1.400×**. Structural explanation contradicted: **21.44** vs **21.95** epochs/attempt |
| **3** | `V-W2`'s four re-measurements, and its SHA-256 method | **CONFIRMED** (4/4 + method) | — (3 hashes reproduce bitwise today; `.mat` re-decode bitwise) |
| **4** | `fig107` absent from `P2_EVIDENCE` | **CONFIRMED** | one missing list entry, the only gap in the 99–110 block |

**3 of 4 CONFIRMED. 1 REFUTED. 0 PARTIAL. 0 UNREACHABLE. 0 THROTTLED.**
180 executable checks, 0 disagreements.

**Verification is not movement toward Clay, and this section is not a scoreboard that says
otherwise.** Three numbers checking out moves no `L1→L4` link. The one that did not check out is a
bookkeeping defect, not a mathematical retreat, and describing its correction as progress would be
prohibited too. Ceiling **TIER 2** — Tier 2 is never a proof, scale is not evidence, Clay odds
**~0.05%, unmoved**.

---

## §4 — DEFECTS FOUND (location + size, **unrepaired**)

**D1 — `E`'s `~8×` cost overrun is a wall-vs-core units error. Size: the whole claim.**
*Locations:* `STATE.md:178-179`; `OPTIONS.md:72-74` and the derived warning at `OPTIONS.md:52`;
`experiments/journal/prog_r4_e.md:393-394` and `:474-476`;
`writeup/4_p2_lottery/TECHNICAL_P2_PROGR4_HHARD.md:212`.
`0.0713` is **wall-hours per attempt at 8 workers** (`experiments/journal/prog_r4_u5.md:405`);
`0.57` is **core-hours per attempt**. Like for like, `E` measured **0.568** against a model of
**0.570** — **ratio 0.996, an under-run**. The claimed ratio is recovered by exactly one operation,
dividing core-hours by wall-hours, and equals the worker count.
*Downstream:* `OPTIONS.md:72`'s standing instruction that the cost model under all four options is
wrong by ~8× is unsupported; the cost model is accurate in both of its factors.

**D2 — the stated derivation of `0.57` does not evaluate to `0.57`. Size: factor 1.400.**
*Locations:* `STATE.md:179`, `OPTIONS.md:73`.
`(5.687 core-hours + 0.806 h of controls) / 16 attempts` = **0.4058**, not 0.57. The `0.57` is
`9.088 / 16`, where `9.088` core-hours is the sum of per-attempt wall — a quantity named at
`prog_r4_e.md:387-388` but not carried into the comparison.

**D3 — the structural explanation for the overrun is contradicted by both ledgers. Size: E used
2.3% fewer epochs per attempt, not more.**
*Location:* `experiments/journal/prog_r4_e.md:394-397`, `:474-476`.
`E` **21.44** epochs/attempt (343/16, from its own `n_iters`); U5 **21.95** (2195/100, from
`experiments/programme_r4/u5_m3_ledger.json`). `E`'s realised **95.389 s/epoch** is within **0.4%**
of the model's 95 s.

**D4 — `prog_r4_u5.md`'s epoch count disagrees with its own ledger. Size: 91 epochs, 4.3%.**
*Location:* `experiments/journal/prog_r4_u5.md:405` says "2,104 epochs / 100 attempts".
`experiments/programme_r4/u5_m3_ledger.json` holds **2195**, and `E`'s `diagnostic_2.n_epochs`
independently reports **2195**.

**D5 — `E`'s two cost figures do not reconcile and the artefact cannot close the gap. Size: 3.40
core-hours, 37% of the larger.**
*Location:* `writeup/data/p2_prog_r4_e_v1.json`, `diagnostic_3.resourcing.core_hours` = 5.687
("the relaunch only") against `sum(attempts[].wall_seconds)` = 9.088 over the same 16 rows.
No per-attempt provenance flag distinguishes relaunched attempts from those inherited from the
launch the host killed, so which subset the 5.687 covers is not recoverable from the record.

**D6 — `fig107` is not registered in `P2_EVIDENCE`. Size: one missing list entry.**
*Location:* `writeup/build_figures.py`, `P2_EVIDENCE` (lines 349–404). The id set runs
`… 99 100 101 102 103 104 105 106 108 109 110`; `107` is the only gap in that block. `fig107`
appears in the file in **0 string literals** and **2 comments** (lines 401, 402). The drawing script
and the `.png` exist under `writeup/figures/` and `writeup/INDEX.md` cites the figure, so it is
rebuilt by nothing and self-checked by nothing.

**NONE OF D1–D6 HAS BEEN REPAIRED BY THIS UNIT.** Reading (a): a verifier that repairs its own
findings has destroyed the measurement. In particular `fig107` remains unregistered and
`writeup/build_figures.py` is untouched on this branch. Every one of D1–D6 is a wording or
bookkeeping question for the Conductor to rule; a defective ban *wording*, had any of these reached
one, would be a **user escalation** and not mine either.

---

## §5 — WHAT I COULD NOT REACH

Recorded as ceiling, not banked as zeros. `UNREACHABLE` count for this gate: **0** — every gate item
was reachable, and all three optional independent legs ran and agreed. What follows is the honest
boundary of what a `CONFIRMED` from this unit means.

1. **I re-ran no Newton solve.** Item (1) establishes that `E`'s 16 attempt records are internally
   consistent, that its summary answers to a recount of its own rows, and that its controls carry
   the fields they claim. It does **not** establish that those 16 solves were executed as described
   or that the solver is right. Re-running them is ~9.1 core-hours; not bought.
2. **D5 is a ceiling as well as a defect.** I could not determine which attempts the banked 5.687
   core-hours covers. Item (2)'s conclusion is robust to the choice — `5.687+0.806` gives a ratio of
   **0.71**, still an under-run — but the reconciliation itself is beyond this artefact.
3. **Item (2) tests arithmetic, not judgement.** Whether U5's `0.0713` *should* have been the basis
   for `E`'s brief is a Conductor question. I measured the comparison; I do not rule the commission.
4. **Item (3) covers `V-W2`'s four re-measurements and its method, not the wave-2 units.** `T4`'s,
   `T5`'s and `T6`'s gate **answers**, their pre-registration ordering, and their readings of what
   the papers *mean* are outside this gate and are not verified by anything here.
5. **Five of `T6`'s seven full texts were not re-fetched.** I re-fetched and hashed the two arXiv
   PDFs `V-W2` hashed. `T6`'s other five deciding sentences are verified at the JSON level only.
6. **I did not run `writeup/build_figures.py`.** Item (4) shows `fig107` is unregistered and the
   other 36 entries **are** registered. It does not show that those 36 build.
7. **Wave 4 is out of territory by design, and this is a scope boundary rather than an
   `UNREACHABLE`.** `V3` (`leg/399-v3-gradeA`) and `L2′` (`leg/397-l2-decay`) were not opened, not
   graded and not commented on. They land `UNVERIFIED` and wave 5 carries their verifier.
8. **`DIRECTION.md` was never opened**, so anything a wave-1 or wave-3 claim rests on that lives
   only there is outside what this unit can say anything about.
