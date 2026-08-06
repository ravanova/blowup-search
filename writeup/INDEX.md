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
| Two-scale sweep | HQW25's exact a=0 two-scale traveling wave continued into gCLM advection at a>0 | Y | Y | Y | Y | fig17 | [T](4_p2_lottery/TECHNICAL_P2_TWO_SCALE.md) · [B](4_p2_lottery/BLOG_P2_TWO_SCALE.md) |
| Two-scale kladder | survival boundary of the a>0 two-scale traveling wave: genuine (a*≈0.5–0.55, measured on a>0) or genome-limited? Genuine | Y | Y | Y | Y | fig18 | [T](4_p2_lottery/TECHNICAL_P2_KLADDER.md) · [B](4_p2_lottery/BLOG_P2_KLADDER.md) |
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
| Route-PORT v1 | Bordered system; a certificate that closes around the wrong (truncated) object | Y | Y | Y | Y† | fig59 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEPORT_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEPORT_V1.md) — **quartet completed by leg 60**, gap-list item 1 now closed |
| Route-V v0 | Novelty gate: dissipation certification pre-empted by Dähne–Figueras (2024), re-derived | Y | Y | Y | Y | fig43 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEV_V0.md) · [B](4_p2_lottery/BLOG_P2_ROUTEV_V0.md) |
| Route-C-PILOT v0 | Certificate-weight fitness on a known-answer object — gate answered **NO** (4/6); GA not run | Y | Y | Y | Y | fig44 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEC_PILOT_V0.md) · [B](4_p2_lottery/BLOG_P2_ROUTEC_PILOT_V0.md) |
| Route-L1 v1 | Certificate stops being a rehearsal: constants become interval bounds | Y | Y | Y | Y | fig45 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEL1_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEL1_V1.md) |
| Route-L1 v2 | Certificate rebuilt where operators are exact; one term left over (weight class) | Y | Y | Y | Y | fig46 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEL1_V2.md) · [B](4_p2_lottery/BLOG_P2_ROUTEL1_V2.md) |
| Route-PORT v2 | Reach makes the truncation gap WORSE (+0.47 dec/unit ρ) — tail lemma forced | Y | Y | **GAP: T only, no BLOG** | Y† | fig60 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEPORT_V2.md) — E and F **added by leg 60**; only the BLOG is still owed, see gap list item 2 |
| Route-T v1 | Bordering restores a bounded tail; works where the failure curve was worst | Y | Y | Y | Y | fig47 | [T](4_p2_lottery/TECHNICAL_P2_ROUTET_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTET_V1.md) |
| Route-TC v1 | Assembling the bordered certificate: four terms in one polynomial; the term that ran out is Z₁'s block coupling | Y | Y | Y | Y | fig48 | [T](4_p2_lottery/TECHNICAL_P2_ROUTETC_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTETC_V1.md) |
| Route-MM v1 | The shape of the approximate inverse, spent — gate answered **NO** | Y | Y | Y | Y† | fig49 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEMM_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEMM_V1.md) |
| Route-NB v1 | Compactified-basis coefficient decay of `HL_S2_nonsymmetric`: is the target in the space? | Y | Y | Y | Y† | fig50 | [T](4_p2_lottery/TECHNICAL_P2_ROUTENB_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTENB_V1.md) |
| Route-TN v1 | The `(H, D)` consistency defect of `L1` step one, enclosed — gate answered **NO** | Y | Y | Y | Y† | fig51 | [T](4_p2_lottery/TECHNICAL_P2_ROUTETN_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTETN_V1.md) |
| Route-XS v1 | The shape dichotomy against published certificates — gate answered **NO** | Y | Y | Y | Y† | fig52 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEXS_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEXS_V1.md) |
| Weight-repairs v1 | Named P2/P3 repairs to the certificate-weight fitness; six-property gate still FAILs | Y | Y | Y | Y | fig48 (**duplicated number** — see gap list item 8) | [T](4_p2_lottery/TECHNICAL_P2_WEIGHT_REPAIRS_V1.md) · [B](4_p2_lottery/BLOG_P2_WEIGHT_REPAIRS_V1.md) — row added by leg 108; its `E` mark **corrected by leg 138**, see gap list item 9 |
| Weight-repairs v2 (leg 59) | The conditioning wall modelled in both weight factors; frozen six-property gate re-run still FAILs | Y | Y | Y | Y† | fig58 | [T](4_p2_lottery/TECHNICAL_P2_WEIGHT_REPAIRS_V2.md) · [B](4_p2_lottery/BLOG_P2_WEIGHT_REPAIRS_V2.md) |
| Route-KA v1 (leg 61) | The interval pipeline reproduces CLN's published Kawahara radius end to end | Y | Y | **GAP: T only, no BLOG** | **GAP: none** | **GAP: none** | [T](4_p2_lottery/TECHNICAL_P2_ROUTEKA_V1.md) — see gap list item 10 |
| Route-NG v1 (leg 58) | Stage `NG`: the no-go stated as a theorem on the class `A21 = 0` — gate answered **YES**; publication scoping **escalated and parked**, the route itself merged | Y | Y | Y | Y† | fig55 | [T](4_p2_lottery/TECHNICAL_P2_ROUTENG_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTENG_V1.md) — added by leg 138 |
| Route-CP v1 (leg 62) | Cadiot arXiv:2505.03091's scope settled from the full text — gate answered **NO** | Y | Y | Y | Y† | fig56 | [T](4_p2_lottery/TECHNICAL_P2_ROUTECP_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTECP_V1.md) — added by leg 138 |
| Route-BX v1 (leg 126) | Stage `B` answered from the banked record, the closure audit — gate answered **NO** | Y | Y | Y | Y† | none | [T](4_p2_lottery/TECHNICAL_P2_ROUTEBX_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEBX_V1.md) — **explicitly no figure by design**: the yes-branch would have registered `fig62`, the no-branch measures nothing (see file header). Added by leg 138 |
| Route-M2P v1 (leg 125) | Chen's γ=2 dissipative gCLM candidate: full text, constants, first `Y₀` — gate answered **NO** on both clauses | Y | Y | Y | **GAP: none** | fig61 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEM2P_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEM2P_V1.md) — added by leg 156; the missing `*_evidence.py` is gap list item 13 |
| Route-NGX v1 (leg 127) | The general class `A₂₁ ≠ 0`, decided: `Z₁ ≥ 1` for every bounded `A` — gate answered **YES (i)** | Y | Y | Y | Y† | fig63 | [T](4_p2_lottery/TECHNICAL_P2_ROUTENGX_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTENGX_V1.md) — added by leg 156 |
| Route-NKR v1 (leg 128) | One guard for three pipelines: the `Y₀`/`Z₀`/`Z₁` fabrication-acceptance gap, closed as a class — gate answered **YES on (b) and (c), NO on (a)** | Y | Y | Y | **GAP: none** | none | [T](4_p2_lottery/TECHNICAL_P2_ROUTENKR_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTENKR_V1.md) — **explicitly no figure by design**: "a repair leg with no curve to plot" (see file header). Added by leg 156; the missing `*_evidence.py` is gap list item 13 |
| Route-M2 v1 (leg 63) — **PARKED, NOT LANDED** | Target reselection under the multiplier/shift screen — gate answered **YES**, and that answer is **escalation #1**: parked on branch `leg/m2-v1`, never merged | — | — | — | — | `fig57` **reserved** | **No files on `main`.** Read the branch with `git show`; do not merge or build on it. Territory and finding: [DIRECTION.md](../DIRECTION.md) §63. Row added by leg 138 |

`gen*` = the runner is the `*_evidence.py` script itself (`--generate` recomputes from
`solver/`), rather than a separate `experiments/*.py` file — legacy legs (HL anchor, GA
framework, Scenario 2/regular-profile) that predate the `experiments/` split later routes
use. Substance of quartet item 1 (a runner that produced the numbers) is present; form
differs from the current convention.

`Y†` = the `*_evidence.py` exists but lives in `experiments/` rather than beside its docs in
`4_p2_lottery/` (10 files: MM, NB, TN, XS, and — added by leg 138 — PORT v1, PORT v2, NG, CP,
BX, and — added by leg 156 — NGX). Placement drift from the earlier Arc-4 routes, not a
missing piece — see gap-list item 7.
Every Arc-4 route landed since leg 57 follows the `experiments/` placement, so `Y†` is now the
majority convention among recent routes rather than a drift from it.

**Index currency.** Arc 4's table above is current through **leg 57 (Route-XS)**. Legs 53
(TC), 54 (MM), 55 (NB), 56 (TN) and 57 (XS) were verified piece-by-piece against the files
on disk when their rows were added — 25 of 25 quartet pieces present, none missing, none
zero-byte; the full per-file inventory is in [novelty/leg_68.md](novelty/leg_68.md).

**Index currency — second pass (leg 108, Route-IX2).** The paragraph above is superseded as a
statement of currency, not corrected: it remains a true record of what leg 68 verified. Since
leg 68's pass, **30 legs** have landed on `main` (58, 59, 61, 64–67, 69, 70, 72–74, 77–82, 84,
86–94, 97, 102) and this file received **0 edits** across all of them. Leg 108 audited every one
against the files on disk; the full per-leg inventory is in
[novelty/leg_108.md](novelty/leg_108.md). The result splits cleanly in two:

- **3 routes were owed a table row and now have one** (appended above): Weight-repairs v1 (no
  leg number — predates the `Leg N:` commit convention), Weight-repairs v2 (leg 59), and
  Route-KA v1 (leg 61). These are the only routes in the window that produced a
  BLOG/TECHNICAL document under `4_p2_lottery/`.
- **28 of the 30 legs produced no BLOG/TECHNICAL and no figure, by design.** They are
  audit, adversarial-robustness, literature-watch, known-answer-check and hygiene legs running
  under the "no measurement, no figure" convention that Route-D advection-scope and Route-D v15
  set the precedent for (gap-list item 6). **This is not a quartet gap and no row is owed**, but
  it was previously assumed rather than recorded, so it is recorded here:

  legs **58** (verify lane; files its pair as `leg_58_verify.md`), **64, 65, 66, 67, 69, 70, 72,
  73, 74, 77, 78, 79, 80, 81, 82, 84, 86, 87, 88, 89, 90, 91, 92, 93, 94, 97, 102**.

  Their evidence lives in `experiments/journal/leg_N.md` + `writeup/novelty/leg_N.md` (present
  for 29 of the 30 legs; leg 58 uses the `_verify` suffix), plus a curated JSON under
  `writeup/data/` for 24 of the 30 and a runner under `experiments/` for all 30. Nothing about
  this set is `GAP`.

> ⚠ **Superseded in part by leg 138 (below).** Three legs in the list above — **58, 60 and
> 62** — have since landed BLOG/TECHNICAL prose and/or registered figures on `main`, in
> commits that post-date leg 108's own pass. The classification was true when written and is
> false now; legs 58 and 62 have Arc 4 rows of their own above, and leg 60's work is recorded
> in the Route-PORT v1/v2 rows. Nothing else in leg 108's block is disturbed.

**Index currency — third pass (leg 138, Route-IX3).** Audit window pinned at
`3474862` (`origin/main` HEAD when leg 138 began), range `63dc163..3474862`. Since leg 108's
pass, **33 numbered legs** have landed (58, 60, 62, 71, 83, 85, 89, 92, 98, 99, 100, 101,
103–107, 111–117, 119–121, 123, 126, 131, 134, 136, 141) plus repo-wide `Leg 0:` integration
work, and this file again received **0 edits** across all of them. Full per-leg inventory and
every claim re-checked against disk: [novelty/leg_138.md](novelty/leg_138.md),
`experiments/p2_route_ix3_v1_index_audit.py` →
`data/p2_route_ix3_v1_index_audit.json`. Note that leg *number* order and *landing* order
differ here — the low numbers in that list are legs whose branches merged after leg 108's
pass, not legs leg 108 missed. The result splits four ways:

- **3 routes were owed a table row and now have one**: Route-NG v1 (leg 58), Route-CP v1
  (leg 62), Route-BX v1 (leg 126). These are the only legs in the window that *added* a
  route's BLOG/TECHNICAL pair.
- **1 route is owed a row that says it did *not* land**: Route-M2 v1 (leg 63), gate YES but
  escalation #1, parked on `leg/m2-v1` with **0 of its 4 declared artifacts on `main`**. It is
  listed above as `PARKED, NOT LANDED`, and `fig57` is **reserved** by it rather than missing.
  This is the first time the parked-escalation convention appears in this file at all.
- **4 `GAP` marks on 3 existing rows were false and are corrected** (Route-PORT v1 `E`/`F`,
  Route-PORT v2 `E`/`F`, Weight-repairs v1 `E`) — see gap-list items 1, 2 and 9. Three of
  these went stale when leg 60 landed; the fourth was **incorrect when leg 108 wrote it**.
- **29 of the 33 legs produced no BLOG/TECHNICAL and no figure**, by design, under the same
  "no measurement, no figure" convention: legs **71, 83, 85, 89, 92, 98, 99, 100, 101,
  103, 104, 105, 106, 107, 111, 112, 113, 114, 115, 116, 117, 119, 120, 121, 123, 131, 134,
  136, 141**. All 33 file both `experiments/journal/leg_N.md` and `writeup/novelty/leg_N.md`,
  and 32 of 33 file a curated JSON under `writeup/data/`. **No row is owed for any of them**
  and nothing about this set is `GAP`.

One state this file previously had no way to express, and now does: a route can be **landed
with a parked escalation attached**. Route-NG v1 is that case — its own TECHNICAL header says
"parked, not merged" of its *publication scoping*, while the route itself was ruled mergeable
and `plan_of_record.py` prints stage `NG` as done. Route-M2 v1 is the different, stricter case:
nothing merged. The two are not the same status and the rows say so.

**Index currency — fourth pass (leg 156, Route-IX4).** Audit window pinned at
`9f6729e` (`origin/main` HEAD when leg 156 began), range `3474862..9f6729e` — `3474862` is
leg 138's *own pin*, so this window is exactly what leg 138's pass could not see. It holds
**81 commits** and **23 numbered legs** other than leg 138 itself (122, 124, 125, 127, 128,
130, 132, 133, 135, 137, 139, 140, 142, 144, 146, 147, 149, 152, 155, 157, 158, 159, 161),
plus repo-wide `Leg 0:` integration work. `INDEX.md` received exactly **1 edit** inside the
window — leg 138's own fix (`b9b6398`), which landed *after* its pin — and **0 edits** across
all 23 audited legs since. Full per-leg inventory and every claim re-checked against the
pinned tree: [novelty/leg_156.md](novelty/leg_156.md),
`experiments/p2_route_ix4_v1_index_audit.py` →
`data/p2_route_ix4_v1_index_audit.json`. The result splits three ways:

- **3 routes were owed a table row and now have one**: Route-M2P v1 (leg 125), Route-NGX v1
  (leg 127), Route-NKR v1 (leg 128). These are the only legs in the window that added a
  route's BLOG/TECHNICAL pair. Two of the three ship no `*_evidence.py` — new gap item 13.
- **20 of the 23 legs produced no BLOG/TECHNICAL and no figure**, by design, under the same
  "no measurement, no figure" convention: legs **122, 124, 130, 132, 133, 135, 137, 139, 140,
  142, 144, 146, 147, 149, 152, 155, 157, 158, 159, 161**. **No row is owed for any of them.**
  Hygiene in this window is the best of the four passes: **23 of 23** file both
  `experiments/journal/leg_N.md` and `writeup/novelty/leg_N.md`, and **23 of 23** file a
  curated JSON under `writeup/data/` (leg 138's window: 32 of 33; leg 108's: 24 of 30).
- **0 new parked routes.** Sweeping every `writeup/4_p2_lottery/` BLOG/TECHNICAL path that
  `DIRECTION.md` declares against the pinned tree leaves exactly one undelivered pair —
  leg 63's Route-M2, which already has its `PARKED, NOT LANDED` row. The convention added by
  leg 138 needed no second entry.

**The predecessor's convention block survives this pass, and that is a result, not a
formality.** Leg 138 had to supersede leg 108's block because 3 of the legs listed there
(58, 60, 62) later landed prose. The identical predicate, run against leg 138's own 29-leg
block, finds **0 violators** — none of those 29 legs touched a `4_p2_lottery/` BLOG/TECHNICAL
file or `writeup/figures/` in this window. This is the first pass at which the previous pass's
classification is confirmed rather than corrected. The check is not a tautology: the same code
returns `MISSING` for the three rows above, which is how legs 125/127/128 were found.

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
   **✅ CLOSED by leg 60, recorded by leg 138.** Both named pieces now exist:
   `experiments/p2_route_port_v1_bordered_evidence.py` and
   `writeup/figures/fig59_route_port_v1.png`. The row above reads `Y†` / `fig59`.
2. **Route-PORT v2** (`writeup/4_p2_lottery/TECHNICAL_P2_ROUTEPORT_V2.md`) — has runner
   (`experiments/p2_route_port_v2_reach.py`) and curated data
   (`writeup/data/p2_route_port_v2_reach.json`), but is missing all of: `BLOG_P2_ROUTEPORT_V2.md`,
   a `p2_route_port_v2_evidence.py`, and a registered figure. This is a negative-leaning
   result (truncation gap gets worse with reach) and per lesson 76 deserves the same care as
   a positive one. Not fixed here — writing the BLOG/TECHNICAL prose and picking what the
   figure should show is a claim-bearing decision, out of DOCS's mechanical-only remit.
   **◐ NARROWED by leg 60, recorded by leg 138: 2 of the 3 named pieces now exist**
   (`experiments/p2_route_port_v2_reach_evidence.py` and
   `writeup/figures/fig60_route_port_v2.png`). **`BLOG_P2_ROUTEPORT_V2.md` is still absent**
   and this item now stands for that one clause alone.
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

9. **Weight-repairs v1 was absent from the Arc 4 table entirely** (found by leg 108). All of
   `experiments/p2_weight_repairs_v1.py`, `writeup/data/p2_weight_repairs_v1.json`,
   `writeup/4_p2_lottery/BLOG_P2_WEIGHT_REPAIRS_V1.md`, `TECHNICAL_P2_WEIGHT_REPAIRS_V1.md` and
   `writeup/figures/fig48_weight_repairs_v1.png` exist on disk — 4 of 5 quartet pieces, with no
   `*_evidence.py`. The route landed in commit `9d9b7ea`, which pre-dates the `Leg N:` commit
   convention and therefore carries no leg number, which is why leg 68's by-number pass over
   legs 53–57 did not reach it. It had been referenced only obliquely, as the other half of the
   duplicated `fig48` in item 8. **Row added above**; the missing `*_evidence.py` stays `GAP` —
   writing one is a claim-bearing choice about what to plot, outside a links-and-labels remit.
   **✖ WITHDRAWN by leg 138 — this clause was wrong when written, not stale.**
   `writeup/4_p2_lottery/p2_weight_repairs_v1_evidence.py` exists and landed in `9d9b7ea`, the
   same commit that created the route, which **pre-dates leg 108's own pass**. So the route has
   **5 of 5** quartet pieces, not 4, and the `E` mark in its row is corrected to `Y`. The rest
   of item 9 (why leg 68's by-number pass missed the route) stands. This is the only claim in
   the file that failed for this reason rather than by going stale.
10. **Route-KA v1 (leg 61) has TECHNICAL but no BLOG, no `*_evidence.py` and no figure** (found
   by leg 108). Runner `experiments/p2_route_ka_v1_kawahara.py` and curated data
   `writeup/data/p2_route_ka_v1_kawahara.json` are both present, and this is the leg that
   reproduced a *published* radius end to end — the repository's one external known-answer check
   of the interval pipeline, so per lesson 76 it earns the same care as a headline result. 3 of
   5 quartet pieces present. Not fixed here: BLOG prose and figure selection are claim-bearing.
11. **`writeup/README.md`'s numbered index is now stale by a further 30 legs** — item 4 recorded
   it stopping at entry #47; leg 108 confirms it has received no entry for any leg in the
   58–102 window either. Same reason as item 4 (numeric-prose paragraphs, out of remit), same
   flag, larger backlog. Confirmed on disk: `writeup/README.md`'s list still ends at entry 47
   and contains 0 mentions of Weight-repairs (v1 or v2) or Route-KA/Kawahara. The three rows and
   the convention block added above cover the gap here in the meantime.
   **Re-checked by leg 138 and still true in substance, with one qualifier retired**: the
   numbered list still ends at entry 47, still skips 45, and still has 0 mentions of
   Weight-repairs or Route-KA/Kawahara — but it is no longer *untouched*, because leg 60 edited
   entries 46 and 47 (adding the `fig 59` / `fig 60` references and a reproduction-check block).
   The backlog grows by this window's 33 legs on top of the 58–102 window's. Same reason as
   item 4 for not fixing it here (numeric prose, out of remit), same flag, larger backlog.
   **Re-checked by leg 156 and still true, verbatim**: the numbered list still holds 46 entries,
   still ends at 47, still skips 45, still has 0 mentions of Weight-repairs or Route-KA/Kawahara
   — and now 0 mentions of **M2P, NGX or NKR** either, so the three routes this pass added to
   the table above are absent from `README.md` as well. Backlog grows by a further 23 legs and
   3 routes. Same reason for not fixing it here, same flag, larger backlog again.
12. **Figure-number registry has 2 unallocated numbers and 1 reserved one** (found by leg 138).
   `writeup/figures/` holds 58 PNGs. **`fig53` and `fig54` name no file and are cited by no
   writeup** — an unallocated hole below the `fig55`–`fig60` block `DIRECTION.md` pre-allocated;
   `reports/TECH_DEBT_REVIEW_2026-08-05.md` row A3 independently records the same hole, together
   with item 8's duplicated `fig48`. **`fig57` is different: it is *reserved*, not missing** —
   pre-allocated to leg 63 / Route-M2, which is parked and unmerged (see its row above). Not
   fixed here: renumbering is a registry ruling over citation keys already baked into banked
   prose, which is exactly what row A3 says it needs, and it is not a links-and-labels decision.
   **Updated by leg 156: the hole set is now `{fig53, fig54, fig62}` and `writeup/figures/`
   holds 60 PNGs, not 58.** `fig62` is a *released reservation*: leg 126's Route-BX row above
   reserved it for a yes-branch that did not fire (the gate answered **NO**), and leg 127 then
   allocated `fig63`, so the number is now permanently skipped rather than pending. `fig57`
   remains reserved-not-missing by parked leg 63. Highest allocated number: `fig63`. Same
   reason for not renumbering here.
13. **Route-M2P v1 (leg 125) and Route-NKR v1 (leg 128) each ship a BLOG/TECHNICAL pair with no
   `*_evidence.py`** (found by leg 156). M2P has runner
   (`experiments/p2_route_m2p_v1_promotion.py`), curated data
   (`writeup/data/p2_route_m2p_v1_promotion.json`), BLOG, TECHNICAL and `fig61` — **5 of 6**
   pieces, the `*_evidence.py` alone missing. NKR has runner
   (`experiments/p2_route_nkr_v1_repair.py`), curated data
   (`writeup/data/p2_route_nkr_v1_repair.json`), BLOG and TECHNICAL — **4 of 5** pieces, with
   no figure **by design** (its own header: "a repair leg with no curve to plot"), so only the
   `*_evidence.py` is owed there too. The third route in the same window, Route-NGX v1
   (leg 127), has all 6 and is the contrast case. Not fixed here, same reason as items 9 and 10:
   writing an `evidence.py` is a claim-bearing choice about what to rebuild and plot, outside a
   links-and-labels remit.

Route-TC is no longer in progress: it landed as leg 53 and has a complete quartet, indexed in
the Arc 4 table above.
