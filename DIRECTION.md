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
coarsening loophole leg 160 found — tightens, does not lift, the ban). **Next fresh leg
number for any future candidate is 185.**

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
