# PRICE — `E`'s field ensemble, and whether this container can survive it

**Priced 2026-08-18 by the Conductor on user instruction: PRICE, DO NOT QUEUE.** Nothing here is
a proposal, a slot, or a claim on a wave. It is two numbers and the evidence behind them.

## 1. What it is, and why it is the honest fix

`E`'s structural limit (`E-iv`): **a published row supplies `(T, s)`; it does not supply a field.**
`E` ran **8 rows × 2 arms, one field each** — so every arm's result is **one draw**, and a null from
one draw cannot separate "this row has no orbit" from "this draw missed it". The fix is not more
rows and not more attempts; it is **independent fields per (row, arm)**.

**Shape:** 8 rows × 2 arms × **10 independent fields = 160 attempts.**

## 2. The price, re-derived rather than quoted

`E`'s own measured per-attempt cost, from the landed artefact (`p2_prog_r4_e_v1.json`, journal
`prog_r4_e.md` §§ on `D5`):

- **32,718.334 core-seconds / 16 attempts = 2,044.90 core-s/attempt** = **0.5680 core-h/attempt**.
- The commissioning model predicted 2,053.44 core-s/attempt; **`E` came in 0.4% UNDER** (ratio
  `0.9958`). The model is trustworthy at this scale because it was *checked against the outturn*.

**160 × 0.5680 = 90.9 core-hours.** This confirms the journal's **~91 core-hours** from the
per-attempt figure rather than inheriting it. At 8 workers and `E`'s measured pool utilisation
band (0.93–0.98, from `R0`), that is **≈11.6–12.2 h wall**; at 10 workers, **≈9.3–9.8 h**.

**Not included, and it is not small:** `U2`'s gitignored `T = 1e5` DNS archive that the seeding
path reads **died with the container** (2026-08-14). Regenerating it is **≈3.4 h of DNS before a
single attempt runs**. So the true door-to-door figure is **≈91 core-hours + a ~3.4 h serial
prologue**, and the prologue is *not* parallel over the 160 attempts.

## 3. Can the container survive a job this size? — the W7 datum

**Yes, on the record's own evidence, and the binding risk is not size.**

**Jobs this container has already completed** (banked, `p2_prog_r4_r0r1_v1.json` §R0):

| campaign | attempt CPU | pool reserved | workers | wall | utilisation |
|---|---|---|---|---|---|
| `PROG-R4` `U3` | **134.45 core-h** | 144.69 core-h | 10 | **14.47 h** | **92.9%** |
| `PROG-R4` `U5` | **56.01 core-h** | 57.04 core-h | 8 | **7.13 h** | **98.2%** |

**The field ensemble (91 core-h, ~11.6 h wall at 8) is SMALLER than `U3`, which finished.** Size,
by itself, is therefore not the objection — this container has completed a 14.5-hour, 145-core-hour
pool at 93% utilisation.

**But every loss in the record has a cause that is not size**, and two of them would hit a job of
exactly this shape:

| date | loss | cause |
|---|---|---|
| 2026-08-06 | **13 agents at once**, ~10 min in | the **orchestrating session** was judged idle and suspended — not 13 failures. Fixed by the §9f heartbeat |
| 2026-08-07 | **5 agents** | account-wide **usage limit** mid-run |
| 2026-08-14 | **`E` killed by the host TWICE** | and after the second kill **8 of 16 checkpoints were gone anyway** — they lived in a **gitignored** working directory and **the container was replaced** |
| wave 3 (2026-08-18) | **3 of 4 units** | host exits. **The only one that left anything had committed** (`L2`/leg 397: pre-registration survived, fully resumable) |
| wave 2 | **5 workers** | same class |

**Reading:** the record contains **no instance of a job dying because it was too big**, and
**several** of jobs dying because (a) the orchestrating session was suspended or limited, or (b)
partial results were written where a container replacement destroys them. `U3` and `U5` are the
control: long, large, and they finished.

**So the survivability answer is conditional, and the condition is cheap:**

1. **Per-(row, arm, field) partials committed to a TRACKED path** — `writeup/data/`, not a
   gitignored working directory. The 2026-08-14 lesson is explicit: a gitignored checkpoint is a
   **within-run** optimisation, **not a cross-container** one.
2. **Push during the run**, not at the gate. Wave 3 proved this twice in one wave.
3. **Resumability by construction** — a relaunch must skip completed (row, arm, field) triples by
   reading the tracked partials, so a host exit costs the in-flight attempts only (≈0.57 core-h
   each), not the campaign.
4. The **~3.4 h DNS prologue banked as an artefact the first time it is paid**, or it will be paid
   again by the next container.

With (1)–(4) the expected cost of a host exit is **one worker-attempt**, ~0.57 core-hours out of
91 — **0.6%**. Without them, a host exit at hour 10 costs the entire campaign.

## 3b. AMENDED 2026-08-19 — QUEUED, and the price is an OUTTURN, not a FLOOR

**The "price, do not queue" steer is WITHDRAWN by the user as over-cautious**: ~11.4 h wall at 8
workers is one overnight run and defers nothing. The ensemble is **queued** as `E-FE`
(`writeup/waves/WAVE7_PLAN.md` §B), behind `R-bank`, which makes it shardable.

**And the 90.9 figure is honest as a MEASUREMENT of what `E` cost — it is not a floor.** It
inherits `95.389 s/epoch`, a constant **no unit in 403 legs has ever profiled**. A Conductor smoke
test finds the inner loop's transforms flat in cost from `N = 24` to `N = 32` — the signature of
**per-call overhead**, paid 20 times per RK4 step. If `R-prof` (§C) finds a factor, **this number
and every cost figure in `OPTIONS.md` move together.**

## 4. What this does NOT say

- It is **not queued**, not ranked, and not in any wave. Nothing in `STATE.md` or `OPTIONS.md`
  moves because of this file.
- **91 core-hours buys statistics on a null, not an orbit.** It converts "one draw found nothing"
  into "ten draws found nothing", which is a **stronger negative**, not a positive. Under §3d it
  would let a null be stated at the scale the question is posed at instead of `UNDER-RESOURCED`.
- It does **not** touch the resolution limit: the same 160 attempts at `N = 48` cost **~730
  core-hours** plus an unbudgeted `T = 1e5` DNS, and that is where the published rows' own
  discretization actually lives.
