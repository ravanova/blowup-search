# Writeup — Evolutionary & rigorous search for Navier–Stokes-type blow-up

The **self-contained, banked writeup** of the project: an honest, long-shot attempt
at the Navier–Stokes blow-up problem via singular-profile / self-similar research.
Every number quoted and every figure is rebuilt from the small committed files in
[`data/`](data/) — **no raw logs, no re-run of any sweep, GA, or solver needed.**

Only a *rigorous proof* (Tier 3 / Level 3) would resolve the Clay problem; nothing
here does. The realistic prize is **novel toy-model singularity research** plus a
tiny Clay "lottery ticket." Each note states its own honest ceiling.

## How this folder is organized

Documents are grouped into four **numbered arc folders** (chronological). The
shared **build layer stays central**: [`data/`](data/) (committed inputs),
[`figures/`](figures/) (rebuilt outputs), and the two cross-arc builders
[`build_figures.py`](build_figures.py) / [`curate_evidence.py`](curate_evidence.py).
Each arc folder holds its own `TECHNICAL_*` / `BLOG_*` notes **and** the
`*_evidence.py` scripts that rebuild that arc's figures from `../data/`.

```
writeup/
  README.md                     <- you are here (the index)
  data/  figures/               <- shared, central (never moved)
  build_figures.py              <- figs 1–7 from data/
  curate_evidence.py            <- (re)curate data/ from raw logs (needs experiments/)
  1_gclm_1d/       the completed 1D gCLM pipeline (Level-0/1)        figs 1–5
  2_phase1_2d/     Route-A Phase-1 2D Boussinesq fitness search      figs 6–7
  3_spikes/        numerics upgrade + Spikes 0/1 (dynamic rescaling) figs 8–11
  4_p2_lottery/    P2 — the 1D Hou–Luo lottery-ticket legs           figs 12–35
```

## The rigor ladder (the project's framing)

- **Level 0** — reproduce a known result.
- **Level 1** — a *novel numerical map* (GA finds an approximate profile, measures a
  residual). **All of Arcs 1–4 through fig18 live here.** A GA proves nothing.
- **Level 2** — a *rigorous, computer-assisted statement* (interval / Newton–
  Kantorovich certification). **Arc 4's Route-D legs (figs 19–24) are the first
  bricks here** — validated tooling, a framing result, and then an honest structural
  *negative* (the naive certification does not close, and why). *Not a certificate.*
- **Level 3** — the Clay problem.

---

## Read in this order

### Arc 1 — the completed 1D gCLM pipeline ([`1_gclm_1d/`](1_gclm_1d/))
1. [SUMMARY.md](1_gclm_1d/SUMMARY.md) — one-page executive summary.
2. [TECHNICAL_WRITEUP.md](1_gclm_1d/TECHNICAL_WRITEUP.md) — full account: model,
   quality-diversity GA, resolution study, the anti-self-deception protocol.
3. [BLOG.md](1_gclm_1d/BLOG.md) — narrative companion (the 1D arc). *(figs 1–5)*

### Arc 2 — Route-A Phase 1: 2D Boussinesq fitness search ([`2_phase1_2d/`](2_phase1_2d/))
4. [BLOG_PHASE1.md](2_phase1_2d/BLOG_PHASE1.md) — the two de-risking experiments that
   opened Phase 1.
5. [BLOG_PHASE1_GATE4.md](2_phase1_2d/BLOG_PHASE1_GATE4.md) — the ν_crit false pass.
6. [BLOG_PHASE1_GSUSTAINED.md](2_phase1_2d/BLOG_PHASE1_GSUSTAINED.md) — the inviscid
   growth-rate currency hits the same wall; a second cheat caught.
7. [BLOG_PHASE1_GATE4_REFORM.md](2_phase1_2d/BLOG_PHASE1_GATE4_REFORM.md) — the
   reformulated Gate 4 fails 4/6; the fitness search is concluded. *(figs 6–7)*
8. [NEGATIVE_RESULT_TWO_CURRENCIES.md](2_phase1_2d/NEGATIVE_RESULT_TWO_CURRENCIES.md)
   — the **standalone** citable negative-result / methods note.

### Arc 3 — numerics upgrade + Spikes 0/1 ([`3_spikes/`](3_spikes/))
9. [TECHNICAL_PHASE2_RESCALING.md](3_spikes/TECHNICAL_PHASE2_RESCALING.md) ·
   [BLOG_PHASE2_RESCALING.md](3_spikes/BLOG_PHASE2_RESCALING.md) — the
   dynamic-rescaling decision + derivation.
10. [TECHNICAL_SPIKE0_RESCALING.md](3_spikes/TECHNICAL_SPIKE0_RESCALING.md) ·
    [BLOG_SPIKE0_RESCALING.md](3_spikes/BLOG_SPIKE0_RESCALING.md) — the CLM
    dynamic-rescaling solver, validated against its closed form. *(fig 8)*
11. [TECHNICAL_SPIKE1_VELOCITY.md](3_spikes/TECHNICAL_SPIKE1_VELOCITY.md) ·
    [BLOG_SPIKE1_STEPA.md](3_spikes/BLOG_SPIKE1_STEPA.md) — 2D velocity operator. *(fig 9)*
12. [TECHNICAL_SPIKE1_STEPB.md](3_spikes/TECHNICAL_SPIKE1_STEPB.md) ·
    [BLOG_SPIKE1_STEPB.md](3_spikes/BLOG_SPIKE1_STEPB.md) — rescaled 2D formulation. *(fig 10)*
13. [TECHNICAL_SPIKE1_STEPC.md](3_spikes/TECHNICAL_SPIKE1_STEPC.md) ·
    [BLOG_SPIKE1_STEPC.md](3_spikes/BLOG_SPIKE1_STEPC.md) — relax to the Chen–Hou
    profile (the gate, PARTIAL 3/4). *(fig 11)*

### Arc 4 — P2: the 1D Hou–Luo lottery-ticket legs ([`4_p2_lottery/`](4_p2_lottery/))
14. [TECHNICAL_P2_HL_ANCHOR.md](4_p2_lottery/TECHNICAL_P2_HL_ANCHOR.md) ·
    [BLOG_P2_HL_ANCHOR.md](4_p2_lottery/BLOG_P2_HL_ANCHOR.md) — the singular-profile
    machine vs the exact Chen–Huang–Li Thm 2.3 state. *(fig 12)*
15. [TECHNICAL_P2_CONJ24.md](4_p2_lottery/TECHNICAL_P2_CONJ24.md) ·
    [BLOG_P2_CONJ24.md](4_p2_lottery/BLOG_P2_CONJ24.md) — Conjecture 2.4: local
    attractor confirmed (9/9), global basin beyond a fixed-grid POC. *(fig 13)*
16. [TECHNICAL_P2_SCENARIO2.md](4_p2_lottery/TECHNICAL_P2_SCENARIO2.md) ·
    [BLOG_P2_SCENARIO2.md](4_p2_lottery/BLOG_P2_SCENARIO2.md) — the regular Stage-1
    profile / CHL's modified (4.1)/(4.2). *(figs 14–15)*
17. [TECHNICAL_P2_GA_FRAMEWORK.md](4_p2_lottery/TECHNICAL_P2_GA_FRAMEWORK.md) ·
    [BLOG_P2_GA_FRAMEWORK.md](4_p2_lottery/BLOG_P2_GA_FRAMEWORK.md) — the global GA
    fixed-point search infrastructure (validated tooling). *(fig 16)*
18. [TECHNICAL_P2_TWO_SCALE.md](4_p2_lottery/TECHNICAL_P2_TWO_SCALE.md) ·
    [BLOG_P2_TWO_SCALE.md](4_p2_lottery/BLOG_P2_TWO_SCALE.md) — the two-scale
    traveling-wave a-sweep (5/6 PARTIAL). *(fig 17)*
19. [TECHNICAL_P2_KLADDER.md](4_p2_lottery/TECHNICAL_P2_KLADDER.md) ·
    [BLOG_P2_KLADDER.md](4_p2_lottery/BLOG_P2_KLADDER.md) — the a_p(K) convergence
    map: the survival boundary is genuine, not genome-limited (7/7). *(fig 18)*
20. [TECHNICAL_P2_ROUTED.md](4_p2_lottery/TECHNICAL_P2_ROUTED.md) ·
    [BLOG_P2_ROUTED.md](4_p2_lottery/BLOG_P2_ROUTED.md) — **Route-D v1**: the rigorous
    interval-arithmetic core + the a=0 Newton–Kantorovich framing (the first Level-2
    brick; tooling + scoping, NOT a certificate). *(fig 19)*
21. [TECHNICAL_P2_ROUTED_DRESS.md](4_p2_lottery/TECHNICAL_P2_ROUTED_DRESS.md) ·
    [BLOG_P2_ROUTED_DRESS.md](4_p2_lottery/BLOG_P2_ROUTED_DRESS.md) — **Route-D v2**:
    the float dress rehearsal. The Newton–Kantorovich ball does **not** close at any
    truncation, gauge or weight; the cause is isolated by ablation (the transport term
    degenerates at `X = ∞`), and the repair — an asymmetric decay-graded space pair, in
    which `‖A‖ = 3.000` uniformly — is identified and measured. *(fig 20)*
22. [TECHNICAL_P2_ROUTED_SPACES.md](4_p2_lottery/TECHNICAL_P2_ROUTED_SPACES.md) ·
    [BLOG_P2_ROUTED_SPACES.md](4_p2_lottery/BLOG_P2_ROUTED_SPACES.md) — **Route-D v3**:
    the space-pair question. A **no-go theorem** for the whole weighted-`ℓ¹` category
    (the two NK requirements are separated by exactly one grading power, and the
    separation is conserved: measured minimum exponent sum **0.98**, control **0.00**),
    which retires v2's literal repair; plus the decay-graded pair that does satisfy
    both, its resonance at the anchor's own decay rate, and its interior optimum
    `α* ≈ 1.44`. *(fig 21)*
23. [TECHNICAL_P2_ROUTED_V4.md](4_p2_lottery/TECHNICAL_P2_ROUTED_V4.md) ·
    [BLOG_P2_ROUTED_V4.md](4_p2_lottery/BLOG_P2_ROUTED_V4.md) — **Route-D v4**: the full
    gauged operator in the decay-graded pair, in a third independent discretization.
    v3's far-field pricing **survives** (model law within 6% of the full `‖A‖`;
    `Z₂ = 13.4` vs 13.3 predicted; a second interior optimum at `α ≈ 1.40`), but the
    decay-graded sup pair does **not** control the quadratic — `H` is unbounded on
    `L^∞`. The certificate's space must carry a decay grading **and** a smoothness
    scale. *(fig 22)*
24. [TECHNICAL_P2_ROUTED_V5.md](4_p2_lottery/TECHNICAL_P2_ROUTED_V5.md) ·
    [BLOG_P2_ROUTED_V5.md](4_p2_lottery/BLOG_P2_ROUTED_V5.md) — **Route-D v5**: the
    two-grading space (decay × smoothness). v4's obstruction is **defused**
    (`γ ≳ 0.35`), smoothness turns out to have its **own interior optimum** just as
    decay does, and `Z₂` falls from 13.4 to 3.29. One marginal direction survives —
    the codomain's critical decay rate — fixed by a detuning that costs nothing.
    *(fig 23)*
25. [TECHNICAL_P2_ROUTED_V6.md](4_p2_lottery/TECHNICAL_P2_ROUTED_V6.md) ·
    [BLOG_P2_ROUTED_V6.md](4_p2_lottery/BLOG_P2_ROUTED_V6.md) — **Route-D v6**: the
    first genuine **upper** bounds (every earlier constant was a family-restricted
    *lower* bound), and the **discrete-ball trap** — computing an induced norm by
    duality over a discrete Hölder ball is unsound, its extremizer being inflated
    `~J²` in the continuum norm. Three of eight constants move to *bounded*; v5's
    joint optimum dies once `Z₁` is priced. *(fig 24)*
26. [TECHNICAL_P2_ROUTED_V7.md](4_p2_lottery/TECHNICAL_P2_ROUTED_V7.md) ·
    [BLOG_P2_ROUTED_V7.md](4_p2_lottery/BLOG_P2_ROUTED_V7.md) — **Route-D v7**: the
    domain **seminorm** part of `‖A‖`, closed by a derivative gain — the first
    uniform upper bound on the *whole* operator, with no `J` and no grid in it, and
    the first `(α,γ)` optimum built entirely from upper bounds. Also: the honest
    `‖A‖` costs the budget another order of magnitude (the second leg running), and
    the interpolant turns out not to lie in the space it is measured in. *(fig 25)*
27. [TECHNICAL_P2_ROUTED_V8.md](4_p2_lottery/TECHNICAL_P2_ROUTED_V8.md) ·
    [BLOG_P2_ROUTED_V8.md](4_p2_lottery/BLOG_P2_ROUTED_V8.md) — **Route-D v8**: the
    codomain **seminorm** part of `C_Q` — the last unpriced constant — bounded with
    the weight `1−γ` that `H`'s failure to inherit decay forces, giving the first
    `Z₂` in the project with **nothing omitted**. v7's optimum survives unmoved,
    v7's reason for doubting it was backwards, and the three-legs-running
    order-of-magnitude budget loss stops at 7%. *(fig 26)*
28. [TECHNICAL_P2_ROUTED_V9.md](4_p2_lottery/TECHNICAL_P2_ROUTED_V9.md) ·
    [BLOG_P2_ROUTED_V9.md](4_p2_lottery/BLOG_P2_ROUTED_V9.md) — **Route-D v9**: the
    sharpness leg. A `|H(h)|` bound rebuilt on the exact folded kernel is 32%
    better on `‖A‖` — and worth **nothing** at the operating point, because the
    closure raises it to the power γ and γ is small there. The elasticity table
    that explains it (`d log‖A‖/d log C_sup = +1.00` vs `+0.11` for the input this
    leg improved) is the leg's real output, and it names the next target.
    *(fig 27)*
29. [TECHNICAL_P2_ROUTED_V10.md](4_p2_lottery/TECHNICAL_P2_ROUTED_V10.md) ·
    [BLOG_P2_ROUTED_V10.md](4_p2_lottery/BLOG_P2_ROUTED_V10.md) — **Route-D v10**:
    the other end of the bracket, earned at last. The sign-pattern lower bound
    every earlier leg quoted was getting *worse* with `J`; an adversary family the
    ball actually contains (a wide far-field bump wins) takes the bracket from 50×
    to **7.7× at the operating point**, and yields the project's first **measured
    ceiling** on what sharpening can buy: budget `2.45e-4 → 1.88e-3`, ~5× short of
    the residual floor rather than 40×. *(fig 28)*
30. [TECHNICAL_P2_ROUTED_V11.md](4_p2_lottery/TECHNICAL_P2_ROUTED_V11.md) ·
    [BLOG_P2_ROUTED_V11.md](4_p2_lottery/BLOG_P2_ROUTED_V11.md) — **Route-D v11**:
    the *other side of the inequality*. A Newton solve on the profile equation
    reaches `relres ~1e-14` where the GA and the relaxation both floored at `1e-2`
    — **twelve orders; that floor was the search, not the equation**. A grid-refinement
    table keeps the correction from becoming an over-claim: solutions stop moving with
    `n` only up to `a ≈ 0.5`, so the survival boundary **survives a fourth, genome-free
    confirmation**. `Y₀`'s binding constraint moves from *search* to *discretization*.
    *(fig 29)*
31. [TECHNICAL_P2_ROUTED_V12.md](4_p2_lottery/TECHNICAL_P2_ROUTED_V12.md) ·
    [BLOG_P2_ROUTED_V12.md](4_p2_lottery/BLOG_P2_ROUTED_V12.md) — **Route-D v12**:
    `Y₀` measured in the basis the bounds are written in — which required the
    `a`-transport term in the compactified basis, and which found that **the `a > 0`
    profile is not a decaying tail at all: the true transport coefficient
    `E = c + aU` carries the velocity's logarithm, crosses zero at a finite radius
    `X_c ≈ e^{c/a}`, and the profile ends there with an algebraic zero of order
    `1/a`** (two independent discretizations agree on `X_c/c` to 0.1%). The `a = 0`
    anchor everything was built on is the degenerate `X_c = ∞` limit. Consequence:
    `‖A‖` is **flat at the anchor (`J^−0.003`) and divergent at the real profile
    (`J^+2.86`)**, so the seven bounded constants are the anchor's and do not
    transfer. *(fig 30)*
32. [TECHNICAL_P2_ROUTED_V13.md](4_p2_lottery/TECHNICAL_P2_ROUTED_V13.md) ·
    [BLOG_P2_ROUTED_V13.md](4_p2_lottery/BLOG_P2_ROUTED_V13.md) — **Route-D v13**:
    a **correction** and a better answer. v12's mechanism for the `‖A‖` divergence
    was wrong (a dropped sign): the mode at `X_c` *vanishes* like `(X_c−X)^{+1/a}`.
    The obstruction is in the far field, where the same equation gives
    `h ~ (log(X/X_c))^{1/a}` — **growth against a decay class**, i.e. a
    codimension-1 range condition no refinement touches (measured exponents match
    `1/a` to 0.02–0.6%). The divergence is then *attributed*: restricting the
    domain sup to a fixed outer radius drops the slope `J^+2.86 → J^+0.31` while
    the `a = 0` control stays flat at every cutoff. Bordering with the speed is
    disqualified — dilation is a symmetry, so it adds kernel, not range.
33. [TECHNICAL_P2_ROUTED_V14.md](4_p2_lottery/TECHNICAL_P2_ROUTED_V14.md) ·
    [BLOG_P2_ROUTED_V14.md](4_p2_lottery/BLOG_P2_ROUTED_V14.md) — **Route-D v14**:
    the profile equation has an **exact first integral**, `Ω = −(E/c)^{1/a}` with
    `E = c + aU` — whose `a → 0` limit *is* the exact anchor (to `1.1e−16`) and from
    which v12's compact support, its order-`1/a` zero (with amplitude) and its radius
    law all follow in one line each. Reduced to a scalar problem on `[0, X_c]`, the
    system converges from a cold start in 5–10 Newton steps and **the kill switch
    passes**: `‖A‖` is flat (`K^−0.0009 … K^+0.0011`, and unchanged under the decay
    grading) against `J^+2.80` for the same question on the whole line. Also: v11's
    grid-refinement argument for `a*` is retired (the same object is grid-converged to
    8–12 digits at `a = 0.5…1.2` on its own support); the other three confirmations
    stand. Still **not** a certificate — no constant of the radii polynomial has been
    computed in the new space. *(fig 32)*
34. [TECHNICAL_P2_LITERATURE_SCOPE.md](4_p2_lottery/TECHNICAL_P2_LITERATURE_SCOPE.md) ·
    [BLOG_P2_LITERATURE_SCOPE.md](4_p2_lottery/BLOG_P2_LITERATURE_SCOPE.md) — **Route-D v15**,
    the literature check, and the only leg that used no code. **Read the limitation first: no
    paper was read** — the container's network policy blocks arXiv and every publisher domain,
    so this is search-snippet evidence and every entry carries a confidence level. Findings:
    the two-scale inner traveling wave — this project's object — appears to have a rigorous
    fixed-point existence proof (`arXiv:2603.25104`, Mar 2026); compactly supported gCLM
    profiles and scalar fixed-point reductions are established (`arXiv:2305.05895`); gCLM
    traveling waves have been computed since 2014 (Okamoto–Sakajo–Wunsch); and
    **computer-assisted interval/Newton–Kantorovich proofs are routine in this family** — so
    **L1 is occupied territory** and finishing the certificate is a capability demonstration,
    not the lottery ticket. v14's novelty claim is retracted in place. The swing moves to the
    DSS lane. *(no figure — no measurement)*
35. [TECHNICAL_P2_ROUTED_V16.md](4_p2_lottery/TECHNICAL_P2_ROUTED_V16.md) ·
    [BLOG_P2_ROUTED_V16.md](4_p2_lottery/BLOG_P2_ROUTED_V16.md) — **Route-D v16**, the float
    rehearsal, framed by v15 as a **capability build, not a result**. `Y₀` reaches machine
    precision (`1.5e−12` at K=96, against the GA's `1e−2` floor and v12's anchor-priced
    `2.4e−4`), `Z₀` is roundoff — and **`Z₂` does not exist in the sup setting, for two reasons
    and neither is the far field**: the finite Hilbert transform is unbounded on sup on a
    *bounded* interval (adversary grows `+0.499` per e-fold in `log K`, stable under a 4×
    quadrature refinement — while the naive probe's apparent divergence collapses to `0.999`),
    and `sup|N''|` is finite exactly for `a ≤ 1/2`, where `Ω` loses `C²`. `Z₁` is not computed
    and the code refuses to assemble a budget. The repair is measured: a Hölder domain norm at
    **`γ ≳ 0.35`** — the same threshold v5 found on the whole line, now separated from the decay
    grading. *(fig 33)*
36. [TECHNICAL_P2_ROUTEE_V1.md](4_p2_lottery/TECHNICAL_P2_ROUTEE_V1.md) ·
    [BLOG_P2_ROUTEE_V1.md](4_p2_lottery/BLOG_P2_ROUTEE_V1.md) — **Route-E v1**, the first leg of
    the **DSS lane** (the swing v15 named). A DSS blow-up is a *periodic orbit* of the rescaled
    flow, so the cheapest way one could exist near this project's objects is a **Hopf
    bifurcation** off the self-similar *fixed point*. This leg computes that fixed point's
    spectrum along the whole gCLM branch, in a compactified basis where `H`, `d/dX` and the
    dilation term `X d/dX = sin θ ∂_θ` are all **exact** and the CLM anchor is the single mode
    `Ω = −sin θ` (residual `1.1e−16`). **Verdict: the only grid-converged eigenvalues at any `a`
    are `0` and `−1` — the two exact SYMMETRY modes (dilation and amplitude), derived in five
    lines before any computation — so nothing is available to cross the axis and there is no
    Hopf.** Backed by a **positive control** (plant a bump, the same filter returns `+1.083`) and
    by an exact `a = 0` result: the linearization's continuum is `(w−1)^{1−λ}(w+1)^{1+λ}` filling
    the strip `−1 < Re λ < 1`, leaving exactly `{0, −1}` in the analytic class. By-products: the
    far-field exponent map `α(a) = −c_ω(a)` (an output, running away at finite `a`) and an
    **analytic resonance at `a = 1/2` with `α = 3` to 11 digits** (novelty unchecked). *(fig 34)*

37. [TECHNICAL_P2_ROUTEF_V1.md](4_p2_lottery/TECHNICAL_P2_ROUTEF_V1.md) ·
    [BLOG_P2_ROUTEF_V1.md](4_p2_lottery/BLOG_P2_ROUTEF_V1.md) — **Route-F v1**, the **viscosity
    lane**: the Clay question in miniature — *can a blow-up beat viscosity?* Three lines of
    scaling, using Route-E v1's by-product `α`, give **`s_c(a) = α(a)/2`**: the critical
    dissipation exponent of `ν(−Δ)^s` is **half the profile's far-field decay exponent**. **NS is
    the marginal member** — its natural scaling `β = 1/2` means `α = 2` and hence `s_c = 1`,
    exactly the ordinary Laplacian, which is why every scaling argument about NS returns zero
    information. Tested by fitting a whole LINE (`D/N ~ (T−t)^p`, `p = 1 − 2s/α`) rather than
    locating a threshold: at `a = 0`, where `α = 1` exactly and **nothing is fitted**, measured
    `p` = +0.733/+0.523/+0.318/+0.109/−0.100/−0.309/−0.503 against +0.700/…/−0.500, slope
    **−2.068** vs −2 and zero at **0.5033** vs 0.5. **The headline is a cross-check**: `α` from a
    *steady compactified solve on the line* against `dp/ds` from *time-dependent periodic
    simulation* — no shared grid, basis, formulation or fitted constant — ratio **1.022 ± 0.014
    while `α` doubles**. Error bar = the fit window, swept not chosen (slope −2.02 ± 0.09,
    `s_c` 0.51 ± 0.05); the `ν`-independence control passes only weakly and says so. Map:
    `s_c` crosses the Laplacian at `a ≈ 0.383` — **arithmetic about gCLM's own scaling, not a
    claim about NS, and not a claim that a viscous blow-up exists there.** *(fig 35)*

38. [TECHNICAL_P2_ROUTEG_V1.md](4_p2_lottery/TECHNICAL_P2_ROUTEG_V1.md) ·
    [BLOG_P2_ROUTEG_V1.md](4_p2_lottery/BLOG_P2_ROUTEG_V1.md) — **Route-G v1**, the **port**:
    the same viscosity question asked of **2D Boussinesq in the Hou–Luo geometry**, the system
    the 1D toy is a model *of*. **The port broke the previous leg's formula and that is the
    result**: `s_c = α/2` is true in gCLM only because that rescaling pins `c_l = 1`, and the
    invariant law is **`s_c = 1/(2β)`** with `β` the collapse exponent of `L ~ (T−t)^β` (1D is
    the `β = 1/α` case; **NS is `β = 1/2`, giving `s_c = 1` exactly**). Two consequences that
    were not visible in 1D: **`s_c` DECREASES with `β`**, so a *faster* collapse loses to
    viscosity more easily and beating ordinary viscosity needs an anomalously **slow** collapse
    `β < 1/2`; and the far-field decay exponent and the collapse rate are **one fact**
    (`α = −1/β`, the statement that the blow-up does not disturb the outer solution) — which is
    why `α/2` looked like a law. The proven **Chen–Hou 2D Boussinesq** blow-up sits at
    **`β = 2.92`, `s_c = 0.171`** — nearly six times the NS collapse rate, on the losing side by
    a wide margin — re-measured by *our own* dynamically-rescaled machine (Spike 1) as a
    **modulation constant**, no fit and no singular-time estimate. The 1D method itself does
    **not** port: a uniform-grid periodic run gives under one decade of `(T−t)` where 1D gave
    ~4, so the collapse fit **refuses**. Also: the condition is the same whether `ω` or `θ`
    carries the dissipation, and the cross-model calibration shows the toy's dial and its
    target sit on **opposite sides** of the NS line. *(fig 36)*

39. [TECHNICAL_P2_ADVECTION_SCOPE.md](4_p2_lottery/TECHNICAL_P2_ADVECTION_SCOPE.md) ·
    [BLOG_P2_ADVECTION_SCOPE.md](4_p2_lottery/BLOG_P2_ADVECTION_SCOPE.md) — **the advection
    scope of the bound programme**, a scoping note with no figure. Every Route-D leg gated
    against the `a = 0` anchor — which is exactly where the advection term is **absent**. So
    the space was tuned on the one member of the family where the term it must carry does not
    exist. It cannot carry it: `U = ∫H(Ω)` grows like `(M/π)log X` (measured against mass to 4
    s.f.), so `DF` leaves the decay-graded codomain for **every** `a ≠ 0` and the eleven-leg
    bound programme is `a = 0`-only. The repair is one the project already owns — the
    **one-scale** grading is one power weaker, exactly enough to absorb the log (rate `+0.317
    → −0.010`). Also records that half the measurement was noise, separated by
    **reproducibility rather than magnitude** (grid-spread 0.4%/2.6% vs 5%/**99%**), and that
    this note's "stagnation point" is better read as v12/v13's **edge of support**.
    *(no figure — the numbers reproduce by running `test_advection_scope.py`)*

40. [TECHNICAL_P2_ROUTEH_V1.md](4_p2_lottery/TECHNICAL_P2_ROUTEH_V1.md) ·
    [BLOG_P2_ROUTEH_V1.md](4_p2_lottery/BLOG_P2_ROUTEH_V1.md) — **Route-H v1**, the
    **marginal case**: what happens *at* `s = s_c`, where the scaling comparison the two
    previous legs rest on returns `0 = 0`. **That point is where NS sits** (`β = 1/2 ⇒ s_c = 1`,
    the ordinary Laplacian), so it is the case rather than a corner of it. Carrying the
    dissipation through the dynamic rescaling makes its coefficient `μ = ν/(AL^{2s})` an
    **autonomous dynamical variable**, `μ_τ = (2s − α)μ` — which turns Route-F's `s_c` into the
    **eigenvalue** `λ_μ = 2s − α₀`, and at criticality that eigenvalue is exactly zero, leaving
    `μ_τ = −α₁μ²` and **one number**, `α₁ = dα/dμ`. Measured at the two resonances where `Λ^{2s}`
    is exact: **`α₁ = 0` at `a = 0`** (a *line* of viscous self-similar blow-ups, gated against a
    closed-form viscous blow-up that Newton rediscovers from a cold start to `1e−15`), and
    **`α₁ = +0.1337` at `a = 1/2`** (`K`-spread `9.1e−4`) — so `μ` decays, but **algebraically**:
    each decade costs nine times the last. Two refusals are the load-bearing part. The third
    resonance is **NOT REACHED**, and would have shipped the *opposite* sign off an `α` excursion
    two orders below its own residual — the gate is now "is there signal above the solve error",
    not "did it converge". And the **DSS re-ask**: dissipation genuinely *does* discretize
    Route-E's continuum (converged eigenvalues `2 → 8`, condensing onto the negative integers),
    removing the mechanism that shut that lane — **and the lane stays shut on better evidence**,
    since everything lands on the negative real axis with max `Re = +3e−13` and nothing complex
    (the pair first flagged as complex was split by `|Im| = 1.8e−5`; the driver now reports a
    magnitude, not a boolean). Positive control: `6 → 9` with one at `Re = +1.58`. *(fig 37)*

41. [TECHNICAL_P2_ROUTEI_V1.md](4_p2_lottery/TECHNICAL_P2_ROUTEI_V1.md) ·
    [BLOG_P2_ROUTEI_V1.md](4_p2_lottery/BLOG_P2_ROUTEI_V1.md) — **Route-I v1**, the marginal
    flow **driven**. Route-H wrote the augmented system and read it *statically* (Newton at
    frozen `μ`, `α(μ)` off the branch, the dynamics inferred); this integrates it as an
    initial-value problem, which turns two inferred numbers into measured ones and answers the
    dynamical half of ranked item (2) — *does a viscous solution actually reach the self-similar
    form?* **THE HEADLINE IS THE THING FOUND ON THE WAY: a stability inversion.** The **inviscid**
    rescaled fixed point at `a = 1/2` has **141 of 144 unstable directions** (max `Re = +4.56` —
    §26's essential spectrum, seen as a count), so nothing generic reaches it; **any `μ > 0` has
    none**, the spectrum collapsing to a discrete negative ladder whose gap is flat in `μ` across
    four decades. **The artifact test is the crossover's `K`-scaling**: dissipation beats a growth
    rate `g` once `μK^p ≳ g`, so `μ*(K) ~ g/K^p` should *fall* under refinement — measured
    `[1e−5,1e−4] → [1e−6,1e−5]` over `K = 48 → 144`, i.e. **the two limits do not commute**, which
    an artifact cannot show. And **where the instability lives is the interesting part**: the
    leading inviscid eigenvalue is `+4.55 + 430i` and `max|Im|` grows with `K`, so `Re` rises with
    log-frequency — **the fastest-growing directions are Route-E's log-periodic continuum, i.e.
    exactly what a DSS solution is built out of, and `μ` deletes them rather than damping them.**
    Third independent reason the cheap DSS entrances do not work. The two cross-checks pass:
    **`λ_μ = 2s − α₀` measured as a growth rate** (predicted `−2/−1/0/+1` vs measured
    `−2.0014/−1.0004/−0.0003/+1.0003`; the line has slope `+2.0011` and zero at `s = 1.50009`),
    and **`α₁` off a trajectory vs off the static branch at matched `K`** (`0.31% → 0.13% →
    0.10%` apart as `K` climbs — converging *toward* each other). Adiabaticity measured, not
    assumed (`1e−4 → 1.6e−6`). **Refusals carry this leg**: `p = 5` on `Λ^p` truncation — the
    *closest*-agreeing rung in the table, discarded on the operator rather than the answer;
    **all three `a = 0.3` rungs** on an unresolved profile, so there is **no off-resonance
    control** and the law is confirmed at one `a` only; a rate fit that returned `+11.8`
    against `+4.6` until it was bounded by the *variable* rather than the *time*; and, in the
    nonlinear control, the `μ = 0` and `μ = 1e−3` rows quoted as **not asymptotic** (fit
    residual 1.5–2.3 against 0.007–0.012 for the clean rows). Two failures found while
    finishing the leg are written up rather than patched away: every off-branch run **NaN'd
    into a published figure legend**, and the cause was that a perturbation "small" in
    coefficients was **3.6e8** too large in the seminorm the gauge divides by — corrected, it
    is a `5e−11` change in the profile, so it tests the gauge direction and **not** the basin.
    *(fig 38)*

42. [TECHNICAL_P2_ROUTEJ_V1.md](4_p2_lottery/TECHNICAL_P2_ROUTEJ_V1.md) ·
    [BLOG_P2_ROUTEJ_V1.md](4_p2_lottery/BLOG_P2_ROUTEJ_V1.md) — **Route-J v1**, the
    **primary-source pass**. Egress to arXiv opened after six legs of being blocked;
    `bash Papers/fetch.sh` pulled **14/14** on the first attempt; Tier 1 is read. **No new
    science — this leg retracts.** The deliverable is deliberately *code*, not prose: nine
    gates that each re-derive a published number from the published equations and compare it
    to ours, because five prose passes produced zero durable facts. **The headline is a
    subtraction: Route-F v1's `s_c = α/2` is `s*(a) = 1/c_l(a)` in arXiv:2607.19762 §6.1
    eq (6.3), posted 22 Jul 2026 — eleven days before that leg** (our `F6` map vs their
    Table 1: worst row `3.1e−3`, mean `1.2e−3`, exact at `a = 0` and `a = 1/2`). **Route-H's
    closed form (E) *is* arXiv:2207.07548 §5.3 eqs (57)–(58)** — worst relative difference
    `6.5e−15`, their `t_c` formula returning our `T` with error `0.0`. **`α(1/2) = 3` is
    exact and known**, reproduced to `7.7e−5` by integrating their `a = 1/2` pole system
    cold — **and that closes Route-E's own open question**: exact pole solutions exist at
    `a = 0` and `a = 1/2` and nowhere else, so `α = 5` was never a property of the problem,
    only of our instrument. **The re-classification with the largest forward consequence is
    Xu's Proposition 2 (realization dichotomy)**: the essential-spectrum continuum Route-E
    measured is the *maximal `L²` realization's*, which is what grids **without an origin
    condition** render — ours has none — so **Route-I's "141 of 144 unstable directions"
    must name its realization**, and re-running I5 with one is the top correction item.
    **One result arrives going the other way**: above `s_c` the balance is
    dissipation-against-stretching, `β = σ c_l` with `ω_t` subdominant, carried by a double
    pole with residue `−12iν` that is *absent inviscidly* — measured here, spread `0.0202`
    at `β = 2` vs `0.990` at `β = 1`, and the `β = 2` residual falling `0.0202 → 0.00187` on
    deeper ladders. Also settled from our side: ALS's correction to Schochet (CPAM 1986)'s
    constant, `24(3±√6)` at `5.2e−16` against the printed `12(6±√6)` at `2.4e−2` — **13.66
    decades**. Ledger: **7 pre-empted, 1 partial, 2 still unsearched, 1 inbound.** *(fig 39)*


**Novelty status:** [../LITERATURE_CHECK.md](../LITERATURE_CHECK.md) is the standing
record. **As of 2026-08-04 it has a SIXTH PASS and it is the first one against primary
sources** — egress opened, all fourteen papers in
[`../Papers/MANIFEST.md`](../Papers/MANIFEST.md) were fetched, and Tier 1 was read. The
verdict table is at the top of that file: **seven standing claims pre-empted, one partial,
two still unsearched, one inbound from the literature.** The five passes below it are
search-level and are superseded wherever they conflict — in particular the third pass named
the wrong paper as Route-F's most likely pre-emption. **Read the sixth pass before making
any novelty claim**, and note that the check is now executable
(`test_literature_gates.py`, 9/9) rather than narrative. **Still genuinely unchecked:**
Tier 2, which gates the Route-D methodological claims — the only ones with a real chance of
being new.

Forward plan: [../CLAY_ROADMAP.md](../CLAY_ROADMAP.md). Working notes:
[../PHASE2_P2_NOTES.md](../PHASE2_P2_NOTES.md).

---

## Figures ([`figures/`](figures/))

| file | arc | what it shows |
|---|---|---|
| `fig1_ga_vs_random.png` | 1 | Stage 2 — GA beats budget-matched random on 3/3 seeds |
| `fig2_resolution_convergence.png` | 1 | Stage 3 — T\* converges with resolution for 9 elites |
| `fig3_nongenericity.png` | 1 | Stage 3.5 — GA edge and the novel α≠1 target are disjoint |
| `fig4_blowup_curve.png` | 1 | a confirmed blow-up: max\|ω\|→∞, BKM 1/M→0 |
| `fig5_rough_rails.png` | 1 | Stage 3.6 — rough `C^{0,h}` data still rails the exponent near a=1 |
| `fig6_phase1_spike.png` | 2 | Phase 1 — the resolution wall: `g` converges, exponent rails |
| `fig7_phase1_axis_screen.png` | 2 | Phase 1 — only ν_crit orders blow-up propensity + is N-stable |
| `fig8_spike0_rescaling.png` | 3 | Spike 0 — CLM rescaling relaxes onto `-4X/(1+4X²)`, `c_ω→-1` |
| `fig9_spike1_stepA_velocity.png` | 3 | Spike 1A — 2D velocity operator, 2nd-order, `u_x(0)` read |
| `fig10_spike1_stepB_rescaled.png` | 3 | Spike 1B — rescaled `(ω,η,ξ)` formulation chosen by data |
| `fig11_spike1_stepC_gate.png` | 3 | Spike 1C — relax to Chen–Hou (gate PARTIAL 3/4) |
| `fig12_p2_hl_anchor.png` | 4 | P2 — singular machine vs exact CHL Thm 2.3 `(X-1)^{-1/2}` |
| `fig13_p2_conj24_relax.png` | 4 | P2 — Conjecture 2.4: local attractor (9/9), global basin not |
| `fig14_p2_regular_profile.png` | 4 | P2 — the regular Stage-1 positive profile (CHL Scenario 2) |
| `fig15_p2_scenario2.png` | 4 | P2 — CHL modified (4.1)/(4.2): invariant `c_l/c_ω→-2.533` |
| `fig16_p2_ga_framework.png` | 4 | P2 — GA global fixed-point map; a=0 known-answer gate |
| `fig17_two_scale_sweep.png` | 4 | P2 — two-scale traveling wave deforms under advection to `a_p≈0.4` |
| `fig18_two_scale_kladder.png` | 4 | P2 — a_p(K) saturates: boundary `a*≈0.5–0.55` genuine |
| `fig19_p2_route_d.png` | 4 | P2 — Route-D v1: interval enclosure, the 2-D valley, the line→circle diagonalization, and the banded+rank-1 linearized operator |
| `fig20_p2_route_d_dress.png` | 4 | P2 — Route-D v2: the NK ball never closes (‖A_N‖ ~ N), the ablation that pins it on the far field, and the decay-graded repair (‖A‖ = 3.000 flat) |
| `fig24_p2_route_d_v6.png` | 4 | P2 — Route-D v6: the discrete-ball trap (extremizer inflated ~J²), the two-point dual that saturates, the closed-form far-field `Z₁` bound, and the optimum moving once `Z₁` is priced |
| `fig25_route_d_v7_seminorm.png` | 4 | P2 — Route-D v7: the `J^γ` localized to the near diagonal, the split Hilbert bound, the `J`-free derivative-gain closure bracketing `‖A‖`, the `(α,γ)` map made of upper bounds, and the price the honest `‖A‖` puts on the matching radius |
| `fig26_route_d_v8_quadratic.png` | 4 | P2 — Route-D v8: the weighted Hölder bound on `H` and its two convergences, the 237× route ablation, the bracket against the adversary family, the γ-structure of the new term against the old, the first complete `Z₂` map, and the budget history across four legs |
| `fig27_route_d_v9_sharpen.png` | 4 | P2 — Route-D v9: the exact folded kernel's sharpening across eight decades, the payer rule's interior optimum, the gain that does not transfer to the operating point, the re-sharpened `Z₂` map, five legs of budget, and the elasticity of `‖A‖` to each input |
| `fig38_route_i_v1_driven.png` | 4 | P2 — Route-I v1: `λ_μ = 2s − α₀` measured as a growth rate along a trajectory (with the refused rungs marked), the tar pit driven against its closed law with the dynamic and static `α₁` ladders side by side, adiabaticity and off-branch starts, THE STABILITY INVERSION (unstable directions vs `μ` at three `K`, with the crossover that shows the limits do not commute), where the instability lives (`Re` against the log-frequency cutoff — the DSS band), and the nonlinear twin-trajectory control against the spectral gap |
| `fig39_route_j_v1_literature.png` | 4 | P2 — Route-J v1, the primary-source pass: the constant ALS corrected in Schochet (1986), settled from our side by the PDE residual (13.66 decades); Route-H's closed form (E) against ALS eqs (57)-(58) pointwise; `α(1/2) = 3` by integrating ALS (49)-(50) cold, with the rungs the `dτ` gate refuses drawn in red rather than truncated away; what lies ABOVE `s_c` (the Schochet family collapsing at `β = 2` and fanning at `β = 1`); our `α(a)` branch against Xu's `s*(a) = 1/c_l(a)`; and the twelve-claim ledger by verdict |
| `fig37_route_h_v1_critical.png` | 4 | P2 — Route-H v1: `s_c` read as the stability eigenvalue `2s − α₀` with the marginal point marked, the `a = 0` neutral line against its closed form, the `a = 1/2` secant extrapolation that gives `α₁` with its `K`-ladder, the DSS re-ask (dissipation discretizes the continuum onto the negative integers and nothing crosses), the time-dependent cross-check at `s = 1/2` exactly, and `μ(τ)` decaying algebraically rather than exponentially |
| `fig36_route_g_v1_collapse.png` | 4 | P2 — Route-G v1: the law `s_c = 1/(2β)` with every object on it (gCLM's dial, Chen–Hou 2D Boussinesq, and NS at `β = 1/2` exactly), `β` re-measured by our own dynamically-rescaled 2D machine as a modulation constant, the direct time-dependent route refused with its reason, the underpowered `p(s)` line kept for its sign structure, the cross-model calibration on gCLM's dial, and who beats the ordinary Laplacian as a signed bar |
| `fig35_p2_route_f_v1_viscosity.png` | 4 | P2 — Route-F v1: the relevance line `p(s)` at `a = 0` with nothing fitted, THE CROSS-CHECK (`α` from a steady solve on the line against `dp/ds` from time-dependent periodic simulation), the fit-window systematic swept rather than chosen, the `ν`-independence control, a resolution ladder, and the `s_c(a) = α(a)/2` map crossing the ordinary Laplacian at `a ≈ 0.383` where `α = 2` — the NS-critical scaling |
| `fig34_p2_route_e_v1_spectrum.png` | 4 | P2 — Route-E v1 (the DSS lane): the self-similar branch's far-field exponent `α(a)` with its Richardson ladder, spectral-vs-algebraic convergence set by the profile's own regularity, the residual scan that locates the analytic resonance at `a = 1/2`, the whole `a = 0` spectrum against the analytically known continuum strip `−1 < Re λ < 1`, the converged spectrum vs `a` (only the two symmetry modes — no Hopf), and the planted-eigenvalue positive control |
| `fig33_route_d_v16_rehearsal.png` | 4 | P2 — Route-D v16: `Y₀` falling to machine precision against its nodal control, which apparent divergence survives refining the instrument, the log-`K` unboundedness of `H` on a bounded interval, the Hölder repair and its `γ ≳ 0.35` threshold, the exact `a ≤ 1/2` threshold for `sup|N''|`, and the ledger with `Z₁` open |
| `fig32_route_d_v14_first_integral.png` | 4 | P2 — Route-D v14: the first integral's defect vanishing with `J` on an independent build (and its `a → 0` limit reproducing the exact anchor), the profile on its own support with the edge exponent, THE KILL SWITCH (`‖A‖` flat in `K` against `J^+2.80` on the whole line), the radius law with the profile's own `(m, U₀)`, and the large-`a` grid convergence that retires v11's fourth confirmation of `a*` |
| `fig31_p2_route_d_v13_turning.png` | 4 | P2 — Route-D v13: the far-field mode growing like `(log X)^{1/a}`, its exponent against the parameter-free prediction (with the `a = 0.5` row refined rather than dropped), the inner mode that *vanishes* (v12's sign error), the divergence attributed by outer radius against an `a = 0` control, where the extremal row is sourced, and the disqualified bordering repair |
| `fig30_p2_route_d_v12_defect.png` | 4 | P2 — Route-D v12: the profile ending at `X_c`, the effective speed `E = c + aU` crossing zero, the zero's order against the parameter-free prediction `1/a` in two discretizations, the defect in the certificate's own norm against the budget, its convergence rate in `J`, and the operator norm flat at the anchor but divergent at the real profile |
| `fig29_route_d_v11_anchor.png` | 4 | P2 — Route-D v11: Newton's residual 12 orders below the GA floor, the grid-refinement table that pins the survival boundary at `a ≈ 0.5` without a genome, and the weighted sup defect against the budget |
| `fig28_route_d_v10_lower.png` | 4 | P2 — Route-D v10: the sign-pattern baseline degrading with `J`, the bracket collapsing 50×→16× and 7.7× at the operating point, the far-field extremizer, brackets across the map, and the measured ceiling on sharpening |
| `fig23_p2_route_d_v5_holder.png` | 4 | P2 — Route-D v5: the square-wave adversary defused in the Hölder norm, the two interior optima (one per grading), the surviving marginal direction at the critical decay rate, and the quadratic constant before/after |
| `fig22_p2_route_d_v4_graded.png` | 4 | P2 — Route-D v4: the third build reproduces the negative and the repair, the compact core costs ~nothing (far-field law within 6%), the conjugate-extremal family showing the quadratic is unbounded in sup norms (and random sampling missing it), and the confirmed price |
| `fig21_p2_route_d_v3_spaces.png` | 4 | P2 — Route-D v3: the conservation law (the two NK exponents sum to ≥1 over every diagonal weight pair), the empty strip in the (s,t) plane with its ablation control, the far-field resonance at α=2, and the decay-graded optimum α*≈1.44 |

## Evidence map ([`data/`](data/))

Every claim traces to one committed file. Key P2 / Route-D rows:

| file | backs |
|---|---|
| `summary_metrics.json` | SUMMARY / headline numbers |
| `ga_vs_random.json`, `stage3_resolution.json`, `promoted_candidates.jsonl`, `nongenericity.json`, `stage3_6_rough.json`, `blowup_curve.json` | Arc 1 (figs 1–5) |
| `phase1_spike.json`, `phase1_axis_screen.json`, `phase1_gate4.json`, `phase1_gsustained.json`, `phase1_gate4_reform.json` | Arc 2 (figs 6–7) |
| `spike0_rescaling.json`, `spike1_stepA_velocity.json`, `spike1_stepB_rescaled.json`, `spike1_stepC_gate.json` | Arc 3 (figs 8–11) |
| `p2_hl_anchor.json`, `p2_conj24_relax.json`, `p2_regular_profile*.json`, `p2_scenario2_relax.json`, `p2_ga_framework.json`, `p2_two_scale_sweep.json`, `p2_two_scale_kladder.json` | Arc 4 (figs 12–18) |
| `p2_route_d_probe.json` | Arc 4 / fig19 — Q1 enclosure precision, Q2 degeneracy singular values, Q3 line→circle covariance, Q4 the banded operator |
| `p2_route_d_v6_bounds.json` | Arc 4 / fig24 — B1 the discrete-ball inflation, B2 the two-point dual ladder, B3 the exact modelling identity, B4 the far-field `Z₁` bound + validation, B5 the `α` tension and conditional budget, B6 the ledger |
| `p2_route_d_v7_seminorm.json` | Arc 4 / fig25 — V1 the near-diagonal localization of the `J^γ`, V2 the split `|H(h)|` bound, V3 the derivative-gain closure ladder, V4 the `(α,γ)` upper-bound map, V5 the matching radius the honest `‖A‖` forces, V6 the interpolant defect + the ledger |
| `p2_route_d_v8_quadratic.json` | Arc 4 / fig26 — X1 the estimate + grid/quadrature ladders + the route ablation, X2 the bracket over ten profiles, X3 the γ-structure vs v6's sup-only term, X4 the complete `Z₂` map, X5 the re-priced budget + its four-leg history, X6 the ledger |
| `p2_route_d_v9_sharpen.json` | Arc 4 / fig27 — Y1 the sharper pointwise bound + both ladders, Y2 the payer rule and the gain-by-point table, Y3 the new `‖A‖` J-ladder, Y4 the re-sharpened `Z₂` map, Y5 the five-leg budget, Y6 the input elasticities |
| `p2_route_i_v1_driven.json` | Arc 4 / fig38 — I1 the integrator against the `a = 0` line of fixed points plus the BDF2 order and the gauge (projected vs raw), I2 `λ_μ` as a growth rate with every rung's seed residual and `Λ^p` truncation and three refusals, I3 the tar pit driven with the dynamic/static `K`-ladder and the fit-window sweep, I4 adiabaticity, the off-branch starts and their norm qualification (with any refusal recorded, never a NaN), I5 the stability inversion at `K = 48/96/144` with the crossover brackets against `g/K^p`, I6 the frequency profile (`Re` vs `|Im|` cutoff, inviscid and viscous), I7 the twin-trajectory control, I8 the verdict with its `τ` scales |
| `p2_route_j_v1_literature.json` | Arc 4 / fig39 — provenance for each primary source (what was read, what it gates); J1 the Schochet constant, both candidates x 3 configurations with every residual; J2 the (E) ↔ ALS (57)-(58) parameter map, pointwise differences at four times, a second parameter set, and the `t_c` check; J3 the `c_l` ladder with the `dτ` floor, the resolved and REFUSED rungs both recorded (including what the refused ones would have read); J4 the collapse spread at four `β` plus the deepening sub-ladder that makes `β = 2` a measurement rather than a fit; J5 our branch against Xu Table 1 row by row, with `a_c` from all three sources; J6 the twelve-claim ledger, each entry naming its source, verdict and what survives |
| `p2_route_h_v1_critical.json` | Arc 4 / fig37 — H1 the closed-form viscous blow-up and its PDE residual in closed form, H2 the `a = 0` marginal branch (`α ≡ 1`, `α₁ = 0`), H3 the `a = 1/2` branch with the `K = 96..240` ladder and both the secant extrapolant and the chord it corrects, H4 the third point REFUSED with its signal-to-residual ratio and the verdict it would have quoted, H5 the dissipative spectrum vs `μ` with the integer ladder and the planted control, H6 the verdict with its `τ` scales, H7 the time-dependent cross-check with its `under_resolved` caveat |
| `p2_route_g_v1_collapse.json` | Arc 4 / fig36 — G0 the law and its anchors, G1 the Chen–Hou published constants, G2 `β` from our own rescaled 2D machine (steps + resolution/domain ladders), G3 the direct route measured and refused (window report + the `p(s)` exponents), G4 the cross-model calibration including a continuation to `a < 0` |
| `p2_route_f_v1_viscosity.json` | Arc 4 / fig35 — F1 the exact CLM solution and the run's own singular time, F2 the relevance line at `a = 0` (nothing fitted), F3 the cross-check against Route-E's `α`, F4 the `ν`-independence control, F5 a resolution ladder, F7 the fit-window systematic swept, F6 the `s_c(a)` map and its crossing of `s = 1` |
| `p2_route_e_v1_spectrum.json` | Arc 4 / fig34 — E1 the exact `a = 0` anchor and its two analytically predicted eigenvalues, E2 the branch `α(a)` with a `K = 64/128/256` ladder and Richardson, E3 spectral (`a = 1/2`) vs algebraic (`a = 0.3`) convergence plus the fine residual scan that finds the resonance, E4 the two structural identities gated, E5 the converged spectrum vs `a` with a tolerance ladder, E6 the planted-eigenvalue positive control, E7 the end of the branch |
| `p2_route_d_v16_rehearsal.json` | Arc 4 / fig33 — A the interpolant defect vs `K` with its nodal control, B the adversary vs the naive probe under quadrature refinement, C the sup divergence in `log K`, D the Hölder repair swept in `γ`, E `sup|N''|` by edge cutoff across `a` (the `a ≤ 1/2` threshold), plus the assembled rehearsal with `Z₁` reported as `None` |
| `p2_literature_scope.json` | Arc 4 / **no figure** — Route-D v15's literature leads: each with reference, claimed content, why it matters, an explicit `confidence`, and a `must_verify` list. Includes one extraordinary claim flagged **do not use**. Nothing in it was read from a paper; the container's network policy blocked arXiv and the publishers |
| `p2_route_d_v14_first_integral.json` | Arc 4 / fig32 — A the first-integral defect on the whole-line build + the exact `a → 0` anchor limit, B the profile on its support with edge exponent and amplitude, C THE KILL SWITCH (`‖A‖` vs `K` in three measures, with the decay-graded whole-line control), D the radius law with measured `(m, U₀)`, E large-`a` `K`-convergence |
| `p2_route_d_v13_turning.json` | Arc 4 / fig31 — S1 the corrected inner-mode exponent, S2 the growing far-field mode + its quadrature and grid convergence, S3 the operator norm by outer cutoff with the `a = 0` control, S4 where the extremal row is sourced, S5 the bordering repair disqualified |
| `p2_route_d_v12_defect.json` | Arc 4 / fig30 — T0 the profiles and their critical radii, T1 the rows Newton enforces vs the row the gauge displaced, T2 `Y₀` in the codomain norm vs the budget, T3 `X_c` and the zero order in two discretizations, T4 the convergence rate in `J`, T5 the operator norm at the real profile + its `J`-ladder, T6 the boundary sweep with the `a = 1/3` control |
| `p2_route_d_v11_anchor.json` | Arc 4 / fig29 — V0 the two-gauge requirement, V1 the known-answer gate read correctly, V2 the residual 12 orders below the GA floor, V3/V4 the grid-refinement table and the surviving boundary, V5 the weighted sup defect vs the budget |
| `p2_route_d_v10_lower.json` | Arc 4 / fig28 — W1 the lower-bound ladder vs the baseline, W2 the operating-point bracket, W3 the extremizer's shape, W4 brackets across the map, W5 the measured ceiling on sharpening, W6 the ledger |
| `p2_route_d_v5_holder.json` | Arc 4 / fig23 — U1 the defusal of the v4 adversary, U2 the Hölder constant of `H` vs `γ`, U3/U3b/U3c the inverse over `(α,γ)` and the critical-direction isolation, U4 the quadratic in the two-graded pair, U5 the joint optimum |
| `p2_route_d_v4_graded.json` | Arc 4 / fig22 — W1 the third-build reproduction, W2 the core's contribution vs the far-field law, W3 the conjugate-extremal quadratic divergence + the random control, W4 the confirmed `Z₂`/budget ceiling, W5 the gauge/drop-row operational finding, W6 the quantified (not bounded) `Z₁`-analogue |
| `p2_route_d_v3_spaces.json` | Arc 4 / fig21 — S1 the pure-convolution identity + sharp constant, S2 the inverse's price in weighted norms, S3 the (s,t) map + gap collapse + conservation law, S4 the ablation control, S5 the far-field resonance (both sides), S6 the decay-graded pair and its optimum |
| `p2_route_d_dress.json` | Arc 4 / fig20 — D1 the N-ladder (`‖A_N‖ ~ N^0.97`), D2 the radii-polynomial bounds, D3 gauge insensitivity, D4 the `(1+cosθ)→1` ablation, D5 the far-field marginality + weight-repair impossibility, D6 the decay-graded pairings |

## Rebuilding

```bash
# Arc-1/2 figures from committed data (no solver runs):
.venv/bin/python writeup/build_figures.py

# any single leg's figure from its committed data (examples):
.venv/bin/python writeup/3_spikes/spike0_rescaling_evidence.py          # fig8
.venv/bin/python writeup/4_p2_lottery/p2_two_scale_kladder_evidence.py  # fig18
.venv/bin/python writeup/4_p2_lottery/p2_route_d_evidence.py            # fig19
.venv/bin/python writeup/4_p2_lottery/p2_route_d_dress_evidence.py      # fig20
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v3_evidence.py         # fig21
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v4_evidence.py         # fig22
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v6_evidence.py         # fig24
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v5_evidence.py         # fig23
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v7_evidence.py         # fig25
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v8_evidence.py         # fig26
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v9_evidence.py         # fig27
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v11_evidence.py        # fig29
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v12_evidence.py        # fig30
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v13_evidence.py        # fig31
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v14_evidence.py        # fig32
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v16_evidence.py        # fig33
.venv/bin/python writeup/4_p2_lottery/p2_route_e_v1_evidence.py         # fig34
.venv/bin/python writeup/4_p2_lottery/p2_route_f_v1_evidence.py         # fig35
.venv/bin/python writeup/4_p2_lottery/p2_route_g_v1_evidence.py         # fig36
.venv/bin/python writeup/4_p2_lottery/p2_route_h_v1_evidence.py         # fig37
.venv/bin/python writeup/4_p2_lottery/p2_route_i_v1_evidence.py         # fig38
.venv/bin/python writeup/4_p2_lottery/p2_route_j_v1_evidence.py         # fig39
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v10_evidence.py        # fig28

# regenerate the Route-D data itself (deterministic; ~10 s and a few seconds):
.venv/bin/python experiments/p2_route_d_probe.py
.venv/bin/python experiments/p2_route_d_dress.py
.venv/bin/python experiments/p2_route_d_v3_spaces.py
.venv/bin/python experiments/p2_route_d_v4_graded.py
.venv/bin/python experiments/p2_route_d_v5_holder.py
.venv/bin/python experiments/p2_route_d_v6_bounds.py
.venv/bin/python experiments/p2_route_d_v7_seminorm.py
.venv/bin/python experiments/p2_route_d_v8_quadratic.py
.venv/bin/python experiments/p2_route_d_v9_sharpen.py
.venv/bin/python experiments/p2_route_d_v10_lower.py
.venv/bin/python experiments/p2_route_d_v11_anchor.py
.venv/bin/python -u experiments/p2_route_d_v12_defect.py   # ~13 min
.venv/bin/python -u experiments/p2_route_d_v13_turning.py   # ~6 min
.venv/bin/python -u experiments/p2_route_d_v14_first_integral.py  # ~6 min
.venv/bin/python -u experiments/p2_route_d_v16_rehearsal.py       # ~5 min

# re-curate data/ from raw logs (only if you still have experiments/*):
.venv/bin/python writeup/curate_evidence.py
```

## Provenance

Solver: [`../solver/`](../solver) (incl. `interval.py`, `gclm_family.py`,
`line_hilbert.py`); GA + resolution study: [`../ga/`](../ga); per-stage records and
design contracts in the repo root (`../PROJECT.md`, `../WIN_CONDITION.md`,
`../CLAY_ROADMAP.md`, `../LOGGING.md`, `../PHASE2_P2_NOTES.md`); one
`../experiments/JOURNAL.md` entry per logged run; tests `../test_*.py` (8 suites
green). Every logged run is pinned to a git commit (and, for GA runs, a frozen
config). The raw logs under `../experiments/` are gitignored (large, regeneratable).
