# STATUS — committed snapshot (sections 1-3 of PROGRESS.md)

*Refreshed 2026-08-11 — same orchestrator session, cycle 8e.
`origin/main` at `476e794`, merge gate green. Full detail in `PROGRESS.md`
(git-ignored, more current), `reports/ORCH_STATE.md` (full handoff detail and
institutional memory), and `experiments/JOURNAL.md` (the durable ledger).*

## ⚠ NEEDS YOU

1. **Leg 313 (SDSS) + leg 320 (MTSC) — bundled escalation packet, parked —
   packet content UPDATED this cycle, ruling still needed, not yet final.**
   The DM's own text routes the DSS ban-wording question to you rather than
   ruling on it ("the DM does not rule on ban scope"). What changed: **leg
   326 read Chae-Tsai (arXiv:1304.7414v1) in full and found it does NOT reach
   the screened Navier-Stokes object — the packet's only theorem is shown
   silent.** Deciding clause: all four of Chae-Tsai's theorems hypothesize a
   solution of their eq. (1.6), the rescaled **Euler** system (no Laplacian);
   the paper displays the Navier-Stokes rescaled equation separately and
   proves nothing about it, and the authors' own stated generalization (eq.
   2.9) only varies two real constants, never gaining a viscosity term. What
   remains in the packet: leg 260's dissolved argument, plus an empty seed
   set that leg 313 itself called "an availability fact, not an
   impossibility." **This is not yet the final packet update** — leg 326 also
   located a new, not-yet-adjudicated candidate (arXiv:2607.09619v2,
   Pineau-Vicol) that might bear on the same object; leg 330 (dispatched this
   cycle, in flight) is reading it in full to determine whether it reaches
   the screened object. The DM's directive: the complete packet — Chae-Tsai
   out, Pineau-Vicol adjudicated — should reach you together once 330
   answers, not in dribbles. **Do not rule yet on the strength of this
   partial update; a follow-up will land once 330 completes.** Both branches
   (`leg/313-sdss-v1`, `leg/320-mtsc-v1`) remain unmerged, untouched. No ban
   touched, `plan_of_record.py` untouched.

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

**Currently running, three of four slots (B vacant):**

| Slot | Leg | Route | Dispatched |
|---|---|---|---|
| A | 334 | DSSP — route-4 seeded DSS/RPO programme plan (Tier 2 ceiling; critical path) | cycle 8d |
| B | — | vacant, awaiting DM refill | — |
| C | 323 | CENV — MF1 spelling-variant census resume (real WIP from spend-limit kill, branch `leg/323-cenv-v1`) | cycle 8b, still running, no stall |
| D | 330 | PVLX — does Pineau-Vicol's Liouville theorem reach the screened object? Feeds directly into the NEEDS-YOU packet update above. | cycle 8c, still running, no stall |

Reserve: 22 undispatched (including newly drafted 339 ORC6, rank 1), 15
immediately dispatchable (339, 335, 336, 337, 338, 307, 328, 324, 322, 327,
287, 229, 293, 298, 299 in rank order). Next fresh leg number: **340**.
No ban lifted this cycle; no L1→L4 link moved.

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
