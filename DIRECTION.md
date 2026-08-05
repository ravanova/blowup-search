# DIRECTION — the leg queue

**Owner: the Decision Maker (Fable 5). No other agent edits this file.**

This is the Decision Maker's durable state. It exists so a DM whose context has bloated can be
discarded and recreated from the file instead of re-derived from the whole repository.

It is **not** `plan_of_record.py`. The plan carries the committed sequence and exactly one
stage marked `NEXT`; this file carries the *exploration* routes running alongside it. Promoting
a route from here into the plan's committed sequence is escalation #1 in `ORCHESTRATION.md` §8
and needs the user.

---

## Status

**LIVE — queue filled 2026-08-05 by the DM, after `TC`'s gate answered NO at leg 53.**

Last leg number used: **53** (Route-TC v1, gate answered NO). Legs **54–57** are dispatched
below; queue items **58–60** are ranked and dispatchable but unassigned.

---

## Live assignments

| Slot | Leg | Route | Critical path? | Difficulty (pre-registered) | Branch | Gate |
|---|---|---|---|---|---|---|
| LEG-A | 54 | **MM** — the mismatch: spend the shape of `A` | **YES** (stage `MM`, `NEXT`) | heavy | `leg/mm-v1` | Does a non-block-diagonal `A` bring the assembled `Z₁` below 1, on the `a=0` CLM object at `s < 0.394`? |
| LEG-B | 55 | **NB** — does the real target have finite norm at all? | no | standard | `leg/nb-v1` | Is `‖HL_S2_nonsymmetric‖_{ℓ¹_w}` finite for some admissible `s < 0.394`? |
| LEG-C | 56 | **TN** — enclose L1 step one's *other* named gap | no | heavy | `leg/tn-v1` | Can the `(H, D)` consistency defect be enclosed below leg 46's `Y₀` budget at `n = 801`? |
| LEG-D | 57 | **XS** — the shape dichotomy against published certificates | no | light | `leg/xs-v1` | Does any published radii-polynomial certificate have an **off-diagonal** unbounded part with a non-decaying tail inverse? |

Exactly one of the four is the stage `plan_of_record.py` marks `NEXT` (currently `MM`, LEG-A).
The other three are independent exploration routes.

**Figure numbers are pre-allocated to avoid a merge collision** (`fig48` is already taken twice):
leg 54 → `fig49`, leg 55 → `fig50`, leg 56 → `fig51`, leg 57 → `fig52`. `writeup/build_figures.py`
and `writeup/curate_evidence.py` are **append-only** shared surfaces for these four legs: append
exactly one block at the end, never edit another leg's block.

## Queue

Ranked. Each entry needs all six fields or it is not dispatchable.

```
### 54 — ROUTE-MM: THE MISMATCH (critical path, stage `MM`)
**Thesis.** Leg 53 assembled the four terms and the polynomial did not close, and the term
that ran out — `Z₁`'s block coupling — exists only after assembly (lesson 89). Four of the
five degrees of freedom are now measured and banned: `s`, the weight family, the split `K`,
the border direction. The one remaining free choice is the SHAPE of the approximate inverse
`A`, and the method's block-diagonal `A = Γ⁻¹ ⊕ A_tail` is precisely what makes the coupling
a term at all. This leg spends that choice. MM-1 writes the mismatch as an inequality rather
than a mood: `Z₁ ≥ |1 − K/2| · (w_{K+1}/w_K) · ‖A_tail e_{K+1}‖_w / w_{K+1}`, which holds for
EVERY finite block because that sub-block does not contain `Γ⁻¹` — with leg 53's measured
second factor (0.94 … 1.33) it is a statement that no block-diagonal `A` can work here. MM-2
is the one move that is not a tuning: an `A` whose off-diagonal blocks are NOT zero — one step
of block Gauss–Seidel across the split, or the Schur complement of the coupling — measured on
the SAME assembled object with the SAME controls (leg 53's dissipative positive control that
reaches `Z₁ = 0.9156` at `μ = 2`, and the border-direction negative controls REWIRED through
the amplitude column per lesson 90). MM-3 is the novelty pass first, with links not counts.
Scope discipline, in leg 53's own wording: `Z₁[Γ←tail]` CONTAINS `Γ⁻¹`, so what is
established is about the block-diagonal `A`, not that no finite block can close it — the
finite-block-independent sub-block bottoms out at 0.9961, BELOW 1, and that is exactly why
this is a real question rather than a formality.
**Gate.** Does an approximate inverse that is NOT block diagonal bring the assembled `Z₁`
below 1, on the `a = 0` CLM object, in a class with `s < 0.394`?
  yes -> Report the assembled terms and the POSITIVE INTERVAL (`r_max > 0`, not `r = 0`), then
         re-run on `HL_S2_nonsymmetric`. Claim nothing about the target before that run —
         `Y₀ = 0` here for the banned degenerate reason (the anchor IS one basis mode).
  no  -> STOP building `ℓ¹`-Fourier radii-polynomial certificates for inviscid self-similar
         transport, and say so in the plan (this is `T`'s own no-branch). Do NOT re-enter by
         tuning `s`, the weight family, the split, or the border — all four are measured dead.
**Territory.** experiments/p2_route_mm_v1_shape.py, experiments/p2_route_mm_v1_shape_evidence.py,
               experiments/p2_route_tc_v1_assemble.py (leg 53's runner — MM owns it, nobody
               else touches it), solver/spectral_certificate.py, test_spectral_certificate.py,
               writeup/4_p2_lottery/BLOG_P2_ROUTEMM_V1.md,
               writeup/4_p2_lottery/TECHNICAL_P2_ROUTEMM_V1.md,
               writeup/data/p2_route_mm_v1_shape.json, writeup/figures/fig49_route_mm_v1_shape.png,
               writeup/novelty/leg_54.md, experiments/journal/leg_54.md
**Difficulty.** heavy
**Independence.** Sole owner of `solver/spectral_certificate.py` and both TC/MM runners. No
other live leg imports the assembled object for WRITE; legs 55 and 57 may import it read-only.
```

```
### 55 — ROUTE-NB: DOES THE REAL TARGET HAVE FINITE NORM AT ALL?
**Thesis.** Every result in legs 51–53 is measured on the `a = 0` CLM anchor, and the standing
ceiling says the real target is different for two reasons: the anchor IS one basis mode (so
`Y₀ = 0` degenerately) and — this is the clause worth testing — `HL_S2_nonsymmetric` "does not
have finite norm in the class where the operator is least bad." That second clause is asserted
in the ban list and, as far as the repository shows, has never been MEASURED. It decides
something MM cannot: even if MM's gate answers YES, its yes-branch promises a re-run on the
target, and that re-run is void if the target is not in the space. So compute it directly —
project `HL_S2_nonsymmetric` (from `solver/bordered_hl.py`, Newton-converged to 5.66e-15 at
n=201) into the compactified/Möbius basis `solver/spectral_certificate.py` already defines,
and measure the decay of its coefficients `|ĥ_k|` on a resolution ladder (n = 201/401/801,
M sweep), with the weighted `ℓ¹_w` partial sums for `s = 0, 0.3, 0.39` and the flat class.
The reportable quantity is the SHAPE of the ladder (lesson 72) — the fitted decay exponent
`|ĥ_k| ~ k^{−p}` with its resolution drift — not one endpoint. Finiteness is `p > 1 + s`.
Positive control that can fail: the same pipeline on the `a = 0` CLM anchor, whose coefficients
are exactly one mode, must report `p = ∞` / exact truncation. Negative control: a deliberately
`|X|^{−1}` far field must report `p` at the divergent threshold.
**Gate.** Do `HL_S2_nonsymmetric`'s compactified-basis coefficients decay fast enough that
`‖·‖_{ℓ¹_w}` is finite for at least one admissible `s < 0.394`, with the exponent stable
across the resolution ladder?
  yes -> The target IS in an admissible class, and the ban-list clause asserting it is not is
         factually wrong. Report the exponent and the margin, and ESCALATE the ban-text
         correction to the user (escalation #2) — the DM does not amend bans.
  no  -> The target is outside every admissible class. That is a SECOND, independent reason
         this lane cannot reach it, and it voids MM's yes-branch re-run regardless of how MM
         answers. Record the measured exponent, and stop proposing the target-basis re-run.
**Territory.** solver/target_norm.py (new), test_target_norm.py (new),
               experiments/p2_route_nb_v1_targetnorm.py,
               experiments/p2_route_nb_v1_targetnorm_evidence.py,
               writeup/4_p2_lottery/BLOG_P2_ROUTENB_V1.md,
               writeup/4_p2_lottery/TECHNICAL_P2_ROUTENB_V1.md,
               writeup/data/p2_route_nb_v1_targetnorm.json,
               writeup/figures/fig50_route_nb_v1_targetnorm.png,
               writeup/novelty/leg_55.md, experiments/journal/leg_55.md
**Difficulty.** standard
**Independence.** Imports `solver/spectral_certificate.py` and `solver/bordered_hl.py`
READ-ONLY (no diff in either — that is a merge-gate condition, not a preference). It measures
the OBJECT, not the certificate, so its answer does not depend on MM's shape of `A`, and MM's
answer does not depend on it. It is not new `ℓ¹`-Fourier radii-polynomial machinery: no `A`,
no `Y₀`, no `Z₁`, no polynomial — a norm of a profile.
```

```
### 56 — ROUTE-TN: ENCLOSE L1 STEP ONE'S *OTHER* NAMED GAP
**Thesis.** `solver/interval_certificate.py` closes the radii polynomial on
`HL_S2_nonsymmetric` at n = 201/401/801 — and its own capability entry names exactly two
things that make it step one of `L1` rather than `L1`: the far-field tail (which legs 51–53
attacked in the coefficient basis, and which MM may be closing off) and **the consistency of
`(H, D)`**, i.e. that the STORED discrete operators are treated as exact data when they are
really discretizations of the continuous Hilbert transform and derivative on the graded grid.
The second gap has never been measured, and it lives in a completely different branch of the
codebase (sup-norm collocation, interval arithmetic) from the `ℓ¹`-Fourier lane. This leg
encloses it: rigorous bounds on `‖H_disc − H‖` and `‖D_disc − ∂_X‖` as operators between the
weighted sup-norm spaces the certificate uses, on the actual graded grid, using the existing
outward-rounded interval kernel and the compensated matvec. The comparison quantity is
pre-committed: leg 46's `Y₀` budget at n = 801 (`Y₀/budget = 2.07e-02`). NOTE: this is not
"closing the truncation gap by extending the domain" — that ban is about domain reach, whose
trend was measured with the wrong sign at leg 47; the domain is FIXED here and the quantity
is a discretization defect at fixed reach.
**Gate.** Can the `(H, D)` consistency defect be enclosed by a rigorous bound that is smaller
than leg 46's `Y₀` budget at n = 801, with a convergence rate measured across n = 201/401/801?
  yes -> One of L1 step one's two named gaps closes, and the REMAINING gap is the far-field
         tail alone. Say exactly that, and nothing about `L1` being done.
  no  -> Report the magnitude and the rate. If the defect exceeds the budget, the collocation
         realization cannot carry `L1`, and the coefficient basis is the only lane left for it
         — which makes `L1`'s fate identical to MM's. Stop proposing grid-basis repairs.
**Territory.** solver/interval_certificate.py, test_interval_certificate.py,
               solver/interval.py, test_interval.py,
               experiments/p2_route_tn_v1_consistency.py,
               experiments/p2_route_tn_v1_consistency_evidence.py,
               writeup/4_p2_lottery/BLOG_P2_ROUTETN_V1.md,
               writeup/4_p2_lottery/TECHNICAL_P2_ROUTETN_V1.md,
               writeup/data/p2_route_tn_v1_consistency.json,
               writeup/figures/fig51_route_tn_v1_consistency.png,
               writeup/novelty/leg_56.md, experiments/journal/leg_56.md
**Difficulty.** heavy
**Independence.** Different basis (graded collocation, sup norm), different modules, different
object emphasis from MM. No file overlap with 54, 55 or 57. See open direction question #1 —
if the user reads the "no further machinery before MM answers" ban as covering this branch and
not just `ℓ¹`-Fourier, this leg is pulled and item 58 is promoted into slot C.
```

```
### 57 — ROUTE-XS: THE SHAPE DICHOTOMY AGAINST PUBLISHED CERTIFICATES
**Thesis.** Lesson 87 says a certification method has a SHAPE and the shape is a property of
the operator: multiplier or shift. Legs 51–53 turned that into this lane's whole explanation —
the standard tail estimate works because the unbounded part is a MULTIPLIER (cut an entry of
size `Λ_M`, the tail inverse is `1/Λ_M`), and here it is OFF-DIAGONAL with a bordered tail
inverse that is a CONSTANT (2.19 … 10.32). If MM answers NO, that explanation becomes the
lane's epitaph, and an epitaph with no external check is a mood. So check it against the
published record: enumerate the radii-polynomial / Newton–Kantorovich computer-assisted
certificates the repository can actually cite (BDL arXiv:1503.06315 — LIT has already settled
that its assumptions (4)–(5) require a diagonal bounded away from zero; CLN arXiv:2302.12877,
whose Kawahara radius `solver/target_selection.py` already reproduces; Chen–Hou
arXiv:2210.07191 + Part II; Dåhne–Figueras arXiv:2410.05480, re-derived at leg 48), and for
each one classify the unbounded part of the linearised operator (multiplier or shift), the
shape of the approximate inverse (block diagonal or not), and whether the tail inverse decays.
The deliverable is that classification as an EXECUTABLE predicate in the existing CLAIM_LEDGER
style, links not counts, with each classification traced to a located statement in the source
rather than to an abstract page (leg 53 lost a claim exactly there).
**Gate.** Is there a published radii-polynomial certificate whose unbounded part is
OFF-DIAGONAL (a shift) and whose tail inverse does not decay — i.e. a counterexample to the
dichotomy legs 51–53 rest on?
  yes -> The mismatch thesis is refuted as a general claim, and that paper's construction is
         the template to port. Report the located statement and the construction; do not
         claim the port works before anyone runs it.
  no  -> The dichotomy is a real classification, TC/MM's negative generalizes beyond this
         repository, and it is banked as an executable ledger entry with links. Stop
         restating the multiplier/shift explanation without this ledger as its citation.
**Territory.** solver/certificate_shapes.py (new), test_certificate_shapes.py (new),
               solver/literature_gates.py, test_literature_gates.py,
               experiments/p2_route_xs_v1_shapes.py,
               experiments/p2_route_xs_v1_shapes_evidence.py,
               writeup/4_p2_lottery/BLOG_P2_ROUTEXS_V1.md,
               writeup/4_p2_lottery/TECHNICAL_P2_ROUTEXS_V1.md,
               writeup/data/p2_route_xs_v1_shapes.json,
               writeup/figures/fig52_route_xs_v1_shapes.png,
               writeup/novelty/leg_57.md, experiments/journal/leg_57.md
**Difficulty.** light
**Independence.** Literature classification plus an executable ledger; builds no certificate
and computes no `Z₁`. `solver/literature_gates.py` is claimed by nobody else. Its answer is
about OTHER operators, so it neither depends on nor pre-empts MM's result on this one.
```

```
### 58 — ROUTE-WV: THE WEIGHT FITNESS'S WALL IS 2-D, NOT 1-D
**Thesis.** Stage `B` is blocked because C-PILOT's six-property viability gate answered
FAIL 4/6 and PREP's named repairs moved it without passing (P2 0.775 → 0.875 against a 0.90
floor; P3 worst `|slope−1|` 0.366 → 0.342 against 0.05). P2's own gate note records the
suspected cause: the measured wall is a 1-D slice of what is actually a 2-D boundary, so the
fitness is being scored against the wrong geometry. Model the wall in both weight factors,
re-derive the analytic growth rate in that geometry (the 1-D version predicted ×7.39 and
measured ×7.39, so the instrument has a known-answer window), and RE-RUN the frozen
six-property gate unchanged. The gate stays frozen — repairing the fitness is allowed, moving
the goalposts is not. **No GA compute runs on either branch**: that ban lifts only on a gate
that PASSES, and lifting it is the user's call, not this leg's.
**Gate.** With a 2-D wall model, does the FROZEN six-property viability gate pass 6/6 — in
particular P2 ≥ 0.90 and P3 max `|slope−1|` ≤ 0.05?
  yes -> The recorded lift condition for the GA ban is met. Report it, run NO GA compute, and
         escalate to the user (escalation #1: stage `B` entering the committed sequence).
  no  -> Report which properties still fail and by how much. Stage `B`'s fitness is dead as
         parameterized, and the next `B` proposal must change the fitness's definition, not
         its wall model.
**Territory.** solver/weight_search.py, test_weight_search.py,
               experiments/p2_weight_repairs_v2.py, experiments/p2_weight_repairs_v2_evidence.py,
               writeup/4_p2_lottery/TECHNICAL_P2_WEIGHT_REPAIRS_V2.md,
               writeup/4_p2_lottery/BLOG_P2_WEIGHT_REPAIRS_V2.md,
               writeup/data/p2_weight_repairs_v2.json, writeup/novelty/leg_58.md,
               experiments/journal/leg_58.md
**Difficulty.** standard
**Independence.** `solver/weight_search.py` is claimed by no live leg. Touches no certificate
term and no literature ledger. Ranked below 55–57 because it cannot move a link of the chain —
it unblocks a stage, which is not the same thing.
```

```
### 59 — ROUTE-PQ: THE TWO NEGATIVE FINDINGS THAT HAVE NO QUARTET
**Thesis.** DOCS flagged that Route-PORT v1 and v2 each have a runner and curated data but no
`*_evidence.py` and no registered figure. Both carry load-bearing negative findings — the
certificate closes around the WRONG truncated object (leg 46: the true object is 1.55e+08 ball
radii outside it), and extending reach makes the truncation gap WORSE (leg 47: +0.47 decades
per unit `ρ`, the wrong sign) — and both are cited as settled in the ban list. Writing their
evidence scripts is not bookkeeping: it re-derives the quoted numbers from the stored data,
which is a reproduction check that can FAIL, and two of this repository's last three
discrepancies (REPRO's 50/50 claim, leg 53's `K` vs `K²`) were exactly this kind.
**Gate.** Do the evidence scripts re-derive every number Route-PORT v1's and v2's prose quotes,
from the stored curated data, to the precision the prose states?
  yes -> Both quartets close; the two bans that cite them keep their evidence.
  no  -> A banked negative finding is not reproducible from its own data. Park it, do NOT edit
         the prose to match, and escalate — a ban resting on an unreproducible number is the
         user's call.
**Territory.** experiments/p2_route_port_v1_bordered_evidence.py,
               experiments/p2_route_port_v2_reach_evidence.py,
               writeup/figures/fig53_route_port_v1.png, writeup/figures/fig54_route_port_v2.png,
               writeup/README.md, writeup/novelty/leg_59.md, experiments/journal/leg_59.md
**Difficulty.** light
**Independence.** Touches no solver module and recomputes no new number. Does not overlap
54–58. Ranked here because it cannot move the chain, only audit it.
```

```
### 60 — ROUTE-KA: A KNOWN-ANSWER WINDOW FOR THE WHOLE INTERVAL PIPELINE
**Thesis.** Read the `validated` column of `capabilities.py` for the certificate stack: nearly
every entry is validated INTERNALLY (enclosures contain exact rationals, rigorous bounds
dominate float readings, a poisoned iterate is rejected). What the stack has never done is
reproduce a PUBLISHED certified radius end to end. `solver/target_selection.py` reproduces
CLN's Kawahara radius, but as a transcribed number in a ledger, not as output of
`solver/interval_certificate.py`. Point the actual pipeline at Kawahara and see whether it
lands inside CLN's published interval. Lesson 84: a known-answer probe has a WINDOW, so the
window is pre-committed — the published radius interval, at their stated truncation.
**Gate.** Does `solver/interval_certificate.py`, run end to end on the Kawahara problem,
produce a certified radius inside CLN's published interval at their truncation?
  yes -> The stack has its first end-to-end published known-answer gate. Bank it as an
         executable test, and every future negative from this pipeline cites it.
  no  -> The pipeline disagrees with a published certificate. That is a bug hunt, and it takes
         priority over every route in this queue including the critical path, because every
         banked interval result depends on it.
**Territory.** solver/interval_certificate.py, test_interval_certificate.py,
               experiments/p2_route_ka_v1_kawahara.py, writeup/data/p2_route_ka_v1_kawahara.json,
               writeup/novelty/leg_60.md, experiments/journal/leg_60.md
**Difficulty.** standard
**Independence.** NOT independent of item 56 — both own `solver/interval_certificate.py`. They
must not run concurrently. That collision is the only reason this sits at #7 rather than #4;
its no-branch is the highest-consequence branch in the queue.
```

## Ranking rationale

Refreshed whenever a gate answers. Rank by, in order:

1. could this leg actually move a link of the L1→L4 chain;
2. can its gate answer either way within one leg's work;
3. is it independent of the other three live legs.

**Refreshed 2026-08-05, after `TC`'s gate answered NO.**

**54 (MM) is first because the plan says so** — it is the stage marked `NEXT`, and it is the
only remaining free choice in a lane where the other four (`s`, weight family, split `K`,
border direction) are all measured and banned. Criterion (2) is unusually strong here: leg 53
left a number, 0.9961, on the finite-block-independent sub-block, which is *below 1* — so the
gate is not decorative, it can genuinely come out either way. Criterion (1) is honest and
weak: `L1` is the only movable link and MM is work on it, but nothing has moved in 53 legs.

**55 (NB) is second because it is the cheapest test of the clause the whole lane's future
rests on.** Every number in legs 51–53 is measured on a substrate the ceiling explicitly says
is not the target, and one of the two stated reasons — that the target has no finite norm in
the admissible class — appears never to have been measured. If it is false, the ban list needs
correcting. If it is true, MM's yes-branch promises a re-run that cannot happen, and knowing
that BEFORE MM reports changes what the yes-branch is worth. It is a norm of a profile, not a
certificate, so it clears the machinery ban cleanly and answers in one leg.

**56 (TN) is third because it is the other named gap of the same link, in a different basis.**
`L1` step one has exactly two things standing between it and `L1`, and legs 51–53 spent
themselves on one of them. If MM answers NO, the coefficient basis is done and this branch is
the only place `L1` can still live — so measuring its gap now is worth more than measuring it
after. It ranks below 55 only on criterion (2): enclosing an operator consistency defect
rigorously is heavy work with a real chance of landing on "the bound is true and useless,"
which is Route-D v6's own recorded trap.

**57 (XS) is fourth because it is the external check on the explanation, and it is light.** It
cannot move the chain. What it can do is stop the multiplier/shift dichotomy from becoming an
unaudited house belief right at the moment the repository is about to close a lane on it.
Cheap, independent, both branches consequential, and it repairs leg 53's specific failure mode
(a literature claim logged as counts, unauditable, withdrawn).

**58 (WV) is fifth, and it is deliberately not in a slot.** It unblocks stage `B`, which is not
the same as moving a link, and its yes-branch ends in an escalation rather than in work. It
also inherits a warning: leg 53 measured the operator split — one of `B`'s three degrees of
freedom — to be worthless as a dial.

**59 (PQ) and 60 (KA) are audit legs.** PQ is last on consequence; KA would rank fourth on
consequence alone (its no-branch invalidates every banked interval result) but collides with
56 on `solver/interval_certificate.py`, and criterion (3) is a ranking criterion, not a
tiebreak. If 56 is pulled for open question #1, promote 60 into slot C ahead of 58.

**Ordering the queue by proximity to the Clay chain is a choice of what to try. It is never a
claim that anything moved.** In 53 legs, no link has moved; Clay stays at ~0.05% behind Walls 1
and 2.

## Open direction questions for the user

These also appear under `⚠ NEEDS YOU` in `PROGRESS.md`. The run continues around them.

1. **Does the standing ban "no further `ℓ¹`-Fourier radii-polynomial machinery for this
   operator before MM's gate answers" cover the interval/collocation branch too?** The DM reads
   it narrowly — it names `ℓ¹`-Fourier explicitly, and leg 56 (Route-TN) is sup-norm collocation
   on a different object (`HL_S2_nonsymmetric`, not the `a = 0` CLM anchor). If you read it
   broadly, pull leg 56 and promote item 60 (Route-KA) into slot C. **The DM does not decide
   this; the leg is dispatched on the narrow reading and can be pulled before it merges.**

2. **If leg 55 finds the target DOES have finite norm in an admissible class, a live ban's text
   is factually wrong.** The ban asserts `HL_S2_nonsymmetric` "does not have finite norm in the
   class where the operator is least bad." Bans are lifted only by their own recorded
   conditions and amended only by you — so leg 55's yes-branch parks and escalates rather than
   editing anything.

3. **What is the fallback if MM answers NO?** The committed sequence has exactly one stage left
   after `MM`, namely `B`, and `B` is blocked by a fitness gate that has failed twice (4/6, then
   4/6 again after two named repairs). If MM answers NO and item 58 also fails, the plan has no
   live stage. Worth deciding now, rather than at the moment it happens, whether the fallback is
   `B` with a hand-designed space and no GA, or a fresh target-selection round (a second `M`)
   aimed at a different model. Either is escalation #1.
