# Route-D v11 — Newton on the profile: the 1e-2 floor was the search

**Status: Level-1 tooling + a structural positive. NOT a certificate, NOT
rigorous, NOT a Clay result.** Plain float64.

**Figure:** `fig29` · **Data:** `writeup/data/p2_route_d_v11_anchor.json`
**Code:** `solver/profile_newton.py` (+ `test_profile_newton.py`, 6/6),
`experiments/p2_route_d_v11_anchor.py`, `p2_route_d_v11_evidence.py`

---

## 0. Why this leg

v10 measured what sharpening the constants can buy: a perfect `‖A‖` bound
multiplies the budget by 7.7, `C_Q`'s slack is ~4×, and the product only just
reaches the residual floor of ~1e-2 with nothing spare for the three open `Z₁`
items. **The constants alone cannot close the gap.**

`Y₀` — the candidate profile's *defect* — enters the radii polynomial linearly
and has never been attacked. Every `a ≠ 0` profile in this project came from a GA
over a small parametric genome or from fixed-grid dynamic relaxation, both of
which floor around 1e-2. Nobody had asked what Newton does.

## 1. The solve

Unknowns `(Ω, c)`; equations `R₂ = Ω H(Ω) − c Ω_X − a U Ω_X = 0` plus **two**
gauges. Two, not one: the `a = 0` zero set is the two-parameter family
`A/(1+B X²)` (§9), which Route-D v1 Q2 already found — one gauge leaves the
Jacobian singular and a direct solve crawls to **1.8e-6 in 40 iterations**, while
two gauges in least squares reach **2e-15 in 5**. The Jacobian is exact
(finite-difference agreement 6.6e-11), assembled from the operators
`solver/gclm_family` already caches.

Gate: at `a = 0`, Newton from a perturbed start finds a zero of the **discrete**
system at 1.1e-15, while the exact continuum anchor scores **7.7e-9** on the same
equations — its own discretization error. A solver reproducing the continuum
profile exactly would be reporting something impossible.

## 2. V2 — the floor was the search

Continuation in `a`, relative residual:

| a | 0 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 |
|---|---|---|---|---|---|---|
| Newton | 9.7e-15 | 8.8e-15 | 2.7e-14 | 1.6e-13 | 9.6e-15 | 2.0e-14 |
| GA / relaxation | ~1e-2 | ~1e-2 | ~1e-2 | ~1e-2 | ~1e-2 | ~1e-2 |

**Twelve orders of magnitude.** The 1e-2 floor that §9 read as a property of the
problem — and that the banked discipline lesson records as a property of
fixed-grid relaxation — is a property of the **search**. With no genome at all,
the discrete equations have machine-precision solutions.

## 3. V4 — the check that decides, and the boundary that survives

Machine precision on a discrete system proves nothing by itself: a solver can
null discrete equations with something that has no continuum limit. The test is
whether the *solution* stops moving as `n` grows.

| a | 0.0 | 0.2 | 0.5 | 0.8 | 1.0 |
|---|---|---|---|---|---|
| spread in `c` over n=401/801/1601 | 8e-4 | 3e-4 | **3e-5** | 3.7e-3 | 1.3e-2 |
| grids reaching machine precision | 3 | 3 | 2 | **1** | **1** |
| continuum object? | yes | yes | **yes** | **no** | **no** |

So Newton's own convergence is *not* the boundary test — it succeeds at isolated
large `a` where the solution is not grid-converged. On the test that matters,
solutions exist up to `a ≈ 0.5` and not beyond.

**That is the GA's survival boundary `a* ≈ 0.5–0.55`, confirmed a fourth time —
now by a method with no genome, no search budget and no stochasticity.** §9-cont2
earned it with GA-, genome- and basis-convergence; this adds method-convergence,
and sharpens the character: below `a*` an exact discrete traveling wave *exists*.

## 4. V5 — what this does and does not do to `Y₀`

The certificate does not see the RMS residual. It sees the **weighted sup
defect** `sup (1+X²)^{(α+1)/2}|R₂|`, and that behaves differently:

| a | 0.10 | 0.20 | 0.30 | 0.40 | 0.45 | 0.50 |
|---|---|---|---|---|---|---|
| RMS | 8.8e-15 | 2.7e-14 | 1.6e-13 | 9.6e-15 | 1.6e-9 | 2.0e-14 |
| **weighted** | 2.3e-14 | 1.1e-8 | 2.2e-7 | 2.4e-8 | **1.5e-2** | 7.5e-7 |

Six or more orders larger, because the codomain weight amplifies exactly the far
field where the truncation lives — and **not uniformly under the budget**
(2.45e-4): `a = 0.45` is above it.

The honest conclusion is a *change of binding constraint*, not a solved problem:

> `Y₀` is no longer **search**-limited. It is **discretization**-limited — and
> that is an item already on the ledger (`Z₁` core discretization, v4 W6 measured
> `J^{−2.1..−2.6}` and never bounded it).

"Find a better profile" was the wrong problem. "Control the far-field
discretization of the profile we can now compute exactly" is the right one, and
it is more tractable: it is a statement about a known object rather than a search.

## 5. Ledger and next

Coverage unchanged. What changed is which item binds:

1. **Carry the Newton profile into the θ-collocation basis the bounds live in**,
   and measure `Y₀` there — the two discretizations are different and the number
   above is in the Route-A one.
2. **Price the core discretization error** — now the binding item for `Y₀`.
3. `C_sup` (elasticity ≈ 1, ~2× available).

## 6. Reproduce

```
.venv/bin/python test_profile_newton.py                            # 6/6, ~10 min
.venv/bin/python experiments/p2_route_d_v11_anchor.py              # ~25 min
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v11_evidence.py   # fig29
```

## 7. Where this sits relative to Clay

The programme's end goal is the Clay problem, so each leg should say which link of
the chain it moved. The chain is:

| link | what it is | status |
|---|---|---|
| **L1** | a certified self-similar blow-up profile for the **1D gCLM/HL toy model** at some `a > 0` | **where this work is; not finished** |
| **L2** | the same for a model with a genuine 2D/3D mechanism (2D Boussinesq / axisymmetric Euler with boundary) | done by others for specific data |
| **L3** | a certified blow-up for **3D Euler** without boundary or symmetry crutches | open frontier |
| **L4** | the same for **3D Navier–Stokes** | this is Clay |

`L2→L3` and `L3→L4` are each widely regarded as harder than everything below them
combined; these are not increments.

**Which link did v11 move?** None of them. It moved an *input* inside `L1`: it
showed that the `10⁻²` residual floor five legs had treated as a property of the
equation was a property of the search, and that below `a* ≈ 0.5` an exact discrete
traveling wave exists. That makes `L1` look closer than it did — the defect is no
longer the obstacle — but the binding constraint moved to far-field discretization
rather than disappearing, and `L1` is still not done.

Two structural walls cap the whole programme regardless (CLAY_ROADMAP.md §2), and
no amount of good work removes them: a search/certification programme can only
argue **for** blow-up, so if 3D NS is globally smooth the direction is empty by
construction; and the only rigorous-proof technology that exists works on models
simple enough for interval arithmetic, which 3D NS is not. The realistic prize
remains a novel Tier-3 result on a toy model where blow-up is provable, with Clay
as a distal horizon.

## 8. Honest ceiling

Nothing here is a certificate: float64, nothing interval-enclosed, three ledger
items open. This is a Route-A tooling result that changes a Route-D input. The
eventual success this line scouts remains a computer-assisted toy-model
certification, not a Clay solve. Clay odds ~0.05%.
