# Leg 79 — Route-PC novelty pass (run BEFORE construction)

**Date:** 2026-08-06. **Agent:** LEG-H. **Branch:** `leg/pc-v1`.
**Verdict: `PROCEED_AS_AUDIT`.** This leg builds no new mathematics and claims no novel
mechanism. It adversarially audits one *logic* property of a downstream consumer —
`solver/port_certification.radii_polynomial_status` — against poisoned `Y_0`/`Z_1`/`Z_2`
inputs. The pass below exists to establish, *before* construction, (i) what the published
radii-polynomial theorem actually **assumes** about its constants, so that any hypothesis the
code fails to enforce is reported as *"a documented hypothesis our code does not check"* and
never as a discovery; and (ii) whether the specific failure modes probed are already named
hazards in the software-verification literature.

Per `writeup/novelty/README.md` and the lesson from leg 53: **links, not counts.** Every query
string below is verbatim, and every link returned that I judged on-topic is listed.

This leg is *complementary to, not a repeat of*, leg 69 (Route-IA). IA stress-tested the
**arithmetic** of the shared interval core (`solver/interval.py`) against exact rational ground
truth. This leg tests a **logic/domain-validation** property one level downstream, in a module
IA never touched. The two share a family (certificate infrastructure) and nothing else.

---

## What is being checked for prior art

* **(N1)** The radii polynomial theorem as published: are `Y_0`, `Z_1`, `Z_2` **hypothesised
  nonnegative**? If yes, then a negative value is not a "conservative" input — it is *outside
  the theorem*, and accepting it is accepting a fabrication.
* **(N2)** Is "a guard of the form `if x >= c: reject` is silently bypassed by NaN" a
  recognised, named soundness hazard, or would reporting it be a claim of discovery?
* **(N3)** Is the *method* — an adversarial poisoned-input battery banked as a permanent
  regression test against certificate-adjacent code — standard practice?

---

## Queries, verbatim, with the links returned

### Q1
`radii polynomial approach Y0 Z1 Z2 hypotheses nonnegative bounds computer-assisted proof`

- https://arxiv.org/abs/2605.07500 — *Computer-Assisted Proofs in Dynamical Systems: A Case
  Study of a Heteroclinic Orbit in the Shimizu–Morioka System.* States the four-step procedure
  (zero-finding formulation / approximate zero / approximate inverse / bound estimates) that
  `radii_polynomial_status` sits at the end of.
- https://arxiv.org/pdf/2404.08529 — Gray–Scott, constructive existence of localized patterns.
- https://arxiv.org/pdf/1704.03128 — *Polynomial interpolation and a priori bootstrap for
  computer-assisted proofs in nonlinear ODEs.*
- https://arxiv.org/pdf/1704.03827 — triangular cross-diffusion, computer-assisted proof.
- https://arxiv.org/pdf/2101.00684 — validated forward integration for parabolic PDEs.
- https://arxiv.org/pdf/2604.08715 — 1D Thomas model, localized patterns and periodic branches.
- https://arxiv.org/pdf/1706.10107 — analytic continuation of local (un)stable manifolds.
- https://arxiv.org/html/2608.01579 — computer-assisted counterexample to the planar Pompeiu
  and Schiffer conjectures.
- https://arxiv.org/pdf/1511.01414 — 3-component reaction–diffusion global bifurcation diagram.

**On-topic finding for (N1) — DECISIVE, and it is the standard statement, not a novelty.**
The literature is uniform: one *builds* `Y_0 ≥ 0`, `Z_1 ≥ 0` (usually `Z_1 > 0`) and
`Z_2 : (0,∞) → [0,∞)` **so that the hypotheses of the radii polynomial theorem are satisfied**,
and the polynomial `p(r) = Z_2 r² + (Z_0 + Z_1 − 1) r + Y_0` is described as having
**coefficients that are all positive** apart from the `−r`. Nonnegativity is a *hypothesis of
the theorem*, not a numerical accident: `Y_0` is a norm (`‖T(x̄) − x̄‖`), `Z_1`/`Z_2` are
suprema of norms. Consequently **a negative `Y_0`, `Z_1` or `Z_2` is not a pessimistic input —
it is an input the theorem says nothing about**, and a discriminant test that accepts it is
outside the imported result. This is the hypothesis the audit checks the code against.

### Q2
`Lessard van den Berg rigorous numerics radii polynomial theorem statement "Y_0" "Z_1" nonnegative constants hypothesis`

- https://www.math.vu.nl/~janbouwe/pub/rignumdyn.pdf — van den Berg & Lessard, *Rigorous
  Numerics in Dynamics* (AMS Notices 62(9):1057, 2015) — the canonical exposition.
- https://www.ams.org/notices/201509/rnoti-p1057.pdf — publisher copy of the same.
- https://www.math.mcgill.ca/jplessard/ODEs_files/final_draft.pdf — Hungria–Lessard–Mireles
  James, *Rigorous numerics for analytic solutions of differential equations: the radii
  polynomial approach* (Math. Comp.), the paper the method is named for.
- https://www.semanticscholar.org/paper/b80a918574d64797864781b877a89424dc9a3903 — record for
  the same paper.
- https://arxiv.org/pdf/1503.06315 — Breden–Desvillettes–Lessard, tridiagonal-dominant linear
  part (already in this repo's ledger, leg 57).
- https://link.springer.com/article/10.1007/s00205-017-1186-0 and
  https://arxiv.org/pdf/1509.08648 — ill-posed PDEs, periodic orbits in Boussinesq.
- https://arxiv.org/pdf/2403.10450 — planar Swift–Hohenberg localized patterns.
- https://arxiv.org/pdf/2211.16445 — localized radial solutions of semilinear elliptic systems.
- https://arxiv.org/pdf/1310.6531 — rigorous numerics for NLS.
- https://arxiv.org/pdf/1112.4874 — rigorous numerics in Floquet theory.
- https://www.math.mcgill.ca/jplessard/Publications_files/piecewise_smooth.pdf — piecewise-smooth
  systems.

**On-topic finding for (N1), confirming.** The bounds are defined by
`‖T(x̄) − x̄‖_ν ≤ Y`, `sup_{u∈B(1)} ‖(I − AA†)u‖_ν ≤ Z_0`, and
`sup_{u,v∈B(1)} ‖A(Df(x̄+rv) − A†)u‖_ν ≤ Z_1 + Z_2 r` — every one an **upper bound on a norm**,
hence nonnegative by construction. Nothing in this leg's finding is new mathematics; the
theorem's hypotheses are 2015-vintage textbook material. **The only question this leg can
answer is whether our code enforces them.**

### Q3
`validated numerics software input validation defensive checks trusted computing base computer-assisted proof errors`

- https://vncap.org/ — *Validated Numerics for Computer-Assisted Proofs* programme.
- https://icms.ac.uk/activities/workshop/validated-numerics-for-computer-assisted-proofs/ — ICMS
  workshop of the same name.
- https://arxiv.org/pdf/2003.06458 — *QED at Large: A Survey of Engineering of Formally Verified
  Software* — the trusted-computing-base framing (Rushby 1981): correctness of the whole reduces
  to correctness of a proper subset of components, **provided those components behave as
  expected**.
- https://www.aptori.com/blog/the-essential-guide-to-input-validation-for-secure-software —
  generic input-validation/defence-in-depth reference; listed for completeness, not load-bearing.
- https://www.researchgate.net/publication/4298569_Computer-assisted_proofs — general survey.
- https://arxiv.org/pdf/1911.06758 — *Any three eigenvalues do not determine a triangle*, an
  Arb-based validated computation; listed as an instance of the practice.

**On-topic finding for (N3).** The TCB framing is exactly the right idiom for this leg: a
kill-switch that a *caller* can talk into `closes=True` is a component that does not "behave as
expected", and it sits inside the certificate chain's trusted base. Auditing such a component
against adversarial inputs is standard software-engineering practice — so the **method** here is
routine, and this leg claims no methodological novelty either.

### Q4
`NaN silent comparison bypass guard floating point validation certificate software soundness`

- https://arxiv.org/html/2601.14059 and https://arxiv.org/pdf/2601.14059 — *Verifying
  Floating-Point Programs in Stainless.* The only on-topic hit; the rest of the result set was
  unrelated floating-point hardware patents (`US7730287`, `US7818548`, `US8683182`, `US8769248`,
  `US7653806`, `US8117426`, `US7849291`, `US7932910`) and is not listed as relevant.

**On-topic finding for (N2) — the hazard is named and documented.** The Stainless paper records
exactly this pattern: *omission of proper NaN handling causes code to return a valid output even
when the input is NaN*, and *code comments sometimes explicitly assume that a false comparison
implies the input is valid and within a certain range, a property that does not hold when the
input is NaN.* It also notes the non-reflexivity of IEEE-754 equality as a source of
unsoundness. **So if this leg finds a NaN bypass, it is reported as a known floating-point
hazard present in our code — never as a discovery.**

---

## Verdict and the constraint it places on this leg's report

`PROCEED_AS_AUDIT`, with three pre-committed constraints:

1. **The nonnegativity of `Y_0`, `Z_1`, `Z_2` is a published hypothesis of the imported
   theorem (Q1, Q2).** Any finding that our code evaluates the discriminant on negative inputs
   is reported as *"the code does not enforce a hypothesis of the result it implements"* — a
   software gap, not a mathematical one.
2. **A NaN-bypassed comparison guard is a named, documented hazard (Q4).** If found, it is
   reported as such, with a citation, and never as novel.
3. **The method is routine (Q3).** No methodological claim is made. The deliverable is a
   battery, its measured pass/fail counts, and a permanent regression test — magnitudes, not a
   theorem.

Nothing found in this pass gives grounds to skip the audit: the literature establishes what the
hypotheses *are*, and says nothing whatever about whether this repository's implementation
enforces them. That is measurable only by running it, which is what follows.
