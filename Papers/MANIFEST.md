# Papers manifest — what to fetch, in priority order, and what each one gates

**Why this file exists.** `Papers/` is gitignored (we do not commit third-party PDFs), so
a previous session's downloads are **destroyed every time the container is rebuilt** —
which is what happened here: Spike 1's notes cite "Source PDFs live in `Papers/`" and the
directory no longer exists. The manifest and `fetch.sh` are committed so the PDFs can be
re-pulled in one command instead of re-derived from memory. **If you download papers, do
not commit them; commit any change to this manifest instead.**

**STATUS 2026-08-04 (leg 48, Route-V v0): TWO PAPERS ADDED, AND ONE OF THEM CLOSED A STAGE.**
`bash Papers/fetch.sh 2410.05480 2404.04054` — neither was in this manifest, and the first
of them **pre-empts stage V outright**: Dahne–Figueras verify branches of self-similar
singular CGL solutions *in the dissipation parameter*, in interval arithmetic. It is now
`solver/viscous_novelty.py`'s primary source, re-derived rather than cited (Tables 1/2 to
1.8e−07, their Fig. 1a branch to 3.0e−06, their fold to 3.8e−07). **Its figures are pgf
vector graphics**, so `read_df_figure` reads the published curve back as data — worth
knowing before settling for a qualitative comparison with anyone's figure.

**STATUS 2026-08-04 (leg 45, Route-M): TIER 2 AND TIER 3 ARE NOW READ FOR WHAT THEY GATE.**
The target ledger they produced is `solver/target_selection.py` (`test_target_selection.py`
9/9), and `LITERATURE_CHECK.md`'s **seventh pass** is the summary. What changed:

* **2302.12877 (CLN)** — the completed unbounded-domain certificate. Their Kawahara `r₀` is
  now a gate on our own radii-polynomial algebra (reproduced exactly). **They work in
  Hilbert/Fourier `H^l`, not weighted `ℓ¹`**, so Route-D's weighted-`ℓ¹` no-go and
  discrete-ball trap are **narrowed, not closed** — still unsearched at primary source.
* **2604.01868 (CHL)** — carries the **top two uncertified targets**, and its §4 Scenario-2
  formulation is the three-constant bordered system the port is now aimed at.
* **2603.25104 (HTW26)** — the third: gCLM one-scale profiles from degenerate data, `a>0`,
  numerical only, with `c_l` changing sign at `a ≈ 0.2329`.
* **2308.01528 / 2305.05895 (HQWW)** — the **exclusion list grew**: the Hou–Luo odd
  non-degenerate profile is proved analytically as well as by CAP, and the **entire smooth
  gCLM branch for all `a ≤ 1`** is analytic. Certifying either contributes nothing.
* **1908.09385 (J. Chen)** — checked and it is **analytic**, no computer assistance. Not a
  CAP precedent; it is an exclusion.
* **2604.09949** — a 3D Navier–Stokes singularity claim. Audited; see LITERATURE_CHECK §7th
  pass. Recorded as `CLAIMED_UNUSABLE`, not as certified and not as open.

**STATUS 2026-08-04: EGRESS WORKS. ALL 14 FETCHED ON THE FIRST ATTEMPT. TIER 1 IS READ.**
See `LITERATURE_CHECK.md` **sixth pass** (the first primary-source pass) and Route-J v1
(`solver/literature_gates.py`, `test_literature_gates.py` 9/9, fig39). Verdict: seven
standing claims pre-empted, one partial, two still unsearched, one result inbound.

**READ:** 2207.07548 (full; §1, §5, §7.3, §8 closely), 2607.19762 (full; abstract, §2, §3,
§6, §7 closely), 2210.07191 (abstract, §1, the `c_l/c_omega` profile section),
2209.08232 (§1, §2 closely).
**FETCHED AND TEXT-EXTRACTED BUT NOT READ:** everything in Tier 2 and Tier 3. **Tier 2 is
the next literature spend and it is now cheap** — it gates the Route-D methodological
claims, the only ones with a real chance of being new.

**TWO CORRECTIONS TO THIS MANIFEST'S OWN PRIORITIES, from having read Tier 1:**
* **2207.07548 does NOT gate `s_c = α/2`.** Its §8 explicitly leaves the critical-σ
  question open. **2607.19762 §6.1 eq (6.3) is the pre-emption** — it was filed here as a
  spectral paper, and its §6 is the one that matters.
* **2207.07548 turned out to matter for something nobody asked it about:** §5.1 (Schochet,
  corrected) is the only primary source in this list on the **supercritical** balance,
  which no leg of this project had. Lesson (69).

**STATUS 2026-08-05 (maintenance sweep, mechanical index-only pass):** three papers that
are currently gating **live leg bans** were missing entries below (they were cited
extensively in leg journals/`DIRECTION.md`/`LITERATURE_CHECK.md` but never indexed here —
this manifest was 9 legs stale). Added as **Tier 0**. No new claims made; this is an
indexing fix only — see `LITERATURE_CHECK.md` and `DIRECTION.md` for the actual verdicts.

Fetch everything: `bash Papers/fetch.sh` (needs the hosts below allowlisted).
Fetch one: `bash Papers/fetch.sh 2207.07548`

---

## Tier 0 — currently gating live leg bans (added 2026-08-05, see STATUS above)

| arXiv | what it is | what it gates |
|---|---|---|
| **2505.03091** | Cadiot, *Stability analysis for localized solutions in PDEs and nonlocal equations on ℝ^m* | Independently states the off-diagonal/zero-diagonal dominance-hypothesis dichotomy (§2, §3) that leg 51's methodological claim rests on; leg 57 flagged it as a pre-emption, leg 62 (`LEG-B`, `leg/cp-v1` in `DIRECTION.md`) is the standing gate to settle its scope against the zero-diagonal case. |
| **1503.06315** | Breden–Desvillettes–Lessard, *Rigorous numerics for nonlinear operators with tridiagonal dominant linear part* (DCDS-A 35(10) 4765–4789) | Publishes the non-block-diagonal approximate inverse but requires a diagonal bounded away from zero, so it **narrows but does not cover** the zero-diagonal case leg 57's novelty claim needs — closed by `LITERATURE_CHECK.md`'s ninth pass reading the full text. |
| **2604.01868** | (CHL) novel self-similar blow-ups, 1D Hou–Luo and 2D Boussinesq — already listed in Tier 3 below; cross-referenced here because it is a live resurfacing-check gate | `reports/REPORT_2026-08-05.md` records a standing resurfacing check ("confirmed absent — search-index gap, not a fetch problem, second independent confirmation of leg 52") that keeps this paper in active rotation rather than closed. |

## Tier 1 — read these first; each one settles standing claims

| arXiv | what it is | what it gates |
|---|---|---|
| **2207.07548** | dissipative gCLM / relevance exponent | **THE most important one. Gates FOUR claims across THREE legs**: Route-F v1's `s_c = α/2` (§27), Route-H v1's `λ_μ = 2s − α₀` (§29), Route-I v1's growth-rate remeasurement (§30), and `α(1/2) = 3`. If this paper contains `s*(a) = 1/c_l(a)`, most of Routes F/H/I phenomenology is pre-empted and the writeups must say so. |
| **2210.07191** | Chen–Hou Part I — 2D Boussinesq finite-time blow-up | **The L1→L2 port's source of truth.** Spike 1 transcribed §2/§7 from it; the certification half still needs it. Also pins `β = 2.92` (Route-G's anchor). |
| **2209.08232** | (per LITERATURE_CHECK) | Gates the **finite-support** finding of Route-D v12/v13 — already assessed as *likely pre-empted*. Confirm or retract. |
| **2607.19762** | (per LITERATURE_CHECK) | Gates **Route-E v1's spectral picture** — already assessed as *likely pre-empted*. Confirm or retract. |

## Tier 2 — the methodological candidates, i.e. where novelty plausibly survives

| arXiv | what it is | what it gates |
|---|---|---|
| **2302.12877** | radii-polynomial / computer-assisted proof methodology | Gates the **only** claims with a real chance of being new: Route-D v6's discrete-ball trap, v3's weighted-`ℓ¹` no-go, and the elasticity discipline. Standard work uses geometric weights on bounded domains; ours is algebraic decay on an unbounded one. |
| **2312.01702** | tracking complex singularities on log-lattices | Gates "measure the exponent, not the threshold" (Route-F's method) and Route-I's log-periodic-band observation. The log-lattice programme is the most likely prior art for both. |
| **1908.09385** | dissipative gCLM | Second source on the relevance exponent; back-up for 2207.07548. |

## Tier 3 — would change numbers rather than claims

| arXiv | what it is | why |
|---|---|---|
| **2308.01528** | exact self-similar blow-up of the Hou–Luo model, smooth profiles | An *exact* profile gives an **exact `β`**, turning Route-G's `s_c = 1/(2β)` into a closed form for that model and giving the 2D leg a known-answer gate it does not currently have. |
| **2604.01868** | novel self-similar blow-ups, 1D Hou–Luo and 2D Boussinesq | If it exhibits **other** self-similar branches, Route-G's "the 2D scenario sits at `β = 2.92`" needs restating as "the Chen–Hou branch sits at 2.92" and the map needs more points. |
| 2010.01201, 2305.05895, 2401.14615, 2603.25104, 2604.09949 | assorted, cited in LITERATURE_CHECK | Context; lowest priority. |

## Not on arXiv — need another route

- **Schochet, CPAM 1986** — explicit solutions of the *viscous* CLM equation by
  complexification. **Gates Route-H's closed-form solution (E) directly**, which the leg
  already declines to claim. Publisher PDF; will not come from arXiv.
- **Nečas–Růžička–Šverák** (self-similar NS non-existence) and **Jia–Šverák**
  (the escaping class) — cited for framing in Routes H/I. Context, not gating.

---

## Host allowlist these need

`arxiv.org`, `export.arxiv.org`, `api.semanticscholar.org`, `www.semanticscholar.org`,
`link.springer.com`, `onlinelibrary.wiley.com`, `aimsciences.org`, `en.wikipedia.org`.

---

## STATUS 2026-08-19 (Conductor, pre-dispatch check for `PB2`): TWO LOAD-BEARING PRIMARIES WERE LIVING IN AN EPHEMERAL WORKTREE, AND ONE OF THEM CANNOT BE RE-FETCHED

**What was found.** `PB2` is briefed to open `W4` clause (b)'s two jaws at primary. `writeup/SOURCES.md`
records both as `FULL TEXT` with hashes. They were **not in `Papers/`**. Both existed only under
`.claude/worktrees/agent-*/Papers/`, which `.gitignore:52` excludes and which is deleted on worktree
cleanup. They have been copied into `Papers/` and verified against the hashes in `SOURCES.md`:

| file | sha256 (12) | matches `SOURCES.md` | `pdftotext -layout` | re-fetchable by `fetch.sh`? |
|---|---|---|---|---|
| `1610.09464.pdf` Chae–Wolf | `1f537bc2b6b2` | **YES** (also md5 `f1d14db1`) | 1002 lines — **matches record** | yes, arXiv |
| `TSAI1998.pdf` Tsai *ARMA* 143 (1998) | `6d3182d53806` | **YES** | 1258 lines — **matches record** | **NO** |

**The finding that matters, and it is an availability finding rather than a mathematical one.**
`fetch.sh` is arXiv-only. **Tsai 1998 is pre-arXiv and was obtained from the author's page**, so the
committed fetcher cannot re-pull it. That PDF is the source in which **NRŠ 1996's hypothesis is
pinned by verbatim quotation** (`SOURCES.md` row 3 is `SECOND HAND`; row 2 is what makes it usable).
**The load-bearing half of `W4` clause (b)'s second jaw was one `git worktree prune` from being
unrecoverable inside this container**, and nothing in the discipline was watching. This is the same
shape as the seed-field blocker: not compute, a `.gitignore` line.

**And the part where the record survived the check.** The line counts in `SOURCES.md` looked wrong
against the `.txt` files on disk (1851 vs 1258; 1002 vs 1002). They are not wrong. Re-running the
extractor settles it: `pdftotext -layout` reproduces **1258** and **1002** exactly, and the 1851-line
file is simply a no-`-layout` extraction of the same bit-identical PDF. **A recorded line count is
reproducible only if the extraction MODE is named**, and `SOURCES.md` does name it. The suspicion was
mine and the record refuted it.

**Residual, not resolved, handed to `PB2`.** `SOURCES.md` row 1 reads *"1002 lines; re-fetched md5
`f1d14db1…`, 1021 lines"*. `f1d14db1` is the md5 of the **same** PDF whose sha256 is `1f537bc2` — one
file, two algorithms, presented as two fetches. **1021 reproduces under neither mode here** (1002
`-layout`, 1609 plain). Likely a `poppler` version difference; **unverified, and it is not a
discrepancy in the source, which is bit-identical.**

**Policy unchanged: the PDFs stay untracked.** `Papers/*` is gitignored for copyright and that is
correct. What is committed is this pointer plus the hashes, so the next session can tell whether the
file it has is the file the record was written against.

---

## LEG 411 (`PB1`, wave 8) — the recurrence-mining corpus fetched for `P1`'s novelty check

**Nine PDFs fetched from arXiv on 2026-08-19 by `curl https://arxiv.org/pdf/<id>` (HTTP 200 first
attempt, every one). `Papers/` is gitignored: pointers and hashes only, never a PDF.**

| file | id | what it is | sha256 |
|---|---|---|---|
| `1207.4682.pdf` | `1207.4682v1` | Chandler & Kerswell, *JFM* **722**:554–595 (2013) | `343d2173…88d80cf` |
| `1406.1820.pdf` | `1406.1820v2` | Lucas & Kerswell, *Phys. Fluids* **27** 045106 (2015), doi `10.1063/1.4917279` | `da9cab5c…f479258` |
| `1406.1820v1.pdf` | `1406.1820v1` | **the version actually quoted** — see the extraction note below | `edf2f7e9…9a6cbad76` |
| `1308.3356.pdf` | `1308.3356v3` | Lucas & Kerswell, 2D Kolmogorov over large domains | `f39f1333…e00e541c` |
| `physics_0604062.pdf` | `physics/0604062` | Viswanath 2007, the founding hookstep paper | `fe9fe1aa…4d5dc5d6` |
| `2309.12754.pdf` | `2309.12754v1` | Page, Holey, Brenner & Kerswell, *JFM* **991** (2024) A10, doi `10.1017/jfm.2024.552` | `5e47a4bd…8200b612` |
| `1108.0975.pdf` | `1108.0975v1` | Kawahara, Uhlmann & van Veen, *Annu. Rev. Fluid Mech.* **44**:203–225 (2012) | `9e4d666e…6fe47be2a9` |
| `1611.04829.pdf` | `1611.04829v1` | Lucas & Kerswell 2017, sustaining processes from recurrent flows | `2ef11677…3cfbbda198` |
| `0810.1974.pdf` | `0810.1974v1` | Halcrow–Gibson–Cvitanović line, plane Couette UPOs | `065f947a…43e3b55a5` |
| `1705.03720.pdf` | `1705.03720v2` | Willis, Cvitanović & Avila, RPOs as the backbone of pipe flow | `85a5b22f…368b08772c` |

**EXTRACTION NOTE, AND IT IS LOAD-BEARING FOR EVERY QUOTE TAKEN FROM `1406.1820`.** The **v2** PDF
carries a **doubled text layer** — two copies of the running text at nearly the same coordinates —
so `pdftotext` (with or without `-layout`, and with column cropping) returns interleaved,
unreadable prose on the pages that matter. **v1 extracts cleanly and is what leg 411 quotes.** The
one sentence leg 411 leans on hardest was then **re-checked in the v2 extraction and is present
there verbatim** (`1406.1820.txt` line 478 vs `lk_v1.txt` line 267), so the quote is not an
artefact of the version chosen. Pagination differs between versions; leg 411 cites **v1 pages**.

**`ANNUREV` NOTE.** `1108.0975` was declared **UNREACHABLE in advance** by leg 411's own
pre-registration, as a review in a journal-only venue. **That declaration was WRONG in the safe
direction: the review IS on arXiv, with its `journal_ref` attached, and it was fetched and read.**
Recorded here rather than silently corrected, per the standing rule on controls and declarations
that do not fire as planted.
