# STATUS — committed snapshot (sections 1-3 of PROGRESS.md)

*Refreshed 2026-08-05, cycle 1, mid-cycle.*

## ⚠ NEEDS YOU

1. **`NG` entering the committed sequence is escalation #1**, applied under the user's
   pre-delegation. Reversible: swap LEG-A/LEG-C and mark `M2` as `NEXT` instead.
2. **Stage `V`'s ban-lift condition may now be permanently unmeetable.** `L1` is measured
   dead in both realizations (leg 54 coefficient basis, leg 56 collocation basis).
3. **What is the exit criterion for this project?** `NG`'s yes-branch would deliver a
   negative Tier-3-shaped result — confirm that's the kind of result you want.
4. **Escalation #4 (leg 60, Route-PQ): a banked negative result is not fully reproducible
   from its own stored data.** Both ban-bearing numbers themselves re-derive exactly; two
   other quoted numbers do not (a mislabelled comparison, a probable transcription slip).
   Branch `leg/pq-v1` pushed, not merged. See `PROGRESS.md` for full detail; your call is
   whether to fix the two prose sentences or record the disagreement as-is.

## Now

- Timestamp: 2026-08-05, cycle 1 in progress
- `main` SHA: `20622b4`
- Stop files: none present
- Ten-leg contract, live legs: 58 (NG, critical path), 59 (WV), 61 (KA), 62 (CP, gate NO,
  ledger still landing), 63 (M2), 70 (RC), 71 (CAP); LEG-G/LEG-J open pending DM's fresh
  candidates (reserve exhausted after two mid-cycle promotions).

## Legs landed this cycle

- 54/55/56/57 (prior session): MM NO, NB YES, TN NO, XS NO.
- 68 (IX): YES, mechanical — INDEX.md caught up.
- 65 (L1G): NO — weighted-l1 no-go / discrete-ball trap confirmed unpublished; verified.
- 64 (A12): split — sigma=3 at a=1/2 published (Xu Tier 1), alpha_1 remains unpublished.
- 66 (QF): YES — found a real, latent bug in `spectral_utils.py` (odd-n derivative), being
  bench-repaired.
- 69 (IA): NO — found real soundness gaps in `solver/interval.py` (subnormal range, NaN
  overflow), scoped as not affecting live operators; being bench-repaired.
- 60 (PQ): NO — escalation #4, parked (see above).

Full detail in `PROGRESS.md` (git-ignored, live) and `DIRECTION.md`.
