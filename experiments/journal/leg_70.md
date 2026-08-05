# Leg 70 — Route-RC: the realization audit of `solver/rescaled_spectrum.py`

Docs-only. Nothing was solved, nothing was diagonalized, no gCLM measurement was made — the
leg-42 ban is untouched and the audit script asserts that against its own AST before printing
anything (`[GUARD]`). Runner: `experiments/p2_route_rc_v1_realization_audit.py`.

## The gate, answered

> **Does `solver/rescaled_spectrum.py`'s discretization impose an origin (H^2-type) condition
> at X=0, or none (the maximal L^2 realization)?**

**NO — none is imposed.** J-4's assertion was made from Xu's paper; this leg confirms it from
the code, four independent ways. The no-branch is the one that lands.

### A. No collocation row sits at the origin

`theta_j = (j + 1/2) pi / K` is the midpoint grid. Rows *at* `X = 0`: **0 of 48, 0 of 96,
0 of 144**. The nearest row to the origin is at `X = 1.636e-2` (K=48), `8.181e-3` (K=96),
`5.454e-3` (K=144) — it moves in as `tan(pi/4K)` and never arrives. A boundary condition needs
a row to live in; there is no row within `5.5e-3` of the origin at the finest resolution used.

### B. The eigenproblem is square and carries no constraint row

`generator()` returns `solve(S, jacobian(b))`, a `144 x 144` dense matrix. Checked at source
level: `generator()` appends a row — **False**. `jacobian()` appends a row — **False**.
`newton()` appends a row — **True**, and that is the *only* append in the module. It is the
dilation gauge `sum_k k b_k = -1`, appended as a `K+1 x K` least-squares system, and its job is
to pick **which** fixed point on the dilation orbit, not to restrict the operator's domain. The
eigenproblem never sees it. That distinction is the whole audit: a gauge on the solve is not a
condition on the realization.

### C. All three origin-evaluated quantities are gauge scalars

| symbol | where | role | restricts admissible `b`? |
|---|---|---|---|
| `h0` | `rescaled_spectrum.py`, 4 occurrences (163, 215, 219, 235) | `H(Omega)(0)`, enters `c_omega` via gauge (N) | no |
| `kk` | `rescaled_spectrum.py`, `newton()` only, 5 occurrences (259–286) | `Omega_X(0)/2`, the appended gauge row | no |
| `lam_dx0` | `critical_dissipation.py`, 4 occurrences (246–263) | `(Lambda^p Omega)_X(0)`, gauge (N') | no |

Every one of them is contracted into a **scalar** (`c_omega`, or a single Newton row). None
removes a basis element, applies a projector to the generator, or adds a row to the
eigenproblem — which are the only three shapes a domain restriction could take here.

*(Scoping note: `kk` is deliberately scoped to `newton()`. An unscoped grep returns 10
occurrences, but 6 of them are an unrelated loop index inside `_velocity_matrix`'s recurrence.
Reporting 10 would have overstated the origin's footprint in the module by 2x.)*

### D. The one piece of evidence pointing the other way, reported not buried

Every basis function is `sin(k theta)` with `theta = 2 arctan X`, so as `X -> 0` it behaves as
`2 k X`: measured at `X = 1e-6`, the deviation from exact linearity is `1.4e-8` relative. So
**the trial space is odd-analytic at the origin**, while the maximal realization's continuum
modes go like `X^{1 - i y}` — a fractional power that is *not* in the span.

Someone could read that as "the discretization does impose analyticity, hence the origin
condition." That reading is wrong, and it is worth writing down why, because it is the trap
this leg exists to walk past:

1. **Smoothness of the trial space is not a condition imposed on the operator.** The scheme is
   *collocation* — the equation is enforced at K interior points and nowhere else. Nothing
   constrains the residual's behaviour near `X = 0`, which is precisely where the realization is
   decided. A Galerkin projection onto a domain-constrained subspace would be a different
   object; this is not that.
2. **The module's own docstring already reports the continuum surviving** (lines ~110–119): "one
   eigenvalue at -1 isolated to 1e-14, everything else pinned to the imaginary axis (the
   discretized continuum) and moving with K", and "THAT IS WHY A CONVERGENCE FILTER IS
   MANDATORY". If the origin condition were in force, the strip would be empty apart from
   `{0, -1}` and there would be nothing for the filter to remove. The filter's existence is
   evidence against its own necessity being avoidable.
3. **The banked counts settle it arithmetically** — §E below.

### E. The decisive corroboration: the count is exactly `K - 3`

Arithmetic on numbers already on file (`TECHNICAL_P2_ROUTEI_V1.md` §1 table), no recomputation:

| K | unstable at `mu = 0` | `K - n` | fraction | max Re |
|---|---|---|---|---|
| 48 | 45 | **3** | 0.937500 | +4.524 |
| 96 | 93 | **3** | 0.968750 | +4.546 |
| 144 | 141 | **3** | 0.979167 | +4.558 |

The deficit is **constant at 3** across all three resolutions. The count grew by **96 as the
dimension grew by 96** — 1:1 — while `max Re` moved only **0.034** across a 3x refinement.

A resolved finite-dimensional unstable manifold has a **K-independent** dimension. This one is
`K - 3` and rising as a fraction (0.9375 -> 0.9688 -> 0.9792), with no sign of saturation. That
is a **dimension-proportional count**, the standard signature of a discretized *continuous*
spectrum, and it is only possible if the discretization is resolving the strip — i.e. the
maximal `L^2` realization. On the origin-`H^2` realization the strip is empty apart from
`{0, 1}` and the count would have been bounded, not `K - 3`.

**So "141 of 144 unstable directions" is not a Morse index. It is the essential spectrum of the
maximal `L^2` realization, counted at `K = 144`, and the number 141 is a statement about the
grid as much as about the operator.** Quote it at `K = 288` and it would read 285.

### The realization is set in exactly one place

`CriticalDissipativeFlow(RescaledFlow)` (which is what Route-I's `unstable_count` actually
diagonalizes, via `marginal_flow.py`) inherits `self.B = OddCompactBasis(K)` unchanged and adds
only the `-mu Lambda^p` term and the re-derived gauge (N'). `marginal_flow.unstable_count` calls
`eigvals(solve(flow.B.S, flow.jacobian(b)))` — same square matrix, same absent origin condition.
So the gate's module governs the count even though the count was produced two modules
downstream, and **a future origin-conditioned re-run has exactly one place to intervene:
`OddCompactBasis`.** That is the useful engineering finding for whoever runs the correction.

### What this does NOT touch

The `mu > 0` half of Route-I's inversion. Dissipation collapses the spectrum onto a *discrete*
negative ladder `(0, ~-1, ~-4.7)` whose gap is flat in `mu` across four decades; a discrete
ladder is not realization-smear. J-4 says this and the audit gives no reason to revisit it. The
DSS verdict also survives — nothing bifurcates in either realization.

## The correction list for the orchestrator

**19 quote sites** across 10 files. **8 name the realization at the site. 1 discloses it in
substance without the word** (BLOG_J:184, "that count of 141 needs the choice named next to
it"). **10 are gaps.** Disclosure was scored within ±12 lines of the quote, because a reader
lifting a number reads the lines around it, not page 200 of the same file — 6 of the 10 gaps sit
in files that *do* disclose elsewhere, which is exactly the failure mode this scoring is for.

All 10 are outside leg 70's territory. Reported, not edited:

| # | site | note |
|---|---|---|
| 1 | `PHASE2_P2_NOTES.md:2175` | §30 headline `45/48, 93/96, 141/144`; disclosure is 205 lines later at J-4 |
| 2 | `PHASE2_P2_NOTES.md:2176` | "a fixed point with a 141-dimensional unstable manifold" — the phrase "141-dimensional unstable manifold" is the specific thing the `K-3` scaling refutes |
| 3 | `experiments/JOURNAL.md:240` | leg-I entry, "the headline, which is real" |
| 4 | `writeup/README.md:336` | disclosure is 46 lines later at 380–383 |
| 5 | `writeup/4_p2_lottery/BLOG_P2_ROUTEI_V1.md:44` | **the worst one — this file contains the word "realization" zero times** |
| 6–8 | `TECHNICAL_P2_ROUTEI_V1.md:72,73,74` | the source-of-truth table itself; callout is at line 18, 54+ lines above |
| 9 | `TECHNICAL_P2_ROUTEI_V1.md:77` | "a 141-dimensional unstable manifold is not an attractor" |
| 10 | `BLOG_P2_ROUTEJ_V1.md:170` | resolved 14 lines later at 184, so this is a proximity gap, not a substantive one — lowest priority of the ten |

**The sentence to insert at each gap site** (from the runner, `DISCLOSURE_SENTENCE`):

> This count is the spectrum of the MAXIMAL L^2 REALIZATION: our discretization imposes no
> origin condition at X = 0 (Xu arXiv:2607.19762 Prop 2's dichotomy), and the count is exactly
> K - 3 at K = 48, 96, 144, i.e. proportional to the discretization dimension rather than a
> realization-independent Morse index. On the origin-H^2 realization the open strip is empty
> apart from {0, 1}.

**Two sites need more than the sentence.** Numbers 2 and 9 above use the phrase *"a
141-dimensional unstable manifold"*. That phrase is not merely under-labelled — it is false in
the way the `K - 3` scaling makes precise, since the object has no 141-dimensional unstable
manifold in any realization; 141 is a resolution. Recommended replacement wording: *"an unstable
set filling §26's essential spectrum, counted as K - 3 = 141 directions at K = 144"*.

**J-4 itself needs no correction.** Its claim "OUR DISCRETIZATION HAS NO ORIGIN CONDITION" is
confirmed. The one addition worth making, if the orchestrator wants it, is that J-4's stated
correction item ("re-run I5 with an origin condition") now has a located intervention point:
`OddCompactBasis` in `solver/rescaled_spectrum.py`, the single class all three modules share.

## Lesson

Lesson 70 held, and got sharper. "A spectrum is not a property of an operator until you name the
realization" is the qualitative half. The quantitative half this leg adds: **when a count of
unstable directions scales with the discretization dimension, the realization has already
answered you** — `K - 3` at three resolutions is the realization confessing, in arithmetic, with
no new solve required. That test is free, it works on numbers already banked, and it should be
run on any eigenvalue count before it is quoted.
