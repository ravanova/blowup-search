# Route-D v10 — a lower bound on `‖A‖` worth reading, and the first measured ceiling on sharpening

**Status: Level-1 tooling + bounds. NOT a certificate, NOT rigorous, NOT a Clay
result.** Plain float64 throughout.

**Figure:** `fig28` · **Data:** `writeup/data/p2_route_d_v10_lower.json`
**Code:** `solver/op_lower.py` (+ `test_op_lower.py`, 6/6),
`experiments/p2_route_d_v10_lower.py`,
`writeup/4_p2_lottery/p2_route_d_v10_evidence.py`

---

## 0. Why

v9 ended with the sharpest statement this project has made about its own state:
every bracket it quotes has a **lower end that is a maximum over sign patterns**,
which is nearly meaningless, so *"the bound is 50× too big"* and *"the operator
really is that large"* cannot be told apart — and they imply opposite decisions
about the whole lane. v9 also paid for the confusion, turning the
uninterpretable bracket into a "19× available gain" that was pure artifact.

This leg builds the adversary — banked lesson (9), applied to the operator rather
than to the quadratic — and then reads the answer.

---

## 1. Why sign patterns fail here, and what replaces them

For a domain index `i`, the vector `g = sign(A_i·)/v` is the exact extremizer of
the *sup-to-sup* problem. In this space it is a terrible direction, for precisely
the reason v6's discrete-ball trap made famous in the other direction: a sign
pattern's **Hölder seminorm is enormous**, so dividing by the full codomain norm
throws away everything the numerator gained. At `J = 400` these report **0.94**
against an upper bound of 47, and — the tell nobody had looked at — they get
**worse as `J` grows** (0.97 → 0.92 over `J = 200..800`). They were never
converging to anything about the operator.

The `Y`-ball says what to look for instead: an element with finite codomain norm
must decay at least like `1/v = cos^{α+1}(θ/2)` and must not oscillate. So the
family is `1/v` times a **slowly varying** shape — powers, low-order cosines,
Gaussian bumps over a wide sweep of centre and width, smoothed steps, and boxes.
Any `g` gives a valid lower bound `‖A‖ ≥ ‖A g‖_X / ‖g‖_Y`, so validity is free
and the whole problem is construction.

A random ascent in a smooth cosine basis is run from the family's best, and
**adds essentially nothing** (gain 1.000×). That is reported rather than dropped:
a flat maximum is information about the problem's shape.

---

## 2. W1/W2 — the numbers

At the reference `(α, γ) = (1.5, 0.5)`:

| J | 200 | 400 | 800 | 1600 |
|---|---|---|---|---|
| sign patterns | 0.973 | 0.942 | 0.921 | — |
| **adversary family** | 2.68 | **2.88** | 3.07 | — |
| bracket | 50× → **16×** | | | |

At the **operating point** `(1.4, 0.15)` — where the budget is actually
evaluated, and has been for three legs:

```
2.74  ≤  ‖A‖  ≤  20.94          a factor of 7.7
```

**The bracket that matters was never 50×. It is 7.7×.** Quoting a bracket at the
reference point was itself part of the confusion.

---

## 3. W3 — what the extremizer is

A **wide, far-field-supported, slowly varying** shape: the winner at `J = 400` is
a bump centred at `θ = 3.12` (i.e. `X ≈ 93`) with width 0.5, and the next four are
its neighbours in centre and width. Nothing oscillatory comes close.

That is the same place every other Route-D finding has pointed at: v2's far-field
degeneracy of the transport term, v3's resonance at `α = 2`, v6's matching radius
`X₀`. The operator's worst direction is a broad far-field disturbance, not a
local one — which is consistent with the physics of the problem and is a small
independent check that the number means something.

---

## 4. W4 — across the map

| (α, γ) | (1.2,0.15) | (1.4,0.15) | (1.4,0.35) | (1.5,0.50) | (1.6,0.25) | (1.8,0.15) |
|---|---|---|---|---|---|---|
| bracket | 10.7× | **8.2×** | 14.2× | 16.2× | 10.8× | 10.4× |

8–16× everywhere, and **tightest at the optimum**. The upper bound is worst
exactly where the closure leans hardest on the interpolation inequality (large γ).

---

## 5. W5 — the verdict, which is the point of the leg

A **perfect** upper bound on `‖A‖` — one reaching the adversary exactly — would
multiply the conditional budget by the bracket and no more:

```
budget now                    2.45e-4
if ‖A‖ were exactly sharp     1.88e-3          (x 7.7)
GA residual floor             1e-2
```

This is **the first measured ceiling on what sharpening can buy** in ten legs.
Read it in both directions and both matter:

* **Better than it looked.** After v7 the budget appeared to be ~40× below the
  residual floor with no idea how much was recoverable. The recoverable part of
  `‖A‖` is 7.7×, which lands **~5× short** of the floor rather than 40×.
* **Not enough on its own.** `‖A‖` alone cannot close the gap even if bounded
  perfectly. Closing it needs `C_Q`'s slack (~4×, v8 X2) as well — and those two
  together would only just reach the floor, with nothing left over for the three
  `Z₁` items still open.

Caveats that travel with the number: the true norm is *somewhere inside* the
bracket, not at its bottom, so 7.7× is itself an over-estimate of the achievable
gain; the lower bound is still a finite family; and the budget remains
CONDITIONAL (far-field `Z₁` only).

---

## 6. Ledger and next

Coverage unchanged — seven of ten bounded, `Z₂` complete. What changed is that
the bracket on the dominant constant is now **interpretable**, so the next leg
can be chosen on evidence: `C_sup` (elasticity ≈ 1 per v9, untouched since v6,
and now with a measured ceiling on the payoff), then the `Z₁` core↔far commutator,
the change of ansatz, and the core discretization.

---

## 7. Reproduce

```
.venv/bin/python test_op_lower.py                                  # 6/6, ~8 min
.venv/bin/python experiments/p2_route_d_v10_lower.py               # ~20 min
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v10_evidence.py   # fig28
```

## 8. Honest ceiling

Nothing here climbs the rigor ladder: float64, nothing interval-enclosed, no
certificate, three ledger items open. The eventual success this line scouts
remains a computer-assisted **toy-model** certification, not a Clay solve. Overall
Clay odds ~0.05%.
