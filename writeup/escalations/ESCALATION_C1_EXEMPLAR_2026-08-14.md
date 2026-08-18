# ESCALATION — C1's EXEMPLAR HAS FALLEN

**Raised:** 2026-08-14, by the Conductor, on the return of leg 393 / `T4` (landed `2c87244`).
**Class:** §8. **A ruling was made on a packet carrying a factual error, and the error is now measured.**
**Status:** ~~OPEN — awaiting the user.~~ **DISCHARGED 2026-08-14.** All three questions below were
ruled by the user on 2026-08-14. The authoritative ruling record is
**`writeup/escalations/RULING_C1_EXEMPLAR_2026-08-14.md`**; this document is retained unchanged
below as the packet that was ruled on. **Work never stopped**; see §6.

> **THE RULINGS, IN ONE LINE EACH** (full text and reasoning in the ruling document):
> **(1) C1 needs NO replacement exemplar — it is an APPARATUS SCOPING and stands EXEMPLAR-FREE**,
> with the scope explicitly no longer carrying any implied *"and this has been demonstrated"*: no
> unit may cite C1 as evidence the technology closes for any object class. C1's **naming
> requirement is unchanged and binds every unit.**
> **(2) Lane T's priority-1 ranking does NOT survive — Lane T is DEMOTED to DEFERRED**, kept alive
> only through **`T2″`**, with two re-open conditions recorded in `OPTIONS.md`. Nothing measured is
> superseded: the domain-shape obstruction is still not refuted, Theorem NGX / leg 341 / the three
> dead realizations stand, W2 stands strengthened, and `T3` is deferred rather than killed.
> **(3) The packet's defect was material to the RANKING, not to the SCOPING** — C1 needs no
> re-ruling and its transcription in `plan_of_record.py` stands byte-unchanged; A2, B1 and the
> narrowed outreach hold are untouched.
> **DIRECTION: the programme's priority lanes are now V and L.** **No ban is lifted, narrowed or
> reworded**; 26 recorded / 19 in force, unchanged.

---

## 1. The one-sentence version

On 2026-08-13 you ruled **C1**, scoping the ℓ¹-Fourier / radii-polynomial ban to an **apparatus**
and thereby unblocking Lane T. The paper the whole lane was built around — `arXiv:1902.00384`,
recorded as *the crack in W2* — has now been read at full text and **is certified by exactly the
banned apparatus**, and **both of its certified rows are 2D lifts**. C1's *general proposition*
survives untouched. Its *exemplar* does not.

## 2. What was measured, and how hard the evidence is

Leg 393 was dispatched to reproduce a published enclosure row. Its brief carried your binding
requirement — name the apparatus, and show it does not construct a single bounded approximate
inverse uniform in `M` — and a pre-committed instruction that **if the apparatus turned out to
require one, the unit should STOP and say so, because that would be more valuable than the
reproduction.** That branch fired.

**(a) The apparatus is the banned one.** A Newton–Kantorovich radii-polynomial contraction
(Thm 2.15, (2.17)–(2.21); symmetry-reduced Thm 4.23, (4.28)–(4.32)) in a weighted `ℓ¹_η` Fourier
space, built on **one bounded approximate inverse** `A : X_{−2,−1} → X` (§2.3): the numerical inverse
of the finite block plus the exact diagonal off it — one operator acting on the whole
infinite-dimensional space. Term counts in the full text: *approximate inverse* ×7,
*Newton-Kantorovich* ×4, *interval arithmetic* ×5, INTLAB ×2.

**This is visible in the abstract.** The Conductor confirmed it independently of the worker, from
the arXiv abstract page: *"a Newton-Kantorovich theorem is applied to obtain the (computer-assisted)
proofs of existence"*, posed on *"a Banach space of geometrically decaying Fourier coefficients."*
Leg 348 classified this paper **at abstract level** — the disqualifying sentence was in the text it
read.

**(b) Both certified rows are 2D lifts.** From the authors' own published data package, not prose:
`N_x3 = 0` in Table 1 and in `Nrec`; decoded coefficient arrays have **extent 1** in `x₃`;
`max|u⁽³⁾| = max|ω⁽¹⁾| = max|ω⁽²⁾| = 0.0` **exactly**, while `max|ω⁽³⁾| = 1.6351 / 1.5274` — so the
zeros are structure, not an empty array; the `setup` field reads `'2D'`. The authors state the
reason: the memory cost of a three-dimensional solution is *"for now, prohibitive."*

**W2's own pre-committed test requires showing the certified object is not a lift of a
lower-dimensional one. It is one.** W2 stands, strengthened.

**(c) The negative control could have fired and did not.** *self-consistent*, *a priori bounds*,
*isolating*, *trapping region*, *logarithmic norm*, *dynamical closure*: **all zero**. Zgliczyński
appears once, as bibliography item [48]. Had any of these fired, C1's scope would have covered the
reproduction and the unit would have proceeded into it.

**Audit.** The pre-registration landed **before any computation** and already contained the verdict
rules and six two-sided controls, with `STOP` written down in advance — it was not constructed after
the answer was seen. The evidence script was re-run by the Conductor from the branch: **exit 0,
68/68**. The 2D shape was visible in Table 1 at pre-registration time, so nothing here is post-hoc.

## 3. What falls, and what explicitly does not

**FALLS.** Leg 348's classification of `1902.00384`. The claim in `WALLS.md` that W2 has a crack.
The claim that "the technology clears W2's bar already, and only the target is missing." Item 3 of
the four-results argument that Lane T is priority 1. All are corrected in this commit, with the
superseded wording kept inline and struck.

**DOES NOT FALL — and the Conductor is not entitled to rule otherwise:**
- **C1's general proposition.** A Zgliczyński-style Galerkin-plus-tail dynamical closure remains a
  different apparatus from a radii-polynomial contraction. Nothing measured here bears on that.
- **Your ruling that Lane T is unblocked by scope.** That is a ruling. A measurement supersedes a
  ban; it does not silently reverse a scoping.
- **Theorem NGX, leg 341, and the three dead realizations.** Untouched, as C1 itself said.
- **`T4`'s own numerical work.** The gate's *first* conjunct was met on both rows — criterion (4.32)
  verified, `r_min`/`r_max` relative deviations down to `5.6e-15`, both `r_sol^Ω` exact, an
  independent norm check at `δ = 5.3e-06` against a `1e-3` threshold. The *second* conjunct — a
  C1-compliant apparatus — cannot be met by anything that actually certifies those rows.

## 4. Why this is escalated rather than decided

The standing instruction is explicit: **ruling any ban-wording question is prohibited to the
Conductor; escalate.** Three questions here are yours and not mine:

1. **Does C1 need a replacement exemplar, or none at all?** C1's proposition can be true with no
   instance in the literature. If it has no instance, Lane T's practical content is thinner than the
   lane was ranked on — the ban would be scoped around an apparatus nobody has yet used for this
   class of object.
2. **Does Lane T's priority-1 ranking survive the loss of item 3?** The remaining three results still
   argue for it; the strongest of them argued that the technology was *demonstrated*. It is not.
3. **Was the escalation packet's defect material to C1?** `T1` posed the questions and, correctly,
   ruled none of them — but it inherited leg 348's classification. You ruled on a packet carrying it.

## 5. The process finding, which is the more general one

**Leg 348's ceiling was known, declared, and not discharged for a full lane's worth of work.** Leg
348 said in its own words that a full-text pass could strengthen *or undercut* its classification.
That flag sat in the record while `WALLS.md`, `CLAY_ROADMAP.md`, the lane ranking and an escalation
packet were all built on the un-discharged classification. You ordered `T6` to discharge it and said
to run it **early, precisely because it can undercut the lane**. That instruction was correct and it
is the reason this was caught within one wave.

**The narrower lesson: an abstract-level classification is load-bearing evidence or it is not, and
this programme treated one as load-bearing for 45 legs.** The disqualifying sentence was in the
abstract the whole time — this was not even a full-text-only finding on the apparatus question.

## 6. Work has not stopped

**UPDATE, same day — `T6` HAS RETURNED, AND IT REPLICATED THE FINDING INDEPENDENTLY** (landed
`e7db624`). It was never told what `T4` found. It reached the same conclusion by a **different
method** — reading the authors' prose, where `T4` reproduced from their published data package — and
it has the sentence outright:

> *"While all of the analysis is performed in full generality on the 3-torus, the solutions we
> present in Theorem 1.1 below are two-dimensional (in space) time-periodic solutions"* … *"they are
> independent of `x₃` and the third component of the velocity vanishes."* — §1, p.3

**Verified by the Conductor directly against the PDF, in both workers' separately fetched copies**
(lines 118 and 132). Two independent fetches, two independent methods, one conclusion. **This is no
longer a judgement call.** `T6` independently confirms the apparatus finding too: Theorem 2.15 (p.13)
is literally a `Y₀/Z₀/Z₁/Z₂` radii-polynomial contraction with a bounded approximate inverse.

**`T6` also found a second, separate undercut** you should know about when ruling: `arXiv:2409.09234`
does not belong in leg 348's `domain_census` at all — 1-D map fitted to DNS data, no-slip walls, not
periodicity — so **the census over-counts by one and leg 390's "6 compact/periodic" figure inherits
the error.** `WALLS.md` carries the flag.

**And what survives, stated plainly: the obstruction leg 348 named is NOT refuted.** No
counter-instance appeared at full text either. **Its evidence base is thinner than the record said,
not wrong.**

`T5` has also returned (landed `a6f0c38`) and bears on question 1 below: C1's sweep found **two**
re-openable refusals, and the genuinely new one — leg 315's Taylor-model flow-map build — points at
**Lane V's direction, not Lane T's.**

**`E` has since returned and landed (`d0d72b1`), and it is unaffected by any of this** — it is Lane
R, it touches no ban and no wall on the Clay chain. Recorded here only so the desk sees the board is
not idle while these three questions wait: its gate PASSED, and its diagnostic (3) — the sharpest
test of H-hard available, seeding all eight named rows at their own published coordinates —
**recovered none of them, 0 of 16, with a positive control proving the predicate can return a
recovery.** **Wave 1 is now complete.** Tier 2; no `L1→L4` link moved; **Clay stays ~0.05%.**

**What the Conductor has done without a ruling:** corrected the factual claims in `WALLS.md`,
recorded the retraction, and left every scoping question open. **What the Conductor has not done:**
re-ranked Lane T, named a replacement exemplar, or touched C1's transcription in `plan_of_record.py`.
