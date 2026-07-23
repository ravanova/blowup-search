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

*All numbers above are drawn from [`data/summary_metrics.json`](data/summary_metrics.json)
and the files it references; see [README.md](README.md) for the evidence map.*
