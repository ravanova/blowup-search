# STATUS — committed snapshot (sections 1-3 of PROGRESS.md)

*Refreshed 2026-08-06, ~23:52 BST — graceful, user-requested session close. Full detail in
`reports/ORCH_STATE.md`, committed in the same close.*

## ⚠ NEEDS YOU

0. **MAJOR DIRECTION CHANGE FROM THE USER — APPLIED.** PUB1/PUB2 approved as the deliverable
   (submission-blocking legs 249 in flight, 250 ready in reserve). The exit criterion is now
   a full Clay solve, applied to `plan_of_record.py` (new stage `P0` live as NEXT, stage `B`
   marked DONE, Wall 2 corrected, one ban re-posed) — all 8 `test_plan_of_record.py`
   invariants pass, merge gate green. Clay odds unchanged at ~0.05%, recorded alongside the
   goal change per explicit instruction. Full technical framing in `CONTINUATION_PROMPT.md`
   Directive 1 and `CLAY_ROADMAP.md` §7.5.
1. Route-D v11 has two independently-confirmed distinct exposures this cycle (profile_newton
   convergence flag, legs 202/226/236; v5_budget min/max selection, legs 235/247) — repairs
   in flight, neither fully landed+independently-verified yet.
2. Leg 178 (WES) — parked, self-conflicted gate, three explicit questions for the user,
   unresolved for many cycles, not actioned by either ruling this session.
3. Leg 129/188 — escalation #4 (Bowman dealiasing rule), sharpened in scope, still parked.
4. Leg 251 (Phase 0 target selection) is the single most consequential leg in flight — its
   YES branch names the object/ansatz the rest of the Clay-directed programme builds on;
   treat its output as needing DM/user sign-off before anything is built on it.

## Now

- **Session closed gracefully by direct user request**, ~23:52 BST 2026-08-06. The user will
  start the next orchestrator session manually; no self-chain `RemoteTrigger` was scheduled.
- `main` SHA at close: `06e96d2`.
- Composition floor (`ORCHESTRATION.md` §3b, added this session): at/above 3/10 at last
  check (236, 251, and one more — verify against `DIRECTION.md`'s own canonical line).
- Ten-leg roster at close (branches/worktrees, not a live-process guarantee — see
  `reports/ORCH_STATE.md` for full detail including exact worktree paths):

| Slot | Leg | Route | Branch |
|---|---|---|---|
| A | 192 | H2CV — **orphaned, needs fresh dispatch** | (uncommitted work only, see ORCH_STATE.md) |
| B | 249 | H2CV2 (verify) — SUBMISSION-BLOCKING for PUB2 | `verify/249-h2cv2-v1` |
| C | 248 | CNR2 (repair) | `leg/248-cnr2-v1` |
| D | 221 | BVRR (repair) | `leg/221-bvrr-v1` |
| E | 251 | P0T (Phase 0) — first leg of the new programme | `leg/251-p0t-v1` |
| F | 236 | RDDEP (math) | `leg/236-rddep-v1` |
| G | — | VACANT — 250/252 ready in reserve | |
| H | 228 | BHRV (verify) | `verify/228-bhrv-v1` |
| I | 210 | M2SV (verify) | `verify/210-m2sv-v1` |
| J | 226 | PNR (repair) — top priority | `leg/226-pnr-v1` |

## Legs

See table above; `reports/ORCH_STATE.md` has full narrative detail per slot, what each leg
already found in its novelty pass, and what the next orchestrator should verify (not assume)
about liveness before proceeding.
