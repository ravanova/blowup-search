# TECHNICAL — PROG-R4 U2/U3: the planted positive control, the defect it caught, and the cap arithmetic

Companion to [BLOG_P2_PROGR4_CONTROL_CATCH](BLOG_P2_PROGR4_CONTROL_CATCH.md).
Pre-registration: `experiments/journal/prog_r4_u2u3_prereg_addendum.md` (§2 cap rule, §3
controls, §3a amendment 1, §3b amendment 2).

**Status at time of writing.** MILESTONE M2 and GATE G1 are both **UNANSWERED**. The T=1e5 DNS
is in flight. Nothing below is evidence on G1 in either direction. Everything below is
**UNVERIFIED** under `ORCHESTRATION.md` §3f (solo mode): it was produced and checked in the same
session, and is carried into G1's own answer with that label.

---

## 1. What G1 asks, and why its `no` needs an instrument warrant

Gate G1, immutable wording:

> DOES AT LEAST ONE NAMED TABLE-IV RPO RECOVER TO tol=1e-8?

* `yes` → U4 proceeds; ceiling TIER 2.
* `no` → a **resourced null**; §3d's stop fires; route 4 stops.

Because the negative branch has consequences, the pre-registration binds the negative branch to
the controls:

> CONTROLS FIRED AS PLANTED := P recovered AND N did not recover (AND R recovered, if R ran).
> If the controls do not fire as planted, G1 is NOT answered `no`. G1 answers `UNANSWERED`.

`UNANSWERED` is **stricter** than `no`, not softer: it withholds a stop that a `no` would fire.

## 2. Control P — construction

P must be recoverable by construction, exactly known, and require no search of ours that could
itself fail. It is the **discrete** relative equilibrium: the exact fixed point of the map the
code iterates, not of the PDE.

For the Lie–Trotter step (RK4 on the nonstiff part, then the exact viscous factor), a state with
no nonlinear self-interaction satisfies, mode by mode,

```
w*_hat = dt * forcing_hat * decay / (1 - decay)
```

with `decay = exp(-dt k² / Re)`. Implemented in `experiments/programme_r4/u3_controls.py`:

```python
def discrete_relative_equilibrium(solver):
    d = solver.decay
    den = 1.0 - d
    ok = np.abs(den) > 1e-300          # masked division: k=0 gives 0/0 under np.where
    w_hat = np.zeros_like(solver.forcing_hat)
    w_hat[ok] = solver.dt * solver.forcing_hat[ok] * d[ok] / den[ok]
    return np.fft.ifft2(w_hat).real
```

Verified residuals of the planted point: `||Φ_dt(w*) − w*|| = 7.6e-14`, and
`||Φ_T(w*) − w*|| = 2.35e-13` at T=19.33. The extended residual there is an exact zero, so P's
seed residual is not an estimate.

P exercises the **state block only**. At a relative equilibrium `||∂R/∂s|| = 0` exactly and
`∂R/∂T` is negligible (this is M1's recorded rank deficiency of 2). The `(T, s)` directions are
control R's job, not P's.

## 3. Amendment 1 — P failed as pre-registered, and the re-scaling rule

At the pre-registered `T=19.33`, P **failed**: `trust_region_collapsed` at epoch 1, residual
`236 → 223`, state unmoved.

It was not retuned to pass. The cause was measured:

| quantity | equilibrium (P) | attractor (the real seeds) |
|---|---|---|
| leading Lyapunov exponent λ | ≈ 2.88 | ≈ 0.35 |
| amplification over T=19.33 | ≈ 1e24 | 8.73e2 |

Double precision spans ~1e16. At `T=19.33` the equilibrium's Jacobian is **numerically empty** —
the linearisation carries no recoverable information, and no globalisation can descend. That
condition is a property of the *equilibrium*, not of the *attractor* the real attempts are
seeded from, so P at full period was testing something the unit does not do.

The re-scaling rule was therefore fixed from the **target**: `T_P` := the multiple of `dt` at
which the equilibrium's *measured* amplification equals the **attractor's** amplification over
one Table IV period, `8.73e2`. The equilibrium's amplification was measured in the linear regime
(`eps = 1e-13` relative):

| `T` | 0.5 | 1.0 | 2.0 | 3.0 | 4.0 |
|---|---|---|---|---|---|
| amplification | 1.91 | 6.09 | 99.9 | 2.81e3 | 1.02e5 |
| implied `λ` | 1.29 | 1.81 | 2.30 | 2.65 | 2.88 |

Log-interpolating between `T=2` and `T=3` for a target of `8.73e2` gives **`T_P = 2.65`**.

Verified after the change: the plant is still exact at the new period
(`||Φ_T(w*) − w*|| = 8.03e-14`) and its amplification is `8.35e2` against the `8.73e2` target.

The number comes from a property of the attractor measured *before* P was re-run — derived from
the quantity being controlled, not from P's outcome. That is the distinction that keeps it a
control rather than a tuned pass. The original failure remains in the record
(`u3_control_P_trial.json`).

Consequence carried forward: P is now a **conservative** positive — it proves the state block can
be recovered at attractor-like conditioning, not at arbitrary conditioning.

## 4. Amendment 2 — the defect

### 4.1 The impossible pair

Sweeping P over GMRES caps returned, at `max_gmres ∈ {80, 120}`:

```
reason = "converged"     converged_to_tol = False     final_residual = 1.63e-8     tol = 1e-8
```

Both cannot hold if the reporting is correct.

### 4.2 Mechanism

`newton_hookstep_rpo` (`solver/kolmogorov2d_nkbasin.py`) drives `newton_hookstep`
(`solver/hookstep_newton.py`) with `max_newton=1` per epoch, because the residual's two phase
rows are evaluated against a reference that is rebuilt at each accepted iterate (a moving
Poincaré section). Inside `newton_hookstep`, with a budget of one iteration, `"converged"` is
reachable from two places:

```python
# hookstep_newton.py, top of the loop
if r < tol:
    reason = "converged"          # (i) AT ENTRY: hist == [r], x unmoved
    break
...
x, F, r = x_try, F_try, r_try
hist.append(r)                    # step taken, post-step residual appended
# after the loop:
if reason == "max_newton_hit" and r < tol:
    reason = "converged"          # (ii) ON THE STEP: hist == [pre, post], x MOVED
```

The outer routine read, unconditionally:

```python
r = float(out["residual_history"][0])     # PRE-step in case (ii)
hist.append(r)
if out["reason"] == "converged":
    reason = "converged"
    break                                  # ...before the block that adopts out["x"]
```

In case (ii) this (a) reports the pre-step residual, (b) never adopts `out["x"]`, so `w0, T, s`
stay at the previous iterate, and (c) returns `success = bool(r < tol) = False` on a solve that
**had reached tol**.

### 4.3 Impact

At G1 this records `recovered_named_orbit = False` on an attempt that recovered — a fabricated
`no` on the gate whose `no` stops route 4 under §3d. It fails silently: no exception, no
non-finite value, a plausible residual, and the exit reason and the success flag disagreeing in
a field nothing was reading.

### 4.4 Fix and blast radius

The converged branch is moved **after** the adopt block and re-reads the converged pair:

```python
        w0, T, s = w0_try, T_try, s_try

        if out["reason"] == "converged":
            r = float(out["final_residual"])
            hist.append(r)
            reason = "converged"
            break
```

Case (i) is preserved unchanged: when the inner call converges at entry it runs no iteration, so
its ledger is empty and it exits through the pre-existing `if not out["ledger"]` branch with
`r` already correct.

Blast radius: the branch is unreachable for any solve that never reaches `tol`.

* `test_hookstep_newton.py` (32/32) and `test_kolmogorov2d_nkbasin.py` (12/12) pass under the
  fix, and `scripts/merge_gate.sh origin/main` prints `MERGE GATE: PASS`. Neither suite detected
  the defect beforehand — the branch only executes on a success this problem had never produced.
* **M1 re-run against the fix reproduces bit-identically** — every field of
  `u1_m1_ledger.json` except wall-time fields. M1 stalls at `||R|| = 0.0794` and never enters the
  branch. **M1 is not re-opened.**

## 5. The cap sweep, and clause (a)

Pre-registered CAP RULE, clause (a): `max_gmres ≥ 2 ×` the 95th percentile of Krylov dimensions
actually consumed, so that GMRES is stopped by its `rtol=1e-3` early exit and not by the cap.

Control P, `max_newton=60`, `T=2.65`, perturbation 1e-3:

| `max_gmres` | P recovered | final ‖R‖ | epochs | p95 Krylov | 2×p95 | epochs hitting cap | wall |
|---|---|---|---|---|---|---|---|
| 80  | **no**  | 1.63e-8 | 28 | 80.0 | 160.0 | 13 of 28 | 440 s |
| 120 | **no**  | 1.64e-8 | 32 | 66.0 | 132.0 | 0 | 705 s |
| 140 | **yes** | 7.75e-9 | 33 | 65.8 | 131.6 | 0 | 521 s |

Readings:

* At 80 the cap is binding in 13 of 28 epochs — clause (a) fails outright, independently of
  anything else.
* The 120 row is a **cap failure and a reporting failure compounded**, and is not a verdict on
  P. Only the 140 row is a clean measurement.
* Clause (a) requires `max_gmres ≥ 131.6`. **`max_gmres = 140`** is the smallest round value
  meeting it, and is also the only cap at which P recovers. The two criteria agree.

### 5.1 Why the cost probe alone was not allowed to set this

The first cost probe reported `p95 ≈ 20` Krylov directions, which would have justified
`max_gmres = 40`. That `p95` was measured over **three epochs only**, all far from the solution,
where the linear solve converges easily. P collapses outright at `max_gmres = 50`.

Had the caps been set from that probe, a `no` at G1 would have been an artefact of the budget
rather than a fact about orbits — precisely the under-resourced null §3d forbids. Clause (a) is
therefore read against **P's measured floor**, not against a probe `p95` alone, and P doubles as
the cap-adequacy test: *if P cannot recover an exact planted solution at the caps the attempts
use, those caps are too small.*

## 6. Measured cost, and the envelope

Second cost probe, run at the fixed `max_gmres = 140` on seeds anchored to named Table IV
periods (T ≈ 14.75 and 17.0), two attempts concurrent with the DNS:

* **≈ 40 s per epoch per attempt**, measured over a 180 s window.
* Both probe attempts *stall* rather than converge — residuals flatten at ‖R‖ ≈ 2.31 and 1.10
  with the trust-region radius decaying geometrically.

The stall is **not** evidence on G1: the probe's seeds come from a T=2000 DNS, which is leg
353's own under-resourced scale — the length whose null §3d already re-read as UNDER-RESOURCED
rather than NO. What transfers from the probe is cost, not outcome. A Jacobian action is one
integration over the orbit period and costs the same seconds whichever DNS the seed came from.

Envelope arithmetic, with `N = max_newton` and `W` workers over 100 attempts:

```
worst case  =  40 s × N × ceil(100 / W)      against the pre-registered 8 h = 28800 s
```

so `W = 10` admits `N ≤ 72` before contention, and less after it. Clause (b) of the cap rule
requires `max_newton ≥ 2 ×` the median epochs to convergence-or-stall. If clauses (a) and (b)
cannot **both** be met inside the envelope, the pre-registration is explicit:

> U3 does not report a `no`. It reports the shortfall as a cost and **G1 answers
> `UNDER-RESOURCED`** per §3d, naming the wall time a compliant attempt would need.

## 7. Realization note (lesson 91)

Carried into G1's answer because a negative names its realization. The stepper is
**Lie–Trotter split and therefore globally first order**, not fourth: RK4 is applied to the
nonstiff part only, then composed with the exact viscous factor. Confirmed by two independent
measurements (local order ratio 4.00, global ratio 2.00).

This **corrects M1's recorded mechanism without changing any M1 number**: M1 attributed its
`||R(w_lam)|| = 0.0794` floor to RK4 truncation at `dt = 0.01`, but `||rhs_physical(w_lam)||
= 7.8e-14` — RK4 truncation where the RHS vanishes identically is exactly zero. The floor is
splitting error. The stepper was **not** changed to Strang: that would alter the realization M1
was validated against and discard an in-flight DNS, and it is outside U2/U3's scope. It is
recorded as the top successor item instead.

Bearing on G1's matching predicate: `MATCH_T_TOL = 0.05` is 0.26% on T ≈ 19.334, against a
measured 0.13% systematic period offset — covered by a factor of only ~2. Reported as a
magnitude, not waved away.

## 8. What is and is not established

**Established (UNVERIFIED, §3f):** one false-negative path in `newton_hookstep_rpo` is closed
and M1 is unaffected; `max_gmres = 140` is fixed by clause (a) and corroborated by P's floor;
P recovers an exact planted solution at those caps; per-epoch cost is ≈ 40 s.

**Not established:** G1 in either direction. M2. That any Table IV orbit is recoverable. That
the solver has no other defects. Nothing here is a null result — a null requires an attempt
resourced at the scale the question is posed at, and that attempt has not yet run.

**Obligations.** `CLAY_OBLIGATIONS` §6's two no-method obligations stay **OPEN**; §4 stays
**OPEN and NOT discharged**. Ceiling **TIER 2**. No `L1→L4` link moved. Clay ~0.05%.
