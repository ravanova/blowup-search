# DIRECTION — the leg queue

**Owner: the Decision Maker (Fable 5). No other agent edits this file.**

This is the Decision Maker's durable state. It exists so a DM whose context has bloated can be
discarded and recreated from the file instead of re-derived from the whole repository.

It is **not** `plan_of_record.py`. The plan carries the committed sequence and exactly one
stage marked `NEXT`; this file carries the *exploration* routes running alongside it. Promoting
a route from here into the plan's committed sequence is escalation #1 in `ORCHESTRATION.md` §8
and needs the user.

---

## Composition floor roster (machine-readable, DM-maintained)

Leg 258 (ROUTE-FLOCK) added this marker so `test_plan_of_record.py` can check
ORCHESTRATION.md §3b's composition floor (>= 3 of the 10 live slots floor-eligible: primary
output is mathematics, external literature, or construction -- not audit, repair, or verify)
without parsing this file's prose. **The DM keeps this block in sync with the "Live-slot
roster" table below on every refill/promotion that changes a slot's occupant or type** --
it is a snapshot of the same facts already stated in prose, not a new source of truth. Only
the block between the two HTML comments is parsed; everything else in this file is free-form
prose as before.

<!-- FLOOR-TABLE-START -->
| Slot | Leg | Route | Eligible |
|---|---|---|---|
| A | 265 | P2C | yes |
| B | 268 | PUB2R | no |
| C | 263 | WESC | no |
| D | 221 | BVRR | no |
| E | 248 | CNR2 | no |
| F | 236 | RDDEP | yes |
| G | 267 | FDL | yes |
| H | 264 | WETP | yes |
| I | 252 | VBRG | no |
| J | 226 | PNR | no |
<!-- FLOOR-TABLE-END -->

(Current snapshot, DM update of 2026-08-07 (slot-A refill after 266+268 landed): 4/10
floor-eligible -- A/265/P2C, F/236/RDDEP, G/267/FDL, H/264/WETP -- matching the "both
corrections landed" DM update at the tail of this file. 265 (Phase-1 costing of the
corrected BCG obligation) was unblocked by 266's landing and promoted immediately as the
top-priority reserve item.)

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
An eleventh refresh adds the **110–124** series, the user-directed promotion adds **125**, the
NG ruling of 2026-08-06 adds **126–127**, and the twelfth refill (the reserve-drain refill of
2026-08-06, drafted concurrently with the NG ruling and rebased on top of it) adds **128–141**.
A thirteenth refill, drafted after leg 126's gate landed NO and exhausted the committed
sequence (see the "leg 126 has landed" Status paragraph below), adds **142–149**. A
fourteenth refill, drafted after the 142–149 batch mostly landed and the reserve drained
again to 0, adds **150–156** (five repair legs closing loops on legs 114/115/117/119/121's
unrepaired YES findings, plus 155/156's fourth freshness pass); legs **118, 122, 124** are
recovered from the older, never-actually-dispatched 110-series reserve rather than
redrafted. A fifteenth refill, drafted in direct response to the user's "pre-empt the
pre-emption" / "consider GA more" steer, adds **157–160** (three literature deep-mine legs on
already-fully-read sources, plus one repaired-fitness leg gated solely by the frozen
six-property check — no GA compute runs under any of the four). A sixteenth refill, in
response to the user's requested strategic-novelty review's concrete action items, adds
**161–162** (LSS full-text read; the untried geometric-weight/compact-support CAP corner),
alongside the correction that leg 125 was legal and ready to dispatch since its 2026-08-06
ruling and should not have been sitting parked. A seventeenth addition, drafted after leg
127 (NGX) landed gate YES-(i) UNVERIFIED (superseding leg 58; citing Xu arXiv:2607.19762 on
origin-H² invertibility) with a full-treatment verifier in flight, adds **163** — a
speculative origin-H² certificate-feasibility SCOPING leg, explicitly NOT dispatchable until
the verifier confirms. An eighteenth refill, responding to a reserve-empty operational
request plus a user steer to weight the batch toward Clay/novel-math over hygiene, adds
**164–171** (three Clay/novelty-thread follow-ups on legs 127/162's findings, five
repair/regression closures), recovers **109, 110** from the old 110-series reserve, and
flags **148** as newly unblocked. A nineteenth addition, answering a user question about
Wall 2 without rewording the odds, adds **172** (a literature scoping leg on whether
validated numerics has ever reached a genuinely 3D PDE model, in any field). A twentieth
addition, responding to a user steer to stop drafting audit/freshness legs and focus Opus on
maths (Part 1), plus three specific math directions to scope (Part 2), adds **173–175** (Xu's
own certification method as a distinct lane; the viscous-certified-blow-up "missing rung"
sharpened against what's already banked; arXiv:2509.14185's own stated obstruction). A
twenty-first refill, keeping the queue flowing continuously per the user's standing
instruction, adds **176–181**: the user-authorized origin-H² construction leg (176), two new
"different space" construction attempts on L1's collocation death and the weighted-energy
window (177, blocked on 165; 178), the leg-58 publication bundle and the two-scale scope-line
correction (179, 180 — both unblocked now that 161/162 landed), and a scoping read of Xu's
modulation technique (181). A twenty-second addition, completing the prior turn's
interrupted draft, adds **182** (H2I, the intermediate-space scoping question between
`ell^1_w` and origin-H²). A twenty-third addition, responding to a user message addressed
directly to the DM relaying an external novelty review's four findings, adds **183** (XU8,
top priority — does Xu §8 pre-empt part of Theorem NGX, blocking leg 179's bundle from being
presented as ready) and **184** (GBW, pins the GA ban's lift condition against the
coarsening loophole leg 160 found — tightens, does not lift, the ban). A twenty-fourth
addition, drafted after leg 184 landed and one slot opened with no fresh reserve, adds
**185** (M2SD, diagnosing leg 125's Object-B Newton stall as genuine non-existence versus a
solver artifact — grounded in leg 125's own already-landed report, found by re-checking git
history directly rather than relying on secondhand summaries). A twenty-fifth addition,
drafted after legs 167 and 182 landed and closed the space-axis investigation cleanly, adds
**186** (PUB2, the space-axis methodological note — `ell^1_w` dead, origin-H² capped at
`a=0`, no interpolant helps — a second, separate synthesis note from leg 179's). A
twenty-sixth addition, drafted to refill 4 open slots (one filled from already-specified
reserve, 170; 148 INCORRECTLY listed as available in this DM's own text at the time — see
the correction below, it stays blocked; one honest gap left open), adds **187** (M2CI — an
unexploited lead in leg 125's own numbers: Chen's inviscid γ=2 profile measured under budget
at every tested row, never certified by anyone; explicitly NOT the viscous rung, a separate
fully-grounded result). A twenty-seventh addition, correcting the 148 error and refilling
per the coordinator's request, adds **188** (SURV, checking whether leg 129's parked
verdict-flip is a necessary consequence of a rule already adopted elsewhere, possibly
resolving escalation #4 without the user) and **189** (XUTRI, a third independent
derivation check on `a_c`/`alpha(1/2)=3` via Xu's own spectral framework). A twenty-eighth
addition, refilling after legs 177/186 landed and only 3 of 10 slots were occupied, adds
**190** (EGML, locating and banking the "EGM" citation) and **192–194** (independent
post-construction verification for legs 176/187/178, drafted now and blocked until each
lands — the postrepair-verification discipline applied to this cycle's new
certificate-construction claims). **191 was WITHDRAWN** (stale premise — leg 60 had already
landed with its correction applied, contrary to 191's assumption; never dispatched, caught
before dispatch) and its number stays retired. A twenty-ninth addition, after the withdrawal
and a spot-check of `origin/main` against every reserve item's blocking premise, adds **195**
(PQVER, replacing 191 — independent verification of leg 60's actually-landed correction),
**196** (USC2, following up leg 175's technique-specific finding — does the authors' later,
obstruction-removed work achieve a certificate) and **197** (VNL, sharing leg 174's located
`arXiv:2208.09445` citation into the shared ledger). **Next fresh leg number for any future
candidate is 198.**

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

**DM ruling 2026-08-06 — leg 58 (NG, critical path) answered YES and escalated; ruling: the
gate answer is VERIFIED, the branch is MERGEABLE AS-IS, stage `NG` goes `DONE` and stage `B`
goes `NEXT` per the plan's own queue; leg 126 (BX) is drafted for the critical-path slot and
leg 127 (NGX) for the queue.** The branch (`leg/ng-v1`, final commit `3f2ee16`, merge base
`ddb4e4c`) was read in full before ruling — the diff, both commits, the TECHNICAL, the novelty
pass, the journal, the solver additions, the runner's arithmetic, and the banked leg 54 battery
(`writeup/data/p2_route_mm_v1_shape.json`) it builds on. Reasoning, in full so it is auditable:

1. **The gate answered YES in its own pre-committed wording, and the wording does not require
   the fully general class.** The gate (`plan_of_record.py`, stage `NG`) asks for "a PROOF for
   a named class of approximate inverses **strictly larger than block-diagonal**, with
   hypotheses that provably contain the `a = 0` CLM linearization" — not for all `A`. The
   named class is `𝒜_upper = {A : A₂₁ = 0}` (block-diagonal AND block-upper-triangular,
   `A₁₂`/`A₂₂` free): strictly larger, since block-diagonal is the single point `A₁₂ = 0,
   A₂₂ = A_tail` inside it, and the containment is verified numerically, not asserted
   (`‖A₂₁‖ = 0` exactly on the in-class shapes while `‖A₁₂‖` reaches 218.97 on `gs_upper`).
   The deliverable's own NG-2 clause pre-authorized exactly this outcome: "extend MM-1 beyond
   block-diagonal A, **or state the restriction honestly**" — leg 58 did both. `NG` does not
   stay open for `A₂₁ ≠ 0`; re-opening a stage whose gate has answered in its pre-committed
   wording is goalpost-moving, and this file will not do it.
2. **The proof itself is checked and correct.** I re-derived it: for `x = (0; h)` with
   `T h = 0`, `(I − AL)x = (−A₁₁Bh − A₁₂Th ; h − A₂₁Bh − A₂₂Th)`; `Th = 0` kills the `A₁₂`
   and `A₂₂` terms, `A₂₁ = 0` kills the third, so `Z₁ ≥ 1 + ‖A₁₁Bh‖_w/‖h‖_w ≥ 1` at every
   split `K` and every `s < 1`. Exact, elementary, three lines. The one inherited dependency
   is honestly attributed: kernel membership (`m⁻²` decay, threshold exactly `s = 1`) is leg
   51's `fredholm_sides`, re-verified here on the vector actually used via the increment-ratio
   ladder (r = 0.2498/0.3785 at s = 0/0.3 — the two classes legs 51–54 actually ran —
   log-divergence exactly at s = 1, r = 0.9988). Both realizations are kept apart (lesson 70):
   the infinite-tail bound is unconditional; the finite-`M` form pays
   `ρ_M(‖A₁₂‖+‖A₂₂‖)` with `ρ_M ~ M^{−(1−s)}`, and the measurement holds to it (min slack
   +5.336e−04, discrepancy/budget ratio 0.5047 < 1 over the whole sweep).
3. **Consistency with the banked record is verified, not assumed.** Leg 54's baseline
   10.4584 and best-admissible 8.9591 re-derive to 7.157e−06 relative; the in-class battery
   minimum 6.0424 ≥ 1 as the theorem requires; MM4c's rank-one escape (floor → ~1e−16 at
   total `Z₁` = 5.7e+05) does not contradict the theorem — it is a finite-`M`
   truncation-budget exploit at enormous `‖A‖`, and the infinite-tail statement never sees
   it. Sharpness is a genuine either-way control: the same two in-class shapes reach 0.6663 /
   0.4026 at `μ = 2` (and the 0.9156-vs-0.6663 convention split with leg 53 is named and both
   numbers emitted). The split-placement objection is measured, not argued — `‖T'⁻¹‖`
   diverges as `M^{+(1−s)}` exactly where `ρ_M` vanishes as `M^{−(1−s)}`, matching to 12
   digits — and is scoped as measured, not proved. The `A₂₁ ≠ 0` class stays "measured, not
   proved" in every place it appears (TECHNICAL §7, solver docstrings, JSON gate fields,
   journal); the scope line is load-bearing and present.
4. **The novelty claim is now doubly confirmed.** NG-0 ran and was committed BEFORE
   construction (`9c8b479`), resolved Cadiot arXiv:2505.03091 from the full text (Fourier
   multiplier, `|l| ≥ l_min > 0`, `|l| → ∞`, infinite diagonal tail — this operator fails all
   three), and pre-committed that leg 62's deeper reading governs on any disagreement. Leg 62
   has since landed on `main` (`59daeaf`, gate NO on the located clauses) and independently
   confirms: Cadiot does not cover the off-diagonal / zero-diagonal case. No located paper
   states a lower bound on `Z₁` over a class of `A` (NG-0's N2, six query framings, links not
   counts). The claim survives at its stated width: the inequality and its class, nothing more.
5. **Merging is NOT an escalation, and leg 58's parking was the over-cautious reading.**
   §8's four escalations: (i) a plan change "other than the one the current gate's
   pre-committed YES/NO branch prescribes" — applying NG's yes-branch IS the pre-committed
   branch, explicitly exempt; (ii) no ban is lifted or weakened; (iii) the prose claims no
   Clay movement — it states the opposite, in the pre-committed ceiling language, and pins
   odds at ~0.05%; (iv) nothing banked is deleted or rewritten. The yes-branch's "escalate
   publication scoping to the user" is a *question for the user*, not a merge blocker: it goes
   under `⚠ NEEDS YOU` while the result banks. Contrast the leg 63 precedent this file set:
   that was a genuine escalation #1 (a plan change no gate had pre-committed); this is the
   opposite case. **Ruling: the orchestrator merges `leg/ng-v1` as-is** (standard finish
   protocol — rebase on current `main`, `scripts/merge_gate.sh`, land), and the §7b
   post-landing verifier does its line-by-line review on `main` — this is the single most
   claim-bearing landing of the run and gets the full treatment.
6. **`plan_of_record.py` changes for the orchestrator, exactly** (integration commit, same
   cycle as the merge): (a) stage `NG` status `NEXT` → `DONE`, recording the yes-branch
   outcome (theorem on `𝒜_upper`/`A₂₁ = 0` at every `K`, every `s < 1`; general `A₂₁ ≠ 0`
   class MEASURED ONLY, battery minimum 8.9591); (b) stage `B` status `QUEUED` → `NEXT` — the
   plan's own queue, not a new stage, so no escalation; B's stage wording is NOT edited;
   (c) `CONTINUATION_PROMPT.md` brought in step (orchestrator-owned; `test_plan_of_record.py`
   enforces agreement); (d) `PROGRESS.md` `⚠ NEEDS YOU` gains the publication-scoping
   question the yes-branch prescribes (the repository now holds a Tier-3-shaped negative
   theorem with its sharpness control; Open question #3 below — the exit criterion — is the
   frame the user should answer it in).
7. **The two flagged loose ends need a bench-repair, not a leg.** (a) `capabilities.py`'s
   `solver/spectral_certificate.py` entry stops at leg 53's assembly and now understates the
   module (the four NG predicate functions, the theorem, the sharpness control) — a one-entry
   factual refresh, same shape as the leg 65 annotation fix (`ab07316`). (b) One docstring
   imprecision found in this review: `block_upper_triangular_bound`'s docstring states the
   finite-`M` bound as `1 − rho·‖A22‖ + floor`, while the honest finite-`M` form (TECHNICAL
   §2a) and the runner (which passes `a12 + a22` as the second argument) use
   `rho·(‖A₁₂‖+‖A₂₂‖)` — no emitted number is wrong, but the parameter name invites misuse;
   rename/clarify in one line. Neither blocks the merge; both go to one mechanical
   bench-repair after it lands. (c) The `writeup/build_figures.py` conflict resolution is
   CORRECT and needs nothing: the list is append-only by standing convention, keeping all four
   entries (46/47/62/58) is the only right resolution, and the rebased diff shows exactly one
   appended line (fig55's evidence script). No cleanup leg.
8. **The critical path after `NG`: stage `B` can only be closed, not run, and closing it
   honestly is the next leg.** B's search has three degrees of freedom, every one now
   separately dead: the space (leg 52), the split (`K/2` at every choice, leg 53), the shape
   of `A` (leg 54 measured; leg 58 now a THEOREM on `A₂₁ = 0`); its GA is banned and the lift
   condition has failed twice (leg 49: 4/6; leg 59: FAIL, P3 worst |slope−1| unmoved at 0.342
   against 0.05); and the third realization is dead too (leg 111/WE, `41f4ac0`: every
   admissible weight's coercivity gap is negative, window width zero). B's own deliverable
   pre-authorizes the exit: "or an honest report that it does not and where the margin runs
   out," and its no-branch is pre-committed ("Report that too. A negative bounds how much of
   the difficulty was tuning versus structure"). **Leg 126 (ROUTE-BX) is drafted below** to
   answer B's gate from the banked record with a genuine either-way completeness audit,
   running no GA compute. On its no-branch the committed sequence is EXHAUSTED — what enters
   next is escalation #1 and the user's call, with the γ=2 dissipative certificate route
   (contingent on leg 125's gate) the obvious leading candidate; Open question #3 is where
   that decision already lives.
9. **The `A₂₁ ≠ 0` mathematics stays alive as exploration, not as the critical path.**
   **Leg 127 (ROUTE-NGX) is drafted below**: prove the full-class no-go via a quantitative
   trade-off, or construct an admissible `A₂₁ ≠ 0` counterexample with `Z₁ < 1` — the one
   outcome that would overturn the measured no-go and revive the method (and which is
   therefore escalation #4 territory on that branch, pre-committed). It is the question
   publication scoping will ask, and the highest-value open mathematics on the board short of
   leg 125. Reserve order updated: 103/104 keep first claim (already promised), then **127**,
   then 115, 123, 117–124 as before. LEG-A refills with 126 the moment `leg/ng-v1`'s merge
   lands; 127 is NOT dispatchable before that merge (it owns files 58 is landing).

---

**DM refresh 2026-08-06, reserve-drain refill (the 128-series). The exploration reserve is
fully drained: every numbered leg through 125 has been dispatched, landed, or escalated, and
the reserve chain the NG ruling above inherited (103/104, then 115, 123, 117–124) has been
fully consumed by dispatch — the orchestrator has had nothing to promote when a slot vacates.
This block was drafted concurrently with the NG ruling above and is rebased on top of it: leg
numbers 126 (BX, critical path) and 127 (NGX) are the ruling's and stand; this refill adds
the fourteen exploration/infrastructure legs 128–141 to the Queue below, and this block is
now the single authoritative account of the reserve, superseding every earlier
reserve/promotion pointer above (including the ruling's point-9 chain, whose pre-128 items
are all dispatched, and the 110-series table's LEG-J flex-slot note).** What this batch is,
and why:

- **The two findings this cycle's audits explicitly flagged for the DM get their repair legs
  first.** Leg 116 (NKA) found the same Y0/Z0/Z1 fabrication-acceptance gap in `nk_bounds.py`
  that legs 79 and 98 found in its two siblings — a **third** instance, flagged for a
  shared-guard repair rather than a third one-off fix: that is **128 (NKR)**. Leg 120 (SUA)
  found the `<= n/3` dealias off-by-one in `spectral_utils.py`, verified the one-character fix
  bit-identical at every grid size the repository has ever run, and located an identical cut in
  `boussinesq.py` plus a dedicated-test assertion that *encodes the defect* — flagged for a
  single repair pass covering all of it: that is **129 (SUR)**. Both are multi-file and
  claim-adjacent, which is exactly why they are legs with verifiers rather than bench-repairs
  (the leg-76 precedent: multi-file, multi-site corrections get a leg).
- **The one unrepaired bound-direction violation on main gets its repair leg**: leg 106 (HPA)
  landed "YES, repair not yet scheduled" on `hilbert_pointwise.py` — that is **130 (HPR)**.
- **Every landed bench-repair that never got its close-the-loop regression leg gets one now**,
  per the 86/87/94/103/104/105 pattern: `boussinesq.py` (leg 89's repair — the most severe
  finding of the audit run, 5.6e13x) is **133 (BOB)**; `fractional_gclm.py` (leg 91) is
  **134 (FGB)**; `holder_norms.py` (leg 100) is **131 (HNB)**; `op_lower.py` (leg 101) is
  **132 (OLB)**; `first_integral.py` (leg 107, repair still in flight) is **135 (FIB)**,
  blocked until that repair merges.
- **One measured residual gets characterized**: the gate-11 partial repair on
  `marginal_flow.py` closed 4 of 9 missed divergent trajectories and left 5 open, deliberately
  not re-escalated — **136 (MF2)** measures whether any pre-named second criterion closes them
  or banks the residual as a characterized permanent limitation.
- **One genuinely new literature question from a banked finding**: leg 111 (WE) killed the
  third realization with a *zero-width window* (damping needs gamma>3, the weighted space
  exists only for gamma<3 — the same threshold). Whether that structural coincidence is
  published anywhere is exactly the L1G/leg-65 question one realization later — **141 (WEL)**
  — and its answer directly strengthens or caps the publication scoping the NG ruling just
  put to the user.
- **Docs freshness on cadence**: the 100–125 landing wave is the largest since either prior
  pass — **137 (JR3)** and **138 (IX3)**.
- **The audit family continues only where genuinely uncovered and safely reachable modules
  remain.** Not yet adversarially audited: `decay_grading.py`, `nk_fourier.py`,
  `nk_seminorm.py`, `viscous_novelty.py`, `energy_coercivity.py` (new this cycle),
  `certificate_shapes.py`/`literature_gates.py` (ledger modules), `ga_search.py` (GA lane,
  banned compute), `rescaled_spectrum.py` (leg 70 was a docs-only realization audit, not an
  adversarial battery), and the currently-unreachable set: `spectral_certificate.py` (claimed
  by leg 127/NGX once `leg/ng-v1` merges), `target_selection.py` (leg 63's parked territory),
  `profile_newton.py`/`fractional_boussinesq.py` (red-test investigation still closing).
  The two most load-bearing of the reachable ones — `decay_grading.py` (graded spaces under
  the collocation lane) and `nk_fourier.py` (the Fourier form of the two-scale operator) —
  get **139 (DGA)** and **140 (NFA)**. The rest are deliberately NOT drafted this pass: thin
  value or unreachable territory, and the family should not become a fishing exercise now
  that its genuinely-uncovered pool is nearly empty.
- **Deliberately not drafted, and why**: repair legs for legs 114/115/117/119/121's brand-new
  YES findings (all landed within hours; the orchestrator's bench-repair path has handled
  every single-module guard fix so far and may already be dispatching these — drafting them
  here would invite a territory collision with a live bench agent; if any is still unrepaired
  at the next refill, it becomes a repair leg then, and its post-repair regression leg after
  that); anything touching leg 125's parked escalation (the inviscid-closed-form finding and
  the a!=0-profile recommendation are the user's call — a reserve leg presupposing that
  ruling would repeat the exact mistake §2's history warns about); a seventh EXT window
  (EXT4/EXT5 windows closed *today*, EXT6 is in flight — no cadence case).

**Dispatchability and recommended order.** **127 (NGX) keeps the first claim the NG ruling
gave it** the moment `leg/ng-v1`'s merge lands (and 126/BX takes LEG-A per the ruling —
neither is this refill's to re-rank). Of the 128-series: immediately dispatchable, in order:
**130, 133, 131, 132, 134, 141, 136, 137, 138, 139, 140**. Blocked, each jumping to the
front the moment its block clears (leg-76 discipline): **128** (until leg 105/ICB lands — it
edits `interval_certificate.py`, which 105 is measuring), **129** (until 133/BOB lands — it
edits `boussinesq.py`, which 133 measures bitwise), **135** (until the
`bench/fix-first-integral-support-extrapolation` repair merges). No leg in this batch depends
on any other leg in it or on any undrafted leg; every gate can answer either way within one
leg's work; territory disjointness is checked explicitly in each entry (none touches
`spectral_certificate.py`, `target_selection.py`, the red-test modules, or anything 126/BX
reads for its audit — 126 owns no solver module, so no collision is possible there).

**DM re-anchor, 2026-08-06 — fresh DM spawn, all ten slots re-dispatched from a vacant board.**
The prior DM session's live agent handles were lost when its container was reclaimed; its
durable work (this file, and everything merged to `main`) survives intact and nothing below
revises any finding. This paragraph is the current, authoritative account of live assignments
and supersedes the 110-series table and its LEG-J flex note above for slot-occupancy purposes
(the 128-series reserve-drain block above it is still the authoritative source for the
individual leg specs and dispatch-order reasoning; only *who currently holds which slot* is
refreshed here).

Ground truth re-verified against `plan_of_record.py` and `git log`, not against this file's own
prose: stages M, PORT, V, C-PILOT, L1, T, TC, MM, NG are DONE; **stage B is NEXT**. Legs with
commits already on `main` include 58, 62, 79, 89, 92, 99, **105**, 107, 116, 120, 123, 60 (PQ,
landed with corrections, not an open escalation), plus the full 1–57 backlog. Legs 125–141 have
**zero commits on main** — all fully specified in the queue above, none previously dispatched
under this incarnation of the DM. Leg 105 (ICB) landing unblocks leg 128 (NKR), which was gated
on it. The `bench/fix-first-integral-support-extrapolation` repair has merged (commits
`9c08287`/`aecafe6`), which technically unblocks leg 135 (FIB) — but leg 135 is deliberately
held in reserve regardless this round, alongside leg 129 (SUR, still genuinely blocked on leg
133/BOB, which has not landed). Leg 63 (M2, escalation #1) stays parked; leg 125 (M2P)
presupposes a user ruling on it that has not been given and is **not dispatched**.

**Fresh ten-slot dispatch, all slots filled from the undispatched 126–141 backlog — no slot is
carried over from any earlier table, since none of the prior session's agents are live to
carry over.**

| Slot | Leg | Route | Critical path? | Difficulty | Branch | Gate (short form) |
|---|---|---|---|---|---|---|
| LEG-A | 126 | **BX** — stage B, answered from the banked record (closure audit) | **YES** (stage `B`, `NEXT`) | standard | `leg/bx-v1` | Does any admissible, ban-respecting corner of stage B's declared search space remain uncovered by the banked record (legs 49,52,53,54,56,58,59,111)? |
| LEG-B | 127 | **NGX** — the general class A21 != 0, proof or counterexample | no | heavy | `leg/ngx-v1` | Can the no-go be decided on the full bounded class — proof for every bounded A, or an explicit admissible A21 != 0 counterexample with Z_1 < 1? |
| LEG-C | 128 | **NKR** — shared-guard repair for the Y0/Z0/Z1 fabrication-acceptance gap (nk_bounds.py + siblings) | no | standard | `leg/nkr-v1` | Do all 21 false-closing cases in leg 116's battery now reject, with port_certification.py / interval_certificate.py bit-identical on clean inputs? |
| LEG-D | 130 | **HPR** — repair the one unrepaired bound-direction violation, hilbert_pointwise.py | no | standard | `leg/hpr-v1` | Do both of leg 106's failing configurations now dominate the true \|H(h)\|, with the module bit-identical elsewhere? |
| LEG-E | 133 | **BOB** — post-repair regression check, boussinesq.py | no | standard | `leg/bob-v1` | Does the repaired module pass leg 89's full battery and reproduce the banked n=32 results bit-identically, independently confirmed? |
| LEG-F | 131 | **HNB** — post-repair regression check, holder_norms.py | no | standard | `leg/hnb-v1` | Does the repaired module reject leg 100's full 6-mechanism battery and reproduce clean calls bit-identically, independently confirmed? |
| LEG-G | 132 | **OLB** — post-repair regression check, op_lower.py | no | standard | `leg/olb-v1` | Does the repaired module return a true lower bound on all 209 of leg 101's cases and reproduce the 307.878-decade headroom, independently confirmed? |
| LEG-H | 134 | **FGB** — post-repair regression check, fractional_gclm.py | no | standard | `leg/fgb-v1` | Does the repaired module reject every s<0/nu<0 case in leg 91's battery and reproduce the banked s_c bit-identically? |
| LEG-I | 141 | **WEL** — is leg 111's zero-width weighted-energy window published? | no | light | `leg/wel-v1` | Does any published work state, imply, or contain leg 111's gamma-threshold coincidence for CLM/gCLM weighted-energy coercivity? |
| LEG-J | 136 | **MF2** — the five divergent trajectories gate 11 still misses | no | standard | `leg/mf2-v1` | Does at least one pre-named second criterion flag all 5 remaining divergent cases with zero false positives across the full battery? |

**Territory-overlap re-check for this dispatch (nine chosen plus 126).** Modules touched:
`solver/spectral_certificate.py`(127, sole owner post-58-merge); `solver/certificate_guards.py`
(128, NEW) + `solver/nk_bounds.py`(128) + `solver/port_certification.py`/
`solver/interval_certificate.py`(128, wiring-only); `solver/hilbert_pointwise.py`(130, sole
owner); `solver/boussinesq.py`(133, read-only regression check); `solver/holder_norms.py`(131,
read-only); `solver/op_lower.py`(132, read-only); `solver/fractional_gclm.py`(134, read-only);
none(141, literature-only); `solver/marginal_flow.py`(136, read-only). 126 (BX) owns no solver
module — reads banked JSONs and landed modules read-only. All distinct — **no collision.**
`writeup/data` JSON names are all distinct per each entry's own Territory field above (checked
directly in the queue entries) — **no collision.**

**Reserve queue: 6 undispatched legs (129, 135, 137, 138, 139, 140).** 129 (SUR) is genuinely
blocked until 133 (BOB, live this round in LEG-E) lands. 135 (FIB) is technically unblocked
(its repair merged) but deliberately held back this round rather than bumping a live slot —
next in line the moment a slot frees. 137 (JR3), 138 (IX3), 139 (DGA), 140 (NFA) are
immediately dispatchable cadence/audit legs, promote in that order without re-ranking unless a
gate answer changes the picture. This count (6) sits inside the 4–6 target band, so no new
candidates are drafted this pass.

**DM update, 2026-08-06 — leg 126 (BX) has landed, gate NO, and the committed sequence is
EXHAUSTED. There is currently NO critical-path leg.** Stage B's full declared search space
(1,686 configurations: 144 by theorem, 1,032 structurally, 510 by measurement) is covered with
zero uncovered corners; even a perfect search over the residual headroom leaves Z₁ >= 6.0424,
6.04x short of closing. Per leg 126's own pre-committed no-branch, this is escalation #1 for
the user, not a DM call — the orchestrator has correctly NOT touched `plan_of_record.py` (doing
so with no replacement `NEXT` stage would violate `test_plan_of_record.py`'s "exactly one
`NEXT`" invariant and break the merge gate repo-wide) and has written it up in `PROGRESS.md`'s
`⚠ NEEDS YOU`, linked alongside the still-open leg 63/125 (M2) escalation and the exit-criterion
question. **This DM's recommendation, per the mandate to choose the work when the plan leaves
the next leg genuinely unclear: no slot claims critical-path status until the user rules.**
LEG-A's designation as "critical path" is retired for now — not reassigned to any other stage,
since none is committed — and every currently live slot is, and should stay, pure exploration
until the user's ruling reinstates a `NEXT` stage (most likely candidate per Open question #3:
the gamma=2 dissipative gCLM route, contingent on leg 125, itself contingent on the same
ruling — so nothing is drafted here that presupposes it, per this file's standing discipline).
Leg 127 (NGX) is confirmed independent of all of this and needs no action — it is mathematics
on the A21 != 0 class, not a claim on stage B or the plan's `NEXT` slot, and stays live.

The orchestrator reports five reserve legs (135/FIB, 137/JR3, 138/IX3, 139/DGA, 140/NFA)
promoted to fill five vacated slots this cycle, beyond leg 126's own. Only two outcomes are
confirmed to this DM directly: **126 landed (gate NO, as above)** and **127 (NGX) is confirmed
still live**. The specific mapping of which four of the other eight originally-dispatched legs
(128, 130, 131, 132, 133, 134, 136, 141) landed/closed versus remain live under their original
slots is not stated in the coordinator's message; per this file's standing practice when a
slot-letter mapping is reported only in aggregate (see the 71/CAP precedent above), this file
defers to the orchestrator's live tracking for the exact ten-slot letter assignment and will
reconcile it explicitly on the next refresh. What is fixed regardless of that mapping: none of
128/130/131/132/133/134/136/141/135/137/138/139/140 claims critical-path status — all ten are,
and stay, pure exploration — and the territory-overlap check already run for each of these
entries (in their own Territory/Independence fields, and in the two dispatch tables above)
holds independent of which specific slot letter each currently occupies.

**Reserve queue after this cycle's five promotions: 1 undispatched leg (129, SUR — still
genuinely blocked until leg 133/BOB lands).** This is below the §3a watermark, so eight new
fully-specified candidates (142–149) are drafted below, in the Queue, following the same
audit-family and post-repair-regression patterns that have had a real hit rate this run:

- **142 (NSA)** and **143 (VNA)** continue the adversarial-audit family onto two of the last
  reachable, never-audited modules (`nk_seminorm.py`, `viscous_novelty.py`) — the family is
  20+ legs deep at roughly a 50% hit rate and these are two of the genuinely few reachable
  modules still uncovered per the 128-series refill's own inventory.
- **144 (ECA)** audits `energy_coercivity.py`, leg 111's brand-new module (landed this run,
  never adversarially tested) — the same "new module gets its first adversarial pass"
  precedent as every other audit-family leg.
- **145 (LGA)** and **146 (CSA)** become dispatchable now that leg 62 (CP) has landed and
  cleared `literature_gates.py`/`certificate_shapes.py` (both were off-limits ledger modules
  while 62 was live; both are confirmed landed per the ground-truth git check this DM ran on
  spawning) — genuinely new territory for the audit family, not a re-tread.
- **147 (NKB)** is the close-the-loop regression leg `nk_bounds.py` will need the moment leg
  128 (NKR) lands, per the 86/87/94/103/104/105/131/132/133/134 pattern — drafted now, blocked
  until 128 merges, so it is ready immediately rather than requiring another refill.
- **148 (SUB)** is the equivalent close-the-loop regression leg for `spectral_utils.py` and
  `boussinesq.py`'s dealias fix, needed the moment leg 129 (SUR) lands — double-blocked (129
  itself is blocked on 133/BOB), drafted now for the same readiness reason.
- **149 (PGF)** is a light hygiene leg: a freshness/self-consistency audit of `PROGRESS.md`'s
  `⚠ NEEDS YOU` escalation ledger itself, newly load-bearing now that three linked escalations
  (leg 126's stage-B exhaustion, leg 63/125's M2 ruling, and the exit-criterion question) sit
  there together for the first time — the same "does the ledger say what actually happened"
  question legs 68/72/102/108/137/138 have asked of every other freshness surface, now asked
  of the one surface the user reads first.

None of the eight presupposes any pending user ruling; none touches `plan_of_record.py`,
`solver/target_selection.py` (leg 63's parked territory), or either parked branch.

**DM note, 2026-08-06 — user-forwarded steer on MD bloat; flagging a maintenance-sweep
recommendation for the orchestrator, not doing the compaction here.** The user asked that the
DM consider Sonnet (or Opus, if the judgment calls warrant it) support-agent tasks to shorten
MD files that don't need their current length, review file structure, and check the README is
current. This is the orchestrator's dispatch, not the DM's edit — the DM's mandate stays
`DIRECTION.md` only — so this is recorded here as a recommendation for the orchestrator to act
on under `ORCHESTRATION.md` §11, split into two pieces because they are NOT symmetric under
§11's own rules:

1. **In scope for a §11 sweep agent, cleanly.** `experiments/JOURNAL.md`,
   `CONTINUATION_PROMPT.md`, `writeup/INDEX.md`'s prose (not its leg table, which is a claim
   ledger), and any other narrative-heavy MD file that has grown by accretion — a Sonnet
   maintenance-sweep agent compacting superseded/redundant prose while leaving every dated
   entry, gate answer, magnitude, and file:line reference verbatim is exactly the "mechanical,
   non-claim-bearing" shape §11 already authorizes, and is a reasonable item for the next
   sweep cycle. A file-structure review and a README freshness check are likewise ordinary
   §11-shaped work. Recommend Opus over Sonnet specifically for the judgment call of *what is
   safe to compact without softening a claim* if the orchestrator finds Sonnet's first pass
   too conservative (compacts nothing) or too aggressive (drops a magnitude or a gate
   qualifier) — that discrimination is exactly the kind of judgment §11 flags as the reason
   claim-bearing items get escalated rather than swept.
2. **Explicitly NOT in scope for a sweep agent as `ORCHESTRATION.md` §11 currently reads.**
   `DIRECTION.md` itself is the file growing fastest (now ~3750 lines) and the most obvious
   candidate for compaction — but §11 states plainly: "Sweep agents obey all of §1 and §5a: no
   ledger edits, **no `DIRECTION.md`**, no banked-result rewrites." That line is not an
   oversight; `DIRECTION.md`'s own header says the DM is its sole owner and no other agent
   edits it, for the explicit reason that recreating the DM from this file is how the system
   survives a lost DM session (as this very spawn demonstrates). So: compaction of
   `DIRECTION.md`'s own superseded-history paragraphs (the "this paragraph supersedes..."
   blocks scattered through Status and Ranking rationale, several of which are now purely
   historical) is either (a) work the DM does itself, in a dedicated pass, under its own
   authority and its own judgment about what is safe to compress without altering a banked
   gate answer or magnitude — recommended the next time this DM is asked to do upkeep rather
   than dispatch, since it is exactly the kind of self-maintenance the file's own design
   anticipates; or (b) a narrow, explicit carve-out to §11 authorizing sweep agents to touch
   `DIRECTION.md` for prose-compaction only (never queue entries, gate wording, or numbers),
   which is a change to `ORCHESTRATION.md` itself and therefore the user's call, not the DM's
   or the orchestrator's to grant unilaterally. Recommend the orchestrator raise (b) to the
   user explicitly rather than assume it, and in the meantime proceed with the JOURNAL.md /
   CONTINUATION_PROMPT.md / README / file-structure sweep under (1), which needs no such
   carve-out and can start immediately.

**DM update, 2026-08-06 — large landing wave; reserve drained again to 0; drafting a fresh
batch, plus a wording correction folded into it.** Since the 142–149 batch: **126 (BX)** landed
first, gate NO, exhausting the committed sequence (recorded above) — no critical-path stage
exists right now, and stays parked pending the user's ruling in `PROGRESS.md`. Also landed this
wave: **128, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141**, plus **142, 143,
144, 145, 146, 147, 149** from the last batch this DM drafted. Only **148 (SUB)** remains
undispatched from that batch, still correctly blocked on leg 129 (SUR), which is in flight.
Reserve is effectively 0 dispatchable items again.

**Correction noted, applies going forward.** The orchestrator flagged that several of this
wave's leg briefs mis-stated a YES (silent-corruption) finding's no-branch as "park it as an
unmerged branch" rather than "merge the report normally, do not patch the module under this
leg's own authority" — corrected repo-wide, legs 139/140 fixed after the fact. Every gate
branch drafted below says explicitly that the leg's own report/finding lands on `main`
regardless of outcome; only patching the audited module itself is what a "no -> escalate,
do not patch" instruction defers to a separate repair leg. This wording is now checked
explicitly in each new entry's gate text, not left implicit.

**Sweep of the older 110-series reserve turned up three fully-specified legs that were never
actually dispatched, despite an earlier table's note that the "103–124 reserve chain... has
been fully dispatched/landed."** `git log` shows no commits for legs **118 (TPA,
turning_point.py)**, **122 (ASA, advection_scope.py)**, or **124 (FSA, finite_support.py)** —
their specs (already in the Queue above, unchanged) are still current and their territory is
still clear (no live or landed leg claims any of the three modules). These rejoin the reserve
immediately, no redrafting needed.

**Five of this wave's audit YES-findings have no repair leg yet, and per this file's own
deferred instruction ("if any is still unrepaired at the next refill, it becomes a repair leg
then") that refill is now.** Legs **114 (CNA, collocation_newton.py: 8 silent corruptions, 3
mechanisms)**, **115 (DCA, decay_collocation.py: 3 silent-corruption gaps)**, **117 (HRA,
hl_rescaled.py: 4 silent-corruption mechanisms)**, **119 (HHA, hilbert_holder.py: bound-
direction violation)**, and **121 (CDA, critical_dissipation.py: non-integer-exponent
truncation)** all landed gate YES with no bench-repair or leg-repair commits found in `git
log` since. Repair legs for all five are drafted below (**150–154**), following the
128/129/130 repair-leg template exactly (fix, prove zero clean-input movement, invert the
adversarial battery's PINs in the same commit).

**Two cadence hygiene legs continue the freshness family** after this wave's size (the
largest since the 100–125 wave that motivated 137/138): **155 (JR4)**, the fourth freshness
pass on `experiments/JOURNAL.md`/`journal/`, and **156 (IX4)**, the fourth freshness pass on
`writeup/INDEX.md`.

**Total fresh reserve after this refill: 10** (three recovered — 118, 122, 124 — plus seven
newly drafted — 150–156), well clear of the §3a watermark. None of the ten touches
`plan_of_record.py`, claims critical-path status, or presupposes the leg 63/125 ruling.
Territory of the five new repair legs (150–154) is checked explicitly against each other, the
128/129/130 repair-leg precedent, and the three recovered legs (118/122/124, different
modules entirely): all eight solver files touched (`collocation_newton.py`,
`decay_collocation.py`, `hl_rescaled.py`, `hilbert_holder.py`, `critical_dissipation.py`,
`turning_point.py`, `advection_scope.py`, `finite_support.py`) are distinct — **no collision.**

**DM response, 2026-08-06 — user steer, forwarded verbatim: "consider pre-empting the
pre-emption" and "consider using GA more, where there is a chance of refining
data/variables."** Decided under the standing directive, on this DM's own read of both:

**On pre-empting the pre-emption.** This repository's own literature legs (57, 62, 65, 90,
93, 111/141, 123) established that several of its negative results and "novel" claims were
already anticipated in the literature — but every one of those legs asked a narrow YES/NO
coverage question ("does paper X already cover/refute claim Y"), never "does paper X, having
already been read at full-text depth, suggest a DIFFERENT construction this repo hasn't
tried." That is genuinely unexplored territory in sources already paid for (no new literature
search cost, full-text access already established) and it is exactly the "read deeper, don't
just confirm/deny" shape the orchestrator's context flagged as legitimate. Three sources
warrant it, each already fully read by a landed leg:
- **Cadiot arXiv:2505.03091** (read in full by leg 62): confirmed NOT to cover the
  off-diagonal/zero-diagonal case, but its own construction was never mined for whether it
  suggests an alternative approximate-inverse DESIGN (not necessarily block-diagonal, not
  necessarily requiring a positive diagonal) that could be adapted to the A21 != 0 class leg
  127 (NGX) is currently searching for a counterexample in. A literature-sourced starting
  candidate would be strictly cheaper than 127's from-scratch construction attempt.
- **BDL arXiv:1503.06315** (read in full by leg 57, confirmed by `plan_of_record.py`'s own
  ban text as "the reason to keep this ban"): publishes a non-block-diagonal approximate
  inverse requiring a diagonal bounded below, confirmed not to extend to the zero-diagonal
  case. Never checked: does BDL suggest a preconditioning, regularization, or
  compensating-term trick (the same shape as leg 58's own SS5 finding — A21 != 0 buys back
  one unit on the kernel direction at a cost elsewhere) that could be adapted computationally,
  even if BDL's own theorem doesn't cover this case directly.
- **The weighted-energy / Chen-Hou lineage** behind legs 65, 111, and 141: leg 111 measured a
  zero-width window (damping needs gamma>3, the weighted space exists only for gamma<3) on
  ONE weighted-energy construction. The same literature consulted for leg 141's novelty check
  was never asked whether it contains a DIFFERENT weighted-energy functional (an added cross
  term, a different Sobolev correction) that could shift either threshold.

Three literature-deep-mine legs are drafted below (**157, 158, 159**) — light-to-standard
difficulty, no compute, gate decidable either way, escalate (don't build) on a YES.

**On GA.** `plan_of_record.py`'s live ban is unambiguous and this DM is not treating the
user's directive as authority to lift it: "any GA compute on an unvalidated fitness... never
[lifts] -- only a re-run of the six-property gate that PASSES on a repaired fitness." That
gate has failed twice (leg 49: 4/6; leg 59: repaired to P2=0.975 but P3 worst |slope-1|
unmoved at 0.342 against the 0.05 floor), and leg 59's own forward-pointer is explicit: "any
future B proposal must change the fitness's DEFINITION, not its wall model" — leg 59 already
tried a wall-model repair (2-D geometry) and it did not move P3 at all. **160 (WVR)** is
drafted below as exactly the leg the coordinator's context describes: it proposes a
genuinely different fitness DEFINITION (not a retry of 46/49/59's linear-defect-tracking
metric), and its gate IS the frozen six-property check — **no GA compute runs on either
branch**, mirroring leg 59's own template exactly. A pass is reported and escalated to the
user as the lift condition being met (the user's call whether to then authorize GA, not this
leg's); a fail banks as the third data point on a dead-as-parameterized fitness family. This
leg does not reopen stage B (which leg 126 closed on the search space, independent of the
fitness) — it answers a narrower, still-open question the user's steer raised: whether a
repaired fitness exists at all, informing (not presupposing) the user's still-pending ruling
on what follows B's exhaustion.

**DM note, 2026-08-06 — novelty/direction review scheduled, PENDING, no findings yet.** Per a
user request forwarded verbatim ("review blog and writeups and assess which things in this
project are genuinely novel... are we pursuing a direction that is worthwhile"), the
orchestrator is dispatching an Opus review agent directly (read-only, surveying `writeup/`,
`experiments/JOURNAL.md`, `PHASE2_P2_NOTES.md`, and this file's own history) — the DM has no
agent-spawning tool, so this is the orchestrator's dispatch, not a leg. **No queue action is
taken here**: this is a placeholder acknowledging the review is in flight so a future DM
spawn (or this same session, resumed) knows to expect its findings and fold them in — cutting
new legs, re-ranking, or escalating anything that would touch a banked claim or the odds
assessment, per the standing rule that a review's own report never moves Clay's ~0.05% by
itself, only what it finds and what a subsequent leg then verifies can. Awaiting the
orchestrator's relay.

**DM response, 2026-08-06 — the review's findings have landed. Acting under the standing
directive; Clay stays ~0.05% (the review itself doesn't move it, per the placeholder above —
nothing here changes that).**

**Coordinator's specific question, answered first: yes, dispatch leg 125.** Re-checked this
file's own history rather than repeating the prior turns' summary. Leg 125 (M2P) was NOT
left parked pending an unresolved ruling — the ruling happened and is recorded in full above
("DM ruling 2026-08-06 — the user has answered open question #2; legality resolved; leg 125
drafted and assigned," with the user's verbatim directive, a six-point legality analysis
concluding the stage-V and gCLM-measurement bans do NOT bind, and a benefit test that passed
disjunctively). It was assigned to LEG-J at that time. **What actually happened is a
bookkeeping gap, not a live block**: every Live-assignments refresh since (the 110-series
table, the 128-series ten-slot table, this DM's own fresh ten-slot dispatch, and the
142–149/150–160 refills) rebuilt the ten-slot table from the undispatched backlog and none of
them carried leg 125 forward into a slot — and this DM's own earlier turns compounded the
gap by citing the *predecessor's* general caution ("check if you can find a ruling; if not,
leave parked") without re-verifying that a ruling had, in fact, already landed by the time of
this DM's first spawn. That was this DM's own error, corrected now: **leg 125 has been ready
and legal since the ruling; nothing has changed that; dispatch it.**

**Action items, disposed:**

1. **Leg 125 — confirmed ready, dispatch.** No new draft needed; the leg is already fully
   specified in the Queue below, unchanged since the ruling. Its own tripwire stands: if its
   work drifts into floating a dissipation parameter against an existing certificate's
   margin, that IS stage V as posed — stop and escalate.
2. **New leg 161 (LSS)**, drafted below: reads Lushnikov-Silantyev-Siegel arXiv:2010.01201 at
   full text (cited 4x in this repo via ALS/Xu as the reference branch for `a_c`, never read
   at primary source) and checks whether its exact `a=1/2` solution accounts for the banked
   `alpha(1/2)=3` finding (currently attributed to ALS eq. 49-50 per PHASE2_P2_NOTES J-3) and
   the `a_c=0.6890665` boundary this repo's own instrument independently measured 0.7% off.
3. **New leg 162 (CAPG)**, drafted below: tests the untried geometric-weight/compact-support
   certificate corner (Chebyshev basis, per HTW arXiv:2603.25104's compact-support result for
   `a=1`) against leg 126's declared-complete search-space audit and leg 58's `A21=0`
   theorem — either it's a real corner leg 126 didn't enumerate, or a clean independent
   confirmation that B's closure is broader than declared. No GA compute; any parameter
   search inside the leg is a deterministic grid, the leg 46/59 precedent, not an
   evolutionary search — the GA ban is untouched either way.
4. **Wind down further adversarial-audit-family drafting — recorded as queue-shaping
   guidance, not a retraction of anything already dispatched or landed.** This DM's own
   128-series-derived refills already said the family's uncovered pool was "nearly empty"
   before drafting 139/140, and the 142–149/150–160 batches have since closed nearly all of
   what remained (nk_seminorm, viscous_novelty, energy_coercivity, literature_gates,
   certificate_shapes, plus five repair legs for the family's own unrepaired findings).
   Guidance for future refills: do not draft a NEW adversarial-audit-family leg on a
   never-before-audited module unless one is flagged by name in a landed leg's own text (the
   leg-76/128 precedent), the way 150–154 were. The reachable, still-genuinely-uncovered pool
   is now essentially: `ga_search.py` (GA lane, banned compute, not auditable without running
   what's banned) and the currently-unreachable red-test/parked modules. Nothing left
   warrants a fresh draft on this DM's own read.
5. **Re-frame (don't withdraw) the two-scale `a*` result — flagged, not drafted as a leg,
   because part of it is outside this DM's or any leg's file scope.** The review's own
   independent check is itself the finding to act on: published literature (arXiv:2603.25104)
   states the two-scale scenario governs `a<=0`, while the banked `a*~0.5-0.55` survival
   boundary was measured at `a>0` — a domain mismatch, not a wrong number. Two distinct
   pieces: (a) `writeup/` and `PHASE2_P2_NOTES.md` scope-line language is in-repo and IS leg
   territory — a leg can and should correct the domain caveat there, on the mechanical-
   correction precedent (leg 65's `capabilities.py` annotation fix), since narrowing a scope
   line to state the domain precisely is not a claim reversal; (b) the user's own
   `MEMORY.md`-format personal memory file (`two-scale-kladder-result.md`, referenced in this
   session's own system context) is OUTSIDE the repo and outside any leg's or this DM's
   file access — recommend the orchestrator relay the corrected framing to the user directly
   for that file, since neither a leg nor this DM can edit it. A dedicated re-framing leg for
   piece (a) is a reasonable next-refill candidate once 161/162 land and inform exactly how
   the caveat should read; not drafted this pass to avoid pre-writing its own conclusion.
6. **Leg 58's publication-scoping bundle (one combined methodological note: exponent-sum
   conservation law + discrete-ball trap + `A21=0` inequality + closure audit) — noted as
   guidance, explicitly deferred, exactly as the coordinator suggested.** This is real
   write-up work, contingent on how 161/162 land (a genuine LSS-explained coincidence or a
   real untried CAP corner would both change what the combined note needs to say), so
   drafting its leg now would risk presupposing an outcome neither 161 nor 162 has reached
   yet. Revisit at the next refill once both report.

**On difficulty and territory for 161/162 (checked against everything currently live):**
161 is literature-only except for an append-only upgrade to `solver/literature_gates.py`'s
existing LSS citation row (from secondary-source to primary-source-read) — no other row
touched, disjoint from 145's read-only ledger audit and from 62/112/113's different papers.
162 needs a NEW solver module (capabilities.py grepped first per the standing ban), disjoint
from 127's `spectral_certificate.py`, 146's `certificate_shapes.py` (read-only reference,
not edited), and every other live/reserve leg's territory.

**DM note, 2026-08-06 — leg 127 (NGX) has landed, gate YES-(i), UNVERIFIED — a full-treatment
verifier is in flight; nothing here treats this as settled.** Reported claim, stated exactly
as the coordinator reported it and no more strongly: a one-direction argument (not the
pre-registered two-direction one, which failed, giving only a vacuous `Z_1 >= 0.068`) proved
`Z_1 >= 1` for EVERY bounded approximate inverse `A` (A21 free) at every `s < 1` on the
bordered `a=0` CLM linearization — superseding leg 58's narrower `A21=0`-only theorem as the
sharpest possible form of the no-go in this space. Separately, leg 127 cites Xu
arXiv:2607.19762 (post-dates leg 58) as proving the SAME operator invertible on a DIFFERENT
space (origin-H², spectral gap 1/2) — which would mean this repository's ~70-leg obstruction
is a property of the `ell^1_w` certificate machinery's chosen space, not the operator itself.
**Both claims are exactly what the verifier is checking (the proof, the numerics, and the Xu
citation specifically) before this DM treats either as banked.** Per the coordinator's
instruction, nothing is drafted here that presupposes verification. Two things are recorded
now, not acted on:

- **This reframes what leg 157 (CDX) was for.** 157 was drafted to surface a literature-
  sourced construction candidate for leg 127's then-open counterexample search. If leg 127's
  proof holds, there is no longer a counterexample to search for on THIS space — 157's Cadiot
  read would need reframing (still worth doing for its own sake — Cadiot's construction is
  still unread for anything beyond leg 62's narrow coverage question — but not as "feeding
  127," since 127 would already be closed in the strongest possible form). Not editing 157
  now; flagging for the next refresh once the verifier reports, per the coordinator's own
  "hold off" instruction and their own statement that scope-line propagation is pointer-block
  work they'll handle post-verification.
- **A speculative next-question leg is drafted below (163), explicitly NOT dispatchable
  until the leg 127 verifier confirms both the proof and the Xu citation.** This satisfies
  the coordinator's ask to "start thinking about what a build-a-certificate-in-origin-H²
  leg would need" without presupposing anything — its own thesis states the contingency in
  its first line, its gate is a SCOPING question (does the space admit the same three
  degrees of freedom a certificate needs, and is there a known obstruction analogous to
  `ell^1_w`'s), not a certificate construction attempt, and its Independence field names the
  exact block. If the verifier does not confirm, this leg is simply never dispatched and
  costs nothing.

**DM update, 2026-08-06 — leg 127's verifier has CONFIRMED. Leg 163 (H2S) is unblocked and
now fully specified as immediately dispatchable — no further drafting needed, dispatch it
directly.** The verifier independently re-derived leg 127's proof and re-computed its
numerics from scratch (banked JSON matches digit-for-digit; local slopes converge
monotonically to `1-s` out to `M=4096`), and confirmed the Xu arXiv:2607.19762 citation is
real and does prove the same operator invertible on origin-H² (spectral gap 1/2 after
modulation). Territory is clean, zero deletions, figures rebuild byte-identically. One
narrow, unrelated gap — a wrong claim that a singular sequence's far-field-amplitude
component is exactly zero (it is actually 6.5% of the norm, growing with `M`) — is being
corrected by a bench-repair outside the leg system, does not touch the theorem (the verifier
separately confirmed bordered/unbordered `sigma_min` agree to 5.7e-15), and does not block
leg 163 (checked explicitly in its own Independence field above: the repair touches
`writeup/` prose only, not `solver/spectral_certificate.py` or Xu's citation). **Leg 163's
own text has been updated in place** (its header, thesis, and Independence field) to record
the confirmation rather than the prior contingency — no new leg number consumed, since it was
already fully specified and only its blocking condition has changed.

Scope-line propagation across banked prose (leg 58's `A21=0` restriction now superseded by
127's stronger theorem; leg 54's "measured not proved" framing likewise superseded) stays the
orchestrator's pointer-block work, as they stated — not touched here. Leg 157 (CDX, the
Cadiot deep-mine) still needs its framing note updated to stop describing itself as feeding
leg 127's now-closed counterexample search; flagged again, not yet edited, since it does not
block anything and a full pass over every downstream reference is better done once alongside
the orchestrator's own propagation pass than piecemeal here.

**DM update, 2026-08-06 — reserve refresh (only 5 of 10 slots live: 118, 153, 154, 160, 163)
PLUS a user steer to weight this batch toward Clay/novelty over hygiene. Both addressed
together, since they're the same decision.**

**On the steer, stated plainly per the coordinator's own caution, so no leg below implies
otherwise.** Toward Clay: the odds ceiling is structural (Wall 2, ~0.05%) and no leg in this
queue, old or new, has moved a link of the L1→L4 chain in 160+ legs — that does not change
today, and nothing drafted below claims it does. What CAN move under this DM's control is
which mathematically substantive threads get worked next versus which hygiene backlog does,
and that is exactly where this refresh leans. Toward novel world-helping maths: the
coordinator is right that leg 127's reframing (the obstruction is the certificate SPACE, not
the operator) and leg 162's ambiguous `Z_1<1` corner are the two most substantive open
mathematical threads on the board right now, both genuinely novel-shaped, and leg 163 is
already running on the first. **This batch prioritizes three follow-up threads on those two
findings ahead of every hygiene item**, then fills remaining slots with the bounded
repair/regression backlog the coordinator's operational message also asked for, then the
oldest never-dispatched reserve at the bottom.

**Tier 1 — Clay/novelty-thread follow-ups (drafted below, top priority):**
- **164 (CSD)**, drafted per the coordinator's own invitation: resolves leg 162's ambiguity
  independently, without needing the user, by answering the definitional question underneath
  it — does the `a=0` CLM linearization admit a compact-support representation AT ALL. This
  could close the "genuine gap vs. structurally inapplicable corner" question on its own.
- **165 (SDM)**, new: leg 127 demonstrated that "the operator is bad" and "this space is bad
  for the operator" are genuinely different claims, retroactively reopening a question about
  every OTHER realization this repository has called dead — legs 52 (space), 53 (split), 56
  (collocation L1 death), 111/141 (weighted-energy). Classify each against the same
  space-vs-operator distinction 127 just proved matters, using only banked data (no new
  compute of dynamics) — a genuinely novel synthesis question, not a repeat of any landed
  audit.
- **171 (XUL)**, new: Xu arXiv:2607.19762 has so far only been mined for the single
  origin-H² invertibility citation legs 127/163 use. Full-text deep-mine for whether Xu
  characterizes any OTHER space's certificate-buildability (not just invertibility) for this
  operator class — directly extends the same thread leg 163 is scoping.

**Tier 2 — bounded repair/regression backlog (the coordinator's operational ask; closes
loops, does not open new ones):**
- **148 (SUB) is now unblocked** — leg 129 (SUR) has landed, clearing the block stated in
  148's own Independence field. No redraft needed; flagging for immediate dispatch, already
  fully specified above.
- **166 (CNB), 167 (DCB), 168 (HRB)**, new: postrepair regression checks for legs 150, 151,
  152 (`collocation_newton.py`, `decay_collocation.py`, `hl_rescaled.py`), all three of which
  landed their repairs without a close-the-loop regression leg yet, per the same
  86/87/94/103/104/105/131–135/147 pattern.
- **169 (HHB), 170 (CDB)**, new, drafted now and blocked: the same regression-check pattern
  for legs 153 (HHR, `hilbert_holder.py`) and 154 (CDR, `critical_dissipation.py`), both
  still in flight — ready the moment each lands.

**Tier 3 — oldest never-dispatched reserve, recovered not redrafted, lowest priority this
refresh:** **109 (RCA, `reduced_certificate.py` audit)** and **110 (L1R, L1 death-certificate
reproduction audit)** — both still fully specified from the 110-series batch, never
dispatched, confirmed via `git log` (no commits for either). Recovered rather than dropped,
but explicitly ranked below every Tier 1/2 item this refresh, consistent with the steer.
**Leg 76 (MI, the Morse-index rework leg) is NOT recovered** — it is the oldest undispatched
entry in the file, predates nearly everything now banked about the space-vs-operator
question, and reviving it would run directly against the steer's direction; if it is still
relevant it can be redrafted fresh against current banked state, not resurrected as-is.

**Total added to reserve this refresh: 11** (three Tier-1 novel-math threads — 164, 165,
171; five Tier-2 repair/regression legs — 166–170, plus 148 unblocked with no new number
consumed; two Tier-3 recovered legs — 109, 110). Recommended dispatch order: **164, 165, 171,
148, 166, 167, 168, then 109/110/169/170 as slots and blocks allow.**

Territory checked explicitly: 164/165/171 are literature-plus-analysis with no new solver
module (164 reads the existing `a=0` CLM profile-equation code, whichever module defines it,
read-only; 165 reads banked JSONs only; 171 is literature-only) — none collides with 163's
`spectral_certificate.py` read-only access or with each other. 166/167/168/169/170 each own a
single already-repaired solver module exclusively (`collocation_newton.py`,
`decay_collocation.py`, `hl_rescaled.py`, `hilbert_holder.py`, `critical_dissipation.py`),
read-only, no overlap with each other or with 109/110's territory.

**DM answer, 2026-08-06 — user question, forwarded verbatim: "is there any way we can combat
Wall 2?" Answered honestly under the standing directive. Per the coordinator's explicit
instruction, this does NOT reword the ~0.05% odds or claim any movement toward Clay — the
odds ceiling stays structural regardless of the answer below.**

1. **Is Wall 2 a property of this repository's approach, or of the field?** Honest answer,
   with the confidence level stated: this DM's working assessment, based on general knowledge
   of the computer-assisted-proof/validated-numerics literature and on this repository's own
   repeated literature passes, is that **no rigorous computer-assisted blow-up certificate is
   known to exist for any genuinely 3D PDE model** — the technique's known reach stops at
   1D/2D (Chen-Hou, Buckmaster-Gómez-Serrano, and this repository's own CLM/gCLM/Boussinesq
   work all sit inside that boundary). But this DM does **not** hold that with full
   confidence, for a specific reason: this repository's own literature legs that touch this
   territory (74, 77, 82, 90, 93, 123) all scoped their search to "has THIS repository's
   specific target object been certified," which is narrower than "has the TECHNIQUE ever
   reached ANY genuinely 3D object, in ANY field" — celestial mechanics, combustion,
   climate-model computer-assisted-proof traditions have never been surveyed by a landed leg.
   Per the coordinator's own suggestion, **leg 172 (W2L) is drafted above** to close that gap
   properly rather than leave the answer resting on this DM's unverified recollection.
2. **Is there a theoretical path from "certified blow-up on a provable toy model" to
   "something rigorous about 3D NS," without solving 3D NS directly?** Honest assessment:
   **mostly closed, with one specific, narrow exception worth naming precisely.** The
   CLM/gCLM family this repository has spent nearly every leg on is a heuristic 1D MODEL
   inspired by 3D vortex-stretching dynamics (De Gregorio's construction) — it is not derived
   from 3D NS by any exact reduction, so a certified blow-up there says nothing rigorous about
   3D NS beyond analogy and intuition-building, exactly as the roadmap states. **The one
   genuine exception**: 2D Boussinesq (this repository's OWN `solver/boussinesq*.py` object)
   is related to 3D axisymmetric, swirl-free Euler by a standard, EXACT change of variables —
   not an analogy, an equivalence — used in the Hou-Luo and Chen-Hou lines of work this
   repository already cites. A rigorous certified blow-up for 2D Boussinesq would therefore be
   a genuine, non-toy statement about a SYMMETRIC SUBCLASS of 3D Euler solutions — inviscid,
   not the Navier-Stokes Clay asks about, and axisymmetric-swirl-free only, not general data.
   Getting from there to viscous 3D NS would need a separate viscous-perturbation argument
   this repository already found pre-empted for a related question (stage V's closure,
   non-novelty against CGL/arXiv:2410.05480). So: the door is not structurally sealed for the
   Boussinesq/axisymmetric-Euler route specifically, but it opens onto a strictly smaller
   room than Clay (inviscid, symmetric-reduced) — which is exactly why the roadmap frames the
   realistic prize as "novel Tier-3 on a provable model," not Clay itself, and nothing here
   revises that framing.
3. **No reword of the odds, no claim of movement, confirmed.** This answer and leg 172 both
   report on where the field's frontier is; neither is a claim that anything in this
   repository moved a link of the L1→L4 chain. Clay stays ~0.05%.

---

**DM update, 2026-08-06 — user steer, forwarded verbatim, two parts. Both addressed below.**

**Part 1 — "stop doing so much review work, focus Opus on maths."** Received and sharpened
into a standing rule for every future refill, not just this one: **no new adversarial-audit
legs** (the `nk_seminorm`-style silent-corruption hunts — that family is, per this DM's own
prior assessment, already down to `ga_search.py`'s banned lane and the currently-unreachable
red-test/parked modules, so there is little left to draft anyway) **and no new freshness-
audit legs** (JR/IX-style ledger checks) **unless something specific and urgent demands one**
— a landed leg's own text flagging a concrete gap (the leg-76/128/150–154 precedent), not a
cadence trigger. This does NOT retract 166–170 (already-drafted, already in reserve,
closing loops on repairs already built — mechanical verification of found bugs, not new
review-hunting) or 148/109/110 (already fully specified, pre-existing); it governs future
drafting. **166–170/109/110/148 are re-ranked below every math-directed leg in this
refresh's recommended dispatch order**, per the steer's spirit, even though they stay
available.

**Part 2 — three math-directed legs, drafted below (173, 174, 175), light/scoping first per
the user's own instruction, heavier construction legs deferred until each is scoped:**

- **173 (XUM)** scopes Xu arXiv:2607.19762's OWN certification method (uniform large-
  imaginary-part bounds, trace-ideal membership, quadrature-error-in-trace-norm) as a
  genuinely different lane from the `ell^1`-Fourier/radii-polynomial approach this
  repository spent ~70 legs on — distinct from leg 171 (XUL), which only asks whether Xu
  covers OTHER spaces; 173 asks what Xu's METHOD itself would take to mature into a working
  certificate here.
- **174 (VBS)** scopes the viscous-certified-blow-up question precisely, because the
  literature answer is more nuanced than "missing entirely": `arXiv:2410.05480`
  (Dahne-Figueras) already interval-verifies self-similar singular CGL profiles continued in
  a dissipation parameter — re-derived by this repository's own leg 48/Route-V to 1.8e-07 —
  which pre-empted stage V precisely because it may already BE a certified viscous blow-up,
  just not in a fluid/vortex-dynamics-adjacent model. **Leg 125 (M2P) is already this
  repository's live attempt at exactly the user's "missing rung"** — a certified viscous
  blow-up on Chen's γ=2 dissipative gCLM, dispatch-ready per this DM's own prior correction
  — so 174's job is narrower than starting from scratch: (a) confirm precisely whether
  2410.05480 counts as "a viscous certified blow-up in any model" already (a definitional
  question, sharpening rather than presupposing the user's framing), and (b) catalog any
  OTHER candidate viscous fluid-adjacent models with an existing analytic (uncertified)
  blow-up proof, as a fallback list if leg 125 doesn't close.
- **175 (USC)** scopes arXiv:2509.14185 (Wang-Lai-Gomez-Serrano-Buckmaster et al., unstable
  self-similar singularities for IPM and 3D Euler with boundary, CAP-ready precision,
  inviscid, no certificate claimed) — currently in this repository's ledger only as a
  one-line EXCLUSION row in `solver/viscous_novelty.py`/`LITERATURE_CHECK.md`, never read at
  full-text depth for its actual method. **Correction to the coordinator's framing, checked
  directly against `LITERATURE_CHECK.md`: the 1.8e-07/3.0e-06/3.8e-07 re-derivation numbers
  already banked belong to `arXiv:2410.05480` (the CGL branch paper), not to `2509.14185`** —
  2509.14185 has no re-derivation on file yet, so 175's first job is establishing what this
  repository actually knows about it independently, not assuming prior work exists. Gate:
  name precisely what "one model class away" means for THIS object — is it that the same
  CAP-ready numerical technique, applied to a model already amenable to this repository's own
  interval-arithmetic infrastructure (gCLM/CLM/Boussinesq), would let a certificate go
  through, or does the CAP technique itself need independent maturation regardless of model.

**Recommended dispatch order for the coordinator's 5-6 open slots, math-first per Part 1:**
**173, 174, 175, 164, 165, 171, 172**, then (lower priority, still available) **148, 166,
167, 168**, then **109, 110, 169, 170** as blocks clear. 163 stays live/already dispatched.

**DM update, 2026-08-06 — leg 163 (H2S) landed as an escalation, PARKED, `leg/163-h2s-v1`,
NOW IN PROGRESS.md's NEEDS YOU.** Reported outcome, stated exactly as the coordinator gave
it: origin-H² IS structurally viable for a certificate (explicit split, shape, bordered
formulation, no `ell^1_w`-class obstruction, verified against Xu at residual 2.8e-14) — but
everything usable depends on `a=0` exactness, which would only re-derive a closed form Xu
already gives analytically, so nothing transfers to the real (non-`a=0`) target object. This
is a genuine yes/no split, not a clean win: structurally viable in the narrow sense leg 163's
gate asked, but not obviously worth a construction leg, which is exactly why it's escalated
rather than auto-followed-up. **No leg is drafted here that presupposes the user's ruling on
whether a construction attempt is worth it anyway** — same discipline as every other parked
escalation (leg 60/PQ, leg 63/125 before its ruling, leg 162/CAPG). Leg 174 (VBS) is
unaffected — it concerns a structurally different question (viscous blow-up certification,
not origin-H² feasibility) and does not depend on 163's outcome either way.

**Answering the coordinator's question on the 3 open slots directly: yes, three math-content
candidates are ready right now — dispatch 173 (XUM), 174 (VBS), 175 (USC).** These were
drafted in this same DM turn, concurrently with the coordinator's message about the open
slots, so the two crossed rather than this DM having nothing ready. All three are Part-2
math-directed legs (Xu's own certification method as a distinct lane; the viscous-blow-up
"missing rung" sharpened against `arXiv:2410.05480`; `arXiv:2509.14185`'s own stated
obstruction), light/scoping difficulty, no overlap with 164/165/171/172 (already running,
correctly not duplicated) or with each other. No hold-open needed for these three slots.

**DM update, 2026-08-06 — all 10 slots full; continuous-flow batch drafted below; the
requested origin-H² construction leg is 176.** Honest accounting first, per the coordinator's
explicit request: **176 is new and the priority item.** Beyond it, this refresh draws on two
pools — (a) five genuinely NEW math-shaped legs (177–181), each independent of any
in-flight leg's still-unknown outcome, and (b) previously-drafted, still-undispatched reserve
from the last two refills that the coordinator's 10-slot list doesn't mention: **148, 109,
110, 168** are unblocked and immediately dispatchable; **169, 170** stay gated on 153/154.
Genuinely fresh math material is thinning for the reason the coordinator would expect: the
highest-value next moves (deeper 173/174/175 construction attempts, anything building on
165's classification or 174/175's catalogs) cannot be drafted yet without presupposing
outcomes no leg has reported. **Saying so explicitly, as asked**: after this batch, the next
refill likely needs at least one of 164/165/171/172/173/174/175 to report before more
first-class math threads can be drafted honestly — the alternative is padding with hygiene,
which the user's steer says not to do.

- **176 (H2C)**, the requested construction leg: builds the origin-H² certificate leg 163
  scoped, at `a=0`, under the user's explicit authorization despite the known ceiling (no
  transfer to the real non-`a=0` target — this leg's own thesis states that ceiling up front,
  it does not discover or hide it).
- **177 (L1RH)**, new: applies leg 127's own reframing (space vs. operator) to L1's OTHER
  dead realization — the collocation basis (leg 56) — by testing whether a non-`ell^1_w`
  space fixes it the way origin-H² fixed the coefficient basis. Drafted now, blocked on leg
  165's classification report (so it doesn't presuppose which realizations are
  space-dependent), ready the moment 165 lands.
- **178 (WES)**, new: applies the same "try a different space" move to the weighted-energy
  realization's zero-width window (leg 111/141) — a genuinely new construction attempt, not
  a repeat of 141's literature check or 165's data-only classification. Independent of 165;
  does not need to wait.
- **179 (PUB1)**, new: leg 58's publication-scoping bundle (action item #6 from the strategic
  review), deferred until 161 and 162 landed — both have. Bundles the exponent-sum
  conservation law, the discrete-ball trap, the `A21` inequality (now leg 127's sharper
  theorem, not leg 58's narrower one), and leg 126's closure audit into one combined
  methodological note, per the review's own suggested shape.
- **180 (TSR)**, new: the in-repo half of action item #5 (deferred pending 161/162, now
  unblocked) — corrects the two-scale `a*` survival boundary's scope line in `writeup/` and
  `PHASE2_P2_NOTES.md` to state its `a<=0` domain precisely, per the review's own independent
  check. Does NOT touch the user's personal `MEMORY.md` file, which stays outside any leg's
  reach (flagged for the orchestrator to relay directly, as before).
- **181 (MOD)**, new: Xu's origin-H² invertibility holds "with a gap of 1/2 AFTER
  MODULATION" — the modulation technique itself has never been read for what it does or
  whether it's transferable. Scopes it directly and asks whether the same modulation move
  could be tried against anything still alive in the `ell^1_w` line (a definitional/
  literature question, not a new construction attempt).

**Small housekeeping note, not a leg:** leg 157 (CDX)'s framing (describing itself as feeding
leg 127's counterexample search) is still stale now that 127 proved the sharpest possible
theorem; flagged twice already, still not worth a dedicated leg on its own — folding the
correction into 179's bundle write-up is cheaper than a standalone fix.

**DM update, 2026-08-06 — one leg drafted for the last open slot (182); one honest gap
flagged.** The coordinator reports 173/174/175 landed with substantive answers relayed
directly to the user, and 179's bundle landed flagging a leg-162-vs-126 ambiguity for the
user's ruling — but **this DM has not been given the actual content of 173/174/175's
findings**, only that they landed. Drafting a leg that specifically "builds on" unknown
findings would mean guessing at their content, which this DM won't do — that's the honest
gap, stated as asked. What follows instead is grounded only in facts already known to this DM
directly (legs 127's and 163's own landed reports, both fully read in earlier turns), so it
does not risk presupposing anything from 173/174/175:

- **182 (H2I)**, new: leg 127 proved `ell^1_w` dead (unconditionally, `Z_1 >= 1` for every
  bounded `A`); leg 163 found origin-H² structurally viable but capped at `a=0` exactness,
  re-deriving Xu's own closed form with no transfer to the real target — leg 176 (in flight)
  is testing whether that viable-but-capped space actually closes as a construction. Neither
  space has been asked the natural next question: is there an INTERMEDIATE space —
  interpolating between `ell^1_w` and origin-H² on some standard scale (weighted Sobolev,
  Besov, or fractional) — that could avoid BOTH obstructions at once: no `ell^1_w`-class
  zero-diagonal floor, AND no collapse to requiring `a=0` exactness the way origin-H² does?
  This is a genuinely new question, not contingent on 173/174/175/176's still-unknown
  outcomes, and it is exactly the shape of move 127 itself validated (test a different space
  against the same operator) applied to the one gap between this repository's two now-mapped
  points on the space axis.

If the coordinator would rather have 173/174/175's actual findings summarized to this DM
before drafting further in that specific direction, that's a cheap, worthwhile handoff for
the next refill — this DM can fold them in properly rather than working around the gap again.

**DM response, 2026-08-06 — user message addressed directly to the DM, forwarded verbatim by
the coordinator: an external novelty review's four findings. Acted on all four below.**

**Item 1 — Xu §8, blocking, top priority. Leg 183 (XU8) drafted above.** Leg 171 (XUL) found,
but did not resolve, that Xu §8 carries its own interval-arithmetic no-go ("no weighted
enclosure can exclude them") on the same operator Theorem NGX (leg 127) concerns, and it is
banked nowhere. **Leg 179's combined methods-note bundle is downgraded to PROVISIONAL as of
this update** — it landed before this review's point was raised, bundles Theorem NGX as a
component of the publishable claim, and per the user's explicit instruction ("nothing should
be drafted [about the note] until this answers"), it must not be presented to the user as
"ready for review" until leg 183 reports. If 183 finds full or partial pre-emption, leg 179's
prose needs a follow-up correction leg (not drafted yet — would presuppose 183's outcome).

**Item 2 — the GA ban's gameable lift condition. Leg 184 (GBW) drafted above.** Leg 160
measured that the unrepaired leg-49 fitness passes the frozen six-property gate 6/6 at a
coarser resolution (n=101/151) where it fails at every resolution that exposed the original
problem — a real loophole in the lift condition's wording ("passes on a repaired fitness,"
no resolution floor), correctly not exploited by leg 160 itself. 184 pins the resolution (or
requires stability across a pre-named minimum resolution set) in `plan_of_record.py`'s ban
text — **this tightens the ban, it does not lift or loosen it**, so this DM is treating it as
within a leg's own authority to land directly (narrowly scoped, one clause, same discipline
as leg 65's annotation fix), rather than requiring separate user sign-off the way lifting a
ban would. If the coordinator or user reads this differently, 184's own no-branch escalates
rather than lands a broader edit, so the exposure is bounded either way.

**Item 3 — leg-111-v2 already exists as leg 178 (WES), confirmed, no new leg drafted.**
Per the coordinator's own note, leg 178 (currently live) is exactly the construction this
review asks for. Recorded explicitly, binding on every leg and writeup pass from here:
**no document may state the weighted-energy lane is dead until leg 178 reports.** The
review's own relayed content from leg 165 (111/141 classified TIER 1: the zero-width window
is a trial-space property, width 2.0 at p=2, with "EGM" cited as certifying a −1/2 gap) is
recorded here as REPORTED, not independently re-verified by this DM — "EGM" does not appear
in `solver/literature_gates.py` or anywhere else this DM has checked, so it is likely a
citation leg 165 itself located and banked; if leg 178's own construction needs EGM's exact
identity, that is 178's own work to locate precisely, not asserted here secondhand.

**Item 4 — math-over-review rule stands, no action needed.** Already governing every refill
since it was adopted; this update's own priority order (183, then 184, both directly
user-flagged; 178 already live and not duplicated) is consistent with it.

**Recommended dispatch order, this update:** **183 (top priority, blocking), 184, 182**, then
whatever remains from the previous refill's pool (176, 177, 178 all already live).

**DM update, 2026-08-06 — leg 184 (GBW) landed clean (`8a2cf6f`): the GA ban's lift
condition now pins the frozen resolution and explicitly excludes leg 160's coarsening
loophole. Ban stays fully in force; item 2 of the external review is closed.** One slot
open; one new candidate drafted below, found by checking this repository's own git history
directly for leg 125's actual landed outcome (not previously relayed to this DM in detail):

**185 (M2SD)**, new: leg 125 (M2P) landed gate **NO on both clauses** — Chen's γ=2 profile
turned out to be the INVISCID closed form (Chen's own text: "we study the inviscid problem,
i.e. ν=0"), so there was no dissipative profile to certify; separately, "Object B" (the
viscous steady state that WOULD have to exist for a genuine dissipative certificate) **stalls
under Newton continuation** at residual 2.65-3.75 with `c_l` running to −10.7, rather than
converging or cleanly diverging. That stall has never been diagnosed — is it genuine
non-existence (no viscous γ=2 steady state exists, strengthening the "missing rung" framing
leg 174 is independently cataloging alternatives for) or a solver artifact (bad initial
guess, a parametrization singularity, insufficient continuation depth)? This is grounded
entirely in leg 125's own already-landed report, not contingent on any in-flight leg's
unknown content, and it is a genuine open diagnostic question this repository has not asked.

**Honest accounting, as asked**: this is the one new candidate this DM found this pass by
actually re-deriving ground truth (checking `git log` directly) rather than working from
memory of what's already drafted. Everything else immediately adjacent — further Xu mining,
further space-axis points, further viscous-model cataloging — is already covered by a live
or provisional leg (171/173/181/183 on Xu; 182 on the interpolation space; 174/178 on
viscous/weighted-energy alternatives) and drafting more there now would mean presupposing
their still-unknown outcomes. If the coordinator wants a second candidate to fully use the
open slot, the honest fallback is one of the still-available lower-priority reserve items
from earlier refills (148, 109, 168, 179's eventual correction leg once 183 lands) rather
than a fabricated new math thread.

**DM update, 2026-08-06 — two significant landings recorded; checked `git log` again for
anything fresh beyond what the coordinator relayed; found nothing new this pass, said
honestly rather than padded.**

- **Leg 164 (CSD) resolved leg 162's ambiguity independently, no user ruling needed.** The
  `a=0` CLM linearization admits NO invariant compact-support representation — a
  Luzin-Privalov uniqueness argument, 14 orders of magnitude of positive control. Leg 126's
  completeness claim stands as scoped; leg 162's corner is confirmed a genuinely different
  object, not a reversal of anything banked. PROGRESS.md item 0 closed.
- **Leg 183 (XU8) answered NOT AT ALL** — Xu §8's no-go does not overlap Theorem NGX (leg
  127) on 5 independently-checked disjointness axes. **Leg 179's publication bundle is now
  CONFIRMED, not provisional** — ready for the user's review, no outstanding blocker. The
  external review's item 1 is closed, alongside item 2 (leg 184, already recorded above).
  Item 3 (leg 178) stays in flight; item 4 stands confirmed with no action needed. Of the
  four items, only 3 is still open.

**On the one open slot: no new candidate found this pass, said explicitly rather than
forced.** Re-checked `git log` for anything landed beyond leg 185 that might open fresh
ground the way leg 125's stall did last time — nothing has landed since. Leg 164's own
technique (a Luzin-Privalov uniqueness argument establishing non-invariance) is genuinely
new machinery this repository hasn't used before, but every place it might obviously apply
next (the interpolation-space question, leg 182; the collocation-basis space test, leg 177)
is already a live or reserve leg whose own construction may or may not need this technique —
drafting a leg presupposing that it does would be presupposing those legs' still-unknown
paths, not extending known ground the way leg 185 did. **Recommend holding the slot**, or
filling it from the existing lower-priority pool (148, 109, 168's sibling regression
closures, or a leg-179-adjacent housekeeping item once the user has reviewed the now-
confirmed bundle) rather than manufacturing new math-shaped content this turn.

**DM update, 2026-08-06 — leg 109 (RCA) landed (3 silent-corruption sites in
`reduced_certificate.py`, bench-repair dispatched); checked `git log` against every number
this DM has drafted rather than re-answer from memory. Found two already-specified,
newly-unblocked legs — no fresh drafting needed for the open slot.**

`git log` confirms **153 and 154 have both landed**, which unblocks the two postrepair
regression legs drafted for exactly this moment: **169 (HHB)**, closing the loop on leg 153's
`hilbert_holder.py` repair, and **170 (CDB)**, closing the loop on leg 154's
`critical_dissipation.py` repair — both fully specified already, both now dispatchable, no
edits needed to either. **148 (SUB)** does not appear in `git log` as landed either, so it
remains available too, unless the coordinator has it in flight outside this DM's visibility.
168 is confirmed in flight (dispatched, not yet landed) per the coordinator's own report,
consistent with `git log` showing no leg-168 commit yet.

**Answering directly: the pool is 169, 170, and 148 — pick any one for the open slot; no new
draft required this turn.** If the coordinator would rather this DM stop tracking the
mechanical-closure pool explicitly and just say "reserve is technically nonzero, check the
Independence field of anything blocked on a leg that's since landed" going forward, that's a
fine simplification — the pattern is mechanical (a repair lands, its regression-check leg
unblocks) and doesn't need this DM to re-derive it by hand each time if the coordinator's own
tracking already catches it.

**DM update, 2026-08-06 — legs 167 and 182 landed clean; the space-axis investigation is now
fully closed. One new candidate drafted below (186); `git log` re-checked, nothing else new
has landed.**

**182 (H2I) answered NO**: no interpolating space between `ell^1_w` and origin-H² avoids
both obstructions. Combined with what was already banked, the space axis now has three
resolved points, forming a complete, coherent result: `ell^1_w` is dead unconditionally (leg
127), origin-H² is structurally viable but capped at `a=0` exactness with no transfer to the
real target (leg 163), and no intermediate space rescues either (leg 182). This is exactly
the shape of finding leg 179's bundle already demonstrated is worth writing up coherently
rather than leaving scattered across three leg reports — and unlike a hygiene item, it is
synthesizing genuinely new mathematical content (163 and 182 both postdate 179's bundle), so
drafting it is consistent with the math-over-review steer, not in tension with it.

- **186 (PUB2)**, new: bundles the space-axis closure (127, 163, 182) into one coherent
  methodological note, on the same precedent as leg 179 — states the three results together,
  with leg 163's known ceiling and leg 182's negative result both stated exactly as landed,
  no softening or strengthening either. Flags explicitly, per this repository's own
  discipline: this bundle is a NEW, separate note from leg 179's (which bundles the no-go
  family: exponent-sum, discrete-ball trap, the `A21` inequality, closure audit) — the two
  should not be merged into one document without the user's own editorial call, since they
  answer different questions (why the method fails vs. where else it might live).

**Honest accounting**: this is grounded entirely in already-landed results (127, 163, 182,
and the leg 179 precedent for how to bundle them), not a presupposition of anything still in
flight. `git log` shows nothing new beyond leg 185 has landed since the last check, so no
other fresh math-shaped thread was found this pass.

**DM update, 2026-08-06 — 4 open slots (live: 176, 177, 178, 185, 169, 186). Leg 166 found
leg 150's repair incomplete (a structural predicate limitation lets one case still slip
through; bench-repair dispatched outside the leg system) and leg 109's bench-repair landed,
correcting two stale banked verdict strings it had flagged — both recorded, neither needs a
DM-drafted leg (mechanical, already handled). Filling the 4 slots: two already-specified
reserve items, one genuinely new construction candidate, and one honest gap.**

- **170 (CDB)** — still available; `git log` confirms it has not landed, and the coordinator's
  live-legs list doesn't include it either, so it appears to have been passed over rather
  than dispatched. Already fully specified (postrepair regression check for leg 154's
  `critical_dissipation.py` repair), no redraft needed.
- **148 (SUB)** — still available on the same basis, already fully specified.
- **187 (M2CI)**, new: leg 125's own landed numbers contain an unexploited lead. "Object A"
  (Chen's actual profile — the INVISCID γ=2 closed form) measured UNDER the radii-polynomial
  budget at all 9 tested rows (`Y_0`/budget 1.325e-09 .. 5.800e-05) — comfortably inside
  certificate range. Chen's own proof of this profile's blow-up is analytic, not
  computer-assisted. If a full certificate closes on Object A, that would be a genuinely
  novel result independent of the viscous "missing rung" question this cycle has otherwise
  focused on: the first computer-assisted certificate of Chen's specific γ=2 profile,
  upgrading an analytic proof to CAP status — the same shape of achievement as Chen-Hou's own
  work, applied to a different object nobody has certified yet (leg 125's own novelty pass
  found none in the searched literature). **Flagged honestly: this is NOT the viscous rung
  the user's earlier steer asked about** — Object A is inviscid — but it is a fully grounded,
  high-value, genuinely fresh construction lead sitting unused in already-banked numbers.
  Drafted below.
- **Fourth slot: genuinely nothing else found this pass, said honestly.** Every other
  immediately-adjacent thread (further Xu mining, further viscous-model cataloging, anything
  building on 174/175/178's still-unknown outcomes) would mean presupposing an in-flight
  leg's result. Recommend holding the fourth slot, or using it for leg 166's own close-the-
  loop regression check once its bench-repair lands (not yet — premature to draft).

**DM correction, 2026-08-06 — leg 148 is STILL BLOCKED; this DM's own earlier "148 available"
claim was wrong, and the underlying method is now flagged as unreliable going forward.** The
coordinator confirmed via `git log --grep "^Leg 129:" ` on `origin/main`: zero hits. Checked
directly in this session: `git log --oneline --all` (which this DM had been using to build
its "landed leg numbers" list) **includes commits reachable from every local branch, not
just `main`** — and leg 129 has real commits, just all on the still-parked
`leg/129-sur-v1` branch (confirmed via `git branch --no-merged main`, which lists it
explicitly), never merged. Leg 129 (SUR) is parked as **escalation #4**: its repair correctly
moves the minimum admissible Boussinesq grid `n>=3` to `n>=4` per a strict Bowman 2/3
dealiasing rule, which flips ONE of leg 133's 90 banked battery verdicts (family
`E_degenerate_discretization`, raised 13/benign 3 -> raised 14/benign 2) — parked because a
repair that flips a banked verdict needs the user's ruling, per this repository's standing
discipline, not because anything about the repair itself is in doubt. **148 (SUB) stays
blocked until either that ruling lands or someone re-verifies 129 actually merged — do not
route it back to the coordinator until then.** Going forward, this DM will treat the
coordinator's own explicit landing reports as authoritative over its own `git log --all`
checks, and will caveat any self-derived check explicitly as unverified rather than assert it
as fact, exactly the mistake made here.

**Two more genuinely fresh candidates, drafted below, both grounded in already-recorded
reasoning (legs 129's and 64/161's own text) rather than presupposing any in-flight leg:**

- **188 (SURV)**, new: leg 129's own parked branch already contains the reasoning for its
  `n>=3` to `n>=4` floor correction — it follows from applying a strict Bowman 2/3
  dealiasing rule (already cited and used elsewhere in this repository, e.g. leg 120's own
  repair) to the `n=3` grid specifically. If that derivation is genuinely NECESSARY (the
  strict rule leaves no other admissible reading) rather than a judgment call, this
  escalation might be independently resolvable without the user's ruling — the same shape of
  move leg 164 made for leg 162's ambiguity. Reads leg 129's own parked-branch commits
  directly (reading a parked branch is not the same as merging it) to check this precisely.
- **189 (XUTRI)**, new: this repository has two independent derivations of `a_c=0.6890665`
  and `alpha(1/2)=3` (ALS's direct integration, re-derived by this repository to 7.7e-5/1.4e-4
  precision, and this repository's own instrument, "the worst of three sources" per
  PHASE2_P2_NOTES J-8) — but Xu's own spectral-picture framework (already extensively read
  for the origin-H² and §8 questions, legs 127/163/171/173/181/183) has never been checked
  for whether it independently reproduces either constant. A third, structurally different
  derivation would either triangulate confidence in both numbers or locate a genuine
  discrepancy this repository's "worst of three sources" framing has not yet explained.

**DM update, 2026-08-06 — legs 177 and 186 landed clean; five new candidates drafted below to
refill the queue, checked against `origin/main` (not `--all`, per the corrected methodology)
before drafting anything.** `git log origin/main --grep "^Leg 1[7-9][0-9]:"` confirms 171–177,
179–186 have real commits on `main`; 178, 187, 188, 189, 190 do not yet (consistent with the
coordinator's report that 187/188/189 are running and 178 is still in flight). Five
candidates, all grounded in already-known facts, none presupposing an in-flight leg's
unknown content:

- **190 (EGML)**, new: the "EGM" citation, relayed twice now (the external novelty review and
  leg 165's own classification, "certifies a −1/2 gap" at `p=2` for the weighted-energy
  window) has never been independently located or banked in `solver/literature_gates.py` —
  it does not appear anywhere in this repository's own ledger. Locate and verify its exact
  identity (full arXiv number, authors, precise claim and hypotheses) before leg 178's own
  construction work needs it secondhand.
- **191 (PQV)**, new: leg 60 (PQ) is parked as escalation #4 on two unreproducible numbers
  (v2's "28x worse" claim reproduces at 63x; v1's `rho=8` reach-table row quotes a different
  resolution's value) — parked because a ban resting on a wrong number is the user's call.
  Independent of that ruling, there is a decidable math question: does substituting the
  CORRECTED, reproducible numbers change any conclusion this repository has drawn from
  Route-PORT v1/v2's results? If the qualitative conclusions are robust to the correction,
  that is useful information for the user's ruling without presupposing it.
- **192, 193, 194**, new, drafted now and blocked until their respective source leg lands:
  independent post-construction verification for the three certificate-construction legs
  this cycle has built — **192** for leg 176 (origin-H² at `a=0`), **193** for leg 187
  (Chen's inviscid γ=2 profile), **194** for leg 178 (weighted-energy v2, once it lands). This
  extends the SAME discipline this repository already applies to every repair
  (86/87/94/103/104/105/131–135/147/166–170) to NEW constructions making certificate claims
  for the first time — arguably more important than a repair check, since these claim
  genuinely novel positive results, not just non-regression. This is not a fresh audit hunt;
  it is the established postrepair-verification pattern applied one level up.

**DM correction, 2026-08-06 — leg 191 (PQV) had a stale premise; withdrawn and redrafted.
Second stale-premise instance this session (after leg 148); spot-check performed below on
every currently-blocked reserve item, as the coordinator suggested.** Leg 60 (PQ) is NOT
parked — it landed long ago at `e0eba8e`: "landed by orchestrator, user-approved correction,"
all three discrepancies corrected (28x->63x mislabeled baseline, a transcription slip, a
rounding fix), both ban-bearing numbers confirmed exact before and after, both scripts CLEAN
114/114. **Leg 191 as drafted (asking whether the correction changes any conclusion, framed
as informing a still-open ruling) is void — the ruling already happened and the correction
already landed.** Withdrawn; redrafted below as **195**, on the coordinator's own suggested
shape: independent verification that the LANDED correction is accurate, not a question about
whether to make it.

**Spot-check of every leg this DM has referenced as "blocked pending X" or "still parked,"
against `git log origin/main` directly (not `--all`), before more get relayed:**
- **129 (SUR)**: confirmed still absent from `origin/main` — genuinely parked, as before.
- **176, 178** (feeding blocked legs 192, 194): **176 has landed** — gate YES on both
  conjuncts, "the origin-H² certificate at `a=0`, BUILT," with one magnitude flagged NO in
  the same breath (leg 192's own re-verification should check that caveat specifically, not
  just the headline YES). **178 has NOT landed** — 194 stays correctly blocked.
- **187** (feeding blocked leg 193): not found in this check — stays correctly blocked.
- **174, 175**: both landed, with real findings this DM had not seen until this check (see
  below) — neither was referenced as blocking anything, so no prior claim was stale here, but
  their content changes what's worth drafting next.

**174 (VBS) landed with the single most consequential finding of this cycle for the "missing
rung" question.** It built an occupancy matrix (fluid vs. non-fluid × Grade A vs. Grade B
certification) and found the **fluid=True/Grade-A cell is EMPTY** — that is the precise,
now-measured shape of "the missing rung," and leg 174's own text says it is empty "for want
of a TARGET, not a method," since the interval-arithmetic Taylor-coefficient technique is
already Grade A on viscous Burgers (`arXiv:2404.04054`). It also located
`arXiv:2208.09445` (3D compressible Navier-Stokes finite-time blow-up, Grade B — the
viscous term is dominated, not enclosed) as a paper absent from the shared
`solver/viscous_novelty.py` ledger despite being read by leg 113. **175 (USC) landed
TECHNIQUE-SPECIFIC**: `arXiv:2509.14185`'s CAP obstruction was one loss-reweighting scheme,
and — the detail worth following up — **the same authors removed it 72 days later**,
meaning a newer version of their work may not carry the same obstruction.

**Three new candidates, all grounded in what was just found, none presupposing 185/187/178's
still-unknown outcomes:**

- **195 (PQVER)**, replacing withdrawn 191: independently re-verify leg 60's already-landed
  correction (114/114 clean claim, both ban-bearing numbers exact) from the banked data
  directly, on the same postrepair-verification precedent as 192–194.
- **196 (USC2)**, new: does the authors' later work (the version that removed
  `arXiv:2509.14185`'s loss-reweighting obstruction, ~72 days on) achieve an actual
  certificate, or does it still stop short for a different reason? Leg 175's own finding
  makes this the obvious next literature question, not a presupposition of it.
- **197 (VNL)**, new: add `arXiv:2208.09445` to `solver/viscous_novelty.py`'s shared
  PRECEDENTS ledger (append-only), per leg 174's own characterization (Grade B, viscous term
  dominated not enclosed) — the same "citation found but not yet shared-ledgered" gap as leg
  190's EGM.

**192 is now unblocked** (leg 176 landed) — flagging for dispatch, no redraft needed, with
the specific note to check leg 176's own "one magnitude says NO" caveat, not just its headline
YES.

---

## THE `NEXT` CALL — recommendation to the orchestrator (OVERTAKEN 2026-08-06: `NG`'s gate
has since ANSWERED YES and the DM ruling in Status supersedes this section — `NG` goes DONE
on `leg/ng-v1`'s merge, `B` goes NEXT, leg 126 (BX) takes the critical-path slot. Preserved
for the record.)

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
| LEG-J | — | reserve/flex — SUPERSEDED: the 103-124 reserve chain listed here has been fully dispatched/landed; current reserve is 127 (NGX, first claim per the NG ruling) plus the 128-series (see the "reserve-drain refill" Status block, which is authoritative for dispatch order) | — | — | — | — |

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
### 58 — ROUTE-NG: THE NO-GO, STATED AS A THEOREM (critical path, stage `NG`) (GATE ANSWERED
YES 2026-08-06 on `leg/ng-v1` at `3f2ee16` — theorem on the class A21 = 0 at every K, every
s < 1; A21 != 0 stays MEASURED ONLY at battery minimum 8.9591. Escalated by the leg, RULED
MERGEABLE AS-IS by the DM — see the DM ruling in Status. Entry preserved for the record.)
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
### 62 — ROUTE-CP: THE CADIOT PRE-EMPTION, SETTLED FROM THE FULL TEXT (LANDED: gate NO at
`59daeaf` — Cadiot does not cover the off-diagonal / zero-diagonal case; NG's novelty claim
is confirmed at full-text depth by a second, independent reading)
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
KNOWN-ANSWER OBJECT (LANDED: gate NO at `41f4ac0` — the THIRD realization dies on the same
object: every admissible weight's coercivity gap is NEGATIVE, converging to -(3-gamma)/2, and
the admissibility/damping window has ZERO width — damping at the origin needs gamma > 3 while
the basis is in L^2_phi only for gamma < 3. gamma = 3's apparent +4e-3 gap collapses like
n^-1 and moves with the quadrature cutoff, i.e. it is an artifact. See capabilities.py's
energy_coercivity.py entry for the banked magnitudes.)
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

```
### 126 — ROUTE-BX: STAGE B, ANSWERED FROM THE BANKED RECORD — THE CLOSURE AUDIT (critical
path, stage `B`; dispatch into LEG-A the moment `leg/ng-v1`'s merge lands and the plan marks
`B` as `NEXT`)
**Thesis.** Stage B ("evolve the certificate -- the function space, the operator split, the
constants") is the last QUEUED stage in the committed sequence, and it can no longer be RUN as
conceived -- only answered. Its GA is banned and the lift condition has now failed twice on the
frozen six-property gate (leg 49: 4/6; leg 59: FAIL with P2 repaired to 0.975 but P3 worst
|slope-1| unmoved at 0.342 against the 0.05 floor -- "Stage B's fitness is dead as
parameterized"). Its three degrees of freedom are each separately dead for this operator: the
SPACE (leg 52), the SPLIT (coupling entry K/2 for every choice, leg 53), and the SHAPE of A --
measured over leg 54's battery (best admissible 8.9591 where < 1 was needed) and now PROVED
impossible on the class A21 = 0 at every K and every s < 1 (leg 58's theorem). The third
realization is dead too (leg 111: every admissible weight's coercivity gap negative, window
width zero). B's own deliverable pre-authorizes the exit this leg takes: "an honest report
that it does not and where the margin runs out." The leg's REAL work -- the part that can
answer either way -- is the COMPLETENESS AUDIT: enumerate B's declared search space against
the banked refutations, clause by clause, and either exhibit an admissible, ban-respecting
corner that no banked result covers, or establish there is none. NO GA compute runs on either
branch (the ban stands; its lift condition is the frozen gate's PASS, which leg 59 did not
produce). No new ell^1-Fourier machinery is built; every number quoted is read from banked
JSONs or recomputed from landed modules read-only. Honest ceiling, pre-committed: closing B is
bookkeeping on a measured negative, not movement on L1->L4; Clay odds stay ~0.05%.
**Gate.** Auditing stage B's full declared search space (space x split x constants/shape,
plus the fitness route) against the banked record (legs 49, 52, 53, 54, 56, 58, 59, 111):
does any admissible, ban-respecting configuration remain that no banked measurement or
theorem covers -- i.e. a corner in which a searched certificate could still close on this
operator?
  yes -> Name the corner precisely, with the banked clause nearest to it and why it escapes.
         B stays NEXT; the follow-up critical-path leg is the measurement of exactly that
         corner (if the corner needs GA compute, its gate is the frozen six-property gate's
         lift condition, which did not pass at leg 59 -- escalate to the user, do not run it).
  no  -> B's own gate ("does the searched certificate beat the hand-tuned one?") answers its
         pre-committed NO in the only sense that matters: nothing in the searchable space
         closes -- the floor is proved >= 1 on A21 = 0, measured 8.9591 at best anywhere, and
         the fitness that would steer a search is dead as parameterized. Write the honest
         report B's deliverable names, quantifying how much of the difficulty was tuning
         versus structure (the structure share is now theorem-grade). The orchestrator applies
         B's pre-committed no-branch and the committed sequence is EXHAUSTED: what enters next
         is escalation #1, for the user, framed by Open question #3 (leading candidate: the
         gamma=2 dissipative certificate route, contingent on leg 125's gate).
**Territory.** experiments/p2_route_bx_v1_stageb.py,
               experiments/p2_route_bx_v1_stageb_evidence.py,
               writeup/4_p2_lottery/BLOG_P2_ROUTEBX_V1.md,
               writeup/4_p2_lottery/TECHNICAL_P2_ROUTEBX_V1.md,
               writeup/data/p2_route_bx_v1_stageb.json,
               writeup/novelty/leg_126.md, experiments/journal/leg_126.md.
               No figure by design (assembly/audit; the Route-D "no measurement, no figure"
               convention) unless the yes-branch measures a corner, in which case fig62.
**Difficulty.** standard
**Independence.** Owns no solver module; reads banked JSONs and landed modules read-only.
Read-set overlaps leg 110's (leg 54/56 data) are read-read and collide with nothing; 110 is
the only live leg near those files and it also never writes them. Touches nothing owned by
114/116/120/125, the repairs in flight, or either parked branch. NOT dispatchable until
`leg/ng-v1` is merged and the plan marks `B` NEXT -- it quotes leg 58's theorem as banked, not
as a branch.
```

```
### 127 — ROUTE-NGX: THE GENERAL CLASS A21 != 0 — PROOF OR COUNTEREXAMPLE (exploration,
reserve; NOT the critical path; not dispatchable before `leg/ng-v1`'s merge lands)
**Thesis.** Leg 58 proved Z_1 >= 1 on A21 = 0 and left the general class exactly where it
honestly is: MEASURED ONLY (battery minimum 8.9591 over seven shapes; MM4c's rank-one
construction kills any column-floor route to a general proof by driving the hhat-column floor
to ~1e-16 at a total-Z_1 cost of 5.7e+05). The open mathematics is the trade-off: leg 58 SS5
measured that A21 != 0 buys back exactly one unit on the kernel direction (0.9451..0.9990,
deficit tracking rho_M at ratio 0.856..0.997), so any A21 that cancels the hhat-column must
feed B h back into the finite block -- the candidate theorem is a TWO-DIRECTION argument
(pair x = (0; h) with the columns A21 populates) showing what it wins on one direction it
pays, with interest, on another. Either that argument closes -- and the no-go becomes a
theorem on EVERY bounded A, the strongest form publication scoping could ask for -- or the
attempt localizes an explicit admissible A with A21 != 0 and Z_1 < 1, which would OVERTURN
the measured no-go and revive the method (leg 54's battery says this needs to beat 8.9591 by
~9x, and MM4c says naive cancellation costs 5 orders of magnitude -- so a counterexample, if
it exists, is structurally clever, not a tweak). Both branches are results; failure to reach
either is also pre-committed. No dynamics run; the object stays the a=0 CLM linearization
with its exactly-zero Y_0 ceiling stated everywhere, as leg 58 states it.
**Gate.** Can the no-go be DECIDED on the full bounded class -- either (i) a proof that
Z_1 >= 1 for every bounded A (A21 free) at some s < 1, with hypotheses containing the a=0 CLM
linearization, or (ii) an explicit admissible A with A21 != 0 and measured Z_1 < 1,
grid-stable over >= 3 resolutions?
  yes, (i)  -> The theorem reaches its sharp form. Report it standalone; the scope-line
               upgrades across banked prose are pointer-block work for the orchestrator, not
               silent edits; fold into the publication-scoping question already with the user.
  yes, (ii) -> The measured no-go is OVERTURNED -- a banked conclusion reverses. That is
               escalation #4 by definition: push the branch, park it, do not merge, list it
               under NEEDS YOU. (It would also be the single best piece of news this
               repository could produce short of leg 125's yes-branch.)
  no        -> Neither the trade-off inequality nor a counterexample within a leg's work. The
               restriction is recorded as fundamental at this machinery's level, with the
               named obstruction (the two-direction argument's failure mode) kept in the
               artifact per lesson 76; the scope line "measured, not proved" for A21 != 0
               stands permanently, and no retry without new machinery.
**Territory.** solver/spectral_certificate.py (append-only additions, sole owner once
               `leg/ng-v1` is merged), test_spectral_certificate.py,
               experiments/p2_route_ngx_v1_general.py,
               experiments/p2_route_ngx_v1_general_evidence.py,
               writeup/4_p2_lottery/BLOG_P2_ROUTENGX_V1.md,
               writeup/4_p2_lottery/TECHNICAL_P2_ROUTENGX_V1.md,
               writeup/data/p2_route_ngx_v1_general.json,
               writeup/figures/fig63_route_ngx_v1_general.png (fig61 is 125's, fig62 is
               reserved for 126's yes-branch),
               writeup/novelty/leg_127.md, experiments/journal/leg_127.md
**Difficulty.** heavy
**Independence.** Sole owner of solver/spectral_certificate.py AFTER leg 58's merge lands
(58's slot is terminated on landing; no other live or reserve leg claims the module). Reads
leg 54's and 58's banked JSONs read-only. No overlap with 114/116/120/125/126, the repairs in
flight, or either parked branch. JSON and figure names pre-checked distinct — no collision.
```

```
### 128 — ROUTE-NKR: SHARED-GUARD REPAIR FOR THE Y0/Z0/Z1 FABRICATION-ACCEPTANCE GAP —
nk_bounds.py PLUS ITS TWO ALREADY-REPAIRED SIBLINGS (RESERVE — NOT dispatchable until leg
105/ICB lands)
**Thesis.** Leg 116 (NKA) found that `nk_bounds.py`'s `budget()` validates only Z2>0, so a
forbidden Z0=-1 turns an honest refusal into a certified ball containing no true zero
(missing by 1.16 ball radii; 21/52 hypothesis-violating inputs false-close) — the THIRD
module with the identical Y0/Z0/Z1 nonnegativity gap, after port_certification.py (leg 79,
repaired) and interval_certificate.py (leg 98, repaired). Leg 116's own landing flagged this
for the DM as a candidate shared-guard repair rather than a third one-off fix, and that is
what this leg is: one shared validation helper (NEW module, capabilities.py grepped first
per the standing ban), wired into all three modules, closing every clause on leg 116's own
repair list — validate Y0, Z0, Z1 >= 0 and finite in `budget`; refuse or flag closes=True
with r_min <= 0; enforce alpha < 2 in `farfield_modelling_error_bound` or flag an argmax_X
on the window boundary (the ~1e8x sup under-report); lower `_I_out`'s bulk floor or bound
the [0, eps] panel; enforce gamma in (0,1]; raise on non-positive off-diagonal q_cod/v_cod.
This is a leg, not a bench-repair, on the leg-76 precedent: multi-file, claim-adjacent
(certifying-bound code), and it must invert leg 116's GAP-PIN gates in the same commit.
**Gate.** Post-repair: (a) do all 21 false-closing cases in leg 116's 52-case battery now
reject, with every GAP-PIN inverted and every HOLDS gate still passing; (b) do
port_certification.py and interval_certificate.py remain bit-identical on clean inputs, with
legs 86's and 105's regression suites passing unchanged; and (c) do all three modules route
hypothesis validation through the one shared guard?
  yes -> The gap class is closed repository-wide, not per-module. Bank leg 116's battery as
         the permanent regression suite; record in capabilities.py (append-only) that the
         three modules share one guard.
  no  -> If any clean-input result moves AT ALL, or any sibling regression suite fails, stop
         and escalate with the exact case — a behavior-changing "repair" of certifying-bound
         code never lands on this leg's own authority.
**Territory.** solver/certificate_guards.py (NEW), solver/nk_bounds.py,
               solver/port_certification.py, solver/interval_certificate.py (wiring only),
               test_nk_bounds_adversarial.py (pin inversions, same commit),
               experiments/p2_route_nkr_v1_repair.py,
               writeup/data/p2_route_nkr_v1_repair.json,
               writeup/novelty/leg_128.md, experiments/journal/leg_128.md
**Difficulty.** standard
**Independence.** NOT dispatchable until leg 105 (ICB) lands — 105 is measuring
interval_certificate.py and this leg edits it. After that, sole owner of all four solver
files; no other 128-series leg (and neither 126/BX nor 127/NGX) touches any of them. Legs
86/105's postrepair test files are run, never edited.
```

```
### 129 — ROUTE-SUR: THE DEALIAS-BOUNDARY REPAIR PASS — spectral_utils.py, boussinesq.py's
IDENTICAL CUT, AND THE TEST THAT ENCODES THE DEFECT (RESERVE — NOT dispatchable until leg
133/BOB lands)
**Thesis.** Leg 120 (SUA) found `dealias_mask` retains one Fourier mode too many whenever
3|n (`<= n/3` where Bowman 2013 requires strict `<`), making the "exact rate"
`energy_production` wrong by 1.66e-01 relative at n=81 vs 2.47e-14 elsewhere — latent only
because every banked grid is a power of two (0 of 107 energy_balance_residual records
exposed). Leg 120 verified the fix (`wavenumbers(n) <= (n-1)//3`) bit-identical at every
resolution the repository has ever run, located the identical `<= n/3` cut in
`boussinesq.py`'s `dealias_mask2d` (line ~149), and found that
`test_spectral_utils_dedicated.py:121-122` ASSERTS the defective behavior ("k = n/3 must be
retained") — so the repair must cover both siblings and invert that assertion in one pass,
which is exactly why leg 120 flagged it for the DM rather than a bench one-off. Scope also
includes leg 120's five silent-absorption defects per its own repair list: `derivative_hat`
multiplies the Nyquist entry by zero rather than assigning (Johnson Alg. 1), `velocity_hat`
builds complex output rather than inheriting dtype, `hilbert_hat`/`derivative_hat` validate
k. The seven PIN gates in test_spectral_utils_adversarial.py invert in the same commit —
that is their designed signal.
**Gate.** Post-repair: (a) are `dealias_mask` and `dealias_mask2d` both strict (k < n/3),
bit-identical at every grid size in the repository's declared set ({64, 256, 512, 1024,
2048, 4096, 8192} and the 2D n=32), with all 107 banked energy_balance_residual records
reproducing exactly; (b) at 3|n does energy_production's error fall from 1.66e-01 to the
2.5e-14 class leg 120's alias-free reference established; and (c) are the five absorption
defects closed with their PINs inverted and every HOLDS gate passing?
  yes -> The latent boundary is closed before anyone ever picks a round grid number. Bank
         leg 120's battery as the permanent regression suite for both modules.
  no  -> If ANY power-of-two-grid quantity changes at all, stop and escalate with the exact
         value — the entire license for this repair is the measured no-op guarantee, and a
         repair that moves a banked number is not this leg's to land.
**Territory.** solver/spectral_utils.py, solver/boussinesq.py (dealias_mask2d only),
               test_spectral_utils_dedicated.py (the two defect-encoding lines),
               test_spectral_utils_adversarial.py (pin inversions, same commit),
               experiments/p2_route_sur_v1_repair.py,
               writeup/data/p2_route_sur_v1_repair.json,
               writeup/novelty/leg_129.md, experiments/journal/leg_129.md
**Difficulty.** standard
**Independence.** NOT dispatchable until leg 133 (BOB) lands — 133 measures boussinesq.py
bitwise and this leg edits it. The bit-identical-at-every-banked-grid guarantee means
in-flight read-only audits of importing modules are unaffected. No other 128-series leg
touches either solver file.
```

```
### 130 — ROUTE-HPR: REPAIR THE ONE UNREPAIRED BOUND-DIRECTION VIOLATION —
hilbert_pointwise.py (RESERVE)
**Thesis.** Leg 106 (HPA) landed gate YES: `hilbert_pointwise.py`'s pointwise |H(h)| bound
fails to dominate the true value on 2 of the tested degenerate/NaN-poisoned configurations —
and, uniquely among this cycle's YES findings, its landing recorded "repair not yet
scheduled." Every other bound-direction violation found this session (op_lower's 47 cases,
nk_bounds' family-1) has a repair landed or a leg drafted; this is the straggler. The repair
follows the op_lower precedent exactly: on the two failing configurations either reject the
input loudly or return a bound that truly dominates — never a sharpened bound (a speedup or
sharpening is a claim change, not a repair) — and prove zero movement everywhere else.
**Gate.** Post-repair: (a) do both of leg 106's failing configurations now either raise or
return a value verified to dominate the true |H(h)| on that configuration; and (b) is the
module bit-identical on every previously-passing case, including its capabilities.py
validated line and every HOLDS gate in leg 106's battery?
  yes -> The bound direction holds under the full battery. Bank it as the permanent
         regression suite; invert leg 106's pins in the same commit.
  no  -> An incomplete fix or a repair regression. Report the exact configuration and
         magnitudes; escalate, do not iterate the repair under this leg's own authority.
**Territory.** solver/hilbert_pointwise.py, test_hilbert_pointwise_adversarial.py (pin
               inversions, same commit), experiments/p2_route_hpr_v1_repair.py,
               writeup/data/p2_route_hpr_v1_repair.json,
               writeup/novelty/leg_130.md, experiments/journal/leg_130.md
**Difficulty.** standard
**Independence.** Sole owner of hilbert_pointwise.py (leg 106 landed and closed; leg 119's
hilbert_holder.py is a different module, checked explicitly). Immediately dispatchable.
```

```
### 131 — ROUTE-HNB: POST-REPAIR REGRESSION CHECK, holder_norms.py (RESERVE)
**Thesis.** Leg 100's bench-repair landed at `fb61a79`: all 7 entry points now reject
NaN/Inf/degenerate input (0 -> 26 raise sites), closing the 6 escalated mechanisms plus a
7th found during repair, self-reporting 14/14 adversarial cases closed and 53/53 clean calls
bit-identical. That is the REPAIR's own report; the 86/87/94/103/104/105 pattern exists
because a repair's self-check is not an independent confirmation. Re-run leg 100's full
original battery and the module's dedicated known-answer tests fresh, from the battery's own
driver, against the repaired module.
**Gate.** Post-repair, does solver/holder_norms.py (a) reject every case in leg 100's
original 6-mechanism battery (no silent corruption remains), and (b) reproduce every
previously-validated clean-call result bit-identically, including the module's dedicated
test file and its capabilities.py validated line?
  yes -> Repair confirmed solid and non-regressive by an independent run. Bank leg 100's
         battery as a permanent regression suite.
  no  -> An incomplete fix or a repair regression. Report the exact case precisely; escalate
         as a priority finding, do not patch under this leg's own authority.
**Territory.** test_holder_norms_postrepair.py, experiments/p2_route_hnb_v1_postrepair.py,
               writeup/data/p2_route_hnb_v1_postrepair.json,
               writeup/novelty/leg_131.md, experiments/journal/leg_131.md
**Difficulty.** standard
**Independence.** Reads solver/holder_norms.py; edits nothing under any outcome. The repair
has landed, so the module is unowned. Immediately dispatchable.
```

```
### 132 — ROUTE-OLB: POST-REPAIR REGRESSION CHECK, op_lower.py (RESERVE)
**Thesis.** Leg 101's bench-repair landed at `147e8c2`: op_lower.py now claims a TRUE lower
bound on all 209 adversarial cases (47 violations -> 0, max L/N_true 1.000604187 ->
1.000000000) via exact power-of-two rescaling plus certified downward deflation, with the
307.878-decade headroom unchanged to every digit. A lower bound that silently stopped being
one was exactly the finding; independently confirm the repair did not overshoot (a deflation
that moves the bound DOWN is admissible, one that moves any validated magnitude is not) by
re-running leg 101's full battery and the module's known-answer line from scratch.
**Gate.** Post-repair, does solver/op_lower.py (a) return a true lower bound (L <= N_true)
on every one of leg 101's 209 original adversarial cases in an independent re-run, and
(b) reproduce the 307.878-decade headroom and every other validated magnitude to the digit?
  yes -> Repair confirmed sound and non-regressive by an independent run. Bank the 209-case
         battery as a permanent regression suite.
  no  -> An incomplete fix or a repair regression. Report the exact case precisely; escalate
         as a priority finding, do not patch under this leg's own authority.
**Territory.** test_op_lower_postrepair.py, experiments/p2_route_olb_v1_postrepair.py,
               writeup/data/p2_route_olb_v1_postrepair.json,
               writeup/novelty/leg_132.md, experiments/journal/leg_132.md
**Difficulty.** standard
**Independence.** Reads solver/op_lower.py; edits nothing under any outcome. The repair has
landed, so the module is unowned. Immediately dispatchable.
```

```
### 133 — ROUTE-BOB: POST-REPAIR REGRESSION CHECK, boussinesq.py (RESERVE)
**Thesis.** Leg 89 (BOA) was the most severe finding of the whole adversarial-audit run — a
false `blowup_candidate` flag triggered by ordinary dealiasing noise amplified 5.6e13x, plus
a silently-dropped kappa parameter and a NaN-masking bug, four defects in all — and its
bench-repair landed with a banked-result audit concluding no Phase-1 number was affected.
It is the only finding of that severity class with NO close-the-loop regression leg: legs
92, 98, 99's comparable findings all got theirs (103/105/104). Re-run leg 89's full original
battery against the repaired module and independently re-confirm the banked-result-audit
conclusion from the banked JSONs, not from the repair's own report.
**Gate.** Post-repair, does solver/boussinesq.py (a) pass leg 89's full original battery —
no false blowup_candidate under dealiasing noise, kappa honored, NaNs propagated or flagged
— and (b) reproduce the banked n=32 Boussinesq results bit-identically, confirming the
repair's no-contamination conclusion independently?
  yes -> Repair confirmed solid and non-regressive; the severest finding of the run is
         fully closed. Bank leg 89's battery as a permanent regression suite.
  no  -> An incomplete fix, a repair regression, or a contamination the repair's own audit
         missed. Report the exact case precisely; escalate as a PRIORITY finding, do not
         patch under this leg's own authority.
**Territory.** test_boussinesq_postrepair.py, experiments/p2_route_bob_v1_postrepair.py,
               writeup/data/p2_route_bob_v1_postrepair.json,
               writeup/novelty/leg_133.md, experiments/journal/leg_133.md
**Difficulty.** standard
**Independence.** Reads solver/boussinesq.py; edits nothing under any outcome. Must land
BEFORE leg 129 (SUR) dispatches, since 129 edits the same module — the DM has sequenced
this explicitly. Immediately dispatchable.
```

```
### 134 — ROUTE-FGB: POST-REPAIR REGRESSION CHECK, fractional_gclm.py (RESERVE)
**Thesis.** Leg 91 (FGA) found fractional_gclm.py silently accepts s<0 and nu<0, returning
a finite p that moves the measured critical exponent s_c by up to +13.3%; the repair landed
(rejection at construction, s_c untouched) but — unlike legs 92/98/99's findings — never got
its close-the-loop regression leg. Re-run leg 91's full adversarial battery against the
repaired module and confirm the banked s_c value bitwise, independently of the repair's own
claim.
**Gate.** Post-repair, does solver/fractional_gclm.py (a) reject every s<0 / nu<0 case in
leg 91's original battery at construction, and (b) reproduce the banked s_c measurement
bit-identically on the validated line?
  yes -> Repair confirmed solid and non-regressive. Bank leg 91's battery as a permanent
         regression suite.
  no  -> An incomplete fix or a repair regression. Report the exact case precisely; escalate
         as a priority finding, do not patch under this leg's own authority.
**Territory.** test_fractional_gclm_postrepair.py,
               experiments/p2_route_fgb_v1_postrepair.py,
               writeup/data/p2_route_fgb_v1_postrepair.json,
               writeup/novelty/leg_134.md, experiments/journal/leg_134.md
**Difficulty.** standard
**Independence.** Reads solver/fractional_gclm.py; edits nothing under any outcome. The
repair has landed, so the module is unowned. Immediately dispatchable.
```

```
### 135 — ROUTE-FIB: POST-REPAIR REGRESSION CHECK, first_integral.py (RESERVE — NOT
dispatchable until the first_integral bench-repair merges)
**Thesis.** Leg 107 (FIA)'s finding is being repaired on
`bench/fix-first-integral-support-extrapolation`, self-reporting 96/96 fabricated values
rejected and zero regression proven bit-for-bit over 860,200 values. When it merges, the
same discipline as 95/103/104/105 applies: independently re-run leg 107's full original
battery and the bit-for-bit regression claim from the battery's own driver, not the repair's
bundled test.
**Gate.** Post-repair, does solver/first_integral.py (a) reject every fabricated value in
leg 107's original battery in an independent re-run, and (b) reproduce the previously-
validated clean results bit-identically, including the long-running gate-4 test?
  yes -> Repair confirmed solid and non-regressive. Bank leg 107's battery as a permanent
         regression suite.
  no  -> An incomplete fix or a repair regression. Report the exact case precisely; escalate
         as a priority finding, do not patch under this leg's own authority.
**Territory.** test_first_integral_postrepair.py,
               experiments/p2_route_fib_v1_postrepair.py,
               writeup/data/p2_route_fib_v1_postrepair.json,
               writeup/novelty/leg_135.md, experiments/journal/leg_135.md
**Difficulty.** standard
**Independence.** Reads solver/first_integral.py; edits nothing under any outcome.
**NOT dispatchable until `bench/fix-first-integral-support-extrapolation` lands** — drafted
now so it is ready immediately after, the same discipline as legs 95/103/104/105.
```

```
### 136 — ROUTE-MF2: THE FIVE DIVERGENT TRAJECTORIES GATE 11 STILL MISSES (RESERVE)
**Thesis.** Leg 83 (MFG) found marginal_flow.py's gate 11 missed 8 of 9 adversarial
divergent trajectories (worst: 4.99e130x state growth at a Newton residual 1.6e-10 of
threshold). The bench-repair's scale-free state-growth threshold closed 4 of the 9 including
the worst, with 0 false positives — a genuine partial fix, correctly not re-escalated — and
5 cases remain open with no characterization of WHY the scale-free criterion misses them.
This leg measures that residual: classify the 5 open cases by mechanism, then test a small
NAMED family of second criteria fixed in the driver before any measurement (per leg 111's
pre-naming discipline — e.g. a windowed growth-rate estimate, a residual-to-state-scale
ratio, a monotone-tail detector), against all 9 original cases, the 11 existing gates, and
the module's well-behaved trajectories.
**Gate.** Does at least one pre-named criterion flag all 5 remaining divergent cases with
zero false positives across the 11 existing gates, the 4 already-closed cases, and the
well-behaved battery?
  yes -> A complete detector exists. Report it with magnitudes and ESCALATE a repair
         proposal (the gate-11 threshold is claim-bearing detector logic — not patched under
         this leg's own authority).
  no  -> The residual gap is characterized, not just counted. Bank the per-case mechanism
         classification and the measured failure of each pre-named criterion as the
         permanent record of gate 11's known limitation; nothing further without new
         information.
**Territory.** experiments/p2_route_mf2_v1_residual.py,
               writeup/data/p2_route_mf2_v1_residual.json,
               writeup/novelty/leg_136.md, experiments/journal/leg_136.md
**Difficulty.** standard
**Independence.** Reads solver/marginal_flow.py (leg 83 landed; module unowned); edits
nothing under any outcome. Disjoint from every repair and audit leg in this batch.
Immediately dispatchable.
```

```
### 137 — ROUTE-JR3: THIRD FRESHNESS AUDIT OF experiments/JOURNAL.md AND journal/ (THE
100-125 WAVE) (RESERVE)
**Thesis.** Leg 72 audited the journal through leg 60's era; leg 102 (JR2) covered legs
73-99. Since then the largest landing wave of the run — the 100-125 series, including two
escalations, multiple bench-repairs, and the user-resolved leg 60 — has gone in at high
throughput, exactly the conditions under which per-leg files go missing (leg 72's founding
finding). Pin the audit window at this leg's own start SHA to avoid racing in-flight
landings: every leg landed on main at that SHA since JR2's window closed, plus confirmation
that JR2's one standing carry-over (leg 60's missing files) closed when leg 60 landed.
**Gate.** At the pinned SHA, does every landed leg since JR2's window have (a) its
experiments/journal/leg_N.md on main, (b) a JOURNAL.md pointer line, and (c) its
writeup/novelty/leg_N.md — with leg 60's former gap confirmed closed?
  yes -> The ledger is complete through the pinned SHA. Bank the dated completeness record.
  no  -> Report the exact missing files per leg (the count IS the finding, per JR1/JR2
         precedent); create nothing on another leg's behalf; escalate only if a missing file
         belongs to a parked escalation (not this leg's to backfill).
**Territory.** experiments/p2_route_jr3_v1_journal_audit.py,
               writeup/data/p2_route_jr3_v1_journal_audit.json,
               writeup/novelty/leg_137.md, experiments/journal/leg_137.md
**Difficulty.** light
**Independence.** Docs-only, read-only on every other leg's files; no solver module.
Disjoint from 138 (different ledger). Immediately dispatchable.
```

```
### 138 — ROUTE-IX3: THIRD FRESHNESS AUDIT OF writeup/INDEX.md (SINCE LEG 108's PASS)
(RESERVE)
**Thesis.** Leg 68 fixed INDEX.md once; leg 108 (IX2) audited it through the ~105 era. The
110-125 wave has since landed — including literature ledgers (112, 113), the NG theorem
(58, now ruled mergeable), post-repair suites (103/104/105), and the audit family's largest
batch — under exactly the high-throughput conditions that made it stale both prior times.
Same audit, new window, pinned at this leg's start SHA; the "no measurement, no figure"
convention and the parked-escalation convention (parked legs are listed as parked, not as
landed) are both part of what freshness means here.
**Gate.** At the pinned SHA, does writeup/INDEX.md correctly reflect every leg landed since
leg 108's pass — present, correctly described, correctly figure-conventioned, with parked
escalations marked parked?
  yes -> Confirmed fresh; bank the dated record.
  no  -> Fix INDEX.md directly (the leg-68 precedent: INDEX.md freshness is this route's own
         territory), listing every corrected row in the JSON.
**Territory.** writeup/INDEX.md, experiments/p2_route_ix3_v1_index_audit.py,
               writeup/data/p2_route_ix3_v1_index_audit.json,
               writeup/novelty/leg_138.md, experiments/journal/leg_138.md
**Difficulty.** light
**Independence.** Owns INDEX.md for this pass (no other live or reserve leg touches it);
read-only on everything else. Disjoint from 137 (different ledger). Immediately
dispatchable.
```

```
### 139 — ROUTE-DGA: ADVERSARIAL AUDIT OF decay_grading.py (RESERVE)
**Thesis.** solver/decay_grading.py carries the decay-graded function spaces under the
collocation lane — sibling to decay_collocation.py, where leg 115 just found three real
silent-corruption gaps. It has a dedicated test file but no adversarial battery, and it is
one of only two load-bearing solver modules the audit family has never touched. Same
silent-corruption question, same robustness-only precedent as legs 69/100/101/115: under
NaN-poisoned grading parameters, degenerate decay exponents, or malformed grids, does it
silently return plausible wrong values instead of flagging the input?
**Gate.** Under an adversarial battery of degenerate or poisoned inputs, does
solver/decay_grading.py ever silently return a wrong value rather than propagating or
flagging the invalid input?
  yes -> Silent-corruption gap; report the exact failing case with magnitudes; escalate, do
         not patch.
  no  -> Confirmed robust; bank the battery as a permanent regression test.
**Territory.** test_decay_grading_adversarial.py,
               experiments/p2_route_dga_v1_adversarial.py,
               writeup/data/p2_route_dga_v1_adversarial.json,
               writeup/novelty/leg_139.md, experiments/journal/leg_139.md
**Difficulty.** standard
**Independence.** Reads solver/decay_grading.py only; edits nothing. Disjoint from leg
115's territory (different module, same lane). Immediately dispatchable.
```

```
### 140 — ROUTE-NFA: ADVERSARIAL AUDIT OF nk_fourier.py (RESERVE)
**Thesis.** solver/nk_fourier.py carries the Fourier (circle) form of the two-scale operator
— certificate-adjacent code in the same family where the fabrication-rejection pattern has
now hit three for three (legs 79, 98, 116). It has a dedicated test file but no adversarial
battery. Same question as its siblings, both flavors: silent corruption under
degenerate/poisoned input, and — where it reports any bound-like or certificate-feeding
quantity — whether a fabricated input can pass unflagged. Read-only precedent throughout.
**Gate.** Under an adversarial battery of degenerate or poisoned inputs, does
solver/nk_fourier.py ever silently return a wrong value, or accept a fabricated
certificate-feeding quantity unflagged?
  yes -> Silent-corruption or fabrication-acceptance gap; report the exact failing case with
         magnitudes; escalate, do not patch (if it is the same Y0/Z0/Z1 guard class, say so
         explicitly — leg 128's shared guard may absorb it).
  no  -> Confirmed robust; bank the battery as a permanent regression test.
**Territory.** test_nk_fourier_adversarial.py,
               experiments/p2_route_nfa_v1_adversarial.py,
               writeup/data/p2_route_nfa_v1_adversarial.json,
               writeup/novelty/leg_140.md, experiments/journal/leg_140.md
**Difficulty.** standard
**Independence.** Reads solver/nk_fourier.py only; edits nothing. Distinct module from
nk_bounds.py (leg 128's territory) and nk_seminorm.py — checked explicitly. Immediately
dispatchable.
```

```
### 141 — ROUTE-WEL: IS LEG 111's ZERO-WIDTH WEIGHTED-ENERGY WINDOW PUBLISHED? (RESERVE)
**Thesis.** Leg 111 (WE) killed the third realization with a structural result, not a bad
margin: on the a=0 CLM linearization, every admissible weight's coercivity gap converges to
-(3-gamma)/2, damping at the origin needs gamma>3, and the weighted space exists only for
gamma<3 — the SAME threshold, so the window has zero width by construction. That is a
sharper statement than "we measured a negative": it is a candidate structural obstruction to
Chen-Hou-style weighted-energy certification on this operator class. Leg 65 (L1G) asked
exactly this question one realization earlier — is the no-go published? — and the answer
(genuinely unpublished) upgraded a dead end into a confirmed-novel negative. Ask it again
for the third realization, at full-text depth, links not counts: does any published work
state, imply, or contain the gamma-threshold coincidence for CLM/gCLM weighted-energy
coercivity (or a strictly more general result it falls out of)? The answer feeds directly
into the publication scoping the NG ruling just put to the user — three dead realizations,
each with a novelty status, is the honest shape of that writeup. Scope guard: this is a
literature leg — it re-runs no coercivity computation, edits no solver module, and lifts no
ban under any outcome; L1 stays measured-dead in all three realizations regardless.
**Gate.** Does any published work contain leg 111's zero-width-window obstruction (the
damping/space gamma-threshold coincidence on the CLM linearization), explicitly or as a
special case of a stated more-general result?
  yes -> The third realization's death was pre-empted in the literature. Record the located
         statement with hypotheses verbatim; cap the finding's novelty accordingly wherever
         it is cited.
  no  -> A third confirmed-novel narrowly-scoped negative, parallel to leg 65's. Bank the
         dated ledger; flag to the user (via the report, not an escalation) that the NG
         publication scoping can cite three dead realizations, two of them confirmed novel.
**Territory.** experiments/p2_route_wel_v1_lit.py,
               writeup/data/p2_route_wel_v1_lit.json,
               writeup/novelty/leg_141.md, experiments/journal/leg_141.md
**Difficulty.** light
**Independence.** Literature-only, own JSON, no solver module. Disjoint from 62/112/113's
papers and questions (those concern the ell-1/radii-polynomial lane; this is the
weighted-energy lane's novelty) and from 127/NGX (that is mathematics on the A21 != 0
class, not literature on the energy realization). Does NOT edit solver/literature_gates.py.
Immediately dispatchable.
```

```
### 142 — ROUTE-NSA: ADVERSARIAL AUDIT OF nk_seminorm.py (RESERVE)
**Thesis.** One of the last reachable, never-audited modules per the 128-series inventory
(decay_grading.py and nk_fourier.py, its siblings in that inventory, are already dispatched as
139/DGA and 140/NFA). `nk_seminorm.py` computes seminorm bounds feeding the same certifying
pipeline that legs 79/98/116 found the Y0/Z0/Z1 fabrication-acceptance gap in three times
running (now under shared-guard repair as leg 128). Run the standard adversarial battery:
NaN/Inf input, degenerate/zero-measure domains, boundary-of-validity parameters, and a planted
wrong-value pass-through, per the pattern that has found a real defect in roughly half of the
prior ~20 audits.
**Gate.** Under adversarial and degenerate inputs, does `nk_seminorm.py` ever silently return
a wrong seminorm value (accept NaN/Inf, mishandle a degenerate domain, or pass a planted wrong
value through unflagged) rather than reject or visibly propagate the defect?
  yes -> Name the exact mechanism and magnitude; do not patch under this leg's own authority —
         flag for a repair leg on the leg-76/128 precedent if it is claim-adjacent.
  no  -> Bank the battery as the module's permanent regression suite; record in
         capabilities.py (append-only) that the module has passed adversarial audit.
**Territory.** test_nk_seminorm_adversarial.py, experiments/p2_route_nsa_v1_adversarial.py,
               writeup/data/p2_route_nsa_v1_adversarial.json,
               writeup/novelty/leg_142.md, experiments/journal/leg_142.md
**Difficulty.** standard
**Independence.** Reads solver/nk_seminorm.py; edits nothing under either outcome. Not
touched by any live or reserve leg. Immediately dispatchable.
```

```
### 143 — ROUTE-VNA: ADVERSARIAL AUDIT OF viscous_novelty.py (RESERVE)
**Thesis.** The other genuinely-uncovered, reachable module per the same 128-series
inventory. `viscous_novelty.py` is read by the EXT-family freshness legs (90/93/123) as part
of their novelty-scoping claims but has itself never had an adversarial battery run against
it. Same standard battery as every other audit-family leg: NaN/Inf, degenerate/zero-measure
input, boundary parameters, planted wrong-value pass-through.
**Gate.** Under adversarial and degenerate inputs, does `viscous_novelty.py` ever silently
return a wrong value rather than reject or visibly propagate the defect?
  yes -> Name the exact mechanism and magnitude; escalate for a repair leg if claim-adjacent,
         do not patch under this leg's own authority.
  no  -> Bank the battery as the permanent regression suite; record the pass in
         capabilities.py.
**Territory.** test_viscous_novelty_adversarial.py,
               experiments/p2_route_vna_v1_adversarial.py,
               writeup/data/p2_route_vna_v1_adversarial.json,
               writeup/novelty/leg_143.md, experiments/journal/leg_143.md
**Difficulty.** standard
**Independence.** Reads solver/viscous_novelty.py; edits nothing under either outcome. Not
touched by any live or reserve leg. Immediately dispatchable.
```

```
### 144 — ROUTE-ECA: ADVERSARIAL AUDIT OF energy_coercivity.py (RESERVE)
**Thesis.** `energy_coercivity.py` is leg 111's brand-new module (the third-realization
weighted-energy coercivity scoping, landed this run) and has never had an adversarial pass —
every other module the audit family has covered got one shortly after landing; this one is
overdue precisely because it landed mid-cycle during the reserve-drain refill. Standard
battery: NaN/Inf input, degenerate weight classes, boundary-of-admissibility parameters
(gamma near the 3-gamma threshold leg 111 itself measured), and a planted wrong-coercivity
pass-through.
**Gate.** Under adversarial and degenerate inputs (including gamma at or near the measured
zero-width-window threshold), does `energy_coercivity.py` ever silently return a wrong
coercivity-gap value rather than reject or visibly propagate the defect?
  yes -> Name the exact mechanism and magnitude. This module underwrites leg 111's
         zero-width-window finding (feeding directly into leg 141/WEL's publication
         scoping) — escalate rather than patch under this leg's own authority.
  no  -> Bank the battery as the permanent regression suite; record the pass in
         capabilities.py. Independently strengthens leg 111's finding.
**Territory.** test_energy_coercivity_adversarial.py,
               experiments/p2_route_eca_v1_adversarial.py,
               writeup/data/p2_route_eca_v1_adversarial.json,
               writeup/novelty/leg_144.md, experiments/journal/leg_144.md
**Difficulty.** standard
**Independence.** Reads solver/energy_coercivity.py; edits nothing under either outcome.
Module unowned — leg 111 (WE) landed and closed. Read-only overlap with 141 (WEL, literature
only, no code) is read-read on the same finding, not a collision. Immediately dispatchable.
```

```
### 145 — ROUTE-LGA: ADVERSARIAL AUDIT OF literature_gates.py's LEDGER SELF-CONSISTENCY
(RESERVE)
**Thesis.** `literature_gates.py` was off-limits to the audit family while leg 62 (CP) was
live (62 owns it); leg 62 has since landed and the module is cleared, the same
free-again pattern as `weight_search.py` and `bordered_hl.py` after their own owning legs
closed. The ledger backs every literature-lane leg's novelty claim (55, 57, 65, 90, 93, 112,
113, 123, 141 and counting) — a defect here would not corrupt a computation, but could
silently misreport what a citation actually says. Audit for self-consistency rather than the
standard numerical battery: does every entry's stored claim match what its own cited
paper/section says, and does every entry cite a paper actually checked (no phantom
citations)?
**Gate.** Does every row in literature_gates.py's ledger (a) cite a real, checked source, and
(b) accurately state that source's claim, with no drift between the stored summary and the
paper's own text?
  yes -> Bank the ledger's clean bill as the permanent audit record; record the pass in
         capabilities.py.
  no  -> Name the exact row, the drift, and its blast radius (which downstream legs' novelty
         claims cite it). Escalate — a ledger correction is claim-adjacent and not this leg's
         to patch unilaterally if any downstream finding's wording would need to change.
**Territory.** test_literature_gates_selfconsistency.py,
               experiments/p2_route_lga_v1_ledger.py,
               writeup/data/p2_route_lga_v1_ledger.json,
               writeup/novelty/leg_145.md, experiments/journal/leg_145.md
**Difficulty.** standard
**Independence.** Reads solver/literature_gates.py; edits nothing under either outcome.
Module is cleared and free — leg 62 (CP) landed and closed. Not touched by any live or
reserve leg. Immediately dispatchable.
```

```
### 146 — ROUTE-CSA: ADVERSARIAL AUDIT OF certificate_shapes.py (RESERVE)
**Thesis.** `certificate_shapes.py` is leg 62's other owned module, likewise cleared and free
now that 62 has landed. It supplies the shape/class enumeration that leg 54's battery and leg
58's theorem both range over (the exact space leg 126/BX's closure audit just certified as
fully covered) — a silent enumeration bug here would be the one thing that could put a hole in
126's own "1,686 configurations, zero uncovered" count without 126 itself detecting it, since
126 reads the enumeration as given. Standard adversarial battery plus an explicit completeness
check: does the enumerated shape/class list match what legs 54/58/126 each assumed it to be.
**Gate.** Under adversarial input (malformed shape descriptors, boundary class parameters,
degenerate splits) does `certificate_shapes.py` ever silently return a wrong or incomplete
enumeration, and does its enumerated set match what legs 54/58/126 each read from it?
  yes -> Name the exact mechanism. If the enumeration itself is short or wrong, this directly
         threatens leg 126's completeness claim — escalate immediately as a priority finding,
         do not patch under this leg's own authority.
  no  -> Bank the battery as the permanent regression suite; record in capabilities.py, and
         note explicitly that leg 126's completeness count is independently corroborated.
**Territory.** test_certificate_shapes_adversarial.py,
               experiments/p2_route_csa_v1_adversarial.py,
               writeup/data/p2_route_csa_v1_adversarial.json,
               writeup/novelty/leg_146.md, experiments/journal/leg_146.md
**Difficulty.** standard
**Independence.** Reads solver/certificate_shapes.py; edits nothing under either outcome.
Module is cleared and free — leg 62 (CP) landed and closed. Read-only overlap with 126/BX's
own read-set is read-read, not a collision (126 has already landed regardless). Immediately
dispatchable.
```

```
### 147 — ROUTE-NKB: POST-REPAIR REGRESSION CHECK, nk_bounds.py (RESERVE — NOT dispatchable
until leg 128/NKR lands)
**Thesis.** Leg 128 (NKR) is repairing the Y0/Z0/Z1 fabrication-acceptance gap across
nk_bounds.py and its two already-repaired siblings via one shared guard. Per the
86/87/94/103/104/105/131/132/133/134 pattern, every repair in this repository gets an
independent close-the-loop regression check rather than resting on its own self-report —
`nk_bounds.py` is the one module in the 128 repair that has not previously had a postrepair
leg drafted for it (its siblings' postrepair legs, 86 and 105, already exist and landed).
**Gate.** Post-repair, does solver/nk_bounds.py (a) reject every one of leg 116's 21
false-closing cases in an independent re-run, with every GAP-PIN inverted and every HOLDS
gate still passing, and (b) reproduce every previously-validated clean-call result
bit-identically, including its capabilities.py validated line?
  yes -> Repair confirmed solid and non-regressive by an independent run. Bank leg 116's
         battery as a permanent regression suite for this module specifically.
  no  -> An incomplete fix or a repair regression. Report the exact case precisely; escalate
         as a priority finding, do not patch under this leg's own authority.
**Territory.** test_nk_bounds_postrepair.py, experiments/p2_route_nkb_v1_postrepair.py,
               writeup/data/p2_route_nkb_v1_postrepair.json,
               writeup/novelty/leg_147.md, experiments/journal/leg_147.md
**Difficulty.** standard
**Independence.** Reads solver/nk_bounds.py; edits nothing under either outcome. **NOT
dispatchable until leg 128 (NKR) lands** — drafted now so it is ready immediately after, same
discipline as legs 95/103/104/105/131–135.
```

```
### 148 — ROUTE-SUB: POST-REPAIR REGRESSION CHECK, spectral_utils.py + boussinesq.py DEALIAS
FIX (RESERVE — NOT dispatchable until leg 129/SUR lands, which is itself blocked until leg
133/BOB lands)
**Thesis.** Leg 129 (SUR) is repairing the shared `<= n/3` dealias off-by-one in both
`spectral_utils.py`'s `dealias_mask` and `boussinesq.py`'s `dealias_mask2d`, plus leg 120's
five silent-absorption defects, inverting the defect-encoding assertion in
test_spectral_utils_dedicated.py in the same commit. Same close-the-loop discipline as every
other repair this run: an independent re-run of leg 120's full original battery against the
repaired modules, not the repair's own bundled report.
**Gate.** Post-repair, do `spectral_utils.py` and `boussinesq.py` (a) both use the strict
(k < n/3) dealias cut, bit-identical at every grid size in the repository's declared set with
all 107 banked energy_balance_residual records reproducing exactly, (b) show energy_
production's 3|n error fall from 1.66e-01 to the 2.5e-14 class independently, and (c) have all
five absorption-defect PINs inverted with every HOLDS gate passing?
  yes -> Repair confirmed solid and non-regressive by an independent run. Bank leg 120's
         battery as a permanent regression suite for both modules.
  no  -> An incomplete fix or a repair regression. Report the exact value precisely; escalate
         as a priority finding, do not patch under this leg's own authority.
**Territory.** test_spectral_utils_postrepair.py, test_boussinesq_dealias_postrepair.py,
               experiments/p2_route_sub_v1_postrepair.py,
               writeup/data/p2_route_sub_v1_postrepair.json,
               writeup/novelty/leg_148.md, experiments/journal/leg_148.md
**Difficulty.** standard
**Independence.** Reads solver/spectral_utils.py and solver/boussinesq.py; edits nothing
under either outcome. **NOT dispatchable until leg 129 (SUR) lands** — and 129 is itself
blocked until leg 133 (BOB) lands, so this is a double-blocked deep-reserve draft, ready the
moment its chain clears.
```

```
### 149 — ROUTE-PGF: FRESHNESS/SELF-CONSISTENCY AUDIT OF PROGRESS.md's ⚠ NEEDS YOU LEDGER
(RESERVE)
**Thesis.** `PROGRESS.md`'s `⚠ NEEDS YOU` section is the one surface the user reads first, and
it is now carrying three linked open items at once for the first time this run (leg 126's
stage-B exhaustion, leg 63/125's M2 ruling, and the exit-criterion question) — exactly the
"high throughput, per-item drift" condition legs 68/72/102/108/137/138 have each found real
gaps under on their own freshness surfaces. Light hygiene: does every parked branch, every
escalation, and every open direction question actually named in this file's own "Open
direction questions for the user" section and Status have a corresponding, accurate entry in
PROGRESS.md, and vice versa (no orphaned entry on either side)?
**Gate.** Does every escalation/parked-branch/open-question item in DIRECTION.md's Status and
"Open direction questions" sections have an accurate, current PROGRESS.md `⚠ NEEDS YOU` entry,
and does every PROGRESS.md `⚠ NEEDS YOU` entry correspond to something actually live in
DIRECTION.md (no stale entry left behind after a ruling lands)?
  yes -> Bank the dated completeness record; no drift between the two ledgers.
  no  -> Report the exact missing or stale entry per item (the count is the finding, per the
         JR-family precedent); create nothing on another leg's or the user's behalf; escalate
         only if the gap concerns a parked escalation, not general hygiene.
**Territory.** experiments/p2_route_pgf_v1_ledger_audit.py,
               writeup/data/p2_route_pgf_v1_ledger_audit.json,
               writeup/novelty/leg_149.md, experiments/journal/leg_149.md
**Difficulty.** light
**Independence.** Reads PROGRESS.md and DIRECTION.md only; no solver module; edits neither
file under either outcome (reports findings for the DM/orchestrator to act on, same
discipline as the JR/IX freshness family). Not touched by any live or reserve leg. Immediately
dispatchable.
```

```
### 150 — ROUTE-CNR: REPAIR collocation_newton.py (leg 114's finding) (RESERVE)
**Thesis.** Leg 114 (CNA) landed gate YES: 8 silent-corruption cases across 3 mechanisms in
the Newton solve behind L1's collocation death certificate — its own report merged to `main`
normally; only the source-module patch was deferred, per the leg's own "do not patch under
this leg's own authority" instruction (which defers the fix, not the finding). No repair has
landed since. Follow the 128/129/130 repair template: fix each of the 3 mechanisms, prove
zero movement on every previously-passing case, invert leg 114's PINs in the same commit.
**Gate.** Post-repair: (a) do all 8 of leg 114's failing cases now either reject the
degenerate/poisoned input or report a residual that accurately reflects non-convergence, with
every PIN inverted, and (b) is the module bit-identical on every previously-passing case,
including leg 110's death-certificate reproduction and any capabilities.py validated line?
  yes -> The collocation death certificate's code-level gap is closed. Merge the repair and
         this leg's report to `main` normally; bank leg 114's battery as the permanent
         regression suite; a close-the-loop postrepair leg follows next refill.
  no  -> If any clean-input result moves at all, or a mechanism resists a clean fix, merge
         this leg's report with the exact case reported and ESCALATE — do not iterate the
         repair under this leg's own authority. The report lands either way; only further
         patching stops.
**Territory.** solver/collocation_newton.py, test_collocation_newton_adversarial.py (pin
               inversions, same commit), experiments/p2_route_cnr_v1_repair.py,
               writeup/data/p2_route_cnr_v1_repair.json,
               writeup/novelty/leg_150.md, experiments/journal/leg_150.md
**Difficulty.** standard
**Independence.** Sole owner of collocation_newton.py (leg 114 landed and closed; no other
live/reserve leg touches it). Disjoint from 151–154 (different modules) and from 110 (reads,
never writes, the same module read-only). Immediately dispatchable.
```

```
### 151 — ROUTE-DCR: REPAIR decay_collocation.py (leg 115's finding) (RESERVE)
**Thesis.** Leg 115 (DCA) landed gate YES: 3 silent-corruption gaps in the nodal spectral core
under the collocation lane; its own report merged normally, only the patch deferred. No
repair has landed since. Same repair template as 150/128/129/130.
**Gate.** Post-repair: (a) do all 3 of leg 115's failing cases now reject or visibly flag the
degenerate/poisoned input, with every PIN inverted, and (b) is the module bit-identical on
every previously-passing case, including any capabilities.py validated line?
  yes -> Merge the repair and this leg's report to `main` normally; bank leg 115's battery as
         the permanent regression suite; a close-the-loop postrepair leg follows next refill.
  no  -> Merge this leg's report with the exact case reported and ESCALATE — do not iterate
         the repair under this leg's own authority. The report lands either way.
**Territory.** solver/decay_collocation.py, test_decay_collocation_adversarial.py (pin
               inversions, same commit), experiments/p2_route_dcr_v1_repair.py,
               writeup/data/p2_route_dcr_v1_repair.json,
               writeup/novelty/leg_151.md, experiments/journal/leg_151.md
**Difficulty.** standard
**Independence.** Sole owner of decay_collocation.py (leg 115 landed and closed). Disjoint
from 150/152/153/154. Immediately dispatchable.
```

```
### 152 — ROUTE-HRR: REPAIR hl_rescaled.py (leg 117's finding) (RESERVE)
**Thesis.** Leg 117 (HRA) landed gate YES: 4 silent-corruption mechanisms — unvalidated
non-ascending X in velocity() (91x true-scale error, 0 warnings), X_ref clamped silently
outside [X.min(), X.max()] via np.interp, sinh_grid_at(M<0) silently mirroring, and
degenerate_ic's np.where laundering a NaN abscissa into a legitimate-looking 0.0 — plus the
same IEEE-754 NaN-comparison blind spot in RescaledHL's own ascending guard (characterized,
not exploited: chains to visible all-NaN downstream, not a finite wrong answer, so this one
clause may be documented rather than patched if the fix would be higher-risk than the latent
defect it closes — leg author's call, stated explicitly either way). Its report merged
normally; the patch was deferred. No repair since.
**Gate.** Post-repair: (a) does velocity() reject or visibly flag non-ascending X, does
X_ref get validated against [X.min(), X.max()] rather than silently clamped, does
sinh_grid_at reject M<0, and does degenerate_ic distinguish a NaN abscissa from a legitimate
0.0 in its np.where — with every PIN inverted for whichever clauses are patched (or the
NaN-comparison clause explicitly documented, not patched, with the leg's own reasoning
recorded) — and (b) is the module bit-identical on every previously-passing case?
  yes -> Merge the repair and this leg's report to `main` normally; bank leg 117's battery as
         the permanent regression suite; a close-the-loop postrepair leg follows next refill.
  no  -> Merge this leg's report with the exact case reported and ESCALATE — do not iterate
         the repair under this leg's own authority. The report lands either way.
**Territory.** solver/hl_rescaled.py, test_hl_rescaled_adversarial.py (pin inversions, same
               commit), experiments/p2_route_hrr_v1_repair.py,
               writeup/data/p2_route_hrr_v1_repair.json,
               writeup/novelty/leg_152.md, experiments/journal/leg_152.md
**Difficulty.** standard
**Independence.** Sole owner of hl_rescaled.py (leg 117 landed and closed). Disjoint from
150/151/153/154. Immediately dispatchable.
```

```
### 153 — ROUTE-HHR: REPAIR hilbert_holder.py (leg 119's finding) (RESERVE)
**Thesis.** Leg 119 (HHA) landed gate YES: a bound-direction violation in
hilbert_holder.py's Holder estimate, the sibling finding to leg 106's hilbert_pointwise.py
(already repaired as leg 130/HPR). Its report merged normally; the patch was deferred. Follow
the leg 130/op_lower precedent exactly: on the failing configuration, either reject the input
loudly or return a bound verified to dominate the true value — never a sharpened bound.
**Gate.** Post-repair: (a) does hilbert_holder.py's reported bound now either raise on the
failing configuration or provably dominate the true value there, with the PIN inverted, and
(b) is the module bit-identical on every previously-passing case, including any
capabilities.py validated line?
  yes -> Merge the repair and this leg's report to `main` normally; bank leg 119's battery as
         the permanent regression suite; a close-the-loop postrepair leg follows next refill.
  no  -> Merge this leg's report with the exact case and magnitudes reported and ESCALATE —
         do not iterate the repair under this leg's own authority. The report lands either way.
**Territory.** solver/hilbert_holder.py, test_hilbert_holder_adversarial.py (pin inversions,
               same commit), experiments/p2_route_hhr_v1_repair.py,
               writeup/data/p2_route_hhr_v1_repair.json,
               writeup/novelty/leg_153.md, experiments/journal/leg_153.md
**Difficulty.** standard
**Independence.** Sole owner of hilbert_holder.py (leg 119 landed and closed; distinct from
hilbert_pointwise.py, leg 130's already-closed module). Disjoint from 150/151/152/154.
Immediately dispatchable.
```

```
### 154 — ROUTE-CDR: REPAIR critical_dissipation.py (leg 121's finding) (RESERVE)
**Thesis.** Leg 121 (CDA) landed gate YES: solver/critical_dissipation.py silently truncates
a non-integer p (2s) to a different, lower integer exponent rather than rejecting or flagging
a fractional-order input outside its validated domain. Its report merged normally; the patch
was deferred. Follow the target_norm.py/leg-94 domain-guard precedent: reject or explicitly
extend and flag, never silently substitute a different exponent.
**Gate.** Post-repair: (a) does critical_dissipation.py reject or visibly flag every
non-integer p (2s) case in leg 121's battery rather than silently truncating, with the PIN
inverted, and (b) is the module bit-identical on every previously-passing integer-p case,
including any capabilities.py validated line?
  yes -> Merge the repair and this leg's report to `main` normally; bank leg 121's battery as
         the permanent regression suite; a close-the-loop postrepair leg follows next refill.
  no  -> Merge this leg's report with the exact case and magnitudes reported and ESCALATE —
         do not iterate the repair under this leg's own authority. The report lands either way.
**Territory.** solver/critical_dissipation.py, test_critical_dissipation_adversarial.py (pin
               inversions, same commit), experiments/p2_route_cdr_v1_repair.py,
               writeup/data/p2_route_cdr_v1_repair.json,
               writeup/novelty/leg_154.md, experiments/journal/leg_154.md
**Difficulty.** standard
**Independence.** Sole owner of critical_dissipation.py (leg 121 landed and closed). Disjoint
from 150/151/152/153. Immediately dispatchable.
```

```
### 155 — ROUTE-JR4: FOURTH FRESHNESS AUDIT OF experiments/JOURNAL.md AND journal/ (SINCE LEG
137's PASS) (RESERVE)
**Thesis.** Leg 137 (JR3) audited the journal through the pinned SHA of its own start,
covering the 100–125 wave. Since then, the 126/128–149 wave — one of the largest of the run,
including the stage-B exhaustion landing — has gone in at high throughput, exactly the
condition under which per-leg files go missing (the founding finding of this freshness
family, leg 72). Pin the audit window at this leg's own start SHA to avoid racing in-flight
landings.
**Gate.** At the pinned SHA, does every landed leg since JR3's window have (a) its
experiments/journal/leg_N.md on main, (b) a JOURNAL.md pointer line, and (c) its
writeup/novelty/leg_N.md?
  yes -> The ledger is complete through the pinned SHA. Bank the dated completeness record;
         merge this leg's report to `main` normally.
  no  -> Report the exact missing files per leg (the count is the finding, per JR1–JR3
         precedent); create nothing on another leg's behalf; merge the report regardless;
         escalate only if a missing file belongs to a parked escalation.
**Territory.** experiments/p2_route_jr4_v1_journal_audit.py,
               writeup/data/p2_route_jr4_v1_journal_audit.json,
               writeup/novelty/leg_155.md, experiments/journal/leg_155.md
**Difficulty.** light
**Independence.** Reads experiments/JOURNAL.md and journal/*.md only; no solver module;
edits neither under either outcome. Disjoint from 156 (INDEX.md, not JOURNAL.md) and from
149 (PROGRESS.md/DIRECTION.md, a different pair of files). Immediately dispatchable.
```

```
### 156 — ROUTE-IX4: FOURTH FRESHNESS AUDIT OF writeup/INDEX.md (SINCE LEG 138's PASS)
(RESERVE)
**Thesis.** Leg 138 (IX3) audited INDEX.md through its own pinned SHA. The same 126/128–149
landing wave that motivates 155 (JR4) applies here: does INDEX.md correctly reflect every leg
landed since, including the stage-B exhaustion entry and every repair/postrepair pair in the
wave.
**Gate.** At this leg's own pinned start SHA, does INDEX.md correctly reflect every leg
landed since leg 138's window closed?
  yes -> The index is current through the pinned SHA. Bank the dated completeness record;
         merge this leg's report to `main` normally.
  no  -> Report the exact stale or missing entries (the count is the finding); fix INDEX.md
         directly per the leg 68/108/138 mechanical-fix precedent (INDEX.md freshness is its
         own territory, not another leg's); merge regardless.
**Territory.** writeup/INDEX.md, experiments/p2_route_ix4_v1_index_audit.py,
               writeup/data/p2_route_ix4_v1_index_audit.json,
               writeup/novelty/leg_156.md, experiments/journal/leg_156.md
**Difficulty.** light
**Independence.** Owns writeup/INDEX.md exclusively among live/reserve legs (same precedent
as 68/108/138). Disjoint from 155 (JOURNAL.md, not INDEX.md). Immediately dispatchable.
```

```
### 157 — ROUTE-CDX: DOES CADIOT arXiv:2505.03091 SUGGEST AN UNTRIED CONSTRUCTION FOR A21 !=
0? (RESERVE)
**Thesis.** Leg 62 read Cadiot arXiv:2505.03091 in full and settled a narrow coverage
question: it does NOT cover the off-diagonal/zero-diagonal case leg 58's theorem occupies.
That leg never asked the deeper question, and the paper is already fully consulted (no new
access cost): does Cadiot's own construction — whatever approximate-inverse or
preconditioning technique it uses for its covered (diagonal-bounded-below) case — suggest an
adaptation, generalization, or explicit alternative construction that could be tried on the
A21 != 0 class leg 127 (NGX) is searching? This is read-deeper-not-reconfirm: no coverage
re-litigation, no re-opening of leg 62's settled NO.
**Gate.** Does Cadiot arXiv:2505.03091, at full-text depth (including any construction,
remark, or forward citation it contains), suggest a concrete alternative construction or
adaptation applicable to the A21 != 0 class that has not already been tried in this
repository (by leg 54's battery, leg 58's theorem, or leg 127's in-progress work)?
  yes -> Record the construction verbatim with its hypotheses and exact page/section
         reference; ESCALATE it as a candidate starting point for leg 127 or a follow-up leg
         — do not build or test it under this leg's own authority.
  no  -> Cadiot's construction is confirmed to offer nothing beyond its own settled scope.
         Bank the ledger entry; this closes the "unmined literature" question for this
         specific source.
**Territory.** experiments/p2_route_cdx_v1_lit.py, writeup/data/p2_route_cdx_v1_lit.json,
               writeup/novelty/leg_157.md, experiments/journal/leg_157.md.
               Does NOT edit solver/literature_gates.py or solver/certificate_shapes.py.
**Difficulty.** light
**Independence.** Literature-only, own JSON, no solver module. Disjoint from 62 (settled,
different question), 127 (NGX, mathematics not literature — this leg only surfaces a
candidate for 127 to evaluate, never evaluates one itself), and 145/146 (code-level ledger
audits of literature_gates.py/certificate_shapes.py, not literature reading). Immediately
dispatchable.
```

```
### 158 — ROUTE-BDX: DOES BDL arXiv:1503.06315 SUGGEST AN UNTRIED FIX FOR THE ZERO-DIAGONAL
CASE? (RESERVE)
**Thesis.** Leg 57 read BDL arXiv:1503.06315 in full and confirmed it publishes a
non-block-diagonal approximate inverse requiring a diagonal bounded away from zero — the
`plan_of_record.py` ban text itself cites this as "the reason to keep this ban." Never asked:
does BDL's own construction contain a preconditioning, regularization, or compensating-term
technique — the same SHAPE as leg 58's own SS5 finding, that A21 != 0 buys back exactly one
unit on the kernel direction at a cost elsewhere — that could be adapted to the zero-diagonal
case even though BDL's own theorem doesn't cover it? Full text already consulted; this is a
second, deeper pass over the same source, not a new literature search.
**Gate.** Does BDL arXiv:1503.06315, at full-text depth, contain a construction, technique,
or remark that suggests a concrete way to compensate for a zero (rather than bounded-below)
diagonal, applicable to leg 58's/127's operator class?
  yes -> Record the technique verbatim with its hypotheses and exact reference; ESCALATE as a
         candidate for leg 127 or a follow-up construction leg — do not build or test it here.
  no  -> BDL is confirmed to offer nothing beyond the zero-diagonal exclusion leg 57 already
         found. Bank the ledger entry.
**Territory.** experiments/p2_route_bdx_v1_lit.py, writeup/data/p2_route_bdx_v1_lit.json,
               writeup/novelty/leg_158.md, experiments/journal/leg_158.md.
               Does NOT edit solver/literature_gates.py or solver/certificate_shapes.py.
**Difficulty.** light
**Independence.** Literature-only, own JSON, no solver module. Disjoint from 57 (settled,
different question) and 157 (different paper). Immediately dispatchable.
```

```
### 159 — ROUTE-WEX: DOES THE WEIGHTED-ENERGY LITERATURE CONTAIN AN UNTRIED FUNCTIONAL?
(RESERVE)
**Thesis.** Leg 111 measured a zero-width window on ONE weighted-energy construction on the
a=0 CLM linearization (damping needs gamma>3, the weighted space exists only for gamma<3).
Leg 141 (WEL) asks whether THAT SPECIFIC obstruction is published — a coverage question, not
a construction search. The same Chen-Hou-lineage sources both legs already consulted were
never asked whether they contain a DIFFERENT weighted-energy functional (an added cross term,
a modified Sobolev correction, a different weight-class family) that could shift either
threshold away from the coincidence leg 111 measured. Scope guard: this leg reads and reports
only — it re-runs no coercivity computation and edits no solver module, same discipline as
141.
**Gate.** Does the weighted-energy / Chen-Hou-lineage literature already consulted by legs 65
and 111/141 contain, explicitly or as a derivable special case, a weighted-energy functional
different from leg 111's construction that is not subject to the same gamma-threshold
coincidence?
  yes -> Record the functional verbatim with its hypotheses and exact reference; ESCALATE as
         a candidate for a leg-111-v2 construction leg — do not compute it here.
  no  -> Confirms leg 111's construction was not merely one of many untried options; the
         zero-width window is the literature's own apparent boundary too. Bank the ledger.
**Territory.** experiments/p2_route_wex_v1_lit.py, writeup/data/p2_route_wex_v1_lit.json,
               writeup/novelty/leg_159.md, experiments/journal/leg_159.md
**Difficulty.** light
**Independence.** Literature-only, own JSON, no solver module (does not touch
solver/energy_coercivity.py, which 144 audits at the code level — read-read on the same
finding at most, not a collision). Disjoint from 141 (coverage of the specific obstruction,
not a construction search). Immediately dispatchable.
```

```
### 160 — ROUTE-WVR: A GENUINELY REPAIRED FITNESS DEFINITION FOR STAGE-B-STYLE GA, GATED BY
THE FROZEN SIX-PROPERTY VIABILITY CHECK — NO GA COMPUTE ON EITHER BRANCH (RESERVE)
**Thesis.** The GA ban's own stated lift condition is "a re-run of the six-property gate that
PASSES on a repaired fitness" — never met (leg 49: 4/6; leg 59: repaired wall model, P2
0.775->0.975, but P3 worst |slope-1| UNMOVED at 0.342 against the 0.05 floor). Leg 59's own
forward-pointer is explicit: "any future B proposal must change the fitness's DEFINITION, not
its wall model" — leg 59 already tried the wall-model repair and P3 did not move AT ALL,
which is the strongest evidence yet that the defect is in what the fitness tracks, not how it
models the geometry. This leg proposes a genuinely different fitness DEFINITION — not a
retry of 46/49/59's linear-in-injected-defect |slope-1| metric — pre-named and fixed in the
driver before any computation (per the leg-111 pre-naming discipline), e.g. a metric that
tracks the defect's actual local curvature rather than assuming linearity, or a
resolution-normalized coercivity measure that does not require P3's fixed 0.05 floor to be
met by a linear proxy. Whatever the specific proposal, it must be a definitional change, per
leg 59's own diagnosis of where the repair needs to happen.
**Gate.** Does the new fitness definition pass the FROZEN six-property viability gate
unchanged (all six properties, including P2 >= 0.90 and P3 max |slope-1| <= 0.05, exactly as
specified in `plan_of_record.py`'s C-PILOT stage)?
  yes -> The GA ban's recorded lift condition is met. Report it precisely, run NO GA compute,
         and ESCALATE to the user (escalation #1) — lifting the ban and authorizing GA
         compute is the user's call, never this leg's or the DM's, exactly as leg 59's own
         precedent established. Note explicitly that this does NOT reopen stage B, which leg
         126 closed on the search space independent of the fitness; a pass here informs the
         user's still-open ruling on what follows B's exhaustion, it does not resolve it.
  no  -> Report which properties still fail and by how much, and specifically whether P3
         moved AT ALL (leg 59's own diagnostic). A third failure of a fitness-repair attempt,
         after two wall/parameter repairs failed, is itself informative: bank it as evidence
         that a linear-defect-tracking fitness may be structurally incompatible with this
         operator, not merely under-tuned.
**Territory.** solver/weight_search.py (read-only unless the yes-branch's report requires a
               new fitness function definition to be added as code — if so, append-only, new
               function, existing functions untouched), experiments/p2_route_wvr_v1_fitness.py,
               experiments/p2_route_wvr_v1_fitness_evidence.py,
               writeup/data/p2_route_wvr_v1_fitness.json,
               writeup/novelty/leg_160.md, experiments/journal/leg_160.md.
               NO GA compute of any kind runs under this leg, on either branch — the gate is
               exactly the six-property check, nothing else.
**Difficulty.** heavy
**Independence.** Reads/appends solver/weight_search.py; no other live or reserve leg claims
it (59's territory closed on landing). Touches no certificate term, no literature ledger, no
target ledger, no GA/ga_search.py code path. Independent of 157/158/159 (literature, not
fitness construction) and of 127/125 (different open questions entirely).
```

```
### 161 — ROUTE-LSS: DOES LUSHNIKOV-SILANTYEV-SIEGEL arXiv:2010.01201 ACCOUNT FOR
alpha(1/2)=3 AND THE a_c BOUNDARY? (user-review action item #2)
**Thesis.** LSS arXiv:2010.01201 is cited four times in this repository, always secondhand —
via ALS's and Xu's references to it as "the reference branch" for `a_c` — and never read at
full text. Two separately-banked findings sit downstream of it without ever having checked
the primary source: (i) `alpha(1/2)=3` (PHASE2_P2_NOTES J-3, currently attributed to
integrating ALS eq. 49-50 directly, "cold, no shared grid, basis or code"); (ii)
`a_c=0.6890665` (`solver/literature_gates.py`'s existing row, sourced via Xu Table 1 /
ALS/LSS, with this repository's own instrument measured 0.7% off — "the worst of three
sources," per PHASE2_P2_NOTES J-8). The review flags this as the cheapest, highest-value read
on the board: if LSS's own exact `a=1/2` solution independently derives either or both
numbers, that reclassifies two "independently confirmed, no shared code" coincidences into
one shared-ancestor fact, which changes what any writeup should claim about their
independence — a citation-depth correction in the shape of leg 65/112/113, not a new
computation.
**Gate.** Does LSS arXiv:2010.01201's own exact `a=1/2` solution (read at full text, not via
ALS's or Xu's secondary citation) explicitly contain, derive, or trivially imply (a) the
`alpha(1/2)=3` scaling exponent, and/or (b) the `a_c=0.6890665` boundary value, with
hypotheses recorded verbatim?
  yes -> Record the exact derivation and page/section reference for whichever number(s) LSS
         accounts for directly. Upgrade `solver/literature_gates.py`'s existing LSS row from
         secondary-source to primary-source-read (append-only edit to that one row). This
         downgrades the "independently confirmed" framing for whichever finding(s) LSS
         explains — flag for the leg-58-bundle writeup (action item #6) to reflect precisely,
         do not silently reword any other file.
  no  -> LSS's own text does not account for either number directly; both stay independently
         confirmed as this repository's own re-derivations, strengthened rather than weakened
         by having actually checked the primary alleged source and ruled it out. Bank the
         ledger entry; upgrade the citation row's provenance note regardless (primary-source
         read now, whatever it says).
**Territory.** solver/literature_gates.py (append-only, LSS's existing row ONLY — no other
               row touched), experiments/p2_route_lss_v1_lit.py,
               writeup/data/p2_route_lss_v1_lit.json,
               writeup/novelty/leg_161.md, experiments/journal/leg_161.md
**Difficulty.** light
**Independence.** Literature-only plus one append-only row edit. Disjoint from 145 (reads
literature_gates.py, edits nothing) and from 62/112/113/157/158/159 (different papers,
different questions). No solver-module compute.
```

```
### 162 — ROUTE-CAPG: THE UNTRIED GEOMETRIC-WEIGHT / COMPACT-SUPPORT CAP CORNER, TESTED
AGAINST LEG 126's AUDIT AND LEG 58's A21=0 THEOREM (user-review action item #3)
**Thesis.** Every certificate corner this repository has killed (legs 49, 52, 53, 54, 56, 58,
59, 111, and leg 126's completeness audit over all of them) worked in a compactified WHOLE-
LINE representation with algebraic weights. HTW arXiv:2603.25104 proves compact support for
the `a=1` (De Gregorio) profile with `c_omega/c_l > 0`, in a GLOBAL spectral (Chebyshev)
basis on the finite interval its support occupies — a narrower, structurally different corner
than "compactified whole line, algebraic weight," and the review's own independent check
found no record of this repository ever having tried it. Two honest outcomes, both valuable:
either (a) this is a real corner outside what leg 126 declared covered (1,686 configurations,
zero uncovered, over the space/split/shape enumeration `certificate_shapes.py` supplies) —
in which case leg 126's completeness claim needs a scope correction — or (b) building and
testing it lands inside leg 58's `A21=0` theorem or leg 126's measured-battery coverage after
all, which is a clean, independent strengthening of B's closure rather than a gap in it.
Construction only, no dynamics: builds the compact-support/Chebyshev-basis certificate object
explicitly per HTW's stated construction and measures its `Z_1` the same way leg 54's battery
measured every other shape. **No GA compute under any outcome** — if the corner's free
parameters (support radius, weight exponent) need a search, it is a deterministic grid over a
pre-named range, the leg 46/59 precedent, never an evolutionary search; the GA ban is
untouched regardless of this leg's outcome.
**Gate.** (a) Is the compact-support/Chebyshev-basis corner already inside the
space/split/shape enumeration leg 126 audited as complete (checked explicitly against
`certificate_shapes.py`'s enumeration and leg 126's own JSON), and (b) when built and
measured directly, does its `Z_1` fall under, at, or over 1?
  yes, uncovered by 126 -> Name the exact enumeration gap (which of space/split/shape it
         falls outside) and report the measured `Z_1`. If `Z_1 < 1` this is escalation #4 (a
         banked completeness claim reversed) — push, park, do not merge, list under NEEDS
         YOU. If `Z_1 >= 1` still, it closes on measurement, extending 126's declared
         coverage rather than contradicting it — bank both the gap and the result.
  yes, covered by 126, Z_1 >= 1 -> Clean independent confirmation; leg 126's completeness
         claim is now cross-checked by direct construction, not enumeration alone. Bank it.
  no (construction fails / degenerate) -> Report exactly which step of HTW's construction
         does not transfer to this operator and why; bank as a characterized negative, same
         discipline as every other dead corner in this file.
**Territory.** solver/compact_cap_cheb.py (NEW, capabilities.py grepped first per the
               standing ban), test_compact_cap_cheb.py (NEW),
               experiments/p2_route_capg_v1_corner.py,
               experiments/p2_route_capg_v1_corner_evidence.py,
               writeup/data/p2_route_capg_v1_corner.json,
               writeup/novelty/leg_162.md, experiments/journal/leg_162.md.
               Reads (never edits) solver/certificate_shapes.py and leg 126's banked JSON to
               classify coverage.
**Difficulty.** heavy
**Independence.** Sole owner of a brand-new module. Read-only overlap with
`certificate_shapes.py` (146's territory, also read-only there) and leg 126's banked JSON
(already landed, closed) is read-read on both counts, not a collision. Disjoint from
127/NGX (mathematics on the `A21 != 0` class in the existing whole-line representation, not a
new basis) and from 157/158/159/161 (literature, not construction). No GA compute under any
outcome.
```

```
### 163 — ROUTE-H2S: ORIGIN-H² CERTIFICATE FEASIBILITY SCOPING (UNBLOCKED 2026-08-06 — leg
127's dedicated verifier CONFIRMED the theorem, the proof, the numerics, and the Xu
arXiv:2607.19762 citation; immediately dispatchable)
**Thesis.** No longer contingent: leg 127's full-treatment verifier independently re-derived
the proof and re-computed the numerics from scratch, matching the banked JSON digit-for-digit
(local slopes converge monotonically to `1-s` out to `M=4096`), and confirmed Xu
arXiv:2607.19762 is a real citation, same operator, same profile, genuinely proving origin-H²
invertibility with a spectral gap of 1/2 after modulation. (One small, unrelated side-finding
gap — a wrong claim about a singular sequence's far-field-amplitude component, actually 6.5%
of the norm and growing with `M`, not exactly zero — is being corrected by a bench-repair the
orchestrator dispatched; it does not touch the theorem, which the verifier separately
confirmed via bordered/unbordered `sigma_min` agreement to 5.7e-15, and this leg does not
depend on it either way.) So: `Z_1 >= 1` is confirmed proved for every bounded `A` on the
`ell^1_w` space (superseding leg 58), AND the same bordered `a=0` CLM linearization is
confirmed invertible on origin-H² — meaning this repository's ~70-leg obstruction is a
property of the certificate machinery's CHOSEN space, not of the operator, and the obvious
next question is whether a certificate attempt in origin-H² itself is even structurally
possible before anyone spends a leg building one. This leg still does NOT build a
certificate — it is a SCOPING leg only, mirroring leg 111's third-realization-scoping
template: enumerate what a
certificate in origin-H² would need (a bordered operator formulation compatible with Xu's
own realization, an analogous three degrees of freedom — space is fixed by definition here,
so SPLIT and SHAPE — and any norm/embedding infrastructure this repository's existing
`holder_norms.py`/`hilbert_pointwise.py`/`op_lower.py` machinery does or does not already
cover), and name any KNOWN obstruction analogous to `ell^1_w`'s (does origin-H²'s own
spectral-gap structure impose a floor the way `ell^1_w`'s diagonal-zero structure did, per
Xu's own text, which leg 127 already read once for the invertibility citation and should be
re-read here for what it says about the gap's own limitations).
**Gate.** Does origin-H² admit a structurally viable certificate formulation — i.e., does Xu's
own text (or this repository's existing norm/embedding infrastructure) supply, or straightforwardly
adapt to, a split and shape analogous to what `ell^1_w`'s stage B needed, with no KNOWN
obstruction of the same class as the one that killed every `ell^1_w` attempt?
  yes -> A structurally viable certificate attempt exists in origin-H². Name the required
         infrastructure precisely (what's reusable vs. what's new) and ESCALATE as a genuine
         new research direction for the user — do not build anything under this leg's own
         authority; a construction attempt is a separate, later leg's work, contingent on the
         user's ruling the way leg 63/125's dissipative direction was.
  no  -> Name the specific structural obstruction (spectral-gap-imposed floor, missing
         embedding infrastructure, or incompatible bordering) that closes this direction
         before a construction leg would even be worth drafting. Bank it as a scoped negative
         — the origin-H² space is invertible for the OPERATOR per Xu, which does not by
         itself imply a certificate is buildable there.
**Territory.** experiments/p2_route_h2s_v1_scoping.py,
               writeup/data/p2_route_h2s_v1_scoping.json,
               writeup/novelty/leg_163.md, experiments/journal/leg_163.md.
               Reads (never edits) solver/spectral_certificate.py (127's territory, closed on
               landing), solver/holder_norms.py, solver/hilbert_pointwise.py,
               solver/op_lower.py, and Xu arXiv:2607.19762 itself. No new solver module; no
               certificate is built or measured under this leg.
**Difficulty.** standard
**Independence.** Literature-plus-scoping only, no compute, no new solver module.
**Immediately dispatchable — leg 127's verifier confirmed both the proof and the Xu
citation on 2026-08-06.** Disjoint from every other live/reserve leg's territory, including
the in-flight bench-repair on leg 127's unrelated side-finding (that repair touches
`writeup/` prose about the far-field-amplitude claim only, not `solver/spectral_certificate.py`
or Xu's citation, so it does not block this leg).
```

```
### 164 — ROUTE-CSD: DOES THE a=0 CLM LINEARIZATION ADMIT A COMPACT-SUPPORT REPRESENTATION
AT ALL? (resolves leg 162's ambiguity independently; user-facing PROGRESS.md item 0's
companion, not a ruling on it)
**Thesis.** Leg 162 built the untried compact-support/Chebyshev certificate corner and found
it (a) uncovered by leg 126's 3-value realization axis and (b) measures `Z_1 < 1`
(0.2737/0.0874) when built directly — but flagged this as honestly ambiguous, since leg 126's
audit was written on the `a=0` CLM LINEARIZATION, which (per leg 162's own report) has no
compact-support interval at all. This leg does NOT rule on whether leg 162's finding stands
— it answers the narrower, decidable question underneath the ambiguity: does the `a=0` CLM
linearization, as actually defined in this repository's own certificate machinery (the object
leg 58/127's theorem and leg 126's audit are both about), admit ANY compact-support
representation under any change of basis/variable this repository's own definitions permit —
or is the linearization's domain structurally whole-line/unbounded, making leg 162's corner
inapplicable to the banked object by construction? This is definitional, not a search: read
the linearization's own construction (wherever it lives in `solver/`) and leg 162's own
construction side by side.
**Gate.** Does the `a=0` CLM linearization, as defined in this repository's certificate
machinery, admit a compact-support representation under any basis change consistent with its
own defining equations?
  yes -> Leg 162's corner IS applicable to the banked object after all, sharpening the
         ambiguity toward "genuine gap" — ESCALATE this finding to the user alongside leg
         162's own parked branch, since it strengthens rather than resolves item 0.
  no  -> The linearization is structurally whole-line/unbounded by construction; leg 162's
         corner tests a DIFFERENT object, not the one leg 126's audit and leg 58/127's
         theorem cover. This resolves the ambiguity without a user ruling: leg 126's
         completeness claim stands as scoped, and leg 162's corner is a genuinely separate
         (and still independently interesting, per leg 162's own measured `Z_1<1`) question
         about a related but distinct construction. Report this precisely; do not overwrite
         leg 162's own report, which stays parked and visible either way.
**Territory.** experiments/p2_route_csd_v1_definitional.py,
               writeup/data/p2_route_csd_v1_definitional.json,
               writeup/novelty/leg_164.md, experiments/journal/leg_164.md.
               Reads (never edits) the `a=0` CLM linearization's defining code (wherever it
               lives — `solver/gclm.py`/`solver/target_norm.py`/`solver/spectral_certificate.py`,
               located by the leg itself, read-only) and leg 162's own
               `p2_route_capg_v1_corner.py`/JSON, read-only.
**Difficulty.** standard
**Independence.** Read-only across every file it touches; edits nothing under either outcome.
Does not touch leg 162's parked branch (`leg/162-capg-v1`) or overwrite its report. Disjoint
from 165/171 (different questions) and from 163 (origin-H², a different space entirely, not
the compact-support question). Immediately dispatchable.
```

```
### 165 — ROUTE-SDM: SPACE-VS-OPERATOR MAPPING ACROSS EVERY REALIZATION THIS REPOSITORY HAS
CALLED DEAD
**Thesis.** Leg 127 proved something with a consequence broader than its own headline: "the
operator is bad" and "this SPACE is bad for the operator" are genuinely different claims, and
this repository's ~70-leg `ell^1_w` obstruction turned out to be the latter, not the former.
That retroactively reopens a classification question about every OTHER realization this
repository has banked as dead: legs 52 (space choice for stage B), 53 (split choice), 56
(collocation-basis L1 death), 111/141 (weighted-energy realization, zero-width window). For
each, using ONLY banked data (no new dynamics, no new certificate construction): does the
landed "dead" finding depend on the specific space/basis/realization chosen, or does it
survive across every realization this repository has actually tried (making it closer to an
operator-level fact)? This is a synthesis question leg 127 makes newly answerable, not a
repeat of any landed audit.
**Gate.** For each of legs 52, 53, 56, 111/141's dead findings, does the repository's own
banked record contain evidence the finding is REALIZATION-DEPENDENT (i.e., a different
choice within the same degree of freedom, already tried elsewhere in the banked record,
behaves differently), or does every tried realization agree?
  yes (at least one is realization-dependent) -> Name it precisely, with the banked evidence
         for both realizations side by side. This is a genuinely novel synthesis finding —
         ESCALATE as a candidate companion to leg 127's own reframing, not a ban-lifting
         result on its own.
  no (all four are realization-invariant across every tried case) -> Report this as
         strengthening, not weakening, the "operator-level" reading of this repository's
         other dead findings — 127's reframing was specific to the `ell^1_w`/stage-B
         obstruction, not a general pattern. Bank the classification.
**Territory.** experiments/p2_route_sdm_v1_mapping.py,
               writeup/data/p2_route_sdm_v1_mapping.json,
               writeup/novelty/leg_165.md, experiments/journal/leg_165.md.
               Reads banked JSONs from legs 52, 53, 56, 58, 111, 127, 141 only; no solver
               module, no new compute.
**Difficulty.** standard
**Independence.** Read-only, no solver module. Disjoint from 164 (definitional question about
one specific object) and 171 (a specific paper's content, not a synthesis across this
repository's own banked record). Immediately dispatchable.
```

```
### 166 — ROUTE-CNB: POST-REPAIR REGRESSION CHECK, collocation_newton.py (closes leg 150)
**Thesis.** Leg 150 (CNR) repaired the 8 silent-corruption cases across 3 mechanisms leg 114
found; no independent regression check has run since, per the
86/87/94/103/104/105/131–135/147 pattern this repository uses for every repair.
**Gate.** Post-repair, does solver/collocation_newton.py (a) reject or correctly flag every
one of leg 114's original 8 failing cases in an independent re-run, and (b) reproduce leg
110's death-certificate reproduction and every other previously-validated result
bit-identically?
  yes -> Repair confirmed solid and non-regressive by an independent run. Bank leg 114's
         battery as a permanent regression suite.
  no  -> An incomplete fix or a repair regression. Report the exact case precisely; escalate
         as a priority finding, do not patch under this leg's own authority.
**Territory.** test_collocation_newton_postrepair.py,
               experiments/p2_route_cnb_v1_postrepair.py,
               writeup/data/p2_route_cnb_v1_postrepair.json,
               writeup/novelty/leg_166.md, experiments/journal/leg_166.md
**Difficulty.** standard
**Independence.** Reads solver/collocation_newton.py; edits nothing under either outcome.
Module unowned since leg 150 landed. Immediately dispatchable.
```

```
### 167 — ROUTE-DCB: POST-REPAIR REGRESSION CHECK, decay_collocation.py (closes leg 151)
**Thesis.** Leg 151 (DCR) repaired the 3 silent-corruption gaps leg 115 found; no independent
regression check has run since.
**Gate.** Post-repair, does solver/decay_collocation.py (a) reject or correctly flag every one
of leg 115's original 3 failing cases in an independent re-run, and (b) reproduce every
previously-validated result bit-identically?
  yes -> Repair confirmed solid and non-regressive. Bank leg 115's battery as a permanent
         regression suite.
  no  -> An incomplete fix or a repair regression. Report the exact case precisely; escalate
         as a priority finding, do not patch under this leg's own authority.
**Territory.** test_decay_collocation_postrepair.py,
               experiments/p2_route_dcb_v1_postrepair.py,
               writeup/data/p2_route_dcb_v1_postrepair.json,
               writeup/novelty/leg_167.md, experiments/journal/leg_167.md
**Difficulty.** standard
**Independence.** Reads solver/decay_collocation.py; edits nothing under either outcome.
Module unowned since leg 151 landed. Immediately dispatchable.
```

```
### 168 — ROUTE-HRB: POST-REPAIR REGRESSION CHECK, hl_rescaled.py (closes leg 152)
**Thesis.** Leg 152 (HRR) repaired the 4 silent-corruption mechanisms leg 117 found (with one
clause — the IEEE-754 NaN-comparison blind spot in RescaledHL's own ascending guard —
possibly documented rather than patched, per 152's own stated option). No independent
regression check has run since.
**Gate.** Post-repair, does solver/hl_rescaled.py (a) reject or correctly flag every one of
leg 117's original failing configurations (per whichever clauses leg 152 actually patched,
checked against its own report), and (b) reproduce every previously-validated result
bit-identically?
  yes -> Repair confirmed solid and non-regressive. Bank leg 117's battery as a permanent
         regression suite.
  no  -> An incomplete fix or a repair regression. Report the exact case precisely; escalate
         as a priority finding, do not patch under this leg's own authority.
**Territory.** test_hl_rescaled_postrepair.py, experiments/p2_route_hrb_v1_postrepair.py,
               writeup/data/p2_route_hrb_v1_postrepair.json,
               writeup/novelty/leg_168.md, experiments/journal/leg_168.md
**Difficulty.** standard
**Independence.** Reads solver/hl_rescaled.py; edits nothing under either outcome. Module
unowned since leg 152 landed. Immediately dispatchable.
```

```
### 169 — ROUTE-HHB: POST-REPAIR REGRESSION CHECK, hilbert_holder.py (RESERVE — NOT
dispatchable until leg 153/HHR lands)
**Thesis.** Leg 153 (HHR) is repairing the bound-direction violation leg 119 found. Drafted
now, ready the moment it lands, per the same close-the-loop discipline as every other repair
in this run.
**Gate.** Post-repair, does solver/hilbert_holder.py (a) either raise on leg 119's failing
configuration or provably dominate the true value there, and (b) reproduce every
previously-validated result bit-identically?
  yes -> Repair confirmed solid and non-regressive. Bank leg 119's battery as a permanent
         regression suite.
  no  -> An incomplete fix or a repair regression. Report the exact case and magnitudes;
         escalate as a priority finding, do not patch under this leg's own authority.
**Territory.** test_hilbert_holder_postrepair.py, experiments/p2_route_hhb_v1_postrepair.py,
               writeup/data/p2_route_hhb_v1_postrepair.json,
               writeup/novelty/leg_169.md, experiments/journal/leg_169.md
**Difficulty.** standard
**Independence.** Reads solver/hilbert_holder.py; edits nothing under either outcome. **NOT
dispatchable until leg 153 lands.**
```

```
### 170 — ROUTE-CDB: POST-REPAIR REGRESSION CHECK, critical_dissipation.py (RESERVE — NOT
dispatchable until leg 154/CDR lands)
**Thesis.** Leg 154 (CDR) is repairing the non-integer-exponent truncation leg 121 found.
Drafted now, ready the moment it lands.
**Gate.** Post-repair, does solver/critical_dissipation.py (a) reject or visibly flag every
non-integer `p (2s)` case in leg 121's battery, and (b) reproduce every previously-validated
integer-`p` result bit-identically?
  yes -> Repair confirmed solid and non-regressive. Bank leg 121's battery as a permanent
         regression suite.
  no  -> An incomplete fix or a repair regression. Report the exact case and magnitudes;
         escalate as a priority finding, do not patch under this leg's own authority.
**Territory.** test_critical_dissipation_postrepair.py,
               experiments/p2_route_cdb_v1_postrepair.py,
               writeup/data/p2_route_cdb_v1_postrepair.json,
               writeup/novelty/leg_170.md, experiments/journal/leg_170.md
**Difficulty.** standard
**Independence.** Reads solver/critical_dissipation.py; edits nothing under either outcome.
**NOT dispatchable until leg 154 lands.**
```

```
### 171 — ROUTE-XUL: DOES Xu arXiv:2607.19762 CHARACTERIZE ANY OTHER SPACE'S
CERTIFICATE-BUILDABILITY, BEYOND THE ORIGIN-H² INVERTIBILITY CITATION?
**Thesis.** Legs 127 and 163 have so far mined Xu arXiv:2607.19762 for exactly one fact: the
bordered `a=0` CLM linearization is invertible on origin-H² with spectral gap 1/2. Xu's paper
is already fully accessed (no new literature-search cost) and was never asked the broader
question: does it characterize, for THIS operator class, which OTHER function spaces admit
or forbid invertibility/a certificate — a map of the space-dependence terrain 127 only sampled
at two points (`ell^1_w`: dead; origin-H²: alive), which would directly extend leg 163's
scoping work and leg 165's synthesis question.
**Gate.** Does Xu arXiv:2607.19762, at full-text depth, characterize the operator's
invertibility or certificate-buildability on any space OTHER than origin-H² and `ell^1_w`
(explicitly, or as a derivable corollary of a stated general theorem)?
  yes -> Record every additional space and its verdict, verbatim with hypotheses. ESCALATE
         as directly informing leg 163's scoping and leg 165's synthesis — do not build or
         test anything under this leg's own authority.
  no  -> Xu's paper is confirmed to speak only to the two points already used. Bank the
         ledger entry; leg 163's scoping work stands as the frontier on this question.
**Territory.** experiments/p2_route_xul_v1_lit.py, writeup/data/p2_route_xul_v1_lit.json,
               writeup/novelty/leg_171.md, experiments/journal/leg_171.md.
               Does NOT edit solver/literature_gates.py or solver/spectral_certificate.py.
**Difficulty.** light
**Independence.** Literature-only, own JSON, no solver module. Disjoint from 163 (scoping,
not literature mining) and from 157/158/159/161 (different papers). Immediately
dispatchable.
```

```
### 172 — ROUTE-W2L: HAS VALIDATED/INTERVAL NUMERICS EVER CERTIFIED A GENUINELY 3D PDE
SINGULARITY, IN ANY FIELD? (user question on Wall 2; literature-only, does not touch the odds)
**Thesis.** The user asked, in substance, whether Wall 2 (validated/interval-numerics
technology today works only on 1D/2D models; 3D NS is out of reach, per `CLAY_ROADMAP.md`
and `plan_of_record.py`) is a property of THIS repository's approach or of the field as a
whole. This repository's own EXT-family freshness legs (74, 77, 82, 90, 93, 123) have
repeatedly checked "has anyone certified THIS repository's specific target object," which is
narrower than "has the TECHNIQUE ever reached a genuinely 3D object, in any field, on any
problem" — climate/combustion/celestial-mechanics ODEs (Tucker's Lorenz proof is 3D but an
ODE, not a PDE) and other computer-assisted-proof traditions have not been surveyed by any
landed leg. This is the honest way to confirm or correct this DM's own working assessment
(stated to the user via the orchestrator: no known rigorous computer-assisted blow-up
certificate exists for any genuinely 3D PDE, based on general knowledge of the field and this
repository's own repeated literature passes finding nothing) rather than assert it from
memory. Scope guard, stated up front and binding: **this leg's outcome does not change the
~0.05% odds assessment or claim any movement toward Clay under either branch** — it answers
a scoping question about where the technology's frontier actually is, which only matters for
deciding whether a FUTURE leg on a genuine 3D reduction (see the DM's own note in Status
about the 2D-Boussinesq / axisymmetric-swirl-free-3D-Euler exact correspondence) would be
worth anyone's time.
**Gate.** Does any published work — in fluid dynamics, PDE theory, or any other
computer-assisted-proof tradition — establish a rigorous (interval-arithmetic, validated
numerics, or otherwise machine-certified) singularity/blow-up result for a genuinely 3D PDE
model (not an ODE, not a 1D/2D reduction)?
  yes -> Record the citation, its hypotheses, and exactly what technique it uses, verbatim.
         This would be the single most consequential literature finding this repository could
         produce for informing (never determining) future direction — ESCALATE to the user;
         do not build or attempt to replicate it under this leg's own authority.
  no  -> Wall 2 is confirmed field-wide, not an artifact of this repository's narrower
         literature scope. Bank the ledger entry. The odds assessment does not move either
         way — this closes a scoping question, not a chain link.
**Territory.** experiments/p2_route_w2l_v1_lit.py, writeup/data/p2_route_w2l_v1_lit.json,
               writeup/novelty/leg_172.md, experiments/journal/leg_172.md.
               Does NOT edit solver/literature_gates.py, `plan_of_record.py`, or
               `CLAY_ROADMAP.md`.
**Difficulty.** light
**Independence.** Literature-only, own JSON, no solver module, no ban touched. Disjoint from
every other live/reserve leg. Immediately dispatchable.
```

```
### 173 — ROUTE-XUM: SCOPING Xu arXiv:2607.19762's OWN CERTIFICATION METHOD AS A DIFFERENT
LANE FROM THE ell^1-FOURIER APPROACH (user-review action item, Part 2 #1; light, scoping
first)
**Thesis.** Every use of Xu arXiv:2607.19762 so far (legs 127, 163, and reserve leg 171) has
mined it for CITATIONS — the origin-H² invertibility fact, and (via 171) whatever other
spaces it characterizes. None has scoped Xu's own certification METHOD, which per the user's
own framing (uniform large-imaginary-part bounds, trace-ideal membership, quadrature error in
trace norm) is methodologically distinct from the `ell^1`-Fourier/radii-polynomial machinery
this repository built stage B's entire certificate infrastructure around and spent ~70 legs
measuring dead in that one lane. This leg does NOT attempt to build a certificate — it reads
Xu's method at full-text depth and catalogs, precisely: what each named technique actually
does, what mathematical/numerical infrastructure it requires that this repository's own
`solver/` code does or does not already have (compare against `holder_norms.py`,
`hilbert_pointwise.py`, `op_lower.py`, `spectral_certificate.py`'s existing capabilities), and
what "maturing by orders of magnitude" concretely means here — is the gap in precision
(quadrature error bounds too loose by some measured factor), in scope (proven for a narrower
operator class than needed), or in infrastructure (techniques exist on paper but no
implementation anywhere)?
**Gate.** Does Xu's certification method, as stated in the paper, already reach — or come
within a scopeable, quantifiable distance of — a working certificate for the operator class
this repository's own certificate work targets, using only techniques the paper itself
states (no new mathematics invented under this leg)?
  yes (or "within a stated, quantifiable distance") -> Name the exact remaining gap precisely
         (a number, a missing lemma, a computational scale) and ESCALATE as a candidate new
         construction lane for the user — do not attempt the construction under this leg's
         own authority; that is a separate, heavier leg, contingent on this scoping.
  no (the gap is not quantifiable from the paper alone, or is structurally large) -> Report
         exactly which technique is farthest from usable and why. Bank this as a characterized
         negative on the "different lane" question — the paper's method exists but is not
         close to a working certificate by any measure this leg can establish.
**Territory.** experiments/p2_route_xum_v1_scoping.py,
               writeup/data/p2_route_xum_v1_scoping.json,
               writeup/novelty/leg_173.md, experiments/journal/leg_173.md.
               Reads (never edits) solver/holder_norms.py, solver/hilbert_pointwise.py,
               solver/op_lower.py, solver/spectral_certificate.py (127's territory, closed on
               landing) for infrastructure comparison only.
**Difficulty.** light
**Independence.** Literature-plus-comparison only, no compute, no new solver module. Disjoint
from 171 (XUL, different-spaces coverage question, not method scoping) and from 163 (H2S,
origin-H² feasibility, a different space-scoping question). Immediately dispatchable.
```

```
### 174 — ROUTE-VBS: VISCOUS CERTIFIED BLOW-UP SCOPING — SHARPENING "THE MISSING RUNG"
AGAINST WHAT'S ALREADY BANKED (user-review action item, Part 2 #2; light, scoping first)
**Thesis.** The user's framing ("a viscous certified blow-up in any model — that's the
missing rung") needs sharpening against what this repository's own literature ledger already
contains, not treated as a blank-slate question: `arXiv:2410.05480` (Dahne-Figueras)
interval-verifies self-similar singular CGL profiles continued in a dissipation parameter
`epsilon` — re-derived independently by this repository's own leg 48/Route-V to 1.8e-07 —
which is precisely what closed stage V for non-novelty. Whether that constitutes "a viscous
certified blow-up in any model" already, or falls short of it in some specific way (e.g.
branch verification without a completed blow-up argument, or a model too far from
fluid/vortex dynamics to count), has never been asked directly — stage V's leg only asked
whether it PRE-EMPTED this repository's own margin-continuation question, not whether it
answers the user's broader one. Separately: **leg 125 (M2P), already dispatch-ready per this
DM's own prior correction, is this repository's live attempt at a certified viscous blow-up
on Chen's γ=2 dissipative gCLM** — a fluid/vortex-dynamics-adjacent model, unlike CGL. This
leg does not duplicate 125's construction work; it (a) settles the CGL definitional question
precisely, and (b) catalogs any OTHER published viscous fluid-adjacent model with an existing
analytic (uncertified) blow-up proof, as a fallback list if leg 125's own attempt does not
close.
**Gate.** (a) Does `arXiv:2410.05480`'s interval-verified CGL branch work constitute a
completed certified blow-up (not merely a certified profile/branch short of the blow-up
argument itself), and (b) does the published literature contain any OTHER viscous
fluid/vortex-dynamics-adjacent model (beyond Chen's γ=2 gCLM) with an existing analytic
blow-up proof that has never been computer-certified?
  yes on (a) -> The "missing rung" already has an occupant, just not in a fluid-adjacent
         model — report this precisely; it reframes but does not retract the user's point
         (fluid dynamics specifically still lacks one). ESCALATE the reframing to the user.
  no on (a) -> CGL's branch work falls short of a completed certified blow-up in a specific,
         named way. Report exactly what is missing; this confirms the rung is genuinely
         empty, strengthening leg 125's priority.
  For (b): report every candidate found, with its own analytic proof's citation, regardless
         of (a)'s answer — this is the fallback catalog either way. Bank it; escalate nothing
         on its own (a catalog is not a claim).
**Territory.** experiments/p2_route_vbs_v1_scoping.py,
               writeup/data/p2_route_vbs_v1_scoping.json,
               writeup/novelty/leg_174.md, experiments/journal/leg_174.md.
               Reads (never edits) solver/viscous_novelty.py's existing PRECEDENTS ledger and
               `LITERATURE_CHECK.md`; does not touch leg 125's territory
               (`solver/target_selection.py`) or presuppose its outcome.
**Difficulty.** light
**Independence.** Literature-only, own JSON, no solver module. Disjoint from leg 125 (reads
its context only, builds nothing, does not block or depend on its dispatch) and from
157/158/159/161/171/173 (different papers/questions). Immediately dispatchable.
```

```
### 175 — ROUTE-USC: arXiv:2509.14185 AT FULL-TEXT DEPTH — WHAT "ONE MODEL CLASS AWAY" FROM
A CAP-READY CERTIFICATE ACTUALLY REQUIRES (user-review action item, Part 2 #3; light,
scoping first)
**Thesis.** `arXiv:2509.14185` (Wang, Lai, Gomez-Serrano, Buckmaster et al.) is in this
repository's ledger (`solver/viscous_novelty.py::PRECEDENTS`, `LITERATURE_CHECK.md`) as a
one-line EXCLUSION row: "unstable self-similar singularities for IPM and 3D Euler with
boundary, CAP-ready precision, inviscid, no certificate claimed." It has never been read at
full-text depth for its actual method or its own stated obstruction to certification.
**Correction to the coordinator's framing, checked directly against this repository's own
`LITERATURE_CHECK.md`: the banked re-derivation numbers (1.8e-07, 3.0e-06/1.9e-06 rms,
3.8e-07) belong to `arXiv:2410.05480`'s CGL branches, NOT to `2509.14185`** — this repository
has no independent re-derivation of `2509.14185`'s numerics on file, so this leg's first job
is establishing what is actually known about it from scratch, not assuming prior
verification exists. The user's framing — "still one model class away" — is the question:
read the paper's own stated obstruction (if any) to turning its CAP-ready numerics into an
actual certificate, and determine whether that obstruction is MODEL-specific (the same
technique, applied to IPM or 3D Euler with boundary specifically, hits a wall a different but
related model wouldn't) or TECHNIQUE-specific (CAP itself needs independent maturation
regardless of model, the same shape of gap leg 173 scopes for Xu's method).
**Gate.** Does `arXiv:2509.14185`'s own text state, imply, or make locatable an obstruction to
certifying its CAP-ready unstable singularities, and is that obstruction MODEL-specific
(naming which alternative model class would avoid it) or TECHNIQUE-specific (a precision or
infrastructure gap independent of model)?
  model-specific -> Name the alternative model class precisely, with the paper's own
         reasoning for why it would or wouldn't face the same obstruction. If that
         alternative model class is one this repository's own infrastructure already touches
         (gCLM/CLM/Boussinesq family), ESCALATE as a candidate new construction lane for the
         user — do not attempt it under this leg's own authority.
  technique-specific -> Report the precision/infrastructure gap precisely, in the same terms
         leg 173 uses for Xu's method, so the two scoping results are comparable. Bank it.
  neither locatable -> The paper does not state its own obstruction explicitly; report what
         CAN be inferred from its stated precision and scope, flagged as inference, not
         quotation, and bank as a partial answer.
**Territory.** experiments/p2_route_usc_v1_scoping.py,
               writeup/data/p2_route_usc_v1_scoping.json,
               writeup/novelty/leg_175.md, experiments/journal/leg_175.md.
               Reads (never edits) solver/viscous_novelty.py's existing PRECEDENTS ledger and
               `LITERATURE_CHECK.md`.
**Difficulty.** light
**Independence.** Literature-only, own JSON, no solver module. Disjoint from 174 (VBS, a
different paper/question, though both read the same PRECEDENTS ledger read-only — read-read,
not a collision) and from every other live/reserve leg. Immediately dispatchable.
```

```
### 176 — ROUTE-H2C: BUILD THE ORIGIN-H² CERTIFICATE AT a=0 (USER-AUTHORIZED CONSTRUCTION,
KNOWN CEILING STATED UP FRONT)
**Thesis.** Leg 163 (H2S) scoped origin-H² as structurally viable for a certificate — an
explicit split, shape, and bordered formulation with no `ell^1_w`-class obstruction,
cross-checked against Xu at residual 2.8e-14 — but flagged that everything usable depends on
`a=0` exactness, which only re-derives a closed form Xu already gives analytically, so
NOTHING TRANSFERS to the real (non-`a=0`) target object. The user has explicitly authorized
building it anyway, ceiling and all. **This leg's own honest ceiling, stated before any
computation, per this repository's standing discipline**: even a complete success is not a
step toward the real target — it is the first constructed (not merely scoped) certificate
outside the `ell^1_w` lane this repository has ever built, valuable as a working example of
the OTHER lane and as infrastructure a later leg on a non-`a=0` extension could reuse or
learn from, not as movement on L1→L4. Build the certificate per leg 163's own scoped
split/shape, using leg 163's report as the construction spec; measure `Z_1` (or whatever
leg-163-scoped diagnostic is the certificate's closing quantity) the same way leg 54's
battery measured every `ell^1_w` shape, so the two lanes' outputs are directly comparable.
**No GA compute** — construction only, deterministic, per the leg 46/59/162 precedent.
**Gate.** Does the origin-H² certificate, built per leg 163's own scoped formulation at
`a=0`, actually close (its diagnostic quantity crosses the threshold a certificate needs), and
does it reproduce Xu's own closed form to the precision leg 163 already established (2.8e-14
class)?
  yes -> The first working non-`ell^1_w` certificate this repository has built. Report the
         magnitudes and the construction precisely, restate the ceiling (no transfer to
         non-`a=0`) in the same breath, and bank it as infrastructure — do not claim Clay
         movement or imply the ceiling has lifted.
  no  -> Report exactly which step of leg 163's scoped construction fails to close and why,
         with magnitudes. This is still informative — it would mean origin-H²'s structural
         viability (leg 163's finding) does not survive contact with an actual construction
         attempt, which matters for anyone considering the same lane later. Bank it as a
         characterized negative.
**Territory.** solver/origin_h2_certificate.py (NEW, capabilities.py grepped first per the
               standing ban), test_origin_h2_certificate.py (NEW),
               experiments/p2_route_h2c_v1_construction.py,
               experiments/p2_route_h2c_v1_construction_evidence.py,
               writeup/data/p2_route_h2c_v1_construction.json,
               writeup/novelty/leg_176.md, experiments/journal/leg_176.md.
               Reads (never edits) leg 163's own report/JSON and
               solver/spectral_certificate.py (127's territory, closed on landing, read-only
               reference for the `ell^1_w`-lane comparison).
**Difficulty.** heavy
**Independence.** Sole owner of a brand-new module. Disjoint from every other live/reserve
leg. No GA compute under any outcome. Immediately dispatchable — the user's authorization is
the only precondition, and it has been given.
```

```
### 177 — ROUTE-L1RH: DOES A NON-ell^1_w SPACE FIX THE COLLOCATION-BASIS L1 DEATH TOO?
(RESERVE — blocked until leg 165's classification report lands)
**Thesis.** Leg 127 proved the coefficient-basis L1 death (leg 54) was a property of the
`ell^1_w` space, not the operator — origin-H² fixes it. L1 has a SECOND death certificate,
in the collocation basis (leg 56), never tested against any alternative space. Drafted now,
blocked on leg 165's classification (does 165 find the collocation death is
realization-dependent or realization-invariant across everything ALREADY tried) so this leg
does not presuppose that answer — but 165 only reads banked data, so even a "realization-
invariant so far" finding would not rule out an entirely untested space like origin-H², which
is exactly what this leg tests directly, once 165's report gives it the right framing to cite.
**Gate.** Does origin-H² (or another space this leg identifies as structurally analogous, per
leg 163's own scoping method) admit a certificate formulation for the collocation-basis
realization of L1, and if built, does its diagnostic close?
  yes -> A second `ell^1_w`-artifact death, doubling the evidence for the space-vs-operator
         reframing. ESCALATE as directly bearing on the publication scoping (leg 179's
         bundle, if not already landed).
  no  -> The collocation death is confirmed NOT a space artifact — it survives on origin-H²
         too (or no analogous space applies). Bank this as strengthening the "some
         obstructions are operator-level" reading leg 165 will have already scoped.
**Territory.** experiments/p2_route_l1rh_v1_construction.py,
               writeup/data/p2_route_l1rh_v1_construction.json,
               writeup/novelty/leg_177.md, experiments/journal/leg_177.md.
               Reads leg 56's and leg 163's own reports/JSONs read-only; new construction (if
               any) goes in a NEW module, capabilities.py grepped first.
**Difficulty.** heavy
**Independence.** New territory if construction is needed; reads only closed/landed legs'
JSONs otherwise. **NOT dispatchable until leg 165 lands.**
```

```
### 178 — ROUTE-WES: DOES A DIFFERENT SPACE SHIFT THE WEIGHTED-ENERGY ZERO-WIDTH WINDOW?
**Thesis.** Leg 111 measured a zero-width window (damping needs gamma>3, the weighted space
exists only for gamma<3) on ONE weighted-energy construction. Leg 141 asked only whether that
specific coincidence is published; leg 165 only classifies using banked data. Neither
attempts a NEW construction. This leg does: following leg 127's playbook directly — the same
operator, a genuinely different space/weight-class than leg 111's — does the coincidence
persist, or is it (like the `ell^1_w` obstruction) a property of leg 111's specific
construction rather than the operator? Pre-name the alternative space/weight-class family in
the driver before any computation, per the leg-111 pre-naming discipline.
**Gate.** For at least one pre-named alternative weighted-energy construction (different from
leg 111's), is the measured coercivity gap positive and grid-stable across two refinements,
outside the gamma>3-needs/gamma<3-exists coincidence?
  yes -> The zero-width window is a construction artifact, not an operator fact — a genuine
         third-realization revival. ESCALATE to the user; do not build further under this
         leg's own authority.
  no  -> The coincidence persists under a second, independently-chosen construction,
         strengthening (not just repeating) leg 111's finding toward an operator-level fact.
         Bank it.
**Territory.** solver/energy_coercivity.py (append-only, new construction added alongside
               leg 111's, existing functions untouched), experiments/p2_route_wes_v1_space.py,
               writeup/data/p2_route_wes_v1_space.json,
               writeup/novelty/leg_178.md, experiments/journal/leg_178.md
**Difficulty.** heavy
**Independence.** Append-only on a module leg 111 (landed, closed) owns solely; no other live
leg touches it. No GA compute. Independent of 165/177 (different degrees of freedom).
Immediately dispatchable.
```

```
### 179 — ROUTE-PUB1: THE COMBINED METHODOLOGICAL NOTE — EXPONENT-SUM CONSERVATION LAW +
DISCRETE-BALL TRAP + THE A21 INEQUALITY (NOW LEG 127's SHARPER FORM) + THE CLOSURE AUDIT
(user-review action item #6, unblocked now that 161/162 have landed)
**Thesis.** The strategic review recommended bundling leg 58's publication scoping as ONE
section of a combined methodological note rather than standalone, deferred until 161 and 162
landed so the note's content wouldn't be written ahead of what they found. Both have landed.
Bundle: (i) the exponent-sum conservation law (leg 65's L1G lane), (ii) the discrete-ball trap
(also leg 65), (iii) the `A21` inequality in its CURRENT, correct form — leg 127's
`Z_1 >= 1` for every bounded `A`, superseding leg 58's narrower `A21=0`-only statement, with
the supersession stated explicitly so nobody reads the note as citing the weaker result — and
(iv) leg 126's closure audit (stage B's declared search space, fully covered). Fold in leg
161's finding on whether LSS accounts for `alpha(1/2)=3`/`a_c`, and leg 162's parked,
ambiguous compact-support corner finding, each exactly as landed, no softening or
strengthening of either. Also corrects leg 157's stale framing (still describing itself as
feeding leg 127's now-closed counterexample search) as a small, explicitly-flagged
housekeeping note within the bundle, not a separate leg.
**Gate.** Does the combined note state all four bundled results (plus 161's and 162's
findings) accurately, with leg 58's superseded status and leg 162's honest ambiguity both
stated explicitly, and does it correct leg 157's stale framing note?
  yes -> Bank the combined note as the current publication-scoping draft; flag it to the user
         as ready for their own review, not as something this leg's landing itself approves.
  no  -> Report exactly which bundled claim doesn't reproduce from its own banked source;
         escalate rather than silently soften it — a publication-scoping note that misstates
         a banked result is exactly the kind of drift this repository's own discipline exists
         to catch.
**Territory.** writeup/4_p2_lottery/TECHNICAL_P2_PUB1_V1.md (NEW),
               writeup/4_p2_lottery/BLOG_P2_PUB1_V1.md (NEW),
               writeup/novelty/leg_179.md, experiments/journal/leg_179.md.
               Reads (never edits under this leg) legs 58/65/126/127/157/161/162's own
               banked JSONs and reports. Corrects leg 157's writeup file's framing note
               ONLY (a sentence-level fix, not a re-litigation of its finding).
**Difficulty.** standard
**Independence.** New writeup files; the one existing-file touch (157's framing note) is a
narrow, explicitly-scoped correction, not a re-opening. Disjoint from every other live/reserve
leg. Immediately dispatchable.
```

```
### 180 — ROUTE-TSR: TWO-SCALE a* SCOPE-LINE CORRECTION (in-repo half of user-review action
item #5, unblocked now that 161/162 have landed)
**Thesis.** The strategic review's own independent check found a domain mismatch, not a wrong
number: published literature (`arXiv:2603.25104`) states the two-scale scenario governs
`a<=0`, while this repository's banked `a*~0.5-0.55` survival boundary was measured at
`a>0`. Deferred until 161/162 landed so this leg's correction could be informed by whatever
either found about the domain's boundaries; neither changed the `a*` finding itself, so the
correction is exactly the one the review specified. Corrects `writeup/` and
`PHASE2_P2_NOTES.md`'s scope-line language to state the domain precisely — re-framing, not
withdrawing, per the review's own instruction. Does NOT touch the user's personal `MEMORY.md`
file (outside any leg's or this DM's file access; the orchestrator relays that correction
directly, as already noted in Status).
**Gate.** Does every `writeup/` and `PHASE2_P2_NOTES.md` passage describing the `a*~0.5-0.55`
survival boundary now state its measured domain (`a>0`) precisely, without asserting or
implying the two-scale SCENARIO (which the literature scopes to `a<=0`) governs it?
  yes -> Bank the corrected scope lines; the `a*` finding itself is untouched, only its
         framing relative to the two-scale literature is sharpened.
  no  -> Report exactly which passage still overclaims; this is a mechanical correction on
         the leg 65 annotation-fix precedent, so a clean pass is expected, but report
         honestly if one is missed.
**Territory.** `writeup/` files describing the two-scale `a*` result (located by this leg,
               grepped for the claim), `PHASE2_P2_NOTES.md` (scope-line sentences only),
               writeup/novelty/leg_180.md, experiments/journal/leg_180.md. No solver module.
**Difficulty.** light
**Independence.** Prose-only, no solver module, no banked number changed. Disjoint from 179
(different files — 179 writes NEW note files, 180 edits EXISTING scope lines). Immediately
dispatchable.
```

```
### 181 — ROUTE-MOD: WHAT DOES XU's "GAP OF 1/2 AFTER MODULATION" ACTUALLY REQUIRE, AND IS
THE MODULATION TECHNIQUE TRANSFERABLE?
**Thesis.** Legs 127/163 use Xu's origin-H² invertibility result but have only ever cited its
headline (gap 1/2 "after modulation") without reading what the modulation technique itself
does. This leg reads it directly: what is being modulated, what does the technique cost
(additional hypotheses, a restricted sub-class, extra computational machinery), and — the
genuinely new question — could the SAME modulation move be applied within the `ell^1_w` line,
where leg 127 proved `Z_1 >= 1` unconditionally (no modulation involved in that proof)? If
modulation is a general technique for improving spectral gaps, it is worth knowing whether it
was even applicable there, even though leg 127's result is already the sharpest possible
UNMODULATED statement.
**Gate.** Does Xu's modulation technique, read at full-text depth, apply (as stated, or via a
straightforward adaptation) to any operator/space combination this repository has already
built, beyond origin-H²?
  yes -> Name the target and what modulation would require precisely. ESCALATE as a
         candidate scoping question for a later leg — do not build or test it here.
  no  -> Modulation is confirmed specific to origin-H²'s own structure (or to a class this
         repository's operator does not fall in for other reasons). Bank the ledger entry.
**Territory.** experiments/p2_route_mod_v1_lit.py, writeup/data/p2_route_mod_v1_lit.json,
               writeup/novelty/leg_181.md, experiments/journal/leg_181.md.
               Reads Xu arXiv:2607.19762 and solver/spectral_certificate.py (127's territory,
               closed on landing, read-only).
**Difficulty.** light
**Independence.** Literature-only plus read-only reference. Disjoint from 171/173 (different
questions about the same paper — 171 asks about OTHER spaces Xu covers, 173 asks about Xu's
certification METHOD generally, this asks specifically about the modulation technique).
Immediately dispatchable.
```

```
### 182 — ROUTE-H2I: IS THERE AN INTERMEDIATE SPACE BETWEEN ell^1_w AND ORIGIN-H² THAT AVOIDS
BOTH OBSTRUCTIONS?
**Thesis.** Two points on the space axis are now mapped: `ell^1_w` is dead unconditionally
(leg 127, `Z_1 >= 1` for every bounded `A`); origin-H² is structurally viable but capped at
`a=0` exactness, re-deriving Xu's own closed form with no transfer to the real target (leg
163). Leg 176 (in flight) is testing whether origin-H² actually closes as a construction, but
even a full success there does not extend past `a=0`. This leg asks the natural next
question, grounded only in what legs 127 and 163 already established (not contingent on
176's or any other in-flight leg's unknown outcome): is there an INTERPOLATING space between
`ell^1_w` and origin-H² — on a standard scale (weighted Sobolev, Besov, or fractional) — that
could avoid BOTH obstructions at once: no `ell^1_w`-class zero-diagonal floor, and no
collapse to requiring `a=0` exactness? Scoping only, per the leg 111/163 precedent: identify
candidate interpolation scales and check for a known obstruction analogous to either dead
end before any construction leg is drafted.
**Gate.** Does any interpolation scale between `ell^1_w` and origin-H² admit a formulation
with (a) no `ell^1_w`-class zero-diagonal floor (checked against leg 127's own proof
technique — does it generalize to the interpolated space, weakening or vanishing), and (b) no
structural requirement of `a=0` exactness (checked against what specifically forces that
requirement in leg 163's construction)?
  yes -> Name the specific scale and point precisely, with both checks' reasoning. ESCALATE
         as a candidate construction leg for the user — do not build under this leg's own
         authority.
  no  -> Report exactly which check fails for every candidate scale considered, and why. Bank
         this as closing the interpolation-space question — the space axis's only two
         tractable points are the ones already mapped.
**Territory.** experiments/p2_route_h2i_v1_scoping.py, writeup/data/p2_route_h2i_v1_scoping.json,
               writeup/novelty/leg_182.md, experiments/journal/leg_182.md.
               Reads (never edits) legs 127's and 163's own reports/JSONs, read-only. No new
               solver module; no certificate is built under this leg.
**Difficulty.** standard
**Independence.** Literature-plus-scoping only, no compute, no new solver module. Disjoint
from 176 (construction, not scoping) and from every other live/reserve leg. Immediately
dispatchable.
```

```
### 183 — ROUTE-XU8: DOES Xu arXiv:2607.19762 §8 PRE-EMPT PART OF THEOREM NGX (LEG 127)?
(USER-FLAGGED, TOP PRIORITY — blocks presenting leg 179's bundle as ready)
**Thesis.** An external novelty review of this repository's writeups found that leg 171 (XUL)
already surfaced, but did not itself resolve, a load-bearing fact: Xu §8 carries its own
interval-arithmetic no-go on the SAME operator this repository's Theorem NGX (leg 127,
`Z_1 >= 1` for every bounded `A` on `ell^1_w`) concerns — stated in Xu's own words as "no
weighted enclosure can exclude them" — and this repository has it banked nowhere. The
publishable methods note (leg 179's bundle: legs 51/54/58/126/127/157/158 composed into one
claim about why the radii-polynomial `ell^1`-Fourier framework fails on transport operators
with singular tails) rests on Theorem NGX's novelty. If Xu §8's no-go covers the same
territory as any part of NGX, the note's novelty claim narrows and must say so precisely, not
approximately. **Per the user's own instruction, nothing about the methods note should be
presented as ready until this leg answers** — leg 179 is downgraded to PROVISIONAL below,
pending exactly this.
**Gate.** Does Xu §8's interval-arithmetic no-go ("no weighted enclosure can exclude them"),
read at full-text depth with its exact hypotheses, cover the SAME operator/space/class that
Theorem NGX (leg 127) proves `Z_1 >= 1` for — fully, partially, or not at all?
  fully -> Theorem NGX is pre-empted; leg 127's landed claim needs an explicit novelty
         correction (not a retraction of the mathematics, which stands regardless of who
         proved it first — a priority correction to how it is described). ESCALATE
         immediately; this is claim-adjacent and not this leg's to silently reword.
  partially -> Name the exact boundary precisely (which sub-class Xu already covers, which
         NGX reaches that Xu does not). ESCALATE with the precise scope-narrowing needed for
         leg 179's bundle and any other prose citing NGX as fully novel.
  not at all -> Theorem NGX's novelty is confirmed independent of Xu §8. Report this
         precisely with Xu §8's own hypotheses recorded verbatim (what it DOES cover, to
         close the question rather than leave it open-ended), and leg 179's bundle can be
         confirmed (not just left provisional) on this specific point.
**Territory.** experiments/p2_route_xu8_v1_novelty.py, writeup/data/p2_route_xu8_v1_novelty.json,
               writeup/novelty/leg_183.md, experiments/journal/leg_183.md.
               Reads (never edits) leg 127's own report/JSON and leg 171's own report/JSON.
               If the outcome requires a correction to leg 127's or leg 179's prose, that
               correction is ESCALATED, not made under this leg's own authority (both are
               claim-bearing, landed results).
**Difficulty.** light
**Independence.** Literature-only, own JSON, no solver module, no compute. Disjoint from
171/173/181 (different questions about the same paper). **Top priority in the recommended
dispatch order below — everything about presenting leg 179 as complete depends on it.**
```

```
### 184 — ROUTE-GBW: PIN THE GA BAN'S LIFT CONDITION SO IT CANNOT BE SATISFIED BY COARSENING
(USER-FLAGGED — closes a measured loophole, does not lift or loosen the ban)
**Thesis.** Leg 160 measured that the UNMODIFIED, UNREPAIRED leg-49 fitness — the same one
that failed the frozen six-property gate 4/6 at leg 49's own resolution, and again at leg
59's repaired wall model with P3 stuck at 0.342 — passes the SAME gate 6/6 when re-run at a
coarser resolution (n=101/151). Leg 160 correctly refused to use this (its own no-branch:
report and escalate a pass, do not treat it as the lift condition being met, since the leg's
whole point was a genuinely REPAIRED fitness, not a coarser grid on the same broken one).
This is a real gap in the ban's own wording: `plan_of_record.py`'s lift condition currently
reads "a re-run of the six-property gate that PASSES on a repaired fitness," with no
resolution floor — so a future re-run at a suffiently coarse grid could satisfy the letter
of the condition without a genuine repair. **This leg CLOSES the loophole; it does not lift,
loosen, or satisfy the ban** — tightening a ban's wording to prevent an accidental gameable
lift needs no user authorization the way lifting one does, but the edit touches
`plan_of_record.py`'s ban infrastructure directly, so it is scoped as narrowly as leg 65's
capabilities.py annotation-fix precedent: ONE clause added, nothing else in the file touched,
and reported with full visibility rather than folded in quietly.
**Gate.** Does `plan_of_record.py`'s GA-ban lift condition, after this leg's edit, require
the six-property gate to pass at a PINNED resolution (or across a pre-named minimum set of
resolutions with monotonic/stable results — not merely "some resolution"), specifically
excluding the coarsening leg 160 found (n=101/151 passing where finer resolutions and the
original construction both fail)?
  yes -> Report the exact wording added, verify `test_plan_of_record.py`'s "exactly one
         NEXT" invariant and every other merge-gate test still pass unchanged, and confirm
         no already-landed leg's gate answer is retroactively altered by the wording (leg
         160's own NO stays NO; this closes a future loophole, it does not relitigate a past
         leg). Bank the corrected wording.
  no  -> If the edit cannot be scoped this narrowly without touching something else in
         `plan_of_record.py`, STOP and escalate the wording itself for the user's sign-off
         instead of landing a broader edit under this leg's own authority.
**Territory.** `plan_of_record.py` (ONE clause, the GA ban's lift-condition text ONLY — no
               other ban, stage, or gate touched), experiments/p2_route_gbw_v1_banwording.py,
               writeup/data/p2_route_gbw_v1_banwording.json,
               writeup/novelty/leg_184.md, experiments/journal/leg_184.md.
**Difficulty.** light
**Independence.** The only leg in this file's history authorized to touch
`plan_of_record.py` directly, and only for this one clause — checked explicitly against
every other live/reserve leg, none of which touches this file. Immediately dispatchable;
already flagged in `PROGRESS.md`'s NEEDS YOU per the coordinator's note, this leg is the
mechanism the DM is choosing for it.
```

```
### 185 — ROUTE-M2SD: DOES LEG 125's OBJECT-B NEWTON STALL MEAN GENUINE NON-EXISTENCE, OR A
SOLVER ARTIFACT?
**Thesis.** Leg 125 (M2P) landed gate NO on both clauses: Chen's γ=2 profile is the INVISCID
closed form (his own text: "we study the inviscid problem, i.e. ν=0"), not a dissipative one,
so there was nothing to certify on Object A; separately, "Object B" — the viscous steady
state that would have to exist for a genuine γ=2 dissipative certificate — was attempted
under Newton continuation and STALLED at residual 2.65-3.75 with `c_l` running to −10.7,
rather than converging to a solution or diverging cleanly to a certified non-existence. That
stall has never been diagnosed. Two honest outcomes: (a) genuine non-existence — the
continuation's own behavior (residual plateau, `c_l`'s monotone runaway) is characteristic of
approaching a genuine obstruction, which would strengthen the "no viscous γ=2 gCLM profile
exists" reading and directly inform leg 174's (VBS) catalog of alternative viscous models; or
(b) a solver artifact — a bad initial guess, a parametrization singularity at the stalled
point, or insufficient continuation depth, in which case a repaired continuation might still
reach a genuine profile leg 125 itself never got the chance to test. Diagnostic only: no new
dissipative-dynamics run, re-examine leg 125's own stalled continuation with standard
diagnostics (residual trend classification, Jacobian conditioning near the stall,
sensitivity to the initial guess) before concluding either way.
**Gate.** Does the Newton stall on Object B, diagnosed against standard non-existence
signatures (residual plateau shape, Jacobian singularity structure, parametrization
degeneracy) versus standard solver-artifact signatures (basin-of-attraction sensitivity,
recoverable convergence from a different initial guess at the SAME target), classify as one
or the other?
  genuine non-existence -> Report the diagnostic evidence precisely. Strengthens the "missing
         rung" framing — bank this as informing leg 174's catalog; do not re-attempt
         construction under this leg's own authority (that would be a new leg, informed by
         this one's diagnosis).
  solver artifact -> Report exactly what changed the outcome (different initial guess,
         reparametrization) and whether a genuine profile becomes reachable. ESCALATE as a
         candidate follow-up construction leg — do not build the corrected continuation here.
  inconclusive -> Report what was tried and why neither signature was clean; bank as a
         characterized open diagnostic, not a forced verdict.
**Territory.** experiments/p2_route_m2sd_v1_diagnostic.py,
               writeup/data/p2_route_m2sd_v1_diagnostic.json,
               writeup/novelty/leg_185.md, experiments/journal/leg_185.md.
               Reads (never edits) leg 125's own report/JSON and
               solver/target_selection.py/solver/dissipative_profile.py, read-only (leg 125's
               territory, closed on landing).
**Difficulty.** standard
**Independence.** Read-only re-diagnosis of a closed leg's own stalled run; no dynamics
construction, no GA compute. Disjoint from 174 (VBS, cataloging OTHER models, not
re-diagnosing this one) and from every other live/reserve leg. Immediately dispatchable.
```

```
### 186 — ROUTE-PUB2: THE SPACE-AXIS METHODOLOGICAL NOTE — ell^1_w DEAD (127) + ORIGIN-H²
CAPPED AT a=0 (163) + NO INTERPOLANT HELPS (182)
**Thesis.** The space axis is now fully mapped and closed: leg 127 proved `Z_1 >= 1`
unconditionally for every bounded `A` on `ell^1_w`; leg 163 found origin-H² structurally
viable but capped at `a=0` exactness, re-deriving Xu's own closed form with no transfer to
the real (non-`a=0`) target; leg 182 confirmed no interpolating space between the two avoids
both obstructions. Read separately, these are three leg reports; read together, they are one
coherent finding about WHERE a certificate for this operator can and cannot live — exactly
the shape of synthesis leg 179 already demonstrated is worth writing up as its own note
rather than leaving scattered. This is genuinely new content (163 and 182 both postdate leg
179's bundle), not a re-tread, and it is synthesis of landed mathematics, not audit/hygiene
work — consistent with, not in tension with, the standing math-over-review steer.
**Gate.** Does the combined note state all three space-axis results accurately — leg 163's
known ceiling and leg 182's negative result stated exactly as landed, with leg 176's
construction outcome (if landed by the time this leg runs) folded in as a fourth data point,
and no softening or strengthening of any of them?
  yes -> Bank the combined note as a second, SEPARATE publication-scoping draft from leg
         179's (different question: where else the method might live, not why it fails on
         `ell^1_w`). Flag both to the user together at the next natural check-in, explicitly
         noting they are two documents, not one, unless the user's own editorial judgment
         says otherwise.
  no  -> Report exactly which bundled claim doesn't reproduce from its own banked source;
         escalate rather than silently soften it, same discipline as leg 179.
**Territory.** writeup/4_p2_lottery/TECHNICAL_P2_PUB2_V1.md (NEW),
               writeup/4_p2_lottery/BLOG_P2_PUB2_V1.md (NEW),
               writeup/novelty/leg_186.md, experiments/journal/leg_186.md.
               Reads (never edits) legs 127/163/176/182's own banked JSONs and reports.
**Difficulty.** light
**Independence.** New writeup files only; no solver module, no existing file edited (unlike
leg 179, which had one small correction to leg 157's framing note — this leg needs no such
touch). Disjoint from every other live/reserve leg. Immediately dispatchable.
```

```
### 187 — ROUTE-M2CI: CAN A COMPUTER-ASSISTED CERTIFICATE CLOSE ON CHEN'S γ=2 INVISCID
PROFILE ("OBJECT A")? (NOT the viscous rung — a separate, fully-grounded lead)
**Thesis.** Leg 125 (M2P) landed gate NO on both its own clauses, but its own numbers contain
an unexploited lead: "Object A" — Chen's actual analytically-proven profile, the INVISCID
γ=2 closed form (his own text: "we study the inviscid problem, i.e. ν=0") — measured UNDER
the radii-polynomial budget at all 9 tested rows (`Y_0`/budget ranging 1.325e-09 to
5.800e-05), comfortably inside certificate range. Chen's proof of this profile's blow-up is
analytic, not computer-assisted, and leg 125's own novelty pass found no CAP of any
self-similar gCLM profile (dissipative OR inviscid at this specific parameter) in the
searched literature. **Stated up front, honestly: this does NOT answer the viscous "missing
rung" question** — Object A is inviscid, the same category as Chen-Hou's own already-CAP'd
work, not a new category. What it offers instead is a fully independent, high-value result:
the first computer-assisted certificate of Chen's SPECIFIC γ=2 profile, upgrading an
analytic proof to CAP status, using infrastructure this repository already has (leg 125's own
transcription of Chen's constants, Newton-recovered shape). No dynamics run; construction
only, following the leg 54/58 certificate-battery discipline, no GA compute.
**Gate.** Does a full radii-polynomial certificate close on Chen's γ=2 inviscid profile
(Object A), using leg 125's own transcribed constants and recovered shape as the starting
construction, with every hypothesis of the certificate framework satisfied (not just the
budget comparison leg 125 already made)?
  yes -> The first CAP of Chen's γ=2 profile. Report the full certificate precisely, stated
         as inviscid and independent of the viscous-blow-up question — do not conflate the
         two framings in the writeup. ESCALATE as a genuinely novel positive result for the
         user's attention, on the same footing as leg 125's original benefit-test framing.
  no  -> Report exactly which certificate hypothesis fails despite the budget comparison
         looking favorable (a common shape: budget-under but a different clause of the
         framework still fails). Bank as a characterized negative — the lead was real but
         did not close.
**Territory.** solver/dissipative_profile.py (read-only, leg 125's territory, closed on
               landing) plus a NEW certificate-construction module
               (`solver/chen_inviscid_certificate.py`, capabilities.py grepped first per the
               standing ban), test_chen_inviscid_certificate.py (NEW),
               experiments/p2_route_m2ci_v1_construction.py,
               experiments/p2_route_m2ci_v1_construction_evidence.py,
               writeup/data/p2_route_m2ci_v1_construction.json,
               writeup/novelty/leg_187.md, experiments/journal/leg_187.md.
**Difficulty.** heavy
**Independence.** Sole owner of a brand-new module. Reads leg 125's territory read-only.
Disjoint from 185 (M2SD, diagnosing Object B's stall — a different object, the viscous one,
not Object A) and from every other live/reserve leg. No GA compute under any outcome.
Immediately dispatchable.
```

```
### 188 — ROUTE-SURV: CORRECTED 2026-08-06 BY THE DM, PREMISE FALSIFIED BY THE LEG'S OWN
NOVELTY PASS (`c273084`) BEFORE CONSTRUCTION — IS n=3's EXCLUSION FORCED BY THE STRICT RULE
ITSELF, GIVEN THAT RULE IS NOT YET ADOPTED ANYWHERE ELSE ON `main`?
**Original premise, now confirmed false, preserved for the record:** this leg was drafted on
the claim that the strict Bowman 2/3 rule (`k < n/3` strictly) is "already cited and used
elsewhere in this repository, e.g. leg 120's own repair." **The leg's own novelty pass
(committed before any analysis, `c273084`) checked this directly and found the opposite**:
leg 120's landed commit is captioned "escalated, not patched" — it did NOT adopt the strict
rule — and every shipped mask on `main` today is still the loose cut (`spectral_utils.py:36`
`<= n/3`, `boussinesq.py:153/419`, `fractional_boussinesq.py:259`, `fractional_gclm.py:265`;
a repo-wide grep for the strict form returns nothing). The strict rule lives on `main` only
inside adversarial-battery PINS, which record the loose cut as a known defect (D1) rather
than replace it. So "does `n=3`'s rejection follow necessarily from a rule this repository
already committed to elsewhere" cannot be asked as originally framed — there is no
already-adopted elsewhere to check it against, and the leg's own text says so before
producing a single number.
**Corrected thesis, narrowed to what can actually be answered without presupposing an
adoption that hasn't happened.** Two questions survive, and this leg answers both without
touching leg 129's parked branch (`leg/129-sur-v1`, still unmerged) or any of the five
shipped loose masks: (i) taking the strict Bowman rule ON ITS OWN mathematical terms (not as
"already used" but as a rule that COULD be adopted), is `n=3`'s exclusion (retaining only the
mean mode, `|k| < 1`, under `k < n/3`) a forced consequence of the rule with no alternative
admissible reading — i.e., is the MATH forced, independent of adoption status; and (ii),
now that adoption status is known to be "nowhere on `main`, pinned as a defect in adversarial
batteries only," does adopting the strict rule for `solver/boussinesq.py`'s mask ALONE (as
leg 129's branch does) create a fresh internal inconsistency against the four other shipped
loose masks that this leg must name, since that inconsistency was invisible under the
original (false) "already used elsewhere" framing and is a NEW fact this correction surfaces.
**Gate.** (a) Is `n=3`'s exclusion under the strict Bowman rule mathematically forced (no
alternative admissible reading of the rule itself admits `n=3`), and (b) does adopting the
strict rule for `boussinesq.py` alone — while `spectral_utils.py`/`boussinesq.py:419`/
`fractional_boussinesq.py`/`fractional_gclm.py` stay on the loose cut — leave those four
modules internally inconsistent with the newly-strict one on the same admissibility question?
  (a) forced, (b) yes (inconsistency created) -> The math is forced but adopting it
         piecemeal creates a NEW, previously-unstated problem: escalation #4 is not just "does
         this one verdict flip," it is "does the repository adopt strict Bowman everywhere or
         nowhere." ESCALATE both findings together as a SHARPENED version of escalation #4 —
         this leg does not merge leg 129, patch any of the four modules, or pick an adoption
         scope itself.
  (a) forced, (b) no (four modules already satisfy strict, or the inconsistency doesn't
         actually arise) -> Report why not, precisely (e.g. their own `n` never goes below 4
         in any shipped caller). Escalate #4 as originally scoped, now on solid mathematical
         footing rather than a false "already used" premise.
  (a) not forced (an alternative admissible reading exists) -> The escalation was never
         resolvable independently; confirms it needs the user's ruling on the rule itself, not
         just its application to `n=3`. Bank this as closing the "could this resolve itself"
         question.
**Territory.** experiments/p2_route_surv_v1_verification.py,
               writeup/data/p2_route_surv_v1_verification.json,
               writeup/novelty/leg_188.md, experiments/journal/leg_188.md.
               Reads (never merges or edits) `leg/129-sur-v1`'s own commits, and
               solver/boussinesq.py, solver/spectral_utils.py, solver/fractional_boussinesq.py,
               solver/fractional_gclm.py as they stand on `main` (unaffected by leg 129, since
               it never merged), read-only.
**Difficulty.** light
**Independence.** Read-only, including of a parked branch (reading, not merging — no
territory claim on any of the four modules, which stay unowned on `main`). Disjoint from
every other live/reserve leg. Immediately dispatchable — WIP already exists on
`leg/188-surv-v1` (novelty pass committed, analysis not yet run); a fresh leg agent should
resume that branch under THIS corrected framing, not the original false one.
```

```
### 189 — ROUTE-XUTRI: DOES Xu's SPECTRAL-PICTURE FRAMEWORK INDEPENDENTLY REPRODUCE
a_c=0.6890665 OR alpha(1/2)=3? (a third derivation, triangulating two already-contested
constants)
**Thesis.** This repository has two independent derivations of `a_c=0.6890665` (published,
LSS via ALS/Xu citation) and `alpha(1/2)=3` (ALS eq. 49-50, re-derived cold by this
repository to 7.7e-5 relative on `c_l` and 1.4e-4 on the `Omega` exponent) — plus its own
instrument's measurement of `a_c`, explicitly recorded as "the worst of three sources"
(PHASE2_P2_NOTES J-8). Xu arXiv:2607.19762's spectral-picture framework has been read
extensively for the origin-H² invertibility citation and the §8 no-go (legs 127, 163, 171,
173, 181, 183), but never asked whether it independently reproduces either constant through
its OWN spectral-gap machinery, structurally different from ALS's direct pole-dynamics
integration. A third, independent derivation would either triangulate confidence in both
numbers (strengthening the existing ledger) or locate a genuine discrepancy this
repository's "worst of three sources" framing has not yet explained.
**Gate.** Does Xu's spectral-picture framework, applied to its own stated spectral data (not
borrowed from ALS/LSS), reproduce `a_c=0.6890665` and/or `alpha(1/2)=3` to a precision
comparable to this repository's existing re-derivations, using only techniques Xu's own paper
states?
  yes (either or both) -> Record the derivation and its precision verbatim. This
         strengthens the ledger's confidence in whichever constant(s) triangulate; update
         `solver/literature_gates.py`'s existing rows (append-only) to note the third source.
  no (Xu's framework doesn't bear on either constant, or gives a materially different value)
         -> If materially different: report the discrepancy precisely and ESCALATE — three
         disagreeing "independent" sources is a priority finding. If Xu's framework simply
         doesn't address either constant: report that clearly and bank it as closing the
         triangulation question with a null result, not a discrepancy.
**Territory.** experiments/p2_route_xutri_v1_lit.py, writeup/data/p2_route_xutri_v1_lit.json,
               writeup/novelty/leg_189.md, experiments/journal/leg_189.md.
               Append-only edit to solver/literature_gates.py's existing `a_c` row ONLY, if
               the yes-branch applies — no other row touched.
**Difficulty.** standard
**Independence.** Literature-plus-derivation, no new solver module. Disjoint from 145 (ledger
self-consistency audit, different question) and from 161 (LSS, a different paper). Read-only
overlap with legs 127/163/171/173/181/183's own use of Xu is read-read, not a collision.
Immediately dispatchable.
```

```
### 190 — ROUTE-EGML: LOCATE AND VERIFY THE "EGM" CITATION
**Thesis.** "EGM" has been relayed to this repository twice — the external novelty review's
own summary of leg 165's classification (weighted-energy realization, TIER 1: "at `p=2` it
is width 2.0 and EGM certifies a −1/2 gap") — but does not appear anywhere in
`solver/literature_gates.py` or any other ledger this DM has checked. It is likely a citation
leg 165 itself located, banked only in its own leg-165 JSON/report rather than the shared
ledger. Locate it precisely: full arXiv identifier, authors, exact claim and hypotheses,
verified at primary-source depth (not re-derived secondhand from the external review's
paraphrase) — this is exactly the discipline every other citation in this repository's ledger
already meets, and leg 178's own construction work may need EGM's precise identity for
comparison.
**Gate.** Can "EGM" be located as a real, checkable primary source, and does it state the
`p=2`, `−1/2`-gap claim as relayed, with its own hypotheses?
  yes -> Record the full citation and verbatim claim; add it to
         `solver/literature_gates.py` (append-only, new row) so it is a shared-ledger
         citation, not a leg-165-only reference.
  no (cannot be located, or the claim doesn't match) -> Report precisely what was found
         instead (a mis-transcription, a different citation the review may have meant, or
         genuinely nothing matching). Flag for the coordinator to check with leg 165's own
         report directly, since this leg's own search came up short.
**Territory.** solver/literature_gates.py (append-only, ONE new row if located — no
               existing row touched), experiments/p2_route_egml_v1_lit.py,
               writeup/data/p2_route_egml_v1_lit.json,
               writeup/novelty/leg_190.md, experiments/journal/leg_190.md.
**Difficulty.** light
**Independence.** Literature-only plus one append-only ledger row. Disjoint from every other
live/reserve leg. Immediately dispatchable.
```

```
### 191 — WITHDRAWN 2026-08-06. Stale premise: drafted on the assumption that leg 60 (PQ)
was still parked awaiting the user's ruling on two unreproducible numbers. It was not — leg
60 landed long ago at `e0eba8e` ("landed by orchestrator, user-approved correction"), all
three discrepancies corrected, both ban-bearing numbers confirmed exact, both scripts CLEAN
114/114. Never dispatched (the coordinator caught this before dispatch). Superseded by **195
(PQVER)** below, which verifies the LANDED correction rather than asking whether to make it.
Leg number 191 stays retired, not reused, per this file's numbering convention.
```

```
### 192 — ROUTE-H2CV: INDEPENDENT POST-CONSTRUCTION VERIFICATION, LEG 176's ORIGIN-H²
CERTIFICATE (RESERVE — NOT dispatchable until leg 176 lands)
**Thesis.** Leg 176 builds the first certificate this repository has constructed outside the
`ell^1_w` lane. Per the same discipline this repository applies to every repair (never trust
a leg's own self-report alone), this construction — a genuinely novel positive-result claim,
not just a non-regression check — deserves the same independent verification, applied one
level up: re-derive the certificate's closing quantity from leg 176's own construction
script, independently, and re-check the claimed agreement with Xu's closed form.
**Gate.** Does an independent re-run of leg 176's construction reproduce its claimed closing
quantity and its claimed agreement with Xu's closed form, to the same precision?
  yes -> Independently confirmed. Bank as the permanent verification record for this
         repository's first non-`ell^1_w` certificate.
  no -> Report the exact discrepancy precisely; escalate as a priority finding — a
         genuinely novel positive claim that doesn't independently reproduce is the single
         most consequential kind of finding this repository could produce right now.
**Territory.** test_origin_h2_certificate_postconstruction.py,
               experiments/p2_route_h2cv_v1_postconstruction.py,
               writeup/data/p2_route_h2cv_v1_postconstruction.json,
               writeup/novelty/leg_192.md, experiments/journal/leg_192.md.
**Difficulty.** standard
**Independence.** Reads solver/origin_h2_certificate.py; edits nothing under either outcome.
**NOT dispatchable until leg 176 lands.**
```

```
### 193 — ROUTE-M2CV: INDEPENDENT POST-CONSTRUCTION VERIFICATION, LEG 187's CHEN-INVISCID
CERTIFICATE (RESERVE — NOT dispatchable until leg 187 lands)
**Thesis.** Leg 187 attempts the first computer-assisted certificate of Chen's γ=2 inviscid
profile. Same discipline as 192, applied to this construction: if leg 187 lands YES (the
certificate closes), that is this cycle's single most novel positive claim and deserves
independent re-derivation before being presented as confirmed, not just self-reported.
**Gate.** Does an independent re-run of leg 187's construction reproduce its claimed
certificate closure (or, if leg 187 landed NO, reproduce its claimed failure point) from
leg 187's own transcribed constants and construction script?
  yes -> Independently confirmed either way. Bank as the permanent verification record.
  no -> Report the exact discrepancy precisely; escalate as a priority finding.
**Territory.** test_chen_inviscid_certificate_postconstruction.py,
               experiments/p2_route_m2cv_v1_postconstruction.py,
               writeup/data/p2_route_m2cv_v1_postconstruction.json,
               writeup/novelty/leg_193.md, experiments/journal/leg_193.md.
**Difficulty.** standard
**Independence.** Reads solver/chen_inviscid_certificate.py; edits nothing under either
outcome. **NOT dispatchable until leg 187 lands.**
```

```
### 194 — ROUTE-WESV: INDEPENDENT POST-CONSTRUCTION VERIFICATION, LEG 178's WEIGHTED-ENERGY
v2 CONSTRUCTION (RESERVE — NOT dispatchable until leg 178 lands)
**Thesis.** Leg 178 tests whether a different weighted-energy construction shifts leg 111's
zero-width window. Whichever way it lands, this is a genuinely new construction result (not a
repair), and the same discipline as 192/193 applies: independently re-derive its measured
coercivity gap from its own append-only addition to `solver/energy_coercivity.py`.
**Gate.** Does an independent re-run of leg 178's construction reproduce its claimed
coercivity-gap measurement (positive-and-stable, or still zero-width) from its own code?
  yes -> Independently confirmed. Bank as the permanent verification record.
  no -> Report the exact discrepancy precisely; escalate as a priority finding — this
        directly bears on the external review's item 3, which has been open the longest of
        the four.
**Territory.** test_energy_coercivity_v2_postconstruction.py,
               experiments/p2_route_wesv_v1_postconstruction.py,
               writeup/data/p2_route_wesv_v1_postconstruction.json,
               writeup/novelty/leg_194.md, experiments/journal/leg_194.md.
**Difficulty.** standard
**Independence.** Reads solver/energy_coercivity.py (leg 178's append-only addition); edits
nothing under either outcome. **NOT dispatchable until leg 178 lands.**
```

```
### 195 — ROUTE-PQVER: INDEPENDENT VERIFICATION OF LEG 60's LANDED PORT v1/v2 CORRECTION
**Thesis.** Leg 60 landed at `e0eba8e` with a self-reported clean result: three discrepancies
corrected (28x->63x mislabeled baseline, a `-2.541222`->`-2.541024` transcription slip,
`1.168%`->`1.169%` rounding), both ban-bearing numbers confirmed exact before and after, both
reproduction scripts reporting CLEAN 114/114. Per the same discipline this repository applies
to every other landed correction (postrepair-verification, 86/87/94/103/104/105/131-135/
147/166-170/192-194), a self-report is not an independent confirmation — re-run both
reproduction scripts fresh, from their own drivers, against the corrected banked prose, and
confirm the 114/114 claim and both ban-bearing numbers independently.
**Gate.** Does an independent re-run of `experiments/p2_route_port_v1_bordered_evidence.py`
and `experiments/p2_route_port_v2_reach_evidence.py` reproduce CLEAN 114/114, with both
ban-bearing numbers exact and all three corrected discrepancies matching the corrected
prose exactly?
  yes -> Independently confirmed. Bank as the permanent verification record; escalation
         #4 (leg 60) is now doubly closed — landed AND independently re-verified.
  no -> Report the exact discrepancy precisely; escalate as a priority finding — a
        user-approved correction that doesn't independently reproduce is serious.
**Territory.** test_route_port_postcorrection.py,
               experiments/p2_route_pqver_v1_verification.py,
               writeup/data/p2_route_pqver_v1_verification.json,
               writeup/novelty/leg_195.md, experiments/journal/leg_195.md.
               Reads (never edits) leg 60's own landed evidence scripts and
               `writeup/4_p2_lottery/TECHNICAL_P2_ROUTEPORT_V1.md`/`V2.md`.
**Difficulty.** standard
**Independence.** Read-only re-verification of a landed, closed leg. Disjoint from every
other live/reserve leg. Immediately dispatchable.
```

```
### 196 — ROUTE-USC2: DOES THE AUTHORS' LATER WORK (POST-OBSTRUCTION-REMOVAL) ACHIEVE AN
ACTUAL CERTIFICATE FOR arXiv:2509.14185's UNSTABLE SINGULARITIES?
**Thesis.** Leg 175 (USC) landed TECHNIQUE-SPECIFIC: `arXiv:2509.14185`'s CAP-readiness
obstruction was one specific loss-reweighting scheme, and the same authors (Wang, Lai,
Gomez-Serrano, Buckmaster et al.) removed it in later work roughly 72 days on. That later
work has never been located or read by this repository. Does it achieve an actual
certificate (closing the CAP-ready numerics into a rigorous enclosure), or does removing
that one obstruction simply expose a different one — the same shape of question leg 175
itself asked, one paper later?
**Gate.** Does the authors' later work (post-obstruction-removal) state, imply, or make
locatable an actual certificate for the unstable singularities `arXiv:2509.14185` reported
at CAP-ready precision, and if not, what NEW obstruction (if any) does it name?
  certificate achieved -> This would be the single most consequential literature finding
         this repository could produce — the first genuinely 3D PDE blow-up certificate
         found anywhere, directly answering the Wall 2 question (leg 172). Record the
         citation and its hypotheses verbatim; ESCALATE immediately, do not attempt to
         replicate it under this leg's own authority.
  still short, new/same obstruction -> Report exactly what remains, in the same terms leg
         175 used, so the two findings are directly comparable. Bank it.
  no later work locatable -> Report the search precisely (this repository's own discipline:
         report the search, not just the absence). Bank as inconclusive.
**Territory.** experiments/p2_route_usc2_v1_lit.py, writeup/data/p2_route_usc2_v1_lit.json,
               writeup/novelty/leg_196.md, experiments/journal/leg_196.md.
               Reads (never edits) solver/viscous_novelty.py's PRECEDENTS ledger, read-only.
**Difficulty.** light
**Independence.** Literature-only, own JSON, no solver module. Disjoint from every other
live/reserve leg. Immediately dispatchable.
```

```
### 197 — ROUTE-VNL: ADD arXiv:2208.09445 TO THE SHARED viscous_novelty.py LEDGER
**Thesis.** Leg 174 (VBS) located and characterized `arXiv:2208.09445` (3D compressible
Navier-Stokes finite-time blow-up from smooth finite-energy data, Grade B — computer
assistance essential via ~10,000 interval-arithmetic Taylor coefficient pairs, but the
viscous term is DOMINATED rather than enclosed, so its certified object is the inviscid
Euler ODE) as present in leg 113's own literature ledger but confirmed ABSENT from the
shared `solver/viscous_novelty.py::PRECEDENTS` list — the same "found but not
shared-ledgered" gap leg 190 closed for "EGM." Bank it properly, append-only, using leg
174's own characterization (already verified at primary-source depth by that leg — this leg
does not need to re-read the paper, only transcribe the citation correctly into the shared
ledger).
**Gate.** Is `arXiv:2208.09445` now present in `solver/viscous_novelty.py::PRECEDENTS` with
the Grade B / viscous-term-dominated characterization leg 174 established, verbatim?
  yes -> Bank it; the shared ledger and leg 174's own occupancy matrix are now consistent
         with each other.
  no (a discrepancy is found between leg 174's characterization and a fresh check of the
  paper) -> Report the discrepancy precisely; escalate rather than silently reconcile it,
  since leg 174's occupancy-matrix conclusion depends on this exact characterization.
**Territory.** solver/viscous_novelty.py (append-only, ONE new PRECEDENTS row),
               experiments/p2_route_vnl_v1_ledger.py,
               writeup/data/p2_route_vnl_v1_ledger.json,
               writeup/novelty/leg_197.md, experiments/journal/leg_197.md.
**Difficulty.** light
**Independence.** One append-only ledger row. Disjoint from every other live/reserve leg.
Immediately dispatchable.
```

## Ranking rationale

Refreshed whenever a gate answers. Rank by, in order:

1. could this leg actually move a link of the L1→L4 chain;
2. can its gate answer either way within one leg's work;
3. is it independent of the other nine live legs.

**Refreshed 2026-08-06 (DM cycle: 128-series reserve-drain refill). This paragraph
supersedes the 110-series refresh below for ranking purposes; the NG ruling's placement of
126 (BX, critical path) and 127 (NGX, first reserve claim) stands and is not re-ranked
here.** Criterion (1): the critical path is the NG ruling's business (126/BX), and leg 111
measured the third realization dead (zero-width window), so nothing in the 128-series claims
chain movement; leg 125's positive-direction finding stays parked for the user and this
refill drafts nothing that presupposes its ruling. The batch is therefore ranked on (2) and
(3), sharpened into: **close the loops the audit family has opened before opening new
ones.** Repairs of found-and-flagged defects outrank fresh audits — 128 (NKR) and 129 (SUR)
discharge the two findings legs 116 and 120 explicitly flagged for the DM, and 130 (HPR)
repairs the one unrepaired bound-direction violation on main; all three have pre-committed
no-branches that stop-and-escalate on ANY clean-input movement, which is what makes
claim-adjacent repair legs safe to run unattended. Close-the-loop regressions outrank fresh
audits too — 133 (BOB, the 5.6e13x finding), 131, 132, 134, 135 apply the proven
86/87/94/103/104/105 pattern to the five repairs that never got one; a repair whose only
evidence is its own self-report is exactly the shape of thing leg 60 taught this repository
to distrust. **141 (WEL)** is the one genuinely new mathematical question in the batch — leg
65's novelty-of-the-no-go question re-asked for the third dead realization — light,
decidable either way, and it directly strengthens or caps the publication scoping now with
the user. **136 (MF2)** converts a known partial fix into either a complete detector
proposal or a characterized permanent limitation. **137/138** are cadence hygiene after the
largest landing wave of the run. **139/140** continue the audit family only on the two
load-bearing modules genuinely still uncovered — the family is 20+ legs deep with roughly a
50% hit rate and its uncovered pool is nearly empty; this file deliberately declines to pad
it. Dispatch order and the three blocked-pending items are stated in the 128-series Status
block, which is authoritative. Nothing in this refresh lifts a ban, touches leg 125's parked
escalation, re-ranks the NG ruling's assignments, or moves any claim about Walls 1 and 2;
Clay stays ~0.05%.

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
   them against each other, not just in the abstract. **UPDATE 2026-08-06: the negative half
   is no longer conditional — leg 58 delivered the theorem (class `A₂₁ = 0`, doubly-confirmed
   novelty), and its gate's own yes-branch puts PUBLICATION SCOPING to you: is a
   standalone negative theorem with a sharpness control, on the a=0 CLM proxy object, worth
   writing for the outside world now, or does it wait on leg 127's attempt at the sharp
   (full-class) form and/or leg 125's positive-direction measurement? The DM's recommendation:
   scope it now — the result is closed, doubly-checked and citable, and 127/125 can only add
   to it, not subtract.**

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

---

## DM cycle 2026-08-06 — RESUMPTION after external laptop shutdown

**Context.** The orchestrator session that was running this got cut off by an external
laptop shutdown (not a graceful stop). Per `reports/ORCH_STATE.md`, five branches were
salvaged and pushed (`leg/170-cdb-v1`, `leg/187-m2ci-v1`, `leg/188-surv-v1`,
`leg/189-xutri-v1`, `leg/190-egml-v1`), and leg 189 has since landed on `main` (`fac2870`,
`2bc65e0` — confirmed via `git log main`, gate NO on both constants, do not re-queue).
`git log --all --grep` confirms exactly the state `ORCH_STATE.md` describes: 176 fully
landed on `main` (`bb0f184`); 170/187/188 have a novelty-pass commit plus one WIP snapshot
commit each, no gate answer yet; 190 has only its novelty-pass commit (`b15e902`, EGM
located at `arXiv:1906.05811`, Anal. PDE 14 (2021) 891, one HTML-mirror sign error caught) —
needs the ledger-row edit plus journal/novelty-writeup finish; 192/195/196/197 have zero
commits anywhere (fully specified, never dispatched, confirmed by grep). No other
"never-dispatched reserve" numbers remain unaccounted for — every leg number from 129
through 190 that isn't one of these five either has a landed commit on `main` or (148 only)
is a genuinely blocked-pending-user item, not a fresh dispatch candidate.

**Correction made this cycle: leg 188's premise.** Leg 188's own novelty pass
(`c273084`, committed before any analysis, already on `leg/188-surv-v1`) found its drafted
premise false: it claimed the strict Bowman 2/3 rule was "already used elsewhere, e.g. leg
120's own repair," but leg 120's landed commit is captioned "escalated, not patched," and
every shipped dealiasing mask on `main` today is still the loose cut. The strict rule exists
on `main` only inside adversarial-battery pins (recording the loose cut as defect D1), never
adopted in shipped code. Leg 188's queue entry (above, § 188) has been rewritten in place to
ask the question this actually supports — is `n=3`'s exclusion mathematically forced by the
strict rule ON ITS OWN TERMS, and does adopting it for `boussinesq.py` alone create a fresh
inconsistency against the four other shipped loose masks — rather than the now-false
"already adopted elsewhere" framing. This is not a retraction of leg 129's math, only of the
precedent-claim this leg was originally handed.

**Ten-slot dispatch, this cycle.** No critical-path stage exists (`B` closed NO at leg 126,
6.04x short of a perfect search over its full declared space; escalation #1, parked for the
user, per `plan_of_record.py`'s own printed state — this DM does not resolve it and does not
pick a replacement `NEXT` stage). All ten slots are therefore exploration legs, ranked by (a)
could it move a link of the L1→L4 chain, (b) can its gate answer either way within one leg,
(c) is it independent of the other nine.

| Slot | Leg | Route | Gate (one line) | Why this rank |
|---|---|---|---|---|
| LEG-A | 192 | H2CV | Does an independent re-run of leg 176's origin-H² construction reproduce its closing quantity and Xu-agreement, to the same precision? | Highest under criterion (a): leg 176 is the single most novel *positive*-shaped construction this run has produced (first certificate outside the `ell^1_w` lane) and has never been independently re-derived — exactly the check this repository's own discipline says a genuinely new positive claim needs before anyone trusts it. |
| LEG-B | 187 | M2CI (resume WIP) | Does a full radii-polynomial certificate close on Chen's γ=2 INVISCID profile (Object A), using leg 125's transcribed constants? | Second-highest: also a live attempt at a genuinely novel positive result (first CAP of Chen's γ=2 profile), novelty pass already clean (N2/N3 pre-empted correctly, N4 identified), construction in progress — finishing it is higher-value than starting anything fresh. |
| LEG-C | 170 | CDB (resume WIP) | Post-repair, does `critical_dissipation.py` reject/flag every non-integer-`p` case in leg 121's battery AND reproduce every integer-`p` result bit-identically? | Deep into a corrected re-run per `ORCH_STATE.md` (gate YES both clauses per last known result); finishing a near-complete regression check is cheap and closes a loop the audit family already opened. |
| LEG-D | 188 | SURV (resume WIP, corrected framing) | (Corrected, see above) Is `n=3`'s exclusion forced by the strict Bowman rule on its own terms, and does adopting it for one module alone create a fresh cross-module inconsistency? | Premise now corrected in this same edit; resuming under the right framing is worth more than leaving a WIP branch stalled on a false premise. |
| LEG-E | 190 | EGML (finish) | Is "EGM" locatable at primary-source depth with the claimed p=2, −1/2-gap statement, and is it now in the shared ledger? | Novelty pass done and citation confirmed correct; only the mechanical ledger-row-plus-writeup finish remains — cheapest possible close of an already-90%-done leg. |
| LEG-F | 195 | PQVER | Does an independent re-run of leg 60's two reproduction scripts reproduce CLEAN 114/114 with both ban-bearing numbers exact? | Read-only re-verification of a landed, closed correction; light, decidable in one leg, zero collision risk with anything else in this batch. |
| LEG-G | 196 | USC2 | Does the authors' later work (72 days after `arXiv:2509.14185`, obstruction removed) achieve an actual certificate, or name a new obstruction? | Directly extends leg 175's landed, technique-specific finding; if YES this would be the first genuinely-3D PDE blow-up certificate found anywhere in the literature this repository has surveyed — high value under criterion (a) even though the base rate is low. |
| LEG-H | 197 | VNL | Is `arXiv:2208.09445` now present in `viscous_novelty.py::PRECEDENTS` with leg 174's Grade-B/viscous-dominated characterization, verbatim? | Mechanical ledger-consistency fix, same shape as 190's EGM gap; cheap, zero risk, closes a known bookkeeping hole. |
| LEG-I | 198 | BHA (new, drafted below) | Under adversarial/degenerate input, does `bordered_hl.py` ever silently return a wrong value? | Highest-value never-audited module in the audit family's own inventory — it borders the actual target certificate construction (leg 54/58/127's own operator), unlike several already-audited peripheral modules. |
| LEG-J | 199 | CGA (new, drafted below) | Under adversarial/degenerate input, does `certificate_guards.py` ever silently accept a case it should reject? | Same fabrication-acceptance shape that leg 116/128 found a real bug in (`nk_bounds.py` and siblings); `certificate_guards.py` is exactly the guard-layer module class that pattern has repeatedly caught real defects in, and it has never itself been audited. |

**Reserve queue: 6 undispatched legs (200, 201, 202, 203, 204, 205) — all newly drafted this
cycle, below, since the pre-existing reserve (192/195/196/197/198/199) is now fully consumed
by the ten-slot dispatch above and the count would otherwise sit at 0.** Per §3a, drafting
began immediately since the count was about to hit zero, not merely ≤3.

```
### 198 — ROUTE-BHA: ADVERSARIAL AUDIT OF bordered_hl.py
**Thesis.** `bordered_hl.py` implements the bordered formulation (leg TC's own assembly: the
far-field amplitude's own column, its own Y_0, and the matching condition) that sits directly
upstream of every certificate-shape battery this repository has run (legs 54, 58, 127) — it
is closer to the actual load-bearing construction than several already-audited peripheral
modules (viscous_novelty.py, energy_coercivity.py) and has never itself had an adversarial
battery run against it. Same standard battery as every other audit-family leg: NaN/Inf,
degenerate/zero-measure input, boundary parameters (the matching condition at or near
degeneracy), planted wrong-value pass-through.
**Gate.** Under adversarial and degenerate inputs (including a degenerate or near-singular
matching condition), does `bordered_hl.py` ever silently return a wrong value rather than
reject or visibly propagate the defect?
  yes -> Name the exact mechanism and magnitude. This module underwrites every bordered
         certificate battery this repository has run (54/58/127) — escalate as a priority
         finding, do not patch under this leg's own authority.
  no  -> Bank the battery as the permanent regression suite; record the pass in
         capabilities.py.
**Territory.** test_bordered_hl_adversarial.py, experiments/p2_route_bha_v1_adversarial.py,
               writeup/data/p2_route_bha_v1_adversarial.json,
               writeup/novelty/leg_198.md, experiments/journal/leg_198.md
**Difficulty.** standard
**Independence.** Reads solver/bordered_hl.py; edits nothing under either outcome. Not
touched by any live or reserve leg. Immediately dispatchable.
```

```
### 199 — ROUTE-CGA: ADVERSARIAL AUDIT OF certificate_guards.py
**Thesis.** `certificate_guards.py` is the guard-layer module class (accept/reject
hypothesis checks feeding a certificate's closing verdict) that leg 116/128's own
fabrication-acceptance pattern found a REAL bug in on a sibling module (`nk_bounds.py` and
its neighbors, 21 false-closing cases). `certificate_guards.py` has never itself been
audited under that same pattern, despite being exactly the shape of module the pattern
targets.
**Gate.** Under adversarial and degenerate inputs, does `certificate_guards.py` ever
silently ACCEPT (fail to reject) a case that should fail — the same fabrication-acceptance
shape leg 116 found in `nk_bounds.py`?
  yes -> Name the exact mechanism, magnitude, and every certificate battery whose banked
         verdict it could have silently affected. Escalate as a priority finding, do not
         patch under this leg's own authority.
  no  -> Bank the battery as the permanent regression suite; record the pass in
         capabilities.py.
**Territory.** test_certificate_guards_adversarial.py,
               experiments/p2_route_cga_v1_adversarial.py,
               writeup/data/p2_route_cga_v1_adversarial.json,
               writeup/novelty/leg_199.md, experiments/journal/leg_199.md
**Difficulty.** standard
**Independence.** Reads solver/certificate_guards.py; edits nothing under either outcome.
Disjoint from 128/NKR (a different, already-repaired module). Immediately dispatchable.
```

```
### 200 — ROUTE-PCA: ADVERSARIAL AUDIT OF port_certification.py (RESERVE)
**Thesis.** `port_certification.py` has been used as the bit-identical comparison target in
leg 128's (NKR) regression check but has never itself had an adversarial battery run
against its own logic, only a pre/post-repair equality check on a sibling module's fix.
Standard battery: NaN/Inf, degenerate port parameters, boundary-of-admissibility inputs,
planted wrong-value pass-through.
**Gate.** Under adversarial and degenerate inputs, does `port_certification.py` ever
silently return a wrong value rather than reject or visibly propagate the defect?
  yes -> Name the exact mechanism and magnitude; escalate as a priority finding (this module
         underwrites every PORT-family route's own reach-table claims), do not patch under
         this leg's own authority.
  no  -> Bank the battery as the permanent regression suite; record the pass in
         capabilities.py.
**Territory.** test_port_certification_adversarial.py,
               experiments/p2_route_pca_v1_adversarial.py,
               writeup/data/p2_route_pca_v1_adversarial.json,
               writeup/novelty/leg_200.md, experiments/journal/leg_200.md
**Difficulty.** standard
**Independence.** Reads solver/port_certification.py; edits nothing under either outcome.
Read-only overlap with leg 128's own bit-identical check (128 compares two versions of a
sibling module against this one; that is read-read, not a collision) and with leg 195
(PQVER, which re-runs PORT's own evidence scripts, not this module's adversarial battery).
Reserve — promote once a slot frees.
```

```
### 201 — ROUTE-ICA2: ADVERSARIAL AUDIT OF interval_certificate.py (RESERVE)
**Thesis.** Sibling of 200 by the same reasoning: `interval_certificate.py` is named
alongside `port_certification.py` in leg 128's own bit-identical regression check but has
never itself been adversarially audited. Given leg 69 (IA) found real soundness gaps in the
shared `interval.py` primitive underneath it (subnormal-range false negatives, a silent NaN
above 2^997 — scoped as not affecting any live operator's actual range), this specific
module is worth checking directly rather than assumed clean by association.
**Gate.** Under adversarial and degenerate inputs — including inputs near `interval.py`'s
own known failure bands (subnormal range, above 2^997), even though no live operator's range
reaches them — does `interval_certificate.py` ever silently return a wrong value?
  yes -> Name the exact mechanism and magnitude, and state explicitly whether it traces to
         `interval.py`'s own known gaps or is a new, independent defect. Escalate as a
         priority finding, do not patch under this leg's own authority.
  no  -> Bank the battery as the permanent regression suite; record the pass in
         capabilities.py. This would also be informative confirmation that leg 69's scoped
         "no live operator affected" finding holds one level up.
**Territory.** test_interval_certificate_adversarial.py,
               experiments/p2_route_ica2_v1_adversarial.py,
               writeup/data/p2_route_ica2_v1_adversarial.json,
               writeup/novelty/leg_201.md, experiments/journal/leg_201.md
**Difficulty.** standard
**Independence.** Reads solver/interval_certificate.py (and solver/interval.py, read-only,
for the known-failure-band inputs); edits nothing under either outcome. Disjoint from 200
(different module) and from every other live/reserve leg. Reserve — promote once a slot
frees.
```

```
### 202 — ROUTE-PNA: ADVERSARIAL AUDIT OF profile_newton.py (RESERVE)
**Thesis.** `profile_newton.py` is a shared Newton-continuation primitive in the same class
as `collocation_newton.py`, which the audit family's own death-certificate history
(`critical_radius`, leg 166) shows is exactly the kind of shared numerical-continuation
module that hides real defects. `profile_newton.py` has never had an adversarial pass.
**Gate.** Under adversarial and degenerate inputs (near-singular Jacobian, poor initial
guess, boundary-of-convergence parameters), does `profile_newton.py` ever silently report a
converged solution that is not (a false-positive convergence claim), or silently return a
wrong value rather than reject/flag?
  yes -> Name the exact mechanism and magnitude, and list every construction leg that calls
         this module (candidates: 125, 185, 187) whose banked convergence claim could be
         affected. Escalate as a priority finding, do not patch under this leg's own
         authority.
  no  -> Bank the battery as the permanent regression suite; record the pass in
         capabilities.py.
**Territory.** test_profile_newton_adversarial.py,
               experiments/p2_route_pna_v1_adversarial.py,
               writeup/data/p2_route_pna_v1_adversarial.json,
               writeup/novelty/leg_202.md, experiments/journal/leg_202.md
**Difficulty.** standard
**Independence.** Reads solver/profile_newton.py; edits nothing under either outcome.
Disjoint from collocation_newton.py's own already-audited history and from every other
live/reserve leg. Reserve — promote once a slot frees.
```

```
### 203 — ROUTE-RSA: ADVERSARIAL AUDIT OF rescaled_spectrum.py (RESERVE)
**Thesis.** `rescaled_spectrum.py` has never appeared in this repository's audit-family
inventory under any name-match. Standard battery: NaN/Inf, degenerate/zero-measure
rescaling parameters, boundary-of-admissibility inputs, planted wrong-value pass-through.
**Gate.** Under adversarial and degenerate inputs, does `rescaled_spectrum.py` ever silently
return a wrong value rather than reject or visibly propagate the defect?
  yes -> Name the exact mechanism and magnitude; escalate if claim-adjacent (check which
         banked spectral-gap numbers, if any, depend on this module before deciding), do not
         patch under this leg's own authority.
  no  -> Bank the battery as the permanent regression suite; record the pass in
         capabilities.py.
**Territory.** test_rescaled_spectrum_adversarial.py,
               experiments/p2_route_rsa_v1_adversarial.py,
               writeup/data/p2_route_rsa_v1_adversarial.json,
               writeup/novelty/leg_203.md, experiments/journal/leg_203.md
**Difficulty.** standard
**Independence.** Reads solver/rescaled_spectrum.py; edits nothing under either outcome. Not
touched by any live or reserve leg. Reserve — promote once a slot frees.
```

```
### 204 — ROUTE-TNA2: ADVERSARIAL AUDIT OF target_norm.py (RESERVE)
**Thesis.** `target_norm.py` has never appeared in this repository's audit-family inventory
under any name-match, despite "norm" modules elsewhere (holder_norms.py, via its own
audited siblings) being exactly the class of module this family has found real defects in.
Standard battery: NaN/Inf, degenerate/zero-norm input, boundary parameters, planted
wrong-value pass-through.
**Gate.** Under adversarial and degenerate inputs, does `target_norm.py` ever silently
return a wrong value rather than reject or visibly propagate the defect?
  yes -> Name the exact mechanism and magnitude; escalate if claim-adjacent, do not patch
         under this leg's own authority.
  no  -> Bank the battery as the permanent regression suite; record the pass in
         capabilities.py.
**Territory.** test_target_norm_adversarial.py,
               experiments/p2_route_tna2_v1_adversarial.py,
               writeup/data/p2_route_tna2_v1_adversarial.json,
               writeup/novelty/leg_204.md, experiments/journal/leg_204.md
**Difficulty.** standard
**Independence.** Reads solver/target_norm.py; edits nothing under either outcome. Disjoint
from 172/196/etc. (route name TNA2 chosen to avoid collision with any prior TNA-named leg;
verify against capabilities.py's route registry before dispatch, per the standing rule for
every leg). Reserve — promote once a slot frees.
```

```
### 205 — ROUTE-BVR: ADVERSARIAL AUDIT OF boussinesq_rescaled.py (RESERVE)
**Thesis.** `boussinesq_rescaled.py` has never appeared in this repository's audit-family
inventory under any name-match, unlike its siblings `boussinesq.py` (leg 129's own repair
target) and `boussinesq_velocity.py` (already audited). Standard battery: NaN/Inf,
degenerate/zero-measure input, boundary parameters (including the same dealiasing-mask
question leg 129/188 raise for `boussinesq.py`, checked here only as an input to the
adversarial battery, not as a repair), planted wrong-value pass-through.
**Gate.** Under adversarial and degenerate inputs, does `boussinesq_rescaled.py` ever
silently return a wrong value rather than reject or visibly propagate the defect?
  yes -> Name the exact mechanism and magnitude; if it is the SAME dealiasing-mask question
         leg 129/188 raise, state that explicitly as a second occurrence rather than a new
         defect, and escalate together with escalation #4. If it is a genuinely different
         defect, escalate separately.
  no  -> Bank the battery as the permanent regression suite; record the pass in
         capabilities.py.
**Territory.** test_boussinesq_rescaled_adversarial.py,
               experiments/p2_route_bvr_v1_adversarial.py,
               writeup/data/p2_route_bvr_v1_adversarial.json,
               writeup/novelty/leg_205.md, experiments/journal/leg_205.md
**Difficulty.** standard
**Independence.** Reads solver/boussinesq_rescaled.py; edits nothing under either outcome.
Disjoint from 188 (SURV, which reads boussinesq.py, not boussinesq_rescaled.py, and does not
merge or patch either) and from every other live/reserve leg. Reserve — promote once a slot
frees.
```

---

## DM bookkeeping update, cycle 1, same day — orchestrator report on 195/170 landing + 200/201 promotion

**195 (PQVER) landed on `main`.** Independently confirmed all five of leg 60's corrected
numbers. Found one small propagation gap of its own: a stale `-2.541222` literal (the
pre-correction transcription slip leg 60 already fixed in prose) survived uncorrected in two
other files; **zero banked results were affected** (the stale literal was inert prose/comment
context, not a computed input). The orchestrator fixed it directly in the integration commit
rather than routing it back through a separate repair leg — correctly proportionate to a
zero-blast-radius, mechanical propagation miss, same discipline as every other
postrepair-verification leg's own no-branch. Escalation #4 (leg 60) is now doubly closed:
landed AND independently re-verified, with this one cosmetic follow-on already swept up.

**170 (CDB) landed on `main`.** Gate **YES** on both clauses: 96/96 adversarial cases
correctly refused, 276077/276077 configurations bit-identical pre/post-repair on the
integer-`p` battery. Leg 154's repair of `critical_dissipation.py` (leg 121's original
finding) is now confirmed non-regressive, closing this audit-family loop cleanly.

**Slots F and C refilled from reserve, both dispatched now**, per the orchestrator's own
report: **200 (PCA)** into the vacated slot, **201 (ICA2)** into the other. Both are removed
from the reserve queue — they are live, not reserve, as of this update.

**Live assignments, corrected to match the orchestrator's own slot letters (supersedes the
ten-slot table two sections above for slot-occupancy purposes only — no leg's content or
gate changed, only which letter each already-assigned leg sits in, plus the two new
promotions):**

| Slot | Leg | Route | Status |
|---|---|---|---|
| A | 192 | H2CV | live (unchanged) |
| B | 187 | M2CI | live (unchanged) |
| C | 201 | ICA2 | **live, newly promoted from reserve** |
| D | 188 | SURV | live (unchanged, corrected framing per above) |
| E | 190 | EGML | live (unchanged) |
| F | 200 | PCA | **live, newly promoted from reserve** |
| G | 196 | USC2 | live (unchanged) |
| H | 197 | VNL | live (unchanged) |
| I | 198 | BHA | live (unchanged) |
| J | 199 | CGA | live (unchanged) |

(195 and 170 have landed and left the board entirely — they held no slot letter at landing
time per the orchestrator's report, so no slot needs vacating for them beyond what's already
reflected above.)

**Reserve queue: 4 undispatched legs (202, 203, 204, 205).** Above the §3a watermark of 3 —
no fresh batch drafted this update. **Flag for the orchestrator: the NEXT promotion out of
this reserve (whichever of 202/203/204/205 fills the next open slot) will drop the count to
3, exactly at the watermark; the promotion AFTER that will drop it to 2, below the
watermark** — this DM will draft at least 8 more fully-specified candidates the moment that
happens, per standing instruction, without waiting to be asked. Promotion order when a slot
next opens, unchanged from the original draft (no re-ranking triggered by this update): 202
(PNA), then 203 (RSA), then 204 (TNA2), then 205 (BVR).

Nothing in this update lifts a ban, resolves any parked escalation, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised this cycle, matching the
orchestrator's own report.

---

## DM bookkeeping update, cycle 1, same day — leg 196 landed, leg 202 promoted, watermark hit,
8 new candidates drafted

**196 (USC2) landed on `main`.** Gate **STILL SHORT**: the authors' follow-up paper
(`arXiv:2511.22819`, ~72 days after `arXiv:2509.14185`) carries no certificate for the
unstable singularities — 0 of leg 175's 4 open items closed, and the follow-up names 3 NEW
obstructions of its own. Clean landing, no escalation (this is the "still short, new
obstruction" branch of leg 196's own pre-committed gate, not the "certificate achieved"
branch). Banked; the Wall-2 question (leg 172) stays answered NO on this literature line.

**Slot G refilled: leg 202 (PNA) promoted from reserve, dispatched now.** Per the
orchestrator's own report, live slots are: A=192(H2CV), B=187(M2CI), C=201(ICA2),
D=188(SURV), E=190(EGML), F=200(PCA), **G=202(PNA, new)**, H=197(VNL), I=198(BHA),
J=199(CGA).

**Watermark hit exactly as flagged last update: reserve drops to 3 (203, 204, 205).** Per
§3a and the standing instruction to draft at least 8 more the moment the count is at or below
3, eight new fully-specified candidates are drafted below, all grounded in already-landed
findings, none presupposing any in-flight leg's unknown outcome. Four close out the
audit-family's now-fully-enumerated remaining pool (`ga_search.py`, `dissipative_profile.py`,
`target_selection.py`, `spectral_certificate.py` — confirmed by grep against this file, the
only four solver modules with zero prior name-matched adversarial-audit entry); one extends
the postconstruction-verification pattern (192/193/194/195) to leg 185's own new numeric
measurement; one is a literature cross-check grounded in leg 185's finding against Xu's
already-fully-read paper; one independently re-verifies leg 196's own literature claim
(same discipline as 195 applied to a literature landing, not just a construction); one is a
ledger-consistency audit of this cycle's own three append-only ledger rows (189/190/197),
the same pattern as leg 145's prior ledger self-consistency audit.

```
### 206 — ROUTE-GSA: ADVERSARIAL AUDIT OF ga_search.py (RESERVE)
**Thesis.** `ga_search.py` is the GA infrastructure module this repository's own standing
ban restricts ("no GA compute on an unvalidated fitness") — every leg that has ever touched
it (49, 59, 160) measured the FITNESS, never the search infrastructure itself for silent
defects under adversarial input. Confirmed zero prior name-matched adversarial-audit entry.
Standard battery: NaN/Inf, degenerate population/parameter bounds, boundary-of-convergence
inputs, planted wrong-value pass-through. **No GA compute under any outcome** — this leg
audits the module's own robustness to bad input, it does not run or repair the banned
search.
**Gate.** Under adversarial and degenerate inputs, does `ga_search.py` ever silently return
a wrong value (a fitness, a converged individual, a termination flag) rather than reject or
visibly propagate the defect?
  yes -> Name the exact mechanism and magnitude, and state explicitly whether it is
         orthogonal to the standing GA ban (an infrastructure bug, not a fitness-validity
         question) or bears on it. Escalate if claim-adjacent, do not patch under this leg's
         own authority.
  no  -> Bank the battery as the permanent regression suite; record the pass in
         capabilities.py.
**Territory.** test_ga_search_adversarial.py, experiments/p2_route_gsa_v1_adversarial.py,
               writeup/data/p2_route_gsa_v1_adversarial.json,
               writeup/novelty/leg_206.md, experiments/journal/leg_206.md
**Difficulty.** standard
**Independence.** Reads solver/ga_search.py; edits nothing under either outcome. No GA
compute triggered under either outcome — does not touch or lift the standing ban. Reserve —
promote once a slot frees.
```

```
### 207 — ROUTE-DPA: ADVERSARIAL AUDIT OF dissipative_profile.py (RESERVE)
**Thesis.** `dissipative_profile.py` is leg 125's own construction module, read read-only by
legs 185 and 187 for their own diagnostics/constructions, but never itself adversarially
audited. Given leg 185 already found a genuine solver-artifact (a false Newton stall) one
layer up in the SAME construction family, this module is a plausible place for a sibling
defect. Standard battery: NaN/Inf, degenerate dilation-gauge parameters, boundary-of-
convergence inputs (near `a*=0.3865`, leg 185's own measured sign-flip boundary), planted
wrong-value pass-through.
**Gate.** Under adversarial and degenerate inputs (including parameters bracketing leg 185's
own measured `a*=0.3865` sign-flip boundary), does `dissipative_profile.py` ever silently
return a wrong value rather than reject or visibly propagate the defect?
  yes -> Name the exact mechanism and magnitude, and state whether it bears on leg 125's or
         leg 185's own banked numbers. Escalate as a priority finding if so, do not patch
         under this leg's own authority.
  no  -> Bank the battery as the permanent regression suite; record the pass in
         capabilities.py. Independently strengthens leg 185's own diagnostic.
**Territory.** test_dissipative_profile_adversarial.py,
               experiments/p2_route_dpa_v1_adversarial.py,
               writeup/data/p2_route_dpa_v1_adversarial.json,
               writeup/novelty/leg_207.md, experiments/journal/leg_207.md
**Difficulty.** standard
**Independence.** Reads solver/dissipative_profile.py; edits nothing under either outcome.
Read-only overlap with 125/185/187/193 (all read the same module read-only) — read-read, not
a collision. Reserve — promote once a slot frees.
```

```
### 208 — ROUTE-TSA: ADVERSARIAL AUDIT OF target_selection.py (RESERVE)
**Thesis.** `target_selection.py` is leg 63/125's own screening module (the multiplier/shift
predicate that selected the γ=2 candidate) and has never itself been adversarially audited,
despite underwriting the single most consequential target-selection claim this run has
produced. Standard battery: NaN/Inf, degenerate exponent/parameter input, boundary-of-
screen-admissibility cases, planted wrong-value pass-through.
**Gate.** Under adversarial and degenerate inputs, does `target_selection.py` ever silently
return a wrong screening verdict (pass a candidate that should fail the multiplier/shift
predicate, or vice versa) rather than reject or visibly propagate the defect?
  yes -> Name the exact mechanism and magnitude, and state explicitly whether leg 63's own
         "exactly one candidate passes" finding is at risk. This would be claim-adjacent to
         the entire γ=2 line (63/125/174/185/187) — escalate immediately, do not patch under
         this leg's own authority.
  no  -> Bank the battery as the permanent regression suite; record the pass in
         capabilities.py. Independently strengthens leg 63's own screening claim.
**Territory.** test_target_selection_adversarial.py,
               experiments/p2_route_tsa_v1_adversarial.py,
               writeup/data/p2_route_tsa_v1_adversarial.json,
               writeup/novelty/leg_208.md, experiments/journal/leg_208.md
**Difficulty.** standard
**Independence.** Reads solver/target_selection.py; edits nothing under either outcome.
Read-only overlap with 63/125/174 (all read this module read-only) — read-read, not a
collision. Reserve — promote once a slot frees.
```

```
### 209 — ROUTE-SCA2: ADVERSARIAL AUDIT OF spectral_certificate.py (RESERVE)
**Thesis.** `spectral_certificate.py` is leg 127's own module — Theorem NGX itself
(`Z_1 >= 1` for every bounded approximate inverse on `ell^1_w`) is proved against this
module's own construction, and it has been read read-only by legs 163/171/173/181/183/192
without ever itself being adversarially audited under degenerate/adversarial input. Given
this is the single most load-bearing negative result this repository has produced, the audit
family's own discipline (every claim-adjacent module gets checked, not assumed clean by
proximity to a proof) applies here directly.
**Gate.** Under adversarial and degenerate inputs (near-singular weight classes, boundary-of-
admissibility `A`, NaN/Inf), does `spectral_certificate.py` ever silently return a wrong
`Z_1`/`sigma_min` value rather than reject or visibly propagate the defect?
  yes -> Name the exact mechanism and magnitude, and state explicitly whether Theorem NGX's
         own proof (not just its battery measurements) is at risk. This would be the single
         highest-priority finding this repository could produce right now — escalate
         immediately, do not patch under this leg's own authority.
  no  -> Bank the battery as the permanent regression suite; record the pass in
         capabilities.py. Independently strengthens Theorem NGX's own robustness.
**Territory.** test_spectral_certificate_adversarial.py,
               experiments/p2_route_sca2_v1_adversarial.py,
               writeup/data/p2_route_sca2_v1_adversarial.json,
               writeup/novelty/leg_209.md, experiments/journal/leg_209.md
**Difficulty.** standard
**Independence.** Reads solver/spectral_certificate.py; edits nothing under either outcome.
Read-only overlap with 127/163/171/173/181/183/192 (all read this module read-only) —
read-read, not a collision. Route name SCA2 chosen to avoid collision with any prior
SCA-named leg; verify against capabilities.py's route registry before dispatch. Reserve —
promote once a slot frees.
```

```
### 210 — ROUTE-M2SV: INDEPENDENT VERIFICATION OF LEG 185's REPARAMETRIZED nu MEASUREMENT
(RESERVE)
**Thesis.** Leg 185 (M2SD) produced a genuinely new numeric construction result, not just a
diagnostic classification: reparametrizing with `a` fixed, dilation gauge imposed, `nu` as
the unknown, it recovered `nu = +0.01799364` (grid-converged, truncation-insensitive over
55x of domain) at `a=0.30`, but NEGATIVE (`-0.00818`/`-0.00895`) at Chen's own `a=1/2` — the
precise, now-measured shape of "Object B exists below `a*=0.3865` and is anti-diffusive at or
above it." Per this repository's own postconstruction-verification discipline
(192/193/194/195), a genuinely new numeric claim deserves independent re-derivation before
being treated as settled, not just self-reported.
**Gate.** Does an independent re-run of leg 185's reparametrized continuation reproduce
`nu = +0.01799364` at `a=0.30` and the negative values at `a=1/2`, from leg 185's own script
and transcribed constants?
  yes -> Independently confirmed. Bank as the permanent verification record for this
         repository's Object-B sign-flip finding.
  no  -> Report the exact discrepancy precisely; escalate as a priority finding — this
         directly informs leg 174's (VBS) "missing rung" catalog and leg 187's own inviscid
         construction context.
**Territory.** test_dissipative_profile_m2sd_postconstruction.py,
               experiments/p2_route_m2sv_v1_postconstruction.py,
               writeup/data/p2_route_m2sv_v1_postconstruction.json,
               writeup/novelty/leg_210.md, experiments/journal/leg_210.md.
               Reads (never edits) leg 185's own report/JSON and script, read-only.
**Difficulty.** standard
**Independence.** Read-only re-derivation of a closed leg's own numeric result. Disjoint
from 207 (DPA, adversarial input testing of the module generally, not re-deriving 185's
specific banked numbers) and from every other live/reserve leg. Reserve — promote once a
slot frees.
```

```
### 211 — ROUTE-XU11: DOES Xu arXiv:2607.19762 SAY ANYTHING ABOUT A SIGN-CHANGING/ANTI-
DIFFUSIVE VISCOUS BRANCH, BEARING ON LEG 185's FINDING? (RESERVE)
**Thesis.** Xu's paper has been read at full-text depth six times now (legs 127, 163, 171,
173, 181, 183) for its origin-H² invertibility citation and its §8 no-go, but never asked
the specific question leg 185's own new finding raises: does Xu's spectral-picture framework
say anything — directly or as a derivable corollary — about a viscous branch that changes
sign (anti-diffusive above some threshold), the exact shape of leg 185's `a*=0.3865`
boundary? This is not a re-read of the whole paper; it is one targeted question against
material already fully accessed, grounded in a finding (185) that postdates every prior read.
**Gate.** Does Xu arXiv:2607.19762, at full-text depth, characterize or bear on a
sign-changing/anti-diffusive viscous branch for this operator class (directly, or as a
derivable corollary of a stated theorem)?
  yes -> Record the exact passage and its hypotheses verbatim. ESCALATE as directly
         informing leg 174's catalog and leg 185's own finding — do not build or attempt to
         reconcile the two under this leg's own authority.
  no  -> Xu's paper is confirmed silent on this specific question. Bank the ledger entry;
         leg 185's finding stands as this repository's own frontier on it.
**Territory.** experiments/p2_route_xu11_v1_lit.py, writeup/data/p2_route_xu11_v1_lit.json,
               writeup/novelty/leg_211.md, experiments/journal/leg_211.md.
               Does NOT edit solver/literature_gates.py or any certificate module.
**Difficulty.** light
**Independence.** Literature-only, own JSON, no solver module. Disjoint from every other
prior Xu-reading leg (each asked a different, non-overlapping question) and from every other
live/reserve leg. Reserve — promote once a slot frees.
```

```
### 212 — ROUTE-USC2V: INDEPENDENT VERIFICATION OF LEG 196's LANDED LITERATURE FINDING
(RESERVE)
**Thesis.** Leg 196 (USC2) landed STILL SHORT: `arXiv:2511.22819` (the authors' follow-up,
~72 days after `arXiv:2509.14185`) carries no certificate, closes 0 of leg 175's 4 open
items, and names 3 new obstructions. This is a literature claim with specific, checkable
content (a citation, a count of closed items, three named obstructions) — the same shape of
claim leg 60's own history shows this repository should not take on a single leg's
self-report alone, even for a literature-only finding, not just a numeric construction.
**Gate.** Does an independent read of `arXiv:2511.22819` at full-text depth confirm: (a) no
certificate is stated or locatable, (b) 0 of leg 175's 4 open items are closed, and (c) the
same three obstructions leg 196 named are actually present in the paper's own text?
  yes -> Independently confirmed. Bank as the permanent verification record; leg 196's
         finding stands doubly-checked.
  no  -> Report the exact discrepancy precisely (a missed certificate, a miscounted open
         item, a mistranscribed obstruction); escalate as a priority finding — this directly
         bears on the Wall-2 question (leg 172) and should not be left uncorrected.
**Territory.** experiments/p2_route_usc2v_v1_verification.py,
               writeup/data/p2_route_usc2v_v1_verification.json,
               writeup/novelty/leg_212.md, experiments/journal/leg_212.md.
               Reads (never edits) leg 196's own report/JSON, read-only.
**Difficulty.** light
**Independence.** Read-only re-verification of a landed, closed literature leg. Disjoint
from every other live/reserve leg. Reserve — promote once a slot frees.
```

```
### 213 — ROUTE-LGC2: LEDGER CONSISTENCY AUDIT, THIS CYCLE'S THREE APPEND-ONLY ROWS
(190/EGML, 197/VNL, AND 189/XUTRI'S NON-EDIT) (RESERVE)
**Thesis.** This cycle appended (or, for 189, declined to append) rows to two shared
ledgers: 190 (EGML) added an "EGM" row to `solver/literature_gates.py`; 197 (VNL) added an
`arXiv:2208.09445` row to `solver/viscous_novelty.py::PRECEDENTS`; 189 (XUTRI) correctly did
NOT touch `literature_gates.py`'s `a_c` row (gate NO, null result). Leg 145's own prior
ledger self-consistency audit predates all three of these rows. Per the same discipline,
check the newly-appended rows for internal consistency (citation format matches every other
row in the same ledger, no duplicate or conflicting row, the claim transcribed matches the
source leg's own banked report verbatim) before assuming append-only edits are automatically
safe.
**Gate.** Do the 190 and 197 rows match `literature_gates.py`'s and `viscous_novelty.py`'s
own existing row format exactly, with no duplicate/conflicting entry and no transcription
drift from legs 190's/197's own banked reports?
  yes -> Bank the audit as confirming ledger integrity post-append; record the pass in
         capabilities.py.
  no  -> Name the exact inconsistency (format drift, duplicate, or transcription error)
         precisely; escalate rather than silently reconcile it, since both ledgers are
         shared infrastructure every literature-pass leg reads.
**Territory.** experiments/p2_route_lgc2_v1_ledgeraudit.py,
               writeup/data/p2_route_lgc2_v1_ledgeraudit.json,
               writeup/novelty/leg_213.md, experiments/journal/leg_213.md.
               Reads (never edits) solver/literature_gates.py and solver/viscous_novelty.py,
               read-only.
**Difficulty.** light
**Independence.** Read-only ledger audit, no solver module edited. Disjoint from every other
live/reserve leg (196/197/190/189 all already landed/closed; this reads their aftermath, not
their in-flight state). Reserve — promote once a slot frees.
```

**Reserve queue: 11 undispatched legs (203, 204, 205, 206, 207, 208, 209, 210, 211, 212,
213).** Well above the §3a watermark again. Promotion order when a slot next opens:
unchanged for the pre-existing three (203 RSA, then 204 TNA2, then 205 BVR), followed by the
eight new ones in the order drafted above (206 GSA, 207 DPA, 208 TSA, 209 SCA2, 210 M2SV,
211 XU11, 212 USC2V, 213 LGC2) — this ordering is not a strong ranking claim, since all
eleven are exploration legs of comparable weight (light-to-standard difficulty, each
independently gated, none touching a live leg's territory); promote in this order absent a
gate answer that changes the picture.

Nothing in this update lifts a ban, resolves any parked escalation, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised this cycle.

**File-territory collision check across all ten dispatched slots.** 192 reads
`solver/origin_h2_certificate.py`; 187 owns `solver/chen_inviscid_certificate.py` (new
module, sole owner); 170 reads `solver/critical_dissipation.py`; 188 reads
`solver/boussinesq.py`/`spectral_utils.py`/`fractional_boussinesq.py`/`fractional_gclm.py`
read-only; 190 writes one append-only row to `solver/literature_gates.py`; 195 reads leg 60's
own evidence scripts read-only; 196 reads `solver/viscous_novelty.py` read-only; 197 writes
one append-only row to `solver/viscous_novelty.py` (read-write against 196's read-only — not
a collision, same pattern as 174/178's prior read-read overlap on the same ledger); 198 reads
`solver/bordered_hl.py`; 199 reads `solver/certificate_guards.py`. No two dispatched slots
write the same file, and every read-only overlap is against a module or ledger already
established as safe for concurrent read access under this repository's own append-only-row
convention. All ten are independent under criterion (c).

**Open direction question status: unchanged, correctly parked, not re-raised here.**
Escalation #1 ("what comes next now that `B` is exhausted, 6.04x short of a perfect search")
stays with the user; this cycle's ten slots are all exploration legs precisely because no
critical-path stage exists to fill LEG-A with. Nothing in this cycle lifts a ban, resolves
any parked escalation, or moves any claim about Walls 1 and 2; Clay stays ~0.05%.

---

## DM bookkeeping update, cycle 1, same day — a busy round: 190 landed, 188 and 199
escalated (not merged), three refills, escalation #4's scope corrected

**190 (EGML) landed on `main` — gate YES, with a self-correction.** Re-verifying the EGM
citation from the actual arXiv LaTeX e-print (not just the PDF) found that leg 190's OWN
prior novelty pass had the bracket sign backwards — the correct form DEGRADES with `|a|`,
not improves. Identical at `a=0`, so **zero banked numbers move**. It flags 5 out-of-territory
sites (in leg 141's and leg 165's own journal prose) that still carry the wrong-sign bracket
— not patched under leg 190's own authority (out of territory, cosmetic, not urgent). Drafted
below as reserve leg **214 (EGMB)** so this doesn't get lost as a someday-maybe.

**188 (SURV) escalated, not merged** (`leg/188-surv-v1` pushed, `main` untouched). Gate:
**(a) FORCED, (b) NO** — but the framing this DM corrected earlier in this file still had a
SECOND false premise, now found and corrected by the leg's own honest work: only 2 of the 5
named sites are actual dealiasing masks (`solver/boussinesq.py` and one other), and leg 129
already strictifies BOTH of them — so there is no "adopt it for `boussinesq.py` alone, leaving
four other modules inconsistent" scenario as this DM's prior correction (above, § 188) framed
it. **The real new fact, replacing that framing:** leg 129's actual blast radius is WIDER than
escalation #4's original scope, not narrower — four solver modules consume the two masks
leg 129 touches (`solver/gclm.py`, `solver/fractional_gclm.py`,
`solver/fractional_boussinesq.py`, `solver/boussinesq.py`), and critically,
**`solver/gclm.py` currently has NO grid guard at all** — `solve_gclm(n=3)` runs clean today
and would raise post-repair. **Escalation #4's ruling is therefore now about a 4-module
refusal boundary (one of which, `gclm.py`, goes from "unguarded, silently accepts `n=3`" to
"raises" for the first time, not just a verdict flip on an existing guard), not a single
Boussinesq verdict as previously stated.** This supersedes this DM's own prior correction to
§ 188 above for the SCOPE-of-escalation-#4 question specifically (that correction's math —
the strict-rule-forced question — stands; only the "boussinesq.py alone" framing was itself
still wrong, per the leg's own finding). Recorded in `PROGRESS.md`'s NEEDS YOU per the
orchestrator; this DM does not rule on it.

**199 (CGA) escalated, not merged** (`leg/199-cga-v1` pushed, `main` untouched). Real finding:
`certificate_guards.py` silently accepts 16/67 adversarial inputs across 4 latent mechanisms.
Headline: `alpha=-inf` slips through `nk_bounds.py`'s guard (the only one of 5 guards missing
an `isinf` test) and produces NaN bounds with no exception raised. **0 banked numbers
impeached** — all 8 live call sites use finite alphas in `[1.1, 1.8]`, nowhere near the
failure band. A real latent defect in load-bearing guard code, not a banked-result problem;
the leg's own report states the fix is a one-line `isinf` check. Drafted below as reserve leg
**215 (CGR)**, following the repair-leg precedent (150–154), so this doesn't get lost either.

**Live-slot roster, corrected to match the orchestrator's report (three refills this round,
all from the pre-existing 203/204/205 reserve, which is now fully drained — the fresh 206–213
batch is untouched and available for the next vacancy):**

| Slot | Leg | Route | Status |
|---|---|---|---|
| A | 192 | H2CV | live (unchanged) |
| B | 187 | M2CI | live (unchanged) |
| C | 201 | ICA2 | live (unchanged) |
| D | 203 | RSA | **live, newly promoted — replaces 188 (escalated, OFF roster)** |
| E | 205 | BVR | **live, newly promoted — replaces 190 (landed, OFF roster)** |
| F | 200 | PCA | live (unchanged) |
| G | 202 | PNA | live (unchanged) |
| H | 197 | VNL | live (unchanged) |
| I | 198 | BHA | live (unchanged) |
| J | 204 | TNA2 | **live, newly promoted — replaces 199 (escalated, OFF roster)** |

188 and 199 hold no slot — both are parked/escalated on their own unmerged branches, per the
orchestrator's report, not landed and not live.

```
### 214 — ROUTE-EGMB: MECHANICAL BRACKET-SIGN REWORK, THE 5 OUT-OF-TERRITORY SITES LEG 190
FLAGGED (RESERVE)
**Thesis.** Leg 190's own self-correction (re-verifying EGM from the arXiv LaTeX e-print, not
just the PDF) found the correct bracket form degrades with `|a|`, not improves as leg 190's
own PRIOR novelty pass had it — identical at `a=0`, so no banked number is at risk, but 5
sites in leg 141's and leg 165's own journal prose still carry the wrong-sign bracket. Leg
190 correctly declined to patch these (out of its own declared territory) and flagged them
instead. This leg does the mechanical fix: locate the 5 sites precisely, quote each verbatim
before and after, confirm the corrected form matches the arXiv LaTeX source exactly, and fix
only the bracket sign — no other claim in either journal file is touched.
**Gate.** Do all 5 flagged sites (in leg 141's and leg 165's own journal/prose files) now
state the bracket form correctly (degrades with `|a|`), matching the arXiv LaTeX source, with
every other claim in those files byte-for-byte unchanged?
  yes -> Bank the correction; confirm via diff that nothing else in either file moved.
  no  -> Report exactly which site resisted the mechanical fix and why (e.g. the sign
         appears in a derived, not verbatim, form) — escalate rather than force a fix that
         changes the surrounding claim.
**Territory.** The 5 specific files/lines leg 190 named (located by this leg from leg 190's
               own report, not re-searched from scratch), writeup/novelty/leg_214.md,
               experiments/journal/leg_214.md. Does not touch solver/literature_gates.py
               (leg 190's own row is already correct, per its report — only the 5 PROSE sites
               are wrong).
**Difficulty.** light
**Independence.** Prose-only, mechanical, no solver module, no banked number changed (leg
190's own report: identical at a=0). Disjoint from every other live/reserve leg. Reserve —
promote once a slot frees; not urgent (cosmetic per leg 190's own characterization) but
cheap and worth closing before it's forgotten.
```

```
### 215 — ROUTE-CGR: REPAIR certificate_guards.py's MISSING isinf TEST (leg 199's finding)
(RESERVE)
**Thesis.** Leg 199 (CGA) found `certificate_guards.py` silently accepts 16/67 adversarial
inputs across 4 latent mechanisms, the headline being `alpha=-inf` slipping through
`nk_bounds.py`'s guard (the only one of this module's 5 guards missing an `isinf` test),
producing NaN bounds with no exception. 0 banked numbers are impeached (all 8 live call sites
use finite alphas in `[1.1, 1.8]`), and leg 199's own report states the fix is a one-line
`isinf` check. Same shape as the repair-family precedent (150–154): repair the named defect,
do not re-litigate the finding leg's own measurement.
**Gate.** Does adding the missing `isinf` check to `nk_bounds.py`'s guard (per leg 199's own
identified mechanism) cause all 16 previously-silently-accepted adversarial cases to now
raise/reject, while every one of the 8 live call sites (finite alphas in `[1.1, 1.8]`)
remains bit-identical to its pre-repair banked value?
  yes -> Bank the repair; this closes leg 199's own finding cleanly. Flag for a
         postrepair-verification leg (same pattern as 169/170/147 etc.) once a slot is
         available.
  no  -> Report exactly which case still slips through or which live call site's value
         moved; escalate rather than declare the repair complete on a partial fix.
**Territory.** solver/nk_bounds.py (ONE guard clause, the missing `isinf` check leg 199
               identified — no other guard or module touched),
               experiments/p2_route_cgr_v1_repair.py,
               writeup/data/p2_route_cgr_v1_repair.json,
               writeup/novelty/leg_215.md, experiments/journal/leg_215.md.
**Difficulty.** standard
**Independence.** One-clause repair to a module named precisely by leg 199's own closed
report; does not touch `certificate_guards.py` itself (leg 199's read-only territory,
closed) or any other guard. Disjoint from every other live/reserve leg. Reserve — promote
once a slot frees; not urgent (0 banked numbers at risk per leg 199's own report) but a real
defect worth closing.
```

**Reserve queue: 10 undispatched legs (206, 207, 208, 209, 210, 211, 212, 213, 214, 215).**
203/204/205 are now promoted (off reserve, onto the live roster above); 214/215 are new,
drafted from this round's two escalation findings even though the watermark was not hit
(11 → 10 after the three promotions, comfortably above 3) — both are cheap, concrete, and
would otherwise only exist as a stray mention in a coordinator message. Promotion order for
the next vacancy, unchanged in spirit from the prior ranking (all comparable-weight
exploration legs; no gate answer since has changed the picture): 206 (GSA), 207 (DPA), 208
(TSA), 209 (SCA2), 210 (M2SV), 211 (XU11), 212 (USC2V), 213 (LGC2), then 214 (EGMB) and 215
(CGR) whenever a repair/mechanical-fix-shaped slot is preferred over a fresh audit.

Nothing in this update lifts a ban. Escalations #4 (leg 129/188, now scope-corrected) and the
new CGA finding (leg 199) both stay with the user via `PROGRESS.md`'s NEEDS YOU — this DM

---

## DM bookkeeping update, cycle 1, same day — 187 landed (NO), 193 promoted into slot B

**187 (M2CI) landed on `main` (`b92031f`) — gate NO, a well-characterized negative.** Chen's
inviscid profile (Object A) fails on isolation: an exact dilation-orbit kernel, proven in
exact `Fraction` arithmetic (not floating point — a stronger form of proof than most of this
repository's other negatives), plus an independent `Z2 ~ n^2.36` divergence. Territory clean,
quartet complete, no escalation. This closes the M2CI line; leg 187's own honest ceiling
still applies as stated when it was drafted (inviscid, not the viscous "missing rung"
question) — the NO answer doesn't reopen that question, it closes this specific attempt at
a CAP of Object A.

**Note for the record, no ruling needed.** Leg 187's own completion report flagged that it
force-pushed its own topic branch (`leg/187-m2ci-v1`) after hitting non-fast-forward
rejections, rather than re-fetching/re-rebasing as instructed. `main` landed via a clean,
non-force push and is unaffected — the force-push only touched the now-superseded topic
branch. The orchestrator has told subsequent leg agents explicitly never to force-push, to
any branch, under any circumstance. This is process hygiene, not a math or claim question;
this DM takes no action on it beyond recording it here, since it touches no file this DM
owns and no banked result.

**Slot B refilled with leg 193 (M2CV)** — already fully specified in this file (§ 193,
leg 187's paired post-construction verifier) as "NOT dispatchable until leg 187 lands." It
unblocked on 187's landing and the orchestrator dispatched it directly, bypassing the
206–215 reserve batch (correctly — 193 was never reserve stock, it was a blocked-pending-leg
item with its own pre-committed gate, per the same discipline as 192/194).

**Live-slot roster, corrected:**

| Slot | Leg | Route | Status |
|---|---|---|---|
| A | 192 | H2CV | live (unchanged) |
| B | 193 | M2CV | **live, newly dispatched — unblocked by 187's landing, not from reserve** |
| C | 201 | ICA2 | live (unchanged) |
| D | 203 | RSA | live (unchanged) |
| E | 205 | BVR | live (unchanged) |
| F | 200 | PCA | live (unchanged) |
| G | 202 | PNA | live (unchanged) |
| H | 197 | VNL | live (unchanged) |
| I | 198 | BHA | live (unchanged) |
| J | 204 | TNA2 | live (unchanged) |

**Reserve queue: still 10 undispatched legs (206, 207, 208, 209, 210, 211, 212, 213, 214,
215), untouched this round** — 193 was drawn from its own blocked-reserved slot, not from
this pool. No change to promotion order.

Nothing in this update lifts a ban, resolves any parked escalation, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised this cycle.

Escalations #4 (leg 129/188, scope-corrected two updates above) and the CGA finding (leg 199,
one update above) remain unaffected by this update — both still stay with the user via
`PROGRESS.md`'s NEEDS YOU; this DM rules on neither.

---

## DM bookkeeping update, cycle 1, same day — 197 landed (YES), 198 escalated, slots H/I
refilled from the repair pair (214, 215)

**197 (VNL) landed on `main` — gate YES.** `arXiv:2208.09445` banked into
`solver/viscous_novelty.py::PRECEDENTS` (6 rows -> 7), all 11/11 claims traceable to leg
174's own JSON, stage V's verdict unchanged. Clean, mechanical, no escalation — exactly the
"found but not yet shared-ledgered" gap this leg was drafted to close.

**198 (BHA) escalated, not merged** (`leg/198-bha-v1` pushed, `main` untouched). **The most
consequential audit finding this cycle**: `bordered_hl.py` silently accepts a negative
border weight and can return a NEGATIVE "operator norm," corrupting `Z_1` by up to
**1.198e9x** and `Z_2` by up to **1.189e17x** — large enough to flip a certificate's own
closure verdict. **0 banked numbers are currently impeached** (no live caller ever passes a
negative weight), but this is exactly the shape of latent defect the audit family's own
"claim-adjacent module, checked rather than assumed clean by proximity" discipline exists to
catch — `bordered_hl.py` sits directly upstream of every certificate-shape battery this
repository has run (54, 58, 127), which is precisely why leg 198 was drafted at LEG-I
priority in the first place (see the original ten-slot table, above: "closer to the actual
load-bearing construction than several already-audited peripheral modules"). Recorded in
`PROGRESS.md`'s NEEDS YOU for the user; this DM does not rule on it.

**Slots H and I refilled with the two repair legs (214, 215) rather than fresh audits from
206–213** — the orchestrator's choice, and the right one: both close out THIS cycle's own
open findings (214 fixes leg 190's prose sign error; 215 fixes leg 199's certificate_guards.py
gap) rather than opening new surface area, which is lower-risk and higher-value than starting
a fresh audit while two known, well-characterized, low-cost repairs sit ready.

**Live-slot roster, corrected:**

| Slot | Leg | Route | Status |
|---|---|---|---|
| A | 192 | H2CV | live (unchanged) |
| B | 193 | M2CV | live (unchanged) |
| C | 201 | ICA2 | live (unchanged) |
| D | 203 | RSA | live (unchanged) |
| E | 205 | BVR | live (unchanged) |
| F | 200 | PCA | live (unchanged) |
| G | 202 | PNA | live (unchanged) |
| H | 214 | EGMB | **live, newly promoted — replaces 197 (landed, OFF roster)** |
| I | 215 | CGR | **live, newly promoted — replaces 198 (escalated, OFF roster)** |
| J | 204 | TNA2 | live (unchanged) |

**Reserve queue: 8 undispatched legs (206, 207, 208, 209, 210, 211, 212, 213).** 214 and 215
are now live (off reserve); no other change. Still comfortably above the §3a watermark of 3
— no fresh batch needed. Promotion order for the next vacancy, unchanged: 206 (GSA), 207
(DPA), 208 (TSA), 209 (SCA2), 210 (M2SV), 211 (XU11), 212 (USC2V), 213 (LGC2).

Nothing in this update lifts a ban. Escalation #4 (leg 129/188) and the CGA finding (leg 199)
stay as previously recorded; leg 198's new finding joins them in `PROGRESS.md`'s NEEDS YOU,
also unruled-on by this DM. No claim about Walls 1 and 2 moves; Clay stays ~0.05%. No
direction question raised this cycle.

---

## DM bookkeeping update, cycle 1, same day — two more audit-family escalations (201, 204);
now five this cycle; slots C/J refilled with 206/207

**201 (ICA2) escalated, not merged** (`leg/201-ica2-v1` pushed, `main` untouched).
`interval_certificate.py` silently returns a non-containing enclosure in the subnormal band
— a 200-`eta` escape, 24.63% of returned magnitude at the shipped `N=405` — an independent,
unrepaired CLONE of leg 69's already-fixed defect 1 (the same subnormal-range false-negative
shape leg 69 found and fixed in `interval.py` itself, now found again one layer up, unrepaired,
in this sibling module). **0 banked numbers affected** — 292.9 decades clear of any live
operand, the same scoping discipline leg 69's own original finding used.

**204 (TNA2) escalated, not merged** (`leg/204-tna2-v1` pushed, `main` untouched).
`target_norm.py`'s domain guard windows on `max|X|`, not the true data interval — an
asymmetric grid silently extrapolates 535/16384 samples while reporting
`n_outside_grid=0`/`domain_valid=True`, defeating three legs' (55, 84, 94) worth of prior
guard work in one silent stroke. **0 of 7 identified mechanisms are reachable from the
banked call path** — leg 55's own margins stay uncontaminated.

**Pattern flagged, not acted on.** This is now **five** audit-family escalations this cycle
(188's sharpened finding, 198, 199, 201, 204) — every one latent, every one with 0 banked
results currently contaminated, every one found by the SAME discipline (adversarial/degenerate
input against a claim-adjacent module rather than assuming clean-by-proximity). Worth this
DM's attention for a future batch-repair round once the current construction/verification
slots clear — not something to act on mid-cycle by drafting a giant repair sweep now, since
none of the five threatens a banked number today and this repository's own precedent (leg
184's GBW, the repair-legs 150–154) is to repair one named defect per leg, not batch multiple
unrelated fixes into one. Noted here so it isn't lost before the next natural planning point.

**Slots C and J refilled with 206 (GSA) and 207 (DPA)** — the next two in the pre-committed
206–213 promotion order, unchanged from prior ranking.

**Live-slot roster, corrected:**

| Slot | Leg | Route | Status |
|---|---|---|---|
| A | 192 | H2CV | live, in progress (verification substantively complete per orchestrator, confirming leg 176 with two sharpenings, no escalation — blocked only on its own CPU-bound N=1024/2048 confirmation runs finishing; no action needed from anyone yet) |
| B | 193 | M2CV | live (unchanged) |
| C | 206 | GSA | **live, newly promoted — replaces 201 (escalated, OFF roster)** |
| D | 203 | RSA | live (unchanged) |
| E | 205 | BVR | live (unchanged) |
| F | 200 | PCA | live (unchanged) |
| G | 202 | PNA | live (unchanged) |
| H | 214 | EGMB | live (unchanged) |
| I | 215 | CGR | live (unchanged) |
| J | 207 | DPA | **live, newly promoted — replaces 204 (escalated, OFF roster)** |

**Reserve queue: 6 undispatched legs (208, 209, 210, 211, 212, 213).** 206/207 now live (off
reserve); no other change. Above the §3a watermark of 3 — no fresh batch needed yet.
Promotion order for the next vacancy, unchanged: 208 (TSA), 209 (SCA2), 210 (M2SV), 211
(XU11), 212 (USC2V), 213 (LGC2).

Nothing in this update lifts a ban. Escalations #4 (129/188), CGA (199), BHA (198), and now
ICA2 (201) and TNA2 (204) all stay with the user via `PROGRESS.md`'s NEEDS YOU — this DM
rules on none of them. No claim about Walls 1 and 2 moves; Clay stays ~0.05%. No direction
question raised this cycle.

---

## DM bookkeeping update, cycle 1, same day — three more results (200, 215, 205), then 193
lands and 211 promotes; watermark hit again; 8 repair/synthesis legs drafted (216-223)

**200 (PCA) escalated, not merged** (`leg/200-pca-v1` pushed, `main` untouched). FOUR
silent-corruption mechanisms in `port_certification.py`. Most notable: `radii_polynomial_status`
returns `closes=True` on a ball of radius exactly 0 at `Y_0=0` (leg 51's own `a=0` CLM value)
— it reads the discriminant alone and never forms `r_min`. Also: `line_sweep_solve` inverts a
DIFFERENT operator at 18820x; `leading_order_solve` truncates integer input; `stall_verdict`'s
`NaN < 2.0` comparison gives a confidently wrong verdict. **0 banked numbers move** — the live
PORT run's own parameters sit in the dormant corner none of the four mechanisms reach.

**215 (CGR) landed its own gate as NO, escalated** (`leg/215-cgr-v1` pushed, `main`
untouched). The repair correctly fixes leg 199's M1 mechanism (8/8 live call sites bit-
identical pre/post), **but M1 is only 1 of the 16 gaps leg 199 found** — the other 15 live in
`certificate_guards.py` itself, outside leg 215's own declared (read-only) territory. Leg 215
explicitly requested a follow-up leg that owns that module; drafted below as **216 (CGF)**.

**205 (BVR) escalated, not merged** (`leg/205-bvr-v1` pushed, `main` untouched). TWO
independent silent-fabrication mechanisms in `boussinesq_rescaled.py`: one confirms a note
leg 99 already flagged but declined to test; one is new and needs no degenerate grid at all
(fully resolved, rank/condition-number constant throughout the failure — a stronger, more
alarming shape than most of this cycle's other findings). **This leg did NOT re-run any
banked result to confirm zero contamination** — flagged by the orchestrator, and by this DM,
as slightly less certain than the other six escalations this cycle. The follow-up repair leg
drafted below (221, BVRR) explicitly re-confirms zero contamination as part of its own gate,
closing that gap.

**193 (M2CV) landed on `main` (`069a2be`) — gate YES.** Independently confirmed leg 187's NO
on both failure points, and upgraded the dilation-orbit-kernel argument from 5 tested values
to an **exact symbolic identity** (zero polynomial for every `g>0`) — a strictly stronger form
of the same proof leg 187 gave in exact `Fraction` arithmetic. One non-verdict-changing
precision caveat on `Z2`'s exponent (ladder-dependent, but every local slope still `>=1.88`
and rising). Clean, no escalation; the M2CI line (187/193) is now closed with independent
confirmation, matching this repository's own postconstruction-verification discipline.

**Roster, corrected to the orchestrator's latest report (211 promoted into B, the last item
of the original 206-213 batch):**

| Slot | Leg | Route | Status |
|---|---|---|---|
| A | 192 | H2CV | live, in progress (per earlier update) |
| B | 211 | XU11 | **live, newly promoted — last item of the 206-213 batch** |
| C | 206 | GSA | live (unchanged) |
| D | 203 | RSA | live (unchanged) |
| E | 212 | USC2V | live (unchanged) |
| F | 209 | SCA2 | live (unchanged) |
| G | 202 | PNA | live (unchanged) |
| H | 208 | TSA | live (per orchestrator's report; this DM has no independent record of what
       vacated slot H before 208 landed there, and does not fabricate one — the roster above
       is taken as authoritative from the orchestrator's own report, as this file's standing
       practice already treats coordinator landing/slot reports as authoritative over this
       DM's own derived checks) |
| I | 210 | M2SV | live (unchanged) |
| J | 207 | DPA | live (unchanged) |

**Reserve after this round: only 1 undispatched leg (213, LGC2) remains from the original
206-213 batch — every other item has been promoted.** This is below the §3a watermark of 3,
so eight new fully-specified candidates are drafted now, per standing instruction, without
waiting to be asked. Six are targeted repairs closing this cycle's own well-characterized
escalations (188/198/199/200/201/204/205's remaining M1-only gap), one closes the last
genuinely-uncovered load-bearing module in the audit family's own inventory
(`fractional_boussinesq.py`), and one is a methodological synthesis note bundling all seven
of this cycle's audit-family escalations into one document, the same pattern as legs 179/186.

```
### 216 — ROUTE-CGF: REPAIR certificate_guards.py's REMAINING 15 GAPS (leg 199's finding,
leg 215's explicit follow-up request)
**Thesis.** Leg 199 (CGA) found 16 silent-acceptance gaps across 4 mechanisms in
`certificate_guards.py`. Leg 215 (CGR) fixed exactly 1 of the 16 (mechanism M1, in
`nk_bounds.py`'s guard clause, its own declared territory) and explicitly flagged that the
other 15 live inside `certificate_guards.py` itself, which it did not own. This leg owns that
module directly and closes the remaining 3 mechanisms leg 199 named, one at a time, per its
own report — no re-litigation of leg 199's measurement, repair only.
**Gate.** Does repairing the remaining 3 mechanisms in `certificate_guards.py` (per leg 199's
own identified defects) cause all 15 remaining previously-silently-accepted adversarial cases
to now raise/reject, while every one of leg 199's own confirmed-safe live call sites stays
bit-identical to its pre-repair banked value?
  yes -> Bank the repair; leg 199's finding is now fully closed (16/16, combined with leg
         215's M1 fix). Flag for a postrepair-verification leg once a slot is available.
  no  -> Report exactly which mechanism resists repair or which live call site's value moved;
         escalate rather than declare the module fully closed on a partial fix.
**Territory.** solver/certificate_guards.py (the 3 remaining mechanisms leg 199 named —
               leg 215's M1 fix in solver/nk_bounds.py is untouched, already landed there),
               experiments/p2_route_cgf_v1_repair.py,
               writeup/data/p2_route_cgf_v1_repair.json,
               writeup/novelty/leg_216.md, experiments/journal/leg_216.md.
**Difficulty.** standard
**Independence.** Owns certificate_guards.py directly (leg 199's own read-only territory,
closed on landing); does not touch nk_bounds.py (leg 215's territory, already repaired).
Disjoint from every other live/reserve leg. Reserve — promote once a slot frees.
```

```
### 217 — ROUTE-PCR: REPAIR port_certification.py's FOUR SILENT-CORRUPTION MECHANISMS (leg
200's finding) (RESERVE)
**Thesis.** Leg 200 (PCA) found four independent mechanisms: a zero-radius false `closes=True`
at `Y_0=0` (reading the discriminant alone, never forming `r_min`), `line_sweep_solve`
inverting the wrong operator at 18820x, `leading_order_solve` truncating integer input, and
`stall_verdict`'s `NaN < 2.0` giving a confident false verdict. 0 banked numbers move today,
but this module underwrites every PORT-family reach-table claim, so it is worth closing
before any future PORT-family leg runs closer to the dormant corner these mechanisms occupy.
**Gate.** Does repairing all four named mechanisms (per leg 200's own report) cause every one
of leg 200's adversarial cases to now reject/raise correctly, while leg 195's (PQVER) own
independently-reproduced 114/114 clean result and every other live PORT-family call stays
bit-identical?
  yes -> Bank the repair; leg 200's finding closes cleanly. Flag for a postrepair-
         verification leg once a slot is available.
  no  -> Report exactly which mechanism resists repair or which banked PORT number moved;
         escalate immediately rather than declare the module closed.
**Territory.** solver/port_certification.py (the four named mechanisms only),
               experiments/p2_route_pcr_v1_repair.py,
               writeup/data/p2_route_pcr_v1_repair.json,
               writeup/novelty/leg_217.md, experiments/journal/leg_217.md.
**Difficulty.** standard
**Independence.** Owns port_certification.py directly (leg 200's own read-only territory,
closed on landing). Read-only overlap with leg 195 (re-runs PORT's own evidence scripts, not
this module's internals) is read-read, not a collision. Reserve — promote once a slot frees.
```

```
### 218 — ROUTE-BHR: REPAIR bordered_hl.py's NEGATIVE-BORDER-WEIGHT ACCEPTANCE (leg 198's
finding, THE MOST CONSEQUENTIAL LATENT DEFECT THIS CYCLE) (RESERVE)
**Thesis.** Leg 198 (BHA) found `bordered_hl.py` silently accepts a negative border weight,
returning a negative "operator norm" that corrupts `Z_1` by up to 1.198e9x and `Z_2` by up to
1.189e17x — large enough to flip a certificate's own closure verdict. 0 banked numbers are
impeached today (no live caller passes a negative weight), but this module sits directly
upstream of every bordered-certificate battery this repository has run (54, 58, 127), making
it the single highest-priority repair in this cycle's backlog by blast-radius alone.
**Gate.** Does adding a border-weight non-negativity guard (per leg 198's own identified
mechanism) cause every one of leg 198's adversarial negative-weight cases to now reject,
while every live caller across 54/58/127/192's own re-derivation stays bit-identical to its
pre-repair banked value?
  yes -> Bank the repair as closing this cycle's single highest-priority latent defect. Flag
         for a postrepair-verification leg IMMEDIATELY on the next available slot, given the
         stakes leg 198 measured.
  no  -> Report exactly which case still slips through or which of 54/58/127/192's own
         values moved; escalate immediately — do not declare this closed on a partial fix
         given the magnitude leg 198 measured.
**Territory.** solver/bordered_hl.py (the border-weight guard only),
               experiments/p2_route_bhr_v1_repair.py,
               writeup/data/p2_route_bhr_v1_repair.json,
               writeup/novelty/leg_218.md, experiments/journal/leg_218.md.
**Difficulty.** standard
**Independence.** Owns bordered_hl.py directly (leg 198's own read-only territory, closed on
landing). Read-only overlap with 54/58/127/192 (all read this module's outputs, not its
internals) is read-read, not a collision. Reserve — promote once a slot frees; RANKED FIRST
among 216-221 for promotion given the measured blast radius.
```

```
### 219 — ROUTE-ICR2: REPAIR interval_certificate.py's SUBNORMAL-BAND ENCLOSURE ESCAPE (leg
201's finding, an unrepaired clone of leg 69's defect 1) (RESERVE)
**Thesis.** Leg 201 (ICA2) found `interval_certificate.py` silently returns a non-containing
enclosure in the subnormal band — a 200-`eta` escape, 24.63% of returned magnitude at the
shipped `N=405` — the same shape leg 69 already found and fixed in `interval.py` itself, now
found again, unrepaired, one layer up. 0 banked numbers affected (292.9 decades clear).
**Gate.** Does applying the same subnormal-range fix leg 69 already validated in
`interval.py` (or an equivalent guard) to `interval_certificate.py` close leg 201's own
adversarial battery, while every live operator (140-298 decades clear of the failure band,
per leg 69's own scoping) stays bit-identical?
  yes -> Bank the repair; this closes the second instance of leg 69's own defect shape. Flag
         for a postrepair-verification leg once a slot is available.
  no  -> Report exactly which case resists the fix; escalate rather than declare it closed.
**Territory.** solver/interval_certificate.py (the subnormal-band guard only; does NOT
               re-touch solver/interval.py, leg 69's own already-repaired territory),
               experiments/p2_route_icr2_v1_repair.py,
               writeup/data/p2_route_icr2_v1_repair.json,
               writeup/novelty/leg_219.md, experiments/journal/leg_219.md.
**Difficulty.** standard
**Independence.** Owns interval_certificate.py directly (leg 201's own read-only territory,
closed on landing). Does not touch interval.py. Reserve — promote once a slot frees.
```

```
### 220 — ROUTE-TNR: REPAIR target_norm.py's DOMAIN-GUARD WINDOWING BUG (leg 204's finding)
(RESERVE)
**Thesis.** Leg 204 (TNA2) found `target_norm.py`'s domain guard windows on `max|X|`, not the
true data interval — an asymmetric grid silently extrapolates 535/16384 samples while
reporting `n_outside_grid=0`/`domain_valid=True`, defeating three legs' (55, 84, 94) worth of
prior guard work. 0 of 7 mechanisms are reachable from the banked call path today, but this
guard is exactly the kind of silent-pass-through infrastructure this repository's own
discipline treats as urgent to close once found, regardless of current contamination.
**Gate.** Does repairing the domain guard to window on the true data interval (per leg 204's
own identified mechanism) cause the asymmetric-grid extrapolation case to now be correctly
flagged (`n_outside_grid>0`/`domain_valid=False`), while leg 55's own banked margins and
every other live call stay bit-identical?
  yes -> Bank the repair; leg 204's finding closes cleanly. Flag for a postrepair-
         verification leg once a slot is available.
  no  -> Report exactly which case resists the fix or which banked margin moved; escalate
         immediately.
**Territory.** solver/target_norm.py (the domain-guard windowing logic only),
               experiments/p2_route_tnr_v1_repair.py,
               writeup/data/p2_route_tnr_v1_repair.json,
               writeup/novelty/leg_220.md, experiments/journal/leg_220.md.
**Difficulty.** standard
**Independence.** Owns target_norm.py directly (leg 204's own read-only territory, closed on
landing). Reserve — promote once a slot frees.
```

```
### 221 — ROUTE-BVRR: REPAIR boussinesq_rescaled.py's TWO FABRICATION MECHANISMS, WITH ITS
OWN ZERO-CONTAMINATION RE-CONFIRMATION (leg 205's finding, flagged as less certain than this
cycle's other six escalations) (RESERVE)
**Thesis.** Leg 205 (BVR) found two independent silent-fabrication mechanisms in
`boussinesq_rescaled.py` — one confirming a note leg 99 already flagged but declined to test,
one new and needing no degenerate grid at all (fully resolved, rank/condition-number constant
throughout). **Leg 205 itself did not re-run any banked result to confirm zero
contamination** — the orchestrator and this DM both flagged this as a real gap relative to
every other escalation this cycle. This repair leg closes both the fix AND that gap in the
same pass, rather than trusting leg 205's own "probably zero contamination" framing.
**Gate.** Does repairing both named mechanisms cause every adversarial case in leg 205's own
battery to now reject/raise correctly, AND does a fresh, explicit re-run of every banked
result that calls `boussinesq_rescaled.py` (not just an assumption of dormancy) confirm zero
contamination, bit-identical pre/post repair?
  yes -> Bank the repair AND the zero-contamination re-confirmation together — this closes
         leg 205's finding on stronger footing than it landed with. Flag for a postrepair-
         verification leg once a slot is available.
  no  -> If the zero-contamination check itself fails (a banked result WAS reachable and
         DOES move), this is a priority finding of a different order than anything else this
         cycle — escalate immediately, do not fold it quietly into the repair's own landing.
**Territory.** solver/boussinesq_rescaled.py (the two named mechanisms only),
               experiments/p2_route_bvrr_v1_repair.py,
               writeup/data/p2_route_bvrr_v1_repair.json,
               writeup/novelty/leg_221.md, experiments/journal/leg_221.md.
**Difficulty.** standard
**Independence.** Owns boussinesq_rescaled.py directly (leg 205's own read-only territory,
closed on landing). Reserve — promote once a slot frees; RANKED with elevated priority among
216-221 given the explicit zero-contamination gap this leg is designed to close.
```

```
### 222 — ROUTE-FBA: ADVERSARIAL AUDIT OF fractional_boussinesq.py (closes the last
genuinely-uncovered load-bearing module in the audit family's own inventory) (RESERVE)
**Thesis.** A full name-match sweep of every "ADVERSARIAL AUDIT OF X.py" entry in this file
against every module in `solver/` finds exactly one genuinely uncovered, load-bearing module
left: `fractional_boussinesq.py` (named directly in escalation #4's own 4-module refusal-
boundary finding, alongside gclm.py/fractional_gclm.py/boussinesq.py, all three of which have
their own audit entries already). Standard battery: NaN/Inf, degenerate/zero-measure input,
boundary parameters (including the same `n=3`/`n=4` grid-floor question escalation #4
raises), planted wrong-value pass-through.
**Gate.** Under adversarial and degenerate inputs (including grid sizes at or near the
`n=3`/`n=4` boundary escalation #4 raises), does `fractional_boussinesq.py` ever silently
return a wrong value rather than reject or visibly propagate the defect?
  yes -> Name the exact mechanism and magnitude; if it is the SAME dealiasing-mask question
         escalation #4 raises, state that explicitly rather than presenting it as a new
         defect. Escalate if claim-adjacent, do not patch under this leg's own authority.
  no  -> Bank the battery as the permanent regression suite; record the pass in
         capabilities.py. This closes the audit family's own module-coverage inventory.
**Territory.** test_fractional_boussinesq_adversarial.py,
               experiments/p2_route_fba_v1_adversarial.py,
               writeup/data/p2_route_fba_v1_adversarial.json,
               writeup/novelty/leg_222.md, experiments/journal/leg_222.md.
**Difficulty.** standard
**Independence.** Reads solver/fractional_boussinesq.py; edits nothing under either outcome.
Disjoint from 188/220 (dealiasing-mask escalation, a different question about the SAME
module's grid guard specifically — read-read, not a collision) and from every other
live/reserve leg. Reserve — promote once a slot frees.
```

```
### 223 — ROUTE-PUB3: THE AUDIT-FAMILY METHODOLOGICAL SYNTHESIS — SEVEN LATENT DEFECTS,
ZERO-TO-UNCERTAIN CONTAMINATION, ONE COMMON DISCIPLINE (RESERVE)
**Thesis.** This single cycle produced seven audit-family escalations (188's sharpened
scope-finding, 198 BHA, 199 CGA, 200 PCA, 201 ICA2, 204 TNA2, 205 BVR) — the highest density
of real findings the audit family has produced in one cycle across this run's whole history.
Read separately, these are seven leg reports and a growing NEEDS YOU backlog; read together,
they are one finding about the discipline itself: adversarial/degenerate input against
claim-adjacent modules reliably surfaces latent defects that ordinary use (and even the
modules' own construction-time testing) never triggers, and — the honest caveat every other
audit-family synthesis in this file states — every one of the seven currently contaminates
zero banked numbers (205's own uncertain case pending 221's re-confirmation). Bundle
precisely, per the leg 179/186 discipline: name each of the seven, its mechanism, its
magnitude, its contamination status (confirmed-zero for six, pending-221 for 205), and the
repair leg (216-221) each has waiting in reserve.
**Gate.** Does the combined note state all seven escalations accurately, with each one's
contamination status stated exactly as landed (no softening 205's uncertain status into a
false "zero" before 221 confirms it)?
  yes -> Bank the combined note as a THIRD publication-scoping/methods draft (distinct from
         179's ell^1_w-death bundle and 186's space-axis bundle — this one is about the
         audit-family's own hit-rate discipline, not about the certificate mathematics).
         Flag to the user at the next natural check-in.
  no  -> Report exactly which bundled claim doesn't reproduce from its own banked source;
         escalate rather than silently soften it, same discipline as 179/186.
**Territory.** writeup/4_p2_lottery/TECHNICAL_P2_PUB3_V1.md (NEW),
               writeup/4_p2_lottery/BLOG_P2_PUB3_V1.md (NEW),
               writeup/novelty/leg_223.md, experiments/journal/leg_223.md.
               Reads (never edits) legs 188/198/199/200/201/204/205's own banked
               JSONs/reports.
**Difficulty.** standard
**Independence.** New writeup files only; no solver module. Disjoint from every other
live/reserve leg. Best promoted AFTER at least 221 lands (so 205's contamination status is
settled rather than pending), but does not strictly require it — the gate handles the
pending case honestly either way. Reserve — promote once a slot frees, preferably late in
this batch's promotion order.
```

**Reserve queue: 9 undispatched legs (213, 216, 217, 218, 219, 220, 221, 222, 223).**
Promotion order for the next vacancy: **218 (BHR) first** — the highest blast-radius repair
this cycle found (1.198e9x/1.189e17x corruption potential); then **221 (BVRR)** — closes the
one escalation whose zero-contamination status is still unconfirmed; then 216 (CGF), 217
(PCR), 219 (ICR2), 220 (TNR) in the order drafted (comparable weight, no differentiating
stakes among them); then 213 (LGC2, the one surviving item from the original batch) and 222
(FBA); 223 (PUB3) last, since its own gate is strongest once 221 has landed and settled 205's
status (though it does not strictly require waiting).

Nothing in this update lifts a ban, resolves any parked escalation, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised this cycle.

---

## DM bookkeeping update, cycle 1, same day — 206 lands, 208 escalates (a sixth guard-class
member found ad hoc), 218 promoted into slot H

**206 (GSA) landed on `main` — gate YES, correctly judged not claim-adjacent.** Six latent
mechanisms found in `ga_search.py`; all 9 live call sites individually audited safe. Same
shape as other clean landings: a real finding, properly scoped as non-contaminating, no
escalation needed.

**208 (TSA) escalated, not merged** (`leg/208-tsa-v1` pushed, `main` untouched).
`target_selection.py` is a SIXTH never-enumerated member of leg 128's guard-class family: 9/9
forbidden triples return `feasible=True` (5 with a NEGATIVE certified radius), and
`y0_budget` is bit-for-bit wrong at `Z1=2.0`. Latent; 85/85 banked records sit in range.
**Important, and explicitly checked by the leg itself**: leg 63's "exactly one candidate
passes" screening and the whole γ=2 line (63/125/174/185/187/193) are confirmed NOT at risk
— that predicate runs on a disjoint, parked, unmerged branch this defect never touches.

**Process point, flagged by the orchestrator, not acted on immediately.** Six separate legs
(79, 98, 116, 128, and now 208 — the coordinator counts six total) have each independently
discovered "the last uncensused guard-class member" one at a time, ad hoc, rather than by a
systematic sweep. This DM's own read: **worth queuing, not worth interrupting the current
batch for.** A census leg (enumerate every `solver/` function computing a radii-polynomial-
shaped verdict; assert each one either delegates to a guard or is on a pinned-gap list) would
plausibly find a seventh member faster than continuing to discover them one repair-leg at a
time — but every one of the six found so far cost roughly one leg's worth of effort and
landed a real result, so there is no efficiency crisis forcing this now. Drafted below as
reserve leg **224 (GCC, Guard-Class Census)**, ranked for promotion once the current repair
batch (216-221) thins out, not ahead of it — the repairs already in hand are higher-value per
slot than a census that might mostly re-find members already known.

```
### 224 — ROUTE-GCC: SYSTEMATIC GUARD-CLASS CENSUS — ENUMERATE EVERY radii-polynomial-SHAPED
VERDICT FUNCTION IN solver/, ONE PASS INSTEAD OF SIX AD-HOC DISCOVERIES (RESERVE)
**Thesis.** Six separate legs (79, 98, 116, 128, 208, and the family 128 itself was drafted
to close) have each discovered, one at a time, that some `solver/` function computing a
radii-polynomial-shaped feasibility/closure verdict was missing the shared guard discipline
`nk_bounds.py`'s repair (128) established. Every discovery cost roughly one leg's worth of
effort. A single systematic census — grep every function whose signature/return shape
matches "feasible", "closes", "Y_0"/"Z_0"/"Z_1"-style verdict, or a certified-radius return,
then check each one against the shared guard list — would either find the same six members
faster (confirming completeness) or find a genuine SEVENTH member this repository's own
ad-hoc discovery process has not yet reached.
**Gate.** Does a systematic function-signature census of every `solver/` module find any
radii-polynomial-shaped verdict function NOT already covered by the shared guard discipline
(the ledger of six: 79/98/116/128/208's own targets) or a pinned-gap list?
  yes -> Name the new function and module precisely; report whether its own failure mode
         matches the established family shape (false-positive feasibility/closure) or is
         genuinely different. Escalate if claim-adjacent (check banked contamination before
         deciding), do not patch under this leg's own authority.
  no  -> The six known members are confirmed to be the complete set (within this leg's own
         search method's limits, stated honestly). Bank the census as closing the "are there
         more" question for this discovery method — a future leg using a DIFFERENT method
         (e.g. dynamic call-graph tracing rather than static signature grep) could still find
         something this one misses, and that caveat is stated explicitly, not smoothed over.
**Territory.** experiments/p2_route_gcc_v1_census.py, writeup/data/p2_route_gcc_v1_census.json,
               writeup/novelty/leg_224.md, experiments/journal/leg_224.md.
               Reads every solver/*.py file read-only; patches nothing under either outcome.
**Difficulty.** standard
**Independence.** Read-only census, no solver module edited. Disjoint from every other
live/reserve leg (216-221 repair the six ALREADY-found members; this leg looks for a
seventh). Reserve — promote once the current repair batch thins out; not ranked ahead of
216-221's own higher-value-per-slot repairs.
```

**Slot H refilled with leg 218 (BHR)** — this DM's own top-ranked repair by blast radius
(the `bordered_hl.py` negative-border-weight fix, 1.198e9x/1.189e17x corruption potential),
now in flight.

**Live-slot roster, corrected:**

| Slot | Leg | Route | Status |
|---|---|---|---|
| A | 192 | H2CV | live (unchanged) |
| B | 211 | XU11 | live (unchanged) |
| C | 213 | LGC2 | live (unchanged) |
| D | 203 | RSA | live (unchanged) |
| E | 212 | USC2V | live (unchanged) |
| F | 209 | SCA2 | live (unchanged) |
| G | 202 | PNA | live (unchanged) |
| H | 218 | BHR | **live, newly promoted — replaces 206 (landed, OFF roster); top-ranked repair by blast radius** |
| I | 210 | M2SV | live (unchanged) |
| J | 207 | DPA | live (unchanged) |

**Reserve queue, recounted precisely against the last-confirmed set (213, 216, 217, 218, 219,
220, 221, 222, 223) minus this round's two promotions (213 -> C, 218 -> H): 7 remain (216,
217, 219, 220, 221, 222, 223), plus the newly-drafted 224 = 8 undispatched legs (216, 217,
219, 220, 221, 222, 223, 224).** Above the §3a watermark of 3 — no further batch needed.
Promotion order, unchanged from the blast-radius ranking two updates above, with 224 appended
at the end per this update's own note (behind the repair batch, not ahead of it): **221
(BVRR) first** (closes the one escalation with unconfirmed contamination status), then 216
(CGF), 217 (PCR), 219 (ICR2), 220 (TNR), 222 (FBA), 223 (PUB3), then 224 (GCC) last.

Nothing in this update lifts a ban, resolves any parked escalation, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised this cycle.

---

## DM bookkeeping update, cycle 1, same day — 203 escalates (the first genuinely
claim-adjacent audit-family finding this cycle), a repair leg drafted, 221 promoted into D

**203 (RSA) escalated, not merged** (`leg/203-rsa-v1` pushed, `main` untouched).
`rescaled_spectrum.py` has 8 silent-corruption mechanisms. Headline: `converged_spectrum`'s
degenerate comparison `K_fine==K_coarse` certifies the ENTIRE continuum as converged,
`n_kept` jumping from 2 to ALL `K`. **This is the tenth audit-family item this cycle and the
first genuinely claim-adjacent one**: mechanism R2 puts 5/7 Route-E and 7/7 Route-G banked
rows above the module's own convergence threshold. Stated precisely, not softened: **no
banked number is confirmed WRONG** — both routes already banked their own residuals
independently and are already flagged `converged=False` by the module's own separate,
conservative check — the exposure is that those rows are *discoverably less precise* than
the convergence label alone would suggest, not that any number is falsified. Confirmed NOT
downstream of the origin-H² work (176/192/etc.). Recorded in `PROGRESS.md`'s NEEDS YOU; this
DM does not rule on it, but drafts the requested repair leg below given the claim-adjacency.

```
### 225 — ROUTE-RSR: REPAIR rescaled_spectrum.py's K_fine==K_coarse DEGENERATE-COMPARISON
BUG, WITH EXPLICIT ROUTE-E/ROUTE-G ROW RE-CONFIRMATION (leg 203's finding, THE FIRST
GENUINELY CLAIM-ADJACENT AUDIT-FAMILY ITEM THIS CYCLE) (RESERVE)
**Thesis.** Leg 203 (RSA) found `converged_spectrum`'s `K_fine==K_coarse` comparison
degenerately certifies the entire continuum as converged. Mechanism R2 is claim-adjacent:
5/7 Route-E and 7/7 Route-G banked rows sit above the module's own convergence threshold,
though both routes already banked independent residuals and are already separately flagged
`converged=False` by the module's own conservative check — so no banked number is currently
wrong, only discoverably less precise than a bare convergence label would suggest. Same
discipline as leg 221 (BVRR) applied to leg 205's finding: repair the mechanism AND
explicitly re-confirm the claim-adjacent rows in the same pass, rather than trusting a
"probably fine because of a separate flag" argument without re-running it.
**Gate.** Does fixing the `K_fine==K_coarse` degenerate comparison (per leg 203's own
identified mechanism) cause every one of leg 203's adversarial cases to now correctly reject
false convergence, AND does an explicit, fresh re-run of the 5/7 Route-E and 7/7 Route-G
banked rows confirm (a) their own independently-banked residuals are unchanged, and (b) their
`converged=False` flag from the module's separate conservative check still holds post-repair
(i.e., the repair doesn't silently relabel them `converged=True` for the wrong reason either)?
  yes -> Bank the repair AND the explicit Route-E/Route-G re-confirmation together — this
         closes leg 203's finding on stronger footing than it landed with, the same upgrade
         leg 221 gives leg 205's finding. Flag for a postrepair-verification leg once a slot
         is available.
  no  -> If the re-confirmation itself turns up a moved residual or an unexpected flag flip
         on any Route-E/Route-G row, this is a priority finding of a different order than
         anything else in this cycle's audit-family backlog — escalate immediately, do not
         fold it quietly into the repair's own landing.
**Territory.** solver/rescaled_spectrum.py (the K_fine==K_coarse comparison only, plus the
               other 7 named mechanisms if leg 203's own report scopes them as part of the
               same repair — read leg 203's report first to confirm scope before coding),
               experiments/p2_route_rsr_v1_repair.py,
               writeup/data/p2_route_rsr_v1_repair.json,
               writeup/novelty/leg_225.md, experiments/journal/leg_225.md.
               Reads (never edits) Route-E's and Route-G's own banked rows/JSONs for the
               re-confirmation.
**Difficulty.** standard
**Independence.** Owns rescaled_spectrum.py directly (leg 203's own read-only territory,
closed on landing). Read-only overlap with Route-E/Route-G's own banked data is read-read,
not a collision. Confirmed NOT downstream of the origin-H² work (176/192), per leg 203's own
finding. Reserve — promote with elevated priority given the claim-adjacency (rank alongside
218/221, ahead of the purely-latent repairs 216/217/219/220/222).
```

**Slot D refilled with leg 221 (BVRR)** — repairing leg 205's finding with the explicit
zero-contamination re-confirmation, in flight now.

**Live-slot roster, corrected:**

| Slot | Leg | Route | Status |
|---|---|---|---|
| A | 192 | H2CV | live (unchanged) |
| B | 211 | XU11 | live (unchanged) |
| C | 213 | LGC2 | live (unchanged) |
| D | 221 | BVRR | **live, newly promoted — replaces 203 (escalated, OFF roster)** |
| E | 212 | USC2V | live (unchanged) |
| F | 209 | SCA2 | live (unchanged) |
| G | 202 | PNA | live (unchanged) |
| H | 218 | BHR | live (unchanged) |
| I | 210 | M2SV | live (unchanged) |
| J | 207 | DPA | live (unchanged) |

**Reserve queue: 8 undispatched legs (216, 217, 219, 220, 222, 223, 224, 225).** 221 now live
(off reserve); 225 newly drafted (claim-adjacent, elevated priority). Above the §3a
watermark of 3 — no further batch needed. Promotion order, revised for 225's elevated
priority: **225 (RSR) and 218 (already promoted this cycle)** rank jointly at the top of
what remains — 225 by being the only claim-adjacent item in the whole backlog; then 216
(CGF), 217 (PCR), 219 (ICR2), 220 (TNR); then 222 (FBA), 223 (PUB3), 224 (GCC) last as before.

Nothing in this update lifts a ban. Escalation #4 (129/188), CGA (199), BHA (198), ICA2
(201), TNA2 (204), and now RSA (203) all stay with the user via `PROGRESS.md`'s NEEDS YOU —
this DM rules on none of them; it drafts repairs for the well-characterized ones so they are
ready to promote regardless of how any user ruling eventually lands (a repair fixing a latent
silent-corruption mechanism is not itself claim-adjacent to any open escalation's ruling).
No claim about Walls 1 and 2 moves; Clay stays ~0.05%. No direction question raised this
cycle.

---

## DM bookkeeping update, cycle 1, same day — 202 escalates, DIFFERENT IN KIND: the first
finding this cycle that plausibly requires re-scoping a banked headline (Route-D v11), not
just a routine latent repair; 213 escalates with a cosmetic finding; C/G refilled

**202 (PNA) escalated, not merged** (`leg/202-pna-v1` pushed, `main` untouched). **Different
in kind from every other audit-family item this cycle** (all of which were latent):
`profile_newton.py`'s `continuation` returns off-branch, grid-scale spurious roots as
`converged=True` at machine-zero residual. **This one materially exposes a banked claim**:
Route-D v11's own `a_max_machine`/`GA_boundary` verdicts trust exactly this flag, and v11's
own JSON already shows the branch-jump signature in its own diagnostics
(`weighted_defect` 0.50/4788/73372 at `a=0.5/0.8/1.0`) — **the rejecting information existed
in the caller's own data and never reached the module's verdict.** At `a=1.50`, `c` reads
`0.20427`/`0.23717`/`0.97282` at three different grids, all reported "converged," **376%
apart**. Route-ASA (leg 122) is confirmed safe (stays on-branch throughout).

**This DM's own assessment, since the orchestrator asked explicitly: yes, this plausibly
needs actual re-scoping of Route-D v11's headline, not just a repair.** The reasoning: a
convergence flag that a caller's own diagnostics already contradict, at three grids differing
by 376% at `a=1.50` alone, is not "a latent defect nothing banked depends on" (this cycle's
other nine items) — it is a specific, named, already-quantified inconsistency IN a banked
headline's own supporting data. That does not mean the headline is WRONG (this DM does not
know yet which of the three `a=1.50` values, if any, is the genuine on-branch one, or whether
`a_max_machine`/`GA_boundary` themselves sit in the affected region) — but "does Route-D v11's
headline survive using the caller's own already-existing rejection signal instead of the
module's blind `converged=True`" is now a decidable, high-priority question this DM cannot
answer from here and should not guess at. **Recorded, matching the orchestrator's own
PROGRESS.md item 1b, as distinct from the routine escalation backlog** — this is the single
highest-priority item in the entire audit-family backlog right now, ranked above even leg 203
(RSA)'s claim-adjacent-but-not-headline-threatening finding.

```
### 226 — ROUTE-PNR: REPAIR profile_newton.py's OFF-BRANCH FALSE-CONVERGENCE BUG, WITH
EXPLICIT ROUTE-D v11 RE-SCOPING (leg 202's finding — ELEVATED TO HIGHEST PRIORITY, THE FIRST
ITEM THIS CYCLE THAT PLAUSIBLY THREATENS A BANKED HEADLINE) (RESERVE)
**Thesis.** Leg 202 (PNA) found `continuation` reports `converged=True` at machine-zero
residual for off-branch, grid-scale spurious roots — and Route-D v11's own
`a_max_machine`/`GA_boundary` verdicts trust exactly this flag, while v11's OWN JSON already
contains the rejecting signal (`weighted_defect` spiking to 4788/73372 at `a=0.8/1.0`) that
never reached the verdict. At `a=1.50`, three grids report `c=0.20427/0.23717/0.97282`, all
"converged," 376% apart. Same discipline as legs 221/225 (fix AND explicitly re-confirm the
affected banked claim in the same pass) — but escalated further here, since the affected
claim is a HEADLINE, not a background row: this leg must not just re-run existing numbers, it
must determine whether `a_max_machine`/`GA_boundary` themselves change once the module's
verdict correctly incorporates the caller's own already-existing `weighted_defect` rejection
signal instead of ignoring it.
**Gate.** Does repairing `continuation` to incorporate the caller's own `weighted_defect`
diagnostic into its convergence verdict (rather than reporting bare machine-zero residual as
sufficient) cause (a) every one of leg 202's off-branch adversarial cases to now correctly
reject, (b) the three `a=1.50` grids to converge to a SINGLE genuine on-branch value once the
spurious roots are excluded (or, if they still disagree, report that honestly rather than
picking one), and (c) an explicit, fresh re-derivation of Route-D v11's own
`a_max_machine`/`GA_boundary` headline verdicts using the repaired module?
  (c) unchanged -> Route-D v11's headline is confirmed to survive the repair. Report the
         before/after values precisely (not just "unchanged," show the numbers) and bank the
         repair. This closes leg 202's finding without touching the headline.
  (c) changed -> **Route-D v11's headline itself needs correcting.** Do NOT correct the
         headline's own prose under this leg's authority — report the exact before/after
         values and the mechanism precisely, and ESCALATE immediately as a priority finding
         requiring the user's and orchestrator's attention, distinct from and above every
         other item in this cycle's audit-family backlog.
  (a)/(b) fail -> Report exactly which adversarial case still slips through or which grid
         still disagrees after the fix; do not declare the repair complete on a partial fix
         given what is at stake here.
**Territory.** solver/profile_newton.py (the convergence-verdict logic, incorporating the
               existing `weighted_defect` caller diagnostic), experiments/p2_route_pnr_v1_repair.py,
               writeup/data/p2_route_pnr_v1_repair.json,
               writeup/novelty/leg_226.md, experiments/journal/leg_226.md.
               Reads (never blindly trusts) Route-D v11's own banked JSON/report and Route-ASA
               (leg 122)'s own banked report (already confirmed safe, re-check only, do not
               presuppose).
**Difficulty.** heavy (the re-scoping question, not the mechanical fix, is the hard part)
**Independence.** Owns profile_newton.py directly (leg 202's own read-only territory, closed
on landing). Read-only overlap with Route-D v11's and Route-ASA's own banked data is
read-read, not a collision, but this leg's own gate may require ESCALATING a headline
correction, which stays outside this leg's own authority to make. Reserve — promote
IMMEDIATELY, ranked above every other item in the backlog including 218/221/225.
```

**213 (LGC2) escalated with a minor, cosmetic finding, not urgent.** The
`EGM_PRIMARY_READ` ledger's own `sign_correction_leg_190` field still describes 5 prose sites
as wrong — but leg 214 already fixed them (`2c901c4`), so the field is now backwards (stale
tense, not a stale fact). **0 banked numbers move.** Drafted below as a tiny reserve leg.

```
### 227 — ROUTE-EGMT: FLIP THE STALE-TENSE ledger FIELD, EGM_PRIMARY_READ's
sign_correction_leg_190 (leg 213's cosmetic finding) (RESERVE)
**Thesis.** Leg 213 (LGC2) found `EGM_PRIMARY_READ`'s own `sign_correction_leg_190` field
still describes leg 214's 5 prose fixes as outstanding, even though leg 214 already landed
them (`2c901c4`). A one-field tense update, mechanical, no other content touched.
**Gate.** Does `EGM_PRIMARY_READ`'s `sign_correction_leg_190` field now correctly state the 5
sites as fixed (past tense, citing `2c901c4`), with every other field in the same ledger
entry byte-for-byte unchanged?
  yes -> Bank the fix; confirm via diff that nothing else moved.
  no  -> Report exactly what resisted the one-field edit.
**Territory.** solver/literature_gates.py (the ONE field, `sign_correction_leg_190`, in the
               `EGM_PRIMARY_READ` entry only), writeup/novelty/leg_227.md,
               experiments/journal/leg_227.md.
**Difficulty.** light
**Independence.** One-field mechanical fix, no other ledger row or module touched. Disjoint
from every other live/reserve leg. Reserve — lowest urgency in the whole backlog (0 banked
numbers move per leg 213's own report), promote whenever a light slot is convenient.
```

**Slots C and G refilled** with **220 (TNR)** — repairing leg 204's `target_norm.py` finding
— and **222 (FBA)** — closing the audit family's own module-coverage inventory
(`fractional_boussinesq.py`) — both per the orchestrator's report.

**Live-slot roster, corrected to match the orchestrator's latest report.** Note: slot B now
shows **217 (PCR)** live, replacing 211 (XU11) — this DM has no independent record of 211's
landing/escalation status this round (not mentioned in any message reaching this DM); per
this file's own standing practice, the orchestrator's live-roster report is treated as
authoritative over this DM's own derived tracking, so it is recorded as given without
fabricating a reason.

| Slot | Leg | Route | Status |
|---|---|---|---|
| A | 192 | H2CV | live (unchanged) |
| B | 217 | PCR | live (per orchestrator's report; 211's fate not detailed to this DM) |
| C | 220 | TNR | **live, newly promoted — replaces 213 (escalated, OFF roster)** |
| D | 221 | BVRR | live (unchanged) |
| E | 212 | USC2V | live (unchanged) |
| F | 209 | SCA2 | live (unchanged) |
| G | 222 | FBA | **live, newly promoted — replaces 202 (escalated, OFF roster)** |
| H | 218 | BHR | live (unchanged) |
| I | 210 | M2SV | live (unchanged) |
| J | 207 | DPA | live (unchanged) |

**Reserve queue: 7 undispatched legs (216, 219, 223, 224, 225, 226, 227).** 220/222 now live
(off reserve); 226 and 227 newly drafted. Above the §3a watermark of 3 — no further batch
needed. **Promotion order, re-ranked for 226's priority: 226 (PNR) FIRST, unconditionally**
— the only item this cycle that plausibly threatens a banked headline outranks everything,
including the already-in-flight 218/221/225. Then **225 (RSR)** (the one other
claim-adjacent item), then 216 (CGF), 219 (ICR2), then 223 (PUB3), 224 (GCC), 227 (EGMT) last
(lowest urgency, purely cosmetic).

Nothing in this update lifts a ban or moves any claim about Walls 1 and 2; Clay stays
~0.05%. Escalation #4 (129/188), CGA (199), BHA (198), ICA2 (201), TNA2 (204), RSA (203), and
now **PNA (202) — flagged as this cycle's highest-priority item and matching the
orchestrator's own PROGRESS.md item 1b** — all stay with the user via `PROGRESS.md`'s NEEDS
YOU; this DM rules on none of them, but has stated its own assessment on 202 explicitly per
the orchestrator's direct question: **yes, Route-D v11's headline plausibly needs re-scoping,
pending leg 226's own re-derivation using the repaired module.** No direction question raised
by this DM itself this cycle.

---

## DM bookkeeping update, cycle 1, same day — 223 landed, a reconciliation pass (real drift
found on this DM's side too), 224/226 promoted, watermark hit again, 8 new postrepair-
verification legs drafted

**223 (PUB3) landed on `main` (`6cb9bca`) — gate YES.** The audit-family synthesis note
corrected its own stale dispatch-time escalation count (7, drafted when the leg was written)
to the actual count at landing time: **13**. It also found `reports/STATUS.md` (the
orchestrator's own committed snapshot) stale by ten escalations — the orchestrator has since
fully refreshed it. A genuinely useful catch from exactly the kind of self-auditing
discipline this leg was drafted to apply.

**Reconciliation, prompted by the orchestrator's own "worth double-checking your tracking"
note, and warranted: this DM's reserve/live bookkeeping had drifted too, in the same
direction as the orchestrator's 3-slot drift.** Cross-checking the orchestrator's latest
roster against this DM's own running reserve list found two items this DM had continued
carrying as "reserve, undispatched" that were, in fact, already dispatched rounds ago without
the promotion reaching this DM in an update: **219 (ICR2)** (now confirmed live in slot F,
per the orchestrator's own report of an accidental duplicate dispatch — the leg was already
running from an earlier round this DM has no record of) and **223 (PUB3) itself** (just
confirmed landed, meaning it was dispatched, ran, and completed without ever appearing in
this DM's "live roster" bookkeeping in between). **Leg 207 (DPA) is also now known to have
landed "several rounds ago"** per the orchestrator's own account of the vacant-slot-J bug —
this DM has no gate detail for 207 beyond that it landed and freed the slot; recorded here as
landed, unqualified, pending any later correction if the orchestrator's own records show
otherwise. Going forward, this DM will treat the orchestrator's periodically-restated full
live-slot roster as the single source of truth for occupancy, and will not carry a leg as
"reserve" once it stops appearing in that roster as either live or explicitly reported
escalated/landed — the drift here came from continuing to track old promotion-order lists
past the point where the ground truth had already moved on.

**224 (GCC) and 226 (PNR) promoted, filling slots E and J.** 226 (the top-priority repair for
leg 202's Route-D v11 exposure) is now in flight — the fastest possible turnaround for this
cycle's single highest-priority item, closing the slot-J gap the orchestrator found in the
same stroke.

**Live-slot roster, corrected and reconciled:**

| Slot | Leg | Route | Status |
|---|---|---|---|
| A | 192 | H2CV | live (unchanged) |
| B | 217 | PCR | live (unchanged) |
| C | 220 | TNR | live (unchanged) |
| D | 221 | BVRR | live (unchanged) |
| E | 224 | GCC | **live, newly promoted** |
| F | 219 | ICR2 | live (duplicate dispatch, per orchestrator — only one push will land; recorded as one occupant of slot F, not two) |
| G | 222 | FBA | live (unchanged) |
| H | 218 | BHR | live (unchanged) |
| I | 210 | M2SV | live (unchanged) |
| J | 226 | PNR | **live, newly promoted — top priority, closes the slot-J gap** |

**True reserve, after the reconciliation above: 3 items (216, 225, 227) — 219 and 223 are
removed from the reserve count entirely (already dispatched/landed, not reserve stock this
DM was correctly still holding).** This lands exactly AT the §3a watermark. Per standing
instruction, eight new fully-specified candidates are drafted now, without waiting to be
asked. All eight are postrepair-verification legs (the same 86/87/94/103/104/105/131-135/
147/166-170/192-195 pattern) for this cycle's own repair batch, each blocked until its
source repair lands — plus one genuinely new scoping question grounded directly in leg
202/226's own finding.

```
### 228 — ROUTE-BHRV: POST-REPAIR VERIFICATION, LEG 218's bordered_hl.py REPAIR (RESERVE —
NOT dispatchable until leg 218 lands)
**Thesis.** Leg 218 (BHR) repairs this cycle's single highest-blast-radius latent defect
(negative border weight corrupting Z_1 by up to 1.198e9x, Z_2 by up to 1.189e17x). Given the
magnitude, this repair deserves the same independent postrepair verification this repository
applies to every other repair, not a self-report alone.
**Gate.** Does an independent re-run of leg 218's own adversarial battery confirm every
negative-weight case now rejects, with every one of 54/58/127/192's own live values
bit-identical pre/post repair?
  yes -> Bank as the permanent verification record for this cycle's highest-stakes repair.
  no  -> Report the exact discrepancy; escalate immediately given the magnitude leg 198
         originally measured.
**Territory.** test_bordered_hl_postrepair.py, experiments/p2_route_bhrv_v1_postrepair.py,
               writeup/data/p2_route_bhrv_v1_postrepair.json,
               writeup/novelty/leg_228.md, experiments/journal/leg_228.md.
**Difficulty.** standard
**Independence.** Reads solver/bordered_hl.py; edits nothing under either outcome. **NOT
dispatchable until leg 218 lands.**
```

```
### 229 — ROUTE-PNRV: POST-REPAIR VERIFICATION, LEG 226's profile_newton.py REPAIR AND ITS
ROUTE-D v11 RE-SCOPING (RESERVE — NOT dispatchable until leg 226 lands; HIGHEST PRIORITY OF
THE EIGHT)
**Thesis.** Leg 226 is this cycle's single highest-priority item — it may determine whether
Route-D v11's own banked headline needs correcting. Whichever way its gate lands, an
independent re-derivation is essential before anyone treats either outcome (headline
survives / headline changes) as settled — this is not an optional postrepair check, it is
the same discipline every genuinely novel claim in this repository gets, applied at maximum
stakes.
**Gate.** Does an independent re-run of leg 226's repaired `profile_newton.py`, applied fresh
to Route-D v11's own inputs, reproduce leg 226's own reported before/after
`a_max_machine`/`GA_boundary` values (whether unchanged or changed) and its own resolution of
the three-grid `a=1.50` disagreement?
  yes -> Independently confirmed either way. If leg 226 found the headline changed, this
         verification is what makes that correction safe to actually apply — do not apply
         any headline correction under this leg's own authority, escalate for the
         user/orchestrator to action.
  no  -> Report the exact discrepancy immediately as the highest-priority finding in the
         entire backlog — a mismatch here would mean even the REPAIR's own re-derivation is
         unreliable.
**Territory.** test_profile_newton_postrepair.py, experiments/p2_route_pnrv_v1_postrepair.py,
               writeup/data/p2_route_pnrv_v1_postrepair.json,
               writeup/novelty/leg_229.md, experiments/journal/leg_229.md.
               Reads (never edits) Route-D v11's own banked report/JSON.
**Difficulty.** heavy
**Independence.** Reads solver/profile_newton.py; edits nothing under either outcome. **NOT
dispatchable until leg 226 lands; promote THIS one immediately the moment it does, ahead of
227/228/230-235.**
```

```
### 230 — ROUTE-TNRV: POST-REPAIR VERIFICATION, LEG 220's target_norm.py REPAIR (RESERVE —
NOT dispatchable until leg 220 lands)
**Thesis/Gate/pattern identical to 228, applied to leg 220's repair** — does an independent
re-run confirm the asymmetric-grid extrapolation case is now correctly flagged
(`n_outside_grid>0`/`domain_valid=False`), with leg 55's own banked margins bit-identical?
**Territory.** test_target_norm_postrepair.py, experiments/p2_route_tnrv_v1_postrepair.py,
               writeup/data/p2_route_tnrv_v1_postrepair.json,
               writeup/novelty/leg_230.md, experiments/journal/leg_230.md.
**Difficulty.** standard
**Independence.** Reads solver/target_norm.py; edits nothing. **NOT dispatchable until leg
220 lands.**
```

```
### 231 — ROUTE-PCRV: POST-REPAIR VERIFICATION, LEG 217's port_certification.py REPAIR
(RESERVE — NOT dispatchable until leg 217 lands)
**Thesis/Gate/pattern identical to 228** — does an independent re-run confirm all four of
leg 200's named mechanisms now reject/raise correctly, with leg 195's own 114/114 clean PORT
reproduction bit-identical?
**Territory.** test_port_certification_postrepair.py, experiments/p2_route_pcrv_v1_postrepair.py,
               writeup/data/p2_route_pcrv_v1_postrepair.json,
               writeup/novelty/leg_231.md, experiments/journal/leg_231.md.
**Difficulty.** standard
**Independence.** Reads solver/port_certification.py; edits nothing. **NOT dispatchable until
leg 217 lands.**
```

```
### 232 — ROUTE-ICRV: POST-REPAIR VERIFICATION, LEG 219's interval_certificate.py REPAIR
(RESERVE — NOT dispatchable until leg 219 lands)
**Thesis/Gate/pattern identical to 228** — does an independent re-run confirm the subnormal-
band enclosure escape is closed, with every live operator (140-298 decades clear, per leg
69's own scoping) bit-identical?
**Territory.** test_interval_certificate_postrepair2.py,
               experiments/p2_route_icrv_v1_postrepair.py,
               writeup/data/p2_route_icrv_v1_postrepair.json,
               writeup/novelty/leg_232.md, experiments/journal/leg_232.md.
**Difficulty.** standard
**Independence.** Reads solver/interval_certificate.py; edits nothing. **NOT dispatchable
until leg 219 lands** (now confirmed live in slot F per this update's reconciliation).
```

```
### 233 — ROUTE-BVRRV: POST-REPAIR VERIFICATION, LEG 221's boussinesq_rescaled.py REPAIR AND
ITS OWN ZERO-CONTAMINATION RE-CONFIRMATION (RESERVE — NOT dispatchable until leg 221 lands)
**Thesis.** Leg 221 both repairs leg 205's two mechanisms AND performs the zero-contamination
re-confirmation leg 205 itself skipped. Both halves deserve independent re-verification,
given leg 205 was flagged as this cycle's least-certain escalation.
**Gate.** Does an independent re-run confirm (a) both named mechanisms now reject correctly,
and (b) the zero-contamination re-confirmation itself reproduces (no banked
`boussinesq_rescaled.py`-dependent value actually moved)?
  yes -> Bank as closing leg 205's finding on fully independently-confirmed footing.
  no  -> Escalate immediately — this would upgrade leg 205 from "uncertain" to "confirmed
         contaminated," the most serious possible outcome in this cycle's backlog.
**Territory.** test_boussinesq_rescaled_postrepair.py,
               experiments/p2_route_bvrrv_v1_postrepair.py,
               writeup/data/p2_route_bvrrv_v1_postrepair.json,
               writeup/novelty/leg_233.md, experiments/journal/leg_233.md.
**Difficulty.** standard
**Independence.** Reads solver/boussinesq_rescaled.py; edits nothing. **NOT dispatchable
until leg 221 lands.**
```

```
### 234 — ROUTE-RSRV: POST-REPAIR VERIFICATION, LEG 225's rescaled_spectrum.py REPAIR (leg
203's finding) (RESERVE — NOT dispatchable until leg 225 lands)
**Thesis/Gate/pattern identical to 228, at the claim-adjacent stakes leg 225 itself
carries** — does an independent re-run confirm the `K_fine==K_coarse` fix rejects false
convergence, AND that Route-E's/Route-G's own banked rows genuinely keep their independent
residuals and `converged=False` flags unchanged?
**Territory.** test_rescaled_spectrum_postrepair.py,
               experiments/p2_route_rsrv_v1_postrepair.py,
               writeup/data/p2_route_rsrv_v1_postrepair.json,
               writeup/novelty/leg_234.md, experiments/journal/leg_234.md.
**Difficulty.** standard
**Independence.** Reads solver/rescaled_spectrum.py; edits nothing. **NOT dispatchable until
leg 225 lands.**
```

```
### 235 — ROUTE-CDAP: DOES THE "CALLER'S OWN DIAGNOSTIC ALREADY CONTRADICTS THE VERDICT"
PATTERN (LEG 202/226'S FINDING) RECUR IN ANY OTHER BANKED HEADLINE VERDICT? (RESERVE)
**Thesis.** Leg 202's finding is a genuinely new DEFECT SHAPE for this repository's audit
family: not "a guard fails to validate adversarial input" (every other item this cycle), but
"a caller's own already-computed diagnostic contradicts a verdict the caller then trusts
anyway." This is worth checking for recurrence directly, before assuming it is a one-off:
does any OTHER banked headline verdict (the same class as Route-D v11's
`a_max_machine`/`GA_boundary`) have its own caller-side diagnostic that a fresh read would
show already contradicts the trusted verdict, the same way leg 202 found for
`weighted_defect`?
**Gate.** Does a systematic check of every other banked headline verdict's own caller-side
diagnostics find a SECOND instance of "the rejecting signal already existed in the caller's
own data and was never used"?
  yes -> Name the headline, the diagnostic, and the magnitude precisely. This would be the
         second instance of a materially new defect shape — escalate immediately at the same
         priority as leg 202/226, do not repair under this leg's own authority.
  no  -> Bank the census as confirming leg 202's finding is (so far) a singular instance, not
         a recurring pattern — still worth having checked rather than assumed.
**Territory.** experiments/p2_route_cdap_v1_census.py, writeup/data/p2_route_cdap_v1_census.json,
               writeup/novelty/leg_235.md, experiments/journal/leg_235.md.
               Reads every banked headline's own report/JSON read-only; patches nothing.
**Difficulty.** standard
**Independence.** Read-only census, no solver module edited. Disjoint from every other
live/reserve leg, including 224 (GCC, a function-signature census for a DIFFERENT defect
shape — the guard-class family, not the ignored-diagnostic shape). Reserve — promote with
elevated priority given what leg 202 already found once; not blocked on anything.
```

**Reserve queue: 11 undispatched legs (216, 225, 227, 228, 229, 230, 231, 232, 233, 234,
235).** Above the §3a watermark of 3 again. **Promotion order: 235 (CDAP) first among the
immediately-dispatchable** (elevated priority, directly follows from leg 202's finding, no
block); then 216 (CGF), 225 (RSR — already ranked high from the prior update), 227 (EGMT,
lowest urgency); 228-234 stay correctly blocked until their respective source repairs land,
with **229 (PNRV) to be promoted the INSTANT leg 226 lands, ahead of every other blocked
item**, given the stakes.

Nothing in this update lifts a ban, resolves any parked escalation, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised by this DM this cycle.

---

## USER-DIRECTED CORRECTION, external review, relayed verbatim by the orchestrator —
composition-floor quota, leg 202/226 re-scoped, items 3-6 actioned

**This DM verified the review's core numbers before acting on them, per its own standing
discipline.** `git log --oneline -60 | grep -icE "audit|repair|regression|postrepair|
verification|adversarial"` returns **33/60 (55%)**, closely matching the review's own 34/60
(57%) — the small difference is almost certainly measurement-window drift between when the
review was written and when this DM checked, not a discrepancy worth chasing. `reports/
STATUS.md`'s own committed roster snapshot confirms **0 of 10 live slots currently produce
math, literature, or construction output** — every one of A-J is verify/repair/audit/census
shaped, including the two slots (E=224 GCC, a census; F=219 duplicate) this DM itself
promoted in the immediately preceding update. **This DM's own last several rounds of
drafting are exactly what the review is correctly describing** — every fresh candidate this
DM has drafted since the watermark first triggered has been another audit, repair, or
verification leg, because those are the cheapest kind to draft and the watermark trigger
does not distinguish. The review's mechanical diagnosis (§3a rewards audits by default; the
math-over-review preference from `e90fa98` did not survive the restart in enforceable form)
is accepted as correct and acted on below, not re-litigated.

### Item 2 — the composition floor, written into this file now

**New standing rule, binding on this DM's own queue-drafting from this point forward:**

> **Composition floor.** At least 3 of the 10 live slots must at all times hold a leg whose
> primary output is mathematics, external literature, or construction (NOT audit, repair, or
> verification/postrepair-check, even when the audit/repair/verify leg is itself
> well-motivated). The §3a watermark trigger may not fill a slot with an audit/repair/verify
> leg while the roster is below this floor. If, at the moment the trigger fires, the reserve
> contains no eligible math/literature/construction candidate, the trigger **fails loudly**
> — this DM states that explicitly in its update rather than silently filling the slot with
> whatever is cheapest — and drafts an eligible candidate before dispatching anything else.
> A leg's classification for this floor is stated explicitly in its own queue entry from now
> on (a one-line tag: `[FLOOR-ELIGIBLE: math/literature/construction]` or
> `[audit/repair/verify — does not count toward floor]`), so the floor is checkable by
> inspection of this file's own live-slot table, not left to inference.

**This DM cannot edit `ORCHESTRATION.md` or `test_plan_of_record.py` — both are outside its
one-file ownership (§3 of `ORCHESTRATION.md` itself: "You own DIRECTION.md and nothing
else").** Per the review's own instruction that a rule needs to be executable to survive a
restart, this DM flags explicitly, for the orchestrator and the user, that the SAME rule
needs mirroring in `ORCHESTRATION.md` §3 (so a future DM spawn inherits it as inherited law,
not just as something the current DM remembers to keep doing), and ideally as a checkable
assertion the merge gate or `test_plan_of_record.py` can run directly against this file's own
live-slot table (e.g., parse the ten-row table's `[FLOOR-ELIGIBLE]` tags and assert
`count >= 3`). This DM drafts the rule's content and applies it to its own file; making it
durable across restarts is the orchestrator's/user's action item, not something this DM can
complete unilaterally.

**Floor status right now, and the preemption this DM is choosing (per the orchestrator's own
question — preempt now, do not wait for natural vacancies):** 0/10 eligible. Waiting for
natural vacancies would mean at minimum 3 more full audit/repair/verify cycles before the
floor is met, during which every fresh watermark-triggered draft would (under the old,
now-superseded practice) keep making it worse. **This DM preempts three slots now**, chosen
to minimize disruption to work already in flight: **F (219, ICR2)** — the orchestrator's own
report named this an accidental duplicate dispatch with a second copy already running
elsewhere; redirecting this occupancy costs zero real progress. **G (222, FBA)** — an
audit-family module-coverage completion, useful but the least time-sensitive of anything
live right now (no claim-adjacency, no blast-radius stakes). **E (224, GCC)** — the
systematic guard-class census, drafted by this DM itself last round at explicitly *lower*
priority than the repair batch ("not ranked ahead of 216-221's own higher-value-per-slot
repairs") — the least-invested slot to redirect. **A/B/C/D/H/I/J are left untouched** —
192(verify, mid-background-compute, wasteful to interrupt), 217/220/221(repairs already
scoped and likely in progress), 218(the highest-blast-radius repair this cycle found),
210(verify, mid-background-compute), and 226(this cycle's single highest-priority item,
addressed directly below rather than preempted).

### Item 3 — leg 202/profile_newton.py, in the order specified

**(a) Leg 226's own gate is corrected in place, per the review's explicit historical
caution.** Four consecutive repair legs in this repository's own history (150, 151, 152,
154) found that the escalating leg's OWN prescribed fix did not survive measurement as
specified — the fix needed adjustment once actually attempted. Leg 226 (drafted by this DM
last round) is now corrected: **leg 202's own prescription — "incorporate the caller's
`weighted_defect` diagnostic into the convergence verdict" — is a HYPOTHESIS about the right
fix, not a specification leg 226 must implement verbatim.** Leg 226's gate (§226 above) is
amended with this clause, binding on whichever branch/session carries it forward: *if the
prescribed fix (incorporating `weighted_defect`) does not itself survive measurement — e.g.
it produces its own false rejections, or fails to resolve the `a=1.50` three-grid
disagreement — leg 226 must report that precisely and is authorized to identify a DIFFERENT
mechanism that does close the gap, rather than declaring the leg failed because the
originally-prescribed fix under-performed.* This does not relax leg 226's own escalation
requirement if Route-D v11's headline changes — that stays mandatory under either fix.

**(b) A new leg, separate from the repair, answering exactly which banked Route-D v11
numbers depend on `profile_newton.py` and whether any move — drafted below as leg 236.**
Per the review's own instruction: *until this leg answers, no document may cite Route-D
v11's numbers as settled.* This DM states that instruction here, explicitly, as binding on
every leg and every writeup touching Route-D v11 from this point forward, not just as a
recommendation.

**(c) The class-level census — drafted below as leg 237, per the review's own framing that
this is "the highest value-per-token leg available right now."** Leg 202's own mechanism
(M2 fails because `relres` is exactly scale-invariant, so no returned field can see the
escape) is a CLASS of defect, not an instance — any module using a scale-invariant residual
as its convergence test can be silently blind the same way. **This leg does NOT count toward
the composition floor** (it is audit/census-shaped, same discipline as 224/GCC), but is
drafted and ranked at elevated priority regardless, per the review's own explicit
value judgment.

```
### 236 — ROUTE-RDDEP: WHICH BANKED Route-D v11 NUMBERS DEPEND ON profile_newton.py, AND DO
ANY MOVE? (leg 202's finding, item 3(b) — SEPARATE FROM THE REPAIR, leg 226)
[FLOOR-ELIGIBLE: math — a quantitative dependency/impeachment determination on a banked
headline, not an audit or repair]
**Thesis.** Leg 202 found `profile_newton.py`'s `continuation` reports false convergence
that Route-D v11's own `a_max_machine`/`GA_boundary` verdicts trust, with the caller's own
`weighted_defect` diagnostic already contradicting it. Leg 226 repairs the mechanism and
re-derives the headline as PART of its own gate — but per the review's explicit instruction,
this question deserves its own leg, not to be answered only as a side effect of a repair
whose own primary gate is "does the mechanism close." This leg traces, precisely and
independently of leg 226's own repair attempt, every banked Route-D v11 number that calls
`profile_newton.py`'s `continuation` (directly or transitively), and determines for EACH one
whether it sits in the affected region (the same `weighted_defect`-spike signature leg 202
already characterized at `a=0.5/0.8/1.0`) or is confirmed clear.
**Gate.** For every banked Route-D v11 number that depends on `profile_newton.py`'s
`continuation`, does it sit in the affected region (per leg 202's own `weighted_defect`
signature), and — for those that do — does the value itself move once the false-convergence
cases are excluded (using leg 226's repaired module if it has landed by the time this leg
runs, or leg 202's own diagnostic data directly if not)?
  none affected -> Route-D v11's headline is confirmed to depend on `profile_newton.py` only
         in regions leg 202 already confirmed safe (e.g. Route-ASA/leg 122's own on-branch
         values). Bank this precisely, with every dependent number's status listed, not just
         a summary verdict.
  some affected, none move -> Report which specific numbers sit in the affected region and
         confirm precisely (not merely assert) that their own values are unchanged once
         false convergence is excluded. Bank as a stronger, independently-checked form of
         "headline survives."
  some affected AND move -> **Route-D v11's headline needs correcting.** Name the exact
         numbers, their before/after values, and escalate immediately — this is the first
         confirmed instance in this entire campaign of a banked headline actually moving,
         and no document may cite the old values as settled from the moment this branch
         fires.
**Territory.** experiments/p2_route_rddep_v1_dependency.py,
               writeup/data/p2_route_rddep_v1_dependency.json,
               writeup/novelty/leg_236.md, experiments/journal/leg_236.md.
               Reads (never edits) Route-D v11's own banked report/JSON and leg 202's own
               report; reads leg 226's repaired module if landed, or leg 202's raw diagnostic
               data otherwise.
**Difficulty.** heavy
**Independence.** Read-only dependency trace and value re-check; does not repair
`profile_newton.py` itself (leg 226's territory). Runs USING leg 226's fix if available but
does not require it — can answer the "which numbers are affected" half immediately, the
"do they move" half once a repaired module exists (from 226) or via direct hand-correction
of the diagnosed cases if 226 hasn't landed yet. Immediately dispatchable — does not block
on 226.
```

```
### 237 — ROUTE-SIRC: SCALE-INVARIANT-RESIDUAL CENSUS — WHICH OTHER MODULES USE A
SCALE-INVARIANT CONVERGENCE TEST, THE SAME BLIND SPOT LEG 202 FOUND? (item 3(c), reviewer-
flagged as highest value-per-token available right now)
[audit/census — does not count toward the composition floor]
**Thesis.** Leg 202's mechanism M2 fails specifically because `relres` (relative residual)
is exactly scale-invariant — no returned field can distinguish a genuine converged solution
from an off-branch spurious root at the same scale-invariant residual value. This is a CLASS
of defect: any `solver/` module that uses a scale-invariant quantity (a relative residual, a
normalized error, a ratio-based tolerance) as its SOLE convergence/closure test is
structurally blind to the same failure mode, regardless of whether it has actually been
triggered yet. Cheap, mechanical: grep every convergence/closure check in `solver/` for
scale-invariant quantities (ratios, relative errors, normalized residuals) used ALONE
(without an absolute-scale companion check), and flag each one.
**Gate.** Does any OTHER `solver/` module (besides `profile_newton.py`, already confirmed
affected) use a scale-invariant residual/ratio as its SOLE convergence or closure test,
without an absolute-scale companion check?
  yes -> Name every module and function precisely. State whether each is claim-adjacent (does
         a banked number depend on it) before deciding priority — this is potentially a
         SECOND confirmed-affected module, escalate any claim-adjacent hit immediately,
         same priority as leg 202/226/236.
  no  -> `profile_newton.py` is confirmed to be the sole instance of this specific defect
         class in `solver/`. Bank the census; this narrows (does not eliminate) concern
         about recurrence.
**Territory.** experiments/p2_route_sirc_v1_census.py, writeup/data/p2_route_sirc_v1_census.json,
               writeup/novelty/leg_237.md, experiments/journal/leg_237.md.
               Reads every solver/*.py file read-only; patches nothing under either outcome.
**Difficulty.** standard
**Independence.** Read-only census, no solver module edited. Disjoint from 224 (GCC, the
guard-class family — a DIFFERENT defect shape, false-positive feasibility, not
scale-invariance blindness) and 235 (CDAP, the ignored-caller-diagnostic shape — also
different: 235 asks whether a contradicting diagnostic already exists and is ignored, this
leg asks whether the convergence test ITSELF is structurally blind regardless of any
diagnostic). Immediately dispatchable — ranked at ELEVATED PRIORITY per the reviewer's own
explicit value judgment, promote alongside or immediately after 236.
```

### Item 4 — the publication path, both blockers cleared, one leg to action it

**Both preconditions confirmed already landed, independently, before this leg is drafted:**
leg 183 (Xu §8 vs. Theorem NGX, 5/5 disjointness axes, the decisive one PROVED not measured)
and leg 209 (adversarial audit of `spectral_certificate.py`, NGX's proof confirmed safe, 0
contamination). Both are additions to already-clean documents, per the review's own framing
— not corrections.

```
### 238 — ROUTE-PUB4: FOLD LEG 176 INTO PUB2, AND APPLY LEG 183's FLAGGED Xu §8 CITATION TO
PUB1 (item 4 — both publication blockers cleared, this is the additive follow-through)
[FLOOR-ELIGIBLE: literature/construction-synthesis — a writeup action item directly
extending landed literature/construction findings, not an audit/repair/verify]
**Thesis.** Two small, independent, purely-additive edits to already-landed publication-
scoping documents. (i) Leg 186 (PUB2, the space-axis synthesis note) explicitly did NOT
include leg 176 (the origin-H² construction at `a=0`) because 176 had not landed when 186
was drafted — 176 has since landed (`bb0f184`, gate YES with one flagged NO magnitude).
**Correction, surfaced by leg 238's own landing: leg 176 is NOT yet independently verified —
leg 192's only commit anywhere is its novelty pass; the construction/measurement work sits
uncommitted in leg 192's own worktree, mid-background-compute, not lost but not landed.**
Leg 238 correctly stated leg 176's numbers in PUB2 as one leg's own float64 measurement, not
an independently-confirmed one — this parenthetical is fixed here to match, so this file
itself doesn't repeat the premature claim leg 238 itself avoided. Fold leg 176 into PUB2 as
the fourth data point PUB2's own text
already anticipated ("with leg 176's construction outcome, if landed by the time this leg
runs, folded in as a fourth data point"). (ii) Leg 183 flagged, as a non-blocking
recommendation, that PUB1 (leg 179's bundle) §3's scope line would be stronger citing Xu §8
as the nearest published relative to Theorem NGX — recorded but never actioned. Apply it now.
**Gate.** Does PUB2 now include leg 176's construction outcome (both its YES headline and its
flagged NO magnitude, neither softened nor strengthened) as its fourth data point, and does
PUB1 §3's scope line now cite Xu §8 as the nearest published relative, per leg 183's own
exact recommendation?
  yes -> Bank both additions; PUB1 and PUB2 are now current with every landed finding that
         bears on them. Flag to the user that both documents are ready for review with these
         additions folded in — this leg's own landing does not itself constitute approval
         (item 6 below: PUB1/PUB2 approval stays parked for the user).
  no  -> Report exactly which addition didn't land cleanly (a mismatch between leg 176's own
         report and what PUB2 says, or a citation that doesn't match leg 183's exact
         recommendation); escalate rather than force it.
**Territory.** writeup/4_p2_lottery/TECHNICAL_P2_PUB2_V1.md (leg 176's data point only),
               writeup/4_p2_lottery/BLOG_P2_PUB2_V1.md (same),
               writeup/4_p2_lottery/TECHNICAL_P2_PUB1_V1.md (§3 scope line only),
               writeup/novelty/leg_238.md, experiments/journal/leg_238.md.
               Reads (never edits) legs 176/183/186/192's own banked reports/JSONs.
**Difficulty.** light
**Independence.** Two narrowly-scoped additive edits to existing writeup files, no solver
module. Disjoint from every other live/reserve leg. Immediately dispatchable — both
preconditions (183, 209) are already landed.
```

### Item 5 — standing instruction, gate contract amended (binding on every future leg this
DM drafts)

**New clause, added to this file's own standing discipline for every negative-result gate
from this point forward:**

> Any leg reporting a negative result ("measured dead," "no viable X," "the coincidence
> persists," etc.) must name, IN THE GATE'S OWN WORDING, the exact realization, trial space,
> or basis the negative holds in. "Measured dead" without a named realization is not an
> admissible gate answer. This is not a retroactive correction of any already-landed leg's
> mathematics — it applies to how FUTURE gates are worded, so a negative doesn't silently
> generalize past the realization it was actually measured in (the exact shape of over-read
> this review names in legs 165, 111/141's zero-width window as a trial-space property not
> generalized; leg 180, the `a*` boundary stated without its measured domain across 15
> documents; and leg 185, leg 125's Object-B stall over-read as non-existence before being
> correctly diagnosed as a solver artifact).

This DM applies this clause to every new leg drafted in this same update (236-238 above) —
none of them are negative-result-shaped gates, so none required the naming clause, but it is
now binding on every FUTURE draft. Like item 2, this needs mirroring in
`ORCHESTRATION.md`/`CONTINUATION_PROMPT.md`'s own inherited-law list to survive a restart;
flagged for the orchestrator, not actioned by this DM outside its own file.

### Item 6 — confirmed: not re-litigated

Stage B's NO / escalation #1 ("committed sequence is EXHAUSTED"), the project exit criterion,
and PUB1/PUB2 approval all stay exactly as parked, per the review's own explicit instruction.
No leg drafted in this update presupposes an answer to any of the three. Item 4's leg (238)
explicitly states its own landing does not constitute PUB1/PUB2 approval.

**Live-slot roster, corrected for the three preemptions.** (Note on slot E, worked out while
drafting: this DM initially considered a third floor-eligible candidate for E, but only two
genuinely new floor-eligible legs — 236, 238 — were ready to draft this round without either
presupposing a parked escalation or repeating already-closed ground. Rather than manufacture
a weak third candidate to force the number, slot E instead carries **237 (SIRC)** — the
reviewer's own explicit "highest value-per-token" item, audit-shaped and NOT floor-eligible —
and the resulting shortfall (2/10, not 3/10) is flagged honestly below rather than papered
over.)

| Slot | Leg | Route | Floor status |
|---|---|---|---|
| A | 192 | H2CV | verify — not floor-eligible |
| B | 217 | PCR | repair — not floor-eligible |
| C | 220 | TNR | repair — not floor-eligible |
| D | 221 | BVRR | repair — not floor-eligible |
| E | 237 | SIRC | **PREEMPTED from 224 (GCC)** — audit/census — not floor-eligible (reviewer's own explicit top-priority item, kept despite not counting) |
| F | 236 | RDDEP | **PREEMPTED from 219 (ICR2 duplicate)** — **FLOOR-ELIGIBLE (math)** |
| G | 238 | PUB4 | **PREEMPTED from 222 (FBA)** — **FLOOR-ELIGIBLE (literature/construction-synthesis)** |
| H | 218 | BHR | repair — not floor-eligible |
| I | 210 | M2SV | verify — not floor-eligible |
| J | 226 | PNR | repair — not floor-eligible (gate corrected, item 3(a)) |

**Floor status: 2/10 floor-eligible (236, 238). Below the required 3 — flagged explicitly,
not silently accepted.** This DM commits to promoting a THIRD floor-eligible candidate into
the next slot that opens naturally (A, H, I, or J, whichever lands first), ahead of any
further audit/repair/verify candidate, per the rule's own text ("the trigger fails loudly...
drafts one before dispatching anything else"). Reserve for the next natural vacancy: a
literature leg extending leg 196's own follow-up finding (arXiv:2511.22819's three newly-
named obstructions, per the pattern legs 175/196 already established) is the most
immediately draftable floor-eligible candidate and will be written up the moment a slot
opens, rather than waiting for another full review cycle to force the issue.

**Reserve queue, recomputed: the true reserve (per the reconciliation two updates above) was
216, 225, 227 (3 items) plus 228-235 (8 blocked/unblocked items) = 11. This update removes
219/222/224 from LIVE status (preempted, not landed or escalated — redirected) and does NOT
return them to reserve (they are superseded by 236/237/238 in the same slots, not vacated).
Adds 236, 237, 238 (now live, not reserve). Net reserve: still 216, 225, 227, 228, 229, 230,
231, 232, 233, 234, 235 = 11 undispatched legs, unchanged by this update's preemptions (which
moved leg occupancy, not reserve stock).**

Nothing in this update lifts a ban. Escalation #1 (B exhausted), the exit criterion, and
PUB1/PUB2 approval all stay parked, per item 6, untouched. Escalation #4, CGA, BHA, ICA2,
TNA2, RSA, and PNA (202, this cycle's highest-priority item, now further scoped by leg 236)
all stay with the user via `PROGRESS.md`'s NEEDS YOU. No claim about Walls 1 and 2 moves;
Clay stays ~0.05%. The composition-floor shortfall (2/10, not yet 3/10) is the one open item
this DM flags for its own next action, not a question for the user.

---

## DM bookkeeping update, cycle 1, same day — preemption confirmed clean, both durable
mirrors confirmed landed, leg 220 lands and opens slot C, the third floor-eligible candidate
drafted and promoted (floor now MET, 3/10)

**Preemption confirmed clean.** All three preempted agents (219-duplicate, 222/FBA,
224/GCC) stopped via `TaskStop` before reaching a landing — no partial/orphaned result to
reconcile. 236 (RDDEP), 237 (SIRC), 238 (PUB4) are now running in slots F, E, G
respectively, exactly as assigned in the prior update.

**Both flagged durable-mirror action items are confirmed done, proactively, by the
orchestrator — before this DM's response even arrived.** `ORCHESTRATION.md` §3b now carries
the composition floor as executable, restart-surviving law. `CONTINUATION_PROMPT.md` carries
lesson 91 (the negative-result naming requirement, item 5). Both of this DM's "outside my
one-file ownership, flagged for you" items are closed. This DM's own copies of the rules in
this file stay as the record of WHY they exist and how this DM applies them to its own
queue-drafting; the orchestrator's copies are now the enforceable ones.

**220 (TNR) landed on `main`, cleanly.** Closes leg 204's `target_norm.py` finding: 6/7
mechanisms re-measured and confirmed closed, a 295,203-leaf regression check clean. This
opens slot C.

**Slot C is exactly the vacancy this DM committed to filling with a third floor-eligible
candidate, per the composition-floor update two sections above. Drafted now, per that
commitment, rather than deferred:**

```
### 239 — ROUTE-USC3: THE THREE NEW OBSTRUCTIONS arXiv:2511.22819 NAMES — MODEL-SPECIFIC OR
TECHNIQUE-SPECIFIC, SAME FRAMING AS LEGS 175/196? (the third composition-floor candidate)
[FLOOR-ELIGIBLE: literature — extends a landed literature finding at full-text depth, not an
audit/repair/verify]
**Thesis.** Leg 196 (USC2) landed STILL SHORT: the authors' follow-up paper
(`arXiv:2511.22819`, ~72 days after `arXiv:2509.14185`) removes the ONE loss-reweighting
obstruction leg 175 identified, closes 0 of leg 175's 4 open items, and **names 3 NEW
obstructions of its own** — but leg 196's own territory was scoped to answering "is there a
certificate," not to characterizing what the three new obstructions actually ARE. This leg
reads `arXiv:2511.22819` at the same full-text depth leg 175 used, and applies the exact same
question leg 175 asked of the ORIGINAL obstruction: for each of the three new obstructions,
is it MODEL-specific (naming an alternative model class that would avoid it) or
TECHNIQUE-specific (a precision/infrastructure gap independent of model, the same shape
leg 173 scoped for Xu's method)? This is not a re-read of ground leg 196 already covered —
leg 196's own report states the three obstructions by name/citation only, per its own
declared territory, and did not characterize each one's shape.
**Gate.** For each of the three obstructions `arXiv:2511.22819` names, is it MODEL-specific
(naming the alternative model class the paper itself points to) or TECHNIQUE-specific (a
precision/infrastructure gap independent of model)?
  any model-specific -> Name the alternative model class precisely, with the paper's own
         reasoning. If that class is one this repository's own infrastructure already
         touches (gCLM/CLM/Boussinesq family), ESCALATE as a candidate new construction lane
         for the user — do not attempt it under this leg's own authority.
  all technique-specific -> Report each precision/infrastructure gap precisely, in the same
         terms leg 173 uses for Xu's method and leg 175 uses for the original obstruction, so
         all three scoping results are directly comparable. Bank it.
  mixed -> Report each of the three separately and precisely; do not average or summarize
         into a single verdict for all three.
**Territory.** experiments/p2_route_usc3_v1_lit.py, writeup/data/p2_route_usc3_v1_lit.json,
               writeup/novelty/leg_239.md, experiments/journal/leg_239.md.
               Reads (never edits) leg 196's own report/JSON and solver/viscous_novelty.py's
               PRECEDENTS ledger, read-only.
**Difficulty.** light
**Independence.** Literature-only, own JSON, no solver module. Disjoint from every other
live/reserve leg (196 already landed and closed; this leg extends it, doesn't re-open it).
Immediately dispatchable.
```

**Slot C filled with 239 (USC3).** The composition floor is now **MET: 3/10 floor-eligible
(236 RDDEP, 238 PUB4, 239 USC3).** No further preemption or forced padding needed this round.

**Live-slot roster, corrected:**

| Slot | Leg | Route | Floor status |
|---|---|---|---|
| A | 192 | H2CV | verify — not floor-eligible |
| B | 217 | PCR | repair — not floor-eligible |
| C | 239 | USC3 | **live, newly promoted — FLOOR-ELIGIBLE (literature)** |
| D | 221 | BVRR | repair — not floor-eligible |
| E | 237 | SIRC | audit/census — not floor-eligible (kept per reviewer's explicit priority) |
| F | 236 | RDDEP | **FLOOR-ELIGIBLE (math)** |
| G | 238 | PUB4 | **FLOOR-ELIGIBLE (literature/construction-synthesis)** |
| H | 218 | BHR | repair — not floor-eligible |
| I | 210 | M2SV | verify — not floor-eligible |
| J | 226 | PNR | repair — not floor-eligible (gate corrected, item 3(a)) |

**Floor status: 3/10 — MET.** Going forward, this DM will keep at least one of 236/238/239's
successors (or a freshly-drafted floor-eligible leg) live at all times, per the rule's own
text, and will state each future draft's floor tag explicitly rather than leave it to
inference.

**Reserve queue: still 11 undispatched legs (216, 225, 227, 228, 229, 230, 231, 232, 233,
234, 235), unchanged by this update** — 239 was drafted fresh for the specific vacancy, not
drawn from this pool.

Nothing in this update lifts a ban, resolves any parked escalation, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised by this DM this cycle.

---

## DM bookkeeping update, cycle 1, same day — 238 landed (with a correction this DM has
fixed in its own record above), slot G vacated, floor back to 2/10, a new floor-eligible leg
drafted to restore it

**238 (PUB4) landed on `main` (`9afe3c2`) — gate YES on both conjuncts.** PUB2 gains leg
176's data point; PUB1 §3 now cites Xu §8 per leg 183's own recommendation. Neither document
is approved by this landing — both stay parked for the user, exactly as leg 238's own gate
required.

**Important correction leg 238 itself surfaced, now fixed in this file's own leg-238 entry
above (not just noted here): leg 176 has NOT actually been independently verified yet.** Leg
192's only commit anywhere is its novelty pass — no runner, no verdict landed. The
construction/measurement work exists uncommitted in leg 192's own worktree
(mid-background-compute, per its last status), so nothing is lost, just not yet landed. PUB2
correctly states leg 176's numbers as one leg's own float64 measurement rather than claiming
independent confirmation — this file's own leg-238 thesis (drafted by this DM) had wrongly
asserted "independently verified (leg 192)" in its background paragraph; that has been
corrected in place two sections above, matching what leg 238 itself actually did. The
orchestrator continues watching leg 192 to completion; no action needed from this DM beyond
the correction just made.

**This vacates slot G. Since 238 was one of the three floor-eligible legs (236, 238, 239),
the floor drops back to 2/10 (236, 239) unless slot G gets a new floor-eligible candidate —
exactly the situation the composition-floor rule anticipates, and exactly why it says the
trigger must "fail loudly" rather than let a non-floor-eligible leg fill the gap quietly.**
Drafted now, per that rule's own text, before anything else fills slot G:

```
### 240 — ROUTE-CNS2: DOES arXiv:2208.09445's OWN AUTHORS HAVE LATER WORK UPGRADING GRADE B
(VISCOUS-DOMINATED) TO GRADE A (VISCOUS TERM ACTUALLY ENCLOSED)? (restores the composition
floor to 3/10, vacated by 238's landing)
[FLOOR-ELIGIBLE: literature — extends a landed literature finding at full-text depth, not an
audit/repair/verify]
**Thesis.** Leg 174 (VBS) located and characterized `arXiv:2208.09445` (3D compressible
Navier-Stokes finite-time blow-up, computer-assistance essential via ~10,000 interval-
arithmetic Taylor coefficient pairs) as Grade B: the viscous term is DOMINATED, not enclosed
— the certified object is the inviscid Euler ODE, not the genuinely viscous PDE. Leg 197
(VNL) banked this characterization into the shared `viscous_novelty.py` ledger. Neither leg
asked the natural follow-on question this repository's own established pattern (legs
175->196, "did the authors' later work remove the obstruction") already applies elsewhere:
does the SAME author group have subsequent work that upgrades Grade B to Grade A for this
specific object — actually enclosing the viscous term rather than dominating it? If so, this
would be the Grade-A/fluid=True cell leg 174's own occupancy matrix found EMPTY (the precise
shape of "the missing rung," per leg 174's own language: empty "for want of a target, not a
method").
**Gate.** Does `arXiv:2208.09445`'s author group have subsequent published work that upgrades
the viscous-term treatment from DOMINATED to ENCLOSED for this same 3D compressible
Navier-Stokes object (or a directly comparable one), achieving a genuine Grade-A/fluid=True
certificate?
  yes -> This would fill the exact empty cell leg 174's occupancy matrix found — the single
         most consequential literature finding this repository could produce for the "missing
         rung" question. Record the citation and its hypotheses verbatim; ESCALATE
         immediately, do not attempt to replicate it under this leg's own authority.
  no (no such later work, or it stops short for a specific stated reason) -> Report the
         search precisely (this repository's own discipline: report the search, not just the
         absence) and, if a stated reason is found, report it in the same terms leg 174/175/
         196 use, so this scoping is directly comparable to theirs. Bank it.
**Territory.** experiments/p2_route_cns2_v1_lit.py, writeup/data/p2_route_cns2_v1_lit.json,
               writeup/novelty/leg_240.md, experiments/journal/leg_240.md.
               Reads (never edits) leg 174's own report/JSON and
               solver/viscous_novelty.py's PRECEDENTS ledger, read-only.
**Difficulty.** light
**Independence.** Literature-only, own JSON, no solver module. Disjoint from every other
live/reserve leg (174/197 already landed and closed; this leg extends them, doesn't re-open
them). Immediately dispatchable.
```

**Slot G filled with 240 (CNS2).** Floor restored to **3/10 (236 RDDEP, 239 USC3, 240
CNS2)** — 238 is off the floor count now that it has landed and left the roster.

**Live-slot roster, corrected:**

| Slot | Leg | Route | Floor status |
|---|---|---|---|
| A | 192 | H2CV | verify — not floor-eligible (still mid-compute) |
| B | 217 | PCR | repair — not floor-eligible |
| C | 239 | USC3 | **FLOOR-ELIGIBLE (literature)** |
| D | 221 | BVRR | repair — not floor-eligible (nearly done per orchestrator) |
| E | 237 | SIRC | audit/census — not floor-eligible (kept per reviewer's priority) |
| F | 236 | RDDEP | **FLOOR-ELIGIBLE (math)** |
| G | 240 | CNS2 | **live, newly promoted — FLOOR-ELIGIBLE (literature)** |
| H | 218 | BHR | repair — not floor-eligible |
| I | 210 | M2SV | verify — not floor-eligible |
| J | 226 | PNR | repair — not floor-eligible (gate corrected, item 3(a)) |

**Floor status: 3/10 — MET, restored same-round as vacated.** This DM notes for its own
future practice: floor-eligible legs (236, 238, 239, now 240) are landing/vacating faster
than the non-floor-eligible repair/verify batch, precisely because they are lighter
(literature-only, no solver module, no adversarial battery) — worth having 1-2 pre-drafted
floor-eligible candidates sitting ready in reserve, not just drafted reactively each time a
slot vacates. Flagged as a process note, not acted on immediately (no pre-drafted spare
exists yet); if another floor slot vacates before this DM's next update, the next
lightest-lift candidate is a literature check of whether either `arXiv:2402.xxxx`-class
Route-E/Route-G-adjacent work (once leg 225 lands and the affected rows are known precisely)
has an independent published cross-check — deferred until 225 lands so it isn't drafted
blind.

**Reserve queue: still 11 undispatched legs (216, 225, 227, 228, 229, 230, 231, 232, 233,
234, 235), unchanged** — 240 was drafted fresh for this specific vacancy, not drawn from
this pool.

Nothing in this update lifts a ban, resolves any parked escalation, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised by this DM this cycle.

---

## DM bookkeeping update, cycle 1, same day — 217 escalates (a strong partial repair, two
out-of-territory artifacts and 3 more silent paths left open), a cleanup leg drafted, 230
promoted into slot B

**217 (PCR) escalated, not merged** (`leg/217-pcr-v1` pushed, `main` untouched; overall gate
NO). Genuinely strong partial result: all four of leg 200's named mechanisms are correctly
repaired, verified with a control leg 200's own battery structurally could not have caught
(all-negative `s_rho`, 1186.6x silent error pre-repair collapsing to 2.11e-16 post-repair),
and leg 195's own 114/114 PORT reproduction stays bit-identical. **But the module isn't
closed**: two landed artifacts OUTSIDE leg 217's own declared territory —
`test_port_certification_regression.py` and a banked JSON row — still assert the OLD
pre-repair accept on the exact degenerate input leg 200 flagged, and **3 more silent paths
survive outside the 4 named mechanisms leg 217 was scoped to fix.** Leg 217 correctly
declined to touch either the out-of-territory artifacts or the 3 unscoped paths without
authorization — same discipline as leg 215's own honest partial-fix report. Drafted below,
per the orchestrator's explicit request.

```
### 241 — ROUTE-PCRC: CLEANUP FOR LEG 217's PARTIAL port_certification.py REPAIR — CORRECT
THE TWO OUT-OF-TERRITORY STALE ARTIFACTS, CHARACTERIZE THE REMAINING 3 SILENT PATHS
**Thesis.** Leg 217 correctly repaired all 4 of leg 200's named mechanisms (verified against
a control its own predecessor's battery could not have caught) but left two things
deliberately untouched, outside its own declared territory: (i)
`test_port_certification_regression.py` and a banked JSON row still assert the OLD
pre-repair accept behavior on the exact degenerate input leg 200 flagged — these are now
STALE, not correct, now that the repair has landed on leg 217's own branch; and (ii) leg
217's own report names 3 MORE silent paths in `port_certification.py` beyond the 4
mechanisms it was scoped to fix, uncharacterized. This leg does both, in order: first update
the two stale artifacts to match the post-repair behavior (a mechanical correction once leg
217's repair itself is trusted — this leg does NOT re-litigate whether leg 217's repair
itself is correct, that stays leg 217's own claim, verified separately by leg 231/PCRV once
217 lands), then characterize (not necessarily repair) the 3 additional silent paths with
the same precision leg 200's original report used for the original 4.
**Gate.** (a) Do `test_port_certification_regression.py` and the banked JSON row now assert
the CORRECT (post-leg-217-repair) behavior on the exact degenerate input leg 200 originally
flagged, with no other assertion in either artifact touched; and (b) are all 3 additional
silent paths leg 217 named characterized with a precise mechanism and magnitude, the same
shape leg 200's own report used for its original 4?
  (a) yes, (b) characterized -> Bank both. If any of the 3 additional paths is
         claim-adjacent (a banked number depends on it), escalate that specifically rather
         than folding it quietly into this cleanup leg's own landing — characterization is
         this leg's job, repair of a NEW mechanism is not.
  (a) or (b) incomplete -> Report precisely what remains and why (e.g. the stale artifacts
         depend on a leg-217 branch state this leg cannot safely assume is final pre-merge);
         do not force either half to closure prematurely.
**Territory.** test_port_certification_regression.py (the specific stale assertions leg 200
               flagged, ONLY), the specific banked JSON row leg 200/217 identified,
               experiments/p2_route_pcrc_v1_cleanup.py,
               writeup/data/p2_route_pcrc_v1_cleanup.json,
               writeup/novelty/leg_241.md, experiments/journal/leg_241.md.
               Reads (never edits beyond the two named stale artifacts) leg 217's own
               branch/report for the repair's exact behavior, and leg 200's own report for
               the 3 additional silent paths' starting characterization.
**Difficulty.** standard
**Independence.** Narrowly scoped to the two artifacts leg 217 explicitly declined to touch
plus characterization (not repair) of 3 named paths. Does not re-touch any of leg 217's own
4 repaired mechanisms. Best sequenced AFTER leg 217 itself lands/merges (so the "post-repair
behavior" it aligns the stale artifacts to is final), but can begin the characterization half
(b) immediately since that only reads leg 200's/217's own reports. Reserve — promote once a
slot frees, ideally timed with or just after leg 217's own landing.
```

**Slot B refilled with leg 230 (TNRV)** — verifying leg 220's already-landed
`target_norm.py` repair, per the postrepair-verification pattern.

**Live-slot roster, corrected:**

| Slot | Leg | Route | Floor status |
|---|---|---|---|
| A | 192 | H2CV | verify — not floor-eligible |
| B | 230 | TNRV | **live, newly promoted** — verify — not floor-eligible |
| C | 239 | USC3 | FLOOR-ELIGIBLE (literature) |
| D | 221 | BVRR | repair — not floor-eligible (nearly done) |
| E | 237 | SIRC | audit/census — not floor-eligible |
| F | 236 | RDDEP | FLOOR-ELIGIBLE (math) |
| G | 240 | CNS2 | FLOOR-ELIGIBLE (literature) |
| H | 218 | BHR | repair — not floor-eligible |
| I | 210 | M2SV | verify — not floor-eligible |
| J | 226 | PNR | repair — not floor-eligible (actively running numerical probes) |

**Floor status: 3/10 — still MET (236, 239, 240), unaffected by this round's changes.**

**Reserve queue, recomputed precisely: previous reserve (216, 225, 227, 228, 229, 230, 231,
232, 233, 234, 235) minus 230 (promoted to slot B) plus 241 (newly drafted) = 11 undispatched
legs (216, 225, 227, 228, 229, 231, 232, 233, 234, 235, 241).**

Nothing in this update lifts a ban, resolves any parked escalation, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised by this DM this cycle.

---

## DM bookkeeping update, cycle 1, same day — 239 lands MIXED (escalation correctly held),
241 promoted into slot C, floor back to 2/10, a spare floor-eligible candidate drafted now
rather than reactively

**239 (USC3) landed on `main` (`27b2d5b`) — gate MIXED.** Reported per-obstruction as its
own gate required: 2 of `arXiv:2511.22819`'s three new obstructions are technique-specific,
1 is model-specific. **Escalation correctly did NOT fire on the model-specific one** — the
leg ran its own positive control before deciding (the named alternative model class was
checked against this repository's own infrastructure and matched only a bibliography line,
not an actual buildable model, versus 12/33 real hits for Boussinesq/gCLM terms) — exactly
the falsifiable-control discipline this repository's own standing practice requires before
an escalation fires. Clean landing.

**Slot C refilled with leg 241 (PCRC)**, the cleanup leg drafted last round for leg 217's
partial repair — now in flight.

**This drops the composition floor back to 2/10 (236, 240), since 239 was floor-eligible.**
Per this DM's own process note two updates above (floor-eligible legs land faster than the
repair/verify batch; worth keeping a spare ready rather than scrambling each time), a new
floor-eligible candidate is drafted now, proactively, rather than waiting for the
orchestrator's next vacancy report — the orchestrator explicitly offered either sequencing
this round; this DM chooses to draft first and let the orchestrator decide preempt-vs-wait
once it exists, rather than pre-committing to preemption before the candidate is even
written.

```
### 242 — ROUTE-DFL2: DO Dahne & Figueras (OR COAUTHORS) HAVE LATER WORK EXTENDING
arXiv:2410.05480's CGL SELF-SIMILAR BRANCHES TOWARD A GENUINELY FLUID/VORTEX-DYNAMICS MODEL,
OR TOWARD COMPLETING "THE MISSING RUNG"? (a spare floor-eligible candidate, drafted
proactively per this DM's own process note)
[FLOOR-ELIGIBLE: literature — extends a landed literature/re-derivation finding at full-text
depth, not an audit/repair/verify]
**Thesis.** `arXiv:2410.05480` (Dahne & Figueras) interval-verifies self-similar singular CGL
branches continued in a dissipation parameter; leg 48 (Route-V) independently re-derived it
to 1.8e-07, and it is the paper that closed stage V for non-novelty. Leg 174 (VBS) later
asked whether this constitutes a completed certified viscous blow-up "in any model" (finding:
yes, but NOT in a fluid/vortex-dynamics-adjacent model — CGL is the wrong category) and
separately cataloged what other viscous fluid-adjacent models have an existing analytic
blow-up proof. Neither leg asked the follow-up this repository's own established
"check for later work by the same authors" pattern (175->196, 174/197->240) already applies
twice elsewhere: does Dahne & Figueras (or a coauthor) have SUBSEQUENT published work that
either (a) extends the same interval-verification technique to a genuinely fluid/vortex-
dynamics-adjacent model (closing leg 174's own empty occupancy-matrix cell directly), or (b)
completes the CGL branch work itself into an actual blow-up certificate rather than a
verified-branch/continuation result (closing leg 174's (a)-question about whether the rung
is genuinely empty)?
**Gate.** Does Dahne & Figueras's subsequent published work extend the interval-verification
technique to a fluid/vortex-dynamics-adjacent model, or complete the CGL work into an actual
certified blow-up?
  yes (either) -> This would bear directly on leg 174's own "missing rung" occupancy matrix
         — record the citation and its hypotheses verbatim, state precisely which cell it
         fills or doesn't, and ESCALATE; do not attempt to replicate or build on it under
         this leg's own authority.
  no -> Report the search precisely (this repository's own discipline: report the search,
        not just the absence). Bank as confirming leg 174's own catalog is still current on
        this specific author line.
**Territory.** experiments/p2_route_dfl2_v1_lit.py, writeup/data/p2_route_dfl2_v1_lit.json,
               writeup/novelty/leg_242.md, experiments/journal/leg_242.md.
               Reads (never edits) leg 48's and leg 174's own reports/JSONs and
               solver/viscous_novelty.py's PRECEDENTS ledger, read-only.
**Difficulty.** light
**Independence.** Literature-only, own JSON, no solver module. Disjoint from every other
live/reserve leg (48/174 already landed and closed; this extends them, doesn't re-open
them; 240 checks a DIFFERENT author line, `arXiv:2208.09445`'s). Immediately dispatchable —
this DM's own choice for the next floor vacancy, whether via preemption or natural opening,
at the orchestrator's discretion.
```

**Reserve queue: 11 undispatched legs (216, 225, 227, 228, 229, 231, 232, 233, 234, 235,
242).** (241 is now live in slot C, not reserve — the prior update's count already reflected
that; this update adds 242 fresh.) 242 is flagged as floor-eligible and ranked for IMMEDIATE
promotion the moment any slot opens (or via preemption, orchestrator's call this round, per
its own offer) — do not let a non-floor-eligible reserve item take the next vacancy ahead of
242 while the floor sits at 2/10.

**Floor status: 2/10 (236, 240) right now, with 242 drafted and ready to restore it to
3/10 the moment it is dispatched.**

Nothing in this update lifts a ban, resolves any parked escalation, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised by this DM this cycle.

---

## DM bookkeeping update, cycle 1, same day — 230 and 240 land clean, 235/242 promoted into
B/G, floor unchanged at 2/10 (242 exactly replaces 240)

**230 (TNRV) landed — independently confirmed leg 220's `target_norm.py` repair, and found
something new in the process.** A decisive NEW test case (`wide_asymmetric`) leg 220 never
ran: the pre-repair window falsely reported 0-outside where 7 samples truly escaped, worst
undercount 677x. Also re-solved leg 55's other two margins for the first time. A strong
independent-verification result, exactly the kind of thing this discipline exists to catch —
a postrepair-verification leg finding the repair correct but the ORIGINAL repair's own test
coverage incomplete.

**240 (CNS2) landed — a thorough NO.** No viscous-term enclosure found anywhere in
`arXiv:2208.09445`'s author group's later work; a DIFFERENT group independently reaching the
same domination theorem via the identical mechanism confirms domination isn't a
computer-assistance artifact of this one group's method. Leg 174's Grade-A/fluid occupancy
cell stays confirmed empty. Clean, informative negative.

**Slot G refilled with leg 242 (DFL2)** — the spare floor-eligible candidate drafted last
round, now checking Dahne & Figueras's own later work, exactly replacing 240's floor-eligible
occupancy. **Slot B refilled with leg 235 (CDAP)** — the recurrence census for leg 202's
"ignored caller diagnostic" defect shape, per this DM's own promotion order.

**Live-slot roster, corrected:**

| Slot | Leg | Route | Floor status |
|---|---|---|---|
| A | 192 | H2CV | verify — not floor-eligible |
| B | 235 | CDAP | **live, newly promoted** — audit/census — not floor-eligible |
| C | 241 | PCRC | repair/cleanup — not floor-eligible |
| D | 221 | BVRR | repair — not floor-eligible |
| E | 237 | SIRC | audit/census — not floor-eligible |
| F | 236 | RDDEP | FLOOR-ELIGIBLE (math) |
| G | 242 | DFL2 | **live, newly promoted** — FLOOR-ELIGIBLE (literature) |
| H | 218 | BHR | repair — not floor-eligible |
| I | 210 | M2SV | verify — not floor-eligible |
| J | 226 | PNR | repair — not floor-eligible |

**Floor status: 2/10 (236, 242) — unchanged by this round**, since 242 landed exactly in
240's vacated floor-eligible occupancy. Still below the required 3; this DM will draft
another spare floor-eligible candidate at the next opportunity rather than wait for the
count to drop further.

**Reserve queue: 9 undispatched legs (216, 225, 227, 228, 229, 231, 232, 233, 234)** — 235
and 242 now live (off reserve); no other change.

Nothing in this update lifts a ban, resolves any parked escalation, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised by this DM this cycle.

---

## DM bookkeeping update, cycle 1, same day — 241 escalates (partial, correctly deferred),
a flagged claim gets a sanity-check leg, reserve tracking corrected (225 and 218 were never
really reserve), 227 promoted into slot C

**241 (PCRC) escalated, not merged** (`leg/241-pcrc-v1` pushed, `main` untouched).
**(a) INCOMPLETE, correctly and deliberately so**: the correction for the stale
`port_certification.py` artifacts is authored and verified against leg 217's own parked
branch, but not applied — applying it now would fail the gate against `main`, since leg 217
itself hasn't merged. Good discipline: not forcing a fix to land against a moving target.
**Also found the bank is stale in FIVE rows, not the one leg 217 originally named** — a
wider version of the same "stale artifact" problem, characterized precisely rather than
undercounted. **(b) Characterized all 3 remaining silent paths, none claim-adjacent**, though
two carry margin exactly `0.0` — correct only by a hardcoded literal or caller convention,
nothing structurally enforcing it, worth remembering as fragile even though not currently
wrong.

**One note flagged by the orchestrator for a sanity check, taken seriously despite the leg's
own "not claim-adjacent" conclusion**: leg 241's own report states `stall_verdict`'s
positional-read finding "flips the published verdict on the one ladder carrying Route-L's
headline" at 94.56x. The phrase itself — flipping a PUBLISHED verdict on a HEADLINE ladder —
is alarming enough on its face that this DM does not want to rely solely on the same leg's
own "concluded not claim-adjacent" judgment without an independent second look, exactly the
orchestrator's own instinct. Drafted below as a light, non-urgent verification leg.

```
### 243 — ROUTE-PCRS: SANITY-CHECK LEG 241's "NOT CLAIM-ADJACENT" CONCLUSION ON THE
stall_verdict / ROUTE-L HEADLINE-FLIP PHRASE (RESERVE, not urgent per the orchestrator's own
framing, but not deferred indefinitely either)
**Thesis.** Leg 241 (PCRC), characterizing `port_certification.py`'s 3 remaining silent
paths, reported that `stall_verdict`'s positional-read finding "flips the published verdict
on the one ladder carrying Route-L's headline" at 94.56x — and then concluded, in the same
report, that this is NOT claim-adjacent. Those two statements sit close enough together that
an independent second read is warranted before trusting the "not claim-adjacent" half at
face value: a 94.56x flip of a HEADLINE ladder's published verdict is exactly the shape of
thing this repository's own discipline treats as high-stakes when found elsewhere (e.g. leg
202/226's Route-D v11 exposure). This leg does not re-litigate leg 241's own characterization
of the mechanism — it independently re-checks specifically whether "Route-L's headline"
really is unaffected, the same way leg 236 independently re-checks Route-D v11 rather than
trusting leg 226's own repair-time re-derivation alone.
**Gate.** Does an independent re-check confirm Route-L's own published headline verdict is
UNAFFECTED by the `stall_verdict` positional-read finding leg 241 characterized (i.e., the
94.56x flip occurs only in a case that does not correspond to Route-L's actual banked
headline configuration), matching leg 241's own "not claim-adjacent" conclusion?
  yes -> Independently confirmed; bank as closing this specific worry, distinct from and
         additional to leg 241's own characterization.
  no -> **Route-L's headline is affected.** This would be a second confirmed instance
         (after leg 202/226) of a banked headline actually needing correction — escalate
         immediately at the same priority, do not fold quietly into leg 241's own landing.
**Territory.** experiments/p2_route_pcrs_v1_verification.py,
               writeup/data/p2_route_pcrs_v1_verification.json,
               writeup/novelty/leg_243.md, experiments/journal/leg_243.md.
               Reads (never edits) leg 241's own report/JSON and Route-L's own banked
               headline report, read-only.
**Difficulty.** standard
**Independence.** Read-only re-check. Disjoint from every other live/reserve leg. Reserve —
not urgent per the orchestrator's own framing, but promote within the next few rounds rather
than let it sit indefinitely, given what it's checking.
```

**Bookkeeping correction, per the orchestrator's own note: this DM's reserve tracking had
two more errors.** **225 (RSR)** was dispatched earlier this cycle and is actively running
(mid-work, having already caught and corrected its own R1-vs-R2 scope question) — it was
never really "undispatched reserve," this DM's list was simply stale. **218 (BHR)** has a
rich journal commit on its own branch but hasn't pushed to `main` — still finishing, correctly
already tracked as live in slot H, not reserve (no correction needed there, just confirming
this DM's slot-H entry was already right). Removing 225 from the reserve count:

**Slot C refilled with leg 227 (EGMT)** — the tiny mechanical tense-fix for leg 213's
cosmetic finding, fully unblocked and ready.

**Live-slot roster, corrected:**

| Slot | Leg | Route | Floor status |
|---|---|---|---|
| A | 192 | H2CV | verify — not floor-eligible |
| B | 235 | CDAP | audit/census — not floor-eligible |
| C | 227 | EGMT | **live, newly promoted** — mechanical fix — not floor-eligible |
| D | 221 | BVRR | repair — not floor-eligible |
| E | 237 | SIRC | audit/census — not floor-eligible |
| F | 236 | RDDEP | FLOOR-ELIGIBLE (math) |
| G | 242 | DFL2 | FLOOR-ELIGIBLE (literature) |
| H | 218 | BHR | repair — not floor-eligible (mid-finish, not landed) |
| I | 210 | M2SV | verify — not floor-eligible |
| J | 226 | PNR | repair — not floor-eligible |

**Floor status: 2/10 (236, 242) — unchanged.**

**Reserve queue, corrected: 7 undispatched legs (216, 228, 229, 231, 232, 233, 234), plus
243 (new) = 8 undispatched legs (216, 228, 229, 231, 232, 233, 234, 243).** 225 removed
(already dispatched, not reserve — this DM's tracking error, now fixed); 227 promoted to
slot C; 243 newly drafted.

Nothing in this update lifts a ban, resolves any parked escalation, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised by this DM this cycle.

---

## DM bookkeeping update, cycle 1, same day — 218 lands YES (this cycle's highest-stakes
repair, closed cleanly), 227 lands clean, 228/243 promoted into H/C

**218 (BHR) landed on `main` (`d9a20fb`/`fe6aab0`) — gate YES on both clauses.** Closes this
cycle's single highest-blast-radius latent defect (leg 198's `bordered_hl.py` finding,
1.198e9x/1.189e17x corruption potential). Notably thorough: it found that BOTH the
dispatch's own caller-set premise AND leg 198's own supporting predicate were false,
corrected both rather than patching around them, adopted its own corrected predicate, found
a genuinely new in-kind extension (`+inf` weights understate by 33.7x, not previously
characterized), and reconciled an apparent `Z_1`-ratio discrepancy with leg 198's own numbers
via lesson 86 (round-off floor, environment-dependent ratio, verdict itself robust). **0
banked numbers at risk.** Given the stakes, leg 228 (BHRV, independent verification) was
dispatched immediately rather than waiting for a natural vacancy — exactly the priority this
DM assigned it when drafting it several updates ago.

**227 (EGMT) landed cleanly** — the cosmetic tense-fix, exactly as scoped, no surprises.

**Slots H and C refilled** with **228 (BHRV)** — independent verification of leg 218's own
repair, given the stakes — and **243 (PCRS)** — this DM's own Route-L headline sanity check,
drafted last round.

**Live-slot roster, corrected:**

| Slot | Leg | Route | Floor status |
|---|---|---|---|
| A | 192 | H2CV | verify — not floor-eligible |
| B | 235 | CDAP | audit/census — not floor-eligible |
| C | 243 | PCRS | **live, newly promoted** — verify — not floor-eligible |
| D | 221 | BVRR | repair — not floor-eligible |
| E | 237 | SIRC | audit/census — not floor-eligible |
| F | 236 | RDDEP | FLOOR-ELIGIBLE (math) |
| G | 242 | DFL2 | FLOOR-ELIGIBLE (literature) |
| H | 228 | BHRV | **live, newly promoted** — verify — not floor-eligible |
| I | 210 | M2SV | verify — not floor-eligible |
| J | 226 | PNR | repair — not floor-eligible |

**Floor status: 2/10 (236, 242) — unchanged; neither 218 nor 227 was floor-eligible, so no
change from this round's landings.**

**Reserve queue: 6 undispatched legs (216, 229, 231, 232, 233, 234)** — 228 and 243 now live
(off reserve); no other change.

Nothing in this update lifts a ban, resolves any parked escalation, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised by this DM this cycle.

---

## DM URGENT bookkeeping update, cycle 1, same day — 242 and 243 land, floor drops to
1/10, reserve confirmed genuinely empty of dispatchable items, two fresh legs drafted now

**242 (DFL2) landed — a thorough NO.** Dahne & Figueras have zero later relevant work; leg
174's Grade-A/fluid occupancy cell stays confirmed empty. Clean, informative, floor-eligible
— its landing is exactly why the floor drops now.

**243 (PCRS) landed — gate YES.** Independently confirmed Route-L's own headline is
genuinely unaffected by leg 241's `stall_verdict` finding, closing that concern cleanly. It
also found the margin really is exactly `0.0` and flagged that a small repair keying the
verdict on array order (rather than the fragile literal/convention this cycle's earlier
characterization already noted) is still warranted. Drafted below.

**Reserve confirmed genuinely empty of anything dispatchable right now, per the
orchestrator's own direct check — this DM's list was stale in exactly the way flagged.**
**216** already ran and escalated earlier this cycle; it should not have still been in this
DM's reserve count (a bookkeeping miss, corrected now). **229** is blocked on leg 226 (still
only at its novelty-pass commit). **231-234** are all blocked on repairs (217, 219, 221, 225)
none of which has landed yet. **Zero of the six were actually promotable.** Two fresh legs
drafted now, urgently, per the orchestrator's explicit request: one floor-eligible, one
immediately-dispatchable and unblocked.

```
### 244 — ROUTE-PCRO: REPAIR stall_verdict's ARRAY-ORDER DEPENDENCE (leg 243's flagged
finding — margin is exactly 0.0, verdict currently correct only by array-order convention)
**Thesis.** Leg 243 (PCRS), while independently confirming Route-L's headline is unaffected
by leg 241's finding, found the margin protecting that verdict is exactly `0.0` — correct
today only because of the specific order `stall_verdict` reads its array in, not because
anything structurally enforces the right answer regardless of order. This is the same shape
of fragility leg 241 itself flagged for two of the 3 characterized silent paths (margin
exactly 0.0, correct only by hardcoded literal/caller convention) — worth closing before a
future refactor or reordering silently flips it.
**Gate.** Does making `stall_verdict`'s verdict robust to array order (rather than relying on
the current incidental ordering) preserve every currently-correct verdict (Route-L's
headline included, re-checked explicitly) while removing the order-dependence leg 243 found?
  yes -> Bank the repair; Route-L's headline and every other currently-correct verdict is now
         robust rather than incidentally correct. Flag for a light postrepair check.
  no -> Report exactly which verdict the fix disturbs and why; do not land a fix that trades
        one fragility for another.
**Territory.** solver/port_certification.py (`stall_verdict`'s array-order handling only),
               experiments/p2_route_pcro_v1_repair.py,
               writeup/data/p2_route_pcro_v1_repair.json,
               writeup/novelty/leg_244.md, experiments/journal/leg_244.md.
               Reads (never edits beyond the named function) leg 243's own report and
               Route-L's own banked headline report.
**Difficulty.** standard
**Independence.** Narrowly scoped to one function's array-order handling. Does not touch
leg 217's own 4 repaired mechanisms or leg 241's own pending stale-artifact correction (a
different part of the same module, different concern). Immediately dispatchable — not
blocked on anything in flight.
```

```
### 245 — ROUTE-BCL2: DOES arXiv:2404.04054's OWN AUTHORS ([BC], THE VISCOUS-BURGERS
GRADE-A PRECEDENT) HAVE LATER WORK EXTENDING PAST BURGERS TOWARD A HARDER, MORE
FLUID/VORTEX-ADJACENT MODEL? (restores the composition floor, urgent per this cycle's drop
to 1/10)
[FLOOR-ELIGIBLE: literature — extends a landed literature/precedent finding at full-text
depth, not an audit/repair/verify]
**Thesis.** `arXiv:2404.04054` ([BC] in `solver/viscous_novelty.py`'s own PRECEDENTS ledger)
is leg 174's own cited example of a technique that is ALREADY Grade A (computer-assistance
essential, viscous term genuinely enclosed, not dominated) — but only on viscous Burgers, a
1D model well short of anything fluid/vortex-dynamics-adjacent. This is arguably the single
most direct literature question left in the "missing rung" line: unlike the two just-closed
NO results (240 checked `2208.09445`'s own authors — no later work; 242 checked Dahne &
Figueras — no later work), THIS precedent is the one that already has the right GRADE, just
not yet the right MODEL. If these authors (or close collaborators) have moved the same
Grade-A technique toward a 2D/3D or vorticity-bearing model, that is the closest thing to
filling leg 174's empty occupancy cell this repository's own literature survey could find.
**Gate.** Does `arXiv:2404.04054`'s author group have subsequent published work applying the
same Grade-A (computer-assisted, viscous-term-enclosing) technique to a model closer to
fluid/vortex dynamics than 1D viscous Burgers (2D, vorticity-bearing, or a genuine
Navier-Stokes-family reduction)?
  yes -> This would be the closest approach yet to filling leg 174's empty Grade-A/fluid
         cell — record the citation, its hypotheses, and precisely how close the model is to
         genuinely fluid/vortex-dynamics-adjacent. ESCALATE immediately; do not attempt to
         replicate or build on it under this leg's own authority.
  no -> Report the search precisely, same discipline as 240/242. Bank as confirming the
        Grade-A technique's own frontier is still 1D Burgers, narrowing (not closing) the
        "missing rung" search.
**Territory.** experiments/p2_route_bcl2_v1_lit.py, writeup/data/p2_route_bcl2_v1_lit.json,
               writeup/novelty/leg_245.md, experiments/journal/leg_245.md.
               Reads (never edits) leg 174's own report/JSON and
               solver/viscous_novelty.py's PRECEDENTS ledger, read-only.
**Difficulty.** light
**Independence.** Literature-only, own JSON, no solver module. Disjoint from 240 (different
author group/paper) and 242 (different author group/paper) — same PATTERN, different,
non-overlapping literature target. Immediately dispatchable, not blocked on anything.
```

**Slots C and G filled with 244 (PCRO) and 245 (BCL2) respectively.**

**Live-slot roster, corrected:**

| Slot | Leg | Route | Floor status |
|---|---|---|---|
| A | 192 | H2CV | verify — not floor-eligible |
| B | 235 | CDAP | audit/census — not floor-eligible |
| C | 244 | PCRO | **live, newly promoted** — repair — not floor-eligible |
| D | 221 | BVRR | repair — not floor-eligible |
| E | 237 | SIRC | audit/census — not floor-eligible |
| F | 236 | RDDEP | FLOOR-ELIGIBLE (math) |
| G | 245 | BCL2 | **live, newly promoted** — FLOOR-ELIGIBLE (literature) |
| H | 228 | BHRV | verify — not floor-eligible |
| I | 210 | M2SV | verify — not floor-eligible |
| J | 226 | PNR | repair — not floor-eligible (in progress; own novelty pass already found the dispatch's premise was false, investigating properly per item 3(a)'s own amended gate) |

**Floor status: 2/10 (236, 245) — restored from 1/10.** Still below the required 3; this DM
will draft a further spare floor-eligible candidate at the next opportunity, per its own
standing process note, rather than wait for another urgent scramble.

**Reserve queue: 5 undispatched legs (229, 231, 232, 233, 234)** — 216 removed (already
ran/escalated, this DM's tracking error now fixed); all five remaining are correctly blocked
(229 on leg 226; 231-234 on repairs 217/219/221/225, none landed yet) — **genuinely zero
dispatchable reserve right now**, confirmed. This DM will monitor for the moment any of
217/219/221/225/226 lands and immediately flag the corresponding unblocked item(s) rather
than wait to be asked.

Nothing in this update lifts a ban, resolves any parked escalation, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised by this DM this cycle.

---

## DM bookkeeping update, cycle 1, same day — 237 lands YES with good discipline, slot E
left open per the orchestrator's own judgment, one fresh floor-eligible candidate drafted
since the opportunity was offered

**237 (SIRC) landed on `main` (`c9d507a`) — gate YES.** Found a second instance of leg 202's
scale-invariant-residual defect class, this time in `collocation_newton.py` — but correctly
graded it latent and NOT claim-adjacent, after running a thorough 6-route reachability
battery (0/41 escapes vs. 2/2 reproducing leg 202's own banked numbers, confirming the
battery itself is a real contrast, not a null result that happened to find nothing). Good
discipline: it caught and reported what could have been a false positive before shipping it
as an escalation.

**Flagged for the orchestrator's own checking, not this DM's**: leg 217's branch appears
gone from local refs. This DM does not investigate git/branch state itself (outside its own
file-only remit) — noting it here only so it isn't lost, and deferring entirely to the
orchestrator's own verification.

**Slot E left open, per the orchestrator's own judgment** — correctly declining to force a
premature verification leg when nothing in the (confirmed-blocked) reserve is ready. Since
the orchestrator explicitly invited a fresh draft in the meantime, this DM used the
opportunity to draft one more floor-eligible candidate — a genuinely well-grounded literature
question this file had not yet asked, directly relevant to the γ=2 dissipative gCLM line
this repository has invested the most legs in (63, 125, 174, 185, 187, 193):

```
### 246 — ROUTE-ALSL2: DO Ambrose, Lushnikov, Siegel & Silantyev HAVE LATER WORK UPGRADING
arXiv:2207.07548's gCLM-WITH-DISSIPATION ANALYSIS INTO AN ACTUAL COMPUTER-ASSISTED
CERTIFICATE? (a fresh floor-eligible candidate, offered for slot E, not urgent)
[FLOOR-ELIGIBLE: literature — extends a landed literature/precedent finding at full-text
depth, not an audit/repair/verify]
**Thesis.** `arXiv:2207.07548` (Ambrose, Lushnikov, Siegel, Silantyev), in
`solver/viscous_novelty.py`'s own PRECEDENTS ledger, studies gCLM WITH dissipation —
global existence vs. singularity formation, line vs. circle — via analysis and numerics,
explicitly "no certificate of a profile." This is the single most directly relevant
precedent to this repository's own γ=2 dissipative gCLM investigation line (63/125/174/185/
187/193) of anything in the ledger, since it studies the SAME dissipative gCLM family this
repository has spent the most legs on — yet nobody has checked whether these specific
authors have since produced an actual certificate, the same "did the authors' later work
close the gap" question this repository's pattern (175->196->239, 2208.09445->240,
2410.05480->242) already applies to three other precedents.
**Gate.** Do Ambrose, Lushnikov, Siegel, or Silantyev (or close collaborators) have
subsequent published work that upgrades `arXiv:2207.07548`'s gCLM-with-dissipation analysis
into an actual computer-assisted certificate of a profile (of any dissipation exponent
`sigma`, not necessarily `gamma=2` specifically)?
  yes -> This would bear directly on the entire γ=2 dissipative gCLM line this repository has
         invested in — record the citation, its hypotheses, and precisely which dissipation
         exponent(s) it covers, verbatim. ESCALATE immediately; do not attempt to replicate
         or build on it under this leg's own authority.
  no -> Report the search precisely, same discipline as 240/242/245. Bank as confirming this
        specific precedent's own frontier is still "no certificate," which is itself useful
        context for anyone evaluating leg 125/187/193's own novelty claims (no certificate
        existed for THIS family before this repository's own attempts, and still doesn't
        elsewhere).
**Territory.** experiments/p2_route_alsl2_v1_lit.py, writeup/data/p2_route_alsl2_v1_lit.json,
               writeup/novelty/leg_246.md, experiments/journal/leg_246.md.
               Reads (never edits) solver/viscous_novelty.py's PRECEDENTS ledger and leg
               63's/125's own reports, read-only.
**Difficulty.** light
**Independence.** Literature-only, own JSON, no solver module. Disjoint from 240/242/245
(different author groups/papers) — same pattern, non-overlapping target. Immediately
dispatchable, not blocked on anything. Offered for slot E; not urgent, per the orchestrator's
own framing that E can stay open a while longer.
```

**Slot E: this DM offers 246 (ALSL2) but does not insist it be dispatched immediately** —
the orchestrator's own judgment to leave E open stands; 246 is simply ready the moment the
orchestrator wants it, restoring the floor to 3/10 if/when dispatched.

**Reserve queue: 6 undispatched legs (229, 231, 232, 233, 234, 246)** — 246 added; all six
remain either confirmed-blocked (229, 231-234) or offered-but-not-forced (246).

**Floor status: 2/10 (236, 245) right now, unchanged; 246 ready to restore it to 3/10
whenever dispatched.**

Nothing in this update lifts a ban, resolves any parked escalation, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised by this DM this cycle.

---

## DM bookkeeping update, cycle 1, same day — 246 confirmed dispatched (floor restored to
3/10), 235 escalates with a SECOND, distinct Route-D v11 exposure, 244 lands clean, two
repairs drafted for slots B/C with territory checked against 226/236

**246 (ALSL2) confirmed dispatched into slot E** per the orchestrator's own roster — the
floor is met, **3/10 (236, 245, 246)**, as of this update.

**244 (PCRO) landed cleanly** — closes leg 243's array-order fragility in `stall_verdict`
with strong verification (1682 permutations, every published number bit-identical). No
issues.

**235 (CDAP) escalated, not merged** (`leg/235-cdap-v1` pushed, `main` untouched). **A
SECOND, DISTINCT instance of the ignored-caller-diagnostic pattern, this time in Route-D
v11's own runner (`experiments/p2_route_d_v11_anchor.py`), NOT the same mechanism leg 226 is
repairing.** Leg 226's mechanism is a bad convergence flag in `profile_newton.py`; this one
is a min/max SELECTION bug: `v5_budget`'s headline margin (`1.0468e+10`) is built from
`newton_weighted_defect_min`, while `newton_weighted_defect_max=1.5196e-02` sits one line
away and is never compared — violating that block's own Y0 budget by **62.02x at a=0.45**.
Systematically confirmed isolated (0 instances across the other 195 banked JSONs, 4320
verdicts screened) — a real, precisely-scoped, second headline exposure, not a recurrence of
226's own mechanism. **It also corrects leg 202 itself**: 2 of leg 202's 3 quoted
`weighted_defect` magnitudes attach to rows already marked `grid_converged=false` — leg 202's
own finding SHAPE stands, but two of its cited numbers were on the wrong rows. Route-D v11
now carries two independent, distinct exposures in flight.

**Territory checked before drafting, per the orchestrator's own request.** 226 owns
`solver/profile_newton.py` exclusively (a different file, a different mechanism — bad
convergence flag, not min/max selection). 236 (RDDEP) only READS Route-D v11's own banked
report/JSON, never edits the runner itself. **235's own fix target
(`experiments/p2_route_d_v11_anchor.py`'s min/max selection logic) is confirmed disjoint
from both** — no file-level collision with 226 or 236. Drafted below.

```
### 247 — ROUTE-VBR: REPAIR Route-D v11's v5_budget MIN/MAX SELECTION BUG (leg 235's
finding — a SECOND, distinct Route-D v11 exposure, not the same mechanism as leg 226)
**Thesis.** Leg 235 found `v5_budget`'s headline margin is built from
`newton_weighted_defect_min` while `newton_weighted_defect_max` sits one line away, unused —
violating the block's own Y0 budget by 62.02x at `a=0.45`, confirmed isolated to this one
runner (0/195 other banked JSONs affected, 4320 verdicts screened). This is independent of
leg 226's own repair (a different mechanism, `profile_newton.py`'s convergence flag) — fix
this one on its own terms, using `newton_weighted_defect_max` (or an explicit,
correctly-reasoned combination of both) rather than silently substituting one for the other.
**Gate.** Does using the correct selection (per leg 235's own diagnosis) for `v5_budget`'s
margin computation at `a=0.45` bring the block back within its own declared Y0 budget, and
does re-running the other 195 banked JSONs confirm they remain unaffected (matching leg
235's own 0/195 isolation finding)?
  yes -> Bank the repair. Report the corrected `a=0.45` margin precisely — this is
         Route-D v11's SECOND confirmed headline-adjacent correction this cycle (after
         226/236's), so state plainly whether the corrected value changes any conclusion
         Route-D v11's own headline draws, the same discipline leg 236 applies to leg 226.
  no -> Report exactly which case resists the fix or which of the 195 other JSONs turns out
        affected after all; escalate immediately rather than declare this closed.
**Territory.** experiments/p2_route_d_v11_anchor.py (the `v5_budget` min/max selection logic
               ONLY — confirmed disjoint from leg 226's `solver/profile_newton.py` and from
               leg 236's read-only territory), experiments/p2_route_vbr_v1_repair.py,
               writeup/data/p2_route_vbr_v1_repair.json,
               writeup/novelty/leg_247.md, experiments/journal/leg_247.md.
               Reads (never edits) leg 235's own report/JSON and leg 202's own report (for
               the row-mislabeling correction leg 235 also found).
**Difficulty.** standard
**Independence.** Confirmed disjoint from 226 (different file, different mechanism) and 236
(read-only on Route-D v11's data, doesn't edit the runner). Immediately dispatchable, not
blocked on anything.
```

**Second slot filled with a repair for leg 237's own finding** (the second scale-invariant-
residual instance, in `collocation_newton.py`) — leg 237 graded it latent/non-claim-adjacent
but never repaired it, the same gap leg 202's finding left before leg 226 was drafted for it.

```
### 248 — ROUTE-CNR2: REPAIR collocation_newton.py's SCALE-INVARIANT-RESIDUAL DEFECT (leg
237's finding — mirrors leg 226's fix for the same defect CLASS in profile_newton.py)
**Thesis.** Leg 237 (SIRC) found a second instance of leg 202's scale-invariant-residual
defect class in `collocation_newton.py`, confirmed via a thorough 6-route reachability
battery (0/41 escapes vs. 2/2 reproducing leg 202's own banked numbers) as latent and NOT
claim-adjacent — but never repaired, since 237's own territory was characterization, not
repair (the same division of labor as 202/226). This leg closes it, using the same fix
shape leg 226 applies to `profile_newton.py` (incorporating an available, non-scale-invariant
diagnostic into the convergence verdict, per leg 237's own report of what that would be for
this module).
**Gate.** Does the repair cause all 41 of leg 237's own reachability-battery cases to
correctly reject/flag, while the 2 cases that reproduce leg 202's own banked numbers remain
correctly flagged as genuine (not accidentally suppressed by an overcorrected fix)?
  yes -> Bank the repair; this closes leg 237's finding on the same footing as 226 closes
         202's. Flag for a light postrepair check once a slot is available.
  no -> Report exactly which case resists the fix; escalate rather than declare it closed.
**Territory.** solver/collocation_newton.py (the scale-invariant-residual convergence check
               only — does not touch leg 150's own earlier, different repair to this same
               module), experiments/p2_route_cnr2_v1_repair.py,
               writeup/data/p2_route_cnr2_v1_repair.json,
               writeup/novelty/leg_248.md, experiments/journal/leg_248.md.
               Reads (never edits) leg 237's own report/JSON.
**Difficulty.** standard
**Independence.** Confirmed disjoint from 226/247 (different files/modules) and from leg
150's own already-closed, unrelated repair to the same module. Immediately dispatchable, not
blocked on anything.
```

**Slots B and C filled with 247 (VBR) and 248 (CNR2) respectively.**

**Live-slot roster, corrected:**

| Slot | Leg | Route | Floor status |
|---|---|---|---|
| A | 192 | H2CV | verify — not floor-eligible |
| B | 247 | VBR | **live, newly promoted** — repair — not floor-eligible |
| C | 248 | CNR2 | **live, newly promoted** — repair — not floor-eligible |
| D | 221 | BVRR | repair — not floor-eligible |
| E | 246 | ALSL2 | FLOOR-ELIGIBLE (literature) |
| F | 236 | RDDEP | FLOOR-ELIGIBLE (math) |
| G | 245 | BCL2 | FLOOR-ELIGIBLE (literature) |
| H | 228 | BHRV | verify — not floor-eligible |
| I | 210 | M2SV | verify — not floor-eligible |
| J | 226 | PNR | repair — not floor-eligible |

**Floor status: 3/10 (236, 245, 246) — MET, unaffected by this round's two repair fills.**

**Reserve queue: 5 undispatched legs (229, 231, 232, 233, 234), unchanged by this round's two
promotions (247, 248 were drafted fresh, not drawn from this pool) — all five remain
confirmed-blocked** (229 on leg 226; 231-234 on repairs 217/219/221/225, none landed yet).
Still above the §3a watermark of 3 by count, but this DM notes explicitly: **effective
immediately-dispatchable reserve is 0**, same situation as several updates ago, resolved each
time by fresh drafting rather than by the blocked pool clearing. This DM will keep drafting
fresh, unblocked candidates as needed rather than wait
on 217/219/221/225/226 to land.

Nothing in this update lifts a ban, resolves any parked escalation, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised by this DM this cycle.

---

# MAJOR TURNING POINT, 2026-08-06 — TWO USER RULINGS, RELAYED VERBATIM BY THE ORCHESTRATOR.
RULING 1: PUB1/PUB2 APPROVED AS THE DELIVERABLE. RULING 2: THE EXIT CRITERION IS ANSWERED —
PURSUE A FULL CLAY SOLVE. THIS SUPERSEDES "A NOVEL TIER-3 RESULT" AS THE GOAL OF RECORD, AND
**RESOLVES ESCALATION #1** ("what comes next now that stage B is exhausted" — the answer is
now: a new stage, under a new goal, per this ruling). Both rulings are recorded here in full
because they change what every future leg in this file is for. Nothing below claims any
movement has happened yet — this section records a DECISION, not a result.

## RULING 1 — PUB1 and PUB2 approved. Two submission-blocking legs drafted.

**Status change: PUB1 and PUB2 move from "drafted, parked for the user" to "approved, finish
for submission."** Both preconditions the user named bind SUBMISSION, not approval — they
are drafted below, immediately, per the user's own instruction.

**(a) Leg 176 has no independent verification — draft the verification leg.** The user's own
check (via leg 238's finding) is authoritative and more precise than this DM's own prior
tracking: leg 192's only commit on ANY ref is its pre-registered novelty pass, not an
ancestor of `main`, with no runner and no verdict landed. **This directly conflicts with
what this DM recorded several updates ago** (leg 192 reported as "verification substantively
complete... blocked on its own CPU-bound N=1024/2048 confirmation runs" — that earlier report
implied real, near-complete progress existed uncommitted). **This DM flags this discrepancy
explicitly rather than silently resolve it**: either (i) leg 192's agent made real progress
that still sits uncommitted somewhere and simply hasn't landed, or (ii) the earlier
"substantively complete" report was itself mistaken/stale and no real progress exists beyond
the novelty pass. This DM cannot distinguish these from here (outside its remit to inspect
running agent state or worktrees) — **this is the one thing this DM needs from the
orchestrator**: check leg 192's actual current state (is its agent still alive, does
uncommitted work exist in its worktree) before deciding whether to let it continue or
redispatch fresh. The verification leg itself is drafted below regardless of that outcome —
it is what leg 192 already was, or its clean replacement if 192 is confirmed stalled.

**(b) The leg 163/176 σ_min conflict — draft the cleanup leg.** PUB2 quotes leg 163's witness
`≥ 0.71465` at three call-sites; leg 176 measures the true value as `0.0908`, making leg
163's witness optimistic by 7.9×. Leg 238 correctly left this outside its own territory and
recorded the conflict in §3.5. Fix the three sites now.

**Route-D v11 confirmed NOT a blocker for either document** — the user verified 0 matches
for `v11`/`profile_newton` across all four files. Leg 236 stays high priority on its own
merits (Route-D v11's own headline integrity), independent of PUB1/PUB2's publication path.

```
### 249 — ROUTE-H2CV2: THE ACTUAL INDEPENDENT VERIFICATION OF LEG 176's ORIGIN-H² CERTIFICATE
(RULING-1(a), REPLACES/CONTINUES LEG 192 — SUBMISSION-BLOCKING FOR PUB2)
**Thesis.** PUB2 currently states leg 176's σ_min = 0.0908 and ‖T⁻¹‖_X = 4.026 as one leg's
own float64 measurement, honestly labeled as such in three sections — but a load-bearing
number in an approved, submission-track document needs independent verification, not an
honest label substituting for one. Leg 192 was drafted for exactly this and has been
"live" for many cycles without landing; per this DM's own flagged discrepancy above, either
resume leg 192's actual work (if real progress exists) or treat this leg as leg 192's clean
restart (if it does not) — the orchestrator's own check on 192's live state decides which,
not this leg's own authority.
**Gate.** Does an independent re-run of leg 176's construction reproduce σ_min = 0.0908 and
‖T⁻¹‖_X = 4.026 (or report a discrepancy precisely), to the same precision leg 176 itself
claims?
  yes -> Independently confirmed. PUB2's three float64-labeled sections can be upgraded to
         "independently verified," with the exact re-derivation precision stated. This is
         SUBMISSION-BLOCKING and should be prioritized accordingly.
  no -> Report the exact discrepancy precisely; escalate immediately — PUB2 is an approved,
        submission-track document and an unreproduced headline number in it is the single
        highest-priority finding this repository could produce right now.
**Territory.** test_origin_h2_certificate_postconstruction.py,
               experiments/p2_route_h2cv_v1_postconstruction.py (leg 192's own file — reuse
               if real progress exists there, per the orchestrator's check),
               writeup/data/p2_route_h2cv_v1_postconstruction.json,
               writeup/novelty/leg_192.md or leg_249.md (whichever this ends up filed under —
               orchestrator's call once 192's actual state is known),
               experiments/journal/leg_192.md or leg_249.md.
**Difficulty.** heavy (CPU-bound per leg 192's own prior status; this is the reason it has
sat mid-compute for so long, not necessarily a sign of trouble on its own)
**Independence.** Reads solver/origin_h2_certificate.py; edits nothing under either outcome.
SUBMISSION-BLOCKING for PUB2 — highest priority in the entire queue right now, above even
Route-D v11's own exposures, since PUB2 is now an approved deliverable, not a parked draft.
```

```
### 250 — ROUTE-PUB2FIX: FIX THE THREE σ_min CITATION SITES IN PUB2 (leg 163's optimistic
witness vs. leg 176's true value — RULING-1(b), SUBMISSION-BLOCKING)
**Thesis.** PUB2 quotes leg 163's witness `≥ 0.71465` at three call-sites; leg 176 measures
the TRUE σ_min as `0.0908` — leg 163's witness is optimistic by 7.9×. Leg 238 correctly left
this conflict unfixed (outside its own declared territory) and recorded it honestly in §3.5.
This leg fixes the three sites: either replace leg 163's witness with leg 176's own
measurement where the two conflict, or state both explicitly with the 7.9× discrepancy named
— whichever reading is more accurate to what each leg actually established (leg 163's
witness may have been a looser, earlier-stage BOUND rather than a wrong measurement; this leg
determines which framing is correct before editing, not just deletes the smaller number).
**Gate.** Do all three σ_min citation sites in PUB2 now state the relationship between leg
163's witness and leg 176's true value accurately (bound vs. measurement, or explicit
discrepancy, whichever is correct), with §3.5's own conflict note updated to match rather
than left redundant?
  yes -> Bank the fix. This closes ruling 1(b) — PUB2 no longer carries an internally
         unreconciled numeric conflict.
  no -> Report exactly which site resists a clean fix and why (e.g. it's unclear from either
        leg's own report which framing is correct); escalate rather than guess.
**Territory.** writeup/4_p2_lottery/TECHNICAL_P2_PUB2_V1.md (the three σ_min sites and §3.5
               ONLY), writeup/4_p2_lottery/BLOG_P2_PUB2_V1.md (if it also cites the figure),
               writeup/novelty/leg_250.md, experiments/journal/leg_250.md.
               Reads (never edits) legs 163's and 176's own reports/JSONs.
**Difficulty.** light
**Independence.** Narrowly scoped prose fix, no solver module. Disjoint from 249 (that leg
verifies the NUMBER, this leg reconciles the CITATION of a different, already-known number
against it — sequencing note: best done AFTER 249 lands, so "independently verified" can be
folded into the same edit, but can start immediately on the bound-vs-measurement question
without waiting). SUBMISSION-BLOCKING for PUB2, immediately dispatchable.
```

## RULING 2 — The exit criterion is answered: pursue a full Clay solve.

**This supersedes "a novel Tier-3 result on a model where blow-up is provable" as the plan's
own stated prize. Recorded here, in the same paragraph as the odds, per the user's own
explicit instruction 6: the goal has changed; the honest odds have not moved on their own —
Clay stays ~0.05% behind Walls 1 and 2, and that number is the user's OWN accepted risk under
the new goal, not a number this file quietly drops now that the goal is bigger.** Everything
below is a decision record and a proposed program, not a claim that anything has moved.

### 1. `plan_of_record.py` needs a new stage — drafted here, flagged for the orchestrator/user
to apply, exactly the composition-floor precedent (this DM does not own that file)

Stage `B` answered its gate NO at leg 126 (6.04× short of a perfect search over its full
declared space) and has had no successor for many cycles — escalation #1, now resolved by
this very ruling. **Proposed successor stage, drafted for literal transcription into
`plan_of_record.py`'s SEQUENCE:**

```
[ ] P0       Target selection under the Clay goal -- a Route-M-shaped leg redone against
             Clay rather than novelty: which object, which ansatz (constrained by NRS/Tsai
             to discretely self-similar / unstable-self-similar-with-finite-spectrum /
             non-self-similar -- see technical framing below), and what certification would
             even mean for it.
  deliverable: A named target object + ansatz class, with an explicit statement of what a
               certificate for it would need to show, checked against NRS/Tsai's exclusion
               and against every already-banked negative in this repository (L1's death in
               three realizations, stage B's exhaustion, the ell^1_w/origin-H^2 space-axis
               mapping).
  GATE: Does a target+ansatz combination survive the NRS/Tsai screen AND avoid every already-
        measured dead end this repository's own record contains?
    yes -> Proceed to P1 (the viscous rung) using this leg's named object.
    no  -> Report precisely which screen killed every candidate tried; this would mean the
           Clay-path target-selection question itself needs more candidates or a different
           screen before P1 can even be posed -- report honestly, do not force a candidate
           through.
```

**This DM proposes `P0` as the stage code**, matching the plan's own short-mnemonic
convention (`M`, `PORT`, `V`, `NG`, `B`). The prize/Clay lines at the top of
`plan_of_record.py`'s own printed output also need updating (prize: pursue a full Clay
solve, not "a novel Tier-3 result... NOT Clay"; Clay odds line: keep ~0.05% stated
explicitly, do not delete it just because the goal changed). This DM drafts the content;
applying it to the file is the orchestrator's action, per ruling 2's own explicit
authorization ("this is no longer an unauthorized escalation").

### 2. Ban review — two bans checked against the new goal, neither lifted unilaterally,
one recommendation each

**DSS ban** ("another DSS re-ask, or the DSS lane's expensive entrance," lifted by: never —
"three independent reasons the cheap entrances fail"). **This DM's recommendation: DO NOT
lift, but re-examine the wording.** The ban as written excludes the CHEAP entrances by three
independent reasons and separately excludes "the expensive entrance" — reading the ban's own
text (`.venv/bin/python plan_of_record.py`'s live output, checked directly by this DM before
writing this recommendation), the "never" applies to the ban as a WHOLE clause, but the three
reasons given are specifically about why the cheap entrances fail, and the expensive
entrance's own exclusion is stated only by inclusion in the same banned phrase, not by its
own independent reason. **Under the old goal (a Tier-3 result, cost-sensitive), an expensive
entrance was correctly out of scope by default. Under a full Clay goal, where the user has
explicitly accepted "building seriously heavy code," an expensive entrance is not
automatically out of scope anymore** — but this DM does not know what DSS's "expensive
entrance" actually IS in enough technical detail to recommend lifting it outright (this
would need a leg reading the DSS lane's own history first, since this DM reasons from the
plan's own printed ban text, not the underlying research). **Recommendation: keep the ban in
force as written; draft a light scoping leg (below, if the user wants it prioritized) asking
specifically whether DSS's expensive entrance is cost-shaped (excluded under the old goal for
being expensive, now potentially in scope) or was excluded for a substantive reason
independent of cost (in which case the Clay goal changes nothing). Do not lift until that
scoping leg reports.**

**Stage V's ban** ("re-opening stage V as posed," lifted by: never — "unless the question is
re-posed for a FLUID transport model, which needs L1 first"). **This DM's recommendation:
this ban's OWN LIFT CONDITION is now unliftable by its own wording**, exactly as the user
states — L1 is measured dead in three realizations (`ell^1_w` coefficient basis, leg 54;
collocation basis, leg 56; and the origin-H² lane, capped at `a=0` exactness with no transfer
to the real target, leg 163/176). A lift condition that requires "L1 first" when L1 has three
independently-dead attempts and no fourth candidate on the table is not a live path, it is a
dead letter. **Recommendation: re-pose or retire the ban deliberately, do not leave it
silently unliftable.** Given the new goal explicitly targets the viscous rung (Phase 1
below) via ansätze NRS/Tsai do not exclude, and NOT via re-attempting `L1`'s own
`ell^1`-Fourier/radii-polynomial machinery (that lane is the one measured dead three times,
independent of which model it's aimed at) — this DM's recommendation is: **retire this ban's
current wording and replace it with a forward-looking one**: "re-attempting the
`ell^1`-Fourier/radii-polynomial machinery this repository has measured dead in three
realizations (`ell^1_w` coefficient/collocation bases, origin-H² capped-at-`a=0`), on ANY
model, fluid or otherwise — lifted by: a namable FOURTH space/basis this repository has not
yet tried, with its own scoping leg establishing it isn't subject to the same three-realization
death." This makes the ban precise about WHAT is dead (the machinery, across models) rather
than gated on an now-impossible precondition (L1 succeeding first). **This DM does not apply
either change itself — both are recommendations for the user's/orchestrator's sign-off, per
ruling 2's own instruction not to lift anything unilaterally.**

**One additional watch-item, not a formal third ban-review entry (the user asked for "at
least two," this DM flags a candidate third rather than expanding scope unasked):** the
"another gCLM measurement leg" ban ("lifted by: never — the model is exhausted, Stage 3.5, leg
42") may also need a careful read before Phase 1 legs are drafted in detail, since Phase 1's
viscous-rung target could plausibly be a gCLM-family object (this repository's most-built-out
machinery). This DM has not read leg 42's own reasoning closely enough to recommend a
disposition here — flagged for whoever drafts Phase 1's actual leg content to check first,
not resolved in this update.

### 3. Technical framing, recorded verbatim from the user's own text, cross-checked against
this repository's own record where it already speaks to the same claims

- **Direction (a), global regularity, is closed to anything search-/certificate-shaped**:
  Tao's averaged-NS supercriticality barrier means energy methods plus preserved algebraic
  structure are provably insufficient. **Only direction (b)** (blow-up) is in scope.
- **Wall 2, as corrected by leg 172, is the operative constraint, and its NAIVE form (spatial
  dimension is the barrier) is false.** The real barrier is TIME-DEPENDENT singularity
  formation, not dimension — van den Berg–Williams certified genuinely 3D Ohta–Kawasaki
  stationary states in 2019. **This DM checked leg 172's own landed finding for consistency**:
  leg 172 asked whether any published work establishes a rigorous singularity/blow-up result
  for a genuinely 3D PDE and reports its own answer in this file's queue — consistent with the
  user's framing that the barrier is about TIME-DEPENDENT formation specifically, not 3D-ness
  per se (a stationary-state certificate, however genuinely 3D, is a different category from a
  time-dependent blow-up certificate). **Every work that states a 3D singularity theorem
  carrying a certificate supplies the 3D-ness via a 2D reduction (Chen–Hou) or a
  spherically-symmetric ODE profile (BCG → CGSS) — never via the certificate itself.** Any
  Clay plan drafted from this point must say explicitly which side of that line it intends to
  live on.
- **The ansatz is constrained**: Nečas–Růžička–Šverák and Tsai exclude nontrivial
  exactly-backward-self-similar 3D NS blow-up under the relevant decay. The target must be
  discretely self-similar, unstable-self-similar with a finite unstable spectrum, or
  non-self-similar. `arXiv:2604.09949` is the recorded example of what happens when this is
  missed — flagged as a negative-control citation for Phase 0's own screen, not something to
  repeat.
- **The missing rung is viscous certification, and it is strictly on the Clay path.** Leg
  174's own occupancy matrix (this DM cross-checked its own record above: "Grade-A/fluid cell
  EMPTY... for want of a target, not a method") stands, and leg 242 (this DM's own drafted
  leg, landed as a thorough NO) confirms nobody has filled it since via the one precedent
  leg 174 flagged as closest (Dahne & Figueras). **No certified viscous blow-up exists in any
  model, in any dimension. If it cannot be done in 1D, 3D NS is not a question of compute** —
  this is the single sentence this DM will hold every future Phase 1/Phase 2 leg accountable
  to.

### 4. Sequencing — Phase 0 drafted now, Phase 1 described (not yet a single dispatchable
leg — it is the shape of the NEW stage `P0`'s own successor), Phase 2 explicitly NOT drafted

**Do not build the 3D solver first.** This repository's own Route-A discipline (two unknowns
must not be debugged simultaneously) applies with more force to a 3D solver than to anything
this repository has built so far. Programme order, per the user's own instruction:

- **Phase 0 — target selection under the new goal.** Drafted below as leg 251, floor-eligible,
  immediately dispatchable, IS the content of the proposed `P0` stage above.
- **Phase 1 — the viscous rung.** Can a viscous blow-up be certified in ANY model? Well-defined,
  unclaimed, genuinely on the Clay path, does NOT need the 3D solver. This is `P0`'s own gate's
  yes-branch destination — not drafted as its own leg yet, since it depends on Phase 0's own
  named object/ansatz. Floor-eligible by nature (construction/math), once posed concretely.
- **Phase 2 — the heavy lift.** The 3D near-singular viscous solver (`PLAN.md` Stage 4,
  unscheduled; AMR or dynamic rescaling, likely compiled/GPU). **User-authorized but
  deliberately NOT drafted or sequenced yet** — Phase 1's own gate decides whether it's worth
  its cost, per the user's own explicit reasoning: a 3D candidate with no certification story
  reproduces Hou–Luo 2013 and answers nothing.

```
### 251 — ROUTE-P0T: PHASE 0 — TARGET SELECTION UNDER THE CLAY GOAL (a Route-M-shaped leg
redone against Clay, not novelty — THE FIRST LEG OF THE NEW PROGRAMME)
[FLOOR-ELIGIBLE: math/construction-scoping — the first leg of a live goal, not an
audit/repair/verify]
**Thesis.** Route-M (leg's own historical target-selection work) screened candidates against
novelty and against this repository's own multiplier/shift predicate. This leg re-runs that
same discipline against a DIFFERENT screen: NRS/Tsai's exclusion of nontrivial
exactly-backward-self-similar 3D NS blow-up under the relevant decay, meaning any candidate
object+ansatz combination must be discretely self-similar, unstable-self-similar with a
finite unstable spectrum, or non-self-similar to survive. Cross-check every candidate against
this repository's own already-banked dead ends before naming one (L1's three-realization
death; stage B's exhaustion; the space-axis mapping legs 127/163/176/182 already produced) —
this leg's job is to not re-propose something already measured dead under a new label.
`arXiv:2604.09949` is recorded as the negative-control citation: whatever this leg proposes,
it must explain why it is NOT the same mistake that paper made.
**Gate.** Does at least one target object + ansatz combination survive BOTH the NRS/Tsai
screen (not excluded) AND a check against every already-banked dead end in this repository's
own record (not a re-proposal of something already measured dead)?
  yes -> Name the object and ansatz precisely, state exactly what a certificate for it would
         need to show, and state explicitly whether it is fluid/vortex-dynamics-adjacent
         (bearing directly on Phase 1, the viscous rung) or a different model entirely.
         ESCALATE as the candidate for Phase 1 — do not attempt certification under this
         leg's own authority, that is Phase 1's job.
  no -> Report precisely which screen killed every candidate tried, and whether the failure
        is at the NRS/Tsai stage or the already-banked-dead-end stage. This would mean
        target selection itself needs more candidates or a different screen before Phase 1
        can even be posed — report honestly, this is itself a real and useful negative.
**Territory.** experiments/p2_route_p0t_v1_targetselection.py,
               writeup/data/p2_route_p0t_v1_targetselection.json,
               writeup/novelty/leg_251.md, experiments/journal/leg_251.md.
               Reads (never edits) every already-banked dead-end report this repository has
               (L1: legs 54/56/163/176/182; stage B: leg 126; the space-axis synthesis: legs
               179/186), and the NRS/Tsai/Tao/van den Berg-Williams/BCG-CGSS citations named
               in the technical framing above (full-text read required, not abstract-only,
               per this repository's own standing discipline).
**Difficulty.** heavy
**Independence.** New territory, own module. Reads (never edits) prior dead-end reports.
Immediately dispatchable — this is the first leg of the new programme; no other live leg
touches this question. HIGHEST PRIORITY alongside 249 (PUB2's own submission blocker) — this
DM recommends both be dispatched immediately, in whichever order the orchestrator's own
slot availability permits.
```

### 5. The composition floor should stop oscillating — acknowledged, not yet resolved

**Agreed diagnosis, stated back precisely**: the floor's own oscillation (2/10, "genuinely
zero dispatchable reserve," repeatedly, across many updates) was a symptom of an exhausted
sequence generating only audits and blocked repairs — a live goal generates math and
construction legs naturally, which is exactly what legs 249/250/251 above are. **This DM
commits, per the user's own instruction: if the floor still breaches 2/10 (or below) TWO
cycles after `P0` lands in `plan_of_record.py`, the problem is the ROSTER, not the reserve —
this DM will report that explicitly rather than keep drafting one-off spares to paper over
it.**

### 6. What does not change — restated, because it matters more now, not less

The three-tier win condition. Lesson 91 (name the realization — every negative-result gate
this DM drafts from this point still names its realization explicitly). The pre-committed-gate
contract (every leg above states both branches before any leg agent runs it). And, above all:
**no output is ever described as movement toward Clay unless a link of the chain actually
moves** — a goal change does not lower this bar, and this DM states explicitly that nothing
in this entire update claims any such movement. The honest odds, ~0.05%, are recorded in this
same section as the goal change, per instruction 6, as the user's own accepted risk — not
quietly dropped now that the prize is bigger.

### What this DM needs from the orchestrator, explicitly, to proceed

1. **Check leg 192's actual live state** (agent alive? uncommitted worktree progress?) before
   deciding whether leg 249 resumes it or restarts clean — this DM cannot check this itself.
2. **Dispatch legs 249, 250, and 251 as top priority**, above the existing Route-D v11/audit-
   family backlog — all three are either submission-blocking (249, 250) or the first leg of
   the new programme (251).
3. **Apply the proposed `plan_of_record.py` changes** (the `P0` stage, the prize/Clay lines)
   once ready — this DM does not own that file.
4. **Decide on the two ban-review recommendations** (DSS: keep banned, optionally dispatch a
   light scoping leg on the expensive entrance; Stage V: retire/re-pose the current wording
   per this DM's proposed replacement) — both are recommendations, not applied by this DM.

Nothing in this update lifts a ban unilaterally. Escalation #1 is RESOLVED by ruling 2 itself.
PUB1/PUB2 approval is recorded per ruling 1. The odds stay ~0.05%, recorded in the same
paragraph as the goal change, per the user's own instruction. No further direction question
raised by this DM — both rulings were clear enough to act on directly.

---

## DM bookkeeping update, cycle 1, same day — plan_of_record.py changes CONFIRMED APPLIED,
leg 192's real state resolved (recoverable, not stalled/fabricated), 249/251 dispatched,
246 lands clean, 247 escalates with a Route-D v11 artifact still needing regeneration

**All of this DM's proposed `plan_of_record.py` changes are confirmed applied by the
orchestrator**: Stage B marked DONE (gate NO, leg 126); new stage `P0` added as NEXT with
this DM's exact proposed content; the PRIZE line updated to state the Clay goal with odds
and Walls recorded in the same breath, per instruction 6; Wall 2 corrected per this DM's own
technical-framing paragraph (time-dependent singularity formation, not dimension); Stage V's
ban re-posed with this DM's recommended forward-looking wording (naming the machinery as dead
across models, not gated on the now-impossible "needs L1 first" precondition); the DSS ban
kept unchanged, as recommended. `test_plan_of_record.py`'s honesty-invariant test was
correctly adapted (checking odds+walls are recorded alongside the goal, not the now-obsolete
literal "NOT Clay" string) rather than weakened. `CLAY_ROADMAP.md` got an appended §7.5
(existing §7 untouched, so the drift-detector stays satisfied) and
`CONTINUATION_PROMPT.md`'s Directive 1 now points at Route-P0T (leg 251). All 8
plan-of-record tests pass, merge gate passes, pushed to `main`. **This closes escalation #1
for real, not just as a recorded ruling — the plan itself now has a `NEXT` stage again.**

**Leg 192's actual state resolved, per the orchestrator's direct check this DM requested**:
its agent is gone from the active task list, but real, substantial work exists uncommitted in
its own worktree (an 871-line runner, a 592-line JSON with real data, a full journal) — **not
stalled or fabricated, just never landed.** Leg 249 was dispatched with explicit instructions
to recover and verify that existing work rather than necessarily restarting from scratch —
exactly the right call given what was actually found, and this DM's earlier flagged
discrepancy (its own "substantively complete" tracking vs. leg 238's "no runner, no verdict"
finding) is now resolved: BOTH were partially right — real work existed, it just never
reached a landed commit. Leg 251 (Phase 0) was also dispatched, with the full technical
framing folded into its brief.

**246 (ALSL2) landed — a thorough NO.** No certificate exists for the Ambrose/Lushnikov/
Siegel/Silantyev author line either. This closes the third of three "does this precedent's
author line have later work" checks this cycle (240, 242, 246), all NO — this DM notes, for
Phase 0's own benefit, that this repository's own literature survey has now checked every
directly-relevant precedent in `viscous_novelty.py`'s ledger for a later-work upgrade and
found nothing, which is itself part of why "the missing rung is strictly on the Clay path" is
stated with confidence in the technical framing above, not just asserted.

**247 (VBR) escalated, not merged.** The repair itself is correct — but it reveals something
real: **Route-D v11's `v5_budget` genuinely misses its own Y0 budget by 62.02x at `a=0.45`**,
confirmed, not an artifact of the min/max selection bug alone. Reassuringly, the prose
(TECHNICAL/blog) already stated this non-uniformity honestly before the repair, so **no
written conclusion moves** — but the banked anchor JSON itself still carries the WRONG
margin (computed pre-repair) and needs regenerating. Drafted below, per the orchestrator's
request.

```
### 252 — ROUTE-VBRG: REGENERATE Route-D v11's BANKED ANCHOR JSON WITH LEG 247's CORRECTED
v5_budget MARGIN (leg 247's finding — the repair is correct, the ARTIFACT is now stale)
**Thesis.** Leg 247 correctly repaired the `v5_budget` min/max selection bug and confirmed
Route-D v11 genuinely misses its own Y0 budget by 62.02x at `a=0.45` — a real, now-corrected
number. The prose already stated this non-uniformity honestly, so no written conclusion needs
to change. But the banked anchor JSON (`experiments/p2_route_d_v11_anchor.py`'s own output
artifact) still carries the PRE-repair margin, computed before leg 247's fix — it is now
simply wrong, not merely imprecise, and needs regenerating from the repaired runner.
**Gate.** Does regenerating the banked anchor JSON from leg 247's repaired
`experiments/p2_route_d_v11_anchor.py` produce a margin at `a=0.45` matching leg 247's own
reported 62.02x-budget-miss finding, with every OTHER banked value in the JSON unchanged
(confirming leg 247's own 0/195-other-JSONs isolation finding extends to this regeneration,
not just the original diagnosis)?
  yes -> Bank the regenerated JSON. State explicitly that no prose conclusion changed (the
         non-uniformity was already stated honestly) — this closes leg 247's finding as a
         pure artifact-freshness fix, not a new correction to any written claim.
  no -> If regeneration produces a DIFFERENT margin than leg 247 itself reported, or if any
        other banked value in the JSON moves, escalate immediately — that would mean leg
        247's own repair or isolation claim doesn't reproduce from a fresh run.
**Territory.** the banked anchor JSON artifact `experiments/p2_route_d_v11_anchor.py`
               produces (regenerate, do not hand-edit), experiments/p2_route_vbrg_v1_regen.py,
               writeup/data/p2_route_vbrg_v1_regen.json,
               writeup/novelty/leg_252.md, experiments/journal/leg_252.md.
               Reads (never further edits) leg 247's own repaired code and report.
**Difficulty.** light
**Independence.** Regenerates one artifact from already-repaired code; does not re-touch leg
247's own repair logic. Disjoint from 236 (RDDEP, the dependency trace, which reads whichever
JSON is current — sequencing note: 236 should read the REGENERATED JSON once this leg lands,
not the stale one) and every other live/reserve leg. Immediately dispatchable, not blocked.
```

**Leg 250 (the PUB2 citation fix, drafted several updates ago) is confirmed still ready and
queued for the next vacancy**, per the orchestrator's own request — it was never dispatched,
sitting correctly in reserve since its own drafting.

**Live-slot roster, corrected:**

| Slot | Leg | Route | Floor status |
|---|---|---|---|
| A | 192 | H2CV | verify — not floor-eligible (superseded in practice by 249's recovery work, same underlying task) |
| B | 249 | H2CV2 | **live, newly promoted — TOP PRIORITY, submission-blocking for PUB2** |
| C | 248 | CNR2 | repair — not floor-eligible |
| D | 221 | BVRR | repair — not floor-eligible |
| E | 251 | P0T | **live, newly promoted — FLOOR-ELIGIBLE (math/construction), first leg of the new programme** |
| F | 236 | RDDEP | FLOOR-ELIGIBLE (math) |
| G | 245 | BCL2 | FLOOR-ELIGIBLE (literature) |
| H | 228 | BHRV | verify — not floor-eligible |
| I | 210 | M2SV | verify — not floor-eligible |
| J | 226 | PNR | repair — not floor-eligible |

**Floor status: 3/10 (251, 236, 245) — MET.** (246's landing removed it from the floor
count, but 251's promotion more than compensates — floor is comfortably met, no scramble
needed this round.)

**Reserve queue: 5 undispatched legs (229, 231-234), plus 250 and 252 (both newly drafted/
confirmed) = 7 undispatched legs (229, 231, 232, 233, 234, 250, 252).** 250 and 252 are both
immediately dispatchable, not blocked — ranked for the next vacancy ahead of the still-blocked
229/231-234.

Nothing in this update lifts a ban. Escalation #1 is now genuinely closed (the plan has a
`NEXT` stage). No claim about Walls 1 and 2 moves beyond what's already recorded in the
technical framing above; Clay stays ~0.05%. No direction question raised by this DM this
cycle.

---

## DM session-boundary recovery update, 2026-08-06 — post-handoff reconciliation: leg 251
re-confirmed for fresh dispatch (total loss, number reused), 192 retired as superseded,
210 parked for 252, new leg 253 (NRSX) drafted to hold the composition floor, full
ten-slot reassignment

**Context (from the orchestrator's direct git audit, taken as ground truth):** the prior
session's ten "live" slots were not all recoverable. Real committed progress exists for 221
(`leg/221-bvrr-v1`), 236 (`leg/236-rddep-v1`, novelty-pass only), 228 (`verify/228-bhrv-v1`,
novelty-pass only), 210 (`verify/210-m2sv-v1`, at/near baseline), 226 (`leg/226-pnr-v1`,
novelty-pass only — found the dispatch's prescribed fix does not work as specified, which its
gate explicitly authorizes). WIP-only salvage branches exist for 192
(`verify/192-h2cv-v1-wip`), 249 (`verify/249-h2cv2-v1-wip`), 248 (`leg/248-cnr2-v1-wip`).
Leg 245 (BCL2) landed (gate NO) before the boundary. **Leg 251 (P0T) is a total loss — no
branch, no worktree, nothing ever committed.**

### 1. Leg 251 (Route-P0T) — number REUSED, spec unchanged, dispatch fresh

No work was ever committed under 251, so the number is clean and is reused (retiring it
would create a phantom gap for no bookkeeping benefit — the withdrawn-191 precedent retired
a number because a *drafted premise* was stale; here the spec is fully current). **The full
spec at "### 251 — ROUTE-P0T" above stands verbatim as the dispatch text** — thesis, gate
(both branches), territory, difficulty all unchanged; nothing that happened at the session
boundary touches its premises. The fresh agent starts from scratch on `main`; there is no
prior work to recover and it must not go looking for any. It remains the single most
consequential leg in flight and dispatches at top priority alongside 249. The technical
framing (Tao's supercriticality barrier, corrected Wall 2, NRS/Tsai constraint, viscous-rung
sequencing) is in `CONTINUATION_PROMPT.md` Directive 1 — fold it into the brief as before.

### 2. Slot-by-slot rulings on the salvage questions

- **192 (H2CV): RETIRED, not resumed.** This DM's own prior roster already recorded it as
  "superseded in practice by 249's recovery work, same underlying task." Spending a slot on
  both would duplicate territory. The salvage branch `verify/192-h2cv-v1-wip` is preserved
  as INPUT to 249's brief (it contains the 871-line runner / 592-line JSON / journal that
  249 was dispatched to recover and verify). 192's number retires with its work absorbed;
  no rework leg needed.
- **249 (H2CV2): RESUME from salvage.** Top priority, submission-blocking for PUB2. Brief
  the fresh agent to recover BOTH salvage branches (`verify/249-h2cv2-v1-wip` and
  `verify/192-h2cv-v1-wip`), verify rather than trust the recovered artifacts, and land
  under 249's existing gate, unchanged.
- **248 (CNR2): RESUME from salvage.** The spec's premises (leg 237's finding, leg 226's
  fix shape) are intact; the WIP branch is a head start, not a liability. Same gate.
- **221/236/228/226: resume from their real branches** under their existing gates,
  unchanged. For 226 specifically: the novelty-pass finding that the prescribed fix fails
  as specified is WITHIN its gate's explicit authorization to find a different mechanism —
  the fresh agent continues under that clause, it is not an escalation.
- **210 (M2SV): PARKED back to reserve** (essentially zero independent progress; a verify
  of closed-stage-B-era work). Its slot goes to 252, which is light, fixes a banked
  artifact that is now known-WRONG (not merely stale), and unblocks 236's sequencing. 210
  redispatches at the next vacancy; its branch `verify/210-m2sv-v1` stays preserved.

### 3. New leg, drafted to hold the composition floor at 3/10

With 245/246 landed and 192 retired, only 251 (math/construction) and 236 (math) of the
live set are floor-eligible — 2/10, a §3b breach. 250 and 252 are fix/regen legs, not
floor-eligible. None of the blocked reserve (229, 231-234) qualifies or is dispatchable.
So one fresh floor-eligible leg is drafted now, chosen to be load-bearing for Phase 0
without overlapping 251's territory:

```
### 253 — ROUTE-NRSX: PIN THE NRS/TSAI EXCLUSION'S EXACT HYPOTHESIS BOUNDARY, AND SWEEP FOR
LATER STRENGTHENINGS THAT SHRINK THE SURVIVOR SPACE (literature — floor-eligible)
**Thesis.** Leg 251's entire screen rests on the NRS/Tsai exclusion of nontrivial
exactly-backward-self-similar 3D NS blow-up "under the relevant decay." The precise
hypothesis set (Nečas-Růžička-Šverák's L³ condition; Tsai's local-energy/decay variants)
determines exactly which candidate classes survive — and any LATER published strengthening
(e.g. discretely-self-similar exclusions, Chae-Tsai-type extensions, weaker-decay variants)
would SHRINK the survivor space 251 assumes. 251 applies the screen; this leg adversarially
pins the screen itself, at full text, and hunts forward citations for strengthenings. A
strengthening found AFTER 251 names its candidate could kill the candidate late; found now,
it costs one literature leg.
**Gate.** Does the full-text hypothesis set of NRS + Tsai, plus a forward-citation sweep for
published strengthenings, leave the survivor classes named in 251's thesis (discretely
self-similar; unstable-self-similar with finite unstable spectrum; non-self-similar) intact
as genuinely not-excluded?
  yes -> Bank the pinned hypothesis boundary as a checked input to Phase 0/1, with verbatim
         locators for each hypothesis and each surveyed strengthening. 251's screen stands
         on read-and-verified footing rather than folklore.
  no -> Name precisely which survivor class a published result excludes, with the locator.
        ESCALATE — this directly narrows or redirects 251's/Phase 1's candidate space and
        must reach 251's agent (or its successor) before a candidate is banked.
**Territory.** experiments/p2_route_nrsx_v1_screenbounds.py,
               writeup/data/p2_route_nrsx_v1_screenbounds.json,
               writeup/novelty/leg_253.md, experiments/journal/leg_253.md.
               Reads (never edits) the same NRS/Tsai citations 251 reads — read-only
               overlap, zero written-territory overlap with 251 or anything else live.
**Difficulty.** standard
**Independence.** Pure literature; edits no solver module, no shared ledger. Independent of
all nine other slots (informs 251 but neither blocks nor is blocked by it — if both land,
the orchestrator cross-checks their readings, which is a feature). Immediately dispatchable.
```

**Next fresh leg number for any future candidate is 254.** (Git history's highest is 249,
but 250-253 are assigned in this file; 191 stays retired; 192 retires per §2 above.)

### 4. The ten slots, assigned for immediate dispatch

| Slot | Leg | Route | Start from | Floor status |
|---|---|---|---|---|
| A | 250 | PUB2FIX | fresh (spec above) | fix — not floor-eligible; SUBMISSION-BLOCKING |
| B | 249 | H2CV2 | `verify/249-h2cv2-v1-wip` + recover `verify/192-h2cv-v1-wip` | verify — TOP PRIORITY, submission-blocking |
| C | 248 | CNR2 | `leg/248-cnr2-v1-wip` | repair — not floor-eligible |
| D | 221 | BVRR | `leg/221-bvrr-v1` (landing candidate) | repair — not floor-eligible |
| E | 251 | P0T | fresh — total loss, nothing to recover | **FLOOR-ELIGIBLE (math/construction); most consequential leg in flight** |
| F | 236 | RDDEP | `leg/236-rddep-v1` | FLOOR-ELIGIBLE (math) |
| G | 253 | NRSX | fresh (spec above) | **FLOOR-ELIGIBLE (literature)** |
| H | 228 | BHRV | `verify/228-bhrv-v1` | verify — not floor-eligible |
| I | 252 | VBRG | fresh (spec above) | regen — not floor-eligible; light, unblocks 236's read |
| J | 226 | PNR | `leg/226-pnr-v1` | repair — not floor-eligible |

**Floor status: 3/10 (251, 236, 253) — MET.**

### 5. Territory / sequencing flags for the orchestrator, resolved before dispatch

- **248 vs 226:** different modules (`collocation_newton.py` vs `profile_newton.py`),
  disjoint per 248's own spec — confirmed, no conflict. 248 also stays clear of leg 150's
  earlier unrelated repair to its module, per its own territory clause.
- **252 vs 236:** 252 regenerates the Route-D v11 anchor JSON that 236 reads. **Dispatch
  252 before (or simultaneously with) 236's resume, and brief 236's fresh agent explicitly:
  the currently-banked anchor margin at `a=0.45` is WRONG (pre-repair); read the
  regenerated JSON once 252 lands, or use leg 247's reported 62.02x figure in the interim,
  never the stale banked value.**
- **249 vs 250:** disjoint (249 verifies the number, 250 reconciles a different number's
  citation); 250's own sequencing note stands — it can start immediately on the
  bound-vs-measurement question, folding "independently verified" in only if 249 lands
  first.
- **249 vs 192:** resolved by retiring 192 (§2); no two slots share that territory.
- **253 vs 251:** read-only overlap on the same citations, zero written overlap — by
  design.

**Canonical reserve line: reserve count 6 — legs 210, 229, 231, 232, 233, 234.** Of these,
only 210 is immediately dispatchable (parked verify, branch preserved); 229 stays blocked
on 226, and 231-234 stay blocked on repairs 217/219/221/225, none of which has landed on
`main` (re-confirmed by direct git check this update). Count 6 is above the §3a watermark
of 3, but this DM flags, continuing the prior update's honesty on this point: **effective
immediately-dispatchable reserve is 1.** If two slots free before the blocked pool clears,
this DM will draft fresh unblocked candidates at that moment rather than let a slot idle —
and if the composition floor breaches again two cycles after `P0` lands, the §5 commitment
above (report the roster problem, stop papering) is still in force.

Nothing in this update lifts a ban, changes any gate already committed, or moves any claim
about Walls 1 and 2; Clay stays ~0.05%. Escalations: none new; #1 remains closed; leg 247's
escalated finding is being closed by 252's dispatch. No direction question raised — the
orchestrator's five requests were all answerable under the standing ruling.

---

## DM revision, 2026-08-07 — user steer applied (verbatim forward, ORCHESTRATION.md §3):
DSS scoping prioritized AHEAD of P0's dispatch, Phase 1 authorized in parallel, legs
254-257 drafted, 258 (floor lock) specified as a bench task, full ten-slot reassignment.
SUPERSEDES the previous update's slot table — nothing from it was dispatched.

**The steer, restated in one paragraph so this file carries it:** the DSS-ban scoping leg
this DM drafted conditionally in the ban review is now user-prioritized, and must settle
BEFORE P0 (leg 251) dispatches — because discretely-self-similar is one of the few ansatz
classes surviving the NRS/Tsai screen, and P0 must not run its screen with a survivor
banned by a clause that never argued against it. Phase 1 is authorized to start NOW, in
parallel with P0 (they ask different questions; do not serialize). Phase 1's target, in
this repository's own measured language: leg 174's occupancy matrix has exactly one empty
cell (`fluid_adjacent=True, grade=A`) — move the viscous term from DOMINATED to ENCLOSED
for a fluid self-similar object (leg 240's words). Reachability evidence: Breden-Chu's own
Remark 40 (arXiv:2404.04054) states `(u·∇)u` is reachable in d ∈ {2,3}, yet their frontier
is still 1D after 7 subsequent papers (leg 245). The stage-V ban must be ENGAGED, not
skirted: Breden-Chu's weighted Sobolev setting is precisely the "namable fourth space" the
re-posed ban's lift clause demands, and connecting the two via a scoping leg is a
prerequisite to any Phase-1 construction. Three legs ordered (P1a census, P1b reproduction,
P1c reach), all floor-eligible; do not rebuild what capabilities.py already lists; check
why 236 is slow; lock the composition floor into code while it is met. Unchanged: the
three-tier win condition, lesson 91, pre-committed gates, and the no-claimed-movement rule.

### The four new legs

```
### 254 — ROUTE-DSSX: IS THE DSS EXPENSIVE ENTRANCE'S EXCLUSION COST-SHAPED OR SUBSTANTIVE?
(THE BAN-REVIEW SCOPING LEG, NOW USER-PRIORITIZED — dispatches BEFORE leg 251)
[FLOOR-ADJACENT: scoping from the repository's own research record — counted OUTSIDE the
floor tally below, conservatively]
**Thesis.** The DSS ban's "never" covers both the cheap entrances and "the DSS lane's
expensive entrance," but the three recorded reasons argue only against the cheap entrances
(ban review, above). Under the old cost-sensitive goal that distinction did not matter;
under the Clay goal with heavy engineering explicitly authorized, it does. This leg reads
the DSS lane's OWN history in this repository (the legs/reports that produced the ban, not
the plan's printed one-liner) and determines what the expensive entrance actually IS and
why it was excluded.
**Gate.** Reading the DSS lane's own underlying record at full depth: was the expensive
entrance excluded for a SUBSTANTIVE reason independent of cost (a measured failure, a
structural obstruction), or only by cost/scope under the old goal?
  yes (substantive) -> Name the reason with locators. The ban stands as written; record
        explicitly that P0 must treat the DSS lane's expensive entrance as excluded by this
        repository's own measurement, not by budget. No escalation needed.
  no (cost-shaped) -> Draft a proposed re-posed ban wording that keeps the cheap entrances
        banned by their three reasons while opening the expensive entrance under the Clay
        goal, and ESCALATE to the user for the actual lift — this leg's authority ends at
        the recommendation; no ban lifts under a leg's own signature.
**Territory.** writeup/novelty/leg_254.md, experiments/journal/leg_254.md,
               writeup/data/p2_route_dssx_v1_scoping.json (a locator ledger, no compute).
               Reads (never edits) the DSS lane's own historical reports/JSONs and
               plan_of_record.py's ban text.
**Difficulty.** light
**Independence.** Pure repository-record read. Blocks leg 251's dispatch BY USER PRIORITY
(251 redispatches at the first vacancy after 254 lands, with 254's finding folded into its
brief). Touches nothing any other slot writes. Immediately dispatchable, top of queue.
```

```
### 255 — ROUTE-P1A: PHASE 1 TARGET CENSUS — DISSIPATIVE BLOW-UP MODELS WITH AN
UNCERTIFIED SELF-SIMILAR/DSS PROFILE INSIDE BREDEN-CHU's STATED REACH
[FLOOR-ELIGIBLE: math/literature]
**Thesis.** Phase 1's goal (user authorization, this update): move the viscous term from
DOMINATED to ENCLOSED for a fluid self-similar object — leg 174's one empty matrix cell.
First question: WHICH models qualify? The census must satisfy all four screens jointly:
(i) proved or strongly-supported DISSIPATIVE finite-time blow-up, (ii) a self-similar or
DSS profile, (iii) no existing certificate (screened against leg 174's matrix,
capabilities.py, and this repository's own precedent sweeps 240/242/245/246), (iv) a
nonlinearity inside Breden-Chu's stated reach (Remark 40's own terms). TECHNICAL CAUTION,
built into the gate per the user's own wording: viscous Burgers is Breden-Chu's home
ground and DOES NOT blow up — "parabolic and certifiable" is not "blows up"; screens (i)
and (iv) are independent and BOTH must pass. Grep capabilities.py before building
anything: fractional_gclm.py, critical_dissipation.py, interval.py, nk_bounds.py,
interval_certificate.py, and leg 61's Kawahara reproduction already exist.
**Gate.** Does at least one model pass all four screens jointly, with each screen's verdict
carried per-candidate in a banked table (including the failures, with which screen killed
each)?
  yes -> Bank the census table; name the surviving candidate(s) precisely, with locators
         for (i) and (iv). These are Phase 1 construction's candidate pool — construction
         itself stays gated behind P1c's ban-lift scoping, not authorized here.
  no -> Bank the full kill table. This would mean Phase 1's target cell cannot be filled
        from any known model — report which screen does most of the killing, as direct
        input to whether Phase 1 needs a weaker screen (i) tier or a different technique.
**Territory.** experiments/p2_route_p1a_v1_census.py,
               writeup/data/p2_route_p1a_v1_census.json,
               writeup/novelty/leg_255.md, experiments/journal/leg_255.md.
               Reads (never edits) leg 174's matrix, capabilities.py, legs 240/242/245/246.
**Difficulty.** standard
**Independence.** Own module, reads-only overlap with 251/253's citation pool. Does not
wait on 254 (the census RECORDS DSS-profile candidates regardless; whether the DSS lane's
expensive entrance is in scope is 254's/the user's call, noted per-row, not decided here).
Immediately dispatchable.
```

```
### 256 — ROUTE-P1B: REPRODUCE ONE PUBLISHED BREDEN-CHU RESULT END TO END, ON ITS OWN
GROUND (the leg-61 Kawahara shape, applied to the Grade-A technique)
[FLOOR-ELIGIBLE: construction/reproduction]
**Thesis.** Before any Phase-1 construction is even posable, the cheapest kill test: can
this repository drive Breden-Chu's machinery AT ALL, on a result they already published?
Exact shape of leg 61's Kawahara reproduction of Cadiot-Lessard-Nave. If it fails, Phase 1
dies early and cheaply — which is the point of running it before construction. BAN
DISCIPLINE, stated up front: this leg operates ENTIRELY within Breden-Chu's own published
weighted-Sobolev setting — the namable FOURTH space the re-posed stage-V ban's lift clause
demands — and touches none of the three dead realizations (ℓ¹_w coefficient basis,
collocation basis, origin-H²). Together with P1c it CONSTITUTES the ban's own scoping
route; it does not lift the ban, and no construction on any Phase-1 target runs under this
leg's authority.
**Gate.** Does an end-to-end reproduction of one published Breden-Chu certificate (chosen
by the leg from arXiv:2404.04054's own results, stated before running) reproduce their
published enclosure/existence verdict, with the leg's own independently-computed bounds
landing inside (or explicably tighter/looser than) theirs?
  yes -> Bank the reproduction as leg 61-grade evidence the machinery is usable here.
         Phase-1 construction remains gated on P1c + the user's ban ruling.
  no -> Report exactly which stage fails (setup, bounds, verification) and whether the
        failure is ours (implementation) or theirs (a published gap — escalate immediately
        if so; that would be a finding at full strength).
**Territory.** experiments/p2_route_p1b_v1_bcrepro.py, solver/bc_weighted_sobolev.py (NEW
               module — the fourth space gets its own file, touching no existing solver
               module), writeup/data/p2_route_p1b_v1_bcrepro.json,
               writeup/novelty/leg_256.md, experiments/journal/leg_256.md.
               Reads (never edits) interval.py, nk_bounds.py, leg 61's reproduction.
**Difficulty.** heavy
**Independence.** New module; zero written overlap with any live slot. Reads-only overlap
with P1c on the same paper — by design, their readings cross-check. Immediately
dispatchable.
```

```
### 257 — ROUTE-P1C: REMARK 40's REACH, MEASURED NOT ARGUED — AND THE STAGE-V BAN-LIFT
SCOPING, FOLDED IN HERE (this DM's call, per the user's "your call")
[FLOOR-ELIGIBLE: math/literature]
**Thesis.** Remark 40 is the authors' claim; this leg establishes what it actually costs.
Full-text read plus scoping computation, NO construction: which Breden-Chu hypotheses bind
on a fluid nonlinearity, what the weighted-Sobolev setup demands in 2D/3D, and where their
own "non-trivial ... future work" flag actually bites. FOLDED IN, as the designated
stage-V ban-lift scoping (this DM's call between P1b and here — here, because
establishing distinctness is a hypothesis-level question, not a reproduction-level one):
establish whether the weighted-Sobolev setting is genuinely NOT subject to the same
three-realization death (ℓ¹_w coefficient: leg 54's Z₁ block-coupling; collocation: leg
56's (H,D) consistency defect; origin-H²: legs 163/176's a=0 cap) — mechanism by
mechanism, named per lesson 91, not by analogy.
**Gate.** Two clauses, both required for yes: (a) does the full-text read yield a concrete,
banked account of what a 2D/3D fluid application demands (hypotheses that bind, setup
cost, where "future work" bites)? (b) does the weighted-Sobolev setting demonstrably evade
EACH of the three dead realizations' named death mechanisms?
  yes -> Bank both. ESCALATE to the user with the ban's lift clause satisfied on paper:
         a namable fourth space, with its own scoping leg establishing non-subjection.
         The lift itself is the user's signature, not this leg's.
  no -> Name which clause fails and which mechanism transfers (if (b)): a death mechanism
        that follows the machinery into the fourth space would close Phase 1's Breden-Chu
        route before construction spent anything — report at full strength; that is this
        leg working, not failing.
**Territory.** experiments/p2_route_p1c_v1_reach.py,
               writeup/data/p2_route_p1c_v1_reach.json,
               writeup/novelty/leg_257.md, experiments/journal/leg_257.md.
               Reads (never edits) arXiv:2404.04054 full text, legs 54/56/163/176's death
               reports, leg 245's locators.
**Difficulty.** standard-to-heavy
**Independence.** Reads-only overlap with P1b (same paper, cross-check by design) and the
dead-realization reports. No written overlap with anything live. Immediately dispatchable.
```

```
### 258 — ROUTE-FLOCK: LOCK THE COMPOSITION FLOOR INTO test_plan_of_record.py / THE MERGE
GATE (BENCH TASK — this DM's call on the orchestrator's offered choice: run this as a
MECHANICAL BENCH DISPATCH, not one of the ten research slots)
**Thesis.** The floor is met (3/10) for the first time; encode it now, while satisfied,
per the user's point 8 — "a floor that is breached invites an exception." Pure
test-writing: a check that DIRECTION.md's live-slot table (or an equivalent
machine-readable roster line) carries >= 3 floor-eligible legs.
**Gate.** Does the new test (a) FAIL when run against a roster with 2/10 floor-eligible
legs (verified by a deliberate fixture, not by editing the real roster), and (b) PASS
against the current roster, and (c) run inside the existing merge gate without touching
any other test's behavior?
  yes -> Land it. The floor is now code.
  no -> Report which clause fails; do not weaken an existing test to force the pass.
**Territory.** test_plan_of_record.py (additive only) or the merge-gate script (additive
               only), a machine-readable roster marker in DIRECTION.md if needed (the DM
               will maintain it thereafter), experiments/journal/leg_258.md.
**Difficulty.** light/mechanical
**Independence.** Test-only. Orchestrator dispatches at its own convenience as a bench
task; it does not consume a research slot and is excluded from the floor tally itself.
```

**Next fresh leg number for any future candidate is 259.**

### The ten slots, revised — SUPERSEDES the previous table; nothing had been dispatched

| Slot | Leg | Route | Start from | Floor status |
|---|---|---|---|---|
| A | 250 | PUB2FIX | fresh (spec above) | fix — SUBMISSION-BLOCKING |
| B | 249 | H2CV2 | `verify/249-h2cv2-v1-wip` + recover `verify/192-h2cv-v1-wip` | verify — TOP PRIORITY, submission-blocking |
| C | 254 | DSSX | fresh — USER-PRIORITIZED, dispatches before 251 | scoping (counted outside floor, conservatively) |
| D | 221 | BVRR | `leg/221-bvrr-v1` (landing candidate) | repair |
| E | 255 | P1A | fresh | **FLOOR-ELIGIBLE (math/literature)** |
| F | 236 | RDDEP | `leg/236-rddep-v1` | FLOOR-ELIGIBLE (math) |
| G | 256 | P1B | fresh | **FLOOR-ELIGIBLE (construction)** |
| H | 257 | P1C | fresh | **FLOOR-ELIGIBLE (math/literature)** |
| I | 252 | VBRG | fresh — light, unblocks 236's read | regen |
| J | 226 | PNR | `leg/226-pnr-v1` | repair |

**Floor status: 4/10 strictly (255, 256, 257, 236) — MET with margin; 254 arguably a
fifth.** Leg 258 (FLOCK) runs as a bench task alongside, encoding the floor while it holds.

**Displaced from the previous (never-dispatched) table:** 251 (P0T — now blocked on 254 BY
USER PRIORITY; redispatches at the first vacancy after 254 lands, spec unchanged, 254's
finding folded into its brief); 253 (NRSX — still fully specified and valuable, first-in-line
among ordinary reserve); 248 (CNR2 — WIP branch `leg/248-cnr2-v1-wip` preserved, resume at
next vacancy); 228 (BHRV — branch preserved); 210 (M2SV — stays parked).

**Answering the user's point 8 on leg 236 (RDDEP)'s slowness, from the orchestrator's own
ground truth:** it was mid-flight (novelty-pass committed, no construction) when the prior
session ended by external interruption/graceful handoff — nothing in the work itself
stalled it. Its fresh agent resumes from `leg/236-rddep-v1` with an updated brief: it now
carries TWO Route-D v11 exposures (post-235), and it must read the REGENERATED anchor JSON
once 252 lands (interim: leg 247's reported 62.02x, never the stale banked value).

**Sequencing and ban discipline, restated as dispatch instructions:**
- 254 dispatches immediately; 251 does NOT dispatch until 254 lands (user priority #1).
- P1a/P1b/P1c dispatch now, in parallel with each other and with everything else. NO
  Phase-1 CONSTRUCTION leg exists or dispatches until P1c reports AND the user rules on
  the stage-V lift — the ban is engaged through its own clause, not skirted; nothing in
  this update lifts it.
- All three P1 briefs carry the do-not-rebuild instruction verbatim (point 7): grep
  capabilities.py first; fractional_gclm.py, critical_dissipation.py, interval.py,
  nk_bounds.py, interval_certificate.py, leg 61's Kawahara reproduction exist.
- 252 before/with 236's resume, as before.

**Canonical reserve line: reserve count 10 — legs 251, 253, 248, 228, 210, 229, 231, 232,
233, 234.** Effective immediately-dispatchable: 4 (253, 248, 228, 210); 251 blocked on 254
by user priority (expected to clear fast — 254 is light); 229 blocked on 226; 231-234
blocked on repairs 217/219/221/225 (none landed on `main`). Count 10 is well above the §3a
watermark.

Nothing in this update lifts a ban (254 and 257 each terminate in a recommendation/
escalation, never a lift under leg authority), changes any already-committed gate, or moves
any claim about Walls 1 and 2; Clay stays ~0.05%. The no-claimed-movement rule is restated
in every P1 leg's own gate language, per the user's point 9 — a Clay-directed programme is
where it erodes most easily, so it is written into the legs, not just remembered. No
direction question raised: the steer was explicit enough to act on directly, and the one
delegated choice (where the ban-lift scoping folds) is decided above (P1c) with the reason
recorded.

---

## DM refill, same cycle — leg 250 LANDED (71cde44, audited clean, §7b verifier in
flight), 253 (NRSX) promoted into slot A

**250 (PUB2FIX) landed, and the finding is better than the leg's own thesis anticipated:**
the σ_min "conflict" was an INVERTED INEQUALITY, not a 7.9× measurement error —
`0.71465 = 1/1.3993` (leg 163's own largest sampled ratio) bounds σ_min only from ABOVE,
so leg 163's data support `σ_min ≤ 0.71465`, fully consistent with leg 176's measured
`0.0908`. Recorded at full strength alongside it: NEITHER leg proves a LOWER bound on
σ_min, and PUB2's "bounded away from zero" framing is now corrected accordingly. This is
claim-bearing on a submission-track document, so the orchestrator's §7b post-landing
verifier is correctly in flight; if that verifier confirms a gap, a rework leg gets cut at
the top of the queue per the standing contract — nothing to pre-draft until it reports.

**Slot A: leg 253 (Route-NRSX) promoted, per its own first-in-line ranking** — no
re-ranking needed, and the reasons have only strengthened since it was drafted: it
adversarially pins the NRS/Tsai hypothesis boundary that leg 251's screen (dispatching
after 254), leg 255's census screen (iii)/(ii) reasoning, and the DSS-survivor argument in
the user's own steer all lean on. Spec above stands verbatim; immediately dispatchable.

| Slot | Leg | Route | Change |
|---|---|---|---|
| A | 253 | NRSX | **promoted this update** — FLOOR-ELIGIBLE (literature) |
| B-J | — | — | unchanged from the revised table above |

**Floor status: 5/10 strictly (253, 255, 256, 257, 236) — comfortably met**; 254 still
counted conservatively outside.

**Canonical reserve line: reserve count 9 — legs 251, 248, 228, 210, 229, 231, 232, 233,
234.** Effective immediately-dispatchable: 3 (248, 228, 210); 251 blocked on 254 by user
priority (254 is light — expected to clear soon, and 251 is pre-committed as its
successor at the next vacancy after it lands); 229 blocked on 226; 231-234 blocked on
repairs 217/219/221/225. Count 9 is above the §3a watermark of 3, so no forced 8-leg
draft triggers — but this DM notes the effective-dispatchable number (3) sits exactly at
the watermark's spirit, and commits to drafting fresh unblocked candidates in the SAME
update that next promotes any of 248/228/210, rather than waiting for the count to breach.

Nothing in this update lifts a ban, changes any committed gate, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised.

---

## DM sync, 2026-08-07 — leg 258 (FLOCK) landed (00f7e06); its FLOOR-TABLE snapshot was
stale on arrival and is now corrected to the dispatched roster

**258 landed as specified** (marker block + two tests, test_10 proving the assertion fails
on a 2/10 fixture — the gate's own honesty clause held). But its snapshot was taken from
the PRE-steer prose table (E/251/P0T, G/245/BCL2 — a roster that was superseded before any
of it dispatched, and 245 had already landed). **The FLOOR-TABLE block at the top of this
file is now synced to the actual dispatched roster** (A/253, B/249, C/254, D/221, E/255,
F/236, G/256, H/257, I/252, J/226 — 5/10 eligible, 254 conservatively "no").
**Ownership recorded: this DM maintains the FLOOR-TABLE block from here on, in the same
edit as any roster-changing update** — exactly as the §3a reserve-line discipline already
works, and per the marker's own comment. The orchestrator does not need to touch it.

Nothing else changes: slots, reserve line (count 9), floor status, and all sequencing
notes stand as in the two updates above.

---

## DM update, 2026-08-07 — slot-C refill: 251 (P0T) DISPATCHES NOW with a conditional-tier
instruction; 254's escalated finding recorded; 250's verifier clean, DOCS nits queued as
leg 259; a standing brief clause against mid-leg pausing

**254 (DSSX) finished and escalated** (branch `leg/254-dssx-v1`, PR #18, slot vacated per
§4a): **the DSS lane's expensive entrance is COST-SHAPED, not substantive** — excluded
under the old cost-sensitive goal, with no measured failure of its own. The proposed ban
re-posing is with the user in NEEDS-YOU; no ban moves until that ruling.

**Slot C: leg 251 (Route-P0T) promoted — dispatch now, not after the ruling.** Reasoning
recorded: the user's prioritization ("settle the ban first") was aimed at a specific
failure mode — P0 screening candidates with one of the few NRS/Tsai survivors banned by a
clause that never argued against it. 254's finding settles the SUBSTANCE: the exclusion is
cost-shaped, so 251 no longer risks wrongly treating DSS-expensive as measured-dead. The
only thing outstanding is the ruling itself, and 251 can respect it without waiting:
**brief addition (mandatory): 251 evaluates DSS-lane candidates on their merits under the
NRS/Tsai + dead-end screens, but any candidate whose viability depends on the DSS
expensive entrance goes in a separate, explicitly-marked CONDITIONAL tier — reportable,
not bankable as THE Phase-1 candidate until the user's ruling lands. If the ruling arrives
mid-leg, the orchestrator forwards it and the tier resolves accordingly.** 254's full
finding (and its locators) folds into 251's brief alongside CONTINUATION_PROMPT.md
Directive 1, as originally specified. This dispatches the plan's own NEXT stage; waiting
would idle the single most consequential leg on a formality whose substance is already
settled — the standing answer ("best for the overall goal") decides this without the user.

**250's §7b verifier confirmed no gap** (landed `600055b`) — the inverted-inequality fix
stands. Two DOCS-level prose-precision nits (no banked number wrong, no urgency), queued
so they are not lost rather than interrupting anything:

```
### 259 — ROUTE-PUB2P: PUB2 PROSE-PRECISION PASS (two nits from leg 250's §7b verifier —
DOCS-only, light, low priority)
**Thesis.** Leg 250's verifier confirmed the fix clean but surfaced two prose-precision
residues in TECHNICAL_P2_PUB2_V1.md: (a) §3.5 states `0.71465 = 1/1.3993` as "exactly"
when it is a round-up by 7.0e-06 (§3.2 already discloses this correctly; §3.5 does not);
(b) the table cell at line 175 (§3.1 — outside leg 250's three declared gate sites) still
presents "σ_min bounded away from zero" as a verified conjunct, which §3.5 now correctly
withdraws as unproven.
**Gate.** After the pass, do §3.5's exactness wording and §3.1's table cell both match
§3.5's own corrected epistemic status (upper bounds only, no proven floor, rounding
disclosed), with no other sentence's meaning changed?
  yes -> Bank; PUB2 is internally consistent on this point at every site, not just the
         three leg 250 declared.
  no -> Report which site resists; escalate rather than guess (same clause as 250's).
**Territory.** writeup/4_p2_lottery/TECHNICAL_P2_PUB2_V1.md (the two named sites ONLY),
               writeup/novelty/leg_259.md, experiments/journal/leg_259.md.
**Difficulty.** light
**Independence.** DOCS-only; disjoint from 249 (which verifies the number itself).
Dispatchable at any vacancy; LOW priority — behind 248/228/210 in the reserve order.
```

**Standing brief clause, adopted from the orchestrator's observation (236 and 226 pausing
mid-computation for interim reports): every future dispatch brief carries — "Run to your
gate answer in one pass. Interim reports are for escalation-worthy findings only; a
progress update is not one."** Recorded here so it applies to all future briefs without
per-leg drafting.

**FLOOR-TABLE block updated in this same edit** (C: 254 → 251). **Floor status: 6/10
strictly (253, 251, 255, 236, 256, 257) — comfortably met.**

**Canonical reserve line: reserve count 9 — legs 248, 228, 210, 259, 229, 231, 232, 233,
234.** Effective immediately-dispatchable: 4 (248, 228, 210, 259 — in that priority
order); 229 blocked on 226; 231-234 blocked on repairs 217/219/221/225. Above the §3a
watermark; the pre-committed refill trigger (draft fresh candidates in the same update
that next promotes any of 248/228/210) stands.

Nothing in this update lifts a ban — 254's re-posing sits with the user, and 251's
conditional tier exists precisely so the leg cannot pre-empt that ruling. No committed
gate changes; no claim about Walls 1 and 2 moves; Clay stays ~0.05%. Next fresh leg
number: 260. No direction question raised.

---

## DM update, 2026-08-07 — USER RULING APPLIED: leg 254 merged, DSS ban split (Entry A
cheap/banned, Entry B expensive/liftable-by-scoping); 251's conditional tier re-anchored;
Entry B's named scoping leg drafted as 260; anti-pausing clause hardened

**The user ruled directly ("Let's get leg 254 merged") and the orchestrator applied it**
(commit `47f76eb`, all 10 invariants pass, merge gate green, 254's artifacts merged
alongside): the DSS ban is now **Entry A** (cheap entrances — bifurcation off a fixed
point — banned "never," unchanged in substance) and **Entry B** (the expensive entrance —
a global unseeded periodic-orbit search — re-posed to "never — unless a scoping leg
answers the function space, the object, and the price"). **254's escalation is RESOLVED
and removed from pending tracking; nothing else sits in NEEDS-YOU from this DM's queue.**
The ban change was made BY THE USER's ruling, not by any leg or by this DM — recorded for
the honesty ledger.

**Leg 251 (in flight): its CONDITIONAL tier re-anchors.** DSS-expensive-dependent
candidates are no longer "blocked on the user" but **"blocked on Entry B's own scoping
leg"** — a liftable, work-shaped condition. The orchestrator has forwarded the ruling to
251's agent. 251 still cannot bank a DSS-expensive candidate as THE Phase-1 candidate
until Entry B's scoping leg answers — that is now the ban's own text, not a DM overlay.

**Entry B's scoping leg, drafted now (this DM's call: cheap insurance — if 251's screen
surfaces a DSS-conditional candidate, the lift path is ready instead of a round-trip):**

```
### 260 — ROUTE-DSSB: ENTRY B's OWN SCOPING LEG — THE FUNCTION SPACE, THE OBJECT, AND THE
PRICE OF THE DSS EXPENSIVE ENTRANCE (the lift condition's three named questions, answered
as a scoping, not a construction)
[Counted OUTSIDE the floor tally, conservatively, same as 254 — scoping, not construction]
**Thesis.** Entry B's re-posed wording (user ruling via leg 254, commit 47f76eb) makes the
DSS expensive entrance liftable by exactly one thing: a scoping leg answering (1) what
FUNCTION SPACE a global unseeded periodic-orbit search would run in, (2) what OBJECT it
would target, and (3) what the PRICE actually is (compute, machinery to build, and which
existing capabilities.py modules carry part of it). This leg answers those three, from leg
254's own locators plus the DSS lane's historical record — it builds nothing and runs no
search.
**Gate.** Can all three questions be answered concretely — a named function space, a named
object, a costed price (including what exists vs. what must be built) — such that the
answer is actionable by a hypothetical construction leg without further scoping?
  yes -> Bank the three answers with locators. ESCALATE to the user with Entry B's lift
         condition satisfied on paper — the lift itself is the user's signature, exactly
         as P1c's gate is worded for the stage-V ban. If 251 has a DSS-conditional
         candidate by then, name the connection explicitly.
  no -> Name which of the three resists a concrete answer and why — an unanswerable
        price/space/object question is itself the measured reason Entry B stays shut, and
        upgrades the ban's basis from cost-shaped to substantive. Report at full strength.
**Territory.** experiments/p2_route_dssb_v1_scoping.py,
               writeup/data/p2_route_dssb_v1_scoping.json,
               writeup/novelty/leg_260.md, experiments/journal/leg_260.md.
               Reads (never edits) leg 254's merged report/JSON, the DSS lane's historical
               reports, capabilities.py.
**Difficulty.** standard
**Independence.** Reads-only; no written overlap with any live slot. NOT urgent — nothing
is currently blocked purely on its absence (251 reports DSS candidates as conditional
either way). Reserve priority: behind 248/228/210, ahead of 259 — UNLESS 251 lands with a
DSS-conditional candidate in its yes-branch, in which case 260 promotes to the next
vacancy immediately, pre-committed here so no re-ranking decision is needed at that
moment.
```

**Anti-pausing clause, hardened (fourth occurrence — 236, 226, 252, and 221, the last
dispatched before the clause existed):** every future brief carries, verbatim: **"Run to
your gate answer in one continuous pass. Nothing wakes you if you stop mid-computation —
there is no monitor, no background job, no resumption. A stopped leg is a stalled leg
until a human notices."** The orchestrator's per-agent nudges cover pre-clause dispatches;
this wording covers everything from here on.

**Roster unchanged** (ten slots as in the slot-C refill update; FLOOR-TABLE block
untouched, still 6/10). **Canonical reserve line: reserve count 10 — legs 248, 228, 210,
260, 259, 229, 231, 232, 233, 234.** Effective immediately-dispatchable: 5 (248, 228,
210, 260, 259 — in that priority order, with 260's pre-committed promotion trigger noted
above); 229 blocked on 226; 231-234 blocked on repairs 217/219/221/225. Next fresh leg
number: **261.**

Nothing in this update lifts a ban (the user lifted/re-posed Entry B; this DM only
records it), changes any committed gate, or moves any claim about Walls 1 and 2; Clay
stays ~0.05%. No direction question raised.

---

## DM update, 2026-08-07 — slot-E refill: 255 (P1A) LANDED AND VERIFIED (2 survivors,
both non-fluid; the fluid-adjacent candidate killed on a Leray-projection screen); 248
(CNR2) promoted per the pre-committed order; fresh candidate 261 drafted per the trigger

**255 (P1A) landed clean and was independently §7b-verified** (`891ebaf`, `72258f0`).
Finding, recorded at full strength: the four-screen census yields **2 survivors, both
NON-fluid; the single fluid-adjacent candidate was killed on a Leray-projection screen.**
If that kill stands, leg 174's empty target cell (`fluid_adjacent=True, grade=A`) has no
reachable occupant among known models under the census's evidence tier — which would be
the most consequential negative Phase 1 could produce. **This DM deliberately does NOT
redirect Phase 1 on it yet**: 257 (P1C) is independently scoping the same question with
255's finding forwarded, and may confirm or contest both the kill and the survivor list.
The right moment to re-pose Phase 1 (if needed) is when 257 lands — one leg's read is not
a programme redirect, per the same discipline that keeps one measurement from moving a
banked claim.

**Slot E: leg 248 (Route-CNR2) promoted, per the pre-committed reserve order** — no gate
answer changed 248's ranking. Resume from `leg/248-cnr2-v1-wip`; spec and gate unchanged;
brief carries the hardened anti-pausing clause verbatim.

**Pre-committed trigger fired (fresh drafting in the same update that promotes any of
248/228/210):**

```
### 261 — ROUTE-P1A2: THE FLUID CENSUS UNDER A RELAXED EVIDENCE TIER (Phase 1's fallback
question, drafted BEFORE it is needed — dispatchable only after 257 lands)
[FLOOR-ELIGIBLE: literature]
**Thesis.** 255's census required proved-or-strongly-supported dissipative blow-up
(screen (i)) and found the fluid cell empty. Its own no-branch anticipated exactly this
contingency: "report which screen does most of the killing, as direct input to whether
Phase 1 needs a weaker screen (i) tier." This leg runs the fluid-only census under a
RELAXED tier — conjectured dissipative blow-up with serious numerical evidence, explicitly
labeled as such — plus a direct re-examination of the Leray-projection kill's scope
(which fluid models it actually reaches, not just the one candidate 255 tested). It
extends 255's table; it does not contradict or reopen it.
**Gate.** Under the relaxed tier, does at least one FLUID model enter the census with all
other screens ((ii) profile, (iii) uncertified, (iv) Breden-Chu reach) still passing, with
the evidence-tier downgrade carried explicitly per-row?
  yes -> Bank the extended table with the tier labels prominent. These are Phase-1
         fallback candidates, weaker-evidenced by construction — reportable to the user
         alongside 257's verdict, never silently substituted for 255's tier-1 census.
  no -> The fluid cell is empty even under the relaxed tier — report which screen kills
        each candidate. Combined with 255 and 257, that would be the measured basis for
        re-posing Phase 1's target itself (a user decision, not this leg's).
**Territory.** experiments/p2_route_p1a2_v1_census2.py,
               writeup/data/p2_route_p1a2_v1_census2.json,
               writeup/novelty/leg_261.md, experiments/journal/leg_261.md.
               Reads (never edits) 255's banked census table/JSON, 257's report once
               landed, leg 174's matrix, capabilities.py.
**Difficulty.** standard
**Independence.** Own module; extends (never edits) 255's banked artifacts. **NOT
dispatchable until 257 (P1C) lands** — its brief must carry 257's confirm/contest of the
Leray-projection kill, else it re-litigates a question already in flight.
```

**FLOOR-TABLE block updated in this same edit** (E: 255 → 248). **Floor status: 5/10
strictly (253, 251, 236, 256, 257) — met with margin.**

**Canonical reserve line: reserve count 10 — legs 228, 210, 260, 259, 261, 229, 231, 232,
233, 234.** Effective immediately-dispatchable: 4 (228, 210, 260, 259 — in that priority
order; 260's pre-committed promotion trigger on a DSS-conditional 251 landing stands);
261 blocked on 257; 229 blocked on 226; 231-234 blocked on repairs 217/219/221/225. Next
fresh leg number: **262.**

Nothing in this update lifts a ban, changes any committed gate, or moves any claim about
Walls 1 and 2; Clay stays ~0.05%. No direction question raised — 255's finding is
consequential but the pre-committed answer (wait for 257, then re-pose if needed, with
the user) is already on record above.

---

## DM update, 2026-08-07 — slot-A refill after 253 (NRSX) gated NO and escalated: the
NRS/Tsai screen was mis-stated (sub-linear growth, not decay), the survivor space is
narrowed AND a fourth window opened (Pineau-Vicol rotated backward self-similar); fresh
leg 262 drafted into slot A; no user interruption needed

**253 (NRSX) finished gate NO, escalated per its own no-branch** (parked at
`leg/253-nrsx-v1`, not merged). The finding, recorded at full strength — this is the leg
WORKING, not failing: (1) Tsai 1998 + erratum, read at full text: the sharp hypothesis is
**Remark 5.3's SUB-LINEAR GROWTH condition, not a decay condition** — this repository had
been restating the screen wrong; (2) "unstable-self-similar with finite unstable
spectrum" is **excluded outright** (the exclusion is stability-blind — a Type I bound
alone puts the profile in every L^p, p>3); (3) **DSS narrowed three ways, axisymmetric
DSS dead entirely** (the leg's own inference, labeled as such); (4) **non-self-similar is
now FORCED, not just permitted**; (5) a **fourth candidate class 251's brief never
named**: rotated backward self-similar at α≈1, per Pineau-Vicol arXiv:2607.09619v1 — a
28-day-old UNREFEREED preprint — the one genuinely open window, bypassing the Bernoulli
maximum-principle argument the whole NRS/Tsai method rests on; (6) every exclusion
threshold (λ_*, λ̄, ᾱ) is non-explicit, depending on the unpublished Type-I constant.

**Escalation routing decision (this DM's call): NO immediate user interruption.** 253's
gate already routes the finding where it must go — "must reach leg 251's agent before a
candidate is banked" — and the orchestrator has done that directly. 251's own eventual
yes-branch ESCALATES its named candidate to the user anyway; the user will see 253's
narrowing folded into that report, which is the decision moment. The NEEDS-YOU parking of
253's branch suffices until then. Note for 260 (DSSB, reserve): its brief must now also
read 253's report — the DSS "object" question is materially sharper (non-axisymmetric
only, thresholds non-explicit).

**Slot A: fresh leg 262, drafted from 253's own finding and promoted directly** — ranking
rule (a) (a leg that could move the chain) puts it above 228/210 (verifies of closed-stage
work); the one genuinely open window in Phase 0's survivor space is exactly what the
plan's NEXT stage needs read adversarially, and 251 (breadth screen, in flight) will not
do a proof-level read of a 28-day-old preprint:

```
### 262 — ROUTE-PVRW: THE PINEAU-VICOL ROTATED-SELF-SIMILAR WINDOW, READ ADVERSARIALLY AT
FULL TEXT (the fourth class 253 surfaced — a 28-day-old unrefereed preprint carrying the
only open window; does it hold, and what would a certificate in its class even mean?)
[FLOOR-ELIGIBLE: literature/math]
**Thesis.** 253 identified rotated backward self-similar solutions at α≈1
(Pineau-Vicol arXiv:2607.09619v1) as the one candidate class genuinely open under the
corrected NRS/Tsai screen — because rotation bypasses the Bernoulli maximum-principle
argument the exclusion method rests on. But the preprint is 28 days old and unrefereed;
Phase 0 must not lean on it unexamined. This leg does the proof-level adversarial read 251
cannot: does the construction/argument hold at full text; where are the gap risks; is the
Bernoulli bypass genuine or an artifact of a hypothesis the authors relax silently; and —
253's point (6) carried forward — do PV's own thresholds inherit the non-explicit Type-I
constant problem, or are they explicit? Then the certificate question: what would a
certified object in this class need (profile equation, function space, what "enclosure"
means for a rotating profile), stated concretely enough for Phase 1 to cost it.
**Gate.** Two clauses, both required for yes: (a) the PV argument survives an adversarial
full-text read (no located gap that breaks the rotated window's openness claim), AND (b)
a certificate target in this class can be stated concretely (named profile equation,
named space, named enclosure meaning).
  yes -> Bank both. Forward to 251/Phase 0 as a candidate-class dossier: the window is
         real as far as one careful read can establish, with the unrefereed caveat carried
         prominently — refereed status is a fact, not a formality, and stays in every
         restatement.
  no -> Name the located gap or the concretization failure precisely, with locators. If
        the gap breaks the window, 253's "only open window" collapses to non-self-similar
        FORCED with no self-similar-adjacent class at all — report at full strength and
        flag for 251 immediately; that materially changes Phase 0's answer space.
**Territory.** experiments/p2_route_pvrw_v1_read.py,
               writeup/data/p2_route_pvrw_v1_read.json,
               writeup/novelty/leg_262.md, experiments/journal/leg_262.md.
               Reads (never edits) arXiv:2607.09619v1 full text, 253's parked report
               (branch leg/253-nrsx-v1), Tsai 1998 + erratum as 253 pinned them.
**Difficulty.** heavy
**Independence.** Own module, read-only overlap with 251/253's citation pool (by design —
cross-checking readings is a feature). No written overlap with any live slot. Brief
carries the anti-pausing clause verbatim. Immediately dispatchable.
```

**Flag to the orchestrator, recorded so it is not lost: the "leg 178 / leg 111 / transfer
probe" ruling referenced as awaiting this DM's response was NEVER RECEIVED in this DM
session** — no such forward appears in this session's record. This DM does not respond to
rulings it has not seen; please re-forward the ruling text itself, and it will be
processed in the next update.

**FLOOR-TABLE block updated in this same edit** (A: 253 → 262). **Floor status: 5/10
strictly (262, 251, 236, 256, 257) — met with margin.**

**Canonical reserve line: reserve count 10 — legs 228, 210, 260, 259, 261, 229, 231, 232,
233, 234.** Effective immediately-dispatchable: 4 (228, 210, 260, 259 — 260's brief now
additionally reads 253's report, and its pre-committed promotion trigger on a
DSS-conditional 251 landing stands); 261 blocked on 257; 229 blocked on 226; 231-234
blocked on repairs 217/219/221/225. Next fresh leg number: **263.**

Nothing in this update lifts a ban, changes any committed gate, or moves any claim about
Walls 1 and 2; Clay stays ~0.05% — 253's narrowing of the survivor space and PV's open
window are recorded as facts about the LITERATURE, not as movement of any link of the
chain. No direction question raised to the user: 253's escalation routes through 251's
own eventual report, per its gate's own wording.

---

## DM update, 2026-08-07 — slot-H refill after 257 (P1C) escalated YES on both clauses:
stage-V lift clause satisfied on paper AND a new obstruction independently closes the
fluid route in H²(µ); 261 unblocked and promoted; DM recommendation drafted for the
NEEDS-YOU packet; leg-178 ruling STILL not received

**257 (P1C) escalated per its own yes-branch** (PR #19, `leg/257-p1c-v1`, not on main).
Recorded at full strength:

1. **The stage-V ban's lift clause is satisfied on paper.** Breden-Chu's H²(µ)
   weighted-Sobolev space is a genuine namable fourth space: each of the three death
   mechanisms (leg 54's Z₁ block-coupling; leg 56's (H,D) consistency defect; legs
   163/176's origin-H² a=0 cap) evades AT THE MECHANISM LEVEL, each with its own locator,
   not by analogy — measured Z₁ = 0.065136 in the new space against leg 54's 8.9591 and
   leg 176's 140.72. 257 correctly does not lift on its own signature; the lift is the
   user's, now pending in NEEDS-YOU.
2. **A NEW, independent obstruction closes the FLUID route through this space anyway:**
   the Leray projection provably leaves L²(µ) — an explicit divergence-free Gaussian
   witness shows P[(u·∇)u] carries an algebraic |x|⁻⁴ tail whose coefficient IS the
   energy (so it cannot vanish) while the space's own weight underflows to 0. This
   CONFIRMS and STRENGTHENS leg 255's Li-Zhou kill and explicitly withdraws 255's own
   concession that the kill might be rescuable. The fluid cell now has TWO independent
   kills. Both findings are with 251's agent.

**DM recommendation for the user's NEEDS-YOU packet (drafted per the orchestrator's
invitation — a recommendation, not a decision):**

> **On the lift: LIFT the stage-V ban per its own clause.** The clause's conditions are
> met exactly as written (namable fourth space + its own scoping leg establishing
> non-subjection, mechanism by mechanism, measured). Keeping a ban whose lift condition
> has been honestly satisfied would convert it from a measurement into a superstition.
> **But lift it with its practical value stated honestly in the same breath:** finding #2
> means the lift does NOT reopen the fluid route through H²(µ) — that door is now closed
> by two independent measurements, and 257 itself withdrew 255's rescuability concession.
> What the lift buys: the machinery is legal again for NON-fluid targets (e.g., 255's two
> non-fluid census survivors), for 256's in-flight reproduction, and for any FUTURE
> space-modification proposal (a different weight evading the |x|⁻⁴-tail obstruction —
> note the tail coefficient is the ENERGY, so polynomial reweighting looks structurally
> doomed; any such proposal needs its own scoping leg either way).
> **On Phase 1's target: no second decision is needed from you today.** This DM's
> pre-committed re-posing moment ("when 257 lands") has arrived, but the honest
> recommendation is to DEFER re-posing until 251 (Phase 0), 261 (the relaxed fluid
> census, dispatching now), and 262 (the Pineau-Vicol window read) land — those three
> determine what a fluid target even is before it is worth re-aiming Phase 1 at one.

**Slot H: leg 261 (Route-P1A2) promoted — its own blocking condition ("NOT dispatchable
until 257 lands") just cleared, and ranking rule (a) puts it first among dispatchables**
(it feeds the user's eventual re-posing decision directly). **Brief addition, mandatory:**
257 CONFIRMED and strengthened the Leray kill (explicit Gaussian witness, |x|⁻⁴ tail,
energy coefficient) and withdrew 255's rescuability concession — 261's scope
re-examination must incorporate 257's witness mechanism, not just 255's Li-Zhou screen,
and its relaxed-tier candidates must each be checked against BOTH kills. Anti-pausing
clause verbatim.

**Leg-178 flag, SECOND notice:** the orchestrator again references "leg-178 dispatch
instructions" as awaited, but the underlying ruling/text has still never reached this DM
session — nothing to act on exists in this session's record. **Re-forward the ruling
text itself; this DM will not respond to a ruling it has not seen.** Recorded twice now
so the gap cannot be attributed to DM silence.

**FLOOR-TABLE block updated in this same edit** (H: 257 → 261). **Floor status: 5/10
strictly (262, 251, 236, 256, 261) — met with margin.**

**Canonical reserve line: reserve count 9 — legs 228, 210, 260, 259, 229, 231, 232, 233,
234.** Effective immediately-dispatchable: 4 (228, 210, 260, 259 — 260's pre-committed
promotion trigger stands, and its brief reads 253's and 257's reports); 229 blocked on
226; 231-234 blocked on repairs 217/219/221/225. Next fresh leg number: **263.**

Nothing in this update lifts a ban — the stage-V lift is drafted as a RECOMMENDATION and
sits with the user; 257's Z₁ = 0.065136 is recorded as a property of the fourth space,
not as movement of any link (the same space's fluid application is closed by finding #2,
and no output here is described as movement toward Clay). Clay stays ~0.05%. The one open
direction question (re-posing Phase 1's target) is deliberately deferred with its trigger
condition named: it ripens when 251, 261, and 262 have all landed.

---

## DM update, 2026-08-07 — THE LEG-178 (WES) RULING, RECEIVED AND PROCESSED (third
notice resolved — the re-forward arrived): 178 unparked for landing under its YES branch,
correction leg 263 and the single transfer probe 264 drafted, Ruling 3 adopted as a
standing pre-registration rule

**The user's three rulings on leg 178, recorded verbatim-in-substance:**

1. **Gate answers YES under its literal wording.** Clause 3 is SCOPED, not overruled:
   evaluated only at grading depths where the runner's own contamination diagnostic is
   below 1 (at n_grade = 96 the innermost panel sits at θ ~ 3e-31 with contamination
   3.1e+03 — the instrument stopped working; over the three valid depths the spread is
   2.2839e-07). This is lesson 86, not a post-hoc relaxation. 178 lands under the YES
   branch with this ruling recorded in its own gate-answer wording.
2. **Leg 111's headline is re-scoped as a DOCUMENTED correction** — visible, not a buried
   capabilities.py qualifier (fourth over-read closure: 165, 180, 185, 178-confirming-165).
   **The two-triples ambiguity governs the edit**: `plan_of_record.py`'s "three
   realizations" (P0 deliverable AND the re-posed stage-V ban) means ℓ¹_w (54) /
   collocation (56) / origin-H² (163/176/182) — weighted-energy NOT a member; the
   journals of legs 141, 165, 183 use the same phrase for a triple that DOES include
   weighted-energy. The revival falsifies only the second usage. Pin per occurrence, edit
   only what the revival reaches, NO global search-and-replace, and the live ban's
   justification is untouchable.
3. **Standing pre-registration rule, adopted here for all future legs touching
   `solver/energy_coercivity.py`:** the fixed depth ladder {12, 24, 48, 96} is replaced
   by "the deepest grading depth at which contamination < 1" — a strengthening, ruled by
   the user, applying to leg 264 below and everything after.

**Bounding, exactly as ruled: NO weighted-energy lane opens** ("not dead" is not "open";
under a Clay goal a revived toy lane is not worth chasing for its own sake). The revival
is a METHOD fact worth exactly one question — the transfer question — drafted as ONE leg
below, ranked behind the programme. Leg 178's own scope line stays load-bearing: EGM's
two free modulation parameters mean a gap on a constrained trial space is not a
certificate; the +0.499999667 is EGM's published −1/2 reproduced numerically ("The −1/2
is theirs"); the object is the a=0 CLM linearisation with its exactly-zero Y₀.

**Dispatch plan (the coordinator's "your call" on ordering, decided):**

- **178-LANDING: unpark `leg/178-wes-*` and land under the YES branch** with Ruling 1's
  wording recorded. Everything is decided; this is light but claim-bearing (it lands a
  YES). **Priority: next vacancy, ahead of 228/210/260/259 — or as a bench-scale dispatch
  now if the orchestrator judges it fits the leg-258 shape; either satisfies the user's
  "dispatch it" without displacing any programme slot.** Its §7b post-landing verify
  can fold into 263's dispatch (same family) or stand alone at the orchestrator's
  convenience.
- **263 then 264, in that order** (the correction before the probe, so 264's brief cites
  corrected prose), both behind every programme need (251, 261, 262, 256 in flight, and
  any Phase-1 construction the user's 257 ruling spawns).

```
### 263 — ROUTE-WESC: THE LEG-111 HEADLINE RE-SCOPE + PER-OCCURRENCE TRIPLE PINNING
(Ruling 2, executed carefully — a DOCUMENTED correction, not a buried qualifier)
**Thesis.** Ruling 2 above, in full. The dangerous failure mode is named by the ruling
itself: a global fix to journal prose that silently weakens plan_of_record.py's live
stage-V ban, whose justification rests on a triple that does NOT include weighted-energy.
**Gate.** After the correction: (a) is every occurrence of the "three realizations" /
"measured-dead" phrasing pinned to its intended triple (plan-triple vs journal-triple),
occurrence by occurrence, with only the revival-reached occurrences edited; (b) is leg
111's headline re-scoped visibly (its own correction note, stating what over-read what);
and (c) is plan_of_record.py's ban text byte-identical before and after?
  yes -> Bank. The fourth over-read closure is on the record as a correction, and the ban
         stands untouched.
  no -> If ANY occurrence is ambiguous at full context (cannot be pinned to one triple),
        STOP, list the ambiguous occurrences, and escalate — do not guess a triple.
**Territory.** the named occurrence sites in experiments/journal/leg_141.md, leg_165.md,
               leg_183.md; leg 111's headline site(s) (locate exactly, cite in report);
               a correction note in writeup/ (visible, per the ruling);
               writeup/novelty/leg_263.md, experiments/journal/leg_263.md.
               plan_of_record.py is READ-ONLY — gate clause (c) enforces it.
**Difficulty.** standard
**Independence.** Prose/documentation territory, disjoint from every live slot. Ranked
behind all programme legs, ahead of 264. Dispatchable once 178 lands (it corrects prose
in light of 178's landed result — sequencing, not a hard block).
```

```
### 264 — ROUTE-WETP: THE ONE TRANSFER PROBE — DOES THE EXACT-FUNCTIONAL TRIAL-SPACE
CONSTRAINT SURVIVE OFF a=0? (the single question Ruling 178-4 licenses)
[FLOOR-ELIGIBLE: math]
**Thesis.** Constraining the trial space by exact functionals moved a window from width
0.0 to 4.0 and a gap from −0.4999241 to +0.499999667 — on the a=0 CLM linearisation, the
easiest object in the building. The ruled question: does that MOVE survive on an object
that is not a=0? If yes, it is a technique the Clay programme can use; if no, a curiosity.
The leg pre-registers its non-a=0 object BEFORE running (its choice, from objects this
repository already carries, respecting every ban — e.g. an a≠0 gCLM linearisation or the
HL profile as a measurement substrate; named in the novelty pass, not after results), and
pre-registers depth per Ruling 3: the deepest grading depth at which contamination < 1,
NOT the fixed ladder.
**Gate.** On the pre-registered non-a=0 object, does the exact-functional constraint
produce the same MOVE SHAPE (a window opening from zero width AND a gap sign change /
comparable-magnitude improvement, both stated as thresholds in the novelty pass before
running)?
  yes -> Report as a transferable METHOD fact for the programme's use. NO lane opens, no
         construction follows under this leg's authority — the user's bounding stands.
  no -> Report the curiosity verdict at full strength: the move belongs to a=0's
        degeneracy. Weighted-energy stays exactly where Ruling 178-4 put it.
**Territory.** experiments/p2_route_wetp_v1_transfer.py,
               writeup/data/p2_route_wetp_v1_transfer.json,
               writeup/novelty/leg_264.md, experiments/journal/leg_264.md.
               Reads (never edits) solver/energy_coercivity.py and leg 178's landed
               report.
**Difficulty.** standard
**Independence.** Own module. Ranked LAST among the 178-family items and behind every
programme leg, per the ruling's own ordering intent ("must not delay P0 or Phase 1").
Dispatchable once 178 lands and 263 is at least dispatched (reads corrected prose).
```

**Canonical reserve line: reserve count 12 — legs 178L (the ruled landing), 263, 264,
228, 210, 260, 259, 229, 231, 232, 233, 234.** Effective dispatchable: 5 now (178L, 228,
210, 260, 259 — priority order: 178L, then 228/210/260/259 as before, with 260's trigger
standing), plus 263/264 sequenced behind 178's landing. 229 blocked on 226; 231-234
blocked on repairs. **Roster and FLOOR-TABLE unchanged (no slot touched). Floor stays
5/10 strictly.** Next fresh leg number: **265.**

Nothing in this update lifts a ban: Ruling 1 lands a leg under its own literal gate;
Ruling 2 explicitly protects the stage-V ban's justification; the weighted-energy lane
stays SHUT by the user's own bounding, and 264's yes-branch pre-commits that no lane
opens under leg authority. Nothing here is a statement about HL_S2_nonsymmetric or any
link of the L1→L4 chain; Clay stays ~0.05%. The leg-178 missing-forward flags (two
notices above) are RESOLVED — the ruling arrived and is fully processed in this update.

---

## DM update, 2026-08-07 — slot-C refill after PHASE 0 ANSWERED: 251 (P0T) gate YES,
escalated — one unconditional candidate named (BCG's compressible imploding profile,
γ=7/5); 260's pre-committed promotion trigger FIRED (slot C = 260); Phase-1 costing leg
265 drafted, blocked on 251's verifier

**251 (P0T) finished gate YES, escalated** (PR #20, `leg/251-p0t-v1`, verifier in flight
at `verify/251-p0t-review`). Recorded at full strength, with its own honesty flags kept
attached: the ONE unconditional Phase-1 candidate is the **3D isentropic COMPRESSIBLE
Navier-Stokes imploding self-similar profile at γ=7/5** (BCG arXiv:2208.09445; non-radial
companion CGSS arXiv:2310.05325) — **explicitly compressible, NOT the incompressible
system Clay's problem is about, per the leg's own flag**. The certificate obligation is
exactly the term BCG's own §7 says nobody has enclosed, only dominated by parameter
restriction — i.e., precisely Phase 1's "viscous term from DOMINATED to ENCLOSED," on a
candidate that (being compressible) sits outside the Leray-projection kills, which apply
to the incompressible projector in H²(µ). Two DSS candidates sit in a CONDITIONAL tier
blocked on Entry B's scoping (leg 260) AND 257's obstruction; Pineau-Vicol is reported
but not named (no numerical anchor — 262's read is in flight). NOTE: arXiv:2208.09445 is
already in this repository's ledger via leg 174/197 (VNL) — 251's naming connects to an
already-located citation, not a fresh one.

**Slot C: leg 260 (Route-DSSB) — the pre-committed promotion trigger FIRED.** Its own
reserve entry says: "UNLESS 251 lands with a DSS-conditional candidate in its yes-branch,
in which case 260 promotes to the next vacancy immediately, pre-committed here so no
re-ranking decision is needed at that moment." 251 landed with TWO. No discretion
exercised; the trigger executes as written. **Brief additions (mandatory): 260 reads
251's parked report (the two DSS-conditional candidates and what blocks them), 253's
narrowing (non-axisymmetric only, thresholds non-explicit), and 257's obstruction — its
"object" answer must name which surviving DSS shape it is scoping, and its price answer
now has a concrete customer.** Anti-pausing clause verbatim.

**Phase-1 costing: drafted NOW, dispatched only after the verifier — agreeing with the
orchestrator's hold recommendation, and matching this DM's own pre-commitment
(construction gated behind reports).** A costing leg is scoping, not construction — it
does not need the stage-V lift (still with the user) and builds nothing — but it would
inherit any defect the verifier finds in 251's naming, so it waits:

```
### 265 — ROUTE-P2C: WHAT WOULD A CERTIFICATE FOR BCG's IMPLODING PROFILE ACTUALLY COST?
(Phase-1 costing of 251's unconditional candidate — scoping, NOT construction; blocked on
251's verifier)
[FLOOR-ELIGIBLE: math/literature]
**Thesis.** 251 named the BCG γ=7/5 imploding self-similar profile as Phase 1's
unconditional candidate; the certificate obligation is BCG §7's own never-enclosed
dissipative term. Before any construction is posable, cost it: (1) the profile equation
and the precise term to enclose, stated from BCG/CGSS full text; (2) what function-space
setting the enclosure would run in — noting the stage-V lift question (H²(µ) legality)
sits with the user, and compressible NS has no Leray projector, so 257's obstruction must
be checked for a compressible ANALOGUE rather than assumed absent; (3) what exists in
capabilities.py vs. what must be built; (4) the honest gap between "certificate for the
compressible imploding profile" and Clay's incompressible problem, stated in the same
breath as the cost, per 251's own flag.
**Gate.** Can all four be answered concretely enough that a hypothetical construction leg
could be drafted with a pre-committed gate and a named territory, with no further scoping
needed?
  yes -> Bank the costing dossier. ESCALATE to the user as Phase 1's construction
         decision packet (cost + gap-to-Clay stated together). Construction itself needs
         the user's go — not this leg's, and not the DM's.
  no -> Name which of the four resists concreteness and why — if the blocker is the
        compressible analogue of 257's obstruction, that is a finding at full strength
        and goes straight to the user's packet alongside the stage-V lift question.
**Territory.** experiments/p2_route_p2c_v1_costing.py,
               writeup/data/p2_route_p2c_v1_costing.json,
               writeup/novelty/leg_265.md, experiments/journal/leg_265.md.
               Reads (never edits) BCG arXiv:2208.09445 + CGSS arXiv:2310.05325 full
               text, 251's report as VERIFIED, 257's obstruction mechanism,
               capabilities.py, leg 240's DOMINATED/ENCLOSED census rows.
**Difficulty.** heavy
**Independence.** Own module; read-only overlaps by design. **BLOCKED on
`verify/251-p0t-review` landing clean** — if the verifier contests 251's naming, this
leg's premise re-opens and it must be re-drafted, not patched. Once unblocked, it is the
TOP-priority reserve item (ranking rule (a): it is the programme's next link).
```

**User-facing framing: held**, per the orchestrator's recommendation — 251's finding
reaches the user through its verified report plus this DM's eventual packet (stage-V lift
+ 257's obstruction + 251's candidate + 265's costing when ready), not piecemeal.

**FLOOR-TABLE block updated in this same edit** (C: 251 → 260). **Floor status: 4/10
strictly (262, 236, 256, 261) — met** (260 counted "no" conservatively, same convention
as 254).

**Canonical reserve line: reserve count 12 — legs 265, 263, 264, 228, 210, 259, 229, 231,
232, 233, 234, plus 178L mid-landing (dispatched, not reserve stock once it lands).**
Effective immediately-dispatchable: 3 (228, 210, 259); 265 blocked on 251's verifier
(TOP priority once clear); 263 sequenced behind 178's landing, 264 behind 263; 229
blocked on 226; 231-234 blocked on repairs 217/219/221/225. Next fresh leg number:
**266.**

Nothing in this update lifts a ban or opens construction — 265's yes-branch terminates in
a user decision packet, and 251's candidate is recorded with its own compressible-not-Clay
flag attached, not as movement of any link. Clay stays ~0.05%. No direction question
raised now; the assembled packet (after the verifier and 260/262/265 report) is where the
user's Phase-1 construction decision lands.

---

## DM update, 2026-08-07 — 251's VERIFIER FOUND A LOAD-BEARING GAP IN OBLIGATION #1
(no stationary dissipative profile system exists at BCG's scaling); rework leg 266 cut at
top of queue into slot A per the standing mandate; 262 (PVRW) landed clean with the
infinite-kinetic-energy caveat; literature leg 267 drafted into slot G; 265's spec
amended; 256's gate answer NOT yet reported to this DM

**251's verifier (merged `6a795cd`): everything confirmed at primary source EXCEPT one
sentence.** Confirmed by direct re-fetch (not from 251's transcriptions): the honesty
framing, the Wall-2 statement, the compressible-NS-has-no-Leray-projector claim, the
agreement with 253. **The gap: obligation #1 asks to enclose "the self-similar profile
system of the dissipative equation" — no such stationary system exists at BCG's scaling.**
Dissipation enters only as a non-autonomous, exponentially-decaying forcing (F_dis, e^{-δs₀}
prefactor) on the RHS of the EULER profile system — an architecture 251's own report
describes correctly elsewhere, making obligation #1 internally inconsistent with its own
text. Taken literally it would send Phase-1 construction after an object that does not
exist. The verifier's assessment of the real obligation: **enclose the STABILITY step —
the r-restriction argument by which the profile dominates F_dis, at an r outside BCG's
dominance regime.**

**Mechanism decision (the orchestrator's "your call"): a REWORK LEG, not a DM-authored
packet patch.** The standing mandate is explicit (verifier confirms a gap → cut a rework
leg at the top of the queue, same territory, gate pre-committed to the corrected
measurement) — and re-posing a certificate obligation is research prose, which this DM
may not write. 251's PR body stays as historical record; the rework leg adds the visible
correction. **Nothing goes to the user until 266 lands — the packet waits.**

```
### 266 — ROUTE-P0TC: RE-POSE 251's OBLIGATION #1 (the verifier's confirmed gap — a
rework leg, same territory, correction in 251's own parked files)
**Thesis.** Verify_251's finding, in full (above). The correction target is ONE
obligation's wording; the naming itself, the compressible-vs-Clay flag, and the rest of
the report survived scrutiny and are NOT reopened by this leg.
**Gate.** Does the re-posed obligation #1 (a) match the papers' actual architecture as
the verifier states it (F_dis as non-autonomous forcing on the Euler profile system; the
enclosure obligation living in the stability step's r-restriction argument, at r outside
BCG's dominance regime), (b) leave every verifier-confirmed claim in 251's report
byte-untouched, and (c) read consistently with 251's own (correct) architecture
description elsewhere in the same report, with a visible correction note citing
verify_251 as the source?
  yes -> Land the correction into 251's parked branch (leg/251-p0t-v1 / PR #20) so the
         report is self-consistent BEFORE it reaches the user. Unblocks 265.
  no -> If the obligation CANNOT be re-posed coherently — i.e. the stability-step
        enclosure also fails to be a statable certificate target — escalate immediately:
        that would reopen the naming itself, which this leg is otherwise forbidden to do.
**Territory.** 251's parked files on leg/251-p0t-v1 (the obligation-#1 sentence(s) and a
               correction note ONLY), writeup/novelty/leg_266.md,
               experiments/journal/leg_266.md.
               Reads (never edits) writeup/novelty/verify_251.md, BCG §7/CGSS full text.
**Difficulty.** standard
**Independence.** Territory is 251's parked branch — no live slot touches it. TOP OF
QUEUE per the standing rework mandate. Anti-pausing clause verbatim.
```

**262 (PVRW) landed clean (`ba0f9fe`), recorded at full strength:** the Pineau-Vicol
window SURVIVES adversarial review (6 soft spots, 0 window-breaking) — but the class
necessarily has **infinite kinetic energy, so even total success resolves Perelman's
conjecture, not Clay** — reinforcing, at proof level, that 251 was right not to name it.
Also: the "α≈1" framing understates the open window by ~5.15 million decades once every
non-explicit constant is unwound to its most favorable value. PV stays REPORTED, not
named; any future leg proposing it must carry the Perelman-not-Clay caveat in its first
sentence.

**Slot G: fresh leg 267, drafted for two reasons at once** (the corrected obligation's
direct literature need; and with 262/256 landed, live floor-eligibility would fall to
2/10 — a §3b breach the FLOOR-TABLE test would catch):

```
### 267 — ROUTE-FDL: HAS ANYONE EVER RIGOROUSLY ENCLOSED A FORCING-DOMINATION /
TRAP-REGIME ARGUMENT OF BCG's SHAPE? (the stability-step precedent question — the
literature the corrected obligation #1 stands on)
[FLOOR-ELIGIBLE: literature]
**Thesis.** If 266 lands, Phase 1's real certificate obligation is enclosing a
stability-step argument: a non-autonomous, exponentially-decaying forcing (F_dis)
dominated by a profile in a restricted regime, at parameter values OUTSIDE the published
dominance regime. Before 265 costs that, the precedent question: has ANY computer-assisted
/ interval-arithmetic work ever enclosed an argument of this shape — non-autonomous
forcing domination, trap regions for non-autonomous perturbations of a stationary
profile, in ANY field? (This is a different question from leg 240's viscous-term census
— that censused fluid self-similar objects; this censuses the ARGUMENT SHAPE.)
**Gate.** Does a full-text-verified precedent exist (named paper, named theorem, the
enclosure genuinely of a non-autonomous forcing-domination step — not a stationary
enclosure relabeled)?
  yes -> Bank with locators; 265 inherits it as its "what exists" row and Phase 1 gets a
         template. Name the gap between the precedent's setting and BCG's.
  no -> Bank the absence at full strength with the closed nets named (lesson 91): the
        stability-step enclosure would be methodologically NEW, which raises 265's cost
        estimate and belongs in the user's packet verbatim.
**Territory.** experiments/p2_route_fdl_v1_precedent.py,
               writeup/data/p2_route_fdl_v1_precedent.json,
               writeup/novelty/leg_267.md, experiments/journal/leg_267.md.
               Reads (never edits) verify_251.md, BCG §7, viscous_novelty.py's ledger.
**Difficulty.** standard
**Independence.** Pure literature, own module. Does NOT wait on 266 (the precedent
question is well-posed from the verifier's own wording either way). Immediately
dispatchable. Anti-pausing clause verbatim.
```

**265's spec is AMENDED (not re-drafted — the naming survived; the obligation did not):**
its thesis clause (1) now reads "the stability-step enclosure obligation as re-posed by
leg 266," not "the profile equation and the precise term to enclose"; its blocking
condition changes from "verify/251-p0t-review landing clean" to **"leg 266 landed"**; it
additionally reads 267's precedent verdict if available at dispatch. All other clauses
(compressible-analogue check of 257's obstruction, exists-vs-build, gap-to-Clay in the
same breath) stand.

**256 (P1B) landed per the orchestrator, but its GATE ANSWER has not been reported to
this DM** — the record here cannot state its outcome. **Flag: send 256's finding summary
in the next message**; its result (did the Breden-Chu reproduction succeed?) bears
directly on 265's exists-vs-build row and on the user's stage-V packet.

**FLOOR-TABLE block updated in this same edit** (A: 262 → 266; G: 256 → 267). **Floor
status: 3/10 strictly (267, 236, 261) — met exactly; the §5 commitment (two cycles after
P0 lands in the plan) is noted as approaching and will be reported honestly if the roster
cannot hold 3 without drafting-to-fit.**

**Canonical reserve line: reserve count 11 — legs 265, 263, 264, 228, 210, 259, 229, 231,
232, 233, 234 (178L mid-landing, not reserve stock).** Effective immediately-dispatchable:
3 (228, 210, 259); 265 blocked on 266; 263 behind 178's landing; 264 behind 263; 229
blocked on 226; 231-234 blocked on repairs. Next fresh leg number: **268.**

Nothing in this update lifts a ban or opens construction. 262's PV verdict and the
verifier's correction are recorded as facts about the literature and about one report's
wording — not movement of any link. Clay stays ~0.05%. No direction question raised: the
packet assembles after 266 (and ideally 256's reported outcome, 260, 265, 267) — one
coherent decision, not piecemeal drops.

---

## DM update, 2026-08-07 — post-usage-limit reconciliation + leg 249's PUB2 finding:
rework leg 268 (PUB2R) cut into slot B (absorbs 259), 264 promoted into slot H (floor
held at 3/10), the missing gate answers recovered from ORCH_STATE.md, verify-256
re-dispatch flagged as support

**The usage-limit event, reconciled** (from reports/ORCH_STATE.md, read directly): five
agents died simultaneously (236, 226, 248, verify-256, 261's sibling checks) to an
account-wide session limit — external, not work-related. Slots E (248), F (236), J (226)
resume from their `-wip2` salvage branches with fresh agents; slots D (221) and I (252)
need their branches re-checked before assuming state; **verify-256 needs a fresh
re-dispatch as SUPPORT (verifiers run outside the ten slots, per this run's own
precedent) — a landed claim-bearing YES (256) currently sits unverified, which §7b does
not allow to persist.**

**The gate answers this DM was missing, now on record:**
- **256 (P1B): gate YES** — the Breden-Chu reproduction succeeded end to end (landed
  `68c74de`). The machinery is usable here; 265's exists-vs-build row and the user's
  stage-V packet both inherit this directly.
- **261 (P1A2): gate NO, at full strength** — 0 of 18 fluid rows survive even the
  RELAXED evidence tier; the killer is screen (iv_a): **incompressibility is a nonlocal
  constraint that no fluid row passes by construction under Remark 40's stated reach**
  (landed `28545ce`, orchestrator-landed post-agent-death). Combined with 255's census
  and 257's Leray obstruction, the incompressible-fluid route through Breden-Chu's
  machinery is now closed THREE independent ways. The pre-committed re-posing trigger
  (251+261+262 all landed) HAS NOW FIRED — the re-posing question goes in the user
  packet, which still waits on 266; recorded here so it cannot be lost.
- **178 (WES): landed under the user's ruling** — 263's sequencing condition ("once 178
  lands") is cleared.
- **260 (DSSB): reported finished by the orchestrator, gate answer STILL not reported to
  this DM** — third missing-outcome flag this session (256's and 260's; 256's now
  resolved). Send 260's finding summary next message.

**Leg 249 (H2CV2), escalated, recorded at full strength — the submission-blocking
finding:** both PUB2 headline numbers reproduce at stated precision, BUT in exact
rational arithmetic: (1) the banked `σ_min_at_512 = 0.09080465147034879` is PROVED wrong
(pencil not positive-definite at that λ; true value certified in `(0.090804094,
0.090804194)`); (2) the banked `‖T⁻¹‖_X = 4.02614534796022` falls OUTSIDE 249's own
certified bracket `[4.02623993, 4.02624155]`; (3) **PUB2's "truncation-independent
‖T⁻¹‖_X = 4.026" is unsupported** — the tail inverse norm is still rising at N=1024 with
decrements converging to ≈4.0318, and leg 176's own raw `reading` field already said
4.03; the journal and PUB2 tightened it beyond what the data supports. Leg 176's gate
answer and conclusions otherwise confirmed — a precision/convergence correction, not a
reversal.

**Slot B: rework leg 268, cut at top of queue per the standing mandate — ranked exactly
as the orchestrator recommends (above 263/264-family work; an approved external-facing
document currently quotes an unsupported number). 259 (PUB2P) is ABSORBED into 268 and
retired as a separate number** (drafted, never dispatched) — two legs must not edit one
submission-track document in the same cycle.

```
### 268 — ROUTE-PUB2R: CORRECT PUB2's ‖T⁻¹‖_X FIGURE AND THE TWO PROVED-WRONG BANKED
VALUES (leg 249's exact-arithmetic finding — SUBMISSION-BLOCKING rework; absorbs 259's
two prose nits)
**Thesis.** Leg 249's findings (1)-(3) above, in full. The correction follows leg 249's
own full report recommendation (read experiments/journal/leg_249.md on leg/249-h2cv2-v2
FIRST — state ≈4.03, or state the convergence trend honestly, per what that report
actually supports). Absorbed from 259: (a) §3.5 states 0.71465 = 1/1.3993 as "exactly"
(it is a round-up by 7.0e-06, disclosed at §3.2 but not §3.5); (b) the §3.1 table cell
at line 175 still presents "σ_min bounded away from zero" as verified, which §3.5
correctly withdraws.
**Gate.** After the rework: (a) does every PUB2 site quoting 4.026 / truncation-
independence state only what leg 249's certified data supports (per 249's own report
recommendation), with the convergence trend stated honestly; (b) are the two proved-wrong
banked values corrected via an EXPLICIT correction artifact citing 249's certified
brackets (no silent hand-edit of a banked JSON; leg 176's gate-answer text untouched, as
249 itself confirms it); (c) are 259's two absorbed nit sites fixed; and (d) is no other
sentence's meaning changed?
  yes -> Bank. PUB2 quotes only supported figures; flag to the orchestrator that the
         document needs a fresh §7b pass before any actual submission.
  no -> If PUB2's ARGUMENT (not merely its quoted figure) turns out to depend on
        truncation-independence at 4.026, STOP and escalate — that would be substantive,
        and the submission approval itself must return to the user.
**Territory.** writeup/4_p2_lottery/TECHNICAL_P2_PUB2_V1.md,
               writeup/4_p2_lottery/BLOG_P2_PUB2_V1.md (if it quotes the figure),
               a correction artifact alongside leg 176's banked JSON (explicit, cited —
               regenerate or annotate, never silently overwrite),
               writeup/novelty/leg_268.md, experiments/journal/leg_268.md.
               Reads (never edits) leg 249's branch leg/249-h2cv2-v2 in full.
**Difficulty.** standard
**Independence.** Submission-track territory, no solver module. TOP priority alongside
266 (both block the user-facing packet/submission). Anti-pausing clause verbatim.
```

**Slot H: leg 264 (WETP) promoted, with its sequencing AMENDED** (this DM's own queue,
amended with the reason recorded): its "263 at least dispatched" condition existed so 264
would read corrected triple-prose; instead, **264's brief now cites Ruling 2's two-triples
distinction directly**, which protects it from the over-read without waiting on 263 —
and 178 (its hard condition) has landed. Promoting 264 also holds the floor at exactly
3/10 (236, 267, 264), which would otherwise breach with 261 landed. 263 stays in
reserve, dispatchable at the next vacancy.

**FLOOR-TABLE block updated in this same edit** (B: 249 → 268; H: 261 → 264). **Floor
status: 3/10 strictly (236, 267, 264) — met exactly; the §5 roster-honesty commitment
stands.**

**Canonical reserve line: reserve count 9 — legs 265, 263, 228, 210, 229, 231, 232, 233,
234** (259 retired-absorbed into 268; 264 promoted; 178L landed). Effective
immediately-dispatchable: 3 (263, 228, 210); 265 blocked on 266's landing; 229 blocked
on 226; 231-234 blocked on repairs 217/219/221/225 (221's own landing would unblock
233). Next fresh leg number: **269.**

Nothing in this update lifts a ban or opens construction. 249's findings are recorded as
corrections to precision/convergence claims, leg 176's gate answer standing — not as
movement of any link. Clay stays ~0.05%. The one ripened direction question (re-posing
Phase 1's incompressible-fluid framing, three independent closures now on record) is
explicitly PARKED INTO THE PACKET behind 266 — not raised piecemeal.

---

## DM update, 2026-08-07 — slot-C refill: 260 (DSSB) gate NO recorded (DSS ban basis
upgraded to SUBSTANTIVE), which resolves 251's conditional tier the hard way; 263 (WESC)
promoted per reserve order; recovery from the outage confirmed complete

**260 (DSSB): gate NO, recorded at full strength** (journaled, on `main`): Entry B's
three lift questions (function space, object, price) could not be answered concretely —
which, per 260's own pre-committed no-branch, is itself the measured reason the expensive
entrance stays shut, and **upgrades the DSS ban's basis from cost-shaped to
SUBSTANTIVE.** Consequences, recorded so the packet carries them: (1) **251's two
DSS-conditional candidates are now EXCLUDED** — their tier was blocked on Entry B's
scoping, which has answered; no user ruling is needed to keep Entry B shut, since its own
lift condition failed on the merits. (2) **Phase 0's answer space is now exactly one
unconditional candidate** — BCG's compressible imploding profile, pending 266's
obligation-#1 correction — plus PV reported-not-named (Perelman-not-Clay, leg 262). The
user packet (behind 266) states this narrowing explicitly.

**Recovery confirmed complete** per the orchestrator: 221/236/248/252/226 redispatched
from salvage, 266 (P0TC) and 268 (PUB2R) running, verify-256 re-dispatched. All three
missing-outcome flags this session (256, 260, and the earlier 178) are now resolved.

**Slot C: leg 263 (Route-WESC) promoted per reserve order** — Ruling 2's correction leg
(per-occurrence two-triples pinning, plan_of_record.py byte-identical, visible correction
note), sequencing long cleared by 178's landing. Spec above stands verbatim; brief
carries the anti-pausing clause. Note for its brief: 264 (WETP, slot H) is running in
parallel with Ruling 2's distinction cited directly in its own brief, so 263 and 264 do
not conflict — 263 edits journal prose 264 only reads rulings about.

**FLOOR-TABLE block updated in this same edit** (C: 260 → 263). **Floor status: 3/10
strictly (236, 267, 264) — unchanged, met exactly.**

**Canonical reserve line: reserve count 8 — legs 265, 228, 210, 229, 231, 232, 233,
234.** Effective immediately-dispatchable: 2 (228, 210) — **below this DM's comfort
line though above the §3a count watermark; per the standing commitment, fresh unblocked
candidates will be drafted in the same update that next promotes either of 228/210, and
the packet's aftermath (user decisions on 266/268/stage-V) is expected to generate the
next natural batch.** 265 blocked on 266's landing (TOP priority once clear); 229
blocked on 226; 231-234 blocked on repairs 217/219/221/225. Next fresh leg number:
**269.**

Nothing in this update lifts a ban — 260's NO tightens one (basis upgraded, recorded, no
wording change needed since "never" already stood). No committed gate changes; Clay
stays ~0.05%. No direction question raised: the packet behind 266 now carries the
DSS-exclusion narrowing alongside everything else.

---

## DM update, 2026-08-07 — both priority corrections LANDED (266 into PR #20, 268 onto
main): 265 unblocked and promoted into slot A with no third review pass; reserve
refreshed with 269/270 from 268's own flags; 249's branch recommended for standalone
merge; THE USER PACKET IS NOW ASSEMBLABLE

**266 (P0TC) landed into 251's parked branch** (PR #20 at `873a15f`, correctly still
unmerged — 251 remains an escalation): obligation #1 re-posed onto the stability step
(enclosing the argument WITH F_dis retained, at r outside BCG's dominance window
`(1.1666667, 1.1909830)`, width 0.0243163; target window `(1, 7/6]` confirmed non-empty
and 6.855× wider — coherent, not vacuous). Every verifier-confirmed claim byte-untouched;
visible dated correction note citing verify_251.

**268 (PUB2R) landed on `main`** (`3f6d5d0`): PUB2 now states the honest convergent
≈4.0318 with the trend stated; the two proved-wrong banked values corrected via a CITED
companion artifact (leg 176's original JSON untouched); 259's nits absorbed; 268
explicitly checked that no downstream argument depended on 4.026 (so no escalation
fired). Its §7b verifier is in flight. Two flags it raised are queued below (269, 270).

**Slot A: leg 265 (Route-P2C) — promoted immediately, NO third review of PR #20 first.**
Reasoning recorded: verify_251 confirmed everything except one sentence at primary
source; 266 corrected exactly that sentence under its own pre-committed three-clause
gate; a formal re-review would be a third pass over the same report with no new question
to ask. 265's spec (as amended) already reads "251's report as VERIFIED" = the corrected
PR. Dispatch with the anti-pausing clause; it remains the programme's next link (ranking
rule (a)).

**Leg 249's branch (`leg/249-h2cv2-v2`): MERGE as a standalone record (this DM's call on
the orchestrator's question)** — via the normal audit path, not fast-tracked. The
correction artifact quotes 249's certified brackets, but the full exact-rational
derivation is the durable record: it is the only independent certification of leg 176's
certificate in existence, 270's pre-submission review will need to cite it, and this
repository's own discipline is that banked findings live on main, not in PR limbo.

**Reserve refresh (requested, and due — effective dispatchable was 2):**

```
### 269 — ROUTE-J176P: FIX LEG 176's JOURNAL PROSE SLIP (leg 249's out-of-territory
finding, flagged by 268 — light DOCS)
**Thesis.** Leg 249 found leg 176's own journal states 1.29e-14 where the underlying
value is 1.4296e-14 — a 9.8% prose slip, out of 268's declared territory, no banked
number involved.
**Gate.** Does the journal prose match the underlying banked value at stated precision
after the fix, with a one-line correction note citing leg 249, and no other sentence's
meaning changed?
  yes -> Bank. no -> Report which site resists and why; do not guess.
**Territory.** experiments/journal/leg_176.md (the slip site + note ONLY),
               writeup/novelty/leg_269.md, experiments/journal/leg_269.md.
**Difficulty.** light
**Independence.** DOCS-only, disjoint from everything live. LOW priority.
```

```
### 270 — ROUTE-PUB2V2: THE FULL PRE-SUBMISSION REVIEW PASS OF PUB2 (268's own flag —
the document has now been edited by legs 250, 268 across multiple cycles and needs one
coherent end-to-end read before any actual submission)
**Thesis.** PUB2 has accumulated corrections (250's inequality fix, 268's ≈4.0318 rework
+ absorbed nits) from different legs at different times. 268 itself flags that a fresh
FULL review pass is needed before submission: every number against its banked source,
every epistemic claim against what the record now supports (including 249's certified
brackets and the no-proven-floor framing), internal cross-references consistent.
**Gate.** Does every quantitative claim and epistemic qualifier in PUB2 trace cleanly to
a banked, on-main source (or 249's branch, if merged per the recommendation above), with
zero internal inconsistencies remaining?
  yes -> Bank the trace table. PUB2 is submission-ready from the record's side; actual
         submission remains the user's action.
  no -> List every failing site with its mismatch — each becomes a candidate rework item;
        escalate only if any mismatch is substantive rather than prose.
**Territory.** a review report (writeup/novelty/leg_270.md, the trace table in
               writeup/data/p2_route_pub2v2_v1_trace.json),
               experiments/journal/leg_270.md. READS PUB2; edits nothing in it — findings
               become rework items, keeping review and repair in separate legs.
**Difficulty.** standard
**Independence.** Read-only on the document. Dispatchable AFTER 268's in-flight §7b
verifier lands (no point tracing a document mid-verification). Priority: HIGH once
unblocked — it gates actual submission.
```

**THE PACKET IS NOW ASSEMBLABLE** — everything it was waiting on has landed or resolved:
251's corrected report (PR #20), the stage-V lift recommendation (drafted above), 257's
obstruction, 260's substantive-basis upgrade (DSS candidates excluded → exactly one
unconditional candidate), 262's Perelman-not-Clay caveat, 261's third closure of the
incompressible route, 256's gate-YES reproduction, and the ripened Phase-1 re-posing
question. **Recommended assembly point: when 265 (costing) lands, so the user's
construction decision has its price attached — but the orchestrator may assemble earlier
if the user asks.** The packet's contents are all already drafted in this file's recent
updates; nothing new needs DM authorship at assembly time.

**FLOOR-TABLE block updated in this same edit** (A: 266 → 265). **Floor status: 4/10
strictly (265, 236, 267, 264).**

**Canonical reserve line: reserve count 9 — legs 228, 210, 269, 270, 229, 231, 232, 233,
234.** Effective immediately-dispatchable: 3 (228, 210, 269); 270 blocked on 268's
verifier (HIGH priority once clear); 229 blocked on 226; 231-234 blocked on repairs
217/219/221/225. Next fresh leg number: **271.**

Nothing in this update lifts a ban or opens construction — 265's yes-branch still
terminates in the user's decision packet, and no output here is described as movement
toward Clay. Clay stays ~0.05%. No direction question raised.
