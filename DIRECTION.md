# DIRECTION — the leg queue

**Owner: the Decision Maker (Opus 5). No other agent edits this file.**

This is the Decision Maker's durable state. It exists so a DM whose context has bloated can be
discarded and recreated from the file instead of re-derived from the whole repository.

It is **not** `plan_of_record.py`. The plan carries the committed sequence and exactly one
stage marked `NEXT`; this file carries the *exploration* routes running alongside it. Promoting
a route from here into the plan's committed sequence is escalation #1 in `ORCHESTRATION.md` §8
and needs the user.

---

## Status

**Cycle of 2026-08-05 closed. All four dispatched legs landed; three answered NO, one YES.**

| Leg | Route | Gate answer | What it settled |
|---|---|---|---|
| 54 | MM (critical path) | **NO** | Best admissible `Z₁` over every shape / class / gauge / split: **8.9591**, against a block-diagonal baseline of **10.4584** — a 1.167× improvement where it needed to go under 1. No shape of approximate inverse closes it. Fires the pre-committed no-branch: **stop building `ℓ¹`-Fourier radii-polynomial certificates for inviscid self-similar transport.** |
| 55 | NB | **YES** | `HL_S2_nonsymmetric`'s compactified coefficients decay as `k^{−1.396}`; `ℓ¹_w` norm finite at `s = 0` and `s = 0.3`, divergent at `s = 1`. The ban clause asserting the target has no finite norm was **narrowed, not deleted**, on user authorization. |
| 56 | TN | **NO** | The `(H, D)` consistency defect exceeds `L1` step one's admissible `τ` by **1.85e7×** (derivative) and **2.04e11×** (Hilbert, corrected mechanism). The narrow reading of the machinery ban was confirmed by the user, so this result banks normally. |
| 57 | XS | **NO** | No published radii-polynomial certificate has an off-diagonal unbounded part with a non-decaying tail inverse; banked as an executable ledger (15/15 gates, 4 papers). BDL *does* publish a non-block-diagonal approximate inverse but requires a diagonal bounded below, so it does not extend to the zero-diagonal case. Leg 57 also flags **Cadiot arXiv:2505.03091** as independently pre-empting leg 51's methodological claim. |

**Read together, that is one finding, not four.** Both realizations of `L1` are now measured
dead — the coefficient basis by 54, the collocation basis by 56 — while 55 says the target was
in the space the whole time and 57 says nobody has published the obstruction. The object we
wanted was reachable; the *method* is not, and the reason is now characterized rather than
suspected.

Last leg number used: **57**. **Queue items renumbered:** the previously-queued-but-never-
dispatched WV / PQ / KA (drafted as 58 / 59 / 60) are now **59 / 60 / 61**, because leg **58**
is the new critical path. Use the numbers as written below.

---

## THE `NEXT` CALL — recommendation to the orchestrator

**Mark stage `NG` as `NEXT` in `plan_of_record.py`'s SEQUENCE.** It is a new stage, sitting
after `MM` and before `B`. This is escalation #1 (a route entering the committed sequence), and
the user pre-delegated this specific call — "whichever pursues our goals best" — to whoever
holds the context.

**`NG` — THE NO-GO, STATED AS A THEOREM AND CHECKED AGAINST THE LITERATURE.**

Seven legs produced a coherent negative with every part a real result needs, and all of it is
currently scattered across four PR bodies and a notes file: a named mechanism (the unbounded
part is off-diagonal and the bordered tail inverse is a constant, not a decaying multiplier);
an inequality that proves the block-diagonal case (MM-1); a battery over shapes, classes,
gauges and splits bottoming at 8.9591; a **positive control that reports the other answer**
(`Z₁ = 0.9156` at `μ = 2`), which makes the hypothesis *necessary* rather than merely
sufficient; and a literature classification saying the case is unpublished. `NG` assembles that
into one stated proposition with explicit hypotheses and an honest scope line, and it spends
its real effort on the one gap that decides whether this is a theorem or a table: **leg 54
measured a battery, MM-1 proves only the block-diagonal case, and "no `A` we tried" is not
"no `A`."**

**Why not the three options as posed.**

* **(b) `B` directly — rejected.** `B`'s three degrees of freedom are the space, the operator
  split and the constants. Leg 52 measured the space, leg 53 measured the split (`K/2` for
  every choice), leg 54 has now measured the shape of `A`. `B` is pre-refuted for this operator
  before its GA would ever run, and its GA is still banned besides.
* **(a) `WV` first — rejected as critical path, kept as exploration.** It unblocks a stage that
  the paragraph above says is empty. Unblocking is worth a slot, not the critical path. It is
  leg **59**, in slot LEG-D.
* **(c) a fresh target round — right idea, wrong order.** What changed across 51–57 is not
  which object we want; leg 55 says the object was fine. What changed is that we now have a
  measured characterization of which operators the method can handle — multiplier yes,
  off-diagonal shift no — and that characterization is the **screen** a new target round should
  run through. Selecting targets before writing the screen down is re-picking blind. So `NG`
  first, and `NG`'s **no-branch routes directly into the target round**, which is queued now as
  leg **63** so it can be scoped in parallel without being promoted.

**What `NG` is not.** It is not movement on the L1→L4 chain. Nothing in this cycle was, and
`NG`'s honest ceiling is that it converts a failure into a statable one. Say that in its prose.

**Deliverables (for the plan's `deliverable` field).** `NG-0` the novelty pass FIRST, and it
must resolve Cadiot arXiv:2505.03091's scope against *this* no-go, not just against leg 51's
claim — links, not counts. `NG-1` the proposition: hypotheses (operator class, weight classes,
admissible `A`), conclusion, and a scope line separating measured from proved. `NG-2` the gap:
extend MM-1 beyond block-diagonal `A`, or state the restriction honestly. `NG-3` sharpness: the
`μ = 2` control as the statement that the hypothesis cannot be dropped.

**Pre-committed gate for `NG` (this is the wording to put in the plan):**

> Does the no-go admit a **proof** for a named class of approximate inverses strictly larger
> than block-diagonal, with hypotheses that provably contain the `a = 0` CLM linearization?
> **yes** → the repository has a Tier-3-shaped negative theorem; write it as a standalone claim
> with its sharpness control, and escalate publication scoping to the user.
> **no** → the result is a **measurement over a battery, not a theorem**. Cap the claim at
> "measured, not proved" everywhere it appears, and the next stage is the target round (leg 63)
> with the multiplier/shift screen as its selection predicate.

---

## Live assignments

Proposed for the next cycle; the orchestrator dispatches.

| Slot | Leg | Route | Critical path? | Difficulty (pre-registered) | Branch | Gate |
|---|---|---|---|---|---|---|
| LEG-A | 58 | **NG** — the no-go as a theorem | **YES** (stage `NG`, proposed `NEXT`) | heavy | `leg/ng-v1` | Does the no-go admit a proof for a class of `A` strictly larger than block-diagonal? |
| LEG-B | 62 | **CP** — the Cadiot pre-emption, settled from the full text | no | standard | `leg/cp-v1` | Does Cadiot arXiv:2505.03091 already cover the off-diagonal / zero-diagonal case? |
| LEG-C | 63 | **M2** — target reselection, screened by the measured predicate | no | standard | `leg/m2-v1` | Is there an uncertified target whose linearization has a **multiplier** unbounded part? |
| LEG-D | 59 | **WV** — the weight fitness's wall is 2-D | no | standard | `leg/wv-v1` | Does the frozen six-property gate pass 6/6 under a 2-D wall model? |

Figure numbers pre-allocated: leg 58 → `fig55`, 62 → `fig56`, 63 → `fig57`, 59 → `fig58`.
`writeup/build_figures.py` and `writeup/curate_evidence.py` stay **append-only** across the four.

## Queue

Ranked. Each entry needs all six fields or it is not dispatchable.

```
### 58 — ROUTE-NG: THE NO-GO, STATED AS A THEOREM (critical path, proposed stage `NG`)
**Thesis.** Legs 51-57 produced every component of a result and assembled none of them. The
mechanism is named (the unbounded part is off-diagonal; the bordered tail inverse is a constant
2.19-10.32, not a decaying multiplier), the block-diagonal case is proved (MM-1's inequality
`Z_1 >= |1 - K/2|(w_{K+1}/w_K)||A_tail e_{K+1}||_w / w_{K+1}`, which holds for every finite
block because that sub-block does not contain Gamma^-1), the general case is measured over a
battery bottoming at 8.9591 against a 10.4584 baseline, the hypothesis is shown NECESSARY by a
positive control that reports the other answer (Z_1 = 0.9156 at mu = 2), and leg 57's ledger
says the case is unpublished. This leg writes that as one proposition and then spends itself on
the single gap that decides its strength: "no A we tried" is not "no A". Either MM-1 extends to
a named larger class -- all A with bounded off-diagonal blocks, all finite-rank corrections to
block-diagonal, all A arising from one Gauss-Seidel or Schur step -- or the restriction gets
stated in the proposition instead of being papered over by the battery's size. The scope line is
load-bearing and pre-committed: measured on the a=0 CLM linearization, whose Y_0 is exactly zero
for the degenerate reason banked since leg 51, so a wall measured here bounds the real target's
difficulty FROM BELOW.
**Gate.** Does the no-go admit a proof for a named class of approximate inverses strictly larger
than block diagonal, with hypotheses that provably contain the a = 0 CLM linearization?
  yes -> The repository has a Tier-3-shaped negative theorem. Write it standalone with its
         sharpness control and its scope line, and escalate publication scoping to the user.
  no  -> The result is a measurement over a battery, NOT a theorem. Cap the claim at "measured,
         not proved" in every place it appears -- PHASE2_P2_NOTES, the ban list, the writeup --
         and the next stage is leg 63's target round with the multiplier/shift screen.
**Territory.** experiments/p2_route_ng_v1_nogo.py, experiments/p2_route_ng_v1_nogo_evidence.py,
               solver/spectral_certificate.py, test_spectral_certificate.py,
               writeup/4_p2_lottery/BLOG_P2_ROUTENG_V1.md,
               writeup/4_p2_lottery/TECHNICAL_P2_ROUTENG_V1.md,
               writeup/data/p2_route_ng_v1_nogo.json,
               writeup/figures/fig55_route_ng_v1_nogo.png,
               writeup/novelty/leg_58.md, experiments/journal/leg_58.md
**Difficulty.** heavy
**Independence.** Sole owner of solver/spectral_certificate.py, as leg 54 was. Leg 62 works the
same literature question but owns different files and its answer CAPS NG's claim strength
rather than blocking its work -- NG-0 runs its own pass regardless.
```

```
### 62 — ROUTE-CP: THE CADIOT PRE-EMPTION, SETTLED FROM THE FULL TEXT
**Thesis.** Leg 57 flagged Cadiot arXiv:2505.03091 as independently pre-empting leg 51's
methodological claim, and recommended not re-claiming that finding at full strength. That
recommendation is correct and insufficient: the same paper is the single largest novelty risk to
leg 58's proposition, and leg 57 did not establish whether Cadiot's construction reaches the
OFF-DIAGONAL unbounded part with a non-decaying tail inverse -- which is NG's actual hypothesis,
not leg 51's. This repository has been burned twice by literature read at the wrong depth: leg
53 read BDL's dominance hypothesis off a publisher abstract page and lost the claim, and LIT
settled it only from the full PDF. So settle this one from the full PDF, locate the statement,
and record the hypotheses verbatim. Do the same for anything Cadiot cites forward into this
case. Links, not counts.
**Gate.** Does Cadiot arXiv:2505.03091's construction cover an operator whose unbounded part is
off-diagonal with a non-decaying tail inverse -- i.e. does it already contain leg 58's no-go, or
a positive result that contradicts it?
  yes -> NG's proposition is pre-empted or refuted. Report the located statement with its
         hypotheses, cap NG's claim at whatever remains, and do not write it as novel.
  no  -> The gap leg 57's ledger measured is confirmed at full-text depth for the one paper most
         likely to close it. Bank the located hypotheses as an executable ledger entry; NG may
         claim novelty against this paper and no further.
**Territory.** solver/certificate_shapes.py, test_certificate_shapes.py,
               solver/literature_gates.py, test_literature_gates.py,
               experiments/p2_route_cp_v1_cadiot.py,
               writeup/4_p2_lottery/TECHNICAL_P2_ROUTECP_V1.md,
               writeup/data/p2_route_cp_v1_cadiot.json,
               writeup/figures/fig56_route_cp_v1_cadiot.png,
               writeup/novelty/leg_62.md, experiments/journal/leg_62.md
**Difficulty.** standard
**Independence.** Owns the ledger modules leg 57 created; NG owns the certificate module. No
file overlap. Informs NG's claim strength without gating NG's work.
```

```
### 63 — ROUTE-M2: TARGET RESELECTION, SCREENED BY THE MEASURED PREDICATE
**Thesis.** Stage M chose HL_S2_nonsymmetric on defensible grounds and leg 55 has now confirmed
the object itself was never the problem -- it sits in an admissible class with coefficients
decaying k^{-1.396}. What legs 51-57 refuted is the METHOD's reach, and they refuted it with a
predicate sharp enough to screen candidates: does the linearization's unbounded part act as a
MULTIPLIER (the method's shape, tail inverse decays like 1/Lambda_M) or as a SHIFT (off-diagonal,
tail inverse constant)? Run M's own TARGET_LEDGER machinery again with that predicate added as a
column, over uncertified targets on models where blow-up is provable -- the prize's actual
wording. This is scoping, NOT promotion: it produces a ranked ledger with the predicate
evaluated, and promoting any row into the committed sequence stays escalation #1. Note the live
constraint honestly in the writeup: the most obvious multiplier-shaped candidates are
dissipative, and stage V's ban forbids re-opening that question as posed "unless re-posed for a
FLUID transport model, which needs L1 first" -- L1 is now measured dead in both realizations, so
whether that lift condition can ever be met is a USER call this leg surfaces and does not make.
**Gate.** Is there at least one uncertified target, on a model where blow-up is provable, whose
linearization's unbounded part is a MULTIPLIER under the leg-57 predicate?
  yes -> Report the ranked ledger with the predicate column and the top candidate's evidence.
         Promote nothing; escalate the sequence change to the user (escalation #1).
  no  -> Every candidate the ledger can reach is shift-shaped, so the method is exhausted for
         this repository's whole target class, not just for one object. That is a materially
         stronger negative than NG's and it goes in the plan as such. Stop proposing new targets
         for this method.
**Territory.** solver/target_selection.py, test_target_selection.py,
               experiments/p2_route_m2_v1_targets.py,
               writeup/4_p2_lottery/BLOG_P2_ROUTEM2_V1.md,
               writeup/4_p2_lottery/TECHNICAL_P2_ROUTEM2_V1.md,
               writeup/data/p2_route_m2_v1_targets.json,
               writeup/figures/fig57_route_m2_v1_targets.png,
               writeup/novelty/leg_63.md, experiments/journal/leg_63.md
**Difficulty.** standard
**Independence.** Owns solver/target_selection.py, claimed by nobody else. Uses leg 57's
predicate as INPUT, which is already merged, so it depends on no live leg's result.
```

```
### 59 — ROUTE-WV: THE WEIGHT FITNESS'S WALL IS 2-D, NOT 1-D
**Thesis.** Stage B is blocked because C-PILOT's six-property viability gate answered FAIL 4/6
and PREP's named repairs moved it without passing (P2 0.775 -> 0.875 against a 0.90 floor; P3
worst |slope-1| 0.366 -> 0.342 against 0.05). P2's own gate note records the suspected cause:
the measured wall is a 1-D slice of what is actually a 2-D boundary, so the fitness is scored
against the wrong geometry. Model the wall in both weight factors, re-derive the analytic growth
rate in that geometry (the 1-D version predicted x7.39 and measured x7.39, so there is a
known-answer window), and RE-RUN the frozen six-property gate unchanged. The gate stays frozen:
repairing the fitness is allowed, moving the goalposts is not. NO GA compute runs on either
branch -- that ban lifts only on a gate that PASSES, and lifting it is the user's call.
NEW CONTEXT, and the leg must carry it: leg 54 has now measured the shape of A dead on top of
leg 53's split and leg 52's space, so even a PASS here unblocks a stage whose three degrees of
freedom are all separately measured worthless for this operator. Passing the gate is worth
knowing; it is not worth reading as a route.
**Gate.** With a 2-D wall model, does the FROZEN six-property viability gate pass 6/6 -- in
particular P2 >= 0.90 and P3 max |slope-1| <= 0.05?
  yes -> The recorded lift condition for the GA ban is met. Report it, run NO GA compute, and
         escalate to the user (escalation #1), with the paragraph above attached so the pass is
         not read as a route.
  no  -> Report which properties still fail and by how much. Stage B's fitness is dead as
         parameterized, and any future B proposal must change the fitness's definition, not its
         wall model.
**Territory.** solver/weight_search.py, test_weight_search.py,
               experiments/p2_weight_repairs_v2.py, experiments/p2_weight_repairs_v2_evidence.py,
               writeup/4_p2_lottery/BLOG_P2_WEIGHT_REPAIRS_V2.md,
               writeup/4_p2_lottery/TECHNICAL_P2_WEIGHT_REPAIRS_V2.md,
               writeup/data/p2_weight_repairs_v2.json,
               writeup/figures/fig58_weight_repairs_v2.png,
               writeup/novelty/leg_59.md, experiments/journal/leg_59.md
**Difficulty.** standard
**Independence.** solver/weight_search.py is claimed by no other live leg. Touches no
certificate term, no literature ledger and no target ledger.
```

```
### 61 — ROUTE-KA: A KNOWN-ANSWER WINDOW FOR THE WHOLE INTERVAL PIPELINE
**Thesis.** Read the `validated` column of capabilities.py for the certificate stack: nearly
every entry is validated INTERNALLY -- enclosures contain exact rationals, rigorous bounds
dominate float readings, a poisoned iterate is rejected. What the stack has never done is
reproduce a PUBLISHED certified radius end to end. solver/target_selection.py reproduces CLN's
Kawahara radius, but as a transcribed number in a ledger, not as output of
solver/interval_certificate.py. Point the actual pipeline at Kawahara and see whether it lands
inside CLN's published interval. Lesson 84: a known-answer probe has a WINDOW, so the window is
pre-committed -- the published radius interval, at their stated truncation. Leg 56 raises the
stakes: it reported defects of 1.85e7x and 2.04e11x from this same pipeline, and a pipeline that
has never met a published answer end to end is a weak place to source a number that large.
**Gate.** Does solver/interval_certificate.py, run end to end on the Kawahara problem, produce a
certified radius inside CLN's published interval at their truncation?
  yes -> The stack has its first end-to-end published known-answer gate. Bank it as an
         executable test; every future negative from this pipeline cites it, including leg 56's.
  no  -> The pipeline disagrees with a published certificate. That is a bug hunt and it takes
         priority over every route in this queue including the critical path, because every
         banked interval result -- leg 56's two exponents most of all -- depends on it.
**Territory.** solver/interval_certificate.py, test_interval_certificate.py,
               experiments/p2_route_ka_v1_kawahara.py,
               writeup/data/p2_route_ka_v1_kawahara.json,
               writeup/novelty/leg_61.md, experiments/journal/leg_61.md
**Difficulty.** standard
**Independence.** Owns solver/interval_certificate.py. Leg 56 has merged, so the earlier
collision is gone -- this is now dispatchable alongside anything in the queue.
```

```
### 60 — ROUTE-PQ: THE TWO NEGATIVE FINDINGS THAT HAVE NO QUARTET
**Thesis.** DOCS flagged that Route-PORT v1 and v2 each have a runner and curated data but no
`*_evidence.py` and no registered figure. Both carry load-bearing negative findings -- the
certificate closes around the WRONG truncated object (leg 46: the true object is 1.55e+08 ball
radii outside it), and extending reach makes the truncation gap WORSE (leg 47: +0.47 decades per
unit rho, the wrong sign) -- and both are cited as settled in the ban list. Writing their
evidence scripts re-derives the quoted numbers from stored data, which is a reproduction check
that can FAIL, and two of this repository's last three discrepancies (REPRO's 50/50 claim, leg
53's K vs K^2) were exactly this kind.
**Gate.** Do the evidence scripts re-derive every number Route-PORT v1's and v2's prose quotes,
from the stored curated data, to the precision the prose states?
  yes -> Both quartets close; the two bans that cite them keep their evidence.
  no  -> A banked negative finding is not reproducible from its own data. Park it, do NOT edit
         the prose to match, and escalate -- a ban resting on an unreproducible number is the
         user's call.
**Territory.** experiments/p2_route_port_v1_bordered_evidence.py,
               experiments/p2_route_port_v2_reach_evidence.py,
               writeup/figures/fig59_route_port_v1.png, writeup/figures/fig60_route_port_v2.png,
               writeup/README.md, writeup/novelty/leg_60.md, experiments/journal/leg_60.md
**Difficulty.** light
**Independence.** Touches no solver module and recomputes no new number.
```

## Ranking rationale

Refreshed whenever a gate answers. Rank by, in order:

1. could this leg actually move a link of the L1→L4 chain;
2. can its gate answer either way within one leg's work;
3. is it independent of the other three live legs.

**Refreshed 2026-08-05 (second refresh), after 54 NO / 55 YES / 56 NO / 57 NO.**

**Criterion (1) has gone quiet, and the ranking has to say so out loud.** `L1` was the only
movable link, and this cycle measured it dead in both of its realizations — coefficient basis by
leg 54, collocation basis by leg 56. No leg in this queue can move a link of the chain. Ranking
them by proximity would be theatre. So the order below is set by criterion (2) sharpened into a
question this repository can actually answer: **which leg converts the most already-paid work
into something statable, and which most cheaply tells us whether a next lane exists at all.**

**58 (NG) is first** because seven legs of paid work currently exist only as PR bodies, and the
one gap between "table" and "theorem" — MM-1 proves block-diagonal, the battery covers what it
covers — is a well-posed mathematical question that one leg can answer either way. Its no-branch
is not a dead end either: it caps the claim and hands off to 63.

**62 (CP) is second** because it is the largest single risk to 58's value and it is cheap. Leg
57 already named the paper. This repository has twice mis-scoped a literature claim by reading
at the wrong depth (leg 53's BDL abstract; leg 53's withdrawn resurfacing clearance), and the
correction both times came from the full text. Reading it now costs one standard leg; reading it
after 58 ships costs the claim.

**63 (M2) is third** because it is the only leg that can tell us whether a next lane exists, and
because leg 57 handed it a predicate sharp enough to screen with. Its no-branch is the most
consequential sentence available in this queue — *every* reachable target is shift-shaped, so
the method is exhausted for the whole target class — and that is worth knowing regardless of how
58 lands. It ranks below 62 only because 62 is cheaper and gates a claim already in flight.

**59 (WV) is fourth and it is deliberately hedged.** It unblocks `B`, and `B` now has all three
degrees of freedom separately measured dead. Its yes-branch is worth knowing and is not worth
reading as a route, which is written into the leg's own text so the finding cannot be quoted
without the caveat.

**61 (KA) and 60 (PQ) are audit legs, and 61 is underranked by its position.** KA's no-branch
invalidates every banked interval result including leg 56's two exponents, which are among the
largest numbers this repository has ever published. It sits at fifth only because its yes-branch
— by far the likely one — is confirmatory. If a slot frees up, it goes before 60 without
argument.

**Ordering the queue by proximity to the Clay chain is a choice of what to try. It is never a
claim that anything moved.** In 57 legs, no link has moved; Clay stays at ~0.05% behind Walls 1
and 2. This cycle is the first one where the honest summary is not "no link moved" but **"the
only movable link was measured unreachable by this method, in both of its realizations."**

## Open direction questions for the user

These also appear under `⚠ NEEDS YOU` in `PROGRESS.md`. The run continues around them.

1. **`NG` entering the committed sequence is escalation #1**, and the DM is making the call
   under the user's explicit pre-delegation ("whichever pursues our goals best"). Flagged here
   so it is visible as a plan change and not just as a queue entry. Reversible: if you would
   rather go straight to the target round, swap slots LEG-A and LEG-C and mark `M2` as `NEXT`
   instead — the cost is that the target screen ships before the predicate it screens with is
   written down.
2. **Stage `V`'s ban has a lift condition that may now be unreachable.** It reads "unless the
   question is re-posed for a FLUID transport model, which needs `L1` first." `L1` is, as of
   this cycle, measured dead in both realizations. So either the condition is permanently unmet
   — in which case the dissipative direction, the one place leg 53's positive control shows the
   instrument actually works (`Z₁ = 0.9156` at `μ = 2`), is closed forever — or you re-word it.
   Leg 63 surfaces this; only you can rule on it. **This is the single highest-value direction
   question open right now.**
3. **What is the exit criterion for this project?** Asked plainly because the honest reading of
   this cycle invites it. The prize is a novel Tier-3 result on a model where blow-up is
   provable. `NG`'s yes-branch would deliver a *negative* Tier-3-shaped result, which may or may
   not be what you wanted to buy. If it is, `NG` → write-up is a short path to shipping. If it
   is not, then leg 63's answer decides whether there is a positive path left at all, and the
   two legs should be read as a pair.
