# ESCALATION — W3's BREAKING TEST NAMES TWO DIFFERENT PREDICATES, AND A PAPER NOW SITS BETWEEN THEM

**Raised:** 2026-08-18, by the Conductor, on the return of leg 399 / `V3` (branch
`leg/399-v3-gradeA` @ `16ba44e`, landed to `main`).
**Class:** defective ban/wall **WORDING**. Under the standing rule — *a ban is superseded by a
MEASUREMENT, never by a decision; a defective ban WORDING is a user escalation* — **the Conductor
may not rule this and has not.** Ranking consequences taken below are rankings, not rulings.
**Status:** **OPEN — awaiting user.**
**Work has not stopped.** Wave 4's other two units (`L2′`, `V-W3`) are in flight and untouched by
this. Nothing was retracted, no ban was lifted, narrowed, reworded or re-read, and
`plan_of_record.py` is byte-unchanged.

---

## 1. THE DEFECT, IN ONE PARAGRAPH

`WALLS.md` W3's **BREAKING W3 CONSISTS OF** clause names, in the same sentence, **two predicates that
are not the same predicate**:

> "an interval enclosure of a blow-up solution of a dissipative *fluid* equation — any dimension, any
> model, provided the dissipative term is inside the certified equation **and the object is a genuine
> finite-time singularity**. Pre-committed test, **and `V3`'s grading predicate**: leg 174's own
> Grade-A criterion, applied unchanged."

**Leg 174's Grade-A criterion has no singularity clause.** Quoted at source from
`writeup/PUB_0C_CENSUS_SPINE.md` §1, unchanged:

> *Grade A* — "the interval-arithmetic certificate encloses a solution of an equation that itself
> carries the dissipative term."
> *fluid* — "the equation is a genuine fluid-dynamics equation (transport nonlinearity,
> incompressibility or a fluid-adjacent structure), not an off-axis scalar/complex-field model."

Two clauses. Neither says *blow-up*, *singularity*, or *finite time*. So the wall's prose test and
the wall's own named grading predicate **differ by exactly one requirement** — and until leg 399 that
difference had never been load-bearing, because nothing occupied the gap.

## 2. THE OBJECT THAT NOW OCCUPIES THE GAP

**`arXiv:2509.25116` — Hou, Wang, Yang, *Nonuniqueness of Leray–Hopf solutions to the unforced
incompressible 3D Navier–Stokes equation*, v2 (19 Mar 2026).** Read at full text by `V3`; row `R1`
of `writeup/data/p2_route_v3_gradeA_v1.json`; adjudication in `experiments/journal/leg_399.md`.

**It passes leg 174's criterion on both clauses.**
- *Grade A.* Proposition 1, eq. (1.15), p.5: the enclosed perturbation `Ū` satisfies an equation
  containing `−ΔŪ`, and `Ũ = U + Ū` solves the certified system (1.12), which carries `−ΔŨ`. The
  enclosure mechanism is named by the paper itself, §7.3, p.55: *"All pointwise evaluations `f_{i,j}`
  are computed with interval arithmetic to enclose round-off."*
- *fluid.* Eq. (1.1): `∂_t u + u·∇u − Δu + ∇p = 0`, `div u = 0`. The unforced 3D incompressible
  Navier–Stokes equations. Not fluid-*adjacent*; the equation Clay asks about.

**It fails the prose test's extra requirement, and the paper says so itself**, §1.2, p.2:

> *"The readers should not confuse this self-similar setting, which starts from singular initial
> data, with the backward self-similar setting related to finite-time singularities from smooth
> initial data."*

Theorem 1's solutions are *"smooth for positive times."* The certified object is a **forward**
self-similar profile underwriting **non-uniqueness**, not a finite-time singularity.

**It had never been graded here.** It is absent from leg 174's 11-row ledger despite v1 predating
leg 174; leg 242's control net surfaced it but, in `WALLS.md`'s own words, graded it against nothing
because that was not leg 242's gate. Leg 399 is the first grading of this row in this record.

## 3. THE THREE QUESTIONS. THE CONDUCTOR ANSWERS NONE OF THEM.

**(Q1) Which wording governs W3 — the prose test (with the finite-time-singularity requirement) or
the named grading predicate (leg 174's two clauses, applied unchanged)?**
Under the predicate, **W3 is broken and the cell is filled**. Under the prose test, **W3 stands and
the cell is still empty of a certified singularity**. Both readings are available on the text as
committed; the wall asserts they are the same test, and they are not.

**(Q2) If the prose test governs, does W3's headline statement still say what it means?** The
headline reads *"No certified (interval-enclosed, equation-carrying-the-dissipative-term) blow-up
exists for any fluid equation, in any dimension."* That sentence survives Q1 either way. But the
wall's **title** — *"The Grade-A × fluid cell is empty"* — does not: on leg 174's own definitions
that cell is now **occupied**. A wall whose title and whose test disagree is a wording defect
independent of Q1's answer.

**(Q3) Does leg 174's banked `the_empty_cell.meaning` need correcting, and by whom?**
`writeup/data/p2_route_vbs_v1_scoping.json::the_empty_cell.meaning` reads *"no published work applies
interval arithmetic to a DISSIPATIVE fluid equation's own self-similar object."* **That sentence is
now measured FALSE** — `2509.25116` does exactly that, and the word *"self-similar"* is in it, so no
reading of it survives. **The Conductor has NOT edited the banked artefact**: it is another leg's
measurement, and rewriting a banked datum to match a later finding is precisely how a record stops
being a record. It is flagged here and left standing.

## 4. WHAT THE CONDUCTOR DID DO, AND WHY IT IS NOT A RULING

`V3`'s **pre-committed reading (a)**, written into `STATE.md` before dispatch, said: *a YES breaks W3
and kills Lane V's premise, reported first, recorded as someone else filling the cell — which is not
this repository moving a link.* **The gate answered YES. The reading FIRED, and it is honoured as
written, not re-interpreted after the fact.** Pre-committed readings exist so that a returning
measurement cannot be argued out of its consequence, and this one is inconvenient in exactly the way
that makes honouring it worth something.

So: **Lane V is DEMOTED from PRIORITY to HELD**, and **Lane L becomes the sole priority lane.**
That is a **ranking**, which is a decision, and a decision supersedes no measurement. It is reversible
by the user in one line. It does **not** assert that W3 is broken; W3's status is recorded as
**DISPUTED / UNRULED** until Q1 is answered.

The Conductor also notes, without weighting it: even on the prose reading, W3 is not where it was.
The gap between *"no certified dissipative-fluid self-similar object exists"* and *"no certified
dissipative-fluid **singularity** exists"* is now the whole of the wall, and that gap is one paper
wide.

## 5. WHAT THIS IS NOT

**No L1→L4 link moved.** Somebody else certified something; this repository graded it. Grading
another group's paper is not construction and is not progress toward Clay, and `V3` says so in its
own §5. **Clay stays ~0.05%.** Whichever way Q1 is ruled, the programme is not closer to a proof
than it was yesterday — it is better informed about which wall it has been standing in front of.

**The YES is not audited.** It rests on Hou–Wang–Yang as published. `V3` audited no certificate, read
one database, title-screened only, and banked Semantic Scholar as a **gap, not a zero**, because no
API key exists in this environment. `V3`'s own costed next unit — an adversarial full-text audit of
`2509.25116` to leg-309 depth, 4–8 h — is the unit that decides whether the YES survives contact, and
it is not dispatched pending this ruling, because what it should test depends on Q1.

## 6. UNRELATED DEFECT SURFACED IN PASSING, RECORDED SO IT IS NOT LOST

Leg 174's ledger grades fractional Burgers (`arXiv:0804.3549`) `fluid_adjacent = TRUE`, while
`PUB_0C_CENSUS_SPINE.md` §2 calls `arXiv:2404.04054`'s viscous Burgers *non-fluid*. `V3`'s row `R8`
does not depend on the tension (it carries a second, independent disqualifier), but the next
Burgers-family row will. **Flagged, not ruled, not repaired.**
