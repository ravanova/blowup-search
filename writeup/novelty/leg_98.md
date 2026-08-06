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
