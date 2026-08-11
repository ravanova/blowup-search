# STATUS — committed snapshot (sections 1-3 of PROGRESS.md)

*Refreshed 2026-08-12 — same orchestrator session, cycle 9f (user's
ceiling-raising programme ANSWERED: S1 DIES, ceiling stays Tier 2).
`origin/main` at `d0248c6`, merge gate green. Full detail in `PROGRESS.md`
(git-ignored, more current), `reports/ORCH_STATE.md` (full handoff detail and
institutional memory), and `experiments/JOURNAL.md` (the durable ledger).*

## ⚠ NEEDS YOU

1. **Leg 313 (SDSS) + leg 320 (MTSC) — bundled escalation packet, parked —
   packet update now COMPLETE, ready for your ruling.** The DM's own text
   routes the DSS ban-wording question to you rather than ruling on it
   itself ("the DM does not rule on ban scope"). Both threads that were open
   are now closed:
   - **Leg 326** read Chae-Tsai (arXiv:1304.7414v1) in full and found it does
     NOT reach the screened Navier-Stokes object — the packet's only theorem
     is shown silent. Deciding clause: all four of Chae-Tsai's theorems
     hypothesize a solution of their eq. (1.6), the rescaled **Euler** system
     (no Laplacian); the paper displays the Navier-Stokes rescaled equation
     separately and proves nothing about it, and the authors' own stated
     generalization (eq. 2.9) only varies two real constants, never gaining a
     viscosity term.
   - **Leg 330** read the candidate leg 326 flagged, Pineau-Vicol
     (arXiv:2607.09619v2), in full and found it ALSO does not reach the
     screened object. Deciding clause, verbatim: "There exists λ̲ =
     λ̲(C_U,0) > 1, such that if 1 < λ < λ̲, then U ≡ 0" — the paper's own
     proof caps that window near 1 (WLOG λ̲ ≤ e^{1/2} ≈ 1.6487, smallness
     requirement (1+α²)S < 2 log λ̲ ≪ 1, final choice "sufficiently close to
     1"), while the screened object is specified with λ significantly larger
     than 1. Two independent reinforcements: Pineau-Vicol's own text says
     this DSS theorem restates Chae-Wolf's (already screened via leg 253);
     and their weak-L³-at-every-phase bound carries its own open conditions
     (non-explicit constant, unclosed pressure-decay positivity), recorded
     honestly rather than suppressed. One genuine corner where the paper
     touches large λ exists (an RSS sub-locus reachable only above λ ≥
     10^21935.3 under leg 262's most favorable constants) — recorded as
     indicative, not certified, and does not change the verdict.

   **What remains in the packet, now final:** leg 260's dissolved argument,
   plus an empty seed set that leg 313 itself called "an availability fact,
   not an impossibility" — no theorem in the literature searched so far
   reaches the screened object. Both branches (`leg/313-sdss-v1`,
   `leg/320-mtsc-v1`) remain unmerged, untouched. No ban touched,
   `plan_of_record.py` untouched. **This is the complete packet — your
   ruling on the DSS ban-wording question is the only thing this is waiting
   on.**

2. **RESOLVED BY MEASUREMENT — leg 340 (EGRB) answered leg 329's C4 reading
   question, and the answer is an identity, not a measurement.** Leg 340
   re-derived the bound with truncation fully controlled, in exact
   rational+π arithmetic (substitution X=tan(θ/2): every relevant integral
   collapses to R=(r1+q1π)/(r2+q2π) exactly, no floats in the exact path).
   At all 19 ladder rungs, for both `B4_egm` and `E_egm`, R = −1/2 EXACTLY:
   bound=1/2, margin=exactly 1e-9, dependence on the truncation parameter=
   exactly 0, enclosure width 1.4e-59 — against a measured eigensolve spread
   of 1.927e-05/2.697e-05, reproducing leg 329's own banked
   3.853e-05/5.394e-05 relative spreads. Structural cause: `Sym(B) = -G/2`
   entry-by-entry, because the nonlocal Hilbert term vanishes identically on
   `T2_egm` while `D_φ ≡ -1/2`. Eleven controls pass; six able to fire
   against, notably `A4_chen_hou` (non-constant `D_φ`) gives -0.5001506 and
   FAILS the ceiling — the instrument is not a tautology of the code itself.
   **The gate answers YES on this bound.**
   - **MANDATORY SECOND READING, pre-registered before the run (novelty
     §7e), and this is the part that needs your ruling**: since R=-1/2 is an
     identity, clause 5 is a TAUTOLOGY on this class and cannot come out
     otherwise. A flip of leg 178's original NO would be a flip ON AN
     IDENTITY, not a measurement. The question for you: does a tautological
     pass flip 178's substance (escalation #3's parked yes-branch fires,
     report-and-escalate), or does the fact that clause 5 cannot fail on this
     class void the clause's evidential weight here entirely, leaving 178's
     NO standing on other grounds?
   - The leg explicitly declined to adjudicate this itself, deferring to you
     per the standing cycle-8e ruling that this class of call is yours, not
     the DM's or the leg's. The DM's cycle-9f ruling adds nothing decisional
     either, endorsing the orchestrator's direct escalation and noting only
     that exact arithmetic decided the knife edge at exactly 1/2 — neither
     prior reading's naive victory, since the "bound" margin was real but is
     the slack itself, and the original "agreement test" fired on eigensolve
     float noise.
   Files: `experiments/journal/leg_340.md`, `writeup/novelty/leg_340.md`,
   `writeup/data/p2_route_egrb_v1.json`. Landed `165a402`.

3. **NEW — the ceiling-raising programme's answer: S1 DIES, route 4's ceiling
   stays Tier 2. A resource-commitment decision now sits on top of this,
   yours to make.** Leg 341 (ALGW) found that leg 260's algebraically
   weighted space — the "namable fourth space" the stage-V ban's lift
   condition asks for — has already been realized in three independent
   lanes, each already dead by a different mechanism (sup-norm/collocation:
   6.04x short at theoretical optimum; coefficient/ℓ¹-weighted: no window at
   any exponent, re-attempt already banned; origin-conjugated/Mellin: dies
   orthogonally, no transfer). No lift-condition packet was assembled; the
   deferred §3 build is never drafted; leg 334's clause (a) closes
   CLOSED-NO. **No ban is lifted or touched by this — that ruling stays
   yours regardless, per your own directive.**
   - Leg 342 (SEED) separately found route 4 has no screen-passing seed
     today, but named one creation path: retargeting PINN/KAN machinery at
     the true 3D NS DSS ansatz, costed at ≈35 legs.
   - Leg 344 (PKLR) sharpened that estimate's inputs with a controlled
     literature inventory: the "Hou PINN/KAN machinery" label was a
     mislabel (KAN was never demonstrated on NS/Euler anywhere), and named a
     stronger retarget base (arXiv:2509.14185, DeepMind+Buckmaster+
     Gómez-Serrano, Sept 2025) whose own authors name boundary-free 3D Euler
     as their next open problem. The ≈35-leg estimate is unmoved
     numerically but its largest risk (the DSS/time-periodic gap) is now
     confirmed against two independent literature lines instead of one.
   - **The decision for you**: 342/344's 35-leg creation path is now costed
     against a route whose parent lift condition already failed (S1 dies).
     Spending those 35 legs would raise route 4's *seeding* completeness,
     not its Tier-2 ceiling — the ceiling stays Tier 2 regardless, per 341's
     finding, unless a different lift condition is found. Is that 35-leg
     spend still worth it under this programme, or should it be shelved?
   Files: `experiments/journal/leg_341.md`, `writeup/data/p2_route_algw_v1.json`,
   `experiments/journal/leg_342.md`, `writeup/data/p2_route_seed_v1.json`,
   `experiments/journal/leg_344.md`, `writeup/data/p2_route_pklr_v1.json`.
   Landed `782a310`, `fc65c1e`, `3ec2516`.

(Older NEEDS-YOU items — leg 297's anchor-JSON fix, leg 280's sign-off, the
Phase-1 construction-decision packet — have since been resolved/absorbed in
earlier cycles; see `experiments/JOURNAL.md` if you need that history.)

## This cycle (8d) — what landed, what's running

- **Leg 331 (NLH)** — gate **NO**, critical path. For the first time the
  (iv_a) obstruction is **measured**, not just named, and its mechanism is
  **reframed**: Breden-Chu's machinery breaks against an algebraic tail
  (predicted exponent 1+2a+2m, measured 1.507674/2.012245/2.517908 against
  1.5/2.0/2.5) meeting a Gaussian weight e^{x²/4} — nonlocality only enters as
  the tail-producer, not the direct cause Remark 40 names. Z1<1 crossing
  bisected to width 6.1e-06 (t*≈0.30–0.52 depending on n, α). Two of the leg's
  own five pre-registered predictions were refuted and recorded as such.
  Reframing routed to the DM, not adjudicated by the leg itself.
- **Leg 329 (EGMF)** — gate **NO**. The DM's thesis (float64
  catastrophic-cancellation artifact in `clause_quad_stable`) is confirmed as
  arithmetic — MP repairs the pointwise contraction by 6.1e+06/4.4e+06 and
  both `B4_egm`/`E_egm` pass `clause_quad_stable` naively — but two
  pre-registered controls able to fire against a flip both fired (C5: rcond
  ladder moves the gap against tolerance; C4: MP Rayleigh disagrees with the
  eigensolve at exactly the magnitude `cond(G)·eps` predicts). The obstruction
  moved, from a pointwise cancellation to a float64 whitened
  assembly/eigensolve the patch can't reach. Escalation #3 stays parked.
  **C4's disposition was flagged unadjudicated, now RULED (cycle 8e, see
  below): the literal pre-registration governs, 329's NO stands.**
- **Housekeeping**: `.gitignore`'s `.venv/`/`venv/` patterns (trailing slash)
  didn't match a *symlink* named `.venv`, so one landed on `main` by accident
  during leg 329's run (self-caught and removed by the leg). Fixed directly by
  the orchestrator at `fd43ac8` (added slash-less variants); endorsed by the
  DM at cycle 8e.

**DM rulings, both integrated (cycle 8d by fast-forward, cycle 8e by rebase
onto the intervening `.gitignore` commit — clean, no conflicts), no
unintended deletions confirmed by diff both times:**

- **Cycle 8d** (`f9321b5`): absorbed 331 NO, folded the tail/weight reframing
  into leg 334's plan clause (a) as a collision it must resolve or route to
  the user (leg 332's vorticity lane lands exactly on the Gaussian weight;
  leg 331 shows that weight intolerant of the tails nonlocal operators
  produce); drafted leg 339 (ORC6, gated adjudication of the closed-three-ways
  sites, rank 1) for the deferred closure-#6 correction; refilled slot A←334
  DSSP now that both its preconditions (331 AND 332 landed) are satisfied.
- **Cycle 8e** (`476e794`, rebased from `dm/cycle8e-direction` at `b4eb03f`):
  **ruled the C4 pre-registration defect — the literal pre-registration
  governs, 329's NO stands**, on three stated grounds: (a) the margin can't
  carry the claim — the 5.19e-18/1.42e-18 bound is thirteen orders of
  magnitude smaller than the 3.85e-05/5.39e-05 truncation sensitivity C5
  itself measured, and a Rayleigh quotient one-sides the *truncated matrix's*
  eigenvalue, not the operator clause 5 is actually about; (b) these rows sit
  at EGM's published +1/2, a knife edge, and the standing 318/302 lesson is
  that knife edges are decided in exact/enclosed arithmetic, never by which
  side a float lands on; (c) overriding a fired control in the hoped-for
  direction is exactly what novelty §7d forbids — the leg's refusal to do so
  is endorsed by name. The bound reading isn't discarded: it earns its own
  gate as **leg 340 (EGRB), drafted at reserve rank 1** — does a
  truncation-controlled version of the bound (re-derived at every C5
  ladder rung and/or with an explicit truncation-error enclosure) hold
  clause 5 with a margin that survives the ladder? Yes-branch inherits 329's
  report-and-escalate path; no-branch classifies TRUNCATION-LIMITED vs
  KNIFE-EDGE at measured width. Escalation #3 stays parked until 340 answers.
  Refilled slot B←339 ORC6 (rank 1 per cycle 8d, dispatched now, per the
  reason that 334 is in flight in slot A this leg-cycle and shouldn't be
  written against sites whose adjudication is left pending).
- **Leg 330 (PVLX)** — gate **YES-(ii)**: Pineau-Vicol's theorem does not
  reach the screened object. See the completed NEEDS-YOU packet above for the
  full finding. Landed at `5496bbc`; territory audited clean (exactly its 3
  declared files, leg 313's packet file/branch untouched). **This closes out
  the last open thread in the NEEDS-YOU packet — ready for your ruling now.**

**Slot D now vacant** (330 landed) — awaiting DM's next ruling.

## Prior cycle (8 and 8b) — what landed, what's running

**Landed and audited clean, all pushed to `main`:**

- **Leg 221 (BVRR)** — gate YES on the repair itself: 0 of 256233
  `odd_field_x_slope` calls moved because of the repair. But it flagged one
  real, unresolved gap *outside its own territory*: `spike1_stepC_gate.json`'s
  committed 2026-07-25 artifact does not reproduce with the repair absent
  (α: -0.3350763095 → -0.3793563731, a 13.2% shift, two gate predicates flip).
  221 explicitly declined to fix this and named the successor leg as the
  resolution path. **Consequence:** leg 307 (TSCX)'s precondition — "struck if
  221's gate resolves the flag, else dispatchable" — resolves to
  **dispatchable**, confirmed independently by both the orchestrator's direct
  journal read and the DM. 307 now ranks directly after leg 338 in the reserve
  queue. The same gap is also the subject of correction leg 335 (S1GR,
  drafted, not yet dispatched).
- **Leg 333 (SHELL)** — gate **NO**. 3D Navier-Stokes sits at dissipation
  degree α=2/5 in the Katz–Pavlovic dyadic hierarchy (per Cheskidov's own
  introduction, read from the e-print source), strictly inside that
  hierarchy's undecided window (1/3, 1/2). Rate-limited queries recorded as
  refusals-to-measure, nothing banked from them.
- **Leg 332 (VORT)** — gate **NO**. The Leray-obstruction argument of legs
  257/261 does **not** survive re-derivation in the vorticity formulation on
  H²(µ): it fails at step S4, because the entire non-vanishing tail lives in
  `grad v`, i.e. in `ker(curl)` — curl annihilates it. Positive content banked
  and bound into leg 334's plan by the DM: the vorticity nonlinearity is a
  bounded map, and the reconstructed Biot-Savart velocity, despite leaving the
  weighted space, lands in L³(ℝ³) — precisely the NRS/Tsai admissibility
  hypothesis, the same wall that already killed leg 309's claimant. Leg 334's
  function-space clause must now state its target's position relative to that
  wall up front. No escalation; pre-registered NO branch.

**DM rulings, both integrated by fast-forward, no unintended deletions
confirmed by diff:**

- **Cycle 8** (`dedfd57`): absorbed 221 YES and 333 NO; refilled slot B←329
  EGMF, slot D←326 CTRX (amended to run GAP-326-A first — the controlled zero
  on the Chae-Tsai author-conjunction query IS a measurement, banked as
  absence, not struck as broken methodology); drafted four correction legs
  (335 S1GR, 336 C305, 337 C318, 338 LCB1) from verifier findings; held the
  Palasek item with named revisit triggers; asked the orchestrator to resolve
  307's flag-state (done in cycle 8b, see above).
- **Cycle 8b** (`ef2c35e`): absorbed 332 NO, bound its two facts (obstruction
  is velocity-pressure-specific; vorticity lane measured OPEN but carries its
  own NRS/Tsai second wall) into leg 334's plan; refilled slot C←323 CENV
  (resume); confirmed 307 dispatchable; deferred an over-read-closure
  correction (#6) to leg 331's landing, so one correction leg can address both
  measured sites on both answers rather than splitting the evidence across two
  legs.
- **Cycle 8c** (`d38de3f`): absorbed 326's YES-(ii) (Chae-Tsai does not bite,
  see NEEDS-YOU above); endorsed leg 326's two self-corrections (GAP-326-A —
  the DM's own cycle-8 characterization of a controlled zero as a
  "term-conjunction artefact" is corrected to "an unbanked measurement,"
  now banked with its control: exactly 1 of 4 control-set records is
  reachable by {nonexistence, Liouville, rigidity} — Pineau-Vicol; GAP-326-B —
  a prior "new to this repository" claim about Pineau-Vicol was false, leg
  262 had already read it four days earlier); refilled slot D←330 PVLX,
  jumping ahead of correction legs 335-338 on a three-part stated
  justification (route-4 de-risk timing, packet completeness for the user,
  floor 4/4 vs 3/4 with a corrections pick); directed the NEEDS-YOU summary
  refresh reflected above.

**Landed this cycle, not yet superseded:** leg 326 (CTRX) — gate **YES-(ii)**
at `c541cdb`. See NEEDS-YOU above for the full Chae-Tsai finding; territory
audited clean (exactly its 3 declared files).

## Cycle 9–9d — the user's ceiling-raising programme, and three more landings

**A new standing priority arrived from the user directly (2026-08-11, "THE
CEILING-RAISING PROGRAMME"): leg 334 was the only Clay-directed route in the
queue and its ceiling is Tier 2 by design — a route that cannot produce a
proof cannot produce a Clay solve. The programme adds "the missing half":**
leg 341 (ALGW) scopes whether leg 260's algebraically-weighted space is the
"namable fourth space" the stage-V ban's own lift condition asks for — if it
escapes the three-realization death AND the CAP apparatus has a coherent
formulation there, the evidence packet goes to the user for a ruling (the leg
itself lifts nothing). A deferred §3 "build" is gated entirely on 341's
report and the user's ruling; if it lands, route 4's ceiling moves Tier 2 →
Tier 3 — the sole justification for the programme. Leg 342 (SEED) scopes
route 4's seeding problem independently. §5 ownership is ruled: leg 341 owns
the Gaussian-weight-vs-algebraic-tail question; leg 334's clause (a) narrows
to consuming 341's answer.

**Leg 339 (ORC6) landed gate YES** — the "closed three ways" claim is
adjudicated on both measured candidate triples (the record never enumerated
which triple it meant): width STANDS (the Grade-A/fluid cell is still empty,
on leg 174's target-absence ground — neither leg 331 nor 332 measures width),
but the GROUNDS are over-read: (iv_a) MISATTRIBUTES (the kill survives, but
its stated mechanism has drifted twice under a fixed verdict) and the Leray
obstruction OVERSTATES (leg 332 measured it velocity-formulation-specific,
failing at step S4). Corrected in place in `JOURNAL.md` and banked as
over-read closure #6 in `CORRECTIONS.md`. DM cycle 9c absorbed this in full,
including applying the two `DIRECTION.md` site corrections itself.

**Leg 323 (CENV) landed gate NO, and this time it's earned** — the pre-kill
NO was not: the DM's cycle-8b re-check condition caught that the pre-kill
rows were mislabelled (a runner bug built each variant job's id from the
BASE query while submitting the variant), not stale. Fixed structurally
(`query_sent` parsed from the actual URL, curation refused on any mismatch).
Clean re-run: hyphen-variant spelling is robust on `abs:` (16/16) but NOT on
`au:` (a new instrument finding, MF4, now standing text in
`CONTINUATION_PROMPT.md` — compound author-name queries are a false-negative
generator, confirmed three independent times). Census screen: 0 of 51 novel
ids clear all four of leg 303's clauses; §0c UNBLOCKS on the corrected
instrument.

**Leg 334 (DSSP) landed gate YES on all four clauses** — the route-4
programme plan itself, Tier 2 ceiling stated and mechanically checked in
every one of nine drafted bricks. Clause (a) was drafted before the user's
§5 ruling reached it; once relayed, the leg retained and re-labelled its own
weight-collision analysis as context offered to leg 341 (OWNED-BY-341-
PENDING, both branches named) rather than asserting a conclusion. Clause (c)
(seeding) re-measured independently, still empty — this is now leg 342's
starting point. Independent gain: vorticity of a Type-I profile lands in
*unweighted* L²(ℝ³), a second argument for the vorticity formulation
alongside leg 332's.

## Cycle 9e-9f — four more landings, three of four slots freed then refilled

**340 (EGRB), 342 (SEED), 341 (ALGW), and 344 (PKLR) all landed this window
— see NEEDS-YOU items 2 and 3 above for the findings.** All four audited
clean (territory diffs exactly the declared files, no ban/DM/sibling-leg
files touched) and independently merge-gate re-verified PASS before being
reported to the DM. DM cycle 9f absorbed 340 and 342 (340's user escalation
endorsed, 342's 35-leg path recorded and routed into the same decision
packet, not drafted on DM authority) and refilled under a stated §3b floor
bind — the entire dispatchable reserve was non-eligible corrections/audit
work, so filling both vacancies from it would have put the floor at 1/4,
below §3b's hard 2-of-4. Slot D got leg 336 (C305, corrections rank 1); slot
B got a fresh floor-eligible leg 344 (PKLR) drafted specifically to feed the
same 341-landing decision packet.

**Leg 336 (C305) landed gate YES** — two claim-bearing corrections to leg
305's prose (elasticity ranking corrected, one of seven "capped rows"
adjudicated inert-by-construction rather than genuinely capped), SHARP
verdict unmoved by either. Two downstream repeat-sites flagged
(`experiments/JOURNAL.md:5018`, `writeup/INDEX.md:124`), not edited
(out of leg 336's territory).

**Currently running (three of four slots vacant, awaiting DM refill):**

| Slot | Leg | Route | Status |
|---|---|---|---|
| A | 335 | S1GR — resolves the 221 flag/repair gap | cycle 9e, running |
| B | — | vacant (344 PKLR landed `3ec2516`) | — |
| C | — | vacant (341 ALGW landed `782a310`) | — |
| D | — | vacant (336 C305 landed `d0248c6`) | — |

Reserve and next fresh leg number as of the DM's cycle 9f ruling: 19
undispatched, 12 dispatchable, next fresh number **345**. No ban lifted this
window; no L1→L4 link moved. Awaiting the DM's next refill ruling for
slots B/C/D.

## Context — the ten-to-four downsize and the spend-limit kill

This run's contract was reduced from ten parallel legs to four by the user
(2026-08-11), and shortly after, a monthly account spend limit terminated all
ten legs of the prior cohort mid-flight. Real WIP was salvaged and preserved
(`ae7ca2c`) before the four-slot contract was rebuilt from scratch. Legs 329
and 323 in the current roster are resumes carrying real pre-kill WIP forward,
not fresh starts.

## Stop

| File | Status |
|---|---|
| `STOP-NOW` | absent |
| `STOP` | absent |
| `PAUSE` | absent |
