# Leg 98 — Route-ICA novelty pass (run BEFORE construction)

**Date:** 2026-08-06. **Agent:** LEG-J. **Branch:** `leg/ica-v1`.
**Verdict: `PROCEED_AS_AUDIT`.** This leg builds no new mathematics and claims no novel
mechanism. It adversarially audits one *logic* property — whether
`solver/interval_certificate.interval_constants` / `radii_verdict` reject enclosures and
constants that violate the hypotheses they are imported under. The pass exists to establish,
**before** construction, (i) what the published radii-polynomial theorem *assumes* about
`Y_0`, `Z_1`, `Z_2`, so that any hypothesis the code fails to enforce is reported as *"a
documented hypothesis our code does not check"* and never as a discovery; (ii) whether an
ill-formed interval (`lo > hi`, NaN endpoint) is already a *named, standardised* failure class,
so that detecting one here is bookkeeping and not a finding; and (iii) whether the *method* —
a poisoned-input battery banked as a permanent regression test — is standard practice.

Per `writeup/novelty/README.md` and the lesson from leg 53: **links, not counts.** Every query
string below is verbatim, and every link returned that I judged on-topic is listed.

**Relationship to the neighbouring legs, stated so this leg cannot be read as a repeat.**
Leg 61 (KA) checked this same pipeline against a *published known answer* (CLN's Kawahara
radius) — correctness on a well-formed problem. Leg 69 (IA) stress-tested the *arithmetic
primitive* underneath (`solver/interval.py`) against exact rational ground truth. Leg 79 (PC)
ran the fabrication-rejection battery against the **sibling** pipeline's status function
(`port_certification.radii_polynomial_status`) and found 11/25 false accepts, since repaired.
This leg is leg 79's question asked of **this** pipeline's own verdict function. Nothing here
is new mathematics; the only question available to it is *whether our code enforces the
hypotheses it inherits*.

---

## What is being checked for prior art

* **(N1)** Are `Y_0`, `Z_1`, `Z_2` **hypothesised nonnegative and finite** in the published
  theorem? If so, a negative value is not a conservative input — it is *outside the theorem*,
  and a discriminant test that accepts it is evaluating something the theorem does not cover.
* **(N2)** Is "an interval with `lo > hi`, or with a NaN endpoint, is ill-formed and must be
  detected" an established, named notion — or would reporting it be a claim of discovery?
* **(N3)** Is an adversarial poisoned-input battery, banked as a permanent regression test
  against certificate-adjacent code, standard software practice?

---

## Queries, verbatim, with the links returned

### Q1 (2026-08-06)
`radii polynomial theorem hypotheses Y0 Z1 Z2 nonnegative upper bounds norms rigorous numerics`

- https://www.math.mcgill.ca/jplessard/ODEs_files/final_draft.pdf — Hungria–Lessard–Mireles
  James, *Rigorous numerics for analytic solutions of differential equations: the radii
  polynomial approach* — the paper the method is named for.
- https://www.researchgate.net/publication/274384127_Rigorous_numerics_for_analytic_solutions_of_differential_equations_The_radii_polynomial_approach — record for the same paper.
- https://arxiv.org/pdf/1503.06315 — Breden–Desvillettes–Lessard, tridiagonal-dominant linear
  part (already in this repo's ledger, leg 57).
- https://arxiv.org/pdf/2101.00684 — validated forward integration for parabolic PDEs via
  Chebyshev series.
- https://arxiv.org/pdf/2009.13597 — rigorous validation of a Hopf bifurcation in
  Kuramoto–Sivashinsky.
- https://arxiv.org/pdf/1112.4874 — rigorous numerics in Floquet theory.
- https://arxiv.org/pdf/1310.6531 — rigorous numerics for NLS.
- https://arxiv.org/pdf/1509.08648 — ill-posed PDEs, periodic orbits in Boussinesq.
- https://arxiv.org/pdf/1704.00029 — *A proof of Wright's conjecture.*

**On-topic finding for (N1) — DECISIVE, and it is the standard statement, not a novelty.**
The bounds are *defined as upper bounds on norms*: `Y ≥ ‖T(x̄) − x̄‖_X = ‖A H(x̄)‖_X`,
`Z_0`/`Z_1`/`Z_2` as suprema of operator norms over the unit ball; the radii polynomial is
`p(r) = Y + (Z_0 + Z_1 − 1) r + Z_2 r²` and the conclusion is drawn from `p(r) < 0` for some
`r > 0` with `A` injective. Every one of these constants is nonnegative **by construction, as a
hypothesis of the theorem** — this is 2015-vintage textbook material. Consequently a negative
`Y_0`, `Z_1` or `Z_2` is **not a pessimistic input**: it is an input about which the theorem
says nothing, and a discriminant evaluated on it is outside the imported result. This is
exactly the hypothesis leg 79 checked in the sibling pipeline, restated for this one.

### Q2 (2026-08-06)
`interval arithmetic reversed interval lo greater than hi invalid enclosure validation soundness`

- https://arxiv.org/pdf/2003.10623 — *Computer-Assisted Verification of Four Interval Arithmetic
  Operators* — states the three properties an interval implementation must have: **validity,
  soundness, tightness**, and notes the case analysis over magnitude relations between the
  argument bounds is exactly where hand-written implementations go wrong.
- https://arxiv.org/pdf/2107.05784 — *An Interval Arithmetic for Robust Error Estimation.*
- https://www.researchgate.net/publication/220261171_Interval_Arithmetic_with_Containment_Sets — containment-set formulation.
- https://interval.louisiana.edu/GLOBSOL/whatisop/node6.html — outward-rounding basics.
- https://drops.dagstuhl.de/storage/16dagstuhl-seminar-proceedings/dsp-vol08021/DagSemProc.08021.14/DagSemProc.08021.14-add.pdf — Wolff von Gudenberg, interval arithmetic and standardization.
- https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2006/n2067.pdf — C++ interval proposal.
- https://github.com/mauriciopoppe/interval-arithmetic-eval — an implementation that checks for
  empty/ill-formed intervals at construction; listed as an instance of the practice.

**On-topic finding for (N2) — the notion is standard, so nothing about it is a discovery.**
"Validity" is a *named* property of an interval implementation, distinct from soundness, and
`lo > hi` is the canonical validity violation. Reporting that our code does or does not check
it is a statement about our code only.

### Q3 (2026-08-06)
`IEEE 1788 interval arithmetic decorations invalid operand ill-formed interval standard`

- https://standards.ieee.org/ieee/1788/4431/ — IEEE Std 1788, Standard for Interval Arithmetic.
- https://ieeexplore.ieee.org/document/7140721/ — 1788-2015 publisher record.
- https://inria.hal.science/hal-01559955/document — *Introduction to the IEEE 1788-2015
  Standard for Interval Arithmetic* (Revol).
- https://link.springer.com/chapter/10.1007/978-3-319-31769-4_3 — *The Forthcoming IEEE
  Standard 1788 for Interval Arithmetic.*
- https://arxiv.org/pdf/2205.11837 — *Testing interval arithmetic libraries, including their
  IEEE-1788 compliance.*
- https://onlinelibrary.wiley.com/doi/10.1002/cpe.7856?af=R — Benet et al., a framework to test
  interval arithmetic libraries and their IEEE 1788-2015 compliance.

**On-topic finding for (N2), confirming and sharpening.** The standard carries a *decoration*
system `{com, dac, def, trv, ill}` precisely so that an **ill-formed** input is tracked and
propagates rather than being silently consumed. So "an ill-formed enclosure must be detected
and must not be allowed to produce a valid-looking verdict" is a **published requirement of the
relevant standard**, dated 2015. Anything this leg finds is a *conformance gap in our code
against a standard idea*, never a new idea.

### Q4 (2026-08-06)
`adversarial fault injection testing computer-assisted proof code trusted computing base regression test poisoned inputs`

- https://arxiv.org/pdf/2509.10819 — *Arguzz: Testing zkVMs for Soundness and Completeness
  Bugs* — the closest structural analogue: adversarially injected inputs used to separate
  **soundness** bugs (accepting what should be rejected) from **completeness** bugs. That is
  the exact partition this battery uses.
- https://arxiv.org/pdf/2509.07757 — *Empirical Security Analysis of Software-based Fault
  Isolation through Controlled Fault Injection.*
- https://www.emergentmind.com/topics/adversarial-testing and
  https://www.educba.com/adversarial-testing/ and https://nhimg.org/glossary/adversarial-testing/ — generic adversarial-testing references; listed for completeness, not load-bearing.

**On-topic finding for (N3).** Fault injection into trusted code handling untrusted data is
long-established practice, and the soundness/completeness partition is the standard framing.
The **method** here is routine; this leg claims no methodological novelty either.

---

## What this leg is therefore permitted to claim

Only this: **a measured count of how many hypothesis-violating inputs this pipeline's verdict
function accepts as closing, and the exact inputs that do it.** Not a theorem, not a new
hazard class, not a new method. If the count is zero the leg banks a regression test; if it is
nonzero the leg reports the failing cases and escalates without patching, exactly as leg 79's
finding was handled in the sibling pipeline.

**Pre-committed reporting discipline (discipline 73, magnitudes not booleans):** every case
reports the numbers the pipeline produced (`Y_0`, `Z_1`, `Z_2`, `r_min`, `r_max`), not just a
pass/fail flag, so that a reader can check the verdict arithmetic without rerunning it.

---

# Findings (written AFTER construction; the pass above is unedited since its commit `ac57551`)

**GATE: YES.** Quoting the gate verbatim — *"Under an adversarial battery of poisoned interval
enclosures (negative widths, NaN endpoints, non-containing enclosures) fed to
`interval_constants` / `radii_verdict`, does the pipeline ever incorrectly report a
closing/valid certificate?"* — **yes, 12 times out of 36 hypothesis-violating inputs (33.3%),
of which 8 are load-bearing.**

Substrate: `BorderedCLM` (a = 0 CLM, bordered), `n = 101`, `N = 103`,
`θ = (0, 0, 0, 0, −2)`. Positive controls: the honest certificate **closes** at the converged
iterate (`Y_0 = 1.396e-11`, `Z_1 = 2.754e-09`, `Z_2 = 7.993e+05`) and **does not close** at that
iterate displaced by `1e-3` (`Y_0 = 5.907e-03`), a separation of **4.23e+08×**.

| magnitude | value |
|---|---|
| cases | 39 |
| hypothesis-violating | 36 |
| **reported a CLOSING certificate anyway** | **12 (33.3%)** |
| of those, **load-bearing** — the same-magnitude hypothesis-*satisfying* input does NOT close | **8** |
| correctly rejected | 20 |
| raised (a refusal, but a loud one) | 4 |

## The two halves of the claim, separated

**(a) `radii_verdict` evaluates the discriminant on constants the theorem excludes.** This is
leg 79's finding, unrepaired, in the other pipeline. Six load-bearing cases:

* `Y_0 = −1.0, Z_1 = 0.3, Z_2 = 1.0` → **closes**, with a **negative** `r_min = −0.8780`.
  `Y_0 = +1.0` does not close (budget `0.2450`).
* `Y_0 = −1e6` → **closes**. `Y_0 = −inf` → **closes**, `r_min = −1.341e+154`, while
  `Y_0 = +inf` is correctly refused — the asymmetry shows the guard is arithmetic, not a
  hypothesis check.
* `Z_1 = −5.0` → **closes** (`Z_1 < 0` passes the `Z1 < 1.0` guard).
* `Y_0 = 1e3, Z_1 = −1e6` → **closes** on a budget of **5.000e+11**: a negative `Z_1` inflates
  `(1−Z_1)²/(2Z_2)` without bound and rescues an arbitrarily large residual. `Z_1 = +1e6`
  rejects the same `Y_0`.
* `Y_0 = −1e-30, Z_1 = 1−1e-16` → **closes**; the `+1e-30` counterpart does not.

**(b) `interval_constants` never checks the enclosure it is handed.** Two load-bearing cases,
and the second is the sharper one:

* An enclosure object reporting `F(z) ≡ [0, 0]` at the displaced iterate yields
  `Y_0 = 7.9e-323` and **closes**, where the true residual is `5.907e-03` — a lie of roughly
  **320 decades**, undetected.
* The honest enclosure **scaled by 1e-8** — `lo ≤ hi`, every endpoint finite, positive width,
  i.e. **passing every validity check that exists** — understates `Y_0` by **1.000e+08×**
  (`5.907e-03 → 5.907e-11`) and **closes**. No amount of interval-*validity* checking sees
  this; only a **containment** check does. This is the case that distinguishes the finding from
  leg 69's, which was about validity.

**(c) supplementary (H3): the weight vector is trusted too.** `w → −w` is accepted as a norm
and produces `Y_0 = −2.463e-28`, which then closes — the one end-to-end path in the battery
from structurally valid enclosures to a hypothesis-violating constant.

## What HELD — and it is not nothing

* **NaN is handled correctly, 4/4.** `radii_verdict`'s `if not (Z1 < 1.0)` is NaN-safe by
  construction. The exact hazard that defeated the sibling before its repair is **absent here**.
* **`Interval.__init__` refuses `lo > hi`** — leg 69's repair, still holding, now shown to cover
  this pipeline's residual path. It is why the negative-width residual cases raise rather than
  lie.
* **The `Z_1` path is hard to fool**: a Jacobian enclosure poisoned to the identity, with
  swapped endpoints, or with a NaN entry is rejected in all four attempts.

## Severity: LATENT, not ACTIVE — and that is a measurement, not a reassurance

No banked number in this repository is shown to be wrong. Every in-repo caller of
`radii_verdict` receives constants from `interval_constants`, where `Y_0 = max(w · mag(·))` and
`Z_1`, `Z_2` are weighted row-sum bounds over magnitudes — nonnegative whenever `w > 0`, and the
shipped weight is `exp(clip(·))`, strictly positive by construction. The unsound inputs are
reachable only by a caller that builds constants some other way, or hands in a fabricated
enclosure object. What the gap removes is the **guarantee**, not any current number — the same
scoping leg 69's finding carried.

## What this leg did NOT do, deliberately

It did not patch `solver/interval_certificate.py`, under any gate outcome, per its territory and
per the precedent set by legs 66, 69 and 79. The recommended repair — reject non-finite/negative
constants before the discriminant; return a structured verdict for `Z_2 = 0` instead of raising
`ZeroDivisionError`; validate `w`; and, the one the sibling does not have, **re-evaluate `F` in
float and refuse a non-containing enclosure** — is written out in `experiments/journal/leg_98.md`
and each of the seven GAP-PIN gates in `test_interval_certificate_adversarial.py` states the
assertion the repaired code should carry. **Invert those gates on repair; do not weaken them.**
