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
This session adds **64–71**, a first refill adds **72–75**, a second refill adds **76–78**, a
third adds **79** (implicitly, per its own entry above), a fourth refill adds **80–83**, a fifth
refill adds **84–87**, and this sixth refill adds **88–91**. **Next fresh leg number for any
future candidate is 92.**

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

**Three landings and a reserve-exhaustion refill, mid-cycle.**

- **Leg 69 (Route-IA) landed. Gate answered NO**, and correctly, on its own pre-committed
  no-branch discipline: `solver/interval.py` has real soundness gaps — subnormal-range false
  negatives and a silent NaN above `2^997` — but the finding is scoped, not a blanket
  invalidation: every live operator's actual working range (0.5–128) sits ~140–298 decades clear
  of both failure bands, so neither leg 58's nor leg 61's numbers are shown to be affected. Per
  the leg's own no-branch text ("do NOT patch `solver/interval.py` under this leg's own
  authority... escalate immediately"), the coordinator dispatched a **bench-repair agent, not a
  leg,** to fix both defects directly — correct, since no live leg owns `interval.py` for
  editing and the fix is mechanical once located. `solver/interval.py` is **off-limits for
  editing** by any new candidate until that repair lands; reading it is fine.
- **Leg 66 (Route-QF) landed. Gate answered YES**: a real but latent bug in
  `solver/spectral_utils.py`'s `derivative_hat` — odd-`n` Nyquist-zeroing destroys the last
  resolved mode — with zero current blast radius, since every live call site uses even `n`.
  Also correctly handled outside the leg system: a bench-repair agent was dispatched, and
  `solver/spectral_utils.py` is likewise **off-limits for editing** (reading fine) until that
  lands.
- **Leg 60 (Route-PQ) answered NO — escalation #4.** 111/114 of Route-PORT v1/v2's quoted
  numbers reproduce from stored data; two do not (v2's "28x worse" claim is 63x in its own
  ladder; v1's `rho=8` reach-table row quotes a different resolution's value). This is exactly
  the leg's own pre-committed no-branch: "park it, do NOT edit the prose to match, and escalate
  — a ban resting on an unreproducible number is the user's call." Branch `leg/pq-v1` is pushed
  and parked, not merged; it is in `PROGRESS.md`'s escalations for the user. **Note for the
  record: `experiments/journal/leg_60.md` does not exist on disk despite the leg having landed
  and escalated** — this is itself a small territory gap, folded into leg 72 below rather than
  fixed ad hoc here.
- **Reserve exhausted.** By the time this update lands, all six prior reserve items (64, 65, 67,
  68, 70, 71) have been dispatched or promoted — the last two, 70 (RC) and 71 (CAP), are now
  live in other slots per the coordinator's report. `solver/rescaled_spectrum.py` is confirmed
  live (70/RC), consistent with the coordinator's stated current-territories list. The exact
  slot holding 71 (CAP) was not stated in the refill request and is not independently
  re-derived here; this file defers to the orchestrator's live tracking for that one cell and
  will reconcile it on the next status message. **Four new candidates (72–75) are added below**
  to refill the queue and specifically to backfill LEG-G (vacated by 69) and LEG-J (vacated by
  66); **72 (JR)** and **73 (BV)** are selected for immediate promotion — see Live assignments
  and the ranking rationale.

**Leg 70 (Route-RC) landed at `c2ce973`. Gate answered NO** (confirms J-4's reading: no origin
condition is imposed) — **but the leg found a larger, load-bearing problem than its own gate
anticipated.** The banked "141 of 144 unstable directions at `mu=0`" claim, quoted across
`PHASE2_P2_NOTES.md` and multiple writeup files, is not merely under-labelled by realization —
the unstable count is **exactly `K-3`** at `K = 48/96/144` (a constant deficit, growing 1:1 with
the discretization dimension, while max `Re` barely moves), which is the textbook signature of a
**discretized continuum**, not a converged eigenvalue count. Ten quote sites need the correction
propagated; two (`PHASE2_P2_NOTES.md:2176`, `TECHNICAL_P2_ROUTEI_V1.md:77`) say "a
141-dimensional unstable manifold," which is **flatly false in any realization**, not just
under-labelled. A verifier is confirming before this lands as a correction.

**DM's read on the §7b vs. §8 classification, as requested:** this is a **rework leg (§7b), not
escalation #4.** The `K-3` counts themselves are not deleted, reinterpreted-away, or in dispute
— leg 70 confirms them; they stay banked exactly as measured. What needs correcting is the
**interpretive claim built on top of the numbers** ("141-dimensional unstable manifold," an
implied converged Morse index), which the `K-3` pattern shows was never a valid reading of that
data. §7b's own language fits this exactly: "a confirmed gap becomes a rework leg... same
territory as the flawed landing, gate pre-committed to the corrected measurement." Escalation #4
is for deleting or reversing a landed *conclusion* (a gate answer, a claimed inequality, a
banked finding's substance) — that is not what is happening here. **Recommend: once the
verifier confirms, dispatch as a rework leg** (drafted below as leg 76, ROUTE-MI), not as an
escalation-#4 parked branch.

**VER-I's post-landing review of leg 64 (Route-A12) found a smaller, separate defect.** The
core gate answer is fully verified (Xu's `s*(1/2)=3` citation checked to the line number,
exponent-dictionary translation independently pinned two ways, `alpha_1` searched-not-found
across a complete 25/25 arXiv corpus) — **unaffected.** But leg 64's supporting "Trap 1"
explanation misstated J. Chen's (1908.09385) critical dissipation at `a=1/2`: leg 64 wrote
`gamma = |a|^-1 = 2`; Chen's `gamma = |a|^-1` only holds for `a <= -1`, and at `a=1/2` his own
text gives `gamma = 1` (from `L^1` conservation), plus the norm index was written inverted
(`L^{|a|^-1}` instead of Chen's `L^{|a|}`). Corrected, the gap is *wider*, not narrower (two
units below `sigma=3`, not one) — no banked number or gate answer changes, only a wrong
supporting explanation in the prose. Two further trivial defects (an Oldroyd-B gloss appearing
nowhere in ALS; two mislabels) round it out. **DM's read: fold this into a bench-repair, not a
dedicated rework leg.** It is the same shape of thing that correctly went to bench-repair for
leg 69's `interval.py` fix and leg 66's `spectral_utils.py` fix — mechanical, single-paragraph,
no banked-number or gate-answer change, no live-territory contention
(`writeup/novelty/leg_64.md` belongs to an already-landed leg). Reserve the leg-76 rework-leg
mechanism for genuinely multi-file, multi-site corrections like the Morse-index finding; this
one doesn't need a branch, a quartet, or a slot. Scope for the bench-repair: correct the `gamma`
value and the inverted norm index in leg 64's "Trap 1" paragraph (wherever cited from), remove
the stray Oldroyd-B gloss, fix the two mislabels — no other content changes.

**Two more landings; a third slot vacated for leg 76; reserve exhausted again.**

- **Leg 77 (EXT2) landed: gate NO.** The rank-2 target object (gCLM_degenerate_one_scale,
  arXiv:2603.25104) remains uncertified 133 days on. Confirmed still-uncertified, banked as a
  dated watch entry, exactly its own pre-committed no-branch. Slot vacated.
- **Leg 79 (PC) answered NO — a real finding.** `radii_polynomial_status` in
  `solver/port_certification.py` does no domain validation: 11/25 adversarial hypothesis-
  violating inputs (negative/NaN `Y_0`, `Z_1`, `Z_2`) incorrectly return `closes=True`,
  including a bare sign-flip case. Severity is latent — both in-repo callers pass `(None,
  None)`, so no banked result is affected — but it is a real gap, exactly the shape leg 69 (IA)
  and leg 66 (QF) also found. Correctly handled outside the leg system: a bench-repair agent is
  adding the missing validation (not a rework leg — a straightforward infra fix with no banked
  claim to correct). `solver/port_certification.py` is now **off-limits for editing** by any new
  candidate until that repair lands; reading is fine. Slot vacated.
- **`solver/interval.py` and `solver/spectral_utils.py`'s bench-repairs have both landed** (legs
  69 and 66's findings) — **no longer off-limits.** New candidates may read or, if warranted,
  touch either module now.
- **A third slot (LEG-D) is being held open for leg 76**, per the coordinator's own plan and
  consistent with this file's recommendation that a confirmed rework leg preempts the next slot
  to open rather than queue behind ordinary reserve. **Leg 76 is not yet dispatchable — its
  scope may be sharpening.** The verifier reviewing leg 70 (for leg 76's benefit) reports the
  core finding solid so far, but has also found: (a) **leg 70 itself never recomputed
  anything** — it hardcoded its `K`-counts from the doc — and the verifier is independently
  re-deriving at `K = 144/192` now; (b) **one wording defect**: leg 70 said three origin
  quantities "contract to a scalar," but one is actually a rank-one matrix; (c) **a sharper
  continuum signature leg 70 didn't use**: `max|Im|` grows `~4.3K`. None of this changes the
  DM's §7b classification above — it is still a rework leg, not an escalation — but leg 76's
  eventual gate and territory may need to absorb the verifier's independent re-derivation and
  the rank-one-matrix correction once it lands, rather than leg 76 simply transcribing leg 70's
  numbers. Leg 76's spec below is left as drafted; whoever dispatches it should read the
  verifier's final report first and patch the gate wording if the re-derivation changes the
  `K`-values or the wording defect needs its own line.
- **Note, unconfirmed:** the coordinator's slot letters for 77/79 (LEG-J, LEG-H) don't match
  this file's LEG-G/LEG-J assignments from the previous update, and LEG-D opening for 76 implies
  leg 59 (WV) has also landed — none of which was individually reported. This file tracks leg
  *numbers* and territory, not letter-for-letter slot identity, since the orchestrator dispatches
  and letters can shift; no discrepancy here changes any territory or ranking conclusion, so it
  is noted and not chased further. If leg 59's outcome matters to a future gate (KA and WV don't
  interact), it will surface in a future status message.
- **Reserve exhausted again. Four new candidates (80–83) are added below.** Two are selected for
  immediate promotion into the two slots that need filling now (LEG-H and LEG-J, using the
  coordinator's letters): **80 (BHN)** and **83 (MFG)** — see Live assignments and the ranking
  rationale. **81 (BRS)** and **82 (EXT3)** are the new reserve.

**Two landings and a promotion, both good news.**

- **Leg 73 (BV) landed with an excellent result: `boussinesq_velocity.py` now has its first
  EXTERNAL known-answer gate** — reproduces the classical Lamb corner-image closed form to
  1.76e-4 relative, a 57x margin. This is the strongest positive validation any infrastructure
  leg has produced this cycle; bank it as the module's permanent external check. Slot vacated.
- **Leg 79's bench-repair landed, bundled with leg 79's own finding: `port_certification.py`'s
  fabrication-rejection gap is fixed** — 11/25 false `closes=True` results is now 0/25.
  `solver/interval.py`, `solver/spectral_utils.py` and `solver/port_certification.py` have **all
  three had their repairs land** and are no longer off-limits for any purpose.
- **82 (EXT3) promoted into the slot leg 73 vacated (the coordinator's LEG-G).** The live table
  also shows **81 (BRS) already dispatched into LEG-E**, which means leg 61 (KA) must have
  landed too, unreported in detail — consistent with the coordinator's newest "avoid" list no
  longer naming `interval_certificate.py`. That fully accounts for "reserve is fully empty":
  both remaining reserve items (81, 82) got dispatched, not just one. **Current live count:
  nine, LEG-D still held open for 76:** 58 (NG, critical), 62 (CP), 63 (M2), 81 (BRS), 71 (CAP),
  82 (EXT3), 80 (BHN), 78 (HLB), 83 (MFG). **Four fresh candidates (84–87) are added below for
  the next refill; no immediate promotion requested this time ("no rush") — all four are
  reserve.**

**Leg 63 (M2) landed: gate YES — the most consequential landing of this entire run.** Full
detail is in leg 63's queue entry above (now marked LANDED) and in the new "Open direction
questions" §2 below: the target-reselection screen found exactly one candidate that passes the
multiplier/shift predicate — gCLM with full Laplacian dissipation (γ=2) — where every inviscid
target ever ranked fails it identically. Blow-up is proved for this model and no CAP of any
dissipative self-similar profile exists in the literature leg 63 searched. This is escalation
#1, correctly parked (`leg/m2-v1`, not merged) rather than decided by the leg or by this file —
promoting it is the user's call. **Per the coordinator's explicit instruction, no dispatchable
leg has been drafted for the γ=2 candidate; an unofficial, clearly-marked non-dispatchable
sketch of what a first leg would need is appended after the open questions, so there is no
restart cost if the user rules to pursue it.** This does not change queue mechanics — LEG-C is
simply open now, refilled from ordinary reserve below like any other landing.

**Slot refill: all of 58–87 have been dispatched at some point; reserve is exhausted again.**
The coordinator confirms LEG-C=85 (GRA, replacing 63 after its landing), LEG-G=87 (IVB,
replacing 82), LEG-I=86 (PCB, replacing 78) are now live. The Live assignments table below also
already shows **LEG-E=84 (TNA)**, which resolves cleanly: leg 81 (BRS) must have landed too
(unreported in detail) and all four of the prior batch (84–87) are now accounted for and
dispatched — matching "reserve is fully exhausted" exactly, with no unexplained leftover.
**Current live nine (LEG-D still held for 76):** 58 (NG, critical, A), 62 (CP, B), 85 (GRA, C),
84 (TNA, E), 71 (CAP, F), 87 (IVB, G), 80 (BHN, H), 86 (PCB, I), 83 (MFG, J). **Four fresh
candidates
(88–91) are added below for the next refill.**

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
| LEG-C | 90 | **EXT4** — has the rank-4 target's Conjecture 2.4 been resolved since? | no | light | `leg/ext4-v1` | Has Chen-Huang-Li's Conjecture 2.4 (HL singular steady stability) been proved or disproved since? |
| LEG-D | — | **OPEN, held for leg 76 (MI)** pending its verifier's confirmation of leg 70's finding | — | — | — | — |
| LEG-E | 84 | **TNA** — does target_norm.py silently extrapolate beyond its validated domain? | no | standard | `leg/tna-v1` | Under adversarial inputs past X_max=745, does target_norm.py silently return an untrustworthy result or flag the violation? |
| LEG-F | 71 | **CAP** — capabilities.py self-audit | no | light | `leg/cap-v1` | Does every module row in capabilities.py have a test file that exists, is collected, and passes at HEAD? |
| LEG-G | 91 | **FGA** — adversarial audit of fractional_gclm.py's critical-exponent computation | no | standard | `leg/fga-v1` | Under malformed dissipation-strength inputs, does s_c computation silently return a plausible-looking wrong value? |
| LEG-H | 88 | **GCA** — adversarial audit of gclm_family.py's residual computation | no | standard | `leg/gca-v1` | Under NaN/Inf-poisoned coefficients, does the residual silently return a plausible-looking wrong value? |
| LEG-I | 89 | **BOA** — adversarial audit of boussinesq.py | no | standard | `leg/boa-v1` | Under malformed physical-space inputs, does the module silently return a plausible-looking wrong result? |
| LEG-J | 83 | **MFG** — adversarial audit of marginal_flow.py's gate 11 | no | standard | `leg/mfg-v1` | Does gate 11 catch non-NaN divergent trajectories, or only the NaN case it was built for? |

**Several earlier paragraphs above ("third pass," "second pass," and their predecessors)
recorded intermediate states that have since been overtaken by further landings; this paragraph
is the single current, authoritative account and supersedes all of them.** Current live nine
(LEG-D held open for leg 76, not filled by anything else): **58** (NG, critical path, LEG-A),
**62** (CP, LEG-B), **63** (M2, LEG-C), **81** (BRS, LEG-E — landed in after leg 61/KA landed,
unreported in detail), **71** (CAP, LEG-F, narrow field only), **82** (EXT3, LEG-G — landed in
after leg 73/BV's excellent result), **80** (BHN, LEG-H), **78** (HLB, LEG-I), **83** (MFG,
LEG-J). Reserve is empty; **84–87 below are the new reserve, no immediate promotion requested
("no rush").** Slot letters are the orchestrator's bookkeeping and have drifted from this file's
labels more than once — leg numbers and territory are the ground truth this file tracks;
letter-for-letter reconciliation is not chased once the leg-number set and territory check out.

Figure numbers pre-allocated: leg 58 → `fig55`, 62 → `fig56`, 63 → `fig57`, 59 → `fig58`,
60 → `fig59`/`fig60`, **73 → a new figure for the Lamb corner-image comparison** (first external
positive-validation figure since 68; number to be assigned by the leg that writes it up, since
this cycle's audit/literature legs have not needed sequential figures). Every other live and
reserve leg (61, 71, 78, 80, 81, 82, 83, 84–87, and every landed/superseded audit-family leg) is
audit/literature/hygiene and registers **no figure**, by the convention established for Route-D
scope (advection) and Route-D v15 (literature scope) — "no measurement, no figure."
`writeup/build_figures.py` and `writeup/curate_evidence.py` stay **append-only**.

**Territory-overlap check (explicit, as required).** Solver modules touched by the current live
nine plus the four new reserve candidates (58, 62, 85, 84, 71, 87, 80, 86, 83, 88, 89, 90, 91):
`spectral_certificate.py`(58), `certificate_shapes.py`+`literature_gates.py`(62),
none-owned/read-only(85 reads `gclm_rescaled.py`, edits nothing under a bug-found outcome),
none-owned/read-only(84 reads `target_norm.py`, edits nothing), `capabilities.py`(71, factual
"test"-field only, pre-committed narrow), none-owned/read-only(87 reads `interval.py`, fully
repaired and unclaimed, edits nothing), `bordered_hl.py`(80), none-owned/read-only(86 reads
`port_certification.py`, fully repaired and unclaimed, edits nothing), `marginal_flow.py`(83),
none-owned/read-only(88 reads `gclm_family.py`, edits nothing), none-owned/read-only(89 reads
`boussinesq.py`, edits nothing), none(90, literature watch, no code edits), none-owned/read-only
(91 reads `fractional_gclm.py`, edits nothing). All thirteen distinct — **no collision.**
`target_selection.py`(63) is **off the live list** — leg 63's branch is parked pending the
user's ruling (see Status and Open direction questions §2); no live or reserve leg touches it
while that's pending, to avoid a merge conflict with whatever the user decides. `hl_rescaled.py`
(78) and `boussinesq_rescaled.py`(81) are similarly no longer claimed (both legs landed) and are
free for a future candidate if needed, but none of 88-91 uses them, so no re-verification of
that freedom was required here. LEG-D stays empty pending leg 76, whose territory
(`PHASE2_P2_NOTES.md`, `TECHNICAL_P2_ROUTEI_V1.md`) no live or reserve leg touches.
`solver/interval.py`, `solver/spectral_utils.py` and `solver/port_certification.py` remain fully
repaired and unclaimed. `writeup/data` JSON files for the current live nine plus reserve are
likewise distinct names (`p2_route_ng_v1_nogo.json`(58), `p2_route_cp_v1_cadiot.json`(62),
`p2_route_gra_v1_adversarial.json`(85), `p2_route_tna_v1_domain_audit.json`(84),
`p2_route_cap_v1_audit.json`(71), `p2_route_ivb_v1_postrepair.json`(87),
`p2_route_bhn_v1_adversarial.json`(80), `p2_route_pcb_v1_postrepair.json`(86),
`p2_route_mfg_v1_adversarial.json`(83), `p2_route_gca_v1_adversarial.json`(88),
`p2_route_boa_v1_adversarial.json`(89), `p2_route_ext4_v1_target_watch4.json`(90),
`p2_route_fga_v1_adversarial.json`(91)) — **no collision.**

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
### 63 — ROUTE-M2: TARGET RESELECTION, SCREENED BY THE MEASURED PREDICATE (LANDED: gate YES —
escalation #1, parked on `leg/m2-v1`, not merged; see Status and the new §D2 note below)
**Landed finding.** Every inviscid target this repository has ever ranked (including
HL_S2_nonsymmetric) fails the multiplier/shift screen identically — tail-inverse K-exponent
`+0.4372`, all four rows, the same mechanism legs 51-57 characterized. One candidate does NOT
fail it: **gCLM with full Laplacian dissipation (γ=2)**, tail-inverse K-exponent `-2.0270`,
robust across all 3 dissipation strengths tested. Blow-up on this model is proved (Chen
arXiv:1908.09385); no computer-assisted certificate of any dissipative self-similar profile
exists in the literature leg 63 searched. Leg 63 surfaced three readings and correctly picked
none — this is escalation #1 by this file's own §1 ("promoting an exploration route into the
committed sequence"), since acting on it would re-open stage V's dissipative direction, whose
ban ("needs L1 first") may be permanently unmeetable now that L1 is measured dead in both
realizations. Parked for the user; not this file's call to make.
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
### 61 — ROUTE-KA: A KNOWN-ANSWER WINDOW FOR THE WHOLE INTERVAL PIPELINE (LANDED; gate outcome
not individually reported to the DM — inferred landed because LEG-E now runs leg 81 and
`interval_certificate.py` no longer appears in the coordinator's live-territory list)
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

```
### 72 — ROUTE-JR: `experiments/JOURNAL.md` / `experiments/journal/` FRESHNESS AUDIT
**Thesis.** The same staleness failure mode leg 68 (IX) found and fixed in `writeup/INDEX.md`
exists one level down, in the narrative journal. `experiments/JOURNAL.md`'s most recent entry
is "Legs 54-57 (2026-08-05)" -- every leg landed since (58's branch, 60, 64, 65, 66, 68, 69, and
whatever lands between now and this leg's dispatch) has no narrative pointer in the journal, even
though the per-leg detail files it should point to (`experiments/journal/leg_N.md`) mostly exist.
Checked directly while drafting this leg: `experiments/journal/leg_60.md` is **missing entirely**
despite leg 60 (PQ) having landed and escalated -- a leg whose gate answered NO and which is
sitting in `PROGRESS.md`'s escalations right now is exactly the kind of result a future DM or
agent most needs to be able to find fast, and today it cannot be found by leg number at all. This
leg is a straight extension of leg 68's audit pattern to the journal.
**Gate.** Does `experiments/JOURNAL.md`'s narrative and `experiments/journal/`'s per-leg file
exist for every leg that has landed (gate has answered) since the "Legs 54-57" entry?
  yes -> Confirmed current; report and close as a clean audit, no edits needed.
  no  -> Append terse, pointer-only narrative entries to `experiments/JOURNAL.md` (mirroring the
         existing "Legs 54-57" block's style -- one line per leg, sourced from each leg's own PR
         body / `experiments/journal/leg_N.md`, never re-deriving a number), and separately list
         which `experiments/journal/leg_N.md` files are missing as a report item -- this leg does
         NOT create a missing leg's own journal file on that leg's behalf, since that file is
         part of the original leg's own territory, not this audit's.
**Territory.** experiments/JOURNAL.md (append-only edit), writeup/novelty/leg_72.md,
               experiments/journal/leg_72.md
**Difficulty.** light
**Independence.** Touches one file (plus its own two report files) outside any other leg's
territory. Reads, never edits, individual `experiments/journal/leg_N.md` files.
```

```
### 73 — ROUTE-BV: EXTERNAL KNOWN-ANSWER CHECK FOR THE 2D VELOCITY SOLVER (LANDED: gate YES)
**Landed finding:** `boussinesq_velocity.py` now has its first external known-answer gate —
reproduces the classical Lamb corner-image closed form to 1.76e-4 relative, a 57x margin. The
strongest positive validation result of this cycle; banked as the module's permanent external
check.
**Thesis.** solver/boussinesq_velocity.py's validated line covers manufactured stream-function
solutions and a self-consistency gate (the Route-L line sweep, checked against the operator it
inverts -- an internal check, not an external one). It has never been checked against a
PUBLISHED, independent benchmark for the polar-grid Biot-Savart / stream-function solve, which
is exactly the shape of gap leg 61 (KA) closed for the interval pipeline against CLN's Kawahara
radius. This module sits underneath every live 2D Boussinesq route (boussinesq_rescaled.py,
fractional_boussinesq.py, and historically the whole Route-A/Phase-1/Spike arcs), so a first
external validation strengthens the same shared-infrastructure case leg 69 (IA) made for
solver/interval.py, just for the velocity solve. Search the literature (Chen-Hou-Huang's own
validation tables are the first place to look, since this repository's boussinesq_rescaled.py
already reproduces their beta) for a suitable closed-form or independently-published benchmark
solution, then run the existing solver against it.
**Gate.** Does a published, independent benchmark exist for the 2D polar-grid Biot-Savart /
stream-function solve, and does solver/boussinesq_velocity.py reproduce it to a pre-committed
tolerance?
  yes, and it reproduces -> Bank the module's first external known-answer gate; cite it from
         every route that imports this module.
  yes, but it disagrees -> A priority bug report: the shared velocity solve disagrees with a
         published answer. Escalate immediately, do not patch under this leg's own authority.
  no benchmark found -> Report the literature search as negative and leave the module's
         validation explicitly flagged as manufactured-solutions-only; no code change.
**Territory.** experiments/p2_route_bv_v1_velocity_benchmark.py,
               writeup/data/p2_route_bv_v1_velocity_benchmark.json,
               writeup/novelty/leg_73.md, experiments/journal/leg_73.md
**Difficulty.** standard
**Independence.** Reads solver/boussinesq_velocity.py; edits nothing under any gate outcome
(a disagreement escalates rather than patches, by the same discipline as legs 69 and 66). Owns
no solver module. No other live or new leg touches this module.
```

```
### 74 — ROUTE-EXT: HAS THE TARGET OBJECT BEEN CERTIFIED BY ANYONE ELSE SINCE?
**Thesis.** target_selection.py's TARGET_LEDGER records HL_S2_nonsymmetric (arXiv:2604.01868,
Chen-Huang-Li) as "certified: NO" and this repository's own attempt (Route-PORT, legs 44-47) got
stuck 1.55e8 ball radii outside the truncated object, with reach making it worse. That was as of
the original April 2026 report. Nobody in this project has since checked whether Chen-Huang-Li or
anyone else has published a certificate for this specific profile in the months since -- if
someone has, the port this repository spent four legs on is externally mooted, which is exactly
the kind of fact a target ledger should not be stale about. This is a pure literature watch: it
does not touch target_selection.py (leg 63/M2 owns that file and any ledger update it implies),
just reports what a search finds, dated, so a future leg or the user can act on it.
**Gate.** Has a certificate (computer-assisted or analytic) for arXiv:2604.01868's
HL_S2_nonsymmetric profile been published, by Chen-Huang-Li or anyone else, since April 2026?
  yes -> The `certified: NO` field in target_selection.py's TARGET_LEDGER is stale. Report the
         citation precisely (paper, date, method) for leg 63 or a future leg to act on -- this
         leg does not self-edit target_selection.py, which is exclusively owned elsewhere.
  no  -> Confirmed still uncertified as of this leg's search date. Bank the dated literature-
         watch entry; no ledger change needed.
**Territory.** experiments/p2_route_ext_v1_target_watch.py,
               writeup/data/p2_route_ext_v1_target_watch.json,
               writeup/novelty/leg_74.md, experiments/journal/leg_74.md
**Difficulty.** standard
**Independence.** Does not touch solver/target_selection.py (read-only reference to its published
TARGET_LEDGER entry via the PDF citation already recorded there, not the code). No other leg
does this specific dated literature check.
```

```
### 75 — ROUTE-LM: BENCHMARK THE CLAIMED 10x CACHED-SLOPE SPEEDUP
**Thesis.** capabilities.py's line_hilbert.py entry holds "the cached slope operator
`slope_matrix` (Route-M: 10x on the Scenario-2 step)" as a holds-field claim, not a validated
one -- it is a performance number, never independently re-benchmarked since it was first
measured, and performance claims are exactly the kind of thing that silently drifts under
refactors (the same failure class leg 66 just found in spectral_utils.py, just for speed instead
of correctness). This is an engineering-audit leg in the same family as leg 69 (IA): does the
claimed speedup still hold on current code, on the same step it was originally measured on.
**Gate.** Does the cached `slope_matrix` path reproduce a speedup at or above 8x (near the
claimed 10x, allowing for machine variance) over the uncached path on the Scenario-2 step it was
originally measured on?
  yes -> Confirmed still true. Bank a regression-guarding benchmark test so a future refactor
         that silently kills the cache gets caught.
  no  -> The claimed speedup has drifted -- either a regression or the original number was
         measurement noise. Report the current multiplier precisely and flag capabilities.py's
         line for correction (report only; correcting the prose is a follow-up, not this leg's
         own edit, to keep this leg's territory narrow).
**Territory.** test_line_hilbert_benchmark.py, experiments/p2_route_lm_v1_speedup_bench.py,
               writeup/data/p2_route_lm_v1_speedup_bench.json,
               writeup/novelty/leg_75.md, experiments/journal/leg_75.md
**Difficulty.** light
**Independence.** Reads solver/line_hilbert.py; edits nothing in solver/. New test file claimed
by nobody else. Distinct from leg 61 (KA), which checks correctness of a different module
(interval_certificate.py) against a published radius, not speed.
```

```
### 76 — ROUTE-MI: THE MORSE-INDEX CORRECTION (rework leg for leg 70's finding; §7b, not §8)
**Thesis.** Leg 70 (RC) confirmed J-4's "no origin condition" reading (gate NO) but found a
larger problem: the banked "141 of 144 unstable directions at mu=0" claim, quoted across
PHASE2_P2_NOTES.md and multiple writeup files, is not merely under-labelled by realization -- it
is misleading AS A MORSE INDEX. The unstable count is exactly K-3 at K = 48/96/144: a constant
deficit that grows 1:1 with the discretization dimension while max Re barely moves, which is the
textbook signature of a discretized CONTINUUM (an artifact of truncation), not a converged
eigenvalue count. Ten quote sites carry the claim; two (PHASE2_P2_NOTES.md:2176,
TECHNICAL_P2_ROUTEI_V1.md:77 -- "a 141-dimensional unstable manifold") are flatly false in any
realization, not just under-labelled. This is a REWORK leg, not an escalation: the K-3 counts
themselves are not deleted, reinterpreted-away, or contested -- they stay banked exactly as
measured. What gets corrected is the interpretive claim built on top of them. Same territory as
the flawed landing (leg 70's own domain plus the ten quote sites), gate pre-committed to the
corrected measurement, per §7b's own wording for this exact situation.
**Gate.** At all identified quote sites (the ten leg 70 located, plus any further site a grep for
"141" / "unstable direction" / "Morse index" in this context turns up), does the prose now state
the K-3 discretized-continuum reading instead of "a 141-dimensional unstable manifold" or any
other implied-converged-Morse-index framing?
  yes -> All sites corrected; the two flatly-false sites (PHASE2_P2_NOTES.md:2176,
         TECHNICAL_P2_ROUTEI_V1.md:77) rewritten outright, not merely annotated. Banked K-3
         counts themselves untouched -- only their interpretation changes. Lands forward on
         `main` like any other leg; landed history is not rewritten.
  no  -> If any site resists a clean fix (the false framing is load-bearing to a further claim
         this leg cannot itself resolve), escalate that specific site as a scoped question rather
         than leaving it half-corrected or silently reworded around.
**Territory.** PHASE2_P2_NOTES.md (targeted prose edits at the identified sites only, not a
               rewrite of the surrounding sections), writeup/4_p2_lottery/TECHNICAL_P2_ROUTEI_V1.md
               and any other writeup file among leg 70's ten located sites,
               writeup/novelty/leg_76.md, experiments/journal/leg_76.md
**Difficulty.** standard
**Independence.** No live leg claims PHASE2_P2_NOTES.md or TECHNICAL_P2_ROUTEI_V1.md as exclusive
territory. Distinct from leg 70 itself (already landed and closed) -- this is the correction leg
its finding requires, drafted per §7b and held for dispatch until the verifier confirms.
**NOT dispatchable until the verifier confirms leg 70's finding** -- drafted now so it is ready
the moment confirmation lands, per the coordinator's request.
```

```
### 77 — ROUTE-EXT2: HAS THE RANK-2 TARGET OBJECT BEEN CERTIFIED BY ANYONE ELSE SINCE?
**Thesis.** The same gap leg 74 (EXT) checks for the rank-1 target (HL_S2_nonsymmetric) exists
for target_selection.py's rank-2 candidate: gCLM_degenerate_one_scale, the a>0 regular branch
from degenerate data (Huang-Tong-Wang, arXiv:2603.25104, reported numerically in March 2026,
"not been found in previous studies"). Nobody has checked whether a certificate -- computer-
assisted or analytic -- has appeared for this branch since. A different object, a different
paper, independent of leg 74's search and its own dated finding.
**Gate.** Has a certificate (computer-assisted or analytic) for arXiv:2603.25104's
gCLM_degenerate_one_scale branch been published since March 2026?
  yes -> The target_selection.py ledger's entry for this candidate is stale. Report the citation
         precisely for leg 63 (M2) or a future leg to act on -- no self-edit of
         target_selection.py, which is exclusively owned elsewhere.
  no  -> Confirmed still uncertified as of this leg's search date. Bank the dated literature-
         watch entry.
**Territory.** experiments/p2_route_ext2_v1_target_watch2.py,
               writeup/data/p2_route_ext2_v1_target_watch2.json,
               writeup/novelty/leg_77.md, experiments/journal/leg_77.md
**Difficulty.** light
**Independence.** Does not touch solver/target_selection.py. Distinct object and distinct paper
from leg 74; no overlap.
```

```
### 78 — ROUTE-HLB: TIGHTER KNOWN-ANSWER CHECK FOR HL's SCENARIO-2 CONTRACTION RATIO
**Thesis.** solver/hl_rescaled.py's validated line reproduces CHL's Scenario-2 contraction ratio
"to ~1%" -- a loose tolerance that has sat unrevisited since it was first measured. Search for
whether CHL published a higher-precision value, or whether a follow-up paper independently
replicated it to more decimals, the same shape of gap leg 61 (KA) closed for the interval
pipeline against CLN's Kawahara radius, just applied to a looser existing check instead of a
missing one.
**Gate.** Does a primary source publish the Scenario-2 contraction ratio to tighter precision
than the ~1% figure this repository currently checks against, and if so does our number still
agree at that tighter tolerance?
  yes, and it agrees -> Report the tighter figure; flag capabilities.py's tolerance annotation
         for a follow-up correction (report only, not this leg's own edit).
  yes, but it disagrees -> Priority bug report; escalate, do not patch under this leg's own
         authority.
  no tighter value found -> Confirmed ~1% is the best available precision on record. Bank as a
         dated literature-search negative; no change.
**Territory.** experiments/p2_route_hlb_v1_contraction_lit.py,
               writeup/data/p2_route_hlb_v1_contraction_lit.json,
               writeup/novelty/leg_78.md, experiments/journal/leg_78.md
**Difficulty.** light
**Independence.** Reads solver/hl_rescaled.py; edits nothing. No other leg touches this module or
this specific claim.
```

```
### 79 — ROUTE-PC: ADVERSARIAL FABRICATION-REJECTION AUDIT OF THE L1->L2 PORT (LANDED: gate NO)
**Landed finding:** `radii_polynomial_status` does no domain validation -- 11/25 adversarial
hypothesis-violating inputs (negative/NaN Y_0, Z_1, Z_2) incorrectly returned `closes=True`,
including a bare sign-flip case. Severity latent (both in-repo callers pass `(None, None)`, no
banked result affected). Bench-repair dispatched to add validation; `solver/port_certification.py`
is off-limits for editing by any new candidate until it lands.
**Thesis.** solver/port_certification.py's validated line claims `radii_polynomial_status`
"returns BLOCKED_AT_STEP_ONE and is gated to carry NO fabricated Y_0 or Z_1" -- a logic property,
distinct from leg 69 (IA)'s arithmetic-precision stress test of solver/interval.py. IA found real
soundness gaps in the shared interval core; this leg checks whether a DOWNSTREAM consumer's
fabrication-rejection guard is equally robust, under a fresh adversarial battery of poisoned
Y_0/Z_1 inputs (values that look plausible but were never actually derived from a certificate
run) -- complementary coverage of the same certificate-infrastructure family IA and KA already
established has real value.
**Gate.** Under an adversarial battery of fabricated/poisoned Y_0 and Z_1 inputs, does
`radii_polynomial_status` still correctly reject every one and continue returning
BLOCKED_AT_STEP_ONE where appropriate?
  yes -> Confirmed robust. Bank the battery as a permanent regression test.
  no  -> A fabrication-rejection gap in certificate-adjacent infrastructure. Report the exact
         failing case precisely and escalate as a priority finding -- do not patch under this
         leg's own authority.
**Territory.** test_port_certification_regression.py,
               experiments/p2_route_pc_v1_regression.py,
               writeup/data/p2_route_pc_v1_regression.json,
               writeup/novelty/leg_79.md, experiments/journal/leg_79.md
**Difficulty.** light
**Independence.** Reads solver/port_certification.py; edits nothing. New test file claimed by
nobody else. Complementary to, not dependent on, leg 69's interval.py stress test -- this leg's
gate is a logic property, not an arithmetic-precision one, so it is valid regardless of the
interval.py bench-repair's timing.
```

```
### 80 — ROUTE-BHN: ADVERSARIAL AUDIT OF THE BORDERED HL NEWTON SOLVE
**Thesis.** Legs 69 (IA) and 79 (PC) each found a real soundness or logic gap by running an
adversarial battery against infrastructure that had only ever been validated on well-behaved
inputs. solver/bordered_hl.py's damped Newton solve has the same shape of exposure:
capabilities.py validates it against Newton convergence "to 5.66e-15 at n=201" and a contraction
ratio extrapolation, both on WELL-POSED starting data. Nobody has checked whether its
convergence-reporting can be fooled -- a near-singular Jacobian, a NaN/Inf-poisoned initial
iterate, or a residual oscillating just above/below tolerance that the damping accepts anyway.
This is the third leg in the productive adversarial-audit family (after IA and PC), applied to
the one Newton solver in the certificate stack that hasn't been stress-tested this way yet.
**Gate.** Under an adversarial battery (near-singular Jacobian at the starting iterate,
NaN/Inf-poisoned initial guess, a residual sequence oscillating just above and below tolerance),
does solver/bordered_hl.py's damped Newton solve ever incorrectly report convergence?
  yes -> A real false-convergence gap in certificate-adjacent infrastructure. Report the exact
         failing case precisely; escalate, do not patch under this leg's own authority (same
         discipline as legs 69, 66, 79).
  no  -> Confirmed robust under the battery. Bank it as a permanent regression test.
**Territory.** test_bordered_hl_adversarial.py, experiments/p2_route_bhn_v1_adversarial.py,
               writeup/data/p2_route_bhn_v1_adversarial.json,
               writeup/novelty/leg_80.md, experiments/journal/leg_80.md
**Difficulty.** standard
**Independence.** Reads solver/bordered_hl.py; edits nothing under any outcome. New test file
claimed by nobody else. Does not touch solver/port_certification.py (currently under
bench-repair) or solver/interval.py / solver/spectral_utils.py (repairs landed, but this leg
doesn't need them regardless).
```

```
### 81 — ROUTE-BRS: DOES boussinesq_rescaled.py EVER CONFLATE "RESOLUTION-STABLE" WITH "CONVERGED"?
**Thesis.** capabilities.py's own validated line for solver/boussinesq_rescaled.py records a
known trap: "Route-K showed the relaxation LIMIT-CYCLES and its residual GROWS under refinement,
so 'resolution-stable' here is NOT 'converged'." That caveat describes a property of the
PHYSICS (the relaxation doesn't actually converge), but it says nothing about whether the
module's own status/exit-reporting logic could still be fooled into flagging a limit-cycling run
as stable or converged -- a labeling bug distinct from the physics itself, and exactly the kind
of thing leg 66 found in a neighboring module (a correctness bug hiding behind physics nobody
had re-examined at the code level). This does not re-measure beta (banned, leg 43) and does not
run any new physics -- it audits the STATUS-REPORTING code path against the refinement ladder
already on record from Route-K.
**Gate.** At the grid refinement levels where Route-K already measured the residual GROWING
(limit-cycling), does solver/boussinesq_rescaled.py's own relaxation loop ever report a
converged/stable status?
  yes -> A false-positive convergence report at exactly the refinement levels already known to
         limit-cycle. Report precisely; escalate, do not patch under this leg's own authority.
  no  -> Confirmed the module never claims convergence it hasn't earned. Bank as a regression
         check tied to the refinement ladder already on record.
**Territory.** test_boussinesq_rescaled_status.py, experiments/p2_route_brs_v1_status_audit.py,
               writeup/data/p2_route_brs_v1_status_audit.json,
               writeup/novelty/leg_81.md, experiments/journal/leg_81.md
**Difficulty.** standard
**Independence.** Reads solver/boussinesq_rescaled.py; edits nothing under any outcome. Distinct
quantity and distinct question from leg 43's banned beta re-measurement (status-reporting logic,
not a physics number) and from leg 73 (BV)'s external check of boussinesq_velocity.py (a
different module).
```

```
### 82 — ROUTE-EXT3: HAS THE RANK-3 TARGET OBJECT BEEN CERTIFIED BY ANYONE ELSE SINCE?
**Thesis.** The same dated literature watch legs 74 (EXT, rank 1) and 77 (EXT2, rank 2) ran --
both landed NO, still uncertified -- applies to target_selection.py's rank-3 candidate:
Boussinesq_S2_nonsymmetric (Chen-Huang-Li, arXiv:2604.01868 section 6.2, the 2D analogue of the
rank-1 1D object). A different object, a different section of a paper already partially read by
this repository (section 2.5/4 for rank 1), independent of legs 74 and 77's own dated findings.
**Gate.** Has a certificate (computer-assisted or analytic) for arXiv:2604.01868 section 6.2's
Boussinesq_S2_nonsymmetric profile been published since the paper's own date?
  yes -> The target_selection.py ledger's entry for this candidate is stale. Report the citation
         precisely for leg 63 (M2) or a future leg to act on -- no self-edit of
         target_selection.py, which is exclusively owned elsewhere.
  no  -> Confirmed still uncertified as of this leg's search date. Bank the dated literature-
         watch entry.
**Territory.** experiments/p2_route_ext3_v1_target_watch3.py,
               writeup/data/p2_route_ext3_v1_target_watch3.json,
               writeup/novelty/leg_82.md, experiments/journal/leg_82.md
**Difficulty.** light
**Independence.** Does not touch solver/target_selection.py. Distinct object (2D, not 1D) from
legs 74 and 77, same paper as leg 74 but a different section; no overlap.
```

```
### 83 — ROUTE-MFG: ADVERSARIAL AUDIT OF marginal_flow.py's GATE 11
**Thesis.** solver/marginal_flow.py's validated line records that "gate 11 enforces convergence
(the NaN of leg 41)" -- a gate purpose-built to catch one specific failure mode (a NaN in the
integrated trajectory). It has never been checked against non-NaN divergence: slow unbounded
polynomial growth, or sustained oscillation that never decays but also never produces a NaN.
A gate built to catch one named failure mode passing silently on a DIFFERENT failure mode it was
never tested against is exactly the shape of gap legs 69, 66 and 79 each found elsewhere in this
repository's infrastructure. This is a robustness audit of existing convergence-checking code,
not a new gCLM physics measurement -- no new parameter sweep, no new profile, just adversarial
inputs against an existing gate's catch coverage.
**Gate.** Under an adversarial battery of non-NaN divergent trajectories (slow polynomial
blowup, sustained non-decaying oscillation), does gate 11 correctly flag non-convergence, or does
it only catch the NaN case it was built for?
  yes (catches all) -> Confirmed gate 11's coverage is broader than its original design case.
         Bank the battery as a permanent regression test.
  no (misses some) -> Gate 11 has a narrower catch than assumed. Report the exact failing
         trajectory precisely; escalate, do not patch under this leg's own authority.
**Territory.** test_marginal_flow_adversarial.py, experiments/p2_route_mfg_v1_adversarial.py,
               writeup/data/p2_route_mfg_v1_adversarial.json,
               writeup/novelty/leg_83.md, experiments/journal/leg_83.md
**Difficulty.** standard
**Independence.** Reads solver/marginal_flow.py; edits nothing under any outcome. New test file
claimed by nobody else. A robustness audit of the gate's catch coverage, not a new physics
measurement, so it does not fall under the gCLM-measurement ban (leg 42).
```

```
### 84 — ROUTE-TNA: DOES target_norm.py SILENTLY EXTRAPOLATE BEYOND ITS VALIDATED DOMAIN?
**Thesis.** solver/target_norm.py's own validated line already documents a known limitation:
"DOMAIN-limited, not resolution-limited: at the shipped X_max = 745 the far-field closure moves
the exponent by 0.190 and the measurement is not trustworthy there." That is a property of the
PHYSICS/numerics leg 55 (NB) already characterized. What has never been checked is whether the
CODE itself detects and flags that domain violation, or silently returns a number with no signal
that the caller has left the validated window -- exactly the shape of gap the adversarial-audit
family (69, 66, 79) keeps finding: a documented limitation with no corresponding guard in code.
**Gate.** Under adversarial inputs that push sample points beyond the validated X_max = 745
window (or otherwise into the region capabilities.py already flags as untrustworthy), does
target_norm.py silently return a result with no warning or flag, or does it correctly signal the
domain violation?
  yes (silent) -> A real gap: a caller could unknowingly rely on an untrustworthy exponent
         outside the validated window. Report precisely; escalate, do not patch under this leg's
         own authority.
  no (flags correctly) -> Confirmed robust. Bank the battery as a permanent regression test
         locking in the domain guard.
**Territory.** test_target_norm_adversarial.py, experiments/p2_route_tna_v1_domain_audit.py,
               writeup/data/p2_route_tna_v1_domain_audit.json,
               writeup/novelty/leg_84.md, experiments/journal/leg_84.md
**Difficulty.** standard
**Independence.** Reads solver/target_norm.py; edits nothing under any outcome. New test file
claimed by nobody else. Distinct from leg 55 (NB, landed), which measured the physics; this leg
audits whether the code surfaces the already-known limitation.
```

```
### 85 — ROUTE-GRA: ADVERSARIAL AUDIT OF gclm_rescaled.py's FIXED-POINT REPORTING
**Thesis.** solver/gclm_rescaled.py's validated line confirms it "relaxes to the exact CLM
self-similar fixed point" -- on well-behaved data. Its relaxation loop's own convergence
reporting has never been checked against adversarial non-convergent trajectories: oscillation
around the fixed point without decaying into it, or slow drift past a saddle. Same pattern as
leg 83 (MFG), applied to the sibling 1D CLM module instead of the augmented flow. This is a
STATUS-REPORTING robustness audit of existing code, not a new gCLM physics measurement or
parameter sweep -- it does not touch the gCLM-measurement ban (leg 42) for the same reason leg
83 does not.
**Gate.** Under an adversarial battery of non-convergent upwind-transport trajectories
(sustained oscillation, slow drift near a saddle rather than the fixed point), does
solver/gclm_rescaled.py's relaxation loop ever report having reached the fixed point when it
has not?
  yes -> A false-positive convergence report. Report the exact failing trajectory precisely;
         escalate, do not patch under this leg's own authority.
  no  -> Confirmed robust. Bank the battery as a permanent regression test.
**Territory.** test_gclm_rescaled_adversarial.py, experiments/p2_route_gra_v1_adversarial.py,
               writeup/data/p2_route_gra_v1_adversarial.json,
               writeup/novelty/leg_85.md, experiments/journal/leg_85.md
**Difficulty.** standard
**Independence.** Reads solver/gclm_rescaled.py; edits nothing under any outcome. New test file
claimed by nobody else. A robustness audit of convergence-reporting, not a new physics
measurement -- the same distinction that clears leg 83.
```

```
### 86 — ROUTE-PCB: POST-REPAIR REGRESSION CHECK, port_certification.py
**Thesis.** Leg 79's bench-repair just added domain validation to `radii_polynomial_status`
(11/25 false `closes=True` results -> 0/25) inside a module whose OTHER claim -- the line-sweep
preconditioner gated to 9.5e-16 against the operator it inverts -- has not been independently
re-checked since the repair landed. New validation branches in a hot path are a classic place
for an accidental precision or performance regression to hide. This closes the loop on leg 79's
finding the same way leg 87 (below) closes the loop on leg 69's.
**Gate.** After the bench-repair, does solver/port_certification.py's line-sweep preconditioner
still (a) hit the 9.5e-16 precision gate it was originally validated to, and (b) run within
normal benchmark variance of its pre-repair timing?
  yes -> Confirmed the repair was surgical -- no precision or performance regression. Bank as a
         permanent post-repair regression test.
  no  -> Report the exact discrepancy (precision or timing) precisely; escalate as a priority
         finding, do not patch under this leg's own authority.
**Territory.** test_port_certification_postrepair.py,
               experiments/p2_route_pcb_v1_postrepair.py,
               writeup/data/p2_route_pcb_v1_postrepair.json,
               writeup/novelty/leg_86.md, experiments/journal/leg_86.md
**Difficulty.** light
**Independence.** Reads solver/port_certification.py, now fully repaired and unclaimed; edits
nothing. New test file claimed by nobody else. Distinct question from leg 79 (precision/
performance regression, not fabrication-rejection).
```

```
### 87 — ROUTE-IVB: POST-REPAIR REGRESSION CHECK, interval.py
**Thesis.** Leg 69's bench-repair fixed two real soundness gaps in the shared interval core
(subnormal-range false negatives, a silent NaN above 2^997). Nobody has independently re-run
leg 69's original adversarial corpus against the repaired module, nor confirmed that the fix did
not regress the previously-validated exact-rational containment checks at the live operator
range (K = 0.5-128) that legs 58 and 61 actually depend on. Closes the loop the same way leg 86
closes it for leg 79's repair.
**Gate.** Does solver/interval.py, post-repair, (a) correctly handle leg 69's original failing
cases (the subnormal range, 2^997), and (b) show zero regression in the previously-validated
exact-rational containment checks at the live K-range?
  yes -> Confirmed the repair is solid and non-regressive. Bank leg 69's adversarial corpus plus
         this leg's fresh battery as a permanent regression suite.
  no  -> An incomplete fix or a repair regression. Report the exact case precisely; escalate as a
         priority finding, do not patch under this leg's own authority.
**Territory.** test_interval_postrepair.py, experiments/p2_route_ivb_v1_postrepair.py,
               writeup/data/p2_route_ivb_v1_postrepair.json,
               writeup/novelty/leg_87.md, experiments/journal/leg_87.md
**Difficulty.** standard
**Independence.** Reads solver/interval.py, now fully repaired and unclaimed; edits nothing. New
test file claimed by nobody else. Closes the loop on leg 69's finding, the highest-consequence
repair of this cycle (shared by legs 58 and 61).
```

```
### 88 — ROUTE-GCA: ADVERSARIAL AUDIT OF gclm_family.py's RESIDUAL COMPUTATION
**Thesis.** solver/gclm_family.py holds the a-family sinh-grid residual
`R = (c_omega + H Omega) Omega - c_l X Omega_X - a U Omega_X`, validated on the exact a=0 profile
(RMS 2.2e-7) -- well-behaved data only. Nobody has checked whether it silently returns a
finite-looking but wrong residual under adversarial coefficient inputs (NaN-poisoned `c_l` or
`c_omega`, wildly out-of-range `a`), rather than flagging the problem. Same adversarial-audit
pattern as legs 69/79/80/83/85, applied to a module none of them has touched. This is a
robustness audit of existing residual-computation code, not a new gCLM physics measurement or
parameter sweep, so it does not fall under the gCLM-measurement ban (leg 42) -- the same
distinction that clears legs 83 and 85.
**Gate.** Under an adversarial battery (NaN/Inf-poisoned `c_l`/`c_omega`, `a` far outside
`[0,1]`), does solver/gclm_family.py's residual computation ever silently return a finite,
plausible-looking value instead of propagating the invalid input or flagging it?
  yes -> A silent-corruption gap. Report the exact failing case precisely; escalate, do not
         patch under this leg's own authority.
  no  -> Confirmed robust. Bank the battery as a permanent regression test.
**Territory.** test_gclm_family_adversarial.py, experiments/p2_route_gca_v1_adversarial.py,
               writeup/data/p2_route_gca_v1_adversarial.json,
               writeup/novelty/leg_88.md, experiments/journal/leg_88.md
**Difficulty.** standard
**Independence.** Reads solver/gclm_family.py; edits nothing under any outcome. New test file
claimed by nobody else. Distinct module from every other adversarial-audit leg dispatched so
far.
```

```
### 89 — ROUTE-BOA: ADVERSARIAL AUDIT OF boussinesq.py (PHYSICAL-SPACE 2D BOUSSINESQ)
**Thesis.** solver/boussinesq.py got dedicated test coverage from leg 66 (QF), which asked
"does a direct test find any discrepancy against what the indirect tests assumed" and answered
no. That is a correctness check on well-behaved inputs, not a robustness check -- the same gap
in kind that made legs 69, 79, 80, 83, 85 and 88 each worth running: does the module silently
produce a wrong-but-plausible result under adversarial physical-space inputs (NaN-seeded initial
vorticity, an all-zero or degenerate stream function, extreme grid-stretching parameters) rather
than flagging them.
**Gate.** Under an adversarial battery of malformed physical-space inputs (NaN-seeded vorticity,
degenerate/zero stream function, extreme grid-stretching), does solver/boussinesq.py ever
silently return a finite, plausible-looking result instead of propagating or flagging the
invalid input?
  yes -> A silent-corruption gap. Report the exact failing case precisely; escalate, do not
         patch under this leg's own authority.
  no  -> Confirmed robust. Bank the battery as a permanent regression test.
**Territory.** test_boussinesq_adversarial.py, experiments/p2_route_boa_v1_adversarial.py,
               writeup/data/p2_route_boa_v1_adversarial.json,
               writeup/novelty/leg_89.md, experiments/journal/leg_89.md
**Difficulty.** standard
**Independence.** Reads solver/boussinesq.py; edits nothing under any outcome. New test file
claimed by nobody else. Distinct question from leg 66 (QF, landed) -- robustness under
adversarial input, not correctness under well-behaved input.
```

```
### 90 — ROUTE-EXT4: HAS THE RANK-4 TARGET OBJECT'S CONJECTURE BEEN RESOLVED SINCE?
**Thesis.** The dated literature-watch pattern (legs 74/EXT rank 1, 77/EXT2 rank 2, 82/EXT3 rank
3, all landed NO -- still uncertified) extends naturally to target_selection.py's rank-4
candidate: HL_singular_steady_stability (Chen-Huang-Li, arXiv:2604.01868 Theorem 2.3 for
existence, Conjecture 2.4 for stability -- explicitly OPEN, blocked on a function space because
the profile is unbounded and only in L^p for p<2). Unlike ranks 1-3, this one is a named OPEN
CONJECTURE, not merely "uncertified" -- a resolution (either direction) would be unusually
consequential news for this repository's target ledger. A different object, a different
question (a conjecture's resolution, not a certificate's existence), independent of legs 74/77/
82's own dated findings.
**Gate.** Has Chen-Huang-Li's Conjecture 2.4 (stability of the HL singular steady state) been
proved or disproved, by anyone, since arXiv:2604.01868?
  yes -> Materially changes the rank-4 entry's status either way. Report the citation and the
         direction of the result precisely for leg 63's successor or a future leg to act on --
         no self-edit of target_selection.py, which is currently parked pending the user's
         ruling on leg 63's escalation (see Status) and untouched by any other leg regardless.
  no  -> Confirmed still open as of this leg's search date. Bank the dated literature-watch
         entry.
**Territory.** experiments/p2_route_ext4_v1_target_watch4.py,
               writeup/data/p2_route_ext4_v1_target_watch4.json,
               writeup/novelty/leg_90.md, experiments/journal/leg_90.md
**Difficulty.** light
**Independence.** Does not touch solver/target_selection.py (parked pending the user; this leg
reads only the citation already recorded in its ledger). Distinct object/question from legs 74,
77, 82.
```

```
### 91 — ROUTE-FGA: ADVERSARIAL AUDIT OF fractional_gclm.py's CRITICAL-EXPONENT COMPUTATION
**Thesis.** solver/fractional_gclm.py's critical exponent `s_c` is validated against XU eq (6.3)
row by row and marked PRE-EMPTED (Route-J) -- the physics claim is settled and this leg does not
reopen it. What has never been checked is whether the code computing `s_c` is robust to malformed
dissipation-strength inputs: negative `s`, `s` above the model's own admissible threshold, or
NaN-poisoned dissipation parameters. Same adversarial-audit pattern as legs 69/79/80/83/85/88/89,
a robustness check on existing code, not a re-measurement of the (already pre-empted, settled)
physics -- it does not reopen or contest Route-J's finding in any way.
**Gate.** Under an adversarial battery (negative `s`, `s` above the model's admissible
threshold, NaN-poisoned dissipation strength), does solver/fractional_gclm.py's critical-exponent
computation ever silently return a finite, plausible-looking `s_c` instead of propagating or
flagging the invalid input?
  yes -> A silent-corruption gap. Report the exact failing case precisely; escalate, do not
         patch under this leg's own authority.
  no  -> Confirmed robust. Bank the battery as a permanent regression test.
**Territory.** test_fractional_gclm_adversarial.py, experiments/p2_route_fga_v1_adversarial.py,
               writeup/data/p2_route_fga_v1_adversarial.json,
               writeup/novelty/leg_91.md, experiments/journal/leg_91.md
**Difficulty.** standard
**Independence.** Reads solver/fractional_gclm.py; edits nothing under any outcome. New test
file claimed by nobody else. Does not touch or contest the PRE-EMPTED s_c finding (Route-J);
robustness only.
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

**68 (IX) and 66 (QF) were ranked to close out the ten, and both have since landed** — 68 gate
YES (mechanical, INDEX.md fixed), 66 gate **YES** with a real finding: a latent odd-`n`
Nyquist-zeroing bug in `spectral_utils.py`'s `derivative_hat`, zero blast radius today but a
real defect, correctly handed to a bench-repair agent rather than fixed inside the leg. Both
outcomes are exactly what "closing out the ten" was for — cheap slots that turned out to still
find real things.

**64 (A12) was promoted out of reserve into LEG-I** on 68's landing, and **67 (FD) was promoted
into LEG-H** on 65's landing, both per this file's refill instruction and both confirmed correct
by the DM at the time (neither gate outcome changed the ranking picture below it).

**69 (IA) then landed: gate NO, and it is the most consequential landing in this batch.** It
found real soundness gaps in `solver/interval.py` — subnormal-range false negatives, a silent
NaN above `2^997` — the shared primitive both NG (58) and KA (61) depend on. The scoping is what
keeps this from being a stop-the-line event: every live operator's actual range (0.5–128) sits
140–298 decades clear of both failure bands, so neither live leg's numbers are shown to be
affected. Correctly handed to a bench-repair agent (no live leg owns `interval.py` for editing),
and `interval.py` plus `spectral_utils.py` (from 66's finding) are now off-limits for editing by
any new candidate until those repairs land.

**60 (PQ) landed: gate NO, escalation #4.** 111/114 numbers reproduce; two do not, parked on
`leg/pq-v1` and escalated per its own pre-committed no-branch — correctly not self-corrected.
Its landing also surfaced a small territory gap of its own (`experiments/journal/leg_60.md`
missing), which is why leg 72 (JR) below extends leg 68's audit pattern one level down rather
than being invented from nothing.

**With the reserve (70, 71) now exhausted and three slots (F, G, J) needing to be refilled from
new candidates, the promotion choice is 72 (JR) and 73 (BV), in that order of urgency, not 74 or
75.** 72 is the cheapest possible win and already has a concrete finding in hand (the missing
`leg_60.md`) before it even formally dispatches — the same shape of "audit that turns out to be
non-trivial" that 68 and 66 both were, and PQ's own escalation makes fixing the ledger's
discoverability more urgent right now, not less. 73 is ranked next because it is the direct
sibling of 69 (IA) and 61 (KA) — a shared-infrastructure module (`boussinesq_velocity.py`, used
by every 2D Boussinesq route) that has never had an external known-answer check, and 69 just
demonstrated that this repository's infrastructure-audit legs have a real hit rate, not a
theoretical one. **74 (EXT) and 75 (LM) are the new reserve, ranked 3rd and 4th of the new
batch.** EXT is a literature watch on the target object itself — valuable (it would moot four
legs' worth of port-building if a certificate has since appeared) but lower-urgency than an
infrastructure check, since nothing suggests the literature has moved since April 2026. LM is a
performance (not correctness) benchmark — real, cheap, but the stakes of a stale speed claim are
categorically lower than the stakes of a stale correctness or discoverability claim. If another
slot frees up, promote from this list in the order given (EXT, then LM), without re-ranking,
unless a gate answer changes the picture.

**Ordering the queue by proximity to the Clay chain is a choice of what to try. It is never a
claim that anything moved.** In 57 landed legs, no link has moved; Clay stays at ~0.05% behind
Walls 1 and 2. The honest summary of the current queue is the same one the prior session closed
on: **"the only movable link was measured unreachable by this method, in both of its
realizations,"** and this refresh's eight new legs are chosen to protect, document and stress-
test that finding and its surrounding infrastructure — not to reopen it.

## Open direction questions for the user

These also appear under `⚠ NEEDS YOU` in `PROGRESS.md`. The run continues around them.

1. **`NG` entering the committed sequence is escalation #1**, and the DM is making the call
   under the user's explicit pre-delegation ("whichever pursues our goals best"). Flagged here
   so it is visible as a plan change and not just as a queue entry. Reversible: if you would
   rather go straight to the target round, swap slots LEG-A and LEG-C and mark `M2` as `NEXT`
   instead — the cost is that the target screen ships before the predicate it screens with is
   written down. **This question is now overtaken in urgency by #2** — the target round (leg 63)
   has itself landed since this was written, and its answer changes what "going straight to the
   target round" would even mean.
2. **UPDATED, no longer speculative — this is now the single highest-value, most concrete
   decision open on this project.** Leg 63 (M2) landed: gate **YES**. Every inviscid target ever
   ranked fails the multiplier/shift screen identically; **exactly one candidate passes it**:
   gCLM with full Laplacian dissipation (`γ=2`), tail-inverse `K`-exponent `-2.0270`, robust
   across three dissipation strengths. Blow-up on this model is **proved** (Chen
   arXiv:1908.09385), and leg 63's search found **no computer-assisted certificate of any
   dissipative self-similar profile in the literature** — meaning if this repository built one,
   it would very plausibly be genuinely novel, not just novel-against-a-narrow-slice. The
   obstruction is exactly stage `V`'s ban: "re-opening the dissipative direction needs `L1`
   first," and `L1` is measured dead in both realizations. Three readings, and this file does
   not pick one — that is the escalation:
   - **(a) The condition is permanently unmet** — the dissipative direction, the one place leg
     53's positive control shows the instrument actually works (`Z₁ = 0.9156` at `μ = 2`), stays
     closed forever, and leg 63's finding is filed as "identified, not pursued."
   - **(b) Re-word the ban's lift condition** to admit a certificate attempt on `γ=2` directly,
     since the *reason* for the original "`L1` first" requirement (this repository's L1-Fourier
     machinery needing validation before trusting it on a fluid transport model) may not bind
     the same way against a model with *proved* blow-up and *no* prior CAP attempt to fail
     against — there is no L1-shaped precedent for THIS object to be measured dead in the first
     place.
   - **(c) Something in between**: lift the ban narrowly, scoped to this one candidate, with its
     own fresh novelty pass and its own gate, rather than a general re-opening of "the
     dissipative direction."
   Branch `leg/m2-v1` is parked, not merged, pending this ruling. **Per the coordinator's
   request, this file has NOT drafted a dispatchable leg for the `γ=2` candidate** — doing so
   would presuppose the ruling — but a short unofficial sketch of what a first leg on this
   candidate would need is below, so that if you rule in favor of (b) or (c), there is no
   restart cost.
3. **What is the exit criterion for this project?** The prize is a novel Tier-3 result on a
   model where blow-up is provable. `NG`'s yes-branch would deliver a *negative* Tier-3-shaped
   result; leg 63's finding, if pursued, points at a possible *positive* one on a genuinely
   different object. These are no longer a hypothetical pair — both are now live, concrete,
   parked results waiting on user rulings, and the exit-criterion question decides how to weigh
   them against each other, not just in the abstract.

**Unofficial sketch — NOT a dispatchable leg, NOT to be built before the ruling on #2 above.**
If the user green-lights (b) or (c), a first leg on the `γ=2` full-Laplacian gCLM candidate
would plausibly need, in order: (i) a novelty pass specifically on dissipative gCLM CAP
attempts (leg 63 searched broadly for "any dissipative self-similar profile"; a dedicated pass
should search narrowly for `γ=2` / full-Laplacian gCLM specifically, the same discipline leg 62
used for Cadiot against NG); (ii) locate or derive the steady self-similar profile equation
under full Laplacian dissipation and confirm a Newton solve reaches it (the `μ=2` positive
control from leg 53 already shows this repository's certificate machinery can produce `Z₁<1` in
a dissipative setting — that result should be re-read against this specific candidate, not
assumed to transfer); (iii) a fresh multiplier-vs-shift check at the ACTUAL linearization for
this candidate (leg 63's screen used the existing predicate at a coarse level — a dedicated leg
should re-derive the tail-inverse exponent from the candidate's own operator, not the ledger
row); (iv) only then, a certificate attempt. This is a heavy, multi-leg undertaking, not a
single leg — flagged here only so the shape of the work is visible alongside the decision.
