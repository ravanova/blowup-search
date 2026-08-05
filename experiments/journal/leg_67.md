# Leg 67 — Route-FD v1: the 2D critical fractional-dissipation exponent, checked against the literature

**Date:** 2026-08-05. **Branch:** `leg/fd-v1`. **Difficulty:** light. **Kind:** literature.
**New solve runs: 0**, under both branches of the gate, as the dispatch required.

## What was asked

`capabilities.py` records `solver/fractional_boussinesq.py` as validated only by "consistency
with the 1D critical exponent; no independent known answer". The 2D object's critical
fractional-dissipation exponent `s_c = 1/(2 beta) = 0.17120` had never been checked against a
published number — only against our own 1D result. This leg searched for one.

## Bans, checked first

`plan_of_record.py` bans "re-measuring beta on the 2D object" (leg 43: the object does not
converge) and "chasing the 2D near-null direction of leg 44". **Neither is touched.** The `beta`
in this leg is the *collapse* exponent `-c_l/c_omega = 2.92056`, a closed-form function of two
constants published by Chen–Hou (Part I, arXiv:2210.07191 (2.23)) — not leg 43's measured growth
rate. No fit, no grid, no time integration appears anywhere in the leg. `capabilities.py` was
grepped before anything was written; nothing was built.

## Gate

> "Does a primary source publish an independent critical fractional-dissipation exponent for 2D
> Boussinesq (or its vorticity-stream equivalent)?"

**NO** — for the quantity this repository holds. The full-precision answer has three parts,
because a bare "no" would be wrong in the other direction:

1. **A published exponent by that name exists.** For 2D Boussinesq with `(-Δ)^{α/2} u` and
   `(-Δ)^{β/2} θ`, the critical relation is `α + β = 1`, with a ladder of sufficient conditions
   descending to `α > 2/3` on that line. The vorticity-stream equivalent is stated as well: at
   `α + β = 1` the problem "boils down to" critical gSQG.
2. **It is not comparable to `s_c`.** The published criticality is where the *equation's scaling*
   stops preserving the controlling norm. Ours is where dissipation overtakes *one specific
   collapse*. Every published value is a one-sided *sufficient condition for global regularity* —
   an upper bound on any arrest threshold — never an equality.
3. **Nobody publishes an arrest exponent for the Chen–Hou blowup.** The blowup corpus is inviscid
   without exception; the dissipation corpus never touches a blowup profile.

**So the exponent remains internally-consistent-only. No claim upgrade. No computation attempted.**

## Magnitudes

Arithmetic on constants already on file, in the literature's convention (`α = 2s`):

| quantity | value |
|---|---|
| `beta` (collapse, `-c_l/c_omega`) | `2.9205610051` |
| stored `s_c = 1/(2 beta)` | `0.1711999849` |
| `alpha_equiv = 2 s_c` | `0.3423999698` |
| `|c_omega/c_l|` | `0.3423999698` (identical — internal) |
| literature critical line at zero thermal diffusion | `α = 1` |
| `alpha_equiv` as a fraction of that line | `0.3423999698` |
| factor below the line | `2.9205610051` |

**The ratio is arithmetically vacuous**: `alpha_equiv / 1 = 1/beta` identically, by the definition
of `s_c`. Comparing our number to the only published line recovers `beta` and nothing else — that
is the precise sense in which the check is unavailable.

**One weak external contact exists and it passes.** Hmidi–Keraani–Rousset prove global regularity
at `α = 1, β = 0`; our law predicts arrest for `α > 0.34240`, hence regularity at `α = 1` —
consistent, with the published datum a factor `2.9206` above our threshold. One-sided; it would
pass for any `s_c < 0.5`. Recorded as a margin, not a validation.

**Why the absence is structural, not an oversight.** `alpha_equiv = 0.3424` sits inside the
supercritical regime `α + β < 1`, which arXiv:2606.03680 §1 calls "largely out of reach". There is
no published exponent ladder down there to compare against.

## Near-miss worth keeping

A search summary asserted a published 1D critical dissipation exponent `γ = 1/3`. It is in none of
the returned papers — two abstracts were fetched in full to confirm — and the follow-up query
silently re-attached "1/3" to a `C^γ` Hölder norm of `θ`. **Discarded as a search-summary
artefact**, and logged in `writeup/novelty/leg_67.md` rather than deleted: a pass that stopped one
step earlier would have reported a published number that does not exist.

Separately, arXiv:1908.09385 §1.2 *does* publish critical dissipation exponents for the 1D gCLM
(`γ_c = 1` for `a > −1`; `γ_c = |a|^{−1}` for `a ≤ −1`) — again the scaling quantity, and Chen
proves blowup with the **full Laplacian** `γ = 2` for `a ≈ ½`, *above* his own critical line.
Reading his `γ_c` as comparable to our `s_c` would manufacture a contradiction out of two correct
statements about different quantities.

## Deliverables

- `experiments/p2_route_fd_v1_lit.py` — the executable query log + full-text locators + arithmetic
- `writeup/data/p2_route_fd_v1_lit.json` — curated data; every number in prose appears here
- `writeup/novelty/leg_67.md` — the novelty pass at full depth (committed before the writeup)
- no figure: a literature leg with one table of arithmetic has nothing to plot

## Handoff to the orchestrator

`capabilities.py` is outside this leg's territory, so the required annotation correction is
**reported, not applied** — the exact drop-in replacement string is in
`writeup/novelty/leg_67.md` and in the JSON under `capabilities_correction`. It changes
`validated` from "no independent known answer" (an absence never looked for) to "searched at
primary source and found none, and here is why none exists". `test_capabilities.py` requires only
`len(validated) > 20`, so it is drop-in. Precedent: commit `ab07316`.
