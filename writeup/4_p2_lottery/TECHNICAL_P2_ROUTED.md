# Phase-2 P2 — Route D v1: a rigorous interval-arithmetic core and the a=0 Newton–Kantorovich framing

**Status: Level-1 *tooling* + a Level-2 *scoping/framing* result — NOT a
certificate.** This is the project's first brick on the **rigor ladder** (the
Level-1 → Level-2 jump): the step from a numerically-found approximate profile
toward a *computer-assisted certification* of an actual solution. It delivers (a)
a hand-rolled, dependency-free **rigorous interval-arithmetic core**, and (b) the
**deterministic a=0 measurements + operator framing** that decide *how* a
Newton–Kantorovich (NK) certification of the gCLM two-scale traveling wave must be
set up. It makes **no certificate claim**, and does not move overall Clay odds
(still ~0.05%). Its value is turning the banked Tier-1 "guess" (the GA two-scale
profile of [TECHNICAL_P2_KLADDER.md](TECHNICAL_P2_KLADDER.md)) into a *certifiable
question*, and answering — with evidence — whether that question can be framed.

Rebuild the figure from committed data (no re-derivation):
`python writeup/4_p2_lottery/p2_route_d_evidence.py` →
`writeup/figures/fig19_p2_route_d.png` (reads
`writeup/data/p2_route_d_probe.json`; regenerate the data — deterministic, ~10 s —
with `python experiments/p2_route_d_probe.py`).

Code: `solver/interval.py` (the interval core) + `test_interval.py` (5/5, gated
with `fractions` as an exact oracle); the probe `experiments/p2_route_d_probe.py`
reuses the banked residual `solver/gclm_family.py::GCLMResidual.residual_two_scale`
and Hilbert operator `solver/line_hilbert.py`. Full test suite (8 files) green.

> **Update (Route-D v2, 2026-07-28).** The dress rehearsal proposed in §8 has been
> run: see [TECHNICAL_P2_ROUTED_DRESS.md](TECHNICAL_P2_ROUTED_DRESS.md) / fig20.
> **The ball does not close, at any truncation, gauge or weight.** Three claims
> below are superseded and should be read with that in mind: (i) §6's "`Z₀ + Z₁ < 1`
> is *plausible*" — it is not; `Z₁ ≥ N+1` from the truncation coupling alone;
> (ii) §7's ordering of the open risks — **G** (gauge) is exonerated by a
> three-gauge ladder, and **R** (the `θ = ±π` far field) is the blocker, confirmed
> by ablation; (iii) §5's "on the *decaying* subspace" caveat on `H(cos kθ) =
> sin kθ` — the identity is in fact unconditional (a Hardy-space argument, v2 §1).
> A `k = 0` coefficient error in this leg's closed-form band was also found and
> fixed (v2 §1). Everything else here stands.

---

## 0. Why this brick, and what "Level-2" means here

Everything banked before this leg is **Level-1**: a *novel numerical map* (the GA
finds an approximate self-similar profile and measures a residual floor). A GA
proves nothing — its output is a guess. **Level-2** is the first genuinely "new
maths" rung: a *rigorous, computer-assisted statement* — an interval /
Newton–Kantorovich argument that a **true** solution exists in an explicit
neighbourhood of the guess, with every inequality machine-checked. This is a real
genre (Chen–Hou, Gómez-Serrano, van den Berg–Lessard) and, honestly, an
*incremental* one: even full success is a toy-model certification, **not** a Clay
solve.

The honest first question is not "certify it" but **"can a certifiable fixed-point
statement even be set up?"** — can we bound the linearized-operator inverse, the
defect, and the Lipschitz constant well enough for an NK ball to close, *gated
against the a=0 exact anchor* where the answer is known? This leg answers the
prerequisites to that question and frames the attempt. It deliberately stops short
of the attempt itself (the next brick, §7).

## 1. The object and the anchor

The two-scale (traveling-wave) rescaled residual of the gCLM `a`-family
(HQW25 = arXiv:2401.14615), at `a=0` first:

    F(Ω, c) := Ω H(Ω) − c Ω_X = 0,        (TW)

with `H` the line Hilbert transform, `Ω` even and decaying, and `c` the
traveling-wave speed. The **exact anchor** is `Ω₂ = −1/(1+X²)`, `c = 1/2`
(HQW25's `a=b=c=1` normalization; `H(Ω₂) = −X/(1+X²)`), at which the discretized
residual is `~10⁻⁹`. The general `a≠0` case adds `−a U Ω_X`, `U = ∫₀ˣ H(Ω)`; we
frame `a=0` first and treat `a>0` as a perturbation (§7).

## 2. The interval-arithmetic core (`solver/interval.py`)

A Level-2 statement is only as trustworthy as its arithmetic, so we do **not**
use floating point for the bounds. `solver/interval.py` is a self-contained,
numpy-backed `Interval` type (scalar or whole-vector), no scipy / no mpmath, with
guaranteed **outward-rounded** `+ − × ÷`, reciprocal (zero-guarded), and the three
rigorous reductions the residual needs: `isum`, `dot`, and `matvec` (point-matrix
× interval-vector, for the Hilbert and derivative operators).

**Rigor model.** We do not portably own the FPU rounding mode from numpy, so we
use the standard *round-outward-by-one-ulp* discipline: evaluate the real
interval-extension formula in IEEE-754 double (each elementary op correctly
rounded to ≤ 0.5 ulp), then push the lower endpoint down and the upper endpoint up
one ulp with `np.nextafter`. One ulp conservatively covers the ≤ 0.5 ulp
elementary rounding, so every result is a **guaranteed enclosure**. For the
reductions, the classic running-error bound `|fl(Σ) − Σ| ≤ γ_m Σ|tᵢ|`,
`γ_m = m·u/(1−m·u)`, `u = 2⁻⁵³`, is added before the outward push — giving a
rigorous, fully-vectorized enclosure of an `m`-term accumulation (here `m ~ 1200`)
with no Python-level sequential loop.

**Validation (`test_interval.py`, 5/5).** Each op is gated against `fractions`
(exact rational arithmetic) as the oracle: `+ − × ÷` of point intervals enclose
the exact rational result; `1/3` straddles the true value at ulp-scale width; a
fresh point interval is width 0 while every arithmetic result is a ≥ 1-ulp box
that still encloses the exact value; inclusion-monotonicity holds; the reciprocal
zero-guard fires; and `isum`/`dot`/`matvec` enclose the exact answer, with the
box-`matvec` covering 64 random samples from the input box.

## 3. Q1 — arithmetic precision at the anchor (fig19-A)

Enclosing `F(Ω₂)` rigorously at the exact anchor gives (n = 2001 grid):

| quantity | value |
|---|---|
| point defect ‖F‖∞ (float) | 8.9 × 10⁻¹⁰ |
| interval enclosure width | 8.5 × 10⁻¹¹ |
| **arithmetic overhead** (width / defect) | **≈ 0.10** |

The enclosure width is ~10% of the defect it encloses — the interval core is
comfortably precise enough to carry a Newton–Kantorovich **defect bound `Y₀`**;
the enclosure `sup|F| ≤ 9.8 × 10⁻¹⁰` is dominated by the true defect, not by
rounding. Over a genome box of radius `r` around the anchor parameters `(A,B) =
(−1,1)`, `sup|F|` grows linearly (`r = 10⁻⁶ → 1.9×10⁻⁴`, slope 1) — i.e.
dominated by genuine residual sensitivity, an honest Lipschitz slope of `~190`,
not by wrapping. **The defect term is enclosable.**

## 4. Q2 — the degeneracy, counted (fig19-B)

The a=0 zero set is **not an isolated point**: every single Lorentzian
`A/(1+BX²)` is an exact traveling wave (speed `−A/2√B`), so the solutions form a
**2-parameter scaling valley** generated by two continuous symmetries —
**amplitude** `(Ω,c) ↦ (λΩ, λc)` and **dilation** `(Ω,c) ↦ (Ω(·/μ), μc)`. A naive
interval-Newton bound on `‖DF⁻¹‖` is therefore *infinite*; the gauge quotient is
**not optional**. Singular values of the finite genome-map Jacobian *count* the
kernel:

| linearization | singular values | kernel dim |
|---|---|---|
| gauge-slaved `c` | [2.0e-7, 1.3e-7], ratio ≈ 1 | **2** |
| fixed `c = 1/2` | [5.90, 9.3e-7], ratio 6×10⁶ | **1** |

Both directions vanish when `c` is slaved (the full 2-D valley); fixing the speed
removes exactly one. So **two scalar gauge conditions** (speed `c` + one
normalization) isolate a nondegenerate zero. Concretely: fix `c = 1/2` and impose
`Ω(0) = −1`; the residual symmetry that preserves `c` is the fiber `λμ = 1`, i.e.
`Ω ↦ (1/μ)Ω(·/μ)`, which sends `Ω(0) ↦ (1/μ)Ω(0)`, so `Ω(0) = −1` forces `μ = 1`
→ isolated. (The precise Fredholm-index bookkeeping — whether `c` floats with the
1-D cokernel bordered, or is fixed — is open sub-task **G**, §7.)

## 5. Q3 — the diagonalization that makes it tractable (fig19-C)

Compactify the line to the circle by `θ = 2 arctan X`, `X = tan(θ/2)`. Then the
**line** Hilbert transform equals the **circular** conjugate-function operator —
diagonal in the Fourier basis, `cos kθ ↦ sin kθ` — verified numerically to ~10⁻⁷
(discretization-limited) for `k = 1…6` on the *decaying* subspace (endpoint-
vanishing at `θ = ±π ⇔ X = ±∞`):

    modes [1,3]: 8.3e-8   [2,4]: 1.4e-7   [1,5]: 2.7e-7   [0,2]: 8.3e-8   [2,6]: 3.3e-7
    anchor (k=1): 2.1e-8

In this basis the anchor is a **2-term Fourier object**:
`Ω₂ = −(1+cosθ)/2` (so `a₀ = a₁ = −1/2`, all higher zero) and
`H(Ω₂) = −(1/2) sinθ`. This is the structural gift the whole framing rests on.

## 6. Q4 — the linearized operator is banded + rank-1 (fig19-D)

`F` maps an **even** profile to an **odd** residual (`Ω` even ⇒ `Ω H(Ω)` and `Ω_X`
odd), so `DF` is a map from **cosine** coefficients `{aₖ}` to **sine**
coefficients `{bₘ}`. With `Ω₂` degree-1, each term of

    DF[h] = h·H(Ω₂) + Ω₂·H(h) − c h_X,     h_X = (1+cosθ) h_θ

couples `cos kθ` only to `sin (k−1)θ, sin kθ, sin (k+1)θ`. Built in closed form,
`DF` is **tridiagonal (bandwidth 1)** plus a **rank-1 column**
`∂/∂c = −Ω₂,ₓ = −(1/2)sinθ − (1/4)sin2θ`. A banded operator whose tail is
dominated by the `c·(ik)` diagonal has an explicit `O(1/(cN))` tail-inverse
bound — this is the concrete reason the finite-section NK bounds `Z₀ + Z₁ < 1`
are *plausible*, not merely hoped. The closed-form band matches the dense grid
operator to `3.9×10⁻²`; the residual is the known `θ = ±π` (Cayley) endpoint
correction — flagged sub-task **R** (§7), not swept under.

## 7. The a-posteriori Newton–Kantorovich framing and its open risks

We instantiate the standard **radii-polynomial** theorem (van den Berg–Lessard).
For an approximate zero `x̄ = (Ω̄, c̄)`, an approximate derivative `A† ≈ DF(x̄)`, and
an injective approximate inverse `A ≈ DF(x̄)⁻¹`, with the Newton-like operator
`T(x) = x − A F(x)`, require bounds

    Y₀ ≥ ‖A F(x̄)‖,   Z₀ ≥ ‖I − A A†‖,   Z₁ ≥ ‖A(A† − DF(x̄))‖,   Z₂ ≥ ‖A · D²F‖.

Then `p(r) = Z₂ r² − (1 − Z₀ − Z₁) r + Y₀`; **if `Z₀ + Z₁ < 1` and
`(1 − Z₀ − Z₁)² ≥ 4 Y₀ Z₂`**, `T` is a contraction on `B(x̄, r₀)` and `F` has a
**unique zero there** — the certificate. Two simplifications are real: `F` is
**quadratic**, so `D²F` is constant and `Z₂` is `r`-independent (no third-order
term); and the anchor being a finite trig polynomial means its convolution tail is
**zero** beyond mode 1. The space is a weighted `ℓ¹_ν` of cosine coefficients (a
Banach algebra under convolution) `⊕ ℝ` for `c`.

**Honest open risks (what could keep it from closing).**
- **G — gauge / Fredholm index.** The exact well-posed square system (fixed-`c`
  + one normalization, vs `c` floating with the 1-D cokernel bordered). *The
  crux*; get it wrong and `Z₀` is meaningless.
- **R — endpoint rank-1 correction.** The diagonalization holds on the *decaying*
  subspace; the `θ = ±π` Cayley correction (the 3.9×10⁻² of §6) must be carried
  explicitly or shown negligible.
- **T — truncation tail.** Make the `O(1/(cN))` tridiagonal tail-inverse bound
  rigorous (the "eventually diagonally dominant" argument), enclosed.
- **a ≠ 0.** `−a U Ω_X` becomes a bounded but non-banded operator under the map,
  and — decisively — **off `a=0` there is no exact anchor** (residual floor
  `~10⁻²`), so `Y₀` jumps from `~10⁻⁹` to `~10⁻²` and the ball very likely will
  **not** close. The probable honest outcome is *"certifies at `a=0`, not yet at
  the `a≈0.5` boundary."*

## 8. The next brick, and the honest ceiling

**Next: a float dress rehearsal** — build `DF` as a finite `(N+1)`-mode matrix in
plain floating point, invert the finite section, and compute `Y₀, Z₀, Z₁, Z₂` and
the radii polynomial across a small `N`-ladder with the §4 gauge. This answers the
*only* question that gates the interval build — *does `Z₀ + Z₁ < 1` and does the
ball close at the anchor?* — at near-zero cost, and either green-lights the
verified-interval enclosure or surfaces exactly which sub-task (G/R/T) blocks it.
A legitimate, publishable result either way (including the negative "why the naive
NK doesn't close here yet"). Only after it closes in float do we harden with the
interval core.

**Ceiling, said plainly.** This leg is validated tooling and a scoping/framing
result. It does **not** climb the rigor ladder by itself — it makes the Route-D
attempt *concrete and grounded*. Even the eventual success it aims at is a
computer-assisted *toy-model* certification, not a Clay solve. What is genuinely
new here is only that the certification question is now framed in a basis where its
central operator is banded — and that we can say so with evidence rather than hope.
