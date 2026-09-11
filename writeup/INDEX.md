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
| PROG-R4 U5 (leg 380) | **MILESTONE M3 — the seed budget is stratified by SHIFT: `DELIVERED`** on all five pre-committed clauses (AMENDMENT 5, `4f6f33f`, before either stage ran). Milestone, not a gate: **G1 is NOT re-answered and stays `UNDER-RESOURCED`**; `n_recovered = 0` is a pre-registered **count**, not a `no`. Does for SHIFT what AMENDMENT 4 did for PERIOD, except shift **cannot** be stratified at the mining stage (`R_red` is shift-invariant by construction), so the reservoir is **exhausted** instead: 913,301 strict local minima → 103,844 anchored → **75,873** taken under the lossless `R_red < 0.25` prune, **37.7×** U2's 2,014, then stratified downstream where `|s|` exists. In-band admissible supply **35 → 72**, in-band spend **31 → 60**, every stratum met quota, shortfall redistribution never fired. Spent **2,104** epochs against U3's 4,629 (**45.5%**) via a stall exit replayed on U3's banked ledger first, cutting **0 of 14** convergences at a **6.9×** margin — **fewer iterations, none bought**. **9/100 converged** to `tol=1e-8`, **0 recovered a named row**, best `‖R‖ = 8.67e-12`. Pre-registered fork settled: **H-supply REFUTED** (premise repaired, prediction failed at 60 in-band seeds), **H-hard favoured but NOT resolved** (matched-`R` pooled over both runs' 200 attempts: in-band **6/91 = 6.6%** vs out-of-band **17/109 = 15.6%**, Fisher two-sided **p = 0.073**). The finding, on a reading commit `c67179e` fixed *while the run was in flight*: **the bias is in the BASIN STRUCTURE, not only the seed supply** — **4 of 5 in-band convergences left the band**, **8 of 9** finished at `|s| < 0.15`, replicating U3's 13-of-14 endpoint on an independent 60-attempt arm. 9 convergences = **5 distinct solutions**, of which **4 are re-finds of U3's 8** and **one is new** (`T=20.4175/|s|=0.5867`, stratum P) — **the only solution either unit has found inside the published band**. R0's metric: **0.0877** distinct orbits/core-hour vs U3's 0.0553, provisional until R0 lands. Option (c) priced: an `m` unknown would unlock **334 of 575** in-window candidates but **only 1 is in band**, so it is the `|s|>0.9` fix, not the band fix | Y | Y | Y | Y | fig107 | [T](4_p2_lottery/TECHNICAL_P2_PROGR4_SHIFT_STRATA.md) · [B](4_p2_lottery/BLOG_P2_PROGR4_SHIFT_STRATA.md) — **UNVERIFIED under §3f** (one session, no paired verifier). Ceiling **TIER 2**, no `L1→L4` link moved, **Clay ~0.05%** |
| PROG-R4 U3 (leg 380) | **GATE G1: does at least one named Lucas–Kerswell Table IV RPO recover to `tol=1e-8`? — answered `UNDER-RESOURCED`**, planted controls FIRED AS PLANTED (P recovered `7.75e-9`, N did **not** `1.75`, R recovered `3.26e-9`). `NO` was removed from the branch set **before** the run by AMENDMENT 3 on measured cost, so **§3d's stop did NOT fire and route 4 is NOT stopped on measurement**. Headline: **0 of 100 recovered a named orbit, but 14 of 100 converged to `tol=1e-8`** — a **14%** per-attempt rate, above Chandler–Kerswell's 4.3% and Lucas–Kerswell's ~10%, best `‖R‖ = 8.67e-12`, onto **eight distinct RPOs of the discrete map**, three of them replicated from independent seeds and different anchors (`T=16.53/|s|=0.100` four times, agreeing to 0.012 in `T` and 0.002 in `|s|`). The misses are **systematic, not scattered**: converged `|s| ∈ [0.073, 0.317]` against published `|s| ∈ [0.295, 0.707]`, and the cause is a **second selection bias** in the seed supply — `corr(|s|, R) = 0.50` over 1153 `m=0` candidates, with the Newton window `R<0.25` admitting **44%** of `|s|<0.15` but only **11%** of the published band. The large-shift recurrences exist (all-candidate median `|s| = 0.824`); the window removes them. **Three errata against my own pre-registration**, the load-bearing one being that the compliant cost AMENDMENT 3 named (238 epochs, 15.1 core-days) is **the wrong purchase**: convergence is bimodal (all 14 finished in ≤29 epochs; the 86 others ran to the cap and were flat — 53% improved <1% over their final 10 epochs), and max Krylov dimension was 25 against `max_gmres=140`, so **neither cap bound any attempt that converged**. 14.47 h, 134.45 core-hours | Y | Y | Y | Y | fig97 | [T](4_p2_lottery/TECHNICAL_P2_PROGR4_G1.md) · [B](4_p2_lottery/BLOG_P2_PROGR4_G1.md) — **UNVERIFIED under §3f** (one session, no paired verifier). U4/G2 **not opened**: it needs a recovered *named* orbit. Ceiling **TIER 2**, no `L1→L4` link moved, **Clay ~0.05%** |
| PROG-R4 U2 (leg 380) | **MILESTONE M2 — the `T=1e5` DNS and its recurrence library.** Milestone, not a gate. DNS run from `t=0` at the compliant scale: 400,000 snapshots, 3.44 h, 1.2379 ms/step, **`D/D_lam = 0.0645 ± 0.0253`** (the planted check that the trajectory is on the chaotic attractor and not the laminar fixed point). Library: **95,542,640** `(t,T)` pairs scanned, **913,301** strict interior local minima of a **lossless** prefilter (`R_red ≤ R` pointwise, from unit-modulus phases plus the reverse triangle inequality), best `R = 0.016543` against **leg 353's 0.177** for UPO37. Headline finding, not asked for: **the global candidate ranking starved the band every named orbit lives in** — of the global top-400, exactly **ONE** candidate was in-window, `m=0` *and* anchored to a named period, because short near-repeats at `T=1.25–2.5` score better for reasons unrelated to being an orbit while every published orbit sits at `T≈14.8–19.3`. **AMENDMENT 4** stratifies the budget across the named periods (additive; removes nothing): **1 → 30 → 133** anchored at `per_anchor` 80 → 500, restoring the pre-registered 100 attempts. The amendment is labelled as made **after** observing the shortfall, and the knob is closed by rule (raised once, in one step, run on a short pool otherwise) | Y | Y | Y | Y | — | [T](4_p2_lottery/TECHNICAL_P2_PROGR4_MINING_BAND.md) · [B](4_p2_lottery/BLOG_P2_PROGR4_MINING_BAND.md) — **UNVERIFIED under §3f**. No figure spent. Ceiling **TIER 2**, **Clay ~0.05%** |
| PROG-R4 U2/U3 controls (leg 380) | **The planted control that caught a fabricated `no`.** Not a gate — an instrument finding banked because G1's `no` was the answer that stops route 4. Control P (the exact fixed point of the **discrete** map in closed form, `ŵ* = dt·f̂·decay/(1−decay)`, `‖Φ_dt(w*)−w*‖ = 7.6e-14`) failed as pre-registered and exposed a defect in `newton_hookstep_rpo`: the wrapper read the **pre-step** residual and broke before the adopt block, **discarding a converged iterate and returning `success=False`** — at G1 that is a non-recovery recorded on an attempt that recovered, i.e. a manufactured `no` on the one gate whose `no` stops a route. Caught by an exact planted fixed point reporting `converged` at `1.6e-8 > tol`. Fix verified by **bit-identical** re-reproduction of MILESTONE M1; both suites pass (32/32, 12/12). Also: AMENDMENT 1 re-scales P to `T_P = 2.65` by log-interpolating the **measured** amplification table, because at the pre-registered `T=19.33` the equilibrium's `λ=2.88` amplifies by `~1e24` — not a control, a different problem | Y | Y | Y | — | — | [T](4_p2_lottery/TECHNICAL_P2_PROGR4_CONTROL_CATCH.md) · [B](4_p2_lottery/BLOG_P2_PROGR4_CONTROL_CATCH.md) — **UNVERIFIED under §3f** |
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
| Route-PORT v2 | Reach makes the truncation gap WORSE (+0.47 dec/unit ρ) — tail lemma forced | Y | Y | Y | Y† | fig60 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEPORT_V2.md) · [B](4_p2_lottery/BLOG_P2_ROUTEPORT_V2.md) — **quartet completed by leg 375**, gap-list item 2 now closed |
| Route-T v1 | Bordering restores a bounded tail; works where the failure curve was worst | Y | Y | Y | Y | fig47 | [T](4_p2_lottery/TECHNICAL_P2_ROUTET_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTET_V1.md) |
| Route-TC v1 | Assembling the bordered certificate: four terms in one polynomial; the term that ran out is Z₁'s block coupling | Y | Y | Y | Y | fig48 | [T](4_p2_lottery/TECHNICAL_P2_ROUTETC_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTETC_V1.md) |
| Route-MM v1 | The shape of the approximate inverse, spent — gate answered **NO** | Y | Y | Y | Y† | fig49 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEMM_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEMM_V1.md) |
| Route-NB v1 | Compactified-basis coefficient decay of `HL_S2_nonsymmetric`: is the target in the space? | Y | Y | Y | Y† | fig50 | [T](4_p2_lottery/TECHNICAL_P2_ROUTENB_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTENB_V1.md) |
| Route-TN v1 | The `(H, D)` consistency defect of `L1` step one, enclosed — gate answered **NO** | Y | Y | Y | Y† | fig51 | [T](4_p2_lottery/TECHNICAL_P2_ROUTETN_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTETN_V1.md) |
| Route-XS v1 | The shape dichotomy against published certificates — gate answered **NO** | Y | Y | Y | Y† | fig52 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEXS_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEXS_V1.md) |
| Weight-repairs v1 | Named P2/P3 repairs to the certificate-weight fitness; six-property gate still FAILs | Y | Y | Y | Y | fig48 (**duplicated number** — see gap list item 8) | [T](4_p2_lottery/TECHNICAL_P2_WEIGHT_REPAIRS_V1.md) · [B](4_p2_lottery/BLOG_P2_WEIGHT_REPAIRS_V1.md) — row added by leg 108; its `E` mark **corrected by leg 138**, see gap list item 9 |
| Weight-repairs v2 (leg 59) | The conditioning wall modelled in both weight factors; frozen six-property gate re-run still FAILs | Y | Y | Y | Y† | fig58 | [T](4_p2_lottery/TECHNICAL_P2_WEIGHT_REPAIRS_V2.md) · [B](4_p2_lottery/BLOG_P2_WEIGHT_REPAIRS_V2.md) |
| Route-KA v1 (leg 61) | The interval pipeline reproduces CLN's published Kawahara radius end to end | Y | Y | **GAP: T only, no BLOG** | Y | not a gap — no figure by design, matching this route's own header | [T](4_p2_lottery/TECHNICAL_P2_ROUTEKA_V1.md) — `E` closed leg 372 (`experiments/p2_route_ka_v1_kawahara_evidence.py`, 8/8 checks pass, reads only the banked JSON); `F` was never a real gap — TECHNICAL_P2_ROUTEKA_V1.md's own header says "No figure ... established convention" (same class as the NKR row below); BLOG stays open, out of a scripts/figures-only remit — gap list item 10 |
| Route-NG v1 (leg 58) | Stage `NG`: the no-go stated as a theorem on the class `A21 = 0` — gate answered **YES**; publication scoping **escalated and parked**, the route itself merged | Y | Y | Y | Y† | fig55 | [T](4_p2_lottery/TECHNICAL_P2_ROUTENG_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTENG_V1.md) — added by leg 138 |
| Route-CP v1 (leg 62) | Cadiot arXiv:2505.03091's scope settled from the full text — gate answered **NO** | Y | Y | Y | Y† | fig56 | [T](4_p2_lottery/TECHNICAL_P2_ROUTECP_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTECP_V1.md) — added by leg 138 |
| Route-BX v1 (leg 126) | Stage `B` answered from the banked record, the closure audit — gate answered **NO** | Y | Y | Y | Y† | none | [T](4_p2_lottery/TECHNICAL_P2_ROUTEBX_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEBX_V1.md) — **explicitly no figure by design**: the yes-branch would have registered `fig62`, the no-branch measures nothing (see file header). Added by leg 138 |
| Route-M2P v1 (leg 125) | Chen's γ=2 dissipative gCLM candidate: full text, constants, first `Y₀` — gate answered **NO** on both clauses | Y | Y | Y | Y | fig61 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEM2P_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEM2P_V1.md) — added by leg 156; `E` closed leg 372: `experiments/p2_route_m2p_v1_promotion_evidence.py` rebuilds `fig61` from the banked JSON alone (no solver import, byte-identical across two reruns), registered in `build_figures.py`'s `P2_EVIDENCE` list — gap list item 13 |
| Route-NGX v1 (leg 127) | The general class `A₂₁ ≠ 0`, decided: `Z₁ ≥ 1` for every bounded `A` — gate answered **YES (i)** | Y | Y | Y | Y† | fig63 | [T](4_p2_lottery/TECHNICAL_P2_ROUTENGX_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTENGX_V1.md) — added by leg 156 |
| Route-NKR v1 (leg 128) | One guard for three pipelines: the `Y₀`/`Z₀`/`Z₁` fabrication-acceptance gap, closed as a class — gate answered **YES on (b) and (c), NO on (a)** | Y | Y | Y | Y | none | [T](4_p2_lottery/TECHNICAL_P2_ROUTENKR_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTENKR_V1.md) — **explicitly no figure by design**: "a repair leg with no curve to plot" (see file header). Added by leg 156; `E` closed leg 372: `experiments/p2_route_nkr_v1_repair_evidence.py` (6/6 checks pass, reads only the banked JSON, no solver import, no figure produced — matching this row's own by-design convention) — gap list item 13 |
| Route-M2 v1 (leg 63) — **PARKED, NOT LANDED** | Target reselection under the multiplier/shift screen — gate answered **YES**, and that answer is **escalation #1**: parked on branch `leg/m2-v1`, never merged | — | — | — | — | `fig57` **reserved** | **No files on `main`.** Read the branch with `git show`; do not merge or build on it. Territory and finding: [DIRECTION.md](../DIRECTION.md) §63. Row added by leg 138 |
| Route-CADX v1 (leg 304) | Does Cadiot arXiv:2505.03091 cover a zero diagonal? Answered **NO — excluded by hypothesis**, Assumption 1 p.6 (`\|l(ξ)\| ≥ l_min > 0`), load-bearing at 8 of 12 located clauses; `l_min = µ` exactly on his leading Swift-Hohenberg example, published runs 0.28/0.32 from the excluded case; a zero *eigenvalue* **is** covered, a zero *diagonal* is not — gate answered **YES (i)** | Y | Y | Y | Y | fig67 | Registered by integration (leg 0). The leg claimed the number provisionally; it landed first and keeps it. **The ban this bears on is NOT lifted** — see the escalation in `reports/ORCH_STATE.md` |
| Route-P0TCV v1 (leg 300) | Independent verification of leg 266's GATE-YES correction to leg 251's certificate obligation #1 — gate answered **NO**: architecture PASS (3/3 sub-claims, 10/10 BCG locators), byte-untouchedness PASS (29/29 claims identical), **magnitudes FAIL 4/5** — the width ratio quoted `6.855` re-derives as the closed form `(7+3√5)/2 = 6.854`, rel. err `1.310e-04`. Leg 266 stays unmerged | Y | Y | Y | Y | fig68 | Renumbered `fig67 → fig68` by integration (leg 0): legs 300 and 304 both claimed `fig67` independently while parallel: 304 landed first and keeps it. Evidence script re-run after the rename, 29/29 checks pass |
| Route-FSB v1 (leg 301) — **PARKED, NOT LANDED** | The fourth space/basis screen: 14 candidates against the three measured death mechanisms, **exactly one survivor** — the Malmquist–Takenaka / Christov rational Hardy basis, `l_min = 1.0` computed vs the incumbent's exactly `0.0`. Gate answered **YES**, which is **escalation #8**: parked on branch `leg/301-fsb-v1`, never merged | — | — | — | — | `fig75` **reserved** (was `fig69`) | **No files on `main`.** `fig69` was reassigned to leg 302, which landed on it while this branch stayed parked — a landed artifact takes precedence over a reservation held by a branch that may never merge, so this leg's reservation moved to `fig75` and its eventual landing must renumber. Read the branch with `git show`; do not merge or build on it. **The ℓ¹-Fourier ban is NOT lifted** — the leg wrote the Route-MT v1 scoping spec the lift condition names instead of lifting anything. Counterweights at full strength: `δ = 1.0000` exactly at every n, no validated MT transform exists anywhere, nonlinearity entirely unmeasured |

| Route-IVAX v1 (leg 311) | Does screen (iv_a) apply off the fluid axis? Answered **YES** — 3 of 3 non-incompressible models (fractional gCLM, critical-dissipation gCLM, fractional Boussinesq) killed by Remark 40's stated reach, the same clause that killed 18/18 fluid rows in leg 261. Mechanism per lesson 91: **nonlocality generally, not incompressibility specifically**. Non-fluid pool is **not** materially larger than leg 261 implied | Y | Y | Y | Y | `fig70` | **Quartet gap closed at leg 322**: `writeup/build_figures.py`'s new `fig_route_ivax_v1()` stanza plots directly from leg 311's own banked `writeup/data/p2_route_ivax_v1.json` census — no re-measurement. Left panel: 18/18 (leg 261 fluid pool) vs 3/3 (this leg's non-fluid pool) kill-rate comparison. Right panel: per-model count of operator classes Remark 40 leaves unnamed, colored fluid-adjacent vs not. Writes `writeup/figures/fig70_route_ivax_v1.png`. Liveness self-test 3/3: stripping dissipation still kills all three via the nonlinearity operator alone; viscous-Burgers positive control passes. Escalated nothing, lifted nothing |

| Route-CNRV v1 (leg 286) | Post-repair verification of leg 248's `collocation_newton.py` gauge-defect repair — gate answered **YES on all three clauses**: 41/41 of leg 237's battery carry the correct verdict (0 mismatches, `gauge_defect` bit-identical to independent recomputation at exactly 0.0 rel. err), leg 202's calibration pair still flags 2/2 genuine escapes with 0 of 8 clean solves suppressed and 7.18 decades of margin, and **0 floats moved of 12,356 bitwise comparisons** against the pre-repair source | Y | Y | Y | n/a | none | **Verification leg, no figure by design.** Honest delta recorded, not smoothed: worst gauge defect 1.110e-15 vs leg 248's banked 8.882e-16, traced to a BLAS-thread-visible 6.7e-10 spread. One test failure diagnosed under flake-diagnosis-before-belief and found **not** a flake but the leg's own wrongly-guessed assertion, narrowed to the measured regime and documented |
| Route-GAF v1 (leg 303) | Grade-A/fluid cell freshness sweep, mid-2026 — gate answered **YES**: 35/35 queries reached, 68 papers, links for every row; leg 174's 12 queries replicate exactly (0/12 counts grew), but **one claimant appears in the empty cell** — arXiv:2604.09949, computer-assisted NK + interval arithmetic on **3D incompressible** NS. Recorded **claimed, not filled**: `before 0 → claimed 1, ESTABLISHED 0` | Y | Y | Y | Y | fig71 | Renumbered `fig68 → fig71` by integration (leg 0); evidence script re-run, 18/18 pass. **Phase 1's premise is NOT recorded as broken** — occupancy cannot be settled at abstract depth, and the adversarial full-text read is leg 309's, dispatched immediately on this landing. Method findings: **MF1** the paper spells itself `Navier--Stokes` (LaTeX double hyphen) so a `Navier-Stokes` search string silently misses it; **MF2** leg 174 banked counts not links, so 10 of its links are unrecoverable |
| Route-PUB2X v1 (leg 280) | The user-gated eighth pass: four Xu-normalization / convention sites corrected — gate answered **YES on all five clauses** (a) 4/4 sites with dated notes, (b) no other site carries the defects, (c) CORRECTIONS.md appended, (d) exactly 4 replace hunks, 7/722 lines touched, rest byte-identical, (e) **zero arguments changed** | Y | n/a | Y | n/a | none | **Document-correction pass, no runner or figure by design.** Ran only after the user's sign-off. Integration note carried forward: `BLOG_P2_PUB2_V1.md` L102/L108 print the same uncorrected `0.0420` and a `0.71465` cross-reference but lie outside this leg's TECHNICAL-only territory — flagged, not edited. **Occupies `CORRECTIONS.md` §13 AND §14** — see leg 319's row |
| Route-DFRE v1 (leg 316) | The standing CAP-reproduction lane's **first entry**: DF-CGL (arXiv:2410.05480) reproduced from its **own released proof-witness data** (CGL.jl @ `be034923`, pinned to the paper's own bibliography commit), decoded from `arb_dump_str` in **exact dyadic-rational arithmetic** (`fractions.Fraction`) and checked against the paper's own Thm 4.1/Sec.6 box-chaining corollary — gate answered **YES on all 49,465 rows** of branch Case I j=1 (top+turn+bottom) plus both connection points | Y | Y | Y | Y | fig74 | Renumbered `fig71 → fig74` by integration (leg 0). **That collision was the orchestrator's error, not the leg's** — I moved 316 off fig70 onto fig71 mid-run and had myself renumbered leg 303 into fig71 the same cycle; 303 landed first and keeps it. Evidence script re-run after the rename, 16/16 checks OK. Decoder cross-checked against the paper's own printed Sec.6 starting point (`µ₁`, `κ₁`). Reproducing someone else's proof is not this repository proving anything |
| Route-P2T1 v1 (leg 302) | The cheapest **load-bearing** apparatus term: BCG term **A4** (adiabatic/γ-law pressure), head of leg 285's measured critical path `A4→A1→A2→A9→A8→A13→A14` — gate answered **NO**, both halves pre-registered. 10/11 known-answer probes pass; **KA8 fails at 129.048× its 1e-9 tolerance** (`\|k(1)−1\| = 1.29e-07`). Negative controls 5/5, self-tests 14/14, every must-fail plant probe failed as pre-stated | Y | Y | Y | Y | fig69 | **Mechanism named (lesson 91): transcription correct, evaluation ill-conditioned.** At 60 digits `k(1)=1` exactly and `k(7/6)=16.347921051661395` reproduces legs 265/266 — the transcription is *proven* right; in IEEE double the `R₂` radicand (exact sum 0 at `r=1`, largest term 24.528) sums to `1.22e-14` of rounding dust and the square root costs half the digits. **Consequence: A15a (ball arithmetic) is a prerequisite of 285's critical path near `r=1`, not the off-path convenience 285 ranked it as** — leg 308 re-scoped. `fig69` was *reserved* to parked leg 301; a landed artifact beats a reservation on a branch with no files on `main`, so 302 keeps it and 301 moves to `fig75`. Quartet gap closed by integration: the leg shipped a `--figure` flag but no file, so the runner was re-run with it — only JSON delta is `emitted_this_run_to`, gate unchanged at NO **Rebuild-stability closed (leg 327):** the runner's `--figure` path exits nonzero on this leg's own NO gate, so it would fail a shared/CI `writeup/build_figures.py` rebuild; leg 327 wrote a standalone `experiments/p2_route_p2t1_v1_evidence.py` that redraws `fig69` from `writeup/data/p2_route_p2t1_v1.json` alone (no re-run, byte-stable across reruns, 5/5 self-checks), registered it additively in `build_figures.py`'s `P2_EVIDENCE` list, and named KA8's failure at its measured magnitude — `129.048x` its `1e-9` tolerance, `\|k(1)−1\| = 1.2904784973954975e-07` — directly on the figure, not smoothed or rounded away |
| Route-GAF2 v1 (leg 309) | **The adversarial full-text read of the claimant in the empty cell.** Does arXiv:2604.09949's claimed computer-assisted NK+interval validation of 3D **incompressible** NS on T³ sustain itself? — gate answered **NO: the paper breaks.** 14 load-bearing items enumerated *first*, then adjudicated; every independently recomputable constant (`K`, `C_rec^map`, the NK closure product) **checks out** — the break is structural, not arithmetic | Y | Y | Y | n/a | none | **Breaking hypothesis quoted verbatim** (Thm 12.1, eq. 18, `Son.tex` l.523–535, cross-checked pixel-for-pixel against the official rendered PDF p.9): `u(x,t) = (1/√(T*−t))·ū(x/√(T*−t))` — an exact backward self-similar 3D NS solution with a smooth, Gevrey-decaying (hence `L³(ℝ³)`) nontrivial profile, **exactly the class Nečas–Růžička–Šverák (1996) / Tsai (1998) prove must be trivial.** Never cited, never addressed. Independently confirmed by a full-text read this repository had already done (found via the mandatory novelty pass in `solver/target_selection.py`), plus three secondary non-load-bearing breaks. **The Grade-A/fluid cell stays empty; Phase 1's premise is unchanged.** Leg 303's row resolves to `claimed 1 / established 0 / adjudicated-and-refuted`. **Refuting someone else's claim is not this repository moving a link** |
| Route-SFTX v1 (leg 317) | The silent-failure taxonomy (steer lane 7): are this repository's two measured defect families literature-novel? — gate answered **NO**, both are folklore. **The taxonomy was therefore not drafted, and that is the finding at full strength** | Y | Y | Y | n/a | none | Family A (legs 79/98/116/128/140/142, hypothesis-violation/fabrication acceptance in `Y₀`/`Z₀`/`Z₁`/`Z₂`) already settled per leg 79's own pass (van den Berg–Lessard, AMS Notices 2015; IEEE 1788-2015 decorations). **Family B is the sharper result and cuts against the assignment's own framing**: legs 202/237's "scale-invariant test blind to scaling-family escape" is the *named justification for an entire existing methodology* — Beyn–Thümmler 2004 freezing/phase-condition, pseudo-arclength continuation, the dynamic-rescaling literature (Merle–Raphaël–Martel–Zaag lineage) — older and broader than expected. Magnitudes carried with their locators: leg 202 M1 `c(a=1.5)` = 0.20427/0.23717/0.97282 at n=101/201/301 (**376% apart, all "converged" at machine precision**); M2 off by `6.15e5×`. **Ran with spelling variants per MF1.** Prior-art map banked as links, not counts |
| Route-P0TCR v1 (leg 319) | Correct the landed surfaces carrying the wrong width ratio `6.855` — gate answered **NO**: **5 of 7 corrected**, no 8th found. The 2 uncorrected are leg 300's own **dispatched gate text** | Y | n/a | Y | n/a | none | **A NO that established a standing rule.** The leg declined to edit the two gate-text sites (`DIRECTION.md:13330`, `:13338`) on the ground that a pre-committed gate records what was *asked* — the DM adopted this: **dispatched gate text is immutable**, because editing it would corrupt the audit trail that caught the wrong digit in the first place. 5/7 banked as complete; the two sites get `CORRECTIONS.md` *pointers* from leg 321, never edits. Corrected surfaces read `6.854`, closed form `(7+3√5)/2`. **`CORRECTIONS.md` §-numbering:** briefed to renumber §13→§14, the landing agent found `main` already carried leg 280 at **both** §13 and §14, so it took **§15** rather than recreate the very collision the renumber exists to prevent — the right call, and the deviation is recorded in its own commit message. No numeric value changed in the landing |
| Route-BLCX v1 (leg 321) | The two blog surfaces leg 280 flagged but could not reach, plus pointers for leg 319's immutable gate-text sites — gate answered **YES**: L102 `0.0420 → 0.057643` (‖R‖_X = 17.348), L108's `0.71465` cross-reference corrected to state it is convention-**free** to `1.87e−16`, `CORRECTIONS.md` §16 appended, **zero other numeric content changed** | Y | n/a | Y | n/a | none | **Record work; every value quoted from a landed leg, none re-derived** — L102 from `CORRECTIONS.md` §13 / leg 280 per leg 277, L108 from §14 / leg 280 per leg 281 E5. **Diff-check delivered rather than asserted:** 9 insertions / 3 deletions confined to the two flagged sentences, every other digit (`0.0908`, `140.72`, `4.03`, `7.9×`) byte-identical; `CORRECTIONS.md` a pure append. The two gate-text sites `DIRECTION.md:13330`/`:13338` confirmed **still reading `6.855x` and not edited** — the immutable-gate rule held on contact. Took §16 after checking §15 was last on `main`, the third leg running to verify its section number rather than trust its brief |
| Route-MTSC v1 (leg 320) — **PARKED, NOT MERGED** | Scoping the Malmquist–Takenaka / Christov rational Hardy basis that leg 301 left as its single survivor — gate answered **YES on all four clauses**, which is an **escalation**: branch `leg/320-mtsc-v1` at `79fea23`, pushed as a branch, never merged. **(a)** M1 does not recur on the **real target's coupled operator** (not a bare differentiation matrix): `l_min` flat `0.4773`, `σ_min` stable `0.025–0.031` across an **8× truncation range** (M=8…64) — leg 301's own kill condition `σ_min → 0` **not triggered**. **(b)** M2 does not recur: exact closed-form `D` and Hilbert diagonal, skew-Hermitian error **exactly 0.0**. **(c)** M3 does not recur, and **the nonlinearity — leg 301's entirely-unmeasured counterweight — is measured for the first time**: `‖Q(v,v)‖/‖v‖²` bounded `0.34–1.37`. **(d)** Build cost floored at **6–9 legs, ~40–65 leg-hours** | — | — | — | — | `fig72` **reserved** | **No files on `main`.** Read the branch with `git show`; do not merge or build on it. **The ℓ¹-Fourier / radii-polynomial ban is NOT lifted** — only the user rules on it, and this leg built nothing beyond its quartet. **Two honesty items that are load-bearing for that ruling and must travel with the packet:** a first pass falsely showed `σ_min` collapsing to `1e-17`, and a **Gram-matrix control caught it as a quadrature-under-resolution artifact** (grid too coarse for the mode count; corrected by `n=801` under `n ≥ 6×(2M+1)`) — unchecked, it would have killed the only surviving space on an instrument defect; and the top test point at n=64 **coincided with the projection window's cap and is reported unresolved, not sold as a pass**. **The counterweight that survives:** still **no validated (interval/CAP) MT transform exists anywhere** — arXiv:1904.10755 (Shindin–Parumasur–Aluko) supplies only *classical, non-interval* convergence theory for the matching structure, which lowers the cost estimate without discharging the gap. A surviving candidate space is not a result about the equations |
| Route-TMS v1 (leg 315) | Validated integration / Taylor models (steer item 2): name a concrete object this repository's radii-polynomial / Newton–Kantorovich apparatus **does not reach** and that TM integration does — gate answered **YES**, two objects named. Headline **O1, the sonic-crossing `r`-tube**: a rigorous enclosure of BCG's autonomous `(W,Z)` self-similar **Euler** ODE flow at γ=7/5 **through the sonic point**, as a Taylor model in the similarity exponent, certifying profile-vs-`F_dis` domination **beyond** the dominance-window endpoint `r = 1.1909830`. Certified width `0.0243163` against available `0.1666667` — shortfall `(7+3√5)/2 = 6.8541019662496845446` | Y | Y | Y | Y | fig79 | **Mechanism named (lesson 91): sonic-point-desingularized Taylor-model flow-map stepping** with Lohner-QR / shrink-wrapping as the wrapping control — not the quasi-homogeneous enclosure already in-repo. **Cost class C (research), and the reason matters more than the class:** Zgliczyński's ODE→PDE bridge (math/0005247) assumes **dissipativity**, while BCG's rescaled system is **quasilinear hyperbolic**, so the Galerkin-plus-tail bridge has no known form here. **Two controls that come out the other way (lesson 90), asserted in code, not narrated:** C1 the repo's own bordered certificate; C2 arXiv:2305.08221, which does validated *parabolic* time-integration **by Newton–Kantorovich** — it **refutes the leg's own naive thesis** that NK cannot do time, and the leg reported that against itself. O3 recorded as reached by **neither**, so the YES is not over-read. **`fig79` registered centrally by integration (leg 0)** — the leg shipped the figure but flagged that it had not edited this index; the registered script rebuilds it **byte-identical** (md5 `fde8e884…`). Secondary object O2 (a rigorous degree-4503 Gauss–Laguerre enclosure) is **routed to leg 312/APIA, not a new leg**. **Nothing was built; `requirements.txt` untouched; no ban lifted** — the leg read the re-posed radii-polynomial ban as *disjoint* (a flow enclosure proposes no function space, so it is not the "fourth space/basis") and **routed that reading to the user rather than acting on it**. **Mis-carry risk named by the leg itself: Taylor models unlock one ODE rung, not the compressible route** — and the compressible route is not the system Clay asks about. No link of the L1→L4 chain moved |
| Route-SDSS v1 (leg 313) — **PARKED, NOT MERGED** | Does leg 260's DSS obstruction survive **seeding** (steer item 3, which states the leg *answers and reports*, it does not lift the ban)? — gate answered **NO: it does not survive.** Leg 260's substantive obstruction ("Entry B's defining adjective UNSEEDED is incompatible with its object's only function space") holds in exactly **one unnamed realization** — a finite-box, unweighted `L²(dy)` trawl — and all four of §3.4's reasons dissolve, including the two it called "the finding". **(a)** weighted `L²((1+\|y\|)^{-s})`, crossing measured at exactly `s=1` (0.9→1.072 diverges, 1.1→0.933 finite). **(b)** all three ban reasons are **gCLM-only** while the target is NS. **(c)** the cost floor **rose** 27→≈33 legs where leg 260 predicted a fall | — | — | — | — | `fig76` **reserved** | **No files on `main`** — branch `leg/313-sdss-v1` @ `434b49a`, pushed as a branch, never merged; read it with `git show`, do not merge or build on it. **No ban lifted, re-posed or weakened; `plan_of_record.py` byte-identical to `origin/main`.** **Mechanism named (lesson 91): THE COMPACTIFICATION TRANSPOSITION** — the compactification that makes the norm finite carries `r^{-1+iκ}` into `(1-X)^{1-iκ}`, the identical form to clause (a)'s own difficulty, at the opposite end of the domain: **the defect is an invariant of the entrance, and can be moved but not deleted.** Priced in modes (`n ≈ 791 κ^0.954`, 823→14,149 at κ=1→20, vs 10 for a smooth control), plus a measured **1414.9×** far-field resolution penalty and DOF `4.64e8` = **23,182×** Phase 1's viscous rung. **Two obstructions found that are not leg 260's and must travel with any ruling:** the **seed set for the screened object is EMPTY** (Hou arXiv:2405.10916 fails the screen three ways) — availability, not impossibility; and **the only one that is a theorem**, Chae–Tsai's nonexistence for DSS solutions with time-periodic `V` under a decay hypothesis on `Ω=∇×V` (conclusion `V≡0`), this leg's exact object met in the rigidity direction, carried at summary level with whether it reaches the screened object recorded as **unknown, not guessed**. **MF3 changed this packet substantively**: re-run under the single-phrase shape, the absence survived but surfaced the Chae–Tsai result — four adverse links banked. A ban-scope observation (neither DSS entry names a search seeded from a numerical candidate) is reported as **a question about wording, which is the user's**. Zero L1→L4 links moved |
| Route-FUS v1 (leg 314) | The finite-unstable-spectrum condition (steer item 5): is it **provable**, **numerically checkable**, or **open**? — gate answered **yes** (a definite classification was produced), and the classification is **(iii) OPEN**, in two load-bearing parts. **(1)** The condition is **not realization-invariant** and arXiv:2509.14185 **names no realization** — as written it has no truth value to prove, disprove *or check*. **(2)** Once a realization is fixed, the residual obligation is a **high-frequency resolvent bound on `|Im µ| → ∞`** (Hardy–Mellin, or maximal dissipativity plus a relatively compact perturbation) — **a theorem, not a computation**; no certified count on a bounded box supplies it | Y | Y | Y | Y | fig77 | **Named mechanism (lesson 91): for this condition, numerics is a REFUTER, not a verifier.** Corroborated in four literatures rather than asserted: Barker–Zumbrun's certified count uses a winding radius `R = (√γ + ½)²` derived **analytically** — the computer works inside the disc, and *the disc is a theorem*; Gallay–Wayne buy finiteness by raising the weight; Chen–Hou sidestep the condition entirely. Xu arXiv:2607.19762's published dichotomy cited, not claimed: same CLM profile, maximal-`L²` smear vs origin-`H²` giving `σ_ess = {Re = −½}`, point spectrum exactly `{0,1}`. **Nothing built** — the construction route is named only, half A (bounded box) within repo tools, half B (unbounded tail) with none; and because the answer is **(iii)** rather than **(ii)**, the DM's construction clause is **not triggered**. **The gCLM measurement ban was walked term by term, found BINDING, and the leg redesigned itself around it** — arithmetic on banked numbers only, enforced by an **AST self-guard**, with its one 4.7 s cost probe declared and nothing from it banked. **This leg is also the one that caught the orchestrator's MF3 error**: it ran the control instead of taking the instruction on authority (`"self-similar" AND "blow-up"` → **251**, every ANDed query non-zero), and its **(iii)-OPEN branch rests on no query zero at all** — D4, its sole absence-based discriminator, rests on a multi-instrument sweep. One out-of-territory edit **flagged, not hidden**: a single §6 figure-registration line in the shared `writeup/build_figures.py`, its rebase conflict with leg 315's fig79 resolved **additively, both kept** |
| Route-CAPA v2 (leg 292) | Freshness audit of `capabilities.py` on 8 axes at HEAD — gate answered **NO**: one stale entry found, fixed, and the count reported; **zero modules missing**. 48 rows / 48 distinct modules / 48 `solver/*.py`, 0 missing, 0 ghost; test presence 0 empty and 0 absent; pass status **47/47 green** over a **5396.5 s** sweep; known-answer-gate presence **36/48 = 75%** | Y | Y | Y | Y | fig80 | **The repair is not the result — the latency is.** Leg 71 measured this same defect **~220 legs ago and could not fix it** (no test then loaded the module); leg 124 wrote exactly that test 53 legs later; **the fix then sat on disk unused for the remaining ~167 legs**. That measures this repository's **audit-loop latency**, not `capabilities.py`: leg 71's check lived in leg 71's runner, so nothing ever re-asked it. The stale entry: `solver/finite_support.py` cited `test_first_integral.py`, which contains **zero occurrences of the module's name** and so cannot fail when it breaks — repointed to `test_finite_support_adversarial.py`, `validated` left frozen. **The 12 magnitude-free rows were named, not rewritten** — supplying another leg's number from an audit chair is precisely the fabrication that field exists to stop. **Secondary finding banked, and it is a live trap for future legs:** leg 124's S10 gate can be turned red by *prose anywhere in the tree* — any `*.py` line carrying both the module stem and `import`, comment or docstring included — while the module stays byte-identical; **the leg's own explanatory comment tripped it**, and a CAUTION note is left beside the row. `test_advection_scope.py` green at **2512.2 s**, 47% of the sweep, and confirmed **genuinely slow, not degraded** (leg 71 measured 2363.7–3045.6 s on the same file). **S5 is plotted AS FOUND (1), not post-repair (0), so the repair cannot erase the finding.** Landing revalidation done by measurement, not assumption: `main` advanced ~30 commits under the leg, but `git diff 80c0cc4..origin/main` over `solver/` and `capabilities.py` is **empty**, so the sweep carries over. Figure renumbered `fig67 → fig80` (fig67 is leg 304's) — the ninth collision, caught before landing |
| Route-APIA v1 (leg 312) | Arbitrary-precision interval arithmetic (steer item 1), applied to re-measure two banked float64 numbers — gate answered **YES**: both moved, one of them in substance. **Leg 178, `T2_egm|E_egm`, n=128, γ=4, n_grade=96: gap `-230.7108027866` → `+0.4999999874556`** (1640 of 7824 quadrature nodes patched at 120 digits; `dim_kept` 122→126, 4 dropped→0). **Leg 176, N=1024 `rect_sigma`: `σ_min 0.09093626076` → `0.09079112560`** | Y | Y | Y | Y | fig73 | **The banked `-230.71` was never a measurement of the object — it was float64 catastrophic cancellation at θ~3e-31.** The leg's own `n_grade=48` cross-check had read `+0.49999975` all along, i.e. the contradiction was **already inside leg 178's own data** and unread for ~134 legs. The `σ_min` correction is the more quietly important one: the banked N=1024 value (`0.09093626`) sat **above** N=512's (`0.09080465`), breaking the ladder's monotone-non-increasing shape; the corrected value **restores it**, so a structural property was being masked by arithmetic. Apparatus is stdlib-only (`solver/interval_mp.py`, `decimal`/`fractions`, **no new dependency**), and its **13/13 adversarial battery caught three real bugs before any result was believed**: a missing ratio factor in an atan recurrence, bare `abs()`/unary `-` silently rounding to the ambient 28-digit default, and `Decimal(1)/Decimal(239)` computed outside any explicit context. **Scoped to magnitudes, not booleans** — the leg deliberately did **not** ask whether the corrected rows now *pass* their clauses; that is leg 329's question, and its precondition is this landing. **Neither correction touches the L1→L4 chain** — both source legs are exploratory, and the leg said so itself |
| Route-DWM v1 (leg 305) | Is BCG's `6.854×` dominance-window deficit **sharp** or **slack**? — gate answered **YES** (both endpoints reproduced through an independent path, and a per-constant width ledger produced naming the costliest constant). Endpoints reproduced by root-solving `D_{Z,1}` at 60 digits against BCG's own closed form: lower dev `3.33e-8`, upper `5.63e-9` (tol `5e-8`); γ-ceiling dev `2.52e-13` (tol `5e-13`); closed forms to `1e-57`; **T4 vs `\eqref{eq:rstar}` exactly `0`** over 12 γ spanning **both** of BCG's branches. Ratio is `(7+3√5)/2 = 6.8541019662…`, **not** `6.855` | Y | Y | Y | Y | fig82 | **Verdict: SHARP for BCG's argument as stated** — all **eleven** constants classify `EXACT_IDENTITY`, so the pre-registered SLACK branch (which requires ≥1 `ESTIMATE`) **cannot** trigger. Costliest is **`C1_c_lap = 2`**, the Laplacian's own derivative count: **[CORRECTED 2026-08-12, leg 338 — Route-LCB1, per `CORRECTIONS.md` §18.1 / leg 336: this clause originally read "largest elasticity (−13.708% of window per 1%)". That is false against the ledger's own `M2_pct_of_window_per_1pct` field — `C9_a1`'s elasticity, `−31.058%`, is `2.27×` larger in magnitude; `C1_c_lap`'s `−13.708%` remains correct as its own value and as the smallest move to close, a different metric, quoted unchanged below]** smallest move to close, **−42.705%**, to `(9−3√5)/2 = 1.145898`. **Named mechanism (lesson 91): the deficit is the distance between a DERIVATIVE COUNT and a DISCRIMINANT** — `r*` is exactly the smaller root of BCG's `R₁` radicand, the `P_s`/`P̄_s` saddle-node — so closing it means `ν(−Δ)^0.5729490169`, **a different PDE, not a sharper proof**. Seven of the eleven (`D_{Z,1}`/`R₂`) are **unreachable** because `r*` sits at a *stationary* maximum, measured via response exponent `p = 2.00` against `p = 1.00` for the four uncapped. **The pre-registered T6 FAILED and is reported as failed, not restricted** — its `0.899` deviation is that stationary maximum's own signature; T6b was added and declared as *additional*. **The conditioning trap was hit twice and diagnosed both times before belief:** BCG's l.603 cancellation gives float `|k(1)−1| = 1.381e-07` (leg 302 measured `1.29e-07`) against exactly `0` at 60 digits; and a **self-inflicted** second instance where T5 first failed at `1.0954e-22` because the probe sat at `r = 1+1e-45`, measuring the leg's own offset through a linearly-vanishing radicand. Three real code defects fixed, including a T2 γ-ceiling failure that was `1e-30` arithmetic dust flipping BCG's branch selection — **not** a contradiction of leg 300. **Route is COMPRESSIBLE (BCG, γ=7/5), not the system Clay asks about; no L1→L4 link moved** |
| Route-BVRRV v1 (leg 233) | Re-grading the leg-205 caller census against the **repaired** `solver/boussinesq_rescaled.py` (post-repair commit `8e753a02`) — gate answered **YES**. Clause (a): the silent-fabrication class is **gone, 18 → 0 SILENT_WRONG** across the 42 graded call sites (OK 32 → 42, RAISED 11 → 19), and the 18 former silent-wrong calls now split 13 RAISED / 5 OK-with-modulation. Clause (b): **340,233 calls compared live and bit-identical, 0 moved** (335,092 artifact calls over six sweeps + 5,141 test-suite calls), against leg 221's 256,233 headline — an excess of 84,000. The three OK → RAISED transitions were adjudicated **3 JUSTIFIED_REFUSAL / 0 UNJUSTIFIED_REGRESSION**, margins `2.7924e-07`, `2.7924e-07`, `2.8868e-04` against tol `5e-4`, with singular-value ratios `4.1e-16`, `3.9e-15`, `2.4e-02` | Y | Y | Y | Y | fig101 | [T](4_p2_lottery/TECHNICAL_P2_ROUTEBVRRV_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTEBVRRV_V1.md) — **the quartet arrived late and by a different hand: B/T, E and fig101 were added by a DOCS-lane rework unit, not by leg 233's original landing** (`43dce32`), which banked only the runner and the curated JSON. The rework closed it **from banked data alone** — `experiments/p2_route_bvrrv_v1_postrepair_evidence.py` passes **52/52** checks rebuilt from `writeup/data/p2_route_bvrrv_v1_postrepair.json`, with **no re-run** of the ~1.9 h four-way-parallel sweeps and no number written that the artifact does not already hold. **The load-bearing number is not the zero but its explanation:** `cap_binds = 0` over all 340,233 calls is evidence only because the minimum window occupancy is **4 nodes against a `min_points` floor of 3**, so the cap could have bound and did not (lesson 90). **The leg's negative construction stays in the artifact:** the auditor found a fabricated zero in its own instrument — a residual field initialised to `0.0` and never written — and the repair is instrumented on only **2 of 6 artifacts, 64 of 340,233 calls**, carried as an explicit OPEN limit rather than smoothed over. A **journal-vs-JSON rounding disagreement** on the lesson-90 control (`2.0007346`/`3.673e-4` vs `2.0007759522991355`/`3.8798e-04`) is recorded neutrally in the TECHNICAL and routed to the Decision Maker, not adjudicated by the DOCS lane. **Verification-lane result: no L1→L4 link moved, Clay stays ~0.05%** |
| Route-CLOC v1 (leg 381) | Is the localisation gap **exactly** as `CLAY_OBLIGATIONS.md` §4 states it? — gate answered **YES** ("the reviewer's arithmetic survives with the DSS modulation handled, and confirms the bounded-energy reading against the primary text"), **with one REFUTED side-clause, one labelling correction and one REPAIRED derivation step**. Headline: **the DSS energy exponent equals the SS one — ratio `0.9999998844`, i.e. no factor** (`0.499999942` vs `0.500000000000`), and the reason is structural, `λ^ℤ` being a subgroup of the same scaling group. The modulation is **not** negligible: `G(s)` swings by **2.99** within one period `2 log λ` (measured period `1.0574` vs `1.0613`, `0.36%`), and dropping it biases a naive OLS fit to `0.487628` — **2.47% off**. Bounded energy **confirmed verbatim** as Fefferman's numbered condition (7); **"with `f ≡ 0`" REFUTED** (it belongs to the existence statements (A),(B)); the `ℝ³` breakdown statement relabelled **(C)**, not "(b)". Clay clause ledger: **4 CONFIRMED, 1 CORRECTED, 1 REFUTED of 6**. Object checks: DSS symmetry `1.14e-15`, divergence-free `8.87e-12`, change-of-variables cross-check in physical `x`-space `4.19e-15` | Y | Y | Y | Y | fig104 | [T](4_p2_lottery/TECHNICAL_P2_ROUTECLOC_V1.md) · [B](4_p2_lottery/BLOG_P2_ROUTECLOC_V1.md) — B/T added by the leg itself as a **disclosed territory deviation** (its spec named four files; the §6 pair requirement needed two more). **E and F arrived later and by a different hand:** leg 381 **drew no figure** and said so, leaving fig99 unused; the gap went on the record as an audit finding and was closed by a DOCS-lane support pass (`176acd1`) that added `experiments/p2_route_cloc_v1_evidence.py` and **fig104** from banked data only — the runner untouched, `writeup/data/p2_route_cloc_v1.json` read-only, every plotted value one leg 381 had already banked. **fig104, NOT fig99** — fig99 was freed by the omission and reallocated to leg 386. Left open by the leg's own naming: `CLAY_OBLIGATIONS.md` §7 (the Millennium Prize rules) unchecked, §1–3/§5–6 unverified, and the composed-`δ` question against leg 382's enclosure settled by neither leg. **No localisation attempted, no obligations file edited; Tier-2-ceiling verification, no L1→L4 link moved, Clay stays ~0.05%** |
| Route-T4 v1 (leg 393) | Reproduce at least one published enclosure row of `arXiv:1902.00384` **using apparatus named and shown C1-compliant in the unit's own pre-registration** — answered by the pre-committed **`STOP`, branch (c)**: the paper is certified by **exactly the banned apparatus**, and **both certified rows are 2D lifts**. **W2 STANDS, STRENGTHENED; W6 UNTOUCHED.** The `STOP` is the C1 naming requirement working as written, not a budget failure — the unit could not name a compliant apparatus because the paper does not use one, and it says which clause it read that from | Y | Y | **GAP: neither, wave unit** | Y | fig110 | `experiments/journal/leg_393.md` (pre-registration Part I committed before the first script existed) · `experiments/p2_route_t4_v1.py` · `writeup/data/p2_route_t4_v1.json` · `experiments/p2_route_t4_v1_evidence.py`, **registered in `P2_EVIDENCE`**, redraws fig110 from the banked JSON alone (no network, no PDF, no `.mat` at rebuild time). **VERIFIED by `V-W2` (`594ff89`)**, whose items (1)/(2) re-fetched the primary artefacts and matched SHA-256 against the banked digests. Landed `2c87244`. **Lane T is DEFERRED on this measurement — the lane's own unit demoted the lane. No L1→L4 link moved** |
| Route-T6 v1 (leg 394) | Read the **full text** of the seven papers leg 348 classified from title/abstract level: does each **confirm**, **strengthen** or **UNDERCUT** leg 348's recorded classification? — answered **7/7 full texts obtained, 2 UNDERCUT / 4 strengthen / 1 confirm, with 0 `UNREACHABLE`, 0 `THROTTLED` and 0 zeros**, each verdict resting on a deciding sentence quoted verbatim and located by section and page. UNDERCUT 1 independently replicates `T4`'s finding from the authors' **prose**; UNDERCUT 2 removes one row from leg 348's `domain_census`. **The obstruction is NOT refuted — its evidence base is thinner than the record said, not wrong**, and the row it removes does not carry W2 | Y | Y | **GAP: neither, wave unit** | **Y — registered `D-REPAIR`, wave 5** (as a *verification*, no figure) | none allocated | `experiments/journal/leg_394.md` (§0 pre-registration and the §0.3 verdict rules committed before the first network call) · `experiments/p2_route_t6_v1.py` · `experiments/p2_route_t6_v1_adjudicate.py` · `writeup/data/p2_route_t6_v1.json` + `p2_route_t6_v1_leg348_lock.json` (the lock file pins leg 348's classification as it stood **before** this unit read anything) · `experiments/p2_route_t6_v1_evidence.py` **was absent from `build_figures.py`'s `P2_EVIDENCE` list** — recorded here as a finding, deliberately left unrepaired while `V-W3` measured registration coverage. `V-W3` returned (`2b8755e`) and the debt was discharged by unit **`D-REPAIR`** (wave 5): the script is **now registered**, as a verification entry with **no figure**. It needs seven full-text PDFs that are **gitignored**, so on a checkout without them the rebuild prints `SKIP … (7 required input(s) absent)` and **counts it as not verified** — it is never silently passed. **VERIFIED by `V-W2`**, which banked one nuance **unreconciled**: the ground for UNDERCUT 2 was the **Conductor's** wording, not `T6`'s. Landed `e7db624`. **No L1→L4 link moved** |
| Route-T5 v1 (leg 395) | The C1 sweep, an obligation created by `RULING_BAN_WORDING_2026-08-13.md` itself: across the record's ban-citing refusals, is each **APPARATUS-based** or **REALIZATION-based**? — answered **PASS**, **7 refusals, APPARATUS 5 / REALIZATION 2**, each deciding sentence quoted verbatim and located by file and line. **Exactly 2 are re-openable under C1, and the sweep leaves them UNRANKED by its own pre-committed reading (a)**: leg 348's Galerkin-plus-tail build, and **leg 315's `O1`** Taylor-model flow-map enclosure that *"needs no function space"* — **the genuinely new item, and it points at LANE V, not Lane T. Leg 257 is NOT re-openable** (a fourth *space*, not a fourth *apparatus*), which is the distinction the ruling turns on | Y | Y | **GAP: neither, wave unit** | none | **no figure by design** — the output is a list, and the unit's own pre-registration forbids ordering it by anything but leg number | `experiments/journal/leg_395.md` (pre-registration immutable once written, committed in the pre-sweep commit) · `experiments/p2_route_t5_sweep.py` · `writeup/data/p2_route_t5_v1.json`. **VERIFIED by `V-W2`**. Landed `a6f0c38`. **A sweep ranks nothing and re-opens nothing** — the leg says so itself; the ranking is the Conductor's, and it was `T5`'s `O1` finding that put Lane V on the board. **No L1→L4 link moved** |
| Verify-Wave1 v1 (`V1`, wave 2) | Independent re-derivation of wave 1's five claims (`T1`, `T2`, `R0`, `R1`, and PROG-R4's `M3`) from banked JSON and landed evidence scripts **alone** — answered **all five reproduce**, and **`M3 = DELIVERED` SURVIVES** `U5`'s 57% seed overlap, which was the claim most likely to fall. **Two defects banked and left unreconciled, not repaired** — a verifier that fixes its own findings has destroyed the measurement | Y | Y | **n/a — verification lane** | Y (the re-derivation script **is** the evidence) | none — verification produces no curve | `experiments/journal/verify_wave1.md` · `experiments/p2_verify_wave1_v1_rederive.py` · `writeup/data/p2_verify_wave1_v1.json`. Landed `2fb399f`, **UNVERIFIED** (a verifier is not itself verified unless a later wave audits it; `V-W3` audits `V-W2`, not this one). **Verification is not movement toward Clay: no link moved, Clay stays ~0.05%** |

| PROG-R4 unit `E` (leg 380, **wave 1**) | **The H-hard diagnostic — PASS in its pre-committed wording: all three diagnostics RETURN**, each with a planted control that fires both ways. Direct-seeded at the eight published Lucas–Kerswell Table IV rows: **converged twice, recovered no named row**, both convergences below diagnostic (1)'s own `\|s\|` shelf; the positive control passes **through `E`'s own predicate**, which is what makes the non-recovery a measurement rather than a broken instrument. Diagnostics `PULL_TO_LOW_S` and `MIXED`. **Pre-committed branch `E-iii` fired.** `G1` stays `UNDER-RESOURCED` **and was not written to** — a hand-placed seed at published coordinates is not a mined seed | Y | Y | Y | Y | fig109 | `experiments/journal/prog_r4_e.md` · `experiments/programme_r4/e_hhard_diagnostic.py` · `writeup/data/p2_prog_r4_e_v1.json` + `experiments/programme_r4/e_hhard_ledger.json` / `e_hhard_converged_orbits.npz` · [T](4_p2_lottery/TECHNICAL_P2_PROGR4_HHARD.md) · [B](4_p2_lottery/BLOG_P2_PROGR4_HHARD.md) · `writeup/figures/fig109_prog_r4_hhard.py` **is** the evidence script (registered in `P2_EVIDENCE`; 17 self-checks, exits non-zero if the JSON stops supporting a panel). Landed `d0d72b1`. **VERIFIED by `V-W3`** on the headline (reproduces 6/6 from the banked JSON); `V-W3` also **REFUTED the `~8×` cost overrun** attached to this unit — it was a wall-vs-core units error, and `E` came in **under** its commissioned model — and located four further defects in the record around it (D2–D5), repaired by wave 5's `D-REPAIR` as marked correction blocks in the journal. **This row was withheld until `V-W3` returned**, so that adding it could not disturb a live measurement. **Ceiling TIER 2, no `L1→L4` link moved, Clay ~0.05%** |
| Verify-Wave2 v1 (`V-W2`, **wave 3**) | The wave-2 verifier: does each of `T4`'s, `T6`'s and `T5`'s claims reproduce **exactly** from banked JSON and landed evidence scripts alone? — answered **ALL FOUR ITEMS REPRODUCE**, with items (1)/(2) re-derived from **re-fetched primary artefacts whose SHA-256 matched the banked digests** — measurements, not transcription checks, and the `.mat` fields bitwise. Banked **one nuance unreconciled and did not repair it**: the *ground* for `T6`'s UNDERCUT 2 was the **Conductor's** wording, not `T6`'s. `T1`'s owed machine record **DISCHARGED**, mutation-tested four ways | Y | Y | **n/a — verification lane** | Y (`p2_verify_wave2_evidence.py` **is** the evidence) | none — verification produces no curve | `experiments/journal/verify_wave2.md` (§§0–2 committed before any number was computed) · `experiments/p2_verify_wave2_evidence.py` · `writeup/data/p2_verify_wave2_v1.json`. Landed `594ff89` — the **one unit of four that survived wave 3's host process exit**, and it survived because it was committed during the run. **VERIFIED by `V-W3`** (gate item (3), both parts, from re-fetched primaries). **This row was withheld until `V-W3` returned.** **Verification is not movement toward Clay: no link moved, Clay stays ~0.05%** |

### In-flight figure allocations (orchestrator-maintained, §6)

Eight figure collisions have happened in four cycles, and every one had the same cause:
the orchestrator allocates a number in a dispatch brief, and that number then exists only
inside a running agent's context, where no other leg can see it. This table is the fix.
**A number is claimed the moment it is allocated at dispatch, not when the figure lands.**
Legs must not pick their own numbers; integration allocates, and records here.

**RECONCILED 2026-08-18 by unit `D-REPAIR` (wave 5)**, discharging the Conductor debt held open
while `V-W3` measured registration coverage. **NOTHING BELOW IS RE-ADJUDICATED.** Every cell in the
`State` column is a mechanical fact — `git ls-files writeup/figures/`, and `ast`-parsed membership of
`P2_EVIDENCE` in `build_figures.py` — not a judgement about whether a leg landed. Where the landed
table above and the files on disk say different things, **both are shown and neither is overruled
here**: that is the Conductor's, and it is flagged in this unit's journal §8.

| Figure | Leg | Slot | State, as at 2026-08-18 (mechanical) |
|---|---|---|---|
| `fig72` | 320 (MTSC) | — | **`.png` IS tracked on `main`** (`fig72_route_mtsc_v1_death_mechanisms.png`), no rebuild script, **not** in `P2_EVIDENCE`. The landed row above still reads *PARKED, NOT MERGED* — **was `reserved, no files on main`, which is no longer true** |
| `fig75` | 301 (FSB) | — | **still reserved** — no `.png`, no script, not in `P2_EVIDENCE`; landed row reads *PARKED, NOT LANDED*. Unchanged |
| `fig76` | 313 (SDSS) | — | **LANDED**: `.png` tracked and `p2_route_sdss_v1_evidence.py` **registered in `P2_EVIDENCE`** ("landed late under the cycle-11a caveat"). The landed row above still reads *PARKED, NOT MERGED* — **was `reserved, no files on main`** |
| `fig78` | 326 (CTRX) | E | **nothing on `main`** — no `.png`, no script, no row in the landed table. **Was `leg live`; no leg is live** |
| `fig81` | 329 (EGMF) | A | **`.png` and `fig81_route_egmf_v1_evidence.py` both tracked**, script **NOT** in `P2_EVIDENCE`, and **no row in the landed table**. **Was `leg live`** |
| `fig83` | 306 (SSE) | F | **nothing on `main`**, no row in the landed table. **Was `leg live`** |
| `fig84` | 318 (DECR) | D | **`.png` tracked**, BLOG+TECHNICAL present, **no rebuild script**, not in `P2_EVIDENCE`, **no row in the landed table**. **Was `leg live`** |

**What this table is for now.** Under CONDUCTOR mode (since 2026-08-13) figure allocation for a wave
is stated at dispatch and tracked in `reports/ORCH_STATE.md`, **not here**. This table is therefore
**closed to new allocations** and kept only as the register of the seven numbers the four-leg-parallel
setup left open. **No leg has been live since the 300s; the record is at leg 399.**

Landed and no longer in flight: `fig73` (leg 312), `fig77` (leg 314), `fig79` (leg 315),
`fig80` (leg 292), `fig82` (leg 305). Also landed since: `fig110` (leg 393), in the table above.
Legs that were live with **no figure**, deliberately: 324 (P2SPF, slot G) and 328 (ORC5, slot I) —
both record/correction legs, and a registered "none" is a legitimate §6 quartet entry.
~~**`fig85` and up are unallocated; `fig85` is the next free number.**~~ **STALE and corrected:**
`.png` files exist through **`fig110`**, so **`fig111` is the next free number.**
`fig107`'s registration gap — flagged here while `V-W3` measured it — **is now closed**: the drawing
script `writeup/figures/fig107_prog_r4_m3_shift_strata.py` is registered in `P2_EVIDENCE`.

**The instrument that answers this question is now executable** —
`.venv/bin/python writeup/check_figure_coverage.py` prints, mechanically, which cited figures
`build_figures.py` rebuilds and self-checks and which it does not, and exits non-zero while any
cited figure is uncovered. **It reports far more uncovered figures than this table lists** (the
pre-`D-REPAIR` count is in that script's own commit message); **that is a finding for the Conductor,
not a repair this unit was commissioned to make**, and it is written up in its journal §8.

**Reconciliation note, 2026-08-11.** This table and the DM's draft-time FIG-TABLE in
`DIRECTION.md` briefly disagreed about leg 326: this table's dispatch mirror had said
`fig85`, the FIG-TABLE said `fig78`. **The FIG-TABLE is authoritative at draft time and the
dispatch briefs went out carrying `fig78` (326) and `fig81` (329)**, so those are the live
allocations and this table is corrected to match. The two registers exist for different
moments — the DM allocates when a spec is drafted, integration confirms at dispatch — and
when they disagree, **what the dispatched brief actually said wins**, because that is the
number the running agent can see.
Leg 314 took `fig77` on landing having read this table's predecessor correctly — it recorded
`fig69`–`fig76` as taken or reserved and took the next free number rather than guessing,
which is the discipline working as intended.

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
   `writeup/figures/fig60_route_port_v2.png`). **✅ CLOSED by leg 375**:
   `writeup/4_p2_lottery/BLOG_P2_ROUTEPORT_V2.md` now exists, every numeric claim in it
   traced directly to `TECHNICAL_P2_ROUTEPORT_V2.md` and
   `writeup/data/p2_route_port_v2_reach.json` with no new measurement or re-derivation, and
   the adverse finding (+0.47 dec/unit ρ, 63× worse at `ρ=10` vs `ρ=6`) stated as the
   headline, unsoftened. The quartet-gap list's last open clause is now closed — the list
   stands at **0 open items**. The row above reads `Y` / `[T]·[B]`.
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
   **Re-verified by leg 372 (Route-IDXB), item CLOSED-WITH-CITATION, not re-touched.**
   `writeup/4_p2_lottery/p2_weight_repairs_v1_evidence.py` is confirmed present on disk and
   runnable, landed in `9d9b7ea` and re-confirmed correct by leg 138. Item 9 was already fully
   closed before this leg started; per this leg's own gate, recreating it would be a duplicate
   and a FAIL, so nothing was written. Bank the citation and move on.
10. **Route-KA v1 (leg 61) has TECHNICAL but no BLOG, no `*_evidence.py` and no figure** (found
   by leg 108). Runner `experiments/p2_route_ka_v1_kawahara.py` and curated data
   `writeup/data/p2_route_ka_v1_kawahara.json` are both present, and this is the leg that
   reproduced a *published* radius end to end — the repository's one external known-answer check
   of the interval pipeline, so per lesson 76 it earns the same care as a headline result. 3 of
   5 quartet pieces present. Not fixed here: BLOG prose and figure selection are claim-bearing.
   **`E` closed by leg 372 (Route-IDXB): `experiments/p2_route_ka_v1_kawahara_evidence.py`
   reads only `writeup/data/p2_route_ka_v1_kawahara.json` (no solver import, no re-run) and
   asserts 8/8 checks — Reading A (CLN's `r0` is a certified radius of ours, YES), Reading B
   (the pre-committed window's shortfall, `3.3531x`/`0.5254` decades, NOT smoothed away), both
   nominated explanations for that shortfall FALSIFIED at their banked magnitudes (trace
   projection `1.0252x` of the needed `3.3387x`; the discarded tail `2.978` decades short),
   the resolution sweep (`Y0` flat, `r_min_Hl` tracking `sqrt(2N+1)`), and the poisoning
   control (linear across 8 decades, fails to close at the largest kick).**
   **`F` was never a genuine gap: `TECHNICAL_P2_ROUTEKA_V1.md`'s own header says, verbatim,
   "No figure: this is a known-answer audit and the established convention is that such legs
   register none" — the same by-design class item 6 already records for Route-D's
   advection/literature-scope legs, and the same class the NKR half of item 13 records below.
   Leg 372 does not claim a new figure number for this route: this repo's own standing
   practice ("legs must not pick their own numbers; integration allocates") is respected, and
   no allocation was owed to a route whose own header declares none needed. Item 10 now
   stands for the BLOG clause alone — prose, outside a scripts/figures-only remit.**
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
   **Both halves CLOSED by leg 372 (Route-IDXB), in 322/327's shape.**
   **M2P**: `experiments/p2_route_m2p_v1_promotion_evidence.py` imports no solver module and
   reads only `writeup/data/p2_route_m2p_v1_promotion.json`, rebuilding `fig61` byte-identical
   across two reruns (`sha256sum` match). Its one deviation from the original `build_figure()`
   is deliberate: the original's panel (a) re-solves a Newton iterate for its dashed line — a
   fresh solve, which this evidence script must not do because the raw coefficient array is
   not itself banked. Leg 372's panel (a) instead plots ONLY Chen's closed form
   `Omega(x) = -2bx/(x^2+b^2)^2` (evaluating a fixed analytic formula at the banked constant
   `b`, not solving anything) and annotates it with the banked `n=1201` Newton-reconstruction
   numbers (`c_l -> 0.333333435`, abs err `1.02e-07`) as text rather than a re-solved curve.
   Registered in `writeup/build_figures.py`'s `P2_EVIDENCE` list.
   **NKR**: `experiments/p2_route_nkr_v1_repair_evidence.py` reads only
   `writeup/data/p2_route_nkr_v1_repair.json`, no solver import, and asserts 6/6 checks —
   gate (a)'s false-accept count (`21/105` pre-repair to `4/105` post, `17` rejected, `0`
   clean-input outcomes moved, the `4` residual named not dropped), gate (b)'s zero regression
   (`4626/4626` comparisons bit-identical, `worst_ulps=0`), gate (c)'s shared-guard agreement,
   and the overall answer (`YES` on (b) and (c), `NO` on (a)). No figure is produced, matching
   the route's own by-design "no curve to plot" header — not registered in `P2_EVIDENCE` for
   that reason, same as the Route-KA v1 script above.

Route-TC is no longer in progress: it landed as leg 53 and has a complete quartet, indexed in
the Arc 4 table above.

## Retired from `STATE.md` under §3j retirement (added 2026-08-18)

*A unit's row leaves `STATE.md` once it is LANDED **and** VERIFIED, and arrives here as one line —
unit, gate answer in the gate's own words, SHA, verifier. `STATE.md` keeps live units, the next wave
and open user items. Full detail for every row below is in the Arc 4 table above and in the unit's
journal; nothing here is a summary written after the fact.*

| unit | gate answer, in the gate's own words | SHA | verifier |
|---|---|---|---|
| **`L2′`** / leg 397 (Lane L) | **GATE `YES`** — the failing hypothesis is **named, quoted and located** for **all 18** techniques: **9 `FAILS` / 8 `FAILS-BY-CONSTRUCTION` / 1 `SATISFIED`**, and **ZERO could supply `α > 1.5` even in principle**. `α` is a **pin, not a gap**: paying leg 381's bill destroys the object it is for. W4 clause (a) SHUT; §6(i) **NOT** retired. | `1493e5e` | `V-W4` (`b46ee4d`) — REPRODUCES, with `D5`/`D6` on the pin's provenance and ESŠ `UNREACHABLE` at primary |
| **`V3`** / leg 399 (Lane V) | **GATE `YES` on 1 row of 9.** `arXiv:2509.25116` passes **both** of leg 174's clauses and had never been graded here; 8 `NO` with the failing clause quoted. **The object is NOT a finite-time singularity.** Cell OCCUPIED; **W3 stands anyway** (ruling Q1 — two different claims). | `16ba44e` | `V-W4` (`b46ee4d`) — REPRODUCES at re-fetched full text; 4 quote defects, none material; **one NEW user escalation** |
| **`T4`** / leg 393 (Lane T) | **`STOP`, pre-committed branch (c).** `arXiv:1902.00384` is certified by **exactly the banned apparatus**, and **both certified rows are 2D lifts**. W2 STANDS, STRENGTHENED; W6 UNTOUCHED. | `2c87244` | `V-W2` (`594ff89`) |
| **`T6`** / leg 394 (Lane T) | **7/7 full texts — 2 UNDERCUT / 4 strengthen / 1 confirm; 0 `UNREACHABLE`, 0 zeros.** The obstruction is **NOT refuted** — its evidence base is thinner than the record said, not wrong. | `e7db624` | `V-W2` (`594ff89`) |
| **`T5`** / leg 395 (Lane T) | **PASS** — the C1 sweep, an obligation of `RULING_BAN_WORDING_2026-08-13.md` discharged. **7 refusals: APPARATUS 5 / REALIZATION 2.** 2 re-openable under C1, UNRANKED (leg 348's Galerkin-plus-tail, leg 315's `O1`); **leg 257 is NOT** — fourth *space*, not *apparatus*. | `a6f0c38` | `V-W2` (`594ff89`) |
| **`T1`** / leg 391 (Lane T) | **`yes`** — the ban-wording escalation packet. The user ruled **none** of its three questions; `RULING_BAN_WORDING_2026-08-13.md`. The machine record is **DISCHARGED**. | wave 1 | `V1` (`2fb399f`) |
| **`T2`** / leg 392 (Lane T) | **`UNDER-RESOURCED`, not `no`** — and it named its own successor, **`T2″`**. | wave 1 | `V1` (`2fb399f`) |
| **`R0`** (Lane R, wave 1) | Metric pre-committed before optimisation; **the inference from its own table is RETRACTED** — ~~*"Lane R's first measured win"*~~. The standing metric survives: **ORBITS NEW TO THE PROGRAMME PER WORKER-HOUR**. | wave 1 | `V1` (`2fb399f`) |
| **`R1`** (Lane R, wave 1) | **CLOSED against itself** (+0.45 pp): the numbers confirm exactly, but U5 had already collected the win. | wave 1 | `V1` (`2fb399f`) |
| **`V-W2`** (wave 3, verification) | **ALL FOUR ITEMS REPRODUCE**, items (1)/(2) from **re-fetched primary artefacts whose SHA-256 matched the banked digests** — measurements, not transcription checks. Banked one nuance unreconciled: the *ground* for `T6`'s UNDERCUT 2 was the **Conductor's** wording, not `T6`'s. `T1`'s owed machine record **DISCHARGED**, mutation-tested four ways. | `594ff89` | `V-W3` (`2b8755e`), item 3 *verify the verifier* — **CONFIRMED**, incl. an independent re-fetch-and-hash of all three sources |
| **`E`** (wave 1, Lane R instrument) | **PASS in its pre-committed wording** — all three diagnostics RETURN, each with a planted control firing both ways. **Branch fired: `E-iii`.** 16 attempts at the eight published Lucas–Kerswell rows: **2 converged, 0 recovered any named row**, both convergences below diagnostic (1)'s 0.15 shelf. Control **R** is load-bearing — it proves the predicate **can** return a recovery. `G1` stays `UNDER-RESOURCED` **and was not written to**. | `d0d72b1` | `V-W3` (`2b8755e`), item 1 — **CONFIRMED**, 16 rows recounted off `diagnostic_3.attempts`. **The gate answer is verified; the RECORD'S COST CLAIM about it was REFUTED** (item 2, the `8×` units error) and corrected, and `V-W3`'s own epoch figure was then corrected by `D-REPAIR` (`036e56d`) — `E` used **+1.9% MORE** epochs/attempt, not 2.3% fewer |

- **`L5`** (leg 400, Lane L) — W4 clause **(b)** measured **SHUT**: gate `NO`, threshold-free, `c_mod = 869.288` per unit similarity time, ρ-exponent `+1.085e-04`. **VERIFIED** by `V-W5` (leg 403) 2026-08-18 — arithmetic only. Ceiling: Tier 2, float64, **SYNTHETIC** profile. `WALLS.md` W4; `CORRECTIONS.md` §34, §35. Row retired from `STATE.md` 2026-08-18 under §3j.
- **`V-W4`** (verification of wave 4) — **PASS**, all five gate items reproduce; both wave-4 artefacts regenerate bit-identically from re-fetched primaries. **6 defects + 1 note, none changing a verdict** (`CORRECTIONS.md` §33); repaired by `V5` as `_v2` deltas, `_v1` untouched. Row retired 2026-08-18 under §3j.

## Views of the record (not sources — the record is the source)

| view | what it shows | regenerate |
|---|---|---|
| `writeup/ROUTE_MAP.html` | Decision tree of every route to a Clay answer: closed by measurement / live / in flight / never explored, plus the W4 clause table and the wall ledger. | **Never automatically.** Procedure and the reasons in `writeup/ROUTE_MAP.md`. A Conductor FLAGS it stale in the integration commit; it does not rebuild it. |
| `writeup/papers/` | Three drafts aimed at refereed venues — P1 selection bias, P2 the α-pin pincer, P4 the methodology record — each with a `STATUS.md` enumerating blockers BEFORE drafting. | **A paper is a VIEW of the record, never a source. No unit may cite one.** Contract and the honesty rules: `writeup/papers/README.md`. |

## Arc 5 — `5_outpaced/` (the field answered first; the 2026-09-08 claim recorded at primary)

| Route | Gate / headline | R | D | B/T | E | F | Docs |
|---|---|---|---|---|---|---|---|
| Outpaced (legs 413–416) | The forced 3D Navier–Stokes blowup claim, as reported, and what it does to this programme's walls | — | Y | Y | Y | — | [T](5_outpaced/TECHNICAL_OUTPACED.md) · [B](5_outpaced/BLOG_OUTPACED.md) — **UNVERIFIED under §3f** |

## Arc 6 — `6_adjudicated/` and `6_reproduction/` (the claim read at primary, then reproduced)

| Route | Gate / headline | R | D | B/T | E | F | Docs |
|---|---|---|---|---|---|---|---|
| First pass, §3f SOLO (legs 417–422) | The statement adjudicated at primary (**(D) is claimed**, `A6-D` dead); the Lean censused at source; **`W4` does not break** under the ported mechanism, measured twice | Y | Y | Y | Y | fig112 | [T](6_adjudicated/TECHNICAL_ADJUDICATED.md) · [B](6_adjudicated/BLOG_ADJUDICATED.md) — **UNVERIFIED** |
| Second pass, §3g CONDUCTOR ×5 (legs 423–434) | **Read all 166 pages twice; 58-node spine re-derived, 10 nodes `VERIFIED` blind; Lemma 4.8's profile instantiated from the paper's schedule (constants, exponents, datum, tail stress reproduce to 10⁻⁹; closure and cone live at `λ ≲ 3·10⁻⁴`, the outer-edge powers on a `10⁻⁶⁹` collar); the Lean measured (`NOT-ESTABLISHED` kernel, statement strictly weaker than Thm 1.1); wave 4's adversary faked 11 of 12 signals.** Nothing contradicts the manuscript; nothing proves it; no wall moved | Y | Y | Y | Y | fig113, fig114 | [T](6_reproduction/TECHNICAL_REPRODUCTION.md) · [B](6_reproduction/BLOG_REPRODUCTION.md) · [evidence](6_reproduction/reproduction_evidence.py) — Conductor-written answers **UNVERIFIED**; ten spine nodes **VERIFIED**. Ceiling **TIER 2**, no `L1→L4` link moved, **Clay ~0.05%** |

## Arc 7 — `7_confirmation/` (the Lean kernel run to completion, and the construction wave that produced nothing)

| Route | Gate / headline | R | D | B/T | E | F | Docs |
|---|---|---|---|---|---|---|---|
| Confirmation, §3g CONDUCTOR ×5 (legs 436–440) | **The kernel check is GREEN and `VERIFIED`: on one pin (`8937a8f4`), in THREE environments and by TWO independent kernels (Lean and nanoda 0.4.17), both exported theorems are accepted with `[propext, Classical.choice, Quot.sound]` and `sorryAx` unreachable.** **Since 2026-09-11 this no longer rests on the published olean cache: a FOURTH run (`K1` phase C) rebuilt mathlib from source with `lake exe cache get` never invoked — 8370 `Built Mathlib.`, 0 `Replayed` — and returned the same axioms byte for byte.** It confirms the Lean project proves what its own statements say — and those statements are Fefferman (C)/(D), **strictly weaker than Theorem 1.1**. Olean INTEGRITY established, PROVENANCE to labelling only, SEMANTIC MATCH **CLOSED 2026-09-11** by that rebuild. `K3`'s construction wave: the blind adversary faked **all five** live gates — **zero surviving evidence in either direction**, a finding about the GATES, not the manuscript | Y | Y | Y | Y | fig115 | [T](7_confirmation/TECHNICAL_CONFIRMATION.md) · [B](7_confirmation/BLOG_CONFIRMATION.md) · [outsiders](7_confirmation/CONFIRMATION_FOR_OUTSIDERS.md) · [evidence](7_confirmation/confirmation_evidence.py) · [note: five gates, five fakes](notes/PREREGISTERED_GATES_FAKED.md) — `K1` **VERIFIED** by a blind agent; everything Conductor-written **UNVERIFIED**. Ceiling **TIER 2**, no `L1→L4` link moved, **Clay ~0.05%**. **No position on priority** |

