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
refill adds **84–87**, a sixth refill adds **88–91**, a seventh refill adds **92–95**, an eighth
refill adds **96–99**, a ninth refill adds **100–105**, and this tenth refill adds **106–109**.
**Next fresh leg number for any future candidate is 110.**

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
candidates (88–91) are added below for the next refill.**

**Fourth adversarial-audit round: two more real findings, two clean closures, reserve
exhausted again.**

- **Leg 84 (TNA) landed: gate YES**, bundled with its bench-repair. `target_norm.py` now has a
  domain guard, and the repair independently re-checked leg 55 (NB)'s banked margins against
  it — confirmed **not contaminated** (0.0 diff). Slot vacated.
- **Leg 85 (GRA) found a real false-convergence bug**: `gclm_rescaled.py`'s relaxation loop
  reports reaching the fixed point after 1 step on certain gauge-scale trajectories. Bench-repair
  dispatched with leg 85's own suggested one-line fix. `solver/gclm_rescaled.py` is off-limits
  for editing by any new candidate until it lands. Slot vacated.
- **Legs 86 (PCB) and 87 (IVB) both landed: gate YES** — the `port_certification.py` and
  `interval.py` repairs are confirmed solid with zero regression. Both loops fully closed. Slots
  vacated.
- **All of 88–91 dispatched or landed** (coordinator confirms LEG-C=90, LEG-G=91; the remaining
  two, 88 and 89, are inferred into the other two openings — E and I — per this file's reserve
  order, not individually confirmed). **Current live nine (LEG-D still held for 76):** 58 (NG,
  critical, A), 62 (CP, B), 90 (EXT4, C), 88 (GCA, E, inferred), 71 (CAP, F), 91 (FGA, G), 80
  (BHN, H), 89 (BOA, I, inferred), 83 (MFG, J). Reserve is empty. **Four fresh candidates
  (92–95) are added below** — the adversarial-audit pattern's remaining pool of genuinely
  untouched, safe `solver/` modules is thinning, so this batch mixes in one literature watch and
  two post-repair regression closures per the coordinator's suggestion, alongside one more fresh
  adversarial audit.

**Fifth round: two clean literature closures, a real (and serious) bug in `boussinesq.py`, and
useful non-actionable context.**

- **Legs 90 (EXT4) and 93 (EXT5) both landed: gate NO on both, thorough literature work.**
  Chen-Huang-Li's Conjecture 2.4 remains open; no community verdict has appeared on
  arXiv:2604.09949 in the confirm/refute/retract sense leg 93 asked about. Note: leg 93 was
  never explicitly reported as dispatched into a slot in this file's prior update — its landing,
  reopening LEG-J, indicates it was dispatched (presumably replacing leg 83/MFG, which must
  therefore have also landed, unreported) — tracked per this file's established practice of not
  chasing letter-for-letter reconciliation once leg numbers and outcomes are confirmed.
- **Leg 89 (BOA) found a real and serious silent-corruption gap in `solver/boussinesq.py`**: a
  false `blowup_candidate` flag triggered by ordinary floating-point dealiasing noise, amplified
  **5.6e13×**; plus a silently-dropped `kappa` parameter and a NaN-masking bug. This is the
  most severe finding of the whole adversarial-audit run so far — a 5.6e13× amplification of
  numerical noise into a false positive is not a latent edge case, it is a live correctness
  risk. Bench-repair in flight, **specifically investigating whether any banked Phase-1 result
  was affected** — this is the first adversarial-audit finding with a real chance of touching
  an already-published number, so treat its resolution as high-priority reading once it lands.
  `solver/boussinesq.py` is **off-limits for any new candidate** until the repair and its
  banked-result audit both resolve.
- **Non-actionable context from leg 93, worth carrying forward**: arXiv:2604.09949's author has
  since posted 6 papers claiming the OPPOSITE result using the same 5D-lifted machinery, with
  zero cross-citation between them — a de facto self-refutation in the literature. This
  repository's own M-5 audit (checked the arithmetic, found it sound) stands unaffected — the
  self-refutation is about the *conclusion*, not the *computation* M-5 verified. Filed here so a
  future candidate touching this corpus (e.g., a successor to leg 93, or anything referencing
  rank-6 on the target ledger) starts from this context rather than re-discovering it.
- **Reserve check: only leg 95 remains, and it is explicitly not dispatchable** (blocked on
  leg 85's still-in-flight bench-repair). **Four fresh candidates (96–99) are added below; two
  are selected for immediate promotion into LEG-C and LEG-J** (the two the coordinator reports
  open): **98 (ICA)** and **96 (LHA)** — see Live assignments and the ranking rationale. **97
  (WSA) and 99 (BVA) join 95 as reserve.**

**Sixth round: three MORE real findings — 97 and 99 were dispatched from reserve and both found
real bugs, and 92 (GLA, itself a backfill for 88) found real bugs too. The adversarial-audit
family is now 13 legs deep and remains extraordinarily productive.**

- **Leg 92 (GLA) found real silent-corruption bugs in `gclm.py`**: blow-up time returned up to
  1.5× too early from an absolute zero-tolerance bug, plus 3 more issues. Bench-repair in
  flight, checking whether `stage1_5_sweep.py`'s banked runs are affected (expected not to be —
  amplitudes are ~8 decades above the bug's onset — but being verified, not assumed).
  `solver/gclm.py` is off-limits until resolved. (Leg 88/GCA's own outcome was never
  individually reported — inferred landed since LEG-E moved on to 92, which has itself now
  landed too.)
- **Leg 99 (BVA) found a real 100%-relative-error case in `boussinesq_velocity.py`**:
  `u_x_at_origin` can silently return `-0.0` when a grid's `r_min` falls outside its fit window.
  Bench-repair in flight, specifically re-checking leg 73's own headline benchmark (same module)
  to confirm it's unaffected. `solver/boussinesq_velocity.py` is off-limits until resolved.
- **Leg 98 (ICA) found the same class of fabrication-acceptance gap in
  `interval_certificate.py`** that leg 79 found in its sibling `port_certification.py`.
  Bench-repair in flight, specifically re-checking leg 61's Kawahara known-answer gate (same
  pipeline) to confirm it's unaffected. `solver/interval_certificate.py` is off-limits until
  resolved.
- **Three slots open: LEG-E, LEG-I, LEG-J** (LEG-D still held for leg 76). **Six new candidates
  (100–105) are added below**, mixing three immediately-dispatchable adversarial/documentation
  legs with three pending post-repair regression closures (blocked until their respective
  repairs land, same discipline as legs 76 and 95). **100 (HNA) → LEG-E, 101 (OLA) → LEG-I, 102
  (JR2) → LEG-J.** **103 (GLB), 104 (BVB) and 105 (ICB) are the new reserve**, each explicitly
  not dispatchable until its corresponding repair (gclm.py, boussinesq_velocity.py,
  interval_certificate.py respectively) lands.

**Table drift caught by the coordinator, not this file: LEG-G and LEG-H were stale.** LEG-G
showed leg 97 (WSA) and LEG-H showed leg 80 (BHN) — both had actually landed clean (gate NO, no
bug found) a while back: 97 cleared `weight_search.py`, 80 cleared `bordered_hl.py`, both now
free again. Marked landed in their queue entries above. **96 (LHA), 100 (HNA), 101 (OLA) and 102
(JR2) — the previous batch — are confirmed dispatched into LEG-C/E/I/J as specified.** Reserve
(103–105) remains fully blocked; none of the three repairs (gclm.py, boussinesq_velocity.py,
interval_certificate.py) has reported back yet. **The adversarial-audit family stands at 15+
legs with roughly a 40% hit rate on real findings** — genuinely productive, not a fishing
exercise. **Four fresh candidates (106–109) are added below, all immediately dispatchable
(nothing pending), mixing two more adversarial audits with two documentation passes** per the
coordinator's suggestion. **106 (HPA) → LEG-G, 108 (IX2) → LEG-H.** 107 (FIA) and 109 (RCA) join
the still-blocked 103–105 as reserve.

---

**DM ruling 2026-08-06 — the user has answered open question #2; legality resolved; leg 125
(M2P) drafted and assigned.** The user's directive, verbatim: *"Leg 63, let's pursue this if it
might be beneficial towards our goal of solving Clay or towards our sub-goal of producing novel
beneficial output."*

**Legality ruling (the DM's call, in the same way leg 111's was): pursuing leg 63's candidate
does NOT require lifting stage V's ban. The ban stands, unmodified, and leg 125 is outside its
scope.** Reasoning, in full so it is auditable:

1. **What the ban's letter says.** The ban is "re-opening stage V **as posed**," and stage V as
   posed (plan of record, SEQUENCE) is: *"Viscous survival, IN FLOAT: does the certificate's
   margin survive dissipation as mu → criticality?"* — a **continuation** question about an
   already-certified profile's margin as a dissipation parameter floats. It was closed for
   **non-novelty**: arXiv:2410.05480 already verifies CGL branches in the dissipation
   parameter, in interval arithmetic, and leg 48 confirmed it by re-deriving their zeros,
   branch and fold.
2. **What leg 63's candidate asks.** Certify, from scratch, at **fixed** γ=2, a dissipative
   self-similar profile of gCLM whose blow-up Chen (arXiv:1908.09385) proved analytically.
   That is a stage-**M**-shaped question (certify WHAT?) with a new target — not a margin
   continuation, not in float, not derived from the a=0 CLM linearization, and no dissipation
   parameter is varied toward criticality. Nothing leg 125 computes is a quantity stage V
   computed.
3. **The ban's reason does not attach.** V was closed because its question was pre-empted.
   Leg 63's N3/N4 searches found the opposite here: **no computer-assisted certificate of any
   dissipative self-similar profile exists** in the searched literature. The preemption that
   closed V is precisely absent for this object.
4. **The lift condition confirms the scope reading.** "Re-posed for a FLUID transport model,
   which needs L1 first" is the condition for re-opening **V's own question** — margin survival
   requires a certified inviscid base profile to float, which is what L1 was for. Certifying a
   profile that is dissipative from the start has no inviscid base certificate to float, so the
   precondition is not merely unmet, it is structurally inapplicable. A lift condition for
   question Q does not fence off questions that are not Q.
5. **Precedent.** Leg 111 (WE) was ruled dispatchable on exactly this construal: bans bind by
   what a leg actually computes, not by topic adjacency ("not tuning s… not stage B, and not
   stage V"). Same rule here.
6. **The residual ambiguity is closed by the user anyway.** The prior DM's §2 cautiously read
   the ban broadly ("the obstruction is exactly stage V's ban") and parked three readings. Even
   under that broad reading, the user's directive is option (c): a narrow, single-candidate,
   conditional authorization. So under **either** reading, a scoped promotion leg on this one
   candidate is legal. What stays banned under either reading: re-running V's
   margin-survival-in-float question, and any *general* re-opening of "the dissipative
   direction" beyond this candidate. **Tripwire, binding on leg 125:** if its work drifts into
   floating a dissipation parameter against an existing certificate's margin, that IS stage V
   as posed — stop and escalate.

**The "another gCLM measurement leg" ban also does not bind**, on leg 63's own landed
construal: that ban is about running the model's blow-up dynamics (Stage 3.5's exhaustion).
Leg 125 runs **no gCLM time evolution** — it transcribes published constants, Newton-solves a
steady profile equation, and computes certificate constants; its JSON records
`no_dynamics_run: true`, same discipline as leg 63.

**Benefit test, under the user's stated condition (disjunctive).** Toward Clay: **no** — this
does not move L1→L4, and the odds stay ~0.05%; leg 125's prose must say so. Toward novel
beneficial output: **yes, and it is the strongest yes available** — the only screen-passing
candidate in 63+ legs, proved blow-up, and an empty CAP literature for dissipative self-similar
profiles, so even the *first measured Y_0* is a novel data point and a closed certificate would
be a genuinely novel positive result. The next step is cheap (full-text read + transcription +
first Y_0 measurement = one standard leg). The condition is met; leg 125 is drafted below and
assigned to **LEG-J** (the flex slot), jumping the 103/104 reserve promotion on the user's
directive — 103/104 remain next in line for whatever slot opens next. `NG` stays `NEXT`;
leg 125 claims no stage; entering the committed sequence remains escalation #1 and happens only
on leg 125's yes-branch, with the user.

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
| LEG-C | 96 | **LHA** — adversarial audit of line_hilbert.py's dense operator | no | standard | `leg/lha-v1` | Under adversarial near-degenerate grid spacing, does the dense operator / cached slope_matrix silently return a wrong result? |
| LEG-D | — | **OPEN, held for leg 76 (MI)** pending its verifier's confirmation of leg 70's finding | — | — | — | — |
| LEG-E | 100 | **HNA** — adversarial audit of holder_norms.py's norm/embedding-constant code | no | standard | `leg/hna-v1` | Under NaN-poisoned or degenerate weight-class inputs, does the norm computation silently return a wrong value? |
| LEG-F | 71 | **CAP** — capabilities.py self-audit | no | light | `leg/cap-v1` | Does every module row in capabilities.py have a test file that exists, is collected, and passes at HEAD? |
| LEG-G | 106 | **HPA** — adversarial audit of hilbert_pointwise.py's bound direction | no | standard | `leg/hpa-v1` | Under adversarial/degenerate inputs, can the pointwise \|H(h)\| bound be exceeded (fail to be a true bound)? |
| LEG-H | 108 | **IX2** — second freshness audit of writeup/INDEX.md (since leg 68's pass) | no | light | `leg/ix2-v1` | Does INDEX.md correctly reflect every leg landed since leg 68, including the "no figure by design" convention this cycle established? |
| LEG-I | 101 | **OLA** — adversarial audit of op_lower.py's lower-bound direction | no | standard | `leg/ola-v1` | Under adversarial/degenerate operator inputs, does op_lower.py ever return a bound that is not actually a lower bound? |
| LEG-J | 102 | **JR2** — second freshness audit of experiments/JOURNAL.md and journal/ (legs 73–99) | no | light | `leg/jr2-v1` | Does the journal narrative and per-leg journal/leg_N.md file exist for every leg landed since leg 72's original pass? |

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
nine plus the reserve (58, 62, 96, 71, 100, 106, 101, 108, 102, 103, 104, 105, 107, 109):
`spectral_certificate.py`(58), `certificate_shapes.py`+`literature_gates.py`(62),
none-owned/read-only(96 reads `line_hilbert.py`, edits nothing under a bug-found outcome),
`capabilities.py`(71, factual "test"-field only, pre-committed narrow), none-owned/read-only(100
reads `holder_norms.py`, edits nothing — robustness only, no bound-sharpening, precedent set by
leg 69), none-owned/read-only(106 reads `hilbert_pointwise.py`, edits nothing, same precedent),
none-owned/read-only(101 reads `op_lower.py`, edits nothing, same precedent), none(108, INDEX.md
freshness, no solver module), none(102, JOURNAL.md freshness, no solver module),
none-owned/read-only(103 reads `gclm.py`, edits nothing — NOT dispatchable until leg 92's repair
lands), none-owned/read-only(104 reads `boussinesq_velocity.py`, edits nothing — NOT
dispatchable until leg 99's repair lands), none-owned/read-only(105 reads
`interval_certificate.py`, edits nothing — NOT dispatchable until leg 98's repair lands),
none-owned/read-only(107 reads `first_integral.py`, edits nothing, same Route-D-robustness-only
precedent), none-owned/read-only(109 reads `reduced_certificate.py`, edits nothing, same
precedent). Fourteen distinct — **no collision.** `target_selection.py`(63) stays off the live
list (parked). `weight_search.py`(97) and `bordered_hl.py`(80) are **cleared and free again**
(both landed clean) — neither is claimed by 106-109, so no re-verification of that freedom was
required here. **Currently off-limits, repairs in flight:** `solver/gclm.py`(92),
`solver/boussinesq_velocity.py`(99), `solver/interval_certificate.py`(98),
`solver/boussinesq.py`(89, plus its banked-result audit), `solver/gclm_rescaled.py`(85) — none
of the reserve touches any of these for editing; 103/104/105 read them for spec purposes only
and are explicitly blocked from dispatch. `solver/interval.py`, `solver/spectral_utils.py`,
`solver/port_certification.py` and `solver/target_norm.py` remain fully repaired and unclaimed.
LEG-D stays empty pending leg 76, whose territory (`PHASE2_P2_NOTES.md`,
`TECHNICAL_P2_ROUTEI_V1.md`) no live or reserve leg touches. `writeup/data` JSON files are
likewise distinct names (`p2_route_ng_v1_nogo.json`(58), `p2_route_cp_v1_cadiot.json`(62),
`p2_route_lha_v1_adversarial.json`(96), `p2_route_cap_v1_audit.json`(71),
`p2_route_hna_v1_adversarial.json`(100), `p2_route_hpa_v1_adversarial.json`(106),
`p2_route_ola_v1_adversarial.json`(101), none(108, docs-only), none(102, docs-only),
`p2_route_glb_v1_postrepair.json`(103), `p2_route_bvb_v1_postrepair.json`(104),
`p2_route_icb_v1_postrepair.json`(105), `p2_route_fia_v1_adversarial.json`(107),
`p2_route_rca_v1_adversarial.json`(109)) — **no collision.**

**DM refresh 2026-08-06 — this block supersedes the table and paragraphs above it as the
single authoritative account of live assignments.** Landed and cleared this cycle: 89 (BOA),
92 (GLA), 99 (BVA), 83 (MFG), 106 (HPA, gate NO — hilbert_pointwise robust). Re-dispatched
fresh after their uncommitted attempts were lost: **58** (NG, critical path, LEG-A,
`leg/ng-v1`) and **62** (CP, LEG-B, `leg/cp-v1`) — their entries, gates, and territories are
unchanged from this file. Running as bench-repairs outside the leg queue: the
test_fractional_boussinesq.py G6 / test_profile_newton.py red-test investigation, and
repairs tracking legs 100 (holder_norms.py), 101 (op_lower.py), 107 (first_integral.py) —
their modules are off-limits to every leg below. Parked escalations, untouchable by any leg:
leg 63/M2 (`leg/m2-v1`) and leg 60/PQ (`leg/pq-v1`). The seven open exploration slots are
filled from the new 110-series queue below:

| Slot | Leg | Route | Critical path? | Difficulty | Branch | Gate (short form) |
|---|---|---|---|---|---|---|
| LEG-A | 58 | **NG** — the no-go as a theorem | **YES** (stage `NG`) | heavy | `leg/ng-v1` | Proof for a class of `A` strictly larger than block-diagonal? |
| LEG-B | 62 | **CP** — Cadiot pre-emption, full text | no | standard | `leg/cp-v1` | Does Cadiot 2505.03091 cover the off-diagonal / non-decaying-tail case? |
| LEG-C | 110 | **L1R** — L1 death-certificate reproduction audit | no (audits the chain's dead link) | light | `leg/l1r-v1` | Do both L1 death certificates (legs 54, 56) reproduce exactly from their own banked data? |
| LEG-D | 111 | **WE** — third-realization scoping: weighted-energy coercivity on a=0 CLM | no (could re-price the dead link) | heavy | `leg/we-v1` | Does any named weight give a grid-stable positive coercivity gap? |
| LEG-E | 112 | **AS2** — verify §24's two load-bearing readings of arXiv:2603.25104 from the full PDF | no | light | `leg/as2-v1` | Does the full text confirm the a-sign and the fixed-point identity? |
| LEG-F | 113 | **MS** — lesson 87's multiplier/shift prediction vs the certified-blow-up literature | no | light | `leg/ms-v1` | Does any certified INVISCID self-similar blow-up use a diagonal-tail framework? |
| LEG-G | 114 | **CNA** — adversarial audit of collocation_newton.py | no | standard | `leg/cna-v1` | Can the Newton solve be fooled into reporting convergence on a poisoned/degenerate case? |
| LEG-H | 116 | **NKA** — adversarial fabrication-rejection audit of nk_bounds.py | no | standard | `leg/nka-v1` | Does a planted wrong point ever survive inside a reported certified ball? |
| LEG-I | 120 | **SUA** — adversarial audit of spectral_utils.py (shared core) | no | standard | `leg/sua-v1` | Does the shared spectral core silently return wrong values on degenerate input? |
| LEG-J | — | reserve/flex — first promotion: 103 (GLB) and 104 (BVB), now dispatchable (92's and 99's repairs landed); then 115, 123, 117-124 in queue order | — | — | — | — |

**Territory-overlap check (explicit, as required).** Solver modules touched by the assigned
set (58, 62, 110, 111, 112, 113, 114, 116, 120) plus the running repairs (100, 101, 107) and
reserve 109: `spectral_certificate.py`(58); `certificate_shapes.py`+`literature_gates.py`(62);
none(110 — reads banked `writeup/data` JSONs only, no solver module);
`energy_coercivity.py`(111, NEW file, exists nowhere else, capabilities.py grepped first per
the standing ban); none(112, literature — explicitly does NOT edit `literature_gates.py`,
which 62 owns; banks its ledger in its own JSON); none(113, literature — same guard, no
`literature_gates.py` edits); `collocation_newton.py`(114, read-only, robustness precedent of
legs 69/100/101); `nk_bounds.py`(116, read-only, fabrication-rejection precedent of legs
79/98); `spectral_utils.py`(120, read-only, shared-core precedent of leg 69);
`holder_norms.py`(100, repair in flight), `op_lower.py`(101, repair in flight),
`first_integral.py`(107, repair in flight); `reduced_certificate.py`(109, reserved).
`fractional_boussinesq.py` and `profile_newton.py` are off-limits to all of the above (red-test
investigation in flight). All distinct — **no collision.** `writeup/data` JSON ownership:
`p2_route_ng_v1_nogo.json`(58), `p2_route_cp_v1_cadiot.json`(62),
`p2_route_l1r_v1_repro.json`(110 — additionally reads, never writes,
`leg_54_verify_headline.json`, `p2_route_l1_v1_interval.json`, `p2_route_l1_v2_spectral.json`
and the leg-56 collocation record located via PHASE2_P2_NOTES.md; no other live leg touches
those), `p2_route_we_v1_coercivity.json`(111), `p2_route_as2_v1_lit.json`(112),
`p2_route_ms_v1_lit.json`(113), `p2_route_cna_v1_adversarial.json`(114),
`p2_route_nka_v1_adversarial.json`(116), `p2_route_sua_v1_adversarial.json`(120) — all
distinct names, none pre-existing — **no collision.**

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
### 80 — ROUTE-BHN: ADVERSARIAL AUDIT OF THE BORDERED HL NEWTON SOLVE (LANDED: gate NO — robust,
no bug found; `bordered_hl.py` cleared and free again)
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
### 84 — ROUTE-TNA: DOES target_norm.py SILENTLY EXTRAPOLATE BEYOND ITS VALIDATED DOMAIN? (LANDED:
gate YES — silent gap found, bench-repair bundled)
**Landed finding.** Confirmed silent: a real gap, since fixed by a bundled bench-repair that
added a domain guard to `target_norm.py`. The repair also independently re-checked leg 55
(NB)'s banked margins against the new guard and confirmed them **not contaminated** (0.0 diff)
— good news beyond the leg's own scope.
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
### 85 — ROUTE-GRA: ADVERSARIAL AUDIT OF gclm_rescaled.py's FIXED-POINT REPORTING (LANDED: gate
YES — real false-convergence bug found, bench-repair dispatched)
**Landed finding.** A real false-convergence bug: the relaxation loop reports having reached
the fixed point after 1 step on certain gauge-scale trajectories. Leg 85 supplied its own
suggested one-line fix; a bench-repair is applying it. `solver/gclm_rescaled.py` is off-limits
for editing by any new candidate until that repair lands.
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
### 86 — ROUTE-PCB: POST-REPAIR REGRESSION CHECK, port_certification.py (LANDED: gate YES —
repair confirmed solid, zero regression)
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
### 87 — ROUTE-IVB: POST-REPAIR REGRESSION CHECK, interval.py (LANDED: gate YES — repair
confirmed solid, zero regression)
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
### 88 — ROUTE-GCA: ADVERSARIAL AUDIT OF gclm_family.py's RESIDUAL COMPUTATION (LANDED — outcome
not individually reported to the DM; inferred landed because LEG-E moved on to leg 92, which has
itself since landed too)
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
### 89 — ROUTE-BOA: ADVERSARIAL AUDIT OF boussinesq.py (PHYSICAL-SPACE 2D BOUSSINESQ) (LANDED:
gate YES — the most serious finding of the whole adversarial-audit run)
**Landed finding.** A false `blowup_candidate` flag triggered by ordinary floating-point
dealiasing noise, amplified **5.6e13×**; plus a silently-dropped `kappa` parameter and a
NaN-masking bug. Bench-repair in flight, specifically investigating whether any banked Phase-1
result was affected. `solver/boussinesq.py` is off-limits for any new candidate until the
repair and its banked-result audit both resolve.
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
### 90 — ROUTE-EXT4: HAS THE RANK-4 TARGET OBJECT'S CONJECTURE BEEN RESOLVED SINCE? (LANDED:
gate NO — still open)
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

```
### 92 — ROUTE-GLA: ADVERSARIAL AUDIT OF gclm.py (PHYSICAL-SPACE gCLM) (LANDED: gate YES — real
silent-corruption bugs found)
**Landed finding.** Blow-up time returned up to 1.5× too early from an absolute zero-tolerance
bug, plus 3 more issues. Bench-repair in flight, checking whether `stage1_5_sweep.py`'s banked
runs are affected — expected not to be (amplitudes are ~8 decades above the bug's onset) but
being verified rather than assumed. `solver/gclm.py` is off-limits for any new candidate until
the repair and its banked-result check both resolve.
**Thesis.** solver/gclm.py got dedicated test coverage from leg 66 (QF) -- a correctness check
on well-behaved inputs, which found no discrepancy. That is the same relationship leg 89 (BOA)
has to leg 66's boussinesq.py finding: a correctness check is not a robustness check. Nobody has
checked whether solver/gclm.py silently produces a wrong-but-plausible result under adversarial
physical-space inputs (NaN-seeded initial vorticity, a degenerate Hilbert-transform input,
extreme parameter values for `a`) rather than flagging them. The last physical-space module in
this family without a dedicated adversarial pass.
**Gate.** Under an adversarial battery of malformed physical-space inputs (NaN-seeded vorticity,
degenerate transform input, extreme `a`), does solver/gclm.py ever silently return a finite,
plausible-looking result instead of propagating or flagging the invalid input?
  yes -> A silent-corruption gap. Report the exact failing case precisely; escalate, do not
         patch under this leg's own authority.
  no  -> Confirmed robust. Bank the battery as a permanent regression test.
**Territory.** test_gclm_adversarial.py, experiments/p2_route_gla_v1_adversarial.py,
               writeup/data/p2_route_gla_v1_adversarial.json,
               writeup/novelty/leg_92.md, experiments/journal/leg_92.md
**Difficulty.** standard
**Independence.** Reads solver/gclm.py; edits nothing under any outcome. New test file claimed
by nobody else. Distinct question from leg 66 (QF, landed) -- robustness, not correctness on
well-behaved input, the same distinction leg 89 established for boussinesq.py.
```

```
### 93 — ROUTE-EXT5: HAS arXiv:2604.09949's 3D NS SELF-SIMILAR SINGULARITY CLAIM BEEN
CONFIRMED, REFUTED, OR RETRACTED SINCE? (LANDED: gate NO — but surfaced useful context, see
Status)
**Landed finding.** No formal confirmation/refutation/retraction found — but the author has
since posted 6 papers claiming the OPPOSITE result with the same 5D-lifted machinery and zero
cross-citation, a de facto self-refutation. M-5's own arithmetic audit stands unaffected (it
checked the computation, not the conclusion). Filed as context for any future leg touching this
corpus.
**Thesis.** PHASE2_P2_NOTES's M-5 audited arXiv:2604.09949's computer-assisted claim of a
finite-time singularity for 3D Navier-Stokes on T^3 rather than assuming it -- the arithmetic
checked out (`2*delta*M*K` and Kantorovich's hypothesis both close, with margin). That audit is
the most consequential external claim this repository has ever independently checked -- rank-6
on the target ledger, "claimed by arXiv:2604.09949." Nobody has since watched whether the
broader community has weighed in: an independent confirmation, a refutation, a retraction, or a
published correction, any of which would be major news for how this repository frames its own
finding. Distinct in KIND from legs 74/77/82/90 (which ask "does a certificate exist"), this
leg asks "has the community's verdict on an EXISTING claim moved."
**Gate.** Since arXiv:2604.09949 was posted, has any independent group published a confirmation,
refutation, retraction, or correction of its 3D NS self-similar singularity claim?
  yes -> Materially changes M-5's standing audit. Report the citation and its direction
         precisely; this bears directly on how `NG` and any future write-up should characterize
         the state of the field, so flag it prominently rather than filing it quietly.
  no  -> Confirmed no community verdict has appeared since. Bank the dated literature-watch
         entry; M-5's own arithmetic audit remains the best available check.
**Territory.** experiments/p2_route_ext5_v1_target_watch5.py,
               writeup/data/p2_route_ext5_v1_target_watch5.json,
               writeup/novelty/leg_93.md, experiments/journal/leg_93.md
**Difficulty.** light
**Independence.** Does not touch solver/target_selection.py. Distinct question (community
verdict, not certificate existence) from legs 74, 77, 82, 90.
```

```
### 94 — ROUTE-TNB: POST-REPAIR REGRESSION CHECK, target_norm.py's NEW DOMAIN GUARD
**Thesis.** Leg 84's bench-repair added a domain guard to target_norm.py and confirmed leg 55's
banked margins survive it uncontaminated -- that closed the FALSE-NEGATIVE direction (silently
accepting out-of-window input). It did not dedicate a check to the opposite failure mode: a
guard that is too aggressive and flags legitimate IN-WINDOW input (well inside X_max=745) as a
violation, which would be a new, self-inflicted correctness bug on top of the fix. Same
"close the loop" pattern as legs 86 (PCB) and 87 (IVB), applied to the newest repair.
**Gate.** Across a battery of legitimate in-window inputs spanning the validated range up to
X_max=745, does target_norm.py's new domain guard ever incorrectly flag a valid input as a
violation (a false positive)?
  yes -> The repair over-corrected. Report the exact false-positive case precisely; escalate,
         do not patch under this leg's own authority.
  no  -> Confirmed the guard is precise -- catches violations without rejecting valid input.
         Bank as a permanent regression test alongside leg 84's own battery.
**Territory.** test_target_norm_postrepair.py, experiments/p2_route_tnb_v1_postrepair.py,
               writeup/data/p2_route_tnb_v1_postrepair.json,
               writeup/novelty/leg_94.md, experiments/journal/leg_94.md
**Difficulty.** light
**Independence.** Reads solver/target_norm.py, now repaired; edits nothing. Distinct failure
direction from leg 84 (false positive vs. false negative). New test file claimed by nobody else.
```

```
### 95 — ROUTE-GRB: POST-REPAIR REGRESSION CHECK, gclm_rescaled.py (PENDING leg 85's repair)
**Thesis.** Leg 85 found a real false-convergence bug in gclm_rescaled.py's relaxation loop
(reports reaching the fixed point after 1 step on certain gauge-scale trajectories) and supplied
a suggested one-line fix; a bench-repair is applying it now. Once it lands, the same "close the
loop" pattern that legs 86, 87 and 94 apply to their repairs should apply here too: confirm the
fix actually closes leg 85's failing trajectories AND does not regress the module's
already-validated behavior (the exact a=0 CLM fixed-point relaxation, previously confirmed).
**Gate.** Post-repair, does solver/gclm_rescaled.py (a) no longer false-converge on leg 85's
original failing gauge-scale trajectories, and (b) still relax correctly to the exact a=0 CLM
fixed point with no regression?
  yes -> Confirmed the repair is solid and non-regressive. Bank leg 85's battery plus this leg's
         fixed-point regression check as a permanent suite.
  no  -> An incomplete fix or a repair regression. Report the exact case precisely; escalate as a
         priority finding, do not patch under this leg's own authority.
**Territory.** test_gclm_rescaled_postrepair.py, experiments/p2_route_grb_v1_postrepair.py,
               writeup/data/p2_route_grb_v1_postrepair.json,
               writeup/novelty/leg_95.md, experiments/journal/leg_95.md
**Difficulty.** standard
**Independence.** Reads solver/gclm_rescaled.py; edits nothing under any outcome.
**NOT dispatchable until leg 85's bench-repair lands** -- drafted now so it is ready immediately
after, the same discipline used for leg 76's pending dependency.
```

```
### 96 — ROUTE-LHA: ADVERSARIAL AUDIT OF line_hilbert.py's DENSE OPERATOR
**Thesis.** solver/line_hilbert.py's validated line covers a known-answer pair (rel 1.6e-4) and
the cached slope operator matching the Thomas sweeps (2.7e-13) -- both on well-behaved,
presumably-uniform-ish grid data (the module explicitly supports NON-uniform grids per its
`holds` field, which makes this gap sharper: a spline-analytic Hilbert transform on a
non-uniform grid has real degenerate cases -- near-duplicate points, extreme local stretching --
that have never been adversarially tested). Same pattern as legs 69/79/80/83/85/88/89/91/92,
applied to the module leg 75 (LM) only benchmarked for SPEED, never for robustness.
**Gate.** Under an adversarial battery of near-degenerate non-uniform grids (near-duplicate
points, extreme local stretching ratios), does solver/line_hilbert.py's dense operator or its
cached `slope_matrix` ever silently return a finite, plausible-looking wrong result instead of
propagating or flagging the ill-conditioning?
  yes -> A silent-corruption gap. Report the exact failing case precisely; escalate, do not
         patch under this leg's own authority.
  no  -> Confirmed robust. Bank the battery as a permanent regression test.
**Territory.** test_line_hilbert_adversarial.py, experiments/p2_route_lha_v1_adversarial.py,
               writeup/data/p2_route_lha_v1_adversarial.json,
               writeup/novelty/leg_96.md, experiments/journal/leg_96.md
**Difficulty.** standard
**Independence.** Reads solver/line_hilbert.py; edits nothing under any outcome. New test file
claimed by nobody else. Distinct from leg 75 (LM, speed benchmark) -- robustness, not
performance.
```

```
### 97 — ROUTE-WSA: ADVERSARIAL AUDIT OF weight_search.py's FitnessEngine (LANDED: gate NO —
robust, no bug found; `weight_search.py` cleared and free again)
**Thesis.** solver/weight_search.py's FitnessEngine batches the weight fitness computation with
"the Jacobian inverted once" -- a numerical shortcut validated on well-posed problems (the
closed-form CLM profile, gauge-invariance to 4.4e-16). A single inverted Jacobian reused across
a batch is exactly the kind of optimization that can silently produce a wrong-but-plausible
fitness value if any member of the batch pushes the shared Jacobian toward near-singularity --
nobody has checked this. Same adversarial pattern as the rest of this family, applied to the
one search/optimization-adjacent module in the certificate stack that has never been stress-
tested this way. Does not reopen or contest stage B's own FAIL 4/6 gate verdict (frozen, still
banned pending its own lift condition) -- this leg audits code robustness, not the fitness's
scientific viability.
**Gate.** Under an adversarial battery (a batch member driving the shared Jacobian toward
near-singularity, NaN-poisoned weight parameters), does FitnessEngine ever silently return a
finite, plausible-looking fitness value instead of propagating or flagging the ill-conditioning?
  yes -> A silent-corruption gap. Report the exact failing case precisely; escalate, do not
         patch under this leg's own authority.
  no  -> Confirmed robust. Bank the battery as a permanent regression test.
**Territory.** test_weight_search_adversarial.py, experiments/p2_route_wsa_v1_adversarial.py,
               writeup/data/p2_route_wsa_v1_adversarial.json,
               writeup/novelty/leg_97.md, experiments/journal/leg_97.md
**Difficulty.** standard
**Independence.** Reads solver/weight_search.py; edits nothing under any outcome. Does not touch
or contest leg 59 (WV)'s frozen gate verdict -- robustness only, no re-scoring.
```

```
### 98 — ROUTE-ICA: ADVERSARIAL FABRICATION-REJECTION AUDIT OF interval_certificate.py (LANDED:
gate YES — the same class of gap leg 79 found in its sibling)
**Landed finding.** `interval_certificate.py`'s verdict function has the same class of
fabrication-acceptance gap leg 79 found in `port_certification.py`. Bench-repair in flight,
specifically re-checking leg 61's Kawahara known-answer gate (same pipeline) to confirm it's
unaffected. `solver/interval_certificate.py` is off-limits for any new candidate until the
repair and its re-check both resolve.
**Thesis.** Leg 61 (KA) validated interval_certificate.py against a published known-answer
(CLN's Kawahara radius) -- correctness on a well-formed problem. Leg 79 (PC) found that
port_certification.py's sibling status function did NO domain validation and accepted fabricated
Y_0/Z_1 11/25 times; leg 69 (IA) found real soundness gaps in the interval PRIMITIVE underneath
BOTH certificate pipelines. Nobody has run the leg-79-style fabrication-rejection battery against
THIS pipeline's own verdict function, `radii_verdict` / `interval_constants` -- does it correctly
reject poisoned or hypothesis-violating interval enclosures (negative widths, NaN endpoints,
enclosures that don't actually contain their claimed center), or can it be fooled the way
port_certification.py's function was.
**Gate.** Under an adversarial battery of poisoned interval enclosures (negative widths, NaN
endpoints, non-containing enclosures) fed to `interval_constants` / `radii_verdict`, does the
pipeline ever incorrectly report a closing/valid certificate?
  yes -> A fabrication-rejection gap in the L1-step-one certificate pipeline, the same shape as
         leg 79's finding in the sibling pipeline. Report the exact failing case precisely;
         escalate, do not patch under this leg's own authority.
  no  -> Confirmed robust. Bank the battery as a permanent regression test, complementary to
         leg 61's known-answer correctness gate.
**Territory.** test_interval_certificate_adversarial.py,
               experiments/p2_route_ica_v1_adversarial.py,
               writeup/data/p2_route_ica_v1_adversarial.json,
               writeup/novelty/leg_98.md, experiments/journal/leg_98.md
**Difficulty.** standard
**Independence.** Reads solver/interval_certificate.py; edits nothing under any outcome. Distinct
question from leg 61 (known-answer correctness, not fabrication-rejection) -- the exact
relationship leg 79 has to leg 61's sibling pipeline.
```

```
### 99 — ROUTE-BVA: ADVERSARIAL AUDIT OF boussinesq_velocity.py's DEGENERATE-GRID HANDLING
(LANDED: gate YES — a real 100% relative-error case)
**Landed finding.** `u_x_at_origin` can silently return `-0.0` instead of the true value when a
grid's `r_min` falls outside its fit window — 100% relative error in the worst case.
Bench-repair in flight, specifically re-checking leg 73's own headline benchmark (same module)
to confirm it's unaffected. `solver/boussinesq_velocity.py` is off-limits for any new candidate
until the repair and its re-check both resolve.
**Thesis.** Leg 73 (BV) gave solver/boussinesq_velocity.py its first external known-answer gate
(the Lamb corner-image closed form, 1.76e-4 relative) -- correctness on a well-posed polar-grid
problem. Nobody has checked robustness: does the Biot-Savart / stream-function solve silently
return a plausible-looking wrong result under degenerate polar-grid inputs (r=0 at the origin
singularity, a malformed or self-intersecting boundary) rather than flagging them. Same
relationship to leg 73 that leg 89 (BOA) has to leg 66 (QF) -- a correctness check on
well-behaved input is not a robustness check.
**Gate.** Under an adversarial battery of degenerate polar-grid inputs (r=0 singularity,
malformed/self-intersecting boundary), does solver/boussinesq_velocity.py ever silently return a
finite, plausible-looking result instead of propagating or flagging the degeneracy?
  yes -> A silent-corruption gap. Report the exact failing case precisely; escalate, do not
         patch under this leg's own authority.
  no  -> Confirmed robust. Bank the battery as a permanent regression test alongside leg 73's
         known-answer gate.
**Territory.** test_boussinesq_velocity_adversarial.py,
               experiments/p2_route_bva_v1_adversarial.py,
               writeup/data/p2_route_bva_v1_adversarial.json,
               writeup/novelty/leg_99.md, experiments/journal/leg_99.md
**Difficulty.** standard
**Independence.** Reads solver/boussinesq_velocity.py; edits nothing under any outcome. Distinct
question from leg 73 (BV, external correctness) -- robustness only.
```

```
### 100 — ROUTE-HNA: ADVERSARIAL AUDIT OF holder_norms.py's NORM / EMBEDDING-CONSTANT CODE
**Thesis.** solver/holder_norms.py's own validated line covers "norm axioms and the embedding
constants" -- on well-formed inputs. The weighted-l1 no-go leg 65 (L1G) confirmed is genuinely
unpublished lives in this module's territory conceptually, but B is dead on all three DOF and
this leg does NOT reopen Route-D bound-sharpening or build any new machinery -- it is a pure
robustness stress test of EXISTING norm/embedding-constant code, the exact precedent leg 69 (IA)
set for solver/interval.py despite that module also underlying the (dead) Route-D programme:
"does not sharpen a bound, pure stress test of infrastructure." Does the code silently return a
wrong norm or embedding constant under NaN-poisoned or degenerate weight-class inputs, rather
than flagging them.
**Gate.** Under an adversarial battery (NaN/Inf-poisoned weight-class parameters, degenerate
grading exponents), does solver/holder_norms.py's norm or embedding-constant computation ever
silently return a finite, plausible-looking wrong value instead of propagating or flagging the
invalid input?
  yes -> A silent-corruption gap. Report the exact failing case precisely; escalate, do not
         patch under this leg's own authority.
  no  -> Confirmed robust. Bank the battery as a permanent regression test.
**Territory.** test_holder_norms_adversarial.py, experiments/p2_route_hna_v1_adversarial.py,
               writeup/data/p2_route_hna_v1_adversarial.json,
               writeup/novelty/leg_100.md, experiments/journal/leg_100.md
**Difficulty.** standard
**Independence.** Reads solver/holder_norms.py; edits nothing under any outcome. Does not
sharpen any Route-D bound and builds no new machinery -- robustness audit only, the same
precedent that cleared leg 69 against the same category of concern.
```

```
### 101 — ROUTE-OLA: ADVERSARIAL AUDIT OF op_lower.py's LOWER-BOUND DIRECTION
**Thesis.** solver/op_lower.py computes "a LOWER bound on ||A||" and is validated to "bracket
the dense operator norm from below wherever both are computable" -- on well-formed operators.
The one property that MUST hold for a lower bound to be meaningful is that it never reports a
value ABOVE the true norm -- if it can be fooled into doing so under adversarial or degenerate
operator inputs (near-singular blocks, NaN-poisoned entries), the bound is worse than useless,
it is actively misleading. Same robustness-only precedent as leg 100 and leg 69 -- no bound-
sharpening, no new machinery, a soundness stress test of existing code.
**Gate.** Under an adversarial battery of degenerate or NaN-poisoned operator inputs, does
solver/op_lower.py ever return a value that is NOT a true lower bound on the dense operator norm
(i.e. exceeds the true norm on a case where both are computable)?
  yes -> A soundness violation in a bound whose entire purpose is to be a safe lower bound.
         Report the exact failing case precisely; escalate, do not patch under this leg's own
         authority.
  no  -> Confirmed sound under the battery. Bank it as a permanent regression test.
**Territory.** test_op_lower_adversarial.py, experiments/p2_route_ola_v1_adversarial.py,
               writeup/data/p2_route_ola_v1_adversarial.json,
               writeup/novelty/leg_101.md, experiments/journal/leg_101.md
**Difficulty.** standard
**Independence.** Reads solver/op_lower.py; edits nothing under any outcome. Robustness/
soundness audit only, not a bound-sharpening or machinery-building leg.
```

```
### 102 — ROUTE-JR2: SECOND FRESHNESS AUDIT OF experiments/JOURNAL.md (LEGS 73–99)
**Thesis.** Leg 72 (JR) closed the journal-freshness gap as of "Legs 54-57" plus whatever had
landed by leg 72's own dispatch. Since then, roughly 30 legs (73 through 99, plus their
bench-repairs) have landed, several with serious findings (leg 89's 5.6e13x amplification, leg
92's up-to-1.5x early blow-up time, leg 98's and leg 99's fabrication/silent-corruption gaps).
Given the volume, the journal is very likely stale again -- the exact failure mode leg 72 fixed
once already. Same audit, new window.
**Gate.** Does experiments/JOURNAL.md's narrative and experiments/journal/'s per-leg file exist
for every leg that has landed (gate answered) since leg 72's own pass?
  yes -> Confirmed current; report and close as a clean audit, no edits needed.
  no  -> Append terse, pointer-only narrative entries (mirroring leg 72's own style -- one line
         per leg, sourced from each leg's PR body / journal/leg_N.md, never re-deriving a
         number), and separately list which journal/leg_N.md files are missing as a report item,
         without creating them on that leg's behalf.
**Territory.** experiments/JOURNAL.md (append-only edit), writeup/novelty/leg_102.md,
               experiments/journal/leg_102.md
**Difficulty.** light
**Independence.** Touches one file outside any other leg's territory, plus its own report files.
Reads, never edits, individual experiments/journal/leg_N.md files. Same pattern as leg 72,
different time window.
```

```
### 103 — ROUTE-GLB: POST-REPAIR REGRESSION CHECK, gclm.py (PENDING leg 92's repair)
**Thesis.** Leg 92 found real silent-corruption bugs in gclm.py (blow-up time up to 1.5x too
early from an absolute zero-tolerance bug, plus 3 more). The bench-repair fixing them is also
checking whether stage1_5_sweep.py's banked runs are affected, but that in-flight check is
scoped to the ALREADY-BANKED runs, not a fresh adversarial battery against the repaired code.
Once the repair lands, the same "close the loop" pattern as legs 86/87/94 should apply: confirm
the fix actually closes leg 92's original failing cases AND does not regress the module's
already-validated well-behaved-input correctness.
**Gate.** Post-repair, does solver/gclm.py (a) no longer exhibit the early-blow-up-time bug or
the other 3 issues leg 92 found, and (b) show zero regression on its previously-validated
well-behaved test cases?
  yes -> Confirmed the repair is solid and non-regressive. Bank leg 92's battery as a permanent
         regression suite.
  no  -> An incomplete fix or a repair regression. Report the exact case precisely; escalate as a
         priority finding, do not patch under this leg's own authority.
**Territory.** test_gclm_postrepair.py, experiments/p2_route_glb_v1_postrepair.py,
               writeup/data/p2_route_glb_v1_postrepair.json,
               writeup/novelty/leg_103.md, experiments/journal/leg_103.md
**Difficulty.** standard
**Independence.** Reads solver/gclm.py; edits nothing under any outcome.
**NOT dispatchable until leg 92's bench-repair lands** -- drafted now so it is ready
immediately after, the same discipline used for legs 76 and 95.
```

```
### 104 — ROUTE-BVB: POST-REPAIR REGRESSION CHECK, boussinesq_velocity.py (PENDING leg 99's
repair)
**Thesis.** Leg 99 found `u_x_at_origin` can silently return `-0.0` (100% relative error) when a
grid's `r_min` falls outside its fit window. The bench-repair is specifically re-checking leg
73's own headline benchmark, but that is ONE benchmark, not leg 99's full adversarial battery of
degenerate grids. Once the repair lands, close the loop across the whole battery, not just the
single case the repair itself re-checks.
**Gate.** Post-repair, does solver/boussinesq_velocity.py (a) no longer return `-0.0` on any of
leg 99's original failing degenerate-grid cases, and (b) still reproduce leg 73's Lamb
corner-image benchmark with zero regression?
  yes -> Confirmed the repair is solid and non-regressive across the full battery. Bank it as a
         permanent regression suite alongside legs 73 and 99.
  no  -> An incomplete fix or a repair regression. Report the exact case precisely; escalate as a
         priority finding, do not patch under this leg's own authority.
**Territory.** test_boussinesq_velocity_postrepair.py,
               experiments/p2_route_bvb_v1_postrepair.py,
               writeup/data/p2_route_bvb_v1_postrepair.json,
               writeup/novelty/leg_104.md, experiments/journal/leg_104.md
**Difficulty.** standard
**Independence.** Reads solver/boussinesq_velocity.py; edits nothing under any outcome.
**NOT dispatchable until leg 99's bench-repair lands.**
```

```
### 105 — ROUTE-ICB: POST-REPAIR REGRESSION CHECK, interval_certificate.py (PENDING leg 98's
repair)
**Thesis.** Leg 98 found the same class of fabrication-acceptance gap in interval_certificate.py
that leg 79 found in port_certification.py. The bench-repair is specifically re-checking leg
61's Kawahara known-answer gate, but that is ONE correctness check, not leg 98's full
fabrication-rejection battery. Once the repair lands, close the loop across the whole battery,
mirroring exactly what leg 86 did for leg 79's sibling repair.
**Gate.** Post-repair, does solver/interval_certificate.py (a) correctly reject every case in
leg 98's original fabrication battery, and (b) still reproduce leg 61's Kawahara known-answer
gate with zero regression?
  yes -> Confirmed the repair is solid and non-regressive. Bank it as a permanent regression
         suite alongside legs 61 and 98.
  no  -> An incomplete fix or a repair regression. Report the exact case precisely; escalate as a
         priority finding, do not patch under this leg's own authority.
**Territory.** test_interval_certificate_postrepair.py,
               experiments/p2_route_icb_v1_postrepair.py,
               writeup/data/p2_route_icb_v1_postrepair.json,
               writeup/novelty/leg_105.md, experiments/journal/leg_105.md
**Difficulty.** standard
**Independence.** Reads solver/interval_certificate.py; edits nothing under any outcome.
**NOT dispatchable until leg 98's bench-repair lands** -- mirrors leg 86's relationship to leg
79 exactly, one pipeline behind.
```

```
### 106 — ROUTE-HPA: ADVERSARIAL AUDIT OF hilbert_pointwise.py's BOUND DIRECTION
**Thesis.** solver/hilbert_pointwise.py holds "the sharper pointwise bound and the payer rule it
exposes," validated only as "no known-answer gate; sampled" -- on well-formed inputs. The one
property that must hold for a pointwise bound to be safe to use downstream is that it is never
EXCEEDED by the true |H(h)| value. Same soundness-direction check as leg 101 (OLA) applied to a
different bound in the same certificate-adjacent family -- a pure robustness/soundness audit, no
bound-sharpening, no new machinery, the precedent legs 69/100/101 already established for
touching Route-D-adjacent code safely.
**Gate.** Under an adversarial battery of degenerate or NaN-poisoned inputs, does
solver/hilbert_pointwise.py's bound ever fail to dominate the true |H(h)| value on a case where
both are computable?
  yes -> A soundness violation in a bound whose entire purpose is to be safe to use downstream.
         Report the exact failing case precisely; escalate, do not patch under this leg's own
         authority.
  no  -> Confirmed sound under the battery. Bank it as a permanent regression test.
**Territory.** test_hilbert_pointwise_adversarial.py,
               experiments/p2_route_hpa_v1_adversarial.py,
               writeup/data/p2_route_hpa_v1_adversarial.json,
               writeup/novelty/leg_106.md, experiments/journal/leg_106.md
**Difficulty.** standard
**Independence.** Reads solver/hilbert_pointwise.py; edits nothing under any outcome.
Robustness/soundness audit only, not bound-sharpening or machinery-building.
```

```
### 107 — ROUTE-FIA: ADVERSARIAL AUDIT OF first_integral.py
**Thesis.** solver/first_integral.py holds "the profile on its own support," validated against
the closed form nulling the ODE residual -- on well-formed parameters. Nobody has checked
whether it silently returns a wrong profile value under adversarial or degenerate inputs: near
the turning point (where the module's sibling, turning_point.py, documents "what actually makes
the inverse diverge"), or NaN-poisoned profile parameters. Same robustness-only precedent as
legs 100/101/106.
**Gate.** Under an adversarial battery (inputs near the documented turning point, NaN-poisoned
profile parameters), does solver/first_integral.py ever silently return a finite,
plausible-looking wrong profile value instead of propagating or flagging the ill-conditioning?
  yes -> A silent-corruption gap. Report the exact failing case precisely; escalate, do not
         patch under this leg's own authority.
  no  -> Confirmed robust. Bank the battery as a permanent regression test.
**Territory.** test_first_integral_adversarial.py,
               experiments/p2_route_fia_v1_adversarial.py,
               writeup/data/p2_route_fia_v1_adversarial.json,
               writeup/novelty/leg_107.md, experiments/journal/leg_107.md
**Difficulty.** standard
**Independence.** Reads solver/first_integral.py; edits nothing under any outcome. Robustness
audit only, no bound-sharpening or machinery-building.
```

```
### 108 — ROUTE-IX2: SECOND FRESHNESS AUDIT OF writeup/INDEX.md (SINCE LEG 68's PASS)
**Thesis.** Leg 68 (IX) closed writeup/INDEX.md's staleness gap as of legs 53-57. Since then,
legs up through the 100s have landed -- most under the "no measurement, no figure" convention
this cycle established for audit/literature/hygiene legs (the same convention Route-D scope and
Route-D v15 set precedent for), so INDEX.md's Arc 4 table may not need a new row per leg the way
earlier arcs did -- but that convention itself needs to be confirmed CORRECTLY REFLECTED in
INDEX.md, not just assumed. Given the volume (100+ legs since leg 68's pass, several with real
findings), a second pass is due -- the same audit, new window, mirroring leg 102 (JR2)'s
relationship to leg 72.
**Gate.** Does writeup/INDEX.md correctly account for every leg landed since leg 68's pass --
either with a full quartet row (for legs that produced one) or an explicit note that the leg
falls under the "no figure by design" audit/literature convention (for legs that did not)?
  yes -> Confirmed current; report and close as a clean audit, no edits needed.
  no  -> Add the missing rows/notes, marking `GAP` explicitly wherever a leg's documentation
         status is genuinely unclear rather than guessing.
**Territory.** writeup/INDEX.md (append-only edit), writeup/novelty/leg_108.md,
               experiments/journal/leg_108.md
**Difficulty.** light
**Independence.** Touches one file outside any other leg's territory. Same pattern as legs 68
and 102, different scope (INDEX.md vs. JOURNAL.md) and a later time window than leg 68's.
```

```
### 109 — ROUTE-RCA: ADVERSARIAL AUDIT OF reduced_certificate.py's SELF-CONSISTENCY CLAIM
**Thesis.** solver/reduced_certificate.py holds "the whole certificate in floats," validated as
"internally self-consistent across the reduced space; explicitly NOT a proof -- float64
throughout." Self-consistency is exactly the kind of property that can be silently violated
under adversarial inputs without the code noticing -- nobody has checked whether the module can
be fed a battery of adversarial/degenerate inputs (NaN-poisoned terms, near-singular sub-blocks)
that it reports as "self-consistent" when they are not. Same robustness-only precedent as legs
100/101/106/107.
**Gate.** Under an adversarial battery of degenerate or NaN-poisoned inputs, does
solver/reduced_certificate.py ever report internal self-consistency on a case that is not
actually self-consistent?
  yes -> A silent-corruption gap. Report the exact failing case precisely; escalate, do not
         patch under this leg's own authority.
  no  -> Confirmed robust. Bank the battery as a permanent regression test.
**Territory.** test_reduced_certificate_adversarial.py,
               experiments/p2_route_rca_v1_adversarial.py,
               writeup/data/p2_route_rca_v1_adversarial.json,
               writeup/novelty/leg_109.md, experiments/journal/leg_109.md
**Difficulty.** standard
**Independence.** Reads solver/reduced_certificate.py; edits nothing under any outcome.
Robustness audit only, no bound-sharpening or machinery-building.
```

```
### 110 — ROUTE-L1R: L1 DEATH-CERTIFICATE REPRODUCTION AUDIT (ASSIGNED, LEG-C)
**Thesis.** The single most consequential negative in the repository — "L1 is dead in both
realizations" (coefficient basis, leg 54; collocation basis, leg 56) — now gates the plan of
record, the stage-V ban's lift condition, and the framing of NG itself. Leg 60/PQ just proved
this project's banked negatives can partially fail reproduction from their own stored data
(two quoted numbers did not reproduce; a probable transcription slip). Nobody has run that
same reproduction discipline against the L1 death certificates. This leg re-derives every
quoted headline number of both deaths — the +0.639 divergence-curve minimum, the 0.606-empty
window, the per-class tail-divergence exponents, and the collocation realization's failing
quantities — strictly from the banked `writeup/data` JSONs, touching no solver and re-running
no measurement. It does NOT touch leg 60's two results or its escalation, and it lifts no ban
under any outcome: a reproduction failure is a report to the user, not a revival of L1.
**Gate.** Does every quoted headline number in the two L1 death records (PHASE2_P2_NOTES.md
§§ for legs 54 and 56, and everywhere those numbers are re-quoted) reproduce exactly from the
banked JSON data alone?
  yes -> The death is final at the data level. Bank the reproduction script as a permanent
         regression check and say so wherever the death is cited.
  no  -> Report the exact discrepancy (file, field, quoted vs reproduced) and ESCALATE to the
         user; change no conclusion, lift no ban, and do not re-measure under this leg.
**Territory.** experiments/p2_route_l1r_v1_repro.py, writeup/data/p2_route_l1r_v1_repro.json,
               writeup/novelty/leg_110.md, experiments/journal/leg_110.md.
               Read-only: leg_54_verify_headline.json, p2_route_l1_v1_interval.json,
               p2_route_l1_v2_spectral.json, plus the leg-56 collocation record located via
               PHASE2_P2_NOTES.md. No solver module.
**Difficulty.** light
**Independence.** No solver module, no shared JSON writes. Same pattern as PQ, different
result; explicitly disjoint from leg 60's numbers and its parked escalation.
```

```
### 111 — ROUTE-WE: THIRD-REALIZATION SCOPING — WEIGHTED-ENERGY COERCIVITY ON THE a=0 CLM
KNOWN-ANSWER OBJECT (ASSIGNED, LEG-D)
**Thesis.** L1 is dead in two realizations, and lesson 87 says why in operator terms: every
ell-1-Fourier tail estimate assumes the unbounded part is a diagonal MULTIPLIER, and inviscid
self-similar transport carries a SHIFT. The same lesson records that the certified INVISCID
blow-ups in the literature (Chen-Hou) did not use that machinery at all — they used weighted
ENERGY estimates. That is a third realization, distinct from both dead ones, and nothing in
the ban list covers it: it is not tuning s, weight family, K, or border direction inside the
Z_1 machinery (all banned, lesson 88), not domain extension (banned), not stage B, and not
stage V. This leg MEASURES, on the friendliest available object (the a=0 CLM linearization,
one mode, analytic), the coercivity gap of the weighted-energy quadratic form for a small
NAMED family of weights fixed in the driver before any computation — a magnitude under grid
refinement, not a boolean. capabilities.py is grepped for the object before any solver code
is written (standing ban). Under either outcome this leg claims no stage — NG stays NEXT —
and its yes-branch escalates, it does not build.
**Gate.** For at least one weight in the pre-named family, is the measured coercivity gap of
the weighted-energy form on the a=0 CLM linearization positive and stable (within a
pre-committed tolerance declared in the driver) across two grid refinements?
  yes -> A candidate third realization for L1 exists. Bank the magnitudes and ESCALATE
         scoping to the user; build nothing further under this leg.
  no  -> The weighted-energy realization joins the dead list on the friendliest object, and
         the wall bounds the real target's difficulty from below. Bank it as a third dead
         realization, which STRENGTHENS NG's framing; report magnitudes, not the boolean.
**Territory.** solver/energy_coercivity.py (NEW), test_energy_coercivity.py (NEW),
               experiments/p2_route_we_v1_coercivity.py,
               writeup/data/p2_route_we_v1_coercivity.json,
               writeup/novelty/leg_111.md, experiments/journal/leg_111.md
**Difficulty.** heavy
**Independence.** Sole owner of a brand-new module; reads capabilities.py (grep only).
Touches nothing owned by 58/62/100/101/107/109 or the repairs in flight. Lesson-87-shaped,
not Z_1-shaped: no quantity this leg computes appears in the banned tuning list.
```

```
### 112 — ROUTE-AS2: VERIFY §24's TWO LOAD-BEARING READINGS OF arXiv:2603.25104 FROM THE
FULL PDF (ASSIGNED, LEG-E)
**Thesis.** §24's "L1 is occupied territory" verdict — which re-priced the entire Route-D
programme — rests on two readings its own text flags as UNVERIFIED: the a-sign in
arXiv:2603.25104, and whether that paper's fixed point IS the banked first integral. §24
says, verbatim, "the binding constraint on the next decision is ACCESS, not compute and not
cleverness," and instructs treating the a>0 two-scale object as POSSIBLY WRONG until a
session with PDF access verifies both. This environment has that access. The repository has
been burned twice by literature read at the wrong depth (leg 53's abstract-page loss; CP
exists for the same reason). Settle both readings from the full text, record the hypotheses
verbatim, links not counts. This is not a re-litigation of either parked escalation and it
lifts no ban: whatever the answer, L1 stays measured-dead — only its EXTERNAL-NOVELTY price
can move.
**Gate.** Does the full text of arXiv:2603.25104 confirm both load-bearing readings — the
a-sign as §24 read it, and the identity of its fixed point with the banked first integral?
  yes -> The occupied-territory verdict is confirmed at full-text depth. Bank the verbatim
         hypotheses as a ledger entry in this leg's own JSON; close §24's open instruction.
  no  -> The verdict rests on a misreading. Report exactly which reading fails and how, and
         ESCALATE — the external pricing of L1 changes, though its measured death does not.
**Territory.** experiments/p2_route_as2_v1_lit.py, writeup/data/p2_route_as2_v1_lit.json,
               writeup/novelty/leg_112.md, experiments/journal/leg_112.md.
               Does NOT edit solver/literature_gates.py (leg 62's territory).
**Difficulty.** light
**Independence.** Literature-only, own JSON, no solver module. Disjoint from 62 (different
paper, different question) and from both parked escalations.
```

```
### 113 — ROUTE-MS: LESSON 87's MULTIPLIER/SHIFT PREDICTION, CHECKED AGAINST THE
CERTIFIED-BLOW-UP LITERATURE (ASSIGNED, LEG-F)
**Thesis.** Lesson 87 carries an explicitly UNCHECKED prediction, flagged in its own text:
certified self-similar blow-ups that used ell-1-Fourier/radii-polynomial machinery
(Dahne-Figueras, CGL) are all dissipative — diagonal multiplier — while certified inviscid
ones (Chen-Hou) used weighted energy estimates instead. If that taxonomy is right, it is the
operator-shape law behind both L1 deaths and behind NG's mechanism, and it directly motivates
leg 111's third realization. If it is WRONG — if any published certified inviscid
self-similar blow-up runs a diagonal-tail framework — then the dead realization has a
published repair this project missed, which outranks everything else in this queue. Check it
from full texts, verbatim hypotheses, links not counts. Scope guard: where the survey passes
through Cadiot arXiv:2505.03091 it records METHOD SHAPE only and defers every
coverage-of-NG's-hypothesis question to leg 62, which owns that question.
**Gate.** Does any published certified INVISCID self-similar blow-up use a diagonal-tail
(ell-1-multiplier / radii-polynomial) framework for its linearized tail estimate?
  yes -> Lesson 87's prediction is falsified and a published repair to the dead realization
         may exist. Record the citation and its hypotheses verbatim; ESCALATE.
  no  -> The prediction is confirmed across the surveyed set. Bank the ledger; the
         operator-shape law stands as the stated reason L1's two realizations died, and
         leg 111 inherits the strengthened motivation.
**Territory.** experiments/p2_route_ms_v1_lit.py, writeup/data/p2_route_ms_v1_lit.json,
               writeup/novelty/leg_113.md, experiments/journal/leg_113.md.
               Does NOT edit solver/literature_gates.py (leg 62's territory).
**Difficulty.** light
**Independence.** Literature-only, own JSON. Disjoint from 62 by the pre-committed scope
guard above and from 112 (different papers, different question).
```

```
### 114 — ROUTE-CNA: ADVERSARIAL AUDIT OF collocation_newton.py (ASSIGNED, LEG-G)
**Thesis.** solver/collocation_newton.py is the solver behind the COLLOCATION realization of
L1 — one of the two death certificates leg 110 audits at the data level. This leg audits the
same conclusion at the code level, by the pattern that has found 11 real bugs in ~15 tries
this session: under adversarial or degenerate inputs (NaN-poisoned residuals, near-singular
Jacobian blocks, degenerate node spacing), does the Newton solve ever report convergence or
a small residual on a case where the reported answer is wrong? Robustness-only precedent of
legs 69/100/101: no bound-sharpening, no new machinery, edits nothing.
**Gate.** Under an adversarial battery of degenerate or poisoned inputs, does
solver/collocation_newton.py ever report a converged solution or plausible residual that is
silently wrong?
  yes -> A silent-corruption gap in a death-certificate-bearing module. Report the exact
         failing case; escalate, do not patch under this leg's own authority.
  no  -> Confirmed robust. Bank the battery as a permanent regression test; the collocation
         death gains a code-level audit to match 110's data-level one.
**Territory.** test_collocation_newton_adversarial.py,
               experiments/p2_route_cna_v1_adversarial.py,
               writeup/data/p2_route_cna_v1_adversarial.json,
               writeup/novelty/leg_114.md, experiments/journal/leg_114.md
**Difficulty.** standard
**Independence.** Reads solver/collocation_newton.py; edits nothing under any outcome.
Complementary to 110 (data level vs code level), zero file overlap with it.
```

```
### 115 — ROUTE-DCA: ADVERSARIAL AUDIT OF decay_collocation.py (RESERVE)
**Thesis.** solver/decay_collocation.py is the nodal spectral core under the collocation
lane. Same silent-corruption question, same robustness-only precedent as legs 69/100/101:
under NaN-poisoned nodal values or degenerate decay/grading parameters, does it silently
return finite plausible-looking wrong values instead of flagging the input?
**Gate.** Under an adversarial battery of degenerate or poisoned inputs, does
solver/decay_collocation.py ever silently return a wrong value rather than propagating or
flagging the invalid input?
  yes -> Silent-corruption gap; report the exact failing case; escalate, do not patch.
  no  -> Confirmed robust; bank the battery as a permanent regression test.
**Territory.** test_decay_collocation_adversarial.py,
               experiments/p2_route_dca_v1_adversarial.py,
               writeup/data/p2_route_dca_v1_adversarial.json,
               writeup/novelty/leg_115.md, experiments/journal/leg_115.md
**Difficulty.** standard
**Independence.** Reads solver/decay_collocation.py only; edits nothing. Disjoint from 114
(different module, same lane).
```

```
### 116 — ROUTE-NKA: ADVERSARIAL FABRICATION-REJECTION AUDIT OF nk_bounds.py (ASSIGNED,
LEG-H)
**Thesis.** solver/nk_bounds.py computes Newton-Kantorovich bounds — the quantity whose
entire meaning is "everything inside this ball is certified." The one property that must
hold is that a WRONG point cannot survive inside a reported ball. Legs 79 and 98 ran exactly
this fabrication-rejection pattern against the port and the interval certificate and found
real gaps; nobody has run it against the NK bound module itself. Plant wrong points, poison
inputs, degrade constants; check whether a reported certified ball ever contains a planted
non-solution.
**Gate.** Under an adversarial battery (planted wrong points, poisoned constants, degenerate
operators), does solver/nk_bounds.py ever report a certified ball that a planted
non-solution survives?
  yes -> A soundness violation in the certifying bound itself. Report the exact failing
         case; escalate, do not patch under this leg's own authority.
  no  -> Confirmed sound under the battery. Bank it as a permanent regression test.
**Territory.** test_nk_bounds_adversarial.py, experiments/p2_route_nka_v1_adversarial.py,
               writeup/data/p2_route_nka_v1_adversarial.json,
               writeup/novelty/leg_116.md, experiments/journal/leg_116.md
**Difficulty.** standard
**Independence.** Reads solver/nk_bounds.py; edits nothing under any outcome.
Fabrication-rejection precedent of legs 79/98.
```

```
### 117 — ROUTE-HRA: ADVERSARIAL AUDIT OF hl_rescaled.py (RESERVE)
**Thesis.** solver/hl_rescaled.py carries the rescaled HL dynamics and has dedicated tests
but no adversarial battery. Same silent-corruption question and robustness-only precedent as
legs 69/100/101/106.
**Gate.** Under an adversarial battery of degenerate or poisoned inputs, does
solver/hl_rescaled.py ever silently return a wrong result instead of flagging the input?
  yes -> Silent-corruption gap; report the exact failing case; escalate, do not patch.
  no  -> Confirmed robust; bank the battery as a permanent regression test.
**Territory.** test_hl_rescaled_adversarial.py,
               experiments/p2_route_hra_v1_adversarial.py,
               writeup/data/p2_route_hra_v1_adversarial.json,
               writeup/novelty/leg_117.md, experiments/journal/leg_117.md
**Difficulty.** standard
**Independence.** Reads solver/hl_rescaled.py only; edits nothing.
```

```
### 118 — ROUTE-TPA: ADVERSARIAL AUDIT OF turning_point.py (RESERVE)
**Thesis.** solver/turning_point.py (Route-D v13's module) detects turning points — a
classification output that can silently mislabel under degenerate input. Same
robustness-only precedent; classification modules have not yet been covered by the audit
family.
**Gate.** Under an adversarial battery (degenerate branches, poisoned derivatives), does
solver/turning_point.py ever silently return a wrong classification instead of flagging the
input?
  yes -> Silent-corruption gap; report the exact failing case; escalate, do not patch.
  no  -> Confirmed robust; bank the battery as a permanent regression test.
**Territory.** test_turning_point_adversarial.py,
               experiments/p2_route_tpa_v1_adversarial.py,
               writeup/data/p2_route_tpa_v1_adversarial.json,
               writeup/novelty/leg_118.md, experiments/journal/leg_118.md
**Difficulty.** standard
**Independence.** Reads solver/turning_point.py only; edits nothing.
```

```
### 119 — ROUTE-HHA: ADVERSARIAL AUDIT OF hilbert_holder.py (RESERVE)
**Thesis.** solver/hilbert_holder.py carries Hilbert-transform Holder estimates — bound-
bearing code, same category as hilbert_pointwise.py, which leg 106 just audited (gate NO,
robust). Extend the same bound-direction battery to the Holder sibling.
**Gate.** Under adversarial/degenerate inputs, can any bound hilbert_holder.py reports be
exceeded (fail to be a true bound), or a wrong value be silently returned?
  yes -> Soundness/corruption gap; report the exact failing case; escalate, do not patch.
  no  -> Confirmed robust; bank the battery as a permanent regression test.
**Territory.** test_hilbert_holder_adversarial.py,
               experiments/p2_route_hha_v1_adversarial.py,
               writeup/data/p2_route_hha_v1_adversarial.json,
               writeup/novelty/leg_119.md, experiments/journal/leg_119.md
**Difficulty.** standard
**Independence.** Reads solver/hilbert_holder.py only; edits nothing.
```

```
### 120 — ROUTE-SUA: ADVERSARIAL AUDIT OF spectral_utils.py — THE SHARED CORE (ASSIGNED,
LEG-I)
**Thesis.** solver/spectral_utils.py is shared utility code that many solver modules import
— the same load-bearing position solver/interval.py held when leg 69 audited it and set the
shared-core precedent. It has dedicated tests (test_spectral_utils_dedicated.py) but no
adversarial battery. A silent corruption here propagates into every downstream module at
once, including already-audited ones, so it is the highest-leverage unaudited target left.
**Gate.** Under an adversarial battery of degenerate or poisoned inputs, does
solver/spectral_utils.py ever silently return a wrong value instead of propagating or
flagging the invalid input?
  yes -> A silent-corruption gap in shared core code. Report the exact failing case and
         which downstream modules consume the affected function; escalate, do not patch.
  no  -> Confirmed robust; bank the battery as a permanent regression test.
**Territory.** test_spectral_utils_adversarial.py,
               experiments/p2_route_sua_v1_adversarial.py,
               writeup/data/p2_route_sua_v1_adversarial.json,
               writeup/novelty/leg_120.md, experiments/journal/leg_120.md
**Difficulty.** standard
**Independence.** Reads solver/spectral_utils.py only; edits nothing. Distinct from
spectral_certificate.py (58's territory) — different module, checked explicitly.
```

```
### 121 — ROUTE-CDA: ADVERSARIAL AUDIT OF critical_dissipation.py (RESERVE)
**Thesis.** solver/critical_dissipation.py computes critical dissipation exponents — the
same category of quantity whose sibling module (fractional_gclm.py) leg 91 audited. Same
silent-corruption question, same robustness-only precedent.
**Gate.** Under an adversarial battery of degenerate or poisoned inputs, does
solver/critical_dissipation.py ever silently return a wrong exponent instead of flagging
the input?
  yes -> Silent-corruption gap; report the exact failing case; escalate, do not patch.
  no  -> Confirmed robust; bank the battery as a permanent regression test.
**Territory.** test_critical_dissipation_adversarial.py,
               experiments/p2_route_cda_v1_adversarial.py,
               writeup/data/p2_route_cda_v1_adversarial.json,
               writeup/novelty/leg_121.md, experiments/journal/leg_121.md
**Difficulty.** standard
**Independence.** Reads solver/critical_dissipation.py only; edits nothing.
```

```
### 122 — ROUTE-ASA: ADVERSARIAL AUDIT OF advection_scope.py (RESERVE)
**Thesis.** solver/advection_scope.py scopes advection terms and has never been through the
audit family. Same silent-corruption question, same robustness-only precedent as legs
69/100/101.
**Gate.** Under an adversarial battery of degenerate or poisoned inputs, does
solver/advection_scope.py ever silently return a wrong result instead of flagging the input?
  yes -> Silent-corruption gap; report the exact failing case; escalate, do not patch.
  no  -> Confirmed robust; bank the battery as a permanent regression test.
**Territory.** test_advection_scope_adversarial.py,
               experiments/p2_route_asa_v1_adversarial.py,
               writeup/data/p2_route_asa_v1_adversarial.json,
               writeup/novelty/leg_122.md, experiments/journal/leg_122.md
**Difficulty.** standard
**Independence.** Reads solver/advection_scope.py only; edits nothing.
```

```
### 123 — ROUTE-EXT6: FRESHNESS — ANY NEW CERTIFIED INVISCID SELF-SIMILAR RESULT, OR gCLM
a>0 CERTIFICATE, SINCE THE EXT-FAMILY'S LAST WINDOWS? (RESERVE)
**Thesis.** The EXT family (74/77/82/90/93) watches whether the outside world moves under
this project's feet. The highest-value watch target now is the exact territory L1's death
and NG's proposition occupy: a new certified inviscid self-similar blow-up, or a completed
gCLM a>0 certificate, published since the last EXT windows closed, would re-price both at
once. Same pattern, new window, new target class; links not counts, full-text depth for
anything that hits.
**Gate.** Has any result been published since the last EXT-family window that either (a)
certifies an inviscid self-similar blow-up profile by any method, or (b) completes a
computer-assisted gCLM a>0 blow-up certificate?
  yes -> Locate the statement, record hypotheses verbatim, and escalate — NG's novelty and
         L1's external pricing both move.
  no  -> The window stays clear; bank the dated null ledger entry as the EXT family always
         has.
**Territory.** experiments/p2_route_ext6_v1_target_watch6.py,
               writeup/data/p2_route_ext6_v1_target_watch6.json,
               writeup/novelty/leg_123.md, experiments/journal/leg_123.md
**Difficulty.** light
**Independence.** Literature-only, own JSON. Disjoint from 112/113 (those verify specific
already-cited papers; this watches for NEW ones) and from 62 (Cadiot coverage question).
```

```
### 124 — ROUTE-FSA: ADVERSARIAL AUDIT OF finite_support.py (RESERVE)
**Thesis.** solver/finite_support.py has neither a dedicated test file in the repository
root nor an adversarial battery — the thinnest coverage of any solver module still standing.
Same silent-corruption question, same robustness-only precedent.
**Gate.** Under an adversarial battery of degenerate or poisoned inputs, does
solver/finite_support.py ever silently return a wrong result instead of flagging the input?
  yes -> Silent-corruption gap; report the exact failing case; escalate, do not patch.
  no  -> Confirmed robust; bank the battery as a permanent regression test.
**Territory.** test_finite_support_adversarial.py,
               experiments/p2_route_fsa_v1_adversarial.py,
               writeup/data/p2_route_fsa_v1_adversarial.json,
               writeup/novelty/leg_124.md, experiments/journal/leg_124.md
**Difficulty.** standard
**Independence.** Reads solver/finite_support.py only; edits nothing.
```

```
### 125 — ROUTE-M2P: M2 PROMOTION — CHEN'S γ=2 DISSIPATIVE gCLM PROFILE, FULL TEXT +
CONSTANTS + FIRST Y_0 BUDGET MEASUREMENT (ASSIGNED, LEG-J, user-directed 2026-08-06)
**Authority.** User directive 2026-08-06 ("pursue this if it might be beneficial...") plus the
DM's legality ruling in Status: OUTSIDE stage V's ban (which stands unmodified — see the six
numbered points), no gCLM dynamics run (JSON records `no_dynamics_run: true`). NG stays NEXT;
this leg claims no stage. Branch `leg/m2-v1` stays parked: READ it via `git show`, never merge
it or build on it — everything leg 125 needs is re-derived on its own branch from main.
**Thesis.** Leg 63 found the only screen-passing candidate in 63+ legs — gCLM with full
Laplacian dissipation (γ=2), tail-inverse K-exponent -2.0270, blow-up PROVED analytically
(Chen arXiv:1908.09385) — and explicitly did not: read Chen's full text (the a-neighbourhood
is unquantified, the dissipation-coefficient dependence unstated), transcribe the profile's
constants, or measure Y_0. This leg discharges exactly those three debts, in order. (i) Novelty
pass FIRST, narrow: γ=2 / full-Laplacian gCLM CAP attempts specifically, links not counts.
(ii) Full-text read of arXiv:1908.09385 at line-level depth — this includes resolving the γ
tension VER-I's leg-64 review already surfaced (Chen's γ=|a|^{-1} holds only for a ≤ -1; at
a=1/2 his text gives γ=1 from L^1 conservation, while the abstract claims self-similar blow-up
at "a close to 1/2 and γ=2") — locate the theorem, quote it verbatim, transcribe the profile
equation and every constant with provenance. The repository has been burned twice by
abstract-depth reading (leg 53/BDL; leg 64's Trap 1). (iii) Construct the profile numerically
(Newton on the steady self-similar equation, NEW module) at >= 2 resolutions and compute the
first Y_0 against the pipeline's radii-polynomial budget. The μ=2 positive control from leg 53
(Z_1 = 0.9156) is RE-READ against this candidate, not assumed to transfer. Honest ceiling,
pre-committed: this is not movement on L1→L4 and not Clay (odds stay ~0.05%); the prize is the
sub-goal — no CAP of any dissipative self-similar profile exists in the searched literature,
so even the measured Y_0 is a novel data point. Tripwire from the legality ruling: if the work
drifts into floating a dissipation parameter against an existing certificate's margin, that IS
stage V as posed — stop and escalate.
**Gate.** With Chen's theorem located and constants transcribed from the FULL TEXT, and the
profile constructed at two or more resolutions, does Y_0 come in under the radii-polynomial
budget at any tested resolution?
  yes -> The candidate advances. Bank the magnitudes; ESCALATE a full certificate-attempt leg
         to the user (escalation #1 — entering the committed sequence stays the user's call).
         Build no certificate under this leg's own authority.
  no  -> Report the measured Y_0 and its gap to budget; the candidate is set aside as
         "identified, measured, not under budget" — no retry without new information. If the
         full text does not support the abstract as read (no explicit profile at γ=2, or the
         a-neighbourhood excludes every usable case), that lands here too: quote the located
         text verbatim and the candidate leaves the ledger's top slot on literature grounds —
         which is itself the finding.
**Territory.** solver/dissipative_profile.py (NEW), test_dissipative_profile.py (NEW),
               experiments/p2_route_m2p_v1_promotion.py,
               writeup/4_p2_lottery/BLOG_P2_ROUTEM2P_V1.md,
               writeup/4_p2_lottery/TECHNICAL_P2_ROUTEM2P_V1.md,
               writeup/data/p2_route_m2p_v1_promotion.json,
               writeup/figures/fig61_route_m2p_v1_promotion.png (next free figure number),
               writeup/novelty/leg_125.md, experiments/journal/leg_125.md
**Difficulty.** standard
**Independence.** Sole owner of a brand-new module (capabilities.py grepped first, standing
ban). Reads solver/fractional_gclm.py (unowned) and leg 53's banked control read-only. Touches
NOTHING owned by 58 (spectral_certificate.py), 62 (certificate_shapes.py,
literature_gates.py), 111 (energy_coercivity.py), 114/116/120 (their audit targets), the
repairs in flight (holder_norms.py, op_lower.py, first_integral.py), the red-test modules
(fractional_boussinesq.py, profile_newton.py), or either parked branch (leg/m2-v1, leg/pq-v1).
JSON name pre-checked distinct from every live and reserve leg — no collision.
```

## Ranking rationale

Refreshed whenever a gate answers. Rank by, in order:

1. could this leg actually move a link of the L1→L4 chain;
2. can its gate answer either way within one leg's work;
3. is it independent of the other nine live legs.

**Refreshed 2026-08-06 (DM cycle: 110-series). This paragraph supersedes the 2026-08-05
refresh below for ranking purposes.** Criterion (1) is no longer entirely quiet, and that is
the news of this refresh. L1 is measured dead in both realizations, and the plan treats that
as law — but "dead in both realizations" is exactly two facts, and this cycle produced a
reason to audit each and a lesson-87-shaped reason to believe a THIRD realization was never
tried. Hence the top of the queue: **110 (L1R)** applies leg 60's hard-won discipline
(banked negatives can fail reproduction from their own data) to the most consequential
negative in the repository, at light cost, gate decidable either way in hours; **111 (WE)**
is the only leg on the board that could genuinely re-price the dead link — the
weighted-energy realization lesson 87 itself points at, untouched by any ban because it
shares no quantity with the banned Z_1/s/K/border tuning space — and its yes-branch
escalates rather than builds, so it cannot collide with NG's claim to NEXT; **112 (AS2)**
closes §24's own explicitly-open instruction (verify the two load-bearing readings; the
binding constraint was ACCESS, which this environment now has); **113 (MS)** checks lesson
87's flagged-unchecked prediction, whose falsification would outrank everything else here.
None of these four claims chain movement — per inherited law §5, ordering by proximity to
the chain is a choice of what to try, never a claim about what happened. Below them, the
audit family continues on criterion (2)+(3) grounds (11 real bugs in ~15 tries): **114
(CNA)** and **120 (SUA)** rank above their siblings because collocation_newton.py bears a
death certificate and spectral_utils.py is shared core (leg 69's precedent); **116 (NKA)**
carries the fabrication-rejection pattern (legs 79/98, both hits) to the certifying bound
itself. Reserve order: 103/104 first (post-repair closes, now unblocked by 92's and 99's
landings), then 115, 123, 117, 118, 119, 121, 122, 124. Legs 58 and 62 keep their standing
rank and entries unchanged. Nothing in this refresh lifts a ban, re-litigates either parked
escalation, or moves any claim about Walls 1 and 2; Clay stays ~0.05%.

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
2. **RESOLVED 2026-08-06 by user directive.** The user ruled: *"Leg 63, let's pursue this if
   it might be beneficial towards our goal of solving Clay or towards our sub-goal of producing
   novel beneficial output."* The DM's legality ruling (see Status) finds pursuit does not
   require lifting stage V's ban — the ban stands, unmodified, and a from-scratch certification
   of Chen's fixed-γ=2 dissipative profile is outside its scope ("stage V as posed" is margin
   continuation in float, which this is not); even under the prior broad reading, the directive
   is exactly reading (c) below, a narrow single-candidate authorization. The benefit condition
   is met on the novel-output prong (Clay prong honestly fails; odds stay ~0.05%). **Leg 125
   (ROUTE-M2P) is drafted in the queue and assigned to LEG-J.** Branch `leg/m2-v1` stays
   parked and unmerged regardless — leg 125 re-derives on its own branch. The original entry is
   preserved below for the record:
   Leg 63 (M2) landed: gate **YES**. Every inviscid target ever
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
