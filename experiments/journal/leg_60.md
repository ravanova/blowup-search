# Leg 60 — Route-PQ: the two negative findings that had no quartet

**Agent:** LEG-F. **Branch:** `leg/pq-v1`. **Date:** 2026-08-05. **Difficulty:** light.
**Outcome:** the gate answers **NO on its literal terms** — 3 of 114 quoted numbers do not
re-derive — so this leg **parks under ORCHESTRATION.md §8 escalation #4** and pushes its
branch only. **The two numbers the two standing bans actually rest on re-derive exactly.**

---

## What was asked

DOCS flagged that Route-PORT v1 (leg 46) and v2 (leg 47) each had a runner and curated data
but no `*_evidence.py` and no registered figure, while both are cited as settled in the ban
list. The gate, verbatim:

> *"Do the evidence scripts re-derive every number Route-PORT v1's and v2's prose quotes,
> from the stored curated data, to the precision the prose states?"*

## What was built

* `experiments/p2_route_port_v1_bordered_evidence.py` → `writeup/figures/fig59_route_port_v1.png`
* `experiments/p2_route_port_v2_reach_evidence.py` → `writeup/figures/fig60_route_port_v2.png`

Neither recomputes anything: both read only `writeup/data/p2_route_port_v{1,2}_*.json`.
Beyond drawing the figure, each runs a **ledger** over every number its writeup quotes
(`writeup/README.md` items 46/47 and the two `TECHNICAL_P2_ROUTEPORT_V*.md`), and prints a
per-number PASS/FAIL line with the magnitude of the disagreement.

**"To the precision the prose states" was made non-negotiable rather than a knob.** Every
quoted value is passed to the ledger as the *string that appears in the document*, and the
tolerance is derived from that string: **half a unit in its own last digit**. A document
that writes `1.831e-01` claims four significant figures, so the check accepts exactly what
rounds to `1.831e-01`. Where the prose writes a tilde (`~5200×`, `~70×`, `~3×`) the claim is
read as that many significant figures and no more. There is no global relative tolerance
anywhere in either script, which is what stops the check from being tuned until it passes.

The v2 script deliberately **re-fits** the three slopes from the ladder with `np.polyfit`
instead of reading the stored `verdict` fields, and then checks the re-fit against the
stored field as a separate row — so the ban-bearing number is genuinely re-derived, not
transcribed twice.

## Result: 111 / 114

| writeup | rows | re-derive | substantive | last-digit |
|---|---|---|---|---|
| Route-PORT v1 (leg 46) | 59 | 57 | 1 | 1 |
| Route-PORT v2 (leg 47) | 55 | 54 | 1 | 0 |

**The ban-bearing numbers are exact.** Both bans keep their evidence:

* `distance / r_max = 1.548e+08` against the quoted **`1.55e+08`** — 1.53e+05 absolute out
  of a 5e+05 half-ulp, i.e. it rounds to the quoted value with room to spare. Clause **P6b**
  holds, 7/7 clauses hold, the ball is `[2.97e−12, 1.18e−09]` against a distance of
  `1.831e−01`.
* the wrong-sign trend **`+0.4703`** decades per unit `ρ`, re-fitted: `+0.470334`, against a
  gate of `−0.05`. Its two constituents also re-fit: distance `−0.019575` (quoted `−0.0196`)
  and `r_max` `−0.489909` (quoted `−0.4899`). Every cell of v2's five-rung table re-derives,
  as does the "rises over the last three rungs" claim (`0.1836 → 0.2049 → 0.3306`).

## The three that do not, with magnitudes

**(1) SUBSTANTIVE — v2 §2 and README item 47: "the gap at `ρ = 10` is 28× worse than at
`ρ = 6`."** The stored ladder gives `4.374e+09 / 6.944e+07` = **62.99×**. The quoted 28×
is the **`ρ = 8 → 10`** factor (`4.374e+09 / 1.553e+08` = 28.16×), so the sentence names the
wrong baseline. Magnitude: 35 absolute, **relative 1.25**, 70 half-ulps out. Direction: the
prose **understates** its own effect by 2.25×. The ban ("closing the truncation gap by
extending the domain") cites the *slope*, not this comparison, and the slope is exact — so
the ban is not at risk from this, but a banked document says 28 where its data says 63.

**(2) SUBSTANTIVE — v1 §2.1: the reach table's `ρ = 8` row quotes `−2.541222`.** The reach
ladder in `C_extrapolation/reach` is at fixed `n = 301` and holds **`−2.541024`** there;
`−2.541222` is the `n = 201` value from §2's *resolution* table on the same page. Magnitude:
`1.98e−04` absolute, **relative 7.8e−05**, 395 half-ulps at the six decimals quoted. Rows
`ρ = 6, 7, 9` of the same table re-derive to all six decimals, and the fitted slope
`−0.437`, the extrapolated limit `−2.511926` and its `2.09e−04` error vs CHL are all
unaffected — the stored ladder that produced them is internally consistent. This is a
transcription from the adjacent table, not a wrong measurement.

**(3) LAST-DIGIT — v1 §2: the `n = 1201` row prints `1.168%`** for a stored
`1.16850%`, which rounds to `1.169%`. Magnitude `5.03e−06` absolute, relative `4.3e−04`,
1.0 half-ulps — the last digit was truncated rather than rounded. Noted for completeness;
it changes nothing, including the headline `1.17%`, which is this same row to three digits
and does re-derive.

## Why this parks instead of landing

The gate's no-branch is pre-committed and says: *park, do NOT edit the prose to match, and
escalate — a ban resting on an unreproducible number is the user's call.* The literal gate
asks about **every** number, and three fail, so the honest answer is **no** and the branch
is pushed without merging. Softening the gate after seeing the result is exactly the failure
mode the pre-commitment exists to prevent.

**But the escalation should be read with its magnitudes, not as a boolean.** No banked
*finding* failed to reproduce. Two bans were checked and both keep their evidence intact.
What failed is one mislabelled baseline in a comparison sentence and one row copied from the
table above it. The decision the user actually faces is narrow: **fix the two sentences in
`TECHNICAL_P2_ROUTEPORT_V1.md` §2.1 and `TECHNICAL_P2_ROUTEPORT_V2.md` §2 (plus README item
47's "28×") to match the data, or record the disagreement.** A leg may not make that edit
under the pre-committed protocol; the numbers are banked.

Note the direction of both substantive errors: the v2 one makes the negative finding look
**milder** than it is. Nothing here makes a banned lane look more promising.

## One piece left outside this leg's territory

DIRECTION.md's leg-60 territory does not include `writeup/build_figures.py`, so the two new
figures are **not** registered in its `P2_EVIDENCE` list. The remaining change is two lines,
alongside the identical entries legs 54–57 already have:

```python
    "../experiments/p2_route_port_v1_bordered_evidence.py",     # fig59 -- Route-PORT v1 (leg 46)
    "../experiments/p2_route_port_v2_reach_evidence.py",        # fig60 -- Route-PORT v2 (leg 47)
```

Both scripts already run standalone and are listed in `writeup/README.md`'s reproduce block,
so the figures rebuild from committed data today; only the sweep-everything entry point is
missing them. Left to integration rather than taken outside territory.

## Files

* `experiments/p2_route_port_v1_bordered_evidence.py` (new)
* `experiments/p2_route_port_v2_reach_evidence.py` (new, shares v1's `Ledger`)
* `writeup/figures/fig59_route_port_v1.png`, `writeup/figures/fig60_route_port_v2.png` (new)
* `writeup/README.md` — two figure pointers, two reproduce lines, and a flagged block
  recording the three discrepancies. **No quoted number was changed.**
* `writeup/novelty/leg_60.md` — the pre-construction novelty pass (`PROCEED_AS_BOOKKEEPING`;
  nothing in print pre-empts either negative, and nothing lifts either ban).
