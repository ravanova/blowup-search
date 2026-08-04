# Route-L v1 — the 2D preconditioner: the stall attributed, and removed

*Phase 2 / P2, leg 44. Figure: `writeup/figures/fig41_route_l_v1_precond.png`.
Code: `solver/port_certification.py` (Route-L additions), `test_port_certification.py`
(10/10), `experiments/p2_route_l_v1_precond.py` →
`writeup/data/p2_route_l_v1_precond.json`. Working notes: `PHASE2_P2_NOTES.md` §33.*

**Step (iii) of the certification chain — an approximate inverse `A` with a computable
`Z₁` — was declared unreachable on this discretization by Route-K. It is now reachable: an
`O(N)` exact sweep takes the Krylov stall from 0.6623 (flat) to 3.3e−6. That is the first
time in 44 legs a blocked link has opened. Steps (i) and (ii) remain blocked, for a
different reason, and the obvious explanation for that reason was tested and refuted. No
link of the L1→L4 chain moved. Clay odds unchanged at ~0.05%.**

---

## 0. What this leg is, in one paragraph

Route-K stopped the port at step (iii) with the obstruction half identified: the
leading-order **radial** dilation split took the stall 0.6623 → 0.3596 and **the curve
stayed flat**, so something else of comparable size remained. Route-K named two candidates
— the nonlocal Biot–Savart velocity, and the wall. This leg tests them by ablation. **Both
are wrong.** The real term was not on the list, and once found it names its own
preconditioner, which works. Then Newton is tried again, still fails, and fails
*differently* — and the obvious explanation for the new failure is tested and does not hold
either.

---

## 1. L1 — the attribution battery

Six ablations of the residual map, each with its own Krylov ladder, ranked by **how much the
ladder bends** rather than by where it ends (lesson 72 — an ablation that removes the
obstruction makes the curve bend, and a curve that ends lower while staying flat has removed
nothing). Gate: the un-ablated variant reproduces `solver.rhs` to **0.0**, so the battery is
measuring ablations and not a reimplementation.

| ablation | `m`=10 | 160 | gain | flat? |
|---|---|---|---|---|
| **pure dilation, no angular** | 0.7518 | **0.1608** | **4.68** | no |
| **angular transport OFF** | 0.7857 | **0.3712** | **2.12** | no |
| velocity in `s_ρ` OFF | 0.6111 | 0.3599 | 1.70 | yes |
| reaction terms OFF | 0.7552 | 0.5817 | 1.30 | yes |
| velocity feedback OFF | 0.8456 | **0.7582** | 1.11 | yes |
| *full* | 0.6946 | 0.6623 | 1.05 | yes |

**The two candidates Route-K named are both eliminated.**

* **The nonlocal velocity is not the obstruction — removing it makes things *worse*.**
  Freezing the Biot–Savart feedback (velocity and modulation held at the base state, so
  `δu` no longer responds to `δω`) takes the stall from 0.6623 to **0.7582**. The nonlocal
  term is mildly *helping* the Krylov solve. This is the only row in the battery that is
  worse than the full problem, and it is the one Route-K's writeup put first.
* **The wall is not the obstruction either** — §2 measures that directly.

**The angular transport is.** Switching off `s_β ∂_β` bends the ladder to 0.3712 (gain
2.12); switching off *both* transport pieces bends it to 0.1608 (gain 4.68). And the
decisive combination is in Route-K's own preconditioner: **angular transport off *plus* the
radial preconditioner runs to machine zero** (0.0401 → 0.0171 → 0.0006 → 0.0 → 0.0). So the
transport operator carries the **entire** obstruction, in two pieces, and nothing else in
the equation contributes.

## 2. L2 — the wall hypothesis, retired by measurement

Route-K found the *relaxation's* surviving defect at the wall, and inferred the Krylov stall
might live there too. It does not. Taking the stalled solve at `m = 160` and computing where
its residual energy sits, in the first three of forty-eight angular nodes (**proportional
share 0.0625**):

| field | wall share | vs proportional |
|---|---|---|
| `ω` | 0.0685 | 1.10× |
| `η` | 0.0794 | 1.27× |
| `ξ` | 0.2745 | 4.39× |

`ω` and `η` are **flat across the domain** — the obstruction is distributed, which is what a
continuum looks like and is not what a boundary-layer problem looks like. Only `ξ` shows a
genuine wall concentration, and `ξ` is not what carries the stall. **Two different defects
were being conflated: the relaxation's, which is at the wall, and the linear solve's, which
is not.**

---

## 3. L3 — the preconditioner, and the negative that made it obvious

### 3.1 What does not work, and why it is worth reporting

The natural move once "radial plus angular" is the answer is to invert each direction
exactly and compose them — classic ADI. **It is catastrophically worse than doing nothing:
0.9960 against 0.6623.** The operator does not split, and composing two exact 1D solves
carries a splitting error larger than the thing being fixed. This is kept in the artifact
and in the module because it is load-bearing: it is what forces the correct construction
rather than merely permitting it.

### 3.2 What does work

**The radial upwinding is outward everywhere on this profile** — measured `s_ρ ∈ [0.390,
5.732]`, strictly positive, and reported as a magnitude so a marginal case would be visible
rather than binary. That single fact makes the *coupled* transport operator **block lower
bidiagonal in the radial index with tridiagonal diagonal blocks**:

```
[(c − s_ρ/dρ) I − s_β ∂_β] f_i  =  rhs_i − (s_ρ/dρ) f_{i−1}
```

so **one outward sweep of Thomas inverts it exactly**, in `O(N)`, with **no splitting error
at all** — because there is no split. Gated (`test_7`): applying the full transport operator
to its own sweep returns the right-hand side to **9.5e−16**.

| preconditioner | `m`=10 | 40 | 160 | 240 | 320 |
|---|---|---|---|---|---|
| none | 0.6946 | 0.6908 | 0.6623 | — | — |
| radial only (Route-K) | 0.4463 | 0.4215 | 0.3593 | — | — |
| ADI composition | 0.99999 | 0.99852 | 0.99604 | — | — |
| **full transport line sweep** | **0.1830** | **0.1313** | **0.0188** | **2.0e−4** | **3.3e−6** |

**The ladder stops being flat.** Route-K's stall verdict classifies the sweep's curve as
*bending* (gain 9.72 across the ladder, against the full problem's 1.05) — which is the
same classifier, on the same data structure, returning the opposite reading. `A` is
constructible. **Step (iii) is unblocked.**

---

## 4. L4/L5 — Newton still fails, differently, and the obvious explanation is wrong

With the linear solve working, the question Route-K left downstream becomes askable.

**The linear solves now succeed: GMRES relative residual 2.5e−3 in 200 iterations, against
1.00 before.** And **Newton still does not converge.** `‖F‖₂` creeps 0.8069 → 0.7378 over
eleven steps — a factor of 1.09 — with the line search accepting only **λ = 1/32** at the
first step and 1/64 thereafter.

That is a *different* failure mode, and the difference is the finding. A full Newton step
being rejected while the linear system is solved accurately is not a spectral problem; it is
the signature of a **near-null direction in `DF`** — Newton computes a large step along a
direction the residual barely sees, and the line search cuts it back.

**The obvious candidate was the scaling gauge, and it is refuted.** `run(renorm=True)`
re-pins `ω_x(0)` and `η_x(0)` after every relaxation step; `F` carries no such constraint,
so Newton is free to wander along the scaling symmetry. Applying the same projection inside
Newton is a two-line test, and it makes things **strictly worse**: at the very first
iteration the line search accepts **no step at all** (λ falls to 1/1024 and is still
rejected), and `‖F‖₂` does not move from 0.8069.

So the near-null direction is **not** the scaling gauge. It is recorded as unidentified,
which is the honest state, and the next leg's job is to find it — the direct route is to
compute the smallest singular directions of the preconditioned Jacobian, which is now cheap
*because the preconditioner exists*.

---

## 5. Where the chain stands

| step | before this leg | after |
|---|---|---|
| (i) a fixed profile `x*` | BLOCKED | **still blocked** — different reason |
| (ii) `Y₀`, the defect | UNDEFINED | **still undefined** |
| (iii) `A ≈ DF⁻¹`, `Z₁ < 1` | NO `A` | **UNBLOCKED** |
| (iv) the radii polynomial | not reached | not reached |

One link opened. It is the link Route-K called impossible on this grid, and it opened
because the obstruction was *attributed* rather than guessed at — both guesses were wrong,
and the battery is what found the right term.

**What this is not.** Not a certificate; nothing is interval-enclosed and `Z₁` itself is
still unmeasured (there is no profile to evaluate it at). Not a claim about the object —
Chen–Hou certified this profile, and this leg is about our discretization. And **not
progress on the chain**: (i) and (ii) are exactly where Route-K left them.

## 6. What must be built next, in order

1. **Identify the near-null direction of the preconditioned Jacobian.** Cheap now: a few
   inverse-iteration or Lanczos steps through `M⁻¹DF`. The gauge is ruled out; the
   candidates worth checking are the `c_l`/`c_ω` modulation's implicit dependence (which
   makes `F` an implicitly-defined map, not an explicit one) and translation along the
   profile branch.
2. **A bordered system**, once (1) names the direction — append the constraint that pins it,
   rather than projecting after the fact, which is what failed here.
3. **Then** the profile, the function space, `Y₀`, and `Z₁`.

## 7. Reproduce

```bash
.venv/bin/python -u experiments/p2_route_l_v1_precond.py     # ~13 min
.venv/bin/python writeup/4_p2_lottery/p2_route_l_v1_evidence.py
.venv/bin/python test_port_certification.py                  # 10/10
```
