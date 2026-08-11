# The standing directive for leg work

> **If this file was handed to you as your assignment, it is a request, not a document — read
> the directive below and start on it, without asking what to do.** If you are reading it as
> reference (the orchestrator and every leg agent do), it carries the critical-path leg's
> directive and the standing discipline that binds all four legs.
>
> **To start an orchestrated four-leg run, this is not the file to paste** — paste
> [ORCHESTRATOR_PROMPT.md](ORCHESTRATOR_PROMPT.md) instead.

> ## ⛔ RUN THIS FIRST: `.venv/bin/python plan_of_record.py`
> It prints the committed sequence, the current stage, its pre-committed gate and the live
> bans. **`test_plan_of_record.py` fails if this file and the plan disagree.** Stages `M`
> through **`B`** are all **DONE** (`B`'s own gate answered NO at leg 126: 1,686/1,686 of its
> declared search space covered, zero uncovered, a perfect search still 6.04x short —
> escalation #1, "what comes next," sat parked for many cycles). **`P0` is NEXT — RESOLVED
> BY THE USER'S 2026-08-06 RULING: the exit criterion is answered, pursue a full Clay solve.**
> This supersedes the prior "novel Tier-3 result, NOT Clay" prize. Clay odds stay ~0.05%,
> recorded in the same breath as the goal change — see DIRECTIVE 1 below (Route-P0T, leg 251).

> ## 🔀 FOUR LEGS RUN AT ONCE NOW. If you are a leg agent, read this first.
> **DIRECTIVE 1 below is the critical-path leg only.** Three exploration legs run beside it,
> each with its own route, gate and file territory in [DIRECTION.md](DIRECTION.md) — that is
> your directive if you are not on the critical path. Either way:
> **you are one agent doing one whole leg**, novelty pass to quartet. Legs are not sharded.
> - **Commit messages start `Leg <N>: <ROLE> — `** (`Leg 0:` for repo-wide work).
> - **Stay inside your declared file territory.** A diff outside it fails the merge gate.
> - **The five shared ledgers are integration-owned — do not edit them.** Write
>   `experiments/journal/leg_<N>.md` and `writeup/novelty/leg_<N>.md` instead of
>   `experiments/JOURNAL.md` and `LITERATURE_CHECK.md`; never touch `plan_of_record.py`,
>   `CONTINUATION_PROMPT.md` or `PHASE2_P2_NOTES.md`. The orchestrator folds them in.
> - **Your gate answer goes in your PR body in its pre-committed wording.** You do not update
>   the plan yourself — the orchestrator applies the branch the gate already prescribed.
>
> Full contract: [ORCHESTRATION.md](ORCHESTRATION.md). Everything below applies to every leg.

---

# DIRECTIVE 1 — ROUTE-P0T: PHASE 0, TARGET SELECTION UNDER THE CLAY GOAL.

**Escalation #1 is RESOLVED.** Stage `B` answered its own gate NO at leg 126 (1,686/1,686 of
its declared search space covered, zero uncovered; a perfect search still lands 6.04x short)
and the committed sequence sat EXHAUSTED for many cycles with no successor. **The user's
2026-08-06 ruling answers "what comes next" by changing the goal itself: pursue a full Clay
solve**, superseding the prior "novel Tier-3 result, NOT Clay" prize. The user explicitly
accepts this means building seriously heavy code, and explicitly does NOT lower the
evidentiary bar for the change — Clay odds stay **~0.05%**, recorded in the same breath as
the goal change, and no output is ever described as movement toward Clay unless a link of the
L1→L4 chain actually moves. That rule is easier to erode under a Clay-directed programme, not
harder, and it does not relax.

## The technical framing this leg (and every Phase 0/1 leg after it) must work inside

- **Direction (a) (global regularity) is closed** to anything search-/certificate-shaped:
  Tao's averaged-NS supercriticality barrier means energy methods plus the preserved
  algebraic structure are provably insufficient. Only direction (b) (blow-up) is in scope.
- **Wall 2, corrected**: its naive form (spatial dimension is the barrier) is FALSE — van den
  Berg–Williams certified genuinely 3D Ohta–Kawasaki stationary states in 2019. The real
  barrier is TIME-DEPENDENT singularity formation, not dimension. Every work stating a 3D
  singularity theorem *with* a certificate supplies the 3D-ness via a 2D reduction (Chen–Hou)
  or a spherically-symmetric ODE profile (BCG → CGSS) — never via the certificate itself.
  This leg must state explicitly which side of that line its own proposal lives on.
- **The ansatz is constrained**: Nečas–Růžička–Šverák and Tsai exclude nontrivial
  exactly-backward-self-similar 3D NS blow-up under the relevant decay — the target must be
  discretely self-similar, unstable-self-similar with a finite unstable spectrum, or
  non-self-similar. `arXiv:2604.09949` is the recorded negative-control citation for what
  happens when this is missed.
- **The missing rung is viscous certification, strictly on the Clay path.** Leg 174's own
  occupancy matrix has the Grade-A/fluid cell empty "for want of a target, not a method"; leg
  242 confirms nobody has filled it since, and leg 309 defended the cell against a claimant
  (`arXiv:2604.09949`, refuted). **State the gap at its measured width, not wider.** What is
  empty is the Grade-A/**fluid** cell: no published work applies interval arithmetic to a
  dissipative *fluid* equation's own self-similar object. Grade-A dissipative certification
  **does** exist off the fluid axis — Dähne–Figueras CGL (`arXiv:2410.05480`), reproduced
  row-for-row by leg 316, and Breden–Chu's viscous Burgers. The older phrasing here — "no
  certified viscous blow-up exists in any model, in any dimension" — was an **over-read
  (closure #5)** and was corrected on 2026-08-11 per the user's external-review packet;
  leg 174's own banked data refutes it in leg 174's own words. **The Phase-1 rationale is
  unchanged and never depended on the wider claim:** if it cannot be done for a dissipative
  fluid equation in 1D, 3D NS is not a question of compute.

## What this leg does, and the sequencing that binds every leg after it

**Do not build the 3D solver first.** This repository's own Route-A discipline — two unknowns
are never debugged simultaneously — applies with more force here than anywhere it has been
applied before. The programme is Phase 0 (this leg: which object, which ansatz, survives the
NRS/Tsai screen and every already-banked dead end) → Phase 1 (the viscous rung: can a viscous
blow-up be certified in *any* model? — does not need the 3D solver) → Phase 2 (the 3D
near-singular viscous solver, `PLAN.md` Stage 4, user-authorized but sequenced strictly after
Phase 1 reports, since a 3D candidate with no certification story reproduces Hou–Luo 2013 and
answers nothing).

**Gate:** does a target+ansatz combination survive BOTH the NRS/Tsai screen and a check
against every already-banked dead end this repository's own record contains (L1's death in
three realizations: legs 54/56/163/176/182; stage B's own exhaustion, leg 126; the space-axis
synthesis, legs 179/186)? **Yes** → name the object and ansatz precisely, state what a
certificate for it would need to show, state whether it is fluid/vortex-dynamics-adjacent
(bearing directly on Phase 1) — escalate as the Phase 1 candidate, do not attempt
certification under this leg's own authority. **No** → report precisely which screen killed
every candidate tried; target selection itself needs more candidates or a different screen
before Phase 1 can even be posed — report honestly, this is itself a real and useful negative.

**Ban review accompanying this ruling** (neither lifted unilaterally, both recorded in
`plan_of_record.py`'s `BANNED` list directly): the DSS ban is kept as-is (an optional light
scoping leg on whether its "expensive entrance" was excluded for cost or substance is
available if wanted); Stage V's ban is re-posed, since its own "needs L1 first" lift
condition had become unliftable (L1 is dead in three realizations with no fourth candidate) —
replaced with a forward-looking wording naming the machinery, not the model, as what's dead.

Full spec: `DIRECTION.md` leg 251 (Route-P0T).

---

# DIRECTIVE 2 — THE THINGS FROM EARLIER LEGS THAT ARE STILL LIVE

**STAGE `B` IS DONE (gate NO, leg 126), NOT NEXT — `P0` is next, per DIRECTIVE 1 above.** `B`
was fully pre-refuted before its own closure audit ran. Its three degrees of freedom are the
space (leg 52: one weight constant's 5186× effect was in the border rows, not the space — pin
`c_l` and it collapses to 0.56×), the operator split (leg 53: `K/2` for every choice), and the
shape of the approximate inverse (leg 54: best improvement 1.167× where >8× was needed). All
three are separately measured dead for this operator, and its GA is still banned besides
(C-PILOT's viability gate answered NO 4/6, twice, and no repair has passed it).

**THE TARGET WAS NEVER THE PROBLEM.** Leg 55 measured `HL_S2_nonsymmetric`'s norm directly for
the first time: finite `ℓ¹_w` at `s = 0` (margin +0.394) and `s = 0.3` (margin +0.094),
divergent only at `s = 1` — which is exactly the class the operator is least bad in (leg 51's
own finding). So "the target was never in the space" is **not** available as an explanation for
legs 52–54's failures; the block-coupling/shape finding stands as the operative reason.

**THE (H,D) CONSISTENCY GAP IS NOW MEASURED, INDEPENDENTLY OF THE `ℓ¹`-FOURIER LANE.** Leg 56:
in the sup-norm collocation realization, the defect exceeds `L1` step one's admissible `τ` by
`1.85e7×` (derivative) / `2.04e11×` (Hilbert, corrected mechanism after review) at `n = 801`.
The collocation realization cannot carry `L1` either.

**THE CLAY CHAIN CANNOT BE CLIMBED AS WRITTEN** (`PHASE2_P2_NOTES.md` §24): `L1` a certified 1D
toy profile — the only movable link, now dead in both the coefficient-basis and collocation
realizations; `L2`/`L3` — Chen–Hou proved both; `L4` — Clay, out of reach by **Wall 2**. Stage
`V` was closed by its own novelty gate at leg 48; its ban lifts only "if re-posed for a fluid
transport model, which needs `L1` first" — and `L1` is now dead in both realizations, so
whether that condition can ever be met is an open question for the user (parked in
`PROGRESS.md`).

**FLAG STATUS.** Leg 52's search-index flag **STANDS**. The BDL flag is **CLOSED** (assumptions
(4)–(5) require a diagonal bounded away from zero; not on their own future-work list) — but
leg 57 found Cadiot (arXiv:2505.03091) independently states the same dominance-hypothesis
observation, so the ban on re-claiming leg 51's finding at full strength stays up for a
**different, stronger** reason than the one that just closed.

---

# DIRECTIVE 3 — WHAT AN EXPLORATION LEG OWES (it is the same debt)

Three of the four live legs are **not** on the critical path. Nothing about that is a
discount. An exploration leg owes exactly what a critical-path leg owes:

**A gate with both branches written down before it starts.** Not "see whether this works" — a
question ending in a question mark, a yes-branch that says what happens next, and a no-branch
that says what *stops*. It is in `DIRECTION.md` before the agent is spawned, and it is answered
in its pre-committed wording. A leg that discovers its gate along the way has no gate.

**The novelty pass first, and the log committed** — `writeup/novelty/leg_<N>.md`, **links, not
counts** (leg 53 logged counts, could not be audited, and was withdrawn).

> **Novelty-pass calibration (user steer 2026-08-07 §0a, recorded by the DM 2026-08-11,
> propagated here by the orchestrator).** On this project's measured-vacated ground (four
> author groups censused: Breden–Chu, Dähne–Figueras, BCG, ALS — each has either left the
> object or stayed and left certification; nobody is in the cell), pre-emption risk is
> measurably low. The pass stays MANDATORY — review its record: what it actually caught was
> prior art, mostly years old (Gallay's Handbook, EGM Prop 2.1, HQWW24's first integral). So
> on vacated cells, weight queries toward locating OLD prior art and stop spending cycles on
> "has anyone done this in the last six months." The one true scooping (Route-F, eleven days)
> happened on ACTIVE ground — if your leg's cell is active, the recency check stays at full
> weight.

> **Control your instrument before you trust it** (measured on this run; propagated here by
> the orchestrator, 2026-08-11). Search tools on this project have lied in three measured
> ways, and an absence claim is only as good as the instrument that produced it.
> - **MF1 — spelling variants.** A paper sitting in this project's target cell spells itself
>   `Navier--Stokes` with a **LaTeX double hyphen**, so a plain search string silently misses
>   it. Search hyphenated, double-hyphenated and unhyphenated forms, and `self similar`
>   alongside `self-similar`.
> - **MF2 — bank links, not counts.** Leg 174 banked counts; **ten of its links are now
>   permanently unrecoverable.** Bank identifiers.
> - **MF4 — compound author-name queries are a false-negative generator (adopted
>   2026-08-11, DM cycle 9b, three independent confirmations: legs 326, 330, 323).**
>   `au:"Chae-Tsai"`, `au:"Breden-Chu"` and group-name forms like them return **zero**
>   even when both authors are censused and co-published — the endpoint does not expand
>   a hyphenated or spaced two-name string into "both authors," it matches a single
>   author field literally. **Never bank a zero from a compound author-name query.**
>   Control it with the per-author `AND` form (`au:"Chae" AND au:"Tsai"`) before trusting
>   an absence.
> - **MF1 is sharpened to per-query AND per-field (DM cycle 9b).** Dash-normalization is
>   not a fixed property of the endpoint — it is measured per query and per field. Leg 323
>   found `abs:` IS dash-normalizing (double-hyphen/en-dash/em-dash/spaced forms all return
>   identical id sets to plain hyphen, 16/16) while `au:` is NOT (`au:"Gomez-Serrano"` 47 vs
>   `au:"Gomez--Serrano"` 0). Do not generalize a dash-robustness finding from one field to
>   another, or from one query to the whole endpoint (leg 326 found MF1 held per-query, not
>   globally, on a different endpoint) — re-measure it for the field and query you're using.
> - **An implausible zero is a broken instrument until proven otherwise — but the rule is a
>   TEST, never a prohibition.** Run a positive control (a query that must return results)
>   and a negative one. For a suspicious zero from a compound query, query each phrase singly,
>   confirm both are non-empty, then check the compound form against a control pair you know
>   intersects. **If the controls pass, the zero is a MEASUREMENT and you bank it as absence.**
>   Do not discard zeros by rule: this project's Phase-1 premise *is* an absence claim about a
>   cell, so a habit of throwing zeros away corrupts the record in the direction that matters
>   most, and silently — a leg that discards a zero reports nothing unusual.
> - **This applies when the instrument is an INSTRUCTION, including one from the orchestrator
>   or the Decision Maker.** On 2026-08-11 the orchestrator relayed a rule ("the arXiv
>   endpoint returns zero for any two ANDed quoted phrases") that was a false generalisation
>   from one leg's six zeros. **Leg 314 ran the control instead of taking it on authority**
>   (`"self-similar" AND "blow-up"` → 251 results) and the error was retracted within the
>   cycle. You have that licence; use it.

**Assess before you run anything long** (user instruction, 2026-08-11, binding on every agent).
**Before running a script you expect to take longer than 10 minutes, assess it for performance
and try to improve it first.** Estimate the runtime before you launch. If the estimate exceeds
~10 minutes, find the hot path and cut it down before running — vectorise, cache, reuse what
`capabilities.py` already provides, and shrink the grid or the sweep to the smallest size that
still answers your gate in its pre-committed wording. Record in your journal: the estimate, what
you changed, and the achieved runtime. If a long run is genuinely unavoidable to answer the
gate, **say so explicitly with the reason and the measured cost** rather than silently spending
the time. This is not a licence to weaken a gate to make it cheap — if the cheap version cannot
answer the gate as written, the run is unavoidable and you say so.

**The full quartet, negative results included** (`ORCHESTRATION.md` §6). Runner, curated JSON
with every number the prose quotes, BLOG **and** TECHNICAL, registered figure. Three of the
last four legs answered NO and all four shipped the same artifact. That is the point.

**The bans, all of them.** `.venv/bin/python plan_of_record.py` prints the ones in force.
Being on a different route does not exempt you from a ban raised on another one — the bans are
about this repository's failure modes, not about a particular stage.

**And the honest ceiling.** The queue is ordered by which legs *could* touch a link of the
L1→L4 chain. **That ordering is a choice of what to try. It is never a claim that anything
moved.** If your leg's result reads like movement on the chain, that is escalation #3 in
`ORCHESTRATION.md` §8: say so in your PR body, park it, and let the user decide. Do not write
it into prose.

---

# STANDING DISCIPLINE (applies to every leg)

Gate the **operator**, not the agreement. Report a **magnitude**, never a boolean. **"Small" in
which norm?** **Name the realization** (70). **Gate the quantity the measurement divides by**
(67). **Report the SHAPE of a ladder, not its endpoint** (72). **When a quantity has no
referent, say so instead of bounding it** (73). **Test all the suspects at once** (74). **Two
defects in the same problem are not the same defect** (75). **Keep the negative construction in
the artifact** (76). **A check that is not executable decays at the rate of memory** (68). **A
known-answer probe has a WINDOW** (84). **Re-measure your own headline before building a stage
on it, and ablate the MECHANISM and not just the effect** (85). **A rigorous bound dominated by
its own EVALUATION error is a statement about the code** (86). **A certification method has a
SHAPE, and the shape is a property of the OPERATOR: multiplier or shift?** (87). **The minimum
of a failure curve is not where to repair it** (88).

**NEW — LESSON 90. A CONTROL THAT CANNOT COME OUT DIFFERENTLY IS NOT A CONTROL, AND THE
TELL IS THAT ITS NUMBERS ARE *IDENTICAL*.** Leg 53 reported "the coupling is 546.57 for all
four border directions" as the sharpest form of its result. It was computed from two objects
neither of which references the border: a tautology of the code, presented as evidence. Four
identical numbers should have read as a bug, not as a finding. **Before quoting a control,
ask what would have had to change in the code for it to report the other answer** — and if the
answer is "nothing", wire the varied quantity through until there is one.

**NEW — LESSON 89. A TERM THAT DOES NOT EXIST UNTIL YOU ASSEMBLE CANNOT BE BOUNDED BY FIXING
THE TERMS THAT DO.** Legs 51–52 measured four terms of a certificate one at a time: three were
exact or tiny and the fourth was repaired. Assembling them produced a *fifth* quantity — the
coupling between the two blocks of the approximate inverse — which is 43 where it needs to be
under 1, and which no amount of further work on the original four can touch. **Assemble early,
even with placeholder constants: the terms you have not written down yet are the ones that
decide.** The corollary is positive, and leg 53 is the case: the assembly took one leg, and it
corrected the reading of two.

**PROCESS RULES THAT KEEP EARNING THEIR PLACE.** Before pushing: regenerate the data, rebuild
the figure, **check every number in the prose against the JSON**. **Run the novelty pass BEFORE
the construction, and commit the query log** — it has now closed one stage (48), narrowed four
(49, 51, 52, 53) and cleared one standing flag (53). **A negative result needs a positive
control that can report the other answer** — leg 53's dissipative control reaching `Z₁ = 0.9156`
is the template — and a positive result needs **negative controls that can fail**. **When a
control contradicts the mechanism, suspect the control's REALIZATION first**: leg 53's first
positive control failed because it bordered an *already invertible* dissipative tail with its
near-null pair, which is the wrong operator, not the wrong answer. **Run the ablation battery
before naming a suspect.** And **grep `capabilities.py` before building anything**.

**AND ONE MORE, EARNED THE HARD WAY THIS SESSION.** **A GROWTH RATE YOU CITE MUST BE
MEASURED ON THE MATRIX YOU ACTUALLY BUILT.** Leg 53 explained its own `‖Γ⁻¹‖` by citing leg
51's numbers for a *different* (unaugmented) matrix — 23× smaller at `K = 64` — and got the
exponent wrong (`K` instead of `K²`) and the responsible factor wrong (`K/2` instead of `2`).
The conclusion survived; the mechanism did not. **When a quantity has a suspiciously tidy
closed form (`2(K²−1)`, `4(K−1)`), that is the signal to check what produced it.**

**NEW — LESSON 91, FROM EXTERNAL REVIEW (2026-08-06). "MEASURED DEAD" WITHOUT A NAMED
REALIZATION IS NOT AN ADMISSIBLE GATE ANSWER.** Three banked closures were found over-read
after the fact: leg 165 (legs 111/141's zero-width window turned out to be a property of one
trial space, not the operator); leg 180 (the a*≈0.5–0.55 boundary was stated without its
measured domain across 15 documents); leg 185 (leg 125's Object-B stall was a solver
artifact, not non-existence). **Every leg reporting a negative result must name, in the
gate's own answer wording, the exact realization, trial space, or basis the negative holds
in** — "measured dead" alone, with no realization named, is not a complete gate answer and
must be sent back for that naming before the finding is banked.

**BANS ARE MACHINE-READABLE.** `plan_of_record.py` carries every ban with what lifts it;
`.venv/bin/python plan_of_record.py` prints the ones in force. New this cycle: **do not repair
`B`'s three degrees of freedom (space, split, shape) — all three are separately measured dead**;
**do not build further `ℓ¹`-Fourier or collocation machinery for this operator before `NG`'s
gate answers**; **do not re-claim leg 51's methodological finding at full strength — Cadiot
independently pre-empts it, a different reason than the BDL one that just closed.**

**CLAY.** Odds remain **~0.05%** behind Walls 1 and 2.
In 57 legs, **no link of the L1→L4 chain has moved.**

---

*Updated 2026-08-05 (session close). **THIS SESSION CLOSED MM (NO), MEASURED THE TARGET'S NORM
(YES), MEASURED A SECOND L1 GAP (NO), BANKED THE SHAPE DICHOTOMY (NO), AND OPENED `NG`.***

**(1) `MM` ANSWERED NO, VERIFIED TWICE.** Best admissible `Z₁` over every shape/class/gauge/
split: **8.9591** vs block-diagonal baseline **10.4584** (1.167×, needed <1). A verifier caught
the first draft's battery omitting `K=2`/`K=6` (true number, not the wrongly-reported 32.75/
45.36) and refuted an over-claimed "shape-independent floor" by explicit counter-construction.
Both fixed before merge.

**(2) THE TARGET WAS NEVER THE PROBLEM (leg 55, gate YES).** `HL_S2_nonsymmetric` has finite
`ℓ¹_w` norm at `s=0`/`0.3`, divergent only at `s=1` — narrowing, not falsifying, the ban-list
clause. "The target was never in the space" is retired as an explanation for legs 52–54.

**(3) THE COLLOCATION REALIZATION IS ALSO DEAD FOR `L1` (leg 56, gate NO).** The `(H,D)`
consistency defect exceeds the admissible budget by `1.85e7×`/`2.04e11×`. Both named gaps in
`L1` step one's collocation realization now have independently-verified magnitudes.

**(4) THE SHAPE DICHOTOMY IS BANKED AS AN EXECUTABLE LEDGER (leg 57, gate NO).** No published
certificate has an off-diagonal unbounded part with a non-decaying tail inverse (4 papers,
15/15 gates). Corrects legs 52–53's "constant 2.19–10.32" to a growing ladder (`2.191→11.528`).

**(5) `NG` OPENS.** With `B` pre-refuted on all three degrees of freedom, the Decision Maker
(under the user's pre-delegation) chose to state the seven-leg negative as a proposition rather
than jump to `B` or a fresh target round — see DIRECTIVE 1 above. This is escalation #1;
reversible.

**NOVELTY: BDL flag closed, replaced by a stronger Cadiot-based reason for the same ban. No
link of the chain moved.**
