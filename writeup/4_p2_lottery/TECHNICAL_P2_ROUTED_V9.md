# Route-D v9 — the sharpness leg: a 32% better `|H(h)|` bound that buys nothing where it matters

**Status: Level-1 tooling + upper bounds. NOT a certificate, NOT rigorous, NOT a
Clay result.** Plain float64 throughout; nothing is interval-enclosed.

**Figure:** `fig27` (`writeup/figures/fig27_route_d_v9_sharpen.png`)
**Data:** `writeup/data/p2_route_d_v9_sharpen.json`
**Code:** `solver/hilbert_pointwise.py` (+ `test_nk_hilbert_pointwise.py`, 6/6),
`experiments/p2_route_d_v9_sharpen.py`,
`writeup/4_p2_lottery/p2_route_d_v9_evidence.py`

---

## 0. Why a sharpness leg

v8 left seven of ten constants bounded and `Z₂` complete, which changed the
question. The budget goes like `1/(‖A‖ C_Q)`; `‖A‖`'s bracket was ~70× wide;
bounding the last three constants can buy a constant factor each, while halving
`‖A‖`'s slack buys more than all three together. So: sharpen, don't cover.

The target picked itself. v7's closure reads `T ≤ F(T)` with the feedback carried
by `|H(h)|`, and at the reference point the Hilbert term supplies **81 of the 93
units** in the derivative bound — the closure is dominated by its own feedback,
and the feedback is v6's `|H(h)|` bound, built from crude majorants
(`|cot| ≤ 2/|u|`, a 4/3 here, a 16/15 there, the singular half charged wholesale
to the seminorm).

**The leg did sharpen it, by 32% at the reference point. The budget did not
move.** Sections 4–5 are why, and that is the result.

---

## 1. The bound

For even `h`, folding the conjugate-function integral onto `(0, π)` gives

```
psi(θ) = (1/2π) p.v. ∫_0^π h(φ) K_θ(φ) dφ ,
K_θ(φ) = 2 sin θ / (cos φ − cos θ) = −sin θ / ( sin((φ+θ)/2) sin((φ−θ)/2) )
```

Three properties, each of which removes something v6 needed:

* **The decay is in the kernel.** `sin θ → 0` as `θ → π`. This is v6's
  even-kernel point in θ coordinates: `H` of an even function is odd, and a form
  that cannot see that cannot see the far-field decay either.
* **`p.v.∫_0^π K_θ dφ = 0` exactly** — it is the conjugate of the constant
  function; the antiderivative `−2 log|sin((φ−θ)/2)/sin((φ+θ)/2)|` vanishes at
  *both* endpoints. So the principal value is handled by a **global**
  subtraction `h(φ) − h(θ)`: no band, no matching scale, no remainder term. v6
  needed all three and each cost a constant.
* **The second form is the one to evaluate.** Near `θ = π` both cosines approach
  `−1` and their difference loses every significant digit; parameterising by the
  offset `s = |φ − θ|` makes `sin((φ−θ)/2) = sin(±s/2)` exact. The first draft
  produced NaNs at `X ≳ 1e4` before this.

Result (Y1), against v6 across eight decades of `X`:

| X | 1e-3 | 1e-2 | 0.1 | 1 | 3 | 10 | 1e2 | 1e3 | 1e5 |
|---|---|---|---|---|---|---|---|---|---|
| new/v6 | 0.09 | 0.26 | 0.66 | 0.87 | 0.65 | 0.67 | 0.85 | 0.95 | 0.99 |

Gated by an exact second build (the same kernel, true integrand, against
`cos kθ → sin kθ`): **1.5e-7**. And the bound is nearly attained: on the anchor
profile the measured `|ψ|` reaches **0.97** of it.

---

## 2. The payer rule — the part worth keeping

At each `φ` the increment can be charged to the seminorm or to the decay
envelope, and **any fixed rule gives a valid linear bound**. v8 chose by
comparing the two at `S = T = 1`. That is the wrong default, and generally:

> the rule should be tuned to the ratio `T/S` of the answer, not to 1.

Introducing `ρ` (seminorm route iff `ρ c_T ≤ c_S`):

| ρ | 1 | 2 | 3 | 4.5 | 6 | 9 | 12 | 25 | 50 |
|---|---|---|---|---|---|---|---|---|---|
| `‖A‖` | 74.7 | 63.4 | 53.1 | 48.4 | 47.2 | **47.2** | 47.7 | 50.6 | 54.0 |
| `C_Q` | 3.36 | **3.16** | 3.45 | 4.07 | 4.63 | 5.48 | 6.11 | 7.82 | 9.44 |

Two things fall out. There is an **interior optimum**, and the neutral rule
`ρ = 1` gives **74.7 — worse than the 69.4 of the crude bound it replaces.** In
the closure `T ~ 10 S`, so charging work to `T` to minimise the `S = T = 1` sum
is charging the expensive account. And the two consumers want **different** `ρ`:
`C_Q` maximises over the unit simplex where the ratio is `O(1)`, so it prefers
`ρ ≈ 2`. Both are valid bounds; each caller picks.

---

## 3. Y3 — the new `‖A‖`

At `(α, γ) = (1.5, 0.5)`, `ρ = 6`:

| J | 125 | 250 | 500 | 800 | 1600 |
|---|---|---|---|---|---|
| `‖A‖` v7/v8 | 69.15 | 69.09 | 69.05 | 69.38 | 70.33 |
| `‖A‖` **v9** | **47.05** | 47.01 | 46.99 | 47.21 | 47.85 |

Still flat in `J` (`J^+0.0059`, inherited entirely from `C_sup`). A 32%
reduction, and the largest single improvement to `‖A‖` since the closure was
built.

---

## 4. Y2b — the gain does not transfer

| (α, γ) | (1.5, 0.50) | (1.4, 0.35) | (1.4, 0.25) | (1.4, 0.15) | (1.2, 0.15) |
|---|---|---|---|---|---|
| reduction in `‖A‖` | **32%** | 11% | 3% | **−0%** | −1% |

**(1.4, 0.15) is the map's optimum** — where the budget is actually evaluated,
and has been for three legs. There the new bound is worth nothing at all.

The mechanism is the interpolation exponent. v7's closure is

```
T ≤ C(γ) (P/2)^γ (2S)^{1−γ}
```

and the `|H(h)|` bound enters **only through `P`**. At `γ = 0.5` a 30%
improvement in `P` moves `T` by ~15%; at `γ = 0.15` it moves it by **4%**. The
operating point sits at small γ precisely because that is where `‖A‖` is cheap —
and small γ is exactly where `‖A‖` stops caring about the estimate this leg
improved.

---

## 5. Y6 — the elasticity, and what it says to do next

Scaling each input of the closure by a factor and fitting the log-log slope:

| point | `d log‖A‖ / d log C_sup` | `d log‖A‖ / d log |H|` |
|---|---|---|
| reference (1.5, 0.50) | **+0.98** | +0.46 |
| operating (1.4, 0.15) | **+1.00** | **+0.11** |

`‖A‖` is **proportional** to `C_sup` — v6's two-point dual on the sup part — and
at the operating point barely sees the `|H|` bound at all. The last two legs
(v8's codomain seminorm, v9's pointwise bound) both worked on inputs with
elasticity ≤ 0.5, and both moved the budget by ≤ 7%. That is not a coincidence;
it is the elasticity table read backwards.

**What this does *not* license.** It is tempting to compute how much is available
by substituting a measured value for `C_sup`. An earlier draft of this leg did
exactly that and reported a **19× available gain** — which was an artifact: the
"measured `C_sup`" was a family lower bound computed by dividing the sup part of
an image by the *full* codomain norm of a sign pattern, whose Hölder seminorm is
enormous. It is an order of magnitude below any plausible sharp value. Banked
lesson (15), again, in a place we had already been warned about.

What is defensible: elasticity says `C_sup` is the input worth attacking; v6 B2's
own bracket says `C_sup` is roughly 2× lossy; so **~2× is on the table there**,
not an order of magnitude. And the wider bracket (47× against a family lower
bound of ~1.0) **cannot be attributed at all**, because a maximum over a handful
of sign patterns says almost nothing about how lossy an upper bound is.

---

## 6. Y4/Y5 — map and budget

The complete `Z₂` map (now choosing ρ per cell from {1, 3, 6, 12}) has its
optimum at **(1.4, 0.15), `Z₂ ≤ 260.7`** — third leg running at the same place,
essentially unchanged from v8's 261.1.

| leg | v5 | v6 | v7 | v8 | **v9** |
|---|---|---|---|---|---|
| `Y₀^max` | 7.6e-2 | 1.18e-2 | 2.58e-4 | 2.39e-4 | **2.40e-4** |

Three order-of-magnitude losses, then three legs of nothing. The losses stopped;
so did the gains.

---

## 7. Ledger after v9

Unchanged in coverage — seven of ten bounded, `Z₂` complete — with two status
notes rewritten:

* **`‖A‖` domain SUP part (`C_sup`)** — bounded (v6), and now identified as the
  **dominant** input: `‖A‖` is proportional to it, and it is the only remaining
  input with elasticity ≈ 1.
* **`C_Q` sup part / `‖A‖` seminorm part** — sharpened by this leg's `|H|` bound,
  materially at moderate γ and not at all at the operating point.

Open, unchanged: `Z₁` core↔far coupling; `Z₁` core discretization; the
discrete↔continuum transfer.

---

## 8. Reproduce

```
.venv/bin/python test_nk_hilbert_pointwise.py                     # 6/6, ~6 min
.venv/bin/python experiments/p2_route_d_v9_sharpen.py             # ~35 min -> JSON
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v9_evidence.py   # fig27 from JSON
```

Deterministic: no GA, no seeds, no predicate lock.

---

## 9. Honest ceiling

v9 improves one estimate by a third and moves the certification budget by 0.4%.
It does not climb the rigor ladder: float64 throughout, nothing interval-enclosed,
no certificate, three ledger items still open. The eventual success this line
scouts remains a computer-assisted **toy-model** certification (Chen–Hou /
Gómez-Serrano genre), not a Clay solve. Overall Clay odds ~0.05%. The honest best
case for the whole Route-D leg is still "certifies the a = 0 traveling wave",
which is already known in closed form.
