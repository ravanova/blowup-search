# Route-K v1 — the L1→L2 certification port, step one

*Phase 2 / P2, leg 43. Figure: `writeup/figures/fig40_route_k_v1_port.png`.
Code: `solver/port_certification.py`, `test_port_certification.py` (6/6),
`experiments/p2_route_k_v1_port.py` → `writeup/data/p2_route_k_v1_port.json`.
Working notes: `PHASE2_P2_NOTES.md` §32.*

**Ranked item (3), deferred six times, attempted. The kill-switch fires at `Y₀` — before
the function space is reached — and the leg is the mechanism plus the controls that make it
a statement about the object rather than about our instrument. No link of the L1→L4 chain
moved; a blocked link is not a moved link. Clay odds unchanged at ~0.05%.**

---

## 0. What this leg is, in one paragraph

The directive named four deliverables: the Newton–Kantorovich setup on the 2D Boussinesq
profile with the function space chosen with Route-D's `a = 0`-only disaster in mind; an
honest `Y₀`; a first bound on `Z₁`/`‖A‖`; and a kill-switch that **stops and reports rather
than hardens** if the radii polynomial does not close in float with margin. This leg gets
two steps down that list and stops, because the first two steps do not have referents:
**there is no fixed profile for `Y₀` to be the defect of, and no approximate inverse `A`
for `Z₁` to be about.** Both are measured, both are controlled, and the second one comes
with a mechanism and a partial repair.

That is the outcome the directive said was worth having — *"even '`Y₀` is machine-level but
`Z₁` diverges, and here is the mechanism' moves the project further than any 1D leg has."*
It is one rung earlier than that, and it is more specific.

---

## 1. The chain, and where it breaks

A radii-polynomial argument needs, in order:

```
(i)   a fixed profile x*  with  F(x*) = 0
(ii)  Y_0 >= ||A F(x*)||                    -- the DEFECT of that profile
(iii) A ~ DF(x*)^{-1},  Z_1 >= ||I - A DF|| < 1
(iv)  Z_2 r^2 - (1 - Z_1) r + Y_0 <= 0  having a root
```

**(i) BLOCKED. (ii) UNDEFINED. (iii) NO `A`. (iv) not reached.**

`radii_polynomial_status(None, None)` returns `BLOCKED_AT_STEP_ONE` and — gated — carries
**no fabricated `Y₀` or `Z₁`**. That matters: substituting a plausible bound would have
turned "there is nothing to bound" into "the bound is too big", which reads as a
quantitative shortfall and is a materially weaker and less true statement.

---

## 2. K1 — the relaxation has no fixed point

`RescaledBoussinesq.run` is an SSPRK3 relaxation toward a steady state, and it is the only
way this project has ever produced a 2D profile. It does not converge in either sense.

**In time, it limit-cycles.** Over a ladder of step counts at `n_r = 200`, `n_β = 48`,
`r_max = 10⁵`:

| steps | `‖F‖_∞` | `c_ω` | `c_l/c_ω` |
|---|---|---|---|
| 500 | 0.9757 | −1.244404 | −2.45948 |
| 1500 | 0.2060 | −1.019573 | −3.00184 |
| 3000 | **0.0257** | −1.014506 | −3.01683 |
| 5000 | 0.2290 | −1.239439 | −2.46934 |

The residual falls by a factor of 38 and then rises by a factor of 9. `c_ω` swings between
−1.0145 and −1.2444, and the ratio swings between −3.017 and −2.459, **straddling the
published Chen–Hou −2.9206 without settling on it**.

**Under refinement, it gets worse.** This is not our run — it is Route-G's own committed
resolution ladder, read out of `writeup/data/p2_route_g_v1_g2.json`:

| `n_r` (at `r_max = 10⁵`) | steady `‖F‖_∞` | `c_ω` |
|---|---|---|
| 300 | 1.671e−2 | −1.026565 |
| 450 | 7.708e−2 | −1.023312 |
| 600 | 2.667e−1 | −1.031202 |

**The steady-state residual grows 16× as the grid is refined 2×.** A converging
discretization does the opposite.

**And the uncomfortable pairing is the interesting part: `c_ω` does not notice.** Across
that same ladder `c_ω` holds to **0.77%**. The modulation reads a resolution-stable
quantity off an object that is not converging — which is possible because the modulation
(2.11) is a *local* read at the origin, and the residual that grows lives elsewhere. Route-G
was right that its number is resolution-stable, and this leg is why "resolution-stable"
was not the same as "converged".

**A consequence Route-G's writeup should carry:** its `β = 2.98 ± 0.02` against the
published 2.9206 is **2.1% out, which its own quoted spread does not cover** — a
disagreement of 2.5 spread-widths. That is now explicable rather than mysterious.

### 2.1 K2 — where the defect lives

Tracking the argmax of each field's residual in `(r, β)` across the ladder: the early
transients sit mid-domain (`r ≈ 10²`) and at the outer edge (`r ≈ 7×10⁴`, i.e. the Robin
boundary), and once those clear, **the survivor is the wall, `β ≈ 0.032`, the first
interior angular node**, at moderate `r ≈ 1–14`. Panel C draws the migration.

That localisation is actionable: the wall is exactly where the Hou–Luo geometry's difficulty
is, and it is where Chen–Hou needed a weighted `L^∞` + `C^{1/2}` pairing rather than a
weighted `L²`. It is not a grid artifact at the outer edge and it is not the corner.

---

## 3. K3 — the instrument, gated before the operator is blamed

Everything in §4 is of the form "the solve stalled", which is precisely what a broken solver
produces. So the solver is gated first (banked lesson 47).

**The GMRES is correct, and its ill-conditioning failure mode is calibrated.** The same
routine solves a well-conditioned dense system to **7.6e−11 in 19 iterations** (reported
residual agreeing with the true one), and on a deliberately `cond ≈ 10⁸` dense system it
stalls at **0.086 after 200 iterations**. That second control is the yardstick: it says what
ill-conditioning *alone* costs, and the real Jacobian does substantially worse.

**The finite-difference Jacobian-vector product is trustworthy.** `‖Jv‖ = 65.140`, flat to
within **3.5e−6 relative across the whole sweep** of `h/‖z‖` from `1e−4` to `1e−9`, with a
best inter-rung drift of **6.3e−8**. The matvec is not the noise floor.

---

## 4. K4 — `DF` has no computable approximate inverse, and the curve is flat

A matrix-free Krylov solve of `DF x = −F`, reported as a **ladder in the Krylov dimension**
rather than as a single number — because the shape of the ladder is the measurement:

| `m` | 10 | 20 | 40 | 80 | 160 |
|---|---|---|---|---|---|
| unpreconditioned, best of cycle | 0.6946 | 0.6927 | 0.6908 | 0.6853 | **0.6623** |
| + leading-order preconditioner | 0.4463 | 0.4388 | 0.4213 | 0.3960 | **0.3596** |
| unpreconditioned, worst of cycle | 0.2695 | 0.2653 | 0.2610 | 0.2589 | **0.2450** |
| + leading-order preconditioner | 0.2388 | 0.2384 | 0.2377 | 0.2373 | **0.2367** |

**Sixteen times the Krylov work buys 5%.** A merely ill-conditioned operator gives a curve
that *bends down* once GMRES has captured the extreme eigenvalues — the `cond ≈ 10⁸` control
reaches 0.086. A curve that is **flat in the Krylov dimension** is the signature of a
spectrum with a **continuum** in it. That is the same object Route-E measured in 1D as the
essential spectrum, and it is exactly what Route-J's lesson (70) says must have its
realization named — our log-polar grid imposes no condition at the singular corner.

### 4.1 The one repair with a principled basis, tried

At large `r` the transport speed `s_ρ → c_l`, so the leading operator is
`−c_l ∂_ρ + (diagonal damping)`, whose spectrum on a log-radial grid fills a band. Upwinded
outward it is **lower bidiagonal per angular line, hence exactly invertible in `O(N)`** — a
gated fact, not an assumption (`test_2` applies the operator to its own solve and recovers
the right-hand side to 3.9e−16). It is also the same split Chen–Hou describe in their own
abstract: *"we decompose the linearized operator into a leading order operator plus a finite
rank operator."*

**It helps, and it does not fix it.** At the best point of the cycle the stall goes
0.6623 → 0.3596, a factor of **1.84**, and the curve stays flat. Nearly halving the stalled
residual says the dilation continuum is a real and *identified* part of the obstruction; the
curve staying flat says **there is a second obstruction of comparable size that the
leading-order operator does not touch.** The nonlocal Biot–Savart velocity and the wall are
the candidates. Separating them is the next leg.

### 4.2 The seed-dependence, which is the sharpest form of the finding

Everything above was quoted "at the best point of the limit cycle" and it had to be, because
**the answer depends on which point you linearize at.** At the worst point (`‖F‖₂ = 11.11`
against 0.807) the unpreconditioned stall is 0.2450 rather than 0.6623 — a **2.7× spread** —
and the preconditioner buys **1.03× rather than 1.84×**.

Neither number is *the* answer. "Linearize at the profile" has no referent when there is no
profile. **`Z₁` here is not large and is not small; it is not about anything.** Reporting a
single stall level would have been the most natural way to write this section and would have
concealed exactly the fact that makes it decisive.

---

## 5. What this is not

* **Not a proof that the 2D profile cannot be certified.** Chen–Hou certified this object.
  They did it with a different decomposition, a weighted `L^∞`/`C^{1/2}` pairing chosen for
  the boundary, and 145 pages. This is a measurement that *our* discretization does not
  admit the first two steps, with the mechanism named. The gap between "our grid cannot" and
  "it cannot" is the whole distance.
* **Not a retraction of Route-G's `β`.** `c_ω` is resolution-stable and that is a real
  property. What changes is the confidence interval around it: the 2.1% gap to the published
  value is larger than the quoted spread, and now has a cause.
* Plain float64. Nothing interval-enclosed, nothing rigorous.
* **Not the function space.** The directive's item (1) — choose the space, checking on day
  one that it carries the *2D* terms — was not reached, because choosing a space in which to
  measure the defect of a non-existent profile is not a well-posed task. It moves to the
  next leg, behind the preconditioner.

---

## 6. What must be built next, in order

1. **A preconditioner that also covers the nonlocal Biot–Savart velocity and the wall.** The
   dilation split accounts for about half the stalled residual at one seed and almost none at
   the other; the remainder is where the next leg goes. Chen–Hou's finite-rank correction is
   the model, and `Papers/2210.07191.pdf` §7 is the section.
2. **A profile from a converged Newton solve, not a relaxation.** This is *downstream* of
   (1): Newton stalls for the same reason the Krylov solve does — a prototype run reduced
   `‖F‖₂` from 0.807 to 0.549 in fifteen Newton steps and then flatlined, with the linear
   solve returning a relative residual of 1.00.
3. **Only then**: the function space, `Y₀` in it, and `Z₁`.

The honest cost estimate is that (1) is a leg in itself and (2) is another. That is what the
port costs, and it is worth saying plainly rather than discovering it a seventh time.

---

## 7. Reproduce

```bash
.venv/bin/python -u experiments/p2_route_k_v1_port.py    # ~9 min
.venv/bin/python writeup/4_p2_lottery/p2_route_k_v1_evidence.py
.venv/bin/python test_port_certification.py              # 6/6
```
