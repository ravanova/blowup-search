# Leg 56 novelty pass — Route-TN, the `(H, D)` consistency gap

**Run BEFORE any construction** (standing discipline). **Links, not counts** — leg 53's
counts-only log was withdrawn for exactly this failure, so every query below carries the
result URLs it was judged on.

**Verdict: `PROCEED_NARROW`. Nothing is banked as novel.** The move this leg makes —
bounding the consistency defect of a spline-based discrete Hilbert transform and of a spline
derivative operator, rigorously, inside a computer-assisted proof — is **established practice
in exactly this literature**, on exactly these models. What this leg produces is a
**measurement of this repository's own realization against this repository's own budget**,
which is an internal engineering fact and not a contribution to the literature. Claim nothing
else.

---

## Q1 — is "rigorous discretization-error bound inside an interval-arithmetic collocation certificate for self-similar blowup" a known move?

Query: `computer-assisted proof discretization error bound collocation Hilbert transform
interval arithmetic self-similar blowup`

- <https://arxiv.org/pdf/2106.05422> — Chen–Hou–Huang, *Asymptotically self-similar blowup of
  the Hou–Luo model for the 3D Euler equations*. **The directly-on-point hit.** The
  approximate profile is an explicit part plus a perturbation part represented by **piecewise
  quintic polynomials**, and the write-up states that grid values of the Hilbert transform are
  computed **with rigorous error bounds from integral formulas using piecewise polynomials**.
  Same model family, same operator, same purpose.
- <https://arxiv.org/pdf/1905.06387> — Chen–Hou–Huang, De Gregorio; same framework.
- <https://arxiv.org/pdf/2305.05660> — Chen–Hou, *2D Boussinesq / 3D Euler II: Rigorous
  Numerics*; approximate space-time solutions **with rigorous error control**.
- <https://arxiv.org/abs/2603.15073>, <https://aimath.org/pastworkshops/compproofsvrep.pdf> —
  survey level: "a-posteriori analysis exploiting interval arithmetic leads to mathematically
  rigorous bounds on all discretization and truncation errors."

**Read:** the *category* of this leg's quantity is standard. Not novel.

## Q2 — is the exactness structure (H is exact on the spline) known, or is it this leg's observation?

Query: `rigorous consistency error cubic spline Hilbert transform quadrature interval
arithmetic enclosure`

- <https://link.springer.com/article/10.1007/s10444-011-9252-x> — *On computing with the
  Hilbert spline transform.*
- <https://www.sciencedirect.com/science/article/abs/pii/S1007570419303028> — *The Hilbert
  transform of cubic splines.*
- <https://arxiv.org/pdf/2507.05083> — *Cubic spline functions revisited* (2025).

Plus, from Q6's sweep, the explicit statement that **when a function is given as a spline
which is `C^{k-1}` everywhere and `C^k` except at finitely many points, one can rigorously
calculate the Hilbert transform.**

**Read:** the structural fact this leg leans on — that a spline-represented Hilbert transform
is not a quadrature approximation but the **exact** transform of a piecewise polynomial — is
**known**. It is the design principle of the method, stated in the sources above and in
`solver/line_hilbert.py`'s own docstring (Appendix C.1 of Huang–Tong–Wang). This leg
**re-derives** it. It does not discover it.

> **CORRECTED after VER-C's review.** This entry originally added "…so the entire consistency
> defect is an **interpolation** error and not a quadrature error." **That is false for this
> implementation, and the error was mine, not the literature's.**
> `line_hilbert_matrix` assembles source columns for interior nodes only, so it transforms an
> **endpoint-zeroed** interpolant — a different object from the natural-spline interpolant
> `slope_matrix` differentiates. The measured defect is therefore ~99.99% an **endpoint
> artifact** and only 4.4181e−07 of it is genuine interpolation error. Details in
> `TECHNICAL_P2_ROUTETN_V1.md` §3 and §7.1.
>
> **This changes nothing about the novelty verdict** — that a spline Hilbert transform is
> exact on its spline remains known and unbanked, and the specific endpoint-column choice in
> this repository's own implementation is not a literature claim in either direction. The
> correction is recorded here because a novelty log that quietly carries a retracted
> structural claim is not auditable.

## Q3 — the specific realization: the source of this repo's spline-analytic H

Query: `Huang Tong Wang arXiv 2603.25104 spline Hilbert transform self-similar CLM`

- <https://arxiv.org/html/2603.25104> — Huang–Tong–Wang, *Self-similar finite-time blowups with
  singular profiles of the gCLM model: theoretical and numerical investigations.* This is the
  paper whose Appendix C.1 `solver/line_hilbert.py` implements. It is a **numerical**
  investigation; it does not certify, and it does not bound its own interpolation defect.
- <https://arxiv.org/pdf/2305.05895>, <https://arxiv.org/pdf/2209.09886>,
  <https://arxiv.org/pdf/2308.01528> — neighbouring gCLM / Hou–Luo self-similar work.

**Read:** the realization is borrowed and un-certified upstream. Measuring its defect is
useful *here* and is not a claim *there*.

## Q4 — does anyone bound the *derivative* operator's defect on a graded mesh in sup norm?

Query: `natural cubic spline derivative approximation error graded mesh sup norm boundary
condition pollution rigorous bound`

- <https://pmc.ncbi.nlm.nih.gov/articles/PMC10491664/> — graded-mesh cubic B-spline collocation,
  parameter-uniform convergence **in the maximum norm**.
- <https://www.johndcook.com/blog/2021/07/13/spline-error-estimates/> — the standard table:
  natural spline is `O(h^4)` for `C^4` data, and the **natural end condition degrades the order
  near the boundary** unless the data actually satisfies `f'' = 0` there.
- <https://arxiv.org/pdf/2507.05083> — error estimates for splines under various boundary
  conditions.

**Read:** classical, textbook-adjacent. The `f''=0` end-condition defect is a known,
named degradation, not a discovery. Novel content: **zero.**

## Q5 / Q6 — sweeps for anyone doing this on *this* operator with an unbounded graded whole-line grid

Queries: `Chen Hou computer-assisted proof Hou-Luo model rigorous bound on numerical
approximation error piecewise polynomial Hilbert transform`; `Chen Hou Huang rigorous numerics
"Hilbert transform" error bound spline interpolation blowup profile approximation error
certificate`

- <https://arxiv.org/pdf/2604.01868> — Chen–Huang–Li, the **target paper** (`HL_S2_nonsymmetric`).
  Numerical only; no rigorous discretization bound. *(Note: leg 52's search-index flag on this
  ID **stands** — it surfaced here inside a broad topical query, which is weak evidence of
  recall and is NOT a clearance. Recording the surfacing, not claiming the flag lifts.)*
- <https://jiajiechen94.github.io/research>, <https://epubs.siam.org/doi/10.1137/23M1580395> —
  Chen's programme; third-order Lagrange interpolation per interval for the Hilbert integral,
  with error control.
- <https://arxiv.org/pdf/2411.18361> — *Validated matrix multiplication transform for orthogonal
  polynomials with applications to computer-assisted proofs for PDEs* — the coefficient-basis
  analogue of the same concern.

**Read:** no hit does this on a `sinh`-graded **whole-line** grid reaching `|X| ~ 745` with a
natural-spline end condition. That is a gap in coverage, but it is a gap of *setting*, not of
*idea*, and the setting is this repository's own choice. **Not bankable.**

---

## What is therefore claimable, and it is narrow

1. This leg **re-derives** a standard consistency bound in a non-standard setting.
2. The only genuinely new number is the **ratio of that defect to leg 46/50's own budget**
   (`writeup/data/p2_route_l1_v1_interval.json`, `n = 801`: `budget = 3.5547e-10`,
   `Y0/budget = 2.068e-02`). That ratio is a fact about **this code**, not about the field.
3. **No link of the `L1`→`L4` chain moves.** Clay stays at ~0.05% behind Walls 1 and 2.
