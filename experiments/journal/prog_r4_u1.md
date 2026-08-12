# PROG-R4, unit U1 — MILESTONE M1: the globalisation layer

**Programme:** PROG-R4 (ORCHESTRATION.md §3c PROGRAMME lane, slot A, leg 380).
**Unit kind:** MILESTONE. A build unit. **No claim is made here and no gate is
answered here.** The programme's two gates are G1 (unit U3) and G2 (unit U4),
pre-registered verbatim in `experiments/journal/prog_r4_prereg.md`. Nothing
below may be read as bearing on either.

**Preceded by:** U0, the programme-level novelty pass
(`writeup/novelty/prog_r4.md`), landed at `dd35bbf` with verdict PROCEED.

---

## 1. What the unit was asked for

Three things, from the dispatch:

1. A genuine hookstep / trust region on the existing Newton–Krylov apparatus.
2. A laminar-fixed-point control that reproduces leg 353's 99.3% baseline
   **through the new layer**.
3. A per-iteration ledger, persisted.

All three are delivered. Item 2 is the milestone proper.

## 2. What was built

`solver/hookstep_newton.py` (new), three public functions:

- `arnoldi` — modified Gram–Schmidt with **one reorthogonalisation pass**, and
  it returns the **raw** Hessenberg matrix rather than a Givens-rotated one.
  Both choices are forced by what the hookstep needs. The RPO Jacobian is
  ill-conditioned enough that plain MGS corrupts orthogonality, and once
  `Q` is not orthonormal `‖dx‖ ≠ ‖y‖` — which would silently destroy the
  meaning of the trust-region radius, the one quantity U4 exists to measure.
  Givens rotations are skipped because the subproblem needs an SVD of `H` at
  many radii, not a triangular solve at one.

- `hookstep_subproblem` — minimise `‖H y − β e₁‖` subject to `‖y‖ ≤ δ`, solved
  by SVD with `y(μ) = V diag(sᵢ/(sᵢ²+μ)) g`, `μ` located by bisection. **This
  is where the cost argument lives:** re-solving at a new radius reuses the
  same `H` and costs *zero* extra Jacobian actions, and one Jacobian action
  here is a full nonlinear time integration over the orbit period.

- `newton_hookstep` — one Arnoldi build per Newton iteration with the entire
  radius loop nested *inside* it; ratio test `ρ = actual/predicted`; radius
  shrink/expand; per-iteration and per-radius-trial ledger; Jacobian-action
  and residual-evaluation counters.

`solver/kolmogorov2d_nkbasin.py` (mine, extended): `newton_hookstep_rpo`,
which reuses `extended_residual` **unchanged**, so leg 353's path is
bit-for-bit untouched (and §5 below shows that it is, by measurement).

## 3. Two design decisions that are not cosmetic

**(a) The cancellation-free predicted reduction.** The obvious ratio test
`predicted = ‖R‖ − ‖H y − β e₁‖` cancels catastrophically at small radii,
where the two terms agree to many digits. In the first working version this
drove `ρ → −∞`, collapsed the trust region, and made the hookstep look *worse*
than a line search. The fix is to work in squared currency and expand:

    β² − ‖Hy − βe₁‖² = 2 y·(Hᵀ rhs) − ‖Hy‖²

with `Hᵀrhs` cached once per Arnoldi build. Recording this because the failure
mode was a property of my arithmetic, not of the method, and a reader
reproducing a *worse* hookstep would otherwise have no way to know that.

**(b) `T > 0` is a domain constraint, and the trust region enforces it.**
The first run of this control terminated at `nonpositive_period` with only a
96.6% reduction: the period walked out of the domain. Two changes, both in my
own driver:

- a trial with `T ≤ 0` returns a non-finite residual, so the radius loop
  rejects it and shrinks — which is exactly what a trust region is *for*, and
  costs no time integration;
- the finite-difference Jacobian action shrinks `ε` rather than probing
  *through* `T = 0` (the generic action sets `ε` from `‖v‖` alone, which
  handed Arnoldi a non-finite column and made the SVD fail to converge).

`extended_residual` itself was deliberately **not** modified. Its `T_eff`
floor silently evaluates a *different* problem at negative `T`, which would
corrupt the ratio test; but changing it would have altered leg 353's
line-search path too, and the whole value of §5 is that that path is
unchanged.

## 4. The three checks that separate a hookstep from a line search

A line search rescales the GMRES direction. A hookstep rotates it. Any test
that both would pass proves nothing, so `test_hookstep_newton.py` (28/28)
carries three that only a hookstep passes:

| | check | measured |
|---|---|---|
| i | as `δ → 0` the step rotates onto `−JᵀF` | `cos = 1.00000000` |
| ii | the constrained step is not parallel to the GMRES step | `cos = 0.8896` (a line search gives exactly 1) |
| iii | the hookstep converges where step-halving cannot | see below |

Check (i) is run on the **full** Krylov space on purpose. On a truncated
space the small-radius limit is the steepest-descent direction *projected onto*
`span(Q_k)`, which is not `−JᵀF`; comparing there measured `cos = 0.73` and
would have been checking the wrong statement. Recorded because it looked like
a failure for some time and was not one.

Check (iii) needed a construction where a stall cannot be blamed on the merit
function. Two earlier attempts were discarded: a `tanh`-based residual which
turned out to have **spurious local minima of ‖F‖** (both methods stalled at
the *same* value — no globalisation escapes those, so the test was vacuous),
and a truncation so severe that neither method converged. The construction
that survives is

    F(x) = A (x + c x³),   componentwise cube,   c = 10,  cond(A) = 1e3,
    dim 6, Krylov 5

for which `J(x) = A diag(1 + 3c x²)` is **nonsingular everywhere**. Hence
`JᵀF = 0 ⟺ F = 0`, `t ↦ t + ct³` is strictly increasing with its only zero at
0, and therefore `‖F‖` has exactly one critical point — the root. No spurious
minimum exists to trap either method. Both methods are then matched on
everything except direction: same analytic Jacobian action (no finite-
difference noise to confound the result), same Krylov dimension, same
acceptance criterion (strict decrease of `‖F‖`). Measured:

| method | outcome |
|---|---|
| step-halving, **8 halvings** (leg 353's exact configuration) | `line_search_failed`, `‖F‖ = 5.030`, iteration 13 |
| step-halving, **200 halvings** | still stalled, `‖F‖ = 3.967` after 200 iterations |
| hookstep | **converged**, `‖F‖ = 1.95e-10`, 51 iterations, `‖x‖ = 1.7e-7`, ≤6 radius trials |

The 200-halving row is the load-bearing one: it isolates **rotation** from the
halving budget. And because `J` is nonsingular by construction, the stall is
provably not a local minimum. It is the direction.

Separately measured: re-solving at 50 further radii added **0** Jacobian
actions to the 8 that built the basis.

## 5. THE MILESTONE: the laminar control through the new layer

The laminar profile `w_lam = −(Re/n) cos(n y)` is an exact fixed point (it is
x-independent, so the nonlinear term vanishes identically and viscous and
forcing terms cancel). Perturbed by 1% of its own L2 norm in a fixed random
direction — leg 353's seed 0, same draw, same normalisation order — and given
to the solver at `T = 1.0, s = 0.1`, `tol = 1e-8`, `max_newton = 8`,
`max_gmres = 15`, `N = 24`, `Re = 60`, `n = 4`, `dt = 0.01`.

| | `‖R‖` start → end | reduction | monotone | reason |
|---|---|---|---|---|
| **hookstep (new layer)** | 19.1100 → **2.753e-2** | **99.8560%** | yes | `max_newton_hit`, 7 iterations |
| line search (leg 353's layer, same inputs) | 19.1100 → 1.256e-1 | **99.3426310647174%** | yes | `max_newton_hit`, 8 iterations |
| leg 353's *recorded* baseline | — | **0.993426310647174** | yes | — |

The line-search column reproduces leg 353's recorded fractional reduction to
**every digit stored in `writeup/data/p2_route_dsspb5_v1.json`**. That is the
real control on the control: it establishes that my replication of the setup is
exact, so the hookstep row is being compared against the right thing rather
than against a near-miss re-run.

**M1 answer: the control reproduces leg 353's baseline through the new layer**
(99.8560% ≥ 99.3426%, monotone). Cost: 120 Jacobian actions, 136 residual
evaluations, 4.89 s.

The trust region was demonstrably active, not decorative — iterations 5, 6, 7
took 4, 3 and 4 radius trials respectively as `δ` came down 1.710 → 0.428 →
0.214 → 0.0534.

## 6. Measured limit of this control, recorded rather than tuned away

Neither globalisation reaches `tol = 1e-8` here, and that is a property of the
control, not of either layer. At an x-independent fixed point both extra
unknowns are null directions: `Φ_T(w_lam) = w_lam` for every `T`, and
`shift_x(w_lam, s) = w_lam` for every `s`. Measured at the exact laminar
point:

- `‖∂R/∂s‖ = 0.0` — **exactly** zero;
- `‖∂R/∂T‖ = 0.0212`, against **9.775** for a unit random state direction
  (a factor ~460; the residue is time-discretisation drift, not signal);
- `‖R(w_lam)‖ = 0.0794` — a **floor** set by RK4 at `dt = 0.01`, and the
  laminar profile drifts `3.12e-4` relative over `T = 1`.

So the extended Jacobian is rank-deficient by 2 on this control and there is a
residual floor above `1e-8` regardless. This is why the milestone is stated as
a *reduction against leg 353's recorded reduction* and not as a convergence.
The control probes the **state block**; it does not exercise `(T, s)`, and it
was never able to.

A consequence, flagged forward: `test_hookstep_rpo_keeps_the_period_strictly_positive`
starts from a deliberately bad `T = 0.05` and the period collapses to
`1.42e-7` — positive, as required, but at the boundary. On this control that is
expected, because `T` carries no information. **For a genuine RPO seed the
period is a real direction, so if U3 sees the same collapse it is a finding
about the seed, not a bug in the layer.**

## 7. What this unit does NOT establish

It shows the new globalisation did not break a solver on a problem whose
answer is known analytically. It shows the hookstep beats step-halving on a
synthetic problem constructed so that the comparison is about direction alone.

It shows **nothing** about whether a published Table-IV RPO recovers. That is
**G1**, unit U3, and its pre-committed wording stands untouched. Leg 353's five
attempts all failed at `line_search_failed` with final `‖R‖ ∈ [22.5, 29.5]` —
never within two orders of `tol` — and the hookstep's advantage on a
6-dimensional cubic says nothing about a 578-unknown chaotic-attractor seed.
U2 must still supply a `T = 1e5` DNS and its recurrence library before G1 can
be asked at the scale the question is posed at.

## 8. Obligations carried

Carried in this unit's persisted record and in both gates when they are
reached:

- **CLAY_OBLIGATIONS §6, obligation 1 (no method) — OPEN.**
- **CLAY_OBLIGATIONS §6, obligation 2 (no method) — OPEN.**
- **CLAY_OBLIGATIONS §4 (finite energy / localisation) — OPEN and NOT
  discharged**, and it stays open in every route-4 gate until leg 386
  (ROUTE-DTOL) lands with a pre-registered δ mode (user ruling, 2026-08-12).
  Leg 382 landed a certified far-field decay enclosure at `104f5b3`, but §4's
  admissible cutoff radius is a function of the *certified decay exponent* and
  so inherits that instrument's tolerance; leg 382's gated `δ = 0` form answers
  EMPTY on every real input, and its measured critical tolerances span two
  orders (`δ* = 3.352868, 0.315697, 0.069739`; `0` only for an exact power
  law).

**Clay: no L1–L4 link moved by this unit. Clay stays ~0.05%.** Nothing here
presumes the POCP spend either way.

## 9. Artefacts

- `solver/hookstep_newton.py` — the layer.
- `test_hookstep_newton.py` — 28/28.
- `solver/kolmogorov2d_nkbasin.py` — `newton_hookstep_rpo`.
- `test_kolmogorov2d_nkbasin.py` — 12/12 (3 new).
- `experiments/programme_r4/u1_m1_globalisation.py` — the runner.
- `experiments/programme_r4/u1_m1_ledger.json` — the persisted per-iteration
  and per-radius-trial ledger, plus the degeneracy measurements of §6.
- `capabilities.py` — one appended entry.

Figures: **none**. `fig97` and `fig98` remain unspent and reserved for the two
claim units, per the dispatch's figure allocation.

## 10. Next

**U2 — MILESTONE M2:** `T = 1e5` DNS at `N = 24` with recurrence-candidate
extraction, thresholds taken from `writeup/data/p2_route_rpol_v1.json`. Leg
353's measured rate (352.33 s for `T = 2000`) puts this at ≈ 4.9 h, so it runs
in the background.
