# Writeup index — one line per leg/route

Machine-checkable companion to [README.md](README.md) (which carries the narrative). This
file exists so a new agent or session can find *every* leg's quartet (runner, curated data,
BLOG+TECHNICAL+evidence.py, registered figure — [ORCHESTRATION.md §4](../ORCHESTRATION.md))
without reading the whole tree. **Quartet gaps are marked `GAP` and explained inline** — a
route missing any piece is incomplete, including negative results (lesson 76).

Maintained by DOCS. Do not add or edit numeric claims here — links and one-line labels only.

## Arc 1 — `1_gclm_1d/` (1D gCLM pipeline, Level 0/1, pre-quartet convention)

| Route | Gate / headline | Docs | Data / figure |
|---|---|---|---|
| gCLM 1D GA search | Evolutionary search finds a candidate profile; validated as a *map*, not a proof | [SUMMARY](1_gclm_1d/SUMMARY.md) · [TECHNICAL](1_gclm_1d/TECHNICAL_WRITEUP.md) · [BLOG](1_gclm_1d/BLOG.md) | figs 1–5 via [build_figures.py](build_figures.py); no BLOG/TECHNICAL split, no `*_evidence.py` (predates the convention) |

## Arc 2 — `2_phase1_2d/` (Route-A Phase-1 2D Boussinesq fitness search, pre-quartet convention)

| Route | Gate / headline | Docs | Data / figure |
|---|---|---|---|
| Phase 1 de-risking | Two experiments before the search: grid resolution + rough-genome rails | [BLOG_PHASE1](2_phase1_2d/BLOG_PHASE1.md) | fig 6 via [build_figures.py](build_figures.py) |
| Phase 1 gate 4 | The ν_crit gate that passed — and shouldn't have | [BLOG_PHASE1_GATE4](2_phase1_2d/BLOG_PHASE1_GATE4.md) | `data/phase1_gate4.json` |
| Phase 1 gate 4 reform | The gate rebuilt to fail correctly | [BLOG_PHASE1_GATE4_REFORM](2_phase1_2d/BLOG_PHASE1_GATE4_REFORM.md) | `data/phase1_gate4_reform.json` |
| Phase 1 g-sustained | Two currencies, one wall (inviscid) | [BLOG_PHASE1_GSUSTAINED](2_phase1_2d/BLOG_PHASE1_GSUSTAINED.md) | `data/phase1_gsustained.json` |
| Two currencies (negative result) | Uniform grid cannot resolve self-similar blow-up — closed the Phase-1 lane | [NEGATIVE_RESULT_TWO_CURRENCIES](2_phase1_2d/NEGATIVE_RESULT_TWO_CURRENCIES.md) | fig 7 via [build_figures.py](build_figures.py) |

GAP (legacy, not urgent): none of arc 2 has a paired TECHNICAL_*.md or `*_evidence.py`; evidence
is rebuilt via the shared [curate_evidence.py](curate_evidence.py) instead. Predates the
quartet contract, which §4 names `4_p2_lottery/` as the banked convention going forward.

## Arc 3 — `3_spikes/` (numerics upgrade, dynamic rescaling, Spikes 0/1)

| Route | Gate / headline | Docs | Data / figure |
|---|---|---|---|
| Phase 2 rescaling | From a uniform-grid wall to a dynamic-rescaling solver | [TECHNICAL](3_spikes/TECHNICAL_PHASE2_RESCALING.md) · [BLOG](3_spikes/BLOG_PHASE2_RESCALING.md) | fig 8 |
| Spike 0 | Dynamic-rescaling solver validated against a closed-form (CLM) answer — held | [TECHNICAL](3_spikes/TECHNICAL_SPIKE0_RESCALING.md) · [BLOG](3_spikes/BLOG_SPIKE0_RESCALING.md) · [evidence](3_spikes/spike0_rescaling_evidence.py) | `data/spike0_rescaling.json` → fig 8 |
| Spike 1 Step A | 2D Boussinesq velocity operator on a stretched grid, known-answer validated | [TECHNICAL (VELOCITY)](3_spikes/TECHNICAL_SPIKE1_VELOCITY.md) · [BLOG](3_spikes/BLOG_SPIKE1_STEPA.md) · [evidence](3_spikes/spike1_stepA_evidence.py) | `data/spike1_stepA_velocity.json` → fig 9 |
| Spike 1 Step B | Rescaled 2D Boussinesq formulation; letting the data pick unknowns | [TECHNICAL](3_spikes/TECHNICAL_SPIKE1_STEPB.md) · [BLOG](3_spikes/BLOG_SPIKE1_STEPB.md) · [evidence](3_spikes/spike1_stepB_evidence.py) | `data/spike1_stepB_rescaled.json` → fig 10 |
| Spike 1 Step C | Relax to the Chen–Hou profile: the gate — partial, honestly reported | [TECHNICAL](3_spikes/TECHNICAL_SPIKE1_STEPC.md) · [BLOG](3_spikes/BLOG_SPIKE1_STEPC.md) · [evidence](3_spikes/spike1_stepC_evidence.py) | `data/spike1_stepC_gate.json` → fig 11 |

## Arc 4 — `4_p2_lottery/` (P2, the 1D Hou–Luo lottery-ticket legs; current quartet convention)

Legend: R = runner in `experiments/` (or `evidence.py --generate` where noted), D = curated
data JSON, B/T = BLOG/TECHNICAL pair, E = `*_evidence.py`, F = figure present in
`writeup/figures/`.

| Route | Gate / headline | R | D | B/T | E | F | Docs |
|---|---|---|---|---|---|---|---|
| HL anchor | 1D Hou–Luo profile machine, validated against exact solution | gen* | Y | Y | Y | fig12 | [T](4_p2_lottery/TECHNICAL_P2_HL_ANCHOR.md) · [B](4_p2_lottery/BLOG_P2_HL_ANCHOR.md) |
| Conj 2.4 | Dynamic-relaxation leg, Conjecture 2.4 at POC fidelity | Y | Y | Y | Y | fig13 | [T](4_p2_lottery/TECHNICAL_P2_CONJ24.md) · [B](4_p2_lottery/BLOG_P2_CONJ24.md) |
| Regular profile / Scenario 2 (B1) | CHL Scenario 2 modified rescaling (4.1)/(4.2), reproduced | gen* | Y | Y | Y | fig14/15 | [T](4_p2_lottery/TECHNICAL_P2_SCENARIO2.md) · [B](4_p2_lottery/BLOG_P2_SCENARIO2.md) |
| GA framework | Genetic-algorithm global search + a=0 known-answer gate | gen* | Y | Y | Y | fig16 | [T](4_p2_lottery/TECHNICAL_P2_GA_FRAMEWORK.md) · [B](4_p2_lottery/BLOG_P2_GA_FRAMEWORK.md) |
| Two-scale sweep | HQW25's exact two-scale traveling wave under gCLM advection | Y | Y | Y | Y | fig17 | [T](4_p2_lottery/TECHNICAL_P2_TWO_SCALE.md) · [B](4_p2_lottery/BLOG_P2_TWO_SCALE.md) |
| Two-scale kladder | gCLM two-scale survival boundary: genuine (a*≈0.5–0.55) or genome-limited? Genuine | Y | Y | Y | Y | fig18 | [T](4_p2_lottery/TECHNICAL_P2_KLADDER.md) · [B](4_p2_lottery/BLOG_P2_KLADDER.md) |
| Route-D v1 | Rigorous interval-arithmetic core, a=0 NK framing | Y | Y | Y | Y | fig19 | [T](4_p2_lottery/TECHNICAL_P2_ROUTED.md) · [B](4_p2_lottery/BLOG_P2_ROUTED.md) |
| Route-D v2 (dress) | Float dress rehearsal: naive NK does not close | Y | Y | Y | Y | fig20 | [T](4_p2_lottery/TECHNICAL_P2_ROUTED_DRESS.md) · [B](4_p2_lottery/BLOG_P2_ROUTED_DRESS.md) |
| Route-D v3 (spaces) | Which space pair can carry the certificate | Y | Y | Y | Y | fig21 | [T](4_p2_lottery/TECHNICAL_P2_ROUTED_SPACES.md) · [B](4_p2_lottery/BLOG_P2_ROUTED_SPACES.md) |
| Route-D v4 | Full operator in the decay-graded pair | Y | Y | Y | Y | fig22 | [T](4_p2_lottery/TECHNICAL_P2_ROUTED_V4.md) · [B](4_p2_lottery/BLOG_P2_ROUTED_V4.md) |
| Route-D v5 | The two-grading space | Y | Y | Y | Y | fig23 | [T](4_p2_lottery/TECHNICAL_P2_ROUTED_V5.md) · [B](4_p2_lottery/BLOG_P2_ROUTED_V5.md) |
| Route-D v6 | First genuine upper bounds; the discrete-ball trap | Y | Y | Y | Y | fig24 | [T](4_p2_lottery/TECHNICAL_P2_ROUTED_V6.md) · [B](4_p2_lottery/BLOG_P2_ROUTED_V6.md) |
| Route-D v7 | Domain seminorm part of ‖A‖, closed by a derivative gain | Y | Y | Y | Y | fig25 | [T](4_p2_lottery/TECHNICAL_P2_ROUTED_V7.md) · [B](4_p2_lottery/BLOG_P2_ROUTED_V7.md) |
| Route-D v8 | Codomain seminorm part of C_Q; first complete Z₂ | Y | Y | Y | Y | fig26 | [T](4_p2_lottery/TECHNICAL_P2_ROUTED_V8.md) · [B](4_p2_lottery/BLOG_P2_ROUTED_V8.md) |
| Route-D v9 (sharpen) | 32% better \|H(h)\| bound that buys nothing where it matters | Y | Y | Y | Y | fig27 | [T](4_p2_lottery/TECHNICAL_P2_ROUTED_V9.md) · [B](4_p2_lottery/BLOG_P2_ROUTED_V9.md) |
| Route-D v10 | Lower bound on ‖A‖; first measured ceiling on sharpening | Y | Y | Y | Y | fig28 | [T](4_p2_lottery/TECHNICAL_P2_ROUTED_V10.md) · [B](4_p2_lottery/BLOG_P2_ROUTED_V10.md) |
| Route-D v11 | Newton on the profile: the 1e-2 floor was the search | Y | Y | Y | Y | fig29 | [T](4_p2_lottery/TECHNICAL_P2_ROUTED_V11.md) · [B](4_p2_lottery/BLOG_P2_ROUTED_V11.md) |
| Route-D v12 | The profile ends: Y₀ in the bounds' own basis | Y | Y | Y | Y | fig30 | [T](4_p2_lottery/TECHNICAL_P2_ROUTED_V12.md) · [B](4_p2_lottery/BLOG_P2_ROUTED_V12.md) |
| Route-D v13 | The turning point: correcting v12, locating the wall | Y | Y | Y | Y | fig31 | [T](4_p2_lottery/TECHNICAL_P2_ROUTED_V13.md) · [B](4_p2_lottery/BLOG_P2_ROUTED_V13.md) |
| Route-D v14 | Two-scale profile equation has a first integral | Y | Y | Y | Y | fig32 | [T](4_p2_lottery/TECHNICAL_P2_ROUTED_V14.md) · [B](4_p2_lottery/BLOG_P2_ROUTED_V14.md) |
| Route-D scope (advection) | Advection scope of the Route-D bound programme: velocity log-divergent | n/a | n/a | Y | n/a | none | [T](4_p2_lottery/TECHNICAL_P2_ADVECTION_SCOPE.md) · [B](4_p2_lottery/BLOG_P2_ADVECTION_SCOPE.md) — **explicitly no figure/JSON by design**: "every number is reproduced by running the gates" (see file header) |
| Route-D v15 (literature scope) | Literature check narrows the lane | n/a | Y | Y | n/a | none | [T](4_p2_lottery/TECHNICAL_P2_LITERATURE_SCOPE.md) · [B](4_p2_lottery/BLOG_P2_LITERATURE_SCOPE.md) — **explicitly no figure by design**: "no measurement" (see file header) |
| Route-D v16 | Float rehearsal: what the reduced space fixed, and what it did not | Y | Y | Y | Y | fig33 | [T](4_p2_lottery/TECHNICAL_P2_ROUTED_V16.md) · [B](4_p2_lottery/BLOG_P2_ROUTED_V16.md) |
| Route-E v1 | Rescaled gCLM flow has no eigenvalue for a Hopf bifurcation | Y | Y | Y | Y | fig34 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEE_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEE_V1.md) |
| Route-F v1 | Critical dissipation exponent = half the far-field decay exponent | Y | Y | Y | Y | fig35 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEF_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEF_V1.md) |
| Route-G v1 | Critical dissipation exponent on the 2D object: s_c = 1/(2β) | Y | Y | Y | Y | fig36 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEG_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEG_V1.md) |
| Route-H v1 | The marginal case: every scaling argument returns zero information | Y | Y | Y | Y | fig37 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEH_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEH_V1.md) |
| Route-I v1 | The marginal flow, driven | Y | Y | Y | Y | fig38 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEI_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEI_V1.md) |
| Route-J v1 | The primary-source literature pass | Y | Y | Y | Y | fig39 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEJ_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEJ_V1.md) |
| Route-K v1 | The L1→L2 certification port, step one | Y | Y | Y | Y | fig40 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEK_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEK_V1.md) |
| Route-L v1 | 2D preconditioner: the stall attributed, and removed | Y | Y | Y | Y | fig41 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEL_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEL_V1.md) |
| Route-M v1 | Target selection: certify *what*, that isn't already done? | Y | Y | Y | Y | fig42 (**was missing, regenerated this session — see gap list**) | [T](4_p2_lottery/TECHNICAL_P2_ROUTEM_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEM_V1.md) |
| Route-PORT v1 | Bordered system; a certificate that closes around the wrong (truncated) object | Y | Y | Y | **GAP: none** | **GAP: none** | [T](4_p2_lottery/TECHNICAL_P2_ROUTEPORT_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEPORT_V1.md) — see gap list below |
| Route-V v0 | Novelty gate: dissipation certification pre-empted by Dähne–Figueras (2024), re-derived | Y | Y | Y | Y | fig43 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEV_V0.md) · [B](4_p2_lottery/BLOG_P2_ROUTEV_V0.md) |
| Route-C-PILOT v0 | Certificate-weight fitness on a known-answer object — gate answered **NO** (4/6); GA not run | Y | Y | Y | Y | fig44 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEC_PILOT_V0.md) · [B](4_p2_lottery/BLOG_P2_ROUTEC_PILOT_V0.md) |
| Route-L1 v1 | Certificate stops being a rehearsal: constants become interval bounds | Y | Y | Y | Y | fig45 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEL1_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEL1_V1.md) |
| Route-L1 v2 | Certificate rebuilt where operators are exact; one term left over (weight class) | Y | Y | Y | Y | fig46 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEL1_V2.md) · [B](4_p2_lottery/BLOG_P2_ROUTEL1_V2.md) |
| Route-PORT v2 | Reach makes the truncation gap WORSE (+0.47 dec/unit ρ) — tail lemma forced | Y | Y | **GAP: T only, no BLOG** | **GAP: none** | **GAP: none** | [T](4_p2_lottery/TECHNICAL_P2_ROUTEPORT_V2.md) — see gap list below |
| Route-T v1 | Bordering restores a bounded tail; works where the failure curve was worst | Y | Y | Y | Y | fig47 | [T](4_p2_lottery/TECHNICAL_P2_ROUTET_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTET_V1.md) |
| Route-TC v1 | Assembling the bordered certificate: four terms in one polynomial; the term that ran out is Z₁'s block coupling | Y | Y | Y | Y | fig48 | [T](4_p2_lottery/TECHNICAL_P2_ROUTETC_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTETC_V1.md) |
| Route-MM v1 | The shape of the approximate inverse, spent — gate answered **NO** | Y | Y | Y | Y† | fig49 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEMM_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEMM_V1.md) |
| Route-NB v1 | Compactified-basis coefficient decay of `HL_S2_nonsymmetric`: is the target in the space? | Y | Y | Y | Y† | fig50 | [T](4_p2_lottery/TECHNICAL_P2_ROUTENB_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTENB_V1.md) |
| Route-TN v1 | The `(H, D)` consistency defect of `L1` step one, enclosed — gate answered **NO** | Y | Y | Y | Y† | fig51 | [T](4_p2_lottery/TECHNICAL_P2_ROUTETN_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTETN_V1.md) |
| Route-XS v1 | The shape dichotomy against published certificates — gate answered **NO** | Y | Y | Y | Y† | fig52 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEXS_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEXS_V1.md) |

`gen*` = the runner is the `*_evidence.py` script itself (`--generate` recomputes from
`solver/`), rather than a separate `experiments/*.py` file — legacy legs (HL anchor, GA
framework, Scenario 2/regular-profile) that predate the `experiments/` split later routes
use. Substance of quartet item 1 (a runner that produced the numbers) is present; form
differs from the current convention.

`Y†` = the `*_evidence.py` exists but lives in `experiments/` rather than beside its docs in
`4_p2_lottery/` (4 files: MM, NB, TN, XS). Placement drift from the earlier Arc-4 routes, not
a missing piece — see gap-list item 7.

**Index currency.** Arc 4's table above is current through **leg 57 (Route-XS)**. Legs 53
(TC), 54 (MM), 55 (NB), 56 (TN) and 57 (XS) were verified piece-by-piece against the files
on disk when their rows were added — 25 of 25 quartet pieces present, none missing, none
zero-byte; the full per-file inventory is in [novelty/leg_68.md](novelty/leg_68.md).

## Quartet gaps found (plain list)

1. **Route-PORT v1** (`writeup/4_p2_lottery/TECHNICAL_P2_ROUTEPORT_V1.md`) — has a runner
   (`experiments/p2_route_port_v1_bordered.py`) and curated data
   (`writeup/data/p2_route_port_v1_bordered.json`), and both BLOG and TECHNICAL exist, but
   there is **no `*_evidence.py` and no registered figure anywhere** — neither file
   references a `figN` and no `writeup/figures/*port_v1*` exists. This is the leg that
   found the certificate closes around the *wrong* (truncated) object at 1.55e+08× the ball
   radius — a load-bearing negative finding that currently has no rebuildable figure. Not
   fixed here: writing an `evidence.py` and choosing what to plot is a claim-bearing
   decision about how to represent the numbers, out of DOCS's mechanical-only remit.
2. **Route-PORT v2** (`writeup/4_p2_lottery/TECHNICAL_P2_ROUTEPORT_V2.md`) — has runner
   (`experiments/p2_route_port_v2_reach.py`) and curated data
   (`writeup/data/p2_route_port_v2_reach.json`), but is missing all of: `BLOG_P2_ROUTEPORT_V2.md`,
   a `p2_route_port_v2_evidence.py`, and a registered figure. This is a negative-leaning
   result (truncation gap gets worse with reach) and per lesson 76 deserves the same care as
   a positive one. Not fixed here — writing the BLOG/TECHNICAL prose and picking what the
   figure should show is a claim-bearing decision, out of DOCS's mechanical-only remit.
3. **fig42 (Route-M v1)** — `p2_route_m_v1_evidence.py` references
   `writeup/figures/fig42_route_m_v1_targets.png`, which was absent from the repo (all other
   `fig1..fig47` present, fig42 was the one gap). **Fixed this session**: ran
   `python writeup/4_p2_lottery/p2_route_m_v1_evidence.py`, which rebuilds the figure from the
   already-curated `writeup/data/p2_route_m_v1_targets.json` with no re-run of any solver —
   purely mechanical, no numeric content touched. The regenerated PNG is committed.
4. **`writeup/README.md`'s numbered index is stale**: it stops at entry #47 (Route-PORT v2)
   and is missing entries entirely for **Route-M v1, Route-V v0, Route-C-PILOT v0, Route-L1
   v1, Route-L1 v2, and Route-T v1** (also skips list-number `45`). Not edited here: every
   entry in that list is a numeric-prose paragraph (exact figures, gate values), and this
   agent's remit is links/index scaffolding, not writing new numeric summaries. Flagged for
   whoever owns that prose next; this `INDEX.md` covers the gap in the meantime.
5. **Arc 1 (`1_gclm_1d/`) and Arc 2 (`2_phase1_2d/`)** predate the quartet convention: no
   `TECHNICAL_*`/`BLOG_*` pairing in arc 1, no paired TECHNICAL docs or `*_evidence.py` in
   arc 2 (evidence is rebuilt via the shared `curate_evidence.py`). Not a live gap to close —
   §4 explicitly names `4_p2_lottery/` as "the banked convention" going forward — but noted
   for completeness since the task asked every route be checked.
6. **Route-D "advection scope" and "literature scope" (v15)** have no data JSON/figure by
   explicit design (stated in their own file headers: no measurement was produced). Not a
   gap — the negative construction ("no number here") is itself the honest artifact.
7. **Evidence-script placement drift, legs 54–57** — `p2_route_mm_v1_shape_evidence.py`,
   `p2_route_nb_v1_targetnorm_evidence.py`, `p2_route_tn_v1_consistency_evidence.py` and
   `p2_route_xs_v1_shapes_evidence.py` all sit in `experiments/`, whereas every Arc-4 route
   before them (including leg 53's `p2_route_tc_v1_evidence.py`) keeps its evidence script in
   `writeup/4_p2_lottery/`. 4 files, all present and all runnable; nothing is missing, so
   these are `Y†` in the table rather than `GAP`. Not moved here: relocating a script rewrites
   the paths its own TECHNICAL file quotes, which is outside a links-and-labels remit.
8. **`fig48` is assigned twice** — both `writeup/figures/fig48_route_tc_v1_assemble.png`
   (leg 53, referenced by `TECHNICAL_P2_ROUTETC_V1.md`) and
   `writeup/figures/fig48_weight_repairs_v1.png` exist. 1 duplicated figure number. Leg 53's
   F slot is genuinely filled; renumbering the other is a registry decision, not an index one.

Route-TC is no longer in progress: it landed as leg 53 and has a complete quartet, indexed in
the Arc 4 table above.
