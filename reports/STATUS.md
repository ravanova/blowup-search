# STATUS — committed snapshot (sections 1-3 of PROGRESS.md)

*Refreshed 2026-08-11 — same orchestrator session, cycle 8b, four-slot contract.
`origin/main` at `ef2c35e`, merge gate green. Full detail in `PROGRESS.md`
(git-ignored, more current), `reports/ORCH_STATE.md` (full handoff detail and
institutional memory), and `experiments/JOURNAL.md` (the durable ledger).*

## ⚠ NEEDS YOU

Unchanged from prior cycles, nothing new this cycle:

1. **Leg 313 (SDSS) + leg 320 (MTSC) — bundled escalation packet, parked.**
   The DM's own text routes the DSS ban-wording question to the user rather
   than ruling on it ("the DM does not rule on ban scope"). Both branches
   (`leg/313-sdss-v1`, `leg/320-mtsc-v1`) remain unmerged pending your ruling.
   No ban touched, `plan_of_record.py` untouched.

(Older NEEDS-YOU items — leg 297's anchor-JSON fix, leg 280's sign-off, the
Phase-1 construction-decision packet — have since been resolved/absorbed in
earlier cycles; see `experiments/JOURNAL.md` if you need that history.)

## This cycle (8 and 8b) — what landed, what's running

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

**Currently running, all four slots:**

| Slot | Leg | Route | Dispatched |
|---|---|---|---|
| A | 331 | NLH — nonlocal machinery test (critical path) | cycle 7, still running, no stall |
| B | 329 | EGMF — arbitrary-precision recheck of B4_egm/E_egm rows | cycle 8 |
| C | 323 | CENV — MF1 spelling-variant census resume (real WIP from spend-limit kill, branch `leg/323-cenv-v1`) | cycle 8b |
| D | 326 | CTRX — resume, GAP-326-A executed first | cycle 8 |

Reserve: 22 undispatched, 14 immediately dispatchable (335, 336, 337, 338, 307,
328, 324, 322, 327, 287, 229, 293, 298, 299 in rank order). Next fresh leg
number: **339**. No ban lifted this cycle; no L1→L4 link moved.

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
