# Leg 86 (Route-PCB) — novelty pass: is the post-repair regression check of the line-sweep preconditioner already done?

**Pass date: 2026-08-06. Run BEFORE any construction, and committed before it, per the leg
contract.** `plan_of_record.py` was run first; every ban it prints was read (see §3).

## 0. What this leg claims, and what it does not

**Claimed:** a *software* fact — that the line-sweep preconditioner in
`solver/port_certification.py`, measured on the repository's own exactness gate and on a fresh
timing bench, is or is not unchanged in precision and in cost across leg 79's bench-repair
(commit `3f187d8`, the `_hypothesis_violations` domain guard on `radii_polynomial_status`).

**Not claimed:** any mathematical novelty whatsoever. This leg discovers nothing about the
Navier-Stokes, Boussinesq or Hou-Luo equations, moves no link of the L1→L4 chain, and produces
no new constant that any certificate depends on. It is a regression check with the same standing
as a test: it can only *withdraw* confidence, never add a result. Zero-novelty claim is the
honest description, so the external-literature dimension of the novelty pass is vacuous — there
is no published-record question to ask about "did this repo's own preconditioner change speed
last Thursday".

## 1. Prior art INSIDE this repository — the dimension that actually bites

Grepped before construction: `capabilities.py` (the `solver/port_certification.py` entry, full
current text, lines 103–118, re-read after leg 79's repair rewrote its `validated` field), every
`line_sweep_solve` call site, and every file mentioning "postrepair"/"post-repair".

| what exists | where | what it covers | why leg 86 is not a repeat |
|---|---|---|---|
| `test_7_line_sweep_is_an_exact_inverse` | `test_port_certification.py:150` | ONE configuration (seed 11, 48×16, drho 0.09, dbeta 0.033, c −1.0145), asserts `err < 1e-11` | its assertion is **~4 decades looser** than the 9.5e-16 that `capabilities.py` actually advertises; it would pass through a precision regression of four orders of magnitude without noticing. It is also a single-point check with no pre/post comparison and no timing at all. |
| `test_port_certification_regression.py` | repo root | leg 79's 11 fabrication labels, i.e. `radii_polynomial_status` ONLY | covers the repaired function, not the module's *other* claim. It cannot see a collateral change in `line_sweep_solve`. |
| `experiments/p2_route_l_v1_precond.py` + `writeup/data/p2_route_l_v1_precond.json` | the Route-L artifact | the Krylov ladders the sweep produces, banked pre-repair | measures the *consequence* (ladder residuals), not the sweep's own exactness or cost, and has not been re-run since the repair. Its numbers are a useful cross-check, not this gate. |
| `test_route_g_perf.py` | repo root | Route-G collapse performance work | its own doc-string says the gates are correctness gates, "not a timing anecdote" — there is **no timing bench anywhere in this repository**, so leg 86 has to build one, and must build it in a form that is not an anecdote either (see §2). |
| DIRECTION.md leg 87 (Route-IVB) | queue | the same closing-the-loop move for `solver/interval.py` / leg 69's repair | different module, different repair, different leg's territory. Sibling, not duplicate. |

**Conclusion of the in-repo pass: NOT a repeat.** Nothing in the repository has compared this
preconditioner's numerics or its cost across commit `3f187d8`, and the one test that touches its
precision is calibrated four decades away from the claim under audit.

## 2. Method novelty, and the one methodological trap

The method is ordinary — differential testing of one module across one commit — with one
non-obvious requirement that this pass exists to pin down:

**A timing comparison with no measured noise floor is not a measurement.** "Within normal
benchmark variance" is unanswerable unless the variance is itself measured in the same run, on
the same machine, under the same load. So the bench must carry a **null arm**: post-repair timed
against post-repair, interleaved with the real pre-vs-post arm, so the null ratio is the noise
band the real ratio is judged against. Reporting a bare speed ratio would repeat exactly the
"timing anecdote" `test_route_g_perf.py` names and refuses. This is pre-committed here, before
any number is seen.

Second pre-commitment, on the precision side: the pre/post comparison is **bit-for-bit on the
returned arrays**, not "both are small". A guard added to a hot path can perturb the last bits
without breaking a 1e-11 assertion; identical endpoint bit patterns is the only statement that
distinguishes "unchanged" from "still passes".

## 3. Bans (`plan_of_record.py`, read in full)

None are tripped. This is not a gCLM measurement (it measures no model at all), not a Route-D
bound-sharpening leg, not a DSS re-ask, not a beta re-measurement on the 2D object, not a
re-test of the scaling gauge, no GA compute, and it re-opens no closed stage. The standing ban
"building a solver without grepping `capabilities.py` for the object first" was honoured before
any file was written — see §1. Nothing is built that a capability entry already provides: the
timing bench has no precedent in the repository, and the exactness battery is a strict
tightening plus a pre/post arm that `test_7` does not have.

## 4. External literature

Vacuous by §0 — the claim is about this repository's own commit, not about the published record.
No arXiv or journal search is applicable, and none is reported, so that no absence is later
mistaken for a searched-and-empty result.

---

## 5. FINDINGS (appended after construction, 2026-08-06)

The pass above was committed before any number was seen (`09b7de9`). What the run then measured:

**Gate answer: YES on both halves.**

| clause | measurement | judged against |
|---|---|---|
| P2 precision, canonical (`test_7`'s configuration) | **9.4723e-16**, *identical* pre and post | the advertised **9.5e-16** — 1.00× margin |
| P2 precision, whole battery, pre vs post | **20/20 cases bit-identical**, **0 of 131 136 entries** differing, worst ULP gap **0** | the pre-commitment in §2: bit-for-bit, not "both are small" |
| P3 timing, 300×48 | **+0.21%** (24.33 → 24.38 ms) | null arm **0.29%** |
| P3 timing, 96×32 | **+1.12%** (5.76 → 5.83 ms) | null arm **0.20%**; budget max(3× null, 10%) |
| P1 static | repair is **+58/−0** lines over `_hypothesis_violations`, `radii_polynomial_status`; **0** defs on the sweep's call path or adjacent hot path | the sweep's enumerated call path |
| P4 consequence | preconditioned Krylov ladder **3.603020e-14 at m = 80**, **4/4 rungs identical** pre vs post | each other |

**Both pre-commitments earned their keep.** The bit-for-bit arm is what upgrades the answer from
"still passes a tolerance" to "nothing moved", and it is the only arm that could have caught a
sub-tolerance perturbation. The null arm is what makes the timing half answerable at all: a first
run on a loaded machine showed a **−5.94%** pre/post ratio at 300×48 with a **2.15%** null and a
*sign-inconsistent* +4.00% at 96×32 — visibly noise, and visibly noise *because the null was
there*. The clean run gives sub-percent deviations against sub-percent nulls. Without the null,
the first run's −5.94% would have been reportable as a 6% speed-up, which it is not.

**The one thing the novelty pass predicted and the run confirmed.** §1 flagged that `test_7`'s
`err < 1e-11` sits ~4 decades from the 9.5e-16 claim. Measuring at the claim's own resolution
turned up a scope caveat nobody had recorded: the battery's **worst** residual is **1.008e-14 =
10.61×** the advertised figure, on the 300×48 grids. It is **not** a regression — it is *exactly
equal* pre and post — but "gated to 9.5e-16" is a one-configuration number being read as uniform.
Reported, not patched: `capabilities.py` and `test_port_certification.py` are both outside this
leg's territory and neither was touched. Gate 1 of `test_port_certification_postrepair.py` holds
the canonical configuration to the advertised number from a file this leg does own, which closes
the four-decade gap without editing anyone else's.
