# RULING — the ban-wording escalation of 2026-08-13

**The user ruled on 2026-08-13**, on the packet at `ESCALATION_BAN_WORDING_2026-08-13.md` (leg 391 /
`T1`, gate `yes`). This document is the authoritative record of the ruling. **It is transcription
work for the Conductor, not interpretation** — the exact wording each ban must carry is given below,
and `plan_of_record.py` is to be edited to match it verbatim.

**`plan_of_record.py` was deliberately NOT edited by the session recording this ruling.** It is the
Conductor's file under `ORCHESTRATION.md` §3g, it is executable, and `test_plan_of_record.py`
cross-checks it against `CONTINUATION_PROMPT.md` and `CLAY_ROADMAP.md`. The Conductor applies these
four items in **one commit per item**, so each diff is legible on its own.

---

## (c) THE APPARATUS QUESTION — **RULED C1. This is a SCOPE ruling, not a lift.**

> **The ℓ¹-Fourier / radii-polynomial ban names an APPARATUS.** A Zgliczyński-style
> Galerkin-plus-tail **dynamical closure** — self-consistent a-priori bounds, in which a finite
> Galerkin block and a controlled tail close a *dynamical* invariance argument rather than a
> Newton–Kantorovich contraction in a function space — **is a different apparatus and is outside the
> ban's object.**

**What does NOT change, and it is most of it.** The ban **stands in full** for the machinery it
names. The three dead realizations stay dead: ℓ¹_w coefficient basis (leg 54), collocation (leg 56),
origin-`H²`/Mellin (legs 163/176). **Theorem NGX stays true** — `Z₁ ≥ 1` for every bounded `A`,
`σ_min(L_M) = c_s M^{−(1−s)} → 0`. Leg 341's three-lane death of the algebraically weighted space
stays true. **No measurement is superseded by this ruling, which is the test §3h rule 1 sets.**

**The evidence the ruling rests on**, recorded so the ruling can be audited rather than trusted:
the ban's subject noun is *"machinery"* qualified by an apparatus name; its generality clause is a
**model** clause (*"on ANY model, fluid or otherwise"*) and is silent on apparatus; NGX states its
own exclusion in apparatus terms — *"what Theorem NGX excludes is a **single bounded `A` working
uniformly in `M`**, which is the only sense the radii-polynomial method has"*; and leg 348, which
was **not** trying to open a lane, already recorded leg 341's death as *"suggestive but not direct …
different apparatus (NK fixed-point contraction vs. Galerkin-tail dynamical closure)"*.

### THE NAMING REQUIREMENT — this scope is claimed per unit, exactly as the DSS precedent requires

**Any unit claiming this scope MUST, in its own pre-registration, BOTH:**

1. **NAME ITS APPARATUS** — the closure it uses, with a citation, and
2. **SHOW IT DOES NOT CONSTRUCT A SINGLE BOUNDED APPROXIMATE INVERSE UNIFORM IN `M`** — which is
   the precise quantity NGX excludes and therefore the precise thing that puts a unit inside or
   outside the ban.

**ABSENT BOTH, THIS BAN APPLIES IN FULL.** A unit that reaches for a `Y₀/Z₀/Z₁/Z₂` contraction, in
any space, is inside the ban whatever it calls itself.

### The lift clause is untouched, and remains defective for space-based candidates

The clause still reads *"unless a namable **FOURTH space/basis** … is proposed"*. Under C1 that
mismatch is **moot for Lane T**, which holds a fourth *apparatus* and needs no lift. **It is not
repaired**, and it still names the wrong kind of object for any future candidate that *is* a space.
Recorded as a known live defect; not ruled here because nothing currently depends on it.

### THE OBLIGATION THIS RULING CREATES — do not skip it

**C1 means this ban is narrower than the repository has been treating it.** That cuts both ways, and
the second way has never been checked: **work may have been declined, deferred or never proposed on
a reading of this ban that the ruling now says was too wide.** A sweep is owed — grep the landed
record for legs that cite this ban as a reason not to proceed, and report which of them were
apparatus-based refusals that C1 would now permit. **This is an obligation of the ruling, not an
optional follow-up**, and it is the honest price of narrowing a ban.

---

## (a) CADIOT — **RULED A2. THE BAN STANDS.**

> Leg 304 resolved the open question and the resolution **confirmed** the ban's justification:
> Cadiot's Assumption 1 requires `|l(ξ)| ≥ l_min > 0`, `L` is a Fourier multiplier by the class
> definition, so `l` **is** the diagonal and a vanishing diagonal is **excluded by hypothesis**, not
> by accident. Lifting a ban because its own justification was validated inverts §3h rule 1.

**Required edit.** The lift clause currently reads as an open invitation — *"unless a pass resolves
whether Cadiot's construction covers a zero diagonal"* — and a pass **has** resolved it. The clause
is **CLOSED**, and must say so rather than continuing to read as a live path:

> *lifted by:* **never — the lift condition's pass HAS RUN (leg 304, Route-CADX, gate YES(i),
> landed `b319449`) and RESOLVED THE QUESTION AGAINST LIFTING: Cadiot does not cover a zero
> diagonal, and the exclusion is BY HYPOTHESIS (Assumption 1, p.6). RULED A2 by the user
> 2026-08-13: the clause is CLOSED, not open. The 2026-08-11 escalation is DISCHARGED.**

**Note for the Conductor:** the existing entry already carries the full leg-304 annotation and the
words *"THE BAN IS NOT LIFTED AND THIS ANNOTATION DOES NOT LIFT IT"*. Keep all of it. This edit only
converts the trailing "ESCALATED TO THE USER … and pending" into the ruling's outcome.

---

## (b) STAGE V'S "NEEDS L1 FIRST" — **RULED B1. THE DEFECT IS EDITORIAL.**

> The 2026-08-06 ban review's re-posed entry says *"this retires the prior 'needs L1 first'
> wording"*. The only text that has ever carried that wording is the **V-as-posed** lift clause. The
> retirement was declared in the new entry's prose and **never applied to the old entry's field**.
> This is a bookkeeping failure, not a substantive block.

**Required edit — the V-as-posed lift clause loses its stale precondition:**

> *lifted by:* **never — unless the question is re-posed for a FLUID transport model.
> ("which needs L1 first" STRUCK 2026-08-13, user ruling B1: the 2026-08-06 ban review retired that
> wording in the re-posed entry's own prose and never applied it to this field. The retirement is an
> editorial correction, not a new decision, and the ban's own justification — the novelty gate of
> 2026-08-04 on arXiv:2410.05480, re-derived by leg 48 — is untouched.)**

**Record alongside it, because the packet surfaced it and it is a real inconsistency:**
`plan_of_record.py`'s `SEQUENCE` marks **`L1` complete** while the ban review describes L1 as dead in
three realizations. Both are true of different things — the stage's completion marker versus its
three realizations — and the file should not read as though they conflict. **Add a clarifying note;
do not change the `[x]`.**

### THE COMPOUND CONSEQUENCE, WHICH NEITHER ITEM CARRIES ALONE

**(b) and (c) together open Lane V, and this was not the stated purpose of either.** Stated
explicitly so it is a decision on the record rather than a side effect nobody noticed:

- **B1** means stage V's question may be re-posed for a **fluid transport model** without an L1
  precondition.
- **C1** means a **Galerkin-plus-tail apparatus** is outside the ℓ¹-Fourier/radii-polynomial ban
  that would otherwise bite whatever model was chosen.

So **a fluid transport target attacked with a dynamical closure is now outside both bans** — subject
in full to (c)'s naming requirement above. **`OPTIONS.md` §C's Lane V is therefore no longer blocked
on a ruling in either half**, and its "name the target" half was never blocked at all. It stays
**deferred** under the user's Lane T priority, and the Conductor records it as *deferred by
priority*, not as *blocked*.

---

## (d) THE OUTREACH HOLD — **NARROWED. Published material may be read; author contact stays held.**

> **The hold is on contacting people, not on reading.** Reading any published document — papers,
> problem statements, proceedings, theses, publisher pages, full texts — **is authorised and
> encouraged**. Contacting an author, a group, a maintainer or a mailing list **remains held** and
> needs its own ruling.

**Immediate consequences:**

1. **Fefferman's official Clay problem description may be fetched and statement (D)'s data
   conditions (8) and (9) read verbatim.** `CLAY_OBLIGATIONS.md`'s *"(D) carries no decay
   condition"* is currently **narrowed to (D)'s solution conditions** pending exactly this. Leg 390
   §5 item 1 owes the re-run of `check_A` against them, and **the §4 disposition may change** if
   either condition carries a data-side decay or regularity requirement.
2. **`T2′`, the compliant rigidity search, gains full-text access** — the forward-citation pass on
   NRS 1996 (Acta Math.) and Tsai 1998 (ARMA) no longer depends on abstracts alone.
3. **Leg 348's own recorded ceiling can be discharged** — it read seven papers *at abstract level
   only* and flagged that a full-text pass could strengthen or undercut its classification. Lane T
   rests on that classification, so this is worth doing early.

**No S2 API key is available** (user, 2026-08-13). Semantic Scholar's unauthenticated endpoint is
rate-limited but usable: **pace and back off rather than assuming a key**, and continue to bank a
throttled query as `THROTTLED`, never as a zero — leg 392's instrument discipline stands unchanged,
and leg 387's namespace failure (arXiv serves `1.1`; the harness listed `1.0`) must not recur.

---

## Summary table for the Conductor

| item | ruling | effect | who applies |
|---|---|---|---|
| **(c)** | **C1 — apparatus** | **LANE T UNBLOCKS BY SCOPE.** `T3`, `T4` open. Naming requirement binds every unit. Sweep obligation owed. | Conductor → `plan_of_record.py` |
| **(a)** | **A2 — ban stands** | Cadiot ban unchanged; lift clause marked **CLOSED**; 2026-08-11 escalation **DISCHARGED**. | Conductor → `plan_of_record.py` |
| **(b)** | **B1 — editorial** | *"which needs L1 first"* **STRUCK**. With (c), Lane V is deferred by priority, **not blocked**. | Conductor → `plan_of_record.py` |
| **(d)** | **narrowed** | Published material readable. Author contact still held. (D)'s (8),(9) now readable. | Conductor → `STATE.md`, `WALLS.md`, `CLAY_OBLIGATIONS.md` |

**Unchanged by all four:** the three-tier win condition (**Tier 2 is never a proof**), pre-committed
gates, the novelty pass, lesson 91, planted controls, `merge_gate.sh`, §3d's `UNDER-RESOURCED`, and
**no output described as movement toward Clay unless a link of the `L1 → L4` chain actually moved.
Ceiling TIER 2. Clay stays ~0.05%.** Nothing in this ruling moved a link; it moved permissions.
