# Phase 1 resolution de-risk spike — results

*Route A Phase 1, reordered before the Gate 3 genome (2026-07-23). The
pre-committed question and gate are in `phase1_resolution_spike.py` /
`analyze_phase1_spike.py`; this records what came back. Verdict determined from
15/16 runs (the 16th, `smooth_mild` N=1024, is a slow no-blow-up confirmation
that cannot move the verdict).*

## Verdict: STABLE — proceed to Gate 3/4 with a growth-based fitness

At feasible uniform resolution there **is** a resolution-stable fitness signal
for buoyancy-driven vorticity growth, even though the Hou–Luo singularity itself
is out of uniform-grid reach. The fixed-window log-growth-rate `g` converges
across N for both smooth growers (all successive changes ≤ the 10% gate, by
~1000×):

| IC | g @128 | g @256 | g @512 | g @1024 | finest-two |
|----|-------|-------|-------|--------|-----------|
| smooth_sharp | 0.6075 | 0.6088 | 0.6087 | 0.6088 | 0.01% |
| smooth_mild  | 1.239 | 1.239 | 1.239 | *(pending)* | 0.000% |

## The four findings (and what each means)

1. **The growth-rate fitness is resolution-stable.** `g` settles to 0.609
   (smooth_sharp) and 1.239 (smooth_mild) — the search can rank shapes by early
   growth with a signal that does **not** move with N. This is the dominant
   viability precondition, and it passed. → the GA search is viable.

2. **The resolved window extends with N.** smooth_sharp: `t_res` 2.46→3.18 and
   `amp_res` 29×→42×→64×→101× as N goes 128→1024. Refinement resolves further,
   exactly as a correct code should. (Note: `amp_res` therefore is **not** a
   resolution-stable fitness — it rewards resolution; `g` is the stable one.)

3. **The blow-up EXPONENT / T\* rails — the resolution wall, quantified.**
   smooth_sharp fitted exponent 2.45→0.70→0.90→1.20 and T\* 5.9→3.1→3.3→3.6
   across N. A uniform grid never reaches T\*, so the singularity's exponent is
   not resolution-converged. **Tier-2 confirmation of the true Hou–Luo
   singularity is not reachable on a uniform grid** (Luo–Hou needed AMR to
   ~10¹² effective resolution). This bounds the *confirmation* leg, not search
   viability.

4. **Rough C^{0,h} data is under-resolved from t≈0.** rough_h0.3 / rough_h0.5:
   `t_res` 0.03–0.07 at every N up to 1024 — the Hölder cusp's spectral tail
   exceeds the grid immediately, leaving no growth window. **The rough-data
   genome axis is resolution-starved on uniform grids**; the Elgindi/Chen–Hou
   C^{1,α} regime is not explorable at feasible N with this discretisation.

## Consequences for Gate 3/4 (recalibrated, honest)

- **Proceed** to the 2D genome + MAP-Elites, on **smooth data**, with a
  **resolution-stable growth-based fitness** (not `amp_res`). A ν_crit-analog —
  the critical viscosity that suppresses the early resolved-window growth — is
  the prime candidate: it mirrors the gCLM fitness that worked and is plausibly
  both resolution-stable and blow-up-predictive. Gate 4 must confirm.
- **Recalibrate the deliverable.** The near-term Phase-1 output is a
  resolution-stable **shape→growth QD map with Tier-1 candidates**, NOT
  Tier-2-confirmed singularities. Tier-2/Tier-3 confirmation of the real
  singularity needs AMR or Route D (validated numerics / expert) — the flagged
  proof leg, now with quantified justification (finding 3).
- **A fitness subtlety Gate 4 must resolve:** smooth_mild has the *higher* early
  `g` (1.24) but *saturates* (no blow-up, amp≈5), while smooth_sharp has lower
  `g` (0.61) but blows up (amp>100). So the early-window growth rate is
  resolution-stable but **not automatically blow-up-predictive** — the six-property
  viability gate must select the axis that tracks blow-up *propensity*, not
  transient early growth.
- **Drop the rough-data axis** from the uniform-grid search (finding 4), or scope
  it explicitly as out-of-reach pending a higher-resolution tool.

Net: the reorder paid off — it converted "is uniform-grid 2D Boussinesq search
viable?" from a weeks-long gamble into a measured answer: **yes for the search
(smooth, growth-fitness), no for uniform-grid Tier-2 confirmation and no for the
rough axis** — all before a line of genome code.
