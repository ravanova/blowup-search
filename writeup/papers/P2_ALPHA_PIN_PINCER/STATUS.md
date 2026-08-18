# P2 — The α-pin × ṁ pincer. STATUS.

**Working claim.** For a nontrivial backward `λ`-DSS blow-up profile of 3D Navier–Stokes the
far-field decay exponent is pinned to exactly `α = 1`. After cut-off, four of five localisation
error terms cancel or decay, and the survivor is the modulation commutator `T₃ ∝ ṁ`, of size
`ρ^(1−α)`. It vanishes only at `α > 1` — which the pin forbids — or at `ṁ = 0` — which the
rigidity results forbid. The natively-finite-energy route is therefore shut at an **endpoint**, not
by a gap.

## What is banked for it

| evidence | field | note |
|---|---|---|
| The pin | `L2′` / leg 397 | `≥1` from Chae–Wolf Thm 1.1; `≤1` from Chae–Wolf Rmk 1.2 + ESS; restated by Pineau–Vicol (2026) §1.2. 18 techniques adjudicated, 9 FAILS / 8 FAILS-BY-CONSTRUCTION / 1 SATISFIED. |
| The survivor | `L5` / leg 400, `p2_route_l5_finite_energy_v1.json` | `|T₁+T₂|/|T₁| = 2.58e-08`; `T₄,T₅ ~ ρ⁻²`; `|R_loc|/|T₃| = 0.999998`. |
| The endpoint | `L5` | ρ-exponent `+1.09e-04` out to `|y| = 1261.72` — enlarging the cutoff buys nothing. Summability needs strictly negative; `α = 1` gives exactly 0. |
| Falsifier did not fire | `L5` control `C7` | Optimal `(δa, δκ)` absorption over all `ℝ³` left `1.00091` of the residual — slightly **worse**. |
| Verification | `V-W5` / leg 403 | Five items reproduce; tail-3 exponent re-fitted independently to `3.4e-16`; C6 tolerance history re-run — introduced once, **never moved**. |

## BLOCKERS — and the first is severe

1. **BOTH JAWS ARE JOURNAL-ONLY AND HAVE NEVER BEEN READ AT PRIMARY.** `V-W5` called this the
   sharpest undischarged item in the file. **A referee reads the sources.** If either theorem
   carries a hypothesis inherited second-hand, the claim collapses — and this is exactly the
   leg-348 shape, on a result the record currently calls *shut and verified*. **§3k rule 2 forbids
   drafting past the claim statement until this is discharged.**
2. **The numerics are on a SYNTHETIC exactly-DSS stand-in**, not route 4's own object
   (`CORRECTIONS.md` §34), and `c_mod` is **basis-dependent by 1.476×**. `L6` has now priced route
   4's own object and returned **NO on refinement**, with a **factor-11 optimiser spread** across
   four identical re-runs.
3. **`C6` did not fire as planted**, and the criterion that passed was added **post-hoc at the
   landing commit**. `V-W5` located this. It goes in the paper, not only in the journal.
4. **Novelty is unassessed.** The ingredients are published; the assembly may not be. Nobody has
   checked.

## What it owes

- The primary read of both jaws, as its own unit, **before any drafting past §1**.
- An honest statement of the contribution boundary: what is new is the identification of `T₃` as
  the sole survivor and its `ṁ`-proportionality — a float64 computation on a synthetic profile.
