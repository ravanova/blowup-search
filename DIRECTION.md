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

**Resuming under the ten-leg contract.** The previous DM session ran under the older four-leg
contract and left six candidate legs (58 NG, 59 WV, 60 PQ, 61 KA, 62 CP, 63 M2) fully specified
but **undispatched** — cycle 1's legs 54–57 had already landed and merged cleanly (see below).
This session's job is to bring the queue up to the ten-slot contract: keep the six existing
candidates, add eight new independent exploration legs (64–71), and fill LEG-A through LEG-J.
Nothing in this refresh changes any landed finding.

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

Last leg number actually landed/merged on main: **57**. Legs **58–63** are reserved,
fully-specified, unused numbers carried over from the prior session (do not renumber them).
This session adds **64–71**. **Next fresh leg number for any future candidate is 72.**

**Refill, mid-cycle: leg 68 (Route-IX) landed at `b3ef49a`.** Gate answered **YES** —
`writeup/INDEX.md` was stale (its own header still said Route-TC "has no writeup yet" for a
route that landed two legs earlier); legs 53(TC)/54(MM)/55(NB)/56(TN)/57(XS) all had complete
quartets on disk, so the five rows were added and the stale paragraph removed. Mechanical, in
territory, no issues — does not change the ranking picture. Per this file's own instruction
("promote from this list in order if a slot frees up, without re-ranking, unless a gate answer
changes the picture"), the orchestrator promoted **leg 64 (Route-A12, reserve rank 11)** into
the now-open LEG-I slot. Confirmed correct; no DM disagreement. LEG-I is now leg 64, not leg
68, in the table below. Reserve was **67 (FD), 70 (RC), 71 (CAP)** at that point.

**Refill, mid-cycle: leg 65 (Route-L1G) landed.** Gate answered **NO** — both the weighted-ℓ¹
no-go and the discrete-ball trap confirmed unpublished after full-text depth on 4 papers and 39
forward citations. Route-D's last claim with "a real chance of being new" (per PHASE2's own
words) is now confirmed genuinely novel, not merely unflagged. The coordinator corrected
`capabilities.py`'s `holder_norms.py` annotation directly, from "UNSEARCHED at primary source"
to "searched and not found" (commit `ab07316`) — a small factual fix matching leg 65's own
pre-committed no-branch instruction ("record this precisely... correct the ban-list annotation
accordingly" applies in spirit to the NO outcome too, since the annotation's factual content
changed from "unsearched" to "searched"); no DM disagreement. A verifier is doing the
post-landing review. Per the reserve-list instruction, the orchestrator promoted **leg 67
(Route-FD, next in reserve order)** into the now-open LEG-H slot. Confirmed correct; no
re-ranking triggered. Reserve is now **70 (RC), 71 (CAP)**.

---

## THE `NEXT` CALL — recommendation to the orchestrator (unchanged from prior session)

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

Ten slots, live at all times under the current contract. LEG-A carries the critical path
(stage `NG`); LEG-B through LEG-J are independent exploration routes. No two rows below share a
`solver/` module or a `writeup/data/*.json` file — checked explicitly.

| Slot | Leg | Route | Critical path? | Difficulty | Branch | Gate (short form) |
|---|---|---|---|---|---|---|
| LEG-A | 58 | **NG** — the no-go as a theorem | **YES** (stage `NG`, proposed `NEXT`) | heavy | `leg/ng-v1` | Does the no-go admit a proof for a class of `A` strictly larger than block-diagonal? |
| LEG-B | 62 | **CP** — the Cadiot pre-emption, settled from the full text | no | standard | `leg/cp-v1` | Does Cadiot arXiv:2505.03091 already cover the off-diagonal / zero-diagonal case? |
| LEG-C | 63 | **M2** — target reselection, screened by the measured predicate | no | standard | `leg/m2-v1` | Is there an uncertified target whose linearization has a **multiplier** unbounded part? |
| LEG-D | 59 | **WV** — the weight fitness's wall is 2-D | no | standard | `leg/wv-v1` | Does the frozen six-property gate pass 6/6 under a 2-D wall model? |
| LEG-E | 61 | **KA** — a known-answer window for the interval pipeline | no | standard | `leg/ka-v1` | Does `interval_certificate.py` reproduce CLN's published Kawahara radius? |
| LEG-F | 60 | **PQ** — the two negative findings that have no quartet | no | light | `leg/pq-v1` | Do Route-PORT v1/v2's evidence scripts re-derive their quoted numbers? |
| LEG-G | 69 | **IA** — adversarial stress audit of the shared interval core | no | standard | `leg/ia-v1` | Does `solver/interval.py`'s compensated matvec bound still dominate under harder adversarial cases? |
| LEG-H | 67 | **FD** — literature search for 2D Boussinesq's fractional critical exponent | no | light | `leg/fd-v1` | Does a primary source publish an independent critical fractional-dissipation exponent for 2D Boussinesq? |
| LEG-I | 64 | **A12** — literature search for alpha_1 at a=1/2 | no | light | `leg/a12-v1` | Does any primary source publish alpha_1 at a=1/2 (or its sigma=3 criticality) for this model? |
| LEG-J | 66 | **QF** — dedicated tests for the three modules with none | no | light | `leg/qf-v1` | Do direct tests of `gclm.py` / `boussinesq.py` / `spectral_utils.py` find any discrepancy? |

**LEG-I promoted 2026-08-05 mid-cycle:** leg 68 (IX) landed YES and vacated the slot; leg 64
(A12) was promoted in per the reserve order, without re-ranking. **LEG-H promoted 2026-08-05
mid-cycle:** leg 65 (L1G) landed NO and vacated the slot; leg 67 (FD) was promoted in per the
reserve order, without re-ranking. See Status above for both landing details.

Figure numbers pre-allocated: leg 58 → `fig55`, 62 → `fig56`, 63 → `fig57`, 59 → `fig58`,
60 → `fig59`/`fig60`. Legs 69, 67, 64, 66 (and the now-landed 68, 65) are audit/literature/
hygiene legs and register **no figure**, by the same convention already established for Route-D
scope (advection) and Route-D v15 (literature scope) — "no measurement, no figure."
`writeup/build_figures.py` and `writeup/curate_evidence.py` stay **append-only** across all ten.

**Territory-overlap check (explicit, as required).** Solver modules touched by the ten:
`spectral_certificate.py`(58), `certificate_shapes.py`+`literature_gates.py`(62),
`target_selection.py`(63), `weight_search.py`(59), `interval_certificate.py`(61), none(60),
none-owned/read-only(69 reads `interval.py`, edits nothing), none-owned/read-only(67 reads
`fractional_boussinesq.py`, edits nothing), none-owned/read-only(64, reads
`critical_dissipation.py`, edits nothing), new test files only(66, touches no existing solver
module). All ten distinct — **no collision.** `writeup/data` JSON files are likewise ten
distinct names (`p2_route_ng_v1_nogo.json`, `p2_route_cp_v1_cadiot.json`,
`p2_route_m2_v1_targets.json`, `p2_weight_repairs_v2.json`, `p2_route_ka_v1_kawahara.json`, two
Route-PORT evidence JSONs already on disk (leg 60 reads, does not create),
`p2_route_ia_v1_interval_stress.json`, `p2_route_fd_v1_lit.json`,
`p2_route_a12_v1_alpha_lit.json`, none(66)) — **no collision.** (Leg 68's territory,
`writeup/INDEX.md` only, and leg 65's, its own literature-lit JSON, have landed and are no
longer live.)

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

```
### 69 — ROUTE-IA: ADVERSARIAL STRESS AUDIT OF THE SHARED INTERVAL CORE
**Thesis.** solver/interval.py is the one module both live realizations of L1 depend on: leg
58's compactified-basis certificate (spectral_certificate.py) and leg 61's known-answer pipeline
(interval_certificate.py) both sit on its hand-rolled outward-rounded intervals and its
compensated (Ogita-Rump-Oishi) matvec, whose bound is relative to the ANSWER rather than to the
terms. capabilities.py's own validated line for it says containment holds "on adversarial
cases, including the directed-rounding edge cases where naive intervals lose the answer" --
but that corpus predates both of this cycle's live legs and was never stress-tested against
the SIZES and CONDITIONING the certificate stack now actually runs (K up to 128 per leg 57,
catastrophic cancellation near the tail block's near-zero diagonal per leg 51-53). A soundness
gap in the shared primitive would silently invalidate every rigorous number both legs 58 and
61 produce, which is a materially larger blast radius than either leg's own gate. This leg
does not sharpen any Route-D bound and builds no new l1-Fourier or collocation machinery -- it
is a pure stress test of infrastructure both live critical-path-adjacent legs already depend on,
which the machinery ban does not reach.
**Gate.** Under a harder adversarial corpus (larger matrices matched to the certificate's own
K range, near-singular conditioning matched to the tail block's near-zero diagonal, and
subnormal-range inputs), does the rigorous bound still provably dominate the exact rational
value on every sampled case -- zero false negatives?
  yes -> The shared interval core gets a stronger, size-matched validation footprint. Cite it
         from leg 58's and leg 61's writeups as additional evidence their numbers are sound.
  no  -> A soundness defect in the primitive underlying BOTH live L1 realizations. This is a
         stop-the-line finding: report the failing case exactly, do NOT patch solver/interval.py
         under this leg's own authority, and escalate immediately -- every rigorous number
         either live leg has produced or will produce is suspect until it is resolved.
**Territory.** test_interval_stress.py, experiments/p2_route_ia_v1_interval_stress.py,
               writeup/data/p2_route_ia_v1_interval_stress.json,
               writeup/novelty/leg_69.md, experiments/journal/leg_69.md
**Difficulty.** standard
**Independence.** Reads solver/interval.py; does not edit it under any gate outcome (a NO
outcome escalates rather than patches, by design, so this leg cannot collide with anything that
depends on the module's current behavior). Owns no solver module. No other leg touches
solver/interval.py or the new test file.
```

```
### 65 — ROUTE-L1G: LITERATURE SEARCH FOR THE WEIGHTED-ELL-1 NO-GO / DISCRETE-BALL TRAP
**Thesis.** solver/holder_norms.py's validated line says the weighted-l1 no-go is "derived here
and is UNSEARCHED at primary source", and PHASE2_P2_NOTES's M-4 confirms it explicitly: CLN
arXiv:2302.12877 works in Hilbert/Fourier H^l spaces, not weighted l1, so it narrows but does
not close Route-D's weighted-l1 no-go and discrete-ball trap (Route-D v6) -- and the notes say
outright these are "still UNSEARCHED at primary source, and still the only claims with a real
chance of being new" in the entire Route-D programme. That sentence has been sitting unactioned
since M2's pass. Two Tier-2 papers are fetched but not read closely for THIS specific claim
(arXiv:2312.01702 unread for it; arXiv:1908.09385 was read for computer-assistance only, per
M-3, not for this). This leg reads them at full-text depth for the weighted-l1 no-go and the
discrete-ball trap specifically -- not for Route-F's critical exponent (already settled, J-1)
and not for NG's off-diagonal hypothesis (leg 62's separate question) -- and extends the search
to whatever those two papers cite forward. Lesson 90: a literature negative is a fact about the
literature, and it decays at the rate of memory (lesson 68) if left as a flagged sentence
instead of an executable gate.
**Gate.** Does any primary source (the two unread Tier-2 papers, or anything they cite forward)
already publish the weighted-ell-1 no-go or the discrete-ball trap for this operator class, or
an equivalent statement under different notation?
  yes -> Route-D's last claim with "a real chance of being new" is pre-empted or narrowed.
         Locate the statement, record its hypotheses verbatim, and correct the ban-list
         annotation on holder_norms.py accordingly -- this does not lift the Route-D
         bound-sharpening ban (B is dead on all three DOF regardless), it only corrects the
         novelty bookkeeping.
  no  -> Confirmed unsearched after full-text depth on the two remaining Tier-2 papers. Record
         this precisely (which papers, which sections, what was and was not found) so a future
         write-up of Route-D's history can cite it, without resuming any Route-D computation --
         this leg produces no new bound and touches no Route-D module.
**Territory.** experiments/p2_route_l1g_v1_lit.py, writeup/data/p2_route_l1g_v1_lit.json,
               writeup/novelty/leg_65.md, experiments/journal/leg_65.md
**Difficulty.** standard
**Independence.** Reads solver/holder_norms.py; edits nothing in solver/. Distinct literature
target from leg 62 (leg 62 is Cadiot arXiv:2505.03091 against NG's off-diagonal hypothesis;
this leg is two different Tier-2 papers against Route-D's weighted-l1 no-go). No file overlap.
```

```
### 68 — ROUTE-IX: `writeup/INDEX.md` FRESHNESS (LEGS 53-57 ARE MISSING)
**Thesis.** writeup/INDEX.md is DOCS's machine-checkable quartet ledger, and it is stale: its
Arc 4 table has no row for Route-TC (leg 53), MM (leg 54), NB (leg 55), TN (leg 56) or XS (leg
57), even though all five have landed, merged, and (checked directly) already have their
BLOG/TECHNICAL/evidence/data files on disk under writeup/4_p2_lottery/ and writeup/data/ -- the
index's own header line still reads "Route-TC ... has no writeup yet ... in progress", which is
now false. A stale index is worse than a missing one: a future DM or agent grepping it for "does
X have a quartet" gets a confidently wrong answer. This is the same failure mode leg 60 (PQ)
addresses for Route-PORT's evidence scripts, one level up -- the ledger itself, not the legs it
tracks.
**Gate.** Do legs 53 (TC) / 54 (MM) / 55 (NB) / 56 (TN) / 57 (XS) each have a complete
runner/data/BLOG+TECHNICAL/evidence/figure quartet on disk, matching the convention documented
at the top of INDEX.md?
  yes -> Add the five rows to Arc 4's table, delete the stale "Route-TC ... in progress"
         paragraph, and the index is caught up to leg 57.
  no  -> Add the five rows anyway, with explicit `GAP` markers on whichever piece is actually
         missing (per lesson 76 -- negative results need quartets too), so the gap is documented
         rather than silently absent.
**Territory.** writeup/INDEX.md, writeup/novelty/leg_68.md, experiments/journal/leg_68.md
**Difficulty.** light
**Independence.** Touches one file outside any other leg's territory. Recomputes nothing;
reads only what is already on disk under writeup/.
```

```
### 66 — ROUTE-QF: DEDICATED TESTS FOR THE THREE MODULES WITH NONE
**Thesis.** capabilities.py records, verbatim, that solver/boussinesq.py, solver/gclm.py and
solver/spectral_utils.py have "no dedicated test file -- exercised through" other modules'
tests (test_solver_boussinesq.py, test_solver_clm.py, and "the solvers above" respectively).
Indirect coverage means these three have never been asked a question they could fail on their
own terms -- a bug local to one of them could hide behind whatever the indirect test happens to
exercise. This is pure hygiene: write direct unit tests against each module's own public
interface (residual/Jacobian shapes, known small-case values, basic invariants already implied
by the modules that use them), run them, and see whether anything the indirect tests never
touched actually breaks.
**Gate.** Do the new dedicated tests find any discrepancy -- an assertion failure, a numeric
mismatch, or a code path the indirect tests never exercised producing a wrong answer -- versus
what test_solver_boussinesq.py / test_solver_clm.py currently assume?
  yes -> A real bug local to one of the three modules, found only because it was tested
         directly. Report it precisely and treat it as a priority fix independent of NG, since
         it could be latent under any leg that imports these modules.
  no  -> capabilities.py's "no dedicated test file" line becomes false for all three; update it
         to point at the new test files. Pure hygiene, banked, no science content.
**Territory.** test_gclm_dedicated.py, test_boussinesq_dedicated.py,
               test_spectral_utils_dedicated.py,
               writeup/novelty/leg_66.md, experiments/journal/leg_66.md
**Difficulty.** light
**Independence.** Reads solver/gclm.py, solver/boussinesq.py, solver/spectral_utils.py; edits
none of them under a NO outcome (a bug found is reported, not silently patched, by the same
discipline as leg 69). Owns three new test files claimed by nobody else.
```

```
### 64 — ROUTE-A12: LITERATURE SEARCH FOR ALPHA_1 AT a=1/2
**Thesis.** solver/critical_dissipation.py's validated line: "alpha_1 = 0 at a=0 == ALS eq (61);
a=1/2 is UNSEARCHED at primary source." PHASE2_P2_NOTES's J-2 sharpens this: our own computed
value is alpha_1 = +0.133683 at a=1/2, criticality there is sigma=3 (in neither ALS nor XU, the
two Tier-1 papers), and the note is explicit -- "UNSEARCHED, not novel." That distinction has
sat unresolved since the J-pass. Search beyond Tier 1 (Lushnikov et al., cited by ALS section 1
for the a=0/a=1/2 exact pole-dynamics results per J-3; the Tier-2 papers) for whether this
specific number, or the sigma=3 criticality statement at a=1/2, is already published anywhere.
**Gate.** Does any primary source publish alpha_1 at a=1/2 (or the sigma=3 criticality
statement it comes from) for this model?
  yes -> Cite it, compare to our +0.133683 to the precision available, and correct the
         capabilities.py annotation from UNSEARCHED to the located citation.
  no  -> Confirmed unsearched after an actual search (not just Tier 1/2's absence). Record
         which sources were checked and record the number as measured-not-independently-
         validated, which is a small but real fact worth stating precisely rather than leaving
         as a stale comment.
**Territory.** experiments/p2_route_a12_v1_alpha_lit.py, writeup/data/p2_route_a12_v1_alpha_lit.json,
               writeup/novelty/leg_64.md, experiments/journal/leg_64.md
**Difficulty.** light
**Independence.** Reads solver/critical_dissipation.py; edits nothing in solver/. No other leg
touches this module or this claim.
```

```
### 67 — ROUTE-FD: LITERATURE SEARCH FOR 2D BOUSSINESQ'S FRACTIONAL CRITICAL EXPONENT
**Thesis.** solver/fractional_boussinesq.py's validated line reads "consistency with the 1D
critical exponent; no independent known answer" -- the 2D object's critical fractional-
dissipation exponent has only ever been checked against our OWN 1D number, never against a
published value. This is a pure literature search: does any primary source state an independent
critical exponent for 2D Boussinesq (or its vorticity-stream formulation) under Lambda^s
dissipation that our stored, already-computed number can be checked against. No new solve runs
under this leg -- if a published value is found, the comparison is arithmetic against the
number already on file, not a new simulation. This is a different quantity from beta (the
2D growth-rate leg 43 measured and found non-convergent) and does not touch that ban.
**Gate.** Does a primary source publish an independent critical fractional-dissipation exponent
for 2D Boussinesq (or its vorticity-stream equivalent)?
  yes -> Compare our stored exponent against it (arithmetic only) and report agreement or
         disagreement, correcting the capabilities.py annotation either way.
  no  -> The exponent remains internally-consistent-only. State that plainly; no claim upgrade,
         no new computation attempted.
**Territory.** experiments/p2_route_fd_v1_lit.py, writeup/data/p2_route_fd_v1_lit.json,
               writeup/novelty/leg_67.md, experiments/journal/leg_67.md
**Difficulty.** light
**Independence.** Reads solver/fractional_boussinesq.py; edits nothing, runs no new solve.
Distinct quantity and distinct module from leg 43's banned beta re-measurement.
```

```
### 70 — ROUTE-RC: REALIZATION AUDIT OF rescaled_spectrum.py (DOCS-ONLY, NO NEW COMPUTE)
**Thesis.** PHASE2_P2_NOTES's J-4 is explicit: our discretization of the gCLM rescaled
linearization's spectrum has NO origin condition, so what sections 26/30 measured and reported
as "the operator's spectrum" is actually the maximal L^2 realization's spectrum (Xu Proposition
2's dichotomy), and "re-running I5 with an origin condition is the top-ranked correction item."
This leg does NOT re-run anything or recompute any spectrum -- that would risk reading as a new
gCLM measurement, which is banned (model exhausted, leg 42). Instead it is a pure code-and-prose
audit: read solver/rescaled_spectrum.py's existing discretization to confirm, from the code
itself, whether an origin condition is or is not imposed, and correct every place the spectrum
count (e.g. "141 of 144 unstable directions at mu=0") is quoted to state its realization
explicitly, per lesson 70 ("a spectrum is not a property of an operator until you name the
realization"). No new numbers; only correct labeling of numbers already on file.
**Gate.** Does solver/rescaled_spectrum.py's discretization impose an origin (H^2-type)
condition at X=0, or none (the maximal L^2 realization)?
  yes -> The "loose realization" caveat J-4 attached is itself wrong or outdated; correct the
         record to say the origin-conditioned realization was measured, and flag J-4's own note
         for a follow-up correction.
  no  -> Confirms the loose-realization reading. Add the explicit realization-disclosure
         sentence everywhere the spectrum count is quoted, without touching the numbers
         themselves or running any new solve.
**Territory.** experiments/p2_route_rc_v1_realization_audit.py (read-only introspection of the
               existing discretization; no new solve), writeup/novelty/leg_70.md,
               experiments/journal/leg_70.md
**Difficulty.** light
**Independence.** Reads solver/rescaled_spectrum.py; explicitly does not edit its logic under
either gate branch (docs-only leg). No other leg touches this module.
```

```
### 71 — ROUTE-CAP: capabilities.py SELF-AUDIT (test presence and pass status)
**Thesis.** capabilities.py is the repository's single ledger of what each solver module holds
and how it was validated, and DIRECTION.md, PHASE2_P2_NOTES.md and every leg in this queue treat
its "test" and "validated" fields as ground truth. It has never been audited against the actual
test suite for drift -- a renamed module, a deleted test, or a test that now fails at HEAD would
sit silently under a confident-looking row. Run pytest --collect-only against every "test" field
cited, and confirm each cited test file exists, is collected, and passes at current HEAD.
**Gate.** Does every module row in capabilities.py have a test file that exists, is collected by
pytest, and passes at current HEAD?
  yes -> capabilities.py is confirmed accurate. Append a one-line self-audit stamp (date and
         commit hash) to the file's header comment; no other edits.
  no  -> List every stale or broken row precisely (missing file, uncollected test, red test, or
         renamed module) and correct ONLY the factual "test" field for those rows -- never the
         "validated" numeric claims, which stay frozen and get their own leg if they need
         correcting. A red test found this way is a priority bug report, not a silent fix.
**Territory.** experiments/p2_route_cap_v1_audit.py, writeup/data/p2_route_cap_v1_audit.json,
               writeup/novelty/leg_71.md, experiments/journal/leg_71.md,
               capabilities.py (factual "test"-field corrections only, pre-committed to never
               touch "validated" prose)
**Difficulty.** light
**Independence.** capabilities.py is not claimed as exclusive edit territory by any other leg
in this queue; this leg's edits are pre-committed to a narrow, non-overlapping field.
```

## Ranking rationale

Refreshed whenever a gate answers. Rank by, in order:

1. could this leg actually move a link of the L1→L4 chain;
2. can its gate answer either way within one leg's work;
3. is it independent of the other nine live legs.

**Refreshed 2026-08-05, resuming under the ten-leg contract.** Criterion (1) is still quiet —
`L1` was the only movable link and it is measured dead in both realizations (coefficient basis
leg 54, collocation basis leg 56). No leg in this queue, old or new, can move a link of the
chain on its own. The order below is set by criterion (2) sharpened, as before, into: which leg
converts already-paid work into something statable, which cheaply tells us whether a next lane
exists, and — new to this refresh, now that the queue has grown to ten — which of the *new*
candidates protects or extends that work most cheaply.

**58 (NG) through 60 (PQ) keep the prior session's order and its stated reasons**, reproduced
in the queue entries above: NG is the one leg that can turn seven legs of paid work into a
statable proposition; CP is the cheapest and largest risk to NG's novelty claim; M2 is the only
leg that tells us whether a next lane exists at all; WV is a deliberately-hedged unblock of a
stage whose three degrees of freedom are all separately measured dead; KA's no-branch would
invalidate every banked interval result including leg 56's two exponents, so it is underranked
by its position, not by its stakes; PQ is the cheapest audit in the queue.

**61 (KA), then 69 (IA), is the right order for the two infrastructure-audit legs, not the
reverse.** KA asks whether the interval PIPELINE reproduces a published answer end to end; IA
asks whether the interval PRIMITIVE underneath both pipelines is sound under harder adversarial
cases. A KA failure is diagnosable from the pipeline's own published-comparison; an IA failure
would explain a KA failure (and would also silently threaten NG, which does not itself have a
known-answer gate). IA sits at LEG-G, right after KA, because it is the highest-leverage new
candidate — a defect here has the largest blast radius of anything in the new batch, reaching
both the critical path and its known-answer control.

**65 (L1G) was next among the new candidates, and it has since landed: gate NO.** PHASE2_P2_NOTES
said outright, in its own words, that the weighted-ℓ¹ no-go and discrete-ball trap were "the only
claims [in Route-D] with a real chance of being new" — and leg 65 settled it at full-text depth
(4 papers, 39 forward citations): both are genuinely unpublished. That upgrades "unflagged
novelty risk" to "confirmed novel, narrowly scoped negative result on infrastructure this
repository is not actively building on" (`B` is dead on all three DOF regardless, so this closes
a bookkeeping question, not a live research direction). `capabilities.py`'s annotation was
corrected accordingly (`ab07316`).

**68 (IX) and 66 (QF) were ranked to close out the ten**, and 68 has since landed: gate YES,
mechanical, in territory — INDEX.md's stale "Route-TC has no writeup yet" paragraph is fixed and
the five missing rows (53/54/55/56/57) are in. QF (66) is still live at LEG-J, closing a
coverage gap capabilities.py names outright ("no dedicated test file") for three modules that
sit underneath several live legs' imports; its no-branch (no bug found) is the likely one, which
is exactly the profile of a leg that belongs at the bottom of a ten-slot queue rather than off
the queue entirely.

**64 (A12) has been promoted out of reserve into LEG-I**, per this file's own refill
instruction, on the orchestrator's correct read that leg 68's YES/mechanical outcome does not
change the ranking picture. **67 (FD) has, in turn, been promoted out of reserve into LEG-H**,
on the same correct read that leg 65's NO does not change the ranking picture either — a
confirmed-novel-but-narrow negative on dead-lane infrastructure doesn't reorder anything below
it. **70 (RC) and 71 (CAP) are the remaining reserve — ranked 13 and 14, not assigned a live
slot this cycle.** Both are real, well-specified, and independent of everything above, but each
is lower-stakes than what is already live: RC is a docs-only correction whose underlying finding
(J-4's realization caveat) is already stated, just not yet propagated; CAP is a self-audit of
the ledger everything else in this queue already trusts, valuable but the least urgent of the
two since nothing has yet flagged capabilities.py itself as drifted. If another slot frees up,
promote from this list in the order given (RC, then CAP), without re-ranking, unless a gate
answer changes the picture.

**Ordering the queue by proximity to the Clay chain is a choice of what to try. It is never a
claim that anything moved.** In 57 landed legs, no link has moved; Clay stays at ~0.05% behind
Walls 1 and 2. The honest summary of the current queue is the same one the prior session closed
on: **"the only movable link was measured unreachable by this method, in both of its
realizations,"** and this refresh's eight new legs are chosen to protect, document and stress-
test that finding and its surrounding infrastructure — not to reopen it.

## Open direction questions for the user

These also appear under `⚠ NEEDS YOU` in `PROGRESS.md`. The run continues around them. Both
carry over unchanged from the prior session — nothing in this refresh resolved or altered them,
and no new question surfaced that clears the bar for "genuinely undecidable by the DM."

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
