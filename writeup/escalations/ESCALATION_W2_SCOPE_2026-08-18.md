# ESCALATION — W2's scope: does a NONUNIQUENESS certificate count?

**Raised** 2026-08-18 by the Conductor at the integration of `V5` (leg 402).
**Status: OPEN. RECORDED, NOT RULED.** A wall's WORDING is the user's, never the Conductor's.

## The measurement that raised it

`V5` audited `arXiv:2509.25116` (Hou–Wang–Huang, *Nonuniqueness of Leray–Hopf solutions to the
3D Navier–Stokes equations*, v2) at full text and answered W2's own pre-committed test as a
**separate clause**, per user ruling Q4:

- The certified profile is **genuinely 3D**. W2's predicate (`writeup/data/p2_route_t4_v1.json`
  :: `controls.C_3D`, located in the record, **not invented**) fails on all three conjuncts.
- `max|u_φ| = 8.754198315291823`, **57.25%** of `max|u_r| = 15.291462690010507` — a principal
  component, not a numerical residue.
- The shipped data **is** the certified object: `λ = 0.1131420327438595` matches the printed
  eigenvalue to **sixteen significant figures**.
- The object is **axisymmetric** (`main.tex:2509`). `V5` flagged this and, under its own
  pre-committed rule R2-c, did **not** let it bear on the verdict.

## The question, which the Conductor is not ruling

W2 as written states: *"Every published work stating a **3D singularity theorem** with a
certificate obtains its 3D-ness somewhere other than the certificate."* This paper states a
**nonuniqueness** theorem, not a singularity theorem. On the wording, W2 does not apply to it,
and the Conductor has recorded W2 as **neither broken nor strengthened** by this finding.

**But the wall's PREMISE is broader than its wording.** The reason W2 matters is the claim that
no certificate has ever certified a genuinely 3D fluid object *by itself*. On `V5`'s measurement
a Grade-A fluid certificate now demonstrably encloses a genuinely 3D object — for nonuniqueness
rather than for blow-up.

**Three readings, all defensible, and the Conductor may rule none of them:**

1. **Wording governs.** W2 is about singularity theorems; a nonuniqueness certificate is out of
   scope; W2 is untouched. *(This is what is currently written in `WALLS.md`, marked as the
   escalated reading, not as a ruling.)*
2. **Premise governs.** W2's real content is "no certificate supplies its own 3D-ness"; that is
   now false in the fluid setting, and W2 should be **narrowed by measurement** to singularity
   certificates explicitly, recording that the general form has fallen.
3. **Re-open condition (i).** Lane T's re-open condition (i) is *"a demonstrated, genuinely-3D
   closure meeting the wall's own pre-committed test."* If a nonuniqueness certificate counts as
   such a closure, **condition (i) may already be met** and Lane T's deferral is live again.

**Reading 3 is the one with a ranking consequence, which is exactly why the Conductor is not
choosing.** Lane T is DEFERRED by user ruling (2026-08-14); a deferral set by ruling is not
undone by a Conductor's reading of a wall's scope. A ban or a wall is superseded by a
**MEASUREMENT**, never by a decision — and the measurement here is about a *different theorem
type* than the wall names, which is precisely the ambiguity.

## What is NOT in question

- `V5`'s clause-2 answer itself. It used W2's own pre-committed test and did not invent one.
- W3, which this audit did not test (it did not run W3's prose criterion) and does not move.
- The separate, still-open `PUB_0C` escalation about "published" vs journal-ref, which this
  paper also raises (`ESCALATION_PUB0C_PUBLISHED_2026-08-18.md`).

## What happens while this is open

Nothing stops. `WALLS.md` records reading 1 with a pointer here. No lane is re-ranked on it.
