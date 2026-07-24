# Executive Summary

**Project:** an honest, search-based attempt at the direction-(b) side of the
Navier–Stokes Millennium problem — *evolve* initial conditions toward
finite-time blow-up — built to never mistake a numerical artifact for a
discovery.

**What was actually built and proven (banked, not hypothetical):**

1. **A validated 1D solver.** A pseudo-spectral solver for the generalized
   Constantin–Lax–Majda (gCLM) family `ω_t + a·u·ω_x = ω·u_x + ν·ω_xx`,
   `u_x = H(ω)` — one code path spanning CLM (`a=0`, closed-form blow-up) to
   De Gregorio (`a=1`). Validated against the CLM analytic blow-up time,
   pure-diffusion decay, and advection/invariant checks.

2. **A working quality-diversity evolutionary search.** A MAP-Elites GA over
   Fourier-coefficient genomes with an evolvable regularity exponent, fitness =
   **ν_crit** (the critical viscosity a shape's blow-up survives) at `a=0.7`.
   **Acceptance criterion met: the GA beats budget-matched random search on
   3/3 seeds** (margins **3.3 / 4.6 / 3.2** bisection tolerances), exceeding the
   best literature profile on every seed — figure
   [`fig1`](figures/fig1_ga_vs_random.png). Reaching this took two failed
   fitness axes first; the failures are themselves findings (the naive axis is
   dominated by a trivial spectral-concentration cheat).

3. **Resolution-confirmed (Tier-2) blow-up.** An automated resolution study
   reran the 9 best elites at N = 256 / 512 / 1024. **All 18 studies
   (9 elites × inviscid + viscous) reached `NUMERICALLY_CONFIRMED`:** the
   extrapolated blow-up time T\* is resolution-converged (finest-two agreement
   ≤ **3.5×10⁻⁶** inviscid, ≤ **4.1×10⁻⁴** viscous, vs a 2% gate), conservation
   drift *shrinks* with resolution (≤ 6.7×10⁻⁵), and the top elite is
   T\*-identical at N=2048 — figures
   [`fig2`](figures/fig2_resolution_convergence.png),
   [`fig4`](figures/fig4_blowup_curve.png).

**The honest limits (stated, not buried):**

- **These are 1D toy models, not 3D Navier–Stokes.** A Tier-2 confirmation here
  validates the *method*, not the real equation.
- **Tier 2 ≠ proof.** Resolution-converged floating-point T\* is strong
  numerical evidence; a Clay answer requires Tier 3 (a rigorous
  computer-assisted proof), for which no pipeline exists here.
- **The confirmed blow-ups are generic (exponent α = 1.000 throughout)** — the
  CLM singularity surviving moderate advection, *not* a novel De Gregorio-type
  singularity. So the value is a **validated pipeline + a defensible
  shape→viscosity-resistance map**, not a new mathematical result.

**The negative result that scoped the next move.** A cheap 240-run gate asked
whether the search could be pointed at the *novel*, non-generic (α≠1) target.
It cannot, on this model: at `a=0.7` (where the GA has its edge) every blow-up
is generic; non-genericity appears only near `a=1` and only as a **resolution
artifact** (15/40 shapes flip between resolutions; α rails 3.0 ↔ 0.3). The GA's
edge and the novel target are **disjoint** — figure
[`fig3`](figures/fig3_nongenericity.png). This closed the cheap route before any
GA compute was spent, exactly as the anti-self-deception protocol intends.

**And the loophole closed too (Stage 3.6).** The literature's *provable*
non-generic blow-ups need genuine limited-regularity (`C^{1,α}`) data, so a
final cheap probe built a real rough-data genome mode — `sign(sin x)|sin x|^h`,
an odd `C^{0,h}` vorticity with a localized Hölder cusp, unit-tested for the
intended regularity — and measured the blow-up exponent near `a=1` at N up to
**4096**. It still rails: an `a=0.7` control validates the fine-N fit (generic
α≈1, stable), then `a=0.9` scatters, `a=0.95` rails 0.30↔3.00 across resolution,
and `a=1.0` is a dead axis (0/18, even for the roughest data) — with drift far
under the artifact guard, so the rail is genuine, not under-resolution — figure
[`fig5`](figures/fig5_rough_rails.png). The cheap 1D route to novelty is closed
for smooth *and* rough data; the rough-data representation and the validated
fine-N exponent method are the transferable deliverables for the next model.

**Bottom line.** The reachable near-term goal — a validated solver + a
non-degenerate evolutionary search + resolution-confirmed candidates + a
shape→resistance map — is **complete and reproducible**. The Millennium problem
itself remains far out of reach; the forward options (a different model where
provable non-generic blow-ups live; or the 3D-Euler scale-up) are laid out in
[../CLAY_ROADMAP.md](../CLAY_ROADMAP.md). Overall probability of solving Clay via
this program stays very low (~0.05%); the honest win is the pipeline and the map.

---

## Route A Phase 1 — in progress (2D Boussinesq, Hou–Luo geometry)

The forward move from the 1D pipeline is a genuine 2D model where a finite-time
singularity is **proven** (Chen–Hou 2022) and numerically gold-standard
(Luo–Hou 2014): 2D Boussinesq in the Hou–Luo symmetry-wall geometry. This is
still a toy model, not 3D Navier–Stokes, and Tier 2 is still not a proof — but
it is a strictly stronger setting for the search. **Banked so far** (Gates 1–2 +
two de-risking spikes; the GA campaign itself is *not* yet run):

1. **A validated 2D pseudo-spectral solver** (`solver/boussinesq.py`): fft2 +
   RK4 + integrating-factor viscosity + 2/3 dealiasing, with `ν`/`κ` and the
   conservation/energy artifact guards first-class. Validated by an exact
   analytic ladder (6/6 at machine precision), and the Hou–Luo no-flow wall
   imposed by parity is a *genuine* invariant of the discrete dynamics (held to
   9×10⁻¹⁵ unenforced; wall BC 8×10⁻¹⁷).

2. **A resolution de-risk spike — verdict STABLE, but recalibrating.** Before
   building the search, a cheap fine-N probe (N=128→1024) tested the dominant
   risk: is the Hou–Luo singularity even resolvable on a uniform grid? The
   answer is a measured *two-part* one — figure
   [`fig6`](figures/fig6_phase1_spike.png):
   - **Yes for the search.** A fixed-window growth-rate `g` **converges** across
     N (smooth growers, finest-two ≲ 10⁻⁴) — a resolution-stable fitness signal
     exists.
   - **No for confirming the true singularity.** The fitted blow-up exponent
     **rails** (α: 2.45→0.70→0.90→1.20) and `T*` never stabilizes — a uniform
     grid never reaches `T*` (Luo–Hou needed AMR to ~10¹²). So **uniform-grid
     Tier-2 confirmation of the real Hou–Luo singularity is out of reach**;
     rough `C^{0,α}` data is under-resolved from `t≈0` and is dropped. The
     honest near-term deliverable is therefore a resolution-stable **shape→growth
     QD map with Tier-1 candidates**, with Tier-2/Tier-3 gated behind AMR or a
     validated-numerics collaborator (Route D).

3. **A fitness-axis screen chose the fitness on labeled ground truth, not
   priors.** The spike left two labeled ICs — one that blows up, one that
   saturates. A pre-committed screen asked which candidate axis orders *blow-up
   propensity* (`sharp > mild > control`) **and** is resolution-stable — figure
   [`fig7`](figures/fig7_phase1_axis_screen.png). The raw growth rate `g` gets it
   **backwards** (the saturating shape has the higher early rate); a persistence
   proxy mis-ranks the non-grower. The **ν_crit-analog** — the viscosity at which
   net amplification crosses 2× — is the sole survivor: right direction and
   **identical to four decimals across N=256/512**. This is the fitness the Gate
   3 genome will carry.

4. **Gate 3 built the smooth 2D genome** (`ga/genome2d_smooth.py`) — truncated
   Fourier modes in the Hou–Luo parity subspace, one joint energy normalization
   (killing the overall-amplitude cheat), MAP-Elites on anisotropy × centroid —
   and wired the ν_crit-analog through the solver (`ga/fitness2d.py`), tested
   12/12.

5. **Gate 4 ran the six-property gate on ν_crit — and it FAILED property 6, the
   same wall as 1D.** The pre-committed predicate printed 6/6 PASS, but that was a
   **false pass**: interrogating the winner showed ν_crit is ~75% explained by the
   initial vorticity amplitude (ρ(ν_crit, log|ω₀|) = **−0.90**; two shapes at
   equal absolute vorticity get a **197×** ν_crit gap), a trivial small-denominator
   cheat the free ω/θ split enables. Fixing the split and a normalized-resistance
   transform both fail to rescue it → the νk²-dissipation wall, reconfirmed and
   fundamental for viscosity-resistance fitness. Per the pre-committed directive
   this is a **finding, not a push-harder signal**. A follow-up probe shows an
   **inviscid growth-rate currency** escapes both cheats (direction ✓; ρ(g, log|ω₀|)
   = +0.24; ρ(g, centroid) flips to +0.38) — promising but necessary-not-sufficient,
   and the open forward decision.

6. **The staged `g_sustained` probe: the escape hatch is real but narrow.** The
   inviscid growth-rate currency was probed cheap-first before any 40-shape gate
   (`phase1_gsustained_probe.py`, data
   [`data/phase1_gsustained.json`](data/phase1_gsustained.json)). Three findings:
   (1) its *magnitude* is on the **same uniform-grid resolution wall** as ν_crit —
   the blow-up shape re-accelerates at the moving edge of its trusted window, so
   `g_frac` climbs with N (sharp: **0.66→0.79→0.97** at N=128/256/512) and never
   converges (spike finding #3 reasserting); (2) but the *rank order* is
   resolution-stable (Spearman **+0.90** at 128↔256), and `g_frac` **survives the
   cheat audit** — direction-correct, ρ(g,log|ω₀|)=+0.17 (no ω₀ cheat),
   ρ(g,centroid)=+0.31 (rewards structure) — where a rival `accel_ratio` is
   rank-stable **but a small-denominator cheat** (mis-ranks the ground truth);
   (3) the free-split property-6 check is **favorable** — no trivial max-split rail
   (interior split optimum), and partial ρ(g,log|ω₀| | split)=**+0.04** proves the
   ω₀ cheat is absent. **Net:** a *rank-based* `g_frac` is the one viable fitness
   found, contingent on an un-run 256→512 **rank**-stability check (paused for
   review). The honest reframing: "resolution-stable" must mean *rank*-stable here,
   because the magnitude is unrecoverable on a uniform grid.

7. **The 256→512 rank check passed — then the reformulated Gate 4 FAILED (4/6).**
   The un-run de-risk was run: `g_frac`'s **rank** survives 256→512 (Spearman
   **+0.905**), cheat audit clean at N=512. That green-lit a full reformulated Gate
   4 (`phase1_gate4_reform.py` + frozen `analyze_phase1_gate4_reform.py`, data
   [`data/phase1_gate4_reform.json`](data/phase1_gate4_reform.json)) with the
   anti-cheat audits promoted to first-class gate conditions. It **fails 4/6**: on a
   **free-split** roster the optimum rails to split→1 (**ω₀→0, the ν_crit
   degeneracy returning**) — top-5 all split 0.93–0.99, ρ(g,log|ω₀|)=−0.66 — while
   `g_frac` carries almost no ω-geometry signal beyond split (partial
   ρ(g,centroid|split)=**+0.11**) and is largely a **formation-time proxy** (partial
   ρ(g,centroid|t_res)=**−0.39**). Property 4 also fails on a second axis: the
   grower/non-grower *classification* is not resolution-stable (7/37 coarse-grid
   false-growers). The controlled split-sweep *passed* (interior optima) — only the
   free-search **winner interrogation** exposed the rail. **Net:** two independent
   currencies now fail the honest gate through the same ω₀→0 degeneracy; a third
   uniform-grid scalar currency is not indicated.

**Honest scope of Phase 1 so far.** No 2D blow-up candidate has been produced —
this is validated infrastructure plus a **concluded fitness search with a decisive
negative result**: neither viscosity-resistance (`ν_crit`) nor inviscid growth-rate
(`g_frac`) survives a pre-committed, cheat-audited viability gate, both defeated by
the same free-split ω₀→0 degeneracy. The deeper finding is about the *grid*: on a
uniform mesh the genuine singular structure forms below grid scale, so no scalar
fitness read off the trusted window can isolate it — it re-expresses through the
next resolvable proxy (amplitude, split, formation time). The honest path to a
structure-tracking fitness (and to Tier-2 of the true singularity) is an
**AMR / self-similar-rescaling solver upgrade to Route A** — better *numerics* that
measure fitness on resolved structure. (This is a Route-A numerics upgrade, **not**
roadmap "Route D," which is the later Tier-3 computer-assisted-proof leg.) A
standalone methods note packages this negative result on its own:
[NEGATIVE_RESULT_TWO_CURRENCIES.md](NEGATIVE_RESULT_TWO_CURRENCIES.md).
Methodology banked repeatedly: a frozen predicate,
a rank-stable winner, *and* a passing controlled sub-test are each a floor, not a
ceiling — interrogate the actual free-search winner against the dumbest cheats.
Forward plan and full record:
[../PHASE1_PLAN.md](../PHASE1_PLAN.md),
[../PHASE1_GATE4_RESULTS.md](../PHASE1_GATE4_RESULTS.md),
[../PHASE1_GSUSTAINED_RESULTS.md](../PHASE1_GSUSTAINED_RESULTS.md),
[../PHASE1_GATE4_REFORM_RESULTS.md](../PHASE1_GATE4_REFORM_RESULTS.md),
[BLOG_PHASE1_GATE4.md](BLOG_PHASE1_GATE4.md),
[BLOG_PHASE1_GSUSTAINED.md](BLOG_PHASE1_GSUSTAINED.md),
[BLOG_PHASE1_GATE4_REFORM.md](BLOG_PHASE1_GATE4_REFORM.md).

---

## Phase 2 — the numerics upgrade (in progress: scoped + de-risked, not built)

The forward move from the concluded fitness search is the solver upgrade that
resolves the singular region so a fitness measures *real* structure. Decision (made
with the user via a reviewed options menu): build **dynamic self-similar rescaling**
— integrate in a rescaled frame so the blow-up is a steady profile on a fixed grid —
rejecting AMR (heavier, discards the validated solver). It reuses our spectral
solver, dissolves the below-grid-scale wall, and its late-time state *is* a
self-similar profile — the on-ramp to direct profile construction (the field's actual
novelty frontier; the "evolve-ICs vs hunt-profiles" question is re-decided at a gate
*after* the solver works). Spike-first, on a known answer: **Spike 0** implements it
in 1D on gCLM against the exact CLM self-similar blow-up (`Ω̄₀=−4X/(1+4X²)`, `T*=2`)
before **Spike 1** ports to 2D Boussinesq.

**Banked so far (reconnaissance, no solver yet):** the rescaled equation derived and
confirmed against the published gCLM scheme (Huang–Tong–Wang, arXiv:2603.25104); three
instructive false starts (pointwise-derivative normalization is a noise amplifier; a
periodic grid converges to the *wrong* profile because periodic H ≠ line H for the
`~1/X` tail; a uniform whole-line grid is CFL-strangled by the self-similar dilation);
and the full build recipe from the paper's Appendix C (spline-analytic **line** Hilbert
transform + stretched cosh/sinh grid + WENO5/SSPRK). Confirmed a genuine multi-day
solver build with all literature gaps closed. Full record:
[TECHNICAL_PHASE2_RESCALING.md](TECHNICAL_PHASE2_RESCALING.md),
[BLOG_PHASE2_RESCALING.md](BLOG_PHASE2_RESCALING.md),
[../PHASE2_NUMERICS_PLAN.md](../PHASE2_NUMERICS_PLAN.md),
[../PHASE2_SPIKE0_NOTES.md](../PHASE2_SPIKE0_NOTES.md). Honest scope unchanged: even a
flawless solver reproduces a *proven* toy-model result (Chen–Hou 2022); the value is
the structure-resolving enabler, and any novelty is downstream in profile construction.

*All Phase-1 numbers above are drawn from [`data/summary_metrics.json`](data/summary_metrics.json)
and the files it references; see [README.md](README.md) for the evidence map.*
