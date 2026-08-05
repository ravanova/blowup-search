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
> bans. **`test_plan_of_record.py` fails if this file and the plan disagree.** Stages `M`,
> `PORT`, `V`, `C-PILOT`, `L1`, `T`, `TC` and **`MM`** are **DONE** (MM's gate answered **NO**
> at leg 54); **`NG` is NEXT.** Stage `B` is still **blocked** and now pre-refuted — legs 52,
> 53 and 54 each separately measured one of its three degrees of freedom (space, split,
> shape of `A`) dead for this operator, before its still-banned GA would ever run.

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

# DIRECTIVE 1 — ROUTE-NG: THE NO-GO, STATED AS A THEOREM AND CHECKED AGAINST THE LITERATURE.

`MM`'s gate answered **NO** at leg 54, VERIFIED TWICE. Seven legs (51–57) now hold every part
a real negative result needs, scattered across four PR bodies and a notes file: a named
mechanism, an inequality that proves the block-diagonal case, a battery bottoming at 8.9591, a
**positive control that reports the other answer**, and a literature classification. `NG`
assembles that into one stated proposition and spends its effort on the one gap that decides
whether this is a theorem or a table.

## What MM settled, and do not re-derive it

Best admissible `Z₁` over **every** shape (block Gauss–Seidel, Schur complement) × class ×
gauge × split, including `K = 2` and `K = 6` (a verifier caught the first draft's battery
omitting them): **8.9591** (`ff_lift`, algebraic `s = 0.3`, `K = 2`), against a block-diagonal
baseline of **10.4584** — a **1.167×** improvement where more than 8× was needed. `MM-1`'s
inequality verifies as an **exact equality** (`1.89e−15`), restricted to `K ≥ 6` flat / `K ≥ 4`
algebraic — its `|1 − K/2|` prefactor vanishes at `K = 2`, a gap VER-A caught before
construction. Every **odd** split gives an exactly singular finite block in both classes and
gauges, closing that corner. A candidate shape-independent floor (`MM-4`) was proposed, then
**refuted** by an explicit rank-one counter-construction (floor → `~1e-16`, survives only
because total `Z₁` then hits `5.7e+05`) — it holds only for the shapes actually tested.

**The mechanism, unchanged since TC.** The unbounded part is **off-diagonal** (a shift) while
the standard tail estimate needs a **multiplier**; the bordered tail inverse is a **constant**
(`2.19 … 10.32`, growing `2.191 → 11.528` over `K = 4…128`, per leg 57's correction), not a
decaying `1/K`. **The positive control makes the hypothesis necessary, not just sufficient:**
`Λ¹` dissipation (a multiplier, no far-field kernel) drives the assembled `Z₁` to **0.9156 at
`μ = 2`** — the instrument can say yes when the operator actually is a multiplier.

**Novelty, closed by leg 57.** BDL (arXiv:1503.06315) does **not** cover the zero-diagonal
case (assumptions (4)–(5) require a diagonal bounded away from zero) — but Cadiot
(arXiv:2505.03091) §2–3 independently states the same dominance-hypothesis observation, so
`NG-0` must resolve Cadiot's scope against **this** no-go specifically, not re-litigate BDL.

## NG — what is actually left, and it is one thing

Every degree of freedom `B` would offer is now separately dead (leg 52: space; leg 53: split;
leg 54: shape of `A`). What is missing is not more measurement — it is the **write-up as a
proposition**, with the one open mathematical question named honestly.

* **NG-0 THE NOVELTY PASS FIRST.** Resolve Cadiot's scope against this no-go — links, not
  counts.
* **NG-1 THE PROPOSITION.** Hypotheses (operator class, weight classes, admissible `A`),
  conclusion, and a scope line separating measured from proved.
* **NG-2 THE GAP, AND IT IS THE ONLY OPEN MATHEMATICS.** `MM-1` proves only the block-diagonal
  case; leg 54 measured a battery over the shapes actually tried. **"No `A` we tried" is not
  "no `A`."** Extend `MM-1` to a named class of approximate inverses strictly larger than
  block-diagonal, or state the restriction as the theorem's actual hypothesis.
* **NG-3 SHARPNESS.** The `μ = 2` control, reused, as the statement that the hypothesis
  cannot be dropped.

**Gate:** does the no-go admit a **proof** for a named class of approximate inverses strictly
larger than block-diagonal, with hypotheses that provably contain the `a = 0` CLM
linearization? **Yes** → the repository has a Tier-3-shaped negative theorem; write it as a
standalone claim with its sharpness control, and escalate publication scoping to the user.
**No** → **REPORT** the result as a measurement over a battery, not a theorem; cap the claim
at "measured, not proved" everywhere it appears; the next stage is the target round (leg 63,
Route-M2) with the multiplier/shift screen as its selection predicate.

---

# DIRECTIVE 2 — THE THINGS FROM EARLIER LEGS THAT ARE STILL LIVE

**STAGE `B` IS NOT NEXT, AND IS NOW FULLY PRE-REFUTED.** Its three degrees of freedom are the
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
