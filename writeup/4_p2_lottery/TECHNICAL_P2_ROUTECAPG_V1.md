# TECHNICAL — Route-CAPG v1 (leg 162): the compact-support / global-Chebyshev corner

Module `solver/compact_cap_cheb.py`. Runner `experiments/p2_route_capg_v1_corner.py`.
Data [`p2_route_capg_v1_corner.json`](../data/p2_route_capg_v1_corner.json).
Tests `test_compact_cap_cheb.py` (22 checks). Figure `fig64_route_capg_v1.png`.
Journal [`experiments/journal/leg_162.md`](../../experiments/journal/leg_162.md).
Novelty [`writeup/novelty/leg_162.md`](../novelty/leg_162.md).

**Gate answer: (a) UNCOVERED, (b) UNDER 1. Escalation #4 — branch pushed, not merged.**

Everything here is **float64**. No interval arithmetic. Every number is a measurement of a
finite matrix at a stated truncation, with a ladder in that truncation.

---

## 1. The object

`solver/first_integral.py`'s reduced system, on the profile's own support, `v = X/X_c ∈
[−1,1]`, dilation gauge `c = 1`:

```
  c e'(v) + a X_c Hpv[ e^{1/a} ](v) = 0,     e(0) = 1,  e(1) = 0
  Hpv[w](v) = (1/pi) p.v. ∫_{-1}^{1} w(u)/(v − u) du        <-- (v − u), this repo's sign
```

linearised at the converged profile:

```
  L h = c h' + X_c Hpv[ p h ],      p(v) = e(v)^{1/a − 1}                       (L)
```

`c d/dv` is the unbounded part; `Hpv[p ·]` is bounded. **HTW Thm 7.10(3) gives compact
support exactly on `0 < a < 1`** (leg 112's full-text read); `a = 1` is the boundary case
where the edge degenerates to a corner, so `GRID_A` maxes at `0.8`.

## 2. Two realizations of one operator

| | domain `φ_n` | codomain | unbounded part | label |
|---|---|---|---|---|
| **A** (this repo's ansatz) | `(1−v²)T_n` | `T_m` | `((n−2)/2)T_{n−1} − ((n+2)/2)T_{n+1}` | `SHIFT`, diagonal **exactly 0**, off-diag `~n/2` |
| **B** (Olver–Townsend) | `√(1−v²)U_{n−1}` | `T_m/√(1−v²)` | `diag(−n)` | `MULTIPLIER`, off-diag **exactly 0** |

The two closed forms B rests on, both verified numerically (§4):

```
  d/dv[ √(1−v²) U_{n−1} ] = −n T_n / √(1−v²) = −n ψ_n
  Hpv[ √(1−v²) U_{n−1} ]  = T_n = √(1−v²) ψ_n
```

The second is the Tricomi identity — **the same one `test_first_integral.py` gate 2 already
banks**, so the sign convention is checked against a landed module and not only against this
module's docstring. Landing `T_n` in the `ψ` codomain costs one multiplication by `√(1−v²)`,
whose Chebyshev coefficients are `O(m^{−2})` and whose `ℓ¹` norm is `4/π = 1.27324`
(measured: `1.273084`). So B's bounded block is bounded.

**Realization A has no closed form for its Hilbert block, and that is a result, not an
implementation detail.** `(1−u²)T_n = √(1−u²)·[√(1−u²)T_n]` and the bracket is not a
polynomial, so the airfoil identity does not apply. This module's first draft asserted
`Hpv[(1−u²)T_n] = (T_{n+1}−T_{n−1})/2`; `verify_identities` measured its error at **0.617**.
Replaced by `hilb_projector`, a numerical projector gated against the family whose answer is
exactly `I` (`3.72e-08`).

## 3. The split, the approximate inverse, and `Z_1`

Leg 54's convention, unchanged: `Z_1 = colmax(I − A L)`, the weighted-`ℓ¹` operator norm
(max absolute column sum) in scaled coordinates `L_s = L · w_i/w_j`.

* **Split.** Finite block `1..K` (+ the border) against tail `K+1..N`. Same split as leg 54.
* **`A22` is built from the tail's OWN diagonal**, `diag(1/T_nn)` — never `inv(T)`. Leg 54's
  MM3 is the ban this respects: inverting the truncated tail makes `Z_1` a statement about
  `numpy.linalg.inv`. In realization A the diagonal is exactly zero, no diagonal `A22`
  exists, and the module falls back to the `A22 = I` convention and says so.
* **Shapes.** `block_diag` and `gs_upper` (both `A21 = 0`), `gs_lower` (`A21 ≠ 0`),
  `exact_inv` kept only as the inadmissible MM3 control.
* **The border.** (RS)'s unknowns are `(s, X_c)`: the support radius is solved for. The
  free-boundary column `∂R/∂X_c = −c e'/X_c` and a gauge row join the **finite block**
  (`nG = K+1`). Lesson 89 — the term that does not exist until you assemble is the one that
  decides.

## 4. Verification, in the order it was done

| check | magnitude |
|---|---|
| `d/dv[(1−v²)T_n]` vs central differences | `1.14e-08` |
| `d/dv[√(1−v²)U_{n−1}]` vs central differences | `2.32e-08` |
| `Hpv[√(1−v²)U_{n−1}] = T_n` vs PV quadrature | `2.55e-09` |
| `hilb_projector` vs the exactly-known `I` | `3.72e-08` |
| `√(1−v²)` series vs the function; its `ℓ¹` vs `4/π` | `7.21e-07`; `1.273084` vs `1.273240` |
| `cheb_mult_matrix_U` vs pointwise `f·U_{n−1}` | `2.22e-16` |
| **operator known-answer gate, realization B** | **`3.40e-04`** |
| operator known-answer gate, realization A | **`0.562`** — does not converge |

**Two errors this leg made and measured, both kept in the artifact (lesson 76).**

1. *The asserted closed form* (§2), error `0.617`.
2. *The gate measuring itself.* The known-answer gate compares **pointwise**, so the matrix
   side must reconstruct `Σ c_m ψ_m(v)` from `N` terms. The unbounded part multiplies input
   coefficients by `−n`, so a probe decaying like `n^{−2}` produces an output series decaying
   like `n^{−1}`, whose partial sums converge only like `1/N`. At that smoothness the gate
   read `1.1712e-02` **invariant across `nq` = 1000/2000/4000/8000, identical to six
   digits** — the invariance is what identified it. Smoothness ladder at `N = 64`:

   | probe decay | `n^{−2}` | `n^{−4}` | `n^{−6}` |
   |---|---|---|---|
   | max rel err | `1.171e-02` | `1.510e-03` | `3.401e-04` |

   Lesson 86 in its own habitat: a bound dominated by its own evaluation error is a statement
   about the code.

3. *A wrong basis, caught before it reached a number.* Realization B's domain is the `U`
   family, so multiplying the perturbation by `p` is a **`U`-basis** product. The first draft
   used the `T`-basis matrix — a wrong operator, not a small error. `test_5` asserts the two
   matrices differ.

**Realization A's `Z_1` is an order of magnitude, not a measurement.** At `56%`
representation error it is partly a statement about the code. Two causes, both structural:
its Hilbert block is dense with slowly decaying entries (§2), and its codomain drops `T_0`
while `d/dv[(1−v²)T_1] = −(1/2)T_0 − (3/2)T_2` has genuine mass there. Its **shape**
classification is unaffected — the derivative block is exact to `1e-8`, and the derivative
block is what carries the shape.

## 5. The control that can come out differently (lesson 90)

`classify_tail` is one code path run against three operators, and they are **required** to
disagree:

| operator | label | min abs diagonal | max abs off-diagonal |
|---|---|---|---|
| realization A derivative block, `N=64` | `SHIFT` | `0.0` exactly | `63.0` |
| **CONTROL** — `spectral_certificate.tail_block(8,128)`, the banked compactified whole line | `SHIFT` | `0.0` exactly | `126.0` |
| realization B derivative block, `N=64` | `MULTIPLIER` | `1.0` | `0.0` exactly |

Realization A's off-diagonal is not merely *like* the whole-line block's — it is the same
shape and the same `n/2`. Had the classifier returned `MULTIPLIER` on the whole-line control,
the Chebyshev result would be a property of this file rather than of the operators.

## 6. Why `Z_1 < 1` does not contradict leg 58's Proposition NG

Proposition NG: for every bounded `A` with `A21 = 0`, `Z_1 ≥ 1`. Every sub-1 row below has
`A21 = 0`. `spectral_certificate.nogo_hypotheses` names three hypotheses, and **(H2) is "the
tail block has a kernel in `ℓ¹_w`"** — the three-line proof sets `x = (0; h)` with `Th = 0`,
and `Th = 0` is what kills both the `A12` and the `A22` terms.

Realization B's tail is `diag(−n)`, `min |diagonal| = 1.0`: **no kernel at any `n ≥ 1`.**
(H2) fails outright — the same failure mode as `μ > 0` in leg 58's own dissipative control,
which is why that control reaches `Z_1 = 0.174`. The theorem is untouched; it does not reach
this realization. **That is the precise sense in which the corner is new.**

## 7. Results

Realization B, `A21 = 0`, bordered, `N = 192`, `K = 16`, amplitude gauge, deterministic grid
`GRID_A × GRID_S` (**no GA compute; no search of any kind**):

| | `block_diag` | `gs_upper` |
|---|---|---|
| grid minimum (`a=0.8`) | `0.27368` (`s=1.0`) / `0.15746` (`s=1.5`) | **`0.087351`** (`s=1.0`) |
| **inside `a ≤ 1/2`** (where `Z_2` is finite) | `0.73698` (`a=0.5,s=1.0`), `0.65436` (`a=0.4,s=1.5`) | `0.22870`, `0.30192` |
| worst corner (`a=0.2, s=0`) | `148.68` | `92.641` |

Realization A over the same grid: best `190.56` (see §4 on how to read it).

Over the whole grid, **27 of 120** `A21 = 0` configurations have `Z_1 < 1`, all of them in
realization B. Realization A has none. The bordered/unbordered pair at the minimum is
`0.273683` vs `0.086295`: the border **costs** a factor `3.17` here rather than being the
term that decides — the opposite of the whole-line case, where it was the far-field amplitude
column that ran the certificate out of margin.

**Truncation ladder** at the minimum (`K=16`): `Z_1` = `0.0872157` → `0.0873089` →
`0.0873509` → `0.0873825` for `N` = 48, 96, 192, 384 — **0.19% over an 8× refinement**.

**Target membership** (leg 126 clause SPACE-TARGET): at the minimum, coefficient decay
`−2.732`, weight growth `+1.0`, margin `decay + s + 1 = −0.73 < 0`, weighted `ℓ¹` partial
sums saturating at `5.34`. The target **is** in the space. A `Z_1` below 1 in a space the
target has left would not be a result.

**Border gauge dependence — the caveat that travels with the number.** Four directions,
`block_diag`, at the minimum:

| gauge | `amplitude` | `first_mode` | `edge_slope` | `mass` |
|---|---|---|---|---|
| `Z_1` | `0.273683` | `0.086125` | `93.336` | `6.712e9` |

`Z_1 < 1` at **2 of 4** gauges. For a negative result the conservative choice is the best
gauge (leg 54's convention); for a positive result it is the worst, and the worst is `6.712e9`
(a near-singular bordered block — a bad gauge, not evidence against the good ones). A
certificate designer picks one gauge, so this is a **restriction, not a refutation**; the
headline is stated with its realization and gauge named and never as a bare `Z_1`.

**Negative controls that can fail:** the same `assemble`/`measure` path returns `190.56`
(realization A) and `148.68` (realization B's worst corner). `Z_1 < 1` is a discrimination,
not an instrument floor.

## 8. The enumeration gap, named exactly

`writeup/data/p2_route_bx_v1_stageb.json` → `BX1_declared_axes.realization` =
`["l1_fourier", "collocation", "weighted_L2"]`, three values, `BX2_n_configurations = 1686`,
`BX2_n_uncovered = 0`.

**The gap is on the `realization` axis — stage `B`'s SPACE degree of freedom.** A global
Chebyshev basis on a compact support interval is a **fourth value** of that axis. It is not a
new split (finite block + tail, leg 54's) and not a new shape (`block_diag`, `gs_upper`,
`gs_lower`, leg 54's). Leg 126's clauses `REAL-COLLOC` (leg 56) and `REAL-ENERGY` (leg 111)
close the second and third values; nothing closes a fourth that was never listed.

`solver/certificate_shapes.py` **cannot** cover or fail to cover this corner: it enumerates
no basis and no domain. Its vocabulary (`MULTIPLIER`/`TRIDIAGONAL_DOMINANT`/`SHIFT`/
`NO_UNBOUNDED_PART` × `BLOCK_DIAGONAL`/`NOT_BLOCK_DIAGONAL`/`FINITE_JACOBIAN`/
`NO_APPROXIMATE_INVERSE`) classifies the *shape of the unbounded part*, which §5 shows is a
**consequence** of the pairing: one operator, two labels.

## 9. Does the corner even exist on leg 126's own object?

Measured, not assumed. Leg 126's audit is written on the `a = 0` CLM linearisation,
`Ω₀(X) = −4X/(1+4X²)`:

* measured decay exponent **`−1.0000`** — algebraic, never compact;
* mass outside radius `R` never reaches zero, over `R = 1 … 4096`;
* `a = 0` is **outside** HTW's `0 < a < 1`;
* `solver/first_integral.py` refuses to construct at `a = 0`: *"a must be positive; a = 0 is
  the degenerate limit (Omega = -exp(U/c), X_c = infinity) and **has no support**."*

**There is no finite interval to put a global basis on.** This is the honest complication,
and it is why the leg parks rather than concludes: "leg 126 declared a space complete that had
a fourth value on one of its axes" and "leg 126's audit was always scoped to an object on
which this corner is empty" are both defensible readings of the same measurements.

## 10. The ceiling

* **`Z_1` is one of four constants. THIS IS NOT A CERTIFICATE.** `Y_0`, `Z_0`, `Z_2` are not
  measured here. `solver/reduced_certificate.py` measured **`Z_2` infinite** on this same
  object in the sup realization, with finiteness of the nonlinearity requiring `a ≤ 1/2` —
  which is why the `a ≤ 0.5` rows in §7 are the load-bearing ones.
* Float64, no intervals, no rigour.
* The object is the **gCLM profile on `0 < a < 1`**, not `HL_S2_nonsymmetric`, and not any
  link of the L1→L4 chain.
* **No GA compute ran**, under either branch. Both free parameters moved on pre-named
  deterministic grids (leg 46/59 precedent). The GA ban is untouched.
* **Ban adjacency, stated:** *"another Route-D bound-sharpening leg (lifted by: `B`)"* is in
  force. This leg sharpens no existing Route-D bound; it computes one Route-D declared
  uncomputed. Separately, `Z_1 < 1` needs `s ≥ 0.7` and `s = 1` is a banned exponent **on the
  whole-line operator** (the Fredholm crossing). Realization B has no tail kernel, so that
  crossing does not exist here — but the proximity is flagged deliberately.
* **No link of the L1→L4 chain moved.** None has in 161 legs. Clay unchanged at ~0.05%.
