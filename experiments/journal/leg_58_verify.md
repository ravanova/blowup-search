# Leg 58 VER-A — re-measuring leg 54's headline before NG builds a proposition on it

**Branch** `verify/58-ng-headline`. **Trigger (a), lesson 85.** **Verdict: the headline
CHECKS OUT.** Three caveats below, none of which move the gate answer; two of them affect
how leg 58 should *word* the proposition.

Script: `experiments/verify_leg58_headline.py` (mine; does not collide with leg 58's
territory). Output: `experiments/verify_leg58_headline.json`.

## What "independent" means here, and what it does not

`experiments/verify_leg58_headline.py` imports **only** `solver/spectral_certificate.py`.
It does not import leg 54's runner (`p2_route_mm_v1_shape.py`) or leg 53's assembler
(`p2_route_tc_v1_assemble.py`); the assembled operator, the weights, the bordered tail
inverse and all five admissible shapes are rebuilt from the primitives. That makes the
check independent of both legs' *assembly code*. It is **not** independent of the modelling
choice underneath — the compactified odd-sine basis, the bordering, the "shipped"
normalisation are leg 51-53's and are taken as given, as they must be for a
re-measurement.

The one thing that *is* re-derived from first principles is the structure (VER1): the
assembled `L`'s four blocks are checked entry-by-entry against
`bordered_linearization(M)`, the honest linearisation on modes `1..M` plus the gauge row
and `delta c_omega`. Leg 54's coupling blocks `Ltg`/`Lgt` are hand-written, so this is the
check that they are the operator's and not a transcription of it. **Max deviation
1.78e-15 over K = 2, 4, 6, 8** — including the far-field column, which is confirmed to be
exactly `L hhat` restricted to the finite rows and `T hhat` on the tail rows.

## VER2 — the battery. The headline reproduces.

True column-max of `I - A L` over the whole space, `M = K + 1024`, five admissible shapes
x two classes x two gauges x seven even splits (2, 4, 6, 8, 16, 32, 64).

| quantity | leg 54 | VER-A | rel. diff |
|---|---|---|---|
| best admissible `Z1` | 8.9591 | **8.959091** (`ff_lift`, algebraic `s=0.3`, `null`, `K=2`) | 9.9e-07 (rounding only) |
| block-diagonal baseline | 10.4584 | **10.458427** (same cell) | 2.6e-06 (rounding only) |
| improvement factor | 1.1674 | **1.167354** | — |

The two numbers are attained in the **same** `(class, gauge, K)` cell, so the 1.167x is a
like-for-like comparison and not a min-over-one-set against a min-over-another.

Beyond the headline: **all 140 admissible cells** (5 shapes x 2 classes x 2 gauges x 7
splits) agree with leg 54's committed `writeup/data/p2_route_mm_v1_shape.json` to a
**relative deviation of exactly 0**. My `ff_lift` scores its four candidate functionals on
the **true full residual**, where leg 54 scores them on a shortcut that assumes the top
block is untouched by a rank-one `A21`; the shortcut is vindicated — same winner, same
number.

## VER3 — MM-1 is an exact equality, and its scope is very slightly sharper than stated

`Z1 >= |1 - K/2| (w_{K+1}/w_K) ||A_tail e_{K+1}||_w / w_{K+1}`, recomputed from its three
stated factors against the measured `(tail, Gamma)` sub-block norm:

* **equality, max |ratio - 1| = 3.55e-15** (leg 54: 1.89e-15). Same magnitude; mine is
  larger only because my sweep also includes the odd splits `K = 3, 5`, where the equality
  also holds exactly. Both numbers are float noise on an identity.
* second factor range **0.941176 .. 1.331843**, matching leg 54's committed JSON exactly.
* smallest even `K` with RHS > 1: **flat 6, algebraic 4** — leg 54's restriction confirmed.
* leg 54's odd-split obstruction reproduced independently: max smallest-singular-value of
  the augmented finite block over odd `K` = **2.5e-17**, min over even `K` = **2.08e-04**.
  Every odd split is exactly singular; even splits are not.

## VER4 — the headline is not a truncation artifact, but it is only stable to 3 s.f.

| `M_extra` | best admissible `Z1` | block-diag baseline |
|---|---|---|
| 512 | 8.953141 | 10.444130 |
| 1024 | **8.959091** | **10.458427** |
| 2048 | 8.962800 | 10.467351 |

Same minimising cell (`ff_lift`, algebraic, `null`, `K = 2`) at every truncation. The value
drifts **upward** with `M` — roughly +0.04% per doubling, decelerating — so the finite
truncation is if anything *flattering* the certificate, and the no-go is not weakened by
taking `M` larger. But it means the fifth digit of `8.9591` is a property of
`M_extra = 1024`, not of the operator.

## The three caveats leg 58 should carry into the proposition

1. **Quote `8.96`, not `8.9591`, as an `M`-independent quantity** (VER4). The number is
   right; the precision it is stated to is a truncation parameter's. `8.9591 at
   M = K + 1024` is fine; a bare `8.9591` is over-stated.
2. **`K >= 6` in the flat class is a restriction over EVEN splits, and should say so.**
   The RHS clears 1 at `K = 5` in the flat class (1.4927), not `K = 6`; `K = 6` is the
   smallest *even* split that clears it, and even-ness is forced separately, by the odd-K
   singularity. Both facts are leg 54's own and both are confirmed here — but "restricted
   to `K >= 6` flat" reads as a property of the inequality when it is a property of the
   inequality *composed with* the admissibility of the split. Stated as one clause in a
   proposition, that is the kind of seam a referee opens. Unconditionally the flat-class
   statement is `K >= 5`.
3. **Leg 54's journal prose says the second factor is `0.94 .. 1.39`; its own committed
   JSON says `0.941176 .. 1.331843`, and so do I.** The `1.39` is not reproducible and
   appears to be a leftover from an earlier sweep. Leg 58 must quote the JSON, not the
   journal's GAP-2 paragraph. Not load-bearing — the factor is `O(1)` either way and MM-1's
   force comes from the `|1 - K/2|` prefactor — but it is wrong where it stands.

## What I did not check

* Not the `oracle_pinv` / `exact_inv` rows (inadmissible; leg 54 kills them via MM-3, and
  they are not in leg 58's proposition).
* Not MM-4's floor (`5.0444`) or MM-4c's rank-one counter-construction. The brief named
  three numbers; those are others, and leg 58's proposition does lean on the floor — with
  the scope correction VER-A2 already forced onto it (`A11` near `Gamma^-1`, not
  shape-independent). **Nobody has re-measured `5.0444` since that correction.**
  Flagged, not repaired.
* Not the positive control (`Z1 = 0.9156` at `mu = 2`) — but that one is already covered:
  leg 54's VER-A confirmed it independently at leg 53's level
  (`writeup/novelty/leg_54_verify.md`), so DIRECTION §58's necessity clause rests on a
  number that has been checked once by someone other than its author.
* Not the modelling layer beneath leg 51-53 (see above).

## Ledger discipline

Wrote only `experiments/journal/leg_58_verify.md`, `writeup/novelty/leg_58_verify.md`,
`experiments/verify_leg58_headline.py` and its JSON. Did not touch
`solver/spectral_certificate.py` (leg 58's exclusive territory), `experiments/JOURNAL.md`,
`LITERATURE_CHECK.md`, `plan_of_record.py`, `CONTINUATION_PROMPT.md` or
`PHASE2_P2_NOTES.md`. Did not re-run leg 54's own script in place, because it writes
`writeup/data/p2_route_mm_v1_shape.json` and that file is leg 54's committed artifact; the
row-by-row comparison against the committed JSON gives the same information without
clobbering it.
