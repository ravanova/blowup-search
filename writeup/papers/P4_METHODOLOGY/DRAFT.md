# Mechanised scepticism and its blind spots

### What a pre-committed, agent-run computational-mathematics programme caught, what it missed, and for how long

**DRAFT — `P4`, leg 414, wave 9, 2026-08-19.** Not submitted. **No unit may cite this file**
(`writeup/papers/README.md`). A paper is a **view of the record, never a source**.

**How to read the numbers.** Every quantitative claim below carries the banked artefact and field
it came from, in the form `[file → field]`. A claim marked **`RECOMPUTED@414`** was re-derived
from that field by this unit while drafting, not copied from the prose that reports it. A claim
marked **`UNBANKED`** exists in the record only as prose — no artefact field holds it — and it is
labelled that way every time it appears, including in the abstract. A claim marked **`UNVERIFIED`**
stays `UNVERIFIED` here. **No result reported as `UNDER-RESOURCED` is written as a null result.**

**How the quotations got here.** Not one was typed. Every quoted sentence — from the literature
and from this repository — was extracted from its source by `inject_quotes.py` (start marker, end
marker) and written into this file mechanically. The reason is in §12.5 and it is not
fastidiousness: the channel these agents read through drops words.

---

## Abstract

We report on a computational-mathematics programme run by large-language-model agents under a
written contract that mechanises scepticism: gates pre-committed in a plan commit before any unit
is dispatched, both outcomes of every gate named in advance, controls planted so that they must
fire in both directions, a verdict `UNDER-RESOURCED` held distinct from `NO`, verifiers forbidden
from auditing work they planned, and a correction register placed *beside* banked data rather than
over it. The programme has produced, over roughly 414 dispatched units, a register of **twelve
filed self-detections**. We report the honest tally: **2 prospective catches against 9
retrospective** — where "prospective" means a written rule fired on a new instance before the
number was banked. **One data point, and then a second, is not a rate, and we do not present it as
one.**

The paper's centre is not a catch. It is a miss. Two correct, banked, separately checked numbers
in two different units — a four-rung discretisation refinement moving a residual `−4.994561%`
`[p2_route_l6_profile_v1.json → gate.B.per_rung_residual]`, and a single ×25 iteration-budget step
at *fixed* discretisation moving it `−6.751678%` `[p2_route_l6b_v1.json →
gate.smallest_residual_at_20000]` — were never divided by one another. The budget term is
**×1.3518** of the entire refinement ladder `[p2_verify_wave7_v1.json → measured.the_under_claim_absent_from_the_landing_record.ratio]` (`RECOMPUTED@414`), which means the refinement study
did not measure refinement. **Nobody performed that one line of arithmetic for eleven legs**, past
the unit, past the integrating Conductor, and past a verifier that passed the wave clean.

We further disclose a control that was planted for exactly this hypothesis and **did not fire as
planted**: the same unit banked a cap-stability sweep over iteration caps 50–800 reading
`verdict_is_stable_in_the_cap = true` `[p2_route_l6_profile_v1.json →
gate.B.stability_against_the_iteration_cap]`, which a later verifier showed to be a post-hoc
truncation of the same 800-iteration runs and therefore not a budget control at all. The published
account of the miss ("nobody divided one by the other") is therefore incomplete in the direction
that flatters the discipline.

Against the literature the result is deflationary. Pre-committed gates are **pre-registration**
under another name, and weaker than **blind analysis** as particle physics has practised it since
the 1990s, because our analysts see the number as it forms. "A verifier may not check what it
planned" is **independent verification and validation** and **separation of duties**, in their
weakest form. "Planted controls that must fire" is positive/negative controls plus **mutation
testing**. "`UNDER-RESOURCED` is not `NO`" is *absence of evidence is not evidence of absence*.
We could not find a published counterpart, at a depth we could reach, for only one construct — a
per-citation **depth register** (`ABSTRACT` / `FULL TEXT` / `RECOMPUTED` / `SECOND HAND` /
`UNREACHABLE`) that gates what a claim is allowed to rest on — and we explicitly decline to call it
novel, because failing to find a thing is not evidence it is absent, which is the same rule as
above.

The transferable findings are three. **(i)** A check written by the unit that wrote the artefact
certifies internal consistency, not the claim; measured over this repository's evidence scripts at
**32 of 49** — a figure that is `UNBANKED` (§8.2). **(ii)** The neighbouring blind spot has no
count at all: an error shared between two artefacts that no single checker reads together. **(iii)**
Every mechanism described here operates on what is *written into an artefact*; none touches what an
agent concluded and carried forward unbanked — and unbanked conclusions are what select the next
unit.

---

## 1. What is claimed, and the ceilings, before anything else

### 1.1 The claim

A set of mechanical disciplines, applied to an agent-run computational programme, produces a
record in which the programme finds and retracts its own errors, and the evidence for this is the
register of retractions rather than an assertion that it works.

### 1.2 The claim is weaker than it was, and the revision is the spine

The disciplines that did the catching are **not** the ones the programme most advertises. What
caught things, repeatedly, was **structural separation between the claimer and the checker**: two
units run in parallel and never told each other's result; a verifier forbidden from auditing what
it planned; a co-tenant's instrument read from outside the unit; and — five times out of twelve —
**someone opening a primary artefact for an unrelated reason.** None of those is a check a unit
wrote about itself.

### 1.3 The ceilings, stated before the evidence and not at the end

1. **`n = 1`.** One programme, one problem domain, one model family, one operator. There is no
   control arm. **We cannot say what an undisciplined version of this programme would have missed**,
   and nothing here should be read as an effect size.
2. **The record is both the instrument and the evidence.** The corrections register is written by
   the same parties that make the errors. Every "catch" in this paper is a *filed* catch. Errors
   that were made and not noticed are, by construction, absent from the numerator — and §7 is our
   attempt to bound that, not to eliminate it.
3. **`2` prospective catches is a count, not a rate.** It has no denominator: we do not know how
   many opportunities to fire a rule went by unrecorded.
4. **This paper contains no mathematics and moves no mathematical link.** The programme's own
   ladder from lemma `L1` to lemma `L4` is untouched by everything below. The underlying target is
   a Clay Millennium problem, the programme's own standing estimate of reaching it is **~0.05%**,
   and **no output described here is movement toward it.** Every computational result quoted as
   evidence is Tier 2 (float64 numerics with declared truncations); **Tier 2 is never a proof.**
5. **The subject and the author are the same kind of system.** This draft was written by an LLM
   agent, about a programme of LLM agents, from a record written by LLM agents. The obvious
   objection — that a system evaluating itself will grade generously — is not answered by this
   paper. What is offered instead is that the strongest material in it is adverse.

---

## 2. The setting, in the minimum needed to read the evidence

**This section is deliberately short. A tour of the repository would be longer and would not be an
argument.** Five constructs are load-bearing for everything below; nothing else about the system is
described.

1. **Unit / leg.** A unit is one dispatched agent with one brief and one job. A leg is its
   numbered slot in the record. Legs referenced here run from 348 to 414.
2. **Wave / plan commit.** Units are dispatched in waves. **The wave plan, including every gate,
   is committed to the repository before any unit in the wave is dispatched.** The gate text is
   immutable thereafter; amendments are documents placed beside it, never edits to it.
3. **Gate.** A gate is a question with a pre-committed answer for each outcome: *"is X true — YES
   or NO"*, plus, written in advance, what each answer licenses and what it does not. A third
   verdict, `UNDER-RESOURCED`, is available and is **not** a `NO`.
4. **Artefact.** A unit lands (a) curated JSON in `writeup/data/`, (b) an `*_evidence.py` script,
   and (c) a journal. The contract's own words for (b), verbatim: *"plus an `*_evidence.py` script that rebuilds the figures/claims from the curated JSON without re-running anything"*
   `[ORCHESTRATION.md → §6 clause 3]`. That clause matters twice below, once as a virtue and once
   as the source of a measured blind spot.
5. **Verifier, and the correction register.** A verifier unit audits a wave against its
   pre-committed gates and **may not verify anything it planned**. Findings land in a numbered
   register (`CORRECTIONS.md`) whose defining property is that corrections are placed **beside**
   the banked data, never over them: a superseded number stays readable with its correction
   attached.

---

## 3. Each mechanism, and the published practice it is an instance of

This is the section where a paper of this kind reinvents something and gives it a new name. We
therefore state, for each mechanism, the existing practice, the depth at which we read that
practice, and a verdict. **Three of the six are renames. One is a rename of a *weaker* form of the
existing practice. One is a rename of a practice whose published evidence contradicts the reason we
adopted it.**

| our mechanism | existing practice | depth reached (§10) | verdict |
|---|---|---|---|
| pre-committed gate, both outcomes named, committed before dispatch | pre-registration; registered reports; the statistical analysis plan of a clinical trial | Nosek et al. 2018, **FULL TEXT** | **RENAME** |
| the analyst may see the number while it forms | **blind analysis** (particle physics, 1990s–) | Roodman 2003, **FULL TEXT** | **RENAME OF A WEAKER FORM** — theirs is strictly stronger |
| verifier may not audit what it planned | independent V&V; separation of duties; theory-impartial laboratories in an adversarial collaboration | IEEE 1012 **SCOPE PAGE ONLY**; NIST SP 800-53r4 AC-5 **FULL TEXT**; Melloni et al. 2023 **FULL TEXT** | **RENAME, weakest form** |
| two units, same question, never told each other's result | N-version programming / multi-version software | NASA TM-102613, **FULL TEXT** | **RENAME — and the published evidence is against the assumption we rely on** |
| planted controls that must fire in both directions; mutation-testing a check | positive/negative controls; blind signal injection; mutation testing | Roodman 2003 **FULL TEXT**; DeMillo–Lipton–Sayward 1978 **UNREACHABLE** | **RENAME** |
| `UNDER-RESOURCED` is a verdict, not a `NO` | *absence of evidence is not evidence of absence*; inconclusive vs. negative trials | Altman & Bland 1995, **CITATION ONLY** | **RENAME** |
| every number in prose must exist in the banked JSON | CONSORT / outcome-reporting fidelity; provenance rules for reproducible computation | Goldacre et al. 2019 **FULL TEXT**; Sandve et al. 2013 **FULL TEXT** | **RENAME — with a measurement attached** |
| per-citation **depth register** gating what a claim may rest on | *no counterpart found at reachable depth* | — | **NOT CLAIMED NOVEL** (§10.4) |

### 3.1 Pre-registration: a rename, and we should say so plainly

Nosek, Ebersole, DeHaven and Mellor state the problem our gates exist to solve:

> This distinction between postdiction and prediction is appreciated conceptually but is not respected in practice. Mistaking generation of postdictions with testing of predictions reduces the credibility of research findings.

and the remedy:

> Preregistration distinguishes analyses and outcomes that result from predictions from those that result from postdictions.

That is our pre-committed gate, in a literature two decades older than this programme. The one
respect in which our implementation is *not* weaker is enforcement: the plan is a git commit whose
hash precedes the dispatch, so a gate cannot be quietly rewritten after the fact — the amendment
must be a new document. Nosek et al. also anticipate our commonest event:

> Deviations from data collection and analysis plans are common, even in the most predictable investigations.

The record bears that out: three of our gates were amended mid-run (§7.4).

### 3.2 Blind analysis: the practice we did *not* adopt, and it is the one that would have bitten

Roodman's review of blind analysis in particle physics defines it:

> A blind analysis is a measurement which is performed without looking at the answer. Blind analyses are the optimal way to reduce or eliminate experimenter’s bias, the unintended biasing of a result in a particular direction.

and describes the KTeV construction, which hides not the data but *the direction of movement*:

> The use of the 1 or −1 factor prevented KTeV from knowing which direction the result moved as changes were made.

**Our programme has pre-registration and does not have blinding.** The analyst — unit or Conductor
— watches the number form. This is not hypothetical harm:

- A gate of the Conductor's own was found **half-defective at iteration 7,000 of 20,000**, and the
  finding was made while the trajectory was visible `[CORRECTIONS.md §41]`. The record's defence is
  that the amendment landed *before the gate number existed*. Under a blind protocol that defence
  is not available and not needed, because the amendment would have been made without knowing which
  way the number was going.
- A remedy written ten minutes later keyed a threshold to a **single terminal sample** of a series
  whose trailing spread is `6.7×` on one start and `24–34×` on two others `[CORRECTIONS.md §44]`;
  the correction to it was likewise written with the series in view.
- A pre-committed gate was **rewritten before dispatch** after a different unit's answer changed
  what the comparison meant `[CORRECTIONS.md §53, the `L6-e` v2 gate]`. The rewrite is, in our
  judgement, correct — it replaced a comparison of two different truncations of a divergent
  integral with a matched-truncation comparison. **It was still a gate rewritten by a party who had
  seen data bearing on it**, and blind-analysis practice exists precisely because that judgement is
  the one nobody can make about themselves.

**Verdict: our pre-commitment discipline is a rename of a weaker form of an existing practice.**
The stronger form is available, is thirty years old, and we do not implement it.

### 3.3 Independent verification: a rename, in the weakest available form

IEEE 1012 defines the activity — read at the standard's public scope page only, the standard itself
being paywalled:

> Verification and validation (V&V) processes are used to determine whether the development products of a given activity conform to the requirements of that activity and whether the product satisfies its intended use and user needs.

NIST SP 800-53r4 defines the organisational control, and the difference in *rationale* is worth
recording rather than glossing:

> Separation of duties addresses the potential for abuse of authorized privileges and helps to reduce the risk of malevolent activity without collusion.

**That rationale is anti-fraud, not anti-error.** Our separation exists because a party cannot
audit its own reasoning, not because it might lie. The nearest published practice with our
rationale is the theory-impartial data collection of a formal adversarial collaboration:

> Six theory-impartial laboratories will follow the study protocol specified here

`[Melloni et al. 2023, PLOS ONE 18(2) e0268577]`. **Six laboratories with no stake in either
hypothesis** is the strong form. Ours is the weak form: the verifier is a fresh agent instance of
the same model family, reading the same repository, under conventions written by the party it is
auditing. It is separation of *context*, not separation of *interest*. It has nonetheless produced
this programme's two largest self-findings (§5, §7.2), which is the honest thing to say on both
sides.

### 3.4 Two units, one question: a rename whose published evidence runs against us

The programme's proudest catch is that its lane's central premise was measured **FALSE** by two
units using two methods that were never told each other's result. That design has a name —
N-version programming — and a literature, and the literature is adverse. The NASA Langley
experiment ran twenty independently developed versions of an aerospace application from four
geographically separate development sites, with independent certification:

> For the twenty versions in this experiment, coincident failures occurred at rates that greatly exceed the rates expected by chance under the assumption of independence.

> the present study suggests that independent development […] alone is not sufficient to achieve high reliability gains over using a single version.

(The elision spans a page break in the scanned report; both fragments are extracted mechanically, not retyped.)

`[NASA TM-102613, §V]`. **Independent development does not deliver independent failure.** Applied
to us this is sharper than it looks, because our two "independent" units share a model, a
repository, a prompt lineage and a house style — every correlate the NASA experiment worked hard to
remove, and it still measured dependence. **A programme whose error model is "two agents will not
make the same mistake" is resting on an assumption that has been tested elsewhere and did not
hold.**

We record one case where the design nonetheless produced its intended result under conditions the
NASA finding would predict against: a unit built a second implementation of a residual functional
in a disjoint basis, with a disjoint derivative mechanism and a disjoint quadrature, and the two
implementations agreed to `1.10e-14` at the minimiser while disagreeing by `4.29e-1` away from it
`[p2_route_ljver_v1.json → gate_points]` (`RECOMPUTED@414`). **The disagreement was the finding**
(§6). That is one instance, in one programme, and it is not a rebuttal of TM-102613.

### 3.5 Controls that must fire: a rename, and one of ours did not fire

Positive and negative controls are not new, and neither is mutation-testing a checker (DeMillo,
Lipton & Sayward 1978 — `UNREACHABLE`, §10.5). Our implementation is ordinary: a defect is planted
that must move the answer, and a check is mutated to confirm it fails. Two live instances:

- A pipeline control that **moves the objective by 80%** when a defect is planted, banked alongside
  the gate it protects `[p2_route_ljver_v1.json]`.
- `test_headroom.py`, mutation-tested on four separate breaks including *"the block to be measured
  cannot be located"*, which it treats as **FAIL** — an unchecked cap is not a passed cap
  `[CORRECTIONS.md §48]`. Executed by this unit at leg 414: `§3j HEADROOM: PASS` on five rows.

**And one control did not fire as planted, and the binding rule for this paper is that it gets
disclosed here rather than only in the journal.** See §5.3.

### 3.6 A rule that is a rename *with a measurement attached*

Our binding rule — every number in prose must exist in the banked JSON — is CONSORT's
outcome-reporting requirement in another vocabulary. What the medical literature adds is the
*compliance* measurement, and it is bleak. The COMPare project checked published trial reports
against their own pre-registered protocols:

> We assessed 67 trials in total, a mean of 13.4 trials per journal (range 3–24).

> on pre-specified primary outcomes (mean 76% correctly reported, journal range 25–96%), secondary outcomes (mean 55%, range 31–72%), and number of undeclared additional outcomes per trial (mean 5.4, range 2.9–8.3)

`[Goldacre et al. 2019, Trials 20:118]`. **Mean 76% of pre-specified primary outcomes correctly
reported, and a mean of 5.4 undeclared additional outcomes per trial — in a field where
pre-registration is mandatory and has been for fifteen years.** The rule is not the hard part. We
have no equivalent audit of our own prose-to-artefact fidelity, and §8.2 records the first place we
looked and found none.

Sandve et al.'s reproducibility rules cover the provenance half:

> Rule 1: For Every Result, Keep Track of How It Was Produced

> Rule 5: Record All Intermediate Results, When Possible in Standardized Formats

`[Sandve et al. 2013, PLoS Comput Biol 9(10) e1003285]`. Our curated-JSON contract is Rule 1 and
Rule 5 with a schema.

---

## 4. The tally: 2 prospective against 9 retrospective

**"Prospective"** means: a rule that was written down in response to one defect fired on a
*differently shaped* new instance, in a different lane or on a different quantity, **before the new
number was banked.** Everything else is retrospective, however fast it arrived.

| # | what | when | found by | P/R | how it was actually found |
|---|---|---|---|---|---|
| 1 | a unit retracted its own headline: the metric counted cross-run re-finds as successes — the defect it was introduced to remove, one level up | wave 1 | the unit itself | R | re-reading its own metric definition |
| 2 | the lane's central premise measured **FALSE**; the cited certification is by the banned apparatus and both rows are 2D lifts | wave 2 | two units, two methods, never told each other's result | R | cross-unit design (**not** an evidence check) |
| 3 | an `8×` cost overrun refuted — wall-hours against core-hours; the factor **was the worker count** | `V-W3` | verifier | R | verifier re-derivation |
| 4 | a post-hoc pass-criterion located on a result the record called *shut and verified* | `V-W5` | verifier | R | verifier re-derivation |
| 5 | a queued remedy named by a **family name, not a scheme**; naming it properly showed the gate needed **two** second-order steppers, not one | pre-dispatch, wave 8 | the Conductor | R | pre-dispatch read of its own queue |
| 6 | a load-bearing source carried at **abstract depth for 45 legs**, through a lane, a roadmap section, an escalation and a user ruling | §3k sweep | depth register | R | building the register |
| 7 | a gate **half-defective**: its `NO` branch only follows at a stationary terminal iterate and the wording never required one | mid-run, iteration 7,000 of 20,000 | the Conductor | R | watching a live run |
| 8 | occupancy computed as finished-work over wall×shards, `80.5%`; the rule written 4 h earlier caught it **before the number was banked**; corrected `92.6%` | 06:05, 2026-08-19 | §42's own rule | **P** | the rule fired |
| 9 | a file landed **2,151 bytes over its cap** through a `MERGE GATE: PASS` `[git: 32,526 → 34,919 bytes vs a 32 KB cap]` (`RECOMPUTED@414`) | 09:40, 2026-08-19 | integration audit | **P**(weak) | someone ran `wc -c` **for an unrelated reason** |
| 10 | the documentation contract **mandates** the blind spot §45 measured: one script ran 31 checks, 0 failed, **0 recomputed anything from a primary source** (`RECOMPUTED@414` — executed, `31 checks, 0 failed`) | leg 410 | landing audit | R | grepping for labels a brief had required |
| 11 | **the under-claim**: a ×25 budget step moved the objective **×1.3518** of an entire four-rung refinement ladder, and nobody divided one by the other for **eleven legs** | leg 412 | verifier, third pass | R | one line of arithmetic across two units |
| 12 | a `[P]`-class check re-hashed PDF bytes and caught the leg's **own** banked manifest carrying two transposed characters — which no re-read of the artefact could have caught | leg 411 | the unit's own independent check | R | the check was of the *independent* class |

**Honest reading of that table.**

- **The tally is 2 prospective against 9 retrospective** (entry 12 is a category demonstration
  rather than a catch of a live defect, and is counted separately below).
- Entry 9 is the weaker of the two prospective catches and must be graded as such: entry 8 fired
  **before the number was banked**; entry 9 fired **after** a bad state had landed on the main
  branch and been pushed.
- **Five of the twelve were found by someone opening a primary artefact for an unrelated reason.**
  That is not a discipline. It is what a discipline looks like when it is not working and something
  else is.
- **The single most consequential entry, #11, was caught by nothing structural at all.**

---

## 5. The centre of gravity: an error that nobody made

Every entry above except one is an error *found*. Entry 11 is an error *not* found, and it is the
most informative thing in this paper because no number in it was ever wrong.

### 5.1 The arithmetic

A unit refined a discretisation through four rungs, all runs capped at 800 optimiser iterations,
and reported that the residual **does not decrease under refinement**. Five legs later a second
unit raised the iteration cap **×25** with the discretisation held fixed at the top rung.

| what was varied | `ρ` | change |
|---|---|---|
| four rungs of refinement, `J1 → J4`, cap 800 | `1.6986514108481086 → 1.613811231995397` | **`−4.994561%`** |
| one budget step ×25, `n_dof` fixed at 6720 | `1.613811231995397 → 1.504851895102804` | **`−6.751678%`** |

`[p2_route_l6_profile_v1.json → gate.B.per_rung_residual.J1, .J4]`;
`[p2_route_l6b_v1.json → gate.smallest_residual_at_20000]`. Both rows `RECOMPUTED@414`.

**One budget step moved the objective ×1.3518 of what the entire four-rung refinement ladder
moved.**
`[p2_verify_wave7_v1.json → measured.the_under_claim_absent_from_the_landing_record.ratio]`
(`RECOMPUTED@414`.) The ladder was differenced at a cap now demonstrated to dominate the quantity being
differenced. It therefore does not measure refinement; it measures where a bounded-memory
quasi-Newton optimiser had got to after 800 iterations at each discretisation, and the rungs are
not converged enough to be subtracted from one another. **The reported headline is not established
in either direction.**

And the ordering can inverse. Rung `J3` reads `1.6218749783288575`
`[p2_route_l6_profile_v1.json → gate.B.per_rung_residual.J3]`, above `J4`. For the ladder to
reverse, `J3` at raised budget must fall **`7.2153%`**; one rung up, at *more* degrees of freedom,
the same budget increase delivered **`6.7517%`**. **The margin is `0.4636` percentage points**
`[…the_under_claim_absent_from_the_landing_record.margin_percentage_points]` (`RECOMPUTED@414`), and it is the wrong way round by less than the measurement already in hand.
`J3` has *fewer* degrees of freedom and is cheaper to run, which on the usual expectation makes it
the rung most likely to clear the bar. **Nothing in the record establishes that it does not**, and
the measurement that would settle it is one unit, priced at ~20–35 core-hours, pre-committed and
scheduled at the time of writing.

### 5.2 Why it was missed, and what class of blind spot it is

The two numbers live in different units, in different waves, in different files, under different
headings, and each was correct where it sat. **Every instrument in this programme is scoped to a
single unit**: a unit's evidence script rebuilds a unit's claims; a verifier checks a wave's units
against their pre-committed gates. §8.1 counts the scripts that cannot see an error shared between
an artefact and its own checker. **This is the neighbouring blind spot, and there is no count for
it: an error shared between two artefacts that no single checker reads together.** No gate in this
programme compares a number in one leg against a number in another and asks whether one makes the
other meaningless.

### 5.3 The control that was planted for this and did not fire as planted

**This subsection exists because the paper's rules require it, and because the published account of
the miss is incomplete without it.**

The record's account of entry 11 is *"nobody divided one by the other."* That is true of the
division. It is **not** true that nobody planted a control against the budget hypothesis. The same
artefact banks a cap-stability sweep:

`[p2_route_l6_profile_v1.json → gate.B.stability_against_the_iteration_cap]`, caps
`50 / 100 / 200 / 400 / 800`, all five rows returning `decreases_under_refinement = NO`, and the
block's verdict field reading `verdict_is_stable_in_the_cap = true` with the stated rationale, in
the artefact's own words:

> *"if the verdict is the same at every iteration cap, it is a fact about the construction and not about where the optimiser stopped"*

**That is exactly the right idea, and the control was structurally incapable of testing it.** A
later verifier established that the `by_cap` table is a **post-hoc truncation of the same
800-iteration runs** — the minimum over recorded trajectory points with `k ≤ K` — and that each
rung's continuation start was warm-started from the previous rung's *full-budget* minimiser, so
every truncated column still carries the full budget from the rung below `[CORRECTIONS.md §38]`.
It controls nothing about budgets above 800.

The numbers show how completely it misled. Over the caps it did sample, `16×` of budget, the top
rung moves from `1.6202442460112116` (cap 50) to `1.6138112319953968` (cap 800):

> **`−0.397040%` over a 16× budget range, and then `−6.751678%` over the next 25×.**
> (`RECOMPUTED@414` from the same field.)

The cap response is radically non-linear and the sampled range sat entirely inside a **false
plateau**. Read as a trend it points the wrong way for the verdict as well: the refinement rate
over the last three rungs reads `−0.03258 → −0.03130 → −0.02958 → −0.02667 → −0.02224` as the cap
rises 50 → 800 — **shrinking monotonically in the budget, by 31.7% over the range measured**
(`RECOMPUTED@414` from `…by_cap.<K>.rate_dlogresid_dlogndof_last3`).

**And no evidence check touched the block at all** — recorded as a coverage defect by the wave-6
verifier.

**What this costs the paper, stated at full strength.** A planted control that cannot fail is worse
than no control, because the discipline then reports a *passed* control and the reader — including
the next unit, the integrating Conductor and the first verifier — stops asking. The result was that
an `UNDER-RESOURCED` measurement (a cap sweep whose range was three-fold too narrow) **was written
into the record as a null result** (`verdict_is_stable_in_the_cap = true`). This programme has a
written rule that `UNDER-RESOURCED` is never a `NO`. **The rule did not prevent its own most
expensive instance**, and the reason is that the rule governs *verdicts a unit declares* and says
nothing about *controls a unit passes*.

### 5.4 What this does not mean

It does not mean the banked numbers are wrong; each is correct as computed. It does not overturn
the unit's gate answer — that answer is left **resting on an ordering that has never been measured
at a budget where the ordering means anything**, which is a different and weaker position than
either "upheld" or "withdrawn". It moves no mathematical link. It is **not progress.**

---

## 6. The second structural finding — and an instrument did not find it

In the same wave, a construction unit built to re-derive an objective from the written mathematics
in a disjoint basis found that **the objective itself is a divergent integral**, and that every
residual in the record is a value of a 72-node truncation of it.

The measurement that makes this a finding rather than a bug report: the unit's independent
operator, evaluated at the original code's own quadrature nodes and contracted with its own
weights, reproduces the original values at relative `1.10e-14`, `2.46e-15`, `5.90e-15`, `1.86e-14`
— **including at the point where the agreement gate fails at `4.29e-1`**
`[p2_route_ljver_v1.json → gate_points; X9]`. Two independently converged quadrature rules
disagreeing about one integrand, while each agrees to machine precision with the other on shared
nodes, is not a coding error in either program. It is a property of the integral: the mass per
decade of radius is flat, which *is* a logarithmic divergence.

**The divergence is present at the minimiser**, which is where every evaluation in the record sits.
Per-decade increments in the objective, at the banked minimiser
`[p2_route_ljver_v1.json → cutoff_sensitivity]`, all `RECOMPUTED@414`:

| band of `r_max` | Δ per decade |
|---|---|
| `1e3 → 1e4` | `+9.573e-3` |
| `1e4 → 1e5` | `+3.316e-4` |
| `1e5 → 1e6` | `+6.537e-5` |
| `1e6 → 1e8` | `+6.226e-5` |
| `1e8 → 1e11` | `+6.246e-5` |
| `1e11 → 1e14` | `+6.212e-5` |

Three consecutive bands spanning eight decades agreeing to better than 1% is a constant increment
per decade. **The gate passing at the minimisers and failing away from them is not a boundary
between a good region and a bad one — it is the divergence being weakest where the optimiser was
always looking.**

### 6.1 The sign, and the uncomfortable fact about it

**Every increment above is positive** (`RECOMPUTED@414`, all six bands). Extending the domain makes
the residual *larger*; the thresholds these results had to beat were upper bounds; therefore the
truncation error points **away** from every threshold, and the gate answers built on these numbers
survive while the numbers themselves lose their meaning as values of the functional.

We report this as the record does, and we decline to soften it in either direction:

> **A foundational defect was discovered and every conclusion built on it survived, because the
> defect has a sign and the sign happened to be unfavourable to the claim nobody had made.**

**Had the sign been the other way, this programme would have lost two gate answers simultaneously,
and the discipline that would have caught it does not exist here.** The finding was made by a
construction unit that had been sent to check a *different* question — whether an objective had
ever been checked against anything outside its author's code — and not by any instrument designed to
ask whether an objective is finite. The cost of the check that would have found it, stated in the
record and not disputed here, is **minutes**: a cutoff sweep, or the mass per decade.

### 6.2 It does not subsume §5, and the arithmetic settles that

The radial reach varies across the refinement rungs — `nq_r` = 36, 48, 48, 60, 72, derivable from
the generator (`nq_r = 3·Nr + 12` at `experiments/p2_route_l6_v1.py:188`, with the rung table's
`Nr` = 8, 12, 12, 16, 20; `RECOMPUTED@414`) — so the ladder differences a divergent integral at
five different truncations, which looks at first like §6 explaining §5. It does not:

| | |
|---|---|
| divergence coefficient at the minimiser | `+6.226e-5` per decade |
| the ladder's last step `J3 → J4` | `−8.06375e-3` |
| ratio | **`×129.5`** |

(`RECOMPUTED@414`.) **The truncation bias is two orders of magnitude too small to account for the
ladder's flatness.** Two independent defects in the same four numbers.

**One caveat on that ratio, disclosed rather than resolved.** It compares an increment *per decade
of radius* with a difference *between two rungs*, and the rungs differ in reach by a fraction of a
decade that the artefact does not bank as a field. The comparison is therefore an order-of-magnitude
argument, not an exact accounting, and it is at the time of writing under audit by a verifier that
did not plan it. **We state it at the strength the record supports and no higher.**

---

## 7. What the discipline failed to catch, and for how long

A paper that reports only the catches is the failure mode it is describing. This section is the
same register read the other way.

| what was wrong | how long it stood | what it survived | how it ended |
|---|---|---|---|
| a load-bearing source carried at **`ABSTRACT`** depth | **45 legs** | a lane ranking, a roadmap section, an escalation, and a user ruling | a depth sweep; when finally read at full text and then recomputed, **the claim it carried fell** |
| the under-claim of §5 | **11 legs** | the unit, the integrating Conductor, and a first verifier that passed the wave clean | a verifier's third pass, one line of arithmetic |
| a citation naming the wrong journal, volume and pages for a theorem the wall rests on | **6 legs**, during which the repository held the correct citation and the incorrect one **simultaneously, in different files, neither noticing the other** | a verifier | a unit sent to a seam, not a defect, opened the PDF |
| the same citation defect in a **fifth** place — the **generator** that emits the string into the banked JSON | longer than the other four, because the correction pass searched prose and data and not the code that writes the data | its own correction | a correction to the correction |
| a selected column (`153.22`) quoted as the whole reading of a minimiser, repeatedly, including into a wave plan and a dispatch brief | **days** | the party whose job is to catch that | opening the banked JSON to check something unrelated |
| an evidence check that **asserted** the ranking it existed to test — it would have PASSED on the false claim and certified it | until a correction arrived from outside the unit | its own suite, reporting `N/N passed` | forced re-examination |
| a brief asking a unit to report the **ambient load** instead of its own footprint, while a co-tenant lost 40% of its throughput | for as long as the clause shipped | every review of the brief | the Conductor happened to open the co-tenant's checkpoint file mid-run |
| a size cap enforced by a person reading a number at a boundary | until a file landed 2,151 bytes over it through a passing merge gate | the merge gate itself, which did not check the cap | `wc -c` run for an unrelated reason, 90 minutes after the cap had been measured by hand and correctly |

### 7.1 Two remedies that had the same defect as what they remedied

The sharpest self-observation in the register is not about a unit. Within ninety minutes, a gate
was found under-specified; the remedy written for it keyed its licence to a **single terminal
sample** of a 6.7×-spread series, which is the same class of error (naming a quantity without
naming how the quantity is read); and the correction of *that* was itself preceded by two wrong
statements about the same figure, each closer than the last. **The same figure was corrected three
times in ninety minutes, by two parties alternating, and the second and third corrections were each
produced by a party who had just been corrected.**

That is worth stating precisely because it is *not* a procedure. It is two agents with different
vantage points and no incentive to agree, reading the same live run for different reasons. It is
cheaper to describe than to institutionalise, and **the paper must not dress it up as a
mechanism.**

### 7.2 What the discipline caught only because a rule mandated the blind spot

The programme's contract requires evidence scripts to rebuild claims from curated JSON *"without
re-running anything"*. That clause has a real purpose: it stops a script silently re-running the
experiment and validating a fresh answer against fresh prose. **And it mandates that the script
cannot detect an error shared between the artefact and the script**, because the same unit wrote
both in the same hour. One recent script ran **31 checks, 0 failed** and **0 of the 31 recomputed
anything from a primary source** — verified by this unit at leg 414 by executing it (`31 checks, 0
failed`) and by reading its imports, which are `json`, `sys` and `pathlib` and nothing else.

**The unit was not free to do otherwise. It followed the contract exactly.**

> **A rule that mandates a procedure also mandates that procedure's blind spot, and the blind spot
> inherits the rule's authority — so it is defended instead of noticed.**

The clause is not withdrawn and is not called defective. What is recorded is that it is not
sufficient, and that the `N/N passed` line it produces means considerably less than it reads as.

### 7.3 The one class the discipline cannot touch at all

Every mechanism in this paper operates on **what is written into an artefact**: pre-committed
gates, evidence checks, corrections beside data, depth labels, `UNVERIFIED` markers. **Not one of
them touches what an agent concluded and carried forward unbanked.**

The record contains the case. Having just written the observation that a cheap quantity is
routinely substituted for an expensive property, the Conductor declined to *bank* an unlanded
number on exactly those grounds — and then **made the inference anyway, in prose, and reasoned from
it**, selecting subsequent work on the basis. The stated reading was that a continuation start was
approaching stationarity; the fuller series gives a fit of `ρ = −0.563` with a reversal in the last
1,000 iterations, and the value was still 43× threshold.

**Declining to bank a claim is not the same as declining to believe it.** The instruments that
caught everything else could not have caught this one: there was nothing to check. **Unbanked
conclusions are what select the next unit**, and they are outside the entire method. That is the
boundary of what is described here, and it is stated where a reader cannot miss it because it is
the first thing a referee should ask about.

### 7.4 Three gates amended mid-run, listed so the count is honest

`[CORRECTIONS.md §41]` (a `NO` branch that did not entail its reading), `[§44]` (a licence keyed to
a single sample of a high-variance series) and `[§53]` (a comparison across two truncations of a
divergent integral, replaced by a matched-truncation comparison). All three amendments are, in our
judgement, improvements; all three were placed *beside* the immutable committed gate text rather
than over it; **and all three were written by parties who could see data bearing on the outcome.**
§3.2 is the reason that last clause is in this paper.

---

## 8. The measured blind spots, and one measurement we could not trace

### 8.1 What an evidence check certifies

Every `*_evidence.py` in the repository was classified by whether it references any data file
**outside its own unit's artefact**:

| | count | share |
|---|---|---|
| evidence scripts | **49** | |
| reference no file outside their own unit's artefact | **32** | **65%** |
| reference at least one independent source | 17 | 35% |
| of the 32, do not recompute at all (pure field read) | 3 | |

**All four figures are `UNBANKED` — see §8.2 before using any of them.**

What the classification says is narrow and sufficient: a check that reads only the artefact its own
unit wrote **cannot detect a claim that is wrong in the artefact and in the script together**. It
still catches transcription errors, internal inconsistency, and prose quoting a figure the artefact
does not contain — all real, all caught here before. But **`N/N passed` is not evidence of anything
until every check carries its class**, and where a finding is load-bearing at least one check on it
must recompute from something the unit did not write, or the finding is `UNVERIFIED` however many
checks passed.

The pointed instance: the evidence script for one of the two units that measured the lane's central
premise FALSE — the largest adverse finding this programme has produced — is of the first kind. **It
re-derives its journal's numbers from its own artefact and reads nothing else.** The result survives
because a second unit reached it independently by another method, which is the cross-unit design,
not the evidence-check design.

The complementary case is entry 12 of §4 and it is the cleanest demonstration of the taxonomy in
the record: an independent-class check re-hashed PDF bytes and found the leg's **own** banked
manifest carrying a two-character transposition. **No re-read of the artefact could have caught it,
because both copies of the wrong string would have agreed.**

### 8.2 The number in this paper's own thesis that has no artefact behind it

**Disclosed here because the binding rule requires it and because it is embarrassing in exactly the
way this paper is about.**

`32 of 49` is quoted in the correction register, twice in this paper's own status document, and in
the docstring of a verifier's evidence script. **It appears nowhere in `writeup/data/`.** There is
no artefact, no classifier, no file list, and therefore no way for a reader — or for this unit — to
re-derive it. Under the rule that opens this paper, *every number cites the banked JSON field it
came from*, **`32 of 49` does not qualify**, and it is labelled `UNBANKED` at every appearance
above.

This unit attempted a re-measurement and reports it with the same caution it is applying to the
original. At leg 414 the repository holds **53** evidence scripts, not 49 — four have landed since
the measurement was taken, so the denominator has moved. Under a *cruder* classifier written for
this draft (any string literal naming a file other than the script's own artefact counts as an
outside reference, which over-counts independence because it also catches `.md` and `.py`
mentions), the split is **27 solo / 26 independent, 51% solo**.

> **We do not claim `51%` supersedes `65%`.** Different classifier, different date, and ours is
> the weaker instrument. What we claim is narrower and is the finding: **the headline is not
> currently reproducible from the record**, and a measurement that cannot be re-derived is in the
> same position as the `N/N passed` lines it was written to criticise.

Routed as a correction, not applied by this unit.

---

## 9. The two prospective catches, graded

**Catch 1 (stronger).** A rate was mis-derived by taking a numerator and a denominator from
different windows of a run — three times in twenty-four hours, in three different shapes, each
erring in the direction that flattered the reporter's schedule. A rule was written: *any reported
rate names the window of both its numerator and its denominator, and they are the same window.*
Hours later, in a different lane, on a different quantity, an ensemble's shard occupancy was
computed as finished work over wall × shards — the same error **with the sign flipped**,
work-in-progress dropped from the numerator and left in the denominator. **The rule fired before
the number was banked.** Corrected occupancy `92.6%` against `80.5%`, and two independent routes to
the price then agreed. This is the only entry in the register where a discipline demonstrably
generalised rather than merely recorded.

**Catch 2 (weaker, and the weakness is the point).** A cap was breached by 2,151 bytes through a
passing merge gate. The cap had been measured by hand, correctly, ninety minutes earlier. Nothing
measured it again, because nothing ever did: the merge gate did not check it, and the standing
clauses shipped in every brief that wave **did not mention the cap at all**. The catch came from
`wc -c` run during an integration audit **for an unrelated reason** — the fifth time in this
register that a defect was found that way, and the first time it happened *after* the pattern had
been named in this paper's own status document.

**What is transferable from catch 2 is not the byte counts.** It is:

> **A limit enforced by a person reading a number at a boundary is not enforced between boundaries,
> and every concurrent unit works between boundaries.**

The remedy is a mechanism rather than a resolution: a check wired into the merge gate that measures
every cap at the moment an artefact is written, treats a cap it cannot locate as a **FAIL**, and was
mutation-tested on four separate breaks. **It cannot tell a retirement from a deletion**, it says
nothing about whether the text is true, and it enforces limits that were themselves chosen by
judgement rather than measured. It makes a policy binding; it does not make the policy right.

---

## 10. Related work, at the depth reached — and what we could not reach

**The rule this section is written under.** A load-bearing claim may not rest on an abstract. Each
row states the depth actually reached by this unit at leg 414, with the fetch URL and a hash where
one exists, so the row can be checked rather than believed. Fetched copies live outside version
control (the repository does not redistribute PDFs); the URL and hash are the reproducible part.

### 10.1 Read at FULL TEXT by this unit

| source | used for | depth |
|---|---|---|
| Roodman, *Blind Analysis in Particle Physics*, PHYSTAT2003, `arXiv:physics/0312102` | §3.2; the practice we do **not** implement | **FULL TEXT**, PDF sha256 `27a4105316c7bcdc…`, 113,321 bytes, 2,704 words extracted |
| Nosek, Ebersole, DeHaven & Mellor, *The preregistration revolution*, **PNAS 115(11):2600–2606 (2018)**, PMC5856500 | §3.1; prediction vs. postdiction; deviations | **FULL TEXT**, 8,925 words extracted |
| Goldacre et al., *COMPare: a prospective cohort study…*, **Trials 20:118 (2019)**, PMC6375128 | §3.6; measured compliance with pre-registration | **FULL TEXT**, 13,323 words extracted |
| Eckhardt, Caglayan, Knight, Lee, McAllister, Vouk & Kelly, *An Experimental Evaluation of Software Redundancy As a Strategy for Improving Reliability*, **NASA TM-102613 (May 1990)**, NTRS 19900014642 | §3.4; independence of independently developed versions | **FULL TEXT**, PDF sha256 `5e9d610591638fe0…`, 8,298 words extracted |
| Sandve, Nekrutenko, Taylor & Hovig, *Ten Simple Rules for Reproducible Computational Research*, **PLoS Comput Biol 9(10):e1003285 (2013)**, PMC3812051 | §3.6; provenance rules | **FULL TEXT**, 4,447 words extracted |
| Melloni, Mudrik, Pitts, Bendtz, Ferrante, Gorska et al., *An adversarial collaboration protocol…*, **PLOS ONE 18(2):e0268577 (2023)** | §3.3; the strong form of impartial checking | **FULL TEXT**, PDF sha256 `2152d15a55f0286c…`, 16,393 words extracted |
| Hales et al., *A formal proof of the Kepler conjecture*, `arXiv:1501.02155` | §10.3; computer-assisted-proof norms | **FULL TEXT**, PDF sha256 `5cde7b6cb206af54…`, 11,629 words extracted |
| **NIST SP 800-53 Rev. 4**, control **AC-5 Separation of Duties** | §3.3; the codified control and its *anti-fraud* rationale | **FULL TEXT** of the control text, PDF sha256 `5460dfd68b7ca489…` |

### 10.2 Reached, but not at full text — stated as such

| source | what was reached | what was not |
|---|---|---|
| **IEEE 1012** (System, Software and Hardware Verification and Validation) | the standard's **public scope/description page**, quoted in §3.3 | **the standard itself is paywalled.** In particular its treatment of *technical, managerial and financial independence* was **not read**, and no claim in this paper rests on it |
| Altman & Bland, *Absence of evidence is not evidence of absence*, **BMJ 311:485 (1995)**, PMID 7647644 / PMC2550545 | citation confirmed at the landing page (journal, year, title, identifiers) | **the body was not obtained** — the PMC record is scan-only and both the XML and PDF routes returned 404/403. Depth: **CITATION**. The paper's use of it in §3 is attribution of a phrase, and nothing rests on the text |

### 10.3 Computer-assisted proof: the norm we are downstream of

The Kepler-conjecture history is the reason this programme labels every numerical result Tier 2 and
refuses to call any of it a proof. On the original submission:

> The delay in publication was caused by the difficulties that the referees had in verifying a complex computer proof.

and:

> In the end, the proof was published without complete certification from the referees.

`[Hales et al. 2015, §1]`. The published response — a decade-long formalisation project — is the
standard against which a repository of float64 residuals and pre-committed gates should measure
itself, and by that standard **nothing in this programme is a proof of anything and none of it is
close.** The relevant transfer is narrower and it is about *review*: the referees' difficulty was
not that the mathematics was wrong but that **the artefact could not be checked by reading it.**
Every mechanism in §3 is an attempt at the same problem one level down.

### 10.4 The construct we did not find a counterpart for — and why we still do not claim it

The programme's depth register grades every citation `ABSTRACT` / `FULL TEXT` / `RECOMPUTED` /
`SECOND HAND` / `UNREACHABLE`, and enforces a rule that a load-bearing claim may not rest on an
`ABSTRACT`. We found no published counterpart at a depth we could reach. **We do not claim it is
novel.** Three reasons, all of which a referee would raise:

1. The obvious neighbours — evidence-grading frameworks in systematic review, and the
   quotation-accuracy literature in medical bibliometrics — were **not read here**, and naming them
   is not reading them.
2. Failing to find a thing is not evidence it is absent. That is this paper's own §3 rule, and
   applying it selectively to our own contribution would be the exact defect §5 documents.
3. The construct's *value* in our record is not that it is a new idea. It is that applying it
   retrospectively found a load-bearing claim standing on an abstract **for 45 legs**, which is a
   measurement about this programme and not a contribution to the literature.

**Recorded as owed: a proper novelty check on the depth register has never been run.**

### 10.5 UNREACHABLE — recorded, not faked

Every one of these was attempted from this container during leg 414. None was obtained. **No
paywall was circumvented and no author, group, maintainer or list was contacted.**

| source | why it matters here | outcome |
|---|---|---|
| **ACM, *Artifact Review and Badging* (current policy)** | the closest institutional analogue to our artefact contract and its badge classes | **HTTP 403** on direct fetch and again through a second fetch path. `UNREACHABLE` |
| DeMillo, Lipton & Sayward, *Hints on Test Data Selection*, **IEEE Computer 11(4) (1978)** | the origin of mutation testing, which §3.5 says our check-mutation is an instance of | no open-access copy located; publisher paywalled. `UNREACHABLE` |
| Jia & Harman, *An Analysis and Survey of the Development of Mutation Testing*, **IEEE TSE (2011)** | the survey that would have supplied depth for the above | two institutional-repository URLs returned 404. `UNREACHABLE` |
| Knight & Leveson, *An experimental evaluation of the assumption of independence in multiversion programming*, **IEEE TSE 12(1) (1986)** | the canonical result behind §3.4 | no open copy; the host that once served it did not resolve. **Substituted at FULL TEXT by NASA TM-102613**, which is a primary report of the same experimental programme and is quoted instead |
| Klein & Roodman, *Blind Analysis in Nuclear and Particle Physics*, **Annu. Rev. Nucl. Part. Sci. 55 (2005)** | the review version of §3.2 | OSTI landing page timed out. **Substituted at FULL TEXT by Roodman 2003**, which is the same author's conference review |
| Mellers, Hertwig & Kahneman, *Do frequency representations eliminate conjunction effects?*, **Psych. Sci. 12(4) (2001)** | the canonical **adversarial collaboration** | repository handle returned **403**. `UNREACHABLE` |
| Kahneman & Klein, *Conditions for intuitive expertise: A failure to disagree*, **Am. Psychol. 64(6) (2009)** | the second canonical adversarial collaboration | no open-access location recorded. `UNREACHABLE` |
| Cowan et al., *How Do Scientific Views Change? Notes From an Extended Adversarial Collaboration*, **Perspect. Psychol. Sci. 15(4) (2020)** | a modern account of the practice | PMC HTML served a stub; the OA mirror returned a bot-check page; full-text XML 404. `UNREACHABLE` |
| Chambers & Tzavella, *The past, present and future of Registered Reports*, **Nat. Hum. Behav. (2022)** | registered reports specifically, as distinct from preregistration | no open-access location recorded. `UNREACHABLE` |
| ICMJE trial-registration statement (De Angelis et al., 2004) | the moment pre-registration became mandatory in medicine | no open copy located in the index searched. `UNREACHABLE` |

**The honest consequence.** §3 names **adversarial collaboration** as one of the three practices
this paper is most at risk of reinventing, and **three of the four canonical adversarial-
collaboration sources are `UNREACHABLE` from here.** The comparison in §3.3 therefore rests on one
reachable modern protocol paper. **That is a thinner base than the comparison deserves and it is
recorded as a debt, not written around.**

---

## 11. Threats to validity

1. **Self-report.** §1.3 item 2. The register counts filed catches.
2. **No counterfactual.** We cannot estimate what the disciplines prevented, only exhibit what they
   caught and what they did not.
3. **Survivorship in the corrections file.** A correction is filed when someone decides it is worth
   filing. Two of the twelve entries were filed by the party who had just been corrected on the
   previous one, which is evidence of a live adversarial dynamic and equally evidence that filing
   is discretionary.
4. **The prospective/retrospective split is a judgement**, made by the same parties. We have stated
   the criterion (§4) so that a reader can re-grade the table; we expect entry 9 to be the one a
   referee reclassifies.
5. **`UNBANKED` numbers.** §8.2 documents one in this paper's own thesis. There may be others; the
   audit that would find them has not been run, and saying so is cheaper than implying it has.
6. **A channel defect in the instrument that wrote this paper.** The tool-output channel through
   which these agents read files **silently drops words from long outputs**. It was first recorded
   at leg 411, where a unit's hand-retyped "verbatim" quotation contained a sentence its source did
   not; it was re-confirmed here at leg 414, where a 224-character quotation rendered through the
   channel came back with roughly a third of its function words missing while `len()` on the same
   string returned 224. **Every quotation in this draft was therefore script-injected from the
   source file, and none was typed.** A reader should treat any quotation in a document produced
   this way, by any agent, as unreliable unless the extraction path is stated. This is a defect of
   the harness, not of the model, and it is the single most under-appreciated hazard we encountered.
7. **Anonymity and scope.** This describes an ongoing programme with a live prize target and a
   standing hold on outreach. What may be said publicly is an operator decision, not a drafting
   one, and this draft is not cleared for circulation.

---

## 12. What we would tell someone building one of these

Each rule is followed by the entry that forced it. **None of them is new; what is new is the
evidence of what it cost not to have them.**

1. **Classify every check; do not count them.** A check that reads only its own unit's artefact
   certifies internal consistency and must be labelled so. `N/N passed` is not evidence until every
   check carries its class. *(§8.1; and §8.2, where the measurement supporting this rule turned out
   not to be reproducible.)*
2. **When a rule prescribes the *form* of a check, read the form for what it makes impossible to
   detect, before congratulating the check for passing.** *(§7.2.)*
3. **A pre-committed gate must state, for each named outcome, the condition under which that outcome
   *entails* its stated reading.** Naming both directions is necessary and is not sufficient.
   *(§7.4.)*
4. **A control that cannot fail is worse than no control.** Before banking a passed control, state
   what result would have failed it and check that the experiment could have produced that result.
   *(§5.3 — the cap sweep whose range sat inside a false plateau.)*
5. **When a refinement study and a budget study measure the same objective, divide one by the other
   before reporting either.** *(§5.1. The comparison costs one line and was not done by the unit,
   the integrator, or the first verifier.)*
6. **Show an objective is finite on its own trial space before quoting any minimum of it**, and
   evaluate it at a point the optimiser has never visited before believing an agreement between two
   implementations. *(§6. A verification performed only at minimisers verifies almost nothing.)*
7. **When something is found divergent or defective, ask the sign of the error before asking which
   results are wrong.** A defect with a known sign can leave every conclusion standing while
   destroying every number, and both facts must be reported. *(§6.1.)*
8. **Any reported rate names the window of both its numerator and its denominator, and they are the
   same window.** *(§9, catch 1 — the only rule in this record that demonstrably generalised.)*
9. **A limit that is not mechanically checked at the moment the artefact is written is a description
   of intent, not a constraint.** *(§9, catch 2.)*
10. **When a wrong string is found in a banked artefact, the search is not finished until it has
    been run against the code that produces the artefact.** *(§7, row 4.)*
11. **A commit subject is an index into the record.** Sweeping another agent's live files under a
    subject that does not name them silently reassigns their provenance.
12. **Do not let an agent retype a quotation.** Inject it from the source, mechanically, and fail
    loudly on an unresolved token. *(§11 item 6.)*
13. **And the one we cannot turn into a rule.** Most of what was caught here was caught by someone
    opening a primary artefact for an unrelated reason, with a different vantage point and no
    incentive to agree. We have not found a way to institutionalise that, and we are suspicious of
    any paper — including this one — that claims to have done so.

---

## 13. Status of this document

**Draft.** Not submitted, not cleared for circulation, and **not citable by any unit of the
programme it describes.** Its numbers are traceable to the fields named beside them; the ones that
are not are labelled `UNBANKED` and routed as corrections. Its quotations were injected by
`inject_quotes.py` from the sources listed in §10; the ten sources in §10.5 were attempted and not
obtained, and are recorded as `UNREACHABLE` rather than dropped.

**The companion document `FINDINGS.md` is the second output of this leg, and on the evidence of the
drafting it is the more valuable of the two.**
