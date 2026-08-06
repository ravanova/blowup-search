# Route-PORT v1 — the bordered system, and a certificate that closes around the wrong object

*Phase 2 / P2, leg 46. Code: `solver/bordered_hl.py`, `test_bordered_hl.py` (10/10),
`experiments/p2_route_port_v1_bordered.py` →
`writeup/data/p2_route_port_v1_bordered.json`. Working notes: `PHASE2_P2_NOTES.md` §35.
Plan stage `PORT` (`plan_of_record.py`).*

**The radii polynomial closes in float, at every rung, on an object nobody has certified —
and the ball it produces is 1.55e+08× too small to contain that object. Both are true, the
second was pre-committed as a predicate before the first was known, and the second is the
result. No link of the L1→L4 chain moved. Clay odds unchanged at ~0.05%.**

---

## 0. What this leg is

Route-M named the target: `HL_S2_nonsymmetric`, the strictly positive, regular,
**non-symmetric** self-similar profile of the 1D Hou–Luo model (Chen–Huang–Li,
arXiv:2604.01868 §2.5/§4), reported April 2026 as a *"previously unreported blowup
phenomenon"* — **numerical only, no proof of any kind, computer-assisted or otherwise.**
This leg builds the certification chain on it and reports where the chain stops.

It stops later than it ever has. Route-K could not define `Y₀` at all (no fixed profile);
Route-L unblocked the linear solve but Newton still would not converge. Here Newton
converges to machine residual, `Y₀`, `Z₁` and `Z₂` are all measurable, and the radii
polynomial closes. Then the pre-committed ceiling clause fires.

---

## 1. Bordered from the start, because leg 44 tried it the other way

The steady form of CHL's rescaling (4.1), evolving `V := Θ_X`, is

```
(U + c_l X + c_r) Ω_X = c_ω Ω + V
(U + c_l X + c_r) V_X = (2 c_ω − U_X) V
U_X = H(Ω),   U(0) = 0
```

with **three** unknown constants, because the system carries exactly three continuous gauge
freedoms — amplitude, dilation, and **translation** (the last is why there are three and not
two: a non-symmetric profile has no symmetry point to pin it). So the square system is `2n`
equations against `2n + 3` unknowns: three short. CHL's normalization (4.2) supplies exactly
three **border rows** pinning `Ω(0)`, `Ω_X(0)`, `V(0)`.

**This shape is a direct consequence of leg 44 (L-7).** On the 2D object we solved first and
projected the constants afterwards, and Newton accepted no step at all — λ down to 1/1024.
Here the constants are unknowns of the *same* Newton system from the first iterate.

**And the ablation confirms the borders are load-bearing, not decorative:** drop them and the
solve does not converge — residual **1.42e−2 after 60 iterations**, against 1e−14 in 4 with
them. That is the same failure the relaxation has, which is the point.

## 2. Newton converges where the relaxation floors

| `n` | residual | iters | `c_l/c_ω` | vs CHL |
|---|---|---|---|---|
| 201 | 5.66e−15 | 16 | −2.541222 | 1.187% |
| 301 | 7.61e−15 | 4 | −2.541024 | 1.180% |
| 501 | 1.25e−14 | 4 | −2.540873 | 1.174% |
| 801 | 3.12e−14 | 4 | −2.540791 | 1.170% |
| 1201 | 3.52e−14 | 4 | −2.540746 | 1.169% |

`solver/hl_rescaled.py::RescaledHLScenario2` time-steps these same equations with the same
origin gauge and **floors at residual ~1e−2** — its own leg said so in advance. The far field
is why: the steady equation forces an **algebraic** tail `Ω ~ |X|^(c_ω/c_l) ~ |X|^−0.394`, and
a relaxation started from compactly-decaying data must transport that tail outward across a
domain reaching `|X| ~ 745`. **Newton does not transport anything; it solves.** That is the
entire reason a defect `Y₀` exists here and did not in Route-K.

### 2.1 The 1.17% gap is reach, not resolution — and it extrapolates

The ratio is resolution-converged to the fourth decimal and still sits 1.17% from CHL's
−2.5114. The ablation ran reach, stretch and datum **together, before naming a suspect**
(lesson 74), and reach is the one that moves it:

| `ρ_max` | `X_max` | `c_l/c_ω` |
|---|---|---|
| 6 | 100.9 | −2.583087 |
| 7 | 274.2 | −2.557642 |
| 8 | 745.2 | −2.541024 |
| 9 | 2025.8 | −2.530473 |

A power law in `X_max` with slope **−0.437** — consistent with the tail exponent −0.394 —
extrapolating to **−2.511926 against CHL's −2.5114, a relative error of 2.09e−04.** Two
independent extrapolation windows agree to **0.93%**. The gap is the finite domain, and
naming it that is what lets the certificate be read as a statement about a *truncated* object
rather than a wrong one.

## 3. The certificate closes — and the space is what closes it

`Y₀`, `Z₁`, `Z₂` in a weighted sup norm, `A = DF⁻¹` in float64:

| `n` | tuned `Y₀/budget` | naive `Y₀/budget` | gain |
|---|---|---|---|
| 201 | **1.95e−04** ✓ | 1.0125 ✗ | 5186.6 |
| 401 | **6.36e−04** ✓ | 3.3193 ✗ | 5221.5 |
| 801 | **2.40e−04** ✓ | 1.2578 ✗ | 5235.6 |

**Closure is a property of the space, not of the object.** The two columns differ in a single
constant — the length scale `w_l` in the weight, `0.01 X_max` against `X_max` — and that one
number is worth **~5200×**, which is the difference between closing and not closing at every
rung. This was found before stage `B` was scheduled and is the empirical case for it.

**There is also a hard boundary on the weight, and it is set by the object.** The profile's
own tail is `Ω ~ |X|^−0.394`, so a weight `(1 + X²)^(p/2)` with `p > 0.394` makes the **true**
profile's norm infinite. `p* = 0.39` is not tuned; it is the largest exponent the object
admits. Any search over this space (stage `B`) is searching a box with one wall already
built by the equation.

## 4. The ceiling — pre-committed, and it is the result

Clause **P6b** was written into the driver's predicate list before the certificate was
computed: *how far is the truncated object from the less-truncated one, measured in the
certificate's own norm?*

```
||z(X_max = 745) − z(X_max = 2026)||  =  1.831e−01     (worst block: Ω)
the float ball                        :  r ∈ [2.97e−12, 1.18e−09]
                                          1.55e+08 × r_max
```

**The certificate closes around the truncated object. The true object is eight orders of
magnitude outside the ball.** A real proof must fold the truncation error into the budget,
and at present that is not close to affordable.

This is the honest reading of the headline. "The radii polynomial closes" and "the ball does
not contain the thing we care about" are both true simultaneously, and reporting only the
first would be the exact failure mode `WIN_CONDITION.md` exists to prevent.

## 5. What this is and is not

* **A float rehearsal, not a proof.** `A` is `DF⁻¹` in float64, so `Z₁` measures the
  *conditioning* of the discretized problem rather than bounding an operator norm on a
  function space. Nothing is interval-enclosed. Same boundary Route-D v16 drew.
* **Not a certification of CHL's object.** It is a certification-shaped computation about a
  finite-dimensional truncation of it, with the distance to the real thing measured and
  reported as too large.
* **Not a link of the chain.** The chain requires Tier 3. This is the closest this project
  has come, and §4 is why that is not the same as progress.
* **What it does establish:** the machinery works end to end on an uncertified object — Newton
  converges, the defect exists, the bounds assemble, the polynomial closes — and the two
  things standing between here and a real result are now *named and quantified*: interval
  arithmetic, and the truncation budget.

## 6. Reproduce

```bash
.venv/bin/python -u experiments/p2_route_port_v1_bordered.py   # ~17 s
.venv/bin/python test_bordered_hl.py                           # 10/10
```

Pre-committed predicate: **7/7 hold** — `P1` Newton converges at every rung, `P2` `F` is
exactly quadratic, `P3` the ratio is resolution-converged, `P4` the gap is attributed to
reach, `P5` the polynomial closes in float, `P6a` the naive weight fails at the finest rung,
`P6b` the truncation distance exceeds `r_max`.
