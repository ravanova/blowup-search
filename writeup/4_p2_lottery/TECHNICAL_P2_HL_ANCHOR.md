# Phase-2 P2 — a 1D Hou–Luo singular-profile machine, validated against an exact solution

**Status: VALIDATION of a proven result — machinery, not novelty, not a proof.**
Evidence figure `figures/fig12_p2_hl_anchor.png` rebuilds from committed
`data/p2_hl_anchor.json` via `python writeup/4_p2_lottery/p2_hl_anchor_evidence.py`
(`--generate` re-runs the machinery). Code: `solver/hl_rescaled.py`,
tests `test_hl_rescaled.py` (5/5). Working notes: `../PHASE2_P2_NOTES.md`.

## 1. Where this sits

Phase 1 concluded that a uniform grid cannot resolve self-similar blow-up
(`NEGATIVE_RESULT_TWO_CURRENCIES.md`). Phase 2 built the stretched-grid
dynamic-rescaling machinery and validated it in 1D (Spike 0, CLM) and 2D
(Spike 1, Boussinesq). Spike 1 reproduced the **proven** Chen–Hou *regular*
self-similar profile — validating the machine but not producing anything novel.

P2 aims at the actual frontier: **singular** self-similar profiles from
**degenerate** initial data, reported numerically by **Chen–Huang–Li
(arXiv:2604.01868, 2026)**. Their finding is a *not-rigorously-proven*
two-stage L^∞→L^p blow-up whose Stage-2 profile is locally unbounded. Crucially,
only *weak existence* of an explicit profile is proven (their Theorem 2.3); the
*asymptotic stability* — that generic degenerate data actually converges to it —
is numerical only. This writeup covers the first step: standing up and
**validating** the 1D machinery against their explicit exact solution, so the
stability question can be attacked next on trustworthy footing.

We chose the **1D Hou–Luo (HL)** model over 2D Boussinesq deliberately (§2).

## 2. The model, the scaling, and the decision to work in 1D

HL model (their (1.1)), with `H` the whole-line Hilbert transform:
```
ω_t + u ω_x = θ_x,   θ_t + u θ_x = 0,   u_x = H(ω).
```
Dynamic-rescaling form (their (2.4)), fields `Ω, Θ` and rescaled velocity `U`:
```
Ω_τ + (U + c_l X) Ω_X = c_ω Ω + Θ_X
Θ_τ + (U + c_l X) Θ_X = (c_l + 2 c_ω) Θ
U_X = H(Ω),   U(0) = 0.
```
Steady states of the frozen system are exact self-similar blow-ups of (1.1) with
`γ = −c_l/c_ω`, `λ = −1`. Two pieces are genuinely new relative to our CLM solver:
the velocity `U` is the **integral** of `H(Ω)` pinned at `U(0)=0` (CLM's transport
speed was purely algebraic `c_l X`), and there is a second **buoyancy** field `Θ`.

**Why 1D, not 2D.** The novel phenomenon appears first in the 1D HL model, which
Chen–Huang–Li describe as modelling the boundary behaviour of the Hou–Luo /
3D-axisymmetric-Euler scenario. 1D reuses machinery we already have and trust
(`solver/line_hilbert.py`, 6/6; CLM/gCLM rescaling, 5/5), and it sidesteps the
far-field-tail difficulty that our 2D machine already hit in Spike-1 Step C. A
feasibility probe (§4, panel C) confirmed the 1D operator survives a genuinely
singular profile.

## 3. An exact anchor, and a closed-form velocity we derived

Their **Theorem 2.3** gives an explicit one-sided singular steady state:
```
Ω̄(X) = (X−1)^{−1/2} · 1_{X>1},   Θ̄(X) = (π/2) · 1_{X>1},   c̄_l = 2,   c̄_ω = −1.
```
`Ω̄` blows up like `(X−1)^{−1/2}` at `X=1` and decays like `X^{−1/2}`, and its
support is `X>1` (so it is *zero near the origin* — the origin-slope normalization
used for the regular case does not even apply here).

To validate the machinery we need the exact velocity. Using the classical Hilbert
pair `H(x₊^{−1/2}) = −(−x)₊^{−1/2}` (immediate from the Fourier multiplier
`−i·sgn(ξ)`), shifting by 1:
```
H(Ω̄)(X) = −(1−X)^{−1/2} · 1_{X<1},   0 for X>1,
U̅(X)   =  2√(1−X) − 2   for X<1,      −2   for X≥1.
```
This is internally consistent three ways: (i) `U̅(0)=0` (the gauge pin);
(ii) `U̅(1⁻) = −2`, matching the strong steady form `(U̅+2X)Ω̄_X + Ω̄ = 0` on the
support (Remark 5.4: strong solution away from the singular point); and
(iii) `c̄_l + 2 c̄_ω = 0` **exactly**, which makes the `Θ` steady equation trivially
satisfied. This closed-form `U̅` is a small self-contained by-product — an explicit
velocity for their Theorem-2.3 profile — and it is what turns "does the machinery
work?" into a known-answer test.

## 4. Validation results (fig12)

`solver/hl_rescaled.py` implements the velocity operator (`U` from `U_X=H(Ω)`,
pinned at `U(0)=0` by cumulative integration and interpolated subtraction), the
rescaled RHS, and the steady residual. Tests (`test_hl_rescaled.py`, 5/5):

**Panel A — the machine holds the exact singular steady state.** On a grid
clustered at `X=1` (`X = 1 + δ·sinh(s)`, which resolves the `(X−1)^{−1/2}` core),
the recovered `U` sits on top of the exact `U̅` straight through the singularity.

**Panel B — convergence under refinement.** The velocity error and the steady-state
residual on the support both fall as the near-singularity spacing `δ` shrinks, at
the `~½`-order set by the integrable `(1−X)^{−1/2}` singularity of `H` (the
reference slope is `δ^{1/2}`). Representative unit-test numbers: velocity operator
vs analytic `arctan(2X)` = 1.1e−5; full pipeline through the dense Hilbert operator
= 1.8e−3; steady residual at `δ=0.004` = 6.2e−3; `Θ`-consistency = exactly 0.

**Panel C — the operator survives the singularity; the tail is the only cost.**
Feeding the singular `Ω̄` to the dense line-Hilbert operator and comparing to the
exact `H(Ω̄)` in `|X−1|` bands: the near-singularity core is representable to a few
percent and improving, while the residual lives in the slow `X^{−1/2}` **tail** and
is **truncation-limited** — it falls with domain reach `M` and is immune to node
clustering. This is the known semi-analytic-outer-patch gap, not a failure to
resolve the core.

## 5. Performance note (shared operator)

The build cost lived in the shared `solver/line_hilbert.py`, not the P2 code. Three
fixes, all accuracy-preserving (verified: `line_hilbert` 6/6, `gclm` 5/5, `hl` 5/5,
identical error digits): a batched Thomas solve for the spline-slope operator
(`_slope_matrix` 6.15s → 0.29s, 21×); Horner + shared + shortened `L(s)` series, the
dominant transcendental cost (n=4001 matrix build 65s → 19.7s, 3.3×); and a lazy
Hilbert matrix so validation runs that use the exact `H` never pay to build it. The
HL suite went from >120s to 3.9s.

## 6. Honest status and what is next

This reproduces a **proven** result (weak existence of the Theorem-2.3 profile). It
validates the singular-profile machinery end to end and contributes an explicit
closed-form velocity for that profile — but it is **not novel and not a proof**,
the same tier as Spike 1. The genuine novelty attempt is the next leg: a dynamic
relaxation with a degenerate-case normalization, to test whether generic smooth
degenerate data *converges* to the singular profile (the asymptotic stability
Chen–Huang–Li asserted numerically). That is a logged run with a pre-locked
predicate; the slow tail will need a fixed-τ protocol plus a semi-analytic `r^α`
outer patch. See `../PHASE2_P2_NOTES.md` §4.
