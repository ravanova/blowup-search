# Route-MTSC v1 — does the MT survivor of leg 301's screen survive on the real target? (leg 320)

**Status: PARKED, escalated to the user.** This leg answers the scoping gate the re-posed
`ℓ¹`-Fourier / radii-polynomial ban's lift condition names. A YES here does **not lift the
ban** — only the user's ruling does. Nothing beyond the artifacts below is built.

| artifact | path |
|---|---|
| runner | `experiments/p2_route_mtsc_v1.py` |
| curated JSON | `writeup/data/p2_route_mtsc_v1.json` |
| figure | `writeup/figures/fig72_route_mtsc_v1_death_mechanisms.png` (provisional `fig72`) |
| novelty pass (committed alone, before construction) | `writeup/novelty/leg_320.md` |
| journal | `experiments/journal/leg_320.md` |

---

## 1. The gate, quoted from the Decision Maker's spec before the work began

> **Gate.** Does the scoping establish, for each of the three death mechanisms, a structural
> argument (backed by the float measurement for the unmeasured nonlinearity) that it cannot
> recur in MT, AND produce the transform build cost?
> `yes` → ESCALATE to the user with the full packet: the lift condition is satisfied ON PAPER,
> the lift ruling is the user's alone. Build nothing.
> `no` → bank at full strength: MT joins the dead list with the killing mechanism named.

**Answer: YES**, on the evidence below — with one clause (S3's top test point) explicitly
window-limited, reported as such rather than oversold.

---

## 2. What "on the real target" means, and why it changes the question

Leg 301 screened structurally, on the **bare closed-form MT differentiation matrix**
(Iserles–Webb eq. 3.3) alone. That establishes `l_min = 1`, growth `+1` for the
*differentiation operator in isolation*. It does not establish anything about what happens once
that operator is **composed with the real target's coupling**: multiplication by
`S(X) = U + c_l X + c_r` (itself built from `Uop`, a dense antiderivative-of-Hilbert-transform
operator, not a simple multiplier), and the `V`-equation's own `H(Ω)` coupling. This leg builds
that composed operator and measures it.

**Method.** Solve `HL_S2_nonsymmetric` for real (`solver/bordered_hl.py`, unmodified) at
`n = 801` — Newton converges to `‖F‖_∞ = 2.276e-14` in 16 iterations
(`c_l = 1.5765, c_omega = -0.6205, c_r = 0.4377`). Take the converged Jacobian's top-left
`2n × 2n` block `J_sub` (drops the 3 border/gauge columns — a finite-rank correction, irrelevant
to the asymptotic-in-truncation questions S1/S2 ask). Transport it into MT coefficient space by
a quadrature-Galerkin change of basis: `L_MT = Ā · J_sub · Φᵀ`, with `Φ[j,i] = φ_{n_j}(X_i)` the
MT closed form evaluated on the SAME grid, and `Ā = Φ̄ · diag(w)` the trapezoid-quadrature
analysis operator. This is a discretisation of the true continuous operator's Galerkin matrix,
not a hand-derived approximation — it takes the operator this repository already built and
verified, and re-expresses it.

**A quadrature-resolution failure was caught before it was reported as a finding, and this is
itself part of the leg's evidence base.** A first pass at grid `n = 201` gave `σ_min` collapsing
to `1e-16`–`1e-17` for truncations `M ≥ 32` — which would have read as a clean M1 recurrence.
A CONTROL (lesson 90: a control that cannot come out differently is not a control) — the
analysis/synthesis Gram matrix `G = Ā·Φᵀ` of the MT basis against the grid's own quadrature,
with **no operator in it at all** — showed the identical collapse, proving the grid, not the
operator, was the cause (lesson 86: a bound dominated by its own evaluation error is a statement
about the code). A convergence sweep (`n = 201…3201`) found the requirement is roughly
`n ≥ 6×(2M+1)`; **`n = 801` keeps `σ_min(G) ≥ 0.945` through `M = 64`**, so all numbers below
are reported only where this control passed (`gram_control_trustworthy = True` at every row of
`M_ladder` in the JSON).

---

## 3. (a) — does M1 (zero-diagonal / block coupling, leg 54/62) recur?

**No, measured over an 8× truncation range (`M = 8, 16, 32, 64`).**

| `M` | `l_min` | diag growth exp. | `δ` median | `δ` max | `σ_min` | Gram `σ_min` |
|---|---|---|---|---|---|---|
| 8 | 0.4773 | n/a (too few modes) | 1.4496 | 5.0545 | 0.03141 | 0.9928 |
| 16 | 0.4773 | 0.9974 | 1.3393 | 5.7211 | 0.02549 | 0.9860 |
| 32 | 0.4773 | 0.9923 | 1.2594 | 6.3055 | 0.02918 | 0.9723 |
| 64 | 0.4773 | 0.8946 | 1.2200 | 6.7709 | 0.03138 | 0.9450 |

`l_min` is **exactly flat** at `0.47732` — the coupling to `Uop`/`H` does not erode it — and the
growth exponent stays near `+1` (`0.89–1.00`), matching Cadiot's `A1_GROWTH`. Most decisively:
`σ_min` does **not** collapse toward zero as `M` grows (`0.0314 → 0.0255 → 0.0292 → 0.0314`) —
leg 301's own pre-committed S1 kill condition (`σ_min → 0` with `N`, "leg 127's verdict
recurring") is **not triggered**. `δ` stays in `[1.22, 1.45]` median (`≤ 6.77` max) — above BDL's
`< 1/2`, exactly the wall leg 301 flagged — but leg 62's test 14 already refuted `δ` as the
coordinate that decides invertibility; the coordinate that matters, the diagonal's nonzeroness
and growth, holds throughout. **M1 does not recur, named realization: the real target's
`2n×2n` linear block, MT-Galerkin-transported at `n = 801`, `M = 8…64`.**

## 4. (b) — does M2 (`(H,D)`-consistency defect, leg 56) recur?

**No, structurally, and re-verified on this leg's own transcription.** `D` (Iserles–Webb) and
the Hilbert diagonal (`∓i`) are **closed-form rational entries with no interpolation step** —
leg 56's mechanism (a spline-interpolated `H` and a full-basis `D` disagreeing at the
endpoints) has nothing to attach to. Self-tested here, not merely quoted from 301: `D` is
skew-Hermitian to `0.0` (exact, machine-zero). The Hilbert-diagonal claim was checked against
the code's own `line_hilbert_matrix` (the object every certificate constant in
`solver/bordered_hl.py` actually uses) applied to sampled MT modes: relative disagreement
**mean 3.63%, max 3.63%** — this is the *discretised* Hilbert transform's own approximation
error against the exact continuous eigenvalue, not a defect of the MT construction; the
continuous claim is exact by Hardy-space theory (Cayley transform to the disk), independent of
any grid. **M2 does not recur.**

## 5. (c) — does M3 (`a=0` exactness / non-transfer, legs 163/176/182) recur, and what does the nonlinearity measure?

**M3: does not recur, and not merely by argument — this leg never touched `a = 0`.** Every
number above is computed on the real `HL_S2_nonsymmetric` Newton solution
(`c_l/c_omega ≠` any CLM value, non-symmetric, converged from generic data). The MT
completeness/Hardy-splitting argument was never asked to transfer from a toy profile because no
toy profile was used.

**The nonlinearity, measured in float on the target (the clause 301 flagged as entirely
unmeasured):**

| input mode `n` | output bandwidth (of 64 projected modes) | bandwidth ratio | `‖Q(v,v)‖_∞ / ‖v‖²` |
|---|---|---|---|
| 1 | 32 | 32.00 | 0.5904 |
| 4 | 29 | 7.25 | 1.2901 |
| 16 | 49 | 3.06 | 1.3671 |
| 64 | **64 (= window cap)** | 1.00 | 0.3446 |

Method: `v = ε·Re(φ_n)` (a real perturbation built from one MT mode), `Q(v,v)` computed
**exactly** (`solver/bordered_hl.py::quadratic`, no remainder — `F` is degree-2), projected onto
64 MT modes via the same quadrature-verified analysis operator (`gram σ_min = 0.945`).

`‖Q(v,v)‖_∞/‖v‖²` stays **bounded, `O(0.34–1.37)`, across two orders of magnitude of input
frequency** — no blow-up. The output-bandwidth ratio **shrinks** from `32×` at `n = 1` to
`3.06×` at `n = 16`, inside the verified window — evidence of *increasing*, not decreasing,
locality at higher input frequency, the opposite of what would kill the algebra property.

**The `n = 64` row is reported and immediately discounted, not silently kept**: its output
bandwidth reads exactly `64`, coinciding with the projection window's own cap
(`M_PROJECT_NL = 64`, chosen because that is where the Gram control was independently verified
trustworthy, not because it matches this test point). Lesson 84 (a known-answer probe has a
WINDOW): this row cannot distinguish "genuinely fills the whole window" from "the window is too
narrow to see the true edge," and it is not used as evidence for either reading. The
`n = 16` row, resolved with `49 < 64` well inside the window, is the best-resolved data point and
it shows shrinking, bounded spread.

**M3 does not recur; the nonlinearity, measured (not argued) on the target, shows bounded
amplitude across the resolved range and no sign of the algebra property failing — but only
up to `M = 64`, and the top test point is explicitly unresolved, not a clean pass.**

## 6. (d) — the validated MT transform's build cost

**No validated (interval/CAP) MT transform exists anywhere** — reconfirmed by this leg's own
novelty pass (`writeup/novelty/leg_320.md`), same conclusion as leg 301's counterweight (b), for
a different, load-bearing reason: `arXiv:1904.10755` (Shindin–Parumasur–Aluko) supplies a
**classical (non-interval) convergence/stability theory for MTC collocation on the Benjamin
equation** — a quadratic nonlinearity coupled to a non-smooth-symbol Hilbert-type multiplier,
structurally the same pairing `HL_S2_nonsymmetric` presents. That paper reduces the
approximation-theory tier of the build; it does **not** supply any rigorous/interval machinery.

**What this leg reused at zero build cost**: Iserles–Webb's closed-form `D`; the exact-diagonal
Hilbert claim (Hardy-space theory, no computation needed); `solver/bordered_hl.py`'s exact
quadratic remainder (`F` degree-2) and Jacobian, both reused unmodified.

**What does not exist and would have to be built, in order, each item blocking the next:**

1. A **validated (interval) MT forward/inverse transform** — nothing published, nothing here.
   Cost floor: comparable to what realization 1's `ℓ¹`-Fourier machinery took to reach
   scoping strength (legs 51–54, four legs) plus the extra step of an interval implementation of
   a *rational*, not polynomial, basis (no off-the-shelf interval package does this) — **≈ 2–3
   leg-equivalents**.
2. A **rigorous bilinear-form / `Z_2` bound** in MT coefficients, i.e. an MT-basis analogue of
   BDL/Cadiot's dominance machinery, informed by but not identical to Shindin–Parumasur–Aluko's
   float convergence theory (their bound is not rigorous and does not cover this leg's specific
   bordered system) — **≈ 2–3 leg-equivalents**, contingent on (1).
3. **Porting `solver/bordered_hl.py`'s bordered system (3 gauge unknowns) into MT coordinates**
   and re-deriving `Y_0`/`Z_1`/`Z_2` in the new norm, analogous to what leg 46/47 (Route-PORT)
   took for the sup-norm collocation realization — **≈ 1–2 leg-equivalents**.
4. **A tail-decay proof for the target's own MT coefficients** — 301 flagged this as
   target-dependent (geometric for rationally-decaying targets, only algebraic
   `|n|^{-5/4..-9/4}` for others) and unmeasured for `HL_S2_nonsymmetric` specifically —
   **≈ 1 leg-equivalent**, and the item most likely to force a restart of (2)/(3) if it comes
   back slow.

**Floor estimate: 6–9 further legs (~40–65 leg-hours at this repository's own per-leg cadence),
with item (1)'s interval-rational-basis implementation as the largest unpriced risk** — nothing
in the literature bounds how long a first validated rational-basis transform takes, because
nobody has built one.

---

## 7. Counterweights re-tested, not inherited

- **`δ ≈ 1` is confirmed, not `= 1` exactly**, on the real operator (`1.22–1.45` median, up to
  `6.77` max) — worse than the bare differentiation matrix's exact `1.0000`, because `Uop`/`H`
  add genuine off-diagonal mass. Scored not-a-death for the same reason leg 301 gave (leg 62's
  test 14): the diagonal stays nonzero and growing, and `δ` is not the coordinate.
- **The nonlinearity is no longer unmeasured** — it is measured here, in float, on the real
  target, and reads bounded, with the caveat in §5 stated plainly rather than smoothed over.
- **`σ_min` was the sharpest test available and it passed** (did not collapse) once the
  quadrature artifact was caught and removed — this is the single measurement most capable of
  having produced a clean NO, and it did not.

## 8. What this leg did NOT do

Did not build a certificate. Did not compute `Y_0`, `Z_1`, `Z_2` for any operator in MT
coordinates. Did not lift the ban — only the lift condition's own wording, and the user's
ruling on it, can do that. Did not resolve the `n = 64` nonlinearity test point (window-limited,
reported as such). Did not move a link of the `L1 → L4` chain — **Clay odds stay ~0.05%**.
Territory: `solver/bordered_hl.py`, `solver/line_hilbert.py`, `solver/hl_rescaled.py` read and
imported unmodified; nothing in `solver/` was edited.

## 9. Provenance

Iserles & Webb, DAMTP NA2019/03 eq. (3.3); Cadiot arXiv:2505.03091 (Assumption 1, as quoted and
machine-verified by leg 304); Shindin, Parumasur & Aluko, arXiv:1904.10755. Internal: legs 54,
56, 62, 127, 163, 176, 182, 301, 304, and `solver/bordered_hl.py` (legs 46/47). Every real-target
number in this file is read from `writeup/data/p2_route_mtsc_v1.json`, produced by
`experiments/p2_route_mtsc_v1.py`; none is re-derived by hand here.
