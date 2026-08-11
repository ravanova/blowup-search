# TECHNICAL — Route-NLH v1 (leg 331): Breden–Chu's machinery against a nonlocal operator

**Arithmetic ceiling.** float64 throughout, *not* interval arithmetic. Every number below
is a magnitude, reproducing constants rather than enclosing them. Nothing here is a
rigorous enclosure and nothing here may be cited as one. `solver/interval_mp.py` was
available and was not needed: the obstruction is 100+ orders of magnitude wide, not a
precision question.

**Ban status.** No ban is lifted. The repository's `ell^1`-Fourier/radii-polynomial ban
covers the `ell^1_w` coefficient basis (leg 54), the collocation basis (leg 56) and
origin-`H^2` (legs 163/176). This leg works in Breden–Chu's `H^2(mu)` with the Hilbert
norm `||u|| = ||Lu||_{L^2(mu)}`, the half-Hermite basis, Sobolev-embedding taming and a
Poincaré tail — the same footing leg 256 banked. It claims no fourth space and does not
constitute a lift.

---

## 1. Object

Breden–Chu (arXiv:2404.04054v2) Theorem 42 concerns the generalised viscous Burgers
self-similar profile, their eq. (54), on

    H^2(mu),   mu = e^{|x|^2/4} / Z,   ||u||_{H^2(mu)} = ||L u||_{L^2(mu)},
    L = -Delta - (x/2) . grad,   L psi_m = lam_m psi_m,   lam_m = 1/2 + m,
    psi_m = L_m^{(-1/2)}(x^2/4) e^{-x^2/4} / Zeta_m = kappa_m H_{2m}(x/2) e^{-x^2/4},

in the even (Neumann) sector, `d = 1`. This leg changes one letter of eq. (54):

    L u - u/4 + u^2 W_t u = 0,     W_t = (1 - t) d_x + t Lam^{2a},     Lam^{2a} = (-Delta)^a.

`alpha = 1/2` gives `Lam = H d_x`, the Hilbert-transform realization (lesson 91: the
realization is named, not implied). `t in [0,1]` is a homotopy in nonlocality; `t = 0`
is eq. (54) verbatim.

## 2. The primitive

`psi_m` is not a Fourier eigenbasis. The identity `FT[H_n e^{-y^2}] ~ H_n` is **false**
here — Hermite *functions* carry `e^{-y^2/2}`, `psi_m` carries `e^{-y^2}`. From the
generating function `e^{2zt - t^2}` one gets a monomial amplitude,

    FT[H_n(x/2) e^{-x^2/4}](xi) = 2 sqrt(pi) (-i)^n (2 xi)^n e^{-xi^2},

whence, exactly, with no special-function dependency beyond `lgamma`:

    Lam^{2a} psi_m (x) = (2 / (sqrt(pi) m! Zeta_m)) Int_0^inf xi^{2m+2a} e^{-xi^2} cos(xi x) dxi.   (*)

`(*)` is evaluated in logs on a Gauss–Legendre panel rule in `xi`, with panel density set
by `cos(xi x_max)` and `xi_max = sqrt(n+1) + 9`.

### Known-answer gates on `(*)`, pre-committed

| gate | expected | measured max rel defect |
|---|---|---|
| `alpha = 0` | `Lam^0 psi_m = psi_m` | **4.388e-15** |
| `alpha = 1` | `-Delta psi_m = lam_m psi_m + (x/2) psi_m'` | **3.948e-15** |
| `solver/line_hilbert.py`, independent algorithm and grid | agreement | worst rel to peak **2.005e-03** |

The `alpha = 0` gate is the one that earned its place. The first (false) amplitude gave
`m = 0` exact to 1.2e-15 and every `m >= 1` at ~100% relative error, identical at 286 and
960 panels and at `x_max` 14 and 20 — resolution-independent, hence structural. Lesson 84:
the known-answer probe had a window, and `m = 0` was inside it.

## 3. Transcription and its grading

Every Breden–Chu formula is used unchanged with `d_x -> W_t` in the operator columns.
Their bounds were graded **before** any number was produced:

- **DERIVATION-FREE** (their algebra is operator-agnostic): `Y`, `Zbar11`, `Zbar21`.
- **TRANSCRIBED** (their derivations invoke locality): `Zbar12`, `Zbar22`, `Z2`, `Z3`.

A TRANSCRIBED number is a magnitude produced by their formula, not a bound their theorem
licenses for this operator. The grading is carried in the JSON.

## 4. Controls

| control | outcome |
|---|---|
| `t = 0` vs `bc.bounds` on all of `Y, Z1, Z2, Z3, Zbar11, Zbar12, Zbar21, Zbar22` | rel diff **0.0**, exactly, at all six (n, alpha) |
| M3 reference at `t = 0` vs local control | 1.617e-12 vs 1.62e-12 |
| half-line vs full-line convention | measured, not assumed: read **exactly 0.5** with a factor 2 present |
| local control Newton at n = 100 / 200 | residual 1.55e-16 / 5.45e-15 |
| trivial-solution guard | `u == 0` closes with `Y ~ 1e-29` at every `t`; flagged, never counted |

The `t = 0` regression is what licenses `t > 0`: the leg's bound code is bit-identical to
`solver/bc_weighted_sobolev.py`'s on the same coefficients. It could have differed.

## 5. Results

### 5.1 The image leaves the space (M1)

Symbol `|xi|^{2a} xi^{2m} e^{-xi^2}` is non-smooth at the origin only through `|xi|^{2a}`,
which is multiplied by a factor vanishing to order `2m`; the forced tail is
`x^{-(1+2a+2m)}`. Pre-registered, then measured at `m = 0`:

| alpha | predicted | fitted |
|---|---|---|
| 0.25 | 1.5 | 1.507674 |
| 0.50 | 2.0 | 2.012245 |
| 0.75 | 2.5 | 2.517908 |

Against `mu = e^{x^2/4}` this is fatal. `||Op psi_0||^2_{L^2(mu), |x|<R}`, `alpha = 0.5`:

| R | `Lam^{2a}psi_0` | control `d_x psi_0` |
|---|---|---|
| 4 | 0.9655 | 0.953988 |
| 8 | 1.196e3 | 0.999999477 |
| 12 | 5.872e10 | 0.9999999999999978 |
| 16 | **1.869e22** | 0.9999999999999993 |

The control saturates at 1; the nonlocal norm has no limit. `Lam^{2a}` does not map
`H^2(mu)` into `L^2(mu)`.

### 5.2 Finiteness is a horizon artefact (M1, rule horizon)

`log10` of the truncated weighted norm² evaluated at each rule's own largest node,
`alpha = 0.5`, `m = 0` (logs because at `n = 1500` it overflows float64):

| n | six-rule largest node | four-rule largest node | log10 nonlocal | log10 control |
|---|---|---|---|---|
| 100 | 30.66796 | 32.24163 | 95.151 | 0.0 |
| 200 | 43.50090 | 45.76315 | 197.728 | -3.9e-16 |
| 1500 | 119.72572 | 126.11696 | **1546.389** | -3.9e-16 |

`n = 1500` is Breden–Chu's own published resolution for Theorem 42. Refinement makes this
strictly worse: a larger `n` pushes the horizon further into the divergence. This is the
sense in which the machinery "produces finite bounds" for a nonlocal operator — it does,
and they are finite only because its quadrature stops before the divergence starts.

### 5.3 Quadrature exactness is lost (M3)

Their K-product Gauss–Laguerre rules (K = 6/4/2) are exact for polynomial×Gaussian only.
Relative error against a refined Gauss–Legendre reference carrying the same `t`-mixture,
`n = 100`, `alpha = 0.5`:

| t | 0.0 | 0.2 | 0.4 | 0.6 |
|---|---|---|---|---|
| nonlocal | 1.617e-12 | 0.3393 | 0.1463 | 0.7639 |
| local control | 1.62e-12 | 1.59e-12 | 1.51e-12 | 5.76e-13 |

`Y` and `Zbar21` compute tail terms as differences of rule-evaluated quantities, so an
O(1) rule error enters those differences directly. (`tail_sq < 0` — the failure mode
predicted in advance — did **not** occur on the tracked branch; recorded as a refuted
prediction.)

### 5.4 The gate quantity: `Z1` crosses 1 at finite `t`

`Z1 < 1` is necessary: above it the radii polynomial has no positive root at all.
Bisected crossing `t*`, bracket width 6.104e-06:

| | alpha = 0.25 | alpha = 0.5 | alpha = 0.75 |
|---|---|---|---|
| n = 100, `Z1(0) = 0.359321` | 0.300003 | 0.400003 | 0.455862 |
| n = 200, `Z1(0) = 0.246098` | not crossed (branch lost first; `Z1 <= 0.960984`) | 0.470499 | 0.515598 |

The machinery tolerates ~30–52% of one nonlocal operator. The crossing moves outward with
`n` (0.4000 -> 0.4705 at `alpha = 0.5`), which taken alone would leave the endpoint open;
5.1 and 5.2 are `n`-independent and worsen with `n`, so the two ladders agree.

### 5.5 Which bound fails

`n = 200`, `alpha = 0.5`, along the tracked branch (`t = 0 -> 0.5 -> 0.6`):

| bound | grade | trajectory |
|---|---|---|
| `Zbar11` | derivation-free | 1.922e-15 -> 5.515e-14 -> 1.628e-12 |
| `Zbar21` | derivation-free | 0.06706 -> 0.10980 -> 0.31568 |
| `Zbar12` | TRANSCRIBED | 0.10175 -> 0.72524 -> **62.349** |
| `Zbar22` | TRANSCRIBED | 0.21560 -> 1.16982 -> **30.585** |

The two that diverge are precisely the two graded TRANSCRIBED before the run.

### 5.6 What did not fail

`sum_m sup|Lam^{2a}psi_m|^2 / lam_m^2` converges: 1.362 / 1.235 / 1.871 for
`alpha = 0.25/0.5/0.75` against 0.857 for the local control; fitted sup growth exponents
0.003 / 0.265 / 0.522. The sup/embedding route is **not** the obstruction. A subsequent
attempt should not spend effort re-deriving `Zbar22`'s sup-norm ingredients.

## 6. Lesson-90 handling

`u == 0` solves the equation for every `t`, and its radii polynomial closes with
`Y ~ 1e-29`, `Z1 ~ 2.5e-3`, `closes = True`. Newton falls into it once the nontrivial
branch folds — which happens in all six (n, alpha) runs before `t = 1`. Every step carries
`collapsed_to_trivial_solution` and `verdict_is_meaningful`; no `closes = True` in this
data set is a certification. Fold located by bisection to width 2.441e-05.

## 7. Answer to the gate

**No.** Pointed at `Lam^{2a}` on its own weighted space, the machinery does not produce
finite closing bounds of the same kind it produces for local operators. It produces
*apparently* finite bounds whose finiteness is a quadrature-horizon artefact of a
divergent integral (5.2), computed by a rule that has lost exactness by O(1) (5.3), and
its contraction constant leaves the admissible region at 30–52% nonlocality (5.4), with
the two failing bounds being exactly the two whose derivations used locality (5.5).

The obstruction is now measured rather than inferred, and it is **not** the one Remark 40
names. What breaks is the interaction between an algebraic tail and a Gaussian weight —
the `e^{|x|^2/4}` weight, not nonlocality as an abstract property. Routing that
distinction to the DM: it reframes the (iv_a) re-screen question as "which weight
tolerates an algebraic tail", and a Gaussian one demonstrably does not.

## 8. Reproduction

    .venv/bin/python experiments/p2_route_nlh_v1.py            # measure + fig85
    .venv/bin/python experiments/p2_route_nlh_v1.py --figure   # fig85 from banked JSON

Data: `writeup/data/p2_route_nlh_v1.json`.
Figure: `writeup/figures/fig85_route_nlh_v1_nonlocal.png`.
Reads `solver/bc_weighted_sobolev.py` and `solver/line_hilbert.py`; edits neither.
