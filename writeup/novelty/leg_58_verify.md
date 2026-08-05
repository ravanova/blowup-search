# Leg 58 — VER-A: independent re-measurement of leg 54's headline, before NG builds on it

**Role.** VER-A, paired to leg 58 (Route-NG), the critical-path leg. Lesson 85, trigger (a):
re-measure a headline before the leg that consumes it builds further on it. I report gaps;
I do not repair them. I have not touched `solver/spectral_certificate.py` (leg 58's
exclusive territory) or any of leg 54's owned files.

**Artifacts.** `experiments/verify_leg58_headline.py` — this pass's own runner, which
rebuilds the assembled operator, the weights, the bordered tail inverse and all five
admissible shapes from `solver/spectral_certificate.py` primitives, importing neither leg
54's runner nor leg 53's assembler — and `experiments/verify_leg58_headline.json`.

**Novelty status of this pass.** NONE claimed. A verification pass banks no novelty; the
literature question for the NG proposition (arXiv:2505.03091, Cadiot) belongs to leg 62 and
is untouched here.

---

## 1. What I independently CONFIRM, and to what precision

| headline | leg 54 | this pass | verdict |
|---|---|---|---|
| best admissible `Z1`, every shape/class/gauge/split | 8.9591 | **8.959091169104095** | confirmed, exact |
| — attained at | `ff_lift`, algebraic `s=0.3`, `K=2` | `ff_lift`, algebraic `s=0.3`, gauge `null`, `K=2` | confirmed |
| block-diagonal baseline | 10.4584 | **10.458427031841403** | confirmed, exact |
| improvement factor | 1.1674 | **1.167354** | confirmed |
| MM-1 is an exact equality | 1.89e-15 | **3.55e-15** | confirmed (both float noise) |
| MM-1 second factor range | 0.941176 .. 1.331843 | **0.941176 .. 1.331843** | confirmed, exact |
| smallest even `K` with MM-1 RHS > 1 | flat 6, algebraic 4 | **flat 6, algebraic 4** | confirmed |
| every odd split has a singular finite block | yes | **max smallest-sv over odd `K` = 2.5e-17**, min over even `K` = 2.08e-04 | confirmed |

Plus two checks leg 54 did not run:

* **Structure.** The assembled `L`'s four blocks agree entry-by-entry with
  `bordered_linearization(M)` — the honest linearisation on modes `1..M` plus gauge and
  `delta c_omega` — to **1.78e-15**, including the far-field column, which is confirmed to
  be exactly `L hhat`. Leg 54's coupling blocks are hand-written; they are the operator's.
* **Whole battery.** All **140** admissible cells (5 shapes x 2 classes x 2 gauges x 7 even
  splits) match the committed `writeup/data/p2_route_mm_v1_shape.json` to relative
  deviation **exactly 0** — not just the minimising cell.
* **`ff_lift`'s shortcut is sound.** Leg 54 scores its four candidate functionals on a
  shortcut that assumes a rank-one `A21` leaves the top block untouched. I scored them on
  the true full residual instead: same winner, same number.

## 2. Three caveats — wording, not arithmetic

None of these move the gate answer, and none of them make `8.96` wrong. All three are
places where leg 58's proposition, as DIRECTION §58 drafts it, would state something
slightly stronger or slightly other than what was measured.

1. **`8.9591` is stable only to three significant figures.** Re-run at `M_extra` 512 /
   1024 / 2048 the headline is **8.953141 / 8.959091 / 8.962800**, baseline **10.444130 /
   10.458427 / 10.467351** — same minimising cell throughout, drifting *upward* about
   +0.04% per doubling and decelerating. The truncation is flattering the certificate, so
   the no-go survives `M -> infinity` in the right direction; but the fifth digit belongs
   to `M_extra = 1024`, not to the operator. Quote `8.96`, or `8.9591 at M = K + 1024`.
2. **"Restricted to `K >= 6` flat" is a restriction over EVEN splits and should say so.**
   Unconditionally, MM-1's RHS clears 1 in the flat class at `K = 5` (RHS 1.4927); `K = 6`
   is the smallest *even* split that clears it, and even-ness is forced by a separate fact
   (the odd-K singularity). Composing two restrictions into one clause is the seam a
   referee opens on a negative result.
3. **Leg 54's journal prose contradicts its own JSON on the second factor.**
   `experiments/journal/leg_54.md` GAP 2 says the range is `0.94 .. 1.39`; the committed
   JSON says `0.941176 .. 1.331843` and so does this pass. The `1.39` is not reproducible.
   Leg 58 must quote the JSON.

## 3. Not checked

MM-4's floor `5.0444` — and specifically, nobody has re-measured it since VER-A2 forced
the scope correction onto it (`A11` in the neighbourhood of `Gamma^-1`; not
shape-independent). DIRECTION §58's proposition leans on that floor. The positive control
`Z1 = 0.9156` at `mu = 2` is *not* an open flank: leg 54's VER-A confirmed it independently
(`writeup/novelty/leg_54_verify.md`).

The modelling layer beneath leg 51-53 — the compactified odd-sine basis, the bordering, the
"shipped" normalisation — is taken as given, as it must be for a re-measurement.
