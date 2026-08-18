# WAVE 6 — CLOSE, LANDING AUDIT AND THE §3i DIRECTION CHECK

**Written 2026-08-19 at the wave-6 integration boundary (§3g step 4).** Wave 6 planned three units,
dispatched three, landed three: **`V-W5` `95cf861`, `V5` `dacc01c`, `L6` `e62c449`.** This file is
the full record; `reports/ORCH_STATE.md`'s live block carries a compressed pointer under §3j.
**I planned this wave, so I did not verify it** — `L6` is `UNVERIFIED` and a verifier for it belongs
in wave 7.

**`L6`'s LANDING AUDIT — what I checked myself rather than reading its report.** Evidence script
re-run by me from the merged tree: **30 checks, 0 failures**, and `C18` re-synthesises the field
from banked coefficients to `ρ = 1.613811231995` exactly. Territory: **7 files, all `A`, zero
modifications, zero deletions**, the only `writeup/data/` touch being its own new artefact.
**One clause of the unit's own summary I do NOT adopt:** it calls the `NO` *"a fact about the
construction, not the stopping point"*. The cap sweep (50→800) supports that against the *iteration
budget*, but **at every rung above the coarsest the reported `ρ` is attained by ONE start — the
continuation — while five independent random seeds land 10–24× higher and get monotonically WORSE
as `n_dof` grows (`J1 ≈ 6.8 → J4 ≈ 32–38`), all capped at 800 iterations.** A ladder whose every
rung starts at its predecessor's minimiser, at a budget too small to explore the added dimensions,
is **biased toward measuring "no change"**. The unit's §8.4 says the number is not the infimum and
does not claim it is — that is honest, and it is the sentence that governs. **The `NO` is a fact
about THIS CONSTRUCTION AT THIS BUDGET.** Reading (d), `UNDER-RESOURCED` with a cost, is the
**dominant** reading here, not a secondary one.

### §3i THE DIRECTION CHECK — `L6`, answered against the RECORD

1. **Did it move an L1→L4 link?** **NO.** The unit says so itself and banks `L1_to_L4_link_moved =
   "NONE"`. Clay stays ~0.05%. Route 4 having a discrete profile is not route 4 closing.
2. **What did it make FALSE?** `OPTIONS.md`'s **`L7` row** — *"needs `L6` first, ~10¹ agent-h on top
   of `L6`"*. `L6` has landed and **`L7` is not unblocked**: an interval/NK enclosure needs a
   residual small enough for a contraction to close, and this one is **1.6 against a unit-normalised
   field**. The price silently assumed that banking a profile meant banking an ACCURATE one.
   Same correction applied to **`L4`**. Also made false: the presumption that route 4's construction
   is a matter of resolution — 17.5× in `n_dof` bought **0.497 %** at the top rung.
   And it **did not** make `W4(b)` false: that `NO` is threshold-free and rests on the **exponent**,
   a class property. `c_mod = 869.288` is still not route 4's number.
3. **Does Lane L still deserve its rank ON WHAT IS MEASURED NOW?** **YES, and more clearly.** It is
   the only lane that has landed three units in a row that each narrowed it, and it is the only lane
   touching the FINAL blockers. But its **next unit changes** — see 5.
4. **Any live claim resting on an undischarged ceiling?** **Yes, one, and it is now named in
   `WALLS.md`:** every route-4 *constant* in the record still comes from the synthetic stand-in.
   `L6` was supposed to end that and **has not** — it produced route 4's own object, but not an
   accurate one. The register's other debt is NRŠ 1996 at `SECOND HAND` (`L7-src`).
5. **CHEAPEST unit that could KILL the priority lane, and why is it not next?** **It IS next now:
   `L6-b`.** `L6` named a ~10³ core-hour resolution ladder as what it lacked. That is the wrong
   next purchase. The decisive question is whether the stall is the **ansatz** or the **800-iteration
   budget**, and that is answered at FIXED `n_dof = 6720` by raising the cap to 20,000 from `L6`'s
   own banked minimiser plus two independent seeds — **~10¹ core-h from `L6`'s own timing (1,240 s
   per start at 800 iterations), two orders below the ladder.** Decisive in both directions: a
   materially lower `ρ` means the ladder measured the budget; no change means the stall is real and
   route 4's construction problem is a genuine obstruction. **Queued in `OPTIONS.md` §D.**
6. **If Lane L died tomorrow, what instead — and is it cheaper?** Lane V, whose `V5` just landed
   with the certificate CLOSING and the profile genuinely 3D, and whose W2 scope escalation is on
   the user's desk. It is **not** cheaper in the sense that matters: it does not touch W4/W5.
   Lane R is cheaper still and **never sets a wave's direction**. **No re-rank.**
7. **Audit/instrument loop? Count the last three units by kind.** `L6` **CONSTRUCTION**, `V5`
   **AUDIT**, `V-W5` **VERIFICATION** — **two of three are audit-kind**, which is the loop §3f rule
   3 warns about, even though both were obligatory (one by user ruling, one by the verifier rule).
   **Consequence, applied not noted:** wave 7 opens with construction and its Lane-L slot is
   **`L6-b`, a measurement on the object**, not another audit; `R-prof` is instrument work and is
   therefore **capped at one slot** and paired with `E-FE`, which measures the object.

**RE-RANK MADE IN THIS COMMIT (§3i q5).** Lane L's next unit is **`L6-b`**, not `L7`. Nothing else
moves: the Lane-R ranking `R4` > `R2` > `R3` stands, and the queued order `R-bank` → `E-FE` ‖
`R-prof` stands.
