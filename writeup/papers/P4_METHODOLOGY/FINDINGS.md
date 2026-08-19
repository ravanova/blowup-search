# `P4_METHODOLOGY` — FINDINGS ABOUT THE RECORD (leg 414, unit `P4-DRAFT`, wave 9)

This is `P4-DRAFT`'s **SECOND output**. The first is `DRAFT.md`. Everything here surfaced *while
drafting the paper* and is about **our own record**, not about the literature. Per the brief it is
**NEVER SMOOTHED OVER IN PROSE**: written at full strength, routed, and left for the Conductor.
**NOTHING BELOW HAS BEEN APPLIED BY THIS UNIT.** `writeup/CORRECTIONS.md`, `STATE.md`, `WALLS.md`,
`OPTIONS.md`, `writeup/waves/**`, `reports/` and every sibling unit's files were not touched.

**The brief asked me to say whether the findings outweigh the draft. THEY DO — and the reason is
specific rather than modest.** The draft is a re-presentation of things the record already knows.
`F2` and `F3` below are not: they say that the discipline's single most expensive miss (§51) has a
**second half that is not in the record at all**, and that the counter-evidence to a banked verdict
was sitting **inside the same JSON object as the verdict**, unread by any check for eleven legs.
`F1` says the measurement on which this paper's own central thesis rests cannot be re-derived from
the record. A paper that reports those three is worth less than the three.

**Method note.** Every number below was re-derived from a primary artefact by this unit at leg 414;
the derivations are tabulated in `experiments/journal/leg_414.md` §2. Nothing here is copied from
prose that reports it.

---

## F1 — `32 of 49` HAS NO BANKED ARTEFACT. This paper's own thesis rests on an unbankable number.

`CORRECTIONS.md` §45's headline — *32 of 49 evidence scripts reference no file outside their own
unit's artefact* — appears in exactly four places: `CORRECTIONS.md` §45 (twice), this paper's
`STATUS.md` (twice), `CORRECTIONS.md` §51's cross-reference, and the docstring of
`experiments/p2_verify_wave7_v1_evidence.py`. **It appears nowhere in `writeup/data/`.**

There is no banked classifier, no file list, no per-script classification, and therefore no way for
a reader — or for a later unit, or for me — to re-derive it or to re-run it as scripts land. Under
the rule that governs this paper (*every number cites the banked JSON field it came from*), **`32
of 49` does not qualify.** It is labelled `UNBANKED` at every appearance in `DRAFT.md`, including
in the abstract.

**In fairness to §45, which the draft also records:** §45 states that its classifier was
*"validated by hand on three scripts before the number was believed"* (`t4`, `l6b`, `ng`), which is
more discipline than most numbers get. That mitigates the risk that the number is wrong. **It does
not make the number re-derivable**, and re-derivability is the property the rule is about.

**My attempted re-measurement, reported with the same caution I am applying to the original.** At
leg 414 the repository holds **53** `*_evidence.py` scripts, not 49 — four landed after §45 was
taken, so the denominator has moved. Under a *cruder* classifier written for this draft (any string
literal naming a file other than the script's own artefact counts as an outside reference — which
**over-counts** independence, because it also catches `.md` and `.py` mentions), the split is **27
solo / 26 independent, 51% solo**.

> **I do NOT claim 51% supersedes 65%.** Different classifier, different date, and mine is the
> weaker instrument. The claim is narrower: **the headline is not currently reproducible from the
> record.** A measurement that cannot be re-derived is in the same epistemic position as the `N/N
> passed` lines it was written to criticise.

**Routing: `CORRECTIONS.md`, and a cheap unit — bank the classifier and its per-script output as
`writeup/data/`, so the number is re-derivable and re-runnable as scripts land. Until then §45's
figure should carry `UNBANKED` wherever it is quoted.**

---

## F2 — §51's ACCOUNT IS INCOMPLETE IN THE DIRECTION THAT FLATTERS THE DISCIPLINE: a control WAS planted, and it did not fire as planted.

**This is the most consequential finding of the leg.**

§51 records the under-claim as *"nobody divided one by the other"*. That is true of the division.
**It is not true that nobody planted a control against the budget hypothesis.** The same artefact,
`writeup/data/p2_route_l6_profile_v1.json`, banks
`gate.B.stability_against_the_iteration_cap` — a sweep over caps `50 / 100 / 200 / 400 / 800`, all
five rows returning `decreases_under_refinement = "NO"`, the block verdict field reading
`verdict_is_stable_in_the_cap: true`, and the rationale field `why` reading:

> *"if the verdict is the same at every iteration cap, it is a fact about the construction and not
> about where the optimiser stopped"*

**That is exactly the right idea, and the control was structurally incapable of testing it.**
`CORRECTIONS.md` §38 (`V-W6`) already establishes why: the `by_cap` table is a **post-hoc
truncation of the same 800-iteration runs** (the minimum over recorded trajectory points with
`k ≤ K`), and each rung's continuation was warm-started from the previous rung's **full-budget**
minimiser, so every truncated column still carries the full budget from the rung below — `J1` reads
`3.2798` at "cap 50" while `J0`'s own genuine cap-50 value is `14.0239`. It controls nothing about
budgets above 800. `D-VW6-10` further records that **no evidence check touches the block at all.**

**What is new here is the joining of §38 to §51, which no document in the record performs.** The
numbers show how completely the control misled:

| | |
|---|---|
| `J4` at cap 50 → cap 800 (16× budget) | `1.6202442460112116 → 1.6138112319953968` = **`−0.397040%`** |
| `J4` at cap 800 → 20,000 (next 25×) | `1.613811231995397 → 1.504851895102804` = **`−6.751678%`** |

(Both `RECOMPUTED@414` from `…by_cap."50".per_rung_residual[4]` (the block stores the rungs as an ordered list, not a dict), `…gate.B.per_rung_residual.J4`, and
`p2_route_l6b_v1.json → gate.smallest_residual_at_20000`.)

The cap response is radically non-linear and the sampled range sat entirely inside a **false
plateau**: a 16× budget range moved the objective by 0.4%, and the *next* 25× moved it by 6.8%.

**The consequence that must reach `CORRECTIONS.md` in these words:** an `UNDER-RESOURCED`
measurement — a cap sweep whose range was, we now know, three-fold too narrow *and* whose
construction made it not a budget control at all — **was written into the record as a null result**,
in a banked boolean field, `verdict_is_stable_in_the_cap: true`. This programme has a written rule
that `UNDER-RESOURCED` is never a `NO`. **The rule did not prevent its own most expensive
instance**, and the reason is structural: **the rule governs the verdict a unit declares on its
gate; it says nothing about a control a unit passes.** A passed control is the most authoritative
object in the record and the least examined.

**A planted control that cannot fail is worse than no control**, because the discipline then
reports a *passed* control and everyone downstream — the next unit, the integrating Conductor, and
the first verifier — stops asking.

**Routing: `CORRECTIONS.md` — an amendment to §51 recording that a control existed and did not fire
as planted, cross-referenced to §38; plus a rule extension: `UNDER-RESOURCED is never a NO` must be
extended from declared verdicts to PASSED CONTROLS. Before banking a passed control, state what
result would have failed it and show the experiment could have produced that result.**

---

## F3 — THE COUNTER-EVIDENCE WAS INSIDE THE SAME JSON OBJECT AS THE VERDICT, AND NO CHECK READ IT.

Independently of F2's structural defect, the `by_cap` block **banks a field whose own trend
contradicts the verdict field four lines above it.**

`gate.B.stability_against_the_iteration_cap.by_cap.<K>.rate_dlogresid_dlogndof_last3`, as `K` rises
50 → 100 → 200 → 400 → 800:

| cap | rate |
|---|---|
| 50 | `−0.03258476875087628` |
| 100 | `−0.031298503419278374` |
| 200 | `−0.029580697900559467` |
| 400 | `−0.026669284557046716` |
| 800 | `−0.02224154647340172` |

**Monotonically shrinking in the budget — by 31.7% over the range measured** (`RECOMPUTED@414`).
The convergence rate the gate is about is *itself a function of the cap*, and it is moving steadily
in the direction that says the sweep has not reached the regime it claims to certify. The verdict
field beside it reads `true`.

**This is not a subtle inference.** It is five numbers in one array, in the same object, under the
same key, and **it went unread for eleven legs** — by the unit, by the wave's evidence script (which
does not open the block), by the integrating Conductor and by `V-W6`, which found the block's
warm-start defect (§38) and did not read the trend inside it.

**The generalisation, which is the transferable part:** we routinely check that a claim matches its
artefact. **We do not check a verdict field against the other fields of its own object.** That is a
cheap, mechanisable check — for every banked boolean verdict, list the sibling fields and ask which
of them would embarrass it — and no instrument in this programme performs it.

**Routing: `CORRECTIONS.md` as a NEW instrument rule (verdict-vs-siblings), and as an amendment to
§51/§38 recording that the trend field existed and was never read.**

---

## F4 — `nq_r` PER RUNG IS NOT A BANKED FIELD, so §53's reach argument is derivable only from source code.

§53's per-rung radial reach — `nq_r` = 36, 48, 48, 60, 72 for `J0…J4` — appears in the record as
prose. It is **not a field in `p2_route_l6_profile_v1.json`.** It is derivable only by reading
`experiments/p2_route_l6_v1.py:188`:

```
self.nq_r = nq_r if nq_r is not None else 3 * Nr + 12
```

against the rung table's `Nr` = 8, 12, 12, 16, 20 (`RECOMPUTED@414`). Reading source to recover a
parameter of a banked result is exactly the *recompute-from-primary* discipline §45 asks for, so
this is not a defect of anyone's method — **but a load-bearing quantity that lives only in a default
argument expression is one refactor away from silently invalidating every downstream statement about
reach, and nothing would flag it.** The `L6-e` v2 gate (§53) is specified in terms of `nq_r = 60`
and `nq_r = 72`; if those defaults change, the gate text still reads correctly and means something
else.

**Routing: `CORRECTIONS.md` (artefact-schema debt) — the run configuration actually used per rung,
including `nq_r`, should be banked in the artefact alongside the residuals. `L6-e` v2 is the natural
place to start, since it must report at two reaches anyway.**

---

## F5 — §53's ×130 SEPARATION COMPARES A PER-DECADE INCREMENT WITH A PER-RUNG DIFFERENCE. Disclosed, not resolved.

§53 separates §52 (the divergent functional) from §51 (the under-claim) by the ratio

`|−8.06375e-3| / 6.225723e-5 = 129.52` (`RECOMPUTED@414`),

the numerator being the ladder's last step `J3 → J4` and the denominator the far-field increment
**per decade of radius** at the minimiser
(`p2_route_ljver_v1.json → cutoff_sensitivity`, the `1e6 → 1e8` band).

**The two quantities have different units.** The rungs differ in reach by a fraction of a decade
(F4: 60 → 72 nodes is not a decade of `r_max`), and the artefact banks no field from which that
fraction can be read. **The conclusion — that the truncation bias is far too small to explain the
ladder's flatness — is very likely right**, because two orders of magnitude is a wide margin and the
rung reach difference is well under one decade in either direction. **But it is an
order-of-magnitude argument, not an exact accounting, and §53 does not say so.**

`DRAFT.md` §6.2 states it at that reduced strength and discloses the caveat rather than resolving
it. `WAVE9_PLAN.md` instructs `V-W8` to attack exactly this (item 3), which is the correct route;
this finding is filed so that the caveat is on the record independently of what `V-W8` concludes,
and so that it is not lost if `V-W8` upholds the ratio for a different reason.

**Routing: `CORRECTIONS.md` — a commensurability caveat on §53's ×130, to stand whatever `V-W8`
rules.**

---

## F6 — THE PROGRAMME HAS NO CROSS-LEG INSTRUMENT AT ALL, AND THE GAP HAS NO NAME AND NO COUNT.

§45 counted one blind spot (an error shared between an artefact and its own checker: 32 of 49,
`UNBANKED` per F1). §51 is the neighbouring one and the record explicitly notes there is **no count
for it**. Drafting made the reason concrete, and it is stronger than "no count":

**Every instrument in this programme is scoped to a single unit or a single wave.** An evidence
script rebuilds its own unit's claims. A verifier checks a wave's units against *their* pre-committed
gates. A depth register grades a citation. `test_headroom.py` measures byte caps. **Not one
instrument in the repository takes a number from leg A and a number from leg B and asks whether one
makes the other meaningless.** §51 is what that costs, and §51 is not a special case: the same
shape — two correct artefacts, one relationship nobody computed — is available anywhere two units
touch the same objective.

The candidate mechanism is not expensive: when a unit lands a number that varies a parameter the
record already varies elsewhere (discretisation, budget, cutoff, seed count), a standing check asks
for the ratio of the two effects. §51 would have been caught by one line.

**Routing: `CORRECTIONS.md` as a named class (`cross-artefact shared error`) with an explicit note
that its incidence is UNMEASURED, plus an `OPTIONS.md` entry for a cross-leg instrument. Both are
the Conductor's to write, not mine.**

---

## F7 — WE HAVE PRE-REGISTRATION AND WE DO NOT HAVE BLINDING, AND THREE GATES WERE AMENDED BY PARTIES WHO COULD SEE THE DATA.

This is a literature finding with a record consequence, so it is filed here as well as written into
`DRAFT.md` §3.2.

Roodman (PHYSTAT2003, **FULL TEXT**) documents blind analysis as standard practice in particle
physics since the 1990s: the analyst is prevented from seeing the answer — in the KTeV construction,
from seeing even *which direction* the result moves — while the analysis is finalised. **Our gates
are pre-registration; our analysts watch the number form.**

The record contains three gates amended mid-run: `CORRECTIONS.md` §41 (a `NO` branch that did not
entail its stated reading, found at iteration 7,000 of 20,000 with the trajectory visible), §44 (a
licence keyed to a single terminal sample of a series whose trailing spread is 6.7× on one start and
24–34× on two others), and §53 (the `L6-e` v2 gate, rewritten before dispatch after a sibling unit's
answer changed what the comparison meant).

**All three amendments are, in my judgement, improvements. All three were written by parties who
could see data bearing on the outcome.** The record's defence in each case is that the amendment
landed before the gate number existed. That defence is real and it is exactly the defence
blind-analysis practice exists because nobody can evaluate about themselves.

I am **not** proposing that this programme adopt blinding — for most of what it does, the "answer"
is not a scalar that can be hidden, and a salt-and-unsalt mechanism would be a large build. **What I
am proposing is that the record stop describing its gate discipline as though it were the strong
form.** It is the weak form of a thirty-year-old practice, and `DRAFT.md` says so.

**Routing: `CORRECTIONS.md` (a note that the pre-commitment discipline is unblinded, with the
Roodman citation at FULL TEXT), and `SOURCES.md` (done, this leg, append-only).**

---

## F8 — N-VERSION INDEPENDENCE IS AN ASSUMPTION THIS PROGRAMME RELIES ON AND THE PUBLISHED EVIDENCE IS AGAINST IT.

The programme's largest adverse finding rests on the cross-unit design: two units, two methods,
never told each other's result. NASA TM-102613 (**FULL TEXT**, leg 414) reports twenty independently
developed versions of an aerospace application, four development sites, independent certification —
and finds coincident failures at rates *greatly exceeding* chance under independence, concluding
that independent development alone is not sufficient.

**Our two "independent" units share a model, a repository, a prompt lineage and a house style** —
every correlate the NASA experiment worked to eliminate, and it still measured dependence.

This does **not** retract anything. `T4`/`T6` reached the same adverse conclusion by genuinely
different methods, and `L-JVER` produced a disjoint reimplementation that agreed at `1.10e-14` on
shared nodes while disagreeing by `4.29e-1` elsewhere — which is the design working. **It means the
programme should stop treating "two agents will not make the same mistake" as a premise and start
treating it as an unmeasured hypothesis with adverse published evidence.**

**Routing: `CORRECTIONS.md` (a standing caveat on the cross-unit design, with the citation), and
`SOURCES.md` (done).**

---

## F9 — UNBANKED CONCLUSIONS ARE OUTSIDE EVERY MECHANISM, AND THEY SELECT THE NEXT UNIT.

Filed as a finding rather than only as paper prose because it bounds the whole method and the record
states it only once, inside a single correction.

Every mechanism in the programme operates on **what is written into an artefact**. The record
contains the counter-case: having just written the observation that a cheap quantity is routinely
substituted for an expensive property, the Conductor declined to *bank* an unlanded number on
exactly those grounds — **and then made the inference anyway, in prose, and reasoned from it**,
selecting subsequent work on that basis (the stated reading was that a continuation start was
approaching stationarity; the fuller series gives `ρ = −0.563` with a reversal in the last 1,000
iterations, at a value still 43× threshold).

**Declining to bank a claim is not the same as declining to believe it.** No instrument here could
have caught this, because there was nothing to check.

**Routing: `CORRECTIONS.md` — this belongs in the standing preamble, not buried in one entry. Any
prose that reasons from an unlanded number must name it as unlanded at the point of use, in the same
sentence.**

---

## F10 — THE TOOL-OUTPUT CHANNEL DROPS WORDS. RE-CONFIRMED LIVE AT LEG 414, WITH A MEASUREMENT.

`PB1`'s finding F8 (leg 411) is not a one-off and is not fixed. At leg 414, reading file content
back through the tool-output channel, a 224-character quotation returned with roughly a third of its
function words missing while `len()` on the identical string, computed in the same process, returned
224. The same leg saw a 21-line file region render as a single run-on paragraph with articles,
prepositions and auxiliaries stripped, annotated by the harness as *"250 items compressed to 169"*.

**Consequence for every agent in this repository, not just paper units:** any quotation an agent
"read and retyped" is unreliable, and so is any judgement made by eyeballing rendered file content
for the presence or absence of short words. Byte-level verification (`len`, `sha256`, `grep -c`) is
the only trustworthy read.

**Mitigation built and landed this leg:** `writeup/papers/P4_METHODOLOGY/inject_quotes.py` extracts
every quotation from its source by (start marker, end marker) and writes it into the target
mechanically, exiting non-zero on any unresolved token. **All 19 quotations in `DRAFT.md` were
injected; none was typed.** The script is general and is not specific to `P4`.

**Routing: `CORRECTIONS.md` as a standing hazard (`PB1` F8 re-confirmed, with the leg-414
measurement), and `ORCHESTRATION.md` as a recommended practice for any unit quoting a source
verbatim. The script is available for reuse as it stands.**

---

## F11 — DEBTS INCURRED BY THIS LEG, STATED SO THEY ARE NOT MISTAKEN FOR COMPLETED WORK.

1. **A novelty check on the depth register has never been run.** `DRAFT.md` §10.4 records that no
   published counterpart was found *at a depth I could reach*, and explicitly declines to call it
   novel — applying this programme's own rule that failing to find a thing is not evidence it is
   absent. The neighbouring literatures that would settle it (evidence-grading frameworks in
   systematic review; quotation-accuracy studies in medical bibliometrics) were **not read**.
2. **Three of the four canonical adversarial-collaboration sources are `UNREACHABLE` from this
   container** (Mellers–Hertwig–Kahneman 2001, Kahneman–Klein 2009, Cowan et al. 2020). §3 of the
   draft names adversarial collaboration as one of the three practices this paper is most at risk of
   reinventing, and the comparison therefore rests on a single reachable modern protocol paper
   (Melloni et al. 2023, FULL TEXT). **That is a thinner base than the comparison deserves.**
3. **Mutation testing's primary sources are `UNREACHABLE`** (DeMillo–Lipton–Sayward 1978;
   Jia–Harman 2011). §3.5's claim that our check-mutation is an instance of mutation testing is
   therefore made at **no** depth. It is a plausible claim and it is unsupported by anything read.
4. **IEEE 1012 was reached at its public scope page only.** Its treatment of technical, managerial
   and financial independence — the part that would sharpen §3.3 — was not read. No claim in the
   draft rests on it.
5. **We have no audit of our own prose-to-artefact fidelity.** COMPare measured trial reports
   against their own protocols and found a mean of 76% of pre-specified primary outcomes correctly
   reported and 5.4 undeclared extra outcomes per trial, in a field where pre-registration has been
   mandatory for fifteen years. **The equivalent audit here has never been run**, and F1 is the first
   place I looked and found the measurement missing.

**Routing: `CORRECTIONS.md` (debts 1, 3, 5) and `SOURCES.md` (debts 2, 4 — recorded append-only
this leg as `UNREACHABLE` / `SCOPE PAGE ONLY`, never as zeros).**

---

## What this unit did NOT do

- Contacted no author, group, maintainer or list. Fetches were of published material only, over
  public endpoints, and no paywall was circumvented.
- Did not edit `CORRECTIONS.md`, `STATE.md`, `WALLS.md`, `OPTIONS.md`, `writeup/waves/**`,
  `reports/`, `Papers/MANIFEST.md`, or any sibling unit's files.
- Did not read `DIRECTION.md`.
- Moved no `L1→L4` link. Nothing in this leg is progress toward Clay (~0.05%), and nothing in it is
  a proof: every computational result it discusses is Tier 2.
