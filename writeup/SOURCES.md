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
| 26 | Canuto, Hussaini, Quarteroni & Zang, *Spectral Methods: Evolution to Complex Geometries and Applications to Fluid Dynamics*, **Springer (2007)**, `doi:10.1007/978-3-540-30728-0`, **Appendix D.3** | the textbook IMEX / low-storage Runge–Kutta–Crank–Nicolson splitting — the published home of the **higher-order stepper `R4-a` would put in place of `U3`'s Lie–Trotter split** | **SECOND HAND.** Located as the citation `jax_cfd`'s `low_storage_runge_kutta_crank_nicolson` gives for itself; the **book is not held here**. The *executable* form — `jax_cfd.spectral.time_stepping`'s IMEX schemes — **is** available and inspectable, and for an implementation question that is the load-bearing artefact. | Conductor, 2026-08-19 | **partially, for `R4-a`** |

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
| **R4** | second-order (Strang) stepper replacing `U3`'s Lie–Trotter | **PARTIALLY NAMED 2026-08-19 (row 26).** Strang splitting itself is Strang, *SIAM J. Numer. Anal.* **5(3):506–517 (1968)** — cited, not read. The nearer reference is **Canuto *et al.* App. D.3**, held here only **SECOND HAND**, but with an **executable** counterpart in `jax_cfd.spectral.time_stepping`. **Still owed before a line is written:** which scheme, at what order, and whether it is a Strang split at all or an IMEX Runge–Kutta — `U3`'s stepper is an *exact integrating factor applied after RK4*, which is a Lie–Trotter split, so "second-order Strang" is a **hypothesis about the fix, not yet a specification**. |
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
