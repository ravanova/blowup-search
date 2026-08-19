# SOURCES — the source register (`ORCHESTRATION.md` §3k rule 1)

**Built 2026-08-18 by the Conductor, wave 6, by sweeping the LANDED record** (`WALLS.md`,
`STATE.md`, `OPTIONS.md`, `writeup/data/*.json`, `experiments/journal/`). **IT IS INCOMPLETE AND
SHIPS INCOMPLETE** — see *What this sweep did not cover* at the foot. Its value is the **DEPTH**
column, not its coverage.

**Scale of the sweep, so the incompleteness is quantified:** the record mentions **1,671 distinct
arXiv ids**; almost all are *screening* output (a title matched a query), which is not a read.
Only **6** appear anywhere in the three load-bearing files. This register lists what the record
can show was actually **opened**, and by whom.

## Depth vocabulary

§3k names three: `ABSTRACT`, `FULL TEXT`, `RECOMPUTED`. The record needs two more and uses them
already, so they are carried here rather than silently collapsed into §3k's three:

| depth | meaning |
|---|---|
| `ABSTRACT` | title/abstract only. **Under §3k rule 2 this may not carry a load-bearing claim.** |
| `FULL TEXT` | the document itself was fetched and read; where a hash is recorded it is cited |
| `RECOMPUTED` | its numbers were re-derived here and compared |
| `SECOND HAND` | primary not obtainable; hypothesis taken **verbatim** from a source read at FULL TEXT. Weaker than `FULL TEXT`, **stronger than `ABSTRACT`** |
| `UNREACHABLE` | pre-arXiv/journal-only, **banked as UNREACHABLE in advance, never as a zero** |

## The register

| # | source | claim it supports | DEPTH | read by | load-bearing |
|---|---|---|---|---|---|
| 1 | `arXiv:1610.09464` Chae–Wolf | **`α ≥ 1`** (Thm 1.1); Rmk 1.2's `L³` clause is one jaw of the `α ≤ 1` side | **FULL TEXT** (sha256 `1f537bc2…`, 1002 lines; re-fetched md5 `f1d14db1…`, 1021 lines) | leg 359 (first primary read here), re-fetched leg 397 (`L2′`) | **YES** |
| 2 | Tsai, *ARMA* **143** (1998) 29–51 | Thm 1 (`U ∈ L^q`, `q ∈ (3,∞]`) and **Thm 2** (local energy estimates, **no `L^q` in the hypothesis**) — `L5`'s second jaw, exactly-SS excluded | **FULL TEXT** — author's page PDF **independently re-downloaded**, re-hashed (sha256 `6d3182d5…`), `pdftotext -layout` 1258 lines, diffed against the cached extraction, byte-identical | leg 359; re-quoted legs 364, 365 | **YES** |
| 3 | Nečas–Růžička–Šverák, *ARMA* **136** (1996) | `U ∈ L³(ℝ³) ⟹ U ≡ 0` — the other half of `L5`'s second jaw | **SECOND HAND**, two independent sources agreeing exactly: Tsai 1998 p.30 quoting `[NRS]` (1.3) verbatim (row 2, FULL TEXT) + the Bradshaw–Tsai survey. Primary is pre-arXiv, **never obtained** | leg 364 (`NRSV`) | **YES** |
| 4 | `arXiv:math/0510396` Seregin §1 | the **local** suitable-weak form whose `m_T` separates the cases **exactly at the `α = 1` pin** — this is what the `α ≤ 1` side actually runs through | **FULL TEXT** (fetched at primary during the verification, by an ESŠ author) | `V-W4` | **YES** |
| 5 | Escauriaza–Seregin–Šverák 2003, *Russ. Math. Surveys* **58** | the `α ≤ 1` direction **as originally cited** | **UNREACHABLE** (journal-only), banked in advance | — | **YES, but superseded**: `V-W4` moved the step onto row 4, read at primary |
| 6 | `arXiv:2607.09619` Pineau–Vicol | Thms 1.6/1.7 (rotated backward SS); PV's own restatement of Chae–Wolf | **FULL TEXT** (v1 leg 330; v2 md5 `53680cb8…`, 2278 lines, leg 397; read again 2026-08-07) | legs 330, 397, `PVRW` | **YES** |
| 7 | `arXiv:2509.25116v2` | `W3`'s cell occupancy; the certificate's constants | **FULL TEXT + RECOMPUTED** — 24 constants re-derived at 50 dps; **4 are wrong as printed**, closure survives | `V5` (leg 402) | **YES** |
| 8 | `arXiv:1902.00384` | `C1`'s **exemplar**; `W2`'s certified rows | **`ABSTRACT` for 45 legs** → `FULL TEXT` (`T6`) → **`RECOMPUTED`** (`T4`, verified `V-W2`): both certified rows are **2D lifts**, so it **fails `W2`'s own pre-committed test** | leg 348 (abstract), `T6`, `T4`/`V-W2` | **YES** |
| 9 | `arXiv:2410.05480` Dähne–Figueras (CGL) | radii-polynomial technology **works off the fluid axis** | **RECOMPUTED** — reproduced row-for-row | leg 316 | **YES** |
| 10 | `arXiv:2409.09234` | leg 348's `domain_census` **over-counts by one** — this is **not** an instance of the technology | **FULL TEXT** | `T6`, verified `V-W2` | **YES** (it makes a census claim false) |
| 11 | Fefferman, *Existence and smoothness of the Navier–Stokes equation* (official Clay problem description) + Clay Millennium **rules** page/PDF | conditions (7)/(8)/(9); the prize direction (C)/(D); what a submission must be | **FULL TEXT** (both URLs pinned in `p2_route_cobv_v1.json`) | `COBV` | **YES** |
| 12 | `arXiv:2006.15776` (Leray backward SS in Morrey spaces) | flagged in-record as **`SECONDARY for NRS/Tsai`** — supports row 3's second-hand route | **FULL TEXT** (md5 `a5341254…`, 1694 lines) | leg 397 (`L2′`) | supporting |
| 13 | `arXiv:2202.08352` Bradshaw–Tsai (spatial decay, DSS) | DSS decay rates used against the screened object | **FULL TEXT** (2134 lines) | leg 397 | supporting |
| 14 | `arXiv:2409.13586` (DSS with rough data) | asymptotics of DSS solutions | **FULL TEXT** (1837 lines) | leg 397 | supporting |
| 15 | `arXiv:1204.0529` Jia–Šverák; `1210.2783`, `1703.03480` Bradshaw–Tsai | forward (D)SS existence — family F3 | **FULL TEXT** (1486 / 1060 / 1412 lines) | leg 397 | supporting |
| 16 | `arXiv:1910.00173`, `2210.07191` Chen–Hou; `1904.04795` Elgindi; `1910.14071` Elgindi–Ghoul–Masmoudi | the `C^{1,α}` blow-up line; `L3`'s persistence-under-localisation lane | **FULL TEXT** (5599 / 12021 / 3680 / 1694 lines) | leg 397 | not yet |
| 17 | `arXiv:1912.11009` MRRS; `2606.12758` | implosion / self-similar imploding — family F5 | **FULL TEXT** (6550 / 1557 lines) | leg 397 | not yet |
| 18 | `arXiv:2112.03116`, `2209.03530` Albritton–Brué–Colombo | **nonuniqueness** (forced NS; gluing) — the class `2509.25116` belongs to; bears on the open `W2` scope escalation | **FULL TEXT** (1647 / 1187 lines) | leg 397 | see escalation |
| 19 | Bogovskiĭ 1979 | the divergence corrector | **UNREACHABLE** (journal-only), declared in advance; secondary `arXiv:1103.3718` at **FULL TEXT** (927 lines) | leg 397 | supporting |
| 20 | Giga–Kohn | asymptotically-SS machinery | **UNREACHABLE**, declared in advance, quoted through secondaries | — | supporting |
| 21 | `arXiv:2308.01528` | `OPTIONS.md` §L3 calls it "**the record's best lead**" on persistence under localisation | **`ABSTRACT`** | `DECR` lit sweep | **NO — and it must stay NO until read** |
| 22 | `arXiv:1801.08060` Bradshaw–Tsai (DSS, `L²_loc`, local energy inequality) | adjacent to `L5`'s jaw, flagged off-gate | **`ABSTRACT`** | leg 359 | **NO** |
| 23 | **JAX-CFD** `jax_cfd.spectral.equations.ForcedNavierStokes2D` + `forcings.kolmogorov_forcing` — Kochkov, Smith, Alieva, Wang, Brenner & Hoyer, *Machine learning–accelerated computational fluid dynamics*, **PNAS 118(21) e2101784118 (2021)**, `arXiv:2102.01010` | the **reference implementation** `R-prof` profiles against: same equation (2D NSE in vorticity form with Kolmogorov forcing), same discretisation family (pseudospectral, dealiased), **independently authored and peer-reviewed** | **SOURCE READ AND EXECUTED** — wheel `jax_cfd-0.2.1` fetched, `spectral/equations.py` read, and the object **constructed and stepped at `N = 24`** under `jax 0.11.1` (state `(24,13) complex128`, `crank_nicolson_rk4`). **The PAPER is NOT read** — only the code is, and it is the code that is load-bearing here. | Conductor, 2026-08-19, pre-registration | **YES for `R-prof`'s gate** |
| 24 | **FFTW3** — Frigo & Johnson, *The design and implementation of FFTW3*, **Proc. IEEE 93(2):216–231 (2005)**, via `pyfftw 0.15.1` | the **transform-cost floor**: 20 transforms of `24 × 24` per RK4 step is the algorithmic price of the step, so anything far above it is overhead, not arithmetic | **LIBRARY FETCHED, PAPER CITATION ONLY.** The load-bearing artefact is the *library measurement*, not the paper's text; recorded as `CITATION` so no reader mistakes it for a read. | Conductor, 2026-08-19, pre-registration | **YES for `R-prof`'s gate** |
| 25 | Chandler & Kerswell, *Invariant recurrent solutions embedded in a turbulent two-dimensional Kolmogorov flow*, **JFM 722:554–595 (2013)**, `doi:10.1017/jfm.2013.122`, `arXiv:1207.4682` | the **published method** this repo's whole Newton–hookstep campaign on 2D Kolmogorov flow is an instance of | **CITATION, UNREAD HERE — but CORROBORATED, not assumed.** The reference implementation of row 23 **cites this paper by name for its own time stepper** (`jax_cfd/spectral/time_stepping.py`, `crank_nicolson_rk2`, *"(Section 3)"*), which confirms the doi and volume and puts the reference and this repo in the **same published lineage**. **Still not read; nothing may rest on it.** | Conductor, 2026-08-19 (citation seen in the reference's source, not the paper) | no |
| 26 | Canuto, Hussaini, Quarteroni & Zang, *Spectral Methods: Evolution to Complex Geometries and Applications to Fluid Dynamics*, **Springer (2007)**, `doi:10.1007/978-3-540-30728-0`, **Appendix D.3** | the textbook IMEX / low-storage Runge–Kutta–Crank–Nicolson family. **Still the correct home of the family; NO LONGER the named remedy for `R4-a`** — `WAVE8_PLAN.md` AMENDMENT 2 names `crank_nicolson_rk2` instead, whose own published home is row 25. | **SECOND HAND.** Located as the citation `jax_cfd`'s `low_storage_runge_kutta_crank_nicolson` gives for itself; the **book is not held here**. **CORRECTED 2026-08-19: the executable form is available ONLY VIA A PINNED RE-INSTALL, not `available` full stop** — it lived in a 615 MB *session-scoped scratchpad* venv that does not survive the session. Reproducible instead from `jax-cfd==0.2.1` + `sha256 11ede6ca9f0c22a1a0b3513df3c0d6ef96a48258f6d06126d47e80cad8fcee09` on `jax_cfd/spectral/time_stepping.py`. | Conductor, 2026-08-19 (corrected same day) | **no longer for `R4-a`; family attribution only** |

## Rule-2 findings (a load-bearing claim may not rest on an abstract)

**No live load-bearing claim in `WALLS.md`/`STATE.md` rests on an `ABSTRACT`.** Two findings, both
recorded rather than assumed:

1. **The record's own worked instance of rule 2 biting is row 8.** `arXiv:1902.00384` carried
   `C1`'s exemplar at **abstract depth for 45 legs**, through an escalation and a user ruling.
   When it was finally read at full text and then recomputed, **the exemplar fell**. This is the
   empirical case for §3k, made by this repo before §3k existed.
2. **The weakest live link is row 3, and it is `SECOND HAND`, not `ABSTRACT`.** NRŠ 1996 has never
   been obtained here. Its hypothesis is pinned by a **verbatim quotation inside Tsai 1998**,
   which *was* read at primary, plus a second independent restatement. **Debt: MEDIUM, not
   BLOCKING** — and note leg 364's finding that the *ledger's quoted deciding clause* (Tsai Thm 1,
   `q ∈ (3,∞]`) does **not** cover NRŠ's own `q = 3`, while the ledger's *operational* test does.

## Correction to the directive that ordered this file

The §3k directive named "**Chae–Wolf Thm 1.1 + Rmk 1.2, the ESŠ step, and NRŠ/Tsai read at full
text**" as an undischarged debt. **Against the record, three of those four are already discharged
at primary**: Chae–Wolf (row 1, leg 359, hashed), Seregin's local form that the ESŠ step now runs
through (row 4, `V-W4`), and **Tsai 1998 (row 2, leg 359, independently re-downloaded and diffed)**.
**Only NRŠ 1996 is unread at primary, and it is `SECOND HAND`, not `ABSTRACT`.** ESŠ 2003 itself
is `UNREACHABLE` and superseded. The remaining primary-read unit is therefore **much smaller than
the directive priced** — and what it should actually buy is a **forward-citation pass** on NRŠ
1996 (`OPTIONS.md` `T2′`), not a re-read of papers already hashed here.

## Owed at pre-registration (§3k rule 3 — do not rebuild what is published)

**No wave-7 construction unit may be dispatched until its row here is filled.** Currently EMPTY:

| lane | what would be built | published method it must name |
|---|---|---|
| **R2** | deflation to stop re-finding solutions (4 of `U5`'s 5 were re-finds) | **NAMED, UNREAD** — `OPTIONS.md` §B writes "Farrell–Birkisson–Funke". **Naming is not reading**: this register records **no depth** for it. Read at primary before a line is written. |
| **R3** | multiple shooting for the periodic-orbit boundary-value problem | **UNNAMED** — a textbook technique. Same requirement. |
| **R4** | second-order stepper replacing `U3`'s Lie–Trotter | **NAMED 2026-08-19 — DEBT DISCHARGED. Specification: `writeup/waves/WAVE8_PLAN.md` AMENDMENT 2 §3, committed before dispatch.** Two steppers, both 2nd order: **`S1` = `crank_nicolson_rk2`** (`jax-cfd==0.2.1`, `jax_cfd/spectral/time_stepping.py:81-114`, hash pinned, **EXECUTED not cited**; published home = **row 25, Chandler & Kerswell §3 — the paper `M1` reproduces**), and **`S2` = Strang-split integrating factor** `E½·RK4_N(E½·w)`, which unlike `S1` keeps the viscous term **exact** as `U3` had it. They differ in exactly that one property, so together they separate *"the first-order splitting moved the orbits"* from *"Crank–Nicolson moved them"* — a single stepper cannot, and would have reported the louder reading. **The old `FULL TEXT` pre-condition on Strang 1968 is WITHDRAWN as defective** (wrong scheme; and it put the load on a citation when the claim rests on a measured order ≈ 2). Strang, *SIAM J. Numer. Anal.* **5(3):506–517 (1968)** stays **cited, not read**, as attribution carrying nothing. |
| **R-prof** | profiling the inner loop against a reference | **NAMED, FETCHED AND VERIFIED EXECUTABLE 2026-08-19 (row 23 + row 24).** Solver level: **JAX-CFD's `ForcedNavierStokes2D`** — same equation, published, independently authored — constructed and stepped at `N = 24` here before dispatch, so the gate is answerable and not a claim nobody can execute (**lesson 68**). Transform level: **FFTW3 via `pyfftw`**, giving the 20-transform floor. **Two differences the unit must MEASURE AND REPORT, not paper over:** the reference steps with **Crank–Nicolson RK4** where ours uses an exact integrating factor + RK4, and it transforms with **`rfftn` (24×13)** where ours uses full **`fft2` (24×24)**. A per-step ratio that ignores either is not an answer. **A self-authored benchmark is still not a reference.** |
| **R-bank** | committing the seed fields | no method to cite — it is provenance, not an algorithm. **Exempt, and the exemption is stated rather than assumed.** |

## What this sweep did not cover

- Every source touched by **screening** legs (the bulk of the 1,671 ids). By construction those
  are `ABSTRACT` or less; none is load-bearing; adding them would drown the DEPTH column.
- The **Ohta–Kawasaki / van den Berg–Williams** line (leg 172) and the rest of the `C1`
  exemplar-family reading — depth not established in this sweep, so **no row was invented**.
- The **`T` lane's** torus literature, deferred with the lane.
- Sources touched only on **unmerged branches** (e.g. `leg/253-nrsx-v1`, parked and escalated),
  except where a landed leg re-verified them independently — which is exactly what leg 359 did.

**Maintenance (§3k rule 1):** a unit that reads a source **updates this file in the same commit**
that lands its artefact. A row with no DEPTH is a defect.

## Appended 2026-08-19 by `L6-b` (leg 406) — APPEND-ONLY, nothing above this line edited

**§3k rule 3, discharged rather than assumed.** `L6-b` builds **no new method**: it runs
`L6`'s own apparatus (`experiments/p2_route_l6_v1.py`, imported unchanged) at a 25× larger
iteration cap. The published method that apparatus implements, named with its citation as the
rule requires:

| # | source | claim it supports | DEPTH | read by | load-bearing |
|---|---|---|---|---|---|
| L6b-1 | Byrd, Lu, Nocedal, Zhu, *"A limited memory algorithm for bound constrained optimization"*, **SIAM J. Sci. Comput. 16(5) (1995) 1190–1208** | the minimiser used by `L6` (leg 401 §0.3) and by `L6-b` (leg 406) — L-BFGS-B, via `scipy.optimize.minimize(method="L-BFGS-B")` | **`ABSTRACT`** — the *implementation* is used and exercised; the **paper is not read at primary** | `L6` named it, `L6-b` records the depth | **NO** — and the reason is executable, not rhetorical: every number `L6-b` reports is the value of a residual functional at a banked coefficient vector, recomputable by anyone from `writeup/data/p2_route_l6b_v1.json` **without knowing which algorithm produced the vector**. If the 1995 paper were wrong, no claim in `WALLS.md`, `STATE.md`, `CLAY_OBLIGATIONS.md` or `L6-b`'s gate answer would change. Under §3k rule 2 an `ABSTRACT` row may not carry a load-bearing claim, and this one carries none. |

**Note for whoever fills the "Owed at pre-registration" table.** `L6`'s own row was never
added there; this row supplies the depth retrospectively for the optimiser both units use.
It does **not** discharge anything owed for `R2`, `R3`, `R4` or the NRŠ 1996 `SECOND HAND`
debt, all of which remain exactly as recorded above.

## Appended by `R-prof` (leg 405, wave 7) — EXECUTION RECORD, rows 23–26 untouched

**§3k rule 1 asks a unit that reads a source to update its row in the same commit; my brief
forbids me editing rows 23–26, which the Conductor filled correctly before dispatch. So this is
appended beside them rather than written into them.** It records the DEPTH at which `R-prof`
actually consumed each, which is the column §3k says the register exists for.

| # | source | what `R-prof` did with it | DEPTH REACHED BY THIS UNIT | load-bearing |
|---|---|---|---|---|
| 27 | **row 23** — JAX-CFD `ForcedNavierStokes2D` + `crank_nicolson_rk4` (Kochkov *et al.*, PNAS 118(21) e2101784118, 2021) | **CONSTRUCTED, STEPPED AND TIMED at `N = 24`** under `jax 0.11.1` / `jax_cfd 0.2.1`, x64, state `(24,13) complex128`; `explicit_terms` and `time_stepping.crank_nicolson_rk4` **read in source** to count 5 explicit stages and 5 transforms per stage, and to establish that `kolmogorov_forcing`'s two `rfft2` calls are **grid-only and therefore constant-folded under `jit`**, so they are NOT in the 25. Reference sanity checked: the state advances and stays finite over 200 steps. | **CODE READ + EXECUTED + MEASURED.** The **PNAS paper itself remains UNREAD** — the code is what is load-bearing here, and nothing in this unit rests on the paper's text. | **YES — gate (iii)** |
| 28 | **row 24** — FFTW3 (Frigo & Johnson, *Proc. IEEE* **93(2):216–231**, 2005) via `pyfftw 0.15.1` | planned `FFTW_MEASURE` transforms on aligned buffers, complex `24×24` **and** real `24×24 → 24×13`, timed in the same interleaved rounds as everything else. Supplies both the 20-transform floor and the **measured** `rfft2/fft2` cost ratio at this size. | **LIBRARY EXECUTED AND MEASURED; PAPER CITATION ONLY.** | **YES — gate (iii)'s floor** |
| 29 | **row 25** — Chandler & Kerswell, *JFM* **722:554–595** (2013) | **not used.** Recorded here only to state that this unit did **not** upgrade its depth and rests nothing on it, as the brief requires. | **CITATION ONLY, UNREAD** | no |
| 30 | numpy's `numpy.fft` (pocketfft) as shipped in `numpy 2.5.1` / `2.5.2` | the **object under measurement**, not a source: every claim about its per-call cost in this leg is `R-prof`'s own measurement, reproducible from `experiments/programme_r4/profiling/r_prof_v1.py`. **No published claim is being leaned on**, so no depth applies. | n/a — **measured, not cited** | **YES, but self-measured** |
| 31 | R. H. Byrd, P. Lu, J. Nocedal, C. Zhu, *A limited memory algorithm for bound constrained optimization*, **SIAM J. Sci. Comput. 16(5):1190–1208** (1995) — `L6`'s `C1`-discharging apparatus (L-BFGS-B) | **LIBRARY EXECUTED, PAPER CITATION ONLY.** `scipy.optimize.minimize(method='L-BFGS-B')` is run by `experiments/p2_route_l6_v1.py` and by `L6-b`; the paper itself is **not opened here**. What `L6` asserts from it — that the method builds **no** bounded approximate inverse uniform in `M`, so `C1` is not engaged — is a statement about the algorithm's *form* (a limited-memory secant approximation to the Hessian of the objective, never an inverse of the linearised operator), and it is checkable from the library's documented interface without the paper. | **YES — `L6`'s `ban_C1.engaged = false` rests on it** |
| 32 | S. Chandrasekhar, *Hydrodynamic and Hydromagnetic Stability* (Oxford, 1961), §II — the poloidal–toroidal representation `V = curl curl (f y) + curl (g y)` used as `L6`'s trial space | **CITATION, UNREAD HERE.** The representation is used because it makes `div V ≡ 0` **identically**, so no Bogovskiĭ corrector is needed; that property is verified in this repository by measurement, not by citation — `L6` selftest `T_A` gives `max|div V| / scale = 1.97e-11`. **The claim that the representation is COMPLETE for divergence-free fields on `ℝ³` is NOT established here and nothing live depends on it**; `L6` needs only that its elements are divergence-free, which is measured. | **YES for divergence-freeness (measured, not cited); NO for completeness (not claimed)** |

**Added 2026-08-19, closing `D-VW6-6`.** `V-W6` recorded that neither row existed at the wave-6/7
bound, and that this is the **landing commit's gap — mine, not `L6`'s**, because §3k postdates `L6`'s
dispatch. Both are now registered with a DEPTH, and both DEPTHs are **honest about what was not**
**opened**: neither paper was read at primary here. `L-JVER` (`WAVE8_PLAN.md` AMENDMENT 1) carries
the standing obligation to keep them current if it upgrades either depth.

**§3k rule 3 (do not rebuild what is published) — the exemption, stated rather than assumed.**
`R-prof` **builds nothing**: it measures a module it is forbidden to modify. The one candidate
change it prices (planned FFTW3 transforms in place of per-call `numpy.fft`, and batching the four
inverse transforms of a stage into one call) is **not a numerical method** — it is the documented
use of row 24's library and of `numpy.fft`'s own `axes=` argument. **It is priced, not landed**, and
a unit that lands it owes its own equivalence check.

---

## Appended 2026-08-19 by `PB2` (leg 410, Lane L) — APPEND-ONLY, nothing above this line edited

**Scope.** AMENDMENT 4 re-scoped this unit away from re-reading sources already at primary. Three
of four rows were already discharged; this block records (i) hash re-confirmations, (ii) the ONE
new depth reached, (iii) the residual on row 1 **RESOLVED**, and (iv) a **citation correction** to
row 3 placed beside it, not over it.

| # | source | what `PB2` did with it | DEPTH REACHED BY THIS UNIT | load-bearing |
|---|---|---|---|---|
| 33 | **row 2** — Tsai, *ARMA* **143** (1998) 29–51, `Papers/TSAI1998.pdf` | Read at primary for the question row 2 did not answer: **which** theorem excludes the exactly-self-similar object. Quoted verbatim: **Thm 1** (p.30, `U ∈ L^q`, **`q ∈ (3,∞]`, open at 3**), **Thm 2** (p.30), the **Thm 2 hypothesis list** (§2 p.34 — *"our only requirements (apart from self-similarity) are (i) and (ii)"*, i.e. the equations and the local energy estimates `(1.4)`; **no `L^q` in the hypothesis**), `(1.2)`–`(1.5)`, and **Rmk 5.3 / Rmk 5.4** (p.49 — a third weaker sufficient condition `|U(y)| ≤ b\|y\|`, `b < a`; and that the growth assumptions **are** necessary, since `U = ∇Φ` with `Φ` harmonic solves `(1.3)` nontrivially) | **FULL TEXT** (confirmed, not newly reached). sha256 `6d3182d53806ce82fa0a2d834b31b758f22399ff625b8c8d7025a65f83fb8182` **matches** the leg-359 pin; `pdftotext -layout` **1258 lines**, matches | **YES — `Thm 2` is what actually carries `W4` clause (b)** |
| 34 | **row 1** — Chae–Wolf `arXiv:1610.09464`, `Papers/1610.09464.pdf` | **NOT re-read** (AMENDMENT 4). Hashes and line counts re-confirmed only | **FULL TEXT** unchanged (leg 359). sha256 `1f537bc2…` and md5 `f1d14db1…` both **match, on the SAME file** | **YES**, unchanged |
| 35 | **row 3** — Nečas–Růžička–Šverák 1996 | Two further fetch attempts, with a **positive network control** leg 364 lacked | **`UNREACHABLE`** at primary (4th independent reproduction: legs 253, 359, 364, 410). Hypothesis remains **`SECOND HAND`** via row 2's verbatim quotation | **NO for `W4` clause (b)** — see the correction below. Still `YES` wherever an `L³` hypothesis is genuinely in play |

### Row 1's residual — **RESOLVED**, not `UNVERIFIED`

Row 1 reads *"1002 lines; re-fetched md5 `f1d14db1…`, 1021 lines"*, which presents one file as two
fetches with two line counts, and `1021` reproduces under **neither** `-layout` (1002) nor plain
(1609). The gap is exactly **19**, and `pdfinfo` gives `Pages: 19`; `grep -c $'\f'` on the same
`-layout` extraction returns **19**. **One file, one extraction, counted once with and once without
page-break form feeds as line terminators.** Both hashes are of the same file and both match. No
second fetch ever happened. **The row is sound; its wording is not, and the wording is left as
banked with this note beside it.**

### Row 3 — CITATION CORRECTION, and the depth finding that matters more

Row 3 (and `WALLS.md` W4(b), `WAVE8_PLAN.md`, and `p2_route_l5_finite_energy_v1.json`) cites NRŠ as
***ARMA* 136 (1996)**, the JSON adding pages `55–98`. Tsai's bibliography, p.50, at FULL TEXT:

> `[NRS]` J. Nečas, M. Růžička & V. Šverák, *On Leray's self-similar solutions of the Navier-Stokes
> equations*, **Acta Math. 176 (1996), 283–294.**

**Wrong journal, wrong volume, wrong pages, in four load-bearing places.** **FIVE, at the landing audit — `CORRECTIONS.md` §47b.** The fifth is `experiments/p2_route_l5_v1_driver.py:640`, which GENERATES the fourth; it is now corrected, and the banked JSON is deliberately left as it was under the W3 Q3 ruling, so a regeneration will differ in that field by design. `WAVE8_PLAN.md` AMENDMENT 4 also propagated the wrong citation in its own jaw table, written by the Conductor while auditing citations. Leg 364's journal
already carried it correctly (with DOI `10.1007/BF02551584`). Banked in full at `CORRECTIONS.md`
**§47**. The two fetch attempts this leg, for the record:

- Springer (`link.springer.com/article/10.1007/BF02551584`) → **login wall**, 247,202 B HTML,
  sha256 `04165b7d…`, containing *"Access this article"* / *"Log in"* / *"institutional"*, with
  **empty** `description` and `citation_abstract` meta tags — so **not even `ABSTRACT` depth** is
  obtainable from the landing page.
- Project Euclid → 1,165 B Incapsula stub, sha256 `d05e2720…`.
- **Positive control:** `arxiv.org/abs/1802.00038` → **HTTP 200, 38,114 B**. The container **has**
  network; the refusal is the publisher's, not the sandbox's. *(No paywall was circumvented and no
  author, group, maintainer or list was contacted.)*

**The depth finding.** `PB2` measured that the route-4 object at the pinned `α = 1` has
**log-divergent `∫|U|³`** (increments constant at `139.287` per decade; coefficient
`60.4916579840` measured against `60.4916579840` closed-form, rel. `1.1e-13`), so **`U ∉ L³` and
NRŠ's hypothesis is NOT SATISFIED.** The one source this repository cannot obtain is the one that
**does not carry the case**. Row 3's `SECOND HAND` debt is real and stays open — it is simply no
longer what `W4` clause (b) rests on. Measurements: `writeup/data/p2_route_pb2_v1.json`; checks:
`experiments/p2_route_pb2_v1_evidence.py` (31 checks, 0 failed).

## LEG 411 (`PB1`, wave 8) — the recurrence-mining corpus, read for `P1`'s novelty gate

**Twelve distinct works / thirteen files, ALL READ AT `FULL TEXT` DEPTH**, fetched from arXiv
on 2026-08-19 and hashed in `Papers/MANIFEST.md`. Added in the same commit as the reads, per
§3k rule 1. `Papers/` is gitignored (copyrighted PDFs): pointers and hashes only, never a PDF.

**Pagination cited by leg 411 is arXiv PREPRINT pagination, NOT journal pagination**, and is
labelled as such in `writeup/papers/P1_SELECTION_BIAS/NOVELTY.md`. No paywalled version was
fetched and no paywall was circumvented. **No external contact of any kind was made.**

Every quote drawn from these documents is banked in
`writeup/data/p1_novelty_fulltext_v1.json` — because `Papers/` is gitignored, the verdict has
to stay readable in a checkout where these PDFs do not exist — and each banked quote is
re-verified against the PDF page it claims, from the bytes, by
`experiments/p1_novelty_v1_evidence.py` check `quotes_on_claimed_pages`
(class `recompute-from-primary`).

**ROW 25 AND ROW 29 ARE WRONG AND THIS UNIT DID NOT EDIT THEM.** Both record Chandler &
Kerswell 2013 as `CITATION, UNREAD HERE` / `CITATION ONLY, UNREAD`. `experiments/journal/leg_358.md`
§1–2 read it at full text, and leg 411 has now re-read it at primary and CONFIRMED leg 358's
`7/163 = 4.3%` from Table 1. Row 36 below places the true depth beside them rather than over
them. The amendment to rows 25/29 belongs to the Conductor:
`writeup/papers/P1_SELECTION_BIAS/FINDINGS.md` **F3**.

| # | source | what leg 411 did with it | DEPTH REACHED BY THIS UNIT | load-bearing |
|---|---|---|---|---|
| 36 | Chandler & Kerswell, *Invariant recurrent solutions embedded in a turbulent two-dimensional Kolmogorov flow*, **JFM 722:554–595 (2013)**, `Papers/1207.4682.pdf` | Gate effect (b) at `S3` (p.14 `considerable duplication`, quantified in Table 1) and effect (a) at `S2` (p.13, search confined to `s = m = 0` shifts, Series B commissioned to undo it). **ALSO: Table 1 RE-READ AT PRIMARY and leg 358's `7/163 = 4.3%` CONFIRMED** — see FINDINGS F3, row 25's depth register is wrong. | **FULL TEXT** — sha256 `343d2173…88d80cf` in `Papers/MANIFEST.md`; 40 pages extracted, 88,420 chars | **YES** — `NOVELTY.md` §2.3, §3.1; and it is the row-25/row-29 depth correction |
| 37 | Lucas & Kerswell, *Recurrent flow analysis in spatiotemporally chaotic 2-dimensional Kolmogorov flow*, **Phys. Fluids 27 045106 (2015)**, `10.1063/1.4917279` — **v1, THE VERSION QUOTED**, `Papers/1406.1820v1.pdf` | Gate effects (a) AND (b) in a single sentence at p.5: skew toward low periods, and ~2/3 of short-period guesses skipped BECAUSE they were known repeats of ref [6] = Chandler & Kerswell 2013 (bibliography verified at p.21, not inferred). | **FULL TEXT** — sha256 `edf2f7e9…6cbad76` in `Papers/MANIFEST.md`; 24 pages extracted, 64,150 chars | **YES** — `NOVELTY.md` §2.2, §3.2 |
| 38 | Lucas & Kerswell (2015) — **v2**, `Papers/1406.1820.pdf` | Cross-check ONLY. **v2 carries a DOUBLED TEXT LAYER and is not safely quotable** (FINDINGS F7). The single load-bearing sentence was re-checked in the v2 extraction and is present in both, so the finding is an artefact of the version, not of the claim. | **FULL TEXT** — sha256 `da9cab5c…f479258` in `Papers/MANIFEST.md`; 28 pages extracted, 123,054 chars | no — it exists to prove the v1/v2 hazard was measured, not assumed |
| 39 | Lucas & Kerswell, *Spatiotemporal dynamics in 2D Kolmogorov flow over large domains*, `Papers/1308.3356.pdf` | Read in full as part of the recurrence-mining corpus. Did not supply a graded quote for either gate effect. | **FULL TEXT** — sha256 `f39f1333…00e541c` in `Papers/MANIFEST.md`; 37 pages extracted, 84,682 chars | no |
| 40 | Viswanath, *Recurrent motions within plane Couette turbulence* (2007) — the founding locally-constrained-optimal hookstep paper, `Papers/physics_0604062.pdf` | Read in full. Supplies the method whose admission filter both gate effects are about; did not itself supply a graded quote. | **FULL TEXT** — sha256 `fe9fe1aa…d5dc5d6` in `Papers/MANIFEST.md`; 23 pages extracted, 59,825 chars | no — but it is the paper `PROG-R4`'s solver descends from |
| 41 | Page, Holey, Brenner & Kerswell, *Exact coherent structures in two-dimensional turbulence identified with convolutional autoencoders*, **JFM 991 (2024) A10**, `10.1017/jfm.2024.552`, `Papers/2309.12754.pdf` | **THE STRONGEST STATEMENT OF GATE EFFECT (a), at `S3`.** pp.2, 16, 18 — the recovered orbit set is skewed low in dissipation, the skew is attributed to the recurrence criterion, and the more unstable structures are `not flagged in this approach at all`. | **FULL TEXT** — sha256 `5e47a4bd…200b612` in `Papers/MANIFEST.md`; 28 pages extracted, 81,541 chars | **YES — this is the paper that kills `P1`'s effect (a)** |
| 42 | Kawahara, Uhlmann & van Veen, *The significance of simple invariant solutions in turbulent flows*, **Annu. Rev. Fluid Mech. 44:203–225 (2012)**, `Papers/1108.0975.pdf` | Read in full. **DECLARED `UNREACHABLE` IN ADVANCE BY THIS LEG AND THAT DECLARATION WAS WRONG** — it is on arXiv with its `journal_ref` attached (FINDINGS F6). Wrong in the safe direction; recorded rather than quietly corrected. | **FULL TEXT** — sha256 `9e4d666e…47be2a9` in `Papers/MANIFEST.md`; 32 pages extracted, 76,109 chars | no — but the failed ceiling is itself a correction |
| 43 | Lucas & Kerswell (2017), sustaining processes in 2D Kolmogorov flow, `Papers/1611.04829.pdf` | Read in full. Contributes an `S0 ADJACENT` co-hit only. | **FULL TEXT** — sha256 `2ef11677…bbda198` in `Papers/MANIFEST.md`; 11 pages extracted, 41,678 chars | no |
| 44 | Halcrow, Gibson & Cvitanović — UPOs in plane Couette flow, `Papers/0810.1974.pdf` | Read in full: the Cvitanović line, which the gate named explicitly. | **FULL TEXT** — sha256 `065f947a…e3b55a5` in `Papers/MANIFEST.md`; 3 pages extracted, 3,191 chars | no graded quote — and that is a real result: the gate's own named line did not supply the strongest statement, the 2024 JFM paper did |
| 45 | Cvitanović line — RPOs, `Papers/1705.03720.pdf` | Read in full: the Cvitanović line, as the gate named it. | **FULL TEXT** — sha256 `85a5b22f…b08772c` in `Papers/MANIFEST.md`; 26 pages extracted, 79,486 chars | no graded quote |
| 46 | Redfern, Lazer & Lucas, nonlinear-triad recurrence function (2024) — **PREPRINT; the served arXiv metadata carries NO `journal_ref` and this leg DID NOT VERIFY publication status**, `Papers/2408.05079.pdf` | Gate effect (a) as the paper's ENTIRE PREMISE (`S3`, discounted one notch for preprint status): the standard recurrence function's choice of norm decides which orbits are recoverable. p.13 supplies the head-to-head number against the standard `L2` recurrence function's **58 unique recurrent flows** at identical parameters. | **FULL TEXT** — sha256 `8ed5ec9a…8ab459e` in `Papers/MANIFEST.md`; 26 pages extracted, 48,502 chars | **YES** — `NOVELTY.md` §2.4, §3.3, **and it is cited as a preprint everywhere it appears** |
| 47 | Page & Kerswell, **JFM 886 (2020) A28** (`journal_ref` read off the served feed, not assumed), `Papers/1906.01310.pdf` | **GRADED `S0 ADJACENT` AND DELIBERATELY NOT COUNTED AS A `YES`.** p.2's `main downside` sentence is about the *requirement* of shadowing, not about *which* orbits the requirement selects. §0.5's rule was written before the corpus was read precisely so this near-miss could not be quietly promoted. | **FULL TEXT** — sha256 `b1349254…7652a51` in `Papers/MANIFEST.md`; 21 pages extracted, 53,737 chars | no — and the refusal to promote it is the load-bearing part |
| 48 | Page, Brenner & Kerswell, **Phys. Rev. Fluids 6 034402 (2021)** (`journal_ref` read off the served feed), `Papers/2008.07515.pdf` | Read in full as part of the autoencoder/latent-space thread. No graded quote. | **FULL TEXT** — sha256 `cf43ee1e…2d43ec6` in `Papers/MANIFEST.md`; 13 pages extracted, 43,954 chars | no |
