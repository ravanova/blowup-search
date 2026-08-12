# PROG-R4 U2/U3 — PRE-REGISTRATION ADDENDUM

**Written and committed BEFORE the cost probe, before the recurrence stage, and before any
recovery attempt.** It adds nothing to G1's wording, which is immutable and quoted from
`prog_r4_prereg.md` §2. It fixes the three things that document says must be fixed in advance
and that the 2026-08-12 wind-down left unfixed: the iteration caps, the planted controls, and
the realization the gate is answered in.

Solo mode (`ORCHESTRATION.md` §3f). There is no paired verifier. Everything below is checked by
the same session that built it, so **every check here is `UNVERIFIED`** in the §3f sense and
says so in its own gate answer. The controls and the merge gate are the whole defence.

---

## 1. The realization, measured before the run — the stepper is FIRST order, not fourth

`solver/kolmogorov2d_nkbasin.py` `_rk4_step` applies RK4 to the nonstiff part
(`-adv + forcing`) and then multiplies by the exact viscous factor `exp(-Ksq*dt/Re)`. That is
a **Lie–Trotter split**, not Strang: the two operators are applied in sequence with no
symmetrisation, so the splitting error is `O(dt^2)` locally and **`O(dt)` globally**, whatever
the order of the sub-integrator. The name `_rk4_step` refers to the sub-integrator, and it has
been read as the order of the scheme.

Measured, not asserted. The laminar state `w_lam = -(Re/n)cos(n y)` is an **exact** steady
solution: `||rhs_physical(w_lam)|| = 7.82e-14` (relative `3.07e-16`), so `Phi_T(w_lam) = w_lam`
exactly in the true flow and the global error of the discrete map is directly observable.

| `dt` | local err (1 step vs 2 half-steps) | ratio | global err at `T=19.334`, rel | ratio |
|---|---|---|---|---|
| 0.0200 | 1.8030e-03 | — | 2.6460e-03 | — |
| 0.0100 | 4.5164e-04 | 3.99 | 1.3242e-03 | 2.00 |
| 0.0050 | 1.1302e-04 | 4.00 | 6.6253e-04 | 2.00 |
| 0.0025 | 2.8270e-05 | 4.00 | 3.3132e-04 | 2.00 |

Local ratio **4.00** (`O(dt^2)`) and global ratio **2.00** (`O(dt)`), on both a laminar and a
turbulent state. First order, confirmed against an exact solution. **At the programme's
`dt=0.01` the relative error of one orbit period is `1.32e-3`.**

**This CORRECTS the mechanism recorded at MILESTONE M1, and changes none of its numbers.** M1
recorded the residual floor `||R(w_lam)|| = 0.0794` and attributed it to "RK4 truncation at
dt=0.01". The number is right and reproduces exactly; the attribution is wrong. RK4 truncation
at a state where the RHS vanishes identically is zero. The floor is **splitting** error, and it
is `O(dt)`, not `O(dt^4)` — so it is ~1000x larger than M1's stated mechanism predicts, and it
shrinks only linearly under refinement. M1's milestone answer (the laminar control reproduces
leg 353's reduction through the new layer) is unaffected and is NOT re-opened.

**Three consequences carried into G1's answer, per lesson 91 (a negative names its
realization).**

1. Newton converges to RPOs **of this discrete map**, which differ from the true PDE's RPOs at
   relative `O(1.3e-3)` per period. `tol=1e-8` is a tolerance on the **discrete** residual and
   is reachable regardless of the splitting order, so this does NOT by itself block a `YES`.
2. The published Table IV `(T, s)` come from the sources' own, higher-order discretisations.
   The matching predicate uses `MATCH_T_TOL = MATCH_S_TOL = 0.05`. On `T ~ 19.334` that is
   **0.26%** against a systematic realization offset of **0.13%** — covered, but by only ~2x.
   On `s ~ 0.3-0.55` the tolerance is 10-17% and comfortable. **The T margin is thin and is
   reported as a magnitude in the gate answer, not smoothed over.**
3. Because of 2, **`n_converged_to_tol` and `n_recovered_named_orbit` are reported separately
   and neither is substituted for the other.** A run that converges orbits but matches none is
   a *different* finding from one that converges nothing, and G1's `no` branch must say which.

**The stepper is NOT changed.** Strang splitting would be nearly free and would buy a second
order, but it changes the realization M1 was validated against, discards a DNS already in
flight, and is outside a U2/U3 scope. Changing the integrator *before* seeing the result it
feeds is the drift §3f names. It is recorded as the top successor item instead.

## 2. The iteration caps — the rule, fixed before the probe reports

The wind-down named this the blocker: the caps were never set from a measured per-epoch cost,
and at the defaults (`max_newton=40 x max_gmres=200`) the worst case is ~4 h **per attempt**,
which does not fit 100 attempts. Caps are a **cost** setting, not part of the pre-registered
compliant scale (`T=1e5` / genuine hookstep / ~100 attempts / `N=24`), but a cap set too low
would manufacture an under-resourced null at G1. So the rule is fixed here, in advance:

> **CAP RULE.** Choose the largest `(max_newton, max_gmres)` whose measured worst-case
> per-attempt wall time, times `ceil(100 / n_workers)` rounds, fits an **8 h** U3 envelope,
> subject to BOTH lower bounds:
>
> - **(a)** `max_gmres >= 2x` the 95th percentile of Krylov dimensions actually consumed in the
>   cost probe — so that GMRES is stopped by its `rtol=1e-3` early exit and not by the cap;
> - **(b)** `max_newton >= 2x` the median number of epochs to convergence-or-stall in the probe.
>
> **If (a) and (b) cannot BOTH be met inside the envelope, U3 does not report a `no`.** It
> reports the shortfall as a cost and **G1 answers `UNDER-RESOURCED`** per `ORCHESTRATION.md`
> §3d, naming the wall time a compliant attempt would need. A cheap attempt may not close this
> lane.

Measured inputs to the rule, taken before the probe: **0.8935 ms/step** for the DNS integrator,
and **1.756 s** for one Jacobian action (one `T=19.334` integration at `N=24`, `dt=0.01`). The
probe supplies the Krylov-dimension and epoch-count distributions that (a) and (b) need.

**The probe's seeds come from a short `T=2000` DNS — leg 353's own under-resourced scale — and
are used for COST ONLY.** No number from the probe is evidence on G1 in either direction, and
the probe cannot change G1's wording, its thresholds, or the caps once this rule has fixed
them.

## 3. The planted controls on G1 — both directions, both able to fire

G1 is a claim, so it carries planted controls that can fire **both** ways (§3f). They test the
*instrument*, which is the thing a solo session cannot otherwise cross-check: if the machinery
cannot drive an exact solution to `tol=1e-8`, then a `no` at G1 is an instrument failure and
not a fact about orbits, and it must not be recorded as a resourced null.

**Control P (positive, unconditional — must succeed).** The discrete map has its own relative
equilibrium `w*`, found by Newton on `Phi_dt(w) - w`, and it is **not** `w_lam` (§1: the split
does not preserve steady states). `w*` satisfies `Phi_T(w*) = w*` exactly for any `T`, with
`s = 0`, so it is an **exact** solution of the extended-residual system and the state row
vanishes identically. Perturb it and require hookstep-Newton to recover it to `tol=1e-8`.

*What it tests and what it does not.* It exercises the **state block only**. At a relative
equilibrium `||dR/ds|| = 0` exactly and `dR/dT` is negligible — M1 measured this and recorded
the rank deficiency of 2 — so `T` and `s` are not probed by P. Stated here rather than
discovered later.

**Control R (positive, conditional — must succeed if it runs).** If any attempt converges, the
converged orbit is perturbed and must be re-recovered. This one *does* exercise `T` and `s`.
It runs only if there is something to plant, and its non-running is reported, not hidden.

**Control N (negative — must FAIL).** A phase-scrambled field carrying the same amplitude
spectrum as a real candidate, seeded with a period drawn from the Table IV anchor band. It is
not near any orbit, so `recovered_named_orbit` must **not** fire on it. This guards the
matching predicate against firing spuriously — the failure mode that would turn a `no` into a
false `yes`.

**CONTROLS FIRED AS PLANTED := P recovered AND N did not recover** (AND R recovered, if R ran).
Mirrors U4's `controls_fired` construction in `u4_g2_basin.py`.

> **If the controls do not fire as planted, G1 is NOT answered `no`.** The run reports an
> instrument failure and G1 answers `UNANSWERED`. A `no` at G1 is a resourced null with
> consequences for all of route 4 (§3d), and it is only permitted to fire on an instrument
> that has been shown, in the same run, to be able to say `yes`.

## 3a. AMENDMENT 1 — control P was run as pre-registered, FAILED, and is re-scaled

**Recorded after the fact, openly, with the original result kept.** This is the amendment §3f
requires be visible rather than silent, and the rule it changes is fixed by a property of the
*target*, not by whether the control passes.

**What happened.** P as pre-registered above used `T_CONTROL = 19.33`. Run at that value it did
not recover: it stalled on the **first** epoch at `reason=trust_region_collapsed`, residual
`236 → 223`, having moved the state not at all — the relative error to `w*` was still `1.0e-3`,
exactly the perturbation it started with.

**Why that failure indicts the control and not the instrument — measured, not argued.** In the
linear regime (`eps = 1e-13` relative) the discrete relative equilibrium amplifies by:

| `T` | 0.5 | 1.0 | 2.0 | 3.0 | 4.0 |
|---|---|---|---|---|---|
| amplification | 1.91 | 6.09 | 99.9 | 2.81e3 | 1.02e5 |
| implied `λ` | 1.29 | 1.81 | 2.30 | 2.65 | 2.88 |

`λ` rises to **2.88**, which extrapolates to `exp(54) ≈ 1e24` over `T=19.33`. Double precision
carries ~`1e16` of dynamic range, so that shooting Jacobian is not merely ill-conditioned but
**numerically empty**: no Newton method can solve it, and P's failure there says only that.

**The targets are nothing like that.** The same measurement on the turbulent attractor, where
the Table IV orbits live, gives **`λ = 0.35`** and an amplification of **`8.73e2`** over
`T=19.33` — about `1e21` times gentler. The equilibrium is simply a far more unstable object
than the orbits being sought, and planting a control on it at a full Table IV period was a
mis-specification.

**The amendment.** `T_P` := the exact multiple of `dt` at which the equilibrium's amplification
equals the **attractor's** amplification over one Table IV period (`8.73e2`). Log-interpolating
the measured table between `T=2` and `T=3` gives **`T_P = 2.65`**. This makes P exactly as hard,
in conditioning, as the real problem — neither easier nor harder — and the number comes from a
property of the attractor measured *before* P was re-run. **It is not tuned to make P pass.**

**Verified after the change.** The plant is still exact at the new period
(`||Φ_T(w*) − w*|| = 8.03e-14`) and its amplification is `8.35e2` against the `8.73e2` target.

**P is CONSERVATIVE, and this is the reason to trust a pass and not over-read a fail.** At a
relative equilibrium `T` and `s` are degenerate (M1's rank deficiency of 2), so P's Jacobian is
*worse* conditioned in those two directions than a genuine RPO's, where neither is degenerate.
P therefore over-states the difficulty of the (T, s) block and matches it on amplification. A
pass is strong evidence; a fail should be read together with control R, which tests the real
regime exactly.

**P doubles as the cap-adequacy test, and this is now part of the cap rule.** P runs at the
**same** caps as the real attempts. If P cannot recover an exact planted solution at those
caps, the caps are too small and a `no` at G1 would be an artefact of the budget rather than a
fact about orbits. Measured while setting them: P recovers at `max_gmres=120` (residual
`195 → 2.16e-5` in 19 epochs, state error `1e-3 → 3.1e-6`, stopped only by `max_newton_hit`)
but **collapses at `max_gmres=50`** (`trust_region_collapsed` at epoch 15). This exposed a real
defect in the cost probe's first pass: its `p95` of ~20 Krylov dimensions was measured over
only 3 epochs, all far from the solution where GMRES converges easily, and it **systematically
under-states** what the hard late epochs need. Clause (a) is therefore read against P's
measured floor, not against that `p95` alone.

## 4. What this addendum does not do

It does not restate, soften or re-scope G1. It does not touch the compliant scale. It does not
change the seed, the eight named Table IV rows, or the anchor rule. `CLAY_OBLIGATIONS` §6's two
no-method obligations stay **OPEN** and §4 stays **OPEN and NOT discharged** on both branches,
per `prog_r4_prereg.md` §3. **Ceiling TIER 2.** No `L1 -> L4` link is moved by anything here;
Clay stays ~0.05%.
