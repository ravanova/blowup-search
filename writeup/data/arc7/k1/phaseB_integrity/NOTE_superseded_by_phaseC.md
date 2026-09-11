# Note beside `rebuild_cost_estimate.md` — its blocker is gone and its estimate was low

**2026-09-11.** `rebuild_cost_estimate.md` is a banked artefact of 2026-09-10 and is **not edited**
(§3f: a banked datum is never edited, only corrected beside). This note is the correction beside it.

That file costed a from-source rebuild of mathlib at **≈4 h wall on 4 cores**, offered a cheaper
**targeted 399-module** alternative, and recorded a **blocker**: `/root` had 11 GB free against a
6.6 GB build output, so a second tree did not fit.

All three of those are now historical:

| its statement, 2026-09-10 | what happened |
|---|---|
| full rebuild ≈4 h, not run | **RUN on 2026-09-11** — `K1` phase C, 11578 s (3.2 h) on 12 cores |
| targeted 399-module alternative | **never needed, never run** — the full rebuild subsumes it |
| blocked: a second tree does not fit | **unblocked** by the operator freeing space |
| disk: 6.6 GB of build output | **an underestimate** — the real tree measured **28.5 GB**; provision ~30 GB |

The rebuild's result: `lake exe cache get` never invoked, **8370 `Built Mathlib.` lines, 0 replayed**,
and both theorems returned `[propext, Classical.choice, Quot.sound]` byte-identically to the cached runs.
Reading **MATCH** — the cached oleans were not load-bearing.

Full record: `writeup/data/arc7/k1/phaseC/phaseC.json`, `writeup/CORRECTIONS.md` §81 and §81a,
`writeup/7_confirmation/TECHNICAL_CONFIRMATION.md` §3b.
