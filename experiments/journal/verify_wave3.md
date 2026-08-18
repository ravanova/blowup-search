# VERIFY WAVE 3 — unit `V-W3`, wave 4 verifier

Branch `verify/wave3`. Data `writeup/data/p2_verify_wave3_v1.json`.
Re-derivation script: `experiments/verify_wave3_rederive.py`.

---

## §0 — THE GATE AS GIVEN (committed before anything was checked)

Four items, pre-committed. Nothing added, nothing dropped.

**(1) Unit `E` — the H-hard diagnostic (`d0d72b1`).** Re-derive its headline **from
`writeup/data/p2_prog_r4_e_v1.json`, not from prose**. Claim on record: **16 attempts, 2 converged,
0 recovered any named row**, with a positive control passing at `‖R‖ ≈ 1.5e-10` **through E's own
predicate**, and two diagnostics — (i) `PULL_TO_LOW_S`, (ii) `MIXED` with `p = 0.9317`. Does the
artefact support **each**? Name any it does not.

**(2) `E`'s cost.** Record: `E` overran commissioning by ~**8×**: ≈**0.57 h/attempt** (5.687
core-hours + 0.806 h controls, 16 attempts) against a commissioning figure of **0.0713**. Re-derive
both sides. **Is the 8× real, and is `0.0713` the like-for-like comparison** — same thing, same unit?
A bogus overrun is as much a finding as a real one.

**(3) `V-W2` (wave-2 verifier, `594ff89`).** Verify the verifier. (a) Do its **four re-measurements**
land where its journal says? Re-run or re-derive each. (b) Its stated method includes **re-fetching
sources and recording SHA-256**. Does that appear in its artefacts with hashes present and
reproducible — or is it prose only?

**(4) `fig107`.** Record states `fig107` is **absent from the `P2_EVIDENCE` structure in
`writeup/build_figures.py`**. Confirm **mechanically** (grep/parse, not eyeball) and report what is
and is not registered.

### Pre-committed readings — binding

(a) **REPORT, DO NOT REPAIR.** A defect gets a location and a size, not a fix. A verifier that
repairs its own findings has destroyed the measurement. Includes `fig107`: it is **not** registered
by this unit.
(b) **Waves 1 and 3 ONLY, NEVER wave 4.** `V3` (`leg/399-v3-gradeA`) and `L2′` (`leg/397-l2-decay`)
are out of territory — not opened, not graded, not commented on. They land `UNVERIFIED` by design.
(c) A **PASS is a real result and so is a FAIL.** Per item: `CONFIRMED` / `REFUTED` / `PARTIAL` /
`UNREACHABLE`, with the discrepancy quantified when `PARTIAL` or `REFUTED`.
(d) Re-derive from `writeup/data/*.json` and code, **never from prose**. Missing artefact =
`UNREACHABLE` and a named finding; it does **not** become a pass.
(e) Lesson 68: a check is executable or it decays. Runnable re-derivation left under `experiments/`.
(f) `UNREACHABLE` and `THROTTLED` bank as themselves, never as zeros.
(g) **Verification is not movement toward Clay.** No link moves because a number checked out. Clay
odds ~0.05%, unmoved. Tier 2 is never a proof. Scale is not evidence.

---
